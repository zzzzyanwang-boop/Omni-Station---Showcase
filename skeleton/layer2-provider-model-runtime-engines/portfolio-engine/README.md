# Portfolio Engine

Portfolio engines evaluate allocation, concentration, risk, and utility under bounded assumptions.

Reviewable responsibilities:

- portfolio intent contract with universe, exposure, leverage, turnover, capacity, and exclusion constraints
- utility and risk summaries linked to replay, cost, and model uncertainty evidence
- concentration and capacity checks that can block promotion even when raw signal metrics pass
- handoff to Layer 3 review gates through manifests, not notebook tables or runtime memory
- native aggregation paths allowed only when they preserve deterministic accounting and explainable attribution
