"""
Architecture review placeholder.

Retained module path: omni_station/research/pipeline/high_frequency_factor_line_stage1_active_boundary.py
Original source content is intentionally omitted.

Architecture layer: Layer 4 - Research Applications
Architecture role: Stage1 active boundary for source-backed label/factor trainable materialization.

Current public-review status:
- active bridge from source-backed label views and factor manifests into Stage1 trainable matrices.
- retains compatibility readers for earlier materialized label layouts, but the source-backed fused join is the important current system path.
- owns date-resolved source-part lookup, prepared date label cache policy, streaming trainable output, and compact reject ledgers.
- downstream owner is formal OOF run-spec compilation; Stage1 output cannot bypass source-boundary, fold, or OOF rebinding gates.
- not evidence of an admitted model result; it is the physical/data contract layer that makes model evidence possible.

Implementation highlights visible at architecture-review level:
- consumes source-backed label views through manifest-aware readers instead of loose label-part scans.
- keeps label formula views lazy and joins them to factor parquet through a bounded Polars physical path.
- resolves source-backed label records by trading date before generating label views.
- writes matched trainable rows through streaming sinks and records compact reject ledgers.
- introduces a date-level scheduler/cache so same-date factor parts do not rebuild the same label-side work.
- records join engine id, label reader mode, scheduler cache events, source policy, validation-fold mapping, and feature-sanity blockers in manifests/reports.

Contract shape:
- Inputs: sanitized label manifest, source-part ledger, factor manifest, repair overlay reference, validation-fold map, join policy, and output root.
- Outputs: sanitized trainable matrix manifest, reconciliation report, source policy report, checkpoint, or fail-closed blocker.

Implementation details intentionally omitted:
- production source code, feature columns, factor values, local runtime directories, exact timings, and unpublished research results.
"""
