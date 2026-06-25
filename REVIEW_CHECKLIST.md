# Technical Review Checklist

Use this checklist to inspect the showcase as a verifiable architecture artifact.

## Reproducibility Checks

- Run `python scripts/verify_showcase.py`.
- Confirm Python capsule tests, Rust capsule tests, path-reference checks, redaction scans, tracked-file hygiene, inventory checks, and count-metadata checks pass.
- Confirm the toy source-to-OOF flow matches both pass and blocked golden reports under `examples/`.
- Confirm examples are synthetic and do not claim production research results.

## Architecture Checks

- Research work starts from explicit ownership: WorkOrder, application contract, evidence packet, gate, closure, and memory.
- Evidence is consumed through manifests and artifact references, not latest-file lookup.
- Runtime, execution, and order-management surfaces are represented as separated boundaries, not direct research outputs.

## Quant Validation Checks

- Feature availability is point-in-time relative to decision timestamps.
- Label windows are forward-looking and fold embargo rules are explicit.
- OOF metrics are tied to fold and regime group keys and handle non-finite values deterministically.
- Gate decisions fail closed when support artifacts are missing, stale, diagnostic-only, or outside the dependency ancestry.

## Physical-Plan Checks

- Source-backed label views avoid dense row-level writes when a logical view is sufficient.
- Performance claims name physical work removed: projection width, scan count, materialization, repeated joins, Python loops, or native boundary work.
- Rust/native surfaces expose deterministic validation, memory layout expectations, and edge-case tests.

## Redaction Checks

- No strategy formulas, feature definitions, model weights, prediction values, broker details, credentials, account identifiers, local paths, runtime logs, or production datasets are present.
- Redacted capability placeholders are used where original names would over-disclose research direction or execution posture.
- Runnable code capsules use toy inputs and public-safe algorithms only.
