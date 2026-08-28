#!/usr/bin/env python3
"""Round-25 Gate-2 product-base anchor and exact nonpromotion frontier.

This append-only certificate uses the first full-dimensional C24 return leaf
to anchor an explicit positive-area cone-product tile and an admissible
reference unstable interval on one actual CM2 collision branch.  The affine
stable-looking foliation and its exact area disintegration are intentionally
typed as *candidates*: one-step regularity does not prove that those curves
are invariant local stable manifolds.  Consequently none of the immutable
seventeen physical Gate-2 fields is promoted.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
Q = Fraction

DEPENDENCIES = {
    "cm2-twenty-fourth-direct-assault-manifest-2026-07-18.sha256":
        "fde26b3f560086484a63cd0cc2e39a025d573c31982295a3702a14f9821e3c2c",
    "cm2-gate2-round23-core-kac-quotient-obstruction-manifest-2026-07-18.json":
        "cb857a533c3c23658cc354d46cd29e87511be9a36679f37c4a6326bae19731ba",
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json":
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183",
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json":
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d",
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json":
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",
}

GATE2 = "cm2-gate2-round23-core-kac-quotient-obstruction-manifest-2026-07-18.json"
OPEN_GEOMETRY = "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
SPARSE_TAIL = "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
FULL_CORE = "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"

ANCHOR_ATOM_ID = (
    "full-core-step1:2f14a5ba38ba80f0089ec976791bc0760f2ca800bf00dc287883e57407856bc0"
)
ANCHOR_ATOM_ROW_SHA256 = (
    "b6b5bfb29286e65fd568f89893a3ca4fdccd95c7b3f4be54e9b22bbbcc9b6b89"
)
FULL_RAW_LEAF_ROWS_SHA256 = (
    "1cfd4d6f7fdd57034655fd002e370c5c1c80b2da53bff06e4ff3b7c0f8c71209"
)
SOURCE_CORE_ID = (
    "core:353ad74b3709b7628481fade52784ee19a4a4d159f4eb1b520f42f796455a670"
)
DESTINATION_CORE_ID = (
    "core:0d155400725ff145cad8ec2e7b26a044a629a022f501fa09f9c800c27f05d74f"
)

# These are the exact core-id payloads used by the frozen full-core producer.
# Replaying them here closes the otherwise implicit source-component/radius
# join behind the cone slope and collision-mass calculations below.
SOURCE_CORE_PAYLOAD = {
    "chart_id": "G:E",
    "t": ["-7/10", "-69/100"],
    "p": ["-1/50", "1/50"],
    "target_id": "W[0,-1]",
    "crossings": [],
}
DESTINATION_CORE_PAYLOAD = {
    "chart_id": "W:N",
    "t": ["-7/10", "-69/100"],
    "p": ["-1/50", "1/50"],
    "target_id": "G[0,1]",
    "crossings": [],
}
SOURCE_RADIUS = Q(9, 25)
PARAMETER_WINDOW_WIDTH = Q(1, 200)
GLOBAL_DTHETA_DT_UPPER = Q(1401, 1000)

GATE2_FIELDS = (
    "stable_saturated_product_base_Lambda_A",
    "reference_unstable_interval_I_A",
    "stable_holonomy_projection_pi_s",
    "stable_holonomy_conditional_SRB_Jacobian",
    "connected_first_return_strip_partition",
    "onto_full_image_quotient_branches_h_a",
    "quotient_density_rho_with_upper_lower_bounds",
    "physical_reverse_weights_p_a",
    "transported_projective_matrix_M_a_in_one_trivialisation",
    "same_carrier_endpoint_maps_X_Y",
    "endpoint_denominator_lower_bound",
    "nonzero_endpoint_wedge",
    "inverse_cylinder_diameter_registry",
    "native_scale_prefix_stopping_antichain",
    "overshoot_cemetery_and_two_sided_scale_comparison",
    "off_diagonal_projective_near_collision_bound",
    "parentwise_normalized_amplitude_moment",
)


class CertificateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_dependencies() -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.parent.resolve() == HERE, f"dependency escapes directory: {name}")
        require(not path.is_symlink(), f"symlink dependency rejected: {name}")
        require(path.is_file(), f"missing dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash changed: {name}")
        if path.suffix == ".json":
            loaded[name] = json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=reject_duplicate_pairs,
                parse_constant=lambda token: (_ for _ in ()).throw(
                    CertificateError(f"non-finite JSON token: {token}")
                ),
            )
    return loaded


def qtext(value: Q) -> str:
    return str(value)


def selected_anchor(full_core: dict[str, Any]) -> dict[str, Any]:
    rows = full_core["result"]["adaptive_full_core_step1_raw_leaf_rows"]
    registry = full_core["result"]["adaptive_full_core_step1_registry"]
    require(digest(rows) == FULL_RAW_LEAF_ROWS_SHA256,
            "full raw-leaf registry digest changed")
    require(registry["raw_leaf_rows_sha256"] == FULL_RAW_LEAF_ROWS_SHA256,
            "declared raw-leaf registry digest changed")
    selected = [row for row in rows if row["atom_id"] == ANCHOR_ATOM_ID]
    require(len(selected) == 1, "anchor atom is not unique")
    row = selected[0]
    first_return = next(
        (candidate for candidate in rows
         if candidate["classification"] == "RETURN_AT_1_INNER"),
        None,
    )
    require(first_return is row, "anchor is no longer the first frozen R1 leaf")
    require(digest(row) == ANCHOR_ATOM_ROW_SHA256, "anchor row digest changed")
    require("core:" + digest(SOURCE_CORE_PAYLOAD) == SOURCE_CORE_ID,
            "source core payload/id join failed")
    require("core:" + digest(DESTINATION_CORE_PAYLOAD) == DESTINATION_CORE_ID,
            "destination core payload/id join failed")
    require(row["classification"] == "RETURN_AT_1_INNER", "anchor is not R1 inner")
    require(row["source_core_id"] == SOURCE_CORE_ID, "source core changed")
    require(row["destination_core_id"] == DESTINATION_CORE_ID, "destination core changed")
    require(row["source_core_index"] == 1, "source core index changed")
    require(row["depth"] == 14 and row["dyadic_path"] == "00000000100000",
            "anchor dyadic registry changed")
    require(row["source_box"] == {
        "t": ["-7/10", "-2239/3200"],
        "p": ["-1/50", "-3/160"],
        "s": ["-3/1600", "-1/640"],
    }, "anchor source box changed")
    require(row["positive_two_dimensional_source_rectangle_at_each_s"] is True,
            "anchor lost positive dimension")
    require(row["strict_next_collision_owner_inherited_from_whole_parent_core"] is True,
            "anchor owner proof changed")
    require(row["complete_retained_candidate_comparison_inherited"] is True,
            "anchor complete owner comparison changed")
    require(row["positive_parameter_interval"] is True,
            "anchor parameter interval became degenerate")
    require(row["canonical_invariant_area_coordinates"] == "(r,p=sin(phi))",
            "anchor area coordinates changed")
    require(row["absolute_inverse_invariant_area_Jacobian"] == "1",
            "anchor area Jacobian changed")
    require(row["log_invariant_area_Jacobian_distortion"] == "0",
            "anchor log area distortion changed")
    require(row["parent_owner_witness_sha256"]
            == "320471cbe8a985447e67ad6e2ff60ff34586f62393fdee3381ced5a30bbd47a3",
            "anchor parent owner witness changed")
    require(row["classification_witness_rows_sha256"]
            == "e40c7da17c703c971a17382d8850fefd7c71a7c50d5febd35dc16e034acb1792",
            "anchor classification witness changed")
    require(row["output_enclosures"] == {
        "normal_x": "[-0.69 +/- 5.68e-3]",
        "normal_y": "[0.72 +/- 3.86e-3]",
        "p_target": "[-0.01 +/- 3.85e-3]",
    }, "anchor output enclosures changed")

    t0, t1 = map(Q, row["source_box"]["t"])
    p0, p1 = map(Q, row["source_box"]["p"])
    s0, s1 = map(Q, row["source_box"]["s"])
    averaged_base_mass = (
        SOURCE_RADIUS * (t1 - t0) * (p1 - p0) * (s1 - s0)
        / PARAMETER_WINDOW_WIDTH
    )
    require(averaged_base_mass == Q(9, 1024000000),
            "anchor parameter-averaged base mass replay failed")
    require(row["parameter_averaged_unnormalized_base_mass"]
            == qtext(averaged_base_mass), "anchor base mass changed")
    require(row["parameter_averaged_unnormalized_collision_mass_lower"]
            == qtext(averaged_base_mass), "anchor collision mass lower changed")
    require(row["parameter_averaged_unnormalized_collision_mass_upper"]
            == qtext(GLOBAL_DTHETA_DT_UPPER * averaged_base_mass),
            "anchor collision mass upper changed")
    atom_payload = {
        "source_core_id": SOURCE_CORE_ID,
        "dyadic_path": row["dyadic_path"],
        "source_box": row["source_box"],
    }
    require("full-core-step1:" + digest(atom_payload) == ANCHOR_ATOM_ID,
            "anchor atom payload/id join failed")
    return row


def exact_cone_product_tile() -> dict[str, Any]:
    # Product coordinates (u,v) inside the selected source atom:
    # t=t_c+u+v, p=p_c+(3/2)u-(3/2)v.
    t0, t1 = Q(-7, 10), Q(-2239, 3200)
    p0, p1 = Q(-1, 50), Q(-3, 160)
    tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
    a = b = Q(1, 25600)
    slope_tp = Q(3, 2)
    t_deviation = a + b
    p_deviation = slope_tp * (a + b)
    require(tc == Q(-4479, 6400) and pc == Q(-31, 1600), "tile center changed")
    require(tc - t_deviation > t0 and tc + t_deviation < t1,
            "tile is not strictly inside t interval")
    require(pc - p_deviation > p0 and pc + p_deviation < p1,
            "tile is not strictly inside p interval")

    # In canonical collision coordinates r=R theta(t), phi=asin(p),
    # |dphi/dr|=(3/2)sqrt(1-t^2)/(R_G sqrt(1-p^2)).  The displayed
    # rational witnesses put both candidate directions strictly in the
    # frozen stable/unstable geometric cones.
    physical_slope_lower = slope_tp * Q(7, 10) / SOURCE_RADIUS
    physical_slope_upper = slope_tp / (SOURCE_RADIUS * Q(49, 50))
    frozen_cone_lower = Q(25, 9)
    frozen_cone_upper = Q(4108425, 145348)
    tile_abs_p_upper = abs(pc) + p_deviation
    require(tile_abs_p_upper == Q(499, 25600) < Q(1, 50),
            "tile p endpoint bound failed")
    require(1 - Q(7, 10) ** 2 > Q(7, 10) ** 2,
            "sqrt(1-t^2)>7/10 square witness failed")
    require(1 - Q(1, 50) ** 2 > Q(49, 50) ** 2,
            "sqrt(1-p^2)>49/50 square witness failed")
    require(GLOBAL_DTHETA_DT_UPPER ** 2 * (1 - Q(7, 10) ** 2) > 1,
            "global dtheta/dt rational upper witness failed")
    require(physical_slope_lower > frozen_cone_lower, "cone lower gap failed")
    require(physical_slope_upper < frozen_cone_upper, "cone upper gap failed")

    tp_jacobian = Q(3)
    tp_area = tp_jacobian * (2 * a) * (2 * b)
    require(tp_area == Q(3, 163840000), "tile area changed")
    collision_mass_lower = SOURCE_RADIUS * tp_area
    require(collision_mass_lower == Q(27, 4096000000), "mass lower changed")
    normalized_mass_lower = collision_mass_lower / (
        4 * Q(22, 7) * Q(13, 25)
    )
    require(normalized_mass_lower == Q(189, 187432960000),
            "normalized mass lower changed")

    # Disintegration of dr dp over the affine candidate fibres v=constant:
    # rho_aff(u)=int 3 R_G / sqrt(1-(t_c+u+v)^2) dv.
    rho_lower = 6 * SOURCE_RADIUS * b
    rho_upper = rho_lower * GLOBAL_DTHETA_DT_UPPER
    require(rho_lower == Q(27, 320000), "affine rho lower changed")
    require(rho_upper == Q(37827, 320000000), "affine rho upper changed")

    core = {
        "product_coordinates": {
            "domain": "|u|<=1/25600, |v|<=1/25600",
            "map_to_collision_chart": (
                "t=-4479/6400+u+v; p=-31/1600+(3/2)u-(3/2)v"
            ),
            "absolute_dt_dp_over_du_dv_Jacobian": "3",
        },
        "strict_source_atom_interior": {
            "t_margin": qtext((t1 - t0) / 2 - t_deviation),
            "p_margin": qtext((p1 - p0) / 2 - p_deviation),
            "inside_selected_R1_atom_for_every_s_in_slab": True,
        },
        "collision_coordinate_binding": {
            "source_core_payload": dict(SOURCE_CORE_PAYLOAD),
            "source_collision_component": "G",
            "source_radius": qtext(SOURCE_RADIUS),
            "coordinate_change": "r=R_G*asin(t), phi=asin(p)",
            "collision_area_density": "R_G/sqrt(1-t^2) dt dp",
        },
        "reference_cone_unstable_candidate": {
            "name": "I_A^cand",
            "definition": "v=0, |u|<=1/25600",
            "physical_abs_dphi_dr_strict_bounds": [
                qtext(physical_slope_lower), qtext(physical_slope_upper)
            ],
            "squared_rational_witnesses": {
                "tile_abs_t_at_most": "7/10",
                "tile_abs_p_strict_upper": "499/25600<1/50",
                "sqrt_one_minus_t2_strict_lower": (
                    "51/100>49/100=(7/10)^2"
                ),
                "sqrt_one_minus_p2_strict_lower": (
                    "2499/2500>2401/2500=(49/50)^2"
                ),
            },
            "inside_frozen_unstable_cone": True,
            "is_declared_actual_unstable_manifold": False,
        },
        "interval_indexed_cone_stable_candidates": {
            "definition": "W_u^cs={u fixed, |v|<=1/25600}",
            "physical_dphi_dr_strict_bounds": [
                qtext(-physical_slope_upper), qtext(-physical_slope_lower)
            ],
            "inside_frozen_stable_cone": True,
            "forward_invariance_certified": False,
            "actual_local_stable_manifolds_certified": False,
        },
        "affine_candidate_projection": {
            "formula": "pi_aff(u,v)=(u,0)",
            "constant_on_affine_candidate_fibres": True,
            "identified_with_physical_stable_holonomy_pi_s": False,
        },
        "positive_collision_area": {
            "dt_dp_area": qtext(tp_area),
            "unnormalized_collision_SRB_mass_strict_lower": qtext(collision_mass_lower),
            "normalized_collision_SRB_mass_strict_lower": qtext(normalized_mass_lower),
        },
        "affine_area_disintegration_only": {
            "rho_aff_formula": (
                "rho_aff(u)=integral_{-1/25600}^{1/25600} "
                "(27/25)/sqrt(1-(-4479/6400+u+v)^2) dv"
            ),
            "rho_aff_strict_bounds": [qtext(rho_lower), qtext(rho_upper)],
            "is_conditional_stable_holonomy_SRB_Jacobian": False,
        },
    }
    return core


def build_result() -> dict[str, Any]:
    deps = load_dependencies()
    gate2 = deps[GATE2]
    geometry = deps[OPEN_GEOMETRY]
    sparse = deps[SPARSE_TAIL]
    full_core = deps[FULL_CORE]
    anchor = selected_anchor(full_core)

    predecessor_audit = gate2["result"]["Gate2_17_field_nonpromotion"]
    require(len(predecessor_audit["field_rows"]) == 17,
            "Gate2 field count changed")
    require(predecessor_audit["completed_physical_field_count_after_round23"] == 0,
            "predecessor Gate2 field count changed")
    require(
        tuple(row["field"] for row in predecessor_audit["field_rows"])
        == GATE2_FIELDS,
        "immutable Gate2 field order changed",
    )
    require(geometry["result"]["stable_curve_open_hole_geometry"][
        "certified_O2_constant_Ct"] == 1493,
        "stable-curve geometry binding changed")
    require(sparse["result"]["scheduled_and_all_time_tail"][
        "uniform_unweighted_exponential_collision_return_tail"] == "CERTIFIED",
        "new C24 exponential tail missing")
    require(full_core["result"]["adaptive_full_core_step1_registry"][
        "source_phase_dimension_at_fixed_parameter"] == 2,
        "full-core carrier dimension changed")
    require(full_core["result"]["provenance"]["clock"]
            == "source_core_state_is_time_0_and_next_collision_is_time_1",
            "full-core clock changed")
    require(full_core["result"]["provenance"]["dependency_sha256"][
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ] == "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
            "physical core registry provenance changed")
    require(geometry["result"]["frozen_core_inventory"]["core_rows_sha256"]
            == "c3042515b4a244b064f1aaef97ee236c5d3f6078a53fe3fb9e865a1976853b2f",
            "frozen physical core rows changed")

    tile = exact_cone_product_tile()
    actual_atom_audit = {
        "full_raw_leaf_rows_sha256": FULL_RAW_LEAF_ROWS_SHA256,
        "selected_raw_row_sha256": ANCHOR_ATOM_ROW_SHA256,
        "selected_is_first_RETURN_AT_1_INNER_row": True,
        "atom_id_payload_replayed": True,
        "source_core_payload": dict(SOURCE_CORE_PAYLOAD),
        "source_core_payload_id": SOURCE_CORE_ID,
        "destination_core_payload": dict(DESTINATION_CORE_PAYLOAD),
        "destination_core_payload_id": DESTINATION_CORE_ID,
        "source_component_and_radius": {"component": "G", "radius": "9/25"},
        "source_box": dict(anchor["source_box"]),
        "dyadic_path": anchor["dyadic_path"],
        "depth": anchor["depth"],
        "classification": anchor["classification"],
        "parent_owner_witness_sha256": anchor["parent_owner_witness_sha256"],
        "classification_witness_rows_sha256": (
            anchor["classification_witness_rows_sha256"]
        ),
        "parameter_averaged_unnormalized_base_mass": (
            anchor["parameter_averaged_unnormalized_base_mass"]
        ),
        "parameter_averaged_unnormalized_collision_mass_upper": (
            anchor["parameter_averaged_unnormalized_collision_mass_upper"]
        ),
        "strict_complete_first_owner_inherited": True,
        "strict_whole_box_R1_core_membership": True,
    }
    anchor_binding = {
        "registry_id": "gate2-r25-anchor:" + digest({
            "actual_atom_audit": actual_atom_audit,
            "tile": tile["product_coordinates"],
        }),
        "anchor_atom_id": ANCHOR_ATOM_ID,
        "source_core_id": SOURCE_CORE_ID,
        "destination_core_id": DESTINATION_CORE_ID,
        "source_parameter_slab": list(anchor["source_box"]["s"]),
        "physical_branch_class": "RETURN_AT_1_INNER",
        "whole_tile_has_same_unique_next_collision_and_returns_to_C24_at_time_1": True,
        "canonical_invariant_area_inverse_Jacobian": "1",
    }

    missing = {
        "true_stable_span": (
            "a positive ell_s and one interval-indexed family of actual local stable "
            "manifolds spanning the registered tile"
        ),
        "infinite_future_domain": (
            "a homogeneous forward itinerary/buffer or graph-transform domain on every "
            "declared plaque; the R1 atom proves only one collision"
        ),
        "stable_contraction": "explicit C_sep and lambda_s<1 on that same plaque registry",
        "log_unstable_Jacobian_modulus": (
            "explicit H_J and alpha for log J^u T along paired stable orbits"
        ),
        "holonomy_product_bound": (
            "B_h=H_J*C_sep^alpha/(1-lambda_s^alpha), giving "
            "exp(-B_h)<=J(pi^s)<=exp(B_h)"
        ),
        "return_strip_compatibility": (
            "connected stable-saturated first-return strips whose images u-cross the "
            "same Lambda_A and preserve the branch ID"
        ),
    }

    core: dict[str, Any] = {
        "schema": "cm2.gate2.round25.product-base-anchor-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "arithmetic": "exact rational replay plus frozen strict Arb branch rows",
            "literature_checked_through": "2026-07-18",
        },
        "actual_R1_atom_input_audit": actual_atom_audit,
        "shared_physical_anchor_registry": anchor_binding,
        "exact_positive_cone_product_tile": tile,
        "what_the_new_tail_does_and_does_not_supply": {
            "C24_uniform_unweighted_exponential_return_tail": True,
            "positive_full_dimensional_R1_atom_on_every_s_in_anchor_slab": True,
            "tail_event_carrier": "C24 return time",
            "stable_manifold_survival_event_carrier": "distance from all future singularity cuts",
            "the_two_events_are_identified": False,
            "C24_return_tail_implies_registered_stable_plaque_family": False,
        },
        "young_rectangle_theorem_match": {
            "qualitative_general_fact": (
                "finite-horizon planar dispersing billiards admit almost-everywhere local "
                "stable/unstable manifolds, absolutely continuous holonomy on suitable "
                "Cantor rectangles, and Young towers"
            ),
            "general_existence_is_bound_to_anchor_atom_id": False,
            "general_existence_is_bound_to_parameter_slab": False,
            "general_existence_preserves_C24_R1_branch_ids": False,
            "general_existence_supplies_explicit_tile_spanning_length": False,
            "general_existence_supplies_explicit_conditional_holonomy_Jacobian_bounds": False,
            "conclusion": (
                "general Young-rectangle existence cannot instantiate the immutable Gate2 "
                "fields on this shared physical registry without the missing carrier constants"
            ),
        },
        "minimal_missing_physical_interface": missing,
        "candidate_maturity": {
            "candidate_cone_product_layers_total": 7,
            "candidate_cone_product_layers_certified": 7,
            "layers": [
                "positive two-dimensional physical R1 anchor",
                "strict inner cone-product tile",
                "explicit cone-unstable interval I_A^cand",
                "interval-indexed cone-stable affine candidate leaves",
                "affine candidate projection pi_aff",
                "positive exact affine area disintegration rho_aff",
                "same unique physical one-step C24 return branch on the whole tile",
            ],
            "invariant_stable_product_dynamical_layers_certified": 0,
            "candidate_fraction_is_not_official_Gate2_maturity": True,
            "official_Gate2_maturity": "0/17",
        },
        "immutable_17_field_audit": {
            "schema_sha256": digest(list(GATE2_FIELDS)),
            "required_field_count": len(GATE2_FIELDS),
            "certified_field_count": 0,
            "official_Gate2_maturity": "0/17",
            "field_status": {field: "NOT_CERTIFIED" for field in GATE2_FIELDS},
            "first_missing_field": GATE2_FIELDS[0],
            "reason_no_candidate_promotion": (
                "a cone-admissible affine foliation is not an invariant physical stable "
                "foliation, and pi_aff is not pi^s"
            ),
        },
        "strict_nonpromotion": {
            "stable_saturated_product_base_Lambda_A": "NOT_CERTIFIED",
            "physical_reference_unstable_interval_I_A_on_Lambda_A": "NOT_CERTIFIED",
            "physical_stable_projection_pi_s": "NOT_CERTIFIED",
            "conditional_stable_holonomy_SRB_Jacobian": "NOT_CERTIFIED",
            "full_mass_countable_quotient_return_partition": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED",
            "Gate2_maturity": "0/17",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result = dict(core)
    result["internal_replay_digest"] = digest(core)
    return result


def main() -> int:
    print(json.dumps(build_result(), sort_keys=True, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
