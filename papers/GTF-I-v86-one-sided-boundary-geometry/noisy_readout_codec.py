#!/usr/bin/env python3
"""Exact supplied-description codes for noisy equatorial readouts.

Public visibility is NOT estimated or included as a variable target coordinate.
The output is a mathematical CP/TP instrument, not a physical classical device.
All precision choices, legality checks and target replay use integer/Fraction
arithmetic. JSON is an envelope; fixed_length_bits counts the payload index.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from math import isqrt, lcm
from pathlib import Path
import sys
from choi_streaming import Instrument
from instrument_streaming import mul
import preparation_codec as prep

TARGET = 'gtf73.noisy-readout-target/1'
CODE = 'gtf73.noisy-readout-code/1'
JOINT = 'gtf73.noisy-conditional-code/1'
SCOPE = ('Reusable supplied-description code at public visibility; complete adaptive '
         'unhalved trace error; no learning, workspace, or physical simulation claim.')


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def fraction(value: object, name: str) -> F:
    require(type(value) is str, name+' must be a canonical rational string')
    try:
        q = F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(name+' is not rational') from exc
    require(str(q) == value, name+' is not canonical')
    return q


def positive(value: object, name: str) -> int:
    require(type(value) is int and value >= 1, name+' must be a positive integer')
    return value


def strict_keys(raw: object, keys: set[str], name: str) -> None:
    require(type(raw) is dict and set(raw) == keys, name+' has missing or extra fields')


def canonical(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def target(raw: dict) -> tuple[F, tuple[F, F], list[Instrument] | None]:
    require(type(raw) is dict, 'target must be an object')
    keys = {'schema', 'visibility', 'direction'}
    if 'preparations' in raw:
        keys.add('preparations')
    strict_keys(raw, keys, 'target')
    require(raw['schema'] == TARGET, 'wrong target schema')
    lam = fraction(raw['visibility'], 'visibility')
    require(0 <= lam <= 1, 'visibility outside [0,1]')
    z = raw['direction']
    require(type(z) is list and len(z) == 2, 'two circle coordinates required')
    x, y = (fraction(z[i], 'direction') for i in range(2))
    require(x*x+y*y == 1, 'direction is not an exact unit vector')
    states = None
    if 'preparations' in raw:
        require(type(raw['preparations']) is list and len(raw['preparations']) == 2,
                'one conditional state for each of two outcomes is required')
        states = [Instrument.from_dict(s) for s in raw['preparations']]
        require(all(a.d == 1 and len(a.outcomes) == 1 for a in states),
                'conditional preparations must be single trace-one states')
        require(states[0].n == states[1].n, 'conditional output dimensions differ')
        require(all(canonical(a.to_dict()) == canonical(s)
                    for a, s in zip(states, raw['preparations'])),
                'conditional state is not canonical')
    return lam, (x, y), states


def ceil_sqrt(q: F) -> int:
    require(isinstance(q, F) and q >= 0, 'nonnegative Fraction required')
    k = isqrt(q.numerator // q.denominator)
    return k if k*k*q.denominator == q.numerator else k+1


def scale_squared(N: int, lam: F) -> F:
    positive(N, 'horizon')
    require(isinstance(lam, F) and 0 <= lam <= 1, 'invalid visibility')
    eta = 1-lam*lam
    return lam*lam*min(F(N*N), F(N)/eta) if eta else F(N*N)


def grid(N: int, lam: F, error: F) -> int:
    positive(N, 'horizon')
    require(isinstance(error, F) and 0 < error < 2, 'error must lie in (0,2)')
    return max(1, ceil_sqrt(16*scale_squared(N, lam)/(error*error))) if lam else 0


def chart_point(sign: int, digit: int, B: int) -> tuple[F, F]:
    require(type(sign) is int and sign in (-1, 1), 'invalid chart sign')
    positive(B, 'grid')
    require(type(digit) is int and -B <= digit <= B, 'digit outside chart')
    t = F(digit, B)
    return sign*(1-t*t)/(1+t*t), sign*2*t/(1+t*t)


def nearest(q: F) -> int:
    # Ties go toward positive infinity, including for negative inputs.
    t = q + F(1, 2)
    return t.numerator // t.denominator


def header(N: int, lam: F, error: F, B: int, body: int) -> dict:
    count = 4*B+2 if B else 1
    return {'schema': CODE, 'horizon': N, 'visibility': str(lam),
            'requested_unhalved_error': str(error), 'grid': B,
            'body_hex': format(body, 'x'), 'fixed_length_bits': (count-1).bit_length(),
            'angular_error_squared_upper': str(F(1, B*B)) if B else '0',
            'adaptive_error_squared_upper': str(scale_squared(N, lam)/(B*B)) if B else '0',
            'scope': SCOPE}


def encode_readout(raw: dict, N: int, error: F) -> dict:
    lam, (x, y), states = target(raw)
    require(states is None, 'use the conditional encoder for state outputs')
    B = grid(N, lam, error)
    body = 0
    if B:
        s = 1 if x >= 0 else -1
        t = s*y/(1+s*x)
        j = nearest(B*t)
        body = int(s == -1)*(2*B+1)+j+B
    ans = header(N, lam, error, B, body)
    decode_readout_parts(ans)
    return ans


def decode_readout_parts(raw: dict) -> tuple[F, tuple[F, F]]:
    keys = {'schema','horizon','visibility','requested_unhalved_error','grid',
            'body_hex','fixed_length_bits','angular_error_squared_upper',
            'adaptive_error_squared_upper','scope'}
    strict_keys(raw, keys, 'readout code')
    require(raw['schema'] == CODE, 'wrong readout code schema')
    N = positive(raw['horizon'], 'horizon')
    lam = fraction(raw['visibility'], 'visibility')
    error = fraction(raw['requested_unhalved_error'], 'error')
    B = grid(N, lam, error)
    require(type(raw['grid']) is int and raw['grid'] == B, 'noncanonical grid')
    count = 4*B+2 if B else 1
    text = raw['body_hex']
    require(type(text) is str and text and all(c in '0123456789abcdef' for c in text),
            'body must be lower-case hexadecimal')
    require(len(text) <= max(1, ((count-1).bit_length()+3)//4), 'overlong body')
    require(len(text) == 1 or text[0] != '0', 'noncanonical body')
    body = int(text, 16)
    require(body < count, 'body outside fixed-length code alphabet')
    require(type(raw['fixed_length_bits']) is int, 'payload bit count is not integral')
    require(canonical(raw) == canonical(header(N, lam, error, B, body)),
            'altered header or certificate')
    require(F(raw['adaptive_error_squared_upper']) <= error*error,
            'precision allocation does not meet requested error')
    if not B:
        return lam, (F(1), F(0))
    sign_bit, d = divmod(body, 2*B+1)
    return lam, chart_point(1 if sign_bit == 0 else -1, d-B, B)


def effects(lam: F, z: tuple[F, F]) -> list:
    x, y = z
    require(0 <= lam <= 1 and x*x+y*y == 1, 'invalid effect coordinates')
    return [[[(F(1,2), F(0)), (s*lam*x/2, -s*lam*y/2)],
             [(s*lam*x/2, s*lam*y/2), (F(1,2), F(0))]]
            for s in (1, -1)]


def assemble(lam: F, z: tuple[F, F], states: list[Instrument] | None = None) -> Instrument:
    if states is None:
        states = [Instrument(1,1,1,[[[(1,0)]]]) for _ in range(2)]
    require(len(states) == 2, 'two conditional states required')
    n = states[0].n
    for a in states:
        a.validate()
        require(a.d == 1 and a.n == n and len(a.outcomes) == 1,
                'invalid conditional state interface')
    mats = []
    for e, rho in zip(effects(lam, z), states):
        mats.append([[mul(e[j//n][i//n],
                          (F(rho.outcomes[0][i % n][j % n][0],rho.denominator),
                           F(rho.outcomes[0][i % n][j % n][1],rho.denominator)))
                      for j in range(2*n)] for i in range(2*n)])
    den = lcm(*(q.denominator for a in mats for row in a for cell in row for q in cell))
    ints = [[[(int(u*den),int(v*den)) for u,v in row] for row in a] for a in mats]
    obj = Instrument(2,n,den,ints)
    obj.validate()
    return obj


def decode_readout(raw: dict) -> Instrument:
    return assemble(*decode_readout_parts(raw))


def encode(raw: dict, N: int, error: F, ranks: list[int] | None = None) -> dict:
    lam, z, states = target(raw)
    if states is None:
        require(ranks is None, 'rank header only applies to conditional states')
        return encode_readout(raw, N, error)
    require(isinstance(error, F) and 0 < error < 2, 'invalid error')
    ranks = [states[0].n]*2 if ranks is None else ranks
    require(type(ranks) is list and len(ranks) == 2, 'two state rank bounds required')
    require(all(type(r) is int and 1 <= r <= states[0].n for r in ranks),
            'invalid conditional ranks')
    bare = {'schema':TARGET,'visibility':str(lam),'direction':[str(q) for q in z]}
    measurement = encode_readout(bare,N,error/2)
    codes = [prep.adaptive(a,N,error/4,[r]) for a,r in zip(states,ranks)]
    ans = {'schema':JOINT,'horizon':N,'requested_unhalved_error':str(error),
           'readout_code':measurement,'preparation_codes':codes,'rank_bounds':ranks,
           'fixed_length_bits':measurement['fixed_length_bits']+
                               sum(c['code']['fixed_length_bits'] for c in codes),
           'scope':SCOPE}
    decode(ans)
    return ans


def decode(raw: dict) -> Instrument:
    require(type(raw) is dict, 'code must be an object')
    if raw.get('schema') == CODE:
        return decode_readout(raw)
    strict_keys(raw, {'schema','horizon','requested_unhalved_error','readout_code',
                      'preparation_codes','rank_bounds','fixed_length_bits','scope'}, 'conditional code')
    require(raw['schema'] == JOINT and raw['scope'] == SCOPE, 'invalid conditional schema/scope')
    N = positive(raw['horizon'], 'horizon')
    error = fraction(raw['requested_unhalved_error'], 'error')
    require(0 < error < 2, 'error outside range')
    lam,z = decode_readout_parts(raw['readout_code'])
    require(raw['readout_code']['horizon'] == N and
            F(raw['readout_code']['requested_unhalved_error']) == error/2,
            'readout budget or horizon mismatch')
    codes = raw['preparation_codes']
    require(type(codes) is list and len(codes) == 2, 'two preparation codes required')
    states = [prep.validate_adaptive(c) for c in codes]
    require(all(a.d == 1 and len(a.outcomes) == 1 for a in states) and states[0].n == states[1].n,
            'invalid decoded row interface')
    ranks = raw['rank_bounds']
    require(type(ranks) is list and len(ranks) == 2 and
            all(type(r) is int and 1 <= r <= states[0].n for r in ranks), 'invalid ranks')
    for c,r in zip(codes,ranks):
        require(c['horizon'] == N and F(c['requested_unhalved_error']) == error/4 and
                c['code']['rank_bounds'] == [r], 'state budget, horizon or rank mismatch')
        # The inherited decoder checks mathematical legality; this wrapper also
        # rejects extra envelope fields; target verification compares every
        # field, including inherited scope strings, by canonical replay.
        strict_keys(c, {'schema','horizon','requested_unhalved_error','error_squared_upper','code','scope'},
                    'preparation envelope')
        strict_keys(c['code'], {'schema','convention','input_dimension','output_dimension','outcome_count',
                               'rank_bounds','pivot_sets','grid','factor_coordinates','rank_family_dimension',
                               'body_hex','fixed_length_bits','one_use_error_squared_upper','scope'},
                    'preparation body')
    expected = raw['readout_code']['fixed_length_bits']+sum(c['code']['fixed_length_bits'] for c in codes)
    require(type(raw['fixed_length_bits']) is int and raw['fixed_length_bits'] == expected, 'payload mismatch')
    return assemble(lam,z,states)


def verify(raw_target: dict, code: dict) -> bool:
    try:
        decode(code)
        expected = encode(raw_target, code['horizon'], F(code['requested_unhalved_error']),
                          code.get('rank_bounds') if code.get('schema') == JOINT else None)
        return canonical(expected) == canonical(code)
    except (ValueError, TypeError, KeyError, IndexError, AttributeError, ZeroDivisionError):
        return False


def load(path: str) -> dict:
    def pairs(items):
        d = {}
        for k,v in items:
            require(k not in d, 'duplicate JSON field')
            d[k] = v
        return d
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action', choices=['encode','decode','verify'])
    ap.add_argument('--input', required=True)
    ap.add_argument('--horizon', type=int)
    ap.add_argument('--error')
    ap.add_argument('--ranks')
    ap.add_argument('--certificate')
    a = ap.parse_args()
    try:
        raw = load(a.input)
        if a.action == 'encode':
            e = fraction(a.error,'error')
            result = encode(raw, a.horizon, e, json.loads(a.ranks) if a.ranks else None)
        elif a.action == 'decode':
            result = decode(raw).to_dict()
        else:
            require(bool(a.certificate), '--certificate is required')
            require(verify(raw,load(a.certificate)), 'target-bound canonical replay failed')
            result = {'schema':'gtf73.noisy-verification/1','status':'success',
                      'target_bound':True,'exact_arithmetic':True}
        print(json.dumps(result, sort_keys=True, indent=2))
    except (ValueError, TypeError, KeyError, IndexError, ZeroDivisionError, OSError) as exc:
        print(json.dumps({'status':'error','error':str(exc)}), file=sys.stderr)
        sys.exit(2)

if __name__ == '__main__':
    main()
