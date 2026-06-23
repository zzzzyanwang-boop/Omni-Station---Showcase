"""
Architecture review placeholder.

Retained module path: omni_station/apps/ui_gateway/recovery_service.py
Original source content is intentionally omitted.

Architecture layer: Layer 5 - Research Governance & Operations
Architecture role: operator-facing UI gateway and read-model surface.

Current source-shaped status:
- actual source file exists at the retained path in the working system.
- this placeholder preserves the file name and module ownership while replacing implementation code with a structural summary.
- the file belongs to the operator-facing UI gateway and read-model surface.
- implementation behavior, algorithms, parameters, thresholds, and data access details are not included.

Actual structural signals (parsed from retained top-level symbols):
Top-level classes:
- none exposed at top level or intentionally omitted

Top-level functions:
- `utc_now_iso`
- `iso_ts`
- `_json_load`
- `_validate_payload`
- `_progress_age_sec`
- `_fallback_age_sec`
- `classify_stale_running_job`
- `recover_stale_running_jobs`

Reviewable responsibilities inferred from source location and file name:
- maintain the boundary implied by the retained module path.
- exchange data through contracts, manifests, packets, read models, or typed helper APIs rather than loose runtime state.
- support the surrounding Research OS layer without becoming an unowned side path.
- fail closed or produce explicit blockers where the surrounding layer requires evidence.

Contract shape:
- Inputs: sanitized contract, manifest, policy, state, request, or artifact references appropriate to this module boundary.
- Outputs: sanitized packet, manifest update, read model, gate result, helper result, or blocker.

Implementation details intentionally omitted:
- production source code, function bodies, algorithms, formulas, thresholds, credentials, data paths, local configuration, runtime state, and unpublished results.
"""
