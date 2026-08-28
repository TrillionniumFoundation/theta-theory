#!/usr/bin/env python3
"""Independent Gate-3 resolver for the 320 owner/Voronoi descriptors.

The audited owner/Voronoi first pass used a global source-wise candidate
union and left 320 target--target common-tangent descriptors unresolved on
the full parameter window.  This certificate regenerates exactly that
descriptor set (digest ``c04fc5...38a2``), but it does not reuse the old
endpoint verdict.

The decisive audit is physical: on an ``earlier`` common-tangent branch the
other contact can delimit visibility of T only when its contact time is
forward.  The old branch checked that no third target preceded B but omitted
``ell_B > 0``.  Every apparently physical leaf among the 320 rows has
``ell_B < 0``.  All remaining rows have one of four other strict empty
witnesses.  A closed dyadic cover therefore classifies all 320 descriptors
as physically empty.

For completeness the executable also:

* isolates the 16 old third-target transition roots and four old tau=3
  roots by exact rational polynomials and Sturm counts;
* transports every source-intersecting cover leaf into its true dominant
  source-normal cell and records rigorous (s,t,p) boxes;
* isolates the eight nonphysical dominant-cell seam duplicates by exact
  Q(sqrt(2)) elimination and Sturm counts.

No frozen v51/v52 file, shared log, or owner/Voronoi source is modified.
The script is fail-closed: any new descriptor, witness type, root count,
cell transition, or digest aborts.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_owner_voronoi_event_registry_cert as owner


ctx.prec = 256
Q = Fraction
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

OWNER_CERT = HERE / "cm2_gate3_owner_voronoi_event_registry_cert.py"
OWNER_MANIFEST = HERE / "cm2-gate3-owner-voronoi-event-registry-manifest-2026-07-15.json"
# Filled with the corrected owner's final immutable hashes by the release
# step.  The semantic checks below remain the primary dependency guard.
OWNER_CERT_SHA256 = "4ec63085667e3fb3a5a4ad9d57195754b92d7f5ee848bd8d5933f897a2085c7a"
OWNER_MANIFEST_SHA256 = "d7b1f9d879b9c02257552a6c51fad16de477e60deaac250b4fc55a13be44e8e5"

EXPECTED_ORIGINAL_SEED_COUNT = 320
EXPECTED_ORIGINAL_SEED_SHA256 = (
    "c04fc55676bcb0341c24f8ae5f50116913bb9b70b18ca901873c7e1ff15238a2"
)
S_LOWER, S_UPPER = -base.EPS, base.EPS
TAU_MAX = base.TAU_MAX
R = base.RADIUS
TARGET_BY_ID = {target.target_id: target for target in base.TARGETS}
SOURCES = ("G", "W")

Descriptor = tuple[str, str, int, str, int, int]
Poly = tuple[Q, ...]  # ascending powers
QuadPoly = tuple[Poly, Poly]  # A(s) + sqrt(2) B(s)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def update_digest(state: "hashlib._Hash", value: Any) -> None:
    state.update(canonical_json(value).encode("utf-8"))
    state.update(b"\n")


def descriptor_dict(descriptor: Descriptor) -> dict[str, Any]:
    source, target, epsilon_t, other, epsilon_b, line_branch = descriptor
    return {
        "source": source,
        "target": target,
        "epsilon_target": epsilon_t,
        "other": other,
        "epsilon_other": epsilon_b,
        "line_branch": line_branch,
    }


# ---------------------------------------------------------------------------
# Exact rational-polynomial engine


def poly_trim(value: Poly) -> Poly:
    rows = list(value)
    while len(rows) > 1 and rows[-1] == 0:
        rows.pop()
    return tuple(rows)


def poly_add(left: Poly, right: Poly) -> Poly:
    return poly_trim(tuple(
        (left[index] if index < len(left) else Q(0))
        + (right[index] if index < len(right) else Q(0))
        for index in range(max(len(left), len(right)))
    ))


def poly_scale(value: Poly, scalar: Q) -> Poly:
    return poly_trim(tuple(scalar * coefficient for coefficient in value))


def poly_sub(left: Poly, right: Poly) -> Poly:
    return poly_add(left, poly_scale(right, Q(-1)))


def poly_mul(left: Poly, right: Poly) -> Poly:
    result = [Q(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return poly_trim(tuple(result))


def poly_eval(value: Poly, point: Q) -> Q:
    result = Q(0)
    for coefficient in reversed(value):
        result = result * point + coefficient
    return result


def poly_derivative(value: Poly) -> Poly:
    if len(value) == 1:
        return (Q(0),)
    return poly_trim(tuple(
        index * value[index] for index in range(1, len(value))
    ))


def poly_divmod(numerator: Poly, denominator: Poly) -> tuple[Poly, Poly]:
    denominator = poly_trim(denominator)
    assert any(denominator)
    remainder = list(poly_trim(numerator))
    quotient = [Q(0)] * max(1, len(remainder) - len(denominator) + 1)
    while len(remainder) >= len(denominator) and any(remainder):
        shift = len(remainder) - len(denominator)
        coefficient = remainder[-1] / denominator[-1]
        quotient[shift] += coefficient
        for index, value in enumerate(denominator):
            remainder[index + shift] -= coefficient * value
        while len(remainder) > 1 and remainder[-1] == 0:
            remainder.pop()
    return poly_trim(tuple(quotient)), poly_trim(tuple(remainder))


def sturm_root_count(value: Poly, lower: Q, upper: Q) -> int:
    """Exact number of distinct roots in the open rational interval."""

    value = poly_trim(value)
    assert len(value) >= 2 and lower < upper
    assert poly_eval(value, lower) != 0 and poly_eval(value, upper) != 0
    sequence = [value, poly_derivative(value)]
    while any(sequence[-1]):
        _quotient, remainder = poly_divmod(sequence[-2], sequence[-1])
        if not any(remainder):
            break
        sequence.append(poly_scale(remainder, Q(-1)))

    def variations(point: Q) -> int:
        signs = []
        for polynomial in sequence:
            evaluated = poly_eval(polynomial, point)
            if evaluated:
                signs.append(1 if evaluated > 0 else -1)
        return sum(left != right for left, right in zip(signs, signs[1:]))

    return variations(lower) - variations(upper)


def qpoly_add(left: QuadPoly, right: QuadPoly) -> QuadPoly:
    return poly_add(left[0], right[0]), poly_add(left[1], right[1])


def qpoly_scale(value: QuadPoly, scalar: Q) -> QuadPoly:
    return poly_scale(value[0], scalar), poly_scale(value[1], scalar)


def qpoly_sub(left: QuadPoly, right: QuadPoly) -> QuadPoly:
    return qpoly_add(left, qpoly_scale(right, Q(-1)))


def qpoly_mul(left: QuadPoly, right: QuadPoly) -> QuadPoly:
    # (A+B sqrt2)(C+D sqrt2)=(AC+2BD)+(AD+BC)sqrt2.
    return (
        poly_add(poly_mul(left[0], right[0]), poly_scale(poly_mul(left[1], right[1]), Q(2))),
        poly_add(poly_mul(left[0], right[1]), poly_mul(left[1], right[0])),
    )


def affine_target_center(target_id: str) -> tuple[Poly, Poly]:
    target = TARGET_BY_ID[target_id]
    if target.obstacle == "G":
        return (Q(target.ix), Q(0)), (Q(target.iy), Q(0))
    return (
        (Q(target.ix) + Q(1, 2), Q(1)),
        (Q(target.iy) + Q(1, 2), Q(0)),
    )


def affine_source_center(source: str) -> tuple[Poly, Poly]:
    if source == "G":
        return (Q(0), Q(0)), (Q(0), Q(0))
    return (Q(1, 2), Q(1)), (Q(1, 2), Q(0))


def third_tangency_polynomial(
    descriptor: Descriptor, third_id: str, epsilon_c: int,
) -> Poly:
    """Exact T/B/C common-line equation, degree at most two here."""

    _source, target_id, epsilon_t, other_id, epsilon_b, _branch = descriptor
    ax, ay = affine_target_center(target_id)
    bx, by = affine_target_center(other_id)
    cx, cy = affine_target_center(third_id)
    dx, dy = poly_sub(bx, ax), poly_sub(by, ay)
    ex, ey = poly_sub(ax, cx), poly_sub(ay, cy)
    target = TARGET_BY_ID[target_id]
    other = TARGET_BY_ID[other_id]
    third = TARGET_BY_ID[third_id]
    h = epsilon_b * R[other.obstacle] - epsilon_t * R[target.obstacle]
    g = epsilon_t * R[target.obstacle] - epsilon_c * R[third.obstacle]
    first = poly_sub(poly_scale(ey, h), poly_scale(dy, g))
    second = poly_sub(poly_scale(dx, g), poly_scale(ex, h))
    determinant = poly_sub(poly_mul(dx, ey), poly_mul(dy, ex))
    return poly_sub(
        poly_add(poly_mul(first, first), poly_mul(second, second)),
        poly_mul(determinant, determinant),
    )


def tau_three_polynomial(descriptor: Descriptor) -> Poly:
    """Eliminate the common-tangent radical from ell_T=3 exactly.

    With v=a-c, d=b-a, D=|d|^2, h=eps_B R_B-eps_T R_T and
    rho^2=D-h^2, the source-circle equation at flight L is A+B rho=0.
    The returned polynomial is A^2-B^2 rho^2.  Branch and sign are checked
    independently by the enclosing Arb flight-time sign change.
    """

    source, target_id, epsilon_t, other_id, epsilon_b, branch = descriptor
    ax, ay = affine_target_center(target_id)
    bx, by = affine_target_center(other_id)
    cx, cy = affine_source_center(source)
    dx, dy = poly_sub(bx, ax), poly_sub(by, ay)
    vx, vy = poly_sub(ax, cx), poly_sub(ay, cy)
    distance_squared = poly_add(poly_mul(dx, dx), poly_mul(dy, dy))
    dot = poly_add(poly_mul(vx, dx), poly_mul(vy, dy))
    cross = poly_sub(poly_mul(vx, dy), poly_mul(vy, dx))
    norm_v_squared = poly_add(poly_mul(vx, vx), poly_mul(vy, vy))
    target = TARGET_BY_ID[target_id]
    other = TARGET_BY_ID[other_id]
    rt, rb, rs = R[target.obstacle], R[other.obstacle], R[source]
    h = epsilon_b * rb - epsilon_t * rt
    flight = Q(3)
    constant = flight * flight + rt * rt - rs * rs
    k_poly = poly_add(norm_v_squared, (constant,))
    a_poly = poly_sub(
        poly_sub(
            poly_mul(distance_squared, k_poly),
            poly_scale(cross, 2 * flight * h),
        ),
        poly_scale(dot, 2 * epsilon_t * rt * h),
    )
    b_poly = poly_scale(
        poly_sub(poly_scale(cross, epsilon_t * rt), poly_scale(dot, flight)),
        2 * branch,
    )
    radical_squared = poly_sub(distance_squared, (h * h,))
    return poly_sub(
        poly_mul(a_poly, a_poly),
        poly_mul(poly_mul(b_poly, b_poly), radical_squared),
    )


def dominant_seam_polynomial(
    descriptor: Descriptor, sign_x: int, sign_y: int,
) -> Poly:
    """Exact diagonal-source-normal equation in Q[sqrt(2)][s]."""

    source, target_id, epsilon_t, other_id, epsilon_b, _branch = descriptor
    ax, ay = affine_target_center(target_id)
    bx, by = affine_target_center(other_id)
    sx, sy = affine_source_center(source)
    dx, dy = poly_sub(bx, ax), poly_sub(by, ay)
    # q=c+R_S(sign_x,sign_y)/sqrt(2); 1/sqrt(2)=sqrt(2)/2.
    ex: QuadPoly = (poly_sub(ax, sx), (Q(-sign_x) * R[source] / 2,))
    ey: QuadPoly = (poly_sub(ay, sy), (Q(-sign_y) * R[source] / 2,))
    qdx: QuadPoly = (dx, (Q(0),))
    qdy: QuadPoly = (dy, (Q(0),))
    target = TARGET_BY_ID[target_id]
    other = TARGET_BY_ID[other_id]
    h = epsilon_b * R[other.obstacle] - epsilon_t * R[target.obstacle]
    k = epsilon_t * R[target.obstacle]
    first = qpoly_sub(qpoly_scale(ey, h), qpoly_scale(qdy, k))
    second = qpoly_sub(qpoly_scale(qdx, k), qpoly_scale(ex, h))
    determinant = qpoly_sub(qpoly_mul(qdx, ey), qpoly_mul(qdy, ex))
    equation = qpoly_sub(
        qpoly_add(qpoly_mul(first, first), qpoly_mul(second, second)),
        qpoly_mul(determinant, determinant),
    )
    # A+B sqrt(2)=0 implies A^2-2B^2=0.  The labelled branch is separately
    # selected by the Arb sign change in the same isolating collar.
    return poly_sub(
        poly_mul(equation[0], equation[0]),
        poly_scale(poly_mul(equation[1], equation[1]), Q(2)),
    )


# ---------------------------------------------------------------------------
# Reproduction of the audited 320-row first pass


def common_tangent_descriptors() -> Iterable[Descriptor]:
    # The global unions and ordering are part of the audited owner registry.
    yield from owner.common_tangent_descriptors()


def strict_clear_before(
    rows: dict[str, tuple[arb, arb, arb]], threshold: arb,
    excluded: set[str],
) -> tuple[bool, bool]:
    unresolved = False
    for target_id, (ell, delta, _w) in rows.items():
        if target_id in excluded:
            continue
        if bool(ell < 0) or bool(ell > threshold) or bool(delta < 0):
            continue
        if bool(ell > 0) and bool(ell < threshold) and bool(delta > 0):
            return False, True
        unresolved = True
    return (not unresolved), False


def strict_clear_between(
    rows: dict[str, tuple[arb, arb, arb]], lower: arb, upper: arb,
    excluded: set[str],
) -> tuple[bool, bool]:
    unresolved = False
    for target_id, (ell, delta, _w) in rows.items():
        if target_id in excluded:
            continue
        if bool(ell < lower) or bool(ell > upper) or bool(delta < 0):
            continue
        if bool(ell > lower) and bool(ell < upper) and bool(delta > 0):
            return False, True
        unresolved = True
    return (not unresolved), False


def original_first_pass_classification(
    descriptor: Descriptor, s0: Q = S_LOWER, s1: Q = S_UPPER,
) -> str:
    """Replay the pre-correction branch, including its missing ell_B>0."""

    source, target_id, epsilon_t, other_id, epsilon_b, line_branch = descriptor
    initial, geometry = owner.common_tangent_source_geometry(
        source, target_id, epsilon_t, other_id, epsilon_b, line_branch, s0, s1,
    )
    if geometry is None:
        if initial == "source_grazing_transition_unresolved":
            if owner.source_grazing_identity_sides(
                source, target_id, epsilon_t, other_id, epsilon_b,
            ):
                return "source_grazing_identity_boundary"
        return initial
    s, qx, qy, ux, uy, ell_t, ell_b, *_rest = geometry
    if bool(ell_t < 0):
        return "target_tangency_behind_source"
    if bool(ell_t > base.arbq(TAU_MAX)):
        return "target_tangency_after_tau3"
    if not (bool(ell_t > 0) and bool(ell_t < base.arbq(TAU_MAX))):
        return "target_time_endpoint_unresolved"
    if bool(ell_b > ell_t):
        order = "later"
    elif bool(ell_b < ell_t):
        order = "earlier"
    else:
        return "strict_tangent_time_order_unresolved"

    rows = owner.competitor_rows(source, qx, qy, ux, uy, s, target_id)
    if order == "later":
        clear_t, blocker_t = strict_clear_before(rows, ell_t, {other_id})
        if blocker_t:
            return "nonphysical_target_strictly_occluded"
        if not clear_t:
            return "target_visibility_unresolved"
        clear_between, blocker_between = strict_clear_between(
            rows, ell_t, ell_b, {other_id},
        )
        if blocker_between:
            return "physical_target_but_other_is_not_next"
        if not clear_between:
            return "later_miss_order_unresolved"
        return "physical_later_miss_switch_boundary"

    # This deliberately reproduces the audited omission: no ell_b>0 test.
    clear_b, blocker_b = strict_clear_before(rows, ell_b, {other_id})
    if blocker_b:
        return "nonphysical_earlier_tangent_strictly_blocked"
    if not clear_b:
        return "earlier_tangent_visibility_unresolved"
    clear_t_without_b, blocker_t_without_b = strict_clear_before(
        rows, ell_t, {other_id},
    )
    if blocker_t_without_b:
        return "earlier_tangent_physical_but_target_still_occluded"
    if not clear_t_without_b:
        return "target_after_earlier_tangent_unresolved"
    return "physical_earlier_occlusion_boundary"


def original_seed_rows() -> list[tuple[Descriptor, str]]:
    rows = []
    digest_rows = []
    counts: Counter[str] = Counter()
    for descriptor in common_tangent_descriptors():
        classification = original_first_pass_classification(descriptor)
        if classification.endswith("_unresolved"):
            rows.append((descriptor, classification))
            counts[classification] += 1
            digest_rows.append(descriptor_dict(descriptor))
    assert len(rows) == EXPECTED_ORIGINAL_SEED_COUNT
    assert canonical_digest(digest_rows) == EXPECTED_ORIGINAL_SEED_SHA256
    assert dict(sorted(counts.items())) == {
        "earlier_tangent_visibility_unresolved": 16,
        "later_miss_order_unresolved": 4,
        "source_grazing_transition_unresolved": 176,
        "target_after_earlier_tangent_unresolved": 40,
        "target_time_endpoint_unresolved": 76,
        "target_visibility_unresolved": 8,
    }
    return rows


# ---------------------------------------------------------------------------
# Corrected physical geometry and empty witnesses


def common_translation_family(descriptor: Descriptor) -> bool:
    source, target, _et, other, _eb, _branch = descriptor
    return (
        source == "W"
        and TARGET_BY_ID[target].obstacle == "W"
        and TARGET_BY_ID[other].obstacle == "W"
    )


def source_geometry(
    descriptor: Descriptor, s0: Q, s1: Q,
) -> tuple[str, tuple[arb, ...] | None, str]:
    """Owner geometry with exact W/W/W common-translation reduction."""

    status, geometry = owner.common_tangent_source_geometry(*descriptor, s0, s1)
    if (
        geometry is None
        and status == "source_grazing_transition_unresolved"
        and common_translation_family(descriptor)
    ):
        status0, point = owner.common_tangent_source_geometry(
            *descriptor, Q(0), Q(0),
        )
        if point is None:
            assert status0 == "no_source_intersection"
            return status0, None, "exact_common_translation_reduction"
        s = base.arb_interval(s0, s1)
        values = list(point)
        values[0] = s
        values[1] = point[1] + s
        # q_y,u,ell,source normal are invariant under the common x shift.
        return status0, tuple(values), "exact_common_translation_reduction"
    return status, geometry, "direct_arb"


def empty_witness(
    descriptor: Descriptor, s0: Q, s1: Q,
) -> dict[str, Any] | None:
    status, geometry, reduction = source_geometry(descriptor, s0, s1)
    if geometry is None:
        if status == "no_source_intersection":
            return {
                "kind": "no_source_intersection",
                "reduction": reduction,
            }
        return None

    source, target_id, _epsilon_t, other_id, _epsilon_b, line_branch = descriptor
    s, qx, qy, ux, uy, ell_t, ell_b, *_rest = geometry
    rows = owner.competitor_rows(source, qx, qy, ux, uy, s, target_id)

    # A strict third hit before T persists in a neighbourhood of this
    # common-tangent curve, so T is not the owner even after B is removed.
    for blocker in sorted(rows):
        if blocker == other_id:
            continue
        ell, delta, _w = rows[blocker]
        if bool(ell > 0) and bool(ell < ell_t) and bool(delta > 0):
            return {
                "kind": "strict_third_target_before_target",
                "blocker": blocker,
                "blocker_center_time": str(ell),
                "blocker_discriminant": str(delta),
                "target_time": str(ell_t),
                "reduction": reduction,
            }

    # Missing condition in the audited earlier branch.  A disk tangent only
    # on the backward ray cannot open or close forward visibility of T.
    if line_branch == -1 and bool(ell_b < 0):
        return {
            "kind": "earlier_common_tangent_behind_source",
            "other_time": str(ell_b),
            "target_time": str(ell_t),
            "reduction": reduction,
        }

    if bool(ell_t < 0):
        return {
            "kind": "target_behind_source",
            "target_time": str(ell_t),
            "reduction": reduction,
        }

    if bool(ell_t > base.arbq(TAU_MAX)):
        return {
            "kind": "target_after_tau3",
            "target_time": str(ell_t),
            "reduction": reduction,
        }

    # For a later common tangent, a strict third hit between T and B means B
    # is not the miss owner and its tangency cannot switch the recorded trace.
    if line_branch == 1:
        for blocker in sorted(rows):
            if blocker == other_id:
                continue
            ell, delta, _w = rows[blocker]
            if bool(ell > ell_t) and bool(ell < ell_b) and bool(delta > 0):
                return {
                    "kind": "later_other_not_next",
                    "intervening_target": blocker,
                    "target_time": str(ell_t),
                    "intervening_center_time": str(ell),
                    "other_time": str(ell_b),
                    "intervening_discriminant": str(delta),
                    "reduction": reduction,
                }
    return None


def adaptive_empty_resolution(
    seeds: list[tuple[Descriptor, str]], max_depth: int = 12,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    descriptor_rows: list[dict[str, Any]] = []
    leaf_rows: list[dict[str, Any]] = []
    descriptor_counts: Counter[str] = Counter()
    leaf_counts: Counter[str] = Counter()
    legacy_matrix: dict[str, Counter[str]] = defaultdict(Counter)
    maximum_depth = 0

    for descriptor, legacy_kind in seeds:
        pending = [(S_LOWER, S_UPPER, 0, "")]
        leaves: list[tuple[Q, Q, int, str, dict[str, Any]]] = []
        while pending:
            s0, s1, depth, path = pending.pop()
            witness = empty_witness(descriptor, s0, s1)
            if witness is None:
                assert depth < max_depth, (descriptor, s0, s1, depth)
                middle = (s0 + s1) / 2
                pending.append((middle, s1, depth + 1, path + "1"))
                pending.append((s0, middle, depth + 1, path + "0"))
                continue
            leaves.append((s0, s1, depth, path, witness))
            maximum_depth = max(maximum_depth, depth)
            leaf_counts[witness["kind"]] += 1

        leaves.sort(key=lambda row: row[0])
        assert leaves[0][0] == S_LOWER and leaves[-1][1] == S_UPPER
        for left, right in zip(leaves, leaves[1:]):
            assert left[1] == right[0]
        kinds = {row[4]["kind"] for row in leaves}
        assert len(kinds) == 1
        witness_kind = next(iter(kinds))
        descriptor_counts[witness_kind] += 1
        legacy_matrix[legacy_kind][witness_kind] += 1

        local_rows = []
        for s0, s1, depth, path, witness in leaves:
            row = {
                **descriptor_dict(descriptor),
                "s": [str(s0), str(s1)],
                "depth": depth,
                "path": path,
                "classification": "EMPTY",
                "witness": witness,
            }
            leaf_rows.append(row)
            local_rows.append(row)
        descriptor_rows.append({
            **descriptor_dict(descriptor),
            "legacy_first_pass_classification": legacy_kind,
            "exact_tangent_order": "earlier" if descriptor[-1] == -1 else "later",
            "resolver_classification": "EMPTY",
            "empty_witness_kind": witness_kind,
            "cover_leaf_count": len(leaves),
            "cover_rows_sha256": canonical_digest(local_rows),
        })

    expected_descriptor_counts = {
        "earlier_common_tangent_behind_source": 52,
        "later_other_not_next": 12,
        "no_source_intersection": 32,
        "strict_third_target_before_target": 164,
        "target_behind_source": 60,
    }
    expected_leaf_counts = {
        "earlier_common_tangent_behind_source": 52,
        "later_other_not_next": 16,
        "no_source_intersection": 128,
        "strict_third_target_before_target": 188,
        "target_behind_source": 64,
    }
    assert dict(sorted(descriptor_counts.items())) == expected_descriptor_counts
    assert dict(sorted(leaf_counts.items())) == expected_leaf_counts
    assert len(descriptor_rows) == 320 and len(leaf_rows) == 448
    assert maximum_depth == 3
    assert Counter(row["exact_tangent_order"] for row in descriptor_rows) == {
        "earlier": 220,
        "later": 100,
    }

    expected_legacy_matrix = {
        "earlier_tangent_visibility_unresolved": {
            "strict_third_target_before_target": 16,
        },
        "later_miss_order_unresolved": {"later_other_not_next": 4},
        "source_grazing_transition_unresolved": {
            "earlier_common_tangent_behind_source": 20,
            "later_other_not_next": 4,
            "no_source_intersection": 32,
            "strict_third_target_before_target": 60,
            "target_behind_source": 60,
        },
        "target_after_earlier_tangent_unresolved": {
            "earlier_common_tangent_behind_source": 32,
            "strict_third_target_before_target": 8,
        },
        "target_time_endpoint_unresolved": {
            "strict_third_target_before_target": 76,
        },
        "target_visibility_unresolved": {
            "later_other_not_next": 4,
            "strict_third_target_before_target": 4,
        },
    }
    normalized_matrix = {
        legacy: dict(sorted(counts.items()))
        for legacy, counts in sorted(legacy_matrix.items())
    }
    assert normalized_matrix == expected_legacy_matrix

    summary = {
        "descriptor_count": len(descriptor_rows),
        "resolver_classification_counts": {"EMPTY": 320},
        "empty_descriptor_witness_counts": expected_descriptor_counts,
        "exact_tangent_order_counts": {"earlier": 220, "later": 100},
        "adaptive_cover_leaf_count": len(leaf_rows),
        "adaptive_cover_maximum_depth": maximum_depth,
        "adaptive_cover_leaf_witness_counts": expected_leaf_counts,
        "legacy_to_resolver_matrix": expected_legacy_matrix,
        "descriptor_rows_sha256": canonical_digest(descriptor_rows),
        "adaptive_cover_rows_sha256": canonical_digest(leaf_rows),
        "physical_boundary_count": 0,
        "physical_duplicate_count": 0,
        "physical_earlier_count": 0,
        "physical_later_count": 0,
        "physical_joint_count": 0,
        "unresolved_count": 0,
    }
    return descriptor_rows, leaf_rows, summary


# ---------------------------------------------------------------------------
# Legacy transition-root boxes, now with corrected physical verdicts


def point_sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    raise AssertionError(f"point sign unresolved: {value}")


def bisect_sign_change(
    function: Any, lower: Q, upper: Q, iterations: int = 56,
) -> tuple[Q, Q, int, int]:
    left_sign = point_sign(function(lower))
    right_sign = point_sign(function(upper))
    assert left_sign == -right_sign
    for _ in range(iterations):
        middle = (lower + upper) / 2
        middle_sign = point_sign(function(middle))
        if middle_sign == left_sign:
            lower = middle
        else:
            upper = middle
    assert point_sign(function(lower)) == left_sign
    assert point_sign(function(upper)) == right_sign
    return lower, upper, left_sign, right_sign


def dominant_cell(geometry: tuple[arb, ...]) -> str | None:
    snx, sny = geometry[8], geometry[9]
    if bool(snx > sny) and bool(snx > -sny):
        return "E"
    if bool(-snx > sny) and bool(-snx > -sny):
        return "W"
    if bool(sny > snx) and bool(sny > -snx):
        return "N"
    if bool(-sny > snx) and bool(-sny > -snx):
        return "S"
    return None


def phase_box(
    descriptor: Descriptor, s0: Q, s1: Q, geometry: tuple[arb, ...],
    cell: str | None,
) -> dict[str, Any]:
    ux, uy = geometry[3], geometry[4]
    snx, sny = geometry[8], geometry[9]
    p = -ux * sny + uy * snx
    assert bool(p > -1) and bool(p < 1)
    if cell in {"E", "W"}:
        t = sny
    elif cell in {"N", "S"}:
        t = snx
    else:
        # At a true dominant seam either coordinate is a valid closed-chart
        # coordinate.  Record both rather than selecting an artificial side.
        t = None
    row: dict[str, Any] = {
        "s": [str(s0), str(s1)],
        "p": str(p),
        "source_normal_x": str(snx),
        "source_normal_y": str(sny),
        "dominant_cell": cell,
    }
    if t is not None:
        assert bool(t > -1) and bool(t < 1)
        row["t"] = str(t)
        chart_id = f"{descriptor[0]}:{cell}"
        row["chart_id"] = chart_id
        row["target_retained_in_true_cell"] = descriptor[1] in base.candidate_ids(chart_id)
        row["other_retained_in_true_cell"] = descriptor[3] in base.candidate_ids(chart_id)
    else:
        row["t_x_chart"] = str(sny)
        row["t_y_chart"] = str(snx)
    return row


def third_signed_gap(
    descriptor: Descriptor, third: str, epsilon_c: int, s_value: Q,
) -> arb:
    status, geometry, _reduction = source_geometry(descriptor, s_value, s_value)
    assert status == "source_intersection" and geometry is not None
    s, qx, qy, ux, uy = geometry[:5]
    rows = owner.competitor_rows(
        descriptor[0], qx, qy, ux, uy, s, descriptor[1],
    )
    w = rows[third][2]
    radius = base.arbq(R[TARGET_BY_ID[third].obstacle])
    return epsilon_c * w - radius


def flight_three_gap(descriptor: Descriptor, s_value: Q) -> arb:
    status, geometry, _reduction = source_geometry(descriptor, s_value, s_value)
    assert status == "source_intersection" and geometry is not None
    return geometry[5] - base.arbq(Q(3))


def legacy_transition_root_boxes(
    seeds: list[tuple[Descriptor, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    third_count = 0
    tau_count = 0

    for descriptor, legacy_kind in seeds:
        left_kind = original_first_pass_classification(
            descriptor, S_LOWER, S_LOWER,
        )
        right_kind = original_first_pass_classification(
            descriptor, S_UPPER, S_UPPER,
        )
        endpoint_kinds = {left_kind, right_kind}

        if endpoint_kinds == {
            "physical_earlier_occlusion_boundary",
            "earlier_tangent_physical_but_target_still_occluded",
        }:
            assert legacy_kind == "target_after_earlier_tangent_unresolved"
            blocked_s = (
                S_LOWER
                if left_kind == "earlier_tangent_physical_but_target_still_occluded"
                else S_UPPER
            )
            clear_s = S_UPPER if blocked_s == S_LOWER else S_LOWER
            status, geometry, _reduction = source_geometry(
                descriptor, blocked_s, blocked_s,
            )
            assert status == "source_intersection" and geometry is not None
            s, qx, qy, ux, uy, ell_t = geometry[:6]
            competitors = owner.competitor_rows(
                descriptor[0], qx, qy, ux, uy, s, descriptor[1],
            )
            blockers = [
                target_id
                for target_id, (ell, delta, _w) in competitors.items()
                if target_id != descriptor[3]
                and bool(ell > 0) and bool(ell < ell_t) and bool(delta > 0)
            ]
            assert len(blockers) == 1
            third = blockers[0]
            epsilon_c = point_sign(competitors[third][2])
            assert point_sign(third_signed_gap(
                descriptor, third, epsilon_c, blocked_s,
            )) == -1
            assert point_sign(third_signed_gap(
                descriptor, third, epsilon_c, clear_s,
            )) == 1
            s0, s1, left_sign, right_sign = bisect_sign_change(
                lambda value: third_signed_gap(descriptor, third, epsilon_c, value),
                S_LOWER,
                S_UPPER,
            )
            polynomial = third_tangency_polynomial(descriptor, third, epsilon_c)
            assert sturm_root_count(polynomial, s0, s1) == 1
            status_box, geometry_box, _reduction = source_geometry(descriptor, s0, s1)
            assert status_box == "source_intersection" and geometry_box is not None
            cell = dominant_cell(geometry_box)
            assert cell is not None
            full_witness = empty_witness(descriptor, S_LOWER, S_UPPER)
            assert full_witness is not None
            assert full_witness["kind"] == "earlier_common_tangent_behind_source"
            rows.append({
                **descriptor_dict(descriptor),
                "legacy_transition_type": "third_target_tangency",
                "legacy_claim_retracted": "physical_joint_vertex",
                "resolver_classification": "EMPTY_NOT_JOINT",
                "third_target": third,
                "epsilon_third": epsilon_c,
                "exact_polynomial_coefficients_ascending": [
                    str(coefficient) for coefficient in polynomial
                ],
                "sturm_root_count_in_s_box": 1,
                "signed_gap_endpoint_signs": [left_sign, right_sign],
                "root_box": phase_box(descriptor, s0, s1, geometry_box, cell),
                "uniform_empty_witness": full_witness,
            })
            third_count += 1
            continue

        if endpoint_kinds == {
            "target_tangency_after_tau3",
            "earlier_tangent_physical_but_target_still_occluded",
        }:
            assert legacy_kind == "target_time_endpoint_unresolved"
            s0, s1, left_sign, right_sign = bisect_sign_change(
                lambda value: flight_three_gap(descriptor, value),
                S_LOWER,
                S_UPPER,
            )
            polynomial = tau_three_polynomial(descriptor)
            assert sturm_root_count(polynomial, s0, s1) == 1
            status_box, geometry_box, _reduction = source_geometry(descriptor, s0, s1)
            assert status_box == "source_intersection" and geometry_box is not None
            cell = dominant_cell(geometry_box)
            assert cell is not None
            full_witness = empty_witness(descriptor, S_LOWER, S_UPPER)
            assert full_witness is not None
            assert full_witness["kind"] == "strict_third_target_before_target"
            rows.append({
                **descriptor_dict(descriptor),
                "legacy_transition_type": "tau_three_crossing",
                "resolver_classification": "EMPTY_NOT_PHYSICAL_BOUNDARY",
                "physical_horizon": "tau_max<3",
                "exact_polynomial_coefficients_ascending": [
                    str(coefficient) for coefficient in polynomial
                ],
                "sturm_root_count_in_s_box": 1,
                "flight_minus_three_endpoint_signs": [left_sign, right_sign],
                "root_box": phase_box(descriptor, s0, s1, geometry_box, cell),
                "uniform_empty_witness": full_witness,
            })
            tau_count += 1

    rows.sort(key=canonical_json)
    assert third_count == 16 and tau_count == 4 and len(rows) == 20
    assert Counter(row["resolver_classification"] for row in rows) == {
        "EMPTY_NOT_JOINT": 16,
        "EMPTY_NOT_PHYSICAL_BOUNDARY": 4,
    }
    summary = {
        "legacy_transition_root_box_count": len(rows),
        "retracted_physical_third_target_vertices": third_count,
        "nonphysical_tau_three_roots": tau_count,
        "exact_sturm_isolated_root_count": len(rows),
        "root_box_rows_sha256": canonical_digest(rows),
        "physical_transition_root_count": 0,
        "unresolved_transition_root_count": 0,
    }
    return rows, summary


# ---------------------------------------------------------------------------
# True dominant-cell atlas and nonphysical seam duplicates


def point_dominant_cell(descriptor: Descriptor, s_value: Q) -> str | None:
    status, geometry, _reduction = source_geometry(descriptor, s_value, s_value)
    if geometry is None:
        assert status == "no_source_intersection"
        return None
    return dominant_cell(geometry)


def dominant_cell_audit(
    seeds: list[tuple[Descriptor, str]], max_depth: int = 24,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    regular_rows: list[dict[str, Any]] = []
    seam_rows: list[dict[str, Any]] = []
    no_phase_count = 0
    maximum_depth = 0
    raw_seam_leaf_count = 0

    for descriptor, _legacy_kind in seeds:
        pending = [(S_LOWER, S_UPPER, 0, "")]
        leaves: list[dict[str, Any]] = []
        while pending:
            s0, s1, depth, path = pending.pop()
            status, geometry, reduction = source_geometry(descriptor, s0, s1)
            if geometry is None:
                if status == "source_grazing_transition_unresolved" and depth < max_depth:
                    middle = (s0 + s1) / 2
                    pending.append((middle, s1, depth + 1, path + "1"))
                    pending.append((s0, middle, depth + 1, path + "0"))
                    continue
                assert status == "no_source_intersection"
                leaves.append({
                    "s0": s0, "s1": s1, "depth": depth, "path": path,
                    "kind": "no_phase", "reduction": reduction,
                })
                maximum_depth = max(maximum_depth, depth)
                continue

            cell = dominant_cell(geometry)
            witness = empty_witness(descriptor, s0, s1)
            # A phase-atlas leaf is accepted only when both its true cell and
            # its physical emptiness are strict on the same closed box.
            if (cell is None or witness is None) and depth < max_depth:
                middle = (s0 + s1) / 2
                pending.append((middle, s1, depth + 1, path + "1"))
                pending.append((s0, middle, depth + 1, path + "0"))
                continue
            assert witness is not None
            if cell is None:
                leaves.append({
                    "s0": s0, "s1": s1, "depth": depth, "path": path,
                    "kind": "seam", "geometry": geometry, "witness": witness,
                })
                raw_seam_leaf_count += 1
            else:
                leaves.append({
                    "s0": s0, "s1": s1, "depth": depth, "path": path,
                    "kind": "cell", "cell": cell, "geometry": geometry,
                    "witness": witness,
                })
            maximum_depth = max(maximum_depth, depth)

        leaves.sort(key=lambda row: row["s0"])
        assert leaves[0]["s0"] == S_LOWER and leaves[-1]["s1"] == S_UPPER
        for left, right in zip(leaves, leaves[1:]):
            assert left["s1"] == right["s0"]

        index = 0
        while index < len(leaves):
            leaf = leaves[index]
            if leaf["kind"] == "no_phase":
                no_phase_count += 1
                index += 1
                continue
            if leaf["kind"] == "cell":
                regular_rows.append({
                    **descriptor_dict(descriptor),
                    "depth": leaf["depth"],
                    "path": leaf["path"],
                    "phase_box": phase_box(
                        descriptor, leaf["s0"], leaf["s1"],
                        leaf["geometry"], leaf["cell"],
                    ),
                    "empty_witness_kind": leaf["witness"]["kind"],
                })
                index += 1
                continue

            start = index
            s0, s1 = leaf["s0"], leaf["s1"]
            while (
                index + 1 < len(leaves)
                and leaves[index + 1]["kind"] == "seam"
                and leaves[index + 1]["s0"] == s1
            ):
                index += 1
                s1 = leaves[index]["s1"]
            end = index
            assert start > 0 and end + 1 < len(leaves)
            left_cell = leaves[start - 1].get("cell")
            right_cell = leaves[end + 1].get("cell")
            assert left_cell is not None and right_cell is not None
            assert left_cell != right_cell
            signs = {
                "E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1),
            }
            sx = signs[left_cell][0] or signs[right_cell][0]
            sy = signs[left_cell][1] or signs[right_cell][1]
            assert sx in {-1, 1} and sy in {-1, 1}
            polynomial = dominant_seam_polynomial(descriptor, sx, sy)
            assert sturm_root_count(polynomial, s0, s1) == 1
            status, geometry, _reduction = source_geometry(descriptor, s0, s1)
            assert status == "source_intersection" and geometry is not None
            witness = empty_witness(descriptor, s0, s1)
            assert witness is not None
            seam_rows.append({
                **descriptor_dict(descriptor),
                "classification": "NONPHYSICAL_CHART_SEAM_DUPLICATE",
                "adjacent_dominant_cells": [left_cell, right_cell],
                "diagonal_source_normal_signs": [sx, sy],
                "exact_polynomial_coefficients_ascending": [
                    str(coefficient) for coefficient in polynomial
                ],
                "sturm_root_count_in_s_box": 1,
                "root_box": phase_box(descriptor, s0, s1, geometry, None),
                "empty_witness": witness,
            })
            index += 1

    regular_rows.sort(key=canonical_json)
    seam_rows.sort(key=canonical_json)
    assert len(seam_rows) == 8
    assert all(row["classification"] == "NONPHYSICAL_CHART_SEAM_DUPLICATE" for row in seam_rows)
    assert maximum_depth == max_depth
    summary = {
        "regular_true_dominant_cell_phase_box_count": len(regular_rows),
        "no_source_phase_leaf_count": no_phase_count,
        "raw_depth_limit_seam_leaf_count": raw_seam_leaf_count,
        "nonphysical_chart_seam_duplicate_root_boxes": len(seam_rows),
        "dominant_cell_adaptive_depth": max_depth,
        "regular_phase_box_rows_sha256": canonical_digest(regular_rows),
        "seam_root_box_rows_sha256": canonical_digest(seam_rows),
        "physical_chart_seam_duplicate_count": 0,
        "dominant_cell_unresolved_count": 0,
    }
    return regular_rows, seam_rows, summary


# ---------------------------------------------------------------------------
# Provenance, aggregate verdict, and CLI


def verify_provenance() -> dict[str, Any]:
    assert OWNER_CERT_SHA256 != "__OWNER_CERT_SHA256__"
    assert OWNER_MANIFEST_SHA256 != "__OWNER_MANIFEST_SHA256__"
    assert sha256_path(OWNER_CERT) == OWNER_CERT_SHA256
    assert sha256_path(OWNER_MANIFEST) == OWNER_MANIFEST_SHA256
    manifest = json.loads(OWNER_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "cm2.gate3.owner-voronoi-event-registry.v1"
    # The corrected owner artifact must retain the audited original set.
    serialized = canonical_json(manifest)
    assert EXPECTED_ORIGINAL_SEED_SHA256 in serialized
    return {
        "owner_cert_sha256": OWNER_CERT_SHA256,
        "owner_manifest_sha256": OWNER_MANIFEST_SHA256,
        "audited_original_seed_count": EXPECTED_ORIGINAL_SEED_COUNT,
        "audited_original_seed_sha256": EXPECTED_ORIGINAL_SEED_SHA256,
    }


def full_summary() -> dict[str, Any]:
    provenance = verify_provenance()
    seeds = original_seed_rows()
    descriptor_rows, leaf_rows, resolution = adaptive_empty_resolution(seeds)
    transition_rows, transitions = legacy_transition_root_boxes(seeds)
    phase_rows, seam_rows, dominant = dominant_cell_audit(seeds)

    # Fail-closed final accounting.  Nonphysical chart seams are coordinate
    # duplicates only; they are not resurrected as physical endpoints.
    assert resolution["descriptor_count"] == 320
    assert resolution["unresolved_count"] == 0
    assert transitions["unresolved_transition_root_count"] == 0
    assert dominant["dominant_cell_unresolved_count"] == 0
    assert not any(
        resolution[key]
        for key in (
            "physical_boundary_count", "physical_duplicate_count",
            "physical_earlier_count", "physical_later_count",
            "physical_joint_count",
        )
    )

    return {
        "schema": "cm2.gate3.endpoint-descriptor-resolver.v1",
        "status": "CERTIFIED_320_PHYSICALLY_EMPTY_UNRESOLVED_ZERO",
        "provenance": provenance,
        "scope": {
            "parameter_window": [str(S_LOWER), str(S_UPPER)],
            "physical_horizon": "tau_max<3",
            "audited_descriptor_count": 320,
            "audited_descriptor_rows_sha256": EXPECTED_ORIGINAL_SEED_SHA256,
        },
        "corrected_physical_resolution": resolution,
        "legacy_transition_root_audit": transitions,
        "true_dominant_cell_audit": dominant,
        "row_registries": {
            "descriptor_rows_sha256": canonical_digest(descriptor_rows),
            "adaptive_empty_leaf_rows_sha256": canonical_digest(leaf_rows),
            "legacy_transition_root_rows_sha256": canonical_digest(transition_rows),
            "regular_phase_box_rows_sha256": canonical_digest(phase_rows),
            "nonphysical_seam_rows_sha256": canonical_digest(seam_rows),
        },
        "verdict": {
            "empty": 320,
            "physical_boundary": 0,
            "physical_duplicate": 0,
            "physical_earlier": 0,
            "physical_later": 0,
            "physical_joint": 0,
            "unresolved": 0,
            "nonphysical_chart_seam_duplicates": 8,
            "retracted_legacy_physical_vertex_claims": 16,
        },
        "fail_closed_limits": {
            "other_81728_target_target_descriptors_reaudited_here": False,
            "connected_immutable_event_rows": None,
            "global_dq": None,
            "global_scalar_matching": None,
        },
    }


def main() -> None:
    summary = full_summary()
    print("GATE3_320_ENDPOINT_DESCRIPTORS: CERTIFIED_PHYSICALLY_EMPTY")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("GATE3_320_ENDPOINT_UNRESOLVED: 0")
    print("GATE3_CONNECTED_IMMUTABLE_EVENT_ROWS: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
