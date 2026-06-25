# Source-Backed Label View Planner

This capsule demonstrates a public-safe physical-plan idea: represent labels as a manifest-bound source-backed view when dense row-level label materialization is not required.

What it shows:

- required source columns are validated before planning;
- projected columns are minimized to entity, time, partition keys, and expression inputs;
- the plan records whether it is a logical view or dense materialization;
- dense writes are treated as a physical cost, not as a default.

Run:

```powershell
python -m unittest discover code_capsules/source_backed_label_view -p "test_*.py"
```
