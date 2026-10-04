#!/usr/bin/env python3
"""Finite exact checks for A2 v38. These do not certify continuum proofs."""
from fractions import Fraction as F
import json
import math
import random

checks = 0

def require(condition, message):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(message)

def solve(a, b):
    """Small exact Gauss--Jordan solver; errors are never disabled by -O."""
    n = len(b)
    mat = [list(map(F, row)) + [F(rhs)] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if mat[i][col]), None)
        if pivot is None:
            raise RuntimeError('Singular exact system')
        mat[col], mat[pivot] = mat[pivot], mat[col]
        scale = mat[col][col]
        mat[col] = [x / scale for x in mat[col]]
        for i in range(n):
            if i != col and mat[i][col]:
                scale = mat[i][col]
                mat[i] = [x - scale*y for x, y in zip(mat[i], mat[col])]
    return [row[-1] for row in mat]

def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))

def matrix(k):
    sites = [(i, j) for i in range(-k, k+1) for j in range(-k, k+1)]
    n = len(sites)
    index = {z: i for i, z in enumerate(sites)}
    q = [[F(0) for _ in sites] for _ in sites]
    for i, (x, y) in enumerate(sites):
        for step in [(1,0),(-1,0),(0,1),(0,-1)]:
            z = (x+step[0], y+step[1])
            if z in index:
                q[i][index[z]] += F(1,4)
    return sites, q, index[(0,0)]

def stopping_vectors(q, origin):
    n = len(q)
    results = []
    for mask in range(1 << n):
        active = [i for i in range(n) if (mask >> i) & 1]
        m = [F(0)]*n
        if origin in active:
            a = [[F(i == j) - q[j][i] for j in active] for i in active]
            b = [F(i == origin) for i in active]
            for i, val in zip(active, solve(a, b)):
                m[i] = val
        results.append(m)
    return results

def main():
    global checks
    sites, q, origin = matrix(1)
    n = len(sites)
    ident = [[F(i == j)-q[i][j] for j in range(n)] for i in range(n)]
    h = solve(ident, [F(1)]*n)
    g = solve(ident, [F(i == origin) for i in range(n)])
    require(all(0 < x <= 5 for x in h), 'exit time bound')
    require(sum(g) == h[origin], 'Green row mass')
    vectors = stopping_vectors(q, origin)
    for m in vectors:
        require(all(0 <= m[i] <= g[i] for i in range(n)), 'Green dominance')
        require(sum(m) <= h[origin], 'occupation mass')
        stop = [F(i == origin)+sum(q[j][i]*m[j] for j in range(n))-m[i]
                for i in range(n)]
        require(all(x >= 0 for x in stop), 'flow feasibility')
    def value(f):
        return max(-dot(f, m) for m in vectors)
    rng = random.Random(38004)
    for _ in range(80):
        f = [F(rng.randrange(-8,9),8) for _ in sites]
        eps = [F(rng.randrange(0,5),32) for _ in sites]
        pert = [F(rng.choice([-1,1]))*e for e in eps]
        f2 = [x+y for x,y in zip(f,pert)]
        v, w = value(f), value(f2)
        require(abs(v-w) <= dot(g, eps), 'arbitrary-data Lipschitz')
        lo = value([x+e for x,e in zip(f,eps)])
        hi = value([x-e for x,e in zip(f,eps)])
        require(lo <= w <= hi, 'interval monotonicity')
    # Discrete analogues only: the target component is isolated from edge mass.
    # Values on the computational boundary are deliberately positive.
    for a in [F(0),F(1,4),F(1,2),F(1)]:
        for b in [F(0),F(1,3),F(1)]:
            physical = {(0,0): a, (1,1): b, (2,1): b, (1,2): b}
            def v(z): return physical.get(z,F(0))
            forcing = []
            for x,y in sites:
                avg = sum(v((x+dx,y+dy)) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])/4
                forcing.append(avg-v((x,y)))
            require(value(forcing) == a, 'nonzero boundary recovery')
    # A non-symmetric, centered lattice law with positive second moment.
    mu = [(-1,F(2,3)),(2,F(1,3))]
    require(sum(a*p for a,p in mu) == 0, 'centered non-symmetric design')
    require(sum(a*a*p for a,p in mu) == 2, 'trace variance')
    # Width and perimeter normalization, and unmatched-component deficits.
    for c in [F(1),F(3,2),F(2)]:
        for r in [F(1,2),F(1),F(3)]:
            for rho in [F(1),F(3,2),F(2)]:
                perimeter_over_pi = 2*(c+rho*r)
                flux_over_t = 2*c
                deficit_over_pi = perimeter_over_pi-flux_over_t
                require(deficit_over_pi == 2*rho*r, 'isotropic deficit')
                require(deficit_over_pi/(2*r) == rho, 'isotropic ratio')
    for m in [9,25,49]:
        for delta in [0.01,0.1,0.5]:
            for eps in [0.01,0.1,0.75]:
                hs=25
                reps=math.ceil(8*hs*hs/eps**2*math.log(4*m/delta))
                logfail=math.log(4*m)-reps*eps*eps/(8*hs*hs)
                require(logfail <= math.log(delta)+1e-12, 'batch confidence algebra')
    for beta in [F(1,4),F(1,2),F(1)]:
        s=6+beta
        require((F(3,2)*s+1)/(s-2) > 2, 'retained stationary rate')
    print(json.dumps({'schema':'a2-v38-finite-diagnostics-1','status':'passed',
                      'checks':checks,'enumerated_stopping_policies':len(vectors),
                      'formal_proof_certificate':False,'physical_sensor_executed':False},
                     sort_keys=True))

if __name__ == '__main__':
    main()
