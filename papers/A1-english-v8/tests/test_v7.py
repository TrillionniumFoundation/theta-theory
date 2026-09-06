#!/usr/bin/env python3
"""Finite exact and floating diagnostics for A1 v7, not proofs of its uniform laws.

Python >=3.10, SymPy and NumPy. The executed streaming fixture stores only an
integer; its separate test harness keeps exact-history reference states. The
finite input fixture is not used to infer a continuous-input asymptotic rate.
"""
from __future__ import annotations
import hashlib
import itertools as it
import json
import math
import platform
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
CHECKS: list[dict] = []
DETAILS: dict = {}

def check(name: str, condition: bool, **detail) -> None:
    if not bool(condition):
        raise AssertionError(f"{name}: {detail}")
    CHECKS.append({"name": name, "passed": True, **detail})

def mul(p: dict, q: dict) -> dict:
    out = {}
    for a, v in p.items():
        for b, w in q.items():
            out[a+b] = out.get(a+b, 0) + v*w
    return {a: v for a,v in out.items() if v != 0}

def product(ps) -> dict:
    out = {F(0): F(1)}
    for p in ps:
        out = mul(out, p)
    return out

def moment(a, prior=0, log=False):
    a = F(a)
    if prior == 0:
        return -1/(a+1)**2 if log else 1/(a+1)
    if prior == 1:
        return -2/(a+2)**2 if log else 2/(a+2)
    return -F(1,2)/(a+1)**2 if log else F(1,2)/(a+1)+F(1,2)*(a==0)

def integral(p, prior=0, shift=F(0), log=False):
    return sum((v*moment(a+shift,prior,log) for a,v in p.items()),F(0))

def rank(rows):
    return sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(rows)).rank()

def cells(theta):
    D=2+theta
    return [{F(0):F(1,3),F(1):-F(1,12),D:-F(1,12)},
            {F(0):F(1,3),F(1):F(1,12)},
            {F(0):F(1,3),D:F(1,12)}]

def add_scaled(ps, scales):
    out={}
    for p,s in zip(ps,scales):
        for a,v in p.items(): out[a]=out.get(a,0)+s*v
    return {a:v for a,v in out.items() if v!=0}

# Limiting strict mixed pairing, including higher confluent multiplicities.
minor=sp.Matrix([[sp.Rational(1,i+1),sp.Rational(1,i+2),sp.Rational(1,i+3),
                  -sp.Rational(1,(i+3)**2),sp.Rational(1,i+4),sp.Rational(1,i+5)]
                 for i in range(6)]).det()
check('six-by-six-limiting-minor',minor==sp.Rational(1,338751673344000000),determinant=str(minor))
for m in (2,3,4):
    pairs={(i+2*j,j) for j in range(m+1) for i in range(m-j+1)}
    counts={l:sum(a==l for a,b in pairs) for l in sorted({a for a,b in pairs})}
    columns=[(l,k) for l,n in counts.items() for k in range(n)]
    K=len(columns)
    mat=sp.Matrix([[sp.Rational((-1)**k,(i+l+1)**(k+1)) for l,k in columns] for i in range(K)])
    det=mat.det(method='domain-ge')
    check(f'confluent-clusters-m{m}',det>0,rows=K,cluster_multiplicities=counts,
          maximum_order=max(k for l,k in columns),determinant=str(det))

# Full normalized command Jacobians. No floating rank threshold is used here.
for theta in map(F,(0,F(1,64),F(1,8),F(1,2))):
    D=2+theta; ks=cells(theta)
    factors=[{F(0):F(1,2),D:F(i,128)} for i in (1,2,3)]
    for i,fac in enumerate(factors,1):
        c=F(i,64); rejections=[F(1,2)-2*c,F(1,2)-2*c,F(1,2)+4*c]
        check(f'attainable-theta{theta}-factor{i}',
              add_scaled(ks,rejections)==fac and all(F(1,4)<u<F(3,4) for u in rejections))
    P=product(factors)
    tangent=[mul(ks[j],product(factors[:i]+factors[i+1:])) for i in range(3) for j in range(3)]
    for prior in range(3):
        Z=integral(P,prior)
        shifts=[F(1),F(2),F(3)+theta,F(4)+2*theta]
        def test(p,k):
            if k<4: return integral(p,prior,shifts[k])
            if theta==0: return integral(p,prior,F(2),True)
            return (integral(p,prior,D)-integral(p,prior,F(2)))/theta
        J=[[(test(Q,k)*Z-test(P,k)*integral(Q,prior))/Z**2 for Q in tangent] for k in range(5)]
        check(f'desingularized-command-rank-{theta}-prior{prior}',rank(J)==5,rank=rank(J))
        physical=J[:4]+[[theta*x for x in J[4]]]
        expected=4 if theta==0 else 5
        check(f'physical-command-rank-{theta}-prior{prior}',rank(physical)==expected,rank=expected)

# A formal expansion in (lambda,gamma) pairs keeps the same labels at collision.
base=[{(0,0):F(1,3),(1,0):-F(1,12),(2,1):-F(1,12)},
      {(0,0):F(1,3),(1,0):F(1,12)}, {(0,0):F(1,3),(2,1):F(1,12)}]
