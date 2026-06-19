# System Overview

OmniStation is structured around a research-to-review pipeline. Each layer has a narrow responsibility and a defined artifact contract. The public showcase presents the private system through a five-layer architecture: control, evidence, engines, governance, and productization boundary.

## Layer Model

| Layer | Responsibility | Public Showcase Representation |
| --- | --- | --- |
| Work Order | Declares objective, scope, owner, and acceptance signal | `examples/toy_work_order.yaml` |
| Research Contract | Converts the work order into executable invariants and gates | `skeleton/contracts/README.md` |
| Evidence DAG | Defines dependencies, lineage, and artifact expectations | `diagrams/evidence-flow.mmd` |
| Application Owner | Owns a route-specific research workflow | `skeleton/apps/README.md` |
| Engine | Performs bounded computation under the contract | `skeleton/engines/README.md` |
| Artifact Manifest | Records outputs, schema, hashes, and provenance | `examples/toy_evidence_manifest.json` |
| Review Gate | Decides whether claims are admitted, blocked, or deferred | `examples/toy_gate_result.json` |

## Public Architecture Domains

| Domain | What It Demonstrates | Public Showcase Representation |
| --- | --- | --- |
| Alpha / factor research | Signal profiling, coverage, redundancy, leakage sentinel, claim admission | `skeleton/alpha-research/README.md`, `examples/toy_factor_profile.json` |
| ML research infrastructure | Model-family contracts, OOF evidence, calibration, registry concepts | `skeleton/model-training/README.md`, `examples/toy_ml_training_manifest.json` |
| FinML validation | Purged folds, embargo, CPCV-style paths, fold-local selection | `skeleton/finml-validation/README.md` |
| Microstructure research | LOB/TBBO/MBO-style input contracts and execution-aware features | `skeleton/microstructure/README.md` |
| Offline evaluation | Replay, cost evidence, fills, latency, economic gate | `skeleton/offline-evaluation/README.md`, `examples/toy_offline_evaluation_report.json` |
| Risk model controls | Beta, factor identity, sidecars, blocked pure-alpha claims | `skeleton/risk-model/README.md`, `examples/toy_risk_identity_ledger.json` |
| Production boundary | Offline-to-live separation, promotion gate, inference eligibility | `skeleton/inference/README.md` |
| Performance engineering | Columnar layout, projection-first scans, native/GPU-ready kernels | `skeleton/performance/README.md` |

## Design Posture

The system treats research success as evidence quality, not simply positive metrics. A result is not promotion-ready unless lineage, leakage controls, sample boundaries, failure modes, and review gates are explicit.

## Runtime Separation

Offline research and live-capable execution are separate surfaces. A research artifact cannot directly become a live action. It must pass through contract checks, review gates, and promotion boundaries.
