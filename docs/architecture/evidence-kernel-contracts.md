# Evidence Kernel Contracts

Layer 3 is the system law layer. It turns application intent into executable evidence paths and decides whether downstream consumers may use a packet.

## Kernel Objects

| Object | Responsibility | Typical Failure |
| --- | --- | --- |
| `ResearchContractCompiler` | Compile WorkOrders, route charters, policy refs, and app contracts into a typed research contract | missing policy, unsupported consumer, wrong route stage |
| `PolicyRefMap` | Bind data, panel, feature, label, model, statistical, decision, economic, and closure policy refs | stale policy, missing policy, incompatible scope |
| `RouteAuthorityRegistry` | Decide whether a route, artifact, or packet is active, diagnostic, legacy, retired, or quarantined | diagnostic packet used as confirmatory evidence |
| `TypeEffectRegistry` | Register field semantics, time semantics, leakage risk, side effects, and allowed transformations | label field appears in feature matrix |
| `ProofObligationEngine` | Generate mandatory proof obligations from route, panel, feature, label, model, and replay contracts | required proof missing or contradicted |
| `EvidenceEnvelope` | Wrap artifacts and reports with tier, claim limits, lineage, blockers, and consumer permissions | loose output without envelope |
| `EvidenceDAGCompiler` | Compile the executable dependency graph from contract and application action | engine call outside route authority |
| `ArtifactTruthResolver` | Resolve manifests, hashes, schema, source refs, revisions, and claim limits | latest-file lookup or stale artifact |
| `StageStateMachine` | Enforce legal transitions across diagnostic, discovery, frozen, confirmatory, blocked, closed, retired | confirmation without freeze |
| `TrialBudgetLedger` | Track statistical freedom, trials, folds, searches, and reuse policy | repeated discovery disguised as confirmation |
| `GateEngine` | Decide passed, blocked, deferred, diagnostic, or quarantined consumer status | unsupported claim admitted |
| `AntiCorruptionKernel` | Wrap legacy or external outputs so they cannot bypass typed contracts | legacy artifact consumed as active truth |
| `InvalidationKernel` | Propagate stale source, schema, policy, or kernel changes through dependent evidence | stale packet remains eligible |
| `ProgressStationInterface` | Attach station progress, heartbeats, checkpoints, and blockers to DAG nodes | opaque long-running execution |
| `ClosureArbitrationInterface` | Build closure case packages for Layer 5 closure authority | metric packet treated as final verdict |

## Research Contract Packet

```yaml
ResearchContractPacket:
  envelope:
    packet_type: research_contract
    evidence_tier: contract_only
    status: passed_or_blocked
  contract_id: synthetic_contract_id
  route_id: synthetic_route_id
  work_order_ref: synthetic_work_order_ref
  route_charter_ref: synthetic_route_charter_ref
  strategy_family: synthetic_strategy_family
  scope_policy_ref: synthetic_scope_policy
  data_policy_ref: synthetic_data_policy
  panel_policy_ref: synthetic_panel_policy
  feature_factor_policy_ref: synthetic_feature_policy
  label_policy_ref: synthetic_label_policy
  model_policy_ref: synthetic_model_policy
  statistical_policy_ref: synthetic_stat_policy
  decision_policy_ref: synthetic_decision_policy
  economic_policy_ref: synthetic_economic_policy
  closure_policy_ref: synthetic_closure_policy
  trial_budget_ref: synthetic_trial_budget
  allowed_stage_sequence:
    - idea
    - discovery
    - freeze
    - confirmation
    - closure
  allowed_consumers:
    - discovery_factory
    - confirmation_lab
  forbidden_consumers:
    - live_runtime
    - order_management
  runtime_posture:
    offline_only: true
    paper: false
    live: false
    broker: false
    oms: false
  blockers: []
```

## Evidence Envelope

```yaml
EvidenceEnvelope:
  envelope_id: synthetic_envelope_id
  contract_ref: synthetic_contract_id
  evidence_tier: diagnostic_or_confirmatory
  artifact_refs:
    - synthetic_artifact_manifest
  source_refs:
    - synthetic_source_manifest
  claim_limits:
    universe_scope: synthetic_scope
    horizon: synthetic_horizon
    fold_policy: synthetic_fold_policy
  diagnostic_claims:
    - synthetic_debug_claim
  confirmatory_claims:
    - synthetic_admitted_claim
  blocked_claims:
    - claim: synthetic_unsupported_claim
      reason_code: missing_required_evidence
  consumer_permissions:
    confirmation_lab: blocked_or_allowed
    economic_replay_lab: blocked_or_allowed
    runtime_surface: blocked
```

## Evidence DAG Node

```yaml
EvidenceDAGNode:
  node_id: synthetic_node_id
  node_type:
    - contract_compile
    - source_audit
    - panel_build
    - feature_materialization
    - label_view
    - trainable_join
    - oof_training
    - validation_gate
  required_inputs:
    - manifest_ref
    - policy_ref
  engine_ref: synthetic_engine_id
  expected_outputs:
    - artifact_manifest
    - evidence_envelope
  failure_policy:
    fail_closed: true
    retry_policy: explicit_only
  progress_contract:
    heartbeat_required: true
    checkpoint_required: true
```

## Gate Semantics

| Gate Output | Meaning | Downstream Permission |
| --- | --- | --- |
| `passed` | claim is supported inside the declared scope | allowed only for listed consumers |
| `blocked` | claim is unsupported or contradicted | no downstream consumer |
| `deferred` | more evidence is required | diagnostic review only |
| `diagnostic` | useful for debugging or exploration | cannot freeze, confirm, or close |
| `quarantined` | input or output is unsafe, stale, or incompatible | no consumption until repaired |

## Recent Kernel Additions

The showcase includes explicit kernel surfaces for source-boundary and OOF governance:

- source-boundary certificate compatibility before label, trainable, or OOF evidence can claim full-scope authority
- formal OOF run-spec compilation that blocks stale or narrow trainable inputs
- confirmation-readiness preflight that requires OOF evidence before CPCV or broader validation
- sequence-shape stability requirements that prevent hidden padding, silent dropping, or exception-based fallback

