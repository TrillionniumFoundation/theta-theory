#!/usr/bin/env python3
"""Exact algebra and finite actual-billiard diagnostics for 284--285.

No sampled word count, finite root search or floating-point pass proves a
uniform continuum growth theorem, a critical-sector limit, or the raw LLT.
All checks remain active under Python -O. The seed and every skipped finite-
difference chart/resolution case are reported; raw cases may be archived.
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
from check_uniform_growth import graph_point

KM,KP,TM=F(100,47),F(20,9),F(3,50)
U=KP+1/TM
U2=KP+2/TM
KF=(KP+2/TM)/TM+1/(TM**3*KM)


def exact_algebra() -> dict[str,Any]:
    k,c,d,p,z,t,A=sp.symbols('k c d p z t A',real=True,nonzero=True)
    V1=k+d*k/A
    ss=-A/d
    ds=-z*V1*ss
    As=(-p+z*ss)*k
    W=(ds*k/A-d*k*As/A**2)/ss
    exact=-z*k/A*(k+2*d*k/A)-p*d**2*k**2/A**3
    require(sp.factor(W-exact)==0,'momentum fibre exact signed curvature identity')
    VV=sp.symbols('VV',positive=True)
    ww=k+VV
    AA=c+t*ww
    require(sp.factor(d*(k+d*ww/AA)*(AA/d)-(k*AA+d*ww))==0,
            'last physical incidence cancels before taking a bound')
    require(sp.factor((k+VV)**2-(1+VV**2)-(k*k+2*k*VV-1))==0,
            'cone adapted metric lower bound has a positive margin')
    R,e,aa,dd,cs=sp.symbols('R e aa dd cs',positive=True)
    Delta=aa*dd-e**2
    G=sp.Matrix([[aa,e],[e,dd]])
    D=sp.diag(-1,1)
    B=sp.Matrix([[-aa/e,-R/e],[-Delta/(R*e),-dd/e]])
    require(sp.factor(B.det()-1)==0,'physical symplectic collision derivative')
    # Absolute e is positive here; both signs are tested in the numerical part.
    inv=R*e/Delta
    J=e/(2*R*cs*sp.sqrt(Delta))
    require(sp.simplify(J-sp.sqrt(Delta)*inv/(2*R**2*cs))==0,
            'no missing R or cstar in critical inverse weight')
    Hess_q_to_z=D*G/R
    alpha0_a=sp.Matrix([[1,0],[0,1]])
    require(sp.factor(Hess_q_to_z.det()+Delta/R**2)==0,'signed endpoint momentum Jacobian')
    # Coarea along fixed p0 contributes inverse lower-left DT entry.
    require(sp.factor((-1/B[1,0])-inv)==0,'pointwise momentum root weight')
    x,y,l11,l12,l21,l22=sp.symbols('x y l11 l12 l21 l22',real=True)
    L=sp.Matrix([[l11,l12],[l21,l22]])
    v=L*sp.Matrix([x,y]); vp=L*sp.Matrix([-y,x])
    require(sp.factor(v[0]*vp[1]-v[1]*vp[0]-L.det()*(x*x+y*y))==0,
            'polar angle numerator for nonorthogonal linear map')
    require(U==F(170,9) and U2==F(320,9),'endpoint Hessian rational constants')
    require(1-4*F(47,100)**2==F(291,2500),'one-flight discriminant lower bound')
    a,v,rad=sp.symbols('a v rad',real=True)
    rr=sp.symbols('rr',positive=True)
    roof=sp.sqrt(rr**2-R**2*(v-a)**2)-R*sp.sqrt(1-a*a)-R*sp.sqrt(1-v*v)
    Hp=sp.hessian(roof,(a,v)).subs({a:0,v:0})
    expected=sp.Matrix([[R-R**2/rr,R**2/rr],[R**2/rr,R-R**2/rr]])
    require(sp.simplify(Hp-expected)==sp.zeros(2),'exact physical one-flight roof Hessian')
    require(sp.factor(Hp.det()-R**2*(1-2*R/rr))==0,'one-flight critical determinant in momenta')
    require(KM>F(100,53),'initial horizontal-fibre relative-angle monotonicity')
    require(F(1,1)-2*F(47,100)==TM,'physical flight lower bound')
    return {'symbolic_identities':'passed','U':str(U),'U2':str(U2),
            'source_curvature_cap_exact':str(KF),'source_curvature_cap':float(KF),
            'initial_fibre_mass':'2*pi in d_alpha, not a probability law',
            'section_normalization':'1/(4*pi*cstar), exactly once',
            'source_incidence_factor_retained':True}


def physical_first_image() -> tuple[dict[str,Any],list[dict[str,Any]]]:
    rng=np.random.default_rng(20261016284)
    probes=[]
    for i in range(1500):
        probes.append(([.45,.46,.47][i%3],float(rng.uniform(-math.pi,math.pi)),
                       float(rng.uniform(-1.54,1.54)),'generic'))
    for R in [.45,.46,.47]:
        for al in [.17,.61,1.13,2.19]:
            for sg in [-1,1]:
                for c in [1e-2,1e-4,1e-6,1e-8]:
                    probes.append((R,al,sg*math.acos(c),'initial-grazing'))
            q=R*np.array([math.cos(al),math.sin(al)])
            for z in CENTERS:
                if not .99<float(np.linalg.norm(z))<2.01:continue
                r=z-q;dist=float(np.linalg.norm(r));psi=math.atan2(r[1],r[0])
                for sg in [-1,1]:
                    th=psi+sg*math.asin(R/dist)
                    for off in [-1e-4,1e-4,-1e-6,1e-6,-1e-8,1e-8]:
                        ph=math.atan2(math.sin(th+off-al),math.cos(th+off-al))
                        if abs(ph)<math.pi/2-1e-7:probes.append((R,al,ph,'terminal-grazing'))
    rows=[];chart_skips=resolution_skips=0
    for R,al,ph,kind in probes:
        x=graph_point(al,ph,0.,0.,R,0.)
        d=x['c1']; A=x['a']; rho=d/(R*A*math.sqrt(1+x['V1']**2))
        require(1/R<=x['V1']<=float(U)+1e-10,'momentum source reaches actual unstable cone')
        require(rho<=d/float(TM)+1e-9,'grazing factor in source density')
        require(abs(x['W1'])/(1+x['V1']**2)**1.5<=float(KF)+1e-7,
                'momentum source geometric curvature cap')
        step=min(1e-7,1e-3*d*d)
        if step<2e-13:resolution_skips+=1;continue
        lo=graph_point(al,ph,0.,0.,R,-step);hi=graph_point(al,ph,0.,0.,R,step)
        if lo['idx']!=x['idx'] or hi['idx']!=x['idx']:chart_skips+=1;continue
        ds=R*math.atan2(math.sin(hi['alpha1']-lo['alpha1']),math.cos(hi['alpha1']-lo['alpha1']))
        dp=hi['phi1']-lo['phi1']
        if abs(ds)<1e-12:resolution_skips+=1;continue
        vals={'s1_derivative':ds/(2*step),'V1':dp/ds,'W1':(hi['V1']-lo['V1'])/ds,
              'rho':(2*step/R)/math.hypot(ds,dp)}
        refs={'s1_derivative':-A/d,'V1':x['V1'],'W1':x['W1'],'rho':rho}
        err={k:abs(vals[k]-refs[k])/max(1e-8,abs(refs[k])) for k in vals}
        # Tiny W1 can be close to a genuine zero; use absolute/relative scaled error.
        err['W1']=abs(vals['W1']-refs['W1'])/max(1,abs(refs['W1']))
        require(max(err.values())<8e-4,'physical momentum-fibre derivative '+str((kind,R,ph,d,err)))
        rows.append({'R':R,'alpha0':al,'phi0':ph,'p0':math.sin(ph),'kind':kind,
                     'c0':math.cos(ph),'c1':d,'tau':x['tau'],'center':CENTERS[x['idx']].tolist(),
                     'step_s0':step,'formulas':refs,'finite_differences':vals,
                     'maximum_scaled_error':max(err.values())})
    require(len(rows)>1800,'insufficient physical first-image diagnostics')
    require(min(r['c0'] for r in rows)<1e-6,'initial grazing probes absent')
    require(min(r['c1'] for r in rows)<1e-3,'terminal grazing probes absent')
    return {'probe_count':len(probes),'actual_cases':len(rows),'chart_skips':chart_skips,
            'floating_resolution_skips':resolution_skips,
            'minimum_c0':min(r['c0'] for r in rows),'minimum_c1':min(r['c1'] for r in rows),
            'maximum_scaled_error':max(r['maximum_scaled_error'] for r in rows),
            'finite_lattice_search_not_a_horizon_proof':True},rows


def physical_last_collision():
    rng=np.random.default_rng(20261016286);rows=[];skips=0
    for i in range(720):
        R=[.45,.46,.47][i%3];k=1/R
        al=float(rng.uniform(-math.pi,math.pi));ph=float(rng.uniform(-1.55,1.55))
        V=float(rng.uniform(k,float(U)))
        x=graph_point(al,ph,V,0.,R,0.)
        A=x['a'];d=x['c1'];w=k+V
        derivative=-(k*A+d*w)/math.sqrt(1+V*V)
        require(abs(derivative)>=float(KM*TM)-1e-10,'last-collision uniform momentum derivative')
        h=min(2e-7,2e-3*d*d/(1+V))
        lo=graph_point(al,ph,V,0.,R,-h);hi=graph_point(al,ph,V,0.,R,h)
        if lo['idx']!=x['idx'] or hi['idx']!=x['idx']:skips+=1;continue
        fd=(hi['p1']-lo['p1'])/(2*h*math.sqrt(1+V*V))
        error=abs(fd-derivative)/max(1,abs(derivative))
        require(error<8e-4,'independent final momentum cancellation derivative')
        rows.append({'R':R,'c0':math.cos(ph),'c1':d,'V':V,'derivative':derivative,
                     'finite_difference':fd,'scaled_error':error})
    return {'cases':len(rows),'skipped_chart_changes':skips,
            'minimum_abs_derivative':min(abs(r['derivative']) for r in rows),
            'universal_lower_bound':str(KM*TM),
            'maximum_scaled_error':max(r['scaled_error'] for r in rows)},rows


def one_step_matrix(c,p,d,p1,tau,R):
    # Independent contact/reflect differentiation in (alpha,p).
    k=1/R
    ds_ds=- (c+tau*k)/d
    ds_dphi=-tau/d
    dphi_ds=k*ds_ds-k
    dphi_dphi=k*ds_dphi-1
    return np.array([[ds_ds,ds_dphi/(R*c)],
                     [d*dphi_ds*R,d*dphi_dphi/c]])


def orbit(al,p,R,m):
    n=np.array([math.cos(al),math.sin(al)])
    q=R*n;v=math.sqrt(1-p*p)*n+p*perp(n);B=np.eye(2);word=[]
    for j in range(m):
        c=float(v@(q/R)); pp=float(v@perp(q/R))
        hit,out,tau,d,idx=next_hit(q,v,R)
        nn=(hit-CENTERS[idx])/R;nn/=np.linalg.norm(nn)
        p1=float(out@perp(nn))
        B=one_step_matrix(c,pp,d,p1,tau,R)@B
        word.append(tuple(float(x) for x in CENTERS[idx]))
        q=R*nn;v=out
    return p1,B,word


def physical_endpoint_derivatives():
    rng=np.random.default_rng(20261016285);rows=[];skips=0
    for i in range(240):
        R=[.45,.46,.47][i%3];al=float(rng.uniform(-math.pi,math.pi));a=float(rng.uniform(-.9,.9));m=1+i%5
        v,B,w=orbit(al,a,R,m)
        h=min(2e-7,2e-5/max(1,np.linalg.norm(B)))
        if h<1e-12:skips+=1;continue
        vl,_,wl=orbit(al-h,a,R,m);vr,_,wr=orbit(al+h,a,R,m)
        if wl!=w or wr!=w:skips+=1;continue
        fd=(vr-vl)/(2*h);err=abs(fd-B[1,0])/max(1,abs(B[1,0]))
        require(err<7e-4,'actual endpoint momentum root derivative')
        require(abs(B[1,0])>0,'root derivative zero on physical unstable image')
        rows.append({'R':R,'m':m,'alpha0':al,'p0':a,'pm':v,'B21':float(B[1,0]),
                     'finite_difference':fd,'step':h,'scaled_error':err})
    require(len(rows)>170,'too few finite physical endpoint derivatives')
    return {'cases':len(rows),'chart_or_resolution_skips':skips,
            'maximum_scaled_error':max(r['scaled_error'] for r in rows)},rows


def physical_oneflight_kernel():
    values=[-.9999,-.9,-.4,0.,.4,.9,.9999]
    centers=[z for z in CENTERS if .99<float(np.linalg.norm(z))<2.01]
    admitted=[];masked=0
    for R in [.45,.46,.47]:
        for a in values:
            for target in values:
                for z in centers:
                    radius=float(np.linalg.norm(z))
                    Q=math.sqrt(radius*radius-R*R*(target-a)**2)
                    al=math.atan2(z[1],z[0])-math.asin(R*(target-a)/radius)-math.asin(a)
                    n=np.array([math.cos(al),math.sin(al)]);q=R*n
                    vel=math.sqrt(1-a*a)*n+a*perp(n)
                    hit,out,tau,d,idx=next_hit(q,vel,R)
                    if np.linalg.norm(CENTERS[idx]-z)>1e-9:masked+=1;continue
                    nn=(hit-z)/R;nn/=np.linalg.norm(nn)
                    p1=float(out@perp(nn))
                    expected_tau=Q-R*math.sqrt(1-a*a)-R*math.sqrt(1-target*target)
                    require(abs(p1-target)<2e-10,'actual exact-lattice kernel terminal momentum')
                    require(abs(tau-expected_tau)<2e-10,'actual original physical roof T_z')
                    B=one_step_matrix(math.sqrt(1-a*a),a,d,p1,tau,R)
                    require(abs(B[1,0]+Q/R)<3e-9,'exact one-flight inverse root derivative')
                    require(R/Q<=47/(2*math.sqrt(291))+1e-12,'one-flight uniform discriminant bound')
                    admitted.append({'R':R,'p0':a,'pm':target,'center':z.tolist(),
                                     'tau':tau,'exact_tau':expected_tau,'inverse_weight':R/Q,
                                     'maximum_absolute_error':max(abs(p1-target),abs(tau-expected_tau))})
    require(len(admitted)>500,'too few actual exact one-flight lattice roots')
    return {'admitted_actual_roots':len(admitted),'excluded_by_actual_first_hit_mask':masked,
            'tested_displacement_candidates':len(centers),
            'maximum_absolute_error':max(r['maximum_absolute_error'] for r in admitted),
            'finite_sample_is_not_complete_continuum_root_enumeration':True},admitted


def sector_and_hessian():
    rng=np.random.default_rng(285284);rows=[]
    # Positivity, determinant and angular laws are algebraic diagnostics, not
    # substitutes for the actual optical-Hessian proof.
    for i in range(96):
        ang=float(rng.uniform(0,math.pi));C=np.array([[math.cos(ang),-math.sin(ang)],[math.sin(ang),math.cos(ang)]])
        ev=np.array([float(rng.uniform(.05,1)),float(rng.uniform(1.1,5))]);G=(C*ev)@C.T
        R=[.45,.46,.47][i%3]; cs=91/(10000*math.pi)
        sqrtG=(C*np.sqrt(ev))@C.T; L=np.diag([-1,1])@sqrtG/R
        theta=float(rng.uniform(-math.pi,math.pi));width=float(rng.uniform(.07,2.9))
        ts=theta+(np.arange(10000)+.5)*width/10000
        E=np.stack([np.cos(ts),np.sin(ts)])
        aj=math.sqrt(np.linalg.det(G))/np.einsum('ij,ij->j',E,G@E)
        bz=float(aj.mean()*width/(2*math.pi));by=width/(2*math.pi)
        ends=L@np.array([[math.cos(theta),math.cos(theta+width)],[math.sin(theta),math.sin(theta+width)]])
        exact_angle=abs(math.atan2(np.linalg.det(ends),float(ends[:,0]@ends[:,1])))
        exact_bz=exact_angle/(2*math.pi)
        require(abs(bz-exact_bz)<3e-7,'anisotropic sector angular coarea')
        Delta=float(np.linalg.det(G));e=float(G[0,1]);u=R*abs(e)/Delta;J=abs(e)/(2*R*cs*math.sqrt(Delta))
        require(J*by<=float(ev.max())/(2*R*R*cs)*u*bz+1e-8,'sector Hessian comparison')
        rows.append({'eigenvalues':ev.tolist(),'width':width,'normalized_sector':by,
                     'momentum_sector':bz,'analytic_momentum_sector':exact_bz,'R':R})
    # Actual shortest normal two-disk flight: build Hessian by independent
    # Euclidean contact derivatives, compare against the collision matrix.
    normal=[]
    for R in [.45,.46,.47]:
        tau=1-2*R;A=R+R*R/tau;e=R*R/tau
        G=np.array([[A,e],[e,A]]);Delta=float(np.linalg.det(G))
        v,B,w=orbit(0.,0.,R,1)
        require(abs(v)<1e-12,'normal orbit terminal momentum')
        require(abs(B[1,0]+Delta/(R*e))<1e-9,'physical B21 and normal Hessian')
        require(math.sqrt(Delta)/R**2<=float(U)+1e-9,'normal determinant upper bound')
        require(float(np.linalg.eigvalsh(G).max())/R**2<=float(U2)+1e-9,'one-flight eigenvalue bound')
        normal.append({'R':R,'tau':tau,'G':G.tolist(),'B21':float(B[1,0]),'u':1/abs(B[1,0]),
                       'lambda_max_over_R2':float(np.linalg.eigvalsh(G).max())/R**2})
    return {'anisotropic_sector_cases':len(rows),'actual_normal_orbits':normal,
            'all_charts_or_limiting_sectors_certified':False},rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--details',type=Path);args=ap.parse_args()
    al=exact_algebra();p,pr=physical_first_image();e,er=physical_endpoint_derivatives();s,sr=sector_and_hessian();last,lr=physical_last_collision();one,orr=physical_oneflight_kernel()
    if args.details:args.details.write_text(json.dumps({'physical_source':pr,'endpoint_derivatives':er,'sector_cases':sr,'last_collision':lr,'oneflight_roots':orr},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','scope':'exact identities and finite physical diagnostics; not proof certification',
                      'algebra':al,'physical_first_image':p,'physical_last_collision':last,'endpoint_derivatives':e,'critical_sectors':s,'exact_oneflight_kernel':one,
                      'full_raw_pointwise_LLT_proved':False,'independent_expert_certificate':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
