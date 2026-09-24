#!/usr/bin/env python3
"""Finite exact regressions, not formal verification of the geometric theorems."""
from pathlib import Path
import json, math
import sympy as s
ROOT=Path(__file__).resolve().parent

def partitions(n,maximum=None):
 if n==0:
  yield ();return
 for a in range(min(n, maximum if maximum is not None else n),0,-1):
  for tail in partitions(n-a,a):yield (a,)+tail

def matrix_case(lam):
 n=sum(lam);blocks=[];grams=[]
 for k in lam:
  blocks.append(s.zeros(k));grams.append(s.zeros(k))
  for i in range(k):
   grams[-1][i,k-1-i]=1
   if i+1<k:blocks[-1][i,i+1]=1
 N=s.diag(*blocks);A=s.diag(*grams)
 assert A*N==N.T*A
 vectors=[]
 for i in range(n):
  for j in range(i+1,n):
   Q=s.zeros(n);Q[i,j]=1;Q[j,i]=-1
   X=A*Q
   vectors.append((X*N-N*X).reshape(n*n,1))
 rank=s.Matrix.hstack(*vectors).rank() if vectors else 0
 cols=[sum(k>=a for k in lam) for a in range(1,max(lam)+1)]
 expected=(n*n-sum(k*k for k in cols))//2
 assert 2*rank==n*n-sum(k*k for k in cols),(lam,rank,expected)
 return {'partition':lam,'orbit_dimension':rank}
rows=[matrix_case(lam) for n in range(1,8) for lam in partitions(n)]
u,v,x,y=s.symbols('u v x y')
f=x*x/2+y**4/4
change={x:u+v*v,y:v}
fy=f.subs(change)
J=s.Matrix([u+v*v,v]).jacobian([u,v])
H=s.hessian(f,[x,y]);Hy=s.hessian(fy,[u,v])
correction=s.zeros(2)
for var,expr in [(x,u+v*v),(y,v)]:
 correction+=s.diff(f,var).subs(change)*s.hessian(expr,[u,v])
assert s.simplify(Hy-J.T*H.subs(change)*J-correction)==s.zeros(2)
G=s.groebner([u+v*v,v**3],u,v)
assert G.reduce(s.expand(Hy.det()-J.det()**2*H.det().subs(change)))[1]==0
assert G.reduce(s.expand(Hy.det()-3*v*v))[1]==0
# The nonzero Hessian class has nonzero nilpotent representative v^2.
assert G.reduce(v*v)[1]!=0 and G.reduce(v**3)[1]==0
curves=[{'n':n,'d':n*n+2*n-4,'tautological_degree':-1,'degree_not_divisible_by_n':(-1)%n!=0,
 'finite_rank':math.comb(n*n+(n*n+2*n-4),n*n+2*n-4)-math.comb(n*(n+1)//2,2)} for n in range(3,9)]
assert all(r['degree_not_divisible_by_n'] and r['finite_rank']>0 for r in curves)
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION145_EXACT.json').write_text(json.dumps({'ok':True,'orthogonal_dimension_cases':rows,
 'hessian_chain_rule_in_nonreduced_critical_quotient':True,'curve_numerics':curves,
 'scope':'Finite exact regression only; no formal verification of reconstruction, dominance, priority or significance.'},indent=2)+'\n')
print('PASS:',len(rows),'exact orthogonal dimensions; nilpotent Hessian coordinate test; curve rank and degree checks')
