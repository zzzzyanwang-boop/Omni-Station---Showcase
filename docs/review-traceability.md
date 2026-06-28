# Review Traceability

This matrix maps representative source-shaped paths to the public proof surface. It is intentionally selective: the complete retained path inventory is in `docs/source-inventory.md`, while this file shows how the architecture can be reviewed from path to capability to executable or fixture-backed proof.

| Source-shaped path | Layer | Capability shown | Public proof |
|---|---|---|---|
| `source/omni_station/research_os/applications/setup_d_confirmation_readiness.py` | Layer 4 | Confirmation readiness, OOF-before-CPCV ordering, blocker posture | `docs/flows/quant-research-validation-playbook.md`; `examples/toy_blocker_matrix.json` |
| `source/omni_station/research_os/model_training/model_branch_oof_full_executor.py` | Layer 4 | OOF execution boundary and batch-shape stability | `pseudocode/sequence_oof_batch_planner.md`; `examples/toy_sequence_batch_plan.json` |
| `source/omni_station/research_os/model_training/sequence_tensor_native_kernel.py` | Layer 2 | Python contract around native sequence tensor assembly | `code_capsules/rust_sequence_tensor_kernel` |
| `source/rust/omni_sequence_tensor_kernel_py/src/lib.rs` | Layer 2 | Rust/PyO3-style fixed-shape tensor kernel boundary | `code_capsules/rust_sequence_tensor_kernel/src/lib.rs` |
| `source/omni_station/research/pipeline/model_branch_oof_run_spec.py` | Layer 4 | OOF run-spec rebinding and stale-scope blocking | `pseudocode/oof_rebinding_gate.md`; `examples/toy_oof_run_spec.json` |
| `source/omni_station/research/data/full_market_source_contract.py` | Layer 1 | Source-boundary certificate and source scope binding | `examples/toy_source_manifest.json`; `docs/flows/source-label-stage1-oof-flow.md` |
| `source/omni_station/research/pipeline/full_market_source_label_panel_materialization.py` | Layer 1 | Source-backed label-panel materialization boundary | `code_capsules/source_backed_label_view`; `examples/toy_source_backed_label_view_manifest.json` |
| `source/omni_station/research/pipeline/high_frequency_factor_line_stage1_active_boundary.py` | Layer 1 | Stage1 source-backed factor/label join boundary | `pseudocode/stage1_trainable_join.md`; `examples/toy_stage1_trainable_manifest.json` |
| `source/tests/research/features/test_source_pit_quality_certificate.py` | Layer 3 | Point-in-time source quality and forbidden future fields | `code_capsules/leakage_fold_checker` |
| `source/tests/research/features/test_fold_local_factor_selector_train_only.py` | Layer 3 | Fold-local selection and train-only policy | `code_capsules/purged_cpcv_splitter` |
| `source/tests/research/features/test_fold_local_bucket_cutpoints_not_reused.py` | Layer 3 | Leakage prevention across fold-local transforms | `code_capsules/purged_cpcv_splitter/tests/test_purged_cpcv_splitter.py` |
| `source/tests/research/features/test_factor_leakage_audit_blocks_realized_edge.py` | Layer 3 | Leakage audit fail-closed behavior | `code_capsules/leakage_fold_checker/tests/test_leakage_fold_checker.py` |
| `source/tests/research/features/test_full_non_sample_factor_store_manifest_gate.py` | Layer 3 | Manifest-bound full-scope artifact gate | `code_capsules/artifact_manifest_hasher` |
| `source/tests/research/features/test_external_factor_store_full_streaming.py` | Layer 1 | Streaming materialization and scan/materialization discipline | `pseudocode/performance_physical_plan.md`; `examples/toy_physical_plan_profile.json` |
| `source/omni_station/research/features/external_projection/quality_gates.py` | Layer 1 | Part-level source joinability rather than date-only coverage | `code_capsules/source_joinability_gate` |
| `source/tests/research/performance/test_hotpath_ranker_no_high_confidence_without_measurement.py` | Layer 1 | Performance claims require measured physical evidence | `scripts/benchmark_capsules.py`; `examples/capsule_benchmark_report.json` |
| `source/tests/research/performance/test_engine_benchmark_case_schema.py` | Layer 1 | Benchmark report schema and physical-plan counters | `scripts/benchmark_capsules.py` |
| `source/tests/research/models/test_model_artifact_prediction_replay.py` | Layer 2 | Model artifact replay and manifest-bound predictions | `code_capsules/artifact_manifest_hasher` |
| `source/tests/research/models/test_no_proxy_score_artifacts.py` | Layer 3 | Unsupported proxy score artifacts cannot support review | `code_capsules/artifact_manifest_hasher/tests/test_artifact_manifest_hasher.py` |
| `source/omni_station/research_foundry/models/training_job.py` | Layer 4 | Fold-local ML training job and OOF score-bus manifest boundary | `code_capsules/toy_model_lifecycle_gate`; `examples/toy_ml_training_manifest.json` |
| `source/omni_station/research_foundry/models/model_factory.py` | Layer 4 | Model branch spec creation and unsupported branch blocking | `code_capsules/toy_model_lifecycle_gate`; `examples/toy_model_branch_eligibility.json` |
| `source/omni_station/research_foundry/models/model_card.py` | Layer 4 | Model-card support refs, decision scope, and runtime posture boundary | `examples/toy_model_card.json`; `code_capsules/toy_model_lifecycle_gate/tests/test_toy_model_lifecycle_gate.py` |
| `source/omni_station/research_foundry/models/calibration.py` | Layer 4 | Calibration reliability artifact and missing-calibration blocker | `examples/toy_calibration_ood_report.json`; `code_capsules/toy_model_lifecycle_gate` |
| `source/omni_station/research_foundry/models/ood.py` | Layer 4 | OOD score-distribution drift blocker for model eligibility | `examples/toy_model_lifecycle_gate_blocked.json`; `code_capsules/toy_model_lifecycle_gate` |
| `source/omni_station/research_foundry/models/uncertainty.py` | Layer 4 | Non-finite prediction and uncertainty diagnostics boundary | `examples/toy_model_lifecycle_gate_pass.json`; `code_capsules/toy_model_lifecycle_gate/tests/test_toy_model_lifecycle_gate.py` |
| `source/omni_station/research_foundry/models/model_multiplicity.py` | Layer 4 | Branch multiplicity and proxy-score rejection boundary | `examples/toy_model_branch_eligibility.json`; `code_capsules/toy_model_lifecycle_gate/tests/test_toy_model_lifecycle_gate.py` |
| `source/omni_station/research_foundry/models/production_evidence.py` | Layer 4 | Decision-grade model evidence packet before productization review | `examples/toy_model_lifecycle_gate_pass.json`; `examples/toy_model_lifecycle_gate_blocked.json` |
| `source/omni_station/research_foundry/model_zoo/evidence/branch_eligibility.py` | Layer 4 | Branch eligibility pass/block packet and blocker propagation | `examples/toy_model_branch_eligibility.json`; `code_capsules/toy_model_lifecycle_gate` |
| `source/omni_station/research_foundry/model_zoo/evidence/calibration_ood.py` | Layer 4 | Combined calibration/OOD model-card support evidence | `examples/toy_calibration_ood_report.json`; `examples/toy_model_lifecycle_gate_blocked.json` |
| `source/omni_station/research_foundry/model_zoo/evidence/calibration_reliability.py` | Layer 4 | Calibration-bin completeness and reliability support checks | `examples/toy_calibration_ood_report.json`; `code_capsules/toy_model_lifecycle_gate` |
| `source/omni_station/research_foundry/model_zoo/evidence/score_distribution_drift.py` | Layer 4 | Score-distribution drift report and OOD block decision | `examples/toy_model_lifecycle_gate_blocked.json`; `code_capsules/toy_model_lifecycle_gate` |
| `source/tests/research/models/test_high_edge_lightgbm_artifactization.py` | Layer 3 | Model artifactization must preserve manifest and branch evidence | `examples/toy_ml_training_manifest.json`; `code_capsules/toy_model_lifecycle_gate` |
| `source/tests/research/models/test_two_stage_tradeable_edge_model.py` | Layer 3 | Two-stage model eligibility requires complete OOF/calibration/replay support | `examples/toy_model_lifecycle_gate_pass.json`; `examples/toy_model_lifecycle_gate_blocked.json` |
| `source/omni_station/research_os/experiment_validation/contracts.py` | Layer 3 | Evidence contract shape and gate-ready claims | `code_capsules/evidence_dag_validator` |
| `source/omni_station/research_os/semantic_kernel/evidence.py` | Layer 3 | Evidence DAG ancestry and support validation | `code_capsules/evidence_dag_validator/src/evidence_dag_validator.py` |
| `source/omni_station/research_os/data_plane/manifest.py` | Layer 3 | Schema/content hash and lineage reference boundary | `code_capsules/artifact_manifest_hasher/src/artifact_manifest_hasher.py` |
| `source/omni_station/research_os/semantic_kernel/gates.py` | Layer 3 | Pass/block gate semantics and supported decision claims | `pseudocode/gate_engine_claim_evaluator.md`; `code_capsules/evidence_dag_validator` |
| `source/omni_station/research/finml/diagnostics/trials_registry.py` | Layer 3 | Multiple-testing and trial accounting boundary | `docs/flows/quant-research-validation-playbook.md`; `examples/toy_gate_result.json` |
| `source/omni_station/research_foundry/governance/confirmatory_production_closure.py` | Layer 4 | Closure case and research memory handoff | `pseudocode/closure_case_builder.md`; `examples/toy_closure_case.json` |
| `source/omni_station/research_os/engines/execution_replay_native.py` | Layer 2 | Offline economic replay boundary | `pseudocode/replay_cost_gate.md`; `examples/toy_offline_evaluation_report.json` |
| `source/omni_station/research_os/factor_evidence/risk_adjusted_identity.py` | Layer 2 | Risk identity, attribution, and sidecar evidence | `examples/toy_risk_identity_ledger.json` |
| `source/omni_station/apps/ui_gateway/proof_graph_ops_page.py` | Layer 5 | Operator-visible evidence graph state | `examples/toy_page_contract.json`; `diagrams/evidence-flow.mmd` |
| `source/omni_station/apps/ui_gateway/factor_registry_governance_lifecycle.py` | Layer 5 | Governance lifecycle and review-state read models | `docs/architecture/research-application-catalog.md`; `examples/toy_capability_review_packet.json` |
| `source/omni_station/apps/ui_gateway/research_workflow_policy.py` | Layer 5 | Allowed action and fail-closed operator policy | `docs/architecture/failure-mode-matrix.md`; `examples/toy_blocker_matrix.json` |
| `source/web/omni-console/src/lib/gateway-fail-closed.ts` | Layer 5 | UI-side fail-closed gateway behavior | `examples/toy_page_contract.json`; `examples/toy_blocker_matrix.json` |
| `source/web/omni-console/src/components/pages/ui009-promotion.tsx` | Layer 5 | Promotion review UI boundary | `redacted_capabilities/governance_operations_surface/promotion_review_page.py`; `examples/toy_capability_review_packet.json` |
| `source/rust/omni_wire/tests/test_sbe_cross_lang_fixture.rs` | Layer 1 | Cross-language wire fixture validation | `code_capsules/rust_native_boundary_proofs/src/lib.rs`; `examples/capsule_benchmark_report.json` |
| `source/rust/omni_features_stream/tests/validate_ir.rs` | Layer 1 | Native feature-stream IR validation boundary | `code_capsules/rust_native_boundary_proofs/src/lib.rs`; `examples/capsule_benchmark_report.json` |
| `source/rust/omni_bus_iceoryx2/src/journal.rs` | Layer 1 | Replayable native event journal boundary | `code_capsules/rust_native_boundary_proofs/src/lib.rs`; `examples/capsule_benchmark_report.json` |
| `source/rust/omni_datafusion_query/src/lib.rs` | Layer 1 | Columnar scan/projection control boundary | `pseudocode/performance_physical_plan.md`; `examples/toy_physical_plan_profile.json` |
| `source/rust/omni_counterfactual_execution_kernel_py/src/lib.rs` | Layer 2 | Native counterfactual execution kernel boundary | `pseudocode/replay_cost_gate.md`; `examples/toy_offline_evaluation_report.json` |
| `source/tests/research/pipeline/test_model_branch_oof_run_spec.py` | Layer 4 | Formal OOF source-boundary compatibility tests | `examples/toy_oof_run_spec.json`; `code_capsules/source_backed_label_view` |
| `source/tests/research/pipeline/test_high_frequency_factor_line_stage1_active_boundary.py` | Layer 1 | Source-backed Stage1 trainable join tests | `pseudocode/stage1_trainable_join.md`; `examples/toy_stage1_trainable_manifest.json` |
| `source/tests/research/pipeline/test_full_market_source_label_panel_materialization.py` | Layer 1 | Source-backed label view tests | `code_capsules/source_backed_label_view/tests/test_source_backed_label_view.py` |

Review interpretation:

- A path is retained only when the filename communicates ownership or architecture shape.
- A public proof is executable when possible; otherwise it is a synthetic fixture, diagram, or pseudocode artifact that shows the contract.
- Sensitive research lines, exact formulas, production source bodies, runtime paths, and real datasets remain outside the review surface.
