#!/usr/bin/env python3
"""Finite independent character, shear-coefficient and nonreduced-section checks."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from math import factorial, prod
from pathlib import Path
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
def char(a,b):return Counter({(x,y):1 for x in range(a,-a-1,-2) for y in range(b,-b-1,-2)})
def power(weights,n,exterior=True):
    comb=combinations(weights,n) if exterior else combinations_with_replacement(weights,n)
    return Counter(tuple(sum(z[i] for z in xs) for i in range(2)) for xs in comb)
V=list(char(1,1));W=list(power(V,2,False).elements())
actual=power(W,3)
summands=[(6,0,1),(0,6,1),(4,4,1),(4,2,2),(2,4,2),(2,2,1),(2,0,2),(0,2,2)]
expected=Counter()
for a,b,m in summands:
    for wt,n in char(a,b).items():expected[wt]+=m*n
assert actual==expected and sum(actual.values())==120
# Complete highest-weight subtraction, rather than merely total dimension.
remaining=actual.copy();highest=[]
while remaining:
    a,b=max(remaining);m=remaining[(a,b)]
    assert a>=0 and b>=0 and m>0
    highest.append([a,b,m])
    for wt,n in char(a,b).items():
        remaining[wt]-=m*n
        assert remaining[wt]>=0
        if remaining[wt]==0:del remaining[wt]
assert all((a,b)!=(0,0) for a,b,m in highest)
quartic=power(V,4,False)
assert quartic==char(4,4)+char(2,2)+char(0,0)
# Audit the noncancelling coefficient used in shear descent, for m=4,
# with formal B-coefficients and every relevant A-degree/radical rank.
x=s.symbols('x0:4');shear_tests=0
for r in [1,2,3]:
    A=x[:r];B=x[r:];b=sum(B)
    for k in range(1,5):
        exps=[e for e in product(range(k+1),repeat=r) if sum(e)==k]
        cs=s.symbols('c0:'+str(len(exps)))
        F=sum(c*prod(a**n for a,n in zip(A,e)) for c,e in zip(cs,exps))
        for e,c in zip(exps,cs):
            for i in range(r):
                if not e[i]:continue
                alpha=list(e);alpha[i]-=1
                deriv=F
                for a,n in zip(A,alpha):deriv=s.diff(deriv,a,n)
                coeff=s.Poly(deriv,*A).coeff_monomial(A[i])
                assert s.expand(coeff-c*prod(factorial(n) for n in e))==0
                result=s.expand(b**(k-1)*deriv)
                assert result!=0
                assert s.Poly(result,*A).total_degree()==1
                shear_tests+=1
# A dual-number base: two Cartier sections remain a product/disjoint union.
e,t=s.symbols('e t');c=1+e;d=2-e
G=s.groebner([e**2,(t-1)*(c+d*t)],t,e,domain=s.QQ)
es=(c+d*t)/3;er=d*(1-t)/3
for f in [es+er-1,es**2-es,er**2-er,es*er]:assert G.reduce(s.expand(f))[1]==0
r=-s.Rational(1,2)-s.Rational(3,4)*e
assert s.rem(s.expand(c+d*r),e**2,e)==0
# Retained support table implies these exact reduced pullbacks, not ideal radicality.
support_rows=[(1,False,4),(2,False,7),(3,False,9),(4,False,10),(4,True,9)]
for ess,square,support in support_rows:
    assert (support<=4)==(ess==1)
    assert (support<=7)==(ess<=2)
    assert (support<=8)==(ess<=2)
    assert (support<=9)==(ess<=3 or square)
result={'ok':True,'SO4_target_dimension':120,'SO4_highest_weights':highest,
 'SO4_invariant_multiplicity':0,'quartic_dimensions':[25,9,1],
 'shear_coefficient_checks':shear_tests,'dual_number_CRT_checks':4,
 'support_pullback_rows':support_rows,
 'scope':'Finite exact coefficient/character checks; structural arguments remain written proofs.',
 'structural_proofs_not_machine_certified':['shear descent for arbitrary invariant subspaces and arbitrary degree',
 'complete reducibility and representation-theoretic identification','arbitrary-base Cartier section gluing',
 'intrinsic normal-cone reconstruction','radicality of pulled-back flattening ideals (not asserted)',
 'historical priority or journal acceptance']}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION135_EXACT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
