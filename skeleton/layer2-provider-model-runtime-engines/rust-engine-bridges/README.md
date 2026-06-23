# Rust Engine Bridges

Rust engine bridges connect Research OS engine contracts to native crates without letting native execution bypass evidence, fold, or runtime-posture controls.

Reviewable responsibilities:

- PyO3/FFI boundary contracts for input schema, enum mapping, null policy, memory ownership, and error propagation
- version binding between a ResearchContract, engine wrapper, native crate, and produced artifact manifest
- parity tests that compare Rust-native results with reference Python/vectorized implementations at the same grain
- sequence tensor bridge checks for feature-validity packing, contiguous anchor runs, fixed-shape batch assembly, and non-finite diagnostics
- deterministic failure modes for unsupported schema, stale kernel version, missing extension, or incomplete bridge telemetry
- artifact output through Layer 3 manifests rather than direct caller-side mutation
- separation between research evaluation kernels, inference-side contracts, market-data/runtime actors, and execution/order boundaries

Review signal:

- native performance is treated as an engine contract and evidence problem, not as an untracked optimization behind the Python layer
