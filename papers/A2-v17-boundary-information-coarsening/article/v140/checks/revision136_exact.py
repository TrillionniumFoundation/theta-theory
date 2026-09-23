#!/usr/bin/env python3
"""Exact finite checks for the dimension-uniform contraction theorem.

The integer polarization matrices are reduced modulo a prime only to
certify lower rank bounds. Exact exhibited kernels supply the matching
upper bounds in these finite cases. No assertion for arbitrary dimension,
representation irreducibility, scheme descent or priority is machine-certified.
"""
from collections import defaultdict
from math import comb, factorial
from fractions import Fraction
from itertools import combinations
import json,time

def expansion(n):
    pairs=list(combinations(range(n),2))+[(i,i) for i in range(n)]
    pairs.sort(); ix={v:i for i,v in enumerate(pairs)}
    out={((0,)*n,()):1}
    for col in range(n):
        nxt=defaultdict(int)
        for (a,w),c in out.items():
            for j in range(n):
                k=ix[tuple(sorted((j,col)))];
                if k in w:continue
                sign=(-1)**sum(t>k for t in w)
                b=list(a);b[j]+=1
                nxt[(tuple(b),tuple(sorted(w+(k,))))]+=sign*c
        out={k:v for k,v in nxt.items() if v}
    cols=defaultdict(dict)
    for (a,w),v in out.items():cols[a][w]=v
    return pairs,dict(cols)

def contract(pairs,cols,r):
    out={}
    for a,z in cols.items():
        c=defaultdict(int)
        for w,v in z.items():
            for pos,k in enumerate(w):
                i,j=pairs[k]
                if i==j and i<r:c[w[:pos]+w[pos+1:]]+=(-1)**pos*v
        out[a]={w:v for w,v in c.items() if v}
    return out

def rankmod(cols,p=1000003):
    piv={}
    for z in cols.values():
        v={w:c%p for w,c in z.items() if c%p}
        while v:
            k=min(v)
            if k not in piv:
                inv=pow(v[k],-1,p);piv[k]={w:c*inv%p for w,c in v.items()};break
            c=v[k]
            for w,d in piv[k].items():
                t=(v.get(w,0)-c*d)%p
                if t:v[w]=t
                else:v.pop(w,None)
    return len(piv)

def multinomial(a):
    v=factorial(sum(a))
    for t in a:v//=factorial(t)
    return v


from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
results={}
for n in range(2,8):
    t=time.time();pairs,cols=expansion(n);rows=[]
    for r in range(1,n+1):
        c=contract(pairs,cols,r); rank=rankmod(c)
        dim=comb(2*n-1,n)
        expected=comb(2*n-r-1,n) if r<n else (1 if n%2==0 else 0)
        if r<n:
            radical_columns=[z for a,z in c.items() if not any(a[:r])]
            assert len(radical_columns)==expected and all(not z for z in radical_columns)
        assert dim-rank==expected,(n,r,dim,rank,expected)
        rows.append({'bilinear_rank':r,'kernel_dim':dim-rank})
    if n%2==0:
        acc=defaultdict(Fraction)
        for a,z in c.items():
            if any(i%2 for i in a):continue
            half=tuple(i//2 for i in a)
            weight=Fraction(multinomial(half),multinomial(a))
            for w,v in z.items():acc[w]+=weight*v
        assert all(v==0 for v in acc.values())
    results[n]={'ranks':rows,'scalar_kernel_exact':n%2==0,'seconds':round(time.time()-t,3)}
    print(n,results[n],flush=True)


# Independently read the harmonic nonvanishing coefficient from the
# polarized matrices, without using the closed coefficient formula.
def monomials(total,variables):
    if variables==1:
        yield (total,);return
    for first in range(total+1):
        for tail in monomials(total-first,variables-1):yield (first,)+tail

def polynomial_vector(cols,poly):
    out=defaultdict(Fraction)
    for a,v in poly.items():
        for w,c in cols[a].items():out[w]+=Fraction(v*c,multinomial(a))
    return {w:c for w,c in out.items() if c}

def support_rank(pairs,z):
    columns={}
    for k in range(len(pairs)):
        c=defaultdict(Fraction)
        for w,v in z.items():
            if k in w:
                i=w.index(k);c[w[:i]+w[i+1:]]+=(-1)**i*v
        columns[k]={w:(v.numerator*pow(v.denominator,-1,1000003))%1000003 for w,v in c.items() if v}
    return rankmod(columns)

coefficients=[];supports=[]
for n in range(2,8):
    pairs,cols=expansion(n);c=contract(pairs,cols,n)
    tau=tuple(pairs.index((0,i)) for i in range(1,n))
    for t in range(n//2+1):
        m=n-2*t;f=defaultdict(int)
        for beta in monomials(t,n):
            for k in range(0,m+1,2):
                a=[2*b for b in beta];a[0]+=m-k;a[1]+=k
                f[tuple(a)]+=multinomial(beta)*(-1)**(k//2)*comb(m,k)
        observed=polynomial_vector(c,f).get(tau,0)
        expected=Fraction(m*(n+m-2),n*(n-1))
        assert observed==expected,(n,m,observed,expected)
        coefficients.append({'n':n,'harmonic_degree':m,'coefficient':str(observed)})
    if n<4:continue
    for d in range(1,n+1):
        f={tuple(n if j==i else 0 for j in range(n)):1 for i in range(d)}
        s=support_rank(pairs,polynomial_vector(cols,f))
        expected=n*(n+1)//2-(n-d)*(n-d+1)//2
        assert s==expected,(n,d,s,expected)
        if d>=3:assert s>2*n
        supports.append({'n':n,'essential_variables':d,'form':'sum of nth powers','support':s})
    if n%2==0:
        f={tuple(2*b for b in beta):multinomial(beta) for beta in monomials(n//2,n)}
        s=support_rank(pairs,polynomial_vector(cols,f))
        assert s==n*(n+1)//2-1
        supports.append({'n':n,'essential_variables':n,'form':'nondegenerate quadratic power','support':s})
    f={(1,)*n:1};s=support_rank(pairs,polynomial_vector(cols,f))
    assert s==n*(n+1)//2
    supports.append({'n':n,'essential_variables':n,'form':'diagonal-web Jacobian product','support':s})
# Polynomial identities for the entire numerical range of the manuscript
# remain written proofs; checking a larger range is only a regression check.
for n in range(4,101):
    assert 3*n-3>2*n and n*(n+1)//2-1>2*n
result={'ok':True,'rational_kernel_rank_certificates':results,
 'modular_lower_bound_prime':1000003,
 'lower_bounds':'Integer polarization matrices, exact Gaussian elimination modulo the listed prime.',
 'upper_bounds':'Singular radical monomials are exactly zero columns; even full-rank quadratic-power kernels are evaluated over Fraction.',
 'harmonic_coefficient_checks':coefficients,'support_checks':supports,
 'structural_proofs_not_machine_certified':['all dimensions beyond these finite cases',
 'orthogonal irreducibility and shear descent for arbitrary invariant subspaces',
 'oriented relative Segre descent and regularity of the PGL morphism',
 'arbitrary-base-change residual colon and pencil-section theorems',
 'historical priority, Ballico 1993 full comparison, or journal acceptance']}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION136_EXACT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
