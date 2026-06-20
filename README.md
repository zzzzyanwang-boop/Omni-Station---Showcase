# OmniStation Research OS Architecture Review

OmniStation is a quantitative research operating system for turning research intent into governed evidence, reproducible artifacts, and reviewable promotion decisions. This repository presents the architecture surface of the system: retained module paths, sanitized capability boundaries, diagrams, pseudocode, and synthetic contract fixtures.

The repository is designed for technical architecture review, not runtime execution. Implementation bodies are replaced with module-level responsibility summaries so the design can be inspected through ownership, contracts, failure boundaries, validation posture, data lineage, and operational controls.

## Research OS Five-Layer Architecture

OmniStation follows the Research OS layer model from the full-system design baseline:

1. Layer 5 - Research Governance & Operations: WorkOrders, route authority, owners, stages, blockers, allowed next actions, freeze/stop/waiver/retirement decisions, and Research Mission Control.
2. Layer 4 - Research Applications: Idea Intake, Mechanism Memo, Data & Panel Contract, Feature / Factor Foundry, Discovery, Review & Freeze, Confirmation, Decision Score, Economic Replay, Portfolio Utility, Closure, Memory, and Quarantine apps.
3. Layer 3 - Evidence / Contract / DAG Kernel: ResearchContractCompiler, EvidenceEnvelope, EvidenceDAG, ArtifactManifestStore, RouteAuthorityRegistry, TrialBudgetLedger, DiscoverySeal, ConfirmatorySpec, and ClosureArbitration.
4. Layer 2 - Provider / Model / Runtime Engines: FeatureProvider, ExternalFactorProvider, SignalStateProvider, EconomicStateProvider, LabelOracle, ModelZoo, Calibration/OOD, DecisionRuntime, ExecutionReplayEngine, and PortfolioEngine.
5. Layer 1 - Data / Compute / Artifact Infrastructure: market-data inputs, Parquet/Arrow/manifests, cache, partitioning, atomic writes, station runners, progress events, local compute, native kernels, and GPU-ready training surfaces.

## Architecture Review Focus

This repository is organized so a technical reviewer can evaluate:

- whether research work has explicit ownership from WorkOrder through application, contract, engine call, artifact, gate, closure, and memory;
- how the system separates governance, research applications, evidence kernel, reusable engines, and physical infrastructure;
- how feature, label, OOF, CPCV, replay, risk, and promotion artifacts become manifest-bound evidence instead of loose files;
- how leakage controls, fold-local policies, multiple-testing discipline, and fail-closed gates are represented at system boundaries;
- how decision runtime, execution replay, cost/capacity, and order-management boundaries remain separated from research evidence;
- how operator-facing read models expose stage, blocker, allowed action, evidence state, and review results without requiring direct access to runtime internals;
- how performance-sensitive paths are shaped around columnar artifacts, projection width, scan count, cache lifecycle, checkpoint semantics, native kernels, and progress telemetry.

## Evidence Boundary

The repository preserves architecture evidence while separating it from implementation IP. Module paths are retained where the filename communicates system ownership. Capability-level placeholders are used where the exact filename would over-disclose research direction, vendor dependency, execution posture, or unpublished result history. Examples use synthetic identifiers, hashes, row counts, and reports so contract shape can be reviewed without implying a production research result.

This boundary is part of the engineering design: the review surface should demonstrate system structure, contract discipline, evidence flow, and operational control without making strategies, data, model internals, or runtime configuration reproducible.

## Repository Map

```text
source/                 Source-shaped module tree with architecture placeholder bodies
redacted_capabilities/  Sanitized capability boundary placeholders
docs/
  architecture/          Five-layer architecture, contracts, lineage, and validation notes
  flows/                 Research workflow and evidence flow notes
  capability-coverage.md
  redacted-capability-inventory.md
  redaction-policy.md
  export-coverage.md
diagrams/                Mermaid diagrams for system and evidence flows
pseudocode/              Language-neutral sketches of core workflows
examples/                Synthetic work orders, manifests, and gate reports
```

## Source-Shaped Module Tree

The `source/` tree gives reviewers a navigable map of selected real modules across Research OS governance, application contracts, evidence kernel modules, provider/runtime engines, data-plane infrastructure, UI/read-model surfaces, and test contracts.

Each placeholder file contains:

- retained module path and filename;
- Research OS layer;
- module responsibility;
- implementation highlights at system-design level;
- sanitized input/output contract;
- implementation details intentionally omitted from the review surface.

## Sanitized Capability Boundaries

The `redacted_capabilities/` tree documents capabilities whose exact module names would reveal more than the architecture needs to prove. The directory uses neutral boundary names such as `research_line_a`, `runtime_engine_boundary`, `order_management_boundary`, and `native_compute_infrastructure`.

These placeholders cover candidate lifecycles, feature/label contracts, OOF/CPCV validation, model governance, risk and replay economics, promotion freeze gates, execution safety, order-management boundaries, source quality, native performance work, and operator-facing evidence surfaces.

## Technical Review Criteria

The design should be evaluated on:

- ownership boundaries between governance, applications, kernel, engines, infrastructure, and UI/read models;
- reproducible evidence chains through manifests, schema/content hashes, evidence envelopes, and explicit gate results;
- fail-closed behavior for missing lineage, stale inputs, unsupported claims, or incomplete validation;
- separation between offline research evidence, promotion review, and live-capable runtime surfaces;
- reviewable artifacts instead of informal notebooks, ad hoc scripts, or latest-file conventions;
- physical execution awareness in data layout, materialization, cache policy, native execution, and progress reporting.

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

## Fixture Semantics

The files under `examples/` are synthetic contract fixtures. They demonstrate schema shape, review semantics, and gate outcomes; they do not represent production research output or a deployable strategy.
