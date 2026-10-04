#!/usr/bin/env python3
"""Finite exact regression for the full biased binary-measurement code.

These checks exercise exact algebra, legal matrices, error-budget consequences
and target-bound replay. They do not certify an adaptive supremum, a continuum
covering theorem, an asymptotic lower bound, or a literature-priority assertion.
"""
from __future__ import annotations
import copy
from fractions import Fraction as F
import json
from math import comb
from pathlib import Path
import subprocess
import sys
import tempfile

import biased_codec as c
from choi_streaming import Instrument


def binomial(n: int, p: F) -> list[F]:
    return [F(comb(n, j))*p**j*(1-p)**(n-j) for j in range(n+1)]


def binomial_distance(n: int, p: F, q: F) -> F:
    return sum(abs(a-b) for a, b in zip(binomial(n, p), binomial(n, q)))


def sqrt_sum_compare(a: F, b: F, z: F) -> int:
    """Independent sign of sqrt(a)+sqrt(b)-z for nonnegative a,b."""
    if z < 0:
        return 1
    t = z*z-a-b
    if t < 0:
        return 1
    return c.sign(4*a*b-t*t)


def endpoint_interval(j: int, B: int) -> tuple[F, F]:
    """Closed probability interval of one nearest-chart digit, with both ties.

    This checks interval membership independently of encoder binary search.
    The middle word includes the adjoining halves of both charts.
    """
    def f(t):
        return t*t/(1+t*t)
    if j == B:
        z = f(F(2*B-1, 2*B))
        return z, 1-z
    k = j if j < B else 2*B-j
    lo = f(max(F(0), F(2*k-1, 2*B)))
    hi = f(min(F(1), F(2*k+1, 2*B)))
    return (lo, hi) if j < B else (1-hi, 1-lo)


