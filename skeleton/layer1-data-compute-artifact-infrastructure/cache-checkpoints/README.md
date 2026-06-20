# Cache and Checkpoints

Cache and checkpoints make repeated research execution resumable without weakening evidence identity.

Reviewable responsibilities:

- cache key semantics that include contract id, source hash, schema hash, engine version, and parameter fingerprint
- checkpoint resume safety for partitioned materialization and long replay runs
- content-addressed reuse only when the manifest and kernel version still match
- stale cache rejection when data, contract, code boundary, or native kernel identity changes
- recovery metadata that distinguishes restartable work from evidence-invalid work
