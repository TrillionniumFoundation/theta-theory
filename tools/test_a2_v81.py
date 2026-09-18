#!/usr/bin/env python3
"""Deterministic algebra regressions for A2 v81; not a formal proof checker.

Requires Python 3 and NumPy. Run from any directory. --json writes an audit
record. No network, repository writes, random global state, or hidden fixtures.
"""
from __future__ import annotations
import argparse
import itertools
import json
import unittest
from pathlib import Path
import numpy as np

SEED = 810918

def channel(rows: int, cols: int, rng: np.random.Generator) -> np.ndarray:
    result = .15 + rng.random((rows, cols))
    result[:cols] += 2.5 * np.eye(cols)
    return result / result.sum(axis=0)

def observed(U: np.ndarray, V: np.ndarray, a: np.ndarray,
             W: np.ndarray, clocks: np.ndarray) -> list[np.ndarray]:
    return [(U * (a * (float(t) - W))) @ V.T for t in clocks]

def blind(M1: np.ndarray, M2: np.ndarray, t1: float, t2: float,
          tolerance: float = 1e-9) -> tuple[np.ndarray, ...]:
    if t2 <= t1 or M1.shape != M2.shape:
        raise ValueError('Ordered clocks and equal matrix shapes required')
    D = (M2 - M1) / (t2 - t1)
    b = int(np.count_nonzero(np.linalg.svd(D, compute_uv=False) > tolerance))
    if not b:
        raise ValueError('No visible component')
    # Finite exhaustive pivot search makes this regression deterministic.
    candidates = ((i, j) for i in itertools.combinations(range(D.shape[0]), b)
                  for j in itertools.combinations(range(D.shape[1]), b))
    I, J = max(candidates, key=lambda ij: abs(np.linalg.det(D[np.ix_(*ij)])))
    inv = np.linalg.inv(D[np.ix_(I, J)])
    K = M1[np.ix_(I, J)] @ inv
    eig = np.linalg.eigvals(K)
    if np.max(np.abs(eig.imag)) > tolerance:
        raise ValueError('Non-real spectral data')
    eig = np.sort(eig.real)[::-1]  # increasing absolute actions
    weights, left, right = [], [], []
    for k, lam in enumerate(eig):
        P = np.eye(b)
        for l, other in enumerate(eig):
            if l != k:
                if abs(lam - other) < tolerance:
                    raise ValueError('Unseparated actions')
                P = P @ ((K - other * np.eye(b)) / (lam - other))
        E = D[:, J] @ inv @ P @ D[I, :]
        weight = E.sum()
        if weight <= 0:
            raise ValueError('Nonpositive component mass')
        weights.append(weight)
        left.append(E.sum(axis=1) / weight)
        right.append(E.sum(axis=0) / weight)
    return t1 - eig, np.array(weights), np.array(left).T, np.array(right).T

