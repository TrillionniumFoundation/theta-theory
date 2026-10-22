#!/usr/bin/env python3
"""Diagnostics for 281--283; never a certificate of continuum dynamics or LLT.

Exact symbolic and rational checks are separated from floating point specular
trajectories. All gates raise exceptions also under Python -O. A finite disk
search box is only a diagnostic implementation, not the horizon proof.
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
from check_cross_flight import next_hit, perp, CENTERS, require

KM, KP, TM = F(100,47), F(20,9), F(3,50)
UM = KP + 1/TM
QBAR = 4*(UM+1/(2*UM))**3/(27*KM*(KM+UM)**2*(1+TM*(KM+UM)))
FORCE = F(58,27)/(TM*KM**2)
LAMBDA = 1+2*KM*TM
AFOOT = math.sqrt(1827)/200
KSOURCE=(float(KP)+1/AFOOT)/AFOOT+(1+(97/200)/AFOOT)/AFOOT**2
BCV=max(KSOURCE,2*float(FORCE))


def algebra() -> dict[str, Any]:
    k,V,c,d,p,z,t,W,A=sp.symbols('k V c d p z t W A', positive=True)
    w=k+V; y=d*w/A; V1=k+y; s1s=-A/d
    cs=-p*V; ds=-z*V1*s1s; ts=-p+z*s1s
    As=cs+ts*w+t*W
    V1s=ds*w/A+d*W/A-d*w*As/A**2
    exact=-z*w/A*(k+2*y)-p*d*d*w*(k+2*V)/A**3-c*d*d*W/A**3
    require(sp.factor((V1s/s1s-exact).subs(c,A-t*w))==0,
            'signed circular second derivative identity')
    logder=(As/A-ds/d+V1*V1s/(1+V1**2)-V*W/(1+V**2))/s1s
    logexact=z*w/A+d*p*(k+2*V)/A**2-d*t*W/A**2+z*V1/d+V1*exact/(1+V1**2)+V*W*d/(A*(1+V**2))
    require(sp.factor((logder-logexact).subs(c,A-t*w))==0,
            'signed image-coordinate logarithmic Jacobian identity')
    require(sp.factor((3*V/(1+V**2)-3/w)-3*(k*V-1)/((1+V**2)*w))==0,
            'positive h derivative remainder')
    require(sp.factor(1/w-t/(1+t*w)-1/(w*(1+t*w)))==0,
            'positive h derivative lower bound')
    Y=sp.symbols('Y',nonnegative=True)
    require(sp.factor(sp.diff(Y**2/(k+Y)**3,Y)-Y*(2*k-Y)/(k+Y)**4)==0,
            'global rational maximum at Y=2*k')
    require(QBAR==F(946236091513673179721,2005319667933288000000),
            'exact rational curvature coefficient')
    require(0<QBAR<F(1,2),'strict contraction without floating-point rounding')
    require(FORCE==F(64061,8100),'forcing constant')
    require(LAMBDA==F(59,47),'actual adapted expansion constant')
    require(sp.factor((2*k+y)*A/(d*w)-(1+2*k*A/(d*w)))==0,
            'exact adapted one-step expansion')
    # The full Jacobian coefficient is checked after squaring positive factors.
    Qsq=c*c*d**4*(1+V**2)**3/(A*A+(k*A+d*w)**2)**3
    Qalt=(c/A)**2*(1+V**2)**3/w**4*y**4/(1+(k+y)**2)**3
    require(sp.cancel(Qsq-Qalt)==0,'geometric, not graph, curvature norm')
    # Uniform forcing proof constants, no sign or collision prefactor omitted.
    require(F(2)/(TM*KM**2)+F(4)/(27*TM*KM**2)==FORCE,'two forcing budgets')
    norms=0
    rng=np.random.default_rng(283281)
    for l in (1,2,8,64,256):
        f=rng.uniform(1,math.sqrt(1+float(KP)**2),l+1)
        require(abs(np.prod(f[1:]/f[:-1])-f[-1]/f[0])<1e-12,
                'arclength norm ratios telescope only at endpoints')
        norms+=1
    return {'symbolic_identities':'passed','qbar_exact':str(QBAR),'qbar':float(QBAR),
            'forcing_exact':str(FORCE),'adapted_expansion_exact':str(LAMBDA),
            'initial_source_curvature_allowance':KSOURCE,'invariant_allowance':BCV,
            'metric_telescoping_cases':norms,
            'independent_continuum_certificate':False}


def transform(k,V,W,c,p,d,p1,tau):
    w=k+V; a=c+tau*w; y=d*w/a; V1=k+y
    W1=-p1*w/a*(k+2*y)-p*d*d*w*(k+2*V)/a**3-c*d*d*W/a**3
    log1=p1*w/a+d*p*(k+2*V)/a**2-d*tau*W/a**2+p1*V1/d+V1*W1/(1+V1*V1)+V*W*d/(a*(1+V*V))
    q=c*d*d*(1+V*V)**1.5/(a*a+(k*a+d*w)**2)**1.5
    return V1,W1,log1,q,a


def graph_point(alpha,phi,V,W,R,z):
    al=alpha+z/R; ph=phi+V*z+W*z*z/2
    n=np.array([math.cos(al),math.sin(al)])
    q=R*n; v=math.cos(ph)*n+math.sin(ph)*perp(n)
    hit,nv,tau,c1,idx=next_hit(q,v,R)
    nn=(hit-CENTERS[idx])/R; nn/=np.linalg.norm(nn)
    p1=float(nv@perp(nn)); al1=math.atan2(nn[1],nn[0]); ph1=math.atan2(p1,c1)
    vv=V+W*z; v1,w1,lg,qcoef,a=transform(1/R,vv,W,math.cos(ph),math.sin(ph),c1,p1,tau)
    JE=(a/c1)*math.sqrt((1+v1*v1)/(1+vv*vv))
    return {'alpha1':al1,'phi1':ph1,'tau':tau,'c1':c1,'p1':p1,'idx':idx,
            'V1':v1,'W1':w1,'logder':lg,'Q':qcoef,'a':a,'JE':JE,'out':nv,'hit':hit}


def physical_derivatives():
    rng=np.random.default_rng(20261016281); probes=[]; rows=[]
    for i in range(1800):
        R=[.45,.46,.47][i%3]
        probes.append((R,float(rng.uniform(-math.pi,math.pi)),float(rng.uniform(-1.54,1.54)),
                       float(rng.uniform(1/R,float(UM))),float(rng.uniform(-40,40)),'generic'))
    for R in [.45,.46,.47]:
        for al in [.19,.72,1.27,2.21]:
            for side in [-1,1]:
                for delta in [1e-2,1e-4,1e-6,1e-8]:
                    probes.append((R,al,side*(math.pi/2-delta),1/R+2,-17.,'initial-grazing'))
            q=R*np.array([math.cos(al),math.sin(al)])
            for z in CENTERS:
                if not .99<float(np.linalg.norm(z))<2.01:continue
                r=z-q; dist=float(np.linalg.norm(r)); psi=math.atan2(r[1],r[0])
                for side in [-1,1]:
                    th0=psi+side*math.asin(R/dist)
                    for off in [1e-4,-1e-4,1e-6,-1e-6,1e-8,-1e-8]:
                        ph=math.atan2(math.sin(th0+off-al),math.cos(th0+off-al))
                        if abs(ph)>=math.pi/2-1e-6:continue
                        probes.append((R,al,ph,1/R+3,11.,'terminal-tangency-approach'))
    skipped_resolution=skipped_chart=0
    for R,al,ph,V,W,kind in probes:
        x=graph_point(al,ph,V,W,R,0)
        require(x['tau']>=float(TM)-1e-9,'actual flight lower bound')
        require(1/R<=x['V1']<=float(UM)+1e-9,'invariant slope cone')
        step=min(1e-7,2e-3*x['c1']**2/(1+V))
        # Initial angle must remain in the actual outgoing domain.
        step=min(step,(math.pi/2-abs(ph))/(100*(1+V)))
        if step<3e-14:skipped_resolution+=1;continue
        lo=graph_point(al,ph,V,W,R,-step); hi=graph_point(al,ph,V,W,R,step)
        if lo['idx']!=x['idx'] or hi['idx']!=x['idx']:skipped_chart+=1;continue
        ds=R*math.atan2(math.sin(hi['alpha1']-lo['alpha1']),math.cos(hi['alpha1']-lo['alpha1']))
        if abs(ds)<1e-12:skipped_resolution+=1;continue
        wfd=(hi['V1']-lo['V1'])/ds
        lgfd=(math.log(hi['JE'])-math.log(lo['JE']))/ds
        vfd=(hi['phi1']-lo['phi1'])/ds
        dsfd=ds/(2*step)
        errors=[abs(wfd-x['W1'])/max(1,abs(x['W1'])),
                abs(lgfd-x['logder'])/max(1,abs(x['logder'])),
                abs(vfd-x['V1'])/max(1,abs(x['V1'])),
                abs(dsfd+x['a']/x['c1'])/max(1,abs(dsfd))]
        require(max(errors)<8e-4,'independent physical derivative failure '+str((kind,R,ph,x['c1'],step,errors)))
        K=abs(W)/(1+V*V)**1.5;K1=abs(x['W1'])/(1+x['V1']**2)**1.5
        require(x['Q']<=float(QBAR)+1e-12,'geometric curvature coefficient')
        require(K1<=float(QBAR)*K+float(FORCE)+1e-12,'physical curvature forcing')
        rows.append({'kind':kind,'R':R,'alpha0':al,'phi0':ph,'V0':V,'W0':W,'step':step,
                     'c0':math.cos(ph),'c1':x['c1'],'target_center':CENTERS[x['idx']].tolist(),
                     'tau':x['tau'],'V1':x['V1'],'W1':x['W1'],'W1_fd':wfd,
                     'log_J_derivative':x['logder'],'log_J_derivative_fd':lgfd,
                     'curvature_coefficient':x['Q'],'maximum_scaled_error':max(errors)})
    require(len(rows)>2000,'insufficient actual derivative cases')
    require(min(r['c1'] for r in rows)<.001,'terminal grazing was not exercised')
    require(min(r['c0'] for r in rows)<1e-6,'initial grazing was not exercised')
    summary={'actual_cases':len(rows),'probe_count':len(probes),
             'minimum_initial_incidence':min(r['c0'] for r in rows),
             'minimum_terminal_incidence':min(r['c1'] for r in rows),
             'maximum_scaled_error':max(r['maximum_scaled_error'] for r in rows),
             'skipped_chart_changes':skipped_chart,'skipped_floating_resolution':skipped_resolution,
             'finite_search_box_is_not_horizon_proof':True}
    return summary,rows


def long_orbits():
    rng=np.random.default_rng(20261016282);rows=[]
    for case in range(180):
        R=[.45,.46,.47][case%3];k=1/R
        al=float(rng.uniform(-math.pi,math.pi));ph=float(rng.uniform(-1.5,1.5));
        n=np.array([math.cos(al),math.sin(al)]);q=R*n
        v=math.cos(ph)*n+math.sin(ph)*perp(n)
        V=k+1;W=20.;K0=abs(W)/(1+V*V)**1.5
        log_actual=0.;log_adapt=0.;first_factor=(k+V)/math.sqrt(1+V*V)
        for j in range(1,65):
            hit,out,tau,d,idx=next_hit(q,v,R);nn=(hit-CENTERS[idx])/R;nn/=np.linalg.norm(nn)
            p1=float(out@perp(nn));c=float(v@(q/R));p=float(v@perp(q/R))
            V1,W1,lg,Q,a=transform(k,V,W,c,p,d,p1,tau)
            Eu=a/d*math.sqrt((1+V1*V1)/(1+V*V));Ad=1+2*k*a/(d*(k+V))
            log_actual+=math.log(Eu);log_adapt+=math.log(Ad)
            endpoint=(k+V1)/math.sqrt(1+V1*V1)
            require(abs(log_adapt-log_actual-math.log(endpoint/first_factor))<1e-10,'all-time norm telescoping')
            bound=float(QBAR)**j*K0+float(FORCE)*(1-float(QBAR)**j)/(1-float(QBAR))
            K1=abs(W1)/(1+V1*V1)**1.5
            require(K1<=bound+1e-10,'actual all-time curvature recurrence')
            require(Ad>=float(LAMBDA)-1e-10,'actual adapted expansion')
            require(abs(float(np.linalg.norm(out))-1)<1e-12,'physical speed')
            if j in [1,8,32,64]:rows.append({'case':case,'R':R,'collisions':j,'curvature':K1,'recurrence_bound':bound,'terminal_incidence':d,'log_euclidean_jacobian':log_actual,'log_adapted_jacobian':log_adapt})
            # Exact spatial periodicity is used only to keep the diagnostic search
            # box centered. Each recorded step still intersects the nearest disk.
            q=R*nn;v=out;V=V1;W=W1
    return {'actual_orbit_cases':180,'collisions_per_orbit':64,'actual_collisions':11520,
            'recorded_checkpoints':len(rows),'continuum_complexity_or_distortion_certificate':False},rows


def tail_and_budget_checks():
    cases=0
    for N in [1,7,37,271,1024]:
        jf=2*N+1
        k0=2+math.ceil(float(2*F(jf)/(KM*TM*(1-1/LAMBDA))))
        tail=F(jf)/(KM*TM*(k0-1))
        require(tail<(1-1/LAMBDA)/2,'exact one-step tail schedule')
        require(1/LAMBDA+tail<1,'strict complete one-step sum')
        cases+=1
    grid=0
    for k in range(2,502):
        width=F(1,k*k)-F(1,(k+1)**2)
        require(width<=F(3,k**3),'homogeneous strip width, exact')
        require(F(1,k*k)<=F(1,k*(k-1)),'telescoping tail')
        grid+=1
    return {'exact_complexity_budget_cases':cases,'exact_strip_width_cases':grid,
            'uniform_central_branch_compactness':'proved in native text, not certified by finite samples',
            'full_normalized_roof_bound_proved':False,'raw_LLT_proved':False}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--details',type=Path);args=ap.parse_args()
    exact=algebra();physical,der=physical_derivatives();orbits,ors=long_orbits();tails=tail_and_budget_checks()
    if args.details:args.details.write_text(json.dumps({'derivative_cases':der,'orbit_checkpoints':ors},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','scope':'exact algebra and finite genuine-collision diagnostics, not a continuum proof certificate',
                      'algebra':exact,'physical_derivatives':physical,'long_orbits':orbits,'tail_and_budget':tails},indent=2,sort_keys=True))
if __name__=='__main__':main()
