#!/usr/bin/env python3
"""Finite algebra and actual two-disk trajectory diagnostics, not proof certification."""
from fractions import Fraction as F
from itertools import combinations, product
from math import sin, cos, hypot, pi, sqrt, factorial
import json


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def coefficients(values):
    out = [F(1)]
    for a in values:
        out = [out[0]] + [out[k] + a * out[k - 1] for k in range(1, len(out))] + [a * out[-1]]
    return out


def solve(a, b):
    z = [list(row) + [rhs] for row, rhs in zip(a, b)]
    n = len(b)
    for j in range(n):
        k = max(range(j, n), key=lambda i: abs(z[i][j]))
        need(abs(z[k][j]) > 1e-14, 'singular Newton matrix')
        z[j], z[k] = z[k], z[j]
        d = z[j][j]
        z[j] = [x / d for x in z[j]]
        for i in range(n):
            if i != j:
                d = z[i][j]
                z[i] = [x - d * y for x, y in zip(z[i], z[j])]
    return [row[-1] for row in z]


def geometry(alpha, R):
    m = len(alpha) - 1
    ns = [(cos(a), sin(a)) for a in alpha]
    ts = [(-n[1], n[0]) for n in ns]
    qs = [(j % 2 + R * n[0], R * n[1]) for j, n in enumerate(ns)]
    h = [[0.0] * (m + 1) for _ in ns]
    g = [0.0] * (m + 1)
    length = 0.0
    vs = []
    dot = lambda u, v: u[0] * v[0] + u[1] * v[1]
    for i in range(m):
        dv = (qs[i + 1][0] - qs[i][0], qs[i + 1][1] - qs[i][1])
        tau = hypot(*dv)
        v = (dv[0] / tau, dv[1] / tau)
        vs.append(v)
        length += tau
        a, b = dot(v, ts[i]), dot(v, ts[i + 1])
        g[i] -= R * a
        g[i + 1] += R * b
        h[i][i] += R * dot(v, ns[i]) + R * R / tau * (1 - a * a)
        h[i + 1][i + 1] += -R * dot(v, ns[i + 1]) + R * R / tau * (1 - b * b)
        mixed = -R * R / tau * (dot(ts[i], ts[i + 1]) - a * b)
        h[i][i + 1] += mixed
        h[i + 1][i] += mixed
    cs = [dot(vs[i], ns[i]) for i in range(m)] + [-dot(vs[-1], ns[-1])]
    return dict(length=length, g=g, h=h, n=ns, tangent=ts, q=qs, v=vs, c=cs, alpha=alpha)


def orbit(m, R, theta, z):
    alpha = [0.0 if j % 2 == 0 else pi for j in range(m + 1)]
    target = [0.0] * (m + 1)
    target[0], target[m] = z * cos(theta), z * sin(theta)
    for _ in range(12):
        d = geometry(alpha, R)
        residual = [g - t for g, t in zip(d['g'], target)]
        if max(map(abs, residual)) < 2e-13:
            break
        step = solve(d['h'], [-r for r in residual])
        alpha = [a + da for a, da in zip(alpha, step)]
    else:
        raise RuntimeError('Newton did not converge')
    need(min(d['c']) > 0.99, 'nonphysical contact')
    need(max(abs(x) for x in d['g'][1:m]) < 2e-13, 'non-specular trajectory')
    need(abs(alpha[0]) < .005 and abs(alpha[m]) < .005, 'outside original angular square')
    need(abs(d['g'][0] / R) < .005 and abs(d['g'][m] / R) < .005, 'outside original momentum square')
    # Every actual flight is checked against all possible nearby third disks.
    for i in range(m):
        x, y = d['q'][i:i + 2]
        dx, dy = y[0] - x[0], y[1] - x[1]
        for a, b in product(range(-2, 3), repeat=2):
            O = (a + b / 2, b * sqrt(3) / 2)
            if O in ((i % 2, 0), ((i + 1) % 2, 0)):
                continue
            s = max(0., min(1., ((O[0] - x[0]) * dx + (O[1] - x[1]) * dy) / (dx * dx + dy * dy)))
            clearance = hypot(x[0] + s * dx - O[0], x[1] + s * dy - O[1]) - R
            need(clearance > .3, 'third-disk collision or insufficient checked clearance')
    return d


