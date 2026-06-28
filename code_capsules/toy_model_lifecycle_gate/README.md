# Toy Model Lifecycle Gate

This capsule demonstrates a public-safe machine-learning research lifecycle on synthetic rows:

```text
trainable manifest
  -> purged fold row-set proof
  -> deterministic toy branch training
  -> OOF prediction manifest
  -> calibration, OOD, and uncertainty diagnostics
  -> model card
  -> prediction replay compatibility
  -> branch eligibility gate
```

The implementation is deliberately compact. It is not a trading model and does not contain production feature logic, model weights, data, thresholds, or runtime configuration.

Review signal:

- model evidence is manifest-bound rather than a loose score file;
- fold row-set proof is required before OOF evidence can support a model card;
- stale trainables, non-finite scores, missing calibration, OOD drift, proxy scores, replay schema mismatch, and diagnostic artifacts all fail closed;
- pass and blocked outcomes are pinned to golden reports under `examples/`.

Run:

```powershell
python -m unittest discover code_capsules/toy_model_lifecycle_gate -p "test_*.py"
python -m code_capsules.toy_model_lifecycle_gate --scenario pass
python -m code_capsules.toy_model_lifecycle_gate --scenario blocked
```
