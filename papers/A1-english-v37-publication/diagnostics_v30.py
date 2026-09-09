#!/usr/bin/env python3
"""Exact finite diagnostics for A1's multilevel revision; not a proof certificate."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path

COUNTS: Counter[str] = Counter()

def check(condition: bool, category: str, detail: str = '') -> None:
    if not condition:
        raise ArithmeticError(f'{category}: {detail}')
    COUNTS[category] += 1

def density(u: F) -> F:
    if u <= 0:
        return 512 * (F(27)/(8-5*u)**3 - F(1)/(8+3*u)**3)
    return 512 * (F(27)/(8+3*u)**3 - F(1)/(8-5*u)**3)

def icbrt(n: int) -> int:
    if n < 0:
        raise ValueError('Nonnegative integer required')
    if not n:
        return 0
    x = 1 << ((n.bit_length()+2)//3)
    while True:
        y = (2*x+n//(x*x))//3
        if y >= x:
            break
        x = y
    while (x+1)**3 <= n:
        x += 1
    while x**3 > n:
        x -= 1
    return x

def certified_integral(n: int = 8192, scale: int = 10**10) -> tuple[F,F]:
    lower = F(0); upper = F(0)
    for lo, hi, length, increasing in ((F(-8,7),F(0),F(1,42),True),
                                      (F(0),F(8,9),F(1,54),False)):
        bounds = []
        previous = None
        for i in range(n+1):
            f = density(lo+(hi-lo)*F(i,n))
            check(f >= 0, 'density_nonnegative')
            if previous is not None:
                check((f >= previous) if increasing else (f <= previous),
                      'density_endpoint_order')
            previous = f
            v = f*scale**3
            root = icbrt(v.numerator//v.denominator)
            check(root**3 <= v < (root+1)**3, 'rational_cube_root_enclosure')
            high = root if F(root**3) == v else root+1
            bounds.append((F(root,scale),F(high,scale)))
        if increasing:
            lower += length/n*sum((p[0] for p in bounds[:-1]),F(0))
            upper += length/n*sum((p[1] for p in bounds[1:]),F(0))
        else:
            lower += length/n*sum((p[0] for p in bounds[1:]),F(0))
            upper += length/n*sum((p[1] for p in bounds[:-1]),F(0))
    return lower, upper

def matrix_game_2x2(a: tuple[F,F,F,F]) -> tuple[F,F,F,F]:
    aa,ab,ba,bb = a
    xp = {F(0),F(1)}
    den = aa-ba-ab+bb
    if den:
        p = (bb-ba)/den
        if 0 <= p <= 1:
            xp.add(p)
    pv,p = min((max(p*aa+(1-p)*ba,p*ab+(1-p)*bb),p) for p in xp)
    xq = {F(0),F(1)}
    den = aa-ab-ba+bb
    if den:
        q = (bb-ab)/den
        if 0 <= q <= 1:
            xq.add(q)
    dv,q = max((min(q*aa+(1-q)*ab,q*ba+(1-q)*bb),q) for q in xq)
    return pv,dv,p,q

def affine_star(U: F) -> dict:
    # This is the exact affine/contact-order model, not an exact finite-theta detector evaluation.
    edge_branches = (((F(7,2),F(0)),),
                     ((F(3),F(0)),(F(9,2),-3*U)),
                     ((F(1,2),F(0)),))
    all_lines = {(F(0),F(0))}; order_lines = []
    for order in permutations(range(4)):
        pos = {v: i for i,v in enumerate(order)}
        lines = {(F(0),F(0))}
        for j in range(1,4):
            cut = [e for e in range(3) if (pos[0] < j) != (pos[e+1] < j)]
            for choices in product(*(edge_branches[e] for e in cut)):
                lines.add((sum((v[0] for v in choices),F(0)),
                           sum((v[1] for v in choices),F(0))))
        order_lines.append(lines); all_lines.update(lines)
    times = {F(0)}
    for (m,b),(n,c) in combinations(all_lines,2):
        if m != n:
            t = (c-b)/(m-n)
            if t >= 0:
                times.add(t)
    times = sorted(times)
    slopes = [max(m for m,b in lines) for lines in order_lines]
    best_slope = min(slopes)
    values = [[max(m*t+b for m,b in lines) for t in times] for lines in order_lines]
    optimum = [min(v[i] for v in values) for i in range(len(times))]
    candidates = [i for i,d in enumerate(slopes) if d == best_slope]
    r1 = min(max(v-g for v,g in zip(values[i],optimum)) for i in candidates)
    r2 = min(max(min(values[i][k],values[j][k])-optimum[k] for k in range(len(times)))
             for i,j in combinations(range(24),2) if min(slopes[i],slopes[j]) == best_slope)
    check(r1 == U, 'fixed_calibration_optimized_finite')
    check(r2 == 0, 'two_menu_zero_affine_excess')
    check(any(d > best_slope for d in slopes), 'prescribed_infinite_menu_negative_control')
    tail = max(times)+10*(1+U)
    winning = min(range(24),key=lambda i: max(m*tail+b for m,b in order_lines[i]))
    for t in (tail,2*tail,10*tail):
        check(max(m*t+b for m,b in order_lines[winning]) ==
              min(max(m*t+b for m,b in lines) for lines in order_lines),
              'eventual_single_order')
    return {'U':str(U),'r1':str(r1),'r2':str(r2),'critical_points':len(times)}

def main() -> None:
    witnesses = {}
    check(density(F(-8,7)) == density(F(8,9)) == 0 and density(F(0)) == 26,
          'density_endpoints')
    def left(u): return F(27,10)/(8-5*u)**2 + F(1,6)/(8+3*u)**2
    def right(u): return -F(27,6)/(8+3*u)**2 - F(1,10)/(8-5*u)**2
    mass = F(512,48)*(left(F(0))-left(F(-8,7))+right(F(8,9))-right(F(0)))
    check(mass == F(1,2), 'full_continuous_mass')
    check(F(5,16)+F(3,16)+mass == 1, 'full_mixed_mass')
    check(96*26**2*128 == 8306688, 'unit_occupation_coefficient')
    check(F(8,15)-F(4,9) == F(4,45), 'full_support_width')
    check(F(8306688,64800) < 129, 'finite_budget_gap_bound')
    for M,s in product((1,2,3,7,32),(F(1),F(1,2),F(1,5))):
        b2 = F(4*26**2*128*M*M)/(s*s)
        check(F(1,24)/b2 == s*s/F(8306688*M*M), 'atom_aware_unit_cost')
        for x in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
            y = max(F(0),x-F(1,2))
            cost = y**3/(3*b2)
            endpoint = y*y/b2
            integrated = y*endpoint-F(2,3)*y**3/b2
            check(cost == integrated, 'exact_layer_cake_cost')
            check(cost <= x/(24*b2), 'predictable_dominates_convex_local_cost')
        check(max(F(0),F(1,2)-F(1,2))**3/(3*b2) == 0,
              'unanchored_two_route_zero')
    for gains in product((F(1),F(1,2),F(1,3)),repeat=4):
        a = tuple(s*s for s in gains)
        pv,dv,p,q = matrix_game_2x2(a)
        check(pv == dv, 'exact_primal_dual_2x2')
        for M in (1,3,11):
            scaled = tuple(x/F(8306688*M*M) for x in a)
            p2,d2,_,_ = matrix_game_2x2(scaled)
            check(p2 == d2 == pv/F(8306688*M*M), 'all_budget_common_design_factor')
    family = []
    for J in range(2,33):
        a = [[F(1) if r==j else F(1,J*J) for j in range(J)] for r in range(J)]
        val = F(1,J)+F(1,J*J)-F(1,J**3)
        for j in range(J):
            check(sum(a[r][j] for r in range(J))/J == val, 'balanced_primal')
        for r in range(J):
            check(sum(a[r])/J == val, 'balanced_dual')
        check(val/F(1,J*J) == J+1-F(1,J), 'separate_checkpoint_penalty')
        if J in (2,3,8,32):
            family.append({'J':J,'V':str(val),'penalty':str(J+1-F(1,J))})
    # Fresh three-point blocks: condition on any past-selected next vertex before seeing its block.
    points = (F(1,4),F(1,2),F(3,4)); weights = (F(1,4),F(1,2),F(1,4))
    for threshold in points:
        selected = [0 if old <= threshold else 1 for old in points]
        for node,gain in enumerate((F(1),F(1,3))):
            visit = sum((p for p,n in zip(weights,selected) if n==node),F(0))
            joint = sum((po*pn*gain**2*(z-F(1,2))**2
                         for po,n in zip(weights,selected) for pn,z in zip(weights,points)
                         if n==node),F(0))
            check(joint == visit*gain**2/F(32), 'predictable_selected_fresh_block')
    # A branching/recombining network: the middle vertex is common and its loss is compulsory.
    for left,right,common in product((F(1,4),F(1)),repeat=3):
        rows = (left,common,right,common)
        pv,dv,p,q = matrix_game_2x2(rows)
        check(pv == dv == max(min(left,right),common), 'recombining_network_compulsory_level')
    witnesses['affine_star'] = [affine_star(U) for U in (F(0),F(1),F(3),F(17,2))]
    lo,hi = certified_integral()
    klo,khi = lo**3/1536,hi**3/1536
    ratio_lo,ratio_hi = 8306688*klo,8306688*khi
    check(F(405,100) < ratio_lo < ratio_hi < F(406,100), 'sharp_ratio_rational_enclosure')
    witnesses['balanced_families'] = family
    witnesses['sharp_coefficient'] = {'lower_exact':str(klo),'upper_exact':str(khi),
                                    'lower_decimal_approximation':float(klo),
                                    'upper_decimal_approximation':float(khi)}
    witnesses['limiting_gap'] = {'lower_exact':str(ratio_lo),'upper_exact':str(ratio_hi),
                               'lower_decimal_approximation':float(ratio_lo),
                               'upper_decimal_approximation':float(ratio_hi)}
    witnesses['finite_gap_bound'] = str(F(8306688,64800))
    print(json.dumps({'schema':'A1-v30-multilevel-diagnostics-1',
                      'checks':sum(COUNTS.values()),'categories':dict(sorted(COUNTS.items())),
                      'arithmetic':'Exact rationals and integer cube roots; decimals are display approximations.',
                      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'scope':'Finite arithmetic and model identities. Not continuum theorem verification, exhaustive priority research, or a native two-volume build.',
                      'integral_method':'8192 monotone subintervals on each side, integer cube-root scale 10^10; monotonicity follows analytically from the displayed density derivatives.',
                      'witnesses':witnesses},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
