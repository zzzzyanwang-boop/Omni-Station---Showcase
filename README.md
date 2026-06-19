# OmniStation System Architecture Showcase

OmniStation is a private quantitative research and operations platform. This repository is a public system-architecture showcase: it documents the five-layer architecture, control flow, evidence flow, gate flow, pseudocode contracts, and synthetic examples without publishing production source code, datasets, strategies, credentials, model artifacts, or runtime outputs.

This repository is intentionally not runnable. It is designed to show architecture, process discipline, and implementation shape without exposing private implementation details.

## Five-Layer Architecture

OmniStation is presented through five public-safe layers:

1. Research Control Plane: work orders, contracts, task scope, evidence DAGs, and operator-visible state.
2. Data and Evidence Fabric: source manifests, feature/label artifacts, schema hashes, content hashes, lineage, and cache policy.
3. Research Engine Layer: factor profiling, ML training, risk sidecars, replay/evaluation, and performance-sensitive kernels.
4. Validation and Governance Layer: leakage checks, fold policies, risk attribution, execution-cost gates, review gates, and closure cases.
5. Productization Boundary Layer: UI/read models, reports, promotion packets, inference eligibility, and live-capable boundary controls.

## What This Shows

- A layered research operating model for moving from work orders to evidence, gates, and review cases.
- Separation between research orchestration, engines, contracts, artifacts, and promotion gates.
- Fail-closed posture for incomplete evidence, unsupported claims, and live-execution boundaries.
- Reproducibility concepts: manifest-bound artifacts, evidence envelopes, lineage, and explicit review results.
- Pseudocode and fake examples that illustrate implementation shape without exposing real trading logic or data.
- Process flow for alpha/factor research, ML validation, risk attribution, offline replay, performance materialization, and promotion gating.

## What Is Not Included

- Production source code or private git history.
- Real strategies, alpha formulas, feature definitions, model logic, or execution rules.
- Broker, OMS, live trading, paper trading, credentials, or deployment configuration.
- Real research datasets, market data, Parquet stores, checkpoints, model weights, logs, or reports.
- Internal operator runbooks, machine paths, usernames, queue state, or runtime artifacts.

## Repository Map

```text
docs/
  architecture/        Public architecture notes and system boundaries
  flows/               Public-safe process flows
diagrams/              Mermaid diagrams for system and evidence flows
pseudocode/            Language-neutral pseudocode for core workflows
examples/              Toy work orders, manifests, and gate reports
```

## Suggested Reading Order

1. `docs/architecture/five-layer-architecture.md`
2. `diagrams/five-layer-architecture.mmd`
3. `docs/flows/research-workflow.md`
4. `pseudocode/research_run_orchestrator.md`
5. `examples/toy_system_run_bundle.json`

## Public Boundary

All examples in this repository are fabricated. They use toy symbols, tiny row counts, placeholder hashes, and non-production names. They are included only to make the contracts readable.
