"""Public-safe source-part joinability gate capsule."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class JoinabilityReport:
    ok: bool
    joinable_pairs: tuple[tuple[str, str], ...]
    issues: tuple[str, ...]
    checked_left_parts: int
    checked_right_parts: int
    join_policy: str


class JoinabilityError(ValueError):
    """Raised when source-part metadata is malformed."""


def check_source_joinability(
    left_parts: list[dict[str, Any]],
    right_parts: list[dict[str, Any]],
    *,
    require_row_count_proof: bool = True,
    join_policy: str = "asof_backward_or_exact",
    expected_left_dataset_id: str | None = None,
    expected_right_dataset_id: str | None = None,
) -> JoinabilityReport:
    """Check whether synthetic source parts are joinable at part level."""

    parsed_left = [_parse_part(part) for part in left_parts]
    parsed_right = [_parse_part(part) for part in right_parts]
    issues: list[str] = []
    joinable_pairs: list[tuple[str, str]] = []
    for left in parsed_left:
        if expected_left_dataset_id is not None and left["dataset_id"] != expected_left_dataset_id:
            issues.append(f"left_dataset_mismatch:{left['part_id']}:{left['dataset_id']}")
            continue
        same_date = [right for right in parsed_right if right["date"] == left["date"]]
        if not same_date:
            issues.append(f"missing_right_date:{left['dataset_id']}:{left['part_id']}")
            continue
        matched = False
        for right in same_date:
            if expected_right_dataset_id is not None and right["dataset_id"] != expected_right_dataset_id:
                issues.append(f"right_dataset_mismatch:{right['part_id']}:{right['dataset_id']}")
                continue
            if left["publisher"] != right["publisher"]:
                issues.append(f"publisher_mismatch:{left['part_id']}:{right['part_id']}")
                continue
            if left["_timezone_state"] != right["_timezone_state"]:
                issues.append(f"timezone_policy_mismatch:{left['part_id']}:{right['part_id']}")
                continue
            has_symbol_overlap = _range_overlap(left["symbol_start"], left["symbol_end"], right["symbol_start"], right["symbol_end"])
            has_time_overlap = _range_overlap(left["time_start"], left["time_end"], right["time_start"], right["time_end"])
            has_row_count_proof = left["row_count"] > 0 and right["row_count"] > 0
            if require_row_count_proof and not has_row_count_proof:
                issues.append(f"missing_row_count_proof:{left['part_id']}:{right['part_id']}")
                continue
            if has_symbol_overlap and has_time_overlap:
                matched = True
                joinable_pairs.append((left["part_id"], right["part_id"]))
        if not matched:
            issues.append(f"date_only_match_without_part_overlap:{left['part_id']}")
    return JoinabilityReport(
        ok=not issues and bool(joinable_pairs),
        joinable_pairs=tuple(joinable_pairs),
        issues=tuple(issues),
        checked_left_parts=len(parsed_left),
        checked_right_parts=len(parsed_right),
        join_policy=join_policy,
    )


def _parse_part(part: dict[str, Any]) -> dict[str, Any]:
    parsed = {
        "part_id": _required_string(part, "part_id"),
        "dataset_id": _required_string(part, "dataset_id"),
        "publisher": _required_string(part, "publisher"),
        "date": _required_string(part, "date"),
        "symbol_start": _required_string(part, "symbol_start").upper(),
        "symbol_end": _required_string(part, "symbol_end").upper(),
        "time_start": _parse_ts(part.get("time_start")),
        "time_end": _parse_ts(part.get("time_end")),
        "row_count": part.get("row_count"),
    }
    if parsed["symbol_start"] > parsed["symbol_end"]:
        raise JoinabilityError("symbol range must be ordered")
    if parsed["time_start"] > parsed["time_end"]:
        raise JoinabilityError("time range must be ordered")
    if _timezone_state(parsed["time_start"]) != _timezone_state(parsed["time_end"]):
        raise JoinabilityError("time_start and time_end must use the same timezone-awareness policy")
    parsed["_timezone_state"] = _timezone_state(parsed["time_start"])
    if not isinstance(parsed["row_count"], int) or isinstance(parsed["row_count"], bool):
        parsed["row_count"] = 0
    return parsed


def _range_overlap(left_start: Any, left_end: Any, right_start: Any, right_end: Any) -> bool:
    return max(left_start, right_start) <= min(left_end, right_end)


def _required_string(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise JoinabilityError(f"{key} must be a non-empty string")
    return value


def _parse_ts(value: Any) -> datetime:
    if not isinstance(value, str) or not value:
        raise JoinabilityError("time fields must be non-empty ISO strings")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise JoinabilityError("time fields must be valid ISO strings") from exc


def _timezone_state(value: datetime) -> str:
    return "aware" if value.tzinfo is not None and value.utcoffset() is not None else "naive"
