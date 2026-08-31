#!/usr/bin/env python3
"""Clean-build all eleven round-seven manuscripts and preserve final diagnostics."""
from __future__ import annotations

from pathlib import Path
import json
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPER_NAMES = [
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
LOG_DIR = ROOT / "ROUND7_BUILD_LOGS"
SUMMARY_PATH = ROOT / "ROUND7_BUILD_SUMMARY.json"
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


def context(text: str, radius: int = 7, max_blocks: int = 8) -> list[str]:
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if ERROR_RE.search(line)]
    if not hits:
        return lines[-100:]
    blocks: list[str] = []
    used: list[tuple[int, int]] = []
    for i in hits:
        lo, hi = max(0, i - radius), min(len(lines), i + radius + 1)
        if any(lo >= a and hi <= b for a, b in used):
            continue
        used.append((lo, hi))
        blocks.append("\n".join(lines[lo:hi]))
        if len(blocks) >= max_blocks:
            break
    return blocks


def main() -> None:
    if shutil.which("latexmk") is None:
        raise SystemExit("latexmk is not installed")
    LOG_DIR.mkdir(exist_ok=True)
    for old in LOG_DIR.glob("*.log"):
        old.unlink()

    results: dict[str, dict[str, object]] = {}
    failed: list[str] = []
    for name in PAPER_NAMES:
        paper = ROOT / "papers" / name
        main_tex = paper / "main.tex"
        if not main_tex.is_file():
            failed.append(name)
            results[name] = {"status": "MISSING_MAIN"}
            continue
        run(["latexmk", "-C", "main.tex"], paper)
        completed = run(
            [
                "latexmk", "-pdf", "-interaction=nonstopmode",
                "-halt-on-error", "-file-line-error", "main.tex",
            ],
            paper,
        )
        log_path = LOG_DIR / f"{name}.log"
        log_path.write_text(completed.stdout, encoding="utf-8", errors="replace")
        pdf = paper / "main.pdf"
        final_log = paper / "main.log"
        ok = (
            completed.returncode == 0
            and pdf.is_file() and pdf.stat().st_size > 0
            and final_log.is_file()
        )
        results[name] = {
            "status": "PASS" if ok else "FAIL",
            "returncode": completed.returncode,
            "pdf_bytes": pdf.stat().st_size if pdf.is_file() else 0,
            "transcript": str(log_path.relative_to(ROOT)),
            "final_log": str(final_log.relative_to(ROOT)) if final_log.is_file() else None,
        }
        if ok:
            print(f"ROUND7_BUILD_PASS {name} pdf_bytes={pdf.stat().st_size}")
        else:
            failed.append(name)
            print(f"ROUND7_BUILD_FAIL_BEGIN {name}", file=sys.stderr)
            for block in context(completed.stdout):
                print(block, file=sys.stderr)
                print("---", file=sys.stderr)
            print(f"ROUND7_BUILD_FAIL_END {name}", file=sys.stderr)

    summary = {
        "schema": "theta-theory-round7-build-summary-v1",
        "status": "PASS" if not failed else "FAIL",
        "paper_count": len(PAPER_NAMES),
        "passed": len(PAPER_NAMES) - len(failed),
        "failed": failed,
        "papers": results,
    }
    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if failed:
        raise SystemExit(
            f"ROUND7_BUILD_SUMMARY_FAIL passed={summary['passed']}/11 "
            f"failed={','.join(failed)}"
        )
    print("ROUND7_BUILD_SUMMARY_PASS 11/11")


if __name__ == "__main__":
    main()
