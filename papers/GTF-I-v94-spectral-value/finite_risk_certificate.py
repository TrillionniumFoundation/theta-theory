#!/usr/bin/env python3
"""Replay a finite rational Choi-readout risk certificate using exact arithmetic.

The verifier rebuilds the COMPLETE public interior grid; a finite prefix is
never a certificate. This checks a supplied rational readout, not a procedure
for finding the general optimal learner. The mathematical extension from grid
risk to all real effects uses the stated rounding and Choi telescoping lemmas.
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

import sympy as sp

import matrix_metric as mm


SCHEMA = "gtf81.finite-risk-certificate/1"
REPLAY = "gtf81.finite-risk-replay/1"
CONVENTION = "y=1:E^T; y=0:(I-E)^T; left-to-right tensor order; d^(-m)"
FIELDS = {"schema", "dimension", "calls", "horizon", "a", "r", "alpha",
          "choi_convention", "dictionary", "readout", "target"}
DEFAULT_GRID_LIMIT = 10000


class IncompleteVerification(ValueError):
    """The complete grid was not checked; no risk certificate was accepted."""


class InvalidCertificate(ValueError):
    """An exact grid inequality of a structurally valid certificate failed."""


def _ceil(value: sp.Rational) -> int:
    p, q = value.as_numer_denom()
    return (int(p) + int(q) - 1) // int(q)


def ceil_sqrt(value: int) -> int:
    value = mm.positive_integer(value, "horizon")
    root = isqrt(value)
    return root if root * root == value else root + 1


def _hermitian(value: sp.MatrixBase) -> sp.ImmutableMatrix:
    mm.require(isinstance(value, sp.MatrixBase) and value.rows == value.cols
               and value.rows > 0, "nonempty square matrix required")
    out = sp.ImmutableMatrix(value.applyfunc(mm.gaussian))
    mm.require(out == out.adjoint(), "matrix must be Hermitian")
    return out


def in_interval(value: sp.MatrixBase, lower: sp.Rational,
                upper: sp.Rational) -> bool:
    value = _hermitian(value)
    identity = sp.eye(value.rows)
    return (mm.is_positive_semidefinite(value - lower * identity)
            and mm.is_positive_semidefinite(upper * identity - value))


def op_leq(value: sp.MatrixBase, radius: sp.Rational) -> bool:
    """Exact two-sided PSD comparison, with equality counted as good."""
    mm.require(getattr(radius, "is_Rational", False) is True and radius >= 0,
               "operator radius must be a nonnegative exact rational")
    value = _hermitian(value)
    if value.is_diagonal():
        return all(abs(value[i, i]) <= radius for i in range(value.rows))
    identity = sp.eye(value.rows)
    return (mm.is_positive_semidefinite(radius * identity - value)
            and mm.is_positive_semidefinite(radius * identity + value))


@dataclass(frozen=True)
class Certificate:
    dimension: int
    calls: int
    horizon: int | None
    a: sp.Rational
    r: sp.Rational
    alpha: sp.Rational
    centres: tuple[sp.ImmutableMatrix, ...]
    # Branches are ordered by the exact m-bit binary string, including zeros.
    readout: tuple[tuple[sp.ImmutableMatrix, ...], ...]
    target: tuple[sp.Rational, sp.Rational] | None
    source_sha256: str


def validate(raw: dict) -> Certificate:
    """Parse every coordinate and verify all branches, positivity and sums."""
    mm.strict_keys(raw, FIELDS, "finite risk certificate")
    mm.require(raw["schema"] == SCHEMA, "wrong certificate schema")
    mm.require(raw["choi_convention"] == CONVENTION,
               "incorrect or unspecified Choi transpose/tensor convention")
    d = mm.positive_integer(raw["dimension"], "dimension")
    m = mm.positive_integer(raw["calls"], "calls")
    N = raw["horizon"]
    if N is not None:
        N = mm.positive_integer(N, "horizon")
    a = mm.rational(raw["a"], "a")
    r = mm.rational(raw["r"], "r")
    alpha = mm.rational(raw["alpha"], "alpha")
    mm.require(0 < a <= 1, "a must be in (0,1]")
    mm.require(0 < r <= sp.Rational(1, 4), "r must be in (0,1/4]")
    mm.require(0 <= alpha < 1, "alpha must be in [0,1)")
    mm.require(type(raw["dictionary"]) is list and raw["dictionary"],
               "dictionary must be a nonempty list")
    centres = []
    for j, entry in enumerate(raw["dictionary"]):
        C = mm.matrix_from_json(entry, d, "dictionary[" + str(j) + "]")
        mm.require(in_interval(C, sp.Rational(1, 8), sp.Rational(7, 8)),
                   "dictionary centre is outside [I/8,7I/8]")
        centres.append(sp.ImmutableMatrix(C))
    L = len(centres)
    mm.require(type(raw["readout"]) is list and raw["readout"],
               "readout must contain every binary branch")
    count = len(raw["readout"])
    # Comparing bit lengths avoids allocating 2**m for a hostile huge m.
    mm.require(count & (count - 1) == 0 and count.bit_length() - 1 == m,
               "readout must contain exactly all 2^m branches")
    D = d ** m
    identity = None
    branches = []
    for index, branch in enumerate(raw["readout"]):
        mm.strict_keys(branch, {"y", "effects"}, "readout branch")
        mm.require(type(branch["y"]) is str
                   and branch["y"] == format(index, "0" + str(m) + "b"),
                   "branches must be complete, unique and in binary order")
        mm.require(type(branch["effects"]) is list
                   and len(branch["effects"]) == L,
                   "each branch must specify exactly L POVM effects")
        effects = []
        total = None
        for j, entry in enumerate(branch["effects"]):
            A = mm.matrix_from_json(entry, D, "A[" + branch["y"]
                                    + "," + str(j) + "]")
            mm.require(mm.is_positive_semidefinite(A),
                       "readout effect is not positive semidefinite")
            effects.append(sp.ImmutableMatrix(A))
            # Reject wrong supplied dimensions before allocating a D-by-D zero
            # or identity matrix. D=d**m can dwarf a malformed input file.
            if total is None:
                total = sp.Matrix(A)
            else:
                total += A
            if identity is None:
                identity = sp.eye(D)
        mm.require(total == identity, "branch POVM does not sum exactly to I")
        branches.append(tuple(effects))
    target = raw["target"]
    if target is not None:
        mm.strict_keys(target, {"accuracy", "failure"}, "target")
        delta = mm.rational(target["accuracy"], "target accuracy")
        eta = mm.rational(target["failure"], "target failure")
        mm.require(0 < delta <= 2 and 0 < eta < 1,
                   "target accuracy/failure are outside the diagnostic range")
        mm.require(N is not None, "a target requires an explicit horizon")
        target = (delta, eta)
    digest = hashlib.sha256(json.dumps(raw, sort_keys=True, separators=(",", ":"),
                                      ensure_ascii=True).encode()).hexdigest()
    return Certificate(d, m, N, a, r, alpha, tuple(centres), tuple(branches),
                       target, digest)


def grid_parameters(d: int, r: sp.Rational) -> tuple[int, int]:
    """Denominator and size of a proved-complete finite coordinate superset.

    An interior G has diagonals in [1/4,3/4] and |G_ij|<=1/4 for
    i!=j, because ||G-I/2||op<=1/4. Restricting each real and imaginary
    coordinate to that interval therefore removes no interior grid point.
    Remaining non-PSD tuples are rejected by complete exact PSD tests.
    """
    d = mm.positive_integer(d, "dimension")
    mm.require(getattr(r, "is_Rational", False) is True
               and 0 < r <= sp.Rational(1, 4), "invalid exact grid radius")
    K = _ceil(4 * d / r)
    mm.require(K >= 16 * d, "interior grid denominator invariant failed")
    diagonal_count = (3 * K) // 4 - (K + 3) // 4 + 1
    off_count = 2 * (K // 4) + 1
    return K, diagonal_count ** d * off_count ** (d * (d - 1))


def grid_tuples(d: int, K: int):
    """Every tuple in the finite superset, before the full PSD filters."""
    diagonal = range((K + 3) // 4, (3 * K) // 4 + 1)
    off = range(-(K // 4), K // 4 + 1)
    pairs = [(i, j) for i in range(d) for j in range(i + 1, d)]
    for diag in product(diagonal, repeat=d):
        for coords in product(off, repeat=2 * len(pairs)):
            G = sp.diag(*[sp.Rational(value, K) for value in diag])
            for position, (i, j) in enumerate(pairs):
                z = (sp.Rational(coords[2 * position], K)
                     + sp.I * sp.Rational(coords[2 * position + 1], K))
                G[i, j], G[j, i] = z, sp.conjugate(z)
            yield sp.ImmutableMatrix(G)


def choi_block(E: sp.MatrixBase, y: str) -> sp.ImmutableMatrix:
    """Subnormalized block d^-m tensor E_y^T; never an adjoint substitute."""
    E = _hermitian(E)
    mm.require(type(y) is str and len(y) > 0 and set(y) <= {"0", "1"},
               "nonempty binary outcome string required")
    mm.require(in_interval(E, sp.Rational(0), sp.Rational(1)),
               "Choi input must be a legal effect")
    factors = [E.transpose() if bit == "1"
               else (sp.eye(E.rows) - E).transpose() for bit in y]
    return sp.ImmutableMatrix(sp.kronecker_product(*factors) / E.rows ** len(y))


def _scalar_coefficients(cert: Certificate) -> tuple[tuple[sp.Rational, ...], ...]:
    coeff = [[sp.Rational(0) for _ in range(cert.calls + 1)]
             for _ in cert.centres]
    for index, branch in enumerate(cert.readout):
        successes = index.bit_count()
        for j, A in enumerate(branch):
            coeff[j][successes] += A[0, 0]
    return tuple(tuple(row) for row in coeff)


def probabilities(cert: Certificate, E: sp.MatrixBase, *,
                  scalar_coefficients=None) -> tuple[sp.Rational, ...]:
    """Recompute readout probabilities; no supplied probabilities are trusted."""
    E = _hermitian(E)
    mm.require(E.rows == cert.dimension
               and in_interval(E, sp.Rational(0), sp.Rational(1)),
               "effect dimension or legality differs from certificate")
    if cert.dimension == 1:
        coeff = (_scalar_coefficients(cert) if scalar_coefficients is None
                 else scalar_coefficients)
        x = E[0, 0]
        weights = [x ** s * (1 - x) ** (cert.calls - s)
                   for s in range(cert.calls + 1)]
        values = [sum(c * w for c, w in zip(row, weights)) for row in coeff]
    else:
        values = [sp.Rational(0) for _ in cert.centres]
        for index, branch in enumerate(cert.readout):
            y = format(index, "0" + str(cert.calls) + "b")
            R = choi_block(E, y)
            for j, A in enumerate(branch):
                values[j] += sp.trace(A * R)
    real_values = []
    for value in values:
        real, imag = mm.gaussian_parts(value)
        mm.require(imag == 0 and 0 <= real <= 1,
                   "calculated readout probability is not real in [0,1]")
        real_values.append(real)
    mm.require(sum(real_values) == 1, "calculated probabilities do not sum to one")
    return tuple(real_values)


def replay(raw: dict, *, max_grid_candidates: int | None = DEFAULT_GRID_LIMIT
           ) -> dict:
    """Return success only after all grid tuples and all legal-point risks pass."""
    cert = validate(raw)
    K, candidate_count = grid_parameters(cert.dimension, cert.r)
    if max_grid_candidates is not None:
        limit = mm.positive_integer(max_grid_candidates, "grid candidate limit")
        if candidate_count > limit:
            raise IncompleteVerification(
                "complete interior grid requires " + str(candidate_count)
                + " coordinate tuples; limit is " + str(limit)
                + "; no grid-risk certificate was accepted")
    scalar = _scalar_coefficients(cert) if cert.dimension == 1 else None
    tested = legal = boundary_good = 0
    minimum = sp.Rational(1)
    worst = None
    for G in grid_tuples(cert.dimension, K):
        tested += 1
        if not in_interval(G, sp.Rational(1, 4), sp.Rational(3, 4)):
            continue
        legal += 1
        probs = probabilities(cert, G, scalar_coefficients=scalar)
        good = [op_leq(G - C, cert.a) for C in cert.centres]
        # Scalar equality counts are diagnostic only, not a norm computation.
        if cert.dimension == 1:
            boundary_good += sum(abs(G[0, 0] - C[0, 0]) == cert.a
                                 for C in cert.centres)
        success = sum((prob for prob, keep in zip(probs, good) if keep),
                      sp.Rational(0))
        if worst is None or success < minimum:
            minimum, worst = success, G
        if success < 1 - cert.alpha:
            raise InvalidCertificate(
                "grid risk failed at " + json.dumps(mm.matrix_to_json(G))
                + ": success=" + str(success) + " < " + str(1 - cert.alpha))
    mm.require(tested == candidate_count and legal > 0 and worst is not None,
               "complete-grid enumeration invariant failed")
    op_radius = cert.a + cert.r
    raw_failure = cert.alpha + cert.calls * cert.r
    theorem_range = False
    target_certified = None
    future_radius = None
    if cert.horizon is not None:
        k = ceil_sqrt(cert.horizon)
        future_radius = min(sp.Rational(2), 4 * k * op_radius)
        if cert.target is not None:
            delta, eta = cert.target
            theorem_range = bool(
                delta <= sp.Rational(1, 2 ** 13)
                and eta <= sp.Rational(1, 8)
                and cert.a == delta / (8 * k)
                and cert.r == min(delta / (32 * k), eta / (16 * cert.calls))
                and cert.alpha == eta / 4)
            target_certified = bool(future_radius <= delta and raw_failure <= eta)
            mm.require(target_certified,
                       "grid passed but its transfer bound does not certify the requested target")
    return {
        "schema": REPLAY, "status": "success", "complete_grid": True,
        "certificate_sha256": cert.source_sha256,
        "dimension": cert.dimension, "calls": cert.calls,
        "horizon": cert.horizon, "dictionary_size": len(cert.centres),
        "readout_branches": len(cert.readout),
        "readout_dimension": cert.dimension ** cert.calls,
        "grid_denominator": K, "candidate_tuples_checked": tested,
        "legal_grid_points_checked": legal, "scalar_good_boundary_pairs": boundary_good,
        "minimum_grid_success": str(minimum),
        "worst_grid_point": mm.matrix_to_json(worst),
        "certified_operator_radius": str(op_radius),
        "grid_failure_allowance": str(cert.alpha),
        "grid_to_real_failure_buffer": str(cert.calls * cert.r),
        "unclipped_failure_bound": str(raw_failure),
        "certified_failure_bound": str(min(sp.Rational(1), raw_failure)),
        "certified_future_radius": (None if future_radius is None else str(future_radius)),
        "target_risk_certified": target_certified,
        "parameter_class": ("theorem-parameter-recipe" if theorem_range
                            else "diagnostic-outside-theorem-range"),
        "dictionary_source": "supplied-finite-family-validated-and-hash-bound",
        "optimal_public_dictionary_reconstructed": False,
        "general_optimal_learner_synthesis_executed": False,
        "scope": ("Exact replay of the supplied rational readout on the complete "
                  "public grid, with the proved grid-to-real bounds; no general "
                  "optimal learner synthesis or large-dimensional execution claim."),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--max-grid-candidates", type=int, default=DEFAULT_GRID_LIMIT,
                        help="complete coordinate-tuple budget; failure is incomplete")
    args = parser.parse_args(argv)
    try:
        raw = mm.loads(args.certificate.read_text(encoding="utf-8"))
        result = replay(raw, max_grid_candidates=args.max_grid_candidates)
    except IncompleteVerification as error:
        print(json.dumps({"schema": REPLAY, "status": "incomplete",
                          "complete_grid": False, "reason": str(error)},
                         sort_keys=True, indent=2))
        return 2
    except (ValueError, TypeError, KeyError, OSError) as error:
        print(json.dumps({"schema": REPLAY, "status": "rejected",
                          "complete_grid": False, "reason": str(error)},
                         sort_keys=True, indent=2))
        return 1
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
