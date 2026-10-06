#!/usr/bin/env python3
"""Assemble v91 from the qualified v90 tree, without editing another paper."""
from pathlib import Path
import argparse
import importlib.util
import json
import re
import shutil

p=argparse.ArgumentParser()
p.add_argument('--source',default='papers/GTF-I-v90-operational-memory')
p.add_argument('--dest',default='papers/GTF-I-v91-reset-variational')
p.add_argument('--reports',default='/tmp/gtf91-reports')
a=p.parse_args()
src=Path(a.source).resolve(); dst=Path(a.dest).resolve()
patch=Path(__file__).resolve().parent/'patch'
if dst.exists():raise RuntimeError('refusing to overwrite an existing native revision')
spec=importlib.util.spec_from_file_location('v90_build',src/'build_revision.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
inv=b.sources(src)
b.require(inv==json.loads((src/'evidence/SOURCE_HASHES.json').read_text()),'v90 native inventory differs')
for name in inv:
    target=dst/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src/name,target)
baseline={'commit':'906e6e12841816f07e4ca31137690fd18bb65853','files':inv,'graphs':{}}
for entry in b.DOCS:
    files,labels=b.graph(src,entry)
    baseline['graphs'][entry]={'files':sorted(files),'labels':sorted(labels)}

def put(name,text):
    path=dst/name
    if name in inv and path.read_text()!=text:
        old=dst/'predecessor-v90-audit'/name
        if not old.exists():old.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,old)
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)

def insert(name,anchor,addition):
    text=(dst/name).read_text();b.require(text.count(anchor)==1,'ambiguous insertion anchor: '+anchor[:80])
    put(name,text.replace(anchor,anchor+addition,1));edited.setdefault(name,[]).append(addition)

b.put(dst/'V90_BASELINE.json',baseline)
for f in sorted(patch.rglob('*')):
    if f.is_file() and f.name!='revision-documents.json':
        text=f.read_text()
        # The exactly enumerated scalar test has value 63/80, not 33/40.
        if f.name=='reset_variational_check.py':text=text.replace('s.Rational(33,40)','s.Rational(63,80)')
        put(f.relative_to(patch).as_posix(),text)
for name,text in json.loads((patch/'revision-documents.json').read_text()).items():put(name,text)
for name in ('FROZEN_R60_REPORT.md','FROZEN_R60_PIPELINE_AUDIT.md'):
    put(name,(Path(a.reports)/name).read_text())
edited={}
section='sections/82-operational-memory-hierarchy.tex'
insert(section,'weights $w_b$ summing to one.  We require\n',r'''The weights are real; rational or algebraic coordinates are not required
by the theorem.  We call this a weighted exact second-moment family,
not necessarily an unweighted projective design.
''')
insert(section,'Early stopping is allowed and can be implemented by a discarded fresh call.\n',r'''The three closed optimization classes are precisely those of
Definition~\ref{def:classes91}.  Lemma~\ref{lem:resetnormal91} gives
the full branch normal form, and Proposition~\ref{prop:causalnormal91}
gives the physical causal normalization independently of this example.
''')
insert(section,'\\begin{theorem}[Exact two-call hierarchy]\\label{thm:operationalhierarchy90}\n',r'''The alternative basis index in this experiment is drawn once and
reused at both calls.  Independently redrawing it instead gives the
scalar product channel and no improvement over the larger prior.
''')
insert(section,'For $t>0$ both inequalities are strict.  ',r'''At $t=0$ all three
values are $1/2$.  The priors sum to one and
$p_E-p_C=t^2/L$, so $p_E$ is the constant-decision baseline.
''')
insert(section,'factors.\n\\end{proof}\n',r'''The normalized equality statement and its singular case are expanded
in the proof of Lemma~\ref{lem:centeredswap91}: normalized fidelity one
forces equality of the two density matrices, and eigenvalue
Cauchy--Schwarz then forces all $d$ eigenvalues to be $1/d$.
''')
insert(section,'These are conditional norm estimates, not physical calibration claims.\n',r'''In the preceding corollary the same $\delta$ bounds the scalar channel
and each entire basis measurement channel individually.  Priors and the
once-drawn-index law stay fixed; index-dependent channel perturbations
are permitted.  Corollary~\ref{cor:gamestability91} additionally treats
prior and law perturbations, with the unhalved norm factors explicit.
''')
b.put(dst/'EDITORIAL_INSERTIONS_V91.json',{'schema':'gtf91.editorial-insertions/1','insertions':edited})

