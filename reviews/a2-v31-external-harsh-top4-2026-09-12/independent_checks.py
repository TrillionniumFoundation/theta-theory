#!/usr/bin/env python3
"""Independent finite diagnostics for the source-pinned A2 v31 review.

These are exact algebraic/model checks, NOT proofs of billiard theorems or
an execution of the author's native build. Standard library only.
Run both: python3 independent_checks.py; python3 -O independent_checks.py.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import isqrt
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def fsqrt(x: F) -> F:
    require(x >= 0, 'negative square root')
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    require(a*a == x.numerator and b*b == x.denominator, 'nonrational root')
    return F(a, b)


def coupling_checks() -> dict:
    cases = [([F(1,2),F(1,3),F(1,6)], [F(1,4),F(1,2),F(1,4)]),
             ([F(1),F(0)], [F(0),F(1)]),
             ([F(1,3),F(2,3)], [F(1,3),F(2,3)])]
    overlaps = []
    for p, q in cases:
        h = [min(x,y) for x,y in zip(p,q)]
        m = sum(h, F(0))
        c = [[(h[i] if i == j else F(0)) +
              ((p[i]-h[i])*(q[j]-h[j])/(1-m) if m < 1 else F(0))
              for j in range(len(p))] for i in range(len(p))]
        require([sum(row) for row in c] == p, 'first marginal')
        require([sum(c[i][j] for i in range(len(p))) for j in range(len(p))] == q,
                'second marginal')
        disagreement = sum(c[i][j] for i in range(len(p)) for j in range(len(p)) if i != j)
        require(disagreement == 1-m == sum(abs(x-y) for x,y in zip(p,q))/2,
                'maximality')
        overlaps.append(str(m))
    # A constant coarsening identifies two disjoint point masses.
    require(sum(cases[1][0]) == sum(cases[1][1]) == 1, 'coarsened marginal')
    return {'cases': len(cases), 'overlap_masses': overlaps,
            'noninjective_map_TV_before': '1', 'noninjective_map_TV_after': '0'}


def density_checks() -> dict:
    S = lambda u: u*u + u*u*u/4
    B = lambda u: 1+u/3
    f = lambda u,v: B(u)*B(v)*(1-S(u)-S(v))/7
    R = lambda u,v: f(u,v)*f(F(0),F(0))/(f(u,F(0))*f(F(0),v))
    grid = [F(-1,4),F(-1,8),F(0),F(1,8),F(1,4)]
    count = 0
    for a in (F(-1,4),F(1,4)):
        q = fsqrt(1-R(a,a))
        require(q > 0, 'anchor positivity')
        for u in grid:
            t = (1-R(u,a))/q
            require(t/(1+t) == S(u), 'action inversion')
            require(f(u,F(0))/f(F(0),F(0))*(1+t) == B(u)/B(F(0)),
                    'amplitude inversion')
            for v in grid:
                require(1-R(u,v) == S(u)/(1-S(u))*S(v)/(1-S(v)),
                        'rank-one density defect')
                count += 1
    return {'rank_one_checks': count, 'anchors': ['-1/4','1/4'],
            'nonsymmetric_action_and_amplitude': True}


def laurent_integral(coeff: dict[int,F], q: F) -> tuple[F,F]:
    """Integral from q to 1, as rational part plus coefficient*log(1/q)."""
    regular, logarithm = F(0), F(0)
    for power, value in coeff.items():
        if power == -1:
            logarithm += value
        else:
            regular += value*(1-q**(power+1))/(power+1)
    return regular, logarithm


def collar_checks() -> dict:
    # f_0=2s, S=1/s-2, s=1-x; only x=1 is the moving boundary.
    score = {-1:F(1), 0:F(-2)}
    mean = {p+1: 2*c for p,c in score.items()}
    second: dict[int,F] = {}
    for p,c in score.items():
        for r,d in score.items():
            second[p+r+1] = second.get(p+r+1,F(0)) + 2*c*d
    for q in (F(1,2),F(1,8),F(1,64),F(1,1024)):
        require(laurent_integral(mean,q) == (-2*q+2*q*q,F(0)), 'score mean')
        require(laurent_integral(second,q) == (-4+8*q-4*q*q,F(2)),
                'logarithmic score coefficient')
        require(1-laurent_integral({1:F(2)},q)[0] == q*q, 'collar mass')
    for theta in (F(1,2),F(1,8),F(1,64)):
        # Integral of 2(1+theta-x)/(1+theta)^2 on (1,1+theta).
        exclusive = 2*(theta*theta-theta*theta/2)/(1+theta)**2
        require(exclusive == theta**2/(1+theta)**2, 'support-exclusive mass')
    return {'q_values_checked': 4, 'boundary_information': '2',
            'truncated_mean': '-2*q+2*q^2',
            'truncated_second_moment': '2*log(1/q)-4+8*q-4*q^2',
            'collar_mass': 'q^2', 'support_exclusive_mass': 'theta^2/(1+theta)^2'}


def ceiling_checks() -> list[dict]:
    # q_{k,z}=2/(1-z/k)^2 on the triangle u>0,r>0,u+r<1-z/k.
    # Layer coordinate y=k(1-u-r), target 2*1_{0<u<1,z<y<R}.
    # The exact L1 intensity error integrates both the moving ceiling and
    # its intersection with the fixed r=0 face. This model's normalized
    # common-bulk laws coincide exactly; it is not a general bulk bound.
    rows = []
    R = F(2)
    for k in (32,64,128,256):
        for z in (F(-1),F(0),F(1)):
            rho = 2/(1-z/k)**2
            e = abs(rho-2)
            lo = max(z,F(0))
            error = e*(R-lo) + (2-e)*(R*R-lo*lo)/(2*k)
            if z < 0:
                error += e*(-z) + rho*z*z/(2*k)
            layer_mass = rho/k*((R-z)-(R*R-z*z)/(2*k))
            require(0 < layer_mass < 1, 'layer probability')
            # For z=-1, k*error<17; for z=0 it is 4; for z=1 it is <8.
            require(error >= 0 and k*error <= 20, 'intensity O(1/k) bound')
            require(k*k*layer_mass*layer_mass <= 40, 'binomial Poisson O(1/k) bound')
            rows.append({'k': k, 'z': int(z), 'intensity_L1': str(error),
                         'k_times_intensity_L1': str(k*error),
                         'layer_probability': str(layer_mass)})
    return rows


def main() -> None:
    result = {'status':'passed', 'scope':'Exact finite algebra and toy statistical models only; no native build or full billiard proof certification.',
              'reviewed_commit':'e1f6304f6069869ac323e7d1a634a619faa4bc32',
              'coupling':coupling_checks(), 'density_inverse':density_checks(),
              'linear_boundary':collar_checks(), 'moving_ceiling':ceiling_checks()}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
