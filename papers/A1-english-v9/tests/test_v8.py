#!/usr/bin/env python3
"""Finite diagnostics of the v8 identities, not proofs of continuum theorems.

The all-prior, bounded-format entropy and global reachable-cover assertions
are proved in the manuscript. This executable checks exact finite rank/update
instances and index-only finite-input tables; it does not synthesize the
continuous-command asymptotically optimal codebook.
"""
from __future__ import annotations
import hashlib
import itertools as it
import json
import math
import platform
import random
import re
from fractions import Fraction as F
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
checks: list[dict] = []

def check(name: str, ok: bool, **details) -> None:
    if not ok:
        raise AssertionError(f'{name}: {details}')
    checks.append({'name': name, 'passed': True, **details})

def sums(A: tuple, m: int) -> list:
    out = {(F(0), F(0))}
    for _ in range(m):
        out = {(x+a, y+b) for x,y in out for a,b in A}
    return sorted(out)

def jets(A: tuple, m: int) -> list:
    pairs = sums(A,m)
    clusters = {a: sorted(b for x,b in pairs if x == a) for a,_ in pairs}
    return sorted(((a,k) for a,bs in clusters.items() for k in range(len(bs))
                   if not (a == 0 and k == 0)), key=lambda z:(z[1],z[0]))

def mom(exponent: F, k: int=0, prior: int=0) -> F:
    """Integral of t**exponent (log t)**k / k!, for three full-support priors."""
    unif = F((-1)**k,1)/(exponent+1)**(k+1)
    if prior == 0: return unif
    if prior == 1: return F(2*(-1)**k,1)/(exponent+2)**(k+1)
    # Half uniform plus one quarter atom at each endpoint.
    return unif/2 + F(k == 0,4) + F(exponent == 0 and k == 0,4)

def exact_rank(rows: list) -> int:
    return int(sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(rows)).rank())

A3=((F(0),F(0)),(F(1),F(0)),(F(2),F(1)))
A4=((F(0),F(0)),(F(1),F(1)),(F(2),F(-1)),(F(3),F(2)))
for ai,A in enumerate((A3,A4)):
    for n,m in it.product((1,2,4),(1,2,3,4)):
        r=len(A); D=A[-1][0]
        B=sorted({j*D for j in range(n+1)} |
                 {a+j*D for a,b in A[1:-1] for j in range(n)})
        chosen=jets(A,m)[:min(n*(r-1),len(jets(A,m)))]
        columns=[(F(0),0)]+sorted(chosen)
        p=len(chosen)
        check(f'tangent-dimension-A{ai}-n{n}-m{m}',len(B)==n*(r-1)+1,
              dimension=len(B),selected=p)
        for prior in range(3):
            mat=[[mom(u+a,k,prior) for a,k in columns] for u in B]
            check(f'zero-flag-rank-A{ai}-n{n}-m{m}-prior{prior}',
                  exact_rank(mat)==p+1,rank=p+1)
            # Delete the constant after normalizing against an actual binomial product.
            product={F(0):F(1)}
            for c in range(1,n+1):
                new={}
                for e,v in product.items():
                    new[e]=new.get(e,F(0))+v
                    new[e+D]=new.get(e+D,F(0))+v*F(c,100)
                product=new
            ev=sum(v*mom(e,0,prior) for e,v in product.items())
            pred=[sum(v*mom(e+a,k,prior) for e,v in product.items())/ev
                  for a,k in columns[1:]]
            deriv=[[(mom(u+a,k,prior)-pred[j]*mom(u,0,prior))/ev
                    for j,(a,k) in enumerate(columns[1:])] for u in B]
            check(f'normalized-flag-rank-A{ai}-n{n}-m{m}-prior{prior}',
                  exact_rank(deriv)==p,rank=p)
        theta=F(1,101)
        Dt=A[-1][0]+theta*A[-1][1]
        Bt=sorted({j*Dt for j in range(n+1)} |
                  {a+theta*b+j*Dt for a,b in A[1:-1] for j in range(n)})
        pairs=sums(A,m)
        clusters={a:sorted(b for x,b in pairs if x==a) for a,b in pairs}
        future=[F(0)]+[a+theta*clusters[a][k] for a,k in chosen]
        check(f'positive-flag-rank-A{ai}-n{n}-m{m}',
              len(set(future))==p+1 and exact_rank([[mom(u+v) for v in future] for u in Bt])==p+1)

