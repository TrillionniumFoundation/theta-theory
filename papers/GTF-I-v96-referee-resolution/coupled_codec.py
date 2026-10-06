#!/usr/bin/env python3
"""Exact supplied-description codec for the unbiased binary qubit ball.

Both visibility and direction belong to the one charged payload index.
The canonical JSON envelope is not the payload; no query learning, optimal
workspace, or physical classical simulator is claimed. All target comparisons
use integers/Fractions, including when the target norm is irrational.
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
from noisy_readout_codec import require, fraction, positive, strict_keys, canonical, ceil_sqrt, scale_squared

TARGET = 'gtf74.binary-ball-target/1'
CODE = 'gtf74.binary-ball-code/1'
SCOPE = ('One reusable supplied-description index, jointly charging visibility and direction; '
         'legal ordered binary qubit measurement; no learning or physical classical simulation.')


def target(raw: dict) -> tuple[F, ...]:
    strict_keys(raw, {'schema', 'bloch_vector'}, 'target')
    require(raw['schema'] == TARGET, 'wrong target schema')
    v = raw['bloch_vector']
    require(type(v) is list and len(v) in (2, 3), 'two or three Cartesian coordinates required')
    x = tuple(fraction(q, 'coordinate') for q in v)
    require(sum(q*q for q in x) <= 1, 'target outside unit ball')
    return x


def parameters(N: int, error: F, d: int) -> None:
    positive(N, 'horizon')
    require(type(d) is int and d in (2, 3), 'dimension must be 2 or 3')
    require(isinstance(error, F) and 0 < error <= F(1, 4), 'error must lie in (0,1/4]')


@lru_cache(maxsize=8)
def _layers(N: int, error: F, d: int) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    """Enumerate only radial layers, not angular words; O(B) stored integers.

