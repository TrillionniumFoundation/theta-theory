#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

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
LOGDIR = ROOT / "ROUND11_BUILD_LOGS"
LOGDIR.mkdir(exist_ok=True)
UNDEFINED = re.compile(
    r"LaTeX Warning: (?:Reference|Citation).+undefined|"
    r"There were undefined references|There were undefined citations"
)

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

summary: dict[str, object] = {
    "schema": "theta-theory-round11-build-summary-v1",
    "papers": {},
    "failed": [],
}
for folder in PAPERS:
    paper = ROOT / "papers" / folder
    transcript = LOGDIR / f"{folder}.log"
    subprocess.run(["latexmk", "-C", "main.tex"], cwd=paper, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    proc = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        cwd=paper,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=300,
    )
    transcript.write_text(proc.stdout, encoding="utf-8", errors="replace")
    pdf = paper / "main.pdf"
    texlog = paper / "main.log"
    undefined_lines: list[str] = []
    if texlog.is_file():
        undefined_lines = [line for line in texlog.read_text(encoding="utf-8", errors="replace").splitlines() if UNDEFINED.search(line)]
    pages = 0
    if pdf.is_file() and pdf.stat().st_size:
        info = subprocess.run(["pdfinfo", str(pdf)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        match = re.search(r"^Pages:\s+(\d+)", info.stdout, re.M)
        pages = int(match.group(1)) if match else 0
    ok = proc.returncode == 0 and pdf.is_file() and pdf.stat().st_size > 0 and pages > 0 and not undefined_lines
    entry = {
        "returncode": proc.returncode,
        "status": "PASS" if ok else "FAIL",
        "pdf_bytes": pdf.stat().st_size if pdf.is_file() else 0,
        "pdf_pages": pages,
        "pdf_sha256": sha(pdf) if pdf.is_file() and pdf.stat().st_size else None,
        "undefined_reference_lines": undefined_lines,
        "transcript": str(transcript.relative_to(ROOT)),
    }
    summary["papers"][folder] = entry
    if not ok:
        summary["failed"].append(folder)
        print(f"ROUND11_BUILD_FAIL {folder}\n{proc.stdout[-5000:]}", file=sys.stderr)
summary["paper_count"] = len(PAPERS)
summary["passed"] = len(PAPERS) - len(summary["failed"])
summary["total_pdf_pages"] = sum(entry["pdf_pages"] for entry in summary["papers"].values())
summary["status"] = "PASS" if not summary["failed"] else "FAIL"
(ROOT / "ROUND11_BUILD_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
if summary["failed"]:
    raise SystemExit(1)
print(f"ROUND11_BUILD_PASS {summary['passed']}/11 pages={summary['total_pdf_pages']}")
