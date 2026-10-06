#!/usr/bin/env python3
"""Exact supplied-description codec for fixed-readout conditional instruments.

Only Choi matrices block diagonal in the fixed input basis are encoded. The
code preserves conditional rank bounds and zero blocks. This is not a learning
algorithm or a physical classical simulator. JSON is a transport envelope;
fixed_length_bits counts the row headers and fixed-length integer bodies.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
from math import isqrt, lcm
from pathlib import Path
import sys
from choi_streaming import Instrument
from instrument_streaming import ZERO, zero
import preparation_codec as prep

SCHEMA = 'gtf71.conditional-instrument-code/1'


def rows(target: Instrument) -> list[Instrument]:
    """Reject, rather than erase, all off-diagonal input blocks of a target."""
    target = Instrument.from_dict(target.to_dict())
    d, n = target.d, target.n
    for mat in target.outcomes:
        for i in range(d*n):
            for j in range(d*n):
                if i//n != j//n and mat[i][j] != ZERO:
                    raise ValueError('target is not fixed-readout block diagonal')
    out = []
    for x in range(d):
        mats = [[row[x*n:(x+1)*n] for row in mat[x*n:(x+1)*n]]
                for mat in target.outcomes]
        a = Instrument(1, n, target.denominator, mats)
        a.validate(); out.append(a)
    return out


def join(row_instruments: list[Instrument]) -> Instrument:
    if not row_instruments: raise ValueError('at least one input row is required')
    d = len(row_instruments); n = row_instruments[0].n
    m = len(row_instruments[0].outcomes)
    for a in row_instruments:
        a.validate()
        if a.d != 1 or a.n != n or len(a.outcomes) != m:
            raise ValueError('incompatible conditional row dimensions')
    den = lcm(*(a.denominator for a in row_instruments))
    mats = [zero(d*n) for _ in range(m)]
    for x, a in enumerate(row_instruments):
        scale = den//a.denominator
        for y, mat in enumerate(a.outcomes):
            for i in range(n):
                for j in range(n):
                    r, s = mat[i][j]
                    mats[y][x*n+i][x*n+j] = (scale*r, scale*s)
    result = Instrument(d, n, den, mats); result.validate()
    return result


def retract(centre: Instrument) -> Instrument:
    """K -> K composed with fixed-basis dephasing, not a rank projection."""
    centre = Instrument.from_dict(centre.to_dict())
    n, d = centre.n, centre.d
    mats = [zero(d*n) for _ in centre.outcomes]
    for y, mat in enumerate(centre.outcomes):
        for x in range(d):
            for i in range(n):
                for j in range(n):
                    mats[y][x*n+i][x*n+j] = mat[x*n+i][x*n+j]
    out = Instrument(d, n, centre.denominator, mats); out.validate()
    return out


def rank_data(raw: object, d: int, n: int, m: int) -> list[list[int]]:
    if not isinstance(raw, list) or len(raw) != d:
        raise ValueError('one list of public conditional ranks per input row is required')
    return [prep.ranks_check(r, n, m) for r in raw]


def canonical_fraction(raw: object, name: str) -> Fraction:
    if type(raw) is not str: raise ValueError(name+' must be a canonical fraction string')
    try: q = Fraction(raw)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(name+' is not a rational number') from exc
    if str(q) != raw: raise ValueError(name+' is not canonical')
    return q


def ceil_sqrt(q: Fraction) -> int:
    if not isinstance(q, Fraction) or q < 0: raise ValueError('nonnegative rational required')
    k = isqrt(q.numerator//q.denominator)
    return k + int(k*k*q.denominator < q.numerator)


def grid_for(N: int, V: int, error: Fraction) -> int:
    prep.positive(N, 'horizon')
    if type(V) is not int or V < 0: raise ValueError('invalid family dimension')
    if not isinstance(error, Fraction) or not 0 < error < 2:
        raise ValueError('unhalved error must be rational and strictly between zero and two')
    return max(1, ceil_sqrt(Fraction(16*N*V)/error**2))


def encode(target: Instrument, N: int, error: Fraction,
           ranks: list[list[int]] | None = None) -> dict:
    rr = rows(target); d, n, m = target.d, target.n, len(target.outcomes)
    ranks = [[n]*m for _ in range(d)] if ranks is None else rank_data(ranks, d, n, m)
    V = sum(prep.rank_dimension(n, r) for r in ranks)
    B = grid_for(N, V, error)
    codes = [prep.encode(a, B, r) for a, r in zip(rr, ranks)]
    loss = sum(c['factor_coordinates']-1 for c in codes)
    out = {'schema':SCHEMA, 'convention':'input-first-unnormalized',
           'input_dimension':d, 'output_dimension':n, 'outcome_count':m,
           'horizon':N, 'requested_unhalved_error':str(error), 'rank_bounds':ranks,
           'rank_family_dimension':V, 'grid':B, 'rows':codes,
           'fixed_length_bits':sum(c['fixed_length_bits'] for c in codes),
           'error_squared_upper':str(Fraction(16*N*loss, B*B)),
           'scope':'Supplied fixed-readout mathematical instrument description. Public dimensions, ranks, horizon and error are not payload. Row masks and integer bodies are charged; expanded matrices and workspace are separate. Bare decoding does not bind an unknown target.'}
    decode(out)
    return out


def decode(raw: dict) -> Instrument:
    if not isinstance(raw, dict) or raw.get('schema') != SCHEMA:
        raise ValueError('invalid conditional-code schema')
    if raw.get('convention') != 'input-first-unnormalized':
        raise ValueError('unsupported Choi convention')
    d = prep.positive(raw.get('input_dimension'), 'input dimension')
    n = prep.positive(raw.get('output_dimension'), 'output dimension')
    m = prep.positive(raw.get('outcome_count'), 'outcome count')
    N = prep.positive(raw.get('horizon'), 'horizon')
    error = canonical_fraction(raw.get('requested_unhalved_error'), 'requested error')
    ranks = rank_data(raw.get('rank_bounds'), d, n, m)
    V = sum(prep.rank_dimension(n, r) for r in ranks)
    B = grid_for(N, V, error)
    for key, value in [('rank_family_dimension', V), ('grid', B)]:
        if type(raw.get(key)) is not int or raw[key] != value:
            raise ValueError(key+' mismatch')
    codes = raw.get('rows')
    if not isinstance(codes, list) or len(codes) != d:
        raise ValueError('conditional row count mismatch')
    decoded = []
    for c, r in zip(codes, ranks):
        a = prep.decode(c)
        if (a.d != 1 or a.n != n or len(a.outcomes) != m or
                c['grid'] != B or c['rank_bounds'] != r):
            raise ValueError('conditional row/public header mismatch')
        decoded.append(a)
    bits = sum(c['fixed_length_bits'] for c in codes)
    if type(raw.get('fixed_length_bits')) is not int or raw['fixed_length_bits'] != bits:
        raise ValueError('payload length mismatch')
    bound = Fraction(16*N*sum(c['factor_coordinates']-1 for c in codes), B*B)
    if canonical_fraction(raw.get('error_squared_upper'), 'error certificate') != bound:
        raise ValueError('error certificate mismatch')
    if bound > error**2: raise ValueError('insufficient accuracy certificate')
    return join(decoded)


def verify(target: Instrument, raw: dict) -> bool:
    decode(raw)
    expected = encode(target, raw['horizon'], Fraction(raw['requested_unhalved_error']),
                      raw['rank_bounds'])
    if json.dumps(expected, sort_keys=True) != json.dumps(raw, sort_keys=True):
        raise ValueError('certificate is not the canonical encoding of this target')
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ['encode','decode','verify','retract']:
        p = sub.add_parser(command); p.add_argument('--input', required=True)
        if command == 'encode':
            p.add_argument('--horizon', type=int, required=True)
            p.add_argument('--error', required=True)
            p.add_argument('--ranks', help='JSON matrix of conditional output-rank bounds')
        if command == 'verify': p.add_argument('--certificate', required=True)
    args = parser.parse_args()
    try:
        raw = json.loads(Path(args.input).read_text())
        if args.command == 'decode': result = decode(raw).to_dict()
        elif args.command == 'retract': result = retract(Instrument.from_dict(raw)).to_dict()
        elif args.command == 'encode':
            result = encode(Instrument.from_dict(raw), args.horizon, Fraction(args.error),
                            None if args.ranks is None else json.loads(args.ranks))
        else:
            certificate = json.loads(Path(args.certificate).read_text())
            verify(Instrument.from_dict(raw), certificate)
            result = {'schema':'gtf71.conditional-verification/1','status':'success',
                      'target_bound':True, 'scope':'Canonical exact re-encoding and legality; not a universal proof or independent priority certificate.'}
        print(json.dumps(result, indent=2, sort_keys=True)); return 0
    except (ValueError, TypeError, KeyError, OSError, ZeroDivisionError) as exc:
        print('conditional codec: '+str(exc), file=sys.stderr); return 2


if __name__ == '__main__': raise SystemExit(main())
