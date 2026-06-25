import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from oof_metric_kernel import average_ranks, grouped_oof_metrics, rank_ic


class OofMetricKernelTests(unittest.TestCase):
    def test_grouped_metrics_are_computed_per_fold_and_regime(self) -> None:
        rows = json.loads((ROOT / "examples" / "toy_oof_rows.json").read_text(encoding="utf-8"))

        metrics = grouped_oof_metrics(rows, ("fold", "regime"))

        self.assertEqual(len(metrics), 2)
        self.assertEqual(metrics[0]["group"], {"fold": "f1", "regime": "calm"})
        self.assertEqual(metrics[0]["row_count"], 3)
        self.assertGreater(metrics[0]["pearson_ic"], 0.9)
        self.assertEqual(metrics[0]["rank_ic"], 1.0)

    def test_average_ranks_handle_ties(self) -> None:
        self.assertEqual(average_ranks([10.0, 10.0, 30.0]), [1.5, 1.5, 3.0])

    def test_rank_ic_detects_inverse_order(self) -> None:
        self.assertEqual(rank_ic([(1.0, 3.0), (2.0, 2.0), (3.0, 1.0)]), -1.0)

    def test_non_finite_rows_are_skipped(self) -> None:
        rows = [
            {"fold": "f1", "score": 1.0, "label": 1.0},
            {"fold": "f1", "score": "nan", "label": 2.0},
            {"fold": "f1", "score": 3.0, "label": 3.0},
        ]

        metrics = grouped_oof_metrics(rows, ("fold",))

        self.assertEqual(metrics[0]["row_count"], 2)
        self.assertEqual(metrics[0]["skipped_non_finite_rows"], 1)


if __name__ == "__main__":
    unittest.main()
