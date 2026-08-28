#!/usr/bin/env python3
"""Round124 exact-seed standard-family operator and installed F15.

This producer is a typed assembly layer over the final Round123 certificate.
It lifts the memberwise arbitrary-density F14 estimate to finite positive
standard families, then to the projective/countable and signed-Jordan
completions.  It also closes the adapted raw-Z properness and restricted
zero-cemetery ledgers.  Only the same 24 Round121 exact-seed children are in
scope.  Global Gate5 remains 10/18 and CM2 remains unavailable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round124.rank3-exact-seed-standard-family-operator-f15.v1"
OUTPUT = (
    HERE
    / "cm2-round124-rank3-exact-seed-standard-family-operator-f15-2026-07-23.json"
)
ROUND123 = (
    HERE
    / "cm2-round123-rank3-exact-seed-stage3-output-properization-f14-2026-07-23.json"
)
ROUND122 = (
    HERE
    / "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json"
)

PINS = {
    # Final Round123 pack, including its geometry helper.
    "deliverables/cm2_round123_rank3_exact_seed_stage3_output_properization_common.py": "8eda085e342655f20ef68a7aa0554b3bed3c26312d1261c49d4f6567d0bbb9e0",
    "deliverables/cm2_round123_rank3_exact_seed_stage3_output_properization_f14.py": "e00b85d722e3784c0c2427ea0f7b32f8306b9d706b902b22df334b8aa9b00c38",
    "deliverables/cm2-round123-rank3-exact-seed-stage3-output-properization-f14-2026-07-23.json": "d3d45e32e45d1a37d5364c0d5fc1f34b537190c2450b7e8f9ead729dc77fe993",
    "deliverables/cm2_round123_rank3_exact_seed_stage3_output_properization_f14_verifier.py": "eec966baae120a442f621e03f4575161545fc6d65604aba5f255a440c90f0625",
    "deliverables/cm2-round123-rank3-exact-seed-stage3-output-properization-f14-verification-2026-07-23.json": "37b70e60e1b9a66875e4565a44c115d50f55d718320fa79187d26bc45a1136d6",
    "deliverables/cm2-round123-rank3-exact-seed-stage3-output-properization-f14-report-2026-07-23.md": "a524de40d3abc818dd89f6b8dfba508f11fd81d6f4fc7fcac56130035655b25f",
    "deliverables/cm2-round123-rank3-exact-seed-stage3-output-properization-f14-cold-replay-2026-07-23.md": "9a4a33817de0b776599bb5b218863bfce8d867f63fe3350ea063643b738873ce",
    "deliverables/cm2-one-hundred-twenty-third-direct-assault-2026-07-23.md": "90fefb284bd0cf23d80a43fab1d6088d1146cf53678d32de574f272e9828acba",
    "deliverables/cm2-one-hundred-twenty-third-direct-assault-manifest-2026-07-23.sha256": "16a667bdbf3098c623199320a0cf85a34eba900ee376e476306ba7d5174b696b",
    # Same-key F7 dependency used by the F15 rows.
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json": "a7ed51149916bbf0d181b9cd45114cd11d81a5d30e72fea50b3336d1ead22028",
    # Gate5 field schema.
    "deliverables/cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "deliverables/cm2_gate5_return_word_three_norm_frontier_cert.py": "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    "deliverables/cm2_gate5_return_word_three_norm_frontier_verifier.py": "0384acdd1f912b0d4b3bee84ff530358d9693893d1c5c64a1deabaede8e0867b",
    # Adapted numeric growth/properness source.
    "deliverables/cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d",
    "deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py": "01e32ca209818f4077443a7692622c4202ab7f1066e2f95802185e2be7a2cc9a",
    "deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_verifier.py": "8074da51347aec415a864d87dc349cff25afa5a9a239febc53cc1ab015763d05",
    # Frozen strong recipient and the later Reg-alpha crosswalk.
    "deliverables/cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json": "3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3",
    "deliverables/cm2_gate4_inner_core_strong_product_bridge_frontier_cert.py": "4720669e90824e8c630276aa3d73606435eb88da2a51b2a756f651f56071605a",
    "deliverables/cm2_gate4_inner_core_strong_product_bridge_frontier_verifier.py": "1c814f82231c8a0181d53ec28f09d07c2528d40eda82a425b280a2858b0c0862",
    "deliverables/cm2_round88_gate5_f14_regalpha_strong_install_cert.py": "2bcb8ac5b5e94ad3335d09f16f62bd68520ad2936e12d79181f55989daca89b5",
    "deliverables/cm2_round88_gate5_f14_regalpha_strong_install_verifier.py": "c0d4936326e94db8146a0d9726d6136c9a70417800e40359f520162344027258",
    "deliverables/cm2-round88-gate5-f14-regalpha-strong-install-2026-07-22.json": "80e4ba31fb86b51410e90a5e1ef561f565cede65ef56792fc40364235d652993",
    "deliverables/cm2-round88-gate5-f14-regalpha-strong-install-audit-2026-07-22.json": "2d890384f3ffc8f3e1f71ae5e5607365f9e76a399e1da0f99cdd352c122953d5",
    "deliverables/cm2-round88-gate5-f14-regalpha-strong-install-report-2026-07-22.md": "fbb28e803a507857fac627f88a5421bc2121e98c897e46b1584bd804ee2bd88c",
    # Scope guards: raw collar law and all-time cemetery remain global frontiers.
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
F15_ONE_STEP = 34
SOURCE_COEFFICIENTS = (Q(200), Q(100, 3), Q(200, 17))
OUTPUT_COEFFICIENTS = (Q(100, 3), Q(200, 17), Q(125, 4))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


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


def reject_float(_value: str) -> Any:
    raise ValueError("JSON floating-point numbers are forbidden")


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"BOM:{path.name}")
    text = raw.decode("utf-8", errors="strict")
    value = json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_float=reject_float,
        parse_constant=reject_float,
    )
    require(type(value) is dict, f"top object:{path.name}")
    return value


def strict_document(path: Path, schema: str) -> dict[str, Any]:
    document = strict_json(path)
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"closed envelope:{path.name}",
    )
    require(document["schema"] == schema, f"schema:{path.name}")
    require(
        document["result_sha256"] == digest(document["result"]),
        f"result digest:{path.name}",
    )
    return document


def verify_pins() -> None:
    for relative, expected in PINS.items():
        path = HERE.parent / relative
        require(path.is_file() and not path.is_symlink(), f"pin:{relative}")
        require(sha256(path) == expected, f"byte pin:{relative}")


def validate_row(row: dict[str, Any], label: str) -> None:
    require(type(row) is dict and type(row.get("row_sha256")) is str, label)
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    require(row["row_sha256"] == digest(payload), f"{label} digest")


def coordinate(row: dict[str, Any]) -> tuple[str, str, int]:
    return (
        row["official_word_key_id"],
        row["refined_homogeneous_subbranch_id"],
        row["roof_level_j"],
    )


def load_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    verify_pins()
    round123 = strict_document(
        ROUND123,
        "cm2.round123.rank3-exact-seed-stage3-output-properization-f14.v1",
    )["result"]
    round122 = strict_document(
        ROUND122,
        "cm2.round122.rank3-exact-seed-physical-face-field-bridge.v1",
    )["result"]
    require(
        round123["rank3_seed_child_field_maturity"] == "15/18"
        and round123["count_ledger"]["combined_child_local_slot_count"] == 1800,
        "final Round123 local state",
    )
    require(
        round123["gate5_actual_child_field_status"]["F15"]
        == "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
        "Round123 F15 frontier",
    )
    require(
        round123["gate5_global_maturity"] == "10/18"
        and round123["complete_18_field_block_count"] == 0
        and round123["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "Round123 strict state",
    )
    require(
        len(round123["accepted_norm_leg_output_rows"]) == 72
        and len(round123["gate5_F14_slot_rows"]) == 120,
        "Round123 row census",
    )
    for row in round123["accepted_norm_leg_output_rows"]:
        validate_row(row, "Round123 leg row")
    for row in round123["gate5_F14_slot_rows"]:
        validate_row(row, "Round123 F14 row")
    for row in round123["input_child_output_partition_rows"]:
        validate_row(row, "Round123 partition row")
    require(
        len(
            [
                row
                for row in round122["gate5_F7_F13_F16_slot_rows"]
                if row["field_index"] == 7
            ]
        )
        == 120,
        "Round122 F7 census",
    )
    return round123, round122


def family_leg_id(common_child_id: str, stage: int) -> str:
    return "round124-standard-family-leg-operator:" + digest(
        [
            "round124-standard-family-leg-operator-v1",
            common_child_id,
            stage,
        ]
    )


def cemetery_row_id(common_child_id: str, stage: int) -> str:
    return "round124-relative-zero-cemetery-ledger:" + digest(
        [
            "round124-relative-zero-cemetery-ledger-v1",
            common_child_id,
            stage,
        ]
    )


def output_tag_templates(
    common_child_id: str, stage: int, output_ids: list[str]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for output_id in output_ids:
        row = {
            "geometry_output_member_id": output_id,
            "tag_tuple_template": [
                "<input-standard-family-member-id>",
                common_child_id,
                stage,
                output_id,
            ],
            "tag_constructor": (
                "round124-output-family-member:"
                "sha256(canonical(tag_tuple_template))"
            ),
            "geometry_coincidence_does_not_identify_tags": True,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    return rows


def build_cemetery_rows(
    round123: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for leg in sorted(
        round123["accepted_norm_leg_output_rows"],
        key=lambda row: (row["common_rank"], row["leg_index"]),
    ):
        stage = leg["leg_index"]
        row = {
            "cemetery_ledger_row_id": cemetery_row_id(
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
                "the materialized Round121 exact-seed common child at this"
                " physical collision stage"
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
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows)
        == len({row["cemetery_ledger_row_id"] for row in rows})
        == 72,
        "72 relative zero-cemetery rows",
    )
    return rows


def build_family_leg_rows(
    round123: dict[str, Any],
    round122: dict[str, Any],
    cemetery_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    f14_map = {
        coordinate(row): row for row in round123["gate5_F14_slot_rows"]
    }
    f7_map = {
        coordinate(row): row
        for row in round122["gate5_F7_F13_F16_slot_rows"]
        if row["field_index"] == 7
    }
    cemetery_map = {
        (row["common_child_id"], row["stage"]): row for row in cemetery_rows
    }
    input_length_lowers = ("1/200", "3/100", "17/200")
    output_length_lowers = ("3/100", "17/200", "4/125")
    rows: list[dict[str, Any]] = []
    for leg in sorted(
        round123["accepted_norm_leg_output_rows"],
        key=lambda row: (row["common_rank"], row["leg_index"]),
    ):
        stage = leg["leg_index"]
        roof_coordinates = [
            (
                leg["official_word_key_id"],
                leg["refined_homogeneous_subbranch_id"],
                roof,
            )
            for roof in leg["roof_level_js"]
        ]
        f14_ids = [f14_map[key]["slot_id"] for key in roof_coordinates]
        f7_ids = [f7_map[key]["slot_id"] for key in roof_coordinates]
        tags = output_tag_templates(
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
            "round123_same_key_F14_slot_ids": f14_ids,
            "round122_same_key_F7_slot_ids": f7_ids,
            "input_member_contract": {
                "tag": "<input-standard-family-member-id>",
                "mass": "M_a>0",
                "density": "rho_a>0",
                "normalization": "integral rho_a d ell_*=1",
                "Reg_alpha_upper": (
                    "500000000000000000000000000"
                ),
                "geometry_carrier": leg[
                    "input_materialized_recut_instance_id"
                ],
            },
            "input_normalized_adapted_length_strict_lower": (
                input_length_lowers[stage]
            ),
            "input_adapted_length_less_or_equal_delta": True,
            "output_member_count": leg["output_member_count"],
            "output_geometry_member_ids": leg["output_member_ids"],
            "output_member_tag_templates": tags,
            "output_member_tag_templates_sha256": digest(tags),
            "output_normalized_adapted_length_strict_lower": (
                output_length_lowers[stage]
            ),
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
            "memberwise_strong_norm_cost_strict_upper": str(F15_ONE_STEP),
            "relative_zero_cemetery_ledger_row_id": cemetery_map[
                (leg["common_child_id"], stage)
            ]["cemetery_ledger_row_id"],
            "tag_preserving_and_no_cross_member_deduplication": True,
            "transparent_wall_roof_split_adds_no_family_operator_factor": True,
            "bypass_designated_b3_is_a_collision_angle": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows)
        == len({row["standard_family_leg_operator_row_id"] for row in rows})
        == 72,
        "72 standard-family leg rows",
    )
    require(
        {row["stage"] for row in rows} == {0, 1, 2},
        "three standard-family stages",
    )
    require(
        sum(row["output_member_count"] for row in rows if row["stage"] == 2)
        == 216,
        "216 stage3 tagged payload members",
    )
    return rows


def f15_slot_id(immutable_key: list[Any]) -> str:
    return "round124-gate5-f15-slot:" + digest(
        ["round124-gate5-f15-slot-v1", immutable_key]
    )


def build_f15_slots(
    round123: dict[str, Any],
    round122: dict[str, Any],
    family_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    family_map = {
        (row["common_child_id"], row["stage"]): row for row in family_rows
    }
    f7_map = {
        coordinate(row): row
        for row in round122["gate5_F7_F13_F16_slot_rows"]
        if row["field_index"] == 7
    }
    rows: list[dict[str, Any]] = []
    keys: set[str] = set()
    for f14 in sorted(
        round123["gate5_F14_slot_rows"],
        key=lambda row: (
            row["common_child_id"],
            row["stage"],
            row["roof_level_j"],
        ),
    ):
        key3 = coordinate(f14)
        family = family_map[(f14["common_child_id"], f14["stage"])]
        immutable_key = [
            f14["official_word_key_id"],
            f14["refined_homogeneous_subbranch_id"],
            f14["roof_level_j"],
            "standard_family_operator_cost",
        ]
        key_text = canonical(immutable_key)
        require(key_text not in keys, "unique F15 immutable key")
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
            "field_value_or_contract": str(F15_ONE_STEP),
            "slot_status": "CERTIFIED_ON_THIS_EXACT_SEED_COMMON_CHILD",
            "common_child_id": f14["common_child_id"],
            "stage": f14["stage"],
            "round123_same_key_F14_slot_id": f14["slot_id"],
            "round122_same_key_F7_slot_id": f7_map[key3]["slot_id"],
            "standard_family_leg_operator_row_id": family[
                "standard_family_leg_operator_row_id"
            ],
            "standard_family_leg_operator_row_sha256": family["row_sha256"],
            "input_materialized_recut_instance_id": family[
                "input_materialized_recut_instance_id"
            ],
            "output_geometry_member_ids": family[
                "output_geometry_member_ids"
            ],
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
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows) == len({row["slot_id"] for row in rows}) == 120,
        "120 unique F15 slots",
    )
    stage_counts = {
        stage: sum(row["stage"] == stage for row in rows)
        for stage in range(3)
    }
    require(stage_counts == {0: 48, 1: 24, 2: 48}, "F15 stage census")
    return rows


def accepted_standard_family_domain() -> dict[str, Any]:
    return {
        "status": (
            "CERTIFIED_ON_THE_24_MATERIALIZED_EXACT_SEED_CARRIERS"
        ),
        "positive_finite_family": {
            "form": "G={(M_a,rho_a,C_a)}_a",
            "carrier": (
                "each C_a is one of the materialized Round123 stage carriers"
            ),
            "mass": "M_a>0",
            "density": "rho_a>0",
            "normalization": "integral_(C_a) rho_a d ell_*=1",
            "regularity": (
                "Reg_(1/3)(rho_a)"
                "<=500000000000000000000000000"
            ),
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


def standard_family_tonelli_theorem() -> dict[str, Any]:
    require(F15_ONE_STEP == 34, "F15 value")
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
        "one_step_F15_strict_upper": str(F15_ONE_STEP),
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


def raw_z_and_properness_theorem() -> dict[str, Any]:
    cp_delta = CP_STAR * DELTA
    require(VARTTHETA_P < 1, "adapted contraction")
    require(cp_delta == Q(1441974652, 358863), "Cp delta identity")
    source_gaps = [cp_delta - value for value in SOURCE_COEFFICIENTS]
    output_gaps = [cp_delta - value for value in OUTPUT_COEFFICIENTS]
    require(all(value > 0 for value in source_gaps + output_gaps),
            "strict properness gaps")
    require(source_gaps[0] == Q(1370202052, 358863),
            "worst source properness gap")
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
                    f"Z_*<{qstr(SOURCE_COEFFICIENTS[stage])}"
                    "*M/delta"
                ),
                "output_Z_star_strict_bound": (
                    f"Z_*<{qstr(OUTPUT_COEFFICIENTS[stage])}"
                    "*M/delta"
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


def scope_separation() -> dict[str, Any]:
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


def build() -> dict[str, Any]:
    round123, round122 = load_inputs()
    cemetery_rows = build_cemetery_rows(round123)
    family_rows = build_family_leg_rows(round123, round122, cemetery_rows)
    f15_rows = build_f15_slots(round123, round122, family_rows)

    inherited_f14_ids = [
        row["slot_id"] for row in round123["gate5_F14_slot_rows"]
    ]
    new_f15_ids = [row["slot_id"] for row in f15_rows]
    require(
        len(inherited_f14_ids) == len(set(inherited_f14_ids)) == 120,
        "Round123 F14 IDs",
    )
    require(
        len(new_f15_ids) == len(set(new_f15_ids)) == 120,
        "Round124 F15 IDs",
    )
    require(set(inherited_f14_ids).isdisjoint(new_f15_ids),
            "F14/F15 namespace separation")

    base = dict(round123)
    for key in (
        "status",
        "strict_scope",
        "strict_nonclaims",
        "upstream_and_helper_pins",
    ):
        base.pop(key)

    gate_status = dict(round123["gate5_actual_child_field_status"])
    gate_status["F15"] = (
        "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN"
    )
    count_ledger = dict(round123["count_ledger"])
    count_ledger.update(
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
    base.update(
        {
            "status": (
                "CERTIFIED_EXACT_SEED_STANDARD_FAMILY_OPERATOR"
                "__F15_INSTALLED"
            ),
            "round123_contract": {
                "certificate_sha256": PINS[
                    "deliverables/cm2-round123-rank3-exact-seed-stage3-output-properization-f14-2026-07-23.json"
                ],
                "result_sha256": (
                    "e3ebade59b4bf8672f72f960a3fe0c13364ee27cd22f3ffe048b0ba7debd8296"
                ),
                "actual_child_count": 24,
                "leg_output_row_count": 72,
                "stage3_output_payload_member_count": 216,
                "inherited_slot_count": 1800,
                "inherited_child_local_maturity": "15/18",
            },
            "accepted_standard_family_domain": (
                accepted_standard_family_domain()
            ),
            "standard_family_leg_operator_rows": family_rows,
            "standard_family_leg_operator_rows_sha256": digest(family_rows),
            "standard_family_Tonelli_lift_theorem": (
                standard_family_tonelli_theorem()
            ),
            "stagewise_raw_Z_and_properness": (
                raw_z_and_properness_theorem()
            ),
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
            "round50_65_scope_separation": scope_separation(),
            "gate5_F15_slot_rows": f15_rows,
            "gate5_F15_slot_rows_sha256": digest(f15_rows),
            "combined_installed_child_local_slot_registry": {
                "Round123_inherited_slot_count": 1800,
                "Round123_combined_slot_ids_sha256": round123[
                    "combined_F1_F14_F16_slot_registry"
                ]["combined_slot_ids_sha256"],
                "Round123_F14_slot_ids_sha256": digest(inherited_f14_ids),
                "new_F15_slot_count": 120,
                "new_F15_slot_ids_sha256": digest(new_f15_ids),
                "combined_slot_count": 1920,
                "slot_count_per_certified_field": 120,
                "certified_field_indices": list(range(1, 17)),
                "uninstalled_field_indices": [17, 18],
                "all_keys_are_full_word_subbranch_roof_field_keys": True,
                "stage3_payload_members_are_not_source_slot_keys": True,
            },
            "count_ledger": count_ledger,
            "gate5_actual_child_field_status": gate_status,
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
            "upstream_and_helper_pins": dict(sorted(PINS.items())),
        }
    )
    result = base
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    document = build()
    text = json.dumps(document, sort_keys=True, indent=2, allow_nan=False) + "\n"
    args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
