# Data and Panel Contract

Data and panel contracts define the sample, universe, timestamps, and source requirements before feature or model work.

Reviewable responsibilities:

- panel identity by universe, timestamp grain, horizon, tradability rules, and inclusion/exclusion policy
- point-in-time constraints for source availability, release lag, survivorship, and corporate-action assumptions
- source quality requirements for completeness, schema stability, quarantine, and vendor/source provenance
- sample versus full-scope distinction so diagnostics cannot masquerade as final evidence
- consumer eligibility for feature providers, label oracles, model training, replay, and review gates
