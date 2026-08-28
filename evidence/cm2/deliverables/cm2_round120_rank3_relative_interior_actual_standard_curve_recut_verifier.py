#!/usr/bin/env python3
"""Independent verifier for the Round120 grazing parent-W child registry.

The verifier intentionally does not import the Round120 producer.  At 1024
bits it rebuilds every one of the 72 Round113/117 parent joins from the older
geometry modules, recomputes the fixed-intercept derivative, checks the
HIT/BYPASS 424/480 monotonicity bounds, replays the three official owners, and
reconstructs every adapted-recut and Gate5 F1--F6 slot-schema row.

The result is a parameterized Borel registry.  It is not a finite enumeration
of children, does not install F7--F18, and does not change global Gate5 10/18.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as component
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
import cm2_round113_rank3_root_sheet_owner_ordering_spike as round113
from cm2_round76_r2_numeric_fields_generator import aq, interval
from cm2_round79_tangency_intersection_generator import strict_sign


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = (
    HERE
    / "cm2-round120-rank3-relative-interior-actual-standard-curve-recut-2026-07-23.json"
)
CERTIFICATE_SCHEMA = (
    "cm2.round120.rank3-relative-interior-actual-standard-curve-recut.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round120.rank3-relative-interior-actual-standard-curve-recut-verification.v1"
)
VERIFIER_PRECISION_BITS = 1024

ROUND112 = HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json"
ROUND113 = HERE / "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
ROUND117 = HERE / "cm2-round117-rank3-countable-homogeneity-operator-cells-2026-07-23.json"
ROUND118 = HERE / "cm2-round118-rank3-repaired-endpoint-source-cylinder-transfer-atlas-2026-07-23.json"
ROUND119 = HERE / "cm2-round119-rank3-eight-grazing-trace-extended-cylinder-reach-2026-07-23.json"
ROUND31 = HERE / "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json"
ROUND35 = HERE / "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
CONE = HERE / "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
UNIVERSAL = HERE / "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
ROUND47 = HERE / "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json"
ROUND50 = HERE / "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
GATE5 = HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"

UPSTREAM_PINS = {
    ROUND112.name: "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5",
    ROUND113.name: "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181",
    ROUND117.name: "31b6535e21886d825d5a4658f2c9d3ccc8c5525c2b9d2fb181f88baa7dcf9eb0",
    ROUND118.name: "91bd73445fd13eeb759e932b0626ba64acef1f10a061d6d416577dfd96feb34f",
    ROUND119.name: "9ff985c91472e0ef57ced9fc10dbb6b2aa9e9627a5ac94c999caeefeca29a749",
    ROUND31.name: "fa654b2c852f2b89e6e85a457f7ec7689dc56b7ccc9582d994db6b2e269bfb74",
    ROUND35.name: "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c",
    CONE.name: "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9",
    UNIVERSAL.name: "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b",
    ROUND47.name: "79eeff7d5c18ec7d28a30c61ae857a733b3136202917c54f6aeaf93d7f414089",
    ROUND50.name: "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73",
    GATE5.name: "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2_round113_rank3_root_sheet_owner_ordering_spike.py": (
        "2263d213bad42163da326c892662f500f29a3c5f6cf4b8ba28cc2bb57990b11e"
    ),
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": (
        "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2_gate25_roof_two_wall_chart_frontier_cert.py": (
        "153e64610404eb4035d3bc019f1eb19e5dc72c577c2de0b7309344ec33ce15f1"
    ),
    "cm2_gate25_selected_component_chart_field_slots_cert.py": (
        "666e7f1ea4198528b143b522d2c5daf55ba4fecfd127d86663b23e0bb38a477f"
    ),
    "cm2_round76_r2_numeric_fields_generator.py": (
        "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf"
    ),
    "cm2_round79_tangency_intersection_generator.py": (
        "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7"
    ),
    "cm2_gate34_round47_postcut_dyadic_recovery_cert.py": (
        "378f50e56c76e80c5d571eb52c99d708710a8b8b0238c8b8024643e6dfdeeca9"
    ),
    "cm2_gate34_round50_physical_whole_family_grouping_cert.py": (
        "f0e95a2756383ee23aa2d6a5df3b5d453b497df8500df7fdddf96096e900a809"
    ),
    "cm2_gate25_universal_operator_endpoint_template_frontier_cert.py": (
        "254a4cc0b26fc12565e8816d9a09a946079114d774f87254f99e448f87a91944"
    ),
    "cm2_gate5_return_word_three_norm_frontier_cert.py": (
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695"
    ),
    "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py": (
        "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6"
    ),
}
for _name, _expected in {
    **round113.PINS,
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
    "cm2_round78_tangency_curve_generator.py": (
        "cc9da9d607bbe19c54ffccfd4974b37eb96459f0c4ed9e70d7a68e732f625d85"
    ),
}.items():
    if _name in UPSTREAM_PINS:
        require_pin = UPSTREAM_PINS[_name] == _expected
        if not require_pin:
            raise RuntimeError(f"inconsistent verifier runtime pin:{_name}")
    UPSTREAM_PINS[_name] = _expected
EXTRA_HELPER_PINS: dict[str, str] = {}
UPSTREAM_SCHEMAS = {
    ROUND112.name: "cm2.round112.rank3-double-grazing-two-sided-root-sheet.v1",
    ROUND113.name: "cm2.round113.rank3-endpoint-sheet-owner-ordering.v1",
    ROUND117.name: "cm2.round117.rank3-countable-homogeneity-operator-cells.v1",
    ROUND118.name: "cm2.round118.rank3-repaired-endpoint-source-cylinder-transfer-atlas.v1",
    ROUND119.name: "cm2.round119.rank3-eight-grazing-trace-extended-cylinder-reach.v1",
}

SOURCE_RADIUS = Q(9, 25)
SOURCE_CURVATURE = Q(25, 9)
SOURCE_ADAPTED_DENSITY = Q(61, 9)
CANONICAL_SLOPE = Q(4)
CANONICAL_ADAPTED_LENGTH = "1e-90"
THETA = Q(144000, 180337)
ONE_STEP_LOG_VARIATION = Q(3, 200000)
THREE_STEP_THETA = THETA**3
THREE_STEP_LOG_VARIATION = 3 * ONE_STEP_LOG_VARIATION
OUTER = Q(1, 16384)
CHART_ORIENTATION = {"E": 1, "N": -1, "W": -1, "S": 1}
CANONICAL_ANGULAR_LIFT = {
    "E": "asin(t)",
    "N": "pi/2-asin(t)",
    "W": "pi-asin(t)",
    "S": "-pi/2+asin(t)",
}
GATE5_FIELDS = (
    "nonempty_or_empty_domain_proof",
    "physical_homogeneity_subbranch_table",
    "homogeneous_prefix_chart",
    "homogeneous_suffix_chart",
    "inverse_Jacobian_bound",
    "log_Jacobian_distortion_sum",
)
INSTALLED_GATE5_FIELDS = GATE5_FIELDS[:4]
CARRIER_CHILD_ID_SCHEMA = (
    "(round120-child-v1,typed-parent-W-id,"
    "round117-operator-cell-id(active-labels),source-interval-rank,"
    "source-adapted-index-k,connected-rank-0)"
)

RESULT_KEYS = {
    "precision_bits",
    "round113_parent_proof_box_count",
    "round117_generator_family_template_count",
    "official_candidate_registry_rows_sha256",
    "actual_parent_W_registry_contract",
    "typed_Borel_locator_precedent",
    "Round31_compact_Q2_parent_W_domain_reused",
    "Round31_compact_Q2_source_abs_momentum_upper",
    "Round120_grazing_source_momentum_square_certified_lower",
    "Round31_and_Round120_physical_source_domains_strictly_disjoint",
    "parameterized_actual_child_registry_installed",
    "finite_actual_child_count_claimed",
    "actual_child_registry_cardinality",
    "nonvacuous_actual_child_fibre_existence",
    "nonempty_or_empty_intersection_theorem",
    "child_generator_rows",
    "child_generator_rows_sha256",
    "canonical_three_step_recut_frontier",
    "owner_candidate_replay_counts",
    "uninstalled_actual_child_F5_F6_frontier",
    "gate5_actual_child_field_status",
    "rank3_actual_child_field_maturity",
    "gate5_global_maturity",
    "complete_18_field_block_count",
    "gate5_block_count",
    "cm2_verdict",
    "natural_boundary_ledger",
    "strict_scope",
    "strict_nonclaims",
    "upstream_and_helper_pins",
}
ROW_KEYS = {
    "parent_round113_cell_id",
    "parent_round113_sheet_id",
    "round117_generator_family_digest",
    "round117_generator_contract_rows",
    "sheet_kind",
    "branch_key",
    "repaired_endpoint_id",
    "exterior_port_id",
    "source_chart",
    "source_grazing_sign_sigma0",
    "parameter_box",
    "official_path_id",
    "official_word_key_ids",
    "ordered_owner_ids",
    "actual_third_collision_contract",
    "canonical_parent_W_leaf",
    "boundary_owner_conjunction",
    "squared_third_coordinate",
    "squared_third_coordinate_derivative_sign",
    "squared_third_coordinate_derivative_abs_strict_lower",
    "squared_third_coordinate_derivative_abs_strict_upper",
    "empty_or_one_connected_interval_for_every_fixed_b_and_active_generator",
    "connected_rank",
    "natural_boundaries_excluded",
    "first_collision_cosine_strict_lower",
    "second_collision_cosine_strict_lower",
    "first_and_second_collision_homogeneity",
    "minimum_selected_collision_chart_dominance_strict_lower",
    "parameterized_actual_child_id_schema",
    "typed_Borel_locator_contract",
    "parameterized_component_rank",
    "positive_length_proof_required_before_child_emission",
    "three_step_adapted_recut_frontier_schema_rows",
    "three_step_adapted_recut_frontier_schema_rows_sha256",
    "actual_image_recut_instance_rows",
    "actual_image_recut_instance_count",
    "gate5_F1_F4_slot_schema_rows",
    "gate5_F1_F4_slot_schema_rows_sha256",
    "gate5_F1_F4_slot_schema_template_count",
    "gate5_actual_child_field_status",
    "candidate_three_step_F5_template_not_installed",
    "candidate_three_step_F6_template_not_installed",
}
LEAF_KEYS = {
    "fixed_system_parameter_s",
    "equation",
    "intercept_on_this_sheet",
    "angular_lift_id",
    "canonical_theta_source_chart_of_t",
    "angular_lift_additive_2pi_index",
    "source_chart_theta_derivative_sign",
    "B_t_sign",
    "B_c_sign",
    "dt_dc_at_fixed_b_sign",
    "abs_B_t_strict_lower",
    "abs_B_c_strict_lower",
    "abs_dt_dc_strict_lower",
    "abs_dt_dc_strict_upper",
}
THIRD_COLLISION_KEYS = {
    "owner_id",
    "homogeneity_label_or_parameter",
    "BYPASS_actual_winner_H0_whole_parent",
    "BYPASS_actual_winner_cosine_minus_b128_enclosure",
    "BYPASS_b3_is_collision_angle",
    "BYPASS_b3_homogeneity_index",
}
BOUNDARY_OWNER_KEYS = {
    "priority_1_natural",
    "priority_2_round113_dyadic",
    "priority_3_round117_homogeneity",
    "priority_4_source_adapted",
    "coincident_artificial_boundaries_use_the_conjunction_of_all_unique_owner_rules",
    "natural_boundary_always_overrides_artificial_ownership",
}
TYPED_LOCATOR_KEYS = {
    "intercept_parameter",
    "source_interval_rank",
    "component_rank",
    "angular_lift_id",
    "same_canonical_angular_lift_used_in_intercept_b",
    "locator_validity",
    "dyadic_endpoint_representation",
    "analytic_boundary_equality",
    "total_computable_real_comparison_oracle_claimed",
    "Arb_or_decimal_text_in_stable_ID",
    "typed_parent_W_tuple",
}
NATURAL_PRIORITY_KEYS = {
    "source_c0_zero_owned_by_singular_ledger",
    "third_coordinate",
    "third_coordinate_zero_owned_by_singular_ledger",
    "regular_child_owns_either_natural_boundary",
    "logical_relation",
}
ROOF_CHART_PAIR_KEYS = {
    "roof_level_j",
    "prefix_chart",
    "suffix_chart",
    "transparent_wall_token",
}
SLOT_SAMPLE_KEYS = {
    "homogeneous_subbranch_id",
    "slot_id",
    "sample_is_an_ID_API_test_not_a_nonempty_claim",
}
GENERATOR_KEYS = {
    "family",
    "source_label_domain",
    "third_label_domain",
    "active_intersection_predicate",
    "cardinality",
    "stable_id_interface_sample",
}
RECUT_KEYS = {
    "parent_round113_cell_id",
    "stage",
    "official_word_key_id",
    "source_chart",
    "target_chart",
    "target_owner_id",
    "clean_wall_records",
    "roof_level_count",
    "roof_level_domain",
    "roof_level_chart_pairs",
    "adapted_coordinate",
    "natural_rule",
    "candidate_actual_instance_key",
    "actual_instance_materialized",
    "candidate_one_step_F5_template_not_installed",
    "candidate_one_step_F6_template_not_installed",
    "recut_rule_id",
}
SLOT_KEYS = {
    "generator_family",
    "label_parameter_domains",
    "official_word_key_id",
    "homogeneous_subbranch_id_schema",
    "roof_level_j",
    "field_index",
    "field_name",
    "field_value_or_contract",
    "immutable_slot_key_schema",
    "slot_status",
    "recut_schema_row_id",
    "carrier_child_id_schema",
    "parameterized_slot_id_constructor",
    "stable_ID_interface_sample",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_integer(token: str) -> int:
    if token == "-0":
        raise ValueError("negative zero")
    if len(token.lstrip("-")) > 1024:
        raise ValueError("oversized integer")
    return int(token)


def reject_surrogates(value: Any) -> None:
    if type(value) is str:
        require(
            not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            "unpaired surrogate",
        )
    elif type(value) is list:
        for item in value:
            reject_surrogates(item)
    elif type(value) is dict:
        for key, item in value.items():
            reject_surrogates(key)
            reject_surrogates(item)


def strict_json(text: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_int=strict_integer,
        parse_float=lambda token: (_ for _ in ()).throw(
            ValueError(f"float forbidden: {token}")
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"constant forbidden: {token}")
        ),
    )
    require(type(value) is dict, "top-level object")
    reject_surrogates(value)
    return value


def qvalue(value: Any, label: str) -> Q:
    require(type(value) is str and value != "", f"{label}:rational string")
    try:
        parsed = Q(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise RuntimeError(f"{label}:invalid rational") from exc
    require(value == str(parsed), f"{label}:noncanonical rational")
    return parsed


def exact_dyadic(point: arb) -> Q:
    mantissa, exponent = point.man_exp()
    return Q(int(mantissa)) * Q(2) ** int(exponent)


def arb_pair(value: arb) -> tuple[Q, Q]:
    return exact_dyadic(value.lower()), exact_dyadic(value.upper())


def abs_bounds(value: arb, label: str) -> tuple[Q, Q]:
    lower, upper = arb_pair(value)
    if lower > 0:
        return lower, upper
    if upper < 0:
        return -upper, -lower
    raise RuntimeError(f"{label}:zero in interval")


def load_closed(path: Path) -> dict[str, Any]:
    document = strict_json(path.read_text(encoding="utf-8"))
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"{path.name}:closed envelope",
    )
    require(document["schema"] == UPSTREAM_SCHEMAS[path.name], f"{path.name}:schema")
    require(type(document["result"]) is dict, f"{path.name}:result")
    require(document["result_sha256"] == digest(document["result"]), f"{path.name}:digest")
    return document["result"]


def load_inputs() -> dict[str, Any]:
    for name, expected in {**UPSTREAM_PINS, **EXTRA_HELPER_PINS}.items():
        require(sha256(HERE / name) == expected, f"pin mismatch:{name}")
    values = {
        "r112": load_closed(ROUND112),
        "r113": load_closed(ROUND113),
        "r117": load_closed(ROUND117),
        "r118": load_closed(ROUND118),
        "r119": load_closed(ROUND119),
        "r31": strict_json(ROUND31.read_text(encoding="utf-8")),
        "r35": strict_json(ROUND35.read_text(encoding="utf-8")),
        "cone": strict_json(CONE.read_text(encoding="utf-8")),
        "universal": strict_json(UNIVERSAL.read_text(encoding="utf-8")),
        "r47": strict_json(ROUND47.read_text(encoding="utf-8")),
        "r50": strict_json(ROUND50.read_text(encoding="utf-8")),
        "gate5": strict_json(GATE5.read_text(encoding="utf-8")),
    }
    require(values["r113"]["certified_parameter_cell_count"] == 72, "R113 count")
    require(values["r113"]["residual_parameter_cell_count"] == 0, "R113 residual")
    require(values["r117"]["round113_parent_proof_box_count"] == 72, "R117 count")
    require(
        values["r117"]["finite_generator_family_template_instance_count"] == 112,
        "R117 family count",
    )
    require(values["r118"]["repaired_endpoint_identity_count"] == 8, "R118 IDs")
    require(
        values["r119"]["certified_per_trace_ambient_extended_cosine_master_reach_count"]
        == 8,
        "R119 reach",
    )
    return values


def verify_inherited_contracts(values: dict[str, Any]) -> dict[str, Any]:
    old = values["r31"]["result"]["Q2_parent_W_Borel_registry"]
    require(old["actual_parent_W_registry"] == "CERTIFIED_PARAMETERIZED", "R31 precedent")
    borel = values["r35"]["result"]["arbitrary_Rn_parent_W_Borel_registry"]
    require(
        borel["registry_type"]
        == "standard-Borel parameterized actual curve registry",
        "R35 Borel precedent",
    )
    require(
        borel["source_interval_rank"].startswith(
            "least rational-dyadic interval basis index"
        ),
        "R35 locator precedent",
    )
    cone = values["cone"]["result"]["global_invariant_geometric_cone"]
    require(qvalue(cone["curvature_lower"], "cone curvature") == SOURCE_CURVATURE, "cone curvature")
    require(qvalue(cone["cone_upper"], "cone upper") > CANONICAL_SLOPE, "cone slope")
    require(cone["strict_forward_invariance"] is True, "cone invariance")
    universal = values["universal"]["result"]["universal_full_collision_branch_templates"]
    require(
        universal["canonical_adapted_length_upper"] == CANONICAL_ADAPTED_LENGTH,
        "universal adapted length",
    )
    require(
        qvalue(
            universal["field_5_inverse_Jacobian_seed"][
                "universal_adapted_inverse_strict_upper"
            ],
            "universal F5",
        )
        == THETA,
        "universal F5",
    )
    require(
        qvalue(
            universal["field_6_log_Jacobian_distortion_seed"][
                "canonical_curve_log_variation_strict_upper"
            ],
            "universal F6",
        )
        == ONE_STEP_LOG_VARIATION,
        "universal F6",
    )
    correction = values["r47"]["result"]["corrected_adapted_source_cell_registry"]
    require(
        correction["status"] == "CERTIFIED_CORRECTED_ADAPTED_SOURCE_CELL_SCHEMA",
        "R47 status",
    )
    require(
        correction["Round31_Euclidean_cell_bound_not_reused_as_adapted"] is True,
        "R47 metric correction",
    )
    ownership = values["r50"]["result"]["physical_Borel_whole_family_grouping"]
    require(ownership["physical_full_registry_reconstructed"] is True, "R50 registry")
    require(
        ownership["half_open_endpoint_owner"].startswith(
            "use oriented half-open natural cells"
        ),
        "R50 half-open ownership",
    )
    fields = values["gate5"]["result"]["required_operator_field_schema"][
        "required_fields"
    ]
    require(type(fields) is list and len(fields) == 18, "Gate5 fields")
    require(tuple(fields[:6]) == GATE5_FIELDS, "Gate5 F1-F6 order")
    return {
        "old": old,
        "borel": borel,
        "cone": cone,
        "universal": universal,
        "correction": correction,
        "ownership": ownership,
        "fields": fields,
    }


def indexes(values: dict[str, Any]) -> dict[str, Any]:
    sheets112 = {row["sheet_id"]: row for row in values["r112"]["sheet_rows"]}
    parents: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for sheet in values["r113"]["sheet_rows"]:
        for parent in sheet["certified_cells"]:
            require(parent["cell_id"] not in parents, "duplicate R113 parent")
            parents[parent["cell_id"]] = (sheet, parent)
    rows117 = {
        row["parent_round113_cell_id"]: row
        for row in values["r117"]["common_refinement_rows"]
    }
    repaired: dict[tuple[str, tuple[Any, ...]], dict[str, Any]] = {}
    for row in values["r118"]["repaired_endpoint_rows"]:
        branch = tuple(row["branch_key"])
        for kind in ("HIT", "BYPASS"):
            repaired[(kind, branch)] = row
    require(len(sheets112) == 16, "R112 sheet index")
    require(len(parents) == 72 and len(rows117) == 72, "parent indexes")
    require(len(repaired) == 16, "repaired index")
    pair_index, pattern_index, registry_digest = component.key_index_tables()
    return {
        "sheets112": sheets112,
        "parents": parents,
        "rows117": rows117,
        "repaired": repaired,
        "pair_index": pair_index,
        "pattern_index": pattern_index,
        "registry_digest": registry_digest,
        "cores": core_cert.physical_cores(),
    }


def expected_generator_contract(generators: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "family": row["family"],
            "source_label_domain": row["source_label_domain"],
            "third_label_domain": row.get(
                "third_label_domain", row.get("actual_third_collision_class")
            ),
            "active_intersection_predicate": row.get(
                "active_intersection_predicate",
                row.get("source_active_intersection_predicate"),
            ),
            "cardinality": row["cardinality"],
            "stable_id_interface_sample": row["stable_id_interface_sample"],
        }
        for row in generators
    ]


def transparent_wall_chart(token: str) -> str:
    require(token in {"X+", "X-", "Y+", "Y-"}, "transparent wall token")
    wall_index = 1 if token[1] == "+" else 0
    if token[0] == "X":
        return f"transparent-wall:x={wall_index}:(z=y, eta=u_y)"
    return f"transparent-wall:y={wall_index}:(z=x, eta=u_x)"


def roof_level_chart_pairs(
    source_chart: str,
    target_chart: str,
    clean_walls: list[str],
    roof: int,
) -> list[dict[str, Any]]:
    require(roof == len(clean_walls) + 1, "roof/wall count")
    source = f"collision:{source_chart}"
    target = f"collision:{target_chart}"
    if not clean_walls:
        return [
            {
                "roof_level_j": 0,
                "prefix_chart": source,
                "suffix_chart": target,
                "transparent_wall_token": None,
            }
        ]
    require(len(clean_walls) == 1 and roof == 2, "rank3 roof-two")
    wall = transparent_wall_chart(clean_walls[0])
    return [
        {
            "roof_level_j": 0,
            "prefix_chart": source,
            "suffix_chart": wall,
            "transparent_wall_token": clean_walls[0],
        },
        {
            "roof_level_j": 1,
            "prefix_chart": wall,
            "suffix_chart": target,
            "transparent_wall_token": clean_walls[0],
        },
    ]


def expected_recut_rows(
    fresh: dict[str, Any], parent_id: str
) -> list[dict[str, Any]]:
    owners = fresh["ordered_regular_relative_interior_owner_ids"]
    words = fresh["official_word_key_ids"]
    rows: list[dict[str, Any]] = []
    for stage in range(3):
        word = fresh["leg_audits"][stage]["official_word_key"]
        require(
            word["row"][1][0] == owners[stage][0],
            "official target species",
        )
        target_chart = (
            f"{word['row'][1]}:"
            f"{fresh['leg_audits'][stage]['selected_collision_chart']}"
        )
        clean_walls = word["row"][2]
        roof = word["row"][3]
        payload = {
            "parent_round113_cell_id": parent_id,
            "stage": stage,
            "official_word_key_id": words[stage],
            "source_chart": word["row"][0],
            "target_chart": target_chart,
            "target_owner_id": owners[stage],
            "clean_wall_records": clean_walls,
            "roof_level_count": roof,
            "roof_level_domain": f"0<=roof_level_j<{roof}",
            "roof_level_chart_pairs": roof_level_chart_pairs(
                word["row"][0], target_chart, clean_walls, roof
            ),
            "adapted_coordinate": "u_i(x)=integral_(x_left)^x (kappa_i+V_i) dr",
            "natural_rule": (
                "half-open [j*1e-90,(j+1)*1e-90), clipped at the last "
                "endpoint which is closed"
            ),
            "candidate_actual_instance_key": (
                "(round120-child-id,stage,natural-adapted-index-j)"
            ),
            "actual_instance_materialized": False,
            "candidate_one_step_F5_template_not_installed": str(THETA),
            "candidate_one_step_F6_template_not_installed": str(
                ONE_STEP_LOG_VARIATION
            ),
        }
        rows.append(
            {
                **payload,
                "recut_rule_id": (
                    f"round120-recut-rule:step{stage}:" + digest(payload)
                ),
            }
        )
    return rows


def expected_slot_rows(
    generators: list[dict[str, Any]], recuts: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for generator in generators:
        family = generator["family"]
        source_domain = generator["source_label_domain"]
        third_domain = generator.get(
            "third_label_domain",
            generator.get("actual_third_collision_class"),
        )
        subbranch = (
            "round117-operator-cell-id(active-labels); this inherited immutable "
            f"ID is the Round120 homogeneous-subbranch ID for family {family}"
        )
        carrier_child = CARRIER_CHILD_ID_SCHEMA
        homogeneity = (
            f"source={source_domain}; collision1=H0_CENTRAL; "
            f"collision2=H0_CENTRAL; actual-collision3={third_domain}"
        )
        for recut in recuts:
            for roof_level in range(recut["roof_level_count"]):
                chart_pair = recut["roof_level_chart_pairs"][roof_level]
                require(
                    chart_pair["roof_level_j"] == roof_level,
                    "roof chart ordering",
                )
                for field_index, field_name in enumerate(
                    INSTALLED_GATE5_FIELDS, start=1
                ):
                    values = {
                        1: (
                            "strict empty or positive-length interval query; "
                            "singleton is boundary-only"
                        ),
                        2: homogeneity,
                        3: chart_pair["prefix_chart"],
                        4: chart_pair["suffix_chart"],
                    }
                    sample_operator_cell_id = generator[
                        "stable_id_interface_sample"
                    ]["operator_cell_id"]
                    sample_slot_payload = [
                        recut["official_word_key_id"],
                        sample_operator_cell_id,
                        roof_level,
                        field_name,
                    ]
                    rows.append(
                        {
                            "generator_family": family,
                            "label_parameter_domains": {
                                "source": source_domain,
                                "actual_third": third_domain,
                            },
                            "official_word_key_id": recut[
                                "official_word_key_id"
                            ],
                            "homogeneous_subbranch_id_schema": subbranch,
                            "carrier_child_id_schema": carrier_child,
                            "roof_level_j": roof_level,
                            "field_index": field_index,
                            "field_name": field_name,
                            "field_value_or_contract": values[field_index],
                            "immutable_slot_key_schema": (
                                "(official-word-key-id,homogeneous-subbranch-id,"
                                "roof-level-j,field-name)"
                            ),
                            "parameterized_slot_id_constructor": (
                                "round120-slot:sha256(canonical([official-word-key-id,"
                                "round117-operator-cell-id(active-labels),"
                                "roof-level-j,field-name]))"
                            ),
                            "stable_ID_interface_sample": {
                                "homogeneous_subbranch_id": sample_operator_cell_id,
                                "slot_id": (
                                    "round120-slot:" + digest(sample_slot_payload)
                                ),
                                "sample_is_an_ID_API_test_not_a_nonempty_claim": True,
                            },
                            "slot_status": (
                                "CERTIFIED_PARAMETERIZED_ON_EVERY_NONEMPTY_"
                                "ACTUAL_CHILD"
                            ),
                            "recut_schema_row_id": recut["recut_rule_id"],
                        }
                    )
    return rows


def static_contract(document: dict[str, Any]) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "certificate envelope keys",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict and set(result) == RESULT_KEYS, "result schema")
    require(document["result_sha256"] == digest(result), "result digest")
    require(type(result["precision_bits"]) is int, "producer precision type")
    require(result["precision_bits"] >= 512, "producer precision")
    require(result["round113_parent_proof_box_count"] == 72, "parent count")
    require(result["round117_generator_family_template_count"] == 112, "family count")
    require(result["upstream_and_helper_pins"] == UPSTREAM_PINS, "upstream pins")
    require(
        result["child_generator_rows_sha256"]
        == digest(result["child_generator_rows"]),
        "child row digest",
    )
    rows = result["child_generator_rows"]
    require(type(rows) is list and len(rows) == 72, "child rows")
    require(
        [row["parent_round113_cell_id"] for row in rows]
        == sorted(row["parent_round113_cell_id"] for row in rows),
        "canonical parent order",
    )
    require(
        len({row["parent_round113_cell_id"] for row in rows}) == 72,
        "parent uniqueness",
    )
    total_generators = 0
    total_slots = 0
    for index, row in enumerate(rows):
        require(type(row) is dict and set(row) == ROW_KEYS, f"row schema:{index}")
        require(
            type(row["canonical_parent_W_leaf"]) is dict
            and set(row["canonical_parent_W_leaf"]) == LEAF_KEYS,
            f"leaf schema:{index}",
        )
        require(
            type(row["actual_third_collision_contract"]) is dict
            and set(row["actual_third_collision_contract"])
            == THIRD_COLLISION_KEYS,
            f"actual-third schema:{index}",
        )
        require(
            type(row["boundary_owner_conjunction"]) is dict
            and set(row["boundary_owner_conjunction"]) == BOUNDARY_OWNER_KEYS,
            f"boundary-owner schema:{index}",
        )
        require(
            type(row["boundary_owner_conjunction"]["priority_1_natural"])
            is dict
            and set(row["boundary_owner_conjunction"]["priority_1_natural"])
            == NATURAL_PRIORITY_KEYS,
            f"natural-boundary schema:{index}",
        )
        require(
            type(row["typed_Borel_locator_contract"]) is dict
            and set(row["typed_Borel_locator_contract"]) == TYPED_LOCATOR_KEYS,
            f"typed locator schema:{index}",
        )
        generators = row["round117_generator_contract_rows"]
        require(type(generators) is list, f"generator rows:{index}")
        for generator in generators:
            require(
                type(generator) is dict and set(generator) == GENERATOR_KEYS,
                f"generator schema:{index}",
            )
        total_generators += len(generators)
        recuts = row["three_step_adapted_recut_frontier_schema_rows"]
        require(type(recuts) is list and len(recuts) == 3, f"recut rows:{index}")
        require(
            row["three_step_adapted_recut_frontier_schema_rows_sha256"]
            == digest(recuts),
            f"recut digest:{index}",
        )
        require([recut["stage"] for recut in recuts] == [0, 1, 2], f"recut stages:{index}")
        for recut in recuts:
            require(
                type(recut) is dict and set(recut) == RECUT_KEYS,
                f"recut schema:{index}",
            )
            require(
                type(recut["roof_level_count"]) is int
                and recut["roof_level_count"] in (1, 2),
                f"roof count:{index}",
            )
            chart_pairs = recut["roof_level_chart_pairs"]
            require(
                type(chart_pairs) is list
                and len(chart_pairs) == recut["roof_level_count"]
                and [
                    pair["roof_level_j"] for pair in chart_pairs
                ]
                == list(range(recut["roof_level_count"])),
                f"roof chart pair count:{index}",
            )
            for pair in chart_pairs:
                require(
                    type(pair) is dict and set(pair) == ROOF_CHART_PAIR_KEYS,
                    f"roof chart pair schema:{index}",
                )
            require(
                recut["actual_instance_materialized"] is False,
                f"recut materialization nonclaim:{index}",
            )
            require(
                qvalue(
                    recut["candidate_one_step_F5_template_not_installed"],
                    "recut F5 frontier",
                )
                == THETA,
                f"recut F5 frontier:{index}",
            )
            require(
                qvalue(
                    recut["candidate_one_step_F6_template_not_installed"],
                    "recut F6 frontier",
                )
                == ONE_STEP_LOG_VARIATION,
                f"recut F6 frontier:{index}",
            )
        require(
            row["actual_image_recut_instance_rows"] == []
            and row["actual_image_recut_instance_count"] == 0,
            f"actual recut nonclaim:{index}",
        )
        slots = row["gate5_F1_F4_slot_schema_rows"]
        require(type(slots) is list, f"slot rows:{index}")
        require(
            row["gate5_F1_F4_slot_schema_rows_sha256"] == digest(slots),
            f"slot digest:{index}",
        )
        require(
            row["gate5_F1_F4_slot_schema_template_count"] == len(slots),
            f"slot count:{index}",
        )
        for slot in slots:
            require(
                type(slot) is dict and set(slot) == SLOT_KEYS,
                f"slot schema:{index}",
            )
            require(
                type(slot["field_index"]) is int
                and 1 <= slot["field_index"] <= 4,
                f"slot field index:{index}",
            )
            require(
                slot["field_name"] == GATE5_FIELDS[slot["field_index"] - 1],
                f"slot field name:{index}",
            )
            require(
                type(slot["roof_level_j"]) is int
                and slot["roof_level_j"] >= 0,
                f"slot roof:{index}",
            )
            require(
                type(slot["label_parameter_domains"]) is dict
                and set(slot["label_parameter_domains"])
                == {"source", "actual_third"},
                f"slot label domains:{index}",
            )
            require(
                type(slot["stable_ID_interface_sample"]) is dict
                and set(slot["stable_ID_interface_sample"])
                == SLOT_SAMPLE_KEYS,
                f"slot sample schema:{index}",
            )
            require(
                slot["stable_ID_interface_sample"][
                    "sample_is_an_ID_API_test_not_a_nonempty_claim"
                ]
                is True,
                f"slot sample nonclaim:{index}",
            )
        total_slots += len(slots)
        require(
            qvalue(
                row["candidate_three_step_F5_template_not_installed"],
                "row F5 frontier",
            )
            == THREE_STEP_THETA,
            f"three-step F5 frontier:{index}",
        )
        require(
            qvalue(
                row["candidate_three_step_F6_template_not_installed"],
                "row F6 frontier",
            )
            == THREE_STEP_LOG_VARIATION,
            f"three-step F6 frontier:{index}",
        )
        require(row["connected_rank"] == 0, f"connected rank:{index}")
        require(row["parameterized_component_rank"] == 0, f"component rank:{index}")
        require(
            row[
                "empty_or_one_connected_interval_for_every_fixed_b_and_active_generator"
            ]
            is True,
            f"connected theorem:{index}",
        )
        require(
            row["positive_length_proof_required_before_child_emission"] is True,
            f"positive child query:{index}",
        )
        require(
            row["parameterized_actual_child_id_schema"]
            == CARRIER_CHILD_ID_SCHEMA,
            f"child ID schema:{index}",
        )
        require(
            row["first_and_second_collision_homogeneity"] == "H0_CENTRAL",
            f"middle H0:{index}",
        )
        require(
            qvalue(
                row["first_collision_cosine_strict_lower"],
                f"first cosine:{index}",
            )
            > Q(4, 5)
            and qvalue(
                row["second_collision_cosine_strict_lower"],
                f"second cosine:{index}",
            )
            > Q(9, 10)
            and qvalue(
                row[
                    "minimum_selected_collision_chart_dominance_strict_lower"
                ],
                f"chart margin:{index}",
            )
            > Q(1, 1000),
            f"middle H0/chart thresholds:{index}",
        )
        require(
            row["gate5_actual_child_field_status"]
            == {
                "F1": "CERTIFIED_PARAMETERIZED_EMPTY_OR_CONNECTED_RANK_0",
                "F2": "CERTIFIED_PARAMETERIZED_PHYSICAL_HOMOGENEITY_SUBBRANCH",
                "F3": "CERTIFIED_PARAMETERIZED_PREFIX_CHART",
                "F4": "CERTIFIED_PARAMETERIZED_SUFFIX_CHART",
                "F5": "NOT_INSTALLED_MISSING_ACTUAL_IMAGE_RECUT_INSTANCES",
                "F6": "NOT_INSTALLED_MISSING_ACTUAL_IMAGE_RECUT_INSTANCES",
            },
            f"row F1-F4/F5-F6 frontier status:{index}",
        )
        lower = qvalue(
            row["squared_third_coordinate_derivative_abs_strict_lower"],
            f"derivative lower:{index}",
        )
        upper = qvalue(
            row["squared_third_coordinate_derivative_abs_strict_upper"],
            f"derivative upper:{index}",
        )
        require(0 < lower < upper, f"derivative enclosure:{index}")
        if row["sheet_kind"] == "HIT":
            require(
                row["squared_third_coordinate"] == "c3^2"
                and row["squared_third_coordinate_derivative_sign"] == -1
                and lower > 424
                and row["natural_boundaries_excluded"] == ["c0=0", "c3=0"],
                f"HIT row:{index}",
            )
        else:
            require(
                row["sheet_kind"] == "BYPASS"
                and row["squared_third_coordinate"] == "b3^2"
                and row["squared_third_coordinate_derivative_sign"] == 1
                and lower > 480
                and row["natural_boundaries_excluded"] == ["c0=0", "b3=0"],
                f"BYPASS row:{index}",
            )
    require(total_generators == 112, "total generator templates")
    require(total_slots > 0, "slot templates")
    require(sum(row["sheet_kind"] == "HIT" for row in rows) == 8, "HIT count")
    require(sum(row["sheet_kind"] == "BYPASS" for row in rows) == 64, "BYPASS count")

    registry = result["actual_parent_W_registry_contract"]
    require(
        set(registry)
        == {
            "registry_type",
            "base_region_key",
            "canonical_leaf_equation",
            "canonical_slope_dphi_dr",
            "source_component",
            "source_radius",
            "source_curvature",
            "unique_leaf_parameter",
            "source_adapted_coordinate",
            "source_adapted_density",
            "corrected_natural_source_cell_rule",
            "adapted_cell_length_upper",
            "Round31_Euclidean_source_cell_rule_reused",
            "finite_actual_curve_count_claimed",
            "parameterized_actual_parent_W_registry_installed",
        },
        "parent-W registry schema",
    )
    require(
        registry
        == {
            "registry_type": (
                "fixed-s=0 grazing-cylinder Borel parameterized actual "
                "parent-W registry"
            ),
            "base_region_key": "round117 operator-cell/root-graph region ID",
            "canonical_leaf_equation": "phi(r)=4*r+b; p(r)=sin(4*r+b)",
            "canonical_slope_dphi_dr": "4",
            "source_component": "G",
            "source_radius": "9/25",
            "source_curvature": "25/9",
            "unique_leaf_parameter": "b=sigma0*arccos(c0)-4*r",
            "source_adapted_coordinate": (
                "u_*(r)=integral_(r_left)^r "
                "(kappa_G+4)dt=(61/9)*(r-r_left)"
            ),
            "source_adapted_density": "61/9",
            "corrected_natural_source_cell_rule": (
                "half-open u_* intervals [k*1e-90,(k+1)*1e-90), "
                "clipped at the last endpoint which is closed"
            ),
            "adapted_cell_length_upper": "1e-90",
            "Round31_Euclidean_source_cell_rule_reused": False,
            "finite_actual_curve_count_claimed": False,
            "parameterized_actual_parent_W_registry_installed": True,
        },
        "parent-W registry contract",
    )
    require(result["Round31_compact_Q2_parent_W_domain_reused"] is False, "R31 reuse")
    require(
        qvalue(result["Round31_compact_Q2_source_abs_momentum_upper"], "R31 p")
        == Q(1, 50),
        "R31 p upper",
    )
    require(
        qvalue(
            result["Round120_grazing_source_momentum_square_certified_lower"],
            "R120 p2",
        )
        == 1 - OUTER**2,
        "R120 p2 lower",
    )
    require(
        result["Round31_and_Round120_physical_source_domains_strictly_disjoint"]
        is True,
        "domain disjointness",
    )
    require(result["parameterized_actual_child_registry_installed"] is True, "child registry")
    require(result["finite_actual_child_count_claimed"] is False, "finite child nonclaim")
    require(
        result["actual_child_registry_cardinality"]
        == "BOREL_PARAMETERIZED_NOT_A_FINITE_INTEGER_ENUMERATION",
        "Borel cardinality",
    )
    nonvacuity = result["nonvacuous_actual_child_fibre_existence"]
    require(
        type(nonvacuity) is dict
        and set(nonvacuity)
        == {
            "round117_nonempty_central_outer_parent_count",
            "positive_length_fixed_b_fibre_family_exists",
            "proof",
            "stable_interface_seed_parent_round113_cell_id",
            "stable_interface_seed_operator_cell_id",
            "seed_is_an_existence_interface_not_a_materialized_exact_b_ID",
            "materialized_exact_b_witness_ID_count",
        },
        "nonvacuity schema",
    )
    require(
        nonvacuity["round117_nonempty_central_outer_parent_count"] == 24
        and nonvacuity["positive_length_fixed_b_fibre_family_exists"] is True
        and nonvacuity[
            "seed_is_an_existence_interface_not_a_materialized_exact_b_ID"
        ]
        is True
        and nonvacuity["materialized_exact_b_witness_ID_count"] == 0,
        "nonvacuity contract",
    )
    require(
        result["typed_Borel_locator_precedent"]
        == {
            "Round35_physical_domain_reused": False,
            "locator_pattern_only": (
                "least rational-dyadic interval basis index with closure "
                "inside the interval"
            ),
            "formal_b_is_an_exact_typed_parameter_not_a_decimal_hash": True,
        },
        "typed Borel locator precedent",
    )
    require(
        result["owner_candidate_replay_counts"]
        == {
            "parent_cells": 72,
            "three_leg_replays": 216,
            "HIT_cells": 8,
            "BYPASS_cells_with_actual_winner": 64,
            "residual_cells": 0,
        },
        "owner replay counts",
    )
    require(
        result["gate5_actual_child_field_status"]
        == {
            **{
                f"F{i}": (
                    "CERTIFIED_PARAMETERIZED_ON_EVERY_NONEMPTY_ROUND120_ACTUAL_CHILD"
                )
                for i in range(1, 5)
            },
            **{
                f"F{i}": "NOT_INSTALLED_ON_ROUND120_ACTUAL_CHILD"
                for i in range(5, 19)
            },
        },
        "global child field status",
    )
    require(result["rank3_actual_child_field_maturity"] == "4/18", "child maturity")
    require(result["gate5_global_maturity"] == "10/18", "global maturity")
    require(result["complete_18_field_block_count"] == 0, "complete block count")
    require(result["gate5_block_count"] == 0, "Gate5 block count")
    require(result["cm2_verdict"] == "NO-GO_FOR_CLAIM", "CM2 verdict")
    require(
        result["natural_boundary_ledger"]
        == {
            "c0_zero": (
                "source grazing singular trace; owned by the singular ledger"
            ),
            "c3_zero": (
                "HIT designated third tangency; owned by the singular ledger"
            ),
            "b3_zero": (
                "BYPASS designated tangent boundary; owned by the singular ledger"
            ),
            "regular_child_scope": (
                "c0>0 and c3>0 (HIT), or c0>0 and b3>0 (BYPASS)"
            ),
            "owner_priority": {
                "natural_boundary_overrides_artificial_rules": True,
                "artificial_owner_rule": (
                    "conjunction of every applicable unique half-open owner"
                ),
                "artificial_layers": [
                    "Round113 dyadic half-open owner",
                    "Round117 homogeneity half-open owner",
                    "corrected source-adapted half-open owner",
                ],
            },
            "round117_boundary_ownership_ledger_sha256": (
                "c0b61bece22f8b5e0e11e7fc3a2d427e0eb056b6da22fa3860bb7168dedeb67c"
            ),
        },
        "natural boundary ledger",
    )
    require(
        result["strict_nonclaims"]
        == [
            (
                "the compact Round31 Q2 parent-W registry is physically "
                "disjoint and is not reused as this grazing registry"
            ),
            (
                "no finite integer count of the Borel-parameterized child "
                "or recut registry is claimed"
            ),
            (
                "c0=0, c3=0, and b3=0 remain natural singular-ledger "
                "strata and are not regular children"
            ),
            (
                "no endpoint-inclusive bounded physical two-sided collar, "
                "cross-trace union reach, or whole-face owner atlas is installed"
            ),
            (
                "actual image recut instances and child-local F5/F6 are not "
                "installed; the stored F5/F6 constants are frontier templates only"
            ),
            "F5-F18 are not installed on the Round120 actual children",
            (
                "child-local 4/18 does not upgrade the global Gate5 10/18 "
                "maturity or create a complete block"
            ),
            "Gate5 and CM2 remain unavailable",
        ],
        "strict nonclaims",
    )
    require(
        result["strict_scope"]
        == (
            "fixed-s=0 Borel-parameterized canonical parent-W intersections "
            "with the 72 Round113/117 regular relative-interior operator-cell "
            "root graphs, child-local F1-F4, and an explicitly uninstalled "
            "three-image-recut/F5-F6 frontier schema"
        ),
        "strict scope",
    )
    theorem = result["nonempty_or_empty_intersection_theorem"]
    require(
        type(theorem) is dict
        and set(theorem)
        == {
            "fixed_leaf_equations",
            "B_t_nonzero_on_all_72_parents",
            "HIT_squared_coordinate_derivative",
            "BYPASS_squared_coordinate_derivative",
            "HIT_parent_count_with_strict_negative_derivative",
            "BYPASS_parent_count_with_strict_positive_derivative",
            "HIT_global_derivative_abs_strict_lower",
            "BYPASS_global_derivative_abs_strict_lower",
            "every_fixed_b_active_operator_cell_intersection_is_empty_or_one_connected_interval",
            "connected_rank",
            "Borel_fibre_construction",
            "total_numeric_decision_procedure_for_arbitrary_exact_real_b_claimed",
            "positive_length_proof_is_required_before_any_child_ID_is_emitted",
            "formal_intercept_parameter_is_never_hashed_from_an_Arb_decimal",
        },
        "intersection theorem schema",
    )
    require(theorem["B_t_nonzero_on_all_72_parents"] is True, "B_t theorem")
    require(
        theorem["HIT_parent_count_with_strict_negative_derivative"] == 8,
        "HIT theorem count",
    )
    require(
        theorem["BYPASS_parent_count_with_strict_positive_derivative"] == 64,
        "BYPASS theorem count",
    )
    require(
        theorem[
            "every_fixed_b_active_operator_cell_intersection_is_empty_or_one_connected_interval"
        ]
        is True
        and theorem["connected_rank"] == 0,
        "connected interval theorem",
    )
    require(
        theorem["formal_intercept_parameter_is_never_hashed_from_an_Arb_decimal"]
        is True,
        "formal intercept contract",
    )
    require(
        theorem[
            "total_numeric_decision_procedure_for_arbitrary_exact_real_b_claimed"
        ]
        is False
        and theorem[
            "positive_length_proof_is_required_before_any_child_ID_is_emitted"
        ]
        is True,
        "Borel fibre/non-oracle contract",
    )
    require(
        qvalue(theorem["HIT_global_derivative_abs_strict_lower"], "global HIT")
        == min(
            qvalue(
                row["squared_third_coordinate_derivative_abs_strict_lower"],
                "row HIT",
            )
            for row in rows
            if row["sheet_kind"] == "HIT"
        ),
        "global HIT lower",
    )
    require(
        qvalue(
            theorem["BYPASS_global_derivative_abs_strict_lower"],
            "global BYPASS",
        )
        == min(
            qvalue(
                row["squared_third_coordinate_derivative_abs_strict_lower"],
                "row BYPASS",
            )
            for row in rows
            if row["sheet_kind"] == "BYPASS"
        ),
        "global BYPASS lower",
    )
    f56 = result["uninstalled_actual_child_F5_F6_frontier"]
    require(
        type(f56) is dict
        and set(f56)
        == {
            "universal_template_scope",
            "one_step_adapted_inverse_strict_upper",
            "one_step_log_variation_strict_upper",
            "three_step_adapted_inverse_strict_upper",
            "three_step_log_variation_strict_upper",
            "area_Jacobian_used",
            "chart_norm_used",
            "restriction_monotonicity_requires_future_actual_child_and_recut_ID_binding",
            "per_leg_per_roof_F5_F6_immutable_slots_installed",
            "finite_slot_instance_count_claimed",
            "first_missing_evidence",
        },
        "F5/F6 frontier schema",
    )
    require(
        qvalue(f56["one_step_adapted_inverse_strict_upper"], "F5 one step")
        == THETA,
        "F5 frontier",
    )
    require(
        qvalue(f56["one_step_log_variation_strict_upper"], "F6 one step")
        == ONE_STEP_LOG_VARIATION,
        "F6 frontier",
    )
    require(
        qvalue(f56["three_step_adapted_inverse_strict_upper"], "F5 three step")
        == THREE_STEP_THETA,
        "F5 product",
    )
    require(
        qvalue(f56["three_step_log_variation_strict_upper"], "F6 three step")
        == THREE_STEP_LOG_VARIATION,
        "F6 sum",
    )
    require(f56["area_Jacobian_used"] is False, "area Jacobian non-use")
    require(f56["chart_norm_used"] is False, "chart norm non-use")
    require(
        f56["restriction_monotonicity_requires_future_actual_child_and_recut_ID_binding"]
        is True
        and f56["per_leg_per_roof_F5_F6_immutable_slots_installed"] is False
        and f56["finite_slot_instance_count_claimed"] is False,
        "F5/F6 uninstalled frontier",
    )
    recut_registry = result["canonical_three_step_recut_frontier"]
    require(
        type(recut_registry) is dict
        and set(recut_registry)
        == {
            "stage_count",
            "source_rule",
            "image_rule",
            "candidate_future_rule",
            "candidate_actual_instance_key",
            "actual_interval_endpoints_materialized",
            "actual_natural_indices_materialized",
            "actual_image_pullback_common_refinement_ranks_materialized",
            "global_invariant_cone_carries_every_image_curve",
            "recut_schema_frontier_installed",
            "parameterized_actual_recut_instance_registry_installed",
            "actual_recut_instance_count",
            "finite_recut_instance_count_claimed",
            "half_open_owner_contract_inherited_from_Round50",
        },
        "recut frontier schema",
    )
    require(recut_registry["stage_count"] == 3, "recut stage count")
    require(
        recut_registry["parameterized_actual_recut_instance_registry_installed"]
        is False
        and recut_registry["actual_recut_instance_count"] == 0
        and recut_registry["finite_recut_instance_count_claimed"] is False,
        "actual recut non-installation",
    )
    require(
        recut_registry["actual_interval_endpoints_materialized"] is False
        and recut_registry["actual_natural_indices_materialized"] is False
        and recut_registry[
            "actual_image_pullback_common_refinement_ranks_materialized"
        ]
        is False
        and recut_registry["recut_schema_frontier_installed"] is True,
        "recut frontier",
    )
    return result


def replay_row(
    stored: dict[str, Any],
    values: dict[str, Any],
    idx: dict[str, Any],
) -> dict[str, Any]:
    parent_id = stored["parent_round113_cell_id"]
    require(parent_id in idx["parents"], f"unknown parent:{parent_id}")
    sheet, parent = idx["parents"][parent_id]
    input_sheet = idx["sheets112"][sheet["sheet_id"]]
    row117 = idx["rows117"][parent_id]
    kind = sheet["sheet_kind"]
    coordinate = "c3" if kind == "HIT" else "b3"
    branch = tuple(input_sheet["branch_key"])
    repaired = idx["repaired"][(kind, branch)]
    require(stored["parent_round113_sheet_id"] == sheet["sheet_id"], "sheet join")
    require(stored["sheet_kind"] == kind, "kind join")
    require(stored["branch_key"] == list(branch), "branch join")
    require(stored["parameter_box"] == parent["parameter_box"], "parameter box join")
    require(stored["repaired_endpoint_id"] == repaired["repaired_endpoint_id"], "endpoint join")
    require(stored["exterior_port_id"] == repaired["exterior_port_id"], "port join")
    require(stored["source_chart"] == input_sheet["source_chart"], "source chart")
    sigma = input_sheet["source_grazing_sign_sigma0"]
    require(stored["source_grazing_sign_sigma0"] == sigma, "source sign")
    require(tuple(row117["branch_key"]) == branch, "R117 branch")
    require(row117["sheet_kind"] == kind, "R117 kind")

    source = replace(idx["cores"][branch[0]], chart_id=input_sheet["source_chart"])
    c0, c1 = map(Q, parent["parameter_box"]["c0"])
    z0, z1 = map(Q, parent["parameter_box"][coordinate])
    fresh = round113.audit_cell(
        input_sheet,
        source,
        branch,
        c0,
        c1,
        z0,
        z1,
        idx["pair_index"],
        idx["pattern_index"],
    )
    require(
        fresh["official_path_id"]
        == parent["official_path_id"]
        == row117["official_path_id_inherited"]
        == stored["official_path_id"],
        "official path replay",
    )
    require(
        fresh["official_word_key_ids"]
        == parent["official_word_key_ids"]
        == row117["official_word_key_ids_inherited"]
        == stored["official_word_key_ids"],
        "official word replay",
    )
    require(
        fresh["ordered_regular_relative_interior_owner_ids"]
        == parent["ordered_regular_relative_interior_owner_ids"]
        == stored["ordered_owner_ids"],
        "owner replay",
    )
    t0, t1 = map(Q, fresh["implicit_t_root_enclosure"])
    geometry = round113.path_geometry(
        source,
        branch,
        sigma,
        kind,
        t0,
        t1,
        c0,
        c1,
        z0,
        z1,
    )
    t = interval(t0, t1)
    c = interval(c0, c1)
    radial_t = (arb(1) - t * t).sqrt()
    radial_c = (arb(1) - c * c).sqrt()
    chart = input_sheet["source_chart"].split(":")[1]
    epsilon = CHART_ORIENTATION[chart]
    angular_lift_id = f"round120-angular-lift:G:{chart}:k0"
    B_c = -arb(sigma) / radial_c
    B_t = -arb(4) * aq(SOURCE_RADIUS) * arb(epsilon) / radial_t
    t_c = -B_c / B_t
    equation = geometry["equation"]
    delta_on_leaf = equation.gradient[1] + equation.gradient[0] * t_c
    third_radius = aq(round112.radius(branch[2]))
    squared_c = delta_on_leaf / (third_radius * third_radius)
    if kind == "BYPASS":
        squared_c = -squared_c
    expected_sign = -1 if kind == "HIT" else 1
    require(strict_sign(squared_c) == expected_sign, "independent derivative sign")
    require(
        stored["squared_third_coordinate_derivative_sign"] == expected_sign,
        "stored derivative sign",
    )
    independent_lower, independent_upper = abs_bounds(squared_c, "derivative")
    stored_lower = qvalue(
        stored["squared_third_coordinate_derivative_abs_strict_lower"],
        "stored derivative lower",
    )
    stored_upper = qvalue(
        stored["squared_third_coordinate_derivative_abs_strict_upper"],
        "stored derivative upper",
    )
    require(
        stored_lower <= independent_lower * Q(1001, 1000),
        "stored derivative lower cross-precision consistency",
    )
    require(
        stored_upper * Q(1001, 1000) >= independent_upper,
        "stored derivative upper cross-precision consistency",
    )
    require(
        independent_lower > (Q(424) if kind == "HIT" else Q(480)),
        "independent 424/480 derivative",
    )

    leaf = stored["canonical_parent_W_leaf"]
    require(leaf["source_chart_theta_derivative_sign"] == epsilon, "chart orientation")
    require(
        leaf["angular_lift_id"] == angular_lift_id
        and leaf["canonical_theta_source_chart_of_t"]
        == CANONICAL_ANGULAR_LIFT[chart]
        and leaf["angular_lift_additive_2pi_index"] == 0,
        "canonical angular lift",
    )
    for key, value in (
        ("B_t_sign", B_t),
        ("B_c_sign", B_c),
        ("dt_dc_at_fixed_b_sign", t_c),
    ):
        require(leaf[key] == strict_sign(value), f"leaf sign:{key}")
    for prefix, value in (("B_t", B_t), ("B_c", B_c), ("dt_dc", t_c)):
        lower, upper = abs_bounds(value, prefix)
        require(
            qvalue(leaf[f"abs_{prefix}_strict_lower"], f"{prefix} lower")
            <= lower,
            f"{prefix} lower dominance",
        )
        if prefix == "dt_dc":
            require(
                qvalue(leaf["abs_dt_dc_strict_upper"], "dt_dc upper")
                >= upper,
                "dt_dc upper dominance",
            )

    first_cosine = (
        arb(1) - geometry["selected"][0]["momentum"].value ** 2
    ).sqrt()
    second_cosine = (
        arb(1) - geometry["selected"][1]["momentum"].value ** 2
    ).sqrt()
    first_lower = arb_pair(first_cosine)[0]
    second_lower = arb_pair(second_cosine)[0]
    require(first_lower > Q(4, 5), "first actual H0")
    require(second_lower > Q(9, 10), "second actual H0")
    require(
        qvalue(stored["first_collision_cosine_strict_lower"], "first cosine")
        <= first_lower,
        "first cosine dominance",
    )
    require(
        qvalue(stored["second_collision_cosine_strict_lower"], "second cosine")
        <= second_lower,
        "second cosine dominance",
    )
    chart_margins: list[Q] = []
    for leg in fresh["leg_audits"]:
        margin = arb(leg["selected_collision_chart_dominance_margin"][0])
        lower = arb_pair(margin)[0]
        require(lower > 0, "chart dominance positive")
        chart_margins.append(lower)
    chart_lower = min(chart_margins)
    require(chart_lower > Q(1, 1000), "chart dominance threshold")
    require(
        qvalue(
            stored["minimum_selected_collision_chart_dominance_strict_lower"],
            "stored chart margin",
        )
        <= chart_lower * Q(1001, 1000),
        (
            "chart dominance stored lower:"
            f"{stored['minimum_selected_collision_chart_dominance_strict_lower']}"
            f">{chart_lower}"
        ),
    )

    generators = row117["generator_families"]
    require(
        stored["round117_generator_family_digest"] == digest(generators),
        "R117 generator digest",
    )
    expected_generators = expected_generator_contract(generators)
    require(
        stored["round117_generator_contract_rows"] == expected_generators,
        "R117 generator contract",
    )
    expected_actual_third = {
        "owner_id": row117["actual_third_collision_owner_id"],
        "homogeneity_label_or_parameter": (
            "R117 active third-label parameter"
            if kind == "HIT"
            else row117["actual_third_collision_homogeneity_label"]
        ),
        "BYPASS_actual_winner_H0_whole_parent": (
            row117.get(
                "actual_third_collision_H0_strict_whole_parent_cell", False
            )
            if kind == "BYPASS"
            else None
        ),
        "BYPASS_actual_winner_cosine_minus_b128_enclosure": (
            row117.get(
                "actual_third_collision_cosine_minus_b128_enclosure"
            )
            if kind == "BYPASS"
            else None
        ),
        "BYPASS_b3_is_collision_angle": (
            row117.get("bypass_b3_is_collision_angle")
            if kind == "BYPASS"
            else None
        ),
        "BYPASS_b3_homogeneity_index": (
            row117.get("bypass_b3_homogeneity_index")
            if kind == "BYPASS"
            else None
        ),
    }
    require(
        stored["actual_third_collision_contract"] == expected_actual_third,
        "actual third collision contract",
    )
    require(
        stored["boundary_owner_conjunction"]
        == {
            "priority_1_natural": {
                "source_c0_zero_owned_by_singular_ledger": True,
                "third_coordinate": coordinate,
                "third_coordinate_zero_owned_by_singular_ledger": True,
                "regular_child_owns_either_natural_boundary": False,
                "logical_relation": (
                    "each natural boundary is excluded individually; "
                    "simultaneous zero is not required"
                ),
            },
            "priority_2_round113_dyadic": row117[
                "parent_artificial_boundary_ownership"
            ],
            "priority_3_round117_homogeneity": (
                "H_n=(sin((n+1)^-2),sin(n^-2)] owns its upper boundary; "
                "H0_CENTRAL_OUTER=(sin(128^-2),1/16384] is open at its "
                "lower boundary"
            ),
            "priority_4_source_adapted": (
                "oriented [k*1e-90,(k+1)*1e-90), clipped at the last "
                "endpoint which is closed"
            ),
            "coincident_artificial_boundaries_use_the_conjunction_of_all_unique_owner_rules": True,
            "natural_boundary_always_overrides_artificial_ownership": True,
        },
        "boundary owner conjunction",
    )
    require(
        stored["typed_Borel_locator_contract"]
        == {
            "intercept_parameter": (
                "exact mathematical real b represented by a canonical nested "
                "rational-dyadic locator"
            ),
            "source_interval_rank": (
                "least rational-dyadic interval basis index whose closure "
                "lies inside the positive-length component"
            ),
            "component_rank": 0,
            "angular_lift_id": angular_lift_id,
            "same_canonical_angular_lift_used_in_intercept_b": True,
            "locator_validity": (
                "nonempty closed dyadic intervals, nested, diameters tending to zero"
            ),
            "dyadic_endpoint_representation": (
                "canonical terminating expansion with trailing zeros"
            ),
            "analytic_boundary_equality": (
                "symbolic half-open owner predicate; no finite-precision "
                "equality inference"
            ),
            "total_computable_real_comparison_oracle_claimed": False,
            "Arb_or_decimal_text_in_stable_ID": False,
            "typed_parent_W_tuple": (
                "(round120-grazing-parent-W-v1,repaired-endpoint-id,"
                "angular-lift-id,exact-b)"
            ),
        },
        "typed Borel locator",
    )
    expected_recuts = expected_recut_rows(fresh, parent_id)
    require(
        stored["three_step_adapted_recut_frontier_schema_rows"]
        == expected_recuts,
        "recut frontier replay",
    )
    require(
        stored["actual_image_recut_instance_rows"] == []
        and stored["actual_image_recut_instance_count"] == 0,
        "actual image recut nonclaim",
    )
    expected_slots = expected_slot_rows(generators, expected_recuts)
    require(
        stored["gate5_F1_F4_slot_schema_rows"] == expected_slots,
        "F1-F4 slot replay",
    )
    if kind == "BYPASS":
        require(
            all(
                row["third_label_domain"] == "H0_CENTRAL"
                for row in expected_generators
            ),
            "BYPASS actual G-winner H0",
        )
    return {
        "parent_round113_cell_id": parent_id,
        "sheet_kind": kind,
        "independent_squared_coordinate_derivative_abs_lower": str(
            independent_lower
        ),
        "independent_squared_coordinate_derivative_abs_upper": str(
            independent_upper
        ),
        "first_collision_cosine_lower": str(first_lower),
        "second_collision_cosine_lower": str(second_lower),
        "minimum_chart_dominance_lower": str(chart_lower),
        "generator_family_template_count": len(generators),
        "recut_stage_count": len(expected_recuts),
        "slot_schema_template_count": len(expected_slots),
    }


def mathematical_replay(
    result: dict[str, Any], values: dict[str, Any], idx: dict[str, Any]
) -> dict[str, Any]:
    rows = [replay_row(row, values, idx) for row in result["child_generator_rows"]]
    require(
        {row["parent_round113_cell_id"] for row in rows}
        == set(idx["parents"]),
        "72-parent replay bijection",
    )
    hit = [row for row in rows if row["sheet_kind"] == "HIT"]
    bypass = [row for row in rows if row["sheet_kind"] == "BYPASS"]
    require(len(hit) == 8 and len(bypass) == 64, "replay kind counts")
    return {
        "independently_replayed_parent_rows": rows,
        "independently_replayed_parent_count": len(rows),
        "independently_replayed_three_leg_count": 3 * len(rows),
        "independently_replayed_HIT_parent_count": len(hit),
        "independently_replayed_BYPASS_parent_count": len(bypass),
        "independent_HIT_derivative_abs_lower": str(
            min(
                qvalue(
                    row["independent_squared_coordinate_derivative_abs_lower"],
                    "replay HIT",
                )
                for row in hit
            )
        ),
        "independent_BYPASS_derivative_abs_lower": str(
            min(
                qvalue(
                    row["independent_squared_coordinate_derivative_abs_lower"],
                    "replay BYPASS",
                )
                for row in bypass
            )
        ),
        "independent_generator_family_template_count": sum(
            row["generator_family_template_count"] for row in rows
        ),
        "independent_recut_stage_template_count": sum(
            row["recut_stage_count"] for row in rows
        ),
        "independent_gate5_F1_F4_slot_schema_template_count": sum(
            row["slot_schema_template_count"] for row in rows
        ),
    }


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def mutation_tests(
    document: dict[str, Any], values: dict[str, Any], idx: dict[str, Any]
) -> list[str]:
    """Exercise closed schemas and selected mathematical dominance checks."""

    static_attacks: list[tuple[str, tuple[Any, ...], Any]] = [
        ("gate5_global_upgrade", ("result", "gate5_global_maturity"), "11/18"),
        ("child_F5_upgrade", ("result", "gate5_actual_child_field_status", "F5"), "CERTIFIED"),
        ("child_F7_upgrade", ("result", "gate5_actual_child_field_status", "F7"), "CERTIFIED"),
        ("actual_recut_registry_forgery", ("result", "canonical_three_step_recut_frontier", "parameterized_actual_recut_instance_registry_installed"), True),
        ("actual_recut_count_forgery", ("result", "canonical_three_step_recut_frontier", "actual_recut_instance_count"), 1),
        ("F5_F6_slot_install_forgery", ("result", "uninstalled_actual_child_F5_F6_frontier", "per_leg_per_roof_F5_F6_immutable_slots_installed"), True),
        ("complete_block_forgery", ("result", "complete_18_field_block_count"), 1),
        ("gate5_block_forgery", ("result", "gate5_block_count"), 1),
        ("cm2_upgrade", ("result", "cm2_verdict"), "GO_FOR_CLAIM"),
        ("finite_child_forgery", ("result", "finite_actual_child_count_claimed"), True),
        ("round31_domain_reuse", ("result", "Round31_compact_Q2_parent_W_domain_reused"), True),
        ("child_registry_erasure", ("result", "parameterized_actual_child_registry_installed"), False),
        ("parent_count_mutation", ("result", "round113_parent_proof_box_count"), 71),
        ("family_count_mutation", ("result", "round117_generator_family_template_count"), 111),
        ("rank_maturity_upgrade", ("result", "rank3_actual_child_field_maturity"), "7/18"),
        ("residual_forgery", ("result", "owner_candidate_replay_counts", "residual_cells"), 1),
        ("connected_rank_mutation", ("result", "child_generator_rows", 0, "connected_rank"), 1),
        ("natural_boundary_capture", ("result", "child_generator_rows", 0, "natural_boundaries_excluded"), []),
        ("middle_H0_erasure", ("result", "child_generator_rows", 0, "first_and_second_collision_homogeneity"), "UNKNOWN"),
        ("recut_F5_frontier_forgery", ("result", "child_generator_rows", 0, "three_step_adapted_recut_frontier_schema_rows", 0, "candidate_one_step_F5_template_not_installed"), "1/10"),
        ("slot_field_swap", ("result", "child_generator_rows", 0, "gate5_F1_F4_slot_schema_rows", 0, "field_name"), GATE5_FIELDS[1]),
    ]

    def assign(root: Any, path: tuple[Any, ...], value: Any) -> None:
        cursor = root
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value

    rejected: list[str] = []
    for label, path, value in static_attacks:
        mutant = copy.deepcopy(document)
        assign(mutant, path, value)
        if path[:2] == ("result", "child_generator_rows"):
            row = mutant["result"]["child_generator_rows"][path[2]]
            if "three_step_adapted_recut_frontier_schema_rows" in path:
                row["three_step_adapted_recut_frontier_schema_rows_sha256"] = digest(
                    row["three_step_adapted_recut_frontier_schema_rows"]
                )
            if "gate5_F1_F4_slot_schema_rows" in path:
                row["gate5_F1_F4_slot_schema_rows_sha256"] = digest(
                    row["gate5_F1_F4_slot_schema_rows"]
                )
            mutant["result"]["child_generator_rows_sha256"] = digest(
                mutant["result"]["child_generator_rows"]
            )
        resign(mutant)
        try:
            static_contract(mutant)
        except (KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"semantic mutation accepted:{label}")

    unknown_attacks = [
        ("unknown_top", ()),
        ("unknown_result", ("result",)),
        ("unknown_row", ("result", "child_generator_rows", 0)),
        (
            "unknown_leaf",
            ("result", "child_generator_rows", 0, "canonical_parent_W_leaf"),
        ),
        (
            "unknown_generator",
            ("result", "child_generator_rows", 0, "round117_generator_contract_rows", 0),
        ),
        (
            "unknown_recut",
            ("result", "child_generator_rows", 0, "three_step_adapted_recut_frontier_schema_rows", 0),
        ),
        (
            "unknown_slot",
            ("result", "child_generator_rows", 0, "gate5_F1_F4_slot_schema_rows", 0),
        ),
    ]
    for label, path in unknown_attacks:
        mutant = copy.deepcopy(document)
        cursor: Any = mutant
        for key in path:
            cursor = cursor[key]
        cursor["unknown_round120_field"] = 1
        if path[:2] == ("result", "child_generator_rows"):
            row = mutant["result"]["child_generator_rows"][path[2]]
            if "three_step_adapted_recut_frontier_schema_rows" in path:
                row["three_step_adapted_recut_frontier_schema_rows_sha256"] = digest(
                    row["three_step_adapted_recut_frontier_schema_rows"]
                )
            if "gate5_F1_F4_slot_schema_rows" in path:
                row["gate5_F1_F4_slot_schema_rows_sha256"] = digest(
                    row["gate5_F1_F4_slot_schema_rows"]
                )
            mutant["result"]["child_generator_rows_sha256"] = digest(
                mutant["result"]["child_generator_rows"]
            )
        resign(mutant)
        try:
            static_contract(mutant)
        except (KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"unknown-key mutation accepted:{label}")

    for label, mutate_rows in (
        ("parent_row_deleted", lambda rows: rows.pop()),
        (
            "parent_row_duplicated",
            lambda rows: rows.append(copy.deepcopy(rows[-1])),
        ),
    ):
        mutant = copy.deepcopy(document)
        mutate_rows(mutant["result"]["child_generator_rows"])
        mutant["result"]["child_generator_rows_sha256"] = digest(
            mutant["result"]["child_generator_rows"]
        )
        resign(mutant)
        try:
            static_contract(mutant)
        except (KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"parent census mutation accepted:{label}")

    # Re-sign a quantitative row after forging its derivative lower bound.
    # The static envelope remains plausible; the 1024-bit replay must reject it.
    row0 = document["result"]["child_generator_rows"][0]

    def expect_row_rejection(label: str, forged_row: dict[str, Any]) -> None:
        mutant = copy.deepcopy(document)
        row_index = next(
            index
            for index, row in enumerate(
                mutant["result"]["child_generator_rows"]
            )
            if row["parent_round113_cell_id"]
            == forged_row["parent_round113_cell_id"]
        )
        mutant["result"]["child_generator_rows"][row_index] = forged_row
        forged_row[
            "three_step_adapted_recut_frontier_schema_rows_sha256"
        ] = digest(forged_row["three_step_adapted_recut_frontier_schema_rows"])
        forged_row["gate5_F1_F4_slot_schema_rows_sha256"] = digest(
            forged_row["gate5_F1_F4_slot_schema_rows"]
        )
        forged_row["gate5_F1_F4_slot_schema_template_count"] = len(
            forged_row["gate5_F1_F4_slot_schema_rows"]
        )
        mutant["result"]["child_generator_rows_sha256"] = digest(
            mutant["result"]["child_generator_rows"]
        )
        resign(mutant)
        try:
            static_contract(mutant)
            replay_row(
                mutant["result"]["child_generator_rows"][row_index],
                values,
                idx,
            )
        except (KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"mathematical mutation accepted:{label}")

    forged = copy.deepcopy(row0)
    forged["squared_third_coordinate_derivative_abs_strict_lower"] = str(
        qvalue(
            row0["squared_third_coordinate_derivative_abs_strict_upper"],
            "attack upper",
        )
        + 1
    )
    expect_row_rejection("resigned_derivative_lower_inflation", forged)

    forged = copy.deepcopy(row0)
    forged["squared_third_coordinate_derivative_sign"] *= -1
    expect_row_rejection("resigned_derivative_sign_flip", forged)

    forged = copy.deepcopy(row0)
    forged["first_collision_cosine_strict_lower"] = "2"
    expect_row_rejection("resigned_middle_H0_lower_inflation", forged)

    forged = copy.deepcopy(row0)
    forged["minimum_selected_collision_chart_dominance_strict_lower"] = "2"
    expect_row_rejection("resigned_chart_margin_inflation", forged)

    forged = copy.deepcopy(row0)
    forged["canonical_parent_W_leaf"]["abs_B_t_strict_lower"] = "100"
    expect_row_rejection("resigned_fixed_b_derivative_inflation", forged)

    forged = copy.deepcopy(row0)
    forged["round117_generator_contract_rows"] = forged[
        "round117_generator_contract_rows"
    ][1:]
    expect_row_rejection("generator_family_deleted", forged)

    forged = copy.deepcopy(row0)
    forged["round117_generator_contract_rows"].append(
        copy.deepcopy(forged["round117_generator_contract_rows"][0])
    )
    expect_row_rejection("generator_family_duplicated", forged)

    forged = copy.deepcopy(row0)
    forged["gate5_F1_F4_slot_schema_rows"] = forged[
        "gate5_F1_F4_slot_schema_rows"
    ][1:]
    expect_row_rejection("F1_F4_slot_deleted", forged)

    forged = copy.deepcopy(row0)
    forged["gate5_F1_F4_slot_schema_rows"].append(
        copy.deepcopy(forged["gate5_F1_F4_slot_schema_rows"][0])
    )
    expect_row_rejection("F1_F4_slot_duplicated", forged)

    forged = copy.deepcopy(row0)
    forged["typed_Borel_locator_contract"][
        "Arb_or_decimal_text_in_stable_ID"
    ] = True
    expect_row_rejection("exact_b_decimal_hash_ambiguity", forged)

    forged = copy.deepcopy(row0)
    forged["typed_Borel_locator_contract"][
        "typed_parent_W_tuple"
    ] = "(Round31-time2-atom-id,b)"
    expect_row_rejection("Round31_parent_W_ID_reuse", forged)

    forged = copy.deepcopy(row0)
    forged["boundary_owner_conjunction"]["priority_1_natural"][
        "regular_child_owns_either_natural_boundary"
    ] = True
    expect_row_rejection("natural_boundary_owner_override", forged)

    forged = copy.deepcopy(row0)
    forged["boundary_owner_conjunction"]["priority_1_natural"][
        "source_c0_zero_owned_by_singular_ledger"
    ] = False
    expect_row_rejection("source_c0_zero_capture", forged)

    forged = copy.deepcopy(row0)
    forged["boundary_owner_conjunction"]["priority_1_natural"][
        "third_coordinate_zero_owned_by_singular_ledger"
    ] = False
    expect_row_rejection("third_coordinate_zero_capture", forged)

    bypass_row = next(
        row
        for row in document["result"]["child_generator_rows"]
        if row["sheet_kind"] == "BYPASS"
    )
    forged = copy.deepcopy(bypass_row)
    forged["actual_third_collision_contract"]["BYPASS_b3_is_collision_angle"] = True
    expect_row_rejection("BYPASS_b3_as_collision_angle", forged)

    forged = copy.deepcopy(bypass_row)
    forged["actual_third_collision_contract"][
        "BYPASS_actual_winner_H0_whole_parent"
    ] = False
    expect_row_rejection("BYPASS_actual_winner_H0_erasure", forged)

    roof_two_stage = next(
        index
        for index, recut in enumerate(
            row0["three_step_adapted_recut_frontier_schema_rows"]
        )
        if recut["roof_level_count"] == 2
    )
    forged = copy.deepcopy(row0)
    pairs = forged["three_step_adapted_recut_frontier_schema_rows"][
        roof_two_stage
    ]["roof_level_chart_pairs"]
    pairs[1] = copy.deepcopy(pairs[0])
    expect_row_rejection("roof_two_duplicated_chart_pair", forged)

    forged = copy.deepcopy(row0)
    pairs = forged["three_step_adapted_recut_frontier_schema_rows"][
        roof_two_stage
    ]["roof_level_chart_pairs"]
    pairs[0]["prefix_chart"] = forged["source_chart"]
    expect_row_rejection("bare_collision_chart_without_type", forged)

    forged = copy.deepcopy(row0)
    recut = forged["three_step_adapted_recut_frontier_schema_rows"][
        roof_two_stage
    ]
    recut["target_chart"] = recut["target_chart"].split("[", 1)[0]
    expect_row_rejection("target_chart_lost_owner_index", forged)
    return rejected


def strict_json_tests() -> list[str]:
    payloads = {
        "duplicate_top_key": '{"schema":"x","schema":"y","result":{},"result_sha256":"z"}',
        "duplicate_nested_key": '{"schema":"x","result":{"a":1,"a":2},"result_sha256":"z"}',
        "duplicate_deep_key": '{"a":{"b":{"c":1,"c":2}}}',
        "nan": '{"x":NaN}',
        "positive_infinity": '{"x":Infinity}',
        "negative_infinity": '{"x":-Infinity}',
        "json_float": '{"x":1.25}',
        "overflowing_float": '{"x":1e9999}',
        "negative_zero": '{"x":-0}',
        "top_level_array": "[]",
        "top_level_null": "null",
        "utf8_bom": '\ufeff{"x":1}',
        "unpaired_high_surrogate": '{"x":"\\ud800"}',
        "unpaired_low_surrogate": '{"x":"\\udfff"}',
        "oversized_integer": '{"x":' + "1" * 1025 + "}",
    }
    rejected: list[str] = []
    for label, payload in payloads.items():
        try:
            strict_json(payload)
        except (TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"strict JSON attack accepted:{label}")
    return rejected


def verify(
    certificate: Path = DEFAULT_CERTIFICATE,
    precision_bits: int = VERIFIER_PRECISION_BITS,
    attacks: bool = True,
) -> dict[str, Any]:
    require(type(precision_bits) is int and precision_bits >= 1024, "verifier precision")
    require(type(attacks) is bool, "attacks flag")
    ctx.prec = precision_bits
    document = strict_json(certificate.read_text(encoding="utf-8"))
    result = static_contract(document)
    values = load_inputs()
    contracts = verify_inherited_contracts(values)
    idx = indexes(values)
    require(len(idx["cores"]) == 24, "Round31 physical core count")
    round31_core_momentum_upper = max(
        max(abs(core.p0), abs(core.p1)) for core in idx["cores"]
    )
    require(
        round31_core_momentum_upper <= Q(1, 50),
        "independent Round31 core momentum bound",
    )
    nonempty_rows117 = sorted(
        (
            row
            for row in values["r117"]["common_refinement_rows"]
            if row["central_outer_source_child_nonempty"] is True
        ),
        key=lambda row: row["parent_round113_cell_id"],
    )
    require(len(nonempty_rows117) == 24, "independent R117 nonempty census")
    seed117 = nonempty_rows117[0]
    seed_generator = next(
        generator
        for generator in seed117["generator_families"]
        if "CENTRAL_OUTER" in generator["family"]
    )
    nonvacuity = result["nonvacuous_actual_child_fibre_existence"]
    require(
        nonvacuity["stable_interface_seed_parent_round113_cell_id"]
        == seed117["parent_round113_cell_id"]
        and nonvacuity["stable_interface_seed_operator_cell_id"]
        == seed_generator["stable_id_interface_sample"]["operator_cell_id"],
        "independent nonvacuity seed",
    )
    require(
        result["official_candidate_registry_rows_sha256"] == idx["registry_digest"],
        "official candidate registry digest",
    )
    require(
        result["typed_Borel_locator_precedent"]["locator_pattern_only"]
        == contracts["borel"]["source_interval_rank"],
        "R35 locator pattern",
    )
    require(
        result["natural_boundary_ledger"][
            "round117_boundary_ownership_ledger_sha256"
        ]
        == values["r117"]["boundary_ownership_ledger_sha256"],
        "R117 boundary ledger digest",
    )
    require(
        result["canonical_three_step_recut_frontier"][
            "global_invariant_cone_carries_every_image_curve"
        ]
        == contracts["cone"]["strict_forward_invariance"],
        "image cone contract",
    )
    require(
        result["canonical_three_step_recut_frontier"][
            "half_open_owner_contract_inherited_from_Round50"
        ]
        == contracts["ownership"]["half_open_endpoint_owner"],
        "half-open ownership inheritance",
    )
    replay = mathematical_replay(result, values, idx)
    semantic_attacks = mutation_tests(document, values, idx) if attacks else []
    json_attacks = strict_json_tests() if attacks else []
    verification = {
        "verdict": "PASS",
        "verification_precision_bits": precision_bits,
        "round120_producer_module_imported": False,
        "shared_round120_mathematics_helper_imported": False,
        **replay,
        "fixed_s_zero_grazing_parent_W_registry_verified": True,
        "Round31_compact_Q2_domain_reused": False,
        "independently_checked_Round31_physical_core_count": len(idx["cores"]),
        "independent_Round31_core_abs_momentum_upper": str(
            round31_core_momentum_upper
        ),
        "independently_checked_nonempty_R117_parent_count": len(
            nonempty_rows117
        ),
        "all_fixed_b_active_intersections_empty_or_connected_rank_0": True,
        "middle_actual_collision_H0_replay_count": 2 * 72,
        "three_step_adapted_recut_frontier_schema_verified": True,
        "actual_image_recut_instance_count": 0,
        "parameterized_actual_child_F1_F4_verified": True,
        "actual_child_F5_F6_installed": False,
        "rank3_actual_child_field_maturity": "4/18",
        "gate5_global_maturity": "10/18",
        "complete_18_field_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
        "attacks_enabled": attacks,
        "semantic_mutations_rejected": len(semantic_attacks),
        "semantic_mutation_labels": semantic_attacks,
        "strict_json_attacks_rejected": len(json_attacks),
        "strict_json_attack_labels": json_attacks,
        "certificate_sha256": sha256(certificate),
        "verified_upstream_and_helper_pins": {
            **UPSTREAM_PINS,
            **EXTRA_HELPER_PINS,
        },
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": verification,
        "result_sha256": digest(verification),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--precision-bits", type=int, default=VERIFIER_PRECISION_BITS)
    parser.add_argument(
        "--attacks",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="run semantic and strict-JSON hostile tests (default: enabled)",
    )
    args = parser.parse_args()
    document = verify(args.certificate, args.precision_bits, args.attacks)
    rendered = json.dumps(
        document,
        indent=2,
        sort_keys=True,
        ensure_ascii=True,
    ) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
