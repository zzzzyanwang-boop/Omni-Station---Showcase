# Performance Materialization Flow

This flow describes how performance-sensitive research work is evaluated through physical execution shape, bounded scans, materialization control, cache policy, and equivalence checks.

```text
hot path identified
  -> input projection reduced
  -> source scan count bounded
  -> row materialization minimized
  -> cache reuse made manifest-bound
  -> vectorized / native kernel boundary chosen
  -> stage timing recorded
  -> equivalence check against prior artifact
  -> adoption gate
```

## Performance Rule

Performance claims should tie to physical work removed: fewer scans, fewer rows materialized, narrower projections, fewer copies, better cache locality, or native/vectorized execution.
