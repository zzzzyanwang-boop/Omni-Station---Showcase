# Code Capsules

This directory contains small, runnable public-safe implementations that demonstrate technical depth without exposing production source code, strategy logic, non-public research data, production configuration, or runtime artifacts.

Each capsule uses synthetic inputs and focuses on one reviewable engineering problem:

- `evidence_dag_validator`: manifest-bound evidence graph validation and fail-closed gate checks.
- `leakage_fold_checker`: point-in-time feature checks, label-window checks, and fold embargo validation.
- `purged_cpcv_splitter`: purged combinatorial cross-validation splits with embargo and group-leakage controls.
- `source_backed_label_view`: a source-backed label view planner that avoids unnecessary dense label materialization.
- `oof_metric_kernel`: grouped OOF metric aggregation using sufficient statistics and segmented rank IC.
- `artifact_manifest_hasher`: schema/content/lineage hashing and stale or diagnostic artifact support checks.
- `source_joinability_gate`: part-level source joinability checks that reject date-only coverage claims.
- `rust_sequence_tensor_kernel`: a Rust toy native kernel for validity bitmap packing, contiguous anchor runs, and sequence batch gathering.
- `rust_native_boundary_proofs`: Rust-native wire fixture, feature IR, and append-only journal boundary checks.
- `e2e_toy_research_flow`: an executable toy source-to-OOF gate flow that connects the Python capsules and verifies both pass and blocked gate outcomes against golden reports.
- `toy_model_lifecycle_gate`: an executable toy train-to-model-card lifecycle gate covering OOF prediction manifests, calibration/OOD, uncertainty, prediction replay compatibility, and branch eligibility blockers.

Run the Python capsules:

```powershell
python -m unittest discover code_capsules -p "test_*.py"
python -m code_capsules.e2e_toy_research_flow.src.toy_research_flow
python -m code_capsules.toy_model_lifecycle_gate --scenario pass
python -m code_capsules.toy_model_lifecycle_gate --scenario blocked
python scripts/benchmark_capsules.py
```

The end-to-end flow is checked against `examples/toy_e2e_gate_report.json` and `examples/toy_e2e_blocked_gate_report.json`. The model lifecycle gate is checked against `examples/toy_model_lifecycle_gate_pass.json` and `examples/toy_model_lifecycle_gate_blocked.json`, so a reviewer can see both complete evidence and fail-closed model blockers without non-public data.

Run the Rust capsule:

```powershell
cargo test --manifest-path code_capsules/rust_sequence_tensor_kernel/Cargo.toml
cargo test --manifest-path code_capsules/rust_native_boundary_proofs/Cargo.toml
```

The code here is intentionally compact. It is meant to show algorithmic and systems judgment: typed boundaries, deterministic validation, fail-closed behavior, physical-plan reasoning, artifact lineage, source joinability, purged validation, native boundary discipline, and careful edge-case tests.
