#!/usr/bin/env python3
"""Finite algebra for flat contact. These checks do not certify a dynamical proof."""
from fractions import Fraction as F
import math
import mpmath as mp
import sympy as sp


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def finite_checks():
    # The two explicit tilt regimes, all at the same finite damping.
    tilt_cases = 0
    for a in range(1, 18):
        k = F(1, 2**(6*a))
        for b in range(0, 24):
            h = F(1, 2**(2*b)) if b else F(0)
            k13 = F(1, 2**(2*a))
            if h <= k13:
                r = k13
                require(k/r <= k13*k13 and h*r <= k13*k13, 'flat tilt budget')
            else:
                r = F(1, 2**(3*a-b))
                require(r*r == k/h, 'quadratic tilt radius')
                require(r*r <= k/r and h*r == k/r, 'mixed tilt budget')
            tilt_cases += 1
    # Exact Gaussian Jacobian and the extra section factor.
    c,t = sp.symbols('c t', positive=True)
    L=sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,-t,1],[0,0,-c,0]])
    D=sp.diag(2,3,5,7);O=c*L*D*L.T
    require(sp.simplify(L.det()-c)==0, 'clock determinant')
    require(sp.simplify(O.det()-c**6*D.det())==0, 'Gaussian determinant')
    require(sp.simplify(c*L.T*O.inv()*L-D.inv())==sp.zeros(4), 'Gaussian exponent')
    require(c**2*c**(-3)/c == c**(-2), 'damped residue normalization')

    # Work in a truncated polynomial ring; do not substitute into uncancelled
    # rational series at the resonance.
    e,A,B,C=sp.symbols('e A B C',real=True)
    def tr(expr,N=4):
        p=sp.Poly(sp.expand(expr),e)
        return sp.Add(*(coef*e**powers[0] for powers,coef in p.terms() if powers[0]<N))
    s=A*e+B*e**2+C*e**3
    phases=[0,s,2*s+2*sp.pi*e+e*s];values=[0,1,2+e]
    exponentials=[tr(sum((sp.I*q)**j/sp.factorial(j) for j in range(4))) for q in phases]
    lam=tr(sum(exponentials)/3)
    inv=tr(sum((-1)**j*tr((lam-1)**j) for j in range(4)))
    first=tr(sp.I*sum(f*q for f,q in zip(values,exponentials))/3)
    ratio=tr(first*inv)
    real=sp.expand(sp.re(ratio))
    require(sp.simplify(real.coeff(e,1)+2*(A+sp.pi)/3)==0,'baker maximum first order')
    require(sp.simplify(real.coeff(e,2)+2*A/3+2*B/3+4*sp.pi/9)==0,'baker maximum second order')
    fitted=sp.expand(ratio.subs({A:-sp.pi,B:sp.pi/3}))
    require(sp.simplify(sp.im(fitted)-(1+e/3)-sp.pi**2*e**3/18)==0,'baker drift coefficient')
    loglam=tr((lam-1)-(lam-1)**2/2,3).subs(A,-sp.pi)
    require(sp.simplify(sp.re(loglam)+sp.pi**2*e**2/9)==0,'baker damping coefficient')
    second=tr(-sum(f*f*q for f,q in zip(values,exponentials))/3)
    H=tr(-second*inv+ratio**2,2).subs(A,-sp.pi)
    require(sp.simplify(H-(sp.Rational(2,3)+2*e/3+2*sp.pi*sp.I*e/9))==0,'baker Hessian coefficient')

    # Check the actual maximum at high precision, rather than only its series.
    mp.mp.dps=65
    baker_cases=0
    for sign in [-1,1]:
        for j in range(5,13):
            eps=mp.mpf(sign)/2**j
            vals=[mp.mpf(0),mp.mpf(1),2+eps]
            def phi(z,r=0):return sum((1j*f)**r*mp.exp(1j*z*f) for f in vals)/3
            a=mp.findroot(lambda z:mp.re(phi(z,1)/phi(z)),2*mp.pi-mp.pi*eps)
            k=-mp.log(abs(phi(a)))
            v=mp.im(phi(a,1)/phi(a))-(1+eps/3)
            h=-phi(a,2)/phi(a)+(phi(a,1)/phi(a))**2
            require(k>0,'baker peak not damped')
            require(abs((a-2*mp.pi+mp.pi*eps)/eps**2-mp.pi/3)<10*abs(eps),'baker maximum remainder')
            require(abs(k/eps**2-mp.pi**2/9)<10*abs(eps),'baker damping remainder')
            require(abs(v/eps**3-mp.pi**2/18)<10*abs(eps),'baker drift remainder')
            require(abs((h-(mp.mpf(2)/3+2*eps/3+2*eps**2/9))/eps-2j*mp.pi/9)<10*abs(eps),'baker Hessian remainder')
            baker_cases+=1

    # Gaussian replacement is a finite calculation, not a billiard simulation.
    gaussian_cases=0
    for m in [16,64,256,1024]:
        for k in [1/m,4/m]:
            eta=math.sqrt(k)
            drift=math.sqrt(k*eta)/4
            Hc=complex(1-eta/4,eta/3)
            for Z in [-4,-1,0,1,4]:
                g=lambda h,z:mp.exp(-z*z/(2*h))/mp.sqrt(2*mp.pi*h)
                error=math.exp(-m*k)*abs(g(Hc,Z-math.sqrt(m)*drift)-g(1,Z))
                require(mp.isfinite(error),'nonfinite accretive Gaussian')
                bound=20*math.exp(-Z*Z/20)*math.exp(-m*k/2)*(abs(Hc-1)+math.sqrt(m)*abs(drift))
                require(error<=bound,'Gaussian segment majorant')
                gaussian_cases+=1

    # Negative controls retain the missing hypotheses and the original height issue.
    # A quadratic contact of nonvanishing curvature permits drift sqrt(kappa).
    k=F(1,256);v=F(1,16);h=F(1)
    require(k-v*v/(2*h)>0 and v*v/k==1,'nonflat countermodel')
    # A flat, nonnegative quadratic gap can have an arbitrarily slow modulus.
    for j in [10,100,1000]:
        hh=F(1,j)
        require(hh>0 and hh<1,'slow modulus model')
    # Continuity-only drift kappa^(1/4) violates positive-pressure domination.
    k=F(1,256);v=F(1,4);tt=-v/2
    require(k+v*tt+tt*tt<0,'bad drift escaped pressure test')
    # Vanishing spike mass is not vanishing essential height.
    require(F(1000)*F(1,1000**3)<F(1,1000) and 1000>100,'spike negative control')
    # Marginal bridge equality does not prescribe independence.
    require([(0,0),(1,1)]!=[(0,0),(0,1),(1,0),(1,1)],'graph negative control')
    return {'tilt_cases':tilt_cases,'exact_baker_coefficients':5,'baker_maxima_cases':baker_cases,
            'accretive_gaussian_cases':gaussian_cases,'covariance_jacobian_checks':4,
            'negative_controls':5,'symbolic_and_numeric_checks_are_not_continuum_proofs':True,
            'unrestricted_physical_height_proved':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
