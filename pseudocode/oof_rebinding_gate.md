# OOF Rebinding Gate Pseudocode

This pseudocode shows how OOF launch readiness is bound to current source scope and trainable evidence.

```text
function evaluate_oof_rebinding(oof_run_spec, trainable_manifest, source_boundary, fold_policy):
    require oof_run_spec.runtime_posture.offline_only == true
    require fold_policy.embargo_policy is declared
    require trainable_manifest.label_reader_mode is declared

    if trainable_manifest.scope is narrower than oof_run_spec.claimed_scope:
        return blocked("trainable_scope_too_narrow")

    if trainable_manifest.source_boundary_hash != source_boundary.compatibility_hash:
        return blocked("source_boundary_mismatch")

    if trainable_manifest.fold_policy_ref != fold_policy.ref:
        return blocked("fold_policy_mismatch")

    if trainable_manifest.status not in ["passed", "contract_bound"]:
        return blocked("trainable_manifest_not_eligible")

    if oof_run_spec.model_policy_ref is missing:
        return blocked("missing_model_policy")

    return passed({
        "allowed_consumer": "full_manifest_oof_executor",
        "blocked_consumers": ["cpcv_until_oof_passes", "runtime_surface"],
        "claim_limits": trainable_manifest.claim_limits
    })
```

Review signal:

- OOF cannot widen scope beyond source and trainable evidence
- stale or narrow manifests block instead of creating a warning-only path
- CPCV and runtime surfaces stay blocked until OOF evidence exists and passes its gates

