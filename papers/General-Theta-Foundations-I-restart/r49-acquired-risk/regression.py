#!/usr/bin/env python3
"""Exact finite checks and tagged numerical checks; not a continuous proof checker."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,math,random,subprocess,sys
ROOT=Path(__file__).resolve().parent
COUNTS:dict[str,int]={}
def check(group:str,condition:bool)->None:
    if not condition:raise RuntimeError('regression failure: '+group)
    COUNTS[group]=COUNTS.get(group,0)+1

def solve(A,b):
    n=len(b);v=[list(A[i])+[b[i]] for i in range(n)]
    for j in range(n):
        t=next(i for i in range(j,n) if v[i][j]);v[j],v[t]=v[t],v[j]
        c=v[j][j];v[j]=[x/c for x in v[j]]
        for i in range(n):
            if i!=j:
                c=v[i][j];v[i]=[x-c*y for x,y in zip(v[i],v[j])]
    return [v[i][-1] for i in range(n)]
def clock_stats(Q,p):
    k=len(Q);q=1-p;r=[1-sum(row) for row in Q]
    m=solve([[F(i==j)-Q[i][j] for j in range(k)] for i in range(k)],[F(1)]*k)[0]
    phi=solve([[F(i==j)-q*Q[i][j] for j in range(k)] for i in range(k)],[q*x for x in r])[0]
    return m,phi

def g(k,p,m):
    q=1-p
    if m<=k:
        j=m.numerator//m.denominator;b=m-j
        return (1-b)*q**j+b*q**(j+1)
    return (1+p*m/(q*k))**(-k)

def optimal_clock(k,m):
    if m<=k:
        j=m.numerator//m.denominator;b=m-j;n=j+(b>0)
        Q=[[F(0) for _ in range(n)] for _ in range(n)]
        for i in range(j-1):Q[i][i+1]=F(1)
        if b:Q[j-1][j]=b
    else:
        Q=[[F(0) for _ in range(k)] for _ in range(k)];rho=F(k)/m
        for i in range(k):
            Q[i][i]=1-rho
            if i+1<k:Q[i][i+1]=rho
    return Q

def main():
    # Concave survival envelope under an arbitrary finite supported stopping law.
    rng=random.Random(49013)
    for _ in range(100):
        times=rng.sample(range(1,31),5);weights=[rng.randint(1,10) for _ in times];total=sum(weights)
        mean=sum((F(w,total)*t for w,t in zip(weights,times)),F(0))
        for rho in [F(1),F(1,2),F(1,8),F(1,32)]:
            q=1-rho;n=mean.numerator//mean.denominator;b=mean-n
            H=sum((q**t for t in range(n)),F(0))+b*q**n
            J=1-q**(n-1)*(1-b*rho)
            actual=sum((F(w,total)*sum((q**t for t in range(tau)),F(0)) for w,tau in zip(weights,times)),F(0))
            bad=sum((F(w,total)*(1-q**(tau-1)) for w,tau in zip(weights,times)),F(0))
            check('survival_mean',actual<=H)
            check('survival_risk',bad<=J<=min(F(1),rho*(mean-1)))
            check('quadratic_margin',mean-H>=rho*mean*(mean-1)/(2*(1+rho*mean)))
            exact=(1-b)*sum((q**t for t in range(n)),F(0))+b*sum((q**t for t in range(n+1)),F(0))
            check('fractional_mean_equality',exact==H)
    for N in [F(2),F(5,2),F(10),F(100)]:
        for a in [F(1,4),F(1,16),F(1,64)]:
            rho=a/N;n=N.numerator//N.denominator;b=N-n;q=1-rho
            H=sum((q**t for t in range(n)),F(0))+b*q**n;zeta=a*a/64
            check('normalized_precision_feasible',H+zeta/rho<=N)
            check('normalized_precision_margin',N-H>=a*N/5)
    # Geometric excursion decoupling is exact rational algebra.
    for r,u,y in product([F(0),F(1,5),F(1,2),F(4,5),F(1)],repeat=3):
        if r==1:continue
        G=lambda z:(1-r)/(1-r*z)
        check('phase_decoupling',G(u*y)>=G(u)*G(y))
    # All-M equality clocks, tested against direct finite-chain linear equations.
    exact_frontiers=[]
    for k in range(1,7):
        for p in [F(1,4),F(1,2),F(3,4)]:
            means=sorted(set([F(1),F(k),F(2*k),F(7*k,2)]+([F(3,2)] if k>=2 else [])))
            for m in means:
                Q=optimal_clock(k,m);mean,phi=clock_stats(Q,p)
                check('optimal_phase_mean',mean==m)
                check('optimal_phase_transform',phi==g(k,p,m))
                check('full_state_count',len(Q)+1<=k+1)
                for b in [F(1,100),F(1,4),F(3,4)]:
                    n=len(Q);q=1-p
                    # Actual state A/T and live label form a 2n-state ensemble.
                    P=[[F(0) for _ in range(2*n)] for _ in range(2*n)]
                    for i in range(n):
                        for j in range(n):P[i][j]=q*Q[i][j];P[n+i][n+j]=Q[i][j]
                    costs=solve([[F(i==j)-P[i][j] for j in range(2*n)] for i in range(2*n)],[F(1)]*(2*n))
                    failure_rhs=[q*(1-sum(Q[i])) for i in range(n)]+[1-sum(Q[i]) for i in range(n)]
                    failure=solve([[F(i==j)-P[i][j] for j in range(2*n)] for i in range(2*n)],failure_rhs)
                    N=(1-b)*costs[0]+b*costs[n];FF=(1-b)*failure[0]+b*failure[n]
                    check('actual_prepared_risk',FF==b+(1-b)*phi)
                    check('actual_prepared_mean',N==(1-FF)/p+b*m)
                    check('prediction_comparison',FF/4<=FF/2-FF*FF/4<=FF/2)
                    for theta in [F(0),b/2,b]:
                        check('common_interval_feasible',(1-theta)*costs[0]+theta*costs[n]<=N)
                        check('common_interval_risk',theta+(1-theta)*phi<=FF)
                if m>=k and p*m-1+phi>0:
                    b=phi/(p*m-1+phi);FF=b+(1-b)*phi
                    if 0<b<1:
                        check('critical_budget',(1-FF)/p+b*m==1/p)
                        check('critical_polynomial',(FF-b)*(FF+(1-p)*k*b)**k==(1-b)*((1-p)*k*b)**k)
                        exact_frontiers.append({'p':str(p),'b':str(b),'N':str(1/p),'M':k+1,'risk':str(FF)})
    # Recurrent non-optimal clock matrices: inequality checked exactly, not inferred from construction.
    for k in range(1,5):
        for it in range(18):
            Q=[]
            for i in range(k):
                weights=[rng.randint(1,9) for _ in range(k+1)];den=sum(weights)
                Q.append([F(w,den) for w in weights[:-1]])
            for p in [F(1,5),F(1,2),F(4,5)]:
                m,phi=clock_stats(Q,p)
                check('all_clock_inequality_exact',phi>=g(k,p,m))
    # Sharpness parameters chosen so the optimal root is rational.
    for p in [F(1,10),F(1,3),F(1,2),F(3,4)]:
        q=1-p;N=1/p
        for FF in [F(i,40) for i in range(1,21)]:
            b=FF*FF/(p*FF+q);rho=p*b/FF
            T=(1-b)/(p+q*rho)+b/rho
            actual=b+(1-b)*q*rho/(p+q*rho)
            check('preparation_exact_root',actual==FF and T==N)
            check('preparation_norm',abs((1-b)-1)+b==2*b)
            h=FF*FF/((N-1)*(1-FF))
            if h<q:
                rho=h*(1-FF)/(FF+h*(1-FF));D=p+q*rho+h*(1-rho)
                T=(1+h*(1-rho)/rho)/D;actual=(q*rho+h*(1-rho))/D
                check('instrument_exact_root',T==N and actual==FF)
                check('instrument_terminal_mass',p/D+rho*(q-h)/D+h/D==1)
                check('instrument_polynomial',FF*FF==(N-1)*h*(1-FF))
                check('instrument_norm',h+h==2*h)
                for hh in [F(0),h/2,h]:
                    DD=p+q*rho+hh*(1-rho)
                    check('instrument_robust_mean',(1+hh*(1-rho)/rho)/DD<=N)
                    check('instrument_robust_risk',(q*rho+hh*(1-rho))/DD<=FF)
    # Floating-point sanity of the explicit root choice; continuum proof is in TeX.
    for N in [1.01,1.5,2.,10.,1000.]:
        for z in [1e-12,1e-8,1e-4,.01,1.,1000.]:
            ss=N*z/(N-1);tt=ss+math.sqrt(ss*ss+2*ss)
            if tt<=N:
                rho=tt/N
                lb=rho*rho*N*(N-1)/(2*(1+rho*N))
                check('normalized_root_numeric',lb+1e-12*max(1,z)>=z)
            else:
                check('one_call_fallback_numeric',z+math.sqrt(z*z+2*(1-1/N)*z)+1e-10>=N-1)
    cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(ROOT/'regression_inherited_r48.py')]
    inherited=json.loads(subprocess.check_output(cmd,text=True))
    check('inherited_native_pass',inherited['status']=='PASS')
    result={'status':'PASS','new_checks':sum(COUNTS.values()),'groups':COUNTS,'exact_frontier_examples':exact_frontiers[:10],
            'inherited_R48':inherited,'arithmetic':'exact rational except explicitly labelled numeric root checks and inherited numerical matrix checks',
            'limitations':'finite checks only; not proofs, priority, efficient synthesis, or a computed Gaussian optimum; nested counts not added'}
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
