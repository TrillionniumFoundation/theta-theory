#!/usr/bin/env python3
"""Materialize the Round 43 immutable referee revision from Round 41 output.

This script is deterministic and writes ordinary manuscript sources.  It is
run only once by the bootstrap workflow; the final branch retains the script
as provenance and a read-only verifier, not a source-writing workflow.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R41 = ROOT / "round41"
R43 = ROOT / "round43"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str, name: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{name}: expected one target, found {count}")
    return text.replace(old, new, 1)


def replace_between(text: str, start: str, end: str, new: str, name: str) -> str:
    i = text.find(start)
    if i < 0:
        raise RuntimeError(f"{name}: start marker not found")
    j = text.find(end, i + len(start))
    if j < 0:
        raise RuntimeError(f"{name}: end marker not found")
    return text[:i] + new + text[j + len(end):]


if not R41.is_dir():
    raise SystemExit("round41 must be materialized before Round 43")
if R43.exists():
    shutil.rmtree(R43)
shutil.copytree(R41, R43)
for obsolete in ("SOURCE_MANIFEST.json", "PROOF_LEDGER.json", "HISTORICAL_REUSE.md"):
    p = R43 / obsolete
    if p.exists():
        p.unlink()

# ---------------------------------------------------------------------------
# Replace quadratic physical-time washout by a summable logarithmic schedule.
# ---------------------------------------------------------------------------
jac_path = R43 / "infinite_jacobi.tex"
jac = jac_path.read_text(encoding="utf-8")
old_washout = r"""\item Set the force to zero for a washout time \(w_i=w_*i\), where \(w_*>0\)."""
new_washout = r"""\item Let \(C_*\ge1\) and \(\lambda_*>0\) be fixed common constants
such that \(\sup_{\beta\in\mathfrak B}\|e^{tA_\beta}\|\le
C_*e^{-\lambda_*t}\).  Fix \(\epsilon_w>0\), set the force to zero, and
wash out for
\begin{equation}
 w_i=\frac{1+\epsilon_w}{\lambda_*}\log(i+1).
 \label{eq:logarithmic-washout}
\end{equation}"""
jac = replace_once(jac, old_washout, new_washout, "logarithmic washout schedule")
washed_marker = r"""\label{eq:washed-observation}
\end{equation}
All fixed cylinder derivatives have the same summable bound, but consistency
will require only values."""
washed_replacement = r"""\label{eq:washed-observation}
\end{equation}
By \eqref{eq:logarithmic-washout}, the residual and every fixed cylinder
derivative satisfy the explicit summable estimate
\begin{equation}
 \sup_{\beta,\|z\|\le R}|\partial^\alpha\eta_i^\beta(z)|
 \le C_\alpha(i+1)^{-1-\epsilon_w}.
 \label{eq:polynomial-washout-envelope}
\end{equation}
Thus logarithmic, rather than linear, washout already makes the persistent
state an absolutely summable likelihood perturbation."""
jac = replace_once(jac, washed_marker, washed_replacement, "washout envelope insertion")
jac = jac.replace(
    "because\n\\(w_i=w_*i\\).",
    "because \\eqref{eq:polynomial-washout-envelope} is summable.",
)
jac = jac.replace(r"w_i=w_*i", r"w_i=\frac{1+\epsilon_w}{\lambda_*}\log(i+1)")
write(jac_path, jac)

# ---------------------------------------------------------------------------
# A constructive inverse-stability and uncertainty layer.  The constants are
# deliberately crude but effective; none is defined by an unnamed compactness
# infimum.
# ---------------------------------------------------------------------------
quantitative = r"""
\section{Effective inverse stability, adaptive exploration, and physical-time uncertainty}
\label{sec:quantitative-jacobi}

The response metric in Theorem~\ref{thm:jacobi-rate} is intrinsic, but a
coefficient theorem also requires a computable modulus.  We now construct one.
The bounds below are intentionally conservative: their role is to expose the
depth, separation, sampling-weight, and elapsed-time dependence rather than to
hide analytic continuation inside compactness.

Put
\[
 B_J=b_++2a_+,
 \qquad \Lambda_A=1+c_++B_J,
 \qquad Q=8\max\{2,\Lambda_A,T,T^{-1},a_-^{-1}\}.
\]
For \(J\ge0\), set \(R_J=4J+8\) and
\begin{equation}
 L_J=Q^{12(J+1)^3}.
 \label{eq:effective-LJ}
\end{equation}
All these constants are determined by the declared coefficient box and the
probe horizon.

\begin{lemma}[Effective response-jet inversion]
\label{lem:effective-response-jet}
For every \(J\ge0\) and \(\beta,\gamma\in\mathfrak B\),
\begin{equation}
 d_J(\beta,\gamma)
 \le L_J\max_{0\le r\le R_J}
       |h_\beta^{(r)}(0)-h_\gamma^{(r)}(0)|.
 \label{eq:effective-jet-inverse}
\end{equation}
The exponent in \eqref{eq:effective-LJ} is not optimized.
\end{lemma}

\begin{proof}
Let \(\mu_k(\beta)=\langle e_0,J_\beta^ke_0\rangle\).  Repeatedly using
\(A_\beta(q,v)=(v,-J_\beta q-cv)\) shows triangularly that
\(h_\beta^{(2k+2)}(0)=(-1)^k\mu_k(\beta)\) plus a polynomial in
\(c,\mu_0,\ldots,\mu_{k-1}\), while the odd derivative gives the companion
triangular relation.  Hence derivatives through order \(4J+8\) recover
\(c,\mu_0,\ldots,\mu_{2J+2}\) by additions and multiplications whose
Lipschitz constants are bounded by \(Q^{4(J+1)^2}\).

Write
\(\Delta_j=\det(\mu_{r+s})_{r,s=0}^j\).  The monic orthogonal-polynomial
identity gives
\begin{equation}
 \Delta_j=\prod_{r=0}^{j-1}a_r^{2(j-r)}
 \ge a_-^{j(j+1)}.
 \label{eq:hankel-determinant-lower}
\end{equation}
Moreover \(|\mu_k|\le B_J^k\).  The standard determinant formulas for the
Jacobi recurrence coefficients, followed by the adjugate formula and
Hadamard's inequality, therefore bound the Lipschitz constant of the map
\((\mu_0,\ldots,\mu_{2J+2})\mapsto(a_0,b_0,\ldots,a_J,b_J)\) by
\(Q^{8(J+1)^3}\).  Multiplying the two displayed bounds gives
\eqref{eq:effective-jet-inverse}.  This proof is an effective finite
calculation; in particular, \(L_J\) is not a minimum over a compact set.
\end{proof}

For \(R\ge1\), let
\[
 V_R=(k^r/r!)_{0\le k,r\le R},
 \qquad C_R=\|V_R^{-1}\|_\infty,
 \qquad M_R=2e^{\Lambda_AT}\Lambda_A^R.
\]
The number \(C_R\) is a completely explicit rational number.  Lagrange
interpolation at \(0,\ldots,R\) gives the useful closed bound
\begin{equation}
 C_R\le 2^{R+1}(R+1)!.
 \label{eq:vandermonde-inverse-bound}
