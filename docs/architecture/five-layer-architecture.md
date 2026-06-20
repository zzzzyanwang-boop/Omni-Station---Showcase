# Research OS Five-Layer Architecture

This document is the architecture map for OmniStation Research OS. It follows the full-system design baseline and focuses on the reviewable system structure: ownership, contracts, evidence flow, engines, artifacts, gates, and infrastructure.

The design is a top-down Research Operating System, not a bottom-up script collection. Research begins with governance and WorkOrders, flows through applications and evidence contracts, calls engines, and lands on data/compute/artifact infrastructure.

```text
Layer 5 - Research Governance & Operations
Layer 4 - Research Applications
Layer 3 - Evidence / Contract / DAG Kernel
Layer 2 - Provider / Model / Runtime Engines
Layer 1 - Data / Compute / Artifact Infrastructure
```

## Layer 5: Research Governance & Operations

Purpose: define how research is initiated, owned, reviewed, frozen, continued, stopped, waived, retired, and remembered.

It answers:

- who can open a research route
- who owns the route and review gates
- what stage the route is in
- what next action is allowed
- what evidence is diagnostic versus confirmatory
- what is blocked, quarantined, frozen, waived, or retired

Representative objects:

- `ResearchWorkOrder`
- `ResearchRouteCharter`
- `ResearchQuestion`
- `MechanismHypothesis`
- `ExperimentMandate`
- `EvidencePlan`
- `ReviewGate`
- `FreezeDecision`
- `StopContinueDecision`
- `WaiverRequest`
- `RetirementDecision`
- `ResearchMemoryEntry`

Representative review artifacts:

- `source/omni_station/research_os/governance/operations.py`
- `source/omni_station/apps/ui_gateway/proof_graph_ops_page.py`
- `redacted_capabilities/governance_operations_surface/evidence_console_read_model.py`

## Layer 4: Research Applications

Purpose: provide the research applications a researcher actually uses. These are not low-level stations. They are OS-level apps that own workflows and call lower layers.

Application families:

- Idea Intake Desk
- Mechanism Memo Studio
- Data & Panel Contract Studio
- Feature / Factor Foundry
- SignalState Lab
- Model Zoo Workbench
- Discovery Factory
- Review & Freeze Board
- Confirmation Lab
- Decision Score Lab
- Economic Replay Lab
- Portfolio Utility Lab
- Closure Committee
- Research Memory Library
- Legacy Quarantine Console

Representative review artifacts:

- `source/omni_station/research_os/applications/contracts.py`
- `source/omni_station/research_foundry/compiler/feature_compiler.py`
- `source/omni_station/research_to_live/candidate_freeze_readiness_gate.py`
- `redacted_capabilities/research_line_a/promotion_packet.py`

## Layer 3: Evidence / Contract / DAG Kernel

Purpose: define the system law. This layer decides what is executable, what remains diagnostic, what can enter OOF, what can enter economic replay, and what can close.

Kernel objects:

- `ResearchContractCompiler`
- `EvidenceEnvelope`
- `EvidenceDAG`
- `ArtifactManifestStore`
- `RouteAuthorityRegistry`
- `TrialBudgetLedger`
- `DiscoverySeal`
- `ConfirmatorySpec`
- `ClosureArbitration`

Representative review artifacts:

- `source/omni_station/research_os/kernel/spine.py`
- `source/omni_station/research_os/semantic_kernel/gates.py`
- `source/omni_station/research_foundry/evidence/proof_graph.py`
- `pseudocode/research_run_orchestrator.md`

## Layer 2: Provider / Model / Runtime Engines

Purpose: provide reusable capability services behind Research OS contracts. These are engines and providers, not the top-level research flow.

Engine families:

- FeatureProvider
- ExternalFactorProvider
- SignalStateProvider
- EconomicStateProvider
- LabelOracle
- ModelZoo
- Calibration / OOD
- DecisionRuntime
- ExecutionReplayEngine
- PortfolioEngine

Representative review artifacts:

- `source/omni_station/research_os/engines/research_core_native.py`
- `source/omni_station/research/features/external_projection/runtime/materialization.py`
- `source/gpm/expr/hybrid_executor.py`
- `redacted_capabilities/evidence_contract_dag_kernel/out_of_fold_prediction_store.py`

## Layer 1: Data / Compute / Artifact Infrastructure

Purpose: own the physical infrastructure: data layout, compute substrate, artifact storage, cache lifecycle, atomic writes, progress events, and local/native/GPU execution surfaces.

Infrastructure areas:

- completed-bar and market-data inputs
- Parquet / Arrow / manifest-backed storage
- cache and partition policy
- atomic writes
- station runner and progress events
- local compute
- native and GPU-ready training surfaces

Representative review artifacts:

- `source/omni_station/research_os/data_plane/manifest.py`
- `source/omni_station/research/data/arrow_utils.py`
- `source/gpm/artifact/io.py`
- `redacted_capabilities/native_compute_infrastructure/cache_checkpoint_telemetry.py`

## Research Lifecycle

The layered architecture supports one unified lifecycle:

```text
0. Idea Intake
1. Mechanism Framing
2. Research Charter
3. Data / Panel Contract
4. Feature / Factor / State Plan
5. Label / Outcome Plan
6. Discovery Factory
7. Evidence Review
8. Freeze Decision
9. Confirmation Lab
10. Statistical Validation
11. Decision Score Validation
12. Economic Replay
13. Portfolio Utility
14. Closure Committee
15. Research Memory / Retirement
```

## Cross-Layer Invariant

No low-level station, runner, model, artifact, or replay result can become decision-grade by itself. A route is decision-grade only when a Layer 5 WorkOrder and Layer 4 application path compile into Layer 3 contracts, call Layer 2 engines, bind Layer 1 artifacts, and return reviewable evidence through the same OS path.
