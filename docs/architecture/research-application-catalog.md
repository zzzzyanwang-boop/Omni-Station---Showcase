# Research Application Catalog

Layer 4 contains applications, not scripts. Each application receives a Layer 5 WorkOrder, compiles or validates a Layer 3 contract path, calls Layer 2 engines, and returns evidence packets or blockers.

## Application Contract Shape

```yaml
ResearchApplicationContract:
  app_id: synthetic_app_id
  app_domain:
    - evidence_collection
    - panel_building
    - feature_factor_foundry
    - label_outcome
    - discovery
    - confirmation
    - model_workbench
    - economic_replay
    - closure_packaging
  accepted_work_order_types:
    - synthetic_work_order_type
  required_research_contract_refs:
    - synthetic_contract_ref
  required_policy_refs:
    - synthetic_policy_ref
  allowed_input_evidence_tiers:
    - contract_only
    - diagnostic
    - confirmatory
  produced_packet_types:
    - synthetic_packet_type
  forbidden_outputs:
    - direct_runtime_action
    - unmanifested_artifact
  lower_layer_dependencies:
    layer3:
      - EvidenceDAG
      - GateEngine
    layer2:
      - FeatureProvider
      - LabelOracle
    layer1:
      - ArtifactManifestStore
  runtime_posture:
    offline_only: true
    paper: false
    live: false
    broker: false
    oms: false
```

## Core Applications

| App | Responsibility | Reviewable Output | Boundary |
| --- | --- | --- | --- |
| A1 Ground Truth Audit App | Audit source readiness, data identity, point-in-time rules, and manifest coverage before research use | source audit packet, quarantine blocker, source-readiness read model | does not produce features, labels, or claims |
| A2 Mechanism & Hypothesis Workbench | Convert a research idea into a falsifiable mechanism hypothesis and evidence plan | mechanism memo, hypothesis graph, adversarial question list | does not admit alpha or model efficacy |
| A3 Research Contract Builder | Compile route intent, policy refs, allowed consumers, and required evidence into a contract | `ResearchContractPacket`, missing-policy blocker | does not execute engines directly |
| A4 Panel Studio | Define universe, time grain, horizon, tradability, inclusion/exclusion, and sample/full-scope status | panel contract, panel readiness packet | does not create labels or model outputs |
| A5 Feature Foundry | Build and qualify feature/factor artifacts under source, fold, and leakage policy | feature manifest, factor profile, preflight packet | does not decide final research validity |
| A6 External Factor Foundry | Govern external-factor intake, mapping, license posture, dependency, and requalification | external-factor registry packet, option ledger, requalification packet | does not allow source names or vendor detail to become strategy claims |
| A7 SignalState Lab | Evaluate state-machine or regime signals as diagnostic or admitted providers | signal-state evidence packet, consumer-port permission | cannot enter OOF without explicit route authority |
| A8 Label & Outcome Lab | Own label and target semantics through source-backed or materialized label contracts | label contract, label-view manifest, label blocker | features cannot own label truth |
| A9 Discovery Factory | Explore candidates under trial budget and discovery-only evidence tier | discovery packet, trial ledger update, rejected-candidate ledger | discovery output cannot enter confirmation directly |
| A10 Feature / Factor Strength Preflight Lab | Check strength, stability, leakage, redundancy, and feasibility before freeze | preflight report, factor eligibility packet | metrics do not become closure verdicts |
| A11 Freeze Package Builder | Freeze selected features, factors, models, contracts, and evidence scope for confirmatory work | freeze packet, frozen subset manifest, immutable review inputs | frozen inputs cannot mutate silently |
| A12 Confirmation Lab | Run confirmatory validation against frozen contract and trial budget | confirmation packet, passed/blocked gate result | cannot run from diagnostic or unfrozen inputs |
| A13 Statistical Validation Workbench | Validate statistical controls, multiple testing, folds, embargo, robustness, and uncertainty | statistical validation packet, trial-budget report | cannot override route authority |
| A14 Model Zoo Workbench | Train, compare, and qualify models through OOF, calibration, and registry contracts | OOF manifest, model candidate packet, calibration input | model scores do not imply action eligibility |
| A15 Calibration / OOD / DecisionScore Lab | Assess score reliability, OOD behavior, uncertainty, and decision-score eligibility | calibration packet, OOD report, decision-score packet | does not create execution intent |
| A16 Decision Runtime Lab | Compile score-to-intent readiness and runtime boundary evidence | runtime eligibility packet, action-intent preflight | cannot enable live-capable routes without higher gates |
| A17 Economic Replay & Portfolio Utility Lab | Replay offline economics, costs, capacity, round-trip accounting, and portfolio contribution | replay packet, cost/capacity packet, utility packet | replay is not live readiness |
| A18 Closure Package Builder + Research Memory App | Build closure cases and persistent memory from admitted and blocked evidence | closure case package, memory entry | final verdict belongs to Layer 5 closure authority |

