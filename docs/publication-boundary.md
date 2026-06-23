# Architecture Review Boundary

The repository is generated as a curated architecture export. It is not produced by filtering a working repository after the fact.

## Review Artifacts

- Architecture summaries.
- Diagrams with sanitized names.
- Source-shaped placeholder files that retain architecture-relevant module paths while replacing implementation bodies with summaries.
- Sanitized capability placeholders where original filenames would over-disclose research or runtime posture.
- Synthetic contract fixtures with toy identifiers and placeholder hashes.
- General engineering decision records.

## Boundary Controls

- No production source bodies.
- No runtime configuration, task state, handoff state, run logs, or queue state.
- No data artifacts, model output, feature matrices, labels, OOF predictions, or replay reports.
- No local filesystem paths, usernames, or local runtime directories.
- No strategy detail that would make research logic reproducible.
- No original filename when the filename itself reveals research direction, execution posture, vendor detail, or unpublished result history.

## Release Checklist

1. Build a new export directory from architecture templates and an allowlist of retained source paths.
2. Replace implementation bodies with placeholders before any publication step.
3. Scan for local paths, secrets, artifact extensions, implementation tokens, and environment-specific identifiers.
4. Initialize a new git repository in the export directory only.
5. Publish the export repository, never the working repository or its history.
6. Re-scan the published repository after publication.
