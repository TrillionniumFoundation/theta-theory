#!/usr/bin/env python3
"""Independent finite diagnostics for the A1 v5 referee report.
No author test module is imported. Exact checks do not prove all-budget claims.
Run: python referee_checks.py [output.json]
Requires SymPy. No network, repository checkout, or mutable external data.
"""
from __future__ import annotations
import hashlib
import json
import platform
import sys
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import isqrt
from pathlib import Path
import sympy as S

CHECKS = []
DETAILS = {}
t = S.Symbol('t', real=True)


def check(name, condition):
    ok = bool(condition)
    CHECKS.append({'name': name, 'passed': ok})
    if not ok:
        raise AssertionError(name)


def integral(poly):
    return sum(c / S.Integer(k[0] + 1) for k, c in S.Poly(S.expand(poly), t).terms())


def columns(polys, degree):
    return S.Matrix([[S.Poly(S.expand(p), t).nth(k) for p in polys]
                     for k in range(degree + 1)])


def atan_bounds(x, n):
    a = sum(((-1)**j) * x**(2*j + 1) / (2*j + 1) for j in range(n))
    b = a + ((-1)**n) * x**(2*n + 1) / (2*n + 1)
    return min(a, b), max(a, b)


def run():
    T, e, area, pi = S.symbols('T e area pi', positive=True)
    C = S.Matrix([[0, 1, 0, 0], [0, -2*T/area, T/area, T/area],
                  [pi/area, -pi/area, 0, 0],
                  [0, 0, 2*T*e/(pi*area), -2*T*e/(pi*area)]])
    check('physical determinant squared', S.factor(C.det()**2 - (4*T*T*e/area**3)**2) == 0)
    check('physical normalization', C*S.ones(4, 1) == S.Matrix([1, 0, 0, 0]))
    check('erased calibration rank', C[:, :2].row_join(C[:, 2]+C[:, 3]).rank() == 3)
    check('zero amplitude calibration rank', C.subs(e, 0).rank() == 3)
    z = S.Matrix(S.symbols('z0:4'))
    check('lookup rejection right inverse', S.simplify(C*(S.ones(4, 1)/2+C.inv()*z)-S.Matrix([S.Rational(1, 2), 0, 0, 0])-z) == S.zeros(4, 1))

    # A separate positive categorical family, not a rational proxy for the billiard.
    for q in range(1, 5):
        x = S.Rational(1, 4) + t/2
        probs = [S.binomial(q, j)*x**j*(1-x)**(q-j) for j in range(q+1)]
        check(f'binomial normalized q={q}', S.expand(sum(probs)-1) == 0)
        check(f'binomial full polynomial span q={q}', columns(probs, q).rank() == q+1)
        for m in (1, 2):
            B = [S.Rational(1, 2)+p/8 for p in probs]
            words = [S.prod(B[j] for j in js) for js in combinations_with_replacement(range(q+1), m)]
            check(f'executed probe product span q={q} m={m}', columns(words, q*m).rank() == q*m+1)

    for q, n, m in [(1, 2, 4), (1, 4, 2), (2, 2, 3), (2, 3, 2), (3, 2, 2), (3, 3, 1), (3, 1, 3), (4, 2, 1)]:
        a, b = q*n, q*m
        G = S.Matrix([[S.Rational(1, i+j+1)-S.Rational(1, (i+1)*(j+1))
                       for i in range(1, a+1)] for j in range(1, b+1)])
        check(f'centered Gram rank q={q} n={n} m={m}', G.rank() == q*min(n, m))
    for q, n in [(1, 4), (2, 3), (3, 3), (4, 2)]:
        Fs = [1+S.Rational(i+1, 37)*t**q for i in range(n)]
        variations = [t**j*S.prod(Fs[k] for k in range(n) if k != i)
                      for i in range(n) for j in range(q+1)]
        check(f'coprime product rank q={q} n={n}', columns(variations, q*n).rank() == q*n+1)

    P = 1+2*t+t**4
    f = S.Rational(2, 5)+t/13+t**3/29
    for j in range(7):
        fc = S.Poly(f, t)
        left = integral(t**j*P*f)/integral(P*f)
        right = sum(fc.nth(i)*integral(t**(i+j)*P) for i in range(4))/sum(fc.nth(i)*integral(t**i*P) for i in range(4))
        check(f'causal shrinking moment identity j={j}', S.cancel(left-right) == 0)
    a, p = S.symbols('a p', real=True)
    check('Brier excess identity', S.expand(p*(a-1)**2+(1-p)*a*a-p*(1-p)-(a-p)**2) == 0)
    for d in (1, 2, 3, 5, 6, 9):
        check(f'volume tail constant d={d}', S.integrate(1-t**S.Rational(d, 2), (t, 0, 1)) == S.Rational(d, d+2))

    # An exactly realizable sparse-factor example: W = span(1,t^2,t^5).
    params = [S.Rational(i, 1000) for i in range(1, 7)]
    Fs = [1+params[2*i]*t**2+params[2*i+1]*t**5 for i in range(3)]
    k = [S.Rational(1, 3)+t**2/12, S.Rational(1, 3)+t**5/12,
         S.Rational(1, 3)-(t**2+t**5)/12]
    commands = []
    for i, (aa, bb) in enumerate(zip(params[::2], params[1::2])):
        u = [S.Rational(1, 2)+4*aa-2*bb, S.Rational(1, 2)-2*aa+4*bb,
             S.Rational(1, 2)-2*(aa+bb)]
        commands.append([str(v) for v in u])
        check(f'sparse gate interior and factor i={i}', all(S.Rational(1, 4)<v<S.Rational(3, 4) for v in u)
              and S.expand(sum(u[j]*k[j] for j in range(3))-Fs[i]/2) == 0)
    exponents = sorted({i+j for i in (0, 2, 5) for j in (0, 2, 5)})
    check('sparse future test exponents', exponents == [0, 2, 4, 5, 7, 10])
    P = S.prod(Fs)
    Z = integral(P)
    variations = [t**j*S.prod(Fs[k0] for k0 in range(3) if k0 != i)
                  for i in range(3) for j in (2, 5)]
    J = S.Matrix([[(integral(t**j*v)*Z-integral(t**j*P)*integral(v))/Z**2
                   for v in variations] for j in exponents[1:]])
    minor = S.factor(J[:, :5].det())
    check('sparse operational derivative nonzero 5x5 minor', minor != 0)
    check('sparse operational derivative rank five', J.rank() == 5)
    DETAILS['sparse_example'] = {'factor_parameters': [str(x) for x in params],
        'rejection_commands': commands, 'prior': 'uniform on [0,1]',
        'future_test_exponents': exponents, 'minor_first_five_columns': str(minor),
        'derivative_rank': 5, 'naive_rank_only_prediction': 4}

    # Independent outward rational enclosure for the physical uniform-prior gain.
    lo1, hi1 = atan_bounds(F(1, 5), 48)
    lo2, hi2 = atan_bounds(F(1, 239), 12)
    pl, pu = 16*lo1-4*hi2, 16*hi1-4*lo2
    den = 10**60
    root = isqrt(3*den*den)
    check('independent sqrt three rational enclosure', root*root < 3*den*den < (root+1)*(root+1))
    al, au = F(root, 2*den), F(root+1, 2*den)
    l, r = F(9, 20), F(47, 100)
    mu = lambda j: (r**(j+1)-l**(j+1))/((j+1)*(r-l))
    v = mu(5)/mu(1)-(mu(3)/mu(1))**2
    check('uniform physical hit variance', v == F(529, 18750000))
    cl = F(1, 2)+F(1, 20)*mu(3)/(pu*mu(1))
    cu = F(1, 2)+F(1, 20)*mu(3)/(pl*mu(1))
    gl = (mu(1)/(10*au))*(v/(20*au))**2/(cl*(1-cl))
    gu = (mu(1)/(10*al))*(v/(20*al))**2/(cu*(1-cu))
    check('physical gain ordered positive bounds', 0 < gl < gu)
    printed_lo = F(5637602588099328, 10**28)
    printed_hi = F(5637602588099330, 10**28)
    check('physical gain printed strict enclosure', printed_lo < gl < gu < printed_hi)
    DETAILS['physical_gain'] = {'prior': 'uniform on [9/20,47/100]', 'T': '1/20',
        'epsilon': '1/20', 'hit_variance': str(v),
        'strict_lower': str(printed_lo), 'strict_upper': str(printed_hi),
        'decimal_interval': ['5.637602588099328e-13', '5.637602588099330e-13']}
    u = F(5, 8)
    check('zero-memory tolerance example', u**(2*20) < F(1, 10**8))
    DETAILS['zero_memory'] = {'shared_menu_c': '1/2', 'delta': '1/8', 'future_m': 20,
        'regret_upper_fraction': str(u**40), 'below_absolute_tolerance': '1/100000000',
        'scope': 'analytic all-history zero-forecast bound; no horizon-uniform lower constant'}
    return {'suite': 'Independent referee A1 v5 finite checks', 'submission': '20a26285a26cb468206b771c38166fd216283af0',
        'python': platform.python_version(), 'sympy': S.__version__,
        'passed': sum(x['passed'] for x in CHECKS), 'total': len(CHECKS),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'arithmetic': 'exact symbolic and rational; printed physical bounds are rational inequalities',
        'scope': {'imports_author_tests': False, 'author_suite_rerun': False, 'prior_referee_suite_rerun': False,
                  'latex_compiled': False, 'pdf_visually_checked': False, 'formal_proof_verification': False,
                  'all_budget_claims_proved_by_finite_checks': False},
        'checks': CHECKS, 'details': DETAILS}


if __name__ == '__main__':
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('DIAGNOSTICS.json')
    result = run()
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(f"{result['passed']}/{result['total']} exact diagnostics passed; {output}")
