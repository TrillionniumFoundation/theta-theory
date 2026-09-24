#!/usr/bin/env python3
"""Non-destructive A2 v145 assembly, pinned to the reviewed v144 source."""
from pathlib import Path
import json,os,re,shutil,subprocess,hashlib
ROOT=Path(os.environ.get('A2_REPO_ROOT',str(Path(__file__).resolve().parents[2])))
BOOT=Path(__file__).resolve().parent
PREFIX='papers/A2-v17-boundary-information-coarsening/article'
OLD=ROOT/PREFIX/'v144';NEW=ROOT/PREFIX/'v145'
PIN='542bcd5027e96ca41568f3eb9c3481dc0f296fed'
REVIEW='d8376b5dbb47422d93a474add8362d39cf2a68c1'
if os.environ.get('GITHUB_ACTIONS'):
 subprocess.run(['git','diff','--exit-code',PIN,'--',PREFIX+'/v144'],cwd=ROOT,check=True)
assert not NEW.exists(), 'Refuse to overwrite an existing revision'
NEW.mkdir(parents=True)
for folder in ['parts','checks']:
 shutil.copytree(OLD/folder,NEW/folder,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
for p in OLD.glob('*.tex'):
 if p.name not in {'geometry.tex','supplement.tex','complete.tex','frontmatter.tex'}:shutil.copy2(p,NEW/p.name)
def put(name,text):
 p=NEW/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def once(text,old,new):
 assert text.count(old)==1,(old,text.count(old));return text.replace(old,new,1)
put('parts/29-curve-reconstruction-v145.tex',(BOOT/'curve.tex').read_text())
put('parts/30-orthogonal-input-v145.tex',(BOOT/'orbits.tex').read_text())
put('parts/00-principal-introduction-v145.tex',(BOOT/'introduction.tex').read_text())
foundation=(OLD/'parts/00-ruling-foundations-v143.tex').read_text()
foundation=once(foundation,'in the supplement.','in the separate research archive.')
start=foundation.index('For the degree-twelve construction below,')
end=foundation.index('\\end{proof}',start)
foundation=foundation[:start]+'''The conclusion applies to every homogeneous degree.  In particular,
no right change of frame can replace the single projective left map
by separate transformations on different coefficient spaces.
'''+foundation[end:]
put('parts/00-ruling-foundations-v145.tex',foundation)
criterion=(OLD/'parts/13a-criterion-v143.tex').read_text()
a=criterion.index('The web problem');b=criterion.index('\\subsection',a)
criterion=criterion[:a]+'''Extracting coefficient data from an abstract scheme and reconstructing
a defining relation space from those data are distinct operations.
The criterion below isolates the first.  Its hypotheses will be
verified directly for the multiplication schemes and then on curves.

'''+criterion[b:]
put('parts/13a-criterion-v145.tex',criterion)
pencil=(OLD/'parts/18-pencil-proof-v143.tex').read_text().replace('in the supplement','in the separate research archive')
put('parts/18-pencil-proof-v145.tex',pencil)
strata=(OLD/'parts/25-fixed-spectral-strata.tex').read_text()
a=strata.index('\\begin{theorem}')
strata=strata[:a]+'\\input{parts/30-orthogonal-input-v145.tex}\n\n'+strata[a:]
a=strata.index('We specify the classical input.');b=strata.index('The primary spaces',a)
strata=strata[:a]+'''We use Lemma~\\ref{lem:orthogonal-orbits-v145}.  Its full-orthogonal
classification and dominance order have exactly the group and
self-adjoint convention needed here.  The comparison for Grassmannian
Segre strata is \\cite[Theorem~5.1]{FevolaMandelshtamSturmfels}.

'''+strata[b:]
put('parts/25-fixed-spectral-strata-v145.tex',strata)
critical=(OLD/'parts/28-projective-critical-divisor-v144.tex').read_text()
critical=once(critical,'''line outside the finite zero set of its fibre of \\(G\\).  Such a
point exists since the residue field has characteristic zero.
After shrinking the base, the value of \\(G\\) there is a unit.''',r'''line outside the finite zero set of its fibre of \(G\).  The
characteristic-zero residue field contains its prime field \(\mathbb Q\).
Thus \(\mathbb P^1(\mathbb Q)\) supplies infinitely many constant
points, whereas the nonzero fibre form has only finitely many zeros.
One of these points avoids them.  Its evaluation is nonzero in the
residue field, and becomes a unit after shrinking the base.''')
# Put the chain rule before the invariant conclusion, without removing its proof.
pos=critical.index('\\begin{proposition}') if '\\begin{proposition}' in critical else len(critical)
# The invariant chain rule is a separate paragraph immediately after the ramification proof.
needle='\\subsection{A length-three critical fibre'
idx=critical.find(needle)
if idx<0:
 idx=critical.index('\\begin{proposition}')
clarification=r'''\paragraph{Coordinate invariance on the critical quotient.}
Write a smooth local coordinate change as \(x=x(y)\), its Jacobian as
\(J=(\partial x_a/\partial y_i)\), and the first scores as \(s_a\).
The second-derivative chain rule is
\[
 H_y=J^{\mathsf t}H_xJ+
             \sum_a s_a\left(\frac{\partial^2x_a}
                                   {\partial y_i\partial y_j}\right)_{ij}.
\]
All \(s_a\) vanish in the critical quotient itself, not only on its
reduction.  There \(H_y=J^{\mathsf t}H_xJ\) and
\(\det H_y=(\det J)^2\det H_x\).  Since \(\det J\) is a unit,
the Hessian ideal is unchanged even in a nonreduced critical algebra.

'''
critical=critical[:idx]+clarification+critical[idx:]
put('parts/28-projective-critical-divisor-v145.tex',critical)
main=(OLD/'geometry.tex').read_text().replace('\\externaldocument{supplement-labels}[supplement.pdf]\n','')
for name in ['00-principal-introduction-v144','00-ruling-foundations-v143','13a-criterion-v143','18-pencil-proof-v143','25-fixed-spectral-strata']:
 new={'00-principal-introduction-v144':'00-principal-introduction-v145','00-ruling-foundations-v143':'00-ruling-foundations-v145','13a-criterion-v143':'13a-criterion-v145','18-pencil-proof-v143':'18-pencil-proof-v145','25-fixed-spectral-strata':'25-fixed-spectral-strata-v145'}[name]
 main=main.replace(name+'.tex',new+'.tex')
main=main.replace('\\input{frontmatter.tex}','\\input{frontmatter-v145.tex}')
main=main.replace('\\input{parts/20-finite-neighbourhoods.tex}','\\input{parts/20-finite-neighbourhoods.tex}\n\\input{parts/29-curve-reconstruction-v145.tex}')
for name in ['23-real-likelihood','26-critical-correspondence-v143','28-projective-critical-divisor-v144']:
 main=main.replace('\\input{parts/'+name+'.tex}\n','')
main=main.replace('references-v144.tex','references-main-v145.tex')
put('geometry.tex',main)
put('frontmatter-v145.tex',r'''\title[Finite failure schemes and quadratic pencils]{Finite failure schemes and the reconstruction of quadratic pencils}
\author{Qian Qi}
\date{September 24, 2026}
\subjclass[2020]{14M12, 14B05, 14D20, 13C40}
\keywords{Quadratic pencil, nonreduced degeneracy locus, intrinsic reconstruction, infinitesimal neighbourhood}
\hypersetup{pdftitle={Finite failure schemes and the reconstruction of quadratic pencils, revision 145},pdfauthor={Qian Qi}}
\begin{abstract}
We reconstruct every complex quadratic pencil from an abstract unmarked
finite-order neighbourhood of its multiplication-failure scheme.
For embedding dimension \(n\ge3\), the smallest uniform order is
\(d=n^2+2n-4\); every lower-order neighbourhood is independent of the
pencil.  The inverse recovers a tensor orientation from intrinsic
rank-one rulings and then recovers the full coefficient line.  In fact,
a neighbourhood supported on a single Schubert line suffices.  More
generally, the same reconstruction works on any smooth projective curve
with a rank-\(n\) bundle having nontrivial projectivization.  We construct
the actual universal finite neighbourhood, compatible with arbitrary
complex base change with its relative socle retained.  For regular
pencils its spectral readout includes all elementary divisors and
higher Fitting incidence schemes.  Fixed-discriminant specializations
illustrate the distinction between this information and reduced rank
data.  The unmarked inverse, the framed parameter immersion, and the
relative constructions are kept separate.
\end{abstract}
\maketitle
''')
put('applications.tex',r'''\input{preamble.tex}
\externaldocument{geometry-labels}[geometry.pdf]
\renewcommand{\thesection}{A\arabic{section}}
\begin{document}
\title[Critical schemes of quadratic pencils]{Spectral likelihood, projective critical schemes, and ramification for quadratic pencils}
\author{Qian Qi}
\date{September 24, 2026}
\hypersetup{pdftitle={Quadratic pencil applications, A2 revision 145},pdfauthor={Qian Qi}}
\begin{abstract}
This separately reviewable applications manuscript retains the reciprocal
likelihood and projective critical-scheme theory of quadratic pencils.
For supplied split semisimple spectral data with simple disjoint
projective poles, the critical divisor is finite locally free through
critical collisions; its ramification ideal equals its Hessian ideal.
For a supplied real definite realization, separated real data give a
totally real critical cover.  The score discriminant is not inverted
in the finite-flat theorem.  Real structure and data are additional
inputs, not conclusions of complex unmarked reconstruction.  References
to the finite-failure inverse and spectral readout refer to the separate
principal article; neither this application nor its real-root proof is
an input to that article.
\end{abstract}
\maketitle
\input{parts/23-real-likelihood.tex}
\input{parts/26-critical-correspondence-v143.tex}
\input{parts/28-projective-critical-divisor-v145.tex}
\input{parts/17-assistance.tex}
\input{references-applications-v145.tex}
\end{document}
''')
archive=(OLD/'complete.tex').read_text().replace('\\input{frontmatter.tex}','\\input{archive-frontmatter.tex}')
put('archive-v144.tex',archive)
put('archive-frontmatter.tex',r'''\title[Unsubmitted A2 research archive]{A2 research archive: the complete revision 144 mathematical text}
\author{Qian Qi}
\date{September 24, 2026}
\begin{abstract}
This is a non-submitted archival compilation, not the supplement of
revision 145 and not an additional certification obligation for its
referee.  It preserves the predecessor's complete mathematical text,
including independent web, exterior-operator, K3, polarized, primary
boundary, and application theories.  Its internal publication language
and reference routing are historical.  Current reconstruction and
applications manuscripts have their own sources, proofs, scope and
review entries.  No historical priority of the auxiliary contraction is
certified by this archival preservation.
\end{abstract}
\maketitle
''')
# Preserve every original part/check byte, while pruning only the bibliographies of new publication objects.
def expand(path):
 text=path.read_text()
 return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(NEW/(m[1] if m[1].endswith('.tex') else m[1]+'.tex')),text)
