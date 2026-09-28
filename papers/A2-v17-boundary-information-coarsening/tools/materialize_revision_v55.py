#!/usr/bin/env python3
"""Add the stopped-record reductions in place; preserve the exact reviewed v54.

All inherited theorem/proof text is retained. Only Theorem 23.4 and its proof
receive inserted paragraphs. Metadata, attribution and overview edits are
explicit below. No inherited input is deactivated and no new section is added.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from source_provenance import require

P = Path(__file__).resolve().parents[1]
ARCHIVE = P / 'history/v54-review-baseline'
SOURCE_V54 = '2cedae961195f97df802aaa81112d95cd32974e1'
REVIEW_FIRST = '1030ca91a96ca1be8ecd0347ecbdac7084cdd8d4'
REVIEW_LATEST = '67250d08714acf76274e82158f107246f0de7eee'
MODULE = 'article/18g_realized_window_information_v53.tex'
INTRO = 'article/00_structural_introduction_v48.tex'
CHANGES = ('main.tex', INTRO, MODULE, 'v5/references_v43.tex')

DEFINITIONS = r'''
For a deterministic cap $b$, let $\mathcal C_h^{[b]}$ retain the
accepted waiting count $W_h\le b$ or the cemetery symbol, and let
$\mathcal B_h^{[b]}$ retain only $\mathbf1_{\{W_h\le b\}}$.  Thus the
censored count distinguishes acceptance at the last preparation from no
acceptance.  Write $\mathcal F_h^{[b]}$ for the full capped record,
$a_{i,h}(b)=1-(1-p_{i,h})^b$, and
$\eta_h=\operatorname{TV}(Q_{s_0,J_h,h},Q_{s_1,J_h,h})$.
Let $R_{C,h}^*(b)$ denote the count-only equal-prior risk.  We use
$\Delta_{\mathrm{LC}}(\mathcal U,\mathcal V)
=\max\{\delta(\mathcal U,\mathcal V),\delta(\mathcal V,\mathcal U)\}$.
The count reduction, finite-intensity bit reduction and count-risk formula
below were communicated in~\cite{A2ReviewV54First,A2ReviewV54Second}.
They specify which component of this stopped experiment carries its
information; they do not supply another geometric inverse.
'''

ADDED_ITEMS = r'''
\item The terminal mark can be removed uniformly over all deterministic
caps.  More precisely, for every $b\ge1$,
\begin{align}
 \delta(\mathcal F_h^{[b]},\mathcal C_h^{[b]})&=0,&
 \delta(\mathcal C_h^{[b]},\mathcal F_h^{[b]})
     &\le a_{1,h}(b)\eta_h, \label{eq:v55-count-simulation}\\
 0\le R_{C,h}^*(b)-R_h^*(b)&\le\tfrac12a_{1,h}(b)\eta_h.
                                      \label{eq:v55-count-risk-bound}
\end{align}
In particular the supremum over $b\ge1$ of the Le Cam distance tends
to zero.  The same reduction without a cap has bound $\eta_h$.
The simulating kernel preserves the censored count and hence the
realized preparation charge, not merely its expectation.

For sufficiently small $h$, suppress $h$ and put $p_i=p_{i,h}$, so that
$0<p_1<p_0<1$.  Define
\begin{equation}\label{eq:v55-count-threshold}
 K_b=\min\left\{b,\left\lfloor 1+
 \frac{\log(p_0/p_1)}{\log((1-p_1)/(1-p_0))}\right\rfloor\right\}.
\end{equation}
Then the exact count-only risk is
\begin{equation}\label{eq:v55-exact-count-risk}
 R_{C,h}^*(b)=\tfrac12\bigl\{(1-p_0)^{K_b}+1-(1-p_1)^{K_b}\bigr\}.
\end{equation}
Choosing either hypothesis at a likelihood tie gives the same risk.
For comparison, if $q_i$ are densities of the two terminal mark laws
with respect to a common measure $\mu$, the exact full-record risk is
\begin{equation}\label{eq:v55-full-overlap}
 R_h^*(b)=\frac12\left\{(1-p_0)^b+
 \sum_{k=1}^{b}\int
 \min\{p_0(1-p_0)^{k-1}q_0,\ p_1(1-p_1)^{k-1}q_1\}\,\dd\mu
 \right\}.
\end{equation}
Thus \eqref{eq:v55-exact-count-risk} is not asserted to be the exact
finite risk of the full record.  Bound \eqref{eq:v55-count-risk-bound}
is an absolute error bound, with no relative-error assertion for
vanishing risks.
\item At finite cap intensity, the acceptance bit already captures the
limiting experiment.  For every finite cap,
\begin{equation}\label{eq:v55-bit-simulation}
 \delta(\mathcal F_h^{[b]},\mathcal B_h^{[b]})=0,\qquad
 \delta(\mathcal B_h^{[b]},\mathcal F_h^{[b]})\le a_{1,h}(b).
\end{equation}
If $b_hp_{0,h}\to\lambda<\infty$, let $\mathcal L_\lambda$ be the
binary experiment on $\{0,1\}$ with success probability
$1-e^{-\lambda}$ under alternative zero and zero under alternative one.
Then
\begin{align}
 \Delta_{\mathrm{LC}}(\mathcal F_h^{[b_h]},\mathcal L_\lambda)
 &\le a_{1,h}(b_h)\notag\\
 &\quad+\max\{|a_{0,h}(b_h)-(1-e^{-\lambda})|,a_{1,h}(b_h)\}
 \longrightarrow0. \label{eq:v55-bit-limit}
\end{align}
This equivalence does not hold uniformly over all caps.  For example,
if $b_hp_{1,h}\to\infty$, the bit has equal-prior risk tending to
$1/2$, while the full record has risk tending to zero, and
\begin{equation}\label{eq:v55-large-cap-bit-loss}
 \delta(\mathcal B_h^{[b_h]},\mathcal F_h^{[b_h]})\longrightarrow\tfrac12.
\end{equation}
'''

ADDED_PROOF = r'''

It remains to identify the two reductions of the full stopped record.
For the count reduction, keep $k\le b$ and independently append a mark
with law $Q_{s_0,J_h,h}$; keep $\partial$ unchanged.  This is one
Markov kernel for both alternatives.  Formula
\eqref{eq:v54-stopped-factorization} shows it is exact under zero.
Under one, its accepted-count components have disjoint supports and
weights $p_{1,h}(1-p_{1,h})^{k-1}$.  Consequently its error is exactly
\[
 \sum_{k=1}^{b}p_{1,h}(1-p_{1,h})^{k-1}\eta_h
                         =a_{1,h}(b)\eta_h.
\]
Projection proves the zero deficiency in the other direction, giving
\eqref{eq:v55-count-simulation}.  For any full-record randomized test,
composition with this kernel changes its error under zero by zero and
under one by at most $a_{1,h}(b)\eta_h$.  Averaging the two errors and
taking infima gives \eqref{eq:v55-count-risk-bound}; the reverse risk
inequality follows by discarding the mark.  The bound is uniform in
$b$ since $a_{1,h}(b)\le1$ and \eqref{eq:v54-mark-distance} makes
$\eta_h\to0$.  The infinite geometric sum gives the uncapped bound.
The kernel retains $k$ and $\partial$, so the charge function, equal
to $k$ on acceptance and $b$ at $\partial$, is preserved pointwise.

For the exact finite risk, the count likelihood ratio at $k\le b$ is
\[
 \frac{p_0}{p_1}\left(\frac{1-p_0}{1-p_1}\right)^{k-1}.
\]
It strictly decreases in $k$, and the likelihood ratio at $\partial$
is $((1-p_0)/(1-p_1))^b<1$.  The largest accepted count at which the
ratio is at least one is exactly \eqref{eq:v55-count-threshold}.
The optimal rule therefore selects zero precisely on the accepted
counts $1,\ldots,K_b$.  Its two errors are $(1-p_0)^{K_b}$ and
$1-(1-p_1)^{K_b}$, proving \eqref{eq:v55-exact-count-risk}.
A tie contributes the same amount whichever decision is used.  For the
full law, use the common dominating mark measure $\mu=Q_0+Q_1$,
counting measure on $\{1,\ldots,b\}$ and an additional atom at
$\partial$.  The minimum equal-prior error is half the integral of
the pointwise minimum of the two densities.  The smaller cemetery
mass is $(1-p_0)^b$, and the other components are precisely those in
\eqref{eq:v55-full-overlap}.  This proves that identity without an
assumption that the terminal marks agree or are finitely supported.

For the bit reduction, send zero to $\partial$.  On input one, draw a
pair $(k,Y)$ from the full law under alternative zero conditional on
acceptance by $b$.  This law is defined because $a_{0,h}(b)>0$;
its weights are
$p_{0,h}(1-p_{0,h})^{k-1}/a_{0,h}(b)$, followed by the independent
zero-alternative mark.  The simulated full law is exact under zero.
Under one the cemetery mass is still exact, and the discrepancy on
the accepted part is at most its mass $a_{1,h}(b)$, proving
\eqref{eq:v55-bit-simulation}.  Notice that no small mark distance
is needed for this step.  Under $b_hp_{0,h}\to\lambda<\infty$,
the earlier calculation gives $a_{0,h}\to1-e^{-\lambda}$ and
$a_{1,h}\to0$.  The actual bit laws and the laws of
$\mathcal L_\lambda$ share a two-point space, and their maximum
total-variation distance is the maximum in
\eqref{eq:v55-bit-limit}.  Composing the stated kernels and using
contraction and the triangle inequality proves that bound in both
directions.  For $\lambda=0$ both limiting laws are the point mass
at zero; no exceptional case of the argument is needed.

Finally suppose $b_hp_{1,h}\to\infty$.  Then both bit acceptance
probabilities tend to one, so the bit pairwise distance tends to zero.
Also $b_hp_{0,h}\to\infty$; the proved cap criterion makes the full
pairwise distance tend to one.  Applying the same contraction and
triangle inequality used for \eqref{eq:v54-deficiency}, now to any
kernel from the bit experiment to the full experiment, gives the
lower limit $1/2$ in \eqref{eq:v55-large-cap-bit-loss}.  Ignoring the
bit and drawing the equal mixture of the two full laws gives the
matching upper bound.  These bit kernels describe comparison of
statistical experiments, not equality of realized physical costs:
unlike the count kernel, a bit kernel need not retain the observed
stopping time.  The deterministic budget and charge remain those in
\eqref{eq:v54-capped-charge}.
'''

OVERVIEW = r'''
The stopped-record conclusion has a precise reduction within this same
pair.  Censored waiting counts are asymptotically sufficient uniformly
over deterministic caps, with an explicit absolute risk error and an
exact count-likelihood threshold.  At finite cap intensity the full
record converges, in Le Cam distance, to a Bernoulli experiment; at much
larger caps the acceptance bit can lose all discrimination while the
count remains informative.  These reductions are proved in
Theorem~\ref{thm:v54-waiting-and-cap}.  They identify the retained mass,
rather than the terminal interaction, as the source of stopped
separation.  They do not identify the stopped experiment with the
conditional-law inverse or supply a sensor-independent preparation bound.
'''

BIBLIOGRAPHY = r'''
\bibitem{A2ReviewV54First}
\emph{Independent referee report on A2, revision 54},
author-requested AI-assisted memorandum, September 15, 2026, Section 5.
\href{https://github.com/TrillionniumFoundation/theta-theory/blob/1030ca91a96ca1be8ecd0347ecbdac7084cdd8d4/reviews/a2-v54-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md}{Frozen first v54 memorandum}.
Cited for the count and bit reductions and the finite count-risk formula;
not a commissioned journal evaluation.

\bibitem{A2ReviewV54Second}
\emph{Second independent referee memorandum on A2, revision 54},
author-requested AI-assisted memorandum, September 15, 2026, Section 4.
\href{https://github.com/TrillionniumFoundation/theta-theory/blob/67250d08714acf76274e82158f107246f0de7eee/reviews/a2-v54-second-referee-top4-2026-09-15/REFEREE_REPORT.md}{Frozen second v54 memorandum}.
Records an overlapping stopped-count comparison and its finite checks;
not a commissioned journal evaluation or a separate priority claim.

'''


def replace_once(text: str, old: str, new: str) -> str:
    require(text.count(old)==1, 'Unexpected edit anchor: '+old[:100])
    return text.replace(old,new,1)


def waiting_blocks(text: str) -> tuple[str,str]:
    start=text.index(r'\begin{theorem}[Accepted marks and charged first-acceptance records]')
    end=text.index(r'\end{theorem}',start)+len(r'\end{theorem}')
    a=text.index(r'\begin{proof}',end)
    b=text.index(r'\end{proof}',a)+len(r'\end{proof}')
    return text[start:end],text[a:b]


def revised(name: str, text: str) -> str:
    if name==MODULE:
        old_statement,old_proof=waiting_blocks(text)
        statement=replace_once(old_statement,r'\end{enumerate}',ADDED_ITEMS+r'\end{enumerate}')
        proof=replace_once(old_proof,r'\end{proof}',ADDED_PROOF+'\n'+r'\end{proof}')
        text=replace_once(text,old_statement,DEFINITIONS+'\n'+statement)
        return replace_once(text,old_proof,proof)
    if name==INTRO:
        anchor='actual nonlinear actions, not stipulated quadratic functions.\n'
        return replace_once(text,anchor,anchor+OVERVIEW)
    if name=='v5/references_v43.tex':
        return replace_once(text,r'\end{thebibliography}',BIBLIOGRAPHY+r'\end{thebibliography}')
    require(name=='main.tex','Unknown amended file')
    text=text.replace('A2 revision 54','A2 revision 55')
    before='''comparison.  Retaining the first waiting count yields reverse binary deficiency
$1/2$ in the limit; deterministic caps have an explicit limiting risk.'''
    after='''comparison.  Retaining the first waiting count yields reverse binary deficiency
$1/2$ in the limit.  Under deterministic caps, censored counts are
asymptotically sufficient uniformly over the cap, with an exact count-risk
formula and a Bernoulli limit at finite acceptance intensity.'''
    text=replace_once(text,before,after)
    anchor='in~\\cite{A2ReviewV53}; the deterministic-cap risk is proved here.\n'
    return replace_once(text,anchor,anchor+r'''The stopped-count and finite-intensity bit reductions, and the count-risk
formula incorporated in the same theorem, were communicated in the two
v54 memoranda~\cite{A2ReviewV54First,A2ReviewV54Second}; their overlap
is acknowledged rather than counted as two independent contributions.
''')


def materialize() -> dict:
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    manifest_path=ARCHIVE/'active-source-manifest.json'
    if not manifest_path.exists():
        original=P.parents[1]/'deliveries/a2-v54'/SOURCE_V54/'active-source-manifest.json'
        require(original.is_file(),'Missing v54 native manifest')
        manifest_path.write_bytes(original.read_bytes())
    groups=json.loads(manifest_path.read_text())
    old={name:info for group in groups.values() for name,info in group.items()}
    require(len(old)==111,'Unexpected v54 active-source count')
    for name,info in old.items():
        archived=ARCHIVE/name
        baseline=archived if name in CHANGES and archived.exists() else P/name
        data=baseline.read_bytes()
        require(hashlib.sha256(data).hexdigest()==info['sha256'],'Unexpected baseline: '+name)
        if name in CHANGES:
            if not archived.exists():
                archived.parent.mkdir(parents=True,exist_ok=True)
                archived.write_bytes(data)
            expected=revised(name,data.decode())
            require((P/name).read_text() in (data.decode(),expected),'Nonprescribed edit: '+name)
            (P/name).write_text(expected)
    return {'baseline_source':SOURCE_V54,'review_heads':[REVIEW_FIRST,REVIEW_LATEST],
        'archived_exact_originals':list(CHANGES),'active_inputs':len(old),
        'expanded_existing_statement':'thm:v54-waiting-and-cap',
        'new_theorem_environments':0,'mathematical_certification':False}

if __name__=='__main__':
    print(json.dumps(materialize(),indent=2,sort_keys=True))
