#!/usr/bin/env python3
"""Fail-closed structural and regression verifier for round-four closure."""
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"

REQUIRED = {
    "A1-exact-benchmarks": [
        "Standing model and notation",
        "Cut-port Hamiltonian suspension",
        "Exact cut-port symplecticity",
        "Conditional Kolmogorov--Nagumo classification",
        "Mechanical calibration of the exponential coefficient",
    ],
    "A2-sinai-homological-pressure": [
        "Current-augmented moving-cut bundle",
        "Frequency-adapted Dolgopyat contraction",
        "Uniform return and cancellation block",
        "Uniform Liv\\v{s}ic alternative and covariance",
        "fixed \\(C^\\infty\\) mollifier of width one",
    ],
    "A3-full-empirical-path-ldp": [
        "Survivor pressure limit",
        "Defect-completed collision pressure",
        "Rate-dense exposed collision phases",
        "Radon annihilator and Hausdorff cotangent",
        "No macroscopic excursion is discarded",
    ],
    "A4-history-memory-universal-pressure": [
        "Volterra construction of the exact memory",
        "Minimal realization of the pole part",
        "Exact nonlinear Doob tower",
        "Prepared rough diffusion with resolved memory",
    ],
    "B1-microcanonical-preparation": [
        "one-label sector",
        "Singleton pressure gap",
        "Singleton-dominated mixed lattice--continuous coefficient",
        "Source-uniform shell coefficient",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "First-cycle witness atlas",
        "Ancestral contact ledger",
        "All-contact forest domination",
        "forgetful surgery",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        "Energy-compatible primal and Radon dual spaces",
        "Radon path-space Fenchel duality",
        "Exact Radon gauge complex",
        "Nuclear-space joint density--collision Gaussian tangent",
        "Mitoma and increment bounds",
    ],
    "B4-nonlinear-kinetic-semigroups": [
        "stable hierarchy functional algebra",
        "Backward connected Duhamel correctors",
        "Energy compactness and exponential containment",
        "Microcanonical dynamics on the conserved constraint surface",
    ],
    "C1-information-risk-sensitive-saddles": [
        "exact block-normalized canonical law control",
        "Uniform conditional source chart",
        "Almost-sure odds and expected posterior selection",
        "Chernoff rate",
        "LAN and Bernstein--von Mises tangent",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        "Direct-pressure continuity ledger",
        "Coercive strict dual and phase compactness",
        "Stable resolved filtrations and deterministic-to-diffusion likelihoods",
        "Kernel and filtration convergence",
        "Linearized history pressure and compressed memory",
    ],
    "D1-deterministic-theta-contractions": [
        "Normalized analytic--convex commutation theorem",
        "-\\inf_{Cx=a}I(x)",
        "Finite-mean Gaussian tangents and exact local likelihoods",
        "m_{\\varepsilon,\\Theta}=DQ_\\varepsilon(\\Theta)",
        "expectation one for every \\(\\varepsilon\\)",
    ],
}

FORBIDDEN = {
    "A1-exact-benchmarks": [
        r"\mathcal S=\mathbb T^2",
        r"H_i^a(q,p)=-(\log w_i(a))qp",
        "Autonomous Hamiltonian impact network",
    ],
    "A2-sinai-homological-pressure": [
        r"(a,b)=\nabla P_R(\xi,s)",
        r"Lemma~\ref{thm:r3-a2-high}",
        "one-step expansion sum is at most",
    ],
    "A3-full-empirical-path-ldp": [
        r"r1_{\{r>L\}}",
        "replace every long symbol by a fixed connector symbol",
        "ordinary empirical block measure" + " gives the full LDP",
    ],
    "A4-history-memory-universal-pressure": [
        r"-\log P_t^\Psi\mathbf1",
        "adjoining the finitely many corresponding exponential modes to the resolved space",
        "unique causal, locally integrable operator-valued distribution",
    ],
    "B1-microcanonical-preparation": [
        "cubes of side\n\\(L\\varepsilon\\)",
        "Select \\(c\\mu_\\varepsilon\\) disjoint safe cubes",
        "fixed positive fraction of cubes are insertion-safe",
    ],
    "B2-collision-clusters-dynamic-ldp": [
        "factorial is the volume of the ordered cycle-time simplex",
        "remaining \\(c-1\\) cycle occurrences",
        "independent geometric gains",
    ],
    "B3-hamilton-boltzmann-cotangents": [
        "Fix \\(m>6\\)",
        "exponential Orlicz heart",
        r"z=n1_B",
    ],
    "B4-nonlinear-kinetic-semigroups": [
        r"1+|v|^m",
        "positive multiple of \\(1+|v|^m\\)",
        "polynomial weight grows only through free transport",
        "lifted static saddle",
    ],
    "C1-information-risk-sensitive-saddles": [
        r"-\mu_\varepsilon\int(q^{u,v}-1)dA_{\pi^\varepsilon}",
        "expected posterior" + " has the relative-entropy exponent",
        "posterior vector is an exact finite-dimensional filter" + ";",
    ],
    "C2-cotangent-rigidity-tangent-representations": [
        r"D\mathcal E_t^\Psi(0)[A](B)",
        r"[P(z-L_\Psi)^{-1}P]^{-1}",
        "long blocks, singularity neighborhoods, and clock residuals have arbitrarily large exponential cost",
    ],
    "D1-deterministic-theta-contractions": [
        r"\mathcal X_\varepsilon-m_\Theta",
        r"\inf_{Tx=y,\ Cx=a}I(x)\n =\left((Q^a\circ T^*)^*\right)(y)",
        "local uniform convergence gives the required central-limit centering rate",
    ],
}

