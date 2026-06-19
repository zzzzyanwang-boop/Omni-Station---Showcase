# Pseudocode: Factor Evidence Engine

```text
function evaluate_factor_candidate(candidate, input_bundle):
    assert input_bundle.source_lineage_valid
    assert input_bundle.point_in_time_policy_declared

    profile = compute_factor_profile(candidate, input_bundle)
    leakage = run_leakage_sentinel(candidate, input_bundle)
    redundancy = compute_redundancy_summary(candidate, input_bundle)
    risk_identity = classify_factor_identity(candidate, input_bundle)

    claims = []
    if profile.stable and leakage.passed and risk_identity.controls_complete:
        claims.append(admit("scoped_factor_evidence"))
    else:
        claims.append(block("unsupported_alpha_claim"))

    return publish_artifact({
        factor_profile: profile,
        leakage: leakage,
        redundancy: redundancy,
        risk_identity: risk_identity,
        claims: claims
    })
```

Design point: a raw diagnostic metric cannot become a production claim without lineage, leakage, risk, and review gates.

