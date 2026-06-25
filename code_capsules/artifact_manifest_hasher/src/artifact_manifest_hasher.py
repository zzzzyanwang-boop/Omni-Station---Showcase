"""Public-safe artifact manifest hashing capsule."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ArtifactManifest:
    artifact_id: str
    schema_hash: str
    content_hash: str
    lineage_hash: str
    artifact_role: str
    diagnostic_only: bool


class ManifestError(ValueError):
    """Raised when an artifact manifest or claim support is unsafe."""


def build_artifact_manifest(
    artifact_id: str,
    *,
    schema: dict[str, Any],
    rows: list[dict[str, Any]],
    lineage: dict[str, Any],
    artifact_role: str = "decision",
    diagnostic_only: bool = False,
) -> ArtifactManifest:
    """Build a deterministic manifest for synthetic artifact metadata."""

    if not artifact_id:
        raise ManifestError("artifact_id must be non-empty")
    if artifact_role not in {"decision", "diagnostic"}:
        raise ManifestError("artifact_role must be decision or diagnostic")
    return ArtifactManifest(
        artifact_id=artifact_id,
        schema_hash=_hash_payload(schema),
        content_hash=_hash_payload(rows),
        lineage_hash=_hash_payload(lineage),
        artifact_role=artifact_role,
        diagnostic_only=diagnostic_only,
    )


def compare_manifest(expected: ArtifactManifest, observed: ArtifactManifest) -> tuple[str, ...]:
    """Return mismatch codes between expected and observed manifests."""

    mismatches: list[str] = []
    if expected.artifact_id != observed.artifact_id:
        mismatches.append("artifact_id_mismatch")
    if expected.schema_hash != observed.schema_hash:
        mismatches.append("schema_hash_mismatch")
    if expected.content_hash != observed.content_hash:
        mismatches.append("content_hash_mismatch")
    if expected.lineage_hash != observed.lineage_hash:
        mismatches.append("lineage_hash_mismatch")
    if expected.diagnostic_only != observed.diagnostic_only:
        mismatches.append("diagnostic_policy_mismatch")
    return tuple(mismatches)


def validate_artifact_support(claim: dict[str, Any], manifests: dict[str, ArtifactManifest]) -> None:
    """Fail closed if claim support is missing, stale, or diagnostic-only."""

    scope = claim.get("scope")
    supporting_ids = claim.get("supported_by")
    expected_hashes = claim.get("expected_content_hashes", {})
    if scope not in {"diagnostic", "decision_grade"}:
        raise ManifestError("claim scope must be diagnostic or decision_grade")
    if not isinstance(supporting_ids, list) or not supporting_ids:
        raise ManifestError("claim must declare supported_by artifact ids")
    if not isinstance(expected_hashes, dict):
        raise ManifestError("expected_content_hashes must be a mapping when provided")
    for artifact_id in supporting_ids:
        if not isinstance(artifact_id, str) or not artifact_id:
            raise ManifestError("supported_by must contain non-empty artifact ids")
        manifest = manifests.get(artifact_id)
        if manifest is None:
            raise ManifestError(f"missing supporting artifact {artifact_id!r}")
        expected_hash = expected_hashes.get(artifact_id)
        if expected_hash is not None and expected_hash != manifest.content_hash:
            raise ManifestError(f"stale supporting artifact {artifact_id!r}")
        if scope == "decision_grade" and (manifest.diagnostic_only or manifest.artifact_role != "decision"):
            raise ManifestError(f"diagnostic artifact {artifact_id!r} cannot support decision-grade claim")


def _hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()

