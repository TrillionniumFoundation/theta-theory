#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v3 referee report.
No repository imports or network calls. Not interval or formal proofs.
Run: python diagnostics.py > diagnostics.json
Dependencies: numpy, scipy, sympy. All tests use explicit non-removable checks.
"""
from __future__ import annotations
import hashlib
import json
import math
import platform
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import brentq
import sympy as sp

CHECKS: list[dict[str, object]] = []
DETAILS: dict[str, object] = {}


def check(name: str, condition: object, kind: str) -> None:
    ok = bool(condition)
    CHECKS.append({"name": name, "kind": kind, "passed": ok})
    if not ok:
        raise RuntimeError(f"Diagnostic failed: {name}")


def schur(j: int, c0: Q, c1: Q, gap: Q) -> list[list[Q]]:
    """Eliminate the tridiagonal interior using exact rational arithmetic."""
    diag = [(c0 if i % 2 == 0 else c1) / gap *
            (1 if i in (0, j) else 2) for i in range(j + 1)]
    left, coupling = diag[0], -1 / gap
    for i in range(1, j):
        pivot = diag[i]
        left -= coupling * coupling / pivot
        nxt = -1 / gap
        diag[i + 1] -= nxt * nxt / pivot
        coupling = -coupling * nxt / pivot
    return [[left, coupling], [coupling, diag[j]]]


def chebyshev(j: int, c: Q) -> tuple[Q, Q]:
    previous, current = Q(0), Q(1)  # U_{-1}, U_0
    for _ in range(j - 1):
        previous, current = current, 2 * c * current - previous
    return previous, current


def exact_chains() -> None:
    cases = [(Q(2), Q(8), Q(4), Q(1, 3)),
             (Q(3, 2), Q(8, 3), Q(2), Q(2, 5)),
             (Q(5, 4), Q(5), Q(5, 2), Q(3, 4)),
             (Q(2), Q(2), Q(2), Q(1))]
    lengths = list(range(1, 13)) + [31, 32, 63, 64, 127, 128]
    for ic, (c0, c1, c, g) in enumerate(cases):
        for j in lengths:
            h = schur(j, c0, c1, g)
            um, u = chebyshev(j, c)
            n = c - um / u
            sigj2 = c1 if j % 2 == 0 else c0
            sigprod = c1 if j % 2 == 0 else c
            predicted = [[c*n/(g*c1), -c/(g*sigprod*u)],
                         [-c/(g*sigprod*u), c*n/(g*sigj2)]]
            prefix = f"chain/{ic}/{j}"
            check(prefix + "/schur", h == predicted, "exact-rational")
            det = h[0][0]*h[1][1] - h[0][1]**2
            check(prefix + "/positive", h[0][0] > 0 and det > 0,
                  "exact-rational")
            check(prefix + "/relative-twist", h[0][1]**2 / det ==
                  1 / ((c*c-1)*u*u), "exact-rational")
            if j % 2:
                v0, v1 = h[1][1]/(3*det), h[0][0]/(3*det)
                base0, base1 = g*c1/(3*(c0*c1-1)), g*c0/(3*(c0*c1-1))
                check(prefix + "/variance-ratio", v1/v0 == c0/c1,
                      "exact-rational")
                check(prefix + "/one-flight-saturation",
                      v0/base0 == n/c and v1/base1 == n/c,
                      "exact-rational")
    DETAILS["exact_chain_lengths"] = lengths


def coth(x: float) -> float:
    z = math.exp(-2*x)
    return (1+z)/(1-z)


def variance(g: float, k0: float, k1: float, j: int) -> np.ndarray:
    c0, c1 = 1+g*k0, 1+g*k1
    gam = math.acosh(math.sqrt(c0*c1))
    scale = g*coth(j*gam)/(3*math.sinh(gam))
    return scale*np.array([math.sqrt(c1/c0), math.sqrt(c0/c1)])


def recover(g: float, v: np.ndarray, j: int) -> np.ndarray:
    p = 3*math.sqrt(float(v[0]*v[1]))/g
    gam = brentq(lambda x: coth(j*x)/math.sinh(x)-p, 1.e-5, 15.,
                 xtol=1.e-14)
    r = math.sqrt(float(v[1]/v[0]))
    c = math.cosh(gam)
    return np.array([(r*c-1)/g, (c/r-1)/g])


def numerical_inverse() -> None:
    min_sv, max_sv = math.inf, 0.
    for g in (.3, .7, 1.):
        for k0, k1 in ((.5, .5), (.5, 2.), (1.3, 2.1), (3., 3.)):
            gam = math.acosh(math.sqrt((1+g*k0)*(1+g*k1)))
            for j in (1, 3, 9, 33, 129, 1025):
                pre = f"inverse/{g}/{k0}/{k1}/{j}"
                v = variance(g, k0, k1, j)
                check(pre + "/reconstruction", np.max(np.abs(
                    recover(g, v, j)-[k0,k1])) < 2.e-10, "numerical")
                step = 1.e-5
                jac = np.column_stack([
                    (variance(g,k0+step,k1,j)-variance(g,k0-step,k1,j))/(2*step),
                    (variance(g,k0,k1+step,j)-variance(g,k0,k1-step,j))/(2*step)])
                singular = np.linalg.svd(jac, compute_uv=False)
                min_sv, max_sv = min(min_sv,float(singular[-1])), max(max_sv,float(singular[0]))
                check(pre + "/jacobian", singular[-1] > .001 and
                      singular[0] < 10, "numerical")
                predicted = variance(g,k0,k1,1)*coth(j*gam)/coth(gam)
                check(pre + "/saturation", np.max(np.abs(v-predicted)) < 1.e-13,
                      "numerical")
    DETAILS["sampled_inverse_singular_values"] = [min_sv, max_sv]


def symbolic_and_fiber() -> None:
    t = sp.symbols("t", real=True)
    a, b, z = sp.symbols("a b z", real=True)
    chi0 = (1+sp.cos(t))*sp.sin(t)**2/4
    chi1 = (1-sp.cos(t))*sp.sin(t)**2/4
    chis = sp.sin(t)**4
    bases = [chi0, chi1, chis]
    for ib, f in enumerate(bases):
        for k in (0,1,2):
            for it, theta in enumerate((0,sp.pi)):
                expected = int(k == 2 and ib == it)
                check(f"support-jet/{ib}/{k}/{it}",
                      sp.simplify(sp.diff(f,t,k).subs(t,theta)-expected) == 0,
                      "exact-symbolic")
    # Exact Fourier coefficients, obtained by trigonometric expansion.
    # chi0=(2+cos t-2 cos 2t-cos 3t)/16;
    # chi1=(2-cos t-2 cos 2t+cos 3t)/16;
    # chis=(3-4 cos 2t+cos 4t)/8.
    f0 = (2+sp.cos(t)-2*sp.cos(2*t)-sp.cos(3*t))/16
    f1 = (2-sp.cos(t)-2*sp.cos(2*t)+sp.cos(3*t))/16
    fs = (3-4*sp.cos(2*t)+sp.cos(4*t))/8
    for i, (f, ff) in enumerate(zip(bases,[f0,f1,fs])):
        check(f"support-fourier/{i}", sp.trigsimp(sp.expand_trig(f-ff)) == 0,
              "exact-symbolic")
    mean = 1+(a+b)/8+3*z/8
    coef2 = -(a+b)/8-z/2
    coef3 = -(a-b)/16
    coef4 = z/8
    area_over_pi = sp.expand(mean**2 +
                            (-3*coef2**2-8*coef3**2-15*coef4**2)/2)
    check("area/compensator-derivative", sp.diff(area_over_pi,z).subs(
        {a:0,b:0,z:0}) == sp.Rational(3,4), "exact-symbolic")
    check("area/reflection", sp.expand(area_over_pi-area_over_pi.xreplace(
        {a:b,b:a})) == 0, "exact-symbolic")
    DETAILS["fiber_area_over_pi"] = str(area_over_pi)
    area = sp.lambdify((a,b,z),area_over_pi,"numpy")
    radius = sp.lambdify((t,a,b,z),
                        1+a*(chi0+sp.diff(chi0,t,2))+
                        b*(chi1+sp.diff(chi1,t,2))+
                        z*(chis+sp.diff(chis,t,2)),"numpy")
    rows = []
    for s in (-.02,-.01,-.003,0.,.003,.01,.02):
        r0, r1 = 1/(2*math.exp(s)-1), 1/(2*math.exp(-s)-1)
        aa,bb = r0-1,r1-1
        zz = brentq(lambda u: float(area(aa,bb,u))-1, -.1,.1,
                    xtol=1.e-15)
        rr = radius(np.linspace(0,2*math.pi,4096,endpoint=False),aa,bb,zz)
        check(f"fiber/{s}/area", abs(float(area(aa,bb,zz))-1) < 1.e-12,
              "numerical")
        check(f"fiber/{s}/sampled-curvature", np.min(rr) > .7,
              "numerical")
        check(f"fiber/{s}/jets", max(abs(float(radius(0,aa,bb,zz))-r0),
              abs(float(radius(math.pi,aa,bb,zz))-r1)) < 1.e-12, "numerical")
        for j in (1,3,31,129):
            v = variance(1.,1/r0,1/r1,j)
            check(f"fiber/{s}/{j}/variance-separation", abs(
                v[1]/v[0]-math.exp(2*s)) < 1.e-12,"numerical")
        rows.append({"s":s,"area_correction":zz,"sampled_min_radius":float(np.min(rr))})
    DETAILS["fiber_samples"] = rows


def coalescence() -> None:
    # High precision avoids finite-difference cancellation at large order.
    import mpmath as mp
    mp.mp.dps = 70
    R,g = mp.mpf(".3"),mp.mpf(".4")
    A0 = mp.sqrt(3)/2-mp.pi*R**2
    alpha = mp.mpf(".4")
    def coeff(s: object, j: int) -> object:
        radii = [R+36*s,R-18*s,R-18*s]
        return sum(1/mp.sinh(j*mp.acosh(1+g/r)) for r in radii)/(A0+45*mp.pi*s*s/4)
    rows = []
    for st in ("0.0001","0.00003","0.00001"):
        s = mp.mpf(st)
        norm = max(mp.exp(alpha*j)*abs(coeff(s,j)-coeff(0,j))
                   for j in range(1,129))
        ratio = float(norm/(s*s))
        check(f"coalescence/{st}/weighted-quadratic", 1. < ratio < 1.e6,
              "numerical-high-precision")
        dist = max(abs(1/(R+36*s)-1/R),abs(1/(R-18*s)-1/R))
        check(f"coalescence/{st}/linear-geometry", 300. < float(dist/s) < 500.,
              "numerical-high-precision")
        rows.append({"s":st,"weighted_norm_over_s_squared":ratio,
                     "curvature_distance_over_s":float(dist/s)})
    DETAILS["coalescence_finite_prefix"] = {"length":128,"weight_exponent":.4,"rows":rows}


def local_quadrature(d: float, ntheta: int, nr: int) -> tuple[float,np.ndarray]:
    """One real nonlinear flight; integrate its exact sublevel, not a Morse approximation."""
    g = .4
    k = np.array([1.3,2.1]); cubic = np.array([.7,-.9]); quartic = np.array([3.,4.])
    h = np.array([[1+g*k[0],-1],[-1,1+g*k[1]]])/g
    ev, vec = np.linalg.eigh(h)
    transform = (vec*(1/np.sqrt(ev)))@vec.T
    jac0 = 2*d*np.linalg.det(transform)
    nodes,weights = np.polynomial.legendre.leggauss(nr)
    nodes,weights = (nodes+1)/2,weights/2
    sums = np.zeros(7)
    def evaluate(y: np.ndarray):
        psi = k*y*y/2+cubic*y**3/6+quartic*y**4/24
        prime = k*y+cubic*y*y/2+quartic*y**3/6
        D = g+psi[...,0]+psi[...,1]
        delta = y[...,1]-y[...,0]
        L = np.sqrt(D*D+delta*delta)
        excess = psi[...,0]+psi[...,1]+delta*delta/(L+D)
        twist = (1-prime[...,0]*prime[...,1])/L + (
            D*prime[...,0]-delta)*(D*prime[...,1]+delta)/(L**3)
        return excess,twist,psi
    for theta in 2*math.pi*np.arange(ntheta)/ntheta:
        axis = math.sqrt(2*d)*transform@np.array([math.cos(theta),math.sin(theta)])
        rad = brentq(lambda r: float(evaluate(r*axis)[0])-d,.2,2.,xtol=1.e-14)
        y = (rad*nodes[:,None])*axis[None,:]
        excess,twist,psi = evaluate(y)
        w = weights*nodes*rad*rad*jac0*(d-excess)*twist*(2*math.pi/ntheta)
        sums[0] += np.sum(w)
        sums[1:3] += np.sum(w[:,None]*y,axis=0)
        sums[3:5] += np.sum(w[:,None]*psi,axis=0)
        sums[5:7] += np.sum(w[:,None]*(y*y+psi*psi),axis=0)
    mass = sums[0]
    v = (sums[5:7]/mass-(sums[1:3]/mass)**2-(sums[3:5]/mass)**2)/d
    leading = math.pi*d*d/g/math.sqrt(np.linalg.det(h))
    return mass/leading,v


def nonlinear_tests() -> None:
    target = variance(.4,1.3,2.1,1)
    rows = []
    for d in (1.e-3,3.e-4,1.e-4,3.e-5):
        ratio,v = local_quadrature(d,128,24)
        refined,vr = local_quadrature(d,256,40)
        check(f"quadrature/{d}/refinement", abs(ratio-refined) < 2.e-9 and
              np.max(np.abs(v-vr)) < 2.e-9,"numerical")
        check(f"quadrature/{d}/relative-onset", abs(refined-1) < 3*d,
              "numerical")
        check(f"quadrature/{d}/physical-variance", np.max(np.abs(vr-target)) < 3*d,
              "numerical")
        rows.append({"d":d,"probability_over_leading":refined,
                     "physical_variances":vr.tolist(),
                     "variance_bias_over_d":((vr-target)/d).tolist()})
    DETAILS["nonlinear_one_flight_quadrature"] = {
        "gap":.4,"curvatures":[1.3,2.1],"cubic_jets":[.7,-.9],
        "quartic_jets":[3.,4.],"limiting_variances":target.tolist(),"rows":rows}


def main() -> None:
    exact_chains(); numerical_inverse(); symbolic_and_fiber(); coalescence(); nonlinear_tests()
    kinds = dict(sorted(Counter(str(x["kind"]) for x in CHECKS).items()))
    data = {"status":"PASS","count":len(CHECKS),"categories":kinds,
            "source_commit":"3f8ad0a5b718818a22c0e2e47378d4d6c93473a1",
            "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "environment":{"python":platform.python_version(),"numpy":np.__version__,
                           "scipy":scipy.__version__,"sympy":sp.__version__},
            "limitations":["Finite diagnostics, not continuum, interval or formal certification.",
                           "Local one-flight quadrature, not a full equilibrium billiard simulation.",
                           "Sampled curvature positivity, not a replacement for the analytic openness proof.",
                           "No manuscript build, author-suite replay, remote CI or network requests."],
            "details":DETAILS,"checks":CHECKS}
    print(json.dumps(data,indent=2,sort_keys=True,allow_nan=False))

if __name__ == "__main__":
    main()
