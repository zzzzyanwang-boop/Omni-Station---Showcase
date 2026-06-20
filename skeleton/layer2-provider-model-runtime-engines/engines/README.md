# Engines

Engines perform bounded computation under explicit contracts.

Typical responsibilities:

- validate required inputs, schema fingerprints, source manifests, and fold/panel eligibility
- select Python, vectorized, or Rust-native execution only through an explicit engine contract
- execute deterministic materialization, evaluation, replay, calibration, or utility scoring
- avoid hidden fallback behavior; unsupported native paths fail closed instead of silently switching semantics
- report schema, hashes, timing, kernel version, bridge version, and failure reasons
- return outputs through manifests instead of loose files