THEOREM_ENVS = ("theorem", "lemma", "proposition", "corollary")


def verify_paper(name: str) -> dict:
    path = PAPERS / name / "ROUND3_POSITIVE_CLOSURE.tex"
    if not path.is_file():
        raise SystemExit(f"missing controlling module: {path}")
    text = path.read_text(encoding="utf-8")
    missing = [m for m in REQUIRED[name] if m not in text]
    present_forbidden = [m for m in FORBIDDEN[name] if m in text]
    if missing:
        raise SystemExit(f"{name}: missing round-four markers: {missing}")
    if present_forbidden:
        raise SystemExit(f"{name}: forbidden old proof language remains: {present_forbidden}")
    controls = sorted({ord(c) for c in text if ord(c) < 32 and c != "\n"})
    if controls:
        raise SystemExit(f"{name}: ASCII control bytes {controls}")

    labels = re.findall(r"\\label\{([^}]+)\}", text)
    duplicates = sorted({x for x in labels if labels.count(x) > 1})
    if duplicates:
        raise SystemExit(f"{name}: duplicate labels: {duplicates}")
    refs = re.findall(r"\\(?:ref|eqref|cref|Cref)\{([^}]+)\}", text)
    unresolved = sorted({x for x in refs if x not in set(labels)})
    if unresolved:
        raise SystemExit(f"{name}: unresolved local references: {unresolved}")

    counts = {}
    theorem_total = 0
    for env in THEOREM_ENVS:
        b = text.count(f"\\begin{{{env}}}")
        e = text.count(f"\\end{{{env}}}")
        if b != e:
            raise SystemExit(f"{name}: unmatched {env}: {b}/{e}")
        counts[env] = b
        theorem_total += b
    proofs = text.count("\\begin{proof}")
    proof_ends = text.count("\\end{proof}")
    if proofs != proof_ends:
        raise SystemExit(f"{name}: unmatched proofs: {proofs}/{proof_ends}")
    if proofs < theorem_total:
        raise SystemExit(
            f"{name}: theorem-like environments exceed proofs: {theorem_total}/{proofs}"
        )
    if "Round-four referee closure" not in text:
        raise SystemExit(f"{name}: section title was not promoted to round four")
    return {
        "bytes": len(text.encode("utf-8")),
        "lines": text.count("\n") + 1,
        "labels": len(labels),
        "references": len(refs),
        "theorem_like_environments": theorem_total,
        "proofs": proofs,
        "required_markers": len(REQUIRED[name]),
        "forbidden_regressions": 0,
    }


def main() -> None:
    if set(REQUIRED) != set(FORBIDDEN):
        raise SystemExit("required/forbidden paper registries differ")
    papers = {name: verify_paper(name) for name in REQUIRED}
    result = {
        "schema": "theta-theory-round4-referee-verification-v1",
        "status": "PASS",
        "papers": papers,
        "paper_count": len(papers),
        "total_theorem_like_environments": sum(
            p["theorem_like_environments"] for p in papers.values()
        ),
        "total_proofs": sum(p["proofs"] for p in papers.values()),
    }
    out = ROOT / "ROUND4_STRUCTURAL_VERIFICATION.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        "ROUND4_STRUCTURAL_VERIFICATION_PASS "
        f"papers={len(papers)} theorems={result['total_theorem_like_environments']} "
        f"proofs={result['total_proofs']}"
    )


if __name__ == "__main__":
    main()
