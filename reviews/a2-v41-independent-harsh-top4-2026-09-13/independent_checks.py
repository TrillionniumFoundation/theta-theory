#!/usr/bin/env python3
"""Independent finite controls for the source-pinned A2 v41 referee report.

This script imports no manuscript code. It is not a proof of an infinite
half-line limit, a periodic realization, a statistical equivalence theorem,
or a native TeX build. Failures use explicit exceptions (also under python -O).
"""
from __future__ import annotations
import json
import math
from fractions import Fraction as F
import numpy as np
from scipy.linalg import solve_banded

TARGET = 'c730a60bbc8af2a4c6e432813c31dccc897828e7'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def density_checks() -> dict:
    d, a = F(3), F(1, 3)
    def s(u: F) -> F:
        return u*u + u**3/F(5) + u**4/F(7)
    def b(u: F) -> F:
        return 1 + u/F(7) + u*u/F(11)
    def f(u: F, v: F) -> F:
        return F(13, 17)*b(u)*b(v)*(d-s(u)-s(v))
    def ratio(u: F, v: F) -> F:
        return f(u,v)*f(F(0),F(0))/(f(u,F(0))*f(F(0),v))
    points = [F(i, 20) for i in range(-9, 10)]
    anchor = s(a)/(d-s(a))
    require(anchor > 0, 'positive fixed anchor failed')
    require(1-ratio(a,a) == anchor**2, 'anchor identity failed')
    for u in points:
        t = (1-ratio(u,a))/anchor
        require(d*t/(1+t) == s(u), 'action inverse failed')
        require(f(u,F(0))/f(F(0),F(0))*(1+t) == b(u), 'amplitude inverse failed')
        for v in points:
            require(1-ratio(u,v) == s(u)*s(v)/((d-s(u))*(d-s(v))),
                    'rank-one defect failed')
    require(s(F(1,3)) != s(F(-1,3)), 'asymmetry negative control failed')
    return {'rational_pair_identities': len(points)**2,
            'rational_action_and_amplitude_reconstructions': 2*len(points),
            'asymmetric_action': True, 'unknown_amplitude_cancelled': True}


def orbit(g: float, kappas: tuple[float,float], start: int,
          u: float, edges: int=96) -> tuple[np.ndarray,np.ndarray,float]:
    """Solve the finite nonlinear action with x[0]=u, x[edges]=0.

    Graphs are parabolic, but Euclidean flight length and stationarity are
    nonlinear. Newton uses the analytic tridiagonal Hessian of the action.
    """
    c = [1+g*k for k in kappas]
    gamma = math.acosh(math.sqrt(c[0]*c[1]))
    indices = np.arange(edges+1)
    x = u*np.exp(-gamma*indices)
    x[1::2] *= math.sqrt(c[start]/c[1-start])
    x[-1] = 0.0
    kinds = (start + np.arange(edges)) % 2
    ky = np.array(kappas)[kinds]
    kz = np.array(kappas)[1-kinds]
    residual = float('inf')
    for _ in range(24):
        y, z = x[:-1], x[1:]
        h = g + 0.5*ky*y*y + 0.5*kz*z*z
        length = np.hypot(h,z-y)
        ay, az = h*ky*y + y-z, h*kz*z + z-y
        gy, gz = ay/length, az/length
        grad = gz[:-1] + gy[1:]
        residual = float(np.max(np.abs(grad)))
        if residual < 2e-15:
            break
        hyy = (ky*ky*y*y + h*ky + 1)/length - ay*ay/length**3
        hzz = (kz*kz*z*z + h*kz + 1)/length - az*az/length**3
        hyz = (ky*kz*y*z - 1)/length - ay*az/length**3
        diagonal = hzz[:-1] + hyy[1:]
        off = hyz[1:-1]
        band = np.zeros((3,edges-1))
        band[1] = diagonal
        band[0,1:] = off
        band[2,:-1] = off
        x[1:-1] -= solve_banded((1,1),band,grad,check_finite=True)
    require(residual < 2e-13, 'nonlinear orbit did not converge')
    y,z = x[:-1],x[1:]
    h = g+0.5*ky*y*y+0.5*kz*z*z
    return x, h/np.hypot(h,z-y), residual


