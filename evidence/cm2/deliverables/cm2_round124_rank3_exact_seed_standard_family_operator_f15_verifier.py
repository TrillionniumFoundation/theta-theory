#!/usr/bin/env python3
"""Independent verifier for the Round124 exact-seed F15 certificate.

This verifier deliberately does not import the Round124 producer or any
Round124 proof helper.  It strict-parses and byte-pins the frozen inputs,
reconstructs the 72 tagged standard-family leg operators from Round123 data,
checks the finite-positive/projective/signed lift, proves the exact F15=34
arithmetic and raw-Z properness bounds, rebuilds the relative zero-cemetery
ledger, and reconstructs all 120 full-key F15 slots.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = (
    HERE
    / "cm2-round124-rank3-exact-seed-standard-family-operator-f15-2026-07-23.json"
)
DEFAULT_OUTPUT = (
    HERE
    / "cm2-round124-rank3-exact-seed-standard-family-operator-f15-verification-2026-07-23.json"
)
ROUND123 = (
    HERE
    / "cm2-round123-rank3-exact-seed-stage3-output-properization-f14-2026-07-23.json"
)
ROUND122 = (
    HERE
    / "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json"
)
ROUND124_PRODUCER = (
    HERE / "cm2_round124_rank3_exact_seed_standard_family_operator_f15.py"
)

CERTIFICATE_SCHEMA = (
    "cm2.round124.rank3-exact-seed-standard-family-operator-f15.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round124.rank3-exact-seed-standard-family-operator-f15-verification.v1"
)
VERIFIER_BITS = 3072
ROUND124_PRODUCER_SHA256 = (
    "084634863c9ecb9dd16fe1c16ef7ae286315525509b5d703df48359426a291a5"
)
ROUND123_SHA256 = (
    "d3d45e32e45d1a37d5364c0d5fc1f34b537190c2450b7e8f9ead729dc77fe993"
)
ROUND123_RESULT_SHA256 = (
    "e3ebade59b4bf8672f72f960a3fe0c13364ee27cd22f3ffe048b0ba7debd8296"
)
ROUND122_SHA256 = (
    "a7ed51149916bbf0d181b9cd45114cd11d81a5d30e72fea50b3336d1ead22028"
)

EXPECTED_PINS = {
    "deliverables/cm2_round123_rank3_exact_seed_stage3_output_properization_common.py": "8eda085e342655f20ef68a7aa0554b3bed3c26312d1261c49d4f6567d0bbb9e0",
    "deliverables/cm2_round123_rank3_exact_seed_stage3_output_properization_f14.py": "e00b85d722e3784c0c2427ea0f7b32f8306b9d706b902b22df334b8aa9b00c38",
    "deliverables/cm2-round123-rank3-exact-seed-stage3-output-properization-f14-2026-07-23.json": ROUND123_SHA256,
    "deliverables/cm2_round123_rank3_exact_seed_stage3_output_properization_f14_verifier.py": "eec966baae120a442f621e03f4575161545fc6d65604aba5f255a440c90f0625",
    "deliverables/cm2-round123-rank3-exact-seed-stage3-output-properization-f14-verification-2026-07-23.json": "37b70e60e1b9a66875e4565a44c115d50f55d718320fa79187d26bc45a1136d6",
    "deliverables/cm2-round123-rank3-exact-seed-stage3-output-properization-f14-report-2026-07-23.md": "a524de40d3abc818dd89f6b8dfba508f11fd81d6f4fc7fcac56130035655b25f",
    "deliverables/cm2-round123-rank3-exact-seed-stage3-output-properization-f14-cold-replay-2026-07-23.md": "9a4a33817de0b776599bb5b218863bfce8d867f63fe3350ea063643b738873ce",
    "deliverables/cm2-one-hundred-twenty-third-direct-assault-2026-07-23.md": "90fefb284bd0cf23d80a43fab1d6088d1146cf53678d32de574f272e9828acba",
    "deliverables/cm2-one-hundred-twenty-third-direct-assault-manifest-2026-07-23.sha256": "16a667bdbf3098c623199320a0cf85a34eba900ee376e476306ba7d5174b696b",
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json": ROUND122_SHA256,
    "deliverables/cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "deliverables/cm2_gate5_return_word_three_norm_frontier_cert.py": "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    "deliverables/cm2_gate5_return_word_three_norm_frontier_verifier.py": "0384acdd1f912b0d4b3bee84ff530358d9693893d1c5c64a1deabaede8e0867b",
    "deliverables/cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d",
    "deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py": "01e32ca209818f4077443a7692622c4202ab7f1066e2f95802185e2be7a2cc9a",
    "deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_verifier.py": "8074da51347aec415a864d87dc349cff25afa5a9a239febc53cc1ab015763d05",
    "deliverables/cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json": "3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3",
    "deliverables/cm2_gate4_inner_core_strong_product_bridge_frontier_cert.py": "4720669e90824e8c630276aa3d73606435eb88da2a51b2a756f651f56071605a",
    "deliverables/cm2_gate4_inner_core_strong_product_bridge_frontier_verifier.py": "1c814f82231c8a0181d53ec28f09d07c2528d40eda82a425b280a2858b0c0862",
    "deliverables/cm2_round88_gate5_f14_regalpha_strong_install_cert.py": "2bcb8ac5b5e94ad3335d09f16f62bd68520ad2936e12d79181f55989daca89b5",
    "deliverables/cm2_round88_gate5_f14_regalpha_strong_install_verifier.py": "c0d4936326e94db8146a0d9726d6136c9a70417800e40359f520162344027258",
    "deliverables/cm2-round88-gate5-f14-regalpha-strong-install-2026-07-22.json": "80e4ba31fb86b51410e90a5e1ef561f565cede65ef56792fc40364235d652993",
    "deliverables/cm2-round88-gate5-f14-regalpha-strong-install-audit-2026-07-22.json": "2d890384f3ffc8f3e1f71ae5e5607365f9e76a399e1da0f99cdd352c122953d5",
    "deliverables/cm2-round88-gate5-f14-regalpha-strong-install-report-2026-07-22.md": "fbb28e803a507857fac627f88a5421bc2121e98c897e46b1584bd804ee2bd88c",
    "deliverables/cm2_gate5_round61_complement_rn_borel_orlicz_frontier_cert.py": "c3b3a3abdb61019d01b86aca0dbec34a94991bf8b174cd634aa5d90fbb039c31",
    "deliverables/cm2_gate5_round61_complement_rn_borel_orlicz_frontier_verifier.py": "32cb2e062ef2a1781c500da6e700b87599a91f62936bad3cc9ea86bf3b687dbf",
    "deliverables/cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json": "59bce010748cccc1ffb829a9c232cab77185e6467433b3fed34988913649ae75",
    "deliverables/cm2-gate5-round61-complement-rn-borel-orlicz-frontier-assault-2026-07-20.md": "9554ac9dbf51d617ce01a442015613394cdc6e345cf021b88e1f20bdbd1e0065",
    "deliverables/cm2_gate5_round65_cross_time_sector_jordan_cemetery_frontier_cert.py": "91fe266ce29c9c9c7766307c2ca5c40544e1a225427ccafb02bfa5284ecc9be8",
    "deliverables/cm2_gate5_round65_cross_time_sector_jordan_cemetery_frontier_verifier.py": "c3af186e2edf0884bbda3354f8400a651fd15bc489371413e18bd90e7131a2ef",
    "deliverables/cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-manifest-2026-07-21.json": "43d80312d1ada853af84a9d8f5edd4393388a62ae3788e9fbcc1eaa4ea510ce5",
    "deliverables/cm2-gate5-round65-cross-time-sector-jordan-cemetery-frontier-assault-2026-07-21.md": "345215404cd3c2e634a614682fc7404fbca57721b3ddd1ab2959699734efd154",
}

DELTA = Q(1, 10**90)
VARTTHETA_P = Q(360134800, 360493663)
CP_STAR = Q(4 * 10**90 * 360493663, 358863)
Q_REG = Q(93, 100)
C_J = 15000000000000000000000000
REG_K = 500000000000000000000000000
F15 = 34
SOURCE_COEFFICIENTS = (Q(200), Q(100, 3), Q(200, 17))
OUTPUT_COEFFICIENTS = (Q(100, 3), Q(200, 17), Q(125, 4))


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(Q(value))


def parse_q(text: Any, *, positive: bool | None = None) -> Q:
    require(type(text) is str, "fraction type")
    require(
        re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", text) is not None,
        "canonical fraction syntax",
    )
    value = Q(text)
    require(str(value) == text, "reduced canonical fraction")
    if positive is True:
        require(value > 0, "positive fraction")
    if positive is False:
        require(value >= 0, "nonnegative fraction")
    return value


def reject_float(_value: str) -> Any:
    raise VerificationError("JSON floating-point numbers are forbidden")


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise VerificationError(f"duplicate JSON key:{key}")
        out[key] = value
    return out


def parse_strict_bytes(raw: bytes) -> Any:
    require(not raw.startswith(b"\xef\xbb\xbf"), "BOM")
    text = raw.decode("utf-8", errors="strict")
    return json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_float=reject_float,
        parse_constant=reject_float,
    )


def strict_document(path: Path, schema: str) -> dict[str, Any]:
    value = parse_strict_bytes(path.read_bytes())
    require(type(value) is dict, "top-level object")
    require(set(value) == {"schema", "result", "result_sha256"}, "envelope")
    require(value["schema"] == schema, "schema")
    require(type(value["result"]) is dict, "result object")
    require(type(value["result_sha256"]) is str, "result digest type")
    require(value["result_sha256"] == digest(value["result"]), "result digest")
    return value


def exact_keys(value: Any, keys: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == keys, f"{label} fields")


def validate_row(row: Any, keys: set[str], label: str) -> None:
    exact_keys(row, keys | {"row_sha256"}, label)
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    require(type(row["row_sha256"]) is str, f"{label} digest type")
    require(row["row_sha256"] == digest(payload), f"{label} digest")


def coordinate(row: dict[str, Any]) -> tuple[str, str, int]:
    return (
        row["official_word_key_id"],
        row["refined_homogeneous_subbranch_id"],
        row["roof_level_j"],
    )


def verify_upstream_bytes() -> None:
    require(
        sha256(ROUND124_PRODUCER) == ROUND124_PRODUCER_SHA256,
        "Round124 producer byte pin",
    )
    for relative, expected in EXPECTED_PINS.items():
        path = HERE.parent / relative
        require(path.is_file() and not path.is_symlink(), f"pin:{relative}")
        require(sha256(path) == expected, f"byte pin:{relative}")


def load_upstream() -> tuple[dict[str, Any], dict[str, Any]]:
    verify_upstream_bytes()
    r123_doc = strict_document(
        ROUND123,
        "cm2.round123.rank3-exact-seed-stage3-output-properization-f14.v1",
    )
    r122_doc = strict_document(
        ROUND122,
        "cm2.round122.rank3-exact-seed-physical-face-field-bridge.v1",
    )
    require(r123_doc["result_sha256"] == ROUND123_RESULT_SHA256, "R123 result")
    r123 = r123_doc["result"]
    r122 = r122_doc["result"]
    require(
        r123["rank3_seed_child_field_maturity"] == "15/18"
        and r123["count_ledger"]["combined_child_local_slot_count"] == 1800,
        "R123 maturity",
    )
    require(
        len(r123["accepted_norm_leg_output_rows"]) == 72
        and len(r123["gate5_F14_slot_rows"]) == 120
        and len(r123["input_child_output_partition_rows"]) == 24,
        "R123 census",
    )
    require(
        r123["gate5_actual_child_field_status"]["F15"]
        == "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
        "R123 F15 frontier",
    )
    require(
        r123["gate5_global_maturity"] == "10/18"
        and r123["complete_18_field_block_count"] == 0
        and r123["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "R123 fail closed",
    )
    f7 = [
        row
        for row in r122["gate5_F7_F13_F16_slot_rows"]
        if row["field_index"] == 7
    ]
    require(len(f7) == 120, "R122 F7 census")
    return r123, r122


TAG_KEYS = {
    "geometry_output_member_id",
    "tag_tuple_template",
    "tag_constructor",
    "geometry_coincidence_does_not_identify_tags",
}
CEMETERY_KEYS = {
    "cemetery_ledger_row_id",
    "common_child_id",
    "common_rank",
    "stage",
    "input_materialized_recut_instance_id",
    "output_geometry_member_ids",
    "output_member_count",
    "restricted_domain",
    "partition_is_disjoint_half_open_and_exhaustive",
    "internal_cut_is_owned_by_the_right_output_member",
    "source_parent_right_endpoint_remains_open",
    "endpoint_set_has_ell_star_measure_zero",
    "accepted_densities_are_ell_star_absolutely_continuous",
    "endpoint_mass_for_every_accepted_density",
    "input_mass_equals_sum_of_tagged_output_masses",
    "discarded_relative_domain_complement",
    "restricted_relative_cemetery_arrival_kernel",
    "cross_child_or_cross_input_member_deduplication",
    "geometry_coincidence_does_not_delete_tagged_mass",
    "ambient_pre_regularization_cemetery",
    "all_time_owner_cemetery",
}
FAMILY_LEG_KEYS = {
    "standard_family_leg_operator_row_id",
    "common_child_id",
    "common_rank",
    "stage",
    "official_word_key_id",
    "refined_homogeneous_subbranch_id",
    "roof_level_js",
    "roof_level_count",
    "actual_collision_owner",
    "actual_collision_chart",
    "input_materialized_recut_instance_id",
    "round123_accepted_norm_leg_output_row_id",
    "round123_accepted_norm_leg_output_row_sha256",
    "round123_same_key_F14_slot_ids",
    "round122_same_key_F7_slot_ids",
    "input_member_contract",
    "input_normalized_adapted_length_strict_lower",
    "input_adapted_length_less_or_equal_delta",
    "output_member_count",
    "output_geometry_member_ids",
    "output_member_tag_templates",
    "output_member_tag_templates_sha256",
    "output_normalized_adapted_length_strict_lower",
    "all_output_member_lengths_less_or_equal_delta",
    "conditional_pushforward",
    "mass_partition_identity",
    "memberwise_strong_norm_cost_strict_upper",
    "relative_zero_cemetery_ledger_row_id",
    "tag_preserving_and_no_cross_member_deduplication",
    "transparent_wall_roof_split_adds_no_family_operator_factor",
    "bypass_designated_b3_is_a_collision_angle",
}
F15_SLOT_KEYS = {
    "slot_id",
    "immutable_slot_key",
    "official_word_key_id",
    "refined_homogeneous_subbranch_id",
    "roof_level_j",
    "field_index",
    "field_name",
    "field_bound_semantics",
    "field_value_or_contract",
    "slot_status",
    "common_child_id",
    "stage",
    "round123_same_key_F14_slot_id",
    "round122_same_key_F7_slot_id",
    "standard_family_leg_operator_row_id",
    "standard_family_leg_operator_row_sha256",
    "input_materialized_recut_instance_id",
    "output_geometry_member_ids",
    "output_member_tag_templates_sha256",
    "relative_zero_cemetery_ledger_row_id",
    "finite_positive_family_then_countable_projective_completion",
    "signed_Jordan_standard_family_extension_installed",
    "transparent_wall_roof_split_adds_no_F15_factor",
    "roof_slot_value_is_one_step_not_direct_path_bound",
    "stage3_fragments_are_payload_not_F15_source_slots",
    "bypass_designated_b3_is_a_collision_angle",
}


def with_row_digest(row: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(row)
    out["row_sha256"] = digest(out)
    return out


def family_leg_id(child: str, stage: int) -> str:
    return "round124-standard-family-leg-operator:" + digest(
        ["round124-standard-family-leg-operator-v1", child, stage]
    )


def cemetery_id(child: str, stage: int) -> str:
    return "round124-relative-zero-cemetery-ledger:" + digest(
        ["round124-relative-zero-cemetery-ledger-v1", child, stage]
    )


def f15_slot_id(key: list[Any]) -> str:
    return "round124-gate5-f15-slot:" + digest(
        ["round124-gate5-f15-slot-v1", key]
    )


def reconstruct_tags(
    child: str, stage: int, output_ids: list[str]
) -> list[dict[str, Any]]:
    rows = []
    for output_id in output_ids:
        rows.append(
            with_row_digest(
                {
                    "geometry_output_member_id": output_id,
                    "tag_tuple_template": [
                        "<input-standard-family-member-id>",
                        child,
                        stage,
                        output_id,
                    ],
                    "tag_constructor": (
                        "round124-output-family-member:"
                        "sha256(canonical(tag_tuple_template))"
                    ),
                    "geometry_coincidence_does_not_identify_tags": True,
                }
            )
        )
    return rows


def reconstruct_cemetery_rows(r123: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    legs = sorted(
        r123["accepted_norm_leg_output_rows"],
        key=lambda row: (row["common_rank"], row["leg_index"]),
    )
    for leg in legs:
        stage = leg["leg_index"]
        rows.append(
            with_row_digest(
                {
                    "cemetery_ledger_row_id": cemetery_id(
                        leg["common_child_id"], stage
                    ),
                    "common_child_id": leg["common_child_id"],
                    "common_rank": leg["common_rank"],
                    "stage": stage,
                    "input_materialized_recut_instance_id": leg[
                        "input_materialized_recut_instance_id"
                    ],
                    "output_geometry_member_ids": leg["output_member_ids"],
                    "output_member_count": leg["output_member_count"],
                    "restricted_domain": (
                        "the materialized Round121 exact-seed common child at"
                        " this physical collision stage"
                    ),
                    "partition_is_disjoint_half_open_and_exhaustive": True,
                    "internal_cut_is_owned_by_the_right_output_member": True,
                    "source_parent_right_endpoint_remains_open": True,
                    "endpoint_set_has_ell_star_measure_zero": True,
                    "accepted_densities_are_ell_star_absolutely_continuous": True,
                    "endpoint_mass_for_every_accepted_density": "0",
                    "input_mass_equals_sum_of_tagged_output_masses": True,
                    "discarded_relative_domain_complement": "EMPTY",
                    "restricted_relative_cemetery_arrival_kernel": "ZERO",
                    "cross_child_or_cross_input_member_deduplication": "FORBIDDEN",
                    "geometry_coincidence_does_not_delete_tagged_mass": True,
                    "ambient_pre_regularization_cemetery": "NOT_INSTALLED",
                    "all_time_owner_cemetery": "NOT_INSTALLED",
                }
            )
        )
    require(len(rows) == 72, "reconstructed cemetery census")
    return rows


def reconstruct_family_rows(
    r123: dict[str, Any],
    r122: dict[str, Any],
    cemetery_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    f14_map = {coordinate(row): row for row in r123["gate5_F14_slot_rows"]}
    f7_map = {
        coordinate(row): row
        for row in r122["gate5_F7_F13_F16_slot_rows"]
        if row["field_index"] == 7
    }
    cemetery_map = {
        (row["common_child_id"], row["stage"]): row for row in cemetery_rows
    }
    input_lowers = ("1/200", "3/100", "17/200")
    output_lowers = ("3/100", "17/200", "4/125")
    rows = []
    legs = sorted(
        r123["accepted_norm_leg_output_rows"],
        key=lambda row: (row["common_rank"], row["leg_index"]),
    )
    for leg in legs:
        stage = leg["leg_index"]
        roof_keys = [
            (
                leg["official_word_key_id"],
                leg["refined_homogeneous_subbranch_id"],
                roof,
            )
            for roof in leg["roof_level_js"]
        ]
        tags = reconstruct_tags(
            leg["common_child_id"], stage, leg["output_member_ids"]
        )
        row = {
            "standard_family_leg_operator_row_id": family_leg_id(
                leg["common_child_id"], stage
            ),
            "common_child_id": leg["common_child_id"],
            "common_rank": leg["common_rank"],
            "stage": stage,
            "official_word_key_id": leg["official_word_key_id"],
            "refined_homogeneous_subbranch_id": leg[
                "refined_homogeneous_subbranch_id"
            ],
            "roof_level_js": leg["roof_level_js"],
            "roof_level_count": leg["roof_level_count"],
            "actual_collision_owner": leg["actual_collision_owner"],
            "actual_collision_chart": leg["actual_collision_chart"],
            "input_materialized_recut_instance_id": leg[
                "input_materialized_recut_instance_id"
            ],
            "round123_accepted_norm_leg_output_row_id": leg[
                "leg_output_row_id"
            ],
            "round123_accepted_norm_leg_output_row_sha256": leg["row_sha256"],
            "round123_same_key_F14_slot_ids": [
                f14_map[key]["slot_id"] for key in roof_keys
            ],
            "round122_same_key_F7_slot_ids": [
                f7_map[key]["slot_id"] for key in roof_keys
            ],
            "input_member_contract": {
                "tag": "<input-standard-family-member-id>",
                "mass": "M_a>0",
                "density": "rho_a>0",
                "normalization": "integral rho_a d ell_*=1",
                "Reg_alpha_upper": str(REG_K),
                "geometry_carrier": leg[
                    "input_materialized_recut_instance_id"
                ],
            },
            "input_normalized_adapted_length_strict_lower": input_lowers[stage],
            "input_adapted_length_less_or_equal_delta": True,
            "output_member_count": leg["output_member_count"],
            "output_geometry_member_ids": leg["output_member_ids"],
            "output_member_tag_templates": tags,
            "output_member_tag_templates_sha256": digest(tags),
            "output_normalized_adapted_length_strict_lower": output_lowers[stage],
            "all_output_member_lengths_less_or_equal_delta": True,
            "conditional_pushforward": {
                "alpha_aj": (
                    "integral_(input member preimage of output j)"
                    " rho_a d ell_*"
                ),
                "M_aj": "M_a*alpha_aj",
                "rho_aj_plus": (
                    "rho_a/(alpha_aj*J_star) transported to output j"
                ),
                "zero_alpha_output": "OMITTED",
            },
            "mass_partition_identity": "sum_j M_aj=M_a",
            "memberwise_strong_norm_cost_strict_upper": str(F15),
            "relative_zero_cemetery_ledger_row_id": cemetery_map[
                (leg["common_child_id"], stage)
            ]["cemetery_ledger_row_id"],
            "tag_preserving_and_no_cross_member_deduplication": True,
            "transparent_wall_roof_split_adds_no_family_operator_factor": True,
            "bypass_designated_b3_is_a_collision_angle": False,
        }
        rows.append(with_row_digest(row))
    require(
        len(rows) == 72
        and len({row["standard_family_leg_operator_row_id"] for row in rows})
        == 72,
        "reconstructed family row census",
    )
    require(
        sum(row["output_member_count"] for row in rows if row["stage"] == 2)
        == 216,
        "stage3 tagged payload census",
    )
    return rows


def reconstruct_f15_rows(
    r123: dict[str, Any],
    r122: dict[str, Any],
    family_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    family_map = {
        (row["common_child_id"], row["stage"]): row for row in family_rows
    }
    f7_map = {
        coordinate(row): row
        for row in r122["gate5_F7_F13_F16_slot_rows"]
        if row["field_index"] == 7
    }
    rows = []
    keys: set[str] = set()
    f14_rows = sorted(
        r123["gate5_F14_slot_rows"],
        key=lambda row: (
            row["common_child_id"],
            row["stage"],
            row["roof_level_j"],
        ),
    )
    for f14 in f14_rows:
        family = family_map[(f14["common_child_id"], f14["stage"])]
        immutable_key = [
            f14["official_word_key_id"],
            f14["refined_homogeneous_subbranch_id"],
            f14["roof_level_j"],
            "standard_family_operator_cost",
        ]
        key_text = canonical(immutable_key)
        require(key_text not in keys, "unique reconstructed F15 key")
        keys.add(key_text)
        row = {
            "slot_id": f15_slot_id(immutable_key),
            "immutable_slot_key": immutable_key,
            "official_word_key_id": f14["official_word_key_id"],
            "refined_homogeneous_subbranch_id": f14[
                "refined_homogeneous_subbranch_id"
            ],
            "roof_level_j": f14["roof_level_j"],
            "field_index": 15,
            "field_name": "standard_family_operator_cost",
            "field_bound_semantics": "STRICT_UPPER",
            "field_value_or_contract": "34",
            "slot_status": "CERTIFIED_ON_THIS_EXACT_SEED_COMMON_CHILD",
            "common_child_id": f14["common_child_id"],
            "stage": f14["stage"],
            "round123_same_key_F14_slot_id": f14["slot_id"],
            "round122_same_key_F7_slot_id": f7_map[coordinate(f14)]["slot_id"],
            "standard_family_leg_operator_row_id": family[
                "standard_family_leg_operator_row_id"
            ],
            "standard_family_leg_operator_row_sha256": family["row_sha256"],
            "input_materialized_recut_instance_id": family[
                "input_materialized_recut_instance_id"
            ],
            "output_geometry_member_ids": family["output_geometry_member_ids"],
            "output_member_tag_templates_sha256": family[
                "output_member_tag_templates_sha256"
            ],
            "relative_zero_cemetery_ledger_row_id": family[
                "relative_zero_cemetery_ledger_row_id"
            ],
            "finite_positive_family_then_countable_projective_completion": True,
            "signed_Jordan_standard_family_extension_installed": True,
            "transparent_wall_roof_split_adds_no_F15_factor": True,
            "roof_slot_value_is_one_step_not_direct_path_bound": True,
            "stage3_fragments_are_payload_not_F15_source_slots": True,
            "bypass_designated_b3_is_a_collision_angle": False,
        }
        rows.append(with_row_digest(row))
    require(len(rows) == len(keys) == 120, "reconstructed F15 census")
    require(
        Counter(row["stage"] for row in rows) == {0: 48, 1: 24, 2: 48},
        "F15 stage census",
    )
    return rows


def expected_domain() -> dict[str, Any]:
    return {
        "status": "CERTIFIED_ON_THE_24_MATERIALIZED_EXACT_SEED_CARRIERS",
        "positive_finite_family": {
            "form": "G={(M_a,rho_a,C_a)}_a",
            "carrier": (
                "each C_a is one of the materialized Round123 stage carriers"
            ),
            "mass": "M_a>0",
            "density": "rho_a>0",
            "normalization": "integral_(C_a) rho_a d ell_*=1",
            "regularity": f"Reg_(1/3)(rho_a)<={REG_K}",
            "repeated_geometry_with_distinct_input_tags": "PRESERVED",
        },
        "strong_standard_family_norm": (
            "||G||_SF=sum_a M_a*(1+Reg_(1/3)(rho_a)+1/L_a)"
        ),
        "adapted_boundary_projection": {
            "mass": "M(G)=sum_a M_a",
            "raw_Z_star": "Z_*(G)=sum_a M_a/L_a",
            "raw_Z_star_is_only_a_projection_of_the_strong_norm": True,
        },
        "positive_projective_scaling": (
            "lambda*(M_a,rho_a,C_a)=(lambda*M_a,rho_a,C_a)"
            " for lambda>0"
        ),
        "countable_completion": {
            "domain": (
                "countable tagged positive families with finite"
                " sum_a M_a*(1+Reg_a+1/L_a)"
            ),
            "extension": (
                "finite partial-family bounds pass by monotone convergence"
                " and Tonelli; the output retains every source tag"
            ),
            "cross_member_geometry_deduplication": "FORBIDDEN",
        },
        "signed_Jordan_completion": {
            "contract": (
                "apply the positive-family operator to positive and negative"
                " Jordan standard families separately and take the infimum"
                " over positive decompositions"
            ),
            "factor_two_added": False,
            "cancellation_used_to_improve_cost": False,
        },
    }


def expected_tonelli() -> dict[str, Any]:
    # The exact one-member inequality is inherited from Round123.  Summing it
    # over a finite tagged family is legitimate because all terms are
    # nonnegative.  Monotone convergence then gives the countable completion.
    require(F15 == 34, "F15 exact value")
    require(Q(F15) > Q(100, 3), "F15 pays inverse-length coefficient")
    require(
        Q(F15) - Q(100, 3) - DELTA * (1 + C_J) > 0,
        "F15 exact strong-norm gap",
    )
    require(Q_REG * REG_K + C_J < REG_K, "regularity cone invariance")
    return {
        "status": (
            "CERTIFIED_ON_EVERY_ACCEPTED_FINITE_POSITIVE_FAMILY_AND"
            "_ITS_COUNTABLE_PROJECTIVE_COMPLETION"
        ),
        "memberwise_source": (
            "the final Round123 arbitrary-density F14 theorem on each tagged"
            " family member"
        ),
        "conditional_pushforward": {
            "alpha_aj": "integral_(C_aj) rho_a d ell_*",
            "M_aj": "M_a*alpha_aj",
            "rho_aj_plus": (
                "rho_a/(alpha_aj*J_star) transported to the tagged output"
            ),
            "normalization": (
                "integral rho_aj_plus d ell_*^+=1 whenever alpha_aj>0"
            ),
            "zero_alpha_members": "OMITTED",
        },
        "per_input_member_mass_identity": "sum_j M_aj=M_a",
        "whole_family_mass_identity": "sum_(a,j) M_aj=sum_a M_a",
        "equal_output_mass_assumption": False,
        "Tonelli_lift": (
            "sum_(a,j) M_aj*(1+Reg_aj_plus+1/ell_aj)"
            " < 34*sum_a M_a*(1+Reg_a+1/L_a)"
        ),
        "one_step_F15_strict_upper": "34",
        "same_numeric_value_as_F14_but_distinct_typed_theorem": True,
        "F15_is_not_obtained_by_renaming_F14_slots": True,
        "fragment_or_member_count_multiplier": "NONE",
        "tag_preservation": (
            "output tag=(source-family-member,child,stage,geometry-output-id)"
        ),
        "roof_split": (
            "roof=2 gives two immutable field slots for one physical"
            " collision-family operator and does not duplicate mass or cost"
        ),
        "countable_extension": (
            "finite tagged partial sums increase to the countable output;"
            " monotone convergence preserves the strict uniform coefficient"
        ),
        "signed_extension_adds_no_factor_two": True,
    }


def expected_raw_z() -> dict[str, Any]:
    cp_delta = CP_STAR * DELTA
    require(VARTTHETA_P < 1, "adapted contraction")
    require(1 - VARTTHETA_P == Q(358863, 360493663), "theta gap")
    require(cp_delta == Q(1441974652, 358863), "Cp delta identity")
    source_gaps = [cp_delta - value for value in SOURCE_COEFFICIENTS]
    output_gaps = [cp_delta - value for value in OUTPUT_COEFFICIENTS]
    require(all(gap > 0 for gap in source_gaps + output_gaps), "properness")
    require(
        source_gaps[0] == Q(1370202052, 358863),
        "worst properness gap",
    )
    return {
        "status": "CERTIFIED_WITH_RECOVERY_CLOCK_ZERO",
        "adapted_boundary_functional": "Z_*(G)=sum_a M_a/L_a",
        "delta": "1/10^90",
        "numeric_growth_recurrence": (
            "Z_*(T G)<=vartheta_p*Z_*(G)+2*10^90*M(G)"
        ),
        "vartheta_p": qstr(VARTTHETA_P),
        "one_minus_vartheta_p": "358863/360493663",
        "adapted_C_p_star": qstr(CP_STAR),
        "adapted_C_p_star_times_delta": qstr(cp_delta),
        "stage_rows": [
            {
                "stage": stage,
                "source_inverse_length_coefficient": qstr(
                    SOURCE_COEFFICIENTS[stage]
                ),
                "output_inverse_length_coefficient": qstr(
                    OUTPUT_COEFFICIENTS[stage]
                ),
                "source_Z_star_strict_bound": (
                    f"Z_*<{qstr(SOURCE_COEFFICIENTS[stage])}*M/delta"
                ),
                "output_Z_star_strict_bound": (
                    f"Z_*<{qstr(OUTPUT_COEFFICIENTS[stage])}*M/delta"
                ),
                "source_Cp_margin_after_multiplying_by_delta": qstr(
                    source_gaps[stage]
                ),
                "output_Cp_margin_after_multiplying_by_delta": qstr(
                    output_gaps[stage]
                ),
                "source_and_output_are_strictly_proper": True,
            }
            for stage in range(3)
        ],
        "uniform_source_inverse_length_coefficient": "200",
        "uniform_output_inverse_length_coefficient": "100/3",
        "worst_strict_Cp_delta_margin": qstr(source_gaps[0]),
        "all_stage_inputs_already_proper": True,
        "all_stage_outputs_already_proper": True,
        "local_exact_seed_recovery_clock": 0,
        "no_recovery_iterate_is_applied": True,
        "raw_Z_star_is_not_the_complete_strong_standard_family_norm": True,
    }


def expected_scope_separation() -> dict[str, Any]:
    return {
        "status": "STRICT_TYPE_SEPARATION_CERTIFIED",
        "local_adapted_Z_star": {
            "definition": "sum_a M_a/L_a",
            "carrier": (
                "finite or countable tagged standard families on the"
                " Round121 exact-seed restricted regular domain"
            ),
            "role": "adapted inverse-length properness projection",
        },
        "Round61_raw_Z_col": {
            "definition": "integral 2^(K+1) d nu_j",
            "carrier": (
                "fixed-j owner/root collar law and labelled complement"
                " cemetery"
            ),
            "identified_with_local_Z_star": False,
            "finiteness_claimed_here": False,
        },
        "Round61_power_Orlicz": "NOT_INSTALLED_OR_PROMOTED",
        "Round62_outer_wZ_series": "NOT_INSTALLED_OR_PROMOTED",
        "Round65_all_time_sector_drift": "NOT_INSTALLED_OR_PROMOTED",
        "Round65_strong_positive_cemetery": "NOT_INSTALLED_OR_PROMOTED",
        "why_global_frontiers_do_not_block_this_local_F15": [
            "exactly three materialized collision stages",
            "finite exact output registry at every stage",
            "disjoint exhaustive half-open partitions",
            "no owner minimization or cross-j deduplication",
            "no discarded relative-domain complement",
            "all internal endpoints are null for accepted densities",
        ],
        "restricted_zero_cemetery_is_not_ambient_cemetery": True,
        "no_global_Orlicz_cemetery_or_owner_drift_claim": True,
    }


def expected_result(
    r123: dict[str, Any], r122: dict[str, Any]
) -> dict[str, Any]:
    cemetery_rows = reconstruct_cemetery_rows(r123)
    family_rows = reconstruct_family_rows(r123, r122, cemetery_rows)
    f15_rows = reconstruct_f15_rows(r123, r122, family_rows)

    result = copy.deepcopy(r123)
    for key in ("status", "strict_scope", "strict_nonclaims",
                "upstream_and_helper_pins"):
        result.pop(key)
    status = dict(r123["gate5_actual_child_field_status"])
    status["F15"] = "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN"
    count = dict(r123["count_ledger"])
    count.update(
        {
            "standard_family_leg_operator_row_count": 72,
            "relative_zero_cemetery_ledger_row_count": 72,
            "tagged_stage3_output_payload_member_count": 216,
            "new_F15_slot_count": 120,
            "inherited_Round123_slot_count": 1800,
            "combined_child_local_slot_count": 1920,
            "certified_child_local_field_count": 16,
            "complete_18_field_block_count": 0,
        }
    )
    f14_ids = [row["slot_id"] for row in r123["gate5_F14_slot_rows"]]
    f15_ids = [row["slot_id"] for row in f15_rows]
    result.update(
        {
            "status": (
                "CERTIFIED_EXACT_SEED_STANDARD_FAMILY_OPERATOR"
                "__F15_INSTALLED"
            ),
            "round123_contract": {
                "certificate_sha256": ROUND123_SHA256,
                "result_sha256": ROUND123_RESULT_SHA256,
                "actual_child_count": 24,
                "leg_output_row_count": 72,
                "stage3_output_payload_member_count": 216,
                "inherited_slot_count": 1800,
                "inherited_child_local_maturity": "15/18",
            },
            "accepted_standard_family_domain": expected_domain(),
            "standard_family_leg_operator_rows": family_rows,
            "standard_family_leg_operator_rows_sha256": digest(family_rows),
            "standard_family_Tonelli_lift_theorem": expected_tonelli(),
            "stagewise_raw_Z_and_properness": expected_raw_z(),
            "local_owner_zero_cemetery_ledger": {
                "status": (
                    "ZERO_CEMETERY_ARRIVAL_ON_THE_RESTRICTED_EXACT_SEED"
                    "_REGULAR_DOMAIN"
                ),
                "row_count": 72,
                "rows": cemetery_rows,
                "rows_sha256": digest(cemetery_rows),
                "half_open_exhaustive_partition_at_every_stage": True,
                "endpoint_nullity_for_every_accepted_density": True,
                "all_tagged_mass_is_preserved": True,
                "cross_child_deduplication": "FORBIDDEN",
                "ambient_or_all_time_cemetery": "NOT_CLAIMED",
            },
            "round50_65_scope_separation": expected_scope_separation(),
            "gate5_F15_slot_rows": f15_rows,
            "gate5_F15_slot_rows_sha256": digest(f15_rows),
            "combined_installed_child_local_slot_registry": {
                "Round123_inherited_slot_count": 1800,
                "Round123_combined_slot_ids_sha256": r123[
                    "combined_F1_F14_F16_slot_registry"
                ]["combined_slot_ids_sha256"],
                "Round123_F14_slot_ids_sha256": digest(f14_ids),
                "new_F15_slot_count": 120,
                "new_F15_slot_ids_sha256": digest(f15_ids),
                "combined_slot_count": 1920,
                "slot_count_per_certified_field": 120,
                "certified_field_indices": list(range(1, 17)),
                "uninstalled_field_indices": [17, 18],
                "all_keys_are_full_word_subbranch_roof_field_keys": True,
                "stage3_payload_members_are_not_source_slot_keys": True,
            },
            "count_ledger": count,
            "gate5_actual_child_field_status": status,
            "rank3_seed_child_field_maturity": "16/18",
            "remaining_uninstalled_child_fields": ["F17", "F18"],
            "gate5_global_maturity": "10/18",
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "cm2_verdict": "NO-GO_FOR_CLAIM",
            "strict_scope": (
                "one Round121 exact-b seed, its 24 materialized common"
                " children, their three materialized physical collision"
                " stages, and tagged positive/countable/signed standard"
                " families supported on those carriers"
            ),
            "strict_nonclaims": [
                "no replacement of the typed F15 theorem by renamed F14 slots",
                "no full Borel-b family materialization or uniform ranking",
                "no identification of local adapted Z_* with Round61 Z_col",
                "no global power-Orlicz or raw-collar finiteness theorem",
                "no ambient pre-regularization or all-time positive cemetery",
                "no owner minimization or cross-child output deduplication",
                "no creation of 216 output-payload F15 source slots",
                "no F17 dynamic-test operator cost",
                "no F18 operator phase block",
                "no complete 18-field block",
                "no global Gate5 maturity upgrade",
                "no endpoint-inclusive physical collar or cross-trace union reach",
                "no CM2 claim",
            ],
            "upstream_and_helper_pins": dict(sorted(EXPECTED_PINS.items())),
        }
    )
    return result


def evaluate_document(
    document: dict[str, Any],
    r123: dict[str, Any],
    r122: dict[str, Any],
    expected_cached: dict[str, Any] | None = None,
) -> dict[str, Any]:
    require(type(document) is dict, "document type")
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict, "certificate result type")
    require(document["result_sha256"] == digest(result), "certificate digest")

    expected = (
        expected_cached
        if expected_cached is not None
        else expected_result(r123, r122)
    )
    require(set(result) == set(expected), "closed result schema")

    # The complete Round123 payload is inherited without semantic mutation.
    replaced = {
        "status",
        "round123_contract",
        "accepted_standard_family_domain",
        "standard_family_leg_operator_rows",
        "standard_family_leg_operator_rows_sha256",
        "standard_family_Tonelli_lift_theorem",
        "stagewise_raw_Z_and_properness",
        "local_owner_zero_cemetery_ledger",
        "round50_65_scope_separation",
        "gate5_F15_slot_rows",
        "gate5_F15_slot_rows_sha256",
        "combined_installed_child_local_slot_registry",
        "count_ledger",
        "gate5_actual_child_field_status",
        "rank3_seed_child_field_maturity",
        "remaining_uninstalled_child_fields",
        "gate5_global_maturity",
        "complete_18_field_block_count",
        "gate5_block_count",
        "cm2_verdict",
        "strict_scope",
        "strict_nonclaims",
        "upstream_and_helper_pins",
    }
    for key in set(r123) - {
        "status", "strict_scope", "strict_nonclaims",
        "upstream_and_helper_pins",
    } - replaced:
        require(
            canonical(result[key]) == canonical(r123[key]),
            f"inherited R123 field:{key}",
        )

    require(
        canonical(result["upstream_and_helper_pins"])
        == canonical(dict(sorted(EXPECTED_PINS.items()))),
        "upstream pin table",
    )
    require(
        canonical(result["round123_contract"])
        == canonical(expected["round123_contract"]),
        "Round123 contract",
    )

    cemetery = result["local_owner_zero_cemetery_ledger"]
    exact_keys(
        cemetery,
        {
            "status",
            "row_count",
            "rows",
            "rows_sha256",
            "half_open_exhaustive_partition_at_every_stage",
            "endpoint_nullity_for_every_accepted_density",
            "all_tagged_mass_is_preserved",
            "cross_child_deduplication",
            "ambient_or_all_time_cemetery",
        },
        "cemetery ledger",
    )
    require(type(cemetery["rows"]) is list, "cemetery rows type")
    for row in cemetery["rows"]:
        validate_row(row, CEMETERY_KEYS, "cemetery row")
    require(cemetery["rows_sha256"] == digest(cemetery["rows"]),
            "cemetery rows digest")
    require(
        len(cemetery["rows"])
        == len({row["cemetery_ledger_row_id"] for row in cemetery["rows"]})
        == 72,
        "cemetery row census",
    )

    family_rows = result["standard_family_leg_operator_rows"]
    require(type(family_rows) is list, "family rows type")
    for row in family_rows:
        validate_row(row, FAMILY_LEG_KEYS, "family leg row")
        require(type(row["output_member_tag_templates"]) is list,
                "tag rows type")
        for tag in row["output_member_tag_templates"]:
            validate_row(tag, TAG_KEYS, "output tag")
        require(
            row["output_member_tag_templates_sha256"]
            == digest(row["output_member_tag_templates"]),
            "tag rows digest",
        )
        require(
            type(row["common_rank"]) is int
            and type(row["stage"]) is int
            and type(row["output_member_count"]) is int,
            "family integer fields",
        )
    require(
        result["standard_family_leg_operator_rows_sha256"]
        == digest(family_rows),
        "family rows digest",
    )
    require(
        len(family_rows)
        == len({row["standard_family_leg_operator_row_id"]
                for row in family_rows})
        == 72,
        "family row census",
    )
    require(
        Counter(row["stage"] for row in family_rows)
        == {0: 24, 1: 24, 2: 24},
        "family stage census",
    )
    require(
        sum(row["output_member_count"] for row in family_rows
            if row["stage"] == 2)
        == 216,
        "stage3 payload member census",
    )

    f15_rows = result["gate5_F15_slot_rows"]
    require(type(f15_rows) is list, "F15 rows type")
    for row in f15_rows:
        validate_row(row, F15_SLOT_KEYS, "F15 slot")
        require(
            type(row["roof_level_j"]) is int
            and type(row["field_index"]) is int
            and type(row["stage"]) is int,
            "F15 integer fields",
        )
        require(
            row["immutable_slot_key"]
            == [
                row["official_word_key_id"],
                row["refined_homogeneous_subbranch_id"],
                row["roof_level_j"],
                "standard_family_operator_cost",
            ],
            "F15 immutable key",
        )
        require(
            row["slot_id"] == f15_slot_id(row["immutable_slot_key"]),
            "F15 slot constructor",
        )
    require(
        result["gate5_F15_slot_rows_sha256"] == digest(f15_rows),
        "F15 rows digest",
    )
    require(
        len(f15_rows)
        == len({canonical(row["immutable_slot_key"]) for row in f15_rows})
        == len({row["slot_id"] for row in f15_rows})
        == 120,
        "F15 slot census",
    )
    require(
        Counter(row["stage"] for row in f15_rows)
        == {0: 48, 1: 24, 2: 48},
        "F15 stage census",
    )

    # Exact rational audit, independent of stored prose.
    raw = result["stagewise_raw_Z_and_properness"]
    exact_keys(raw, set(expected_raw_z()), "raw-Z theorem")
    require(parse_q(raw["vartheta_p"]) == VARTTHETA_P, "theta value")
    require(parse_q(raw["one_minus_vartheta_p"]) == 1 - VARTTHETA_P,
            "theta complement")
    require(parse_q(raw["adapted_C_p_star"]) == CP_STAR, "Cp value")
    require(
        parse_q(raw["adapted_C_p_star_times_delta"]) == CP_STAR * DELTA,
        "Cp delta value",
    )
    require(type(raw["stage_rows"]) is list and len(raw["stage_rows"]) == 3,
            "raw-Z stage rows")
    for stage, row in enumerate(raw["stage_rows"]):
        require(type(row["stage"]) is int and row["stage"] == stage,
                "raw-Z stage")
        src = parse_q(row["source_inverse_length_coefficient"],
                      positive=True)
        out = parse_q(row["output_inverse_length_coefficient"],
                      positive=True)
        src_gap = parse_q(
            row["source_Cp_margin_after_multiplying_by_delta"],
            positive=True,
        )
        out_gap = parse_q(
            row["output_Cp_margin_after_multiplying_by_delta"],
            positive=True,
        )
        require(src == SOURCE_COEFFICIENTS[stage], "source coefficient")
        require(out == OUTPUT_COEFFICIENTS[stage], "output coefficient")
        require(src_gap == CP_STAR * DELTA - src, "source Cp gap")
        require(out_gap == CP_STAR * DELTA - out, "output Cp gap")
    require(raw["local_exact_seed_recovery_clock"] == 0
            and type(raw["local_exact_seed_recovery_clock"]) is int,
            "recovery clock")

    require(
        canonical(result["accepted_standard_family_domain"])
        == canonical(expected_domain()),
        "accepted family domain",
    )
    require(
        canonical(result["standard_family_Tonelli_lift_theorem"])
        == canonical(expected_tonelli()),
        "Tonelli theorem",
    )
    require(
        canonical(result["round50_65_scope_separation"])
        == canonical(expected_scope_separation()),
        "scope separation",
    )
    require(
        canonical(raw) == canonical(expected_raw_z()),
        "raw-Z theorem exact",
    )

    # Full independent reconstruction is the final semantic comparison.
    require(
        canonical(result["local_owner_zero_cemetery_ledger"])
        == canonical(expected["local_owner_zero_cemetery_ledger"]),
        "reconstructed cemetery ledger",
    )
    require(
        canonical(family_rows)
        == canonical(expected["standard_family_leg_operator_rows"]),
        "reconstructed family rows",
    )
    require(
        canonical(f15_rows) == canonical(expected["gate5_F15_slot_rows"]),
        "reconstructed F15 slots",
    )
    for key in (
        "combined_installed_child_local_slot_registry",
        "count_ledger",
        "gate5_actual_child_field_status",
        "rank3_seed_child_field_maturity",
        "remaining_uninstalled_child_fields",
        "gate5_global_maturity",
        "complete_18_field_block_count",
        "gate5_block_count",
        "cm2_verdict",
        "status",
        "strict_scope",
        "strict_nonclaims",
    ):
        require(
            canonical(result[key]) == canonical(expected[key]),
            f"final state:{key}",
        )
    require(canonical(result) == canonical(expected), "complete result")
    return {
        "family_leg_row_count": len(family_rows),
        "relative_zero_cemetery_row_count": len(cemetery["rows"]),
        "stage3_tagged_payload_member_count": sum(
            row["output_member_count"] for row in family_rows
            if row["stage"] == 2
        ),
        "F15_slot_count": len(f15_rows),
        "F15_stage_slot_counts": {
            str(stage): sum(row["stage"] == stage for row in f15_rows)
            for stage in range(3)
        },
        "combined_child_local_slot_count": result["count_ledger"][
            "combined_child_local_slot_count"
        ],
        "rank3_seed_child_field_maturity": result[
            "rank3_seed_child_field_maturity"
        ],
        "gate5_global_maturity": result["gate5_global_maturity"],
        "complete_18_field_block_count": result[
            "complete_18_field_block_count"
        ],
        "cm2_verdict": result["cm2_verdict"],
    }


def resign(document: dict[str, Any]) -> None:
    """Re-sign every Round124 nested digest after a semantic mutation."""
    result = document["result"]
    cemetery = result.get("local_owner_zero_cemetery_ledger")
    if type(cemetery) is dict and type(cemetery.get("rows")) is list:
        for row in cemetery["rows"]:
            if type(row) is dict and "row_sha256" in row:
                row["row_sha256"] = digest(
                    {k: v for k, v in row.items() if k != "row_sha256"}
                )
        cemetery["rows_sha256"] = digest(cemetery["rows"])
    family_rows = result.get("standard_family_leg_operator_rows")
    if type(family_rows) is list:
        for row in family_rows:
            if type(row) is not dict:
                continue
            tags = row.get("output_member_tag_templates")
            if type(tags) is list:
                for tag in tags:
                    if type(tag) is dict and "row_sha256" in tag:
                        tag["row_sha256"] = digest(
                            {k: v for k, v in tag.items()
                             if k != "row_sha256"}
                        )
                row["output_member_tag_templates_sha256"] = digest(tags)
            if "row_sha256" in row:
                row["row_sha256"] = digest(
                    {k: v for k, v in row.items() if k != "row_sha256"}
                )
        result["standard_family_leg_operator_rows_sha256"] = digest(
            family_rows
        )
    f15_rows = result.get("gate5_F15_slot_rows")
    if type(f15_rows) is list:
        family_map = {}
        if type(family_rows) is list:
            family_map = {
                row.get("standard_family_leg_operator_row_id"): row
                for row in family_rows if type(row) is dict
            }
        for row in f15_rows:
            if type(row) is not dict:
                continue
            family = family_map.get(row.get("standard_family_leg_operator_row_id"))
            if family is not None:
                row["standard_family_leg_operator_row_sha256"] = family.get(
                    "row_sha256"
                )
                row["output_member_tag_templates_sha256"] = family.get(
                    "output_member_tag_templates_sha256"
                )
            if "row_sha256" in row:
                row["row_sha256"] = digest(
                    {k: v for k, v in row.items() if k != "row_sha256"}
                )
        result["gate5_F15_slot_rows_sha256"] = digest(f15_rows)
    document["result_sha256"] = digest(result)


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    target = root
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value


def delete_path(root: Any, path: tuple[Any, ...]) -> None:
    target = root
    for part in path[:-1]:
        target = target[part]
    del target[path[-1]]


def semantic_mutations(
    certificate: dict[str, Any],
    r123: dict[str, Any],
    r122: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    cases: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def setter(label: str, path: tuple[Any, ...], value: Any) -> None:
        cases.append((label, lambda d, p=path, v=value: set_path(d, p, v)))

    def deleter(label: str, path: tuple[Any, ...]) -> None:
        cases.append((label, lambda d, p=path: delete_path(d, p)))

    r = ("result",)
    setter("schema swap", ("schema",), "cm2.round124.mutant.v1")
    deleter("missing result field", r + ("status",))
    setter("unknown result field", r + ("mutant_unknown",), True)
    setter("status downgrade", r + ("status",), "FRONTIER_ONLY")
    setter("local maturity virtual 17", r + ("rank3_seed_child_field_maturity",),
           "17/18")
    setter("global maturity virtual 11", r + ("gate5_global_maturity",), "11/18")
    setter("complete block virtual one",
           r + ("complete_18_field_block_count",), 1)
    setter("gate block virtual one", r + ("gate5_block_count",), 1)
    setter("CM2 virtual GO", r + ("cm2_verdict",), "GO_FOR_CLAIM")
    setter("F17 virtual install",
           r + ("gate5_actual_child_field_status", "F17"),
           "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN")
    setter("F18 virtual install",
           r + ("gate5_actual_child_field_status", "F18"),
           "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN")
    setter("remaining fields omit F17",
           r + ("remaining_uninstalled_child_fields",), ["F18"])
    setter("combined count virtual", r + ("count_ledger",
           "combined_child_local_slot_count"), 2040)
    setter("certified field count virtual",
           r + ("count_ledger", "certified_child_local_field_count"), 17)
    setter("F15 count virtual", r + ("count_ledger", "new_F15_slot_count"), 216)
    setter("tag payload count virtual", r + ("count_ledger",
           "tagged_stage3_output_payload_member_count"), 217)
    setter("Round123 contract result", r + ("round123_contract",
           "result_sha256"), "0" * 64)
    setter("Round123 contract inherited slots", r + ("round123_contract",
           "inherited_slot_count"), 1920)
    setter("upstream byte pin", r + ("upstream_and_helper_pins",
           next(iter(EXPECTED_PINS))), "0" * 64)
    deleter("upstream pin removed", r + ("upstream_and_helper_pins",
            next(iter(EXPECTED_PINS))))
    setter("inherited Round123 geometry altered",
           r + ("stage3_adapted_coordinate_contract", "actual_collision_chart"),
           "S")

    # Standard-family domain and the typed Tonelli lift.
    setter("positive mass relaxed", r + ("accepted_standard_family_domain",
           "positive_finite_family", "mass"), "M_a>=0")
    setter("density positivity relaxed", r + ("accepted_standard_family_domain",
           "positive_finite_family", "density"), "rho_a>=0")
    setter("normalization removed", r + ("accepted_standard_family_domain",
           "positive_finite_family", "normalization"), "NONE")
    setter("regularity cone enlarged", r + ("accepted_standard_family_domain",
           "positive_finite_family", "regularity"), "UNBOUNDED")
    setter("strong norm loses inverse length",
           r + ("accepted_standard_family_domain",
                "strong_standard_family_norm"),
           "sum_a M_a*(1+Reg_a)")
    setter("raw Z renamed full norm", r + ("accepted_standard_family_domain",
           "adapted_boundary_projection",
           "raw_Z_star_is_only_a_projection_of_the_strong_norm"), False)
    setter("countable finite norm removed", r + ("accepted_standard_family_domain",
           "countable_completion", "domain"), "all tagged families")
    setter("geometry dedup allowed", r + ("accepted_standard_family_domain",
           "countable_completion", "cross_member_geometry_deduplication"),
           "ALLOWED")
    setter("Jordan factor two", r + ("accepted_standard_family_domain",
           "signed_Jordan_completion", "factor_two_added"), True)
    setter("Jordan cancellation", r + ("accepted_standard_family_domain",
           "signed_Jordan_completion", "cancellation_used_to_improve_cost"),
           True)

    t = r + ("standard_family_Tonelli_lift_theorem",)
    setter("F15 value lowered 33", t + ("one_step_F15_strict_upper",), "33")
    setter("F15 value inflated 216", t + ("one_step_F15_strict_upper",), "216")
    setter("F15 renamed F14", t + ("F15_is_not_obtained_by_renaming_F14_slots",),
           False)
    setter("typed theorem conflated", t + (
           "same_numeric_value_as_F14_but_distinct_typed_theorem",), False)
    setter("alpha masses equal", t + ("equal_output_mass_assumption",), True)
    setter("mass partition deleted", t + ("per_input_member_mass_identity",),
           "UNKNOWN")
    setter("whole family mass deleted", t + ("whole_family_mass_identity",),
           "UNKNOWN")
    setter("fragment multiplier 216", t + ("fragment_or_member_count_multiplier",),
           "216")
    setter("J star removed", t + ("conditional_pushforward", "rho_aj_plus"),
           "rho_a/alpha_aj")
    setter("conditional normalization removed",
           t + ("conditional_pushforward", "normalization"), "NOT_PROVED")
    setter("zero alpha retained", t + ("conditional_pushforward",
           "zero_alpha_members"), "KEPT")
    setter("tag preservation disabled", t + ("tag_preservation",), "NONE")
    setter("roof split duplicates cost", t + ("roof_split",),
           "roof=2 duplicates operator")
    setter("countable extension missing", t + ("countable_extension",),
           "NOT_INSTALLED")
    setter("signed extension factor", t + ("signed_extension_adds_no_factor_two",),
           False)
    setter("Tonelli inequality fragmentwise", t + ("Tonelli_lift",),
           "cost(fragment)<=34*M_fragment")

    z = r + ("stagewise_raw_Z_and_properness",)
    setter("theta contraction changed", z + ("vartheta_p",), "1")
    setter("theta gap changed", z + ("one_minus_vartheta_p",), "0")
    setter("Cp changed", z + ("adapted_C_p_star",), "1")
    setter("Cp delta changed", z + ("adapted_C_p_star_times_delta",), "200")
    setter("growth additive debt removed", z + ("numeric_growth_recurrence",),
           "Z_*(TG)<=vartheta_p*Z_*(G)")
    setter("recovery clock one", z + ("local_exact_seed_recovery_clock",), 1)
    setter("recovery iterate applied", z + ("no_recovery_iterate_is_applied",),
           False)
    setter("raw Z promoted strong", z + (
           "raw_Z_star_is_not_the_complete_strong_standard_family_norm",), False)
    setter("uniform source lowered", z + (
           "uniform_source_inverse_length_coefficient",), "199")
    setter("uniform output lowered", z + (
           "uniform_output_inverse_length_coefficient",), "31")
    for stage in range(3):
        setter(
            f"stage {stage} source coefficient",
            z + ("stage_rows", stage, "source_inverse_length_coefficient"),
            "1",
        )
        setter(
            f"stage {stage} output coefficient",
            z + ("stage_rows", stage, "output_inverse_length_coefficient"),
            "1",
        )
        setter(
            f"stage {stage} source gap",
            z + (
                "stage_rows", stage,
                "source_Cp_margin_after_multiplying_by_delta",
            ),
            "1",
        )
        setter(
            f"stage {stage} output proper false",
            z + ("stage_rows", stage,
                 "source_and_output_are_strictly_proper"),
            False,
        )

    scope = r + ("round50_65_scope_separation",)
    setter("Z star identified with Z col", scope + ("Round61_raw_Z_col",
           "identified_with_local_Z_star"), True)
    setter("Z col finiteness promoted", scope + ("Round61_raw_Z_col",
           "finiteness_claimed_here"), True)
    setter("Orlicz promoted", scope + ("Round61_power_Orlicz",), "INSTALLED")
    setter("outer series promoted", scope + ("Round62_outer_wZ_series",),
           "INSTALLED")
    setter("all time drift promoted", scope + ("Round65_all_time_sector_drift",),
           "INSTALLED")
    setter("strong cemetery promoted", scope + (
           "Round65_strong_positive_cemetery",), "INSTALLED")
    setter("relative cemetery ambient", scope + (
           "restricted_zero_cemetery_is_not_ambient_cemetery",), False)
    setter("global nonclaim removed", scope + (
           "no_global_Orlicz_cemetery_or_owner_drift_claim",), False)

    # Census/list attacks are fully re-signed.
    cases.append(("delete cemetery row", lambda d:
                  d["result"]["local_owner_zero_cemetery_ledger"]["rows"].pop()))
    cases.append(("duplicate cemetery row", lambda d:
                  d["result"]["local_owner_zero_cemetery_ledger"]["rows"].append(
                      copy.deepcopy(d["result"][
                          "local_owner_zero_cemetery_ledger"]["rows"][0]))))
    cases.append(("reorder cemetery rows", lambda d:
                  d["result"]["local_owner_zero_cemetery_ledger"]["rows"].reverse()))
    setter("cemetery top mass false", r + (
           "local_owner_zero_cemetery_ledger",
           "all_tagged_mass_is_preserved"), False)
    setter("cemetery top dedup allowed", r + (
           "local_owner_zero_cemetery_ledger",
           "cross_child_deduplication"), "ALLOWED")
    setter("cemetery row stage", r + (
           "local_owner_zero_cemetery_ledger", "rows", 0, "stage"), 2)
    setter("cemetery row child", r + (
           "local_owner_zero_cemetery_ledger", "rows", 0, "common_child_id"),
           "round121-common-child:mutant")
    setter("cemetery partition false", r + (
           "local_owner_zero_cemetery_ledger", "rows", 0,
           "partition_is_disjoint_half_open_and_exhaustive"), False)
    setter("cemetery cut owned left", r + (
           "local_owner_zero_cemetery_ledger", "rows", 0,
           "internal_cut_is_owned_by_the_right_output_member"), False)
    setter("cemetery endpoint mass nonzero", r + (
           "local_owner_zero_cemetery_ledger", "rows", 0,
           "endpoint_mass_for_every_accepted_density"), "POSITIVE")
    setter("cemetery discarded complement", r + (
           "local_owner_zero_cemetery_ledger", "rows", 0,
           "discarded_relative_domain_complement"), "NONEMPTY")
    setter("cemetery arrival nonzero", r + (
           "local_owner_zero_cemetery_ledger", "rows", 0,
           "restricted_relative_cemetery_arrival_kernel"), "NONZERO")
    setter("cemetery ambient installed", r + (
           "local_owner_zero_cemetery_ledger", "rows", 0,
           "ambient_pre_regularization_cemetery"), "INSTALLED")

    cases.append(("delete family leg row", lambda d:
                  d["result"]["standard_family_leg_operator_rows"].pop()))
    cases.append(("duplicate family leg row", lambda d:
                  d["result"]["standard_family_leg_operator_rows"].append(
                      copy.deepcopy(d["result"][
                          "standard_family_leg_operator_rows"][0]))))
    cases.append(("reorder family rows", lambda d:
                  d["result"]["standard_family_leg_operator_rows"].reverse()))
    lf = r + ("standard_family_leg_operator_rows", 0)
    setter("family row id", lf + ("standard_family_leg_operator_row_id",),
           "round124-standard-family-leg-operator:mutant")
    setter("family stage", lf + ("stage",), 1)
    setter("family common rank", lf + ("common_rank",), 23)
    setter("family owner", lf + ("actual_collision_owner",), "W[-1,-2]")
    setter("family chart", lf + ("actual_collision_chart",), "S")
    setter("family recut", lf + ("input_materialized_recut_instance_id",),
           "round121-recut-instance:mutant")
    setter("family F14 crosslink", lf + ("round123_same_key_F14_slot_ids", 0),
           "round123-gate5-f14-slot:mutant")
    setter("family F7 crosslink", lf + ("round122_same_key_F7_slot_ids", 0),
           "round122-gate5-slot:mutant")
    setter("family input mass nonnegative", lf + ("input_member_contract", "mass"),
           "M_a>=0")
    setter("family input density nonnegative",
           lf + ("input_member_contract", "density"), "rho_a>=0")
    setter("family input normalization",
           lf + ("input_member_contract", "normalization"), "NONE")
    setter("family input lower too high",
           lf + ("input_normalized_adapted_length_strict_lower",), "1/2")
    setter("family input length not proper",
           lf + ("input_adapted_length_less_or_equal_delta",), False)
    setter("family output count", lf + ("output_member_count",), 216)
    setter("family output member", lf + ("output_geometry_member_ids", 0),
           "round123-image-member:mutant")
    setter("family tag constructor", lf + (
           "output_member_tag_templates", 0, "tag_constructor"), "mutant")
    setter("family tag dedup", lf + (
           "output_member_tag_templates", 0,
           "geometry_coincidence_does_not_identify_tags"), False)
    setter("family output lower", lf + (
           "output_normalized_adapted_length_strict_lower",), "1")
    setter("family output length over delta", lf + (
           "all_output_member_lengths_less_or_equal_delta",), False)
    setter("family pushforward drops J", lf + (
           "conditional_pushforward", "rho_aj_plus"), "rho_a/alpha_aj")
    setter("family equal masses", lf + ("conditional_pushforward", "M_aj"),
           "M_a/output_member_count")
    setter("family mass identity", lf + ("mass_partition_identity",), "UNKNOWN")
    setter("family F15 33", lf + (
           "memberwise_strong_norm_cost_strict_upper",), "33")
    setter("family cemetery link", lf + (
           "relative_zero_cemetery_ledger_row_id",), "mutant")
    setter("family tag preservation false", lf + (
           "tag_preserving_and_no_cross_member_deduplication",), False)
    setter("family roof duplicates", lf + (
           "transparent_wall_roof_split_adds_no_family_operator_factor",),
           False)
    setter("family b3 collision angle", lf + (
           "bypass_designated_b3_is_a_collision_angle",), True)

    cases.append(("delete F15 slot", lambda d:
                  d["result"]["gate5_F15_slot_rows"].pop()))
    cases.append(("duplicate F15 slot", lambda d:
                  d["result"]["gate5_F15_slot_rows"].append(
                      copy.deepcopy(d["result"]["gate5_F15_slot_rows"][0]))))
    cases.append(("reorder F15 slots", lambda d:
                  d["result"]["gate5_F15_slot_rows"].reverse()))
    sf = r + ("gate5_F15_slot_rows", 0)
    setter("F15 slot id", sf + ("slot_id",), "round124-gate5-f15-slot:mutant")
    setter("F15 immutable word", sf + ("immutable_slot_key", 0),
           "gate5-word:mutant")
    setter("F15 immutable field", sf + ("immutable_slot_key", 3),
           "dynamic_test_operator_cost")
    setter("F15 official word", sf + ("official_word_key_id",),
           "gate5-word:mutant")
    setter("F15 subbranch", sf + ("refined_homogeneous_subbranch_id",),
           "round121-refined-subbranch:mutant")
    setter("F15 roof", sf + ("roof_level_j",), 9)
    setter("F15 field index", sf + ("field_index",), 14)
    setter("F15 field name", sf + ("field_name",),
           "regular_density_operator_cost")
    setter("F15 bound weak", sf + ("field_bound_semantics",), "NONSTRICT")
    setter("F15 value 33", sf + ("field_value_or_contract",), "33")
    setter("F15 status frontier", sf + ("slot_status",), "FRONTIER")
    setter("F15 stage", sf + ("stage",), 2)
    setter("F15 F14 crosslink", sf + ("round123_same_key_F14_slot_id",),
           "round123-gate5-f14-slot:mutant")
    setter("F15 F7 crosslink", sf + ("round122_same_key_F7_slot_id",),
           "round122-gate5-slot:mutant")
    setter("F15 leg link", sf + ("standard_family_leg_operator_row_id",),
           "round124-standard-family-leg-operator:mutant")
    setter("F15 recut", sf + ("input_materialized_recut_instance_id",),
           "round121-recut-instance:mutant")
    setter("F15 output member", sf + ("output_geometry_member_ids", 0),
           "round123-image-member:mutant")
    setter("F15 cemetery", sf + ("relative_zero_cemetery_ledger_row_id",),
           "mutant")
    setter("F15 projective completion false", sf + (
           "finite_positive_family_then_countable_projective_completion",),
           False)
    setter("F15 signed extension false", sf + (
           "signed_Jordan_standard_family_extension_installed",), False)
    setter("F15 roof duplicate", sf + (
           "transparent_wall_roof_split_adds_no_F15_factor",), False)
    setter("F15 direct path confused", sf + (
           "roof_slot_value_is_one_step_not_direct_path_bound",), False)
    setter("F15 payload becomes slots", sf + (
           "stage3_fragments_are_payload_not_F15_source_slots",), False)
    setter("F15 b3 collision", sf + (
           "bypass_designated_b3_is_a_collision_angle",), True)

    combined = r + ("combined_installed_child_local_slot_registry",)
    setter("combined inherited count", combined + (
           "Round123_inherited_slot_count",), 1680)
    setter("combined F14 digest", combined + (
           "Round123_F14_slot_ids_sha256",), "0" * 64)
    setter("combined F15 digest", combined + (
           "new_F15_slot_ids_sha256",), "0" * 64)
    setter("combined slots 2160", combined + ("combined_slot_count",), 2160)
    setter("combined fields include F17", combined + (
           "certified_field_indices",), list(range(1, 18)))
    setter("combined uninstalled omits F17", combined + (
           "uninstalled_field_indices",), [18])
    setter("combined payload as slots", combined + (
           "stage3_payload_members_are_not_source_slot_keys",), False)

    labels: list[str] = []
    for label, mutate in cases:
        mutant = copy.deepcopy(certificate)
        try:
            mutate(mutant)
            resign(mutant)
            evaluate_document(mutant, r123, r122, expected)
        except Exception:
            labels.append(label)
            continue
        raise VerificationError(f"semantic mutant accepted:{label}")
    require(len(labels) == len(set(labels)), "unique semantic labels")
    return labels


def strict_json_attacks(
    certificate: dict[str, Any],
    r123: dict[str, Any],
    r122: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    full = (
        json.dumps(certificate, sort_keys=True, separators=(",", ":"))
        .encode("utf-8")
    )

    def resigned(path: tuple[Any, ...], value: Any) -> bytes:
        doc = copy.deepcopy(certificate)
        set_path(doc, path, value)
        resign(doc)
        return json.dumps(
            doc, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")

    attacks: list[tuple[str, bytes]] = [
        (
            "duplicate top-level key",
            b'{"schema":"x","schema":"y","result":{},"result_sha256":"z"}',
        ),
        (
            "duplicate deep key",
            (
                b'{"schema":"'
                + CERTIFICATE_SCHEMA.encode()
                + b'","result":{"status":"a","status":"b"},'
                  b'"result_sha256":"z"}'
            ),
        ),
        (
            "NaN constant",
            b'{"schema":"x","result":{"x":NaN},"result_sha256":"z"}',
        ),
        (
            "Infinity constant",
            b'{"schema":"x","result":{"x":Infinity},"result_sha256":"z"}',
        ),
        (
            "negative Infinity constant",
            b'{"schema":"x","result":{"x":-Infinity},"result_sha256":"z"}',
        ),
        (
            "JSON decimal float",
            b'{"schema":"x","result":{"x":1.25},"result_sha256":"z"}',
        ),
        (
            "JSON exponent float",
            b'{"schema":"x","result":{"x":1e9999},"result_sha256":"z"}',
        ),
        ("top-level array", b"[]"),
        ("top-level null", b"null"),
        ("UTF-8 BOM", b"\xef\xbb\xbf" + full),
        ("invalid UTF-8", b"\xff" + full),
        (
            "unpaired surrogate",
            b'{"schema":"\\ud800","result":{},"result_sha256":"z"}',
        ),
        (
            "bool masquerading as integer",
            resigned(
                ("result", "count_ledger",
                 "standard_family_leg_operator_row_count"),
                True,
            ),
        ),
        (
            "noncanonical fraction",
            resigned(
                ("result", "stagewise_raw_Z_and_properness", "vartheta_p"),
                "720269600/720987326",
            ),
        ),
        (
            "zero-denominator fraction",
            resigned(
                ("result", "stagewise_raw_Z_and_properness", "vartheta_p"),
                "1/0",
            ),
        ),
    ]
    labels = []
    for label, raw in attacks:
        try:
            value = parse_strict_bytes(raw)
            require(type(value) is dict, "strict attack top object")
            evaluate_document(value, r123, r122, expected)
        except Exception:
            labels.append(label)
            continue
        raise VerificationError(f"strict JSON attack accepted:{label}")
    require(len(labels) == len(set(labels)) == 15, "strict JSON labels")
    return labels


def verification_document(
    certificate_path: Path,
    certificate: dict[str, Any],
    r123: dict[str, Any],
    r122: dict[str, Any],
) -> dict[str, Any]:
    expected = expected_result(r123, r122)
    counts = evaluate_document(certificate, r123, r122, expected)
    semantic_labels = semantic_mutations(
        certificate, r123, r122, expected
    )
    strict_labels = strict_json_attacks(
        certificate, r123, r122, expected
    )
    cp_delta = CP_STAR * DELTA
    strong_gap = Q(F15) - Q(100, 3) - DELTA * (1 + C_J)
    result = {
        "status": "PASS",
        "verifier_precision_bits": VERIFIER_BITS,
        "independence_contract": {
            "imports_Round124_producer": False,
            "imports_Round124_proof_helper": False,
            "Round124_producer_is_byte_pinned_but_not_executed": True,
            "Round123_and_Round122_are_strict_parsed_as_frozen_data": True,
            "all_72_family_leg_rows_reconstructed": True,
            "all_72_relative_zero_cemetery_rows_reconstructed": True,
            "all_120_full_key_F15_slots_reconstructed": True,
            "all_1920_combined_keys_accounted_for": True,
        },
        "producer_sha256": ROUND124_PRODUCER_SHA256,
        "certificate_sha256": sha256(certificate_path),
        "certificate_result_sha256": certificate["result_sha256"],
        "upstream_byte_pin_count": len(EXPECTED_PINS),
        "reconstructed_counts": counts,
        "exact_arithmetic_audit": {
            "delta": "1/10^90",
            "regularity_recurrence": (
                "Reg_plus<(93/100)*Reg+"
                "15000000000000000000000000"
            ),
            "regularity_cone_K": str(REG_K),
            "regularity_cone_invariant": Q_REG * REG_K + C_J < REG_K,
            "uniform_output_inverse_length_coefficient": "100/3",
            "one_step_F15_strict_upper": "34",
            "F15_strong_norm_exact_gap": qstr(strong_gap),
            "F15_strong_norm_exact_gap_is_positive": strong_gap > 0,
            "adapted_vartheta_p": qstr(VARTTHETA_P),
            "adapted_C_p_star_times_delta": qstr(cp_delta),
            "worst_Cp_delta_margin": qstr(
                cp_delta - SOURCE_COEFFICIENTS[0]
            ),
            "recovery_clock": 0,
        },
        "typed_scope_audit": {
            "finite_positive_family_Tonelli_lift": "PASS",
            "countable_projective_completion": "PASS",
            "signed_Jordan_extension_without_factor_two": "PASS",
            "tag_preserving_no_geometry_deduplication": "PASS",
            "relative_half_open_zero_cemetery": "PASS",
            "local_Z_star_distinct_from_Round61_Z_col": "PASS",
            "no_global_Orlicz_or_all_time_cemetery_promotion": "PASS",
            "roof_split_does_not_duplicate_physical_operator": "PASS",
        },
        "semantic_mutation_test_count": len(semantic_labels),
        "semantic_mutation_rejection_labels": semantic_labels,
        "strict_json_attack_count": len(strict_labels),
        "strict_json_attack_rejection_labels": strict_labels,
        "determinism_contract": {
            "canonical_JSON": (
                "sort_keys=True, indent=2, allow_nan=False, final newline"
            ),
            "stable_sort_order": (
                "common_rank, stage for family/cemetery rows;"
                " child, stage, roof for F15 slots"
            ),
            "PYTHONHASHSEED_independent": True,
        },
        "safety_state": {
            "rank3_seed_child_field_maturity": "16/18",
            "remaining_uninstalled_child_fields": ["F17", "F18"],
            "gate5_global_maturity": "10/18",
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "cm2_verdict": "NO-GO_FOR_CLAIM",
        },
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate", type=Path, default=DEFAULT_CERTIFICATE
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    r123, r122 = load_upstream()
    certificate = strict_document(args.certificate, CERTIFICATE_SCHEMA)
    document = verification_document(
        args.certificate, certificate, r123, r122
    )
    text = json.dumps(
        document, sort_keys=True, indent=2, allow_nan=False
    ) + "\n"
    args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
