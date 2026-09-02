#!/usr/bin/env python3
"""Second-pass Round-31 mathematical hardening against newly exposed edge cases."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = ROOT / ".round31-hardened"


def replace_exact(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"expected fragment not found: {path.relative_to(ROOT)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    if MARKER.exists():
        print("Round 31 hardening already applied.")
        return

    a2 = ROOT / "papers/A2-sinai-homological-pressure/ROUND31_POSITIVE_CLOSURE.tex"
    replace_exact(
        a2,
        r"\ge c_D(1+|b|)^{-\nu_D},\qquad b\ne0,",
        r"\ge c_D(1+|b|)^{-\nu_D},\qquad |b|\ge1,",
    )
    replace_exact(
        a2,
        """where $b\cdot\beta=(b\cdot\beta_j)_j$.  Lattice periodic differences generate
$\Z^3$ and the periods are coprime.""",
        """where $b\cdot\beta=(b\cdot\beta_j)_j$.  The restriction $|b|\ge1$
is essential: the central neighbourhood is governed by the covariance/Riesz
expansion rather than by a Diophantine lower bound.  Lattice periodic
differences generate $\Z^3$ and the periods are coprime.""",
    )

    a4 = ROOT / "papers/A4-history-memory-universal-pressure/ROUND31_POSITIVE_CLOSURE.tex"
    replace_exact(
        a4,
        """Let $L_0$ generate a semigroup on $\cH$ satisfying
\[
 \norm{e^{tL_0}}_{\cH\to\cH}\le Me^{-\omega t}.            \tag{A4.12}
\]
Let $A:D(L_0)\to\cH$ be closed relative to $L_0$.  Assume that for some
$\sigma> -\omega$,
\[
 \sup_{\operatorname{Re}z\ge\sigma}
 \norm{A(z-L_0)^{-1}}\le\vartheta<1.                      \tag{A4.13}
\]

\begin{lemma}[Resolvent-certified relative perturbation]
\label{lem:r31-a4-relative}
The operator $L_0+A$ on $D(L_0)$ generates a semigroup, and
\[
 (z-L_0-A)^{-1}=(z-L_0)^{-1}
 [I-A(z-L_0)^{-1}]^{-1}.                                  \tag{A4.14}
\]
If (A4.13) holds on $\operatorname{Re}z\ge-\omega/2$, then
$\norm{e^{t(L_0+A)}}\le C e^{-\omega t/2}$.
\end{lemma}

\begin{proof}
The Neumann inverse in (A4.14) is uniform on the stated half-plane.  The
resolvent identity gives the Hille--Yosida powers by differentiating in $z$;
the inverse Laplace formula yields the semigroup and the exponential bound.
This is a relative-resolvent theorem, not the bounded perturbation theorem on
$\cH$.
\end{proof}""",
        """After replacing the Hilbert norm by an equivalent Lyapunov norm, assume
$L_0+\omega I$ is maximal dissipative; hence
\[
 \norm{e^{tL_0}}_{\cH\to\cH}\le e^{-\omega t}.             \tag{A4.12}
\]
Let $A:D(L_0)\to\cH$ be $L_0$-bounded with relative bound smaller than one.
Assume that $G:=L_0+A+\omega I/2$ is dissipative and
\[
 \sup_{\operatorname{Re}z\ge-\omega/2}
 \norm{A(z-L_0)^{-1}}\le\vartheta<1.                      \tag{A4.13}
\]

\begin{lemma}[Resolvent-certified relative perturbation]
\label{lem:r31-a4-relative}
The operator $L_0+A$ is closed on $D(L_0)$, generates a semigroup, and
\[
 (z-L_0-A)^{-1}=(z-L_0)^{-1}
 [I-A(z-L_0)^{-1}]^{-1}                                   \tag{A4.14}
\]
for $\operatorname{Re}z\ge-\omega/2$.  Moreover
\[
 \norm{e^{t(L_0+A)}}\le e^{-\omega t/2}.                  \tag{A4.15}
\]
\end{lemma}

\begin{proof}
Relative bound smaller than one makes $L_0+A$ closed on $D(L_0)$.  For every
$z$ in the stated half-plane, the Neumann factor in (A4.14) is invertible, so
$z-(L_0+A)$ is onto.  In particular
$\lambda I-G$ is onto for one, hence every, $\lambda>0$.  The assumed
dissipativity of $G$ and the range condition imply by the Lumer--Phillips
theorem that $G$ is maximal dissipative.  Therefore $G$ generates a
contraction semigroup, which is exactly (A4.15) after undoing the shift.  No
bounded-perturbation theorem for a merely graph-bounded operator is used.
\end{proof}""",
    )
    replace_exact(
        a4,
        r"Under (A4.12), graph invertibility of $S$, and (A4.16),",
        r"Under (A4.12)--(A4.13), graph invertibility of $S$, and (A4.16),",
    )

    b1 = ROOT / "papers/B1-microcanonical-preparation/ROUND31_POSITIVE_CLOSURE.tex"
    replace_exact(
        b1,
        """Disjoint anchor groups are conditionally independent up to a uniformly
