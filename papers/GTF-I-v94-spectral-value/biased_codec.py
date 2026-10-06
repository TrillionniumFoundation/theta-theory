#!/usr/bin/env python3
"""Exact supplied-description code for all ordered binary qubit measurements.

One index jointly charges bias, contrast and direction. A Cartesian target may
have an irrational norm; every comparison and decoded Choi entry is exact. The
reference implementation uses O(B**2) arithmetic operations and O(B) stored
row counts, with B = ceil(8 sqrt(N)/delta). It makes no optimal workspace or
polynomial encoded-precision running-time claim.
"""
from __future__ import annotations
import argparse
from bisect import bisect_right
from fractions import Fraction as F
from functools import lru_cache
import json
from math import lcm
from pathlib import Path
import sys

from choi_streaming import Instrument
from coupled_codec import chart, nearest_algebraic, ratio_compare, sign, loads
from noisy_readout_codec import require, fraction, positive, strict_keys, canonical, ceil_sqrt

TARGET = 'gtf75.biased-binary-target/1'
CODE = 'gtf75.biased-binary-code/1'
SCOPE = ('One reusable supplied-description index jointly charging bias, contrast and direction; '
         'complete adaptive unhalved trace error; no query learning or physical classical simulation.')


def target(raw: dict) -> tuple[F, tuple[F, ...]]:
    strict_keys(raw, {'schema', 'bias', 'bloch_vector'}, 'target')
    require(raw['schema'] == TARGET, 'wrong target schema')
    b = fraction(raw['bias'], 'bias')
    v = raw['bloch_vector']
    require(type(v) is list and len(v) in (2, 3), 'two or three Cartesian coordinates required')
    x = tuple(fraction(q, 'coordinate') for q in v)
    require(-1 <= b <= 1 and sum(q*q for q in x) <= (1-abs(b))**2,
            'target does not define a legal binary measurement')
    return b, x


def parameters(N: int, error: F, d: int) -> None:
    positive(N, 'horizon')
    require(type(d) is int and d in (2, 3), 'dimension must be 2 or 3')
    require(isinstance(error, F) and 0 < error <= F(1, 4), 'error must lie in (0,1/4]')


def radial_grid(N: int, error: F) -> int:
    parameters(N, error, 3)
    return ceil_sqrt(F(64*N)/(error*error))


def probability(j: int, B: int) -> F:
    positive(B, 'spectral grid')
    require(type(j) is int and 0 <= j <= 2*B, 'spectral digit outside grid')
    k = j if j <= B else 2*B-j
    p = F(k*k, B*B+k*k)
    return p if j <= B else 1-p


def radical_sign(c: F, s: int, Q: F) -> int:
    """Sign of c + s sqrt(Q), without evaluating a square root.

    Sign checks precede squaring. In particular a negative left side is never
    treated as a positive number merely because its square is large.
    """
    require(isinstance(c, F) and isinstance(Q, F) and Q >= 0,
            'invalid rational radical comparison')
    require(type(s) is int and s in (-1, 1), 'invalid radical sign')
    if s == -1:
        return -radical_sign(-c, 1, Q)
    if c >= 0:
        return int(c > 0 or Q > 0)
    return sign(Q-c*c)


def endpoint_compare(alpha: F, Q: F, s: int, v: F) -> int:
    """Sign of (alpha + s sqrt(Q))/2 - v."""
    require(isinstance(alpha, F) and isinstance(v, F), 'rational endpoint comparison required')
    return radical_sign(alpha-2*v, s, Q)


def spectral_digit(alpha: F, Q: F, s: int, B: int) -> int:
    """Quantize a spectral probability through its nearer square-root chart.

    The scalar rounding map is nondecreasing, so ordered endpoints remain
    ordered. Chart-coordinate midpoint ties go toward zero.
    """
    positive(B, 'spectral grid')
    require(endpoint_compare(alpha, Q, s, F(0)) >= 0
            and endpoint_compare(alpha, Q, s, F(1)) <= 0, 'endpoint outside [0,1]')
    if endpoint_compare(alpha, Q, s, F(1, 2)) <= 0:
        return nearest_algebraic(lambda v: endpoint_compare(alpha, Q, s, v*v/(1+v*v)), B)
    j = nearest_algebraic(lambda v: -endpoint_compare(alpha, Q, s, 1-v*v/(1+v*v)), B)
    return 2*B-j


