# Security and Disclosure Policy

This public repository is intentionally limited to architecture documentation, source-shaped placeholder files, redacted capability placeholders, diagrams, pseudocode, and synthetic examples.

## Out of Scope for Public Disclosure

- Production source bodies or private implementation logic
- Real sensitive filenames when those filenames reveal research direction, strategy posture, vendor details, execution posture, or unpublished results
- Credentials, tokens, certificates, or account identifiers
- Broker, exchange, OMS, or live execution configuration
- Real market data, vendor data, logs, checkpoints, model weights, or research artifacts
- Strategy logic, factor formulas, alpha claims, or position-sizing rules
- Internal hostnames, local paths, queue roots, usernames, or machine-specific runbooks

## Reporting Concerns

If a commit appears to contain private implementation details, credentials, live configuration, or real research data, treat it as a disclosure issue. The correct response is to remove the content, rotate any affected secret if applicable, and rebuild the public repository from a clean export.

## Publishing Rule

The private repository must never be forked or made public. Public material should be generated through a whitelist export process into a new repository with clean git history.
