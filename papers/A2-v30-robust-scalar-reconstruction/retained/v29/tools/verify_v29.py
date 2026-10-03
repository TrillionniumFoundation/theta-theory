#!/usr/bin/env python3
"""Finite independent diagnostics for the scalar collision revision.
No physical apparatus, continuum proof certification, or minimax test.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math
import random
import re

COUNTS: Counter[str] = Counter()
ROOT = Path(__file__).resolve().parents[1]


def check(value: bool, group: str) -> None:
    if not value:
        raise RuntimeError(group)
    COUNTS[group] += 1


def segment_truth_tables() -> None:
    # Interior entries record arbitrary multiple intersections. Endpoints are
    # separately treated as solid starts, not as observed free-start flags.
    for n in range(2, 11):
        for occ in product((0, 1), repeat=n):
            hit = int(any(occ))
            forward = (1-occ[0])*hit
            reverse = (1-occ[-1])*hit
            check(forward-reverse == occ[-1]-occ[0], 'reversal_all_endpoint_cases')
    # Weighted, shifted preparation pairing; weights need not be symmetric.
    for n in range(3, 10):
        weights = [F((j+1)**2, sum(k*k for k in range(1, n+1))) for j in range(n)]
        for occ in product((0, 1), repeat=n+1):
            pf = sum(w*(1-occ[j])*int(occ[j] or occ[j+1]) for j, w in enumerate(weights))
            pr = sum(w*(1-occ[j+1])*int(occ[j] or occ[j+1]) for j, w in enumerate(weights))
            check(pf-pr == sum(w*(occ[j+1]-occ[j]) for j, w in enumerate(weights)),
                  'shifted_asymmetric_probability_balance')


def minimum_inverse() -> None:
    for n in range(2, 11):
        for values in product((0, 1), repeat=n):
            if min(values) != 0:
                continue
            diff = [values[i+1]-values[i] for i in range(n-1)]
            sums = [0]
            for d in diff:
                sums.append(sums[-1]+d)
            check(-min(sums) == values[0], 'binary_chain_inverse')
    rng = random.Random(291003)
    for m in range(1, 25):
        for _ in range(25):
            values = [F(rng.randrange(0, 100), 100) for _ in range(m+1)]
            values[rng.randrange(m+1)] = F(0)
            d = [values[j+1]-values[j] for j in range(m)]
            eps = F(1, 1000)
            noise = [F(rng.randrange(-100, 101), 100)*eps for _ in d]
            sums = [F(0)]
            perturbed = [F(0)]
            for delta, err in zip(d, noise):
                sums.append(sums[-1]+delta)
                perturbed.append(perturbed[-1]+delta+err)
            check(-min(sums) == values[0], 'nonnegative_chain_inverse')
            check(abs(-min(perturbed)-values[0]) <= m*eps, 'minimum_noise_bound')
            check(abs(min(max(-min(perturbed), 0), 1)-values[0]) <= m*eps,
                  'clipping_nonexpansive')
    # Explicitly exercise the excluded all-positive ambiguity, rather than
    # silently verifying a formula beyond its zero-witness hypothesis.
    check([0, 0] == [1-1, 1-1] and -min([0, 0, 0]) != 1,
          'zero_witness_is_necessary')


def geometric_segments() -> dict[str, int]:
    # Analytic segment/ellipse intersection is computed independently of the
    # balance formula. Long segments can meet several obstacles.
    bodies = [(0., 0., .4, .5), (2.2, .3, .5, .35), (-2.1, -.5, .3, .6)]
    def inside(q):
        return any(((q[0]-x)/rx)**2+((q[1]-y)/ry)**2 <= 1 for x,y,rx,ry in bodies)
    def meets(q, a):
        for x,y,rx,ry in bodies:
            u, w = (q[0]-x)/rx, (q[1]-y)/ry
            p, r = a[0]/rx, a[1]/ry
            A, B, C = p*p+r*r, 2*(u*p+w*r), u*u+w*w-1
            if C <= 0:
                return True
            disc = B*B-4*A*C
            if disc >= 0:
                lo, hi = (-B-math.sqrt(disc))/(2*A), (-B+math.sqrt(disc))/(2*A)
                if hi >= 0 and lo <= 1:
                    return True
        return False
    outcomes = Counter()
    rng = random.Random(10729)
    for _ in range(4000):
        q = (rng.uniform(-3, 3), rng.uniform(-1.5, 1.5))
        angle, length = rng.uniform(0, 2*math.pi), rng.uniform(.03, 5)
        a = (length*math.cos(angle), length*math.sin(angle))
        end = (q[0]+a[0], q[1]+a[1])
        b1 = int(not inside(q) and meets(q, a))
        b2 = int(not inside(end) and meets(end, (-a[0], -a[1])))
        outcomes[f'{b1}{b2}'] += 1
        check(b1-b2 == int(inside(end))-int(inside(q)), 'ellipse_first_hit_reversal')
    for outcome in ('00', '01', '10', '11'):
        check(outcomes[outcome] > 0, 'all_bit_pairs_exercised')
    return dict(outcomes)


def mollified_chain() -> None:
    # A finite nonnegative quadrature kernel tests the algebra of averaging.
    # It is not relabelled as a continuum convergence test.
    offsets = [F(-1, 20), F(0), F(1, 20)]
    weights = [F(1, 4), F(1, 2), F(1, 4)]
    t, m = F(1, 5), 5
    intervals = [(F(-1, 4), F(1, 4)), (F(7, 4), F(9, 4))]
    def chi(x): return F(any(lo <= x <= hi for lo, hi in intervals))
    def hit(x, a):
        if chi(x): return F(0)
        lo, hi = sorted((x, x+a))
        return F(any(max(lo, l) <= min(hi, r) for l, r in intervals))
    for k in range(-80, 81):
        x = F(k, 40)
        u = [sum(w*chi(x+j*t+o) for w,o in zip(weights, offsets)) for j in range(m+1)]
        check(min(u) == 0, 'expanded_component_zero_witness')
        d = []
        for j in range(m):
            balance = sum(w*(hit(x+j*t+o,t)-hit(x+(j+1)*t+o,-t))
                          for w,o in zip(weights, offsets))
            check(balance == u[j+1]-u[j], 'positive_kernel_average_balance')
            d.append(balance)
        sums = [F(0)]
        for value in d: sums.append(sums[-1]+value)
        check(-min(sums) == u[0], 'averaged_finite_chain_inverse')


def periods_and_rates() -> None:
    # Exhaustive uncoloured finite motifs; multiple equal bodies are permitted.
    sites = list(product(range(3), repeat=2))
    for bits in product((0, 1), repeat=9):
        motif = {p for p,b in zip(sites,bits) if b}
        if not motif: continue
        periods = []
        for v in sites:
            shift = lambda p, s: ((p[0]+s*v[0])%3, (p[1]+s*v[1])%3)
            local = all(shift(p,s) in motif for p in motif for s in (-1,1))
            global_equal = {shift(p,1) for p in motif} == motif
            check(local == global_equal, 'two_sided_full_motif_period')
            if local: periods.append(v)
        check(len(motif)%len(periods) == 0, 'period_quotient_free_action')
        check(len(periods) <= len(motif), 'period_index_bound')
    for m in range(1,100):
        eps = F(1,256*m)
        check(3*eps < F(1,32*m), 'candidate_mean_tolerance')
        check(2*m*F(1,32*m)+2*F(1,32) <= F(1,8), 'grid_occupation_tolerance')
    check(F(4,3)-F(1,3)==1 and F(4,3)-F(4,3)==0, 'compensated_kernel_moments')
    check(F(1)-2*F(1,6)==4*F(1,6)==F(2,3), 'C2_interpolation_balance')
    check(F(3,2)*F(2,3)==1 and 2*F(3,2)==3, 'scalar_resource_exponents')
    for Q in range(1,30):
        rationals = sorted({F(a,b) for b in range(1,Q+1) for a in range(-b,b+1)})
        check(all(y-x >= F(1,Q*Q) for x,y in zip(rationals,rationals[1:])),
              'rational_lock_separation')


def source_checks() -> None:
    main = (ROOT/'main.tex').read_text()
    text = main
    for item in re.findall(r'\\input\{([^}]+)\}', main):
        path = ROOT/(item+'.tex')
        check(path.is_file(), 'primary_input_present')
        text += '\n'+path.read_text()
    labels = re.findall(r'\\label\{([^}]+)\}',text)
    check(len(labels)==len(set(labels)), 'unique_labels')
    for ref in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text):
        check(ref in labels, 'resolved_cross_reference')
    bib = re.findall(r'\\bibitem\{([^}]+)\}',text)
    for cite in re.findall(r'\\cite\{([^}]+)\}',text):
        for key in cite.split(','): check(key in bib, 'resolved_citation')


def main() -> None:
    segment_truth_tables(); minimum_inverse(); details=geometric_segments()
    mollified_chain(); periods_and_rates(); source_checks()
    print(json.dumps({'schema':'a2-v29-diagnostics-1','status':'passed',
        'checks':dict(sorted(COUNTS.items())), 'total_checks':sum(COUNTS.values()),
        'independent_ellipse_outcomes':details,
        'scope':'Finite algebra, exact motifs, independent ellipse intersections and source references only',
        'physical_sensor_executed':False,'formal_proof_certificate':False},indent=2,sort_keys=True))

if __name__=='__main__': main()