probes=[]
for k in base:
    p={a:v/8 for a,v in k.items()};p[(0,0)]+=F(1,2);probes.append(p)
def pairmul(p,q):
    out={}
    for (a,b),v in p.items():
        for (c,d),w in q.items(): out[(a+c,b+d)]=out.get((a+c,b+d),0)+v*w
    return out
formal=[(0,0),(1,0),(2,0),(2,1),(3,1),(4,2)]
C=sp.Matrix([[pairmul(p,q).get(a,0) for a in formal] for p in probes for q in probes])
check('fixed-nine-query-formal-rank',C.rank()==6,rank=6)
weak=sum(C[j,3]**2 for j in range(9))/18
check('ticket-weak-coefficient',weak>0,b_star=str(weak))
# Substitute M_(2+theta)=M_2+theta*Z: the unscaled map stays injective.
T=sp.eye(6);T[3,2]=1
# Columns are [1,M1,M2,weak,M3+theta,M4+2theta].
G=C*T
check('fixed-scaled-query-map',G.rank()==6 and G[:,3]==C[:,3])
t=sp.symbols('theta',positive=True)
check('near-collision-L2-identity',sp.simplify(1/(5+2*t)-2/(5+t)+sp.Rational(1,5)
       -2*t**2/(5*(5+t)*(5+2*t)))==0)
p,q=sp.symbols('p q',real=True)
check('integrated-threshold-loss',sp.expand(p*p/2-(p*q-q*q/2)-(p-q)**2/2)==0)

# Exact Bayes shrinking formula compared with the unnormalized full product.
commands=[[F(1,3),F(1,2),F(2,3)],[F(2,3),F(1,3),F(1,2)]]
for theta in (F(0),F(1,16),F(1,2)):
    ks=cells(theta);D=2+theta
    report_factors=[]
    for g in commands:
        report_factors.extend([{a:g[j]*v for a,v in ks[j].items()} for j in range(3)])
        report_factors.append(add_scaled(ks,[1-u for u in g]))
    for word in ((0,1,2,3),(7,7,7,7),(3,7,3,0),(6,2,5,1)):
        P=product([report_factors[i] for i in word[:3]]);Z=integral(P)
        def M(a):return integral(P,shift=a)/Z
        w=[M(1),M(2),M(3+theta),M(4+2*theta),M(D)-M(2)]
        f=report_factors[word[3]];a,b,c=(f.get(v,0) for v in (F(0),F(1),D))
        den=a+b*w[0]+c*(w[1]+w[4])
        got=[(a*w[0]+b*w[1]+c*w[2])/den,
             (a*(w[1]+w[4])+b*w[2]+c*w[3])/den]
        exact=mul(P,f);zz=integral(exact)
        expected=[integral(exact,shift=s)/zz for s in (F(1),D)]
        check(f'exact-physical-update-{theta}-{word}',got==expected and den>=F(1,24))

# Rectangular integer allocation checks, including activation of a weak axis.
def allocation(widths,M):
    widths=np.asarray(widths,dtype=float)
    ix=np.argsort(-widths);positive=[i for i in ix if widths[i]>0]
    if not positive:return np.ones(len(widths),dtype=int),0.0
    cum=1.0;vals=[]
    for j,i in enumerate(positive,1):cum*=widths[i];vals.append((cum/M)**(1/j))
    e=max(vals)
    N=np.ones(len(widths),dtype=int)
    for i in positive:N[i]=max(1,int(math.floor(widths[i]/e+1e-12)))
    # Floating arithmetic at an exact integer boundary must never exceed M.
    while math.prod(map(int,N))>M:
        i=max(positive,key=lambda j:N[j]);N[i]-=1
    return N,e
for theta in (0.0,1/1024,1/16,0.5):
    for M in (1,2,5,16,100,4096,1000000):
        widths=[1,1,1,1,theta];N,e=allocation(widths,M)
        check(f'rectangle-budget-{theta}-{M}',math.prod(map(int,N))<=M and
              max(w/n for w,n in zip(widths,N))<=2*e+1e-12,
              subdivisions=N.tolist(),states=math.prod(map(int,N)))

# Actual finite-input, index-only transducers, quantized at every report.
class IndexOnly:
    __slots__=('index',)
    def __init__(self):self.index=0
    def read(self,table,input_symbol):self.index=int(table[self.index,input_symbol])

