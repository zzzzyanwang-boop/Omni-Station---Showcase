/*!
Architecture review placeholder.

Retained Rust path: rust/omni_market_gateway/src/frame.rs
Research OS layer: Layer 1 - Data / Compute / Artifact Infrastructure
Architecture role: frame parsing and validation boundary for native market-data ingress.

Reviewable highlights:
- makes packet/frame identity, schema, and validation explicit.
- rejects malformed or unsupported frames before they reach downstream consumers.
- supports deterministic replay and fixture validation for gateway behavior.

Contract shape:
- Inputs: raw frame bytes or synthetic frame fixture, schema/version descriptor.
- Outputs: validated frame, normalized event fields, or explicit parse rejection.

Implementation body removed from this review artifact.
*/
