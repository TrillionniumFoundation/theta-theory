#!/usr/bin/env python3
"""Exact finite algebra and genuine first-hit billiard checks for modules 294--295.
Finite diagnostics are not a continuum proof, a fixed-radius LLT, or a root-sum certificate.
"""
from __future__ import annotations
import argparse,json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp
import check_endpoint_localization as old
from check_reflection_resolvent import solve_tri

H=F(28,5);OM=F(179,400);RM=F(9,20);RP=F(47,100);TM=F(3,50)
GAM=(RM-OM)/(2*H);LAM=F(50,47);CB=2*(1+2/(LAM-1));LR=4/TM
KR=48/TM+512/TM**2;SR=min(F(1,8),TM/24);RR=min(SR,1/(8*CB*KR))
ER=RR/(8*(1+CB*LR));DR=CB*LR;CR=DR+(2+2*RP*DR)/TM;KAP=2*GAM/94

def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def exact():
    widths=[F(961,4804),F(13697401,73866304),F(529,3136),F(75,448)]
    require(all(x<=widths[0]<OM**2<RM**2 for x in widths),'strict buffered covering')
    require(F(3847,124)<H**2,'strict foot interior')
    require(94*TM>H and GAM==F(1,4480) and GAM/93==F(1,416640),'collision block indexing')
    require(CB==F(194,3) and DR==F(38800,9) and KAP==F(1,210560),'exact inverse/clock constants')
    require(6*SR<=TM/4 and CB*KR*RR<=F(1,8),'complex domain and contraction')
    require(CB*LR*ER<=RR/8,'radius forcing')
    require(CB*KR*(ER+RR/2)**2/2<=RR/16,'invariant-ball nonlinear remainder')
    require(CB*KR*(ER+RR/2)<=F(1,8),'full-ball Lipschitz bound')
    for m in range(1,10001):require(2+2*GAM*(m//94)>=KAP*m,'all-count linear slope conversion')
    count=0;entries=0;row_counterexample=False;zero_cases=0
    for m in [1,2,3,6,12]:
      for variant in range(10):
        cs=[F(1)]+[[F(0),F(1,10**30),F(1,2),F(1)][(i+variant)%4] for i in range(1,m)]+[F(1)]
        
        if variant>=5:
            cs[0]=[F(0),F(4,5),F(1,10**30)][variant%3]
            cs[-1]=[F(1,10**30),F(0),F(3,5)][variant%3]
        ts=[TM+F((i+variant)%4,7) for i in range(m)];w=[1/t for t in ts]
        d=[(1 if i in [0,m] else 2)+RP*cs[i]*((w[i-1] if i else 0)+(w[i] if i<m else 0)) for i in range(m+1)]
        lo=[RP*w[i]*cs[i] for i in range(m)];up=[RP*w[i]*cs[i+1] for i in range(m)]
        inv=[]
        for j in range(m+1):
            v=solve_tri(d,lo,up,[F(int(i==j)) for i in range(m+1)]);inv.append(v)
            require(sum(map(abs,v))<=1,'full inverse column norm')
            require(sum(LAM**abs(i-j)*abs(x) for i,x in enumerate(v))<=2,'full weighted inverse column')
            for i,x in enumerate(v):
                y=d[i]*x+(lo[i-1]*v[i-1] if i else 0)+(up[i]*v[i+1] if i<m else 0)
                require(y==int(i==j),'exact inverse identity');entries+=1
                require((-1)**(i+j)*x>=0,'alternating positive inverse')
        for i in range(m+1):
            require(sum(abs(inv[j][i]) for j in range(m+1))<=CB,'full inverse row bound')
            off=(abs(lo[i-1]) if i else 0)+(abs(up[i]) if i<m else 0)
            row_counterexample|=off>d[i]
        zero_cases+=int(F(0) in cs);count+=1
    require(row_counterexample and zero_cases>0,'negative control for false row dominance')
    # General telescoping of the physical radius boundary factors, not a numeric sign guess.
    for m in range(1,12):
        c=sp.symbols('c0:'+str(m+1))
        require(sp.expand(sum(-c[i]-c[i+1] for i in range(m))+c[0]+c[-1]+2*sum(c[1:-1]))==0,'boundary coefficient telescope')
    return dict(constants={k:str(v) for k,v in dict(H=H,omega=OM,gamma=GAM,kappa=KAP,lambda_=LAM,C_B=CB,L_R=LR,K_R=KR,s_R=SR,r_R=RR,eta_R=ER,D_R=DR,C_cR=CR).items()},
        rational_full_matrices=count,exact_inverse_entries=entries,simultaneous_zero_incidence_cases=zero_cases,
        false_row_dominance_negative_control=True,integer_slope_cases=10000,
        scope='exact finite arithmetic and matrix diagnostics; the test arrays are not claimed to be billiard words')

def actual_bending():
    rng=np.random.default_rng(20261016294);records=[]
    for R in [.45,.46,.47]:
      for m in [94,188,282]:
       for rep in range(2):
        o=old.trace(float(rng.uniform(-math.pi,math.pi)),float(rng.uniform(-.9,.9)),R,m)
        cs=np.asarray(o['incidences']);ts=np.asarray(o['flights']);ang=o['angles']
        n=np.column_stack((np.cos(ang),np.sin(ang)));points=o['centers']+R*n
        velocities=np.diff(points,axis=0)/ts[:,None];checks=[]
        for start in range(0,m-93,94):
            s=float(sum(cs[start+1:start+94]));require(s>=float(GAM),'actual complete block bending')
            require(max(cs[start+1:start+94])>=float(GAM/93),'actual moderately transverse collision')
            v=velocities[start];q=points[start];relative=old.CEN+o['centers'][start]-q
            foot=relative@v;perp=np.linalg.norm(relative-np.outer(foot,v),axis=1)
            mask=(foot>0)&(foot<float(H));idx=int(np.argmin(np.where(mask,perp,np.inf)))
            require(perp[idx]<float(OM),'actual line buffered covering')
            t=float(foot[idx]);cum=np.concatenate(([0.],np.cumsum(ts[start:start+94])))
            j=int(np.searchsorted(cum,t,side='right')-1);pos=points[start+j]+(t-cum[j])*velocities[start+j]
            dev=float(np.linalg.norm(pos-q-t*v));sumc=float(sum(cs[start+1:start+j+1]))
            require(dev<=2*float(H)*sumc+2e-8,'exact polygon-jump upper bound')
            require(np.linalg.norm(pos-(old.CEN[idx]+o['centers'][start]))>=R-2e-8,'actual physical nonpenetration')
            checks.append({'first_collision':start,'sum_incidence':s,'line_cover_distance':float(perp[idx]),'foot_time':t,'polygon_deviation':dev})
        records.append({'R':R,'m':m,'word':o['word'],'initial_alpha':float(ang[0]),'initial_p':float(o['momenta'][0]),
          'physical_roof':o['physical_roof'],'return_count':o['return_count'],'initial_section':o['initial_section'],'terminal_section':o['terminal_section'],
          'displacement_label':o['displacement_label'],'minimum_incidence':float(min(cs)),'minimum_clearance':float(min(o['clearances'])),'blocks':checks})
    return records

def normal_system(R,centers,angles):
    z=centers[:,0]+1j*centers[:,1];n=np.exp(1j*angles);X=np.diff(z+R*n);N=len(angles)
    th=np.angle(X);D=np.zeros((N-1,N));tr=np.imag(np.diff(n)/X)
    for i in range(N-1):
        D[i,i]=np.imag(-1j*R*n[i]/X[i]);D[i,i+1]=np.imag(1j*R*n[i+1]/X[i])
    E=np.empty(N);B=np.zeros((N,N));bR=np.empty(N)
    E[0]=angles[0]-th[0];E[-1]=angles[-1]-th[-1]-math.pi
    B[0]=-D[0];B[0,0]+=1;B[-1]=-D[-1];B[-1,-1]+=1;bR[0]=-tr[0];bR[-1]=-tr[-1]
    if N>2:
        E[1:-1]=2*angles[1:-1]-th[:-1]-th[1:]-math.pi
        B[1:-1]=-(D[:-1]+D[1:]);B[np.arange(1,N-1),np.arange(1,N-1)]+=2
        bR[1:-1]=-tr[:-1]-tr[1:]
    E=(E+math.pi)%(2*math.pi)-math.pi
    return E,B,bR

def solve_normal(R,centers,angles):
    a=np.array(angles,dtype=float,copy=True)
    for _ in range(32):
        E,B,_=normal_system(R,centers,a);err=float(max(abs(E)))
        if err<8e-13:return a
        step=np.linalg.solve(B,E);accepted=False
        for power in range(12):
            nxt=a-step/2**power
            if max(abs(normal_system(R,centers,nxt)[0]))<err:
                a=nxt;accepted=True;break
        if not accepted:break
    require(max(abs(normal_system(R,centers,a)[0]))<3e-10,'normal-boundary Newton did not converge')
    return a

def critical_checks():
    rng=np.random.default_rng(20261016295);rows=[];trials=[];seen=set()
    candidates=[]
    for R in [.451,.46,.469]:
      for m in [1,2,3,4,8,16,32]:candidates.append(('normal-bounce',old.trace(0.,0.,R,m)))
    for R in [.455,.46,.465]:
      for m in [2,3,5,8,12]:
       for i in range(10):
        alpha=float(rng.uniform(-math.pi,math.pi));candidates.append(('search',old.trace(alpha,0.,R,m)))
    for source,o in candidates:
        R=o['R'];m=o['m'];centers=o['centers']
        trial={'R':R,'m':m,'source':source,'word':o['word'],'initial_alpha':float(o['angles'][0])}
        try:a=solve_normal(R,centers,o['angles'])
        except (RuntimeError,np.linalg.LinAlgError) as exc:
            trial.update(status='not_accepted',reason=str(exc));trials.append(trial);continue
        if not old.physical_valid(R,centers,a):
            trial.update(status='not_accepted',reason='formal root is not a physical first-hit record');trials.append(trial);continue
        key=(R,tuple(tuple(z) for z in o['word']))
        if key in seen:
            trial.update(status='duplicate',reason='same radius and word already checked');trials.append(trial);continue
        seen.add(key);E,B,bR=normal_system(R,centers,a);ap=-np.linalg.solve(B,bR)
        data=old.action(R,centers,a);cs,cls,ts,_=old.observables(R,centers,a)
        require(max(abs(E))<3e-10 and abs(cs[0]-1)<2e-10 and abs(cs[-1]-1)<2e-10,'true normal endpoints')
        w=1/ts;BM=np.zeros_like(B)
        for i in range(m+1):
            BM[i,i]=(1 if i in [0,m] else 2)+R*cs[i]*((w[i-1] if i else 0)+(w[i] if i<m else 0))
            if i<m:BM[i,i+1]=R*w[i]*cs[i+1];BM[i+1,i]=R*w[i]*cs[i]
        require(np.max(abs(B-BM))<2e-8,'full physical reflection matrix incl boundary rows')
        require(max(abs(ap))<=float(DR)+1e-7,'physical implicit radius response')
        derivative=-2.-2*float(sum(cs[1:-1]));direct=float(sum(data[7][i]@(data[5][i+1]-data[5][i]) for i in range(m)))
        require(abs(direct-derivative)<2e-8,'envelope boundary coefficients and signs')
        require(float(KAP)*m<=-derivative<=2*m+1e-8,'actual normalized physical-clock slope')
        h=2e-6
        for _ in range(10):
            plus=solve_normal(R+h,centers,a);minus=solve_normal(R-h,centers,a)
            if old.physical_valid(R+h,centers,plus) and old.physical_valid(R-h,centers,minus):break
            h/=2
        else:raise RuntimeError('no tested two-sided physical interval')
        dp=old.action(R+h,centers,plus);dm=old.action(R-h,centers,minus)
        fd=(dp[0]-dm[0])/(2*h);aderr=float(max(abs((plus-minus)/(2*h)-ap)))
        require(abs(fd-derivative)<3e-5*m and aderr<3e-4,'actual radius finite difference of clock and full angle lift')
        # Differentiate true unit velocities to check second variation separately.
        n,t,v= data[5:8];dx=np.diff(n+R*t*ap[:,None],axis=0)
        dv=(dx-v*np.sum(v*dx,axis=1)[:,None])/ts[:,None]
        dc=np.array([-dv[i-1]@n[i]-v[i-1]@t[i]*ap[i] for i in range(1,m)])
        second=-2*float(sum(dc));cp=old.observables(R+h,centers,plus)[0];cm=old.observables(R-h,centers,minus)[0]
        secondfd=-2*float(sum(cp[1:-1]-cm[1:-1]))/(2*h)
        require(abs(second-secondfd)<5e-4*m,'physical second clock variation')
        require(abs(second)<=2*m*float(CR),'second-derivative uniform constant')
        def labels(r,aa,dd):
            tang=dd[6];vel=dd[7];pp=[float(vel[i]@tang[i]) for i in range(m)]+[float(vel[-1]@tang[-1])]
            return dict(return_count=sum(old.section(float(x),p,r) for x,p in zip(aa[:-1],pp[:-1])),
                        initial_section=old.section(float(aa[0]),pp[0],r),terminal_section=old.section(float(aa[-1]),pp[-1],r),displacement_label=o['displacement_label'])
        rows.append(dict(R=R,m=m,word=o['word'],angles=a.tolist(),minimum_incidence=float(min(cs)),minimum_clearance=float(min(cls)),physical_roof=data[0],
                    clock_derivative=derivative,clock_second_derivative=second,radius_step=h,clock_fd_error=abs(fd-derivative),angle_fd_max_error=aderr,
                    second_fd_error=abs(second-secondfd),implicit_angle_derivative=ap.tolist(),original_labels=labels(R,a,data),
                    plus_labels=labels(R+h,plus,dp),minus_labels=labels(R-h,minus,dm),source=source))
        trial.update(status='accepted');trials.append(trial)
    nonnormal=sum(r['minimum_incidence']<.99 for r in rows)
    require(nonnormal>=10,'insufficient nonspecial physical critical roots')
    return rows,trials


def solve_momenta(R,centers,angles,a0,vm):
    a=np.array(angles,dtype=float,copy=True)
    def residual(aa):
        E,B,bR=normal_system(R,centers,aa)
        E[0]+=math.asin(a0);E[-1]-=math.asin(vm)
        E=(E+math.pi)%(2*math.pi)-math.pi
        return E,B,bR
    for _ in range(32):
        E,B,_=residual(a);err=float(max(abs(E)))
        if err<8e-13:return a
        step=np.linalg.solve(B,E)
        for power in range(12):
            nxt=a-step/2**power
            if max(abs(residual(nxt)[0]))<err:a=nxt;break
        else:break
    require(max(abs(residual(a)[0]))<3e-10,'fixed-momentum Newton convergence')
    return a

def complete_records():
    rng=np.random.default_rng(20261016296);rows=[]
    for R in [.451,.46,.469]:
      for m in [1,2,5,16,64]:
       for rep in range(2):
        o=old.trace(float(rng.uniform(-math.pi,math.pi)),float(rng.uniform(-.9,.9)),R,m)
        a=o['angles'];centers=o['centers'];p0=o['momenta'][0];pm=o['momenta'][-1]
        E,B,bR=normal_system(R,centers,a);ap=-np.linalg.solve(B,bR)
        d=old.action(R,centers,a);cs=np.asarray(o['incidences']);w=1/np.asarray(o['flights']);formula=np.zeros_like(B)
        for i in range(m+1):
            formula[i,i]=(1 if i in [0,m] else 2)+R*cs[i]*((w[i-1] if i else 0)+(w[i] if i<m else 0))
            if i<m:formula[i,i+1]=R*w[i]*cs[i+1];formula[i+1,i]=R*w[i]*cs[i]
        require(np.max(abs(B-formula))<5e-8,'noncritical full endpoint-cosine matrix')
        require(max(abs(ap))<=float(DR),'noncritical full radius response')
        explicit=-cs[0]-cs[-1]-2*sum(cs[1:-1]);work=R*(-p0*ap[0]+pm*ap[-1]);total=explicit+work
        direct=sum(d[7][i]@(d[5][i+1]-d[5][i]) for i in range(m))+d[1]@ap
        require(abs(direct-total)<5e-8*m,'noncritical physical clock incl endpoint work')
        loss=float(2*RP*DR+2*GAM);require(float(KAP)*m-loss<=-total<=2*m+float(2*RP*DR),'all-count slope with bounded loss')
        h=1e-6
        for _ in range(12):
            plus=solve_momenta(R+h,centers,a,p0,pm);minus=solve_momenta(R-h,centers,a,p0,pm)
            if old.physical_valid(R+h,centers,plus) and old.physical_valid(R-h,centers,minus):break
            h/=2
        else:raise RuntimeError('noncritical tested continuation not physical')
        dp=old.action(R+h,centers,plus);dm=old.action(R-h,centers,minus);fd=(dp[0]-dm[0])/(2*h)
        require(abs(fd-total)<5e-5*m,'noncritical radius clock finite difference')
        require(max(abs((plus-minus)/(2*h)-ap))<8e-4,'noncritical radius full lift finite difference')
        require(abs(dp[7][0]@dp[6][0]-p0)<2e-9 and abs(dp[7][-1]@dp[6][-1]-pm)<2e-9,'prescribed momenta really fixed')
        rows.append(dict(R=R,m=m,word=o['word'],physical_roof=o['physical_roof'],return_count=o['return_count'],
         displacement_label=o['displacement_label'],initial_section=o['initial_section'],terminal_section=o['terminal_section'],
         fixed_p0=p0,fixed_pm=pm,explicit_radius_term=float(explicit),endpoint_work=float(work),full_clock_derivative=float(total),
         clock_fd_error=float(abs(fd-total)),radius_step=h,angles=a.tolist(),angle_radius_derivative=ap.tolist()))
    require(max(abs(row['endpoint_work']) for row in rows)>.01,'missing endpoint work negative control')
    vr,va,vp,l=sp.symbols('vr va vp l',nonzero=True)
    first=sp.Matrix([[1,0,0],[0,0,1],[vr,va,vp]])
    require(first.det()==-va and sp.diag(l,1,1).det()==l,'complete source radius-roof Jacobian orientation')
    threshold=(2*(2*RP*DR+2*GAM)/KAP).__ceil__()
    require(F(KAP)*threshold>=2*(2*RP*DR+2*GAM),'exact all-record transversality threshold')
    return rows,threshold

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--details',type=Path);args=parser.parse_args()
    rational=exact();bending=actual_bending();critical,trials=critical_checks();complete,threshold=complete_records()
    details={'exact':rational,'actual_bending_records':bending,'actual_critical_radius_records':critical,'all_critical_search_trials':trials,'complete_noncritical_records':complete,'all_record_theoretical_m0':threshold,
             'scope':'finite actual first-hit trajectories and exact algebra only; no claim of continuum proof or fixed-radius raw LLT'}
    if args.details:args.details.parent.mkdir(parents=True,exist_ok=True);args.details.write_text(json.dumps(details,sort_keys=True,indent=2)+'\n')
    result={'status':'passed','exact':rational,'actual_bending_records':len(bending),'complete_94_flight_blocks':sum(len(r['blocks']) for r in bending),
            'actual_critical_continuations':len(critical),'nonspecial_critical_continuations':sum(r['minimum_incidence']<.99 for r in critical),
            'recorded_critical_search_trials':len(trials),'complete_noncritical_records':len(complete),'theoretical_m0_not_simulated':threshold,'maximum_missing_endpoint_work':max(abs(r['endpoint_work']) for r in complete),'maximum_clock_fd_error':max(r['clock_fd_error'] for r in critical),
            'full_raw_pointwise_LLT_proved':False,'formal_proof_certificate':False}
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
