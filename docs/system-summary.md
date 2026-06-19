# System Summary

OmniStation is organized as a research operating system rather than a collection of scripts. The architecture emphasizes evidence provenance, repeatable gates, and explicit ownership between orchestration, engines, artifacts, and review surfaces.

This public showcase focuses on system architecture and flow. It does not include private source code, private data, real research output, or non-architecture narrative.

## Engineering Themes

- Contract-first research execution.
- Manifest-bound artifact discovery instead of loose latest-file lookup.
- Separation between offline research, promotion review, and live-capable surfaces.
- Fail-closed handling for missing data, unsupported claims, and incomplete evidence.
- Review gates that make system state auditable before any downstream promotion.
- Feature, label, OOF, replay, risk, and inference artifacts treated as governed data products.
- Performance work tied to physical execution shape: scan count, projection width, materialization cost, cache lifecycle, and native-kernel boundaries.

## System Themes

- Alpha and factor research is framed as an evidence problem: coverage, stability, leakage, redundancy, risk identity, and claim scope.
- ML research is framed as a validation problem: fold-local selection, OOF binding, calibration, model registry, and blocked promotion when evidence is incomplete.
- Market microstructure work is framed as an execution problem: order-book inputs, replay determinism, fill/slippage/latency cost evidence, and economic pass/fail gates.
- Risk work is framed as an attribution problem: beta, sector/style controls, factor identity, and explicit separation between raw signal and neutralized alpha.

## Public Showcase Scope

This repository demonstrates structure and decision quality. It does not publish the private implementation or any production research result.
