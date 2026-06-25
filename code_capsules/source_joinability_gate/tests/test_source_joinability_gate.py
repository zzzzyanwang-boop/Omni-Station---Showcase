import unittest

from code_capsules.source_joinability_gate import check_source_joinability


def _left_part(**overrides):
    part = {
        "part_id": "bars_p0",
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


if __name__ == "__main__":
    unittest.main()

