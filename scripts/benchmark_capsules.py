"""Build a lightweight public-safe physical-plan proof for code capsules."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from time import perf_counter


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    from code_capsules.oof_metric_kernel import grouped_oof_metrics
    from code_capsules.purged_cpcv_splitter import build_purged_cpcv_splits
    from code_capsules.source_backed_label_view import build_label_view_plan
    from code_capsules.source_joinability_gate import check_source_joinability

    label_fixture = json.loads(
        (root / "code_capsules" / "source_backed_label_view" / "examples" / "toy_label_plan.json").read_text(
            encoding="utf-8"
        )
    )
    start = perf_counter()
    label_plan = build_label_view_plan(label_fixture["source_manifest"], label_fixture["label_spec"])
    dense_plan = build_label_view_plan(label_fixture["source_manifest"], label_fixture["label_spec"], force_dense=True)
    oof_rows = json.loads(
        (root / "code_capsules" / "oof_metric_kernel" / "examples" / "toy_oof_rows.json").read_text(encoding="utf-8")
    )
    oof_metrics = grouped_oof_metrics(oof_rows, ("fold", "regime"))
    cpcv_plans = build_purged_cpcv_splits(
        _cpcv_rows(),
        fold_count=4,
        validation_fold_count=2,
        embargo_seconds=24 * 60 * 60,
    )
    cpcv_group_purge_plans = build_purged_cpcv_splits(
        _cpcv_group_purge_rows(),
        fold_count=4,
        validation_fold_count=1,
        embargo_seconds=0,
    )
    cpcv_time_purge_plans = build_purged_cpcv_splits(
        _cpcv_time_purge_rows(),
        fold_count=4,
        validation_fold_count=1,
        embargo_seconds=0,
    )
    joinability = check_source_joinability(
        [_left_part()],
        [_right_part()],
        expected_left_dataset_id="toy.bars",
        expected_right_dataset_id="toy.tbbo",
    )
    rejected_joinability = check_source_joinability(
        [_left_part(dataset_id="toy.other_bars")],
        [_right_part()],
        expected_left_dataset_id="toy.bars",
        expected_right_dataset_id="toy.tbbo",
    )
    elapsed_ms = round((perf_counter() - start) * 1000, 3)
    rust_status = _cargo_manifest_status(root, "code_capsules/rust_sequence_tensor_kernel/Cargo.toml")
    rust_boundary_status = _cargo_manifest_status(root, "code_capsules/rust_native_boundary_proofs/Cargo.toml")
    report = {
        "benchmark_id": "toy_capsule_physical_plan_proof_v2",
        "ci_policy": "correctness_and_shape_only",
        "source_backed_label_plan": {
            "projection_width": len(label_plan.projected_columns),
            "source_scan_count": _scan_count(label_plan.physical_operations),
            "dense_rows_written": label_plan.estimated_dense_rows_written,
            "source_backed_view_rows": label_plan.estimated_view_rows_written,
        },
        "dense_label_baseline": {
            "projection_width": len(dense_plan.projected_columns),
            "source_scan_count": _scan_count(dense_plan.physical_operations),
            "dense_rows_written": dense_plan.estimated_dense_rows_written,
        },
        "physical_delta": {
            "avoided_dense_rows": dense_plan.estimated_dense_rows_written - label_plan.estimated_dense_rows_written,
            "dense_materialization_avoided": label_plan.estimated_dense_rows_written == 0,
            "extra_source_scans": _scan_count(label_plan.physical_operations) - _scan_count(dense_plan.physical_operations),
        },
        "capsule_coverage": {
            "cpcv_split_count": len(cpcv_plans),
            "cpcv_group_purged_rows": sum(len(plan.group_purged_row_ids) for plan in cpcv_group_purge_plans),
            "cpcv_time_purged_rows": sum(len(plan.purged_row_ids) for plan in cpcv_time_purge_plans),
            "joinability_pair_count": len(joinability.joinable_pairs),
            "joinability_reject_count": len(rejected_joinability.issues),
            "oof_group_count": len(oof_metrics),
        },
        "rust_python_parity": rust_status,
        "rust_native_boundary_proofs": rust_boundary_status,
        "bounded_timing_smoke": {
            "elapsed_ms": elapsed_ms,
            "threshold_enforced": False,
            "reason": "timing is recorded for review shape only; CI gates correctness and report schema",
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    rust_ok = rust_status in {"pass", "skipped_no_cargo"} and rust_boundary_status in {"pass", "skipped_no_cargo"}
    return 0 if report["physical_delta"]["dense_materialization_avoided"] and rust_ok else 1


def _scan_count(operations: tuple[str, ...]) -> int:
    return sum(1 for op in operations if op.startswith("read_source_projection"))


def _cargo_manifest_status(root: Path, manifest_path: str) -> str:
    if shutil.which("cargo") is None:
        return "skipped_no_cargo"
    completed = subprocess.run(
        ["cargo", "test", "--manifest-path", manifest_path],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return "pass" if completed.returncode == 0 else "fail"


def _cpcv_rows() -> list[dict[str, object]]:
    return [
        {
            "row_id": f"r{index}",
            "group": f"G{index}",
            "fold": index // 2,
            "as_of": f"2025-0{index // 2 + 1}-01T00:00:00",
            "label_window_start": f"2025-0{index // 2 + 1}-02T00:00:00",
            "label_window_end": f"2025-0{index // 2 + 1}-03T00:00:00",
        }
        for index in range(8)
    ]


def _cpcv_group_purge_rows() -> list[dict[str, object]]:
    return [
        _cpcv_row("g0_a", "A", 0, "2025-01-01"),
        _cpcv_row("g0_b", "B", 0, "2025-01-04"),
        _cpcv_row("g1_a", "A", 1, "2025-02-01"),
        _cpcv_row("g1_c", "C", 1, "2025-02-04"),
        _cpcv_row("g2_d", "D", 2, "2025-03-01"),
        _cpcv_row("g2_e", "E", 2, "2025-03-04"),
        _cpcv_row("g3_f", "F", 3, "2025-04-01"),
        _cpcv_row("g3_g", "G", 3, "2025-04-04"),
    ]


def _cpcv_time_purge_rows() -> list[dict[str, object]]:
    return [
        _cpcv_row("t0_a", "A", 0, "2025-01-01"),
        _cpcv_row("t0_b", "B", 0, "2025-01-04"),
        _cpcv_row("t1_c", "C", 1, "2025-01-01"),
        _cpcv_row("t1_d", "D", 1, "2025-01-04"),
        _cpcv_row("t2_e", "E", 2, "2025-03-01"),
        _cpcv_row("t2_f", "F", 2, "2025-03-04"),
        _cpcv_row("t3_g", "G", 3, "2025-04-01"),
        _cpcv_row("t3_h", "H", 3, "2025-04-04"),
    ]


def _cpcv_row(row_id: str, group: str, fold: int, date: str) -> dict[str, object]:
    return {
        "row_id": row_id,
        "group": group,
        "fold": fold,
        "as_of": f"{date}T00:00:00",
        "label_window_start": f"{date}T12:00:00",
        "label_window_end": f"{date}T23:00:00",
    }


def _left_part(**overrides: object) -> dict[str, object]:
    part = {
        "part_id": "bars_p0",
        "dataset_id": "toy.bars",
        "publisher": "toy_publisher",
        "date": "2025-01-02",
        "symbol_start": "A",
        "symbol_end": "M",
        "time_start": "2025-01-02T14:30:00",
        "time_end": "2025-01-02T21:00:00",
        "row_count": 100,
    }
    part.update(overrides)
    return part


def _right_part(**overrides: object) -> dict[str, object]:
    part = {
        "part_id": "tbbo_p0",
        "dataset_id": "toy.tbbo",
        "publisher": "toy_publisher",
        "date": "2025-01-02",
        "symbol_start": "C",
        "symbol_end": "Z",
        "time_start": "2025-01-02T15:00:00",
        "time_end": "2025-01-02T20:00:00",
        "row_count": 200,
    }
    part.update(overrides)
    return part


if __name__ == "__main__":
    raise SystemExit(main())
