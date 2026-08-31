#!/usr/bin/env python3
"""Materialize the round-nine positive referee reconstruction for eleven papers."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "revision" / "round9-referee-final"
PAPERS = ROOT / "papers"

REGISTRY: dict[str, dict[str, str]] = {
    "A1-exact-benchmarks": {
        "source": "A1_PHYSICAL_IMPACT_DIRECTIONAL_RESPONSE.tex",
        "platform": "A1-HAM-IMPACT-v3",
        "abstract": """We separate the physical two-dimensional Liouville section from its Cantor symbolic natural extension.  The generalized baker map is realized as an autonomous Hamiltonian impact suspension on the regular physical section, while all generated seam currents are controlled on a directional two-sided anisotropic scale.  This yields finite-order physical response and a conditional canonical-cocycle calibration without treating symbolic endpoint germs as smooth phase points.""",
    },
    "A2-sinai-homological-pressure": {
        "source": "A2_BLOWUP_UNI_DENSITY_LLT.tex",
        "platform": "TL2-HOM-v3",
        "abstract": """For a compact finite-horizon Sinai family we construct a parabolically blown-up moving-cut bundle with a material connection through branch births.  Compact-frequency arithmetic is certified by a finite chartwise periodic packet, whereas high-frequency contraction follows from a separate returned-branch temporal nonintegrability theorem.  A density-level vector--roof local limit theorem gives sharp lattice/continuous windows with the correct scaling.""",
    },
    "A3-full-empirical-path-ldp": {
        "source": "A3_POINTED_EDGE_FLOW_LDP.tex",
        "platform": "TL3-LPATH-v3",
        "abstract": """We prove collision- and physical-time empirical-path large deviations on a state retaining the actual inducing edge, actual excursion profile, return-step intensity, and pointed terminal excursion.  Finite marked-flow LDPs, a common projective recovery construction, an actual recession epigraph, and a renewal spectral/recession dichotomy produce a good full rate without forgetting the transition data needed for entropy.""",
    },
    "A4-history-memory-universal-pressure": {
        "source": "A4_PAST_KERNEL_DISTRIBUTIONAL_MEMORY.tex",
        "platform": "TL3-HIST-v3",
        "abstract": """A genuine natural-extension past, rather than a future-determining stable quotient, carries the prepared history process.  We prove a weighted Feller kernel and a quenched enhanced invariance principle.  Exact memory is obtained from the full compressed resolvent with the causal sign; instantaneous Dirac terms are separated from an exponentially decaying regular residual, and finite principal parts are realized without discarding the unresolved space.""",
    },
    "B1-microcanonical-preparation": {
        "source": "B1_FULL_PRESSURE_WEIGHTED_SHELL.tex",
        "platform": "HSBG-LIO-v3",
        "abstract": """Microcanonical preparation is derived from the full connected hard-sphere source pressure, not an ideal compound proxy.  Conditional regenerative full-rank blocks give a global mixed lattice--continuous characteristic theorem, typical activity gives uniform covariance, and an exact source-dependent saddle is retained.  The shell likelihood remains inside the Gaussian coefficient, yielding the prepared pressure, LDP, and covariance Schur complement at every declared shell scale.""",
    },
    "B2-collision-clusters-dynamic-ldp": {
        "source": "B2_TRACE_JACOBI_SEWING_LDP.tex",
        "platform": "HSBG-LIO-v3",
        "abstract": """We construct a compatible measure-valued kinetic normal-trace graph and its positive boundary-renewal hierarchy.  Recollisions are controlled in the actual chronological variables by a flux-weighted exterior-power estimate for the physical hard-sphere Jacobi cocycle, followed by factorial collision-tree summation.  A source-uniform scaled block theorem and an exactly conservative finite-cell recovery yield the good grand-canonical and microcanonical density--actual-contact LDPs.""",
    },
    "B3-hamilton-boltzmann-cotangents": {
        "source": "B3_KKT_COVARIANCE_OBSERVABILITY.tex",
        "platform": "HSBG-LIO-v3",
        "abstract": """The raw perspective-entropy Hessian may be indefinite.  On a regular short-time constrained phase we add the KKT multiplier curvature and prove coercivity from an explicit linearized kinetic energy estimate.  Finite-volume marked cumulants construct the Gaussian covariance first; backward observability identifies the complete balance gauge, and second-order Mosco convergence identifies the covariance with the closed constrained tangent form.""",
    },
    "B4-nonlinear-kinetic-semigroups": {
        "source": "B4_LAW_CORE_TRUNCATED_COMPARISON.tex",
        "platform": "HSBG-LIO-v3",
        "abstract": """The exact finite state is the probability law on the hard-sphere configuration augmented by its actual-contact ledger.  A Yosida resolvent graph core and finite-generator correlation correctors give the Hamilton--Boltzmann nonlinear-generator limit.  The transition action contains only dynamic entropy, and comparison is proved by bounded contact-ratio truncation followed by monotone removal of the truncation, yielding the unique kinetic semigroup and its microscopic limit.""",
    },
    "C1-information-risk-sensitive-saddles": {
        "source": "C1_EVIDENCE_CURRENT_BELIEF_DPP.tex",
        "platform": "HSBG-CONTROL-v3",
        "abstract": """Repeated noiseless observations are represented by an arbitrary-codimension current tower and an unnormalized evidence-bearing belief state.  We prove the exact belief DPP, a two-saddle coarea/shell coefficient with separate numerator and denominator determinants, and exponential evidence containment.  Reduction to kinetic variables is restricted to a strategy-reachable phase-chaotic class which retains phase weights and the finite correlation skeleton created by exact conditioning.""",
    },
    "C2-cotangent-rigidity-tangent-representations": {
        "source": "C2_SCALE_CONNECTION_RESOLVED_MEMORY.tex",
        "platform": "TYPED-COPRODUCT-v3",
        "abstract": """Invariant-integral and normalized-pressure nullspaces are defined as closed linear spans and characterized by a weighted invariant-separator theorem.  Source response is transported on a common strong--weak transfer scale by Kato's connection, without Radon--Nikodym trivialization of mutually singular phases.  The phase spectral projector and the resolved memory projection are kept distinct, giving the correct covariant compressed-resolvent derivative, optional-projection limit, and nonlinear cotangent chain rule.""",
    },
    "D1-deterministic-theta-contractions": {
        "source": "D1_EXACT_PHASE_LABEL_MIXTURE.tex",
        "platform": "LABELLED-COMMUTE-v3",
        "abstract": """Phase coexistence is represented by an exact microscopic labelled mixture of genuine phase-restricted laws.  The physical rate is obtained by contracting the joint label/state LDP, not by conjugating a maximum pressure, and phase-local complex charts remain compatible with Lee--Yang pinching.  Labelled projective passage, thin-shell conditioning, exact finite-centred likelihoods, and nonlinear values form a standalone commutation theorem.""",
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def materialize(paper_name: str, meta: dict[str, str]) -> dict[str, object]:
    paper = PAPERS / paper_name
    main = paper / "main.tex"
    source = SRC / meta["source"]
    response = paper / "AUTHOR_RESPONSE_ROUND9.md"
    if not main.is_file() or not source.is_file() or not response.is_file():
        raise SystemExit(f"missing round-nine input for {paper_name}")

    old = main.read_text(encoding="utf-8")
    marker = r"\begin{document}"
    if marker not in old:
        raise SystemExit(f"no document boundary in {main}")
    preamble = old.split(marker, 1)[0].rstrip()
    source_bytes = source.read_bytes()
    module = paper / "ROUND9_POSITIVE_CLOSURE.tex"
    module.write_bytes(source_bytes)

    body = (
        preamble + "\n" + marker + "\n\\raggedbottom\n"
        + "\\begin{abstract}\n" + meta["abstract"].strip() + "\n\\end{abstract}\n"
        + "\\maketitle\n"
        + "\\noindent\\textbf{Platform identifier:} \\texttt{" + meta["platform"] + "}.\n"
        + "\\noindent\\textbf{Controlling revision:} \\texttt{ROUND9-REFEREE-POSITIVE-CLOSURE}.\n"
        + "\\tableofcontents\n\n"
        + "\\input{ROUND9_POSITIVE_CLOSURE.tex}\n\n"
        + "\\section*{Scope and verification status}\n"
        + "This manuscript states positive theorem closure in the declared model-specific regular regime. "
        + "Every cross-paper input is typed in the round-nine dependency ledger.  Repository proof and build gates "
        + "are internal checks and do not replace independent external mathematical review.\n"
        + "\\printbibliography\n\\end{document}\n"
    )
    main.write_text(body, encoding="utf-8")

    for old_module in paper.glob("ROUND[0-8]_POSITIVE_CLOSURE.tex"):
        old_module.unlink()

    return {
        "paper": paper_name,
        "source": str(source.relative_to(ROOT)),
        "source_sha256": sha256(source_bytes),
        "module": str(module.relative_to(ROOT)),
        "module_sha256": sha256(module.read_bytes()),
        "response": str(response.relative_to(ROOT)),
        "platform": meta["platform"],
    }


def main() -> None:
    entries = [materialize(name, meta) for name, meta in REGISTRY.items()]
    manifest = {
        "schema": "theta-theory-round9-materialization-v1",
        "review_branch": "review/round8-gpt56-pro-harsh-11paper-2026-08-31",
        "review_head": "57349d5b8f042fd995b37a369f71af7f22f6acdb",
        "revision_branch": "revision/round9-referee-positive-closure-11paper-2026-08-31",
        "policy": {
            "positive_reconstruction": True,
            "no_downgrade": True,
            "no_nogo_substitution": True,
            "historical_status_not_theorem_credit": True,
        },
        "papers": entries,
    }
    (ROOT / "ROUND9_MATERIALIZATION_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"ROUND9_MATERIALIZATION_PASS papers={len(entries)}")


if __name__ == "__main__":
    main()
