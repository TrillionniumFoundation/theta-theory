#!/usr/bin/env python3
"""Independent finite controls for the A2 v39 referee report.

No manuscript source is imported, no billiard is simulated, and no TeX is run.
High-precision residuals are numerical diagnostics, not interval certificates.
"""
from __future__ import annotations

from fractions import Fraction
import json
import platform
import mpmath as mp

SUBMISSION = 'dd0e5aefd49d200652afc3fc3f29f7a6f38ae326'
mp.mp.dps = 100


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def number(x: mp.mpf) -> str:
    return mp.nstr(x, 24)


def hellinger_squared(theta: mp.mpf) -> mp.mpf:
    # f_theta(x) = 3 (r^2-x^2)_+/(4 r^3), r=1+theta.
    r = 1 + theta
    a = 3 / (4 * r**3)
    c = min(mp.mpf(1), r)
    f0 = lambda x: mp.mpf(3) * max(1-x*x, 0) / 4
    f1 = lambda x: a * max(r*r-x*x, 0)
    # Split close to the support edge to resolve the logarithmic contribution.
    points = [mp.mpf(0), c/2, 3*c/4, 9*c/10]
    gap = abs(theta)
    for factor in (1000, 100, 10, 1, mp.mpf('0.1')):
        p = c - factor*gap
        if 0 < p < c:
            points.append(p)
    points = sorted(set(points + [c]))
    common = 2*mp.quad(lambda x: (mp.sqrt(f1(x))-mp.sqrt(f0(x)))**2, points)
    # Exact mass on the support-exclusive interval, written without cancellation.
    R = max(r, mp.mpf(1))
    A = a if r > 1 else mp.mpf(3)/4
    exclusive = 2*A*(R-c)**2*(R-(R-c)/3)
    return common + exclusive


def boundary_controls() -> dict:
    # w_theta=r^2-x^2, a_theta=3/(4r^3). At theta=0 the two
    # boundary points contribute (3/4)*2^2/2 each, so J=3.
    J = mp.mpf(3)
    rows = []
    for sign in (-1, 1):
        errors = []
        for exponent in (2, 4, 6, 8):
            theta = sign*mp.power(10, -exponent)
            H2 = hellinger_squared(theta)
            ratio = H2/(theta**2*mp.log(1/abs(theta)))
            error = abs(ratio-J/4)
            require(H2 > 0, 'Nonpositive Hellinger distance')
            errors.append(error)
            rows.append({'theta': number(theta), 'H2': number(H2),
                         'H2_over_theta2_log': number(ratio),
                         'asymptotic_target': '0.75'})
        require(all(b < a for a, b in zip(errors, errors[1:])),
                'Hellinger coefficient failed the displayed convergence control')
        require(errors[-1] < mp.mpf('0.05'), 'Hellinger coefficient normalization')
    return {'boundary_information': '3', 'rows': rows}


def collar_controls() -> dict:
    # For q=delta*ell^(1/4), cutoff c=sqrt(1-q), the null score is
    # S=-3+2/(1-x^2). These are exact antiderivatives under the
    # ORIGINAL alternative density, not expectations transferred by TV.
    rows = []
    worst_identity_error = mp.mpf(0)
    for ell in (16, 32, 64, 128):
        delta = mp.exp(-ell)
        q = delta*mp.root(ell, 4)
        c = mp.sqrt(1-q)
        k = 1/(delta**2*ell)  # Effective intensity, not an integer sample size.
        for h in (-1, 0, 1):
            r = 1+delta*h
            A = r*r
            B = A-1
            a = 3/(4*r**3)
            require(r > c, 'Chosen alternatives do not share the tested collar')
            mean_mark = 2*a*(c**3 + (2-3*A)*c + 2*B*mp.atanh(c))
            second_mark = 2*a*((9*A-12)*c-3*c**3 +
                               (4-10*B)*mp.atanh(c)+2*B*c/q)
            mean_delta = k*delta*mean_mark
            variance_delta = k*delta**2*(second_mark-mean_mark**2)
            # Mass between c and r on both sides; stable factored expression.
            collar_mass = 2*a*(r-c)**2*(r-(r-c)/3)
            require(collar_mass > 0 and second_mark > 0, 'Collar moment positivity')
            require(abs(mean_delta-3*h) < mp.mpf('1.5'), 'Alternative mean scale')
            require(abs(variance_delta-3) < mp.mpf('1'), 'Alternative variance scale')
            if ell == 16:
                score = lambda x: -3+2/(1-x*x)
                density = lambda x: a*(A-x*x)
                knots = [0, c/2, mp.mpf('0.9')*c,
                         c-100*q, c-10*q, c-q, c]
                knots = sorted(set(x for x in knots if 0 <= x <= c))
                numerical_mean = 2*mp.quad(lambda x: score(x)*density(x), knots)
                numerical_second = 2*mp.quad(lambda x: score(x)**2*density(x), knots)
                error = max(abs(mean_mark-numerical_mean),
                            abs(second_mark-numerical_second))
                worst_identity_error = max(worst_identity_error, error)
                require(error < mp.mpf('1e-65'), 'Antiderivative/quadrature disagreement')
            rows.append({'ell': ell, 'h': h, 'mean_Delta': number(mean_delta),
                         'mean_limit': str(3*h), 'variance_Delta': number(variance_delta),
                         'variance_limit': '3', 'effective_k_times_collar_mass': number(k*collar_mass)})
    for h in (-1, 0, 1):
        sequence = [row for row in rows if row['h'] == h]
        require(all(mp.mpf(row['effective_k_times_collar_mass']) <=
                    3/mp.sqrt(row['ell']) for row in sequence), 'Uniform collar mass bound')
        require(abs(mp.mpf(sequence[-1]['mean_Delta'])-3*h) < mp.mpf('0.15'),
                'Final alternative mean check')
        require(abs(mp.mpf(sequence[-1]['variance_Delta'])-3) < mp.mpf('0.12'),
                'Final alternative variance check')
    return {'scope': 'Finite high-precision effective-intensity controls, not sampling or a LAN proof',
            'max_antiderivative_quadrature_discrepancy': number(worst_identity_error),
            'rows': rows}


