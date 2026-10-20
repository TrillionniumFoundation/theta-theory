#!/usr/bin/env python3
"""Finite diagnostics for physical-tube and common-roof proofs 292--293.
Exact rational checks and actual triangular billiard samples are distinguished.
Neither samples nor algebraic test functions certify the continuous root theorem.
"""
from __future__ import annotations
import argparse,json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp
import check_endpoint_localization as old
import check_reflection_resolvent as reflection

A=F(47,6); RP=F(47,100); RM=F(9,20); LAM=F(50,47); Q0=F(47,53)
K=2*(1+LAM)*(4*A+16*A*A)
RS=min(1/(8*(1+A)),1/(8*K)); ETA=RS/(8*(1+LAM*A))
P=2*(1+LAM*A); CI=P*(1+2*A*(1+LAM)); CL=RP*P
DELTA=min(ETA,1/(2*CI),1/(2*CL)); G=RM/2; U=F(320,9)

def require(ok,msg):
    if not ok: raise RuntimeError(msg)

def exact():
    require(0<RS<F(1,8) and 2*A*RS<F(1,4),'nonvanishing complex flight disks')
    require(K*RS<=F(1,8),'complex contraction')
    require(LAM*A*ETA<=RS/8,'boundary forcing')
    require(ETA+RS/2<RS,'fixed point stays in analytic domain')
    require(K*RS**2/2<=RS/16,'nonlinear remainder')
    require(F(16,15)*(1+LAM*A)<=P,'localized fixed point bound')
    require(CI*DELTA<=F(1,2) and CL*DELTA<=F(1,2),'physical half margins')
    require(LAM**4*Q0>1,'analytic localization beats original depth guard')
    require(old.SIG**4<Q0,'optical distortion depth summability')
    # Bracket beta without treating an approximate fourth root as a proof.
    blo=F(820,1000);bhi=F(821,1000)
    require(blo**4*Q0<old.SIG**4<bhi**4*Q0,'rational beta bracket')
    pairs=0
    for m in range(1,101):
        for i in range(m):
            d=min(i,m-i);dn=min(i+1,m-i-1);df=min(i,m-i-1)
            require(abs(d-dn)<=1 and min(d,dn)==df,'endpoint / flight depth indexing')
            pairs+=1
        # Exact rational majorants of the infinite geometric series.
        ss=[old.SIG**i+old.SIG**(m-i) for i in range(m+1)]
        require(sum(ss[i]+ss[i+1] for i in range(m))<=4/(1-old.SIG),'full flight sum')
        require(sum(2*bhi**min(i,m-i) for i in range(m+1))<=4/(1-bhi),'all-depth incidence envelope')
    # Coarea normalization checked over a physical momentum measure:
    # dt=r*h dr; density u*r/(4*pi*c* r*h); angle length 2*pi.
    aa,ee,dd,RR,hh,rr,cc=sp.symbols('aa ee dd RR hh rr cc',positive=True)
    dp=(ee-dd*aa/ee)/RR
    require(sp.simplify(dp+(aa*dd-ee**2)/(RR*ee))==0,'fixed initial momentum Jacobian')
    source=RR*ee/(aa*dd-ee**2)/(4*sp.pi*cc)
    require(sp.simplify(source*rr/(rr*hh)-source/hh)==0,'radial r cancellation')
    require(sp.simplify(2*sp.pi*source/hh-RR*ee/(2*cc*hh*(aa*dd-ee**2)))==0,'section and full angular normalization')
    return {'rational_checks':'passed','depth_index_pairs':pairs,
        'constants':{k:str(v) for k,v in dict(a=A,lambda_=LAM,K=K,r_star=RS,eta_star=ETA,
            P_star=P,C_inc=CI,C_clr=CL,delta_star=DELTA,g=G,U=U).items()},
        'beta_rational_bracket':[str(blo),str(bhi)],
        'scope':'exact finite arithmetic checks supporting, not replacing, the written all-count proof'}

def solve(o,h):
    """Actual reflection equations, not a stochastic transition approximation."""
    alpha=o['angles'].copy();alpha[0]+=h[0];alpha[-1]+=h[-1]
    if o['m']>1:
        # Use reflection residual (including its fixed lift), not divide by incidence.
        def residual(a):
            n=np.column_stack((np.cos(a),np.sin(a)));x=o['centers']+o['R']*n
            theta=np.unwrap(np.arctan2(np.diff(x,axis=0)[:,1],np.diff(x,axis=0)[:,0]))
            return 2*a[1:-1]-theta[:-1]-theta[1:]
        base=residual(o['angles'])
        for _ in range(20):
            r=residual(alpha)-base;r=(r+math.pi)%(2*math.pi)-math.pi
            if np.max(abs(r))<3e-14: break
            B,_,_=reflection.reflection(o,alpha)
            alpha[1:-1]-=np.linalg.solve(B[:,1:-1],r)
        require(np.max(abs((residual(alpha)-base+math.pi)%(2*math.pi)-math.pi))<2e-12,'reflection solve residual')
    return alpha

