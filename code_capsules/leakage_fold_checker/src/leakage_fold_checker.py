"""Public-safe leakage and fold validation capsule."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


VALID_SPLITS = {"train", "validation", "test"}


@dataclass(frozen=True)
class LeakageIssue:
    code: str
    row_id: str | None
    fold_id: str | None
    message: str


@dataclass(frozen=True)
class LeakageReport:
    ok: bool
    issues: tuple[LeakageIssue, ...]


def validate_rows(rows: list[dict[str, Any]], embargo_seconds: int = 0) -> LeakageReport:
    """Validate point-in-time row semantics and fold embargo.

    The rows are synthetic. Each row is expected to carry an ``as_of`` decision
    timestamp, a ``feature_available_at`` timestamp, and a forward label window.
    """

    issues: list[LeakageIssue] = []
    parsed_rows: list[dict[str, Any]] = []
    for row in rows:
        parsed = _parse_row(row, issues)
        if parsed is not None:
            parsed_rows.append(parsed)
            _validate_row_temporal_order(parsed, issues)

    _validate_fold_embargo(parsed_rows, timedelta(seconds=embargo_seconds), issues)
    return LeakageReport(ok=not issues, issues=tuple(issues))


def _parse_row(row: dict[str, Any], issues: list[LeakageIssue]) -> dict[str, Any] | None:
    row_id = _string(row.get("row_id"))
    fold_id = _string(row.get("fold_id"))
    split = _string(row.get("split"))
    if split not in VALID_SPLITS:
        issues.append(LeakageIssue("invalid_split", row_id, fold_id, "split is not recognized"))
        return None

    fields = ("as_of", "feature_available_at", "label_window_start", "label_window_end")
    parsed: dict[str, Any] = dict(row)
    for field in fields:
        try:
            parsed[field] = _parse_ts(row[field])
        except (KeyError, TypeError, ValueError):
            issues.append(LeakageIssue("invalid_timestamp", row_id, fold_id, f"{field} is invalid"))
            return None
    return parsed


def _validate_row_temporal_order(row: dict[str, Any], issues: list[LeakageIssue]) -> None:
    row_id = _string(row.get("row_id"))
    fold_id = _string(row.get("fold_id"))
    as_of = row["as_of"]
    feature_available_at = row["feature_available_at"]
    label_start = row["label_window_start"]
    label_end = row["label_window_end"]

    if feature_available_at > as_of:
        issues.append(
            LeakageIssue(
                "future_feature",
                row_id,
                fold_id,
                "feature availability is after the decision timestamp",
            )
        )
    if label_start < as_of:
        issues.append(
            LeakageIssue(
                "backward_label_window",
                row_id,
                fold_id,
                "label window starts before the decision timestamp",
            )
        )
    if label_end <= label_start:
        issues.append(
            LeakageIssue(
                "empty_label_window",
                row_id,
                fold_id,
                "label window must end after it starts",
            )
        )


def _validate_fold_embargo(
    rows: list[dict[str, Any]],
    embargo: timedelta,
    issues: list[LeakageIssue],
) -> None:
    folds = sorted({_string(row.get("fold_id")) for row in rows})
    for fold_id in folds:
        if fold_id is None:
            continue
        fold_rows = [row for row in rows if row.get("fold_id") == fold_id]
        train_rows = [row for row in fold_rows if row.get("split") == "train"]
        validation_rows = [row for row in fold_rows if row.get("split") == "validation"]
        if not train_rows or not validation_rows:
            continue
        max_train_label_end = max(row["label_window_end"] for row in train_rows)
        min_validation_as_of = min(row["as_of"] for row in validation_rows)
        if max_train_label_end + embargo > min_validation_as_of:
            issues.append(
                LeakageIssue(
                    "fold_embargo_violation",
                    None,
                    fold_id,
                    "training label windows overlap the validation decision region after embargo",
                )
            )


def _parse_ts(value: str) -> datetime:
    if not isinstance(value, str):
        raise TypeError("timestamp must be a string")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None
