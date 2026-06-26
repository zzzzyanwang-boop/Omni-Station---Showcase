# Evidence DAG Validator

This capsule implements a small evidence graph validator. It demonstrates how decision-grade research artifacts can be checked through explicit nodes, dependencies, manifests, claims, and gate decisions.

What it shows:

- unique evidence node ownership;
- dependency existence and cycle detection;
- artifact manifest completeness, including schema, content, and lineage hashes;
- claim support through known artifact references;
- fail-closed behavior when a gate passes without support or a diagnostic node tries to make a decision-grade claim.

Run:

```powershell
python -m unittest discover code_capsules/evidence_dag_validator -p "test_*.py"
```

The example data is synthetic and does not represent any production research result.
