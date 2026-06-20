# Native Compute

Native compute boundaries exist for performance-sensitive kernels where Python orchestration would create excessive scan, allocation, bridge, or loop overhead.

Reviewable responsibilities:

- define which work moves into Rust/vectorized/native execution and which work remains orchestration
- preserve Arrow/columnar memory semantics across language boundaries
- run equivalence checks against reference artifacts before a native path can satisfy a gate
- surface memory, IO, partition, and kernel timing budgets instead of opaque wall-clock claims
- fail closed when a native extension is missing, stale, not parity-certified, or called with unsupported schema/null policy
- return manifest-ready artifacts rather than mutable in-process state
