#!/usr/bin/env python3
"""Apply the first exact-commit harsh rereview fixes to round-three sources.

This pass does two different jobs and keeps them explicit:

1. restore LaTeX command initials accidentally encoded as ASCII control bytes
   in a few early connector writes, and repair the corresponding normalized
   line breaks already materialized by Python; and
2. replace four proof passages which a hostile rereview found too strong or
   logically incomplete: A3's bounded-return finite-alphabet claim, A4's
   Feller assertion for arbitrary prepared laws, B2's iteration language for
   cycle gains, and D1's insufficient infinite-dimensional holomorphic
   convergence hypothesis.  B4 is also made to use the proved B2 LDP as its
   primary semigroup-convergence route.

The script is idempotent and fail-closed.  A replacement either finds exactly
one old region or verifies the already-installed new marker.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"


def write_if_changed(path: Path, text: str) -> int:
    old = path.read_text(encoding="utf-8")
    if old == text:
        return 0
    path.write_text(text, encoding="utf-8")
    return 1


def restore_control_bytes(path: Path) -> int:
    raw = path.read_bytes()
    # These are precisely the first letters consumed by JSON/Python escape
    # sequences in the original connector write: \b, \t, \v, \f, and \r.
    control_initial = {
        0x08: b"b",
        0x09: b"t",
        0x0B: b"v",
        0x0C: b"f",
        0x0D: b"r",
    }
    out = bytearray()
    changed = 0
    for byte in raw:
        if byte in control_initial:
            out.extend(b"\\" + control_initial[byte])
            changed += 1
        else:
            out.append(byte)
    if changed:
        path.write_bytes(bytes(out))
    return changed


def normalized_command_repairs(text: str) -> tuple[str, int]:
    changed = 0

    def sub(pattern: str, replacement: str, value: str) -> str:
        nonlocal changed
        value, count = re.subn(pattern, replacement, value)
        changed += count
        return value

    # A command whose first letter had already become a physical newline in a
    # previous materialization.  The suffixes are sufficiently specific to be
    # unambiguous in the mathematical source.
    text = sub(r"(?m)^rac(?=(?:\{|[0-9]))", r"\\frac", text)
    text = sub(r"(?m)^arepsilon(?=(?:\^|\(|\{|[0-9]))", r"\\varepsilon", text)
    text = sub(r"(?m)^ho(?=\^)", r"\\rho", text)
    text = sub(r"(?m)^ight(?=\))", r"\\right", text)
    text = text.replace("_{\nm conn}", "_{\\rm conn}")
    text = text.replace("\\Gamma^\narepsilon", "\\Gamma^\\varepsilon")
    text = text.replace("\\night)", "\\right)")
    text = text.replace("\\widehat\\mathbb P", "\\widehat{\\mathbb P}")

    # Count the literal replacements conservatively after the regex pass.
    # Idempotence is checked below by forbidden-pattern assertions.
    return text, changed


def sanitize_all_modules() -> int:
    changes = 0
    forbidden_controls = set(range(0x00, 0x20)) - {0x0A}
    for path in sorted(PAPERS.glob("*/ROUND3_POSITIVE_CLOSURE.tex")):
        changes += restore_control_bytes(path)
        text = path.read_text(encoding="utf-8")
        repaired, count = normalized_command_repairs(text)
        changes += count
        path.write_text(repaired, encoding="utf-8")
        raw = path.read_bytes()
        bad = sorted(set(raw) & forbidden_controls)
        if bad:
            raise SystemExit(f"{path}: remaining ASCII control bytes {bad}")
        for forbidden in (
            "\\night)",
            "_{\nm conn}",
            "\\Gamma^\narepsilon",
            "\\widehat\\mathbb P",
        ):
            if forbidden in repaired:
                raise SystemExit(f"{path}: unresolved TeX corruption {forbidden!r}")
        suspicious = re.findall(r"(?m)^(?:rac|arepsilon|ho\^|ight\))", repaired)
        if suspicious:
            raise SystemExit(f"{path}: suspicious command suffixes {suspicious}")
    return changes


def replace_region(
    path: Path,
    start: str,
    end: str,
    replacement: str,
    installed_marker: str,
) -> int:
    text = path.read_text(encoding="utf-8")
    if installed_marker in text:
        return 0
    start_index = text.find(start)
    if start_index < 0:
        raise SystemExit(f"{path}: start marker not found: {start[:80]!r}")
    end_index = text.find(end, start_index)
    if end_index < 0:
        raise SystemExit(f"{path}: end marker not found: {end[:80]!r}")
    text = text[:start_index] + replacement.rstrip() + "\n\n" + text[end_index:]
    path.write_text(text, encoding="utf-8")
    return 1


def replace_once(path: Path, old: str, new: str, installed_marker: str) -> int:
    text = path.read_text(encoding="utf-8")
    if installed_marker in text:
        return 0
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one replacement, found {count}: {old[:100]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return 1


def fix_a3() -> int:
    path = PAPERS / "A3-full-empirical-path-ldp" / "ROUND3_POSITIVE_CLOSURE.tex"
    start = r"For \(L\ge1\), let \(\mathcal A_L=\{a:r(a)\le L\}\)."
    end = r"\subsection{A quantitative singularity shield}"
    replacement = r"""For a return branch \(a\), let \(h(a)\) be the largest
