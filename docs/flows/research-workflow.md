# Research Workflow

This flow shows how a research question becomes a reviewable evidence packet.

```text
1. Draft work order
2. Attach owner, scope, non-goals, and acceptance signal
3. Build research contract
4. Build evidence DAG
5. Resolve manifest-bound input bundle
6. Run bounded research engines
7. Publish output manifests and evidence envelopes
8. Run validation and governance gates
9. Emit review gate result
10. Emit closure case or blocked decision
```

## Key Design Point

The architecture does not treat a successful computation as a successful research claim. A claim is admitted only when the gate result explicitly admits it.

