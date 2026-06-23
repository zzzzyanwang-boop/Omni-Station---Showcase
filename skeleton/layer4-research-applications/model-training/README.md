# Model Training

Model training is governed by contracts and evidence artifacts.

Reviewable responsibilities:

- model-family specification
- training-run contract
- fold policy and sample scope
- OOF prediction manifest
- formal OOF run-spec rebinding to the active source boundary
- coalesced fixed-shape sequence batches for sequence-model OOF stability
- calibration artifact
- model registry candidate
- inference eligibility gate

Review surface:

- model code, weights, training rows, and metric values are represented through model-family contracts, artifact manifests, calibration records, and gate outcomes

