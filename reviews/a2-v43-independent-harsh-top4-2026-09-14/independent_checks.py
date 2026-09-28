#!/usr/bin/env python3
"""Independent finite diagnostics for A2 v43. Not a proof certificate.
Run: python3 independent_checks.py > RESULTS.json
Dependencies: Python 3, NumPy, SciPy, Git. No network or manuscript imports.
"""
from __future__ import annotations
import json
import math
import platform
import subprocess
import tempfile
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import solve_banded


def require(test: bool, message: str) -> None:
    if not test:
        raise RuntimeError(message)


def rational_inverse() -> dict:
    def S(x):
        x = F(x)
        return x*x/2+x**3/7+x**4/5
    def B(x):
        x = F(x)
        return 1+x/3+x*x/4
    points = [F(i, 30) for i in range(-9, 10)]
    anchors = [F(-1, 5), F(1, 6), F(1, 4)]
    pairs = recoveries = 0
    for d in [F(1), F(3, 2), F(2)]:
        def f(x, y):
            return B(x)*B(y)*(d-S(x)-S(y))/F(13, 7)
        def R(x, y):
            return f(x, y)*f(0, 0)/(f(x, 0)*f(0, y))
        for x in points:
            for y in points:
                require(1-R(x, y) == S(x)*S(y)/((d-S(x))*(d-S(y))),
                        'rational rank-one defect')
                pairs += 1
        for a in anchors:
            t_a = S(a)/(d-S(a))
            require(t_a > 0 and t_a*t_a == 1-R(a, a), 'positive anchor')
            for x in points:
                t = (1-R(x, a))/t_a
                require(d*t/(1+t) == S(x), 'action recovery')
                require(f(x, 0)*(1+t)/f(0, 0) == B(x)/B(0), 'amplitude recovery')
                recoveries += 1
    return dict(pair_identities=pairs, action_amplitude_recoveries=recoveries,
                odd_action_terms=True, unknown_nonconstant_amplitude=True)


# Local flight model with unequal positive curvatures and nonzero cubic jets.
GAP = 0.8
KAPPA = np.array([0.65, 1.15])
Q3 = np.array([0.21, -0.16])
Q4 = np.array([0.35, 0.27])


def flight_data(x: np.ndarray, start: int):
    types = (np.arange(len(x))+start) % 2
    k, q3, q4 = KAPPA[types], Q3[types], Q4[types]
    psi = k*x*x/2+q3*x**3/6+q4*x**4/24
    dp = k*x+q3*x*x/2+q4*x**3/6
    ddp = k+q3*x+q4*x*x/2
    h = GAP+psi[:-1]+psi[1:]
    z = x[1:]-x[:-1]
    length = np.hypot(h, z)
    p, q = dp[:-1], dp[1:]
    al, ar = h*p-z, h*q+z
    gl, gr = al/length, ar/length
    hl = (p*p+1+h*ddp[:-1])/length-al*al/length**3
    hr = (q*q+1+h*ddp[1:])/length-ar*ar/length**3
    off = (p*q-1)/length-al*ar/length**3
    grad = np.r_[gl[0], gr[:-1]+gl[1:], gr[-1]]
    diag = np.r_[hl[0], hr[:-1]+hl[1:], hr[-1]]
    return length, h, grad, diag, off


def band(diag, off):
    a = np.zeros((3, len(diag)))
    a[1] = diag
    a[0, 1:] = off
    a[2, :-1] = off
    return a


def stationary(n: int, start: int, u: float, v: float):
    x = np.zeros(n+1)
    x[0], x[-1] = u, v
    for _ in range(25):
        length, h, grad, diag, off = flight_data(x, start)
        residual = float(np.max(np.abs(grad[1:-1])))
        if residual < 2e-15:
            break
        step = solve_banded((1, 1), band(diag[1:-1], off[1:-1]), grad[1:-1])
        x[1:-1] -= step
    require(residual < 2e-13, 'stationary solve did not converge')
    require(np.all(-off > 0), 'positive twist factors')
    pivots = diag[1:-1].copy()
    for i in range(1, len(pivots)):
        pivots[i] -= off[i]*off[i]/pivots[i-1]
    require(np.all(pivots > 0), 'positive interior Hessian')
    logtwist = float(np.sum(np.log(-off))-np.sum(np.log(pivots)))
    return x, length, h, residual, diag, off, logtwist


