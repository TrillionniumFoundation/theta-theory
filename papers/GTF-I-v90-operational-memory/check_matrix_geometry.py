#!/usr/bin/env python3
"""Finite exact checks of matrix-modulus algebra, parsing and pair replay.

The tests do not prove the continuum metric theorem, a multi-logarithmic
entropy law, optimal coding, the adaptive supremum, or literature priority.
"""
from __future__ import annotations

import copy
from fractions import Fraction
from itertools import combinations
import json
from math import comb, isqrt
from pathlib import Path
import subprocess
import sys
import tempfile

import sympy as sp

import biased_codec as legacy
import matrix_metric as c


R = sp.Rational


def clean(matrix):
    return sp.Matrix(matrix).applyfunc(sp.expand)


def raw_pair(E, F):
    return {'schema': c.PAIR, 'dimension': E.rows,
            'effect_e': c.matrix_to_json(E), 'effect_f': c.matrix_to_json(F)}


def rational_unitary(d: int, reverse: bool = False):
    U = sp.eye(d)
    indices = list(range(d-1))
    if reverse:
        indices.reverse()
    for j in indices:
        G = sp.eye(d)
        G[j, j] = G[j+1, j+1] = R(3, 5)
        if (j+int(reverse)) % 2:
            G[j, j+1] = G[j+1, j] = 4*sp.I/5
        else:
            G[j, j+1], G[j+1, j] = -R(4, 5), R(4, 5)
        U = clean(G*U)
    return U


def conjugate(U, E):
    return clean(U*E*U.adjoint())


def binomial_distance(N, p, q):
    return sum(abs(comb(N, j)*p**j*(1-p)**(N-j)
                   -comb(N, j)*q**j*(1-q)**(N-j)) for j in range(N+1))


def principal_minor_psd(A):
    """Independent finite PSD oracle; only used for matrices of order <=4."""
    return all(sp.expand(A.extract(indices, indices).det()) >= 0
               for k in range(1, A.rows+1)
               for indices in combinations(range(A.rows), k))


