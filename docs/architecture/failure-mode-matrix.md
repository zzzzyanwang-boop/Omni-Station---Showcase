# Failure Mode Matrix

This matrix shows how the architecture handles predictable failure classes. It is meant to demonstrate fail-closed reasoning, not production incident history.

| Failure Class | Example Risk | Detection Surface | Blocker / Response | Reviewable Files |
| --- | --- | --- | --- | --- |
| Missing WorkOrder authority | A runner is executed without route ownership | Layer 5 route authority and allowed-next-action state | mark diagnostic-only or block | `skeleton/layer5-research-governance-operations/work-orders/README.md` |
| Missing ResearchContract | An application tries to compute before policy refs exist | Contract compiler and app contract validation | block decision-grade execution | `docs/architecture/evidence-kernel-contracts.md` |
| Loose artifact lookup | A workflow reads a latest file instead of a manifest | Artifact truth resolver and manifest store | block consumer permission | `docs/architecture/layer-contracts.md` |
| Source scope mismatch | A narrow or stale source packet claims wider coverage | source-boundary gate | block OOF or confirmation readiness | `source/omni_station/research/data/full_market_source_contract.py` |
| Point-in-time ambiguity | feature availability is unclear at decision timestamp | data lineage and time policy proof | block feature or label consumption | `docs/architecture/data-lineage.md` |
| Label leakage | target fields or future data enter feature matrix | Type/effect registry and leakage gate | quarantine artifact and block model input | `docs/architecture/validation-gates.md` |
| Trial-budget overuse | repeated discovery is reused as confirmatory evidence | TrialBudgetLedger and discovery seal | downgrade to diagnostic or block confirmation | `docs/architecture/evidence-kernel-contracts.md` |
| OOF scope overclaim | OOF spec uses a stale or narrow trainable matrix | OOF rebinding gate | block OOF launch or broader validation | `pseudocode/oof_rebinding_gate.md` |
| Sequence shape drift | variable batches require padding or silent row dropping | sequence batch planner and tensor diagnostics | block sequence OOF path | `pseudocode/sequence_oof_batch_planner.md` |
| Non-finite training signal | loss, logits, or tensors contain invalid values | numeric diagnostics attached to evidence | block or mark diagnostic with reason code | `source/omni_station/research_os/model_training/model_branch_oof_full_executor.py` |
| Native bridge mismatch | Python wrapper imports unsupported kernel version | engine contract and native metadata | block native path, do not silently fall back | `source/rust/omni_sequence_tensor_kernel_py/src/lib.rs` |
| Cache identity drift | prepared cache no longer matches source or policy | cache manifest and content/schema refs | rebuild through contract or block reuse | `redacted_capabilities/native_compute_infrastructure/cache_checkpoint_telemetry.py` |
| Replay accounting mismatch | mark-to-market is confused with realized round-trip accounting | economic accounting and replay gates | block economic claim | `docs/flows/risk-replay-promotion-flow.md` |
| Runtime boundary violation | offline evidence is treated as live-capable authority | runtime posture and promotion gates | block runtime consumer | `redacted_capabilities/runtime_engine_boundary/runtime_mode_token_contract.py` |
| UI truth leakage | dashboard infers status from partial files or stale logs | read-model contract and evidence envelopes | show blocker state, do not infer pass | `source/web/omni-console/src/components/pages/ui039-proof-graph-ops-console.tsx` |

## Fail-Closed Posture

The common response is not a broad fallback. The system prefers:

- explicit blocker code
- evidence-tier downgrade when appropriate
- quarantine for unsafe inputs
- manifest-bound rebuild for stale artifacts
- consumer-specific permission denial
- closure or memory entry that records the limitation

This makes failures reviewable and prevents a useful diagnostic artifact from silently becoming a research conclusion.