def nonlinear_bridges() -> dict:
    cofactor_errors, interaction, residuals = [], [], []
    solves = 0
    for start in (0, 1):
        for u, v in [(0.13, -0.09), (-0.11, 0.07)]:
            for n in (4, 8, 12, 20, 32, 48):
                values = []
                for a, b in ((u, v), (u, 0.), (0., v), (0., 0.)):
                    x, ell, h, res, diag, off, logt = stationary(n, start, a, b)
                    solves += 1
                    residuals.append(res)
                    values.append(logt)
                    # Independent Schur elimination, compared in relative error.
                    rhs = np.zeros(n-1)
                    rhs[-1] = off[-1]
                    sol = solve_banded((1, 1), band(diag[1:-1], off[1:-1]), rhs)
                    schur_twist = off[0]*sol[0]
                    cofactor_errors.append(abs(schur_twist/math.exp(logt)-1))
                # log b(u,v)-log b(u,0)-log b(0,v); zero base cancels once.
                interaction.append(dict(start=start, u=u, v=v, flights=n,
                                        log_factorization_defect=values[0]-values[1]-values[2]+values[3]))
    max_error = max(cofactor_errors)
    require(max_error < 2e-12, 'relative Schur/cofactor identity')
    final_defect = max(abs(r['log_factorization_defect']) for r in interaction if r['flights']==48)
    require(final_defect < 2e-11, 'finite endpoint factorization diagnostic')
    return dict(stationary_solves=solves, maximum_stationarity_residual=max(residuals),
                maximum_relative_schur_cofactor_error=max_error,
                maximum_48_flight_log_factorization_defect=final_defect,
                factorization_records=interaction)


def sixth_jet_envelope() -> dict:
    c = 1+GAP*KAPPA
    gamma = math.acosh(math.sqrt(float(c[0]*c[1])))
    errors, records = [], []
    solves = 0
    for start in (0, 1):
        for varied in (0, 1):
            expected = (1/math.tanh(6*gamma) if varied==start else
                        (math.sqrt(c[start]/c[1-start])**6)/math.sinh(6*gamma))
            for u in (0.08, 0.04, 0.02, 0.01):
                estimates = []
                for endpoint in (u, -u):
                    x, length, h, residual, *_ = stationary(60, start, endpoint, 0.)
                    solves += 1
                    types = (np.arange(len(x))+start) % 2
                    # Exact finite-envelope variation for psi_varied += theta*y^6/6!.
                    powers = np.where(types==varied, x**6, 0.)
                    estimate = float(np.sum((h/length)*(powers[:-1]+powers[1:]))/endpoint**6)
                    estimates.append(estimate)
                estimate = sum(estimates)/2
                error = abs(estimate-expected)
                records.append(dict(start=start, varied=varied, endpoint=u,
                                    symmetric_envelope_coefficient=estimate,
                                    predicted_coefficient=expected, absolute_error=error))
                if u==0.01:
                    errors.append(error)
    require(max(errors) < 5e-5, 'sixth-jet finite envelope diagnostic')
    return dict(stationary_solves=solves, flights=60,
                maximum_smallest_endpoint_error=max(errors), records=records,
                scope='Finite stationary envelope; not an infinite-half-line proof')


def git_retention_control() -> dict:
    ignore = ('*.aux\n*.bbl\n*.bcf\n*.blg\n*.fdb_latexmk\n*.fls\n*.log\n*.out\n'
              '*.run.xml\n*.toc\n*.synctex.gz\n*.pdf\n__pycache__/\n*.py[cod]\n')
    names = ['main'+suffix for suffix in ('.aux','.fdb_latexmk','.fls','.log','.out','.pdf','.toc')]
    names += ['two_collision'+suffix for suffix in ('.aux','.fdb_latexmk','.fls','.log','.out','.pdf')]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        def git(*args):
            return subprocess.check_output(['git', '-C', tmp, *args], text=True, stderr=subprocess.DEVNULL)
        git('init', '-q')
        (root/'.gitignore').write_text(ignore)
        dest = root/'deliveries'/'test'
        dest.mkdir(parents=True)
        for name in names+['build-report.json', 'README.md']:
            (dest/name).write_text('synthetic retention regression fixture\n')
        git('add', '--', 'deliveries/test')
        tracked = git('ls-files').splitlines()
        require(len(tracked)==2, 'ordinary git add must reproduce ignore omission')
        git('add', '-f', '--', 'deliveries/test')
        forced = git('ls-files').splitlines()
        require(len(forced)==15, 'explicit force adds fixture products')
    return dict(promised_ignored_native_names=names, omitted_by_plain_add=len(names),
                plain_add_tracked=len(tracked), explicit_force_tracked=len(forced),
                scope='Temporary local Git repository; no change to author repository')


def main() -> None:
    out = dict(review='A2-v43-independent-harsh-top4-2026-09-14',
               python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
               rational_inverse=rational_inverse(), nonlinear_bridges=nonlinear_bridges(),
               sixth_jet_envelope=sixth_jet_envelope(), git_retention_control=git_retention_control(),
               status='passed', mathematical_certification=False)
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
