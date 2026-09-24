#!/usr/bin/env python3
"""Finite diagnostics for the v20 formulas; not an analytic proof checker."""
from __future__ import annotations
import argparse,itertools,json,math
from fractions import Fraction as F
from pathlib import Path


def key(n:int,t:int,u:int,v:int):
    h=(n+1)//2;r=n-t
    if u>=h:return ('L',)
    if v>=h:return ('R',)
    return ('P',min(h-u,r+1),min(h-v,r+1))


def profile(n:int,t:int)->int:
    h=(n+1)//2
    return math.comb(t+2,2) if t<h else math.comb(n-t+3,2)


def run(mutant:str|None=None)->dict:
    checks=0
    def check(ok:bool,label:str):
        nonlocal checks
        checks+=1
        if not ok:raise RuntimeError('diagnostic failed: '+label)
    # Exact cube-vertex checks for all three response inequalities.
    for x,y,z,t in itertools.product([F(0),F(1)],repeat=4):
        f0=(-3*x-5*y+3*z+5*t)/16
        f1=(5*x+3*y-5*z-3*t)/16
        fc=(3*x+y+z+3*t)/16
        cap=F(2,3) if mutant=='triangle' else F(3,4)
        check(f0+f1<=F(1,4),'endpoint inequality')
        check(f0+fc<=cap and f1+fc<=F(3,4),'center inequalities')
    # Exact rational candidate grid checks, used only as diagnostics.
    h0=[F(2,3),F(0),F(1),F(1)]
    if mutant=='response':h0[0]=F(1)
    Q=[F(5,16),F(3,16),F(3,16),F(5,16)]
    check(sum(x*y for x,y in zip(h0,Q))==F(17,24),'response target mean')
    for pi in range(41):
        for qi in range(41):
            p=F(pi,40);q=F(qi,40);a=(1-p)*(1-q);c=p*q
            check(min(a,c)<=F(1,4),'small coordinate')
            check((a+3*c<=1) if a>=c else (c+3*a<=1),'linear envelope')
            check(max(F(17,24)-a/3-c,F(17,24)-a-c/3)>=F(3,8),'two response lower')
    # Exhaust the actual finite word functions, not just their formulas.
    for n in [1,3,5,7,9]:
        h=(n+1)//2
        words=list(itertools.product(range(3),repeat=n))
        outputs=[]
        for w in words:
            u=w.count(0);v=w.count(1)
            out='L' if u>=h else 'R' if v>=h else 'D'
            if mutant=='labels':out='R' if out=='L' else out
            outputs.append(out)
        for cut in range(n+1):
            by_prefix={}
            for w,out in zip(words,outputs):
                by_prefix.setdefault(w[:cut],[]).append(out)
            residuals={tuple(v) for v in by_prefix.values()}
            claimed=profile(n,cut)+(1 if mutant=='profile' else 0)
            check(len(residuals)==claimed,'enumerated residual count')
            key_to_response={}
            response_to_key={}
            for prefix,values in by_prefix.items():
                k=key(n,cut,prefix.count(0),prefix.count(1));v=tuple(values)
                check(k not in key_to_response or key_to_response[k]==v,'key determines response')
                check(v not in response_to_key or response_to_key[v]==k,'response determines key')
                key_to_response[k]=v;response_to_key[v]=k
    # Real n=399 checkpoint key enumeration, with all 400 profile entries.
    ns=399
    prof=[profile(ns,t) for t in range(ns+1)]
    for cut in [0,1,198,199,200,201,398,399]:
        keys={key(ns,cut,u,v) for u in range(cut+1) for v in range(cut-u+1)}
        check(len(keys)==prof[cut],'399 exact checkpoint enumeration')
    check(max(prof)==20301 and prof.index(max(prof))==200,'peak width')
    check(prof[-1]==3 and 2*max(prof)==40602 and 40602<2**16,'complete register bound')
    # Selected quotient transitions checked against multiple representatives.
    for n in [3,7,15]:
        for cut in range(n):
            trans={}
            for u in range(cut+1):
                for v in range(cut-u+1):
                    k=key(n,cut,u,v)
                    nxt=tuple(key(n,cut+1,u+(s==0),v+(s==1)) for s in range(3))
                    check(k not in trans or trans[k]==nxt,'compatible quotient shift')
                    trans[k]=nxt
    # Exact positive rational physical margin, without decimal thresholds.
    check(F(707,500)**2<2 and 28**2<798,'square root enclosures')
    margin=F(207,500)-F(1,112)-F(1,300)-F(2,5)-F(1,2**51)
    if mutant=='margin':margin=-margin
    check(margin>0,'strict physical margin')
    check(F(3,8)+F(1,300)<F(2,5),'two-state physical upper')
    # Old threshold map before and after clipping, all n=400 count pairs.
    def mask(u,v):return (u<250,u<150,v<150,v<250)
    for u in range(401):
        for v in range(401-u):
            clip=249 if mutant=='clip' else 250
            check(mask(u,v)==mask(min(u,clip),min(v,clip)),'old clipping invariance')
    # Nonuniform two-word equality in the weighted bound.
    for p in [F(1,10),F(1,3),F(1,2),F(4,5)]:
        lam=min(p,1-p)
        for a in [F(i,10) for i in range(11)]:
            check(p*a+(1-p)*(1-a)>=lam,'one-state weighted optimum')
    return {'schema':'gtf20.finite-diagnostics/1','checks':checks,
      'peak_training_width':max(prof),'peak_cut':prof.index(max(prof)),
      'profile':prof,'complete_state_upper':40602,'training_informative':399,
      'training_scheduled':400,'total_scheduled_trials':402,
      'rational_score_margin_over_two_fifths':str(margin),
      'analytic_score_lower_decimal':math.sqrt(2)-1-1/(4*math.sqrt(399*math.e))-math.exp(-399/8)/4-1/300,
      'analytic_proof_certification':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--mutant');parser.add_argument('--out');args=parser.parse_args()
    result=run(args.mutant);text=json.dumps(result,indent=2,sort_keys=True)
    if args.out:Path(args.out).write_text(text+'\n')
    else:print(text)
