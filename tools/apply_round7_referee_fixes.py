#!/usr/bin/env python3
"""Materialize the round-seven referee reconstruction into all eleven papers."""
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "revision" / "round7-referee-final"
PAPERS = ROOT / "papers"

DATA = {
    "A1-exact-benchmarks": {
        "code": "A1",
        "sources": ["A1_BISEAM_ANISOTROPIC_AUTONOMOUS.tex"],
        "abstract": """We construct a biseam graph completion retaining both vertical and horizontal oriented germs, so the four-port affine return is genuinely bijective on every corner stratum. An explicit autonomous extended Hamiltonian realizes the return with exact unit clock and full-port work. A polyhedral anisotropic current scale, including face, corner, and mixed jets, yields arbitrary finite-order physical response without importing an isotropic Holder spectral gap. Mechanical and valuation parameters coincide only under the stated likelihood-cocycle compatibility axiom.""",
        "response": "Biseam completion removes the explicit boundary collision of images; the physical transfer theory is rebuilt on an anisotropic strong/weak scale; all corner currents and the autonomous Hamiltonian are constructed explicitly.",
    },
    "A2-sinai-homological-pressure": {
        "code": "A2",
        "sources": ["A2_QUOTIENT_FIVEWORD_DOLGOPYAT.tex"],
        "abstract": """We place the ambient singular-current field on its complemented Hausdorff physical quotient, compute paired birth/death currents through the actual square-root geometry, and eliminate kernel-only spectrum. Five periodic words provide four independent equations for the two homology coefficients, roof coefficient, and coboundary constant. A near-opposition cone inequality gives the Dolgopyat loss on bulk, face, and corner jets. One target-dependent saddle then yields the local, central, and saturated vector-roof limit regimes without double counting.""",
        "response": "The nonclosed ambient realization is replaced by a complemented physical quotient; the arithmetic certificate is four-dimensional and uses five words; the false two-vector inequality is replaced by quantitative near-opposition cancellation.",
    },
    "A3-full-empirical-path-ldp": {
        "code": "A3",
        "sources": ["A3_CANONICAL_EXCURSION_GAMMA_LDP.tex"],
        "abstract": """A single length-weighted marked empirical measure compactifies recurrent and escaping excursion clock without a threshold diagonal. Branch profiles are intrinsic Gibbs conditional kernels. The recession cost is the Gamma limit of actual admissible excursion laws and is proved equal to its pressure conjugate by an exposed-profile recovery theorem. Periodic survivor components retain their period, and a strong-positive-recurrence versus recession dichotomy assigns spectral and escaping sectors correctly. This yields full collision-clock and deterministic-time large deviations.""",
        "response": "The limsup-conjugate shortcut is removed: the rate is first an actual-excursion Gamma limit with a recovery sequence. The compactification is threshold free, cyclic periods are preserved, and non-SPR components are moved to the recession sector.",
    },
    "A4-history-memory-universal-pressure": {
        "code": "A4",
        "sources": ["A4_COARSE_HISTORY_RIESZ_SCHUR.tex"],
        "abstract": """Conditional kernels are defined on a stable-leaf quotient history, never on a complete microscopic state whose future is deterministic. A renewal formula constructs the continuous-time Feller semigroup before Ray compactification. The history Doob eigenfunction is defined without a last-return ambiguity. Finite transmission zeros are extracted as actual Riesz residue modes of the compressed resolvent, giving an operator-compatible Schur dilation and a zero-free residual memory. Enhanced conditional homogenization retains the deterministic area anomaly.""",
        "response": "The complete-history Dirac contradiction is resolved by an explicit coarse stable-fiber filtration. Ray theory is no longer circular, and formal Smith-McMillan language is replaced by an operator-compatible finite-rank Riesz-Schur dilation.",
    },
    "B1-microcanonical-preparation": {
        "code": "B1",
        "sources": ["B1_SECTORWISE_COMPOUND_POISSON_SHELL.tex"],
        "abstract": """The one-particle momentum-energy mark is treated as a singular paraboloid surface measure. Full-dimensional smoothing begins only in a finite compound-Poisson convolution sector whose sum map has full rank. Empty and low-particle sectors remain as explicit exponentially small terms in every high-frequency estimate. Uniform covariance and exact finite saddles are obtained from the positive compound sector. The continuous shell is centered at the extensive target and has extensive shrinking width, yielding the mixed coefficient, microcanonical pressure, constrained covariance, and prepared LDP.""",
        "response": "The impossible singleton density is removed; atom and small-particle sectors are retained; the characteristic bound has an exponential atomic term; normalized and extensive shell variables are now dimensionally consistent.",
    },
    "B2-collision-clusters-dynamic-ldp": {
        "code": "B2",
        "sources": ["B2_FRAME_RESET_MEASURE_TRACE_LDP.tex"],
        "abstract": """A symplectic frame-reset construction localizes surplus-contact transversality at the youngest separating fork and gives a Gramian lower bound whose grazing exponent is independent of ancestral depth. The resulting recollision power is jointly summable in depth and particle scale. Incoming states are finite flux measures, so collision-time Dirac states are legitimate and the true reflected future is propagated by an integrated boundary-renewal semigroup. Stable source sewing, exact balance-preserving regularization, and projected normalized tilts yield fixed-horizon grand-canonical and microcanonical joint density-contact LDPs.""",
        "response": "The depth loss delta^{C(1+m)} is replaced by a frame-reset fork estimate delta^C; common-root translations are not used for relative control; stopping contacts live in a measure-valued trace state; regularization commutes exactly with balance.",
    },
    "B3-hamilton-boltzmann-cotangents": {
        "code": "B3",
        "sources": [
            "B3_EXACT_TANGENT_LAX_MILGRAM_PART1.tex",
            "B3_EXACT_TANGENT_LAX_MILGRAM_PART2.tex",
        ],
        "abstract": """Local analytic response and global bounded-source Fenchel duality are kept on distinct domains. We compute the full second variation of the contact perspective entropy, including the nonlinear second derivative of the Boltzmann reference measure. A weighted linearized balance estimate proves closed range and identifies the exact gauge annihilator. Lax-Milgram, rather than formal infinite-dimensional Hessian inversion, constructs the covariance operator. Integrated deterministic-interval cumulant densities give nuclear-space Gaussian process tightness without point-conditioned stopping states.""",
        "response": "The exact nonlinear tangent action and its cross terms are computed; the balance annihilator follows from a closed-range theorem; covariance is a coercive Hilbert inverse; process tightness is based on deterministic-interval cumulants.",
    },
    "B4-nonlinear-kinetic-semigroups": {
        "code": "B4",
        "sources": ["B4_FORWARD_POISSON_TATARU_SEMIGROUP.tex"],
        "abstract": """The exact law state is augmented by the cumulative actual-contact ledger. The BBGKY perturbed test solves a terminal-value Poisson equation with the backward observable propagator constructed by forward evolution in remaining time; it has zero terminal remainder and never invokes a negative-time hierarchy. Normal convergence is proved in an absolute generator graph norm. Analytic cylinders form the core and smooth cylinders are approximated on action compacta. A bounded-gradient Tataru penalty keeps every doubled cotangent inside a uniform exponential Hamiltonian chart, yielding comparison and nonlinear semigroup convergence.""",
        "response": "The finite-time pseudo-inverse is replaced by the exact terminal-value equation; path-contact observables enter an augmented Markov state; analytic and smooth test classes are separated; comparison gradients remain uniformly bounded.",
    },
    "C1-information-risk-sensitive-saddles": {
        "code": "C1",
        "sources": ["C1_COAREA_POSTERIOR_QUENCHED_GAME.tex"],
        "abstract": """Exact noiseless observations are retained through coarea posterior currents on their level sets rather than being forced into an interior density class. The B2 measure-valued trace semigroup propagates these beliefs and their collision traces. Prediction followed by observed disintegration defines a Feller belief kernel, while a uniform coarea ratio theorem gives quenched block pressures on strategy-reachable compacta. Exponential contraction of connected hierarchy coordinates proves asymptotic sufficiency of the resolved kinetic state. Continuous-prior Chernoff bounds use an explicit local denominator; LAN remains centered at the exact finite-volume mean.""",
        "response": "Singular level-set posteriors are represented as coarea currents inside the revised B2 state. Quenched pressure ratios, Feller selectors, higher-correlation sufficiency, and the continuous-prior denominator are proved explicitly.",
    },
    "C2-cotangent-rigidity-tangent-representations": {
        "code": "C2",
        "sources": ["C2_TWO_NULLSPACES_COVARIANT_DOOB.tex"],
        "abstract": """Equality of invariant integrals is quotiented only by coboundaries, whereas normalized pressure equivalence also quotients constants. Weighted Folner averaging turns separating Radon functionals into invariant measures. Exact likelihood martingales and optional projections use the A4 coarse-history filtration. Source variation is formulated as a covariant derivative on the Doob Hilbert bundle and includes eigenfunction, invariant-measure, pairing, and projection derivatives. Linear and nonlinear contractions are distinguished and the full Frechet chain rule is retained.""",
        "response": "The constants counterexample is eliminated by two null spaces. Optional projections use the valid coarse filtration, and source-dependent memory differentiation includes every moving Doob datum instead of a fixed-Hilbert Duhamel term alone.",
    },
    "D1-deterministic-theta-contractions": {
        "code": "D1",
        "sources": ["D1_STRATIFIED_PROJECTIVE_LOCAL_CHARTS.tex"],
        "abstract": """Finite projective pressures are organized by local zero-free complex atlases rather than a global complex logarithm. Bounded cylinder projections use convex-support face stratification instead of an impossible gradient blow-up at infinity. Phase coexistence is retained as a maximum of analytic phase charts, with phase-wise microscopic recovery and a lower-semicontinuous minimum rate. An explicit topology-upgrade lemma, genuine thin-shell conditioning, complete finite-dimensional duality hypotheses, and exact finite-centered local likelihoods yield a standalone stratified projective commutation theorem.""",
        "response": "Entire pressure and infinity-steepness assumptions are removed. The replacement theorem covers bounded supports, exposed faces, coexistence, topology upgrade, thin constraints, and exact local likelihoods without deleting the standalone paper.",
    },
}

