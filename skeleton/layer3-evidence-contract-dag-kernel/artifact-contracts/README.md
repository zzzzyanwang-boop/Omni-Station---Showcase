# Artifact Contracts

Artifact contracts define the evidence-facing shape of outputs before physical storage concerns are handled by Layer 1.

Reviewable responsibilities:

- artifact kind, owner, producing application, and consuming gate
- schema version, nullable-field policy, index/grain, and contract fingerprint
- source references for data, feature, model, replay, or review inputs
- row or record counts with sample/full-scope distinction
- content hashes and producer version for stale-artifact detection
- consumer eligibility that blocks use outside the declared evidence path
