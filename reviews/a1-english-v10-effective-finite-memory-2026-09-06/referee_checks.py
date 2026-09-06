#!/usr/bin/env python3
"""Independent exact diagnostics for A1 v10. Standard library only; no author imports.

Finite examples test algebra, perturbed-data evaluation and all-query causal
output error. They do not prove continuum entropy, priority or journal merit.
Usage: python referee_checks.py [OUTPUT_JSON]
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial
from pathlib import Path
import json
import sys

COUNTS = Counter()
SUMMARY = {}


def check(ok, category):
    if not ok:
        raise AssertionError(category)
    COUNTS[category] += 1


def norm(v, w):
    return max((abs(a-b) for a, b in zip(v, w)), default=F(0))


def dyadic(x, bits=14):
    return F(round(x*(1 << bits)), 1 << bits)


def farthest(points, M):
    selected = [0]
    while len(selected) < min(M, len(points)):
        available = [i for i in range(len(points)) if i not in selected]
        selected.append(max(available, key=lambda i: (min(norm(points[i], points[j])
                                                       for j in selected), -i)))
    return selected


def one_dim_optimum(xs, M):
    xs = sorted(xs)
    dp = {(0, 0): F(0)}
    for k in range(1, M+1):
        for j in range(1, len(xs)+1):
            options = [max(dp[k-1, i], (xs[j-1]-xs[i])/2)
                       for i in range(j) if (k-1, i) in dp]
            if options:
                dp[k, j] = min(options)
    return min(dp[k, len(xs)] for k in range(1, M+1) if (k, len(xs)) in dp)


def greedy_tests():
    samples = [(F(0), F(1, 9), F(1, 3), F(1, 3), F(1)),
               (F(1, 2),)*6,
               (F(0), F(1, 10**12), F(1, 4), F(1, 4)+F(1, 10**12), F(1))]
    tau = F(1, 128)
    for xs in samples:
        for sign in (-1, 1):
            noisy = [(x + sign*((-1)**i)*tau,) for i, x in enumerate(xs)]
            for M in range(1, len(xs)+2):
                ids = farthest(noisy, M)
                radius = max(min(abs(x-xs[j]) for j in ids) for x in xs)
                check(radius <= 2*one_dim_optimum(xs, min(M, len(xs)))+4*tau,
                      'signed_noise_greedy_radius')
                check(len(set(ids)) == len(ids) <= M, 'greedy_budget')


def labels(m):
    return tuple((i, j, m-i-j) for i in range(m+1) for j in range(m-i+1))


def polynomial_mul(p, f):
    out = {}
    for a, c in p.items():
        for i, v in enumerate(f):
            b = tuple(a[j]+int(i == j) for j in range(3))
            out[b] = out.get(b, F(0)) + c*v
    return out


def moment(a, label, prior):
    exponent = sum(x*y for x, y in zip(a, label))
    return prior/(exponent+prior)


def finite_moment_tests():
    N, kappa, tau, delta = 3, F(1, 32), F(1, 1024), F(1, 2**40)
    D = 270
    cells = ((F(1, 3), -F(1, 16), -F(1, 16)),
             (F(1, 3), F(1, 16), F(0)), (F(1, 3), F(0), F(1, 16)))
    commands = ((F(1, 4), F(1, 2), F(3, 4)),
                (F(3, 4), F(1, 4), F(1, 2)))
    basis = ((F(1, 2), F(0), F(0)), (F(1, 2), F(1, 32), F(0)),
             (F(1, 2), F(0), F(1, 32)))
    worst_error = F(0)
    for gap, prior in ((F(0), F(1)), (F(1, 10**12), F(1)), (F(1, 7), F(3))):
        a = (F(0), F(1), F(2)+gap)
        table = {b: moment(a, b, prior) for b in labels(N)}
        for sign in (-1, 1):
            table_tilde = {b: v+sign*((-1)**i)*delta for i, (b, v) in enumerate(table.items())}
            cells_tilde = tuple(tuple(c+sign*((-1)**(3*j+i))*delta for i, c in enumerate(row))
                                for j, row in enumerate(cells))
            def factor(c, u, x):
                if x < 3:
                    return tuple(u[x]*v for v in c[x])
                return tuple(sum((1-u[j])*c[j][i] for j in range(3)) for i in range(3))
            for n in range(3):
                for hist in product(tuple(product(commands, range(4))), repeat=n):
                    p, pt = {(0, 0, 0): F(1)}, {(0, 0, 0): F(1)}
                    for u, x in hist:
                        p = polynomial_mul(p, factor(cells, u, x))
                        pt = polynomial_mul(pt, factor(cells_tilde, u, x))
                    m = N-n
                    def linear(poly, t, alpha):
                        return sum(c*t[tuple(b[i]+alpha[i] for i in range(3))]
                                   for b, c in poly.items())
                    zero = (m, 0, 0)
                    z, zt = linear(p, table, zero), linear(pt, table_tilde, zero)
                    check(z >= kappa**n, 'true_prefix_evidence')
                    check(abs(zt-z) <= D*delta and zt >= z/2, 'perturbed_denominator_certificate')
                    exact, rounded = {}, {}
                    for alpha in labels(m):
                        A, At = linear(p, table, alpha), linear(pt, table_tilde, alpha)
                        direct_A = sum(c*moment(a, tuple(b[i]+alpha[i] for i in range(3)), prior)
                                       for b, c in p.items())
                        check(A == direct_A, 'formal_table_equals_direct_integral')
                        check(abs(At-A) <= D*delta, 'perturbed_numerator_certificate')
                        error = abs(At/zt-A/z)
                        worst_error = max(worst_error, error)
                        check(error <= (abs(At-A)+abs(zt-z))/zt <= 4*D*kappa**(-N)*delta,
                              'certified_quotient_error')
                        exact[alpha], rounded[alpha] = A/z, dyadic(At/zt)
                        check(abs(exact[alpha]-rounded[alpha]) <= tau,
                              'rounded_raw_state_error')
                    for word in product(basis, repeat=m):
                        q = {(0, 0, 0): F(1)}
                        for f in word:
                            q = polynomial_mul(q, f)
                        truth = sum(c*exact[b] for b, c in q.items())
                        estimate = dyadic(sum(c*rounded[b] for b, c in q.items()))
                        check(abs(estimate-truth) <= tau, 'all_physical_query_output_error')
    SUMMARY['largest_perturbed_raw_error_float'] = float(worst_error)
    SUMMARY['finite_moment_input_error'] = str(delta)
    SUMMARY['finite_moment_output_tolerance'] = str(tau)


def determinant_tests():
    for gap in (F(0), F(1, 10**12), F(1, 7)):
        a = (F(0), F(1), F(2)+gap)
        for m in (1, 2, 3):
            xs = [sum(b[i]*a[i] for i in range(3))/10 for b in labels(m) if b != (m, 0, 0)]
            left, selected, pivots = list(range(len(xs))), [], []
            while left:
                scores = {}
                for j in left:
                    score = F(1)
                    for i in selected:
                        score *= abs(xs[j]-xs[i])
                    scores[j] = score
                j = max(left, key=lambda j: (scores[j], -j))
                pivots.append(scores[j]); selected.append(j); left.remove(j)
            check(all(a >= b for a, b in zip(pivots, pivots[1:])), 'leja_nonincreasing')
            scale = F(1)
            for l in range(1, len(xs)+1):
                scale *= pivots[l-1]
                V = F(0)
                for indices in combinations(range(len(xs)), l):
                    val = F(1)
                    for i, j in combinations(indices, 2):
                        val *= abs(xs[i]-xs[j])
                    V = max(V, val)
                check(scale <= V <= factorial(l)*scale, 'exact_determinant_volume_comparison')
                check((V == 0) == (l > len(set(xs))), 'exact_collision_zero_tail')


def causal_toy_tests():
    # Exact reachable scalar dynamics, independent of the monomial examples:
    # s' = s/2 + (u+x)/4,  U=[1/4,3/4], x in {0,1}.
    # L=1/2, G=1/4, Q=(s,s^2,(1+s)/2), K<=2 on [0,1].
    grid = tuple(F(1, 4)+F(i, 8) for i in range(5))
    offgrid = tuple(F(5+2*i, 16) for i in range(4))
    h, tau, T = F(1, 16), F(1, 1024), 3
    alphabet = tuple(product(grid, (0, 1)))
    H = [tuple(product(alphabet, repeat=n)) for n in range(T+1)]
    def state(hist):
        s = F(1, 2)
        for u, x in hist:
            s = s/2 + (u+x)/4
        return s
    def queries(s):
        return (s, s*s, (1+s)/2)
    def evaluation(hist):
        # Signed, deterministic offline error followed by dyadic rounding.
        sign = 1 if sum(x for _, x in hist) % 2 else -1
        return dyadic(state(hist)+sign*tau/4)
    candidates = [[state(hist) for hist in stage] for stage in H]
    approx = [[evaluation(hist) for hist in stage] for stage in H]
    maximum_error, maximum_bound, nonvacuous = F(0), F(0), 0
    for M in (2, 4, 8):
        chosen = [farthest([(s,) for s in stage], M) for stage in approx]
        reps = [[H[n][i] for i in chosen[n]] for n in range(T+1)]
        centers = [[state(hist) for hist in stage] for stage in reps]
        ctilde = [[evaluation(hist) for hist in stage] for stage in reps]
        sample_radii = [max(min(abs(s-c) for c in centers[n]) for s in candidates[n])
                        for n in range(T+1)]
        for n in range(T+1):
            e_sample = one_dim_optimum(candidates[n], M) if n < 2 else F(1, 2*M)
            check(sample_radii[n] <= 2*e_sample+4*tau, 'toy_greedy_radius')
            check(len(centers[n]) <= M, 'toy_persistent_budget')
        transitions = []
        for n in range(T):
            transitions.append({(i, u, x): min(range(len(reps[n+1])),
                                  key=lambda j: (abs(evaluation(hist+((u, x),))-ctilde[n+1][j]), j))
                                for i, hist in enumerate(reps[n]) for u, x in alphabet})
        outputs = [[tuple(dyadic(q+((-1)**k)*tau/4) for k, q in enumerate(queries(c)))
                    for c in stage] for stage in centers]
        for n in range(T+1):
            for i, c in enumerate(centers[n]):
                for k, q in enumerate(queries(c)):
                    check(abs(outputs[n][i][k]-q) <= tau, 'toy_all_representative_outputs')
        for actual in product(tuple(product(offgrid, (0, 1))), repeat=T):
            i, truth, error_bound, A = 0, F(1, 2), F(0), F(0)
            for n, (u, x) in enumerate(actual):
                code = min(grid, key=lambda g: (abs(u-g), g))
                check(abs(u-code) <= h, 'toy_memoryless_command_name')
                i = transitions[n][i, code, x]
                truth = truth/2+(u+x)/4
                A = A/2+F(1, 4)
                error_bound = error_bound/2+h/4+sample_radii[n+1]+A*h+4*tau
                error = abs(truth-centers[n+1][i])
                check(error <= error_bound, 'toy_accumulated_causal_error')
                check(error_bound < 1, 'toy_nonvacuous_error_bound')
                nonvacuous += 1
                maximum_error, maximum_bound = max(maximum_error, error), max(maximum_bound, error_bound)
                for k, q in enumerate(queries(truth)):
                    check(abs(outputs[n+1][i][k]-q) <= 2*error_bound+tau,
                          'toy_all_queries_end_to_end')
    SUMMARY['toy_maximum_state_error'] = str(maximum_error)
    SUMMARY['toy_maximum_propagated_bound'] = str(maximum_bound)
    SUMMARY['toy_nonvacuous_history_checkpoint_checks'] = nonvacuous



def structural_floor_tests():
    calibrations = ((F(0), F(1)), (F(0), F(1), F(2)),
                    (F(0), F(1), F(2)+F(1, 10**12)),
                    (F(0), F(1), F(2), F(3)),
                    (F(0), F(1), F(2)+F(1, 32), F(3)+F(1, 64)))
    fixtures = 0
    for a in calibrations:
        r, D = len(a), a[-1]
        gap = min(a[i]-a[i-1] for i in range(1, r))
        for N in range(2, 9):
            k, m = N//2, N-N//2
            d0, H = (r-1)*k, N*D
            chain = {j*D for j in range(m+1)}
            chain.update(v+j*D for v in a[1:-1] for j in range(m))
            ordered = sorted(chain)
            check(len(ordered) == m*(r-1)+1, 'structural_chain_cardinality')
            check(min(y-x for x, y in zip(ordered, ordered[1:])) >= gap,
                  'structural_chain_uniform_separation')
            witness = [x/H for x in ordered[1:1+d0]]
            vol = F(1)
            for x, y in combinations(witness, 2):
                vol *= abs(y-x)
            check(vol >= (gap/H)**(d0*(d0-1)//2) > 0,
                  'positive_floor_determinant_witness')
            for M in (1, 2, 3, 8, 31, 128, 1000):
                b = 0
                while 1 << (b*d0) < M+1:
                    b += 1
                mesh = F(1, 1 << b)
                check(mesh**(2*d0) <= F(1, M*M), 'sharpened_precision_absorption')
            fixtures += 1
    SUMMARY['structural_floor_configurations'] = fixtures


def main():
    structural_floor_tests()
    greedy_tests()
    determinant_tests()
    finite_moment_tests()
    causal_toy_tests()
    result = {'status': 'passed', 'assertions': sum(COUNTS.values()),
              'categories': dict(COUNTS), 'measurements': SUMMARY,
              'author_code_imported': False,
              'scope': 'Finite exact diagnostics; not continuum proof, priority certification, or journal approval.'}
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('INDEPENDENT_DIAGNOSTICS.json')
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
