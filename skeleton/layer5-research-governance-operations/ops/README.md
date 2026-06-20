# Operations

Operations surfaces coordinate bounded runs and review handoffs.

Review scope:

- conceptual run lifecycle from queued, running, blocked, review-ready, closed, waived, or retired
- safe publication boundary for artifacts, gate packets, read models, and closure records
- synthetic status records showing allowed next action and blocker reason
- operator handoff semantics for long-running materialization, validation, replay, or review packets
- fail-closed behavior when route ownership, evidence state, or publication identity is incomplete

Runtime queues, service controls, machine paths, and logs are represented only through sanitized state projections.
