# Technical Review Map

This file gives a reviewer a concrete path through the showcase. It is organized by engineering questions rather than by repository order.

## 1. Does Research Have a Governed Entry Point?

Inspect:

- `docs/architecture/five-layer-architecture.md`
- `docs/architecture/research-application-catalog.md`
- `skeleton/layer5-research-governance-operations/`
- `source/omni_station/research_os/governance/operations.py`

What to verify:

- every decision-grade workflow starts from a `ResearchWorkOrder`
- route ownership, allowed next action, blocker state, and stage are explicit
- low-level stations and runners cannot become decision-grade entry points by themselves
- diagnostic, confirmatory, frozen, blocked, waived, retired, and closure states are separate

## 2. Are Research Applications Real Workflow Owners?

Inspect:

- `docs/architecture/research-application-catalog.md`
- `skeleton/layer4-research-applications/`
- `source/omni_station/research_os/applications/contracts.py`
- `source/omni_station/research/pipeline/full_market_source_label_panel_materialization.py`
- `source/omni_station/research/pipeline/high_frequency_factor_line_stage1_active_boundary.py`

What to verify:

- Layer 4 applications receive WorkOrders and produce typed evidence packets
- application contracts declare accepted inputs, produced packets, lower-layer dependencies, and forbidden outputs
- source/label, feature/factor, model, replay, closure, and memory workflows are separated by application ownership
- applications call engines through contracts and do not infer truth from loose reports

## 3. Is Evidence a First-Class System Object?

Inspect:

- `docs/architecture/evidence-kernel-contracts.md`
- `docs/architecture/layer-contracts.md`
- `docs/architecture/validation-gates.md`
- `source/omni_station/research_os/semantic_kernel/gates.py`
- `source/omni_station/research/pipeline/model_branch_oof_run_spec.py`

What to verify:

- `ResearchContract`, `EvidenceEnvelope`, `EvidenceDAG`, `ArtifactManifest`, `TrialBudget`, and gate decisions have separate roles
- route authority and consumer permissions prevent evidence overclaiming
- unsupported claims are blocked instead of silently downgraded
- artifacts are consumed through manifests, not latest-file lookup

## 4. Can a Reviewer Follow Data Lineage?

Inspect:

- `docs/architecture/data-lineage.md`
- `docs/flows/source-label-stage1-oof-flow.md`
- `examples/toy_source_backed_label_view_manifest.json`
- `examples/toy_stage1_trainable_manifest.json`
- `source/omni_station/research/data/full_market_source_contract.py`

What to verify:

- source identity, point-in-time availability, schema hash, content hash, and sample/full-scope boundaries are explicit
- label views remain source-backed when dense row-level materialization is not needed
- Stage1 trainable output records label/factor source refs, join policy, and reject evidence
- OOF launch gates check source-boundary compatibility before allowing downstream validation

## 5. Is ML Validation Bound to the Right Evidence?

Inspect:

- `docs/flows/ml-training-validation-flow.md`
- `docs/flows/source-label-stage1-oof-flow.md`
- `examples/toy_oof_run_spec.json`
- `examples/toy_sequence_batch_plan.json`
- `source/omni_station/research_os/model_training/model_branch_oof_full_executor.py`

What to verify:

- OOF is bound to a full manifest, fold policy, trainable manifest, source boundary, and runtime posture
- sequence-model batching uses fixed-shape descriptor-run planning and fails closed on incompatible shapes
- non-finite diagnostics are evidence metadata, not hidden retries
- CPCV or broader validation cannot start from stale, narrow, or source-incompatible OOF artifacts

## 6. Is Performance Treated as Physical Work Removed?

Inspect:

- `docs/flows/performance-materialization-flow.md`
- `docs/architecture/engine-fabric.md`
- `pseudocode/source_backed_label_view.md`
- `pseudocode/stage1_trainable_join.md`
- `pseudocode/sequence_oof_batch_planner.md`
- `source/rust/omni_sequence_tensor_kernel_py/src/lib.rs`

What to verify:

- the physical plan names scans, projections, materializations, cache boundaries, and native bridge calls
- cache and checkpoint controls are evidence constraints, not claimed speedups by themselves
- source-backed formula views and prepared date caches remove avoidable dense writes or repeated label-side work
- Rust/PyO3 kernels are contract-bound and parity-tested rather than untracked optimizations

## 7. Does Runtime Separation Stay Enforced?

Inspect:

- `docs/architecture/system-overview.md`
- `docs/capability-coverage.md`
- `redacted_capabilities/runtime_engine_boundary/`
- `redacted_capabilities/runtime_engine_boundary/runtime_mode_token_contract.py`
- `source/omni_station/apps/ui_gateway/high_risk_policy.py`

What to verify:

- offline research evidence is separate from live-capable runtime surfaces
- action intent, order-management boundaries, promotion freeze, and runtime posture are explicitly gated
- research artifacts cannot directly become executable actions
- credentials, broker wiring, account identifiers, and execution rules are outside the review package

## 8. Can a Reviewer See the Design Rationale?

Inspect:

- `docs/capability-rationale.md`
- `docs/architecture/failure-mode-matrix.md`
- `docs/architecture/selected-source-path-guide.md`
- `examples/toy_capability_review_packet.json`
- `diagrams/capability-rationale-map.mmd`

What to verify:

- each capability is explained as a problem, design response, evidence surface, and boundary control
- predictable failure modes have explicit blockers rather than hidden fallback paths
- representative source paths are grouped by governance, applications, evidence kernel, engines, infrastructure, Rust, and tests
- synthetic packets explain capability reasoning without exposing formulas, raw data, model internals, or runtime configuration

## 9. Is Quant Validation Reasoning Explicit?

Inspect:

- `docs/flows/quant-research-validation-playbook.md`
- `pseudocode/gate_engine_claim_evaluator.md`
- `pseudocode/closure_case_builder.md`
- `examples/toy_blocker_matrix.json`
- `examples/toy_closure_case.json`

What to verify:

- discovery, freeze, OOF, CPCV, replay, and closure have separate evidence roles
- leakage, trial budget, fold contamination, calibration, replay accounting, and runtime boundary risks are called out
- closure consumes admitted, blocked, and deferred claims rather than only positive metrics

## 10. Is Performance Reasoning Explicit?

Inspect:

- `docs/flows/performance-optimization-playbook.md`
- `pseudocode/performance_physical_plan.md`
- `examples/toy_physical_plan_profile.json`

What to verify:

- performance claims are tied to physical work removed
- source scans, projection width, materialization, joins, memory, cache identity, native bridge use, parity, and telemetry are all reviewable
- cache, checkpoint, and manifest controls are treated as evidence constraints unless they actually remove computation
