#!/usr/bin/env python3
"""Independent finite diagnostics for A2 v45; no author diagnostic is imported.

Run: python independent_checks.py > CHECK_RESULTS.json
     python -O independent_checks.py > optimized.json
     cmp CHECK_RESULTS.json optimized.json

Inputs to the cochain inverse are abstract recovered support images, incidence
labels and integer deck marks, NOT laws, jets or the generating lattice. These
finite checks are not proofs, a channel-clearance algorithm, or a simulation of
an empirical-law-to-entire-analytic-boundary reconstruction. In particular the
random image configurations are not asserted to be admissible billiard tables.
"""
from __future__ import annotations
import cmath
import json
import math
import random
from typing import Any


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def sub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] - b[0], a[1] - b[1]


def lin(columns: tuple[complex, complex], x: tuple[int, int]) -> complex:
    return columns[0] * x[0] + columns[1] * x[1]


def gram(columns: tuple[complex, complex]) -> tuple[float, float, float]:
    a, b = columns
    return abs(a)**2, (a.conjugate() * b).real, abs(b)**2


def rotation(source: dict[int, complex], target: dict[int, complex],
             bezout: dict[int, int]) -> complex:
    """z_k(R_alpha C)=exp(-ik alpha) z_k(C); sum k*b_k=1."""
    require(sum(k * b for k, b in bezout.items()) == 1, 'not a Bezout identity')
    u = 1 + 0j
    for k, b in bezout.items():
        require(abs(source[k]) > 1e-10 and abs(target[k]) > 1e-10,
                'zero harmonic anchor')
        u *= (source[k] / target[k])**b
    require(abs(u) > 1e-10, 'zero rotation')
    u /= abs(u)
    require(max(abs(source[k] * u**(-k) - target[k])
                for k in bezout) < 1e-8, 'incompatible oriented images')
    return u


def reconstruct(n: int, edges: list[dict[str, Any]],
                bezout: dict[int, int]) -> tuple[tuple[complex, complex], list[complex]]:
    """The first n-1 edges form a tree; the last two close independent cycles."""
    require(n >= 1 and len(edges) == n + 1, 'wrong skeleton size')
    known = {edges[0]['a']: edges[0]['za']}
    rotations: dict[int, complex] = {}
    while len(rotations) < len(edges):
        before = len(rotations)
        for j, e in enumerate(edges):
            if j in rotations:
                continue
            choices = [(e['a'], e['za']), (e['b'], e['zb'])]
            available = [(a, z) for a, z in choices if a in known]
            if not available:
                continue
            a, z = available[0]
            u = rotation(z, known[a], bezout)
            for b, w in choices:
                aligned = {k: value * u**(-k) for k, value in w.items()}
                if b in known:
                    require(max(abs(aligned[k] - known[b][k]) for k in bezout)
                            < 1e-8, 'inconsistent incidence')
                else:
                    known[b] = aligned
            rotations[j] = u
        require(len(rotations) > before, 'disconnected incidence graph')
    require(len(known) == n, 'unreached obstacle')
    d = [rotations[j] * (e['cb'] - e['ca']) for j, e in enumerate(edges)]
    p: dict[int, complex] = {0: 0j}
    m: dict[int, tuple[int, int]] = {0: (0, 0)}
    while len(p) < n:
        before = len(p)
        for j, e in enumerate(edges[:n-1]):
            a, b, ell = e['a'], e['b'], e['ell']
            if a in p and b not in p:
                p[b], m[b] = p[a] + d[j], add(m[a], ell)
            elif b in p and a not in p:
                p[a], m[a] = p[b] - d[j], sub(m[b], ell)
        require(len(p) > before, 'not a spanning tree')
    eta, v = [], []
    for j in [n-1, n]:
        e = edges[j]
        eta.append(sub(add(m[e['a']], e['ell']), m[e['b']]))
        v.append(p[e['a']] + d[j] - p[e['b']])
    (a, c), (b, dd) = eta
    det = a * dd - b * c
    require(det != 0, 'rank-one deck gains')
    lattice = ((dd*v[0] - c*v[1])/det, (-b*v[0] + a*v[1])/det)
    centers = [p[i] - lin(lattice, m[i]) for i in range(n)]
    return lattice, centers


