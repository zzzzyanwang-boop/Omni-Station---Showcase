import unittest

from code_capsules.source_joinability_gate import check_source_joinability


def _left_part(**overrides):
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


def _right_part(**overrides):
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


class SourceJoinabilityGateTests(unittest.TestCase):
    def test_part_overlap_passes(self) -> None:
        report = check_source_joinability([_left_part()], [_right_part()])

        self.assertTrue(report.ok)
        self.assertEqual(report.joinable_pairs, (("bars_p0", "tbbo_p0"),))

    def test_date_only_match_does_not_pass(self) -> None:
        report = check_source_joinability(
            [_left_part(symbol_start="A", symbol_end="B")],
            [_right_part(symbol_start="C", symbol_end="D")],
        )

        self.assertFalse(report.ok)
        self.assertIn("date_only_match_without_part_overlap:bars_p0", report.issues)

    def test_symbol_range_gap_blocks(self) -> None:
        report = check_source_joinability(
            [_left_part(symbol_start="A", symbol_end="B")],
            [_right_part(symbol_start="Y", symbol_end="Z")],
        )

        self.assertFalse(report.ok)

    def test_row_count_proof_required(self) -> None:
        report = check_source_joinability([_left_part(row_count=0)], [_right_part()])

        self.assertFalse(report.ok)
        self.assertIn("missing_row_count_proof:bars_p0:tbbo_p0", report.issues)

    def test_publisher_mismatch_blocks(self) -> None:
        report = check_source_joinability([_left_part()], [_right_part(publisher="other")])

        self.assertFalse(report.ok)
        self.assertIn("publisher_mismatch:bars_p0:tbbo_p0", report.issues)

    def test_timezone_policy_mismatch_blocks(self) -> None:
        report = check_source_joinability(
            [_left_part()],
            [_right_part(time_start="2025-01-02T15:00:00Z", time_end="2025-01-02T20:00:00Z")],
        )

        self.assertFalse(report.ok)
        self.assertIn("timezone_policy_mismatch:bars_p0:tbbo_p0", report.issues)

    def test_symbol_ranges_are_normalized_before_overlap(self) -> None:
        report = check_source_joinability([_left_part(symbol_start="a", symbol_end="m")], [_right_part()])

        self.assertTrue(report.ok)


if __name__ == "__main__":
    unittest.main()
