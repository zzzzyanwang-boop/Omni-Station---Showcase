# Columnar Storage

Columnar storage keeps row-level research artifacts scan-efficient and reproducible.

Reviewable responsibilities:

- Parquet/Arrow primary layout for high-volume offline tables
- partition policy by stable research dimensions rather than ad hoc output folders
- projection width control before scan and materialization
- scan amplification control for repeated feature, replay, and validation passes
- streaming trainable writes and compact reject ledgers for high-volume joins
- Arrow-compatible memory handoff into Rust/native kernels where zero-copy or low-copy execution is required
