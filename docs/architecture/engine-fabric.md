# Engine Fabric

Layer 2 is a controlled engine fabric. Engines compute artifacts or scores, but they do not own research conclusions.

## Engine Service Contract

```yaml
EngineServiceContract:
  engine_id: synthetic_engine_id
  engine_domain:
    - data_access
    - panel
    - feature
    - external_factor
    - signal_state
    - label
    - model
    - calibration_ood
    - decision_score
    - decision_runtime
    - execution_replay
    - economic_accounting
    - portfolio
    - metric
  owner_module: synthetic_owner
  accepted_task_types:
    - synthetic_task_type
  accepted_input_ref_types:
    - artifact_manifest
    - source_manifest
    - evidence_envelope
  produced_artifact_types:
    - synthetic_artifact_type
  required_policy_refs:
    - synthetic_policy_ref
  deterministic: true_or_false
  random_seed_policy: explicit_or_not_applicable
  side_effect_class:
    - read_only
    - materialization
    - training
    - replay
    - diagnostic
  runtime_posture:
    offline_only: true
    paper: false
    live: false
    broker: false
    oms: false
  cache_policy: manifest_bound
  checkpoint_policy: explicit
  failure_policy:
    fail_closed: true
  forbidden_outputs:
    - research_verdict
    - runtime_action
```

## Engine Run Record

```yaml
EngineRunRecord:
  engine_id: synthetic_engine_id
  work_order_ref: synthetic_work_order_ref
  research_contract_ref: synthetic_contract_ref
  evidence_dag_node_ref: synthetic_node_ref
  input_manifest_refs:
    - synthetic_input_manifest
  output_manifest_refs:
    - synthetic_output_manifest
  status: passed_or_blocked
  rows_processed: synthetic_count
  columns_projected: synthetic_count
  partitions_processed: synthetic_count
  bytes_in: synthetic_size
  bytes_out: synthetic_size
  elapsed_ms: synthetic_duration
  cache_hits: synthetic_count
  cache_misses: synthetic_count
  checkpoint_refs:
    - synthetic_checkpoint
  schema_hash: synthetic_hash
  content_hash: synthetic_hash
  warnings: []
  blockers: []
```

## Engine Families

| Engine | Role | Review Signal |
| --- | --- | --- |
| E2.1 Data Access & AsOf Engine | Resolve source and normalized data through point-in-time and availability semantics | no loose data reads; available-time proof is explicit |
| E2.2 Panel Provider Engine | Build eligible panels for setup-first, factor-first, model, or replay workflows | panel scope and exclusions are manifest-bound |
| E2.3 Setup Lifecycle / PathState Engine | Produce setup lifecycle state and anchor eligibility | missing anchors block downstream feature generation |
| E2.4 Setup-Native Feature Provider | Materialize setup-native features under contract | features carry source, fold, and time semantics |
| E2.5 External Factor Provider | Govern external-factor mapping, dependency, and setup/factor-first use | external factor cannot bypass registry and licensing posture |
| E2.6 SignalState Provider | Produce state-machine or regime outputs for allowed consumer ports | diagnostic-only state cannot enter OOF without authority |
| E2.7 EconomicState / H-Gate Provider | Produce economic state or higher-level gate inputs | economic state is not replay outcome |
| E2.8 Label & Outcome Oracle Engine | Own label, target, outcome, and source-backed label-view semantics | label fields cannot enter features |
| E2.9 Feature / Factor Preflight Engine | Compute factor strength, leakage, redundancy, and feasibility evidence | metrics are tied to fold and panel policy |
| E2.10 Model Zoo Engine | Train, compare, and emit OOF/model candidate artifacts | scores are evidence inputs, not conclusions |
| E2.11 Calibration / OOD / Uncertainty Engine | Evaluate score reliability, drift, uncertainty, and OOD behavior | calibration is bound to OOF and source scope |
| E2.12 DecisionScore Engine | Convert evidence into decision-score eligibility under policy | no action intent is emitted |
| E2.13 DecisionRuntime Engine | Compile runtime eligibility and action-intent preconditions | live-capable boundary remains blocked without higher authority |
| E2.14 Execution Replay Engine | Replay offline execution paths, cost, fills, and round-trip state | replay does not equal live readiness |
| E2.15 Economic Accounting Engine | Separate realized round-trip, mark-to-market, fees, borrow, and capacity assumptions | accounting semantics are explicit |
| E2.16 Portfolio Utility Engine | Evaluate portfolio-level utility, exposure, drawdown, and contribution | portfolio result is one closure input |
| E2.17 Metric Computation Engine | Compute reusable metric artifacts across statistical/economic/portfolio domains | computation and interpretation are separate |
| E2.18 Statistical Metric Engine | Compute fold, uncertainty, trial-budget, and robustness statistics | cannot override TrialBudget conclusions |
| E2.19 Economic Metric Engine | Compute cost, capacity, turnover, PnL, and replay metrics | metric packet cannot admit economic validity alone |
| E2.20 Portfolio Metric Engine | Compute portfolio utility and attribution metrics | no direct promotion authority |
| E2.21 Cross-Lane Attribution Engine | Compare overlap, redundancy, and contribution across routes | evidence borrowing is blocked unless contracted |
| E2.22 Setup Route Template Provider | Provide setup template compatibility and route expansion evidence | setup expansion is not automatic reuse |
| E2.23 Factor-First Panel Provider | Provide factor-first panel eligibility and basket inputs | separated from setup-first authority |

## Native and Vectorized Boundary

Native or vectorized execution is allowed only when it is selected through an engine contract and produces the same evidence shape as the reference path.

Reviewable native surfaces include:

- `source/rust/omni_expr_compiler_py/src/lib.rs`
- `source/rust/omni_features_stream/src/lib.rs`
- `source/rust/omni_datafusion_query/src/lib.rs`
- `source/rust/omni_counterfactual_execution_kernel_py/src/lib.rs`
- `source/rust/omni_sequence_tensor_kernel_py/src/lib.rs`

Required bridge evidence:

- engine id and native kernel id
- input schema and null policy
- memory ownership and copy policy
- parity or equivalence gate
- unsupported-mode blocker
- telemetry for rows, partitions, projected columns, cache, and kernel phase timing

