# System Summary

OmniStation is organized as a research operating system rather than a collection of scripts. The architecture emphasizes evidence provenance, repeatable gates, and explicit ownership between orchestration, engines, artifacts, and review surfaces.

This public showcase focuses on system architecture and flow. It does not include private source code, private data, real research output, or non-architecture narrative.

## Engineering Themes

- Contract-first research execution.
- Manifest-bound artifact discovery instead of loose latest-file lookup.
- Separation between offline research, promotion review, and live-capable surfaces.
- Fail-closed handling for missing data, unsupported claims, and incomplete evidence.
- Feature, label, OOF, replay, risk, and inference artifacts treated as governed data products.
- Performance work tied to physical execution shape: scan count, projection width, materialization cost, cache lifecycle, and native-kernel boundaries.