seven_orders=[k for a,k in jets(A3,3)]
check('seven-ambient-orders',seven_orders==[0]*6+[1]*3,orders=seven_orders)
check('seven-attained-orders',seven_orders[:8]==[0]*6+[1]*2)
cols=[(F(0),0)]+sorted(jets(A3,3)[:8])
minor=sp.Matrix([[sp.Rational(mom(F(i)+a,k)) for a,k in cols] for i in range(9)]).det(method='domain-ge')
check('seven-limiting-nine-by-nine-minor',minor>0,determinant=str(minor))
for theta in (F(0),F(1,8),F(1,2)):
    profile=[min(2*n,len({a+theta*b for a,b in sums(A3,7-n)})-1) for n in range(8)]
    target=[0,2,4,6,6,4,2,0] if theta==0 else [0,2,4,6,8,5,2,0]
    check(f'seven-exact-profile-{theta}',profile==target,profile=profile)
check('seven-middle-is-geometric-mean',F(3,7)*F(1,3)+F(4,7)*F(1,4)==F(2,7)
      and F(4,7)*F(1,2)==F(2,7))
for theta in (F(1,2),F(1,4),F(1,16)):
    M=theta**-6
    # Avoid fractional powers: cube and fourth-power identities at the crossover.
    check(f'seven-crossover-{theta}',M*(theta**2)**3==1 and M*(theta**2)**4==theta**2)
    for M in (1,3,17,1024,10**9):
        all_terms=[float(theta)**(2*sum(seven_orders[:l])/l)*M**(-2/l) for l in range(1,9)]
        endpoint=max(M**(-1/3),float(theta)**.5*M**(-.25))
        check(f'truncated-profile-endpoints-{theta}-M{M}',math.isclose(max(all_terms),endpoint,rel_tol=1e-12))

# Check the integer-count implication used to invert the entropy estimate.
for C,p in it.product((1,5,19),(1,3,8,20)):
    L=4*C+2
    series=sum(F(1,L**j) for j in range(1,p+1))
    check(f'cover-budget-C{C}-p{p}',C*series<=F(1,2)
          and all(C+M*C*series<=M for M in (2*C,2*C+1,1000)))

# Exact raw formal updates. Report 0 is failure, 1..3 are accepted cells.
CELLS=({(0,0):F(1,3),(1,0):-F(1,12),(2,1):-F(1,12)},
       {(0,0):F(1,3),(1,0):F(1,12)},
       {(0,0):F(1,3),(2,1):F(1,12)})
COMMANDS=((F(1,4),F(1,2),F(3,4)),(F(2,3),F(1,3),F(1,2)))
def factor(ci: int,report: int) -> dict:
    g=COMMANDS[ci]
    if report: return {e:v*g[report-1] for e,v in CELLS[report-1].items()}
    out={}
    for j,c in enumerate(CELLS):
        for e,v in c.items():out[e]=out.get(e,F(0))+(1-g[j])*v
    return {e:v for e,v in out.items() if v}

def multiply(P: dict,f: dict) -> dict:
    out={}
    for (a,b),v in P.items():
        for (c,d),w in f.items():out[a+c,b+d]=out.get((a+c,b+d),F(0))+v*w
    return {e:v for e,v in out.items() if v}

def integrate(P: dict,theta: F,prior: int,shift=(0,0)) -> F:
    a,b=shift
    return sum((v*mom(x+a+theta*(y+b),0,prior) for (x,y),v in P.items()),F(0))

def reference(P: dict,m: int,theta: F,prior: int) -> dict:
    ev=integrate(P,theta,prior)
    return {b:integrate(P,theta,prior,b)/ev for b in sums(A3,m)}

def update(v: dict,m: int,ci: int,x: int) -> dict:
    f=factor(ci,x)
    denominator=sum(co*v[e] for e,co in f.items())
    if denominator<F(1,24):raise AssertionError('Positivity margin violated')
    return {b:sum(co*v[b[0]+e[0],b[1]+e[1]] for e,co in f.items())/denominator for b in sums(A3,m-1)}