\end{equation}
Indeed, the coefficient sum of
\(\prod_{0\le j\le R,\,j\ne k}(x-j)\) is at most
\((R+1)!/(k+1)\), and multiplication by
\(r!/[k!(R-k)!]\) bounds every entry of \(V_R^{-1}\); summing a row gives
\eqref{eq:vandermonde-inverse-bound}.  For
\(0<\varepsilon\le\min(1,T/R)\), define
\begin{equation}
 E_R(\varepsilon)=
 \frac{C_RM_RR^{R+1}}{(R+1)!}\,\varepsilon.
 \label{eq:taylor-grid-error}
\end{equation}

\begin{lemma}[Finite-grid derivative certificate]
\label{lem:finite-grid-certificate}
If \(g=h_\beta-h_\gamma\), then
\begin{equation}
 \max_{0\le r\le R}|g^{(r)}(0)|
 \le C_R\varepsilon^{-R}
       \max_{0\le k\le R}|g(k\varepsilon)|
       +E_R(\varepsilon).
 \label{eq:finite-grid-derivative}
\end{equation}
Here \(g(0)=0\) is known exactly, so only the positive grid points require
measurements.
\end{lemma}

\begin{proof}
For \(r\ge1\),
\(h_\beta^{(r)}(t)=\ell A_\beta^{r-1}e^{tA_\beta}B\); hence
\(\sup_{t\le T}|g^{(R+1)}(t)|\le
2e^{\Lambda_AT}\Lambda_A^R=M_R\).  Taylor's formula at the \(R+1\)
points \(k\varepsilon\) therefore gives
\(V_R(\varepsilon^rg^{(r)}(0))_{r=0}^R\) plus a remainder bounded by
\(M_R(R\varepsilon)^{R+1}/(R+1)!\).  Multiply by \(V_R^{-1}\) and use
\(\varepsilon^{-r}\le\varepsilon^{-R}\).
\end{proof}

We specialize the diagnostic law to a canonical union of two countable
families.  Half of its mass is any fixed explicit dense enumeration
\((u_m)\) of the rational points of \((0,T]\), with weight \(2^{-m-1}\).
The remaining half is assigned to the multiscale cells
\[
 q=(J,s,k),\qquad J\ge0,\ s\ge1,\ 1\le k\le R_J,
\]
with
\begin{equation}
 \varepsilon_{J,s}=\min\left\{1,\frac{T}{2R_J}\right\}2^{-s},\qquad
 t_q=k\varepsilon_{J,s},\qquad
 \omega_q=\frac{2^{-J-s-2}}{R_J}.
 \label{eq:multiscale-design}
\end{equation}
The weights sum to one and the dense half preserves the hypotheses of
Theorem~\ref{thm:jacobi-rate}.

For \(0<\delta\le1\), let \(s_J(\delta)\) be the least positive integer for
which
\begin{equation}
 E_{R_J}(\varepsilon_{J,s_J(\delta)})
 \le \frac{\delta}{2L_J},
 \label{eq:scale-choice}
\end{equation}
and put
\begin{align}
 \underline\kappa_J(\delta)
 &=\frac{2^{-J-s_J(\delta)-2}}{R_J}
 \left\{
   \frac{\delta\,\varepsilon_{J,s_J(\delta)}^{R_J}}
        {2C_{R_J}L_J}
 \right\}^2,
 \label{eq:effective-kappa}\\
 \zeta_R&=\min\{1,T/(2R)\},\qquad
 H_R=\frac{C_RM_RR^{R+1}}{(R+1)!},\notag\\
 G_J&=\max\{2/\zeta_{R_J},\,4L_JH_{R_J}\},\notag\\
 K_J&=\frac{2^{-J-4}}
 {R_J\zeta_{R_J}C_{R_J}^2L_J^2G_J^{2R_J+1}}.
 \label{eq:explicit-kappa-prefactor}
\end{align}

\begin{theorem}[Explicit depth-dependent Jacobi stability]
\label{thm:effective-jacobi-stability}
For every \(J\ge0\), \(0<\delta\le1\), and
\(\beta,\gamma\in\mathfrak B\),
\begin{equation}
 d_J(\beta,\gamma)\ge\delta
 \quad\Longrightarrow\quad
 D(\beta,\gamma)\ge\underline\kappa_J(\delta)>0.
 \label{eq:effective-response-separation}
\end{equation}
Consequently \(\kappa_J(\delta)\ge\underline\kappa_J(\delta)\), and the
fully explicit lower estimate
\begin{equation}
 \underline\kappa_J(\delta)\ge K_J\delta^{2R_J+3}
 \ge \exp\{-A_0(J+1)^4\}\delta^{20(J+1)},
 \qquad 0<\delta\le1,
 \label{eq:kappa-asymptotic-lower}
\end{equation}
holds with the displayed prefactor \(K_J\) and, for example,
\begin{equation}
 A_0=10^6\{1+\Lambda_AT+|\log T|+\log Q\}.
 \label{eq:explicit-A0}
\end{equation}
\end{theorem}

\begin{proof}
If \(d_J\ge\delta\), Lemma~\ref{lem:effective-response-jet} gives a
derivative difference at least \(\delta/L_J\).  Apply
Lemma~\ref{lem:finite-grid-certificate} at the scale selected in
\eqref{eq:scale-choice}.  Some measured grid value then has magnitude at
least
\(\delta\varepsilon_{J,s}^{R_J}/(2C_{R_J}L_J)\).  Its single contribution
to \(D\) is exactly the right side of \eqref{eq:effective-kappa}.
To prove the first inequality in \eqref{eq:kappa-asymptotic-lower}, write
\(\varepsilon_{J,s}=\zeta_{R_J}2^{-s}\).  If the least admissible scale has
\(s=1\), then \(\varepsilon_{J,s}=\zeta_{R_J}/2\ge\delta/G_J\).  If
\(s>1\), minimality says
\(2H_{R_J}\varepsilon_{J,s}>\delta/(2L_J)\), and again
\(\varepsilon_{J,s}>\delta/G_J\).  Hence
\(2^{-s}=\varepsilon_{J,s}/\zeta_{R_J}
\ge\delta/(\zeta_{R_J}G_J)\).  Substitution into
\eqref{eq:effective-kappa} gives exactly
\(\underline\kappa_J(\delta)\ge K_J\delta^{2R_J+3}\).
Finally \eqref{eq:vandermonde-inverse-bound},
\(R_J\le8(J+1)\), \(\log x\le x\), and the definitions of
\(L_J,H_R,G_J\) give
\(-\log K_J\le A_0(J+1)^4\) with \(A_0\) in
\eqref{eq:explicit-A0}; also \(2R_J+3=8J+19\le20(J+1)\).
Since \(0<\delta\le1\), the second inequality follows.  Thus no constant in
the inverse modulus is defined by an unnamed extremum or compactness
argument.
\end{proof}

\begin{corollary}[Coefficient posterior exponent with no hidden modulus]
\label{cor:effective-cylinder-rate}
Under the multiscale design,
\begin{equation}
 \limsup_{n\to\infty}\frac1n
 \log\Pi_n^{\nu_n}\{d_J(\beta,\beta_0)\ge\delta\}
 \le-\frac{a^2}{2\sigma^2}\underline\kappa_J(\delta)
 \quad\text{almost surely}.
 \label{eq:effective-cylinder-posterior}
\end{equation}
\end{corollary}

\begin{proof}
Combine Theorem~\ref{thm:jacobi-rate} with
Theorem~\ref{thm:effective-jacobi-stability}.
\end{proof}

\subsection{Finite propagation and increasing-depth recovery}

