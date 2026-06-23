# Stage1 Trainable Join Pseudocode

This pseudocode shows how a trainable matrix can be built from source-backed labels and factor artifacts without exposing factor values or label formulas.

```text
function build_stage1_trainable(contract, factor_manifest, label_view_manifest):
    require contract.stage == "stage1_trainable"
    require factor_manifest.source_scope compatible with contract.panel_scope
    require label_view_manifest.source_boundary compatible with contract.source_boundary
    require contract.join_policy is declared

    date_plan = group_factor_parts_by_trading_date(factor_manifest)
    output_parts = []
    reject_summary = []

    for date_key in date_plan.ordered_dates:
        label_side = get_or_build_prepared_date_label_cache(
            date_key,
            label_view_manifest,
            contract.join_policy
        )

        for factor_part in date_plan.factor_parts[date_key]:
            projected_factor = scan_columns(
                factor_part,
                columns=contract.required_factor_columns
            )
            joined = streaming_asof_or_key_join(
                projected_factor,
                label_side,
                keys=contract.join_policy.keys
            )
            output_part = sink_parquet(joined.matched_rows)
            output_parts.append(output_part.manifest_ref)
            reject_summary.append(joined.reject_counts)

    return trainable_manifest(
        parts=output_parts,
        label_reader_mode="source_backed",
        reject_ledger=compact(reject_summary),
        source_refs=[factor_manifest.id, label_view_manifest.id]
    )
```

Review signal:

- source-backed labels stay lazy until the join point
- date-level preparation is reused only through manifest-bound cache identity
- matched rows stream to columnar output
- rejects are summarized instead of hidden
- the active path does not require collecting a full joined table in memory

