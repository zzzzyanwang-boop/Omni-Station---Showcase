# Artifact Storage

Artifact storage owns physical storage locations and atomic publication.

Reviewable responsibilities:

- storage-location ownership tied to a compiled contract and route authority
- atomic writer semantics for temporary output, fsync/commit, and publish visibility
- manifest publication boundary with schema hash, content hash, row count, and producer version
- stale and partial output rejection before evidence gates can consume results
- compatibility with Python orchestration and Rust-native writers without loose latest-file lookup
