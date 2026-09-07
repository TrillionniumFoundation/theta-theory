#!/usr/bin/env python3
"""Independent exact-arithmetic diagnostics for A1 English v21.

No author implementation is imported. These are finite diagnostic examples,
not verification of analytic uniformity, measure minorization, or optimality.
Run: python independent_diagnostics.py --output DIAGNOSTICS.json
Python 3.10+ and SymPy are required. Checks remain active under python -O.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from typing import Iterable

import sympy as sp

PIN = "7c44bdccc91667c583b5d5cbcff3f8d9160a57d6"
COUNTS: Counter[str] = Counter()
CASES: Counter[str] = Counter()


def require(condition: bool, category: str, description: str) -> None:
    COUNTS[category] += 1
    if not condition:
        raise ArithmeticError(f"{category}: {description}")


def prod(values: Iterable[F]) -> F:
    out = F(1)
    for value in values:
        out *= value
    return out


def matrix(rows: list[list[F]]) -> sp.Matrix:
    return sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in row]
                      for row in rows])


def compositions(total: int, size: int):
    if size == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, size - 1):
            yield (first,) + tail


def formal_exponents(a: tuple[F, ...], m: int) -> list[F]:
    return [sum((F(k) * x for k, x in zip(alpha, a)), F(0))
            for alpha in compositions(m, len(a)) if alpha[0] != m]


def leja(exponents: list[F], H: F) -> tuple[list[F], list[F]]:
    remaining = list(enumerate(x / H for x in exponents))
    first = min(remaining, key=lambda item: (item[1], item[0]))
    remaining.remove(first)
    selected, pivots = [first[1]], [F(1)]
    while remaining:
        candidate = max(remaining, key=lambda item: (
            prod(abs(item[1] - y) for y in selected), -item[0]))
        pivots.append(prod(abs(candidate[1] - y) for y in selected))
        selected.append(candidate[1])
        remaining.remove(candidate)
    return selected, pivots


def polynomial_multiply(p: dict[F, F], q: dict[F, F]) -> dict[F, F]:
    out: dict[F, F] = {}
    for a, ca in p.items():
        for b, cb in q.items():
            out[a+b] = out.get(a+b, F(0)) + ca*cb
    return {a: c for a, c in out.items() if c}


def polynomial_product(factors: list[dict[F, F]]) -> dict[F, F]:
    out = {F(0): F(1)}
    for factor in factors:
        out = polynomial_multiply(out, factor)
    return out


def moment(exponent: F, alpha: F) -> F:
    # alpha * uniform[0,1] + (1-alpha) * atom at zero, always full support.
    return alpha/(exponent+1) + (1-alpha if exponent == 0 else F(0))


def integral(p: dict[F, F], alpha: F) -> F:
    return sum((c*moment(b, alpha) for b, c in p.items()), F(0))


def raw_integral(p: dict[F, F], e: F, alpha: F) -> F:
    return sum((c*moment(b+e, alpha) for b, c in p.items()), F(0))


def newton_integral(p: dict[F, F], prefix: list[F], H: F, alpha: F) -> F:
    # Integrate the divided difference of t^(H*x) directly via the identity
    # [x_1,...,x_j] 1/(b+1+H*x) = (-H)^(j-1)/prod_i(b+1+H*x_i).
    # Every node is positive, so the atom at zero contributes zero.
    return sum((c*alpha*(-H)**(len(prefix)-1) /
                prod(b+1+H*x for x in prefix) for b, c in p.items()), F(0))


def geometry_and_history() -> None:
    R = lambda *a: tuple(F(x) for x in a)
    configurations = [
        (R(0,1), 1,1), (R(0,1), 2,2),
        (R(0,1,2), 1,2), (R(0,1,2), 2,2), (R(0,1,2), 2,3),
        (R(0,1,F(129,64)), 1,2), (R(0,1,F(129,64)), 2,2),
        (R(0,1,F(129,64)), 2,3), (R(0,1,F(127,64)), 2,2),
        (R(0,1,F(3,2)), 2,2), (R(0,1,2,3), 3,2),
        (R(0,1,F(129,64),F(194,64)), 3,2),
        (R(0,1,F(129,64),F(12353,4096)), 3,2),
        (R(0,1,F(129,64),F(193,64)), 3,2),
    ]
    ambient_negative_controls = 0
    for a, n, m in configurations:
        exps = formal_exponents(a, m)
        H = max(F(1), (n+m)*a[-1])
        nodes, d = leja(exps, H)
        q, s = len(nodes), len(set(nodes))
        p = min(n*(len(a)-1), q)
        CASES['leja_and_ambient_geometry'] += 1
        require(all(d[j] >= d[j+1] >= 0 for j in range(q-1)),
                'leja_and_ambient_geometry', 'ordered nonnegative pivots')
        L = matrix([[prod(nodes[i]-nodes[k] for k in range(j))/d[j]
                     if d[j] else F(0) for j in range(q)] for i in range(q)])
        diag = sp.diag(*[sp.Rational(x.numerator, x.denominator) for x in d])
        require(all(abs(x) <= 1 for x in L), 'leja_and_ambient_geometry',
                'bounded evaluation entries')
        A, B = L[:s,:s], L[s:,:s]
        T = sp.eye(q)
        T[:s,:s] = A.inv()
        if s < q:
            T[s:,:s] = -B*A.inv()
        require(T*L*diag == diag, 'leja_and_ambient_geometry',
                'ambient coordinate identity including inactive coordinates')
        expected_inverse = sp.eye(q)
        expected_inverse[:s,:s] = A
        if s < q:
            expected_inverse[s:,:s] = B
        require(T*expected_inverse == sp.eye(q), 'leja_and_ambient_geometry',
                'explicit ambient inverse')
        for ell in range(1,q+1):
            volume = max(prod(abs(nodes[i]-nodes[j]) for i,j in
                              itertools.combinations(subset,2))
                         for subset in itertools.combinations(range(q),ell))
            pivot_volume = prod(d[:ell])
            require(pivot_volume <= volume <= sp.factorial(ell)*pivot_volume,
                    'leja_and_ambient_geometry', 'maximal Vandermonde comparison')
        if s < q:
            bad_T = sp.eye(q)
            bad_T[:s,:s] = A.inv()
            require(bad_T*L*diag != diag, 'negative_controls',
                    'omitting the inactive-block subtraction must be detected')
            ambient_negative_controls += 1

        factors = [{F(0):F(1,2),a[-1]:F(1,2*(8+i))} for i in range(n)]
        P = polynomial_product(factors)
        directions = [polynomial_multiply({x:F(1)}, polynomial_product(
            factors[:i]+factors[i+1:])) for i in range(n) for x in a]
        for alpha in (F(1),F(2,5)):
            CASES['normalized_history_and_updates'] += 1
            Z = integral(P,alpha)
            require(Z > 0, 'normalized_history_and_updates', 'positive evidence')
            iz = [newton_integral(P,nodes[:j+1],H,alpha) for j in range(q)]
            iv = [raw_integral(P,H*x,alpha) for x in nodes]
            require(L*diag*matrix([[x/Z] for x in iz]) == matrix([[x/Z] for x in iv]),
                    'normalized_history_and_updates', 'raw/Newton posterior identity')
            Jnew = matrix([[(newton_integral(Q,nodes[:j+1],H,alpha)*Z
                             -iz[j]*integral(Q,alpha))/Z**2
                            for Q in directions] for j in range(p)])
            require(Jnew.rank() == p, 'normalized_history_and_updates',
                    'complete normalized Newton prefix rank')
            Jraw = matrix([[(raw_integral(Q,H*x,alpha)*Z-v*integral(Q,alpha))/Z**2
                            for Q in directions] for x,v in zip(nodes,iv)])
            require(Jraw.rank() == min(n*(len(a)-1),s),
                    'normalized_history_and_updates', 'raw acquired rank')
            tangent_pairing = matrix([[integral(Q,alpha) for Q in directions]] +
                [[newton_integral(Q,nodes[:j+1],H,alpha) for Q in directions]
                 for j in range(p)])
            require(tangent_pairing.rank() == p+1,
                    'normalized_history_and_updates', 'evidence-augmented pairing rank')
            report_factor = {x:F(i+1,8*len(a)**2) for i,x in enumerate(a)}
            report_factor[F(0)] += F(1,2)
            nextP = polynomial_multiply(P,report_factor)
            denominator = sum((c*raw_integral(P,x,alpha)/Z
                               for x,c in report_factor.items()), F(0))
            for e in sorted(set([F(0)]+formal_exponents(a,m-1))) if m>1 else [F(0)]:
                recursive = sum((c*raw_integral(P,e+x,alpha)/Z
                                 for x,c in report_factor.items()), F(0))/denominator
                direct = raw_integral(nextP,e,alpha)/integral(nextP,alpha)
                require(recursive == direct, 'normalized_history_and_updates',
                        'remaining raw-moment update equals direct posterior')
    require(ambient_negative_controls > 0, 'negative_controls',
            'collision mutation checks were actually exercised')


def rational_identity_checks() -> None:
    z, b, H = sp.symbols('z b H', positive=True)
    for nodes in ([F(1,4),F(1,2)], [F(1,8),F(3,8),F(7,8)]):
        exact = sum(1/(b+1+H*sp.Rational(x.numerator,x.denominator)) /
                    sp.Rational(prod(x-y for y in nodes if y != x)) for x in nodes)
        formula = (-H)**(len(nodes)-1)/sp.prod(b+1+H*sp.Rational(x) for x in nodes)
        require(sp.cancel(exact-formula) == 0, 'integrated_newton_identity',
                'distinct-node integral divided difference')
        CASES['integrated_newton_identity'] += 1
    for j in range(1,5):
        require(sp.simplify(sp.diff(1/(b+1+H*z),z,j-1)/sp.factorial(j-1)
                           -(-H)**(j-1)/(b+1+H*z)**j) == 0,
                'integrated_newton_identity', 'all-coincident Hermite identity')
        CASES['integrated_newton_identity'] += 1


def moving_kernel() -> None:
    for weights in itertools.product((1,2,3), repeat=4):
        p = [F(w,sum(weights)) for w in weights]
        p1,p2,p3,p4 = p
        H = matrix([[F(1),p3,p4],[p1,F(0),F(0)],[p2,F(0),F(0)]])
        kernel = matrix([[F(0)],[p4],[-p3]])
        require(H.rank() == 2 and H*kernel == sp.zeros(3,1),
                'moving_kernel', 'square pairing rank and exact kernel')
        f = [[F(1,4),F(0),F(0),F(0)], [F(0),F(1,4),F(0),F(0)]]
        g = [[F(1,2),F(1,2),F(3,4),F(1,2)],
             [F(1,2),F(1,2),F(1,2),F(3,4)]]
        cov = [[sum((p[k]*g[i][k]*f[j][k] for k in range(4)), F(0))
                -sum((p[k]*g[i][k] for k in range(4)), F(0))
                 *sum((p[k]*f[j][k] for k in range(4)), F(0))
                for j in range(2)] for i in range(2)]
        require(cov == [[-x*y/F(16) for y in (p1,p2)] for x in (p3,p4)],
                'moving_kernel', 'physical covariance before sqrt query weighting')
        scale2 = sum((v*v/F(2) for row in cov for v in row), F(0))
        require(scale2 == (p1*p1+p2*p2)*(p3*p3+p4*p4)/512,
                'moving_kernel', 'unique squared singular scale')
        CASES['moving_kernel'] += 1


def finite_matroids() -> None:
    examples = [
        (sp.Matrix([[1,1,1,1],[1,0,0,0],[0,1,0,0]]),
         sp.Matrix([[1,1,1,1],[0,0,1,0],[0,0,0,1]])),
        (sp.Matrix([[1,0,1,2],[0,1,1,1]]),
         sp.Matrix([[1,2,0,1],[0,1,1,2],[1,0,1,1]])),
        (sp.zeros(2,3),sp.Matrix([[1,2,3]])),
        (sp.Matrix([[1,0,1],[0,1,1]]),sp.Matrix([[1,1,2]])),
    ]
    for A,B in examples:
        s = A.cols
        common = 0
        for ell in range(1,min(A.rows,B.rows,s)+1):
            if any(A[:,list(S)].rank() == ell and B[:,list(S)].rank() == ell
                   for S in itertools.combinations(range(s),ell)):
                common = ell
        attained = max((A*sp.diag(*weights)*B.T).rank()
                       for weights in itertools.product((1,2),repeat=s))
        require(common == attained, 'finite_common_independence',
                'brute common independence equals attained positive-weight rank')
        CASES['finite_common_independence'] += 1


def propagation_and_collision_phases() -> None:
    for L in ((F(2),F(3),F(4)),(F(0),F(2),F(1,2)),(F(1,2),)*3):
        errors = [F(1,7),F(1,11),F(1,13),F(1,17)]
        e = errors[0]
        for n in range(1,4):
            e = L[n-1]*e+errors[n]
            formula = sum((errors[j]*prod(L[j:n]) for j in range(n+1)), F(0))
            require(e == formula, 'causal_recurrence', 'full propagated sum')
        CASES['causal_recurrence'] += 1
    require(F(2)*F(1,7)+F(1,11) != F(1,11), 'negative_controls',
            'discarding propagated earlier error must be detected')
    for k in (2,3,5,9):
        b1,b2 = F(6),F(8*k-2)
        # Risk exponents in theta when M = theta^(-budget exponent).
        first,second = b1/3,F(1,2)+b1/4
        second_late,third_late = F(1,2)+b2/4,F(4+2*k,9)+F(2,9)*b2
        require(first == second == 2, 'collision_phases', 'first crossover')
        require(second_late == third_late == 2*k and b2>b1,
                'collision_phases', 'second crossover and genuine intervening regime')
        CASES['collision_phases'] += 1


def run() -> dict:
    rational_identity_checks()
    geometry_and_history()
    moving_kernel()
    finite_matroids()
    propagation_and_collision_phases()
    return {
        'reviewed_commit': PIN,
        'status': 'PASS',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python': platform.python_version(), 'sympy': sp.__version__,
        'cases_by_category': dict(sorted(CASES.items())),
        'checks_by_category': dict(sorted(COUNTS.items())),
        'total_cases': sum(CASES.values()), 'total_checks': sum(COUNTS.values()),
        'limitations': [
            'Finite exact examples, not proof verification.',
            'Does not establish parameter-uniform analytic constants, inverse-chart mass, or entropy bounds.',
            'Does not test an actual optimal finite-state code or certify numerical resource complexity.',
            'Does not rerun the author validator or compile or inspect the manuscript PDF.',
            'No author theorem implementation is imported.',
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(encoded, encoding='utf-8')
    print(encoded, end='')


if __name__ == '__main__':
    main()
