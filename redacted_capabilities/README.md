# Sanitized Capability Boundaries

This directory complements `source/`.

- `source/` retains module paths when the filename is useful for architecture review.
- `redacted_capabilities/` uses neutral capability names when the original filename would over-disclose research direction, execution posture, vendor dependency, account assumption, or unpublished result history.

Each file describes the capability boundary, Research OS layer, architecture-level highlights, and sanitized input/output contract. The intent is to make sensitive surfaces reviewable as system design without exposing implementation details or reproducible research logic.
