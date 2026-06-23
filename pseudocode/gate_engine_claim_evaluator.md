# Gate Engine Claim Evaluator Pseudocode

This pseudocode shows how a gate evaluates a requested claim against evidence and consumer permissions.

```text
function evaluate_claim(contract, evidence_envelope, requested_claim, requested_consumer):
    require contract.status == "passed"
    require evidence_envelope.contract_ref == contract.contract_id

    if requested_consumer not in contract.allowed_consumers:
        return blocked("consumer_not_authorized")

    if requested_claim.scope exceeds evidence_envelope.claim_limits:
        return blocked("claim_scope_exceeds_evidence")

    for artifact_ref in evidence_envelope.artifact_refs:
        manifest = resolve_manifest(artifact_ref)
        if manifest.status not in ["passed", "contract_bound"]:
            return blocked("artifact_not_eligible")
        if manifest.schema_hash is missing or manifest.content_hash is missing:
            return blocked("artifact_not_content_bound")

    for obligation in required_obligations(contract, requested_consumer):
        if obligation not satisfied by evidence_envelope:
            return blocked("missing_required_obligation")

    return passed({
        "admitted_claim": requested_claim,
        "allowed_consumer": requested_consumer,
        "claim_limits": evidence_envelope.claim_limits
    })
```

Review signal:

- the gate evaluates a specific claim for a specific consumer
- successful computation is not enough
- missing manifests, missing obligations, and scope overclaiming block the claim

