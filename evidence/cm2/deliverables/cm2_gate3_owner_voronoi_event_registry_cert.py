#!/usr/bin/env python3
"""Gate-3 analytic owner partition and finite event-endpoint registry.

This continuation replaces incoming-root comparisons by the exact projection
order for pairwise disjoint target circles.  It gives a finite Boolean owner
partition of every one of the parent atlas's multi-candidate leaves and an
exhaustive *raw* registry of the analytic tangency sheets and the only extra
target-target boundaries that can split their hit/miss typing.

It deliberately does not call the raw sheets immutable global event rows:
later-target double tangencies can change the miss trace on one connected
physical first-tangency sheet.  A rigorous full-window Arb counterexample is
included.  The remaining endpoint registry is finite and executable, while
global DQ and scalar matching stay fail-closed.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate3_ge_interval_atlas_cert as ge
import cm2_gate3_normal_form_dedup_cert as nf


ctx.prec = 256
Q = Fraction
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT_MANIFEST = HERE / "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
PARENT_SHA256 = "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987"
SOURCES = ("G", "W")
CELLS = base.CELLS
CHARTS = tuple(f"{source}:{cell}" for source in SOURCES for cell in CELLS)
TARGET_BY_ID = {target.target_id: target for target in base.TARGETS}
S_LOWER, S_UPPER = -base.EPS, base.EPS
R = base.RADIUS


# Polynomials below are stored in ascending powers of s.  All coefficients
# are exact Fractions; the source-grazing identity test therefore does not
# infer an algebraic equality from an Arb ball containing zero.
Poly = tuple[Q, ...]


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


def affine_target_center_exact(target_id: str) -> tuple[Poly, Poly]:
    target = TARGET_BY_ID[target_id]
    if target.obstacle == "G":
        return (Q(target.ix), Q(0)), (Q(target.iy), Q(0))
    return (
        (Q(target.ix) + Q(1, 2), Q(1)),
        (Q(target.iy) + Q(1, 2), Q(0)),
    )


def affine_source_center_exact(source: str) -> tuple[Poly, Poly]:
    if source == "G":
        return (Q(0), Q(0)), (Q(0), Q(0))
    return (Q(1, 2), Q(1)), (Q(1, 2), Q(0))


def source_grazing_polynomial(
    source: str,
    target_id: str,
    epsilon_t: int,
    other_id: str,
    epsilon_b: int,
    source_side: int,
) -> Poly:
    """Exact degree-at-most-two equation for a common tangent to graze S.

    Put d=b-a, e=a-c_S, h=eps_B R_B-eps_T R_T, and
    g=eps_T R_T+sigma R_S.  A unit normal n satisfying n.d=h and
    n.e=g exists precisely when

      (h e_y-g d_y)^2 + (g d_x-h e_x)^2
        - det(d,e)^2 = 0.

    Vanishing of every coefficient means the entire common-tangent family
    lies on a source-grazing boundary; it is not an unresolved numerical
    transition.
    """

    ax, ay = affine_target_center_exact(target_id)
    bx, by = affine_target_center_exact(other_id)
    cx, cy = affine_source_center_exact(source)
    dx, dy = poly_sub(bx, ax), poly_sub(by, ay)
    ex, ey = poly_sub(ax, cx), poly_sub(ay, cy)
    target = TARGET_BY_ID[target_id]
    other = TARGET_BY_ID[other_id]
    h = epsilon_b * R[other.obstacle] - epsilon_t * R[target.obstacle]
    g = epsilon_t * R[target.obstacle] + source_side * R[source]
    first = poly_sub(poly_scale(ey, h), poly_scale(dy, g))
    second = poly_sub(poly_scale(dx, g), poly_scale(ex, h))
    determinant = poly_sub(poly_mul(dx, ey), poly_mul(dy, ex))
    return poly_sub(
        poly_add(poly_mul(first, first), poly_mul(second, second)),
        poly_mul(determinant, determinant),
    )


def third_target_tangency_polynomial(
    target_id: str,
    epsilon_t: int,
    other_id: str,
    epsilon_b: int,
    third_id: str,
    epsilon_c: int,
) -> Poly:
    """Exact equation for T/B's common line to graze a third target C."""

    ax, ay = affine_target_center_exact(target_id)
    bx, by = affine_target_center_exact(other_id)
    cx, cy = affine_target_center_exact(third_id)
    dx, dy = poly_sub(bx, ax), poly_sub(by, ay)
    ex, ey = poly_sub(ax, cx), poly_sub(ay, cy)
    target = TARGET_BY_ID[target_id]
    other = TARGET_BY_ID[other_id]
    third = TARGET_BY_ID[third_id]
    h = epsilon_b * R[other.obstacle] - epsilon_t * R[target.obstacle]
    # n.(a-c)=eps_T R_T-eps_C R_C.
    g = epsilon_t * R[target.obstacle] - epsilon_c * R[third.obstacle]
    first = poly_sub(poly_scale(ey, h), poly_scale(dy, g))
    second = poly_sub(poly_scale(dx, g), poly_scale(ex, h))
    determinant = poly_sub(poly_mul(dx, ey), poly_mul(dy, ex))
    return poly_sub(
        poly_add(poly_mul(first, first), poly_mul(second, second)),
        poly_mul(determinant, determinant),
    )


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


def poly_divmod_exact(numerator: Poly, denominator: Poly) -> tuple[Poly, Poly]:
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
    """Count distinct real roots in (lower, upper), with exact arithmetic."""

    value = poly_trim(value)
    assert len(value) >= 2 and lower < upper
    assert poly_eval(value, lower) != 0 and poly_eval(value, upper) != 0
    sequence = [value, poly_derivative(value)]
    while any(sequence[-1]):
        _quotient, remainder = poly_divmod_exact(sequence[-2], sequence[-1])
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


@lru_cache(maxsize=None)
def source_grazing_identity_sides(
    source: str,
    target_id: str,
    epsilon_t: int,
    other_id: str,
    epsilon_b: int,
) -> tuple[int, ...]:
    return tuple(
        source_side
        for source_side in (-1, 1)
        if all(coefficient == 0 for coefficient in source_grazing_polynomial(
            source, target_id, epsilon_t, other_id, epsilon_b, source_side,
        ))
    )


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def update_digest(state: "hashlib._Hash", value: Any) -> None:
    state.update(canonical_json(value).encode("utf-8"))
    state.update(b"\n")


