# Research OS

The Research OS is the private system's conceptual path from request to evidence-backed review.

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

## Public Example

The files under `examples/` show a toy work order, evidence manifest, and gate result. They intentionally use fake row counts, hashes, and symbols.

