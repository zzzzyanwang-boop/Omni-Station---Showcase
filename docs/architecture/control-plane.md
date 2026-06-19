# Control Plane

The control plane exists to keep research work bounded, repeatable, and reviewable.

## Responsibilities

- Select a bounded work order.
- Resolve the owning application and engine.
- Enforce required metadata before execution.
- Preserve evidence contracts and artifact manifests.
- Record review outcomes and residual risks.
- Prevent unsupported promotion into live-capable paths.

## Failure Handling

The control plane should fail closed when required inputs are missing, stale, malformed, or outside the declared scope. Partial evidence may be useful for diagnosis, but it is not a promotion signal.
