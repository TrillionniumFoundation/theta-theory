#!/usr/bin/env python3
"""Exact midpoint-modulus certificates for supplied binary matrix effects.

This program evaluates a rational Sylvester equation and the squared bounds
in Theorem thm:matrixmetric76. It does not compute the adaptive distance,
construct a high-dimensional optimal code, or learn an unknown device.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys

import sympy as sp


PAIR = 'gtf76.matrix-effect-pair/1'
CERTIFICATE = 'gtf76.matrix-effect-bound/1'
VERIFICATION = 'gtf76.matrix-effect-verification/1'
THEOREM = 'thm:matrixmetric76'
NORMALIZATION = 'unhalved final joint-state trace norm'
SCOPE = ('Exact supplied-pair midpoint modulus and theorem bounds for ordered '
         'binary memoryless measurement channels; not the exact adaptive distance, '
         'a high-dimensional encoder, or device learning.')
PAIR_FIELDS = {'schema', 'dimension', 'effect_e', 'effect_f'}
CERTIFICATE_FIELDS = {
    'schema', 'dimension', 'horizon', 'pair_sha256', 'q_squared',
    'nonadaptive_lower_squared', 'adaptive_upper_squared',
    'sylvester_solution', 'theorem', 'normalization', 'scope',
}
RATIONAL_PATTERN = re.compile(r'-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z')
DIGEST_PATTERN = re.compile(r'[0-9a-f]{64}\Z')


def require(condition, message: str) -> None:
    if not condition:
        raise ValueError(message)


def strict_keys(raw, fields: set[str], name: str) -> None:
    require(type(raw) is dict and set(raw) == fields,
            name+' has missing, additional, or invalid fields')


def positive_integer(value, name: str) -> int:
    require(type(value) is int and value > 0, name+' must be a positive integer')
    return value


def rational(value, name: str = 'rational') -> sp.Rational:
    require(type(value) is str and RATIONAL_PATTERN.fullmatch(value) is not None,
            name+' must be a canonical rational string')
    exact = Fraction(value)
    require(str(exact) == value, name+' is not a reduced canonical rational')
    return sp.Rational(exact.numerator, exact.denominator)


def gaussian_parts(value) -> tuple[sp.Rational, sp.Rational]:
    real, imag = sp.expand(value).as_real_imag()
    require(real.is_Rational is True and imag.is_Rational is True,
            'calculation left the Gaussian rational field')
    return real, imag


def gaussian(value) -> sp.Expr:
    real, imag = gaussian_parts(value)
    return real+sp.I*imag


def matrix_from_json(raw, d: int, name: str = 'matrix') -> sp.Matrix:
    positive_integer(d, 'dimension')
    require(type(raw) is list and len(raw) == d, name+' has the wrong row count')
    entries = []
    for row in raw:
        require(type(row) is list and len(row) == d, name+' has the wrong column count')
        for entry in row:
            require(type(entry) is list and len(entry) == 2,
                    name+' entries must be [real, imaginary] rational-string pairs')
            entries.append(rational(entry[0], name+' real part')
                           +sp.I*rational(entry[1], name+' imaginary part'))
    matrix = sp.Matrix(d, d, entries)
    require(matrix == matrix.adjoint(), name+' must be Hermitian')
    return matrix


def matrix_to_json(matrix: sp.MatrixBase) -> list:
    return [[[str(part) for part in gaussian_parts(matrix[i, j])]
             for j in range(matrix.cols)] for i in range(matrix.rows)]


def is_positive_semidefinite(matrix: sp.MatrixBase) -> bool:
    """Hermitian PSD by exact Schur elimination, including zero pivots.

    A zero diagonal in a PSD matrix forces its complete row and column to
    vanish. Checking that implication avoids the incorrect leading-minor
    test at singular matrices. No eigenvalue or floating-point test is used.
    """
    require(matrix.rows == matrix.cols and matrix.rows > 0,
            'PSD test requires a nonempty square matrix')
    work = sp.Matrix(matrix).applyfunc(gaussian)
    require(work == work.adjoint(), 'PSD test requires a Hermitian matrix')
    d = work.rows
    for k in range(d):
        pivot, imag = gaussian_parts(work[k, k])
        require(imag == 0, 'nonreal Schur pivot')
        if pivot < 0:
            return False
        if pivot == 0:
            if any(work[i, k] != 0 for i in range(k+1, d)):
                return False
            continue
        for i in range(k+1, d):
            for j in range(k+1, d):
                work[i, j] = gaussian(work[i, j]-work[i, k]*work[k, j]/pivot)
        for i in range(k+1, d):
            work[i, k] = work[k, i] = 0
    return True


def pair(raw: dict) -> tuple[sp.Matrix, sp.Matrix]:
    strict_keys(raw, PAIR_FIELDS, 'pair')
    require(raw['schema'] == PAIR, 'wrong pair schema')
    d = positive_integer(raw['dimension'], 'dimension')
    E = matrix_from_json(raw['effect_e'], d, 'effect_e')
    F = matrix_from_json(raw['effect_f'], d, 'effect_f')
    identity = sp.eye(d)
    for name, matrix in [('effect_e', E), ('effect_f', F)]:
        require(is_positive_semidefinite(matrix), name+' is not positive semidefinite')
        require(is_positive_semidefinite(identity-matrix), name+' exceeds the identity')
    return E, F


def sylvester_solution(V: sp.MatrixBase, H: sp.MatrixBase,
                       tau: sp.Rational) -> sp.Matrix:
    """Solve V X + X V + tau X = H over the Gaussian rationals.

    Column vectorization gives a d**2 by d**2 exact linear system. SymPy's
    domain-matrix inverse is exact; the explicit residual and Hermiticity
    checks are required before returning its solution.
    """
    require(V.rows == V.cols == H.rows == H.cols and V.rows > 0,
            'incompatible Sylvester matrix dimensions')
    require(V == V.adjoint() and H == H.adjoint(),
            'Sylvester coefficients and tangent must be Hermitian')
    require(getattr(tau, 'is_Rational', False) is True and tau > 0,
            'Sylvester cutoff must be a positive exact rational')
    V = sp.Matrix(V).applyfunc(gaussian)
    H = sp.Matrix(H).applyfunc(gaussian)
    require(is_positive_semidefinite(V), 'Sylvester variance must be positive semidefinite')
    d = V.rows
    coefficient = (sp.kronecker_product(sp.eye(d), V)
                   +sp.kronecker_product(V.T, sp.eye(d))+tau*sp.eye(d*d))
    vector = coefficient.inv(method='DM')*H.vec()
    X = sp.Matrix(d, d, lambda i, j: gaussian(vector[i+j*d]))
    require(X == X.adjoint(), 'Sylvester solution is not Hermitian')
    residual = (V*X+X*V+tau*X-H).applyfunc(gaussian)
    require(residual == sp.zeros(d), 'nonzero exact Sylvester residual')
    return X


def canonical(raw: dict) -> str:
    return json.dumps(raw, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                      allow_nan=False)


def compute(raw: dict, horizon: int) -> dict:
    N = positive_integer(horizon, 'horizon')
    E, F = pair(raw)
    d = E.rows
    midpoint = (E+F)/2
    H = F-E
    V = (midpoint*(sp.eye(d)-midpoint)).applyfunc(gaussian)
    X = sylvester_solution(V, H, sp.Rational(1, N))
    real, imag = gaussian_parts(N*sp.trace(H*X))
    require(imag == 0 and real >= 0, 'modulus square must be real and nonnegative')
    require((real == 0) == (E == F), 'modulus degeneracy inconsistent with the pair')
    lower_squared = min(sp.Integer(1), real)/sp.Integer(8192*d)**2
    upper_squared = min(sp.Integer(4), 64*real)
    return {
        'schema': CERTIFICATE,
        'dimension': d,
        'horizon': N,
        'pair_sha256': hashlib.sha256(canonical(raw).encode('utf-8')).hexdigest(),
        'q_squared': str(real),
        'nonadaptive_lower_squared': str(lower_squared),
        'adaptive_upper_squared': str(upper_squared),
        'sylvester_solution': matrix_to_json(X),
        'theorem': THEOREM,
        'normalization': NORMALIZATION,
        'scope': SCOPE,
    }


def validate_certificate(raw: dict) -> None:
    strict_keys(raw, CERTIFICATE_FIELDS, 'certificate')
    require(raw['schema'] == CERTIFICATE, 'wrong certificate schema')
    d = positive_integer(raw['dimension'], 'certificate dimension')
    positive_integer(raw['horizon'], 'certificate horizon')
    require(type(raw['pair_sha256']) is str
            and DIGEST_PATTERN.fullmatch(raw['pair_sha256']) is not None,
            'certificate pair digest must be lowercase SHA-256 hexadecimal')
    for field in ['q_squared', 'nonadaptive_lower_squared', 'adaptive_upper_squared']:
        require(rational(raw[field], field) >= 0, field+' must be nonnegative')
    matrix_from_json(raw['sylvester_solution'], d, 'sylvester_solution')
    require(raw['theorem'] == THEOREM, 'unsupported theorem identifier')
    require(raw['normalization'] == NORMALIZATION, 'unsupported distance normalization')
    require(raw['scope'] == SCOPE, 'unsupported certificate scope')


def verify(raw: dict, certificate: dict, horizon: int | None = None) -> bool:
    """Replay the entire supplied pair and certificate, optionally pinning N."""
    validate_certificate(certificate)
    pair(raw)
    if horizon is not None:
        positive_integer(horizon, 'expected horizon')
        if certificate['horizon'] != horizon:
            return False
    return compute(raw, certificate['horizon']) == certificate


def loads(data: str) -> dict:
    require(type(data) is str, 'JSON text required')

    def object_pairs(items):
        out = {}
        for key, value in items:
            require(key not in out, 'duplicate JSON field: '+key)
            out[key] = value
        return out

    def constant(name):
        raise ValueError('nonfinite JSON number: '+name)

    return json.loads(data, object_pairs_hook=object_pairs, parse_constant=constant)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    command = sub.add_parser('compute', help='compute an exact supplied-pair certificate')
    command.add_argument('--input', required=True)
    command.add_argument('--horizon', type=int, required=True)
    command = sub.add_parser('verify', help='replay a certificate against the supplied pair')
    command.add_argument('--input', required=True)
    command.add_argument('--certificate', required=True)
    command.add_argument('--horizon', type=int, help='require this expected horizon')
    args = parser.parse_args(argv)
    try:
        raw = loads(Path(args.input).read_text(encoding='utf-8'))
        if args.action == 'compute':
            result = compute(raw, args.horizon)
            print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
            return 0
        certificate = loads(Path(args.certificate).read_text(encoding='utf-8'))
        verified = verify(raw, certificate, args.horizon)
        print(json.dumps({'schema': VERIFICATION, 'verified': verified}, sort_keys=True))
        return 0 if verified else 1
    except (ValueError, TypeError, KeyError, IndexError, OSError) as error:
        print(json.dumps({'error': str(error)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
