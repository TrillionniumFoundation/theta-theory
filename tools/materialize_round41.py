#!/usr/bin/env python3
"""Materialize the Round 41 positive revision from the frozen Round 39 source.

The script is intentionally deterministic: it copies the reviewed source set,
replaces the exact proof blocks implicated by the Round 40 report, adds the
quantitative Jacobi response-rate theorem, and writes reviewer-facing ledgers,
tests, and a source manifest.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R39 = ROOT / "round39"
R41 = ROOT / "round41"


def replace_once(text: str, old: str, new: str, name: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{name}: expected one replacement target, found {count}")
    return text.replace(old, new, 1)


def replace_between(text: str, start: str, end: str, new: str, name: str) -> str:
    i = text.find(start)
    if i < 0:
        raise RuntimeError(f"{name}: start marker not found: {start!r}")
    j = text.find(end, i + len(start))
    if j < 0:
        raise RuntimeError(f"{name}: end marker not found: {end!r}")
    return text[:i] + new + text[j + len(end):]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if not R39.is_dir():
    raise SystemExit("round39 source directory is missing")
if R41.exists():
    shutil.rmtree(R41)
shutil.copytree(R39, R41)
for obsolete in ("SOURCE_MANIFEST.json", "PROOF_LEDGER.json", "HISTORICAL_REUSE.md", "preparations_verification.tex"):
    target = R41 / obsolete
    if target.exists():
        target.unlink()

# ---------------------------------------------------------------------------
# Abstract triangular theorem: disambiguate the deterministic transient
# envelope.  This is the source-level clarification that the dormant Round 39
# finalizer intended but never landed on the reviewed head.
# ---------------------------------------------------------------------------
tri_path = R41 / "triangular.tex"
tri = tri_path.read_text(encoding="utf-8")
tri = replace_once(
    tri,
    r"""The true transient cross term is at most
\(B\sum_i d_i\abs{\theta-\theta_0}\), and""",
    r"""Because \(\abs{d_i(\theta)}\le B\abs{\theta-\theta_0}\), the true
transient cross term is at most
\(B(\sum_{i\ge1}d_i)\abs{\theta-\theta_0}\), where the \(d_i\)'s inside
the summation are the deterministic transient envelope from
Assumption~\ref{ass:triangular}, not the mean increment \(d_i(\theta)\).  Also,""",
    "triangular transient notation",
)
write(tri_path, tri)

# ---------------------------------------------------------------------------
# Five-parameter experiment: commit the common policy class, its chronology,
# exact finite-prefix window arithmetic, and a complete empirical-contrast
# proof with constants independent of horizon-dependent policies.
# ---------------------------------------------------------------------------
lat_path = R41 / "lattice.tex"
lat = lat_path.read_text(encoding="utf-8")
policy_start = r"""Fix a bounded force amplitude \(a>0\) and a calibration density
\(\rho\in(0,1]\)."""
policy_end = "The state is never reset."
policy_new = r"""Fix a calibration amplitude \(a>0\), an exploitation-force bound
\(U<\infty\), exploitation-duration bounds
\(0<\tau_{\min}\le\tau_{\max}<\infty\), a calibration density
\(\rho\in(0,1]\), and a prefix defect \(C_{\rm cal}<\infty\).  These
constants are common to the entire triangular class, including policies that
depend on the terminal size \(n\).  Exploitation blocks may use arbitrary
feedback forces bounded in absolute value by \(U\), and their durations lie
in \([\tau_{\min},\tau_{\max}]\).  All policy randomizers and the complete
action of a block are selected before its readout noise.

Let \(N_{\rm cal}(m)\) be the number of calibration slots among the first
\(m\) blocks.  The admissible policy class is defined by the finite-prefix
condition
\begin{equation}
 N_{\rm cal}(m)\ge \rho m-C_{\rm cal}
 \qquad(1\le m\le n),
 \label{eq:prefix-calibration}
\end{equation}
not merely by a terminal or asymptotic density.  Calibration slots, in their
own chronological order, are partitioned into consecutive windows of six.
At a calibration slot \(i\), the duration \(s_i\) is
\(\cF_{i-1}\)-measurable and is selected from the durations not yet used in
the current window; the six realized durations are therefore a permutation of
\(\{\tau,2\tau,\ldots,6\tau\}\).  Only after \(s_i\) is fixed is an
independent Rademacher sign \(S_i\) drawn.  Force \(aS_i\) is then held for
\(s_i\), and finally an independent \(N(0,\sigma^2)\) readout noise is drawn.
Thus the calibration chronology is
\[
 \cF_{i-1}\longrightarrow s_i\longrightarrow S_i
 \longrightarrow\xi_i\longrightarrow Y_i.
\]
The class is nonempty: a deterministic Beatty-type calibration schedule has
\(N_{\rm cal}(m)=\lfloor\rho m\rfloor\), and the six durations may be cycled
in any predictable order.

\begin{lemma}[Complete windows in every finite prefix]
\label{lem:prefix-window-count}
Let \(W_n\) be the number of complete six-slot calibration windows contained
in the first \(n\) blocks.  Then, pathwise and uniformly over the policy
class,
\begin{equation}
 W_n=\left\lfloor\frac{N_{\rm cal}(n)}6\right\rfloor
 \ge \frac{\rho n}{6}-C_{\rm win},
 \qquad C_{\rm win}=\frac{C_{\rm cal}}6+1.
 \label{eq:complete-window-count}
\end{equation}
The sole loss from the unfinished terminal window is the additive constant in
\eqref{eq:complete-window-count}.
\end{lemma}

\begin{proof}
Use \eqref{eq:prefix-calibration} at \(m=n\) and
\(\lfloor x\rfloor\ge x-1\).  The window partition is chronological, so
exactly \(\lfloor N_{\rm cal}(n)/6\rfloor\) windows are complete.
\end{proof}

The state is never reset."""
lat = replace_between(lat, policy_start, policy_end, policy_new, "lattice policy class")
lat = replace_once(
    lat,
    r"""where \(D_{i,s_i}\) is measurable before \(S_i\) is drawn.  Therefore
\begin{equation}
 \E\left[(m_i^\vartheta-m_i^{\vartheta_0})^2
 \mid\cF_{i-1},s_i\right]
 =D_{i,s_i}^2+a^2\{h_\vartheta(s_i)-h_{\vartheta_0}(s_i)\}^2.
 \label{eq:sign-square}
\end{equation}""",
    r"""where \(D_{i,s_i}\) is \(\cF_{i-1}\)-measurable because the duration
was fixed before the fresh sign.  Therefore
\begin{equation}
 \E\left[(m_i^\vartheta-m_i^{\vartheta_0})^2
 \mid\cF_{i-1}\right]
 =D_{i,s_i}^2+a^2\{h_\vartheta(s_i)-h_{\vartheta_0}(s_i)\}^2.
 \label{eq:sign-square}
\end{equation}""",
    "lattice sign chronology",
)
prop_start = r"\begin{proposition}[Full-index empirical contrast]"
prop_end = r"\subsection{The five-parameter quasi-posterior theorem}"
prop_new = r"""\begin{proposition}[Full-index empirical contrast]
\label{prop:balanced-contrast}
Put
\[
 \bar c_\tau=\frac{\rho a^2b_\tau^2}{6}.
\]
For every fixed \(c_*\in(0,\bar c_\tau)\) there are
\(C_1,C_2>0\), independent of the policy, true parameter, true initial state,
and sample size, such that
\begin{equation}
 P_E\left\{
 \inf_{\vartheta\ne\vartheta_0}
 \frac{n^{-1}\sum_{i=1}^n
 (m_i^\vartheta-m_i^{\vartheta_0})^2}
      {\abs{\vartheta-\vartheta_0}^2}<c_*
 \right\}\le C_1e^{-C_2n}.
 \label{eq:full-empirical-contrast}
\end{equation}
On the same event,
\[
 \frac1n\sum_{i=1}^n
 \{v^TDm_i^{\vartheta_0}\}^2\ge c_*\abs v^2
 \quad\hbox{for all }v\in\R^5.
\]
The predictable contrast before martingale fluctuation is
\(\bar c_\tau n-O(1)\), with the explicit incomplete-window loss
\(a^2b_\tau^2C_{\rm win}\).
\end{proposition}

