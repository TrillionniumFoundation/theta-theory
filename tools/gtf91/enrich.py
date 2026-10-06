#!/usr/bin/env python3
"""Complete the general comparison before freezing the v91 native source."""
from pathlib import Path
import json
import re

root=Path('papers/GTF-I-v91-reset-variational')
name='sections/83-reset-variational-principle.tex'
s=(root/name).read_text()
anchor='\\subsection{The unrestricted causal normalization}\n'
if s.count(anchor)!=1:raise RuntimeError('missing causal-normalization insertion anchor')
addition=r'''\subsection{A geometric criterion for retained receiver advantage}
Let $\mathcal P_{d_1}$ be the rank-one density matrices.  In parallel
with \eqref{eq:roof91}, define
\begin{equation}\label{eq:pureroot91}
 c_y^{\rm cl}(\rho)=\sup\left\{\sum_h\lambda_h g_y(a_h):
 a_h\in\mathcal P_{d_1},\quad
 \lambda_h\ge0,\quad\sum_h\lambda_h a_h=\rho\right\}.
\end{equation}
The weights sum to one by taking traces.  Every density matrix admits
such a decomposition, but the value of this pure-atom envelope need
not equal the all-density envelope $c_y$.

\begin{theorem}[Classical and quantum receiver envelopes]
\label{thm:classicalroof91}
For every finite experiment of Definition~\ref{def:classes91},
\begin{equation}\label{eq:classicalroof91}
 P_{\rm ca}=\max_{\rho\in\mathcal D_{d_1}}\sum_yc_y^{\rm cl}(\rho)
 =\min_{(H_y)}\lambda_{\max}\left(\sum_yH_y\right),
 \qquad \tr(H_ya)\ge g_y(a)\quad(a\in\mathcal P_{d_1}).
\end{equation}
Both optima are attained.  At most
$(\operatorname{rank}\rho)^2$ nonzero first-receiver outcomes per
first device label suffice at an optimal $\rho$.
The passage from complete classical readout to retained quantum
receiver memory replaces the pure-atom envelopes $c_y^{\rm cl}$ by
the all-density envelopes $c_y$.  In particular, the invariant
\begin{equation}\label{eq:receivergap91}
 \Gamma=\max_\rho\sum_yc_y(\rho)
          -\max_\rho\sum_yc_y^{\rm cl}(\rho)
\end{equation}
is exactly the optimal retained-receiver advantage in that experiment.
\end{theorem}
\begin{proof}
After complete first readout, a classical branch has a positive input
Gram effect $A$ and retains no quantum system depending on $\theta$.
Its probability under a first effect is $\tr(AE_y^{\mathsf T})$.
Refine a spectral decomposition $A=\sum_i\lambda_i a_i$ into the
classical record and keep the former second preparation and decision
on each refined branch.  This does not change the score and gives a
rank-one decomposition with the same barycenter.  Optimizing the
second action separately after the refined record can only increase it.

Conversely, for a rank-one atom $a=|u\rangle\langle u|$, the old
receiver in the canonical normal form has
\[
 \sqrt a E_y^{\mathsf T}\sqrt a
 =\langle u,E_y^{\mathsf T}u\rangle a.
\]
Its normalized state is independent of the unknown device.  A joint
POVM with this known factor is equivalent to a POVM on the fresh
reference alone, by taking its expectation against $a$.
Thus $g_y(a)$ is attainable with only a classical first record.
The converse part of Lemma~\ref{lem:resetnormal91}, followed by discarding
this known old state, realizes every finite pure-atom decomposition.
These two observations give the first equality in
\eqref{eq:classicalroof91}.

The graph of $g_y$ on the compact pure-state set is compact.  The
compact-convex-hull and rank-face atom-elimination arguments of
Theorem~\ref{thm:resetvariational91} therefore apply verbatim, giving
attainment and the stated branch count.  Its homogeneous hypograph is
again a closed convex cone, with a strictly feasible point at a
positive definite common barycenter and negative heights.  The proof
of Theorem~\ref{thm:resetdual91} applies with majorization required only
on pure atoms and gives the attained dual.  Majorization on pure atoms
is equivalent to majorization of $c_y^{\rm cl}$ on every density matrix,
not to majorization of $g_y$ on every density matrix.  The last assertion
now follows from the two exact primal formulas.
\end{proof}

\begin{corollary}[Complete separation certificates]\label{cor:gapcertificate91}
There is a strict retained-receiver advantage if and only if there exist
a finite feasible reset collection from \eqref{eq:resetvariational91},
with achieved reward $v$, and Hermitian matrices $H_y$ such that
\[
 \tr(H_ya)\ge g_y(a)\quad(a\in\mathcal P_{d_1}),\qquad
 v>\lambda_{\max}\left(\sum_yH_y\right).
\]
There is no advantage if and only if an attaining classical strategy
has contact and spectral equality with an all-density dual majorant
of Theorem~\ref{thm:resetdual91}.
\end{corollary}
\begin{proof}
The displayed inequalities compare a physically attained reset lower
with a valid classical upper.  If the gap is positive, take an optimal
finite reset collection and an optimal classical dual, whose existence
was proved above.  This proves both directions of the first assertion.
If the gap is zero, an optimal classical strategy also attains the reset
value; complementarity with any attained reset dual gives the second
condition.  Conversely, that condition certifies a common upper and
lower for the two classes, so their values agree.
\end{proof}
These are certificates with finitely many matrix variables and universal
majorization requirements, not finite-sampling tests.  The criterion
applies to any fixed-pair problem as well as to ensemble decisions,
but does not require every experiment to have positive $\Gamma$.
For example, the equal-prior qubit calculation below gives pure-atom
majorants $H_0=H_1=(7/24)I$, whereas a reset strategy attains $5/8$.
The gap is $1/24$.  Its universal pure-atom majorization follows from
the classical upper in Theorem~\ref{thm:equalprior91}, not from the
finite arithmetic regression.

'''
(root/name).write_text(s.replace(anchor,addition+anchor,1))

