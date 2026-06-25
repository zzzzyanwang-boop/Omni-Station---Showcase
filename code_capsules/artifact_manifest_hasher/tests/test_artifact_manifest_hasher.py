import unittest

from code_capsules.artifact_manifest_hasher import (
    ManifestError,
    build_artifact_manifest,
    compare_manifest,
    validate_artifact_support,
)


class ArtifactManifestHasherTests(unittest.TestCase):
    def _manifest(self):
        return build_artifact_manifest(
            "toy.oof.v1",
            schema={"columns": ["score", "label"]},
            rows=[{"score": 0.1, "label": 0.2}],
            lineage={"source": "toy.source.v1"},
        )

    def test_same_content_same_hash(self) -> None:
        left = self._manifest()
        right = build_artifact_manifest(
            "toy.oof.v1",
            schema={"columns": ["score", "label"]},
            rows=[{"label": 0.2, "score": 0.1}],
            lineage={"source": "toy.source.v1"},
        )

        self.assertEqual(left.content_hash, right.content_hash)
        self.assertEqual(compare_manifest(left, right), ())

    def test_schema_change_blocks(self) -> None:
        expected = build_artifact_manifest(
            "toy.oof.v1",
            schema={"columns": ["score", "label"]},
            rows=[{"score": 0.1, "label": 0.2}],
            lineage={"source": "toy.source.v1"},
        )
        observed = build_artifact_manifest(
            "toy.oof.v1",
            schema={"columns": ["score", "label", "fold"]},
            rows=[{"score": 0.1, "label": 0.2}],
            lineage={"source": "toy.source.v1"},
        )

        self.assertIn("schema_hash_mismatch", compare_manifest(expected, observed))

    def test_decision_claim_must_pin_all_hashes(self) -> None:
        manifest = self._manifest()

        with self.assertRaises(ManifestError):
            validate_artifact_support(
                {
                    "scope": "decision_grade",
                    "supported_by": ["toy.oof.v1"],
                    "expected_content_hashes": {"toy.oof.v1": "sha256:stale"},
                },
                {"toy.oof.v1": manifest},
            )

    def test_decision_claim_accepts_exact_schema_content_and_lineage(self) -> None:
        manifest = self._manifest()

        validate_artifact_support(
            {
                "scope": "decision_grade",
                "supported_by": ["toy.oof.v1"],
                "expected_hashes": {
                    "toy.oof.v1": {
                        "schema_hash": manifest.schema_hash,
                        "content_hash": manifest.content_hash,
                        "lineage_hash": manifest.lineage_hash,
                    }
                },
            },
            {"toy.oof.v1": manifest},
        )

    def test_schema_change_blocks_decision_claim_even_when_content_matches(self) -> None:
        manifest = self._manifest()

        with self.assertRaises(ManifestError):
            validate_artifact_support(
                {
                    "scope": "decision_grade",
                    "supported_by": ["toy.oof.v1"],
                    "expected_hashes": {
                        "toy.oof.v1": {
                            "schema_hash": "sha256:stale",
                            "content_hash": manifest.content_hash,
                            "lineage_hash": manifest.lineage_hash,
                        }
                    },
                },
                {"toy.oof.v1": manifest},
            )

    def test_lineage_change_blocks_decision_claim_even_when_content_matches(self) -> None:
        manifest = self._manifest()

        with self.assertRaises(ManifestError):
            validate_artifact_support(
                {
                    "scope": "decision_grade",
                    "supported_by": ["toy.oof.v1"],
                    "expected_hashes": {
                        "toy.oof.v1": {
                            "schema_hash": manifest.schema_hash,
                            "content_hash": manifest.content_hash,
                            "lineage_hash": "sha256:stale",
                        }
                    },
                },
                {"toy.oof.v1": manifest},
            )

    def test_diagnostic_artifact_cannot_support_decision_claim(self) -> None:
        manifest = build_artifact_manifest(
            "toy.diag.v1",
            schema={"columns": ["note"]},
            rows=[{"note": "bounded diagnostic"}],
            lineage={"source": "toy.source.v1"},
            artifact_role="diagnostic",
            diagnostic_only=True,
        )

        with self.assertRaises(ManifestError):
            validate_artifact_support(
                {
                    "scope": "decision_grade",
                    "supported_by": ["toy.diag.v1"],
                    "expected_hashes": {
                        "toy.diag.v1": {
                            "schema_hash": manifest.schema_hash,
                            "content_hash": manifest.content_hash,
                            "lineage_hash": manifest.lineage_hash,
                        }
                    },
                },
                {"toy.diag.v1": manifest},
            )


if __name__ == "__main__":
    unittest.main()
