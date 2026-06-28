"""Verify the public showcase repository.

This script is intentionally dependency-light so a technical reviewer can run
the same checks locally that CI runs: tests, path references, redaction scans,
and repository hygiene checks.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


def sensitive_patterns() -> tuple[str, ...]:
    """Build redaction patterns without embedding the target strings verbatim."""

    return (
        "D:" + r"\\",
        "C:" + r"\\",
        "_" + "codex" + "_out",
        "202606" + "22_",
        "797" + "dee",
        "13278" + "443651",
        "25419" + "59529",
        "515" + ",461",
        "41,309" + ",936",
        "82,619" + ",872",
        "30" + r"\.576",
        "19" + r"\.247",
        "8" + r"\.316",
        "1" + r"\.030",
        "full_market_source_label_panel_" + "source_view_hi290",
        "candidate_discovery_rust_fused_" + "projection_label_v10",
        "c4" + "bbbfc7",
        "runtime" + " roots",
        "run" + " roots",
        "file" + " roots",
        "artifact" + " roots",
        "launch" + " hashes",
        "202606" + "20",
        "262" + "_144",
        "4" + "_096",
        "sequence_tensor_native_kernel_" + "rust_pyo3_v1",
        "inter" + "view",
        "recruit" + "ing",
        "hir" + "ing",
        "car" + "eer",
        r"\b" + "J" + "D" + r"\b",
        "面" + "试",
        "简" + "历",
        "岗" + "位",
        "private" + " system",
        "private" + " repository",
        "private" + " implementation",
        "private" + " research",
        "not" + " published",
    )

FORBIDDEN_TRACKED_PARTS = (
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "target",
    "node_modules",
    ".venv",
    "dist",
    "build",
)

FORBIDDEN_TRACKED_NAMES = (
    ".env",
    ".env.local",
    ".env.production",
    ".npmrc",
    ".pypirc",
    "credentials.json",
    "secrets.json",
    "token.json",
    "id_rsa",
    "id_ed25519",
    "known_hosts",
)

FORBIDDEN_TRACKED_SUFFIXES = (
    ".pyc",
    ".pyo",
    ".pyd",
    ".parquet",
    ".feather",
    ".duckdb",
    ".sqlite",
    ".db",
    ".csv",
    ".zip",
    ".7z",
    ".tar",
    ".gz",
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".token",
    ".secret",
    ".pkl",
    ".pickle",
    ".onnx",
    ".pt",
    ".pth",
    ".ckpt",
)

EXPECTED_COUNTS = {
    "source_files": 831,
    "redacted_files": 39,
    "skeleton_readmes": 55,
    "docs_files": 36,
    "examples_files": 30,
    "pseudocode_files": 12,
    "diagram_files": 8,
    "code_capsule_roots": 11,
}

COUNT_REFERENCE_SPECS = (
    ("README.md", "source_files", r"-\s+(\d+)\s+source-shaped module placeholders"),
    ("README.md", "redacted_files", r"-\s+(\d+)\s+sanitized capability placeholders"),
    ("README.md", "skeleton_readmes", r"-\s+(\d+)\s+five-layer skeleton README nodes"),
    ("README.md", "docs_files", r"-\s+(\d+)\s+architecture and flow documents"),
    ("README.md", "examples_files", r"-\s+(\d+)\s+synthetic examples"),
    ("README.md", "pseudocode_files", r"-\s+(\d+)\s+pseudocode sketches"),
    ("README.md", "diagram_files", r"-\s+(\d+)\s+Mermaid diagrams"),
    ("README.md", "code_capsule_roots", r"-\s+(\d+)\s+runnable public-safe code capsule roots"),
    ("docs/export-coverage.md", "source_files", r"Source-shaped retained module placeholders:\s+(\d+)"),
    ("docs/export-coverage.md", "redacted_files", r"Sanitized capability boundary placeholders:\s+(\d+)"),
    ("docs/export-coverage.md", "skeleton_readmes", r"Five-layer Research OS skeleton nodes:\s+(\d+)"),
    ("docs/export-coverage.md", "docs_files", r"Architecture and flow documents:\s+(\d+)"),
    ("docs/export-coverage.md", "pseudocode_files", r"Pseudocode:\s+(\d+)"),
    ("docs/export-coverage.md", "examples_files", r"Examples:\s+(\d+)"),
    ("docs/export-coverage.md", "diagram_files", r"Diagrams:\s+(\d+)"),
    ("docs/export-coverage.md", "code_capsule_roots", r"Runnable code capsule roots:\s+(\d+)"),
    ("docs/source-inventory.md", "source_files", r"Exported placeholder files:\s+(\d+)"),
    ("docs/redacted-capability-inventory.md", "redacted_files", r"Redacted placeholder files:\s+(\d+)"),
)

SOURCE_PLACEHOLDER_FIELDS = {
    "retained_path": ("Retained module path:", "Retained source path:", "Retained Rust path:"),
    "layer": ("Architecture layer:", "Research OS layer:", "System layer:"),
    "role": ("Architecture role:", "Review role:"),
    "inputs": ("Inputs:",),
    "outputs": ("Outputs:",),
    "omission_boundary": (
        "Implementation details intentionally omitted:",
        "Implementation body removed",
        "Deliberate redaction boundary:",
    ),
    "failure_or_boundary": (
        "fail-closed",
        "Failure",
        "blocker",
        "blocked",
        "validation error",
        "reject",
        "gate",
        "boundary",
        "regression",
    ),
}

ALLOWED_LAYER_MARKERS = (
    "Layer 5 - Research Governance & Operations",
    "Layer 4 - Research Applications",
    "Layer 3 - Evidence / Contract / DAG Kernel",
    "Layer 2 - Provider / Model / Runtime Engines",
    "Layer 1 - Data / Compute / Artifact Infrastructure",
    "Validation Evidence - Test Contracts",
    "Productization Boundary Layer",
    "Validation Layer",
)

STRONG_TRACEABILITY_PROOF_PREFIXES = (
    "code_capsules/",
    "examples/",
)

STRONG_TRACEABILITY_PROOF_FILES = {
    "scripts/benchmark_capsules.py",
    "scripts/verify_showcase.py",
}

TRACEABILITY_REQUIRED_PROOFS = {
    "source/rust/omni_wire/tests/test_sbe_cross_lang_fixture.rs": ("code_capsules/rust_native_boundary_proofs/",),
    "source/rust/omni_features_stream/tests/validate_ir.rs": ("code_capsules/rust_native_boundary_proofs/",),
    "source/rust/omni_bus_iceoryx2/src/journal.rs": ("code_capsules/rust_native_boundary_proofs/",),
    "source/omni_station/research_foundry/models/training_job.py": ("code_capsules/toy_model_lifecycle_gate",),
    "source/omni_station/research_foundry/models/model_factory.py": ("code_capsules/toy_model_lifecycle_gate",),
    "source/omni_station/research_foundry/models/model_card.py": ("examples/toy_model_card.json",),
    "source/omni_station/research_foundry/models/calibration.py": ("examples/toy_calibration_ood_report.json",),
    "source/omni_station/research_foundry/models/ood.py": ("examples/toy_model_lifecycle_gate_blocked.json",),
    "source/omni_station/research_foundry/models/uncertainty.py": ("code_capsules/toy_model_lifecycle_gate",),
    "source/omni_station/research_foundry/models/model_multiplicity.py": ("code_capsules/toy_model_lifecycle_gate",),
    "source/omni_station/research_foundry/models/production_evidence.py": ("examples/toy_model_lifecycle_gate_pass.json",),
}

RUST_CAPSULE_MANIFESTS = (
    "code_capsules/rust_sequence_tensor_kernel/Cargo.toml",
    "code_capsules/rust_native_boundary_proofs/Cargo.toml",
)

ML_REQUIRED_EXAMPLES = (
    "examples/toy_ml_training_manifest.json",
    "examples/toy_model_card.json",
    "examples/toy_model_branch_eligibility.json",
    "examples/toy_calibration_ood_report.json",
    "examples/toy_prediction_replay_manifest.json",
    "examples/toy_model_lifecycle_gate_pass.json",
    "examples/toy_model_lifecycle_gate_blocked.json",
)

ML_REQUIRED_TRACEABILITY_PATHS = (
    "source/omni_station/research_foundry/models/training_job.py",
    "source/omni_station/research_foundry/models/model_factory.py",
    "source/omni_station/research_foundry/models/model_card.py",
    "source/omni_station/research_foundry/models/calibration.py",
    "source/omni_station/research_foundry/models/ood.py",
    "source/omni_station/research_foundry/models/uncertainty.py",
    "source/omni_station/research_foundry/models/model_multiplicity.py",
    "source/omni_station/research_foundry/models/production_evidence.py",
    "source/omni_station/research_foundry/model_zoo/evidence/branch_eligibility.py",
    "source/omni_station/research_foundry/model_zoo/evidence/calibration_ood.py",
    "source/omni_station/research_foundry/model_zoo/evidence/calibration_reliability.py",
    "source/omni_station/research_foundry/model_zoo/evidence/score_distribution_drift.py",
)


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify showcase repository integrity")
    parser.add_argument("--skip-rust", action="store_true", help="skip cargo test")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    results = [
        run_command(
            "python code capsule tests",
            [sys.executable, "-m", "unittest", "discover", "code_capsules", "-p", "test_*.py"],
            root,
        ),
        run_command(
            "toy research flow",
            [sys.executable, "-m", "code_capsules.e2e_toy_research_flow.src.toy_research_flow"],
            root,
        ),
        check_ml_lifecycle_proof(root),
        check_markdown_path_refs(root),
        check_sensitive_patterns(root),
        check_tracked_hygiene(root),
        check_tracked_review_coverage(root),
        check_inventory(root),
        check_count_metadata(root),
        check_source_placeholder_schema(root),
        check_traceability_matrix(root),
        check_benchmark_smoke(root),
    ]
    if not args.skip_rust:
        if shutil.which("cargo") is None:
            results.append(CheckResult("rust code capsule tests", False, "cargo is not available"))
        else:
            for manifest_path in RUST_CAPSULE_MANIFESTS:
                results.append(
                    run_command(
                        f"rust code capsule tests ({manifest_path})",
                        ["cargo", "test", "--manifest-path", manifest_path],
                        root,
                    )
                )

    print("\nShowcase verification")
    print("=====================")
    for result in results:
        marker = "PASS" if result.ok else "FAIL"
        print(f"{marker} {result.name}: {result.detail}")

    return 0 if all(result.ok for result in results) else 1


def run_command(name: str, command: list[str], cwd: Path) -> CheckResult:
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    tail = "\n".join(completed.stdout.strip().splitlines()[-6:])
    return CheckResult(name, completed.returncode == 0, tail or "completed")


def check_markdown_path_refs(root: Path) -> CheckResult:
    markdown_files = [root / "README.md", root / "REVIEW_CHECKLIST.md"]
    for folder in ("docs", "code_capsules"):
        candidate = root / folder
        if candidate.exists():
            markdown_files.extend(candidate.rglob("*.md"))

    missing: list[str] = []
    for markdown_file in markdown_files:
        if not markdown_file.exists():
            continue
        text = markdown_file.read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r"`([^`]+)`", text):
            value = match.group(1).strip()
            if not looks_like_repo_path(value):
                continue
            path = value.split("#")[0].rstrip(".,:;")
            if not (root / path).exists():
                missing.append(f"{markdown_file.relative_to(root).as_posix()} -> {value}")

    if missing:
        return CheckResult("markdown path references", False, "; ".join(missing[:10]))
    return CheckResult("markdown path references", True, f"checked {len(markdown_files)} markdown files")


def looks_like_repo_path(value: str) -> bool:
    if value.startswith(("http://", "https://")):
        return False
    if " " in value or "->" in value:
        return False
    if "/" not in value:
        return False
    return value.startswith(
        (
            "source/",
            "docs/",
            "skeleton/",
            "examples/",
            "pseudocode/",
            "diagrams/",
            "redacted_capabilities/",
            "code_capsules/",
            "scripts/",
            ".github/",
        )
    )


def check_sensitive_patterns(root: Path) -> CheckResult:
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in sensitive_patterns()]
    hits: list[str] = []
    for path in iter_review_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in compiled:
            if pattern.search(text):
                hits.append(f"{path.relative_to(root).as_posix()} -> {pattern.pattern}")
                break

    if hits:
        return CheckResult("redaction scan", False, "; ".join(hits[:10]))
    return CheckResult("redaction scan", True, "no sensitive markers matched")


def iter_review_files(root: Path):
    ignored_dirs = {".git", "target", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    allowed_suffixes = {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".rs", ".mmd", ".txt"}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_dirs for part in path.relative_to(root).parts):
            continue
        if path.suffix.lower() in allowed_suffixes or path.name in {".gitignore", "NOTICE.md", "SECURITY.md"}:
            yield path


def check_tracked_hygiene(root: Path) -> CheckResult:
    command = ["git", "ls-files"]
    completed = subprocess.run(command, cwd=str(root), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if completed.returncode != 0:
        return CheckResult("tracked hygiene", False, completed.stderr.strip() or "git ls-files failed")
    bad: list[str] = []
    for line in completed.stdout.splitlines():
        path = Path(line)
        parts = tuple(part.lower() for part in path.parts)
        name = path.name.lower()
        suffix = path.suffix.lower()
        if any(part in FORBIDDEN_TRACKED_PARTS for part in parts):
            bad.append(line)
        if name in FORBIDDEN_TRACKED_NAMES:
            bad.append(line)
        if suffix in FORBIDDEN_TRACKED_SUFFIXES:
            bad.append(line)
    if bad:
        return CheckResult("tracked hygiene", False, "; ".join(bad[:10]))
    return CheckResult("tracked hygiene", True, "no generated/cache/data files tracked")


def check_tracked_review_coverage(root: Path) -> CheckResult:
    completed = subprocess.run(["git", "ls-files"], cwd=str(root), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if completed.returncode != 0:
        return CheckResult("tracked review coverage", False, completed.stderr.strip() or "git ls-files failed")
    tracked = {line.strip() for line in completed.stdout.splitlines() if line.strip()}
    missing = [
        path.relative_to(root).as_posix()
        for path in iter_review_files(root)
        if path.relative_to(root).as_posix() not in tracked
    ]
    if missing:
        return CheckResult("tracked review coverage", False, "; ".join(missing[:10]))
    return CheckResult("tracked review coverage", True, f"all {len(tracked)} tracked review paths are publishable")


def check_inventory(root: Path) -> CheckResult:
    source_files = sum(1 for path in (root / "source").rglob("*") if path.is_file())
    capsule_roots = [
        path for path in (root / "code_capsules").iterdir()
        if path.is_dir() and not path.name.startswith("__")
    ]
    required = {
        "artifact_manifest_hasher",
        "evidence_dag_validator",
        "leakage_fold_checker",
        "source_backed_label_view",
        "oof_metric_kernel",
        "purged_cpcv_splitter",
        "rust_sequence_tensor_kernel",
        "source_joinability_gate",
        "rust_native_boundary_proofs",
        "e2e_toy_research_flow",
        "toy_model_lifecycle_gate",
    }
    names = {path.name for path in capsule_roots}
    missing = sorted(required - names)
    if missing:
        return CheckResult("inventory", False, f"missing code capsules: {', '.join(missing)}")
    return CheckResult("inventory", True, f"{source_files} source files, {len(capsule_roots)} code capsule roots")


def check_count_metadata(root: Path) -> CheckResult:
    actual = {
        "source_files": count_files(root / "source"),
        "redacted_files": count_files(root / "redacted_capabilities"),
        "skeleton_readmes": count_files(root / "skeleton", pattern="README.md"),
        "docs_files": count_files(root / "docs"),
        "examples_files": count_files(root / "examples"),
        "pseudocode_files": count_files(root / "pseudocode"),
        "diagram_files": count_files(root / "diagrams"),
        "code_capsule_roots": sum(
            1 for path in (root / "code_capsules").iterdir()
            if path.is_dir() and not path.name.startswith("__")
        ),
    }

    mismatches: list[str] = []
    for key, expected in EXPECTED_COUNTS.items():
        observed = actual[key]
        if observed != expected:
            mismatches.append(f"{key}: actual {observed}, expected metadata {expected}")

    for relative_path, key, pattern in COUNT_REFERENCE_SPECS:
        path = root / relative_path
        if not path.exists():
            mismatches.append(f"{relative_path}: missing count reference file")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        match = re.search(pattern, text)
        if not match:
            mismatches.append(f"{relative_path}: missing count pattern for {key}")
            continue
        declared = int(match.group(1))
        if declared != actual[key]:
            mismatches.append(f"{relative_path}: declares {declared} for {key}, actual {actual[key]}")

    if mismatches:
        return CheckResult("count metadata", False, "; ".join(mismatches[:10]))
    return CheckResult(
        "count metadata",
        True,
        (
            f"{actual['source_files']} source, {actual['redacted_files']} redacted, "
            f"{actual['examples_files']} examples, {actual['code_capsule_roots']} capsule roots"
        ),
    )


def count_files(path: Path, pattern: str = "*") -> int:
    if not path.exists():
        return 0
    return sum(1 for candidate in path.rglob(pattern) if candidate.is_file())


def check_source_placeholder_schema(root: Path) -> CheckResult:
    source_root = root / "source"
    source_files = [
        path for path in source_root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".py", ".ts", ".tsx", ".rs"}
    ]
    failures: list[str] = []
    for path in source_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        missing = [
            field for field, markers in SOURCE_PLACEHOLDER_FIELDS.items()
            if not any(marker in text for marker in markers)
        ]
        if missing:
            failures.append(f"{path.relative_to(root).as_posix()} missing {','.join(missing)}")
            continue
        retained_path = _extract_retained_path(text)
        actual_path = path.relative_to(root / "source").as_posix()
        if retained_path != actual_path:
            failures.append(f"{path.relative_to(root).as_posix()} retained path {retained_path!r} != actual {actual_path!r}")
        layer = _extract_line_value(text, ("Architecture layer:", "Research OS layer:", "System layer:"))
        if layer is None or not any(marker in layer for marker in ALLOWED_LAYER_MARKERS):
            failures.append(f"{path.relative_to(root).as_posix()} has invalid layer {layer!r}")
        role = _extract_line_value(text, ("Architecture role:", "Review role:"))
        if role is None or len(role.split()) < 3:
            failures.append(f"{path.relative_to(root).as_posix()} has under-specified role {role!r}")
    if failures:
        return CheckResult("source placeholder schema", False, "; ".join(failures[:10]))
    return CheckResult("source placeholder schema", True, f"checked {len(source_files)} source placeholder files")


def check_traceability_matrix(root: Path) -> CheckResult:
    path = root / "docs" / "review-traceability.md"
    if not path.exists():
        return CheckResult("traceability matrix", False, "docs/review-traceability.md is missing")
    text = path.read_text(encoding="utf-8", errors="ignore")
    rows = [
        line for line in text.splitlines()
        if line.startswith("| `source/") and "|" in line
    ]
    failures: list[str] = []
    if len(rows) < 30:
        failures.append(f"expected at least 30 traceability rows, found {len(rows)}")
    for line in rows:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            failures.append(f"malformed row: {line[:120]}")
            continue
        source_path = _first_backtick_value(cells[0])
        if source_path is None or not (root / source_path).exists():
            failures.append(f"missing source path: {cells[0]}")
        if not cells[1].startswith("Layer "):
            failures.append(f"invalid layer cell: {cells[1]}")
        if len(cells[2]) < 12:
            failures.append(f"capability too terse: {source_path}")
        proof_paths = re.findall(r"`([^`]+)`", cells[3])
        if not proof_paths:
            failures.append(f"missing proof path: {source_path}")
        if source_path in proof_paths:
            failures.append(f"source path cannot prove itself: {source_path}")
        if not any(_is_strong_traceability_proof(proof_path) for proof_path in proof_paths):
            failures.append(f"missing executable or fixture proof: {source_path}")
        required_proofs = TRACEABILITY_REQUIRED_PROOFS.get(source_path or "")
        if required_proofs and not any(
            proof_path.startswith(required_proof)
            for required_proof in required_proofs
            for proof_path in proof_paths
        ):
            failures.append(f"missing semantically bound proof for {source_path}: {', '.join(required_proofs)}")
        for proof_path in proof_paths:
            if looks_like_repo_path(proof_path) and not (root / proof_path).exists():
                failures.append(f"missing proof path: {proof_path}")
    if failures:
        return CheckResult("traceability matrix", False, "; ".join(failures[:10]))
    return CheckResult("traceability matrix", True, f"checked {len(rows)} source-to-proof rows")


def check_benchmark_smoke(root: Path) -> CheckResult:
    completed = subprocess.run(
        [sys.executable, "scripts/benchmark_capsules.py"],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        return CheckResult("capsule benchmark smoke", False, completed.stdout.strip()[-500:])
    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return CheckResult("capsule benchmark smoke", False, f"benchmark did not emit JSON: {exc}")
    required = {
        "benchmark_id",
        "source_backed_label_plan",
        "dense_label_baseline",
        "physical_delta",
        "capsule_coverage",
        "rust_python_parity",
        "rust_native_boundary_proofs",
        "bounded_timing_smoke",
    }
    missing = sorted(required - set(report))
    if missing:
        return CheckResult("capsule benchmark smoke", False, f"missing fields: {', '.join(missing)}")
    label_plan = report["source_backed_label_plan"]
    baseline = report["dense_label_baseline"]
    delta = report["physical_delta"]
    coverage = report["capsule_coverage"]
    if label_plan["projection_width"] != 4 or label_plan["source_scan_count"] != 1:
        return CheckResult("capsule benchmark smoke", False, "unexpected source-backed label physical plan")
    if baseline["dense_rows_written"] <= 0:
        return CheckResult("capsule benchmark smoke", False, "dense baseline did not materialize rows")
    if label_plan["dense_rows_written"] != 0 or delta["dense_materialization_avoided"] is not True:
        return CheckResult("capsule benchmark smoke", False, "dense materialization was not avoided")
    if delta["avoided_dense_rows"] != baseline["dense_rows_written"]:
        return CheckResult("capsule benchmark smoke", False, "dense-row delta does not match baseline")
    if coverage["cpcv_split_count"] != 6 or coverage["joinability_pair_count"] != 1 or coverage["oof_group_count"] != 2:
        return CheckResult("capsule benchmark smoke", False, "capsule coverage counters drifted")
    if coverage["cpcv_group_purged_rows"] <= 0 or coverage["cpcv_time_purged_rows"] <= 0:
        return CheckResult("capsule benchmark smoke", False, "CPCV purge paths are not covered")
    if coverage["joinability_reject_count"] <= 0:
        return CheckResult("capsule benchmark smoke", False, "joinability reject path is not covered")
    if report["rust_python_parity"] not in {"pass", "skipped_no_cargo"}:
        return CheckResult("capsule benchmark smoke", False, "rust kernel parity smoke failed")
    if report["rust_native_boundary_proofs"] not in {"pass", "skipped_no_cargo"}:
        return CheckResult("capsule benchmark smoke", False, "rust native boundary proofs failed")
    timing = report["bounded_timing_smoke"]
    if not isinstance(timing, dict) or timing.get("threshold_enforced") is not False:
        return CheckResult("capsule benchmark smoke", False, "benchmark timing policy is not review-safe")
    golden_path = root / "examples" / "capsule_benchmark_report.json"
    golden = json.loads(golden_path.read_text(encoding="utf-8"))
    if _normalize_benchmark_report(report) != _normalize_benchmark_report(golden):
        return CheckResult("capsule benchmark smoke", False, "generated benchmark report does not match golden shape")
    return CheckResult("capsule benchmark smoke", True, "source-backed physical-plan smoke report is valid")


def check_ml_lifecycle_proof(root: Path) -> CheckResult:
    missing_examples = [path for path in ML_REQUIRED_EXAMPLES if not (root / path).exists()]
    if missing_examples:
        return CheckResult("ML lifecycle proof", False, f"missing examples: {', '.join(missing_examples)}")

    traceability = (root / "docs" / "review-traceability.md").read_text(encoding="utf-8", errors="ignore")
    missing_traceability = [path for path in ML_REQUIRED_TRACEABILITY_PATHS if path not in traceability]
    if missing_traceability:
        return CheckResult("ML lifecycle proof", False, f"missing traceability paths: {', '.join(missing_traceability[:5])}")

    pass_report = _run_ml_lifecycle_scenario(root, "pass")
    blocked_report = _run_ml_lifecycle_scenario(root, "blocked")
    if isinstance(pass_report, str):
        return CheckResult("ML lifecycle proof", False, pass_report)
    if isinstance(blocked_report, str):
        return CheckResult("ML lifecycle proof", False, blocked_report)

    pass_golden = json.loads((root / "examples" / "toy_model_lifecycle_gate_pass.json").read_text(encoding="utf-8"))
    blocked_golden = json.loads((root / "examples" / "toy_model_lifecycle_gate_blocked.json").read_text(encoding="utf-8"))
    if pass_report != pass_golden:
        return CheckResult("ML lifecycle proof", False, "pass scenario does not match golden report")
    if blocked_report != blocked_golden:
        return CheckResult("ML lifecycle proof", False, "blocked scenario does not match golden report")
    if pass_report["eligibility_gate"]["status"] != "pass":
        return CheckResult("ML lifecycle proof", False, "pass scenario did not pass")
    if blocked_report["eligibility_gate"]["status"] != "block":
        return CheckResult("ML lifecycle proof", False, "blocked scenario did not block")
    posture = pass_report.get("runtime_posture", {})
    if posture.get("offline_only") is not True or any(posture.get(key) is not False for key in ("paper", "live", "broker", "oms")):
        return CheckResult("ML lifecycle proof", False, "runtime posture is not offline-only")
    checked_modes = set(pass_report["eligibility_gate"].get("failure_modes_checked", []))
    required_modes = {
        "stale_trainable_manifest",
        "missing_fold_row_set_proof",
        "non_finite_prediction",
        "missing_calibration",
        "ood_drift",
        "proxy_score_artifact",
        "diagnostic_support_artifact",
        "prediction_replay_schema_mismatch",
    }
    if not required_modes.issubset(checked_modes):
        return CheckResult("ML lifecycle proof", False, "ML lifecycle failure-mode coverage is incomplete")
    return CheckResult("ML lifecycle proof", True, "pass/block model lifecycle reports match golden fixtures")


def _run_ml_lifecycle_scenario(root: Path, scenario: str) -> dict[str, object] | str:
    completed = subprocess.run(
        [sys.executable, "-m", "code_capsules.toy_model_lifecycle_gate", "--scenario", scenario],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        return f"scenario {scenario} failed: {completed.stdout.strip()[-500:]}"
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return f"scenario {scenario} did not emit JSON: {exc}"


def _first_backtick_value(text: str) -> str | None:
    match = re.search(r"`([^`]+)`", text)
    return match.group(1) if match else None


def _extract_retained_path(text: str) -> str | None:
    for marker in ("Retained module path:", "Retained source path:", "Retained Rust path:"):
        value = _extract_line_value(text, (marker,))
        if value is not None:
            return value
    return None


def _extract_line_value(text: str, markers: tuple[str, ...]) -> str | None:
    for line in text.splitlines():
        stripped = line.strip().lstrip("*").strip()
        for marker in markers:
            if stripped.startswith(marker):
                return stripped[len(marker):].strip()
    return None


def _is_strong_traceability_proof(path: str) -> bool:
    return path in STRONG_TRACEABILITY_PROOF_FILES or path.startswith(STRONG_TRACEABILITY_PROOF_PREFIXES)


def _normalize_benchmark_report(report: dict[str, object]) -> dict[str, object]:
    normalized = json.loads(json.dumps(report, sort_keys=True))
    timing = normalized.get("bounded_timing_smoke")
    if isinstance(timing, dict):
        timing.pop("elapsed_ms", None)
    for key in ("rust_python_parity", "rust_native_boundary_proofs"):
        if normalized.get(key) in {"pass", "skipped_no_cargo"}:
            normalized[key] = "pass_or_skipped"
    return normalized


if __name__ == "__main__":
    raise SystemExit(main())
