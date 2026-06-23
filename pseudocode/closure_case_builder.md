# Closure Case Builder Pseudocode

This pseudocode shows how closure is separated from metric computation.

```text
function build_closure_case(route, evidence_index, closure_policy):
    require route.stage in ["confirmation_complete", "blocked", "retirement_review"]
    require closure_policy is declared

    admitted = collect_gate_results(evidence_index, status="passed")
    blocked = collect_gate_results(evidence_index, status="blocked")
    deferred = collect_gate_results(evidence_index, status="deferred")

    if any_required_gate_missing(closure_policy, evidence_index):
        return closure_case(status="incomplete", blockers=["missing_required_gate"])

    return closure_case({
        "route_id": route.route_id,
        "admitted_claims": admitted.claims,
        "blocked_claims": blocked.claims,
        "deferred_claims": deferred.claims,
        "scope_limits": merge_claim_limits(admitted),
        "residual_risks": summarize_residual_risks(evidence_index),
        "memory_entry": build_research_memory(route, admitted, blocked, deferred)
    })
```

Review signal:

- closure consumes gate results; it does not recompute metrics
- blocked and deferred claims are retained in memory
- residual risk and claim limits remain visible after a route closes

