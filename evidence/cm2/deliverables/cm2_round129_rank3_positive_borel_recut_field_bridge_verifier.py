#!/usr/bin/env python3
"""Independent verifier for the Round129 positive-Borel rank-three stratum.

This file never imports or executes the Round129 producer.  Its mathematical
core starts from frozen Round113/117/120/121 objects, verifies the full
``lambda=b3`` collar by interval arithmetic, and then feeds the resulting
theta over-enclosure through the already independent Round122 native Jet2
replay.  Thus the lambda sheet, the independent physical ``s`` collar, all
169 candidate checks, the five-face/seven-boundary empty audit, and the
twenty-three moving cut graphs are checked jointly without sharing Round129
producer code.

The certificate layer separately reconstructs all stable IDs and finite
template registries from pinned upstream certificates.  Re-signed semantic
mutations are tested without relaxing the official certificate byte pin.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
from collections import Counter, defaultdict
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_round113_rank3_root_sheet_owner_ordering_spike as round113
import cm2_round122_rank3_exact_seed_physical_face_field_bridge_verifier as v122
from cm2_round76_r2_numeric_fields_generator import aq, interval
from cm2_round79_tangency_intersection_generator import strict_sign


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = HERE / "cm2_round129_rank3_positive_borel_recut_field_bridge.py"
CERTIFICATE = (
    HERE
    / "cm2-round129-rank3-positive-borel-recut-field-bridge-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round129-rank3-positive-borel-recut-field-bridge-verification-2026-07-24.json"
)
CERTIFICATE_SCHEMA = "cm2.round129.rank3-positive-borel-recut-field-bridge.v1"
VERIFICATION_SCHEMA = (
    "cm2.round129.rank3-positive-borel-recut-field-bridge-verification.v1"
)
PRODUCER_SHA256 = (
    "bb0884aa14c256d16acd86c47ef1bf75e910507fa0b9334be704a6ee3995a054"
)
CERTIFICATE_SHA256 = (
    "1e2527ddb73158554ad238ff2f9f7fd6cb805f80d55bdafd770a8c9c1688d762"
)
CERTIFICATE_RESULT_SHA256 = (
    "79cb3501fd7d52d1a22fecf3dc0faaa979dfd9b06fea7ce7afd872b39fbf2bd5"
)
VERIFIER_PRECISION_BITS = 4096

LAMBDA_CENTER = Q(3, 65536)
LAMBDA_EPSILON = Q(1, 2**512)
LAMBDA_LOWER = LAMBDA_CENTER - LAMBDA_EPSILON
LAMBDA_UPPER = LAMBDA_CENTER + LAMBDA_EPSILON
LAMBDA_LENGTH = 2 * LAMBDA_EPSILON
FIXED_C0 = Q(1, 16384)
T_GUARD_PADDING = Q(1, 2**520)
S_EPSILON = Q(1, 2**512)
DELTA = Q(1, 10**90)
CERTIFIED_FIELDS = tuple(range(1, 14)) + (16,)
EXPECTED_CUT_ORDER = (
    (2, 1), (2, 2), (1, 1), (2, 3), (2, 4), (2, 5),
    (1, 2), (2, 6), (2, 7), (1, 3), (2, 8), (2, 9),
    (2, 10), (1, 4), (2, 11), (2, 12), (1, 5), (2, 13),
    (2, 14), (2, 15), (1, 6), (2, 16), (2, 17),
)
OFFICIAL_WORDS = (
    "gate5-word:102441:3ef7afa1895a984d7edeab7005cfcb7daed7ae8aa07f0767bdd9144da94749ba",
    "gate5-word:346720:53f03ff6fc716b0187c62b5e3cc7971c9e030686426d13ff5eee585f33daeb3e",
    "gate5-word:180256:564ba69e20fe29980fb28d97a50efa2326d024c92c36c930bdb4a2157c3335c8",
)
SEED_SHEET_ID = (
    "round112-bypass-sheet:"
    "82388860fd9a24f85561682533f70ba8789125b13ea29deb027aa3bcb293201f"
)
ROOF_COUNTS = (2, 1, 2)
STAGE_ORIENTATIONS = (1, -1, 1)
FIELD_NAMES = {
    1: "nonempty_or_empty_domain_proof",
    2: "physical_homogeneity_subbranch_table",
    3: "homogeneous_prefix_chart",
    4: "homogeneous_suffix_chart",
    5: "inverse_Jacobian_bound",
    6: "log_Jacobian_distortion_sum",
    7: "one_step_cut_growth_Z_sum",
    8: "face_transversality_lower",
    9: "face_C2_atlas_bound",
    10: "coarea_density_regular_bound",
    11: "dynamic_Holder_test_pullback_bound",
    12: "C1_face_trace_pullback_bound",
    13: "moving_boundary_DQ_current_and_two_traces",
    16: "flux_face_operator_cost",
}

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

UPSTREAM_PINS = {
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

MATH_HELPER_PINS = {
    "cm2_gate25_physical_return_core_registry_cert.py":
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate34_round26_q1_time2_frontier_cert.py":
        "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py":
        "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f",
    "cm2_round113_rank3_root_sheet_owner_ordering_spike.py":
        "2263d213bad42163da326c892662f500f29a3c5f6cf4b8ba28cc2bb57990b11e",
    "cm2_round76_r2_numeric_fields_generator.py":
        "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
    "cm2_round79_tangency_intersection_generator.py":
        "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
}


class VerificationError(RuntimeError):
    """A fail-closed verification error."""


def require(condition: Any, label: str) -> None:
    if not bool(condition):
        raise VerificationError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q | int) -> str:
    value = Q(value)
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str and key not in result, f"duplicate key:{key}")
        result[key] = value
    return result


def reject_number(token: str) -> Any:
    raise VerificationError(f"forbidden JSON number:{token}")


def strict_integer(token: str) -> int:
    require(token != "-0", "negative zero")
    require(len(token.lstrip("-")) <= 18, "oversized integer token")
    value = int(token)
    require(abs(value) <= 2**63 - 1, "integer outside int64")
    return value


def reject_surrogates(value: Any) -> None:
    if type(value) is str:
        require(
            not any(0xD800 <= ord(character) <= 0xDFFF for character in value),
            "unpaired surrogate",
        )
    elif type(value) is list:
        for item in value:
            reject_surrogates(item)
    elif type(value) is dict:
        for key, item in value.items():
            reject_surrogates(key)
            reject_surrogates(item)


def parse_bytes(raw: bytes, *, certificate_mode: bool = True) -> Any:
    require(not raw.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM")
    kwargs: dict[str, Any] = {
        "object_pairs_hook": strict_pairs,
        "parse_constant": reject_number,
        "parse_int": strict_integer if certificate_mode else int,
    }
    if certificate_mode:
        kwargs["parse_float"] = reject_number
    value = json.loads(raw.decode("utf-8", errors="strict"), **kwargs)
    reject_surrogates(value)
    return value


def closed_document(path: Path, schema: str | None = None) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), f"regular input:{path.name}")
    value = parse_bytes(path.read_bytes())
    require(type(value) is dict, f"top object:{path.name}")
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"closed envelope:{path.name}",
    )
    require(type(value["schema"]) is str, f"schema type:{path.name}")
    if schema is not None:
        require(value["schema"] == schema, f"schema:{path.name}")
    require(type(value["result"]) is dict, f"result object:{path.name}")
    require(
        value["result_sha256"] == digest(value["result"]),
        f"result digest:{path.name}",
    )
    return value


def qvalue(value: Any, label: str) -> Q:
    require(type(value) is str, f"rational string:{label}")
    require(
        value == "0"
        or value == qstr(Q(value))
        and not value.startswith("+"),
        f"canonical rational:{label}",
    )
    return Q(value)


def qinterval(value: Any, label: str) -> tuple[Q, Q]:
    require(type(value) is list and len(value) == 2, f"interval:{label}")
    lower, upper = qvalue(value[0], f"{label}.lower"), qvalue(
        value[1], f"{label}.upper"
    )
    require(lower <= upper, f"ordered interval:{label}")
    return lower, upper


def arb_pair(value: arb) -> tuple[Q, Q]:
    def exact_dyadic(point: arb) -> Q:
        mantissa, exponent = point.man_exp()
        return Q(int(mantissa)) * Q(2) ** int(exponent)

    return exact_dyadic(value.lower()), exact_dyadic(value.upper())


def interval_contains(stored: Any, actual: arb, label: str) -> None:
    lower, upper = qinterval(stored, label)
    actual_lower, actual_upper = arb_pair(actual)
    require(
        lower <= actual_lower <= actual_upper <= upper,
        f"stored interval contains independent replay:{label}",
    )


def interval_overlaps(stored: Any, actual: arb, label: str) -> None:
    lower, upper = qinterval(stored, label)
    actual_lower, actual_upper = arb_pair(actual)
    require(
        lower <= actual_upper and actual_lower <= upper,
        f"stored interval overlaps independent replay:{label}",
    )


def row_digest(row: dict[str, Any], label: str) -> None:
    require(type(row) is dict, f"row object:{label}")
    require(type(row.get("row_sha256")) is str, f"row digest type:{label}")
    payload = dict(row)
    stored = payload.pop("row_sha256")
    require(stored == digest(payload), f"row digest:{label}")


def require_exact(value: Any, expected: Any, label: str) -> None:
    require(value == expected, label)


def validate_pins() -> dict[int, dict[str, dict[str, Any]]]:
    require(
        PRODUCER.is_file() and not PRODUCER.is_symlink(),
        "producer regular file",
    )
    require(sha256(PRODUCER) == PRODUCER_SHA256, "producer byte pin")
    for name, expected in {**UPSTREAM_PINS, **MATH_HELPER_PINS}.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pin target:{name}")
        require(path.resolve().parent == HERE, f"pin parent:{name}")
        require(sha256(path) == expected, f"pin mismatch:{name}")

    documents: dict[int, dict[str, dict[str, Any]]] = {}
    for round_index, (certificate_name, verification_name) in sorted(
        CERTIFICATE_FILES.items()
    ):
        certificate = closed_document(HERE / certificate_name)
        verification = closed_document(HERE / verification_name)
        verdict = (
            verification["result"].get("verdict")
            or verification["result"].get("status")
        )
        require(verdict == "PASS", f"Round{round_index} verification PASS")
        documents[round_index] = {
            "certificate": certificate,
            "verification": verification,
        }
    for round_index in range(120, 127):
        result = documents[round_index]["certificate"]["result"]
        require(result["gate5_global_maturity"] == "10/18", "upstream Gate5")
        require(result["complete_18_field_block_count"] == 0, "upstream blocks")
        require(result["cm2_verdict"] == "NO-GO_FOR_CLAIM", "upstream CM2")
    safety127 = documents[127]["certificate"]["result"]["global_safety_state"]
    require(safety127["gate5_global_maturity"] == "10/18", "Round127 Gate5")
    require(
        safety127["global_complete_18_field_block_count"] == 0,
        "Round127 blocks",
    )
    require(safety127["cm2_verdict"] == "NO-GO_FOR_CLAIM", "Round127 CM2")
    safety128 = documents[128]["certificate"]["result"][
        "D_global_safety_and_nonpromotion"
    ]
    require(safety128["gate5_global_maturity"] == "10/18", "Round128 Gate5")
    require(
        safety128["global_complete_18_field_block_count"] == 0,
        "Round128 blocks",
    )
    require(safety128["CM2"] == "NO-GO_FOR_CLAIM", "Round128 CM2")
    require(
        safety128["global_exact_nonempty_candidate_key_count"] is None,
        "Round128 null global census",
    )
    return documents


def replay_family_faces(
    theta_guard: arb,
    round121: dict[str, Any],
) -> list[dict[str, Any]]:
    """Check the frozen 2^-200 guards without correlation-destroying overbisect.

    The lambda t-tube is far narrower than the recut signal at the frozen
    Round121 guard scale, but it is wider than the signal created by another
    184 unnecessary bisections.  Evaluating the already frozen guards is the
    correct uniform graph test.
    """
    upstream = {
        (row["stage"], row["natural_index_j"]): row
        for row in round121["pullback_endpoint_rows"]
    }
    rows: list[dict[str, Any]] = []
    for stage, natural_index in EXPECTED_CUT_ORDER:
        lower, upper = map(
            Q, upstream[(stage, natural_index)]["x_dyadic_bracket"]
        )
        left = v122.face_jet(
            theta_guard, stage, natural_index, lower, lower
        )
        right = v122.face_jet(
            theta_guard, stage, natural_index, upper, upper
        )
        require(bool(left.value < 0) and bool(right.value > 0),
                f"uniform lambda face signs:S{stage}:{natural_index}")
        jet = v122.face_jet(
            theta_guard, stage, natural_index, lower, upper
        )
        normalized_lower = Q(5) if stage == 1 else Q(16)
        require(
            bool(jet.x / aq(DELTA) > aq(normalized_lower)),
            f"uniform face derivative:S{stage}:{natural_index}",
        )
        root_s = -jet.s / jet.x
        root_ss = -(
            jet.ss + 2 * jet.xs * root_s + jet.xx * root_s * root_s
        ) / jet.x
        first_claim = Q(4) if stage == 1 else Q(13)
        second_claim = Q(56) if stage == 1 else Q(616)
        require(
            v122.upper_abs(root_s) < first_claim,
            f"uniform implicit s derivative:S{stage}:{natural_index}",
        )
        require(
            v122.upper_abs(root_ss) < second_claim,
            f"uniform implicit ss derivative:S{stage}:{natural_index}",
        )
        rows.append({
            "stage": stage,
            "natural_index_j": natural_index,
            "guard": [qstr(lower), qstr(upper)],
            "face_signs": [-1, 1],
            "normalized_Fx_lower": qstr(normalized_lower),
            "implicit_s_upper": qstr(v122.upper_abs(root_s)),
            "implicit_ss_upper": qstr(v122.upper_abs(root_ss)),
        })
    rows.sort(key=lambda row: Q(row["guard"][0]))
    require(
        tuple((row["stage"], row["natural_index_j"]) for row in rows)
        == EXPECTED_CUT_ORDER,
        "independent family face order",
    )
    return rows


def independent_math_core(
    documents: dict[int, dict[str, dict[str, Any]]],
) -> dict[str, Any]:
    """Rebuild the lambda sheet and joint lambda-by-s geometry."""
    ctx.prec = VERIFIER_PRECISION_BITS
    values = v122.load_inputs()
    indexes = v122.seed_indexes(values)
    round121 = documents[121]["certificate"]["result"]
    witness = round121["exact_parent_W_witness_rows"][0]
    anchor_lower, anchor_upper = map(
        Q, witness["anchor_t_unique_root_dyadic_bracket"]
    )
    require(anchor_lower < anchor_upper, "anchor root bracket")
    source = replace(
        core_cert.physical_cores()[v122.SEED_BRANCH[0]],
        chart_id=v122.SEED_SOURCE_CHART,
    )

    def equation(t: Q, lambda_lower: Q, lambda_upper: Q) -> arb:
        return round113.equation_value(
            source,
            v122.SEED_BRANCH,
            1,
            "BYPASS",
            t,
            FIXED_C0,
            FIXED_C0,
            lambda_lower,
            lambda_upper,
        )

    require(
        (strict_sign(equation(anchor_lower, LAMBDA_CENTER, LAMBDA_CENTER)),
         strict_sign(equation(anchor_upper, LAMBDA_CENTER, LAMBDA_CENTER)))
        == (1, -1),
        "independent anchor signs",
    )
    t_lower = anchor_lower - T_GUARD_PADDING
    t_upper = anchor_upper + T_GUARD_PADDING
    face_signs = (
        strict_sign(equation(t_lower, LAMBDA_LOWER, LAMBDA_UPPER)),
        strict_sign(equation(t_upper, LAMBDA_LOWER, LAMBDA_UPPER)),
    )
    require(face_signs == (1, -1), "uniform lambda root face signs")

    geometry = round113.path_geometry(
        source,
        v122.SEED_BRANCH,
        1,
        "BYPASS",
        t_lower,
        t_upper,
        FIXED_C0,
        FIXED_C0,
        LAMBDA_LOWER,
        LAMBDA_UPPER,
    )
    partial_t = geometry["equation"].gradient[0]
    partial_lambda = geometry["equation"].gradient[2]
    ft_lower, ft_upper = arb_pair(partial_t)
    fl_lower, fl_upper = arb_pair(partial_lambda)
    require(-8 < ft_lower <= ft_upper < -7, "-8<F_t<-7")
    require(
        Q(1, 500000) < fl_lower <= fl_upper < Q(3, 1000000),
        "2e-6<F_lambda<3e-6",
    )
    # The BYPASS square term is (4/25)^2 lambda^2, so this is an
    # independent symbolic derivative cross-check, not just a Jet readout.
    symbolic_fl = interval(
        Q(32, 625) * LAMBDA_LOWER,
        Q(32, 625) * LAMBDA_UPPER,
    )
    symbolic_lower, symbolic_upper = arb_pair(symbolic_fl)
    require(
        fl_lower <= symbolic_lower <= symbolic_upper <= fl_upper,
        "symbolic F_lambda in Jet enclosure",
    )

    dt_dlambda = -partial_lambda / partial_t
    dt_lower, dt_upper = arb_pair(dt_dlambda)
    require(
        Q(1, 4000000) < dt_lower <= dt_upper < Q(1, 3000000),
        "implicit dt/dlambda",
    )
    t_ball = interval(t_lower, t_upper)
    db_dlambda = aq(Q(36, 25)) * dt_dlambda / (
        arb(1) - t_ball * t_ball
    ).sqrt()
    db_lower, db_upper = arb_pair(db_dlambda)
    require(
        Q(1, 2250000) < db_lower <= db_upper < Q(1, 2000000),
        "db/dlambda",
    )
    b_image_lower = LAMBDA_LENGTH * Q(1, 2250000)
    require(b_image_lower > 0, "positive Borel image length")

    theta_guard = arb.pi() - t_ball.asin()
    # v122 is a separately frozen verifier, not the Round129 producer.
    candidate_rows = v122.replay_candidates(theta_guard, indexes)
    physical = v122.replay_physical_boundaries(theta_guard, candidate_rows)
    faces = replay_family_faces(theta_guard, round121)
    require(
        tuple(
            (row["stage"], row["natural_index_j"]) for row in faces
        ) == EXPECTED_CUT_ORDER,
        "independent 23-face order",
    )
    boundaries: list[tuple[Q, Q]] = [(Q(0), Q(0))]
    boundaries.extend(
        (
            Q(row["guard"][0]),
            Q(row["guard"][1]),
        )
        for row in faces
    )
    boundaries.append((Q(1), Q(1)))
    gaps = [
        right[0] - left[1]
        for left, right in zip(boundaries, boundaries[1:])
    ]
    require(len(gaps) == 24 and min(gaps) > Q(1, 200), "24 positive gaps")

    # Independent U1/U2 length and derivative replay on the full t guard.
    zero = v122.source_and_collisions(
        theta_guard, v122.Jet2(arb(0)), v122.Jet2(arb(0))
    )
    one = v122.source_and_collisions(
        theta_guard, v122.Jet2(arb(1)), v122.Jet2(arb(0))
    )
    whole = v122.source_and_collisions(
        theta_guard,
        v122.Jet2(interval(Q(0), Q(1)), x=arb(1)),
        v122.Jet2(arb(0)),
    )
    length1 = (zero["a1"].value - one["a1"].value) / aq(DELTA)
    length2 = (one["a2"].value - zero["a2"].value) / aq(DELTA)
    derivative1 = -whole["a1"].x / aq(DELTA)
    derivative2 = whole["a2"].x / aq(DELTA)
    require(bool(length1 > aq(Q(34, 5))) and bool(length1 < 7), "U1 length")
    require(bool(length2 > aq(Q(87, 5))) and bool(length2 < 18), "U2 length")
    require(bool(derivative1 > 6) and bool(derivative1 < 7), "U1 derivative")
    require(bool(derivative2 > 17) and bool(derivative2 < 18), "U2 derivative")

    return {
        "anchor_bracket": [qstr(anchor_lower), qstr(anchor_upper)],
        "t_guard": [qstr(t_lower), qstr(t_upper)],
        "face_signs": list(face_signs),
        "partial_t": partial_t,
        "partial_lambda": partial_lambda,
        "dt_dlambda": dt_dlambda,
        "db_dlambda": db_dlambda,
        "b_image_length_lower": qstr(b_image_lower),
        "theta_guard": theta_guard,
        "candidate_rows": candidate_rows,
        "physical": physical,
        "faces": faces,
        "minimum_gap": qstr(min(gaps)),
        "length1": length1,
        "length2": length2,
        "derivative1": derivative1,
        "derivative2": derivative2,
    }


RESULT_KEYS = set(
    """precision_bits status frozen_chain_contract
    positive_Borel_family_root_contract two_parameter_namespace_contract
    parameterized_actual_parent_W_registry
    uniform_stage_adapted_coordinate_contract uniform_pullback_face_guard_rows
    uniform_pullback_face_guard_rows_sha256
    parameterized_stage_recut_template_rows
    parameterized_stage_recut_template_rows_sha256
    parameterized_common_rank_template_rows
    parameterized_common_rank_template_rows_sha256
    uniform_physical_face_empty_audit physical_five_face_grammar_rows
    physical_five_face_grammar_rows_sha256
    physical_seven_boundary_kind_rows
    physical_seven_boundary_kind_rows_sha256
    parameterized_artificial_face_registry
    parameterized_base_key_template_rows
    parameterized_base_key_template_rows_sha256
    parameterized_F1_F13_F16_slot_template_rows
    parameterized_F1_F13_F16_slot_template_rows_sha256
    uniform_field_theorems count_ledger local_field_status
    positive_Borel_family_local_field_maturity gate5_global_maturity
    gate5_status complete_18_field_block_count
    global_complete_18_field_block_count gate5_block_count cm2_verdict
    strict_scope strict_nonclaims""".split()
)
ROOT_KEYS = set(
    """family_root_id round112_sheet_id round113_parent_id
    round117_operator_cell_id angular_lift_id sheet_kind branch_key fixed_c0
    lambda_coordinate lambda_exact_dyadic_closed_collar lambda_center
    lambda_epsilon lambda_interval_length_exact
    lambda_collar_inside_one_Round113_parent_and_Round117_operator_cell
    exact_Round121_anchor_root_bracket uniform_t_guard_padding uniform_t_guard
    uniform_t_guard_face_signs uniform_F_t_enclosure
    uniform_F_lambda_enclosure uniform_simple_F_t_bounds
    uniform_simple_F_lambda_bounds implicit_dt_dlambda_enclosure
    implicit_dt_dlambda_strict_bounds b_of_lambda_definition
    db_dlambda_enclosure db_dlambda_strict_bounds
    b_of_lambda_strictly_increasing b_image_length_MVT_formula
    b_image_length_strict_lower_exact
    b_image_is_a_non_degenerate_positive_Borel_interval
    analytic_IFT_root_sheet_used
    finite_precision_enclosure_text_participates_in_family_ID""".split()
)
ENDPOINT_KEYS = set(
    """face_template_id family_root_id stage natural_index_j
    exact_level_equation Round121_guard_endpoint_id uniform_x_dyadic_guard
    uniform_guard_exactly_equals_Round121_guard guard_width
    all_lambda_left_function_sign all_lambda_right_function_sign
    all_lambda_normalized_U_x_strict_lower U_x_sign
    unique_root_for_every_exact_lambda unique_analytic_lambda_graph_by_IFT
    family_actual_endpoint_id_constructor
    exact_lambda_locator_required_for_actual_endpoint_ID
    numeric_guard_text_participates_in_actual_endpoint_ID row_sha256""".split()
)
RECUT_KEYS = set(
    """recut_template_id family_root_id stage natural_index_j
    lower_face_template_id upper_face_template_id orientation
    adapted_coordinate_id adapted_lower adapted_upper adapted_length_upper
    normalized_adapted_length_strict_lower roof_level_count
    official_word_key_id lower_closed upper_closed
    source_parent_right_endpoint_is_open
    internal_cut_owned_by_right_natural_cell
    actual_materialized_input_recut_for_every_exact_lambda
    family_actual_recut_id_constructor
    exact_lambda_locator_required_for_actual_recut_ID
    finite_template_is_not_one_actual_fibre_recut row_sha256""".split()
)
COMMON_KEYS = set(
    """common_rank_template_id family_root_id common_rank
    lower_face_template_id upper_face_template_id
    positive_source_x_length_strict_lower_exact
    positive_source_x_length_exceeds_1_over_200 covering_stage_indices
    source_recut_template_id first_image_recut_template_id
    second_image_recut_template_id round117_operator_cell_id official_path_id
    typed_parent_W_id_constructor refined_homogeneous_subbranch_id_constructor
    actual_child_id_constructor exact_lambda_and_derived_exact_b_locators_required
    actual_standard_curve_child_exists_for_every_exact_lambda
    finite_common_rank_template_is_not_one_actual_fibre_child row_sha256""".split()
)


def expected_family_root_id(round121: dict[str, Any]) -> str:
    contract = round121["exact_seed_contract"]
    payload = [
        "round129-positive-borel-family-root-v1",
        SEED_SHEET_ID,
        contract["round113_parent_id"],
        contract["round117_operator_cell_id"],
        contract["angular_lift_id"],
        qstr(FIXED_C0),
        qstr(LAMBDA_LOWER),
        qstr(LAMBDA_UPPER),
    ]
    return "round129-positive-borel-family-root:" + digest(payload)


def validate_root_namespace(
    result: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
    core: dict[str, Any],
) -> str:
    round121 = documents[121]["certificate"]["result"]
    upstream_contract = round121["exact_seed_contract"]
    root = result["positive_Borel_family_root_contract"]
    require(type(root) is dict and set(root) == ROOT_KEYS, "root closed schema")
    family_root_id = expected_family_root_id(round121)
    require(root["family_root_id"] == family_root_id, "family root ID")
    exact = {
        "round112_sheet_id": SEED_SHEET_ID,
        "round113_parent_id": upstream_contract["round113_parent_id"],
        "round117_operator_cell_id": upstream_contract["round117_operator_cell_id"],
        "angular_lift_id": upstream_contract["angular_lift_id"],
        "sheet_kind": "BYPASS",
        "branch_key": [7, "G[0,0]", "W[-1,-2]", 1],
        "fixed_c0": qstr(FIXED_C0),
        "lambda_coordinate": "b3",
        "lambda_exact_dyadic_closed_collar": [
            qstr(LAMBDA_LOWER), qstr(LAMBDA_UPPER)
        ],
        "lambda_center": qstr(LAMBDA_CENTER),
        "lambda_epsilon": qstr(LAMBDA_EPSILON),
        "lambda_interval_length_exact": qstr(LAMBDA_LENGTH),
        "lambda_collar_inside_one_Round113_parent_and_Round117_operator_cell": True,
        "exact_Round121_anchor_root_bracket": core["anchor_bracket"],
        "uniform_t_guard_padding": qstr(T_GUARD_PADDING),
        "uniform_t_guard": core["t_guard"],
        "uniform_t_guard_face_signs": [1, -1],
        "uniform_simple_F_t_bounds": "-8<F_t<-7",
        "uniform_simple_F_lambda_bounds": "1/500000<F_lambda<3/1000000",
        "implicit_dt_dlambda_strict_bounds":
            "1/4000000<dt/dlambda<1/3000000",
        "b_of_lambda_definition":
            "b(lambda)=acos(1/16384)-(36/25)*(pi-asin(t(lambda)))",
        "db_dlambda_strict_bounds":
            "1/2250000<db/dlambda<1/2000000",
        "b_of_lambda_strictly_increasing": True,
        "b_image_length_MVT_formula":
            "(lambda_upper-lambda_lower)*inf(db/dlambda)",
        "b_image_length_strict_lower_exact": core["b_image_length_lower"],
        "b_image_is_a_non_degenerate_positive_Borel_interval": True,
        "analytic_IFT_root_sheet_used": True,
        "finite_precision_enclosure_text_participates_in_family_ID": False,
    }
    for key, value in exact.items():
        require(root[key] == value, f"root contract:{key}")
    interval_contains(root["uniform_F_t_enclosure"], core["partial_t"], "F_t")
    interval_contains(
        root["uniform_F_lambda_enclosure"],
        core["partial_lambda"],
        "F_lambda",
    )
    interval_contains(
        root["implicit_dt_dlambda_enclosure"],
        core["dt_dlambda"],
        "dt/dlambda",
    )
    interval_overlaps(root["db_dlambda_enclosure"], core["db_dlambda"], "db/dlambda")
    require(LAMBDA_LOWER > Q(1, 32768), "lambda lower in parent")
    require(LAMBDA_UPPER < Q(1, 16384), "lambda upper in parent")

    namespace = result["two_parameter_namespace_contract"]
    require_exact(
        namespace,
        {
            "lambda_parameter":
                "b3 coordinate indexing exact parent-W Borel fibres",
            "lambda_collar": [qstr(LAMBDA_LOWER), qstr(LAMBDA_UPPER)],
            "s_parameter": "horizontal displacement of every W obstacle center",
            "s_collar": [qstr(-S_EPSILON), qstr(S_EPSILON)],
            "lambda_is_not_s": True,
            "lambda_changes_the_parent_W_exact_b_locator": True,
            "s_changes_the_physical_system_geometry": True,
            "no_identifier_substitutes_one_parameter_for_the_other": True,
            "joint_scope": "exact lambda fibre times independent closed s collar",
        },
        "two-parameter namespace",
    )
    registry = result["parameterized_actual_parent_W_registry"]
    require(type(registry) is dict and registry["family_root_id"] == family_root_id,
            "parent-W registry root")
    require(registry["whole_registry_is_uncountable_and_not_finitely_enumerated"] is True,
            "uncountable registry")
    require(registry["finite_precision_or_decimal_text_in_actual_parent_W_ID"] is False,
            "stable parent-W ID")
    require(registry["every_exact_lambda_emits_one_positive_length_source_cell"] is True,
            "one parent-W per exact lambda")
    return family_root_id


def validate_endpoints_recuts_common(
    result: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
    core: dict[str, Any],
    family_root_id: str,
) -> tuple[
    list[dict[str, Any]],
    dict[tuple[int, int], str],
    list[dict[str, Any]],
]:
    round121 = documents[121]["certificate"]["result"]
    stage = result["uniform_stage_adapted_coordinate_contract"]
    require(type(stage) is dict, "stage contract object")
    interval_overlaps(
        stage["U1_length_over_delta_enclosure"], core["length1"], "U1 length"
    )
    interval_overlaps(
        stage["U2_length_over_delta_enclosure"], core["length2"], "U2 length"
    )
    interval_overlaps(
        stage["U1_prime_over_delta_enclosure"], core["derivative1"], "U1 prime"
    )
    interval_overlaps(
        stage["U2_prime_over_delta_enclosure"], core["derivative2"], "U2 prime"
    )
    require(stage["source_adapted_coordinate"] == "u0(lambda,x)=10^-90*x",
            "source adapted coordinate")
    require(stage["stage_orientations"] == [1, -1, 1], "stage orientations")
    require(stage["uniform_natural_cell_counts"] == [1, 7, 18], "cell counts")
    require(stage["uniform_internal_cut_counts"] == [0, 6, 17], "cut counts")
    require(stage["uniform_pullback_cut_count"] == 23, "23 cuts")
    require(stage["uniform_common_rank_count"] == 24, "24 ranks")
    require(
        stage["uniform_cut_order"]
        == [f"S{s}:{j}" for s, j in EXPECTED_CUT_ORDER],
        "stage cut order",
    )
    require(stage["whole_lambda_collar_same_Round113_owner_path_and_Round117_homogeneity"]
            is True, "uniform owner/operator path")

    upstream_endpoints = {
        (row["stage"], row["natural_index_j"]): row
        for row in round121["pullback_endpoint_rows"]
    }
    endpoints = result["uniform_pullback_face_guard_rows"]
    require(type(endpoints) is list and len(endpoints) == 23, "endpoint census")
    require(
        result["uniform_pullback_face_guard_rows_sha256"] == digest(endpoints),
        "endpoint list digest",
    )
    face_ids: dict[tuple[int, int], str] = {}
    for index, row in enumerate(endpoints):
        require(type(row) is dict and set(row) == ENDPOINT_KEYS,
                f"endpoint schema:{index}")
        row_digest(row, f"endpoint:{index}")
        key = (row["stage"], row["natural_index_j"])
        require(key in upstream_endpoints and key not in face_ids,
                f"endpoint key:{key}")
        inherited = upstream_endpoints[key]
        face_id = "round129-uniform-pullback-face-template:" + digest([
            "round129-uniform-pullback-face-template-v1",
            family_root_id,
            key[0],
            key[1],
        ])
        face_ids[key] = face_id
        require(row["face_template_id"] == face_id, f"endpoint ID:{key}")
        require(row["family_root_id"] == family_root_id, f"endpoint root:{key}")
        require(
            row["Round121_guard_endpoint_id"] == inherited["endpoint_id"],
            f"endpoint upstream ID:{key}",
        )
        require(
            row["uniform_x_dyadic_guard"] == inherited["x_dyadic_bracket"],
            f"endpoint frozen guard:{key}",
        )
        require(
            qvalue(row["guard_width"], f"guard width:{key}")
            == Q(1, 2**200),
            f"endpoint guard width:{key}",
        )
        require(
            row["exact_level_equation"] == f"U{key[0]}(lambda,x)={key[1]}*10^-90",
            f"endpoint equation:{key}",
        )
        require(
            row["all_lambda_left_function_sign"] == -1
            and row["all_lambda_right_function_sign"] == 1
            and row["U_x_sign"] == 1,
            f"endpoint signs:{key}",
        )
        require(
            qvalue(row["all_lambda_normalized_U_x_strict_lower"],
                   f"endpoint derivative:{key}")
            == (Q(6) if key[0] == 1 else Q(17)),
            f"endpoint derivative bound:{key}",
        )
        for flag in (
            "uniform_guard_exactly_equals_Round121_guard",
            "unique_root_for_every_exact_lambda",
            "unique_analytic_lambda_graph_by_IFT",
            "exact_lambda_locator_required_for_actual_endpoint_ID",
        ):
            require(row[flag] is True, f"endpoint flag:{flag}:{key}")
        require(
            row["numeric_guard_text_participates_in_actual_endpoint_ID"] is False,
            f"endpoint stable ID:{key}",
        )
    require(
        tuple((row["stage"], row["natural_index_j"]) for row in endpoints)
        == EXPECTED_CUT_ORDER,
        "certificate endpoint order",
    )
    boundaries = [
        ("round129-family-source-outer-left", Q(0), Q(0)),
        *[
            (
                row["face_template_id"],
                Q(row["uniform_x_dyadic_guard"][0]),
                Q(row["uniform_x_dyadic_guard"][1]),
            )
            for row in endpoints
        ],
        ("round129-family-source-outer-right", Q(1), Q(1)),
    ]
    gaps = [
        right[1] - left[2] for left, right in zip(boundaries, boundaries[1:])
    ]
    require(len(gaps) == 24 and min(gaps) > Q(1, 200), "certificate child gaps")
    require(
        stage["minimum_24_child_x_length_strict_lower_exact"] == qstr(min(gaps))
        and stage["minimum_24_child_x_length_exceeds_1_over_200"] is True,
        "stage minimum gap",
    )

    inherited_recuts = {
        (row["stage"], row["natural_index_j"]): row
        for row in round121["stage_recut_rows"]
    }
    recuts = result["parameterized_stage_recut_template_rows"]
    require(type(recuts) is list and len(recuts) == 26, "recut census")
    require(
        result["parameterized_stage_recut_template_rows_sha256"] == digest(recuts),
        "recut list digest",
    )
    recut_ids: dict[tuple[int, int], str] = {}
    for index, row in enumerate(recuts):
        require(type(row) is dict and set(row) == RECUT_KEYS,
                f"recut schema:{index}")
        row_digest(row, f"recut:{index}")
        key = (row["stage"], row["natural_index_j"])
        require(key in inherited_recuts and key not in recut_ids, f"recut key:{key}")
        inherited = inherited_recuts[key]
        template_id = "round129-recut-template:" + digest([
            "round129-family-recut-template-v1",
            family_root_id,
            key[0],
            key[1],
        ])
        recut_ids[key] = template_id
        count = (1, 7, 18)[key[0]]
        expected = {
            "recut_template_id": template_id,
            "family_root_id": family_root_id,
            "stage": key[0],
            "natural_index_j": key[1],
            "lower_face_template_id": (
                "round129-family-source-outer-left"
                if key[1] == 0 else face_ids[(key[0], key[1])]
            ),
            "upper_face_template_id": (
                "round129-family-source-outer-right"
                if key[1] == count - 1 else face_ids[(key[0], key[1] + 1)]
            ),
            "orientation": STAGE_ORIENTATIONS[key[0]],
            **{
                name: inherited[name]
                for name in (
                    "adapted_coordinate_id", "adapted_lower", "adapted_upper",
                    "adapted_length_upper",
                    "normalized_adapted_length_strict_lower",
                    "roof_level_count", "official_word_key_id", "lower_closed",
                    "upper_closed", "source_parent_right_endpoint_is_open",
                    "internal_cut_owned_by_right_natural_cell",
                )
            },
            "actual_materialized_input_recut_for_every_exact_lambda": True,
            "family_actual_recut_id_constructor":
                "round129-recut:sha256(canonical([recut-template-id,"
                "exact-lambda-locator]))",
            "exact_lambda_locator_required_for_actual_recut_ID": True,
            "finite_template_is_not_one_actual_fibre_recut": True,
        }
        expected["row_sha256"] = digest(expected)
        require(row == expected, f"recut exact rebuild:{key}")

    common = result["parameterized_common_rank_template_rows"]
    require(type(common) is list and len(common) == 24, "common census")
    require(
        result["parameterized_common_rank_template_rows_sha256"] == digest(common),
        "common list digest",
    )
    inherited_common = sorted(
        round121["common_refinement_rows"], key=lambda row: row["common_rank"]
    )
    stage_indices = [0, 0, 0]
    for rank, row in enumerate(common):
        require(type(row) is dict and set(row) == COMMON_KEYS,
                f"common schema:{rank}")
        row_digest(row, f"common:{rank}")
        lower, upper = boundaries[rank], boundaries[rank + 1]
        gap = upper[1] - lower[2]
        require(inherited_common[rank]["covering_stage_indices"] == stage_indices,
                f"upstream covering stages:{rank}")
        template_id = "round129-common-rank-template:" + digest([
            "round129-family-common-rank-template-v1", family_root_id, rank
        ])
        expected = {
            "common_rank_template_id": template_id,
            "family_root_id": family_root_id,
            "common_rank": rank,
            "lower_face_template_id": lower[0],
            "upper_face_template_id": upper[0],
            "positive_source_x_length_strict_lower_exact": qstr(gap),
            "positive_source_x_length_exceeds_1_over_200": True,
            "covering_stage_indices": list(stage_indices),
            "source_recut_template_id": recut_ids[(0, 0)],
            "first_image_recut_template_id": recut_ids[(1, stage_indices[1])],
            "second_image_recut_template_id": recut_ids[(2, stage_indices[2])],
            "round117_operator_cell_id":
                round121["exact_seed_contract"]["round117_operator_cell_id"],
            "official_path_id": inherited_common[rank]["official_path_id"],
            "typed_parent_W_id_constructor":
                "round129-parent-W:sha256(canonical([family-root-id,"
                "angular-lift-id,exact-b-locator-derived-from-lambda]))",
            "refined_homogeneous_subbranch_id_constructor":
                "round129-refined-subbranch:sha256(canonical([typed-parent-W-id,"
                "round117-operator-cell-id,source-k=0,common-rank]))",
            "actual_child_id_constructor":
                "round129-common-child:sha256(canonical([refined-subbranch-id,"
                "exact-lambda-locator,common-rank]))",
            "exact_lambda_and_derived_exact_b_locators_required": True,
            "actual_standard_curve_child_exists_for_every_exact_lambda": True,
            "finite_common_rank_template_is_not_one_actual_fibre_child": True,
        }
        expected["row_sha256"] = digest(expected)
        require(row == expected, f"common exact rebuild:{rank}")
        if rank < 23:
            crossed_stage = endpoints[rank]["stage"]
            stage_indices[crossed_stage] += 1
    require(stage_indices == [0, 6, 17], "terminal stage indices")
    return common, recut_ids, endpoints


PHYSICAL_KEYS = set(
    """family_core_clearance_rows family_core_clearance_rows_sha256
    family_child_stage_boundary_rows family_child_stage_boundary_rows_sha256
    check_counts actual_interval_lower_minima claimed_strict_lower_margins
    along_curve_diagnostic_upper_not_F11 rank3_candidate_occurrence_stage_counts
    rank3_candidate_occurrence_count_per_common_rank
    rank3_candidate_occurrence_total_check_count
    physical_five_face_incidence_count residual_physical_face_count
    complete_typed_physical_face_empty_on_lambda_times_s_collar""".split()
)
CORE_ROW_KEYS = set(
    """common_rank collision_section physical_face_grammar_kind obstacle chart
    typed_C24_core_face_check_count distance_strict_lower
    actual_interval_lower_minimum incidence_count family_root_id
    common_rank_template_id uniform_over_entire_lambda_collar row_sha256""".split()
)
CHILD_PHYSICAL_KEYS = set(
    """common_rank stage source_owner actual_next_owner source_chart s_collar
    candidate_check_count active_integer_corner_ray_check_count
    typed_boundary_check_counts typed_boundary_actual_interval_lower_minima
    typed_boundary_claimed_strict_lower physical_boundary_incidence_count
    BYPASS_designated_b3_used_as_collision_angle
    along_seed_adapted_forward_Lipschitz_actual_upper
    along_seed_diagnostic_only_not_F11_field_value family_root_id
    common_rank_template_id uniform_over_entire_lambda_collar row_sha256""".split()
)
MOVING_FACE_KEYS = set(
    """face_template_id family_root_id stage natural_index_j boundary_label
    face_kind exact_level_equation_id exact_level_equation delta
    Round121_uniform_guard_endpoint_id s0_x_dyadic_bracket
    equation_decimal_participates_in_id base_image_chart base_image_obstacle
    base_curvature source_pullback_rank_path owner_below owner_above
    F_x_sign F_x_s0_abs_lower F_x_collar_abs_lower F_x_claimed_strict_lower
    F_s_abs_upper F_xx_abs_upper F_xs_abs_upper F_ss_abs_upper
    implicit_x_s_first_derivative_actual_abs_upper
    implicit_x_s_first_derivative_abs_upper
    implicit_x_s_second_derivative_actual_abs_upper
    implicit_x_s_second_derivative_abs_upper unique_analytic_graph
    graph_stays_in_s0_guard cut_order_preserved minimum_pair_separation_lower
    F8_normalized_wedge_strict_lower F8_formula F8_unstable_slope_interval
    F8_worst_case_squared_residual
    F9_source_pullback_unit_speed_C2_strict_upper F12_suffix_rank_path
    F12_C1_trace_pullback_strict_upper artificial_not_physical
    lambda_collar independent_s_collar lambda_and_s_are_distinct_parameters
    uniform_over_lambda_and_s_collar family_actual_face_id_constructor
    row_sha256""".split()
)
TRACE_KEYS = set(
    """trace_template_id face_template_id side adjacent_common_rank
    adjacent_common_rank_template_id family_actual_trace_id_constructor
    artificial_not_physical row_sha256""".split()
)
INCIDENCE_KEYS = set(
    """incidence_template_id common_rank common_rank_template_id
    lower_face_template_id upper_face_template_id lower_trace_template_id
    upper_trace_template_id exactly_two_artificial_boundary_faces
    physical_face_incidence_count row_sha256""".split()
)


def validate_physical(
    result: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
    core: dict[str, Any],
    family_root_id: str,
    common: list[dict[str, Any]],
) -> None:
    physical = result["uniform_physical_face_empty_audit"]
    require(type(physical) is dict and set(physical) == PHYSICAL_KEYS,
            "physical closed schema")
    require(
        physical["check_counts"] == v122.EXPECTED_PHYSICAL_COUNTS,
        "physical occurrence census",
    )
    require(
        physical["claimed_strict_lower_margins"] == {
            key: qstr(value)
            for key, value in sorted(v122.SAFE_PHYSICAL_MARGINS.items())
        },
        "physical claimed margins",
    )
    for key, value in physical["actual_interval_lower_minima"].items():
        require(
            qvalue(value, f"physical minimum:{key}")
            > v122.SAFE_PHYSICAL_MARGINS[key],
            f"physical stored strict minimum:{key}",
        )
    independent_minima = core["physical"]["independent_strict_lower_minima"]
    for key, value in independent_minima.items():
        require(
            Q(value) > v122.SAFE_PHYSICAL_MARGINS[key],
            f"independent physical strict minimum:{key}",
        )
    require(
        physical["rank3_candidate_occurrence_stage_counts"] == [57, 55, 57]
        and physical["rank3_candidate_occurrence_count_per_common_rank"] == 169
        and physical["rank3_candidate_occurrence_total_check_count"] == 4056,
        "physical candidate census",
    )
    require(
        physical["physical_five_face_incidence_count"] == 0
        and physical["residual_physical_face_count"] == 0
        and physical[
            "complete_typed_physical_face_empty_on_lambda_times_s_collar"
        ] is True,
        "physical empty conclusion",
    )
    diagnostics = [
        qvalue(value, f"along diagnostic:{stage}")
        for stage, value in enumerate(
            physical["along_curve_diagnostic_upper_not_F11"]
        )
    ]
    require(
        all(value < bound for value, bound in zip(diagnostics, (Q(7), Q(3), Q(12)))),
        "along-curve diagnostics",
    )

    core_rows = physical["family_core_clearance_rows"]
    require(type(core_rows) is list and len(core_rows) == 96, "96 core rows")
    require(
        physical["family_core_clearance_rows_sha256"] == digest(core_rows),
        "core rows digest",
    )
    expected_sections = {
        0: ("source_core_clipping_face", "G", "W"),
        1: ("intermediate_core_avoidance_preimage_face", "W", "N"),
        2: ("intermediate_core_avoidance_preimage_face", "G", "S"),
        3: ("terminal_core_preimage_face", "G", "N"),
    }
    seen_core: set[tuple[int, int]] = set()
    for index, row in enumerate(core_rows):
        require(type(row) is dict and set(row) == CORE_ROW_KEYS,
                f"core row schema:{index}")
        row_digest(row, f"core row:{index}")
        key = (row["common_rank"], row["collision_section"])
        require(key not in seen_core, f"core row unique:{key}")
        seen_core.add(key)
        rank, section = key
        require(0 <= rank < 24 and section in expected_sections,
                f"core row index:{key}")
        role, obstacle, chart = expected_sections[section]
        require(
            row["physical_face_grammar_kind"] == role
            and row["obstacle"] == obstacle
            and row["chart"] == chart,
            f"core row grammar:{key}",
        )
        require(
            row["family_root_id"] == family_root_id
            and row["common_rank_template_id"]
            == common[rank]["common_rank_template_id"]
            and row["uniform_over_entire_lambda_collar"] is True,
            f"core row family crosswalk:{key}",
        )
        require(
            row["typed_C24_core_face_check_count"] == 12
            and qvalue(row["distance_strict_lower"], f"core claim:{key}") == Q(1, 3)
            and qvalue(row["actual_interval_lower_minimum"],
                       f"core actual:{key}") > Q(1, 3)
            and row["incidence_count"] == 0,
            f"core row strict empty:{key}",
        )
    require(len(seen_core) == 96, "complete core row keys")

    child_rows = physical["family_child_stage_boundary_rows"]
    require(type(child_rows) is list and len(child_rows) == 72,
            "72 child-stage rows")
    require(
        physical["family_child_stage_boundary_rows_sha256"] == digest(child_rows),
        "child-stage rows digest",
    )
    current = ("G[0,0]", "W[-1,-1]", "G[0,0]")
    selected = ("W[-1,-1]", "G[0,0]", "G[-1,-2]")
    charts = ("W", "N", "S")
    seen_child: set[tuple[int, int]] = set()
    for index, row in enumerate(child_rows):
        require(type(row) is dict and set(row) == CHILD_PHYSICAL_KEYS,
                f"child physical schema:{index}")
        row_digest(row, f"child physical:{index}")
        key = (row["common_rank"], row["stage"])
        require(key not in seen_child, f"child physical unique:{key}")
        seen_child.add(key)
        rank, stage = key
        require(0 <= rank < 24 and stage in (0, 1, 2),
                f"child physical index:{key}")
        require(
            row["source_owner"] == current[stage]
            and row["actual_next_owner"] == selected[stage]
            and row["source_chart"] == charts[stage],
            f"child physical path:{key}",
        )
        require(
            row["candidate_check_count"] == (57, 55, 57)[stage],
            f"candidate count:{key}",
        )
        require(
            row["family_root_id"] == family_root_id
            and row["common_rank_template_id"]
            == common[rank]["common_rank_template_id"]
            and row["uniform_over_entire_lambda_collar"] is True,
            f"child physical family:{key}",
        )
        require(
            row["physical_boundary_incidence_count"] == 0
            and row["BYPASS_designated_b3_used_as_collision_angle"] is False
            and row["along_seed_diagnostic_only_not_F11_field_value"] is True,
            f"child physical semantics:{key}",
        )
        counts = row["typed_boundary_check_counts"]
        minima = row["typed_boundary_actual_interval_lower_minima"]
        claims = row["typed_boundary_claimed_strict_lower"]
        require(set(counts) == set(minima) == set(claims),
                f"typed physical keys:{key}")
        for name in counts:
            require(type(counts[name]) is int and counts[name] > 0,
                    f"typed count:{key}:{name}")
            require(
                qvalue(claims[name], f"typed claim:{key}:{name}")
                == v122.SAFE_PHYSICAL_MARGINS[name],
                f"typed claim exact:{key}:{name}",
            )
            require(
                qvalue(minima[name], f"typed actual:{key}:{name}")
                > v122.SAFE_PHYSICAL_MARGINS[name],
                f"typed actual strict:{key}:{name}",
            )
    require(len(seen_child) == 72, "complete child-stage keys")

    round122 = documents[122]["certificate"]["result"]
    for name in ("physical_five_face_grammar_rows",
                 "physical_seven_boundary_kind_rows"):
        rows = result[name]
        require(rows == round122[name], f"{name} exact frozen grammar")
        require(result[f"{name}_sha256"] == digest(rows), f"{name} digest")


def validate_artificial(
    result: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
    family_root_id: str,
    common: list[dict[str, Any]],
    endpoints: list[dict[str, Any]],
) -> dict[int, dict[str, Any]]:
    registry = result["parameterized_artificial_face_registry"]
    expected_registry_keys = {
        "stationary_outer_face_template_rows",
        "stationary_outer_face_template_rows_sha256",
        "moving_artificial_face_template_rows",
        "moving_artificial_face_template_rows_sha256",
        "artificial_trace_template_rows",
        "artificial_trace_template_rows_sha256",
        "child_face_incidence_template_rows",
        "child_face_incidence_template_rows_sha256",
        "stationary_outer_face_template_count",
        "moving_artificial_face_template_count",
        "artificial_face_template_count",
        "artificial_trace_template_count",
        "child_face_incidence_template_count",
        "artificial_faces_retained_despite_physical_empty_statement",
    }
    require(type(registry) is dict and set(registry) == expected_registry_keys,
            "artificial registry schema")
    require(
        (
            registry["stationary_outer_face_template_count"],
            registry["moving_artificial_face_template_count"],
            registry["artificial_face_template_count"],
            registry["artificial_trace_template_count"],
            registry["child_face_incidence_template_count"],
        ) == (2, 23, 25, 48, 24),
        "artificial registry census",
    )
    require(registry["artificial_faces_retained_despite_physical_empty_statement"]
            is True, "artificial faces retained")
    round121 = documents[121]["certificate"]["result"]
    upstream_endpoints = {
        (row["stage"], row["natural_index_j"]): row
        for row in round121["pullback_endpoint_rows"]
    }

    moving = registry["moving_artificial_face_template_rows"]
    require(type(moving) is list and len(moving) == 23, "moving face census")
    require(
        registry["moving_artificial_face_template_rows_sha256"] == digest(moving),
        "moving face digest",
    )
    moving_by_key: dict[tuple[int, int], dict[str, Any]] = {}
    for index, row in enumerate(moving):
        require(type(row) is dict and set(row) == MOVING_FACE_KEYS,
                f"moving face schema:{index}")
        row_digest(row, f"moving face:{index}")
        key = (row["stage"], row["natural_index_j"])
        require(key in upstream_endpoints and key not in moving_by_key,
                f"moving face key:{key}")
        moving_by_key[key] = row
        endpoint = next(
            endpoint for endpoint in endpoints
            if (endpoint["stage"], endpoint["natural_index_j"]) == key
        )
        require(
            row["face_template_id"] == endpoint["face_template_id"]
            and row["Round121_uniform_guard_endpoint_id"]
            == upstream_endpoints[key]["endpoint_id"]
            and row["s0_x_dyadic_bracket"]
            == upstream_endpoints[key]["x_dyadic_bracket"],
            f"moving face endpoint crosswalk:{key}",
        )
        require(
            row["family_root_id"] == family_root_id
            and row["lambda_collar"] == [qstr(LAMBDA_LOWER), qstr(LAMBDA_UPPER)]
            and row["independent_s_collar"]
            == [qstr(-S_EPSILON), qstr(S_EPSILON)]
            and row["lambda_and_s_are_distinct_parameters"] is True
            and row["uniform_over_lambda_and_s_collar"] is True,
            f"moving face parameter namespace:{key}",
        )
        require(
            row["face_kind"] == "PARAMETERIZED_ARTIFICIAL_PULLBACK_RECUT"
            and row["artificial_not_physical"] is True
            and row["unique_analytic_graph"] is True
            and row["graph_stays_in_s0_guard"] is True
            and row["cut_order_preserved"] is True,
            f"moving artificial semantics:{key}",
        )
        require(
            row["exact_level_equation"] == f"U{key[0]}(lambda,x,s)={key[1]}*10^-90",
            f"moving face equation:{key}",
        )
        require(
            row["F_x_sign"] == 1
            and qvalue(row["F_x_collar_abs_lower"], f"moving Fx:{key}")
            > qvalue(row["F_x_claimed_strict_lower"],
                     f"moving Fx claim:{key}"),
            f"moving face derivative:{key}",
        )
    require(
        tuple(moving_by_key) == EXPECTED_CUT_ORDER,
        "moving face order",
    )

    outer = registry["stationary_outer_face_template_rows"]
    require(type(outer) is list and len(outer) == 2, "outer face census")
    require(
        registry["stationary_outer_face_template_rows_sha256"] == digest(outer),
        "outer face digest",
    )
    for index, row in enumerate(outer):
        require(type(row) is dict and "row_sha256" in row,
                f"outer face schema:{index}")
        row_digest(row, f"outer face:{index}")
        require(
            row["face_template_id"]
            == ("round129-family-source-outer-left",
                "round129-family-source-outer-right")[index]
            and row["family_root_id"] == family_root_id
            and row["face_kind"] == "STATIONARY_ARTIFICIAL_SOURCE_OUTER_FACE"
            and row["artificial_not_physical"] is True
            and row["lambda_and_s_are_distinct_parameters"] is True
            and row["uniform_over_lambda_and_s_collar"] is True,
            f"outer face semantics:{index}",
        )

    ordered_faces = [outer[0], *moving, outer[1]]
    traces = registry["artificial_trace_template_rows"]
    require(type(traces) is list and len(traces) == 48, "trace census")
    require(
        registry["artificial_trace_template_rows_sha256"] == digest(traces),
        "trace digest",
    )
    trace_index: dict[tuple[str, str], str] = {}
    for index, row in enumerate(traces):
        require(type(row) is dict and set(row) == TRACE_KEYS,
                f"trace schema:{index}")
        row_digest(row, f"trace:{index}")
        face_id, side = row["face_template_id"], row["side"]
        require(side in ("lower", "upper"), f"trace side:{index}")
        trace_id = "round129-artificial-trace-template:" + digest([
            "round129-family-artificial-trace-template-v1", face_id, side
        ])
        require(row["trace_template_id"] == trace_id, f"trace ID:{index}")
        rank = row["adjacent_common_rank"]
        require(0 <= rank < 24, f"trace rank:{index}")
        require(
            row["adjacent_common_rank_template_id"]
            == common[rank]["common_rank_template_id"]
            and row["artificial_not_physical"] is True,
            f"trace crosswalk:{index}",
        )
        require((face_id, side) not in trace_index, f"trace unique:{index}")
        trace_index[(face_id, side)] = trace_id

    incidences = registry["child_face_incidence_template_rows"]
    require(type(incidences) is list and len(incidences) == 24,
            "incidence census")
    require(
        registry["child_face_incidence_template_rows_sha256"]
        == digest(incidences),
        "incidence digest",
    )
    incidence_by_rank: dict[int, dict[str, Any]] = {}
    for rank, row in enumerate(incidences):
        require(type(row) is dict and set(row) == INCIDENCE_KEYS,
                f"incidence schema:{rank}")
        row_digest(row, f"incidence:{rank}")
        lower = ordered_faces[rank]["face_template_id"]
        upper = ordered_faces[rank + 1]["face_template_id"]
        incidence_id = "round129-child-face-incidence-template:" + digest([
            "round129-family-child-face-incidence-template-v1",
            family_root_id,
            rank,
            lower,
            upper,
        ])
        require(
            row["common_rank"] == rank
            and row["incidence_template_id"] == incidence_id
            and row["common_rank_template_id"]
            == common[rank]["common_rank_template_id"]
            and row["lower_face_template_id"] == lower
            and row["upper_face_template_id"] == upper
            and row["lower_trace_template_id"] == trace_index[(lower, "upper")]
            and row["upper_trace_template_id"] == trace_index[(upper, "lower")]
            and row["exactly_two_artificial_boundary_faces"] is True
            and row["physical_face_incidence_count"] == 0,
            f"incidence exact crosswalk:{rank}",
        )
        incidence_by_rank[rank] = row
    return incidence_by_rank


BASE_KEYS = set(
    """base_key_template_id family_root_id common_rank
    common_rank_template_id official_word_key_id stage roof_level_j
    materialized_input_recut_template_id parameterized_base_key_constructor
    per_exact_lambda_fibre_actual_base_key_exists
    finite_row_is_a_parameterized_template_not_an_actual_fibre_key
    row_sha256""".split()
)
FIELD_BASE_KEYS = set(
    """field_slot_template_id base_key_template_id family_root_id common_rank
    official_word_key_id stage roof_level_j field_index field_name
    field_value_or_contract field_bound_semantics
    parameterized_immutable_slot_key_constructor
    parameterized_actual_slot_id_constructor
    exact_lambda_locator_and_derived_exact_b_locator_required
    per_exact_lambda_fibre_actual_slot_certified
    finite_row_is_a_parameterized_slot_template_not_an_actual_slot
    slot_template_status materialized_input_recut_template_id
    transparent_wall_roof_split_does_not_add_collision_factor row_sha256""".split()
)
FACE_FIELD_KEYS = {
    "child_face_incidence_template_id",
    "lower_artificial_face_template_id",
    "upper_artificial_face_template_id",
    "complete_physical_face_empty_audit_bound",
}


def validate_templates_and_safety(
    result: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
    family_root_id: str,
    common: list[dict[str, Any]],
    recut_ids: dict[tuple[int, int], str],
    incidence_by_rank: dict[int, dict[str, Any]],
) -> None:
    round121 = documents[121]["certificate"]["result"]
    round122 = documents[122]["certificate"]["result"]
    rank_by_child = {
        row["common_child_id"]: row["common_rank"]
        for row in round121["common_refinement_rows"]
    }
    exact121 = {
        (
            row["common_child_id"],
            row["stage"],
            row["roof_level_j"],
            row["field_index"],
        ): row
        for row in round121["gate5_F1_F6_slot_rows"]
    }
    exact122 = {
        (
            row["common_child_id"],
            row["stage"],
            row["roof_level_j"],
            row["field_index"],
        ): row
        for row in round122["gate5_F7_F13_F16_slot_rows"]
    }
    base_source = sorted(
        (
            row for row in round121["gate5_F1_F6_slot_rows"]
            if row["field_index"] == 1
        ),
        key=lambda row: (
            rank_by_child[row["common_child_id"]],
            row["stage"],
            row["roof_level_j"],
        ),
    )
    require(len(base_source) == 120, "upstream base source census")
    base_rows = result["parameterized_base_key_template_rows"]
    field_rows = result["parameterized_F1_F13_F16_slot_template_rows"]
    require(type(base_rows) is list and len(base_rows) == 120, "base census")
    require(type(field_rows) is list and len(field_rows) == 1680, "field census")
    require(
        result["parameterized_base_key_template_rows_sha256"] == digest(base_rows),
        "base list digest",
    )
    require(
        result["parameterized_F1_F13_F16_slot_template_rows_sha256"]
        == digest(field_rows),
        "field list digest",
    )

    expected_bases: list[dict[str, Any]] = []
    expected_fields: list[dict[str, Any]] = []
    for source in base_source:
        rank = rank_by_child[source["common_child_id"]]
        stage = source["stage"]
        roof = source["roof_level_j"]
        word = source["official_word_key_id"]
        require(word == OFFICIAL_WORDS[stage], f"base official word:{rank}:{stage}")
        base_id = "round129-base-key-template:" + digest([
            "round129-family-base-key-template-v1",
            family_root_id,
            rank,
            word,
            stage,
            roof,
        ])
        recut_id = recut_ids[
            (stage, common[rank]["covering_stage_indices"][stage])
        ]
        base = {
            "base_key_template_id": base_id,
            "family_root_id": family_root_id,
            "common_rank": rank,
            "common_rank_template_id": common[rank]["common_rank_template_id"],
            "official_word_key_id": word,
            "stage": stage,
            "roof_level_j": roof,
            "materialized_input_recut_template_id": recut_id,
            "parameterized_base_key_constructor":
                "(official-word-key-id,refined-subbranch-id(exact-b-locator),"
                "roof-level-j)",
            "per_exact_lambda_fibre_actual_base_key_exists": True,
            "finite_row_is_a_parameterized_template_not_an_actual_fibre_key":
                True,
        }
        base["row_sha256"] = digest(base)
        expected_bases.append(base)

        for field_index in CERTIFIED_FIELDS:
            source_map = exact121 if field_index <= 6 else exact122
            inherited = source_map[
                (source["common_child_id"], stage, roof, field_index)
            ]
            require(
                inherited["field_name"] == FIELD_NAMES[field_index],
                f"field name upstream:{rank}:{stage}:{roof}:F{field_index}",
            )
            field = {
                "field_slot_template_id":
                    "round129-field-slot-template:" + digest([
                        "round129-family-field-slot-template-v1",
                        base_id,
                        field_index,
                        FIELD_NAMES[field_index],
                    ]),
                "base_key_template_id": base_id,
                "family_root_id": family_root_id,
                "common_rank": rank,
                "official_word_key_id": word,
                "stage": stage,
                "roof_level_j": roof,
                "field_index": field_index,
                "field_name": FIELD_NAMES[field_index],
                "field_value_or_contract": inherited["field_value_or_contract"],
                "field_bound_semantics": inherited.get(
                    "field_bound_semantics", "INHERITED_EXACT_CONTRACT"
                ),
                "parameterized_immutable_slot_key_constructor":
                    "(official-word-key-id,refined-subbranch-id(exact-b-locator),"
                    "roof-level-j,field-name)",
                "parameterized_actual_slot_id_constructor":
                    "round129-slot:sha256(canonical([official-word-key-id,"
                    "refined-subbranch-id(exact-b-locator),roof-level-j,"
                    "field-name]))",
                "exact_lambda_locator_and_derived_exact_b_locator_required": True,
                "per_exact_lambda_fibre_actual_slot_certified": True,
                "finite_row_is_a_parameterized_slot_template_not_an_actual_slot":
                    True,
                "slot_template_status":
                    "CERTIFIED_ON_EVERY_EXACT_LAMBDA_FIBRE_COMMON_CHILD",
                "materialized_input_recut_template_id": recut_id,
                "transparent_wall_roof_split_does_not_add_collision_factor":
                    True,
            }
            if field_index >= 7:
                incidence = incidence_by_rank[rank]
                field.update({
                    "child_face_incidence_template_id":
                        incidence["incidence_template_id"],
                    "lower_artificial_face_template_id":
                        incidence["lower_face_template_id"],
                    "upper_artificial_face_template_id":
                        incidence["upper_face_template_id"],
                    "complete_physical_face_empty_audit_bound": True,
                })
            if field_index == 5:
                field["uniform_template_scope"] = (
                    "every actual homogeneous physical solid-collision child "
                    "on a canonical adapted standard curve"
                )
            if field_index == 6:
                field.update({
                    "uniform_template_scope":
                        "one canonical-curve log-Jacobian oscillation on this leg",
                    "three_leg_only_not_arbitrary_return_depth": True,
                })
            if field_index == 11:
                field.update({
                    "full_phase_authoritative_envelope_used": True,
                    "along_curve_diagnostic_used_as_field_value": False,
                    "alpha_scope": "0<alpha<=1",
                })
            field["row_sha256"] = digest(field)
            expected_fields.append(field)
    require(base_rows == expected_bases, "120 base templates exact rebuild")
    require(field_rows == expected_fields, "1680 field templates exact rebuild")

    for index, row in enumerate(base_rows):
        require(type(row) is dict and set(row) == BASE_KEYS,
                f"base closed schema:{index}")
        row_digest(row, f"base:{index}")
    field_counts: Counter[int] = Counter()
    grouped: defaultdict[str, list[int]] = defaultdict(list)
    for index, row in enumerate(field_rows):
        keys = set(row)
        expected_keys = set(FIELD_BASE_KEYS)
        field_index = row["field_index"]
        if field_index >= 7:
            expected_keys |= FACE_FIELD_KEYS
        if field_index == 5:
            expected_keys |= {"uniform_template_scope"}
        if field_index == 6:
            expected_keys |= {
                "uniform_template_scope",
                "three_leg_only_not_arbitrary_return_depth",
            }
        if field_index == 11:
            expected_keys |= {
                "full_phase_authoritative_envelope_used",
                "along_curve_diagnostic_used_as_field_value",
                "alpha_scope",
            }
        require(keys == expected_keys, f"field closed schema:{index}")
        row_digest(row, f"field:{index}")
        field_counts[field_index] += 1
        grouped[row["base_key_template_id"]].append(field_index)
    require(
        field_counts == Counter({field: 120 for field in CERTIFIED_FIELDS}),
        "120 templates per field",
    )
    require(
        len(grouped) == 120
        and all(sorted(indices) == list(CERTIFIED_FIELDS)
                for indices in grouped.values()),
        "fourteen fields exact once per base",
    )

    theta = Q(144000, 180337)
    variation = Q(3, 200000)
    theorems = result["uniform_field_theorems"]
    require_exact(
        theorems,
        {
            "certified_field_indices": list(CERTIFIED_FIELDS),
            "certified_field_names": [
                FIELD_NAMES[index] for index in CERTIFIED_FIELDS
            ],
            "F5_one_step_adapted_inverse_strict_upper": qstr(theta),
            "F5_three_leg_path_product_strict_upper": qstr(theta**3),
            "F6_one_leg_canonical_curve_log_variation_strict_upper":
                qstr(variation),
            "F6_three_leg_path_sum_strict_upper": qstr(3 * variation),
            "F6_scope_is_exactly_the_fixed_three_leg_record": True,
            "F6_arbitrary_return_depth_or_global_all_record_claim": False,
            "F11_full_phase_stage_strict_upper": {
                "0": qstr(150 * 2**15),
                "1": qstr(150 * 2**14),
                "2": qstr(150 * 2**14),
            },
            "F11_uses_full_phase_authoritative_rank_envelopes": True,
            "F11_along_curve_diagnostics_not_used_as_field_values": True,
            "F10_F13_F16_are_zero_only_because_complete_physical_face_family_is_empty":
                True,
            "artificial_recut_faces_are_retained_and_not_called_physical_faces":
                True,
        },
        "uniform field theorems",
    )

    expected_ledger = {
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
    }
    require_exact(result["count_ledger"], expected_ledger, "count ledger")

    local_status = {
        **{
            f"F{field}":
                "CERTIFIED_ON_EVERY_EXACT_LAMBDA_FIBRE_AND_ALL_24_COMMON_RANKS"
            for field in CERTIFIED_FIELDS
        },
        "F14": "NOT_INSTALLED_ON_POSITIVE_BOREL_FAMILY",
        "F15": "NOT_INSTALLED_ON_POSITIVE_BOREL_FAMILY",
        "F17": "NOT_INSTALLED_ON_POSITIVE_BOREL_FAMILY",
        "F18": "NOT_INSTALLED_ON_POSITIVE_BOREL_FAMILY",
    }
    require_exact(result["local_field_status"], local_status, "local field status")
    require(
        result["positive_Borel_family_local_field_maturity"] == "14/18"
        and result["gate5_global_maturity"] == "10/18"
        and result["gate5_status"] == "NOT_CERTIFIED"
        and result["complete_18_field_block_count"] == 0
        and result["global_complete_18_field_block_count"] == 0
        and result["gate5_block_count"] == 0
        and result["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "fail-closed safety state",
    )


def validate_frozen_chain(
    result: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
) -> None:
    chain = result["frozen_chain_contract"]
    require(type(chain) is dict and set(chain) == {
        "Round120_through_Round128_primary_file_pin_count",
        "all_primary_certificates_closed_and_verifications_PASS",
        "certificate_result_sha256_pins",
        "verification_result_sha256_pins",
        "upstream_primary_file_byte_pins",
    }, "frozen chain schema")
    require(
        chain["Round120_through_Round128_primary_file_pin_count"]
        == len(UPSTREAM_PINS),
        "frozen primary pin count",
    )
    require(chain["all_primary_certificates_closed_and_verifications_PASS"] is True,
            "frozen verifications PASS")
    require(
        chain["upstream_primary_file_byte_pins"]
        == dict(sorted(UPSTREAM_PINS.items())),
        "frozen upstream byte pins",
    )
    expected_certificates = {
        f"Round{round_index}_certificate_result_sha256":
            documents[round_index]["certificate"]["result_sha256"]
        for round_index in range(120, 129)
    }
    expected_verifications = {
        f"Round{round_index}_verification_result_sha256":
            documents[round_index]["verification"]["result_sha256"]
        for round_index in range(120, 129)
    }
    require(
        chain["certificate_result_sha256_pins"] == expected_certificates,
        "certificate result pins",
    )
    require(
        chain["verification_result_sha256_pins"] == expected_verifications,
        "verification result pins",
    )


def validate_document(
    document: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
    core: dict[str, Any],
) -> dict[str, Any]:
    require(type(document) is dict, "certificate top object")
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "certificate closed envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(type(document["result"]) is dict, "certificate result object")
    require(
        document["result_sha256"] == digest(document["result"]),
        "certificate result digest",
    )
    result = document["result"]
    require(set(result) == RESULT_KEYS, "certificate result closed schema")
    require(result["precision_bits"] == 4096, "certificate precision")
    require(
        result["status"]
        == "CERTIFIED_POSITIVE_BOREL_RANK3_RECUT_FIELD_STRATUM__LOCAL_14_OF_18",
        "certificate status",
    )
    validate_frozen_chain(result, documents)
    family_root_id = validate_root_namespace(result, documents, core)
    common, recut_ids, endpoints = validate_endpoints_recuts_common(
        result, documents, core, family_root_id
    )
    validate_physical(result, documents, core, family_root_id, common)
    incidences = validate_artificial(
        result, documents, family_root_id, common, endpoints
    )
    validate_templates_and_safety(
        result, documents, family_root_id, common, recut_ids, incidences
    )
    require(
        result["strict_scope"]
        == "one explicit positive-Borel b-image of the lambda=b3 collar inside "
           "one frozen Round112/Round113/Round117 rank-three root/operator cell; "
           "24 parameterized common ranks per exact lambda; independent "
           "|s|<=2^-512 physical collar; local F1-F13 and F16 only",
        "strict scope",
    )
    require(type(result["strict_nonclaims"]) is list
            and len(result["strict_nonclaims"]) == 10,
            "strict nonclaim census")
    required_nonclaim_fragments = (
        "not the global 441280-word registry",
        "no finite count is assigned",
        "lambda=b3",
        "not arbitrary return depth",
        "does not certify arbitrary global return words",
        "physical-face family is empty",
        "no nonempty F10",
        "not copied onto this positive-Borel family",
        "no complete 18-field block",
    )
    nonclaims_text = "\n".join(result["strict_nonclaims"])
    for fragment in required_nonclaim_fragments:
        require(fragment in nonclaims_text, f"strict nonclaim:{fragment}")
    return {
        "family_root_id": family_root_id,
        "endpoint_count": 23,
        "recut_template_count": 26,
        "common_rank_count": 24,
        "base_template_count": 120,
        "field_template_count": 1680,
        "physical_candidate_check_count": 4056,
        "physical_face_count": 0,
        "local_maturity": "14/18",
        "global_maturity": "10/18",
        "cm2": "NO-GO_FOR_CLAIM",
    }


def get_path(root: Any, path: tuple[Any, ...]) -> Any:
    value = root
    for key in path:
        value = value[key]
    return value


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    target = root
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def resign_tree(value: Any) -> None:
    """Repair every nested row/list digest after a semantic mutation."""
    if type(value) is list:
        for item in value:
            resign_tree(item)
        return
    if type(value) is not dict:
        return
    for key, item in list(value.items()):
        if key == "row_sha256" or key.endswith("_sha256"):
            continue
        resign_tree(item)
    if "row_sha256" in value:
        payload = dict(value)
        payload.pop("row_sha256")
        value["row_sha256"] = digest(payload)
    for key in list(value):
        if key.endswith("_sha256") and key != "row_sha256":
            sibling = key[:-7]
            if sibling in value:
                value[key] = digest(value[sibling])


def resign_document(document: dict[str, Any]) -> None:
    resign_tree(document["result"])
    document["result_sha256"] = digest(document["result"])


Mutator = Callable[[dict[str, Any]], None]


def path_mutation(path: tuple[Any, ...], value: Any) -> Mutator:
    return lambda document: set_path(document, path, value)


def semantic_mutations(
    document: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
    core: dict[str, Any],
) -> list[str]:
    r = ("result",)
    attacks: list[tuple[str, Mutator]] = [
        ("schema", path_mutation(("schema",), "cm2.round129.mutated")),
        ("precision", path_mutation(r + ("precision_bits",), 3072)),
        ("status", path_mutation(r + ("status",), "PASS")),
        (
            "upstream pin",
            path_mutation(
                r + ("frozen_chain_contract", "upstream_primary_file_byte_pins",
                     "cm2_round128_base_r1_component_global_word_incidence.py"),
                "0" * 64,
            ),
        ),
        (
            "verification pin",
            path_mutation(
                r + ("frozen_chain_contract", "verification_result_sha256_pins",
                     "Round128_verification_result_sha256"),
                "0" * 64,
            ),
        ),
        (
            "family root ID",
            path_mutation(
                r + ("positive_Borel_family_root_contract", "family_root_id"),
                "round129-positive-borel-family-root:" + "0" * 64,
            ),
        ),
        (
            "sheet HIT",
            path_mutation(
                r + ("positive_Borel_family_root_contract", "sheet_kind"), "HIT"
            ),
        ),
        (
            "branch",
            path_mutation(
                r + ("positive_Borel_family_root_contract", "branch_key"),
                [7, "G[0,0]", "W[-1,-1]", 1],
            ),
        ),
        (
            "lambda center",
            path_mutation(
                r + ("positive_Borel_family_root_contract", "lambda_center"),
                "1/65536",
            ),
        ),
        (
            "lambda epsilon",
            path_mutation(
                r + ("positive_Borel_family_root_contract", "lambda_epsilon"),
                qstr(Q(1, 2**511)),
            ),
        ),
        (
            "lambda collar gap",
            path_mutation(
                r + ("positive_Borel_family_root_contract",
                     "lambda_exact_dyadic_closed_collar", 0),
                qstr(LAMBDA_CENTER),
            ),
        ),
        (
            "t face signs",
            path_mutation(
                r + ("positive_Borel_family_root_contract",
                     "uniform_t_guard_face_signs"),
                [-1, 1],
            ),
        ),
        (
            "Ft sign",
            path_mutation(
                r + ("positive_Borel_family_root_contract",
                     "uniform_F_t_enclosure"),
                ["7", "8"],
            ),
        ),
        (
            "Flambda sign",
            path_mutation(
                r + ("positive_Borel_family_root_contract",
                     "uniform_F_lambda_enclosure"),
                ["-1/100000", "-1/2000000"],
            ),
        ),
        (
            "dt sign",
            path_mutation(
                r + ("positive_Borel_family_root_contract",
                     "implicit_dt_dlambda_enclosure"),
                ["-1/3000000", "-1/4000000"],
            ),
        ),
        (
            "db sign",
            path_mutation(
                r + ("positive_Borel_family_root_contract",
                     "db_dlambda_enclosure"),
                ["-1/2000000", "-1/2250000"],
            ),
        ),
        (
            "b monotonicity",
            path_mutation(
                r + ("positive_Borel_family_root_contract",
                     "b_of_lambda_strictly_increasing"),
                False,
            ),
        ),
        (
            "Borel image zero",
            path_mutation(
                r + ("positive_Borel_family_root_contract",
                     "b_image_length_strict_lower_exact"),
                "0",
            ),
        ),
        (
            "lambda equals s",
            path_mutation(
                r + ("two_parameter_namespace_contract", "lambda_is_not_s"),
                False,
            ),
        ),
        (
            "namespace s collar",
            path_mutation(
                r + ("two_parameter_namespace_contract", "s_collar"),
                [qstr(LAMBDA_LOWER), qstr(LAMBDA_UPPER)],
            ),
        ),
        (
            "namespace substitution",
            path_mutation(
                r + ("two_parameter_namespace_contract",
                     "no_identifier_substitutes_one_parameter_for_the_other"),
                False,
            ),
        ),
        (
            "finite parent registry",
            path_mutation(
                r + ("parameterized_actual_parent_W_registry",
                     "whole_registry_is_uncountable_and_not_finitely_enumerated"),
                False,
            ),
        ),
        (
            "stage orientation",
            path_mutation(
                r + ("uniform_stage_adapted_coordinate_contract",
                     "stage_orientations"),
                [1, 1, 1],
            ),
        ),
        (
            "cut count",
            path_mutation(
                r + ("uniform_stage_adapted_coordinate_contract",
                     "uniform_pullback_cut_count"),
                22,
            ),
        ),
        (
            "cut order",
            lambda d: get_path(
                d, r + ("uniform_stage_adapted_coordinate_contract",
                        "uniform_cut_order")
            ).__setitem__(
                slice(0, 2),
                list(reversed(get_path(
                    d, r + ("uniform_stage_adapted_coordinate_contract",
                            "uniform_cut_order")
                )[:2])),
            ),
        ),
        (
            "U1 derivative",
            path_mutation(
                r + ("uniform_stage_adapted_coordinate_contract",
                     "U1_prime_over_delta_enclosure"),
                ["0", "1"],
            ),
        ),
        (
            "endpoint duplicate",
            lambda d: get_path(
                d, r + ("uniform_pullback_face_guard_rows",)
            ).__setitem__(
                1, copy.deepcopy(get_path(
                    d, r + ("uniform_pullback_face_guard_rows", 0)
                ))
            ),
        ),
        (
            "endpoint face ID",
            path_mutation(
                r + ("uniform_pullback_face_guard_rows", 0,
                     "face_template_id"),
                "round129-uniform-pullback-face-template:" + "0" * 64,
            ),
        ),
        (
            "endpoint stage",
            path_mutation(
                r + ("uniform_pullback_face_guard_rows", 0, "stage"), 1
            ),
        ),
        (
            "endpoint guard",
            path_mutation(
                r + ("uniform_pullback_face_guard_rows", 0,
                     "uniform_x_dyadic_guard", 0),
                "0",
            ),
        ),
        (
            "endpoint sign",
            path_mutation(
                r + ("uniform_pullback_face_guard_rows", 0,
                     "all_lambda_left_function_sign"),
                1,
            ),
        ),
        (
            "endpoint uniqueness",
            path_mutation(
                r + ("uniform_pullback_face_guard_rows", 0,
                     "unique_root_for_every_exact_lambda"),
                False,
            ),
        ),
        (
            "recut duplicate",
            lambda d: get_path(
                d, r + ("parameterized_stage_recut_template_rows",)
            ).__setitem__(
                1, copy.deepcopy(get_path(
                    d, r + ("parameterized_stage_recut_template_rows", 0)
                ))
            ),
        ),
        (
            "recut orientation",
            path_mutation(
                r + ("parameterized_stage_recut_template_rows", 1,
                     "orientation"),
                1,
            ),
        ),
        (
            "recut lower face",
            path_mutation(
                r + ("parameterized_stage_recut_template_rows", 2,
                     "lower_face_template_id"),
                "round129-family-source-outer-left",
            ),
        ),
        (
            "recut not materialized",
            path_mutation(
                r + ("parameterized_stage_recut_template_rows", 0,
                     "actual_materialized_input_recut_for_every_exact_lambda"),
                False,
            ),
        ),
        (
            "common duplicate rank",
            path_mutation(
                r + ("parameterized_common_rank_template_rows", 1,
                     "common_rank"),
                0,
            ),
        ),
        (
            "common zero gap",
            path_mutation(
                r + ("parameterized_common_rank_template_rows", 0,
                     "positive_source_x_length_strict_lower_exact"),
                "0",
            ),
        ),
        (
            "common covering",
            path_mutation(
                r + ("parameterized_common_rank_template_rows", 3,
                     "covering_stage_indices"),
                [0, 1, 1],
            ),
        ),
        (
            "common path",
            path_mutation(
                r + ("parameterized_common_rank_template_rows", 0,
                     "official_path_id"),
                "wrong-path",
            ),
        ),
        (
            "physical candidate census",
            path_mutation(
                r + ("uniform_physical_face_empty_audit", "check_counts",
                     "candidate_tangency"),
                4055,
            ),
        ),
        (
            "physical minimum",
            path_mutation(
                r + ("uniform_physical_face_empty_audit",
                     "actual_interval_lower_minima", "candidate_tangency"),
                "0",
            ),
        ),
        (
            "physical empty false",
            path_mutation(
                r + ("uniform_physical_face_empty_audit",
                     "complete_typed_physical_face_empty_on_lambda_times_s_collar"),
                False,
            ),
        ),
        (
            "physical incidence",
            path_mutation(
                r + ("uniform_physical_face_empty_audit",
                     "physical_five_face_incidence_count"),
                1,
            ),
        ),
        (
            "core incidence",
            path_mutation(
                r + ("uniform_physical_face_empty_audit",
                     "family_core_clearance_rows", 0, "incidence_count"),
                1,
            ),
        ),
        (
            "core face count",
            path_mutation(
                r + ("uniform_physical_face_empty_audit",
                     "family_core_clearance_rows", 0,
                     "typed_C24_core_face_check_count"),
                11,
            ),
        ),
        (
            "child candidate count",
            path_mutation(
                r + ("uniform_physical_face_empty_audit",
                     "family_child_stage_boundary_rows", 0,
                     "candidate_check_count"),
                56,
            ),
        ),
        (
            "b3 collision angle",
            path_mutation(
                r + ("uniform_physical_face_empty_audit",
                     "family_child_stage_boundary_rows", 0,
                     "BYPASS_designated_b3_used_as_collision_angle"),
                True,
            ),
        ),
        (
            "along diagnostic used",
            path_mutation(
                r + ("uniform_physical_face_empty_audit",
                     "family_child_stage_boundary_rows", 0,
                     "along_seed_diagnostic_only_not_F11_field_value"),
                False,
            ),
        ),
        (
            "five-face row delete",
            lambda d: get_path(
                d, r + ("physical_five_face_grammar_rows",)
            ).pop(),
        ),
        (
            "seven-boundary incidence",
            path_mutation(
                r + ("physical_seven_boundary_kind_rows", 0,
                     "actual_instance_count"),
                1,
            ),
        ),
        (
            "artificial count",
            path_mutation(
                r + ("parameterized_artificial_face_registry",
                     "artificial_face_template_count"),
                24,
            ),
        ),
        (
            "artificial retained",
            path_mutation(
                r + ("parameterized_artificial_face_registry",
                     "artificial_faces_retained_despite_physical_empty_statement"),
                False,
            ),
        ),
        (
            "moving physical kind",
            path_mutation(
                r + ("parameterized_artificial_face_registry",
                     "moving_artificial_face_template_rows", 0, "face_kind"),
                "PHYSICAL_FACE",
            ),
        ),
        (
            "moving artificial flag",
            path_mutation(
                r + ("parameterized_artificial_face_registry",
                     "moving_artificial_face_template_rows", 0,
                     "artificial_not_physical"),
                False,
            ),
        ),
        (
            "moving lambda-s merge",
            path_mutation(
                r + ("parameterized_artificial_face_registry",
                     "moving_artificial_face_template_rows", 0,
                     "lambda_and_s_are_distinct_parameters"),
                False,
            ),
        ),
        (
            "trace physical",
            path_mutation(
                r + ("parameterized_artificial_face_registry",
                     "artificial_trace_template_rows", 0,
                     "artificial_not_physical"),
                False,
            ),
        ),
        (
            "incidence physical",
            path_mutation(
                r + ("parameterized_artificial_face_registry",
                     "child_face_incidence_template_rows", 0,
                     "physical_face_incidence_count"),
                1,
            ),
        ),
        (
            "base duplicate",
            lambda d: get_path(
                d, r + ("parameterized_base_key_template_rows",)
            ).__setitem__(
                1, copy.deepcopy(get_path(
                    d, r + ("parameterized_base_key_template_rows", 0)
                ))
            ),
        ),
        (
            "base word",
            path_mutation(
                r + ("parameterized_base_key_template_rows", 0,
                     "official_word_key_id"),
                OFFICIAL_WORDS[1],
            ),
        ),
        (
            "base actual false",
            path_mutation(
                r + ("parameterized_base_key_template_rows", 0,
                     "per_exact_lambda_fibre_actual_base_key_exists"),
                False,
            ),
        ),
        (
            "field delete",
            lambda d: get_path(
                d, r + ("parameterized_F1_F13_F16_slot_template_rows",)
            ).pop(),
        ),
        (
            "field duplicate",
            lambda d: get_path(
                d, r + ("parameterized_F1_F13_F16_slot_template_rows",)
            ).__setitem__(
                1, copy.deepcopy(get_path(
                    d, r + ("parameterized_F1_F13_F16_slot_template_rows", 0)
                ))
            ),
        ),
        (
            "field index F14",
            path_mutation(
                r + ("parameterized_F1_F13_F16_slot_template_rows", 0,
                     "field_index"),
                14,
            ),
        ),
        (
            "field actual false",
            path_mutation(
                r + ("parameterized_F1_F13_F16_slot_template_rows", 0,
                     "per_exact_lambda_fibre_actual_slot_certified"),
                False,
            ),
        ),
        (
            "F11 along used",
            path_mutation(
                r + ("uniform_field_theorems",
                     "F11_along_curve_diagnostics_not_used_as_field_values"),
                False,
            ),
        ),
        (
            "F11 envelope",
            path_mutation(
                r + ("uniform_field_theorems",
                     "F11_full_phase_stage_strict_upper", "0"),
                "1",
            ),
        ),
        (
            "F6 global",
            path_mutation(
                r + ("uniform_field_theorems",
                     "F6_arbitrary_return_depth_or_global_all_record_claim"),
                True,
            ),
        ),
        (
            "whole-family finite child count",
            path_mutation(
                r + ("count_ledger", "whole_family_actual_child_row_count"),
                24,
            ),
        ),
        (
            "template slot count",
            path_mutation(
                r + ("count_ledger", "finite_field_slot_template_row_count"),
                1679,
            ),
        ),
        (
            "F14 local promotion",
            path_mutation(
                r + ("local_field_status", "F14"),
                "CERTIFIED_ON_EVERY_EXACT_LAMBDA_FIBRE_AND_ALL_24_COMMON_RANKS",
            ),
        ),
        (
            "local maturity promotion",
            path_mutation(
                r + ("positive_Borel_family_local_field_maturity",), "18/18"
            ),
        ),
        (
            "Gate5 promotion",
            path_mutation(r + ("gate5_global_maturity",), "18/18"),
        ),
        (
            "global block promotion",
            path_mutation(r + ("global_complete_18_field_block_count",), 1),
        ),
        (
            "CM2 promotion",
            path_mutation(r + ("cm2_verdict",), "GO_FOR_CLAIM"),
        ),
        (
            "scope promotion",
            path_mutation(r + ("strict_scope",), "global complete theorem"),
        ),
        (
            "nonclaim delete",
            lambda d: get_path(d, r + ("strict_nonclaims",)).pop(),
        ),
    ]

    rejected: list[str] = []
    for label, mutate in attacks:
        attack = copy.deepcopy(document)
        mutate(attack)
        resign_document(attack)
        try:
            validate_document(attack, documents, core)
        except (
            VerificationError, KeyError, IndexError, TypeError, ValueError,
        ):
            rejected.append(label)
        else:
            raise VerificationError(f"semantic mutation accepted:{label}")
    return rejected


def strict_json_attacks(
    raw: bytes,
    document: dict[str, Any],
    documents: dict[int, dict[str, dict[str, Any]]],
    core: dict[str, Any],
) -> list[str]:
    text = raw.decode("utf-8")
    attacks: list[tuple[str, bytes]] = [
        (
            "duplicate top schema",
            text.replace(
                '"schema": "cm2.round129.rank3-positive-borel-recut-field-bridge.v1"',
                '"schema": "x", "schema": '
                '"cm2.round129.rank3-positive-borel-recut-field-bridge.v1"',
                1,
            ).encode(),
        ),
        (
            "duplicate nested precision",
            text.replace(
                '"precision_bits": 4096',
                '"precision_bits": 4096, "precision_bits": 4096',
                1,
            ).encode(),
        ),
        (
            "JSON float",
            text.replace('"precision_bits": 4096', '"precision_bits": 4096.0', 1)
            .encode(),
        ),
        (
            "JSON exponent",
            text.replace('"precision_bits": 4096', '"precision_bits": 4e3', 1)
            .encode(),
        ),
        (
            "NaN",
            text.replace('"precision_bits": 4096', '"precision_bits": NaN', 1)
            .encode(),
        ),
        (
            "Infinity",
            text.replace('"precision_bits": 4096', '"precision_bits": Infinity', 1)
            .encode(),
        ),
        ("UTF-8 BOM", b"\xef\xbb\xbf" + raw),
        ("invalid UTF-8", raw + b"\xff"),
        (
            "negative zero",
            text.replace('"precision_bits": 4096', '"precision_bits": -0', 1)
            .encode(),
        ),
        (
            "oversized integer",
            text.replace(
                '"precision_bits": 4096',
                '"precision_bits": 999999999999999999999999999999',
                1,
            ).encode(),
        ),
        (
            "unpaired surrogate",
            text.replace(
                CERTIFICATE_SCHEMA,
                CERTIFICATE_SCHEMA + r"\ud800",
                1,
            ).encode(),
        ),
        ("top array", b"[]"),
    ]
    extra_top = copy.deepcopy(document)
    extra_top["extra"] = 1
    attacks.append(("closed envelope extra key", canonical(extra_top).encode()))
    extra_result = copy.deepcopy(document)
    extra_result["result"]["extra"] = True
    resign_document(extra_result)
    attacks.append(("closed result extra key", canonical(extra_result).encode()))
    stale = copy.deepcopy(document)
    stale["result"]["precision_bits"] = 3072
    attacks.append(("stale outer digest", canonical(stale).encode()))
    noncanonical = copy.deepcopy(document)
    noncanonical["result"]["positive_Borel_family_root_contract"][
        "fixed_c0"
    ] = "2/32768"
    resign_document(noncanonical)
    attacks.append(("noncanonical fraction", canonical(noncanonical).encode()))

    rejected: list[str] = []
    for label, attack in attacks:
        try:
            candidate = parse_bytes(attack)
            validate_document(candidate, documents, core)
        except (
            VerificationError, UnicodeDecodeError, json.JSONDecodeError,
            KeyError, IndexError, TypeError, ValueError,
        ):
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    return rejected


def safe_input_path(path: Path) -> None:
    require(path.is_file() and not path.is_symlink(), "certificate regular file")
    require(path.resolve().parent.is_dir(), "certificate parent")
    protected = [PRODUCER, VERIFIER, *[HERE / name for name in {
        **UPSTREAM_PINS, **MATH_HELPER_PINS
    }]]
    for protected_path in protected:
        try:
            require(
                not os.path.samefile(path, protected_path),
                "certificate aliases protected source",
            )
        except FileNotFoundError:
            pass
    if path.resolve() != CERTIFICATE.resolve():
        try:
            require(
                not os.path.samefile(path, CERTIFICATE),
                "certificate hardlink alias forbidden",
            )
        except FileNotFoundError:
            pass


def safe_output_path(path: Path, certificate_path: Path) -> None:
    require(path.parent.resolve().is_dir(), "output parent directory")
    protected = [
        PRODUCER, VERIFIER, CERTIFICATE, certificate_path,
        *[HERE / name for name in {**UPSTREAM_PINS, **MATH_HELPER_PINS}],
    ]
    candidate = (path.parent.resolve() / path.name).resolve()
    require(
        all(candidate != protected_path.resolve() for protected_path in protected),
        "output aliases protected path",
    )
    if path.exists() or path.is_symlink():
        require(not path.is_symlink(), "output symlink forbidden")
        require(stat.S_ISREG(path.stat().st_mode), "output regular file")
        for protected_path in protected:
            try:
                require(
                    not os.path.samefile(path, protected_path),
                    "output hardlink to protected input/source forbidden",
                )
            except FileNotFoundError:
                pass


def verification_result(
    document: dict[str, Any],
    summary: dict[str, Any],
    core: dict[str, Any],
    mutation_labels: list[str],
    strict_labels: list[str],
) -> dict[str, Any]:
    physical_minima = core["physical"]["independent_strict_lower_minima"]
    return {
        "verdict": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": document["result_sha256"],
        "producer_sha256": PRODUCER_SHA256,
        "verifier_sha256": sha256(VERIFIER),
        "verification_precision_bits": VERIFIER_PRECISION_BITS,
        "independence_contract": {
            "Round129_producer_imported_or_executed": False,
            "lambda_root_sheet_independently_rebuilt": True,
            "symbolic_Flambda_equals_32_over_625_times_lambda_checked": True,
            "monotone_b_image_independently_rebuilt": True,
            "Round122_independent_Jet2_math_layer_reused_under_byte_pin": True,
            "joint_lambda_by_s_physical_replay": True,
            "certificate_template_IDs_and_crosslinks_independently_rebuilt": True,
        },
        "independent_geometry": {
            "lambda_collar": [qstr(LAMBDA_LOWER), qstr(LAMBDA_UPPER)],
            "uniform_t_guard": core["t_guard"],
            "uniform_root_face_signs": core["face_signs"],
            "b_image_length_strict_lower_exact":
                core["b_image_length_lower"],
            "pullback_face_count": len(core["faces"]),
            "pullback_face_order": [
                f"S{row['stage']}:{row['natural_index_j']}"
                for row in core["faces"]
            ],
            "minimum_24_child_gap_strict_lower": core["minimum_gap"],
            "physical_candidate_stage_counts": [57, 55, 57],
            "physical_candidate_total_per_rank": 169,
            "physical_candidate_total_all_24_ranks": 4056,
            "physical_independent_strict_lower_minima": physical_minima,
            "physical_five_face_incidence_count": 0,
        },
        "registry_summary": summary,
        "semantic_resigned_mutation_count": len(mutation_labels),
        "semantic_resigned_mutation_rejection_labels": mutation_labels,
        "strict_json_attack_count": len(strict_labels),
        "strict_json_attack_rejection_labels": strict_labels,
        "fail_closed_safety": {
            "positive_Borel_local_maturity": "14/18",
            "global_Gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        safe_input_path(args.certificate)
        safe_output_path(args.output, args.certificate)
        require(sha256(args.certificate) == CERTIFICATE_SHA256,
                "official certificate byte pin")
        raw = args.certificate.read_bytes()
        document = parse_bytes(raw)
        require(
            document["result_sha256"] == CERTIFICATE_RESULT_SHA256,
            "official certificate result pin",
        )
        documents = validate_pins()
        core = independent_math_core(documents)
        summary = validate_document(document, documents, core)
        mutation_labels = semantic_mutations(document, documents, core)
        strict_labels = strict_json_attacks(
            raw, document, documents, core
        )
        result = verification_result(
            document, summary, core, mutation_labels, strict_labels
        )
        envelope = {
            "schema": VERIFICATION_SCHEMA,
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
        print("PASS")
        print(f"semantic_resigned_mutations={len(mutation_labels)}")
        print(f"strict_json_attacks={len(strict_labels)}")
        print(f"result_sha256={envelope['result_sha256']}")
        return 0
    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
