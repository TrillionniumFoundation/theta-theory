#!/usr/bin/env python3
"""Independent finite rational diagnostics for the A2 v13 referee report.

Standard library only. No author module is imported. Explicit failures remain
active under python -O. These checks are not a proof certificate or simulation.
"""
from __future__ import annotations
import argparse
import json
from collections import Counter
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path

COUNTS: Counter[str] = Counter()


def check(category: str, condition: bool) -> None:
    if not condition:
        raise ArithmeticError(f"Independent diagnostic failed: {category}")
    COUNTS[category] += 1


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv(a):
    d = det(a)
    if not d:
        raise ArithmeticError("Singular diagnostic matrix")
    return [[a[1][1]/d, -a[0][1]/d], [-a[1][0]/d, a[0][0]/d]]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


def unweighted(nu, m):
    # Coefficient of d^(m-1), divided by the residual-weighted base integral.
    return F(2*factorial(2*m), 2**m*factorial(m)**2*(m+1))*nu**m


def weighted(nu, k):
    # Coefficient of d^k of the residual-weighted normalized moment.
    return F(2*comb(2*k, k), 2**k*(k+1)*(k+2))*nu**k


def contact_checks():
    blocks = rows = 0
    for g in (F(1, 2), F(1), F(2)):
        for k0 in (F(1, 3), F(1), F(2)):
            for k1 in (F(1, 3), F(1), F(2)):
                c = [1+g*k0, 1+g*k1]
                z = c[0]*c[1]-1
                scales = [g/(2*x*z) for x in c]
                for m in range(2, 11):
                    km = F(4, 2**m*(m+1)*factorial(m)**2)
                    U, V = (1+2*z)**m, 1+2*m*z
                    matrix = []
                    for b in (0, 1):
                        o = 1-b
                        h = [[(c[b]-1/(2*c[o]))/g, -1/(2*c[o]*g)],
                             [-1/(2*c[o]*g), (c[b]-1/(2*c[o]))/g]]
                        hi = inv(h)
                        nu = hi[0][0]
                        a = 1/(2*c[o])
                        nuw = a*a*sum(sum(row) for row in hi)
                        check('Schur determinant', det(h) == c[b]*z/(c[o]*g*g))
                        check('endpoint variance', nu == scales[b]*(1+2*z))
                        check('middle variance', nuw == scales[o])
                        own = -F(2, factorial(2*m))*unweighted(nu, m)
                        action_other = -F(2, factorial(2*m))*unweighted(nuw, m)
                        twist_other = -(g/c[o])/factorial(2*m-2)*weighted(nuw, m-1)
                        other = action_other+twist_other
                        check('own block entry', own == -km*scales[b]**m*U)
                        check('other block entry including twist', other == -km*scales[o]**m*V)
                        check('negative control: omitted twist', action_other != other)
                        row = [own, other] if b == 0 else [other, own]
                        matrix.append(row)
                        rows += 1
                    sep = sum(F(comb(m, r))*(2*z)**r for r in range(2, m+1))
                    check('strict binomial separation', U-V == sep and sep > 0)
                    check('positive full block determinant', det(matrix) > 0)
                    check('finite block inverse', mul(matrix, inv(matrix)) == [[1, 0], [0, 1]])
                    blocks += 1
    g, cb, z, m = F(1), F(2), F(3), 2
    L, km = g/(2*cb*z), F(1, 12)
    own, other = -km*L**2*49, -km*L**2*13
    check('printed quartic matrix', (own, other) == (F(-49,1728), F(-13,1728)))
    check('printed antisymmetric eigenvalue', abs(own-other) == F(1,48))
    return {'geometries': 27, 'orders': [2,10], 'blocks': blocks, 'oriented_rows': rows}


