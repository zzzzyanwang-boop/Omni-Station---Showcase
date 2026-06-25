import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from leakage_fold_checker import validate_rows


class LeakageFoldCheckerTests(unittest.TestCase):
    def test_accepts_point_in_time_rows_with_embargo(self) -> None:
        rows = json.loads((ROOT / "examples" / "toy_rows.json").read_text(encoding="utf-8"))

        report = validate_rows(rows, embargo_seconds=24 * 60 * 60)

        self.assertTrue(report.ok, report.issues)

    def test_blocks_future_feature(self) -> None:
        rows = json.loads((ROOT / "examples" / "toy_rows.json").read_text(encoding="utf-8"))
        rows[0]["feature_available_at"] = "2025-01-04T16:00:00"

        report = validate_rows(rows)

        self.assertFalse(report.ok)
        self.assertIn("future_feature", {issue.code for issue in report.issues})

    def test_blocks_fold_embargo_overlap(self) -> None:
        rows = json.loads((ROOT / "examples" / "toy_rows.json").read_text(encoding="utf-8"))
        rows[0]["label_window_end"] = "2025-01-08T16:00:00"

        report = validate_rows(rows, embargo_seconds=1)

        self.assertFalse(report.ok)
        self.assertIn("fold_embargo_violation", {issue.code for issue in report.issues})

    def test_blocks_backward_label_window(self) -> None:
        rows = json.loads((ROOT / "examples" / "toy_rows.json").read_text(encoding="utf-8"))
        rows[1]["label_window_start"] = "2025-01-08T15:59:59"

        report = validate_rows(rows)

        self.assertFalse(report.ok)
        self.assertIn("backward_label_window", {issue.code for issue in report.issues})

    def test_mixed_timezone_policy_returns_issue_not_exception(self) -> None:
        rows = json.loads((ROOT / "examples" / "toy_rows.json").read_text(encoding="utf-8"))
        rows[0]["as_of"] = "2025-01-03T16:00:00Z"

        report = validate_rows(rows)

        self.assertFalse(report.ok)
        self.assertIn("mixed_timestamp_timezone_policy", {issue.code for issue in report.issues})

    def test_fold_timezone_mismatch_returns_issue_not_exception(self) -> None:
        rows = json.loads((ROOT / "examples" / "toy_rows.json").read_text(encoding="utf-8"))
        for field in ("as_of", "feature_available_at", "label_window_start", "label_window_end"):
            rows[1][field] = rows[1][field] + "+00:00"

        report = validate_rows(rows)

        self.assertFalse(report.ok)
        self.assertIn("fold_timezone_policy_mismatch", {issue.code for issue in report.issues})


if __name__ == "__main__":
    unittest.main()