def run() -> dict:
    count = 0
    controls = []
    cases = {'bernoulli': 0, 'qubit_angular': 0, 'qubit_spectral': 0,
             'matrix_pairs': 0, 'unitary_covariance': 0,
             'repeated_midpoint': 0, 'scalar': 0,
             'horizontal_gauge': 0, 'psd_crosscheck': 0, 'cli': 0}

    def check(condition, message):
        nonlocal count
        count += 1
        if not condition:
            raise RuntimeError(message)

    def reject(name, action):
        try:
            action()
        except (ValueError, TypeError, KeyError, IndexError):
            controls.append(name)
            return
        raise RuntimeError('negative control accepted: '+name)

    def exercise(E, F, N, category, replay=False):
        raw = raw_pair(E, F)
        certificate = c.compute(raw, N)
        X = c.matrix_from_json(certificate['sylvester_solution'], E.rows)
        H, M = F-E, (E+F)/2
        V = clean(M-M*M)
        q2 = c.rational(certificate['q_squared'])
        check(clean(V*X+X*V+X/N-H) == sp.zeros(E.rows), 'independent Sylvester residual')
        check(X == X.adjoint(), 'Hermitian Sylvester solution')
        check(q2 == sp.expand(N*sp.trace(H*X)), 'independent quadratic contraction')
        check(q2 >= 0 and (q2 == 0) == (E == F), 'positive definite comparison form')
        check(q2 <= sp.expand(N*N*sp.trace(H*H)), 'finite-cutoff Hilbert-Schmidt bound')
        check(c.rational(certificate['nonadaptive_lower_squared'])
              == min(1, q2)/sp.Integer(8192*E.rows)**2, 'lower constant and dimension charge')
        check(c.rational(certificate['adaptive_upper_squared']) == min(4, 64*q2),
              'unhalved upper constant and universal cap')
        check(clean(V-(E-E*E+F-F*F)/2-H*H/4) == sp.zeros(E.rows),
              'noncommutative midpoint variance identity')
        check(c.loads(c.canonical(certificate)) == certificate, 'certificate JSON roundtrip')
        if replay:
            check(c.verify(raw, certificate, N), 'full target-bound certificate replay')
        cases[category] += 1
        return q2, X, certificate

    # The one-dimensional midpoint formula is checked against the exact
    # finite Bernoulli product distance, including both support endpoints.
    for N in [1, 2, 5, 16]:
        for p in [R(0), R(1, 1000), R(1, 4), R(1, 2), R(3, 4), R(999, 1000), R(1)]:
            for q in [p, (p+1)/2, R(1)]:
                q2, _, certificate = exercise(sp.Matrix([[p]]), sp.Matrix([[q]]),
                                              N, 'bernoulli')
                m = (p+q)/2
                expected = N*(p-q)**2/(2*m*(1-m)+R(1, N))
                check(q2 == expected, 'one-dimensional midpoint denominator')
                D = binomial_distance(N, p, q)
                check(c.rational(certificate['nonadaptive_lower_squared']) <= D*D
                      <= c.rational(certificate['adaptive_upper_squared']),
                      'certified interval contains exact Bernoulli product distance')
                T2 = N*(p-q)**2/(max(p*(1-p), q*(1-q))+R(1, N))
                check(q2 <= T2, 'diagonal compression agrees with legacy endpoint witness')

    # For a common qubit spectrum, rotation by t changes the Bloch direction
    # by 2t. Eliminating t through rational sine/cosine yields an independent
    # exact midpoint formula, with no floating-point angle or eigensystem.
    for p, q in [(R(1), R(0)), (R(3, 4), R(0)), (R(1), R(1, 4)),
                 (R(4, 5), R(1, 5)), (R(3, 5), R(1, 5)), (R(1, 3), R(1, 3))]:
        E = sp.diag(p, q)
        for ct, st in [(R(1), R(0)), (R(3, 5), R(4, 5)), (R(4, 5), R(3, 5)),
                       (R(0), R(1)), (R(12, 13), R(5, 13))]:
            U = sp.Matrix([[ct, -st], [st, ct]])
            F = conjugate(U, E)
            check(U.adjoint()*U == sp.eye(2), 'rational qubit rotation')
            for N in [1, 3, 9]:
                q2, _, _ = exercise(E, F, N, 'qubit_angular')
                z2 = (p-q)**2*st*st
                V = p*(1-p)+q*(1-q)
                check(q2 == 2*N*z2/(V+z2/2+R(1, N)),
                      'isospectral qubit midpoint formula')
                old = legacy.scale_squared(N, Fraction(str(p)), Fraction(str(q)))
                K2 = R(old.numerator, old.denominator)
                check(K2 == N*(p-q)**2/(V+R(1, N)), 'legacy angular scale convention')
                check(q2 == 2*K2*st*st/(1+z2/(2*(V+R(1, N)))),
                      'matrix modulus and legacy angular scale compatibility')

    for p, q, s, t in [(R(1), R(0), R(3, 4), R(1, 4)),
                       (R(1, 3), R(1, 3), R(2, 3), R(1, 6)),
                       (R(1), R(1, 4), R(1), R(1, 3)),
                       (R(1, 10), R(0), R(1, 5), R(0))]:
        for N in [1, 7, 32]:
            q2, _, _ = exercise(sp.diag(p, q), sp.diag(s, t), N, 'qubit_spectral')
            expected = sum(N*(a-b)**2/(2*((a+b)/2)*(1-(a+b)/2)+R(1, N))
                           for a, b in [(p, s), (q, t)])
            check(q2 == expected, 'aligned qubit spectral decomposition')

    # Dense Gaussian-rational noncommuting pairs in dimensions three and
    # four, with all endpoint strata and nontrivial projection ranks.
    for d in [3, 4]:
        U, W = rational_unitary(d), rational_unitary(d, True)
        check(clean(U.adjoint()*U) == sp.eye(d) and clean(W.adjoint()*W) == sp.eye(d),
              'Gaussian-rational higher-dimensional unitaries')
        A = sp.diag(*[R(j+1, d+2) for j in range(d)])
        B = sp.diag(*[R(d-j, d+2) for j in range(d)])
        P = sp.diag(*[1 if j < d//2 else 0 for j in range(d)])
        face = sp.diag(*[R(j, d+1) for j in range(d)])
        repeated = sp.diag(*([R(1, 3)]*(d-1)+[R(2, 3)]))
        pairs = [(A, conjugate(U, B)),
                 (conjugate(W, A), conjugate(U, B)),
                 (P, conjugate(U, P)),
                 (face, conjugate(U, face)),
                 (sp.eye(d)-face, conjugate(U, sp.eye(d)-face)),
                 (repeated, conjugate(U, repeated))]
        for E, F in pairs:
            check(clean(E*F-F*E) != sp.zeros(d), 'test pair is actually noncommuting')
            for matrix in [E, F, sp.eye(d)-E, sp.eye(d)-F]:
                check(principal_minor_psd(matrix) == c.is_positive_semidefinite(matrix),
                      'Schur legality versus all principal minors')
                cases['psd_crosscheck'] += 1
            for N in [1, 5, 25]:
                q2, X, _ = exercise(E, F, N, 'matrix_pairs', replay=N == 5)
                complemented = c.compute(raw_pair(sp.eye(d)-E, sp.eye(d)-F), N)
                check(c.rational(complemented['q_squared']) == q2, 'common outcome-complement invariance')
                swapped = c.compute(raw_pair(F, E), N)
                check(c.rational(swapped['q_squared']) == q2, 'pair symmetry')
                check(c.matrix_from_json(swapped['sylvester_solution'], d) == -X,
                      'pair reversal reverses the Sylvester tangent')
                if N == 5:
                    changed = c.compute(raw_pair(conjugate(W, E), conjugate(W, F)), N)
                    check(c.rational(changed['q_squared']) == q2, 'unitary covariance of modulus square')
                    check(c.matrix_from_json(changed['sylvester_solution'], d) == conjugate(W, X),
                          'unitary covariance of the full Sylvester solution')
                    cases['unitary_covariance'] += 1

        # A repeated midpoint is chosen directly, so the expected denominator
        # needs no eigensystem and remains unambiguous in the repeated block.
        for diagonal in [[R(1, 2)]*d, [R(1, 3)]*(d-1)+[R(2, 3)]]:
            M = sp.diag(*diagonal)
            H = sp.zeros(d)
            for j in range(d-1):
                H[j, j+1] = (1+sp.I)/40
                H[j+1, j] = (1-sp.I)/40
            for N in [1, 16]:
                q2, _, _ = exercise(M-H/2, M+H/2, N, 'repeated_midpoint', replay=True)
                expected = N*sum(sp.expand(H[i, j]*sp.conjugate(H[i, j]))
                                 /(diagonal[i]*(1-diagonal[i])
                                   +diagonal[j]*(1-diagonal[j])+R(1, N))
                                 for i in range(d) for j in range(d))
                check(q2 == expected, 'repeated-midpoint spectral sum without eigenvector choices')

    for d in [1, 2, 3, 4]:
        for p, q in [(R(0), R(1)), (R(1, 3), R(2, 3)), (R(1, 2), R(1, 2))]:
            for N in [1, 4, 64]:
                q2, _, _ = exercise(p*sp.eye(d), q*sp.eye(d), N, 'scalar')
                m = (p+q)/2
                check(q2 == d*N*(p-q)**2/(2*m*(1-m)+R(1, N)),
                      'scalar effect has the correct Hilbert-Schmidt dimension factor')

    # Rational square roots from Pythagorean pairs permit exact checks of
    # the horizontal identities and the anti-Hermitian gauge realization.
    # Every G used here is strictly interior; no boundary tangent lift is
    # claimed. Boundary legality is tested separately above.
    root_pairs = [(R(3, 5), R(4, 5)), (R(5, 13), R(12, 13)),
                  (R(8, 17), R(15, 17)), (R(20, 29), R(21, 29))]
    for d in [2, 3, 4]:
        U = rational_unitary(d)
        a = [root_pairs[j][0] for j in range(d)]
        b = [root_pairs[j][1] for j in range(d)]
        A1, A0 = conjugate(U, sp.diag(*a)), conjugate(U, sp.diag(*b))
        G = clean(A1*A1)
        S = clean(A1*A0)
        K = sp.diag(*[R(j+1, 10*d) for j in range(d)])
        for j in range(d-1):
            K[j, j+1], K[j+1, j] = (1+sp.I)/30, (1-sp.I)/30
        check(clean(A1*A1+A0*A0) == sp.eye(d), 'rational complementary square roots')
        check(clean(S*S) == clean(G-G*G), 'rational variance square root')
        H0 = clean(S*K+K*S)
        B1, B0 = clean(A0*K), clean(-A1*K)
        check(clean(A1.adjoint()*B1+B1.adjoint()*A1) == H0, 'first horizontal tangent equation')
        check(clean(A0.adjoint()*B0+B0.adjoint()*A0) == -H0, 'second horizontal tangent equation')
        check(clean(A1.adjoint()*B1+A0.adjoint()*B0) == sp.zeros(d), 'horizontal zero cross overlap')
        check(clean(B1.adjoint()*B1+B0.adjoint()*B0) == clean(K*K), 'horizontal derivative Gram matrix')
        W = sp.Matrix.vstack(A0, sp.zeros(d), sp.zeros(d), A1)
        derivative = sp.Matrix.vstack(B0, sp.zeros(d), sp.zeros(d), B1)
        check(clean(W.adjoint()*W) == sp.eye(d), 'measurement dilation isometry')
        check(clean(W.adjoint()*derivative) == sp.zeros(d), 'dilation horizontal overlap')
        check(clean(derivative.adjoint()*derivative) == clean(K*K), 'dilation derivative square')
        Hbasis = clean(U.adjoint()*H0*U)
        R1prime = conjugate(U, sp.Matrix(d, d, lambda i, j: Hbasis[i, j]/(a[i]+a[j])))
        R0prime = conjugate(U, sp.Matrix(d, d, lambda i, j: -Hbasis[i, j]/(b[i]+b[j])))
        for A, B, Rprime in [(A1, B1, R1prime), (A0, B0, R0prime)]:
            T = clean((B-Rprime)*A.inv(method='DM'))
            check(clean(T+T.adjoint()) == sp.zeros(d), 'realizing gauge is anti-Hermitian')
            check(clean(T*A+Rprime) == B, 'genuine dilation gauge has prescribed derivative')
        for N in [1, 4, 25]:
            kappa = R(1, isqrt(N))
            H = clean(H0+kappa*K)
            recovered = c.sylvester_solution(S, H, kappa)
            check(recovered == K, 'regularized horizontal Sylvester equation')
            check(clean(H-H0) == kappa*K, 'horizontal and hybrid residual splitting')
            cases['horizontal_gauge'] += 1

    # Strict schema and PSD rejection is tested independently of replay.
    E = sp.diag(R(3, 4), R(1, 4))
    F = sp.Matrix([[R(1, 2), sp.I/10], [-sp.I/10, R(1, 3)]])
    raw = raw_pair(E, F)
    certificate = c.compute(raw, 3)
    for field, value, name in [('schema', 'unknown', 'pair-schema'),
                               ('dimension', True, 'boolean-dimension'),
                               ('dimension', 2.0, 'float-dimension'),
                               ('dimension', 0, 'zero-dimension'),
                               ('dimension', -2, 'negative-dimension')]:
        reject(name, lambda field=field, value=value: c.compute({**raw, field: value}, 3))
    reject('additional-pair-field', lambda: c.compute({**raw, 'eigenvectors': []}, 3))
    reject('missing-pair-field', lambda: c.compute({k: v for k, v in raw.items() if k != 'effect_f'}, 3))
    for value, name in [(True, 'boolean-horizon'), (3.0, 'float-horizon'),
                        (0, 'zero-horizon'), (-1, 'negative-horizon')]:
        reject(name, lambda value=value: c.compute(raw, value))
    for value, name in [(True, 'boolean-entry'), (1, 'integer-entry'), (0.5, 'float-entry'),
                        ('2/4', 'unreduced-rational'), ('0/1', 'noncanonical-zero'),
                        ('-0', 'negative-zero'), ('+1', 'plus-sign'), ('01', 'leading-zero'),
                        (' 1/2', 'rational-whitespace'), ('1/0', 'zero-denominator'),
                        ('1/-2', 'negative-denominator'), ('nan', 'nan-string'),
                        ('sqrt(2)', 'symbolic-expression'), ('1+I', 'complex-expression-string')]:
        altered = copy.deepcopy(raw)
        altered['effect_e'][0][0][0] = value
        reject(name, lambda altered=altered: c.compute(altered, 3))
    for field, value, name in [('effect_e', [], 'wrong-row-count'),
                               ('effect_e', [[['0', '0']]], 'wrong-matrix-dimension')]:
        reject(name, lambda field=field, value=value: c.compute({**raw, field: value}, 3))
    altered = copy.deepcopy(raw)
    altered['effect_e'][0][0] = ['3/4']
    reject('wrong-gaussian-entry-length', lambda: c.compute(altered, 3))
    altered = copy.deepcopy(raw)
    altered['effect_e'][0][0][1] = '1/100'
    reject('nonreal-diagonal', lambda: c.compute(altered, 3))
    altered = copy.deepcopy(raw)
    altered['effect_f'][1][0][1] = '1/10'
    reject('wrong-complex-conjugate', lambda: c.compute(altered, 3))
    illegal = [(-sp.eye(2)/100, 'negative-effect'),
               (101*sp.eye(2)/100, 'effect-above-identity'),
               (sp.Matrix([[R(1, 2), R(3, 4)], [R(3, 4), R(1, 2)]]), 'positive-diagonal-indefinite'),
               (sp.Matrix([[0, R(1, 10)], [R(1, 10), R(1, 2)]]), 'zero-pivot-nonzero-column'),
               (sp.Matrix([[0, 0, 0], [0, 0, R(1, 10)], [0, R(1, 10), 0]]),
                'vanishing-leading-minors-indefinite'),
               (sp.ones(2)*R(3, 4), 'positive-effect-with-illegal-complement')]
    for bad, name in illegal:
        reject(name, lambda bad=bad: c.compute(raw_pair(bad, sp.eye(bad.rows)/2), 3))
        check(c.is_positive_semidefinite(bad) == principal_minor_psd(bad),
              'independent principal-minor negative control')
        cases['psd_crosscheck'] += 1
    for field, value, name in [('schema', 'other', 'certificate-schema'),
                               ('dimension', True, 'certificate-boolean-dimension'),
                               ('horizon', True, 'certificate-boolean-horizon'),
                               ('q_squared', True, 'certificate-boolean-square'),
                               ('q_squared', '-1', 'negative-modulus-square'),
                               ('q_squared', '2/4', 'noncanonical-modulus-square'),
                               ('pair_sha256', 'A'*64, 'noncanonical-target-digest'),
                               ('scope', 'exact adaptive distance', 'overclaimed-scope'),
                               ('normalization', 'half trace norm', 'wrong-normalization'),
                               ('theorem', 'unproved', 'wrong-theorem')]:
        reject(name, lambda field=field, value=value:
               c.verify(raw, {**certificate, field: value}))
    reject('additional-certificate-field', lambda: c.verify(raw, {**certificate, 'hidden_bias': '0'}))
    reject('missing-certificate-field', lambda: c.verify(raw, {k: v for k, v in certificate.items()
                                                              if k != 'sylvester_solution'}))
    for field in ['q_squared', 'nonadaptive_lower_squared', 'adaptive_upper_squared']:
        changed = {**certificate, field: str(c.rational(certificate[field])+1)}
        check(not c.verify(raw, changed), 'changed bound rejected by full replay')
        controls.append('tampered-'+field)
    changed = copy.deepcopy(certificate)
    changed['sylvester_solution'][0][0][0] = str(c.rational(changed['sylvester_solution'][0][0][0])+1)
    check(not c.verify(raw, changed), 'Hermitian but wrong Sylvester solution rejected')
    controls.append('tampered-sylvester-solution')
    check(not c.verify(raw, {**certificate, 'pair_sha256': '0'*64}), 'changed pair digest rejected')
    controls.append('tampered-target-digest')
    check(not c.verify(raw_pair(F, E), certificate), 'reversed target pair rejected despite equal modulus')
    controls.append('different-target-equal-modulus')
    check(not c.verify(raw, certificate, 4), 'caller-pinned horizon mismatch rejected')
    controls.append('wrong-expected-horizon')
    reject('boolean-expected-horizon', lambda: c.verify(raw, certificate, True))
    reject('duplicate-json-field', lambda: c.loads('{"dimension":2,"dimension":3}'))
    reject('nested-duplicate-json-field', lambda: c.loads('{"pair":{"x":1,"x":2}}'))
    for token in ['NaN', 'Infinity', '-Infinity']:
        reject('nonfinite-json-'+token, lambda token=token: c.loads('{"value":'+token+'}'))

    # Exercise actual parsing, output, mismatch/malformed exit codes and
    # normal/-O parity. The suite itself likewise contains no Python assert.
    with tempfile.TemporaryDirectory(prefix='gtf76-matrix-') as folder:
        folder = Path(folder)
        inp, certfile = folder/'pair.json', folder/'certificate.json'
        inp.write_text(json.dumps(raw), encoding='utf-8')
        script = str(Path(c.__file__).resolve())

        def cli(arguments, optimized=False):
            command = [sys.executable]+(['-O'] if optimized else [])+[script]+arguments
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            cases['cli'] += 1
            return result

        arguments = ['compute', '--input', str(inp), '--horizon', '3']
        normal = cli(arguments)
        optimized = cli(arguments, True)
        check(normal.returncode == optimized.returncode == 0 and normal.stdout == optimized.stdout,
              'CLI normal and optimized computation are identical')
        check(c.loads(normal.stdout) == certificate, 'CLI compute matches exact pair certificate')
        certfile.write_text(normal.stdout, encoding='utf-8')
        arguments = ['verify', '--input', str(inp), '--certificate', str(certfile), '--horizon', '3']
        normal, optimized = cli(arguments), cli(arguments, True)
        check(normal.returncode == optimized.returncode == 0 and normal.stdout == optimized.stdout
              and c.loads(normal.stdout)['verified'], 'CLI normal and optimized replay are identical')
        result = cli(arguments[:-1]+['4'])
        check(result.returncode == 1 and not c.loads(result.stdout)['verified'], 'CLI pinned-horizon refusal')
        certfile.write_text(json.dumps({**certificate, 'q_squared': '0'}), encoding='utf-8')
        result = cli(arguments)
        check(result.returncode == 1 and not c.loads(result.stdout)['verified'], 'CLI tampered-value refusal')
        certfile.write_text(json.dumps({**certificate, 'extra': '0'}), encoding='utf-8')
        result = cli(arguments)
        check(result.returncode == 2 and 'additional' in result.stderr, 'CLI additional-field refusal')
        inp.write_text('{"schema":0,"schema":1}', encoding='utf-8')
        result = cli(['compute', '--input', str(inp), '--horizon', '3'])
        check(result.returncode == 2 and 'duplicate JSON field' in result.stderr,
              'CLI actual duplicate-key parser refusal')

    return {'schema': 'gtf76.matrix-finite-regression/1', 'status': 'success',
            'exact_assertions': count, 'cases': cases, 'negative_controls': controls,
            'floating_point_decisions': False,
            'optimized_mode_cli_invariance': True,
            'scope': ('Finite exact Bernoulli and qubit compatibility, noncommuting matrix, '
                      'unitary covariance, repeated-spectrum, PSD, Sylvester, interior '
                      'horizontal-gauge and strict-CLI replay checks. Not a continuum '
                      'metric or entropy proof, an adaptive-distance solver, optimal coding '
                      'evidence, or a priority certificate.')}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