def source_candidate_union(source: str) -> tuple[str, ...]:
    return tuple(sorted(set(itertools.chain.from_iterable(
        base.candidate_ids(f"{source}:{cell}") for cell in CELLS
    ))))


GLOBAL_CANDIDATES = {source: source_candidate_union(source) for source in SOURCES}


def verify_frozen_parent() -> dict[str, Any]:
    assert sha256_path(PARENT_MANIFEST) == PARENT_SHA256
    parent = json.loads(PARENT_MANIFEST.read_text(encoding="utf-8"))
    assert parent["global_totals"]["multi_candidate"] == 95596
    assert parent["global_totals"]["pair_unresolved"] == 3038
    assert parent["global_totals"]["triple_unresolved"] == 10288
    return parent


def verify_projection_order_premises() -> dict[str, Any]:
    """Check strict disjointness for every pair in each global source union.

    If a line intersects target T, its intersection with the closed disk is
    the interval [ell_T-sqrt(Delta_T), ell_T+sqrt(Delta_T)].  Strictly
    disjoint disks give strictly disjoint line intervals.  Their centers are
    ell_T, so the interval order is exactly the ell order.  This elementary
    lemma is proved in the accompanying report; this function exhaustively
    checks its sole geometric premise.
    """

    rows: dict[str, Any] = {}
    for source in SOURCES:
        ids = GLOBAL_CANDIDATES[source]
        digest = hashlib.sha256()
        minimum_margin: Q | None = None
        count = 0
        for left, right in itertools.combinations(ids, 2):
            witness = nf.separation_witness(left, right)
            margin = Q(witness["separation_margin"])
            assert margin > 0
            minimum_margin = margin if minimum_margin is None else min(minimum_margin, margin)
            update_digest(digest, {
                "targets": [left, right],
                "separation_margin": str(margin),
                "line_interval_order": "strict_center_projection_order",
            })
            count += 1
        assert minimum_margin is not None
        rows[source] = {
            "candidate_union_count": len(ids),
            "pair_count": count,
            "minimum_squared_separation_margin": str(minimum_margin),
            "projection_order_rows_sha256": digest.hexdigest(),
        }
    assert rows["G"]["candidate_union_count"] == 76
    assert rows["W"]["candidate_union_count"] == 68
    return rows


OWNER_PREDICATE = (
    "Delta_T>0 and ell_T>0 and for every B!=T: "
    "(Delta_B<0 or ell_B<=0 or ell_T<ell_B)"
)
EVENT_VISIBILITY_PREDICATE = (
    "w_T=epsilon*R_T and ell_T>0 and c_p=u dot n_source>0 and ell_T<3 and "
    "for every B!=T: (Delta_B<0 or ell_B<=0 or ell_T<ell_B)"
)
MISS_OWNER_PREDICATE = (
    "Delta_M>0 and ell_T<ell_M and for every B notin {T,M}: "
    "(Delta_B<0 or ell_B<=ell_T or ell_M<ell_B)"
)


def owner_and_sheet_registries() -> dict[str, Any]:
    chart_owner_rows = []
    chart_sheet_rows = []
    for chart_id in CHARTS:
        for target_id in sorted(base.candidate_ids(chart_id)):
            chart_owner_rows.append({
                "chart_id": chart_id,
                "owner": target_id,
                "predicate": OWNER_PREDICATE,
            })
            for epsilon in (-1, 1):
                chart_sheet_rows.append({
                    "chart_id": chart_id,
                    "target": target_id,
                    "epsilon": epsilon,
                    "tangent_parameterization": (
                        "lambda=sqrt(|d|^2-R_T^2); "
                        "u=(lambda*d-epsilon*R_T*d_perp)/|d|^2"
                    ),
                    "visibility_predicate": EVENT_VISIBILITY_PREDICATE,
                    "hit_trace": "target T at grazing coordinate p_out=epsilon",
                    "miss_owner_predicate": MISS_OWNER_PREDICATE,
                    "partial_p_Delta": "2*epsilon*R_T*ell_T/c_p (nonzero for |p|<1)",
                    "partial_s_Delta": (
                        "2*(1_{T=W}-1_{source=W})*epsilon*R_T*u_y"
                    ),
                })
    assert len(chart_owner_rows) == 448
    assert len(chart_sheet_rows) == 896

    global_owner_rows = []
    global_sheet_rows = []
    for source in SOURCES:
        for target_id in GLOBAL_CANDIDATES[source]:
            global_owner_rows.append({
                "source": source,
                "owner": target_id,
                "predicate": OWNER_PREDICATE,
            })
            for epsilon in (-1, 1):
                global_sheet_rows.append({
                    "source": source,
                    "target": target_id,
                    "epsilon": epsilon,
                    "visibility_predicate": EVENT_VISIBILITY_PREDICATE,
                    "miss_owner_predicate": MISS_OWNER_PREDICATE,
                })
    assert len(global_owner_rows) == 144
    assert len(global_sheet_rows) == 288
    return {
        "chart_owner_predicate_rows": len(chart_owner_rows),
        "chart_owner_rows_sha256": canonical_digest(chart_owner_rows),
        "chart_signed_tangency_sheets": len(chart_sheet_rows),
        "chart_sheet_rows_sha256": canonical_digest(chart_sheet_rows),
        "global_owner_predicate_rows_after_chart_merge": len(global_owner_rows),
        "global_owner_rows_sha256": canonical_digest(global_owner_rows),
        "global_signed_tangency_sheets_after_chart_merge": len(global_sheet_rows),
        "global_sheet_rows_sha256": canonical_digest(global_sheet_rows),
    }


def reflected_target_fast(source: str, axis: str, target_id: str) -> str:
    target = TARGET_BY_ID[target_id]
    obstacle, ix, iy = target.obstacle, target.ix, target.iy
    if axis == "vertical":
        if source == "G":
            ix = -ix if obstacle == "G" else -ix - 1
        else:
            ix = 1 - ix if obstacle == "G" else -ix
    elif axis == "horizontal":
        if source == "G":
            iy = -iy if obstacle == "G" else -iy - 1
        else:
            iy = 1 - iy if obstacle == "G" else -iy
    else:  # pragma: no cover
        raise ValueError(axis)
    return f"{obstacle}[{ix},{iy}]"


