# Route Authority Registry

The route authority registry connects governed route state to executable evidence contracts.

Reviewable responsibilities:

- route id binding between WorkOrder, research application, contract, and gate state
- stage eligibility for discovery, freeze, confirmation, replay, promotion review, closure, waiver, or retirement
- owner and reviewer authority that prevents orphaned or self-authorized evidence paths
- blocked stage transitions when evidence, review ownership, trial budget, or closure state is incomplete
- read-model projection for UI and operator surfaces without exposing runtime internals
