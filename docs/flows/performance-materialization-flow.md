# Performance Materialization Flow

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

Performance claims should tie to physical work removed: fewer scans, fewer rows materialized, narrower projections, fewer copies, better cache locality, or native/vectorized execution.
