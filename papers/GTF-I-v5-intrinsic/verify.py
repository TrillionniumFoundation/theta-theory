#!/usr/bin/env python3
"""Finite deterministic diagnostics for the fifth revision; not a proof checker."""
from __future__ import annotations
import argparse, heapq, itertools, json, math
from fractions import Fraction as Q
from functools import lru_cache

COUNT = 0

def require(ok: bool, message: str) -> None:
    global COUNT
    COUNT += 1
    if not ok:
        raise SystemExit('FAILED: ' + message)


def pf2(matrix: tuple[tuple[float, float], tuple[float, float]]) -> float:
    (a,b),(c,d)=matrix
    return (a+d+math.sqrt((a-d)**2+4*b*c))/2


def bisect_zero(fn) -> float:
    lo,hi=0.0,1.0
    require(fn(lo)>0 and fn(hi)<0,'pressure root bracket')
    for _ in range(80):
        mid=(lo+hi)/2
        if fn(mid)>0: lo=mid
        else: hi=mid
    return (lo+hi)/2


def markov_data(p: tuple[tuple[Q,Q],tuple[Q,Q]], r: tuple[Q,Q], q: Q):
    pi=(p[1][0]/(p[0][1]+p[1][0]),p[0][1]/(p[0][1]+p[1][0]))
    @lru_cache(None)
    def mass(w: tuple[int,...]) -> Q:
        if not w:return Q(1)
        ans=pi[w[0]]
        for i,j in zip(w,w[1:]):ans*=p[i][j]
        return ans
    @lru_cache(None)
    def radius(w: tuple[int,...]) -> Q:
        ans=Q(1)
        for i in w:ans*=r[i]
        return ans
    @lru_cache(None)
    def v(w: tuple[int,...]) -> Q:
        return sum(((1-q)*q**k*radius(w[k:])**2 for k in range(len(w))),q**len(w))
    @lru_cache(None)
    def energy(w: tuple[int,...]) -> Q:return mass(w)*v(w)
    return mass,radius,v,energy


