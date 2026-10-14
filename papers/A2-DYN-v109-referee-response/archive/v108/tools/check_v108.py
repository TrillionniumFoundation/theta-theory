#!/usr/bin/env python3
"""Exact rational diagnostics. These are not a continuum proof certificate."""
from fractions import Fraction as F
import json
import random


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def overlap(a, b, x, y):
    return max(F(0), min(b, y)-max(a, x))


def pool(rows, t, r, delta):
    p = d = e = F(0)
    orientations = []
    for a, b, c, loss in rows:
        plus = 0 < b-a < delta and a < t and t+r < b
        minus = (not plus) and 0 < b-a < delta and a < t-r and t < b
        q = int(plus)+int(minus)
        require(q in (0, 1), 'overlap exceeds one')
        p += q*(c+loss)
        d += q*c
        e += q*loss
        orientations.append((int(plus), int(minus)))
    return p, d, e, orientations


def checks():
    rng = random.Random(108)
    trials = 4000
    for _ in range(trials):
        t, r, delta = F(rng.randrange(-5, 6), 5), F(1, 5), F(3)
        rows = []
        for j in range(rng.randrange(1, 18)):
            a = F(rng.randrange(-30, 31), 10)
            b = a+F(rng.randrange(1, 30), 10)
            rows.append((a, b, F(rng.randrange(11), 10), F(rng.randrange(7), 10)))
        p, d, e, orientations = pool(rows, t, r, delta)
        require(p == d+e, 'envelope split')
        paired_window = sum(c*overlap(a,b,t-r,t+r)
                            for a,b,c,loss in rows if b-a < delta)
        require(r*d <= paired_window, 'finite paired-window bound')
        variation_window = sum(loss*overlap(a,b,t-delta,t+delta)/(b-a)
                               for a,b,c,loss in rows)
        require(e <= variation_window, 'full variation window')
        for row, (plus, minus) in zip(rows, orientations):
            a,b,_,_ = row
            if plus or minus:
                require(t-delta < a < b < t+delta, 'localization')
        u = sum(c*F(rng.randrange(11),10) for a,b,c,loss in rows if a<t<b)
        k = F(rng.randrange(1,31),10)
        v, residual = min(u,k*p), max(F(0),u-k*p)
        require(v+residual == u and 0 <= v <= u, 'positive source split')
        gamma = v/(k*p) if p else F(0)
        require(0 <= gamma <= 1 and k*gamma*p == v, 'attained certificate')
        require(v <= k*(paired_window/r+variation_window), 'paid source bound')
    p,d,e,q = pool([(F(0),F(4),F(1),F(0))],F(2),F(1),F(5))
    require(q == [(1,0)] and p == 1, 'two orientations double counted')
    require(pool([(F(0),F(1,100),F(1),F(0))],F(1,200),F(1,10),F(1))[0] == 0,
            'empty pool must retain short pulse')
    p,d,e,_ = pool([(F(0),F(1),F(0),F(3))],F(1,2),F(1,10),F(2))
    require(p == e == 3 and d == 0, 'zero paired trace loses variation payment')
    r,s,t = F(1,10),F(1,1000),F(1,2000)
    rows = [(F(0),s,F(1),F(0)), (3*s/8,r+7*s/8,F(1),F(0))]
    p,_,_,_ = pool(rows,t,r,F(1))
    require(p == 1 and all(b-a < r+s for a,b,c,e in rows), 'strict class inclusion')
    # Overlapping old comparison supports: use full physical overlap, not source disjointness.
    capacities = [F(2),F(3),F(5)]
    weights = [[F(1),F(1,2),F(0)],[F(1,2),F(1),F(1)]]
    n = max(sum(w[j] for w in weights) for j in range(3))
    kappa = F(2)
    demands = [F(7),F(13)]
    accepted = sum(min(d,kappa*sum(w*p for w,p in zip(row,capacities)))
                   for d,row in zip(demands,weights))
    require(accepted <= min(sum(demands),n*kappa*sum(capacities)), 'old-family domination')
    # Quantifier diagnostic only: artificial intervals, not Lorentz trajectories.
    fixed_r = F(1,10)
    for m in (100,1000,10000):
        ell = F(1,m)
        row = [(F(0),ell,F(1),F(0))]
        require(pool(row,ell/2,fixed_r,F(1))[0] == 0, 'fixed-window diagnostic')
        require(pool(row,ell/2,ell/4,F(1))[0] == 1, 'finite-count exhaustion diagnostic')
    require(F(1,16)-F(1,32) == F(1,32), 'epsilon exponent')
    require(F(1,32)*F(1,12) == F(1,384), 'outer exponent')
    return {'random_rational_trials': trials,
            'checks': ['one_copy_pool','paired_window','variation_window','localization',
                       'positive_split','attained_maximum','empty_capacity','zero_minimum_trace',
                       'strict_certificate_class','overlap_budget','old_family_domination',
                       'finite_count_exhaustion_only','outer_exponents'],
            'formal_proof_certificate': False, 'realized_lorentz_diagnostic': False}


if __name__ == '__main__':
    print(json.dumps(checks(), sort_keys=True, indent=2))
