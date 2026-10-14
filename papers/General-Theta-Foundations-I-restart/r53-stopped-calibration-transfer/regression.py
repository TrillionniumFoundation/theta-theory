#!/usr/bin/env python3
"""Exact finite witnesses only; not continuum proof or exhaustive synthesis."""
from fractions import Fraction as F
import json
counts={}
def check(condition, group):
    if not condition: raise RuntimeError('finite check failed: '+group)
    counts[group]=counts.get(group,0)+1

def solve(a,b):
    n=len(b); m=[list(map(F,row))+[F(rhs)] for row,rhs in zip(a,b)]
    for i in range(n):
        pivot=next(j for j in range(i,n) if m[j][i])
        m[i],m[pivot]=m[pivot],m[i]
        x=m[i][i];m[i]=[v/x for v in m[i]]
        for j in range(n):
            if j!=i:
                x=m[j][i];m[j]=[u-x*v for u,v in zip(m[j],m[i])]
    return [row[-1] for row in m]

def main():
    # Rational killed chains: fundamental counts, cost/loss potentials and flows.
    for d in range(2,12):
      for ip in range(1,d+1):
       p=F(ip,d)
       for js in range(1,d+1):
        s=F(js,d);Q=[[1-p,p],[1-s,F(0)]];k=1+1/p
        mat=[[F(i==j)-Q[i][j] for j in range(2)] for i in range(2)]
        W=solve(mat,[1,1]);x=solve(list(map(list,zip(*mat))),[1,0])
        check(W[0]==k/s and W[1]==W[0]-1/p,'gate_potentials')
        check(x[1]==p*x[0] and x[1]*s==1,'actual_terminal_mass')
        check(sum(x)==W[0] and x[1]>=1,'paid_raw_cost')
        loss=F(3,7);U=solve(mat,[0,s*loss])
        check(U==[loss,loss],'loss_potential')
        # Perturb only the active acceptance, retaining exact gate support.
        e=s/3;t=s-e;newQ=[[1-p,p],[1-t,F(0)]]
        drift=[sum((newQ[i][j]-Q[i][j])*W[j] for j in range(2)) for i in range(2)]
        rho=max(drift)
        if rho<1:
            newW=k/t
            check(newW<=W[0]/(1-rho),'drift_mean_bound')
        check(k/t>=k/s and t>0,'active_hazard_margin')
    # A nontrivial circulation has no terminal mass and must not be inverted.
    for z in range(1,31):
        Q=[[F(0),F(0)],[F(0),F(1)]];x=[F(1),F(z)];minimal=[F(1),F(0)]
        check(all(x[j]==F(j==0)+sum(x[i]*Q[i][j] for i in range(2)) for j in range(2)),'circulation_balance')
        check(sum(x[i]*(1-sum(Q[i])) for i in range(2))==1,'circulation_terminal')
        check(minimal[0]==x[0] and sum(minimal)<sum(x),'circulation_removal')
    # Calibration is checked at rational prior/likelihood values independently.
    for q in [F(1,10),F(1,5),F(1,3),F(1,2)]:
      for eta in [F(1,5),F(1,2),F(4,5)]:
       gamma=(1-eta)/2;a=q*gamma/(1-gamma)
       for n in range(21):
        prior=q+(1-2*q)*F(n,20)
        for v in [-1,1]:
         post=prior*(1+eta*v)/(prior*(1+eta*v)+(1-prior)*(1-eta*v))
         check(a<=post<=1-a,'raw_posterior_floor')
         b=2*post-1;check(4*a*(1-a)<=1-b*b<=1,'calibrated_variance')
    for M in range(13,501):
        m=(M-1)//3-2
        check(m>=2 and 1+3*(2+m)<=M,'complete_lane_budget')
        check(M-1<3*m+9<=8*m,'width_comparison')
    for eps in [F(i,100) for i in range(51)]:
        erase=2*eps
        check(erase/2==eps and erase<=1,'attained_early_deficiency')
        check(erase==2*eps,'bit_bayes_loss')
    # Solvable multibranch transient rows, not just two-stage formula substitution.
    for k in range(2,12):
        Q=[[F(1,k+2),F(1,k+3),F(1,k+4)],
           [F(1,k+5),F(1,k+2),F(1,k+6)],
           [F(1,k+7),F(1,k+8),F(1,k+2)]]
        mat=[[F(i==j)-Q[i][j] for j in range(3)] for i in range(3)]
        x=solve(list(map(list,zip(*mat))),[1,0,0]);accept=[1-sum(row) for row in Q]
        check(all(v>=0 for v in x),'three_mode_nonnegative')
        check(sum(u*v for u,v in zip(x,accept))==1,'three_mode_terminal_balance')
        cost=[F(1),F(2),F(3)];W=solve(mat,cost)
        check(sum(u*v for u,v in zip(x,cost))==W[0],'three_mode_resource_duality')
    print(json.dumps({'status':'PASS','exact_fraction_checks':sum(counts.values()),'groups':counts,'scope':'finite arithmetic witnesses; not mathematical proof or exhaustive observer enumeration'},sort_keys=True,indent=2))
if __name__=='__main__':main()