def physical():
    rng=np.random.default_rng(2026292293);rows=[]
    # All words below are actual first-hit billiard trajectories.
    for case in range(36):
        R=[.45,.46,.47][case%3];m=[1,2,3,5,8,16][case%6]
        alpha=float(rng.uniform(-math.pi,math.pi));p=float(rng.uniform(-.85,.85))
        o=old.trace(alpha,p,R,m);r=float(Q0)**.25
        eps=min(.25,min(c/r**min(i,m-i) for i,c in enumerate(o['incidences'])),
                        min(c/r**min(i,m-1-i) for i,c in enumerate(o['clearances'])))/2
        require(eps>0,'positive true guard margin')
        h=float(DELTA)*eps*np.array([.21,-.17]);a=solve(o,h)
        require(old.physical_valid(R,o['centers'],a),'all unvisited obstacles / first-hit order')
        cs,cl,ts,_=old.observables(R,o['centers'],a)
        require(min(cs[i]/(eps*r**min(i,m-i)) for i in range(m+1))>=.5-1e-8,'all incidence half margins')
        require(min(cl[i]/(eps*r**min(i,m-1-i)) for i in range(m))>=.5-1e-8,'all third-disk half margins')
        increments=(a-o['angles']+math.pi)%(2*math.pi)-math.pi
        weighted=sum(float(LAM)**min(i,m-i)*abs(increments[i]) for i in range(m+1))
        require(weighted<=float(P)*sum(abs(h))+2e-11,'weighted analytic displacement')
        data=old.action(R,o['centers'],a);mom=[float(data[7][0]@data[6][0])]+[float(data[7][i-1]@data[6][i]) for i in range(1,m+1)]
        # Endpoint momenta from first variation use terminal incoming tangential component.
        visits=int(sum(old.section(a[i],mom[i],R) for i in range(m)))
        rows.append({'case':case,'R':R,'m':m,'epsilon':eps,'endpoint_increment':h.tolist(),
             'all_incidence_margins':cs.tolist(),'all_unvisited_clearances':cl.tolist(),
             'reference_exact_record':{'return_count':o['return_count'],'displacement':o['displacement_label'],
                'collision_count':m,'physical_roof':o['physical_roof'],'initial_section':o['initial_section'],'terminal_section':o['terminal_section']},
             'continued_physical_roof':float(sum(ts)),'continued_return_count':visits,
             'word':o['word'],'weighted_displacement':weighted})
    # Actual normal two-disk reversing orbits give controlled critical centers.
    critical=[];beta=float(old.SIG)/float(Q0)**.25
    D=8*float(old.CC)/(1-beta)+4*float(A*old.J)/(1-float(old.SIG))+4*float(old.CF)/float(G)
    for R in [.45,.46,.47]:
        for m in [1,2,3,4,8,16,32]:
            o=old.trace(0.,0.,R,m);eps=.1;rho=min(.25,float(G*DELTA)*eps/(4*float(RP)))
            q=np.zeros(2);z=rho*np.array([.32,.24]);a=o['angles'].copy()
            for _ in range(6):
                a=solve(o,q);data=old.action(R,o['centers'],a)
                e=data[1][[0,m]]-R*np.array([-z[0],z[1]])
                if np.linalg.norm(e)<4e-14:break
                q-=np.linalg.solve(data[3],e)
            require(old.physical_valid(R,o['centers'],a),'critical common momentum disk physical')
            require(np.linalg.norm(q)<=float(RP/G)*np.linalg.norm(z)+2e-12,'strong convexity inverse distance')
            # Positive optical denominator rather than subtractive small mixed entries.
            def logu(angles):
                data=old.action(R,o['centers'],angles);cs,cl,ts,e_over_R=old.observables(R,o['centers'],angles)
                return math.log(R*R*e_over_R)-math.log(float(np.linalg.det(data[3])))
            variation=abs(logu(a)-logu(o['angles']))
            require(variation<=D*np.max(abs(q))/eps+1e-9,'relative physical optical distortion')
            critical.append({'R':R,'m':m,'epsilon':eps,'rho':rho,'target_momenta':z.tolist(),
              'endpoint_increment':q.tolist(),'log_inverse_weight_change':variation,
              'critical_physical_roof':o['physical_roof'],'continued_physical_roof':data[0],
              'scope':'finite actual reversing trajectory; long-time normalized root abundance not tested'})
    return rows,critical,{'actual_nonspecial_trajectories':len(rows),'actual_critical_trajectories':len(critical),
        'uniform_log_distortion_bound':D*float(DELTA)/2,'continuation_checks':'passed',
        'floating_checks_prove_continuum_or_raw_LLT':False}

def different_radii():
    # Deliberately labelled algebraic coarea check; not a replacement physical model.
    rows=[];origins=[F(0),F(1,16),F(1,8)];weights=[F(1,3),F(1,5),F(1,7)]
    hs=[F(1,2),F(3,4),F(1)];t=F(1,4);Utest=F(2)
    total=F(0)
    for a,u,h in zip(origins,weights,hs):
        r2=2*(t-a)/h;require(r2>0,'positive distinct radial inverse')
        total+=u/h;rows.append({'critical_roof':str(a),'u':str(u),'h':str(h),'radius_squared':str(r2)})
    require(len(set(row['radius_squared'] for row in rows))==3,'different radii not synchronized')
    require(total<=Utest*sum(weights),'common roof comparison with angle factor unabsorbed')
    return {'scope':'exact algebraic substitution test, NOT a triangular billiard or Markov model',
        'cases':rows,'sum_u_over_h':str(total),'common_upper_bound':str(Utest*sum(weights))}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--details',type=Path);args=parser.parse_args()
    ex=exact();rows,critical,p=physical();alg=different_radii()
    details={'exact':ex,'physical_trajectories':rows,'physical_critical_trajectories':critical,'different_radius_algebra':alg}
    if args.details:args.details.parent.mkdir(parents=True,exist_ok=True);args.details.write_text(json.dumps(details,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'passed','exact':ex,'physical':p,'different_radius_algebra':'passed',
        'full_raw_pointwise_LLT_proved':False,'complete_normalized_clearance_source_proved':False},sort_keys=True,indent=2))
if __name__=='__main__':main()
