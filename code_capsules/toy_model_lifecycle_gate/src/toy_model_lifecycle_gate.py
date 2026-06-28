"""Executable public-safe toy model lifecycle gate.

The capsule is intentionally small, deterministic, and synthetic. It shows the
contract shape of an ML research lifecycle without exposing production model
code, feature definitions, data, weights, thresholds, or runtime configuration.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from math import isfinite
from pathlib import Path
from statistics import mean
from typing import Any

from code_capsules.artifact_manifest_hasher import (
    ArtifactManifest,
    ManifestError,
    build_artifact_manifest,
    validate_artifact_support,
)
from code_capsules.oof_metric_kernel import grouped_oof_metrics
from code_capsules.purged_cpcv_splitter import build_purged_cpcv_splits


ROOT = Path(__file__).resolve().parents[3]
FEATURE_FIELDS = ("toy_feature_a", "toy_feature_b")
PREDICTION_SCHEMA = ("row_id", "fold", "branch_id", "score", "label")


@dataclass(frozen=True)
class BranchSpec:
    branch_id: str
    model_family: str
    feature_fields: tuple[str, ...]
    deterministic_seed: int


class ModelLifecycleError(ValueError):
    """Raised when a synthetic ML lifecycle contract is malformed."""


def run_toy_model_lifecycle_gate(
    *,
    inject_stale_trainable: bool = False,
    inject_missing_fold_proof: bool = False,
    inject_non_finite_prediction: bool = False,
    inject_missing_calibration: bool = False,
    inject_ood_drift: bool = False,
    inject_proxy_score_artifact: bool = False,
    inject_replay_schema_mismatch: bool = False,
    inject_diagnostic_model_card_support: bool = False,
) -> dict[str, Any]:
    """Run a deterministic synthetic train-to-eligibility lifecycle."""

    rows = _trainable_rows()
    branch = BranchSpec(
        branch_id="toy_linear_branch_v1",
        model_family="toy_linear_ranker",
        feature_fields=FEATURE_FIELDS,
        deterministic_seed=17,
    )
    split_plans = [] if inject_missing_fold_proof else build_purged_cpcv_splits(
        rows,
        fold_count=3,
        validation_fold_count=1,
        embargo_seconds=0,
    )
    oof_rows = _build_oof_rows(rows, split_plans, branch)
    if inject_non_finite_prediction and oof_rows:
        oof_rows[0]["score"] = "nan"

    trainable_manifest = _manifest(
        "toy.trainable_matrix.v1",
        schema={
            "columns": ("row_id", "fold", "as_of", *branch.feature_fields, "label"),
            "fold_policy": "purged_embargoed_fold_rows",
        },
        rows=[
            {
                "row_id": row["row_id"],
                "fold": row["fold"],
                "as_of": row["as_of"],
                "features": {field: row[field] for field in branch.feature_fields},
                "label": row["label"],
            }
            for row in rows
        ],
        lineage={"source": "toy.stage1_trainable_manifest", "label_reader": "source_backed_view"},
    )
    prediction_manifest = _manifest(
        "toy.proxy_score_artifact.v1" if inject_proxy_score_artifact else "toy.oof_predictions.v1",
        schema={"columns": PREDICTION_SCHEMA, "branch_id": branch.branch_id},
        rows=oof_rows,
        lineage={"trainable": trainable_manifest.artifact_id, "fold_policy": "purged_embargoed_fold_rows"},
        artifact_role="diagnostic" if inject_proxy_score_artifact else "decision",
        diagnostic_only=inject_proxy_score_artifact,
    )
    calibration_report = None if inject_missing_calibration else _calibration_report(oof_rows)
    calibration_manifest = None if calibration_report is None else _manifest(
        "toy.calibration_ood_report.v1",
        schema={"columns": ("bucket", "count", "mean_score", "mean_label", "absolute_gap")},
        rows=calibration_report["calibration_bins"],
        lineage={"oof_predictions": prediction_manifest.artifact_id},
        artifact_role="diagnostic" if inject_diagnostic_model_card_support else "decision",
        diagnostic_only=inject_diagnostic_model_card_support,
    )
    ood_report = _ood_report(oof_rows, inject_ood_drift=inject_ood_drift)
    replay_report = _prediction_replay_report(oof_rows, inject_schema_mismatch=inject_replay_schema_mismatch)
    replay_manifest = _manifest(
        "toy.prediction_replay_manifest.v1",
        schema={"columns": replay_report["observed_schema"]},
        rows=replay_report["sample_rows"],
        lineage={"oof_predictions": prediction_manifest.artifact_id},
    )

    blockers = _evaluate_blockers(
        trainable_manifest=trainable_manifest,
        prediction_manifest=prediction_manifest,
        calibration_manifest=calibration_manifest,
        replay_manifest=replay_manifest,
        expected_trainable_content_hash="sha256:stale" if inject_stale_trainable else trainable_manifest.content_hash,
        split_plans=split_plans,
        oof_rows=oof_rows,
        calibration_report=calibration_report,
        ood_report=ood_report,
        replay_report=replay_report,
        inject_proxy_score_artifact=inject_proxy_score_artifact,
        inject_diagnostic_model_card_support=inject_diagnostic_model_card_support,
    )
    gate_status = "pass" if not blockers else "block"
    model_card = _model_card(
        branch=branch,
        trainable_manifest=trainable_manifest,
        prediction_manifest=prediction_manifest,
        calibration_manifest=calibration_manifest,
        replay_manifest=replay_manifest,
        gate_status=gate_status,
        blockers=blockers,
    )
    return {
        "flow_id": "toy_model_lifecycle_gate",
        "runtime_posture": _offline_posture(),
        "trainable_manifest": _manifest_view(trainable_manifest)
        | {
            "row_count": len(rows),
            "feature_fields": list(branch.feature_fields),
            "label_policy": "source_backed_forward_label",
            "source_boundary_ref": "synthetic_source_boundary_packet",
        },
        "fold_row_set_proof": [_split_view(plan) for plan in split_plans],
        "branch": {
            "branch_id": branch.branch_id,
            "model_family": branch.model_family,
            "deterministic_seed": branch.deterministic_seed,
            "training_policy": "fold_local_oof_only",
            "candidate_state": "eligible" if gate_status == "pass" else "blocked",
            "oof_prediction_manifest": _manifest_view(prediction_manifest),
            "oof_metrics": grouped_oof_metrics(oof_rows, ("fold",), score_field="score", label_field="label"),
            "calibration_ood_report": calibration_report,
            "ood_report": ood_report,
            "uncertainty": _uncertainty_report(oof_rows),
            "model_card": model_card,
        },
        "prediction_replay": replay_report,
        "eligibility_gate": {
            "status": gate_status,
            "blockers": blockers,
            "supported_artifacts": [
                trainable_manifest.artifact_id,
                prediction_manifest.artifact_id,
                calibration_manifest.artifact_id if calibration_manifest is not None else "missing:calibration",
                replay_manifest.artifact_id,
            ],
            "failure_modes_checked": [
                "stale_trainable_manifest",
                "missing_fold_row_set_proof",
                "non_finite_prediction",
                "missing_calibration",
                "ood_drift",
                "proxy_score_artifact",
                "diagnostic_support_artifact",
                "prediction_replay_schema_mismatch",
            ],
        },
    }


def _evaluate_blockers(
    *,
    trainable_manifest: ArtifactManifest,
    prediction_manifest: ArtifactManifest,
    calibration_manifest: ArtifactManifest | None,
    replay_manifest: ArtifactManifest,
    expected_trainable_content_hash: str,
    split_plans: list[Any],
    oof_rows: list[dict[str, Any]],
    calibration_report: dict[str, Any] | None,
    ood_report: dict[str, Any],
    replay_report: dict[str, Any],
    inject_proxy_score_artifact: bool,
    inject_diagnostic_model_card_support: bool,
) -> list[str]:
    blockers: list[str] = []
    if not split_plans:
        blockers.append("missing_fold_row_set_proof")
    if any(not _is_finite_number(row.get("score")) for row in oof_rows):
        blockers.append("non_finite_prediction")
    if calibration_report is None:
        blockers.append("missing_calibration_report")
    if ood_report["status"] != "pass":
        blockers.append("ood_score_distribution_drift")
    if replay_report["status"] != "pass":
        blockers.append("prediction_replay_schema_mismatch")
    if inject_proxy_score_artifact:
        blockers.append("proxy_score_artifact")
    if inject_diagnostic_model_card_support:
        blockers.append("diagnostic_support_artifact")

    manifests = {
        trainable_manifest.artifact_id: trainable_manifest,
        prediction_manifest.artifact_id: prediction_manifest,
        replay_manifest.artifact_id: replay_manifest,
    }
    supported_by = [trainable_manifest.artifact_id, prediction_manifest.artifact_id, replay_manifest.artifact_id]
    expected_hashes = {
        trainable_manifest.artifact_id: {
            "schema_hash": trainable_manifest.schema_hash,
            "content_hash": expected_trainable_content_hash,
            "lineage_hash": trainable_manifest.lineage_hash,
        },
        prediction_manifest.artifact_id: _expected_hashes(prediction_manifest),
        replay_manifest.artifact_id: _expected_hashes(replay_manifest),
    }
    if calibration_manifest is not None:
        manifests[calibration_manifest.artifact_id] = calibration_manifest
        supported_by.append(calibration_manifest.artifact_id)
        expected_hashes[calibration_manifest.artifact_id] = _expected_hashes(calibration_manifest)
    try:
        validate_artifact_support(
            {
                "scope": "decision_grade",
                "supported_by": supported_by,
                "expected_hashes": expected_hashes,
            },
            manifests,
        )
    except ManifestError as exc:
        message = str(exc)
        if "stale supporting artifact" in message and "toy.trainable_matrix.v1" in message:
            blockers.append("stale_trainable_manifest")
        elif "diagnostic artifact" in message:
            blockers.append("diagnostic_artifact_support")
        else:
            blockers.append("artifact_support_invalid")
    return sorted(set(blockers))


def _build_oof_rows(rows: list[dict[str, Any]], split_plans: list[Any], branch: BranchSpec) -> list[dict[str, Any]]:
    by_id = {row["row_id"]: row for row in rows}
    predictions: list[dict[str, Any]] = []
    for plan in split_plans:
        train_rows = [by_id[row_id] for row_id in plan.train_row_ids]
        model = _fit_toy_model(train_rows, branch.feature_fields)
        for row_id in plan.validation_row_ids:
            row = by_id[row_id]
            score = model["intercept"] + sum(model["weights"][field] * row[field] for field in branch.feature_fields)
            predictions.append(
                {
                    "row_id": row_id,
                    "fold": f"f{row['fold']}",
                    "branch_id": branch.branch_id,
                    "score": round(score, 6),
                    "label": row["label"],
                }
            )
    return sorted(predictions, key=lambda row: row["row_id"])


def _fit_toy_model(rows: list[dict[str, Any]], feature_fields: tuple[str, ...]) -> dict[str, Any]:
    if not rows:
        raise ModelLifecycleError("training rows must be non-empty")
    label_mean = mean(float(row["label"]) for row in rows)
    weights: dict[str, float] = {}
    for field in feature_fields:
        feature_values = [float(row[field]) for row in rows]
        feature_mean = mean(feature_values)
        numerator = sum((float(row[field]) - feature_mean) * (float(row["label"]) - label_mean) for row in rows)
        denominator = sum((float(row[field]) - feature_mean) ** 2 for row in rows)
        weights[field] = numerator / denominator if denominator else 0.0
    intercept = label_mean - sum(weights[field] * mean(float(row[field]) for row in rows) for field in feature_fields)
    return {"intercept": intercept, "weights": weights}


def _calibration_report(oof_rows: list[dict[str, Any]]) -> dict[str, Any]:
    finite_rows = [row for row in oof_rows if _is_finite_number(row.get("score")) and _is_finite_number(row.get("label"))]
    ordered = sorted(finite_rows, key=lambda row: float(row["score"]))
    midpoint = len(ordered) // 2
    buckets = [("low_score", ordered[:midpoint]), ("high_score", ordered[midpoint:])]
    bins = []
    for bucket, rows in buckets:
        if not rows:
            continue
        mean_score = mean(float(row["score"]) for row in rows)
        mean_label = mean(float(row["label"]) for row in rows)
        bins.append(
            {
                "bucket": bucket,
                "count": len(rows),
                "mean_score": round(mean_score, 6),
                "mean_label": round(mean_label, 6),
                "absolute_gap": round(abs(mean_score - mean_label), 6),
            }
        )
    return {
        "report_id": "toy_calibration_ood_report",
        "status": "pass" if len(bins) == 2 else "block",
        "calibration_bins": bins,
        "policy": "synthetic_two_bucket_reliability",
    }


def _ood_report(oof_rows: list[dict[str, Any]], *, inject_ood_drift: bool) -> dict[str, Any]:
    finite_scores = [float(row["score"]) for row in oof_rows if _is_finite_number(row.get("score"))]
    if not finite_scores:
        return {"status": "block", "mean_shift": None, "policy": "synthetic_score_distribution_shift"}
    replay_scores = [score + (3.0 if inject_ood_drift else 0.05) for score in finite_scores]
    shift = mean(replay_scores) - mean(finite_scores)
    return {
        "status": "pass" if abs(shift) <= 0.5 else "block",
        "mean_shift": round(shift, 6),
        "policy": "synthetic_score_distribution_shift",
        "threshold": 0.5,
    }


def _uncertainty_report(oof_rows: list[dict[str, Any]]) -> dict[str, Any]:
    finite_scores = [float(row["score"]) for row in oof_rows if _is_finite_number(row.get("score"))]
    return {
        "status": "pass" if len(finite_scores) == len(oof_rows) and finite_scores else "block",
        "non_finite_prediction_count": len(oof_rows) - len(finite_scores),
        "score_min": round(min(finite_scores), 6) if finite_scores else None,
        "score_max": round(max(finite_scores), 6) if finite_scores else None,
        "policy": "finite_oof_scores_required",
    }


def _prediction_replay_report(oof_rows: list[dict[str, Any]], *, inject_schema_mismatch: bool) -> dict[str, Any]:
    observed_schema = list(PREDICTION_SCHEMA[:-1] if inject_schema_mismatch else PREDICTION_SCHEMA)
    sample_rows = [{field: row[field] for field in observed_schema if field in row} for row in oof_rows[:2]]
    return {
        "manifest_id": "toy_prediction_replay_manifest",
        "status": "pass" if tuple(observed_schema) == PREDICTION_SCHEMA else "block",
        "expected_schema": list(PREDICTION_SCHEMA),
        "observed_schema": observed_schema,
        "sample_rows": sample_rows,
        "compatibility_policy": "prediction_replay_schema_must_match_oof_manifest",
    }


def _model_card(
    *,
    branch: BranchSpec,
    trainable_manifest: ArtifactManifest,
    prediction_manifest: ArtifactManifest,
    calibration_manifest: ArtifactManifest | None,
    replay_manifest: ArtifactManifest,
    gate_status: str,
    blockers: list[str],
) -> dict[str, Any]:
    return {
        "model_card_id": "toy_model_card_v1",
        "branch_id": branch.branch_id,
        "model_family": branch.model_family,
        "decision_scope": "decision_grade" if gate_status == "pass" else "blocked",
        "supported_by": [
            trainable_manifest.artifact_id,
            prediction_manifest.artifact_id,
            calibration_manifest.artifact_id if calibration_manifest is not None else "missing:calibration",
            replay_manifest.artifact_id,
        ],
        "blocked_reasons": blockers,
        "inference_eligible": False,
        "runtime_posture": _offline_posture(),
    }


def _manifest(
    artifact_id: str,
    *,
    schema: dict[str, Any],
    rows: list[dict[str, Any]],
    lineage: dict[str, Any],
    artifact_role: str = "decision",
    diagnostic_only: bool = False,
) -> ArtifactManifest:
    return build_artifact_manifest(
        artifact_id,
        schema=schema,
        rows=rows,
        lineage=lineage,
        artifact_role=artifact_role,
        diagnostic_only=diagnostic_only,
    )


def _expected_hashes(manifest: ArtifactManifest) -> dict[str, str]:
    return {
        "schema_hash": manifest.schema_hash,
        "content_hash": manifest.content_hash,
        "lineage_hash": manifest.lineage_hash,
    }


def _manifest_view(manifest: ArtifactManifest) -> dict[str, Any]:
    return asdict(manifest)


def _split_view(plan: Any) -> dict[str, Any]:
    return {
        "split_id": plan.split_id,
        "path_key": plan.path_key,
        "validation_folds": list(plan.validation_folds),
        "train_row_ids": list(plan.train_row_ids),
        "validation_row_ids": list(plan.validation_row_ids),
        "purged_row_ids": list(plan.purged_row_ids),
        "group_purged_row_ids": list(plan.group_purged_row_ids),
    }


def _offline_posture() -> dict[str, bool]:
    return {"offline_only": True, "paper": False, "live": False, "broker": False, "oms": False}


def _is_finite_number(value: Any) -> bool:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return False
    return isfinite(parsed)


def _trainable_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "r0",
            "group": "g0",
            "fold": 0,
            "as_of": "2025-01-01T00:00:00",
            "label_window_start": "2025-01-02T00:00:00",
            "label_window_end": "2025-01-03T00:00:00",
            "toy_feature_a": 0.10,
            "toy_feature_b": 0.40,
            "label": 0.15,
        },
        {
            "row_id": "r1",
            "group": "g1",
            "fold": 0,
            "as_of": "2025-01-04T00:00:00",
            "label_window_start": "2025-01-05T00:00:00",
            "label_window_end": "2025-01-06T00:00:00",
            "toy_feature_a": 0.25,
            "toy_feature_b": 0.35,
            "label": 0.30,
        },
        {
            "row_id": "r2",
            "group": "g2",
            "fold": 1,
            "as_of": "2025-02-01T00:00:00",
            "label_window_start": "2025-02-02T00:00:00",
            "label_window_end": "2025-02-03T00:00:00",
            "toy_feature_a": 0.40,
            "toy_feature_b": 0.30,
            "label": 0.42,
        },
        {
            "row_id": "r3",
            "group": "g3",
            "fold": 1,
            "as_of": "2025-02-04T00:00:00",
            "label_window_start": "2025-02-05T00:00:00",
            "label_window_end": "2025-02-06T00:00:00",
            "toy_feature_a": 0.55,
            "toy_feature_b": 0.25,
            "label": 0.55,
        },
        {
            "row_id": "r4",
            "group": "g4",
            "fold": 2,
            "as_of": "2025-03-01T00:00:00",
            "label_window_start": "2025-03-02T00:00:00",
            "label_window_end": "2025-03-03T00:00:00",
            "toy_feature_a": 0.70,
            "toy_feature_b": 0.20,
            "label": 0.68,
        },
        {
            "row_id": "r5",
            "group": "g5",
            "fold": 2,
            "as_of": "2025-03-04T00:00:00",
            "label_window_start": "2025-03-05T00:00:00",
            "label_window_end": "2025-03-06T00:00:00",
            "toy_feature_a": 0.85,
            "toy_feature_b": 0.15,
            "label": 0.82,
        },
    ]


def _scenario_kwargs(scenario: str) -> dict[str, bool]:
    if scenario == "pass":
        return {}
    if scenario == "blocked":
        return {"inject_ood_drift": True}
    raise ModelLifecycleError(f"unknown scenario {scenario!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run toy model lifecycle gate")
    parser.add_argument("--scenario", choices=("pass", "blocked"), default="pass")
    args = parser.parse_args()
    print(json.dumps(run_toy_model_lifecycle_gate(**_scenario_kwargs(args.scenario)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
