# System Overview

OmniStation is structured around a research-to-review pipeline. Each layer has a narrow responsibility and a defined artifact contract. The public showcase presents the private system through a five-layer architecture: control, evidence, engines, governance, and productization boundary.

## Layer Model

| Layer | Responsibility | Public Showcase Representation |
| --- | --- | --- |
| Work Order | Declares objective, scope, owner, and acceptance signal | `examples/toy_work_order.yaml` |
| Research Contract | Converts the work order into executable invariants and gates | `docs/architecture/layer-contracts.md` |
| Evidence DAG | Defines dependencies, lineage, and artifact expectations | `diagrams/evidence-flow.mmd` |
| Engine | Performs bounded computation under the contract | `pseudocode/factor_evidence_engine.md` |
| Artifact Manifest | Records outputs, schema, hashes, and provenance | `examples/toy_evidence_manifest.json` |
| Review Gate | Decides whether claims are admitted, blocked, or deferred | `examples/toy_gate_result.json` |

## Design Posture

The system treats research success as evidence quality, not simply positive metrics. A result is not promotion-ready unless lineage, leakage controls, sample boundaries, failure modes, and review gates are explicit.