base=(OLD/'references.tex').read_text()
items={m[1]:m[0].strip() for m in re.finditer(r'\\bibitem\{([^}]+)\}[\s\S]*?(?=\\bibitem|\\end\{thebibliography\})',base)}
extra=(OLD/'references-v144.tex').read_text()
for m in re.finditer(r'\\bibitem\{([^}]+)\}[\s\S]*?(?=\\bibitem|\\inheritedendbibliography)',extra):items[m[1]]=m[0].strip()
items['Ohta1986']=r'''\bibitem{Ohta1986}
T.~Ohta, The singularities of the closures of nilpotent orbits in certain
symmetric pairs, \emph{Tohoku Math. J. (2)} \textbf{38} (1986), 441--468.
doi:10.2748/tmj/1178228456.'''
for doc,bib in [('geometry','main'),('applications','applications')]:
 stub='references-'+bib+'-v145.tex';put(stub,'')
 text=expand(NEW/(doc+'.tex'))
 keys=set()
 for m in re.finditer(r'\\cite(?:\[[^\]]*\])*\{([^}]+)\}',text):keys.update(x.strip() for x in m[1].split(','))
 assert keys<=items.keys(),keys-items.keys()
 put(stub,'\\begin{thebibliography}{99}\n\n'+'\n\n'.join(items[k] for k in sorted(keys))+'\n\\end{thebibliography}\n')
