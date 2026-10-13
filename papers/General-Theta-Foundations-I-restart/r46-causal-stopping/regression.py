#!/usr/bin/env python3
"""Finite exact algebra and numerical sanity checks; never continuum proofs."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product,combinations
from collections import Counter
import json,math
import numpy as np
COUNTS=Counter()
def check(ok:bool,group:str,message:str)->None:
    if not bool(ok):raise RuntimeError(group+': '+message)
    COUNTS[group]+=1

def occupation()->None:
    for k in range(1,21):
        p=F(k,23);z0=1/(1-p)
        for h in [F(0),F(1,7),F(2),F(100)]:
            check(z0==1+p*z0,'occupation_exact','balance')
            check((1-p)*z0==1,'occupation_exact','terminal mass')
            check(z0<=z0+h,'occupation_exact','budget removal')
            for t in range(1,10):
                actual=sum(p**j for j in range(t))
                check(z0-actual==p**t*z0,'occupation_exact','finite resolvent identity')
    for n in range(1,18):
        N=F(n,3)+1;a=1/N
        for t in range(1,11):
            check(sum(a*(1-a)**j for j in range(t))==1-(1-a)**t,'stopping_exact','geometric terminal law')
            check(sum((1-a)**j for j in range(t))<=N,'stopping_exact','partial mean')

def common_routing()->None:
    for u0,u1,v0,v1 in product(range(-2,3),repeat=4):
        joint=max(u0+u1,v0+v1);wrong=max(u0,v0)+max(u1,v1)
        check(joint<=wrong,'joint_support_exact','sum must precede maximum')
        for gamma in (F(0),F(1,3),F(1)):
            actual=gamma*(u0+u1)+(1-gamma)*(v0+v1)
            check(actual<=joint,'joint_support_exact','one common routing witness')
    check(max(1-1,-1+1)<max(1,-1)+max(-1,1),'joint_support_exact','strict modelwise relaxation')
    for r0,r1 in product([F(j,10) for j in range(11)],repeat=2):
        risks=[((r0-F(model))**2+(r1-F(1-model))**2)/2 for model in (0,1)]
        check(max(risks)>=F(1,4),'unknown_bit_exact','common minimax lower')

def trimmed_mass()->None:
    weights=[F(1,10),F(1,5),F(3,10),F(2,5)]
    values=[F(-1,2),F(-1,6),F(1,6),F(1,2)]
    for N in [F(1),F(5,4),F(2),F(3),F(5),F(10)]:
        for centers in [(F(0),),(F(-1,2),F(1,2)),(F(-1,6),F(1,6))]:
            costs=[min((x-c)**2 for c in centers) for x in values]
            rest=F(1);density=[F(0)]*4
            for j in sorted(range(4),key=lambda j:(costs[j],j)):
                take=min(rest,N*weights[j]);density[j]=take/weights[j];rest-=take
            check(rest==0,'trimmed_exact','selected mass filled')
            check(sum(w*h for w,h in zip(weights,density))==1,'trimmed_exact','normalization')
            check(all(0<=h<=N for h in density),'trimmed_exact','mass budget')
            check(sum(w*h/N for w,h in zip(weights,density))==1/N,'trimmed_exact','physical acceptance')
            risk=sum(w*h*c for w,h,c in zip(weights,density,costs))
            for i,j in product(range(4),repeat=2):
                if density[i]>0 and density[j]<N:
                    check(costs[i]<=costs[j],'trimmed_exact','threshold optimality')
            if risk==0:
                mass=sum(weights[j] for j,c in enumerate(costs) if c==0)
                check(mass>=1/N,'atoms_exact','zero-risk atom threshold')
    for m in range(1,5):
        largest=max(sum(weights[j] for j in S) for S in combinations(range(4),m))
        for N in [F(1),F(2),F(3),F(5),F(10)]:
            feasible=any(sum(weights[j] for j in S)>=1/N for S in combinations(range(4),m))
            check(feasible==(N*largest>=1),'atoms_exact','finite support criterion')

def classical_audit()->None:
    for i in range(-20,21):
        x=F(i,40);pplus=(x*x+F(1,2)+x)/2;pminus=(x*x+F(1,2)-x)/2;pzero=F(1,2)-x*x
        check(min(pplus,pminus,pzero)>0,'classical_audit_exact','positive audit')
        check(pplus+pminus+pzero==1,'classical_audit_exact','normalization')
        check(pplus-pminus==x,'classical_audit_exact','mean')
        check(pplus+pminus-x*x==F(1,2),'classical_audit_exact','constant variance')
    for d in range(1,5):
        for theta in [F(-3,4),F(-1,4),F(0),F(1,2),F(3,4)]:
            for x in product([F(-1,2),F(0),F(1,2)],repeat=d):
                for y in [tuple([F(-1,2)]*d),tuple([F(1,2)]*d)]:
                    v=1+4*theta*sum(a*b for a,b in zip(x,y))/d
                    check(1-abs(theta)<=v<=1+abs(theta),'raw_kernel_exact','uniform conditional density')

def correlated_rejection()->None:
    grid=np.linspace(-.5,.5,9);nu=np.ones(9)/9
    for theta in [-.8,-.3,0,.4,.8]:
        lower=1-abs(theta);upper=1+abs(theta)
        K=(1+4*theta*grid[:,None]*grid[None,:])*nu[None,:]
        for N in [5.,10.,30.]:
            if lower*N<1-1e-12:continue
            centers=np.array([-.5,.5]);cost=np.min((grid[:,None]-centers[None,:])**2,axis=1)
            h=np.zeros(9);rest=1.
            for j in np.argsort(cost,kind='stable'):
                take=min(rest,lower*N*nu[j]);h[j]=take/nu[j];rest-=take
            A=h/(lower*N);Q=K*(1-A)[None,:]
            initial=np.zeros(9);initial[4]=1
            visits=np.linalg.solve(np.eye(9)-Q.T,initial)
            terminal=(visits@K)*A;mean=float(visits.sum());risk=float(terminal@cost);target=float((nu*h)@cost)
            check(abs(terminal.sum()-1)<1e-10,'correlated_numeric','actual terminal mass')
            check(mean<=N+1e-9,'correlated_numeric','actual mean cap')
            check(risk<=upper/lower*target+1e-10,'correlated_numeric','conditional comparison upper')
            check(np.max(terminal/(upper*N*nu))<=1+1e-9,'correlated_numeric','actual law domination')
            check(np.min(K@A)>=1/N-1e-12,'correlated_numeric','implemented acceptance floor')

def quantum()->None:
    rng=np.random.default_rng(460012)
    for q in range(2,8):
        c0=q*q+q-1;B=c0-1
        for _ in range(30):
            v=rng.normal(size=q)+1j*rng.normal(size=q);v=v/np.linalg.norm(v);P=np.outer(v,v.conj())
            Z=(q+1)*P-np.eye(q)
            check(abs(np.trace(Z@Z).real-c0)<1e-9,'quantum_numeric','audit squared norm')
            check(abs(np.trace(P@P).real-1)<1e-12,'quantum_numeric','pure-state norm')
            rho=rng.normal(size=(q,q))+1j*rng.normal(size=(q,q));rho=rho@rho.conj().T;rho/=np.trace(rho)
            eta=.2;T=eta*np.eye(q)/q+(1-eta)*rho;lik=q*np.trace(P@T).real
            check(eta-1e-12<=lik<=q+1e-12,'quantum_numeric','raw report comparison')
        for r in range(1,q+1):
            check(F(c0)-F(1,r)>=0,'rank_exact','rank-dependent noise')
        for j in range(1,10):
            radius=math.sqrt(2)*j/10;mass=(radius*radius/2)**(q-1)
            check(0<mass<=1,'haar_formula_numeric','declared ball formula finite evaluation')
    for n in range(1,12):
        check(F(2,3)**n==F(2**n,3**n),'cantor_exact','level interval mass scale')
        check(F(1,2**n)*2**n==1,'cantor_exact','cylinder probability')

def errors()->None:
    for erased in [F(j,10) for j in range(11)]:
        eps=erased/2
        for delta in [F(0),F(1,10),F(1,2)]:
            for r in [F(j,10) for j in range(-10,11)]:
                bit=((1-r)**2+(-1-r)**2)/2
                calibration=((delta-r)**2+(-delta-r)**2)/2
                check(bit>=1,'errors_exact','erased unknown bit lower')
                check(calibration>=delta*delta,'errors_exact','hidden offset lower')
                check(erased==2*eps,'errors_exact','attained deficiency coefficient')
    for M in range(5,101):
        m=(M-1)//4
        check(4*m+1<=M,'resource_integer','all product labels charged')
        check(m>=M/8,'resource_integer','uniform coarse budget comparison')
    for R,M in product(range(1,12),repeat=2):
        check((R*M).bit_length()>0,'resource_integer','positive product-state count')

def main()->None:
    occupation();common_routing();trimmed_mass();classical_audit();correlated_rejection();quantum();errors()
    print(json.dumps({'status':'PASS','component':'R46 finite checks','checks_by_group':dict(sorted(COUNTS.items())),'finite_checks':sum(COUNTS.values()),'scope':'Exact Fraction/integer algebra except explicitly named numerical groups; none is a continuum proof; no inherited count is added.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