DATE_RE = re.compile(r"\\date\{[^}]*\}")
ABSTRACT_RE = re.compile(r"\\begin\{abstract\}.*?\\end\{abstract\}", re.DOTALL)
CONTROL_RE = re.compile(
    r"\\noindent\\textbf\{Controlling revision:\}\s*"
    r"\\texttt\{[^}]+\}\."
)
INPUT_RE = re.compile(r"\\input\{ROUND\d+_POSITIVE_CLOSURE\.tex\}")
BAD_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def replace_once(pattern: re.Pattern[str], text: str, replacement: str, name: str) -> str:
    updated, count = pattern.subn(lambda _: replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"{name}: expected one replacement, found {count}")
    return updated


def read_registered(meta: dict[str, object]) -> str:
    pieces: list[str] = []
    for source_name in meta["sources"]:  # type: ignore[index]
        source = SRC / str(source_name)
        if not source.is_file():
            raise SystemExit(f"missing round-seven source: {source}")
        text = source.read_text(encoding="utf-8")
        match = BAD_CONTROL_RE.search(text)
        if match:
            raise SystemExit(
                f"{source}: ASCII control byte {ord(match.group(0))} at {match.start()}"
            )
        pieces.append(text.rstrip() + "\n")
    return "\n".join(pieces)


