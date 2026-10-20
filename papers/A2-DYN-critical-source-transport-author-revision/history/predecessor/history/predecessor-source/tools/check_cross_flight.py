#!/usr/bin/env python3
"""Finite diagnostics for core/277--278, not a continuum or LLT certificate.

All critical checks raise exceptions explicitly; Python -O cannot disable them.
Exact rational matrix/normalization checks are separate from floating-point
actual specular trajectories. No sampled word count is used as a theorem input.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import itertools
import json
import math
from pathlib import Path
import random
from typing import Any
import numpy as np


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def mm(x, y):
    return tuple(tuple(sum(x[i][k]*y[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def prop(t): return ((F(1),t),(F(0),F(1)))
def kick(k): return ((F(1),F(0)),(k,F(1)))


def exact_checks() -> dict[str, Any]:
    amin2=F(1827,40000)
    km=F(100,47);kp=F(20,9);tmin=F(3,50)
    Lmax2=1+(kp+1/tmin)**2
    CJ2=Lmax2/(km**2*amin2**2)
    require((1-F(47,100))**2-(F(47,100)+F(3,200))**2==amin2,
            'exact physical standoff')
    require(amin2>tmin**2,'foot exceeds the original minimum full-flight scale')
    rng=random.Random(20261015)
    count=0;max_h=0;min_incidence=F(1)
    for h in [1,2,3,4,8,16,32]:
        for case in range(18):
            R=[F(9,20),F(23,50),F(47,100)][case%3];kap=1/R
            a=F(rng.randrange(23,81),100);b=F(rng.randrange(23,81),100)
            gaps=[F(rng.randrange(6,101),100) for _ in range(h-1)]
            cs=[F(1,rng.choice([1,2,3,5,10,100,1000])) for _ in range(h)]
            ks=[2*kap/c for c in cs]
            M=mm(kick(ks[0]),prop(a))
            for i in range(1,h): M=mm(mm(kick(ks[i]),prop(gaps[i-1])),M)
            M=mm(prop(b),M)
            A,B=M[0];C,D=M[1]
            require(A*D-B*C==1,'determinant one for every rational chain')
            require(B>=a+b+sum(gaps),'complete free-length lower bound')
            require(B*B>=amin2*(1+2*km*tmin)**(2*(h-1)),
                    'exponential positive propagation lower bound')
            # A genuine positive Riccati continuation, algebraically exact.
            tail_gap=b+F(1,3)
            next_k=2*kap/F(1,3)
            tail_beta=F(1,7)
            beta=[F(0)]*h
            beta[-1]=(next_k+tail_beta)/(1+tail_gap*(next_k+tail_beta))
            for i in range(h-2,-1,-1):
                beta[i]=(ks[i+1]+beta[i+1])/(1+gaps[i]*(ks[i+1]+beta[i+1]))
            Jmid=F(1)
            for ell,bb in zip(gaps,beta):
                require(0<ell*bb<1,'no stable focal crossing before actual collision')
                Jmid*=1-ell*bb
            gamma=Jmid*(1-b*beta[-1])/(1+a*(ks[0]+beta[0]))
            bend=beta[-1]/(1-b*beta[-1])
            require(gamma*(D+B*bend)==1,'inverse monodromy/stable contraction identity')
            require(b*beta[-1]<1,'second foot precedes next collision')
            require((D/B)**2<=1/amin2,'last free factor controls D/B')
            require(bend*bend<=1/amin2,'last stable slope bound')
            L1sq=1+(kap+cs[0]*beta[0])**2
            Lhsq=1+(kap+cs[-1]*beta[-1])**2
            # j = Jmid*(c1/ch)*(Lh/L1); square removes only positive roots.
            chj_sq=Jmid**2*cs[0]**2*Lhsq/L1sq
            require(F(1,B*B)<=CJ2*chj_sq,'metric-correct stable Green comparison')
            if h==1: require(Jmid==1 and L1sq==Lhsq,'empty stable block')
            count+=1;max_h=max(max_h,h);min_incidence=min(min_incidence,*cs)
    factorial_cases=0
    for length in range(1,8):
        for vals in itertools.product(range(4),repeat=length):
            N=sum(vals)
            rhs=sum(v*(v-1) for v in vals)+2*sum(vals[i]*vals[j]
                        for i in range(length) for j in range(i+1,length))
            require(N*(N-1)==rhs,'same-flight / cross-flight exact ordered decomposition')
            require(0<=N-int(N>=1)<=F(N*(N-1),2),'overcount normalization factor 1/2')
            require(N*int(N>=2)<=N*(N-1),'one-witness lower bound')
            factorial_cases+=1
    schedule_cases=0
    for m in range(1,129):
        for r in [F(1,2),F(9,10),F(99,100)]:
            eps=F(1,2000)
            ds=[2*eps*r**min(j,m-1-j) for j in range(m)]
            S=sum(ds)
            require(S<=4*eps/(1-r),'original two-ended sum for odd/even m')
            require(S*S/F(2)<=8*eps*eps/(1-r)**2,'complete-record normalized mass factor')
            require(sum(x*x for x in ds)<=8*eps*eps/(1-r*r),'inherited same-flight schedule')
            schedule_cases+=1
    return {'rational_jacobi_chains':count,'largest_exact_h':max_h,
            'smallest_test_incidence':str(min_incidence),
            'factorial_integer_cases':factorial_cases,'schedule_cases':schedule_cases,
            'standoff_squared':str(amin2),'pressure_bound_numerically_certified':False}


def perp(v): return np.array([-v[1],v[0]])
CENTERS=np.array([(a+b/2,b*math.sqrt(3)/2)
                  for a in range(-14,15) for b in range(-14,15)],float)


def next_hit(q, v, R):
    """Nearest actual disk intersection in a finite diagnostic search box."""
    rel=CENTERS-q;along=rel@v;side=rel@perp(v)
    disc=R*R-side*side
    valid=(disc>1e-15)&(along>1e-9)
    ts=np.where(valid,along-np.sqrt(np.maximum(disc,0)),np.inf)
    ts=np.where(ts>1e-8,ts,np.inf)
    idx=int(np.argmin(ts));t=float(ts[idx])
    require(math.isfinite(t),'diagnostic lattice search exhausted; do not assume horizon')
    hit=q+t*v;n=(hit-CENTERS[idx])/R
    normal_length=float(np.linalg.norm(n))
    require(abs(normal_length-1)<1e-7,'uncorrected contact normal is inconsistent with disk geometry')
    n=n/normal_length
    # Restore the exact unit-speed convention after floating-point roundoff.
    c=-float(v@n)
    require(c>0,'actual inward incidence at the next collision')
    nv=v+2*c*n
    nv=nv/float(np.linalg.norm(nv))
    require(abs(float(nv@nv)-1)<1e-14,'physical unit speed after specular reflection')
    return hit,nv,t,c,idx


def trace(theta,u,sign,R,h):
    v=np.array([math.cos(theta),math.sin(theta)])
    q=-sign*(R+u)*perp(v);rec=[]
    for _ in range(h):
        q,v,l,c,idx=next_hit(q,v,R)
        rec.append((q.copy(),v.copy(),l,c,idx))
    _,_,t,_,idx=next_hit(q,v,R)
    return rec,t,idx


def physical_checks() -> tuple[dict[str,Any],list[dict[str,Any]]]:
    rng=np.random.default_rng(20261015);rows=[];a0=math.sqrt(1827)/200
    skipped_resolution=0;skipped_chart=0
    hs=[1,2,3,4,6,8]
    for run in range(1400):
        R=[.45,.46,.47][run%3];sign=[-1,1][run%2]
        theta=float(rng.uniform(0,2*math.pi));u=float(rng.uniform(.001,.014))
        for h in hs:
            rec,t,idx=trace(theta,u,sign,R,h)
            q,v=rec[-1][:2];rel=CENTERS-q
            foot=rel@v;impact=rel@perp(v)
            marked=np.where((np.abs(impact)>R)&(np.abs(impact)<R+.015)
                            &(foot>1e-7)&(foot<t-1e-7))[0]
            for zidx in marked:
                M=np.eye(2)
                for _,_,l,c,_ in rec:
                    M=np.array([[1.,0.],[2/(R*c),1.]])@np.array([[1.,l],[0.,1.]])@M
                b=float(foot[zidx]);M=np.array([[1.,b],[0.,1.]])@M;B=float(M[0,1])
                require(rec[0][2]+1e-10>=a0 and b+1e-10>=a0 and t-b+1e-10>=a0,
                        'actual feet obey the improved geometric bound')
                require(B+1e-8>=a0*(1+2*(100/47)*.06)**(h-1),
                        'actual transverse propagation lower bound')
                eta=min(1e-6,1e-6/B)
                if eta<2e-14: skipped_resolution+=1;continue
                vals=[];same=True
                for off in [-eta,eta]:
                    rr,tt,_=trace(theta+off,u,sign,R,h)
                    qq,vv=rr[-1][:2];ft=float((CENTERS[zidx]-qq)@vv)
                    if [r[4] for r in rr]!=[r[4] for r in rec] or not 0<ft<tt:
                        same=False;break
                    vals.append(float((CENTERS[zidx]-qq)@perp(vv)))
                if not same: skipped_chart+=1;continue
                derivative=(vals[1]-vals[0])/(2*eta)
                err=abs(abs(derivative)-B)/B
                require(err<1e-3,'actual physical two-mark Jacobian disagrees with derived formula')
                rows.append({'h':h,'R':R,'theta':theta,'u1':u,'sign1':sign,
                    'second_center':CENTERS[zidx].tolist(),
                    'collision_word_indices':[r[4] for r in rec],
                    'a':rec[0][2],'b':b,'B':B,'finite_difference':derivative,
                    'relative_error':err,'step':eta})
    by_h={str(h):sum(row['h']==h for row in rows) for h in hs}
    require(all(n>=10 for n in by_h.values()),'insufficient finite diagnostic coverage')
    return {'initial_marked_rays':1400,'separations_tested':hs,
            'actual_fixed_word_jacobian_cases':len(rows),'cases_by_separation':by_h,
            'max_relative_error':max(row['relative_error'] for row in rows),
            'minimum_observed_foot_standoff':min(min(row['a'],row['b']) for row in rows),
            'maximum_observed_Green_entry':max(row['B'] for row in rows),
            'skipped_due_to_machine_resolution':skipped_resolution,
            'skipped_due_to_chart_change':skipped_chart,
            'finite_search_box_not_a_horizon_proof':True},rows


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--details',type=Path)
    args=parser.parse_args()
    exact=exact_checks();physical,rows=physical_checks()
    if args.details:
        args.details.parent.mkdir(parents=True,exist_ok=True)
        args.details.write_text(json.dumps(rows,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'passed','exact_algebra':exact,'physical_diagnostics':physical,
        'full_raw_pointwise_LLT_certified':False,'independent_continuum_proof_certificate':False},
        sort_keys=True,indent=2))

if __name__=='__main__':main()
