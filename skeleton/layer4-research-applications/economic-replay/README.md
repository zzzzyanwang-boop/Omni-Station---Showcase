# Economic Replay

Economic replay converts model or signal evidence into cost, capacity, fill, and portfolio utility evidence.

Reviewable responsibilities:

- replay scenario ownership by route, score artifact, tradable universe, timestamp grain, and action-intent contract
- cost and capacity model requirements for fees, slippage, latency, participation, liquidity, and turnover
- execution assumption boundary separated from order-management or broker side effects
- replay evidence handoff to Layer 3 gates through closed-trade ledger, fill/cost summaries, and blocked economic claims
- deterministic replay or native replay kernels accepted only when source, clock, and parity contracts are satisfied