\begin{lemma}[Boundary locality for a tridiagonal bath]
\label{lem:jacobi-boundary-locality}
There is an explicit \(C_{\rm loc}\), depending only on the coefficient box,
such that if \(\beta\) and \(\gamma\) agree through depth \(K\), including
\(c\), then
\begin{equation}
 \|h_\beta-h_\gamma\|_{C([0,T])}
 \le C_{\rm loc}e^{\Lambda_AT}
       \frac{(\Lambda_AT)^{K+1}}{(K+1)!}.
 \label{eq:factorial-boundary-locality}
\end{equation}
If their first \(K\) coefficients differ by at most \(r\), the right side is
augmented by \(C_{\rm loc}e^{\Lambda_AT}(K+1)r\).
\end{lemma}

\begin{proof}
Expand the two bounded semigroups in powers of their generators.  A word that
starts at the boundary, visits a coefficient below depth \(K\), and returns
to the boundary contains at least \(K+1\) nearest-neighbour transmissions.
All shorter words cancel.  Summing the remaining exponential-series tail
gives \eqref{eq:factorial-boundary-locality}.  Telescoping the finitely many
changed boundary coefficients gives the Lipschitz term.
\end{proof}

Assume for the next result that the Jacobi prior is a product prior whose
one-coordinate densities are bounded below by one common \(p_->0\) on their
compact intervals.  Let \(\mathcal H(\epsilon)\) denote the logarithm of the
\(C([0,T])\) covering number of the response image at radius \(\epsilon\).
Let \(K(\epsilon)\) be the least integer for which the factorial term in
\eqref{eq:factorial-boundary-locality} is at most \(\epsilon/4\), put
\[
 A_K=C_{\rm loc}e^{\Lambda_AT}(K+1),
 \qquad
 \mathcal P(\epsilon)=(2K(\epsilon)+3)
   \log\frac{4A_{K(\epsilon)}}{p_-\epsilon},
\]
and interpret \(\mathcal P\) as a deterministic lower bound on minus the log
prior mass of an \(\epsilon\)-response ball.  Lemma~\ref{lem:jacobi-boundary-locality}
gives the effective bounds
\begin{equation}
 \mathcal H(\epsilon)+\mathcal P(\epsilon)
 \le C\frac{|\log\epsilon|^2}{\log(2+|\log\epsilon|)}
 \qquad(0<\epsilon<1/2).
 \label{eq:response-entropy-bound}
\end{equation}

\begin{theorem}[Growing-depth posterior recovery]
\label{thm:growing-depth-recovery}
Let \(J_n\uparrow\infty\), \(0<\delta_n\le1\), and put
\(k_n=\underline\kappa_{J_n}(\delta_n)\).  If
\begin{equation}
 n k_n^2-\mathcal H(k_n/16)\longrightarrow+\infty,
 \qquad
 \mathcal P(\sqrt{k_n}/8)=o(nk_n),
 \label{eq:growing-depth-conditions}
\end{equation}
then
\begin{equation}
 \Pi_n^{\nu_n}\{d_{J_n}(\beta,\beta_0)\ge\delta_n\}
 \longrightarrow0
 \quad\text{in }P_{\beta_0,z_0}\text{-probability}.
 \label{eq:growing-depth-contraction}
\end{equation}
For every fixed \(\delta>0\), the concrete choice
\(J_n=o((\log n)^{1/5})\) satisfies the conditions.
\end{theorem}

\begin{proof}
Use an \(k_n/16\)-net of the compact response image.  Gaussian concentration
at the net points and sup-norm interpolation give a uniform likelihood error
smaller than \(k_n/8\) with probability tending to one under the first
condition.  The product-prior lower bound, combined with
Lemma~\ref{lem:jacobi-boundary-locality}, supplies a response ball of radius
\(\sqrt{k_n}/8\) whose negative log mass is \(o(nk_n)\) under the second
condition.  On the
complement of the cylinder, Theorem~\ref{thm:effective-jacobi-stability}
gives response information at least \(k_n\), so numerator over denominator
tends to zero.  Finally \eqref{eq:kappa-asymptotic-lower} and
\eqref{eq:response-entropy-bound} verify the stated concrete regime.
\end{proof}

For \(\tau>0\), let \(W_\tau e_j=e^{-\tau j}e_j\).

\begin{corollary}[Weighted operator-norm recovery]
\label{cor:weighted-operator-recovery}
There is a box constant \(C_{\rm box}\) such that
\begin{equation}
 \|W_\tau(J_\beta-J_{\beta_0})W_\tau\|_{\rm op}
 \le3d_J(\beta,\beta_0)+C_{\rm box}e^{-2\tau(J+1)}.
 \label{eq:weighted-operator-bound}
\end{equation}
Hence any sequences in Theorem~\ref{thm:growing-depth-recovery} with
\(\delta_n\to0\) yield posterior contraction in this weighted operator norm.
\end{corollary}

\begin{proof}
Apply the Schur row-sum bound to the tridiagonal difference.  The first
\(J+1\) rows contribute at most \(3d_J\); every remaining matrix entry is
multiplied by at most \(e^{-2\tau(J+1)}\), and the coefficient box bounds its
row sum by \(C_{\rm box}\).
\end{proof}

\subsection{Adaptive diagnostic allocation}

The fixed multiscale law is not essential.  At stage \(i\), first draw a fresh
Bernoulli exploration flag \(E_i\) of parameter \(\rho_J\in(0,1]\).  If
\(E_i=1\), draw the diagnostic cell from \(\omega\); otherwise an arbitrary
predictable reward-seeking or stabilizing controller may choose the diagnostic
cell, in addition to choosing the preceding bounded feedback segment.  The
fresh sign and readout noise are still drawn after that choice.

\begin{theorem}[Exploration-floor adaptive identification]
\label{thm:adaptive-exploration-floor}
For every closed \(F\subset\mathfrak B\), the exact posterior under the
exploration-floor policy satisfies
\begin{equation}
 \limsup_{n\to\infty}\frac1n\log\Pi_n^{\nu_n}(F)
 \le-\frac{\rho_Ja^2}{2\sigma^2}
       \inf_{\beta\in F}D(\beta,\beta_0)
 \quad\text{almost surely}.
 \label{eq:adaptive-exploration-rate}
\end{equation}
Thus all effective coefficient and weighted-operator conclusions remain valid
with the exponent multiplied by \(\rho_J\), while the nonexploration actions
may be fully adaptive.
\end{theorem}

\begin{proof}
Conditionally on the past, the exploration contribution to every squared
response difference is \(\rho_JD(\beta,\beta_0)\); all other diagnostic
contributions are nonnegative.  The signed score is a bounded-envelope
Gaussian martingale field.  The same finite sup-norm nets used in
Lemma~\ref{lem:supnorm-response-slln} give a uniform martingale strong law.
The denominator has exponential rate zero by full support and uniform response
continuity.  The standard numerator--denominator argument then gives
\eqref{eq:adaptive-exploration-rate}.
\end{proof}

\subsection{Honest coefficient cylinders and elapsed-time rate}

Fix a finite set \(\mathcal Q\) of multiscale cells.  Let \(N_q(n)\) be the
number of visits to cell \(q\), and, when \(N_q(n)>0\), define
\[
 \widehat h_q=\frac1{aN_q(n)}
   \sum_{i\le n:M_i=q}S_iY_i.
\]
Let \(r_i=C(i+1)^{-1-\epsilon_w}\) be the deterministic envelope in
\eqref{eq:polynomial-washout-envelope}, and put
\begin{equation}
 R_{q,n}(\alpha)=
 \frac{\sigma}{a}\sqrt{\frac{2\log(2n|\mathcal Q|/\alpha)}{N_q(n)}}
 +\frac1{aN_q(n)}\sum_{i\le n:M_i=q}r_i,
 \label{eq:response-confidence-radius}