def global_symmetry_orbits() -> dict[str, Any]:
    owner_orbits = []
    sheet_orbits = []
    for source in SOURCES:
        ids = set(GLOBAL_CANDIDATES[source])
        seen_owner: set[str] = set()
        for target in sorted(ids):
            if target in seen_owner:
                continue
            vertical = reflected_target_fast(source, "vertical", target)
            horizontal = reflected_target_fast(source, "horizontal", target)
            both = reflected_target_fast(source, "horizontal", vertical)
            orbit = tuple(sorted({target, vertical, horizontal, both}))
            assert set(orbit) <= ids
            seen_owner.update(orbit)
            owner_orbits.append({"source": source, "members": list(orbit)})

        universe = {(target, epsilon) for target in ids for epsilon in (-1, 1)}
        seen_sheet: set[tuple[str, int]] = set()
        for target, epsilon in sorted(universe):
            if (target, epsilon) in seen_sheet:
                continue
            vertical = reflected_target_fast(source, "vertical", target)
            horizontal = reflected_target_fast(source, "horizontal", target)
            both = reflected_target_fast(source, "horizontal", vertical)
            orbit = {
                (target, epsilon),
                (vertical, -epsilon),
                (horizontal, -epsilon),
                (both, epsilon),
            }
            assert orbit <= universe and len(orbit) == 4
            seen_sheet.update(orbit)
            sheet_orbits.append({
                "source": source,
                "members": [[item[0], item[1]] for item in sorted(orbit)],
            })
    assert len(owner_orbits) == 42
    assert len(sheet_orbits) == 72
    return {
        "global_owner_orbits_under_Jx_Jy": len(owner_orbits),
        "owner_orbits_sha256": canonical_digest(owner_orbits),
        "global_signed_sheet_orbits_under_Jx_Jy": len(sheet_orbits),
        "sheet_orbits_sha256": canonical_digest(sheet_orbits),
        "signed_sheet_orbit_size": 4,
    }


def critical_endpoint_registry() -> dict[str, Any]:
    """Build every raw double-tangency and source-grazing descriptor.

    For fixed T/B signed offsets, a common tangent normal has two algebraic
    branches.  Intersecting the resulting line with the source circle and
    choosing the outgoing intersection gives at most one endpoint curve per
    descriptor.  Empty, duplicate, earlier-occluding, later-miss-switching,
    and genuine joint-vertex classifications remain the finite completion
    task.
    """

    double_hash = hashlib.sha256()
    double_count = 0
    grazing_hash = hashlib.sha256()
    grazing_count = 0
    for source in SOURCES:
        ids = GLOBAL_CANDIDATES[source]
        for target in ids:
            for epsilon_t in (-1, 1):
                for other in ids:
                    if other == target:
                        continue
                    for epsilon_b in (-1, 1):
                        for line_branch in (-1, 1):
                            update_digest(double_hash, {
                                "source": source,
                                "target": target,
                                "epsilon_target": epsilon_t,
                                "other": other,
                                "epsilon_other": epsilon_b,
                                "common_tangent_line_branch": line_branch,
                                "equation": (
                                    "n dot (b-a)=epsilon_other*R_B-"
                                    "epsilon_target*R_T; |n|=1; "
                                    "n dot (q-a)=-epsilon_target*R_T"
                                ),
                            })
                            double_count += 1
                for source_grazing_p in (-1, 1):
                    update_digest(grazing_hash, {
                        "source": source,
                        "target": target,
                        "epsilon_target": epsilon_t,
                        "source_grazing_p": source_grazing_p,
                        "equation": "u=p*n_source_perp and w_T=epsilon_target*R_T",
                        "root_upper_bound": 2,
                    })
                    grazing_count += 1
    assert double_count == 82048
    assert grazing_count == 576
    return {
        "raw_target_target_common_tangent_curve_descriptors": double_count,
        "target_target_descriptors_sha256": double_hash.hexdigest(),
        "raw_source_grazing_equations": grazing_count,
        "source_grazing_equations_sha256": grazing_hash.hexdigest(),
        "source_grazing_endpoint_root_upper_bound": 2 * grazing_count,
        "raw_parameter_boundary_sheet_rows": 2 * 288,
        "raw_constant_polarity_split_equations_u_y_zero": 288,
        "tau_zero_physical_endpoints": 0,
        "tau_three_physical_first_endpoints": 0,
        "tau_three_reason": "independent certified physical tau_max<3",
        "total_raw_analytic_endpoint_descriptors": double_count + grazing_count,
    }


def affine_center(target_id: str, s: arb) -> tuple[arb, arb]:
    return base.target_center(TARGET_BY_ID[target_id], s)


def common_tangent_source_geometry(
    source: str,
    target_id: str,
    epsilon_t: int,
    other_id: str,
    epsilon_b: int,
    line_branch: int,
    s0: Q,
    s1: Q,
) -> tuple[str, tuple[arb, ...] | None]:
    """Evaluate one common-tangent/source-intersection curve on an s box."""

    s = base.arb_interval(s0, s1)
    ax, ay = affine_center(target_id, s)
    bx, by = affine_center(other_id, s)
    dx, dy = bx - ax, by - ay
    distance_squared = dx * dx + dy * dy
    rt = base.arbq(R[TARGET_BY_ID[target_id].obstacle])
    rb = base.arbq(R[TARGET_BY_ID[other_id].obstacle])
    h = epsilon_b * rb - epsilon_t * rt
    radical_squared = distance_squared - h * h
    assert bool(radical_squared > 0)
    radical = radical_squared.sqrt()
    nx = (h * dx - line_branch * radical * dy) / distance_squared
    ny = (h * dy + line_branch * radical * dx) / distance_squared
    ux, uy = ny, -nx
    if source == "G":
        cx, cy = arb(0), arb(0)
    else:
        cx, cy = base.arbq(Q(1, 2)) + s, base.arbq(Q(1, 2))
    rs = base.arbq(R[source])
    line_offset = nx * (ax - cx) + ny * (ay - cy) - epsilon_t * rt
    z = line_offset / rs
    z_squared = z * z
    if bool(z_squared > 1):
        return "no_source_intersection", None
    if not bool(z_squared < 1):
        return "source_grazing_transition_unresolved", None
    cp = (1 - z_squared).sqrt()
    source_nx = cp * ux + z * nx
    source_ny = cp * uy + z * ny
    qx = cx + rs * source_nx
    qy = cy + rs * source_ny
    ell_t = ux * (ax - qx) + uy * (ay - qy)
    ell_b = ux * (bx - qx) + uy * (by - qy)
    return "source_intersection", (
        s, qx, qy, ux, uy, ell_t, ell_b, cp, source_nx, source_ny,
    )


