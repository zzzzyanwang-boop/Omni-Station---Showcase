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
| Source-boundary gate | Source, label, trainable, and OOF artifacts share compatible scope |
| Fold policy gate | OOF/CPCV/fold-local validation uses the declared fold and embargo policy |
| Runtime posture gate | Research evidence stays offline unless higher-level authority changes posture |
| Native parity gate | Rust/native outputs match the contract and supported reference behavior |

## Gate Outcomes

- `passed`: claim is supported inside the declared scope.
- `blocked`: claim is not supported and must not move downstream.
- `deferred`: claim needs additional evidence before review.
- `diagnostic`: useful for debugging, not for promotion.

## Gate Input Pattern

```yaml
GateInput:
  contract_ref: synthetic_contract
  evidence_envelope_ref: synthetic_envelope
  artifact_manifest_refs:
    - synthetic_manifest
  requested_consumer: synthetic_consumer
  claim_scope: synthetic_scope
  runtime_posture:
    offline_only: true
```

## Gate Output Pattern

```yaml
GateResult:
  status: passed_or_blocked
  admitted_claims:
    - synthetic_claim
  blocked_claims:
    - claim: synthetic_claim
      reason_code: synthetic_reason
  allowed_consumers:
    - synthetic_consumer
  blocked_consumers:
    - runtime_surface
  review_notes:
    - synthetic_review_note
```

## Common Blocking Conditions

- artifact exists but is not manifest-bound
- source scope is narrower than the claim
- label policy is not bound to the source manifest
- OOF run spec uses stale trainable evidence
- fold policy or embargo is missing
- metric result is diagnostic but requested for confirmation
- native bridge version does not match the engine contract
- replay evidence attempts to imply live readiness
