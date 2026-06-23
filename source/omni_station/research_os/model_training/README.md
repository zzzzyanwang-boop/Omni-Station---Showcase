# Model Training and OOF Status Cards

This subtree represents OOF, sequence tensor, and model-training governance surfaces.

## Key Files

| File | Current status represented in the showcase |
| --- | --- |
| `contracts.py` | contract surface for model-training and OOF evidence semantics |
| `model_branch_oof_full_executor.py` | full-manifest OOF engine boundary for tree and sequence challengers |
| `sequence_tensor_native_kernel.py` | Python contract wrapper around the Rust/PyO3 sequence tensor kernel |
| `sequence_tensor_store_governance.py` | sequence tensor store governance and artifact eligibility boundary |
| `research_governance.py` | model research governance and promotion-readiness surface |

## Current System Shape

```text
OOF run spec
  -> trainable partitions and fold policy
  -> tree and sequence candidate execution
  -> score-bus partitions
  -> model cards and candidate states
  -> execution profile and EvidenceEnvelope
```

The executor is not a standalone entrypoint. It is meaningful only when upstream run-spec and source-boundary gates pass. If a required branch blocks, the score bus cannot be presented as full formal evidence.

## Sequence Path

The sequence path tracks sample policy, dataloader policy, descriptor-run batching, native batch-kernel mode, shape stability, and non-finite diagnostics. This is the reviewable state that shows the system treats sequence-model OOF as a governed evidence problem, not only a training loop.