def distance(v: dict,w: dict) -> float:
    return sum((float(v[b]-w[b]))**2 for b in v)

class IndexOnly:
    __slots__=('index','clock','tables')
    def __init__(self,tables):self.index=0;self.clock=0;self.tables=tables
    def step(self,ci,x):
        self.index=self.tables[self.clock][self.index,ci,x]
        self.clock+=1
        return self.index

rng=random.Random(80906)
exact_updates=0; fixtures=0
for theta,prior,M in it.product((F(0),F(1,8),F(1,2)),(0,2),(2,7)):
    books=[[reference({(0,0):F(1)},7,theta,prior)]]
    tables=[]
    for n in range(7):
        candidates=[]; keys=[]
        for i,v in enumerate(books[-1]):
            for ci,x in it.product(range(2),range(4)):
                candidates.append(update(v,7-n,ci,x));keys.append((i,ci,x))
        uniq=list({tuple(v.items()):v for v in candidates}.values())
        size=min(M,len(uniq))
        reps=[uniq[j*len(uniq)//size] for j in range(size)]
        tables.append({key:min(range(size),key=lambda j:distance(v,reps[j])) for key,v in zip(keys,candidates)})
        books.append(reps)
    check(f'index-only-codebook-count-theta{theta}-prior{prior}-M{M}',all(len(b)<=M for b in books))
    for trial in range(24):
        machine=IndexOnly(tuple(tables));P={(0,0):F(1)};v=books[0][0]
        for n in range(7):
            ci,x=rng.randrange(2),rng.randrange(4)
            direct=update(v,7-n,ci,x)
            P=multiply(P,factor(ci,x))
            independently=reference(P,6-n,theta,prior)
            if direct!=independently:raise AssertionError('Exact raw update mismatch')
            old=machine.index; idx=machine.step(ci,x)
            if idx!=tables[n][old,ci,x]:raise AssertionError('Index transition mismatch')
            if not isinstance(idx,int) or not 0<=idx<M:raise AssertionError('Persistent index invalid')
            if direct[(F(0),F(0))]!=1:raise AssertionError('Normalization lost')
            groups={}
            for (a,b),value in direct.items():
                exponent=a+theta*b
                if exponent in groups and groups[exponent]!=value:raise AssertionError('Duplicate-label inconsistency')
                groups[exponent]=value
            v=direct;exact_updates+=1
    fixtures+=1
    check(f'finite-input-seven-trial-transducer-theta{theta}-prior{prior}-M{M}',True,
          streams=24,steps=7,storage='one index; clock and transition tables read-only')

# The referee's necessary-budget constant selection, at finite rational fixtures.
for ce,Ce,cs in ((F(1,9),F(3),F(1,7)),(F(1,2),F(2),F(3,5))):
    k=(cs/(2*Ce))**2
    check(f'necessary-budget-{ce}-{Ce}-{cs}',cs**2/k==4*Ce**2)

# Preservation is checked by labels and hashes, not inferred from a page count.
legacy_labels=set()
predecessor=ROOT.parent/'A1-english-v7'
if predecessor.is_dir():
    old='\n'.join(p.read_text() for p in sorted((predecessor/'sections').glob('*.tex')))
    new='\n'.join(p.read_text() for p in sorted((ROOT/'sections').glob('*.tex')))
    pattern=r'\\label\{((?:thm|lem|prop|cor):[^}]+)\}'
    legacy_labels=set(re.findall(pattern,old))
    current=set(re.findall(pattern,new))
    check('all-predecessor-result-labels-retained',legacy_labels<=current,
          previous=len(legacy_labels),current=len(current),added=sorted(current-legacy_labels))

receipt={'revision':'A1 English v8','python':platform.python_version(),'sympy':sp.__version__,
         'passed':len(checks),'total':len(checks),'new_seven_trial_index_only_fixtures':fixtures,
         'new_exact_raw_updates':exact_updates,'seven_limiting_minor':str(minor),
         'checks':checks,'scope':'Finite exact and numerical diagnostics, not proof verification, continuous-code synthesis, or journal approval.'}
(ROOT/'V8_DIAGNOSTICS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ('passed','total','new_seven_trial_index_only_fixtures','new_exact_raw_updates','seven_limiting_minor')},indent=2))