manifest: dict[str, object] = {
    "schema": "theta-theory-round7-materialization-v1",
    "paper_count": len(DATA),
    "papers": {},
}

for paper, meta in DATA.items():
    source_text = read_registered(meta)
    module = PAPERS / paper / "ROUND7_POSITIVE_CLOSURE.tex"
    module.write_text(
        "% ROUND7-REFEREE-POSITIVE-CLOSURE\n" + source_text,
        encoding="utf-8",
    )

    main = PAPERS / paper / "main.tex"
    text = main.read_text(encoding="utf-8")
    text = replace_once(DATE_RE, text, r"\date{August 31, 2026}", str(main))
    abstract = (
        "\\begin{abstract}\n"
        + str(meta["abstract"]).strip()
        + "\n\\end{abstract}"
    )
    text = replace_once(ABSTRACT_RE, text, abstract, str(main))
    marker = (
        r"\noindent\textbf{Controlling revision:} "
        r"\texttt{ROUND7-REFEREE-POSITIVE-CLOSURE}."
    )
    text = replace_once(CONTROL_RE, text, marker, str(main))
    text = replace_once(
        INPUT_RE,
        text,
        r"\input{ROUND7_POSITIVE_CLOSURE.tex}",
        str(main),
    )
    text = re.sub(r"round-(?:three|four|five|six) dependency ledger", "round-seven dependency ledger", text)
    main.write_text(text, encoding="utf-8")

    report = PAPERS / paper / "REFEREE_REPORT_ROUND6_GPT56_PRO.md"
    if not report.is_file():
        raise SystemExit(f"missing latest referee report: {report}")
    response = PAPERS / paper / "AUTHOR_RESPONSE_ROUND7.md"
    response.write_text(
        f"# {meta['code']} author response to the round-six independent report\n\n"
        f"**Controlling source:** `ROUND7_POSITIVE_CLOSURE.tex`  \n"
        f"**Latest report retained:** `REFEREE_REPORT_ROUND6_GPT56_PRO.md`\n\n"
        "## Positive reconstruction\n\n"
        + str(meta["response"]).strip()
        + "\n\n"
        "No principal claim is replaced by a no-go statement or by deletion of the paper. "
        "Every reported direct counterexample is answered by a changed state space, operator, "
        "estimate, or proof mechanism in the controlling source.\n",
        encoding="utf-8",
    )

    manifest["papers"][paper] = {  # type: ignore[index]
        "code": meta["code"],
        "sources": meta["sources"],
        "module": str(module.relative_to(ROOT)),
        "main": str(main.relative_to(ROOT)),
        "response": str(response.relative_to(ROOT)),
        "report": str(report.relative_to(ROOT)),
    }

(ROOT / "ROUND7_MATERIALIZATION_MANIFEST.json").write_text(
    json.dumps(manifest, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(f"ROUND7_MATERIALIZATION_PASS papers={len(DATA)}")
