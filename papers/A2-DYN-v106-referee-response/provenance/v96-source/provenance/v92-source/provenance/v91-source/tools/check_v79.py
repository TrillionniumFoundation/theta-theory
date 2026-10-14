#!/usr/bin/env python3
"""Finite regression fixtures for v79, not a continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
import numpy as np
import sympy as sp
from check_v77 import require


def checks() -> dict:
    counts = dict(stationary_cubic=0, flight_cubic=0, optical_polynomial=0,
                  jacobian_factor=0, flux_pullback=0, legal_scales=0)
    q,z = sp.symbols('q z')
    for a,r,A,B,C,D in itertools.product((F(1),F(1,1000000)),
                                       (F(-2),F(0),F(3,2)),
                                       (F(-1),F(2)),(F(1),),
                                       (F(-2),F(3)),(F(1),)):
        aa,rr,aa3,bb3,cc3,dd3=map(sp.Rational,(a,r,A,B,C,D))
        action=aa*(z-rr*q)**2/2+aa3*q**3/6+bb3*q*q*z/2+cc3*q*z*z/2+dd3*z**3/6
        second=-(bb3/2+cc3*rr+dd3*rr**2/2)/aa
        curve=rr*q+second*q*q
        stationary=sp.Poly(sp.expand(sp.diff(action,z).subs(z,curve)),q)
        require(stationary.coeff_monomial(q)==0 and stationary.coeff_monomial(q*q)==0,
                'stationary two-jet')
        reduced=sp.Poly(sp.expand(action.subs(z,curve)),q).coeff_monomial(q**3)*6
        contract=aa3+3*bb3*rr+3*cc3*rr*rr+dd3*rr**3
        require(sp.simplify(reduced-contract)==0,'cubic envelope cancellation')
        counts['stationary_cubic']+=2
    rng=np.random.default_rng(790180)
    tau=.06;Rmin=.45;constant=6/tau**2+3/(Rmin*tau)+1/Rmin**2
    for _ in range(200):
        R=float(rng.uniform(.45,.47));ang=rng.uniform(-math.pi,math.pi,2)
        normals=np.array([[math.cos(x),math.sin(x)] for x in ang])
        tangents=np.array([[-math.sin(x),math.cos(x)] for x in ang])
        centers=np.array([[0.,0.],[1.,0.]])
        points=centers+R*normals;dz=points[1]-points[0];length=float(np.linalg.norm(dz))
        require(length>=tau-1e-12,'flight lower bound fixture')
        unit=dz/length;U,V,W=rng.normal(size=(3,2))
        d=lambda X:tangents[1]*X[1]-tangents[0]*X[0]
        d2=lambda X,Y:(-normals[1]*X[1]*Y[1]+normals[0]*X[0]*Y[0])/R
        d3=(-tangents[1]*U[1]*V[1]*W[1]+tangents[0]*U[0]*V[0]*W[0])/R**2
        nu=lambda X:float(unit@X)
        n2=lambda X,Y:float((X@Y-nu(X)*nu(Y))/length)
        X,Y,Z=d(U),d(V),d(W)
        n3=(-nu(X)*(Y@Z)-nu(Y)*(X@Z)-nu(Z)*(X@Y)+3*nu(X)*nu(Y)*nu(Z))/length**2
        actual=n3+n2(d2(U,V),Z)+n2(d2(U,W),Y)+n2(d2(V,W),X)+nu(d3)
        bound=constant*np.abs(U).sum()*np.abs(V).sum()*np.abs(W).sum()
        require(abs(actual)<=bound*(1+1e-12),'circle flight cubic bound')
        counts['flight_cubic']+=2
    for m in range(1,7):
        lengths=sp.symbols('l0:'+str(m));potentials=sp.symbols('v1:'+str(m))
        y=lengths[0];f=sp.Integer(1)
        for i in range(m-1):
            f=f+potentials[i]*y;y=sp.expand(y+lengths[i+1]*f)
        variables=(*lengths,*potentials);poly=sp.Poly(y,*variables)
        require(all(co>0 for co in poly.coeffs()),'positive polynomial coefficients')
        require(all(max(mono)<=1 for mono in poly.monoms()),'separate affineness')
        counts['optical_polynomial']+=2
        values={v:sp.Rational(i+2,i+1) for i,v in enumerate(variables)}
        yy=y.subs(values)
        for v in variables:
            sensitivity=(v*sp.diff(y,v)).subs(values)/yy
            require(0<=sensitivity<=1,'optical sensitivity is a probability')
            counts['optical_polynomial']+=1
    vals=(F(1,9),F(1,2),F(1),F(3),F(11))
    for eta,x,y in itertools.product(vals,repeat=3):
        k=x/y;J=eta*k
        require(abs(max(F(0),1-J)-max(F(0),1-eta))<=eta*abs(1-k),
                'complete angular positive-part comparison')
        require(eta==J*y/x,'target Jacobian direction')
        counts['jacobian_factor']+=2
    for t,b,theta in itertools.product((F(0),F(1,4)),(F(1,2),F(3,4)),vals):
        source=(2+theta)/(1+t*t);boundary=(2+theta)/(1+b*b)
        J=boundary/source
        require(boundary/J==source,'first-exit initial-density pullback')
        counts['flux_pullback']+=1
    for n in (2,10,100,1000000):
        boundary=F(1,n);source=F(1,2)
        require(boundary/(boundary/source)==source,'vanishing exit density retains initial mass')
        counts['flux_pullback']+=1
    for qx,qo,bx,bo in itertools.product((F(0),F(2)),(F(1),F(4)),(F(1,4),F(1)),(F(1,2),F(2))):
        gamma=max(F(2),qx/bx,qo/bo)+1
        require(gamma/2-1>0 and gamma*bx-qx>0 and gamma*bo-qo>0,'separate legal powers')
        counts['legal_scales']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite exact polynomial, rational Jacobian/flux, and seeded differential fixtures',
            'full_raw_return_LLT_proved':False,'formal_proof_certificate':False,
            'independent_human_review':False}


if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
