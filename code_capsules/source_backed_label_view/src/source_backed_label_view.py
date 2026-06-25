"""Public-safe source-backed label view planner capsule."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LabelViewPlan:
    label_id: str
    source_dataset_id: str
    materialization_policy: str
    projected_columns: tuple[str, ...]
    physical_operations: tuple[str, ...]
    estimated_dense_rows_written: int
    estimated_view_rows_written: int


class LabelPlanError(ValueError):
    """Raised when a label plan would be unsafe or under-specified."""


def build_label_view_plan(
    source_manifest: dict[str, Any],
    label_spec: dict[str, Any],
    *,
    force_dense: bool = False,
) -> LabelViewPlan:
    """Build a deterministic label view physical plan for synthetic metadata."""

    dataset_id = _required_string(source_manifest, "dataset_id")
    entity_key = _required_string(source_manifest, "entity_key")
    time_key = _required_string(source_manifest, "time_key")
    label_id = _required_string(label_spec, "label_id")
    horizon_rows = int(label_spec.get("horizon_rows", 0))
    if horizon_rows <= 0:
        raise LabelPlanError("forward-looking labels must declare a positive horizon_rows")

    columns = _columns_by_name(source_manifest)
    required_columns = tuple(_required_string_list(label_spec, "required_columns"))
    missing = [column for column in required_columns if column not in columns]
    if missing:
        raise LabelPlanError(f"label requires missing source columns: {', '.join(missing)}")

    unsafe = [
        column
        for column in required_columns
        if not bool(columns[column].get("point_in_time_safe"))
    ]
    if unsafe:
        raise LabelPlanError(f"label uses non point-in-time-safe columns: {', '.join(unsafe)}")

    partition_keys = tuple(_string_list(source_manifest.get("partition_keys", [])))
    projected_columns = _unique((*partition_keys, entity_key, time_key, *required_columns))
    policy = "dense_materialization" if force_dense else label_spec.get(
        "materialization_policy", "source_backed_view"
    )
    if policy not in {"source_backed_view", "dense_materialization"}:
        raise LabelPlanError("unsupported materialization policy")

    estimated_rows = int(source_manifest.get("estimated_rows", 0))
    dense_rows = estimated_rows if policy == "dense_materialization" else 0
    view_rows = len(partition_keys) + 1 if policy == "source_backed_view" else estimated_rows
    operations = _operations(policy, projected_columns, horizon_rows)

    return LabelViewPlan(
        label_id=label_id,
        source_dataset_id=dataset_id,
        materialization_policy=policy,
        projected_columns=projected_columns,
        physical_operations=operations,
        estimated_dense_rows_written=dense_rows,
        estimated_view_rows_written=view_rows,
    )


def _operations(policy: str, projected_columns: tuple[str, ...], horizon_rows: int) -> tuple[str, ...]:
    common = (
        f"read_source_projection[{','.join(projected_columns)}]",
        f"bind_forward_window[horizon_rows={horizon_rows}]",
        "record_source_manifest_ref",
    )
    if policy == "source_backed_view":
        return (*common, "write_logical_label_view_manifest", "defer_row_level_label_materialization")
    return (*common, "compute_dense_label_column", "write_dense_label_partitions")


def _columns_by_name(source_manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    columns = source_manifest.get("columns")
    if not isinstance(columns, list):
        raise LabelPlanError("source_manifest.columns must be a list")
    by_name: dict[str, dict[str, Any]] = {}
    for column in columns:
        if not isinstance(column, dict) or not isinstance(column.get("name"), str):
            raise LabelPlanError("each source column must have a string name")
        by_name[column["name"]] = column
    return by_name


def _required_string(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise LabelPlanError(f"{key} must be a non-empty string")
    return value


def _required_string_list(mapping: dict[str, Any], key: str) -> tuple[str, ...]:
    values = mapping.get(key)
    if not isinstance(values, list) or not values:
        raise LabelPlanError(f"{key} must be a non-empty list")
    parsed = _string_list(values)
    if len(parsed) != len(values):
        raise LabelPlanError(f"{key} must only contain strings")
    return parsed


def _string_list(values: Any) -> tuple[str, ...]:
    if not isinstance(values, list):
        return ()
    return tuple(value for value in values if isinstance(value, str) and value)


def _unique(values: tuple[str, ...]) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return tuple(result)
