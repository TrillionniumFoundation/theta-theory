#!/usr/bin/env python3
"""Clean-build all eleven round-three manuscripts with concise diagnostics.

GitHub Actions log transport can truncate a monolithic ``make all`` failure.
This runner compiles every paper independently, persists the full logs, emits a
small failure context for each paper, and writes a machine-readable summary.
It deliberately continues after a paper failure so one CI run exposes every
remaining TeX problem.
"""
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
LOG_DIR = ROOT / "ROUND3_BUILD_LOGS"
SUMMARY_PATH = ROOT / "ROUND3_BUILD_SUMMARY.json"
ERROR_MARKERS = re.compile(
    r"(^! |LaTeX Error:|Package .* Error:|Undefined control sequence|"
    r"Emergency stop|Fatal error|^.*\.tex:\d+:|There were undefined references|"
    r"There were undefined citations|Citation .* undefined|Reference .* undefined)",
    re.IGNORECASE | re.MULTILINE,
)


def concise_context(text: str, radius: int = 8, max_blocks: int = 6) -> list[str]:
    lines = text.splitlines()
    hit_indices = [i for i, line in enumerate(lines) if ERROR_MARKERS.search(line)]
    if not hit_indices:
        return lines[-80:]
    blocks: list[str] = []
    seen: set[tuple[int, int]] = set()
    for index in hit_indices:
        lo = max(0, index - radius)
        hi = min(len(lines), index + radius + 1)
        key = (lo, hi)
        if key in seen:
            continue
        seen.add(key)
        blocks.append("\n".join(lines[lo:hi]))
        if len(blocks) >= max_blocks:
            break
    return blocks


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def main() -> None:
    if shutil.which("latexmk") is None:
        raise SystemExit("latexmk is not installed")
    LOG_DIR.mkdir(exist_ok=True)
    for old in LOG_DIR.glob("*.log"):
        old.unlink()

    results: dict[str, dict[str, object]] = {}
    failures: list[str] = []

    for name in PAPER_NAMES:
        paper = ROOT / "papers" / name
        main_tex = paper / "main.tex"
        if not main_tex.is_file():
            failures.append(name)
            results[name] = {"status": "MISSING_MAIN", "returncode": 127}
            print(f"ROUND3_BUILD_MISSING {name}", file=sys.stderr)
            continue

        run(["latexmk", "-C", "main.tex"], paper)
        completed = run(
            [
                "latexmk",
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                "main.tex",
            ],
            paper,
        )
        log_path = LOG_DIR / f"{name}.log"
        log_path.write_text(completed.stdout, encoding="utf-8", errors="replace")

        pdf = paper / "main.pdf"
        ok = completed.returncode == 0 and pdf.is_file() and pdf.stat().st_size > 0
        results[name] = {
            "status": "PASS" if ok else "FAIL",
            "returncode": completed.returncode,
            "pdf_bytes": pdf.stat().st_size if pdf.is_file() else 0,
            "log": str(log_path.relative_to(ROOT)),
        }
        if ok:
            print(f"ROUND3_BUILD_PASS {name} pdf_bytes={pdf.stat().st_size}")
        else:
            failures.append(name)
            print(
                f"ROUND3_BUILD_FAIL_BEGIN {name} returncode={completed.returncode}",
                file=sys.stderr,
            )
            for block in concise_context(completed.stdout):
                print(block, file=sys.stderr)
                print("---", file=sys.stderr)
            print(f"ROUND3_BUILD_FAIL_END {name}", file=sys.stderr)

    summary = {
        "status": "PASS" if not failures else "FAIL",
        "paper_count": len(PAPER_NAMES),
        "passed": len(PAPER_NAMES) - len(failures),
        "failed": failures,
        "papers": results,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if failures:
        print(
            "ROUND3_BUILD_SUMMARY_FAIL "
            f"passed={summary['passed']}/11 failed={','.join(failures)}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print("ROUND3_BUILD_SUMMARY_PASS 11/11")


if __name__ == "__main__":
    main()
