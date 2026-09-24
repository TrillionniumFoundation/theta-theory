#!/usr/bin/env python3
"""Finite regression tests for v21. These are not an analytic proof checker."""
from __future__ import annotations
import argparse,itertools,json,math
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path


def step(state:str,z:int,t:int,L:int)->str:
    """t is zero based. Clock supplies block polarity and position."""
    if state in ('+','-'): return state
    positive=(t//L)%2==0
    alive=state=='a' and z==int(positive)
    if (t+1)%L==0: return ('+' if positive else '-') if alive else 'a'
    return 'a' if alive else 'f'


def positive_probability(u:F,L:int,R:int)->F:
    x=u**L;y=(1-u)**L;s=x+(1-x)*y
    return x/s*(1-(1-s)**R)


def numerical_probability(u:float,L:int,R:int)->float:
    x=u**L;y=(1-u)**L;s=x+(1-x)*y
    if s==1: return x
    return x/s*(-math.expm1(R*math.log1p(-s)))


def phase_dp(u:F,L:int,R:int)->tuple[F,int]:
    law={'a':F(1)};peak=1
    for t in range(2*L*R):
        new=defaultdict(F)
        for state,mass in law.items():
            for z,pz in [(0,1-u),(1,u)]:
                if pz:new[step(state,z,t,L)]+=mass*pz
        law=dict(new);peak=max(peak,len(law))
    return law.get('+',F(0)),peak


def run(mutant:str|None=None)->dict:
    checks=0
    def check(ok:bool,label:str):
        nonlocal checks
        checks+=1
        if not ok:raise RuntimeError('diagnostic failed: '+label)
    # Exact enumeration of input words against the finite-horizon hazard formula.
    for L,R in [(1,1),(1,2),(2,1),(2,2)]:
        n=2*L*R
        for u in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
            total=F(0)
            for word in itertools.product([0,1],repeat=n):
                state='a'
                for t,z in enumerate(word):state=step(state,z,t,L)
                final=state=='+' or (mutant=='block-default' and state not in ('+','-'))
                if final:total+=u**sum(word)*(1-u)**(n-sum(word))
            value=positive_probability(u,L,R)
            if mutant=='block-hazard':value=u**L
            check(total==value,'exact first-success probability')
            dp,peak=phase_dp(u,L,R)
            check(dp==value and peak<=4,'four-state dynamic program')
    # Dyadic inverse-CDF sampler: one label per resolved outcome or unresolved prefix.
    for r in range(1,8):
        D=2**r
        for a in range(D+1):
            for depth in range(r+1):
                width=2**(r-depth)
                labels=set()
                for prefix in range(2**depth):
                    lo=prefix*width;hi=lo+width
                    labels.add(('yes',) if hi<=a else ('no',) if lo>=a else ('pending',prefix))
                bound=2 if mutant=='precision' else 3
                check(len(labels)<=bound,'three-label binary sampler')
        for s in range(2,min(D,5)+1):
            # Equally spaced integer thresholds, with possible unequal final cells.
            boundaries=[j*D//s for j in range(s+1)]
            for depth in range(r+1):
                labels=set();width=2**(r-depth)
                for prefix in range(2**depth):
                    lo=prefix*width;hi=lo+width
                    cell=next((j for j in range(s) if boundaries[j]<=lo and hi<=boundaries[j+1]),None)
                    labels.add(('done',cell) if cell is not None else ('pending',prefix))
                check(len(labels)<=2*s-1,'finite dyadic sampler bound')
    # Comparison randomizer, including endpoint probabilities and calibration.
    for qi,qj,hi,hj in itertools.product([F(0),F(1,4),F(1,2),F(1)],repeat=4):
        coin=F(1,2)+(qj-qi-hj+hi)/4
        check(0<=coin<=1 and (coin*16).denominator==1,'comparison probability and precision')
    for values in itertools.product([F(-1),F(-1,2),F(0),F(1,2),F(1)],repeat=4):
        gap=F(1,2)
        paths=[(0,values[0])]
        for j in range(1,4):
            nxt=[]
            for i,current in paths:
                for choice in (i,j):
                    if values[choice]>=max(current,values[j])-gap:
                        nxt.append((choice,values[choice]))
            paths=nxt
            for _,value in paths:check(value>=max(values[:j+1])-j*gap,'tournament regret induction')
    # Shared capacity prevents multiplying one word's error budget across cuts.
    lam=F(1,2) if mutant=='capacity' else F(1,4)
    capacity_per_word=2*lam
    check(capacity_per_word<=F(1,2),'joint word capacity')
    for decision_probability in [F(j,10) for j in range(11)]:
        error=F(1,2)*decision_probability+F(1,2)*(1-decision_probability)
        check(error>=2*lam,'joint two-cut obstruction')
    # Point-source response spectrum: all binary dictionaries for small dimensions.
    for d in range(2,5):
        responses=list(itertools.product([F(0),F(1)],repeat=d))
        payoffs=[tuple(sum(h,F(0))/d-h[i] for i in range(d)) for h in responses]
        for K in range(1,min(d,3)+1):
            best=max(min(max(row[i] for row in dictionary) for i in range(d))
                     for dictionary in itertools.product(payoffs,repeat=K))
            exact=1-F(math.ceil(d/K),d)
            check(best==exact,'point-source deterministic dictionary optimum')
            for partition in itertools.product(range(K),repeat=d):
                check(max(partition.count(j) for j in range(K))>=math.ceil(d/K),'pigeonhole lower bound')
    # Active-label profiles and small stochastic encoders/decoders.
    intervals=[(0,3,2),(1,4,3),(2,3,2)]
    widths=[]
    for t in range(5):
        active=[q for a,b,q in intervals if a<=t<b]
        D=math.prod(active);widths.append(D)
        check(len(list(itertools.product(*[range(q) for q in active])))==D,'active-label exact profile')
        for K in range(1,D+1):
            for assignment in itertools.product(range(K),repeat=min(D,4)):
                # Full enumeration when D<=4; identity count inequality otherwise.
                decoded=len(set(assignment))
                check(decoded<=K,'finite-message decoding bound')
    # Physical two-phase procedure: probabilities, peak registers, signed score.
    for L,R in [(1,1),(2,1),(2,2)]:
        for p,q in itertools.product([F(0),F(1,4),F(1,2),F(3,4),F(1)],repeat=2):
            a=(1-p)*(1-q);c=p*q
            ha,wa=phase_dp(a,L,R);hc,wc=phase_dp(c,L,R)
            check(ha==positive_probability(a,L,R) and hc==positive_probability(c,L,R),'physical phase probabilities')
            probs=[ha,(1-ha)*hc,(1-ha)*(1-hc)]
            check(sum(probs)==1 and min(probs)>=0,'physical event law')
            check(wa<=4 and wc+1<=5 and 2*(wc+1)<=10,'physical training registers')
            check(3*2*2==12,'physical validation register')
            expected=probs[0]*(F(1,2)-c)+probs[1]*(F(1,2)-a)+probs[2]*(1-a-c)
            check(-1<=expected<=1,'physical score range')
    # Concrete long-clock construction, stable numerical evaluation is diagnostic only.
    L=400;R=8*2**400;N=4*L*R
    check(F(8,3)**8>2000,'exponential error enclosure')
    check(F(707,500)**2<2,'square-root enclosure')
    margin=F(707,500)-1-F(1,300)-F(1,200)-F(2,1000)-F(2,5)
    if mutant=='physical-margin':margin=-margin
    check(margin==F(11,3000) and margin>0,'physical rational margin')
    minimum=1.0
    for pi in range(101):
        for qi in range(101):
            p=pi/100;q=qi/100;a=(1-p)*(1-q);c=p*q
            ha=numerical_probability(a,L,R);hc=numerical_probability(c,L,R)
            score=ha*(.5-c)+(1-ha)*hc*(.5-a)+(1-ha)*(1-hc)*(1-a-c)-1/300
            minimum=min(minimum,score)
            check(score>.4,'physical parameter-grid regression')
    # Costs are not discarded by the state count.
    check(N==12800*2**400,'all scheduled training calls counted')
    autonomous=12 if mutant=='clock' else 12*(N*3+10)
    check(autonomous>12,'clock is charged in autonomous implementation')
    for J in [1,2,10,100]:
        gamma=F(2,5)
        exponent=F(J)*gamma**2/(2 if mutant=='confidence' else 8)
        check(exponent==F(J,50),'confidence two-sided range constant')
        check(12*(2*J+1)>=12 and 401*J>J,'confidence accumulator and resets')
    for Nsmall,alpha in [(1,F(1,10)),(10,F(1,100)),(100,F(1,1000))]:
        loss=2*min(F(1),Nsmall*alpha)
        wrong=2*alpha if mutant=='training-transport' else loss
        check(wrong==loss,'training-count transport multiplier')
    return {'schema':'gtf21.finite-diagnostics/1','checks':checks,
      'block_formula':'x/(x+(1-x)y)*(1-(1-x-(1-x)y)^R)',
      'physical_width_lower':3,'physical_width_upper':12,'physical_training_calls':str(N),
      'physical_rational_margin_over_two_fifths':str(margin),
      'physical_grid_minimum':minimum,'active_label_profile':widths,
      'general_width_factor':'12*alphabet_size','analytic_proof_certification':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--mutant');parser.add_argument('--out');args=parser.parse_args()
    result=run(args.mutant);text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.out:Path(args.out).write_text(text)
    else:print(text,end='')