The reference program is pseudo-polynomial in numerical grid size. This
bounded cache is only a speed aid, not part of a minimum-workspace claim.
"""
    parameters(N, error, d)
    B = ceil_sqrt(F(64*N)/(error*error))
    grids = [0]
    starts = [0, 1]  # layer 0 starts at 0 and consists of the single erased word
    for i in range(1, B+1):
        r = F(2*i*B, B*B+i*i)
        A = max(1, ceil_sqrt(64*(d-1)*scale_squared(N, r)/(error*error)))
        grids.append(A)
        starts.append(starts[-1]+2*d*(2*A+1)**(d-1))
    return B, tuple(grids), tuple(starts)


def layers(N: int, error: F, d: int) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    # Validate before cache lookup: bool and int compare equal in cache keys.
    parameters(N, error, d)
    return _layers(N, error, d)


def sign(q: F) -> int:
    return int(q > 0)-int(q < 0)


def nearest_algebraic(compare, limit: int) -> int:
    """Nearest digit j for a number in [0,1], using comparison with j/limit.
    compare(v) has the sign of target-v; ties go toward zero.
    """
    positive(limit, 'grid')
    lo, hi = 0, limit
    while lo < hi:
        mid = (lo+hi+1)//2
        if compare(F(mid, limit)) >= 0:
            lo = mid
        else:
            hi = mid-1
    if lo < limit and compare(F(2*lo+1, 2*limit)) > 0:
        lo += 1
    return lo


def radial_compare(Q: F, v: F) -> int:
    require(0 <= Q <= 1 and 0 <= v <= 1, 'invalid radial comparison')
    r = 2*v/(1+v*v)
    return sign(Q-r*r)


def ratio_compare(b: F, a: F, Q: F, v: F) -> int:
    require(b >= 0 and a >= 0 and Q > 0 and v >= 0, 'invalid direction comparison')
    c = b-v*a
    # Never square a negative left side of b-va ? v sqrt(Q).
    return -1 if c < 0 else sign(c*c-v*v*Q)


def chart(axis: int, s: int, digits: tuple[int, ...], A: int, d: int) -> tuple[F, ...]:
    require(type(axis) is int and 0 <= axis < d and d in (2, 3), 'invalid chart axis')
    require(type(s) is int and s in (-1, 1), 'invalid chart sign')
    positive(A, 'angular grid')
    require(len(digits) == d-1 and all(type(j) is int and -A <= j <= A for j in digits),
            'angular digit outside grid')
    z = tuple(F(j, A) for j in digits)
    norm2 = sum(t*t for t in z)
    out = []
    j = 0
    for a in range(d):
        if a == axis:
            out.append(s*(1-norm2)/(1+norm2))
        else:
            out.append(2*z[j]/(1+norm2)); j += 1
    return tuple(out)


def header(N: int, error: F, d: int, body: int) -> dict:
    B, _, starts = layers(N, error, d)
    return {'schema': CODE, 'dimension': d, 'horizon': N,
            'requested_unhalved_error': str(error), 'radial_grid': B,
            'codeword_count': str(starts[-1]), 'body_hex': format(body, 'x'),
            'fixed_length_bits': (starts[-1]-1).bit_length(),
            'adaptive_error_upper': str(error/4), 'scope': SCOPE}


def encode(raw: dict, N: int, error: F) -> dict:
    x = target(raw); d = len(x)
    B, grids, starts = layers(N, error, d)
    Q = sum(q*q for q in x)
    i = nearest_algebraic(lambda v: radial_compare(Q, v), B)
    body = 0
    if i:
        axis = max(range(d), key=lambda a: (abs(x[a]), -a))
        s = 1 if x[axis] >= 0 else -1
        A = grids[i]
        digits = []
        for a in range(d):
            if a != axis:
                mag = nearest_algebraic(lambda v: ratio_compare(abs(x[a]), abs(x[axis]), Q, v), A)
                digits.append(sign(x[a])*mag)
        local = 2*axis+int(s == -1)
        for j in digits:
            local = local*(2*A+1)+j+A
        body = starts[i]+local
    return header(N, error, d, body)


def decode_vector(raw: dict) -> tuple[F, ...]:
    strict_keys(raw, {'schema','dimension','horizon','requested_unhalved_error','radial_grid',
                      'codeword_count','body_hex','fixed_length_bits','adaptive_error_upper','scope'}, 'code')
    require(raw['schema'] == CODE, 'wrong code schema')
    N = positive(raw['horizon'], 'horizon'); d = raw['dimension']
    error = fraction(raw['requested_unhalved_error'], 'error')
    B, grids, starts = layers(N, error, d)
    text = raw['body_hex']
    require(type(text) is str and text and all(c in '0123456789abcdef' for c in text), 'invalid hexadecimal')
    require(len(text) == 1 or text[0] != '0', 'noncanonical hexadecimal')
    require(len(text) <= max(1, ((starts[-1]-1).bit_length()+3)//4), 'overlong payload')
    body = int(text, 16)
    require(body < starts[-1], 'payload outside code alphabet')
    require(type(raw['radial_grid']) is int and type(raw['fixed_length_bits']) is int, 'nonintegral header')
    require(canonical(raw) == canonical(header(N, error, d, body)), 'altered header or error certificate')
    if body == 0:
        return (F(0),)*d
    i = bisect_right(starts, body)-1
    A = grids[i]; local = body-starts[i]; digits = []
    for _ in range(d-1):
        local, j = divmod(local, 2*A+1); digits.append(j-A)
    axis, sign_bit = divmod(local, 2)
    u = chart(axis, 1 if sign_bit == 0 else -1, tuple(reversed(digits)), A, d)
    r = F(2*i*B, B*B+i*i)
    return tuple(r*t for t in u)


def measurement(x: tuple[F, ...]) -> Instrument:
    require(len(x) in (2, 3) and all(isinstance(q, F) for q in x), 'invalid vector')
    require(sum(q*q for q in x) <= 1, 'decoded vector outside ball')
    x1, x2, x3 = (*x, F(0)) if len(x) == 2 else x
    mats = []
    for s in (1, -1):
        # Input-first Choi convention: each scalar-output Choi block is E_s^T.
        mats.append([[((1+s*x3)/2,F(0)),(s*x1/2,s*x2/2)],
                     [(s*x1/2,-s*x2/2),((1-s*x3)/2,F(0))]])
    den = lcm(*(q.denominator for m in mats for row in m for cell in row for q in cell))
    out = Instrument(2,1,den,[[[(int(a*den),int(b*den)) for a,b in row] for row in m] for m in mats])
    out.validate()
    return out


def decode(raw: dict) -> Instrument:
    return measurement(decode_vector(raw))


def verify(raw: dict, code: dict) -> bool:
    try:
        decode(code)
        return canonical(encode(raw, code['horizon'], F(code['requested_unhalved_error']))) == canonical(code)
    except (ValueError, TypeError, KeyError, IndexError, AttributeError, ZeroDivisionError):
        return False


def loads(text: str) -> dict:
    def unique(items):
        result = {}
        for k,v in items:
            require(k not in result, 'duplicate JSON field'); result[k] = v
        return result
    return json.loads(text, object_pairs_hook=unique)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['encode','decode','verify'])
    parser.add_argument('--input', required=True)
    parser.add_argument('--horizon', type=int)
    parser.add_argument('--error')
    parser.add_argument('--certificate')
    args = parser.parse_args()
    try:
        raw = loads(Path(args.input).read_text())
        if args.action == 'encode':
            require(args.horizon is not None and args.error is not None, 'horizon and error required')
            ans = encode(raw,args.horizon,fraction(args.error,'error'))
        elif args.action == 'decode':
            ans = decode(raw).to_dict()
        else:
            require(args.certificate is not None, 'certificate required')
            good = verify(raw,loads(Path(args.certificate).read_text()))
            ans = {'schema':'gtf74.target-replay/1','verified':good,
                   'scope':'Canonical target-bound replay, not universal proof certification.'}
            if not good:
                print(json.dumps(ans,indent=2,sort_keys=True)); return 1
        print(json.dumps(ans,indent=2,sort_keys=True)); return 0
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print('error: '+str(exc),file=sys.stderr); return 2


if __name__ == '__main__':
    raise SystemExit(main())