def strict_clear_before(
    rows: dict[str, tuple[arb, arb, arb]],
    threshold: arb,
    excluded: set[str],
) -> tuple[bool, bool]:
    """Return (proved clear, proved strict blocker exists)."""

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
    rows: dict[str, tuple[arb, arb, arb]],
    lower: arb,
    upper: arb,
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


def classify_common_tangent_descriptor(
    source: str,
    target_id: str,
    epsilon_t: int,
    other_id: str,
    epsilon_b: int,
    line_branch: int,
    s0: Q = S_LOWER,
    s1: Q = S_UPPER,
) -> str:
    initial, geometry = common_tangent_source_geometry(
        source, target_id, epsilon_t, other_id, epsilon_b,
        line_branch, s0, s1,
    )
    if geometry is None:
        if initial == "source_grazing_transition_unresolved":
            identity_sides = source_grazing_identity_sides(
                source, target_id, epsilon_t, other_id, epsilon_b,
            )
            if identity_sides:
                return "source_grazing_identity_boundary"
        return initial
    s, qx, qy, ux, uy, ell_t, ell_b, _cp, _snx, _sny = geometry
    if bool(ell_t < 0):
        return "target_tangency_behind_source"
    if bool(ell_t > base.arbq(base.TAU_MAX)):
        return "target_tangency_after_tau3"
    if not (bool(ell_t > 0) and bool(ell_t < base.arbq(base.TAU_MAX))):
        return "target_time_endpoint_unresolved"
    if bool(ell_b > ell_t):
        order = "later"
    elif bool(ell_b < ell_t):
        order = "earlier"
    else:
        return "strict_tangent_time_order_unresolved"

    rows = competitor_rows(source, qx, qy, ux, uy, s, target_id)
    if order == "later":
        clear_t, blocker_t = strict_clear_before(rows, ell_t, {other_id})
        if blocker_t:
            return "nonphysical_target_strictly_occluded"
        if not clear_t:
            return "target_visibility_unresolved"
        clear_between, blocker_between = strict_clear_between(
            rows, ell_t, ell_b, {other_id}
        )
        if blocker_between:
            return "physical_target_but_other_is_not_next"
        if not clear_between:
            return "later_miss_order_unresolved"
        return "physical_later_miss_switch_boundary"

    # B is tangent earlier.  It opens/closes visibility of T only if B is
    # itself first and no third target remains before T after B is removed.
    # In particular its contact time must be forward.  Omitting this check
    # would mis-type a common tangent whose B contact lies behind q as a
    # physical occlusion boundary.
    if bool(ell_b < 0):
        return "nonphysical_earlier_tangent_behind_source"
    if not bool(ell_b > 0):
        return "earlier_tangent_time_endpoint_unresolved"
    clear_b, blocker_b = strict_clear_before(rows, ell_b, {other_id})
    if blocker_b:
        return "nonphysical_earlier_tangent_strictly_blocked"
    if not clear_b:
        return "earlier_tangent_visibility_unresolved"
    clear_t_without_b, blocker_t_without_b = strict_clear_before(
        rows, ell_t, {other_id}
    )
    if blocker_t_without_b:
        return "earlier_tangent_physical_but_target_still_occluded"
    if not clear_t_without_b:
        return "target_after_earlier_tangent_unresolved"
    return "physical_earlier_occlusion_boundary"


def common_tangent_descriptors() -> Iterable[tuple[str, str, int, str, int, int]]:
    for source in SOURCES:
        ids = GLOBAL_CANDIDATES[source]
        for target in ids:
            for epsilon_t in (-1, 1):
                for other in ids:
                    if other == target:
                        continue
                    for epsilon_b in (-1, 1):
                        for line_branch in (-1, 1):
                            yield (
                                source, target, epsilon_t, other, epsilon_b,
                                line_branch,
                            )


def classify_all_common_tangent_descriptors() -> dict[str, Any]:
    """Full-window first pass over all 82,048 analytic curve descriptors."""

    counts: dict[str, int] = {}
    unresolved_rows: list[dict[str, Any]] = []
    classified_hash = hashlib.sha256()
    for source, target, epsilon_t, other, epsilon_b, line_branch in (
        common_tangent_descriptors()
    ):
        classification = classify_common_tangent_descriptor(
            source, target, epsilon_t, other, epsilon_b, line_branch,
        )
        descriptor = {
            "source": source,
            "target": target,
            "epsilon_target": epsilon_t,
            "other": other,
            "epsilon_other": epsilon_b,
            "line_branch": line_branch,
        }
        counts[classification] = counts.get(classification, 0) + 1
        update_digest(classified_hash, {
            **descriptor,
            "classification": classification,
        })
        if classification.endswith("_unresolved"):
            unresolved_rows.append(descriptor)
    assert sum(counts.values()) == 82048
    assert counts.get("source_grazing_identity_boundary") == 832
    assert len(unresolved_rows) == 288
    return {
        "classification_counts": dict(sorted(counts.items())),
        "classified_rows_sha256": classified_hash.hexdigest(),
        "unresolved_descriptor_count": len(unresolved_rows),
        "unresolved_descriptors_sha256": canonical_digest(unresolved_rows),
    }


ADAPTIVE_ENDPOINT_DEPTH = 24


def descriptor_dict(
    descriptor: tuple[str, str, int, str, int, int],
) -> dict[str, Any]:
    source, target, epsilon_t, other, epsilon_b, line_branch = descriptor
    return {
        "source": source,
        "target": target,
        "epsilon_target": epsilon_t,
        "other": other,
        "epsilon_other": epsilon_b,
        "line_branch": line_branch,
    }


