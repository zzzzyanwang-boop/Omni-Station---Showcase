# OmniStation Research OS Architecture Review

OmniStation is a quantitative research operating system for turning research intent into governed evidence, reproducible artifacts, and reviewable promotion decisions. This repository presents the architecture surface of the system: retained module paths, sanitized capability boundaries, diagrams, pseudocode, and synthetic contract fixtures.

The repository is designed for technical architecture review, not production runtime execution or strategy reproduction. In the source-shaped tree, implementation bodies are replaced with module-level responsibility summaries so the design can be inspected through ownership, contracts, failure boundaries, validation posture, data lineage, and operational controls. Compact code capsules are included separately where a public-safe implementation is useful for verification.

## Verify First

Run the same checks used by CI before reviewing the architecture:

```powershell
python scripts/verify_showcase.py
```

For a fast technical review, start with `docs/review-in-10-minutes.md`. For source-to-proof mapping, use `docs/review-traceability.md`.

The verifier runs all public-safe Python code capsules, the toy source-to-OOF gate flow, the Rust capsule tests, markdown path checks, redaction scans, tracked-file hygiene checks, inventory checks, count-metadata drift checks, source placeholder schema lint, traceability checks, and benchmark smoke checks. The toy end-to-end flow is pinned against both pass and blocked golden reports under `examples/`.

Current review surface:

- 831 source-shaped module placeholders
- 39 sanitized capability placeholders
- 55 five-layer skeleton README nodes
- 35 architecture and flow documents
- 24 synthetic examples
- 12 pseudocode sketches
- 8 Mermaid diagrams
- 9 runnable public-safe code capsule roots

## Research OS Five-Layer Architecture

OmniStation follows the Research OS layer model from the full-system design baseline:

1. Layer 5 - Research Governance & Operations: WorkOrders, route authority, owners, stages, blockers, allowed next actions, freeze/stop/waiver/retirement decisions, and Research Mission Control.
2. Layer 4 - Research Applications: Idea Intake, Mechanism Memo, Data & Panel Contract, Feature / Factor Foundry, Discovery, Review & Freeze, Confirmation, Decision Score, Economic Replay, Portfolio Utility, Closure, Memory, and Quarantine apps.
3. Layer 3 - Evidence / Contract / DAG Kernel: ResearchContractCompiler, EvidenceEnvelope, EvidenceDAG, ArtifactManifestStore, RouteAuthorityRegistry, TrialBudgetLedger, DiscoverySeal, ConfirmatorySpec, and ClosureArbitration.
4. Layer 2 - Provider / Model / Runtime Engines: FeatureProvider, ExternalFactorProvider, SignalStateProvider, EconomicStateProvider, LabelOracle, ModelZoo, Calibration/OOD, DecisionRuntime, ExecutionReplayEngine, and PortfolioEngine.
5. Layer 1 - Data / Compute / Artifact Infrastructure: market-data inputs, Parquet/Arrow/manifests, cache, partitioning, atomic writes, station runners, progress events, Rust-native compute surfaces, local compute, and GPU-ready training surfaces.

## Architecture Review Focus

This repository is organized so a technical reviewer can evaluate:

- whether research work has explicit ownership from WorkOrder through application, contract, engine call, artifact, gate, closure, and memory;
- how the system separates governance, research applications, evidence kernel, reusable engines, and physical infrastructure;
- how feature, label, OOF, CPCV, replay, risk, and promotion artifacts become manifest-bound evidence instead of loose files;
- how leakage controls, fold-local policies, multiple-testing discipline, and fail-closed gates are represented at system boundaries;
- how decision runtime, execution replay, cost/capacity, and order-management boundaries remain separated from research evidence;
- how operator-facing read models expose stage, blocker, allowed action, evidence state, and review results without requiring direct access to runtime internals;
- how performance-sensitive paths are shaped around columnar artifacts, projection width, scan count, source-backed formula views, date-level scheduler caches, checkpoint semantics, Rust/native kernel boundaries, cross-language parity checks, and progress telemetry;
- how the application catalog, evidence-kernel contracts, engine fabric, pseudocode, and synthetic manifests connect into one reviewable path from source-bound data to OOF evidence;
- how capability rationale, failure modes, quant validation controls, performance physical plans, and selected source paths demonstrate engineering reasoning without publishing implementation code.

## Rust / Native Compute Surface

The repository now includes a source-shaped Rust surface under `source/rust/`. It preserves selected crate and file names where they demonstrate engineering scope without exposing implementation bodies. The retained paths cover:

- wire-codec and cross-language fixture boundaries;
- low-latency bus, journal, recorder, and replay surfaces;
- feature-stream validation and benchmark harnesses;
- DataFusion-style query entrypoints and PyO3 bridges used by Python orchestration;
- counterfactual execution, microstructure simulation, inference contracts, market-gateway frame/replay logic, observability, profiling, and deterministic rules surfaces.

The review signal is not that Rust exists as a label. The signal is that performance-sensitive work is split into contract-bound native crates, parity-tested language bridges, explicit memory and IO boundaries, and evidence-producing benchmarks or validation harnesses.

## Recent Optimization Surface

The showcase now includes the newest reviewable optimization surfaces:

- source-boundary-bound full-market source/label panel materialization;
- source-backed formula views that avoid dense row-level label materialization;
- manifest-aware Stage1 label/factor joins that keep source-backed labels lazy and stream matched trainable rows to columnar output;
- date-level prepared label cache scheduling for repeated same-date factor joins;
- formal OOF run-spec rebinding gates that block stale or narrow-universe artifacts from claiming broader source-boundary authority;
- coalesced fixed-shape sequence batch planning and Rust/PyO3 sequence tensor kernel contracts for sequence-model OOF stability.