homogeneity-strip index met by its recorded excursion.  For \(L,K\ge1\), put
\[
 \mathcal A_{L,K}=\{a:r(a)\le L,\ h(a)\le K\}.
\]
The finite-time singularity arrangement has only finitely many components
after both cutoffs, so \(\mathcal A_{L,K}\) is finite.  The high-homogeneity
set has Gibbs mass \(O(K^{-\zeta})\) for some \(\zeta>0\), uniformly on every
fixed return cutoff.

\begin{theorem}[Block empirical-measure LDP without an unverified coding
packet]
\label{thm:r3-a3-block}
The empirical block measures
\[
 \widehat L_N=\frac1N\sum_{j=0}^{N-1}
 \delta_{\widehat\Theta^j\widehat\omega}
\]
satisfy a full weak LDP with a good rate \(\widehat{\mathcal I}\).  On
invariant probabilities of finite mark moment,
\[
 \widehat{\mathcal I}(\widehat\nu)
 =\sup_{F\in C_b^{\rm cyl}}
 \left\{\widehat\nu(F)-
 \big(P(\widehat\phi+F)-P(\widehat\phi)\big)\right\},
\]
and it is infinite off invariant probabilities or when the required mark
moment is infinite.
\end{theorem}

\begin{proof}
Give the countable code the weighted variation norm
\[
 \|g\|_{\eta}=\sup e^{-\eta(r+\mathfrak t)}|g|
 +\sum_{n\ge1}\rho^{-n}\operatorname{var}_n(g),
\]
with \(0<\eta\) below the exponential-mark exponent.  Finite primitivity,
summable distortion, and the connector words give the Doeblin--Fortet
estimate
\[
 \|\widehat{\mathcal L}^{\,n}g\|_\eta
 \le C\rho_0^n\|g\|_\eta+C\|g\|_{w,\eta},
 \qquad \rho_0<1.
\]
The exponential mark tail makes the strong unit ball compact in the weighted
weak norm.  Thus every bounded cylinder twist has a simple pressure
eigenvalue on a common neighborhood, and every finite tuple of cylinder
coordinates has the finite-dimensional upper bound and exposed-point lower
bound obtained by exponential tilting.

The two missing global ingredients are exponential tightness and density of
exposed finite-state phases.  For long marks, normal convergence of the
operator twisted by \(s r1_{\{r>L\}}\) gives, for every fixed \(s<\eta\),
\[
 \lim_{L\to\infty}\big(P(\widehat\phi+s r1_{\{r>L\}})
 -P(\widehat\phi)\big)=0.
\]
Chernoff's inequality makes the empirical long-mark mass exponentially
negligible with a cost tending to infinity.  For grazing branches, the weak
operator norm of multiplication by \(1_{\{h>K\}}\) tends to zero by the
homogeneity-strip mass estimate.  Hence, for every fixed \(s>0\),
\[
 P(\widehat\phi+s1_{\{h>K\}})-P(\widehat\phi)\longrightarrow0.
\]
First let \(K\to\infty\) and then \(s\to\infty\); this gives an arbitrarily
large cost for a fixed positive empirical grazing frequency.  These two
bounds give exponential tightness in the cylinder topology augmented by the
mark moment.

Finally let \(\widehat\nu\) be invariant with finite rate.  Restrict it to
\(\mathcal A_{L,K}\), and replace each discarded excursion by the fixed
connector word having the same entrance and exit components.  The discarded
frequency and mark mass tend to zero.  Summable variations make the potential
and entropy/free-energy costs of the connector insertions tend to zero as
well.  The resulting invariant finite-state phases
\(\widehat\nu_{L,K}\) converge to \(\widehat\nu\) on every cylinder and
satisfy
\[
 \widehat{\mathcal I}_{L,K}(\widehat\nu_{L,K})
 \longrightarrow\widehat{\mathcal I}(\widehat\nu).
\]
The finite-state LDP lower bound followed by this diagonal approximation gives
the lower bound at every finite-rate law.  The projective upper bound and
exponential tightness give the full upper bound.  Compactness of rate
sublevels and the displayed pressure duality follow from the same two tail
estimates.
\end{proof}"""
    changes = replace_region(
        path,
        start,
        end,
        replacement,
        "Block empirical-measure LDP without an unverified coding packet",
    )

    text = path.read_text(encoding="utf-8")
    if "homogeneity cutoff" not in text:
        old = r"""Fix a collision-window radius \(q\) and a return cutoff \(L\).  Let
