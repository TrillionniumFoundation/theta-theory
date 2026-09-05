#!/usr/bin/env python3
"""Round 52 finite audit of frozen Round 51; not a theorem prover.

Run from an ordinary checkout: python reviews/round52/independent_checks.py
A successful exit means the regression checks passed AND the three documented
unsafe-certification witnesses were reproduced. It does NOT certify the API.
"""
from __future__ import annotations
import hashlib
import json
import platform
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import round51_certificates as c

FROZEN = 'f991a17a5d99bf0cce9f1e457df91097e69dcd8a'
EXPECTED = {
    'tools/round51_certificates.py': '6eda73359c1999027394062f2edb1532e0bed21f',
    'tests/test_round51.py': '2a6999afad296310a633d77c81a96950e45cf4d5',
}
BOX = c.ModelBox((F(1), F(2)), (F(1, 2), F(1)), (F(3), F(4)), F(1))


def run() -> dict:
    groups = {}
    identities = {}
    for name, expected in EXPECTED.items():
        raw = (ROOT / name).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert blob == expected, (name, blob, expected)
        identities[name] = dict(git_blob=blob, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
    groups['frozen_source_identity'] = len(identities)

    count = 0
    for m in range(1, 8):
        ds = [F((-1)**k, k+2) for k in range(m)]
        base = [F(2*k+1, 11) for k in range(m)]
        a = F(3, 5)
        lhs = sum(sum((base[k] + a*sum(s[j]*ds[k-j] for j in range(k+1)))**2
                      for k in range(m)) for s in product((-1, 1), repeat=m)) / 2**m
        rhs = sum(x*x for x in base) + a*a*sum((m-k)*ds[k]**2 for k in range(m))
        assert lhs == rhs
        count += 1
    groups['all_sign_block_energy'] = count

    _, rows = c.sampled_coefficients(F(1, 1024), 8, 16)
    for row in rows:
        weights = [F(17-k) for k in range(17)]
        dual = sum(x*x/w for x, w in zip(row, weights))
        ds = [x/w for x, w in zip(row, weights)]
        assert sum(x*y for x, y in zip(row, ds))**2 == dual*sum(w*y*y for w, y in zip(weights, ds))
    groups['weighted_cauchy_equality'] = len(rows)

    count = 0
    for J in range(7):
        n = J+3
        diagonal, edges = [F(7, 2)]*n, [F(3, 4)]*(n-1)
        for kind, order in [('diagonal', 4*J+4), ('edge', 4*J+6)]:
            dd, ee = list(diagonal), list(edges)
            change = F(1, 11)
            if kind == 'diagonal':
                dd[J] += change
                expected = -change * F(9, 16)**J
            else:
                ee[J] += change
                expected = ((F(3, 4)+change)**2-F(9, 16))*F(9, 16)**J
            lhs = c.boundary_jets(F(5, 4), diagonal, edges, order)
            rhs = c.boundary_jets(F(5, 4), dd, ee, order)
            assert lhs[:order] == rhs[:order]
            assert rhs[order]-lhs[order] == expected
            count += 1
    groups['first_changed_physical_jets'] = count

    for K in range(1, 6):
        full = c.boundary_jets(F(3, 2), [F(7, 2)]*(K+3), [F(3, 4)]*(K+2), 4*K+6)
        cut = c.boundary_jets(F(3, 2), [F(7, 2)]*(K+1), [F(3, 4)]*K, 4*K+6)
        assert full[:-1] == cut[:-1]
        assert full[-1]-cut[-1] == F(9, 16)**(K+1)
    groups['finite_section_word_locality'] = 5

    count = 0
    for J in range(5):
        n = J+4
        dd = [F(3)+F(k, n+2) for k in range(n)]
        ee = [F(1, 2)+F(k, 8*n) for k in range(n-1)]
        for damping in [F(1), F(5, 4), F(7, 4)]:
            order = 2*J+2
            mu = c.jacobi_moments(dd, ee, order)
            jets = c.boundary_jets(damping, dd, ee, 2*order+2)
            assert c.moments_from_jets(jets, order) == mu
            diag, edges2 = c.recover_jacobi(mu, J)
            assert diag == dd[:J+1] and edges2 == [x*x for x in ee[:J+1]]
            count += 1
    groups['damped_moment_reconstruction'] = count

    count = 0
    for rho, w, m in product([F(1, 4), F(1, 2), F(1)], [F(1, 4096), F(1, 3), F(1)], [1, 3, 11]):
        p = c.success_probability(rho, w)
        assert p == 1-rho+rho*w and p**m >= (rho*w)**m
        count += 1
    groups['enlarged_event_probability'] = count

    cert = c.certificate(BOX, 0, F(1, 8), F(1, 2048), F(1, 2), F(1, 4096))
    assert (cert['N'], cert['m']) == (60, 61)
    assert cert['L']*cert['E'] <= F(1, 16) < 16*cert['L']*cert['E']
    assert -F(97, 512)+F(13, 256)+F(1, 32) == -F(55, 512) <= -F(1, 16)
    assert 12*F(1, 16)/(1-F(1, 16)) == F(4, 5)
    groups['sampled_remainder_and_posterior_arithmetic'] = 3

    for denominator in [64, 128, 256, 512, 1024]:
        x = F(1, denominator)
        Delta = x/BOX.Lambda
        tau = 2*x/(1-x)
        assert 0 < tau < F(1, 16) and 12*Delta*tau/(1-tau) <= 1
    groups['sharper_clock_tail_prefactor'] = 5

    tiny = F(1, 10**7)
    try:
        c.validate_band((-tiny, tiny), (-F(1), F(1)), F(0))
    except c.RepresentationError:
        pass
    else:
        raise AssertionError('Unbudgeted representation inflation accepted')
    try:
        c.outer_boxes(BOX, 0, 2, F(1, 1000), 4, [[(F(1), F(1, 100))]],
                      [((-F(1), F(1)), (-F(1), F(1)), F(0))], max_boxes=1)
    except c.ResourceLimit:
        pass
    else:
        raise AssertionError('Exhaustive resource preflight failed')
    groups['repaired_representation_and_resource_guards'] = 2

    witnesses = []
    t = F(1, 10**100)
    # Universal bound: |h(t)| <= Lambda*exp(Lambda*t)*t^2/2 <= 27*t^2/2.
    # Lambda=9, Lambda*t<1 and exp(1)<3. Thus this band contains every truth.
    radius = F(27, 2)*t*t
    for name, obs, reference in [
        ('zero_observable', [[(F(0), F(1, 100))]], (F(0), F(0))),
        ('one_nonzero_wrong_time', [[(F(1), t)]], (-radius, radius)),
        ('m_nonzero_duplicated_wrong_times', [[(F(1), t)]]*cert['m'], (-radius, radius)),
    ]:
        bands = [(reference, reference, F(0)) for _ in obs]
        result = c.outer_boxes(BOX, 0, 1, F(1), 2, obs, bands, max_boxes=1)
        assert result['complete'] and result['boxes_visited'] == 1 and len(result['retained']) == 1
        prefix = result['retained'][0]['prefix']
        actual_diameter = max(hi-lo for lo, hi in prefix)
        answer = c.diameter_certified(result['outer_radii'], cert, F(1, 8))
        assert answer is True and actual_diameter == 1 and actual_diameter > F(1, 8)
        witnesses.append(dict(name=name, observables=len(obs), required_lags=cert['m'],
                              reported_diameter_certified=answer, target='1/8', actual_prefix_diameter='1',
                              all_box_parameters_feasible=True, witness_reproduced=True))
    return dict(schema=1, frozen_commit=FROZEN, python=platform.python_version(),
                identities=identities, regression_groups=groups,
                regression_group_count=len(groups), regression_case_count=sum(groups.values()),
                regressions_passed=True, adversarial_witnesses=witnesses,
                meaning='Successful execution reproduces unsafe unbound certification; not software correctness.',
                formal_proof_verification=False, full_source_verifier_executed=False, tex_build_executed=False)


if __name__ == '__main__':
    result = run()
    result['audit_script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path = ROOT / 'reviews/round52/INDEPENDENT_CHECKS.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
