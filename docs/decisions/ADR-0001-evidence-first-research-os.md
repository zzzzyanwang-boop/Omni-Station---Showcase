# ADR-0001: Evidence-First Research OS

## Status

Accepted for the private system architecture.

## Context

Quantitative research workflows can drift into ad hoc scripts, loose reports, and fragile latest-file conventions. That makes results hard to reproduce and easy to overclaim.

## Decision

Research execution is organized around explicit work orders, contracts, evidence DAGs, artifact manifests, and review gates.

## Consequences

- More upfront metadata is required.
- Intermediate artifacts need schema and provenance.
- Claims can be blocked even when a diagnostic metric looks attractive.
- Reviewers can audit what was proven, what was not proven, and which downstream paths remain closed.

