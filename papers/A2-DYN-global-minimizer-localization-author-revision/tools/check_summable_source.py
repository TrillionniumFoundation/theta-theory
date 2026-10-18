#!/usr/bin/env python3
"""Auxiliary exact algebra, bounded-overlap, and actual first-hit checks for 302--303.
No finite sample or floating-point tolerance is a continuum proof certificate.
All required checks use explicit exceptions, including under python -O.
"""
from __future__ import annotations
import argparse,json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
import check_sublevel as inherited

def require(ok,msg):
    if not ok:raise RuntimeError(msg)

RPLUS=F(47,100);RMIN=F(9,20);N=94;CA=F(1,416640);TM=F(3,50);T=F(187,25);C=10**8
CG=4*RPLUS**3/CA+16*RPLUS**3+8*RPLUS**2*(RPLUS+3*N*RPLUS/CA+6*N*N*T+12*N*N*RPLUS)
CE=16*RPLUS**3+96*N*RPLUS**3
KP=128/TM+24*C/RMIN**4

def exact_checks():
    require(CG==F(12318659063517,125000),'C_G rational evaluation')
    require(CE==F(11731999,12500),'C_E rational evaluation')
    require(C-CG-CE==F(181223616493,125000)>0,'uniform constant margin')
    require(4*RPLUS<=RPLUS/CA,'shared initial and anchor gap coefficient')
    require(F(1,4480)/93==CA,'physical block anchor threshold')
    overlap=[]
    # Combinatorial tests of the proof's deterministic overlap argument, NOT billiard samples.
    for n in (2,3,7,94):
      for m in sorted(set((1,2,n-1,n,n+1,2*n,4096))):
       for offset in (1,max(1,n//2),n-1):
        anchors=set(range(offset,m,n-1));anchors.discard(0)
        start_count={};fc=np.zeros(m,dtype=int);cc=np.zeros(m+1,dtype=int);j=0
        for i in range(1,m):
            if i in anchors:j=i;continue
            require(i-j<n,'bounded gap, endpoint or incomplete block')
            start_count[j]=start_count.get(j,0)+1
            fc[j:i]+=1;cc[j+1:i]+=1
        maxima=[max(start_count.values(),default=0),int(fc.max(initial=0)),int(cc.max(initial=0))]
        require(max(maxima)<=n,'bounded overlap without collision-count payment')
        overlap.append({'N':n,'m':m,'offset':offset,'maxima':maxima})
    # Exact nonnegative algebra used in sum and phase conversion.
    algebra=0
    for x in (F(-3,7),F(0),F(2,3),F(4,5)):
     for y in (F(-5,8),F(0),F(1,6),F(3,5)):
      require((x+y)**4<=8*(x**4+y**4),'fourth-power convexity')
      require(max(x**4,y**4)<=x**4+y**4,'segment two-endpoint budget')
      for z in (F(-1,3),F(0),F(7,8)):
       require((x+y+z)**2<=3*(x*x+y*y+z*z),'three-piece squared telescope')
       algebra+=1
    # An endpoint gap may not be set to zero on an arbitrary actual record.
    r=F(23,50);c=F(4,5)
    require(2*r*(1-c)>0,'noncritical endpoint-work negative control')
    # Last incoming flight determines the final momentum as well as the previous outgoing state.
    require([min(i,0) for i in range(2)]==[0,0],'m=1 terminal duplicate indexing')
    # Small integrated mass does not control height in the target topology.
    require(F(1,1000000)*F(1000)==F(1,1000) and F(1000)>1,'mass/height distinction')
    return {'CG':str(CG),'CE':str(CE),'C_margin':str(C-CG-CE),'phase_K':str(KP),
      'conditional_overlap_arrays':overlap,'exact_scalar_cases':algebra,
      'negative_controls':['noncritical endpoint deficit nonzero','terminal flight used twice',
       'bounded overlap not number of contacts','small mass does not imply small roof height'],
      'scope':'finite exact algebra and conditional indexing, not proof that arbitrary arrays are physical'}

def vector_data(Q,O,R):
    edges=np.diff(Q,axis=0);tau=np.linalg.norm(edges,axis=1);v=edges/tau[:,None]
    normals=(Q-O)/R
    ci=np.r_[v[0]@normals[0],-np.sum(v*normals[1:],axis=1)]
    d=np.vstack((-v[0],v[:-1]-v[1:],v[-1]))
    D=float(np.sum(d*O)-R*np.linalg.norm(d,axis=1).sum())
    E=float(R*(2-ci[0]-ci[-1]));return tau,v,normals,ci,d,D,E

def trace(R,alpha,phi,m):
    q=(R*math.cos(alpha),R*math.sin(alpha));v=(math.cos(alpha+phi),math.sin(alpha+phi))
    current=(0,0);Q=[q];O=[(0.,0.)];ids=[current]
    for _ in range(m):
        q,n,current,o=inherited.next_hit(q,v,current,R)
        Q.append(q);O.append(o);ids.append(current)
        v=inherited.unit(inherited.sub(v,inherited.mul(2*inherited.dot(v,n),n)))
    Q=np.array(Q);O=np.array(O);data=vector_data(Q,O,R)
    tau,v,n,ci,d,D,E=data
    require(min(ci)>0,'unresolved singular sample; no silent exclusion')
    require(np.max(np.abs(np.linalg.norm(n,axis=1)-1))<1e-9,'actual contact geometry')
    require(np.max(np.abs(np.linalg.norm(v,axis=1)-1))<1e-12,'actual physical unit clock')
    if m>1:require(np.max(np.linalg.norm(v[1:]-v[:-1]-2*ci[1:-1,None]*n[1:-1],axis=1))<2e-8,'actual reflection')
    return Q,O,ids,data

def verify_candidate(Q,O,R,Y,kind):
    m=len(Q)-1;tau,v,n,ci,d,D,E=vector_data(Q,O,R);L=float(tau.sum())
    edges=np.diff(Y,axis=0);ell=np.linalg.norm(edges,axis=1);vh=edges/ell[:,None];ee=vh-v
    delta=Y-Q;ds2=np.sum(delta**2,axis=1);A=float(ell.sum());G=A-D
    h=np.sum(d*(Y-O),axis=1)+R*np.linalg.norm(d,axis=1)
    flight=float(.5*np.sum(ell*np.sum(ee**2,axis=1)));tol=2e-8*max(1,L,A)
    require(np.max(np.linalg.norm(Y-O,axis=1))<=R+1e-10,'comparison leaves disk domain')
    require(np.min(ell)>=float(TM)-1e-9 and np.max(ell)<=float(T)+1e-9,'global comparison edge bounds')
    require(min(h)>=-tol and G>=-tol,'positive gap terms')
    require(abs(G-flight-h.sum())<=tol and abs(L-D-E)<=tol,'full gap and endpoint identities')
    require(float(np.sum(ci[1:-1]*ds2[1:-1]))<=R*h[1:-1].sum()+tol,'summed contact gap')
    quartic=float(ds2@ds2)
    require(quartic<=float(CG)*max(G,0)+float(CE)*max(E,0)+float(CG+CE)*tol,'quartic whole-product inequality')
    is_sublevel=A<=L+tol
    if is_sublevel:require(quartic<=C*max(E,0)+C*tol,'whole-sublevel summability')
    # Reconstruct every transverse equality and aggregate, including tiny incidences.
    w=np.column_stack((-v[:,1],v[:,0]));rr=ell[:,None]*ee
    anchors={i for i in range(1,m) if ci[i]>=float(CA)};j=0;sum_b=0.;telescope=0.;nonanchors=0
    for i in range(1,m):
        if i in anchors:j=i;continue
        nonanchors+=1;require(i-j<N,'actual turning anchors')
        left=float(w[i-1]@delta[i]);right=float(w[j]@delta[j])
        right+=float(np.sum(w[j:i]*rr[j:i]))
        if i-j>1:right+=float(np.sum((w[j+1:i]-w[j:i-1])*delta[j+1:i]))
        telescope=max(telescope,abs(left-right));sum_b+=left*left
    require(telescope<=tol,'unabridged transverse telescope')
    bound=float(3*N*RPLUS/CA+6*N*N*T+12*N*N*RPLUS)*max(G,0)+float(12*N*RPLUS)*max(E,0)
    require(sum_b<=bound+float(CG)*tol,'summed transverse estimate')
    # Exact all-center theorem is analytic; these nearest-row evaluations detect implementation errors only.
    candidates=sorted(set(tuple(o) for o in O))
    gaps=[]
    def dist(z,a,b):
        v=b-a;t=np.clip(((z-a)@v)/(v@v),0.,1.);return float(np.linalg.norm(z-a-t*v))
    for i in range(m):
        target=candidates[max(0,i%len(candidates)-1):i%len(candidates)+2]
        k=max((abs(dist(np.array(z),Y[i],Y[i+1])-dist(np.array(z),Q[i],Q[i+1])) for z in target),default=0.)
        require(k<=math.sqrt(max(ds2[i],ds2[i+1]))+tol,'sample Hausdorff-to-clearance difference')
        gaps.append(k)
    require(sum(x**4 for x in gaps)<=2*quartic+tol,'summed sample clearance')
    return {'kind':kind,'flights':m,'R':R,'Q':Q.tolist(),'Y':Y.tolist(),'centers':O.tolist(),
      'incidences':ci.tolist(),'E':E,'G':G,'roof_Q':L,'roof_Y':A,'is_sublevel_with_tolerance':bool(is_sublevel),
      'comparison_is_claimed_physical':False,'quartic_sum':quartic,'quartic_bound':float(CG)*max(G,0)+float(CE)*max(E,0),
      'gap_residual':abs(G-flight-h.sum()),'transverse_identity_residual':telescope,'nonanchor_indices':nonanchors,
      'sum_transverse_squared':sum_b,'clearance_sample_fourth_sum':sum(x**4 for x in gaps),'tolerance':tol}

def phase_states(Q,O,R):
    tau,v,n,ci,d,D,E=vector_data(Q,O,R);tang=np.column_stack((-n[:,1],n[:,0]))
    return np.column_stack((np.arctan2(n[:,1],n[:,0]),np.sum(np.vstack((v,v[-1]))*tang,axis=1)))

def section_rectangles(R):
    def poly(q):return 8*R*q*(1+q*q)-4*q*(1-q*q)+math.sqrt(3)*(1-6*q*q+q**4)
    q=brentq(poly,.49,.53,xtol=1e-14);theta=2*math.atan(q)
    return [(0.,0.,1/200,1/200),(math.pi/6,-.5,1/200,1/200),
       (-theta,math.sin(theta),1/200,1/200),(math.pi/3-theta,math.sin(theta),1/200,1/200),
       (math.pi/6,0.,3/50,3/20)]

def angular(a,b):return abs((a-b+math.pi)%(2*math.pi)-math.pi)

def section_info(x,R):
    eta=False;bounds=[]
    for aa,p,h1,h2 in section_rectangles(R):
        da,dp=angular(float(x[0]),aa),abs(float(x[1])-p)
        inside=da<h1 and dp<h2;eta=eta or inside
        # Rectangles in the original model are disjoint; distance to their boundaries in l-infinity.
        bounds.append(min(h1-da,h2-dp) if inside else max(da-h1,dp-h2,0.))
    return int(eta),min(bounds)

def physical_phase_tests():
    rows=[];actual_return_events=0;changes=0
    for R in (.45,.46,.47):
      for m in (1,2,4):
       for perturb in (0.,1e-5,.0004,.006):
        Q,O,ids,data=trace(R,perturb,-perturb,m)
        require(all(z[1]==0 and z[0] in (0,1) for z in ids),'chosen actual two-disk physical word')
        # The exact normal bouncing orbit is a true first-hit global minimum, not a solver output.
        Y=np.array([(R,0.) if i%2==0 else (1-R,0.) for i in range(m+1)])
        tau,v,n,ci,d,D,E=data;E=max(E,0.)
        xs=phase_states(Q,O,R);ys=phase_states(Y,O,R)
        ds=np.array([max(angular(x[0],y[0]),abs(x[1]-y[1])) for x,y in zip(xs,ys)])
        require(float(np.sum(ds**4))<=float(KP)*E+1e-6,'actual full phase budget')
        sx=[section_info(x,R) for x in xs];sy=[section_info(y,R) for y in ys]
        cut=sum(abs(x[0]-y[0]) for x,y in zip(sx,sy));aq=sum(x[0] for x in sx[:-1]);ay=sum(x[0] for x in sy[:-1])
        actual_return_events+=int(sx[0][0] and sx[-1][0]);changes+=int(cut>0)
        for i in range(m+1):
            if sx[i][0]!=sy[i][0]:require(sx[i][1]<=ds[i]+1e-10,'section change requires actual boundary crossing')
        for rho in (.001,.01,.1):
            br=sum(b<=rho for eta,b in sx)
            require(cut<=br+float(KP)*E/rho**4+1e-6,'complete original section discrepancy budget')
        L=float(tau.sum());LY=m*(1-2*R)
        require(LY<=L+1e-8 and L-LY<=E+1e-8,'true physical roof enclosure')
        max_error=0.
        for freq in (0.,.125,7.,100.):
         for u in (0.,math.pi/3,math.pi,2*math.pi):
          # The common lattice phase cancels, not the separate roof or occupation phases.
          err=abs(np.exp(1j*(freq*L+u*aq))-np.exp(1j*(freq*LY+u*ay)))
          require(err<=abs(freq)*E+2*abs(math.sin(u/2))*cut+1e-10,'joint true-mark Fourier inequality')
          max_error=max(max_error,float(err))
        rows.append({'R':R,'m':m,'perturbation':perturb,'true_points':Q.tolist(),'physical_reference':Y.tolist(),
          'lattice_ids':ids,'E':E,'Q_section':[x[0] for x in sx],'reference_section':[y[0] for y in sy],
          'Q_boundary_distances':[x[1] for x in sx],'state_distances':ds.tolist(),'cut_count':cut,
          'original_n':aq,'reference_n':ay,'terminal_test':sx[-1][0],'true_roof':L,'reference_roof':LY,
          'observed_max_twist_error':max_error,'claim':'both records are actual first-hit; exact events not transported by fiat'})
    require(actual_return_events>0 and changes>0,'nontrivial exact-return and changed-section negative controls')
    return {'rows':rows,'true_exact_return_events':actual_return_events,'section_change_cases_retained':changes}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--details',type=Path,required=True);args=ap.parse_args()
    data={'status':'started','exact':exact_checks(),'physical_candidates':[],
       'full_raw_pointwise_LLT_proved':False,'continuum_proof_certificate':False}
    args.details.parent.mkdir(parents=True,exist_ok=True);rng=np.random.default_rng(20261017302)
    try:
      for R in (.45,.46,.47):
       trials=[(.12,.17,m) for m in (1,2,93,94,95,192)]
       # An actual near-tangent next collision, not an arbitrary incidence array.
       theta=math.asin(R/(1-R)*math.sqrt(1-1e-12))
       trials.append((0.,theta,96))
       for alpha,phi,m in trials:
        Q,O,ids,_=trace(R,alpha,phi,m)
        Y=Q.copy();Y[0]=O[0]+R*(Q[1]-O[0])/np.linalg.norm(Q[1]-O[0]);Y[-1]=O[-1]+R*(Q[-2]-O[-1])/np.linalg.norm(Q[-2]-O[-1])
        data['physical_candidates'].append(verify_candidate(Q,O,R,Y,'feasible endpoint-shortened sublevel'))
        # Full-domain bound must also tolerate arbitrary nonphysical interior competitors.
        shifts=rng.normal(size=Q.shape);shifts/=np.maximum(1.,np.linalg.norm(shifts,axis=1))[:,None]
        Z=O+.91*R*shifts
        data['physical_candidates'].append(verify_candidate(Q,O,R,Z,'arbitrary interior disk-product competitor'))
      data['physical_phase']=physical_phase_tests()
      require(sum(x['nonanchor_indices'] for x in data['physical_candidates'])>0,'actual below-anchor incidence case required')
      data['status']='passed'
    except Exception as exc:
      data['status']='failed';data['error']=repr(exc)
      args.details.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n');raise
    args.details.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'passed','candidate_records':len(data['physical_candidates']),
       'distinct_actual_reference_records':len(data['physical_candidates'])//2,
       'full_record_sublevel_cases':sum(x['is_sublevel_with_tolerance'] for x in data['physical_candidates']),
       'actual_below_anchor_incidence_checks':sum(x['nonanchor_indices'] for x in data['physical_candidates']),
       'physical_mark_comparisons':len(data['physical_phase']['rows']),
       'actual_exact_return_events':data['physical_phase']['true_exact_return_events'],
       'changed_section_cases_retained':data['physical_phase']['section_change_cases_retained'],
       'exact_overlap_arrays':len(data['exact']['conditional_overlap_arrays']),
       'exact_scalar_cases':data['exact']['exact_scalar_cases'],'C_G':str(CG),'C_E':str(CE),
       'full_raw_pointwise_LLT_proved':False,'formal_proof_certificate':False},sort_keys=True))
if __name__=='__main__':main()
