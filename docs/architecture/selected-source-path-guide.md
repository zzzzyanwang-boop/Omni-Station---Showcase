# Selected Source Path Guide

The `source/` tree contains source-shaped placeholders. This guide highlights representative paths and explains what each group demonstrates. It is not a full file inventory; the full list is in `docs/source-inventory.md`.

## Governance and UI Read Models

| Path | What It Demonstrates |
| --- | --- |
| `source/omni_station/research_os/governance/operations.py` | route ownership, stage state, allowed action, and blocker projection |
| `source/omni_station/apps/ui_gateway/proof_graph_ops_page.py` | operator-facing evidence graph and gate state read model |
| `source/web/omni-console/src/components/pages/ui039-proof-graph-ops-console.tsx` | UI surface for proof graph review without direct runtime truth inference |
| `source/web/omni-console/src/lib/factor-governance-read-model.ts` | typed read-model boundary for factor governance state |

## Research Applications

| Path | What It Demonstrates |
| --- | --- |
| `source/omni_station/research_os/applications/contracts.py` | common application contract surface |
| `source/omni_station/research_os/applications/setup_d_confirmation_readiness.py` | confirmation readiness preflight with source-boundary and OOF ordering |
| `source/omni_station/research/pipeline/full_market_source_label_panel_materialization.py` | source-boundary label-panel materialization application |
| `source/omni_station/research/pipeline/high_frequency_factor_line_stage1_active_boundary.py` | Stage1 source-backed trainable materialization boundary |
| `source/omni_station/research/pipeline/model_branch_oof_run_spec.py` | formal OOF run-spec compilation and stale-scope blocking |

## Evidence and Contract Kernel

| Path | What It Demonstrates |
| --- | --- |
| `source/omni_station/research_os/semantic_kernel/gates.py` | gate semantics for admitted, blocked, deferred, diagnostic, and quarantined evidence |
| `source/omni_station/research_os/semantic_kernel/evidence.py` | evidence envelope and packet shape |
| `source/omni_station/research_os/semantic_kernel/artifacts.py` | artifact contract and manifest references |
| `source/omni_station/research_os/conformance/suite.py` | conformance checks for Research OS boundaries |
| `source/omni_station/research_foundry/evidence/proof_graph.py` | proof graph representation for route evidence |

## Feature, Factor, and External Source Governance

| Path | What It Demonstrates |
| --- | --- |
| `source/omni_station/research_foundry/compiler/feature_compiler.py` | feature compilation under contracts |
| `source/omni_station/research_foundry/compiler/label_compiler.py` | label compilation and separation from feature ownership |
| `source/omni_station/research/features/external_factor_source_ownership.py` | source ownership and external-factor governance |
| `source/omni_station/research/features/external_projection/runtime/materialization.py` | external projection materialization runtime boundary |
| `source/omni_station/research/features/external_projection/runtime/cs_whole_dag_executor.py` | whole-DAG factor execution surface |

## Model and OOF Validation

| Path | What It Demonstrates |
| --- | --- |
| `source/omni_station/research_os/model_training/model_branch_oof_full_executor.py` | full-manifest OOF executor and fixed-shape sequence batch planning |
| `source/omni_station/research_os/model_training/sequence_tensor_native_kernel.py` | Python contract wrapper for native sequence tensor assembly |
| `source/omni_station/research_foundry/model_zoo/evidence/calibration_ood.py` | calibration and out-of-distribution evidence |
| `source/omni_station/research_foundry/model_zoo/evidence/branch_eligibility.py` | model branch eligibility and blocker reasoning |
| `source/tests/research/pipeline/test_model_branch_oof_run_spec.py` | fail-closed tests for formal OOF scope binding |

## Runtime, Replay, and Promotion Boundary

| Path | What It Demonstrates |
| --- | --- |
| `redacted_capabilities/runtime_engine_boundary/runtime_mode_token_contract.py` | runtime posture control before live-capable surfaces |
| `redacted_capabilities/runtime_engine_boundary/promotion_freeze_gate.py` | freeze and promotion readiness boundary |
| `source/omni_station/apps/ui_gateway/high_risk_policy.py` | UI-facing high-risk action guardrail and blocked runtime posture |
| `source/omni_station/research_os/engines/execution_replay_native.py` | execution replay engine boundary |
| `source/rust/omni_counterfactual_execution_kernel_py/src/lib.rs` | native counterfactual replay bridge |

## Data, Artifact, and Physical Infrastructure

| Path | What It Demonstrates |
| --- | --- |
| `source/omni_station/research/data/full_market_source_contract.py` | source-boundary compatibility and source contract |
| `source/omni_station/research_os/data_plane/manifest.py` | manifest-bound artifact data plane |
| `source/gpm/artifact/manifest.py` | artifact manifest serialization and hash policy |
| `source/gpm/artifact/io.py` | artifact IO boundary and storage convention |
| `source/gpm/expr/hybrid_executor.py` | vectorized expression engine selection boundary |

## Rust and Native Systems

| Path | What It Demonstrates |
| --- | --- |
| `source/rust/omni_wire/src/lib.rs` | deterministic wire-codec boundary |
| `source/rust/omni_bus_iceoryx2/src/lib.rs` | native event bus and local transport boundary |
| `source/rust/omni_features_stream/src/lib.rs` | native feature-stream execution surface |
| `source/rust/omni_datafusion_query/src/lib.rs` | native columnar query and projection control |
| `source/rust/omni_sequence_tensor_kernel_py/src/lib.rs` | sequence tensor PyO3 kernel bridge |

## Test Surface

| Path | What It Demonstrates |
| --- | --- |
| `source/tests/research/pipeline/test_full_market_source_label_panel_materialization.py` | source-backed label panel contract tests |
| `source/tests/research/pipeline/test_high_frequency_factor_line_stage1_active_boundary.py` | Stage1 join, prepared cache, and reject ledger tests |
| `source/tests/research/pipeline/test_model_branch_oof_execution_runner.py` | sequence OOF fixed-shape and non-finite behavior tests |
| `source/tests/research/features/test_fold_local_factor_selector_train_only.py` | fold-local feature selection discipline |
| `source/tests/research/performance/test_hotpath_ranker_no_high_confidence_without_measurement.py` | performance evidence must be measured before strong claims |
