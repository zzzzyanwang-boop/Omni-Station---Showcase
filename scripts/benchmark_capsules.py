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
    from code_capsules.source_backed_label_view import build_label_view_plan

    label_fixture = json.loads(
        (root / "code_capsules" / "source_backed_label_view" / "examples" / "toy_label_plan.json").read_text(
            encoding="utf-8"
        )
    )
    start = perf_counter()
    label_plan = build_label_view_plan(label_fixture["source_manifest"], label_fixture["label_spec"])
    elapsed_ms = round((perf_counter() - start) * 1000, 3)
    rust_status = _rust_kernel_status(root)
    report = {
        "benchmark_id": "toy_capsule_physical_plan_smoke_v1",
        "ci_policy": "correctness_and_shape_only",
        "projection_width": len(label_plan.projected_columns),
        "source_scan_count": sum(1 for op in label_plan.physical_operations if op.startswith("read_source_projection")),
        "dense_rows_written": label_plan.estimated_dense_rows_written,
        "source_backed_view_rows": label_plan.estimated_view_rows_written,
        "dense_materialization_avoided": label_plan.estimated_dense_rows_written == 0,
        "rust_python_parity": rust_status,
        "bounded_timing_smoke": {
            "elapsed_ms": elapsed_ms,
            "threshold_enforced": False,
            "reason": "timing is recorded for review shape only; CI gates correctness and report schema",
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["dense_materialization_avoided"] and rust_status in {"pass", "skipped_no_cargo"} else 1


def _rust_kernel_status(root: Path) -> str:
    if shutil.which("cargo") is None:
        return "skipped_no_cargo"
    completed = subprocess.run(
        ["cargo", "test", "--manifest-path", "code_capsules/rust_sequence_tensor_kernel/Cargo.toml"],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return "pass" if completed.returncode == 0 else "fail"


if __name__ == "__main__":
    raise SystemExit(main())
