import json
import unittest
from pathlib import Path

from code_capsules.e2e_toy_research_flow import run_toy_research_flow


ROOT = Path(__file__).resolve().parents[3]


class ToyResearchFlowTests(unittest.TestCase):
    def test_passed_toy_flow_matches_golden_report(self) -> None:
        result = run_toy_research_flow()
        expected = json.loads((ROOT / "examples" / "toy_e2e_gate_report.json").read_text(encoding="utf-8"))

        self.assertEqual(result, expected)
        self.assertEqual(result["flow_id"], "toy_source_to_oof_gate")
        self.assertEqual(result["label_plan"]["policy"], "source_backed_view")
        self.assertEqual(result["label_plan"]["dense_rows_written"], 0)
        self.assertTrue(result["leakage_report"]["ok"])
        self.assertEqual(result["evidence_gate"]["status"], "pass")
        self.assertEqual(
            result["evidence_gate"]["topological_order"],
            [
                "source_manifest",
                "label_plan",
                "fold_leakage_check",
                "oof_metric_kernel",
                "review_gate",
            ],
        )

    def test_blocked_toy_flow_matches_golden_report(self) -> None:
        result = run_toy_research_flow(inject_leakage_failure=True)
        expected = json.loads((ROOT / "examples" / "toy_e2e_blocked_gate_report.json").read_text(encoding="utf-8"))

        self.assertEqual(result, expected)
        self.assertFalse(result["leakage_report"]["ok"])
        self.assertEqual(result["evidence_gate"]["status"], "block")
        self.assertEqual(result["evidence_gate"]["issues"], [])

    def test_bad_artifact_support_blocks_review_gate(self) -> None:
        result = run_toy_research_flow(inject_bad_artifact_support=True)

        self.assertEqual(result["evidence_gate"]["status"], "block")
        self.assertIn("unknown_supporting_artifact", result["evidence_gate"]["issues"])


if __name__ == "__main__":
    unittest.main()
