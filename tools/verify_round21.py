#!/usr/bin/env python3
"""Fail-closed structural verifier for the Round-Twenty-One source tree.

This checks source identity, theorem/proof structure, superseded mechanisms,
and the declared acyclic dependency order.  A PASS is an internal source gate,
not mathematical peer review.
"""
from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = {
    "A1": "papers/A1-exact-benchmarks",
    "A2": "papers/A2-sinai-homological-pressure",
    "A3": "papers/A3-full-empirical-path-ldp",
    "A4": "papers/A4-history-memory-universal-pressure",
    "B1": "papers/B1-microcanonical-preparation",
    "B2": "papers/B2-collision-clusters-dynamic-ldp",
    "B3": "papers/B3-hamilton-boltzmann-cotangents",
    "B4": "papers/B4-nonlinear-kinetic-semigroups",
    "C1": "papers/C1-information-risk-sensitive-saddles",
    "C2": "papers/C2-cotangent-rigidity-tangent-representations",
    "D1": "papers/D1-deterministic-theta-contractions",
}

REQUIRED_ROOT = [
    "ROUND21_HISTORICAL_DERIVATION_AUDIT.md",
    "ROUND21_PROOF_DEPENDENCY_LEDGER.md",
    "ROUND21_INTERNAL_HARSH_REREVIEW.md",
    "REFEREE_ROUND20_RESPONSE.md",
]

# Exact fragments encoding superseded proof mechanisms.  This scan is
# restricted to the active TeX modules, so reports may discuss the old errors.
FORBIDDEN = {
    "linear nonlinear-resolvent identity": r"R_\\lambda-R_\\mu\s*=",
    "negative Sobolev restriction by duality":
        r"duality gives the asserted maps\s*on negative",
    "unweighted countable branch sum":
        r"\\sum_h\s*e\^\{\\eta r_h\}\s*\\bigl\(\\\|J_h",
    "factorial silently discarded":
        r"k!C\^kT\^\{k-1\}.*?\\sum_k\s*C\^kT",
    "separately optimized latent components":
        r"\\log\\sum_j\\rho\(j\).*?S_t\^j",
    "false cutoff H1v target":
        r"H\^1_\{x,v,w\}.*?\\int\s*\|\\Delta p\|\^2",
}

MAIN_LABEL = {key: f"thm:r21-{key.lower()}-main" for key in PAPERS}

# Edges point from prerequisite to dependent node.  B2 is split logically into
# its grand-canonical and microcanonical stages to expose any B1 cycle.
NODES = [
    "A1", "A2", "A3", "A4", "B2-GC", "B1", "B2-MC", "B3", "B4",
    "C1", "C2", "D1",
]
EDGES = [
    ("A2", "A3"), ("A3", "A4"),
    ("B2-GC", "B1"), ("B1", "B2-MC"),
    ("B2-GC", "B2-MC"), ("B2-MC", "B3"), ("B3", "B4"),
    ("A2", "C1"), ("A3", "C1"), ("A4", "C1"),
    ("B1", "C1"), ("B2-GC", "C1"), ("B2-MC", "C1"),
    ("B3", "C1"), ("B4", "C1"),
    ("A3", "C2"), ("A4", "C2"), ("B3", "C2"),
    ("B4", "C2"), ("C1", "C2"),
]
for parent in [
    "A1", "A2", "A3", "A4", "B1", "B2-GC", "B2-MC", "B3", "B4",
    "C1", "C2",
]:
    EDGES.append((parent, "D1"))


