# Feature Providers

Feature providers serve contract-bound features, factors, and state representations.

Reviewable responsibilities:

- required input validation against the Data / Panel Contract and fold policy
- fold-local feature availability so future data cannot enter train or validation folds
- source and schema binding carried from Layer 1 manifests into provider outputs
- provider output manifest references for feature matrix, factor exposure, state tensor, or diagnostic sample artifacts
- optional Rust/vectorized materialization calls only when parity-certified and recorded in the artifact manifest
