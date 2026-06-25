import unittest

from code_capsules.purged_cpcv_splitter import (
    SplitPlan,
    SplitPlanError,
    build_purged_cpcv_splits,
    validate_split_plan,
)


def _rows() -> list[dict]:
    return [
        {"row_id": "r0", "group": "A", "fold": 0, "as_of": "2025-01-01T00:00:00", "label_window_start": "2025-01-02T00:00:00", "label_window_end": "2025-01-03T00:00:00"},
        {"row_id": "r1", "group": "B", "fold": 0, "as_of": "2025-01-04T00:00:00", "label_window_start": "2025-01-05T00:00:00", "label_window_end": "2025-01-06T00:00:00"},
        {"row_id": "r2", "group": "C", "fold": 1, "as_of": "2025-02-01T00:00:00", "label_window_start": "2025-02-02T00:00:00", "label_window_end": "2025-02-03T00:00:00"},
        {"row_id": "r3", "group": "D", "fold": 1, "as_of": "2025-02-04T00:00:00", "label_window_start": "2025-02-05T00:00:00", "label_window_end": "2025-02-06T00:00:00"},
        {"row_id": "r4", "group": "E", "fold": 2, "as_of": "2025-03-01T00:00:00", "label_window_start": "2025-03-02T00:00:00", "label_window_end": "2025-03-03T00:00:00"},
        {"row_id": "r5", "group": "F", "fold": 2, "as_of": "2025-03-04T00:00:00", "label_window_start": "2025-03-05T00:00:00", "label_window_end": "2025-03-06T00:00:00"},
        {"row_id": "r6", "group": "G", "fold": 3, "as_of": "2025-04-01T00:00:00", "label_window_start": "2025-04-02T00:00:00", "label_window_end": "2025-04-03T00:00:00"},
        {"row_id": "r7", "group": "H", "fold": 3, "as_of": "2025-04-04T00:00:00", "label_window_start": "2025-04-05T00:00:00", "label_window_end": "2025-04-06T00:00:00"},
    ]


class PurgedCpcvSplitterTests(unittest.TestCase):
    def test_cpcv_combination_count(self) -> None:
        plans = build_purged_cpcv_splits(
            _rows(),
            fold_count=4,
            validation_fold_count=2,
            embargo_seconds=24 * 60 * 60,
        )

        self.assertEqual(len(plans), 6)
        self.assertTrue(all(plan.train_row_ids for plan in plans))

    def test_valid_split_has_no_overlap(self) -> None:
        plans = build_purged_cpcv_splits(
            _rows(),
            fold_count=4,
            validation_fold_count=1,
            embargo_seconds=24 * 60 * 60,
        )

        validate_split_plan(plans[0], rows=_rows(), embargo_seconds=24 * 60 * 60)

    def test_group_leakage_blocks_manual_plan(self) -> None:
        plan = SplitPlan(
            split_id="bad_group",
            path_key="folds:1",
            validation_folds=(1,),
            train_row_ids=("r0",),
            validation_row_ids=("r2",),
            purged_row_ids=(),
            group_purged_row_ids=(),
        )
        rows = _rows()
        rows[0]["group"] = "C"

        with self.assertRaises(SplitPlanError):
            validate_split_plan(plan, rows=rows, embargo_seconds=0)

    def test_embargo_violation_blocks_manual_plan(self) -> None:
        plan = SplitPlan(
            split_id="bad_embargo",
            path_key="folds:1",
            validation_folds=(1,),
            train_row_ids=("r0",),
            validation_row_ids=("r2",),
            purged_row_ids=(),
            group_purged_row_ids=(),
        )
        rows = _rows()
        rows[0]["label_window_start"] = "2025-02-01T12:00:00"
        rows[0]["label_window_end"] = "2025-02-02T12:00:00"

        with self.assertRaises(SplitPlanError):
            validate_split_plan(plan, rows=rows, embargo_seconds=24 * 60 * 60)

    def test_duplicate_row_id_blocks(self) -> None:
        rows = _rows()
        rows[1]["row_id"] = "r0"

        with self.assertRaises(SplitPlanError):
            build_purged_cpcv_splits(rows, fold_count=4, validation_fold_count=1, embargo_seconds=0)

    def test_missing_fold_blocks(self) -> None:
        rows = _rows()
        rows = [row for row in rows if row["fold"] != 3]

        with self.assertRaises(SplitPlanError):
            build_purged_cpcv_splits(rows, fold_count=4, validation_fold_count=1, embargo_seconds=0)

    def test_mixed_timezone_policy_blocks(self) -> None:
        rows = _rows()
        rows[0]["as_of"] = "2025-01-01T00:00:00Z"

        with self.assertRaises(SplitPlanError):
            build_purged_cpcv_splits(rows, fold_count=4, validation_fold_count=1, embargo_seconds=0)


if __name__ == "__main__":
    unittest.main()
