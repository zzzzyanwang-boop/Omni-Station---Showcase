# Rust Native Kernels

Rust-native kernels are used where the fastest correct physical computation requires bounded memory ownership, deterministic error handling, and reduced Python-loop or bridge overhead.

Reviewable responsibilities:

- preserve real Rust crate/file boundaries in the source-shaped tree while replacing implementation bodies with architecture notes
- define FFI/PyO3 contracts for schema, null policy, memory ownership, error propagation, and version compatibility
- operate on Arrow-compatible buffers or manifest-bound columnar artifacts instead of loose runtime objects
- fuse repeated rank, rolling, mask, neutralization, replay, codec, or stream operations when that removes scans, allocations, or copies
- publish parity evidence against reference implementations before a native path is allowed to replace a slower path
- expose timing, allocation, row-group, and partition counters as reviewable evidence rather than informal benchmark claims

Review signal:

- `source/rust/` shows crate/file ownership for the native surface
- `redacted_capabilities/native_compute_infrastructure/` shows capability boundaries whose exact implementation would over-disclose kernel internals
