# System Summary

OmniStation is organized as a research operating system rather than a collection of scripts. The architecture emphasizes evidence provenance, repeatable gates, and explicit ownership between orchestration, engines, artifacts, and review surfaces.

This repository focuses on system architecture and decision flow. It provides a reviewable map of how research intent becomes contract-bound execution, evidence artifacts, validation gates, promotion decisions, and retained research memory.

## Engineering Themes

- Contract-first research execution.
- Manifest-bound artifact discovery instead of loose latest-file lookup.
- Separation between offline research, promotion review, and live-capable surfaces.
- Fail-closed handling for missing data, unsupported claims, and incomplete evidence.
- Review gates that make system state auditable before any downstream promotion.
- Feature, label, OOF, replay, risk, and inference artifacts treated as governed data products.
- Performance work tied to physical execution shape: scan count, projection width, materialization cost, source-backed views, date-level cache scheduling, cache lifecycle, Rust-native boundaries, bridge parity, and kernel telemetry.
- Formal OOF launch readiness tied to manifest-bound source scope, sequence batch stability, and source-boundary rebinding gates.
- Review path expanded through an application catalog, evidence-kernel contract detail, engine-fabric detail, source-to-OOF flow, pseudocode, and synthetic manifests.

## System Themes

- Alpha and factor research is framed as an evidence problem: coverage, stability, leakage, redundancy, risk identity, and claim scope.
- ML research is framed as a validation problem: fold-local selection, OOF binding, calibration, model registry, and blocked promotion when evidence is incomplete.
- Market microstructure work is framed as an execution problem: order-book inputs, replay determinism, fill/slippage/latency cost evidence, and economic pass/fail gates.
- Risk work is framed as an attribution problem: beta, sector/style controls, factor identity, and explicit separation between raw signal and neutralized alpha.
- Full-market research is framed as a source-boundary problem: downstream labels, trainable matrices, OOF run specs, and confirmation readiness must carry compatible source-boundary evidence.
- Model validation is framed as a binding problem: OOF, sequence batches, source scope, fold policy, and runtime posture must agree before broader validation can consume results.

## Review Standard

The repository is complete when a reviewer can understand the Research OS architecture, the evidence lifecycle, the validation posture, the promotion boundary, and the physical execution concerns without relying on source bodies or runtime artifacts.
