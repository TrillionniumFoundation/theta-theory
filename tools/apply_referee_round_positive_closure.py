#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re
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
MARKER = "% REFEREE_ROUND2_POSITIVE_CLOSURE"

def patch_main(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return
    supplement = (
        "\n" + MARKER + "\n"
        "\\input{REFEREE_REVISION_ADDENDUM.tex}\n"
    )
    if "\\printbibliography" in text:
        text = text.replace("\\printbibliography", supplement + "\\printbibliography", 1)
    elif "\\end{document}" in text:
        text = text.replace("\\end{document}", supplement + "\\end{document}", 1)
    else:
        raise RuntimeError(f"no insertion point in {path}")
    path.write_text(text, encoding="utf-8")

def append_once(path: Path, heading: str, body: str) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if heading in text:
        return
    path.write_text(text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n",
                    encoding="utf-8")

def verify_addendum(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    theorem_like = len(re.findall(r"\\begin\{(?:theorem|lemma|proposition|corollary)\}", text))
    proofs = text.count("\\begin{proof}")
    if theorem_like == 0 or theorem_like != proofs:
        raise RuntimeError(
            f"{path}: theorem/proof mismatch {theorem_like}/{proofs}"
        )
    if "TODO" in text or "Proof sketch" in text or "left to the reader" in text:
        raise RuntimeError(f"{path}: forbidden proof placeholder")

for paper in PAPERS:
    folder = ROOT / "papers" / paper
    for required in [
        folder / "main.tex",
        folder / "references.bib",
        folder / "REFEREE_REPORT.md",
        folder / "REFEREE_REPORT_GPT56_PRO.md",
        folder / "REFEREE_REVISION_ADDENDUM.tex",
    ]:
        if not required.exists():
            raise RuntimeError(f"missing {required}")
    verify_addendum(folder / "REFEREE_REVISION_ADDENDUM.tex")
    patch_main(folder / "main.tex")
    append_once(
        folder / "README.md",
        "## Second referee-round revision",
        "The controlling `main.tex` includes `REFEREE_REVISION_ADDENDUM.tex`. "
        "The addendum responds theorem-by-theorem to both independent reports. "
        "The report files remain unchanged as review provenance."
    )
    append_once(
        folder / "REFEREE_GUIDE.md",
        "## Round-two positive-closure checks",
        "- verify the new addendum in the compiled PDF;\n"
        "- check every new theorem against both report files;\n"
        "- check cross-paper dependencies against `REVISION_MANIFEST.yaml`;\n"
        "- do not treat successful compilation as mathematical certification."
    )

# Root README receives a branch-specific review notice.
append_once(
    ROOT / "README.md",
    "## Referee round-two revision branch",
    "On `revision/referee-round-positive-closure-11paper-2026-08-30`, all "
    "eleven controlling manuscripts include a positive-closure addendum. "
    "The exact branch head, build result, and external rereview status are "
    "recorded in `REVISION_STATUS.md`."
)

# Fail closed on coverage.
included = 0
for paper in PAPERS:
    text = (ROOT / "papers" / paper / "main.tex").read_text(encoding="utf-8")
    included += MARKER in text
if included != 11:
    raise RuntimeError(f"only {included}/11 controlling manuscripts include addenda")

print("APPLY_REFEREE_ROUND2_PASS")
