#!/usr/bin/env python3
"""Exact finite diagnostics. They do not certify the universal theorems."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import random
from fractions import Fraction
from pathlib import Path

P = 1000003
SEED = 20260921110


def transpose(a):
    return [list(x) for x in zip(*a)]


def mm(a, b):
    bt = transpose(b)
    return [[sum(x*y for x, y in zip(row, col)) % P for col in bt] for row in a]


def rref(a):
    a = [[x % P for x in row] for row in a]
    pivots = []
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inv = pow(a[row][col], -1, P)
        a[row] = [(x*inv) % P for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                t = a[i][col]
                a[i] = [(x-t*y) % P for x, y in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    return a, pivots


def rank(a):
    return len(rref(a)[1])


def inv(a):
    n = len(a)
    rr, piv = rref([row + [int(i == j) for j in range(n)] for i, row in enumerate(a)])
    if piv[:n] != list(range(n)):
        raise ValueError('Singular matrix')
    return [row[n:] for row in rr]


def null(a):
    rr, piv = rref(a)
    free = [j for j in range(len(a[0])) if j not in piv]
    columns = []
    for j in free:
        v = [0]*len(a[0])
        v[j] = 1
        for i, col in enumerate(piv):
            v[col] = -rr[i][j] % P
        columns.append(v)
    return transpose(columns)


def det(a):
    a = [row[:] for row in a]
    result = 1
    for j in range(len(a)):
        i = next((i for i in range(j, len(a)) if a[i][j] % P), None)
        if i is None:
            return 0
        if i != j:
            a[j], a[i] = a[i], a[j]
            result = -result
        result = result*a[j][j] % P
        inverse = pow(a[j][j], -1, P)
        for i in range(j+1, len(a)):
            t = a[i][j]*inverse % P
            a[i] = [(x-t*y) % P for x, y in zip(a[i], a[j])]
    return result % P


def convolution(a, b):
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] = (out[i+j]+x*y) % P
    return out


def polynomial(roots):
    out = [1]
    for r in roots:
        out = convolution(out, [-r, 1])
    return out


def evaluate(coeff, t):
    y = 0
    for x in reversed(coeff):
        y = (y*t+x) % P
    return y


def native(k):
    roots = list(range(1, k+1))
    clocks = list(range(k+2, 3*k+3))
    jmat = []
    for ri in roots:
        di = math.prod(ri-t for t in clocks) % P
        di = di*pow(math.prod((ri-ra)**2 for ra in roots if ra != ri) % P, -1, P) % P
        jmat.append([(di*x) % P for x in polynomial([r for r in roots if r != ri])])
    score = [[1]+[-pow(t-r, -1, P) % P for r in roots]
             +[-pow(t-r, -1, P)**2 % P for r in roots] for t in clocks]
    zi = inv(score)[k+1:]
    for i in range(k):
        for j, t in enumerate(clocks):
            ps = math.prod(t-r for r in roots) % P
            pp = math.prod(t-u for u in clocks if u != t) % P
            xi = ps*ps*pow(pp, -1, P) % P
            assert zi[i][j] == xi*pow(ps, -1, P)*evaluate(jmat[i], t) % P
    return jmat, zi, roots, clocks


def witness(d, k, rng):
    jmat, zraw, roots, clocks = native(k)
    c = k-d
    for trial in range(1, 101):
        a = [[rng.randint(1, 7)] + [rng.randint(-7, 7) for _ in range(d-1)] for i in range(k)]
        if rank(a) != d:
            continue
        b = [[a[i][0]*x % P for x in a[i]] for i in range(k)]
        w = null(transpose(b))
        assert len(w[0]) == c
        u = mm(transpose(jmat), w)
        polys = transpose(u)
        pairs = list(itertools.combinations_with_replacement(range(c), 2))
        products = transpose([convolution(polys[i], polys[j]) for i, j in pairs])
        pivots = rref(products)[1]
        if len(pivots) != 2*k-1:
            continue
        # Finite-field nonincidence proves nonincidence over Q for these integer A.
        annihilator = transpose(null(transpose(a)))
        sign_count = 0
        separated = True
        z = [row[0] for row in a]
        for mask in range(1, 1 << (k-1)):
            signed = [z[0]] + [(-z[i] if mask & (1 << (i-1)) else z[i]) for i in range(1, k)]
            if all(sum(x*y for x, y in zip(row, signed)) % P == 0 for row in annihilator):
                separated = False
                break
            sign_count += 1
        if not separated:
            continue
        # Independent compression from the inverse raw score matrix.
        compressed = mm(transpose(w), zraw)
        raw_measure = [[compressed[i][j]*compressed[l][j] % P for j in range(len(clocks))]
                       for i, l in pairs]
        for h, (i, l) in enumerate(pairs):
            prod = convolution(polys[i], polys[l])
            for j, t in enumerate(clocks):
                ps = math.prod(t-r for r in roots) % P
                pp = math.prod(t-u for u in clocks if u != t) % P
                rho = ps*ps*pow(pp, -1, P)**2 % P
                assert raw_measure[h][j] == rho*evaluate(prod, t) % P
        assert rank(raw_measure) == 2*k-1
        square = [[row[j] for j in pivots] for row in products]
        minor = det(square)
        assert minor != 0
        return {'d': d, 'k': k, 'c': c, 'loading': a, 'trial': trial,
                'product_rank': len(pivots), 'raw_score_compression_rank': rank(raw_measure),
                'selected_product_columns': pivots, 'minor_mod_prime': minor,
                'nonconstant_sign_classes_excluded': sign_count,
                'target_strictly_positive': True}
    raise AssertionError(f'No certified loading found for {(d,k)}')


def run():
    threshold_cases = []
    for d in range(2, 501):
        c = next(c for c in range(1, d+10) if c*(c+1)//2 >= 2*(d+c)-1)
        # Integer arithmetic avoids floating-point ceiling errors.
        assert c*c-3*c-4*d+2 >= 0
        assert (c-1)*(c-1)-3*(c-1)-4*d+2 < 0
        threshold_cases.append([d, d+c, c])
    tested_bases = 0
    for n in range(4, 151):
        for a in range(2, n//2+1):
            q, r = divmod(n, a)
            s = set(range(a)) | set(range(a, q*a+1, a)) | set(range(n-a+1, n+1))
            assert {x+y for x in s for y in s} == set(range(2*n+1))
            assert len(s) <= 2*a+q-1
            tested_bases += 1
    referee_sets = [[0,1,3,5,6], [0,1,2,5,8,11,12,13]]
    for s in referee_sets:
        assert {a+b for a in s for b in s} == set(range(2*max(s)+1))
    # Exhaust the equality-threshold monomial cases without assuming the proof.
    monomial_failures = []
    for n, c in [(7,5), (10,6)]:
        tested = 0
        for s in itertools.combinations(range(n+1), c):
            assert len({a+b for a in s for b in s}) < 2*n+1
            tested += 1
        monomial_failures.append({'n': n, 'c': c, 'subsets_exhausted': tested})
    rng = random.Random(SEED)
    witnesses = [witness(d, k, rng) for d, k in [(2,7), (3,8), (5,11), (6,13)]]
    # Rational nonorthogonal normalization, using independent exact 2x2 formulas.
    def mulq(a,b):
        return [[sum(Fraction(x)*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
    def invq(a):
        t = a[0][0]*a[1][1]-a[0][1]*a[1][0]
        return [[Fraction(a[1][1],t), Fraction(-a[0][1],t)],
                [Fraction(-a[1][0],t), Fraction(a[0][0],t)]]
    b = [[3,1],[1,2]]
    o = [[2,1],[0,3]]
    kt = mulq(transpose(o),o)
    g = mulq(mulq(transpose(o),invq(b)),o)
    assert mulq(mulq(kt,invq(g)),kt) == mulq(mulq(transpose(o),b),o)
    return {'status': 'passed', 'scope': 'finite exact diagnostics, not universal proof certification',
            'prime': P, 'seed': SEED, 'threshold_cases': len(threshold_cases),
            'first_thresholds': threshold_cases[:9], 'additive_bases_tested': tested_bases,
            'referee_bases': referee_sets, 'monomial_exhaustions': monomial_failures,
            'native_witnesses': witnesses, 'nonorthogonal_identity': 'passed',
            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text)
