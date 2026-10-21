#!/usr/bin/env python3
"""Supplementary exact algebra and actual first-hit diagnostics for 297--299.
The convex comparison variables are NOT claimed to be physical trajectories.
Finite calculations do not prove continuum theorems or the original raw LLT.
"""
from __future__ import annotations
import argparse,json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import minimize
import check_endpoint_localization as old
import check_critical_clock as clock

def require(ok,msg):
    if not ok: raise RuntimeError(msg)

def vectors(Y):
    e=np.diff(Y,axis=0); lens=np.linalg.norm(e,axis=1)
    require(np.all(lens>0),'zero comparison edge')
    v=e/lens[:,None];d=np.vstack((-v[0],v[:-1]-v[1:],v[-1]))
    return lens,v,d

def dual(centers,R,v):
    d=np.vstack((-v[0],v[:-1]-v[1:],v[-1]))
    T=float(np.linalg.norm(d,axis=1).sum())
    C=float(np.sum(v*np.diff(centers,axis=0)))
    return C-R*T,T,d

def gap(centers,R,Y,v):
    dvalue,T,d=dual(centers,R,v)
    e=np.diff(Y,axis=0)
    flights=np.linalg.norm(e,axis=1)-np.sum(v*e,axis=1)
    contacts=np.sum(d*(Y-centers),axis=1)+R*np.linalg.norm(d,axis=1)
    L=float(np.linalg.norm(e,axis=1).sum())
    return L-dvalue,flights,contacts

def solve_comparison(centers,R,start):
    """A constrained numerical minimizer with explicit primal/dual gap reporting."""
    N=len(centers)
    def fun(z):
        Y=centers+R*z.reshape(N,2)
        lens,_,d=vectors(Y)
        return float(lens.sum()),(R*d).ravel()
    def con(z):return 1.-np.sum(z.reshape(N,2)**2,axis=1)
    def con_jac(z):
        out=np.zeros((N,2*N));a=z.reshape(N,2)
        for i in range(N):out[i,2*i:2*i+2]=-2*a[i]
        return out
    z0=(start-centers)/R;z0=z0/np.maximum(1.,np.linalg.norm(z0,axis=1))[:,None]
    res=minimize(fun,z0.ravel(),jac=True,method='SLSQP',constraints=[{'type':'ineq','fun':con,'jac':con_jac}],
                 options={'ftol':2e-12,'maxiter':500})
    # Projection makes the reported primal feasible; its dual uses feasible unit vectors.
    zz=res.x.reshape(N,2);zz=zz/np.maximum(1.,np.linalg.norm(zz,axis=1))[:,None]
    Y=centers+R*zz;lens,v,d=vectors(Y);D,T,_=dual(centers,R,v)
    gapvalue=float(lens.sum()-D)
    require(gapvalue>=-2e-9 and np.max(np.linalg.norm(zz,axis=1))<=1.+5e-15,'numerical primal-dual feasibility')
    require(gapvalue<2e-7*N,'comparison solver insufficient primal-dual certificate')
    return Y,dict(solver_success=bool(res.success),solver_message=str(res.message),iterations=int(res.nit),
       primal_upper=float(lens.sum()),dual_lower=D,primal_dual_gap=gapvalue,
       T=T,comparison_is_physical=False,comparison_points=Y.tolist(),dual_velocities=v.tolist())

def exact():
    symbolic=0
    for m in range(1,10):
        q=sp.symbols('q0:'+str(m+1));o=sp.symbols('o0:'+str(m+1));v=sp.symbols('v0:'+str(m))
        d=[-v[0]]+[v[i-1]-v[i] for i in range(1,m)]+[v[-1]]
        require(sp.expand(sum(v[i]*(q[i+1]-q[i]) for i in range(m))-sum(d[i]*q[i] for i in range(m+1)))==0,'exact open-word telescope')
        require(sp.expand(sum(v[i]*(o[i+1]-o[i]) for i in range(m))-sum(d[i]*o[i] for i in range(m+1)))==0,'exact center telescope')
        symbolic+=2
    for p,c in [(F(0),F(1)),(F(3,5),F(4,5)),(F(5,13),F(12,13)),(F(8,17),F(15,17))]:
        require(p*p+c*c==1 and 1-c==p*p/(1+c),'exact endpoint deficit')
    R=F(23,50)
    require(2-2*R==(1-2*R)+(1-2*R)+2*R,'straight-block positive junction penalty')
    require(2-4*R==(1-2*R)+(1-2*R),'normal reversal zero junction penalty')
    # The naive zero-endpoint/cyclic penalty would incorrectly claim length 1.
    require(1-2*R!=1,'negative control for dropped open endpoint penalties')
    require(F(1,2)/(F(91,10000)*F(1,1))>0,'positive single section factor')
    return dict(symbolic_telescope_cases=symbolic,exact_endpoint_cases=4,
        junction_controls=2,missing_endpoint_negative_control=True,
        all_record_bending_threshold=int(sp.ceiling(64*sp.Rational(47,100)/(sp.Rational(3,50)*sp.Rational(1,210560)**2))),
        large_count_threshold_simulated=False,
        scope='finite exact identities only; arbitrary algebraic arrays are not called physical records')

