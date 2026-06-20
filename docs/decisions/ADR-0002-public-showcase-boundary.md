# ADR-0002: Architecture Review Boundary

## Status

Accepted for this architecture review repository.

## Context

OmniStation needs a review surface that communicates architecture, evidence discipline, validation posture, and operational boundaries without depending on implementation access.

## Decision

The repository is generated as a clean, documentation-only architecture export. It contains architecture summaries, diagrams, source-shaped module placeholders, sanitized capability boundaries, and synthetic contract fixtures.

## Consequences

- The repository is useful for architecture review but not runnable.
- The working repository history is not part of the review surface.
- Synthetic examples use neutral identifiers and placeholder hashes.
- Future updates must be rebuilt through the same curated export boundary.
