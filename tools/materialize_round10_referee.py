#!/usr/bin/env python3
"""Materialize the eleven Round-Ten controlling manuscripts deterministically."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "revision" / "round10-referee-final"

PAPERS: dict[str, dict[str, str]] = {
    "A1-exact-benchmarks": {
        "source": "A1_MAPPING_TORUS_ONE_SIDED_RESPONSE.tex",
        "abstract": (
            "We separate the physical generalized-baker section from its symbolic natural "
            "extension and realize the physical map by an exact mapping-torus Hamiltonian. "
            "Response is constructed from the two noninvertible one-sided Ruelle operators, "
            "with bounded Hadamard cut-current insertions for transported observables; no "
            "spectral gap is asserted for the bilateral Koopman shift.  The full-port work "
            "identity and the mechanical valuation coefficient remain explicitly conditional "
            "on equality of likelihood cocycles."
        ),
    },
    "A2-sinai-homological-pressure": {
        "source": "A2_EXPLICIT_CERTIFICATE_FOURIER_RANGES.tex",
        "abstract": (
            "For a compact finite-horizon periodic Lorentz family we construct a renormalized "
            "physical trace bundle through branch births, compute a finite family of explicit "
            "periodic arithmetic certificates, and prove geometric temporal nonintegrability "
            "from returned inverse branches.  A four-range Fourier theorem, including a "
            "separate very-high-frequency integration-by-parts regime, yields the vector--roof "
            "density local limit theorem and correctly separated local, central, saturated, "
            "and macroscopic window asymptotics."
        ),
    },
    "A3-full-empirical-path-ldp": {
        "source": "A3_DETERMINISTIC_SPEED_PROJECTIVE_FLOW_LDP.tex",
        "abstract": (
            "We formulate the induced empirical process at deterministic inducing-block speed. "
            "The state retains vertices, admissible edge flow, return and roof marks, and actual "
            "excursion path profiles.  Finite-core Markov large deviations pass through a "
            "projective exponential-tightness theorem, while an actual-excursion recession "
            "functional and terminal-profile clock surgery give full collision- and "
            "physical-time empirical-path large deviations."
        ),
    },
    "A4-history-memory-universal-pressure": {
        "source": "A4_DOOB_PAST_KERNEL_MEMORY.tex",
        "abstract": (
            "Prepared Sinai paths are conditioned on a genuine past-only natural-extension "
            "history.  The resulting future kernel is a weighted Feller semigroup and supports "
            "a correctly centered martingale--coboundary decomposition and quenched enhanced "
            "invariance principle.  Nonlinear history pressure is normalized by the positive "
            "Feynman--Kac eigenfunction, and exact resolved memory is obtained from the full "
            "unresolved-space compressed resolvent with the causal Volterra sign."
        ),
    },
    "B1-microcanonical-preparation": {
        "source": "B1_INTERIOR_SADDLE_REGENERATIVE_SHELL.tex",
        "abstract": (
            "We prove source-dependent microcanonical preparation for regular interior "
            "constraint targets satisfying an explicit affine-span condition.  Typical "
            "compound-Poisson activity gives the uniform covariance, while linearly many "
            "regenerative full-rank blocks yield a globally smooth Fourier component and an "
            "exponentially small nonsmoothing remainder.  The exact finite-volume saddle then "
            "gives the mixed lattice--continuous shell coefficient and prepared rate."
        ),
    },
    "B2-collision-clusters-dynamic-ldp": {
        "source": "B2_COMPATIBLE_TRACE_INTEGRATED_JACOBI_LDP.tex",
        "abstract": (
            "The hard-sphere hierarchy is built on the closed graph of compatible kinetic "
            "interior states and incoming flux traces.  Recollisions are controlled by an "
            "integrated small-singular-value estimate for the true physical Jacobi map rather "
            "than a coordinate reset or a pointwise depth bound.  A source-uniform one-block "
            "theorem, conservative balance repair, and exact actual-contact tilting yield the "
            "grand-canonical and source-conditioned microcanonical joint LDP."
        ),
    },
    "B3-hamilton-boltzmann-cotangents": {
        "source": "B3_COVARIANCE_FIRST_GAUGE_PROCESS.tex",
        "abstract": (
            "The raw perspective-entropy Hessian is not assumed positive.  We prove short-time "
            "coercivity directly on the balanced tangent by a weighted linearized Boltzmann "
            "energy estimate, construct covariance first from exact finite-volume cumulants, "
            "and identify its inverse with the second epi-derivative of the exposed rate.  A "
            "backward observability theorem closes the full balance gauge and localized "
            "connected cumulants give the prepared density--contact Gaussian process."
        ),
    },
    "B4-nonlinear-kinetic-semigroups": {
        "source": "B4_DYNAMIC_ACTION_GRAPH_CORE_COMPARISON.tex",
        "abstract": (
            "Microscopic states, Koopman observables, push-forward laws, ensemble log-Laplace "
            "values, and the limiting kinetic semigroup are kept distinct.  An observable "
            "resolvent core and full-hierarchy terminal correctors give the cylinder "
            "Hamiltonian, while the B2 dynamic action constructs the additive Lax--Oleinik "
            "semigroup without repeated preparation cost.  A two-scale coercive Tataru "
            "comparison and the prepared Laplace principle identify the microscopic limit."
        ),
    },
    "C1-information-risk-sensitive-saddles": {
        "source": "C1_STRATIFIED_EVIDENCE_FILTERING.tex",
        "abstract": (
            "Exact observations are represented by an arbitrary-codimension stratified current "
            "tower.  The state retains the unnormalized coarea current, its projective direction, "
            "and log evidence, so rare observations do not require a false uniform normalizer "
            "bound.  A Feller evidence kernel, a uniform coarea coefficient theorem, and a "
            "quantitatively reachable chaotic belief cluster yield the exact belief DPP, "
            "reduced kinetic game, and statistical tangent."
        ),
    },
    "C2-cotangent-rigidity-tangent-representations": {
        "source": "C2_COMMON_TRANSFER_BUNDLE_COTANGENTS.tex",
        "abstract": (
            "Invariant-integral and pressure null spaces are defined as closed linear spans. "
            "Platform-specific Cesaro Lyapunov bounds give invariant Radon separators.  Source "
            "response is transported on one common transfer-operator Banach bundle by Kato "
            "parallel transport, avoiding nonexistent infinite-path Radon--Nikodym densities; "
            "the resolved Hilbert projection is constructed separately and the covariant memory "
            "and optional-projection diagrams follow on their proper domains."
        ),
    },
    "D1-deterministic-theta-contractions": {
        "source": "D1_MICROSCOPIC_PHASE_DISINTEGRATION.tex",
        "abstract": (
            "We construct genuine positive finite-volume phase components on a common sample "
            "space and prove exact reconstruction of the physical law up to a "
            "superexponentially negligible remainder.  Phase-local analytic charts coexist with "
            "Lee--Yang pinching, while a microscopic subexponential mixture theorem—not a "
            "formal conjugacy of a maximum pressure—gives the minimum component rate.  The "
            "labelled projective LDP, shell coefficient, local likelihood, and contraction "
            "commutation then follow."
        ),
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def platform_from(old: str, fallback: str) -> str:
    m = re.search(r"\\textbf\{Platform identifier:\}\s*\\texttt\{([^}]+)\}", old)
    return m.group(1) if m else fallback


def materialize(folder: str, meta: dict[str, str]) -> dict[str, object]:
    paper = ROOT / "papers" / folder
    main = paper / "main.tex"
    source = SRC / meta["source"]
    if not main.is_file() or not source.is_file():
        raise SystemExit(f"missing source for {folder}: {main} / {source}")
    old = main.read_text(encoding="utf-8")
    boundary = r"\begin{document}"
    if boundary not in old:
        raise SystemExit(f"missing document boundary: {main}")
    preamble = old.split(boundary, 1)[0].rstrip()
    platform = platform_from(old, folder)
    active = paper / "ROUND10_POSITIVE_CLOSURE.tex"
    active.write_bytes(source.read_bytes())
    body = (
        preamble
        + "\n"
        + boundary
        + "\n\\raggedbottom\n"
        + "\\begin{abstract}\n"
        + meta["abstract"]
        + "\n\\end{abstract}\n"
        + "\\maketitle\n"
        + "\\noindent\\textbf{Platform identifier:} \\texttt{" + platform + "}.\n"
        + "\\noindent\\textbf{Controlling revision:} "
        + "\\texttt{ROUND10-REFEREE-POSITIVE-CLOSURE}.\n"
        + "\\noindent\\textbf{Registered proof source:} "
        + "\\texttt{" + meta["source"].replace("_", r"\_") + "}.\n"
        + "\\tableofcontents\n\n"
        + "\\input{ROUND10_POSITIVE_CLOSURE.tex}\n\n"
        + "\\section*{Scope and verification status}\n"
        + "This manuscript states positive theorem closure in the declared model-specific "
        + "regular regime.  Cross-paper inputs are used only in the acyclic order recorded "
        + "in the round-ten dependency ledger.  Repository source, proof-structure, "
        + "counterexample, and build gates are internal reproducibility checks; they do not "
        + "replace independent external mathematical review.\n"
        + "\\printbibliography\n"
        + "\\end{document}\n"
    )
    main.write_text(body, encoding="utf-8")
    return {
        "folder": folder,
        "registered_source": f"revision/round10-referee-final/{meta['source']}",
        "registered_sha256": sha256(source),
        "active_module": f"papers/{folder}/ROUND10_POSITIVE_CLOSURE.tex",
        "active_sha256": sha256(active),
        "main_tex": f"papers/{folder}/main.tex",
        "main_sha256": sha256(main),
        "byte_identity": source.read_bytes() == active.read_bytes(),
    }


records = [materialize(folder, meta) for folder, meta in PAPERS.items()]
cert = SRC / "A2_ROUND10_CERTIFICATE.json"
if cert.is_file():
    target = ROOT / "papers" / "A2-sinai-homological-pressure" / "A2_ROUND10_CERTIFICATE.json"
    target.write_bytes(cert.read_bytes())

manifest = {
    "schema": "theta-theory-round10-materialization-v1",
    "paper_count": len(records),
    "status": "PASS" if len(records) == 11 and all(r["byte_identity"] for r in records) else "FAIL",
    "papers": records,
}
(ROOT / "ROUND10_MATERIALIZATION_MANIFEST.json").write_text(
    json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
if manifest["status"] != "PASS":
    raise SystemExit("round-ten materialization failed")
print("ROUND10_MATERIALIZATION_PASS 11/11")
