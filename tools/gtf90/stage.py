#!/usr/bin/env python3
"""Create v90 from the pinned v89 source; preserve every original byte and proof label."""
from pathlib import Path
import argparse, base64, gzip, hashlib, importlib.util, json, re, shutil
p=argparse.ArgumentParser();p.add_argument('--source',default='papers/GTF-I-v89-resource-profile')
p.add_argument('--dest',default='papers/GTF-I-v90-operational-memory')
p.add_argument('--patch',default=str(Path(__file__).parent/'patch'))
p.add_argument('--reports',default='/tmp/gtf90-reports');a=p.parse_args()
src=Path(a.source).resolve();dst=Path(a.dest).resolve();patch=Path(a.patch).resolve()
if dst.exists():raise RuntimeError('refusing to overwrite an existing v90 native directory')
if not patch.exists():
    payload=base64.b64decode(''.join((Path(__file__).parent/f'payload-{i}.b64').read_text() for i in range(3)),validate=True)
    if hashlib.sha256(payload).hexdigest()!='f9b761773b2c0cd0343d77f8d3cb78fdbe33ff0fe2859654cad921565a69ee29':
        raise RuntimeError('revision payload digest mismatch')
    files=json.loads(gzip.decompress(payload))
    if not isinstance(files,dict):raise RuntimeError('invalid revision payload')
    for name,text in files.items():
        rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts or not isinstance(text,str):raise RuntimeError('unsafe payload entry')
        target=patch/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)

spec=importlib.util.spec_from_file_location('v89_helpers',src/'build_revision.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
inv=old.sources(src)
expected=json.loads((src/'evidence/SOURCE_HASHES.json').read_text()) if (src/'evidence/SOURCE_HASHES.json').exists() else inv
old.require(inv==expected,'v89 source archive inventory mismatch')
for name in inv:
    target=dst/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src/name,target)
base={'commit':'df7ed618813224b058b97c6cbda720ad936e2c53','files':inv,'graphs':{}}
for entry in old.DOCS:
    files,labels=old.graph(src,entry);base['graphs'][entry]={'files':sorted(files),'labels':sorted(labels)}
old.put(dst/'V89_BASELINE.json',base)
def put(name,text):
    target=dst/name
    if name in inv and target.read_text()!=text:
        backup=dst/'predecessor-v89-audit'/name
        if not backup.exists():backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src/name,backup)
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
def add(name,anchor,text):
    data=(dst/name).read_text();old.require(data.count(anchor)==1,'insertion anchor: '+name)
    put(name,data.replace(anchor,anchor+text));insertions.setdefault(name,[]).append(text)
for file in sorted(patch.rglob('*')):
    if file.is_file() and file.name!='source_check90.txt':put(file.relative_to(patch).as_posix(),file.read_text())
for name in ['FROZEN_R59_REPORT.md','FROZEN_R59_PIPELINE_AUDIT.md']:
    put(name,(Path(a.reports)/name).read_text())