sec83='sections/83-reset-variational-principle'
sec84='sections/84-equal-prior-memory-hierarchy'
for entry in ('main.tex','quantitative.tex'):
    text=(dst/entry).read_text()
    text=text.replace('\\input{sections/82-operational-memory-hierarchy}',
        '\\input{'+sec83+'}\n\\input{sections/82-operational-memory-hierarchy}\n\\input{'+sec84+'}')
    if entry=='main.tex':
        text=text.replace('\\input{editions/bibliography-addendum90}',
            '\\input{editions/bibliography-addendum90}\n\\input{editions/bibliography-addendum91}')
        text=text.replace('\\end{abstract}',r'''For arbitrary finite two-call measurement decision experiments we further
prove an attained reset variational principle, a finite receiver and
branch bound, and exact dual majorization certificates.  The same finite
basis family has a strict three-class hierarchy also at equal hypothesis
priors, with an explicit open perturbation neighborhood.
\end{abstract}''')
    else:
        text=text.replace('operational-introduction90','operational-introduction91').replace('current-comparison90','current-comparison91').replace('bibliography90','bibliography91')
        lo=text.index('\\begin{abstract}');hi=text.index('\\end{abstract}',lo)+len('\\end{abstract}')
        abstract=r'''\begin{abstract}
We study ordered quantum measurements with separate acquisition and
receiver resources.  For arbitrary finite two-call decision experiments,
we express the optimal unit-reset value as a concave-envelope problem
on density matrices with a common barycenter.  The optimum is attained
with at most $d_1^2$ receiver-instrument outcomes per first label and
quantum receiver dimension $d_1d_2$.  An exact dual gives majorization
and contact certificates and identifies the effect of receiver feedback.
These results require neither a symmetric ensemble nor a special prior.
We then solve a finite basis-measurement experiment in every dimension
with equal hypothesis priors.  Complete measure-and-reprepare adaptation,
unit-reset receiver storage and unrestricted two-call acquisition have
respective optimal successes $1/2+t^2(d-1)/(2d(d+1))$,
$1/2+t^2(d-1)/(2d^2)$ and $1/2+t^2/(2d)$.
A centered filtered-swap inequality bounds the entire reset class;
explicit strategies attain all three values.  The hierarchy persists
under full-rank deformation and small changes of channels, priors and
the shared latent law.  We retain the complementary local geometric
classification: in a fixed quadratic tangent tube, an allocation with
$N=\sum n_r$ and $V=\sum n_r^2$ has trace orders
$\min\{1,\sqrt Ns\}$, $\min\{1,\sqrt Vs\}$ or $\min\{1,Ns\}$,
according to the complete support-covariance trichotomy.
Hard reset-policy square budget $Q$ yields coherent order
$\min\{1,\sqrt Qs\}$, uniformly over the allocation and unknown quadratic
remainder.  Local constants depend on the fixed tube; exact variational
values do not assert strict advantage for every fixed pair.
\end{abstract}'''
        text=text[:lo]+abstract+text[hi:]
    put(entry,text)

intro=(src/'editions/operational-introduction90.tex').read_text()
intro=intro.replace('The interface and the two main results','Local geometry and exact experiments')
intro=intro.replace('This article gives a local geometric classification with sharp allocation\nlaws and an exact finite experiment separating receiver storage from\ncoherent acquisition.',
 'This article gives a local geometric classification with sharp allocation\nlaws, a general variational principle for reset decisions, and exact\nfinite experiments separating receiver storage from coherent acquisition.')
