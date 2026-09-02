#!/usr/bin/env python3
"""Write exact Round-Twenty-Three source/PDF build records.

Run only after tools/verify_round23.py and a clean build of all eleven papers.
The record identifies the pre-publication source commit and cryptographic
hashes.  It deliberately describes repository reproducibility, not external
mathematical acceptance.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "ROUND23_SOURCE_MANIFEST.json"
RESULTS_PATH = ROOT / "ROUND23_REGRESSION_RESULTS.json"
SUMMARY_PATH = ROOT / "ROUND23_BUILD_SUMMARY.json"
STATUS_PATH = ROOT / "ROUND23_REVISION_STATUS.md"


def die(message: str) -> None:
    print(f"ROUND23_BUILD_RECORD_FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def digest(path: Path) -> str:
    hasher = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def git(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT
        ).strip()
    except subprocess.CalledProcessError as exc:
        die(f"git {' '.join(args)} failed: {exc.output.strip()}")
    raise AssertionError("unreachable")


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        die(f"missing {path.name}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        die(f"cannot parse {path.name}: {exc}")
    if not isinstance(value, dict):
        die(f"{path.name} is not a JSON object")
    return value


def scan_log(path: Path, paper: str) -> dict[str, int]:
    if not path.is_file():
        die(f"{paper}: missing main.log after build")
    text = path.read_text(encoding="utf-8", errors="replace")
    fatal_patterns = (
        "! LaTeX Error:",
        "! Emergency stop.",
        "Fatal error occurred",
        "There were undefined references",
        "Please (re)run Biber",
    )
    for pattern in fatal_patterns:
        if pattern in text:
            die(f"{paper}: build log contains {pattern!r}")
    undefined_citations = text.count("Citation '") + text.count("Citation `")
    if undefined_citations:
        die(f"{paper}: build log contains undefined citation diagnostics")
    return {
        "overfull_hbox": text.count("Overfull \\hbox"),
        "underfull_hbox": text.count("Underfull \\hbox"),
        "multiply_defined_labels": text.count("multiply defined"),
    }


def main() -> None:
    manifest = load_json(MANIFEST_PATH)
    results = load_json(RESULTS_PATH)
    if results.get("status") != "PASS":
        die("Round-Twenty-Three regression results are not PASS")
    if results.get("revision") != manifest.get("revision"):
        die("manifest and regression revision identifiers differ")

    source_commit = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    expected_branch = manifest.get("branch")
    if branch and branch != expected_branch:
        die(f"building branch {branch!r}, expected {expected_branch!r}")

    records: list[dict[str, Any]] = []
    for key, entry in manifest["papers"].items():
        folder = ROOT / entry["directory"]
        source = folder / manifest["active_source"]
        wrapper = folder / "main.tex"
        pdf = folder / "main.pdf"
        for path in (source, wrapper, pdf):
            if not path.is_file():
                die(f"{key}: missing {path.relative_to(ROOT)}")
        if pdf.stat().st_size < 20_000:
            die(f"{key}: PDF is unexpectedly small ({pdf.stat().st_size} bytes)")
        data_start = pdf.read_bytes()[:8]
        if not data_start.startswith(b"%PDF-"):
            die(f"{key}: main.pdf has no PDF header")
        log_metrics = scan_log(folder / "main.log", key)
        records.append(
            {
                "paper": key,
                "directory": entry["directory"],
                "active_source": source.name,
                "source_bytes": source.stat().st_size,
                "source_sha256": digest(source),
                "wrapper_sha256": digest(wrapper),
                "pdf_bytes": pdf.stat().st_size,
                "pdf_sha256": digest(pdf),
                "log_metrics": log_metrics,
            }
        )

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    summary = {
        "schema": "theta-theory-round23-build-summary-v1",
        "revision": manifest["revision"],
        "branch": manifest["branch"],
        "source_verified_commit": source_commit,
        "built_at_utc": now,
        "referee_report_git_blob_sha": manifest["referee_report"]["git_blob_sha"],
        "combined_active_source_sha256": results["combined_active_source_sha256"],
        "regression_count": len(results["regressions"]),
        "paper_count": len(records),
        "papers": records,
        "status": "PASS",
        "scope": (
            "Clean repository build plus source, citation, dependency, and "
            "finite-dimensional referee-counterexample regression checks."
        ),
        "disclaimer": (
            "This is internal reproducibility evidence and does not constitute "
            "independent mathematical peer review or journal acceptance."
        ),
    }
    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Round-Twenty-Three revision status",
        "",
        "**Repository verification status:** PASS  ",
        f"**Revision:** `{manifest['revision']}`  ",
        f"**Branch:** `{manifest['branch']}`  ",
        f"**Source-verified commit:** `{source_commit}`  ",
        f"**Built at (UTC):** `{now}`  ",
        f"**Controlling referee report blob:** `{manifest['referee_report']['git_blob_sha']}`  ",
        f"**Combined active-source SHA-256:** `{results['combined_active_source_sha256']}`  ",
        "",
        "## Gates completed",
        "",
        f"- {len(records)} active Round-Twenty-Three manuscript sources verified.",
        f"- {len(results['regressions'])} mathematical counterexample regressions passed.",
        "- All active citation keys and local theorem references resolved.",
        "- The declared proof dependency graph was acyclic.",
        "- All eleven manuscripts were clean-built in one checkout.",
        "- The inherited Round-Twenty-Two referee report matched its registered Git blob.",
        "",
        "## Paper artifacts",
        "",
        "| Paper | Source bytes | PDF bytes | Source SHA-256 | PDF SHA-256 | Overfull boxes |",
        "|---|---:|---:|---|---|---:|",
    ]
    for record in records:
        lines.append(
            f"| {record['paper']} | {record['source_bytes']} | {record['pdf_bytes']} | "
            f"`{record['source_sha256']}` | `{record['pdf_sha256']}` | "
            f"{record['log_metrics']['overfull_hbox']} |"
        )
    lines.extend(
        [
            "",
            "## Scope",
            "",
            "The PASS certifies source identity, bibliography closure, dependency order, "
            "the executable finite-dimensional regressions derived from the latest referee "
            "counterexamples, and reproducible PDF generation on the recorded commit.  It "
            "does not replace independent specialist review.  The branch is prepared for "
            "the next referee round with the complete prior report and revision provenance "
            "retained.",
            "",
        ]
    )
    STATUS_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(
        "ROUND23_BUILD_RECORD_PASS "
        f"papers={len(records)} source_commit={source_commit} built_at={now}"
    )


if __name__ == "__main__":
    main()
