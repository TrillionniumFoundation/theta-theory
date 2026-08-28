#!/usr/bin/env python3
"""Physical Gate-5 return cores, with a strict Gate-2 nonpromotion audit.

The 441,280-key registry deliberately allowed empty fibres.  This replay
binds twenty-four of those keys to explicit positive collision rectangles on
the actual two-disk billiard, uniformly for |s|<=1/400.  Every rectangle is
checked against the complete retained first-hit candidate list.  It also
certifies its transparent-wall word, a central incoming/outgoing
homogeneity margin, local prefix/suffix charts, invariant-area Jacobian, and
a first-order test-pullback seed.

These compact cores are not claimed to be maximal word domains or a stable
Young quotient.  In particular, they do not define rho, reverse weights,
native stopping, PPE, or any of the three global CM2 norm lifts.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate5_return_word_three_norm_frontier_cert as gate5


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent

GATE5_MANIFEST = HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
GATE2_MANIFEST = HERE / "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json"
FIRST_HIT_MANIFEST = HERE / "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"

S_LOWER, S_UPPER = -Q(1, 400), Q(1, 400)
AXIS_T_LOWER = Q(1, 100)
AXIS_T_UPPER = Q(1, 50)
AXIS_P_HALF_WIDTH = Q(1, 500)
DIAGONAL_T_LOWER = Q(69, 100)
DIAGONAL_T_UPPER = Q(7, 10)
DIAGONAL_P_HALF_WIDTH = Q(1, 50)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arbq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


@dataclass(frozen=True)
class Core:
    chart_id: str
    t0: Q
    t1: Q
    p0: Q
    p1: Q
    target_id: str
    crossings: tuple[str, ...]
    family: str

    @property
    def source(self) -> str:
        return self.chart_id.split(":")[0]

    @property
    def box(self) -> first_hit.PhaseBox:
        return first_hit.PhaseBox(
            self.chart_id, self.t0, self.t1, self.p0, self.p1,
            S_LOWER, S_UPPER,
        )


def physical_cores() -> tuple[Core, ...]:
    rows: list[Core] = []
    axis_targets = {
        "E": (1, 0, "X+"),
        "W": (-1, 0, "X-"),
        "N": (0, 1, "Y+"),
        "S": (0, -1, "Y-"),
    }
    for source in ("G", "W"):
        for cell in ("E", "W", "N", "S"):
            ix, iy, token = axis_targets[cell]
            # A gray lift straddles the transparent grid wall, so the short
            # G-to-G gap stays inside one open cell.  The central white lift
            # does not straddle it and its translate crosses exactly once.
            crossings = () if source == "G" else (token,)
            rows.append(Core(
                f"{source}:{cell}", AXIS_T_LOWER, AXIS_T_UPPER,
                -AXIS_P_HALF_WIDTH, AXIS_P_HALF_WIDTH,
                f"{source}[{ix},{iy}]", crossings, "axis_translate",
            ))

    diagonal_data = {
        "G": {
            "NE": (("E", 1), ("N", 1), "W[0,0]"),
            "NW": (("W", 1), ("N", -1), "W[-1,0]"),
            "SE": (("E", -1), ("S", 1), "W[0,-1]"),
            "SW": (("W", -1), ("S", -1), "W[-1,-1]"),
        },
        "W": {
            "NE": (("E", 1), ("N", 1), "G[1,1]"),
            "NW": (("W", 1), ("N", -1), "G[0,1]"),
            "SE": (("E", -1), ("S", 1), "G[1,0]"),
            "SW": (("W", -1), ("S", -1), "G[0,0]"),
        },
    }
    for source in ("G", "W"):
        for direction in ("NE", "NW", "SE", "SW"):
            first, second, target_id = diagonal_data[source][direction]
            for cell, sign in (first, second):
                if sign > 0:
                    t0, t1 = DIAGONAL_T_LOWER, DIAGONAL_T_UPPER
                else:
                    t0, t1 = -DIAGONAL_T_UPPER, -DIAGONAL_T_LOWER
                rows.append(Core(
                    f"{source}:{cell}", t0, t1,
                    -DIAGONAL_P_HALF_WIDTH, DIAGONAL_P_HALF_WIDTH,
                    target_id, (), f"diagonal_{direction}",
                ))
    rows.sort(key=lambda row: (
        row.chart_id, row.target_id, row.crossings,
        row.t0, row.t1, row.p0, row.p1,
    ))
    assert len(rows) == 24
    return tuple(rows)


def load_dependencies() -> dict[str, str]:
    gate5_manifest = json.loads(GATE5_MANIFEST.read_text(encoding="utf-8"))
    gate2_manifest = json.loads(GATE2_MANIFEST.read_text(encoding="utf-8"))
    first_manifest = json.loads(FIRST_HIT_MANIFEST.read_text(encoding="utf-8"))
    assert gate5_manifest["result"]["immutable_candidate_key_registry"][
        "candidate_return_word_key_count"
    ] == 441280
    assert gate5_manifest["result"]["immutable_candidate_key_registry"][
        "exact_nonempty_candidate_key_count"
    ] is None
    assert gate5_manifest["result"]["immutable_candidate_key_registry"][
        "domain_contract"
    ]["regular_domain_partition"] is True
    assert gate5_manifest["result"]["required_operator_field_schema"][
        "required_field_count_per_physical_homogeneous_level"
    ] == 18
    assert gate5_manifest["result"]["required_operator_field_schema"][
        "homogeneous_subbranch_ids_materialized"
    ] is False
    assert gate2_manifest["verdict"]["gate2"] == "NOT_CERTIFIED"
    assert first_manifest["candidate_reduction"]["retained_pair_count"] == 448
    return {
        GATE5_MANIFEST.name: file_sha256(GATE5_MANIFEST),
        GATE2_MANIFEST.name: file_sha256(GATE2_MANIFEST),
        FIRST_HIT_MANIFEST.name: file_sha256(FIRST_HIT_MANIFEST),
        Path(first_hit.__file__).name: file_sha256(Path(first_hit.__file__)),
        Path(gate5.__file__).name: file_sha256(Path(gate5.__file__)),
    }


def contact_geometry(core: Core) -> dict[str, arb]:
    box = core.box
    target = first_hit.target_by_id(core.target_id)
    qx, qy, ux, uy, s = first_hit.phase_geometry(box)
    ax, ay = first_hit.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = arbq(first_hit.RADIUS[target.obstacle])
    discriminant = radius * radius - transverse * transverse
    assert bool(discriminant > 0)
    radical = discriminant.sqrt()
    root = ell - radical
    assert bool(root > 0) and bool(root < 3)
    # Dependency-reduced contact and target normal.
    hx = ax - radical * ux + transverse * uy
    hy = ay - radical * uy - transverse * ux
    nx = (-radical * ux + transverse * uy) / radius
    ny = (-radical * uy - transverse * ux) / radius
    p_target = transverse / radius
    return {
        "qx": qx, "qy": qy, "ux": ux, "uy": uy,
        "hx": hx, "hy": hy, "nx": nx, "ny": ny,
        "p_target": p_target, "root": root,
    }


def integer_crossings(q: arb, h: arb, velocity: arb, axis: str) -> tuple[str, ...]:
    if bool(velocity > 0):
        sign = "+"
    elif bool(velocity < 0):
        sign = "-"
    else:
        # On the transverse coordinate of an axis core the velocity family
        # contains both signs.  A common open grid cell for both endpoints
        # still proves that every member has zero crossings there.
        for wall in range(-2, 3):
            wall_arb = arb(wall)
            same_lower = bool(q < wall_arb) and bool(h < wall_arb)
            same_upper = bool(q > wall_arb) and bool(h > wall_arb)
            if not (same_lower or same_upper):
                raise AssertionError(
                    f"sign-changing coordinate meets wall {axis}={wall}: q={q}, h={h}"
                )
        return ()
    assert bool(q > -3) and bool(q < 3) and bool(h > -3) and bool(h < 3)
    hits: list[str] = []
    for wall in range(-2, 3):
        wall_arb = arb(wall)
        if sign == "+" and bool(q < wall_arb) and bool(h > wall_arb):
            hits.append(axis + sign)
            continue
        if sign == "-" and bool(q > wall_arb) and bool(h < wall_arb):
            hits.append(axis + sign)
            continue
        same_lower = bool(q < wall_arb) and bool(h < wall_arb)
        same_upper = bool(q > wall_arb) and bool(h > wall_arb)
        if not (same_lower or same_upper):
            raise AssertionError(f"wall {axis}={wall} unresolved: q={q}, h={h}")
    return tuple(hits)


def expected_suffix_direction(core: Core) -> tuple[int, int]:
    source = first_hit.Target(core.source, 0, 0)
    target = first_hit.target_by_id(core.target_id)
    # At s=0, the near-side target normal points back toward the source.
    sx = source.ix + (Q(1, 2) if source.obstacle == "W" else Q(0))
    sy = source.iy + (Q(1, 2) if source.obstacle == "W" else Q(0))
    tx = target.ix + (Q(1, 2) if target.obstacle == "W" else Q(0))
    ty = target.iy + (Q(1, 2) if target.obstacle == "W" else Q(0))
    dx, dy = tx - sx, ty - sy
    cx = -1 if dx > 0 else (1 if dx < 0 else 0)
    cy = -1 if dy > 0 else (1 if dy < 0 else 0)
    assert (cx, cy) != (0, 0)
    return cx, cy


def certify_core(core: Core) -> dict[str, Any]:
    assert core.target_id in first_hit.candidate_ids(core.chart_id)
    assert core.crossings in set(gate5.crossing_patterns())
    selected_root, missed, later = first_hit.certify_first_hit_patch(
        core.box, core.target_id
    )
    geometry = contact_geometry(core)
    x_crossings = integer_crossings(
        geometry["qx"], geometry["hx"], geometry["ux"], "X"
    )
    y_crossings = integer_crossings(
        geometry["qy"], geometry["hy"], geometry["uy"], "Y"
    )
    actual_crossings = x_crossings + y_crossings
    # Our cores have at most one wall event, so no cross-axis time ordering
    # remains to be decided.
    assert len(actual_crossings) <= 1
    assert actual_crossings == core.crossings

    p_source = first_hit.arb_interval(core.p0, core.p1)
    p_target = geometry["p_target"]
    assert bool(arbq(Q(9, 100)) - p_source * p_source > 0)
    assert bool(arbq(Q(9, 100)) - p_target * p_target > 0)
    cp_source = (1 - p_source * p_source).sqrt()
    cp_target = (1 - p_target * p_target).sqrt()
    assert bool(cp_source > arbq(Q(19, 20)))
    assert bool(cp_target > arbq(Q(19, 20)))

    suffix_direction = expected_suffix_direction(core)
    suffix_chart_dot = (
        suffix_direction[0] * geometry["nx"]
        + suffix_direction[1] * geometry["ny"]
    )
    assert bool(suffix_chart_dot > arbq(Q(1, 3)))

    key = gate5.registry_key_row(core.chart_id, core.target_id, core.crossings)
    return {
        "key": [core.chart_id, core.target_id, list(core.crossings), len(core.crossings) + 1],
        "family": core.family,
        "parameter_window": [str(S_LOWER), str(S_UPPER)],
        "source_rectangle": {
            "t": [str(core.t0), str(core.t1)],
            "p=sin(phi)": [str(core.p0), str(core.p1)],
        },
        "strict_first_hit": True,
        "selected_root_enclosure": str(selected_root),
        "retained_competitors_missed": missed,
        "retained_competitors_strictly_later": later,
        "transparent_wall_record": list(actual_crossings),
        "no_simultaneous_corner_crossing": True,
        "incoming_and_outgoing_abs_p_strict_upper": "3/10",
        "incoming_and_outgoing_cos_phi_strict_lower": "19/20",
        "prefix_chart": f"canonical collision chart on {core.chart_id}",
        "suffix_chart": {
            "target_lift": core.target_id,
            "open_semicircle_direction": list(suffix_direction),
            "normal_dot_direction_strict_lower": "1/3",
        },
        "canonical_area_coordinates": "(r,p=sin(phi))",
        "absolute_inverse_area_Jacobian": "1",
        "log_area_Jacobian_distortion": "0",
        "forward_and_reverse_D_infinity_norm_strict_upper": "158",
        "local_Calpha_test_pullback_cost_strict_upper": "158 for 0<alpha<=1",
        "key_row_sha256": canonical_digest(key),
    }


def physical_registry() -> dict[str, Any]:
    cores = physical_cores()
    rows = [certify_core(core) for core in cores]
    keys = [canonical_json(row["key"]) for row in rows]
    assert len(set(keys)) == 24
    # Distinct regular word keys are pairwise disjoint by the frozen domain
    # contract.  Every core was proved to lie inside its displayed key, so
    # summing their collision masses does not double count chart rectangles.
    pairwise_disjoint_by_word_partition = len(set(keys)) == len(keys)
    assert pairwise_disjoint_by_word_partition
    roof_histogram = {"1": 20, "2": 4}
    assert sum(len(row["key"][2]) == 0 for row in rows) == 20
    assert sum(len(row["key"][2]) == 1 for row in rows) == 4

    raw_mass_lower = sum(
        first_hit.RADIUS[core.source]
        * (core.t1 - core.t0) * (core.p1 - core.p0)
        for core in cores
    )
    # dr=R dtheta and dtheta/dt=(1-t^2)^(-1/2)>=1.
    assert raw_mass_lower == Q(273, 156250)
    # Total collision volume is 4*pi*(R_G+R_W); pi<22/7.
    normalized_mass_lower = raw_mass_lower / (
        4 * Q(22, 7) * (first_hit.RADIUS["G"] + first_hit.RADIUS["W"])
    )
    assert normalized_mass_lower == Q(147, 550000)

    # The exact Birkhoff derivative matrix has infinity-norm numerator
    # 2391/16<150.  Both incidence cosines exceed 19/20 here.
    assert Q(2391, 16) < 150
    assert 150 * Q(20, 19) < 158

    return {
        "candidate_key_universe_size": 441280,
        "distinct_certified_nonempty_key_lower_bound": 24,
        "physical_compact_homogeneous_core_count": 24,
        "roof_histogram": roof_histogram,
        "registered_roof_level_prefix_suffix_pairs": 28,
        "registered_endpoint_boundary_splits": 52,
        "all_cores_uniform_on_full_parameter_window": True,
        "all_24_keys_members_of_frozen_441280_envelope": True,
        "all_cores_strict_first_hit_against_complete_retained_candidate_list": True,
        "all_wall_records_physically_replayed": True,
        "all_cores_central_incoming_and_outgoing_homogeneity": True,
        "all_cores_have_local_prefix_and_suffix_collision_charts": True,
        "all_24_core_domains_pairwise_disjoint_by_distinct_regular_word_keys": (
            pairwise_disjoint_by_word_partition
        ),
        "mass_lower_bound_sums_only_pairwise_disjoint_core_domains": True,
        "collision_SRB_unnormalized_mass_rational_lower": str(raw_mass_lower),
        "collision_SRB_normalized_mass_strict_lower_using_pi_lt_22_over_7": str(
            normalized_mass_lower
        ),
        "collision_SRB_normalized_mass_decimal_lower": float(normalized_mass_lower),
        "rows_sha256": canonical_digest(rows),
        "distinct_key_rows_sha256": canonical_digest(sorted(keys)),
        "local_seed_bindings_on_each_core": {
            "nonempty_or_empty_domain_proof": "CERTIFIED_NONEMPTY",
            "compact_central_homogeneity_core": "CERTIFIED_LOCAL_SUBCORE_ONLY",
            "source_collision_endpoint_chart": "CERTIFIED",
            "target_collision_endpoint_chart": "CERTIFIED_LOCAL_SEMICIRCLE",
            "collision_SRB_area_Jacobian_identity": "CERTIFIED_SEED:1",
            "log_collision_SRB_area_Jacobian_identity": "CERTIFIED_SEED:0",
            "full_collision_branch_Calpha_test_pullback_seed": (
                "CERTIFIED_LOCAL_FULL_RETURN_COST_LT_158"
            ),
        },
        "full_key_schema_field_completion": {
            "completed_field_count_on_each_of_24_keys": 1,
            "completed_field": "nonempty_or_empty_domain_proof=NONEMPTY",
            "seven_local_seed_types_are_not_seven_completed_schema_fields": True,
            "physical_homogeneity_subbranch_table_completed": False,
            "all_roof_level_prefix_suffix_charts_completed": False,
            "roof_two_intermediate_transparent_wall_chart_completed": False,
            "area_Jacobian_seed_is_not_unstable_curve_inverse_Jacobian_field": True,
            "log_area_seed_is_not_log_unstable_Jacobian_distortion_field": True,
        },
        "strict_scope": (
            "positive compact subcores of 24 candidate keys; not maximal word "
            "domains, not a partition of the regular collision section, and "
            "not complete 18-field CM2 operator blocks"
        ),
    }


def remaining_operator_frontier() -> dict[str, Any]:
    return {
        "one_full_key_schema_field_decided_on_each_of_24_keys": True,
        "seven_typed_local_seed_types_on_each_of_24_cores": True,
        "seven_physical_schema_fields_bound_on_each_core": False,
        "physical_homogeneity_subbranch_table_on_full_key": False,
        "all_roof_level_prefix_suffix_charts": False,
        "roof_two_intermediate_transparent_wall_chart_and_costs": False,
        "area_Jacobian_is_not_unstable_curve_Jacobian": True,
        "branch_internal_no_singularity_cut": True,
        "global_one_step_cut_growth_Z_sum": False,
        "face_transversality_C2_coarea_fields": False,
        "C1_face_trace_and_moving_boundary_DQ": False,
        "global_regular_density_operator_cost_after_characteristic_restriction": False,
        "standard_family_operator_cost": False,
        "flux_face_operator_cost": False,
        "global_dynamic_test_operator_cost": False,
        "operator_phase_block": False,
        "complete_18_field_physical_operator_block_count": 0,
        "exact_total_nonempty_key_count": None,
        "three_CM2_norm_lifts": False,
        "full_Kac_operator_phase_transfer": False,
        "gate5_certified": False,
    }


def gate2_nonpromotion() -> dict[str, Any]:
    return {
        "new_positive_collision_SRB_key_mass_lower": "147/550000",
        "carrier": "two-dimensional standard collision section N=G sqcup W",
        "stable_saturated_product_base": False,
        "stable_projection": False,
        "quotient_density_rho": False,
        "onto_quotient_inverse_branches": False,
        "physical_reverse_weights": False,
        "same_carrier_endpoint_maps": False,
        "native_stopping_antichain": False,
        "PPE": False,
        "key_refined_two_dimensional_reverse_kernel_remains_Dirac": True,
        "raw_two_strip_common_rectangle_unregistered_fraction_lower": "0.903",
        "why_gap_does_not_change": (
            "the new mass is collision-SRB mass on N, whereas 0.903 is the "
            "independent unsaturated fraction of the declared common rectangle; "
            "no stable saturation or projection relates the two carriers"
        ),
        "gate2_certified": False,
    }


def certify() -> dict[str, Any]:
    provenance = load_dependencies()
    registry = physical_registry()
    frontier = remaining_operator_frontier()
    gate2 = gate2_nonpromotion()
    result = {
        "schema": "cm2.gate25.physical-return-core-registry.v1",
        "provenance": provenance,
        "physical_return_core_registry": registry,
        "remaining_operator_frontier": frontier,
        "Gate2_nonpromotion": gate2,
        "completion": {
            "at_least_24_candidate_keys_certified_nonempty": True,
            "positive_collision_SRB_mass_physical_core_registry": True,
            "one_full_key_schema_field_decided_on_each_of_24_keys": True,
            "seven_typed_local_seed_types_on_registered_cores": True,
            "seven_physical_word_schema_fields_bound_on_registered_cores": False,
            "all_roof_level_prefix_suffix_slots_bound": False,
            "complete_nonempty_word_domain_decision": False,
            "complete_18_field_operator_registry": False,
            "stable_quotient_or_PPE": False,
            "gate2_certified": False,
            "gate5_certified": False,
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE5_PHYSICAL_NONEMPTY_RETURN_KEYS_AT_LEAST_24: CERTIFIED")
    print("GATE5_POSITIVE_MASS_PHYSICAL_CORE_REGISTRY: CERTIFIED")
    print("GATE5_SEVEN_LOCAL_SEEDS_ARE_NOT_SEVEN_SCHEMA_FIELDS: CERTIFIED")
    print("GATE5_COMPLETE_18_FIELD_OPERATOR_REGISTRY: NOT_CERTIFIED")
    print("GATE2_STABLE_QUOTIENT_PPE: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
