# Validation Gates

Validation gates prevent unsupported claims from moving downstream.

## Gate Categories

| Gate | Purpose |
| --- | --- |
| Contract gate | Required metadata and ownership are present |
| Lineage gate | Inputs and outputs are manifest-bound |
| Leakage gate | Evidence respects train/test and point-in-time boundaries |
| Quality gate | Metrics meet declared thresholds without hidden exclusions |
| Claim gate | The claim does not exceed the available evidence |
| Promotion gate | Offline evidence is not confused with live readiness |

## Gate Outcomes

- `passed`: claim is supported inside the declared scope.
- `blocked`: claim is not supported and must not move downstream.
- `deferred`: claim needs additional evidence before review.
- `diagnostic`: useful for debugging, not for promotion.

