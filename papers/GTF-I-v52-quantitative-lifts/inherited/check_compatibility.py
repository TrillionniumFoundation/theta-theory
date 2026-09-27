"""Exact finite regressions for the v47 two-label theorems.

Uses rational arithmetic and explicit exceptions (also under python -O).
The analytic all-machine lower bounds are in the manuscript, not inferred
from these finite tests. This is not a general optimal-realization solver.
"""
from __future__ import annotations
import argparse
import itertools
import json
import random
from fractions import Fraction as F
from pathlib import Path
from typing import Sequence


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def mm(a, b):
    require(bool(a) and bool(b) and len(a[0]) == len(b), 'matrix shape')
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def transpose(a):
    return [list(x) for x in zip(*a)]


def mv(a, v):
    return [sum(x*y for x, y in zip(row, v)) for row in a]


def stochastic(a):
    require(bool(a) and bool(a[0]), 'empty row table')
    require(all(len(row) == len(a[0]) for row in a), 'ragged row table')
    require(all(all(x >= 0 for x in row) and sum(row) == 1 for row in a), 'not stochastic')


def decoder(a):
    require(all(-1 <= x <= 1 for row in a for x in row), 'decoder outside [-1,1]')


I = [[F(1), F(0)], [F(0), F(1)]]
R = [[F(0), F(-1)], [F(1), F(0)]]
SEEDS = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))]


def vertices(a):
    return [(a, F(0)), (F(0), a), (-a, -a)]


def bary(a, y):
    x, z = y
    return [(1+(2*x-z)/a)/3, (1+(2*z-x)/a)/3, (1-(x+z)/a)/3]


def frontier_machine(k0: int, k1: int, rho: F):
    """The three nontrivial matching witnesses from Theorem frontier47."""
    require(0 < rho <= F(1, 6), 'finite-frontier signal range')
    if k0 == k1 == 3:
        e = [bary(2*rho, [rho*t for t in x]) for x in SEEDS]
        t = [[bary(6*rho, mv(u, v)) for v in vertices(2*rho)] for u in (I, R)]
        d = vertices(6*rho)
    elif (k0, k1) == (2, 3):
        e = [[F(1), F(0)], [F(1), F(0)], [F(0), F(1)], [F(0), F(1)]]
        vs = [(rho/2, rho/2), (-rho/2, -rho/2)]
        t = [[bary(2*rho, mv(u, v)) for v in vs] for u in (I, R)]
        d = vertices(2*rho)
    elif (k0, k1) == (3, 2):
        e = [bary(2*rho, [rho*t for t in x]) for x in SEEDS]
        t = []
        for u in (I, R):
            rows = []
            for v in vertices(2*rho):
                p = (1+sum(mv(u, v))/2)/2
                rows.append([p, 1-p])
            t.append(rows)
        d = [(F(1), F(1)), (F(-1), F(-1))]
    else:
        require(k0 >= 1 and k1 >= 1, 'positive widths required')
        e = [[F(1)]+[F(0)]*(k0-1) for _ in SEEDS]
        t = [[[F(1)]+[F(0)]*(k1-1) for _ in range(k0)] for _ in range(2)]
        d = [(F(0), F(0)) for _ in range(k1)]
    stochastic(e)
    for rows in t:
        stochastic(rows)
    decoder(d)
    return e, t, d


def max_error(e, ts, d, rho):
    residuals = []
    for row, x in zip(e, SEEDS):
        for t, u in zip(ts, (I, R)):
            got = mm(mm([row], t), d)[0]
            residuals.extend(abs(a-rho*b)/2 for a, b in zip(got, mv(u, x)))
    return max(residuals)


def incidence(entry, n=2, alphabet=2, queries=2):
    i, word, j = entry
    v = 1 << i
    for t, a in enumerate(word):
        v ^= 1 << (n+t*alphabet+a)
    v ^= 1 << (n+len(word)*alphabet+j)
    return v


def solve_signs(rows: Sequence[tuple[int, int]]):
    """GF(2) solution or a list of row indices forming a contradiction."""
    basis = {}
    for i, (mask, sign) in enumerate(rows):
        require(mask >= 0 and sign in (0, 1), 'invalid parity row')
        witness = 1 << i
        while mask:
            pivot = mask.bit_length()-1
            if pivot not in basis:
                basis[pivot] = (mask, sign, witness)
                break
            bmask, bsign, bw = basis[pivot]
            mask ^= bmask
            sign ^= bsign
            witness ^= bw
        if not mask and sign:
            return None, [j for j in range(len(rows)) if witness >> j & 1]
    solution = 0
    for pivot in sorted(basis):
        mask, sign, _ = basis[pivot]
        bit = sign ^ ((mask & solution).bit_count() & 1)
        if bit:
            solution |= 1 << pivot
    return solution, None


