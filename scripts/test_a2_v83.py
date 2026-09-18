#!/usr/bin/env python3
"""Deterministic regression checks for A2 v83; not a proof certificate.

Run: python scripts/test_a2_v83.py --output revisions/a2-v83/checks.json
Requires NumPy, SciPy and SymPy. No network or repository writes occur.
"""
from __future__ import annotations
import argparse
import itertools
import json
import sys
import time
import unittest
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq, linear_sum_assignment, root


def divided_difference(nodes: np.ndarray, values: np.ndarray) -> float:
    nodes, values = np.asarray(nodes, float), np.asarray(values, float)
    if nodes.ndim != 1 or nodes.size != values.size or np.unique(nodes).size != nodes.size:
        raise ValueError('Distinct one-dimensional nodes and equally sized values are required')
    return float(sum(values[i] / np.prod(nodes[i] - np.delete(nodes, i)) for i in range(len(nodes))))


def scalar_values(t: np.ndarray, coefficients: np.ndarray, x: float, y: float) -> np.ndarray:
    if max(x, y) >= min(t):
        raise ValueError('Actions must precede the first deadline')
    return np.polynomial.polynomial.polyval(t, coefficients) + np.log(t - x) - np.log(t - y)


def interval_inverse(t: np.ndarray, values: np.ndarray, bounds: tuple[float, float]) -> tuple[float, float]:
    """Global bracketed scalar inverse on a prescribed action interval."""
    q = len(t) - 3
    if q < 0:
        raise ValueError('At least three clocks are required')
    lo, hi = bounds
    if not lo < hi < t[0]:
        raise ValueError('Invalid action interval')
    d0 = (-1.) ** (q + 2) * divided_difference(t[:-1], values[:-1])
    d1 = (-1.) ** (q + 2) * divided_difference(t[1:], values[1:])
    if abs(d0) < 1e-13:
        raise ValueError('No separated anchor at this precision')
    sign = 1 if d0 > 0 else -1
    d0, d1 = sign * d0, sign * d1
    w0 = lambda s: 1. / np.prod(t[:-1] - s)
    w1 = lambda s: 1. / np.prod(t[1:] - s)
    def integral(fun, a, b):
        return quad(fun, a, b, epsabs=1e-13, epsrel=2e-12)[0]
    Fmax = integral(w0, lo, hi)
    def Finv(u):
        if abs(u) < 1e-15:
            return lo
        if abs(u - Fmax) < 1e-15:
            return hi
        return brentq(lambda s: integral(w0, lo, s) - u, lo, hi, xtol=1e-13)
    def residual(u):
        return integral(w1, Finv(u), Finv(u + d0)) - d1
    u = brentq(residual, 0., Fmax - d0, xtol=1e-13)
    y, x = Finv(u), Finv(u + d0)
    return (x, y) if sign == 1 else (y, x)


def latent_data(t, actions, logweights, theta, U, V):
    logs = np.asarray(logweights)[None, :] + np.log(t[:, None] - actions[None, :])
    for k in range(theta.shape[1]):
        logs += t[:, None] ** (k + 1) * theta[None, :, k]
    logs -= logs.max(axis=1)[:, None]
    pi = np.exp(logs)
    pi /= pi.sum(axis=1)[:, None]
    return np.array([(U * p) @ V.T for p in pi]), pi


