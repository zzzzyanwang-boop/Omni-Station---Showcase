# Data Lineage

OmniStation treats data lineage as part of the research result. A metric without a source contract, schema, and evidence path is not decision-grade.

## Lineage Concepts

- Source identity: where the input came from and what contract it satisfies.
- Point-in-time boundary: whether the input is valid at the decision timestamp.
- Projection boundary: which columns and rows were materialized.
- Hash boundary: content or manifest hashes used to detect drift.
- Sample boundary: whether evidence is sample, bounded certification, or full-scope.
- Consumer boundary: which downstream gate is allowed to consume the artifact.
- Source-boundary compatibility: whether downstream labels, trainable matrices, and OOF specs share the same declared source scope.
- Revision boundary: whether an artifact supersedes or invalidates prior evidence.
- Cache boundary: whether reused work is manifest-bound or merely local convenience.

## Lineage Chain

```text
LandingManifest
  -> NormalizedDatasetManifest
  -> SourceBoundaryPacket
  -> LabelViewManifest or FeatureManifest
  -> TrainableManifest
  -> OOFManifest or ReplayManifest
  -> EvidenceEnvelope
  -> GateResult
```

## Required Review Fields

| Field | Why It Matters |
| --- | --- |
| `source_refs` | proves which inputs were used |
| `schema_hash` | detects schema drift |
| `content_hash` | detects content drift |
| `available_ts_policy` | prevents future-data leakage |
| `claim_limits` | prevents scope overclaiming |
| `consumer_permissions` | prevents downstream misuse |
| `revision_id` | supports invalidation and reproducibility |
| `materialization_policy` | distinguishes dense artifacts from logical/source-backed views |

## Synthetic Example

`examples/toy_evidence_manifest.json` shows the shape of an evidence manifest without including real data paths or real hashes.
