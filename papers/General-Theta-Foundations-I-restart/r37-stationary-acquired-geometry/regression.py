#!/usr/bin/env python3
"""Finite algebraic regression; not a continuum proof or a certificate of optimality."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import hashlib,json,math
COUNTS={}
def check(ok,group):
    COUNTS[group]=COUNTS.get(group,0)+1
    if not ok:raise RuntimeError('finite regression failed: '+group)
def matmul(a,b):return [[sum((x*y for x,y in zip(r,c)),F(0)) for c in zip(*b)] for r in a]
def mv(a,v):return [sum((x*y for x,y in zip(r,v)),F(0)) for r in a]
def transpose(a):return list(map(list,zip(*a)))
def l1(v):return sum(map(abs,v),F(0))
def identity(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def Gaussian_finite_surrogate():
    # A binary report model tests exact identities, not the Gaussian density hypothesis.
    P=[[F(3,4),F(1,4)],[F(1,4),F(3,4)]]
    for k in range(1,9):
      alpha=F(k,16);eta=F(1,2);gap=alpha*eta
      for j in range(11,20):
        p=F(j,20);q=[F(1,2),F(3,4)-p/2,F(1,4)+p/2]
        weights=[alpha,(1-alpha)/2,(1-alpha)/2]
        z=[weights[s]*(1-q[s] if i==0 else q[s]) for s in range(3) for i in range(2)]
        T=[[F(0) for _ in range(6)] for _ in range(6)]
        for s,i,y,ii in product(range(3),range(2),range(2),range(2)):
            ell=p if y==i else 1-p
            T[ii][2*s+i]+=alpha*ell*P[ii][i]
            out=1+y;T[2*out+ii][2*s+i]+=(1-alpha)*ell*P[ii][i]
        check(all(sum(c)==1 for c in zip(*T)),'instrument_normalization')
        check(mv(T,z)==z,'exact_stationary_calibration')
        check(sum(z)==1 and min(z)>0,'actual_ensemble_positive')
        # Grid consistency must hold for every incoming calibrated codepoint.
        atoms=[]
        for s,y in product(range(3),range(2)):
            ell=q[s]*(p if y else 1-p)+(1-q[s])*(1-p if y else p)
            w=F(1,4)+F(1,2)*q[s]*(p if y else 1-p)/ell
            check((w>F(1,2))==bool(y),'common_grid_compatible')
            atoms.append((weights[s]*ell,w,1+y))
        check(sum(a[0] for a in atoms)==1,'acquired_row_mass')
        outmass=[F(0)]*3;outmoment=[F(0)]*3;msq=F(0);jensen=F(0)
        for mass,w,sout in atoms:
            for out,r in ((0,alpha),(sout,1-alpha)):
                mass2=mass*r;outmass[out]+=mass2;outmoment[out]+=mass2*w
                msq+=mass2*(w-q[out])**2;jensen+=mass2*(w*w-q[out]**2)
        check(outmass==weights,'pooled_label_mass')
        check(all(outmoment[s]==weights[s]*q[s] for s in range(3)),'pooled_centroid')
        check(jensen==msq and msq>=0,'strong_concavity_identity')
        check(all(T[i][j]>=gap/2 for i in range(2) for j in range(6)),'raw_erasure_minorization')
        for u,v in product(range(6),repeat=2):
            d=[F(i==u)-F(i==v) for i in range(6)]
            check(l1(mv(T,d))<=(1-gap)*l1(d),'base_norm_contraction')
        # Independent bit is prepared after all controls: exact additive floor.
        for a in (F(0),F(1,4),F(1,2),F(1)):
            eps=a/2;delta=F(3,8)
            bitrisk=a;cal=(delta**2+(-delta)**2)/2
            check(bitrisk+cal==2*eps+delta**2,'same_task_error_algebra')
    # Zero ensemble contributes zero regardless of codepoint/action choices.
    for q in (F(0),F(1,7),F(1,2),F(1)):
        check(mv(P,[F(0)*q,F(0)*(1-q)])==[0,0],'zero_mass_row')
def finite_strata_and_acquisition():
    for m in range(2,130):
      for d in range(1,7):
        p=F(2,d);target=(m-1)**(-float(p));k=math.ceil(-math.log2(target/2))
        alpha=2.0**(-k)
        check(target/4-1e-15<=alpha<=target/2+1e-15,'dyadic_erasure_budget')
      check((m+1)/2==sum(range(1,m+1))/m,'protected_expected_calls')
    for w in (F(1,8),F(1,4),F(1,2),F(3,4)):
      for m in range(8,65,4):
        xi=w*F(1,m*m)+(1-w)*F(1,m)
        check(xi>=w*F(1,m*m) and xi>= (1-w)*F(1,m),'actual_stratum_weights')
    # An invariant law without a mixing certificate need not attract another law.
    I=identity(2);check(mv(I,[F(1),F(0)])!=[F(0),F(1)],'invariance_not_attraction')
def quantum_rational_congruence():
    # Rational positive congruence, noncommutation and marked projections.
    rho=[[F(2,5),F(1,10)],[F(1,10),F(3,5)]]
    for a in range(-3,4):
      for b in range(6,15):
        B=[[F(1),F(a,20)],[F(a,20),F(b,10)]]
        raw=matmul(matmul(B,rho),B);mass=raw[0][0]+raw[1][1]
        sigma=[[x/mass for x in row] for row in raw]
        E=matmul(B,B);scale=F(2)/(E[0][0]+E[1][1]);E=[[scale*x for x in row] for row in E]
        check(E[0][0]+E[1][1]==2,'trace_D_effect')
        check(sigma[0][0]+sigma[1][1]==1,'normalized_congruence')
        check(sigma[0][0]*sigma[1][1]>sigma[0][1]**2,'positive_posterior')
        check(E[0][0]*E[1][1]>E[0][1]**2,'positive_effect')
        for lam in (F(1,4),F(1,2),F(3,4)):
            out=[[lam*sigma[i][j]+(1-lam)*F(i==j,2) for j in range(2)] for i in range(2)]
            rem=[[out[i][j]-(1-lam)*F(i==j,2) for j in range(2)] for i in range(2)]
            check(rem[0][0]*rem[1][1]>=rem[0][1]**2,'quantum_raw_minorization')
            deph=[[out[0][0],F(0)],[F(0),out[1][1]]]
            check(deph[0][0]+deph[1][1]==1,'visible_rank_projection')
        check((matmul(E,rho)==matmul(rho,E))==(b==10+a),'commutation_characterization')
def main():
    Gaussian_finite_surrogate();finite_strata_and_acquisition();quantum_rational_congruence()
    result={'status':'PASS','checks':sum(COUNTS.values()),'groups':COUNTS,'arithmetic':'exact rational except dyadic-bound floating comparison','limitations':'finite algebraic regressions only; no density, fixedpoint, continuum proof, optimality or priority certified'}
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
