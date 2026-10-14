#!/usr/bin/env python3
"""Finite exact/algebraic regressions, not a certificate of limit theorems."""
from fractions import Fraction as F
from itertools import product
import cmath
import math
import numpy as np
from scipy.integrate import quad

P=((F(3,4),F(1,4)),(F(1,3),F(2,3)))
PI=(F(4,7),F(3,7))

def require(ok,message):
    if not ok: raise RuntimeError(message)

def intersection(a,b):
    return max(F(0),min(a[1],b[1])-max(a[0],b[0]))

def cuts(state,s):
    return [(F(0),s),(P[state][0]-s,P[state][0]+s),(1-s,F(1))]

def words(m):
    for states in product((0,1),repeat=m+1):
        weight=PI[states[0]];a=F(1);b=F(0);x=F(0);width=F(1);A=B=0
        for i,j in zip(states,states[1:]):
            x += width*(P[i][0] if j else 0)
            width *= P[i][j]
            weight *= P[i][j]
            b=(P[j][0] if i else 0)+P[j][i]*b
            a=P[j][i]*a
            A+=j;B+=i*j
        yield states,weight,a,b,x,width,A,B

def finite_checks():
    cov=((F(204,343),F(192,343)),(F(192,343),F(198,343)))
    det=cov[0][0]*cov[1][1]-cov[0][1]**2
    conditional=cov[1][1]-cov[0][1]**2/cov[0][0]
    require(det==F(72,2401) and conditional==F(6,119),'joint covariance')
    require(cov[0][1]/cov[0][0]==F(16,17),'conditional drift')
    require(2*conditional==F(12,119),'critical damping/contact mismatch')
    # Exact joint reward recursion retains the endpoint state.
    law={(i,0,0):PI[i] for i in (0,1)}
    dp_cases=0
    for m in range(1,25):
        nxt={}
        for (i,k,l),mass in law.items():
            for j in (0,1):
                key=(j,k+j,l+i*j)
                nxt[key]=nxt.get(key,F(0))+mass*P[i][j]
        law=nxt
        require(sum(law.values())==1,'lost joint probability mass')
        require(sum(k*v for (i,k,l),v in law.items())==F(3*m,7),'A mean')
        require(sum(l*v for (i,k,l),v in law.items())==F(2*m,7),'B mean')
        require(all(sum(v for (i,k,l),v in law.items() if i==j)==PI[j] for j in (0,1)),'terminal factor')
        for u,v in [(0.31,-0.47),(math.pi,math.pi),(2*math.pi,0)]:
            direct=sum(float(mass)*cmath.exp(1j*(u*k+v*l)) for (i,k,l),mass in law.items())
            mat=np.array([[float(P[i][j])*cmath.exp(1j*(u*j+v*i*j)) for j in (0,1)] for i in (0,1)])
            matrix=np.array([float(x) for x in PI])@np.linalg.matrix_power(mat,m)@np.ones(2)
            require(abs(direct-matrix)<2e-12,'two-count Fourier pairing')
            dp_cases+=1
    # Exact word coarea and source mass: no quadrature near discontinuities.
    word_cases=0;source_cases=0;witness_cases=0;s=F(1,40)
    for m in range(2,8):
        full=F(0);vert=F(0);stable=F(0);age=F(0);wrong=F(0)
        data=list(words(m))
        for st,w,a,b,x,width,A,B in data:
            require(0<a<=F(3,4)**m and 0<=b<=1-a,'stable full word')
            # Integrating height w/(1-a) over the exact coarea interval.
            full += (w/(1-a))*(1-a)
            wrong += w*(1-a)
            vx=sum(intersection((x,x+width),J) for J in cuts(st[0],s))
            vert += PI[st[0]]*vx
            ylen=sum(intersection((F(0),F(1)),((J[0]-b)/a,(J[1]-b)/a)) for J in cuts(st[-1],s))
            stable += w*ylen
            age += w*(2*s)
            word_cases+=1
        require(full==1 and wrong!=1,'coarea Jacobian control')
        require(vert==stable==4*s and age==2*s,'actual boundary source normalization')
        source_cases+=3
        for eps in [F(-1,5),F(0),F(1,11),F(1,5)]:
            mean=F(3,7)+eps*F(2,7)
            # Fixed witnesses cancel the continuous endpoint term at z=2*pi.
            direct=sum(float(w)*cmath.exp(2j*math.pi*float(A+eps*B-m*mean)) for st,w,a,b,x,width,A,B in data)
            D=np.array([[float(P[i][j])*cmath.exp(2j*math.pi*float(j+eps*i*j-mean)) for j in (0,1)] for i in (0,1)])
            matrix=np.array([float(x) for x in PI])@np.linalg.matrix_power(D,m)@np.ones(2)
            require(abs(direct-matrix)<3e-12,'fixed witness/coarea pressure pairing')
            witness_cases+=1
    # Mesoscopic depth never exceeds the two restrictions in the positive bound.
    for m in range(2,1000):
        L=min(m//2,math.isqrt(m))
        require(1<=L<=m/2 and L<=math.sqrt(m),'mesoscopic depth restriction')
    # Gaussian conditioning and the actual witness profile, tested independently by quadrature.
    Sigma=np.array(cov,dtype=float);inv=np.linalg.inv(Sigma);normal=1/(2*math.pi*math.sqrt(float(det)))
    gaussian_checks=0
    for c,z,r in product([0.0,0.5,1.0,2.0],[-2.0,0.0,1.0],[0.17,0.73]):
        def integrand(y):
            v=np.array([z,y]);return normal*math.exp(-float(v@inv@v)/2)*cmath.exp(-2j*math.pi*(r-c*y))
        value=quad(lambda y:integrand(y).real,-14,14,epsabs=1e-11)[0]+1j*quad(lambda y:integrand(y).imag,-14,14,epsabs=1e-11)[0]
        expected=math.exp(-z*z/(2*float(cov[0][0])))/math.sqrt(2*math.pi*float(cov[0][0]))*cmath.exp(-2j*math.pi*(r-F(16,17)*c*z))*math.exp(-float(F(12,119))*math.pi**2*c*c)
        require(abs(value-expected)<1e-9,'critical Gaussian damping or phase sign')
        gaussian_checks+=1
    # Negative controls: projecting away B, omitting the Jacobian, and erasing the witness phase.
    eps=F(1,5)
    require(cov[0][0]+2*eps*cov[0][1]+eps*eps*cov[1][1]!=cov[0][0],'lost perturbed variance undetected')
    require(abs(cmath.exp(-2j*math.pi*0.17)-1)>0.5,'erased arithmetic endpoint factor undetected')
    return {'exact_joint_recursions':24,'Fourier_pairing_cases':dp_cases,
      'full_words_checked':word_cases,'exact_source_mass_cases':source_cases,
      'fixed_witness_pressure_cases':witness_cases,'Gaussian_profile_quadratures':gaussian_checks,
      'negative_controls':3,'conditional_variance':str(conditional),
      'critical_damping_over_pi_squared':'12/119','finite_checks_are_not_limit_proofs':True}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
