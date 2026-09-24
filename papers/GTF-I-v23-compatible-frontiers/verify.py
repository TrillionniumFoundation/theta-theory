#!/usr/bin/env python3
"""Finite exact and numerical diagnostics, not an analytic proof checker."""
from __future__ import annotations
import argparse,itertools,json,math
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path


def step(s:int,z:int,m:int,mutant:str|None=None)->int:
    if abs(s)==m and mutant!='walk-absorption':return s
    return s+2*z-1


def walk_law(u:F,m:int,n:int,mutant:str|None=None):
    law={0:F(1)};active=F(0)
    for _ in range(n):
        active+=sum(p for s,p in law.items() if abs(s)<m)
        nxt=defaultdict(F)
        for s,p in law.items():
            for z,pz in [(0,1-u),(1,u)]:
                nxt[step(s,z,m,mutant)]+=p*pz
        law=dict(nxt)
    return law,active


def frontier(prior:tuple[F,...],qs:tuple[F,...],ks:tuple[int,...],mutant:str|None=None)->F:
    M=len(prior);ordered=sorted(prior,reverse=True)
    if mutant=='revelation-prior':ordered=[F(1,M)]*M
    a=math.prod(1-q for q in qs);value=a*ordered[0]
    for t,q in enumerate(qs):
        k=min(M,ks[t]) if mutant=='revelation-bottleneck' else min(M,*ks[t:])
        value+=q*math.prod(1-x for x in qs[t+1:])*sum(ordered[:k])
    return value


def exact_best(prior:tuple[F,...],qs:tuple[F,...],ks:tuple[int,...])->tuple[F,int]:
    """Enumerate every deterministic transition table, then optimize decoder.
    Deduplicate only identical parameter--state joint laws. No frontier formula.
    """
    M=len(prior);states={tuple((p,) for p in prior)};oldK=1;tables=0
    for q,K in zip(qs,ks):
        newstates=set()
        for table in itertools.product(range(K),repeat=oldK*(M+1)):
            for law in states:
                tables+=1
                out=[[F(0) for _ in range(K)] for _ in range(M)]
                for theta in range(M):
                    for old in range(oldK):
                        mass=law[theta][old]
                        out[theta][table[old*(M+1)]]+=mass*(1-q)
                        out[theta][table[old*(M+1)+theta+1]]+=mass*q
                newstates.add(tuple(tuple(row) for row in out))
        states=newstates;oldK=K
    return max(sum(max(law[t][s] for t in range(M)) for s in range(oldK)) for law in states),tables


