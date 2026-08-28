#!/usr/bin/env python3
"""Independent verifier for the final Round123 stage-3/F14 certificate.

The verifier does not import the Round123 producer, its common module, the
diagnostic spike, or the provisional frontier.  The only reused geometry
implementation is the byte-pinned independent Round121 verifier.  From it we
rebuild the exact seed, the three physical images, all 192 third-image
natural-cut roots, the 215-cut common refinement, the 216 output members, and
the 72 one-leg output rows.  The Round122 certificate is parsed and pinned as
data so that the F10/F13/F16 full-key crosswalk is checked independently.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_round121_rank3_exact_seed_three_leg_recut_f5f6_verifier as v121


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = (
    HERE
    / "cm2-round123-rank3-exact-seed-stage3-output-properization-f14-2026-07-23.json"
)
DEFAULT_OUTPUT = (
    HERE
    / "cm2-round123-rank3-exact-seed-stage3-output-properization-f14-verification-2026-07-23.json"
)
CERTIFICATE_SCHEMA = (
    "cm2.round123.rank3-exact-seed-stage3-output-properization-f14.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round123.rank3-exact-seed-stage3-output-properization-f14-verification.v1"
)
VERIFIER_BITS = 3072

ROUND121 = (
    HERE
    / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
)
ROUND122 = (
    HERE
    / "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json"
)
ROUND121_PRODUCER = (
    HERE / "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py"
)
ROUND121_VERIFIER = (
    HERE / "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6_verifier.py"
)
ROUND122_PRODUCER = (
    HERE / "cm2_round122_rank3_exact_seed_physical_face_field_bridge.py"
)
ROUND122_VERIFIER = (
    HERE / "cm2_round122_rank3_exact_seed_physical_face_field_bridge_verifier.py"
)
ROUND122_VERIFICATION = (
    HERE
    / "cm2-round122-rank3-exact-seed-physical-face-field-bridge-verification-2026-07-23.json"
)
ROUND122_MANIFEST = (
    HERE / "cm2-one-hundred-twenty-second-direct-assault-manifest-2026-07-23.sha256"
)

ROUND121_SHA256 = (
    "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e"
)
ROUND121_PRODUCER_SHA256 = (
    "30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed"
)
ROUND121_VERIFIER_SHA256 = (
    "d35c0e04b9d339c1271533abdefa5addcb73096b70abdec94d60e475daa45e95"
)
ROUND122_SHA256 = (
    "a7ed51149916bbf0d181b9cd45114cd11d81a5d30e72fea50b3336d1ead22028"
)
ROUND122_PRODUCER_SHA256 = (
    "44a64789635b8adfb597376d25afcbf8cb39dbaf0c2a19c4031bcbe78b3848f4"
)
ROUND122_VERIFIER_SHA256 = (
    "bcf6e34398dcd2fd4cb6bb23aec649db5df75d26a80f307e58521d8ef439d31e"
)
ROUND122_VERIFICATION_SHA256 = (
    "aa0eca5e14fccbeeaad74d075cce0f10ee01f4caf8fccd0e9130ccc0e5cba82b"
)
ROUND122_MANIFEST_SHA256 = (
    "b78e37b17c1c3f5dd677aa669a2d4bdf71504b1a98bf988cae0144e6d81457bb"
)

EXPECTED_PINS = {
    "deliverables/cm2_round123_rank3_exact_seed_stage3_output_properization_common.py": (
        "8eda085e342655f20ef68a7aa0554b3bed3c26312d1261c49d4f6567d0bbb9e0"
    ),
    "deliverables/cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py": (
        ROUND121_PRODUCER_SHA256
    ),
    "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json": (
        ROUND121_SHA256
    ),
    "deliverables/cm2_round121_rank3_exact_seed_three_leg_recut_f5f6_verifier.py": (
        ROUND121_VERIFIER_SHA256
    ),
    "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json": (
        "ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80"
    ),
    "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-report-2026-07-23.md": (
        "8db9291b0eb679b6137d18ccc1e5254a79efbb7e0e2a085042aada1f93754f8d"
    ),
    "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-cold-replay-2026-07-23.md": (
        "e670b24f4939d39df4cc84591aad4213bbc80e3ffb3cbe1899d81ef83fe9b11b"
    ),
    "deliverables/cm2-one-hundred-twenty-first-direct-assault-2026-07-23.md": (
        "4f14877dfb39362d2b3607922ec2eb65628271aaf9a1392b31abfec0bd369cc0"
    ),
    "deliverables/cm2-one-hundred-twenty-first-direct-assault-manifest-2026-07-23.sha256": (
        "e53ad73d4e7120c2ce4f30c49f83f29d4d2b99a5f8a451f9085e5fb473959b83"
    ),
    "deliverables/cm2_round122_rank3_exact_seed_physical_face_field_bridge.py": (
        ROUND122_PRODUCER_SHA256
    ),
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json": (
        ROUND122_SHA256
    ),
    "deliverables/cm2_round122_rank3_exact_seed_physical_face_field_bridge_verifier.py": (
        ROUND122_VERIFIER_SHA256
    ),
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-verification-2026-07-23.json": (
        ROUND122_VERIFICATION_SHA256
    ),
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-report-2026-07-23.md": (
        "137d2be2729ccdd5b01ed379fd611575e871e94d8d2af32fbf1a6fe62feac00f"
    ),
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-cold-replay-2026-07-23.md": (
        "ccdc04d1463ba9ce6c391085eb7b9e75d316403ef71ec28f056cdc82d062e16c"
    ),
    "deliverables/cm2-one-hundred-twenty-second-direct-assault-2026-07-23.md": (
        "97a9911706aaad0ca18a67d1840f63c81c177c3f4c35cc62ec3f3c4a0847cfef"
    ),
    "deliverables/cm2-one-hundred-twenty-second-direct-assault-manifest-2026-07-23.sha256": (
        ROUND122_MANIFEST_SHA256
    ),
    "deliverables/cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
    "deliverables/cm2_gate5_return_word_three_norm_frontier_cert.py": (
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695"
    ),
    "deliverables/cm2_gate5_return_word_three_norm_frontier_verifier.py": (
        "0384acdd1f912b0d4b3bee84ff530358d9693893d1c5c64a1deabaede8e0867b"
    ),
    "deliverables/cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py": (
        "01e32ca209818f4077443a7692622c4202ab7f1066e2f95802185e2be7a2cc9a"
    ),
    "deliverables/cm2_gate4_numeric_invariant_family_growth_recovery_frontier_verifier.py": (
        "8074da51347aec415a864d87dc349cff25afa5a9a239febc53cc1ab015763d05"
    ),
    "deliverables/cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json": (
        "3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3"
    ),
    "deliverables/cm2_gate4_inner_core_strong_product_bridge_frontier_cert.py": (
        "4720669e90824e8c630276aa3d73606435eb88da2a51b2a756f651f56071605a"
    ),
    "deliverables/cm2_gate4_inner_core_strong_product_bridge_frontier_verifier.py": (
        "1c814f82231c8a0181d53ec28f09d07c2528d40eda82a425b280a2858b0c0862"
    ),
    "deliverables/cm2-round88-gate5-f14-regalpha-strong-install-2026-07-22.json": (
        "80e4ba31fb86b51410e90a5e1ef561f565cede65ef56792fc40364235d652993"
    ),
}

DELTA = Q(1, 10**90)
Q_REGULARITY = Q(93, 100)
THETA_INVERSE = Q(144000, 180337)
DISTORTION_CJ = 15000000000000000000000000
REGULAR_DENSITY_CONE_K = 500000000000000000000000000
DISTORTION_ONLY_CONSTANT = 13950000000000000000000001
F14_ONE_STEP = 34
F14_GENERIC_THREE_LEG = 39304
F14_DIRECT_THREE_LEG = 34

RESULT_KEYS = {
    "accepted_norm_leg_output_rows",
    "accepted_norm_leg_output_rows_sha256",
    "arbitrary_density_and_Jordan_contract",
    "cm2_verdict",
    "combined_F1_F14_F16_slot_registry",
    "complete_18_field_block_count",
    "count_ledger",
    "derived_count_ledger",
    "gate5_F14_slot_rows",
    "gate5_F14_slot_rows_sha256",
    "gate5_actual_child_field_status",
    "gate5_block_count",
    "gate5_global_maturity",
    "input_child_output_partition_rows",
    "input_child_output_partition_rows_sha256",
    "merged_cut_spacing_audit",
    "merged_internal_cut_rows",
    "merged_internal_cut_rows_sha256",
    "precision_bits",
    "rank3_seed_child_field_maturity",
    "remaining_uninstalled_child_fields",
    "root_bisections",
    "round121_contract",
    "round122_contract",
    "stage3_adapted_coordinate_contract",
    "stage3_endpoint_rows",
    "stage3_endpoint_rows_sha256",
    "stage3_natural_cell_rows",
    "stage3_natural_cell_rows_sha256",
    "stage3_output_fragment_rows",
    "stage3_output_fragment_rows_sha256",
    "stagewise_output_length_theorem",
    "status",
    "strict_nonclaims",
    "strict_scope",
    "upstream_and_helper_pins",
}


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


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_constant(token: str) -> Any:
    raise ValueError(f"non-finite JSON number:{token}")


def reject_float(token: str) -> Any:
    raise ValueError(f"JSON float forbidden:{token}")


def strict_integer(token: str) -> int:
    if token == "-0":
        raise ValueError("negative zero forbidden")
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
    if text.startswith("\ufeff"):
        raise ValueError("BOM forbidden")
    value = json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_constant=reject_constant,
        parse_float=reject_float,
        parse_int=strict_integer,
    )
    require(type(value) is dict, "top-level JSON object")
    reject_surrogates(value)
    return value


def qvalue(value: Any, label: str) -> Q:
    require(type(value) is str, f"{label}:fraction type")
    require(
        re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", value)
        is not None,
        f"{label}:canonical fraction syntax",
    )
    result = Q(value)
    require(str(result) == value, f"{label}:reduced fraction")
    return result


def row_digest(row: dict[str, Any]) -> str:
    return digest(
        {key: value for key, value in row.items() if key != "row_sha256"}
    )


def interval_pair(value: arb) -> tuple[Q, Q]:
    return v121.arb_pair(value)


def stored_contains(stored: Any, fresh: arb, label: str) -> None:
    require(
        type(stored) is list and len(stored) == 2,
        f"{label}:stored interval",
    )
    lower = qvalue(stored[0], f"{label}:lower")
    upper = qvalue(stored[1], f"{label}:upper")
    fresh_lower, fresh_upper = interval_pair(fresh)
    require(
        lower <= fresh_lower <= fresh_upper <= upper,
        f"{label}:fresh interval containment",
    )


def load_envelope(
    path: Path, expected_sha: str, schema: str
) -> dict[str, Any]:
    require(sha256(path) == expected_sha, f"{path.name}:byte pin")
    document = strict_json(path.read_text(encoding="utf-8"))
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"{path.name}:closed envelope",
    )
    require(document["schema"] == schema, f"{path.name}:schema")
    require(
        document["result_sha256"] == digest(document["result"]),
        f"{path.name}:result digest",
    )
    return document["result"]


def load_inputs() -> dict[str, Any]:
    require(
        sha256(ROUND121_PRODUCER) == ROUND121_PRODUCER_SHA256,
        "Round121 producer pin",
    )
    require(
        sha256(ROUND121_VERIFIER) == ROUND121_VERIFIER_SHA256,
        "Round121 independent verifier pin",
    )
    require(
        sha256(ROUND122_PRODUCER) == ROUND122_PRODUCER_SHA256,
        "Round122 producer pin",
    )
    require(
        sha256(ROUND122_VERIFIER) == ROUND122_VERIFIER_SHA256,
        "Round122 independent verifier pin",
    )
    require(
        sha256(ROUND122_VERIFICATION) == ROUND122_VERIFICATION_SHA256,
        "Round122 verification pin",
    )
    require(
        sha256(ROUND122_MANIFEST) == ROUND122_MANIFEST_SHA256,
        "Round122 manifest pin",
    )
    r121 = load_envelope(
        ROUND121,
        ROUND121_SHA256,
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
    )
    r122 = load_envelope(
        ROUND122,
        ROUND122_SHA256,
        "cm2.round122.rank3-exact-seed-physical-face-field-bridge.v1",
    )
    require(
        r122["rank3_seed_child_field_maturity"] == "14/18"
        and r122["combined_F1_F13_F16_slot_registry"][
            "combined_slot_count"
        ]
        == 1680,
        "Round122 certified bridge status",
    )
    return {"r121": r121, "r122": r122}


def source_boundary_id(which: str, seed_id: str) -> str:
    require(which in {"left", "right"}, "source boundary side")
    return f"round121-source-{which}-endpoint:" + digest(
        ["round121-source-boundary-v1", seed_id, which]
    )


def endpoint_id(seed_id: str, level: int) -> str:
    return "round123-stage3-endpoint:" + digest(
        [
            "round123-stage3-output-level-root-v0",
            seed_id,
            "actual-third-chart:N",
            "orientation:U3=a3(0)-a3(x)",
            f"U3={level}*delta",
        ]
    )


def stage3_cell_id(seed_id: str, natural_index: int) -> str:
    return "round123-stage3-output-natural-cell:" + digest(
        [
            "round123-stage3-output-natural-cell-v0",
            seed_id,
            "actual-third-chart:N",
            "orientation:U3=a3(0)-a3(x)",
            natural_index,
        ]
    )


def output_fragment_id(
    seed_id: str,
    child_id: str,
    lower_id: str,
    upper_id: str,
    stage3_index: int,
) -> str:
    return "round123-stage3-output-fragment:" + digest(
        [
            "round123-stage3-output-fragment-v0",
            seed_id,
            child_id,
            lower_id,
            upper_id,
            stage3_index,
        ]
    )


def leg_output_row_id(seed_id: str, child_id: str, leg_index: int) -> str:
    return "round123-leg-output:" + digest(
        [
            "round123-accepted-norm-leg-output-v0",
            seed_id,
            child_id,
            leg_index,
        ]
    )


def image_member_id(seed_id: str, child_id: str, stage: int) -> str:
    return "round123-image-member:" + digest(
        [
            "round123-existing-common-child-image-member-v0",
            seed_id,
            child_id,
            stage,
        ]
    )


def f14_slot_id(immutable_key: list[Any]) -> str:
    return "round123-gate5-f14-slot:" + digest(
        ["round123-gate5-f14-slot-v1", immutable_key]
    )


def a3(theta_star: arb, x: arb, differentiated: bool) -> v121.Dual:
    state = v121.source_and_collisions(theta_star, x, differentiated)
    actual = state["actual_third"]
    return (
        v121.Dual(arb.pi() / 2)
        - actual[4].asin()
        + actual[6].asin()
    )


def u3_value(
    theta_star: arb, a3_zero: arb, lower: Q, upper: Q
) -> arb:
    return a3_zero - a3(
        theta_star, v121.interval(lower, upper), False
    ).value


def independent_geometry() -> dict[str, Any]:
    values = v121.load_inputs()
    indexes = v121.seed_indexes(values)
    anchor = v121.isolate_anchor(indexes)
    theta_star = anchor["theta_ball"]
    state0 = v121.source_and_collisions(theta_star, arb(0), False)
    a3_zero = a3(theta_star, arb(0), False).value
    a3_one = a3(theta_star, arb(1), False).value
    whole = a3(theta_star, v121.interval(Q(0), Q(1)), True)
    delta = v121.aq(DELTA)
    ratio = (a3_zero - a3_one) / delta
    derivative_ratio = -whole.derivative / delta
    ratio_lower, ratio_upper = interval_pair(ratio)
    derivative_lower, derivative_upper = interval_pair(derivative_ratio)
    require(
        Q(192) < ratio_lower <= ratio_upper < Q(193),
        "independent U3 length",
    )
    require(
        Q(192) < derivative_lower <= derivative_upper < Q(193),
        "independent U3 derivative",
    )
    return {
        "theta_star": theta_star,
        "a3_zero": a3_zero,
        "ratio": ratio,
        "derivative_ratio": derivative_ratio,
        "ratio_pair": (ratio_lower, ratio_upper),
        "derivative_pair": (derivative_lower, derivative_upper),
        "u1_zero": state0["a1"].value,
        "u2_zero": state0["a2"].value,
    }


def stage_u_value(
    geometry: dict[str, Any], stage: int, lower: Q, upper: Q
) -> arb:
    require(stage in {1, 2, 3}, "stage adapted coordinate")
    if stage == 3:
        return u3_value(
            geometry["theta_star"], geometry["a3_zero"], lower, upper
        )
    state = v121.source_and_collisions(
        geometry["theta_star"], v121.interval(lower, upper), False
    )
    if stage == 1:
        return geometry["u1_zero"] - state["a1"].value
    return state["a2"].value - geometry["u2_zero"]


def verify_coordinate_contract(
    result: dict[str, Any], geometry: dict[str, Any]
) -> None:
    contract = result["stage3_adapted_coordinate_contract"]
    require(
        set(contract)
        == {
            "U3",
            "U3_1_over_delta_strict_enclosure",
            "a3",
            "actual_third_collision_chart",
            "actual_third_owner",
            "normalized_U3_derivative_strict_enclosure",
            "orientation",
            "simple_length_bound",
        },
        "closed stage3 coordinate contract",
    )
    require(
        contract["a3"] == "pi/2-asin(n3_x)+asin(p3)"
        and contract["U3"] == "a3(0)-a3(x)",
        "stage3 coordinate formula",
    )
    require(
        contract["actual_third_collision_chart"] == "N"
        and contract["actual_third_owner"] == "G[-1,-2]"
        and contract["orientation"] == "STRICTLY_INCREASING_U3"
        and contract["simple_length_bound"] == "192<U3(1)/delta<193",
        "stage3 owner/chart/orientation",
    )
    stored_contains(
        contract["U3_1_over_delta_strict_enclosure"],
        geometry["ratio"],
        "stored U3 length",
    )
    stored_contains(
        contract["normalized_U3_derivative_strict_enclosure"],
        geometry["derivative_ratio"],
        "stored U3 derivative",
    )


def verify_endpoints(
    result: dict[str, Any],
    r121: dict[str, Any],
    geometry: dict[str, Any],
) -> None:
    rows = result["stage3_endpoint_rows"]
    require(type(rows) is list and len(rows) == 192, "192 stage3 roots")
    require(
        result["stage3_endpoint_rows_sha256"] == digest(rows),
        "stage3 roots digest",
    )
    seed_id = r121["exact_seed_contract"]["exact_parent_W_seed_id"]
    seen: set[str] = set()
    prior_upper = Q(0)
    delta = v121.aq(DELTA)
    for level, row in enumerate(rows, 1):
        require(
            type(row) is dict
            and set(row)
            == {
                "actual_third_chart",
                "endpoint_id",
                "exact_root_equation",
                "exact_root_equation_id",
                "left_function_sign",
                "lower_owner",
                "natural_index_j",
                "normalized_derivative_strict_enclosure",
                "numeric_bracket_participates_in_ID",
                "orientation",
                "right_function_sign",
                "row_sha256",
                "stage",
                "unique_root_certified",
                "upper_owner",
                "x_bracket_width",
                "x_dyadic_bracket",
            },
            f"closed stage3 root row:{level}",
        )
        identifier = endpoint_id(seed_id, level)
        require(
            row["endpoint_id"] == identifier
            and identifier not in seen
            and row["stage"] == 3
            and row["natural_index_j"] == level,
            f"stage3 root identity:{level}",
        )
        seen.add(identifier)
        require(
            row["exact_root_equation_id"]
            == f"round123-U3-equals-{level}-delta"
            and row["exact_root_equation"] == f"U3(x)={level}*10^-90"
            and row["actual_third_chart"] == "N"
            and row["orientation"] == "U3(x)=a3(0)-a3(x)",
            f"stage3 root equation:{level}",
        )
        bracket = row["x_dyadic_bracket"]
        require(
            type(bracket) is list and len(bracket) == 2,
            f"stage3 root bracket:{level}",
        )
        lower = qvalue(bracket[0], f"stage3 root lower:{level}")
        upper = qvalue(bracket[1], f"stage3 root upper:{level}")
        require(
            prior_upper < lower < upper < 1,
            f"strict stage3 root order:{level}",
        )
        prior_upper = upper
        require(
            qvalue(row["x_bracket_width"], f"root width:{level}")
            == upper - lower,
            f"root width identity:{level}",
        )
        target = v121.aq(Q(level) * DELTA)
        left = (
            u3_value(
                geometry["theta_star"],
                geometry["a3_zero"],
                lower,
                lower,
            )
            - target
        )
        right = (
            u3_value(
                geometry["theta_star"],
                geometry["a3_zero"],
                upper,
                upper,
            )
            - target
        )
        require(
            v121.strict_sign(left) == -1
            and v121.strict_sign(right) == 1,
            f"stage3 root signs:{level}",
        )
        derivative = (
            -a3(
                geometry["theta_star"],
                v121.interval(lower, upper),
                True,
            ).derivative
            / delta
        )
        dlow, dhigh = interval_pair(derivative)
        require(
            Q(192) < dlow <= dhigh < Q(193),
            f"stage3 root uniqueness:{level}",
        )
        stored_contains(
            row["normalized_derivative_strict_enclosure"],
            derivative,
            f"stored stage3 root derivative:{level}",
        )
        require(
            row["left_function_sign"] == -1
            and row["right_function_sign"] == 1
            and row["unique_root_certified"] is True
            and row["numeric_bracket_participates_in_ID"] is False
            and row["lower_owner"] == f"stage-3-natural-cell-{level - 1}"
            and row["upper_owner"] == f"stage-3-natural-cell-{level}"
            and row["row_sha256"] == row_digest(row),
            f"stage3 root contract:{level}",
        )


def verify_natural_cells(
    result: dict[str, Any], r121: dict[str, Any]
) -> None:
    rows = result["stage3_natural_cell_rows"]
    roots = result["stage3_endpoint_rows"]
    require(type(rows) is list and len(rows) == 193, "193 stage3 cells")
    require(
        result["stage3_natural_cell_rows_sha256"] == digest(rows),
        "stage3 cell digest",
    )
    seed_id = r121["exact_seed_contract"]["exact_parent_W_seed_id"]
    endpoints = [
        source_boundary_id("left", seed_id),
        *(row["endpoint_id"] for row in roots),
        source_boundary_id("right", seed_id),
    ]
    ratio_lower, ratio_upper = (
        qvalue(value, "stored terminal stage3 length")
        for value in result["stage3_adapted_coordinate_contract"][
            "U3_1_over_delta_strict_enclosure"
        ]
    )
    for index, row in enumerate(rows):
        full = index < 192
        require(
            row["stage"] == 3
            and row["natural_index_j"] == index
            and row["recut_instance_id"] == stage3_cell_id(seed_id, index)
            and row["adapted_coordinate_id"]
            == "round123-U3-north-chart-output",
            f"stage3 cell identity:{index}",
        )
        require(
            row["adapted_lower"] == f"{index}*delta"
            and row["adapted_upper"]
            == (f"{index + 1}*delta" if full else "U3(1)")
            and row["lower_endpoint_id"] == endpoints[index]
            and row["upper_endpoint_id"] == endpoints[index + 1],
            f"stage3 cell endpoints:{index}",
        )
        expected_length = (
            [Q(1), Q(1)]
            if full
            else [ratio_lower - 192, ratio_upper - 192]
        )
        require(
            [
                qvalue(value, f"stage3 cell length:{index}")
                for value in row["normalized_adapted_length_enclosure"]
            ]
            == expected_length,
            f"stage3 cell length identity:{index}",
        )
        require(
            row["lower_closed"] is True
            and row["upper_closed"] is False
            and row["internal_cut_is_owned_by_right_cell"] is True
            and row["source_parent_right_endpoint_remains_open"] is True
            and row["full_delta_cell"] is full
            and row["terminal_partial_cell"] is (not full)
            and row["actual_third_owner"] == "G[-1,-2]"
            and row["actual_third_collision_chart"] == "N"
            and row["row_sha256"] == row_digest(row),
            f"stage3 cell ownership:{index}",
        )


def verify_merged_cuts(
    result: dict[str, Any],
    r121: dict[str, Any],
    geometry: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = result["merged_internal_cut_rows"]
    require(type(rows) is list and len(rows) == 215, "215 merged cuts")
    require(
        result["merged_internal_cut_rows_sha256"] == digest(rows),
        "merged cut digest",
    )
    old = {
        row["endpoint_id"]: row for row in r121["pullback_endpoint_rows"]
    }
    new = {
        row["endpoint_id"]: row for row in result["stage3_endpoint_rows"]
    }
    require(len(old) == 23 and len(new) == 192, "cut source census")
    seen_old: set[str] = set()
    seen_new: set[str] = set()
    prior_upper = Q(0)
    gaps: list[Q] = []
    cross_gaps: list[Q] = []
    for row in rows:
        require(
            set(row)
            == {
                "endpoint_id",
                "natural_index_j",
                "origin",
                "stage",
                "u3_over_delta_enclosure",
                "x_dyadic_bracket",
            },
            "closed merged cut row",
        )
        lower = qvalue(row["x_dyadic_bracket"][0], "merged cut lower")
        upper = qvalue(row["x_dyadic_bracket"][1], "merged cut upper")
        require(prior_upper < lower < upper < 1, "strict merged cut order")
        if prior_upper:
            gaps.append(lower - prior_upper)
        prior_upper = upper
        identifier = row["endpoint_id"]
        if identifier in old:
            source = old[identifier]
            seen_old.add(identifier)
            require(
                row["origin"] == "ROUND121_EXISTING_INPUT_CUT"
                and row["stage"] == source["stage"]
                and row["natural_index_j"] == source["natural_index_j"]
                and row["x_dyadic_bracket"] == source["x_dyadic_bracket"],
                "merged Round121 cut crosswalk",
            )
            fresh = (
                u3_value(
                    geometry["theta_star"],
                    geometry["a3_zero"],
                    lower,
                    upper,
                )
                / v121.aq(DELTA)
            )
            stored_contains(
                row["u3_over_delta_enclosure"],
                fresh,
                "merged Round121 cut U3",
            )
        elif identifier in new:
            source = new[identifier]
            seen_new.add(identifier)
            level = source["natural_index_j"]
            require(
                row["origin"] == "ROUND123_STAGE3_OUTPUT_CUT"
                and row["stage"] == 3
                and row["natural_index_j"] == level
                and row["x_dyadic_bracket"] == source["x_dyadic_bracket"]
                and row["u3_over_delta_enclosure"]
                == [str(level), str(level)],
                "merged Round123 cut crosswalk",
            )
        else:
            raise RuntimeError("unknown merged cut")
    require(
        seen_old == set(old) and seen_new == set(new),
        "complete 23+192 merged census",
    )
    # Rebuild adjacent-gap types, including the cross-origin minimum.
    for left, right in zip(rows, rows[1:]):
        if left["origin"] != right["origin"]:
            cross_gaps.append(
                qvalue(right["x_dyadic_bracket"][0], "cross right")
                - qvalue(left["x_dyadic_bracket"][1], "cross left")
            )
    require(
        min(gaps) > Q(1, 6000)
        and min(cross_gaps) > Q(1, 6000),
        "merged cut separation >1/6000",
    )
    audit = result["merged_cut_spacing_audit"]
    require(
        audit["combined_internal_cut_count"] == 215
        and audit["all_cut_brackets_pairwise_strictly_ordered"] is True
        and qvalue(audit["minimum_combined_x_gap"], "stored minimum gap")
        == min(gaps)
        and qvalue(
            audit["minimum_x_gap_by_kind"]["CROSS_ORIGIN"]["gap"],
            "stored cross gap",
        )
        == min(cross_gaps),
        "merged spacing audit",
    )
    return rows


def refinement_boundaries(
    result: dict[str, Any], r121: dict[str, Any]
) -> list[dict[str, Any]]:
    seed_id = r121["exact_seed_contract"]["exact_parent_W_seed_id"]
    return [
        {
            "endpoint_id": source_boundary_id("left", seed_id),
            "origin": "SOURCE_OUTER_LEFT",
            "x_dyadic_bracket": ["0", "0"],
        },
        *result["merged_internal_cut_rows"],
        {
            "endpoint_id": source_boundary_id("right", seed_id),
            "origin": "SOURCE_OUTER_RIGHT",
            "x_dyadic_bracket": ["1", "1"],
        },
    ]


def verify_fragments_and_partitions(
    result: dict[str, Any],
    r121: dict[str, Any],
    geometry: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    rows = result["stage3_output_fragment_rows"]
    partitions = result["input_child_output_partition_rows"]
    require(type(rows) is list and len(rows) == 216, "216 output fragments")
    require(
        result["stage3_output_fragment_rows_sha256"] == digest(rows),
        "output fragment digest",
    )
    require(
        type(partitions) is list
        and len(partitions) == 24
        and result["input_child_output_partition_rows_sha256"]
        == digest(partitions),
        "24 output partitions",
    )
    children = sorted(
        r121["common_refinement_rows"], key=lambda row: row["common_rank"]
    )
    require(
        [row["common_rank"] for row in children] == list(range(24)),
        "Round121 common-child order",
    )
    seed_id = r121["exact_seed_contract"]["exact_parent_W_seed_id"]
    boundaries = refinement_boundaries(result, r121)
    input_rank = 0
    stage3_index = 0
    grouped: dict[int, list[dict[str, Any]]] = {
        index: [] for index in range(24)
    }
    for fragment_rank, (lower, upper, row) in enumerate(
        zip(boundaries, boundaries[1:], rows)
    ):
        lower_high = qvalue(
            lower["x_dyadic_bracket"][1], "fragment lower core"
        )
        upper_low = qvalue(
            upper["x_dyadic_bracket"][0], "fragment upper core"
        )
        require(lower_high < upper_low, "positive fragment source length")
        child = children[input_rank]
        expected_id = output_fragment_id(
            seed_id,
            child["common_child_id"],
            lower["endpoint_id"],
            upper["endpoint_id"],
            stage3_index,
        )
        require(
            row["fragment_rank"] == fragment_rank
            and row["output_fragment_id"] == expected_id
            and row["input_common_child_id"] == child["common_child_id"]
            and row["input_common_rank"] == input_rank
            and row["stage3_natural_index_j"] == stage3_index
            and row["stage3_output_recut_instance_id"]
            == stage3_cell_id(seed_id, stage3_index)
            and row["source_x_lower_endpoint_id"] == lower["endpoint_id"]
            and row["source_x_upper_endpoint_id"] == upper["endpoint_id"],
            f"output fragment crosswalk:{fragment_rank}",
        )
        require(
            qvalue(
                row["source_x_open_gap_strict_lower"],
                f"source fragment gap:{fragment_rank}",
            )
            == upper_low - lower_high,
            f"source fragment gap identity:{fragment_rank}",
        )
        fresh_length = (
            stage_u_value(geometry, 3, upper_low, upper_low)
            - stage_u_value(geometry, 3, lower_high, lower_high)
        ) / v121.aq(DELTA)
        stored_contains(
            row["normalized_stage3_output_length_strict_enclosure"],
            fresh_length,
            f"stage3 output length:{fragment_rank}",
        )
        require(
            qvalue(
                row["normalized_stage3_output_length_strict_enclosure"][0],
                f"stage3 output lower:{fragment_rank}",
            )
            > Q(4, 125),
            f"stage3 output lower >4/125:{fragment_rank}",
        )
        require(
            row["normalized_stage3_output_length_strict_lower_exceeds"]
            == "4/125"
            and row["lower_closed"] is True
            and row["upper_closed"] is False
            and row["source_parent_right_endpoint_remains_open"] is True
            and row["internal_stage3_cut_owned_by_right_cell"] is True
            and row["fragment_mass_is_nonnegative"] is True
            and row["mass_is_not_sampled_or_assumed_equal"] is True
            and row["row_sha256"] == row_digest(row),
            f"output fragment ownership/mass:{fragment_rank}",
        )
        grouped[input_rank].append(row)
        if upper["origin"] == "ROUND121_EXISTING_INPUT_CUT":
            input_rank += 1
        elif upper["origin"] == "ROUND123_STAGE3_OUTPUT_CUT":
            stage3_index += 1
    require(
        input_rank == 23 and stage3_index == 192,
        "terminal merged refinement indices",
    )

    by_child: dict[str, dict[str, Any]] = {}
    counts: list[int] = []
    for rank, (child, row) in enumerate(zip(children, partitions)):
        parts = grouped[rank]
        counts.append(len(parts))
        require(
            row["input_common_child_id"] == child["common_child_id"]
            and row["input_common_rank"] == rank
            and row["output_fragment_count"] == len(parts)
            and row["output_fragment_ids"]
            == [part["output_fragment_id"] for part in parts]
            and row["stage3_natural_index_span"]
            == [
                parts[0]["stage3_natural_index_j"],
                parts[-1]["stage3_natural_index_j"],
            ]
            and row["source_partition_lower_endpoint_id"]
            == parts[0]["source_x_lower_endpoint_id"]
            and row["source_partition_upper_endpoint_id"]
            == parts[-1]["source_x_upper_endpoint_id"],
            f"output partition crosswalk:{rank}",
        )
        minimum = min(
            qvalue(
                part["normalized_stage3_output_length_strict_enclosure"][0],
                f"partition output lower:{rank}",
            )
            for part in parts
        )
        require(
            qvalue(
                row[
                    "minimum_normalized_stage3_output_length_strict_lower"
                ],
                f"partition minimum:{rank}",
            )
            == minimum
            and row["disjoint_half_open_union_equals_input_child"] is True
            and row["symbolic_mass_partition_identity"]
            == "M_input_child=sum(output_fragment_masses)"
            and row[
                "arbitrary_positive_density_mass_weights_not_preassigned"
            ]
            is True
            and row["mass_weighted_inverse_length_assembly"]
            == (
                "sum_fragment M_fragment/ell_fragment"
                " < (100/(3*delta))*M_input_child"
            )
            and row[
                "fragment_count_does_not_multiply_mass_weighted_bound"
            ]
            is True
            and row["row_sha256"] == row_digest(row),
            f"output partition theorem:{rank}",
        )
        by_child[child["common_child_id"]] = row
    require(
        counts
        == [
            12,
            12,
            7,
            6,
            12,
            12,
            2,
            11,
            12,
            8,
            5,
            12,
            12,
            3,
            10,
            12,
            9,
            4,
            12,
            12,
            4,
            9,
            12,
            6,
        ],
        "independent per-child output counts",
    )
    require(
        Counter(counts)
        == Counter(
            {
                2: 1,
                3: 1,
                4: 2,
                5: 1,
                6: 2,
                7: 1,
                8: 1,
                9: 2,
                10: 1,
                11: 1,
                12: 11,
            }
        ),
        "output fragment histogram",
    )
    return rows, partitions, by_child


def derivative_replay(geometry: dict[str, Any]) -> dict[int, arb]:
    state = v121.source_and_collisions(
        geometry["theta_star"], v121.interval(Q(0), Q(1)), True
    )
    delta = v121.aq(DELTA)
    derivatives = {
        0: -state["a1"].derivative / delta,
        1: state["a2"].derivative / delta,
        2: geometry["derivative_ratio"],
    }
    thresholds = {0: Q(6), 1: Q(17), 2: Q(192)}
    ceilings = {0: Q(7), 1: Q(18), 2: Q(193)}
    for leg in range(3):
        lower, upper = interval_pair(derivatives[leg])
        require(
            thresholds[leg] < lower <= upper < ceilings[leg],
            f"independent output derivative:{leg}",
        )
    return derivatives


def verify_leg_rows(
    result: dict[str, Any],
    r121: dict[str, Any],
    r122: dict[str, Any],
    geometry: dict[str, Any],
    partition_by_child: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[tuple[str, int], dict[str, Any]]]:
    rows = result["accepted_norm_leg_output_rows"]
    require(type(rows) is list and len(rows) == 72, "72 leg-output rows")
    require(
        result["accepted_norm_leg_output_rows_sha256"] == digest(rows),
        "leg-output rows digest",
    )
    children = sorted(
        r121["common_refinement_rows"], key=lambda row: row["common_rank"]
    )
    children_by_id = {row["common_child_id"]: row for row in children}
    require(len(children_by_id) == 24, "24 leg-row children")
    seed_id = r121["exact_seed_contract"]["exact_parent_W_seed_id"]
    endpoint_brackets = {
        row["endpoint_id"]: tuple(
            qvalue(value, "Round121 endpoint bracket")
            for value in row["x_dyadic_bracket"]
        )
        for row in r121["pullback_endpoint_rows"]
    }
    endpoint_brackets[source_boundary_id("left", seed_id)] = (Q(0), Q(0))
    endpoint_brackets[source_boundary_id("right", seed_id)] = (Q(1), Q(1))

    f1_by_child_stage: dict[
        tuple[str, int], list[dict[str, Any]]
    ] = {}
    for slot in r121["gate5_F1_F6_slot_rows"]:
        if slot["field_index"] == 1:
            f1_by_child_stage.setdefault(
                (slot["common_child_id"], slot["stage"]), []
            ).append(slot)
    r122_slots = {
        (
            slot["official_word_key_id"],
            slot["refined_homogeneous_subbranch_id"],
            slot["roof_level_j"],
            slot["field_index"],
        ): slot
        for slot in r122["gate5_F7_F13_F16_slot_rows"]
    }
    require(len(r122_slots) == 960, "Round122 slot coordinate census")
    derivatives = derivative_replay(geometry)
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
    length_lowers = (Q(3, 100), Q(17, 200), Q(4, 125))
    recut_fields = (
        "source_recut_instance_id",
        "first_image_recut_instance_id",
        "second_image_recut_instance_id",
    )
    rows_by_child_leg: dict[
        tuple[str, int], dict[str, Any]
    ] = {}
    for row in rows:
        child_id = row["common_child_id"]
        leg = row["leg_index"]
        require(
            child_id in children_by_id
            and type(leg) is int
            and leg in {0, 1, 2}
            and (child_id, leg) not in rows_by_child_leg,
            "unique leg-output coordinate",
        )
        rows_by_child_leg[(child_id, leg)] = row
        child = children_by_id[child_id]
        rank = child["common_rank"]
        require(
            row["leg_output_row_id"]
            == leg_output_row_id(seed_id, child_id, leg)
            and row["common_rank"] == rank
            and row["input_stage"] == leg
            and row["output_stage"] == leg + 1
            and row["input_materialized_recut_instance_id"]
            == child[recut_fields[leg]]
            and row["input_natural_index_j"]
            == child["covering_stage_indices"][leg]
            and row["input_adapted_length_less_or_equal_delta"] is True,
            f"leg input crosswalk:{rank}:{leg}",
        )
        coordinates_for_leg = sorted(
            f1_by_child_stage[(child_id, leg)],
            key=lambda slot: slot["roof_level_j"],
        )
        roofs = [slot["roof_level_j"] for slot in coordinates_for_leg]
        word_ids = {
            slot["official_word_key_id"] for slot in coordinates_for_leg
        }
        require(
            len(word_ids) == 1
            and roofs == list(range(len(roofs)))
            and len(roofs) in {1, 2},
            f"leg official roofs:{rank}:{leg}",
        )
        word = next(iter(word_ids))
        subbranch = child["refined_homogeneous_subbranch_id"]
        require(
            row["refined_homogeneous_subbranch_id"] == subbranch
            and row["official_word_key_id"] == word
            and row["roof_level_js"] == roofs
            and row["roof_level_count"] == len(roofs),
            f"leg full-key coordinate:{rank}:{leg}",
        )
        expected_same_key: dict[str, list[str]] = {}
        for field in (10, 13, 16):
            expected_same_key[f"F{field}"] = [
                r122_slots[(word, subbranch, roof, field)]["slot_id"]
                for roof in roofs
            ]
        require(
            row["round122_same_key_slot_ids"] == expected_same_key,
            f"leg Round122 same-key crosswalk:{rank}:{leg}",
        )
        require(
            row["actual_collision_target"] == targets[leg]
            and row["actual_collision_owner"] == targets[leg]
            and row["actual_collision_chart"] == charts[leg]
            and row["adapted_output_coordinate"] == coordinates[leg]
            and row["adapted_output_coordinate_orientation"]
            == orientations[leg]
            and row[
                "normalized_output_coordinate_derivative_strict_lower"
            ]
            == derivative_lowers[leg]
            and row[
                "source_x_or_fragment_separation_strict_lower"
            ]
            == separation_lowers[leg],
            f"leg physical output semantics:{rank}:{leg}",
        )
        derivative_lower, _ = interval_pair(derivatives[leg])
        require(
            derivative_lower
            > qvalue(
                row[
                    "normalized_output_coordinate_derivative_strict_lower"
                ],
                f"leg derivative literal:{rank}:{leg}",
            ),
            f"leg derivative proof:{rank}:{leg}",
        )

        if leg < 2:
            lower_bracket = endpoint_brackets[
                child["source_x_lower_endpoint_id"]
            ]
            upper_bracket = endpoint_brackets[
                child["source_x_upper_endpoint_id"]
            ]
            lower_inside = lower_bracket[1]
            upper_inside = upper_bracket[0]
            require(
                lower_inside < upper_inside,
                f"positive leg source core:{rank}:{leg}",
            )
            fresh_length = (
                stage_u_value(
                    geometry, leg + 1, upper_inside, upper_inside
                )
                - stage_u_value(
                    geometry, leg + 1, lower_inside, lower_inside
                )
            ) / v121.aq(DELTA)
            expected_member_ids = [
                image_member_id(seed_id, child_id, leg + 1)
            ]
            require(
                row["output_member_count"] == 1
                and row["output_member_ids"] == expected_member_ids
                and len(
                    row[
                        "normalized_output_member_length_strict_enclosures"
                    ]
                )
                == 1,
                f"single image member:{rank}:{leg}",
            )
            stored_contains(
                row["normalized_output_member_length_strict_enclosures"][
                    0
                ],
                fresh_length,
                f"leg output length:{rank}:{leg}",
            )
            require(
                qvalue(
                    row[
                        "normalized_output_member_length_strict_enclosures"
                    ][0][0],
                    f"leg output lower:{rank}:{leg}",
                )
                > length_lowers[leg],
                f"leg output length theorem:{rank}:{leg}",
            )
            expected_mass_identity = "M_output_member=M_input_child"
        else:
            partition = partition_by_child[child_id]
            expected_member_ids = partition["output_fragment_ids"]
            require(
                row["output_member_count"] == len(expected_member_ids)
                and row["output_member_ids"] == expected_member_ids
                and row[
                    "normalized_output_member_length_strict_enclosures"
                ]
                == [
                    result["stage3_output_fragment_rows"][
                        next(
                            index
                            for index, fragment in enumerate(
                                result["stage3_output_fragment_rows"]
                            )
                            if fragment["output_fragment_id"] == identifier
                        )
                    ][
                        "normalized_stage3_output_length_strict_enclosure"
                    ]
                    for identifier in expected_member_ids
                ],
                f"stage3 output members:{rank}",
            )
            expected_mass_identity = (
                "sum_output_fragment_masses=M_input_child"
            )
        require(
            row["every_output_member_length_strict_lower_exceeds"]
            == qstr(length_lowers[leg])
            and row["every_output_member_length_less_or_equal_delta"] is True
            and row["output_members_are_half_open"] is True
            and row[
                "conditional_restriction_and_normalization_do_not_increase_Reg"
            ]
            is True
            and row["zero_mass_output_members_are_omitted"] is True
            and row["mass_partition_identity"] == expected_mass_identity
            and row["arbitrary_positive_normalized_density_scope"] is True
            and row["bypass_designated_b3_is_a_collision_angle"] is False
            and row["row_sha256"] == row_digest(row),
            f"leg family contract:{rank}:{leg}",
        )
    require(
        set(rows_by_child_leg)
        == {(child_id, leg) for child_id in children_by_id for leg in range(3)},
        "complete 24x3 leg-output census",
    )
    return rows, rows_by_child_leg


def expected_operator_theorem() -> dict[str, Any]:
    q = Q_REGULARITY
    cj = DISTORTION_CJ
    cone = REGULAR_DENSITY_CONE_K
    one_step_cone = q * cone + cj
    three_step_b = cj * (1 + q + q**2)
    three_step_cone = q**3 * cone + three_step_b
    require(
        THETA_INVERSE < q**3
        and 93**3 * 180337 - 144000 * 100**3 == 1055328309,
        "inverse Jacobian versus regularity arithmetic",
    )
    require(
        one_step_cone < cone and three_step_cone < cone,
        "regular-density cone invariance",
    )
    require(
        three_step_b == 41923500000000000000000000,
        "three-leg distortion arithmetic",
    )
    one_step_margin = (
        Q(F14_ONE_STEP) - Q(100, 3) - (1 + cj) * DELTA
    )
    direct_margin = (
        Q(F14_DIRECT_THREE_LEG)
        - Q(100, 3)
        - (1 + three_step_b) * DELTA
    )
    require(
        one_step_margin > 0
        and direct_margin > 0
        and F14_ONE_STEP**3 == F14_GENERIC_THREE_LEG,
        "F14=34 exact margins and composition",
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
        "C_J": str(cj),
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
            F14_GENERIC_THREE_LEG
        ),
        "generic_composition_identity": "34^3=39304",
        "physical_collision_factor_count": 3,
        "roof_level_slot_count_per_subbranch": 5,
        "roof_split_does_not_change_34_cubed_to_34_to_the_fifth": True,
        "direct_exact_seed_three_leg_distortion_B": str(three_step_b),
        "direct_exact_seed_three_leg_F14_bound": F14_DIRECT_THREE_LEG,
        "direct_exact_seed_three_leg_exact_margin": qstr(direct_margin),
        "direct_three_leg_bound_is_not_a_one_step_slot": True,
        "signed_Jordan_extension": (
            "apply the positive bound to positive and negative Jordan parts"
            " and take the strong-norm positive-decomposition infimum"
        ),
        "signed_extension_adds_no_factor_two": True,
        "cancellation_is_not_used_to_reduce_cost": True,
    }


def verify_operator_theorem(result: dict[str, Any]) -> None:
    require(
        result["arbitrary_density_and_Jordan_contract"]
        == expected_operator_theorem(),
        "closed arbitrary-density/Jordan theorem",
    )


def verify_f14_slots(
    result: dict[str, Any],
    r121: dict[str, Any],
    r122: dict[str, Any],
    leg_by_child: dict[tuple[str, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = result["gate5_F14_slot_rows"]
    require(type(rows) is list and len(rows) == 120, "120 F14 slots")
    require(
        result["gate5_F14_slot_rows_sha256"] == digest(rows),
        "F14 slot digest",
    )
    coordinates = [
        row
        for row in r121["gate5_F1_F6_slot_rows"]
        if row["field_index"] == 1
    ]
    require(len(coordinates) == 120, "120 source full-key coordinates")
    r122_slots = {
        (
            slot["official_word_key_id"],
            slot["refined_homogeneous_subbranch_id"],
            slot["roof_level_j"],
            slot["field_index"],
        ): slot
        for slot in r122["gate5_F7_F13_F16_slot_rows"]
    }
    expected_rows: list[dict[str, Any]] = []
    keys: set[str] = set()
    ids: set[str] = set()
    for coordinate in coordinates:
        child_id = coordinate["common_child_id"]
        leg = coordinate["stage"]
        leg_row = leg_by_child[(child_id, leg)]
        word = coordinate["official_word_key_id"]
        subbranch = coordinate["refined_homogeneous_subbranch_id"]
        roof = coordinate["roof_level_j"]
        immutable_key = [
            word,
            subbranch,
            roof,
            "regular_density_operator_cost",
        ]
        key_text = canonical(immutable_key)
        require(key_text not in keys, "unique expected F14 key")
        keys.add(key_text)
        identifier = f14_slot_id(immutable_key)
        require(identifier not in ids, "unique expected F14 slot ID")
        ids.add(identifier)
        roof_position = leg_row["roof_level_js"].index(roof)
        expected = {
            "slot_id": identifier,
            "immutable_slot_key": immutable_key,
            "official_word_key_id": word,
            "refined_homogeneous_subbranch_id": subbranch,
            "roof_level_j": roof,
            "field_index": 14,
            "field_name": "regular_density_operator_cost",
            "field_bound_semantics": "STRICT_UPPER",
            "field_value_or_contract": str(F14_ONE_STEP),
            "slot_status": "CERTIFIED_ON_THIS_EXACT_SEED_COMMON_CHILD",
            "common_child_id": child_id,
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
            "round122_same_key_F10_slot_id": r122_slots[
                (word, subbranch, roof, 10)
            ]["slot_id"],
            "round122_same_key_F13_slot_id": r122_slots[
                (word, subbranch, roof, 13)
            ]["slot_id"],
            "round122_same_key_F16_slot_id": r122_slots[
                (word, subbranch, roof, 16)
            ]["slot_id"],
            "arbitrary_positive_normalized_density_scope": True,
            "Round122_F10_zero_is_dependency_only_not_payment_for_F14": True,
            "signed_Jordan_extension_installed": True,
            "transparent_wall_roof_split_adds_no_F14_factor": True,
            "roof_slot_value_is_one_step_not_path_product": True,
            "bypass_designated_b3_is_a_collision_angle": False,
        }
        expected["row_sha256"] = digest(expected)
        expected_rows.append(expected)
    require(rows == expected_rows, "independently rebuilt F14 slots")
    return rows


def verify_combined_registry(
    result: dict[str, Any],
    r121: dict[str, Any],
    r122: dict[str, Any],
    f14_rows: list[dict[str, Any]],
) -> None:
    inherited = [
        row["slot_id"] for row in r121["gate5_F1_F6_slot_rows"]
    ] + [
        row["slot_id"] for row in r122["gate5_F7_F13_F16_slot_rows"]
    ]
    require(
        len(inherited) == len(set(inherited)) == 1680,
        "1680 inherited slots",
    )
    require(
        digest(inherited)
        == r122["combined_F1_F13_F16_slot_registry"][
            "combined_slot_ids_sha256"
        ],
        "Round122 combined slot digest",
    )
    combined = inherited + [row["slot_id"] for row in f14_rows]
    require(
        len(combined) == len(set(combined)) == 1800,
        "1800 combined slots",
    )
    expected = {
        "inherited_Round122_slot_count": 1680,
        "new_F14_slot_count": 120,
        "combined_slot_count": 1800,
        "slot_count_per_certified_field": 120,
        "certified_field_indices": list(range(1, 15)) + [16],
        "combined_slot_ids_sha256": digest(combined),
        "all_immutable_slot_keys_are_full_word_subbranch_roof_field_keys": True,
        "F14_slots_are_source_full_keys_not_output_fragment_keys": True,
    }
    require(
        result["combined_F1_F14_F16_slot_registry"] == expected,
        "combined 1800-slot registry",
    )


def verify_pins(result: dict[str, Any], *, check_bytes: bool = True) -> None:
    require(
        result["upstream_and_helper_pins"]
        == dict(sorted(EXPECTED_PINS.items())),
        "closed upstream/helper pins",
    )
    if check_bytes:
        for relative, expected in EXPECTED_PINS.items():
            path = HERE.parent / relative
            require(
                path.is_file()
                and not path.is_symlink()
                and sha256(path) == expected,
                f"byte pin:{relative}",
            )


def expected_status(r122: dict[str, Any]) -> dict[str, str]:
    status = dict(r122["gate5_actual_child_field_status"])
    status["F14"] = "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN"
    return status


def verify_static_contract(
    document: dict[str, Any],
    inputs: dict[str, Any],
    *,
    check_bytes: bool = True,
) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict and set(result) == RESULT_KEYS,
            "closed certificate result")
    require(
        document["result_sha256"] == digest(result),
        "certificate result digest",
    )
    require(
        type(result["precision_bits"]) is int
        and result["precision_bits"] >= 1536,
        "producer precision",
    )
    require(
        type(result["root_bisections"]) is int
        and result["root_bisections"] >= 240,
        "producer root depth",
    )
    verify_pins(result, check_bytes=check_bytes)
    r121 = inputs["r121"]
    r122 = inputs["r122"]
    require(
        result["status"]
        == "CERTIFIED_EXACT_SEED_STAGE3_OUTPUT_PROPERIZATION__F14_INSTALLED",
        "Round123 certified status",
    )
    require(
        result["round121_contract"]
        == {
            "result_sha256": (
                "962db517d76b18e7681c411734b568491e600776dbf5317d9ebff8494a9aebd8"
            ),
            "actual_child_count": 24,
            "inherited_F1_F6_slot_count": 720,
        },
        "Round121 contract",
    )
    require(
        result["round122_contract"]
        == {
            "certificate_sha256": ROUND122_SHA256,
            "result_sha256": (
                "e8bc4e02635b70dda7cee0485811ae68d42ee595c37a03a5b2aa94ecf170f6cb"
            ),
            "inherited_certified_field_indices": (
                list(range(1, 14)) + [16]
            ),
            "inherited_slot_count": 1680,
        },
        "Round122 bridge contract",
    )
    require(
        result["stagewise_output_length_theorem"]
        == {
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
        "stagewise output-length theorem",
    )
    require(
        result["gate5_actual_child_field_status"] == expected_status(r122)
        and result["rank3_seed_child_field_maturity"] == "15/18"
        and result["remaining_uninstalled_child_fields"]
        == ["F15", "F17", "F18"]
        and result["gate5_global_maturity"] == "10/18"
        and result["complete_18_field_block_count"] == 0
        and result["gate5_block_count"] == 0
        and result["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "fail-closed Gate5/CM2 status",
    )
    require(
        result["strict_scope"]
        == (
            "one Round121 exact-b seed, its 24 materialized common children,"
            " three physical collision legs, and the 216-member actual-third"
            " output properization"
        ),
        "strict scope",
    )
    require(
        result["strict_nonclaims"]
        == [
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
        "strict nonclaims",
    )
    return result


def verify_count_ledgers(
    result: dict[str, Any],
    partitions: list[dict[str, Any]],
    leg_rows: list[dict[str, Any]],
) -> None:
    counts = [row["output_fragment_count"] for row in partitions]
    minimum = min(
        qvalue(
            row["minimum_normalized_stage3_output_length_strict_lower"],
            "global partition minimum",
        )
        for row in partitions
    )
    histogram = {
        str(key): value for key, value in sorted(Counter(counts).items())
    }
    derived = {
        "existing_round121_internal_cut_count": 23,
        "stage3_internal_cut_count": 192,
        "stage3_natural_cell_count": 193,
        "combined_internal_cut_count": 215,
        "output_fragment_count": 216,
        "input_common_child_count": 24,
        "output_fragment_count_per_input_child_min": min(counts),
        "output_fragment_count_per_input_child_max": max(counts),
        "output_fragment_count_per_input_child_histogram": histogram,
        "global_minimum_normalized_stage3_output_length_strict_lower": qstr(
            minimum
        ),
        "stage1_output_member_length_strict_lower": "3/100",
        "stage2_output_member_length_strict_lower": "17/200",
        "stage3_output_fragment_length_strict_lower": "4/125",
        "uniform_all_leg_output_member_length_strict_lower": "3/100",
        "family_mass_weighted_inverse_length_coefficient": "100/(3*delta)",
        "accepted_norm_leg_output_row_count": len(leg_rows),
        "all_counts_derived_without_expected_output_fragment_literal": True,
    }
    require(result["derived_count_ledger"] == derived,
            "derived count ledger")
    count_ledger = dict(derived)
    count_ledger.update(
        {
            "actual_child_count": 24,
            "accepted_norm_leg_output_row_count": 72,
            "stage3_output_fragment_count": 216,
            "new_F14_slot_count": 120,
            "inherited_Round122_slot_count": 1680,
            "combined_child_local_slot_count": 1800,
            "certified_child_local_field_count": 15,
            "complete_18_field_block_count": 0,
        }
    )
    require(result["count_ledger"] == count_ledger,
            "closed count ledger")


def fast_semantic_contract(
    document: dict[str, Any], inputs: dict[str, Any]
) -> None:
    """Closed symbolic replay used by every re-signed hostile mutation."""

    result = verify_static_contract(document, inputs, check_bytes=False)
    r121 = inputs["r121"]
    r122 = inputs["r122"]
    seed_id = r121["exact_seed_contract"]["exact_parent_W_seed_id"]
    verify_operator_theorem(result)

    for key in (
        "stage3_endpoint_rows",
        "stage3_natural_cell_rows",
        "stage3_output_fragment_rows",
        "input_child_output_partition_rows",
        "accepted_norm_leg_output_rows",
        "gate5_F14_slot_rows",
    ):
        require(
            result[f"{key}_sha256"] == digest(result[key]),
            f"fast list digest:{key}",
        )
        for row in result[key]:
            require(
                type(row) is dict and row["row_sha256"] == row_digest(row),
                f"fast row digest:{key}",
            )
    require(
        result["merged_internal_cut_rows_sha256"]
        == digest(result["merged_internal_cut_rows"]),
        "fast merged digest",
    )
    verify_coordinate_contract_fast(result)

    roots = result["stage3_endpoint_rows"]
    require(len(roots) == 192, "fast 192 roots")
    prior_upper = Q(0)
    root_by_id: dict[str, dict[str, Any]] = {}
    for level, row in enumerate(roots, 1):
        require(
            set(row)
            == {
                "actual_third_chart",
                "endpoint_id",
                "exact_root_equation",
                "exact_root_equation_id",
                "left_function_sign",
                "lower_owner",
                "natural_index_j",
                "normalized_derivative_strict_enclosure",
                "numeric_bracket_participates_in_ID",
                "orientation",
                "right_function_sign",
                "row_sha256",
                "stage",
                "unique_root_certified",
                "upper_owner",
                "x_bracket_width",
                "x_dyadic_bracket",
            },
            f"fast closed root:{level}",
        )
        lower, upper = (
            qvalue(value, f"fast root bracket:{level}")
            for value in row["x_dyadic_bracket"]
        )
        derivative = [
            qvalue(value, f"fast root derivative:{level}")
            for value in row["normalized_derivative_strict_enclosure"]
        ]
        identifier = endpoint_id(seed_id, level)
        require(
            row["endpoint_id"] == identifier
            and identifier not in root_by_id
            and row["stage"] == 3
            and row["natural_index_j"] == level
            and row["exact_root_equation_id"]
            == f"round123-U3-equals-{level}-delta"
            and row["exact_root_equation"] == f"U3(x)={level}*10^-90"
            and row["actual_third_chart"] == "N"
            and row["orientation"] == "U3(x)=a3(0)-a3(x)"
            and prior_upper < lower < upper < 1
            and qvalue(row["x_bracket_width"], "fast root width")
            == upper - lower
            and Q(192) < derivative[0] <= derivative[1] < Q(193)
            and row["left_function_sign"] == -1
            and row["right_function_sign"] == 1
            and row["unique_root_certified"] is True
            and row["numeric_bracket_participates_in_ID"] is False
            and row["lower_owner"] == f"stage-3-natural-cell-{level - 1}"
            and row["upper_owner"] == f"stage-3-natural-cell-{level}",
            f"fast root contract:{level}",
        )
        prior_upper = upper
        root_by_id[identifier] = row

    cells = result["stage3_natural_cell_rows"]
    require(len(cells) == 193, "fast 193 natural cells")
    endpoint_ids = [
        source_boundary_id("left", seed_id),
        *root_by_id,
        source_boundary_id("right", seed_id),
    ]
    for index, row in enumerate(cells):
        full = index < 192
        require(
            row["recut_instance_id"] == stage3_cell_id(seed_id, index)
            and row["stage"] == 3
            and row["natural_index_j"] == index
            and row["adapted_coordinate_id"]
            == "round123-U3-north-chart-output"
            and row["adapted_lower"] == f"{index}*delta"
            and row["adapted_upper"]
            == (f"{index + 1}*delta" if full else "U3(1)")
            and row["lower_endpoint_id"] == endpoint_ids[index]
            and row["upper_endpoint_id"] == endpoint_ids[index + 1]
            and row["lower_closed"] is True
            and row["upper_closed"] is False
            and row["internal_cut_is_owned_by_right_cell"] is True
            and row["source_parent_right_endpoint_remains_open"] is True
            and row["full_delta_cell"] is full
            and row["terminal_partial_cell"] is (not full)
            and row["actual_third_owner"] == "G[-1,-2]"
            and row["actual_third_collision_chart"] == "N",
            f"fast natural cell:{index}",
        )

    old = {
        row["endpoint_id"]: row for row in r121["pullback_endpoint_rows"]
    }
    merged = result["merged_internal_cut_rows"]
    require(len(merged) == 215, "fast 215 merged cuts")
    seen_old: set[str] = set()
    seen_new: set[str] = set()
    prior_upper = Q(0)
    adjacent_gaps: list[Q] = []
    for row in merged:
        require(
            set(row)
            == {
                "endpoint_id",
                "natural_index_j",
                "origin",
                "stage",
                "u3_over_delta_enclosure",
                "x_dyadic_bracket",
            },
            "fast closed merged row",
        )
        lower, upper = (
            qvalue(value, "fast merged bracket")
            for value in row["x_dyadic_bracket"]
        )
        require(prior_upper < lower < upper < 1, "fast merged order")
        if prior_upper:
            adjacent_gaps.append(lower - prior_upper)
        prior_upper = upper
        identifier = row["endpoint_id"]
        if identifier in old:
            source = old[identifier]
            seen_old.add(identifier)
            require(
                row["origin"] == "ROUND121_EXISTING_INPUT_CUT"
                and row["stage"] == source["stage"]
                and row["natural_index_j"] == source["natural_index_j"]
                and row["x_dyadic_bracket"] == source["x_dyadic_bracket"],
                "fast old merged crosswalk",
            )
        else:
            require(identifier in root_by_id, "fast known new merged root")
            source = root_by_id[identifier]
            seen_new.add(identifier)
            require(
                row["origin"] == "ROUND123_STAGE3_OUTPUT_CUT"
                and row["stage"] == 3
                and row["natural_index_j"] == source["natural_index_j"]
                and row["x_dyadic_bracket"] == source["x_dyadic_bracket"]
                and row["u3_over_delta_enclosure"]
                == [
                    str(source["natural_index_j"]),
                    str(source["natural_index_j"]),
                ],
                "fast new merged crosswalk",
            )
    require(
        seen_old == set(old) and seen_new == set(root_by_id),
        "fast complete merge",
    )
    require(
        qvalue(
            result["merged_cut_spacing_audit"]["minimum_combined_x_gap"],
            "fast minimum merged gap",
        )
        == min(adjacent_gaps)
        and min(adjacent_gaps) > Q(1, 6000)
        and result["merged_cut_spacing_audit"][
            "combined_internal_cut_count"
        ]
        == 215
        and result["merged_cut_spacing_audit"][
            "all_cut_brackets_pairwise_strictly_ordered"
        ]
        is True,
        "fast merged spacing",
    )

    children = sorted(
        r121["common_refinement_rows"], key=lambda row: row["common_rank"]
    )
    boundaries = refinement_boundaries(result, r121)
    fragments = result["stage3_output_fragment_rows"]
    require(len(fragments) == 216, "fast 216 fragments")
    input_rank = 0
    stage3_index = 0
    grouped: dict[int, list[dict[str, Any]]] = {
        index: [] for index in range(24)
    }
    for rank, (lower, upper, row) in enumerate(
        zip(boundaries, boundaries[1:], fragments)
    ):
        child = children[input_rank]
        lower_high = qvalue(
            lower["x_dyadic_bracket"][1], "fast fragment lower"
        )
        upper_low = qvalue(
            upper["x_dyadic_bracket"][0], "fast fragment upper"
        )
        length = [
            qvalue(value, "fast output length")
            for value in row[
                "normalized_stage3_output_length_strict_enclosure"
            ]
        ]
        require(
            row["fragment_rank"] == rank
            and row["output_fragment_id"]
            == output_fragment_id(
                seed_id,
                child["common_child_id"],
                lower["endpoint_id"],
                upper["endpoint_id"],
                stage3_index,
            )
            and row["input_common_child_id"] == child["common_child_id"]
            and row["input_common_rank"] == input_rank
            and row["stage3_natural_index_j"] == stage3_index
            and row["stage3_output_recut_instance_id"]
            == stage3_cell_id(seed_id, stage3_index)
            and row["source_x_lower_endpoint_id"] == lower["endpoint_id"]
            and row["source_x_upper_endpoint_id"] == upper["endpoint_id"]
            and qvalue(row["source_x_open_gap_strict_lower"], "fast gap")
            == upper_low - lower_high
            and Q(4, 125) < length[0] <= length[1] <= 1
            and row[
                "normalized_stage3_output_length_strict_lower_exceeds"
            ]
            == "4/125"
            and row["lower_closed"] is True
            and row["upper_closed"] is False
            and row["source_parent_right_endpoint_remains_open"] is True
            and row["internal_stage3_cut_owned_by_right_cell"] is True
            and row["fragment_mass_is_nonnegative"] is True
            and row["mass_is_not_sampled_or_assumed_equal"] is True,
            f"fast fragment:{rank}",
        )
        grouped[input_rank].append(row)
        if upper["origin"] == "ROUND121_EXISTING_INPUT_CUT":
            input_rank += 1
        elif upper["origin"] == "ROUND123_STAGE3_OUTPUT_CUT":
            stage3_index += 1
    require(input_rank == 23 and stage3_index == 192,
            "fast terminal refinement")

    partitions = result["input_child_output_partition_rows"]
    require(len(partitions) == 24, "fast 24 partitions")
    partition_by_child: dict[str, dict[str, Any]] = {}
    for rank, (child, row) in enumerate(zip(children, partitions)):
        parts = grouped[rank]
        minimum_part_length = min(
            qvalue(
                part["normalized_stage3_output_length_strict_enclosure"][0],
                "fast partition member minimum",
            )
            for part in parts
        )
        require(
            row["input_common_child_id"] == child["common_child_id"]
            and row["input_common_rank"] == rank
            and row["output_fragment_count"] == len(parts)
            and row["output_fragment_ids"]
            == [part["output_fragment_id"] for part in parts]
            and row["disjoint_half_open_union_equals_input_child"] is True
            and row["symbolic_mass_partition_identity"]
            == "M_input_child=sum(output_fragment_masses)"
            and row[
                "arbitrary_positive_density_mass_weights_not_preassigned"
            ]
            is True
            and row[
                "fragment_count_does_not_multiply_mass_weighted_bound"
            ]
            is True
            and row["mass_weighted_inverse_length_assembly"]
            == (
                "sum_fragment M_fragment/ell_fragment"
                " < (100/(3*delta))*M_input_child"
            ),
            f"fast partition:{rank}",
        )
        require(
            qvalue(
                row[
                    "minimum_normalized_stage3_output_length_strict_lower"
                ],
                "fast partition stored minimum",
            )
            == minimum_part_length,
            f"fast partition minimum:{rank}",
        )
        partition_by_child[child["common_child_id"]] = row

    leg_by_child = fast_leg_contract(
        result, r121, r122, partition_by_child
    )
    f14_rows = verify_f14_slots(result, r121, r122, leg_by_child)
    verify_combined_registry(result, r121, r122, f14_rows)
    verify_count_ledgers(
        result, partitions, result["accepted_norm_leg_output_rows"]
    )


def verify_coordinate_contract_fast(result: dict[str, Any]) -> None:
    contract = result["stage3_adapted_coordinate_contract"]
    length = [
        qvalue(value, "fast U3 length")
        for value in contract["U3_1_over_delta_strict_enclosure"]
    ]
    derivative = [
        qvalue(value, "fast U3 derivative")
        for value in contract[
            "normalized_U3_derivative_strict_enclosure"
        ]
    ]
    require(
        contract["a3"] == "pi/2-asin(n3_x)+asin(p3)"
        and contract["U3"] == "a3(0)-a3(x)"
        and contract["actual_third_collision_chart"] == "N"
        and contract["actual_third_owner"] == "G[-1,-2]"
        and contract["orientation"] == "STRICTLY_INCREASING_U3"
        and contract["simple_length_bound"] == "192<U3(1)/delta<193"
        and Q(192) < length[0] <= length[1] < Q(193)
        and Q(192) < derivative[0] <= derivative[1] < Q(193),
        "fast coordinate contract",
    )


def fast_leg_contract(
    result: dict[str, Any],
    r121: dict[str, Any],
    r122: dict[str, Any],
    partition_by_child: dict[str, dict[str, Any]],
) -> dict[tuple[str, int], dict[str, Any]]:
    rows = result["accepted_norm_leg_output_rows"]
    require(len(rows) == 72, "fast 72 legs")
    children = {
        row["common_child_id"]: row
        for row in r121["common_refinement_rows"]
    }
    f1_by_child_stage: dict[
        tuple[str, int], list[dict[str, Any]]
    ] = {}
    for slot in r121["gate5_F1_F6_slot_rows"]:
        if slot["field_index"] == 1:
            f1_by_child_stage.setdefault(
                (slot["common_child_id"], slot["stage"]), []
            ).append(slot)
    r122_slots = {
        (
            slot["official_word_key_id"],
            slot["refined_homogeneous_subbranch_id"],
            slot["roof_level_j"],
            slot["field_index"],
        ): slot
        for slot in r122["gate5_F7_F13_F16_slot_rows"]
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
    length_lowers = (Q(3, 100), Q(17, 200), Q(4, 125))
    recut_fields = (
        "source_recut_instance_id",
        "first_image_recut_instance_id",
        "second_image_recut_instance_id",
    )
    seed_id = r121["exact_seed_contract"]["exact_parent_W_seed_id"]
    seen: dict[tuple[str, int], dict[str, Any]] = {}
    for row in rows:
        child_id = row["common_child_id"]
        leg = row["leg_index"]
        require(
            child_id in children
            and type(leg) is int
            and leg in {0, 1, 2}
            and (child_id, leg) not in seen,
            "fast unique leg",
        )
        child = children[child_id]
        coordinates_for_leg = sorted(
            f1_by_child_stage[(child_id, leg)],
            key=lambda slot: slot["roof_level_j"],
        )
        roofs = [slot["roof_level_j"] for slot in coordinates_for_leg]
        word = coordinates_for_leg[0]["official_word_key_id"]
        subbranch = child["refined_homogeneous_subbranch_id"]
        same_key = {
            f"F{field}": [
                r122_slots[(word, subbranch, roof, field)]["slot_id"]
                for roof in roofs
            ]
            for field in (10, 13, 16)
        }
        lengths = [
            [
                qvalue(value, "fast leg output length")
                for value in enclosure
            ]
            for enclosure in row[
                "normalized_output_member_length_strict_enclosures"
            ]
        ]
        require(
            row["leg_output_row_id"]
            == leg_output_row_id(seed_id, child_id, leg)
            and row["common_rank"] == child["common_rank"]
            and row["input_stage"] == leg
            and row["output_stage"] == leg + 1
            and row["input_materialized_recut_instance_id"]
            == child[recut_fields[leg]]
            and row["input_natural_index_j"]
            == child["covering_stage_indices"][leg]
            and row["input_adapted_length_less_or_equal_delta"] is True
            and row["refined_homogeneous_subbranch_id"] == subbranch
            and row["official_word_key_id"] == word
            and row["roof_level_js"] == roofs
            and row["roof_level_count"] == len(roofs)
            and row["round122_same_key_slot_ids"] == same_key
            and row["actual_collision_target"] == targets[leg]
            and row["actual_collision_owner"] == targets[leg]
            and row["actual_collision_chart"] == charts[leg]
            and row["adapted_output_coordinate"] == coordinates[leg]
            and row["adapted_output_coordinate_orientation"]
            == orientations[leg]
            and row[
                "normalized_output_coordinate_derivative_strict_lower"
            ]
            == derivative_lowers[leg]
            and row[
                "source_x_or_fragment_separation_strict_lower"
            ]
            == separation_lowers[leg]
            and row["output_member_count"]
            == len(row["output_member_ids"])
            == len(lengths)
            and all(
                length_lowers[leg] < pair[0] <= pair[1] <= 1
                for pair in lengths
            )
            and row["every_output_member_length_strict_lower_exceeds"]
            == qstr(length_lowers[leg])
            and row["every_output_member_length_less_or_equal_delta"] is True
            and row["output_members_are_half_open"] is True
            and row[
                "conditional_restriction_and_normalization_do_not_increase_Reg"
            ]
            is True
            and row["zero_mass_output_members_are_omitted"] is True
            and row["arbitrary_positive_normalized_density_scope"] is True
            and row["bypass_designated_b3_is_a_collision_angle"] is False,
            "fast leg contract",
        )
        if leg < 2:
            require(
                row["output_member_count"] == 1
                and row["output_member_ids"]
                == [image_member_id(seed_id, child_id, leg + 1)]
                and row["mass_partition_identity"]
                == "M_output_member=M_input_child",
                "fast image leg members",
            )
        else:
            partition = partition_by_child[child_id]
            require(
                row["output_member_ids"] == partition["output_fragment_ids"]
                and row["mass_partition_identity"]
                == "sum_output_fragment_masses=M_input_child",
                "fast third-leg members",
            )
        seen[(child_id, leg)] = row
    require(
        set(seen)
        == {(child_id, leg) for child_id in children for leg in range(3)},
        "fast complete legs",
    )
    return seen


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    cursor = root
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def get_path(root: Any, path: tuple[Any, ...]) -> Any:
    cursor = root
    for key in path:
        cursor = cursor[key]
    return cursor


def resign_document(
    document: dict[str, Any], inputs: dict[str, Any]
) -> None:
    """Re-sign every nested integrity layer after a hostile mutation."""

    result = document["result"]
    row_lists = (
        "stage3_endpoint_rows",
        "stage3_natural_cell_rows",
        "stage3_output_fragment_rows",
        "input_child_output_partition_rows",
        "accepted_norm_leg_output_rows",
    )
    for key in row_lists:
        rows = result.get(key, [])
        if type(rows) is list:
            for row in rows:
                if type(row) is dict:
                    row["row_sha256"] = row_digest(row)
            digest_key = f"{key}_sha256"
            if digest_key in result:
                result[digest_key] = digest(rows)
    if type(result.get("merged_internal_cut_rows")) is list:
        result["merged_internal_cut_rows_sha256"] = digest(
            result["merged_internal_cut_rows"]
        )

    leg_by_coordinate = {
        (row.get("common_child_id"), row.get("leg_index")): row
        for row in result.get("accepted_norm_leg_output_rows", [])
        if type(row) is dict
    }
    for slot in result.get("gate5_F14_slot_rows", []):
        if type(slot) is not dict:
            continue
        key = slot.get("immutable_slot_key")
        if type(key) is list:
            slot["slot_id"] = f14_slot_id(key)
        leg = leg_by_coordinate.get(
            (slot.get("common_child_id"), slot.get("stage"))
        )
        if leg is not None:
            slot["accepted_norm_leg_output_row_id"] = leg.get(
                "leg_output_row_id"
            )
            slot["accepted_norm_leg_output_row_sha256"] = leg.get(
                "row_sha256"
            )
            slot["input_materialized_recut_instance_id"] = leg.get(
                "input_materialized_recut_instance_id"
            )
            slot["output_member_count"] = leg.get("output_member_count")
            slot["output_member_ids"] = leg.get("output_member_ids")
        slot["row_sha256"] = row_digest(slot)
    if type(result.get("gate5_F14_slot_rows")) is list:
        result["gate5_F14_slot_rows_sha256"] = digest(
            result["gate5_F14_slot_rows"]
        )
        inherited = [
            row["slot_id"]
            for row in inputs["r121"]["gate5_F1_F6_slot_rows"]
        ] + [
            row["slot_id"]
            for row in inputs["r122"]["gate5_F7_F13_F16_slot_rows"]
        ]
        combined = inherited + [
            row.get("slot_id")
            for row in result["gate5_F14_slot_rows"]
            if type(row) is dict
        ]
        registry = result.get("combined_F1_F14_F16_slot_registry")
        if type(registry) is dict:
            registry["combined_slot_ids_sha256"] = digest(combined)
    document["result_sha256"] = digest(result)


def semantic_attacks(
    baseline: dict[str, Any], inputs: dict[str, Any]
) -> list[str]:
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def add(label: str, path: tuple[Any, ...], value: Any) -> None:
        attacks.append(
            (
                label,
                lambda doc, p=path, v=value: set_path(doc, p, v),
            )
        )

    def delete(label: str, path: tuple[Any, ...], index: int = 0) -> None:
        attacks.append(
            (
                label,
                lambda doc, p=path, i=index: get_path(doc, p).pop(i),
            )
        )

    def swap(
        label: str, path: tuple[Any, ...], left: int, right: int
    ) -> None:
        def mutation(doc: dict[str, Any], p: tuple[Any, ...] = path) -> None:
            rows = get_path(doc, p)
            rows[left], rows[right] = rows[right], rows[left]

        attacks.append((label, mutation))

    r = ("result",)
    theorem = r + ("arbitrary_density_and_Jordan_contract",)
    roots = r + ("stage3_endpoint_rows",)
    cells = r + ("stage3_natural_cell_rows",)
    merged = r + ("merged_internal_cut_rows",)
    fragments = r + ("stage3_output_fragment_rows",)
    partitions = r + ("input_child_output_partition_rows",)
    legs = r + ("accepted_norm_leg_output_rows",)
    slots = r + ("gate5_F14_slot_rows",)

    add("schema_mutation", ("schema",), "cm2.round123.mutant")
    attacks.append(
        (
            "unknown_result_field",
            lambda doc: doc["result"].__setitem__("unknown", 1),
        )
    )
    add("precision_downgrade", r + ("precision_bits",), 1024)
    add("root_depth_downgrade", r + ("root_bisections",), 199)
    first_pin = next(iter(baseline["result"]["upstream_and_helper_pins"]))
    add(
        "upstream_pin_mutation",
        r + ("upstream_and_helper_pins", first_pin),
        "0" * 64,
    )
    attacks.append(
        (
            "upstream_pin_delete",
            lambda doc, key=first_pin: doc["result"][
                "upstream_and_helper_pins"
            ].pop(key),
        )
    )
    add("status_fail_closed", r + ("status",), "PENDING")
    add(
        "round121_result_pin",
        r + ("round121_contract", "result_sha256"),
        "0" * 64,
    )
    add(
        "round122_certificate_pin",
        r + ("round122_contract", "certificate_sha256"),
        "0" * 64,
    )
    add(
        "round122_fields_add_F14",
        r + ("round122_contract", "inherited_certified_field_indices"),
        list(range(1, 17)),
    )
    add(
        "coordinate_a3",
        r + ("stage3_adapted_coordinate_contract", "a3"),
        "ordinary Euclidean curvature",
    )
    add(
        "coordinate_U3_orientation",
        r + ("stage3_adapted_coordinate_contract", "U3"),
        "a3(x)-a3(0)",
    )
    add(
        "coordinate_actual_owner",
        r + ("stage3_adapted_coordinate_contract", "actual_third_owner"),
        "W[-1,-2]",
    )
    add(
        "coordinate_actual_chart",
        r
        + (
            "stage3_adapted_coordinate_contract",
            "actual_third_collision_chart",
        ),
        "S",
    )
    add(
        "coordinate_length_claim",
        r + ("stage3_adapted_coordinate_contract", "simple_length_bound"),
        "191<U3(1)/delta<192",
    )
    add(
        "coordinate_derivative_inflate",
        r
        + (
            "stage3_adapted_coordinate_contract",
            "normalized_U3_derivative_strict_enclosure",
        ),
        ["193", "194"],
    )
    delete("stage3_root_delete", roots)

    def duplicate_root(doc: dict[str, Any]) -> None:
        doc["result"]["stage3_endpoint_rows"][-1] = copy.deepcopy(
            doc["result"]["stage3_endpoint_rows"][0]
        )

    attacks.append(("stage3_root_duplicate", duplicate_root))
    swap("stage3_root_reorder", roots, 0, 1)
    add("stage3_root_level", roots + (0, "natural_index_j"), 2)
    add(
        "stage3_root_equation",
        roots + (0, "exact_root_equation"),
        "U3(x)=2*10^-90",
    )
    add(
        "stage3_root_bracket",
        roots + (0, "x_dyadic_bracket"),
        ["1/2", "3/4"],
    )
    add("stage3_root_left_sign", roots + (0, "left_function_sign"), 1)
    add(
        "stage3_root_derivative_inflate",
        roots + (0, "normalized_derivative_strict_enclosure"),
        ["193", "194"],
    )
    add("stage3_root_lower_owner", roots + (0, "lower_owner"), "wrong")
    add(
        "stage3_root_numeric_identity",
        roots + (0, "numeric_bracket_participates_in_ID"),
        True,
    )
    attacks.append(
        (
            "unknown_stage3_root_field",
            lambda doc: doc["result"]["stage3_endpoint_rows"][0].__setitem__(
                "unknown", True
            ),
        )
    )
    delete("stage3_cell_delete", cells)

    def duplicate_cell(doc: dict[str, Any]) -> None:
        doc["result"]["stage3_natural_cell_rows"][-1] = copy.deepcopy(
            doc["result"]["stage3_natural_cell_rows"][0]
        )

    attacks.append(("stage3_cell_duplicate", duplicate_cell))
    add(
        "stage3_cell_endpoint",
        cells + (0, "upper_endpoint_id"),
        "wrong",
    )
    add("stage3_cell_right_closed", cells + (0, "upper_closed"), True)
    add(
        "stage3_cell_left_owns_cut",
        cells + (0, "internal_cut_is_owned_by_right_cell"),
        False,
    )
    add(
        "stage3_cell_terminal_flag",
        cells + (0, "terminal_partial_cell"),
        True,
    )
    delete("merged_cut_delete", merged)

    def duplicate_merged(doc: dict[str, Any]) -> None:
        doc["result"]["merged_internal_cut_rows"][-1] = copy.deepcopy(
            doc["result"]["merged_internal_cut_rows"][0]
        )

    attacks.append(("merged_cut_duplicate", duplicate_merged))
    swap("merged_cut_reorder", merged, 0, 1)
    add(
        "merged_cut_origin",
        merged + (0, "origin"),
        "ROUND121_EXISTING_INPUT_CUT",
    )
    add("merged_cut_stage", merged + (0, "stage"), 2)
    add(
        "merged_cut_overlap",
        merged + (1, "x_dyadic_bracket"),
        get_path(baseline, merged + (0, "x_dyadic_bracket")),
    )
    add(
        "merged_min_gap_inflate",
        r + ("merged_cut_spacing_audit", "minimum_combined_x_gap"),
        "1/100",
    )
    delete("output_fragment_delete", fragments)

    def duplicate_fragment(doc: dict[str, Any]) -> None:
        doc["result"]["stage3_output_fragment_rows"][-1] = copy.deepcopy(
            doc["result"]["stage3_output_fragment_rows"][0]
        )

    attacks.append(("output_fragment_duplicate", duplicate_fragment))
    add(
        "output_fragment_id",
        fragments + (0, "output_fragment_id"),
        "round123-stage3-output-fragment:" + "0" * 64,
    )
    add(
        "output_fragment_child",
        fragments + (0, "input_common_child_id"),
        "wrong",
    )
    add(
        "output_fragment_natural_index",
        fragments + (0, "stage3_natural_index_j"),
        1,
    )
    add(
        "output_fragment_recut_id",
        fragments + (0, "stage3_output_recut_instance_id"),
        "wrong",
    )
    add(
        "output_fragment_length_fake",
        fragments
        + (0, "normalized_stage3_output_length_strict_enclosure"),
        ["2", "2"],
    )
    add(
        "output_fragment_gap_inflate",
        fragments + (0, "source_x_open_gap_strict_lower"),
        "1",
    )
    add(
        "output_fragment_right_closed",
        fragments + (0, "upper_closed"),
        True,
    )
    add(
        "output_fragment_equal_mass",
        fragments + (0, "mass_is_not_sampled_or_assumed_equal"),
        False,
    )
    delete("partition_delete", partitions)
    add(
        "partition_output_count",
        partitions + (0, "output_fragment_count"),
        13,
    )
    add(
        "partition_output_ids",
        partitions + (0, "output_fragment_ids"),
        [],
    )
    add(
        "partition_mass_identity",
        partitions + (0, "symbolic_mass_partition_identity"),
        "all masses equal",
    )
    add(
        "partition_fragment_multiplier",
        partitions
        + (0, "fragment_count_does_not_multiply_mass_weighted_bound"),
        False,
    )
    add(
        "partition_inverse_length_multiplier",
        partitions + (0, "mass_weighted_inverse_length_assembly"),
        "216*(100/(3*delta))*M",
    )
    delete("leg_output_delete", legs)

    def duplicate_leg(doc: dict[str, Any]) -> None:
        doc["result"]["accepted_norm_leg_output_rows"][-1] = copy.deepcopy(
            doc["result"]["accepted_norm_leg_output_rows"][0]
        )

    attacks.append(("leg_output_duplicate", duplicate_leg))
    add(
        "leg_actual_target",
        legs + (0, "actual_collision_target"),
        "G[-1,-2]",
    )
    add("leg_actual_chart", legs + (0, "actual_collision_chart"), "S")
    add(
        "leg_orientation_flip",
        legs + (0, "adapted_output_coordinate_orientation"),
        "U1(x)=a1(x)-a1(0), strictly increasing",
    )
    add(
        "leg_derivative_inflate",
        legs
        + (0, "normalized_output_coordinate_derivative_strict_lower"),
        "7",
    )
    add(
        "leg_separation_inflate",
        legs + (0, "source_x_or_fragment_separation_strict_lower"),
        "1/100",
    )
    add("leg_output_member_count", legs + (0, "output_member_count"), 2)
    add("leg_output_member_delete", legs + (0, "output_member_ids"), [])
    add(
        "leg_output_length_fake",
        legs + (0, "normalized_output_member_length_strict_enclosures"),
        [["2", "2"]],
    )
    add(
        "leg_same_key_F10",
        legs + (0, "round122_same_key_slot_ids", "F10", 0),
        "wrong",
    )
    add(
        "leg_b3_collision_angle",
        legs + (0, "bypass_designated_b3_is_a_collision_angle"),
        True,
    )
    add(
        "theorem_alpha",
        theorem + ("closed_positive_input_domain", "alpha"),
        "1/2",
    )
    add(
        "theorem_normalization",
        theorem + ("closed_positive_input_domain", "normalization"),
        "integral rho=2",
    )
    add(
        "theorem_regular_density_cone",
        theorem + ("closed_positive_input_domain", "regularity"),
        "unbounded",
    )
    add(
        "theorem_pushforward_J",
        theorem
        + ("conditional_pushforward_contract", "adapted_Jacobian"),
        "J_*=1",
    )
    add(
        "theorem_conditional_density",
        theorem
        + ("conditional_pushforward_contract", "conditional_density"),
        "rho_j^+=rho",
    )
    add(
        "theorem_recurrence_wrong_parentheses",
        theorem + ("one_step_regularity_recurrence",),
        "Reg_alpha_out < (93/100)*(Reg_alpha_in+C_J)",
    )
    add(
        "theorem_equal_mass",
        theorem + ("mass_contract", "equal_mass_assumption"),
        True,
    )
    add(
        "theorem_F10_pays_F14",
        theorem + ("Round122_F10_zero_role",),
        "F10=0 pays F14",
    )
    add(
        "theorem_family_multiplier",
        theorem + ("family_inverse_length_bound",),
        "216*(100/(3*delta))*M",
    )
    add(
        "theorem_F14_value_33",
        theorem + ("F14_one_step_slot_value",),
        33,
    )
    add(
        "theorem_F14_margin_drop_delta",
        theorem + ("F14_one_step_exact_margin",),
        "2/3",
    )
    add(
        "theorem_roof_factor_five",
        theorem
        + (
            "roof_split_does_not_change_34_cubed_to_34_to_the_fifth",
        ),
        False,
    )
    add(
        "theorem_generic_34_to_fifth",
        theorem
        + ("generic_three_physical_leg_compositional_bound",),
        45435424,
    )
    add(
        "theorem_direct_bound_product",
        theorem + ("direct_exact_seed_three_leg_F14_bound",),
        39304,
    )
    add(
        "theorem_signed_factor_two",
        theorem + ("signed_extension_adds_no_factor_two",),
        False,
    )
    add(
        "theorem_cancellation",
        theorem + ("cancellation_is_not_used_to_reduce_cost",),
        False,
    )
    delete("F14_slot_delete", slots)

    def duplicate_slot(doc: dict[str, Any]) -> None:
        doc["result"]["gate5_F14_slot_rows"][-1] = copy.deepcopy(
            doc["result"]["gate5_F14_slot_rows"][0]
        )

    attacks.append(("F14_slot_duplicate", duplicate_slot))
    add("F14_slot_field", slots + (0, "field_index"), 15)
    add("F14_slot_value", slots + (0, "field_value_or_contract"), "33")
    add(
        "F14_slot_key",
        slots + (0, "immutable_slot_key", 3),
        "standard_family_operator_cost",
    )
    add("F14_slot_roof", slots + (0, "roof_level_j"), 99)
    add("F14_slot_leg", slots + (0, "physical_leg_factor_index"), 1)
    add(
        "F14_slot_same_key_F10",
        slots + (0, "round122_same_key_F10_slot_id"),
        "wrong",
    )
    add(
        "F14_slot_F10_pays",
        slots
        + (0, "Round122_F10_zero_is_dependency_only_not_payment_for_F14"),
        False,
    )
    add(
        "F14_slot_roof_multiplier",
        slots + (0, "transparent_wall_roof_split_adds_no_F14_factor"),
        False,
    )
    add(
        "F14_slot_b3_collision_angle",
        slots + (0, "bypass_designated_b3_is_a_collision_angle"),
        True,
    )
    add(
        "combined_slot_count_2016",
        r + ("combined_F1_F14_F16_slot_registry", "combined_slot_count"),
        2016,
    )
    add(
        "combined_fields_add_F15",
        r + ("combined_F1_F14_F16_slot_registry", "certified_field_indices"),
        list(range(1, 17)),
    )
    add(
        "count_ledger_fragment_count",
        r + ("count_ledger", "stage3_output_fragment_count"),
        215,
    )
    add(
        "count_ledger_slot_count",
        r + ("count_ledger", "new_F14_slot_count"),
        216,
    )
    add(
        "maturity_inflate",
        r + ("rank3_seed_child_field_maturity",),
        "16/18",
    )
    add(
        "install_F15",
        r + ("gate5_actual_child_field_status", "F15"),
        "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN",
    )
    add(
        "install_F17",
        r + ("gate5_actual_child_field_status", "F17"),
        "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN",
    )
    add(
        "install_F18",
        r + ("gate5_actual_child_field_status", "F18"),
        "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN",
    )
    add("global_gate_inflate", r + ("gate5_global_maturity",), "11/18")
    add(
        "complete_block_inflate",
        r + ("complete_18_field_block_count",),
        1,
    )
    add("gate5_block_inflate", r + ("gate5_block_count",), 1)
    add("CM2_inflate", r + ("cm2_verdict",), "GO_FOR_CLAIM")
    delete("strict_nonclaim_delete", r + ("strict_nonclaims",))
    add("scope_inflate", r + ("strict_scope",), "all Borel-b seeds")
    add("bool_as_precision", r + ("precision_bits",), True)

    rejected: list[str] = []
    for label, mutation in attacks:
        mutant = copy.deepcopy(baseline)
        mutation(mutant)
        resign_document(mutant, inputs)
        try:
            fast_semantic_contract(mutant, inputs)
        except (AssertionError, KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"semantic mutant accepted:{label}")
    require(
        len(rejected) == len(attacks) and len(rejected) >= 90,
        "semantic attack census",
    )
    return rejected


def strict_json_attacks(
    baseline: dict[str, Any], inputs: dict[str, Any]
) -> list[str]:
    oversized = "1" * 1025
    parser_cases = [
        ("top_duplicate_key", '{"a":1,"a":2}'),
        ("deep_duplicate_key", '{"a":{"b":1,"b":2}}'),
        ("NaN", '{"a":NaN}'),
        ("Infinity", '{"a":Infinity}'),
        ("negative_Infinity", '{"a":-Infinity}'),
        ("JSON_float", '{"a":1.0}'),
        ("JSON_exponent", '{"a":1e9999}'),
        ("top_array", "[]"),
        ("top_null", "null"),
        ("negative_zero", '{"a":-0}'),
        ("oversized_integer", '{"a":' + oversized + "}"),
        ("BOM", "\ufeff{}"),
        ("unpaired_surrogate", '{"a":"\\ud800"}'),
    ]
    rejected: list[str] = []
    for label, text in parser_cases:
        try:
            strict_json(text)
        except (TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"strict JSON mutant accepted:{label}")
    for label, path, value in (
        ("bool_as_integer", ("result", "precision_bits"), True),
        (
            "noncanonical_fraction",
            (
                "result",
                "stage3_endpoint_rows",
                0,
                "x_bracket_width",
            ),
            "01/2",
        ),
    ):
        mutant = copy.deepcopy(baseline)
        set_path(mutant, path, value)
        resign_document(mutant, inputs)
        text = json.dumps(mutant, sort_keys=True)
        try:
            parsed = strict_json(text)
            fast_semantic_contract(parsed, inputs)
        except (TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"strict contract mutant accepted:{label}")
    require(len(rejected) == 15, "strict JSON attack census")
    return rejected


def verify_certificate(
    certificate: Path,
    *,
    run_attacks: bool = True,
) -> dict[str, Any]:
    ctx.prec = VERIFIER_BITS
    document = strict_json(certificate.read_text(encoding="utf-8"))
    inputs = load_inputs()
    result = verify_static_contract(document, inputs)
    geometry = independent_geometry()
    verify_coordinate_contract(result, geometry)
    verify_endpoints(result, inputs["r121"], geometry)
    verify_natural_cells(result, inputs["r121"])
    verify_merged_cuts(result, inputs["r121"], geometry)
    _, partitions, partition_by_child = verify_fragments_and_partitions(
        result, inputs["r121"], geometry
    )
    leg_rows, leg_by_child = verify_leg_rows(
        result,
        inputs["r121"],
        inputs["r122"],
        geometry,
        partition_by_child,
    )
    verify_operator_theorem(result)
    f14_rows = verify_f14_slots(
        result,
        inputs["r121"],
        inputs["r122"],
        leg_by_child,
    )
    verify_combined_registry(
        result, inputs["r121"], inputs["r122"], f14_rows
    )
    verify_count_ledgers(result, partitions, leg_rows)
    semantic: list[str] = []
    strict: list[str] = []
    if run_attacks:
        semantic = semantic_attacks(document, inputs)
        strict = strict_json_attacks(document, inputs)
    verification = {
        "verdict": "PASS",
        "verification_precision_bits": VERIFIER_BITS,
        "certificate_sha256": sha256(certificate),
        "certificate_result_sha256": document["result_sha256"],
        "independently_verified_stage3_internal_cut_count": 192,
        "independently_verified_stage3_natural_cell_count": 193,
        "independently_verified_merged_internal_cut_count": 215,
        "independently_verified_stage3_output_fragment_count": 216,
        "independently_verified_input_partition_count": 24,
        "independently_verified_leg_output_row_count": 72,
        "independently_verified_F14_slot_count": 120,
        "combined_child_local_slot_count": 1800,
        "F14_one_step_slot_value": F14_ONE_STEP,
        "F14_generic_three_leg_compositional_bound": F14_GENERIC_THREE_LEG,
        "F14_direct_exact_seed_three_leg_bound": F14_DIRECT_THREE_LEG,
        "semantic_attack_count": len(semantic),
        "semantic_attack_labels": semantic,
        "strict_JSON_attack_count": len(strict),
        "strict_JSON_attack_labels": strict,
        "upstream_and_helper_pin_count": len(EXPECTED_PINS),
        "rank3_seed_child_field_maturity": "15/18",
        "remaining_uninstalled_child_fields": ["F15", "F17", "F18"],
        "gate5_global_maturity": "10/18",
        "complete_18_field_block_count": 0,
        "gate5_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": verification,
        "result_sha256": digest(verification),
    }


def write_verification(
    certificate: Path, output: Path | None, *, run_attacks: bool
) -> None:
    document = verify_certificate(certificate, run_attacks=run_attacks)
    text = json.dumps(document, sort_keys=True, indent=2, allow_nan=False)
    text += "\n"
    if output is None:
        print(text, end="")
    else:
        output.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--no-attacks",
        action="store_true",
        help="run the complete independent proof replay without mutation tests",
    )
    args = parser.parse_args()
    write_verification(
        args.certificate, args.output, run_attacks=not args.no_attacks
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
