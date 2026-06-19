# Layer Contracts

This document describes the public contract between the five layers.

## Contract Summary

| From | To | Contract | Failure Rule |
| --- | --- | --- | --- |
| Control Plane | Evidence Fabric | Work order, research contract, evidence DAG | Block if owner, scope, or contract is missing |
| Evidence Fabric | Research Engines | Manifest-bound input bundle | Block if source lineage or schema is stale |
| Research Engines | Evidence Fabric | Output manifest and evidence envelope | Block if output is loose, partial, or unhashable |
| Evidence Fabric | Validation Layer | Evidence bundle with claim scope | Block claims outside manifest scope |
| Validation Layer | Productization Boundary | Review gate and closure case | Block runtime posture unless promotion evidence is explicit |

## Public-Safe Interface Sketch

```text
ResearchWorkOrder
  id
  objective
  non_goals
  owner
  acceptance_signal
  allowed_claims
  blocked_claims

ResearchContract
  work_order_id
  required_inputs
  invariants
  failure_modes
  validation_plan
  artifact_outputs

ArtifactManifest
  artifact_id
  artifact_kind
  schema_version
  row_count
  schema_hash
  content_hash
  source_refs
  claim_limits

ReviewGateResult
  admitted_claims
  blocked_claims
  deferred_claims
  evidence_refs
  closure_status
```

The real implementation is private. This sketch shows the shape of the architecture, not source code.

