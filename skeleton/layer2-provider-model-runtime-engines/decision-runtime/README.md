# Decision Runtime

Decision runtime resolves scores into action-intent or abstention semantics under explicit contracts.

Reviewable responsibilities:

- score-to-action boundary with declared eligibility, thresholds, and abstention semantics
- abstention policy for missing evidence, unsupported runtime posture, stale model state, or invalid replay coverage
- action validation that produces intent records rather than broker/order side effects
- runtime posture separation between offline evidence, promoted research, paper-capable boundary, and live-capable boundary
- native scoring or inference calls accepted only when the model, bridge contract, and output schema are version-bound
