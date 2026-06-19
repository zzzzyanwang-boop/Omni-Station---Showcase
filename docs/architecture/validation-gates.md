# Validation Gates

Validation gates prevent unsupported claims from moving downstream.

| Gate | Purpose |
| --- | --- |
| Contract gate | Required metadata and ownership are present |
| Lineage gate | Inputs and outputs are manifest-bound |
| Leakage gate | Evidence respects train/test and point-in-time boundaries |
| Quality gate | Metrics meet declared thresholds without hidden exclusions |
| Claim gate | The claim does not exceed the available evidence |
| Promotion gate | Offline evidence is not confused with live readiness |

Gate outcomes: `passed`, `blocked`, `deferred`, or `diagnostic`.
