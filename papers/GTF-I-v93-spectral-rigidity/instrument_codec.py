#!/usr/bin/env python3
"""Exact intrinsic coordinate code for input-first unnormalized instruments.

This encodes supplied rational data, not an unknown channel. Decoding checks
CP and joint TP but cannot certify proximity to an unspecified target.
The code length below excludes the separately stored JSON parameter header.
No floating-point decisions, quantum preparation, or random sampling occur.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from math import isqrt
import json
from pathlib import Path
import sys
from typing import Iterator
from choi_streaming import Instrument, constants, rational_psd, partial_trace
from instrument_streaming import ZERO, add, conj, identity, plus, zero, toward_zero


def positive_int(x: object, name: str) -> int:
    if type(x) is not int or x < 1:
        raise ValueError(name + ' must be a positive integer')
    return x


def intrinsic_dimension(d: int, n: int, m: int) -> int:
    constants(d, n, m)
    return d*d*(m*n*n - 1)


def coordinates(d: int, n: int, m: int, ay: int = 0, ao: int = 0) -> Iterator[tuple[int, int, int, int]]:
    """Retained independent real coordinates: outcome,row,column,component."""
    constants(d, n, m)
    if type(ay) is not int or not 0 <= ay < m or type(ao) is not int or not 0 <= ao < n:
        raise ValueError('invalid omitted outcome/output coordinate')
    q = d*n
    for y in range(m):
        for u in range(q):
            for v in range(u, q):
                if y == ay and u % n == ao and v % n == ao:
                    continue
                for component in range(1 if u == v else 2):
                    yield y, u, v, component


def pack_digits(digits: list[int], B: int) -> int:
    positive_int(B, 'grid')
    code = 0
    for z in digits:
        if type(z) is not int or not -B <= z <= B:
            raise ValueError('digit outside certified coordinate range')
        code = code*(2*B+1) + z+B
    return code


def unpack_digits(code: int, B: int, s: int) -> list[int]:
    positive_int(B, 'grid')
    if type(s) is not int or s < 0 or type(code) is not int or code < 0:
        raise ValueError('invalid code or dimension')
    M = 2*B+1
    if code >= M**s:
        raise ValueError('code is outside its fixed-length alphabet')
    digits = [0]*s
    for j in range(s-1, -1, -1):
        code, v = divmod(code, M)
        digits[j] = v-B
    return digits


def fill_affine(digits: list[int], d: int, n: int, m: int, B: int,
                ay: int = 0, ao: int = 0) -> list:
    """Integer B*Q, before adding the positive buffer; exact marginal."""
    positive_int(B, 'grid')
    coords = list(coordinates(d, n, m, ay, ao))
    if len(digits) != len(coords):
        raise ValueError('wrong number of intrinsic digits')
    mats = [zero(d*n) for _ in range(m)]
    for z, (y, u, v, c) in zip(digits, coords):
        if type(z) is not int or abs(z) > B:
            raise ValueError('invalid coordinate digit')
        value = list(mats[y][u][v]); value[c] = z
        mats[y][u][v] = tuple(value)
        mats[y][v][u] = conj(tuple(value))
    for i in range(d):
        for j in range(d):
            value = (B if i == j else 0, 0)
            for y in range(m):
                for alpha in range(n):
                    if (y, alpha) != (ay, ao):
                        z = mats[y][i*n+alpha][j*n+alpha]
                        value = (value[0]-z[0], value[1]-z[1])
            mats[ay][i*n+ao][j*n+ao] = value
    return mats


def decode_digits(digits: list[int], d: int, n: int, m: int, B: int,
                  ay: int = 0, ao: int = 0) -> Instrument:
    mats = fill_affine(digits, d, n, m, B, ay, ao)
    c, _ = constants(d, n, m)
    for mat in mats:
        for u in range(d*n):
            mat[u][u] = add(mat[u][u], (c, 0))
    obj = Instrument(d, n, B+m*n*c, mats)
    obj.validate()  # Arbitrary in-range words need not be PSD.
    return obj


def encode(target: Instrument, B: int, ay: int = 0, ao: int = 0,
           preserve_zeros: bool = False) -> dict:
    target.validate(); positive_int(B, 'grid')
    if type(preserve_zeros) is not bool:
        raise ValueError('preserve_zeros must be Boolean')
    active = [y for y, mat in enumerate(target.outcomes)
              if not preserve_zeros or any(z != ZERO for row in mat for z in row)]
    sub = Instrument(target.d, target.n, target.denominator, [target.outcomes[y] for y in active])
    sub.validate()
    coords = list(coordinates(sub.d, sub.n, len(active), ay, ao))
    digits = [toward_zero(B*sub.outcomes[y][u][v][c], sub.denominator) for y,u,v,c in coords]
    s = intrinsic_dimension(sub.d, sub.n, len(active))
    if len(digits) != s:
        raise RuntimeError('internal coordinate count mismatch')
    candidate = decode_digits(digits, sub.d, sub.n, len(active), B, ay, ao)
    _, K = constants(sub.d, sub.n, len(active))
    out = {'schema':'gtf67.intrinsic-instrument-code/1',
           'convention':'input-first-unnormalized', 'input_dimension':sub.d,
           'output_dimension':sub.n, 'outcome_count':len(target.outcomes),
           'active_outcomes':active, 'preserve_zeros':preserve_zeros,
           'anchor_outcome':ay, 'anchor_output':ao, 'grid':B,
           'intrinsic_dimension':s, 'payload_hex':format(pack_digits(digits,B),'x'),
           'fixed_length_payload_bits':((2*B+1)**s-1).bit_length(),
           'diamond_error_upper':str(Fraction(K,candidate.denominator)),
           'scope':'Proximity bound requires the encoder target; decoding alone certifies legality only. Header, validation and full matrix output are separate resources.'}
    decode(out)
    return out


def decode(raw: dict) -> Instrument:
    if not isinstance(raw, dict) or raw.get('schema') != 'gtf67.intrinsic-instrument-code/1':
        raise ValueError('invalid codec schema')
    if raw.get('convention') != 'input-first-unnormalized':
        raise ValueError('unsupported tensor convention')
    d = positive_int(raw.get('input_dimension'), 'input dimension')
    n = positive_int(raw.get('output_dimension'), 'output dimension')
    count = positive_int(raw.get('outcome_count'), 'outcome count')
    B = positive_int(raw.get('grid'), 'grid')
    active = raw.get('active_outcomes')
    if not isinstance(active,list) or not active or any(type(y) is not int or not 0 <= y < count for y in active):
        raise ValueError('invalid active-outcome mask')
    if active != sorted(set(active)):
        raise ValueError('active-outcome mask must be strictly increasing')
    preserve = raw.get('preserve_zeros')
    if type(preserve) is not bool or (not preserve and active != list(range(count))):
        raise ValueError('inconsistent zero-outcome mask')
    m = len(active); s = intrinsic_dimension(d,n,m)
    if type(raw.get('intrinsic_dimension')) is not int or raw['intrinsic_dimension'] != s:
        raise ValueError('intrinsic dimension mismatch')
    bits = ((2*B+1)**s-1).bit_length()
    if type(raw.get('fixed_length_payload_bits')) is not int or raw['fixed_length_payload_bits'] != bits:
        raise ValueError('payload bit count mismatch')
    h = raw.get('payload_hex')
    if not isinstance(h,str) or not h or any(c not in '0123456789abcdef' for c in h):
        raise ValueError('payload must be canonical unsigned hexadecimal')
    # Bound parsing storage by the alphabet, not by an adversarial hex field.
    if len(h) > max(1, (bits+3)//4) or (len(h)>1 and h[0]=='0'):
        raise ValueError('overlong or noncanonical payload')
    digits = unpack_digits(int(h,16),B,s)
    obj = decode_digits(digits,d,n,m,B,raw.get('anchor_outcome'),raw.get('anchor_output'))
    _,K = constants(d,n,m)
    if raw.get('diamond_error_upper') != str(Fraction(K,obj.denominator)):
        raise ValueError('tampered error formula')
    mats = [zero(d*n) for _ in range(count)]
    for y,mat in zip(active,obj.outcomes):
        mats[y] = mat
    ans = Instrument(d,n,obj.denominator,mats);ans.validate()
    return ans


def verify(target: Instrument, certificate: dict) -> bool:
    try:
        expected = encode(target,certificate['grid'],certificate['anchor_outcome'],
                          certificate['anchor_output'],certificate['preserve_zeros'])
        return expected == certificate
    except (ValueError,TypeError,KeyError,IndexError,AttributeError):
        return False


def has_margin(target: Instrument, a: Fraction) -> bool:
    target.validate()
    a = Fraction(a)
    for mat in target.outcomes:
        b = [[(Fraction(x),Fraction(y)) for x,y in row] for row in mat]
        for u in range(target.d*target.n):
            b[u][u] = (b[u][u][0]-a*target.denominator, b[u][u][1])
        if not rational_psd(b):
            return False
    return True


def adaptive_grid(d: int, n: int, m: int, N: int,
                  a: Fraction, delta: Fraction) -> int:
    positive_int(N,'horizon');constants(d,n,m)
    a,delta = Fraction(a),Fraction(delta)
    if not 0<a<Fraction(1,m*n) or not 0<delta<1:
        raise ValueError('require 0<a<1/(mn) and 0<delta<1')
    _,K = constants(d,n,m)
    sqrt_ceiling = isqrt(N)
    if sqrt_ceiling**2 < N:
        sqrt_ceiling += 1
    x = Fraction(K,a)*(2+Fraction(4*sqrt_ceiling,delta))
    return -(-x.numerator//x.denominator)


def encode_adaptive(target: Instrument, N: int, a: Fraction, delta: Fraction) -> dict:
    if not has_margin(target,a):
        raise ValueError('target does not have the asserted Choi eigenvalue margin')
    B = adaptive_grid(target.d,target.n,len(target.outcomes),N,a,delta)
    return {'schema':'gtf67.adaptive-code/1','horizon':N,'margin':str(Fraction(a)),
            'stopped_joint_trace_error_upper':str(Fraction(delta)),
            'code':encode(target,B),
            'scope':'Same memoryless decoded quantum instrument, reused by any common causal quantum tester with public stopping; not a physical classical simulator.'}


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['encode','decode','verify','adaptive'])
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--grid',type=int,default=4096)
    p.add_argument('--anchor-outcome',type=int,default=0)
    p.add_argument('--anchor-output',type=int,default=0)
    p.add_argument('--preserve-zeros',action='store_true')
    p.add_argument('--certificate',type=Path)
    p.add_argument('--horizon',type=int,default=100)
    p.add_argument('--margin',type=Fraction,default=Fraction(1,16))
    p.add_argument('--error',type=Fraction,default=Fraction(1,4))
    args=p.parse_args()
    try:
        raw=json.loads(args.input.read_text())
        if args.mode=='decode':
            ans=decode(raw).to_dict()
        else:
            target=Instrument.from_dict(raw)
            if args.mode=='encode':
                ans=encode(target,args.grid,args.anchor_outcome,args.anchor_output,args.preserve_zeros)
            elif args.mode=='adaptive':
                ans=encode_adaptive(target,args.horizon,args.margin,args.error)
            else:
                if args.certificate is None:
                    raise ValueError('--certificate is required')
                ok=verify(target,json.loads(args.certificate.read_text()))
                ans={'status':'success' if ok else 'rejected','verified':ok}
                if not ok:
                    print(json.dumps(ans,sort_keys=True));sys.exit(1)
        print(json.dumps(ans,indent=2,sort_keys=True))
    except (ValueError,TypeError,KeyError,IndexError,OSError) as e:
        p.exit(2,'codec error: '+str(e)+'\n')


if __name__=='__main__':
    main()