def run(mutant:str|None=None)->dict:
    checks=0;enum_tables=0
    def check(ok:bool,label:str):
        nonlocal checks
        checks+=1
        if not ok:raise RuntimeError('diagnostic failed: '+label)
    # Word enumeration independently checks absorbing transitions and probabilities.
    for m in range(1,5):
        for n in range(1,9):
            for u in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
                law,active=walk_law(u,m,n,mutant)
                ref=defaultdict(F);refactive=F(0)
                for word in itertools.product([0,1],repeat=n):
                    prob=u**sum(word)*(1-u)**(n-sum(word));s=0;a=0
                    for z in word:
                        if -m<s<m:s+=2*z-1;a+=1
                    ref[s]+=prob;refactive+=a*prob
                check(law==dict(ref),'word law and absorbing transitions')
                check(active==refactive and active<=min(n,m*m),'active-time bound')
                check(all(abs(s)<=m for s in law),'walk state interval')
                if u!=F(1,2):
                    theta=abs(float(u)-.5)
                    error=sum(p for s,p in law.items() if (s<0 if u>F(1,2) else s>=0))
                    check(float(error)<=math.exp(-4*theta*m)+math.exp(-2*n*theta*theta)+1e-14,'finite-horizon error bound')
    # Difference equations provide an independent check of the mean absorption formula.
    for m in range(1,15):
        for u in [F(1,4),F(1,2),F(3,4)]:
            if u==F(1,2):
                times={s:F(m*m-s*s) for s in range(-m,m+1)}
            else:
                r=(1-u)/u;x=2*u-1
                times={s:((2*m)*(1-r**(s+m))/(1-r**(2*m))-(s+m))/x for s in range(-m,m+1)}
            for s in range(-m+1,m):
                check(times[s]==1+u*times[s+1]+(1-u)*times[s-1],'absorption difference equation')
            declared=F(m) if mutant=='walk-time' and u==F(1,2) else times[0]
            x=float(2*u-1)
            closed=m*m if x==0 else m*math.tanh(m*math.atanh(x))/x
            check(abs(float(declared)-closed)<1e-10,'mean absorption closed form')
    # Exhaustive Bayesian optimization, with terminal decoder optimized independently.
    configurations=[
      ((F(1,2),F(1,2)),(F(1,2),F(1,2)),(2,1)),
      ((F(1,2),F(1,2)),(F(1,2),F(1,2)),(1,2)),
      ((F(1,2),F(1,2)),(F(1,3),F(2,3),F(1,2)),(2,1,2)),
      ((F(1,3),)*3,(F(1,2),F(1,2)),(2,2)),
      ((F(1,2),F(1,3),F(1,6)),(F(1,3),F(2,3)),(2,2)),
      ((F(1,2),F(1,3),F(1,6)),(F(1,2),F(1,2),F(1,2)),(2,1,2)),
      ((F(1,2),F(1,3),F(1,6)),(F(0),F(1)),(1,2))]
    exact_results=[]
    for prior,qs,ks in configurations:
        optimum,tables=exact_best(prior,qs,ks);enum_tables+=tables
        predicted=frontier(prior,qs,ks,mutant)
        check(optimum==predicted,'all deterministic tables versus exact Bayesian frontier')
        exact_results.append({'M':len(prior),'profile':ks,'value':str(optimum),'tables_evaluated':tables})
    # Constructing the nested machine and conditioning on every reveal pattern.
    for M in range(2,6):
        prior=tuple(F(M-j,sum(range(1,M+1))) for j in range(M));qs=(F(1,4),F(1,2),F(3,4))
        for ks in itertools.product(range(1,M+1),repeat=3):
            k=[min(M,*ks[t:]) for t in range(3)];success=F(0)
            for pattern in itertools.product([0,1],repeat=3):
                probability=math.prod(q if e else 1-q for e,q in zip(pattern,qs))
                for theta in range(1,M+1):
                    state=1
                    for t,e in enumerate(pattern):
                        if e:state=theta if theta<=k[t] else 1
                        check(1<=state<=ks[t],'nested machine respects every cut')
                    if state==theta:success+=prior[theta-1]*probability
            check(success==frontier(prior,qs,ks),'exact nested attainment with actual prior weights')
    check(frontier((F(1,4),)*4,(F(1,2),)*3,(4,1,4))==F(5,8),'single early bottleneck example')
    check(frontier((F(1,4),)*4,(F(1,2),)*3,(4,4,4))==F(29,32),'unconstrained-history comparison')
    for M in range(2,8):
        for n in range(1,7):
            a=F(1,2)**n
            for j in range(1,11):
                s=F(1,M)+(1-F(1,M))*F(j,10)
                ratio=(M*s-a)/(1-a)
                K=math.floor(ratio) if mutant=='frontier-rounding' else math.ceil(ratio)
                if K<=M:
                    check((a+K*(1-a))/M>=s,'inverse width is sufficient')
                    if K>1:check((a+(K-1)*(1-a))/M<s,'inverse width is minimal')
    # Independent Markov-product sensitivity with absorption.
    for m in [1,2,3]:
        for n in [2,3,4,7,10]:
            for p,q in [(F(1,4),F(1,3)),(F(1,3),F(1,2)),(F(1,2),F(3,4))]:
                lp,active=walk_law(p,m,n);lq,_=walk_law(q,m,n)
                tv=sum(abs(lp.get(s,0)-lq.get(s,0)) for s in range(-m,m+1))/2
                budget=abs(p-q)*(1 if mutant=='active-budget' else active)
                check(tv<=min(1,budget),'occupation-weighted retained-law transfer')
    # Coin centering, horizon parameters, rational physical margin, and complete widths.
    for g in [F(1,8),F(3,8),F(1,2),F(1)]:
        for D in [-1,0,1]:
            coin=F(1,2)+(D-g/2)/4
            check(0<=coin<=1 and coin.denominator&(coin.denominator-1)==0,'dyadic confidence coin')
        theta=g/(4 if mutant=='confidence-gap' else 8)
        check(F(1,2)+(0-g/2)/4==F(1,2)-theta,'null confidence gap')
        check(F(1,2)+(g-g/2)/4==F(1,2)+theta,'alternative confidence gap')
    m,n=400,160000;theta=F(1,200)
    check(4*theta*m==2*n*theta*theta==8,'physical exponent equality')
    check(F(8,3)**8>2000 and F(707,500)**2<2,'rational physical enclosures')
    margin=F(707,500)-1-F(1,300)-theta-F(2,1000)-F(2,5)
    check(margin==F(11,3000)>0,'strict physical score margin')
    width=2*m+2 if mutant=='physical-buffer' else 4*m+4
    check(width>=2*(2*m+2) and width==1604,'first-bit physical state product')
    check(2*n==320000,'both fixed training phases counted')
    for K,d in itertools.product(range(1,5),range(1,6)):
        peak=3*d*K*(2*m+1)
        check(peak>=max(K*(2*m+1),K*(2*d+1),2*K*(d+1)),'general full-cut storage bound')
    return {'schema':'gtf22.finite-diagnostics/1','checks':checks,
      'exhaustive_transition_tables_evaluated':enum_tables,'exact_Bayes_examples':exact_results,
      'physical_training_trials':320000,'physical_peak_upper':1604,
      'physical_margin_rational_lower':str(margin),'analytic_proof_certification':False,
      'scope':'finite independent regression examples; proofs remain subject to external mathematical review'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--mutant');parser.add_argument('--out');args=parser.parse_args()
    result=run(args.mutant);text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.out:Path(args.out).write_text(text)
    else:print(text,end='')