def fail(message: str) -> None:
    print(f"ROUND21_VERIFY_FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_dependency_graph() -> None:
    indegree = {node: 0 for node in NODES}
    children: dict[str, list[str]] = defaultdict(list)
    for left, right in EDGES:
        if left not in indegree or right not in indegree:
            fail(f"unknown dependency node {left}->{right}")
        children[left].append(right)
        indegree[right] += 1
    queue = deque(node for node, degree in indegree.items() if degree == 0)
    seen: list[str] = []
    while queue:
        node = queue.popleft()
        seen.append(node)
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(seen) != len(NODES):
        fail("declared proof dependency graph contains a cycle")
    print("dependency_order=" + " -> ".join(seen))


def check_balanced(text: str, name: str, begin: str, end: str) -> None:
    depth = 0
    events: list[tuple[int, int, int, int, str]] = []
    first_negative: tuple[int, str] | None = None
    for number, line in enumerate(text.splitlines(), start=1):
        opens = line.count(begin)
        closes = line.count(end)
        if opens or closes:
            depth += opens - closes
            events.append((number, opens, closes, depth, line.strip()))
            if depth < 0 and first_negative is None:
                first_negative = (number, line.strip())
    if depth != 0 or first_negative is not None:
        print(
            f"ROUND21_BALANCE_DIAGNOSTIC paper={name} begin={begin!r} "
            f"end={end!r} final_depth={depth}",
            file=sys.stderr,
        )
        if first_negative is not None:
            print(
                f"first_negative_line={first_negative[0]} text={first_negative[1]!r}",
                file=sys.stderr,
            )
        for number, opens, closes, running, line in events:
            print(
                f"line={number} opens={opens} closes={closes} "
                f"depth={running} text={line!r}",
                file=sys.stderr,
            )
        fail(f"{name}: unbalanced {begin}/{end}")


def check_transport_corruption(text: str, name: str) -> None:
    suspicious = {
        "form-feed": "\x0c",
        "vertical-tab": "\x0b",
        "carriage-return": "\r",
        "truncated-frac": "rac12",
    }
    for label, token in suspicious.items():
        if token not in text:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            if token in line:
                print(
                    f"ROUND21_TRANSPORT_DIAGNOSTIC paper={name} "
                    f"kind={label} line={number} text={line!r}",
                    file=sys.stderr,
                )
        fail(f"{name}: source transport corruption detected ({label})")


def main() -> None:
    for rel in REQUIRED_ROOT:
        path = ROOT / rel
        if not path.is_file() or path.stat().st_size < 500:
            fail(f"missing or empty root evidence file: {rel}")

    all_active: list[str] = []
    for key, rel_dir in PAPERS.items():
        folder = ROOT / rel_dir
        main_tex = folder / "main.tex"
        active = folder / "ROUND17_POSITIVE_CLOSURE.tex"
        response = folder / "AUTHOR_RESPONSE_ROUND20.md"
        for path in (main_tex, active, response):
            if not path.is_file():
                fail(f"{key}: missing {path.relative_to(ROOT)}")
        main_text = main_tex.read_text(encoding="utf-8")
        if "\\input{ROUND17_POSITIVE_CLOSURE.tex}" not in main_text:
            fail(f"{key}: main.tex does not input the active source")
        text = active.read_text(encoding="utf-8")
        all_active.append(text)
        if "Round-twenty-one positive closure" not in text:
            fail(f"{key}: active source is not the Round-Twenty-One replacement")
        if MAIN_LABEL[key] not in text:
            fail(f"{key}: missing main theorem label {MAIN_LABEL[key]}")
        theorem_count = text.count("\\begin{theorem}")
        proof_count = text.count("\\begin{proof}")
        if theorem_count < 3:
            fail(f"{key}: fewer than three theorem environments")
        if proof_count < theorem_count:
            fail(f"{key}: fewer proof environments than theorem environments")
        check_balanced(text, key, "\\begin{proof}", "\\end{proof}")
        check_balanced(text, key, "\\[", "\\]")
        check_transport_corruption(text, key)
        if re.search(r"\b(TODO|TBD|FIXME|PLACEHOLDER)\b", text, re.I):
            fail(f"{key}: placeholder token in active proof")
        response_text = response.read_text(encoding="utf-8")
        if "Round Twenty" not in response_text and "Round-Twenty" not in response_text:
            fail(f"{key}: author response does not identify Round Twenty")
        print(
            f"paper={key} bytes={len(text.encode('utf-8'))} "
            f"theorems={theorem_count} proofs={proof_count}"
        )

    combined = "\n".join(all_active)
    for label, pattern in FORBIDDEN.items():
        if re.search(pattern, combined, re.S):
            fail(f"superseded mechanism recurs: {label}")

    ledger = (ROOT / "ROUND21_PROOF_DEPENDENCY_LEDGER.md").read_text(
        encoding="utf-8"
    )
    for key in PAPERS:
        if f"| {key} |" not in ledger:
            fail(f"dependency ledger has no row for {key}")
    check_dependency_graph()
    print("ROUND21_STRUCTURAL_VERIFY_PASS papers=11")


if __name__ == "__main__":
    main()