def limiting_separation_checks():
    def coth(lam, k):
        t = lam**(2*k)
        return (1+t)/(1-t)
    def csch(lam, k):
        t = lam**k
        return 2*t/(1-t*t)
    def tanh(lam, k):
        t = lam**(2*k)
        return (1-t)/(1+t)
    for lam in (F(1,10), F(1,4), F(1,2), F(3,4), F(9,10)):
        for m in range(2,11):
            E = lam**(4*(m-1))/(1-lam**(4*(m-1)))-lam**(4*m)/(1-lam**(4*m))
            O = (csch(lam,2*(m-1))-csch(lam,2*m))/2
            P, Q = coth(lam,2*m)+2*m*E, csch(lam,2*m)+2*m*O
            rhs = m*tanh(lam,m-1)-(m-1)*tanh(lam,m)
            check('limiting antisymmetric identity', P-Q == rhs)
            check('limiting separation positivity', P > Q > 0)


def normal_form_checks():
    # Independent routes: product of one-step derivatives; implicit mixed
    # boundary differentiation; and two symplectic endpoint coordinate charts.
    cin = [[F(2),F(1)],[F(1),F(1)]]
    cout = [[F(3),F(2)],[F(1),F(1)]]
    ident = [[F(1),F(0)],[F(0),F(1)]]
    cases = 0
    for lam in (F(1,4), F(1,2), F(3,4)):
        for alpha in (F(0), F(1,3), F(-1,5)):
            for beta in (F(0), F(1,7)):
                for n in range(1,13):
                    I = lam**n / 10**6
                    delta = lam+alpha*I+beta*I*I
                    prime = alpha+2*beta*I
                    power = delta**n
                    s = F(1,10)
                    p = I/s
                    t = p/power
                    q = s*power
                    derivative = ident
                    si, pi = s, p
                    for _ in range(n):
                        one = [[delta+I*prime, si*si*prime],
                               [-pi*pi*prime/(delta*delta), 1/delta-I*prime/(delta*delta)]]
                        derivative = mul(one, derivative)
                        si, pi = si*delta, pi/delta
                    den = 1-n*I*prime/delta
                    twist = power/den
                    check('normal form iterate', (si,pi) == (q,t))
                    check('normal form symplectic determinant', det(derivative) == 1)
                    check('normal form mixed-boundary derivative', 1/derivative[1][1] == twist)
                    check('normal form uniform-small denominator sample', den > F(1,2))
                    ap = n*delta**(n-1)*prime
                    Is, It = t*power/den, s*power/den
                    ps, pt = t*ap*Is, power+t*ap*It
                    qs, qt = power+s*ap*Is, s*ap*It
                    check('mixed generating integrability', pt == qs == twist)
                    D = det([[2+ps,pt],[3*qs,3*qt+2]])
                    physical = mul(mul(cout, derivative), inv(cin))
                    check('physical endpoint Jacobian formula', 1/physical[0][1] == twist/D)
                    cases += 1
    return {'normal_form_cases': cases, 'iterate_range': [1,12], 'charts': [cin,cout]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    contact = contact_checks()
    limiting_separation_checks()
    nf = normal_form_checks()
    result = {
        'reviewed_commit': '0e54099f079232df233316ae6fe7986fc51b7ea1',
        'status': 'passed',
        'total_explicit_checks': sum(COUNTS.values()),
        'checks_by_category': dict(sorted(COUNTS.items())),
        'contact_grid': contact,
        'normal_form_grid': nf,
        'arithmetic': 'exact fractions; standard library; no author imports',
        'scope_limits': [
            'Finite algebra only, not a proof certificate.',
            'No author verification suite was run.',
            'No nonlinear billiard simulation or empirical probability experiment.',
            'No TeX compilation, remote CI, or exhaustive appendix audit.',
            'Normal-form checks are on supplied canonical maps, not a theorem producing charts for smooth billiards.'
        ]
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, default=str)+'\n', encoding='utf-8')
    print(f"PASS: {result['total_explicit_checks']} explicit exact-rational checks")

if __name__ == '__main__':
    main()