def check_cycle(rows, indices):
    require(bool(indices) and len(set(indices)) == len(indices), 'empty/repeated certificate')
    mask = sign = 0
    for i in indices:
        require(0 <= i < len(rows), 'certificate index')
        mask ^= rows[i][0]
        sign ^= rows[i][1]
    require(mask == 0 and sign == 1, 'not a negative balanced certificate')


def row(p):
    return [p, 1-p]


def odd_regressions():
    rng = random.Random(4701)
    cases = coordinates = 0
    for nsteps in range(6):
        for _ in range(8):
            e = [row(F(rng.randrange(11), 10)) for _ in SEEDS]
            ts = [[ [row(F(rng.randrange(11), 10)) for _ in range(2)] for a in range(2)] for t in range(nsteps)]
            ds = [[F(rng.randrange(-10, 11), 10) for j in range(2)] for s in range(2)]
            h = [(e[i][0]-e[i][1]-e[i+2][0]+e[i+2][1])/2 for i in range(2)]
            d = [(ds[0][j]-ds[1][j])/2 for j in range(2)]
            for word in itertools.product(range(2), repeat=nsteps):
                prod = F(1)
                out = e
                for t, a in enumerate(word):
                    prod *= ts[t][a][0][0]-ts[t][a][1][0]
                    out = mm(out, ts[t][a])
                out = mm(out, ds)
                for i, j in itertools.product(range(2), repeat=2):
                    require((out[i][j]-out[i+2][j])/2 == h[i]*prod*d[j], 'odd-part identity')
                    coordinates += 1
                cases += 1
    return cases, coordinates


def diagonal(t, u):
    """Block diag(T,U^T), so row products match execution order."""
    a = [[F(0)]*(len(t[0])+2) for _ in range(len(t)+2)]
    for i, rr in enumerate(t):
        a[i][:len(t[0])] = rr
    for i, rr in enumerate(transpose(u)):
        a[len(t)+i][len(t[0]):] = rr
    return a


def gram_regressions():
    sums = []
    for shape in [(2, 3), (3, 2), (3, 3)]:
        rho = F(1, 10)
        e, ts, d = frontier_machine(*shape, rho)
        us = [list(rr)+[-rho*x for x in seed] for rr, seed in zip(e, SEEDS)]
        vs = [list(col)+list(unit) for col, unit in zip(zip(*d), I)]
        gs = [diagonal(t, u) for t, u in zip(ts, (I, R))]
        n = len(us[0])
        g = [[sum(u[i]*u[j] for u in us) for j in range(n)] for i in range(n)]
        outs = [mm(mm(transpose(a), g), a) for a in gs]
        g1 = [[sum(b[i][j] for b in outs) for j in range(len(outs[0]))] for i in range(len(outs[0]))]
        s2 = sum(mm(mm([v], g1), transpose([v]))[0][0] for v in vs)
        vals = [mm(mm([u], a), transpose([v]))[0][0] for u in us for a in gs for v in vs]
        require(s2 == sum(z*z for z in vals), 'Gram sum identity')
        # A direct fourth-power tensor identity on the same displayed examples.
        s4 = F(0)
        for u in us:
            for a in gs:
                z = mm([u], a)[0]
                for v in vs:
                    s4 += sum(z[i]*v[i] for i in range(len(z)))**4
        require(s4 == sum(z**4 for z in vals), 'fourth moment identity')
        sums.append({'profile': shape, 'sum_squares': str(s2), 'fourth_moment': str(s4)})
    return sums


