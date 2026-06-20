# Layer 2 - Provider / Model / Runtime Engines

Layer 2 provides reusable capability services behind Research OS contracts. These engines compute, evaluate, replay, calibrate, and project results, but they do not own the top-level research route.

Review focus:

- feature and external-factor providers
- ModelZoo and calibration/OOD engines
- decision runtime and score resolution
- execution replay and portfolio engines
- Rust/PyO3 bridge contracts for native engine calls
- runtime mode and inference eligibility boundaries

Representative nodes:

- `feature-providers/`
- `model-zoo/`
- `calibration-ood/`
- `decision-runtime/`
- `execution-replay-engine/`
- `portfolio-engine/`
- `engines/`
- `rust-engine-bridges/`
- `inference/`
- `runtime/`
