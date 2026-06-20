# Runtime

Runtime modules define posture, eligibility, and execution boundaries. They do not let research artifacts become side-effecting actions by default.

Reviewable responsibilities:

- runtime mode token or posture contract for offline, review, paper-capable, and live-capable states
- blocked-state behavior when evidence, replay, model eligibility, or safety gates are incomplete
- idempotency and duplicate-intent controls at the action boundary
- separation between decision intent, execution replay, order-management boundary, and broker/runtime adapters
- native actor or inference runtime calls only through explicit versioned contracts
- operator-visible reason codes for disabled or blocked runtime paths
