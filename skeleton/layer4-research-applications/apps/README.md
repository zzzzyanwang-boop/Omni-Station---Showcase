# Applications

Application owners bind a research route to contracts, engines, and review outputs.

Typical responsibilities:

- accept a WorkOrder only when Layer 5 route authority allows the stage
- resolve the correct research contract and reject unowned routes
- call approved Layer 2 engines with manifest-bound inputs and declared failure modes
- publish ArtifactManifest and EvidenceEnvelope outputs rather than local files
- hand results to Layer 3 gates with explicit admitted, blocked, and diagnostic claims
