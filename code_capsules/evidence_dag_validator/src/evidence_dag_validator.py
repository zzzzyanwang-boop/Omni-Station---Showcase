"""Public-safe evidence DAG validation capsule.

The implementation is deliberately small but complete: it validates node
ownership, artifact references, graph acyclicity, and claim support without
depending on any OmniStation private source code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


REQUIRED_ARTIFACT_FIELDS = ("artifact_id", "schema_hash", "content_hash")
DECISION_GRADE = "decision_grade"


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    code: str
    node_id: str | None
    message: str


@dataclass(frozen=True)
class ValidationReport:
    ok: bool
    topological_order: tuple[str, ...]
    issues: tuple[ValidationIssue, ...]


def validate_evidence_dag(packet: dict[str, Any]) -> ValidationReport:
    """Validate a synthetic manifest-bound evidence DAG.

    The validator is fail-closed: any issue with severity ``error`` makes
    ``ok`` false even if some graph portions are otherwise valid.
    """

    issues: list[ValidationIssue] = []
    nodes_raw = packet.get("nodes")
    if not isinstance(nodes_raw, list):
        return ValidationReport(
            ok=False,
            topological_order=(),
            issues=(
                ValidationIssue(
                    "error",
                    "nodes_not_list",
                    None,
                    "packet.nodes must be a list",
                ),
            ),
        )

    nodes: dict[str, dict[str, Any]] = {}
    for index, node in enumerate(nodes_raw):
        if not isinstance(node, dict):
            issues.append(
                ValidationIssue("error", "node_not_object", None, f"node {index} is not an object")
            )
            continue
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id:
            issues.append(
                ValidationIssue("error", "missing_node_id", None, f"node {index} has no id")
            )
            continue
        if node_id in nodes:
            issues.append(
                ValidationIssue("error", "duplicate_node_id", node_id, "node id is duplicated")
            )
            continue
        nodes[node_id] = node

    artifact_owner: dict[str, str] = {}
    for node_id, node in nodes.items():
        _validate_dependencies(node_id, node, nodes, issues)
        _validate_artifacts(node_id, node, artifact_owner, issues)

    order = _topological_order(nodes, issues)
    ancestors = _ancestor_map(nodes)
    for node_id, node in nodes.items():
        _validate_claims(node_id, node, artifact_owner, ancestors, issues)
        _validate_gate(node_id, node, issues)

    return ValidationReport(
        ok=not any(issue.severity == "error" for issue in issues),
        topological_order=tuple(order),
        issues=tuple(issues),
    )


def _validate_dependencies(
    node_id: str,
    node: dict[str, Any],
    nodes: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    depends_on = node.get("depends_on", [])
    if not isinstance(depends_on, list):
        issues.append(
            ValidationIssue("error", "dependencies_not_list", node_id, "depends_on must be a list")
        )
        return
    for dependency in depends_on:
        if not isinstance(dependency, str) or not dependency:
            issues.append(
                ValidationIssue(
                    "error",
                    "invalid_dependency_ref",
                    node_id,
                    "dependency references must be non-empty strings",
                )
            )
        elif dependency not in nodes:
            issues.append(
                ValidationIssue(
                    "error",
                    "missing_dependency",
                    node_id,
                    f"dependency {dependency!r} does not exist",
                )
            )


def _validate_artifacts(
    node_id: str,
    node: dict[str, Any],
    artifact_owner: dict[str, str],
    issues: list[ValidationIssue],
) -> None:
    artifacts = node.get("artifacts", [])
    if not isinstance(artifacts, list):
        issues.append(
            ValidationIssue("error", "artifacts_not_list", node_id, "artifacts must be a list")
        )
        return
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            issues.append(
                ValidationIssue("error", "artifact_not_object", node_id, "artifact is not an object")
            )
            continue
        missing = [field for field in REQUIRED_ARTIFACT_FIELDS if not artifact.get(field)]
        if missing:
            issues.append(
                ValidationIssue(
                    "error",
                    "artifact_manifest_incomplete",
                    node_id,
                    f"artifact is missing required fields: {', '.join(missing)}",
                )
            )
            continue
        artifact_id = str(artifact["artifact_id"])
        if artifact_id in artifact_owner:
            issues.append(
                ValidationIssue(
                    "error",
                    "duplicate_artifact_id",
                    node_id,
                    f"artifact {artifact_id!r} is already produced by {artifact_owner[artifact_id]!r}",
                )
            )
        artifact_owner[artifact_id] = node_id
        if artifact_id.endswith(".latest") or "/latest/" in artifact_id:
            issues.append(
                ValidationIssue(
                    "error",
                    "latest_artifact_ref",
                    node_id,
                    "decision-grade manifests must not rely on latest-style artifact ids",
                )
            )


def _validate_claims(
    node_id: str,
    node: dict[str, Any],
    artifact_owner: dict[str, str],
    ancestors: dict[str, set[str]],
    issues: list[ValidationIssue],
) -> None:
    claims = node.get("claims", [])
    if not isinstance(claims, list):
        issues.append(ValidationIssue("error", "claims_not_list", node_id, "claims must be a list"))
        return
    diagnostic_only = bool(node.get("diagnostic_only"))
    for claim in claims:
        if not isinstance(claim, dict):
            issues.append(ValidationIssue("error", "claim_not_object", node_id, "claim is not an object"))
            continue
        claim_id = claim.get("claim_id")
        supported_by = claim.get("supported_by", [])
        scope = claim.get("scope", "diagnostic")
        if not isinstance(claim_id, str) or not claim_id:
            issues.append(ValidationIssue("error", "missing_claim_id", node_id, "claim has no id"))
        if scope == DECISION_GRADE and diagnostic_only:
            issues.append(
                ValidationIssue(
                    "error",
                    "diagnostic_node_decision_claim",
                    node_id,
                    "diagnostic-only nodes cannot make decision-grade claims",
                )
            )
        if not isinstance(supported_by, list) or not supported_by:
            issues.append(
                ValidationIssue(
                    "error",
                    "claim_without_support",
                    node_id,
                    f"claim {claim_id!r} has no supporting artifacts",
                )
            )
            continue
        for artifact_id in supported_by:
            if artifact_id not in artifact_owner:
                issues.append(
                    ValidationIssue(
                        "error",
                        "unknown_supporting_artifact",
                        node_id,
                        f"claim {claim_id!r} references unknown artifact {artifact_id!r}",
                    )
                )
                continue
            owner = artifact_owner[artifact_id]
            if owner != node_id and owner not in ancestors.get(node_id, set()):
                issues.append(
                    ValidationIssue(
                        "error",
                        "non_ancestor_supporting_artifact",
                        node_id,
                        f"claim {claim_id!r} references artifact {artifact_id!r} from non-ancestor node {owner!r}",
                    )
                )


def _validate_gate(node_id: str, node: dict[str, Any], issues: list[ValidationIssue]) -> None:
    if node.get("type") != "gate":
        return
    decision = node.get("gate_decision")
    if decision not in {"pass", "block"}:
        issues.append(
            ValidationIssue(
                "error",
                "invalid_gate_decision",
                node_id,
                "gate_decision must be pass or block",
            )
        )
    if decision == "pass":
        has_decision_claim = any(
            isinstance(claim, dict) and claim.get("scope") == DECISION_GRADE
            for claim in node.get("claims", [])
        )
        if not has_decision_claim:
            issues.append(
                ValidationIssue(
                    "error",
                    "passing_gate_without_decision_claim",
                    node_id,
                    "passing gates must publish at least one supported decision-grade claim",
                )
            )


def _topological_order(
    nodes: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> list[str]:
    inbound_count = {node_id: 0 for node_id in nodes}
    outgoing: dict[str, list[str]] = {node_id: [] for node_id in nodes}

    for node_id, node in nodes.items():
        for dependency in _string_refs(node.get("depends_on", [])):
            if dependency not in nodes:
                continue
            inbound_count[node_id] += 1
            outgoing[dependency].append(node_id)

    ready = sorted(node_id for node_id, count in inbound_count.items() if count == 0)
    order: list[str] = []
    while ready:
        node_id = ready.pop(0)
        order.append(node_id)
        for child in sorted(outgoing[node_id]):
            inbound_count[child] -= 1
            if inbound_count[child] == 0:
                ready.append(child)
        ready.sort()

    if len(order) != len(nodes):
        cyclic = sorted(node_id for node_id, count in inbound_count.items() if count > 0)
        issues.append(
            ValidationIssue(
                "error",
                "cycle_detected",
                None,
                f"graph contains a cycle involving: {', '.join(cyclic)}",
            )
        )
    return order


def _ancestor_map(nodes: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    ancestors: dict[str, set[str]] = {node_id: set() for node_id in nodes}

    def visit(node_id: str, stack: set[str]) -> set[str]:
        if node_id in stack:
            return set()
        if ancestors[node_id]:
            return ancestors[node_id]
        stack.add(node_id)
        collected: set[str] = set()
        for dependency in _string_refs(nodes[node_id].get("depends_on", [])):
            if dependency not in nodes:
                continue
            collected.add(dependency)
            collected.update(visit(dependency, stack))
        stack.remove(node_id)
        ancestors[node_id] = collected
        return collected

    for node_id in nodes:
        visit(node_id, set())
    return ancestors


def _string_refs(value: Any) -> Iterable[str]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str))
