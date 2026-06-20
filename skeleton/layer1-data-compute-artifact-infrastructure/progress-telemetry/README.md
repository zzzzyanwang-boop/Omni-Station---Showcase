# Progress Telemetry

Progress telemetry makes long-running materialization and evaluation inspectable.

Reviewable responsibilities:

- stage timing for scan, materialization, native kernel, bridge, write, and gate phases
- checkpoint state with resumable partition, completed row group, and artifact publication status
- row or partition progress for long-running factor, replay, and validation jobs
- failure and blocker visibility with explicit operator-visible next action
- kernel-level counters that can be attached to EvidenceEnvelope or ArtifactManifest metadata