records=[]
for theta in (0.0,1/16,0.5):
    D=2+theta
    ks=[{0.0:1/3,1.0:-1/12,D:-1/12},{0.0:1/3,1.0:1/12},{0.0:1/3,D:1/12}]
    factors=[]
    for g0 in commands:
        g=list(map(float,g0))
        factors.extend([{a:g[j]*v for a,v in ks[j].items()} for j in range(3)])
        factors.append(add_scaled(ks,[1-u for u in g]))
    def integ(p,shift=0.0):return sum(v/(a+shift+1) for a,v in p.items())
    def normal(f):
        Z=integ(f);return (f.get(1.0,0)/Z,f.get(D,0)/Z)
    def decode_factors(s):
        return [{0.0:1-b/2-c/(D+1),1.0:b,D:c} for b,c in zip(s[::2],s[1::2])]
    def transition(n,s,ix):
        f=factors[ix]
        if n<2:return tuple(s)+normal(f)
        if n==2:
            P=product(decode_factors(s)+[f]);Z=integ(P)
            def mm(a):return integ(P,a)/Z
            return (mm(1),mm(2),mm(3+theta),mm(4+2*theta),mm(D)-mm(2))
        if n==3:
            a,b,c=(f.get(v,0.0) for v in (0.0,1.0,D));w=s
            Z=a+b*w[0]+c*(w[1]+w[4])
            return ((a*w[0]+b*w[1]+c*w[2])/Z,
                    (a*(w[1]+w[4])+b*w[2]+c*w[3])/Z)
        return ()
    universe=[[()]]
    for n in range(4):universe.append([transition(n,s,i) for s in universe[-1] for i in range(8)])
    query_polys={}
    fs=[]
    for k in ks:
        f={a:v/8 for a,v in k.items()};f[0.0]+=0.5;fs.append(f)
    for n in range(1,5):query_polys[n]=[product(ps) for ps in it.product(fs,repeat=5-n)]
    def predict(n,s):
        if n<=2:
            P=product(decode_factors(s));Z=integ(P)
            return np.array([integ(mul(P,h))/Z for h in query_polys[n]])
        if n==3:
            moments={0.0:1.0,1.0:s[0],2.0:s[1],D:s[1]+s[4],3+theta:s[2],4+2*theta:s[3]}
        else:moments={0.0:1.0,1.0:s[0],D:s[1]}
        return np.array([sum(v*moments[a] for a,v in h.items()) for h in query_polys[n]])
    for Msize in (1,4,16,64):
        reps=[[()]];quant=[lambda s:0]
        for stage in range(1,5):
            points=np.asarray(universe[stage]);lo=points.min(axis=0);hi=points.max(axis=0)
            widths=hi-lo;N,e=allocation(widths,Msize)
            def key(s,lo=lo,widths=widths,N=N):
                ar=np.asarray(s)
                if np.any(ar<lo-1e-10) or np.any(ar>lo+widths+1e-10):raise AssertionError('infeasible quantizer input')
                ratio=np.divide(ar-lo,widths,out=np.zeros_like(ar),where=widths>0)
                return tuple(np.clip(np.floor(ratio*N).astype(int),0,N-1))
            rep=[];lookup={}
            for s in universe[stage]:
                k=key(s)
                if k not in lookup:lookup[k]=len(rep);rep.append(s)
            def Q(s,key=key,lookup=lookup):return lookup[key(s)]
            reps.append(rep);quant.append(Q)
        tables=[np.asarray([[quant[n+1](transition(n,s,i)) for i in range(8)] for s in reps[n]],dtype=int)
                for n in range(4)]
        nodes=[((),0)];worst=[]
        for n in range(4):
            nxt=[];err=0.0
            for exact,index in nodes:
                for ix in range(8):
                    machine=IndexOnly();machine.index=index;machine.read(tables[n],ix)
                    truth=transition(n,exact,ix);j=machine.index
                    pred=predict(n+1,reps[n+1][j]);ptrue=predict(n+1,truth)
                    if np.any(pred<-1e-12) or np.any(pred>1+1e-12):raise AssertionError('nonprobability decoder')
                    err=max(err,float(np.mean((pred-ptrue)**2)));nxt.append((truth,j))
            nodes=nxt;worst.append(err)
        check(f'index-only-uniform-family-{theta}-M{Msize}',
              all(len(r)<=Msize for r in reps) and all(0<=i<Msize for _,i in nodes),
              input_symbols=8,prefixes_through_time_four=4096,state_counts=list(map(len,reps)))
        records.append({'theta':theta,'M':Msize,'state_counts':list(map(len,reps)),
                        'worst_regret_by_checkpoint':worst})
DETAILS['index_only_fixture']={'N':5,'query_checkpoint_choices':[1,2,3,4],
    'persistent_runtime_fields':['index'],'records':records,
    'scope':'Two fixed commands and four reports; floating diagnostics, not a continuum or all-budget proof.'}
receipt={'revision':'A1 English v7','python':platform.python_version(),'sympy':sp.__version__,
    'numpy':np.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'checks_passed':len(CHECKS),'checks_total':len(CHECKS),'all_passed':True,'checks':CHECKS,'details':DETAILS,
    'limitations':['Finite exact identities and finite-menu executions are diagnostics, not proofs of the uniform theorems.',
                   'No asymptotic conclusion is inferred from a finite input alphabet.',
                   'No formal verification, independent human review, exhaustive priority search or journal acceptance is asserted.']}
(ROOT/'DIAGNOSTICS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'passed':len(CHECKS),'total':len(CHECKS),'index_only_fixtures':len(records),
                  'limiting_minor':str(minor),'weak_coefficient':str(weak)},indent=2))
