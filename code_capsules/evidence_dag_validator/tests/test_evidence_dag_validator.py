import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evidence_dag_validator import validate_evidence_dag


class EvidenceDagValidatorTests(unittest.TestCase):
    def test_accepts_supported_acyclic_dag(self) -> None:
        packet = json.loads((ROOT / "examples" / "toy_dag.json").read_text(encoding="utf-8"))

        report = validate_evidence_dag(packet)

        self.assertTrue(report.ok, report.issues)
        self.assertEqual(
            report.topological_order,
            ("source_manifest", "trainable_manifest", "oof_gate"),
        )

    def test_blocks_unknown_supporting_artifact(self) -> None:
        packet = json.loads((ROOT / "examples" / "toy_dag.json").read_text(encoding="utf-8"))
        packet["nodes"][2]["claims"][0]["supported_by"] = ["missing.artifact"]

        report = validate_evidence_dag(packet)

        self.assertFalse(report.ok)
        self.assertIn("unknown_supporting_artifact", {issue.code for issue in report.issues})

    def test_blocks_artifact_missing_lineage_hash(self) -> None:
        packet = json.loads((ROOT / "examples" / "toy_dag.json").read_text(encoding="utf-8"))
        del packet["nodes"][1]["artifacts"][0]["lineage_hash"]

        report = validate_evidence_dag(packet)

        self.assertFalse(report.ok)
        self.assertIn("artifact_manifest_incomplete", {issue.code for issue in report.issues})

    def test_detects_cycles(self) -> None:
        packet = {
            "nodes": [
                {"id": "a", "type": "artifact", "depends_on": ["b"], "artifacts": [], "claims": []},
                {"id": "b", "type": "artifact", "depends_on": ["a"], "artifacts": [], "claims": []},
            ]
        }

        report = validate_evidence_dag(packet)

        self.assertFalse(report.ok)
        self.assertIn("cycle_detected", {issue.code for issue in report.issues})

    def test_diagnostic_node_cannot_make_decision_claim(self) -> None:
        packet = {
            "nodes": [
                {
                    "id": "diagnostic",
                    "type": "artifact",
                    "diagnostic_only": True,
                    "depends_on": [],
                    "artifacts": [
                        {
                            "artifact_id": "toy.diagnostic.v1",
                            "schema_hash": "sha256:schema",
                            "content_hash": "sha256:content",
                            "lineage_hash": "sha256:lineage",
                        }
                    ],
                    "claims": [
                        {
                            "claim_id": "overclaim",
                            "scope": "decision_grade",
                            "supported_by": ["toy.diagnostic.v1"],
                        }
                    ],
                }
            ]
        }

        report = validate_evidence_dag(packet)

        self.assertFalse(report.ok)
        self.assertIn("diagnostic_node_decision_claim", {issue.code for issue in report.issues})

    def test_claim_cannot_reference_non_ancestor_artifact(self) -> None:
        packet = {
            "nodes": [
                {
                    "id": "left",
                    "type": "artifact",
                    "depends_on": [],
                    "artifacts": [
                        {
                            "artifact_id": "toy.left.v1",
                            "schema_hash": "sha256:schema-left",
                            "content_hash": "sha256:content-left",
                            "lineage_hash": "sha256:lineage-left",
                        }
                    ],
                    "claims": [],
                },
                {
                    "id": "right",
                    "type": "artifact",
                    "depends_on": [],
                    "artifacts": [
                        {
                            "artifact_id": "toy.right.v1",
                            "schema_hash": "sha256:schema-right",
                            "content_hash": "sha256:content-right",
                            "lineage_hash": "sha256:lineage-right",
                        }
                    ],
                    "claims": [
                        {
                            "claim_id": "bad_cross_edge_claim",
                            "scope": "diagnostic",
                            "supported_by": ["toy.left.v1"],
                        }
                    ],
                },
            ]
        }

        report = validate_evidence_dag(packet)

        self.assertFalse(report.ok)
        self.assertIn("non_ancestor_supporting_artifact", {issue.code for issue in report.issues})

    def test_blocked_gate_cannot_publish_decision_grade_claim(self) -> None:
        packet = {
            "nodes": [
                {
                    "id": "artifact",
                    "type": "artifact",
                    "depends_on": [],
                    "artifacts": [
                        {
                            "artifact_id": "toy.artifact.v1",
                            "schema_hash": "sha256:schema",
                            "content_hash": "sha256:content",
                            "lineage_hash": "sha256:lineage",
                        }
                    ],
                    "claims": [],
                },
                {
                    "id": "blocked_gate",
                    "type": "gate",
                    "depends_on": ["artifact"],
                    "gate_decision": "block",
                    "artifacts": [],
                    "claims": [
                        {
                            "claim_id": "must_not_publish",
                            "scope": "decision_grade",
                            "supported_by": ["toy.artifact.v1"],
                        }
                    ],
                },
            ]
        }

        report = validate_evidence_dag(packet)

        self.assertFalse(report.ok)
        self.assertIn("blocked_gate_with_decision_claim", {issue.code for issue in report.issues})


if __name__ == "__main__":
    unittest.main()