insertions={}
add('sections/79-classical-feedback-reset-width.tex',
    '\\label{sec:reset88}\n',r'''We use normal quantum instruments on trace-class operators.  Countably
many recorded outcomes form an $\ell^1$ direct sum.  All identities below
follow from finite truncations retaining a remainder outcome and passage
to the trace-norm limit; positivity gives monotone convergence of trace
sums.  The hard finite depth makes the conditional induction applicable.
''')
add('sections/80-allocation-profiles.tex','Early termination can be padded by unused reserved blocks.\n',r'''Our convention records a deterministic terminal symbol at each remaining
round, executes a fixed fresh preparation and discards its output.  All
positive reservations in the prescribed profile are still charged.
Zero-length terminal symbols are not additional profile components.
''')
add('sections/80-allocation-profiles.tex','Consequently the full product laws have at least this separation.\n',r'''In the application, $(x_r)$ is fixed by $E,H,\Lambda,s$ and the public
profile.  The readout has precisely this public dependence and no
dependence on the unknown tuple $F-E-sH$ or actual biases $(u_r)$.
''')
add('sections/81-quadratic-budgets-and-memory.tex',
    'For tangential directions one may substitute the right side of\n\\eqref{eq:policyprofile89} for $D(\\pi;E,F)$.\n',r'''For the same pair of ideal and implemented channels the proof gives the
two-sided estimate $|\widetilde D(\pi;E,F)-D(\pi;E,F)|\le2\varepsilon$.
In particular a lower $c\omega$ remains at least $c\omega/2$ if
$\varepsilon\le c\omega/4$; the condition $\varepsilon=o(\omega)$
suffices along a shrinking-signal sequence.
''')
add('sections/81-quadratic-budgets-and-memory.tex',
    '$|\\Phi^+\\rangle=(|00\\rangle+|11\\rangle)/\\sqrt2$.\n',r'''For precision, order factors as $I_1,Y_1,I_2,Y_2$ and take the fully
transposed unnormalized Choi representative
$J^\sharp(E)=\sum_yE_y\otimes|y\rangle\langle y|$, obtained from
$(\operatorname{Id}\otimes\mathcal M_E)(|\Omega\rangle\langle\Omega|)$
by full transpose, with $|\Omega\rangle=|00\rangle+|11\rangle$.
Thus $\tr_YJ^\sharp=I$.  The two normalized pairs produce the receiver
operator $(J^\sharp(E)\otimes J^\sharp(F))^{\mathsf T}/4$.
For any receiver effect $M$, the Born probability is
$\tr[M^{\mathsf T}(J^\sharp(E)\otimes J^\sharp(F))]/4$.
This proves the transpose and factor $1/4$ for arbitrary complex effects,
not merely for the real Bell projector.  Grouping the input factors below
means the canonical permutation of the stated factor order.
''')
add('sections/81-quadratic-budgets-and-memory.tex',
    'no old reference enters the second acquisition.\n',r'''Indeed $0\preceq\Pi^{\mathsf T}\otimes|00\rangle\langle00|\preceq I$,
so the complementary effect is positive.  The deterministic sum is
$\Xi\otimes I_{Y_2}$ with
$\Xi=I_{I_1}\otimes I_{Y_1}\otimes I_{I_2}/4$ and
$\tr_{I_2}\Xi=(I_{I_1}/2)\otimes I_{Y_1}$; the initial marginal has
trace one.  This verifies both causal tester trace constraints.
The cone of positive separable operators across the complete-call cut
$I_1Y_1\mid I_2Y_2$ is closed: its trace-one slice is the compact convex
hull of the compact set of product states, and trace controls the scaling
in its cone.  Hence the limiting sums mentioned below lie in this same
closed cone.  Partial transpose is used only as a necessary condition
for separability.
''')
old.put(dst/'EDITORIAL_INSERTIONS_V90.json',{'schema':'gtf90.editorial-insertions/1','insertions':insertions})
newsection='sections/82-operational-memory-hierarchy'
for entry in ['main.tex','quantitative.tex']:
    text=(dst/entry).read_text().replace('\\date{5 October 2026}','\\date{6 October 2026}')
    text=text.replace('\\input{sections/81-quadratic-budgets-and-memory}',
                      '\\input{sections/81-quadratic-budgets-and-memory}\n\\input{'+newsection+'}')
    if entry=='main.tex':
        text=text.replace('\\input{editions/bibliography-addendum89}',
                          '\\input{editions/bibliography-addendum89}\n\\input{editions/bibliography-addendum90}')
        text=text.replace('\\end{abstract}',r'''We further prove an exact all-dimension, two-call operational hierarchy
separating measure-and-reprepare adaptation, unit-reset receiver memory,
and unrestricted acquisition on a finite ordered-measurement ensemble,
including its full-rank depolarizing deformation.
\end{abstract}''')
    else:
        text=text.replace('operational-introduction89','operational-introduction90').replace('current-comparison89','current-comparison90').replace('bibliography89','bibliography90')
        lo=text.index('\\begin{abstract}');hi=text.index('\\end{abstract}',lo)+len('\\end{abstract}')
        abstract=r'''\begin{abstract}
We study the finite-use geometry of ordered quantum measurements under
separate acquisition and receiver resources.  In a fixed quadratic
neighborhood of a nonzero tangent, a prescribed profile of complete
groups with $N=\sum n_r$ and $V=\sum n_r^2$ has optimal trace orders
$\min\{1,\sqrt Ns\}$, $\min\{1,\sqrt Vs\}$ and $\min\{1,Ns\}$,
according to the complete support-covariance trichotomy.  The same orders
hold with reset feedback, provided every fresh complete acquisition is
conditionally independent of the old receiver.  Hard quadratic policy
budget $Q$ gives coherent order $\min\{1,\sqrt Qs\}$.  All finite remainder
terms are retained, and lower readouts are independent of the unknown
remainder.  Constants depend on the fixed tube, not on the allocation.
We also give an exact operational hierarchy on a finite ensemble in every
dimension: two-call classical adaptation, unit-reset receiver storage,
and unrestricted adaptive acquisition have strictly different optimal
success probabilities.  For seven qubit devices these are $3/5$, $13/20$
and $4/5$.  A swap-filter identity proves the upper for arbitrary reset
feedback; the separation persists under full-rank depolarization with
explicit stability bounds.  The covariance kernel, finite orbit and curve
laws, and the linked interior geometry and learning theory are retained.
Local orders are not exact-distance equalities, and reset costs are not
memory dimensions.
\end{abstract}'''
        text=text[:lo]+abstract+text[hi:]
        for section in ['71-transported-regularization','65-finite-outcome-geometry','66-finite-outcome-learning','68-affine-legalization']:
            text=text.replace('\\input{sections/'+section+'}\n','')
    put(entry,text)
text=(dst/'supplement.tex').read_text().replace('\\date{5 October 2026}','\\date{6 October 2026}')
insert='\\section{Retained multi-outcome geometry and consequences}\n'
for section in ['71-transported-regularization','65-finite-outcome-geometry','66-finite-outcome-learning','68-affine-legalization']:
    insert+='\\input{sections/'+section+'}\n'