smooth hard-core factor, so their oscillatory bounds multiply after iterated integration.""",
        """Iterate the argument in each disjoint relative-velocity block.  The
hard-core coupling remains inside the common amplitude and its mixed
derivatives are uniformly bounded, so the stationary-phase decay exponents
add under iterated integration; probabilistic independence is not required.""",
    )

    b2 = ROOT / "papers/B2-collision-clusters-dynamic-ldp/ROUND31_POSITIVE_CLOSURE.tex"
    replace_exact(
        b2,
        """On the regular set
\[
 |(v_i-v_j)(t_e^-)\cdot\omega_e|\ge\eta,\quad
 |t_e-t_{e'}|\ge\eta,\quad |v_i|\le L,                    \tag{B2.6}
\]
order variables by contact time.  Differentiating $F_T=(F_e)_{e\in T}$ with
respect to $(t_e,\omega_e)$ gives a block lower-triangular matrix.  Its
diagonal block is
\[
 \bigl((v_i-v_j)\cdot\omega_e,\,-\varepsilon
 D_{\theta_1}\omega_e,\,-\varepsilon D_{\theta_2}\omega_e\bigr),        \tag{B2.7}
\]
whose determinant has magnitude at least $c\varepsilon^2\eta$.

\begin{proposition}[Constructed causal right inverse]
\label{prop:r31-b2-tree-right-inverse}
Every regular tree history satisfying (B2.6) has a finite chronological chart
on which $DF_T$ has an explicitly constructed right inverse $R_T$ with
\[
 \norm{R_T}\le C_{K,L}\varepsilon^{-2(K-1)}\eta^{-K}.     \tag{B2.8}
\]
If a constraint is created at time $t_e$, the correction $R_T$ can be chosen
to change only $t_{e'}$, $\omega_{e'}$, and descendant root coordinates with
$t_{e'}\ge t_e$.  The finitely many charts cover the entire regular set.
\end{proposition}

\begin{proof}
Invert the diagonal blocks (B2.7) successively in chronological order.
Earlier collision maps depend only on earlier variables, so forward
substitution never changes an already solved row.  Elastic reflection is a
smooth involution on (B2.6); its derivative and inverse are bounded by a
polynomial in $\eta^{-1}$ and $L$.  Induction over the $K-1$ tree contacts
gives (B2.8) and the causal support.  A finite atlas of sphere coordinates and
contact-order types covers the compact cutoff set.  This constructs the right
inverse from the collision equations rather than assuming it as a field of
certificate data.
\end{proof}""",
        """On the regular set
\[
 |(v_i-v_j)(t_e^-)\cdot\omega_e|\ge\eta,\quad
 |t_e-t_{e'}|\ge\eta,\quad |v_i|\le L.                    \tag{B2.6}
\]
Orient every tree edge from the older component toward the component first
joined at that edge.  Immediately before the joining contact, use as three
ambient coordinates the common translation $y_e\in\R^3$ of all root positions
in the child component.  Internal contacts of that component and every
earlier contact are unchanged, while
\[
 D_{y_e}F_e=I_3.                                          \tag{B2.7}
\]
Later tree rows may depend on $y_e$, so the derivative of $F_T$ with respect
to the chronologically ordered $(y_e)_{e\in T}$ is block lower triangular
with identity diagonal.

\begin{proposition}[Constructed causal right inverse]
\label{prop:r31-b2-tree-right-inverse}
Every regular tree history satisfying (B2.6) has a finite chronological chart
on which $DF_T$ has an explicitly constructed causal right inverse $R_T$ with
\[
 \norm{R_T}\le C_{K,L}\eta^{-q_K}.                        \tag{B2.8}
\]
A correction for the row created at $t_e$ changes only the child-component
root variables at that edge and variables belonging to later contacts.  The
finitely many component-order and torus charts cover the entire regular set.
\end{proposition}

\begin{proof}
Solve the lower-triangular system by forward substitution using the identity
blocks (B2.7).  Translating a child component before its first joining contact
preserves all of its internal tree contacts and cannot affect the older
component or any earlier row.  Derivatives propagated through later elastic
reflections are bounded by a polynomial in $\eta^{-1}$ and $L$ on (B2.6),
which gives (B2.8).  A finite chronological/component atlas covers the compact
$K,L,\eta$ cutoff.  Thus the right inverse is constructed from legal component
translations and has no inverse power of the sphere diameter.
\end{proof}""",
    )
    replace_exact(
        b2,
        r"a(t)=a_0-\Lambda t,\qquad a_*=a_0-\Lambda T>0.",
        r"a(t)=a_0-\Lambda t,\qquad 0<a_*<a_0-\Lambda T.",
    )
    replace_exact(
        b2,
        """The analytic-translation counterexample is therefore respected:
existence to time $T$ requires the initial reserve $a_0-a_* =\Lambda T$.""",
        """The analytic-translation counterexample is therefore respected:
existence to time $T$ requires the strict reserve
$a_0-a_*>\Lambda T$, leaving a positive target-radius margin at the endpoint.""",
    )

    d1 = ROOT / "papers/D1-deterministic-theta-contractions/ROUND31_POSITIVE_CLOSURE.tex"
    replace_exact(
        d1,
        """P\{J_N=j,K_N=k,Y_N\in\dd y\}
 =e^{-N\cI_j(k/N,y)}N^{-d_Z/2}
 \left[a_j(k/N,y)+N^{-1/2}b_j+N^{-1}c_j+o(N^{-1})\right]
 \dd y,""",
        """P\{J_N=j,K_N=k,Y_N\in\dd y\}
 =e^{-N\cI_j(k/N,y)}N^{\lambda_j-d_Z/2}
 \left[a_j(k/N,y)+N^{-1/2}b_j+N^{-1}c_j+o(N^{-1})\right]
 \dd y,""",
    )
    replace_exact(
        d1,
        """with four source derivatives and the lattice covolume included in $a_j$.
The continuous minimizer set is a compact $C^5$ manifold""",
        """with four source derivatives and the lattice covolume included in $a_j$.
The explicit exponent $\lambda_j$ is the continuous-density normalization
exported by A2/B1 after the raw continuous sum is changed to the normalized
coordinate $Y_N$; in the standard nondegenerate $d_R$-dimensional case,
$\lambda_j=d_R/2$.  The continuous minimizer set is a compact $C^5$ manifold""",
    )
    replace_exact(
        d1,
        r"\kappa_j^{\rm fib}={d_Z\over2}+{d_R-r_j\over2}.",
        r"\kappa_j^{\rm fib}={d_Z\over2}-\lambda_j+{d_R-r_j\over2}.",
    )
    replace_exact(
        d1,
        r"\kappa_j^{\rm cell}={d_R-r_j\over2}.",
        r"\kappa_j^{\rm cell}=-\lambda_j+{d_R-r_j\over2}.",
    )
    replace_exact(
        d1,
        """On a pinned fibre retain the local lattice factor in (D1.2) and apply
Morse--Bott integration only in the $d_R-r_j$ continuous normal directions,
giving (D1.4)--(D1.5).""",
        """On a pinned fibre retain the local factor
$N^{\lambda_j-d_Z/2}$ in (D1.2) and apply Morse--Bott integration only in the
$d_R-r_j$ continuous normal directions.  This gives exactly the exponent in
(D1.5).""",
    )
    replace_exact(
        d1,
        """The lattice power cancels.  The A2/B1 Edgeworth expansion and a sixth-order
continuous normal form give the stated $N^{-1/2}$ and $N^{-1}$ coefficients.""",
        """The lattice factor $N^{-d_Z/2}$ cancels, while the upstream continuous
normalization $N^{\lambda_j}$ remains.  The A2/B1 Edgeworth expansion and a
sixth-order continuous normal form give the stated $N^{-1/2}$ and $N^{-1}$
coefficients.  For a standard isolated Gaussian phase
($\lambda_j=d_R/2$, $r_j=0$), the summed-cell exponent is zero, as required
for a phase cell of asymptotically nonzero probability.""",
    )

    verifier = ROOT / "tools/verify_round31.py"
    replace_exact(
        verifier,
        '        r"|b|\\ge B_0",\n',
        '        r"|b|\\ge B_0",\n        r"|b|\\ge1",\n',
    )
    replace_exact(
        verifier,
        '        r"\\kappa_j^{\\rm fib}",\n',
        '        r"\\kappa_j^{\\rm fib}",\n        r"N^{\\lambda_j-d_Z/2}",\n',
    )

    MARKER.write_text(
        "ROUND31_HARDENED=1\n"
        "A2_DIOPHANTINE_RANGE=|b|>=1\n"
        "A4_GENERATOR=LUMER_PHILLIPS\n"
        "B2_TARGET_RADIUS=STRICT_MARGIN\n"
        "D1_CONTINUOUS_DENSITY_EXPONENT=lambda_j\n",
        encoding="utf-8",
    )
    print("Round 31 second-pass hardening applied successfully.")


if __name__ == "__main__":
    main()
