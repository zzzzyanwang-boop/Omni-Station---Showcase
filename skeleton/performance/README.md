# Performance Engineering

Performance work is evaluated by physical computation removed, not by wrapper complexity.

Public-safe responsibilities:

- column projection before scan and materialization
- columnar storage and partition policy
- vectorized engine boundaries
- native/Rust/GPU-ready hot paths
- cache lifecycle and manifest-bound reuse
- stage timing and bottleneck reports

Private kernels, benchmarks, runtime logs, and hardware-specific traces are not published.

