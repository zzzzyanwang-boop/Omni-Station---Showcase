# Source-Label and Stage1 Trainable

This node shows the application boundary for turning source-bound market data into label views and Stage1 trainable matrices without publishing formulas, row-level labels, or research results.

Reviewable responsibilities:

- bind source-boundary certificates, universe scope, horizon, timestamp semantics, and cost assumptions before labels can feed downstream training
- represent labels as source-backed formula views when dense row-level materialization is avoidable
- resolve label records by source part and date before joining against factor artifacts
- build prepared date label caches for repeated joins without changing the evidence scope
- stream matched trainable rows to columnar output and record compact reject ledgers for unmatched or invalid rows
- fail closed when a narrow, stale, or source-incompatible artifact attempts to claim full-scope authority
