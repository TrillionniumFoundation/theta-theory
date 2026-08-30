#!/usr/bin/env python3
"""Apply the second-pass mathematical corrections before main publication.

This patch is deliberately separate from the first materializer so an exact
audit trail shows which statements were strengthened after hostile rereview.
It is idempotent and fails if an expected first-pass passage is missing.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str, *, already: str | None = None) -> None:
    text = path.read_text(encoding="utf-8")
    if already and already in text:
        return
    if old not in text:
        raise SystemExit(f"hostile patch anchor missing in {path}: {old[:90]!r}")
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")


# A2: the corridor argument must cover every primitive lattice direction,
# not only the three shortest visual directions.
a2 = ROOT / "papers/A2-sinai-homological-pressure/ROUND3_POSITIVE_CLOSURE.tex"
replace_once(
    a2,
    """A free line
of unbounded length would have a limiting direction.  Reducing this direction
modulo the triangular lattice gives one of the three primitive corridor
strips.  Their transverse width is \\(\\sqrt3/2\\), whereas the two disks which
bound a strip occupy transverse width at least \\(2R\\ge 9/10\\).  The positive
margin \\(h_*\\) therefore bounds the number of crossed cells, and compactness
of direction and base point gives \\(\\tau_+\\).""",
    """If an unbounded free line existed, periodicity and compactness would
produce a strip parallel to a primitive lattice vector \\(v\\in\\Lambda\\).
The distance between adjacent lattice rows parallel to \\(v\\) is
\\[
 \\frac{\\operatorname{area}(\\mathbb R^2/\\Lambda)}{|v|}
 =\\frac{\\sqrt3}{2|v|}
 \\le\\frac{\\sqrt3}{2}.
\\]
A corridor therefore requires \\(2R\\le\\sqrt3/(2|v|)\\).  But
\\(2R\\ge9/10>\\sqrt3/2\\), so no primitive direction admits a corridor.
The strict margin \\(h_*\\) is smallest for the shortest lattice vectors and
is larger for all longer vectors.  Compactness of initial point and direction
then gives one uniform upper flight bound \\(\\tau_+\\).""",
    already="distance between adjacent lattice rows parallel",
)

# B2: make the regular lower-bound source realization explicit.  This closes
# the gap between a feasible smooth pair and an actual canonical source.
b2 = ROOT / "papers/B2-collision-clusters-dynamic-ldp/ROUND3_POSITIVE_CLOSURE.tex"
text = b2.read_text(encoding="utf-8")
if "Regular tilted-source realization" not in text:
    anchor = "\\begin{theorem}[Grand-canonical density--actual-collision LDP]"
    if anchor not in text:
        raise SystemExit("B2 hostile insertion anchor missing")
    lemma = r"""
\begin{lemma}[Regular tilted-source realization]
\label{lem:r3-b2-source-realization}
Let \((f,\Gamma)\) be a smooth strictly positive feasible pair on
\([0,T]\), with \(q=d\Gamma/dA_f\) bounded above and below and with compact
velocity support before the final weighted approximation.  Then there are
smooth bounded density and collision sources \((h,\psi)\) in the marked
source chart and a smooth cotangent \(p\) such that
\[
 \psi=\log q-\Delta_\omega p
\]
and \((f,\Gamma)\) is the unique first derivative of the limiting marked
pressure at \((h,\psi)\).  One may take
\[
 h=-\partial_t p-v\cdot\nabla_xp
   -\frac{\delta}{\delta f}
   \int\left(e^{\Delta_\omega p+\psi}-1\right)dA_f,
\]
with endpoint values of \(p\) chosen to match the prescribed initial and
terminal density sources.
\end{lemma}

