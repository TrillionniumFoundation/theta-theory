#!/usr/bin/env python3
"""Clean-build all eleven Round-Seventeen papers in parallel and record hashes."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = sorted(p for p in (ROOT / "papers").iterdir() if p.is_dir())
LOGDIR = ROOT / "ROUND17_BUILD_LOGS"
LOGDIR.mkdir(exist_ok=True)
if len(PAPERS) != 11:
    raise SystemExit(f"expected 11 paper directories, found {len(PAPERS)}")

bad_patterns = [
    re.compile(r"LaTeX Warning: (?:Reference|Citation).*undefined"),
    re.compile(r"There were undefined references"),
    re.compile(r"There were undefined citations"),
]

def build(paper: Path) -> tuple[str, dict[str, object]]:
    for ext in ("aux", "bbl", "bcf", "blg", "fdb_latexmk", "fls", "log", "out", "run.xml", "toc", "pdf"):
        target = paper / f"main.{ext}"
        if target.exists(): target.unlink()
    proc = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        cwd=paper, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    transcript = proc.stdout
    (LOGDIR / f"{paper.name}.log").write_text(transcript, encoding="utf-8", errors="replace")
    log_text = (paper / "main.log").read_text(encoding="utf-8", errors="replace") if (paper / "main.log").exists() else transcript
    undefined = [line for line in log_text.splitlines() if any(p.search(line) for p in bad_patterns)]
    pdf = paper / "main.pdf"
    pages = 0
    if pdf.exists():
        info = subprocess.run(["pdfinfo", str(pdf)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        m = re.search(r"^Pages:\s+(\d+)", info.stdout, re.M)
        pages = int(m.group(1)) if m else 0
    ok = proc.returncode == 0 and pdf.is_file() and pdf.stat().st_size > 0 and not undefined
    return paper.name, {
        "status": "PASS" if ok else "FAIL", "returncode": proc.returncode,
        "undefined_reference_lines": undefined,
        "transcript": f"ROUND17_BUILD_LOGS/{paper.name}.log",
        "pdf_bytes": pdf.stat().st_size if pdf.exists() else 0,
        "pdf_pages": pages,
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest() if pdf.exists() else None,
    }

summary: dict[str, object] = {"schema": "theta-theory-round17-build-summary-v1", "papers": {}, "failed": []}
with ThreadPoolExecutor(max_workers=6) as pool:
    futures = {pool.submit(build, paper): paper for paper in PAPERS}
    for future in as_completed(futures):
        name, entry = future.result()
        summary["papers"][name] = entry
        if entry["status"] != "PASS": summary["failed"].append(name)
        print(f"ROUND17_BUILD {name} {entry['status']} pages={entry['pdf_pages']}", flush=True)
summary["papers"] = dict(sorted(summary["papers"].items()))
summary["paper_count"] = len(PAPERS)
summary["passed"] = len(PAPERS) - len(summary["failed"])
summary["total_pdf_pages"] = sum(x["pdf_pages"] for x in summary["papers"].values())
summary["status"] = "PASS" if not summary["failed"] else "FAIL"
(ROOT / "ROUND17_BUILD_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
if summary["failed"]:
    raise SystemExit("Round-Seventeen build failures: " + ", ".join(summary["failed"]))
print(f"ROUND17_BUILD_PASS 11/11 pages={summary['total_pdf_pages']}")
