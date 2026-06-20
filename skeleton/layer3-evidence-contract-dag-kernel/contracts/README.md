# Contracts

Contracts define the executable shape of a workflow before computation starts.

Typical fields:

- objective, non-goals, route authority, and application owner
- required inputs, source manifests, feature/label scope, and engine eligibility
- invariants for point-in-time data, fold-local selection, artifact identity, and runtime posture
- allowed claims, blocked claims, diagnostic-only claims, and review scope
- failure modes for missing data, stale artifacts, leakage, incomplete replay, and unsupported native paths
- validation plan with OOF/CPCV/replay/risk requirements where applicable
- done criteria that name the required EvidenceEnvelope, ArtifactManifest, and ReviewGate outputs
