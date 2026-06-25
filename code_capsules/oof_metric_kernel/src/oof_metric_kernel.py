"""Public-safe grouped OOF metric kernel capsule."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Any, Iterable


@dataclass
class MomentState:
    count: int = 0
    sum_x: float = 0.0
    sum_y: float = 0.0
    sum_xx: float = 0.0
    sum_yy: float = 0.0
    sum_xy: float = 0.0

    def update(self, x: float, y: float) -> None:
        self.count += 1
        self.sum_x += x
        self.sum_y += y
        self.sum_xx += x * x
        self.sum_yy += y * y
        self.sum_xy += x * y

    def pearson(self) -> float | None:
        if self.count < 2:
            return None
        n = float(self.count)
        cov = self.sum_xy - (self.sum_x * self.sum_y / n)
        var_x = self.sum_xx - (self.sum_x * self.sum_x / n)
        var_y = self.sum_yy - (self.sum_y * self.sum_y / n)
        if var_x <= 0.0 or var_y <= 0.0:
            return None
        return cov / sqrt(var_x * var_y)


class MetricInputError(ValueError):
    """Raised when metric input is malformed enough to make the result unsafe."""


def grouped_oof_metrics(
    rows: Iterable[dict[str, Any]],
    group_fields: tuple[str, ...],
    *,
    score_field: str = "score",
    label_field: str = "label",
) -> list[dict[str, Any]]:
    """Aggregate grouped OOF metrics with deterministic filtering."""

    moments: dict[tuple[Any, ...], MomentState] = defaultdict(MomentState)
    rank_pairs: dict[tuple[Any, ...], list[tuple[float, float]]] = defaultdict(list)
    skipped_by_group: dict[tuple[Any, ...], int] = defaultdict(int)

    if not group_fields:
        raise MetricInputError("group_fields must contain at least one field")

    for row in rows:
        key = _group_key(row, group_fields)
        score = _finite_float(row.get(score_field))
        label = _finite_float(row.get(label_field))
        if score is None or label is None:
            skipped_by_group[key] += 1
            continue
        moments[key].update(score, label)
        rank_pairs[key].append((score, label))

    output: list[dict[str, Any]] = []
    for key in sorted(moments):
        state = moments[key]
        output.append(
            {
                "group": dict(zip(group_fields, key)),
                "row_count": state.count,
                "pearson_ic": state.pearson(),
                "rank_ic": rank_ic(rank_pairs[key]),
                "mean_score": state.sum_x / state.count if state.count else None,
                "mean_label": state.sum_y / state.count if state.count else None,
                "skipped_non_finite_rows": skipped_by_group[key],
            }
        )
    return output


def rank_ic(pairs: list[tuple[float, float]]) -> float | None:
    if len(pairs) < 2:
        return None
    scores = [score for score, _ in pairs]
    labels = [label for _, label in pairs]
    score_ranks = average_ranks(scores)
    label_ranks = average_ranks(labels)
    state = MomentState()
    for x_rank, y_rank in zip(score_ranks, label_ranks):
        state.update(x_rank, y_rank)
    return state.pearson()


def average_ranks(values: list[float]) -> list[float]:
    """Return one-based average ranks with deterministic tie handling."""

    indexed = sorted(enumerate(values), key=lambda item: (item[1], item[0]))
    ranks = [0.0] * len(values)
    cursor = 0
    while cursor < len(indexed):
        tie_end = cursor + 1
        while tie_end < len(indexed) and indexed[tie_end][1] == indexed[cursor][1]:
            tie_end += 1
        average_rank = (cursor + 1 + tie_end) / 2.0
        for position in range(cursor, tie_end):
            original_index = indexed[position][0]
            ranks[original_index] = average_rank
        cursor = tie_end
    return ranks


def _finite_float(value: Any) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if isfinite(parsed) else None


def _group_key(row: dict[str, Any], group_fields: tuple[str, ...]) -> tuple[str, ...]:
    key: list[str] = []
    for field in group_fields:
        value = row.get(field)
        if value is None or value == "":
            raise MetricInputError(f"group field {field!r} is missing or empty")
        if not isinstance(value, (str, int)):
            raise MetricInputError(f"group field {field!r} must be a string or integer")
        key.append(str(value))
    return tuple(key)
