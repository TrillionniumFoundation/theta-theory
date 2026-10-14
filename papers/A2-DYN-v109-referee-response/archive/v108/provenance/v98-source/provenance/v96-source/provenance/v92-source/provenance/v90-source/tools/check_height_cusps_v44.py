#!/usr/bin/env python3
"""Finite algebra and model regressions only; not a billiard proof certificate."""
from fractions import Fraction as F
from math import comb,exp,log,pi,sqrt
import random
import numpy as np

def require(ok,message):
    if not ok:raise RuntimeError(message)

def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def finite_checks():
    rng=random.Random(4408);v0=F(6,47);matrix_cases=0
    for m in range(1,10):
        for _ in range(12):
            cs=[F(rng.randint(1,20),20) for _ in range(m+1)]
            P=[[F(1),F(0)],[F(0),F(1)]]
            for j in range(m):
                v=v0+F(rng.randint(0,20),10);c,cp=cs[j:j+2]
                one=[[(v+c)/cp,v/(c*cp)],[v+c+cp,(v+cp)/c]]
                require(one[0][0]*one[1][1]-one[0][1]*one[1][0]==1,'one-flight determinant')
                require(all(x>=v0 for row in one for x in row),'entry lower bound')
                P=mul(one,P)
            A,B=P[0];C,D=P[1]
            require(A*D-B*C==1 and B>=v0**m,'product determinant/Jacobian')
            # In units R=1; changing parity changes only the off-diagonal sign.
            h11=A/B-cs[0];h22=D/B-cs[-1];h12=1/B
            require(h11>=0 and h22>=0 and h11*h22>=h12*h12,'endpoint curvature domination')
            matrix_cases+=1
    delta=F(1,20)
    require(1-delta*delta>(F(1,2)+4*delta)**2,'rational-chart Hessian margin')
    signs=0
    for s in range(1,51):
        for r in range(1,31):
            total=sum(4**j*comb(s,j) for j in range(min(s,r)+1))
            require(total<=5**s,'finite sign-condition exponential bound')
            signs+=1
    theta=np.linspace(0,2*pi,8192,endpoint=False)
    curvature_models=0
    for a,b in [(1,1),(1,9),(0.25,4),(3,17)]:
        H=np.diag([a,b]);x=np.stack([np.cos(theta)/sqrt(a),np.sin(theta)/sqrt(b)],axis=1)
        tangent=np.stack([-np.sin(theta)/sqrt(a),np.cos(theta)/sqrt(b)],axis=1)
        speed=np.linalg.norm(tangent,axis=1);grad=x@H
        normg=np.linalg.norm(grad,axis=1);unit=tangent/speed[:,None]
        curvature=np.einsum('ij,jk,ik->i',unit,H,unit)/normg
        inverse=float(np.mean(speed/normg)*2*pi)
        turning=float(np.mean(curvature*speed)*2*pi)
        require(abs(inverse-2*pi/sqrt(a*b))<1e-10,'quadratic coarea normalization')
        require(abs(turning-2*pi)<1e-8,'Gauss total turning')
        require(np.all(1/normg<=curvature/min(a,b)+1e-10),'curvature-coarea inequality')
        curvature_models+=1
    cusp_cases=0;max_dyadic=0
    for alpha in [F(1,8),F(1,3),F(1,2),F(1),F(3,2)]:
        for k in range(4):
            for budget in [1e-3,1e-8]:
                j=1
                while True:
                    L=j*log(2)
                    size=exp(-float(alpha)*L)*(1+L**k)
                    if L>2*(k+1)/float(alpha) and size<=budget:break
                    j+=1
                    require(j<4096,'positive cusp failed to localize')
                for q in range(1,10):
                    L2=(j+q)*log(2)
                    require(exp(-float(alpha)*L2)*(1+L2**k)<=budget,'cusp tail is not uniformly small')
                max_dyadic=max(max_dyadic,j);cusp_cases+=1
    # Exact C2 transition polynomial at u=0 and u=1.
    co=[F(1),F(0),F(0),F(-10),F(15),F(-6)]
    for order in range(3):
        require(sum(co)==0,'cutoff right trace')
        require(co[0]==(1 if order==0 else 0),'cutoff left trace')
        co=[(i+1)*co[i+1] for i in range(len(co)-1)]
    # Residual x^(3/2) has equal value/first-derivative traces and integrable second derivative.
    require(F(3,2)>1 and F(3,2)-2>-1,'residual W21 exponent')
    negative_controls=0
    for d in [F(1,4),F(1,16),F(1,64)]:
        require(float(d)**(-.5)>1,'negative-power height countercheck');negative_controls+=1
        step=lambda t: 2 if 0<t<float(d) else 0
        require(step(float(d)/2)==2 and 2*float(d)<1,'step keeps height as its mass shrinks')
    for left,right in [(-1,1),(0,7),(-3,4),(2+3j,-5+1j)]:
        require(max(abs(left),abs(right))>=abs(right-left)/2,'jump lower bound')
    # At a fixed physical collision, there is at most one actual return index.
    disjoint=0
    for mask in range(256):
        eta=[1]+[(mask>>j)&1 for j in range(8)]
        for m in range(1,9):
            indices=[n for n in range(1,m+1) if eta[m] and sum(eta[1:m+1])==n]
            require(len(indices)<=1,'return partition');disjoint+=1
    return {'matrix_models':matrix_cases,'sign_bound_cases':signs,'curvature_models':curvature_models,
            'cusp_localization_cases':cusp_cases,'largest_dyadic_exponent':max_dyadic,
            'return_partition_cases':disjoint,'negative_power_controls':negative_controls,
            'full_raw_signed_correction_verified':False,'continuum_proof_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
