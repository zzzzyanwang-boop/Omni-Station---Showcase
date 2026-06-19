# Control Plane

The control plane exists to keep research work bounded, repeatable, and reviewable.

## Responsibilities

- Select a bounded work order.
- Resolve the owning application and engine.
- Enforce required metadata before execution.
- Preserve evidence contracts and artifact manifests.
- Record review outcomes and residual risks.
- Prevent unsupported promotion into live-capable paths.

## Non-Responsibilities

- It does not create trading signals by itself.
- It does not weaken validation to unblock a run.
- It does not treat logs or ad hoc notebooks as decision-grade evidence.
- It does not allow loose artifact discovery to replace manifests.

## Failure Handling

The control plane should fail closed when required inputs are missing, stale, malformed, or outside the declared scope. Partial evidence may be useful for diagnosis, but it is not a promotion signal.

