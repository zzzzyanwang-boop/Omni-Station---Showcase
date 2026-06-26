const MAGIC: [u8; 4] = *b"OMNI";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WireFrame {
    pub msg_type: u8,
    pub sequence: u64,
    pub payload: Vec<u8>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError {
    BadMagic,
    BadChecksum,
    DuplicateNode(String),
    MissingInput { node: String, input: String },
    InvalidSourceInput(String),
    SequenceGap { expected: u64, observed: u64 },
    EmptyStream,
}

pub fn encode_wire_frame(frame: &WireFrame) -> Vec<u8> {
    let payload_len = frame.payload.len() as u32;
    let mut bytes = Vec::with_capacity(18 + frame.payload.len());
    bytes.extend_from_slice(&MAGIC);
    bytes.push(1);
    bytes.push(frame.msg_type);
    bytes.extend_from_slice(&frame.sequence.to_be_bytes());
    bytes.extend_from_slice(&payload_len.to_be_bytes());
    bytes.extend_from_slice(&frame.payload);
    bytes.extend_from_slice(&checksum(&bytes).to_be_bytes());
    bytes
}

pub fn decode_wire_frame(bytes: &[u8]) -> Result<WireFrame, BoundaryError> {
    if bytes.len() < 22 || bytes[0..4] != MAGIC {
        return Err(BoundaryError::BadMagic);
    }
    let checksum_start = bytes.len() - 4;
    let expected = u32::from_be_bytes(bytes[checksum_start..].try_into().unwrap());
    if checksum(&bytes[..checksum_start]) != expected {
        return Err(BoundaryError::BadChecksum);
    }
    let payload_len = u32::from_be_bytes(bytes[14..18].try_into().unwrap()) as usize;
    if checksum_start != 18 + payload_len {
        return Err(BoundaryError::BadChecksum);
    }
    Ok(WireFrame {
        msg_type: bytes[5],
        sequence: u64::from_be_bytes(bytes[6..14].try_into().unwrap()),
        payload: bytes[18..checksum_start].to_vec(),
    })
}

fn checksum(bytes: &[u8]) -> u32 {
    bytes.iter().fold(0u32, |acc, byte| acc.wrapping_mul(16777619) ^ (*byte as u32))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FeatureOp {
    Source,
    RollingMean { window: usize },
    Difference,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FeatureNode {
    pub id: String,
    pub op: FeatureOp,
    pub inputs: Vec<String>,
}

pub fn validate_feature_ir(nodes: &[FeatureNode]) -> Result<Vec<String>, BoundaryError> {
    let mut seen = Vec::<String>::new();
    for node in nodes {
        if seen.iter().any(|id| id == &node.id) {
            return Err(BoundaryError::DuplicateNode(node.id.clone()));
        }
        match node.op {
            FeatureOp::Source if !node.inputs.is_empty() => {
                return Err(BoundaryError::InvalidSourceInput(node.id.clone()));
            }
            FeatureOp::RollingMean { window } if window == 0 => {
                return Err(BoundaryError::MissingInput {
                    node: node.id.clone(),
                    input: "positive_window".to_string(),
                });
            }
            _ => {}
        }
        for input in &node.inputs {
            if !seen.iter().any(|id| id == input) {
                return Err(BoundaryError::MissingInput {
                    node: node.id.clone(),
                    input: input.clone(),
                });
            }
        }
        seen.push(node.id.clone());
    }
    Ok(seen)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JournalEvent {
    pub sequence: u64,
    pub stream: String,
    pub payload_hash: u64,
}

#[derive(Debug, Default)]
pub struct EventJournal {
    events: Vec<JournalEvent>,
}

impl EventJournal {
    pub fn append(&mut self, event: JournalEvent) -> Result<(), BoundaryError> {
        if event.stream.is_empty() {
            return Err(BoundaryError::EmptyStream);
        }
        let expected = self.events.last().map_or(1, |last| last.sequence + 1);
        if event.sequence != expected {
            return Err(BoundaryError::SequenceGap {
                expected,
                observed: event.sequence,
            });
        }
        self.events.push(event);
        Ok(())
    }

    pub fn replay_from(&self, sequence: u64) -> Vec<JournalEvent> {
        self.events
            .iter()
            .filter(|event| event.sequence >= sequence)
            .cloned()
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn wire_frame_round_trips_deterministically() {
        let frame = WireFrame {
            msg_type: 7,
            sequence: 42,
            payload: b"synthetic-cross-language-fixture".to_vec(),
        };

        let encoded = encode_wire_frame(&frame);

        assert_eq!(encoded, encode_wire_frame(&frame));
        assert_eq!(decode_wire_frame(&encoded).unwrap(), frame);
    }

    #[test]
    fn wire_frame_rejects_checksum_drift() {
        let frame = WireFrame {
            msg_type: 1,
            sequence: 1,
            payload: b"payload".to_vec(),
        };
        let mut encoded = encode_wire_frame(&frame);
        encoded[18] ^= 1;

        assert_eq!(decode_wire_frame(&encoded), Err(BoundaryError::BadChecksum));
    }

    #[test]
    fn feature_ir_rejects_unresolved_inputs() {
        let nodes = vec![FeatureNode {
            id: "rolling_close".to_string(),
            op: FeatureOp::RollingMean { window: 5 },
            inputs: vec!["close".to_string()],
        }];

        assert_eq!(
            validate_feature_ir(&nodes),
            Err(BoundaryError::MissingInput {
                node: "rolling_close".to_string(),
                input: "close".to_string(),
            })
        );
    }

    #[test]
    fn feature_ir_accepts_topological_order() {
        let nodes = vec![
            FeatureNode {
                id: "close".to_string(),
                op: FeatureOp::Source,
                inputs: vec![],
            },
            FeatureNode {
                id: "rolling_close".to_string(),
                op: FeatureOp::RollingMean { window: 5 },
                inputs: vec!["close".to_string()],
            },
            FeatureNode {
                id: "delta".to_string(),
                op: FeatureOp::Difference,
                inputs: vec!["rolling_close".to_string()],
            },
        ];

        assert_eq!(
            validate_feature_ir(&nodes).unwrap(),
            vec!["close".to_string(), "rolling_close".to_string(), "delta".to_string()]
        );
    }

    #[test]
    fn journal_replays_from_sequence_boundary() {
        let mut journal = EventJournal::default();
        journal
            .append(JournalEvent {
                sequence: 1,
                stream: "market".to_string(),
                payload_hash: 10,
            })
            .unwrap();
        journal
            .append(JournalEvent {
                sequence: 2,
                stream: "market".to_string(),
                payload_hash: 20,
            })
            .unwrap();

        assert_eq!(
            journal.replay_from(2),
            vec![JournalEvent {
                sequence: 2,
                stream: "market".to_string(),
                payload_hash: 20,
            }]
        );
    }

    #[test]
    fn journal_rejects_sequence_gaps() {
        let mut journal = EventJournal::default();

        assert_eq!(
            journal.append(JournalEvent {
                sequence: 2,
                stream: "market".to_string(),
                payload_hash: 20,
            }),
            Err(BoundaryError::SequenceGap {
                expected: 1,
                observed: 2,
            })
        );
    }
}