\begin{proof}
The compact radial index set is
\[
 \mathscr K=\{(\theta_0,r,v):\theta_0\in\Theta,\ v\in S^4,\ r\ge0,
 \ \theta_0+rv\in\Theta\}.
\]
At \(r=0\), define
\[
 q_i(\theta_0,0,v)=v^TDm_i^{\theta_0};
\]
for \(r>0\), set
\[
 q_i(\theta_0,r,v)=
 \frac{m_i^{\theta_0+rv}-m_i^{\theta_0}}r
 =\int_0^1v^TDm_i^{\theta_0+srv}\,ds.
\]
Let \(\bar U=\max(a,U)\).  Uniform exponential stability and Duhamel
iteration show that every fixed-order parameter derivative of the forced
trajectory is bounded by a deterministic constant depending only on
\(\bar U,\tau_{\max},\tau\) and the parameter box, not on the number or
ordering of blocks.  Hence \(q_i^2\) is uniformly bounded and uniformly
Lipschitz on \(\mathscr K\), simultaneously in \(i,n\) and the policy.
The continuous definition at \(r=0\) makes the true parameter and tangent
boundary part of the same compact net.

For each \(\kappa\in\mathscr K\), put
\[
 X_i(\kappa)=q_i(\kappa)^2-
 \E\{q_i(\kappa)^2\mid\cF_{i-1}\}.
\]
Because the current action is chosen before the readout and \(q_i\) is a
function of the action record, \((X_i(\kappa),\cF_i)\) is a bounded
martingale-difference sequence.  At every complete calibration window,
\eqref{eq:sign-square} and Theorem~\ref{thm:jet-embedding}, divided by
\(r^2\) and continuously extended to \(r=0\), give
\[
 \sum_{i\in W}\E\{q_i(\kappa)^2\mid\cF_{i-1}\}
 \ge a^2b_\tau^2.
\]
Lemma~\ref{lem:prefix-window-count} therefore yields, uniformly in
\(\kappa\),
\begin{equation}
 \sum_{i=1}^n\E\{q_i(\kappa)^2\mid\cF_{i-1}\}
 \ge \bar c_\tau n-a^2b_\tau^2C_{\rm win}.
 \label{eq:predictable-prefix-contrast}
\end{equation}
Noncalibration blocks contribute nonnegative conditional squares.

Let \(Q\) bound \(\abs{q_i}\), and let \(L_X\) be a common Lipschitz
constant for \(X_i\); conditional expectation is a contraction in supremum
norm, so \(L_X\) is deterministic.  Fix \(c_*<\bar c_\tau\), choose
\(\eta>0\) and a mesh \(\delta>0\) so that
\(\eta+L_X\delta<(\bar c_\tau-c_*)/2\), and take a finite
\(\delta\)-net of \(\mathscr K\).  At each net point, Azuma--Hoeffding gives
\[
 P_E\left\{\sum_{i=1}^nX_i<-\eta n\right\}
 \le \exp\{-\eta^2n/(8Q^4)\}.
\]
A union bound over the fixed net and Lipschitz interpolation give, outside an
event \(C'_1e^{-C'_2n}\),
\[
 \inf_{\kappa\in\mathscr K}\frac1n\sum_{i=1}^nX_i(\kappa)
 \ge-\eta-L_X\delta.
\]
Combining this with \eqref{eq:predictable-prefix-contrast} proves the desired
lower bound for all sufficiently large \(n\).  Enlarging \(C_1\) absorbs the
finitely many smaller sizes.  Substitution of
\(r=\abs{\vartheta-\vartheta_0}\) proves
\eqref{eq:full-empirical-contrast}; \(r=0\) gives the simultaneous tangent
information inequality.
\end{proof}

\subsection{The five-parameter quasi-posterior theorem}"""
lat = replace_between(lat, prop_start, prop_end, prop_new, "balanced contrast proposition")
lat = replace_once(
    lat,
    r"""Every duration is bounded below by \(\tau\), so
Lemma~\ref{lem:five-energy} gives
\[
 \sup_{\vartheta,\norm z\le R}
 \abs{\partial_\vartheta^\alpha b_i^\vartheta(z)}
 \le C_re^{-\lambda_ri\tau}.
\]""",
    r"""Every block duration is bounded below by
\(\underline\tau=\min(\tau,\tau_{\min})>0\), hence the physical endpoint
time satisfies \(t_i\ge i\underline\tau\).  Lemma~\ref{lem:five-energy}
therefore gives
\[
 \sup_{\vartheta,\norm z\le R}
 \abs{\partial_\vartheta^\alpha b_i^\vartheta(z)}
 \le C_re^{-\lambda_ri\underline\tau}.
\]""",
    "lattice block time",
)
lat = replace_once(
    lat,
    r"""A positive asymptotic density of calibration blocks remains necessary for a
uniform root-\(n\) statement over arbitrary exploitation policies.  The
stronger per-block condition that every diagnostic atom have fixed positive
conditional mass has been removed.  The order of durations inside each
window may be selected adaptively, while the fresh sign is the randomizer that
prevents cancellation by the existing state.""",
    r"""The finite-prefix lower bound \eqref{eq:prefix-calibration}, rather than a
bare terminal liminf, is the exact uniformity condition needed when policies
may depend on \(n\).  It still avoids the stronger requirement that every
duration--sign atom have positive conditional mass at every block.  The order
inside each complete window may be selected adaptively; the fresh sign is the
randomizer that prevents cancellation by the existing state.""",
    "lattice policy remark",
)
write(lat_path, lat)

# ---------------------------------------------------------------------------
# Strong filter jets: deterministic separable target spaces and explicit
# polynomial dependence on total-variation derivative norms.
# ---------------------------------------------------------------------------
fil_path = R41 / "filter_memory.tex"
fil = fil_path.read_text(encoding="utf-8")
sub_start = r"\subsection{The Banach spaces and strong derivatives}"
sub_end = r"\begin{theorem}[Time-uniform strong filter jets]"
sub_new = r"""\subsection{The Banach spaces, deterministic jet range, and strong derivatives}

