# Sequence Tensor Native Kernel

This crate path represents the Rust/PyO3 native sequence tensor boundary used by the model-training wrapper.

Current source-shaped status:

- exports kernel metadata so Python can verify id, version, runtime posture, and supported encodings
- supports feature-validity bitmap packing
- supports contiguous anchor-run discovery
- supports fixed-shape sequence batch gathering
- validates shape, bounds, contiguity, and non-finite target behavior at the native boundary
- is called only through the Python Research OS engine wrapper, not directly by a research application

Reviewer signal:

- Rust is used for concrete high-volume tensor work, not only as a label
- native acceleration remains auditable through metadata, encoding checks, and fail-closed wrapper behavior
- fallback behavior is explicit in the Python wrapper and not hidden inside training logic
