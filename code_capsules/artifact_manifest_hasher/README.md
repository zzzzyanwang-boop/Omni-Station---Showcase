# Artifact Manifest Hasher

This capsule demonstrates public-safe manifest discipline for research artifacts.

What it shows:

- schema, content, and lineage hashes are canonical and deterministic;
- stale artifact references fail closed instead of being treated as latest-file lookups;
- diagnostic artifacts cannot support decision-grade claims;
- claim support is validated by explicit artifact ids and expected hashes.

Run:

```powershell
python -m unittest discover code_capsules/artifact_manifest_hasher -p "test_*.py"
```

