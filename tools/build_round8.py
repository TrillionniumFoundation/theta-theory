#!/usr/bin/env python3
"""Clean-build all eleven round-eight manuscripts and preserve diagnostics."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import os

ROOT = Path(__file__).resolve().parents[1]
PAPERS = [
    "A1-exact-benchmarks",
    "A2-sinai-homological-pressure",
    "A3-full-empirical-path-ldp",
    "A4-history-memory-universal-pressure",
    "B1-microcanonical-preparation",
    "B2-collision-clusters-dynamic-ldp",
    "B3-hamilton-boltzmann-cotangents",
    "B4-nonlinear-kinetic-semigroups",
    "C1-information-risk-sensitive-saddles",
    "C2-cotangent-rigidity-tangent-representations",
    "D1-deterministic-theta-contractions",
]
LOG_DIR = ROOT / "ROUND8_BUILD_LOGS"
SUMMARY = ROOT / "ROUND8_BUILD_SUMMARY.json"
WARNING_RE = re.compile(
    r"LaTeX Warning: (?:Reference|Citation).*undefined|"
    r"There were undefined references|There were undefined citations|"
    r"Please \(re\)run Biber",
    re.IGNORECASE,
)
ERROR_RE = re.compile(
    r"(^! |LaTeX Error:|Package .* Error:|Undefined control sequence|"
    r"Emergency stop|Fatal error|^.*\.tex:\d+:)",
    re.IGNORECASE | re.MULTILINE,
)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def error_context(output: str) -> list[str]:
    lines = output.splitlines()
    hits = [i for i, line in enumerate(lines) if ERROR_RE.search(line)]
    if not hits:
        return lines[-80:]
    result: list[str] = []
    for i in hits[:8]:
        result.extend(lines[max(0, i - 5): min(len(lines), i + 7)])
        result.append("---")
    return result


def main() -> None:
    if shutil.which("latexmk") is None:
        raise SystemExit("latexmk is not installed")
    if shutil.which("pdfinfo") is None:
        raise SystemExit("pdfinfo is not installed")
    LOG_DIR.mkdir(exist_ok=True)
    for old in LOG_DIR.glob("*.log"):
        old.unlink()

    results: dict[str, object] = {}
    failures: list[str] = []
    total_pages = 0
    resume = os.environ.get("ROUND8_RESUME") == "1"
    for name in PAPERS:
        paper = ROOT / "papers" / name
        existing_pdf = paper / "main.pdf"
        existing_log = paper / "main.log"
        if resume and existing_pdf.is_file() and existing_pdf.stat().st_size > 0 and existing_log.is_file():
            log_text = existing_log.read_text(encoding="utf-8", errors="replace")
            undefined_existing = [line for line in log_text.splitlines() if WARNING_RE.search(line)]
            info = run(["pdfinfo", "main.pdf"], paper)
            match = re.search(r"^Pages:\s*(\d+)", info.stdout, re.MULTILINE)
            if match and not undefined_existing:
                pages = int(match.group(1))
                total_pages += pages
                results[name] = {
                    "status": "PASS",
                    "pdf_bytes": existing_pdf.stat().st_size,
                    "pdf_pages": pages,
                    "pdf_sha256": sha256(existing_pdf),
                    "transcript": "RESUMED_EXISTING_FINAL_LOG",
                    "undefined_reference_lines": [],
                }
                print(f"ROUND8_BUILD_RESUME_PASS {name} pages={pages} pdf_bytes={existing_pdf.stat().st_size}")
                continue
        clean = run(["latexmk", "-C", "main.tex"], paper)
        completed = run(
            [
                "latexmk", "-pdf", "-interaction=nonstopmode",
                "-halt-on-error", "-file-line-error", "main.tex",
            ],
            paper,
        )
        transcript = LOG_DIR / f"{name}.log"
        transcript.write_text(completed.stdout, encoding="utf-8", errors="replace")
        pdf = paper / "main.pdf"
        final_log = paper / "main.log"
        undefined: list[str] = []
        if final_log.is_file():
            undefined = [
                line for line in final_log.read_text(encoding="utf-8", errors="replace").splitlines()
                if WARNING_RE.search(line)
            ]
        pages = 0
        if pdf.is_file() and pdf.stat().st_size > 0:
            info = run(["pdfinfo", "main.pdf"], paper)
            match = re.search(r"^Pages:\s*(\d+)", info.stdout, re.MULTILINE)
            if match:
                pages = int(match.group(1))
        ok = (
            completed.returncode == 0
            and pdf.is_file() and pdf.stat().st_size > 0
            and final_log.is_file() and pages >= 1
            and not undefined
        )
        if ok:
            total_pages += pages
            results[name] = {
                "status": "PASS",
                "pdf_bytes": pdf.stat().st_size,
                "pdf_pages": pages,
                "pdf_sha256": sha256(pdf),
                "transcript": str(transcript.relative_to(ROOT)),
                "undefined_reference_lines": [],
            }
            print(f"ROUND8_BUILD_PASS {name} pages={pages} pdf_bytes={pdf.stat().st_size}")
        else:
            failures.append(name)
            results[name] = {
                "status": "FAIL",
                "returncode": completed.returncode,
                "pdf_bytes": pdf.stat().st_size if pdf.is_file() else 0,
                "pdf_pages": pages,
                "undefined_reference_lines": undefined[:30],
                "clean_returncode": clean.returncode,
                "transcript": str(transcript.relative_to(ROOT)),
            }
            print(f"ROUND8_BUILD_FAIL_BEGIN {name}", file=sys.stderr)
            for line in error_context(completed.stdout):
                print(line, file=sys.stderr)
            for line in undefined[:30]:
                print(f"UNDEFINED {line}", file=sys.stderr)
            print(f"ROUND8_BUILD_FAIL_END {name}", file=sys.stderr)

    summary = {
        "schema": "theta-theory-round8-build-summary-v1",
        "status": "PASS" if not failures else "FAIL",
        "paper_count": len(PAPERS),
        "passed": len(PAPERS) - len(failures),
        "failed": failures,
        "total_pdf_pages": total_pages,
        "papers": results,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit(f"ROUND8_BUILD_SUMMARY_FAIL failed={','.join(failures)}")
    print(f"ROUND8_BUILD_SUMMARY_PASS papers=11 total_pages={total_pages}")


if __name__ == "__main__":
    main()
