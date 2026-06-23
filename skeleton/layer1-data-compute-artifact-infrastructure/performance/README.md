# Performance Engineering

Performance work is evaluated by physical computation removed, not by wrapper complexity.

Reviewable responsibilities:

- column projection before scan and materialization
- source-backed formula views when label semantics can be preserved without dense row-level writes
- date-level prepared label caches and scheduler caches when repeated trainable joins share source-bound inputs
- columnar storage and partition policy
- vectorized engine boundaries
- Rust-native and GPU-ready hot paths with explicit bridge contracts
- cache lifecycle and manifest-bound reuse
- stage timing and bottleneck reports
- parity and regression gates before replacing reference implementations
- claimed speedups tied to fewer scans, fewer allocations/copies, smaller materializations, lower bridge overhead, or native kernel time reduction

Kernels, benchmarks, runtime logs, and hardware-specific traces remain outside the review surface.
