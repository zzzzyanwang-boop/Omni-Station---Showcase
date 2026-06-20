# Security and Disclosure Policy

This repository is scoped to architecture documentation, source-shaped placeholder files, sanitized capability placeholders, diagrams, pseudocode, and synthetic contract fixtures.

## Disclosure Boundary

- Implementation bodies and production logic stay outside the repository.
- Original filenames are sanitized when they would over-disclose research direction, strategy posture, vendor detail, execution posture, or unpublished result history.
- Credentials, tokens, certificates, account identifiers, broker configuration, exchange configuration, OMS configuration, and live-execution configuration stay outside the repository.
- Market data, vendor data, logs, checkpoints, model weights, generated artifacts, and research outputs stay outside the repository.
- Strategy logic, factor formulas, alpha claims, position-sizing rules, local paths, queue roots, usernames, and machine-specific runbooks stay outside the repository.

## Reporting Concerns

Treat any accidental commit of implementation logic, credentials, live configuration, runtime output, or research data as a disclosure issue. The response is to remove the content, rotate affected secrets where applicable, and rebuild the architecture export from a clean source.

## Publishing Rule

Publish only the generated architecture export. Do not publish the working repository or its git history.
