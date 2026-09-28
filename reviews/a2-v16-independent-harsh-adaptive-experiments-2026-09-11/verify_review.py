#!/usr/bin/env python3
"""Independent finite diagnostics for the source-pinned A2 v16 review.
Standard library only. Exact fractions; explicit checks survive python -O.
These are finite identities/kernel tests, not proof or billiard certificates.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from fractions import Fraction as F
from math import comb, factorial
import hashlib
import json
from pathlib import Path

COUNTS = Counter()
DIGEST = hashlib.sha256()

def check(group: str, name: str, condition: bool, value: object = None) -> None:
    if not condition:
        raise RuntimeError(f'{group}: {name}: {value!r}')
    COUNTS[group] += 1
    DIGEST.update(f'{group}|{name}|{value!r}\n'.encode())

def law(kernels: dict, policy, cap: int, seed: int = 0) -> dict:
    result = defaultdict(F)
    def walk(history: tuple, mass: F) -> None:
        action = policy(history, seed)
        if len(history) == cap or action is None:
            result[history] += mass
            return
        for record, probability in kernels[action].items():
            if probability:
                walk(history + ((action, record),), mass * probability)
    walk((), F(1))
    return dict(result)

def tv(p: dict, q: dict) -> F:
    return sum((abs(p.get(x, F(0))-q.get(x, F(0)))
                for x in p.keys() | q.keys()), F(0))/2

def expectation(p: dict, function) -> F:
    return sum((mass*function(history) for history, mass in p.items()), F(0))

def stopped_kernels() -> None:
    for case in range(1, 5):
        P, Q = {}, {}
        for a in range(2):
            x, y = F(case+a+1, 12), F(2+a, 12)
            shift = F(a+1, 60)
            P[a] = {0:1-x-y, 1:x, 2:y}
            Q[a] = {0:1-x-y-shift, 1:x+shift/2, 2:y+shift/2}
        errors = {a:tv(P[a], Q[a]) for a in P}
        for cap in range(5):
            for seed in range(2):
                for stop_kind in range(3):
                    def policy(h, s):
                        successes = sum(y != 0 for _, y in h)
                        if ((stop_kind == 1 and successes >= 1)
                            or (stop_kind == 2 and len(h) >= 2 and h[-1][1] == 0)):
                            return None
                        return (s+sum(y for _, y in h)+len(h)) % 2
                    p, q = law(P, policy, cap, seed), law(Q, policy, cap, seed)
                    ep = expectation(p, lambda h:sum((errors[a] for a,_ in h), F(0)))
                    eq = expectation(q, lambda h:sum((errors[a] for a,_ in h), F(0)))
                    value = tv(p,q)
                    key = f'{case}/{cap}/{seed}/{stop_kind}'
                    check('stopped_kernel',key, sum(p.values()) == sum(q.values()) == 1
                          and value <= min(F(1),ep,eq), (value,ep,eq))
    tau = F(1,3)
    P = {0:{0:F(3,4),1:F(1,4)},1:{0:F(2,3),1:F(1,3)}}
    probs = {a:P[a][1] for a in P}
    Q = {a:{0:1-probs[a]*(1+tau**(a+1)/4),
            1:probs[a]*(1+tau**(a+1)/4)} for a in P}
    for cap in range(1,7):
        for k in (1,2,3):
            for seed in (0,1):
                def policy(h,s):
                    if sum(y for _,y in h) >= k:
                        return None
                    return (s+len(h)+sum(y for _,y in h)) % 2
                p,q = law(P,policy,cap,seed),law(Q,policy,cap,seed)
                predictable = expectation(p,lambda h:sum((probs[a]*tau**(a+1) for a,_ in h),F(0)))
                realized = expectation(p,lambda h:sum((y*tau**(a+1) for a,y in h),F(0)))
                cost = expectation(p,lambda h:F(len(h)))
                successes = expectation(p,lambda h:F(sum(y for _,y in h)))
                check('success_budget',f'{cap}/{k}/{seed}',predictable == realized
                      and realized <= k*tau and tv(p,q) <= predictable/4
                      and cost > successes, (predictable,realized,cost,successes,tv(p,q)))

def overlap() -> dict:
    hazards = {0:F(1,5),1:F(1,10),2:F(2,5)}
    P = {a:{'c0':(1-h)/2,'c1':(1-h)/2,'p':h} for a,h in hazards.items()}
    Q = {a:{'c0':(1-h)/2,'c1':(1-h)/2,'q':h} for a,h in hazards.items()}
    R = {a:{'c0':F(1,2),'c1':F(1,2)} for a in hazards}
    witness = {}
    for cap in range(6):
        for mode in range(3):
            def policy(h,s):
                if not h:
                    return 0
                if mode == 1 and h[-1][1] in ('p','q'):
                    return None
                if mode == 2 and len(h) >= 2 and h[-1][1] == 'c1':
                    return None
                return 1 if h[0][1] == 'c0' else 2
            p,q,r = law(P,policy,cap),law(Q,policy,cap),law(R,policy,cap)
            def weight(h):
                z=F(1)
                for a,_ in h:
                    z *= 1-hazards[a]
                return z
            common = {h:v*weight(h) for h,v in r.items()}
            m=sum(common.values(),F(0))
            minimum = {h:min(p.get(h,F(0)),q.get(h,F(0)))
                       for h in p.keys() | q.keys()}
            check('common_history',f'{cap}/{mode}',tv(p,q)==1-m
                  and all(minimum.get(h,F(0))==common.get(h,F(0)) for h in minimum.keys()|common.keys()),m)
            for label,marginal in [('p',p),('q',q)]:
                reconstructed = {h:common.get(h,F(0))+
                                 (v if minimum.get(h,F(0))==0 else F(0))
                                 for h,v in marginal.items()}
                check('reverse_erasure',f'{cap}/{mode}/{label}',reconstructed==marginal, m/2)
            if cap == 3 and mode == 0:
                naive = (1-hazards[0])*(1-(hazards[1]+hazards[2])/2)**2
                posterior = sum(v for h,v in common.items() if h[0][1]=='c0')/m
                check('negative_control','adaptive_product',m==F(117,250)
                      and naive==F(9,20) and m!=naive and posterior==F(9,13), (m,naive,posterior))
                witness={'exact_common_mass':str(m),'naive_unconditional_product':str(naive),
                         'weighted_common_first_c0_probability':str(posterior),
                         'unweighted_auxiliary_first_c0_probability':'1/2',
                         'exact_total_variation':str(1-m),'equal_prior_error':str(m/2)}
    # A bounded random-hazard limit is a Laplace transform, not exp(-mean).
    # Finite two-branch product benchmark; this is an extension, not a refutation.
    for n in (3,5,10,30):
        mixture=((1-F(1,n))**n+(1-F(2,n))**n)/2
        wrong=(1-F(3,2*n))**n
        check('negative_control',f'random_hazard/{n}',mixture>wrong,(mixture,wrong))
    return witness

def scalar() -> None:
    for lam in (F(1,4),F(1,2),F(3,4)):
        for a in (F(-1,5),F(0),F(1,5)):
            for u in (F(-1,7),F(1,7)):
                x,derivative=u,F(1)
                for n in range(9):
                    power=lam**n
                    explicit=power*u/(1+a*(1-power)*u)
                    B=lambda y:1/(1+a*y)**2
                    error=a*power*u*u/((1+a*(1-power)*u)*(1+a*u))
                    check('scalar',f'{lam}/{a}/{u}/{n}',x==explicit
                          and derivative/power*B(x)==B(u)
                          and x/power-u/(1+a*u)==error,(x,derivative))
                    derivative*=lam/(1+a*(1-lam)*x)**2
                    x=lam*x/(1+a*(1-lam)*x)
    for lam in (F(1,4),F(1,2),F(3,4)):
        x,u=F(1,7),F(1,7)
        da,dl,mixed=F(0),F(0),F(0)
        for n in range(1,11):
            mixed_new=da+lam*mixed-(1-2*lam)*x*x-2*lam*(1-lam)*x*dl
            da_new=lam*da-lam*(1-lam)*x*x
            dl_new=x+lam*dl
            x,da,dl,mixed=lam*x,da_new,dl_new,mixed_new
            normalized=mixed/lam**n-F(n)*da/lam**(n+1)
            check('mixed_margin',f'{lam}/{n}',normalized==n*lam**(n-1)*u*u,normalized)

def geometry() -> None:
    for q in (F(1,5),F(1,2),F(4,5)):
        coth=lambda n:(1+q**(2*n))/(1-q**(2*n))
        csch=lambda n:2*q**n/(1-q**(2*n))
        tanh=lambda n:(1-q**(2*n))/(1+q**(2*n))
        for m in range(2,9):
            E=q**(4*(m-1))/(1-q**(4*(m-1)))-q**(4*m)/(1-q**(4*m))
            O=(csch(2*(m-1))-csch(2*m))/2
            P,Q=coth(2*m)+2*m*E,csch(2*m)+2*m*O
            minus=m*tanh(m-1)-(m-1)*tanh(m)
            check('contact_block',f'{q}/{m}',P-Q==minus and minus>0 and P+Q>0,minus)
    for g,c0,c1 in ((F(1),F(2),F(2)),(F(3,2),F(7,4),F(5,2))):
        for cb,co in ((c0,c1),(c1,c0)):
            z=cb*co-1
            diagonal=(cb-1/(2*co))/g
            off=-1/(2*co*g)
            det=diagonal**2-off**2
            nu=diagonal/det
            nw=(diagonal-off)/(2*co**2*det)
            Lb,Lo=g/(2*cb*z),g/(2*co*z)
            check('schur',f'{g}/{cb}/{co}',nu==Lb*(1+2*z) and nw==Lo,(nu,nw))
            for m in range(2,8):
                k=F(4,2**m*(m+1)*factorial(m)**2)
                action=-k*nw**m
                weighted=F(2*comb(2*m-2,m-1),2**(m-1)*m*(m+1))*nw**(m-1)
                twist=-g/co*weighted/factorial(2*m-2)
                check('two_flight',f'{g}/{cb}/{co}/{m}',action+twist==-k*Lo**m*(1+2*m*z)
                      and (1+2*z)**m-(1+2*m*z)>0,(action,twist))
    check('two_flight','quartic_equal_curvature',F(49-13,1728)==F(1,48),F(1,48))

def profiles() -> None:
    degree=7
    rising=[F(1)]
    for n in range(1,degree+1):
        rising.append(rising[-1]*F(2*n-1,2))
    for seed in range(4):
        v=[F(1)]+[F((-1)**(n+seed)*(seed+1),n+3) for n in range(1,degree+1)]
        beta=[sum((rising[r]*rising[n-r]*v[r]*v[n-r] for r in range(n+1)),F(0))*F(2,factorial(n+2)) for n in range(degree+1)]
        recovered=[F(1)]
        for n in range(1,degree+1):
            moment=beta[n]*F(factorial(n+2),2)
            recovered.append((moment-sum((recovered[r]*recovered[n-r] for r in range(1,n)),F(0)))/2)
        check('profile_jets',str(seed),all(recovered[n]/rising[n]==v[n] for n in range(degree+1)),tuple(beta))

def main() -> None:
    stopped_kernels()
    witness=overlap()
    scalar()
    geometry()
    profiles()
    output={'reviewed_commit':'bd27ed3208cc869f6c7a6547453a2557bfcd03ed',
            'status':'passed','arithmetic':'exact fractions; standard library only',
            'checks':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),
            'case_digest_sha256':DIGEST.hexdigest(),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'adaptive_witness':witness,
            'scope':'Finite identities and finite discrete experiments; not a billiard simulation, full manuscript build, or proof certificate.'}
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
