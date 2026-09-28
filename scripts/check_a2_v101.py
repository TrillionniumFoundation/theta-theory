#!/usr/bin/env python3
"""Finite exact diagnostics for A2 v101; not a verification of universal theorems.

The calibration example is the actual degree-two binary experiment:
f1=(z-1)^2, f2=(z-3)^2, D=4, five exterior clocks, and all five
stochastic/weight parameters unknown. No artificial cone is substituted.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sympy as sp
import mpmath as mp


def run() -> dict:
    R = sp.Rational
    alpha = R(1, 2)
    u = [sp.Matrix([R(3, 4), R(1, 4)]), sp.Matrix([R(1, 4), R(3, 4)])]
    v = [sp.Matrix([R(2, 3), R(1, 3)]), sp.Matrix([R(1, 3), R(2, 3)])]
    e = sp.Matrix([1, -1])
    clocks = list(range(5, 10))
    names = ['s1', 's2', 'alpha', 'u1', 'u2', 'v1', 'v2', 'X1', 'X2']
    scores = {name: [] for name in names}
    probabilities = []
    weights = []
    for z in clocks:
        f = [sp.Integer((z-1)**2), sp.Integer((z-3)**2)]
        C = [u[a]*v[a].T for a in (0, 1)]
        K = alpha*f[0]*C[0] + (1-alpha)*f[1]*C[1]
        q = alpha*f[0] + (1-alpha)*f[1]
        P = K/q
        probabilities.extend(list(P))
        weights.extend([R(1, 5)/p for p in P])
        for name in names:
            dK = sp.zeros(2)
            dq = sp.Integer(0)
            if name in ('s1', 's2', 'X1', 'X2'):
                a = int(name[-1])-1
                dp = -(z-(1 if a == 0 else 3)) if name[0] == 's' else -1
                dK = R(1, 2)*dp*C[a]
                dq = R(1, 2)*dp
            elif name == 'alpha':
                dK = f[0]*C[0]-f[1]*C[1]
                dq = f[0]-f[1]
            elif name[0] == 'u':
                a = int(name[-1])-1
                dK = R(1, 2)*f[a]*e*v[a].T
            else:
                a = int(name[-1])-1
                dK = R(1, 2)*f[a]*u[a]*e.T
            scores[name].extend(list((dK-P*dq)/q))
    S = sp.Matrix.hstack(*(sp.Matrix(scores[name]) for name in names))
    W = sp.diag(*weights)
    L, D = S[:, :7], S[:, 7:]
    H = L.T*W*L
    optimal = -H.inv()*L.T*W*D
    Q = sp.simplify(D.T*W*D-D.T*W*L*H.inv()*L.T*W*D)
    assert S.rank() == 9 and L.rank() == 7
    assert Q[0, 0] > 0 and Q.det() > 0
    probes = [sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([1, 1])]
    costs = [(z.T*Q*z)[0] for z in probes]
    recovered = sp.Matrix([[costs[0], (costs[2]-costs[0]-costs[1])/2],
                           [(costs[2]-costs[0]-costs[1])/2, costs[1]]])
    assert recovered == Q
    assert sp.simplify(L.T*W*(L*optimal+D)) == sp.zeros(7, 2)
    mp.mp.dps = 90
    to_mp = lambda x: mp.mpf(str(sp.numer(x)))/mp.mpf(str(sp.denom(x)))
    base = [to_mp(p) for p in probabilities]
    trials = []
    for probe, cost in zip(probes, costs):
        free = [to_mp(x) for x in optimal*probe]
        # This scale keeps every unknown stochastic coordinate strictly feasible.
        scale = mp.mpf('0.01')/(1+max(abs(x) for x in free))
        errors, rows = [], []
        for power in (2, 3, 4, 5):
            t = scale*mp.power(10, -power)
            a = mp.mpf('0.5')+t*free[2]
            U = [[mp.mpf('0.75')+t*free[3], mp.mpf('0.25')+t*free[4]],
                 [mp.mpf('0.25')-t*free[3], mp.mpf('0.75')-t*free[4]]]
            V = [[mp.mpf(2)/3+t*free[5], mp.mpf(1)/3+t*free[6]],
                 [mp.mpf(1)/3-t*free[5], mp.mpf(2)/3-t*free[6]]]
            assert mp.mpf('0.1') < a < mp.mpf('0.9')
            assert all(0 < x < 1 for M in (U, V) for row in M for x in row)
            for j, centre in enumerate((1, 3)):
                roots = [centre+t*free[j]/2-sign*mp.sqrt(t*int(probe[j])) for sign in (-1, 1)]
                assert all(0 < r < 4 for r in roots)
            out = []
            for z in clocks:
                f = [(z-r-t*free[j]/2)**2-t*int(probe[j]) for j, r in enumerate((1, 3))]
                q = a*f[0]+(1-a)*f[1]
                for i in (0, 1):
                    for j in (0, 1):
                        out.append((a*f[0]*U[i][0]*V[j][0]+(1-a)*f[1]*U[i][1]*V[j][1])/q)
            h2 = sum((mp.sqrt(x)-mp.sqrt(y))**2 for x, y in zip(out, base))/5
            measured = 4*h2/t**2
            error = abs(measured/to_mp(cost)-1)
            errors.append(error)
            rows.append({'t': mp.nstr(t, 16), 'scaled_recovery_curve_cost': mp.nstr(measured, 24),
                         'relative_error_to_Q': mp.nstr(error, 12)})
        assert all(errors[i+1] < errors[i] for i in range(len(errors)-1))
        assert errors[-1] < mp.mpf('1e-4')
        trials.append({'probe': [int(x) for x in probe], 'exact_limit': str(cost), 'trials': rows})
    # The chart following the existing singular contact example is exact.
    uvar, zvar = sp.symbols('u z')
    contacts = []
    for m, n in ((2, 3), (3, 5), (1, 2)):
        delta = uvar**m-uvar**n*zvar
        assert sp.expand((uvar**m-delta)-uvar**n*zvar) == 0
        assert sp.expand(delta-uvar**m*(1-uvar**(n-m)*zvar)) == 0
        contacts.append({'m': m, 'n': n, 'residual_to_time_ratio': str(R(n, m))})
    return {
        'status': 'passed',
        'scope': 'finite exact arithmetic and feasible recovery curves, not universal proof verification',
        'model': {'degree': 2, 'D': 4, 'clocks': clocks, 'clock_weights': '1/5',
                  'f1': '(z-1)^2', 'f2': '(z-3)^2', 'unknown_free_parameters': names[:7]},
        'score_rank': 9, 'free_score_rank': 7,
        'profile_Q': [[str(x) for x in Q.row(i)] for i in range(2)],
        'profile_determinant': str(Q.det()),
        'finite_probe_reconstruction_exact': True,
        'first_order_profile_orthogonality_exact': True,
        'recovery_curves': trials,
        'divisorial_chart_checks': contacts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('revisions/a2-v101/EXACT_DIAGNOSTICS.json'))
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': result['status'], 'output': str(args.output), 'score_rank': result['score_rank']}))


if __name__ == '__main__':
    main()
