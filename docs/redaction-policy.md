# Disclosure Boundary Policy

The architecture review repository uses three visibility classes.

## Class A: Retained Module Filename

Use the retained path and filename when the name reveals architecture ownership or general engineering function.

Examples:

- `source/omni_station/research_os/kernel/spine.py`
- `source/omni_station/research_os/data_plane/manifest.py`
- `source/gpm/expr/engine_planner.py`
- `source/omni_station/apps/ui_gateway/app.py`
- `source/rust/omni_features_stream/src/lib.rs`
- `source/rust/omni_bus_iceoryx2/src/proof_atomic.rs`

The file body is still replaced with an architecture placeholder.

## Class B: Sanitized Capability Filename

Use a neutral filename when the original path would over-disclose research direction, strategy posture, vendor detail, execution posture, or unpublished result history.

Examples:

- `redacted_capabilities/research_line_a/oof_validation.py`
- `redacted_capabilities/runtime_engine_boundary/order_management_boundary.py`
- `redacted_capabilities/native_compute_infrastructure/native_candidate_materialization.py`

These placeholders make the capability reviewable without preserving an over-disclosing filename.

## Class C: Omitted Runtime Material

Omit the item completely when it would not improve architecture review or would create unnecessary disclosure risk.

Examples:

- raw data, Parquet stores, checkpoints, model weights, logs, reports, screenshots;
- credentials, tokens, environment files, host paths, usernames;
- exact strategy names, alpha formulas, feature formulas, thresholds, score values;
- task files, handoff files, queue state, local run state, generated artifacts.

## Filename-Level Disclosure Control

Filenames can reveal system posture even when source bodies are removed. They can communicate:

- research directions and hypotheses;
- model families and validation stages;
- execution posture and runtime capability;
- vendor/data dependencies;
- failure, repair, and promotion history;
- priority of unpublished research lines.

The repository therefore retains filenames only where they help architecture review. Other areas are represented through capability-level names.

## Placeholder Body Contract

Every placeholder must contain only:

- architecture role summary;
- Research OS layer or capability area;
- implementation highlights at system-design level;
- sanitized input/output contract;
- explicit note that implementation details are omitted.

It must not contain:

- production source code;
- imports, functions, classes, real configs, or executable logic;
- credentials, paths, hashes, run ids, account ids, order ids, or raw data samples;
- exact formulas, thresholds, model internals, or unpublished result metrics.
