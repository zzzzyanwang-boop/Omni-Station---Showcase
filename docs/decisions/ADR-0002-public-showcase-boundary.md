# ADR-0002: Public Showcase Boundary

## Status

Accepted for this public repository.

## Context

The private OmniStation repository contains production implementation details, research artifacts, and operational context that are not appropriate for publication.

## Decision

The public repository is generated as a clean, documentation-only export. It contains architecture summaries, diagrams, skeleton directories, and synthetic examples.

## Consequences

- The public repository is useful for architecture review but not runnable.
- No private git history is exposed.
- Public examples use toy identifiers and fake hashes.
- Any future public update must be rebuilt through the same whitelist boundary.