def generated_case(rng: random.Random, n: int, bezout: dict[int, int],
                   det_six: bool) -> tuple[list[dict[str, Any]], tuple[complex, complex], list[complex], complex]:
    lattice = (complex(rng.uniform(7, 11), rng.uniform(-1, 1)),
               complex(rng.uniform(-1, 1), rng.uniform(12, 16)))
    centers = [complex(rng.uniform(-3, 3), rng.uniform(-3, 3)) for _ in range(n)]
    # Arbitrary changes of obstacle representatives are explicitly included.
    centers = [z + lin(lattice, (rng.randint(-2, 2), rng.randint(-2, 2)))
               for z in centers]
    harmonics = [{k: rng.uniform(.0005, .001) * cmath.exp(1j*rng.uniform(-3, 3))
                  for k in bezout} for _ in range(n)]
    raw, m = [], [(0, 0)]
    for b in range(1, n):
        a = rng.randrange(b)
        ell = (rng.randint(-2, 2), rng.randint(-2, 2))
        m.append(add(m[a], ell))
        raw.append((a, b, ell))
    gains = [(2, 0), (1, 3)] if det_six else [(1, 0), (0, 1)]
    for eta in gains:
        a, b = rng.randrange(n), rng.randrange(n)
        raw.append((a, b, add(sub(eta, m[a]), m[b])))
    edges, first_pose = [], 0j
    for j, (a, b, ell) in enumerate(raw):
        pose = cmath.exp(1j*rng.uniform(-math.pi, math.pi))
        shift = complex(rng.uniform(-20, 20), rng.uniform(-20, 20))
        if j == 0:
            first_pose = pose
        edges.append({'a': a, 'b': b, 'ell': ell,
                      'ca': pose*centers[a]+shift,
                      'cb': pose*(centers[b]+lin(lattice, ell))+shift,
                      'za': {k: z*pose**(-k) for k, z in harmonics[a].items()},
                      'zb': {k: z*pose**(-k) for k, z in harmonics[b].items()}})
    return edges, lattice, centers, first_pose


def run() -> dict[str, Any]:
    rng = random.Random(450914)
    max_lattice = max_center = max_gram = 0.0
    cases = loops = nonunimodular = mode49 = 0
    for n in range(1, 7):
        for trial in range(20):
            for bezout in [{2: -1, 3: 1}, {4: -2, 9: 1}]:
                six = bool(trial % 2)
                edges, lattice, centers, frame = generated_case(rng, n, bezout, six)
                got, got_centers = reconstruct(n, edges, bezout)
                max_lattice = max(max_lattice, *(abs(got[i]-frame*lattice[i]) for i in range(2)))
                max_center = max(max_center, *(abs(got_centers[i]-frame*(centers[i]-centers[0])) for i in range(n)))
                max_gram = max(max_gram, *(abs(a-b) for a, b in zip(gram(got), gram(lattice))))
                cases += 1
                loops += n == 1
                nonunimodular += six
                mode49 += 4 in bezout
    require(max_lattice < 1e-9 and max_center < 1e-9 and max_gram < 1e-8,
            'cochain recovery error')
    negatives = {}
    for kind in ['rank_one', 'disconnected', 'zero_anchor', 'reflected_image']:
        edges, _, _, _ = generated_case(rng, 3, {2: -1, 3: 1}, False)
        if kind == 'rank_one':
            edges[-1] = dict(edges[-2])
        elif kind == 'disconnected':
            edges = [dict(edges[0]) for _ in range(4)]
        elif kind == 'zero_anchor':
            edges[0]['za'][3] = 0j
        else:
            edges[0]['za'] = {k: z.conjugate() for k, z in edges[0]['za'].items()}
        try:
            reconstruct(3, edges, {2: -1, 3: 1})
        except ValueError as error:
            negatives[kind] = str(error)
        else:
            raise RuntimeError(f'negative control accepted: {kind}')
    # A third unit disk centered at (4,1) touches the closest segment [1,7]
    # of the unit disks at (0,0) and (8,0). Tangency must be obstructed.
    replacement = 2*(math.sqrt(17)-2)
    require(replacement <= 6 and math.sqrt(17)-2 > 0, 'descent inequality')
    tangent_obstructed = abs(complex(4, 1)-complex(4, 0)) <= 1
    require(tangent_obstructed, 'tangency counted clear')
    # Independent non-even single-offset law/amplitude inverse on an interior box.
    d, anchor = 1.2, .23
    action = lambda u: .8*u*u + .13*u**3 + .07*u**4
    amplitude = lambda u: math.exp(.3*u + .2*u*u)
    density = lambda u, v: amplitude(u)*amplitude(v)*(d-action(u)-action(v))/1.7
    ratio = lambda u, v: density(u, v)*density(0, 0)/(density(u, 0)*density(0, v))
    q = math.sqrt(1-ratio(anchor, anchor))
    action_error = amplitude_error = 0.0
    for i in range(-30, 31):
        u = i/100
        t = (1-ratio(u, anchor))/q
        recovered = d*t/(1+t)
        recovered_b = density(u, 0)/density(0, 0)*(1+t)
        action_error = max(action_error, abs(recovered-action(u)))
        amplitude_error = max(amplitude_error, abs(recovered_b-amplitude(u)))
    require(action_error < 1e-10 and amplitude_error < 1e-10, 'density cancellation error')
    return {'status': 'pass', 'seed': 450914, 'abstract_recovered_image_cases': cases,
            'single_obstacle_loop_cases': loops, 'determinant_six_cases': nonunimodular,
            'gcd_one_modes_4_9_cases': mode49, 'max_lattice_error': max_lattice,
            'max_center_error': max_center, 'max_gram_error': max_gram,
            'rejected_negative_controls': negatives, 'tangency_obstructed': tangent_obstructed,
            'tangent_replacement_gap_sum': replacement, 'original_gap': 6,
            'non_even_action_error': action_error, 'unknown_amplitude_error': amplitude_error,
            'author_code_imported': False, 'mathematical_proof_certification': False,
            'random_configurations_claimed_admissible_billiards': False,
            'empirical_law_to_analytic_image_tested': False}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
