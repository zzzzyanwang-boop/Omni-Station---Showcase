"""Public-safe purged CPCV splitter capsule."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import combinations
from typing import Any


@dataclass(frozen=True)
class SplitPlan:
    split_id: str
    validation_folds: tuple[int, ...]
    train_row_ids: tuple[str, ...]
    validation_row_ids: tuple[str, ...]
    purged_row_ids: tuple[str, ...]
    group_purged_row_ids: tuple[str, ...]


class SplitPlanError(ValueError):
    """Raised when a split plan would be unsafe or under-specified."""


def build_purged_cpcv_splits(
    rows: list[dict[str, Any]],
    *,
    fold_count: int,
    validation_fold_count: int,
    embargo_seconds: int,
    group_field: str = "group",
) -> list[SplitPlan]:
    """Build purged combinatorial validation splits for synthetic row metadata."""

    if fold_count < 2:
        raise SplitPlanError("fold_count must be at least 2")
    if validation_fold_count <= 0 or validation_fold_count >= fold_count:
        raise SplitPlanError("validation_fold_count must be between 1 and fold_count - 1")
    if embargo_seconds < 0:
        raise SplitPlanError("embargo_seconds cannot be negative")

    parsed = [_parse_row(row, group_field) for row in rows]
    folds = {row["fold"] for row in parsed}
    expected_folds = set(range(fold_count))
    if not folds.issubset(expected_folds):
        raise SplitPlanError("rows contain a fold outside declared fold_count")

    split_plans: list[SplitPlan] = []
    embargo = timedelta(seconds=embargo_seconds)
    for index, validation_folds in enumerate(combinations(range(fold_count), validation_fold_count)):
        validation = [row for row in parsed if row["fold"] in validation_folds]
        if not validation:
            raise SplitPlanError(f"split {index} has no validation rows")
        validation_groups = {row[group_field] for row in validation}
        train_ids: list[str] = []
        purged_ids: list[str] = []
        group_purged_ids: list[str] = []
        for row in parsed:
            if row["fold"] in validation_folds:
                continue
            if row[group_field] in validation_groups:
                group_purged_ids.append(row["row_id"])
                continue
            if any(_intervals_overlap(row, validation_row, embargo) for validation_row in validation):
                purged_ids.append(row["row_id"])
                continue
            train_ids.append(row["row_id"])
        if not train_ids:
            raise SplitPlanError(f"split {index} has no safe training rows after purging")
        plan = SplitPlan(
            split_id=f"cpcv_{index:02d}",
            validation_folds=tuple(validation_folds),
            train_row_ids=tuple(train_ids),
            validation_row_ids=tuple(row["row_id"] for row in validation),
            purged_row_ids=tuple(purged_ids),
            group_purged_row_ids=tuple(group_purged_ids),
        )
        validate_split_plan(plan, parsed_rows=parsed, embargo_seconds=embargo_seconds, group_field=group_field)
        split_plans.append(plan)
    return split_plans


def validate_split_plan(
    plan: SplitPlan,
    *,
    parsed_rows: list[dict[str, Any]] | None = None,
    rows: list[dict[str, Any]] | None = None,
    embargo_seconds: int,
    group_field: str = "group",
) -> None:
    """Fail closed if a split violates overlap, group, or embargo constraints."""

    if parsed_rows is None:
        if rows is None:
            raise SplitPlanError("rows or parsed_rows must be provided")
        parsed_rows = [_parse_row(row, group_field) for row in rows]
    by_id = {row["row_id"]: row for row in parsed_rows}
    train = [_required_row(by_id, row_id) for row_id in plan.train_row_ids]
    validation = [_required_row(by_id, row_id) for row_id in plan.validation_row_ids]
    if not train or not validation:
        raise SplitPlanError("split must contain train and validation rows")
    if set(plan.train_row_ids) & set(plan.validation_row_ids):
        raise SplitPlanError("train and validation row ids must be disjoint")
    train_groups = {row[group_field] for row in train}
    validation_groups = {row[group_field] for row in validation}
    if train_groups & validation_groups:
        raise SplitPlanError("train and validation groups must be disjoint")
    embargo = timedelta(seconds=embargo_seconds)
    for train_row in train:
        for validation_row in validation:
            if _intervals_overlap(train_row, validation_row, embargo):
                raise SplitPlanError("train label window overlaps validation window plus embargo")


def _parse_row(row: dict[str, Any], group_field: str) -> dict[str, Any]:
    row_id = _required_string(row, "row_id")
    group = _required_string(row, group_field)
    fold = row.get("fold")
    if not isinstance(fold, int) or fold < 0:
        raise SplitPlanError("fold must be a non-negative integer")
    label_start = _parse_ts(row.get("label_window_start"))
    label_end = _parse_ts(row.get("label_window_end"))
    if label_end < label_start:
        raise SplitPlanError("label_window_end must be at or after label_window_start")
    return {
        **row,
        "row_id": row_id,
        group_field: group,
        "fold": fold,
        "label_window_start": label_start,
        "label_window_end": label_end,
    }


def _intervals_overlap(train_row: dict[str, Any], validation_row: dict[str, Any], embargo: timedelta) -> bool:
    train_start = train_row["label_window_start"] - embargo
    train_end = train_row["label_window_end"] + embargo
    validation_start = validation_row["label_window_start"]
    validation_end = validation_row["label_window_end"]
    return train_start <= validation_end and validation_start <= train_end


def _required_row(by_id: dict[str, dict[str, Any]], row_id: str) -> dict[str, Any]:
    row = by_id.get(row_id)
    if row is None:
        raise SplitPlanError(f"unknown row id {row_id!r}")
    return row


def _required_string(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise SplitPlanError(f"{key} must be a non-empty string")
    return value


def _parse_ts(value: Any) -> datetime:
    if not isinstance(value, str) or not value:
        raise SplitPlanError("timestamps must be non-empty ISO strings")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SplitPlanError("timestamps must be valid ISO strings") from exc

