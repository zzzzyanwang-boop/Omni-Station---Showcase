# Sequence OOF Batch Planner Pseudocode

This pseudocode shows the reviewable shape of fixed-size descriptor-run planning for sequence-model OOF.

```text
function plan_sequence_oof_batches(oof_spec, trainable_manifest, tensor_policy):
    require oof_spec.fold_policy is declared
    require trainable_manifest.source_boundary compatible with oof_spec.source_boundary
    require tensor_policy.fixed_shape_required == true

    descriptors = resolve_sequence_descriptors(trainable_manifest, tensor_policy)
    validity = native_pack_feature_validity(descriptors.feature_matrix)
    runs = native_find_contiguous_anchor_runs(validity, tensor_policy.lookback)

    batches = []
    for run in runs:
        for batch in coalesce_fixed_shape(run, tensor_policy.batch_shape):
            if batch.shape != tensor_policy.batch_shape:
                return blocker("sequence_shape_instability")
            batches.append(batch)

    if batches is empty:
        return blocker("no_valid_sequence_batches")

    return sequence_batch_plan(
        batches=batches,
        native_kernel_id=tensor_policy.kernel_id,
        diagnostics={
            "shape_stability_required": true,
            "padding_allowed": false,
            "silent_drop_allowed": false
        }
    )
```

Review signal:

- descriptor-run batching is explicit
- shape instability blocks rather than padding or dropping silently
- native kernel use is metadata-bound
- non-finite or shape diagnostics become evidence metadata

