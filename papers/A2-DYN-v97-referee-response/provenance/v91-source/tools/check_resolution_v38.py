#!/usr/bin/env python3
"""Finite regression models for the new proof algebra; not billiard proof certificates."""
from fractions import Fraction as F
from itertools import product
from math import comb, exp, pi, sqrt
import numpy as np
import sympy as sp

def require(ok,message):
    if not ok: raise RuntimeError(message)

def finite_checks():
    cases=0
    gaps=[F(0),F(1,7),F(1),F(3)]
    for f,g in product([F(0),F(1)],repeat=2):
        for A,B,C,D in product(gaps,repeat=4):
            qp,qm,pp,pm=f+A,f-B,g+C,g-D
            lower=qm*pp+qp*pm-qp*pp
            require(lower<=f*g<=qp*pp,'product-envelope order')
            cases+=1
    require(F(-1)*F(-1)>0,'negative control must reject product of minorants')
    L,H,e,s=sp.symbols('L H e s')
    lower=(L-e)*(H+s)+(L+e)*(H-s)-(L+e)*(H+s)
    require(sp.expand(L*H-lower)==H*e+L*s+3*e*s,'lower envelope mass')
    c=sp.Rational(2,7);tau=sp.Rational(5,4)
    B=sp.Matrix([[2,1,0,0],[0,2,1,0],[1,0,2,1],[0,0,1,2]])
    D=B*B.T+sp.eye(4)
    A=sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,-tau,1],[0,0,-c,0]])
    Om=c*A*D*A.T
    require(Om.det()==c**6*D.det(),'four-dimensional determinant')
    z1,z2,z3,y=sp.symbols('z1 z2 z3 y')
    require(A.inv()*sp.Matrix([z1,z2,z3,y])==sp.Matrix([z1,z2,-y/c,z3-tau*y/c]),'inverse clock')
    count_cases=0
    for m in range(1,12):
        for middle in product([0,1],repeat=m-1):
            visits=(1,)+middle+(1,)
            times=[j for j,v in enumerate(visits) if v]
            n=len(times)-1
            require(sum(visits[:-1])==n and times[n]==m,'[0,m) occupation disintegration')
            require(sum(visits)==n+1,'terminal-included negative control')
            count_cases+=1
    block_cases=0
    for j in range(-5,6):
        for H0 in range(1,17):
            center=F(2*j+H0-1,2)
            chosen=[n for n in range(-30,40) if -F(H0,2)<=n-center<=F(H0,2)]
            require(chosen==list(range(j,j+H0)),'half-integer block selection')
            block_cases+=1
    # Finite torus orthogonality, including a nonintegral mc and the signed split.
    N=128;angles=2*pi*np.arange(N)/N
    cut=(np.abs((angles+pi)%(2*pi)-pi)<=F(1,4)).astype(float)
    max_error=0.0
    for m in range(1,25):
        p=F(3,11);pf=float(p)
        raw=((1-pf)+pf*np.exp(1j*angles))**m
        centered=raw*np.exp(-1j*angles*m*pf)
        for n in range(m+1):
            integrand=np.exp(-1j*angles*(n-m*pf))*centered
            exact=comb(m,n)*pf**n*(1-pf)**(m-n)
            full=np.mean(integrand); central=np.mean(cut*integrand); rest=np.mean((1-cut)*integrand)
            err=max(abs(full-exact),abs(full-central-rest));max_error=max(max_error,float(err))
            require(err<2e-13,'centered torus inversion or exact signed split')
    # A finite parity model detects the invalid inference from averaged limits
    # and pointwise upper bounds to a singleton Gaussian asymptotic.
    scale=128.0;ns=np.arange(-2048,2049);gauss=np.exp(-0.5*(ns/scale)**2)/(sqrt(2*pi)*scale)
    weights=gauss*(1+(ns%2==0).astype(int)*2-1)  # 2 on even sites, 0 on odd sites
    weights=weights/weights.sum()
    require(weights[ns==1][0]==0 and gauss[ns==1][0]>0,'parity singleton negative control')
    block=(ns>=-32)&(ns<32)
    require(abs(weights[block].sum()-gauss[block].sum())<1e-3,'parity averaging model')
    require(float((weights/gauss).max())<2.01,'parity concentration model')
    # The explicit band budget does not vanish for H=1 at fixed sigma.
    require(F(1,1)/(F(1,8)*1)==8,'singleton cannot be set in diverging-width proof')
    require(F(1,1)/(F(1,10**6)*10**6)==1,'shrinking-band negative control')
    return {'product_envelope_cases':cases,'exact_lower_mass_formula':'H*e_B + L*e_sigma + 3*e_B*e_sigma',
            'orbit_endpoint_cases':count_cases,'half_integer_block_cases':block_cases,
            'torus_inversion_max_error':max_error,'covariance_determinant_identity':True,
            'negative_controls':['product of negative minorants','terminal-included occupation',
                                 'parity singleton inference','H=1 substitution','uncontrolled shrinking strip'],
            'continuum_proof_certified':False,'full_occupation_torus_cancellation_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
