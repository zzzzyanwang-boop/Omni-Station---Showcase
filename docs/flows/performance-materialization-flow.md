# Performance Materialization Flow

This flow describes how performance-sensitive research work is evaluated through physical execution shape, bounded scans, materialization control, cache policy, and equivalence checks.

```text
hot path identified
  -> input projection reduced
  -> source scan count bounded
  -> row materialization minimized
  -> cache reuse made manifest-bound
  -> Rust/vectorized/native kernel boundary chosen
  -> bridge parity and memory-ownership contract checked
  -> stage timing recorded
  -> equivalence check against prior artifact
  -> adoption gate
```

## Performance Rule

Performance claims should tie to physical work removed: fewer scans, fewer rows materialized, narrower projections, fewer copies, better cache locality, native/vectorized execution, or lower cross-language bridge overhead.
