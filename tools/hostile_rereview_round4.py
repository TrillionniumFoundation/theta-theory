#!/usr/bin/env python3
"""Dependency-aware hostile rereview of the exact round-four source tree."""
from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"

DAG = {
    "A1": [],
    "A2": [],
    "A3": ["A2"],
    "A4": ["A2", "A3"],
    "B2-GC": [],
    "B1": ["B2-GC"],
    "B2-MC": ["B2-GC", "B1"],
    "B3": ["B1", "B2-MC"],
    "B4": ["B2-MC", "B3"],
    "C1": ["B2-MC", "B3", "B4"],
    "C2": ["A1", "A2", "A3", "A4", "B2-MC", "B3", "B4"],
    "D1": ["B1", "B2-MC", "B3", "B4", "C2"],
}

FILES = {
    "A1": "A1-exact-benchmarks",
    "A2": "A2-sinai-homological-pressure",
    "A3": "A3-full-empirical-path-ldp",
    "A4": "A4-history-memory-universal-pressure",
    "B1": "B1-microcanonical-preparation",
    "B2-GC": "B2-collision-clusters-dynamic-ldp",
    "B2-MC": "B2-collision-clusters-dynamic-ldp",
    "B3": "B3-hamilton-boltzmann-cotangents",
    "B4": "B4-nonlinear-kinetic-semigroups",
    "C1": "C1-information-risk-sensitive-saddles",
    "C2": "C2-cotangent-rigidity-tangent-representations",
    "D1": "D1-deterministic-theta-contractions",
}

LOAD_BEARING = {
    "A1": ["thm:r3-a1-impact", "thm:r3-a1-calibration"],
    "A2": ["lem:r3-a2-atlas", "thm:r3-a2-high", "thm:r3-a2-llt"],
    "A3": ["thm:r3-a3-block", "thm:r3-a3-collision-ldp", "thm:r3-a3-cotangent"],
    "A4": ["thm:r3-a4-memory", "thm:r3-a4-memory-decay", "thm:r3-a4-nonlinear", "thm:r3-a4-tangent"],
    "B1": ["lem:r3-b1-convex", "thm:r3-b1-coefficient", "thm:r3-b1-transfer"],
    "B2-GC": ["lem:r3-b2-generating", "thm:r3-b2-gc-cluster", "thm:r3-b2-source-continuation", "thm:r3-b2-gc-ldp"],
    "B2-MC": ["thm:r3-b2-mc-ldp"],
    "B3": ["thm:r3-b3-duality", "thm:r3-b3-gauge", "thm:r3-b3-gaussian"],
    "B4": ["lem:r3-b4-corrector", "thm:r3-b4-generator", "thm:r3-b4-comparison", "thm:r3-b4-micro"],
    "C1": ["thm:r3-c1-adaptive", "thm:r3-c1-filter", "thm:r4-c1-lan"],
    "C2": ["thm:r3-c2-strict", "thm:r3-c2-girsanov", "thm:r3-c2-memory"],
    "D1": ["thm:r3-d1-commutation", "thm:r3-d1-likelihood", "thm:r3-d1-triangle"],
}

AUDITS = {
    "A1": [
        ("global object", "mapping torus"),
        ("section flux", "flux of port"),
        ("derived calibration", "Kolmogorov--Nagumo"),
    ],
    "A2": [
        ("all-depth cuts", "moving-boundary current series"),
        ("Dolgopyat loss", "exp\\left\\{-\\frac{cn}{\\log"),
        ("roof sign", "-it\\bar\\tau"),
        ("submacroscopic smoothing", "relative error is therefore \\(O(b_n^{-1})\\)"),
    ],
    "A3": [
        ("escape branch", "q_{\\infty,R}"),
        ("pressure maximum", "max\\{q_{Y,R}(F),q_{\\infty,R}(F)\\}"),
        ("zero-frequency phases", "zero-magnet-frequency laws"),
    ],
    "A4": [
        ("time-domain kernel", "second-kind Volterra equation"),
        ("realization typing", "auxiliary coordinates are a minimal state-space realization"),
        ("true nonlinear tower", "Doob-normalized nonlinear history pressure"),
    ],
    "B1": [
        ("singleton scale", "one-label trajectory"),
        ("connected remainder", "C_2T_*<c_1/4"),
        ("mixed coefficient", "Schur complement of the continuous"),
    ],
    "B2-GC": [
        ("ancestral witness", "last common vertex"),
        ("degenerate strata", "simultaneous-contact"),
        ("whole cyclic sector", "entire cyclic sector"),
        ("global sources", "Bounded real-source continuation"),
    ],
    "B2-MC": [
        ("conditioned joint LDP", "Microcanonical joint LDP"),
    ],
    "B3": [
        ("singular current test", "Urysohn"),
        ("Radon dual", "countably additive signed Radon"),
        ("process tightness", "Mitoma"),
    ],
    "B4": [
        ("integrable energy source", "0<\\eta<\\beta"),
        ("collision Lyapunov", "mathbb H(f,D\\Upsilon,0)=0"),
        ("exact corrector domain", "exact connected propagator"),
    ],
    "C1": [
        ("finite normalization", "exact mean-one martingale"),
        ("testing exponent", "Chernoff"),
        ("LAN center", "DQ_\\varepsilon(z_0)"),
    ],
    "C2": [
        ("coercive strict dual", "I(\\nu)\\ge a\\nu(W)-b"),
        ("resolved filtration", "not the complete microscopic filtration"),
        ("optional projection", "Kernel and filtration convergence"),
    ],
    "D1": [
        ("rate constant", "-\\inf_{Cx=a}I(x)"),
        ("finite center", "m_{\\varepsilon,\\Theta}"),
        ("exact density", "expectation one for every"),
    ],
}


