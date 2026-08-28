#!/usr/bin/env python3
"""Round123 exact-seed stage-3 properization and installed F14.

This producer starts from the frozen Round121 exact seed and the final
Round122 physical-face/field bridge.  It materializes the actual-third
north-chart output recut, proves stagewise output-length lower bounds for all
24 x 3 physical leg inputs, and installs 120 immutable one-step F14 slots with
value 34.  The 216 output fragments are payload members, not new source slot
keys.  Global Gate5 remains 10/18 and CM2 remains unavailable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_round123_rank3_exact_seed_stage3_output_properization_common as common


HERE = Path(__file__).resolve().parent
SCHEMA = (
    "cm2.round123.rank3-exact-seed-stage3-output-properization-f14.v1"
)
OUTPUT = (
    HERE
    / "cm2-round123-rank3-exact-seed-stage3-output-properization-f14-2026-07-23.json"
)
PRECISION_BITS = 1536
ROOT_BISECTIONS = 240

ROUND121 = (
    HERE
    / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
)
ROUND122 = (
    HERE
    / "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json"
)

COMMON_SHA256 = (
    "8eda085e342655f20ef68a7aa0554b3bed3c26312d1261c49d4f6567d0bbb9e0"
)

PINS = {
    "deliverables/cm2_round123_rank3_exact_seed_stage3_output_properization_common.py": COMMON_SHA256,
    "deliverables/cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py": "30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed",
    "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json": "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e",
    "deliverables/cm2_round121_rank3_exact_seed_three_leg_recut_f5f6_verifier.py": "d35c0e04b9d339c1271533abdefa5addcb73096b70abdec94d60e475daa45e95",
    "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json": "ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80",
    "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-report-2026-07-23.md": "8db9291b0eb679b6137d18ccc1e5254a79efbb7e0e2a085042aada1f93754f8d",
    "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-cold-replay-2026-07-23.md": "e670b24f4939d39df4cc84591aad4213bbc80e3ffb3cbe1899d81ef83fe9b11b",
    "deliverables/cm2-one-hundred-twenty-first-direct-assault-2026-07-23.md": "4f14877dfb39362d2b3607922ec2eb65628271aaf9a1392b31abfec0bd369cc0",
    "deliverables/cm2-one-hundred-twenty-first-direct-assault-manifest-2026-07-23.sha256": "e53ad73d4e7120c2ce4f30c49f83f29d4d2b99a5f8a451f9085e5fb473959b83",
    "deliverables/cm2_round122_rank3_exact_seed_physical_face_field_bridge.py": "44a64789635b8adfb597376d25afcbf8cb39dbaf0c2a19c4031bcbe78b3848f4",
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json": "a7ed51149916bbf0d181b9cd45114cd11d81a5d30e72fea50b3336d1ead22028",
    "deliverables/cm2_round122_rank3_exact_seed_physical_face_field_bridge_verifier.py": "bcf6e34398dcd2fd4cb6bb23aec649db5df75d26a80f307e58521d8ef439d31e",
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-verification-2026-07-23.json": "aa0eca5e14fccbeeaad74d075cce0f10ee01f4caf8fccd0e9130ccc0e5cba82b",
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-report-2026-07-23.md": "137d2be2729ccdd5b01ed379fd611575e871e94d8d2af32fbf1a6fe62feac00f",
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-cold-replay-2026-07-23.md": "ccdc04d1463ba9ce6c391085eb7b9e75d316403ef71ec28f056cdc82d062e16c",
    "deliverables/cm2-one-hundred-twenty-second-direct-assault-2026-07-23.md": "97a9911706aaad0ca18a67d1840f63c81c177c3f4c35cc62ec3f3c4a0847cfef",
    "deliverables/cm2-one-hundred-twenty-second-direct-assault-manifest-2026-07-23.sha256": "b78e37b17c1c3f5dd677aa669a2d4bdf71504b1a98bf988cae0144e6d81457bb",
    "deliverables/cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "deliverables/cm2_gate5_return_word_three_norm_frontier_cert.py": "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    "deliverables/cm2_gate5_return_word_three_norm_frontier_verifier.py": "0384acdd1f912b0d4b3bee84ff530358d9693893d1c5c64a1deabaede8e0867b",
    "deliverables/cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d",
    "deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py": "01e32ca209818f4077443a7692622c4202ab7f1066e2f95802185e2be7a2cc9a",
    "deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_verifier.py": "8074da51347aec415a864d87dc349cff25afa5a9a239febc53cc1ab015763d05",
    "deliverables/cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json": "3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3",
    "deliverables/cm2_gate4_inner_core_strong_product_bridge_frontier_cert.py": "4720669e90824e8c630276aa3d73606435eb88da2a51b2a756f651f56071605a",
    "deliverables/cm2_gate4_inner_core_strong_product_bridge_frontier_verifier.py": "1c814f82231c8a0181d53ec28f09d07c2528d40eda82a425b280a2858b0c0862",
    "deliverables/cm2-round88-gate5-f14-regalpha-strong-install-2026-07-22.json": "80e4ba31fb86b51410e90a5e1ef561f565cede65ef56792fc40364235d652993",
}

Q_REG = Q(93, 100)
C_J = 15000000000000000000000000
DELTA = Q(1, 10**90)
F14_ONE_STEP = 34
F14_COMPOSITIONAL_THREE_LEG = 39304
DIRECT_THREE_LEG_B = 41923500000000000000000000


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(Q(value))


def verify_pins() -> None:
    for relative, expected in PINS.items():
        path = HERE.parent / relative
        require(path.is_file() and not path.is_symlink(), f"pin target:{relative}")
        require(sha256(path) == expected, f"byte pin:{relative}")


def strict_document(path: Path, schema: str) -> dict[str, Any]:
    document = common.r121.strict_json(path)
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"closed envelope:{path.name}",
    )
    require(document["schema"] == schema, f"schema:{path.name}")
    require(
        document["result_sha256"]
        == common.r121.closed_digest(document["result"]),
        f"result digest:{path.name}",
    )
    return document


def load_final_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    verify_pins()
    round121 = strict_document(
        ROUND121,
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
    )["result"]
    round122_document = strict_document(
        ROUND122,
        "cm2.round122.rank3-exact-seed-physical-face-field-bridge.v1",
    )
    round122 = round122_document["result"]
    require(
        round122["rank3_seed_child_field_maturity"] == "14/18"
        and round122["count_ledger"]["combined_slot_count"] == 1680,
        "final Round122 maturity",
    )
    require(
        round122["gate5_actual_child_field_status"]["F14"]
        == "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
        "Round122 F14 frontier",
    )
    require(
        round122["gate5_global_maturity"] == "10/18"
        and round122["complete_18_field_block_count"] == 0
        and round122["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "Round122 strict status",
    )
    return round121, round122


def slot_coordinate(row: dict[str, Any]) -> tuple[str, str, int, int]:
    return (
        row["official_word_key_id"],
        row["refined_homogeneous_subbranch_id"],
        row["roof_level_j"],
        row["field_index"],
    )


def enrich_leg_rows(
    base_rows: list[dict[str, Any]],
    round121: dict[str, Any],
    round122: dict[str, Any],
) -> list[dict[str, Any]]:
    children = {
        row["common_child_id"]: row
        for row in round121["common_refinement_rows"]
    }
    f1_by_child_stage: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for row in round121["gate5_F1_F6_slot_rows"]:
        if row["field_index"] == 1:
            f1_by_child_stage.setdefault(
                (row["common_child_id"], row["stage"]), []
            ).append(row)
    r122_slots = {
        slot_coordinate(row): row
        for row in round122["gate5_F7_F13_F16_slot_rows"]
    }
    targets = ("W[-1,-1]", "G[0,0]", "G[-1,-2]")
    charts = ("N", "S", "N")
    coordinates = ("U1", "U2", "U3")
    orientations = (
        "U1(x)=a1(0)-a1(x), strictly increasing",
        "U2(x)=a2(x)-a2(0), strictly increasing",
        "U3(x)=a3(0)-a3(x), strictly increasing",
    )
    derivative_lowers = ("6", "17", "192")
    separation_lowers = ("1/200", "1/200", "1/6000")

    rows: list[dict[str, Any]] = []
    for base in base_rows:
        require(
            base["row_sha256"]
            == digest({key: value for key, value in base.items()
                       if key != "row_sha256"}),
            "base leg-output row digest",
        )
        child = children[base["common_child_id"]]
        leg = base["leg_index"]
        coordinates_for_leg = sorted(
            f1_by_child_stage[(base["common_child_id"], leg)],
            key=lambda row: row["roof_level_j"],
        )
        require(
            len(coordinates_for_leg) in {1, 2}
            and len(
                {row["official_word_key_id"] for row in coordinates_for_leg}
            )
            == 1,
            "leg full-key coordinates",
        )
        word = coordinates_for_leg[0]["official_word_key_id"]
        subbranch = child["refined_homogeneous_subbranch_id"]
        roofs = [row["roof_level_j"] for row in coordinates_for_leg]
        same_key_ids: dict[str, list[str]] = {}
        for field_index in (10, 13, 16):
            same_key_ids[f"F{field_index}"] = [
                r122_slots[(word, subbranch, roof, field_index)]["slot_id"]
                for roof in roofs
            ]
        row = {
            key: value for key, value in base.items() if key != "row_sha256"
        }
        row.update(
            {
                "refined_homogeneous_subbranch_id": subbranch,
                "official_word_key_id": word,
                "roof_level_js": roofs,
                "roof_level_count": len(roofs),
                "actual_collision_target": targets[leg],
                "actual_collision_owner": targets[leg],
                "actual_collision_chart": charts[leg],
                "adapted_output_coordinate": coordinates[leg],
                "adapted_output_coordinate_orientation": orientations[leg],
                "normalized_output_coordinate_derivative_strict_lower": (
                    derivative_lowers[leg]
                ),
                "source_x_or_fragment_separation_strict_lower": (
                    separation_lowers[leg]
                ),
                "every_output_member_length_less_or_equal_delta": True,
                "round122_same_key_slot_ids": same_key_ids,
                "bypass_designated_b3_is_a_collision_angle": False,
            }
        )
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(len(rows) == 72, "72 final leg-output rows")
    require(
        {row["leg_index"] for row in rows} == {0, 1, 2},
        "three physical legs",
    )
    return rows


def f14_slot_id(immutable_key: list[Any]) -> str:
    return "round123-gate5-f14-slot:" + digest(
        ["round123-gate5-f14-slot-v1", immutable_key]
    )


def build_f14_slots(
    round121: dict[str, Any],
    leg_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    leg_map = {
        (row["common_child_id"], row["leg_index"]): row for row in leg_rows
    }
    coordinates = [
        row
        for row in round121["gate5_F1_F6_slot_rows"]
        if row["field_index"] == 1
    ]
    require(len(coordinates) == 120, "120 F14 coordinates")
    rows: list[dict[str, Any]] = []
    immutable_keys: set[str] = set()
    for coordinate in coordinates:
        leg = coordinate["stage"]
        leg_row = leg_map[(coordinate["common_child_id"], leg)]
        roof = coordinate["roof_level_j"]
        word = coordinate["official_word_key_id"]
        subbranch = coordinate["refined_homogeneous_subbranch_id"]
        immutable_key = [
            word,
            subbranch,
            roof,
            "regular_density_operator_cost",
        ]
        key_text = canonical(immutable_key)
        require(key_text not in immutable_keys, "unique F14 immutable key")
        immutable_keys.add(key_text)
        roof_position = leg_row["roof_level_js"].index(roof)
        row = {
            "slot_id": f14_slot_id(immutable_key),
            "immutable_slot_key": immutable_key,
            "official_word_key_id": word,
            "refined_homogeneous_subbranch_id": subbranch,
            "roof_level_j": roof,
            "field_index": 14,
            "field_name": "regular_density_operator_cost",
            "field_bound_semantics": "STRICT_UPPER",
            "field_value_or_contract": str(F14_ONE_STEP),
            "slot_status": "CERTIFIED_ON_THIS_EXACT_SEED_COMMON_CHILD",
            "common_child_id": coordinate["common_child_id"],
            "stage": leg,
            "physical_leg_factor_index": leg,
            "accepted_norm_leg_output_row_id": leg_row[
                "leg_output_row_id"
            ],
            "accepted_norm_leg_output_row_sha256": leg_row["row_sha256"],
            "input_materialized_recut_instance_id": leg_row[
                "input_materialized_recut_instance_id"
            ],
            "output_member_count": leg_row["output_member_count"],
            "output_member_ids": leg_row["output_member_ids"],
            "round122_same_key_F10_slot_id": leg_row[
                "round122_same_key_slot_ids"
            ]["F10"][roof_position],
            "round122_same_key_F13_slot_id": leg_row[
                "round122_same_key_slot_ids"
            ]["F13"][roof_position],
            "round122_same_key_F16_slot_id": leg_row[
                "round122_same_key_slot_ids"
            ]["F16"][roof_position],
            "arbitrary_positive_normalized_density_scope": True,
            "Round122_F10_zero_is_dependency_only_not_payment_for_F14": True,
            "signed_Jordan_extension_installed": True,
            "transparent_wall_roof_split_adds_no_F14_factor": True,
            "roof_slot_value_is_one_step_not_path_product": True,
            "bypass_designated_b3_is_a_collision_angle": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows) == len({row["slot_id"] for row in rows}) == 120,
        "120 unique F14 slots",
    )
    return rows


def operator_theorem() -> dict[str, Any]:
    one_step_margin = (
        Q(F14_ONE_STEP)
        - Q(100, 3)
        - (1 + C_J) * DELTA
    )
    direct_margin = (
        Q(F14_ONE_STEP)
        - Q(100, 3)
        - (1 + DIRECT_THREE_LEG_B) * DELTA
    )
    require(one_step_margin > 0 and direct_margin > 0, "F14 exact margins")
    require(F14_ONE_STEP**3 == F14_COMPOSITIONAL_THREE_LEG,
            "F14 path product")
    require(
        C_J * (1 + Q_REG + Q_REG**2) == DIRECT_THREE_LEG_B,
        "direct three-leg distortion",
    )
    return {
        "status": "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN",
        "accepted_strong_norm": "N(W,M,rho)=M*(1+Reg_alpha(rho)+1/L)",
        "closed_positive_input_domain": {
            "alpha": "1/3",
            "mass": "M>0",
            "density": "rho>0",
            "normalization": "integral rho d ell_*=1",
            "regularity": (
                "Reg_alpha(rho)<=500000000000000000000000000"
            ),
        },
        "conditional_pushforward_contract": {
            "fragment_probability": (
                "alpha_j=integral_(C_j) rho d ell_*"
            ),
            "fragment_mass": "M_j=M*alpha_j",
            "adapted_Jacobian": (
                "J_*(x)=d ell_*^+(T x)/d ell_*(x)"
            ),
            "conditional_density": (
                "rho_j^+(T x)=rho(x)/(alpha_j*J_*(x))"
            ),
            "conditional_normalization": (
                "integral rho_j^+ d ell_*^+=1"
            ),
            "zero_probability_fragments": "OMITTED",
        },
        "one_step_regularity_recurrence": (
            "Reg_alpha_out < (93/100)*Reg_alpha_in + C_J"
        ),
        "C_J": str(C_J),
        "restriction_and_conditional_normalization": (
            "adds only a constant to log(rho) and does not increase Reg_alpha"
        ),
        "zero_mass_output_members": "OMITTED",
        "mass_contract": {
            "member_mass": "M_j>=0 is the pushforward mass on member j",
            "conservation": "sum_j M_j=M",
            "equal_mass_assumption": False,
        },
        "Round122_F10_zero_role": (
            "same-key dependency/crosswalk only; the zero coarea face value"
            " does not pay the nonzero F14 accepted-norm cost"
        ),
        "stagewise_output_length_strict_lowers": {
            "stage1": "(3/100)*delta",
            "stage2": "(17/200)*delta",
            "stage3": "(4/125)*delta",
            "uniform": "(3/100)*delta",
        },
        "family_inverse_length_bound": (
            "sum_j M_j/ell_j < (100/(3*delta))*M"
        ),
        "no_output_member_count_multiplier": True,
        "one_step_accepted_norm_bound": (
            "N_out < M*(1+(93/100)*Reg_alpha_in"
            "+C_J+100/(3*delta))"
        ),
        "F14_one_step_slot_value": F14_ONE_STEP,
        "F14_one_step_exact_margin": qstr(one_step_margin),
        "generic_three_physical_leg_compositional_bound": (
            F14_COMPOSITIONAL_THREE_LEG
        ),
        "generic_composition_identity": "34^3=39304",
        "physical_collision_factor_count": 3,
        "roof_level_slot_count_per_subbranch": 5,
        "roof_split_does_not_change_34_cubed_to_34_to_the_fifth": True,
        "direct_exact_seed_three_leg_distortion_B": str(
            DIRECT_THREE_LEG_B
        ),
        "direct_exact_seed_three_leg_F14_bound": F14_ONE_STEP,
        "direct_exact_seed_three_leg_exact_margin": qstr(direct_margin),
        "direct_three_leg_bound_is_not_a_one_step_slot": True,
        "signed_Jordan_extension": (
            "apply the positive bound to positive and negative Jordan parts"
            " and take the strong-norm positive-decomposition infimum"
        ),
        "signed_extension_adds_no_factor_two": True,
        "cancellation_is_not_used_to_reduce_cost": True,
    }


def build(
    precision_bits: int = PRECISION_BITS,
    root_bisections: int = ROOT_BISECTIONS,
) -> dict[str, Any]:
    require(precision_bits >= 1024, "producer precision")
    require(root_bisections >= 200, "root depth")
    round121, round122 = load_final_inputs()
    common_document = common.build(precision_bits, root_bisections)
    base = dict(common_document["result"])
    base.pop("status")
    base.pop("strict_scope")
    base.pop("strict_nonclaims")
    base.pop("upstream_and_helper_pins")

    leg_rows = enrich_leg_rows(
        base["accepted_norm_leg_output_rows"],
        round121,
        round122,
    )
    base["accepted_norm_leg_output_rows"] = leg_rows
    base["accepted_norm_leg_output_rows_sha256"] = digest(leg_rows)
    f14_rows = build_f14_slots(round121, leg_rows)

    inherited_ids = [
        row["slot_id"] for row in round121["gate5_F1_F6_slot_rows"]
    ] + [
        row["slot_id"] for row in round122["gate5_F7_F13_F16_slot_rows"]
    ]
    require(
        len(inherited_ids) == len(set(inherited_ids)) == 1680,
        "1680 inherited slots",
    )
    require(
        digest(inherited_ids)
        == round122["combined_F1_F13_F16_slot_registry"][
            "combined_slot_ids_sha256"
        ],
        "Round122 combined slot digest",
    )
    combined_ids = inherited_ids + [row["slot_id"] for row in f14_rows]
    require(
        len(combined_ids) == len(set(combined_ids)) == 1800,
        "1800 combined slots",
    )
    all_keys = [
        canonical(row["immutable_slot_key"])
        for row in round121["gate5_F1_F6_slot_rows"]
    ] + [
        canonical(row["immutable_slot_key"])
        for row in round122["gate5_F7_F13_F16_slot_rows"]
    ] + [
        canonical(row["immutable_slot_key"]) for row in f14_rows
    ]
    require(len(all_keys) == len(set(all_keys)) == 1800,
            "1800 immutable keys")

    gate_status = dict(round122["gate5_actual_child_field_status"])
    gate_status["F14"] = (
        "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN"
    )
    base.update(
        {
            "status": (
                "CERTIFIED_EXACT_SEED_STAGE3_OUTPUT_PROPERIZATION"
                "__F14_INSTALLED"
            ),
            "round121_contract": {
                "result_sha256": (
                    "962db517d76b18e7681c411734b568491e600776dbf5317d9ebff8494a9aebd8"
                ),
                "actual_child_count": 24,
                "inherited_F1_F6_slot_count": 720,
            },
            "round122_contract": {
                "certificate_sha256": PINS[
                    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json"
                ],
                "result_sha256": (
                    "e8bc4e02635b70dda7cee0485811ae68d42ee595c37a03a5b2aa94ecf170f6cb"
                ),
                "inherited_certified_field_indices": (
                    list(range(1, 14)) + [16]
                ),
                "inherited_slot_count": 1680,
            },
            "arbitrary_density_and_Jordan_contract": operator_theorem(),
            "stagewise_output_length_theorem": {
                "leg_output_row_count": 72,
                "rows_per_physical_leg": 24,
                "all_leg_inputs_have_adapted_length_less_or_equal_delta": True,
                "stage1_output_member_length_strict_lower": "3/100*delta",
                "stage2_output_member_length_strict_lower": "17/200*delta",
                "stage3_output_fragment_length_strict_lower": "4/125*delta",
                "uniform_output_member_length_strict_lower": "3/100*delta",
                "all_output_member_lengths_less_or_equal_delta": True,
                "stage3_output_fragment_count": 216,
                "stage3_fragments_are_payload_not_source_slots": True,
            },
            "gate5_F14_slot_rows": f14_rows,
            "gate5_F14_slot_rows_sha256": digest(f14_rows),
            "combined_F1_F14_F16_slot_registry": {
                "inherited_Round122_slot_count": 1680,
                "new_F14_slot_count": 120,
                "combined_slot_count": 1800,
                "slot_count_per_certified_field": 120,
                "certified_field_indices": list(range(1, 15)) + [16],
                "combined_slot_ids_sha256": digest(combined_ids),
                "all_immutable_slot_keys_are_full_word_subbranch_roof_field_keys": True,
                "F14_slots_are_source_full_keys_not_output_fragment_keys": True,
            },
            "count_ledger": {
                **base["derived_count_ledger"],
                "actual_child_count": 24,
                "accepted_norm_leg_output_row_count": 72,
                "stage3_output_fragment_count": 216,
                "new_F14_slot_count": 120,
                "inherited_Round122_slot_count": 1680,
                "combined_child_local_slot_count": 1800,
                "certified_child_local_field_count": 15,
                "complete_18_field_block_count": 0,
            },
            "gate5_actual_child_field_status": gate_status,
            "rank3_seed_child_field_maturity": "15/18",
            "remaining_uninstalled_child_fields": ["F15", "F17", "F18"],
            "gate5_global_maturity": "10/18",
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "cm2_verdict": "NO-GO_FOR_CLAIM",
            "strict_scope": (
                "one Round121 exact-b seed, its 24 materialized common children,"
                " three physical collision legs, and the 216-member actual-third"
                " output properization"
            ),
            "strict_nonclaims": [
                "no full Borel-b family uniform materialization or ranking theorem",
                "no creation of 216 output-fragment source F14 slots",
                "no multiplication by 193, 216, or five symbolic roof levels",
                "no F15 standard-family operator cost",
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
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--root-bisections", type=int, default=ROOT_BISECTIONS)
    args = parser.parse_args()
    document = build(args.precision_bits, args.root_bisections)
    text = json.dumps(document, sort_keys=True, indent=2, allow_nan=False) + "\n"
    args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
