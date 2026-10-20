#!/usr/bin/env python3
"""Finite algebra/physical diagnostics for modules 279--280.

These checks are NOT certificates for continuum curve growth, full word sums,
roof densities, or the raw LLT. All acceptance gates raise explicit exceptions,
including under python -O. Actual nearest-disk specular intersections are used;
a finite diagnostic search box is never used as a proof of finite horizon.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path
from typing import Any
import numpy as np
import sympy as sp
from check_cross_flight import CENTERS, next_hit, perp, require

A0 = math.sqrt(1827)/200
BMAX = 97/200
KMIN, KMAX = 100/47, 20/9
U0 = KMAX + 1/A0
K0 = U0/A0 + (1+BMAX/A0)/A0**2


def algebra() -> dict[str, Any]:
    a,b,c,p,k = sp.symbols('a b c p k', real=True)
    positive_a = sp.symbols('positive_a', positive=True)
    sprime = -a/c
    aprime = -b-a*p/c
    V = k-1/sprime
    as_ = sp.cancel(aprime/sprime)
    cs_ = -p*V
    Vs = sp.cancel(cs_/a-c*as_/a**2)
    require(sp.simplify(V-k-c/a)==0,'specular outgoing slope sign')
    require(sp.simplify(as_-p-b*c/a)==0,'signed physical foot derivative')
    require(sp.simplify(Vs+p*k/a+2*p*c/a**2+b*c**2/a**3)==0,
            'exact source graph second derivative')
    # Exact pointwise upper bound is the triangle inequality with |p|,c<=1.
    kp,am,bm=sp.symbols('kp am bm', positive=True)
    bound1=(kp+1/am)/am+(1+bm/am)/am**2
    bound2=kp/am+2/am**2+bm/am**3
    require(sp.simplify(bound1-bound2)==0,'uniform curvature budget algebra')
    require((1-F(47,100))**2-(F(47,100)+F(3,200))**2==F(1827,40000),
            'exact lattice standoff normalization')
    require(F(1827,40000)>F(3,50)**2,'source fits the common unstable cone')
    require(1-F(97,200)>F(47,100),'source foot exterior to all other disks')
    require(F(100,47)>F(100,53),'strict relative-angle monotonicity')
    j=sp.symbols('j', positive=True)
    require(sp.cancel(1/(j*(j-1))-1/j**2-1/(j**2*(j-1)))==0,
            'positive telescoping homogeneous tail majorant, j>=2')
    # Exact mass normalization: signs already in A, terminal signs already in Ct.
    A,Cg,Ct,R,cs,S=sp.symbols('A Cg Ct R cs S', positive=True)
    H=A*Cg*Ct
    require(sp.cancel(H/(4*sp.pi*R)-A*Cg*Ct/(4*sp.pi*R))==0,
            'single flux normalization')
    r,eps,C=sp.symbols('r eps C', positive=True)
    require(sp.cancel(C*(4*eps/(1-r))**2/(2*cs)-
                      8*C*eps**2/(cs*(1-r)**2))==0,'exact source schedule payment')
    # Coordinate changes telescope at endpoints, not once per collision.
    metric_cases=0
    rng=np.random.default_rng(90279)
    for n in (1,2,8,64):
        for _ in range(20):
            factors=rng.uniform(.9,1.1,n+1)
            product=float(np.prod(factors[1:]/factors[:-1]))
            require(abs(product-factors[-1]/factors[0])<2e-14,
                    'endpoint-only norm conversion')
            metric_cases+=1
    return {'symbolic_identities':'passed','exact_standoff_squared':'1827/40000',
            'source_slope_cap':U0,'source_curvature_cap':K0,
            'telescoping_majorant':'1/(j*(j-1))-1/j**2 = 1/(j**2*(j-1)), j>=2',
            'metric_endpoint_cases':metric_cases,
            'curve_growth_theorem_independently_certified':False}


def state(theta: float,u: float,sign: int,R: float) -> dict[str, Any]:
    v=np.array([math.cos(theta),math.sin(theta)])
    b=sign*(R+u)
    foot=-b*perp(v)
    q,out,a,c,idx=next_hit(foot,v,R)
    n=(q-CENTERS[idx])/R
    n=n/np.linalg.norm(n)
    p=float(out@perp(n))
    alpha=math.atan2(float(n[1]),float(n[0]))
    phi=math.atan2(p,c)
    V=1/R+c/a
    ap=p+b*c/a
    W=-p*V/a-c*ap/a**2
    return {'q':q,'out':out,'a':a,'c':c,'p':p,'alpha':alpha,'phi':phi,
            'idx':idx,'V':V,'W':W,'rho':c/(a*math.sqrt(1+V*V))}


def circle_difference(x,y):
    return math.atan2(math.sin(x-y),math.cos(x-y))


def derivative_checks() -> tuple[dict[str,Any],list[dict[str,Any]]]:
    rng=np.random.default_rng(202610279)
    rows=[];unstable_steps=0;changed=0;roundoff=0
    probes=[]
    for i in range(1200):
        probes.append((float(rng.uniform(0,2*math.pi)),
                       [.00001,.003,.014999][i%3],[-1,1][i%2],
                       [.45,.46,.47][i%3],None))
    # Approach algebraically known tangencies; keep only actual first targets.
    for R in [.45,.46,.47]:
        for u in [.00001,.0075,.014999]:
            for sig in [-1,1]:
                b=sig*(R+u)
                for z in CENTERS:
                    norm=float(np.linalg.norm(z))
                    if not .99<norm<2.01: continue
                    phase=math.atan2(-float(z[0]),float(z[1]))
                    for rhs in [R-b,-R-b]:
                        if abs(rhs)>=norm: continue
                        for theta0 in [phase+math.acos(rhs/norm),phase-math.acos(rhs/norm)]:
                            for off in [1e-4,-1e-4,1e-6,-1e-6,1e-8,-1e-8]:
                                probes.append((theta0+off,u,sig,R,abs(off)))
    for theta,u,sign,R,near in probes:
        x=state(theta,u,sign,R)
        require(x['a']>=A0-1e-9,'genuine first collision violates foot standoff')
        require(KMIN-1e-12<=x['V']<=U0+1e-9,'outgoing unstable cone')
        require(abs(x['W'])<=K0+1e-7,'outgoing graph curvature budget')
        require(0<x['rho']<=x['c']/A0+1e-12,'retained incidence in density')
        step=min(2e-7,1e-3*x['c']**2)
        if near is not None: step=min(step,near/300)
        if step<5e-13: roundoff+=1;continue
        lo=state(theta-step,u,sign,R);hi=state(theta+step,u,sign,R)
        if lo['idx']!=x['idx'] or hi['idx']!=x['idx']:
            changed+=1;continue
        ds=R*circle_difference(hi['alpha'],lo['alpha'])
        dphi=hi['phi']-lo['phi']
        if abs(ds)<1e-11: roundoff+=1;continue
        s_der=ds/(2*step);V_fd=dphi/ds
        a_fd=(hi['a']-lo['a'])/ds
        W_fd=(hi['V']-lo['V'])/ds
        rho_fd=2*step/math.hypot(ds,dphi)
        errors=[abs(s_der+x['a']/x['c'])/max(1,abs(s_der)),
                abs(V_fd-x['V'])/max(1,abs(x['V'])),
                abs(a_fd-(x['p']+sign*(R+u)*x['c']/x['a'])),
                abs(W_fd-x['W'])/max(1,abs(x['W'])),
                abs(rho_fd-x['rho'])/max(1e-8,x['rho'])]
        require(max(errors)<8e-4,'independent physical finite difference mismatch')
        rows.append({'R':R,'u':u,'sign':sign,'theta':theta,'step':step,
                     'first_center':CENTERS[x['idx']].tolist(),
                     'a':x['a'],'c':x['c'],'V':x['V'],'W':x['W'],
                     'rho':x['rho'],'ds_dtheta_fd':s_der,'V_fd':V_fd,
                     'da_ds_fd':a_fd,'dV_ds_fd':W_fd,'rho_fd':rho_fd,
                     'maximum_scaled_error':max(errors)})
    require(len(rows)>1500,'insufficient independent derivative diagnostics')
    require(min(r['c'] for r in rows)<.001,'grazing approach not exercised')
    return {'actual_derivative_cases':len(rows),
            'minimum_positive_incidence_tested':min(r['c'] for r in rows),
            'maximum_scaled_error':max(r['maximum_scaled_error'] for r in rows),
            'skipped_for_chart_changes':changed,'skipped_for_floating_resolution':roundoff,
            'search_box_not_a_finite_horizon_proof':True},rows


def angular_roots(z: np.ndarray,rhs: float) -> list[float]:
    norm=float(np.linalg.norm(z))
    if norm==0 or abs(rhs)>norm: return []
    phase=math.atan2(-float(z[0]),float(z[1]))
    ar=math.acos(max(-1,min(1,rhs/norm)))
    return [(phase+ar)%(2*math.pi),(phase-ar)%(2*math.pi)]


def branch_checks() -> dict[str, Any]:
    # D=4 is solely a finite diagnostic window; source theorem uses original tau+.
    candidates=[z for z in CENTERS if .5<float(np.linalg.norm(z))<=4]
    cases=0;intervals=0;maxcount=0
    for R in [.45,.46,.47]:
        for u in [.00001,.0075,.014999]:
            for sign in [-1,1]:
                b=sign*(R+u);cuts=[0.,2*math.pi]
                for z in candidates:
                    cuts+=angular_roots(z,R-b)+angular_roots(z,-R-b)
                    cuts+=angular_roots(z+np.array([R,0.]),-b)
                cuts=sorted(set(round(c,14) for c in cuts))
                require(len(cuts)-1<=8*len(candidates)+1,'first-hit branch budget')
                for l,r in zip(cuts,cuts[1:]):
                    if r-l<1e-10: continue
                    xs=[state(l+t*(r-l),u,sign,R) for t in [.1,.3,.5,.7,.9]]
                    require(len({x['idx'] for x in xs})==1,'target changes away from declared cuts')
                    require(float(np.linalg.norm(CENTERS[xs[0]['idx']]))<=4+1e-9,
                            'diagnostic candidate truncation misses first hit')
                    require(all(xs[i+1]['phi']<xs[i]['phi']+1e-9 for i in range(4)),
                            'source phi must be monotone on fixed first-hit interval')
                    intervals+=1
                cases+=1;maxcount=max(maxcount,len(cuts)-1)
    return {'parameter_cases':cases,'regular_intervals_checked':intervals,
            'diagnostic_candidates':len(candidates),'maximum_cut_interval_count':maxcount,
            'continuum_branch_count_certificate':False}


def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument('--details',type=Path)
    args=ap.parse_args()
    exact=algebra();physical,rows=derivative_checks();branches=branch_checks()
    out={'status':'passed','scope':'finite algebra and actual-ray diagnostics only',
         'algebra':exact,'physical_first_collision':physical,'first_hit_partition':branches,
         'full_physical_root_sum_numerically_certified':False,
         'roof_Linf_estimate_certified':False,'raw_pointwise_LLT_certified':False,
         'continuum_proof_certificate':False}
    if args.details:
        args.details.parent.mkdir(parents=True,exist_ok=True)
        args.details.write_text(json.dumps(rows,sort_keys=True,indent=2)+'\n')
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__': main()
