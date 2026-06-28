import json
import unittest
from pathlib import Path

from code_capsules.toy_model_lifecycle_gate import run_toy_model_lifecycle_gate


ROOT = Path(__file__).resolve().parents[3]


class ToyModelLifecycleGateTests(unittest.TestCase):
    def test_passed_lifecycle_matches_golden_report(self) -> None:
        result = run_toy_model_lifecycle_gate()
        expected = json.loads((ROOT / "examples" / "toy_model_lifecycle_gate_pass.json").read_text(encoding="utf-8"))

        self.assertEqual(result, expected)
        self.assertEqual(result["eligibility_gate"]["status"], "pass")
        self.assertFalse(result["branch"]["model_card"]["inference_eligible"])

    def test_blocked_lifecycle_matches_golden_report(self) -> None:
        result = run_toy_model_lifecycle_gate(inject_ood_drift=True)
        expected = json.loads((ROOT / "examples" / "toy_model_lifecycle_gate_blocked.json").read_text(encoding="utf-8"))

        self.assertEqual(result, expected)
        self.assertEqual(result["eligibility_gate"]["status"], "block")
        self.assertIn("ood_score_distribution_drift", result["eligibility_gate"]["blockers"])

    def test_stale_trainable_manifest_blocks(self) -> None:
        result = run_toy_model_lifecycle_gate(inject_stale_trainable=True)

        self.assertEqual(result["eligibility_gate"]["status"], "block")
        self.assertIn("stale_trainable_manifest", result["eligibility_gate"]["blockers"])

    def test_missing_fold_row_set_proof_blocks(self) -> None:
        result = run_toy_model_lifecycle_gate(inject_missing_fold_proof=True)

        self.assertEqual(result["eligibility_gate"]["status"], "block")
        self.assertIn("missing_fold_row_set_proof", result["eligibility_gate"]["blockers"])

    def test_non_finite_predictions_block(self) -> None:
        result = run_toy_model_lifecycle_gate(inject_non_finite_prediction=True)

        self.assertEqual(result["eligibility_gate"]["status"], "block")
        self.assertIn("non_finite_prediction", result["eligibility_gate"]["blockers"])
        self.assertEqual(result["branch"]["uncertainty"]["status"], "block")

    def test_missing_calibration_blocks(self) -> None:
        result = run_toy_model_lifecycle_gate(inject_missing_calibration=True)

        self.assertEqual(result["eligibility_gate"]["status"], "block")
        self.assertIn("missing_calibration_report", result["eligibility_gate"]["blockers"])

    def test_proxy_score_artifact_blocks_decision_grade_card(self) -> None:
        result = run_toy_model_lifecycle_gate(inject_proxy_score_artifact=True)

        self.assertEqual(result["eligibility_gate"]["status"], "block")
        self.assertIn("proxy_score_artifact", result["eligibility_gate"]["blockers"])
        self.assertIn("diagnostic_artifact_support", result["eligibility_gate"]["blockers"])

    def test_diagnostic_artifact_cannot_support_model_card(self) -> None:
        result = run_toy_model_lifecycle_gate(inject_diagnostic_model_card_support=True)

        self.assertEqual(result["eligibility_gate"]["status"], "block")
        self.assertIn("diagnostic_support_artifact", result["eligibility_gate"]["blockers"])
        self.assertIn("diagnostic_artifact_support", result["eligibility_gate"]["blockers"])

    def test_prediction_replay_schema_mismatch_blocks(self) -> None:
        result = run_toy_model_lifecycle_gate(inject_replay_schema_mismatch=True)

        self.assertEqual(result["eligibility_gate"]["status"], "block")
        self.assertIn("prediction_replay_schema_mismatch", result["eligibility_gate"]["blockers"])


if __name__ == "__main__":
    unittest.main()
