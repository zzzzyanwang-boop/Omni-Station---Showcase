# ML Training and Validation Flow

This flow demonstrates model evidence governance without exposing private models, weights, features, or data.

```text
model family spec
  -> training run contract
  -> purged / embargoed fold policy
  -> fold-local feature selection
  -> bounded training run
  -> OOF prediction manifest
  -> calibration artifact
  -> registry candidate
  -> inference eligibility gate
```

## Gate Rule

If feature selection sees test-fold information, if OOF predictions are not manifest-bound, or if calibration evidence is missing, promotion remains blocked.

