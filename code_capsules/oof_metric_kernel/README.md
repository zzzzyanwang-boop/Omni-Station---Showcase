# OOF Metric Kernel

This capsule implements a compact grouped OOF metric kernel. It demonstrates the metric shape without using production predictions, labels, features, or model code.

What it shows:

- one-pass sufficient statistics for Pearson IC;
- grouped metric aggregation by arbitrary stable dimensions;
- segmented average-rank IC with deterministic tie handling;
- finite-value filtering instead of silent NaN propagation.

Run:

```powershell
python -m unittest discover code_capsules/oof_metric_kernel -p "test_*.py"
```
