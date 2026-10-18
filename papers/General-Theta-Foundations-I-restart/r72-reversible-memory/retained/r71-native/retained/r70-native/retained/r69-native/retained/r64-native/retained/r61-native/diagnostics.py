#!/usr/bin/env python3
"""Finite diagnostics only: exact rational checks and separate floating probes.
No assert statements: normal and python -O must execute the same checks.
"""
from __future__ import annotations
import hashlib, itertools, json, math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize_scalar
import sympy as sp

COUNTS: dict[str, int] = {}
MAX_RESIDUAL = 0.0

def check(ok: bool, group: str, detail: str) -> None:
    if not bool(ok):
        raise RuntimeError(f'{group}: {detail}')
    COUNTS[group] = COUNTS.get(group, 0) + 1

def exact_checks() -> None:
    # Fractional selection, including tied thresholds and b=1.
    for n in range(2, 9):
        weights = [F(i + 1, n * (n + 1) // 2) for i in range(n)]
        losses = [F((i * 5) % 7, 7) for i in range(n)]
        for b in [F(1), F(4, 3), F(2), F(3), F(7)]:
            remaining, primal = F(1), F(0)
            for i in sorted(range(n), key=lambda i: losses[i]):
                mass = min(remaining, b * weights[i])
                primal += mass * losses[i]; remaining -= mass
            dual = max(t - b * sum(w * max(F(0), t - d)
                                     for w, d in zip(weights, losses))
                       for t in set(losses + [F(0), F(1)]))
            check(remaining == 0 and primal == dual, 'exact_selection_dual', str((n, b)))
    # Exhaust all finite atom dictionaries, not a numerical continuous optimizer.
    for n in range(2, 9):
        masses = [F(i + 1, n * (n + 1) // 2) for i in range(n)]
        for m in range(1, n + 1):
            maximum = max(sum(masses[i] for i in C)
                          for C in itertools.combinations(range(n), m))
            check(maximum == sum(sorted(masses, reverse=True)[:m]),
                  'exact_zero_spectrum', str((n, m)))
            check((F(1, 1) / maximum) * maximum == 1,
                  'exact_zero_threshold', str((n, m)))
    check(F(1, 4) * 1 < 1 and F(1, 4) + F(3, 4) == 1,
          'exact_old_atom_counterexample', 'two zero atoms at width two and b=1')
    I = sp.eye(2); Z = sp.diag(1, -1); X = sp.Matrix([[0, 1], [1, 0]])
    R = [lambda A: sp.trace(A) * sp.diag(1, 0) / 2,
         lambda A: sp.trace(A) * sp.diag(0, 1) / 2]
    rho = I / 2
    cols = [sp.Matrix(A).reshape(4, 1) for A in [rho, R[0](rho), R[1](rho)]]
    check(sp.Matrix.hstack(*cols).rank() == 2, 'exact_report_span', 'resolved rank')
    check(R[0](rho) + R[1](rho) == rho, 'exact_report_span', 'pooled fixed state')
    check(sp.trace(Z * rho) == 0 and sp.trace(Z * R[0](rho)) != 0,
          'exact_report_span', 'pooled calibration is insufficient')
    check(all(sp.trace(X * A) == 0 for A in [rho, R[0](rho), R[1](rho)]) and X != sp.zeros(2),
          'exact_report_span', 'full support identity is unnecessarily strong')
    T = sp.diag(0, 1); seed = sp.Matrix([1, 0]); P = sp.diag(1, 0)
    check(T * seed == sp.zeros(2, 1) and max(T.eigenvals()) == 1,
          'exact_reachable_support', 'unreachable recurrent block')
    check(P * T * P == sp.zeros(2), 'exact_reachable_support', 'restricted transience')
    for b in [F(3, 2), F(2), F(5)]:
        for cutoff in [1, 3, 8]:
            K = max(2 * cutoff + 2, int(b) + 2)
            prob = (b - 1) / (K - 1)
            mean = 1 + prob * (K - 1)
            check(mean == b and prob <= (b - 1) / cutoff,
                  'exact_survival_tail', str((b, cutoff)))
    # Exact barycentric witness for the sharp physical continuation depth.
    for d in [2, 3, 4]:
        q = d*d-1
        nodes = [F(1)] + [F(i, 2*d*q*(q+1)) for i in range(1, q+1)]
        weights = [F(1) / math.prod(x-y for j,y in enumerate(nodes) if j != i)
                   for i,x in enumerate(nodes)]
        check(sum(nodes[1:]) == F(1,4*d), 'exact_sharp_depth_cp_margin', str(d))
        check(F(1,d) - q*F(1,2*d*q) == F(1,2*d),
              'exact_sharp_depth_preparation', str(d))
        for n in range(q+1):
            actual = sum(w*x**n for w,x in zip(weights,nodes))
            check(actual == (1 if n == q else 0), 'exact_sharp_depth_moments', str((d,n)))
    # Exact Bellman solution by enumerating every stationary selector, not value iteration.
    vectors = [sp.Matrix([1, 0]), sp.Matrix([3, 4]), sp.Matrix([4, -3])]
    states = [u * u.T / (u.dot(u)) for u in vectors]
    states[2] = (states[2] + sp.eye(2) / 2) / 2  # a genuinely mixed reset
    for case in range(12):
        effects = [[sp.Rational(1 + ((case + a + j) % 3), 18) * states[(a + j) % 3]
                    for j in range(3)] for a in range(3)]
        G = [sp.diag(sp.Rational(2 + a, 2), sp.Rational(3 + ((case + a) % 3), 3))
             for a in range(3)]
        Q = [[[sp.trace(E * state) for E in effects[a]] for a in range(3)]
             for state in states]
        c = [[sp.trace(Ga * state) for Ga in G] for state in states]
        values = []
        for alpha in itertools.product(range(3), repeat=3):
            mat = sp.Matrix([Q[i][alpha[i]] for i in range(3)])
            vec = (sp.eye(3) - mat).inv() * sp.Matrix([c[i][alpha[i]] for i in range(3)])
            values.append((alpha, vec))
        v = sp.Matrix([min(vec[i] for _, vec in values) for i in range(3)])
        check(any(vec == v for _, vec in values), 'exact_reset_bellman', f'common selector {case}')
        for i in range(3):
            options = [c[i][a] + sum(Q[i][a][j] * v[j] for j in range(3)) for a in range(3)]
            check(v[i] == min(options), 'exact_reset_bellman', str((case, i)))
        # Exact matrix continuation identity from the raw reset maps.
        alpha = next(a for a, vec in values if vec == v)
        H = [G[a] + sum((v[j] * effects[a][j] for j in range(3)), sp.zeros(2)) for a in alpha]
        for i in range(3):
            rhs = G[alpha[i]] + sum((sp.trace(H[j] * states[j]) * effects[alpha[i]][j]
                                     for j in range(3)), sp.zeros(2))
            check(H[i] == rhs and sp.trace(H[i] * states[i]) == v[i],
                  'exact_reset_raw_instrument', str((case, i)))
    # Rank-one pair: exact unequal-cost Bellman values by both equations.
    q = sp.Rational(9, 25); ka, kb = sp.Rational(2), sp.Rational(3)
    va = (kb + q * ka) / (1 - q*q); vb = (ka + q * kb) / (1 - q*q)
    # Alternation need not be optimal with unequal costs. Verify only its equations.
    check(va == kb + q * vb and vb == ka + q * va,
          'exact_alternating_cost_identity', 'no false optimality assertion')

def controller_cost(cosine: float, rows: np.ndarray, transition: np.ndarray) -> float:
    """Independent raw completely-positive killed-map solve, 2 labels x 2x2 matrices."""
    u = np.array([1.0, 0.0]); v = np.array([cosine, math.sqrt(1-cosine*cosine)])
    projectors = [np.outer(u, u), np.outer(v, v)]
    T = np.zeros((8, 8))
    for s in range(2):
        for a in range(2):
            for t in range(2):
                T[4*t:4*t+4, 4*s:4*s+4] += rows[s, a] * transition[s, a, t] * np.kron(projectors[a], projectors[a])
    cost = np.tile(np.eye(2).reshape(-1), 2)
    H = np.linalg.solve(np.eye(8)-T.T, cost)
    H0 = H[:4].reshape(2,2)
    return float(np.linalg.eigvalsh((H0+H0.T)/2)[-1])

def floating_checks() -> None:
    global MAX_RESIDUAL
    rng = np.random.default_rng(61015)
    for c in [0.0, 0.1, 0.3, 0.6, 0.78, 0.8, 0.9, 0.97]:
        q = c*c
        def formula(r: float) -> float:
            a, b = r+q, (1-r)*(1/r+q)
            return 1+(a+b+math.sqrt((a-b)**2+4*q*a*b))/(2*(1-q*q))
        opt = minimize_scalar(formula, bounds=(1e-7, 1.0), method='bounded', options={'xatol':1e-13})
        r = 1.0 if formula(1.0) <= opt.fun else float(opt.x)
        closed = formula(r)
        transition = np.zeros((2,2,2)); transition[:,0,1]=1; transition[:,1,0]=1
        rows = np.array([[r, 1-r], [0., 1.]])
        raw = controller_cost(c, rows, transition)
        error = abs(raw-closed); MAX_RESIDUAL=max(MAX_RESIDUAL,error)
        check(error < 1e-8, 'float_two_label_raw_match', str(c))
        unrestricted = 1+1/(2*(1-c))
        check(closed > unrestricted + 1e-7, 'float_two_label_strict_gap', str(c))
        if q >= (math.sqrt(5)-1)/2:
            check(r == 1.0, 'float_transition_boundary', str(c))
        for _ in range(16):
            rr = rng.dirichlet([1,1],size=2)
            tt = rng.dirichlet([1,1],size=(2,2))
            val = controller_cost(c,rr,tt)
            check(val+1e-8 >= closed, 'float_arbitrary_two_label_probe', str(c))

if __name__ == '__main__':
    exact_checks(); floating_checks()
    out = {'status':'PASS','schema':'theta.r61.finite-diagnostics.v1',
           'checks_by_group':COUNTS,'total_checks':sum(COUNTS.values()),
           'maximum_floating_raw_formula_residual':MAX_RESIDUAL,
           'seed':61015,'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,
           'scope':'Finite examples only; exact rational and floating checks separated. Not formal proof, human referee approval, priority certification, or journal acceptance.'}
    print(json.dumps(out,sort_keys=True,indent=2))