\begin{proof}
The Hamilton equations associated with the marked Hamiltonian are the weak
balance equation for the first variable and the backward adjoint equation for
the cotangent.  The relation
\(e^{\Delta p+\psi}=q\) makes the forward collision intensity exactly
\(qA_f=\Gamma\).  Defining \(h\) by the displayed residual makes the given
smooth density path solve the backward/forward canonical system.  On the
short-time analytic chart, the linearization is the identity plus an integral
operator whose norm is \(O(T)\); for the B2 time window it is invertible by a
Neumann series.  Strict convexity in the collision source and the positive
quotient covariance of the density source make the pressure gradient locally
one-to-one.  Hence the canonical source has \((f,\Gamma)\) as its unique mean.
The compact support assumption makes every source bounded; weighted velocity
truncation is performed only after this realization step.
\end{proof}

"""
    text = text.replace(anchor, lemma + anchor, 1)
    b2.write_text(text, encoding="utf-8")

replace_once(
    b2,
    """For the lower bound, first take a smooth feasible pair with
\\(q=d\\Gamma/dA_f\\) bounded above and below.  Choose a smooth \\(p\\) solving the
backward linearized balance and put
\\(\\psi=\\log q-\\Delta p\\).  Tilt the microscopic initial activity and every
actual contact by these sources.  Theorem~\\ref{thm:r3-b2-gc-cluster} remains
normal on a slightly larger complex ball.  Its first derivative gives the
biased Boltzmann law \\((f,\\Gamma)\\), and its second derivative plus compact
containment gives exponential concentration under the tilted law.""",
    """For the lower bound, first take a smooth feasible pair with
\\(q=d\\Gamma/dA_f\\) bounded above and below.  Use
Lemma~\\ref{lem:r3-b2-source-realization} to obtain an actual bounded
particle-path source \\(h\\), collision source \\(\\psi\\), and cotangent \\(p\\)
whose canonical mean is exactly \\((f,\\Gamma)\\).  Tilt the microscopic
initial activity, path weight, and every actual contact by these sources.
Theorem~\\ref{thm:r3-b2-gc-cluster} remains normal on a slightly larger
complex ball.  Its first derivative is the prescribed biased law and its
positive Hessian, together with compact containment, gives exponential
concentration under the tilted measure.""",
    already="Use\nLemma~\\ref{lem:r3-b2-source-realization}",
)

# C1: adaptive control is a sequence of normalized conditional canonical
# tilts on the coarse filtration.  A deterministic contact process does not
# possess the stochastic compensator that the first draft had written down.
c1 = ROOT / "papers/C1-information-risk-sensitive-saddles/ROUND3_POSITIVE_CLOSURE.tex"
replace_once(
    c1,
    """At finite \\(\\varepsilon\\), a predictable
piecewise-constant strategy changes path probabilities by the actual-contact
likelihood
\\[
 \\exp\\left\\{\\
 \\sum_{c}\\log q^{u_c,v_c}(c)
 -\\mu_\\varepsilon\\int(q^{u,v}-1)dA_{\\pi^\\varepsilon}
 \\right\\},
\\]
constructed by the B2 marked source.  The elastic hard-sphere trajectory is
unchanged; only its canonical path weight is controlled.""",
    """Fix a coarse observation filtration \\((\\mathcal Y_t^\\varepsilon)\\)
and a time partition \\(t_j\\).  On block \\([t_j,t_{j+1}]\\), a predictable
piecewise-constant strategy uses the exact normalized canonical factor
\\[
 L_{j+1}^\\varepsilon
 =\\frac{\\exp\\{\\mu_\\varepsilon
   \\langle\\log q^{u_j,v_j},
   \\Gamma_{[t_j,t_{j+1}]}^\\varepsilon\\rangle\\}}
 {\\mathbb E[\\exp\\{\\mu_\\varepsilon
   \\langle\\log q^{u_j,v_j},
   \\Gamma_{[t_j,t_{j+1}]}^\\varepsilon\\rangle\\}
   \\mid\\mathcal Y_{t_j}^\\varepsilon]}.
\\]
The product of these conditional factors is a mean-one likelihood ratio.
Its block normalizer is the B2 marked pressure; subtracting that normalizer
changes the excess collision Hamiltonian to
\\(q^{u,v}(e^{\\Delta p}-1)\\).  No stochastic point-process compensator is
postulated for the deterministic contacts.  The elastic hard-sphere
trajectory is unchanged; only the prepared path law on the coarse filtration
is canonically reweighted.""",
    already="exact normalized canonical factor",
)

replace_once(
    c1,
    """For a fixed control pair, B2 with collision source
