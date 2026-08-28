#!/usr/bin/env python3
"""Gate-4 same-occurrence weak-Borel payload frontier.

This certificate performs one deliberately narrow join.  It combines the
query-independent product occurrence record and its numerical recovery
moment with the already certified finite-signed-measure/bounded-Borel-test
operator constants.  The join supplies an honest weak-Borel source/test
payload on every controlled product record.  On the frozen corrected
64-row current it also supplies the actual singular two-coordinate Kac
payload and its height-nine lift.

The certificate does *not* promote total variation to any of the three CM2
strong norms.  In particular it does not manufacture standard-family Z,
regular-density variation, a dynamic-C1 inverse pullback, a flux-face atlas,
finite-s Gate-3 current matching, or native arbitrary-indicator recovery.
Complete C_fw, C_rev, q and Gate 4 therefore remain fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate4_product_same_occurrence_joint_moment_frontier_cert as product_cert


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json": (
        "67db1ec8aead4cbb0ff966e9136508636690074acb5959a6d705893eeef00eff"
    ),
    "cm2_gate4_product_same_occurrence_joint_moment_frontier_cert.py": (
        "759f6cb1d9cf97cb253326fe62bad6a00ae31beb9f6b1944ad41a0520f65bab3"
    ),
    "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json": (
        "64f3820e2dc2f6d544be94bbe205fcf08f9517eef29131311e6fafa295060a93"
    ),
    "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json": (
        "d5f563545c4ddaddfbb6b5cde5c4f5d8030247209e2284c06aeb9d3255a771f0"
    ),
    "cm2-v52-manifest.sha256": (
        "5cef5b8e60f0cfe2291da6bb34b2c57eed6cf2d1a13d164b74b566f752b6b368"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependencies() -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        if path.suffix == ".json":
            loaded[name] = json.loads(path.read_text(encoding="utf-8"))

    product_manifest = loaded[
        "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json"
    ]
    assert product_manifest["result_sha256"] == canonical_digest(
        product_cert.certify()
    )
    product = product_cert.certify()
    prefix = loaded[
        "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json"
    ]
    rows = loaded[
        "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json"
    ]

    record = product["same_occurrence_product_record"]
    assert record["base_occurrence_count"] == 64
    assert record["K_independent_of_physical_point_and_B"] is True
    assert record["same_K_j_and_restriction_in_both_orientations"] is True
    assert record["forward_reverse_are_alternative_nonadditive_views"] is True

    envelope = product["controlled_product_cost_envelope"]
    assert envelope["declared_controlled_envelope"] == (
        "C_prod(s,a,K)=2^K*exp(gamma*(R_fw+R_rev))*"
        "max(204*2^B_s(a),C_mesh,2)"
    )
    assert envelope["integral_C_prod_strict_upper_before_Z_N_inverse"] == (
        "1087598065258783059015245434544676138185728521412801591795461/"
        "6710886400000"
    )

    borel = prefix["result"]["physical_borel_prefix_suffix_constants"]
    for key in (
        "single_physical_prefix_pushforward_TV_norm_upper",
        "single_physical_suffix_pushforward_TV_norm_upper",
        "single_physical_prefix_test_pullback_Linf_norm_upper",
        "single_physical_suffix_test_pullback_Linf_norm_upper",
        "complete_partition_endpoint_pushforward_TV_norm_upper",
        "complete_partition_endpoint_test_pullback_Linf_norm_upper",
    ):
        assert borel[key] == "1"
    assert borel["return_height_upper"] == 9
    assert borel["normalized_tower_source_TV_norm_upper"] == "9"
    assert borel["unnormalized_Kac_test_sum_Linf_norm_upper"] == "9"

    kac = prefix["result"]["corrected_Kac_borel_output"]
    assert kac["global_event_current_TV_upper"] == "16128/5"
    assert kac["two_singular_coordinate_l1_TV_upper"] == "32256/5"
    assert kac[
        "worst_case_height_nine_phase_lifted_singular_l1_TV_upper"
    ] == "290304/5"
    assert kac["full_four_term_physical_CM2_output"] is False

    ledger = rows["result"]["corrected_global_occurrence_ledger"]
    assert ledger["maximal_physical_occurrence_count"] == 64
    assert ledger["one_corrected_m_per_occurrence"] is True
    assert ledger["all_singular_coordinate_pairs_share_mark_plus_one_minus_one"] is True
    return loaded


def weak_borel_operator_join() -> dict[str, Any]:
    return {
        "source_space": "M_b (finite signed Borel measures with total variation)",
        "test_space": "B_b (bounded Borel tests with sup norm)",
        "single_prefix_suffix_source_multiplier_upper": "1",
        "single_prefix_suffix_test_multiplier_upper": "1",
        "complete_disjoint_partition_source_multiplier_upper": "1",
        "complete_disjoint_partition_test_multiplier_upper": "1",
        "tower_height_upper": 9,
        "tower_source_or_test_multiplier_upper": "9",
        "record_identity": (
            "the same (e,s,K,j,owner,polarity,restriction) is used by both "
            "orientations before the bounded test is selected"
        ),
        "product_record_weak_Borel_source_test_payload": "CERTIFIED",
        "finite_s_parameter_window": "|s|<=1/400",
        "physical_finite_s_current_or_MT_DQ_match": False,
    }


def corrected_current_kac_join() -> dict[str, Any]:
    event = Q(16128, 5)
    pair = 2 * event
    lifted = 9 * pair
    assert pair == Q(32256, 5)
    assert lifted == Q(290304, 5)
    return {
        "scope": "the frozen corrected 64-row physical event current",
        "occurrence_count": 64,
        "one_positive_law_m_e_per_occurrence": True,
        "row_current_TV_rule": "||J_e||_TV<=2*m_e",
        "two_singular_coordinate_rule": "l1(TV)<=4*m_e",
        "height_nine_pair_rule": "l1(TV)<=36*m_e",
        "global_event_current_TV_upper": str(event),
        "global_two_coordinate_l1_TV_upper": str(pair),
        "global_height_nine_lifted_pair_l1_TV_upper": str(lifted),
        "corrected_current_physical_Borel_Kac_payload": "CERTIFIED",
        "full_four_term_physical_CM2_Kac_output": False,
    }


def controlled_product_payload() -> dict[str, Any]:
    c_mesh = Q(69986663973833932800)
    payload_coefficient = Q(36)
    assert c_mesh > payload_coefficient
    clocked_depth_upper = Q(2 * 3**50)
    payload_moment_upper = payload_coefficient * clocked_depth_upper
    product_integral_upper = Q(
        1087598065258783059015245434544676138185728521412801591795461,
        6710886400000,
    )
    return {
        "weak_Borel_height_nine_two_coordinate_coefficient_per_unit_occurrence_mass": str(
            payload_coefficient
        ),
        "C_mesh": str(c_mesh),
        "payload_coefficient_strictly_below_C_mesh": True,
        "clocked_depth_moment_strict_upper": str(clocked_depth_upper),
        "standalone_weak_Borel_payload_moment_strict_upper_per_unit_base_mass": str(
            payload_moment_upper
        ),
        "existing_C_prod_envelope_already_dominates_coefficient_36": True,
        "existing_C_prod_integral_strict_upper_before_Z_N_inverse": str(
            product_integral_upper
        ),
        "no_additional_forward_reverse_double_charge": True,
        "finite_s_product_record_weak_Borel_payload_envelope": "CERTIFIED",
        "physical_finite_s_signed_current_identification": "NOT_CERTIFIED",
    }


def exact_nonpromotion_boundary() -> dict[str, Any]:
    return {
        "TV_does_not_control_standard_family_Z": True,
        "TV_does_not_control_regular_density_variation": True,
        "Linf_does_not_control_dynamic_C1_inverse_pullback": True,
        "Borel_payload_does_not_supply_flux_face_atlas": True,
        "Gate3_finite_s_common_branch_record_current_MT_DQ": False,
        "native_countable_time_zero_boundary_Z_finite": False,
        "arbitrary_or_unbounded_repeated_indicator_recovery": False,
        "complete_same_occurrence_CM2_strong_operator_ledger": False,
        "complete_C_fw": False,
        "complete_C_rev": False,
        "final_q_max_Cfw_Crev_2m": False,
        "gate4_certified": False,
    }


def certify() -> dict[str, Any]:
    load_dependencies()
    result = {
        "schema": "cm2.gate4.product-borel-payload-frontier.v1",
        "provenance": {
            "dependency_count": len(DEPENDENCIES),
            "parameter_window": "|s|<=1/400",
            "maximal_occurrence_count": 64,
        },
        "weak_borel_operator_join": weak_borel_operator_join(),
        "corrected_current_kac_join": corrected_current_kac_join(),
        "controlled_product_payload": controlled_product_payload(),
        "exact_nonpromotion_boundary": exact_nonpromotion_boundary(),
    }
    result["internal_replay_digest"] = canonical_digest(
        {
            "operator": result["weak_borel_operator_join"],
            "kac": result["corrected_current_kac_join"],
            "product": result["controlled_product_payload"],
        }
    )
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE4_PRODUCT_WEAK_BOREL_OPERATOR_TEST_PAYLOAD: CERTIFIED")
    print("GATE4_CORRECTED_CURRENT_BOREL_KAC_PAYLOAD: CERTIFIED")
    print("GATE4_FINITE_S_PHYSICAL_CURRENT_MT_DQ_MATCH: NOT_CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