\(\mathcal S_{q,L}\) be the union, over retained branches, of singularity
curves met by the expanded window.  Homogeneity and the complexity estimate
give
\[
 \#\mathcal S_{q,L}\le CLe^{\kappa q},
 \qquad
 \widehat{\mathbb P}\big(N_\delta(\mathcal S_{q,L})\big)
 \le CLe^{\kappa q}\delta^\alpha .
\]"""
        new = r"""Fix a collision-window radius \(q\), a return cutoff \(L\), and a
homogeneity cutoff \(K\).  Let \(\mathcal S_{q,L,K}\) be the union, over
retained branches, of singularity curves met by the expanded window.  The
finite-cut complexity and strip-mass bounds give, for fixed \(c_0\),
\[
 \#\mathcal S_{q,L,K}\le CLK^{c_0}e^{\kappa q},
 \qquad
 \widehat{\mathbb P}\big(N_\delta(\mathcal S_{q,L,K})\big)
 \le CLK^{c_0}e^{\kappa q}\delta^\alpha .
\]"""
        if text.count(old) != 1:
            raise SystemExit("A3 singularity-cutoff paragraph not found exactly once")
        text = text.replace(old, new, 1)
        text = text.replace(r"\mathcal S_{q,L}", r"\mathcal S_{q,L,K}")
        text = text.replace(r"\lim_{q,L\to\infty}", r"\lim_{q,L,K\to\infty}")
        text = text.replace(r"Le^{\kappa q}\delta^\alpha", r"LK^{c_0}e^{\kappa q}\delta^\alpha")
        text = text.replace(r"b_{q,L,\delta}", r"b_{q,L,K,\delta}")
        text = text.replace(r"\mathscr S_{c,q,L,\delta}", r"\mathscr S_{c,q,L,K,\delta}")
        text = text.replace(r"\mathscr S_{p,q,L,\delta}", r"\mathscr S_{p,q,L,K,\delta}")
        text = text.replace(r"\mathscr S_{\bullet,q,L,\delta}", r"\mathscr S_{\bullet,q,L,K,\delta}")
        marker = r"and the same assertion holds with \(r\) replaced by \(\mathfrak t\)."
        addition = marker + r"""
If \(h_j\) is the maximal homogeneity index of block \(j\), then
\[
 \lim_{K\to\infty}\limsup_{N\to\infty}\frac1N
 \log\widehat{\mathbb P}\left(
 \frac1N\sum_{j<N}1_{\{h_j>K\}}>\epsilon
 \right)=-\infty.
\]"""
        if text.count(marker) != 1:
            raise SystemExit("A3 frequency-ledger insertion point is ambiguous")
        text = text.replace(marker, addition, 1)
        proof_marker = r"The mark statements are the exponential-tilt argument used in
Theorem~\ref{thm:r3-a3-block}."
        proof_addition = proof_marker + r"""  For high homogeneity, use the
fixed-\(s\) pressure convergence for \(s1_{\{h>K\}}\) proved in that theorem;
Chernoff first sends \(K\to\infty\) and then \(s\to\infty\)."""
        if text.count(proof_marker) != 1:
            raise SystemExit("A3 homogeneity proof insertion point is ambiguous")
        text = text.replace(proof_marker, proof_addition, 1)
        path.write_text(text, encoding="utf-8")
        changes += 1
    return changes


def fix_a4() -> int:
    path = PAPERS / "A4-history-memory-universal-pressure" / "ROUND3_POSITIVE_CLOSURE.tex"
    start = r"For a stationary prepared path law \(\nu\), disintegrate the future given the"
    end = r"\subsection{An exact memory kernel without orthogonal dynamics}"
    replacement = r"""For a stationary prepared path law \(\nu\), disintegrate the future given
the complete resolved past and concatenate the sampled future to the past.
This gives a Borel right semigroup \(P_t^\nu\) on the history sigma-field for
every prepared law, with no continuity assumption.