\\(\\psi=\\log q^{u,v}\\) gives the controlled cumulant and the action
\\[
 \\int\\ell\\left(\\frac{d\\Gamma}{q^{u,v}dA_f}\\right)
 q^{u,v}dA_f.
\\]""",
    """For a fixed control pair, B2 with collision source
\\(\\psi=\\log q^{u,v}\\), followed by subtraction of the zero-cotangent block
normalizer, gives the excess Hamiltonian
\\(\\int q^{u,v}(e^{\\Delta p}-1)dA_f\\) and the controlled action
\\[
 \\int\\ell\\left(\\frac{d\\Gamma}{q^{u,v}dA_f}\\right)
 q^{u,v}dA_f.
\\]""",
    already="followed by subtraction of the zero-cotangent block",
)

# Synchronize the controlling titles with the revised theorems.  The first
# materializer intentionally retained house-style metadata; hostile review
# removes stale 'universal' or old-body claims from the actual titles.
titles = {
    "A1-exact-benchmarks": ("Hamiltonian Impact Path Ensembles", "Hamiltonian Impact Path Ensembles, Driven Maps, and Canonical Cocycles"),
    "A2-sinai-homological-pressure": ("Uniform Vector--Roof Spectra", "Uniform Vector--Roof Spectra and Homological Conditioning for Sinai Billiards"),
    "A3-full-empirical-path-ldp": ("Two-Clock Sinai Path Large Deviations", "Two-Clock Empirical-Path Large Deviations for Finite-Horizon Sinai Billiards"),
    "A4-history-memory-universal-pressure": ("Compressed-Resolvent Memory", "Compressed-Resolvent Memory and Nonlinear History Pressure for Sinai Billiards"),
    "B1-microcanonical-preparation": ("Source-Dependent Microcanonical Preparation", "Source-Dependent Microcanonical Preparation for Deterministic Hard Spheres"),
    "B2-collision-clusters-dynamic-ldp": ("Actual-Collision Clusters", "Actual-Collision Trajectory Clusters and Joint Dynamic Large Deviations"),
    "B3-hamilton-boltzmann-cotangents": ("Balance-Gauge Cotangents", "Balance-Gauge Cotangents and Prepared Fluctuations for the Boltzmann Action"),
    "B4-nonlinear-kinetic-semigroups": ("Correlation-State Kinetic Semigroups", "Correlation-State Kinetic Semigroups and Microcanonical Pressure"),
    "C1-information-risk-sensitive-saddles": ("Three Typed Kinetic Games", "Three Typed Kinetic Games, Saddle Envelopes, and Phase Information"),
    "C2-cotangent-rigidity-tangent-representations": ("Platform-Labelled Path Cotangents", "Platform-Labelled Path Cotangents and Tangent Representations"),
    "D1-deterministic-theta-contractions": ("Analytic--Convex Commutation", "Analytic--Convex Commutation for Deterministic Kinetic Path Pressures"),
}
for folder, (short, long) in titles.items():
    main = ROOT / "papers" / folder / "main.tex"
    text = main.read_text(encoding="utf-8")
    replacement = rf"\\title[{short}]{{{long}}}"
    new_text, n = re.subn(r"\\title(?:\[[^\]]*\])?\{[^{}]*\}", replacement, text, count=1)
    if n != 1:
        raise SystemExit(f"could not synchronize title in {main}")
    main.write_text(new_text, encoding="utf-8")

print("ROUND3_HOSTILE_FIXES_APPLIED")
