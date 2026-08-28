#!/usr/bin/env python3
"""Round129: one positive-Borel rank-three recut and field stratum.

Round121 certified one exact analytic parent-W seed.  This producer thickens
that seed in the analytic miss coordinate

    lambda = b3 in [3/65536 - 2^-512, 3/65536 + 2^-512]

while keeping c0=1/16384.  The implicit BYPASS root is enclosed on the whole
collar, the induced intercept b(lambda) is proved strictly increasing with a
rational derivative lower bound, and all twenty-three Round121 pullback
guards are replayed uniformly.

The Borel fibre parameter ``lambda`` is not the physical deformation
parameter ``s``.  Independently, the Round122 collar |s|<=2^-512 is replayed
over the whole lambda collar.  This retains the twenty-five artificial recut
faces while proving that the complete typed physical-face family is empty.

The finite rows below are parameterized registry templates.  Every exact
lambda locator emits 24 actual children and 1680 actual F1--F13/F16 slots,
but the uncountable family is never misreported as a finite actual-slot
census.  The result is one positive-Borel local 14/18 stratum; global Gate5
remains 10/18 and CM2 remains NO-GO_FOR_CLAIM.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_round113_rank3_root_sheet_owner_ordering_spike as r113
import cm2_round121_rank3_exact_seed_three_leg_recut_f5f6 as r121
import cm2_round122_rank3_exact_seed_physical_face_field_bridge as r122


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2-round129-rank3-positive-borel-recut-field-bridge-2026-07-24.json"
SCHEMA = "cm2.round129.rank3-positive-borel-recut-field-bridge.v1"
PRECISION_BITS = 4096

LAMBDA_CENTER = Q(3, 65536)
LAMBDA_EPSILON = Q(1, 2**512)
LAMBDA_LOWER = LAMBDA_CENTER - LAMBDA_EPSILON
LAMBDA_UPPER = LAMBDA_CENTER + LAMBDA_EPSILON
LAMBDA_INTERVAL_LENGTH = 2 * LAMBDA_EPSILON
FIXED_C0 = Q(1, 16384)
T_GUARD_PADDING = Q(1, 2**520)
S_EPSILON = Q(1, 2**512)

DT_D_LAMBDA_LOWER = Q(1, 4_000_000)
DT_D_LAMBDA_UPPER = Q(1, 3_000_000)
DB_D_LAMBDA_LOWER = Q(1, 2_250_000)
DB_D_LAMBDA_UPPER = Q(1, 2_000_000)
B_IMAGE_LENGTH_LOWER = LAMBDA_INTERVAL_LENGTH * DB_D_LAMBDA_LOWER

CERTIFICATE_FILES = {
    120: (
        "cm2-round120-rank3-relative-interior-actual-standard-curve-recut-2026-07-23.json",
        "cm2-round120-rank3-relative-interior-actual-standard-curve-recut-verification-2026-07-23.json",
    ),
    121: (
        "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json",
        "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json",
    ),
    122: (
        "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json",
        "cm2-round122-rank3-exact-seed-physical-face-field-bridge-verification-2026-07-23.json",
    ),
    123: (
        "cm2-round123-rank3-exact-seed-stage3-output-properization-f14-2026-07-23.json",
        "cm2-round123-rank3-exact-seed-stage3-output-properization-f14-verification-2026-07-23.json",
    ),
    124: (
        "cm2-round124-rank3-exact-seed-standard-family-operator-f15-2026-07-23.json",
        "cm2-round124-rank3-exact-seed-standard-family-operator-f15-verification-2026-07-23.json",
    ),
    125: (
        "cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-2026-07-23.json",
        "cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-verification-2026-07-23.json",
    ),
    126: (
        "cm2-round126-rank3-exact-seed-operator-phase-block-f18-2026-07-23.json",
        "cm2-round126-rank3-exact-seed-operator-phase-block-f18-verification-2026-07-23.json",
    ),
    127: (
        "cm2-round127-global-return-word-exact-seed-crosswalk-2026-07-24.json",
        "cm2-round127-global-return-word-exact-seed-crosswalk-verification-2026-07-24.json",
    ),
    128: (
        "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json",
        "cm2-round128-base-r1-component-global-word-incidence-verification-2026-07-24.json",
    ),
}

PINS = {
    "cm2-round120-rank3-relative-interior-actual-standard-curve-recut-2026-07-23.json":
        "a7b9df3450268c9a812aff682520ae24b36970a0526bad9aad15431a79f288d5",
    "cm2-round120-rank3-relative-interior-actual-standard-curve-recut-verification-2026-07-23.json":
        "ad5be920fc6864009f5d2966d41b9271419aa053866c5ac50d8d7186731c17bc",
    "cm2_round120_rank3_relative_interior_actual_standard_curve_recut.py":
        "ea1b4cd78a8009063e87cfe09b0d3fa80097f430a1f742d5f109761c20973a9a",
    "cm2_round120_rank3_relative_interior_actual_standard_curve_recut_verifier.py":
        "5d9c48807fdc540fc53970508bd377c911d98ec72b49a210a5ca05777b708a18",
    "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json":
        "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e",
    "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json":
        "ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80",
    "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py":
        "30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed",
    "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6_verifier.py":
        "d35c0e04b9d339c1271533abdefa5addcb73096b70abdec94d60e475daa45e95",
    "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json":
        "a7ed51149916bbf0d181b9cd45114cd11d81a5d30e72fea50b3336d1ead22028",
    "cm2-round122-rank3-exact-seed-physical-face-field-bridge-verification-2026-07-23.json":
        "aa0eca5e14fccbeeaad74d075cce0f10ee01f4caf8fccd0e9130ccc0e5cba82b",
    "cm2_round122_rank3_exact_seed_physical_face_field_bridge.py":
        "44a64789635b8adfb597376d25afcbf8cb39dbaf0c2a19c4031bcbe78b3848f4",
    "cm2_round122_rank3_exact_seed_physical_face_field_bridge_verifier.py":
        "bcf6e34398dcd2fd4cb6bb23aec649db5df75d26a80f307e58521d8ef439d31e",
    "cm2-round123-rank3-exact-seed-stage3-output-properization-f14-2026-07-23.json":
        "d3d45e32e45d1a37d5364c0d5fc1f34b537190c2450b7e8f9ead729dc77fe993",
    "cm2-round123-rank3-exact-seed-stage3-output-properization-f14-verification-2026-07-23.json":
        "37b70e60e1b9a66875e4565a44c115d50f55d718320fa79187d26bc45a1136d6",
    "cm2_round123_rank3_exact_seed_stage3_output_properization_f14.py":
        "e00b85d722e3784c0c2427ea0f7b32f8306b9d706b902b22df334b8aa9b00c38",
    "cm2_round123_rank3_exact_seed_stage3_output_properization_f14_verifier.py":
        "eec966baae120a442f621e03f4575161545fc6d65604aba5f255a440c90f0625",
    "cm2-round124-rank3-exact-seed-standard-family-operator-f15-2026-07-23.json":
        "ec2df85d5caf87f4bd25fa70c32afc5893bfbb147c3d0af21b3be9bc09c62b3b",
    "cm2-round124-rank3-exact-seed-standard-family-operator-f15-verification-2026-07-23.json":
        "3c1987adcefd7986128b5a35c77babd3c00f760ef28d8b73f491961f0dff0ccd",
    "cm2_round124_rank3_exact_seed_standard_family_operator_f15.py":
        "084634863c9ecb9dd16fe1c16ef7ae286315525509b5d703df48359426a291a5",
    "cm2_round124_rank3_exact_seed_standard_family_operator_f15_verifier.py":
        "4a964cc016cee5de5cc42469bee96f87f61803f46973da24084e79a02e770a3f",
    "cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-2026-07-23.json":
        "cecae7d1b864abcb62215c317bb87bbf392848c70b6affca253d350a9f687579",
    "cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-verification-2026-07-23.json":
        "919c50840eee75bcebb7ed8d870f2300d6a47466055bd4d25d95645dbbc6bd62",
    "cm2_round125_rank3_exact_seed_graph_current_dynamic_test_f17.py":
        "e360c511c87f10483ee19cf566d9542f123a2fbdf37585d9954a9c33575b940b",
    "cm2_round125_rank3_exact_seed_graph_current_dynamic_test_f17_verifier.py":
        "15f5313fc9f9593a0e1d41b95a9c09f7cc204f3471e177c17b1355b9a3f13737",
    "cm2-round126-rank3-exact-seed-operator-phase-block-f18-2026-07-23.json":
        "5980d0714aade1d71b32d3fa280d157e98dc97cefca2dd1e8e614f5203a8897e",
    "cm2-round126-rank3-exact-seed-operator-phase-block-f18-verification-2026-07-23.json":
        "bfbee771cc25cfb623297fe5e5c63483cbd296c372c1c4a143b247c834046f4b",
    "cm2_round126_rank3_exact_seed_operator_phase_block_f18.py":
        "db5a3a4250e26bdeeb6ac4a2a6abade5014073b5901339e30d5c4b4907fcba68",
    "cm2_round126_rank3_exact_seed_operator_phase_block_f18_verifier.py":
        "2fa8136e0c07457486515bc7c342a4857ed61705f33c7a91bf681ab02905a9ec",
    "cm2-round127-global-return-word-exact-seed-crosswalk-2026-07-24.json":
        "4aa7cde5e22883dfcb8e59f16e7bd6ab16c4436229c9964384ef72dda0c16408",
    "cm2-round127-global-return-word-exact-seed-crosswalk-verification-2026-07-24.json":
        "5958b4905b8e005886302a6bffc32d15fd1091cf8dbe20b743488e3f91eeb383",
    "cm2_round127_global_return_word_exact_seed_crosswalk.py":
        "ea461b3ed1301149bca350f32190348aca955f0a04ce42663fab23451144b0dd",
    "cm2_round127_global_return_word_exact_seed_crosswalk_verifier.py":
        "24de0b53c872d43f0a0d7422164e5a2a776a1d35879c923bcf5a07afef94e157",
    "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json":
        "7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e",
    "cm2-round128-base-r1-component-global-word-incidence-verification-2026-07-24.json":
        "3798cb3e38b7f26de0a5361234d57ef626bd7f990e26d6c787f0abf62647a76d",
    "cm2_round128_base_r1_component_global_word_incidence.py":
        "d218d92a6aa7a929e734c86110e67ec8ebea75b3c57bf74e5a7d3b3e33d32e35",
    "cm2_round128_base_r1_component_global_word_incidence_verifier.py":
        "2745ccccdab9869c4754bab37f13ece70f32c7b59063bf0aed4f59cdd81af544",
}

CERTIFIED_FIELDS = tuple(range(1, 14)) + (16,)
FIELD_NAMES = {
    **{index: name for index, name in enumerate(r121.GATE5_FIELDS, start=1)},
    **{index: name for index, name in r122.NEW_FIELDS},
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def strict_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), f"unsafe input: {path.name}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_float=lambda token: (_ for _ in ()).throw(
            ValueError(f"floating JSON number forbidden: {token}")
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"invalid JSON constant: {token}")
        ),
    )
    require(type(value) is dict, f"top-level JSON object: {path.name}")
    return value


def load_closed(path: Path) -> dict[str, Any]:
    value = strict_json(path)
    require(set(value) == {"schema", "result", "result_sha256"}, f"closed envelope: {path.name}")
    require(type(value["schema"]) is str and type(value["result"]) is dict, f"closed types: {path.name}")
    require(value["result_sha256"] == digest(value["result"]), f"result digest: {path.name}")
    return value


def arb_bounds(value: arb) -> tuple[Q, Q]:
    return r121.arb_pair(value)


def interval_strings(value: arb) -> list[str]:
    lower, upper = arb_bounds(value)
    return [qstr(lower), qstr(upper)]


def validate_frozen_chain() -> dict[int, dict[str, Any]]:
    for name, expected in sorted(PINS.items()):
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pinned file type: {name}")
        require(path.resolve().parent == HERE, f"pinned file parent: {name}")
        require(sha256(path) == expected, f"pin mismatch: {name}")

    documents: dict[int, dict[str, Any]] = {}
    for round_index, (certificate_name, verification_name) in sorted(CERTIFICATE_FILES.items()):
        certificate = load_closed(HERE / certificate_name)
        verification = load_closed(HERE / verification_name)
        verification_status = (
            verification["result"].get("verdict")
            or verification["result"].get("status")
        )
        require(verification_status == "PASS", f"Round{round_index} verification PASS")
        documents[round_index] = {
            "certificate": certificate,
            "verification": verification,
        }

    for round_index in range(120, 127):
        result = documents[round_index]["certificate"]["result"]
        require(result["gate5_global_maturity"] == "10/18", f"Round{round_index} global maturity")
        require(result["complete_18_field_block_count"] == 0, f"Round{round_index} complete blocks")
        require(result["cm2_verdict"] == "NO-GO_FOR_CLAIM", f"Round{round_index} CM2")

    round127 = documents[127]["certificate"]["result"]["global_safety_state"]
    require(round127["gate5_global_maturity"] == "10/18", "Round127 global maturity")
    require(round127["global_complete_18_field_block_count"] == 0, "Round127 global blocks")
    require(round127["cm2_verdict"] == "NO-GO_FOR_CLAIM", "Round127 CM2")

    round128 = documents[128]["certificate"]["result"]["D_global_safety_and_nonpromotion"]
    require(round128["gate5_global_maturity"] == "10/18", "Round128 global maturity")
    require(round128["global_complete_18_field_block_count"] == 0, "Round128 global blocks")
    require(round128["CM2"] == "NO-GO_FOR_CLAIM", "Round128 CM2")
    require(round128["global_exact_nonempty_candidate_key_count"] is None, "Round128 null global census")
    return documents


def family_root_contract(
    seed: dict[str, Any],
    exact_root_lower: Q,
    exact_root_upper: Q,
) -> tuple[dict[str, Any], tuple[Q, Q]]:
    require(LAMBDA_LOWER > Q(1, 32768), "lambda lower inside Round113 parent")
    require(LAMBDA_UPPER < Q(1, 16384), "lambda upper inside Round113 parent")
    t_lower = exact_root_lower - T_GUARD_PADDING
    t_upper = exact_root_upper + T_GUARD_PADDING

    lower_value = r113.equation_value(
        seed["source"], r121.EXPECTED_BRANCH, 1, "BYPASS",
        t_lower, FIXED_C0, FIXED_C0, LAMBDA_LOWER, LAMBDA_UPPER,
    )
    upper_value = r113.equation_value(
        seed["source"], r121.EXPECTED_BRANCH, 1, "BYPASS",
        t_upper, FIXED_C0, FIXED_C0, LAMBDA_LOWER, LAMBDA_UPPER,
    )
    lower_sign = r113.strict_sign(lower_value)
    upper_sign = r113.strict_sign(upper_value)
    require((lower_sign, upper_sign) == (1, -1), "uniform lambda root face signs")

    geometry = r113.path_geometry(
        seed["source"], r121.EXPECTED_BRANCH, 1, "BYPASS",
        t_lower, t_upper, FIXED_C0, FIXED_C0, LAMBDA_LOWER, LAMBDA_UPPER,
    )
    partial_t = geometry["equation"].gradient[0]
    partial_lambda = geometry["equation"].gradient[2]
    partial_t_lower, partial_t_upper = arb_bounds(partial_t)
    partial_lambda_lower, partial_lambda_upper = arb_bounds(partial_lambda)
    require(-8 < partial_t_lower and partial_t_upper < -7, "uniform -8<F_t<-7")
    require(
        Q(1, 500_000) < partial_lambda_lower
        and partial_lambda_upper < Q(3, 1_000_000),
        "uniform 2e-6<F_lambda<3e-6",
    )

    dt_d_lambda = -partial_lambda / partial_t
    dt_lower, dt_upper = arb_bounds(dt_d_lambda)
    require(
        dt_lower > DT_D_LAMBDA_LOWER
        and dt_upper < DT_D_LAMBDA_UPPER,
        "uniform dt/dlambda",
    )

    radial_t = (arb(1) - r121.interval(t_lower, t_upper) ** 2).sqrt()
    db_d_lambda = arb(36) / 25 / radial_t * dt_d_lambda
    db_lower, db_upper = arb_bounds(db_d_lambda)
    require(
        db_lower > DB_D_LAMBDA_LOWER
        and db_upper < DB_D_LAMBDA_UPPER,
        "uniform db/dlambda",
    )
    require(B_IMAGE_LENGTH_LOWER > 0, "positive b-image length")

    family_root_payload = [
        "round129-positive-borel-family-root-v1",
        r121.EXPECTED_SHEET_ID,
        r121.PARENT_ID,
        r121.OPERATOR_CELL_ID,
        r121.ANGULAR_LIFT_ID,
        qstr(FIXED_C0),
        qstr(LAMBDA_LOWER),
        qstr(LAMBDA_UPPER),
    ]
    family_root_id = "round129-positive-borel-family-root:" + digest(family_root_payload)
    contract = {
        "family_root_id": family_root_id,
        "round112_sheet_id": r121.EXPECTED_SHEET_ID,
        "round113_parent_id": r121.PARENT_ID,
        "round117_operator_cell_id": r121.OPERATOR_CELL_ID,
        "angular_lift_id": r121.ANGULAR_LIFT_ID,
        "sheet_kind": "BYPASS",
        "branch_key": list(r121.EXPECTED_BRANCH),
        "fixed_c0": qstr(FIXED_C0),
        "lambda_coordinate": "b3",
        "lambda_exact_dyadic_closed_collar": [qstr(LAMBDA_LOWER), qstr(LAMBDA_UPPER)],
        "lambda_center": qstr(LAMBDA_CENTER),
        "lambda_epsilon": qstr(LAMBDA_EPSILON),
        "lambda_interval_length_exact": qstr(LAMBDA_INTERVAL_LENGTH),
        "lambda_collar_inside_one_Round113_parent_and_Round117_operator_cell": True,
        "exact_Round121_anchor_root_bracket": [
            qstr(exact_root_lower), qstr(exact_root_upper),
        ],
        "uniform_t_guard_padding": qstr(T_GUARD_PADDING),
        "uniform_t_guard": [qstr(t_lower), qstr(t_upper)],
        "uniform_t_guard_face_signs": [lower_sign, upper_sign],
        "uniform_F_t_enclosure": interval_strings(partial_t),
        "uniform_F_lambda_enclosure": interval_strings(partial_lambda),
        "uniform_simple_F_t_bounds": "-8<F_t<-7",
        "uniform_simple_F_lambda_bounds": "1/500000<F_lambda<3/1000000",
        "implicit_dt_dlambda_enclosure": interval_strings(dt_d_lambda),
        "implicit_dt_dlambda_strict_bounds": (
            "1/4000000<dt/dlambda<1/3000000"
        ),
        "b_of_lambda_definition": (
            "b(lambda)=acos(1/16384)-(36/25)*(pi-asin(t(lambda)))"
        ),
        "db_dlambda_enclosure": interval_strings(db_d_lambda),
        "db_dlambda_strict_bounds": (
            "1/2250000<db/dlambda<1/2000000"
        ),
        "b_of_lambda_strictly_increasing": True,
        "b_image_length_MVT_formula": (
            "(lambda_upper-lambda_lower)*inf(db/dlambda)"
        ),
        "b_image_length_strict_lower_exact": qstr(B_IMAGE_LENGTH_LOWER),
        "b_image_is_a_non_degenerate_positive_Borel_interval": True,
        "analytic_IFT_root_sheet_used": True,
        "finite_precision_enclosure_text_participates_in_family_ID": False,
    }
    return contract, (t_lower, t_upper)


def family_endpoint_rows(
    family_root_id: str,
    seed: dict[str, Any],
    t_guard: tuple[Q, Q],
    round121: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[tuple[int, int], str]]:
    adapted = r121.adapted_data(seed, t_guard)
    replay = r121.isolate_pullback_endpoints(
        seed, t_guard, adapted, family_root_id,
    )
    frozen = {
        (row["stage"], row["natural_index_j"]): row
        for row in round121["pullback_endpoint_rows"]
    }
    require(len(replay) == len(frozen) == 23, "family endpoint count")

    rows: list[dict[str, Any]] = []
    face_ids: dict[tuple[int, int], str] = {}
    for row in replay:
        key = (row["stage"], row["natural_index_j"])
        inherited = frozen[key]
        require(
            row["x_dyadic_bracket"] == inherited["x_dyadic_bracket"],
            f"uniform guard equals Round121 guard: {key}",
        )
        require(
            (row["left_function_sign"], row["right_function_sign"]) == (-1, 1),
            f"uniform endpoint signs: {key}",
        )
        face_id = "round129-uniform-pullback-face-template:" + digest([
            "round129-uniform-pullback-face-template-v1",
            family_root_id, row["stage"], row["natural_index_j"],
        ])
        face_ids[key] = face_id
        item = {
            "face_template_id": face_id,
            "family_root_id": family_root_id,
            "stage": row["stage"],
            "natural_index_j": row["natural_index_j"],
            "exact_level_equation": (
                f"U{row['stage']}(lambda,x)={row['natural_index_j']}*10^-90"
            ),
            "Round121_guard_endpoint_id": inherited["endpoint_id"],
            "uniform_x_dyadic_guard": row["x_dyadic_bracket"],
            "uniform_guard_exactly_equals_Round121_guard": True,
            "guard_width": row["x_bracket_width_upper"],
            "all_lambda_left_function_sign": row["left_function_sign"],
            "all_lambda_right_function_sign": row["right_function_sign"],
            "all_lambda_normalized_U_x_strict_lower": row[
                "normalized_derivative_abs_strict_lower"
            ],
            "U_x_sign": row["derivative_sign"],
            "unique_root_for_every_exact_lambda": True,
            "unique_analytic_lambda_graph_by_IFT": True,
            "family_actual_endpoint_id_constructor": (
                "round129-endpoint:sha256(canonical([face-template-id,"
                "exact-lambda-locator]))"
            ),
            "exact_lambda_locator_required_for_actual_endpoint_ID": True,
            "numeric_guard_text_participates_in_actual_endpoint_ID": False,
        }
        item["row_sha256"] = digest(item)
        rows.append(item)

    rows.sort(key=lambda item: Q(item["uniform_x_dyadic_guard"][0]))
    require(
        tuple((row["stage"], row["natural_index_j"]) for row in rows)
        == r121.EXPECTED_CUT_ORDER,
        "uniform family cut order",
    )
    boundaries = [
        ("outer-left", Q(0), Q(0)),
        *[
            (
                row["face_template_id"],
                Q(row["uniform_x_dyadic_guard"][0]),
                Q(row["uniform_x_dyadic_guard"][1]),
            )
            for row in rows
        ],
        ("outer-right", Q(1), Q(1)),
    ]
    gaps = [
        boundaries[index + 1][1] - boundaries[index][2]
        for index in range(len(boundaries) - 1)
    ]
    require(len(gaps) == 24 and min(gaps) > Q(1, 200), "uniform 24 positive gaps")

    stage_contract = {
        "source_adapted_coordinate": "u0(lambda,x)=10^-90*x",
        "source_parameter_domain_per_fibre": "[0,1)",
        "slope_four_identity_per_fibre": (
            "phi0(lambda,x)-4*(9/25)*theta0(lambda,x)=b(lambda)"
        ),
        "stage_orientations": [1, -1, 1],
        "U1_length_over_delta_enclosure": interval_strings(adapted["length1_ratio"]),
        "U2_length_over_delta_enclosure": interval_strings(adapted["length2_ratio"]),
        "U1_prime_over_delta_enclosure": interval_strings(adapted["derivative1_ratio"]),
        "U2_prime_over_delta_enclosure": interval_strings(adapted["derivative2_ratio"]),
        "uniform_simple_length_bounds": [
            "34/5<U1(lambda,1)/delta<7",
            "87/5<U2(lambda,1)/delta<18",
        ],
        "uniform_simple_derivative_bounds": [
            "6<U1_x/delta<7",
            "17<U2_x/delta<18",
        ],
        "uniform_natural_cell_counts": [1, 7, 18],
        "uniform_internal_cut_counts": [0, 6, 17],
        "uniform_pullback_cut_count": 23,
        "uniform_common_rank_count": 24,
        "minimum_24_child_x_length_strict_lower_exact": qstr(min(gaps)),
        "minimum_24_child_x_length_exceeds_1_over_200": True,
        "uniform_cut_order": [
            f"S{stage}:{natural_index}"
            for stage, natural_index in r121.EXPECTED_CUT_ORDER
        ],
        "whole_lambda_collar_same_Round113_owner_path_and_Round117_homogeneity": True,
    }
    return stage_contract, rows, face_ids


def family_recut_rows(
    family_root_id: str,
    face_ids: dict[tuple[int, int], str],
    round121: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[tuple[int, int], str]]:
    frozen = {
        (row["stage"], row["natural_index_j"]): row
        for row in round121["stage_recut_rows"]
    }
    rows: list[dict[str, Any]] = []
    recut_ids: dict[tuple[int, int], str] = {}
    for stage, count in enumerate((1, 7, 18)):
        for natural_index in range(count):
            key = (stage, natural_index)
            inherited = frozen[key]
            template_id = "round129-recut-template:" + digest([
                "round129-family-recut-template-v1",
                family_root_id, stage, natural_index,
            ])
            recut_ids[key] = template_id
            lower_face = (
                "round129-family-source-outer-left"
                if natural_index == 0
                else face_ids[(stage, natural_index)]
            )
            upper_face = (
                "round129-family-source-outer-right"
                if natural_index == count - 1
                else face_ids[(stage, natural_index + 1)]
            )
            item = {
                "recut_template_id": template_id,
                "family_root_id": family_root_id,
                "stage": stage,
                "natural_index_j": natural_index,
                "lower_face_template_id": lower_face,
                "upper_face_template_id": upper_face,
                "orientation": (1, -1, 1)[stage],
                "adapted_coordinate_id": inherited["adapted_coordinate_id"],
                "adapted_lower": inherited["adapted_lower"],
                "adapted_upper": inherited["adapted_upper"],
                "adapted_length_upper": inherited["adapted_length_upper"],
                "normalized_adapted_length_strict_lower": inherited[
                    "normalized_adapted_length_strict_lower"
                ],
                "roof_level_count": inherited["roof_level_count"],
                "official_word_key_id": inherited["official_word_key_id"],
                "lower_closed": inherited["lower_closed"],
                "upper_closed": inherited["upper_closed"],
                "source_parent_right_endpoint_is_open": inherited[
                    "source_parent_right_endpoint_is_open"
                ],
                "internal_cut_owned_by_right_natural_cell": inherited[
                    "internal_cut_owned_by_right_natural_cell"
                ],
                "actual_materialized_input_recut_for_every_exact_lambda": True,
                "family_actual_recut_id_constructor": (
                    "round129-recut:sha256(canonical([recut-template-id,"
                    "exact-lambda-locator]))"
                ),
                "exact_lambda_locator_required_for_actual_recut_ID": True,
                "finite_template_is_not_one_actual_fibre_recut": True,
            }
            item["row_sha256"] = digest(item)
            rows.append(item)
    require(len(rows) == 26, "family recut template count")
    return rows, recut_ids


def family_common_rank_rows(
    family_root_id: str,
    endpoint_rows: list[dict[str, Any]],
    recut_ids: dict[tuple[int, int], str],
    round121: dict[str, Any],
) -> list[dict[str, Any]]:
    outer_left = "round129-family-source-outer-left"
    outer_right = "round129-family-source-outer-right"
    boundaries: list[dict[str, Any]] = [{
        "face_template_id": outer_left,
        "uniform_x_dyadic_guard": ["0", "0"],
        "stage": 0,
        "natural_index_j": 0,
    }, *endpoint_rows, {
        "face_template_id": outer_right,
        "uniform_x_dyadic_guard": ["1", "1"],
        "stage": 0,
        "natural_index_j": 1,
    }]
    inherited = sorted(round121["common_refinement_rows"], key=lambda row: row["common_rank"])
    stage_indices = [0, 0, 0]
    rows: list[dict[str, Any]] = []
    for rank, (lower, upper) in enumerate(zip(boundaries, boundaries[1:])):
        gap = (
            Q(upper["uniform_x_dyadic_guard"][0])
            - Q(lower["uniform_x_dyadic_guard"][1])
        )
        require(gap > Q(1, 200), f"family common rank positive: {rank}")
        require(inherited[rank]["covering_stage_indices"] == stage_indices, f"covering stages: {rank}")
        template_id = "round129-common-rank-template:" + digest([
            "round129-family-common-rank-template-v1",
            family_root_id, rank,
        ])
        item = {
            "common_rank_template_id": template_id,
            "family_root_id": family_root_id,
            "common_rank": rank,
            "lower_face_template_id": lower["face_template_id"],
            "upper_face_template_id": upper["face_template_id"],
            "positive_source_x_length_strict_lower_exact": qstr(gap),
            "positive_source_x_length_exceeds_1_over_200": True,
            "covering_stage_indices": list(stage_indices),
            "source_recut_template_id": recut_ids[(0, 0)],
            "first_image_recut_template_id": recut_ids[(1, stage_indices[1])],
            "second_image_recut_template_id": recut_ids[(2, stage_indices[2])],
            "round117_operator_cell_id": r121.OPERATOR_CELL_ID,
            "official_path_id": inherited[rank]["official_path_id"],
            "typed_parent_W_id_constructor": (
                "round129-parent-W:sha256(canonical([family-root-id,"
                "angular-lift-id,exact-b-locator-derived-from-lambda]))"
            ),
            "refined_homogeneous_subbranch_id_constructor": (
                "round129-refined-subbranch:sha256(canonical([typed-parent-W-id,"
                "round117-operator-cell-id,source-k=0,common-rank]))"
            ),
            "actual_child_id_constructor": (
                "round129-common-child:sha256(canonical([refined-subbranch-id,"
                "exact-lambda-locator,common-rank]))"
            ),
            "exact_lambda_and_derived_exact_b_locators_required": True,
            "actual_standard_curve_child_exists_for_every_exact_lambda": True,
            "finite_common_rank_template_is_not_one_actual_fibre_child": True,
        }
        item["row_sha256"] = digest(item)
        rows.append(item)
        if rank < 23:
            crossed = upper
            require(crossed["stage"] in (1, 2), "internal crossed family face")
            stage_indices[crossed["stage"]] += 1
    require(stage_indices == [0, 6, 17], "family terminal stage indices")
    require(len(rows) == 24, "family common rank template count")
    return rows


def transformed_physical_audit(
    family_root_id: str,
    common_rows: list[dict[str, Any]],
    physical: dict[str, Any],
) -> dict[str, Any]:
    rank_ids = {
        row["common_rank"]: row["common_rank_template_id"]
        for row in common_rows
    }

    def transform(row: dict[str, Any]) -> dict[str, Any]:
        item = dict(row)
        rank = item["common_rank"]
        item.pop("common_child_id")
        item.pop("row_sha256")
        item["family_root_id"] = family_root_id
        item["common_rank_template_id"] = rank_ids[rank]
        item["uniform_over_entire_lambda_collar"] = True
        item["row_sha256"] = digest(item)
        return item

    core_rows = [transform(row) for row in physical["core_clearance_rows"]]
    child_stage_rows = [
        transform(row) for row in physical["child_stage_boundary_rows"]
    ]
    require(len(core_rows) == 96 and len(child_stage_rows) == 72, "family physical row counts")
    return {
        "family_core_clearance_rows": core_rows,
        "family_core_clearance_rows_sha256": digest(core_rows),
        "family_child_stage_boundary_rows": child_stage_rows,
        "family_child_stage_boundary_rows_sha256": digest(child_stage_rows),
        "check_counts": physical["check_counts"],
        "actual_interval_lower_minima": physical["actual_interval_lower_minima"],
        "claimed_strict_lower_margins": physical["claimed_strict_lower_margins"],
        "along_curve_diagnostic_upper_not_F11": physical[
            "along_seed_adapted_forward_Lipschitz_actual_upper"
        ],
        "rank3_candidate_occurrence_stage_counts": [57, 55, 57],
        "rank3_candidate_occurrence_count_per_common_rank": 169,
        "rank3_candidate_occurrence_total_check_count": 4056,
        "physical_five_face_incidence_count": 0,
        "residual_physical_face_count": 0,
        "complete_typed_physical_face_empty_on_lambda_times_s_collar": True,
    }


def family_artificial_face_registry(
    family_root_id: str,
    endpoint_face_ids: dict[tuple[int, int], str],
    common_rows: list[dict[str, Any]],
    moving: list[dict[str, Any]],
    stationary: list[dict[str, Any]],
) -> dict[str, Any]:
    moving_rows: list[dict[str, Any]] = []
    for inherited in moving:
        key = (inherited["stage"], inherited["natural_index_j"])
        item = {
            key_name: value
            for key_name, value in inherited.items()
            if key_name not in {
                "face_id", "exact_seed_id", "lower_trace_id", "upper_trace_id",
                "row_sha256", "round121_s0_endpoint_id", "exact_level_equation",
                "s_collar",
            }
        }
        item.update({
            "face_template_id": endpoint_face_ids[key],
            "family_root_id": family_root_id,
            "lambda_collar": [qstr(LAMBDA_LOWER), qstr(LAMBDA_UPPER)],
            "independent_s_collar": [qstr(-S_EPSILON), qstr(S_EPSILON)],
            "exact_level_equation": (
                f"U{key[0]}(lambda,x,s)={key[1]}*10^-90"
            ),
            "Round121_uniform_guard_endpoint_id": inherited[
                "round121_s0_endpoint_id"
            ],
            "lambda_and_s_are_distinct_parameters": True,
            "uniform_over_lambda_and_s_collar": True,
            "family_actual_face_id_constructor": (
                "round129-artificial-face:sha256(canonical([face-template-id,"
                "exact-lambda-locator]))"
            ),
        })
        item["row_sha256"] = digest(item)
        moving_rows.append(item)
    moving_rows.sort(key=lambda row: Q(row["s0_x_dyadic_bracket"][0]))
    require(
        [(row["stage"], row["natural_index_j"]) for row in moving_rows]
        == list(r121.EXPECTED_CUT_ORDER),
        "family moving face order",
    )

    outer_specs = (
        ("left", "round129-family-source-outer-left", "u0(lambda,x)=0"),
        ("right", "round129-family-source-outer-right", "u0(lambda,x)=10^-90"),
    )
    outer_rows: list[dict[str, Any]] = []
    for (label, face_id, equation), inherited in zip(outer_specs, stationary):
        item = {
            key_name: value
            for key_name, value in inherited.items()
            if key_name not in {
                "face_id", "exact_seed_id", "lower_trace_id", "upper_trace_id",
                "row_sha256", "exact_level_equation",
            }
        }
        item.update({
            "face_template_id": face_id,
            "family_root_id": family_root_id,
            "boundary_label": f"source-{label}",
            "exact_level_equation": equation,
            "lambda_collar": [qstr(LAMBDA_LOWER), qstr(LAMBDA_UPPER)],
            "independent_s_collar": [qstr(-S_EPSILON), qstr(S_EPSILON)],
            "lambda_and_s_are_distinct_parameters": True,
            "uniform_over_lambda_and_s_collar": True,
            "family_actual_face_id_constructor": (
                "round129-artificial-face:sha256(canonical([face-template-id,"
                "exact-lambda-locator]))"
            ),
        })
        item["row_sha256"] = digest(item)
        outer_rows.append(item)

    ordered_faces = [outer_rows[0], *moving_rows, outer_rows[1]]
    traces: list[dict[str, Any]] = []
    trace_index: dict[tuple[str, str], str] = {}
    for position, face in enumerate(ordered_faces):
        sides = ("upper",) if position == 0 else (
            ("lower",) if position == 24 else ("lower", "upper")
        )
        for side in sides:
            trace_id = "round129-artificial-trace-template:" + digest([
                "round129-family-artificial-trace-template-v1",
                face["face_template_id"], side,
            ])
            adjacent_rank = position - 1 if side == "lower" else position
            require(0 <= adjacent_rank < 24, "family trace adjacent rank")
            item = {
                "trace_template_id": trace_id,
                "face_template_id": face["face_template_id"],
                "side": side,
                "adjacent_common_rank": adjacent_rank,
                "adjacent_common_rank_template_id": common_rows[
                    adjacent_rank
                ]["common_rank_template_id"],
                "family_actual_trace_id_constructor": (
                    "round129-artificial-trace:sha256(canonical([trace-template-id,"
                    "exact-lambda-locator]))"
                ),
                "artificial_not_physical": True,
            }
            item["row_sha256"] = digest(item)
            traces.append(item)
            trace_index[(face["face_template_id"], side)] = trace_id
    require(len(traces) == 48, "family artificial trace count")

    incidences: list[dict[str, Any]] = []
    for rank in range(24):
        lower_face = ordered_faces[rank]["face_template_id"]
        upper_face = ordered_faces[rank + 1]["face_template_id"]
        item = {
            "incidence_template_id": "round129-child-face-incidence-template:" + digest([
                "round129-family-child-face-incidence-template-v1",
                family_root_id, rank, lower_face, upper_face,
            ]),
            "common_rank": rank,
            "common_rank_template_id": common_rows[rank]["common_rank_template_id"],
            "lower_face_template_id": lower_face,
            "upper_face_template_id": upper_face,
            "lower_trace_template_id": trace_index[(lower_face, "upper")],
            "upper_trace_template_id": trace_index[(upper_face, "lower")],
            "exactly_two_artificial_boundary_faces": True,
            "physical_face_incidence_count": 0,
        }
        item["row_sha256"] = digest(item)
        incidences.append(item)
    require(len(incidences) == 24, "family face incidence count")

    return {
        "stationary_outer_face_template_rows": outer_rows,
        "stationary_outer_face_template_rows_sha256": digest(outer_rows),
        "moving_artificial_face_template_rows": moving_rows,
        "moving_artificial_face_template_rows_sha256": digest(moving_rows),
        "artificial_trace_template_rows": traces,
        "artificial_trace_template_rows_sha256": digest(traces),
        "child_face_incidence_template_rows": incidences,
        "child_face_incidence_template_rows_sha256": digest(incidences),
        "stationary_outer_face_template_count": 2,
        "moving_artificial_face_template_count": 23,
        "artificial_face_template_count": 25,
        "artificial_trace_template_count": 48,
        "child_face_incidence_template_count": 24,
        "artificial_faces_retained_despite_physical_empty_statement": True,
    }


def base_and_field_templates(
    family_root_id: str,
    common_rows: list[dict[str, Any]],
    recut_ids: dict[tuple[int, int], str],
    artificial: dict[str, Any],
    round121: dict[str, Any],
    round122: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rank_by_child = {
        row["common_child_id"]: row["common_rank"]
        for row in round121["common_refinement_rows"]
    }
    exact_r121 = {
        (
            row["common_child_id"], row["stage"], row["roof_level_j"],
            row["field_index"],
        ): row
        for row in round121["gate5_F1_F6_slot_rows"]
    }
    exact_r122 = {
        (
            row["common_child_id"], row["stage"], row["roof_level_j"],
            row["field_index"],
        ): row
        for row in round122["gate5_F7_F13_F16_slot_rows"]
    }
    base_exact = sorted(
        (
            row for row in round121["gate5_F1_F6_slot_rows"]
            if row["field_index"] == 1
        ),
        key=lambda row: (
            rank_by_child[row["common_child_id"]],
            row["stage"], row["roof_level_j"],
        ),
    )
    require(len(base_exact) == 120, "family base template count")
    incidence_by_rank = {
        row["common_rank"]: row
        for row in artificial["child_face_incidence_template_rows"]
    }

    base_rows: list[dict[str, Any]] = []
    field_rows: list[dict[str, Any]] = []
    for base in base_exact:
        rank = rank_by_child[base["common_child_id"]]
        stage = base["stage"]
        roof = base["roof_level_j"]
        base_id = "round129-base-key-template:" + digest([
            "round129-family-base-key-template-v1",
            family_root_id, rank, base["official_word_key_id"], stage, roof,
        ])
        recut_template_id = recut_ids[
            (stage, common_rows[rank]["covering_stage_indices"][stage])
        ]
        base_item = {
            "base_key_template_id": base_id,
            "family_root_id": family_root_id,
            "common_rank": rank,
            "common_rank_template_id": common_rows[rank]["common_rank_template_id"],
            "official_word_key_id": base["official_word_key_id"],
            "stage": stage,
            "roof_level_j": roof,
            "materialized_input_recut_template_id": recut_template_id,
            "parameterized_base_key_constructor": (
                "(official-word-key-id,refined-subbranch-id(exact-b-locator),"
                "roof-level-j)"
            ),
            "per_exact_lambda_fibre_actual_base_key_exists": True,
            "finite_row_is_a_parameterized_template_not_an_actual_fibre_key": True,
        }
        base_item["row_sha256"] = digest(base_item)
        base_rows.append(base_item)

        for field_index in CERTIFIED_FIELDS:
            source_index = exact_r121 if field_index <= 6 else exact_r122
            inherited = source_index[(
                base["common_child_id"], stage, roof, field_index,
            )]
            require(inherited["field_name"] == FIELD_NAMES[field_index], "field name crosswalk")
            item = {
                "field_slot_template_id": "round129-field-slot-template:" + digest([
                    "round129-family-field-slot-template-v1",
                    base_id, field_index, FIELD_NAMES[field_index],
                ]),
                "base_key_template_id": base_id,
                "family_root_id": family_root_id,
                "common_rank": rank,
                "official_word_key_id": base["official_word_key_id"],
                "stage": stage,
                "roof_level_j": roof,
                "field_index": field_index,
                "field_name": FIELD_NAMES[field_index],
                "field_value_or_contract": inherited["field_value_or_contract"],
                "field_bound_semantics": inherited.get(
                    "field_bound_semantics", "INHERITED_EXACT_CONTRACT"
                ),
                "parameterized_immutable_slot_key_constructor": (
                    "(official-word-key-id,refined-subbranch-id(exact-b-locator),"
                    "roof-level-j,field-name)"
                ),
                "parameterized_actual_slot_id_constructor": (
                    "round129-slot:sha256(canonical([official-word-key-id,"
                    "refined-subbranch-id(exact-b-locator),roof-level-j,field-name]))"
                ),
                "exact_lambda_locator_and_derived_exact_b_locator_required": True,
                "per_exact_lambda_fibre_actual_slot_certified": True,
                "finite_row_is_a_parameterized_slot_template_not_an_actual_slot": True,
                "slot_template_status": (
                    "CERTIFIED_ON_EVERY_EXACT_LAMBDA_FIBRE_COMMON_CHILD"
                ),
                "materialized_input_recut_template_id": recut_template_id,
                "transparent_wall_roof_split_does_not_add_collision_factor": True,
            }
            if field_index >= 7:
                incidence = incidence_by_rank[rank]
                item.update({
                    "child_face_incidence_template_id": incidence[
                        "incidence_template_id"
                    ],
                    "lower_artificial_face_template_id": incidence[
                        "lower_face_template_id"
                    ],
                    "upper_artificial_face_template_id": incidence[
                        "upper_face_template_id"
                    ],
                    "complete_physical_face_empty_audit_bound": True,
                })
            if field_index == 5:
                item["uniform_template_scope"] = (
                    "every actual homogeneous physical solid-collision child "
                    "on a canonical adapted standard curve"
                )
            if field_index == 6:
                item.update({
                    "uniform_template_scope": (
                        "one canonical-curve log-Jacobian oscillation on this leg"
                    ),
                    "three_leg_only_not_arbitrary_return_depth": True,
                })
            if field_index == 11:
                item.update({
                    "full_phase_authoritative_envelope_used": True,
                    "along_curve_diagnostic_used_as_field_value": False,
                    "alpha_scope": "0<alpha<=1",
                })
            item["row_sha256"] = digest(item)
            field_rows.append(item)

    require(len(base_rows) == 120, "120 finite base templates")
    require(len({row["base_key_template_id"] for row in base_rows}) == 120, "unique base templates")
    require(len(field_rows) == 1680, "1680 finite field templates")
    require(
        len({
            (row["base_key_template_id"], row["field_index"])
            for row in field_rows
        }) == 1680,
        "field templates exact once",
    )
    field_counts = Counter(row["field_index"] for row in field_rows)
    require(
        field_counts == Counter({field_index: 120 for field_index in CERTIFIED_FIELDS}),
        "120 templates per certified field",
    )
    grouped: dict[str, list[int]] = defaultdict(list)
    for row in field_rows:
        grouped[row["base_key_template_id"]].append(row["field_index"])
    require(
        all(sorted(indices) == list(CERTIFIED_FIELDS) for indices in grouped.values()),
        "fourteen fields exact once on each base template",
    )
    return base_rows, field_rows


def safe_output_path(path: Path) -> None:
    resolved_parent = path.parent.resolve()
    require(resolved_parent.is_dir(), "output parent directory")
    protected = [Path(__file__).resolve(), *[(HERE / name).resolve() for name in PINS]]
    candidate = (resolved_parent / path.name).resolve()
    require(candidate not in protected, "output aliases protected input")
    if path.exists() or path.is_symlink():
        require(not path.is_symlink(), "output symlink")
        mode = path.stat().st_mode
        require(stat.S_ISREG(mode), "output must be regular file")
        for protected_path in protected:
            try:
                require(not os.path.samefile(path, protected_path), "output hardlinks protected input")
            except FileNotFoundError:
                pass


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    require(precision_bits >= 3072, "precision must be at least 3072 bits")
    ctx.prec = precision_bits
    documents = validate_frozen_chain()

    inherited_values = r121.load_inputs()
    seed = r121.locate_seed(inherited_values)
    exact_root_lower, exact_root_upper, _lower_sign, _upper_sign = (
        r121.isolate_anchor_root(seed)
    )
    family_root, t_guard = family_root_contract(
        seed, exact_root_lower, exact_root_upper,
    )
    family_root_id = family_root["family_root_id"]

    round121 = documents[121]["certificate"]["result"]
    round122 = documents[122]["certificate"]["result"]
    require(
        round121["exact_seed_contract"]["round117_operator_cell_id"]
        == r121.OPERATOR_CELL_ID,
        "Round121 operator crosswalk",
    )
    stage_contract, endpoint_rows, endpoint_face_ids = family_endpoint_rows(
        family_root_id, seed, t_guard, round121,
    )
    recut_rows, recut_ids = family_recut_rows(
        family_root_id, endpoint_face_ids, round121,
    )
    common_rows = family_common_rank_rows(
        family_root_id, endpoint_rows, recut_ids, round121,
    )

    # Replay Round122 on the full lambda over-enclosure and its independent s collar.
    round122_loaded = r122.load_round121()
    require(digest(round122_loaded) == digest(round121), "Round122 loader Round121 crosslink")
    physical_raw = r122.physical_empty_audit(seed, t_guard, round122_loaded)
    five_face_rows, seven_boundary_rows = r122.physical_grammar_rows(physical_raw)
    moving_raw = r122.moving_recut_faces(seed, t_guard, round122_loaded)
    stationary_raw = r122.outer_faces(round122_loaded)
    raw_traces, raw_incidences = r122.face_trace_and_incidence_rows(
        moving_raw, stationary_raw, round122_loaded,
    )
    require(
        len(moving_raw) == 23 and len(stationary_raw) == 2
        and len(raw_traces) == 48 and len(raw_incidences) == 24,
        "Round122 full lambda replay artificial census",
    )
    physical = transformed_physical_audit(
        family_root_id, common_rows, physical_raw,
    )
    artificial = family_artificial_face_registry(
        family_root_id, endpoint_face_ids, common_rows,
        moving_raw, stationary_raw,
    )
    base_rows, field_rows = base_and_field_templates(
        family_root_id, common_rows, recut_ids, artificial,
        round121, round122,
    )

    source_chain_pins = {
        f"Round{round_index}_certificate_result_sha256":
            documents[round_index]["certificate"]["result_sha256"]
        for round_index in range(120, 129)
    }
    verification_chain_pins = {
        f"Round{round_index}_verification_result_sha256":
            documents[round_index]["verification"]["result_sha256"]
        for round_index in range(120, 129)
    }
    result = {
        "precision_bits": precision_bits,
        "status": "CERTIFIED_POSITIVE_BOREL_RANK3_RECUT_FIELD_STRATUM__LOCAL_14_OF_18",
        "frozen_chain_contract": {
            "Round120_through_Round128_primary_file_pin_count": len(PINS),
            "all_primary_certificates_closed_and_verifications_PASS": True,
            "certificate_result_sha256_pins": source_chain_pins,
            "verification_result_sha256_pins": verification_chain_pins,
            "upstream_primary_file_byte_pins": dict(sorted(PINS.items())),
        },
        "positive_Borel_family_root_contract": family_root,
        "two_parameter_namespace_contract": {
            "lambda_parameter": "b3 coordinate indexing exact parent-W Borel fibres",
            "lambda_collar": [qstr(LAMBDA_LOWER), qstr(LAMBDA_UPPER)],
            "s_parameter": "horizontal displacement of every W obstacle center",
            "s_collar": [qstr(-S_EPSILON), qstr(S_EPSILON)],
            "lambda_is_not_s": True,
            "lambda_changes_the_parent_W_exact_b_locator": True,
            "s_changes_the_physical_system_geometry": True,
            "no_identifier_substitutes_one_parameter_for_the_other": True,
            "joint_scope": "exact lambda fibre times independent closed s collar",
        },
        "parameterized_actual_parent_W_registry": {
            "registry_type": (
                "standard-Borel exact-locator parameterized actual parent-W registry"
            ),
            "family_root_id": family_root_id,
            "exact_lambda_locator_contract": (
                "canonical nested rational-dyadic intervals with nonempty closure, "
                "diameters tending to zero, and value in the frozen lambda collar"
            ),
            "exact_b_locator_constructor": (
                "monotone analytic image of the exact lambda locator under b(lambda)"
            ),
            "typed_parent_W_payload": (
                "(round129-positive-borel-parent-W-v1,family-root-id,"
                "angular-lift-id,exact-b-locator)"
            ),
            "every_exact_lambda_emits_one_positive_length_source_cell": True,
            "finite_precision_or_decimal_text_in_actual_parent_W_ID": False,
            "whole_registry_is_uncountable_and_not_finitely_enumerated": True,
        },
        "uniform_stage_adapted_coordinate_contract": stage_contract,
        "uniform_pullback_face_guard_rows": endpoint_rows,
        "uniform_pullback_face_guard_rows_sha256": digest(endpoint_rows),
        "parameterized_stage_recut_template_rows": recut_rows,
        "parameterized_stage_recut_template_rows_sha256": digest(recut_rows),
        "parameterized_common_rank_template_rows": common_rows,
        "parameterized_common_rank_template_rows_sha256": digest(common_rows),
        "uniform_physical_face_empty_audit": physical,
        "physical_five_face_grammar_rows": five_face_rows,
        "physical_five_face_grammar_rows_sha256": digest(five_face_rows),
        "physical_seven_boundary_kind_rows": seven_boundary_rows,
        "physical_seven_boundary_kind_rows_sha256": digest(seven_boundary_rows),
        "parameterized_artificial_face_registry": artificial,
        "parameterized_base_key_template_rows": base_rows,
        "parameterized_base_key_template_rows_sha256": digest(base_rows),
        "parameterized_F1_F13_F16_slot_template_rows": field_rows,
        "parameterized_F1_F13_F16_slot_template_rows_sha256": digest(field_rows),
        "uniform_field_theorems": {
            "certified_field_indices": list(CERTIFIED_FIELDS),
            "certified_field_names": [
                FIELD_NAMES[index] for index in CERTIFIED_FIELDS
            ],
            "F5_one_step_adapted_inverse_strict_upper": qstr(r121.THETA),
            "F5_three_leg_path_product_strict_upper": qstr(r121.THREE_STEP_THETA),
            "F6_one_leg_canonical_curve_log_variation_strict_upper": qstr(
                r121.ONE_STEP_LOG_VARIATION
            ),
            "F6_three_leg_path_sum_strict_upper": qstr(
                r121.THREE_STEP_LOG_VARIATION
            ),
            "F6_scope_is_exactly_the_fixed_three_leg_record": True,
            "F6_arbitrary_return_depth_or_global_all_record_claim": False,
            "F11_full_phase_stage_strict_upper": {
                str(stage): qstr(bound)
                for stage, bound in sorted(r122.F11_BY_STAGE.items())
            },
            "F11_uses_full_phase_authoritative_rank_envelopes": True,
            "F11_along_curve_diagnostics_not_used_as_field_values": True,
            "F10_F13_F16_are_zero_only_because_complete_physical_face_family_is_empty":
                True,
            "artificial_recut_faces_are_retained_and_not_called_physical_faces": True,
        },
        "count_ledger": {
            "lambda_collar_is_non_degenerate": True,
            "exact_lambda_fibre_count": "UNCOUNTABLE_PARAMETERIZED_REGISTRY",
            "uniform_pullback_face_guard_row_count": 23,
            "finite_stage_recut_template_row_count": 26,
            "finite_common_rank_template_row_count": 24,
            "finite_base_key_template_row_count": 120,
            "finite_field_slot_template_row_count": 1680,
            "finite_template_count_per_certified_field": 120,
            "certified_field_count": 14,
            "per_exact_lambda_fibre_actual_parent_W_count": 1,
            "per_exact_lambda_fibre_actual_child_count": 24,
            "per_exact_lambda_fibre_actual_base_key_count": 120,
            "per_exact_lambda_fibre_actual_slot_count": 1680,
            "whole_family_actual_child_row_count": None,
            "whole_family_actual_slot_row_count": None,
            "whole_family_actual_rows_are_generated_only_after_exact_locator_input":
                True,
            "physical_core_clearance_template_row_count": 96,
            "physical_child_stage_template_row_count": 72,
            "physical_face_instance_count": 0,
            "artificial_face_template_count": 25,
            "artificial_trace_template_count": 48,
            "child_face_incidence_template_count": 24,
            "global_complete_18_field_block_count": 0,
        },
        "local_field_status": {
            **{
                f"F{index}": (
                    "CERTIFIED_ON_EVERY_EXACT_LAMBDA_FIBRE_AND_ALL_24_COMMON_RANKS"
                )
                for index in CERTIFIED_FIELDS
            },
            "F14": "NOT_INSTALLED_ON_POSITIVE_BOREL_FAMILY",
            "F15": "NOT_INSTALLED_ON_POSITIVE_BOREL_FAMILY",
            "F17": "NOT_INSTALLED_ON_POSITIVE_BOREL_FAMILY",
            "F18": "NOT_INSTALLED_ON_POSITIVE_BOREL_FAMILY",
        },
        "positive_Borel_family_local_field_maturity": "14/18",
        "gate5_global_maturity": "10/18",
        "gate5_status": "NOT_CERTIFIED",
        "complete_18_field_block_count": 0,
        "global_complete_18_field_block_count": 0,
        "gate5_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
        "strict_scope": (
            "one explicit positive-Borel b-image of the lambda=b3 collar inside "
            "one frozen Round112/Round113/Round117 rank-three root/operator cell; "
            "24 parameterized common ranks per exact lambda; independent "
            "|s|<=2^-512 physical collar; local F1-F13 and F16 only"
        ),
        "strict_nonclaims": [
            "the positive-Borel local family is not the global 441280-word registry",
            "no finite count is assigned to all actual fibres, children, or slots in the uncountable family",
            "the 1680 finite rows are slot templates; 1680 actual slots occur separately on each exact lambda fibre",
            "lambda=b3 is a Borel curve-family coordinate and is not the physical deformation parameter s",
            "F6 covers the fixed three-leg record only, not arbitrary return depth or a global all-record sum",
            "F11 uses full-phase rank envelopes but does not certify arbitrary global return words",
            "the physical-face family is empty on this collar; artificial recut faces remain present",
            "no nonempty F10 coarea, F13 physical current, or F16 physical flux contribution is claimed",
            "Round123-Round126 exact-seed F14/F15/F17/F18 are not copied onto this positive-Borel family",
            "no complete 18-field block, global Gate5 upgrade, Wiener claim, Kac closure, or CM2 claim",
        ],
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    args = parser.parse_args()
    safe_output_path(args.output)
    result = build(args.precision_bits)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    args.output.write_text(
        json.dumps(
            envelope, indent=2, sort_keys=True, ensure_ascii=False,
            allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.output}")
    print(f"result_sha256={envelope['result_sha256']}")
    print("POSITIVE_BOREL_LOCAL_FIELD_MATURITY=14/18")
    print("GLOBAL_GATE5=10/18")
    print("CM2=NO-GO_FOR_CLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
