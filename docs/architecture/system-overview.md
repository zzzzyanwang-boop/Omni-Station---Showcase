# System Overview

OmniStation is structured as an institutional Research Operating System. The architecture follows the full-system design baseline: research starts at Governance & Operations, enters Research Applications, compiles into Evidence / Contract / DAG Kernel objects, calls Provider / Model / Runtime Engines, and binds Data / Compute / Artifact Infrastructure.

## Layer Model

| Layer | Responsibility | Review Artifact Examples |
| --- | --- | --- |
| Layer 5 - Research Governance & Operations | WorkOrders, route authority, stage state, review ownership, freeze/stop/waiver/retirement decisions, Research Mission Control | `source/omni_station/research_os/governance/operations.py`, `source/omni_station/apps/ui_gateway/proof_graph_ops_page.py` |
| Layer 4 - Research Applications | Idea intake, mechanism framing, data/panel contracts, feature/factor foundry, discovery, review/freeze, confirmation, decision score, replay, closure, memory | `source/omni_station/research_os/applications/contracts.py`, `source/omni_station/research_foundry/compiler/feature_compiler.py` |
| Layer 3 - Evidence / Contract / DAG Kernel | ResearchContractCompiler, EvidenceEnvelope, EvidenceDAG, ArtifactManifestStore, route authority, trial budget, discovery seal, confirmatory spec, closure arbitration | `source/omni_station/research_os/kernel/spine.py`, `source/omni_station/research_os/semantic_kernel/gates.py` |
| Layer 2 - Provider / Model / Runtime Engines | Feature/external-factor/signal/economic providers, LabelOracle, ModelZoo, Calibration/OOD, DecisionRuntime, ExecutionReplayEngine, PortfolioEngine, native engine bridge contracts | `source/omni_station/research_os/engines/research_core_native.py`, `source/gpm/expr/hybrid_executor.py`, `source/rust/omni_expr_compiler_py/src/lib.rs` |
| Layer 1 - Data / Compute / Artifact Infrastructure | Market-data inputs, Parquet/Arrow/manifests, cache, partitioning, atomic writes, station runner, progress events, Rust-native bus/codec/query/feature-stream/profiling surfaces | `source/omni_station/research_os/data_plane/manifest.py`, `source/gpm/artifact/io.py`, `source/rust/omni_bus_iceoryx2/src/lib.rs` |

## Lifecycle Model

The OS lifecycle is the main design object:

```text
Idea Intake -> Mechanism Framing -> Research Charter -> Data / Panel Contract
-> Feature / Factor / State Plan -> Label / Outcome Plan -> Discovery Factory
-> Evidence Review -> Freeze Decision -> Confirmation Lab
-> Statistical Validation -> Decision Score Validation -> Economic Replay
-> Portfolio Utility -> Closure Committee -> Research Memory / Retirement
```

## Architecture Domains

| Domain | What It Demonstrates | Review Artifact Examples |
| --- | --- | --- |
| Governance and operations | WorkOrder authority, stage state, allowed next action, blockers, review board state | `docs/architecture/five-layer-architecture.md`, `redacted_capabilities/governance_operations_surface/evidence_console_read_model.py` |
| Research applications | OS apps that own the research workflow rather than raw scripts or stations | `source/omni_station/research_os/applications/contracts.py`, `redacted_capabilities/research_line_a/candidate_lifecycle.py` |
| Evidence kernel | Evidence DAGs, contracts, manifests, route authority, trial budgets, closure arbitration | `source/omni_station/research_os/kernel/spine.py`, `source/omni_station/research_foundry/evidence/proof_graph.py` |
| Providers and engines | Feature, factor, model, calibration, replay, decision runtime, portfolio engines, and native bridge contracts | `source/gpm/expr/engine_planner.py`, `source/rust/omni_counterfactual_execution_kernel_py/src/lib.rs`, `redacted_capabilities/native_compute_infrastructure/fused_factor_kernel.py` |
| Infrastructure | Physical storage, compute, artifacts, cache, checkpoints, progress, Rust-native bus/codec/query surfaces, and atomic writes | `source/gpm/artifact/manifest.py`, `source/rust/omni_datafusion_query/src/lib.rs`, `redacted_capabilities/data_compute_artifact_infrastructure/lineage_manifest_store.py` |

## Design Posture

The system treats research success as evidence quality, not simply positive metrics. A result is not decision-grade unless it has a WorkOrder, route charter, compiled contract, evidence DAG, manifest-bound artifacts, review gates, and closure/freeze state.

## Runtime Separation

Offline research and live-capable execution remain separate. A research artifact cannot directly become a live action. Runtime-capable surfaces require explicit authority, safety contracts, evidence review, and promotion controls.