anchor='\\subsection{Geometry underlying the allocation law}'
addition=r'''\subsection{A general optimization principle and equal priors}
Theorem~\ref{thm:resetvariational91} applies to every finite two-call
ordered-measurement decision experiment, with arbitrary priors and
rewards.  If $g_y(\rho)$ is the best fresh-reference value after a first
label without receiver feedback and $c_y$ is its upper concave envelope
on all density matrices, then
\[
 P_{\rm reset}=\max_{\rho}\sum_yc_y(\rho).
\]
A common first marginal is essential.  At most
$(\operatorname{rank}\rho)^2$ instrument outcomes per first label
suffice, and the quantum receiver has dimension at most $d_1d_2$.
Theorem~\ref{thm:resetdual91} supplies exact Hermitian majorants and
contact conditions.  Mixed density-matrix atoms cannot be replaced
silently by pure states.  This is a finite-dimensional characterization
of optimal values, not a polynomial-time optimization claim.

For the same finite basis devices, Theorem~\ref{thm:equalprior91}
removes the special prior in \eqref{eq:fronthierarchy90}.  With equal
hypothesis priors its exact values are
\[
 \frac12+\frac{t^2(d-1)}{2d(d+1)},\qquad
 \frac12+\frac{t^2(d-1)}{2d^2},\qquad
 \frac12+\frac{t^2}{2d}.
\]
For the seven qubit devices at $t=1$ these become
$7/12<5/8<3/4$.  The middle upper permits all receiver feedback,
but its attaining strategy uses none.  The alternative index is chosen
once for both calls; independent redraws give no signal.  The explicit
qubit calculation and a channel/prior/law stability estimate follow the
theorem.

These statements share one operational interface and one precise
fresh-preparation cut, but have different quantifiers.  The local profile
law classifies shrinking fixed-tube signals at arbitrary hard resources.
The variational principle treats exact two-call values for arbitrary
finite experiments.  The two basis theorems solve particular experiments
inside that general class.  Neither exact calculation supplies uniform
constants for the local theorem, and the local theorem is not a premise
of either exact score proof.

'''
b.require(intro.count(anchor)==1,'introduction anchor')
put('editions/operational-introduction91.tex',intro.replace(anchor,addition+anchor))
comparison=(src/'editions/current-comparison90.tex').read_text()+r'''
\subsection{Finite reset optimization}
The constrained-separability formulations of Ohst et al.\ \cite{OZNPQ89}
and the finite-time compilation theorem of Zonnios--Binder
\cite{ZB90} are direct antecedents for optimization with memory
restrictions.  Theorem~\ref{thm:resetvariational91} instead fixes a
complete fresh-preparation cut and retains an arbitrary old receiver;
it realizes a common-barycenter concave-envelope formula with a finite
branch bound for every finite two-call measurement decision experiment.
It does not classify all auxiliary-dimension slices of those models.
Concave envelopes, Carath\'eodory reduction and conic duality are
established tools \cite{Uhlmann91,BV91}, not separate novelty claims.
The equal-prior values in Theorem~\ref{thm:equalprior91} are an exact
application, with all class uppers proved rather than inferred from
exhibited strategies.  Antisymmetric comparison and finite design
mechanisms remain credited to \cite{ZHS90,GAE90}.  Independent specialist
assessment of the resulting optimization statements remains appropriate.
'''
put('editions/current-comparison91.tex',comparison)
addition=r'''\bibitem{Uhlmann91} A.~Uhlmann, Roofs and convexity,
Entropy \textbf{12} (2010), 1799--1832.
\bibitem{BV91} S.~Boyd and L.~Vandenberghe, \emph{Convex Optimization},
Cambridge University Press, Cambridge, 2004.
'''
put('editions/bibliography-addendum91.tex','\\begin{thebibliography}{99}\n'+addition+'\\end{thebibliography}\n')
put('editions/bibliography91.tex',(src/'editions/bibliography90.tex').read_text().replace('\\end{thebibliography}',addition+'\\end{thebibliography}'))

