#!/usr/bin/env python3
"""Independent exact diagnostics for the source-pinned A1 v9 review.

Python standard library only. No author code or repository input is imported.
Finite checks are not proofs of continuum entropy or uniform all-prior claims.
The small codebooks below test index-only execution, not optimal covering rates.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, product, zip_longest
import hashlib
import json
import math
from pathlib import Path
import platform
import random

SUBMISSION = 'e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5'
COUNTS: Counter[str] = Counter()
RNG = random.Random(190906)


def require(condition, family):
    if not condition:
        raise AssertionError(family)
    COUNTS[family] += 1


def multiply(values):
    result = Q(1)
    for value in values:
        result *= value
    return result


def matmul(a, b):
    return [[sum((x*y for x, y in zip(row, col)), Q(0))
             for col in zip(*b)] for row in a]


def rank(a):
    a = [list(map(Q, row)) for row in a]
    pivot = 0
    for col in range(len(a[0])):
        row = next((i for i in range(pivot, len(a)) if a[i][col]), None)
        if row is None:
            continue
        a[pivot], a[row] = a[row], a[pivot]
        divisor = a[pivot][col]
        a[pivot] = [v/divisor for v in a[pivot]]
        for i in range(pivot+1, len(a)):
            scale = a[i][col]
            if scale:
                a[i] = [x-scale*y for x, y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def greedy_nodes(nodes):
    remaining = list(enumerate(nodes))
    ordered, scales = [], []
    while remaining:
        idx = min(range(len(remaining)), key=lambda i:
                  (-multiply(abs(remaining[i][1]-y) for y in ordered),
                   remaining[i][1] if not ordered else Q(0), remaining[i][0]))
        _, x = remaining.pop(idx)
        scales.append(multiply(abs(x-y) for y in ordered))
        ordered.append(x)
    return ordered, scales


def volume(nodes, ell):
    return max(multiply(abs(x-y) for x, y in combinations(subset, 2))
               for subset in combinations(nodes, ell))


def matrix_checks():
    cases = [[Q(1, 3)]*6, [Q(1, 8), Q(1, 8), Q(1, 2), Q(7, 8), Q(1, 2)],
             [Q(1, 4), Q(1, 4)+Q(1, 10**12), Q(1, 4)+Q(1, 1000), Q(3, 4)]]
    cases += [[Q(RNG.randrange(17), 16) for _ in range(q)]
              for q in range(2, 10) for _ in range(3)]
    for nodes in cases:
        x, d = greedy_nodes(nodes)
        q, s = len(x), len(set(x))
        require(all(a >= b for a, b in zip(d, d[1:])) and
                all(d[j] == 0 for j in range(s, q)), 'Leja_order_and_zero_tail')
        # Columns of T are monic Newton polynomials in the power basis.
        columns, coef = [], [Q(1)]
        for j in range(q):
            columns.append(coef+[Q(0)]*(q-len(coef)))
            nxt = [Q(0)]*(len(coef)+1)
            for k, value in enumerate(coef):
                nxt[k] -= x[j]*value
                nxt[k+1] += value
            coef = nxt
        T = list(map(list, zip(*columns)))
        W = [[xi**j for j in range(q)] for xi in x]
        L = [[multiply(xi-y for y in x[:j])/d[j] if d[j] else Q(0)
              for j in range(q)] for xi in x]
        LD = [[L[i][j]*d[j] for j in range(q)] for i in range(q)]
        require(matmul(W, T) == LD, 'exact_power_Newton_factorization')
        require(all(abs(v) <= 1 for row in L for v in row) and
                all(abs(L[j][j]) == 1 for j in range(s)), 'bounded_active_triangular_factor')
        extended = [[L[i][j] if j < s else Q(i == j)
                     for j in range(q)] for i in range(q)]
        require(rank(extended) == q and rank(W) == s, 'zero_pivot_invertible_extension')
        for ell in range(1, q+1):
            v, p = volume(x, ell), multiply(d[:ell])
            require(p <= v <= math.factorial(ell)*p, 'maximal_minor_inequality')
    return len(cases)


@lru_cache(None)
def labels(r, m):
    if r == 1:
        return ((m,),)
    return tuple((k,)+tail for k in range(m+1) for tail in labels(r-1, m-k))


def exponent(a, alpha):
    return sum((x*k for x, k in zip(a, alpha)), Q(0))


def sums(a, m):
    return [exponent(a, alpha) for alpha in labels(len(a), m) if any(alpha[1:])]


def polynomial_product(p, f):
    out = {}
    for a, x in p.items():
        for b, y in f.items():
            out[a+b] = out.get(a+b, Q(0))+x*y
    return {a: x for a, x in out.items() if x}


def moment(b, prior):
    if prior == 0:
        return Q(1)/(b+1)
    if prior == 1:
        return Q(3)/(b+3)
    return Q(1, 2)/(b+1)+Q(1, 2)  # half uniform, half atom at one


def dd_integral(b, nodes, prior):
    # Divided differences of 1/(b+z+c), valid also at nonadjacent repeats.
    j = len(nodes)
    if prior == 1:
        return 3*(-1)**(j-1)/multiply(b+x+3 for x in nodes)
    v = Q((-1)**(j-1))/multiply(b+x+1 for x in nodes)
    return v if prior == 0 else v/2+Q(j == 1, 2)


def flag_checks():
    calibrations = [(Q(0), Q(1), Q(2)), (Q(0), Q(1), Q(65, 32)),
                    (Q(0), Q(1), Q(2), Q(3)),
                    (Q(0), Q(1), Q(65, 32), Q(97, 32)),
                    (Q(0), Q(1), Q(65, 32), Q(97, 32)+Q(1, 32**5))]
    count = 0
    for a, (n, m) in product(calibrations, [(1, 3), (2, 2), (3, 2)]):
        D = a[-1]
        tangent = sorted({j*D for j in range(n+1)} |
                         {x+j*D for x in a[1:-1] for j in range(n)})
        p = min(n*(len(a)-1), len(sums(a, m)))
        P = {Q(0): Q(1)}
        for j in range(1, n+1):
            P = polynomial_product(P, {Q(0): Q(1), D: Q(j, 16*(n+1))})
        raw = sums(a, m)
        shuffled = raw[:]
        RNG.shuffle(shuffled)
        for order, prior in product([raw, list(reversed(raw)), shuffled], range(3)):
            pairing = [[moment(b, prior)] +
                       [dd_integral(b, order[:j], prior) for j in range(1, p+1)]
                       for b in tangent]
            evidence = sum(c*moment(b, prior) for b, c in P.items())
            z = [sum(c*dd_integral(b, order[:j], prior) for b, c in P.items())/evidence
                 for j in range(1, p+1)]
            derivative = [[row[j+1]-row[0]*z[j] for j in range(p)] for row in pairing]
            require(rank(pairing) == p+1, 'arbitrary_prefix_Hermite_pairing_rank')
            require(rank(derivative) == p, 'normalization_loses_exactly_one')
            count += 1
    return count


def order_of_difference(a, b):
    return next(j for j, (x, y) in enumerate(zip_longest(a, b, fillvalue=0)) if x != y)


def energies(polys):
    polys = list(dict.fromkeys(polys))
    q = len(polys)
    w = {(i, j): order_of_difference(polys[i], polys[j]) for i, j in combinations(range(q), 2)}
    def weight(i, j):
        return w[tuple(sorted((i, j)))]
    def solve(ids, parent):
        if len(ids) == 1:
            return [0, 0]
        h = min(weight(i, j) for i, j in combinations(ids, 2))
        groups = []
        for i in ids:
            dest = next((g for g in groups if weight(i, g[0]) > h), None)
            if dest is None:
                groups.append([i])
            else:
                dest.append(i)
        table = [0]
        for g in groups:
            child = solve(g, h)
            nxt = [math.inf]*(len(table)+len(child)-1)
            for i, x in enumerate(table):
                for j, y in enumerate(child):
                    nxt[i+j] = min(nxt[i+j], x+y)
            table = nxt
        return [v+(h-parent)*k*(k-1)//2 for k, v in enumerate(table)]
    result = solve(list(range(q)), 0)
    brute = [0]+[min(sum(weight(i, j) for i, j in combinations(subset, 2))
                     for subset in combinations(range(q), k)) for k in range(1, q+1)]
    require(result == brute, 'tree_allocation_matches_subset_enumeration')
    return result


def geometry_checks():
    for polys in [[(1,), (1, 0, 1), (1, 1), (2,)],
                  [(1,), (1, 0, 0, 1), (1, 0, 0, 2), (1, 1), (2,), (2, 0, 1), (3,)],
                  [(0, 0, 1), (0, 0, 2), (0, 0, 2, 0, 1)]]:
        energies(polys)
    paths = []
    for k in [2, 3, 4, 7, 11]:
        a = [(0,)*(k+1), (1,)+(0,)*k, (2, 1)+(0,)*(k-1),
             (3, 1)+(0,)*(k-2)+(1,)]
        polys = [tuple(sum(alpha[i]*a[i][j] for i in range(4)) for j in range(k+1))
                 for alpha in labels(4, 2) if any(alpha[1:])]
        beta = energies(polys)
        require(beta == [0]*7+[1, 2, k+2], 'tangent_path_determinant_orders')
        b1 = (Q(1, 2)-0)/(Q(1, 3)-Q(1, 4))
        b2 = (Q(2*(k+2), 9)-Q(1, 2))/(Q(1, 4)-Q(2, 9))
        require((b1, b2) == (6, 8*k-2), 'three_regime_crossover_exponents')
        paths.append({'k': k, 'beta_1_to_9': beta[1:], 'budget_exponents': [int(b1), int(b2)]})
    for u, v in product([Q(j, 32) for j in range(-2, 3)], repeat=2):
        a = (Q(0), Q(1), 2+u, 3+v)
        dims = [min(3*n, len(set(sums(a, 5-n)))) for n in range(1, 5)]
        expected = 6 if u == v == 0 else 8 if u == 0 or v == u or v == 2*u else 9
        require(max(dims) == expected, 'signed_two_parameter_exact_peak')
        gaps = sorted([abs(u), abs(v-u), abs(v-2*u)], reverse=True)
        rho = max(abs(u), abs(v))
        require(gaps[0] <= 2*gaps[1] and rho/2 <= gaps[0] <= 3*rho,
                'three_gap_comparability')
    return paths


CELLS = ((Q(1, 4), Q(1, 16), Q(1, 16), Q(1, 16)),
         (Q(1, 4), -Q(1, 16), Q(0), Q(0)),
         (Q(1, 4), Q(0), -Q(1, 16), Q(0)),
         (Q(1, 4), Q(0), Q(0), -Q(1, 16)))
COMMANDS = ((Q(1, 4), Q(1, 3), Q(1, 2), Q(2, 3)),
            (Q(3, 4), Q(1, 2), Q(1, 3), Q(1, 4)))


def report_coeff(command, report):
    g = COMMANDS[command]
    if report < 4:
        return tuple(g[report]*v for v in CELLS[report])
    return tuple(sum((1-g[j])*CELLS[j][i] for j in range(4)) for i in range(4))


def raw_vector(P, a, m):
    z = sum(c/(b+1) for b, c in P.items())
    return {alpha: sum(c/(b+exponent(a, alpha)+1) for b, c in P.items())/z
            for alpha in labels(4, m)}


def transition(v, m, f):
    denominator = sum(f[i]*v[tuple((m-1)*(j == 0)+(j == i) for j in range(4))]
                      for i in range(4))
    require(denominator >= Q(3, 64), 'physical_report_denominator')
    return {alpha: sum(f[i]*v[tuple(alpha[j]+(j == i) for j in range(4))]
                       for i in range(4))/denominator for alpha in labels(4, m-1)}


def distance(v, w):
    return sum((v[key]-w[key])**2 for key in v)


class Machine:
    __slots__ = ('index',)
    def __init__(self):
        self.index = 0
    def accept(self, read_only_table, command, report):
        self.index = read_only_table[self.index, command, report]
        return self.index


def streaming_checks():
    fixtures = 0
    raw_comparisons = 0
    uv = [(Q(0), Q(0)), (Q(0), Q(1, 32)), (Q(1, 32), Q(1, 32)),
          (Q(1, 32), Q(1, 16)), (-Q(1, 32), Q(1, 32)),
          (Q(1, 32), Q(1, 32)+Q(1, 32**5))]
    for (u, v), M in product(uv, [1, 2, 4]):
        a = (Q(0), Q(1), 2+u, 3+v)
        books = [[raw_vector({Q(0): Q(1)}, a, 5)]]
        tables = []
        for n in range(5):
            candidates = { (i, c, x): transition(old, 5-n, report_coeff(c, x))
                           for i, old in enumerate(books[-1])
                           for c, x in product(range(2), range(5)) }
            unique = list({tuple(y.items()): y for y in candidates.values()}.values())
            size = min(M, len(unique))
            reps = [unique[j*(len(unique)-1)//max(1, size-1)] for j in range(size)]
            tables.append({key: min(range(size), key=lambda j: distance(y, reps[j]))
                           for key, y in candidates.items()})
            books.append(reps)
        for trial in range(5):
            machine = Machine()
            P = {Q(0): Q(1)}
            exact = books[0][0]
            for n in range(5):
                c, x = RNG.randrange(2), RNG.randrange(5)
                f = report_coeff(c, x)
                exact = transition(exact, 5-n, f)
                P = polynomial_product(P, {b: z for b, z in zip(a, f) if z})
                require(exact == raw_vector(P, a, 4-n), 'raw_update_matches_direct_integration')
                raw_comparisons += 1
                i = machine.accept(tables[n], c, x)
                require(0 <= i < M and all(0 <= value <= 1 for value in books[n+1][i].values()),
                        'index_budget_and_probability_bounds')
        require(Machine.__slots__ == ('index',), 'index_only_fixture')
        fixtures += 1
    return fixtures, raw_comparisons


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    matrices = matrix_checks()
    flags = flag_checks()
    paths = geometry_checks()
    fixtures, updates = streaming_checks()
    result = {'submission': SUBMISSION, 'seed': 190906,
              'generated_utc': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(), 'dependencies': 'Python standard library only',
              'program_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'passed': sum(COUNTS.values()), 'failed': 0,
              'checks_by_family': dict(sorted(COUNTS.items())),
              'matrix_configurations': matrices, 'normalized_flag_configurations': flags,
              'signed_calibration_grid_points': 25, 'tangent_paths': paths,
              'index_only_fixtures': fixtures, 'exact_raw_update_vector_comparisons': updates,
              'author_programs_executed': False, 'manuscript_compiled': False,
              'limits': 'Finite rational diagnostics, not continuum proofs, all-prior verification, optimal codebook construction, exhaustive priority certification or journal approval.'}
    text = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    print(text, end='')


if __name__ == '__main__':
    main()
