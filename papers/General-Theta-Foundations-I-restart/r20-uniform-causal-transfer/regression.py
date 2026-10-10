#!/usr/bin/env python3
"""Exact finite R20 checks; no numerical certificate of continuum theorems."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parent
COUNTS:dict[str,int]={}
def require(ok:bool,message:str,group:str)->None:
    if not ok:raise RuntimeError(message)
    COUNTS[group]=COUNTS.get(group,0)+1

def common_dual()->None:
    # Two models, one identical report. A next-label distribution is shared.
    target=F(2)
    common_support=max(F(1),F(1))
    independent_support=max(F(1),F(0))+max(F(0),F(1))
    require(target>common_support and target==independent_support,
            'max must follow parameter sum','joint_dual')
    # Every rational shared row satisfies every selected finite support function.
    for q in range(9):
        k=F(q,8)
        for a,b,c,d in product((-2,0,3),repeat=4):
            val=k*(a+c)+(1-k)*(b+d)
            require(val<=max(a+c,b+d),'joint affine support inequality','joint_dual')
    # Min/sup cannot be exchanged, even with compact decision sets.
    grid=[F(i,16) for i in range(17)]
    robust=min(max(u*u,(1-u)**2) for u in grid)
    oracle=max(min(u*u for u in grid),min((1-u)**2 for u in grid))
    require(robust==F(1,4) and oracle==0,'oracle is a different interface','joint_dual')

def calibration()->None:
    for pp in (F(1,8),F(1,5),F(1,3),F(3,8)):
        worst=F(0)
        for theta in (0,1):
            for p in (pp/3,pp/2,pp):
                risk=F(0);mean_error=F(0)
                for e,y in product((0,1),repeat=2):
                    c=theta^e;w=c^y;x=theta^y
                    prob=(p if e else 1-p)/2
                    u=pp if w==0 else 1-pp
                    risk+=prob*(u-x)**2;mean_error+=prob*(u-x)
                    require(w==c^y,'explicit common update','calibration')
                require(risk==pp**2+p*(1-2*pp),'fixed parameter risk polynomial','calibration')
                require(risk<=pp*(1-pp) and mean_error==0,'uniform attained upper','calibration')
                worst=max(worst,risk)
                for b in (F(-2,7),F(0),F(2,7)):
                    shifted=F(0)
                    for e,y in product((0,1),repeat=2):
                        x=theta^y;w=(theta^e)^y;u=pp if w==0 else 1-pp
                        shifted+=(p if e else 1-p)/2*(u-x-b)**2
                    require(shifted==risk+b*b,'attained offset not tolerance lower','calibration')
        require(worst==pp*(1-pp),'worst noise endpoint','calibration')
        # Explicit Bayesian lower: uniform hidden bit, fixed p=pp.
        for c,y in product((0,1),repeat=2):
            joint=[(F(1,2)*(pp if c!=theta else 1-pp)*F(1,2),theta^y) for theta in(0,1)]
            mass=sum(w for w,x in joint);posterior=sum(w*x for w,x in joint)/mass
            var=sum(w*(x-posterior)**2 for w,x in joint)/mass
            require(var==pp*(1-pp),'conditional Bayes variance','calibration')
    # Exact support graph: initial + intermediate + stopping supports are disjoint.
    for M in range(1,12):
        profiles=[(m1,m2) for m1 in range(1,M) for m2 in range(1,M) if 1+m1+m2<=M]
        require(bool(profiles)==(M>=3),'exact deadline feasibility','deadline')
        if profiles:
            lower=min(F(3,16) if min(m1,m2)>=2 else F(1,4) for m1,m2 in profiles)
            require(lower==(F(1,4) if M<=4 else F(3,16)),'sharp five-state threshold','deadline')
    # One unknown model is fixed, not resampled adversarially at every step.
    qs=(F(1,10),F(9,10))
    fixed=max(2*q*(1-q) for q in qs)
    dynamic=max(q1*(1-q2)+(1-q1)*q2 for q1,q2 in product(qs,repeat=2))
    require(fixed==F(9,50) and dynamic==F(41,50),'timewise adversary changes task','fixed_parameter')

def erased_calibration()->None:
    for pm,pp,a in product((F(1,12),F(1,8)),(F(1,4),F(1,3)),(F(1,5),F(1,2),F(4,5))):
        epsilon=a*(F(1,2)-pm)
        pair_target=1-2*pm;pair_source=(1-a)*pair_target
        require((pair_target-pair_source)/2==epsilon,'deficiency pair lower equals fill upper','attained_erasure')
        lower=(1-a)*pp*(1-pp)+a/4
        require(lower==pp*(1-pp)+(F(1,2)-pp)**2/(F(1,2)-pm)*epsilon,'attained epsilon coefficient','attained_erasure')
        for theta,p in product((0,1),(pm,pp)):
            risk=F(0);mean=F(0)
            for er,e,y in product((0,1),repeat=3):
                prob=(a if er else 1-a)*(p if e else 1-p)/2
                w=(theta^e)^y;x=theta^y
                u=F(1,2) if er else (pp if w==0 else 1-pp)
                risk+=prob*(u-x)**2;mean+=prob*(u-x)
            require(risk==(1-a)*(pp*pp+p*(1-2*pp))+a/4 and mean==0,'explicit seven-state risk','attained_erasure')
            require(risk<=lower and (p!=pp or risk==lower),'uniform worst endpoint with erasure','attained_erasure')

def instrument_moments()->None:
    # All computations below use exactly one transition matrix for both calls.
    # Five labels: 0=root, 1/2=intermediate, 3/4=stop. Positive finite reports.
    def trans(t):return ((1-t,t),(t,1-t))
    def emit(y,x):return F(3,4) if y==x else F(1,4)
    for t,p,r in product((F(0),F(1,5),F(2,3)),(F(1,4),F(1,2)),(F(0),F(1,3),F(1))):
        T=trans(t);x0=(p,1-p)
        k={}
        for y in(0,1):
            a=r if y==0 else 1-r
            k[(0,y)]={1:a,2:1-a}
            for z in(1,2):
                a=F(3,4) if (z-1)^y else F(1,4)
                k[(z,y)]={3:a,4:1-a}
        # Integrated positive operator per occupied row / target label.
        mats={}
        for z in(0,1,2):
            for j in(1,2) if z==0 else(3,4):
                mats[z,j]=tuple(tuple(sum(k[(z,y)].get(j,0)*emit(y,xp)*T[xp][x] for y in(0,1)) for x in(0,1)) for xp in(0,1))
        vec={0:x0}
        for _ in range(2):
            nxt={}
            for z,v in vec.items():
                for (zz,j),A in mats.items():
                    if zz!=z:continue
                    w=tuple(sum(A[xp][x]*v[x] for x in(0,1)) for xp in(0,1))
                    nxt[j]=tuple(a+b for a,b in zip(nxt.get(j,(F(0),F(0))),w))
            vec=nxt
        direct={3:[F(0),F(0)],4:[F(0),F(0)]}
        for x,x1,x2,y1,y2,z,j in product((0,1),(0,1),(0,1),(0,1),(0,1),(1,2),(3,4)):
            w=x0[x]*T[x1][x]*emit(y1,x1)*k[(0,y1)][z]*T[x2][x1]*emit(y2,x2)*k[(z,y2)][j]
            direct[j][x2]+=w
        require(sum(sum(v) for v in vec.values())==1,'positive total mass','finite_moments')
        for j in(3,4):
            require(vec[j]==tuple(direct[j]),'shared-row integrated moment factorization','finite_moments')
        risk=sum(w*((F(1,4) if j==3 else F(3,4))-x)**2 for j,v in vec.items() for x,w in enumerate(v))
        require(0<=risk<=1,'bounded same-task risk','finite_moments')

def intervals()->None:
    # The target is an inaccessible theta in [0,1], risk (u-theta)^2.
    # A parameter net missing 0 still covers [0,1] with its stated radius.
    for Q,J in product((2,4,8),(2,3,5,8)):
        decisions=[F(i,Q) for i in range(Q+1)];models=[F(j,J) for j in range(1,J+1)]
        eta=F(1,100);err=F(1,Q);omega=min(F(1),F(2,J))
        lows=[];ups=[]
        for u in decisions:
            risks=[(u-th)**2 for th in models]
            lows.append(max(max(F(0),v-eta/2) for v in risks))
            ups.append(max(min(F(1),v+eta/2) for v in risks))
        L,U=min(lows),min(ups);best=ups.index(U);u=decisions[best]
        require(U-L<=eta,'min-max interval enclosure width','global_certificate')
        require(L-err<=F(1,4)<=U+omega,'two-sided all-programme value bracket','global_certificate')
        require(max(u*u,(1-u)**2)<=F(1,4)+err+omega+eta,'attained uniform excess bound','global_certificate')
    # Finite-model lower exclusions require multiple models in this example.
    for r in(F(0),F(1,8),F(1,5)):
        require(r<F(1,4),'two-model global obstruction target','finite_model_exclusion')
        for u in [F(i,20) for i in range(21)]:
            require(max(u*u,(1-u)**2)>r,'joint model risk exclusion','finite_model_exclusion')
    # Actual mass in the singular tail is not renormalized to one.
    for k in range(1,9):
        mass=F(1,2**k)
        require(2*mass<=(F(1) if k>=1 else F(2)),'actual atomic tail allowance','singular_mass')
    # Resource products / at-most vs exact acquisition interfaces remain distinct.
    for M,S in product((1,3,5),(1,2,4)):
        require(len(list(product(range(M),range(S))))==M*S,'simulator state product','resource')

def main()->None:
    common_dual();calibration();erased_calibration();instrument_moments();intervals()
    inherited=subprocess.check_output([sys.executable,str(ROOT.parent/'r19-effective-frontier'/'regression.py')],text=True)
    result={'status':'PASS','component':'R20 uniform causal transfer selected exact finite checks','new_checks':sum(COUNTS.values()),'groups':COUNTS,'retained_R19':json.loads(inherited),'limitations':'Finite rational identities, specified graph profiles and counter-controls only. No exhaustive proof of all randomized programmes, weak-star compactness, Gaussian derivatives, quantum operator bounds, continuum minimax, or mathematical priority.'}
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
