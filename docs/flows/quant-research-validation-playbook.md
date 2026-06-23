# Quant Research Validation Playbook

This playbook describes the reasoning discipline behind the validation surfaces in the showcase.

## Validation Sequence

```text
hypothesis
  -> source and panel contract
  -> feature/factor or model plan
  -> label/outcome plan
  -> discovery-only evidence
  -> trial-budget accounting
  -> freeze packet
  -> OOF or confirmatory validation
  -> robustness and calibration checks
  -> replay and economic evidence
  -> portfolio utility
  -> closure case
```

## Core Research Risks and Controls

| Risk | Why It Matters | Control |
| --- | --- | --- |
| future-data leakage | invalidates apparent predictiveness | point-in-time source policy and leakage gate |
| sample overclaiming | makes a small or narrow result look general | source-boundary and claim-limit gates |
| repeated search | inflates false discovery risk | TrialBudgetLedger and discovery/confirmation split |
| fold contamination | creates optimistic OOF or CPCV evidence | fold-local selection and embargo policy |
| stale labels or trainables | breaks model evidence lineage | OOF rebinding gate and manifest compatibility |
| model instability | makes score evidence unreliable | calibration, OOD, uncertainty, and branch eligibility checks |
| metric-only claims | confuses computation with validity | gate engine separates metric packet from admitted claim |
| replay mismatch | makes economic evidence non-comparable | execution replay and accounting contracts |
| runtime drift | allows offline evidence to be overused | runtime posture and promotion boundary |

## OOF Reasoning

OOF evidence is useful only when it is bound to the same contract scope as the training data:

- same source-boundary compatibility
- same panel and sample/full-scope policy
- declared fold and embargo policy
- declared label reader mode
- declared model policy
- no stale or narrow trainable manifest
- no hidden sequence-shape repair
- numeric diagnostics attached to evidence

The OOF gate therefore evaluates whether the evidence can be consumed, not only whether a training job completed.

## CPCV and Robustness Reasoning

CPCV and robustness checks are downstream of valid OOF evidence. They should not be used to repair missing OOF lineage. The consumer must know:

- which folds and purging/embargo rules were used
- which trial-budget policy applies
- whether feature selection was fold-local
- whether source and label scopes match the claim
- whether results are confirmatory or diagnostic

## Economic Evidence Reasoning

Replay and economic evidence are separate from statistical evidence. The system keeps:

- signal score
- decision score
- action intent readiness
- replay path
- realized round-trip accounting
- mark-to-market diagnostics
- cost and capacity assumptions
- portfolio utility

separate so a strong model metric cannot become an economic or runtime conclusion without the required evidence.

