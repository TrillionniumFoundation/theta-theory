#!/usr/bin/env python3
"""Independent finite diagnostics for A2 v5 at 1e57d9c.
No repository imports/network calls. Exact identities and non-interval
quadrature are explicitly separated; neither certifies continuum theorems.
Usage: python independent_diagnostics.py > DIAGNOSTICS.json
"""
from __future__ import annotations
import json
import platform
import math
import numpy as np
import scipy
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
import sympy as sp

checks: list[dict] = []

def exact(name: str, residual) -> None:
    value = sp.factor(sp.simplify(residual))
    if value != 0:
        raise RuntimeError(f'{name}: nonzero exact residual {value}')
    checks.append({'name': name, 'kind': 'exact', 'passed': True})

def bounded(name: str, value: float, target: float, tolerance: float) -> None:
    if not math.isfinite(value) or abs(value-target) > tolerance:
        raise RuntimeError(f'{name}: {value} versus {target}; tolerance {tolerance}')
    checks.append({'name': name, 'kind': 'ordinary_floating_non_interval',
                   'value': value, 'target': target, 'absolute_tolerance': tolerance,
                   'passed': True})

c = sp.symbols('c', positive=True)
f = [sp.S.One, 1/(2*c), 1/(4*c*c-1), 1/(4*c*(2*c*c-1))]
W = sp.factor(sp.Matrix([[sp.diff(fi,c,k) for k in range(4)] for fi in f]).det())
W_printed = 12*(64*c**8+32*c**6+116*c**4+4*c*c+1)/(c**4*(4*c*c-1)**4*(2*c*c-1)**4)
exact('four_amplitude_Wronskian', W-W_printed)

r,g = sp.symbols('r g', positive=True)
phi1 = r/sp.sqrt(g*(g+2*r))
exact('third_radius_derivative', sp.diff(phi1,r,3)-3*(3*g+r)/(sp.sqrt(g)*(g+2*r)**sp.Rational(7,2)))
exact('physical_two_sided_cubic_multiplier', sp.Rational(36**3+2*(-18)**3,3)-11664)

R,al,be,ze,e1,e2,P,A = sp.symbols('R al be ze e1 e2 P A', positive=True)
# Support h=R+(1-cos(6t))*(al+be*cos(2t)+ze*sin(2t)).
# Area follows independently from the Fourier identity, with P standing for pi.
harmonics = {2:(be,ze),4:(-be/2,ze/2),6:(-al,0),8:(-be/2,-ze/2)}
area_fourier = P*(R+al)**2 + P/2*sum((1-n*n)*(aa*aa+bb*bb) for n,(aa,bb) in harmonics.items())
area_printed = P*(R**2+2*R*al-sp.Rational(33,2)*al**2-sp.Rational(45,4)*(be**2+ze**2))
exact('support_function_area_Fourier_identity', area_fourier-area_printed)
area_symmetric = P*(R**2+R*e1/54-sp.Rational(41,7776)*e1**2+sp.Rational(5,432)*e2)
substituted = P*(R**2+2*R*e1/108-sp.Rational(33,2)*(e1/108)**2-sp.Rational(45,4)*(e1**2/2916-e2/972))
exact('physical_area_in_symmetric_coordinates', substituted-area_symmetric)

# New referee calculation: first THREE amplitudes suffice locally in the
# physical family near R=1/4, g=1/2, where area is constrained by shape.
phis = [phi1,phi1*r/(2*(r+g)),phi1*r*r/(4*(r+g)**2-r*r)]
vals = [[sp.simplify(sp.diff(fi,r,k).subs({r:sp.Rational(1,4),g:sp.Rational(1,2)})) for k in range(4)] for fi in phis]
M = sp.Matrix([[v[1]+P*v[0]/(72*A),-v[2]+5*P*v[0]/(144*A),v[3]/2] for v in vals])
D3 = sp.factor(M.det()/A**3)
D3_printed = -2*sp.sqrt(2)*(15804720*A+64253*P)/(72930375*A**4)
exact('three_amplitude_physical_Jacobian_at_R_quarter', D3-D3_printed)

lam,a,nu = sp.symbols('lam a nu', positive=True)
for m in range(2,9):
    k=m-1
    # Independent angular and radial moment integration constants.
    angular = 2*sp.pi*sp.binomial(2*k,k)/4**k
    weighted_radial = sp.Rational(1,2*(k+1)*(k+2))
    moment = sp.simplify(angular*(2/a)**k*weighted_radial/(sp.pi/2))
    printed_moment = 2*sp.binomial(2*k,k)/(2**k*(k+1)*(k+2)*a**k)
    exact(f'weighted_disk_moment_order_{k}',moment-printed_moment)
    angular_m = 2*sp.pi*sp.binomial(2*m,m)/4**m
    action_coefficient = -sp.simplify(2*angular_m*(2/a)**(m+1)/(2*m+2)/sp.factorial(2*m)/(sp.pi/a))
    Km=sp.Rational(4,2**m*(m+1)*sp.factorial(m)**2)/a**m
    exact(f'action_diagonal_order_{2*m}',action_coefficient+Km)
    Dm=lam**(2*m-2)/(1-lam**(2*m-2))-lam**(2*m)/(1-lam**(2*m))
    B=(1+lam**(2*m))/(1-lam**(2*m))+2*m*Dm
    # a*nu=coth(gamma), hence finite/limiting sensitivity ratio below.
    ratio = ((1-lam**2)/(1+lam**2))**m*B
    gamma=math.acosh(2.0)
    ratio_num=float(ratio.subs(lam,math.exp(-gamma)))
    direct=(math.tanh(gamma)**m)*(1/math.tanh(m*gamma)+2*m*(1/math.expm1(2*(m-1)*gamma)-1/math.expm1(2*m*gamma)))
    bounded(f'limiting_to_one_flight_ratio_m_{m}',ratio_num,direct,1e-12)

