#!/usr/bin/env python3
"""Materialize the round-three controlling manuscripts.

The historical bodies on main contain theorem statements superseded by the
round-three referee reconstruction.  This script preserves each paper's
preamble, title, author data, bibliography, and house style, but regenerates
the document body from the audited ROUND3_POSITIVE_CLOSURE.tex module.  It is
idempotent and fails closed if any expected source is absent.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

PAPERS = {
    "A1-exact-benchmarks": {
        "platform": "A1-HAM-IMPACT-v2",
        "abstract": r"""We construct an exact autonomous Hamiltonian impact network whose
Liouville return map is the four-branch driven family.  All parameter values
are typed on one common symbolic path space; canonical tilting, uniformly
rooted microcanonical conditioning, physical port work, and moving-seam
response are proved on that same system.  The preparation field is identified
with the nonlinear-expectation coefficient only under an explicit
canonical-cocycle compatibility axiom, so mechanical preparation is not
confused with an unrelated preference parameter.""",
    },
    "A2-sinai-homological-pressure": {
        "platform": "TL2-HOM-v2",
        "abstract": r"""For the compact triangular-lattice finite-horizon Sinai family we
construct a radius-uniform moving-cut anisotropic Banach bundle, prove the
complex vector-displacement/roof spectral packet, and establish temporal
uniform non-integrability through an explicit pair of inverse branches in a
triangular gap.  A three-frequency Fourier argument yields a uniform
lattice--nonlattice local limit theorem down to submacroscopic physical-clock
windows.  The physical pressure root, its transport Hessian, and two-sided
current--clock Gibbs conditioning follow without an unverified arithmetic
packet.""",
    },
    "A3-full-empirical-path-ldp": {
        "platform": "TL3-LPATH-v2",
        "abstract": r"""We prove full weak empirical-path large-deviation principles in
collision and physical time for a finite-horizon Sinai billiard.  A
finite-connector Young code is treated first at bounded return length and then
completed by exponentially good mark truncations.  A quantitative
singularity-frequency ledger and terminal clock-surgery lemma give both upper
and lower bounds after the collision and physical random clocks.  The rates
are presentation independent, finite only on graph-completed deterministic
paths, support compact information projections, and possess a closed weighted
coboundary cotangent quotient.""",
    },
    "A4-history-memory-universal-pressure": {
        "platform": "TL3-HIST-v2",
        "abstract": r"""Prepared Sinai paths are represented by a strongly continuous
weighted history Feller semigroup.  Exact memory is defined from the
compressed Koopman resolvent rather than from an assumed semigroup generated
by the orthogonal compression.  The resulting causal Volterra identity is
domain safe; resonant poles are promoted into the resolved state to produce an
exponentially integrable residual memory kernel.  We construct the nonlinear
history pressure generator and prove its rough short-memory diffusion tangent
from the vector--roof spectral packet.""",
    },
    "B1-microcanonical-preparation": {
        "platform": "HSBG-LIO-v2",
        "abstract": r"""We prove source-dependent microcanonical preparation for a dilute
deterministic hard-sphere gas.  Particle-path and actual-collision sources are
included before conditioning, and the finite-dimensional constraint
multiplier is reoptimized at every source.  A joint lattice--continuous local
coefficient theorem shows that the exact particle-number and shrinking
continuous shell has only subexponential cost under the reoptimized law.  The
limiting constrained pressure, initial rate, and fluctuation covariance have
the required saddle and Schur-complement formulas, including the decisive
time-zero source test.""",
    },
    "B2-collision-clusters-dynamic-ldp": {
        "platform": "HSBG-LIO-v2",
        "abstract": r"""Every actual incoming hard-sphere contact is marked in a
source-uniform real-trajectory cluster expansion.  Recollisions are controlled
by deleting the first cycle edge and extracting an independent geometric tube
constraint; they are never counted as fictitious new labels.  Normal
convergence gives the marked Hamilton--Jacobi equation, joint density--contact
covariances, exponential compact containment, and a full short-time upper and
lower large-deviation principle.  Source-dependent conditioning transfers the
result to the primitive microcanonical shell.""",
    },
    "B3-hamilton-boltzmann-cotangents": {
        "platform": "HSBG-LIO-v2",
        "abstract": r"""We place the density--collision action in weighted measure and
exponential-Orlicz dual spaces and prove the complete path-space Fenchel
duality.  The cotangent pair is quotiented by the exact balance gauge
$(p,\psi)\mapsto(p+r,\psi-\Delta r)$, so the identifiable field is
$\Delta p+\psi$ rather than two separately unique multipliers.  Regular macro
constraints have analytic information-projection multipliers, and the
microscopic density and actual-collision fields converge jointly to the
prepared fluctuating Boltzmann Gaussian law with the microcanonical initial
Schur complement.""",
    },
    "B4-nonlinear-kinetic-semigroups": {
        "platform": "HSBG-LIO-v2",
        "abstract": r"""The exact finite hard-sphere state is retained as its BBGKY
correlation hierarchy.  Density cylinders are lifted by recursive correlation
correctors whose nonlinear generators converge to the exponential
Hamilton--Boltzmann Hamiltonian.  Independently, the joint dynamic action
constructs a weighted density Lax--Oleinik semigroup; exponential containment
and a doubled-variable comparison theorem identify the microscopic limit.
Microcanonical preparation is a terminal contraction of a lifted semigroup
with a static source-dependent multiplier, and the risk-sensitive diffusion
generator is obtained as the proved Gaussian tangent.""",
    },
    "C1-information-risk-sensitive-saddles": {
        "platform": "HSBG-CONTROL-v2",
        "abstract": r"""We separate three kinetic games which obey different timing
