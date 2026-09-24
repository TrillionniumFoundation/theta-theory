#!/usr/bin/env python3
"""Add the proved local inverse after the v145-preserving v146 assembly."""
from pathlib import Path
import json,re,shutil
BOOT=Path(__file__).resolve().parent
ROOT=BOOT.parents[1]
P=ROOT/'papers/A2-v17-boundary-information-coarsening/article/v146'
shutil.copy2(BOOT/'local-inverse.tex',P/'parts/32-local-inverse-v146.tex')
g=(P/'geometry.tex').read_text()
anchor='\\input{parts/31-moving-pencils-v146.tex}'
assert g.count(anchor)==1
(P/'geometry.tex').write_text(g.replace(anchor,anchor+'\n\\input{parts/32-local-inverse-v146.tex}'))
f=P/'frontmatter-v146.tex';s=f.read_text()
s=s.replace('projective base with nontrivial source projectivization','projective base with an arbitrary source bundle')
s=s.replace('filtered nilpotent automorphism kernel.','filtered nilpotent automorphism kernel.  Coefficient-support asymmetry\nalso yields reconstruction from a single unmarked Artin local algebra,\nwhose tangent-identity automorphism group is explicitly unipotent.')
f.write_text(s)
f=P/'parts/00-principal-introduction-v146.tex';s=f.read_text()
s=re.sub(r'A single unmarked Artinian normal[\s\S]*?local-algebra classification assertion\.',r'The geometric orientation used here has a local replacement: coefficient-support asymmetry.  Theorem~\\ref{thm:artin-local-inverse-v146} uses it to reconstruct the pencil from one unmarked Artin local algebra.',s)
addition=r'''\subsection{A single unmarked local algebra suffices}
The strongest form of the inverse needs no positive-dimensional support.
Choose an \(n\)-dimensional source space \(U\), write \(T=(t_{ij})\)
for its universal map to \(V\), and let \(\mathfrak m=(t_{ij})\).
Define
\[
 \mathfrak A_R^{[d]}=
 \C[t_{ij}]/\bigl((\det T)I_p(\gamma_R\Sym^2T)
                                      +\mathfrak m^{d+1}\bigr).
\]
\begin{theorem}[Local algebraic inverse]\label{thm:principal-local-v146}
For every pair of complex quadratic pencils, an ungraded algebra
isomorphism \(\mathfrak A_R^{[d]}\simeq\mathfrak A_{R'}^{[d]}\)
exists if and only if \(R'=gR\) for some \(g\in\PGL(V)\).
The order \(d=n^2+2n-4\) is the smallest uniform order already for
these single-point objects.
\end{theorem}
The full statement and proof are
Theorem~\ref{thm:artin-local-inverse-v146}.  The extra local ingredient
is that the residual coefficient module has factor-support ranks
\((1,\binom N2)\).  Transposition reverses these unequal ranks and
therefore cannot carry one pencil ideal to another.  This orients the
unordered matrix factors without a nontrivial projective bundle.
Theorem~\ref{thm:unrestricted-moving-v146} consequently removes that
restriction from the moving-family theorem as well.  This is not a
claim that the reduced determinant cone alone remembers the pencil:
the nonreduced first relation kernel and its residual coefficients
are indispensable.  Proposition~\ref{prop:local-automorphisms-v146}
also identifies the entire tangent-identity kernel, including its
affine-space parametrization and nonadditive group law.

'''
anchor='\\subsection{The intrinsic mechanism}'
assert s.count(anchor)==1
s=s.replace(anchor,addition+anchor)
s=s.replace('let \\(\\mathcal U\\) have rank \\(n\\) with nontrivial\nprojectivization,','let \\(\\mathcal U\\) have rank \\(n\\),')
f.write_text(s)
check=r'''#!/usr/bin/env python3
"""Exact finite support-rank and local-automorphism regressions, not a proof checker."""
from pathlib import Path
from itertools import combinations
from random import Random
import json,math
import sympy as S
P=1000003
rng=Random(146032)
def rank(A):
    A=[list(map(lambda x:x%P,row)) for row in A]
    if not A:return 0
    r=0
    for j in range(len(A[0])):
        pivot=next((i for i in range(r,len(A)) if A[i][j]),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r];q=pow(A[r][j],P-2,P)
        A[r]=[(q*x)%P for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][j]:
                q=A[i][j];A[i]=[(x-q*y)%P for x,y in zip(A[i],A[r])]
        r+=1
        if r==len(A):break
    return r
def det(A):
    A=[row[:] for row in A];v=1
    for j in range(len(A)):
        i=next((i for i in range(j,len(A)) if A[i][j]%P),None)
        if i is None:return 0
        if i!=j:A[i],A[j]=A[j],A[i];v=-v
        pivot=A[j][j]%P;v=v*pivot%P;q=pow(pivot,P-2,P)
        for i in range(j+1,len(A)):
            a=A[i][j]*q%P
            for k in range(j,len(A)):A[i][k]=(A[i][k]-a*A[j][k])%P
    return v%P
pairs=list(combinations(range(3),2))
quad=[(i,j) for i in range(3) for j in range(i,3)]
columns=list(combinations(range(6),4))
def sym2(T):
    return [[(T[a][i]*T[a][j] if a==b else T[a][i]*T[b][j]+T[b][i]*T[a][j])%P for i,j in quad] for a,b in quad]
def coeff(T,kernel):
    A=sym2(T);rows=[i for i in range(6) if i not in kernel]
    return [det([[A[i][j] for j in J] for i in rows]) for J in columns]
rows=[]
for kernel in [(0,1),(0,3),(1,4)]:
    values=[]
    for _ in range(48):
        T=[[rng.randrange(P) for _ in range(3)] for _ in range(3)]
        Tt=[list(x) for x in zip(*T)]
        values.append(coeff(T,kernel)+coeff(Tt,kernel))
    a=rank([r[:15] for r in values]);b=rank([r[15:] for r in values]);ab=rank(values)
    assert (a,b,ab)==(15,15,29),(kernel,a,b,ab)
    rows.append({'kernel_monomial_indices':kernel,'original_rank':a,'transposed_rank':b,'combined_rank':ab,'intersection_dimension_in_evaluations':a+b-ab})
# Exact tensor-support ranks: the full-right and full-left modules cannot agree.
beta=S.Matrix([1,2,3]);K=S.kronecker_product(beta,S.eye(3))
left=S.Matrix.hstack(*[S.Matrix([K[3*i+r,j] for i in range(3)]) for r in range(3) for j in range(3)])
right=S.Matrix.hstack(*[S.Matrix([K[3*i+r,j] for r in range(3)]) for i in range(3) for j in range(3)])
assert (left.rank(),right.rank())==(1,3)
# A model first-relation algebra tests arbitrary, not merely triangular, generator corrections.
x,y=S.symbols('x y');d=5
basis=[(a,k-a) for k in range(d+1) for a in range(k+1) if (a,k-a) not in {(5,0),(0,5)}]
def reduction(f):
    p=S.Poly(S.expand(f),x,y)
    return {m:a for m,a in p.terms() if sum(m)<=d and m not in {(5,0),(0,5)}}
X=x+x*y+y*y+x**4;Y=y+x*x+x*y*y
assert not reduction(X**5) and not reduction(Y**5)
C=S.zeros(len(basis))
for j,(a,b) in enumerate(basis):
    q=reduction(X**a*Y**b)
    for i,m in enumerate(basis):C[i,j]=q.get(m,0)
assert C.det()==1 and all(C[i,i]==1 for i in range(len(basis)))
assert (C-S.eye(len(basis)))**(d+1)==S.zeros(len(basis))
numerics=[]
for n in range(3,7):
    a=n*n;N=n*(n+1)//2;d=n*n+2*n-4;length=math.comb(a+d,d)-math.comb(N,2)
    numerics.append({'n':n,'d':d,'length':length,'tangent_identity_kernel_dimension':a*(length-1-a)})
result={'ok':True,'prime':P,'pencil_coefficient_evaluation_cases':rows,'support_ranks':[1,3],
 'model_arbitrary_corrections_invertible':True,'model_algebra_dimension':len(basis),'local_rank_numerics':numerics,
 'proof_certified':False,'scope':'Finite exact checks. Finite-field evaluations separate these concrete transposed coefficient modules; the all-pencil orientation and local inverse are proved in the manuscript, not established by sampling.'}
E=Path(__file__).resolve().parent/'evidence';E.mkdir(exist_ok=True)
(E/'LOCAL_INVERSE146_EXACT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
'''
(P/'check_local_v146.py').write_text(check)
f=P/'check_v146.py';f.write_text(f.read_text().replace('for d in (13,20):','for d in (11,20):'))
f=P/'revision_v146.py';s=f.read_text()
s=s.replace("['check_v145.py','check_v146.py']","['check_v145.py','check_v146.py','check_local_v146.py']")
s=s.replace('len(records)==22','len(records)==23').replace('twenty_two_scripts_executed_successfully','twenty_three_scripts_executed_successfully').replace('All 22 executed','All 23 executed')
s=s.replace('New in v146: intrinsic reconstruction of nonconstant pencil subbundles','New in v146: an unmarked single-point Artin local inverse, coefficient-support orientation, an explicit local unipotent kernel, and intrinsic reconstruction of nonconstant pencil subbundles')
anchor="    records=json.loads((e/'EXECUTED_CHECKS_V146.json').read_text())"
assert s.count(anchor)==1
s=s.replace(anchor,"    checks['local_inverse_exact_regression_passed']=json.loads((e/'LOCAL_INVERSE146_EXACT.json').read_text())['ok']\n    checks['local_inverse_and_unrestricted_family_present']={'thm:artin-local-inverse-v146','thm:unrestricted-moving-v146','prop:local-automorphisms-v146','lem:coefficient-orientation-v146'}<=set(labels(main))\n"+anchor)
f.write_text(s)
for n in ['README.md','RESPONSE_TO_V144_REPORTS_V146.md']:
    f=P/n;s=f.read_text().replace('22 regression scripts','23 regression scripts').replace('twenty-one v145 exact-regression scripts plus the new v146 script','twenty-one v145 exact-regression scripts plus the two new v146 scripts')
    s=s.replace('with rank-n source bundle whose projectivization is nontrivial','with an arbitrary rank-n source bundle')
    s=s.replace('The new intrinsic reduction is smooth, projective and reduced, with nontrivial right projective bundle.','The family inverse has smooth connected projective reduced base. The coefficient-support theorem removes the nontrivial-right-projective-bundle assumption and allows a point.')
    f.write_text(s)
