"""Executable public-safe toy research flow."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from code_capsules.evidence_dag_validator import validate_evidence_dag
from code_capsules.leakage_fold_checker import validate_rows
from code_capsules.oof_metric_kernel import grouped_oof_metrics
from code_capsules.source_backed_label_view import build_label_view_plan


ROOT = Path(__file__).resolve().parents[2]


def run_toy_research_flow() -> dict[str, Any]:
    label_fixture = _load_json(ROOT / "source_backed_label_view" / "examples" / "toy_label_plan.json")
    label_plan = build_label_view_plan(label_fixture["source_manifest"], label_fixture["label_spec"])

    fold_rows = _load_json(ROOT / "leakage_fold_checker" / "examples" / "toy_rows.json")
    leakage_report = validate_rows(fold_rows, embargo_seconds=24 * 60 * 60)

    oof_rows = _load_json(ROOT / "oof_metric_kernel" / "examples" / "toy_oof_rows.json")
    oof_metrics = grouped_oof_metrics(oof_rows, ("fold", "regime"))

    dag_packet = _build_evidence_packet(
        label_plan_ok=label_plan.materialization_policy == "source_backed_view",
        leakage_ok=leakage_report.ok,
        oof_group_count=len(oof_metrics),
    )
    dag_report = validate_evidence_dag(dag_packet)
    gate_status = "pass" if dag_report.ok and leakage_report.ok and oof_metrics else "block"

    return {
        "flow_id": "toy_source_to_oof_gate",
        "label_plan": {
            "label_id": label_plan.label_id,
            "policy": label_plan.materialization_policy,
            "projected_columns": list(label_plan.projected_columns),
            "dense_rows_written": label_plan.estimated_dense_rows_written,
            "view_rows_written": label_plan.estimated_view_rows_written,
        },
        "leakage_report": {
            "ok": leakage_report.ok,
            "issues": [issue.code for issue in leakage_report.issues],
        },
        "oof_metrics": oof_metrics,
        "evidence_gate": {
            "status": gate_status,
            "topological_order": list(dag_report.topological_order),
            "issues": [issue.code for issue in dag_report.issues],
        },
    }


def _build_evidence_packet(label_plan_ok: bool, leakage_ok: bool, oof_group_count: int) -> dict[str, Any]:
    gate_decision = "pass" if label_plan_ok and leakage_ok and oof_group_count > 0 else "block"
    return {
        "nodes": [
            {
                "id": "source_manifest",
                "type": "source",
                "depends_on": [],
                "artifacts": [_artifact("toy.source_manifest.v1")],
                "claims": [],
            },
            {
                "id": "label_plan",
                "type": "artifact",
                "depends_on": ["source_manifest"],
                "artifacts": [_artifact("toy.label_plan.v1")],
                "claims": [
                    {
                        "claim_id": "label_view_is_source_backed",
                        "scope": "diagnostic",
                        "supported_by": ["toy.source_manifest.v1", "toy.label_plan.v1"],
                    }
                ],
            },
            {
                "id": "fold_leakage_check",
                "type": "gate",
                "depends_on": ["label_plan"],
                "gate_decision": "pass" if leakage_ok else "block",
                "artifacts": [_artifact("toy.leakage_report.v1")],
                "claims": [
                    {
                        "claim_id": "toy_rows_pass_pit_and_embargo",
                        "scope": "decision_grade",
                        "supported_by": ["toy.label_plan.v1", "toy.leakage_report.v1"],
                    }
                ],
            },
            {
                "id": "oof_metric_kernel",
                "type": "artifact",
                "depends_on": ["fold_leakage_check"],
                "artifacts": [_artifact("toy.oof_metrics.v1")],
                "claims": [
                    {
                        "claim_id": "toy_oof_metrics_available",
                        "scope": "diagnostic",
                        "supported_by": ["toy.oof_metrics.v1", "toy.leakage_report.v1"],
                    }
                ],
            },
            {
                "id": "review_gate",
                "type": "gate",
                "depends_on": ["oof_metric_kernel"],
                "gate_decision": gate_decision,
                "artifacts": [],
                "claims": [
                    {
                        "claim_id": "toy_flow_reviewable",
                        "scope": "decision_grade",
                        "supported_by": [
                            "toy.source_manifest.v1",
                            "toy.label_plan.v1",
                            "toy.leakage_report.v1",
                            "toy.oof_metrics.v1",
                        ],
                    }
                ],
            },
        ]
    }


def _artifact(artifact_id: str) -> dict[str, str]:
    safe_name = artifact_id.replace(".", "-")
    return {
        "artifact_id": artifact_id,
        "schema_hash": f"sha256:{safe_name}-schema",
        "content_hash": f"sha256:{safe_name}-content",
    }


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(run_toy_research_flow(), indent=2, sort_keys=True))