def strict_third_blockers_on_descriptor_box(
    descriptor: tuple[str, str, int, str, int, int],
    s0: Q,
    s1: Q,
) -> tuple[list[str], dict[str, tuple[arb, arb, arb]], arb]:
    source, target, epsilon_t, other, epsilon_b, line_branch = descriptor
    initial, geometry = common_tangent_source_geometry(
        source, target, epsilon_t, other, epsilon_b, line_branch, s0, s1,
    )
    assert initial == "source_intersection" and geometry is not None
    s, qx, qy, ux, uy, ell_t, _ell_b, *_rest = geometry
    rows = competitor_rows(source, qx, qy, ux, uy, s, target)
    blockers = [
        target_id
        for target_id, (ell, delta, _w) in rows.items()
        if target_id != other
        and bool(ell > 0)
        and bool(ell < ell_t)
        and bool(delta > 0)
    ]
    return blockers, rows, ell_t


def adaptive_endpoint_isolation(
    max_depth: int = ADAPTIVE_ENDPOINT_DEPTH,
) -> dict[str, Any]:
    """Subdivide only the 288 non-identity corrected first-pass descriptors.

    Regular subintervals receive a strict Arb classification.  Genuine
    changes are retained as tiny rational collars, then adjacent unresolved
    leaves of the same descriptor are merged.  This is an interval root
    isolation certificate, not a claim that a collar has been replaced by
    an exact algebraic vertex.
    """

    seeds: list[tuple[str, str, int, str, int, int]] = []
    seed_counts: dict[str, int] = {}
    for descriptor in common_tangent_descriptors():
        classification = classify_common_tangent_descriptor(*descriptor)
        if classification.endswith("_unresolved"):
            seeds.append(descriptor)
            seed_counts[classification] = seed_counts.get(classification, 0) + 1
    assert len(seeds) == 288

    leaves_by_descriptor: dict[
        tuple[str, str, int, str, int, int], list[tuple[Q, Q, int, str]]
    ] = {}
    regular_counts: dict[str, int] = {}
    regular_digest = hashlib.sha256()
    raw_unresolved_count = 0
    for descriptor in seeds:
        pending = [(S_LOWER, S_UPPER, 0)]
        leaves: list[tuple[Q, Q, int, str]] = []
        while pending:
            s0, s1, depth = pending.pop()
            classification = classify_common_tangent_descriptor(
                *descriptor, s0, s1,
            )
            if classification.endswith("_unresolved") and depth < max_depth:
                middle = (s0 + s1) / 2
                pending.append((middle, s1, depth + 1))
                pending.append((s0, middle, depth + 1))
                continue
            leaves.append((s0, s1, depth, classification))
            if classification.endswith("_unresolved"):
                raw_unresolved_count += 1
            else:
                regular_counts[classification] = (
                    regular_counts.get(classification, 0) + 1
                )
                update_digest(regular_digest, {
                    **descriptor_dict(descriptor),
                    "s": [str(s0), str(s1)],
                    "depth": depth,
                    "classification": classification,
                })
        leaves.sort(key=lambda row: row[0])
        assert leaves[0][0] == S_LOWER and leaves[-1][1] == S_UPPER
        for left, right in zip(leaves, leaves[1:]):
            assert left[1] == right[0]
        leaves_by_descriptor[descriptor] = leaves

    collars: list[dict[str, Any]] = []
    transition_counts: dict[str, int] = {}
    descriptors_with_collars = 0
    for descriptor, leaves in leaves_by_descriptor.items():
        found_for_descriptor = False
        index = 0
        while index < len(leaves):
            if not leaves[index][3].endswith("_unresolved"):
                index += 1
                continue
            found_for_descriptor = True
            start_index = index
            s0, s1, _depth, first_kind = leaves[index]
            unresolved_kinds = {first_kind}
            index += 1
            while (
                index < len(leaves)
                and leaves[index][3].endswith("_unresolved")
                and leaves[index][0] == s1
            ):
                s1 = leaves[index][1]
                unresolved_kinds.add(leaves[index][3])
                index += 1
            left_kind = leaves[start_index - 1][3] if start_index else None
            right_kind = leaves[index][3] if index < len(leaves) else None
            signature = f"{left_kind}|{','.join(sorted(unresolved_kinds))}|{right_kind}"
            transition_counts[signature] = transition_counts.get(signature, 0) + 1
            row: dict[str, Any] = {
                **descriptor_dict(descriptor),
                "s_collar": [str(s0), str(s1)],
                "width": str(s1 - s0),
                "unresolved_kinds": sorted(unresolved_kinds),
                "left_regular_classification": left_kind,
                "right_regular_classification": right_kind,
            }

            physical_kind = "physical_earlier_occlusion_boundary"
            blocked_kind = "earlier_tangent_physical_but_target_still_occluded"
            if {left_kind, right_kind} == {physical_kind, blocked_kind}:
                blocked_leaf = (
                    leaves[start_index - 1]
                    if left_kind == blocked_kind
                    else leaves[index]
                )
                physical_leaf = (
                    leaves[start_index - 1]
                    if left_kind == physical_kind
                    else leaves[index]
                )
                blockers, blocked_rows, _blocked_ell_t = (
                    strict_third_blockers_on_descriptor_box(
                        descriptor, blocked_leaf[0], blocked_leaf[1],
                    )
                )
                assert len(blockers) == 1
                third = blockers[0]
                physical_blockers, physical_rows, physical_ell_t = (
                    strict_third_blockers_on_descriptor_box(
                        descriptor, physical_leaf[0], physical_leaf[1],
                    )
                )
                assert not physical_blockers
                ell, delta, _w = physical_rows[third]
                if bool(delta < 0):
                    clear_reason = "third_target_strict_miss"
                elif bool(ell < 0):
                    clear_reason = "third_target_strictly_behind"
                elif bool(ell > physical_ell_t):
                    clear_reason = "third_target_strictly_after_target"
                else:  # pragma: no cover - fail closed on an untyped side.
                    raise AssertionError((descriptor, third, physical_leaf))
                blocked_w = blocked_rows[third][2]
                if bool(blocked_w > 0):
                    epsilon_c = 1
                elif bool(blocked_w < 0):
                    epsilon_c = -1
                else:  # pragma: no cover
                    raise AssertionError((descriptor, third, blocked_w))
                radius_c = base.arbq(R[TARGET_BY_ID[third].obstacle])
                assert bool(epsilon_c * blocked_w - radius_c < 0)
                assert bool(epsilon_c * physical_rows[third][2] - radius_c > 0)
                polynomial = third_target_tangency_polynomial(
                    descriptor[1], descriptor[2], descriptor[3],
                    descriptor[4], third, epsilon_c,
                )
                assert sturm_root_count(polynomial, s0, s1) == 1
                row.update({
                    "endpoint_type": "exact_third_target_tangency_vertex",
                    "third_target": third,
                    "epsilon_third": epsilon_c,
                    "physical_side_clear_reason": clear_reason,
                    "exact_polynomial_coefficients_ascending": [
                        str(coefficient) for coefficient in polynomial
                    ],
                    "sturm_root_count_in_collar": 1,
                    "fixed_branch_signed_gap_changes": "positive_to_negative_or_reverse",
                })
            elif {
                left_kind, right_kind,
            } == {
                "target_tangency_after_tau3",
                "earlier_tangent_physical_but_target_still_occluded",
            }:
                initial, geometry = common_tangent_source_geometry(
                    *descriptor, s0, s1,
                )
                assert initial == "source_intersection" and geometry is not None
                _s, _qx, _qy, _ux, _uy, ell_t, ell_b, *_rest = geometry
                assert bool(ell_b > 0) and bool(ell_b < ell_t)
                row.update({
                    "endpoint_type": "nonphysical_tau_three_crossing_collar",
                    "uniform_nonphysical_witness": "0<ell_other<ell_target",
                })
            else:  # pragma: no cover - any new type must be explicitly audited.
                raise AssertionError((descriptor, left_kind, right_kind))
            collars.append(row)
        if found_for_descriptor:
            descriptors_with_collars += 1

    collars.sort(key=lambda row: canonical_json(row))
    collar_widths = [Q(row["width"]) for row in collars]
    assert len(collars) == 4 and descriptors_with_collars == 4
    assert sum(
        row["endpoint_type"] == "exact_third_target_tangency_vertex"
        for row in collars
    ) == 0
    assert sum(
        row["endpoint_type"] == "nonphysical_tau_three_crossing_collar"
        for row in collars
    ) == 4
    grid_width = (S_UPPER - S_LOWER) / (2 ** max_depth)
    assert max(collar_widths) <= 22 * grid_width

    def collar_key(row: dict[str, Any]) -> tuple[Any, ...]:
        return (
            row["source"], row["target"], row["epsilon_target"],
            row["other"], row["epsilon_other"], row["line_branch"],
            row["endpoint_type"], row.get("third_target"),
            row.get("epsilon_third"), row["s_collar"][0],
            row["s_collar"][1],
        )

    def reflect_collar_key(value: tuple[Any, ...], axis: str) -> tuple[Any, ...]:
        (
            source, target, epsilon_t, other, epsilon_b, line_branch,
            endpoint_type, third, epsilon_c, s0, s1,
        ) = value
        reflected_third = (
            reflected_target_fast(source, axis, third) if third is not None else None
        )
        if axis == "vertical":
            reflected_s0, reflected_s1 = str(-Q(s1)), str(-Q(s0))
        else:
            reflected_s0, reflected_s1 = s0, s1
        return (
            source,
            reflected_target_fast(source, axis, target), -epsilon_t,
            reflected_target_fast(source, axis, other), -epsilon_b,
            line_branch, endpoint_type, reflected_third,
            -epsilon_c if epsilon_c is not None else None,
            reflected_s0, reflected_s1,
        )

    collar_universe = {collar_key(row) for row in collars}

    def jsonable_collar_key(value: tuple[Any, ...]) -> list[Any]:
        """Canonical JSON-safe form of a collar key.

        The last two entries are exact Fractions.  Keeping the working keys
        as tuples is useful for set/orbit checks, but feeding those Fractions
        directly to json.dumps is a hard error rather than a certificate.
        """

        return [
            str(item) if isinstance(item, Q) else item
            for item in value
        ]

    seen_collars: set[tuple[Any, ...]] = set()
    collar_orbits: list[list[tuple[Any, ...]]] = []
    for key in sorted(collar_universe, key=lambda value: canonical_json(
        jsonable_collar_key(value)
    )):
        if key in seen_collars:
            continue
        vertical = reflect_collar_key(key, "vertical")
        horizontal = reflect_collar_key(key, "horizontal")
        both = reflect_collar_key(vertical, "horizontal")
        orbit = {key, vertical, horizontal, both}
        assert len(orbit) == 4 and orbit <= collar_universe
        seen_collars.update(orbit)
        collar_orbits.append(sorted(
            orbit,
            key=lambda value: canonical_json(jsonable_collar_key(value)),
        ))
    assert len(collar_orbits) == 1 and seen_collars == collar_universe
    collar_orbits_json = [
        [jsonable_collar_key(key) for key in orbit]
        for orbit in collar_orbits
    ]
    physical_orbits = [
        orbit for orbit in collar_orbits
        if orbit[0][6] == "exact_third_target_tangency_vertex"
    ]
    nonphysical_orbits = [
        orbit for orbit in collar_orbits
        if orbit[0][6] == "nonphysical_tau_three_crossing_collar"
    ]
    assert len(physical_orbits) == 0
    assert len(nonphysical_orbits) == 1
    return {
        "adaptive_depth": max_depth,
        "initial_unresolved_descriptor_count": len(seeds),
        "initial_unresolved_classification_counts": dict(sorted(seed_counts.items())),
        "descriptors_fully_resolved_after_subdivision": len(seeds) - descriptors_with_collars,
        "descriptors_with_isolated_transition_collars": descriptors_with_collars,
        "regular_subinterval_leaf_count": sum(regular_counts.values()),
        "regular_subinterval_classification_counts": dict(sorted(regular_counts.items())),
        "regular_subinterval_rows_sha256": regular_digest.hexdigest(),
        "raw_depth_limit_unresolved_leaf_count": raw_unresolved_count,
        "merged_transition_collar_count": len(collars),
        "merged_transition_classification_counts": dict(sorted(transition_counts.items())),
        "exact_third_target_tangency_vertices": 0,
        "nonphysical_tau_three_crossing_collars": 4,
        "dyadic_grid_width": str(grid_width),
        "maximum_merged_collar_width": str(max(collar_widths)),
        "maximum_collar_grid_widths": str(max(collar_widths) / grid_width),
        "merged_transition_collars_sha256": canonical_digest(collars),
        "transition_collar_orbits_under_Jx_Jy": len(collar_orbits),
        "transition_collar_orbit_size": 4,
        "transition_collar_orbits_sha256": canonical_digest(collar_orbits_json),
        "physical_transition_vertex_orbits_under_Jx_Jy": len(physical_orbits),
        "nonphysical_tau_three_orbits_under_Jx_Jy": len(nonphysical_orbits),
        "all_transition_collars_exactly_typed": True,
        "numerically_unresolved_transition_collar_count": 0,
    }


