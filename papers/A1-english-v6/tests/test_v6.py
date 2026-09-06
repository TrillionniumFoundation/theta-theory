#!/usr/bin/env python3
"""Exact finite diagnostics for A1 v6; not a formal proof certificate.

Requires Python >=3.10 and SymPy. Run from any directory:
    python tests/test_v6.py
Outputs DIAGNOSTICS.json beside main.tex. The finite-command streaming
example is deliberately not used to infer a continuous-input asymptotic law.
"""
from __future__ import annotations
import hashlib
import itertools as it
import json
import math
from collections import Counter
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from pathlib import Path
import platform
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
CHECKS: list[dict] = []
DETAILS: dict = {}

def check(name: str, condition: bool, **detail) -> None:
    if not bool(condition):
        raise AssertionError(f"{name}: {detail}")
    CHECKS.append({"name": name, "passed": True, **detail})

def ss(A, n):
    out = {F(0)}
    for _ in range(n):
        out = {x + a for x in out for a in A}
    return sorted(out)

def mul(p, q):
    out = {}
    for a, v in p.items():
        for b, w in q.items():
            out[a+b] = out.get(a+b, F(0)) + v*w
    return {a: v for a, v in out.items() if v}

def prod(ps):
    out = {F(0): F(1)}
    for p in ps:
        out = mul(out, p)
    return out

def mom(a, prior=0):
    a = F(a)
    # Full-support uniform, triangular, and half-uniform/half-atom priors.
    if prior == 0:
        return 1/(a+1)
    if prior == 1:
        return 2/(a+2)
    # The mixed prior is used only with integral exponents below.
    return F(1,2)/(a+1) + F(1,2)*F(1,2)**int(a)

def integ(p, prior=0, shift=F(0)):
    return sum((v*mom(a+shift, prior) for a, v in p.items()), F(0))

def rank(rows):
    return sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(rows)).rank()

# 1. Sumsets and the three-generator Hilbert function, including gcd cases.
for a, b in [(1,2),(1,7),(2,5),(3,8),(4,10),(6,15),(5,13)]:
    B = b//math.gcd(a,b)
    vals = [len(ss([0,a,b], m)) for m in range(2*B+3)]
    predicted = [math.comb(m+2,2) - (math.comb(m-B+2,2) if m>=B else 0)
                 for m in range(2*B+3)]
    check(f"hilbert-{a}-{b}", vals == predicted, degrees=len(vals))
A = [F(0),F(2),F(5)]
profile = [min(2*n,len(ss(A,6-n))-1) for n in range(7)]
check("asymmetric-six-trial-profile", profile == [0,2,4,6,5,2,0], profile=profile)

# 2. Full attainable product derivatives and normalized prediction ranks.
cases = [([0,1],1,4,0),([0,1],3,2,0),([0,1,2,3],2,2,0),
         ([0,2,5],3,2,0),([0,2,5],2,3,0),([0,2,5],3,3,1),
         ([0,2,5],3,2,2),([0,1,4,9],2,2,0),
         ([0,3,7,8],3,1,1),([0,4,10],2,3,0),
         ([F(0),F(1,2),F(3,2)],3,2,0),
         ([F(0),F(2,3),F(7,4)],2,3,1)]
for ix,(aval,n,m,prior) in enumerate(cases):
    aval = list(map(F,aval)); r=len(aval); D=aval[-1]
    c = [F(i+1,100000) for i in range(n)]
    fs = [{F(0): F(1,2), D: x/2} for x in c]
    P=prod(fs); Z=integ(P,prior); S=ss(aval,m)
    variations = [mul({a:F(1)},prod(fs[:i]+fs[i+1:]))
                  for i in range(n) for a in aval]
    support=sorted(set().union(*(p.keys() for p in variations)))
    tangent_rows=[[p.get(a,F(0)) for p in variations] for a in support]
    expected_B = sorted({j*D for j in range(n+1)} |
                        {a+j*D for a in aval[1:-1] for j in range(n)})
    check(f"tangent-support-{ix}", support==expected_B)
    check(f"tangent-rank-{ix}", rank(tangent_rows)==n*(r-1)+1)
    J=[[(Z*integ(V,prior,s)-integ(P,prior,s)*integ(V,prior))/Z**2
        for V in variations] for s in S[1:]]
    d=min(n*(r-1),len(S)-1)
    check(f"normalized-pairing-{ix}", rank(J)==d,
          exponents=list(map(str,aval)),n=n,m=m,prior=prior,rank=d)
    # All binomial factors are implemented in the same positive r-cell cube.
    delta=F(1,4*r*(r-1))
    cells=[{F(0):F(1,r),a:delta} for a in aval[1:]]
    cells.append({F(0):F(1,r),**{a:-delta for a in aval[1:]}})
    for ci,Fi in zip(c,fs):
        u0=F(1,2)-ci/(2*r*delta)
        us=[u0+(ci/(2*delta) if a==D else 0) for a in aval[1:]]+[u0]
        realized={}
        for uj,k in zip(us,cells):
            for a,v in k.items(): realized[a]=realized.get(a,F(0))+uj*v
        realized={a:v for a,v in realized.items() if v}
        check(f"same-cube-witness-{ix}-{ci}",
              min(us)>F(1,4) and max(us)<F(3,4) and realized==Fi)

