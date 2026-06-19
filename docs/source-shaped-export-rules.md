# Source-Shaped Export Rules

The showcase export is whitelist-based. It preserves a public-safe subset of the real source tree while replacing implementation bodies with descriptive placeholders.

## Included

- Research OS contracts, data-plane interfaces, semantic kernel, engine contracts, and conformance checks.
- Research foundry modules for evidence, adversarial validation, decision runtime, economics, external-factor governance, and general orchestration.
- Feature, training, validation, performance, model-governance, and promotion-boundary modules that communicate architecture rather than private edge details.
- UI gateway and console read-model contracts that show operator-facing architecture.
- Tests that demonstrate fail-closed boundaries, leakage controls, evidence contracts, and promotion guards.

## Excluded

- Production source bodies.
- Real configs, tasks, queue state, handoffs, run logs, datasets, model artifacts, checkpoints, reports, and generated stores.
- Paths whose filenames reveal sensitive research lines, private setup labels, unpublished strategy names, vendor-specific run repair, or live/broker posture details beyond boundary guards.
- Local usernames, machine paths, vendor credentials, tokens, and any secret-like material.

## Placeholder Contract

Each exported source-shaped file must contain only:

- original public-safe path,
- architecture layer,
- module responsibility,
- public-safe implementation highlights,
- sanitized input/output contract,
- explicit list of removed private material.

The files are documentation artifacts, not runnable source code.
