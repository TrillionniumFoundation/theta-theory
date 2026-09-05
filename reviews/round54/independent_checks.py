"""Round 54 finite checks of the frozen Round 53 submission.

Successful execution means the stated checks AND two exact-arithmetic
contract witnesses were reproduced. It is not certification of the author
implementation or a proof of the infinite-dimensional theorems.
"""
from __future__ import annotations
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
from math import factorial, log, log10, sqrt, e
from pathlib import Path
import hashlib
import json
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import round51_certificates as core
from tools import round53_certificates as c

REVIEWED_COMMIT = '7f1bc9a42ba27615aea61afb9a417ef076e2c6e1'
EXPECTED = {
    'tools/round51_certificates.py': '6eda73359c1999027394062f2edb1532e0bed21f',
    'tools/round53_certificates.py': '6a80f4fb264ab29958ebc3f6ea1ab5c2a06e62fb',
    'tests/test_round53.py': '5fd6b0f474eec22b9a6a3be589ff9dd3f3aeef83',
}
COUNTS: dict[str, int] = {}


def check(group: str, condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(f'{group}: {message}')
    COUNTS[group] = COUNTS.get(group, 0) + 1


def source_checks() -> dict:
    out = {}
    for name, expected in EXPECTED.items():
        data = (ROOT / name).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        check('source_identity', blob == expected, name)
        out[name] = {'git_blob': blob, 'sha256': hashlib.sha256(data).hexdigest(),
                     'bytes': len(data)}
    return out


def local_mathematical_checks() -> None:
    box = c.ModelBox((1, 2), (F(1, 2), 1), (3, 4), 1)
    for J, den, rho, w in product((0, 1), (2048, 4096),
                                  (F(0), F(1, 2)), (F(0), F(1, 4))):
        spec = c.CertificateSpec(box, J, F(1, 8), F(1, den), rho, w)
        cert = c.certificate(spec)
        check('clock', cert.L * cert.E <= spec.delta / 2, 'remainder budget')
        check('clock', cert.N == cert.R or cert.L * cert.E / cert.tau > spec.delta / 2,
              'minimal order')
        check('clock', 0 < cert.tau <= F(2, 63), 'actual clock ratio')
        check('clock', 12 * cert.Delta * cert.tau / (1 - cert.tau) <= 1, 'tail prefactor')
    for m in range(1, 6):
        response = [F((-1)**k * (k + 1), 7) for k in range(m)]
        intercept = [F(k - 2, 5) for k in range(m)]
        amplitude = F(3, 2)
        average = sum(sum((intercept[k] + amplitude * sum(
            signs[j] * response[k-j] for j in range(k+1)))**2
            for k in range(m)) for signs in product((-1, 1), repeat=m)) / (2**m)
        target = sum(v*v for v in intercept) + amplitude**2 * sum(
            (m-k)*v*v for k, v in enumerate(response))
        check('all_sign_energy', average == target, 'orthogonality identity')
    for J in range(4):
        n = J + 4
        diagonal, edges = [F(3)] * n, [F(1, 2)] * (n-1)
        jets = core.boundary_jets(F(1), diagonal, edges, 4*J+8)
        changed = list(diagonal)
        changed[J] += F(1, 5)
        other = core.boundary_jets(F(1), changed, edges, 4*J+8)
        first = next(k for k, (x, y) in enumerate(zip(jets, other)) if x != y)
        check('jet_locality', first == 4*J+4, 'first changed diagonal jet')
        changed_edges = list(edges)
        changed_edges[J] += F(1, 10)
        other = core.boundary_jets(F(1), diagonal, changed_edges, 4*J+8)
        first = next(k for k, (x, y) in enumerate(zip(jets, other)) if x != y)
        check('jet_locality', first == 4*J+6, 'first changed edge jet')
        mu = core.moments_from_jets(jets, 2*J+2)
        check('moment_inverse', mu == core.jacobi_moments(diagonal, edges, 2*J+2),
              'damped moment identity')
        diag, edges2 = core.recover_jacobi(mu, J)
        check('moment_inverse', diag == diagonal[:J+1], 'labeled diagonals')
        check('moment_inverse', edges2 == [a*a for a in edges[:J+1]], 'squared edges')
    for d, f in product((F(-7), F(-1, 3), F(0), F(2, 5)),
                         (F(-9), F(-1, 2), F(0), F(3))):
        check('energy_transfer', abs(d*f) <= f*f/16 + 4*d*d, 'Young inequality')
    check('energy_transfer', -F(3, 8)*F(15, 32)+F(1, 64) == -F(41, 256), 'numerator')
    check('energy_transfer', -F(5, 8)*F(1, 16)-F(1, 64) == -F(7, 128), 'denominator')
    check('energy_transfer', -F(41, 256)+F(7, 128) == -F(27, 256), 'ratio')
    check('energy_transfer', -F(27, 256)+F(8, 1024)+F(2, 64) <= -F(1, 16), 'budget')
    for M in range(1, 9):
        signs = [F((-1)**k) for k in range(M)]
        amplitude, drift_level = F(3, 2), F(2, 7)
        drift = [drift_level*s for s in signs]
        bias = sum(s*d for s, d in zip(signs, drift)) / (amplitude*M)
        D = sum(d*d for d in drift)
        check('robust_response', bias*bias == D/(amplitude**2*M),
              'sign-correlated Cauchy-Schwarz saturation')
    check('robust_response', F(3, 4)+F(1, 4) == 1, 'physical error split')
    check('robust_response', 2*F(1, 32) == F(1, 4)**2, 'D <= information/32')
    check('robust_response', F(4, 12**2*4) == F(1, 144), 'tail exponent constant')


def arithmetic_witness() -> dict:
    box = c.ModelBox((1, 2), (F(1, 2), 1), (3, 4), 1)
    spec = c.CertificateSpec(box, 0, F(1, 8), F(1, 2048), F(1, 2), F(1, 4096))
    cert = c.certificate(spec)
    mixed = replace(cert, A=float(cert.A))
    c.validate_certificate(mixed)
    check('arithmetic_witness', type(mixed.A) is float and mixed == cert,
          'numeric equality accepts a floating derived field')
    rstar = (spec.delta/cert.L-cert.E)/(2*cert.A)
    radius = rstar*(1+F(1, 10**16))
    exact_bound = cert.L*(2*cert.A*radius+cert.E)
    floating_bound = mixed.L*(2*mixed.A*radius+mixed.E)
    exact_ok = c.radius_budget_satisfied([radius]*cert.m, cert)
    floating_ok = c.radius_budget_satisfied([radius]*cert.m, mixed)
    check('arithmetic_witness', exact_bound > spec.delta and not exact_ok, 'exact rejection')
    check('arithmetic_witness', floating_ok and floating_bound == 0.125, 'false budget acceptance')
    check('arithmetic_witness', exact_bound-spec.delta == (spec.delta-cert.L*cert.E)/10**16,
          'exact positive overage identity')
    return {'N': cert.N, 'A_power_of_two': cert.A.numerator.bit_length()-1,
            'relative_radius_increment': '1/10^16', 'validator_accepted_float': True,
            'exact_predicate': exact_ok, 'floating_predicate': floating_ok,
            'exact_bound_gt_delta': True, 'floating_bound': floating_bound,
            'overage_identity': '(delta-L*E)/10^16 > 0'}


def endpoint_witness() -> dict:
    h = F(1, 10**180)
    box = c.ModelBox((1-h, 1+h), (F(1, 2)-h, F(1, 2)+h), (3-h, 3+h), 1)
    spec = c.CertificateSpec(box, 0, F(1, 8), F(1, 2048), F(1, 2), F(1, 4096))
    cert = c.certificate(spec)
    mixed = replace(cert, A=float(cert.A))
    c.validate_certificate(mixed)
    grid, K, P = c.pulse_grid(cert), 80, 80
    errors = core.outer_errors(box, max(t for row in grid for _, t in row), K, h, P)
    rstar = (spec.delta/cert.L-cert.E)/(2*cert.A)
    radius = rstar*(1+F(1, 10**16))
    jets = core.boundary_jets(F(1), [F(3)]*(K+1), [F(1, 2)]*K, P+1)
    def val(t: F) -> F:
        return sum(jets[k+1]*t**(k+1)/factorial(k+1) for k in range(P+1))
    bands = []
    for row in grid:
        center = sum(a*val(t) for a, t in row)
        error = sum(abs(a) for a, _ in row)*sum(errors.values())
        statistical_radius = radius-2*error
        check('endpoint_band_coverage', statistical_radius > error > 0,
              'bands cover the narrow full box')
        band = (center-statistical_radius, center+statistical_radius)
        bands.append((band, band, F(0)))
    exact = c.certify_outer(box, 0, K, h, P, grid, bands, cert, max_boxes=1)
    floating = c.certify_outer(box, 0, K, h, P, grid, bands, mixed, max_boxes=1)
    check('endpoint_witness', exact.complete and floating.complete, 'complete enumerations')
    check('endpoint_witness', exact.full_boxes == floating.full_boxes and len(exact.full_boxes) == 1,
          'same nonempty full-box union')
    check('endpoint_witness', exact.outer_radii == (radius,)*cert.m, 'bound radii')
    check('endpoint_witness', exact.status == 'enclosed' and exact.diameter_upper_bound > spec.delta,
          'exact endpoint correctly refuses the sufficient budget')
    check('endpoint_witness', floating.status == 'certified' and floating.diameter_upper_bound == 0.125,
          'floating endpoint accepts the same over-budget instance')
    check('endpoint_witness', type(floating.diameter_upper_bound) is float,
          'loss of exact arithmetic in returned bound')
    actual_diameter = max(hi-lo for prefix in floating.prefix_boxes for lo, hi in prefix)
    check('endpoint_witness', actual_diameter == 2*h < spec.delta,
          'qualification: NOT a physical-diameter counterexample')
    return {'N': cert.N, 'A_power_of_two': cert.A.numerator.bit_length()-1,
            'mesh_radius': '1/10^180', 'K': K, 'P': P,
            'boxes_visited_each': 1, 'retained_each': 1, 'same_full_boxes': True,
            'exact_status': exact.status, 'floating_status': floating.status,
            'exact_bound_gt_delta': True, 'floating_bound': floating.diameter_upper_bound,
            'floating_bound_type': type(floating.diameter_upper_bound).__name__,
            'actual_prefix_diameter': '2/10^180', 'actual_prefix_diameter_lt_delta': True,
            'scope': 'False exact-budget acceptance; not a counterexample to actual diameter or analytic theorem'}


def numerical_calibration() -> dict:
    box = c.ModelBox((1, 2), (F(1, 2), 1), (3, 4), 1)
    spec = c.CertificateSpec(box, 0, F(1, 8), F(1, 2048), F(1, 2), F(1, 4096))
    cert = c.certificate(spec)
    d0, ell = log(1/cert.Delta), log(1/cert.tau)
    Ktau = 12+(log(2)+25*log(box.Q)+8*d0)/ell
    Hp = log(1/cert.p)+log(16)
    Ctau = log(256)+50*log(box.Q)+16*d0+Ktau*Hp
    ptau = 2+Hp/ell
    kminus, B0 = float(box.b[0]-2*box.a[1]), float(box.b[1]+2*box.a[1])
    eps = min(1, float(box.c[0])/2, sqrt(kminus)/2)
    ME = max(.75, B0/2+eps**2+eps*float(box.c[1])/2)
    de = min(float(box.c[0])/2, eps*kminus)
    lam = de/(2*ME)
    theta = min(log(2), lam/(8*e*float(box.Lambda)))
    return {'scope': 'Floating descriptive evaluations only; not certified quantities or sample lower bounds',
            'C_tau': Ctau, 'p_tau': ptau, 'inner_r_intercept': 1/Ctau,
            'outer_r_intercept': 1/(8*theta),
            'log10_inverse_kappa': log10(cert.kappa.denominator)-log10(cert.kappa.numerator)}


def main() -> None:
    start = time.monotonic()
    identities = source_checks()
    local_mathematical_checks()
    witness_a = arithmetic_witness()
    witness_b = endpoint_witness()
    result = {'reviewed_commit': REVIEWED_COMMIT, 'python': platform.python_version(),
              'source_identities': identities, 'finite_checks_by_group': COUNTS,
              'finite_checks_total': sum(COUNTS.values()), 'all_assertions_passed': True,
              'contract_witnesses_reproduced': 2, 'arithmetic_witness': witness_a,
              'endpoint_witness': witness_b, 'numerical_calibration': numerical_calibration(),
              'elapsed_seconds': round(time.monotonic()-start, 3),
              'scope': 'Finite checks and reproduced defects, not formal verification, a PDF build, or posterior simulation'}
    path = ROOT/'reviews/round54/INDEPENDENT_CHECKS.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