def spectral_components(P, q, rows, cols, tchoice=None):
    B = len(rows)
    H = P[0][np.ix_(rows, cols)]
    inv = np.linalg.inv(H)
    K = [P[j][np.ix_(rows, cols)] @ inv for j in range(1, q + 2)]
    L = B * (B - 1) // 2
    candidates = [0] if q == 0 else list(range(q * L + 1))
    if tchoice is not None:
        candidates = [tchoice]
    best = None
    for a in candidates:
        A = sum(a ** l * K[l] for l in range(q + 1))
        eig, S = np.linalg.eig(A)
        if np.max(abs(eig.imag)) > 1e-8:
            continue
        gap = min(abs(eig[b] - eig[c]) for b in range(B) for c in range(b))
        if best is None or gap > best[0]:
            best = gap, eig.real, S.real, a
    if best is None or best[0] < 1e-10:
        raise ValueError('No separated real spectrum')
    _, eig, S, choice = best
    Sinv = np.linalg.inv(S)
    E = np.zeros((len(P), B, *P.shape[1:]))
    left = P[0][:, cols] @ inv
    for b in range(B):
        R = np.outer(S[:, b], Sinv[b, :])
        for j in range(len(P)):
            E[j, b] = left @ R @ P[j][rows, :]
    pi = E.sum(axis=(2, 3))
    U = (E[0].sum(axis=2) / pi[0, :, None]).T
    V = (E[0].sum(axis=1) / pi[0, :, None]).T
    return U, V, pi, E, choice


def align(U, target):
    costs = np.linalg.norm(U[:, :, None] - target[:, None, :], axis=0)
    left, right = linear_sum_assignment(costs)
    order = np.empty(U.shape[1], dtype=int)
    order[right] = left
    return order


