#!/usr/bin/env python3
"""Exact finite identity checks and negative controls; not an analytic proof verifier."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import product
from math import comb, factorial
import json
from pathlib import Path
import sys
import sympy as S

MUTANTS=('resample_candidate','unpriced_erasure_memory','omit_innovation_shift','wrong_collision_modulus','insufficient_training','erase_preparation_mark')

class Check:
    def __init__(self, mutant: str | None): self.n=0; self.mutant=mutant
    def need(self, ok: bool, msg: str) -> None:
        self.n+=1
        if not ok: raise RuntimeError('FAILED: '+msg)

def counts(n: int, d: int):
    if d==1:
        yield (n,); return
    for k in range(n+1):
        for tail in counts(n-k,d-1): yield (k,)+tail

def multinomial(c: tuple[int,...], p: tuple[F,...]) -> F:
    v=F(factorial(sum(c)))
    for k,x in zip(c,p): v=v*x**k/factorial(k)
    return v

def tv(p, q): return sum((abs(a-b) for a,b in zip(p,q)), F(0))/2

def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument('--mutant',choices=MUTANTS); ap.add_argument('--write-certificates',type=Path); arg=ap.parse_args(); ck=Check(arg.mutant)
    # Backward continuation kernels for a genuinely stochastic, input-dependent toy machine.
    L=3; widths=(1,2,2,1); rows={}
    for t in range(L):
        for m,x in product(range(widths[t]),range(2)):
            w={(z,u):1+(t+2*m+3*x+z+u)%5 for z,u in product(range(2),range(widths[t+1]))}; den=sum(w.values())
            rows[t,m,x]={key:F(v,den) for key,v in w.items()}
            ck.need(sum(rows[t,m,x].values())==1,'stochastic row normalization')
    def residual(t,m,xs,zs):
        if t==L:return F(1)
        return sum((rows[t,m,xs[0]][zs[0],u]*residual(t+1,u,xs[1:],zs[1:]) for u in range(widths[t+1])),F(0))
    for t in range(L):
        for m in range(widths[t]):
            for xs in product(range(2),repeat=L-t):
                mass=sum((residual(t,m,xs,zs) for zs in product(range(2),repeat=L-t)),F(0))
                ck.need(mass==1,'normalized continuation slice')
                for z in range(2):
                    mass=sum((residual(t,m,xs,(z,)+zs) for zs in product(range(2),repeat=L-t-1)),F(0))
                    ck.need(mass==sum(rows[t,m,xs[0]][z,u] for u in range(widths[t+1])),'future-input independent shift mass')
    # Exact erasure cut: enumerate all deterministic encoders; optimal decoder per cell.
    cut_values=[]
    for N in range(2,7):
        pi=tuple(F(x,N*(N+1)//2) for x in range(1,N+1))
        for K in range(1,min(3,N)+1):
            optimum=F(0)
            for enc in product(range(K),repeat=N):
                val=sum((max((pi[x] for x in range(N) if enc[x]==m),default=F(0)) for m in range(K)),F(0))
                optimum=max(optimum,val)
            claimed=sum(sorted(pi,reverse=True)[:K])
            if arg.mutant=='unpriced_erasure_memory' and K==1:claimed=F(1)
            ck.need(optimum==claimed,'erasure cut retains exactly K symbols')
            cut_values.append({'N':N,'K':K,'error':str(1-optimum)})
    # Exact empirical variance and count normalization for a three-atom row.
    p=(F(1,6),F(1,3),F(1,2))
    for n in range(1,7):
        data=[(c,multinomial(c,p)) for c in counts(n,3)]
        ck.need(sum(v for c,v in data)==1,'multinomial count normalization')
        sq=sum((v*tv(tuple(F(x,n) for x in c),p)**2 for c,v in data),F(0))
        ck.need(sq<=F(2,4*n),'empirical variation second moment')
        for j in range(3):
            ck.need(sum(v*(F(c[j],n)-p[j])**2 for c,v in data)==p[j]*(1-p[j])/n,'coordinate variance')
    # Binary finite-reset game: exact optimal signed statistic and non-Dirac dual.
    binary=[]; h=F(1,16)
    for n in range(1,10):
        plus=[F(comb(n,k))*(F(1,2)+h)**k*(F(1,2)-h)**(n-k) for k in range(n+1)]; minus=plus[::-1]
        statistic=[F(1 if a>b else -1 if a<b else 0) for a,b in zip(plus,minus)]
        value=h*tv(plus,minus)
        ck.need(h*sum(a*d for a,d in zip(plus,statistic))==value,'binary plus score')
        ck.need(-h*sum(a*d for a,d in zip(minus,statistic))==value,'binary minus score')
        dual=sum((max(F(0),h*(a-b)/2,h*(b-a)/2) for a,b in zip(plus,minus)),F(0))
        if arg.mutant=='resample_candidate':dual=F(0)
        ck.need(dual==value and 0<value<h,'replicated mixture is not barycenter and not Dirac')
        binary.append({'n':n,'h':str(h),'value':str(value),'Dirac_objective':str(h)})
    # Exact chart coefficient span with an invisible redundant row.
    p,q,r=S.symbols('p q r'); polys=[S.Poly(p,p,q,r),S.Poly(q,p,q,r),S.Poly(p*q,p,q,r)]
    mons=sorted(set(m for f in polys for m,c in f.terms()))
    mat=S.Matrix([[f.coeff_monomial(m) for m in mons] for f in polys])
    ck.need(mat.rank()==3,'computed observable dimension ignores unused row r')
    sample=S.Matrix([[1,0,1],[0,1,1],[0,0,1]])
    ck.need(sample.det()==1,'rational sample basis')
    y=S.Matrix([p,q,p*q]); coord=sample.inv()*y
    ck.need(sample*coord==y,'exact rational chart pullback')
    # Rational physical certificate, independent of simulator parameters.
    n=2800 if arg.mutant!='insufficient_training' else 700
    root_lower=F(947,600); ideal_lower=root_lower-F(9,8)
    ck.need(F(5,2)-root_lower**2==F(3191,360000),'positive exact radical margin')
    ck.need(F(7,n)<=F(1,20)**2,'2800-reset approximation budget')
    ck.need(ideal_lower-F(1,20)-F(1,300)==F(2,5),'uniform certificate strict threshold')
    ck.need(F(1,8)+F(1,300)<F(13,100),'hidden physical upper bound')
    target=[F(5 if w==b else 3,16) if b==c else F(0) for w,b,c in product(range(2),repeat=3)]
    if arg.mutant=='erase_preparation_mark':target=[F(1,4) if b==c else F(0) for w,b,c in product(range(2),repeat=3)]
    ck.need(sum(target)==1 and target[0]==F(5,16) and target[4]==F(3,16),'actual prepared mark is retained')
    ck.need(F(1000,1443)<1,'collision-time derivative bound')
    ck.need(F(3+1,1)/F(9,10)<5,'normal derivative bound')
    ck.need(2*3*5==30,'outgoing velocity Lipschitz bound')
    quadratic=2700 if arg.mutant!='wrong_collision_modulus' else 900
    ck.need(quadratic>=3*30**2,'whole-time post-collision squared-signal bound')
    ck.need(3+3*30+4<100,'aligned position constant')
    # Symbolic innovation correction in the entropic equation.
    u,v,gamma=S.symbols('u v gamma',nonzero=True)
    drift=-(u*u-v*v)/(2*gamma)+(u-v)*v/gamma
    if arg.mutant=='omit_innovation_shift':drift=-(u*u-v*v)/(2*gamma)
    ck.need(S.expand(drift+(u-v)**2/(2*gamma))==0,'innovation drift equals negative quadratic generator')
    # Diagnostic of the exact historical normalization mismatch, not a new B4 theorem.
    lam,mu=F(2),F(3)
    ck.need(F(0)!=(mu-lam)*1,'historical displayed normalized resolvent identity fails on one')
    ck.need(mu-lam==(mu-lam)*1,'linear normalized alternative is consistent on constants')
    state_count=8*257*comb(2807,7)
    certificate={'kind':'procedural rational expected-score certificate','training_trials':2800,'row':'all-on marked (W,Z1,Z2), lexicographic eight-atom order','target_probabilities':[str(v) for v in target],'event_rule':'Choose the smallest mask A in 0..255 maximizing Qstar(A)-sum(C[w] for w in A)/2800. Empty event allowed. Candidate design remains fixed.','validation':'Independent physical target and candidate trials; score 1_A(target)-1_A(candidate).','auditor_state_bound':str(state_count),'threshold':'2/5','proof_inequality':'sqrt(5/2)-9/8-sqrt(7/2800)-1/300 > 2/5','rational_root_lower':'947/600','squared_root_margin':'3191/360000','scope':'Expected signed score, width-one private candidate, blind source, actual marked target. Not a stored table or confidence guarantee.'}
    result={'scope':'finite exact identities and designated implementation-error checks only; not analytic proof certification','checks':ck.n,'erasure_examples':cut_values,'binary_games':binary,'audit_certificate':certificate,'collision_constants':{'time':1,'normal':5,'velocity':30,'energy_quadratic':2700,'path_metric':100},'historical_B4_normalization_diagnostic':'literal formula rejected on constant-one payoff'}
    if arg.write_certificates:
        arg.write_certificates.mkdir(parents=True,exist_ok=True)
        (arg.write_certificates/'AUDIT_CERTIFICATE.json').write_text(json.dumps(certificate,indent=2)+'\n')
    if arg.mutant:raise RuntimeError('designated mutant survived')
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':
    try: main()
    except Exception as exc:
        print(str(exc),file=sys.stderr);sys.exit(1)
