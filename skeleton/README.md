# Research OS Skeleton

This directory is the quick architecture skeleton for OmniStation Research OS. It is organized by the formal five-layer model so reviewers can inspect the system from governance down to physical data and compute infrastructure.

```text
skeleton/
  layer5-research-governance-operations/
  layer4-research-applications/
  layer3-evidence-contract-dag-kernel/
  layer2-provider-model-runtime-engines/
  layer1-data-compute-artifact-infrastructure/
```

Each directory contains README-only architecture nodes. The nodes describe responsibility boundaries, not runtime source code.

## Layer Reading Model

- Layer 5 owns authority, route state, review decisions, and operator-visible governance.
- Layer 4 owns researcher-facing applications and research workflow stages.
- Layer 3 owns contracts, evidence DAGs, manifest authority, budgets, and gate semantics.
- Layer 2 owns reusable provider, model, replay, decision, and portfolio engines.
- Layer 1 owns data layout, artifact storage, compute substrate, cache, checkpoints, and progress telemetry.

The skeleton is intentionally aligned with `docs/architecture/five-layer-architecture.md` and the source-shaped inventory under `source/`.
