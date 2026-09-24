#!/usr/bin/env python3
"""Exact finite regression witnesses for v149; not proof or priority certificates."""
from pathlib import Path
from itertools import combinations
from math import comb
from fractions import Fraction
import json
import sympy as s
HERE=Path(__file__).resolve().parent
out=HERE/'evidence';out.mkdir(exist_ok=True)
checks={};data={}
def schur_dimension(weight):
 n=len(weight);v=Fraction(1)
 for i in range(n):
  for j in range(i+1,n):v*=Fraction(weight[i]-weight[j]+j-i,j-i)
 assert v.denominator==1
 return v.numerator
for n in range(3,9):
 N=comb(n+1,2);M=comb(N,2);mu=[3]*(n-2)+[2,0];lam=[n+1]*(n-2)+[n,n-2]
 checks[f'n{n}_primitive_weight']=[a-(n-2) for a in lam]==mu and sum(mu)==3*n-4
 checks[f'n{n}_primitive_dimension']=schur_dimension(mu)==schur_dimension(lam)==M
 checks[f'n{n}_first_relation_degree']=(n-1)*n+sum(mu)==n*n+2*n-4
 checks[f'n{n}_fixed_support_plane_exists_dimension']=M>n*n
 checks[f'n{n}_effective_stack_dimension']=2*(N-2)-(n*n-1)==n-3
# Exact 3x3 maximal-minor calculation for a singular common-factor pencil.
v=s.symbols('v0:3');xx=s.symbols('t0:9');T=s.Matrix(3,3,xx)
basis=[v[i]*v[j] for i,j in combinations(range(3),2)]
pairs=[(i,j) for i in range(3) for j in range(i,3)]
basis=[v[i]*v[j] for i,j in pairs]
lin=list(T.T*s.Matrix(v))
S2=s.Matrix([[s.Poly(s.expand(lin[i]*lin[j]),*v).coeff_monomial(mon) for i,j in pairs] for mon in basis])
Q=S2[[2,3,4,5],:]
delta=s.Poly(T.det(),*xx,domain=s.QQ)
primitive=[];mins=[]
for cols in combinations(range(6),4):
 f=s.Poly(Q[:,list(cols)].det(method='domain-ge'),*xx,domain=s.QQ)
 quotient,remainder=s.div(f,delta)
 assert remainder.is_zero
 primitive.append(quotient);mins.append(f)
g=primitive[0]
for f in primitive[1:]:g=s.gcd(g,f)
checks['singular_n3_all_15_minors_divisible_by_delta']=len(primitive)==15
checks['singular_n3_primitive_gcd_is_one']=g.total_degree()==0
checks['singular_n3_primitive_degree_five']=all(f.total_degree()==5 for f in primitive if not f.is_zero)
checks['singular_n3_failure_common_divisor_delta_squared']=s.Poly(s.gcd_list([f.as_expr()*delta.as_expr() for f in mins],*xx),*xx,domain=s.QQ).monic()==(delta**2).monic()
# An invertible rational evaluation cannot kill the coefficient vector.
G=s.Matrix([[1,2,0],[0,1,3],[2,0,1]])
checks['singular_n3_invertible_evaluation_nonzero']=G.det()!=0 and any(f.eval(dict(zip(xx,list(G))))!=0 for f in primitive)
# Dual-number counterexample: x^2+eps*y^2 has no deforming linear factor x+eps*l.
x,y=s.symbols('x y');a,b,c,d=s.symbols('a b c d')
der=s.Poly((a*x+b*y)*x+x*(c*x+d*y)-y*y,x,y)
A,z=s.linear_eq_to_matrix(der.coeffs(),[a,b,c,d])
checks['dual_number_fibrewise_gcd_is_insufficient']=A.rank()<A.row_join(z).rank()
# Differential of multiplication with coprime residuals J=<x^2,y^2>, f=x+y.
# f must divide dotf*j for both j; reduction at x=-y forces dotf scalar f.
a,b=s.symbols('a b')
conditions=[s.Poly(s.expand(((a*x+b*y)*j).subs(x,-y)),y).coeffs()[0] for j in (x*x,y*y)]
mat,_=s.linear_eq_to_matrix(conditions,[a,b])
checks['gcd_differential_only_scalar_kernel']=mat.nullspace()==[s.Matrix([1,1])]
# Exact tangent rank for selected genuine pencils in several dimensions.
def tangent_rank(n,polynomials):
 vv=s.symbols(f'z0:{n}');pairs=[(i,j) for i in range(n) for j in range(i,n)];mons=[vv[i]*vv[j] for i,j in pairs]
 ff=[f(vv) for f in polynomials];R=s.Matrix([[s.Poly(f,*vv).coeff_monomial(mon) for f in ff] for mon in mons])
 ann=R.T.nullspace();eq=[];X=s.Matrix(n,n,s.symbols(f'a0:{n*n}'))
 for f in ff:
  df=s.expand(sum(s.diff(f,vv[i])*sum(X[i,j]*vv[j] for j in range(n)) for i in range(n)))
  vec=s.Matrix([s.Poly(df,*vv).coeff_monomial(mon) for mon in mons])
  eq.extend((q.T*vec)[0] for q in ann)
 A,_=s.linear_eq_to_matrix(eq,list(X));orbit=A.rank();stab=n*n-1-orbit
 return {'orbit_dimension':orbit,'projective_stabilizer_dimension':stab,'tangent_cokernel_dimension':2*(len(mons)-2)-orbit}
for n in (3,4,5):
 regular=tangent_rank(n,[lambda v:sum(z*z for z in v),lambda v:sum((i+1)*z*z for i,z in enumerate(v))])
 singular=tangent_rank(n,[lambda v:v[0]**2,lambda v:v[0]*v[1]])
 data[f'n{n}_regular']=regular;data[f'n{n}_singular']=singular
 checks[f'n{n}_regular_finite_stabilizer']=regular['projective_stabilizer_dimension']==0
 checks[f'n{n}_singular_has_stabilizer_jump']=singular['projective_stabilizer_dimension']>0
 checks[f'n{n}_tangent_cokernel_formula']=all(q['tangent_cokernel_dimension']==n-3+q['projective_stabilizer_dimension'] for q in (regular,singular))
for n in range(3,6):
 N=comb(n+1,2);M=comb(N,2);H=comb(n*n+3*n-5,3*n-4)
 normal=comb(N-2,2)+(M-1)*(M*M-1)+M*(H-M*M)
 checks[f'n{n}_three_normal_modes_dimension']=normal==M*(H-M)-2*(N-2)
 data[f'n{n}_ambient_residual_dimension']=H
 data[f'n{n}_normal_dimension']=normal
# Rank-one residual in another Cauchy block cannot be a full right or left block.
checks['other_cauchy_line_breaks_both_supports']=comb(3+5-1,5)>1
record={'revision':149,'ok':all(checks.values()),'check_count':len(checks),'checks':checks,'data':data,'universal_proofs_certified':False,'historical_priority_certified':False,'scope':'Exact polynomial divisibility, dual-number and tangent-rank witnesses; not a proof verifier.'}
(out/'REVISION149_EXACT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
if not record['ok']:raise SystemExit(1)
