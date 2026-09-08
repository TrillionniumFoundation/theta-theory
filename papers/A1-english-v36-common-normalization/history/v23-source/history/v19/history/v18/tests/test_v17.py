#!/usr/bin/env python3
"""Exact finite diagnostics for operational reconstruction.

No imports from author geometric, compiler, or prior test modules. Rational
powers are compared after taking a common integer power, never by floats.
These fixtures do not prove the analytic attainment or entropy theorems.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import factorial, lcm, prod
from pathlib import Path
import hashlib
import json
import random
import sys

COUNTS: Counter[str] = Counter()

def check(condition: bool, suite: str, detail: str) -> None:
    COUNTS[suite] += 1
    if not condition:
        raise AssertionError(suite+': '+detail)

def volumes(s: tuple[F, ...]) -> tuple[F, ...]:
    result=[F(1)]
    for x in s:
        result.append(result[-1]*x)
    return tuple(result)

def envelope_power(v: tuple[F, ...], budget: F, degree: int) -> F:
    """Return e(budget)**degree exactly; degree is a multiple of all indices."""
    return max((x/budget)**(degree//j) for j,x in enumerate(v[1:],1))

def ceil_fraction(x: F) -> int:
    return -(-x.numerator//x.denominator)

def check_sides(s: tuple[F, ...]) -> None:
    suite='ordered_product_reconstruction'
    p=len(s); degree=lcm(*range(1,p+1)); v=volumes(s)
    check(all(x>=0 for x in s) and all(s[i]>=s[i+1] for i in range(p-1)),suite,'ordered nonnegative sides')
    rank=sum(x>0 for x in s)
    for ell in range(1,p+1):
        for M in (1,2,3,7,19,128):
            power=envelope_power(v,F(M),degree)
            check(F(M)**degree*power**ell>=v[ell]**degree,suite,'all-budget lower product bound')
        if s[ell-1]:
            b=v[ell]/s[ell-1]**ell
            check(b>=1,suite,'admissible supporting budget')
            check(envelope_power(v,b,degree)==s[ell-1]**degree,suite,'continuous equality')
            M=ceil_fraction(b)
            check(b<=M<=2*b,suite,'rounding with integer budget')
            power=envelope_power(v,F(M),degree)
            check(v[ell]**degree<=F(M)**degree*power**ell<=(2*v[ell])**degree,suite,'integer factor two')
        elif not rank:
            check(envelope_power(v,F(13),degree)==0,suite,'rank zero envelope')
        else:
            br=v[rank]/s[rank-1]**rank
            for factor in (1,2,16):
                b=br*factor
                check(envelope_power(v,b,degree)==(v[rank]/b)**(degree//rank),suite,'last positive branch')
            check(ell>rank and F(1)-F(ell,rank)<0,suite,'vanishing transform exponent above rank')

def rational_families() -> int:
    rng=random.Random(20260907)
    families=[]
    for p in range(1,8):
        families += [tuple(F(0) for _ in range(p)),tuple(F(1) for _ in range(p)),
                     tuple(F(3,2) for _ in range(p)),tuple(F(1,2**i) for i in range(p))]
        for rank in range(p+1):
            families.append(tuple(F(1,3**i) if i<rank else F(0) for i in range(p)))
        for _ in range(20):
            families.append(tuple(sorted((F(rng.randrange(0,13),rng.randrange(1,12)) for _ in range(p)),reverse=True)))
    for s in families:
        check_sides(s)
    return len(families)

def circular_products() -> int:
    suite='paired_contrast_products'
    families=0
    for k in range(1,7):
        for tau in (F(0),F(1,2),F(1,3),F(1,7)):
            s=tuple(tau**(2*j) for j in range(1,k+1) for _ in range(2));v=volumes(s)
            for j in range(1,k+1):
                check(v[2*j-1]==tau**(2*j*j),suite,'odd product exponent')
                check(v[2*j]==tau**(2*j*(j+1)),suite,'even product exponent')
                if tau:
                    check(v[2*j-1]/v[2*j-2]==v[2*j]/v[2*j-1]==tau**(2*j),suite,'both successive ratios')
                    b=v[2*j]/s[2*j-1]**(2*j)
                    check(b==tau**(-2*j*(j-1)),suite,'shared supporting budget for a paired scale')
                    degree=lcm(*range(1,2*k+1))
                    check(envelope_power(v,b,degree)==tau**(2*j*degree),suite,'all-branch supporting equality')
            if k<=4:check_sides(s+(F(0),))
            families+=1
    return families

def leja_fixtures() -> int:
    suite='collision_product_comparison'
    families=[(F(0),F(0),F(0)),(F(0),F(1,3),F(1,3),F(1)),
              (F(0),F(1,100),F(2,100),F(1,2),F(1)),
              (F(0),F(1,10000),F(1,100),F(101,10000),F(1)),
              tuple(F(i,6) for i in range(7))]
    for nodes in families:
        remain=list(range(len(nodes)));order=[];pivots=[]
        while remain:
            i=max(remain,key=lambda j:(prod(abs(nodes[j]-nodes[h]) for h in order),-j))
            pivots.append(F(prod(abs(nodes[i]-nodes[h]) for h in order)));order.append(i);remain.remove(i)
        check(all(pivots[i]>=pivots[i+1] for i in range(len(pivots)-1)),suite,'ordered complete Leja pivots')
        v=volumes(tuple(pivots))
        for ell in range(1,len(nodes)+1):
            maximal=max(F(prod(abs(nodes[i]-nodes[j]) for i,j in combinations(subset,2))) for subset in combinations(range(len(nodes)),ell))
            check(v[ell]<=maximal<=factorial(ell)*v[ell],suite,'maximal volume versus ordered product')
        for truncation in range(1,len(nodes)+1):
            check_sides(tuple(pivots[:truncation])+(F(0),))
    return len(families)

def comparison_fixtures() -> None:
    suite='uniform_curve_comparison'
    rng=random.Random(1709)
    for p in range(1,7):
        degree=lcm(*range(1,p+1))
        for rank in range(p+1):
            s=tuple(sorted((F(rng.randrange(1,8),rng.randrange(1,8)) for _ in range(rank)),reverse=True))+tuple(F(0) for _ in range(p-rank))
            t=tuple(sorted((F(rng.randrange(1,8),rng.randrange(1,8)) for _ in range(rank)),reverse=True))+tuple(F(0) for _ in range(p-rank))
            vs,vt=volumes(s),volumes(t)
            B=max([F(1)]+[x for j in range(1,rank+1) for x in (vs[j]/vt[j],vt[j]/vs[j])])
            for M in (1,2,17,10000):
                a=envelope_power(vs,F(M),degree);b=envelope_power(vt,F(M),degree)
                check(a/B**degree<=b<=a*B**degree,suite,'product comparison implies envelope comparison')
            check([v==0 for v in vs]==[v==0 for v in vt],suite,'matching rank-zero pattern')

def resource_and_source_fixtures(root: Path) -> None:
    suite='resource_wording_and_retention'
    for B in (1,2,3):
        alphabet=5*B
        for n in range(5):
            count=alphabet**n
            for encoded in (0,count//2,count-1):
                x=encoded;digits=[]
                for _ in range(n):digits.append(x%alphabet);x//=alphabet
                restored=sum(d*alphabet**j for j,d in enumerate(digits))
                check(x==0 and restored==encoded,suite,'finite-alphabet exact-prefix indexing')
    text=(root/'sections/structural_comparison.tex').read_text()
    check('specified finite detector commands' not in text,suite,'reported ambiguity removed from active comparison')
    check('continuous gate cube' in text,suite,'continuous command model explicit')
    check('continuously over' in (root/'sections/circular.tex').read_text(),suite,'formal resource description explicit')
    main=(root/'main.tex').read_text()
    check('\\input{sections/operational_reconstruction}' in main,suite,'new results actually compiled')
    old=json.loads((root/'history/V16_SOURCE_MANIFEST.json').read_text())['files']
    for name in sorted(old):
        if name.startswith('core/') or name in ['finite_compiler.py','certified_compiler.py','construction_contracts.py'] or name.startswith('tests/'):
            check(hashlib.sha256((root/name).read_bytes()).hexdigest()==old[name],suite,'unchanged inherited source: '+name)

def main() -> None:
    root=Path(__file__).resolve().parents[1]
    path=Path(sys.argv[1]) if len(sys.argv)>1 else root/'validation/V17_OPERATIONAL_RECONSTRUCTION.json'
    result={'version':17,'arithmetic':'fractions.Fraction and integers; no floating point',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'families':{'ordered_sides':rational_families(),'circular':circular_products(),'collision':leja_fixtures()}}
    comparison_fixtures();resource_and_source_fixtures(root)
    result.update(passed=True,assertions=sum(COUNTS.values()),assertions_by_suite=dict(COUNTS),
        scope='Finite exact diagnostics and source invariants. Not analytic proof verification, novelty verification, or an independent referee decision.')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
