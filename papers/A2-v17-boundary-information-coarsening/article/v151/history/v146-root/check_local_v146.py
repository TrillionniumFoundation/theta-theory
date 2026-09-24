#!/usr/bin/env python3
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
