# OmniStation System Architecture Showcase

OmniStation is a private quantitative research and operations platform. This repository is a public system-architecture showcase: it preserves a public-safe subset of the real source tree while replacing every implementation body with module highlights, responsibility summaries, sanitized input/output contracts, and explicit disclosure boundaries.

This repository is intentionally not runnable. The files under `source/` keep original public-safe paths and filenames, but their contents are documentation placeholders rather than production source code.

Sensitive areas are represented separately under `redacted_capabilities/` with sanitized names. This proves coverage of private research lines, strategy/economic evidence, execution safety, order-management boundaries, vendor/data boundaries, and native/performance work without disclosing filenames that would reveal private research assets.

## Five-Layer Architecture

OmniStation is presented through five public-safe layers:

1. Research Control Plane: work orders, contracts, task scope, evidence DAGs, and operator-visible state.
2. Data and Evidence Fabric: source manifests, feature/label artifacts, schema hashes, content hashes, lineage, and cache policy.
3. Research Engine Layer: factor profiling, ML training, risk sidecars, replay/evaluation, and performance-sensitive kernels.
4. Validation and Governance Layer: leakage checks, fold policies, risk attribution, execution-cost gates, review gates, and closure cases.
5. Productization Boundary Layer: UI/read models, reports, promotion packets, inference eligibility, and live-capable boundary controls.

## What This Shows

- The source-shaped architecture of the private system, including actual public-safe module paths and file names.
- Redacted capability structures for sensitive research, execution, order-management, vendor/data, and performance surfaces.
- A capability matrix mapping system abilities to public-safe real files and redacted placeholders.
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
source/               Public-safe source-shaped skeleton with placeholder file bodies
redacted_capabilities/ Sanitized capability placeholders for sensitive private surfaces
docs/
  architecture/        Public architecture notes and system boundaries
  flows/               Public-safe process flows
  capability-coverage.md
  redacted-capability-inventory.md
  redaction-policy.md
  export-coverage.md
diagrams/              Mermaid diagrams for system and evidence flows
pseudocode/            Language-neutral pseudocode for core workflows
examples/              Toy work orders, manifests, and gate reports
```

## Source-Shaped Skeleton

The `source/` tree is the core of this showcase. It mirrors selected real paths such as Research OS contracts, data-plane boundaries, research engines, evidence/gate modules, validation and governance layers, performance/materialization components, UI read models, and test contracts.

Each placeholder file contains:

- original public-safe path and filename
- architecture layer
- module responsibility
- implementation highlights visible at the system-design level
- sanitized input/output contract
- private material removed from the public version

It deliberately excludes data, runtime outputs, private configs, task files, logs, checkpoints, model artifacts, credentials, local paths, strategy-specific filenames, and any source body that would make private research reproducible.

## Redacted Capabilities

The `redacted_capabilities/` tree covers sensitive areas where the real filename itself would disclose too much. The files use sanitized names such as `research_line_a`, `execution_boundary`, `order_management_boundary`, and `performance_native_paths`.

This layer shows that the private system includes candidate lifecycles, feature/label contracts, OOF/CPCV validation, model governance, risk/replay economics, promotion freeze gates, execution safety, order-management boundaries, source quality, native performance work, and operator-facing evidence surfaces without exposing private strategy names or implementation.

## Evaluation Lens

The point of the design is not to claim a public trading edge. The point is to show how the private system is structured to support disciplined quantitative research:

- clear ownership boundaries
- reproducible evidence chains
- fail-closed validation gates
- promotion controls
- operational separation between offline research and live-capable surfaces
- reviewable artifacts instead of informal notebooks or loose files

## Suggested Reading Order

1. `docs/architecture/five-layer-architecture.md`
2. `source/README.md`
3. `docs/capability-coverage.md`
4. `docs/source-inventory.md`
5. `docs/redaction-policy.md`
6. `docs/redacted-capability-inventory.md`
7. `redacted_capabilities/README.md`
8. `diagrams/five-layer-architecture.mmd`
9. `docs/flows/research-workflow.md`
10. `pseudocode/research_run_orchestrator.md`
11. `examples/`

## Public Boundary

All examples in this repository are fabricated. They use toy symbols, tiny row counts, placeholder hashes, and non-production names. They are included only to make the contracts readable.