# 3. Strict mixed minors (sampled sizes, exact, not an all-size certificate).
B=[0,2,5,7,10,12,15]; S=[0,2,4,5,7,10]
minor_count=0
for size in (1,2,3):
    for rows in it.combinations(B,size):
        for cols in it.combinations(S,size):
            det=sp.det(sp.Matrix([[F(1,x+y+1) for y in cols] for x in rows]))
            if not det>0: raise AssertionError((rows,cols,det))
            minor_count+=1
check("strict-mixed-minors",True,exact_minors=minor_count)

# 4. Reproduce the referee's non-binomial rank-five determinant verbatim.
fs=[{F(0):F(1),F(2):F(2*i+1,1000),F(5):F(2*i+2,1000)} for i in range(3)]
P=prod(fs); Z=integ(P)
vs=[mul({F(a):F(1)},prod(fs[:i]+fs[i+1:])) for i in range(3) for a in (2,5)]
J=sp.Matrix([[(Z*integ(v,shift=F(s))-integ(P,shift=F(s))*integ(v))/Z**2
             for v in vs] for s in (2,4,5,7,10)])
refdet=F(-149355957460881864071474244699533159667968750000000000000,
321006326403084606311224880739213913091275853342726956011747270080699228465818648617)
check("referee-original-rank-five", J.rank()==5 and J[:,:5].det()==refdet,
      attribution="v5 referee report section 7, not a new example")
for i,fi in enumerate(fs):
    a,b=fi[F(2)],fi[F(5)]
    u=[F(1,2)+4*a-2*b,F(1,2)-2*a+4*b,F(1,2)-2*a-2*b]
    check(f"referee-original-gate-{i}",min(u)>F(1,4) and max(u)<F(3,4))

# 5. Sparse moment recursion independently compared with direct multiplication.
for aval in ([0,2,5],[0,1,4,9],[0,3,7]):
    for m in (1,2,3):
        factors=[{F(0):F(1,2),F(a):F(1,100+i)} for i,a in enumerate(aval[1:])]
        P=prod(factors); Z=integ(P)
        M={s:integ(P,shift=s)/Z for s in ss(aval,m)}
        f={F(0):F(1,2),**{F(a):F(1,300+int(a)) for a in aval[1:]}}
        denom=sum((v*M[a] for a,v in f.items()),F(0))
        Pnext=mul(P,f); Zn=integ(Pnext)
        direct={s:integ(Pnext,shift=s)/Zn for s in ss(aval,m-1)}
        updated={s:sum((v*M[s+a] for a,v in f.items()),F(0))/denom
                 for s in ss(aval,m-1)}
        check(f"sparse-update-{aval}-{m}",updated==direct and denom>0)

# 6. Rational outward intervals for the actual mechanical constants.
class IV:
    __slots__=("lo","hi")
    def __init__(self,lo,hi=None): self.lo=F(lo); self.hi=F(lo if hi is None else hi)
    @staticmethod
    def cast(x): return x if isinstance(x,IV) else IV(x)
    def __add__(self,x):
        x=self.cast(x); return IV(self.lo+x.lo,self.hi+x.hi)
    __radd__=__add__
    def __neg__(self): return IV(-self.hi,-self.lo)
    def __sub__(self,x): return self+-self.cast(x)
    def __rsub__(self,x): return self.cast(x)+-self
    def __mul__(self,x):
        x=self.cast(x); ps=[a*b for a in (self.lo,self.hi) for b in (x.lo,x.hi)]
        return IV(min(ps),max(ps))
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.cast(x)
        if x.lo<=0<=x.hi: raise ZeroDivisionError("interval contains zero")
        return self*IV(1/x.hi,1/x.lo)
    def __rtruediv__(self,x): return self.cast(x)/self
    def __pow__(self,n):
        if n<0: return IV(1)/(self**(-n))
        out=IV(1)
        for _ in range(n): out=out*self
        return out
    def enclosure(self):
        vals=[]
        for x,rounding in ((self.lo,ROUND_FLOOR),(self.hi,ROUND_CEILING)):
            with localcontext() as ctx:
                ctx.prec=35; ctx.rounding=rounding
                vals.append(str(Decimal(x.numerator)/Decimal(x.denominator)))
        return vals