def scale_squared(N: int, p: F, q: F) -> F:
    positive(N, 'horizon')
    require(isinstance(p, F) and isinstance(q, F) and 0 <= q <= p <= 1,
            'ordered rational endpoints required')
    V = p*(1-p)+q*(1-q)
    return F(N)*(p-q)**2/(V+F(1, N))


def angular_grid(N: int, error: F, d: int, p: F, q: F) -> int:
    parameters(N, error, d)
    K2 = scale_squared(N, p, q)
    return max(1, ceil_sqrt(128*(d-1)*K2/(error*error))) if p != q else 0


def layer_size(N: int, error: F, d: int, p: F, q: F) -> int:
    A = angular_grid(N, error, d, p, q)
    return 2*d*(2*A+1)**(d-1) if A else 1


@lru_cache(maxsize=4)
def _layout(N: int, error: F, d: int) -> tuple[int, tuple[F, ...], tuple[int, ...]]:
    """Only O(B) endpoint values and row starts are retained.

    The ordered-pair triangular sum takes O(B**2) exact arithmetic operations;
    angular words are counted and ranked without enumeration.
    """
    B = radial_grid(N, error)
    ps = tuple(probability(j, B) for j in range(2*B+1))
    rows = [0]
    for i, p in enumerate(ps):
        rows.append(rows[-1]+sum(layer_size(N, error, d, p, ps[j]) for j in range(i+1)))
    return B, ps, tuple(rows)


def layout(N: int, error: F, d: int) -> tuple[int, tuple[F, ...], tuple[int, ...]]:
    # Validate before cache lookup: booleans and integers compare equal as keys.
    parameters(N, error, d)
    return _layout(N, error, d)


def header(N: int, error: F, d: int, body: int) -> dict:
    B, _, rows = layout(N, error, d)
    require(type(body) is int and 0 <= body < rows[-1], 'payload outside code alphabet')
    return {'schema': CODE, 'dimension': d, 'horizon': N,
            'requested_unhalved_error': str(error), 'spectral_grid': B,
            'codeword_count': str(rows[-1]), 'body_hex': format(body, 'x'),
            'fixed_length_bits': (rows[-1]-1).bit_length(),
            'adaptive_error_upper': str(error/2), 'scope': SCOPE}


def encode(raw: dict, N: int, error: F) -> dict:
    b, x = target(raw)
    d = len(x)
    B, ps, rows = layout(N, error, d)
    Q = sum(t*t for t in x)
    i = spectral_digit(1+b, Q, 1, B)
    j = spectral_digit(1+b, Q, -1, B)
    require(i >= j, 'spectral order failure')
    body = rows[i]+sum(layer_size(N, error, d, ps[i], ps[k]) for k in range(j))
    if i != j:
        require(Q > 0, 'nonzero decoded contrast requires nonzero target contrast')
        axis = max(range(d), key=lambda a: (abs(x[a]), -a))
        s = 1 if x[axis] >= 0 else -1
        A = angular_grid(N, error, d, ps[i], ps[j])
        local = 2*axis+int(s == -1)
        for a in range(d):
            if a != axis:
                mag = nearest_algebraic(lambda v: ratio_compare(abs(x[a]), abs(x[axis]), Q, v), A)
                local = local*(2*A+1)+sign(x[a])*mag+A
        body += local
    return header(N, error, d, body)


