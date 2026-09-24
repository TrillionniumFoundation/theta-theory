#!/usr/bin/env python3
"""Exact checks of spectral presentations, Artin square roots and nilpotent bases."""
from pathlib import Path
from itertools import combinations
from math import comb
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
x=s.symbols('x'); checks={};details={}
for lam,root in [(1,1),(4,2),(9,3),(-1,s.I)]:
 for order in range(1,9):
  h=root*sum(s.binomial(s.Rational(1,2),j)*((x-lam)/lam)**j for j in range(order))
  checks[f'Artin-root-{lam}-{order}']=s.rem(s.expand(h*h-x),(x-lam)**order,x)==0
factors=[(x-1)**3,(x-4)**2]
M=s.prod(factors);h=0
for lam,root,mod in [(1,1,factors[0]),(4,2,factors[1])]:
 order=s.degree(mod,x)
 loc=root*sum(s.binomial(s.Rational(1,2),j)*((x-lam)/lam)**j for j in range(order))
 other=s.div(M,mod,x)[0]
 h+=loc*other*s.invert(other,mod,x)
h=s.rem(h,M,x)
checks['CRT-square-root']=s.rem(h*h-x,M,x)==0
J3=s.eye(3);J3[0,1]=J3[1,2]=1
J2=4*s.eye(2);J2[0,1]=1
K=s.diag(J3,J2)
def reversal(n):return s.Matrix(n,n,lambda i,j: int(i+j==n-1))
A=s.diag(reversal(3),reversal(2));C=K*K+K
H=s.zeros(5)
for (power,),coef in s.Poly(h,x).terms():H+=coef*K**power
Ap=A*K;B=A*C;Bp=Ap*C
checks['nonsemisimple-matrix-root']=H*H==K
checks['self-adjoint-hypotheses']=K.T*A==A*K and C.T*A==A*C and Ap.T==Ap
checks['two-form-congruence']=H.T*A*H==Ap and H.T*B*H==Bp
checks['root-commutes']=H*C==C*H
u,v,w,z=s.symbols('u v w z');X=s.Matrix([[u,v],[w,z]])
for a in range(1,5):
 block=s.zeros(2*a)
 for j in range(a):
  block[2*j:2*j+2,2*j:2*j+2]=X
  if j+1<a:block[2*j+2:2*j+4,2*j:2*j+2]=-s.eye(2)
 P=s.Matrix.hstack(*[X**j for j in range(a)])
 target=s.Matrix.hstack(*([s.zeros(2)]*(a-1)+[X**a]))
 checks[f'polynomial-module-map-{a}']=s.simplify(P*block-target)==s.zeros(2,2*a)
 if a==2:
  minors=[block.extract(I,J).det() for I in combinations(range(4),3) for J in combinations(range(4),3)]
  entries=list(X**2)
  G=s.groebner(entries,u,v,w,z);F=s.groebner(minors,u,v,w,z)
  checks['full-Fitting-ideal-not-just-support']=all(G.reduce(q)[1]==0 for q in minors) and all(F.reduce(q)[1]==0 for q in entries)
eps=s.symbols('eps');Xd=s.Matrix([[0,1],[eps,0]])
checks['dual-number-spectral-incidence']=(Xd**2==eps*s.eye(2)) and s.rem((Xd**2).det(),eps**2,eps)==0
checks['dual-number-nonzero-incidence-ideal']=s.rem((Xd**2)[0,0],eps**2,eps)==eps

def parts(n,maximum=None):
 if n==0:yield ();return
 for first in range(min(n,maximum or n),1-1,-1):
  for rest in parts(n-first,first):yield (first,)+rest
part_count=0
for n in range(2,9):
 for partition in parts(n):
  J=s.diag(*[s.Matrix(k,k,lambda i,j:int(j==i+1)) for k in partition])
  lengths=[0]+[int(n-(J**a).rank()) for a in range(1,n+1)]
  expected=[sum(min(a,e) for e in partition) for a in range(n+1)]
  recovered=tuple(sum(1 for a in range(1,n+1) if lengths[a]-lengths[a-1]>=j) for j in range(1,len(partition)+1))
  checks[f'partition-{n}-{partition}']=lengths==expected and recovered==partition
  part_count+=1
checks['universal-rank-positive']=all(comb(n*n+n*n+2*n-4,n*n+2*n-4)-comb(n*(n+1)//2,2)>0 for n in range(3,11))
for m in [1,2,5,9]:
 graph=s.Matrix.vstack(s.eye(m),eps*s.eye(m))
 checks[f'first-relation-split-over-dual-numbers-{m}']=graph[:m,:]==s.eye(m) and graph[m:,:]==eps*s.eye(m)
out={'revision':141,'audit':'relative spectral and square-root calculations','ok':all(checks.values()),
 'arithmetic':'exact symbolic rational and Gaussian-rational arithmetic','partition_configurations':part_count,
 'checks':checks,'CRT_polynomial':str(h),'scope':'Finite audits; the universal bundle gluing and general proof are written in the manuscript.'}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION141_SPECTRAL_EXACT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
if not out['ok']:raise SystemExit('spectral exact audit failed')
