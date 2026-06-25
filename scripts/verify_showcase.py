"""Verify the public showcase repository.

This script is intentionally dependency-light so a technical reviewer can run
the same checks locally that CI runs: tests, path references, redaction scans,
and repository hygiene checks.
"""

from __future__ import annotations

import argparse
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
    "docs_files": 33,
    "examples_files": 23,
    "pseudocode_files": 12,
    "diagram_files": 8,
    "code_capsule_roots": 6,
}

COUNT_REFERENCE_SPECS = (
    ("README.md", "source_files", r"-\s+(\d+)\s+source-shaped module placeholders"),
    ("README.md", "redacted_files", r"-\s+(\d+)\s+sanitized capability placeholders"),
    ("README.md", "skeleton_readmes", r"-\s+(\d+)\s+five-layer skeleton README nodes"),
    ("README.md", "docs_files", r"-\s+(\d+)\s+architecture and flow documents"),
    ("README.md", "examples_files", r"-\s+(\d+)\s+synthetic examples"),
    ("README.md", "pseudocode_files", r"-\s+(\d+)\s+pseudocode sketches"),
    ("README.md", "diagram_files", r"-\s+(\d+)\s+Mermaid diagrams"),
    ("docs/export-coverage.md", "source_files", r"Source-shaped retained module placeholders:\s+(\d+)"),
    ("docs/export-coverage.md", "redacted_files", r"Sanitized capability boundary placeholders:\s+(\d+)"),
    ("docs/export-coverage.md", "skeleton_readmes", r"Five-layer Research OS skeleton nodes:\s+(\d+)"),
    ("docs/export-coverage.md", "docs_files", r"Architecture and flow documents:\s+(\d+)"),
    ("docs/export-coverage.md", "pseudocode_files", r"Pseudocode:\s+(\d+)"),
    ("docs/export-coverage.md", "examples_files", r"Examples:\s+(\d+)"),
    ("docs/export-coverage.md", "diagram_files", r"Diagrams:\s+(\d+)"),
    ("docs/source-inventory.md", "source_files", r"Exported placeholder files:\s+(\d+)"),
    ("docs/redacted-capability-inventory.md", "redacted_files", r"Redacted placeholder files:\s+(\d+)"),
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
        check_markdown_path_refs(root),
        check_sensitive_patterns(root),
        check_tracked_hygiene(root),
        check_inventory(root),
        check_count_metadata(root),
    ]
    if not args.skip_rust:
        if shutil.which("cargo") is None:
            results.append(CheckResult("rust code capsule tests", False, "cargo is not available"))
        else:
            results.append(
                run_command(
                    "rust code capsule tests",
                    ["cargo", "test", "--manifest-path", "code_capsules/rust_sequence_tensor_kernel/Cargo.toml"],
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


def check_inventory(root: Path) -> CheckResult:
    source_files = sum(1 for path in (root / "source").rglob("*") if path.is_file())
    capsule_roots = [
        path for path in (root / "code_capsules").iterdir()
        if path.is_dir() and not path.name.startswith("__")
    ]
    required = {
        "evidence_dag_validator",
        "leakage_fold_checker",
        "source_backed_label_view",
        "oof_metric_kernel",
        "rust_sequence_tensor_kernel",
        "e2e_toy_research_flow",
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


if __name__ == "__main__":
    raise SystemExit(main())