# Reuse the audited reconstruction engine; update only the immediate baseline,
# report identities, active new theorem inventory and the clean journal package.
code=(src/'build_revision.py').read_text()
code=code.replace("BASE='df7ed618813224b058b97c6cbda720ad936e2c53'","BASE='906e6e12841816f07e4ca31137690fd18bb65853'")
code=code.replace("ROOT/'V89_BASELINE.json'","ROOT/'V90_BASELINE.json'")
code=code.replace("ROOT/'EDITORIAL_INSERTIONS_V90.json'","ROOT/'EDITORIAL_INSERTIONS_V91.json'")
code=code.replace("ROOT/'predecessor-v89-audit'","ROOT/'predecessor-v90-audit'")
code=code.replace('wrong v89 source identity','wrong v90 source identity')
code=code.replace('gtf90','gtf91').replace('v90 build','v91 build').replace('Source-bound v90','Source-bound v91')
code=code.replace('GENERAL_THETA_FOUNDATIONS_I_V90_','GENERAL_THETA_FOUNDATIONS_I_V91_')
code=code.replace("'FROZEN_R59_REPORT.md','b95c190a89823651c656e1d47a6e7e5ffaf5a2ee'","'FROZEN_R60_REPORT.md','dceb7c7d0c3e862ed494cdb46a0c50ec56bea5ed'")
code=code.replace("'FROZEN_R59_PIPELINE_AUDIT.md','10c0f8bca52d016ae6fed65b9b7ef8d594a6ac86'","'FROZEN_R60_PIPELINE_AUDIT.md','fc282d8e45e7ebf93e8897a3c9d407090f76ffd3'")
code=code.replace('controlling R59 report changed','controlling R60 report changed')
new_sections=[sec83+'.tex',sec84+'.tex']
labels=[]
for name in new_sections:labels+=re.findall(r'\\label\{((?:thm|lem|prop|cor):[^}]+)\}',(dst/name).read_text())
code=re.sub(r'NEW_SECTIONS=.*\n','NEW_SECTIONS='+repr(new_sections)+'\n',code,count=1)
code=re.sub(r'NEW_LABELS=.*\n','NEW_LABELS='+repr(labels)+'\n',code,count=1)
start=code.index('JOURNAL_EXTRAS=');end=code.index('# These established',start)
code=code[:start]+"JOURNAL_EXTRAS={'paper.pdf','BINARY_SUPPLEMENT.pdf','REPRODUCIBILITY.md','journal_verify.py'}\n"+code[end:]
code=code.replace("'budget_domain_check.py')","'budget_domain_check.py','reset_variational_check.py','equal_prior_check.py')")
code=code.replace("('quantitative.tex','supplement.tex','structural.tex')","('quantitative.tex','supplement.tex')")
code=code.replace("('paper.pdf','BINARY_SUPPLEMENT.pdf','STRUCTURAL_PAPER.pdf')","('paper.pdf','BINARY_SUPPLEMENT.pdf')")
code=code.replace('standalone primary/supplement/structural reconstruction','standalone primary/supplement reconstruction')
put('build_revision.py',code)
jv=(src/'journal_verify.py').read_text().replace('gtf90','gtf91').replace('v90','v91')
jv=jv.replace(", 'structural.tex': 'STRUCTURAL_PAPER.pdf'",'')
lo=jv.index('EXTRAS =');hi=jv.index('\n\n\ndef sha',lo)
jv=jv[:lo]+"EXTRAS = {'paper.pdf','BINARY_SUPPLEMENT.pdf','REPRODUCIBILITY.md','journal_verify.py'}"+jv[hi:]
jv=jv.replace('primary, supplement and structural article','primary and supplement').replace('three active source graphs','two active source graphs')
put('journal_verify.py',jv)
status=json.loads((src/'PROOF_STATUS.json').read_text())
status.update(schema='gtf91.proof-status/1',revision=91,current_revision_directory='papers/GTF-I-v91-reset-variational',new_labels=labels)
status['executed_scope']['regression_suites']=32
status['external_status']['journal_objective']='Four-leading-general-journal objective retained; R60 disposition preserved for reconsideration.'
status['inherited_status']={'path':'predecessor-v90-audit/PROOF_STATUS.json','meaning':'All predecessor proof paragraphs preserved; registered additions only in module 82.'}
status['new_claims'].update(general_two_call_reset_variational_value=True,attained_reset_duality=True,
 finite_decision_optimal_receiver_and_branch_bound=True,equal_hypothesis_prior_exact_hierarchy=True,
 arbitrary_pair_value_formula=True,arbitrary_fixed_pair_score_gap=False,full_memory_dimension_hierarchy=False,
 efficient_global_reset_optimization=False)
put('PROOF_STATUS.json',json.dumps(status,indent=2,sort_keys=True)+'\n')
put('CONTROLLING_REPORTS.json',json.dumps({'schema':'gtf91.reports/1','reviewed_head':baseline['commit'],
 'external':{'commit':'cf13712c54e9ef0c9c54a240b1f26efc78cc3568','blob':'dceb7c7d0c3e862ed494cdb46a0c50ec56bea5ed'},
 'pipeline':{'commit':'e4e72a512bf747e7bd190196cd8dc3db35689e3c','blob':'fc282d8e45e7ebf93e8897a3c9d407090f76ffd3'}},indent=2)+'\n')
print(json.dumps({'status':'staged','base_native_files':len(inv),'new_labels':labels,'destination':str(dst)},indent=2))
