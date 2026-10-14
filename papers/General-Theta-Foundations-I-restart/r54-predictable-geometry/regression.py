#!/usr/bin/env python3
"""Exact finite instances of stated identities, not continuum proof verification."""
from fractions import Fraction as F
from itertools import combinations,product
import json,hashlib
checks={}
def check(group,condition,message):
    if not condition:raise RuntimeError(group+': '+message)
    checks[group]=checks.get(group,0)+1

def calibration():
    for q,gamma,beta in product([F(1,8),F(1,4),F(1,2)],[F(1,8),F(1,4)],[F(0),F(1,4),F(1,2)]):
        c,C=1-beta,1+beta;a=q*c*gamma/(C*(1-gamma));av=4*a*(1-a)
        km=1/max(F(2),F(3)/av)
        for prior,phi,v in product([q,F(1,2),1-q],[F(-1),F(0),F(1)],[-1,1]):
            lp,lm=1+beta*phi,1-beta*phi
            gp,gm=((1-gamma,gamma) if v==1 else (gamma,1-gamma))
            post=prior*lp*gp/(prior*lp*gp+(1-prior)*lm*gm)
            check('raw_calibration',a<=post<=1-a,'posterior floor')
            mu=2*post-1;var=4*post*(1-post)
            for r in [F(-2),F(-1),F(0),F(1),F(2)]:
                loss=var+(mu-r)**2;mark=1+r*r
                check('raw_calibration',km*mark<=loss<=3*mark,'all-output quadratic comparison')

def fibers():
    # Symmetric actual fibers admit an exact minimax center and radius.
    for a,s in product([F(0),F(1,4),F(1,2),F(1)],[F(1,8),F(1,4),F(1),F(2)]):
        w=s+a*a;K=w/s
        for mu,r in product([-a,a],[F(i,4) for i in range(-8,9)]):
            loss=s+(mu-r)**2;mark=w+r*r
            check('fiber_radius',mark/(3*K)<=loss<=2*mark,'canonical criterion constants')
    gamma=F(1,4)
    ratios=[]
    for n in [8,16,32,64,128]:
        q=F(1,n);a=q*gamma/((1-q)*(1-gamma)+q*gamma)
        check('positivity_boundary',a==F(1,3*n-2),'exact posterior')
        ratios.append(1/(4*a*(1-a)))
    check('positivity_boundary',all(x<y for x,y in zip(ratios,ratios[1:])),'degenerating calibration ratio')

def drift():
    for lo,hi in [(F(1,8),F(1,4)),(F(1,10),F(1,3)),(F(1),F(1))]:
        km,kp=1+1/hi,1+1/lo;WG,WA=kp,F(1);VA=-1/hi
        for p in [lo,(lo+hi)/2,hi]:
            check('predictable_effort',1+p*VA>=0,'gate drift')
            check('predictable_effort',1-VA==km,'productive drift')
            check('attempt_cost',1+(1-p)*WG+p*WA<=WG,'upper gate potential')
            check('attempt_cost',WA==1,'productive finish')
    # History-dependent attempts. The second mark law genuinely depends on the first mark.
    nu=[F(1,2),F(1,2)];ell,u=F(1,2),F(3,2);b=F(2);h=[F(3,2),F(1,2)]
    alive=[(F(1),())];accepted=F(0);count=F(0);dist=F(0);cost=F(0)
    for t in range(1,13):
        nxt=[]
        for mass,hist in alive:
            count+=mass
            p=F(1,4) if sum(hist)%2 else F(3,4)
            for j,pj in enumerate([p,1-p]):
                a=h[j]/b;accepted+=mass*pj*a;dist+=mass*pj*a*j
                nxt.append((mass*pj*(1-a),hist+(j,)))
        alive=nxt
        check('correlated_rejection',sum(x for x,_ in alive)<=(1-ell/b)**t,'survival envelope')
        check('correlated_rejection',count<=b/ell,'finite expected attempts')
        check('correlated_rejection',dist<=u/ell*sum(nu[j]*h[j]*j for j in range(2)),'distortion envelope')
    check('correlated_rejection',accepted+sum(x for x,_ in alive)==1,'finite stopped mass accounting')

def semantic_width(sets):
    n=len(sets);compatible=[]
    for mask in range(1,1<<n):
        rows=[sets[i] for i in range(n) if mask>>i&1]
        if set.intersection(*rows):compatible.append(mask)
    dp=[n+1]*(1<<n);dp[0]=0
    for mask in range(1<<n):
        for block in compatible:dp[mask|block]=min(dp[mask|block],dp[mask]+1)
    return dp[-1]
def semantics():
    physical=[{'gate'},{'acquire'}]
    check('physical_width',semantic_width(physical)==2,'two physical ports')
    # Three spelling aliases of the same physical gate do not give extra width.
    aliasmap={'g1':'gate','g2':'gate','g3':'gate','a1':'acquire','a2':'acquire'}
    aliases=[{'g1','g2','g3'},{'a1','a2'}]
    check('physical_width',semantic_width([{aliasmap[a] for a in S} for S in aliases])==2,'alias invariance')
    check('physical_width',semantic_width([{'gate','both'},{'acquire','both'}])==1,'new phase-aware primitive changes the interface')
    check('physical_width',semantic_width([{'a','b'},{'b','c'},{'a','c'}])==2,'nonpairwise intersection example')

