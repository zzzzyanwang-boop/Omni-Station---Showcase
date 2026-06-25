//! Public-safe toy sequence tensor native kernel.
//!
//! This crate demonstrates the shape of a native boundary: explicit metadata,
//! deterministic validation errors, bitmap packing, contiguous anchor runs, and
//! row-major sequence gathering. It contains no private strategy, model, data,
//! or production bridge code.

use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DescriptorRun {
    pub start_index: usize,
    pub len: usize,
    pub first_anchor: usize,
    pub last_anchor: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum KernelError {
    InvalidFeatureCount,
    RaggedRowMajorInput {
        value_count: usize,
        feature_count: usize,
    },
    AnchorOutOfBounds {
        anchor: usize,
        lookback: usize,
        row_count: usize,
    },
}

impl fmt::Display for KernelError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            KernelError::InvalidFeatureCount => write!(formatter, "feature_count must be positive"),
            KernelError::RaggedRowMajorInput {
                value_count,
                feature_count,
            } => write!(
                formatter,
                "value_count {value_count} is not divisible by feature_count {feature_count}"
            ),
            KernelError::AnchorOutOfBounds {
                anchor,
                lookback,
                row_count,
            } => write!(
                formatter,
                "anchor {anchor} with lookback {lookback} is outside row_count {row_count}"
            ),
        }
    }
}

impl std::error::Error for KernelError {}

pub fn kernel_metadata() -> &'static str {
    "toy_sequence_tensor_kernel:v1:row_major_f32"
}

pub fn pack_validity_bitmap(valid: &[bool]) -> Vec<u8> {
    let mut bytes = vec![0_u8; valid.len().div_ceil(8)];
    for (index, is_valid) in valid.iter().enumerate() {
        if *is_valid {
            bytes[index / 8] |= 1 << (index % 8);
        }
    }
    bytes
}

pub fn find_contiguous_anchor_runs(anchors: &[usize]) -> Vec<DescriptorRun> {
    if anchors.is_empty() {
        return Vec::new();
    }

    let mut runs = Vec::new();
    let mut start_index = 0;
    let mut first_anchor = anchors[0];
    let mut previous_anchor = anchors[0];

    for (index, anchor) in anchors.iter().copied().enumerate().skip(1) {
        if anchor == previous_anchor + 1 {
            previous_anchor = anchor;
            continue;
        }

        runs.push(DescriptorRun {
            start_index,
            len: index - start_index,
            first_anchor,
            last_anchor: previous_anchor,
        });
        start_index = index;
        first_anchor = anchor;
        previous_anchor = anchor;
    }

    runs.push(DescriptorRun {
        start_index,
        len: anchors.len() - start_index,
        first_anchor,
        last_anchor: previous_anchor,
    });
    runs
}

pub fn gather_sequences(
    row_major_values: &[f32],
    feature_count: usize,
    anchors: &[usize],
    lookback: usize,
) -> Result<Vec<f32>, KernelError> {
    if feature_count == 0 || lookback == 0 {
        return Err(KernelError::InvalidFeatureCount);
    }
    if row_major_values.len() % feature_count != 0 {
        return Err(KernelError::RaggedRowMajorInput {
            value_count: row_major_values.len(),
            feature_count,
        });
    }

    let row_count = row_major_values.len() / feature_count;
    let mut output = Vec::with_capacity(anchors.len() * lookback * feature_count);
    for anchor in anchors.iter().copied() {
        if anchor >= row_count || anchor + 1 < lookback {
            return Err(KernelError::AnchorOutOfBounds {
                anchor,
                lookback,
                row_count,
            });
        }
        let start_row = anchor + 1 - lookback;
        for row in start_row..=anchor {
            let offset = row * feature_count;
            output.extend_from_slice(&row_major_values[offset..offset + feature_count]);
        }
    }
    Ok(output)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn packs_validity_bitmap_lsb_first() {
        let bytes = pack_validity_bitmap(&[
            true, false, true, true, false, false, false, true, true,
        ]);

        assert_eq!(bytes, vec![0b1000_1101, 0b0000_0001]);
    }

    #[test]
    fn finds_contiguous_anchor_runs() {
        let runs = find_contiguous_anchor_runs(&[2, 3, 4, 8, 9, 12]);

        assert_eq!(
            runs,
            vec![
                DescriptorRun {
                    start_index: 0,
                    len: 3,
                    first_anchor: 2,
                    last_anchor: 4,
                },
                DescriptorRun {
                    start_index: 3,
                    len: 2,
                    first_anchor: 8,
                    last_anchor: 9,
                },
                DescriptorRun {
                    start_index: 5,
                    len: 1,
                    first_anchor: 12,
                    last_anchor: 12,
                },
            ]
        );
    }

    #[test]
    fn gathers_row_major_sequences() {
        let values = vec![
            1.0, 10.0, 2.0, 20.0, 3.0, 30.0, 4.0, 40.0,
        ];

        let gathered = gather_sequences(&values, 2, &[1, 3], 2).unwrap();

        assert_eq!(gathered, vec![1.0, 10.0, 2.0, 20.0, 3.0, 30.0, 4.0, 40.0]);
    }

    #[test]
    fn rejects_out_of_bounds_anchor() {
        let values = vec![1.0, 2.0, 3.0, 4.0];

        let error = gather_sequences(&values, 1, &[0], 2).unwrap_err();

        assert_eq!(
            error,
            KernelError::AnchorOutOfBounds {
                anchor: 0,
                lookback: 2,
                row_count: 4,
            }
        );
    }

    #[test]
    fn rejects_ragged_row_major_input() {
        let error = gather_sequences(&[1.0, 2.0, 3.0], 2, &[1], 1).unwrap_err();

        assert_eq!(
            error,
            KernelError::RaggedRowMajorInput {
                value_count: 3,
                feature_count: 2,
            }
        );
    }
}
