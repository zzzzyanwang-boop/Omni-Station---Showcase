# Pseudocode: Research Run Orchestrator

This is language-neutral pseudocode, not production source code.

```text
function run_research_work_order(work_order):
    assert work_order.owner is not empty
    assert work_order.acceptance_signal is explicit

    contract = build_contract(work_order)
    if contract.missing_required_metadata:
        return blocked("missing_contract_metadata")

    evidence_dag = build_evidence_dag(contract)
    input_bundle = resolve_manifest_bound_inputs(evidence_dag)
    if input_bundle.has_loose_or_stale_inputs:
        return blocked("invalid_input_lineage")

    engine_result = run_declared_engines(contract, input_bundle)
    manifests = publish_output_manifests(engine_result)
    envelope = build_evidence_envelope(contract, manifests)

    gate_result = run_review_gates(envelope)
    closure_case = write_closure_case(work_order, gate_result)
    return closure_case
```

Design point: the orchestrator never discovers artifacts by `latest` naming or filesystem globbing.