def unpack(raw: dict) -> tuple[F, F, tuple[F, ...]]:
    strict_keys(raw, {'schema', 'dimension', 'horizon', 'requested_unhalved_error',
                      'spectral_grid', 'codeword_count', 'body_hex', 'fixed_length_bits',
                      'adaptive_error_upper', 'scope'}, 'code')
    require(raw['schema'] == CODE, 'wrong code schema')
    N = positive(raw['horizon'], 'horizon')
    d = raw['dimension']
    error = fraction(raw['requested_unhalved_error'], 'error')
    B, ps, rows = layout(N, error, d)
    text = raw['body_hex']
    require(type(text) is str and text and all(c in '0123456789abcdef' for c in text),
            'invalid hexadecimal')
    require(len(text) == 1 or text[0] != '0', 'noncanonical hexadecimal')
    require(len(text) <= max(1, ((rows[-1]-1).bit_length()+3)//4), 'overlong payload')
    body = int(text, 16)
    require(body < rows[-1], 'payload outside code alphabet')
    require(type(raw['spectral_grid']) is int and type(raw['fixed_length_bits']) is int,
            'nonintegral header')
    require(canonical(raw) == canonical(header(N, error, d, body)), 'altered header or error certificate')
    i = bisect_right(rows, body)-1
    local = body-rows[i]
    for j in range(i+1):
        size = layer_size(N, error, d, ps[i], ps[j])
        if local < size:
            break
        local -= size
    p, q = ps[i], ps[j]
    if i == j:
        return p, q, (F(0),)*d
    A = angular_grid(N, error, d, p, q)
    digits = []
    for _ in range(d-1):
        local, digit = divmod(local, 2*A+1)
        digits.append(digit-A)
    axis, sign_bit = divmod(local, 2)
    u = chart(axis, 1 if sign_bit == 0 else -1, tuple(reversed(digits)), A, d)
    return p, q, u


def decode_coordinates(raw: dict) -> tuple[F, tuple[F, ...]]:
    p, q, u = unpack(raw)
    return p+q-1, tuple((p-q)*t for t in u)


def measurement(b: F, x: tuple[F, ...]) -> Instrument:
    require(isinstance(b, F) and len(x) in (2, 3) and all(isinstance(q, F) for q in x),
            'invalid rational measurement coordinates')
    require(-1 <= b <= 1 and sum(q*q for q in x) <= (1-abs(b))**2,
            'coordinates do not define a legal binary measurement')
    x1, x2, x3 = (*x, F(0)) if len(x) == 2 else x
    mats = []
    for s in (1, -1):
        # Input-first unnormalized Choi blocks are E_+^T and E_-^T.
        mats.append([[((1+s*b+s*x3)/2, F(0)), (s*x1/2, s*x2/2)],
                     [(s*x1/2, -s*x2/2), ((1+s*b-s*x3)/2, F(0))]])
    den = lcm(*(q.denominator for mat in mats for row in mat for cell in row for q in cell))
    out = Instrument(2, 1, den,
                     [[[(int(a*den), int(b0*den)) for a, b0 in row] for row in mat] for mat in mats])
    out.validate()
    return out


def decode(raw: dict) -> Instrument:
    return measurement(*decode_coordinates(raw))


def verify(raw: dict, code: dict) -> bool:
    """Check deterministic target-bound replay, not a universal proof certificate."""
    try:
        decode(code)
        return canonical(encode(raw, code['horizon'], F(code['requested_unhalved_error']))) == canonical(code)
    except (ValueError, TypeError, KeyError, IndexError, AttributeError, ZeroDivisionError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['encode', 'decode', 'verify'])
    parser.add_argument('--input', required=True)
    parser.add_argument('--horizon', type=int)
    parser.add_argument('--error')
    parser.add_argument('--certificate')
    args = parser.parse_args()
    try:
        raw = loads(Path(args.input).read_text())
        if args.action == 'encode':
            require(args.horizon is not None and args.error is not None, 'horizon and error required')
            answer = encode(raw, args.horizon, fraction(args.error, 'error'))
        elif args.action == 'decode':
            answer = decode(raw).to_dict()
        else:
            require(args.certificate is not None, 'certificate required')
            good = verify(raw, loads(Path(args.certificate).read_text()))
            answer = {'schema': 'gtf75.target-replay/1', 'verified': good,
                      'scope': 'Canonical target-bound replay, not universal proof certification.'}
            if not good:
                print(json.dumps(answer, indent=2, sort_keys=True))
                return 1
        print(json.dumps(answer, indent=2, sort_keys=True))
        return 0
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print('error: '+str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
