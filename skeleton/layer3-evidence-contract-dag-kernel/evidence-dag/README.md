# Evidence DAG

The Evidence DAG records dependency structure between inputs, computations, artifacts, gates, and claims.

Reviewable responsibilities:

- node identity for work orders, contracts, sources, engines, artifacts, gates, waivers, and closure cases
- dependency ordering from source manifests through providers, engines, artifacts, and claims
- stale artifact detection when any upstream schema, content, kernel, fold, or contract fingerprint changes
- no-bypass proof that downstream consumers cannot cite diagnostics as confirmatory evidence
- explicit blocked edges for missing lineage, unsupported claims, failed leakage checks, or incomplete replay