For an integer \(r\ge0\), let \(C_b^r(\Hh)\) be the Banach space of bounded
functions with bounded continuous Fr\'echet derivatives through order \(r\),
with norm
\[
 \norm\phi_{C_b^r}
 =\max_{0\le j\le r}
 \sup_{x\in\Hh}\norm{D^j\phi(x)}_{\operatorname{Sym}^j(\Hh)^*}.
\]
For \(j\ge0\), write \(\mathbb E_j=(C_b^{j+1}(\Hh))'\).  If
\(0\le\ell\le j\), \(x\in\Hh\), and
\(v_1,\ldots,v_\ell\in\Hh\), define the jet evaluation
\[
 \mathcal J_{\ell}(x;v_1,\ldots,v_\ell)(\phi)
 =D^\ell\phi(x)[v_1,\ldots,v_\ell].
\]
Let \(\mathbb E_j^0\) be the closed linear span in \(\mathbb E_j\) of all
such evaluations.  Since \(\Hh\) is separable and
\[
 \norm{\mathcal J_\ell(x;\mathbf v)-
       \mathcal J_\ell(y;\mathbf v)}_{\mathbb E_j}
 \le \norm{x-y}\prod_{k=1}^\ell\norm{v_k},
 \qquad \ell\le j,
\]
together with the analogous multilinear bounds in the \(v_k\)'s,
\(\mathbb E_j^0\) is a deterministic separable Banach subspace.  It does not
depend on the data, policy, prior, or sample size.

Parameter derivative tensors use the operator norm on
\(\operatorname{Sym}^j(\R^5;\mathbb E_j)\).  For a \(C^r\) curve
\(y_\vartheta\in\Hh\), the notation
\(\partial_\vartheta^j\delta_{y_\vartheta}\) denotes its strong derivative
in \(\mathbb E_j\).

\begin{lemma}[Concentrated push-forward jets with a deterministic range]
\label{lem:strong-pushforward}
Let \(U\subset\R^d\) be compact, let \(\nu\) be a Borel probability on the
radius-\(R\) ball of the separable Hilbert space \(\Hh\), and write
\(\mu_\theta(dz)=p_\theta(z)\nu(dz)\).  Assume
\(\theta\mapsto p_\theta\) is \(C^r\) in \(L^1(\nu)\),
\(p_\theta\ge0\), and \(\int p_\theta d\nu=1\).  Suppose
\(x_\theta\in\Hh\) and \(S_\theta\in\mathcal L(\Hh)\) are
\(C^{r+1}\), and set
\begin{align*}
 K&=1+\max_{\abs\alpha\le r+1}\sup_{\theta\in U}
       \norm{\partial_\theta^\alpha x_\theta},\\
 M_r&=1+\max_{\abs\alpha\le r}\sup_{\theta\in U}
       \norm{\partial_\theta^\alpha p_\theta}_{L^1(\nu)}.
\end{align*}
If \(0<\varepsilon\le1\) and
\[
 \max_{\abs\alpha\le r+1}\sup_{\theta\in U}
 \norm{\partial_\theta^\alpha S_\theta}\le\varepsilon,
\]
then \(\theta\mapsto(x_\theta+S_\theta z)_\#\mu_\theta\) is strongly
\(C^r\), and for \(0\le j\le r\),
\begin{equation}
 \sup_{\theta\in U}
 \norm{\partial_\theta^j[(x_\theta+S_\theta z)_\#\mu_\theta]
       -\partial_\theta^j\delta_{x_\theta}}_{\mathbb E_j}
 \le C_r(1+R)^{r+1}K^{r+1}M_r\varepsilon.
 \label{eq:strong-pushforward-bound}
\end{equation}
Every derivative on the left belongs to the deterministic separable space
\(\mathbb E_j^0\).

If \(x,S,p\) additionally depend on a random element and all displayed
parameter derivatives are jointly measurable, then the derivative-valued
maps are strongly measurable into \(\mathbb E_j^0\), and the supremum in
\eqref{eq:strong-pushforward-bound} is a measurable real random variable.
\end{lemma}

\begin{proof}
For \(\norm\phi_{C_b^{r+1}}\le1\), put
\[
 g_\theta(z)=\phi(x_\theta+S_\theta z)-\phi(x_\theta)
 =\int_0^1D\phi(x_\theta+tS_\theta z)[S_\theta z]dt.
\]
Differentiate at most \(r\) times in \(\theta\).  Every term still contains
one factor \(S_\theta z\) or one parameter derivative of \(S_\theta z\);
all other factors are derivatives of \(x_\theta\), derivatives of \(\phi\)
of order at most \(r+1\), and vectors of norm at most \(R\).  Hence
\[
 \max_{\abs\alpha\le r}\sup_{\theta,z}
 \abs{\partial_\theta^\alpha g_\theta(z)}
 \le C_r(1+R)^{r+1}K^{r+1}\varepsilon.
\]
Leibniz's rule for \(\int g_\theta p_\theta d\nu\) gives
\eqref{eq:strong-pushforward-bound}; the dependence on derivatives of the
weight is explicitly linear in their common \(L^1\) bound \(M_r\).

The order-\(j\) derivative of the push-forward is a finite sum of Bochner
integrals of jet evaluations \(\mathcal J_\ell\), \(\ell\le j\), whose
vector arguments are parameter derivatives of \(x_\theta+S_\theta z\).
The continuity estimates above, dominated convergence, and the
\(L^1(\nu)\) Taylor formula for \(p_\theta\) prove norm differentiability and
show that every term lies in \(\mathbb E_j^0\).  In the random case these
Bochner integrands are jointly measurable with values in the same fixed
separable space, hence their integrals are strongly measurable.  Pathwise
norm continuity in \(\theta\) and a countable dense set \(U_0\subset U\),
chosen once and for all, give
\[
 \sup_{\theta\in U}\norm{F(\theta)}
 =\sup_{\theta\in U_0}\norm{F(\theta)},
\]
which proves measurability of the supremum.
\end{proof}

\begin{theorem}[Time-uniform strong filter jets]"""
fil = replace_between(fil, sub_start, sub_end, sub_new, "filter Banach subsection")
theorem_start = r"\begin{theorem}[Time-uniform strong filter jets]"
theorem_end = r"\begin{corollary}[Finite-rank current-state Gaussian image]"
theorem_new = r"""\begin{theorem}[Time-uniform strong filter jets]
\label{thm:filter-jets}
For each fixed integer \(r\ge0\) and \(q<\infty\), there are
\(C_{r,q},\gamma_{r,q}>0\) such that
\begin{equation}
 \sup_{E\in\frE_n}
 \E_E\left[
 \sup_{\vartheta\in\Theta}
 \norm{\partial_\vartheta^j\Pi_{n,\vartheta}^{\nu_n}
       -\partial_\vartheta^j\delta_{x_n^\vartheta}}_{\mathbb E_j}^q
 \right]
 \le C_{r,q}e^{-\gamma_{r,q}n},
 \qquad 0\le j\le r.
 \label{eq:filter-jet-decay}
\end{equation}
The random derivative fields take values in the deterministic separable
spaces \(\mathbb E_j^0\), so both the norm and the supremum in
\eqref{eq:filter-jet-decay} are measurable.  The assertion holds for
arbitrary Borel \(\nu_n\) supported in the Hilbert ball.  For two such
working priors, the difference of their filter jets is bounded by the sum of
the two right sides.  In particular, with
\(\underline\tau=\min(\tau,\tau_{\min})\),
\[
 W_1(\Pi_{n,\vartheta}^{\nu_n^1},
     \Pi_{n,\vartheta}^{\nu_n^2})
 \le2MRe^{-\lambda n\underline\tau}
\]
holds deterministically for the undifferentiated filters.
\end{theorem}

\begin{proof}
Write
\(w_{n,\vartheta}^{\nu_n}(dz)=p_{n,\vartheta}(z)\nu_n(dz)\).
Lemma~\ref{lem:nuisance-budget} and differentiation of the normalized density
give, for every \(\abs\alpha\le r\),
\[
 \sup_{\vartheta}
 \norm{\partial_\vartheta^\alpha p_{n,\vartheta}}_{L^1(\nu_n)}
 \le C_r(1+W_{n,r,E})^{C_r}.
\]
This is a measurable polynomial bound with moments of every fixed order,
uniformly over \(E\); no density or regularity of \(\nu_n\) is used.
Uniform stability and the common force bound give deterministic bounds on all
fixed-order derivatives of \(x_n^\vartheta\).  Moreover
\[
 \sup_{\vartheta,\abs\alpha\le r+1}
 \norm{\partial_\vartheta^\alpha T_\vartheta(t_n)}
 \le C_re^{-\lambda_rt_n}
 \le C_re^{-\lambda_rn\underline\tau}.
\]
Apply Lemma~\ref{lem:strong-pushforward} pathwise with
\(S_\vartheta=T_\vartheta(t_n)\).  It yields the explicit random bound
\[
 \sup_{\vartheta}
 \norm{\partial_\vartheta^j\Pi_{n,\vartheta}^{\nu_n}
       -\partial_\vartheta^j\delta_{x_n^\vartheta}}_{\mathbb E_j}
 \le C_re^{-\lambda_rn\underline\tau}
       (1+W_{n,r,E})^{C_r}.
\]
Taking the \(q\)-th moment proves \eqref{eq:filter-jet-decay}.  Coupling two
posterior initial states in the radius-\(R\) ball proves the deterministic
Wasserstein estimate.
\end{proof}

\begin{corollary}[Finite-rank current-state Gaussian image]"""
fil = replace_between(fil, theorem_start, theorem_end, theorem_new, "filter theorem")
fil = fil.replace(r"\sqrt nMRe^{-\lambda n\tau}", r"\sqrt nMRe^{-\lambda n\underline\tau}")
write(fil_path, fil)

# ---------------------------------------------------------------------------
# Infinite Jacobi model: declare a genuine compact box, a common feedback
# class, replace the invalid L2-net maximal argument by a sup-norm compact
# response class, and strengthen consistency to an exact closed-set
# exponential posterior upper bound.
# ---------------------------------------------------------------------------
jac_path = R41 / "infinite_jacobi.tex"
jac = jac_path.read_text(encoding="utf-8")
jac = replace_once(
    jac,
    r"""Fix constants \(0<a_-<a_+<\infty\), \(c_->0\), and
\(b_->2a_+\).  Let""",
    r"""Fix constants \(0<c_-<c_+<\infty\), \(0<a_-<a_+<\infty\), and
\(2a_+<b_-<b_+<\infty\).  Let""",
    "Jacobi compact box",
)
experiment_start = r"""Choose a dense sequence \((t_m)_{m\ge1}\) in \((0,T]\) and probabilities
\(\omega_m>0\), \(\sum_m\omega_m=1\).  At stage \(i\), the following
chronological experiment is performed."""
experiment_end = "Let \\(h_\\beta(t)\\) be the response from rest."
experiment_new = r"""Choose a dense sequence \((t_m)_{m\ge1}\) in \((0,T]\) and probabilities
\(\omega_m>0\), \(\sum_m\omega_m=1\).  Fix common feedback bounds
\(U_J<\infty\) and \(T_J<\infty\).  At stage \(i\), the following
chronological experiment is performed.
\begin{enumerate}
\item A parameter-independent feedback segment of duration at most \(T_J\)
may be run, with force bounded in absolute value by \(U_J\).  It may depend on
the terminal sample size and the observed past.
\item Set the force to zero for a washout time \(w_i=w_*i\), where \(w_*>0\).
\item Draw \(M_i\) with law \((\omega_m)\), then draw an independent
Rademacher sign \(S_i\), apply force \(aS_i\) for duration \(t_{M_i}\), and
only then draw the independent \(N(0,\sigma^2)\) readout noise.
\end{enumerate}
The variables \((M_i,S_i,\xi_i)\) are independent across stages and of the
past.  All uniform statements below range over feedback segments satisfying
the same pair \((U_J,T_J)\); thus ``bounded'' always means bounded by declared
common constants.

Let \(h_\beta(t)\) be the response from rest."""
jac = replace_between(jac, experiment_start, experiment_end, experiment_new, "Jacobi experiment")
prior_marker = r"""The exact posterior is
\[
 \Pi_n^{\nu_n}(d\beta)
 =\frac{L_n^{\nu_n}(\beta)\Pi(d\beta)}
        {\int L_n^{\nu_n}(\gamma)\Pi(d\gamma)}.
\]
"""
replacement_start = r"\begin{theorem}[Strong posterior consistency for the infinite Jacobi bath]"
replacement_end = r"\begin{remark}[Genuine infinite-dimensional content]"
new_theorem = r"""\begin{proposition}[Response geometry and coefficient separation]
\label{prop:jacobi-response-geometry}
The quantity \(D^{1/2}\) is a metric on \(\mathfrak B\) that induces the
product topology.  For
\[
 d_J(\beta,\beta_0)=\max\left\{\abs{c-c_0},
 \max_{0\le j\le J}\abs{a_j-a_{0,j}},
 \max_{0\le j\le J}\abs{b_j-b_{0,j}}\right\}
\]
and every \(\delta>0\), the response-information modulus
\begin{equation}
 \kappa_J(\delta)=
 \inf_{\{\beta:d_J(\beta,\beta_0)\ge\delta\}}
 D(\beta,\beta_0)
 \label{eq:jacobi-separation-modulus}
\end{equation}
is strictly positive whenever the constraint set is nonempty; set
\(\kappa_J(\delta)=+\infty\) when it is empty.
\end{proposition}

\begin{proof}
The map
\(\beta\mapsto(h_\beta(t_m))_{m\ge1}\) is continuous from the compact
product space into \(\ell^2(\omega)\), by
Lemma~\ref{lem:product-continuity} and dominated convergence.  It is injective
by analyticity and Theorem~\ref{thm:jacobi-reconstruction}.  A continuous
bijection from a compact space to a Hausdorff space is a homeomorphism onto
its image, proving the first assertion.  The set in
\eqref{eq:jacobi-separation-modulus} is compact and excludes \(\beta_0\), so
continuity and point separation give a positive minimum.
\end{proof}

\begin{theorem}[Jacobi posterior response-rate bound]
\label{thm:jacobi-rate}
For every closed set \(F\subset\mathfrak B\),
\begin{equation}
 \limsup_{n\to\infty}\frac1n
 \log\Pi_n^{\nu_n}(F)
 \le-\frac{a^2}{2\sigma^2}
       \inf_{\beta\in F}D(\beta,\beta_0)
 \quad P_{\beta_0,z_0}\text{-almost surely}.
 \label{eq:jacobi-closed-set-rate}
\end{equation}
The bound holds for every sequence of working initial-state priors supported
in the fixed Hilbert ball.  In particular, for every \(J\) and \(\delta>0\),
\begin{equation}
 \limsup_{n\to\infty}\frac1n
 \log\Pi_n^{\nu_n}\{d_J(\beta,\beta_0)\ge\delta\}
 \le-\frac{a^2\kappa_J(\delta)}{2\sigma^2}<0.
 \label{eq:jacobi-cylinder-rate}
\end{equation}
The corresponding \(\varepsilon\)-relaxed finite-\(n\) inequalities hold in
probability uniformly over the feedback segments with common bounds
\((U_J,T_J)\).
\end{theorem}

\begin{proof}
Put
\(f_\beta(t)=a\{h_\beta(t)-h_{\beta_0}(t)\}\).  By
Lemma~\ref{lem:product-continuity}, the class
\(\mathcal F=\{f_\beta:\beta\in\mathfrak B\}\) is compact in
\(C([0,T])\), and it has a deterministic bound \(B_F\).
Lemma~\ref{lem:supnorm-response-slln} gives, almost surely,
\begin{align}
 \sup_{\beta\in\mathfrak B}
 \left|\frac1n\sum_{i=1}^nS_i\xi_i f_\beta(t_{M_i})\right|&\longrightarrow0,
 \label{eq:uniform-score-slln}\\
 \sup_{\beta\in\mathfrak B}
 \left|\frac1n\sum_{i=1}^nf_\beta(t_{M_i})^2
      -a^2D(\beta,\beta_0)\right|&\longrightarrow0.
 \label{eq:uniform-square-slln}
\end{align}
This is a sup-norm interpolation argument over the entire compact class; no
maximal inequality is applied to an uncountable family.

The true washout residual contributes, uniformly in \(\beta\), at most
\[
 \frac{B_F}{n\sigma^2}\sum_{i=1}^n\abs{\eta_i^{\beta_0}(z_0)}=o(1).
\]
Consequently the ideal log-likelihood ratios satisfy the uniform limit
\begin{equation}
 \sup_{\beta\in\mathfrak B}
 \left|\frac1n\log\frac{L_n^\star(\beta)}{L_n^\star(\beta_0)}
       +\frac{a^2}{2\sigma^2}D(\beta,\beta_0)\right|
 \longrightarrow0
 \quad\text{almost surely}.
 \label{eq:uniform-jacobi-likelihood-limit}
\end{equation}
Lemma~\ref{lem:washout-correction} changes a log ratio by at most
\(2C_n=o(n)\), uniformly in \(\beta\) and \(\nu_n\), so the same limit holds
for the exact integrated likelihood.

Let
\(Z_n=\int L_n^{\nu_n}(\beta)/L_n^{\nu_n}(\beta_0)\,\Pi(d\beta)\).
For every \(\eta>0\), the product-open set
\(B_\eta=\{\beta:D(\beta,\beta_0)<\eta\}\) has positive prior mass.  The
uniform limit gives
\[
 \liminf_{n\to\infty}\frac1n\log Z_n
 \ge-\frac{a^2\eta}{2\sigma^2}.
\]
Letting \(\eta\downarrow0\) shows that the denominator has exponential rate
at least zero.  For a closed \(F\), the numerator is at most its prior mass
times the maximum likelihood ratio on \(F\), and
\eqref{eq:uniform-jacobi-likelihood-limit} gives rate at most
\(-a^2\inf_FD/(2\sigma^2)\).  Subtracting the denominator rate proves
\eqref{eq:jacobi-closed-set-rate}.  Equation
\eqref{eq:jacobi-cylinder-rate} follows from
Proposition~\ref{prop:jacobi-response-geometry}.  All random estimates use the
same deterministic response class and common force/duration bounds; the
finite-\(n\) relaxed uniform-in-probability statement follows from the same
bounds and the uniform washout envelope.
\end{proof}

\begin{corollary}[Strong posterior consistency for the infinite Jacobi bath]
\label{thm:jacobi-consistency}
For every open neighbourhood \(U\) of \(\beta_0\) in the product topology,
\[
 \Pi_n^{\nu_n}(U^c)\longrightarrow0
 \quad P_{\beta_0,z_0}\text{-almost surely}.
\]
\end{corollary}

\begin{proof}
The compact set \(U^c\) excludes \(\beta_0\); hence
\(\inf_{U^c}D>0\) by Proposition~\ref{prop:jacobi-response-geometry}.
Apply Theorem~\ref{thm:jacobi-rate}.
\end{proof}

\begin{remark}[Genuine infinite-dimensional content]"""
jac = replace_between(jac, replacement_start, replacement_end, new_theorem, "Jacobi posterior theorem")
jac = replace_once(
    jac,
    r"""Every product neighbourhood constrains finitely many coefficients, and the
theorem learns every such finite block as the sample grows.  The parameter
space contains an infinite sequence, the response is nonrational, and the
reconstruction iterates without a terminal index.  This is not a two- or
five-parameter regression embedded in a known bath.  It is also not claimed
to be a nonparametric Gaussian limit: the proven infinite-dimensional result
is strong posterior consistency in the natural compact product topology.""",
    r"""Every product neighbourhood constrains finitely many coefficients, and
\eqref{eq:jacobi-cylinder-rate} gives an exponential posterior rate for each
such block through the deterministic inverse-response modulus
\(\kappa_J\).  The parameter space contains an infinite sequence, the
response is nonrational, and the reconstruction iterates without a terminal
index.  Thus the statistical conclusion is stronger than qualitative
consistency while remaining intrinsic to the full infinite chain.""",
    "Jacobi strength remark",
)
write(jac_path, jac)

# ---------------------------------------------------------------------------
# Appendix: exact finite-prefix arithmetic and the corrected compact-class
# strong laws.  The latter uses a C([0,T]) net and the empirical first moment
# of |xi| to control every member of a sup-norm ball at once.
# ---------------------------------------------------------------------------
app_path = R41 / "appendix_uniformity.tex"
app = app_path.read_text(encoding="utf-8")
app_start = r"\subsection{Uniform strong law for the countable-duration experiment}"
app_end = r"\subsection{Analytic continuation from a finite duration interval}"
app_new = r"""\subsection{Uniform strong laws for the compact response class}

The proof below uses the compactness that is actually available in the
Jacobi experiment: the response family is compact in the supremum norm on a
finite time interval.  This avoids applying a fixed-function maximal
inequality to an uncountable class.

\begin{lemma}[Supremum-norm response strong laws]
\label{lem:supnorm-response-slln}
Let \(\mathcal F\) be a compact subset of \(C([0,T])\), and suppose
\(\sup_{f\in\mathcal F}\norm f_\infty\le B\).  Let \(M_i\) be independent
with \(\Prob(M_i=m)=\omega_m\), let \(S_i\) be independent Rademacher
variables, and let \(\xi_i\) be independent centred variables with
\(\E\abs{\xi_i}<\infty\); assume the three sequences are mutually
independent.  Then, almost surely,
\begin{align}
 \sup_{f\in\mathcal F}
 \left|\frac1n\sum_{i=1}^nS_i\xi_i f(t_{M_i})\right|&\longrightarrow0,
 \label{eq:supnorm-score-slln}\\
 \sup_{f\in\mathcal F}
 \left|\frac1n\sum_{i=1}^nf(t_{M_i})^2
       -\sum_{m\ge1}\omega_m f(t_m)^2\right|&\longrightarrow0.
 \label{eq:supnorm-square-slln}
\end{align}
\end{lemma}

\begin{proof}
Fix \(\varepsilon>0\) and choose a finite supremum-norm
\(\varepsilon\)-net \(f^1,\ldots,f^N\) of \(\mathcal F\).  At every net
point the ordinary strong law applies to the integrable centred variables
\(S_i\xi_if^k(t_{M_i})\), and also to the bounded variables
\(f^k(t_{M_i})^2\).  The conclusions hold simultaneously over the finite
net.

For \(f\) in the ball of \(f^k\), the score interpolation error satisfies
\[
 \left|\frac1n\sum_{i=1}^nS_i\xi_i
       \{f(t_{M_i})-f^k(t_{M_i})\}\right|
 \le \varepsilon\frac1n\sum_{i=1}^n\abs{\xi_i}
 \longrightarrow\varepsilon\E\abs{\xi_1}
\]
almost surely.  Thus one empirical first moment controls every member of the
entire supremum-norm ball at once.  For the square field,
\[
 \abs{f(t)^2-f^k(t)^2}\le2B\varepsilon
\]
controls both the empirical average and its \(\omega\)-expectation.  Take the
limsup and then let \(\varepsilon\downarrow0\) along a deterministic
sequence.  This proves both assertions.
\end{proof}

\subsection{Analytic continuation from a finite duration interval}"""
app = replace_between(app, app_start, app_end, app_new, "appendix compact-class SLLN")
write(app_path, app)

# ---------------------------------------------------------------------------
# The introduction is recast around one common response-geometry architecture.
# It states the new closed-set rate and places the work against the relevant
# Bayesian inverse-problem literature without repository governance language.
# ---------------------------------------------------------------------------
intro = r"""
\section{Introduction and statement of contribution}
\label{sec:introduction}

Boundary inference for a damped half-line lattice is governed by one object:
the map from physical coefficients to the boundary step response.  The two
experiments studied here use different parameter spaces, but the same
mathematical architecture.  First one proves that response coordinates
separate the physical models, quantitatively whenever finite-dimensional
geometry permits it.  One then converts that deterministic separation into
statistical contrast under a chronological randomized calibration, while the
unobserved state is controlled by exponential stability rather than by
physical resets.  Finally one normalizes the resulting likelihood in the
appropriate finite- or infinite-dimensional parameter topology.

For a homogeneous bath, the unknown parameter is
\[
 \vartheta=(c,k,\epsilon,c_b,k_b)\in\Theta\Subset(0,\infty)^5.
\]
The entries are boundary damping, boundary pinning, coupling strength, bath
damping, and bath pinning.  Six short forcing durations recover the first
eight time jets of the response.  Five jets form a triangular global
coordinate system for \(\vartheta\), and a generalized Vandermonde transform
turns this jet inversion into a quantitative six-response embedding.  The
statistical design places calibration slots in every finite prefix at a
common positive density, groups them into complete six-duration windows, and
draws a fresh sign only after the duration is predictably fixed.  Arbitrary
feedback exploitation remains available between calibration slots, subject
to common force and duration bounds.  Exact window counting and a compact
radial net then give policy-uniform global contrast and tangent information.

The finite-dimensional likelihood is nonlinear and triangular: the policy
may depend on the terminal sample size, the physical state is never reset,
and the working likelihood integrates an arbitrary sample-size-dependent
probability on a Hilbert ball even when the frequentist initial state is not
in its support.  We prove a random-information quasi-Bernstein--von Mises
theorem in total variation without assuming convergence of the realized
information matrix.  The proof includes a relative unnormalized \(L^1\)
Laplace principle, global localization, and a summable nuisance factor.  The
same stability mechanism yields strong parameter jets of the current-state
filter in deterministic separable subspaces of
\((C_b^{r+1})'\), and propagates the posterior to the complete time-domain
memory kernel.

For the genuinely inhomogeneous bath, the parameter is
\[
 \beta=\bigl(c,(a_j)_{j\ge0},(b_j)_{j\ge0}\bigr)
\]
in a compact coefficient product.  The damped response determines \(c\),
the boundary Weyl function, and then every Jacobi coefficient by an explicit
Schur recursion.  Countably many response values define a metric \(D^{1/2}\)
that is topologically equivalent to the product topology.  Increasing
zero-force washouts make the persistent state a uniformly summable
log-likelihood perturbation.  A new supremum-norm compact-class strong law
then gives the uniform likelihood limit
\[
 \frac1n\log\frac{L_n(\beta)}{L_n(\beta_0)}
 \longrightarrow-\frac{a^2}{2\sigma^2}D(\beta,\beta_0)
\]
uniformly over the complete coefficient product.  Consequently every closed
set satisfies an exact exponential posterior upper bound, and every fixed
finite block of Jacobi coefficients contracts exponentially through a
strictly positive inverse-response modulus.  Qualitative strong consistency
is an immediate corollary of this quantitative statement.

\subsection{Main theorem map}

The proof is organized as one response-geometry pipeline.
\begin{enumerate}
\item Theorem~\ref{thm:abstract-bvm} proves a nonlinear adaptive Gaussian
quasi-Bernstein--von Mises theorem with summably transient Hilbert-state
nuisance and fully uniform triangular quantifiers.
\item Theorem~\ref{thm:jet-embedding} gives the global six-duration embedding
of the five homogeneous coefficients, while
Proposition~\ref{prop:balanced-contrast} converts it into finite-prefix
empirical contrast.
\item Theorem~\ref{thm:lattice-bvm} applies the abstract theorem to the
non-resetting lattice.  Theorem~\ref{thm:filter-jets} and
Corollary~\ref{cor:memory-posterior} propagate the result to current-state
filter jets and the inferred memory kernel.
\item Theorem~\ref{thm:jacobi-reconstruction} reconstructs the complete
unknown Jacobi bath from the boundary response.
\item Proposition~\ref{prop:jacobi-response-geometry} identifies the response
metric with the coefficient product topology, and
Theorem~\ref{thm:jacobi-rate} gives closed-set and finite-cylinder exponential
posterior rates.  Corollary~\ref{thm:jacobi-consistency} gives strong
consistency.
\end{enumerate}

\subsection{Relation to adaptive identification and Bayesian inverse problems}
\label{sec:literature}

Adaptive identification of infinite-dimensional systems has a substantial
history.  Baumeister, Scondo, Demetriou and Rosen~\cite{Baumeister1997} develop
online parameter estimation and persistence of excitation for abstract
infinite-dimensional systems.  Demetriou and Rosen
\cite{DemetriouRosen1994Inverse,DemetriouRosen1994PE} treat second-order
distributed systems, while Chattopadhyay, Sukumar and
Natarajan~\cite{Chattopadhyay2025} recover stable SISO infinite-dimensional
systems from transfer information.  Sharrock and Kantas
\cite{SharrockKantas2022} study online parameter estimation in a partially
observed stochastic evolution equation.  Our conclusions concern instead a
chronological Bayesian likelihood with nonlinear parameter-dependent means,
non-resetting deterministic hidden mechanics, and either a random-information
total-variation limit or a full-sequence Jacobi posterior rate.

Du, Nair and Janson~\cite{DuNairJanson2025} provide the closest comparison on
Bernstein--von Mises limits for adaptively collected data.  The theorem here
allows nonlinear predictable means, verifies global contrast from a physical
response embedding, admits horizon-dependent policies, and retains an exact
integrated initial-state likelihood.  General misspecified Bernstein--von
Mises theory~\cite{KleijnVanDerVaart2012} supplies broader context; here the
misspecification is a single exponentially forgotten initial state, so its
log-likelihood contribution is summable and its pseudo-true displacement is
of order \(n^{-1}\).

For Bayesian inverse problems, Vollmer~\cite{Vollmer2013} derives posterior
consistency by combining deterministic stability of a forward inverse map
with regression consistency.  De Hoop, Kovachki, Nelsen and
Stuart~\cite{deHoopEtAl2023} prove contraction rates for learning linear
operators from noisy random-input data.  The present infinite-Jacobi theorem
shares the principle that response stability must drive posterior
concentration, but its data are chronological scalar boundary experiments,
its forward object is a nonlinear Weyl/Schur response map, and its rate
function is the explicitly sampled response metric \(D\).  The coefficient
moduli \(\kappa_J\) convert that metric rate into quantitative recovery of
every finite Jacobi block.

Inverse spectral recovery of Jacobi matrices is classical; see Gesztesy and
Simon~\cite{GesztesySimon1997}, Teschl~\cite{Teschl2000}, and the dynamic
inverse formulation of Mikhaylov, Mikhaylov and
Simonov~\cite{Mikhaylov2019}.  The Schur recursion itself is used as the
deterministic identification engine.  The statistical contribution is the
uniform noisy likelihood limit, the exact integrated washout correction, and
the resulting posterior rate on the complete compact coefficient product.
"""
write(R41 / "introduction.tex", intro)

# ---------------------------------------------------------------------------
# Keep the finite preparation theorem, but remove build/repository governance
# from the article.  Verification records remain in the reviewer packet.
# ---------------------------------------------------------------------------
old_prep = (R39 / "preparations_verification.tex").read_text(encoding="utf-8")
cut = old_prep.find(r"\section{Reproducibility and the exact scope of computation}")
if cut < 0:
    raise RuntimeError("preparations: verification section marker missing")
prep = old_prep[:cut]
prep = prep.replace("Under one fixed infinite balanced policy", "Under one fixed infinite prefix-balanced policy")
prep = prep.replace("one fixed infinite policy", "one fixed infinite prefix-balanced policy")
write(R41 / "preparations.tex", prep)

# ---------------------------------------------------------------------------
# Bibliography additions requested by the referee's significance discussion.
# ---------------------------------------------------------------------------
ref_path = R41 / "references.tex"
refs = ref_path.read_text(encoding="utf-8")
new_refs = r"""
\bibitem{Vollmer2013}
S.~J.~Vollmer,
\emph{Posterior consistency for Bayesian inverse problems through stability
and regression results},
Inverse Problems \textbf{29} (2013), 125011.
doi:10.1088/0266-5611/29/12/125011.

\bibitem{deHoopEtAl2023}
M.~V.~de Hoop, N.~B.~Kovachki, N.~H.~Nelsen and A.~M.~Stuart,
\emph{Convergence rates for learning linear operators from noisy data},
SIAM/ASA J. Uncertain. Quantif. \textbf{11} (2023), 480--513.
doi:10.1137/21M1442942.

"""
refs = replace_once(refs, r"\end{thebibliography}", new_refs + r"\end{thebibliography}", "references")
write(ref_path, refs)

# ---------------------------------------------------------------------------
# Main manuscript wrapper.
# ---------------------------------------------------------------------------
main = r"""\documentclass[11pt,reqno]{amsart}
\input{round41/preamble.tex}
\title[Adaptive boundary identification]{Adaptive Boundary Identification and Bayesian Asymptotics for Infinite Damped Jacobi Lattices}
\author{Qian Qi}
\date{September 4, 2026}
\begin{document}

\begin{abstract}
We develop one response-geometry framework for Bayesian identification of
damped oscillator lattices from a single noisy boundary coordinate.  For a
homogeneous bath, six short durations recover a triangular system of response
jets for five physical coefficients.  A finite-prefix balanced calibration
scheme with predictable durations and fresh signs gives policy-uniform global
contrast without resetting the state.  We prove a random-information
quasi-Bernstein--von Mises theorem in total variation under arbitrary
sample-size-dependent initial-state priors on a Hilbert ball, together with
strong filter jets in deterministic separable dual subspaces and a functional
posterior limit for the complete inferred memory kernel.

For an inhomogeneous bath, every Jacobi coupling and pinning coefficient is
unknown.  The boundary response reconstructs the complete sequence by a
Weyl--Schur recursion.  Countable randomized response probes and increasing
washouts yield a uniform log-likelihood limit on the compact coefficient
product.  The posterior of every closed set has an exact exponential upper
rate given by its sampled response distance, and every finite coefficient
block contracts exponentially through a positive inverse-response modulus.
This quantitative result implies strong posterior consistency for the entire
semi-infinite Jacobi operator.
\end{abstract}

\maketitle
\tableofcontents

\input{round41/introduction.tex}
\input{round41/triangular.tex}
\input{round41/lattice.tex}
\input{round41/filter_memory.tex}
\input{round41/infinite_jacobi.tex}
\input{round41/preparations.tex}

\appendix
\input{round41/appendix_uniformity.tex}
\input{round41/references.tex}
\end{document}
"""
write(ROOT / "ROUND41_REVISION.tex", main)

# ---------------------------------------------------------------------------
# Reviewer-facing response and proof ledgers.
# ---------------------------------------------------------------------------
response = r"""# Author response to Round 40

**Controlling report:** `REFEREE_REPORT_ROUND40_GPT56_PRO_HARSH.md`  
**Reviewed head:** `1144f2c08a9dee66b6cc12b3bcc35252a054160b`  
**Revision entry point:** `ROUND41_REVISION.tex`

The revision strengthens the two response-identification theorems while
preserving their full positive claims.  The finite model now has a genuinely
uniform horizon-dependent policy class; the infinite model now has a valid
compact-class likelihood proof and a quantitative posterior rate theorem.

| Referee item | Revision | Mathematical closure |
|---|---|---|
| R40-M1/M2 | `round41/lattice.tex`, Lemma `lem:prefix-window-count` and Proposition `prop:balanced-contrast` | Replaces asymptotic density by `N_cal(m) >= rho m-C_cal` for every prefix; proves `W_n >= rho n/6-C_win` and carries the constant through the predictable contrast and Azuma/net argument. |
| R40-M3 | `round41/lattice.tex` | Declares one common exploitation force bound `U` and uses `max(a,U)` in all Duhamel derivative bounds. |
| R40-M4/M9 | `round41/lattice.tex`, `round41/filter_memory.tex` | Declares common `tau_min,tau_max`; sets `underline tau=min(tau,tau_min)` and proves `t_i >= i underline tau` in nuisance and filter estimates. |
| R40-M5 | `round41/lattice.tex` | Makes the duration `F_{i-1}`-measurable before the fresh sign and conditions the sign-square identity on `F_{i-1}`. |
| R40-M6 | `round41/infinite_jacobi.tex` | Declares the compact box `0<c_-<c_+`, `0<a_-<a_+`, `2a_+<b_-<b_+`. |
| R40-M7/M8 | `round41/appendix_uniformity.tex`, Lemma `lem:supnorm-response-slln` | Replaces the invalid `L^2`-net/uncountable-Doob step by a finite `C([0,T])` sup-norm net.  One empirical first moment `n^{-1} sum |xi_i|` controls every member of a net ball; the square field uses `|f^2-g^2| <= 2B||f-g||_infty`. |
| R40-M10 | `round41/filter_memory.tex`, Lemma `lem:strong-pushforward` | Introduces deterministic separable jet-dual spaces `E_j^0`, proves Bochner measurability there, uses a fixed countable dense parameter set for suprema, and displays the polynomial dependence on `L^1`/TV derivative norms. |
| Significance | `round41/introduction.tex`; Proposition `prop:jacobi-response-geometry`; Theorem `thm:jacobi-rate` | Unifies both models through response geometry and strengthens infinite-Jacobi consistency to an exact closed-set exponential posterior upper rate and finite-cylinder contraction via `kappa_J(delta)`.  Adds Vollmer (2013) and de Hoop et al. (2023). |
| Article focus | `round41/preparations.tex` and wrapper | Removes repository manifests, CI descriptions, SHA records, and review-governance prose from the mathematical article; they remain only in this reviewer packet. |

## New positive theorem

For every closed `F` in the full compact Jacobi coefficient product,

`limsup n^{-1} log Pi_n(F) <= -(a^2/(2 sigma^2)) inf_F D(β,β0)` almost surely.

For every finite coefficient block and every nonzero separation `delta`, the
compact inverse-response modulus `kappa_J(delta)` is positive, giving a
strictly negative exponential posterior rate.  Strong product-topology
consistency is now a corollary rather than the endpoint of the proof.

## Verification boundary

The executable checks cover source invariants, exact finite jet algebra, the
Vandermonde determinant, the finite Schur identity, source hashes, and the
LaTeX build.  The new martingale and Banach-space arguments are mathematical
proofs in the article, not claims of proof-assistant verification.
"""
write(ROOT / "AUTHOR_RESPONSE_ROUND40.md", response)

review_index = r"""# Round 41 review index

## Primary files

- `ROUND41_REVISION.tex` — manuscript entry point.
- `AUTHOR_RESPONSE_ROUND40.md` — itemized response to the controlling report.
- `round41/PROOF_LEDGER.json` — machine-readable obligation map.
- `round41/SOURCE_MANIFEST.json` — exact source hashes and byte sizes.
- `ROUND41_LOCAL_VERIFICATION.json` — generated build/source verification record.

## Proof map

- Abstract nonlinear adaptive theorem: `round41/triangular.tex`.
- Five-coefficient response embedding, prefix-balanced contrast, and BvM:
  `round41/lattice.tex`.
- Deterministic separable strong filter jets and memory posterior:
  `round41/filter_memory.tex`.
- Complete Jacobi reconstruction, response geometry, and exponential posterior
  rate: `round41/infinite_jacobi.tex`.
- Compact response-class strong laws: `round41/appendix_uniformity.tex`.
- Finite preparation mixture: `round41/preparations.tex`.

## New theorem labels

- `lem:prefix-window-count`
- `lem:strong-pushforward`
- `lem:supnorm-response-slln`
- `prop:jacobi-response-geometry`
- `thm:jacobi-rate`
"""
write(ROOT / "ROUND41_REVIEW_INDEX.md", review_index)

ready = r"""# Round 41 ready for review

This branch contains the positive Round 41 revision responding to the latest
Round 40 referee report.  The canonical source is `ROUND41_REVISION.tex`.
The reviewer packet consists of `AUTHOR_RESPONSE_ROUND40.md`,
`ROUND41_REVIEW_INDEX.md`, `round41/PROOF_LEDGER.json`, and the exact source
manifest.  The generated verification record reports source tests and the
two-pass LaTeX build at the revision head.
"""
write(ROOT / "ROUND41_READY_FOR_REVIEW.md", ready)

history = r"""# Historical derivations reused and strengthened in Round 41

| Source | Reused mechanism | Round 41 strengthening |
|---|---|---|
| `round39/lattice.tex` | six-duration jet inversion and radial compact net | finite-prefix calibration arithmetic, common action bounds, and exact window constants |
| dormant `finalize-round39-sources.yml` | draft declarations of compact boxes and duration bounds | retained only after full proofs were supplied; the invalid uncountable-class argument was not reused |
| `round33/chapters/C1.tex` | strong differentiation on a common finite-cylinder level | upgraded to deterministic separable Hilbert jet-dual spaces for the actual filter push-forward |
| `round33/chapters/C2.tex` | chronological policy cancellation and evidence normalization | retained in the exact adaptive likelihood architecture |
| `round39/infinite_jacobi.tex` | Weyl/Schur reconstruction and compact response image | upgraded from qualitative consistency to a uniform likelihood limit and closed-set exponential posterior rate |

## New tools

1. **Finite-prefix window calculus.**  A pathwise floor identity converts the
   common prefix lower density into an explicit number of complete diagnostic
   windows at every horizon.
2. **Supremum-norm response-class strong law.**  Compactness in `C([0,T])`
   gives a finite net; `n^{-1} sum |xi_i|` controls all functions in one net
   ball simultaneously.
3. **Deterministic separable jet range.**  Point and derivative evaluations
   generate a fixed separable subspace of the full test-function dual, closing
   strong measurability of filter jets.
4. **Response-information rate geometry.**  The sampled response metric is a
   homeomorphic coordinate on the compact Jacobi product, and its closed-set
   minima become exact posterior exponential rates.
"""
write(R41 / "HISTORICAL_REUSE.md", history)

ledger = {
    "round": 41,
    "controlling_report": "REFEREE_REPORT_ROUND40_GPT56_PRO_HARSH.md",
    "reviewed_head": "1144f2c08a9dee66b6cc12b3bcc35252a054160b",
    "base_revision_head": "1f1409c10d4444ef38c746e12ce426520d7f1ef5",
    "status": "positive closure implemented with quantitative strengthening",
    "obligations": {
        "R40-M1-M2": {"status": "closed", "labels": ["lem:prefix-window-count", "prop:balanced-contrast"]},
        "R40-M3": {"status": "closed", "location": "round41/lattice.tex common U"},
        "R40-M4-M9": {"status": "closed", "location": "underline tau in lattice and filter theorems"},
        "R40-M5": {"status": "closed", "location": "predictable duration before sign"},
        "R40-M6": {"status": "closed", "location": "round41/infinite_jacobi.tex compact coefficient box"},
        "R40-M7-M8": {"status": "closed", "label": "lem:supnorm-response-slln"},
        "R40-M10": {"status": "closed", "label": "lem:strong-pushforward"},
        "R40-significance": {
            "status": "strengthened",
            "labels": ["prop:jacobi-response-geometry", "thm:jacobi-rate"],
            "result": "closed-set posterior rate and finite-cylinder exponential contraction",
        },
    },
    "article_governance_separation": {
        "status": "closed",
        "article_source": "round41/preparations.tex contains only mathematics",
        "reviewer_records": ["AUTHOR_RESPONSE_ROUND40.md", "ROUND41_REVIEW_INDEX.md", "round41/SOURCE_MANIFEST.json"],
    },
    "formal_proof_assistant": False,
}
write(R41 / "PROOF_LEDGER.json", json.dumps(ledger, indent=2, sort_keys=True))

# ---------------------------------------------------------------------------
# Exact source tests.  Retain the finite algebra from Round 39 and add
# regression tests for every Round 40 source-level obligation.
# ---------------------------------------------------------------------------
old_test = (ROOT / "tests" / "test_round39.py").read_text(encoding="utf-8")
test = old_test.replace("Round39", "Round41").replace("round39", "round41")
test = test.replace("preparations_verification.tex", "preparations.tex")
insertion = r'''
    def test_round40_uniformity_invariants_are_landed(self) -> None:
        lattice = (ROOT / "round41/lattice.tex").read_text(encoding="utf-8")
        for token in (
            r"N_{\rm cal}(m)\ge \rho m-C_{\rm cal}",
            r"\tau_{\min}",
            r"U<\infty",
            r"\cF_{i-1}\longrightarrow s_i\longrightarrow S_i",
            r"\label{lem:prefix-window-count}",
            r"\underline\tau=\min(\tau,\tau_{\min})",
        ):
            self.assertIn(token, lattice)

    def test_uncountable_class_gap_is_replaced_by_supnorm_net(self) -> None:
        appendix = (ROOT / "round41/appendix_uniformity.tex").read_text(encoding="utf-8")
        self.assertIn(r"\label{lem:supnorm-response-slln}", appendix)
        self.assertIn(r"\frac1n\sum_{i=1}^n\abs{\xi_i}", appendix)
        self.assertIn(r"\abs{f(t)^2-f^k(t)^2}\le2B\varepsilon", appendix)
        self.assertNotIn("conditional second moment at most", appendix)
        self.assertNotIn("Doob's inequality", appendix)

    def test_filter_range_is_fixed_and_separable(self) -> None:
        text = (ROOT / "round41/filter_memory.tex").read_text(encoding="utf-8")
        self.assertIn(r"\mathbb E_j^0", text)
        self.assertIn("deterministic separable Banach subspace", text)
        self.assertIn(r"K^{r+1}M_r\varepsilon", text)

    def test_quantitative_jacobi_rate_is_present(self) -> None:
        text = (ROOT / "round41/infinite_jacobi.tex").read_text(encoding="utf-8")
        for label in (
            "prop:jacobi-response-geometry",
            "thm:jacobi-rate",
            "eq:jacobi-closed-set-rate",
            "eq:jacobi-cylinder-rate",
        ):
            self.assertIn(f"\\label{{{label}}}", text)
        self.assertIn(r"2a_+<b_-<b_+<\infty", text)
        self.assertIn(r"U_J<\infty", text)

    def test_article_excludes_repository_governance(self) -> None:
        article_paths = [
            ROOT / "ROUND41_REVISION.tex",
            *sorted((ROOT / "round41").glob("*.tex")),
        ]
        forbidden = ("GitHub Actions", "SHA--256", "Round 40 report", "source manifest")
        combined = "\n".join(path.read_text(encoding="utf-8") for path in article_paths)
        for token in forbidden:
            self.assertNotIn(token, combined)
'''
marker = "\n\nif __name__ == \"__main__\":\n"
if marker not in test:
    raise RuntimeError("test insertion marker missing")
test = test.replace(marker, "\n" + insertion + marker, 1)
write(ROOT / "tests" / "test_round41.py", test)

# ---------------------------------------------------------------------------
# Verification utility.
# ---------------------------------------------------------------------------
verifier = r'''#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "round41" / "SOURCE_MANIFEST.json"
PDF = ROOT / "ROUND41_REVISION.pdf"
LOG = ROOT / "ROUND41_REVISION.log"

EXPECTED_LABELS: dict[str, tuple[str, ...]] = {
    "round41/triangular.tex": ("thm:abstract-bvm", "lem:random-laplace"),
    "round41/lattice.tex": ("thm:jet-embedding", "lem:prefix-window-count", "prop:balanced-contrast", "thm:lattice-bvm"),
    "round41/filter_memory.tex": ("lem:strong-pushforward", "thm:filter-jets", "cor:state-image", "cor:memory-posterior"),
    "round41/infinite_jacobi.tex": ("thm:jacobi-reconstruction", "prop:jacobi-response-geometry", "thm:jacobi-rate", "thm:jacobi-consistency"),
    "round41/preparations.tex": ("thm:preparation-mixture",),
    "round41/appendix_uniformity.tex": ("lem:supnorm-response-slln",),
}

REQUIRED_INPUTS = (
    "round41/introduction.tex",
    "round41/triangular.tex",
    "round41/lattice.tex",
    "round41/filter_memory.tex",
    "round41/infinite_jacobi.tex",
    "round41/preparations.tex",
    "round41/appendix_uniformity.tex",
    "round41/references.tex",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_structure() -> dict[str, Any]:
    failures: list[str] = []
    main = ROOT / "ROUND41_REVISION.tex"
    main_text = main.read_text(encoding="utf-8") if main.is_file() else ""
    if not main.is_file():
        failures.append("missing ROUND41_REVISION.tex")
    for source in REQUIRED_INPUTS:
        if not (ROOT / source).is_file():
            failures.append(f"missing {source}")
        if f"\\input{{{source}}}" not in main_text:
            failures.append(f"main manuscript does not input {source}")
    for source, labels in EXPECTED_LABELS.items():
        path = ROOT / source
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for label in labels:
            if f"\\label{{{label}}}" not in text:
                failures.append(f"missing label {label} in {source}")
    article = "\n".join((ROOT / p).read_text(encoding="utf-8") for p in ("ROUND41_REVISION.tex", *REQUIRED_INPUTS) if (ROOT / p).is_file())
    for token in ("GitHub Actions", "SHA--256", "Round 40 report", "source manifest"):
        if token in article:
            failures.append(f"article contains governance token: {token}")
    return {"passed": not failures, "failures": failures}


def check_manifest() -> dict[str, Any]:
    failures: list[str] = []
    if not MANIFEST.is_file():
        return {"passed": False, "failures": ["manifest missing"]}
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("files", [])
    for entry in entries:
        path = ROOT / entry["path"]
        if not path.is_file():
            failures.append(f"missing {entry['path']}")
            continue
        if path.stat().st_size != entry["bytes"]:
            failures.append(f"size mismatch for {entry['path']}")
        if sha256(path) != entry["sha256"]:
            failures.append(f"sha256 mismatch for {entry['path']}")
    return {"passed": bool(entries) and not failures, "checked_files": len(entries), "failures": failures}


def check_build() -> dict[str, Any]:
    failures: list[str] = []
    if not PDF.is_file() or PDF.stat().st_size < 10_000:
        failures.append("ROUND41_REVISION.pdf missing or unexpectedly small")
    text = LOG.read_text(encoding="utf-8", errors="replace") if LOG.is_file() else ""
    if not LOG.is_file():
        failures.append("ROUND41_REVISION.log missing")
    for token in ("! LaTeX Error:", "There were undefined references", "Citation `", "Reference `", "Emergency stop", "Fatal error occurred"):
        if token in text:
            failures.append(f"build log contains: {token}")
    match = re.search(r"Output written on .*?\((\d+) pages?", text)
    if not match and LOG.is_file():
        failures.append("could not determine page count")
    return {
        "passed": not failures,
        "pdf_bytes": PDF.stat().st_size if PDF.is_file() else None,
        "pdf_pages": int(match.group(1)) if match else None,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-manifest", action="store_true")
    parser.add_argument("--check-build", action="store_true")
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()
    result: dict[str, Any] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": {"implementation": platform.python_implementation(), "version": platform.python_version()},
        "structure": check_structure(),
        "scope": {
            "formal_proof_assistant": False,
            "checked": ["source invariants", "manifest hashes", "two-pass LaTeX build"],
            "analytic_proofs": ["finite-prefix empirical process", "strong dual measurability", "compact-class SLLN", "Jacobi posterior rate"],
        },
    }
    if args.check_manifest:
        result["manifest"] = check_manifest()
    if args.check_build:
        result["build"] = check_build()
    result["all_passed"] = all(v.get("passed", True) for k, v in result.items() if isinstance(v, dict) and k not in {"python", "scope"})
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json_path:
        out = args.json_path if args.json_path.is_absolute() else ROOT / args.json_path
        out.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
write(ROOT / "tools" / "verify_round41.py", verifier)

# ---------------------------------------------------------------------------
# Exact source manifest.  It intentionally excludes generated PDF/log files.
# ---------------------------------------------------------------------------
manifest_paths = [
    "ROUND41_REVISION.tex",
    "round41/preamble.tex",
    "round41/introduction.tex",
    "round41/triangular.tex",
    "round41/lattice.tex",
    "round41/filter_memory.tex",
    "round41/infinite_jacobi.tex",
    "round41/preparations.tex",
    "round41/appendix_uniformity.tex",
    "round41/references.tex",
    "AUTHOR_RESPONSE_ROUND40.md",
    "ROUND41_REVIEW_INDEX.md",
    "ROUND41_READY_FOR_REVIEW.md",
    "round41/HISTORICAL_REUSE.md",
    "round41/PROOF_LEDGER.json",
    "tools/materialize_round41.py",
    "tools/verify_round41.py",
    "tests/test_round41.py",
    ".github/workflows/materialize-round41.yml",
    ".github/workflows/verify-round41.yml",
]
entries = []
for relative in manifest_paths:
    path = ROOT / relative
    if not path.is_file():
        raise RuntimeError(f"manifest source missing: {relative}")
    entries.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})
manifest = {
    "source_set": "round41-positive-referee-closure",
    "base_revision_head": "1f1409c10d4444ef38c746e12ce426520d7f1ef5",
    "reviewed_head": "1144f2c08a9dee66b6cc12b3bcc35252a054160b",
    "controlling_report": "REFEREE_REPORT_ROUND40_GPT56_PRO_HARSH.md",
    "generated_at_utc": "2026-09-04T06:00:00+00:00",
    "hash": "sha256",
    "files": entries,
}
write(R41 / "SOURCE_MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True))

print(json.dumps({"materialized": True, "round": 41, "files": len(entries)}, indent=2))
