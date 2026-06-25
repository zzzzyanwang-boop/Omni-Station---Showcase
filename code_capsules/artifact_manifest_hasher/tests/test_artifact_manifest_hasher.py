import unittest

from code_capsules.artifact_manifest_hasher import (
    ManifestError,
    build_artifact_manifest,
    compare_manifest,
    validate_artifact_support,
)


class ArtifactManifestHasherTests(unittest.TestCase):
    def test_same_content_same_hash(self) -> None:
        left = build_artifact_manifest(
            "toy.oof.v1",
            schema={"columns": ["score", "label"]},
            rows=[{"score": 0.1, "label": 0.2}],
            lineage={"source": "toy.source.v1"},
        )
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

    def test_content_change_blocks_stale_claim(self) -> None:
        manifest = build_artifact_manifest(
            "toy.oof.v1",
            schema={"columns": ["score", "label"]},
            rows=[{"score": 0.1, "label": 0.2}],
            lineage={"source": "toy.source.v1"},
        )

        with self.assertRaises(ManifestError):
            validate_artifact_support(
                {
                    "scope": "decision_grade",
                    "supported_by": ["toy.oof.v1"],
                    "expected_content_hashes": {"toy.oof.v1": "sha256:stale"},
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
                {"scope": "decision_grade", "supported_by": ["toy.diag.v1"]},
                {"toy.diag.v1": manifest},
            )


if __name__ == "__main__":
    unittest.main()

