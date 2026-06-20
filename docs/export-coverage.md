# Review Coverage

This repository is an architecture review package for OmniStation. It is scoped to system structure, boundary contracts, evidence flow, validation posture, and operational controls.

## Artifact Counts

- Source-shaped retained module placeholders: 781
- Sanitized capability boundary placeholders: 34
- Architecture and flow documents: system-design summaries
- Pseudocode: language-neutral workflow sketches
- Examples: synthetic contract fixtures

## Review Surfaces

- Layer 5 governance/operations, Research Mission Control, route authority, and stage state.
- Layer 4 research applications such as intake, mechanism framing, data/panel contracts, foundry, discovery, review/freeze, confirmation, replay, closure, and memory.
- Layer 3 evidence/contracts/DAG kernel, semantic kernel, manifest store concepts, conformance, and route authority.
- Layer 2 provider/model/runtime engines, including feature providers, model validation, replay/economic engines, and runtime services.
- Layer 1 data/compute/artifact infrastructure, including manifests, cache, partitions, atomic writes, and progress evidence.
- Research foundry concepts: evidence, adversarial checks, decision runtime, economics, external-factor governance.
- Feature/label/data lineage, source quality, manifest stores, checkpoints, materialization boundaries.
- ML validation, OOF/CPCV, fold-local controls, calibration, leakage and multiple-testing controls.
- Risk/economic/replay evidence, freeze decisions, closure state, and runtime boundary contracts.
- UI gateway and operator-facing read-model surfaces.
- Tests that demonstrate fail-closed boundaries and validation contracts.

## Sanitized Boundary Surfaces

Some capability areas are represented through `redacted_capabilities/` instead of retained filenames:

- research-line lifecycles;
- alpha/factor hypotheses with over-disclosing names;
- strategy/economic evidence with sensitive naming;
- execution and order-management implementation boundaries;
- vendor/data-specific repair paths;
- native/performance work tied to non-public datasets or benchmarks.

## Boundary Controls

The export deliberately keeps the review surface separate from implementation and runtime material:

- source bodies, production settings, formulas, thresholds, and model internals are omitted;
- datasets, feature matrices, labels, OOF predictions, replay outputs, checkpoints, caches, logs, queue state, and reports are omitted;
- local paths, credentials, usernames, account ids, order ids, and run identifiers are omitted;
- original filenames are omitted when the name itself would reveal research direction, execution posture, vendor detail, or unpublished result history.

## Completeness Standard

The repository is complete when a reviewer can understand:

- the official Research OS five-layer architecture;
- how research moves from WorkOrder to Research Application, compiled contract, evidence DAG, engines, artifacts, review, closure, and memory;
- where data lineage, leakage control, OOF/CPCV, model governance, risk/replay, freeze/confirmation, and UI surfaces fit;
- which areas use sanitized capability boundaries and why.

Completeness is measured by architecture coverage and reviewability, not by mirroring every implementation file.