def normal_geometry(chart_id: str, t0: Q, t1: Q, s0: Q, s1: Q) -> tuple[arb, ...]:
    source, cell = chart_id.split(":")
    t = base.arb_interval(t0, t1)
    s = base.arb_interval(s0, s1)
    radical = ge.sqrt_one_minus_square(t0, t1)
    if cell == "E":
        nx, ny = radical, t
    elif cell == "W":
        nx, ny = -radical, t
    elif cell == "N":
        nx, ny = t, radical
    elif cell == "S":
        nx, ny = t, -radical
    else:  # pragma: no cover
        raise ValueError(cell)
    if source == "G":
        cx, cy = arb(0), arb(0)
    else:
        cx, cy = base.arbq(Q(1, 2)) + s, base.arbq(Q(1, 2))
    qx = cx + base.arbq(R[source]) * nx
    qy = cy + base.arbq(R[source]) * ny
    return nx, ny, qx, qy, s


def tangent_geometry(
    chart_id: str, t0: Q, t1: Q, s0: Q, s1: Q,
    target_id: str, epsilon: int,
) -> tuple[arb, ...]:
    nx, ny, qx, qy, s = normal_geometry(chart_id, t0, t1, s0, s1)
    target = TARGET_BY_ID[target_id]
    ax, ay = base.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    distance_squared = dx * dx + dy * dy
    radius = base.arbq(R[target.obstacle])
    assert bool(distance_squared - radius * radius > 0)
    ell = (distance_squared - radius * radius).sqrt()
    # d_perp=(-dy,dx): u=(ell*d-epsilon*R*d_perp)/|d|^2.
    ux = (ell * dx + epsilon * radius * dy) / distance_squared
    uy = (ell * dy - epsilon * radius * dx) / distance_squared
    cp = ux * nx + uy * ny
    p = -ux * ny + uy * nx
    return nx, ny, qx, qy, ux, uy, ell, cp, p, s


