#!/usr/bin/env python3
"""Independent finite checks for A2 v52; no author code is imported.
Requires Python 3 and NumPy. These checks are not a billiard-realization,
infinite-flight, full-proof, or statistical-optimality certificate.
Run: python independent_checks.py; python -O independent_checks.py.
"""
import json
from fractions import Fraction
import numpy as np
from numpy.polynomial.legendre import leggauss


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)


def action(u, t=0.0):
    return u*u/2 + u**3/20 + u**4/40 + t*(u*u/10 + u**3/40)


def derivative(u):
    return u + 3*u*u/20 + u**3/10


def setup(t, x, y):
    u, v = x-(0.04+0.3*t), y-(-0.02-0.2*t)
    w = np.exp((0.2+0.3*t)*x+(-0.1+0.2*t)*y)*(2+y*y)
    H = 2-action(u,t)-action(v,t)
    return u, v, w, H


def integrate(f, x, y, weights):
    return float(np.sum(weights*f(x,y)))


def main():
    z, w = leggauss(100)
    xx, yy = (0.05+0.35*z)[:,None], (-0.05+0.3*z)[None,:]
    ww = 0.35*0.3*w[:,None]*w[None,:]
    def normalizer(t):
        return integrate(lambda x,y: setup(t,x,y)[2]*setup(t,x,y)[3],xx,yy,ww)
    def density(t,x,y):
        _,_,weight,H=setup(t,x,y)
        return weight*H/normalizer(t)
    u,v,weight,H=setup(0,xx,yy)
    require(np.min(H)>1.8, 'positive-window margin')
    f=weight*H
    ax=0.2
    cy=-0.1+2*yy/(2+yy*yy)
    fx=weight*(ax*H-derivative(u))
    fy=weight*(cy*H-derivative(v))
    fxy=weight*(ax*cy*H-ax*derivative(v)-cy*derivative(u))
    interaction=fxy/f-fx*fy/f**2
    interaction_error=float(np.max(np.abs(interaction+derivative(u)*derivative(v)/H**2)))
    require(interaction_error<1e-14,'interaction cancellation')
    def recovered(t, us, frozen=False, omit_anchor=False):
        xi,eta=(0.04,-0.02) if frozen else (0.04+0.3*t,-0.02-0.2*t)
        def R(a,b):
            return density(t,xi+a,eta+b)*density(t,xi,eta)/(density(t,xi+a,eta)*density(t,xi,eta+b))
        q=np.sqrt(1-R(0.15,0.15))
        if omit_anchor:
            q=action(0.15)/(2-action(0.15))
        T=(1-R(us,0.15))/q
        return 2*T/(1+T)
    us=np.linspace(-0.18,0.18,31)
    action_error=max(float(np.max(np.abs(recovered(t,us)-action(us,t)))) for t in (-0.01,0,0.01))
    require(action_error<1e-10,'signed scalar-anchor recovery')
    eps=1e-4
    expected=us*us/10+us**3/40
    observed=(recovered(eps,us)-recovered(-eps,us))/(2*eps)
    derivative_error=float(np.max(np.abs(observed-expected)))
    require(derivative_error<2e-7,'translated action derivative')
    frozen=(recovered(eps,us,True)-recovered(-eps,us,True))/(2*eps)
    noanchor=(recovered(eps,us,False,True)-recovered(-eps,us,False,True))/(2*eps)
    frozen_error=float(np.max(np.abs(frozen-expected)))
    anchor_error=float(np.max(np.abs(noanchor-expected)))
    require(frozen_error>1e-3 and anchor_error>1e-3,'negative derivative controls')
    dotH=-(u*u/10+u**3/40+v*v/10+v**3/40)+0.3*derivative(u)-0.2*derivative(v)
    dotw=weight*(0.3*xx+0.2*yy)
    Z=normalizer(0)
    dotZ=float(np.sum(ww*(dotw*H+weight*dotH)))
    dotp=(dotw*H+weight*dotH)/Z-density(0,xx,yy)*dotZ/Z
    fd=(density(eps,xx,yy)-density(-eps,xx,yy))/(2*eps)
    normalizer_error=float(np.max(np.abs(dotp-fd)))
    require(normalizer_error<1e-8,'fixed-window normalizer derivative')
    require(abs(float(np.sum(ww*dotp)))<1e-13,'derivative integrates to zero')
    omitted_Z_mass=float(np.sum(ww*(dotw*H+weight*dotH)/Z))
    require(abs(omitted_Z_mass)>1e-3,'normalizer-omission control')
    d=3.0
    zw=z[:,None]; yw=z[None,:]; weights=w[:,None]*w[None,:]
    def quadratic_density(a,h):
        T=(a*h*h*z*z/2)/(d-a*h*h*z*z/2)
        den=4-float(np.sum(w*T))**2
        return (1-T[:,None]*T[None,:])/den
    exact_coefficient=Fraction(7,16200)*Fraction(9,81)
    rows=[]
    for h in (0.3,0.15,0.075,0.0375,0.01875):
        p,q=quadratic_density(1,h),quadratic_density(2,h)
        H2=float(np.sum(weights*((p-q)/(np.sqrt(p)+np.sqrt(q)))**2))
        TV=float(np.sum(weights*np.abs(p-q))/2)
        require(abs(float(np.sum(weights*p))-1)<1e-12,'quadrature normalization')
        rows.append({'h':h,'TV_over_h4':TV/h**4,'H2_over_h8':H2/h**8})
    require(abs(rows[-1]['H2_over_h8']/float(exact_coefficient)-1)<0.001,'eighth-order asymptotic')
    require(abs(rows[-1]['TV_over_h4']/rows[-2]['TV_over_h4']-1)<0.001,'fourth-order asymptotic')
    integral=Fraction(4,25)-Fraction(4,81)
    require(integral*Fraction(9,16*16*81)==exact_coefficient,'exact Hellinger coefficient')
    out={'status':'passed','scope':'Independent finite functional calculations; not full proof or a billiard simulation','interaction_max_error':interaction_error,'signed_action_max_error':action_error,'action_derivative_max_error':derivative_error,'negative_frozen_origins_error':frozen_error,'negative_omitted_anchor_derivative_error':anchor_error,'fixed_window_normalizer_max_error':normalizer_error,'negative_omitted_normalizer_mass':omitted_Z_mass,'small_window_H2_coefficient':str(exact_coefficient),'small_window_quadrature':rows,'optimization_independence':'Explicit exceptions, no assert statements','mathematical_claim':'The report supplies the analytic derivation; the finite quadrature only corroborates it.'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
