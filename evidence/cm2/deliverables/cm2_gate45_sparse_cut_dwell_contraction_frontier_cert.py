#!/usr/bin/env python3
"""Scheduled sparse-cut contraction blocks for the Gate-4/5 frontier.

The frozen fixed-core coefficient satisfies the stronger exact estimate

    b_core**2018 < 3/8.

Consequently one registered shell cut followed by one 2018-step core dwell
has coefficient below 45/64.  One raw all-key field-7 cut followed by six
such blocks has coefficient below 13213125/16375808.  Both yield deterministic
Green ledgers for arbitrarily many *scheduled* cuts and rational exponential
cut weights.  Physical occurrence-to-core incidence, no-hidden-cut dwell,
common strong-space typing, and cemetery payloads are not inferred.
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
    "cm2-gate4-incidence-shell-repeated-frontier-manifest-2026-07-16.json": (
        "c452c07f70db7bac05f23b97491db283707a9d84b15dff9e542a7272e22cd644"
    ),
    "cm2-gate4-fixed-core-green-kernel-unbounded-cut-frontier-manifest-2026-07-17.json": (
        "3475b2cf6af105b4d229e9683eb2f61433be2e4cefc8f1e8f2318c07762f3dd5"
    ),
    "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json": (
        "41c766d25b007944313db93b389a616d086a7318700a867e13d90aedd159be35"
    ),
}

B_CORE = Q(720269600000, 720626832337)
CORE_BLOCK_LENGTH = 2018
CORE_BLOCK_UPPER = Q(3, 8)
SHELL_CUT_FACTOR = Q(15, 8)
FIELD7_CUT_FACTOR = Q(580000, 1999)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integer_digest(value: int) -> str:
    width = max(1, (value.bit_length() + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "big")).hexdigest()


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        value = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(value, dict)
        loaded[name] = value

    shell = loaded[
        "cm2-gate4-incidence-shell-repeated-frontier-manifest-2026-07-16.json"
    ]
    fixed = loaded[
        "cm2-gate4-fixed-core-green-kernel-unbounded-cut-frontier-manifest-2026-07-17.json"
    ]
    field7 = loaded[
        "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json"
    ]

    assert shell["replay_summary"]["one_cut_mass_clock_factor_upper"] == "15/8"
    assert shell["replay_summary"]["fixed_core_unnormalized_arbitrary_n"] is True
    assert shell["verdict"]["native_or_arbitrary_unbounded_repeated_recovery"] == (
        "NOT_CERTIFIED"
    )

    core = fixed["result"]["fixed_core_green_kernel"]
    assert core["b_core"] == str(B_CORE)
    assert core["rational_exponential_moment"]["half_life_block"] == (
        CORE_BLOCK_LENGTH
    )
    assert core["rational_exponential_moment"]["exact_input"] == (
        "b_core^2018<1/2"
    )
    assert fixed["verdict"]["native_unbounded_repeated_cut_recovery"] == (
        "NOT_CERTIFIED"
    )

    registry = field7["result"]["all_key_all_component_characteristic_registry"]
    assert registry["candidate_key_count_covered"] == 441280
    assert registry[
        "uniform_unnormalized_characteristic_Z_multiplier_upper"
    ] == str(FIELD7_CUT_FACTOR)
    assert field7["verdict"]["field7_growth_contraction"] == "NOT_CERTIFIED"
    return loaded


def core_block_sharpening() -> dict[str, Any]:
    exact_power = B_CORE**CORE_BLOCK_LENGTH
    assert exact_power < CORE_BLOCK_UPPER
    assert CORE_BLOCK_UPPER < Q(1, 2)
    witness = {
        "numerator_sha256": integer_digest(exact_power.numerator),
        "denominator_sha256": integer_digest(exact_power.denominator),
    }
    return {
        "b_core": str(B_CORE),
        "block_length": CORE_BLOCK_LENGTH,
        "previous_certified_upper": "1/2",
        "sharpened_exact_rational_upper": "3/8",
        "exact_statement": "b_core^2018<3/8<1/2",
        "exact_power_witness_sha256": canonical_digest(witness),
        "comparison_replayed_with_exact_integer_arithmetic": True,
    }


def abstract_scheduled_ledger() -> dict[str, Any]:
    return {
        "recurrence": "E_(h+1)<=lambda E_h+J_(h+1), h>=0",
        "pointwise_solution": (
            "E_h<=lambda^h E_0+sum_{j=1}^h lambda^(h-j)J_j"
        ),
        "uniform_forcing_conclusion": (
            "if sup_h J_h<=J_*, then sup_h E_h<=E_0+J_*/(1-Lambda) "
            "whenever 0<=lambda<Lambda<1"
        ),
        "weighted_l1_conclusion": (
            "sum_{h>=0}w^h E_h<=(E_0+sum_{h>=1}w^h J_h)/"
            "(1-w Lambda) whenever w>1 and w Lambda<1"
        ),
        "arbitrary_registered_cut_count_h": True,
        "probabilistic_geometric_cut_count_tail_used": False,
        "deterministic_dwell_schedule_used": True,
        "weighted_forcing_summability_still_required_for_weighted_l1": True,
    }


def shell_scheduled_contraction() -> dict[str, Any]:
    coefficient_upper = SHELL_CUT_FACTOR * CORE_BLOCK_UPPER
    weight = Q(4, 3)
    weighted_upper = weight * coefficient_upper
    resolvent_upper = 1 / (1 - coefficient_upper)
    weighted_resolvent_upper = 1 / (1 - weighted_upper)
    assert coefficient_upper == Q(45, 64) < 1
    assert weighted_upper == Q(15, 16) < 1
    assert resolvent_upper == Q(64, 19)
    assert weighted_resolvent_upper == 16
    assert SHELL_CUT_FACTOR * B_CORE**CORE_BLOCK_LENGTH < coefficient_upper
    return {
        "registered_cycle": (
            "one same-interval two-view shell cut, then at least 2018 "
            "fixed-core steps before the next registered cut"
        ),
        "cut_factor_strict_upper": str(SHELL_CUT_FACTOR),
        "dwell_steps": CORE_BLOCK_LENGTH,
        "cycle_coefficient_strict_upper": str(coefficient_upper),
        "cycle_contraction": True,
        "pointwise_Green_resolvent_strict_upper": str(resolvent_upper),
        "rational_exponential_cut_weight": str(weight),
        "weighted_cycle_coefficient_strict_upper": str(weighted_upper),
        "weighted_Green_resolvent_strict_upper": str(weighted_resolvent_upper),
        "external_cut_count_tail_required_for_scheduled_scalar_ledger": False,
        "scheduled_shell_arbitrary_cut_count_contraction": "CERTIFIED_ABSTRACTLY",
    }


def field7_scheduled_contraction() -> dict[str, Any]:
    core_block_count = 6
    dwell_steps = CORE_BLOCK_LENGTH * core_block_count
    coefficient_upper = FIELD7_CUT_FACTOR * CORE_BLOCK_UPPER**core_block_count
    previous_block_upper = FIELD7_CUT_FACTOR * CORE_BLOCK_UPPER ** (
        core_block_count - 1
    )
    weight = Q(6, 5)
    weighted_upper = weight * coefficient_upper
    resolvent_upper = 1 / (1 - coefficient_upper)
    weighted_resolvent_upper = 1 / (1 - weighted_upper)

    assert previous_block_upper > 1
    assert coefficient_upper == Q(13213125, 16375808) < 1
    assert FIELD7_CUT_FACTOR * B_CORE**dwell_steps < coefficient_upper
    assert weighted_upper == Q(7927875, 8187904) < 1
    assert resolvent_upper == Q(16375808, 3162683)
    assert weighted_resolvent_upper == Q(8187904, 260029)
    assert weighted_resolvent_upper < 32
    return {
        "registered_cycle": (
            "one raw all-key field-7 characteristic restriction, then at "
            "least six 2018-step fixed-core blocks before the next registered cut"
        ),
        "all_key_cut_factor_upper": str(FIELD7_CUT_FACTOR),
        "covered_candidate_key_count": 441280,
        "core_block_count": core_block_count,
        "dwell_steps": dwell_steps,
        "five_coarse_blocks_do_not_contract": True,
        "six_coarse_blocks_are_first_contracting_count_for_the_3_over_8_bound": True,
        "cycle_coefficient_strict_upper": str(coefficient_upper),
        "cycle_contraction": True,
        "pointwise_Green_resolvent_strict_upper": str(resolvent_upper),
        "rational_exponential_cut_weight": str(weight),
        "weighted_cycle_coefficient_strict_upper": str(weighted_upper),
        "weighted_Green_resolvent_exact_upper": str(weighted_resolvent_upper),
        "weighted_Green_resolvent_simplified_strict_upper": "32",
        "external_cut_count_tail_required_for_scheduled_scalar_ledger": False,
        "scheduled_raw_field7_arbitrary_cut_count_contraction": (
            "CERTIFIED_ABSTRACTLY"
        ),
    }


def physical_installation_frontier() -> dict[str, Any]:
    return {
        "common_missing_interfaces": [
            "transport every physical cut occurrence into the frozen 24-core",
            "prove the post-cut range and core contraction use one common strong norm",
            "exclude hidden recuts throughout every required dwell interval",
            "supply strong complement and cemetery payload bounds",
            "prove weighted forcing summability for the transported recovery ledger",
        ],
        "shell_route_extra_interface": (
            "the registered cut must be the same one physical interval in both "
            "orientation views, exactly as required by the 15/8 estimate"
        ),
        "field7_route_extra_interfaces": [
            "materialize the physical homogeneous subbranch for every admitted key",
            "embed field 7 into a complete typed 18-field operator block",
            "show the raw characteristic loss is followed by 12108 valid core steps",
        ],
        "transported_occurrence_to_24_core_incidence": "NOT_CERTIFIED",
        "common_strong_space_DQ_MT_DQ_FACE": "NOT_CERTIFIED",
        "strong_complement_cemetery_payload": "NOT_CERTIFIED",
        "native_no_hidden_cut_dwell_schedule": "NOT_CERTIFIED",
        "complete_18_field_operator_blocks": "NOT_CERTIFIED",
        "technology_check": (
            "Demers-Liverani arXiv:2606.10155 section 5.6.1 notes that sparse "
            "holes with sufficient intervening mixing can recover cone contraction; "
            "it does not provide these CM2 physical interfaces"
        ),
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate45.sparse-cut-dwell-contraction-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "core_block_sharpening": core_block_sharpening(),
        "abstract_scheduled_ledger": abstract_scheduled_ledger(),
        "shell_scheduled_contraction": shell_scheduled_contraction(),
        "raw_field7_scheduled_contraction": field7_scheduled_contraction(),
        "physical_installation_frontier": physical_installation_frontier(),
        "strict_nonpromotion": {
            "abstract_schedule_implies_native_recut_schedule": False,
            "scalar_block_product_implies_common_strong_operator_typing": False,
            "field7_block_contraction_implies_other_17_fields": False,
            "scheduled_ledger_implies_transport_incidence": False,
            "scheduled_ledger_implies_cemetery_payload": False,
            "native_unbounded_repeated_cut_recovery": "NOT_CERTIFIED",
            "stable_quotient_PPE": "NOT_CERTIFIED",
            "three_norm_Kac_phase_closure": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("SCHEDULED_SHELL_ARBITRARY_CUT_CONTRACTION: CERTIFIED_ABSTRACTLY")
    print("SCHEDULED_RAW_FIELD7_ARBITRARY_CUT_CONTRACTION: CERTIFIED_ABSTRACTLY")
    print("NATIVE_PHYSICAL_DWELL_SCHEDULE: NOT_CERTIFIED")
    print("GATE4_GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