def deproject(N: list[np.ndarray], clocks: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    H = np.column_stack((N[0].ravel(), N[1].ravel()))
    if np.linalg.matrix_rank(H, tol=1e-10) < 2:
        raise ValueError('Projective two-plane is not visible')
    alpha, beta = np.linalg.lstsq(H, N[2].ravel(), rcond=None)[0]
    delta = clocks[1] - clocks[0]
    a0, b0 = (clocks[1] - clocks[2]) / delta, (clocks[2] - clocks[0]) / delta
    if alpha / a0 <= 0 or beta / b0 <= 0:
        raise ValueError('Nonpositive recovered exposures')
    return (alpha / a0) * N[0], (beta / b0) * N[1]

class ClockPencilTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rng = np.random.default_rng(SEED)
        self.T = np.array([6., 8., 11.])

    def instance(self, b: int = 3) -> tuple[np.ndarray, ...]:
        U, V = channel(b+1, b, self.rng), channel(b+2, b, self.rng)
        a, W = .02 + .01 * self.rng.random(b), np.linspace(.7, 3.5, b)
        return U, V, a, W

    def test_unknown_count_and_channels(self) -> None:
        for b in range(1, 5):
            U, V, a, W = self.instance(b)
            M = observed(U, V, a, W, self.T)
            for actual, target in zip(blind(M[0], M[1], *self.T[:2]), (W, a, U, V)):
                np.testing.assert_allclose(actual, target, atol=2e-10, rtol=2e-10)

    def test_three_unknown_exposures(self) -> None:
        for b in range(2, 5):
            U, V, a, W = self.instance(b)
            c = np.array([.31, 2.7, 1.9])
            N = [x*y for x,y in zip(c, observed(U,V,a,W,self.T))]
            P = deproject(N, self.T)
            for actual, target in zip(blind(*P, *self.T[:2]), (W, c[2]*a, U, V)):
                np.testing.assert_allclose(actual, target, atol=3e-9, rtol=3e-9)

    def test_endpoint_dependent_channels_and_detectors(self) -> None:
        U0, V0, a, W = self.instance()
        for z in np.linspace(-.8,.8,17):
            U = U0 * np.exp(z*np.arange(U0.shape[0]))[:,None]; U /= U.sum(axis=0)
            V = V0 * np.exp(-z*np.arange(V0.shape[0]))[:,None]; V /= V.sum(axis=0)
            Wz = W + .15*np.sin(z + np.arange(len(W)))
            c = np.exp(np.array([z, -2*z, .3*z]))
            N = [x*y for x,y in zip(c, observed(U,V,a,Wz,self.T))]
            got = blind(*deproject(N,self.T), *self.T[:2])
            for actual, target in zip(got, (Wz,c[2]*a,U,V)):
                np.testing.assert_allclose(actual,target,atol=2e-8,rtol=2e-8)

    def test_only_conditional_pair_at_endpoint(self) -> None:
        U,V,a,W = self.instance()
        M = observed(U,V,a,W,self.T)
        N = [x / x.sum() for x in M]
        got = blind(*deproject(N,self.T),*self.T[:2])
        np.testing.assert_allclose(got[0],W,atol=3e-10)
        np.testing.assert_allclose(got[1]/got[1].sum(),a/a.sum(),atol=3e-10)

    def test_two_projective_clock_ambiguity(self) -> None:
        U,V,a,W = self.instance()
        q = 1.025; t1,t2 = self.T[:2]
        ratio = (t2-W)/(t1-W)
        Wp = (t2-q*ratio*t1)/(1-q*ratio)
        ap = a*(t1-W)/(t1-Wp)
        M = observed(U,V,a,W,self.T[:2]); P = observed(U,V,ap,Wp,self.T[:2])
        self.assertGreater(np.linalg.norm(Wp-W), .05)
        np.testing.assert_allclose(P[0],M[0],atol=2e-14)
        np.testing.assert_allclose(P[1]/q,M[1],atol=2e-14)

    def test_one_view_nonidentifiability(self) -> None:
        U,V,a,W = self.instance()
        R = np.eye(3); R[:,0] += np.array([-.01,.01,0.])
        Up = U@R; ap = np.linalg.solve(R,a); Wp = np.linalg.solve(R,a*W)/ap
        self.assertGreater(np.linalg.norm(Wp-W),1e-3)
        for t in np.linspace(6,20,21):
            np.testing.assert_allclose(Up@(ap*(t-Wp)),U@(a*(t-W)),atol=1e-14)

    def test_single_sheet_projective_rank_failure(self) -> None:
        U,V,a,W = self.instance(1)
        M = observed(U,V,a,W,self.T)
        with self.assertRaises(ValueError):
            deproject([x/x.sum() for x in M], self.T)

    def test_fixed_source_retention_compensation(self) -> None:
        z = np.linspace(-1,1,101)
        # rho is one fixed function; J changes only through the physical map.
        rho = lambda p: np.exp(-p*p)
        W0, Wt = 1 + .1*z*z, 1 + .1*z*z + .005*np.cos(z)
        J0, Jt = rho(z)*(1+.2*z*z), rho(z+.004)*(1+.2*z*z+.003)
        baseline = .4 + .02*z
        for T in self.T:
            et = baseline*(J0/Jt)*((T-W0)/(T-Wt))
            self.assertTrue(np.all((et>0)&(et<1)))
            np.testing.assert_allclose(et*Jt*(T-Wt),baseline*J0*(T-W0),atol=1e-14)

    def test_common_window_construction(self) -> None:
        for horizon in (0.,1.,20.):
            h=.3; D=horizon+4*h
            T=horizon+h*np.arange(1,4)
            for W in np.linspace(0,horizon,101):
                self.assertTrue(np.all(T-W >= h-1e-12))
                self.assertTrue(np.all(T-W <= D-h+1e-12))

    def test_actual_nonconvex_three_sheet_shear(self) -> None:
        for s in np.linspace(.04,.12,9):
            p = np.sort(np.roots([1.,0.,-1.,-s]).real)
            W = 1 + .75*p**4 - .5*p**2
            self.assertGreater(np.min(np.diff(np.sort(W))), .02)
            U = np.exp(np.arange(3)[:,None]*p[None,:]); U /= U.sum(axis=0)
            V = np.exp(.7*np.arange(3)[:,None]*p[None,:]); V /= V.sum(axis=0)
            self.assertEqual(np.linalg.matrix_rank(U),3)
            self.assertEqual(np.linalg.matrix_rank(V),3)
            a = np.exp(-p*p)*.01/np.abs(3*p*p-1)
            M = observed(U,V,a,W,self.T)
            got = blind(*deproject([x/x.sum() for x in M],self.T),*self.T[:2])
            np.testing.assert_allclose(got[0],np.sort(W),atol=2e-9)

    def test_local_noise_is_not_certification(self) -> None:
        U,V,a,W = self.instance()
        M = observed(U,V,a,W,self.T)
        noise = [self.rng.normal(size=x.shape) for x in M[:2]]
        errors=[]
        for epsilon in (1e-8,1e-9,1e-10):
            # Keep rank fixed by a signal threshold above the noise.
            got=blind(M[0]+epsilon*noise[0],M[1]+epsilon*noise[1],*self.T[:2],tolerance=1e-6)
            errors.append(float(np.linalg.norm(got[0]-W)))
        self.assertLess(errors[1],.2*errors[0])
        self.assertLess(errors[2],.2*errors[1])

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path)
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ClockPencilTests))
    report={'seed':SEED,'tests_run':result.testsRun,'failures':len(result.failures),
            'errors':len(result.errors),'passed':result.wasSuccessful(),
            'scope':'Finite-dimensional numerical regression only; not proof certification.'}
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