def nonlinear_jet_checks() -> dict:
    cases = [(0.7,(0.3,1.8)), (1.2,(2.1,0.4)), (0.4,(0.8,0.8))]
    degrees = range(3,7)
    records = []
    max_residual = 0.0
    worst_swapped_label_error = 0.0
    for g,k in cases:
        c = [1+g*t for t in k]
        gamma = math.acosh(math.sqrt(c[0]*c[1]))
        for start in (0,1):
            for n in degrees:
                exact = [1/math.tanh(n*gamma),
                         (c[start]/c[1-start])**(n/2)/math.sinh(n*gamma)]
                errs = []
                for u in (0.04,0.02,0.01,-0.01):
                    x,weight,residual = orbit(g,k,start,u)
                    max_residual = max(max_residual,residual)
                    kinds = (start+np.arange(len(x)-1))%2
                    observed = []
                    for r in (start,1-start):
                        # This is n! dS/dq_{r,n} divided by u**n.
                        direct = weight*((kinds==r)*x[:-1]**n+
                                          ((1-kinds)==r)*x[1:]**n)
                        observed.append(float(direct.sum()/u**n))
                    err = max(abs(observed[i]-exact[i]) for i in (0,1))
                    errs.append(err)
                    if k[0] != k[1] and start == 0 and n == 3 and u == 0.01:
                        swapped = (c[1]/c[0])**(n/2)/math.sinh(n*gamma)
                        worst_swapped_label_error = max(worst_swapped_label_error,
                                                       abs(observed[1]-swapped))
                require(errs[2] < 0.002, 'finite nonlinear jet coefficient mismatch')
                require(errs[2] < 0.36*errs[1] and errs[1] < 0.36*errs[0],
                        'expected quadratic approach to jet coefficient failed')
                require(abs(errs[2]-errs[3]) < 1e-11, 'signed parity control failed')
                records.append({'gap':g,'curvatures':list(k),'start_type':start,'degree':n,
                                'errors_u_004_002_001_minus001':errs})
    require(worst_swapped_label_error > 0.01,'swapped-label negative control not detected')
    return {'finite_edges':96,'rows':len(records),'nonlinear_orbit_solves':4*len(records),
            'max_stationarity_residual':max_residual,
            'max_error_at_abs_u_001':max(r['errors_u_004_002_001_minus001'][2] for r in records),
            'swapped_label_negative_control_error':worst_swapped_label_error,'details':records}


def collar_checks() -> dict:
    # On the plane, f_theta = 2/(pi(1+theta)^2) * (1+theta-|x|^2)_+.
    # Under the null, s=1-|x|^2 has density 2s on (0,1).
    # J_Sigma = 2. Censor to s >= q = delta * (log 1/delta)^(1/4).
    rows=[]
    for logdelta in (32.,64.,128.,256.):
        delta=math.exp(-logdelta)
        q=delta*logdelta**0.25
        n=1/(delta*delta*logdelta)  # scale diagnostic, not an integer sample
        max_mass=0.0
        means=[]
        for local in (-2.,0.,2.):
            theta=delta*local
            mass=(q+theta)**2/(1+theta)**2
            require(q+theta>0,'collar not beyond alternative boundary')
            max_mass=max(max_mass,n*mass)
            mean=2*n*delta/(1+theta)**2*(-q+q*q+theta*(math.log(1/q)-2+2*q))
            means.append(mean)
        rows.append({'log_inverse_delta':logdelta,'np_delta2_log':n*delta**2*logdelta,
                     'max_union_censoring_bound_h_minus2_0_2':max_mass,
                     'central_means_h_minus2_0_2':means,
                     'null_second_moment_budget':2*n*delta**2*(math.log(1/q)-2+4*q-2*q*q)})
    require(all(rows[i+1]['max_union_censoring_bound_h_minus2_0_2'] <
                rows[i]['max_union_censoring_bound_h_minus2_0_2'] for i in range(3)),
            'collar union-mass trend failed')
    require(abs(rows[-1]['central_means_h_minus2_0_2'][-1]-4)<0.35,
            'alternative mean does not approach J h')
    return {'model':'radial linearly vanishing density','boundary_information':2,
            'scale_diagnostic_not_monte_carlo':True,'rows':rows}


def support_control() -> dict:
    # Increasing F with F(1-z)=1-F(z) preserves the sum<1 sublevel set.
    # It does NOT preserve the density-ratio invariant.
    eps=0.08
    transform=lambda z: z+eps*math.sin(2*math.pi*z)
    require(1-2*math.pi*eps>0,'transform not monotone')
    tested=0
    for x in np.linspace(0.01,0.99,49):
        for y in np.linspace(0.01,0.99,49):
            if abs(x+y-1)<1e-10:
                continue
            require((x+y<1)==(transform(x)+transform(y)<1),'support gauge failed')
            tested+=1
    x=0.2
    defect=(x/(1-x))**2
    newdefect=(transform(x)/(1-transform(x)))**2
    require(abs(defect-newdefect)>0.03,'law invariant did not detect support gauge')
    return {'support_comparisons':tested,'same_support_different_density_invariant':True,
            'interpretation':'negative control for support-only inversion, not a counterexample to the law theorem'}


def main() -> None:
    result={'target_commit':TARGET,'scope':'independent finite diagnostics, not theorem or native-build certification',
            'density':density_checks(),'nonlinear_jets':nonlinear_jet_checks(),
            'collar':collar_checks(),'support_negative_control':support_control(),'status':'PASS'}
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))

if __name__=='__main__':
    main()
