#!/usr/bin/env python3
"""Exact finite witnesses for R58. Not a proof of any continuum theorem."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json,subprocess,sys
COUNTS={};VALUES=[]
def check(group,condition,message,value=None):
    if not condition:raise RuntimeError(group+': '+message)
    COUNTS[group]=COUNTS.get(group,0)+1
    if value is not None:VALUES.append(repr(value))
def occupancy(Q,initial=(F(1),F(0))):
    a=1-Q[0][0];b=-Q[0][1];c=-Q[1][0];d=1-Q[1][1];det=a*d-b*c
    if det<=0:raise RuntimeError('transient two-state system required')
    return ((initial[0]*d-initial[1]*c)/det,(-initial[0]*b+initial[1]*a)/det)
def capped_value(nu,cost,cap):
    remaining=F(1);ans=F(0)
    for i in sorted(range(len(nu)),key=lambda i:(cost[i],i)):
        mass=min(remaining,cap*nu[i]);ans+=mass*cost[i];remaining-=mass
    if remaining:raise RuntimeError('insufficient capped mass')
    return ans

def main():
    # Actual occupancies, not a substituted reference execution.
    nu=[F(1,2),F(1,3),F(1,6)];means=[F(-1,3),F(0),F(1,3)];var=[F(1,7),F(1,3),F(3,4)]
    delta=F(1,1000);gamma=F(1,2000)
    P=[[nu[0]+delta,nu[1]-delta,nu[2]],[nu[0]-delta,nu[1]+delta,nu[2]]]
    W=[[x+gamma for x in var],[x-gamma for x in var]]
    d0=[sum(abs(P[s][y]-nu[y]) for y in range(3)) for s in range(2)]
    d1=[sum(abs((P[s][y]-nu[y])*means[y]) for y in range(3)) for s in range(2)]
    d2=[sum(abs(P[s][y]*(W[s][y]+means[y]**2)-nu[y]*(var[y]+means[y]**2)) for y in range(3)) for s in range(2)]
    rowe=[d2[s]+4*d1[s]+4*d0[s] for s in range(2)] # radius 2
    for pattern in product((F(1,4),F(1,2),F(3,4)),repeat=6):
        qs=[pattern[:3],pattern[3:]]
        Q=[[sum(P[s][y]*(1-qs[s][y]) for y in range(3) if y%2==t) for t in range(2)] for s in range(2)]
        visit=occupancy(Q);budget=sum(visit)
        accepted=sum(visit[s]*P[s][y]*qs[s][y] for s in range(2) for y in range(3))
        check('exact_actual_occupation',accepted==1,'actual almost-sure terminal mass')
        xi=[nu[y]*sum(visit[s]*qs[s][y] for s in range(2)) for y in range(3)]
        total=sum(xi);A=budget*delta;E=sum(visit[s]*rowe[s] for s in range(2));t0=1-A
        check('exact_comparison_mass',abs(total-1)<=A,'unnormalized mass discrepancy',(total,A))
        for y in range(3):check('exact_comparison_cap',xi[y]<=budget*nu[y],'cap on actual prehistories')
        check('exact_positive_retained_mass',t0>0 and total>=t0,'positive retained mass')
        for centers in ((F(0),),(F(-1),F(1)),(F(-1),F(0),F(1))):
            assigned=[[centers[(y+s)%len(centers)] for y in range(3)] for s in range(2)]
            actual=sum(visit[s]*P[s][y]*qs[s][y]*(W[s][y]+(means[y]-assigned[s][y])**2) for s in range(2) for y in range(3))
            replaced=sum(visit[s]*nu[y]*qs[s][y]*(var[y]+(means[y]-assigned[s][y])**2) for s in range(2) for y in range(3))
            check('exact_task_replacement',abs(actual-replaced)<=E,'finite-image response certificate')
            cost=[var[y]+min((means[y]-r)**2 for r in centers) for y in range(3)]
            lower=t0*capped_value(nu,cost,budget/t0)-E
            check('exact_reference_lower',actual>=max(F(0),lower),'two-sided reference converse',(actual,lower))
    # Measurable-dependence hazard proof checked on exact rational design values.
    for n in range(2,35):
        for da in (80,100,500):
            a=F(1,da);b=F(n);beta=b/(1+b*a)
            if beta<1:continue
            check('exact_budget_restore',beta/(1-beta*a)==b,'same expected acquisition budget')
            for rho in (F(0),F(1,100),F(1,40)):
                rhs=(1+b*a)*rho+b*F(1,1000)
                lhs=(rho+beta*F(1,1000))/(1-beta*a)
                check('exact_upper_substitution',lhs==rhs,'no missing mass denominator')
    # All deterministic/randomized policies depending on current mode in this finite family.
    for u,v,pi in product((F(1,100),F(1,20),F(1,5)),(F(1,10),F(1,2),F(1)),(F(0),F(1,10),F(1))):
        trans=[[1-u,u],[v,1-v]]
        for q0,q1 in product((F(1,8),F(1,4),F(1,2),F(1)),repeat=2):
            qs=[q0,q1];Q=[[(1-qs[s])*trans[s][t] for t in range(2)] for s in range(2)]
            visit=occupancy(Q,(1-pi,pi));calls=sum(visit);bad=visit[1]
            check('exact_metastable_occupation',bad<=pi/v+u*calls/v,'adaptive killed-potential bound',(bad,pi/v+u*calls/v))
        for mode in (0,1):
            drift=sum(trans[mode][j]*(F(j)/v) for j in range(2))-F(mode)/v
            check('exact_mode_drift',F(mode)+drift<=u/v,'raw one-call certificate')
    # Inverse-exit-time charge is visible; dropping the preparation term is invalid.
    u=F(1,10000);v=F(1,100);pi=F(1);q=F(1,2)
    visit=occupancy([[(1-q)*(1-u),(1-q)*u],[(1-q)*v,(1-q)*(1-v)]],(0,1))
    check('exact_transient_counterexample',visit[1]>u*sum(visit)/v,'initial bad mass cannot be suppressed')
    for b in range(1,41):
        for k in range(0,6):
            e=F(k,5*b);variance=b*e
            check('exact_two_way_sharpness',variance/b==e and 0<=variance<=1,'productive task defect')
            check('exact_two_way_sharpness',F(1,b)*b==1,'actual paid selection',variance)
    # A mark-only certificate would hide one bit of audit information.
    check('exact_full_report_counterexample',sum(F(1,2)*(z-z)**2 for z in (-1,1))==0,'full report prediction')
    check('exact_full_report_counterexample',sum(F(1,2)*z*z for z in (-1,1))==1,'constant mark profile')
    for M in range(13,201):
        mt=(M-1)//3-2;me=M//3
        check('exact_joint_resource_accounting',7+3*mt<=M and max(7,3*me)<=M,'separate stop interfaces')
        check('exact_joint_resource_accounting',8*mt>=M and 4*me>=M,'fixed geometric width ratios')
    # Concrete noncommuting full instruments, including rank-changing effects.
    import numpy as np
    I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]).astype(complex)
    pauli=[I,X,Y,Z];proj=[(I+Z)/2,(I-Z)/2]
    def instrument(rho,axis,eta):
        vals=[]
        for sign in (-1,1):
            effect=(I+sign*eta*axis)/2
            ev,U=np.linalg.eigh(effect);K=(U*np.sqrt(np.maximum(ev,0)))@U.conj().T
            state=K@rho@K.conj().T
            vals += [float(np.trace(P@state).real) for P in proj]
        return np.array(vals)
    for amplitude,theta,eta in product((0.,.02,.2,.8,1.),(.13,.61,1.3),(0.,.5,1.)):
        rho=(I+amplitude*(np.cos(theta)*X+np.sin(theta)*Z))/2;axis=np.cos(theta)*X+np.sin(theta)*Y
        p0=instrument(I/2,axis,eta)
        for C in pauli:
            p=instrument(C@rho@C.conj().T,axis,eta)
            check('numeric_raw_quantum_certificate',np.min(p)>=-1e-13 and abs(p.sum()-1)<1e-12,'positive normalized full instrument')
            check('numeric_raw_quantum_certificate',np.abs(p-p0).sum()/2<=amplitude/2+2e-13,'raw trace-to-joint-variation contraction')
    inherited=subprocess.run([sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(Path(__file__).with_name('inherited_regression.py'))],capture_output=True,text=True)
    if inherited.returncode:raise RuntimeError(inherited.stdout+inherited.stderr)
    inherited_result=json.loads(inherited.stdout)
    result={'status':'PASS','counts':dict(sorted(COUNTS.items())),'exact_checks':sum(v for k,v in COUNTS.items() if k.startswith('exact_')),'floating_checks':sum(v for k,v in COUNTS.items() if k.startswith('numeric_')),'witness_sha256':hashlib.sha256('\n'.join(VALUES).encode()).hexdigest(),'inherited_R57':inherited_result,'limitations':'Finite exact witnesses and numerical consistency only. Not continuous-parameter proof, priority, significance, or a sum of independent historical tests.'}
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
