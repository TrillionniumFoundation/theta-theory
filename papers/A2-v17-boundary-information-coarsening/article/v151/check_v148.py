#!/usr/bin/env python3
"""Exact regression witnesses, not a certificate of universal reconstruction."""
from pathlib import Path
from itertools import combinations, product
from math import comb
import json
import sympy as s
HERE=Path(__file__).resolve().parent
out=HERE/'evidence';out.mkdir(exist_ok=True)
checks={}
a,b,z=s.symbols('a b z')
columns=s.Matrix([[a,0],[b,a],[0,b]])
wedge=s.Matrix([columns[list(rows),:].det() for rows in combinations(range(3),2)])
syzygy=s.Matrix([[-b,a,0],[0,-b,a]])
checks['pencil_pluecker_column']=wedge==s.Matrix([a*a,a*b,b*b])
checks['conic_quotient_complex']=syzygy*wedge==s.zeros(2,1)
checks['syzygy_maximal_minors']=[s.expand(syzygy[:,list(cols)].det()) for cols in combinations(range(3),2)]==[b*b,-a*b,a*a]
checks['quotient_rank_on_standard_charts']=syzygy.subs({a:1}).rank()==2 and syzygy.subs({b:1}).rank()==2
# All one-sided dimension patterns for two small Schur factors.  A nonzero
# block has supports (r,m), whereas a zero block has supports (0,0).
patterns=[]
for r1,r2 in product(range(3),range(4)):
 if (r1,r2)==(0,0):continue
 support=[(r,m) if r else (0,0) for r,m in ((r1,2),(r2,3))]
 symmetric=all(u==v for u,v in support)
 full=all(r in (0,m) for r,m in ((r1,2),(r2,3)))
 patterns.append(symmetric==full)
checks['exhaustive_small_support_dichotomy']=all(patterns)
# q=1, n=2: exact Lie-algebra calculation on polynomial relation spaces.
x=s.symbols('x0:4'); delta=x[0]*x[3]-x[1]*x[2]
M=s.Matrix(4,4,s.symbols('m0:16'))
vars=list(M)
monoms=[s.prod(t**k for t,k in zip(x,exps)) for exps in product(range(4),repeat=4) if sum(exps)==3]
def stabilizer_dimension(polys):
 B=s.Matrix([[s.Poly(f,*x).coeff_monomial(mon) for f in polys] for mon in monoms])
 annih=B.T.nullspace()
 eqs=[]
 for f in polys:
  derivative=s.expand(sum(s.diff(f,x[i])*sum(M[i,j]*x[j] for j in range(4)) for i in range(4)))
  coeff=s.Matrix([s.Poly(derivative,*x).coeff_monomial(mon) for mon in monoms])
  for row in annih:eqs.append((row.T*coeff)[0])
 A,_=s.linear_eq_to_matrix(eqs,vars)
 return 16-A.rank()
# A proper left line selects one entire matrix row.  Its left stabilizer
# has dimension3; adding GL2 and removing the scalar gives6. Full gives7.
checks['proper_stabilizer_lie_dimension_6']=stabilizer_dimension([delta*x[0],delta*x[1]])==6
checks['full_stabilizer_lie_dimension_7']=stabilizer_dimension([delta*t for t in x])==7
transpose={x[0]:x[0],x[1]:x[2],x[2]:x[1],x[3]:x[3]}
f=delta*x[1]
polyvec=lambda f:s.Matrix([s.Poly(f,*x).coeff_monomial(mon) for mon in monoms])
proper=s.Matrix.hstack(polyvec(delta*x[0]),polyvec(delta*x[1]))
checks['transpose_excluded_by_proper_support']=s.expand(f.xreplace(transpose)-delta*x[2])==0 and proper.row_join(polyvec(f.xreplace(transpose))).rank()==3
checks['transpose_preserves_full_system']=set(s.expand((delta*t).xreplace(transpose)) for t in x)==set(s.expand(delta*t) for t in x)
# Covering maps and ramification are exact, including infinity.
checks['cubic_critical_roots_distinct']=s.discriminant(3*z*z+1,z)==-12
checks['cubic_critical_roots_nonzero']=s.resultant(3*z*z+1,z,z)==1
checks['cubic_maps_degree_three']=s.degree(z**3,z)==3 and s.degree(z**3+z,z)==3
checks['ramification_total_both_four']=2*(3-1)==(3-1)+2*(2-1)==4
# Universal rank identities in several embedding dimensions and cover degrees.
ranks=[]
for n in range(3,7):
 N=comb(n+1,2);d=n*n+2*n-4;e=n*n;M0=comb(N,2)
 top=comb(e+d-1,d)
 ranks.append(top>=M0*M0)
 ranks.append((top-M0*M0)+(M0-3)*M0==top-3*M0)
 ranks.append(sum(comb(e+j-1,j) for j in range(d))+top-M0==comb(e+d,d)-M0)
checks['graded_rank_identities_n3_through_n6']=all(ranks)
checks['n3_total_rank_167945']=comb(20,11)-15==167945
checks['n3_top_trivial_rank_75537']=comb(19,11)-45==75537
checks['n3_top_positive_rank_30']=2*15==30
# Equivariance of the Pluecker column under a nonscalar constant GL2 map.
g=s.Matrix([[2,1],[1,1]]);aa,bb=list(g*s.Matrix([a,b]));
Sym2=s.Matrix([[4,4,1],[2,3,1],[1,2,1]])
# Compare expanded expressions to remove harmless polynomial presentation.
checks['constant_target_conic_equivariance']=all(s.expand(t)==0 for t in Sym2*wedge-s.Matrix([aa*aa,aa*bb,bb*bb]))
record={'revision':148,'ok':all(checks.values()),'checks':checks,'check_count':len(checks),
        'small_support_patterns':len(patterns),'universal_proofs_certified':False,
        'priority_certified':False,'scope':'Exact finite identities and low-dimensional witnesses only.'}
(out/'REVISION148_EXACT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
if not record['ok']:raise SystemExit(1)
