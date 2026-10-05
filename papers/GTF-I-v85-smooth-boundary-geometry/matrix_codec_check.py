#!/usr/bin/env python3
"""Exact regression for the finite rational matrix codec.

Complete theorem dictionaries are enumerated only in dimension one.
Small full matrix grids below use K=2 or K=3 to audit the enumeration
kernel; they are not substitutes for the theorem's much larger grid.
The dimension-two theorem-grid audit stops at an explicitly recorded
prefix. No large-dimensional full-codebook execution is claimed.
"""
from __future__ import annotations

import json
from math import comb
from pathlib import Path
import subprocess
import sys
import tempfile

import sympy as sp

import matrix_codec as mc
import matrix_metric as mm


ASSERTIONS = 0


def check(condition, message: str) -> None:
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(message)


def rejects(callable_, exception=ValueError) -> None:
    try:
        callable_()
    except exception:
        check(True, "expected rejection")
    else:
        check(False, "expected rejection was not raised")


def bernoulli_distance(p: sp.Rational, q: sp.Rational, N: int) -> sp.Rational:
    """Independent exact final-law l1 distance for the scalar experiment."""
    return sum(comb(N, k)*abs(p**k*(1-p)**(N-k)-q**k*(1-q)**(N-k))
               for k in range(N+1))


def d2_coordinate_tuple(matrix: sp.MatrixBase, k: int) -> tuple[int, ...]:
    real, imag = mm.gaussian_parts(matrix[0, 1])
    return (int(k*matrix[0, 0]), int(k*matrix[1, 1]),
            int(k*real), int(k*imag))


