#!/usr/bin/env python3
"""Deterministic checks of A2 v82 identities. These are not proof certification."""
from __future__ import annotations

import itertools
import unittest

import numpy as np
import sympy as sp
from numpy.testing import assert_allclose
from scipy.optimize import least_squares, linear_sum_assignment, root


def normalize(m: np.ndarray) -> np.ndarray:
    mass = float(m.sum())
    if not np.isfinite(mass) or mass <= 0:
        raise ValueError("A positive finite total mass is required")
    return m / mass


def observations(t, w, k, a, u, v):
    weights = np.exp(np.outer(t, k)) * a * (np.asarray(t)[:, None] - w)
    if np.any(weights <= 0):
        raise ValueError("Nonpositive latent weights")
    return np.array([normalize((u * row) @ v.T) for row in weights])


def split_components(p: np.ndarray, threshold: float = 1e-9):
    """Pointwise observable inverse, with no supplied B or channel columns."""
    b = int(np.sum(np.linalg.svd(p[0], compute_uv=False) > threshold))
    candidates = []
    for i in itertools.combinations(range(p.shape[1]), b):
        for j in itertools.combinations(range(p.shape[2]), b):
            minor = p[0][np.ix_(i, j)]
            candidates.append((np.linalg.svd(minor, compute_uv=False)[-1], i, j))
    _, i, j = max(candidates, key=lambda item: item[0])
    inv = np.linalg.inv(p[0][np.ix_(i, j)])
    ks = [mat[np.ix_(i, j)] @ inv for mat in p]
    choices = []
    for t in range(b * (b - 1) // 2 + 1):
        vals, vecs = np.linalg.eig(ks[1] + t * ks[2])
        gaps = [abs(vals[r] - vals[s]) for r in range(b) for s in range(r)]
        choices.append((min(gaps, default=1.0), vals, vecs))
    gap, vals, vecs = max(choices, key=lambda item: item[0])
    if gap < 1e-10 or np.max(np.abs(vals.imag)) > 1e-8:
        raise ValueError("No separated real local spectral chart")
    vecs = vecs.real
    inverse_vecs = np.linalg.inv(vecs)
    components = np.empty((len(p), b, p.shape[1], p.shape[2]))
    left = p[0][:, j] @ inv
    for clock, mat in enumerate(p):
        for c in range(b):
            projector = np.outer(vecs[:, c], inverse_vecs[c])
            components[clock, c] = left @ projector @ mat[list(i), :]
    pi = components.sum(axis=(2, 3))
    u = (components[0].sum(axis=2) / pi[0, :, None]).T
    v = (components[0].sum(axis=1) / pi[0, :, None]).T
    if np.any(pi <= 0):
        raise ValueError("Recovered component has nonpositive mass")
    return u, v, pi


def fit_anchor(t: np.ndarray, values: np.ndarray):
    """Bounded deterministic multistart for an example, not a global solver proof."""
    design = np.column_stack((np.ones_like(t), t))
    q, _ = np.linalg.qr(design, mode="complete")
    contrast = q[:, 2:].T
    def residual(xy):
        return contrast @ (values - np.log(t - xy[0]) + np.log(t - xy[1]))
    upper = float(t.min() - 0.05)
    starts = [t.min() - h for h in (0.4, 0.8, 1.3, 2.5)]
    best = None
    for x, y in itertools.product(starts, repeat=2):
        if x == y:
            continue
        result = least_squares(residual, [x, y], bounds=([-5, -5], [upper, upper]),
                               xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=2000)
        score = np.linalg.norm(result.fun)
        if best is None or score < best[0]:
            best = (score, result.x)
    assert best is not None
    x, y = best[1]
    ak = np.linalg.lstsq(design, values - np.log(t-x) + np.log(t-y), rcond=None)[0]
    return np.r_[ak, x, y], best[0]


class SelectiveDetectorChecks(unittest.TestCase):
    def setUp(self):
        self.t = np.arange(2.0, 7.0)
        self.w = np.array([1.0, 1.25, 1.25])
        self.k = np.array([-0.02, -0.08, -0.16])
        self.a = np.array([0.3, 0.2, 0.5])
        self.u = np.array([[.55,.12,.08],[.15,.58,.1],[.2,.18,.55],[.1,.12,.27]])
        self.v = np.array([[.4,.05,.12],[.2,.5,.08],[.1,.1,.5],[.2,.15,.2],[.1,.2,.1]])
        self.p = observations(self.t,self.w,self.k,self.a,self.u,self.v)

    def test_01_rank_and_component_reconstruction(self):
        u,v,pi = split_components(self.p)
        rows, cols = linear_sum_assignment(np.linalg.norm(u[:,:,None]-self.u[:,None,:],axis=0))
        order = np.array([rows[np.where(cols==c)[0][0]] for c in range(3)])
        u,v,pi = u[:,order],v[:,order],pi[:,order]
        assert_allclose(u,self.u,atol=2e-12)
        assert_allclose(v,self.v,atol=2e-12)
        for j in range(5):
            assert_allclose((u*pi[j])@v.T,self.p[j],atol=2e-12)

    def test_02_scalar_inverse_with_unequal_anchor(self):
        vals=np.log(self.a[0]/self.a[1])+(self.k[0]-self.k[1])*self.t
        vals+=np.log(self.t-self.w[0])-np.log(self.t-self.w[1])
        recovered, residual=fit_anchor(self.t,vals)
        self.assertLess(residual,1e-11)
        assert_allclose(recovered,[np.log(1.5),.06,1.,1.25],atol=2e-8)

    def test_03_common_detector_gauge(self):
        p2=observations(self.t,self.w,self.k+.37,self.a*5.7,self.u,self.v)
        assert_allclose(self.p,p2,atol=1e-15)

    def test_04_arbitrary_projective_rescaling(self):
        for j,scale in enumerate([.01,8.,.5,1000.,3.]):
            assert_allclose(normalize(scale*self.p[j]),self.p[j],atol=1e-15)

    def test_05_equal_action_obstruction(self):
        p1=observations(self.t,np.ones(3),self.k,self.a,self.u,self.v)
        p2=observations(self.t,np.ones(3)*.3,self.k,self.a,self.u,self.v)
        assert_allclose(p1,p2,atol=1e-15)

    def test_06_one_operator_collision_resolved_jointly(self):
        w=np.array([.3,1.2]); k=np.array([0.,0.])
        k[1]=np.log(((self.t[1]-w[0])/(self.t[0]-w[0]))/
                    ((self.t[1]-w[1])/(self.t[0]-w[1])))/(self.t[1]-self.t[0])
        p=observations(self.t,w,k,np.array([.4,.6]),self.u[:,:2]/self.u[:,:2].sum(0),
                       self.v[:,:2]/self.v[:,:2].sum(0))
        u,v,pi=split_components(p)
        q=pi/pi[0]
        self.assertLess(abs(q[1,0]-q[1,1]),1e-12)
        self.assertGreater(abs(q[2,0]-q[2,1]),1e-3)
        for j in range(5): assert_allclose((u*pi[j])@v.T,p[j],atol=1e-12)

    def test_07_exact_jacobian_determinant(self):
        x,y=sp.symbols('x y')
        c=sp.Matrix([[x*y,0,y,-x],[-x-y,x*y,-1,1],[1,-x-y,0,0],[0,1,0,0]])
        self.assertEqual(sp.factor(c.det()),y-x)
        ts=list(map(sp.Rational,[2,3,4,5])); xx=sp.Rational(1,3); yy=sp.Rational(7,6)
        j=sp.Matrix([[1,t,-1/(t-xx),1/(t-yy)] for t in ts])
        rhs=(yy-xx)*sp.prod(ts[j]-ts[i] for i in range(4) for j in range(i+1,4))
        rhs/=sp.prod((t-xx)*(t-yy) for t in ts)
        self.assertEqual(sp.simplify(j.det()-rhs),0)

    def test_08_four_pole_numerator_degree_and_sum(self):
        t,k=sp.symbols('t k'); poles=list(map(sp.Rational,[0,1,-1,-2]))
        d=sp.prod(t-p for p in poles)
        r=sp.cancel(d*sum(c/(t-p) for c,p in zip([1,-1,-1,1],poles)))
        self.assertLessEqual(sp.degree(r,t),2)
        numerator=sp.Poly(k*d+r,t)
        self.assertEqual(sp.simplify(-numerator.coeff_monomial(t**3)/k),sum(poles))

    def test_09_three_clock_action_ambiguity(self):
        ts=self.t[:3]; x0=.4; y0=1.1; aa=.2; kk=-.15
        target=aa+kk*ts+np.log(ts-x0)-np.log(ts-y0)
        y1=y0+.01
        def eq(z):
            a,k,x=z
            return a+k*ts+np.log(ts-x)-np.log(ts-y1)-target
        sol=root(eq,[aa,kk,x0],tol=1e-11)
        self.assertTrue(sol.success)
        self.assertGreater(abs(sol.x[2]-x0),1e-5)
        assert_allclose(eq(sol.x),np.zeros(3),atol=1e-12)

    def test_10_polynomial_local_jacobian(self):
        for degree in [1,2,3]:
            ts=list(map(sp.Rational,range(2,degree+5)))
            x=sp.Rational(1,3); y=sp.Rational(4,3)
            j=sp.Matrix([[t**r for r in range(degree+1)]+[-1/(t-x),1/(t-y)] for t in ts])
            self.assertNotEqual(j.det(),0)

    def test_11_unrestricted_detector_interpolation(self):
        neww=self.w+np.array([.1,-.2,.15])
        newweights=[]
        for b in range(3):
            values=self.k[b]*self.t+np.log((self.t-self.w[b])/(self.t-neww[b]))
            coeff=np.polynomial.polynomial.polyfit(self.t,values,4)
            newweights.append(self.a[b]*np.exp(np.polynomial.polynomial.polyval(self.t,coeff))*(self.t-neww[b]))
        for j,row in enumerate(np.array(newweights).T):
            assert_allclose(normalize((self.u*row)@self.v.T),self.p[j],atol=2e-13)

    def test_12_shear_exactness_and_roof(self):
        p=sp.symbols('p',real=True)
        phi=p**3-p; action=1+sp.Rational(3,4)*p**4-sp.Rational(1,2)*p**2
        self.assertEqual(sp.simplify(sp.diff(action,p)-p*sp.diff(phi,p)),0)
        self.assertEqual(sp.factor(action-sp.Rational(11,12)),(3*p**2-1)**2/12)
        self.assertEqual(action.subs(p,1),action.subs(p,-1))
        self.assertNotEqual(action.subs(p,0),action.subs(p,1))

    def test_13_crossed_action_physical_channels(self):
        momenta=np.array([-1.,0.,1.])
        raw=np.exp(np.outer(np.arange(3),.7*momenta))
        chan=raw/raw.sum(0)
        self.assertGreater(abs(np.linalg.det(chan)),.005)
        rates=.4+.1*momenta
        retention=.6*np.exp(-np.outer(self.t-self.t[0],rates))
        self.assertTrue(np.all((retention>0)&(retention<=.6)))

    def test_14_common_clock_margins(self):
        h=.3; H=4.; D=H+6*h
        ts=H+np.arange(1,6)*h
        for action in np.linspace(0,H,30):
            self.assertGreaterEqual(float(np.min(ts-action)),h-1e-14)
            self.assertGreaterEqual(float(np.min(D-(ts-action))),h-1e-14)

    def test_15_visible_rank_threshold(self):
        singular=np.linalg.svd(self.p[0],compute_uv=False)
        margin=singular[2]; rng=np.random.default_rng(82)
        noise=rng.normal(size=self.p[0].shape)
        noise*=margin/(8*np.linalg.norm(noise,2))
        self.assertEqual(np.sum(np.linalg.svd(self.p[0]+noise,compute_uv=False)>margin/2),3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