def competitor_rows(
    source: str, qx: arb, qy: arb, ux: arb, uy: arb, s: arb,
    excluded: str,
) -> dict[str, tuple[arb, arb, arb]]:
    rows: dict[str, tuple[arb, arb, arb]] = {}
    for target_id in GLOBAL_CANDIDATES[source]:
        if target_id == excluded:
            continue
        target = TARGET_BY_ID[target_id]
        ax, ay = base.target_center(target, s)
        dx, dy = ax - qx, ay - qy
        ell = ux * dx + uy * dy
        w = -uy * dx + ux * dy
        radius = base.arbq(R[target.obstacle])
        delta = radius * radius - w * w
        rows[target_id] = (ell, delta, w)
    return rows


def certify_visible_box(
    chart_id: str, t0: Q, t1: Q, target_id: str, epsilon: int,
) -> tuple[dict[str, tuple[arb, arb, arb]], tuple[arb, ...]]:
    geom = tangent_geometry(chart_id, t0, t1, S_LOWER, S_UPPER, target_id, epsilon)
    nx, ny, qx, qy, ux, uy, ell_t, cp, p, s = geom
    del nx, ny
    assert bool(cp > 0) and bool(ell_t > 0) and bool(ell_t < base.arbq(base.TAU_MAX))
    assert bool(p > -1) and bool(p < 1)
    source = chart_id.split(":")[0]
    rows = competitor_rows(source, qx, qy, ux, uy, s, target_id)
    for other_id, (ell_b, delta_b, _w_b) in rows.items():
        assert (
            bool(ell_b < 0)
            or bool(ell_b > ell_t)
            or bool(delta_b < 0)
        ), (chart_id, target_id, other_id, t0, t1)
    return rows, geom


def certify_miss_seed(
    chart_id: str, t0: Q, t1: Q, target_id: str, epsilon: int,
    miss_target: str,
) -> dict[str, Any]:
    rows, geom = certify_visible_box(chart_id, t0, t1, target_id, epsilon)
    _nx, _ny, _qx, _qy, _ux, uy, ell_t, cp, p, _s = geom
    ell_m, delta_m, _w_m = rows[miss_target]
    assert bool(ell_m > ell_t) and bool(delta_m > 0)
    root_m = ell_m - delta_m.sqrt()
    assert bool(root_m > ell_t)
    for other_id, (ell_b, delta_b, _w_b) in rows.items():
        if other_id == miss_target:
            continue
        assert (
            bool(ell_b < 0)
            or bool(delta_b < 0)
            or bool(ell_b > ell_m)
        ), (chart_id, target_id, miss_target, other_id)

    source = chart_id.split(":")[0]
    target_obstacle = TARGET_BY_ID[target_id].obstacle
    eta = int(target_obstacle == "W") - int(source == "W")
    if eta == 0:
        coarea_polarity = 0
        signed_p_coarea = arb(0)
    else:
        signed_p_coarea = eta * epsilon * cp * uy / ell_t
        assert bool(signed_p_coarea > 0) or bool(signed_p_coarea < 0)
        coarea_polarity = 1 if bool(signed_p_coarea > 0) else -1
    return {
        "chart_id": chart_id,
        "t": [str(t0), str(t1)],
        "s": [str(S_LOWER), str(S_UPPER)],
        "target": target_id,
        "epsilon": epsilon,
        "miss_owner": miss_target,
        "tangent_p_interval": str(p),
        "tangent_flight_interval": str(ell_t),
        "miss_root_interval": str(root_m),
        "hit_trace_grazing_p": epsilon,
        "parameter_coarea_polarity": coarea_polarity,
        "signed_p_coarea_interval": str(signed_p_coarea),
    }