def greedy(energy, n: int):
    heap=[(-energy(()),())]
    threshold=Q(1)
    while len(heap)<n:
        neg,w=heapq.heappop(heap);threshold=-neg
        for i in (0,1):
            child=w+(i,);heapq.heappush(heap,(-energy(child),child))
    return tuple(w for _,w in heap),threshold


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--mutant',choices=['drop-survival-pressure','forget-suffix-states',
        'replace-dependent-posterior','erase-critical-log','ordinary-matrix-power'])
    mutant=ap.parse_args().mutant
    P=((Q(4,5),Q(1,5)),(Q(7,20),Q(13,20)))
    r=(Q(1,5),Q(1,6))
    summaries=[]
    for q in (Q(1,25),Q(1,5),Q(1,2),Q(4,5)):
        mass,radius,v,energy=markov_data(P,r,q)
        words=[w for n in range(8) for w in itertools.product((0,1),repeat=n)]
        rho=q+(1-q)*max(r)**2
        for w in words:
            require(radius(w)**2<=v(w)<=1,'coordinate diameter bounded by orbit profile')
            children=[w+(i,) for i in (0,1)]
            require(sum(mass(c) for c in children)==mass(w),'cylinder partition mass')
            require(sum(energy(c) for c in children)<=rho*energy(w),'contracting total child energy')
            for i in (0,1):
                require(v(w+(i,))<=rho*v(w),'one-letter profile contraction')
                require(v(w+(i,))>=min(r)**2*v(w),'affine lower profile contraction')
            for k in range(len(w)+1):
                u,t=w[:k],w[k:]
                require(v(w)<=v(u)*v(t),'submultiplicative orbit diameter')
                require(energy(w)<=energy(t),'stationary suffix domination')
        require(sum(mass(w) for w in itertools.product((0,1),repeat=7))==1,'Markov word normalization')
        for n in (8,32,128,512):
            leaves,theta=greedy(energy,n)
            suffixes={w[k:] for w in leaves for k in range(len(w)+1)}
            require(sum(mass(w) for w in leaves)==1,'complete adaptive prefix code')
            require(len(leaves)==n,'greedy leaf budget')
            vertices={w[:k] for w in leaves for k in range(len(w)+1)}
            require(len(vertices)==2*n-1,'exact full-tree state count')
            require(suffixes<=vertices,'all leaf suffixes are existing greedy vertices')
            require(all(not w or w[1:] in vertices for w in vertices),'entire greedy tree is suffix closed')
            require(max(energy(w) for w in leaves)<=theta,'balanced upper threshold')
            for w in suffixes:
                require(w==() or w[1:] in suffixes,'closed deterministic suffix update')
                require(energy(w)>=min(energy(t) for t in leaves),'suffix threshold inherited')
            # A finite observed ratio, not a universal numerical bound asserted in the theorem.
            summaries.append({'q':str(q),'leaves':n,'distinct_suffixes':len(suffixes),
                'profile':float(sum(energy(w) for w in leaves)),'max_depth':max(map(len,leaves))})
            if mutant=='forget-suffix-states':
                require(all(w[1:] in set(leaves) for w in leaves),'mutant leaf-only code is not autonomous')
    # Exact homogeneous critical identity, and two different sides of the pressure balance.
    for base in (2,3,5):
        rr=Q(1,base+2);qc=rr**2
        sg=math.log(base)/(math.log(base)-2*math.log(float(rr)))
        for n in (2,5,13,29,73):
            profile=(1-qc)*sum(qc**k*rr**(2*(n-k)) for k in range(n))+qc**n
            expected=rr**(2*n)*(1+n*(1-qc))
            if mutant=='erase-critical-log':expected=rr**(2*n)
            require(profile==expected,'exact critical n factor')
        for q in (Q(1,100),Q(1,5),Q(4,5)):
            st=math.log(base)/(math.log(base)-math.log(float(q)))
            actual=(1-max(sg,st))/max(sg,st)
            if mutant=='drop-survival-pressure':actual=(1-sg)/sg
            target=min(-2*math.log(float(rr))/math.log(base),-math.log(float(q))/math.log(base))
            require(abs(actual-target)<1e-12,'spatial versus survival exponent')
    # Variable branch Markov matrix roots; powers are entrywise.
    def pres_g(s: float)->float:
        return math.log(pf2(tuple(tuple(float(P[i][j])**s*float(r[i])**(2*s)
                                      for j in (0,1)) for i in (0,1))))
    def pres_i(s: float)->float:
        return math.log(pf2(tuple(tuple(float(P[i][j])**s for j in (0,1)) for i in (0,1))))
    sg=bisect_zero(pres_g);qc=math.exp(-pres_i(sg)/sg)
    require(0<qc<1,'variable branch critical threshold')
    require(abs(pres_i(sg)+sg*math.log(qc))<1e-12,'two pressures meet at critical q')
    spectral_half=math.exp(pres_i(0.5))
    if mutant=='ordinary-matrix-power':spectral_half=1.0
    require(spectral_half>1.1,'Hadamard square-root matrix differs from stochastic matrix power')
    roots=[]
    for q in (qc/2,qc,min(0.9,2*qc),0.8):
        st=bisect_zero(lambda s:pres_i(s)+s*math.log(q))
        require((st<=sg+1e-11)==(q<=qc*(1+1e-11)),'pressure threshold direction')
        roots.append({'q':q,'s_g':sg,'s_t':st,'alpha':(1-max(sg,st))/max(sg,st)})
    # A finite prefix/suffix partition calculation checks the mixed-pressure expression.
    for q in (0.03,0.3,0.8):
        mass,_,v,_=markov_data(P,r,Q(str(q)))
        for s in (0.25,0.5,0.8):
            for n in (3,6,9):
                h=sum(float(mass(w)*v(w))**s for w in itertools.product((0,1),repeat=n))
                A=pres_g(s);B=pres_i(s)+s*math.log(q)
                convolution=sum(math.exp(k*B+(n-k)*A) for k in range(n+1))
                require(h>0 and h<=20*convolution,'finite mixed partition upper diagnostic')
                require(h>=0.01*max(math.exp(n*A),math.exp(n*B)),'finite mixed partition endpoint diagnostic')
    # Independent reference posterior is not the dependent full-history posterior.
    eta=Q(1,5);epsilon=Q(1,10)
    kernel=lambda x,u:(1-epsilon)*int(x==u)+epsilon/2
    obs=lambda x,y:(1-eta) if x==y else eta
    single_floor=eta*(1-eta)
    full_floor=Q(0)
    pair_means={}
    for y0,y1 in itertools.product((0,1),repeat=2):
        weights=[sum(Q(1,2)*obs(x0,y0)*kernel(x0,x1)*obs(x1,y1)
                     for x0 in (0,1)) for x1 in (0,1)]
        z=sum(weights);mean=weights[1]/z
        pair_means[str((y0,y1))]=str(mean)
        full_floor+=z*mean*(1-mean)
    require(full_floor<single_floor,'older data improve dependent Bayes risk')
    if mutant=='replace-dependent-posterior':
        require(full_floor==single_floor,'mutant identifies latest and full-history posteriors')
    for x,u in itertools.product((0,1),repeat=2):
        require(kernel(x,u)>=epsilon/2,'conditional minorization, not conditional equality')
    for u in (0,1):require(sum(Q(1,2)*kernel(x,u) for x in (0,1))==Q(1,2),'invariant hidden marginal')
    for eps in (Q(1,10),Q(1,2),Q(1)):
        Qeps=lambda x,u:(1-eps)*int(x==u)+eps/2
        risk=Q(0)
        for x0,x1,y1 in itertools.product((0,1),repeat=3):
            dec=(1-eta) if y1 else eta
            risk+=Q(1,2)*Qeps(x0,x1)*obs(x1,y1)*(x1-dec)**2
        require(risk==single_floor,'restarting observer expected-loss transfer')
    # Smooth family assumptions follow from explicit derivative intervals.
    for eps in (Q(0),Q(1,200),Q(1,100)):
        require(Q(1,5)-eps>Q(1,6)+eps,'unequal fixed-point inverse multiplier intervals')
        require(Q(1,6)-eps>0 and Q(1,5)+eps<1,'uniform nonlinear contraction')
        require(Q(3,4)-Q(1,5)>0,'strong separation of branch image intervals')
    print(json.dumps({'status':'passed','finite_checks':COUNT,'adaptive_code_diagnostics':summaries,
        'variable_markov_pressure':{'s_g':sg,'q_c':qc,'sample_roots':roots},
        'dependent_reference_floor':str(single_floor),'two_observation_bayes_floor':str(full_floor),
        'two_observation_posterior_means':pair_means,
        'scope':'Finite rational identities and deterministic regressions only; not validation of infinite-dimensional quantifiers or mathematical priority.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
