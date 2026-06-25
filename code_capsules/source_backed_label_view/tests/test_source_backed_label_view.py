import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from source_backed_label_view import LabelPlanError, build_label_view_plan


class SourceBackedLabelViewTests(unittest.TestCase):
    def _fixture(self) -> tuple[dict, dict]:
        payload = json.loads((ROOT / "examples" / "toy_label_plan.json").read_text(encoding="utf-8"))
        return payload["source_manifest"], payload["label_spec"]

    def test_builds_source_backed_plan_with_minimal_projection(self) -> None:
        source_manifest, label_spec = self._fixture()

        plan = build_label_view_plan(source_manifest, label_spec)

        self.assertEqual(plan.materialization_policy, "source_backed_view")
        self.assertEqual(plan.projected_columns, ("trade_date", "symbol", "bar_time", "close"))
        self.assertEqual(plan.estimated_dense_rows_written, 0)
        self.assertIn("defer_row_level_label_materialization", plan.physical_operations)

    def test_can_force_dense_materialization_for_compatibility(self) -> None:
        source_manifest, label_spec = self._fixture()

        plan = build_label_view_plan(source_manifest, label_spec, force_dense=True)

        self.assertEqual(plan.materialization_policy, "dense_materialization")
        self.assertEqual(plan.estimated_dense_rows_written, 1000)

    def test_blocks_missing_required_column(self) -> None:
        source_manifest, label_spec = self._fixture()
        label_spec["required_columns"] = ["missing_column"]

        with self.assertRaises(LabelPlanError):
            build_label_view_plan(source_manifest, label_spec)

    def test_blocks_non_point_in_time_safe_column(self) -> None:
        source_manifest, label_spec = self._fixture()
        source_manifest["columns"].append({"name": "future_close", "point_in_time_safe": False})
        label_spec["required_columns"] = ["future_close"]

        with self.assertRaises(LabelPlanError):
            build_label_view_plan(source_manifest, label_spec)


if __name__ == "__main__":
    unittest.main()
