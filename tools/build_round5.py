#!/usr/bin/env python3
"""Clean-build all eleven round-five manuscripts and record PDF hashes/pages."""
from __future__ import annotations

from pathlib import Path
import hashlib
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
LOG_DIR = ROOT / "ROUND5_BUILD_LOGS"
PDF_DIR = ROOT / "ROUND5_PDF_BUNDLE"
SUMMARY_PATH = ROOT / "ROUND5_BUILD_SUMMARY.json"
FAILURES_PATH = ROOT / "ROUND5_BUILD_FAILURES.md"
ERROR_MARKERS = re.compile(
    r"(^! |LaTeX Error:|Package .* Error:|Undefined control sequence|"
    r"Emergency stop|Fatal error|^.*\.tex:\d+:|There were undefined references|"
    r"There were undefined citations|Citation .* undefined|Reference .* undefined)",
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
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pages(path: Path) -> tuple[int, str]:
    """Return a fail-closed page count plus compact diagnostics.

    Poppler versions differ in whitespace and line endings, so parse the
    ``Pages:`` field permissively. If ``pdfinfo`` succeeds but its localized
    output cannot be parsed, fall back to counting PDF page objects. The
    fallback deliberately excludes the ``/Pages`` tree object via a word
    boundary and is used only for PDFs just emitted by pdfTeX.
    """
    completed = run(["pdfinfo", str(path.resolve())], path.parent)
    output = completed.stdout.replace("\r", "\n")
    if completed.returncode == 0:
        match = re.search(r"(?im)^\s*Pages\s*:\s*(\d+)\b", output)
        if match:
            return int(match.group(1)), "pdfinfo"
    try:
        data = path.read_bytes()
    except OSError as exc:
        return 0, f"read-error:{exc}"
    page_objects = len(re.findall(rb"/Type\s*/Page\b", data))
    if page_objects > 0:
        return page_objects, "pdf-object-fallback"
    diagnostic = " | ".join(line.strip() for line in output.splitlines()[:8])
    return 0, f"pdfinfo-returncode={completed.returncode}; output={diagnostic}"


def concise_context(text: str, radius: int = 8, max_blocks: int = 6) -> list[str]:
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if ERROR_MARKERS.search(line)]
    if not hits:
        return ["\n".join(lines[-100:])]
    blocks: list[str] = []
    occupied: list[tuple[int, int]] = []
    for index in hits:
        lo = max(0, index - radius)
        hi = min(len(lines), index + radius + 1)
        if any(not (hi <= a or lo >= b) for a, b in occupied):
            continue
        occupied.append((lo, hi))
        blocks.append("\n".join(lines[lo:hi]))
        if len(blocks) >= max_blocks:
            break
    return blocks


def main() -> None:
    for command in ("latexmk", "pdfinfo"):
        if shutil.which(command) is None:
            raise SystemExit(f"{command} is not installed")

    LOG_DIR.mkdir(exist_ok=True)
    PDF_DIR.mkdir(exist_ok=True)
    for directory in (LOG_DIR, PDF_DIR):
        for old in directory.iterdir():
            if old.is_file():
                old.unlink()

    results: dict[str, dict[str, object]] = {}
    failures: list[str] = []
    failure_blocks: list[str] = ["# Round-five build failures", ""]

    for name in PAPER_NAMES:
        paper = ROOT / "papers" / name
        main_tex = paper / "main.tex"
        if not main_tex.is_file():
            failures.append(name)
            results[name] = {"status": "MISSING_MAIN", "returncode": 127}
            failure_blocks += [f"## {name}", "", "`main.tex` missing.", ""]
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
        page_count, page_counter = pages(pdf) if pdf.is_file() else (0, "missing-pdf")
        undefined = bool(
            re.search(
                r"LaTeX Warning: (?:Reference|Citation).*undefined|"
                r"There were undefined references|There were undefined citations",
                completed.stdout,
                re.IGNORECASE,
            )
        )
        ok = (
            completed.returncode == 0
            and pdf.is_file()
            and pdf.stat().st_size > 0
            and page_count > 0
            and not undefined
        )
        bundle_pdf = PDF_DIR / f"{name}.pdf"
        if pdf.is_file() and pdf.stat().st_size > 0:
            shutil.copy2(pdf, bundle_pdf)

        results[name] = {
            "status": "PASS" if ok else "FAIL",
            "returncode": completed.returncode,
            "pdf_bytes": pdf.stat().st_size if pdf.is_file() else 0,
            "pdf_pages": page_count,
            "page_counter": page_counter,
            "pdf_sha256": sha256(pdf) if pdf.is_file() else None,
            "module_sha256": sha256(paper / "ROUND5_POSITIVE_CLOSURE.tex")
            if (paper / "ROUND5_POSITIVE_CLOSURE.tex").is_file()
            else None,
            "undefined_references_or_citations": undefined,
            "log": str(log_path.relative_to(ROOT)),
            "bundle_pdf": str(bundle_pdf.relative_to(ROOT)) if bundle_pdf.is_file() else None,
        }

        if ok:
            print(
                f"ROUND5_BUILD_PASS {name} pages={page_count} "
                f"counter={page_counter} pdf_bytes={pdf.stat().st_size}"
            )
        else:
            failures.append(name)
            blocks = concise_context(completed.stdout)
            failure_blocks += [
                f"## {name}",
                "",
                f"- latexmk return code: `{completed.returncode}`",
                f"- page count: `{page_count}` via `{page_counter}`",
                f"- PDF exists: `{pdf.is_file()}`",
                f"- undefined references/citations: `{undefined}`",
                "",
                "```text",
            ]
            failure_blocks += blocks
            failure_blocks += ["```", ""]
            print(
                f"ROUND5_BUILD_FAIL_BEGIN {name} "
                f"returncode={completed.returncode} pages={page_count} "
                f"counter={page_counter} pdf_exists={pdf.is_file()} "
                f"undefined={undefined}",
                file=sys.stderr,
            )
            for block in blocks:
                print(block, file=sys.stderr)
                print("---", file=sys.stderr)
            print(f"ROUND5_BUILD_FAIL_END {name}", file=sys.stderr)

    summary = {
        "schema": "theta-theory-round5-build-v1",
        "status": "PASS" if not failures else "FAIL",
        "paper_count": len(PAPER_NAMES),
        "passed": len(PAPER_NAMES) - len(failures),
        "failed": failures,
        "papers": results,
    }
    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    failure_output = (
        failure_blocks
        if failures
        else [
            "# Round-five build failures",
            "",
            "None. All eleven manuscripts clean-built with resolved references and citations.",
            "",
        ]
    )
    FAILURES_PATH.write_text("\n".join(failure_output), encoding="utf-8")

    if failures:
        print(
            f"ROUND5_BUILD_SUMMARY_FAIL passed={summary['passed']}/11 "
            f"failed={','.join(failures)}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print("ROUND5_BUILD_SUMMARY_PASS 11/11")


if __name__ == "__main__":
    main()
