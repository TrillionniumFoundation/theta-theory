"""Materialize v50 native sources, retaining the complete v49 mathematical text."""
from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path
HOME=Path(__file__).resolve().parent
OLD=HOME.parent/'GTF-I-v49-robust-duality'
REVIEW='d9f3273b3575517cc54054a79412fe3d09378fa7'
PUBLICATION='0a33f027a9088c4a55542efcd2784de95f43f557'

def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def main()->None:
    inherited=HOME/'inherited';inherited.mkdir(exist_ok=True)
    expected=json.loads((HOME/'EXPECTED_V49.json').read_text())
    for name,checksum in expected['files'].items():
        if digest(OLD/name)!=checksum:raise RuntimeError('Pinned v49 source drift: '+name)
    edits={}
    names=[p.name for p in OLD.glob('*.tex') if p.name not in {'main.tex','inherited-introduction.tex','v47-introduction.tex'}]
    names += ['check_duality.py','check_compatibility.py','verify_inherited.py','dual_certificate.py','finite_bit.py']
    for name in names:shutil.copyfile(OLD/name,inherited/name)
    def replace(name:str,old:str,new:str,note:str)->None:
        p=inherited/name;s=p.read_text()
        if s.count(old)!=1:raise RuntimeError('Unique editorial anchor missing: '+name+' '+note)
        p.write_text(s.replace(old,new));edits.setdefault(name,[]).append(note)
    replace('introduction.tex',r'\section{Introduction}',r'\section{The two-state structural alternative}', 'Retitle current two-state summary, not another historical introduction')
    replace('introduction.tex','This paper develops an exact global error alternative in the','The two-state component develops an exact global error alternative in the','Scope two-state summary within integrated paper')
    replace('introduction.tex','where $v$ is the number of essential factors.',r'where $v=|V_\delta|$ is the number of essential factor coordinates at the tested threshold $\delta$. The sparsity bound is per rejected chamber.','r31.10.1-2 threshold-dependent count')
    oldtarget=r'''For the retained orthogonal-word results, the target is
\begin{equation}\label{eq:target}
 \Pp(B=b\mid x,w,j)=\frac{1+b\rho\ip{e_j}{U_wx}}2,
 \qquad b\in\{-1,1\}.
\end{equation}'''
    replace('introduction.tex',oldtarget,'The orthogonal-word target is equation~\\eqref{eq:target}, stated in the introduction.','Move target equation to common introduction, preserving exact law')
    replace('machine-model.tex','No distribution on command words is part of the specification.','No distribution on command words is part of the specification. Unless a theorem explicitly restricts the query set, every coordinate query is available. The calibration lemma below uses that full query set; the selected-query example does not invoke it.','Make the selected-query/full-coordinate boundary explicit')
    replace('machine-model.tex','We keep $\\rho\\le1/10$','For the retained planar arithmetic results we keep $\\rho\\le1/10$','Do not override explicit signal ranges of new theorems')
    replace('magnitude-duality.tex',r'a_v=\max_{e\ni v}(|f_e|-\delta)>0.',r'0<a_v=\max_{e\ni v}(|f_e|-\delta)\le1.','r31.10.3 factor lower cap in (0,1]')
    replace('magnitude-duality.tex','A chamber with some $U_e\\le0$ is rejected:', 'Every surviving entry is retained, including inactive entries all of whose factor coordinates survive. A positive upper endpoint means $U_e>0$. A chamber with some $U_e\\le0$ is rejected:','r31.10.4-5 surviving inactive entries and strict upper endpoint')
    replace('magnitude-duality.tex','For $e\\in\\mathcal I$, let $b_e', 'To distinguish the exponent incidence data from right-hand-side bases, we use $\\nu_e$ for an entry incidence vector. For $e\\in\\mathcal I$, let $b_e','r31.10.6 distinguish incidence and bases')
    # Rename only incidence symbols, not the later base b_i or vector b.
    p=inherited/'magnitude-duality.tex';p.write_text(p.read_text().replace('b_e',r'\nu_e'))
    replace('magnitude-duality.tex','The input comprises defining polynomials, isolating intervals, and','For effective input, a common primitive element and isolating interval specify the coefficient field, and each entry has explicit coordinates in that field. Positive rational powers always mean the positive real branch. The input comprises defining polynomials, isolating intervals, and','r31.10.9-10 coefficient representation and positive branches')
    replace('exact-error-examples.tex','The feasible tolerance in this stratum is the intersection of the\none-dimensional intervals determined by these multiplicative tests.','The feasible set in this fixed chamber and stratum is the intersection of all multiplicative-test intervals and the endpoint conditions $U_e>0$. The full optimizer also tests the stratum endpoints separately.','r31.10.11 fixed-stratum feasible set')
    replace('exact-error-examples.tex','Every decomposable tensor satisfies','The five entries used below are $000,011,101,110,111$. Every decomposable tensor satisfies','r31.10.12 identify circuit entries')
    replace('exact-error-examples.tex','All factors belong to $(0,1)$.',r'''For completeness the weight-one calculation is
\[
 D^2=A^{4/3}B^{2/3}=A(AB^2)^{1/3}=AC,
 \qquad \frac4{25}<\frac9{25}\frac{539}{1000}<AC
 <\frac{361}{1000}\frac{27}{50}<\frac14.
\]
All powers use their positive real branches. All factors belong to $(0,1)$.''','r31.10.13 explicit weight-one rational bounds')
    replace('exact-error-examples.tex','The same circuit lower bound with $\\delta/\\rho$ proves sharpness.',r'''The scaled lower constraint is explicitly
\[
 (4\rho/5-\delta)^3\le(\rho/10+\delta)(2\rho/5+\delta)^2;
\]
division by $\rho^3$ proves sharpness.''','r31.10.14 scaled lower inequality')
    replace('exact-error-examples.tex','An all-rational machine at this fixed finite horizon has rational','Here all-rational means that every initialization, transition and decoder coefficient is rational. Such a machine at this fixed finite horizon has rational','r31.10.15 define rational machine')
    replace('exact-error-examples.tex','Inside retain an identity word and a word with exactly one swap.','For cuts $s<t$, retain the macro-words $0^{t-s}$ and $10^{t-s-1}$ inside them and fix query $j=1$.','r31.10.17 specify macro-words and query')
    replace('exact-error-examples.tex','Both examples use actual\nnonidentical commands and a positive horizon.','Both examples use actual nonidentical commands and a positive horizon. The identity and swap commute; noncommutativity is supplied instead by Theorem~\\ref{thm:orthogonal50}.','r31.10.18 old example commuting')
    replace('encoding-and-comparison.tex','is NP-complete. This is a direct transfer','is NP-complete. Here $\\varepsilon$ is binary-TV tolerance and $2\\varepsilon$ is mean tolerance. This is a direct transfer','r31.10.19 mean versus binary-TV tolerance')
    replace('encoding-and-comparison.tex','obtained from an appropriate basic system.','obtained from an appropriate basic system by Cramer\'s rule: after clearing denominators, $q$ variables and coefficient bit length $L$ give determinant bit length $O(q(L+\\log(q+1)))$. The feasible set is pointed because $t_i\\ge1$ and $0\\le\\beta_a\\le1$, so a basic feasible point exists. This is the standard rational-polyhedron argument; compare \\cite[Chapter 10]{Sch86}.','r31.10.20 explicit basic-feasible-solution bit bound')
    replace('encoding-and-comparison.tex','It does not classify general three-state or larger\nhidden realizations.','This two-state optimizer does not classify general three-state or larger hidden realizations. The distinct rank-tight geometric results of Section~\\ref{sec:simplex50} do apply beyond two states under their stated spanning and orthogonality hypotheses.','Scope inherited limitation in presence of new rank-tight results')
    replace('dual_certificate.py',"parser.add_argument('--max-rows',type=int,default=50000)","parser.add_argument('--max-rows',type=int,default=50000,help='Maximum Fourier-Motzkin rows (default 50000); exhaustion returns undetermined')\n    parser.add_argument('--max-sign-variables',type=int,default=20,help='Maximum essential factor-sign variables (default 20); exhaustion returns undetermined')",'r31.10.23 expose and describe both resource limits')
    p=inherited/'dual_certificate.py';p.write_text(p.read_text().replace('max_rows=args.max_rows)','max_rows=args.max_rows,max_sign_variables=args.max_sign_variables)'))
    replace('references.tex',r'\end{thebibliography}',r'''\bibitem{KKKR17} T. Kahle, K. Kubjas, M. Kummer and Z. Rosen,
The geometry of rank-one tensor completion,
\emph{SIAM J. Appl. Algebra Geom.} \textbf{1} (2017), 200--221;
arXiv:1605.01678v2, Section 2.
\bibitem{Sch86} A. Schrijver,
\emph{Theory of Linear and Integer Programming}, Wiley, 1986, Chapter 10.
\end{thebibliography}''','r31.9.2 and 10.20-21 tensor-completion and rational-LP references')
    oldmain=(OLD/'main.tex').read_text();preamble=oldmain.split(r'\title')[0]
    body=r'''\title[Compatible simplices and stochastic width]{General Theta Foundations I: \\
Compatible Simplices and Exact Stochastic Width}
\author{Qian Qi}
\date{27 September 2026; revision 50}
\begin{document}
\begin{abstract}
We study finite stochastic realizations of controlled orthogonal
experiments. At minimal Hankel rank, equality of row spaces eliminates
hidden future directions and identifies every state with a vertex of a
compatible simplex. The simplex difference-body identity gives a
quantitative occupation bound for minimal-width cuts, even with
arbitrarily wider intervening registers. This yields an exact four-state
frontier for a class of planar signed-permutation alphabets, including
noncommuting ones. Exact minimal-width realization at every horizon is
equivalent to a single invariant simplex and hence to a finite
permutation action. We further compute a strict separation between
word-distortion and enclosure profiles: the former vanish for the
antipodal alphabet while minimal-simplex dilation is exactly the
ambient dimension. A rational nine-dimensional orthogonal experiment
with three command epochs has a cubic two-state optimum strictly above
all separate flattening bounds. The full two-state sign--magnitude
alternative and the prior arithmetic and finite-bit realization
theorems are retained, with explicit certificate-size bounds and a
direct comparison to tensor-completion geometry. The resource is
nonuniform clocked atomic-row label width.
\end{abstract}
\maketitle
\input{introduction.tex}
\input{inherited/machine-model.tex}
\input{inherited/hankel-compatibility.tex}
\input{compatible-simplex.tex}
\input{orthogonal-circuit.tex}
\input{inherited/introduction.tex}
\input{inherited/two-state-compatibility.tex}
\input{inherited/magnitude-duality.tex}
\input{inherited/exact-error-examples.tex}
\input{certificate-complexity.tex}
\input{inherited/encoding-and-comparison.tex}
\input{inherited/inherited-statements.tex}
\input{inherited/finite-horizon-certificates.tex}
\input{inherited/word-profiles.tex}
\input{inherited/distortion-rate.tex}
\input{inherited/circle-optimization.tex}
\input{inherited/arithmetic-scales.tex}
\input{inherited/metric-width.tex}
\input{inherited/irrational-fluctuations.tex}
\input{inherited/finite-bit-memory.tex}
\input{inherited/comparison.tex}
\input{inherited/references.tex}
\end{document}
'''
    (HOME/'main.tex').write_text(preamble+body)
    manifest={'schema':'gtf50.preservation/1','review_commit':REVIEW,'v49_publication':PUBLICATION,
      'policy':'Every v49 manuscript theorem and proof retained. Old repository paths unchanged. Only copied sources edited, as listed. Prior redundant historical introductions remain at their original paths, not in compact submission.',
      'files':{name:{'v49_sha256':digest(OLD/name),'v50_sha256':digest(inherited/name),'amendments':edits.get(name,[])} for name in sorted(names)},
      'archival_paths_untouched':['papers/GTF-I-v49-robust-duality/complete-manuscript.pdf','papers/GTF-I-v49-robust-duality/complete-development.pdf'],
      'label_preservation':'build.py verifies every theorem/equation label in a loaded v49 manuscript module is present in current native sources.'}
    (HOME/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'materialized','native_files':len(names)+2,'edited_copies':len(edits)}))
if __name__=='__main__':main()
