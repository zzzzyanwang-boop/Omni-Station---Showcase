"""
Architecture review placeholder.

Retained module path: omni_station/research_os/model_training/model_branch_oof_full_executor.py
Original source content is intentionally omitted.

Architecture layer: Layer 2 - Provider / Model / Runtime Engines
Architecture role: full-manifest model-branch OOF executor for tree and sequence challengers.

Current public-review status:
- engine boundary for full-manifest OOF score-bus generation.
- executes only after a formal OOF run spec passes upstream gates; it is not an independent research entrypoint.
- supports tree-family and sequence-family candidate paths, with separate cache, resume, heartbeat, profile, score-bus, and model-card outputs.
- sequence path tracks sample policy, dataloader policy, fixed-shape descriptor-run planning, native batch-kernel mode, shape stability, and non-finite diagnostics.
- a required blocked branch cannot be hidden by another passing branch; formal evidence must preserve branch-specific blockers.

Implementation highlights visible at architecture-review level:
- executes only from a compiled, manifest-bound OOF run specification.
- separates tree-family training, sequence-family training, score-bus output, model cards, and candidate state.
- uses coalesced fixed-shape descriptor-run batching for sequence models when shape stability is required.
- records candidate heartbeats, fold row-set certificates, cache/resume manifests, numerical diagnostics, score partition manifests, execution profiles, and fail-closed blockers.
- prevents tree-only or sequence-downgraded score buses from satisfying formal evidence when a required branch blocks.

Contract shape:
- Inputs: sanitized OOF run spec, trainable partitions, fold policy, model candidate registry, feature/normalizer manifests, sequence tensor references, cache policy, and native-kernel mode.
- Outputs: sanitized score-bus manifest, model cards, candidate states, profile report, EvidenceEnvelope, or execution blocker.

Implementation details intentionally omitted:
- production source code, model hyperparameters, feature values, score outputs, dataset roots, and runtime logs.
"""
