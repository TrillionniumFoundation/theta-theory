#!/usr/bin/env python3
"""Exact algebra and independent finite density models, not a billiard proof."""
from __future__ import annotations
from fractions import Fraction as F
from math import factorial
import json
import mpmath as mp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def integrate_polynomial(coefficients: list[F]) -> F:
    return sum((a / (i + 1) for i, a in enumerate(coefficients)), F(0))


def derivative(coefficients: list[F]) -> list[F]:
    return [i * a for i, a in enumerate(coefficients)][1:] or [F(0)]


def value(coefficients: list[F], x: F) -> F:
    return sum((a * x**i for i, a in enumerate(coefficients)), F(0))


def log_moment(a: mp.mpf, k: int, d: mp.mpf) -> mp.mpf:
    return d**a * sum(mp.mpf(factorial(k)) / factorial(k-j) *
                     (-mp.log(d))**(k-j) / a**(j+1) for j in range(k+1))


def raw_jet_checks() -> dict:
    mp.mp.dps = 60
    tolerance = mp.mpf('1e-45')
    # Quintic C2 cutoff. Endpoint derivatives, not visual similarity, matter.
    cutoff = [F(1), F(0), F(0), F(-10), F(15), F(-6)]
    require(value(cutoff, F(0)) == 1 and value(cutoff, F(1)) == 0,
            'cutoff value trace')
    for order in (1, 2):
        d = cutoff
        for _ in range(order):
            d = derivative(d)
        require(value(d, F(0)) == value(d, F(1)) == 0, 'cutoff derivative trace')
    # A one-sided constant and slope have boundary distributions even though
    # their classical second derivatives on (0,1) are zero.
    test = [F(1), F(-4), F(6), F(-4), F(1)]  # (1-t)^4
    second = derivative(derivative(test))
    constant_boundary = integrate_polynomial(second)
    slope_boundary = integrate_polynomial([F(0)] + second)
    require(constant_boundary == 4 and slope_boundary == 1,
            'distributional trace negative controls')
    require(constant_boundary != 0 and slope_boundary != 0,
            'omitting constant/slope would pass')
    # Selection includes all logs at alpha=1. alpha>1 is the sufficient
    # second-derivative-integrability range for the remainder.
    cases = [(F(-1,2), 0, True), (F(0), 1, True), (F(0), 0, True),
             (F(1,2), 0, True), (F(1), 0, True), (F(1), 1, True),
             (F(3,2), 0, False), (F(4,3), 3, False), (F(2), 2, False)]
    for exponent, log_degree, extracted in cases:
        require((-1 < exponent <= 1) == extracted, 'wrong raw jet exponent')
        if not extracted:
            require(exponent - 2 > -1, 'residual second derivative not integrable')
        require(log_degree >= 0, 'log degree')
    # Closed log moment versus the independent x=d exp(-u) integral.
    count, error = 0, mp.mpf(0)
    for a0 in [F(1,3), F(1,2), F(1), F(3,2), F(2)]:
        a = mp.mpf(a0.numerator) / a0.denominator
        for k in range(5):
            for d in [mp.mpf(1)/4, mp.mpf(1)/8]:
                analytic = log_moment(a, k, d)
                quadrature = d**a * mp.quad(
                    lambda u: mp.exp(-a*u)*(u-mp.log(d))**k, [0, mp.inf])
                relative = abs(analytic-quadrature)/max(1, abs(analytic))
                error = max(error, relative)
                require(relative < tolerance, 'log-moment formula')
                count += 1
    # Three explicit pushforwards, computed by integration over the fibers.
    # x^2 on (-1,1)x(0,1), probability density 1/2 -> 1/(2 sqrt(t)).
    # xy on the unit square -> -log(t).
    # The exact weight xy on that square -> -t log(t), mass 1/4.
    fiber_cases = 0
    for t in [mp.mpf(1)/16, mp.mpf(1)/8, mp.mpf(1)/4, mp.mpf(1)/2,
              mp.mpf(3)/4, mp.mpf(7)/8]:
        square_root_density = 2*(mp.mpf(1)/2)/(2*mp.sqrt(t))
        require(abs(square_root_density-1/(2*mp.sqrt(t))) < tolerance,
                'fold density normalization')
        product_density = mp.quad(lambda x: 1/x, [t,1])
        weighted_product = mp.quad(lambda x: t/x, [t,1])
        require(abs(product_density+mp.log(t)) < tolerance, 'product logarithmic density')
        require(abs(weighted_product+t*mp.log(t)) < tolerance, 'weighted slope-log density')
        fiber_cases += 3
    masses = [mp.quad(lambda u: mp.exp(-u/2)/2, [0,mp.inf]),
              mp.quad(lambda u: u*mp.exp(-u), [0,mp.inf]),
              mp.quad(lambda u: u*mp.exp(-2*u), [0,mp.inf])]
    require(all(abs(a-b)<tolerance for a,b in zip(masses,[1,1,mp.mpf(1)/4])),
            'raw model masses')
    # Endpoint Taylor tails of the product densities after slope extraction.
    # -log(1-x)-x = sum_{j>=2} x^j/j.
    for denominator in [8,16,32,64,128]:
        x = mp.mpf(1)/denominator
        unweighted_tail = -mp.log1p(-x)-x
        weighted_tail = -(1-x)*mp.log1p(-x)-x
        require(0 < unweighted_tail < x*x, 'log endpoint remainder')
        require(-x*x < weighted_tail < 0, 'weighted endpoint remainder')
    # Exact finite count/frequency-splitting telescope, including convolution
    # of the high-count tail. No finite model is identified with a billiard.
    mu = [F(1,5)]*5
    edge = [F(1,7), F(-1,11), F(2,9), F(0), F(0)]
    residual = [mu[i]-edge[i] if i<3 else F(0) for i in range(5)]
    tail = [F(0)]*3 + mu[3:]
    kernel = [[F(1, 1+(i-j)**2) for j in range(5)] for i in range(5)]
    apply = lambda v: [sum((kernel[i][j]*v[j] for j in range(5)), F(0))
                       for i in range(5)]
    km, ke, kr, kt = map(apply, [mu,edge,residual,tail])
    for i in range(3):
        rhs = km[i]+edge[i]-ke[i]+residual[i]-kr[i]-kt[i]
        require(rhs == mu[i], 'exact count-localized inversion')
        require(rhs+kt[i] != mu[i], 'omitted high-count convolution escaped control')
    require(F(2)-4*F(99,200) == F(1,50), 'scaled count convolution exponent')
    require(F(1,2)-F(1,200) == F(99,200), 'physical central cutoff')
    require(1-F(99,200)==F(101,200), 'separated count kernel scale')
    require(F(1,50)-8*F(101,200)<-4, 'rapid central count correction')
    # The L1 integral of min(A0,A2/b^2) and its far-tail upper bound.
    fourier_cases = 0
    for a0,a2 in [(1,1),(2,3),(5,7),(mp.mpf(1)/3,mp.mpf(2)/5)]:
        a0,a2 = mp.mpf(a0),mp.mpf(a2)
        split = mp.sqrt(a2/a0)
        integral = 2*(a0*split+mp.quad(lambda b: a2/b**2,[split,mp.inf]))
        require(abs(integral-4*mp.sqrt(a0*a2)) < tolerance, 'Fourier L1 budget')
        B = 2*split
        far = 2*mp.quad(lambda b: a2/b**2,[B,mp.inf])
        require(abs(far-2*a2/B)<tolerance, 'far roof budget')
        fourier_cases += 1
    return {'cutoff_trace_checks': 6, 'jet_exponent_cases': len(cases),
            'log_moment_cases': count, 'log_moment_relative_error_below': '1e-45',
            'explicit_fiber_density_cases': fiber_cases,
            'explicit_model_masses': ['1','1','1/4'],
            'endpoint_remainder_cases': 10, 'count_localized_fiber_cases': 3,
            'Fourier_budget_cases': fourier_cases,
            'negative_controls': 5, 'count_convolution_power': '1/50',
            'tests_are_not_continuum_proof_certification': True}


if __name__ == '__main__':
    print(json.dumps(raw_jet_checks(), indent=2, sort_keys=True))
