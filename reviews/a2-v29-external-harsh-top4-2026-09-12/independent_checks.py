#!/usr/bin/env python3
"""Independent finite exact checks for A2 v29; not a continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import platform

HEAD = 'b137f2a92943d5491e0239eee193599eaa3728b8'
COUNTS: dict[str, int] = {}

def check(family: str, condition: bool) -> None:
    if not condition:
        raise RuntimeError('Independent check failed: ' + family)
    COUNTS[family] = COUNTS.get(family, 0) + 1

def ratio(f, x: Q, y: Q) -> Q:
    return f(x, y) * f(Q(0), Q(0)) / (f(x, Q(0)) * f(Q(0), y))

def multiply(A, B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))

def main() -> None:
    grid = tuple(Q(i, 12) for i in range(-4, 5))
    anchors = (Q(-1, 4), Q(-1, 6), Q(1, 6), Q(1, 4))
    # Nonsymmetric, nonfactorized functions are also in the new formula domain.
    for z in (Q(-1, 200), Q(1, 200), Q(1, 400)):
        def f(x, y):
            x, y = Q(x), Q(y)
            return (1-x*x-y*y)*(1+z*x*y*(x+2*y))*(1+x/20)*(1-y/30)
        def reflected(x, y):
            return f(-x, -y)
        def rescaled(x, y):
            return Q(7, 3)*f(x, y)
        for a in anchors:
            d = 1-ratio(f, a, a)
            check('off_model_positive_radical', d > 0)
            check('off_model_transported_radical', d == 1-ratio(reflected, -a, -a))
            for u in grid:
                n = 1-ratio(f, -u, a)
                nr = 1-ratio(reflected, u, -a)
                check('off_model_transported_numerator', n == nr)
                check('off_model_positive_one_plus_T', n >= 0 or n*n < d)
                check('off_model_transported_axis_amplitude', reflected(u, 0)/reflected(0, 0) == f(-u, 0)/f(0, 0))
                for v in grid:
                    check('off_model_positive_density', f(u, v) > 0)
                    check('off_model_reflection_ratio', ratio(reflected, u, v) == ratio(f, -u, -v))
                    check('mass_scale_invariance', ratio(f, u, v) == ratio(rescaled, u, v))
    # Exact asymmetric action and amplitude with non-unit offset and amplitude.
    for d in (Q(1), Q(3, 2)):
        def S(x):
            x = Q(x)
            return x*x+Q(1, 7)*x**3+Q(1, 11)*x**4
        def B(x):
            x = Q(x)
            return Q(2)+x/9+x*x/13
        def exact(x, y):
            return B(x)*B(y)*(d-S(x)-S(y))/7
        for a in anchors:
            q = S(a)/(d-S(a))
            check('exact_anchor_positive', q > 0)
            check('exact_scalar_root_identity', q*q == 1-ratio(exact, a, a))
            for u in grid:
                t = (1-ratio(exact, u, a))/q
                check('exact_action_any_anchor', d*t/(1+t) == S(u))
                check('exact_normalized_amplitude', exact(u, 0)/exact(0, 0)*(1+t) == B(u)/B(0))
    # General last-jet blocks, using x=exp(-gamma) for rational hyperbolics.
    identity = ((Q(1), Q(0)), (Q(0), Q(1)))
    for x in (Q(1, 4), Q(1, 3), Q(1, 2)):
        c, s = (1/x+x)/2, (1/x-x)/2
        for r in (Q(1), Q(9, 10), Q(11, 10)):
            c0, c1 = c*r, c/r
            check('positive_curvature_geometry', c0 > 1 and c1 > 1)
            g = Q(7, 5)
            a0, a1 = r*s/g, s/(r*g)
            check('quadratic_product_recovery', g*g*a0*a1 == s*s)
            check('quadratic_ratio_recovery', a0/a1 == (c0/c1))
            for n in range(3, 15):
                y = x**n
                h, k = (1+y*y)/(1-y*y), 2*y/(1-y*y)
                M = ((h, r**n*k), (r**(-n)*k, h))
                inverse = ((h, -r**n*k), (-r**(-n)*k, h))
                check('last_jet_determinant_one', h*h-M[0][1]*M[1][0] == 1)
                check('last_jet_inverse', multiply(M, inverse) == identity)
                check('own_site_multiplicity', 1+2*y*y/(1-y*y) == h)
                check('opposite_site_multiplicity', 2*r**n*y/(1-y*y) == M[0][1])
    # Anchor projection and common reversal, not independent channel reversals.
    for degree in range(2, 11):
        coefficients = tuple(Q(n+2, 2*n+3) for n in range(degree+1))
        for u in grid:
            lhs = sum(((-1)**n)*coefficients[n]*u**n for n in range(2, degree+1))
            rhs = sum(coefficients[n]*(-u)**n for n in range(2, degree+1))
            check('projected_jet_parity', lhs == rhs)
    # All finite binary stopped histories up to length eight, including no successes.
    for length in range(9):
        for sequence in product((False, True), repeat=length):
            runs, failures = [], 0
            for success in sequence:
                if success:
                    runs.append(failures)
                    failures = 0
                else:
                    failures += 1
            restored = []
            for run in runs:
                restored.extend([False]*run+[True])
            restored.extend([False]*failures)
            check('complete_censored_count_encoding', tuple(restored) == sequence)
            check('stopping_length_retained', sum(runs)+len(runs)+failures == length)
    # A retained adaptive design can preserve the deleted residual time.
    r0, r1 = Q(1, 7), Q(2, 7)
    ce0 = ((('initial', Q(1)), (Q(0), Q(0))), (('next', r0), None))
    ce1 = ((('initial', Q(1)), (Q(0), Q(0))), (('next', r1), None))
    check('adaptive_design_information_warning', ce0 != ce1)
    # Reference-layer arithmetic in a normalized uniform moving-ceiling toy model.
    # This checks normalization and rates, not the billiard deficiency theorem.
    R = Q(4)
    for k in (40, 80, 160):
        for z in (Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1)):
            p = (R-z)/(k-z)
            check('toy_layer_intensity_error', k*p-(R-z) == z*(R-z)/(k-z))
            check('toy_bulk_parameter_independent', (1/(1-z/k))/(1-p) == 1/(1-R/k))
            check('toy_trace_uniform_rate', abs(Q(k)/(k-z)-1) <= 2*abs(z)/k)
    # Old failure, new repair: this remains off-model, not table nonidentifiability.
    D, h = Q(1, 225), Q(7, 22500)
    left, right = D+h, D*D/(D-h)
    check('fixed_anchor_witness', left-right == Q(-49, 2092500))
    body = Path(__file__).read_bytes()
    print(json.dumps({
        'reviewed_commit': HEAD, 'status': 'passed', 'arithmetic': 'exact rational',
        'python_version': platform.python_version(),
        'script_sha256': hashlib.sha256(body).hexdigest(),
        'checks_by_family': COUNTS, 'total_checks': sum(COUNTS.values()),
        'witness': {'left_square': str(left), 'right_square': str(right), 'difference': str(left-right)},
        'scope': 'Finite algebra and encoding only; not a certificate of infinite-dimensional convergence, complete native build, or all statistical theorems.'
    }, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