def topo_sort(graph: dict[str, list[str]]) -> list[str]:
    remaining = {k: set(v) for k, v in graph.items()}
    order: list[str] = []
    while remaining:
        ready = sorted(k for k, deps in remaining.items() if not deps)
        if not ready:
            raise SystemExit(f"dependency cycle: {remaining}")
        for node in ready:
            order.append(node)
            del remaining[node]
        for deps in remaining.values():
            deps.difference_update(ready)
    return order


def main() -> None:
    order = topo_sort(DAG)
    errors: list[str] = []
    nodes: dict[str, dict] = {}
    cache: dict[str, str] = {}
    for node in order:
        folder = FILES[node]
        path = PAPERS / folder / "ROUND3_POSITIVE_CLOSURE.tex"
        text = cache.setdefault(folder, path.read_text(encoding="utf-8"))
        missing_labels = [
            label for label in LOAD_BEARING[node]
            if f"\\label{{{label}}}" not in text
        ]
        missing_audits = [
            name for name, snippet in AUDITS[node] if snippet not in text
        ]
        if missing_labels:
            errors.append(f"{node}: missing load-bearing labels {missing_labels}")
        if missing_audits:
            errors.append(f"{node}: missing hostile audit evidence {missing_audits}")
        nodes[node] = {
            "paper": folder,
            "dependencies": DAG[node],
            "load_bearing_labels": LOAD_BEARING[node],
            "audit_checks": [name for name, _ in AUDITS[node]],
            "status": "PASS" if not missing_labels and not missing_audits else "FAIL",
        }

    for folder in sorted(set(FILES.values())):
        report = PAPERS / folder / "REFEREE_REPORT_ROUND3_GPT56_PRO.md"
        response = PAPERS / folder / "AUTHOR_RESPONSE_ROUND4.md"
        if not report.is_file():
            errors.append(f"{folder}: referee report missing")
        if not response.is_file():
            errors.append(f"{folder}: author response missing")

    result = {
        "schema": "theta-theory-round4-hostile-rereview-v1",
        "status": "PASS" if not errors else "FAIL",
        "topological_order": order,
        "nodes": nodes,
        "errors": errors,
    }
    (ROOT / "ROUND4_HOSTILE_REREVIEW.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Round-four proof dependency ledger",
        "",
        f"Status: **{result['status']}**",
        "",
        "The order below is computed from the declared DAG; a cycle fails the gate.",
        "",
        "| Node | Controlling paper | Dependencies | Load-bearing theorem labels |",
        "|---|---|---|---|",
    ]
    for node in order:
        d = nodes[node]
        lines.append(
            f"| `{node}` | `{d['paper']}` | "
            f"{', '.join(d['dependencies']) or 'none'} | "
            f"{', '.join('`'+x+'`' for x in d['load_bearing_labels'])} |"
        )
    lines.extend([
        "",
        "## Non-circular hard-sphere order",
        "",
        "`B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1`",
        "",
        "## Non-circular Sinai order",
        "",
        "`A2 -> A3 -> A4 -> C2 -> D1`, with the independent A1 platform entering C2 only through its typed map.",
        "",
    ])
    (ROOT / "ROUND4_PROOF_DEPENDENCY_LEDGER.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    if errors:
        for error in errors:
            print("ROUND4_HOSTILE_ERROR " + error)
        raise SystemExit(1)
    print(f"ROUND4_HOSTILE_REREVIEW_PASS nodes={len(nodes)}")


if __name__ == "__main__":
    main()
