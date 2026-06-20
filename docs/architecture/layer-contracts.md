# Layer Contracts

This document describes the reviewable contract between the Research OS layers.

## Contract Summary

| From | To | Contract | Failure Rule |
| --- | --- | --- | --- |
| Layer 5 - Research Governance & Operations | Layer 4 - Research Applications | WorkOrder, route charter, owner, allowed next action | Block if route ownership, stage, or authority is missing |
| Layer 4 - Research Applications | Layer 3 - Evidence / Contract / DAG Kernel | Application-scoped research intent and required evidence path | Block if the app tries to bypass ResearchContract compilation |
| Layer 3 - Evidence / Contract / DAG Kernel | Layer 2 - Provider / Model / Runtime Engines | Compiled contract, evidence DAG, input manifest requirements, trial budget | Block if execution is loose, diagnostic-only, or outside route authority |
| Layer 2 - Provider / Model / Runtime Engines | Layer 1 - Data / Compute / Artifact Infrastructure | Bounded engine request and physical artifact requirements | Block if data, compute, cache, checkpoint, or artifact ownership is missing |
| Layer 1 - Data / Compute / Artifact Infrastructure | Layer 3 - Evidence / Contract / DAG Kernel | Manifest-bound artifact, schema/content hashes, lineage, progress and write evidence | Block if output is partial, unhashable, stale, or not contract-bound |
| Layer 3 - Evidence / Contract / DAG Kernel | Layer 5 - Research Governance & Operations | Evidence envelope, review gate result, closure/freeze/retirement state | Block claims outside the compiled contract or approved route stage |

## Interface Sketch

```text
ResearchWorkOrder
  id
  owner
  route_candidate
  requested_stage
  allowed_next_action
  blocked_claims

ResearchRouteCharter
  route_id
  research_mode
  owners
  allowed_consumers
  forbidden_consumers
  required_review_gates
  trial_budget_policy
  closure_policy

ResearchContract
  route_id
  application_owner
  required_inputs
  required_engines
  evidence_dag
  invariants
  failure_modes
  artifact_outputs

EvidenceEnvelope
  contract_id
  evidence_refs
  diagnostic_claims
  confirmatory_claims
  blocked_claims
  trial_budget_refs

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
  freeze_state
  closure_status
```

This sketch shows the architecture contract shape, not production source code.
