#!/usr/bin/env python3
"""Typed Gate-4/5 payload frontier for the C24 first-return operator.

The collision-SRB Kac leaf already certifies a complete measurable first-
return partition modulo a null set and an induced L1 operator.  This leaf
materializes the exact *Borel-level* payload that follows from that theorem:
the level-set formulas, common forward/reverse restriction schema, symbolic
branch masses, invariant-area Jacobian, singular mass zero, and survivor
outer bounds.

It separately audits every strong payload.  The frozen unstable-Jacobian and
distortion data are only source-core/one-collision seeds; no full-dimensional
geometric R_n branch currently carries them.  Thus no Borel payload is
silently promoted to an unstable Jacobian, q_n envelope, common strong
carrier, or induced Lasota--Yorke coefficient.

The leaf also adds a rational uniform upper bound for the normalized mass of
the 24-core union.  It replays the exact axis/diagonal rectangle census from
the frozen core producer and uses rational upper bounds for dtheta/dt and the
elementary lower bound pi>3.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": (
        "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a"
    ),
    "cm2-gate45-induced-strong-coefficient-obstruction-manifest-2026-07-18.json": (
        "bad4bd8c12bccdcfad7210d44ed85fb023615c6db7aca9954e815a4729ce31e6"
    ),
    "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json": (
        "417464531cae76bf774bdc35f1d2f25799237d1efde39be8850cf3408740f271"
    ),
    "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json": (
        "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b"
    ),
    "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json": (
        "64f3820e2dc2f6d544be94bbe205fcf08f9517eef29131311e6fafa295060a93"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}

CORE_MASS_STRICT_LOWER = Q(147, 550000)
SAMPLE_HORIZONS = (0, 1, 544, 648, 1530, 2018, 2584, 3741, 12108)


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency path: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        if path.suffix == ".json":
            value = parse_json_text(path.read_text(encoding="utf-8"))
            require(isinstance(value, dict), f"dependency JSON type: {name}")
            loaded[name] = value

    core = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]
    registry = core["result"]["physical_return_core_registry"]
    require(registry["physical_compact_homogeneous_core_count"] == 24, "core count")
    require(registry["roof_histogram"] == {"1": 20, "2": 4}, "roof histogram")
    require(
        registry["collision_SRB_unnormalized_mass_rational_lower"] == "273/156250",
        "raw core mass lower",
    )
    require(
        registry[
            "collision_SRB_normalized_mass_strict_lower_using_pi_lt_22_over_7"
        ]
        == qstr(CORE_MASS_STRICT_LOWER),
        "normalized core mass lower",
    )

    kac = loaded[
        "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json"
    ]
    require(
        kac["verdict"]["collision_SRB_first_return_mass_identity"] == "CERTIFIED",
        "Kac mass identity",
    )
    require(
        kac["verdict"]["measurable_induced_L1_operator_baseline"] == "CERTIFIED",
        "induced L1 baseline",
    )
    require(
        kac["result"]["measurable_induced_L1_baseline"]["L1_operator_norm"] == "1",
        "induced L1 norm",
    )

    obstruction = loaded[
        "cm2-gate45-induced-strong-coefficient-obstruction-manifest-2026-07-18.json"
    ]
    require(
        obstruction["verdict"]["open_to_induced_coefficient_nonimplication"]
        == "CERTIFIED",
        "open-to-induced obstruction",
    )
    require(
        obstruction["result"]["missing_induced_strong_interface"][
            "required_record_count"
        ]
        == 13,
        "13-interface frontier",
    )

    selected = loaded[
        "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json"
    ]["result"]
    maturity = selected["Gate5_maturity_update"]
    require(maturity["completed_field_count_on_each_selected_component_level"] == 4, "4/18 maturity")
    require(maturity["field_5_6_completed_roof_level_slot_count"] == 0, "field 5/6 slots")

    universal = loaded[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]["result"]["universal_full_collision_branch_templates"]
    require(
        universal["field_5_inverse_Jacobian_seed"][
            "core_local_seed_on_all_24_positive_cores"
        ]
        is True,
        "field 5 seed",
    )
    require(
        universal["field_6_log_Jacobian_distortion_seed"][
            "core_local_seed_on_all_24_positive_cores"
        ]
        is True,
        "field 6 seed",
    )

    norm = loaded[
        "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json"
    ]["result"]
    require(norm["completion"]["physical_Borel_TV_Linf_prefix_suffix_constants"] is True, "Borel costs")
    require(norm["completion"]["standard_family_CM2_norm_lift"] is False, "standard norm open")
    require(norm["completion"]["flux_face_CM2_norm_lift"] is False, "flux norm open")
    require(norm["completion"]["dynamic_test_CM2_norm_lift"] is False, "test norm open")

    schema = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]
    require(schema["required_field_count_per_physical_homogeneous_level"] == 18, "18 fields")
    require(len(schema["required_fields"]) == 18, "18-field list")
    return loaded


def exact_core_mass_upper() -> dict[str, Any]:
    # Frozen producer census: eight axis rectangles (four per obstacle) and
    # sixteen diagonal rectangles (eight per obstacle).  In dr dp measure the
    # radius-weighted dt dp bases are respectively A and D below.
    radius_sum = Q(13, 25)
    axis_base = 4 * radius_sum * Q(1, 100) * Q(1, 250)
    diagonal_base = 8 * radius_sum * Q(1, 100) * Q(1, 25)
    require(axis_base == Q(13, 156250), "axis base")
    require(diagonal_base == Q(26, 15625), "diagonal base")
    require(axis_base + diagonal_base == Q(273, 156250), "base total")

    axis_derivative_upper = Q(1001, 1000)
    diagonal_derivative_upper = Q(1401, 1000)
    axis_square_witness = axis_derivative_upper**2 * (1 - Q(1, 50) ** 2)
    diagonal_square_witness = diagonal_derivative_upper**2 * (1 - Q(7, 10) ** 2)
    require(axis_square_witness > 1, "axis derivative witness")
    require(diagonal_square_witness > 1, "diagonal derivative witness")

    raw_upper = axis_base * axis_derivative_upper + diagonal_base * diagonal_derivative_upper
    require(raw_upper == Q(377273, 156250000), "raw upper")
    # Total collision volume = 4*pi*(R_G+R_W), and pi>3.
    normalized_upper = raw_upper / (4 * Q(3) * radius_sum)
    require(normalized_upper == Q(29021, 75000000), "normalized upper")
    require(CORE_MASS_STRICT_LOWER < normalized_upper < Q(1, 2500), "mass interval")

    return {
        "quantifier": "for_every_fixed_s_with_|s|<=1/400",
        "collision_coordinates": "dr_dp_with_dr=R*dtheta_and_t_coordinate",
        "core_census": {
            "axis_rectangle_count": 8,
            "diagonal_rectangle_count": 16,
            "source_obstacle_count_each": {"G": 12, "W": 12},
            "axis_radius_weighted_dt_dp_base": qstr(axis_base),
            "diagonal_radius_weighted_dt_dp_base": qstr(diagonal_base),
            "total_radius_weighted_dt_dp_base": qstr(axis_base + diagonal_base),
        },
        "dtheta_dt_formula": "1/sqrt(1-t^2)",
        "axis_abs_t_upper": "1/50",
        "axis_dtheta_dt_strict_upper": qstr(axis_derivative_upper),
        "axis_squared_strict_witness": qstr(axis_square_witness),
        "diagonal_abs_t_upper": "7/10",
        "diagonal_dtheta_dt_strict_upper": qstr(diagonal_derivative_upper),
        "diagonal_squared_strict_witness": qstr(diagonal_square_witness),
        "unnormalized_core_mass_strict_upper": qstr(raw_upper),
        "normalizer_formula": "4*pi*(R_G+R_W)",
        "normalizer_strict_lower_using_pi_gt_3": qstr(4 * Q(3) * radius_sum),
        "normalized_core_mass_strict_lower": qstr(CORE_MASS_STRICT_LOWER),
        "normalized_core_mass_strict_upper": qstr(normalized_upper),
        "normalized_core_mass_strict_upper_lt_1_over_2500": True,
        "exact_interval_statement": (
            "147/550000<mu_s(C_s)<29021/75000000<1/2500"
        ),
        "small_measure_alone_implies_open_hole_admissibility": False,
    }


def survivor_rows(core_upper: Q) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in SAMPLE_HORIZONS:
        kac_upper = Q(1, n + 1)
        if core_upper <= kac_upper:
            displayed = core_upper
            relation = "strictly_less_than"
            source = "core_mass_strict_upper"
        else:
            displayed = kac_upper
            relation = "less_than_or_equal_to"
            source = "general_Kac_integral_upper"
        rows.append({
            "n": n,
            "absolute_survivor_event": "mu_s(C_s_intersection_{tau_C_s_plus>n})",
            "displayed_upper": qstr(displayed),
            "relation": relation,
            "core_mass_strict_upper": qstr(core_upper),
            "Kac_first_moment_upper": qstr(kac_upper),
            "selected_source": source,
        })
    require(rows[6]["n"] == 2584 and rows[6]["selected_source"] == "general_Kac_integral_upper", "tail crossover")
    return rows


def measurable_return_payload(core_upper: Q) -> dict[str, Any]:
    rows = survivor_rows(core_upper)
    restriction_payload = {
        "core_id": "C24:frozen-core-rows:c3042515b4a244b064f1aaef97ee236c5d3f6078a53fe3fb9e865a1976853b2f",
        "parameter": "fixed_s",
        "level": "integer_n>=1",
        "source_atom": (
            "A_s,n=C_s_intersection_(intersection_{k=1}^{n-1}T_s^{-k}C_s^c)"
            "_intersection_T_s^{-n}C_s"
        ),
        "target_atom": "B_s,n=T_s^n(A_s,n)",
        "forward_map": "T_s^n_restricted_to_A_s,n",
        "reverse_map": "T_s^{-n}_restricted_to_B_s,n",
    }
    restriction_schema_id = "restriction-schema:" + canonical_digest(restriction_payload)
    return {
        "return_clock": "tau_C_s_plus=inf{n>=1:T_s^n(x)_in_C_s}",
        "source_atom_formula": restriction_payload["source_atom"],
        "target_atom_formula": restriction_payload["target_atom"],
        "source_atoms_partition_C_s_modulo_null": True,
        "target_atoms_partition_C_s_modulo_null": True,
        "all_preterminal_complement_guards_present_in_set_formula": True,
        "singular_orbit_cemetery_absolute_mass": "0",
        "nonreturning_absolute_mass": "0",
        "symbolic_absolute_branch_mass": "m_s,n=mu_s(A_s,n)=mu_s(B_s,n)",
        "symbolic_normalized_branch_mass": "p_s,n=m_s,n/mu_s(C_s)",
        "branch_masses_nonnegative": True,
        "absolute_mass_identity": "sum_{n>=1}m_s,n=mu_s(C_s)",
        "normalized_mass_identity": "sum_{n>=1}p_s,n=1",
        "common_forward_reverse_restriction_schema_id": restriction_schema_id,
        "common_restriction_payload_sha256": canonical_digest(restriction_payload),
        "restriction_instance_id_formula": restriction_schema_id + ":s={s}:n={n}",
        "forward_reverse_maps_are_mutual_inverses_modulo_singular_null": True,
        "collision_SRB_area_Jacobian_abs": "1",
        "log_collision_SRB_area_Jacobian_distortion": "0",
        "area_Jacobian_is_unstable_curve_Jacobian": False,
        "first_return_transfer_levels": "R_s,n=M_C L_s (M_Cc L_s)^(n-1) M_C",
        "survivor_levels": "Q_s,n=(M_Cc L_s)^n M_C",
        "sum_of_return_levels_is_induced_Perron_operator_on_L1_mu_C_s": True,
        "induced_L1_operator_norm": "1",
        "geometric_connected_branch_rows_materialized": 0,
        "numeric_exact_m_s_n_rows_materialized": 0,
        "stepwise_margin_rows_materialized": 0,
        "sample_absolute_survivor_outer_bounds": rows,
        "sample_absolute_survivor_outer_bounds_sha256": canonical_digest(rows),
        "exponential_survivor_tail": "NOT_CERTIFIED",
    }


def strong_seed_inventory(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    selected = loaded[
        "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json"
    ]["result"]
    universal = loaded[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]["result"]["universal_full_collision_branch_templates"]
    norm = loaded[
        "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json"
    ]["result"]
    schema = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]

    f5 = universal["field_5_inverse_Jacobian_seed"]
    f6 = universal["field_6_log_Jacobian_distortion_seed"]
    one = norm["one_collision_three_norm_seeds"]
    field_rows = []
    completed_names = {
        "nonempty_or_empty_domain_proof",
        "homogeneous_prefix_chart",
        "homogeneous_suffix_chart",
        "one_step_cut_growth_Z_sum",
    }
    seed_names = {"inverse_Jacobian_bound", "log_Jacobian_distortion_sum"}
    for index, name in enumerate(schema["required_fields"], start=1):
        if name in completed_names:
            status = "COMPLETED_ON_28_SELECTED_SOURCE_COMPONENT_LEVELS_ONLY"
        elif name in seed_names:
            status = "COMPONENT_LOCAL_ONE_COLLISION_SEED_ONLY"
        else:
            status = "MISSING_ON_SELECTED_SOURCE_COMPONENT_LEVELS"
        field_rows.append({
            "index": index,
            "field": name,
            "source_core_or_component_status": status,
            "completed_on_geometric_R_n_branch_count": 0,
        })
    require(len(field_rows) == 18, "field row count")
    require(sum(row["field"] in completed_names for row in field_rows) == 4, "4 fields")
    return {
        "selected_source_core_count": 24,
        "selected_source_component_level_count": 28,
        "completed_selected_source_fields": sorted(completed_names),
        "completed_selected_source_field_count": 4,
        "component_local_seed_fields": sorted(seed_names),
        "component_local_seed_field_count": 2,
        "field5_universal_adapted_inverse_strict_upper": f5[
            "universal_adapted_inverse_strict_upper"
        ],
        "field5_universal_Euclidean_inverse_strict_upper": f5[
            "universal_Euclidean_inverse_Jacobian_strict_upper"
        ],
        "field6_Holder_exponent": f6["Holder_exponent"],
        "field6_canonical_curve_log_variation_strict_upper": f6[
            "canonical_curve_log_variation_strict_upper"
        ],
        "physical_Borel_prefix_suffix_TV_Linf_constant": "1",
        "one_collision_forward_reverse_C1_subcost": "151*2^B_s",
        "one_collision_geometric_subcost": one[
            "uniform_finite_s_one_collision_geometric_subcost"
        ],
        "one_collision_log_Holder_constant": one[
            "uniform_finite_s_controlled_atom_log_Hoelder_constant"
        ],
        "initial_C_mesh": one["uniform_finite_s_initial_C_mesh"],
        "these_payloads_attach_to_full_geometric_R_n_Q_n_branches": False,
        "completed_geometric_R_n_strong_field_slot_count": 0,
        "field_rows": field_rows,
        "field_rows_sha256": canonical_digest(field_rows),
    }


def interface_maturity() -> dict[str, Any]:
    rows = [
        ("complete_collision_SRB_source_partition", "CERTIFIED_MOD_NULL_AS_BOREL_LEVEL_SETS", "NOT_MATERIALIZED_AS_GEOMETRIC_COMPONENTS"),
        ("raw_first_return_branch_records", "COUNTABLE_OPERATOR_LEVEL_SCHEMA_CERTIFIED", "ZERO_FULL_DIMENSIONAL_GEOMETRIC_ROWS"),
        ("all_preterminal_complement_guards", "CERTIFIED_IN_BOREL_SET_FORMULA", "ZERO_STEPWISE_STRICT_MARGIN_ROWS"),
        ("homogeneity_and_hidden_recut_margins", "NOT_CERTIFIED", "NOT_CERTIFIED"),
        ("branch_source_mass_m_n", "SYMBOLIC_MEASURES_AND_SUM_IDENTITY_CERTIFIED", "ZERO_NUMERIC_BRANCH_MASS_ROWS"),
        ("unstable_Jacobian_and_inverse", "AREA_JACOBIAN_ONE_PLUS_SOURCE_LOCAL_UNSTABLE_SEED", "NO_RETURN_BRANCH_UNSTABLE_JACOBIAN"),
        ("log_Jacobian_distortion_sum", "AREA_LOG_DISTORTION_ZERO_PLUS_SOURCE_LOCAL_SEED", "NO_RETURN_BRANCH_UNSTABLE_DISTORTION_SUM"),
        ("regular_standard_flux_dynamic_operator_costs", "BOREL_TV_LINF_AND_ONE_COLLISION_SEEDS", "NO_RETURN_WIDE_THREE_NORM_COST"),
        ("common_fw_rev_restriction_id_and_carriers", "COMMON_BOREL_LEVEL_RESTRICTION_SCHEMA_CERTIFIED", "NO_COMMON_GEOMETRIC_STRONG_CARRIERS"),
        ("physical_four_term_Kac_typing", "EXACT_BOUNDED_BOREL_KAC_LAYER_ONLY", "NO_FOUR_TERM_CM2_STRONG_TYPING"),
        ("singular_cemetery_and_survivor_outer_mass", "SINGULAR_ZERO_AND_KAC_SURVIVOR_OUTER_BOUNDS_CERTIFIED", "NO_WEIGHTED_STRONG_CEMETERY"),
        ("weighted_q_excursion_tail", "NOT_CERTIFIED", "NOT_CERTIFIED"),
        ("induced_common_space_contraction_coefficient", "MEASURABLE_L1_NORM_ONE_ONLY", "NOT_CERTIFIED"),
    ]
    records = [
        {
            "index": index,
            "field": field,
            "measurable_or_seed_payload": measurable,
            "geometric_strong_payload": strong,
            "complete_strong_record": False,
        }
        for index, (field, measurable, strong) in enumerate(rows, start=1)
    ]
    require(len(records) == 13, "interface count")
    require(not any(row["complete_strong_record"] for row in records), "no promotion")
    return {
        "required_interface_count": 13,
        "interfaces_with_nontrivial_measurable_or_seed_payload": sum(
            row["measurable_or_seed_payload"] != "NOT_CERTIFIED" for row in records
        ),
        "complete_geometric_strong_interface_count": 0,
        "records": records,
        "records_sha256": canonical_digest(records),
        "strong_completion_still_requires": (
            "full-dimensional connected R_n/Q_n refinement atoms with strict collision, "
            "homogeneity and hidden-recut margins; numeric m_n, unstable Jacobian, "
            "distortion, q_n, common strong carriers, and an exponential weighted tail"
        ),
    }


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    mass = exact_core_mass_upper()
    core_upper = Q(mass["normalized_core_mass_strict_upper"])
    result: dict[str, Any] = {
        "schema": "cm2.gate45.induced-strong-payload-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameterwise_not_joint_parameter_measure": True,
            "typing_policy": "Borel_area_payload_is_not_unstable_strong_payload",
        },
        "exact_C24_collision_SRB_mass_interval": mass,
        "measurable_first_return_payload": measurable_return_payload(core_upper),
        "source_core_strong_seed_inventory": strong_seed_inventory(loaded),
        "induced_interface_maturity": interface_maturity(),
        "strict_nonpromotion": {
            "small_core_measure_implies_open_hole_O1prime_O2": False,
            "Borel_level_sets_are_connected_geometric_branches": False,
            "invariant_area_Jacobian_is_unstable_curve_Jacobian": False,
            "symbolic_m_s_n_are_numeric_materialized_branch_masses": False,
            "common_Borel_restriction_schema_is_common_strong_carrier": False,
            "Kac_survivor_outer_bound_is_exponential_q_tail": False,
            "L1_operator_norm_one_is_strong_Lasota_Yorke_coefficient": False,
            "complete_18_field_operator_block_count": 0,
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("C24_NORMALIZED_COLLISION_SRB_MASS_STRICT_UPPER: 29021/75000000")
    print("MEASURABLE_RETURN_LEVEL_PAYLOAD: CERTIFIED_MOD_NULL")
    print("GEOMETRIC_RN_STRONG_PAYLOAD: NOT_CERTIFIED")
    print("GATE4_GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
