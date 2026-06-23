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

## Contract Handoff Detail

| Handoff | Required Payload | Reviewer Question |
| --- | --- | --- |
| Layer 5 to Layer 4 | WorkOrder, route charter, owner, allowed next action, stage, blockers | Is this an authorized research action? |
| Layer 4 to Layer 3 | app contract, proposed evidence path, required policies, expected packet types | Is the app trying to bypass system law? |
| Layer 3 to Layer 2 | EvidenceDAG node, engine id, input manifests, policy refs, failure policy | Is the engine call bounded and authorized? |
| Layer 2 to Layer 1 | projected columns, partition plan, materialization policy, cache/checkpoint policy | Is physical work controlled and reproducible? |
| Layer 1 to Layer 3 | manifests, schema/content hashes, source refs, progress and write evidence | Is the artifact consumable evidence? |
| Layer 3 to Layer 5 | evidence envelope, gate result, admitted/blocked claims, closure packet | Does governance have enough evidence to decide? |

## Cross-Layer Invariants

- an artifact without a manifest is not decision-grade evidence
- an engine run without a ResearchContract is diagnostic at most
- a metric without claim limits cannot promote a route
- a source-backed label view must declare source refs, formula ref, horizon, cost dimension, and materialization policy
- a trainable matrix must declare label reader mode, join policy, fold policy, and reject evidence
- an OOF spec must bind trainable manifest, fold policy, model policy, source boundary, and runtime posture
- a runtime-capable consumer remains blocked unless explicitly allowed by route authority and promotion gates