These are presented as architecture and contract evidence only. Exact market-data counts, local runtime directories, performance traces, formulas, certificate hashes, and model outputs are not part of the review surface.

## Evidence Boundary

The repository preserves architecture evidence while separating it from implementation IP. Module paths are retained where the filename communicates system ownership. Capability-level placeholders are used where the exact filename would over-disclose research direction, vendor dependency, execution posture, or unpublished result history. Examples use synthetic identifiers, hashes, row counts, and reports so contract shape can be reviewed without implying a production research result.

This boundary is part of the engineering design: the review surface should demonstrate system structure, contract discipline, evidence flow, and operational control without making strategies, data, model internals, or runtime configuration reproducible.

## Repository Map

```text
source/                 Source-shaped Python, TypeScript, and Rust module tree with architecture placeholder bodies
redacted_capabilities/  Sanitized capability boundary placeholders
skeleton/               Five-layer Research OS skeleton with README-only boundary nodes
docs/
  architecture/          Five-layer architecture, contracts, lineage, and validation notes
  flows/                 Research workflow and evidence flow notes
  technical-review-map.md
  capability-coverage.md
  redacted-capability-inventory.md
  redaction-policy.md
  export-coverage.md
diagrams/                Mermaid diagrams for system and evidence flows
pseudocode/              Language-neutral sketches of core workflows
examples/                Synthetic work orders, manifests, and gate reports
code_capsules/           Small runnable public-safe implementations with tests
scripts/                 Repository verification script used by CI
.github/workflows/       CI workflow for tests, path checks, redaction scan, and hygiene
```

## Source-Shaped Module Tree

The `source/` tree gives reviewers a navigable map of selected real modules across Research OS governance, application contracts, evidence kernel modules, provider/runtime engines, data-plane infrastructure, Rust-native crates, UI/read-model surfaces, and test contracts.

Each placeholder file contains:

- retained module path and filename;
- Research OS layer;
- module responsibility;
- implementation highlights at system-design level;
- sanitized input/output contract;
- implementation details intentionally omitted from the review surface.

## Sanitized Capability Boundaries

The `redacted_capabilities/` tree documents capabilities whose exact module names would reveal more than the architecture needs to prove. The directory uses neutral boundary names such as `research_line_a`, `runtime_engine_boundary`, `order_management_boundary`, and `native_compute_infrastructure`.

These placeholders cover candidate lifecycles, feature/label contracts, source-backed label views, OOF/CPCV validation, model governance, risk and replay economics, promotion freeze gates, execution safety, order-management boundaries, source quality, native performance work, and operator-facing evidence surfaces.

## Runnable Code Capsules

The `code_capsules/` tree contains compact public-safe implementations that can be run and tested. They are not production OmniStation source code. They use synthetic inputs to demonstrate evidence-DAG validation, point-in-time/fold leakage checks, purged CPCV split validation, source-backed label view planning, grouped OOF metric aggregation, artifact manifest hashing, source-part joinability gating, a Rust sequence-tensor native-kernel shape, and one toy end-to-end source-to-OOF gate flow with pass and blocked golden reports.

Run `python scripts/verify_showcase.py` to execute the same checks used by CI.

## Technical Review Criteria

The design should be evaluated on:

- ownership boundaries between governance, applications, kernel, engines, infrastructure, and UI/read models;
- reproducible evidence chains through manifests, schema/content hashes, evidence envelopes, and explicit gate results;
- fail-closed behavior for missing lineage, stale inputs, unsupported claims, or incomplete validation;
- separation between offline research evidence, promotion review, and live-capable runtime surfaces;
- reviewable artifacts instead of informal notebooks, ad hoc scripts, or latest-file conventions;
- physical execution awareness in data layout, materialization, cache policy, Rust/native execution, bridge parity, memory ownership, and progress reporting.

## Suggested Reading Order

1. `docs/review-in-10-minutes.md`
2. `docs/review-traceability.md`
3. `docs/architecture/five-layer-architecture.md`
4. `docs/technical-review-map.md`
5. `docs/capability-rationale.md`
6. `docs/architecture/research-application-catalog.md`
7. `docs/architecture/evidence-kernel-contracts.md`
8. `docs/architecture/engine-fabric.md`
9. `docs/architecture/failure-mode-matrix.md`
10. `docs/architecture/selected-source-path-guide.md`
11. `docs/flows/source-label-stage1-oof-flow.md`
12. `docs/flows/quant-research-validation-playbook.md`
13. `docs/flows/performance-optimization-playbook.md`
14. `skeleton/`
15. `source/README.md`
16. `docs/capability-coverage.md`
17. `docs/source-inventory.md`
18. `docs/redaction-policy.md`
19. `docs/redacted-capability-inventory.md`
20. `redacted_capabilities/README.md`
21. `diagrams/five-layer-architecture.mmd`
22. `diagrams/source-to-oof-flow.mmd`
23. `diagrams/capability-rationale-map.mmd`
24. `pseudocode/research_run_orchestrator.md`
25. `code_capsules/README.md`
26. `REVIEW_CHECKLIST.md`
27. `examples/`

## Fixture Semantics

The files under `examples/` are synthetic contract fixtures. They demonstrate schema shape, review semantics, and gate outcomes; they do not represent production research output or a deployable strategy.
