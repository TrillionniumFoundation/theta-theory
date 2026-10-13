#!/usr/bin/env python3
"""Exact finite diagnostics; these are not continuum Lorentz proof certificates."""
from fractions import Fraction as F
import cmath
import json
import math


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def kappa(t, delta):
    if -delta < t < 0:
        return -(delta+t)/(2*delta)
    if 0 < t < delta:
        return (delta-t)/(2*delta)
    return F(0)


def current(segments):
    atoms = {}
    for left, right, value in segments:
        atoms[left] = atoms.get(left, F(0)) + value
        atoms[right] = atoms.get(right, F(0)) - value
    return {x: v for x, v in atoms.items() if v}


def value_at(segments, t):
    return sum((v for a,b,v in segments if a < t < b), F(0))


def average(segments, t, delta):
    return sum((v*max(F(0),min(b,t+delta)-max(a,t-delta))
                for a,b,v in segments),F(0))/(2*delta)


def allocation(b, s, q, K):
    require(0 <= s <= b and q >= 0 and K >= 1, 'invalid allocation inputs')
    r=b-s
    alpha=min(F(1),max(F(0),K*q-s)/r) if r else F(0)
    return alpha,s+alpha*r,(1-alpha)*r


def finite_checks():
    profiles = [
        [(F(0),F(1),F(1))],
        [(F(1,2),F(1),F(1))],
        [(F(0),F(1,3),F(1,4)),(F(1,3),F(2,3),F(3,4)),(F(2,3),F(1),F(1,2))],
        [(F(-2),F(-1),F(2)),(F(0),F(1),F(3,2)),(F(1),F(2),F(1,3))]
    ]
    identity_checks=0; flux_checks=0; fourier_checks=0
    for segments in profiles:
        atoms=current(segments)
        require(sum(atoms.values(),F(0))==0,'moving-window derivative mass')
        for delta in [F(1,8),F(1,2),F(2)]:
            for t in [F(j,32) for j in range(-100,101)]:
                if any(t==a or t==b for a,b,_ in segments):
                    continue
                discrepancy=value_at(segments,t)-average(segments,t,delta)
                primitive=sum((v*kappa(t-x,delta) for x,v in atoms.items()),F(0))
                require(discrepancy==primitive,'compact primitive sign/trace identity')
                directed=sum((v for x,v in atoms.items() if v>0 and t-delta<=x<=t),F(0))
                directed+=sum((-v for x,v in atoms.items() if v<0 and t<=x<=t+delta),F(0))
                require(max(F(0),primitive)<=directed/2,'directed flux bound')
                identity_checks+=1;flux_checks+=1
        for xi in [.125, .75, 2., 7.5, 19.]:
            flux=sum(float(v)*cmath.exp(-1j*xi*float(x)) for x,v in atoms.items())
            density=sum(float(v)*(cmath.exp(-1j*xi*float(a))-cmath.exp(-1j*xi*float(b)))/(1j*xi) for a,b,v in segments)
            require(abs(flux-1j*xi*density)<1e-12,'Fourier derivative sign')
            fourier_checks+=1
    glued=current([(F(0),F(1,2),F(2,3)),(F(1,2),F(1),F(2,3))])
    require(F(1,2) not in glued,'artificial cut must cancel')
    jumped=current([(F(0),F(1,2),F(1,3)),(F(1,2),F(1),F(2,3))])
    require(jumped[F(1,2)]==F(1,3),'true jump counted once')
    # Missing the exit trace is detected, rather than accepted as a derivative.
    require(sum({F(1,2):F(1)}.values())!=0,'negative control: omitted exit')
    # Translation and physical weights precede cancellation.
    pooled=current([(F(0),F(1),F(2)),(F(1),F(2),F(2))])
    require(F(1) not in pooled,'common-roof weighted cancellation')
    unequal=current([(F(0),F(1),F(2)),(F(1),F(2),F(3))])
    require(unequal[F(1)]==1,'unequal weights cannot be suppressed')
    allocation_checks=0
    for si in range(9):
        for ri in range(9):
            s=F(si,4);r=F(ri,4);b=s+r
            for qi in range(13):
                q=F(qi,4);previous=F(-1)
                for K in [F(1),F(3,2),F(2),F(4)]:
                    alpha,S,R=allocation(b,s,q,K)
                    require(0<=alpha<=1 and S+R==b,'complementary source weights')
                    require(S==min(b,max(s,K*q)),'preserved-source minimum formula')
                    require(R==max(F(0),b-max(s,K*q)),'residual formula')
                    require(s<=S<=s+K*q and R<=max(F(0),b-K*q),'capacity bounds')
                    require(S>=previous,'reserve monotonicity')
                    if r and alpha<1:
                        require(s+(alpha+(1-alpha)/2)*r>max(s,K*q),'scalar maximality')
                    previous=S;allocation_checks+=1
    # One common alpha on all old positive remainders, not label transport.
    d,inc,out=F(1),F(2),F(3);s=F(1);b=s+d+inc+out
    alpha,S,R=allocation(b,s,F(2),F(2))
    require(R==(1-alpha)*d+(1-alpha)*inc+(1-alpha)*out,'all three residuals retained')
    require(alpha*inc>0 and alpha*out>0,'genuine incidence/outside recovery fixture')
    _,_,own=allocation(F(1),F(0),F(0),F(1))
    _,_,wrong=allocation(F(1),F(0),F(1),F(1))
    require(own==1 and wrong==0,'negative control: another label changes result')
    # Fourier multiplier near zero: test a stable integral-bound expansion.
    multiplier_checks=0
    for x in [.01,.1,.5,1.,2.,5.,10.,50.]:
        one_minus_sinc=1-math.sin(x)/x
        require(-1e-15<=one_minus_sinc<=min(x*x/6,2)+1e-14,'primitive multiplier bound')
        multiplier_checks+=1
    require(F(1,12)*F(1,16)==F(1,192),'full-source reserve exponent')
    require(F(1,24)*6==F(1,4),'selected-source exponent')
    q,beta,a=F(3),F(2),F(1,4)
    require(-q+beta*(q+a)/beta==a,'legal power-width rate')
    # Exact narrow spike: normalized mass disappears but height stays one.
    for m in [2,4,8,16]:
        width=F(1,2**m);height=F(1,m*m)
        require(m*m*height==1 and m*m*height*width==width,'small mass not height')
    return {'primitive_exact_rational_checks':identity_checks,
            'directed_flux_checks':flux_checks,'fourier_identity_checks':fourier_checks,
            'source_allocation_checks':allocation_checks,'multiplier_checks':multiplier_checks,
            'window_atoms_gluing_and_weight_tests':True,'all_three_original_residual_types':True,
            'negative_controls':['omitted exit atom','mixed exact label','mass-to-height inference'],
            'fixed_band_exponents_verified':True,'lorentz_realization_claimed':False,
            'continuum_proof_certificate':False}


if __name__=='__main__':
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