## Extension Applications

| App | Responsibility | Reviewable Output | Boundary |
| --- | --- | --- | --- |
| A19 Setup Expansion Studio | Govern expansion from one setup route to additional setup templates | setup route charter, template compatibility packet | cannot reuse setup evidence across incompatible route contracts |
| A20 Factor-First Workbench | Run factor-first discovery, panel eligibility, baskets, and confirmation path | factor-first contract, factor basket packet | kept separate from setup-first route authority |
| A21 Metric Computation Lab | Compute reusable statistical, economic, portfolio, and attribution metrics under metric contracts | metric evidence packet, metric artifact manifest | metric computation does not interpret research outcome |
| A22 Performance Diagnostics Lab | Profile physical execution, data movement, kernels, cache behavior, and materialization cost | performance evidence packet, bottleneck report | performance evidence cannot weaken validation evidence |
| A23 Cross-Lane Attribution Lab | Compare routes, factor families, model branches, and economic attribution across lanes | cross-lane attribution packet, overlap/redundancy report | cannot promote one lane by borrowing another lane's evidence |

## Recently Added Application Detail

### Source / Label Panel Materialization

Review signal:

- binds label views to source-boundary evidence
- can represent labels as source-backed formula views rather than dense row-level label tables
- publishes source-part ledgers and materialization policy
- blocks stale, interrupted, diagnostic, or incompatible materialization roots

Representative files:

- `source/omni_station/research/data/full_market_source_contract.py`
- `source/omni_station/research/pipeline/full_market_source_label_panel_materialization.py`
- `redacted_capabilities/data_compute_artifact_infrastructure/source_backed_label_formula_view.py`

### Stage1 Source-Backed Trainable Boundary

Review signal:

- joins source-backed labels to factor artifacts through manifest-aware readers
- resolves source parts by date before building label views
- streams matched trainable rows to columnar output
- records compact reject ledgers and scheduler-cache evidence

Representative files:

- `source/omni_station/research/pipeline/high_frequency_factor_line_stage1_active_boundary.py`
- `redacted_capabilities/data_compute_artifact_infrastructure/stage1_source_backed_join_scheduler.py`

### Formal OOF Readiness and Sequence Stability

Review signal:

- blocks stale or narrow trainable manifests from broader OOF claims
- binds OOF run specs to source-boundary evidence and fold policy
- coalesces descriptor runs into fixed-shape sequence batches
- routes sequence tensor assembly through a Rust/PyO3 kernel contract

Representative files:

- `source/omni_station/research/pipeline/model_branch_oof_run_spec.py`
- `source/omni_station/research_os/applications/setup_d_confirmation_readiness.py`
- `source/omni_station/research_os/model_training/model_branch_oof_full_executor.py`
- `source/rust/omni_sequence_tensor_kernel_py/src/lib.rs`

