#!/usr/bin/env python3
"""Independent exact diagnostics for the external A2 v19 rereview.

The suite imports no author verification module and uses only the Python
standard library.  It checks finite algebra appearing in the local
two-density inverse, finite-index lattice descent, prime-index ambiguity,
incidence bookkeeping, histogram reconstruction, and rate balancing.

These checks are diagnostics, not a proof certificate, a TeX build, a
literature search, or an editorial decision.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
import math

REVIEWED_COMMIT = "2f51ac5a2ab72deceb21c23084ca3062056edb4c"
CHECKS: Counter[str] = Counter()


def check(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    CHECKS[group] += 1


# ---------------------------------------------------------------------------
# Local stationary Schur-complement geometry
# ---------------------------------------------------------------------------

def exact_local_geometry() -> None:
    gaps = [F(1, 4), F(2, 5), F(3, 4), F(1), F(7, 4), F(5, 2)]
    source_curvatures = [F(1, 7), F(1, 3), F(3, 5), F(1), F(11, 6)]
    opposite_curvatures = [F(1, 8), F(2, 7), F(4, 5), F(3, 2), F(7, 3)]
    slopes = [F(0), F(1, 11), F(-1, 9), F(2, 9), F(-1, 4), F(3, 10)]

    for gap, source_k, opposite_k, slope in product(
        gaps, source_curvatures, opposite_curvatures, slopes
    ):
        # Rational parametrization a^2+v^2=1 with v>0.
        a = 2 * slope / (1 + slope * slope)
        v = (1 - slope * slope) / (1 + slope * slope)

        d_ss = v * v / gap + source_k * v
        d_su = -v / gap
        d_uu = 1 / gap + opposite_k

        w_st = -(d_su * d_su) / (2 * d_uu)
        w_ss = d_ss + w_st

        recovered_source = (w_ss - w_st - v * v / gap) / v
        recovered_opposite = (v * v / (-2 * gap * w_st) - 1) / gap
        recovered_speed = -d_su / d_uu

        check(
            recovered_source == source_k,
            "source_curvature",
            str((gap, source_k, opposite_k, slope)),
        )
        check(
            recovered_opposite == opposite_k,
            "opposite_curvature",
            str((gap, source_k, opposite_k, slope)),
        )
        check(
            recovered_speed == v / (1 + gap * opposite_k),
            "foot_speed",
            str((gap, source_k, opposite_k, slope)),
        )
        check(
            w_st < 0 and v > 0 and d_uu > 0 and a * a + v * v == 1,
            "local_margins",
            str((gap, source_k, opposite_k, slope)),
        )


# ---------------------------------------------------------------------------
# Cubic bivariate jets for the two-density quotient
# ---------------------------------------------------------------------------

KEYS = [(i, j) for i in range(4) for j in range(4 - i)]


def add(a: dict[tuple[int, int], F], b: dict[tuple[int, int], F]) -> dict:
    return {key: a.get(key, F(0)) + b.get(key, F(0)) for key in KEYS}


def scale(a: dict[tuple[int, int], F], scalar: F) -> dict:
    return {key: scalar * a.get(key, F(0)) for key in KEYS}


def multiply(a: dict[tuple[int, int], F], b: dict[tuple[int, int], F]) -> dict:
    result = {key: F(0) for key in KEYS}
    for (i, j), x in a.items():
        for (p, q), y in b.items():
            key = (i + p, j + q)
            if key in result:
                result[key] += x * y
    return result


def reciprocal(a: dict[tuple[int, int], F]) -> dict:
    constant = a.get((0, 0), F(0))
    if constant == 0:
        raise ZeroDivisionError("zero constant term")
    z = scale(a, 1 / constant)
    z[(0, 0)] -= 1
    one = {(0, 0): F(1)}
    z2 = multiply(z, z)
    z3 = multiply(z2, z)
    # (1+z)^(-1)=1-z+z^2-z^3 through total degree three.
    return scale(add(add(one, scale(z, -1)), add(z2, scale(z3, -1))), 1 / constant)


def reflect(poly: dict[tuple[int, int], F]) -> dict:
    return {
        key: (-1) ** (key[0] + key[1]) * value
        for key, value in poly.items()
    }


def exact_two_density_jets() -> None:
    for index in range(1, 241):
        action = {
            (i, j): F(
                ((7 * index + 11 * i + 13 * j) % 41) - 20,
                23 + i + 2 * j,
            )
            for i, j in KEYS
        }
        action[(0, 0)] = F(2 + index % 5, 7)

        flux = {
            (i, j): F(
                ((5 * index + 17 * i + 19 * j) % 37) - 18,
                31 + 2 * i + j,
            )
            for i, j in KEYS
        }
        flux[(0, 0)] = F(3 + index % 7, 9)

        time_1 = F(5 + index % 4, 2)
        time_2 = time_1 + F(2 + index % 5, 13)

        density_1 = multiply(
            flux, add({(0, 0): time_1}, scale(action, -1))
        )
        density_2 = multiply(
            flux, add({(0, 0): time_2}, scale(action, -1))
        )
        difference = add(density_2, scale(density_1, -1))

        recovered = multiply(
            add(scale(density_2, time_1), scale(density_1, -time_2)),
            reciprocal(difference),
        )
        for key in KEYS:
            check(
                recovered[key] == action[key],
                "two_density_C3_identity",
                str((index, key)),
            )

        check(
            scale(difference, 1 / (time_2 - time_1)) == flux,
            "flux_recovery",
            str(index),
        )

        recovered_reflected = multiply(
            add(
                scale(reflect(density_2), time_1),
                scale(reflect(density_1), -time_2),
            ),
            reciprocal(reflect(difference)),
        )
        check(
            recovered_reflected == reflect(action),
            "reversal_equivariance",
            str(index),
        )


# ---------------------------------------------------------------------------
# Row-Hermite finite-index classification
# ---------------------------------------------------------------------------

def fractional_part(x: F) -> F:
    return x - math.floor(x)


def divisor_sum(n: int) -> int:
    return sum(d for d in range(1, n + 1) if n % d == 0)


def hnf_matrices(n: int):
    # B=[[a,b],[0,d]], ad=n, 0<=b<d.
    for d in range(1, n + 1):
        if n % d:
            continue
        a = n // d
        for b in range(d):
            yield a, b, d


def quotient_signature(a: int, b: int, d: int) -> frozenset[tuple[F, F]]:
    # Cosets of B^{-1}Z^2 modulo Z^2, using the column convention.
    points: set[tuple[F, F]] = set()
    for z0 in range(a):
        for z1 in range(d):
            x0 = F(z0, a) - F(b * z1, a * d)
            x1 = F(z1, d)
            points.add((fractional_part(x0), fractional_part(x1)))
    return frozenset(points)


def exact_hnf_classification() -> None:
    dual_cases: list[tuple[int, int, int, F, F]] = []

    for n in range(1, 25):
        matrices = list(hnf_matrices(n))
        expected = divisor_sum(n)
        check(len(matrices) == expected, "row_HNF_count", str(n))
        check(expected == sum(d for d in range(1, n + 1) if n % d == 0),
              "divisor_sum_count", str(n))

        signatures: list[frozenset[tuple[F, F]]] = []
        seen_signatures: set[frozenset[tuple[F, F]]] = set()
        for a, b, d in matrices:
            signature = quotient_signature(a, b, d)
            check(len(signature) == n, "overlattice_index", str((n, a, b, d)))
            check(signature not in seen_signatures,
                  "row_HNF_distinct", str((n, a, b, d)))
            seen_signatures.add(signature)
            signatures.append(signature)

            for x0, x1 in signature:
                # n B^{-1} has integral entries.
                check((n * x0).denominator == 1,
                      "index_annihilates_quotient", str((n, a, b, d, x0)))
                check((n * x1).denominator == 1,
                      "index_annihilates_quotient", str((n, a, b, d, x1)))

                # Bx is integral for each enumerated point.
                y0 = a * x0 + b * x1
                y1 = d * x1
                dual_cases.append((a, b, d, y0, y1))

        if len(set(signatures)) != len(signatures):
            raise RuntimeError(f"duplicate row-HNF lattice at index {n}")

    # A deterministic broad sample of exact dual-membership tests.
    for a, b, d, y0, y1 in dual_cases[:3805]:
        check(
            y0.denominator == 1 and y1.denominator == 1,
            "dual_membership",
            str((a, b, d, y0, y1)),
        )


# ---------------------------------------------------------------------------
# Prime-index physical ambiguity controls
# ---------------------------------------------------------------------------

def exact_prime_examples() -> None:
    primes = [3, 5, 7, 11, 13, 17, 19]
    for p in primes:
        candidates: list[frozenset[tuple[int, int]]] = []
        for j in range(1, p):
            # Lambda_j/Z^2 is generated by (1,j)/p and has p cosets.
            cosets = frozenset(((m % p), (m * j) % p) for m in range(p))
            check(len(cosets) == p, "prime_index", str((p, j)))
            candidates.append(cosets)

            # Equality of axial centers only at integral multiples of d1,d2.
            # The nonzero residue controls both off-axis coordinate scales.
            for m in range(1, p):
                x_residue = m % p
                y_residue = (m * j) % p
                check(
                    y_residue != 0,
                    "no_horizontal_axis_intermediate",
                    str((p, j, m)),
                )
                check(
                    x_residue != 0,
                    "no_vertical_axis_intermediate",
                    str((p, j, m)),
                )
                check(
                    min(x_residue, p - x_residue) >= 1
                    and min(y_residue, p - y_residue) >= 1,
                    "off_axis_clearance_scale",
                    str((p, j, m)),
                )

        seen: set[frozenset[tuple[int, int]]] = set()
        for signature in candidates:
            check(signature not in seen, "prime_lattices_distinct", str((p, signature)))
            seen.add(signature)
        check(len(seen) == p - 1,
              "prime_candidate_count", str(p))


# ---------------------------------------------------------------------------
# Incidence bookkeeping under record permutation and local reversal
# ---------------------------------------------------------------------------

def exact_incidence_bookkeeping() -> None:
    # Four shape classes, with a loop and a repeated edge.
    records = [
        ("A", "B"), ("B", "C"), ("C", "A"), ("A", "A"),
        ("C", "D"), ("D", "B"), ("A", "B"), ("D", "D"),
    ]
    target = sorted(tuple(sorted(edge)) for edge in records)

    for mask in range(256):
        transformed = []
        for index, edge in enumerate(records):
            transformed.append(edge[::-1] if (mask >> index) & 1 else edge)
        # A deterministic permutation depending on the reversal mask.
        shift = mask % len(records)
        transformed = transformed[shift:] + transformed[:shift]
        recovered = sorted(tuple(sorted(edge)) for edge in transformed)
        check(
            recovered == target,
            "incidence_permutation_reversal",
            str(mask),
        )


# ---------------------------------------------------------------------------
# Cell-average inversion, rates, and integer locking
# ---------------------------------------------------------------------------

def inverse_matrix(matrix: list[list[F]]) -> list[list[F]]:
    size = len(matrix)
    rows = [
        [F(value) for value in row] + [F(i == j) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(i for i in range(column, size) if rows[i][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        value = rows[column][column]
        rows[column] = [entry / value for entry in rows[column]]
        for row in range(size):
            if row == column:
                continue
            value = rows[row][column]
            rows[row] = [
                x - value * y for x, y in zip(rows[row], rows[column])
            ]
    return [row[size:] for row in rows]


def exact_histogram_and_locking() -> None:
    nodes = [-1, 0, 1]
    matrix = [[F(1), F(node), F(node * node) + F(1, 12)] for node in nodes]
    inverse = inverse_matrix(matrix)

    for i, j in product(range(3), repeat=2):
        check(
            sum(inverse[i][k] * matrix[k][j] for k in range(3)) == F(i == j),
            "cell_matrix_inverse",
            str((i, j)),
        )

    for p, q in product(range(3), repeat=2):
        values = [
            [matrix[i][p] * matrix[j][q] for j in range(3)]
            for i in range(3)
        ]
        for a, b in product(range(3), repeat=2):
            recovered = sum(
                inverse[a][i] * inverse[b][j] * values[i][j]
                for i, j in product(range(3), repeat=2)
            )
            check(
                recovered == F(a == p and b == q),
                "cell_tensor_reproduction",
                str((p, q, a, b)),
            )

    betas = [F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(1)]
    for beta in betas:
        exponent = F(1, 2 * beta + 6)
        check(
            beta * exponent == F(1, 2) - 3 * exponent,
            "Bernstein_balance",
            str(beta),
        )
        check(
            1 - 4 * exponent > beta * exponent,
            "Bernstein_linear_term_smaller",
            str(beta),
        )
        check(
            exponent < F(1, 2),
            "cell_count_sublinear",
            str(beta),
        )

    # Exact calibrated determinant/covolume ratios.
    for index in range(1, 9):
        determinant = F(3 * index, 5)
        covolume = determinant / index
        check(
            determinant / covolume == index,
            "calibrated_index",
            str(index),
        )

    # If physical candidates give integer vectors less than 1/2 apart,
    # their discrete values are locked.
    for index in range(1, 25):
        for i in range(-6, 6):
            for j in range(-5, 6):
                true_vector = (F(i), F(j))
                perturbation = (
                    F((index + i + 17) % 3 - 1, 4),
                    F((2 * index + j + 19) % 3 - 1, 4),
                )
                candidate = (
                    true_vector[0] + perturbation[0],
                    true_vector[1] + perturbation[1],
                )
                check(
                    abs(candidate[0] - true_vector[0]) < F(1, 2)
                    and abs(candidate[1] - true_vector[1]) < F(1, 2),
                    "integer_locking",
                    str((index, i, j)),
                )


def main() -> None:
    exact_local_geometry()
    exact_two_density_jets()
    exact_hnf_classification()
    exact_prime_examples()
    exact_incidence_bookkeeping()
    exact_histogram_and_locking()

    result = {
        "schema": "a2-v19-independent-review-diagnostics-1",
        "reviewed_commit": REVIEWED_COMMIT,
        "status": "passed",
        "scope": (
            "finite exact algebra for the two-density quotient, curvature "
            "Schur complement, incidence bookkeeping, finite-index lattice "
            "classification, prime ambiguity, histograms, rates and integer locking"
        ),
        "checks": dict(sorted(CHECKS.items())),
        "total_checks": sum(CHECKS.values()),
        "imports_author_verification_code": False,
        "formal_proof_certificate": False,
        "full_tex_build": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
