# Layer 1 - Data / Compute / Artifact Infrastructure

Layer 1 owns the physical substrate: data layout, columnar storage, artifact storage, compute execution, cache lifecycle, checkpoints, station runners, and progress telemetry.

Review focus:

- data-plane contracts
- Parquet/Arrow and manifest-backed storage
- cache and checkpoint lifecycle
- atomic writes and artifact roots
- native/vectorized/GPU-ready compute boundaries
- progress and stage timing evidence

Representative nodes:

- `data-plane/`
- `columnar-storage/`
- `artifact-storage/`
- `cache-checkpoints/`
- `station-runner/`
- `native-compute/`
- `progress-telemetry/`
- `performance/`