def atan_interval(x,n):
    x=F(x); s=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
    t=s+(-1)**n*x**(2*n+1)/F(2*n+1)
    return IV(min(s,t),max(s,t))
PI=16*atan_interval(F(1,5),80)-4*atan_interval(F(1,239),25)
scale=10**100; root=math.isqrt(3*scale**2)
area=IV(F(root,2*scale),F(root+1,2*scale))
l,u=F(9,20),F(47,100)
mu={j:(u**(j+1)-l**(j+1))/((j+1)*(u-l)) for j in range(6)}
T=F(1,20); epsilon=F(1,20)
hbar=PI*mu[2]/area
ps=[PI*mu[2]/area,1-PI*mu[2]/area-2*T*mu[1]/area,
    T*mu[1]/area+2*T*epsilon*mu[3]/(PI*area),
    T*mu[1]/area-2*T*epsilon*mu[3]/(PI*area)]
zs=[PI**2*mu[4]/area**2,PI*mu[2]/area-PI**2*mu[4]/area**2-2*T*PI*mu[3]/area**2,
    T*PI*mu[3]/area**2+2*T*epsilon*mu[5]/area**2,
    T*PI*mu[3]/area**2-2*T*epsilon*mu[5]/area**2]
check("physical-cell-masses-positive", all(p.lo>0 for p in ps))
v=mu[5]/mu[1]-(mu[3]/mu[1])**2
cbar=IV(F(1,2))+epsilon/PI*(mu[3]/mu[1])
Delta=(2*T*mu[1]/area)*(epsilon*v/area)**2/(cbar*(1-cbar))
check("physical-hit-variance", v==F(529,18750000))
check("physical-gain-referee-enclosure",
      Delta.lo>F(5637602588099328,10**28) and Delta.hi<F(5637602588099330,10**28))

def partitions(n):
    if n==0: yield (); return
    for blocks in partitions(n-1):
        yield blocks+((n-1,),)
        for i in range(len(blocks)):
            yield blocks[:i]+(blocks[i]+(n-1,),)+blocks[i+1:]

def score(blocks,p,z):
    return sum((sum((z[j] for j in b),IV(0))**2/sum((p[j] for j in b),IV(0))
                for b in blocks),IV(0))

def paircost(i,j):
    return ps[i]*ps[j]/(ps[i]+ps[j])*(zs[i]/ps[i]-zs[j]/ps[j])**2
pairs={(i,j):paircost(i,j) for i,j in it.combinations(range(4),2)}
check("three-state-optimal-sign-merge",
      all(pairs[(2,3)].hi<x.lo for ij,x in pairs.items() if ij!=(2,3)))
pe=[ps[0],ps[1],ps[2]+ps[3]]; ze=[zs[0],zs[1],zs[2]+zs[3]]
raw=list(partitions(4)); erased=list(partitions(3))
check("two-block-partition-counts",sum(len(q)==2 for q in raw)==7 and
      sum(len(q)==2 for q in erased)==3)
raw2=[(q,score(q,ps,zs)) for q in raw if len(q)==2]
same=[(q,s) for q,s in raw2 if any(2 in b and 3 in b for b in q)]
split=[(q,s) for q,s in raw2 if all(not (2 in b and 3 in b) for b in q)]
best=max(same,key=lambda item:item[1].lo)
check("two-state-optimal-sign-coarsening",
      all(best[1].lo>s.hi for _,s in split),best_partition=best[0])
check("four-state-positive-common-risk-gain",Delta.lo>0)
DETAILS["physical_instance"]={"T":"1/20","epsilon":"1/20", "prior":"uniform [9/20,47/100]",
    "constants":"pi: Machin alternating series; sqrt(3): rational integer-sqrt enclosure",
    "gain_enclosure":Delta.enclosure(),"hit_variance":str(v),
    "certified_gamma_M1_M2_M3":"0", "gamma_M_ge4":"gain_enclosure",
    "two_state_best_partition":best[0]}

