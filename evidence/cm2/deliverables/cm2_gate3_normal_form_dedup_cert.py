#!/usr/bin/env python3
"""Exact Gate-3 pair/triple normal forms and one local event-row orbit.

The frozen eight-cell interval atlas records conservative co-occurrence
collars.  Such a collar is not itself a multiple physical event.  This
certificate separates the two notions.

* Every distinct target-circle pair in every candidate registry is proved
  disjoint on the whole parameter window.  Equality of two first roots would
  put one Euclidean point on both circles and is therefore impossible.
* If one oriented line is tangent to two distinct targets, its two tangency
  times are strictly different.  Thus at most the earlier contact can be a
  physical first tangency.  Triples reduce pairwise.
* The exact Jx/Jy transports reduce the 3038/10288 frozen unresolved rows to
  1519/5144 representative conservative rows.
* A positive-width G:E -> W[0,0] switching chart and its complete Jx orbit
  are certified, including the miss target, hit trace, geometric polarity,
  parameter-coarea sign, and exact reflection typing.

This does not resolve the 95,596 multi-candidate boxes into a global event
partition, assemble the global DQ, or prove scalar-current matching.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate4_explicit_tangency_cert as exact_seed


ctx.prec = 192
Q = Fraction
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT_MANIFEST = HERE / "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
PARENT_MANIFEST_SHA256 = "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987"

CHARTS = ("G:E", "G:W", "G:N", "G:S", "W:E", "W:W", "W:N", "W:S")
REFLECTIONS = {
    "G:E": ("G:W", "vertical"),
    "G:N": ("G:S", "horizontal"),
    "W:E": ("W:W", "vertical"),
    "W:N": ("W:S", "horizontal"),
}
R = base.RADIUS
EPS = base.EPS
TARGET_BY_ID = {target.target_id: target for target in base.TARGETS}
SEPARATION_CACHE: dict[tuple[str, str], dict[str, str]] = {}


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def fraction_min_square(a: Q, b: Q) -> Q:
    """Return min_{|s|<=EPS} (a+b*s)^2 exactly."""

    values = (a - b * EPS, a + b * EPS)
    if min(values) <= 0 <= max(values):
        return Q(0)
    return min(value * value for value in values)


def target_center_affine(target_id: str) -> tuple[Q, int, Q]:
    target = TARGET_BY_ID[target_id]
    if target.obstacle == "G":
        return Q(target.ix), 0, Q(target.iy)
    return Q(target.ix) + Q(1, 2), 1, Q(target.iy) + Q(1, 2)


def separation_witness(left_id: str, right_id: str) -> dict[str, str]:
    """Exact uniform circle-separation and resultant witness."""

    assert left_id != right_id
    key = tuple(sorted((left_id, right_id)))
    cached = SEPARATION_CACHE.get(key)
    if cached is not None:
        return cached
    left = TARGET_BY_ID[left_id]
    right = TARGET_BY_ID[right_id]
    ax, bx, ay = target_center_affine(left_id)
    cx, dx, cy = target_center_affine(right_id)
    x0, x1, y0 = cx - ax, dx - bx, cy - ay
    distance_squared_lower = fraction_min_square(x0, x1) + y0 * y0
    radius_sum = R[left.obstacle] + R[right.obstacle]
    separation_margin = distance_squared_lower - radius_sum * radius_sum
    assert separation_margin > 0

    # Subtracting the two circle equations gives the linear radical-axis
    # equation.  Its substitution into either circle has discriminant
    #   -(D^2-(Ra+Rb)^2)(D^2-(Ra-Rb)^2).
    # The first factor is strictly positive by the witness above, so no
    # common point, hence no equal first root, exists.
    radius_difference = abs(R[left.obstacle] - R[right.obstacle])
    assert distance_squared_lower > radius_difference * radius_difference

    # For a line tangent with signed offsets eps_i R_i, the squared
    # separation of the two along-line projections is
    # D^2-(eps_l R_l-eps_r R_r)^2.  Its worst case is bounded by (Rl+Rr)^2.
    common_line_time_gap_squared_lower = separation_margin
    assert common_line_time_gap_squared_lower > 0
    result = {
        "distance_squared_lower": str(distance_squared_lower),
        "radius_sum_squared": str(radius_sum * radius_sum),
        "separation_margin": str(separation_margin),
        "circle_intersection_resultant": "strictly_negative",
        "common_tangent_time_gap_squared_lower": str(common_line_time_gap_squared_lower),
    }
    SEPARATION_CACHE[key] = result
    return result


def update_row_digest(state: "hashlib._Hash", row: dict[str, Any]) -> None:
    state.update(canonical_json(row).encode("utf-8"))
    state.update(b"\n")


def chart_normal_form_summary(chart_id: str) -> dict[str, Any]:
    candidate_ids = sorted(base.candidate_ids(chart_id))
    pair_witness: dict[tuple[str, str], dict[str, str]] = {}
    pair_hash = hashlib.sha256()
    minimum_margin: Q | None = None
    pair_count = 0
    for pair in itertools.combinations(candidate_ids, 2):
        witness = separation_witness(*pair)
        pair_witness[pair] = witness
        margin = Q(witness["separation_margin"])
        minimum_margin = margin if minimum_margin is None else min(minimum_margin, margin)
        update_row_digest(
            pair_hash,
            {
                "target_ids": list(pair),
                "normal_form": "distinct_disjoint_targets_no_simultaneous_first_occurrence",
                "first_root_equality": "empty_by_circle_intersection_resultant",
                "common_line_tangency": "strictly_time_ordered_if_present",
                "witness": witness,
            },
        )
        pair_count += 1

    triple_hash = hashlib.sha256()
    triple_count = 0
    for triple in itertools.combinations(candidate_ids, 3):
        pairs = tuple(itertools.combinations(triple, 2))
        margin = min(Q(pair_witness[tuple(sorted(pair))]["separation_margin"]) for pair in pairs)
        update_row_digest(
            triple_hash,
            {
                "target_ids": list(triple),
                "normal_form": "pairwise_disjoint_targets_no_simultaneous_first_occurrence",
                "reduction": "every alleged triple contains an impossible equal-first-root pair",
                "minimum_pair_separation_margin": str(margin),
            },
        )
        triple_count += 1

    assert pair_count == len(candidate_ids) * (len(candidate_ids) - 1) // 2
    assert triple_count == len(candidate_ids) * (len(candidate_ids) - 1) * (len(candidate_ids) - 2) // 6
    assert minimum_margin is not None and minimum_margin > 0
    return {
        "candidate_count": len(candidate_ids),
        "pair_count": pair_count,
        "pair_normal_form_rows_sha256": pair_hash.hexdigest(),
        "triple_count": triple_count,
        "triple_normal_form_rows_sha256": triple_hash.hexdigest(),
        "minimum_squared_separation_margin": str(minimum_margin),
    }


def mapped_combination(source_chart: str, axis: str, values: Iterable[str]) -> tuple[str, ...]:
    source = source_chart.split(":")[0]
    mapped: list[str] = []
    for value in values:
        target = TARGET_BY_ID[value]
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
        else:  # pragma: no cover - fixed registry
            raise ValueError(axis)
        mapped.append(f"{obstacle}[{ix},{iy}]")
    return tuple(sorted(mapped))


def reflection_combination_digest(source_chart: str, order: int) -> tuple[str, int]:
    partner, axis = REFLECTIONS[source_chart]
    source_rows = list(itertools.combinations(sorted(base.candidate_ids(source_chart)), order))
    partner_rows = set(itertools.combinations(sorted(base.candidate_ids(partner)), order))
    mapped_rows = [mapped_combination(source_chart, axis, row) for row in source_rows]
    assert len(mapped_rows) == len(set(mapped_rows))
    assert set(mapped_rows) == partner_rows
    # Uniform separation witnesses are invariant under the exact isometry
    # and the symmetric s interval.
    for old, new in zip(source_rows, mapped_rows):
        old_margin = min(Q(separation_witness(*pair)["separation_margin"]) for pair in itertools.combinations(old, 2))
        new_margin = min(Q(separation_witness(*pair)["separation_margin"]) for pair in itertools.combinations(new, 2))
        assert old_margin == new_margin
    return canonical_digest(
        [{"source_targets": list(old), "reflected_targets": list(new)} for old, new in zip(source_rows, mapped_rows)]
    ), len(source_rows)


def load_parent_manifest() -> dict[str, Any]:
    assert sha256_path(PARENT_MANIFEST) == PARENT_MANIFEST_SHA256
    data = json.loads(PARENT_MANIFEST.read_text(encoding="utf-8"))
    assert data["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
    assert data["global_totals"]["pair_unresolved"] == 3038
    assert data["global_totals"]["triple_unresolved"] == 10288
    for row in data["provenance"]:
        path = ROOT / row["path"]
        assert path.is_file() and sha256_path(path) == row["sha256"]
    return data


def arb_abs(value: arb) -> arb:
    if bool(value > 0):
        return value
    if bool(value < 0):
        return -value
    raise AssertionError(f"sign unresolved: {value}")


def certify_local_event(
    chart_id: str,
    p0: Q,
    p1: Q,
    target_id: str,
    miss_target_id: str,
    expected_w_sign: int,
) -> dict[str, Any]:
    box = atlas.AtlasBox(
        -Q(1, 10**6), Q(1, 10**6), p0, p1,
        -Q(1, 10**6), Q(1, 10**6), 0, "local.event.orbit",
    )
    rows = atlas.records(chart_id, box)
    target = next(row for row in rows if row.target_id == target_id)
    miss = next(row for row in rows if row.target_id == miss_target_id)
    assert atlas.physical_tangency_graph(chart_id, box, target, rows)
    assert target.classification == "unresolved_discriminant"
    assert miss.classification == "strict_future_root" and miss.near is not None
    assert bool(target.ell > base.arbq(Q(49, 100)))
    assert bool(target.ell < miss.near)
    assert bool(miss.near - target.ell > base.arbq(Q(3, 10)))
    assert bool(miss.near > base.arbq(Q(4, 5))) and bool(miss.near < base.arbq(Q(9, 10)))

    # Once the tangency target is omitted (the miss side), miss_target is
    # rigorously the first remaining positive incoming root on the whole box.
    for other in rows:
        if other.target_id in {target_id, miss_target_id}:
            continue
        if other.classification in {"no_real_intersection", "intersection_behind"}:
            continue
        lower = atlas.ge.earliest_possible_root_lower(other)
        assert lower is not None and bool(miss.near < lower), (chart_id, other.target_id)

    qx, qy, ux, uy, _s, cp = atlas.geometry(chart_id, box)
    del qx, qy
    partial_p = 2 * target.transverse * target.ell / cp
    source = chart_id.split(":")[0]
    target_obstacle = TARGET_BY_ID[target_id].obstacle
    eta = int(target_obstacle == "W") - int(source == "W")
    partial_s = 2 * eta * target.transverse * uy
    assert eta == 1
    assert (1 if bool(target.transverse > 0) else -1) == expected_w_sign
    assert (1 if bool(partial_p > 0) else -1) == expected_w_sign
    assert (1 if bool(partial_s > 0) else -1) == expected_w_sign
    assert bool(arb_abs(partial_p) > base.arbq(Q(7, 25)))
    assert bool(arb_abs(partial_s) > base.arbq(Q(1, 4)))
    signed_p_coarea = partial_s / arb_abs(partial_p)
    graph_velocity = -partial_s / partial_p
    assert (1 if bool(signed_p_coarea > 0) else -1) == expected_w_sign
    assert bool(arb_abs(signed_p_coarea) > base.arbq(Q(4, 5)))
    assert bool(arb_abs(signed_p_coarea) < base.arbq(Q(1)))
    assert bool(graph_velocity < -base.arbq(Q(4, 5)))
    assert bool(graph_velocity > -base.arbq(Q(1)))

    lower_face = atlas.root_at_fixed_p(chart_id, box, target_id, p0).discriminant
    upper_face = atlas.root_at_fixed_p(chart_id, box, target_id, p1).discriminant
    if expected_w_sign > 0:
        assert bool(lower_face < 0) and bool(upper_face > 0)
        hit_side = "p>p_star(t,s)"
    else:
        assert bool(lower_face > 0) and bool(upper_face < 0)
        hit_side = "p<p_star(t,s)"

    target_radius = R[target_obstacle]
    assert bool(target.ell - base.arbq(target_radius) > 0)
    return {
        "chart_id": chart_id,
        "box": {
            "t": [str(box.t0), str(box.t1)],
            "p": [str(box.p0), str(box.p1)],
            "s": [str(box.s0), str(box.s1)],
        },
        "owner": target_id,
        "event_equation": "Delta_T=R_T^2-(u_perp dot (a_T-q))^2=0",
        "root": "tau_T=ell_T (positive first tangency)",
        "hit_side": hit_side,
        "geometric_p_polarity": expected_w_sign,
        "parameter_coarea_polarity": expected_w_sign,
        "p_coarea_coefficient": "partial_s Delta_T/abs(partial_p Delta_T)",
        "p_coarea_interval": str(signed_p_coarea),
        "graph_velocity": "-partial_s Delta_T/partial_p Delta_T=-sqrt(1-p^2)*u_y/ell_T",
        "graph_velocity_interval": str(graph_velocity),
        "hit_trace": {
            "target": target_id,
            "contact": "q+ell_T*u=a_T-w_T*u_perp",
            "outgoing_velocity": "u (specular reflection fixes a tangent velocity)",
            "target_grazing_p": expected_w_sign,
        },
        "miss_trace": {
            "target": miss_target_id,
            "root": "ell_B-sqrt(Delta_B)",
            "root_interval": str(miss.near),
            "outgoing_velocity": "u-2*(u dot n_B)*n_B",
        },
        "solid_boundary_trace_relation": "genuine_jump_distinct_target_components",
        "certified_margins": {
            "ell_T_lower": "49/100",
            "miss_minus_tangent_time_lower": "3/10",
            "abs_partial_p_Delta_lower": "7/25",
            "abs_partial_s_Delta_lower": "1/4",
            "abs_p_coarea_between": ["4/5", "1"],
        },
    }


def local_event_orbit() -> dict[str, Any]:
    radical = exact_seed.Q610(Q(0), Q(1))
    p_seed = (25 * radical - 56) / 674
    assert p_seed > Q(833, 1000) and p_seed < Q(834, 1000)
    east = certify_local_event(
        "G:E", Q(833, 1000), Q(834, 1000), "W[0,0]", "G[1,1]", +1
    )
    west = certify_local_event(
        "G:W", -Q(834, 1000), -Q(833, 1000), "W[-1,0]", "G[-1,1]", -1
    )
    assert atlas.reflected_target("G", "vertical", east["owner"]) == west["owner"]
    assert atlas.reflected_target("G", "vertical", east["miss_trace"]["target"]) == west["miss_trace"]["target"]
    assert east["box"]["t"] == west["box"]["t"]
    assert east["box"]["s"] == west["box"]["s"]
    assert east["geometric_p_polarity"] == -west["geometric_p_polarity"]
    assert east["parameter_coarea_polarity"] == -west["parameter_coarea_polarity"]
    rows = [east, west]
    return {
        "orbit_id": "Jx.orbit.G-source.W-diagonal-tangency.local-v1",
        "exact_seed": {
            "t": "0",
            "s": "0",
            "p": "(25*sqrt(610)-56)/674",
            "flight": "sqrt(610)/50",
        },
        "row_count": 2,
        "event_rows": rows,
        "event_rows_sha256": canonical_digest(rows),
        "status": "complete_positive_width_Jx_symmetry_orbit",
    }


def seam_registry() -> dict[str, Any]:
    seams = []
    for source in ("G", "W"):
        for left, right, normal in (
            ("E", "N", "(+1,+1)/sqrt(2)"),
            ("N", "W", "(-1,+1)/sqrt(2)"),
            ("W", "S", "(-1,-1)/sqrt(2)"),
            ("S", "E", "(+1,-1)/sqrt(2)"),
        ):
            seams.append({
                "source": source,
                "charts": [f"{source}:{left}", f"{source}:{right}"],
                "normal": normal,
                "classification": "duplicate_source_chart_seam_cancelled",
                "physical_state_identity": "same (q,u,s) on the torus quotient",
                "target_equation_identity": "same Delta_T and selected root for every common physical target",
                "one_sided_trace_identity": "identical physical quotient trace",
                "coarea_relation": "opposite artificial boundary orientations",
                "owner": None,
                "polarity": [1, -1],
            })
    return {
        "row_count": len(seams),
        "rows": seams,
        "rows_sha256": canonical_digest(seams),
        "lift_seam_rule": "integer-translated Euclidean representatives have identical torus trace and cancel before absolute values",
        "physical_target_duplicate_inside_one_fixed_source_lift": "none_by_strict_circle_separation",
    }


def full_summary() -> dict[str, Any]:
    parent = load_parent_manifest()
    chart_summaries = {chart_id: chart_normal_form_summary(chart_id) for chart_id in CHARTS}
    assert sum(row["pair_count"] for row in chart_summaries.values()) == 12324
    assert sum(row["triple_count"] for row in chart_summaries.values()) == 221980

    reflection_rows: dict[str, Any] = {}
    for representative, (partner, axis) in REFLECTIONS.items():
        pair_digest, pair_count = reflection_combination_digest(representative, 2)
        triple_digest, triple_count = reflection_combination_digest(representative, 3)
        parent_left = parent["charts"][representative]
        parent_right = parent["charts"][partner]
        assert parent_left["pair_rows"]["unresolved"] == parent_right["pair_rows"]["unresolved"]
        assert parent_left["triple_rows"]["unresolved"] == parent_right["triple_rows"]["unresolved"]
        reflection_rows[f"{representative}->{partner}"] = {
            "axis": axis,
            "pair_combination_count": pair_count,
            "pair_mapping_sha256": pair_digest,
            "triple_combination_count": triple_count,
            "triple_mapping_sha256": triple_digest,
            "unresolved_pair_representatives": parent_left["pair_rows"]["unresolved"],
            "unresolved_triple_representatives": parent_left["triple_rows"]["unresolved"],
            "parent_pair_registry_sha256": parent_left["pair_rows"]["sha256"],
            "parent_triple_registry_sha256": parent_left["triple_rows"]["sha256"],
        }

    pair_reps = sum(row["unresolved_pair_representatives"] for row in reflection_rows.values())
    triple_reps = sum(row["unresolved_triple_representatives"] for row in reflection_rows.values())
    assert pair_reps == 1519 and 2 * pair_reps == parent["global_totals"]["pair_unresolved"]
    assert triple_reps == 5144 and 2 * triple_reps == parent["global_totals"]["triple_unresolved"]

    return {
        "parent_manifest_sha256": PARENT_MANIFEST_SHA256,
        "scope": {
            "parameter_window": "|s|<=1/400",
            "all_candidate_pair_rows": 12324,
            "all_candidate_triple_rows": 221980,
            "frozen_unresolved_pair_rows": 3038,
            "frozen_unresolved_triple_rows": 10288,
        },
        "universal_normal_form": {
            "pair": "distinct circles: no equal first root; any double line tangency is strictly time ordered",
            "triple": "pairwise reduction; no simultaneous triple first occurrence",
            "linear_bisector": "2(b-a) dot (q+tau*u)=|b|^2-|a|^2+R_a^2-R_b^2",
            "circle_resultant": "-((D^2-(R_a+R_b)^2)*(D^2-(R_a-R_b)^2))<0",
            "physical_multiple_event_count": 0,
        },
        "charts": chart_summaries,
        "reflection_deduplication": {
            "rows": reflection_rows,
            "unresolved_pair_representatives": pair_reps,
            "unresolved_triple_representatives": triple_reps,
            "orbit_size": 2,
        },
        "local_event_orbit": local_event_orbit(),
        "seam_registry": seam_registry(),
        "global_completion": {
            "pair_physical_multiple_event_normal_forms": "CERTIFIED_EMPTY_ALL_3038_COLLARS",
            "triple_physical_multiple_event_normal_forms": "CERTIFIED_EMPTY_ALL_10288_COLLARS",
            "exact_resolution_of_multi_candidate_leaves": None,
            "immutable_global_event_rows": None,
            "global_dq": None,
            "global_scalar_matching": None,
        },
    }


def main() -> None:
    summary = full_summary()
    print("GATE3_PAIR_TRIPLE_PHYSICAL_MULTIPLICITY_NORMAL_FORMS: CERTIFIED")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("GATE3_LOCAL_JX_EVENT_ROW_ORBIT: CERTIFIED")
    print("GATE3_GLOBAL_EVENT_INVENTORY_DQ_SCALAR_MATCHING: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
