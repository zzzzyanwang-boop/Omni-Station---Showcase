# Pseudocode: Manifest Store

```text
function publish_artifact(artifact):
    schema_hash = hash_schema(artifact.schema)
    content_hash = hash_content(artifact.content)

    manifest = {
        artifact_id,
        artifact_kind,
        schema_version,
        row_count,
        schema_hash,
        content_hash,
        source_refs,
        claim_limits
    }

    write_manifest_atomically(manifest)
    return manifest

function resolve_artifact(manifest_ref, expected_kind, expected_schema):
    manifest = read_manifest(manifest_ref)
    assert manifest.artifact_kind == expected_kind
    assert manifest.schema_hash == expected_schema
    assert content_hash_matches(manifest)
    return manifest
```