# Bounds concern retained registers, not ancillary workspaces of a chosen
# gate decomposition for the allowed instrument operations.
s=(root/name).read_text().replace(
 'These assertions include arbitrary priors and arbitrary fixed\npairs as particular decision problems;',
 'The dimension bounds concern the retained registers at the recording\ncuts, not temporary workspaces for implementing an instrument.\nThese assertions include arbitrary priors and arbitrary fixed\npairs as particular decision problems;')
s=s.replace('\\cite[Section~5.2.3]{BV91}', '\\cite[Sections~5.2.3 and~5.9.1]{BV91}')
(root/name).write_text(s)

labels=[]
for f in ('sections/83-reset-variational-principle.tex','sections/84-equal-prior-memory-hierarchy.tex'):
    labels+=re.findall(r'\\label\{((?:thm|lem|prop|cor):[^}]+)\}',(root/f).read_text())
code=(root/'build_revision.py').read_text()
code=re.sub(r'NEW_LABELS=.*\n','NEW_LABELS='+repr(labels)+'\n',code,count=1)
(root/'build_revision.py').write_text(code)
status=json.loads((root/'PROOF_STATUS.json').read_text())
status['new_labels']=labels
status['new_claims'].update(classical_pure_atom_variational_value=True,
    necessary_sufficient_retained_receiver_gap_certificate=True,
    retained_register_bound_is_temporary_workspace_bound=False)
(root/'PROOF_STATUS.json').write_text(json.dumps(status,indent=2,sort_keys=True)+'\n')

intro=root/'editions/operational-introduction91.tex'
s=intro.read_text()
anchor='These statements share one operational interface'
paragraph=r'''Theorem~\ref{thm:classicalroof91} identifies the classical optimum by
restricting the envelope atoms to pure states.  Thus two explicit
convexifications distinguish complete classical readout from quantum
receiver storage in every finite experiment.
Corollary~\ref{cor:gapcertificate91} gives necessary and sufficient
primal--dual certificates for a strict gap, and contact certificates
for equality.  Their majorization inequalities are universal; no
sampling procedure is asserted to certify them.

'''
if s.count(anchor)!=1:raise RuntimeError('missing conceptual-bridge anchor')
intro.write_text(s.replace(anchor,paragraph+anchor,1))
abstract=root/'quantitative.tex'
s=abstract.read_text().replace('These results require neither a symmetric ensemble nor a special prior.',
 'Pure-atom envelopes give the classical optimum and necessary and\nsufficient certificates of retained-receiver advantage.\nThese results require neither a symmetric ensemble nor a special prior.')
abstract.write_text(s)

note='''\n\n## General classical-versus-quantum receiver criterion\n\nPrimary Section 15 additionally proves Theorem `classicalroof91`: complete classical readout is exactly the same common-barycenter problem with atoms restricted to rank-one density matrices. A complete first measurement can be spectrally refined without loss, and a rank-one Gram factor carries only a known receiver state; these give both operational directions. Compact graph convexification and the same strictly feasible hypograph dual give attained classical primal and dual optima. Corollary `gapcertificate91` then gives necessary and sufficient certificates of a strict retained-receiver advantage, and all-density dual contacts characterize equality. This extends the R60 breadth response to an exact general comparison criterion, not merely an evaluated example.\n\nThe finite receiver dimensions refer to retained registers at the recording cuts, not to all temporary workspaces of a selected implementation of an instrument. The dual majorizations remain universal requirements and are not checked by sampling.\n'''
for f in ('README.md','RESPONSE_TO_REFEREE.md','PROOF_AUDIT.md',
          'HISTORY_AND_PIPELINE_AUDIT.md','INTERNAL_MATHEMATICAL_REVIEW.md',
          'INDEPENDENT_REVIEW_BRIEF.md','PIPELINE_DERIVATION_V91.md'):
    p=root/f;p.write_text(p.read_text()+note)
print(json.dumps({'status':'success','new_labels':labels,'general_classical_comparison':True},sort_keys=True))
