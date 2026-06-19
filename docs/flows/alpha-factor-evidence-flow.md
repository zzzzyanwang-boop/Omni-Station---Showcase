# Alpha and Factor Evidence Flow

This flow demonstrates factor profiling without exposing private formulas or results.

```text
factor candidate
  -> source lineage check
  -> point-in-time check
  -> coverage and sample scope
  -> Rank IC / ICIR style diagnostics
  -> redundancy and correlation check
  -> leakage sentinel
  -> risk identity ledger
  -> admitted / blocked / deferred claim
```

## Public-Safe Example

See `examples/toy_factor_profile.json` and `examples/toy_risk_identity_ledger.json`.

## Claim Rule

Raw predictive diagnostics do not imply production alpha, neutralized alpha, or live eligibility.