class Revision83Checks(unittest.TestCase):
    def test_01_cauchy_divided_differences(self):
        s = sp.symbols('s')
        for n in range(1, 7):
            nodes = [sp.Integer(2 * j + 1) for j in range(n + 1)]
            lhs = sum(1 / ((t - s) * sp.prod(t - u for u in nodes if u != t)) for t in nodes)
            rhs = (-1) ** n / sp.prod(t - s for t in nodes)
            self.assertEqual(sp.factor(lhs - rhs), 0)

    def test_02_ratio_and_jacobian(self):
        s, first, last = sp.symbols('s first last')
        self.assertEqual(sp.factor(sp.diff((first - s) / (last - s), s) - (first - last) / (last - s) ** 2), 0)
        wx, wy, rx, ry = sp.symbols('wx wy rx ry')
        M = sp.Matrix([[wx, -wy], [wx * rx, -wy * ry]])
        self.assertEqual(sp.factor(M.det() - wx * wy * (rx - ry)), 0)

    def test_03_sharp_global_interval_recovery(self):
        for q in range(4):
            t = np.linspace(1., 2.8, q + 3)
            c = np.array([.13 * (-.4) ** k for k in range(q + 1)])
            for x, y in [(-.3, -1.7), (-2.4, -.7), (.15, -1.2)]:
                got = interval_inverse(t, scalar_values(t, c, x, y), (-3., .35))
                np.testing.assert_allclose(got, [x, y], atol=3e-7, rtol=0)

    def test_04_contrast_integral_identity(self):
        for q in range(5):
            t = np.linspace(1., 3., q + 3)
            f = scalar_values(t, np.zeros(q + 1), -.2, -1.1)
            d = (-1.) ** (q + 2) * divided_difference(t[:-1], f[:-1])
            exact = quad(lambda s: 1 / np.prod(t[:-1] - s), -1.1, -.2, epsabs=1e-13)[0]
            self.assertAlmostEqual(d, exact, delta=1e-11)

    def test_05_q_plus_2_action_changing_ambiguity(self):
        for q in range(4):
            t = np.linspace(1., 2.2, q + 2)
            c = np.linspace(.1, -.03, q + 1)
            x, y = -.4, -1.5
            target = scalar_values(t, c, x, y)
            y2 = y + .002
            result = root(lambda z: scalar_values(t, z[:-1], z[-1], y2) - target, np.r_[c, x], tol=1e-11)
            self.assertLess(np.max(abs(result.fun)), 1e-10)
            self.assertGreater(abs(y2 - y), .001)
            self.assertLess(max(result.x[-1], y2), t[0])
            p1 = 1 / (1 + np.exp(-target))
            p2 = 1 / (1 + np.exp(-scalar_values(t, result.x[:-1], result.x[-1], y2)))
            np.testing.assert_allclose(p1, p2, atol=1e-11)

    def test_06_full_scalar_jacobians(self):
        for q in range(5):
            t = np.linspace(1., 3., q + 3)
            J = np.column_stack([t ** k for k in range(q + 1)] + [-1 / (t + .3), 1 / (t + 1.4)])
            self.assertEqual(np.linalg.matrix_rank(J, tol=1e-11), q + 3)

    @staticmethod
    def model():
        U = np.array([[.55, .12, .1], [.1, .5, .15], [.2, .13, .5], [.15, .25, .25]])
        V = np.array([[.45, .08, .1], [.1, .45, .07], [.08, .1, .45], [.2, .2, .18], [.17, .17, .2]])
        t = np.array([1., 1.4, 1.9, 2.5])
        W = np.array([-.3, -1.2, -.3])  # A genuine action coincidence.
        theta = np.array([[-.12], [.18], [.45]])
        a = np.array([.12, -.2, .08])
        P, pi = latent_data(t, W, a, theta, U, V)
        return t, W, theta, a, U, V, P, pi

    def test_07_spectral_recovery_at_action_coincidence(self):
        t, W, theta, a, U, V, P, pi = self.model()
        Uh, Vh, ph, E, _ = spectral_components(P, 1, [0, 1, 2], [0, 1, 2])
        order = align(Uh, U)
        np.testing.assert_allclose(Uh[:, order], U, atol=2e-10)
        np.testing.assert_allclose(Vh[:, order], V, atol=2e-10)
        np.testing.assert_allclose(ph[:, order], pi, atol=2e-10)
        np.testing.assert_allclose(E.sum(axis=1), P, atol=2e-10)

    def test_08_minor_and_separator_independence(self):
        _, _, _, _, U, V, P, pi = self.model()
        for rows, cols, a in [([0, 1, 2], [0, 1, 2], 0), ([0, 2, 3], [1, 2, 4], 1), ([0, 1, 3], [0, 3, 4], 3)]:
            Uh, Vh, ph, _, _ = spectral_components(P, 1, rows, cols, a)
            order = align(Uh, U)
            np.testing.assert_allclose(Uh[:, order], U, atol=2e-9)
            np.testing.assert_allclose(Vh[:, order], V, atol=2e-9)
            np.testing.assert_allclose(ph[:, order], pi, atol=2e-9)

    def test_09_common_gauge_invariance(self):
        t, W, theta, a, U, V, P, _ = self.model()
        Pg, _ = latent_data(t, W, a + 2.4, theta + 1.7, U, V)
        np.testing.assert_allclose(Pg, P, atol=1e-14)
        np.testing.assert_allclose((a + 2.4) - np.mean(a + 2.4), a - np.mean(a), atol=1e-14)

    def test_10_noisy_overlap_matching_cocycle(self):
        _, _, _, _, U, _, _, _ = self.model()
        rng = np.random.default_rng(83)
        perms = [np.array([0, 1, 2]), np.array([2, 0, 1]), np.array([1, 2, 0])]
        noisy = [U[:, p] + 1e-5 * rng.normal(size=U.shape) for p in perms]
        trans = {(a, b): align(noisy[b], noisy[a]) for a in range(3) for b in range(3)}
        for a, b, c in itertools.product(range(3), repeat=3):
            np.testing.assert_array_equal(trans[b, c][trans[a, b]], trans[a, c])
        weights = [.2, .3, .5]
        glued = [sum(weights[b] * noisy[b][:, trans[a, b]] for b in range(3)) for a in range(3)]
        for a, b in itertools.product(range(3), repeat=2):
            np.testing.assert_allclose(glued[b][:, trans[a, b]], glued[a], atol=1e-14)

    def test_11_off_model_local_error_scaling(self):
        _, _, _, _, U, _, P, _ = self.model()
        rng = np.random.default_rng(123)
        noise = rng.normal(size=P.shape)
        errors = []
        for eps in [1e-7, 5e-8, 2.5e-8]:
            Uh, _, _, _, _ = spectral_components(P + eps * noise, 1, [0, 1, 2], [0, 1, 2], 1)
            errors.append(np.linalg.norm(Uh[:, align(Uh, U)] - U))
        self.assertTrue(1.95 < errors[0] / errors[1] < 2.05)
        self.assertTrue(1.95 < errors[1] / errors[2] < 2.05)

    def test_12_rank_threshold(self):
        _, _, _, _, _, _, P, _ = self.model()
        sigma = np.linalg.svd(P[0], compute_uv=False)[2]
        rng = np.random.default_rng(5)
        perturb = rng.normal(size=P[0].shape)
        perturb *= sigma / (8 * np.linalg.norm(perturb, 2))
        s = np.linalg.svd(P[0] + perturb, compute_uv=False)
        self.assertEqual(np.count_nonzero(s > sigma / 2), 3)

    def test_13_one_view_exact_counterexample(self):
        T = sp.symbols('T')
        U = sp.Matrix([[sp.Rational(1, 5), sp.Rational(4, 5)], [sp.Rational(4, 5), sp.Rational(1, 5)]])
        V = sp.Matrix([[sp.Rational(2, 5), sp.Rational(3, 5)], [sp.Rational(3, 5), sp.Rational(2, 5)]])
        self.assertEqual(U * sp.Matrix([T, T - 1]), V * sp.Matrix([T + 1, T - 2]))
        self.assertNotEqual(U.det(), 0)
        self.assertNotEqual(V.det(), 0)

    def test_14_monodromy_three_cycle(self):
        e = np.array([1., -1., 0.]) / np.sqrt(2)
        f = np.array([1., 1., -2.]) / np.sqrt(6)
        ts = np.array([1., 1.5, 2., 2.5])
        endpoints = []
        for z in np.linspace(0., 2 * np.pi, 41):
            phi = z / 3 + 2 * np.pi * np.arange(3) / 3
            U = np.ones((3, 3)) / 3 + .08 * (e[:, None] * np.cos(phi) + f[:, None] * np.sin(phi))
            W = -3 + np.cos(phi)
            theta = np.sin(phi)[:, None]
            P, _ = latent_data(ts, W, np.zeros(3), theta, U, U)
            self.assertGreater(U.min(), 0)
            self.assertGreater(np.linalg.svd(U, compute_uv=False)[-1], .08)
            self.assertGreater(np.ptp(W), 1.4)
            endpoints.append((U, P))
        np.testing.assert_allclose(endpoints[-1][0], endpoints[0][0][:, [1, 2, 0]], atol=1e-14)
        np.testing.assert_allclose(endpoints[-1][1], endpoints[0][1], atol=1e-14)

    def test_15_shear_exactness_and_roof(self):
        p = sp.symbols('p', real=True)
        phi = p ** 3 - p
        A = 1 + sp.Rational(3, 4) * p ** 4 - sp.Rational(1, 2) * p ** 2
        self.assertEqual(sp.expand(sp.diff(A, p) - p * sp.diff(phi, p)), 0)
        self.assertEqual(sp.factor(A - sp.Rational(11, 12)), (3 * p ** 2 - 1) ** 2 / 12)
        self.assertEqual(A.subs(p, 1), sp.Rational(5, 4))
        self.assertEqual(A.subs(p, 0), 1)

    def test_16_uniform_delay_margins(self):
        for q in range(5):
            J, H, h = q + 3, 4.2, .1
            D = H + (J + 1) * h
            for W in np.linspace(0., H, 20):
                for j in range(1, J + 1):
                    residual = H + j * h - W
                    self.assertGreaterEqual(residual, h - 1e-14)
                    self.assertLessEqual(residual, D - h + 1e-14)

    def test_17_failure_of_nonmonotone_interval_identification(self):
        # w=1, r=s^2: equal-length intervals related by reflection have equal moments.
        a, b = -2., -1.
        c, d = 1., 2.
        self.assertEqual(b - a, d - c)
        self.assertAlmostEqual((b ** 3 - a ** 3) / 3, (d ** 3 - c ** 3) / 3)

    def test_18_equal_action_projective_cancellation(self):
        t, _, theta, a, U, V, _, _ = self.model()
        P, _ = latent_data(t, np.full(3, -.5), a, theta, U, V)
        Q, _ = latent_data(t, np.full(3, -2.), a, theta, U, V)
        np.testing.assert_allclose(P, Q, atol=1e-14)

    def test_19_finite_separator_count(self):
        for q in range(1, 5):
            rng = np.random.default_rng(q)
            coefficients = rng.normal(size=(5, q + 1))
            L = 10
            gaps = []
            for a in range(q * L + 1):
                vals = coefficients @ np.array([float(a) ** k for k in range(q + 1)])
                gaps.append(min(abs(vals[b] - vals[c]) for b in range(5) for c in range(b)))
            self.assertGreater(max(gaps), .001)

    def test_20_input_validation(self):
        with self.assertRaises(ValueError):
            divided_difference(np.array([1., 1.]), np.array([0., 1.]))
        with self.assertRaises(ValueError):
            scalar_values(np.array([1., 2., 3.]), np.zeros(1), 1., 0.)
        with self.assertRaises(ValueError):
            interval_inverse(np.array([1., 2., 3.]), np.zeros(3), (-2., 0.))

    def test_21_nonpolynomial_kernels(self):
        s, a = sp.symbols('s a')
        k0 = a/(1-s) - (a+1)/(2-s) + 1/(3-s)
        k1 = a/(2-s) - (a+1)/(3-s) + 1/(4-s)
        B0 = 3 + 2/(a-1)
        self.assertEqual(sp.factor(k0 - (a-1)*(B0-s)/((1-s)*(2-s)*(3-s))), 0)
        ratio = (1-s)*(B0+1-s)/((4-s)*(B0-s))
        self.assertEqual(sp.factor(k1/k0 - ratio), 0)
        derivative = -3/((1-s)*(4-s)) + 1/((B0-s)*(B0+1-s))
        self.assertEqual(sp.factor(sp.diff(ratio, s)/ratio - derivative), 0)
        for aa in [1.01, 1.2, 2., 10.]:
            for ss in [-100., -4., -.1, .9]:
                self.assertGreater(float(k0.subs({a:aa, s:ss})), 0)
                self.assertLess(float(derivative.subs({a:aa, s:ss})), 0)

    def test_22_nonpolynomial_three_clock_ambiguity(self):
        t = np.array([1., 2., 3.])
        lam, x, y = .7, -.4, -1.3
        def vals(z, yy):
            alpha, beta, xx = z
            return alpha + beta*np.exp(lam*t) + np.log(t-xx) - np.log(t-yy)
        z0 = np.array([.15, -.2, x])
        target = vals(z0, y)
        fitted = root(lambda z: vals(z, y+.001)-target, z0, tol=1e-11)
        self.assertLess(np.max(abs(fitted.fun)), 1e-11)
        self.assertLess(fitted.x[-1], 1.)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Revision83Checks)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    record = {'tests_run': result.testsRun, 'failures': len(result.failures),
              'errors': len(result.errors), 'passed': result.wasSuccessful(),
              'elapsed_seconds': round(time.monotonic() - started, 3),
              'scope': 'Deterministic algebra/numerical regression checks; not independent mathematical proof certification.',
              'details': [{'test': str(case), 'traceback': tb} for case, tb in result.failures + result.errors]}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    sys.exit(0 if result.wasSuccessful() else 1)
