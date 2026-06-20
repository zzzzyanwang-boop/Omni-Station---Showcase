# Model Zoo

Model Zoo owns reusable model-family execution behind application and evidence contracts.

Reviewable responsibilities:

- model candidate registration with family, feature schema, training window, fold policy, and artifact identity
- training and evaluation request shape separated from application route ownership
- OOF artifact binding with prediction store, calibration input, and leakage/fold-local evidence
- challenger/default eligibility signals that remain review-gated rather than metric-only
- native or compiled-model paths represented through explicit engine bridge contracts and parity checks
