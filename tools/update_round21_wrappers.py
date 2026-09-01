#!/usr/bin/env python3
"""Update all eleven manuscript wrappers to Round-Twenty-One metadata.

The active proof filename is retained for build compatibility, while its bytes
are replaced by the Round-Twenty-One mathematical module.
"""
from __future__ import annotations

from pathlib import Path
import re

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

for paper in PAPERS:
    path = ROOT / "papers" / paper / "main.tex"
    original = path.read_text(encoding="utf-8")
    output: list[str] = []
    response_written = False
    for line in original.splitlines():
        if line.startswith(r"\date{"):
            line = r"\date{September 2, 2026}"
        elif "Platform identifier:" in line:
            changed = re.sub(r"([vV])17(?=})", r"\g<1>21", line)
            if changed == line:
                changed = line.replace(r"}.\par", r"-R21}.\par", 1)
            line = changed
        elif "Controlling revision:" in line:
            line = (
                r"\noindent\textbf{Controlling revision:} "
                r"\texttt{ROUND21-REFEREE-POSITIVE-CLOSURE}.\par"
            )
        elif "Registered proof source:" in line:
            line = (
                r"\noindent\textbf{Registered proof source:} "
                r"\texttt{ROUND17\_POSITIVE\_CLOSURE.tex} "
                r"(Round-Twenty-One replacement in the legacy active-source slot).\par"
            )
            output.append(line)
            output.append(
                r"\noindent\textbf{Round-Twenty referee response:} "
                r"\texttt{AUTHOR\_RESPONSE\_ROUND20.md}.\par"
            )
            response_written = True
            continue
        if "AUTHOR_RESPONSE_ROUND20.md" in line:
            response_written = True
        output.append(line)

    text = "\n".join(output) + "\n"
    text = text.replace(
        "Cross-paper inputs follow the Round-Seventeen dependency ledger.",
        "Cross-paper inputs follow the Round-Twenty-One dependency ledger.",
    )
    text = text.replace(
        "Cross-paper inputs follow the Round-Seventeen proof dependency ledger.",
        "Cross-paper inputs follow the Round-Twenty-One proof dependency ledger.",
    )
    if not response_written:
        text = text.replace(
            r"\tableofcontents",
            r"\noindent\textbf{Round-Twenty referee response:} "
            r"\texttt{AUTHOR\_RESPONSE\_ROUND20.md}.\par" + "\n"
            r"\tableofcontents",
            1,
        )
    required = [
        "ROUND21-REFEREE-POSITIVE-CLOSURE",
        "Round-Twenty-One replacement",
        "AUTHOR\\_RESPONSE\\_ROUND20.md",
        r"\input{ROUND17_POSITIVE_CLOSURE.tex}",
    ]
    missing = [token for token in required if token not in text]
    if missing:
        raise SystemExit(f"{path}: wrapper update missing tokens {missing}")
    path.write_text(text, encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")
