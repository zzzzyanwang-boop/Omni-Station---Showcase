# Capability Rationale

This document explains the engineering thinking behind the showcase. It is written for a technical reviewer who wants to understand why the system is shaped this way, not only what files exist.

## Capability Themes

| Capability | Problem Being Solved | Design Response | Review Evidence |
| --- | --- | --- | --- |
| Research control plane | Research can drift into ad hoc scripts, repeated trials, or unsupported claims | WorkOrders, route charters, allowed next action, route authority, and review gates own the lifecycle | `docs/architecture/five-layer-architecture.md`, `skeleton/layer5-research-governance-operations/` |
| Application ownership | Low-level stations can become accidental product surfaces | Layer 4 applications own workflow shape; stations are lower-level tools called through contracts | `docs/architecture/research-application-catalog.md` |
| Evidence kernel | Reports and metrics can be mistaken for truth | ResearchContract, EvidenceDAG, EvidenceEnvelope, ArtifactManifest, TrialBudget, and GateEngine separate computation from claim admission | `docs/architecture/evidence-kernel-contracts.md` |
| Data lineage | Source scope, timestamp availability, and revisions can become ambiguous | Manifests, source refs, schema/content hashes, claim limits, and point-in-time policies are carried through artifacts | `docs/architecture/data-lineage.md` |
| Label governance | Labels are high-leakage and high-blast-radius artifacts | Label ownership sits behind Label/Outcome contracts; source-backed label views avoid unnecessary dense label writes | `docs/flows/source-label-stage1-oof-flow.md`, `pseudocode/source_backed_label_view.md` |
| Trainable matrix construction | Factor and label joins can become memory-heavy and hard to audit | Stage1 join contracts record label reader mode, join policy, prepared-date cache, streaming writes, and reject evidence | `pseudocode/stage1_trainable_join.md` |
| ML validation | Models can overfit through fold leakage, stale inputs, or narrow-scope artifacts | OOF specs bind trainable manifests, source boundaries, fold policy, model policy, and runtime posture | `examples/toy_oof_run_spec.json`, `pseudocode/oof_rebinding_gate.md` |
| Sequence model stability | Variable-length sequence batches can hide padding, dropping, or non-finite failures | Fixed-shape descriptor-run planning and native tensor bridge metadata make shape and numeric failures explicit | `pseudocode/sequence_oof_batch_planner.md`, `examples/toy_sequence_batch_plan.json` |
| Physical performance | Wrappers can add governance without removing real computation | Performance work names scans, projections, materialization, cache identity, native kernels, bridge overhead, and parity gates | `docs/flows/performance-optimization-playbook.md` |
| Runtime separation | Offline evidence can be confused with action eligibility | Runtime posture, action-intent contracts, promotion freeze, and order-management boundaries are separated from research evidence | `redacted_capabilities/runtime_engine_boundary/` |

## Design Pattern: Problem -> Contract -> Evidence -> Gate

The system uses the same pattern across research areas:

```text
problem statement
  -> explicit owner
  -> typed contract
  -> bounded engine call
  -> manifest-bound artifact
  -> evidence envelope
  -> gate decision
  -> memory or closure state
```

This pattern is intentionally repetitive. The repetition is a control: a reviewer can inspect the same ownership, lineage, failure, and permission shape across source data, features, labels, models, replay, and runtime boundaries.

## What This Demonstrates

- ability to turn vague research ideas into typed, reviewable workflows
- understanding that quantitative research quality is a data, validation, evidence, and governance problem, not only a modeling problem
- ability to design fail-closed systems where unsupported claims do not move downstream
- performance thinking grounded in physical execution rather than only orchestration wrappers
- Rust/native integration as a controlled engine boundary with parity and metadata, not as a side-channel
- productization discipline: UI/read models expose state without becoming truth sources

## What Is Deliberately Omitted

- formulas, strategy rules, raw data, feature values, labels, scores, model weights, replay rows, exact thresholds, local configuration, and runtime material
- original names where a filename would reveal a research direction or execution posture beyond architecture review needs
- benchmark numbers or result metrics that would imply a production research conclusion

