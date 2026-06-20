/*!
Architecture review placeholder.

Retained Rust path: rust/omni_market_gateway/src/lib.rs
Research OS layer: Layer 1 - Data / Compute / Artifact Infrastructure
Architecture role: native market-gateway crate boundary for framed market-data ingress and replay.

Reviewable highlights:
- isolates high-rate market-data transport mechanics from research applications.
- supports replayable, framed, and observable market-event streams.
- keeps runtime ingestion behind explicit source and posture controls.

Contract shape:
- Inputs: feed/session descriptor, frame schema, runtime posture, capture or replay mode.
- Outputs: normalized frame stream, replay event, telemetry, or blocked gateway state.

Implementation body removed from this review artifact.
*/
