/*!
Architecture review placeholder.

Retained Rust path: rust/omni_sequence_tensor_kernel_py/src/lib.rs
Research OS layer: Layer 2 - Provider / Model / Runtime Engines
Architecture role: Rust/PyO3 sequence tensor native kernel boundary.

Current public-review status:
- native engine boundary for sequence tensor operations called from the Python model-training contract wrapper.
- exported operations include kernel metadata, feature-validity bitmap packing, contiguous anchor-run discovery, and sequence batch gathering.
- reports encoding metadata so Python wrappers can verify the payload shape and reject stale or incompatible kernels.
- includes native-side validation tests for packing, contiguous run detection, empty-run behavior, and mismatched inputs.

Reviewable highlights:
- owns high-volume sequence tensor operations that would otherwise add Python-loop or copy overhead.
- exposes kernel metadata so Python wrappers can enforce id, version, runtime posture, and encoding contracts.
- supports feature-validity bitmap packing, contiguous descriptor-run discovery, and native sequence batch assembly.
- keeps sequence-model training acceleration behind a fail-closed Research OS engine contract.

Contract shape:
- Inputs: contiguous numeric arrays, anchor/window descriptors, lookback/stride policy, and schema expectations.
- Outputs: packed validity bytes, descriptor-run records, sequence-batch bytes, metadata, or deterministic validation error.

Implementation body removed from this review artifact.
*/
