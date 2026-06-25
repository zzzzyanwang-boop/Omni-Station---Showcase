import unittest

from code_capsules.e2e_toy_research_flow import run_toy_research_flow


class ToyResearchFlowTests(unittest.TestCase):
    def test_toy_flow_reaches_passed_gate(self) -> None:
        result = run_toy_research_flow()

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


if __name__ == "__main__":
    unittest.main()