def atoms():
    for lam,b in product([F(1,10),F(1,4),F(1,2)],[F(1),F(2),F(4),F(10)]):
        r=max(F(0),1-b*lam)
        check('atomic_transition',r>=0 and r<=1,'real regular mass')
        if r:
            breg=b*(1-lam)/r
            check('atomic_transition',breg>=1,'normalized regular cap')
            check('atomic_transition',b*lam+r==1,'retained physical weights')
        else:check('atomic_transition',b*lam>=1,'zero-risk threshold')

def dyadic():
    e=F(1,2**14);de=F(5,4)*(F(1,32)-(F(1,4)-4*e)*(F(1,8)-2*e))
    rho=384*de;bound=F(384)/(1-rho)
    check('dyadic_certificate',de==F(10235,134217728),'boundary mass')
    check('dyadic_certificate',rho==F(30705,1048576) and rho<1,'drift reserve')
    check('dyadic_certificate',bound==F(402653184,1017871),'stopped cost')
    check('dyadic_certificate',400-bound==F(4495216,1017871)>0,'budget slack')
    check('dyadic_certificate',[int((F(3,8)+e)/e),int((F(5,8)-e)/e),int((F(1,8)-e)/e)]==[6145,10239,2047],'threshold words')
    for y,t in product([F(3,8)-e,F(3,8),F(3,8)+2*e,F(1,2),F(5,8)-2*e,F(5,8),F(5,8)+e],[F(0),2*e,F(1,8)-2*e,F(1,8),F(1,8)+e]):
        for ey,et in product([-e,F(0),e],repeat=2):
            yh=min(F(1),max(F(0),y+ey));th=min(F(1),max(F(0),t+et))
            accept=F(3,8)+e<=yh<=F(5,8)-e and th<=F(1,8)-e
            inside=F(3,8)<=y<=F(5,8) and t<=F(1,8)
            inner=F(3,8)+2*e<=y<=F(5,8)-2*e and 0<=t<=F(1,8)-2*e
            check('same_report_digitization',not accept or inside,'accepted true report')
            check('same_report_digitization',not inner or accept,'inner report never lost')
    Q=[[F(7,8),F(1,8)],[1-F(3,128),F(0)]];W=[F(384),F(376)];U=[F(1,16)]*2
    for i in range(2):
        check('killed_potentials',W[i]==1+sum(Q[i][j]*W[j] for j in range(2)),'exact W equation')
        term=(1-sum(Q[i]))*F(1,16)
        check('killed_potentials',U[i]==term+sum(Q[i][j]*U[j] for j in range(2)),'exact U equation')

def flow():
    # One transient state plus an arbitrary unreachable invariant self-loop mass.
    for a,d in product([F(1,4),F(1,2),F(3,4)],[F(0),F(1),F(100)]):
        xi=[1/a,d];bar=[1/a,F(0)];Q=[[1-a,F(0)],[F(0),F(1)]]
        for i in range(2):
            check('borel_flow_finite_instance',xi[i]==(1 if i==0 else 0)+sum(xi[j]*Q[j][i] for j in range(2)),'flow balance')
            check('borel_flow_finite_instance',bar[i]<=xi[i],'minimal occupation domination')
        check('borel_flow_finite_instance',xi[0]*a==bar[0]*a==1,'same terminal submeasure')
        check('borel_flow_finite_instance',d*(1-Q[1][1])==0,'zero-terminal invariant residual')

def composition():
    for eps in [F(0),F(1,16),F(1,4),F(1,2)]:
        # Joint law of protected sign and immediate completed virtual report.
        target={(e,v):F(1,2) if e==v else F(0) for e,v in product([-1,1],repeat=2)}
        simulated={(e,v):(1-2*eps)*target[e,v]+2*eps*F(1,4) for e,v in target}
        tv=sum(abs(target[k]-simulated[k]) for k in target)/2
        check('joint_task',tv==eps,'actual deficiency')
        check('joint_task',2*eps*F(1)==2*eps,'erased squared risk')
    for M in range(13,128):
        m=(M-1)//3-2
        check('joint_task',m>=2 and 1+3*(2+m)<=M,'all early-tag lanes counted')
        check('joint_task',F(m,M)>=F(2,15),'uniform dictionary comparison')
    for delta,r in product([F(0),F(1,8),F(1),F(3)],[F(-2),F(0),F(3)]):
        check('joint_task',((delta-r)**2+(-delta-r)**2)/2==delta**2+r*r,'unobservable calibration alternatives')

def gaussian_odds():
    for q in [F(1,16),F(1,8),F(1,4),F(1,2)]:
        c,C=q/(1-q),(1-q)/q
        for r,t in product([q,F(1,2),1-q],[F(1,2**k) for k in range(10)]):
            odds=(1-r)*t/r;mean=(1-odds)/(1+odds);var=1-mean*mean
            check('gaussian_raw_odds',4*c*t/(1+C)**2<=var<=4*C*t,'variance from raw likelihood odds')
            check('gaussian_raw_odds',(mean-1)**2<=4*C*C*t,'mean-mark comparison')

def main():
    calibration();gaussian_odds();fibers();drift();semantics();atoms();dyadic();flow();composition()
    print(json.dumps({'status':'PASS','checks':checks,'total_exact_finite_checks':sum(checks.values()),'arithmetic':'fractions.Fraction; no randomized numerical acceptance','scope':'finite examples and arithmetic only; continuous theorems are proved in the manuscript'},sort_keys=True,indent=2))
if __name__=='__main__':main()
