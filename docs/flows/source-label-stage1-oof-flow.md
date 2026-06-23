# Source-Label to Stage1 to OOF Flow

This flow shows how source-bound data becomes label views, Stage1 trainable matrices, and OOF-ready model evidence without publishing formulas, data, scores, or model internals.

## Flow

```text
ResearchWorkOrder
  -> ResearchContract
  -> source-boundary contract
  -> source manifest and source-part ledger
  -> source-backed label formula view
  -> Stage1 label/factor join plan
  -> prepared date label cache where reusable
  -> streaming trainable matrix writer
  -> trainable manifest and compact reject ledger
  -> formal OOF run spec
  -> full-manifest OOF executor
  -> sequence batch planner when sequence models are selected
  -> OOF evidence envelope
  -> confirmation-readiness gate
```

## Step Detail

| Step | Owner | Input | Output | Fail-Closed Condition |
| --- | --- | --- | --- | --- |
| WorkOrder and route charter | Layer 5 | route intent, owner, allowed next action | governed research request | missing owner or unauthorized next action |
| Contract compilation | Layer 3 | WorkOrder, app contract, policy refs | `ResearchContractPacket` | missing data, panel, label, model, statistical, or closure policy |
| Source-boundary binding | Layer 1 / Layer 3 | source manifest, source certificate ref | source-boundary evidence | stale, narrow, or incompatible source scope |
| Label formula view | Layer 4 / Layer 2 | label contract, source refs, horizon policy | logical label view manifest | formula not bound to source policy |
| Stage1 join planning | Layer 4 | factor manifest, label view, join policy | trainable join plan | direct label-part glob or missing label reader mode |
| Prepared date cache | Layer 1 | source-backed label work for a reusable date partition | cache manifest | cache identity not manifest-bound |
| Streaming trainable write | Layer 1 / Layer 2 | factor rows, label view, join keys | trainable manifest | full joined table collect required for active path |
| Reject ledger | Layer 4 / Layer 3 | unmatched or invalid join records | compact reject evidence | rejects hidden or silently dropped |
| OOF run spec | Layer 3 / Layer 4 | trainable manifest, fold policy, model policy | OOF run spec | trainable manifest is stale, narrow, or source-incompatible |
| Sequence batch planning | Layer 2 | sequence descriptors and tensor policy | fixed-shape batch plan | incomplete batch, shape drift, padding, or hidden drop |
| OOF evidence | Layer 2 / Layer 3 | model output manifest and diagnostics | OOF evidence envelope | non-finite evidence hidden or not attached |
| Readiness gate | Layer 3 / Layer 5 | OOF envelope, source-boundary proof, posture proof | passed, blocked, or deferred gate | OOF missing before CPCV or broader validation |

## Reviewable Files

- `source/omni_station/research/data/full_market_source_contract.py`
- `source/omni_station/research/pipeline/full_market_source_label_panel_materialization.py`
- `source/omni_station/research/pipeline/high_frequency_factor_line_stage1_active_boundary.py`
- `source/omni_station/research/pipeline/model_branch_oof_run_spec.py`
- `source/omni_station/research_os/applications/setup_d_confirmation_readiness.py`
- `source/omni_station/research_os/model_training/model_branch_oof_full_executor.py`
- `source/omni_station/research_os/model_training/sequence_tensor_native_kernel.py`
- `source/rust/omni_sequence_tensor_kernel_py/src/lib.rs`

## Evidence Artifacts

The examples directory contains synthetic fixtures for this flow:

- `examples/toy_source_backed_label_view_manifest.json`
- `examples/toy_stage1_trainable_manifest.json`
- `examples/toy_oof_run_spec.json`
- `examples/toy_sequence_batch_plan.json`

## Design Invariants

- labels are owned by label/outcome contracts, not by feature providers
- source-backed views can replace dense label materialization only when the manifest records formula id, horizon, cost dimension, and source policy
- trainable matrices must preserve source refs, fold policy, label reader mode, and reject evidence
- OOF cannot claim broader scope than the trainable manifest and source boundary support
- sequence OOF must preserve fixed-shape batch semantics or fail closed
- CPCV and later validation cannot run from missing, stale, diagnostic, or source-incompatible OOF evidence

