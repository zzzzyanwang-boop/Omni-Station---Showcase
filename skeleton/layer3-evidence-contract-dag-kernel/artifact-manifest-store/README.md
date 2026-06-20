# Artifact Manifest Store

The manifest store is the authority for artifact identity and consumer eligibility.

Reviewable responsibilities:

- artifact id, kind, route id, producer, and producing contract
- schema and content hashes used by gates, cache reuse, and native kernel parity checks
- source references for lineage back to data-plane manifests and prior evidence
- row or record counts with partition and sample/full-scope markers
- allowed consumers and blocked consumers with explicit reason codes
- latest-file avoidance: consumers resolve artifacts by manifest identity, not folder scans