def actual_records():
    rng=np.random.default_rng(20261016297);rows=[]
    for R in [.45,.46,.47]:
      for m in [1,2,3,5,8,12,24]:
       for rep in range(2):
        o=old.trace(float(rng.uniform(-math.pi,math.pi)),float(rng.uniform(-.93,.93)),R,m)
        centers=o['centers'];aa=np.asarray(o['angles']);Q=centers+R*np.column_stack((np.cos(aa),np.sin(aa)))
        lens,v,d=vectors(Q);L=float(lens.sum());cs=np.asarray(o['incidences']);E=R*(2-cs[0]-cs[-1]);D,T,_=dual(centers,R,v)
        gg,ff,cc=gap(centers,R,Q,v)
        require(np.max(abs(ff))<3e-12 and min(cc)>-1e-9 and abs(gg-E)<2e-8*m,'physical endpoint-only exact gap')
        require(np.max(abs(cc[1:-1]))<2e-8 if m>1 else True,'no hidden internal contact penalty')
        Y,opt=solve_comparison(centers,R,Q);eps=max(0.,opt['primal_dual_gap'])
        require(opt['dual_lower']<=L+2e-8*m and L-opt['dual_lower']<=E+eps+2e-8*m,'global endpoint enclosure bracket')
        # Approximate minimizer: include its certified primal-dual error explicitly.
        EE=max(E+eps,0.);deltas=np.full(m+1,2*math.sqrt(2*R*EE))
        if m>1:deltas[1:-1]=np.sqrt(R*EE/cs[1:-1])
        displacement=np.linalg.norm(Y-Q,axis=1)
        require(np.all(displacement<=deltas+4e-6),'quantitative competitor contact bounds with solver error')
        lensY,vY,dY=vectors(Y)
        boundary=np.linalg.norm(Y-centers,axis=1)
        physical=bool(np.max(abs(boundary-R))<2e-7 and old.physical_valid(R,centers,np.arctan2((Y-centers)[:,1],(Y-centers)[:,0])))
        opt['comparison_is_physical']=physical
        velocity_energy=float(.5*np.sum(lensY*np.sum((vY-v)**2,axis=1)))
        require(velocity_energy<=E+eps+2e-8*m,'complete physical-to-minimizing velocity energy')
        physical_turn=2+2*float(sum(cs[1:-1]));turn_loss=2*math.sqrt(2*m*max(E+eps,0.)/float(clock.TM))
        require(opt['T']>=physical_turn-turn_loss-3e-8*m,'complete bending transfer without physical minimizer')
        opt['physical_velocity_energy']=velocity_energy
        opt['physical_turn']=physical_turn
        opt['turn_loss_bound_with_solver_error']=turn_loss
        # Test distance/Hausdorff bound against the full proved finite search domain;
        # the theorem itself is for all centers and has no truncation.
        min_margin=math.inf
        for i in range(m):
            Z=old.CEN+centers[i]
            def distance(A,B):
                e=B-A;t=np.clip((Z-A)@e/float(e@e),0.,1.)
                return np.linalg.norm(Z-A-t[:,None]*e,axis=1)
            margin=distance(Y[i],Y[i+1])-distance(Q[i],Q[i+1])+max(displacement[i],displacement[i+1])
            min_margin=min(min_margin,float(min(margin)))
        require(min_margin>=-2e-9,'all tested lattice distance inequalities')
        rows.append(dict(R=R,m=m,word=o['word'],initial_alpha=float(aa[0]),initial_p=float(o['momenta'][0]),
          physical_roof=L,physical_points=Q.tolist(),incidences=cs.tolist(),clearances=list(map(float,o['clearances'])),
          initial_section=o['initial_section'],terminal_section=o['terminal_section'],return_count=o['return_count'],displacement_label=o['displacement_label'],
          physical_dual=D,endpoint_deficit=E,endpoint_identity_error=abs(L-D-E),
          comparison=opt,competitor_displacements=displacement.tolist(),competitor_bounds_with_optimization_error=deltas.tolist(),distance_min_margin=min_margin))
    return rows