def run():
    block_cases = witness_cases = depth_cases = trajectory_pairs = 0
    for m in range(1, 8):
        for s in range(m):
            for S in combinations(range(1, m), s):
                for word in product(range(2), repeat=m):
                    blocks = []
                    at = 0
                    for i in S:
                        blocks.append(word[at:i])
                        at = i + 1
                    blocks.append(word[at:])
                    restored = []
                    for j, block in enumerate(blocks):
                        restored.extend(block)
                        if j < s:
                            restored.append(word[S[j]])
                    need(tuple(restored) == word, 'marked-word reconstruction')
                    need(sum(map(len, blocks)) == m - s, 'block lengths')
                    block_cases += 1

    for n in range(0, 6):
        thresholds = [F(1, i + 2) for i in range(n)]
        es = coefficients(thresholds)
        A = sum(thresholds)
        for cs in product((F(1, 5), F(1, 2), F(1)), repeat=n):
            N = sum(c < a for c, a in zip(cs, thresholds))
            upper = coefficients([a / c for a, c in zip(thresholds, cs)])
            for s in range(1, n + 1):
                actual = F(factorial(N), factorial(s) * factorial(N - s)) if N >= s else F(0)
                need(F(N >= s) <= actual <= upper[s], 'changing-witness positive insertion')
                need(es[s] <= A ** s / factorial(s), 'factorial elementary symmetric bound')
                witness_cases += 1

    for m in range(1, 40):
        for r in (F(4, 5), F(47, 53), F(97, 100)):
            for L in (1, 2, 3, 7, 20, 100):
                eps = F(1, 100)
                lhs = sum(2 * eps * r ** min(i, m - i) for i in range(1, m) if min(i, m - i) >= L)
                need(lhs <= 4 * eps * r ** L / (1 - r), 'depth-tail summation')
                depth_cases += 1

    for m, R, theta in product((2, 4, 6, 8), (.45, .46, .47), (0., .4, 1.4, 2.6, 4.2, 5.7)):
        old = orbit(m, R, theta, .00008)
        for z in (.00016, .00032):
            new = orbit(m, R, theta, z)
            bs = [1 - u[0] * v[0] - u[1] * v[1] for u, v in zip(old['n'], new['n'])]
            ss = [t[0] * n[0] + t[1] * n[1] for t, n in zip(old['tangent'], new['n'])]
            normal_old = R * sum((1 if i in (0, m) else 2) * old['c'][i] * bs[i] for i in range(m + 1))
            normal_new = R * sum((1 if i in (0, m) else 2) * new['c'][i] * bs[i] for i in range(m + 1))
            work_old = old['g'][0] * ss[0] + old['g'][m] * ss[m]
            work_new = new['g'][0] * ss[0] + new['g'][m] * ss[m]
            delta = new['length'] - old['length']
            need(delta > 0, 'roof is not increasing on common gradient ray')
            need(delta + 2e-12 >= normal_old + work_old, 'forward support inequality')
            need(-delta + 2e-12 >= normal_new - work_new, 'backward support inequality')
            need(work_new - work_old + 2e-12 >= normal_new + normal_old, 'summed support inequality')
            endpoint_range = sum(hypot(new['q'][i][0] - old['q'][i][0], new['q'][i][1] - old['q'][i][1]) for i in (0, m))
            need(abs(delta) <= endpoint_range + 1e-13, 'word roof-range inequality')
            trajectory_pairs += 1
            old = new
    return dict(status='passed', exact_marked_block_cases=block_cases,
                exact_witness_cases=witness_cases, exact_depth_tail_cases=depth_cases,
                actual_two_disk_trajectory_pairs=trajectory_pairs,
                trajectory_arithmetic='double precision Newton; original endpoint section checked',
                marked_witness_arithmetic='exact rational',
                theorem_proof_certified=False, original_LLT_certified=False)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