for m in range(1,11):
    weights=[(-1)**(l-1)*sp.binomial(m,l) for l in range(1,m+1)]
    exact(f'extrapolation_constant_m_{m}',sum(weights)-1)
    for k in range(1,m):
        exact(f'extrapolation_m_{m}_power_{k}',sum(weights[l-1]*l**k for l in range(1,m+1)))
    exact(f'harmonic_timing_m_{m}',sum(weights[l-1]/l for l in range(1,m+1))-sp.harmonic(m))

# Actual one-flight length and twist, NOT evaluation of the asserted formula.
# Local polynomial graph only: this is not a whole-table equilibrium simulation.
u,v,q = sp.symbols('u v q', real=True)
base_s = 1+(u*u+v*v)/2
length = sp.sqrt(base_s**2+(v-u)**2)
b_expr = -sp.diff(length,u,v)
b_fn = sp.lambdify((u,v),b_expr,'numpy',cse=True)
length_fn = sp.lambdify((u,v),length,'numpy',cse=True)
H = np.array([[2.0,-1.0],[-1.0,2.0]])
eig,Q = np.linalg.eigh(H)
Hinvroot = (Q*(1/np.sqrt(eig)))@Q.T
n_theta,n_radial = 96,32
nodes,weights = leggauss(n_radial)
quadrature_records=[]
for m in (2,3,4,5):
    dlength=base_s/length*(u**(2*m)+v**(2*m))/sp.factorial(2*m)
    db=-sp.diff(dlength,u,v)
    dl_fn=sp.lambdify((u,v),dlength,'numpy',cse=True)
    db_fn=sp.lambdify((u,v),db,'numpy',cse=True)
    target=-4*(2/3)**m/(2**m*(m+1)*math.factorial(m)**2)
    estimates=[]
    for d in (0.004,0.001,0.00025):
        total=0.0
        for theta in 2*math.pi*np.arange(n_theta)/n_theta:
            direction=math.sqrt(2*d)*(Hinvroot@np.array([math.cos(theta),math.sin(theta)]))
            def excess(t: float) -> float:
                return float(length_fn(*(direction*t)))-1-d
            upper=brentq(excess,0.0,2.0,xtol=1e-14)
            radii=upper*(nodes+1)/2
            uu=direction[0]*radii
            vv=direction[1]*radii
            E=length_fn(uu,vv)-1
            integrand=(-dl_fn(uu,vv)*b_fn(uu,vv)+(d-E)*db_fn(uu,vv))*radii
            total += float(np.sum(weights*integrand)*upper/2)
        derivative=2/(math.pi*d)*total*(2*math.pi/n_theta)
        slope=derivative/d**(m-1)
        estimates.append(slope)
        # Modest finite-d relative tolerance, not an interval error certificate.
        bounded(f'actual_one_flight_q{2*m}_offset_{d:g}',slope,target,0.05*abs(target))
    if abs(estimates[-1]-target) >= abs(estimates[0]-target):
        raise RuntimeError(f'one-flight q{2*m}: refinement did not reduce bias')
    quadrature_records.append({'jet_order':2*m,'offsets':[0.004,0.001,0.00025],
        'coefficient_derivative_estimates':estimates,'predicted_limit':target})

result={'reviewed_commit':'1e57d9c024f90f0304e5572c0e320707bab88074',
        'environment':{'python':platform.python_version(),'numpy':np.__version__,
                       'scipy':scipy.__version__,'sympy':sp.__version__},
        'summary':{'total':len(checks),'passed':sum(z['passed'] for z in checks),
                   'exact':sum(z['kind']=='exact' for z in checks),
                   'ordinary_floating_non_interval':sum(z['kind']=='ordinary_floating_non_interval' for z in checks)},
        'new_referee_identity':{'physical_area':'A(e)=A0-pi*R*e1/54+41*pi*e1^2/7776-5*pi*e2/432',
         'three_amplitude_Jacobian_R_quarter':'-2*sqrt(2)*(15804720*A0+64253*pi)/(72930375*A0^4)',
         'A0':'sqrt(3)/2-pi/16',
         'Jacobian_numeric':float(D3_printed.subs({A:sp.sqrt(3)/2-sp.pi/16,P:sp.pi}))},
        'one_flight_quadrature':quadrature_records,'checks':checks,
        'limitations':['Finite diagnostics only; no formal or interval certification.',
         'No repository test suites, PDF build, or remote CI rerun.',
         'No infinite determinant, full sequence, or whole-table simulation certificate.',
         'Sensitivity ratios concern diagonal coefficient response at fixed lower jets, not minimax risk.',
         'Three-amplitude inverse calculation is local to the physical family near R=1/4.']}
print(json.dumps(result,indent=2,sort_keys=True))