def horizon_profiles():
    """Construct and enumerate the declared {1,2,4}-profile family."""
    rho = F(1, 6)
    axes = list(SEEDS)
    v = (F(1, 2), F(1, 2))
    orbit = [v]
    for _ in range(3):
        orbit.append(tuple(mv(R, orbit[-1])))
    checks = words = 0
    for nsteps in range(1, 5):
        for widths in itertools.product((1, 2, 4), repeat=nsteps+1):
            narrow = [t for t, k in enumerate(widths) if k == 2]
            if 1 in widths or len(narrow) >= 2:
                # Explicit legal fair-coin construction has the displayed error.
                e = [[F(1)]+[F(0)]*(widths[0]-1) for _ in axes]
                ts = [[[[F(1)]+[F(0)]*(widths[t+1]-1) for _ in range(widths[t])] for a in range(2)] for t in range(nsteps)]
                ds = [[F(0), F(0)] for _ in range(widths[-1])]
                expected = rho/2
            else:
                special = narrow[0] if narrow else nsteps+1
                points = [axes if t < special else [orbit[0], orbit[2]] if t == special else orbit for t in range(nsteps+1)]
                def project(y):
                    return (sum(y)/2, sum(y)/2)
                e = []
                for seed in axes:
                    point = project(seed) if special == 0 else seed
                    e.append([F(int(y == point)) for y in points[0]])
                ts = []
                for t in range(nsteps):
                    commands = []
                    for u in (I, R):
                        rows = []
                        for old in points[t]:
                            new = tuple(mv(u, old))
                            if t+1 == special:
                                new = project(new)
                            rows.append([F(int(y == new)) for y in points[t+1]])
                        commands.append(rows)
                    ts.append(commands)
                ds = [[rho*z for z in y] for y in points[-1]]
                expected = rho/4 if narrow else F(0)
            stochastic(e)
            for commands in ts:
                for t in commands:
                    stochastic(t)
            decoder(ds)
            err = F(0)
            for word in itertools.product(range(2), repeat=nsteps):
                for row0, seed in zip(e, axes):
                    got = [row0]
                    target = list(seed)
                    for t, a in enumerate(word):
                        got = mm(got, ts[t][a])
                        target = mv((I, R)[a], target)
                    out = mm(got, ds)[0]
                    err = max(err, max(abs(x-rho*y)/2 for x, y in zip(out, target)))
                words += 1
            require(err == expected, 'all-horizon profile witness')
            checks += 1
    return {'profiles': checks, 'words': words, 'maximum_horizon': 4}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    front = []
    for rho in [F(1, 100), F(1, 20), F(1, 10), F(1, 6)]:
        for k0, k1 in itertools.product(range(1, 4), repeat=2):
            e, ts, d = frontier_machine(k0, k1, rho)
            err = max_error(e, ts, d, rho)
            expected = F(0) if (k0, k1) == (3, 3) else rho/4 if (k0, k1) in [(2, 3), (3, 2)] else rho/2
            require(err == expected, 'frontier upper witness')
            front.append({'rho': str(rho), 'profile': [k0, k1], 'error': str(err)})
    entries = [(i, (a,), j) for i, a, j in itertools.product(range(2), repeat=3)]
    masks = [incidence(e) for e in entries]
    consistent = inconsistent = 0
    for signs in itertools.product([-1, 0, 1], repeat=8):
        rows = [(mask, int(s < 0)) for mask, s in zip(masks, signs) if s]
        sol, cert = solve_signs(rows)
        if cert is not None:
            check_cycle(rows, cert)
            require(len(cert) <= 7, 'certificate length')
            inconsistent += 1
        else:
            require(all(((mask & sol).bit_count() & 1) == sign for mask, sign in rows), 'parity solution')
            consistent += 1
    quarter = [(incidence((0, (0,), 0)), 0), (incidence((1, (0,), 1)), 0),
               (incidence((0, (1,), 1)), 0), (incidence((1, (1,), 0)), 1)]
    check_cycle(quarter, list(range(4)))
    # Exhaustively check the four-entry sign product for all factor sign choices.
    for factors in itertools.product([-1, 1], repeat=6):
        vals = [factors[i]*factors[2+a]*factors[4+j] for i, a, j in [(0,0,0),(1,0,1),(0,1,1),(1,1,0)]]
        require(vals[0]*vals[1]*vals[2]*vals[3] == 1, 'balanced product')
    negative = []
    tests = [
        ('row_mass', lambda: stochastic([[F(1), F(1)]])),
        ('negative_probability', lambda: stochastic([[F(-1), F(2)]])),
        ('decoder_range', lambda: decoder([[F(2)]])),
        ('false_cycle', lambda: check_cycle(quarter, [0,1,2])),
        ('duplicate_cycle', lambda: check_cycle(quarter, [0,0])),
        ('signal_range', lambda: frontier_machine(3,3,F(1,5))),
        ('empty_labels', lambda: frontier_machine(0,1,F(1,10))),
        ('ragged_table', lambda: stochastic([[F(1)], [F(1),F(0)]])),
    ]
    for name, test in tests:
        try:
            test()
        except ValueError:
            negative.append(name)
        else:
            raise RuntimeError('negative control escaped: '+name)
    cases, coords = odd_regressions()
    result = {
        'schema': 'gtf47.exact/1',
        'frontier_upper_witnesses': front,
        'ternary_sign_tables': 3**8,
        'consistent_tables': consistent,
        'negative_balanced_tables': inconsistent,
        'odd_word_cases': cases,
        'odd_mean_coordinates': coords,
        'balanced_factor_sign_assignments': 64,
        'gram_checks': gram_regressions(),
        'all_horizon_frontier_checks': horizon_profiles(),
        'negative_controls_detected': negative,
        'scope': 'Exact finite witnesses and identities; universal lower bounds and optimality are analytic proofs. No generic optimization, independent proof or priority certification.'
    }
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
