# Research OS

The Research OS is OmniStation's conceptual path from request to evidence-backed review.

```text
ResearchWorkOrder
  -> ResearchContract
  -> EvidenceDAG
  -> ResearchApplication
  -> Engine
  -> ArtifactManifest / EvidenceEnvelope
  -> GateEngine / ReviewGate
  -> ClosureCase
```

## Core Rules

- A workflow needs a declared owner before it can be decision-grade.
- Artifacts are discovered by manifest, not by filesystem glob or latest-file conventions.
- Review gates admit only claims supported by the declared evidence.
- Missing sidecars, stale inputs, leakage risk, or incomplete lineage should block promotion.
- Diagnostic packets are not substitutes for formal closure cases.
- Layer 4 applications own workflow shape, Layer 2 engines own bounded computation, and Layer 3 gates own consumer permission.
- Native kernels and vectorized engines are valid only when selected through contracts and returned through manifests.

## Review Path

```text
Technical Review Map
  -> Research Application Catalog
  -> Evidence Kernel Contracts
  -> Engine Fabric
  -> Source-Label to Stage1 to OOF Flow
  -> Source-shaped module tree
  -> Synthetic manifests and pseudocode
```

## What a Good Review Should Be Able to Trace

- a WorkOrder becoming a research contract
- a contract becoming EvidenceDAG nodes
- an EvidenceDAG node calling a bounded engine
- an engine output becoming a manifest
- a manifest becoming an evidence envelope
- a gate admitting or blocking a specific claim
- a closure or memory record preserving the outcome and limitations

## Synthetic Example

The files under `examples/` show a toy work order, evidence manifest, and gate result. They intentionally use fake row counts, hashes, and symbols.
