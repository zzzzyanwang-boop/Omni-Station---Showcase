# Layer 1 - Data / Compute / Artifact Infrastructure

Layer 1 owns the physical substrate: data layout, columnar storage, artifact storage, compute execution, Rust-native runtime surfaces, cache lifecycle, checkpoints, station runners, and progress telemetry.

Review focus:

- data-plane contracts that bind source identity, schema hash, content hash, and point-in-time eligibility
- Parquet/Arrow and manifest-backed storage with projection and partition control
- cache and checkpoint lifecycle with stale-artifact rejection
- atomic writes and storage-location ownership that prevents partial publication
- Rust-native bus, codec, query, feature-stream, replay, profiling, and PyO3 bridge boundaries
- native/vectorized/GPU-ready compute surfaces with parity checks against reference artifacts
- progress and stage timing evidence that makes long-running materialization inspectable

Representative nodes:

- `data-plane/`
- `columnar-storage/`
- `artifact-storage/`
- `cache-checkpoints/`
- `station-runner/`
- `native-compute/`
- `rust-native-kernels/`
- `progress-telemetry/`
- `performance/`