def actual_critical():
    oldrows,trials=clock.critical_checks();rows=[];curvatures=[];radius_tests=[]
    for x in oldrows:
        R=x['R'];m=x['m'];word=np.array(x['word']);a=np.asarray(x['angles'])
        inc=np.column_stack((word[:,0]+.5*word[:,1],math.sqrt(3.)*.5*word[:,1]))
        centers=np.vstack((np.zeros(2),np.cumsum(inc,axis=0)))
        require(old.physical_valid(R,centers,a),'reconstructed actual critical word')
        data=old.action(R,centers,a);cs,cls,ts,_=old.observables(R,centers,a)
        residual,B,bR=clock.normal_system(R,centers,a);ap=-np.linalg.solve(B,bR)
        n,t,v=data[5:8];Q=centers+R*n;Qp=n+R*t*ap[:,None];dx=np.diff(Qp,axis=0)
        projection=dx-v*np.sum(v*dx,axis=1)[:,None]
        lam=np.concatenate(([1.],2*cs[1:-1],[1.]))
        flight=float(np.sum(np.sum(projection**2,axis=1)/ts));contact=float(R*np.sum(lam*ap**2));energy=flight+contact
        dc=np.array([-projection[i-1]@n[i]/ts[i-1]-v[i-1]@t[i]*ap[i] for i in range(1,m)])
        second=-2*float(sum(dc));require(abs(second-energy)<3e-7*m,'positive physical shape energy, sign and endpoint weights')
        D,T,d=dual(centers,R,v);require(abs(D-data[0])<3e-9*m,'true critical global dual equality')
        require(abs(T-2-2*sum(cs[1:-1]))<3e-8,'critical support slope')
        nonspecial=min(cs)<.99
        require(energy>1e-8 if nonspecial else energy>=0,'critical positive energy or normal zero energy')
        if x['source']=='normal-bounce':require(energy<1e-18,'normal bouncing zero energy')
        # Genuine physical continuation on a wider checked radius interval.
        rs=[]
        for rr in [R-1e-4,R,R+1e-4]:
            if not .45<=rr<=.47:continue
            ar=clock.solve_normal(rr,centers,a)
            if not old.physical_valid(rr,centers,ar):continue
            dr=old.action(rr,centers,ar);DV,TV,_=dual(centers,rr,dr[7])
            rs.append((rr,dr[0],TV))
        for r1,l1,t1 in rs:
          for r2,l2,t2 in rs:
           if r2>r1:
            diff=l1-l2;step=r2-r1
            require(t2*step-3e-9*m<=diff<=t1*step+3e-9*m,'global affine supports in radius')
            require(float(clock.KAP)*m*step<=diff+3e-9*m<=2*m*step+6e-9*m,'physical global slope comparison')
            radius_tests.append(dict(R1=r1,R2=r2,m=m,word=x['word'],roof_difference=diff,lower_support=t2*step,upper_support=t1*step))
        rows.append({**x,'global_dual':D,'flight_shape_energy':flight,'contact_shape_energy':contact,'total_shape_energy':energy,'independent_second_derivative':second,'shape_energy_error':abs(energy-second)})
        curvatures.append(energy)
    return rows,trials,radius_tests

