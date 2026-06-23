# Source-Backed Label View Pseudocode

This pseudocode shows the contract shape for a source-backed label view. It is not source code and does not include label formulas.

```text
function build_source_backed_label_view(contract, source_manifest, label_policy):
    require contract.runtime_posture.offline_only == true
    require source_manifest.scope satisfies contract.source_boundary
    require label_policy.formula_id is declared
    require label_policy.horizon_policy is declared
    require label_policy.cost_dimension is declared

    source_parts = resolve_source_parts(source_manifest, contract.panel_scope)
    if source_parts are missing:
        return blocker("missing_source_parts")

    schema_proof = verify_schema_hashes(source_parts)
    if schema_proof.status != "passed":
        return blocker("source_schema_mismatch")

    view_manifest = {
        artifact_kind: "source_backed_label_view",
        source_refs: source_parts.manifest_refs,
        formula_ref: label_policy.formula_id,
        horizon_policy: label_policy.horizon_policy,
        cost_dimension: label_policy.cost_dimension,
        materialization_policy: "logical_view",
        claim_limits: contract.claim_limits
    }

    return evidence_envelope(view_manifest, tier="contract_bound")
```

Review signal:

- the label truth is source-bound
- dense row-level labels are not written unless the contract requires them
- downstream readers must consume the manifest-aware view
- missing source, schema drift, or missing formula policy blocks the view

