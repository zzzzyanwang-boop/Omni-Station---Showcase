# Calibration and OOD

Calibration and OOD engines convert raw scores into reviewable reliability evidence.

Reviewable responsibilities:

- calibration artifact identity linked to model version, fold policy, target definition, and scoring horizon
- reliability, rank stability, drift, and OOD summaries that can be attached to evidence envelopes
- OOD state boundary that can force abstention or block inference eligibility
- parity between native/compiled scoring outputs and reference evaluation outputs where applicable
- blocked inference eligibility when calibration, OOD, or validation evidence is incomplete
