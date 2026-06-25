# Source Joinability Gate

This capsule demonstrates a public-safe preflight for source-part joinability.

What it shows:

- date-level coverage is not accepted as proof of factor/label joinability;
- source parts must overlap on symbol range and time range;
- row-count proof is required before a part can support a join claim;
- missing or non-overlapping parts fail closed with explicit issue codes.

Run:

```powershell
python -m unittest discover code_capsules/source_joinability_gate -p "test_*.py"
```

