#!/usr/bin/env python3
"""Exact finite checks for A2 v155. General proofs are not certified by samples."""
from __future__ import annotations
import collections
from fractions import Fraction
import hashlib
import itertools as it
import json
from pathlib import Path
import subprocess
import sys
import sympy as s
HERE=Path(__file__).resolve().parent

def require(test: bool, message: str) -> None:
    if not test: raise AssertionError(message)

def partitions(d: int, h: int):
    if d==0: yield ()
    else:
        for a in range(h+1):
            for tail in partitions(d-1,a): yield (a,)+tail

def schur_dimension(lam: tuple[int,...]) -> int:
    value=Fraction(1)
    for i in range(len(lam)):
        for j in range(i+1,len(lam)): value*=Fraction(2*lam[i]-2*lam[j]+j-i,j-i)
    require(value.denominator==1,'integral Schur dimension')
    return value.numerator

def hilbert(d: int,h: int) -> list[int]:
    out=[0]*(d*h+1)
    for lam in partitions(d,h): out[sum(lam)]+=schur_dimension(lam)
    return out

def weyl_length(d: int,h: int) -> int:
    value=Fraction(1)
    for i in range(1,d+1):
        value*=Fraction(h+d-i+1,d-i+1)
        for j in range(i+1,d+1): value*=Fraction(2*h+2*d-i-j+2,2*d-i-j+2)
    require(value.denominator==1,'integral symplectic dimension')
    return value.numerator

def small_sections(d: int,h: int) -> dict:
    xs=s.symbols(f'x0:{d}');pairs=list(it.combinations_with_replacement(range(d),2))
    ys=s.symbols(f'y0:{len(pairs)}');Q=sum(y*xs[i]*xs[j] for y,(i,j) in zip(ys,pairs))
    equations=s.Poly(Q**(h+1),*xs).coeffs()
    G=s.groebner(equations,*ys,order='grevlex',domain=s.QQ)
    leading=[p.LM(order=G.order).exponents for p in G.polys]
    bounds=[min(ex[i] for ex in leading if ex[i]>0 and sum(ex)==ex[i]) for i in range(len(ys))]
    basis=[ex for ex in it.product(*(range(b) for b in bounds)) if not any(all(a>=b for a,b in zip(ex,lm)) for lm in leading)]
    counts=collections.Counter(sum(ex) for ex in basis);actual=[counts[i] for i in range(max(counts)+1)]
    require(actual==hilbert(d,h),'Groebner Hilbert versus independent Schur formula')
    require(len(basis)==weyl_length(d,h),'Groebner length versus symplectic product')
    X=s.zeros(d)
    for y,(i,j) in zip(ys,pairs): X[i,j]=X[j,i]=y
    determinant_power=s.expand(X.det()**h)
    for f in equations:
        value=s.Integer(0)
        for ex,c in s.Poly(f,*ys).terms():
            term=determinant_power
            for y,n in zip(ys,ex):
                if n: term=s.diff(term,y,n)
            value+=c*term
        require(s.expand(value)==0,'every section generator annihilates determinant power')
    return {'d':d,'h':h,'field':'QQ','length':len(basis),'ordinary_hilbert':actual,'groebner_basis_size':len(G.polys),'all_generators_annihilate_determinant_power':True}

def valuation_checks(exponents: tuple[int|None,...],h: int) -> dict:
    n=len(exponents);t,z=s.symbols('t z');pairs=list(it.combinations_with_replacement(range(n),2))
    xs=s.symbols(f'X0:{len(pairs)}');X=s.zeros(n)
    for x,(i,j) in zip(xs,pairs):X[i,j]=X[j,i]=x
    D=s.diag(*[0 if e is None else t**e for e in exponents]);U=s.eye(n)
    for i in range(n-1):U[i,i+1]=t+i+1
    A=U.T*D*U;coefficients=s.Poly(s.expand((X+z*A).det()**h),z);got=[]
    for p in range(1,n*h+1):
        poly=s.Poly(coefficients.nth(p),*xs)
        if poly.is_zero:actual=None
        else:actual=min(min(ex[0] for ex,c in s.Poly(v,t).terms() if c) for v in poly.coeffs() if v)
        q,r=divmod(p,h);occupied=list(exponents[:q])+([exponents[q]] if r else [])
        expected=None if any(e is None for e in occupied) else h*sum(exponents[:q])+(r*exponents[q] if r else 0)
        require(actual==expected,f'power ideal valuation n={n}, h={h}, p={p}')
        got.append({'p':p,'valuation':actual,'zero_ideal':actual is None})
    return {'elementary_exponents':exponents,'h':h,'unimodular_congruence':'upper triangular, polynomial in t','computed_over':'QQ[t]','powers':got}

def main() -> None:
    subprocess.run([sys.executable,str(HERE.parent/'v154'/'check_v154.py')],check=True)
    inherited=json.loads((HERE.parent/'v154'/'EXACT_CHECKS_V154.json').read_text())
    require(inherited['all_checks_pass'],'inherited check suite')
    products=[]
    for d in range(1,9):
        for h in range(1,4):
            hs=hilbert(d,h);require(hs==hs[::-1],'complementary-partition symmetry')
            require(sum(hs)==weyl_length(d,h),'Schur sum equals Weyl product')
            products.append({'d':d,'h':h,'ordinary_hilbert':hs,'length':sum(hs)})
    small=[small_sections(d,h) for d,h in [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2)]]
    valuations=[valuation_checks(ex,h) for ex,h in [((0,1),1),((1,2),2),((0,3),3),((0,None),2),((0,1,3),1),((0,2,None),1)]]
    big=hilbert(8,3);require(sum(big)==922268360,'ternary boundary quadratic-section length')
    out={'revision':155,'all_checks_pass':True,'coefficient_field':'QQ','section_groebner_checks':small,'representation_product_checks':products,'local_power_ideal_checks':valuations,
         'ternary_boundary_section':{'d':8,'h':3,'length':sum(big),'ordinary_hilbert':big,'socle_ordinary_degree':24,'socle_reciprocal_weight':48,'whole_fibre_length_computed':False},
         'inherited_v154_suite_rerun':True,'inherited_v154_all_checks_pass':True,'inherited_v154_report_sha256':hashlib.sha256((HERE.parent/'v154'/'EXACT_CHECKS_V154.json').read_bytes()).hexdigest(),
         'historical_28_checks_rerun':False,'general_theorems_certified_by_computation':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'EXACT_CHECKS_V155.json').write_text(json.dumps(out,indent=2)+'\n')
    (HERE/'INHERITED_V154_CHECKS_RERUN.json').write_text(json.dumps(inherited,indent=2)+'\n')
    print('All v155 exact finite checks passed; inherited v154 suite rerun; section length 922268360.')
if __name__=='__main__':main()
