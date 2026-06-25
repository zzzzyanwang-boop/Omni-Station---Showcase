# Purged CPCV Splitter

This capsule demonstrates public-safe cross-validation controls for research rows with forward label windows.

What it shows:

- validation folds are generated as combinations rather than a single latest split;
- training rows are purged when their label interval overlaps a validation interval plus embargo;
- group leakage is removed from train rows when the same group appears in validation;
- split validation fails closed if a hand-built split violates row overlap, group isolation, or embargo rules.

Run:

```powershell
python -m unittest discover code_capsules/purged_cpcv_splitter -p "test_*.py"
```