def ceil_fraction(x: Fraction) -> int:
    return -((-x.numerator)//x.denominator)


def pilot_controls() -> dict:
    cases = 0
    lo, hi = Fraction(1, 3), Fraction(7, 3)
    for j in (2, 4, 100, 10000):
        for step in (Fraction(1, 10), Fraction(1, 100), Fraction(1, 997)):
            L = ceil_fraction(j*(hi-lo)/step)+2
            for weight in (Fraction(0), Fraction(1, 997), Fraction(1, 3),
                           Fraction(1, 2), Fraction(996, 997), Fraction(1)):
                g = lo+(hi-lo)*weight
                index = ceil_fraction((j*g+step-j*lo)/step)
                time = j*lo+index*step
                require(0 <= index <= L, 'Pilot grid coverage')
                require(step <= time-j*g < 2*step, 'Pilot near-onset grid interval')
                # Every earlier success lies in (jg, this time]; test exact
                # endpoint and interior representatives of that interval.
                for excess in (step/Fraction(10000), step, time-j*g):
                    estimate = (j*g+excess-step)/j
                    require(j*abs(estimate-g) <= step, 'Final-flight centering bound')
                    cases += 1
    return {'exact_rational_centering_cases': cases,
            'flight_numbers': [2, 4, 100, 10000],
            'scope': 'Grid coverage and j-scaled centering only; not billiard flux/localization'}


def finite_compact_negative_control() -> dict:
    # K=[0,1], Q_t=delta_0; P_{n,t}=delta_1 at t=1/(n+1), delta_0 otherwise.
    # A reverse kernel chooses Bernoulli(q), and its worst error is max(q,1-q).
    values = [(Fraction(i, 1000), max(Fraction(i, 1000), 1-Fraction(i, 1000)))
              for i in range(1001)]
    minimizer, value = min(values, key=lambda pair: pair[1])
    require(minimizer == Fraction(1, 2) and value == Fraction(1, 2),
            'Finite-grid reverse-deficiency control')
    # Exact proof for all q: max(q,1-q)>=1/2, with equality at q=1/2.
    return {'finite_restrictions': 'Every fixed finite subset agrees with Q eventually',
            'full_Le_Cam_distance': '1/2', 'arbitrarily_small_radius_TV_modulus': '1',
            'scope': 'Negative control explaining why the modulus is needed; NOT a counterexample to the manuscript, which proves a modulus'}


def main() -> None:
    result = {'status': 'passed', 'submission': SUBMISSION,
              'python': platform.python_version(), 'mpmath': mp.__version__,
              'decimal_precision': mp.mp.dps,
              'native_build_performed': False, 'manuscript_source_imported': False,
              'pdf_pages_inspected': 0,
              'boundary_Hellinger': boundary_controls(),
              'original_alternative_collar': collar_controls(),
              'pilot_grid': pilot_controls(),
              'finite_vs_compact': finite_compact_negative_control()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
