# Redaction Policy

The public repository uses three visibility classes.

## Class A: Real Public-Safe Filename

Use the real path and filename when the name reveals only architecture ownership or general engineering function.

Examples:

- `source/omni_station/research_os/kernel/spine.py`
- `source/omni_station/research_os/data_plane/manifest.py`
- `source/gpm/expr/engine_planner.py`
- `source/omni_station/apps/ui_gateway/app.py`

The file body is still replaced with a public placeholder.

## Class B: Redacted Capability Filename

Use a sanitized filename when the real path would reveal private research direction, strategy posture, vendor details, execution posture, or unpublished results.

Examples:

- `redacted_capabilities/research_line_a/oof_validation.py`
- `redacted_capabilities/runtime_engine_boundary/order_management_boundary.py`
- `redacted_capabilities/native_compute_infrastructure/native_candidate_materialization.py`

These placeholders show what the system does without preserving a sensitive private filename.

## Class C: Excluded Entirely

Exclude the item completely when even a sanitized placeholder would add little public value or would create unnecessary disclosure risk.

Examples of excluded categories:

- raw data, Parquet stores, checkpoints, model weights, logs, reports, screenshots
- credentials, tokens, environment files, host paths, usernames
- exact strategy names, alpha formulas, feature formulas, thresholds, score values
- task files, handoff files, queue state, local run state, generated artifacts

## Why Filenames Are Redacted

Filenames can leak information even when source bodies are removed. They can reveal:

- research directions and hypotheses
- model families and validation stages
- execution posture and runtime capability
- vendor/data dependencies
- failure, repair, and promotion history
- priority of unpublished research lines

The showcase therefore preserves real filenames only where they are useful and safe. Sensitive areas are represented through capability-level names.

## Public File Body Contract

Every placeholder must contain only:

- public-safe role summary
- architecture layer or capability area
- implementation highlights at system-design level
- sanitized input/output contract
- explicit list of removed private material

It must not contain:

- production source code
- imports, functions, classes, real configs, or executable logic
- credentials, paths, hashes, run ids, account ids, order ids, or raw data samples
- exact formulas, thresholds, model internals, or unpublished result metrics
