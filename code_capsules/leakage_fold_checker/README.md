# Leakage Fold Checker

This capsule implements a compact point-in-time and fold validation checker for synthetic research rows.

What it shows:

- feature availability must not be after the decision timestamp;
- label windows must begin after the decision timestamp and end after they begin;
- validation rows must be separated from training label windows by a configurable embargo;
- checks return structured issues instead of silently coercing bad rows.

Run:

```powershell
python -m unittest discover code_capsules/leakage_fold_checker -p "test_*.py"
```
