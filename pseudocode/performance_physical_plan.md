# Performance Physical Plan Pseudocode

This pseudocode shows how a performance rewrite is framed before implementation.

```text
function build_physical_plan(contract, baseline_profile):
    require contract.correctness_oracle is declared
    require baseline_profile.hotspots are measured

    dominant = select_largest_physical_cost(baseline_profile)

    if dominant.kind == "repeated_source_scan":
        plan = reduce_scans_with_partition_or_source_backed_view(contract)
    else if dominant.kind == "dense_materialization":
        plan = replace_with_logical_view_or_streaming_writer(contract)
    else if dominant.kind == "python_loop":
        plan = move_loop_to_vectorized_or_native_boundary(contract)
    else if dominant.kind == "repeated_join_preparation":
        plan = introduce_manifest_bound_prepared_cache(contract)
    else:
        plan = keep_reference_path_and_collect_more_profile(contract)

    plan.must_include = [
        "removed_work",
        "input_contract",
        "output_manifest_shape",
        "parity_gate",
        "rollback_or_blocker_policy",
        "remaining_bottleneck_report"
    ]

    return plan
```

Review signal:

- speedup claims start from measured physical cost
- governance wrappers are not counted as performance gains unless they remove work
- native rewrites require parity and explicit blocker behavior