def run() -> dict:
    count = 0
    controls = []
    cases = {'radical_comparisons': 0, 'binomial': 0, 'gauge_overlap': 0, 'spectral_intervals': 0,
             'codec': 0, 'legal_words': 0, 'cli': 0}
    capacities = []

    def check(ok, message):
        nonlocal count
        count += 1
        if not ok:
            raise RuntimeError(message)

    def reject(name, fn):
        try:
            fn()
        except (ValueError, TypeError, KeyError, IndexError):
            controls.append(name)
            return
        raise RuntimeError('negative control accepted: '+name)

    # Perfect-square and signed-threshold checks independently catch an
    # illicit squaring step, including negative thresholds and exact equality.
    for r in [F(0), F(1, 7), F(1, 2), F(1), F(7, 3)]:
        for z in [F(-3), -r, F(-1, 7), F(0), F(1, 7), r, F(3)]:
            for s in (-1, 1):
                check(c.radical_sign(z, s, r*r) == c.sign(z+s*r), 'signed radical comparison')
                cases['radical_comparisons'] += 1
    for Q, z, expected in [(F(2), F(-1), 1), (F(2), F(-3, 2), -1),
                           (F(1, 3), F(-1, 2), 1), (F(1, 3), F(-3, 5), -1)]:
        check(c.radical_sign(z, 1, Q) == expected, 'nonsquare radical comparison')
        cases['radical_comparisons'] += 1
    for a in [F(0), F(1, 7), F(1, 2), F(1)]:
        for b in [F(0), F(1, 3), F(1)]:
            for z in [F(-1), F(0), a+b, F(3)]:
                check(sqrt_sum_compare(a*a, b*b, z) == c.sign(a+b-z), 'independent radical-sum comparator')

    # Exact finite Bernoulli product distances, checked against their
    # Hellinger upper bound after algebraic elimination of both radicals.
    for N in [1, 2, 3, 7, 16, 31]:
        for p in [F(0), F(1, 1000), F(1, 10), F(1, 2), F(9, 10), F(1)]:
            for q in [p, (p+1)/2, F(1)]:
                D = binomial_distance(N, p, q)
                threshold = 1-D*D/(8*N)
                check(sqrt_sum_compare(p*q, (1-p)*(1-q), threshold) <= 0,
                      'Bernoulli product Hellinger bound')
                T2 = F(N)*(p-q)**2/(max(p*(1-p), q*(1-q))+F(1, N))
                check(D*D >= min(F(1), T2)/4096, 'two-endpoint spectral lower constant')
                check(D*D <= 9*T2, 'two-endpoint spectral upper constant')
                check(0 <= D <= 2, 'unhalved distance convention')
                cases['binomial'] += 1

    # Scalar-overlap proof arithmetic with rational spectral square roots.
    # Multiplying the environment gauge by D avoids any irrational matrix
    # entries: D cos(phi)=f cos(t), D sin(phi)=sin(t). These checks include
    # biased interiors, both rank-one faces, and a repeated eigenvalue.
    def mm(a, b):
        return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

    def add(a, b):
        return [[a[i][j]+b[i][j] for j in range(2)] for i in range(2)]

    def diag(a, b):
        return [[a, F(0)], [F(0), b]]

    spectral_roots = [
        ((F(4, 5), F(3, 5)), (F(3, 5), F(4, 5))),
        ((F(12, 13), F(5, 13)), (F(3, 5), F(4, 5))),
        ((F(3, 5), F(4, 5)), (F(5, 13), F(12, 13))),
        ((F(1), F(0)), (F(5, 13), F(12, 13))),
        ((F(4, 5), F(3, 5)), (F(0), F(1))),
        ((F(3, 5), F(4, 5)), (F(3, 5), F(4, 5)))
    ]
    rotations = [(F(1), F(0)), (F(4, 5), F(3, 5)), (F(3, 5), F(4, 5)),
                 (F(12, 13), F(5, 13)), (F(5, 13), F(12, 13)), (F(0), F(1))]
    for (sp, sp0), (sq, sq0) in spectral_roots:
        p, q = sp*sp, sq*sq
        f = sp*sq+sp0*sq0
        A = sp*sp0+sq*sq0
        T = sp*sq0+sq*sp0
        r = p-q
        check(sp*sp+sp0*sp0 == 1 and sq*sq+sq0*sq0 == 1 and p >= q,
              'rational spectral square roots')
        for ct, st in rotations:
            check(ct*ct+st*st == 1, 'rational unit rotation')
            D2 = f*f*ct*ct+st*st
            gauge_D = [[f*ct, -st], [st, f*ct]]
            gauge_DT = [[f*ct, st], [-st, f*ct]]
            check(mm(gauge_DT, gauge_D) == diag(D2, D2), 'scaled gauge orthogonality')
            first = mm(mm(diag(sp, sq), gauge_D), diag(sp, sq))
            second = mm(mm(diag(sp0, sq0), gauge_D), diag(sp0, sq0))
            overlap_D = mm(add(first, second), [[ct, st], [-st, ct]])
            check(overlap_D == diag(f, f), 'scalar gauge matrix overlap')
            check(f*T == A, 'overlap spectral identity fT=A')
            check((1-f*f)*T*T == r*r, 'overlap spectral identity for gap')
            check(f*f/D2 == A*A/(A*A+r*r*st*st), 'exact scalar-overlap square formula')
            check(0 <= f*f/D2 <= 1, 'scalar overlap lies in unit interval')
            cases['gauge_overlap'] += 1

    # Full-endpoint scalar grids, including monotonicity across the chart seam.
    for B in [1, 2, 7, 32]:
        ps = [c.probability(j, B) for j in range(2*B+1)]
        check(ps[0] == 0 and ps[B] == F(1, 2) and ps[-1] == 1, 'spectral endpoints')
        check(all(a < b for a, b in zip(ps, ps[1:])), 'strictly increasing endpoint grid')
        check(all(ps[j]+ps[-1-j] == 1 for j in range(2*B+1)), 'complement symmetry')
        for p in [F(j, 128) for j in range(129)]:
            j = c.spectral_digit(2*p, F(0), 1, B)
            lo, hi = endpoint_interval(j, B)
            check(lo <= p <= hi, 'nearest chart interval')
            cases['spectral_intervals'] += 1
        for j, p in enumerate(ps):
            check(c.spectral_digit(2*p, F(0), 1, B) == j, 'exact gridpoint roundtrip')
    check(c.spectral_digit(F(2, 5), F(0), 1, 1) == 0, 'lower chart midpoint tie')
    check(c.spectral_digit(F(8, 5), F(0), 1, 1) == 2, 'upper chart midpoint tie')

    targets = {
        2: [('0', ['0', '0']), ('1', ['0', '0']), ('-1', ['0', '0']),
            ('1/3', ['0', '0']), ('0', ['3/5', '4/5']),
            ('1/5', ['1/2', '1/3']), ('-1/5', ['-1/2', '1/3']),
            ('1/2', ['3/10', '2/5']), ('-1/2', ['0', '-1/2']),
            ('999/1000', ['1/1000', '0']),
            ('1/10', ['1/100000', '-1/200000'])],
        3: [('0', ['0', '0', '0']), ('1', ['0', '0', '0']), ('-1', ['0', '0', '0']),
            ('-2/3', ['0', '0', '0']), ('0', ['2/3', '2/3', '1/3']),
            ('1/5', ['1/2', '1/3', '1/5']), ('-1/5', ['-1/2', '1/3', '-1/5']),
            ('1/2', ['1/3', '1/3', '1/6']), ('-1/2', ['0', '0', '-1/2']),
            ('-999/1000', ['0', '1/1000', '0']),
            ('1/10', ['1/100000', '-1/200000', '1/300000'])]
    }
    for N, error in [(1, F(1, 4)), (2, F(1, 8)), (7, F(1, 16))]:
        for d in (2, 3):
            B, ps, rows = c.layout(N, error, d)
            capacities.append({'dimension': d, 'horizon': N, 'error': str(error),
                               'spectral_grid': B, 'codeword_count': str(rows[-1]),
                               'fixed_length_bits': (rows[-1]-1).bit_length()})
            check(F(B*B) >= 64*N/error**2, 'spectral error budget')
            check(rows[0] == 0 and len(rows) == 2*B+2, 'row indexing')
            check(rows[1] == 1, 'zero effect is a singleton')
            check(c.scale_squared(N, F(1), F(0)) == N*N, 'projective angular scale')
            check(c.scale_squared(N, F(1, 2), F(1, 2)) == 0, 'scalar angular scale')
            # First/middle/last words on representative rows and exact
            # endpoint strata; no random sampling or floating point is used.
            for i in sorted({0, 1, B, max(0, 2*B-1), 2*B}):
                js = sorted({0, i//2, i})
                offset = rows[i]
                k = 0
                for j in js:
                    while k < j:
                        offset += c.layer_size(N, error, d, ps[i], ps[k])
                        k += 1
                    size = c.layer_size(N, error, d, ps[i], ps[j])
                    for local in sorted({0, size//2, size-1}):
                        code = c.header(N, error, d, offset+local)
                        p, q, u = c.unpack(code)
                        b, x = c.decode_coordinates(code)
                        inst = c.decode(code)
                        check(p == ps[i] and q == ps[j], 'triangular index inversion')
                        check(sum(v*v for v in x) == (p-q)**2, 'exact decoded contrast')
                        check(b == p+q-1, 'exact decoded bias')
                        check(inst.d == 2 and inst.n == 1 and len(inst.outcomes) == 2, 'ordered binary interface')
                        for mat, det0, tr0 in zip(inst.outcomes,
                                                  [p*q, (1-p)*(1-q)], [p+q, 2-p-q]):
                            a = F(mat[0][0][0], inst.denominator)
                            z = mat[0][1]
                            e = F(mat[1][1][0], inst.denominator)
                            det = a*e-F(z[0]**2+z[1]**2, inst.denominator**2)
                            check(det == det0 and det >= 0, 'exact effect determinant')
                            check(a+e == tr0 and a >= 0 and e >= 0, 'exact effect trace and diagonal')
                        check(Instrument.from_dict(inst.to_dict()).to_dict() == inst.to_dict(),
                              'legal Choi serialize/parse roundtrip')
                        cases['legal_words'] += 1
            for b0, vector in targets[d]:
                raw = {'schema': c.TARGET, 'bias': b0, 'bloch_vector': vector}
                b, x = c.target(raw)
                Q = sum(t*t for t in x)
                code = c.encode(raw, N, error)
                check(c.verify(raw, code), 'canonical target replay')
                check(c.loads(c.canonical(code)) == code, 'canonical code JSON roundtrip')
                p, q, u = c.unpack(code)
                i = ps.index(p)
                j = ps.index(q)
                for digit, s in [(i, 1), (j, -1)]:
                    lo, hi = endpoint_interval(digit, B)
                    check(c.endpoint_compare(1+b, Q, s, lo) >= 0
                          and c.endpoint_compare(1+b, Q, s, hi) <= 0,
                          'irrational endpoint in exact quantization interval')
                check(4*F(N, B*B) <= error**2/16, 'radial adaptive budget squared')
                if i != j:
                    A = c.angular_grid(N, error, d, p, q)
                    dot = sum(a*z for a, z in zip(x, u))
                    threshold = 1-F(d-1, 2*A*A)
                    check(dot >= 0 and dot*dot >= threshold*threshold*Q,
                          'independent exact unit-direction chord bound')
                    check(8*c.scale_squared(N, p, q)*F(d-1, A*A) <= error**2/16,
                          'angular adaptive budget squared')
                else:
                    check(u == (F(0),)*d, 'scalar word has no direction payload')
                check(F(code['adaptive_error_upper']) == error/2, 'combined adaptive budget')
                check(code['fixed_length_bits'] == (int(code['codeword_count'])-1).bit_length(),
                      'all coordinates charged in fixed-length alphabet')
                cases['codec'] += 1

    # Pauli-Y fixes the transposition convention independently of determinants.
    inst = c.measurement(F(1, 5), (F(0), F(2, 5), F(0)))
    plus_i = [[(F(1, 2), F(0)), (F(0), F(-1, 2))],
              [(F(0), F(1, 2)), (F(1, 2), F(0))]]
    # Instrument.branch acts on integer Choi numerators; divide by the
    # advertised denominator to obtain the physical branch probability.
    check(inst.branch(plus_i, 0) == [[(F(4*inst.denominator, 5), F(0))]], 'Pauli-Y plus probability')
    check(inst.branch(plus_i, 1) == [[(F(inst.denominator, 5), F(0))]], 'Pauli-Y minus probability')

    # Very large N and small delta are checked without enumerating their
    # pseudo-polynomial alphabet. These are arithmetic parameter checks only.
    for N, error in [(10**6, F(1, 10**6)), (1, F(1, 10**12))]:
        B = c.radial_grid(N, error)
        check(B*B >= 64*N/error**2 and (B-1)**2 < 64*N/error**2, 'large exact spectral grid')
        A = c.angular_grid(N, error, 3, F(1), F(0))
        check(A*A >= 256*N*N/error**2 and (A-1)**2 < 256*N*N/error**2,
              'large exact projective angular grid')

    raw = {'schema': c.TARGET, 'bias': '1/5', 'bloch_vector': ['1/2', '1/3', '1/5']}
    code = c.encode(raw, 1, F(1, 4))
    for key, value in [('schema', 'bad'), ('dimension', True), ('dimension', 4),
                       ('horizon', False), ('horizon', 0),
                       ('requested_unhalved_error', '2/8'), ('requested_unhalved_error', '0'),
                       ('requested_unhalved_error', '1'), ('spectral_grid', True), ('spectral_grid', 1),
                       ('fixed_length_bits', False), ('fixed_length_bits', 0),
                       ('codeword_count', '01'), ('body_hex', '00'), ('body_hex', 'AB'),
                       ('body_hex', '-1'), ('body_hex', ''), ('body_hex', True),
                       ('body_hex', format(int(code['codeword_count']), 'x')),
                       ('adaptive_error_upper', '0'), ('scope', 'fabricated')]:
        bad = copy.deepcopy(code)
        bad[key] = value
        reject('code-'+key+'-'+str(value), lambda bad=bad: c.decode(bad))
    for key in ['bias', 'visibility', 'contrast', 'direction']:
        bad = {**code, key: '1/2'}
        reject('uncharged-'+key+'-header', lambda bad=bad: c.decode(bad))
    bad = copy.deepcopy(code)
    del bad['body_hex']
    reject('missing-payload', lambda: c.decode(bad))
    for name, bad in [
            ('bias-outside', {**raw, 'bias': '2'}),
            ('biased-positivity', {**raw, 'bias': '1/2'}),
            ('positive-boundary-nonzero', {**raw, 'bias': '1'}),
            ('negative-boundary-nonzero', {**raw, 'bias': '-1'}),
            ('noncanonical-bias', {**raw, 'bias': '2/10'}),
            ('boolean-bias', {**raw, 'bias': True}),
            ('decimal-coordinate', {**raw, 'bloch_vector': ['0.5', '0']}),
            ('noncanonical-coordinate', {**raw, 'bloch_vector': ['2/4', '0']}),
            ('wrong-dimension', {**raw, 'bloch_vector': ['0']}),
            ('nonnumeric-coordinate', {**raw, 'bloch_vector': ['nan', '0']}),
            ('extra-target-field', {**raw, 'visibility': '1/2'})]:
        reject(name, lambda bad=bad: c.encode(bad, 1, F(1, 4)))
    reject('duplicate-json', lambda: c.loads('{"bias":"0","bias":"1"}'))
    reject('illegal-rational-effect', lambda: c.measurement(F(1, 2), (F(3, 4), F(0))))
    reject('illegal-bias-effect', lambda: c.measurement(F(2), (F(0), F(0))))
    reject('invalid-radical-sign', lambda: c.radical_sign(F(1), 0, F(1)))
    reject('negative-radicand', lambda: c.radical_sign(F(1), 1, F(-1)))
    reject('unordered-endpoints', lambda: c.scale_squared(1, F(0), F(1)))
    reject('outside-spectral-digit', lambda: c.probability(3, 1))
    bad_matrix = c.decode(code).to_dict()
    bad_matrix['outcomes'][0][0][0][0] = -1
    reject('negative-Choi-diagonal', lambda: Instrument.from_dict(bad_matrix))
    nonhermitian = c.decode(code).to_dict()
    nonhermitian['outcomes'][0][0][1][1] += 1
    reject('non-Hermitian-Choi', lambda: Instrument.from_dict(nonhermitian))
    not_tp = c.decode(code).to_dict()
    not_tp['denominator'] *= 2
    reject('Choi-total-not-identity', lambda: Instrument.from_dict(not_tp))
    wrong = {**code, 'body_hex': format(int(code['body_hex'], 16)+1, 'x')}
    c.decode(wrong)  # It is a legal codeword; target replay is a separate test.
    check(not c.verify(raw, wrong), 'wrong legal payload rejected by target replay')
    controls.append('wrong-legal-index-replay')
    changed = {**raw, 'bloch_vector': ['-1/2', '1/3', '1/5']}
    check(not c.verify(changed, code), 'different target rejected by replay')
    controls.append('different-target-replay')
    c.layout(1, F(1, 4), 3)
    reject('boolean-horizon-cached', lambda: c.layout(True, F(1, 4), 3))
    reject('boolean-dimension-cached', lambda: c.layout(1, F(1, 4), True))
    reject('nonfraction-error-cached', lambda: c.layout(1, 0.25, 3))

    # Exercise all three actual command-line paths and both refusal exit codes.
    with tempfile.TemporaryDirectory(prefix='gtf75-biased-') as temp:
        temp = Path(temp)
        inp = temp/'target.json'
        cert = temp/'code.json'
        inp.write_text(json.dumps(raw))
        script = str(Path(c.__file__).resolve())
        result = subprocess.run([sys.executable, script, 'encode', '--input', str(inp),
                                 '--horizon', '1', '--error', '1/4'], capture_output=True, text=True, timeout=30)
        check(result.returncode == 0 and c.loads(result.stdout) == code, 'CLI encode')
        cert.write_text(result.stdout)
        result = subprocess.run([sys.executable, script, 'decode', '--input', str(cert)],
                                capture_output=True, text=True, timeout=30)
        check(result.returncode == 0 and c.loads(result.stdout) == c.decode(code).to_dict(), 'CLI decode')
        result = subprocess.run([sys.executable, script, 'verify', '--input', str(inp),
                                 '--certificate', str(cert)], capture_output=True, text=True, timeout=30)
        check(result.returncode == 0 and c.loads(result.stdout)['verified'], 'CLI successful replay')
        cert.write_text(json.dumps(wrong))
        result = subprocess.run([sys.executable, script, 'verify', '--input', str(inp),
                                 '--certificate', str(cert)], capture_output=True, text=True, timeout=30)
        check(result.returncode == 1 and not c.loads(result.stdout)['verified'], 'CLI wrong-index refusal')
        inp.write_text('{"schema":0,"schema":1}')
        result = subprocess.run([sys.executable, script, 'encode', '--input', str(inp),
                                 '--horizon', '1', '--error', '1/4'], capture_output=True, text=True, timeout=30)
        check(result.returncode == 2 and 'duplicate JSON field' in result.stderr, 'CLI malformed-input refusal')
        cases['cli'] = 5

    return {'schema': 'gtf75.finite-regression/1', 'status': 'success',
            'exact_assertions': count, 'cases': cases, 'capacities': capacities,
            'negative_controls': controls, 'floating_point_decisions': False,
            'scope': ('Finite exact Bernoulli, radical, scalar-gauge, spectral-rounding, angular-error-budget, '
                      'payload, legal-Choi and CLI replay regression. Not a proof of an adaptive '
                      'supremum, a continuum covering law, an asymptotic lower bound, or priority.')}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
