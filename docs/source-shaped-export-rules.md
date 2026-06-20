# Source-Shaped Export Rules

The architecture export is allowlist-based. It retains module paths that help reviewers understand system ownership while replacing implementation bodies with descriptive placeholders.

## Retained Surfaces

- Research OS governance/operations, application contracts, evidence kernel, data-plane interfaces, engine contracts, and conformance checks.
- Research foundry modules for applications, evidence, adversarial validation, decision runtime, economics, external-factor governance, and general orchestration.
- Feature, training, validation, performance, model-governance, and promotion-boundary modules that communicate architecture rather than implementation edge.
- UI gateway and console read-model contracts that show operator-facing architecture.
- Tests that demonstrate fail-closed boundaries, leakage controls, evidence contracts, and promotion guards.
- Sanitized capability placeholders for research lines, execution/order-management boundaries, vendor/data details, and performance work where the original filename would over-disclose system posture.

## Boundary Controls

- Production source bodies are replaced before publication.
- Runtime configs, task state, queue state, handoffs, run logs, datasets, model artifacts, checkpoints, reports, and generated stores stay outside the review tree.
- Paths whose filenames reveal research lines, setup labels, unpublished strategy names, vendor-specific repair history, or live/broker posture are represented by sanitized capability boundaries instead of retained filenames.
- Local usernames, machine paths, vendor credentials, tokens, and any secret-like material stay outside the review tree.

## Sanitized Capability Rule

When a module is important for proving capability coverage but the original path is too revealing, publish a sanitized placeholder under `redacted_capabilities/`.

The placeholder may describe:

- capability area;
- official Research OS layer when applicable;
- architecture role;
- architecture-level highlights;
- sanitized input/output contract;
- implementation details omitted from the review surface.

It must not preserve exact internal filenames, strategy labels, experiment labels, vendor-specific paths, account/order details, run ids, thresholds, formulas, or implementation logic.

## Placeholder Contract

Each exported source-shaped file must contain only:

- retained module path;
- Research OS architecture layer;
- module responsibility;
- implementation highlights at system-design level;
- sanitized input/output contract;
- explicit note that implementation details are omitted.

The files are architecture review artifacts, not runnable source code.
