# End-to-End Toy Research Flow

This capsule connects the public-safe capsule implementations into one executable toy flow:

1. build a source-backed label physical plan;
2. validate point-in-time rows and fold embargo;
3. compute grouped OOF metrics;
4. assemble synthetic evidence artifacts;
5. validate the resulting Evidence DAG gate.

Run:

```powershell
python -m code_capsules.e2e_toy_research_flow.src.toy_research_flow
python -m unittest discover code_capsules/e2e_toy_research_flow -p "test_*.py"
```

The output is a synthetic gate packet. It is designed to prove executable contract flow, not strategy performance.