Choose a countable bounded algebra \((F_j)\) which determines the history
Borel sigma-field and a countable dense set of resolvent parameters
\((a_\ell)\subset(0,\infty)\).  Put
\[
 R_a^\nu F=\int_0^\infty e^{-at}P_t^\nu F\,dt
\]
and let \(d_\nu^{\rm Ray}\) be the bounded metric generated by the functions
\(F_j\), \(R_{a_\ell}^\nu F_j\), and their rational-time images.  Its
completion has the same measurable sets as the original history space.

\begin{theorem}[Weighted history Feller theorem]
\label{thm:r3-a4-feller}
For every stationary prepared path law, the Ray completion just defined is a
Polish history realization on which \((P_t^\nu)_{t\ge0}\) is a strongly
continuous Feller contraction semigroup.  The algebra generated by the Ray
resolvents is a core for its generator.

If \(\nu\) is an exposed prepared phase generated by a weighted dynamically
H\"older potential in the simple spectral component of A2--A3, the Ray
realization may be chosen to be the explicit weighted Skorokhod history space
\((\mathsf H,d_\beta)\).  It preserves \(\mathscr C_\beta\), and for a
cylinder depending on the last \(m\) units of history,
\[
 \operatorname{Lip}_\beta(P_t^\nu F)
 \le C e^{-\gamma(t-m)_+}\operatorname{Lip}_\beta(F)
     +C\|F\|_\infty.
\]
On this spectral phase, the graph closure of the dynamically H\"older
cylinder derivation is the generator and \(\mathscr C_\beta\) is a core.
\end{theorem}

\begin{proof}
The history process is right-continuous and has a standard Borel state space.
The resolvent identity
\[
 R_a-R_b=(b-a)R_aR_b
\]
shows that the countable Ray algebra separates points modulo equality of all
future conditional laws and is invariant under the resolvent.  Completing
its evaluation metric produces a Polish Ray space with the original completed
sigma-field.  On this space each \(R_aF_j\) is continuous by construction;
the resolvent identity, positivity, and the right-continuity of paths imply
that \(P_t\) maps the uniform closure of the Ray algebra into itself and
\(P_tF\to F\) uniformly on that closure.  Thus the semigroup is Feller and
strongly continuous.  The Yosida resolvent averages
\(aR_aF\) approximate every function in the graph norm, proving the general
core assertion.

For an exposed weighted H\"older phase, the finite-connector Gibbs code has a
summable-variation conditional density.  Two pasts agreeing for \(n\) regular
symbols have future conditional laws whose Radon--Nikodym derivatives differ
by \(O(\rho^n)\).  The A3 singularity shield transfers this estimate from the
code to \(d_\beta\)-close billiard histories.  Coupling at the next common
magnet return gives failure probability
\(Ce^{-\gamma(t-m)_+}\), proving the displayed Lipschitz estimate.  The same
shield gives uniform right continuity on cylinders.  Resolvent averaging then
shows that their graph closure is the generator core.
\end{proof}"""
    return replace_region(
        path,
        start,
        end,
        replacement,
        "Ray completion just defined is a",
    )


def fix_b2() -> int:
    path = PAPERS / "B2-collision-clusters-dynamic-ldp" / "ROUND3_POSITIVE_CLOSURE.tex"
    old = r"""For cycle edges, choose the first one and apply
Lemma~\ref{lem:r3-b2-first-cycle}.  Delete it and restart the argument after
its time.  Iterating gives, for \(c\) cycles, the bound
\[
 \frac{(CTe^{r+u})^c}{c!}
 \varepsilon^{\alpha 1_{\{c\ge1\}}}
 k!C^k(T+\varepsilon)^{k-1}.
\]
The factorial is the volume of the ordered cycle-time simplex; no cycle is
counted as a new label."""
    new = r"""For a cluster containing cycle edges, choose only its first cycle and apply
Lemma~\ref{lem:r3-b2-first-cycle}; this supplies the single uniform
\(\varepsilon^\alpha\) gain required to make the entire cyclic sector
negligible.  After deleting that first edge, the remaining \(c-1\) cycle
occurrences are not claimed to give independent geometric gains.  They are
bounded by the same source-weighted collision operator and their ordered time
simplex.  Thus, for \(c\ge1\),
\[
 \frac{(CTe^{r+u})^c}{c!}
 \varepsilon^\alpha
 k!C^k(T+\varepsilon)^{k-1}
\]
is valid, while \(c=0\) is the creation-forest estimate.  The factorial is
the volume of the ordered cycle-time simplex; no cycle is counted as a new
label."""
    return replace_once(path, old, new, "remaining cycle occurrences are not claimed")


def fix_b4() -> int:
    path = PAPERS / "B4-nonlinear-kinetic-semigroups" / "ROUND3_POSITIVE_CLOSURE.tex"
    old = r"""\begin{proof}
