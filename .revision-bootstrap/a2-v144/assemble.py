#!/usr/bin/env python3
"""Native, non-destructive A2 v144 assembly from the pinned v143 tree."""
from pathlib import Path
import json,os,shutil,subprocess
ROOT=Path(os.environ.get('A2_REPO_ROOT',str(Path(__file__).resolve().parents[2])))
BOOT=Path(__file__).resolve().parent
PIN='40ef003998cbeb20f418e1b5e0dcfa9cfef9416d'
REVIEW='3afecca5e65d7fe9c6784020ea6e813122938140'
PREFIX='papers/A2-v17-boundary-information-coarsening/article'
OLD=ROOT/PREFIX/'v143';NEW=ROOT/PREFIX/'v144'
if os.environ.get('GITHUB_ACTIONS'):
 subprocess.run(['git','diff','--exit-code',PIN,'--',PREFIX+'/v143'],cwd=ROOT,check=True)
assert not NEW.exists(), 'Do not overwrite an existing native revision'
shutil.copytree(OLD,NEW,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
for p in OLD.rglob('*'):
 if p.is_file() and p.suffix in {'.tex','.py','.sh','.md','.json'} and 'evidence' not in p.relative_to(OLD).parts:
  q=NEW/'history/v143'/p.relative_to(OLD);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
shutil.rmtree(NEW/'evidence',ignore_errors=True)
for p in NEW.iterdir():
 if p.is_file() and p.suffix in {'.pdf','.aux','.log','.out','.toc','.fls','.fdb_latexmk'}:p.unlink()
for name in ['SOURCE_LOCK_V143.json','NONDELETION_V143.json','PROVENANCE_MANIFEST_V143.json']:(NEW/name).unlink(missing_ok=True)
def put(name,text):
 p=NEW/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def once(text,old,new):
 assert text.count(old)==1,(old,text.count(old))
 return text.replace(old,new,1)
projective=(BOOT/'projective.tex').read_text().replace('\\begin{split}','\\begin{aligned}').replace('\\end{split}','\\end{aligned}')
projective=projective.replace(r''' \omega=\sum_i(n-m_i)\,d\log L_i-n\,d\log Q_h
       =\frac{\eta}{D_hQ_h},\qquad
 \eta=Q_h\sum_i(n-m_i)D_i\,dL_i-nD_h\,dQ_h.''',r''' \begin{aligned}
 \omega&=\sum_i(n-m_i)\,d\log L_i-n\,d\log Q_h
       =\frac{\eta}{D_hQ_h},\\
 \eta&=Q_h\sum_i(n-m_i)D_i\,dL_i-nD_h\,dQ_h.
 \end{aligned}''')
put('parts/28-projective-critical-divisor-v144.tex',projective)
put('checks/revision144_projective_exact.py',(BOOT/'projective_exact.py').read_text())
intro=(OLD/'parts/00-principal-introduction-v143.tex').read_text()
intro=once(intro,r'\subsection{Proof dependencies and further results}',r'''The affine etale description is not the end of the correspondence.
Theorems~\ref{thm:projective-critical-v144} and
\ref{thm:critical-ramification-v144} retain the full projective critical
divisor on the split semisimple spectral-data open.  It is finite
locally free of degree \(2r-3\), including critical collisions and
directions at infinity.  Its Hessian-degeneracy ideal is its relative
ramification ideal, and its trace discriminant records collision
multiplicities.  Proposition~\ref{prop:triple-critical-v144} exhibits
a length-three nonreduced critical fibre in one fixed pencil.  This
continues the same reconstruction chain without changing the
hypotheses of the all-pencil inverse theorem.

\subsection{Proof dependencies and further results}''')
intro=once(intro,r'''Congruence-covariant algebraic correspondence \\[3pt]
Totally real cover''',r'''Congruence-covariant algebraic correspondence \\[3pt]
Projective critical divisor & Split semisimple data; disjoint simple poles &
Finite flat scheme; ramification and trace discriminant \\[3pt]
Totally real cover''')
intro=once(intro,"Ballico's paper \\cite{Ballico93} is a directly relevant predecessor.",r'''Ballico's later paper \cite[Theorem~0.2; \S1,
Remark~1.2 and equation~(6)]{Ballico96} detects failure of quadratic
normality on finite linear sections of a surface using a relative
multiplication map.  Our parameter is instead the quotient algebra
\(B_R\), and our output is reconstruction from an unmarked
infinitesimal failure scheme.  The inverse argument must be compared
with that relative construction, not merely with its terminology.

Ballico's paper \cite{Ballico93} is a directly relevant predecessor.''')
put('parts/00-principal-introduction-v144.tex',intro)
for name in ['geometry.tex','supplement.tex','complete.tex']:
 text=(OLD/name).read_text().replace('revision 143','revision 144').replace('references-v143.tex','references-v144.tex').replace('00-principal-introduction-v143.tex','00-principal-introduction-v144.tex')
 if name!='supplement.tex':text=once(text,r'\input{parts/26-critical-correspondence-v143.tex}',r'\input{parts/26-critical-correspondence-v143.tex}'+'\n'+r'\input{parts/28-projective-critical-divisor-v144.tex}')
 put(name,text)
front=(OLD/'frontmatter.tex').read_text().replace('revision 143','revision 144')
front=once(front,'The full web, contraction, polarized, and boundary theory is retained',r'''For split semisimple data, the projective critical scheme is finite flat
through collisions, with Hessian ramification and a trace discriminant.
The full web, contraction, polarized, and boundary theory is retained''')
put('frontmatter.tex',front)
refs=(OLD/'references-v143.tex').read_text()
refs=once(refs,r'\inheritedendbibliography}',r'''\bibitem{StacksCritical144}
The Stacks Project Authors,
\emph{The Stacks Project}, Tags 056Q, 062Y, 0BVH, and 0BJF,
relative effective Cartier divisors and discriminants of finite locally
free morphisms; accessed September 24, 2026.
\url{https://stacks.math.columbia.edu}.
\inheritedendbibliography}''')
put('references-v144.tex',refs)
verify=(OLD/'verify_v143.py').read_text().replace("ROOT.parent/'v142'","ROOT.parent/'v143'").replace("'history/v142'","'history/v143'").replace('4deb7a35f4488a0c8b686261569ce4ef324ca750',PIN)
verify=verify.replace('V143','V144').replace('verify_v143.py','verify_v144.py').replace('revision 143','revision 144').replace("'revision':143","'revision':144").replace("issue['revision']==143","issue['revision']==144").replace('v143 checks failed','v144 checks failed')
verify=once(verify,"'thm:real-critical-cover-v143'])","'thm:real-critical-cover-v143','thm:projective-critical-v144','thm:critical-ramification-v144','prop:triple-critical-v144'])")
verify=once(verify,"'revision142_exact','revision143_critical_exact']","'revision142_exact','revision143_critical_exact','revision144_projective_exact']")
verify=verify.replace('all_nineteen_scripts_executed','all_twenty_scripts_executed')
anchor="checks['exact_143_critical_algebra']=json.loads((ROOT/'evidence/REVISION143_CRITICAL_EXACT.json').read_text())['ok']"
verify=once(verify,anchor,anchor+"\nchecks['exact_144_projective_algebra']=json.loads((ROOT/'evidence/REVISION144_PROJECTIVE_EXACT.json').read_text())['ok']")
put('verify_v144.py',verify)
put('build.sh',(OLD/'build.sh').read_text().replace('verify_v143.py','verify_v144.py').replace('revision143_critical_exact;','revision143_critical_exact revision144_projective_exact;'))
issue=json.loads((OLD/'ISSUE_MATRIX.json').read_text());issue['revision']=144;issue['mathematical_predecessor_commit']=PIN;issue['current_source_commit_authority']='SOURCE_LOCK_V144.json#/source_commit'
for item in issue['issues']:
 item['evidence']=item['evidence'].replace('V143','V144').replace('revision 143','revision 144').replace('nineteen','twenty').replace('history/v142','history/v143')
 if item['id']=='B140.2':item['evidence']='Six-axis comparison of inspected Ballico 1996 Theorem 0.2 and Remark 1.2 supplied. The separate six-axis 1993 comparison still requires full theorem text; no theorem numbers or nonanticipation conclusions invented.'
 if item['id']=='B140.4':item['evidence']+=' Full projective critical divisor, finite flat across critical collisions, Hessian ramification, trace discriminant and a triple fibre now proved.'
 if item['id']=='Request 8':item['evidence']+=' The new finite-flat divisor continues the same inverse/spectral/critical chain, with an updated dependency table.'
issue['issues'].append({'id':'V144-structural-continuation','status':'proved-with-exact-regression','evidence':'parts/28-projective-critical-divisor-v144.tex: finite flat projective score scheme; Hessian/Fitting equality; trace discriminant; triple collision; arbitrary base change on the specified split semisimple data open.'})
put('ISSUE_MATRIX.json',json.dumps(issue,indent=2)+'\n')
response=r'''# Response to the second v141 referee report — revision 144

Controlling report: `3afecca5e65d7fe9c6784020ea6e813122938140`, reviewing `8cd389f4048a1047be9aa8e8e4f642595175a555`. This revision starts from v143 at `40ef003998cbeb20f418e1b5e0dcfa9cfef9416d`, not from the older manuscript. The v142 and v143 results are inherited, not relabelled as new v144 work.

## Substantive continuation of the principal argument

The new section `parts/28-projective-critical-divisor-v144.tex` extends the reconstructed critical correspondence to the full projective critical divisor. It proves finite local freeness of degree 2r-3 without inverting the critical discriminant. The proof identifies the entire original two-score scheme by inverse coordinate-ring maps, including nilpotents and points at infinity. It proves arbitrary base change on the specified split semisimple data open. This strengthens the existing finite-failure / spectral / critical chain rather than introducing an independent headline theorem.

The ramification theorem identifies Fitt_0 of relative differentials with the Hessian-degeneracy ideal on the critical scheme. The trace discriminant is the binary score discriminant up to a unit. A fixed three-dimensional pencil has a fibre C[u]/(u^3) at the nonsingular matrix I_3/3, ramification ideal (u^2), and base discriminant ideal ((3c+2)^3). The degree remains three through this collision. The existing totally real chamber is retained as an etale restriction.

## Disposition of the referee requests

**B140.1 / source evidence.** Twenty scripts are actually executed; all three manuscripts are compiled natively. Every inherited labelled result, theorem/lemma/proposition/corollary/proof block and numbered equation/align/gather block must remain active unchanged. Original part/check files are byte-identical, with a complete predecessor source archive. SOURCE_LOCK_V144.json binds the exact source SHA and native PDFs; evidence/BUILD_RECEIPT_V144.json records checks, hashes and the run.

**B140.2 / Ballico.** LITERATURE_AUDIT_V144.md supplies six comparison axes against the actually inspected 1996 Theorem 0.2, Remark 1.2 and equation (6). The 1993 paper remains a separate full-text obligation; this comparison is not marked closed or replaced by the 1996 paper. No theorem number or exclusion of anticipation is fabricated.

**B140.3 / exact exterior map.** The all-rank contraction theorem, Jacobian–Casimir identity, singular-value proof and v143 equality-level differential dictionary remain active unchanged. The main pencil proof is independent of this auxiliary map. Exact inspected-source comparison is preserved; exhaustive historical priority is not certified.

**B140.4 / likelihood.** The earlier total-real proof and spectral-projector construction remain unchanged. The new projective family permits critical collisions, but still excludes repeated roots of Q_h and its collisions with spectral poles. These are data-polynomial restrictions, not exclusions of critical collisions. Real definiteness is supplied, not inferred from an abstract complex failure scheme; unrestricted real data are not asserted positive definite.

**Requests 5–7 / universality and spectral strata.** Universal ideal-adic neighbourhoods, arbitrary complex base change with the relative socle retained, spectral sheaf reconstruction and the polynomial-square-root congruence argument remain unchanged. Reduced rank loci are distinguished from full spectral Fitting schemes. Finite-neighbourhood flatness is not promoted to flatness of the full failure scheme or auxiliary curves.

**Request 8 / architecture.** One principal sharp inverse theorem leads through spectral readout to the projective critical divisor and its real restriction. The dependency table is updated. Every web, operator, K3, polarized and boundary proof remains in the active complete supplement.

**Request 9 / sharpness and scope.** The smallest uniform order d=n^2+2n-4 is unchanged for all complex pencils, n>=3. No pairwise minimality or unmarked moduli-stack equivalence is claimed. On nonreduced bases, split semisimplicity explicitly requires idempotent projectors; semisimplicity of geometric fibres alone is not substituted for this hypothesis.

**B141-R2.1 / routing.** The root entry, current matrix and source lock refer to v144 and the controlling second-v141 report. Earlier root entries are archived. Native source is committed before the build; publication adds source-bound PDFs and receipts. A future mathematical change requires a new branch.

## Evidence boundary

The new results have proofs and exact regression checks. The full Ballico 1993 theorem-level comparison remains documentary-open. Computational success does not certify all proofs formally, exhaustive priority, or a top-four editorial outcome. No mathematical theorem has been weakened for that reason.
'''
put('RESPONSE_TO_REFEREES_V141_R2_V144.md',response)
put('LITERATURE_AUDIT_V144.md',r'''# A2 v144: inspected literature and the remaining full-text obligation

## Ballico 1996: numbered, six-axis comparison

E. Ballico, *On the failure cycles for the quadratic normality of a projective variety*, Pacific J. Math. 172 (1996), 307–313. Publisher full text: https://msp.org/pjm/1996/172-2/pjm-v172-n2-p01-s.pdf . Theorem 0.2 is on printed p. 308; Remark 1.2 and equation (6) on p. 311 identify the relative multiplication map. The theorem detects failure on finite codimension-two sections of a surface under a cohomological inequality. Browser PDF text was inspected; its screenshot endpoint failed, so no visual transcription is claimed.

| Axis | Specified 1996 statements | Present manuscript |
|---|---|---|
| Parameter | Linear sections of a fixed embedded variety, §1 | Pencils R, quotient algebras B_R and Gr(n,V+S_R) |
| Exact map | Relative section-cohomology multiplication, Remark 1.2, (6) | Literal Sym^m(O+K) -> B_R, m >= 2 |
| Scheme | Incidence construction and failure-sheaf support, §1–§2 | Maximal-minor scheme, not only support |
| Nilpotents | Finite section schemes allowed, Theorem 0.2 | Intrinsic ideal-adic neighbourhoods with first relation degree d |
| Relative structure | Pushforward construction over the section Grassmannian | Universal order-d neighbourhood over the relative socle |
| Inverse assertion | Theorem 0.2 detects failure | Unmarked order-d failure neighbourhood reconstructs a pencil up to one PGL transformation |

This compares these specified statements, not every possible implication of the paper. Relative failure constructions and nonreduced finite sections are not claimed as innovations of v144.

## Ballico 1993 remains distinct and unresolved

E. Ballico, *On the failure locus of higher order properties of embeddings in projective spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102. Metadata: https://onlinelibrary.wiley.com/doi/abs/10.1002/mana.19931630102 . Full theorem text was not obtained from the publisher or available file library. For each axis—parameter, exact map, scheme, nilpotents, relative structure, inverse assertion—the present-paper side is explicit, but the 1993 side remains `full text required`. No theorem number, map identity, nonanticipation or priority conclusion is invented. The 1996 comparison does not close B140.2.

## Classical critical count versus scheme-theoretic continuation

C. Fevola, Y. Mandelshtam and B. Sturmfels, *Pencils of quadrics: old and new*, arXiv:2009.04334v2, https://arxiv.org/pdf/2009.04334 , Theorem 4.2 and Conjecture 4.5. The semisimple generic reciprocal critical count 2r-3 and rational-score reduction are credited. The inherited manuscript retains its real-root argument.

Revision 144 instead supplies the projective score scheme across critical collisions, finite local freeness on the specified data open, equality with the original score ideal, ramification/Hessian equality and the triple-fibre trace-discriminant multiplicity. These are structural outputs of the finite inverse chain, not an exhaustive priority claim about likelihood literature.

## Classical scheme tools and the exact auxiliary operator

The Stacks Project: https://stacks.math.columbia.edu/tag/056Q (relative Cartier base change), https://stacks.math.columbia.edu/tag/062Y (relative Cartier criterion), https://stacks.math.columbia.edu/tag/0BVH (trace discriminant), and Tag 0BJF (etaleness criterion). The general tools are credited as classical. The monic presentation, score-ring identification and Hessian Schur factor are proved in the manuscript.

The v143 equality-level operator dictionary, the all-rank kernel theorem and Jacobian–Casimir proof remain unchanged in the active supplement. Read parts/27-operator-dictionary-v143.tex, parts/24-jacobian-casimir.tex and the preserved LITERATURE_AUDIT_V143.md. Exhaustive historical precedence for the restricted contraction is not newly certified.
''')
put('REFEREE_GUIDE_V144.md',r'''# Referee reading route — A2 v144

SOURCE_LOCK_V144.json defines the exact source SHA; the controlling report is the second v141 report.

Begin with the principal sharp finite reconstruction theorem and the dependency table. Follow the oriented ruling/coefficient proof into universal finite neighbourhoods and spectral Fitting readout. The reconstructed critical correspondence then leads to the new section The finite flat critical divisor and its ramification. Check the residue argument, both affine charts, radial elimination as ring maps, the local monic presentation, Hessian Schur factor and fixed-pencil triple fibre.

Every web/operator/K3/polar/boundary proof remains active in the technical supplement and complete manuscript. The v143 operator dictionary is retained. Read the response and literature audit before evaluating historical priority: Ballico 1996 has a numbered comparison; Ballico 1993 still requires its full theorem text.

The inverse theorem covers all complex pencils. Spectral readout requires regularity. The new critical divisor requires supplied split semisimple data with simple disjoint poles. Real structure and definiteness are extra inputs. Trace discriminant is not identified with the scheme-theoretic image of ramification. Build evidence is not formal proof or editorial acceptance.
''')
put('README.md',r'''# A2 revision 144 — finite failure schemes and quadratic pencils

**Finite failure schemes and the reconstruction of quadratic pencils**, Qian Qi, September 24, 2026.

Principal article: `geometry.tex` / `geometry.pdf`. Full technical supplement: `supplement.tex` / `supplement.pdf`. Complete manuscript: `complete.tex` / `complete.pdf`. Begin with REFEREE_GUIDE_V144.md and RESPONSE_TO_REFEREES_V141_R2_V144.md.

The controlling second-v141 report is at `3afecca5e65d7fe9c6784020ea6e813122938140`, reviewing `8cd389f4048a1047be9aa8e8e4f642595175a555`. The preserved predecessor is v143 at `40ef003998cbeb20f418e1b5e0dcfa9cfef9416d`. Earlier version directories and review branches are untouched.

Revision 144 extends finite-failure reconstruction through the full projective finite-flat critical divisor, Hessian ramification and trace discriminant, including a nonreduced triple fibre in one fixed pencil. Every inherited theorem and proof remains active without weakening. Scope and exact changes are in the response.

SOURCE_LOCK_V144.json and evidence/BUILD_RECEIPT_V144.json bind the native source SHA, twenty executed scripts, three PDFs, layout and preservation checks. Run `bash build.sh`; an isolated local tree needs A2_PREDECESSOR_DIR pointing to pinned v143. A local-preflight receipt is not a remote success. Complete predecessor source is archived under history/v143. Earlier tagged protocol files describe their own versions only.

LITERATURE_AUDIT_V144.md supplies the numbered Ballico 1996 comparison. The complete Ballico 1993 theorem-level comparison remains documentary-open. Exact regression is not formal proof, exhaustive priority or an editorial certificate. A further mathematical revision requires a new branch.
''')
archive=ROOT/'revisions/a2-v144/history';archive.mkdir(parents=True,exist_ok=True)
for name in ['README.md','CURRENT_REVIEW_ENTRY.md']:
 if (ROOT/name).exists():shutil.copy2(ROOT/name,archive/('ROOT_'+name))
(ROOT/'README.md').write_text('# Theta-Theory — A2 revision 144\n\nBegin at [CURRENT_REVIEW_ENTRY.md](CURRENT_REVIEW_ENTRY.md).\n\nThe [native A2 v144 manuscript]('+PREFIX+'/v144/README.md) retains all earlier mathematics and extends reconstruction through the projective critical divisor, ramification and collisions. Earlier root entries are archived in [revisions/a2-v144/history](revisions/a2-v144/history).\n')
(ROOT/'CURRENT_REVIEW_ENTRY.md').write_text('# Current A2 revision: 144\n\nNative manuscript: `'+PREFIX+'/v144/geometry.tex`.\n\nControlling second-v141 report: `'+REVIEW+'`. Preserved predecessor: `'+PIN+'`.\n\nNative source is published before compilation. No older receipt certifies this source. SOURCE_LOCK_V144.json and evidence/BUILD_RECEIPT_V144.json define the exact review object after a successful build.\n')
print('Assembled native v144; original parts and checks preserved.')
