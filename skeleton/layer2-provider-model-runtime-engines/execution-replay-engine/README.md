# Execution Replay Engine

Execution replay evaluates fills, slippage, latency, cost, and capacity assumptions.

Reviewable responsibilities:

- replay input contract with decision timestamps, tradable universe, liquidity/cost assumptions, and abstention states
- fill, slippage, latency, fee, and capacity evidence attached to replay manifests
- closed-trade ledger boundary separated from mark-to-market-only diagnostics
- blocked economic pass when replay evidence is incomplete, stale, or not linked to the reviewed score artifact
- Rust/native replay kernels permitted only behind deterministic parity and cost-model contract checks
