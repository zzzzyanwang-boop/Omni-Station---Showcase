# Five-Layer Architecture

This document is the public-safe architecture map for OmniStation. It describes ownership boundaries, data flow, and gate flow without exposing production source code, private datasets, alpha formulas, credentials, or runtime state.

## Layer 1: Research Control Plane

Purpose: turn a research question into a bounded, reviewable unit of work.

Responsibilities:

- declare work order identity, scope, non-goals, and acceptance signal
- bind the work order to a research contract
- build the evidence DAG before execution
- reject missing owner, missing contract, loose artifact discovery, and unbounded runs
- expose operator-readable status without exposing private runtime details

Representative public artifacts:

- `examples/toy_work_order.yaml`
- `pseudocode/research_run_orchestrator.md`

## Layer 2: Data and Evidence Fabric

Purpose: make every input and output manifest-bound and reproducible.

Responsibilities:

- represent sources with source manifests
- represent feature, label, model, risk, replay, and report outputs as evidence artifacts
- preserve schema hashes, content hashes, row counts, sample scope, and lineage
- prefer columnar, partitionable artifact concepts for row-level research data
- fail closed on stale caches, missing manifests, mixed artifact formats, or untracked inputs

Representative public artifacts:

- `examples/toy_source_manifest.json`
- `examples/toy_evidence_manifest.json`
- `pseudocode/manifest_store.md`

## Layer 3: Research Engine Layer

Purpose: run bounded research computation behind explicit contracts.

Engine families:

- alpha and factor profiling
- feature and label materialization
- ML training and OOF evidence generation
- sequence tensor and market-data model preparation
- risk sidecar generation
- deterministic replay and execution-cost evaluation
- performance-sensitive materialization kernels

Representative public artifacts:

- `examples/toy_factor_profile.json`
- `examples/toy_ml_training_manifest.json`
- `pseudocode/factor_evidence_engine.md`
- `pseudocode/ml_validation_gate.md`

## Layer 4: Validation and Governance Layer

Purpose: decide what can be claimed from the evidence.

Gate families:

- source and point-in-time lineage gates
- leakage, purged-fold, embargo, and fold-local selection gates
- risk attribution and factor-identity gates
- replay determinism and execution-cost gates
- metric, calibration, and model-registry gates
- review gate and closure-case gate

The layer blocks unsupported claims even when a diagnostic artifact exists.

Representative public artifacts:

- `examples/toy_gate_result.json`
- `examples/toy_risk_identity_ledger.json`
- `examples/toy_offline_evaluation_report.json`
- `pseudocode/replay_cost_gate.md`

## Layer 5: Productization Boundary Layer

Purpose: prevent offline research output from directly becoming production behavior.

Responsibilities:

- expose read models, reports, and review packets
- separate offline evidence from paper/live/broker/OMS posture
- require promotion packets before any runtime-capable path
- require inference eligibility before model serving
- preserve blocked and deferred claims for operator review

Representative public artifacts:

- `skeleton/inference/README.md`
- `skeleton/runtime/README.md`
- `skeleton/ui/README.md`

## Cross-Layer Invariant

No layer can promote an artifact by implication. A downstream layer must consume an explicit manifest, verify its contract, and record the claim it admits or blocks.

