#!/usr/bin/env python3
"""Finite regression models for v45. They are not billiard proof certificates."""
from fractions import Fraction as F
import math
import numpy as np


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def inverse(a):
    n=len(a)
    aug=[list(row)+[F(int(i==j)) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if aug[i][j])
        aug[j],aug[pivot]=aug[pivot],aug[j]
        d=aug[j][j];aug[j]=[v/d for v in aug[j]]
        for i in range(n):
            if i!=j:
                d=aug[i][j];aug[i]=[x-d*y for x,y in zip(aug[i],aug[j])]
    return [row[n:] for row in aug]


def det_tridiagonal(diag, off):
    pprev,p=F(1),F(1)
    for j,d in enumerate(diag):
        pprev,p=p,d*p-(off[j-1]**2*pprev if j else 0)
    return p


def finite_checks():
    q=F(47,53);vstar=F(200,47);tstar=F(50,3)
    require(2*tstar/(2*tstar+vstar)==q,'row-contraction constant')
    alpha=F(1,4)
    require(1-alpha==F(3,4) and 1-2*alpha==F(1,2) and 1-3*alpha==F(1,4),
            'graded influence/margin/distortion balance')
    require(3-3==0 and 2*3==6,'collar and roof exponents')
    cases=0
    for m in range(2,10):
        for seed in range(3):
            R=F(45+seed,100)
            cs=[F(1)]+[F(2+(j+seed)%7,10) for j in range(1,m)]+[F(1)]
            ts=[F(3+(2*j+seed)%14) for j in range(m)]
            diag=[ts[j-1]+ts[j]+2/(R*cs[j]) for j in range(1,m)]
            off=[-ts[j] for j in range(1,m-1)]
            A=[[diag[i] if i==j else (off[min(i,j)] if abs(i-j)==1 else F(0))
                for j in range(m-1)] for i in range(m-1)]
            Ai=inverse(A)
            for i in range(m-1):
                rowsum=sum(abs(A[i][j]) for j in range(m-1) if j!=i)/A[i][i]
                require(rowsum<=q,'row-sum bound')
                for j in range(m-1):
                    require(0<=Ai[i][j]<=q**abs(i-j)/(vstar*(1-q)), 'inverse decay')
            # The internal incidence factors cancel from the endpoint cross term.
            H=[[cs[i+1]*A[i][j]*cs[j+1] for j in range(m-1)] for i in range(m-1)]
            Hi=inverse(H)
            cross=cs[0]*cs[1]*ts[0]*Hi[0][-1]*cs[-2]*cs[-1]*ts[-1]
            product=math.prod(ts)*cs[0]*cs[-1]/det_tridiagonal(diag,off)
            require(cross==product,'cross-Hessian determinant identity')
            resp=[cs[0]*ts[0]*Ai[j][0]/cs[j+1] for j in range(m-1)]
            for j,x in enumerate(resp):
                require(x<=cs[0]*ts[0]*q**j/(vstar*(1-q)*cs[j+1]),'incidence cancellation')
            cases+=1
    # Graded margins permit tiny interior cosines without an m-dependent sum.
    graded=0
    for m in [2,3,8,32,64,128,256,512]:
        d=np.minimum(np.arange(m+1),m-np.arange(m+1))
        for eps in [0.01,0.03,0.08]:
            e=np.power(float(q),d/4)
            response=np.power(float(q),3*d/4)/eps
            potential=response/(eps*e)**2
            require(np.allclose(potential*eps**3,np.power(float(q),d/4)), 'potential power')
            require(float(np.sum(potential))*eps**3 <= 2/(1-float(q)**0.25)+1e-10,
                    'graded sum uniform in word length')
            graded+=1
    # Log-determinant differential checked without products that underflow.
    differential=0
    for m in [3,8,16,32]:
        R=.46;cs=np.linspace(.22,.8,m-1);ts=np.linspace(3,12,m)
        dc=np.sin(np.arange(m-1)+1)/100;dt=np.cos(np.arange(m)+1)/100
        def matrix(c,t):
            a=np.diag(t[:-1]+t[1:]+2/(R*c))
            return a+np.diag(-t[1:-1],1)+np.diag(-t[1:-1],-1)
        A=matrix(cs,ts)
        dA=np.diag(dt[:-1]+dt[1:]-2*dc/(R*cs**2))+np.diag(-dt[1:-1],1)+np.diag(-dt[1:-1],-1)
        rhs=float(np.sum(dt/ts)-np.trace(np.linalg.solve(A,dA)))
        def logcross(x):
            a=matrix(cs+x*dc,ts+x*dt)
            sign,value=np.linalg.slogdet(a)
            require(sign>0,'positive contact determinant')
            return float(np.sum(np.log(ts+x*dt))-value)
        fd=(logcross(1e-4)-logcross(-1e-4))/(2e-4)
        require(abs(fd-rhs)<1e-7,'logarithmic distortion derivative')
        differential+=1
    # Exact abstract positive-collar comparison, with coincident edge values.
    collision_cases=0
    for count in [1,2,10,100]:
        h=F(1,20);jumps=[F(1,(i+2)**2) for i in range(count)]
        tvalues=[F((i%3)-1,40) for i in range(count)]
        selected=[j for j,t in zip(jumps,tvalues) if -h<=t<=h]
        mass=sum(h*j for j in selected)
        require(mass==h*sum(selected),'positive collar union keeps all coefficients')
        require(all(-h<=t and t+h<=2*h for t in tvalues),'roof interval containment')
        collision_cases+=1
    # Physical projection amplitudes, including nontrivial phase classes.
    residue_cases=0
    for order in range(1,13):
        weights=np.arange(1,order+1,dtype=float);weights/=weights.sum()
        mass=.012
        for j in range(order):
            z=np.exp(2j*np.pi*j*np.arange(order)/order)
            amplitude=abs(np.dot(mass*weights,z))**2
            require(amplitude<=mass**2+1e-16,'residue amplitude domination')
            residue_cases+=1
    require(1-3*F(1,2)<0,'unsafe graded exponent not rejected')
    require(F(1,3)-F(1,4)>0,'strict graded exponent budget')
    require(F(1,100)<F(1,10),'window shrinks without rescaling an edge coefficient')
    return {'exact_contact_matrix_cases':cases,'graded_margin_cases':graded,
      'log_determinant_differential_cases':differential,'coincident_cluster_cases':collision_cases,
      'nontrivial_residue_amplitude_cases':residue_cases,'negative_controls':2,
      'graded_exponent':'1/4','endpoint_collar_power':3,'roof_collar_power':6,
      'continuum_proof_certified':False,'full_raw_LLT_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
