# Performance Optimization Playbook

This playbook explains how performance work is represented in the showcase. It focuses on physical execution rather than broad claims.

## Optimization Sequence

```text
define contract and correctness oracle
  -> profile physical plan
  -> identify dominant scan, join, materialization, copy, or kernel cost
  -> remove avoidable work
  -> fuse or stream remaining work
  -> introduce manifest-bound cache only where reused work is proven
  -> move hot loops to vectorized or native boundary when justified
  -> run parity or equivalence gate
  -> publish performance evidence and remaining bottleneck
```

## Physical Work Categories

| Category | Review Question | Example Control |
| --- | --- | --- |
| source scans | how many times is the same source read? | source-backed views and partition/date planning |
| projection width | are unused columns read or copied? | column projection before scan |
| row materialization | are dense rows written when a logical view is enough? | source-backed formula view |
| joins | is the join date/partition-aware? | prepared date label cache and streaming join |
| memory | is a full table collected in process memory? | streaming sink and bounded partitions |
| cache identity | is reused work content-bound? | cache manifest with source and policy refs |
| native bridge | does native work remove a real hot loop? | PyO3 kernel selected through engine contract |
| parity | does fast path preserve semantics? | old/new equivalence or reference check |
| telemetry | can the remaining bottleneck be seen? | stage timing and engine run record |

## Source-Backed Label Optimization

Problem:

Dense label tables can add write amplification and repeated scans when the downstream consumer only needs a formula-bound view over source parts.

Design response:

- keep source manifests and formula metadata as the truth
- defer dense row materialization unless a contract requires it
- bind horizon, cost dimension, source refs, and materialization policy in the manifest
- force downstream readers through the label view API

Review signal:

- fewer dense writes
- clearer label ownership
- stronger source-boundary compatibility
- no direct label-part globbing

## Stage1 Trainable Optimization

Problem:

Joining labels and factor rows can become expensive and hard to audit if each factor part rebuilds the same label-side work or collects a full joined table.

Design response:

- resolve source-backed label records by date
- prepare label-side cache only when reused
- stream matched rows to columnar output
- summarize rejects through compact ledgers
- bind join policy, label reader mode, and cache events to the trainable manifest

Review signal:

- reduced repeated label preparation
- bounded memory footprint
- explicit reject evidence
- manifest-bound trainable output

## Sequence OOF Optimization

Problem:

Sequence model OOF can fail or become misleading when descriptor batches have inconsistent shapes, hidden padding, or non-finite tensor values.

Design response:

- coalesce descriptor runs into fixed-shape batches
- block incomplete batches instead of padding or silently dropping
- move tensor packing and batch assembly into a native kernel boundary
- attach shape and numeric diagnostics to OOF evidence

Review signal:

- stable batch semantics
- explicit failure conditions
- native bridge metadata
- no exception-based fallback into a different training shape

