#!/usr/bin/env python3
"""Fail-closed independent verifier for the round-25 Gate-2 product anchor.

The verifier never imports the producer.  It pins all inputs, replays the
actual first frozen R1 atom, reconstructs both physical core ids, and checks
the cone, area, collision-mass, and affine-disintegration arithmetic over
``Fraction``.  The seven positive rows are candidate cone-product layers;
the number of invariant stable-product dynamical layers is exactly zero and
the official immutable Gate-2 score remains 0/17.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_gate2_round25_product_base_cert.py"
MANIFEST = HERE / "cm2-gate2-round25-product-base-manifest-2026-07-18.json"
REPORT = HERE / "cm2-gate2-round25-product-base-assault-2026-07-18.md"
EXPECTED_CERTIFICATE_SHA256 = (
    "03637e41c11353807da8a0f0629b5dd74e1a4341408268c472766f6a7bac9800"
)

EXPECTED_DEPENDENCIES = {
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
SOURCE_CORE_PAYLOAD = {
    "chart_id": "G:E", "t": ["-7/10", "-69/100"],
    "p": ["-1/50", "1/50"], "target_id": "W[0,-1]", "crossings": [],
}
DESTINATION_CORE_PAYLOAD = {
    "chart_id": "W:N", "t": ["-7/10", "-69/100"],
    "p": ["-1/50", "1/50"], "target_id": "G[0,1]", "crossings": [],
}
Q = Fraction
SOURCE_RADIUS = Q(9, 25)
PARAMETER_WINDOW_WIDTH = Q(1, 200)
GLOBAL_DTHETA_DT_UPPER = Q(1401, 1000)
HEX64 = re.compile(r"^[0-9a-f]{64}$")

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

EXPECTED_ANCHOR_ROW = {
    "absolute_inverse_invariant_area_Jacobian": "1",
    "atom_id": ANCHOR_ATOM_ID,
    "canonical_invariant_area_coordinates": "(r,p=sin(phi))",
    "classification": "RETURN_AT_1_INNER",
    "classification_witness_rows_sha256": (
        "e40c7da17c703c971a17382d8850fefd7c71a7c50d5febd35dc16e034acb1792"
    ),
    "complete_retained_candidate_comparison_inherited": True,
    "depth": 14,
    "destination_core_id": DESTINATION_CORE_ID,
    "dyadic_path": "00000000100000",
    "log_invariant_area_Jacobian_distortion": "0",
    "midpoint_proposal_promoted_parent": True,
    "output_enclosures": {
        "normal_x": "[-0.69 +/- 5.68e-3]",
        "normal_y": "[0.72 +/- 3.86e-3]",
        "p_target": "[-0.01 +/- 3.85e-3]",
    },
    "parameter_averaged_unnormalized_base_mass": "9/1024000000",
    "parameter_averaged_unnormalized_collision_mass_lower": "9/1024000000",
    "parameter_averaged_unnormalized_collision_mass_upper": (
        "12609/1024000000000"
    ),
    "parent_owner_witness_sha256": (
        "320471cbe8a985447e67ad6e2ff60ff34586f62393fdee3381ced5a30bbd47a3"
    ),
    "positive_parameter_interval": True,
    "positive_two_dimensional_source_rectangle_at_each_s": True,
    "source_box": {
        "p": ["-1/50", "-3/160"],
        "s": ["-3/1600", "-1/640"],
        "t": ["-7/10", "-2239/3200"],
    },
    "source_core_id": SOURCE_CORE_ID,
    "source_core_index": 1,
    "strict_next_collision_owner_inherited_from_whole_parent_core": True,
}


class VerificationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise VerificationError(code, detail)


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "DUPLICATE_JSON_KEY", key)
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise VerificationError("NONFINITE_JSON", token)


def parse_json_text(text: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_pairs,
            parse_constant=reject_constant,
        )
    except VerificationError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise VerificationError("MALFORMED_JSON", str(exc)) from exc


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qtext(value: Q) -> str:
    return str(value)


def safe_regular_file(path: Path, code: str) -> None:
    require(path.parent.resolve() == HERE, code, f"escaped parent: {path.name}")
    require(not path.is_symlink(), code, f"symlink: {path.name}")
    require(path.is_file(), code, f"missing: {path.name}")


def load_dependency_data() -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for name, expected in EXPECTED_DEPENDENCIES.items():
        path = HERE / name
        safe_regular_file(path, "DEPENDENCY_PATH")
        require(sha256_path(path) == expected, "DEPENDENCY_HASH", name)
        if path.suffix == ".json":
            loaded[name] = parse_json_text(path.read_text(encoding="utf-8"))
    return loaded


def independent_anchor(full_core: dict[str, Any]) -> dict[str, Any]:
    result = full_core["result"]
    rows = result["adaptive_full_core_step1_raw_leaf_rows"]
    require(type(rows) is list, "R1_ROWS_TYPE")
    require(digest(rows) == FULL_RAW_LEAF_ROWS_SHA256, "R1_ROWS_DIGEST")
    require(result["adaptive_full_core_step1_registry"]["raw_leaf_rows_sha256"]
            == FULL_RAW_LEAF_ROWS_SHA256, "R1_DECLARED_DIGEST")
    chosen = [row for row in rows if row.get("atom_id") == ANCHOR_ATOM_ID]
    require(len(chosen) == 1, "R1_ATOM_UNIQUENESS")
    first_return = next(
        (row for row in rows if row.get("classification") == "RETURN_AT_1_INNER"),
        None,
    )
    require(first_return is chosen[0], "R1_FIRST_RETURN_ORDER")
    require(chosen[0] == EXPECTED_ANCHOR_ROW, "R1_ATOM_ROW")
    require(digest(chosen[0]) == ANCHOR_ATOM_ROW_SHA256, "R1_ATOM_DIGEST")
    require("core:" + digest(SOURCE_CORE_PAYLOAD) == SOURCE_CORE_ID,
            "SOURCE_CORE_ID")
    require("core:" + digest(DESTINATION_CORE_PAYLOAD) == DESTINATION_CORE_ID,
            "DESTINATION_CORE_ID")
    payload = {
        "source_core_id": SOURCE_CORE_ID,
        "dyadic_path": EXPECTED_ANCHOR_ROW["dyadic_path"],
        "source_box": EXPECTED_ANCHOR_ROW["source_box"],
    }
    require("full-core-step1:" + digest(payload) == ANCHOR_ATOM_ID,
            "R1_ATOM_ID")
    box = EXPECTED_ANCHOR_ROW["source_box"]
    t0, t1 = map(Q, box["t"])
    p0, p1 = map(Q, box["p"])
    s0, s1 = map(Q, box["s"])
    averaged = SOURCE_RADIUS * (t1-t0) * (p1-p0) * (s1-s0) / PARAMETER_WINDOW_WIDTH
    require(averaged == Q(9, 1024000000), "R1_BASE_MASS")
    require(GLOBAL_DTHETA_DT_UPPER * averaged == Q(12609, 1024000000000),
            "R1_UPPER_MASS")
    return chosen[0]


def independent_tile() -> dict[str, Any]:
    t0, t1 = Q(-7, 10), Q(-2239, 3200)
    p0, p1 = Q(-1, 50), Q(-3, 160)
    tc, pc = (t0+t1)/2, (p0+p1)/2
    a = b = Q(1, 25600)
    slope = Q(3, 2)
    tdev, pdev = a+b, slope*(a+b)
    require(tc == Q(-4479, 6400), "TILE_CENTER_T")
    require(pc == Q(-31, 1600), "TILE_CENTER_P")
    t_margin = (t1-t0)/2-tdev
    p_margin = (p1-p0)/2-pdev
    require(t_margin == Q(1, 12800) > 0, "TILE_MARGIN_T")
    require(p_margin == Q(13, 25600) > 0, "TILE_MARGIN_P")
    lower = slope*Q(7, 10)/SOURCE_RADIUS
    upper = slope/(SOURCE_RADIUS*Q(49, 50))
    stable_lower, stable_upper = Q(25, 9), Q(4108425, 145348)
    require(lower == Q(35, 12) > stable_lower, "CONE_LOWER")
    require(upper == Q(625, 147) < stable_upper, "CONE_UPPER")
    require(abs(pc)+pdev == Q(499, 25600) < Q(1, 50), "P_BOUND")
    require(1-Q(7, 10)**2 > Q(7, 10)**2, "SQRT_T")
    require(1-Q(1, 50)**2 > Q(49, 50)**2, "SQRT_P")
    require(GLOBAL_DTHETA_DT_UPPER**2*(1-Q(7, 10)**2) > 1,
            "DTHETA_BOUND")
    jacobian = Q(3)
    area = jacobian*(2*a)*(2*b)
    raw_lower = SOURCE_RADIUS*area
    normalized_lower = raw_lower/(4*Q(22, 7)*Q(13, 25))
    rho_lower = 6*SOURCE_RADIUS*b
    rho_upper = rho_lower*GLOBAL_DTHETA_DT_UPPER
    require(area == Q(3, 163840000), "AREA")
    require(raw_lower == Q(27, 4096000000), "RAW_MASS")
    require(normalized_lower == Q(189, 187432960000), "NORMALIZED_MASS")
    require(rho_lower == Q(27, 320000), "RHO_LOWER")
    require(rho_upper == Q(37827, 320000000), "RHO_UPPER")
    return {
        "product_coordinates": {
            "domain": "|u|<=1/25600, |v|<=1/25600",
            "map_to_collision_chart": (
                "t=-4479/6400+u+v; p=-31/1600+(3/2)u-(3/2)v"
            ),
            "absolute_dt_dp_over_du_dv_Jacobian": "3",
        },
        "strict_source_atom_interior": {
            "t_margin": qtext(t_margin),
            "p_margin": qtext(p_margin),
            "inside_selected_R1_atom_for_every_s_in_slab": True,
        },
        "collision_coordinate_binding": {
            "source_core_payload": dict(SOURCE_CORE_PAYLOAD),
            "source_collision_component": "G",
            "source_radius": "9/25",
            "coordinate_change": "r=R_G*asin(t), phi=asin(p)",
            "collision_area_density": "R_G/sqrt(1-t^2) dt dp",
        },
        "reference_cone_unstable_candidate": {
            "name": "I_A^cand",
            "definition": "v=0, |u|<=1/25600",
            "physical_abs_dphi_dr_strict_bounds": [qtext(lower), qtext(upper)],
            "squared_rational_witnesses": {
                "tile_abs_t_at_most": "7/10",
                "tile_abs_p_strict_upper": "499/25600<1/50",
                "sqrt_one_minus_t2_strict_lower": "51/100>49/100=(7/10)^2",
                "sqrt_one_minus_p2_strict_lower": "2499/2500>2401/2500=(49/50)^2",
            },
            "inside_frozen_unstable_cone": True,
            "is_declared_actual_unstable_manifold": False,
        },
        "interval_indexed_cone_stable_candidates": {
            "definition": "W_u^cs={u fixed, |v|<=1/25600}",
            "physical_dphi_dr_strict_bounds": [qtext(-upper), qtext(-lower)],
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
            "dt_dp_area": qtext(area),
            "unnormalized_collision_SRB_mass_strict_lower": qtext(raw_lower),
            "normalized_collision_SRB_mass_strict_lower": qtext(normalized_lower),
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


def independent_expected_result() -> dict[str, Any]:
    deps = load_dependency_data()
    gate2 = deps[GATE2]
    geometry = deps[OPEN_GEOMETRY]
    sparse = deps[SPARSE_TAIL]
    full_core = deps[FULL_CORE]
    anchor = independent_anchor(full_core)
    predecessor = gate2["result"]["Gate2_17_field_nonpromotion"]
    require(len(predecessor["field_rows"]) == 17, "PREDECESSOR_FIELDS")
    require(predecessor["completed_physical_field_count_after_round23"] == 0,
            "PREDECESSOR_SCORE")
    require(tuple(row["field"] for row in predecessor["field_rows"]) == GATE2_FIELDS,
            "PREDECESSOR_SCHEMA")
    require(geometry["result"]["stable_curve_open_hole_geometry"]
            ["certified_O2_constant_Ct"] == 1493, "O2_BINDING")
    require(geometry["result"]["frozen_core_inventory"]["core_rows_sha256"]
            == "c3042515b4a244b064f1aaef97ee236c5d3f6078a53fe3fb9e865a1976853b2f",
            "CORE_ROWS_BINDING")
    require(sparse["result"]["scheduled_and_all_time_tail"]
            ["uniform_unweighted_exponential_collision_return_tail"] == "CERTIFIED",
            "TAIL_BINDING")
    require(full_core["result"]["adaptive_full_core_step1_registry"]
            ["source_phase_dimension_at_fixed_parameter"] == 2, "PHASE_DIMENSION")
    require(full_core["result"]["provenance"]["clock"]
            == "source_core_state_is_time_0_and_next_collision_is_time_1",
            "CLOCK_BINDING")
    require(full_core["result"]["provenance"]["dependency_sha256"]
            ["cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"]
            == "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
            "CORE_PROVENANCE")

    tile = independent_tile()
    atom_audit = {
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
        "classification_witness_rows_sha256": anchor["classification_witness_rows_sha256"],
        "parameter_averaged_unnormalized_base_mass": anchor["parameter_averaged_unnormalized_base_mass"],
        "parameter_averaged_unnormalized_collision_mass_upper": anchor["parameter_averaged_unnormalized_collision_mass_upper"],
        "strict_complete_first_owner_inherited": True,
        "strict_whole_box_R1_core_membership": True,
    }
    anchor_binding = {
        "registry_id": "gate2-r25-anchor:" + digest({
            "actual_atom_audit": atom_audit,
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
            "dependency_sha256": dict(EXPECTED_DEPENDENCIES),
            "old_artifacts_modified": False,
            "arithmetic": "exact rational replay plus frozen strict Arb branch rows",
            "literature_checked_through": "2026-07-18",
        },
        "actual_R1_atom_input_audit": atom_audit,
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
            "required_field_count": 17,
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


TOP_KEYS = {
    "schema", "date", "certificate_sha256", "verifier_sha256",
    "report_sha256", "dependencies", "result", "verdict",
}
VERDICT = (
    "7/7 CANDIDATE CONE-PRODUCT LAYERS CERTIFIED; 0 INVARIANT "
    "STABLE-PRODUCT DYNAMICAL LAYERS; OFFICIAL GATE 2 0/17 NOT CERTIFIED"
)


def validate_manifest(manifest: Any, expected_result: dict[str, Any]) -> None:
    require(type(manifest) is dict, "TOP_TYPE")
    require(set(manifest) == TOP_KEYS, "TOP_KEYS")
    for key in ("schema", "date", "certificate_sha256", "verifier_sha256",
                "report_sha256", "verdict"):
        require(type(manifest[key]) is str, "FIELD_TYPE", key)
    require(type(manifest["dependencies"]) is dict, "FIELD_TYPE", "dependencies")
    require(type(manifest["result"]) is dict, "FIELD_TYPE", "result")
    require(manifest["schema"] == "cm2.gate2.round25.product-base.manifest.v1",
            "MANIFEST_SCHEMA")
    require(manifest["date"] == "2026-07-18", "DATE")
    for key in ("certificate_sha256", "verifier_sha256", "report_sha256"):
        require(HEX64.fullmatch(manifest[key]) is not None, "MALFORMED_SHA", key)
    require(manifest["certificate_sha256"] == EXPECTED_CERTIFICATE_SHA256,
            "CERTIFICATE_PIN")
    require(manifest["dependencies"] == EXPECTED_DEPENDENCIES, "DEPENDENCY_MAP")
    require(canonical_bytes(manifest["result"]) == canonical_bytes(expected_result),
            "RESULT_MISMATCH")
    require(manifest["verdict"] == VERDICT, "VERDICT")


def load_and_validate() -> tuple[dict[str, Any], dict[str, Any]]:
    require(sys.flags.optimize == 0, "OPTIMIZED_PYTHON")
    for path, code in (
        (CERTIFICATE, "CERTIFICATE_PATH"),
        (MANIFEST, "MANIFEST_PATH"),
        (REPORT, "REPORT_PATH"),
        (Path(__file__).resolve(), "VERIFIER_PATH"),
    ):
        safe_regular_file(path, code)
    require(sha256_path(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256,
            "CERTIFICATE_HASH")
    expected = independent_expected_result()
    manifest = parse_json_text(MANIFEST.read_text(encoding="utf-8"))
    validate_manifest(manifest, expected)
    require(sha256_path(CERTIFICATE) == manifest["certificate_sha256"],
            "CERTIFICATE_HASH")
    require(sha256_path(Path(__file__).resolve()) == manifest["verifier_sha256"],
            "VERIFIER_HASH")
    require(sha256_path(REPORT) == manifest["report_sha256"], "REPORT_HASH")
    require(sha256_path(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256,
            "CERTIFICATE_REHASH")
    for name, expected_hash in EXPECTED_DEPENDENCIES.items():
        require(sha256_path(HERE / name) == expected_hash, "DEPENDENCY_REHASH", name)
    return manifest, expected


def mutate_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def run_self_test(valid: dict[str, Any], expected: dict[str, Any]) -> int:
    tests: list[tuple[str, str, Callable[[dict[str, Any]], None]]] = []

    def add(name: str, code: str, fn: Callable[[dict[str, Any]], None]) -> None:
        tests.append((name, code, fn))

    add("remove top key", "TOP_KEYS", lambda x: x.pop("date"))
    add("extra top key", "TOP_KEYS", lambda x: x.update(extra=False))
    add("replace top shape", "TOP_KEYS", lambda x: x.clear() or x.update({"x": 1}))
    add("schema", "MANIFEST_SCHEMA", lambda x: x.update(schema="v2"))
    add("date", "DATE", lambda x: x.update(date="2026-07-17"))
    add("cert malformed", "MALFORMED_SHA", lambda x: x.update(certificate_sha256="0"))
    add("verifier malformed", "MALFORMED_SHA", lambda x: x.update(verifier_sha256="g"*64))
    add("report malformed", "MALFORMED_SHA", lambda x: x.update(report_sha256=""))
    add("cert changed", "CERTIFICATE_PIN", lambda x: x.update(certificate_sha256="0"*64))
    add("dependencies list", "FIELD_TYPE", lambda x: x.update(dependencies=[]))
    add("dependency missing", "DEPENDENCY_MAP", lambda x: x["dependencies"].pop(next(iter(x["dependencies"]))))
    add("dependency extra", "DEPENDENCY_MAP", lambda x: x["dependencies"].update({"../escape": "0"*64}))
    add("dependency changed", "DEPENDENCY_MAP", lambda x: x["dependencies"].update({next(iter(x["dependencies"])): "0"*64}))
    add("result list", "FIELD_TYPE", lambda x: x.update(result=[]))
    add("result missing key", "RESULT_MISMATCH", lambda x: x["result"].pop("candidate_maturity"))
    add("result extra key", "RESULT_MISMATCH", lambda x: x["result"].update(extra=False))

    mutations: list[tuple[str, tuple[Any, ...], Any]] = [
        ("raw rows digest", ("result", "actual_R1_atom_input_audit", "full_raw_leaf_rows_sha256"), "0"*64),
        ("selected row digest", ("result", "actual_R1_atom_input_audit", "selected_raw_row_sha256"), "0"*64),
        ("first R1 false", ("result", "actual_R1_atom_input_audit", "selected_is_first_RETURN_AT_1_INNER_row"), False),
        ("atom id replay false", ("result", "actual_R1_atom_input_audit", "atom_id_payload_replayed"), False),
        ("source component", ("result", "actual_R1_atom_input_audit", "source_component_and_radius", "component"), "W"),
        ("source radius", ("result", "actual_R1_atom_input_audit", "source_component_and_radius", "radius"), "4/25"),
        ("source core id", ("result", "actual_R1_atom_input_audit", "source_core_payload_id"), DESTINATION_CORE_ID),
        ("destination core id", ("result", "actual_R1_atom_input_audit", "destination_core_payload_id"), SOURCE_CORE_ID),
        ("source box", ("result", "actual_R1_atom_input_audit", "source_box", "t", 1), "-69/100"),
        ("dyadic path", ("result", "actual_R1_atom_input_audit", "dyadic_path"), "00000000100001"),
        ("classification", ("result", "actual_R1_atom_input_audit", "classification"), "SURVIVE_THROUGH_1_INNER"),
        ("owner false", ("result", "actual_R1_atom_input_audit", "strict_complete_first_owner_inherited"), False),
        ("whole R1 false", ("result", "actual_R1_atom_input_audit", "strict_whole_box_R1_core_membership"), False),
        ("registry id", ("result", "shared_physical_anchor_registry", "registry_id"), "gate2-r25-anchor:"+"0"*64),
        ("branch class", ("result", "shared_physical_anchor_registry", "physical_branch_class"), "UNKNOWN"),
        ("whole tile R1", ("result", "shared_physical_anchor_registry", "whole_tile_has_same_unique_next_collision_and_returns_to_C24_at_time_1"), False),
        ("tile domain", ("result", "exact_positive_cone_product_tile", "product_coordinates", "domain"), "|u|<=1"),
        ("tile jacobian", ("result", "exact_positive_cone_product_tile", "product_coordinates", "absolute_dt_dp_over_du_dv_Jacobian"), "1"),
        ("t margin", ("result", "exact_positive_cone_product_tile", "strict_source_atom_interior", "t_margin"), "0"),
        ("radius binding", ("result", "exact_positive_cone_product_tile", "collision_coordinate_binding", "source_radius"), "4/25"),
        ("unstable cone false", ("result", "exact_positive_cone_product_tile", "reference_cone_unstable_candidate", "inside_frozen_unstable_cone"), False),
        ("unstable promoted", ("result", "exact_positive_cone_product_tile", "reference_cone_unstable_candidate", "is_declared_actual_unstable_manifold"), True),
        ("stable promoted", ("result", "exact_positive_cone_product_tile", "interval_indexed_cone_stable_candidates", "actual_local_stable_manifolds_certified"), True),
        ("stable invariant", ("result", "exact_positive_cone_product_tile", "interval_indexed_cone_stable_candidates", "forward_invariance_certified"), True),
        ("projection promoted", ("result", "exact_positive_cone_product_tile", "affine_candidate_projection", "identified_with_physical_stable_holonomy_pi_s"), True),
        ("area", ("result", "exact_positive_cone_product_tile", "positive_collision_area", "dt_dp_area"), "0"),
        ("normalized mass", ("result", "exact_positive_cone_product_tile", "positive_collision_area", "normalized_collision_SRB_mass_strict_lower"), "0"),
        ("rho bound", ("result", "exact_positive_cone_product_tile", "affine_area_disintegration_only", "rho_aff_strict_bounds", 0), "0"),
        ("rho promoted", ("result", "exact_positive_cone_product_tile", "affine_area_disintegration_only", "is_conditional_stable_holonomy_SRB_Jacobian"), True),
        ("tail identified", ("result", "what_the_new_tail_does_and_does_not_supply", "the_two_events_are_identified"), True),
        ("tail implies plaques", ("result", "what_the_new_tail_does_and_does_not_supply", "C24_return_tail_implies_registered_stable_plaque_family"), True),
        ("general theorem bound", ("result", "young_rectangle_theorem_match", "general_existence_is_bound_to_anchor_atom_id"), True),
        ("candidate total", ("result", "candidate_maturity", "candidate_cone_product_layers_total"), 8),
        ("candidate positive", ("result", "candidate_maturity", "candidate_cone_product_layers_certified"), 8),
        ("invariant layer promoted", ("result", "candidate_maturity", "invariant_stable_product_dynamical_layers_certified"), 1),
        ("candidate official", ("result", "candidate_maturity", "candidate_fraction_is_not_official_Gate2_maturity"), False),
        ("candidate score", ("result", "candidate_maturity", "official_Gate2_maturity"), "7/17"),
        ("field count", ("result", "immutable_17_field_audit", "certified_field_count"), 1),
        ("field score", ("result", "immutable_17_field_audit", "official_Gate2_maturity"), "1/17"),
        ("field promoted", ("result", "immutable_17_field_audit", "field_status", GATE2_FIELDS[0]), "CERTIFIED"),
        ("Gate2 promoted", ("result", "strict_nonpromotion", "Gate2"), "CERTIFIED"),
        ("Gate2 score", ("result", "strict_nonpromotion", "Gate2_maturity"), "7/17"),
        ("CM2 promoted", ("result", "strict_nonpromotion", "CM2"), "GO"),
        ("old modified", ("result", "provenance", "old_artifacts_modified"), True),
        ("digest stale", ("result", "internal_replay_digest"), "0"*64),
    ]
    for name, path, replacement in mutations:
        add(name, "RESULT_MISMATCH",
            lambda x, p=path, r=replacement: mutate_path(x, p, r))
    add("verdict", "VERDICT", lambda x: x.update(verdict="GATE 2 CERTIFIED"))

    passed = 0
    for name, expected_code, mutation in tests:
        candidate = deepcopy(valid)
        mutation(candidate)
        try:
            validate_manifest(candidate, expected)
        except VerificationError as exc:
            require(exc.code == expected_code, "SELF_TEST_WRONG_CODE",
                    f"{name}: {exc.code} != {expected_code}")
            passed += 1
        else:
            raise VerificationError("SELF_TEST_ACCEPTED", name)

    for malformed, code in (
        ('{"schema":"x","schema":"y"}', "DUPLICATE_JSON_KEY"),
        ('{"x":NaN}', "NONFINITE_JSON"),
        ('{"x":Infinity}', "NONFINITE_JSON"),
        ('{"x":-Infinity}', "NONFINITE_JSON"),
        ('{"x":1} trailing', "MALFORMED_JSON"),
    ):
        try:
            parse_json_text(malformed)
        except VerificationError as exc:
            require(exc.code == code, "SELF_TEST_WRONG_CODE", malformed)
            passed += 1
        else:
            raise VerificationError("SELF_TEST_ACCEPTED", malformed)
    print(f"SELF-TEST PASS: {passed}/{passed} hostile mutations rejected")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--integrity-only", action="store_true")
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not (args.integrity_only or args.replay or args.self_test):
        print("LIVE VERDICT: Gate 2 NOT_CERTIFIED; official score 0/17 (fail-closed)")
        return 2
    try:
        manifest, expected = load_and_validate()
        if args.self_test:
            run_self_test(manifest, expected)
        elif args.replay:
            print("REPLAY PASS: actual R1 atom, core ids, cone tile, area/mass/rho, 0/17 boundary")
        else:
            print("INTEGRITY PASS: certificate, dependencies, report, verifier, manifest")
        return 0
    except VerificationError as exc:
        print(f"VERIFY FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
