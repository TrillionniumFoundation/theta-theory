#!/usr/bin/env python3
"""Exact finite audits over QQ; these supplement but do not certify the proofs."""
from __future__ import annotations
import argparse, hashlib, importlib.util, itertools as it, json, math, subprocess, sys
from fractions import Fraction
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('checks157',HERE.parent/'v157'/'check_v157.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def require(test: bool, message: str) -> None:
    if not test: raise AssertionError(message)

def rank_integer_rows(rows, width: int) -> int:
    pivots={}
    for row in rows:
        a=[Fraction(x) for x in row]
        for j,b in sorted(pivots.items()):
            if a[j]:
                q=a[j];a=[x-q*y for x,y in zip(a,b)]
        j=next((i for i,x in enumerate(a) if x),None)
        if j is not None:
            q=a[j];pivots[j]=[x/q for x in a]
            if len(pivots)==width:return width
    return len(pivots)

def diagonal_coefficients(exponents):
    # Product (z+(i+1)t)^e_i, indexed by t-exponent; exact integer convolution.
    row=[1]
    for i,e in enumerate(exponents,1):
        factor=[math.comb(e,j)*i**j for j in range(e+1)]
        out=[0]*(len(row)+e)
        for j,a in enumerate(row):
            for k,b in enumerate(factor):out[j+k]+=a*b
        row=out
    return row

def tangent_spaces():
    records=[]
    for c in range(2,9):
        for j in range(1,c):
            rows=[diagonal_coefficients([int(i in subset) for i in range(c)])
                  for subset in it.combinations(range(c),j)]
            rank=rank_integer_rows(rows,j+1)
            require(rank==j+1,'distinct-factor exact coefficient span')
            records.append({'c':c,'j':j,'rank':rank,'generators':len(rows)})
    return records

def tail_spaces():
    records=[]
    for c in range(2,7):
        for h in range(1,4):
            groups={b:[] for b in range(c*h+1)}
            for ex in it.product(range(h+1),repeat=c):groups[sum(ex)].append(ex)
            for b,exs in groups.items():
                common=max(b-h*(c-1),0);degree=b-c*common
                require(all(min(ex)>=common for ex in exs),'forced determinant divisor')
                reduced=[tuple(e-common for e in ex) for ex in exs]
                rank=rank_integer_rows((diagonal_coefficients(ex) for ex in reduced),degree+1)
                require(rank==degree+1,'complete arbitrary-corank tail Veronese span')
                records.append({'c':c,'h':h,'residual_power':b,'common_determinant_power':common,'degree':degree,'rank':rank})
    return records

def determinant_ideals():
    z,t,u=s.symbols('z t u');records=[]
    for n,c,h in ((3,3,1),(3,3,2),(4,3,1),(4,3,2)):
        xs,X=old.symmetric(n,'x');r=n-c
        A=s.diag(*([1]*r+[z+(i+1)*t for i in range(c)]))
        f=s.prod(z+(i+1)*t for i in range(c))
        F=s.Poly(s.expand((X+u*A).det()**h),u)
        for p in range(1,n*h+1):
            coeff=s.Poly(F.nth(p),*xs).coeffs()
            b=max(p-h*r,0);q=max(p-h*(n-1),0);degree=b-c*q
            expected=[z**j*t**(degree-j)*f**q for j in range(degree+1)]
            actual=s.groebner(coeff,z,t,domain=s.QQ)
            target=s.groebner(expected,z,t,domain=s.QQ)
            require(actual==target,'independent determinant-apolar ideal comparison')
            records.append({'n':n,'c':c,'h':h,'p':p,'maximal_ideal_exponent':degree,'determinant_exponent':q,'groebner_equal':True})
        print(f'Ordinary apolar ideals passed: n={n}, c={c}, h={h}',flush=True)
    return records

def higher_jets():
    z,t=s.symbols('z t');records=[]
    S=s.Matrix([[z+t+z*z,z*t,t*t],[z*t,z+2*t+t*t,z*z],[t*t,z*z,z+3*t+z*t]])
    for cutoff in (3,4,5):
        trunc=[z**j*t**(cutoff-j) for j in range(cutoff+1)]
        for q in (1,2):
            actual=s.groebner(old.minors(S,q)+trunc,z,t,domain=s.QQ)
            expected=s.groebner([z**j*t**(q-j) for j in range(q+1)]+trunc,z,t,domain=s.QQ)
            require(actual==expected,'higher-order perturbation on the Artin surface jet')
            records.append({'matrix':'symmetric 3x3 with mixed quadratic perturbations','minor_order':q,'base':f'QQ[z,t]/(z,t)^{cutoff}','groebner_equal':True})
    return records

def cluster_partitions(n: int, minimum: int=2):
    yield ()
    for c in range(minimum,n+1):
        for rest in cluster_partitions(n-c,c):yield (c,)+rest

def degree_identities():
    records=[]
    for n in range(3,15):
        for cs in cluster_partitions(n):
            if not cs or max(cs)>=n:continue
            rs=[n-c for c in cs];simple=n-sum(cs)
            main=sum(q-sum(max(q-r,0) for r in rs) for q in range(1,n))
            tails=sum(math.comb(c,2) for c in cs)
            require(main+tails==math.comb(n,2),'exterior Hilbert multidegree conservation')
            require(main>=1,'main curve has positive polarization degree')
            for h in (1,2,3):
                for p in range(1,n*h+1):
                    common=max(p-h*(n-1),0)
                    bs=[max(p-h*r,0) for r in rs]
                    degrees=[b-c*common for b,c in zip(bs,cs)]
                    mainpower=p-sum(bs)-simple*common
                    require(mainpower>=0 and min(degrees)>=0,'nonnegative resolved degrees')
                    require(mainpower+sum(degrees)==p-n*common,'every power multidegree conservation')
            records.append({'n':n,'clusters':cs,'main_exterior_degree':main,'tail_exterior_degree':tails,'residual_parameter_dimension':sum(math.comb(c+1,2)-2 for c in cs)})
    return records

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-inherited',action='store_true');args=ap.parse_args()
    inherited=False
    if not args.skip_inherited:
        subprocess.run([sys.executable,str(HERE.parent/'v158'/'check_v158.py')],check=True)
        p=HERE.parent/'v158'/'EXACT_CHECKS_V158.json'
        require(json.loads(p.read_text())['all_checks_pass'],'inherited v158 suite')
        (HERE/'INHERITED_V158_CHECKS_RERUN.json').write_bytes(p.read_bytes());inherited=True
    result={'revision':159,'field':'QQ','tangent_factor_tests':tangent_spaces(),
            'tail_coefficient_tests':tail_spaces(),'apolar_ideal_tests':determinant_ideals(),
            'higher_order_Artin_tests':higher_jets(),'simultaneous_cluster_degree_tests':degree_identities(),
            'inherited_v158_suite_rerun':inherited,'historical_28_checks_rerun':False,
            'general_proofs_certified_by_computation':False,'all_checks_pass':True,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'EXACT_CHECKS_V159.json').write_text(json.dumps(result,indent=2)+'\n')
    print('All exact v159 checks passed; these are finite audits, not general proof certificates.',flush=True)
if __name__=='__main__':main()
