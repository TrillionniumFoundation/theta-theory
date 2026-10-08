#!/usr/bin/env python3
"""Finite regression checks of the new continuous proofs; not a proof oracle.

The Newton computation implements the half action directly and imports none
of the retained author solvers. mpmath is used only by this diagnostic.
The analytical all-parameter and infinite-period arguments are in Section 6.
"""
from __future__ import annotations
from fractions import Fraction as F
import json
import mpmath as mp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def compute(radius: str, m: int):
    R = mp.mpf(radius)
    D = mp.sqrt(3)
    g = D - 2*R
    d = mp.mpf('0.5')-R

    def arc(y):
        x = mp.sqrt(R*R-y*y)
        return R-x, y/x, R*R/x**3

    def action(y):
        grad = mp.matrix(m, 1)
        hess = mp.matrix(m, m)
        u, uy, uyy = arc(y[0])
        h = g/2+u
        v = d+y[0]
        e = mp.sqrt(h*h+v*v)
        e1 = (h*uy+v)/e
        value = e-g/2
        grad[0] += e1
        hess[0,0] += (uy*uy+1-e1*e1)/e+h*uyy/e
        for k in range(m-1):
            a, ay, ayy = arc(y[k])
            z, az, azz = arc(y[k+1])
            h = g+a+z
            v = y[k+1]-y[k]
            ell = mp.sqrt(h*h+v*v)
            ly = (h*ay-v)/ell
            lz = (h*az+v)/ell
            value += ell-g
            grad[k] += ly
            grad[k+1] += lz
            hess[k,k] += (ay*ay+1-ly*ly)/ell+h*ayy/ell
            hess[k+1,k+1] += (az*az+1-lz*lz)/ell+h*azz/ell
            cross = (ay*az-1-ly*lz)/ell
            hess[k,k+1] += cross
            hess[k+1,k] += cross
        a, a1, a2 = arc(y[-1])
        value += a
        grad[m-1] += a1
        hess[m-1,m-1] += a2
        return value, grad, hess

    y = [mp.mpf(0)]*m
    for step in range(25):
        value, grad, hess = action(y)
        residual = max(abs(v) for v in grad)
        if residual < mp.mpf('1e-65'):
            break
        change = mp.lu_solve(hess, -grad)
        ynew = [y[k]+change[k] for k in range(m)]
        require(all(-d < z < 0 for z in ynew), 'Newton left physical interior')
        y = ynew
    else:
        raise RuntimeError('Newton iteration did not converge')
    require(residual < mp.mpf('1e-65'), 'stationarity tolerance')
    require(all(-2*d/5 < z < 0 for z in y), 'physical height margin')
    return {'R': radius, 'm': m, 'E': 2*value, 'a': -y[-1],
            'gradient_residual': residual}


def main():
    mp.mp.dps = 90
    exact = {
        'terminal_response_slope': F(1,2)/(4+3) == F(1,14),
        'height_ratio': F(3,5)/14 == F(3,70),
        'increment_ratio_margin': F(158,47)*F(3,70)**4 > F(1,100000),
        'schur_subtraction_upper': 4-F(100,47) < 2,
        'schur_subtraction_lower': F(3,2)-3 > -2,
        'selected_phase_m1': F(1,10000)/400 == F(1,4000000),
        'selected_phase_later': F(1,200000) > F(1,4000000),
        'selected_section_angle_margin': F(1,22) < F(3,50),
        'selected_section_p_margin': F(1,22)+F(2,79) < F(3,20),
    }
    require(all(exact.values()), 'exact rational comparison')
    samples = []
    comparisons = []
    selections = []
    for R in ('0.45', '0.46', '0.47'):
        rows = [compute(R,m) for m in range(1,11)]
        samples += rows
        ds = [rows[k+1]['E']-rows[k]['E'] for k in range(len(rows)-1)]
        require(all(v>0 for v in ds), 'finite increment sign')
        for k in range(len(rows)-1):
            rat = rows[k+1]['a']/rows[k]['a']
            require(rat >= mp.mpf(3)/70, 'adjacent terminal comparison')
            if k < len(ds)-1:
                drat = ds[k+1]/ds[k]
                require(drat >= mp.mpf('0.00001'), 'adjacent increment ratio')
                comparisons.append({'R':R,'m':k+1,'height_ratio':mp.nstr(rat,32),
                                    'increment_ratio':mp.nstr(drat,32)})
        for b in (1,10**3,10**6,10**9,10**12,10**15):
            eligible = [k for k,v in enumerate(ds) if b*v <= mp.mpf('0.5')]
            require(bool(eligible),'diagnostic sample did not contain first crossing')
            k = eligible[0]
            phase = b*ds[k]
            require(phase >= mp.mpf(1)/4000000,'selected phase lower bound')
            budget = 1+mp.ceil(mp.log(b)/mp.log(mp.mpf(100)/49))
            require(k+1<=budget,'logarithmic length budget')
            selections.append({'R':R,'b':b,'j':k+1,'phase':mp.nstr(phase,32)})
    serial = [{k:(mp.nstr(v,72) if isinstance(v,mp.mpf) else v)
               for k,v in r.items()} for r in samples]
    print(json.dumps({'status':'passed','scope':'finite diagnostic only',
        'all_parameter_proof_source':'core/14_periodic_coercivity.tex',
        'full_raw_LLT_verified':False,'independent_human_review':False,
        'precision_decimal_digits':mp.mp.dps,'exact_rational_checks':exact,
        'samples':serial,'adjacent_comparisons':comparisons,
        'frequency_selections':selections},indent=2))


if __name__ == '__main__':
    main()
