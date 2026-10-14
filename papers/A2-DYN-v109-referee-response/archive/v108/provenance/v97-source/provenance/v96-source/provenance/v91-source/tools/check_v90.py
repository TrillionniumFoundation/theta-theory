#!/usr/bin/env python3
"""Finite regression fixtures only; not a certificate for the continuum proofs."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
from check_v77 import require


def checks() -> dict:
    counts = {}
    def test(group: str, ok: bool, message: str) -> None:
        require(ok, message)
        counts[group] = counts.get(group, 0) + 1
    # A time u in a surviving segment can be visited from at most min(h,u-a) roofs.
    for a, length, h, j0, jlen, frac in itertools.product(
            (F(-2),F(0)), (F(1),F(3)), (F(1,8),F(1,2),F(2)),
            (F(-3),F(0),F(1)), (F(1,3),F(4)), (F(1,8),F(1,2),F(7,8))):
        b=a+length;u=a+length*frac
        lo=max(a,u-h,j0);hi=min(u,b-h,j0+jlen)
        mult=max(F(0),hi-lo)
        test('intermediate_roof_multiplicity',mult<=min(h,u-a),'survivor multiplicity')
    # Prefix endpoints are varied independently; no angular smoothness is assumed.
    for f0,f1,t,c,h in itertools.product((F(0),F(1,3),F(2)),repeat=5):
        lhs=abs(f1*int(t+h<c)-f0*int(t<c))
        rhs=abs(f1-f0)+f0*int(t<c<=t+h)
        test('exact_prefix_product',lhs<=rhs,'prefix product difference')
    for rho,hfrac,gap in itertools.product((F(1,16),F(1,4),F(2)),
                                         (F(1,32),F(1,8),F(1,4)),
                                         (F(1),F(2),F(5))):
        a=F(-3);c=a+gap*rho;h=rho*hfrac
        for vfrac,tfrac in itertools.product((F(1,4),F(3,8),F(1,2)),(F(0),F(1,2),F(1))):
            anchor=c-vfrac*rho;t=c-tfrac*h
            test('far_anchor_geometry',a<anchor<=t<=c,'anchor before crossing')
            test('far_anchor_geometry',anchor-a>=rho/2,'radial lower bound at anchor')
    for h,d in itertools.product((1e-12,1e-6,.01,.4),(1e-14,1e-8,.003,.1,2.)):
        test('radial_kernel_payment',min(h,d)*d**(-3/8)<=h**(5/8)*(1+1e-12),'fractional radial payment')
        test('radial_kernel_payment',min(h,d)/math.sqrt(d)<=math.sqrt(h)*(1+1e-12),'guard radial payment')
    gamma=F(1,32);eta=F(1,4);kappa=(1-eta)/2;choice=F(32,33)
    test('exact_exponents',choice*gamma==1-choice==F(1,33),'prefix balance')
    test('exact_exponents',1-choice*kappa==F(7,11),'far optical exponent')
    test('exact_exponents',F(129,128)/2>gamma,'backward critical leading power')
    test('exact_exponents',F(33)*128==4224,'cofinal epsilon coefficient')
    # Test the physical cap retained at every count, not an uncapped spectral error.
    for theta,s,m in itertools.product((.2,.5,.9), (1e-32,1e-16,1e-8,.01,.5), range(2,181)):
        a=-math.log(theta)
        bound=100*(1+a**-3)*math.sqrt(s)*(1+abs(math.log(s)))**3
        test('capped_count_envelope',m**3*min(theta**m,math.sqrt(s))<=bound,'capped count envelope fixture')
    # Exact L1 translation for zero-extended constant pulses, including tiny residence.
    for length,h in itertools.product((F(1,1024),F(1,8),F(1),F(3)),
                                     (F(1,2048),F(1,16),F(1,2),F(4))):
        overlap=max(F(0),length-h)
        oscillation=2*(length-overlap)
        test('complete_pulse_ends',oscillation==2*min(length,h),'both pulse ends retained')
        test('complete_pulse_ends',float(oscillation)<=2*float(h)**(1/33) or h>1,'pulse does not imply height closure')
    # Finite-count interpolation integral, evaluated before any limit.
    chi=1/33;h0=.2
    for s,A,mu in itertools.product((chi/4,chi/2,3*chi/4),(0.1,1.,7.),(1e-18,1e-9,.02,.7,10.)):
        logcut=math.log(2*mu/A)/chi
        if logcut<math.log(h0):
            val=A*math.exp((chi-s)*logcut)/(chi-s)+2*mu*(math.exp(-s*logcut)-h0**(-s))/s
        else:val=A*h0**(chi-s)/(chi-s)
        bound=2*(1/(chi-s)+1/s)*(A**(s/chi)*mu**(1-s/chi)+mu*h0**(-s))
        test('mass_variation_interpolation',val<=bound*(1+1e-10),'integrated min envelope')
    for ss in (F(1,132),F(1,66),F(1,44)):
        expo=(1-33*ss)/128;N=F(4224)*ss/(1-33*ss)+1
        test('cofinal_limit_order',expo>0 and N*expo-33*ss>0,'outer cutoffs after fixed-count bound')
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite rational identities, interval geometry, radial kernels, physical caps and interpolation fixtures',
            'continuum_proof_certificate':False,'independent_human_review':False,
            'essential_height_charge_zero_proved':False}

if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
