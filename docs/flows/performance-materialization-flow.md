# Performance Materialization Flow

This flow describes how performance-sensitive research work is evaluated through physical execution shape, bounded scans, materialization control, cache policy, and equivalence checks.

```text
hot path identified
  -> input projection reduced
  -> source scan count bounded
  -> row materialization minimized
  -> source-backed view or compact layout selected when row-level materialization is avoidable
  -> partition/date-level scheduling chosen before repeated scans
  -> cache reuse made manifest-bound
  -> Rust/vectorized/native kernel boundary chosen
  -> bridge parity and memory-ownership contract checked
  -> fallback and compatibility modes made explicit
  -> stage timing recorded
  -> equivalence check against prior artifact
  -> adoption gate
```

## Performance Rule

Performance claims should tie to physical work removed: fewer scans, fewer rows materialized, narrower projections, fewer copies, better cache locality, native/vectorized execution, lower cross-language bridge overhead, avoided dense writes, or eliminated repeated same-part/date preparation work.

## Source-Backed View Pattern

For label and trainable-matrix workflows, the reviewable optimization is the physical plan:

- use source manifests and formula metadata as the label truth rather than writing dense row-level label tables by default
- resolve source-backed label records by partition/date before building label views
- stream matched trainable rows to parquet instead of collecting full joined tables
- record compact reject ledgers when row-level rejects are not needed for the gate
- build prepared date label caches only when multiple factor parts reuse the same date-level label work
- store engine id, physical layout, source policy, and scheduler/cache evidence in manifests and reports