addendum='''\n## Principal strengthening: a single unmarked Artin local algebra\n\nThe final v146 theorem `thm:artin-local-inverse-v146` reconstructs every complex pencil from `C[t_ij]/((det T) I_p(gamma_R Sym^2 T)+(t_ij)^(d+1))`, without grading, generators, tangent coordinates, tensor factors or a positive-dimensional support. The order `d=n^2+2n-4` is still smallest uniform. This is not inferred from a reduced determinant cone. The first relation kernel reconstructs the homogeneous cone; its determinant quotient supplies the coefficient module.\n\nThe new conceptual ingredient is `lem:coefficient-orientation-v146`: in a multiplicity-one Cauchy summand, a proper nonzero left coefficient space tensored with the full right factor has unequal factor-support ranks. A transposed matrix map exchanges those ranks and cannot identify two ideals of that type. For every pencil the ranks are `(1, binomial(N,2))`, so transposition is excluded even at one point. This is a local intrinsic orientation criterion and applies beyond the particular projective-bundle obstruction used in the earlier proof.\n\nTheorem `thm:unrestricted-moving-v146` consequently removes the source-projectivization restriction from the whole moving-family theorem. The earlier restricted theorem and its proof remain valid special cases and are preserved. Proposition `prop:local-automorphisms-v146` gives the full local tangent-identity kernel: every generator may receive an arbitrary element of the squared maximal ideal. The kernel is a unipotent algebraic group, with affine-space underlying variety of dimension `n^2(length-1-n^2)`, and generally nonadditive group law. This replaces the earlier limitation to curve-supported reconstruction by a proved stronger inverse, not by a weakened claim.\n\nA second new script checks support ranks, three concrete genuine three-variable pencil coefficient spaces against their transposes by exact finite-field evaluation, and general higher-order corrections in a first-relation algebra. All 23 scripts are executed. Sampling does not prove the universal orientation theorem; the representation-theoretic support argument supplies that proof. The Ballico 1993 full-text priority comparison remains documentary-open and is not discharged by this strengthening.\n'''
for n in ['README.md','RESPONSE_TO_V144_REPORTS_V146.md']:
    f=P/n;f.write_text(f.read_text()+addendum)
