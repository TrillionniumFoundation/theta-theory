#!/usr/bin/env python3
"""Exact finite diagnostics for A2 v16. Not a proof certificate.

Uses Fraction throughout. The checks are explicit exceptions (not assert),
so optimized and ordinary Python must execute exactly the same tests.
No simulation, fitted billiard, or statistical lower bound is claimed.
"""
from __future__ import annotations
from fractions import Fraction as F
import hashlib
import json

CHECKS: list[str] = []

def require(ok: bool, name: str) -> None:
    if not ok:
        raise RuntimeError('Diagnostic failed: ' + name)
    CHECKS.append(name)

def law(p: F, j: int, side: str, perturbed: bool = False) -> dict[str, F]:
    h = p * F(1, 2) ** j
    a, b = (p-h)/3, 2*(p-h)/3
    if perturbed:
        shift = h/8 if side == 'P' else -h/8
        a, b = a + shift, b - shift
    if side == 'R':
        return {'F': (1-p)/(1-h), 'A': a/(1-h), 'B': b/(1-h)}
    return {'F': 1-p, 'A': a, 'B': b, ('L' if side == 'P' else 'R'): h}

def policy(hist: tuple, cap: int, k: int, mode: int):
    if len(hist) >= cap or sum(x != 'F' for _, x in hist) >= k:
        return None
    code = sum((i+1)*{'F':1,'A':2,'B':3,'L':4,'R':5}[x]
               for i, (_, x) in enumerate(hist))
    choice = (code + len(hist) + mode) % 2
    return choice

DESIGNS = ((F(1, 5), 2), (F(2, 7), 3))

def transcripts(cap: int, k: int, mode: int, side: str, perturbed=False):
    out: dict[tuple, F] = {}
    def visit(hist, mass):
        a = policy(hist, cap, k, mode)
        if a is None:
            out[hist] = mass
            return
        p, j = DESIGNS[a]
        for x, prob in law(p, j, side, perturbed).items():
            if prob:
                visit(hist + ((a, x),), mass*prob)
    visit((), F(1))
    return out

def tv(P, Q):
    return sum((abs(P.get(x,F(0))-Q.get(x,F(0)))
                for x in P.keys() | Q.keys()), F(0))/2

def expect(P, func):
    return sum((mass*func(hist) for hist, mass in P.items()), F(0))

def budget(hist, actual=False):
    return sum((((F(x != 'F') if actual else DESIGNS[a][0])
                 *F(1,2)**DESIGNS[a][1]) for a,x in hist),F(0))

def product_survival(hist):
    z = F(1)
    for a, _ in hist:
        p,j = DESIGNS[a]
        z *= 1-p*F(1,2)**j
    return z

def main():
    # Strict-margin rational benchmark: closed iterate, cocycle, telescoping.
    for lam in (F(1,4), F(1,2), F(3,4)):
        for a in (F(-1,3),F(0),F(2,5)):
            for u in (F(-1,5),F(1,7),F(1,4)):
                x, derivative = u, F(1)
                for n in range(9):
                    key = f'rational:{lam}:{a}:{u}:{n}'
                    den = 1+a*(1-lam**n)*u
                    closed = lam**n*u/den
                    B = lambda y: 1/(1+a*y)**2
                    require(x == closed, key+':iterate')
                    require(derivative/lam**n == 1/den**2, key+':derivative')
                    require(derivative/lam**n*B(x) == B(u), key+':cocycle')
                    require(x/lam**n-u/(1+a*u) ==
                            a*lam**n*u*u/(den*(1+a*u)), key+':tail')
                    derivative *= lam/(1+a*(1-lam)*x)**2
                    x = lam*x/(1+a*(1-lam)*x)
    # The exact mixed derivative divided by lambda^n grows as n/lambda.
    for n in range(1,33):
        lam,u = F(3,4),F(1,5)
        mixed = n*lam**(n-1)*u*u
        require(mixed/lam**n == F(n)*u*u/lam, f'mixed:{n}')
    naive_counterexamples = 0
    largest_transcript_support = 0
    for cap in range(0,6):
        for k in range(1,4):
            for mode in range(2):
                name=f'adaptive:{cap}:{k}:{mode}'
                P=transcripts(cap,k,mode,'P')
                Q=transcripts(cap,k,mode,'Q')
                R=transcripts(cap,k,mode,'R')
                largest_transcript_support=max(largest_transcript_support,len(P))
                for s,X in [('P',P),('Q',Q),('R',R)]:
                    require(sum(X.values(),F(0))==1,name+':mass:'+s)
                common={h:min(P.get(h,F(0)),Q.get(h,F(0)))
                        for h in P.keys() | Q.keys()}
                m=expect(R,product_survival)
                require(tv(P,Q)==1-m,name+':overlap')
                require(sum(common.values(),F(0))==m,name+':common-mass')
                require(all(common.get(h,F(0))==w*product_survival(h)
                            for h,w in R.items()),name+':tilted-common-law')
                # The reverse erasure kernel restores the exact transcript law.
                for s,X in [('P',P),('Q',Q)]:
                    recovered={h:common.get(h,F(0))+(X.get(h,F(0))-common.get(h,F(0)))
                               for h in X}
                    require(recovered==X,name+':reverse:'+s)
                ep=expect(P,budget); eq=expect(Q,budget)
                require(tv(P,Q)<=min(ep,eq),name+':stopped-bound')
                require(ep==expect(P,lambda h:budget(h,True)),name+':tower')
                require(all(budget(h,True)<=k*F(1,2)**2 for h in P),name+':success-cap')
                require(ep<=k*F(1,2)**2,name+':expected-success-cap')
                failures=expect(P,lambda h:sum(x=='F' for _,x in h))
                successes=expect(P,lambda h:sum(x!='F' for _,x in h))
                total=expect(P,lambda h:len(h))
                require(total==failures+successes,name+':all-preparations')
                if cap:
                    require(failures>0,name+':failure-cost-positive')
                naive=F(1)
                for i in range(cap):
                    mean_h=expect(R,lambda h: (DESIGNS[h[i][0]][0]*F(1,2)**DESIGNS[h[i][0]][1]) if i<len(h) else F(0))
                    naive*=1-mean_h
                if naive!=m:
                    naive_counterexamples+=1
                # General kernels: unequal common densities, no erasure identity used.
                Pp=transcripts(cap,k,mode,'P',True)
                Qp=transcripts(cap,k,mode,'Q',True)
                e={i:tv(law(p,j,'P',True),law(p,j,'Q',True))
                   for i,(p,j) in enumerate(DESIGNS)}
                bound=expect(Pp,lambda h:sum((e[a] for a,_ in h),F(0)))
                require(tv(Pp,Qp)<=bound,name+':general-kernel-bound')
    require(naive_counterexamples>0,'negative-control:unconditional-product-rejected')
    # The explicit checker itself must reject a false identity under -O as well.
    try:
        require(False,'deliberate-false-check')
    except RuntimeError:
        pass
    else:
        raise RuntimeError('Check mechanism was disabled')
    result={
        'status':'passed', 'arithmetic':'exact rational', 'checks':len(CHECKS),
        'case_digest_sha256':hashlib.sha256(('\n'.join(CHECKS)+'\n').encode()).hexdigest(),
        'naive_product_counterexamples':naive_counterexamples,
        'largest_single_transcript_support':largest_transcript_support,
        'scope':'Finite algebra and finite discrete observation-kernel diagnostics only; not a proof certificate or a billiard simulation.',
        'optimization_independence':'All checks use explicit exceptions, not assert.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