text=text.replace('\\input{editions/coding-bibliography}',insert+'\\input{editions/coding-bibliography90}')
put('supplement.tex',text)
bib=(src/'editions/bibliography89.tex').read_text()
addition=(dst/'editions/bibliography-addendum90.tex').read_text().split('\\begin{thebibliography}{99}\n',1)[1].rsplit('\\end{thebibliography}',1)[0]
put('editions/bibliography90.tex',bib.replace('\\end{thebibliography}',addition+'\\end{thebibliography}'))
codebib=(src/'editions/coding-bibliography.tex').read_text();keys=set(re.findall(r'\\bibitem\{([^}]+)\}',codebib))
for chunk in re.split(r'(?=\\bibitem\{)',bib)[1:]:
    key=re.match(r'\\bibitem\{([^}]+)\}',chunk).group(1)
    if key not in keys:
        codebib=codebib.replace('\\end{thebibliography}',chunk.split('\\end{thebibliography}')[0]+'\\end{thebibliography}')
put('editions/coding-bibliography90.tex',codebib)
comparison=(src/'editions/current-comparison89.tex').read_text()
comparison=comparison.replace('The Bell-reference witness establishes a model\nboundary only;',
 'The Bell-reference witness alone establishes a model\nboundary; Theorem~\\ref{thm:operationalhierarchy90} now supplies a strict\nexact score hierarchy for the specified finite ensemble, whereas')
comparison+='\n'+(patch/'editions/memory-comparison90.tex').read_text()
put('editions/current-comparison90.tex',comparison)
# Keep existing deterministic build/reconstruction machinery, replace only its
# immediate baseline and source conservation audit.
build=(src/'build_revision.py').read_text()
start=build.index('def check_source():');end=build.index('def source_commit_inventory(',start)
build=build[:start]+(patch/'source_check90.txt').read_text()+build[end:]
build=build.replace("BASE='d1add4a7ba45230b3cba71b47ef46da5e4a88d72'","BASE='df7ed618813224b058b97c6cbda720ad936e2c53'")
build=build.replace('gtf89','gtf90').replace('v89 build','v90 build').replace('V89_','V90_').replace("EPOCH='1791158400'","EPOCH='1791244800'")
build=re.sub(r'NEW_SECTIONS=.*\n',"NEW_SECTIONS=['sections/82-operational-memory-hierarchy.tex']\n",build,count=1)
labels=re.findall(r'\\label\{((?:thm|lem|prop|cor):[^}]+)\}',(dst/(newsection+'.tex')).read_text())
build=re.sub(r'NEW_LABELS=.*\n','NEW_LABELS='+repr(labels)+'\n',build,count=1)
build=build.replace("'resource_check.py')","'resource_check.py','memory_check.py','budget_domain_check.py')")
# The source baseline filename must remain V89_BASELINE after schema replacement.
build=build.replace("ROOT/'V90_BASELINE.json'","ROOT/'V89_BASELINE.json'")
put('build_revision.py',build)
put('journal_verify.py',(src/'journal_verify.py').read_text().replace('v89','v90').replace('gtf89','gtf90').replace('1791158400','1791244800'))
status=json.loads((src/'PROOF_STATUS.json').read_text());status['schema']='gtf90.proof-status/1';status['revision']=90
status['current_revision_directory']='papers/GTF-I-v90-operational-memory';status['new_labels']=labels
status['current_crosswalk']={'path':'RESPONSE_TO_REFEREE.md','required':15,'detailed':30}
status['external_status']['journal_objective']='Four-leading-general-journal objective retained; R59 disposition not overwritten'
status['executed_scope']['regression_suites']=30
status['new_claims'].update({'finite_ensemble_exact_three_class_hierarchy':True,'all_dimension_full_rank_deformation':True,
 'arbitrary_fixed_pair_score_gap':False,'full_memory_dimension_hierarchy':False})
status['inherited_status']={'path':'predecessor-v89-audit/PROOF_STATUS.json','meaning':'Every original proof paragraph retained; editorial insertions registered and invertible.'}
put('PROOF_STATUS.json',json.dumps(status,indent=2,sort_keys=True)+'\n')
put('CONTROLLING_REPORTS.json',json.dumps({'schema':'gtf90.reports/1','reviewed_head':base['commit'],
 'external':{'commit':'a7d030d635a2bb40c8b4f7f2265df877bad95492','blob':'b95c190a89823651c656e1d47a6e7e5ffaf5a2ee'},
 'pipeline':{'commit':'994c41dbeec1da13b6b6486876855fa30ad7cfd5','blob':'10c0f8bca52d016ae6fed65b9b7ef8d594a6ac86'}},indent=2)+'\n')
print(json.dumps({'status':'staged','destination':str(dst),'base_native_files':len(inv),'new_labels':labels},indent=2))
