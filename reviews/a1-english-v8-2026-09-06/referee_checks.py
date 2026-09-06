#!/usr/bin/env python3
"""Independent finite diagnostics for the source-pinned A1 v8 review.

Run: python3 referee_checks.py [output.json]
Requires Python 3.10+ and SymPy. Imports no manuscript or author test code.
Exact finite examples do NOT verify continuum covering, arbitrary-prior
minorization, optimal codebooks, asymptotic rates, or journal significance.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import math
import platform
import random
import sys
import sympy as sp

CHECKS = []
DETAILS = {}
ZERO = (0, 0)
A = (ZERO, (1, 0), (2, 1))


def check(name, assertion, **data):
    if not assertion:
        raise AssertionError((name, data))
    CHECKS.append({'name': name, 'passed': True, **data})


def sums(a, m):
    out = {ZERO}
    for _ in range(m):
        out = {(x + u, y + v) for x, y in out for u, v in a}
    return sorted(out)


def jets(a, m):
    counts = Counter(x for x, _ in sums(a, m))
    return sorted(((x, k) for x, c in counts.items() for k in range(c)
                   if (x, k) != ZERO), key=lambda z: (z[1], z[0]))


def moment(x, k=0, prior=0):
    """Integral t^x (log t)^k/k! for three fixed full-support priors."""
    x = F(x)
    if prior == 0:
        return F((-1)**k, 1) / (x + 1)**(k + 1)
    if prior == 1:
        return F(3 * (-1)**k, 1) / (x + 3)**(k + 1)
    if prior == 2:
        return (moment(x, k, 0) / 2
                + F(int(k == 0 and x == 0), 4)
                + F(int(k == 0), 4))
    raise ValueError('unknown prior')


def rank(rows):
    return sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(rows)).rank()


def multiply(p, q):
    out = {}
    for (a, b), c in p.items():
        for (x, y), d in q.items():
            key = (a + x, b + y)
            out[key] = out.get(key, F(0)) + c * d
    return {k: v for k, v in out.items() if v}


def integral(p, theta, prior, shift=ZERO):
    a, b = shift
    return sum((c * moment(x + a + theta * (y + b), prior=prior)
                for (x, y), c in p.items()), F(0))


def flag_checks():
    families = [(A, 1, 4), (A, 2, 3), (A, 4, 3), (A, 9, 5),
                ((ZERO, (1, 1), (2, -1), (3, 2)), 3, 3)]
    for a, n, m in families:
        D = a[-1][0]
        rows = sorted({j * D for j in range(n + 1)} |
                      {x + j * D for x, _ in a[1:-1] for j in range(n)})
        cap = min(n * (len(a) - 1), len(jets(a, m)))
        # Every initial flag is checked for the smaller examples. The 19x19
        # higher-multiplicity endpoint is checked without enumerating all minors.
        stops = range(1, cap + 1) if cap < 12 else (10, 17, cap)
        for p in stops:
            cols = [ZERO] + jets(a, m)[:p]
            for prior in (0, 1, 2):
                L = [[moment(x + y, k, prior) for x in rows] for y, k in cols]
                check(f'flag-rank-r{len(a)}-n{n}-m{m}-p{p}-prior{prior}',
                      rank(L) == p + 1)
                # Actual positive binomial product; its coefficients sit in
                # the monomial tangent, rather than an arbitrary image vector.
                coeff = [F(1)]
                for j in range(1, n + 1):
                    new = [F(0)] * (len(coeff) + 1)
                    for i, c in enumerate(coeff):
                        new[i] += c
                        new[i + 1] += c * F(j, 64 * (n + 1))
                    coeff = new
                z = [sum((c * moment(j * D + y, k, prior)
                          for j, c in enumerate(coeff)), F(0)) for y, k in cols]
                J = [[(L[i][j] * z[0] - z[i] * L[0][j]) / z[0]**2
                      for j in range(len(rows))] for i in range(1, len(cols))]
                check(f'normalized-rank-r{len(a)}-n{n}-m{m}-p{p}-prior{prior}', rank(J) == p)
    cols = sorted([ZERO] + jets(A, 3)[:8])
    det = sp.Matrix([[moment(i + x, k) for x, k in cols] for i in range(9)]).det(method='domain-ge')
    check('seven-trial-signed-nine-by-nine-minor', det > 0)
    DETAILS['seven_trial_minor'] = str(det)
    check('seven-selected-orders', [k for _, k in jets(A, 3)[:8]] == [0]*6 + [1]*2)
    check('higher-order-selected-flag', [k for _, k in jets(A, 5)[:18]] == [0]*10 + [1]*7 + [2])
    DETAILS['n9_m5_selected_orders'] = [k for _, k in jets(A, 5)[:18]]


def divided(values, nodes):
    while len(values) > 1:
        order = len(nodes) - len(values) + 1
        values = [(values[j + 1] - values[j]) / (nodes[j + order] - nodes[j])
                  for j in range(len(values) - 1)]
    return values[0]


def metric_checks():
    for m in (2, 3, 5):
        groups = {}
        for a, b in sums(A, m):
            groups.setdefault(a, []).append(b)
        for theta in (F(1, 128), F(1, 7)):
            for prior in (0, 2):
                identities = 0
                for a, gammas in groups.items():
                    nodes = [a + theta*g for g in gammas]
                    vals = [moment(x, prior=prior) for x in nodes]
                    ds = [divided(vals[:k+1], nodes[:k+1]) for k in range(len(vals))]
                    for j, value in enumerate(vals):
                        newton = sum((theta**k * math.prod(gammas[j] - gammas[v] for v in range(k))
                                      * ds[k] for k in range(j+1)), F(0))
                        if newton != value:
                            raise AssertionError('Newton physical identity')
                        identities += 1
                check(f'newton-fixed-triangular-m{m}-theta{theta}-prior{prior}', True, identities=identities)
    basis = [{ZERO:F(1,2)}, {ZERO:F(1,2),(1,0):F(1,64)},
             {ZERO:F(1,2),(2,1):F(1,64)}]
    for m in (1, 2, 3, 4):
        b = sums(A, m)
        rows = []
        for word in product(range(3), repeat=m):
            p = {ZERO:F(1)}
            for j in word:
                p = multiply(p, basis[j])
            rows.append([p.get(x, F(0)) for x in b])
        check(f'physical-product-menu-rank-m{m}', rank(rows) == len(b), formal_dimension=len(b))


def profile_checks():
    for theta, expected in ((F(0), [0,2,4,6,6,4,2,0]),
                            (F(1,8), [0,2,4,6,8,5,2,0]),
                            (F(1,2), [0,2,4,6,8,5,2,0])):
        profile = [min(2*n, len({a+theta*b for a,b in sums(A,7-n)})-1) for n in range(8)]
        check(f'exact-seven-profile-{theta}', profile == expected, profile=profile)
    # Work with exact logarithms: theta=2^-t, M=2^b.
    # Each candidate equals 2^-e, where e=2(S*t+b)/ell.
    for t in (0, 1, 3, 11):
        for b in (0, 1, 4, 6, 15, 40, 100, 400):
            e = [F(2*(sum(k for _,k in jets(A,3)[:ell])*t+b),ell) for ell in range(1,9)]
            check(f'seven-envelope-t{t}-b{b}', min(e) == min(F(b,3),F(t,2)+F(b,4)))
            e2 = [F(2*(sum(k for _,k in jets(A,5)[:ell])*t+b),ell) for ell in range(1,19)]
            check(f'higher-order-envelope-t{t}-b{b}', min(e2) == min(F(b,5),F(14*t+2*b,17),F(t)+F(b,9)))
    check('higher-order-crossovers-exact', F(14+20,17)==2 and F(14+54,17)==4 and 1+F(27,9)==4)
    rng=random.Random(57083)
    for case in range(60):
        dim=rng.randint(1,10); M=rng.randint(1,10000)
        sides=sorted([2.0**(-rng.randint(0,50)) for _ in range(dim)],reverse=True)
        e=max((math.prod(sides[:k])/M)**(1/k) for k in range(1,dim+1))
        counts=[max(1,math.floor(a/e*(1-1e-14))) for a in sides]
        check(f'integer-box-allocation-{case}', math.prod(counts)<=M and max(a/c for a,c in zip(sides,counts))<=2*e*(1+1e-12))


def report_factor(command, report):
    k = [{ZERO:F(1,3),(1,0):-F(1,12),(2,1):-F(1,12)},
         {ZERO:F(1,3),(1,0):F(1,12)}, {ZERO:F(1,3),(2,1):F(1,12)}]
    out = {}
    for j in range(3):
        scale = 1-command[j] if report==3 else (command[j] if j==report else 0)
        for b,v in k[j].items():
            out[b]=out.get(b,F(0))+scale*v
    return {b:v for b,v in out.items() if v}


def raw(p, m, theta, prior):
    Z=integral(p,theta,prior)
    return {b:integral(p,theta,prior,b)/Z for b in sums(A,m)}


def update(v, f, m):
    Z=sum(c*v[b] for b,c in f.items())
    if Z<F(1,24):
        raise AssertionError('positivity margin')
    return {b:sum(c*v[(b[0]+e[0],b[1]+e[1])] for e,c in f.items())/Z for b in sums(A,m-1)}


class IndexOnly:
    __slots__=('index',)
    def __init__(self): self.index=0
    def read(self, table, symbol): self.index=table[self.index][symbol]


def streaming_checks():
    commands=((F(1,4),F(1,2),F(3,4)),(F(2,3),F(1,3),F(1,2)))
    inputs=[report_factor(c,x) for c in commands for x in range(4)]
    exact_updates=0; fixtures=0
    for theta in (F(0), F(1,128), F(1,7), F(1,2)):
      for prior in (0,2):
       for M in (1,3,5):
        reps=[[raw({ZERO:F(1)},7,theta,prior)]]; tables=[]
        for stage in range(7):
            images=[[update(v,f,7-stage) for f in inputs] for v in reps[-1]]
            unique={tuple(v.items()):v for row in images for v in row}
            candidates=list(unique.values())
            next_reps=[candidates[j*len(candidates)//min(M,len(candidates))] for j in range(min(M,len(candidates)))]
            def nearest(v):
                return min(range(len(next_reps)),key=lambda j:sum((v[b]-next_reps[j][b])**2 for b in v))
            tables.append([[nearest(v) for v in row] for row in images]); reps.append(next_reps)
        rng=random.Random(20260906)
        for trial in range(16):
            machine=IndexOnly(); P={ZERO:F(1)}; v=raw(P,7,theta,prior)
            for stage in range(7):
                symbol=rng.randrange(len(inputs)); previous=machine.index
                machine.read(tables[stage],symbol)
                if machine.index != tables[stage][previous][symbol] or not 0<=machine.index<M:
                    raise AssertionError('persistent index transition')
                P=multiply(P,inputs[symbol]); truth=raw(P,6-stage,theta,prior)
                if update(v,inputs[symbol],7-stage)!=truth:
                    raise AssertionError('raw update disagrees with full-history reference')
                grouped={}
                for (a,b),value in truth.items():
                    x=a+theta*b
                    if x in grouped and grouped[x]!=value:
                        raise AssertionError('formal duplicate labels disagree')
                    grouped[x]=value
                if truth[ZERO]!=1:
                    raise AssertionError('normalization')
                v=truth; exact_updates+=1
        check(f'index-only-seven-theta{theta}-prior{prior}-M{M}',all(len(r)<=M for r in reps),state_counts=list(map(len,reps)))
        fixtures+=1
    DETAILS['index_only_fixtures']=fixtures
    DETAILS['exact_raw_update_comparisons']=exact_updates
    DETAILS['input_symbols']=len(inputs)
    DETAILS['implementation_persistent_fields']=['index']
    DETAILS['fixture_limitation']='Finite-input nonoptimal codebooks; exact histories exist only in the reference harness. No asymptotic rate is inferred.'


def main():
    flag_checks(); metric_checks(); profile_checks(); streaming_checks()
    receipt={'submission':'5d3d7e04b172f98bddfd037c488d93d516d20a98',
             'python':platform.python_version(),'sympy':sp.__version__,
             'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'checks_passed':len(CHECKS),'checks_total':len(CHECKS),'details':DETAILS,'checks':CHECKS,
             'limitations':['Finite diagnostics, not formal proof verification.','No author code imported.','Continuum entropy and all-prior lower bounds require the written proofs.']}
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_DIAGNOSTICS.json')
    out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='checks'},indent=2))

if __name__=='__main__':
    main()