def miss_owner_nonconstancy_counterexample() -> dict[str, Any]:
    """Two full-window rows on one connected physical T-sheet.

    The path t in [0,3221/5000] is covered by visible boxes, so W[0,0]
    remains the physical first tangency throughout.  Its miss owner is
    G[1,1] near the first endpoint and G[2,1] near the second.  Therefore a
    later-target double tangency, not equal first roots, must split the miss
    trace registry.
    """

    target, epsilon = "W[0,0]", 1
    end = Q(3221, 5000)
    seed_a = certify_miss_seed(
        "G:E", Q(0), Q(1, 100000), target, epsilon, "G[1,1]"
    )
    seed_b = certify_miss_seed(
        "G:E", end - Q(1, 100000), end, target, epsilon, "G[2,1]"
    )

    pending = [(Q(0), end, 0, "")]
    leaves: list[dict[str, Any]] = []
    while pending:
        t0, t1, depth, path = pending.pop()
        try:
            certify_visible_box("G:E", t0, t1, target, epsilon)
        except AssertionError:
            assert depth < 12
            middle = (t0 + t1) / 2
            pending.append((middle, t1, depth + 1, path + "1"))
            pending.append((t0, middle, depth + 1, path + "0"))
        else:
            leaves.append({
                "path": path,
                "t": [str(t0), str(t1)],
                "depth": depth,
            })
    leaves.sort(key=lambda row: Q(row["t"][0]))
    assert leaves[0]["t"][0] == "0" and leaves[-1]["t"][1] == str(end)
    for left, right in zip(leaves, leaves[1:]):
        assert left["t"][1] == right["t"][0]
    assert len(leaves) == 10 and max(row["depth"] for row in leaves) == 4
    return {
        "sheet": {"source": "G", "target": target, "epsilon": epsilon},
        "full_s_window": [str(S_LOWER), str(S_UPPER)],
        "connected_visible_path_t": ["0", str(end)],
        "visible_path_leaf_count": len(leaves),
        "visible_path_max_depth": max(row["depth"] for row in leaves),
        "visible_path_rows_sha256": canonical_digest(leaves),
        "first_seed": seed_a,
        "second_seed": seed_b,
        "conclusion": (
            "miss owner changes on one connected physical first-tangency "
            "sheet; target-target double tangencies are mandatory endpoints"
        ),
    }


def full_summary() -> dict[str, Any]:
    parent = verify_frozen_parent()
    projection = verify_projection_order_premises()
    registries = owner_and_sheet_registries()
    symmetries = global_symmetry_orbits()
    endpoints = critical_endpoint_registry()
    endpoint_first_pass = classify_all_common_tangent_descriptors()
    endpoint_isolation = adaptive_endpoint_isolation()
    counterexample = miss_owner_nonconstancy_counterexample()
    return {
        "parent_manifest_sha256": PARENT_SHA256,
        "parent_multi_candidate_leaves": parent["global_totals"]["multi_candidate"],
        "projection_order_theorem": {
            "statement": (
                "for forward-intersected pairwise disjoint disks, incoming-root "
                "order equals center-projection ell order"
            ),
            "source_unions": projection,
        },
        "owner_partition": {
            "status": "CERTIFIED_FINITE_BOOLEAN_SINGLE_OWNER_PARTITION",
            "regular_owner_predicate": OWNER_PREDICATE,
            "tangency_visibility_predicate": EVENT_VISIBILITY_PREDICATE,
            "miss_owner_predicate": MISS_OWNER_PREDICATE,
            "coverage_reason": "complete candidate lists plus certified physical tau_max<3",
            "uniqueness_reason": "strict disk separation and projection-order theorem",
            **registries,
        },
        "symmetry_deduplication": symmetries,
        "critical_endpoint_registry": {
            **endpoints,
            "full_window_first_pass": endpoint_first_pass,
            "adaptive_interval_isolation": endpoint_isolation,
            "retracted_pre_forward_time_audit": {
                "status": "RETRACTED_BY_MISSING_ELL_OTHER_POSITIVITY_CHECK",
                "old_unresolved_descriptor_count": 320,
                "old_unresolved_descriptors_sha256": (
                    "c04fc55676bcb0341c24f8ae5f50116913bb9b70b18ca901873c7e1ff15238a2"
                ),
                "old_claimed_third_target_vertex_count": 16,
                "corrected_classification": (
                    "all sixteen contacts have ell_other<0 and are not "
                    "forward physical boundaries"
                ),
            },
        },
        "miss_owner_nonconstancy": counterexample,
        "completion": {
            "all_95596_multi_leaves_have_exact_owner_predicate_partition": True,
            "raw_signed_tangency_sheet_registry": True,
            "target_target_endpoint_descriptor_registry": True,
            "finite_interval_classification_of_all_target_target_descriptors": True,
            "source_grazing_identity_boundaries_exactly_typed": True,
            "four_residual_transition_collars_isolated": True,
            "retracted_sixteen_physical_transition_vertex_claim": True,
            "corrected_physical_transition_vertex_count": 0,
            "nonphysical_tau_three_transition_collars_uniformly_discarded": True,
            "all_target_target_descriptors_interval_typed": True,
            "duplicate_endpoint_quotient_across_distinct_descriptors": None,
            "connected_visible_component_registry": None,
            "constant_miss_trace_subrows": None,
            "constant_parameter_polarity_subrows": None,
            "immutable_global_event_rows": None,
            "global_dq": None,
            "global_scalar_matching": None,
        },
    }


def main() -> None:
    summary = full_summary()
    print("GATE3_ANALYTIC_SINGLE_OWNER_PARTITION: CERTIFIED")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("GATE3_CONNECTED_IMMUTABLE_EVENT_ROWS: NOT_CERTIFIED")
    print("GATE3_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
