# Data Plane

The data plane owns source identity, schema, point-in-time constraints, and consumer eligibility.

Reviewable responsibilities:

- source manifest boundary for vendor/source identity, schema version, content hash, and ingestion timestamp
- point-in-time validation before a provider or engine can request columns
- projection and sample boundary so diagnostic slices cannot silently become full evidence
- row/partition eligibility checks before native or vectorized execution begins
- source-to-artifact lineage references carried into EvidenceEnvelope and ArtifactManifest records