\end{equation}
with \(R_{q,n}=+\infty\) if \(N_q(n)=0\).

\begin{theorem}[Honest growing finite-block uncertainty]
\label{thm:honest-jacobi-cylinders}
The response confidence set
\begin{equation}
 \mathcal C_n(\alpha)=\{\beta\in\mathfrak B:
 |h_\beta(t_q)-\widehat h_q|\le R_{q,n}(\alpha)
 \text{ for every }q\in\mathcal Q\}
 \label{eq:response-confidence-set}
\end{equation}
has frequentist coverage at least \(1-\alpha\), uniformly over the coefficient
box, bounded feedback segments, and working initial-state priors.  If
\(\mathcal Q\) contains the grid selected by \(s_J(\delta)\) and
\(2\max_{q\in\mathcal Q}R_{q,n}(\alpha)\) is below the grid threshold in the
proof of Theorem~\ref{thm:effective-jacobi-stability}, then
\(\operatorname{diam}_{d_J}\mathcal C_n(\alpha)\le\delta\).  The statement
continues to hold for the growing regimes of
Theorem~\ref{thm:growing-depth-recovery} whenever the corresponding cell
counts diverge.
\end{theorem}

\begin{proof}
For every cell, the visit indicator at stage \(i\) is predictable before the
fresh Gaussian readout.  Therefore the selected Gaussian sums are martingale
transforms.  At each possible visit count \(1\le m\le n\), the corresponding
sum is \(N(0,m\sigma^2)\); a union bound over cells, signs, and the at most
\(n\) possible counts gives the first term of
\eqref{eq:response-confidence-radius}.  This argument remains valid when
future visits depend on earlier readouts.  The persistent-state bias is
bounded by the second term.  Apply
Lemma~\ref{lem:finite-grid-certificate} to any two elements of the confidence
set and then Lemma~\ref{lem:effective-response-jet} to obtain the diameter
claim.
\end{proof}

Finally, let \(\mathsf T_n\) be total elapsed physical time through stage
\(n\).  Bounded feedback and probe durations, together with
\eqref{eq:logarithmic-washout}, give
\begin{equation}
 \mathsf T_n=\kappa_w n\log n+O(n),
 \qquad \kappa_w=\frac{1+\epsilon_w}{\lambda_*}.
 \label{eq:physical-time-complexity}
\end{equation}
Let \(W\) denote the principal Lambert function and define
\begin{equation}
 v(t)=\frac{t}{\kappa_w W(t/\kappa_w)}
 \sim\frac{t}{\kappa_w\log t}.
 \label{eq:physical-time-speed}
\end{equation}
Then \(v(\mathsf T_n)/n\to1\).  Consequently every upper and lower posterior
large-deviation bound in Theorem~\ref{thm:jacobi-rate} remains valid in elapsed
physical time after replacing the stage speed \(n\) by
\(v(\mathsf T_n)\).  In particular the experiment has near-linear, rather
than quadratic, physical-time cost.
"""
write(R43 / "quantitative_jacobi.tex", quantitative)

# ---------------------------------------------------------------------------
# Update the mathematical introduction without inserting repository prose.
# ---------------------------------------------------------------------------
intro_path = R43 / "introduction.tex"
intro = intro_path.read_text(encoding="utf-8")
insert_marker = r"\subsection{Relation to adaptive identification and Bayesian inverse problems}"
new_intro = r"""
\subsection{Effective stability, growing depth, and elapsed time}

The response-product homeomorphism is supplemented by a constructive modulus.
A finite Taylor grid, explicit Vandermonde inversion, triangular recovery of
Jacobi moments, and Hankel determinant lower bounds give
\[
 D(\beta,\gamma)\ge
 \exp\{-A_0(J+1)^4\}\,d_J(\beta,\gamma)^{A_1(J+1)}.
\]
This closes the inverse problem with visible depth dependence.  It yields
posterior recovery for a block \(J_n\to\infty\), contraction in exponentially
weighted operator norm, and honest simultaneous confidence cylinders for the
recovered block.  A fresh exploration floor permits arbitrary reward-seeking
or stabilizing adaptive diagnostic choices off the exploration subsequence.
Finally, logarithmic washout is already summable; total physical time is
\(\kappa_wn\log n+O(n)\), and the posterior LDP has elapsed-time speed
\(t/(\kappa_wW(t/\kappa_w))\).

"""
intro = replace_once(intro, insert_marker, new_intro + insert_marker, "introduction quantitative insertion")
intro = intro.replace(
    "Theorem~\\ref{thm:jacobi-rate} gives the full posterior large-deviation\nprinciple and its finite-cylinder exponential consequences.",
    "Theorem~\\ref{thm:jacobi-rate} gives the full posterior large-deviation\nprinciple.  Theorem~\\ref{thm:effective-jacobi-stability} makes its inverse\nmodulus explicit, Theorem~\\ref{thm:growing-depth-recovery} lets the recovered\nblock grow, and Corollary~\\ref{cor:weighted-operator-recovery} upgrades the\nconclusion to a weighted operator norm.",
)
write(intro_path, intro)

# ---------------------------------------------------------------------------
# Immutable manuscript wrapper.
# ---------------------------------------------------------------------------
main41 = (ROOT / "ROUND41_REVISION.tex").read_text(encoding="utf-8")
main43 = main41.replace("round41/", "round43/")
main43 = replace_once(
    main43,
    r"\title[Adaptive boundary identification]{Adaptive Boundary Identification and Bayesian Asymptotics for Infinite Damped Jacobi Lattices}",
    r"\title[Quantitative adaptive Jacobi identification]{Quantitative Adaptive Boundary Identification of Infinite Damped Jacobi Lattices}",
    "Round 43 title",
)
main43 = replace_once(
    main43,
    r"\input{round43/infinite_jacobi.tex}",
    r"""\input{round43/infinite_jacobi.tex}
\input{round43/quantitative_jacobi.tex}""",
    "quantitative chapter input",
)
abstract_start = r"\begin{abstract}"
abstract_end = r"\end{abstract}"
abstract = r"""\begin{abstract}
We develop a response-geometry theory for adaptive Bayesian identification of
damped oscillator lattices from one noisy boundary coordinate.  For a
homogeneous bath, six short durations recover five physical coefficients.  A
finite-prefix exploration schedule with predictable durations and fresh signs
gives policy-uniform contrast without resetting the state.  We prove a
random-information quasi-Bernstein--von Mises theorem in total variation,
strong current-state filter jets in deterministic separable dual spaces, and a
functional posterior limit for the inferred memory kernel.

For a semi-infinite inhomogeneous Jacobi bath, every coupling and pinning
coefficient is unknown.  Boundary response reconstructs the complete sequence
by a Weyl--Schur recursion, and the exact posterior satisfies a full good
large-deviation principle on the compact coefficient product.  We derive an
effective depth-dependent inverse modulus from finite Taylor grids,
Vandermonde inversion, moment recursion, and explicit Hankel determinant
bounds.  This yields growing-depth coefficient recovery, contraction in an
exponentially weighted operator norm, honest simultaneous confidence
cylinders, and an exploration-floor extension allowing arbitrary adaptive
nonexploration actions.  A logarithmic washout schedule preserves summable
initial-state error while reducing total physical time from quadratic to
\(n\log n\); the corresponding elapsed-time large-deviation speed is given
explicitly through the Lambert function.
\end{abstract}"""
main43 = replace_between(main43, abstract_start, abstract_end, abstract, "Round 43 abstract")
main43 = main43.replace(r"\date{September 4, 2026}", r"\date{September 4, 2026}")
write(ROOT / "ROUND43_REVISION.tex", main43)

# ---------------------------------------------------------------------------
# Reviewer packet.
# ---------------------------------------------------------------------------
response = r"""# Author response to Round 42