def main() -> int:
    scalar_reports = []
    configurations = [(1, "1"), (1, "1/2"), (2, "1"),
                      (2, "1/2"), (4, "1"), (4, "1/2")]
    first_book = None
    for N, delta_text in configurations:
        delta = mm.rational(delta_text)
        book = mc.construct_codebook(1, N, delta)
        check(book.legal_candidates == book.denominator+1,
              "scalar grid was not exhausted")
        check(book.payload_bits == (len(book.centres)-1).bit_length(),
              "payload length differs from the complete dictionary")
        if first_book is None:
            first_book = book
        largest = sp.Rational(0)
        for numerator in range(38):
            p = sp.Rational(numerator, 37)
            source = sp.Matrix([[p]])
            code = mc.encode_with_book(source, book)
            decoded = mc.decode_with_book(code, book)
            distance = bernoulli_distance(p, decoded[0, 0], N)
            largest = max(largest, distance)
            check(distance <= 11*delta/16,
                  "exact scalar final-law error exceeds theorem bound")
            check(len(code["payload"]) == book.payload_bits,
                  "source-dependent payload length")
        for index in range(1 << book.payload_bits):
            raw = {"schema": mc.CODE, "dimension": 1, "horizon": N,
                   "accuracy": delta_text,
                   "payload": format(index, "0"+str(book.payload_bits)+"b")}
            value = mc.decode_with_book(raw, book)
            check(0 <= value[0, 0] <= 1, "a fixed-length word is not legal")
            if index >= len(book.centres):
                check(value == sp.eye(1)/2, "unused word has wrong fallback")
        scalar_reports.append({**mc.book_summary(book),
                               "tested_sources": 38,
                               "largest_exact_bernoulli_distance": str(largest)})

    repeated = mc.construct_codebook(1, 1, "1")
    check(mc.book_summary(repeated) == mc.book_summary(first_book),
          "deterministic replay changed the dictionary")

    grid_reports = []
    for k in [2, 3]:
        actual_matrices = tuple(mc.finite_grid(2, k))
        actual = [d2_coordinate_tuple(matrix, k) for matrix in actual_matrices]
        # In dimension two these determinant conditions are necessary and
        # sufficient, independently of the Schur implementation.
        expected = [
            (a, b, real, imag)
            for a in range(k+1) for b in range(k+1)
            for real in range(-k, k+1) for imag in range(-k, k+1)
            if real*real+imag*imag <= a*b
            and real*real+imag*imag <= (k-a)*(k-b)
        ]
        check(actual == expected,
              "matrix grid differs from independent principal-minor enumeration")
        check(actual == sorted(set(actual)), "grid ordering or uniqueness failed")
        grid_reports.append({"dimension": 2, "denominator": k,
                             "complete_legal_grid_size": len(actual),
                             "theorem_dictionary": False})

    coarse = tuple(mc.finite_grid(2, 2))
    cutoff = sp.Rational(1, 4)
    retained, count = mc.greedy_centres(coarse, 1, cutoff)
    check(count == len(coarse), "coarse greedy pass was not complete")
    for i, centre in enumerate(retained):
        for previous in retained[:i]:
            check(mc.midpoint_q_squared(centre, previous, 1) > cutoff,
                  "coarse retained pair violates strict separation")
    for candidate in coarse:
        check(any(mc.midpoint_q_squared(candidate, centre, 1) <= cutoff
                  for centre in retained), "coarse greedy cover omitted a point")

    zero, half = sp.zeros(1), sp.eye(1)/2
    equality_cutoff = mc.midpoint_q_squared(zero, half, 1)
    equality_book, _ = mc.greedy_centres([zero, half], 1, equality_cutoff)
    check(len(equality_book) == 1, "equality was treated as strict separation")

    grid3 = tuple(mc.finite_grid(3, 2))
    check(sp.ones(3)/2 not in grid3,
          "2-by-2 pruning incorrectly replaced the full upper PSD test")
    check(sp.zeros(3) in grid3 and sp.eye(3) in grid3,
          "rank-zero or full-rank endpoint omitted from dimension-three grid")
    grid_reports.append({"dimension": 3, "denominator": 2,
                         "complete_legal_grid_size": len(grid3),
                         "theorem_dictionary": False})

    qubit_e = sp.diag(1, 0)
    qubit_f = sp.Matrix([[sp.Rational(1, 2), sp.I/2],
                        [-sp.I/2, sp.Rational(1, 2)]])
    rotation = sp.Matrix([[sp.Rational(3, 5), sp.Rational(-4, 5), 0],
                          [sp.Rational(4, 5), sp.Rational(3, 5), 0],
                          [0, 0, 1]])
    matrix_e = sp.diag(0, sp.Rational(1, 3), 1)
    matrix_f = rotation*matrix_e*rotation.T
    for E, F, N in [(qubit_e, qubit_f, 7), (matrix_e, matrix_f, 3)]:
        pair = {"schema": mm.PAIR, "dimension": E.rows,
                "effect_e": mm.matrix_to_json(E),
                "effect_f": mm.matrix_to_json(F)}
        reference = mm.compute(pair, N)
        check(mc.midpoint_q_squared(E, F, N)
              == mm.rational(reference["q_squared"]),
              "codec midpoint kernel differs from the pair certificate")

    for d in [1, 2, 3]:
        for N, delta in [(1, "1"), (7, "3/7"), (10, "1/100")]:
            k = mc.denominator(d, N, delta)
            s = sp.Rational(2*d, k)
            check(mc.quantize(sp.zeros(d), N, delta) == s*sp.eye(d),
                  "zero effect inward rounding changed")
            check(mc.quantize(sp.eye(d), N, delta) == (1-s)*sp.eye(d),
                  "identity effect inward rounding changed")
    check(mc.quantize(sp.eye(1)/2, 1, "64/65") == sp.Matrix([[sp.Rational(17, 33)]]),
          "exact rounding tie was not sent toward the larger grid point")
    check(mc.nearest_grid_rational(sp.Rational(-1, 8), 4) == 0,
          "negative rounding tie was not sent toward positive infinity")
    check(mc.nearest_grid_rational(sp.Rational(1, 8), 4) == sp.Rational(1, 4),
          "positive rounding tie failed")
    for E in [qubit_e, qubit_f, matrix_e, matrix_f]:
        rounded = mc.quantize(E, 7, "3/7")
        k = mc.denominator(E.rows, 7, "3/7")
        bound = sp.Rational(3*E.rows, k)
        check(mm.is_positive_semidefinite(bound*sp.eye(E.rows)-(E-rounded))
              and mm.is_positive_semidefinite(bound*sp.eye(E.rows)+(E-rounded)),
              "noncommuting quantization lacks its exact operator certificate")

    rejects(lambda: mc.denominator(True, 1, "1"))
    rejects(lambda: mc.accuracy("2/2"))
    rejects(lambda: mc.accuracy("0"))
    rejects(lambda: mc.accuracy("2"))
    rejects(lambda: mc.accuracy(0.5))
    rejects(lambda: mc.legal_effect(sp.diag(1, -sp.Rational(1, 10))))
    rejects(lambda: mc.legal_effect(sp.ones(3)/2))
    rejects(lambda: mc.construct_codebook(1, 1, "1", max_candidates=1),
            mc.IncompleteConstruction)
    source = sp.Matrix([[sp.Rational(2, 7)]])
    code = mc.encode_with_book(source, first_book)
    rejects(lambda: mc.decode_with_book({**code, "payload": "x"}, first_book))
    rejects(lambda: mc.decode_with_book({**code, "payload": code["payload"]+"0"},
                                        first_book))
    rejects(lambda: mc.decode_with_book({**code, "horizon": 2}, first_book))
    rejects(lambda: mc.decode_with_book({**code, "accuracy": sp.Rational(1)}, first_book))
    rejects(lambda: mc.decode_with_book({**code, "custom_centres": []}, first_book))

    executable = Path(__file__).with_name("matrix_codec.py")
    with tempfile.TemporaryDirectory() as temporary:
        source_path = Path(temporary)/"source.json"
        source_path.write_text(mm.canonical(mc.effect_to_json(source)),
                               encoding="utf-8")
        encoded = subprocess.run(
            [sys.executable, str(executable), "encode", "--input", str(source_path),
             "--horizon", "1", "--accuracy", "1", "--max-candidates", "33"],
            text=True, capture_output=True, check=False)
        check(encoded.returncode == 0, "exact CLI encoding failed")
        check(mm.loads(encoded.stdout) == code, "CLI encoding changed the payload")
        code_path = Path(temporary)/"code.json"
        code_path.write_text(encoded.stdout, encoding="utf-8")
        decoded = subprocess.run(
            [sys.executable, str(executable), "decode", "--input", str(code_path),
             "--max-candidates", "33"],
            text=True, capture_output=True, check=False)
        check(decoded.returncode == 0, "exact CLI replay decoding failed")
        check(mc.effect_from_json(mm.loads(decoded.stdout))
              == mc.decode_with_book(code, first_book), "CLI replay changed the effect")
        incomplete = subprocess.run(
            [sys.executable, str(executable), "encode", "--input", str(source_path),
             "--horizon", "1", "--accuracy", "1", "--max-candidates", "1"],
            text=True, capture_output=True, check=False)
        check(incomplete.returncode == 2 and incomplete.stdout == "",
              "a resource-limited CLI emitted a purported code")
        check("no codebook or payload" in mm.loads(incomplete.stderr)["error"],
              "incomplete construction did not identify its status")

    prefix = mc.audit_prefix(2, 1, "1", 96)
    check(prefix["legal_prefix_checked"] == 96, "matrix prefix ended unexpectedly")
    check(prefix["full_enumeration_claimed"] is False
          and prefix["codec_produced"] is False,
          "prefix audit falsely claimed a complete matrix code")
    result = {
        "schema": "gtf77.matrix-effect-codec-regression/1",
        "exact_assertions": ASSERTIONS,
        "status": "pass",
        "complete_theorem_dictionary_dimensions": [1],
        "complete_scalar_cases": scalar_reports,
        "complete_coarse_matrix_kernel_grids": grid_reports,
        "matrix_theorem_grid_prefix": prefix,
        "arbitrary_dimension_implementation": True,
        "full_dictionary_executed_in_dimension_at_least_two": False,
        "operational_distance_computed": "scalar Bernoulli cases only",
        "large_dimension_efficiency_claimed": False,
    }
    print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
