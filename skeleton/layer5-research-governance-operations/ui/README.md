# UI

UI surfaces present reviewable state and operator decisions.

Review concepts:

- work order status with route, owner, stage, blocker, and next permitted action
- evidence lineage view from source manifest to artifact, gate, review decision, and closure case
- gate result view that separates admitted, blocked, diagnostic, and deferred claims
- closure case review with memory entry, retirement/waiver status, and downstream eligibility
- native/runtime telemetry surfaced only as bounded counters and status projections

UI source bodies, credentials, endpoints, and operational state are represented only through sanitized read-model contracts.