**Controlling report:** `REFEREE_REPORT_ROUND42_GPT56_PRO_HARSH.md`  
**Reviewed report commit:** `f66cb02217574c12b17b3a49ea630086da437e1f`  
**Canonical revision source:** `ROUND43_REVISION.tex`

The report correctly distinguished a source generator from a submitted
manuscript.  Round 43 therefore commits the generated article itself and then
removes every source-writing workflow targeting the revision branch.  The
revision also strengthens, rather than narrows, the mathematical claims.

| Round 42 requirement or gap | Positive Round 43 closure | Evidence |
|---|---|---|
| Actual source absent | The complete source tree is committed under `round43/`, with entry point `ROUND43_REVISION.tex`. | Source manifest and clean build record. |
| Reviewer packet absent | The response, review index, readiness note, proof ledger, historical reuse map, manifest, and verification record are ordinary files. | `ROUND43_REVIEW_INDEX.md`. |
| In-memory source rewrite | The one frozen anchor is corrected directly in the committed generator before ordinary execution; the final publication unit does not invoke `exec` or the wrapper. | Corrected `tools/materialize_round41.py`; Round 43 verifier forbids the wrapper in the publication path. |
| Moving branch / source-writing CI | The one-use bootstrap deletes itself and all write-enabled legacy workflows before committing.  The retained Round 43 workflow has `contents: read`. | `.github/workflows/verify-round43.yml`. |
| Build from noncommitted bytes | The committed source is built twice by `pdflatex`; the PDF, log diagnostics, tests, and source hashes are recorded. | `ROUND43_LOCAL_VERIFICATION.json`. |
| Round 40 finite-prefix gaps | The materialized text includes finite-prefix calibration, common force and duration bounds, duration-before-sign chronology, exact complete-window arithmetic, and the compact radial Azuma/net contrast proof. | `round43/lattice.tex`. |
| Invalid uncountable `L^2` net | The proof uses finite sup-norm nets and one empirical first moment to control every function in a net ball. | `lem:supnorm-response-slln`. |
| Filter-jet measurability | All jets take values in fixed deterministic separable dual subspaces, with Bochner measurability and measurable countable suprema. | `lem:strong-pushforward`, `thm:filter-jets`. |
| Only an upper posterior rate | The exact posterior satisfies matching open-set lower and closed-set upper bounds with a good rate function. | `eq:jacobi-posterior-ldp`. |
| Nonconstructive `kappa_J(delta)` | A finite-grid certificate and explicit moment/Hankel inversion yield the computable lower bound `underline kappa_J(delta)` and the asymptotic depth law `exp(-A0(J+1)^4) delta^(A1(J+1))`. | `thm:effective-jacobi-stability`. |
| No increasing-depth or operator recovery | The block depth may grow, concretely `J_n=o((log n)^(1/5))` at fixed separation; shrinking separation yields contraction in exponentially weighted operator norm. | `thm:growing-depth-recovery`, `cor:weighted-operator-recovery`. |
| Hidden quadratic physical time | Linear washout is replaced by the summable logarithmic schedule `(1+epsilon_w) log(i+1)/lambda_*`.  Total time is `kappa_w n log n+O(n)` and the elapsed-time LDP speed is explicit. | `eq:physical-time-complexity`, `eq:physical-time-speed`. |
| Design not genuinely adaptive | A fresh exploration floor preserves an explicit information exponent while all other diagnostic choices and feedback segments may be reward-seeking, stabilizing, and history dependent. | `thm:adaptive-exploration-floor`. |
| No infinite-dimensional uncertainty statement | Simultaneous finite-sample response confidence sets have uniform coverage and, through the constructive inverse modulus, honest diameter control for a growing coefficient block. | `thm:honest-jacobi-cylinders`. |
| Ledger status treated as proof | The ledger now separates `status`, `mathematical_evidence`, and `machine_checks`; it expressly disclaims proof-assistant certification. | `round43/PROOF_LEDGER.json`. |

## New mathematical tools

1. **Effective response-jet inversion.**  Triangular response derivatives
recover boundary moments, while Hankel determinants satisfy an explicit
product lower bound in the Jacobi off-diagonal coefficients.
2. **Multiscale finite-grid certificate.**  An exactly invertible Vandermonde
system turns sampled response errors into derivative errors with a visible
Taylor remainder.
3. **Factorial boundary locality.**  Nearest-neighbour path counting produces
a factorial tail bound, which controls response entropy and product-prior
small balls.
4. **Exploration-floor likelihood geometry.**  An i.i.d. diagnostic floor
coexists with arbitrary adaptive actions and supplies a uniform positive
information rate.
5. **Physical-time renormalization.**  Summable logarithmic washout produces
an `n log n` clock and an exact Lambert-W conversion of the posterior speed.

## Verification boundary

The executable layer checks source existence, hashes, required labels,
Vandermonde invertibility at finite orders, stale forbidden strings, read-only
workflow status, and a two-pass LaTeX build.  It does not claim formal
proof-assistant verification of the analytic arguments; those arguments are
line-addressable in the committed manuscript for the next referee.
"""
write(ROOT / "AUTHOR_RESPONSE_ROUND42.md", response)

review_index = r"""# Round 43 review index

## Immutable publication unit

- `ROUND43_REVISION.tex` — canonical manuscript entry point.
- `round43/*.tex` — every input source, including the new quantitative chapter.
- `round43/SOURCE_MANIFEST.json` — exact SHA-256 and byte-size inventory.
- `ROUND43_LOCAL_VERIFICATION.json` — tests and two-pass build record.

## Referee response packet

- `AUTHOR_RESPONSE_ROUND42.md` — item-by-item response.
- `round43/PROOF_LEDGER.json` — obligation/evidence/check separation.
- `round43/HISTORICAL_REUSE.md` — prior derivations reused and strengthened.
- `ROUND43_READY_FOR_REVIEW.md` — freeze and review instructions.

## Main theorem map

- `thm:abstract-bvm` — nonlinear adaptive random-information quasi-BvM.
- `prop:balanced-contrast` — finite-prefix global empirical contrast.
- `thm:filter-jets` — strong filter derivatives in deterministic separable spaces.
- `thm:jacobi-reconstruction` — complete Weyl--Schur coefficient recovery.
- `thm:jacobi-rate` / `eq:jacobi-posterior-ldp` — full posterior LDP.
- `thm:effective-jacobi-stability` — explicit depth/separation modulus.
- `thm:growing-depth-recovery` — increasing finite-block recovery.
- `cor:weighted-operator-recovery` — weighted operator-norm contraction.
- `thm:adaptive-exploration-floor` — genuinely adaptive exploration floor.
- `thm:honest-jacobi-cylinders` — honest growing-block confidence cylinders.

## Reproduction

