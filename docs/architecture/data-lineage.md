# Data Lineage

The private system treats data lineage as part of the research result. A metric without a source contract, schema, and evidence path is not decision-grade.

## Lineage Concepts

- Source identity: where the input came from and what contract it satisfies.
- Point-in-time boundary: whether the input is valid at the decision timestamp.
- Projection boundary: which columns and rows were materialized.
- Hash boundary: content or manifest hashes used to detect drift.
- Sample boundary: whether evidence is sample, bounded certification, or full-scope.
- Consumer boundary: which downstream gate is allowed to consume the artifact.