# 7. A real index-only transducer on a finite rational diagnostic menu.
# This fixture is not substituted for the continuous-input theorem.
commands=list(it.product((F(1,4),F(1,2),F(3,4)),repeat=2))
inputs=list(it.product(range(len(commands)),range(3)))

def factor(command_index,report):
    g0,g1=commands[command_index]
    if report==0: return {F(0):g0/2,F(1):g0/8}
    if report==1: return {F(0):g1/2,F(1):-g1/8}
    return {F(0):(2-g0-g1)/2,F(1):(g1-g0)/8}

def normfactor(slope): return {F(0):1-slope/2,F(1):slope}

def transition(stage,state,inp):
    f=factor(*inp)
    if stage<2: return state+(f[F(1)]/integ(f),)
    if stage==2:
        P=mul(prod([normfactor(v) for v in state]),f)
        return (integ(P,shift=F(1))/integ(P),)
    return ()

universe=[{()}]
for stage in range(4):
    universe.append({transition(stage,s,inp) for s in universe[-1] for inp in inputs})

def quantizer(states,M):
    if len(next(iter(states)))==0: return [()],lambda _:0
    d=len(next(iter(states))); k=math.isqrt(M) if d==2 else M
    low=[min(s[j] for s in states) for j in range(d)]
    high=[max(s[j] for s in states) for j in range(d)]
    def cell(s):
        return tuple(0 if high[j]==low[j] else
                     min(k-1,int((s[j]-low[j])*k/(high[j]-low[j]))) for j in range(d))
    rep={}
    for s in sorted(states): rep.setdefault(cell(s),s)
    keys=sorted(rep); table={key:i for i,key in enumerate(keys)}
    reps=[rep[key] for key in keys]
    return reps,lambda s:table[cell(s)]

class IndexOnly:
    __slots__=("index",)
    def __init__(self,index=0): self.index=index
    def read(self,table,input_number): self.index=table[self.index][input_number]

stream_records=[]
for Msize in (1,2,4,8,16):
    reps=[]; quant=[]
    for states in universe:
        r,q=quantizer(states,Msize); reps.append(r); quant.append(q)
    tables=[[[quant[n+1](transition(n,s,inp)) for inp in inputs] for s in reps[n]]
            for n in range(4)]
    # Harness carries the exact state; the tested transducer carries one integer.
    nodes={((),0)}; worst=F(0); paths=1
    for n in range(3):
        new=set()
        for exact,idx in nodes:
            for ix,inp in enumerate(inputs):
                machine=IndexOnly(idx); machine.read(tables[n],ix)
                truth=transition(n,exact,inp)
                new.add((truth,machine.index))
        nodes=new; paths*=len(inputs)
    for truth,idx in nodes:
        # At time 3, a one-step raw-first-cell query is an observable test.
        p=F(1,2)+truth[0]/8; phat=F(1,2)+reps[3][idx][0]/8
        worst=max(worst,(p-phat)**2)
    check(f"index-only-streaming-{Msize}",
          all(len(r)<=Msize for r in reps) and all(0<=i<Msize for _,i in nodes),
          menu_size=len(inputs),prefixes_covered=paths,reachable_oracle_index_pairs=len(nodes))
    stream_records.append({"M":Msize,"state_counts":list(map(len,reps)),
                           "worst_Brier_excess":str(worst)})
DETAILS["streaming_fixture"]={"scope":"finite rational menu only; no asymptotic inference",
    "N":4,"A":[0,1],"records":stream_records,"persistent_runtime_fields":["index"]}

check("rare-probe-zero-memory-bound",F(5,8)**40<F(1,10**8))
check("volume-integral-constant",sp.integrate(1-sp.Symbol('x')**(sp.Rational(5,2)),
      (sp.Symbol('x'),0,1))==sp.Rational(5,7))

receipt={"revision":"A1 English v6","python":platform.python_version(),"sympy":sp.__version__,
    "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "checks_passed":len(CHECKS),"checks_total":len(CHECKS),"all_passed":True,
    "checks":CHECKS,"details":DETAILS,
    "limitations":["Finite diagnostics do not prove the all-budget or topological theorems.",
        "Prior v5 author and referee suites were not rerun or relabeled as current tests.",
        "The finite-menu transducer fixture does not test a continuous-input asymptotic exponent.",
        "This is not formal proof verification or an independent human referee report."]}
(ROOT/'DIAGNOSTICS.json').write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"passed":len(CHECKS),"total":len(CHECKS),"mixed_minors":minor_count,
                  "physical_gain":Delta.enclosure(),"streaming":stream_records},indent=2))