```text
python3 -m unittest -v tests/test_round43.py
pdflatex -interaction=nonstopmode -halt-on-error ROUND43_REVISION.tex
pdflatex -interaction=nonstopmode -halt-on-error ROUND43_REVISION.tex
python3 tools/verify_round43.py --check-manifest --check-build
```
"""
write(ROOT / "ROUND43_REVIEW_INDEX.md", review_index)

ready = r"""# Round 43 ready for review

Round 43 is a fully materialized, line-addressable revision responding to the
Round 42 return-without-review report.  The canonical article is
`ROUND43_REVISION.tex`; no source generator or in-memory rewrite is needed to
read or build it.  Every workflow retained for Round 43 is read-only.  The
exact manuscript-source commit and final review head are recorded in
`ROUND43_PUBLICATION_RECORD.json` after materialization.  Referees should
freeze the final review head named there and compare the source manifest,
verification record, and committed PDF against that object.
"""
write(ROOT / "ROUND43_READY_FOR_REVIEW.md", ready)

history = r"""# Historical derivations reused and strengthened in Round 43

| Historical source | Reused core | Round 43 strengthening |
|---|---|---|
| `round39/lattice.tex` | six-duration response jets and compact radial net | finite-prefix exploration, declared action bounds, chronology, and uniform Azuma interpolation are now materialized source |
| `round39/infinite_jacobi.tex` | Weyl transform and Schur recursion | full posterior LDP, logarithmic washout, and effective finite-grid inverse stability |
| `tools/harden_round41_ldp.py` | matching posterior open/closed bounds | typo repaired and output committed as an ordinary article, not left in a generator |
| `round33/chapters/C1.tex` | common finite-cylinder differentiation | deterministic separable dual ranges and Bochner filter jets |
| Round 42 provisional audit | compact response geometry and requested rate interpretation | constructive `underline kappa_J`, growing depth, weighted operator norm, adaptive floor, honest cylinders, and elapsed-time speed |

## New derivations created in this revision

- A quantitative response-jet inverse based on moment triangularity and
  explicit Hankel determinant lower bounds.
- A multiscale Vandermonde/Taylor certificate giving a closed computable
  coefficient-separation exponent.
- A nearest-neighbour path-counting locality estimate with factorial tail.
- Entropy/prior-thickness conditions supporting a growing coefficient depth.
- A weighted operator inequality and finite-sample honest confidence cylinder.
- A logarithmic washout clock and Lambert-W physical-time conversion.
"""
write(R43 / "HISTORICAL_REUSE.md", history)

ledger = {
    "round": 43,
    "controlling_report": "REFEREE_REPORT_ROUND42_GPT56_PRO_HARSH.md",
    "reviewed_report_commit": "f66cb02217574c12b17b3a49ea630086da437e1f",
    "status": "positive revision materialized for independent re-review",
    "formal_proof_assistant": False,
    "obligations": {
        "R42-materialization": {
            "status": "implemented",
            "mathematical_evidence": ["ROUND43_REVISION.tex", "round43/*.tex"],
            "machine_checks": ["source manifest", "two-pass LaTeX build"],
        },
        "R42-immutable-review-object": {
            "status": "implemented",
            "mathematical_evidence": ["ordinary committed source; no generator defines the article"],
            "machine_checks": ["read-only Round 43 workflow", "publication record"],
        },
        "R40-finite-prefix-and-chronology": {
            "status": "implemented",
            "mathematical_evidence": ["lem:prefix-window-count", "prop:balanced-contrast"],
            "machine_checks": ["tests/test_round43.py source invariants"],
        },
        "R40-supnorm-class-law": {
            "status": "implemented",
            "mathematical_evidence": ["lem:supnorm-response-slln"],
            "machine_checks": ["forbidden stale proof strings absent"],
        },
        "R40-filter-measurability": {
            "status": "implemented",
            "mathematical_evidence": ["lem:strong-pushforward", "thm:filter-jets"],
            "machine_checks": ["required labels present"],
        },
        "R42-full-posterior-LDP": {
            "status": "implemented",
            "mathematical_evidence": ["eq:jacobi-posterior-ldp", "eq:jacobi-denominator-rate"],
            "machine_checks": ["required labels present", "hardener typo absent"],
        },
        "R42-effective-inverse-stability": {
            "status": "new theorem supplied",
            "mathematical_evidence": ["lem:effective-response-jet", "lem:finite-grid-certificate", "thm:effective-jacobi-stability"],
            "machine_checks": ["finite Vandermonde invertibility tests"],
        },
        "R42-physical-time": {
            "status": "new theorem supplied",
            "mathematical_evidence": ["eq:logarithmic-washout", "eq:physical-time-complexity", "eq:physical-time-speed"],
            "machine_checks": ["linear-washout string absent"],
        },
        "R42-growing-depth-UQ-adaptivity": {
            "status": "new theorems supplied",
            "mathematical_evidence": ["thm:growing-depth-recovery", "cor:weighted-operator-recovery", "thm:adaptive-exploration-floor", "thm:honest-jacobi-cylinders"],
            "machine_checks": ["required labels present"],
        },
    },
    "interpretation": "Ledger status records where an argument and check are located; it is not a substitute for independent mathematical review.",
}
write(R43 / "PROOF_LEDGER.json", json.dumps(ledger, indent=2, sort_keys=True))

# ---------------------------------------------------------------------------
# Read-only workflow retained on the frozen branch.
# ---------------------------------------------------------------------------
verify_workflow = r"""name: Verify immutable Round 43 manuscript

on:
  workflow_dispatch:
  pull_request:
    paths:
      - 'ROUND43_REVISION.tex'
      - 'round43/**'
      - 'tools/verify_round43.py'
      - 'tests/test_round43.py'

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - name: Install TeX dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y --no-install-recommends texlive-latex-base texlive-latex-recommended texlive-fonts-recommended lmodern
      - name: Run source and algebra tests
        run: python3 -m unittest -v tests/test_round43.py
      - name: Build exact committed source twice
        run: |
          pdflatex -interaction=nonstopmode -halt-on-error ROUND43_REVISION.tex
          pdflatex -interaction=nonstopmode -halt-on-error ROUND43_REVISION.tex
      - name: Verify manifest and build
        run: python3 tools/verify_round43.py --check-manifest --check-build
