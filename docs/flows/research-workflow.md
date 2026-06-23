# Research Workflow

This flow shows how a research question becomes a reviewable evidence packet and, later, a closure-ready case. It follows the Research OS design baseline: governance starts the route, applications execute the workflow, the evidence kernel enforces contracts, engines compute bounded artifacts, and infrastructure publishes manifests.

```text
1. Draft ResearchWorkOrder
2. Attach owner, scope, non-goals, and acceptance signal
3. Build ResearchRouteCharter
4. Select Layer 4 Research Application
5. Compile ResearchContract and policy refs
6. Compile EvidenceDAG
7. Resolve manifest-bound input bundle
8. Run bounded Layer 2 engines
9. Publish Layer 1 output manifests
10. Wrap outputs in EvidenceEnvelope
11. Run validation and governance gates
12. Emit ReviewGate result
13. Build closure case or blocked/deferred decision
14. Store ResearchMemory entry
```

## Stage Map

| Stage | Primary Layer | Reviewable Output | Blocking Example |
| --- | --- | --- | --- |
| Idea intake | Layer 5 | work order, owner, question, non-goals | no owner or unsupported route |
| Mechanism framing | Layer 4 | falsifiable hypothesis and mechanism memo | vague claim or missing adversarial test |
| Route charter | Layer 5 / Layer 3 | route scope, allowed consumers, trial budget policy | missing closure or statistical policy |
| Data/panel contract | Layer 4 / Layer 1 | source, panel, timestamp, and sample/full-scope contract | point-in-time or sample-scope mismatch |
| Feature/factor/state plan | Layer 4 / Layer 2 | feature/factor plan, provider contract, dependency map | label leakage or missing source refs |
| Label/outcome plan | Layer 4 / Layer 2 | label contract or source-backed label view manifest | formula or horizon not contract-bound |
| Discovery factory | Layer 4 / Layer 3 | discovery packet and trial ledger update | trial budget exceeded |
| Review/freeze | Layer 5 / Layer 3 | freeze packet and immutable review inputs | unfrozen or mutable artifacts |
| Confirmation/statistical validation | Layer 4 / Layer 3 | confirmatory packet, fold policy, OOF/CPCV evidence | stale, narrow, or diagnostic-only input |
| Decision/economic/replay | Layer 2 / Layer 4 | decision-score packet, replay packet, utility packet | runtime boundary or accounting mismatch |
| Closure/memory | Layer 5 | closure case and memory entry | unsupported claim or incomplete evidence chain |

## Key Design Point

The architecture does not treat a successful computation as a successful research claim. A claim is admitted only when the gate result explicitly admits it.

## No-Bypass Rule

No low-level runner, notebook, metric report, model score, replay output, or native kernel result can become decision-grade by itself. The output must be bound to a `ResearchContract`, appear in an `EvidenceDAG`, publish an `ArtifactManifest`, be wrapped by an `EvidenceEnvelope`, and pass the relevant gate for the specific downstream consumer.