Theorem~\ref{thm:r3-b4-generator} gives the upper and lower nonlinear
generator limits on a separating core.  Lemma~\ref{lem:r3-b4-containment}
prevents escape from compact moment sets.  Half-relaxed limits are respectively
viscosity sub- and supersolutions.  Theorem~\ref{thm:r3-b4-comparison}
identifies them with the unique action value.  Cylinder approximation and
contraction extend the convergence to bounded uniformly continuous terminal
data.  Local uniform convergence and the exact hierarchy tower give the
limiting semigroup law.
\end{proof}"""
    new = r"""\begin{proof}
The primary convergence route is the good joint density--actual-collision LDP
of B2.  Condition its initial rate on a regular initial density and apply the
Laplace principle to a bounded terminal cylinder.  The resulting variational
formula is exactly \(S_{s,t}\Phi\), because the transition part of the B2 rate
is \(\mathcal A_{s,t}\).  Uniform exponential compact containment makes this
convergence locally uniform on compact regular initial families.  Bounded
collision work is handled by the same joint Laplace principle with the
collision coordinate retained.

Theorem~\ref{thm:r3-b4-generator} is now a consistency theorem on the
separating core: it identifies the infinitesimal Hamiltonian of the already
constructed action value.  Lemma~\ref{lem:r3-b4-containment} and
Theorem~\ref{thm:r3-b4-comparison} extend the cylinder result to bounded
uniformly continuous terminal data and identify the unique viscosity
solution.  Local uniform convergence and the exact hierarchy tower give the
limiting semigroup law.
\end{proof}"""
    return replace_once(path, old, new, "The primary convergence route is the good joint")


def fix_d1() -> int:
    path = PAPERS / "D1-deterministic-theta-contractions" / "ROUND3_POSITIVE_CLOSURE.tex"
    text = path.read_text(encoding="utf-8")
    changed = 0
    old_h1 = r"""\item \(Q_\varepsilon\) extends holomorphically to \(B_{\mathbb C}^+\), is
      locally uniformly bounded there, and converges pointwise on a set with
      an accumulation point to \(Q\);
\item the laws of \(\mathcal X_\varepsilon\) are exponentially tight in a
      weighted weak topology and have a good exposed-point lower bound;"""
    new_h1 = r"""\item \(Q_\varepsilon\) extends holomorphically to \(B_{\mathbb C}^+\)
      and converges locally uniformly there to a holomorphic \(Q\); in the
      hard-sphere application this is the normal convergence of the B2
      connected-cluster series on a strictly larger complex ball;
\item the laws of \(\mathcal X_\varepsilon\) satisfy a full LDP with a good
      convex rate in the weighted weak topology, and every finite-rate point
      is approximable, with convergence of the rate, by exposed points of the
      pressure;"""
    if "normal convergence of the B2" not in text:
        if text.count(old_h1) != 1:
            raise SystemExit("D1 H1--H2 block not found exactly once")
        text = text.replace(old_h1, new_h1, 1)
        changed += 1
    old_proof = r"""Local boundedness and pointwise convergence of holomorphic functions give
normal-family convergence.  Uniqueness of the real limit identifies every
subsequence, and Cauchy's formula gives local uniform convergence of all
derivatives, proving (i).

Exponential tightness gives the pressure upper bound.  Exponential tilting at
an exposed source, together with the exposed-point lower bound, gives the
matching lower bound.  Approximation by exposed points and lower-semicontinuous
closure yield (ii)."""
    new_proof = r"""Local uniform holomorphic convergence on a larger complex ball and Cauchy's
integral formula give local uniform convergence of every Fr\'echet derivative,
proving (i).  The full LDP gives the Laplace upper bound and the lower bound at
exposed points.  The rate-preserving exposed-point approximation in (H2),
followed by lower semicontinuity, identifies the complete good rate with the
convex dual, proving (ii)."""
    if "rate-preserving exposed-point approximation" not in text:
        if text.count(old_proof) != 1:
            raise SystemExit("D1 analytic proof paragraph not found exactly once")
        text = text.replace(old_proof, new_proof, 1)
        changed += 1
    path.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changes = sanitize_all_modules()
    changes += fix_a3()
    changes += fix_a4()
    changes += fix_b2()
    changes += fix_b4()
    changes += fix_d1()
    # Run sanitation once more because substantive raw strings may meet a
    # previously normalized source file.
    changes += sanitize_all_modules()
    print(f"ROUND3_HARSH_FIXES_PASS changes={changes}")


if __name__ == "__main__":
    main()
