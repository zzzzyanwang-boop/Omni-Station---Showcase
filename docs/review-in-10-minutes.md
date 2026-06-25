# Review in 10 Minutes

This is the fastest path for a technical architecture review of the showcase.

| Step | Review target | Question to answer | Public proof |
|---|---|---|---|
| 1 | `README.md` | What system is being reviewed, and what is deliberately not exposed? | Review surface counts, Research OS layer summary, and `SECURITY.md` |
| 2 | `docs/architecture/five-layer-architecture.md` | Does the system separate governance, applications, evidence contracts, engines, and infrastructure? | Five-layer model and source-shaped tree |
| 3 | `docs/review-traceability.md` | Do representative real module paths map to concrete capabilities and proof artifacts? | Source-to-proof matrix |
| 4 | `python scripts/verify_showcase.py` | Can the public artifact be verified without private code or data? | Tests, redaction scan, placeholder lint, inventory checks, and benchmark smoke |
| 5 | `code_capsules/` | Are the core claims backed by executable public-safe implementations? | Evidence DAG, leakage, OOF, CPCV, manifest hashing, joinability, label-view, Rust kernel, and toy E2E capsules |
| 6 | `docs/redaction-policy.md` | Is the public boundary intentional and auditable? | Redaction rules, sanitized capability boundaries, and tracked-file hygiene gate |

Review questions with direct evidence:

- Can a blocked gate publish a decision-grade claim? Proof: `code_capsules/evidence_dag_validator/tests/test_evidence_dag_validator.py`.
- Can mixed timestamp timezone policy crash leakage validation? Proof: `code_capsules/leakage_fold_checker/tests/test_leakage_fold_checker.py`.
- Can malformed OOF group keys silently sort into a metric? Proof: `code_capsules/oof_metric_kernel/tests/test_oof_metric_kernel.py`.
- Can purged CPCV detect embargo and group leakage errors? Proof: `code_capsules/purged_cpcv_splitter/tests/test_purged_cpcv_splitter.py`.
- Can stale or diagnostic artifacts support decision-grade claims? Proof: `code_capsules/artifact_manifest_hasher/tests/test_artifact_manifest_hasher.py`.
- Can date-level source coverage pass when part-level joinability is missing? Proof: `code_capsules/source_joinability_gate/tests/test_source_joinability_gate.py`.
- Can source-backed label planning show physical work avoided? Proof: `scripts/benchmark_capsules.py` and `examples/capsule_benchmark_report.json`.

