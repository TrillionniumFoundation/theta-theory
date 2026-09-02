#!/usr/bin/env python3
"""Activate Round-Twenty-Three sources in all eleven manuscript wrappers.

The script is intentionally idempotent.  It changes only the declared wrappers,
keeps all historical sources in place, and never reports mathematical validity.
"""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAPERS = (
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
)

OLD_INPUTS = (
    "ROUND17_POSITIVE_CLOSURE.tex",
    "ROUND21_POSITIVE_CLOSURE.tex",
    "ROUND21_REPLACEMENT.tex",
)
NEW_INPUT = "ROUND23_POSITIVE_CLOSURE.tex"
BIB_LINE = r"\addbibresource{../../ROUND23_REFERENCES.bib}"


def activate(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    for old in OLD_INPUTS:
        text = text.replace(old, NEW_INPUT)

    # Fail closed if no recognizable input slot exists.
    if NEW_INPUT not in text:
        raise RuntimeError(f"{path}: no recognized active source input")

    if "ROUND23_REFERENCES.bib" not in text:
        marker = r"\begin{document}"
        if marker not in text:
            raise RuntimeError(f"{path}: missing document marker")
        text = text.replace(marker, BIB_LINE + "\n\n" + marker, 1)

    replacements = {
        "Round-Twenty-One": "Round-Twenty-Three",
        "Round Twenty One": "Round Twenty Three",
        "Round-21": "Round-23",
        "Round 21": "Round 23",
        "round-twenty-one": "round-twenty-three",
        "round twenty one": "round twenty three",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    date_line = r"\date{Round-Twenty-Three Revision -- 2 September 2026}"
    if re.search(r"\\date\{[^\n]*\}", text):
        text = re.sub(r"\\date\{[^\n]*\}", lambda _m: date_line, text, count=1)
    elif r"\begin{document}" in text:
        text = text.replace(r"\begin{document}", date_line + "\n\n" + r"\begin{document}", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed: list[str] = []
    for paper in PAPERS:
        source = ROOT / "papers" / paper / NEW_INPUT
        wrapper = ROOT / "papers" / paper / "main.tex"
        if not source.is_file():
            raise FileNotFoundError(source)
        if not wrapper.is_file():
            raise FileNotFoundError(wrapper)
        if activate(wrapper):
            changed.append(str(wrapper.relative_to(ROOT)))

    print(f"Round 23 wrappers checked: {len(PAPERS)}")
    if changed:
        print("Activated:")
        for path in changed:
            print(f"  {path}")
    else:
        print("All wrappers were already active.")


if __name__ == "__main__":
    main()