for name in ['check_v145.py','verify_v145.py','build.sh','RESPONSE_TO_V144_REPORTS.md','LITERATURE_AUDIT_V145.md','README.md']:
 put(name,(BOOT/name).read_text())
original={str(p.relative_to(OLD)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['parts','checks'] for p in (OLD/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
assert all(hashlib.sha256((NEW/k).read_bytes()).hexdigest()==v for k,v in original.items())
put('INHERITED_SOURCE_V145.json',json.dumps({'predecessor_commit':PIN,'predecessor_mathematical_source':'fb4e7c4d00167e422fdb7ee73876a74f6649fb68','review_commit':REVIEW,'original_parts_and_checks_sha256':original},indent=2)+'\n')
put('ISSUE_MATRIX.json',json.dumps({'revision':145,'controlling_review':REVIEW,'additional_review':'e392e7ba5f04a94444831140b22638ae42aa2972','issues':{'publication_object':'implemented: standalone principal article; separate applications; non-submitted archive','intrinsic_significance':'strengthened: reconstruction over projective curves and one Schubert line; editorial significance remains for referee','orthogonal_references':'implemented: original Ohta Proposition 1, Theorem 1, section 2.4 Remark 8(i); component proof supplied','critical_proof_clarifications':'implemented: prime-field section and Hessian chain rule in critical quotient','scope':'all-pencil theorem unchanged; regular/split/real/framed conditions explicit','Ballico_1993':'documentary-open: complete theorem text not obtained; no anticipation or nonanticipation conclusion','operator_priority':'separate archival research obligation, not certified and not a principal-paper significance claim'}},indent=2)+'\n')
archive_route=ROOT/'revisions/a2-v145/history';archive_route.mkdir(parents=True,exist_ok=True)
for name in ['README.md','CURRENT_REVIEW_ENTRY.md']:
 if (ROOT/name).exists():shutil.copy2(ROOT/name,archive_route/('ROOT_'+name))
(ROOT/'README.md').write_text('# Theta-Theory — A2 revision 145\n\nBegin at [CURRENT_REVIEW_ENTRY.md](CURRENT_REVIEW_ENTRY.md).\n\nThe current principal article, separate applications manuscript and non-submitted archive have explicit independent review scopes. See the source lock and response in the native v145 directory.\n')
(ROOT/'CURRENT_REVIEW_ENTRY.md').write_text('# A2 revision 145 — current review object\n\n'+
 'Principal article: ['+PREFIX+'/v145/geometry.pdf]('+PREFIX+'/v145/geometry.pdf).\n\n'+
 'Separate applications: ['+PREFIX+'/v145/applications.pdf]('+PREFIX+'/v145/applications.pdf).\n\n'+
 'Begin with ['+PREFIX+'/v145/README.md]('+PREFIX+'/v145/README.md) and the point-by-point response. '+
 'The source lock and build receipt identify the immutable source after successful compilation. '+
 'The complete v144 mathematical archive is preserved but is not a submission supplement. '+
 'The full Ballico 1993 comparison remains documentary-open.\n')
print('Assembled v145 without modifying v144 or any original mathematical part/check.')
