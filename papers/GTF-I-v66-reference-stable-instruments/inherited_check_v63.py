"""Finite regression only; no spectral or universal theorem is certified."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from copy import deepcopy
from math import isqrt
import json
import sympy as sp
from accuracy_profile import eta,log_interval,sqrt2_upper,certificate,verify

CHECKS=0
NEG=[]

def check(ok,label):
    global CHECKS
    CHECKS+=1
    if not ok:raise RuntimeError(label)

def negative(label,ok):
    check(ok,'negative control failed: '+label)
    NEG.append(label)

def reduced(word):
    out=[]
    for a in word:
        if out and out[-1]==-a:out.pop()
        else:out.append(a)
    return tuple(out)

def tests():
    # Exact free-word convolution identity, including the exceptional b=2 coefficient.
    for r in [2,3]:
        letters=tuple(range(1,r+1))+tuple(range(-r,0));q=2*r-1
        spheres=[{()}]
        for b in range(1,6):
            prev=spheres[-1]
            now={w+(a,) for w in prev for a in letters if not w or a!=-w[-1]}
            check(len(now)==(q+1)*q**(b-1),'sphere count')
            conv=Counter(reduced((a,)+w) for a in letters for w in prev)
            rhs=Counter({w:1 for w in now})
            if b==2:rhs[()]+=q+1
            elif b>=3:
                rhs.update({w:q for w in spheres[-2]})
            check(conv==rhs,'formal radial recurrence')
            for w in now:
                check(reduced(w)==w and len(w)==b,'no-backtrack word')
                check(tuple(-a for a in reversed(w)) in now,'inverse word distribution')
            spheres.append(now)
        bad=Counter({w:1 for w in spheres[2]});bad[()]=q
        correct=Counter(reduced((a,)+w) for a in letters for w in spheres[1])
        negative('length-two coefficient r='+str(r),bad!=correct)
        negative('iid is not nonbacktracking r='+str(r),(q+1)**3!=(q+1)*q**2)
    x=sp.Symbol('x')
    for q in [3,5,7,11]:
        ss=[sp.Integer(1),x,x*x-(q+1)]
        for b in range(3,13):ss.append(sp.expand(x*ss[-1]-q*ss[-2]))
        for b in range(1,13):
            rhs=q**(sp.Rational(b,2))*(sp.chebyshevu(b,x/(2*sp.sqrt(q)))-(sp.chebyshevu(b-2,x/(2*sp.sqrt(q)))/q if b>=2 else 0))
            check(sp.expand(rhs-ss[b])==0,'Chebyshev radial identity')
        for b in range(4,65):
            z=eta(b,q)
            check(0<z<=F(1,4),'eta range')
            check(eta(b+1,q)<z,'eta decreases')
            check(z>=F(1,q**b),'eta lower bound')
            check(2*z-z*z<1 and 2*z-z*z<=2*z,'log defect admissible')
    check(eta(4,3)==F(1,4),'non-strict boundary exactly attained')
    negative('strict-quarter false',not eta(4,3)<F(1,4))
    # Rational enclosure structure: nested intervals and product/inverse consistency.
    for a in range(1,18):
        for b in range(1,12):
            x=F(a,b);lo,hi=log_interval(x,7);lo2,hi2=log_interval(x,10)
            check(lo<=lo2<=hi2<=hi,'nested log intervals')
            nl,nu=log_interval(1/x,10)
            check(lo2+nl<=0<=hi2+nu,'inverse logarithm intervals')
            yl,yu=log_interval(x*x,10)
            check(yl<=2*hi2 and 2*lo2<=yu,'square logarithm interval overlap')
    check(log_interval(F(1))==(F(0),F(0)),'exact log one')
    for err in [F(0),F(1,2),F(2,3),F(7,10),F(70,99)]:
        u=sqrt2_upper(err)
        check(u*u>2 and u*err<1,'safe residual bound')
    try:log_interval(F(0))
    except ValueError:negative('reject log zero',True)
    else:negative('reject log zero',False)
    try:sqrt2_upper(F(3,4))
    except ValueError:negative('reject supercritical error',True)
    else:negative('reject supercritical error',False)
    examples=[]
    for n,b,k,e in [(16,4,1,F(0)),(32,8,100,F(0)),(100,10,10,F(1,5**30)),
                     (200,20,5**30,F(1,5**60)),(1000,40,5**100,F(1,5**300))]:
        c=certificate(n,k,e,b,8)
        check(c['excluded'] and verify(c),'strict rational exclusion')
        check(certificate(n,max(1,k//2),e,b,8)['excluded'],'smaller width also excluded')
        check(certificate(n,k,e/2,b,8)['excluded'],'smaller error also excluded')
        examples.append({'N':n,'b':b,'width':str(k),'error':str(e),'excluded':True})
    c=certificate(100,10,F(1,5**30),10,8)
    for name,value in [('excluded',False),('width',11),('horizon',99),('eta','1/4'),('gap_lower','0'),
                       ('transport_squared_upper','0'),('sqrt2_upper','1'),('assumption','matrix gap only')]:
        bad=deepcopy(c);bad[name]=value
        negative('tampered '+name,not verify(bad))
    nc=certificate(1,1,F(1,2),4,8)
    negative('no complete blocks is inconclusive',not nc['excluded'] and not verify(nc))
    negative('exact feasible width not excluded',not certificate(16,5**16,F(0),4,8)['excluded'])
    # Exact greedy cut counting with arbitrarily long gaps.
    for step in [1,2,3,9,31]:
        for j in range(1,60):
            cuts=[1+step*i for i in range(j)]
            for b in [4,5,7,12]:
                chosen=[]
                for t in cuts:
                    if not chosen or t-chosen[-1]>=b:chosen.append(t)
                check(len(chosen)>=(j+b-1)//b,'positive-cut greedy count')
                check(all(t>=1 for t in chosen),'cut zero excluded')
    return {'schema':'gtf63.finite-checks/1','status':'success','exact_finite_assertions':CHECKS,
            'negative_controls_detected':NEG,'strict_exclusion_examples':examples,
            'not_verified':['full action spectral norm','universal entropy inequalities','uniform asymptotic theorem','independent priority'],
            'scope':'Exact integer/fraction/symbolic regression and sufficient-certificate arithmetic only.'}

if __name__=='__main__':
    print(json.dumps(tests(),indent=2,sort_keys=True))
