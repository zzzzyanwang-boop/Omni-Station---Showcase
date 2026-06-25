# Code Capsules

This directory contains small, runnable public-safe implementations that demonstrate technical depth without exposing private OmniStation source code, strategy logic, research data, production configuration, or runtime artifacts.

Each capsule uses synthetic inputs and focuses on one reviewable engineering problem:

- `evidence_dag_validator`: manifest-bound evidence graph validation and fail-closed gate checks.
- `leakage_fold_checker`: point-in-time feature checks, label-window checks, and fold embargo validation.
- `source_backed_label_view`: a source-backed label view planner that avoids unnecessary dense label materialization.
- `oof_metric_kernel`: grouped OOF metric aggregation using sufficient statistics and segmented rank IC.
- `rust_sequence_tensor_kernel`: a Rust toy native kernel for validity bitmap packing, contiguous anchor runs, and sequence batch gathering.
- `e2e_toy_research_flow`: an executable toy source-to-OOF gate flow that connects the Python capsules.

Run the Python capsules:

```powershell
python -m unittest discover code_capsules -p "test_*.py"
python -m code_capsules.e2e_toy_research_flow.src.toy_research_flow
```

Run the Rust capsule:

```powershell
cargo test --manifest-path code_capsules/rust_sequence_tensor_kernel/Cargo.toml
```

The code here is intentionally compact. It is meant to show algorithmic and systems judgment: typed boundaries, deterministic validation, fail-closed behavior, physical-plan reasoning, and careful edge-case tests.
