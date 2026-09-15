#!/usr/bin/env python3
"""Reviewer-written finite controls for A2 v53. Imports no author code.

Run with Python 3 and NumPy, ordinarily and with -O.  Explicit exceptions
remain active under optimization.  Synthetic quartic actions below test
Taylor formulas, not the realization of arbitrary billiard actions.  The
infinite-dimensional and statistical arguments are in REFEREE_REPORT.md.
"""
from __future__ import annotations
from fractions import Fraction as F
import json
import math
import numpy as np


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def close(x: float, y: float, tolerance: float, message: str) -> None:
    require(math.isfinite(x) and abs(x-y) <= tolerance, message)


def main() -> None:
    R, g = F(1, 10), F(4, 5)
    ss = [R/128, R/64]
    curvature = [1/(R-16*s) for s in ss]
    a2 = [k*k+2*k/g for k in curvature]
    require(a2 == [F(7800, 49), F(1900, 9)], 'Actual Hessian coefficients')
    delta = a2[1]-a2[0]
    require(delta == F(22900, 441), 'Squared Hessian contrast')
    min_radius = R-16*ss[1]
    require(min_radius == 3*R/4, 'Uniform curvature-radius margin')
    c = [1+g*k for k in curvature]
    gamma = [math.acosh(float(v)) for v in c]
    require(gamma[1] > gamma[0] > 0, 'Distinct positive escape exponents')
    # Compute the quadratic half-line energy directly along x_j = exp(-gamma*j).
    # A single flight contributes [c(x_j^2+x_{j+1}^2)-2x_j*x_{j+1}]/(2g).
    energy_controls = []
    for cc, gam, expected in zip(c, gamma, a2):
        x = np.exp(-gam*np.arange(65, dtype=float))
        twice_energy = np.sum((float(cc)*(x[:-1]**2+x[1:]**2)
                               -2*x[:-1]*x[1:])/float(g))
        close(float(twice_energy), math.sqrt(float(expected)), 1e-11,
              'Direct half-line quadratic energy')
        energy_controls.append(float(twice_energy))

    # F(z,w) = 1/9-z^2*w^2, with Lebesgue integration on [-1,1]^2.
    integral_F = 4*F(1,9)-F(2,3)**2
    integral_F2 = 4*F(1,81)-2*F(1,9)*F(2,3)**2+F(2,5)**2
    require(integral_F == 0 and integral_F2 == F(224,2025), 'Moment integrals')
    variance = integral_F2/4
    Hcoef = delta**2*integral_F2/256  # coefficient multiplied by d^4
    Jcoef = delta**2*integral_F2/64
    mean_contrast = delta*integral_F2/16  # coefficient multiplied by d^2
    require(Hcoef == 7*delta**2/16200 and Jcoef == 4*Hcoef, 'Hellinger / LAN')
    require(mean_contrast**2/variance == Jcoef, 'Efficient bounded statistic')

    # A negative control: omitting the normalizer drops the constant 1/9.
    wrong_Hcoef = delta**2*F(4,25)/256
    require(wrong_Hcoef != Hcoef, 'Normalizer omission not detected')

    nodes, weights = np.polynomial.legendre.leggauss(100)
    z, w = nodes[:,None], nodes[None,:]
    ww = weights[:,None]*weights[None,:]
    statistic = 1/9-z*z*w*w
    hs = [0.08, 0.04, 0.02, 0.01]
    rows = []
    for h in hs:
        densities = []
        for aq, quartic in zip(a2, [0.7, 1.1]):
            u = h*nodes
            action = math.sqrt(float(aq))*u*u/2+quartic*u**4
            t = action/(1-action)  # synthetic test at d=1
            I = float(weights@t)
            q = (1-t[:,None]*t[None,:])/(4-I*I)
            close(float(np.sum(ww*q)), 1.0, 1e-13, 'Quadrature normalization')
            require(bool(np.all(q > 0)), 'Positive square density')
            densities.append(q)
        p, q = densities
        H2 = float(np.sum(ww*((q-p)/(np.sqrt(q)+np.sqrt(p)))**2))
        moments = [float(np.sum(ww*v*statistic)) for v in densities]
        hratio = H2/(h**8*float(Hcoef))
        rows.append({'h':h, 'H2_over_predicted_leading_term':hratio,
                     'mean_contrast_over_predicted':
                       (moments[1]-moments[0])/(h**4*float(mean_contrast))})
    require(abs(rows[-1]['H2_over_predicted_leading_term']-1) < 0.005,
            'Higher-order action Hellinger asymptotic')
    require(abs(rows[-1]['mean_contrast_over_predicted']-1) < 0.005,
            'Higher-order action moment asymptotic')
    require(all(abs(rows[j+1]['H2_over_predicted_leading_term']-1)
                < abs(rows[j]['H2_over_predicted_leading_term']-1)
                for j in range(len(rows)-1)), 'Hellinger asymptotic convergence')

    # Product affinity identity: no fitted Monte Carlo approximation.
    affinity_checks = []
    for epsilon, n in [(1e-3,100),(1e-4,10000),(1e-5,1000000)]:
        p = np.full((100,100), 0.25)
        q = p+epsilon*statistic
        H2 = float(np.sum(ww*((q-p)/(np.sqrt(q)+np.sqrt(p)))**2))
        product_H2 = -2*math.expm1(n*math.log1p(-H2/2))
        require(product_H2 <= n*H2+1e-13, 'Affinity tensorization bound')
        affinity_checks.append({'epsilon':epsilon,'n':n,'H2':H2,
                                'product_H2':product_H2,'n_H2':n*H2})

    # Geometric waiting-time error bound. Probabilities here are diagnostic,
    # not numerically asserted values of the physical billiard acceptance.
    waiting_checks = []
    for rho in [1e-2,1e-4,1e-6]:
        p0, p1 = 0.01, 0.01*rho
        m = math.ceil(1/math.sqrt(p0*p1))
        err0 = math.exp(m*math.log1p(-p0))
        err1 = -math.expm1(m*math.log1p(-p1))
        upper = 0.5*(math.exp(-1/math.sqrt(rho))+math.sqrt(rho)+p1)
        error = 0.5*(err0+err1)
        require(error <= upper+1e-14, 'One-waiting-count test bound')
        waiting_checks.append({'rho':rho,'threshold':m,
                               'equal_prior_error':error,'proved_upper':upper})
    out = {'status':'PASS','imports_author_code':False,
           'proof_certificate':False,
           'actual_family':{'curvature_radius_lower':str(min_radius),
                            'a_squared':[str(v) for v in a2],
                            'delta':str(delta),'gamma':gamma,
                            'direct_quadratic_energy':energy_controls},
           'exact_coefficients':{'integral_F2':str(integral_F2),
                                 'variance_uniform':str(variance),
                                 'H2_coefficient_times_d4':str(Hcoef),
                                 'LAN_coefficient_times_d4':str(Jcoef),
                                 'normalizer_omission_detected':True},
           'synthetic_quartic_actions':rows,
           'product_affinity_controls':affinity_checks,
           'geometric_waiting_controls':waiting_checks}
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
