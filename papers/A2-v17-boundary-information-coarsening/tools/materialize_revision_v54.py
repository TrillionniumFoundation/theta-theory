#!/usr/bin/env python3
"""Materialize A2 v54 with exact v53 originals and checked, idempotent edits.

The sole replaced mathematical statement/proof is a strengthened corollary.
Every other inherited statement/proof remains verbatim and active.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from source_provenance import require

P = Path(__file__).resolve().parents[1]
ARCHIVE = P / 'history/v53-review-baseline'
SOURCE_V53 = '42cc62f230473c34d78af1d06b9ca5c2651ae86d'
REVIEW_V53 = '000ce24f65f8381d2180cbd1f080d3d8470c8157'
MODULE = 'article/18g_realized_window_information_v53.tex'
CHANGES = ('main.tex', 'article/00_structural_introduction_v48.tex', MODULE,
           'v5/references_v43.tex')

COROLLARY = r'''\begin{corollary}[Uniform small-window finite-flight transfer]
\label{cor:v53-finite-flight}
Choose the gates and recording profiles as in
Theorem~\ref{thm:v53-realized-experiment}.  Let $Q_{s,J,h}$ be the rescaled
recorded law for an even $J$-flight bridge at time $Jg+d$, conditional on
recording both endpoints in the window.  There are $J_0$, $C<\infty$ and
$\tau\in(0,1)$, independent of $0<h\le h_0$ and $s$ in the displayed
compact interval, such that
\begin{equation}\label{eq:v53-finite-flight}
       \|q_{s,J,h}-q_{s,h}\|_\infty\le C\tau^J,
                  \qquad J\ge J_0.
\end{equation}
After decreasing $h_0$ and increasing $J_0$, both densities are bounded
below by a common $m>0$ on the rescaled square.  In particular,
\begin{align}
 H^2(Q_{s,J,h},Q_{s,h})&\le C\tau^{2J},
                                    \label{eq:v54-one-record-H}\\
 \operatorname{TV}\!\left(\bigotimes_{k=1}^n Q_{s,J,h}^{(k)},
                           \bigotimes_{k=1}^n Q_{s,h}^{(k)}\right)
   &\le \min\{1,C\sqrt n\,\tau^J\}.
                                    \label{eq:v54-product-TV}
\end{align}
Here the superscripts allow any fixed allocation among the four labelled
same-type laws.  Thus all optimal-error limits in
Theorem~\ref{thm:v53-realized-experiment} hold for the finite-flight pair
if $n_h\tau^{2J_h}\to0$.  The finite-flight mean-test error is at most
\begin{equation}\label{eq:v54-error-transfer}
          \exp(-cn_hh^8)+C\sqrt{n_h}\,\tau^{J_h}.
\end{equation}
For that mean test alone there is also a direct conclusion: whenever
$\tau^{J_h}=o(h^4)$, its error is at most $\exp(-c'n_hh^8)$ for all
sufficiently small $h$, without a product-approximation hypothesis on
$n_h$.

Let $\pi_{s,J}$ be the original gated-bridge success probability, before
endpoint recording and cropping, and let $r_{s,J}(h)$ be the conditional
probability of the extra recording and crop given that bridge.  Then
\begin{equation}\label{eq:v53-recording-mass}
 c_-h^2\le r_{s,J}(h)\le c_+h^2,\qquad
 r_{s,\infty}(h)=\frac{c_*^2h^2}{dZ_s}\{4-I_s(h)^2\},
\end{equation}
where $Z_s$ is the normalizer of the full limiting same-type endpoint law.
For independent repeated preparations at a fixed design, the expected
number needed for $n$ recorded successes is exactly
$n/(\pi_{s,J}r_{s,J}(h))$.  This expectation is not a deterministic
preparation-cap guarantee.
\end{corollary}

\begin{proof}
Let $f_{s,J}$ and $f_s$ be the successful full endpoint densities in the
true signed contact chart, before recording.  The relative factorization
in Theorem~\ref{thm:v4-factorization}, with its positive fixed-offset
normalizer, gives
\[
 \|f_{s,J}-f_s\|_{C^0([-h_0,h_0]^2)}\le C\tau^J.
\]
This is the density comparison in the proof of
Corollary~\ref{cor:v26-finite-flight-inverse}; the compact analytic family
supplies its uniform constants.  Shrinking $h_0$ and increasing $J_0$
make both densities uniformly positive and bounded on this square.
The recording profiles and their reciprocals are bounded there as well.
Writing $w_s(u,v)=e_s(u)e_s(v)$ and
$A_{s,J}(h)=\int_{(-h,h)^2}w_sf_{s,J}$, we have
\[
 A_{s,J}(h)\asymp h^2,\qquad
 |A_{s,J}(h)-A_{s,\infty}(h)|\le Ch^2\tau^J.
\]
Subtract the rescaled quotients
\[
 q_{s,J,h}(z,w)=
 \frac{h^2w_s(hz,hw)f_{s,J}(hz,hw)}{A_{s,J}(h)}.
\]
The numerator error and normalizer have the same area factor.  Their
quotient proves \eqref{eq:v53-finite-flight}, with no inverse-area loss.
The same bounds give the common positive lower density bound.

For any such two densities $p,q$ on $[-1,1]^2$,
\[
 H^2(P,Q)=\int\frac{(p-q)^2}{(\sqrt p+\sqrt q)^2}
       \le\frac{1}{4m}\int(p-q)^2
       \le m^{-1}\|p-q\|_\infty^2.
\]
This proves \eqref{eq:v54-one-record-H}.  If
$\mathfrak a(P,Q)=\int\sqrt{pq}=1-H^2(P,Q)/2$, independence gives
$\mathfrak a(\bigotimes P_k,\bigotimes Q_k)=\prod_k\mathfrak a(P_k,Q_k)$.
The inequality $1-\prod_k(1-x_k)\le\sum_kx_k$, $0\le x_k\le1$,
therefore gives
$H^2(\bigotimes P_k,\bigotimes Q_k)\le\sum_k H^2(P_k,Q_k)$.
Together with $\operatorname{TV}\le H$, this proves
\eqref{eq:v54-product-TV}, uniformly in the fixed label allocation.
Expectations of tests taking values in $[0,1]$ differ by at most total
variation under each alternative.  Taking the infimum over tests proves
the assertion about optimal errors; applying the bound to the mean test
proves \eqref{eq:v54-error-transfer}.  The former sufficient condition
$n_h\tau^{J_h}\to0$ and bound $\exp(-cn_hh^8)+Cn_h\tau^{J_h}$ follow
as weaker consequences, since $n_h\ge1$ and $\tau^{J_h}\le1$.

For the direct mean-test bound, put
$D_h=\mu_1(h)-\mu_0(h)=c_0h^4+O(h^6)$, where
$c_0=14\Delta/(2025d^2)>0$ and the means are those of the two ideal
laws.  The boundedness of $F$ and \eqref{eq:v53-finite-flight} show that
every finite-flight mean differs from its corresponding ideal mean by
at most $C\tau^J$.  If $\tau^J=o(h^4)$, the fixed ideal midpoint is
at distance at least $D_h/4$ from each finite-flight mean, on the correct
side.  The bounded-variable inequality used in the preceding theorem,
applied directly to the independent finite-flight variables of range
length one, bounds each error by $\exp(-n_hD_h^2/8)$.  This is
$\exp(-c'n_hh^8)$ for small $h$.  It compares the performance of this
statistic, not the total variation of two growing product experiments.

Finally $r_{s,J}(h)=A_{s,J}(h)$.  Substitution of the limiting density
and \eqref{eq:v53-efficiency} gives the exact mass formula in
\eqref{eq:v53-recording-mass}; the positivity bounds give its two-sided
estimate.  Each independent preparation is accepted with probability
$\pi_{s,J}r_{s,J}(h)>0$.  The sum of $n$ independent geometric waiting
times has the displayed expectation.  No conditioning on completion
of a finite preparation cap is used in this calculation.
\end{proof}

The Hellinger sharpening and the distinction between product transfer and
direct testing were communicated in~\cite{A2ReviewV53}.  The choices are
joint: for example, taking the smallest admissible even $J$ with
$\tau^J\le h/\sqrt{n_h+1}$ ensures $n_h\tau^{2J}\to0$.  At the critical
scale $n_hh^8\asymp1$, it suffices that $\tau^{J_h}=o(h^4)$.
For any fixed $\varepsilon>0$, a sufficient explicit choice there is
\[
 J_h=2\left\lceil
       \frac{(4+\varepsilon)\log(1/h)}{2|\log\tau|}
      \right\rceil,
\]
with $J_h$ increased to $J_0$ if necessary.  This improves a sufficient
flight-length coefficient; no optimal geometric convergence exponent is
asserted.  In the supercritical regime a direct bound for the mean test
need not approximate its entire growing sample law.
'''

WAITING = r'''
\subsection{Waiting records, coarsening and a deterministic cap}

We next retain the accepted mass of the same experiment, rather than
normalizing it away.  Fix one channel and one contact type in
Theorem~\ref{thm:v53-realized-experiment}, and retain its two specified
table/profile alternatives $s_0,s_1$.  Only the acceptance indicator is
recorded on a failed preparation; no raw failed-shot position or residual
time is available.  Independent preparations are made at one even flight
number $J_h\to\infty$, fixed before acquisition.  Put
\begin{equation}\label{eq:v54-accepted-probability}
 p_{i,h}=\pi_{s_i,J_h}r_{s_i,J_h}(h),\qquad
 \gamma_i=\operatorname{arcosh}(1+g\kappa_{s_i}),\qquad
 \rho_h=p_{1,h}/p_{0,h}.
\end{equation}
Let $W_h$ count preparations up to and including the first accepted
window record, and let $Y_h$ be that rescaled mark.  Denote the binary
experiments observing $Y_h$ and $(W_h,Y_h)$ by $\mathcal E_h$ and
$\mathcal F_h$, respectively.  For binary experiments
$\mathcal U=(U_0,U_1)$, $\mathcal V=(V_0,V_1)$, use
\[
 \delta(\mathcal U,\mathcal V)
   =\inf_K\max_{i=0,1}\operatorname{TV}(KU_i,V_i),
\]
where $K$ ranges over Markov kernels independent of the unknown
alternative.  The repeat-to-first-success coarsening calculation below
was communicated in~\cite{A2ReviewV53}.  The deterministic-cap conclusion
also identifies the testing scale when the experiment can end without an
accepted mark.

\begin{theorem}[Accepted marks and charged first-acceptance records]
\label{thm:v54-waiting-and-cap}
For the specified pair and any even $J_h\to\infty$, as $h\downarrow0$,
\begin{equation}\label{eq:v54-escape-separation}
 p_{i,h}\asymp h^2e^{-\gamma_iJ_h},\qquad
 \gamma_1>\gamma_0>0,\qquad
 \rho_h\asymp e^{-(\gamma_1-\gamma_0)J_h}\longrightarrow0.
\end{equation}
No relation between $h$ and $\tau^{J_h}$ is needed for the following
conclusions.
\begin{enumerate}
\item The optimal equal-prior error for one accepted mark tends to
$1/2$, whereas that for the record $(W_h,Y_h)$ tends to zero.  More
precisely,
\begin{equation}\label{eq:v54-deficiency}
 \delta(\mathcal F_h,\mathcal E_h)=0,\qquad
 \delta(\mathcal E_h,\mathcal F_h)\longrightarrow\tfrac12.
\end{equation}
\item Fix an integer cap $b_h\ge1$.  Observe $(W_h,Y_h)$ if $W_h\le b_h$
and a single cemetery outcome $\partial$ otherwise.  Let $R_h^*(b_h)$
be the optimal equal-prior error in this capped experiment.  If
$b_hp_{0,h}\to\lambda\in[0,\infty)$, then
\begin{equation}\label{eq:v54-capped-critical-risk}
                       R_h^*(b_h)\longrightarrow\tfrac12e^{-\lambda}.
\end{equation}
The test selecting alternative zero exactly when an acceptance occurs
before the cap attains this limit.  For arbitrary cap sequences,
$R_h^*(b_h)\to0$ if and only if $b_hp_{0,h}\to\infty$.
\item The stopped experiment uses at most $b_h$ preparations.  Its
expected charge under alternative $i$ is exactly
\begin{equation}\label{eq:v54-capped-charge}
 \mathbb E_i\min(W_h,b_h)=\frac{1-(1-p_{i,h})^{b_h}}{p_{i,h}},
                \qquad \mathbb E_iW_h=p_{i,h}^{-1}.
\end{equation}
Thus the critical deterministic-cap order for this binary
first-acceptance experiment is
$p_{0,h}^{-1}\asymp h^{-2}e^{\gamma_0J_h}$; vanishing error requires
a diverging multiple of that scale.  This is a scale in preparations,
not the $h^{-8}$ scale in successful marks.
\end{enumerate}
All tests here are for the two specified alternatives; their thresholds
may use the corresponding acceptance probabilities.  The theorem does not
assert a uniform estimator over unknown recording profiles, or an optimal
preparation bound for experiments retaining additional failed-shot data.
\end{theorem}

\begin{proof}
The contact curvatures of the pair are $80/7$ and $40/3$.  Hence
$\gamma_0=\operatorname{arcosh}(71/7)$ and
$\gamma_1=\operatorname{arcosh}(35/3)>\gamma_0$.
The positive fixed-offset prefactor in Theorem~\ref{thm:v4-law} gives
$\pi_{s_i,J}\asymp e^{-\gamma_iJ}$ along this even subsequence.
The bound \eqref{eq:v53-recording-mass} is uniform in small $h$ and large
$J$.  Multiplication proves \eqref{eq:v54-escape-separation}; in
particular both $p_{i,h}$ tend to zero.  These are the original bridge
probabilities and the fixed recording profiles of actual tables, not
freely assigned geometric-distribution parameters.

Independence of the preparations gives the exact factorization, for
$k\ge1$ and measurable $A\subset[-1,1]^2$,
\begin{equation}\label{eq:v54-stopped-factorization}
 \Pr_i(W_h=k,Y_h\in A)
   =(1-p_{i,h})^{k-1}p_{i,h}Q_{s_i,J_h,h}(A).
\end{equation}
Thus the waiting count is geometric on $\{1,2,\ldots\}$ and is
independent of its terminal mark under each alternative.  Summing
\eqref{eq:v54-stopped-factorization} in $k$ shows that discarding the
count gives exactly the finite-flight conditional mark, without any
approximation or selection of a favorable history.
By \eqref{eq:v53-tv} and \eqref{eq:v53-finite-flight},
\begin{equation}\label{eq:v54-mark-distance}
 \operatorname{TV}(E_{0,h},E_{1,h})\le C(h^4+\tau^{J_h})\longrightarrow0.
\end{equation}
Choose $m_h=\lceil(p_{0,h}p_{1,h})^{-1/2}\rceil$ and select alternative
zero when $W_h\le m_h$.  The two errors satisfy
\begin{equation}\label{eq:v54-waiting-errors}
 \Pr_0(W_h>m_h)\le e^{-\rho_h^{-1/2}},\qquad
 \Pr_1(W_h\le m_h)\le \sqrt{\rho_h}+p_{1,h}.
\end{equation}
The first bound uses $(1-p)^m\le e^{-pm}$; the second uses
$1-(1-p)^m\le mp$ and the upper rounding bound for $m_h$.
Both errors vanish, so $\operatorname{TV}(F_{0,h},F_{1,h})\to1$.
The equal-prior error identity proves the first comparison.

Projection discarding $W_h$ proves
$\delta(\mathcal F_h,\mathcal E_h)=0$.  For any kernel $K$, contraction
and the triangle inequality give
\[
 \operatorname{TV}(F_{0,h},F_{1,h})
 \le 2\max_i\operatorname{TV}(KE_{i,h},F_{i,h})
              +\operatorname{TV}(E_{0,h},E_{1,h}).
\]
Equations \eqref{eq:v54-mark-distance}--\eqref{eq:v54-waiting-errors}
therefore give the lower limit $1/2$ for the reverse deficiency.
The kernel ignoring its input and drawing from
$(F_{0,h}+F_{1,h})/2$ has maximum error
$\operatorname{TV}(F_{0,h},F_{1,h})/2\le1/2$ and proves the matching
upper bound.  Kernels may depend on the specified pair and on $h$, but
not on which alternative generated the input.

For the deterministic cap, put
$a_{i,h}=1-(1-p_{i,h})^{b_h}$, the probability of at least one acceptance.
Eventually $p_{1,h}<p_{0,h}$, so $a_{1,h}\le a_{0,h}$.
The two capped laws have respective cemetery masses $1-a_{i,h}$.
Testing the event of any acceptance gives a lower bound on their total
variation, and their common cemetery mass gives an upper bound:
\begin{equation}\label{eq:v54-capped-TV-sandwich}
 a_{0,h}-a_{1,h}
  \le \operatorname{TV}(F_{0,h}^{[b_h]},F_{1,h}^{[b_h]})
  \le a_{0,h}.
\end{equation}
This bound does not presume equality of the conditional accepted-mark
laws.  If $b_hp_{0,h}\to\lambda<\infty$, then
$b_hp_{1,h}=\rho_hb_hp_{0,h}\to0$ and
$b_hp_{0,h}^2\to0$.  Expanding $\log(1-p_{0,h})$ shows
$a_{0,h}\to1-e^{-\lambda}$, while $a_{1,h}\to0$.
The sandwich proves \eqref{eq:v54-capped-critical-risk}.  The stated
test has exact equal-prior error
$\{(1-p_{0,h})^{b_h}+1-(1-p_{1,h})^{b_h}\}/2$ and hence attains that
limit.

If $b_hp_{0,h}\to\infty$, use the earlier test with the observable
threshold $t_h=\min\{b_h,m_h\}$.  It is determined by the capped
record, including its cemetery outcome.  Its errors are bounded by
$e^{-p_{0,h}t_h}$ and $p_{1,h}t_h$.  The first vanishes because
$p_{0,h}t_h=\min\{b_hp_{0,h},p_{0,h}m_h\}\to\infty$; the second is
at most $\sqrt{\rho_h}+p_{1,h}\to0$.  Conversely, if
$b_hp_{0,h}$ does not tend to infinity, a bounded subsequence has a
further subsequence converging to some finite $\lambda$.  On that
subsequence \eqref{eq:v54-capped-critical-risk} gives a strictly
positive limiting error.  This proves the necessity as well as
sufficiency of the cap criterion.

Finally the tail-sum identity gives
$\mathbb E_i\min(W_h,b_h)=\sum_{k=0}^{b_h-1}(1-p_{i,h})^k$,
which is \eqref{eq:v54-capped-charge}; the infinite geometric sum gives
$\mathbb E_iW_h$.  Every failed preparation before stopping is included.
The cap scale follows from \eqref{eq:v54-escape-separation} and the
proved risk criterion, not from turning an expected waiting time into
a deterministic bound.
\end{proof}

The two limits describe distinct coarsenings of one physical acquisition
record.  Conditional normalization suppresses the accepted mass, leaving
an $h^4$ interaction contrast; retaining failures exposes the different
hyperbolic exponents.  At a fixed preparation cap, the cemetery outcome
itself becomes informative.  None of these operations changes the exact
window invariant or the geometric rigidity theorem.  Their statistical
conclusions remain specific to the stated records and fixed pair of
profiles, which need not be known or shared in the unrestricted nuisance
problem.
'''


def replace_once(text: str, before: str, after: str) -> str:
    require(text.count(before) == 1, 'Unexpected edit anchor: ' + before[:100])
    return text.replace(before, after, 1)


def old_corollary_region(text: str) -> tuple[int, int]:
    a=text.index(r'\begin{corollary}[Uniform small-window finite-flight transfer]')
    b=text.index(r'\end{proof}',a)+len(r'\end{proof}')
    return a,b


def revised(name: str, text: str) -> str:
    if name=='main.tex':
        text=text.replace('A2 revision 53','A2 revision 54')
        text=replace_once(text,
            'comparison.  The local experiments obtained by retaining',
            'comparison.  Retaining the first waiting count yields reverse binary deficiency\n$1/2$ in the limit; deterministic caps have an explicit limiting risk.\nThe local experiments obtained by retaining')
        return replace_once(text,
            'comparison.\n\n\\appendix',
            'comparison.  The Hellinger improvement and repeat-to-first-success\ncomparison in Section~\\ref{sec:v53-window-information} were communicated\nin~\\cite{A2ReviewV53}; the deterministic-cap risk is proved here.\n\n\\appendix')
    if name=='article/00_structural_introduction_v48.tex':
        return replace_once(text,
            'Corollary~\\ref{cor:v53-finite-flight} transfers the experiment to actual\nfinite flights under $n\\tau^J\\to0$.  Its normalizing integrals also show\nan additional recording fraction of order $h^2$, separate from the\noriginal bridge rarity.',
            'Corollary~\\ref{cor:v53-finite-flight} transfers the experiment to actual\nfinite flights with total-variation error $C\\sqrt n\\,\\tau^J$, under\n$n\\tau^{2J}\\to0$.  The bounded-moment test has a direct exponential\nerror bound whenever $\\tau^J=o(h^4)$, without requiring product\napproximation in the supercritical regime.  Its normalizing integrals\nalso show an additional recording fraction of order $h^2$, separate\nfrom the original bridge rarity.  For this same pair,\nTheorem~\\ref{thm:v54-waiting-and-cap} shows that one first-acceptance\ncount consistently distinguishes the tables, while its accepted mark\nalone becomes uninformative: the reverse binary deficiency tends to\n$1/2$.  At a deterministic cap $b_h$, the optimal error tends to\n$e^{-\\lambda}/2$ when $b_hp_{0,h}\\to\\lambda<\\infty$, and tends to\nzero exactly when $b_hp_{0,h}\\to\\infty$.  Here\n$p_{0,h}\\asymp h^2e^{-\\gamma_0J_h}$ is the actual acceptance probability.\nThese charged and conditional conclusions concern different records of\none specified experiment, not competing universal complexity bounds.')
    if name==MODULE:
        a,b=old_corollary_region(text)
        # The two old paragraphs after the corollary are preserved except the
        # obsolete sufficient-flight prescription, which the new proof strengthens.
        tail=text.index('For every fixed window these records',b)
        return text[:a]+COROLLARY+'\n'+text[tail:]+WAITING
    if name=='v5/references_v43.tex':
        return replace_once(text,r'\end{thebibliography}',r'''\bibitem{A2ReviewV53}
\emph{Independent referee report on A2, revision 53},
author-requested AI-assisted memorandum, September 15, 2026, Sections 4--5.
Repository \texttt{TrillionniumFoundation/theta-theory},
\href{https://github.com/TrillionniumFoundation/theta-theory/blob/000ce24f65f8381d2180cbd1f080d3d8470c8157/reviews/a2-v53-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md}{frozen review memorandum}.
Cited for the Hellinger transfer and first-waiting-record comparison;
not a commissioned journal evaluation or a mathematical certificate.

\end{thebibliography}''')
    raise RuntimeError('Unknown edited file: '+name)


def materialize() -> dict:
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    target=ARCHIVE/'active-source-manifest.json'
    if not target.exists():
        origin=P.parents[1]/'deliveries/a2-v53'/SOURCE_V53/'active-source-manifest.json'
        require(origin.is_file(),'Missing source-matched v53 active manifest')
        target.write_bytes(origin.read_bytes())
    groups=json.loads(target.read_text())
    baseline={n:info for group in groups.values() for n,info in group.items()}
    require(len(baseline)==111,'Unexpected v53 active-source count')
    for name,info in baseline.items():
        archived=ARCHIVE/name
        origin=archived if name in CHANGES and archived.exists() else P/name
        raw=origin.read_bytes()
        require(len(raw)==info['bytes'] and hashlib.sha256(raw).hexdigest()==info['sha256'],
                'Unexpected v53 source: '+name)
        if name in CHANGES:
            if not archived.exists():
                archived.parent.mkdir(parents=True,exist_ok=True);archived.write_bytes(raw)
            expected=revised(name,raw.decode('utf-8'))
            require((P/name).read_text() in (raw.decode('utf-8'),expected),
                    'Unexpected existing edit: '+name)
            (P/name).write_text(expected)
    return {'baseline_source':SOURCE_V53,'review_head':REVIEW_V53,
            'baseline_active_inputs':111,'active_inputs':111,
            'archived_exact_originals':list(CHANGES),
            'strengthened_in_place':'cor:v53-finite-flight',
            'new_theorem':'thm:v54-waiting-and-cap','mathematical_certification':False}

if __name__=='__main__':
    print(json.dumps(materialize(),indent=2,sort_keys=True))