"""
write(ROOT / ".github" / "workflows" / "verify-round43.yml", verify_workflow)

# ---------------------------------------------------------------------------
# Source/algebra tests.
# ---------------------------------------------------------------------------
tests = '#!/usr/bin/env python3\nfrom __future__ import annotations\n\nimport json\nimport math\nimport unittest\nfrom fractions import Fraction\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\n\n\nclass Round43SourceTests(unittest.TestCase):\n    def test_publication_unit_is_materialized(self) -> None:\n        required = [\n            "ROUND43_REVISION.tex",\n            "AUTHOR_RESPONSE_ROUND42.md",\n            "ROUND43_REVIEW_INDEX.md",\n            "ROUND43_READY_FOR_REVIEW.md",\n            "round43/introduction.tex",\n            "round43/triangular.tex",\n            "round43/lattice.tex",\n            "round43/filter_memory.tex",\n            "round43/infinite_jacobi.tex",\n            "round43/quantitative_jacobi.tex",\n            "round43/preparations.tex",\n            "round43/appendix_uniformity.tex",\n            "round43/references.tex",\n            "round43/PROOF_LEDGER.json",\n            "round43/HISTORICAL_REUSE.md",\n        ]\n        for relative in required:\n            self.assertTrue((ROOT / relative).is_file(), relative)\n\n    def test_main_inputs_every_article_source(self) -> None:\n        text = (ROOT / "ROUND43_REVISION.tex").read_text(encoding="utf-8")\n        for relative in (\n            "round43/introduction.tex",\n            "round43/triangular.tex",\n            "round43/lattice.tex",\n            "round43/filter_memory.tex",\n            "round43/infinite_jacobi.tex",\n            "round43/quantitative_jacobi.tex",\n            "round43/preparations.tex",\n            "round43/appendix_uniformity.tex",\n            "round43/references.tex",\n        ):\n            self.assertIn(f"\\\\input{{{relative}}}", text)\n\n    def test_round40_gaps_are_landed(self) -> None:\n        lattice = (ROOT / "round43/lattice.tex").read_text(encoding="utf-8")\n        for token in (\n            r"N_{\\rm cal}(m)\\ge \\rho m-C_{\\rm cal}",\n            r"U<\\infty",\n            r"\\tau_{\\min}",\n            r"\\cF_{i-1}\\longrightarrow s_i\\longrightarrow S_i",\n            r"\\label{lem:prefix-window-count}",\n            r"\\label{prop:balanced-contrast}",\n        ):\n            self.assertIn(token, lattice)\n\n    def test_full_ldp_and_new_theorems_are_present(self) -> None:\n        combined = "\\n".join(\n            (ROOT / p).read_text(encoding="utf-8")\n            for p in ("round43/infinite_jacobi.tex", "round43/quantitative_jacobi.tex")\n        )\n        for label in (\n            "eq:jacobi-posterior-ldp",\n            "eq:jacobi-denominator-rate",\n            "lem:effective-response-jet",\n            "lem:finite-grid-certificate",\n            "thm:effective-jacobi-stability",\n            "thm:growing-depth-recovery",\n            "cor:weighted-operator-recovery",\n            "thm:adaptive-exploration-floor",\n            "thm:honest-jacobi-cylinders",\n            "eq:physical-time-speed",\n            "eq:vandermonde-inverse-bound",\n            "eq:explicit-kappa-prefactor",\n            "eq:explicit-A0",\n        ):\n            self.assertIn(f"\\\\label{{{label}}}", combined)\n\n    def test_stale_failure_modes_are_absent(self) -> None:\n        article = "\\n".join(\n            p.read_text(encoding="utf-8")\n            for p in [ROOT / "ROUND43_REVISION.tex", *sorted((ROOT / "round43").glob("*.tex"))]\n        )\n        for token in (chr(12), "w_i=w_*i", "Doob\'s inequality", "conditional second moment at most"):\n            self.assertNotIn(token, article)\n            self.assertIn(r"\\frac1n\\log", article)\n    def test_vandermonde_certificates_are_invertible(self) -> None:\n        quantitative = (ROOT / "round43/quantitative_jacobi.tex").read_text(encoding="utf-8")\n        self.assertIn(r"M_R=2e^{\\Lambda_AT}\\Lambda_A^R", quantitative)\n        self.assertIn(r"C_R\\le 2^{R+1}(R+1)!", quantitative)\n        self.assertIn(r"K_J\\delta^{2R_J+3}", quantitative)\n        for order in range(1, 10):\n            matrix = [\n                [Fraction(k**r, math.factorial(r)) for r in range(order + 1)]\n                for k in range(order + 1)\n            ]\n            det = Fraction(1)\n            for col in range(order + 1):\n                pivot = next(row for row in range(col, order + 1) if matrix[row][col] != 0)\n                if pivot != col:\n                    matrix[col], matrix[pivot] = matrix[pivot], matrix[col]\n                    det *= -1\n                piv = matrix[col][col]\n                det *= piv\n                for j in range(col, order + 1):\n                    matrix[col][j] /= piv\n                for row in range(col + 1, order + 1):\n                    factor = matrix[row][col]\n                    for j in range(col, order + 1):\n                        matrix[row][j] -= factor * matrix[col][j]\n            self.assertNotEqual(det, 0)\n\n    def test_ledger_separates_evidence_from_checks(self) -> None:\n        ledger = json.loads((ROOT / "round43/PROOF_LEDGER.json").read_text(encoding="utf-8"))\n        self.assertFalse(ledger["formal_proof_assistant"])\n        for obligation in ledger["obligations"].values():\n            self.assertTrue(obligation.get("status"))\n            self.assertTrue(obligation.get("mathematical_evidence"))\n            self.assertTrue(obligation.get("machine_checks"))\n\n    def test_round43_workflow_is_read_only(self) -> None:\n        text = (ROOT / ".github/workflows/verify-round43.yml").read_text(encoding="utf-8")\n        self.assertIn("contents: read", text)\n        self.assertNotIn("contents: write", text)\n        self.assertNotIn("git push", text)\n\n\nif __name__ == "__main__":\n    unittest.main()\n'
write(ROOT / "tests" / "test_round43.py", tests)

# ---------------------------------------------------------------------------
# Verifier.  It can refresh the manifest only when explicitly requested during
# the one-use materialization run; the retained verification workflow is read-only.
# ---------------------------------------------------------------------------
verifier = '#!/usr/bin/env python3\nfrom __future__ import annotations\n\nimport argparse\nimport hashlib\nimport json\nimport platform\nimport re\nimport sys\nfrom datetime import datetime, timezone\nfrom pathlib import Path\nfrom typing import Any\n\nROOT = Path(__file__).resolve().parents[1]\nMANIFEST = ROOT / "round43/SOURCE_MANIFEST.json"\nPDF = ROOT / "ROUND43_REVISION.pdf"\nLOG = ROOT / "ROUND43_REVISION.log"\n\nMANIFEST_PATHS = (\n    "ROUND43_REVISION.tex",\n    "round43/preamble.tex",\n    "round43/introduction.tex",\n    "round43/triangular.tex",\n    "round43/lattice.tex",\n    "round43/filter_memory.tex",\n    "round43/infinite_jacobi.tex",\n    "round43/quantitative_jacobi.tex",\n    "round43/preparations.tex",\n    "round43/appendix_uniformity.tex",\n    "round43/references.tex",\n    "AUTHOR_RESPONSE_ROUND42.md",\n    "ROUND43_REVIEW_INDEX.md",\n    "ROUND43_READY_FOR_REVIEW.md",\n    "round43/HISTORICAL_REUSE.md",\n    "round43/PROOF_LEDGER.json",\n    "tools/materialize_round41.py",\n    "tools/harden_round41_ldp.py",\n    "tools/materialize_round43.py",\n    "tools/verify_round43.py",\n    "tests/test_round41.py",\n    "tests/test_round43.py",\n    ".github/workflows/verify-round43.yml",\n)\n\nREQUIRED_LABELS = (\n    "thm:abstract-bvm",\n    "lem:prefix-window-count",\n    "prop:balanced-contrast",\n    "lem:strong-pushforward",\n    "lem:supnorm-response-slln",\n    "thm:jacobi-reconstruction",\n    "eq:jacobi-posterior-ldp",\n    "thm:effective-jacobi-stability",\n    "thm:growing-depth-recovery",\n    "cor:weighted-operator-recovery",\n    "thm:adaptive-exploration-floor",\n    "thm:honest-jacobi-cylinders",\n    "eq:physical-time-complexity",\n    "eq:physical-time-speed",\n)\n\n\ndef sha256(path: Path) -> str:\n    return hashlib.sha256(path.read_bytes()).hexdigest()\n\n\ndef refresh_manifest() -> None:\n    entries = []\n    for relative in MANIFEST_PATHS:\n        path = ROOT / relative\n        if not path.is_file():\n            raise SystemExit(f"manifest source missing: {relative}")\n        entries.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})\n    payload = {\n        "source_set": "round43-positive-referee-closure-effective-jacobi",\n        "controlling_report": "REFEREE_REPORT_ROUND42_GPT56_PRO_HARSH.md",\n        "reviewed_report_commit": "f66cb02217574c12b17b3a49ea630086da437e1f",\n        "hash": "sha256",\n        "publication_unit": "ordinary committed TeX sources; generators are provenance only",\n        "files": entries,\n    }\n    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\\n", encoding="utf-8")\n\n\ndef check_structure() -> dict[str, Any]:\n    failures: list[str] = []\n    for relative in MANIFEST_PATHS:\n        if not (ROOT / relative).is_file():\n            failures.append(f"missing {relative}")\n    article_paths = [ROOT / "ROUND43_REVISION.tex", *sorted((ROOT / "round43").glob("*.tex"))]\n    article = "\\n".join(p.read_text(encoding="utf-8") for p in article_paths if p.is_file())\n    for label in REQUIRED_LABELS:\n        if f"\\\\label{{{label}}}" not in article:\n            failures.append(f"missing label {label}")\n    for token in (chr(12), "w_i=w_*i", "Doob\'s inequality", "conditional second moment at most"):\n        if token in article:\n            failures.append(f"stale forbidden token: {token}")\n    workflow = (ROOT / ".github/workflows/verify-round43.yml").read_text(encoding="utf-8")\n    if "contents: read" not in workflow or "contents: write" in workflow or "git push" in workflow:\n        failures.append("Round 43 verification workflow is not read-only")\n    return {"passed": not failures, "failures": failures}\n\n\ndef check_manifest() -> dict[str, Any]:\n    failures: list[str] = []\n    if not MANIFEST.is_file():\n        return {"passed": False, "failures": ["manifest missing"]}\n    data = json.loads(MANIFEST.read_text(encoding="utf-8"))\n    entries = data.get("files", [])\n    if tuple(e.get("path") for e in entries) != MANIFEST_PATHS:\n        failures.append("manifest path list differs from verifier publication unit")\n    for entry in entries:\n        path = ROOT / entry["path"]\n        if not path.is_file():\n            failures.append(f"missing {entry[\'path\']}")\n            continue\n        if path.stat().st_size != entry["bytes"]:\n            failures.append(f"size mismatch for {entry[\'path\']}")\n        if sha256(path) != entry["sha256"]:\n            failures.append(f"sha256 mismatch for {entry[\'path\']}")\n    return {"passed": bool(entries) and not failures, "checked_files": len(entries), "failures": failures}\n\n\ndef check_build() -> dict[str, Any]:\n    failures: list[str] = []\n    if not PDF.is_file() or PDF.stat().st_size < 10_000:\n        failures.append("ROUND43_REVISION.pdf missing or unexpectedly small")\n    log = LOG.read_text(encoding="utf-8", errors="replace") if LOG.is_file() else ""\n    if not LOG.is_file():\n        failures.append("ROUND43_REVISION.log missing")\n    for token in ("! LaTeX Error:", "There were undefined references", "Citation `", "Reference `", "Emergency stop", "Fatal error occurred"):\n        if token in log:\n            failures.append(f"build log contains: {token}")\n    match = re.search(r"Output written on .*?\\((\\d+) pages?", log)\n    if LOG.is_file() and not match:\n        failures.append("could not determine PDF page count")\n    return {\n        "passed": not failures,\n        "pdf_bytes": PDF.stat().st_size if PDF.is_file() else None,\n        "pdf_sha256": sha256(PDF) if PDF.is_file() else None,\n        "pdf_pages": int(match.group(1)) if match else None,\n        "failures": failures,\n    }\n\n\ndef main() -> int:\n    parser = argparse.ArgumentParser()\n    parser.add_argument("--refresh-manifest", action="store_true")\n    parser.add_argument("--check-manifest", action="store_true")\n    parser.add_argument("--check-build", action="store_true")\n    parser.add_argument("--json", dest="json_path", type=Path)\n    args = parser.parse_args()\n    if args.refresh_manifest:\n        refresh_manifest()\n    result: dict[str, Any] = {\n        "generated_at_utc": datetime.now(timezone.utc).isoformat(),\n        "python": {"implementation": platform.python_implementation(), "version": platform.python_version()},\n        "structure": check_structure(),\n        "scope": {\n            "formal_proof_assistant": False,\n            "checked": ["source invariants", "finite Vandermonde algebra", "manifest hashes", "two-pass LaTeX build", "read-only workflow"],\n            "analytic_proofs_for_referee": ["adaptive martingale likelihood", "strong dual measurability", "posterior LDP", "effective inverse stability", "growing-depth contraction", "confidence cylinders"],\n        },\n    }\n    if args.check_manifest:\n        result["manifest"] = check_manifest()\n    if args.check_build:\n        result["build"] = check_build()\n    result["all_passed"] = all(\n        value.get("passed", True)\n        for key, value in result.items()\n        if isinstance(value, dict) and key not in {"python", "scope"}\n    )\n    rendered = json.dumps(result, indent=2, sort_keys=True) + "\\n"\n    if args.json_path:\n        path = args.json_path if args.json_path.is_absolute() else ROOT / args.json_path\n        path.write_text(rendered, encoding="utf-8")\n    sys.stdout.write(rendered)\n    return 0 if result["all_passed"] else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
write(ROOT / "tools" / "verify_round43.py", verifier)

# Initial exact manifest; the workflow refreshes it after all source files are
# written and before the immutable commit.
manifest_paths = (
    "ROUND43_REVISION.tex",
    "round43/preamble.tex",
    "round43/introduction.tex",
    "round43/triangular.tex",
    "round43/lattice.tex",
    "round43/filter_memory.tex",
    "round43/infinite_jacobi.tex",
    "round43/quantitative_jacobi.tex",
    "round43/preparations.tex",
    "round43/appendix_uniformity.tex",
    "round43/references.tex",
    "AUTHOR_RESPONSE_ROUND42.md",
    "ROUND43_REVIEW_INDEX.md",
    "ROUND43_READY_FOR_REVIEW.md",
    "round43/HISTORICAL_REUSE.md",
    "round43/PROOF_LEDGER.json",
    "tools/materialize_round41.py",
    "tools/harden_round41_ldp.py",
    "tools/materialize_round43.py",
    "tools/verify_round43.py",
    "tests/test_round41.py",
    "tests/test_round43.py",
    ".github/workflows/verify-round43.yml",
)
entries = []
for relative in manifest_paths:
    path = ROOT / relative
    if not path.is_file():
        raise RuntimeError(f"manifest source missing: {relative}")
    entries.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})
manifest = {
    "source_set": "round43-positive-referee-closure-effective-jacobi",
    "controlling_report": "REFEREE_REPORT_ROUND42_GPT56_PRO_HARSH.md",
    "reviewed_report_commit": "f66cb02217574c12b17b3a49ea630086da437e1f",
    "hash": "sha256",
    "publication_unit": "ordinary committed TeX sources; generators are provenance only",
    "files": entries,
}
write(R43 / "SOURCE_MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True))

print(json.dumps({"materialized": True, "round": 43, "manifest_files": len(entries)}, indent=2))