rules: one-time preparation, reward-only feedback on a fixed phase, and
adaptive canonical control of actual-contact likelihoods.  Only the third has
a pointwise Isaacs Hamiltonian, and its microscopic strategy class is
constructed from the marked contact source.  Smooth preparation manifolds
have a verified optimizer-response Schur complement, whereas finite action
sets use active-branch directional envelopes.  Coarse phase observations
satisfy an exponential posterior-selection theorem; complete microscopic
observation reduces to deterministic continuation.""",
    },
    "C2-cotangent-rigidity-tangent-representations": {
        "platform": "TYPED-COPRODUCT-v2",
        "abstract": r"""We formulate the series on a platform-labelled coproduct, so every
contraction retains its own microscopic law and cross-platform conclusions
require a separately proved scaling map.  A weighted strict topology has the
countably additive Radon path measures as its continuous dual, and the closed
coboundary quotient supplies Hausdorff cotangents.  Spectral and cluster
packets yield first and second pressure responses.  We then prove the
canonical-cocycle calibration criterion, deterministic-to-diffusion
likelihood/Girsanov/BSDE convergence, and an exact commutative identity between
linearized history pressure and compressed-resolvent memory.""",
    },
    "D1-deterministic-theta-contractions": {
        "platform": "HSBG-COMMUTE-v2",
        "abstract": r"""We prove an analytic--convex commutation theorem for deterministic
kinetic path pressures.  Locally uniform complex convergence is shown to
commute with all pressure derivatives, source-dependent microcanonical
conditioning, convex duality, typed observable contraction, and Gaussian
likelihood-ratio limits.  The pressure Hessian is the large-deviation-speed
normalized covariance and conditioning produces its exact Schur complement.
Applied to the hard-sphere series, the theorem yields one rigorous
rate--pressure--semigroup triangle and the correctly normalized
Cameron--Martin, Girsanov, BSDE, and calibrated scalar-ray tangents.""",
    },
}

SCOPE = r"""\section*{Scope and verification status}
This manuscript states positive theorem closure in the declared local source,
short-time, finite-horizon or Boltzmann--Grad regime specified in its theorems.
Every load-bearing cross-paper input is typed in the round-three dependency
ledger.  Clean compilation and automated structural checks are necessary
verification gates; independent external journal review remains a separate
process.
"""


def materialize(name: str, meta: dict[str, str]) -> None:
    paper = ROOT / "papers" / name
    main = paper / "main.tex"
    module = paper / "ROUND3_POSITIVE_CLOSURE.tex"
    if not main.is_file() or not module.is_file():
        raise SystemExit(f"missing controlling source for {name}")

    old = main.read_text(encoding="utf-8")
    marker = r"\begin{document}"
    if marker not in old:
        raise SystemExit(f"no document boundary in {main}")
    preamble = old.split(marker, 1)[0].rstrip()

    # One cross-paper label survived in the authored B4 prose.  Cross-paper
    # dependencies are textual/theorem-ID imports, not LaTeX references.
    module_text = module.read_text(encoding="utf-8")
    module_text = module_text.replace(
        r"Proposition~\ref{prop:r3-b3-normalization} of B3",
        "the round-three finite-volume normalization theorem of Paper B3",
    )
    module.write_text(module_text, encoding="utf-8")

    body = (
        preamble
        + "\n"
        + marker
        + "\n\\raggedbottom\n"
        + "\\begin{abstract}\n"
        + meta["abstract"].strip()
        + "\n\\end{abstract}\n"
        + "\\maketitle\n"
        + "\\noindent\\textbf{Platform identifier:} "
        + "\\texttt{" + meta["platform"] + "}.\n"
        + "\\noindent\\textbf{Controlling revision:} "
        + "\\texttt{ROUND3-POSITIVE-CLOSURE}.\n"
        + "\\tableofcontents\n\n"
        + r"\input{ROUND3_POSITIVE_CLOSURE.tex}"
        + "\n\n"
        + SCOPE
        + "\\printbibliography\n"
        + "\\end{document}\n"
    )
    main.write_text(body, encoding="utf-8")


for paper_name, metadata in PAPERS.items():
    materialize(paper_name, metadata)

manifest = ROOT / "ROUND3_REVISION_MANIFEST.yaml"
manifest.write_text(
    """schema: theta-theory-round3-v1
base_commit: 970d88ae41faf601ae609d833b48288f213e5c5c
branch: revision/round3-full-positive-closure-11paper-2026-08-30
status: materialized_pending_build
policy:
  positive_reconstruction: true
  no_downgrade: true
  no_nogo_substitution: true
  fail_closed_merge: true
dependency_order:
  sinai: [A2, A3, A4, C2, D1]
  hard_sphere: [B2-GC, B1, B2-MC, B3, B4, C1, C2, D1]
  benchmark: [A1]
papers:
"""
    + "".join(
        f"  - folder: papers/{name}\n"
        f"    controlling_module: ROUND3_POSITIVE_CLOSURE.tex\n"
        f"    platform: {meta['platform']}\n"
        for name, meta in PAPERS.items()
    ),
    encoding="utf-8",
)

print(f"ROUND3_MATERIALIZED {len(PAPERS)}/11")
