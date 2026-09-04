#!/usr/bin/env python3
"""Apply the final referee-packet and adaptive-rate audit corrections."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{relative}: expected one anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    "round43/quantitative_jacobi.tex",
    r"""Thus all effective coefficient and weighted-operator conclusions remain valid
with the exponent multiplied by \(\rho_J\), while the nonexploration actions
may be fully adaptive.""",
    r"""For fixed \(J\), all effective coefficient conclusions remain valid with the
exponent multiplied by \(\rho_J\), while the nonexploration actions may be
fully adaptive.  For a triangular sequence \(J=J_n\) with exploration floors
\(\rho_n\), put
\[
 k_n^{\rm ad}=\rho_n\underline\kappa_{J_n}(\delta_n).
\]
If
\begin{equation}
 n(k_n^{\rm ad})^2-\mathcal H(k_n^{\rm ad}/16)\longrightarrow+\infty,
 \qquad
 \mathcal P(\sqrt{k_n^{\rm ad}}/8)=o(nk_n^{\rm ad}),
 \label{eq:adaptive-growing-depth-conditions}
\end{equation}
then the growing-block conclusion of
Theorem~\ref{thm:growing-depth-recovery} holds under the adaptive policy; if
also \(\delta_n\to0\), so does the weighted operator-norm conclusion of
Corollary~\ref{cor:weighted-operator-recovery}.  In particular, whenever
\(\inf_n\rho_n>0\), the concrete fixed-\(\delta\) regime
\(J_n=o((\log n)^{1/5})\) is unchanged.""",
)

replace_once(
    "round43/quantitative_jacobi.tex",
    r"""The denominator has exponential rate zero by full support and uniform response
continuity.  The standard numerator--denominator argument then gives
\eqref{eq:adaptive-exploration-rate}.
\end{proof}""",
    r"""The denominator has exponential rate zero by full support and uniform response
continuity.  The standard numerator--denominator argument then gives
\eqref{eq:adaptive-exploration-rate}.

For the triangular assertion, the exploration quadratic term supplies the
uniform separation \(k_n^{\rm ad}\), whereas every nonexploration quadratic
term remains nonnegative.  Bernoulli and Gaussian martingale concentration on
an \(k_n^{\rm ad}/16\)-net has exponent at least a constant multiple of
\(n(k_n^{\rm ad})^2\).  The response ball of radius
\(\sqrt{k_n^{\rm ad}}/8\) supplies the denominator.  Hence the proof of
Theorem~\ref{thm:growing-depth-recovery} applies verbatim under
\eqref{eq:adaptive-growing-depth-conditions}; the weighted conclusion then
follows from Corollary~\ref{cor:weighted-operator-recovery}.
\end{proof}""",
)

replace_once(
    "round43/quantitative_jacobi.tex",
    r"""uniform over the coefficient
box, bounded feedback segments, and working initial-state priors.  If
\(\mathcal Q\) contains the grid selected by \(s_J(\delta)\) and
\(2\max_{q\in\mathcal Q}R_{q,n}(\alpha)\) is below the grid threshold in the
proof of Theorem~\ref{thm:effective-jacobi-stability}, then
\(\operatorname{diam}_{d_J}\mathcal C_n(\alpha)\le\delta\).  The statement
continues to hold for the growing regimes of
Theorem~\ref{thm:growing-depth-recovery} whenever the corresponding cell
counts diverge.""",
    r"""uniform over the coefficient
box, bounded feedback segments, and working initial-state priors.  Let
\[
 \epsilon_{J,\delta}=\zeta_{R_J}2^{-s_J(\delta)}
\]
be the scale selected in the proof of
Theorem~\ref{thm:effective-jacobi-stability}.  If \(\mathcal Q\) contains its
\(R_J+1\) grid cells and
\begin{equation}
 2\max_{q\in\mathcal Q}R_{q,n}(\alpha)
 <\frac{\delta\epsilon_{J,\delta}^{R_J}}
        {2C_{R_J}L_J},
 \label{eq:honest-cylinder-explicit-threshold}
\end{equation}
then \(\operatorname{diam}_{d_J}\mathcal C_n(\alpha)\le\delta\).  The same
coverage statement holds for triangular finite cell sets \(\mathcal Q_n\)\)
when \(|\mathcal Q|\) in \eqref{eq:response-confidence-radius} is replaced by
\(|\mathcal Q_n|\); the growing-block diameter conclusion follows whenever
\eqref{eq:honest-cylinder-explicit-threshold} eventually holds.""",
)

replace_once(
    "AUTHOR_RESPONSE_ROUND42.md",
    "The one-use bootstrap deletes itself and all write-enabled legacy workflows before committing.  The retained Round 43 workflow has `contents: read`.",
    "The one-use materialization lane was retired after the ordinary-source commit; all legacy write-enabled workflows were then removed by SHA-pinned repository commits.  The sole retained Round 43 workflow has `contents: read`.",
)

(ROOT / "ROUND43_READY_FOR_REVIEW.md").write_text(
    """# Round 43 ready for review

Round 43 is a fully materialized, line-addressable revision responding to the
Round 42 return-without-review report.  The canonical article is
`ROUND43_REVISION.tex`; no source generator or in-memory rewrite is needed to
read or build it.  The revision branch retains exactly one workflow,
`.github/workflows/verify-round43.yml`, and it has read-only repository
permissions.  Referees should freeze the branch head attached to the review
request, then compare `round43/SOURCE_MANIFEST.json`,
`ROUND43_LOCAL_VERIFICATION.json`, and the committed `ROUND43_REVISION.pdf`
against that immutable object.  The proof ledger expressly distinguishes
mathematical arguments from executable consistency checks.
""",
    encoding="utf-8",
)

replace_once(
    "round43/PROOF_LEDGER.json",
    '        "publication record"',
    '        "source manifest and verification record"',
)

print("Round 43 final audit corrections applied")
