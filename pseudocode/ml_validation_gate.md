# Pseudocode: ML Validation Gate

```text
function validate_model_run(training_manifest):
    assert training_manifest.fold_policy == "purged_embargoed"
    assert training_manifest.feature_selection == "fold_local_only"
    assert training_manifest.oof_predictions.manifest_bound

    if training_manifest.uses_test_fold_selection:
        return blocked("test_fold_leakage")

    if not training_manifest.calibration_artifact.present:
        return blocked("missing_calibration")

    if not training_manifest.registry_candidate.has_claim_limits:
        return blocked("missing_claim_limits")

    return admitted("offline_model_evidence_only")
```

Design point: offline ML evidence is not inference eligibility by itself.

