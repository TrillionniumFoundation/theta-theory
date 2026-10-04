#!/usr/bin/env python3
"""Finite exact rational code for ordered binary matrix effects.

This is the exhaustive construction in Theorem thm:matrixcodec77, using
the exact Sylvester and PSD routines of matrix_metric.py. The public
parameters are (dimension, horizon, accuracy). No custom dictionary is
accepted by the decoder. A complete dictionary is reconstructed before
the fixed payload length is determined.

The full enumeration can be extremely expensive. A resource cutoff raises
IncompleteConstruction and never returns an incomplete code. audit-prefix
is explicitly a kernel audit and does not produce a code. The source is a
supplied Gaussian-rational effect; this program does not learn a device.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from itertools import product
import json
from math import isqrt
from pathlib import Path
import sys
from typing import Iterable, Iterator

import sympy as sp

import matrix_metric as mm


EFFECT = "gtf77.matrix-effect/1"
CODE = "gtf77.matrix-effect-code/1"
SUMMARY = "gtf77.matrix-effect-codebook-summary/1"
PREFIX = "gtf77.matrix-effect-codec-prefix-audit/1"
THEOREM = "thm:matrixcodec77"
EFFECT_FIELDS = {"schema", "dimension", "effect"}
CODE_FIELDS = {"schema", "dimension", "horizon", "accuracy", "payload"}


class IncompleteConstruction(ValueError):
    """A finite resource limit was reached before full enumeration."""


def accuracy(value: str | sp.Rational) -> sp.Rational:
    if type(value) is str:
        value = mm.rational(value, "accuracy")
    mm.require(getattr(value, "is_Rational", False) is True
               and 0 < value <= 1,
               "accuracy must be an exact rational in (0, 1]")
    return sp.Rational(value)


def rational_hermitian(value: sp.MatrixBase) -> sp.ImmutableMatrix:
    mm.require(isinstance(value, sp.MatrixBase)
               and value.rows == value.cols and value.rows > 0,
               "a nonempty square matrix is required")
    value = sp.ImmutableMatrix(value.applyfunc(mm.gaussian))
    mm.require(value == value.adjoint(), "matrix must be Hermitian")
    return value


def legal_effect(value: sp.MatrixBase) -> sp.ImmutableMatrix:
    value = rational_hermitian(value)
    mm.require(mm.is_positive_semidefinite(value),
               "effect is not positive semidefinite")
    mm.require(mm.is_positive_semidefinite(sp.eye(value.rows)-value),
               "effect exceeds the identity")
    return value


def effect_from_json(raw: dict) -> sp.ImmutableMatrix:
    mm.strict_keys(raw, EFFECT_FIELDS, "effect")
    mm.require(raw["schema"] == EFFECT, "wrong effect schema")
    d = mm.positive_integer(raw["dimension"], "dimension")
    return legal_effect(mm.matrix_from_json(raw["effect"], d, "effect"))


def effect_to_json(value: sp.MatrixBase) -> dict:
    value = legal_effect(value)
    return {"schema": EFFECT, "dimension": value.rows,
            "effect": mm.matrix_to_json(value)}


def denominator(d: int, horizon: int, delta: str | sp.Rational) -> int:
    d = mm.positive_integer(d, "dimension")
    N = mm.positive_integer(horizon, "horizon")
    delta = accuracy(delta)
    value = 32*d*N/delta
    p, q = value.as_numer_denom()
    return (int(p)+int(q)-1)//int(q)


def finite_grid(d: int, k: int) -> Iterator[sp.ImmutableMatrix]:
    """All legal denominator-k effects, in the theorem's lexicographic order.

    Coordinates are diagonal entries first, then (Re G_ij, Im G_ij) for
    i<j. The exact necessary 2-by-2 principal-minor inequalities

        |k G_ij|^2 <= min(a_i a_j, (k-a_i)(k-a_j))

    prune tuples before full Schur tests. They remove no legal matrix and
    leave the order of all surviving tuples unchanged. Full PSD tests are
    still required, in particular in dimension three and above.
    """
    d = mm.positive_integer(d, "dimension")
    k = mm.positive_integer(k, "grid denominator")
    pairs = [(i, j) for i in range(d) for j in range(i+1, d)]
    for diagonal in product(range(k+1), repeat=d):
        work = sp.diag(*[sp.Rational(a, k) for a in diagonal])

        def visit(index: int) -> Iterator[sp.ImmutableMatrix]:
            if index == len(pairs):
                if (mm.is_positive_semidefinite(work)
                        and mm.is_positive_semidefinite(sp.eye(d)-work)):
                    yield sp.ImmutableMatrix(work)
                return
            i, j = pairs[index]
            radius_squared = min(diagonal[i]*diagonal[j],
                                 (k-diagonal[i])*(k-diagonal[j]))
            real_bound = isqrt(radius_squared)
            for real in range(-real_bound, real_bound+1):
                imaginary_bound = isqrt(radius_squared-real*real)
                for imag in range(-imaginary_bound, imaginary_bound+1):
                    entry = sp.Rational(real, k)+sp.I*sp.Rational(imag, k)
                    work[i, j], work[j, i] = entry, sp.conjugate(entry)
                    yield from visit(index+1)

        yield from visit(0)


def _q_squared(E: sp.MatrixBase, F: sp.MatrixBase, N: int) -> sp.Rational:
    """Exact midpoint modulus for already validated legal effects."""
    d = E.rows
    H = F-E
    midpoint = (E+F)/2
    if E.is_diagonal() and F.is_diagonal():
        value = sum(
            N*H[i, i]**2
            / (2*midpoint[i, i]*(1-midpoint[i, i])+sp.Rational(1, N))
            for i in range(d)
        )
        real, imag = mm.gaussian_parts(value)
    else:
        V = (midpoint*(sp.eye(d)-midpoint)).applyfunc(mm.gaussian)
        X = mm.sylvester_solution(V, H, sp.Rational(1, N))
        real, imag = mm.gaussian_parts(N*sp.trace(H*X))
    mm.require(imag == 0 and real >= 0, "invalid midpoint modulus square")
    mm.require((real == 0) == (E == F), "invalid modulus degeneracy")
    return real


def midpoint_q_squared(E: sp.MatrixBase, F: sp.MatrixBase,
                       horizon: int) -> sp.Rational:
    N = mm.positive_integer(horizon, "horizon")
    E, F = legal_effect(E), legal_effect(F)
    mm.require(E.rows == F.rows, "effect dimensions differ")
    return _q_squared(E, F, N)


def greedy_centres(candidates: Iterable[sp.MatrixBase], horizon: int,
                   cutoff_squared: sp.Rational, *,
                   max_candidates: int | None = None
                   ) -> tuple[tuple[sp.ImmutableMatrix, ...], int]:
    """Exhaust the given finite candidate stream, or fail without a book.

    This kernel accepts an explicitly finite stream for small regression
    cases. Only construct_codebook supplies the theorem's complete grid.
    """
    N = mm.positive_integer(horizon, "horizon")
    mm.require(getattr(cutoff_squared, "is_Rational", False) is True
               and cutoff_squared > 0,
               "cutoff square must be a positive exact rational")
    if max_candidates is not None:
        mm.positive_integer(max_candidates, "candidate limit")
    retained: list[sp.ImmutableMatrix] = []
    count, dimension = 0, None
    for candidate in candidates:
        count += 1
        if max_candidates is not None and count > max_candidates:
            raise IncompleteConstruction(
                "complete grid was not exhausted within the legal-candidate "
                "limit; no codebook or payload was produced")
        candidate = legal_effect(candidate)
        if dimension is None:
            dimension = candidate.rows
        mm.require(candidate.rows == dimension,
                   "candidate dimensions differ")
        if all(_q_squared(candidate, centre, N) > cutoff_squared
               for centre in retained):
            retained.append(candidate)
    mm.require(count > 0, "empty candidate stream")
    return tuple(retained), count


@dataclass(frozen=True)
class Codebook:
    """A completed deterministic construction, kept in local memory."""

    dimension: int
    horizon: int
    accuracy: sp.Rational
    denominator: int
    centres: tuple[sp.ImmutableMatrix, ...]
    legal_candidates: int

    @property
    def payload_bits(self) -> int:
        return (len(self.centres)-1).bit_length()


def construct_codebook(d: int, horizon: int, delta: str | sp.Rational, *,
                       max_candidates: int | None = None) -> Codebook:
    d = mm.positive_integer(d, "dimension")
    N = mm.positive_integer(horizon, "horizon")
    delta = accuracy(delta)
    k = denominator(d, N, delta)
    centres, count = greedy_centres(finite_grid(d, k), N, delta**2/256,
                                   max_candidates=max_candidates)
    return Codebook(d, N, delta, k, centres, count)


def nearest_grid_rational(value: sp.Rational, k: int) -> sp.Rational:
    """Nearest grid value, with ties toward positive infinity."""
    mm.require(getattr(value, "is_Rational", False) is True,
               "rounding requires an exact rational")
    k = mm.positive_integer(k, "grid denominator")
    p, q = (k*value+sp.Rational(1, 2)).as_numer_denom()
    return sp.Rational(int(p)//int(q), k)


def quantize(E: sp.MatrixBase, horizon: int,
             delta: str | sp.Rational) -> sp.ImmutableMatrix:
    E = legal_effect(E)
    N = mm.positive_integer(horizon, "horizon")
    delta = accuracy(delta)
    d, k = E.rows, denominator(E.rows, N, delta)
    s = sp.Rational(2*d, k)
    interior = (1-2*s)*E+s*sp.eye(d)
    grid = sp.zeros(d)
    for i in range(d):
        grid[i, i] = nearest_grid_rational(interior[i, i], k)
        for j in range(i+1, d):
            real, imag = mm.gaussian_parts(interior[i, j])
            entry = (nearest_grid_rational(real, k)
                     +sp.I*nearest_grid_rational(imag, k))
            grid[i, j], grid[j, i] = entry, sp.conjugate(entry)
    grid = legal_effect(grid)
    margin = sp.Rational(d, k)
    mm.require(mm.is_positive_semidefinite(grid-margin*sp.eye(d))
               and mm.is_positive_semidefinite((1-margin)*sp.eye(d)-grid),
               "quantization lost its certified spectral margin")
    displacement = E-grid
    bound = 3*margin
    mm.require(mm.is_positive_semidefinite(bound*sp.eye(d)-displacement)
               and mm.is_positive_semidefinite(bound*sp.eye(d)+displacement),
               "quantization violated its operator-norm error bound")
    return grid


def encode_with_book(E: sp.MatrixBase, book: Codebook) -> dict:
    """Use a completed book already reconstructed in this process."""
    E = legal_effect(E)
    mm.require(E.rows == book.dimension, "source dimension differs")
    grid = quantize(E, book.horizon, book.accuracy)
    index = next((j for j, centre in enumerate(book.centres)
                  if _q_squared(grid, centre, book.horizon)
                  <= book.accuracy**2/256), None)
    mm.require(index is not None, "completed codebook did not cover the grid")
    payload = (format(index, "0"+str(book.payload_bits)+"b")
               if book.payload_bits else "")
    return {"schema": CODE, "dimension": book.dimension,
            "horizon": book.horizon, "accuracy": str(book.accuracy),
            "payload": payload}


def encode(raw: dict, horizon: int, delta: str | sp.Rational, *,
           max_candidates: int | None = None) -> dict:
    E = effect_from_json(raw)
    book = construct_codebook(E.rows, horizon, delta,
                              max_candidates=max_candidates)
    return encode_with_book(E, book)


def code_parameters(raw: dict) -> tuple[int, int, sp.Rational]:
    mm.strict_keys(raw, CODE_FIELDS, "code")
    mm.require(raw["schema"] == CODE, "wrong code schema")
    d = mm.positive_integer(raw["dimension"], "dimension")
    N = mm.positive_integer(raw["horizon"], "horizon")
    delta = accuracy(raw["accuracy"])
    mm.require(type(raw["accuracy"]) is str,
               "code accuracy must be a canonical rational string")
    mm.require(type(raw["payload"]) is str
               and all(bit in "01" for bit in raw["payload"]),
               "payload must be a binary string")
    return d, N, delta


def decode_with_book(raw: dict, book: Codebook) -> sp.ImmutableMatrix:
    parameters = code_parameters(raw)
    mm.require(parameters == (book.dimension, book.horizon, book.accuracy),
               "code parameters do not match the reconstructed codebook")
    mm.require(len(raw["payload"]) == book.payload_bits,
               "payload does not have the reconstructed fixed length")
    index = int(raw["payload"], 2) if book.payload_bits else 0
    if index >= len(book.centres):
        return sp.ImmutableMatrix(sp.eye(book.dimension)/2)
    return book.centres[index]


def decode(raw: dict, *,
           max_candidates: int | None = None) -> sp.ImmutableMatrix:
    d, N, delta = code_parameters(raw)
    book = construct_codebook(d, N, delta, max_candidates=max_candidates)
    return decode_with_book(raw, book)


def book_summary(book: Codebook) -> dict:
    digest = hashlib.sha256()
    for centre in book.centres:
        digest.update(mm.canonical(effect_to_json(centre)).encode("ascii"))
        digest.update(b"\n")
    return {"schema": SUMMARY, "theorem": THEOREM,
            "dimension": book.dimension, "horizon": book.horizon,
            "accuracy": str(book.accuracy),
            "grid_denominator": book.denominator,
            "legal_candidates": book.legal_candidates,
            "centres": len(book.centres), "payload_bits": book.payload_bits,
            "ordered_centres_sha256": digest.hexdigest(),
            "complete": True,
            "scope": "complete exact dictionary; public parameters supplied "
                     "separately from the fixed-length payload"}


def audit_prefix(d: int, horizon: int, delta: str | sp.Rational,
                 legal_limit: int) -> dict:
    """Audit a finite prefix without emitting a purported dictionary."""
    d = mm.positive_integer(d, "dimension")
    N = mm.positive_integer(horizon, "horizon")
    delta = accuracy(delta)
    legal_limit = mm.positive_integer(legal_limit, "legal prefix limit")
    k = denominator(d, N, delta)
    retained: list[sp.ImmutableMatrix] = []
    digest = hashlib.sha256()
    count, comparisons = 0, 0
    stream = finite_grid(d, k)
    for _ in range(legal_limit):
        candidate = next(stream, None)
        if candidate is None:
            break
        count += 1
        separated = True
        for centre in retained:
            comparisons += 1
            if _q_squared(candidate, centre, N) <= delta**2/256:
                separated = False
                break
        if separated:
            retained.append(candidate)
        digest.update(mm.canonical(effect_to_json(candidate)).encode("ascii"))
        digest.update(b"\n")
    return {"schema": PREFIX, "dimension": d, "horizon": N,
            "accuracy": str(delta), "grid_denominator": k,
            "legal_prefix_checked": count, "retained_in_prefix": len(retained),
            "exact_modulus_comparisons": comparisons,
            "prefix_sha256": digest.hexdigest(),
            "full_enumeration_claimed": False, "codec_produced": False,
            "scope": "exact finite-prefix kernel audit; not a complete "
                     "matrix dictionary or an operational-distance computation"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    command = sub.add_parser("encode")
    command.add_argument("--input", required=True)
    command.add_argument("--horizon", required=True, type=int)
    command.add_argument("--accuracy", required=True)
    command.add_argument("--max-candidates", type=int)
    command = sub.add_parser("decode")
    command.add_argument("--input", required=True)
    command.add_argument("--max-candidates", type=int)
    command = sub.add_parser("summary")
    command.add_argument("--dimension", required=True, type=int)
    command.add_argument("--horizon", required=True, type=int)
    command.add_argument("--accuracy", required=True)
    command.add_argument("--max-candidates", type=int)
    command = sub.add_parser("audit-prefix")
    command.add_argument("--dimension", required=True, type=int)
    command.add_argument("--horizon", required=True, type=int)
    command.add_argument("--accuracy", required=True)
    command.add_argument("--legal-limit", required=True, type=int)
    args = parser.parse_args(argv)
    try:
        if args.action == "encode":
            raw = mm.loads(Path(args.input).read_text(encoding="utf-8"))
            result = encode(raw, args.horizon, args.accuracy,
                            max_candidates=args.max_candidates)
        elif args.action == "decode":
            raw = mm.loads(Path(args.input).read_text(encoding="utf-8"))
            result = effect_to_json(decode(raw,
                                          max_candidates=args.max_candidates))
        elif args.action == "summary":
            result = book_summary(construct_codebook(
                args.dimension, args.horizon, args.accuracy,
                max_candidates=args.max_candidates))
        else:
            result = audit_prefix(args.dimension, args.horizon, args.accuracy,
                                  args.legal_limit)
        print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))
        return 0
    except (ValueError, TypeError, KeyError, IndexError, OSError) as error:
        print(json.dumps({"error": str(error)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