f=P/'LITERATURE_AUDIT_V146.md';s=f.read_text().replace('the right projective bundle is nontrivial','the source bundle is arbitrary; coefficient-support asymmetry supplies orientation, including over a point')
s=s.replace('All-pencil inverse; moving-family and actual-bundle reconstruction; geometric automorphism quotient and nilpotent kernel','Unmarked single-point Artin inverse; unrestricted moving-family and actual-bundle reconstruction; geometric automorphism quotient and explicit local unipotent kernel')
s+='\nThe new local orientation criterion is the elementary contraction-support argument inside the classical Cauchy summand. Its use to exclude transposition is proved here; no priority claim is made for Cauchy decomposition itself. The full 1993 comparison remains unverified.\n'
f.write_text(s)
f=P/'ISSUE_MATRIX_V146.json';x=json.loads(f.read_text())
x['issues']['1_5_11_16_intrinsic_consequence']='new proof: one unmarked Artin local algebra reconstructs every pencil; asymmetric coefficient supports exclude transposition; moving-family inverse has arbitrary source bundle; explicit local unipotent kernel; editorial significance remains independently assessable'
x['issues']['14_evidence']='23 actual script statuses, three native PDFs and source hashes required; finite computations do not certify universal proofs or priority'
x['issues']['15_5_15_6_scope']='all-pencil local and family inverses; smooth connected projective reduced base may be a point; source projective nontriviality removed; separate marked-socle nonreduced-base, regular, split and real conditions retained'
f.write_text(json.dumps(x,indent=2)+'\n')
print('Added the local inverse, unrestricted moving theorem and 23rd exact-regression script')
