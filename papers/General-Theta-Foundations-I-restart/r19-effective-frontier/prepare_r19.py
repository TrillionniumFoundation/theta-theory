#!/usr/bin/env python3
"""Reproduce R19 ordinary source from immutable R18 and explicit new source files.
This is a deterministic editorial transform, not an external build dependency.
No existing R18 source or historical branch is modified.
"""
from __future__ import annotations
import hashlib,json,importlib.util,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'r18-causal-allocation'
OLD_TREE='2ae0b903d0a621eeec3525e8e143b12ec609cd83'
sys.dont_write_bytecode=True
from revision_additions import OPERATIONAL,FINITE_EXAMPLE,OBSTRUCTION_NOTE

def old(name):return (OLD/name).read_text()
def put(name,text):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def replace(text,a,b):
    if a not in text:raise RuntimeError('editorial anchor missing: '+a[:90])
    return text.replace(a,b)
def main():
    spec=importlib.util.spec_from_file_location('r18_verify',OLD/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    if v.verify()['native_source_tree_sha']!=OLD_TREE:raise RuntimeError('R18 source binding changed')
    abstract=r'''Which finite predictive laws can an observer acquire, retain and execute? On compact affine predictive carriers derived from prepared experimental kernels, we characterize the exact causal risk frontier by barycentric allocation under the deployed law and by a simultaneous dual enforcing one stationary programme. We then prove an effective completion of this invariant for support-resolved positive instruments. At a fixed horizon and fixed total label budget, finite dyadic programmes give convergent, certified upper and lower risk bounds uniform over all Borel controllers; the report and probability resolutions and the number of candidates are explicit. Common report reconstruction and support-preserving rounding retain legal actions, programme reuse and exact stopping without a normalized-filter contraction hypothesis. Untruncated Gaussian experiments with possibly nonmixing transitions and noncommuting finite-dimensional instruments, including unitary evolution and pure states, verify the same theorem. Singular reference laws, atomic tails and flagged rank changes are included. A finite experiment has a sharp three-, four- and five-state risk threshold determined by the simultaneous constraint. The general exact criterion remains non-effective without the additional presentation, and the finite search need not be efficient. Matching regular and singular resource laws, common-task simulation and separate numerical and computation accounts complete the transfer from actual acquired geometry to decision risk.'''
    text=old('main.tex');text=re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda m:'\\begin{abstract}\n'+abstract+'\n\\end{abstract}',text,flags=re.S)
    text=text.replace('convex order, finite-state observer, acquired geometry, quantum instrument','convex order, finite-state observer, effective synthesis, acquired geometry, quantum instrument')
    text=replace(text,r'\input{sections/06_geometry}',r'\input{sections/06_effective}'+'\n'+r'\input{sections/07_effective_realizations}'+'\n'+r'\input{sections/06_geometry}')
    put('main.tex',text)
    intro=r'''\section{Introduction}\label{sec:introduction}
A prepared experiment does not supply its observer with a parameter manifold. It supplies legal actions, reports and executable future tests. Past histories are equivalent when those tests cannot distinguish their continuations. Even after this predictive quotient has been realized, its formal size does not determine what a causal observer can retain: the distribution available for compression is created by the observer's own acquisition policy. A finite label subsequently changes that policy and hence changes the next available distribution. The mathematical problem is to characterize this feedback constraint and to determine when its optimal risk can actually be approximated by a finite programme.

There are two distinct obstructions. First, a terminal codebook need not admit intermediate causal updates. Second, separately feasible updates at different phases need not be updates of one stationary programme. Conditional predictive states attached to a reused label may differ with phase as law parameters, but the executed rule may read neither those states nor an uncharged clock. A third issue appears once existence is settled: a Borel report-to-label kernel may require an infinite description. A finite cardinality theorem is not yet an effective finite-resource theorem.

Theorem~\ref{thm:completion} gives an exact allocation invariant and its effective completion. Its first four parts identify feasible retained laws by finite-support barycentric contractions of actual acquisition laws and identify stationary compatibility by one simultaneous affine inequality. The maximum is taken after summing the phase contributions. This eliminates the unknown common report-to-label kernel, but not the law-valued trajectory of occupancies and conditional predictive states. The exact action-slack and pooling-loss identity yields the optimal same-task risk. These exact allocation arguments are retained and re-proved here. Their one-step convex-order ingredient is classical\cite{strassen,leskela}; the serial and stationary compatibility constraints are the additional content.

The effective part is the principal new step. For positive finite-dimensional raw instruments having the support-resolved presentation of Definition~\ref{def:effective}, it yields an interval
\[
 l-E_h-\beta_Q\le B_n^*+\Phi_{\aut}(n,M)\le u,
 \qquad u-l\le\eta,
\]
computed from at most $M2^M K_\rho^M(Q+1)^{MA+M^2\sum_a B_a}$ programmes. Every candidate uses at most the original $M$ labels, including its actions, timing and stopping state. Its rows are shared across phases exactly as the information pattern requires. The error $E_h$ is a complete-law instrument error; $\beta_Q$ separately accounts for probability-row and terminal-decision resolution. The supplied bounds make the interval effectively convergent. In particular, it gives certified lower bounds for \emph{all} Borel programmes, not only upper bounds for a chosen quantization or an enumeration of promising controllers. The external-clock statement is separate and does not charge phase states.

The proof first replaces reports by a common finite partition while retaining their actual cell instruments. A reconstruction measure independent of phase and state averages each old report row into one new common row. Positivity controls the joint physical-state/label error without differentiating a normalized posterior update. A support certificate makes the fine and coarse programmes have the same possible finite paths. Dyadic rounding removes, but never creates, supported edges; thus it retains exact legality and the deadline. Finite enumeration with certified integration then brackets the optimum. Its candidate bound may be very large. It is a value-computation and feasible-execution theorem, not a polynomial-time algorithm or an optimal description-length result.

Theorems~\ref{thm:effective_gaussian} and~\ref{thm:effective_quantum} verify these hypotheses directly for Gaussian hidden-state observations and positive noncommuting instruments. The former permits reducible or deterministic transitions; the latter permits unitary channels and pure states. Neither requires normalized-filter contraction. Proposition~\ref{prop:effective_singular} supplies effective Cantor and atomic-tail refinements and a rank-changing acquired law with its actual masses. These results do not turn the physical hidden or quantum state into a free controller register. The effective presentation, rather than a presumed Fisher or covariance geometry, is checked at the raw kernel.

For accessibility, Theorem~\ref{thm:finite_reuse} solves a complete finite stationary-reuse problem: three labels give risk $1/2$, four give $1/4$, and five give zero. The nontrivial feasible parallelogram and an implementing common kernel are explicit. This example isolates the simultaneous constraint; it is not presented as the resolution of a long-standing filtering problem.

The quantitative geometric theory remains essential. Theorem~\ref{thm:regular} estimates the exact frontier using actual mass, global covering, task curvature and block stability, and gives matching externally timed and internally timed risk curves. Theorem~\ref{thm:blind} gives a different exact curve for noncontracting singular acquisition, controlled by the narrowest intermediate alphabet. These inherited results are re-proved, rather than promoted again as new contributions. Programme bits, scratch, numerical error and parameter-independent simulation appear with explicit certificates in Sections~\ref{sec:effective} and~\ref{sec:resources}. The full-history baseline always belongs to the same horizon, preparation and scored task; a Bayes preparation is not a parameter-uniform minimax theorem.

Finite-state-controller synthesis and observation quantization are established subjects\cite{poupart,junges,continuous}. Our distinction is a certified approximation of the \emph{fixed-cardinality} causal frontier, preserving one whole stationary programme and its exact support constraints. The comparison in Section~\ref{sec:literature} explains both the overlap and the limits. The compact exact theorem alone has no universal effective modulus; the effective theorem assumes known kernels, finite-dimensional positive instruments, support data and computation certificates. Unknown-kernel learning, arbitrary noncompact predictive quotients, infinite horizons and a matched optimum for every computational resource are not claimed. The manuscript's subject remains the general passage from prepared experiments to predictive quotients, actual acquired geometry, executable causal morphisms and finite-resource decision risk.
'''
    put('sections/01_introduction.tex',intro)
    text=old('sections/02_experiments.tex')
    anchor=r'\end{definition}'
    text=text.replace(anchor,anchor+r'''
A reused autonomous label has one action distribution supported in the intersection of all phase-legal action sets at which it has positive occupancy. The common report space is indexed by action, not by an unread phase. Programme cardinality here bounds labels only; a general Borel rule need not have a finite-bit description. Theorem~\ref{thm:effective} supplies one effective specialization.
''',1)
    put('sections/02_experiments.tex',text+OPERATIONAL)
    text=old('sections/03_completion.tex')
    text=text.replace('Causal allocation and exact resource--risk frontier','Causal acquired geometry and exact/effective resource transfer',1)
    # Keep the exact theorem and add its effective part without altering its hypotheses silently.
    end=text.index(r'\end{theorem}')
    addition=r'''
\medskip\noindent\textup{(e) Effective completion.} For the additional support-resolved effective presentation of Definition~\ref{def:effective}, the exact optimal value in \textup{(c)} admits the certified finite intervals \eqref{eq:effective_interval}, with the candidate bound \eqref{eq:programme_count}. They are uniform over every legal Borel programme of the fixed cardinality. The minimizing listed programme is executable at that same cardinality, with separately charged cell access, readout, probability precision, scratch and programme costs. This effective assertion does not apply to arbitrary compact Borel presentations merely by compactness. Its proof is Theorem~\ref{thm:effective}.
'''
    text=text[:end]+addition+text[end:]
    text=text.replace('The theorem does not assume a density, a stable update, finite-dimensional closure, or full task curvature.', 'Parts (a)--(d) do not assume a density, a stable update, finite-dimensional closure, or full task curvature. Part (e) has the additional effective positive-instrument presentation stated there.')
    text+=r'''
The affine components in the displayed duals are continuous functions on the predictive carrier. Lemma~\ref{lem:operational_tests} identifies their precise relation to executable tests and uniform test-span limits. The finite family of maxima in a global obstruction is not generally one scored continuation. The dominating measure $\eta_{z,a}$ is a finite measure of aggregate occupancy-action mass $\sum_t p_{t,z}\alpha_z(a)$; it need not be a probability or even have mass at most one. The same action-indexed report space makes its shared row well-typed across phases.
'''
    put('sections/03_completion.tex',text)
    text=old('sections/04_allocation_proof.tex')
    text+=OBSTRUCTION_NOTE
    text+=r'''
For clarity, the candidate space in the compactness argument may be written using $\gamma_t\in\cP(K_t\times\mathcal A_t)$ with first marginal $\nu_t$ supported on at most $m_t$ points, initial $\nu_0=\delta_{q_0}$, and $\lambda_{t+1}=\int\Lambda_t(q,a)\gamma_t(dq,da)$. If $h_i$ enumerates the convex test family, its $k$th closed candidate subset imposes
\[
 \int h_i\,d\nu_{t+1}\le\int h_i\,d\lambda_{t+1}
 \quad (t<n,\ i\le k),\qquad
 c_k=\min\left\{\int g\,d\nu_n:\gamma\text{ in that subset}\right\}.
\]
All finite atoms and action weights are chosen jointly for this fixed experiment. No measurable dependence of an optimizer on an external model parameter is asserted. The moment-image topology is the product of the real mass and affine-coordinate lines, so a continuous linear separator depends on finitely many coordinates. Completed-probability measurable allocation functions have Borel versions on the standard-Borel carrier, with values on null sets completed arbitrarily.
'''
    put('sections/04_allocation_proof.tex',text)
    text=old('sections/05_stationary.tex')
    marker=r'\begin{proposition}'
    at=text.index(marker)
    text=text[:at]+FINITE_EXAMPLE+'\n'+text[at:]
    text+=r'''
In the reference-trace argument, every action with positive probability at a reused label is legal at both occurrences by the occupancy legality constraint. Equivalence of trace null sets is not a uniform likelihood-ratio estimate; no such stronger bound is used.
'''
    put('sections/05_stationary.tex',text)
    text=old('sections/06_geometry.tex').replace(r'\kappa_f',r'\mu_f')
    text=text.replace(r'\section{',r'\section{',1)
    text+=r'''
The ambient Euclidean chart in the curvature estimate is the finite-dimensional affine span of $K$; the chosen predictive norm is compared to its Euclidean norm with fixed constants. The curvature measure $\mu_f$ is distinct from the task's strong-concavity constant $\kappa$. In Theorem~\ref{thm:regular}, $B_n^*$ remains horizon- and task-dependent. Uniformity in $n$ concerns the excess constants, not a common stationary learning curve across different terminal tasks. Optimization over adaptive acquisitions is within the known-kernel, finite-action, phase-legal interface and its uniform hypotheses.
'''
    put('sections/06_geometry.tex',text)
    text=old('sections/07_realizations.tex')
    text+=r'''
In the Gaussian realization the operative nondegeneracy is $\operatorname{rank}B_a=d$, including when the observation dimension is larger than $d$. The invertible legal transition used to separate predictive states may depend on phase; action availability belongs to the phase-specific predictive interface and is not a clock that an autonomous programme may read.

For the quantum inverse, one can see the full differential directly. With $K=(q^{1/2}\sigma q^{1/2})^{1/2}$, a variation $H$ of $\sigma$ induces the unique solution $X$ of $KX+XK=q^{1/2}Hq^{1/2}$ and $\dot A=q^{-1/2}Xq^{-1/2}$. Differentiating $E=DA^2/\tr(A^2)$ gives
\[
 \dot E=D\left(\frac{A\dot A+\dot A A}{\tr(A^2)}
       -\frac{2A^2\tr(A\dot A)}{\tr(A^2)^2}\right).
\]
Thus the smooth inverse and compact positive domain give the asserted nonsingular Jacobian bound. This calculation is finite-dimensional; it makes no claim about unbounded-operator closures.
'''
    put('sections/07_realizations.tex',text)
    text=old('sections/08_singular.tex')
    text+=r'''
In Theorem~\ref{thm:blind}, $m_n$ counts terminal stopping/readout labels and the decision may be issued immediately upon entering one. The post-decision audit cannot break the cut Markov relation $X-Z_t-U$. In the accumulating-atom lower bound, absence of a center from the selected interval means that every center is at distance at least $x_j/8$ from its atom; this gives exactly the asserted single-atom contribution.
'''
    put('sections/08_singular.tex',text)
    text=old('sections/09_resources.tex')
    text=replace(text,'The general continuous-instrument results do not inherit this finite rational decidability. Conversely, the finite theorem does not replace the main compact-carrier criterion by an enumeration of one special model.',r'''Arbitrary compact Borel instruments do not inherit finite rational decidability. Theorem~\ref{thm:effective} instead gives effective value approximation for its separately certified continuous-instrument class. Signs and zero tests of algebraic row probabilities are decidable, so the support used in the finite rational rounding can be identified. Only paths up to the fixed horizon are enumerated; no infinite-horizon recurrence constraint is solved. Bounded finite-state-controller parameter synthesis predates this compilation result\cite{junges,poupart}; the additional execution statement here preserves support, legality and deadline at the declared budget.''')
    put('sections/09_resources.tex',text)
    # Preserve the full raw quotient proof.
    put('sections/11_quotient.tex',old('sections/11_quotient.tex'))
    for name in ('sections/03_completion.tex','sections/04_allocation_proof.tex'):
        text=(ROOT/name).read_text().replace('A_t+J_t',r'A_t+\mathscr J_t').replace('J_t&=',r'\mathscr J_t&=').replace('=J_t\\ge0',r'=\mathscr J_t\ge0').replace('A_t=J_t=0',r'A_t=\mathscr J_t=0')
        # The proof occasionally writes the term at the end of a display.
        text=text.replace('=J_t.',r'=\mathscr J_t.').replace('=J_t\n',r'=\mathscr J_t'+'\n')
        put(name,text)
    put('verify.py',old('verify.py'))
    put('native_build.py',old('native_build.py').replace('R18','R19').replace('r18','r19'))
    # The new build/regression and audit sources are supplied explicitly, never generated from a remote mutable branch.
    from revision_documents import write_documents,write_literature
    write_documents(ROOT);write_literature(ROOT,OLD)
    # Self-contained manifest over the generated ordinary manuscript, scripts and audits.
    spec=importlib.util.spec_from_file_location('new_verify',ROOT/'verify.py');nv=importlib.util.module_from_spec(spec);spec.loader.exec_module(nv)
    files={n:{'sha256':nv.sha256((ROOT/n).read_bytes()),'git_blob_sha':nv.git_hash('blob',(ROOT/n).read_bytes())} for n in nv.sources(ROOT)}
    put('SOURCE_MANIFEST.json',json.dumps({'format':'ordinary-source-manifest-v1','files':files},sort_keys=True,indent=2)+'\n')
    print(json.dumps(nv.verify(ROOT),sort_keys=True,indent=2))
if __name__=='__main__':main()
