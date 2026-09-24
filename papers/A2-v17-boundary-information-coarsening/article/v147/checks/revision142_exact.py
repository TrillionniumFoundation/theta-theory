#!/usr/bin/env python3
"""Exact finite regression evidence, not a formal proof. Python 3 + SymPy."""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import factorial, comb, prod
from pathlib import Path
import json, random, time
import sympy as sp

def exterior_columns(n):
 pairs=[(i,j) for i in range(n) for j in range(i,n)];pos={p:i for i,p in enumerate(pairs)}
 terms=defaultdict(lambda:defaultdict(int))
 for choice in product(range(n),repeat=n):
  z=tuple(pos[tuple(sorted((a,i)))] for i,a in enumerate(choice))
  if len(set(z))<n:continue
  sign=(-1)**sum(z[i]>z[j] for i in range(n) for j in range(i+1,n))
  alpha=tuple(choice.count(i) for i in range(n));terms[alpha][tuple(sorted(z))]+=sign
 cols=sorted(terms);weights=[F(prod(factorial(b) for b in a),factorial(n)) for a in cols]
 return pairs,cols,weights,terms

def contraction_gram(n,r,data):
 pairs,cols,weights,terms=data;rows=defaultdict(lambda:defaultdict(F))
 for c,alpha in enumerate(cols):
  for z,v in terms[alpha].items():
   if not v:continue
   for k,w in enumerate(z):
    i,j=pairs[w]
    if i==j and i<r:rows[z[:k]+z[k+1:]][c]+=(-1)**k*v*weights[c]
 gram=defaultdict(F)
 for z,cs in rows.items():
  norm=F(1,2**sum(pairs[w][0]!=pairs[w][1] for w in z));cs={i:v for i,v in cs.items() if v}
  for i,a in cs.items():
   for j,b in cs.items():gram[i,j]+=norm*a*b
 return {k:v for k,v in gram.items() if v}

def casimir(n,cols):
 loc={a:i for i,a in enumerate(cols)};L=defaultdict(F)
 for j,beta in enumerate(cols):
  L[j,j]+=2*n*(n-1)
  for i in range(n):
   if beta[i]<2:continue
   for k in range(n):
    a=list(beta);a[i]-=2;a[k]+=2;L[loc[tuple(a)],j]-=beta[i]*(beta[i]-1)
 return {k:v for k,v in L.items() if v}

def partitions(n,bound=None):
 if n==0:yield ();return
 for x in range(min(n,bound or n),0,-1):
  for tail in partitions(n-x,x):yield (x,)+tail

def exact_checks():
 out={'kind':'exact finite regression; not a formal proof','gram_identities':[],'rank_strata':[],'mixed_identity_evaluations':0,'partition_pairs':0}
 for n in range(2,7):
  data=exterior_columns(n);_,cols,weights,_=data
  gram=contraction_gram(n,n,data);L=casimir(n,cols)
  expected={ij:F(2,2**n*n*(n-1))*weights[ij[0]]*v for ij,v in L.items()}
  assert gram==expected,(n,'Gram/Casimir identity')
  out['gram_identities'].append({'n':n,'domain_dimension':len(cols),'nonzero_entries':len(gram)})
  if n<=5:
   for r in range(n+1):
    g=contraction_gram(n,r,data)
    mat=sp.MutableSparseMatrix(len(cols),len(cols),{ij:sp.Rational(v.numerator,v.denominator) for ij,v in g.items()})
    nullity=len(cols)-sp.polys.matrices.DomainMatrix.from_Matrix(mat).rank()
    wanted=comb(2*n-r-1,n) if r<n else int(n%2==0)
    assert nullity==wanted,(n,r,nullity,wanted)
    out['rank_strata'].append({'n':n,'rank_q':r,'kernel_dimension':nullity})
 rng=random.Random(142)
 for n in range(2,9):
  for sample in range(12):
   x=sp.Matrix([rng.randrange(-3,4) for _ in range(n)]);a=sp.Matrix([rng.randrange(-3,4) for _ in range(n)])
   H=sp.Matrix(n,n,lambda i,j:rng.randrange(-2,3));H=H+H.T
   Q=sp.Matrix(n,n,lambda i,j:rng.randrange(-2,3));Q=Q+Q.T
   ell=(a.T*x)[0];J=ell*sp.eye(n)+x*a.T;b=Q*a;grad=(2*H*x).T;lhs=0
   for i in range(n):
    A=J.copy();A[i,:]=grad;lhs+=b[i]*A.det(method='domain-ge')
   rhs=4*ell**(n-1)*(x.T*H*Q*a)[0]-2*ell**(n-2)*(x.T*H*x)[0]*(a.T*Q*a)[0]
   assert lhs==rhs,(n,sample,lhs,rhs)
   out['mixed_identity_evaluations']+=1
 for m in range(1,17):
  ps=list(partitions(m))
  for c in range(1,m+1):
   block=[p for p in ps if len(p)==c]
   assert (len(block)==1)==(c==1 or m-c<=1)
   for lam in block:
    for mu in block:
     dom=all(sum(lam[:a])>=sum(mu[:a]) for a in range(1,c+1))
     profiles=all(sum(min(a,x) for x in mu)>=sum(min(a,x) for x in lam) for a in range(1,m+1))
     assert dom==profiles,(lam,mu)
     if dom and lam!=mu:
      ss=lambda p:sum(sum(x>=a for x in p)**2 for a in range(1,m+1))
      assert ss(mu)>ss(lam)
     out['partition_pairs']+=1
 return out
if __name__=='__main__':
 start=time.monotonic();result=exact_checks();result['elapsed_seconds']=round(time.monotonic()-start,3)
 target=Path(__file__).resolve().parents[1]/'evidence/revision142-exact.json'
 target.parent.mkdir(exist_ok=True);target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
