#!/usr/bin/env python3
"""Finite exact interior binary-effect descriptions (Theorem interiorcodec79).

This is supplied-matrix encoding, not an unknown-device learner. The complete
public dictionary is reconstructed before any payload is emitted. Enumeration
is finite but can be enormous; no polynomial-time or workspace claim is made.
A candidate cutoff raises IncompleteConstruction, not a partial codebook.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from itertools import islice
import json
from math import isqrt
from pathlib import Path
import sys
from typing import Iterable, Iterator
import sympy as sp
import matrix_metric as mm
import matrix_codec as mc

CODE = 'gtf79.interior-effect-code/1'
SUMMARY = 'gtf79.interior-codebook-summary/1'
PREFIX = 'gtf79.interior-codec-prefix-audit/1'
FIELDS = {'schema', 'dimension', 'horizon', 'accuracy', 'payload'}
IncompleteConstruction = mc.IncompleteConstruction


def ceil_sqrt(n: int) -> int:
    n = mm.positive_integer(n, 'horizon')
    a = isqrt(n)
    return a if a*a == n else a+1


def parameters(d: int, N: int, delta: str | sp.Rational) -> tuple[int, sp.Rational]:
    d = mm.positive_integer(d, 'dimension')
    k, delta = ceil_sqrt(N), mc.accuracy(delta)
    v = 128*d*k/delta
    p, q = v.as_numer_denom()
    return (int(p)+int(q)-1)//int(q), delta/(16*k)


def interior(value: sp.MatrixBase, *, expanded: bool = False) -> sp.ImmutableMatrix:
    value = mc.rational_hermitian(value)
    margin = sp.Rational(1, 8) if expanded else sp.Rational(1, 4)
    I = sp.eye(value.rows)
    mm.require(mm.is_positive_semidefinite(value-margin*I)
               and mm.is_positive_semidefinite((1-margin)*I-value),
               'matrix is outside the specified interior')
    return value


def op_leq(H: sp.MatrixBase, t: sp.Rational) -> bool:
    """Exact operator-norm comparison, including equality and zero pivots."""
    H = mc.rational_hermitian(H)
    mm.require(getattr(t, 'is_Rational', False) is True and t >= 0,
               'threshold must be a nonnegative exact rational')
    if H.is_diagonal():
        return all(abs(H[i, i]) <= t for i in range(H.rows))
    I = sp.eye(H.rows)
    return (mm.is_positive_semidefinite(t*I-H)
            and mm.is_positive_semidefinite(t*I+H))


def grid(d: int, K: int) -> Iterator[sp.ImmutableMatrix]:
    """Subsequence of the inherited lexicographic grid lying in [I/8,7I/8]."""
    for G in mc.finite_grid(d, K):
        I = sp.eye(d)
        if (mm.is_positive_semidefinite(G-I/8)
                and mm.is_positive_semidefinite(7*I/8-G)):
            yield G


def greedy(candidates: Iterable[sp.MatrixBase], t: sp.Rational, *,
           max_candidates: int | None = None) -> tuple[tuple[sp.ImmutableMatrix, ...], int]:
    """A finite-stream kernel. Only construct() supplies the entire public grid.

    The limit counts admissible candidates, not all pruned coordinate tuples or
    wall-clock time. No result is returned if the supplied stream is incomplete.
    """
    mm.require(getattr(t, 'is_Rational', False) is True and t > 0,
               'threshold must be a positive exact rational')
    if max_candidates is not None:
        mm.positive_integer(max_candidates, 'candidate limit')
    centres: list[sp.ImmutableMatrix] = []
    count, dimension = 0, None
    for raw in candidates:
        count += 1
        if max_candidates is not None and count > max_candidates:
            raise IncompleteConstruction('complete grid not exhausted; no codebook or payload produced')
        G = interior(raw, expanded=True)
        if dimension is None:
            dimension = G.rows
        mm.require(G.rows == dimension, 'candidate dimensions differ')
        if all(not op_leq(G-C, t) for C in centres):
            centres.append(G)
    mm.require(count > 0, 'empty interior candidate stream')
    return tuple(centres), count


@dataclass(frozen=True)
class Codebook:
    dimension: int
    horizon: int
    accuracy: sp.Rational
    denominator: int
    threshold: sp.Rational
    centres: tuple[sp.ImmutableMatrix, ...]
    legal_candidates: int

    @property
    def payload_bits(self) -> int:
        return (len(self.centres)-1).bit_length()


def construct(d: int, N: int, delta: str | sp.Rational, *,
              max_candidates: int | None = None) -> Codebook:
    d, N = mm.positive_integer(d, 'dimension'), mm.positive_integer(N, 'horizon')
    delta = mc.accuracy(delta)
    K, t = parameters(d, N, delta)
    centres, count = greedy(grid(d, K), t, max_candidates=max_candidates)
    return Codebook(d, N, delta, K, t, centres, count)


def quantize(E: sp.MatrixBase, K: int) -> sp.ImmutableMatrix:
    E = interior(E)
    K = mm.positive_integer(K, 'denominator')
    mm.require(K >= 128*E.rows, 'grid too coarse for the guaranteed interior rounding')
    d, G = E.rows, sp.zeros(E.rows)
    for i in range(d):
        G[i, i] = mc.nearest_grid_rational(E[i, i], K)
        for j in range(i+1, d):
            a, b = mm.gaussian_parts(E[i, j])
            z = mc.nearest_grid_rational(a, K)+sp.I*mc.nearest_grid_rational(b, K)
            G[i, j], G[j, i] = z, sp.conjugate(z)
    G = interior(G, expanded=True)
    mm.require(op_leq(G-E, sp.Rational(d, K)), 'rational rounding bound failed')
    return G


def encode(E: sp.MatrixBase, book: Codebook) -> dict:
    E = interior(E)
    mm.require(E.rows == book.dimension, 'source dimension differs from dictionary')
    G = quantize(E, book.denominator)
    for index, C in enumerate(book.centres):
        if op_leq(G-C, book.threshold):
            payload = format(index, '0'+str(book.payload_bits)+'b') if book.payload_bits else ''
            return {'schema': CODE, 'dimension': book.dimension, 'horizon': book.horizon,
                    'accuracy': str(book.accuracy), 'payload': payload}
    raise RuntimeError('completed public dictionary failed to cover the rounded source')


def decode_with_book(raw: dict, book: Codebook) -> sp.ImmutableMatrix:
    mm.strict_keys(raw, FIELDS, 'interior code')
    mm.require(raw['schema'] == CODE, 'wrong interior code schema')
    mm.require(mm.positive_integer(raw['dimension'], 'dimension') == book.dimension
               and mm.positive_integer(raw['horizon'], 'horizon') == book.horizon
               and mc.accuracy(raw['accuracy']) == book.accuracy,
               'public parameters differ from dictionary')
    word = raw['payload']
    mm.require(type(word) is str and len(word) == book.payload_bits
               and all(c in '01' for c in word), 'malformed fixed-length payload')
    index = int(word, 2) if word else 0
    return (book.centres[index] if index < len(book.centres)
            else sp.ImmutableMatrix(sp.eye(book.dimension)/2))


def decode(raw: dict, *, max_candidates: int | None = None) -> sp.ImmutableMatrix:
    mm.strict_keys(raw, FIELDS, 'interior code')
    mm.require(raw['schema'] == CODE, 'wrong interior code schema')
    book = construct(raw['dimension'], raw['horizon'], raw['accuracy'],
                     max_candidates=max_candidates)
    return decode_with_book(raw, book)


def summary(book: Codebook) -> dict:
    return {'schema': SUMMARY, 'complete': True, 'dimension': book.dimension,
            'horizon': book.horizon, 'accuracy': str(book.accuracy),
            'denominator': book.denominator, 'threshold': str(book.threshold),
            'legal_candidates': book.legal_candidates, 'centres': len(book.centres),
            'payload_bits': book.payload_bits, 'unknown_device_learning_executed': False,
            'polynomial_time_claimed': False}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action', choices=['encode', 'decode', 'summary', 'audit-prefix'])
    ap.add_argument('--input', type=Path)
    ap.add_argument('--dimension', type=int)
    ap.add_argument('--horizon', type=int)
    ap.add_argument('--accuracy')
    ap.add_argument('--max-candidates', type=int)
    ap.add_argument('--prefix-count', type=int, default=4)
    args = ap.parse_args()
    try:
        if args.action == 'decode':
            mm.require(args.input is not None, '--input is required')
            raw = json.loads(args.input.read_text())
            result = mc.effect_to_json(decode(raw, max_candidates=args.max_candidates))
        elif args.action == 'encode':
            mm.require(args.input is not None, '--input is required')
            E = interior(mc.effect_from_json(json.loads(args.input.read_text())))
            book = construct(E.rows, args.horizon, args.accuracy, max_candidates=args.max_candidates)
            result = encode(E, book)
        elif args.action == 'summary':
            result = summary(construct(args.dimension, args.horizon, args.accuracy,
                                       max_candidates=args.max_candidates))
        else:
            n = mm.positive_integer(args.prefix_count, 'prefix count')
            K, t = parameters(args.dimension, args.horizon, args.accuracy)
            observed = list(islice(grid(args.dimension, K), n))
            result = {'schema': PREFIX, 'scope': 'finite exact kernel prefix, not a dictionary',
                      'complete': False, 'observed_candidates': len(observed),
                      'denominator': K, 'threshold': str(t),
                      'candidates': [mm.matrix_to_json(G) for G in observed]}
        print(json.dumps(result, indent=2, sort_keys=True))
    except (ValueError, TypeError, OSError, RuntimeError) as exc:
        print(json.dumps({'status': 'error', 'error_type': type(exc).__name__,
                          'message': str(exc), 'codebook_or_payload_produced': False}), file=sys.stderr)
        raise SystemExit(2)


if __name__ == '__main__':
    main()
