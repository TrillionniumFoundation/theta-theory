#!/usr/bin/env python3
"""Deterministic finite identities for v77; no continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
import sympy as S


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def checks() -> dict:
    counts = dict(section_constants=0, exact_differential_identities=0,
                  quadratic_flow=0, angular_residue=0, finite_recoupling=0,
                  angular_current=0, ordered_exponents=0)
    rlo,rhi,tau=F(9,20),F(47,100),F(3,50)
    q=F(53,100)
    require(2*q/(1+q*q)+F(1,200)<F(9,10), 'section endpoint momentum bound')
    require(2*rhi*rhi/tau+rhi==F(47,6), 'uniform Hessian upper constant')
    require((rlo*rlo*F(19,100))==F(1539,40000), 'uniform Hessian lower square')
    counts['section_constants']+=3
    x,y=S.symbols('x y', real=True)
    potentials=[x*x+S.Rational(3,2)*y*y,
                x*x+x*y+2*y*y+S.Rational(1,6)*x**3,
                x*x+2*y*y+(x*x+y*y)**2/S.Integer(8)]
    for pot in potentials:
        z=S.Matrix([x,y]);g=S.Matrix([S.diff(pot,c) for c in z]);K=S.hessian(pot,z)
        adj=K.adjugate();den=(g.T*adj*g)[0];v=K.inv()*g;s=(g.T*v)[0]
        X=adj*g/den
        tgrad=S.Matrix([-g[1],g[0]]).T*K/(g.dot(g))
        jac=S.det(S.Matrix([list(g.T),list(tgrad)]))
        chi=den/g.dot(g)
        identities=[g.dot(X)-1,(tgrad*X)[0],jac-chi,
                    g.dot(K*X)-g.dot(g)/s]
        div=S.diff(X[0],x)+S.diff(X[1],y)
        tensor=sum(S.diff(pot,z[i],z[j],z[k])*v[i]*v[j]*v[k]
                   for i,j,k in itertools.product(range(2),repeat=3))
        loggrad=S.Matrix([S.diff(K.det(),c)/K.det() for c in z])
        identities.append(div-(tensor/s**2-v.dot(loggrad)/s))
        Z=adj*g/g.dot(g)
        identities.append(S.diff(Z[0],x)+S.diff(Z[1],y))
        for value in identities:
            require(S.cancel(value)==0, 'exact field, coarea, or drift identity')
            counts['exact_differential_identities']+=1
    # Independent finite matrix fixtures for the explicit quadratic flow.
    for aa,bb in [(1.,1.),(2.,5.),(.25,7.)]:
        for z in [(1.,2.),(.03,-.02),(-1.2,.7)]:
            f=(aa*z[0]**2+bb*z[1]**2)/2
            for h in [.0001,.2,1.]:
                scale=math.sqrt(1+h/f);zh=tuple(scale*c for c in z)
                require(abs((aa*zh[0]**2+bb*zh[1]**2)/2-f-h)<1e-12,'roof translation')
                r2=(aa*z[0])**2+(bb*z[1])**2
                rh2=(aa*zh[0])**2+(bb*zh[1])**2
                require(2*min(aa,bb)*h-1e-12<=rh2-r2<=2*max(aa,bb)*h+1e-12,
                        'radial speed brackets')
                g0=(aa*z[0],bb*z[1]);gh=(aa*zh[0],bb*zh[1])
                require(abs(g0[0]*gh[1]-g0[1]*gh[0])<1e-12,'angle preservation')
                # det(scale I - h z(Kz)^T/(2 f^2 scale)) = 1.
                deriv=[[scale*(i==j)-h*z[i]*g0[j]/(2*f*f*scale) for j in range(2)] for i in range(2)]
                require(abs(deriv[0][0]*deriv[1][1]-deriv[0][1]*deriv[1][0]-1)<1e-10,
                        'unit area Jacobian of quadratic field')
                counts['quadratic_flow']+=4
        nn=16384
        integral=sum(1/(bb*math.cos(2*math.pi*(j+.5)/nn)**2+
                        aa*math.sin(2*math.pi*(j+.5)/nn)**2) for j in range(nn))*2*math.pi/nn
        require(abs(integral-2*math.pi/math.sqrt(aa*bb))<1e-10,'angular critical residue')
        counts['angular_residue']+=1
    # Three actual-state slots in one angle and label: exact rational marginals.
    arrays=list(itertools.product(range(3),repeat=3))
    for raw in arrays:
        for other in arrays:
            a=list(map(F,raw));b=list(map(F,other));sa=sum(a,F(0));sb=sum(b,F(0))
            matched=min(sa,sb)
            coupling=[[matched*a[i]*b[j]/(sa*sb) if sa and sb else F(0)
                       for j in range(3)] for i in range(3)]
            require(all(sum(row,F(0))<=a[i] for i,row in enumerate(coupling)),'source domination')
            require(all(sum((coupling[i][j] for i in range(3)),F(0))<=b[j] for j in range(3)),
                    'target domination')
            require(sum((sum(row,F(0)) for row in coupling),F(0))==matched,'maximal matched mass')
            require(sa-matched==max(F(0),sa-sb),'exact unmatched mass')
            require(sa-matched<=sum((max(F(0),a[i]-b[i]) for i in range(3)),F(0)),
                    'recoupling does not exceed branchwise stopped loss')
            counts['finite_recoupling']+=5
    require(max(F(0),sum([F(1),F(0)])-sum([F(0),F(1)]))==0,'strict recoupling example')
    require(sum([max(F(0),F(1)-F(0)),max(F(0),F(0)-F(1))])==1,'stopped comparison strictness')
    counts['finite_recoupling']+=2
    # Each angle is treated separately; summing before the negative part is required.
    for raw in itertools.product(range(3),repeat=4):
        f=list(map(F,raw))
        for i in range(4):
            for j in range(i+1,4):
                drop=max(F(0),f[i]-f[j])
                neg=sum((max(F(0),f[k]-f[k+1]) for k in range(i,j)),F(0))
                require(drop<=neg,'one-sided angular BV loss')
                counts['angular_current']+=1
    require(F(1,12)*F(1,16)==F(1,192),'fixed-width exponent')
    for q in [F(0),F(1),F(7,2)]:
        for beta in [F(1,4),F(1,2),F(1)]:
            require(-q+beta*((q+F(2))/beta)==F(2),'ordered roof-width exponent')
            counts['ordered_exponents']+=1
    counts['ordered_exponents']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'exact finite algebra, finite rational couplings, and quadratic/numerical residue fixtures only',
            'full_raw_return_LLT_proved':False,'independent_human_review':False,
            'formal_proof_certificate':False}


if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
