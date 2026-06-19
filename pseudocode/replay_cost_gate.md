# Pseudocode: Replay and Cost Gate

```text
function evaluate_replay_cost(signal_manifest, replay_manifest):
    assert signal_manifest.content_hash_verified
    assert replay_manifest.deterministic_hash_verified

    cost_evidence = compute_cost_evidence(
        fill_model,
        slippage_model,
        latency_model,
        transaction_cost_model
    )

    if cost_evidence.missing_required_component:
        return blocked("incomplete_execution_cost_evidence")

    if not cost_evidence.economic_gate_passed:
        return blocked("economic_gate_failed")

    return admitted("offline_economic_evidence")
```

Design point: mark-to-market diagnostics are not enough for economic approval.