def physical_certificates(critical_rows):
    rows=[];accepted=0
    # Tiny but nonzero endpoint perturbations are genuine reflected trajectories,
    # not a claimed common physical tube for arbitrary words.
    for x in [x for x in critical_rows if x['minimum_incidence']<.99][:18]:
        R=x['R'];m=x['m'];word=np.array(x['word']);a=np.array(x['angles'])
        inc=np.column_stack((word[:,0]+.5*word[:,1],math.sqrt(3.)*.5*word[:,1]));centers=np.vstack((np.zeros(2),np.cumsum(inc,axis=0)))
        ncrit=np.column_stack((np.cos(a),np.sin(a)));Y=centers+R*ncrit
        for amp in [1e-5,3e-4,2e-2]:
            aa=clock.solve_momenta(R,centers,a,amp,-amp*.7)
            if not old.physical_valid(R,centers,aa):
                rows.append(dict(R=R,m=m,word=x['word'],amplitude=amp,status='not_physical_no_assertion'));continue
            data=old.action(R,centers,aa);cs,cls,ts,_=old.observables(R,centers,aa);Q=centers+R*data[5]
            E=R*(2-cs[0]-cs[-1]);ds=np.full(m+1,2*math.sqrt(max(0.,2*R*E)))
            if m>1:ds[1:-1]=np.sqrt(max(0.,R*E)/cs[1:-1])
            require(np.all(np.linalg.norm(Y-Q,axis=1)<=ds+8e-8),'true critical center quantitative proximity')
            clearance=bool(np.all(cls>np.maximum(ds[:-1],ds[1:])))
            incidence=bool(np.all(cs[1:-1]>(ds[:-2]+2*ds[1:-1]+ds[2:])/float(clock.TM)))
            passes=clearance and incidence;accepted+=int(passes)
            if passes:require(old.physical_valid(R,centers,a),'certified critical center is actual first hit')
            rows.append(dict(R=R,m=m,word=x['word'],amplitude=amp,status='actual_physical_record_retained',
                 endpoint_deficit=E,clearance_test=clearance,incidence_test=incidence,certificate_passes=passes,
                 comparison_physical_verified=True,labels_transferred=False,original_record_deleted=False))
    require(accepted>0,'no nonzero physical certificate accepted')
    require(any(r.get('certificate_passes') is False for r in rows),'no retained certificate-failure control')
    return rows

def junctions():
    rows=[]
    cases=[np.array([[0.,0.],[1.,0.],[2.,0.]]),np.array([[0.,0.],[1.,0.],[0.,0.]]),
       np.array([[0.,0.],[1.,0.],[.5,math.sqrt(3)/2],[0.,0.]])]
    for centers in cases:
        R=.46;Y,whole=solve_comparison(centers,R,centers)
        vs=[];summ=0.
        for i in range(len(centers)-1):
            YY,opt=solve_comparison(centers[i:i+2],R,centers[i:i+2]);vs.append(vectors(YY)[1][0]);summ+=opt['dual_lower']
        V=np.array(vs);D,T,d=dual(centers,R,V)
        cost=R*sum(2-np.linalg.norm(V[i-1]-V[i]) for i in range(1,len(V)))
        require(abs(D-summ-cost)<2e-10,'junction dual identity')
        require(whole['primal_upper']>=summ+cost-3e-9,'actual finite block comparison')
        rows.append(dict(centers=centers.tolist(),R=R,whole_bracket=whole,block_dual_sum=summ,junction_cost=float(cost),
              concatenated_dual=D,physical_word_claimed=False))
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--details',type=Path);a=ap.parse_args()
    exactdata=exact();records=actual_records();critical,trials,radial=actual_critical();cert=physical_certificates(critical);junc=junctions()
    result={'status':'passed','new_modules':[297,298,299],'exact':exactdata,
      'actual_regular_records':len(records),'actual_critical_records':len(critical),'nonspecial_critical_records':sum(r['minimum_incidence']<.99 for r in critical),
      'all_critical_search_trials_retained':len(trials),'radius_support_comparisons':len(radial),
      'physicality_certificate_trials':len(cert),'physicality_certificate_passes':sum(r.get('certificate_passes',False) for r in cert),
      'certificate_failure_records_retained':sum(r.get('certificate_passes') is False for r in cert),
      'nonphysical_numerical_comparison_minima':sum(not r['comparison']['comparison_is_physical'] for r in records),
      'junction_cases':len(junc),'maximum_endpoint_identity_error':max(r['endpoint_identity_error'] for r in records),
      'maximum_shape_energy_error':max(r['shape_energy_error'] for r in critical),
      'maximum_comparison_primal_dual_gap':max(r['comparison']['primal_dual_gap'] for r in records),
      'scope':'supplementary finite exact algebra, floating-point convex brackets and actual first-hit diagnostics; not continuum or all-word proof certification',
      'full_raw_pointwise_LLT_proved':False,'independent_expert_review':False}
    if a.details:a.details.parent.mkdir(parents=True,exist_ok=True);a.details.write_text(json.dumps({'summary':result,'actual_records':records,'critical_records':critical,'critical_search_trials':trials,'radius_support_cases':radial,'physicality_certificates':cert,'junction_cases':junc},indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
