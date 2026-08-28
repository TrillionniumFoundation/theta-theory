#!/usr/bin/env python3
"""Independent verifier for the Round125 exact-seed F17 certificate.

The verifier does not import or execute the Round125 producer, a Round125
proof helper, or any upstream producer module.  Frozen inputs are byte-pinned
and strict-parsed as data.  The verifier independently rebuilds all artificial
trace templates and incidences, the graph-current topology and algebraic
audit, all F17 slots, and the chained 2040-slot ledger.
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

import cm2_round122_rank3_exact_seed_physical_face_field_bridge_verifier as v122


HERE = Path(__file__).resolve().parent
CERTIFICATE = (
    HERE
    / "cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-2026-07-23.json"
)
OUTPUT = (
    HERE
    / "cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-verification-2026-07-23.json"
)
ROUND121 = (
    HERE
    / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
)
ROUND122 = (
    HERE
    / "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json"
)
ROUND123 = (
    HERE
    / "cm2-round123-rank3-exact-seed-stage3-output-properization-f14-2026-07-23.json"
)
ROUND124 = (
    HERE
    / "cm2-round124-rank3-exact-seed-standard-family-operator-f15-2026-07-23.json"
)
ROUND124_VERIFICATION = (
    HERE
    / "cm2-round124-rank3-exact-seed-standard-family-operator-f15-verification-2026-07-23.json"
)
ROUND43 = (
    HERE
    / "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
)
ROUND125_PRODUCER = (
    HERE / "cm2_round125_rank3_exact_seed_graph_current_dynamic_test_f17.py"
)

CERTIFICATE_SCHEMA = (
    "cm2.round125.rank3-exact-seed-graph-current-dynamic-test-f17.v2"
)
VERIFICATION_SCHEMA = (
    "cm2.round125.rank3-exact-seed-graph-current-dynamic-test-f17-verification.v1"
)
ROUND125_PRODUCER_SHA256 = (
    "e360c511c87f10483ee19cf566d9542f123a2fbdf37585d9954a9c33575b940b"
)
VERIFIER_BITS = 3072
PRODUCER_BITS = 1536
DELTA = Q(1, 10**90)
ENCLOSURE_GUARD = DELTA / 10**6

UPSTREAM_PINS = {
    "deliverables/cm2_round124_rank3_exact_seed_standard_family_operator_f15.py":
        "084634863c9ecb9dd16fe1c16ef7ae286315525509b5d703df48359426a291a5",
    "deliverables/cm2-round124-rank3-exact-seed-standard-family-operator-f15-2026-07-23.json":
        "ec2df85d5caf87f4bd25fa70c32afc5893bfbb147c3d0af21b3be9bc09c62b3b",
    "deliverables/cm2_round124_rank3_exact_seed_standard_family_operator_f15_verifier.py":
        "4a964cc016cee5de5cc42469bee96f87f61803f46973da24084e79a02e770a3f",
    "deliverables/cm2-round124-rank3-exact-seed-standard-family-operator-f15-verification-2026-07-23.json":
        "3c1987adcefd7986128b5a35c77babd3c00f760ef28d8b73f491961f0dff0ccd",
    "deliverables/cm2_round123_rank3_exact_seed_stage3_output_properization_f14.py":
        "e00b85d722e3784c0c2427ea0f7b32f8306b9d706b902b22df334b8aa9b00c38",
    "deliverables/cm2-round123-rank3-exact-seed-stage3-output-properization-f14-2026-07-23.json":
        "d3d45e32e45d1a37d5364c0d5fc1f34b537190c2450b7e8f9ead729dc77fe993",
    "deliverables/cm2_round122_rank3_exact_seed_physical_face_field_bridge.py":
        "44a64789635b8adfb597376d25afcbf8cb39dbaf0c2a19c4031bcbe78b3848f4",
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json":
        "a7ed51149916bbf0d181b9cd45114cd11d81a5d30e72fea50b3336d1ead22028",
    "deliverables/cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py":
        "30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed",
    "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json":
        "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e",
    "deliverables/cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json":
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "deliverables/cm2_gate5_return_word_three_norm_frontier_cert.py":
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    "deliverables/cm2-gate5-round41-physical-parameter-jet-envelopes-manifest-2026-07-19.json":
        "dd19fd73a01c3aa9868fb9e3c89a039a5e8c97d807b6f57048fddc35c744c2cc",
    "deliverables/cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json":
        "33e3fae4633b133ffcaeb7bd0e552629ecf8528b3648b93ce85d5420e141bef5",
    "deliverables/cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json":
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d",
    "deliverables/cm2-gate5-round47-regular-c1dual-f13-manifest-2026-07-19.json":
        "3415f8533865e9ed907df823c1453ee981f3f1f1d5e04333fc14a90ddb2884d0",
    "deliverables/cm2-gate5-round49-typed-measure-f10-f17-frontier-manifest-2026-07-19.json":
        "1a53a0bac41f6c0d6f8155c69b67daf31337b5f13578af9fb9f497d16277d6ad",
    "deliverables/cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json":
        "1c4437a3c237739bacb823f0a9309626bea06b6f6562c1e268d589ed7debb7c5",
    "deliverables/cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json":
        "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b",
    "deliverables/cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json":
        "8cacd8daa582c522a175cca3f24c7da1cb10c47f860b20645a365b27678d4590",
    "deliverables/cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.json":
        "9abdc07cb0618f4a81b8e5591d8de83da7cce2c6d6a82fa41c834dd46c28412c",
}

INDEPENDENT_VERIFIER_PINS = {
    "deliverables/cm2_round121_rank3_exact_seed_three_leg_recut_f5f6_verifier.py":
        "d35c0e04b9d339c1271533abdefa5addcb73096b70abdec94d60e475daa45e95",
    "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json":
        "ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80",
    "deliverables/cm2_round122_rank3_exact_seed_physical_face_field_bridge_verifier.py":
        "bcf6e34398dcd2fd4cb6bb23aec649db5df75d26a80f307e58521d8ef439d31e",
    "deliverables/cm2-round122-rank3-exact-seed-physical-face-field-bridge-verification-2026-07-23.json":
        "aa0eca5e14fccbeeaad74d075cce0f10ee01f4caf8fccd0e9130ccc0e5cba82b",
}

F17_BY_STAGE = {0: 4915200, 1: 2457600, 2: 2457600}
RELATIVE_CENTER_ETA = {0: 1, 1: -1, 2: 0}
TARGET_RADII = {0: Q(4, 25), 1: Q(9, 25), 2: Q(9, 25)}
RAW_INCIDENCE_RANK = {0: 15, 1: 14, 2: 14}
ADAPTED_X_DERIVATIVE = {
    0: DELTA,
    1: 7 * DELTA,
    2: 18 * DELTA,
}
ADAPTED_COORDINATE = {
    0: "source-u0-exact-delta-x",
    1: "image-U1",
    2: "image-U2",
}
RECIPIENT_COMPONENTS = (
    ("G:W", "G[0,0]", "W"),
    ("W:N", "W[-1,-1]", "N"),
    ("G:S", "G[0,0]", "S"),
    ("G:N", "G[-1,-2]", "N"),
)
SOURCE_COMPONENT_BY_STAGE = {0: "G:W", 1: "W:N", 2: "G:S"}
TARGET_COMPONENT_BY_STAGE = {0: "W:N", 1: "G:S", 2: "G:N"}
SOURCE_INJECTION = {
    stage: 25 * (1 << RAW_INCIDENCE_RANK[stage]) + 27
    for stage in range(3)
}
END_TO_END = {
    stage: SOURCE_INJECTION[stage] * F17_BY_STAGE[stage]
    for stage in range(3)
}
THREE_LEG_PRODUCT = (
    F17_BY_STAGE[0] * F17_BY_STAGE[1] * F17_BY_STAGE[2]
)
GLOBAL_THRESHOLD = Q(7961063, 7800000)


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


def qstr(value: Q | int) -> str:
    return str(Q(value))


def parse_q(value: Any, *, nonnegative: bool | None = None) -> Q:
    require(type(value) is str, "fraction type")
    require(
        re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", value)
        is not None,
        "canonical fraction syntax",
    )
    result = Q(value)
    require(str(result) == value, "reduced canonical fraction")
    if nonnegative is True:
        require(result >= 0, "nonnegative fraction")
    if nonnegative is False:
        require(result > 0, "positive fraction")
    return result


def parse_interval(value: Any, label: str) -> tuple[Q, Q]:
    require(type(value) is list and len(value) == 2, f"{label} interval")
    lower, upper = parse_q(value[0]), parse_q(value[1])
    require(lower <= upper, f"{label} interval order")
    return lower, upper


def interval_square(value: tuple[Q, Q]) -> tuple[Q, Q]:
    lower, upper = value
    if lower <= 0 <= upper:
        return Q(0), max(lower * lower, upper * upper)
    return min(lower * lower, upper * upper), max(
        lower * lower, upper * upper
    )


def interval_add(
    left: tuple[Q, Q], right: tuple[Q, Q]
) -> tuple[Q, Q]:
    return left[0] + right[0], left[1] + right[1]


def reject_float(_value: str) -> Any:
    raise VerificationError("JSON floating-point numbers are forbidden")


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def parse_strict_bytes(raw: bytes) -> Any:
    require(not raw.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM")
    text = raw.decode("utf-8", errors="strict")
    value = json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_float=reject_float,
        parse_constant=reject_float,
    )
    return value


def strict_document(path: Path, schema: str) -> dict[str, Any]:
    value = parse_strict_bytes(path.read_bytes())
    require(type(value) is dict, f"top object:{path.name}")
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"closed envelope:{path.name}",
    )
    require(value["schema"] == schema, f"schema:{path.name}")
    require(type(value["result"]) is dict, f"result type:{path.name}")
    require(
        value["result_sha256"] == digest(value["result"]),
        f"result digest:{path.name}",
    )
    return value


def strict_round43_manifest() -> dict[str, Any]:
    value = parse_strict_bytes(ROUND43.read_bytes())
    require(type(value) is dict, "Round43 manifest type")
    require(
        set(value)
        == {
            "certificate_sha256",
            "dependencies",
            "result",
            "schema",
            "verdict",
            "verifier_sha256",
        },
        "Round43 closed manifest",
    )
    require(
        value["schema"]
        == "cm2.gate5.round43-duhamel-eulerian-charge-frontier.v1.manifest.v1",
        "Round43 manifest schema",
    )
    require(type(value["result"]) is dict, "Round43 result type")
    require(
        value["result"]["schema"]
        == "cm2.gate5.round43-duhamel-eulerian-charge-frontier.v1",
        "Round43 result schema",
    )
    require(
        value["verdict"]["CM2"] == "NO-GO_FOR_CLAIM"
        and value["verdict"]["Gate5_maturity"] == "7/18_UNCHANGED",
        "Round43 nonpromotion state",
    )
    return value


def validate_row(row: Any, label: str) -> None:
    require(type(row) is dict, f"{label} type")
    require(type(row.get("row_sha256")) is str, f"{label} digest type")
    payload = {key: value for key, value in row.items()
               if key != "row_sha256"}
    require(row["row_sha256"] == digest(payload), f"{label} digest")


def coordinate(row: dict[str, Any]) -> tuple[str, str, int]:
    return (
        row["official_word_key_id"],
        row["refined_homogeneous_subbranch_id"],
        row["roof_level_j"],
    )


def verify_byte_pins() -> None:
    for relative, expected in UPSTREAM_PINS.items():
        path = HERE.parent / relative
        require(path.is_file() and not path.is_symlink(), f"pin:{relative}")
        require(sha256(path) == expected, f"byte pin:{relative}")
    for relative, expected in INDEPENDENT_VERIFIER_PINS.items():
        path = HERE.parent / relative
        require(
            path.is_file() and not path.is_symlink(),
            f"independent verifier pin:{relative}",
        )
        require(
            sha256(path) == expected,
            f"independent verifier byte pin:{relative}",
        )
    require(
        ROUND125_PRODUCER.is_file()
        and not ROUND125_PRODUCER.is_symlink()
        and sha256(ROUND125_PRODUCER) == ROUND125_PRODUCER_SHA256,
        "Round125 producer byte pin",
    )


def load_upstream() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    verify_byte_pins()
    r121 = strict_document(
        ROUND121,
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
    )["result"]
    r122 = strict_document(
        ROUND122,
        "cm2.round122.rank3-exact-seed-physical-face-field-bridge.v1",
    )["result"]
    r123 = strict_document(
        ROUND123,
        "cm2.round123.rank3-exact-seed-stage3-output-properization-f14.v1",
    )["result"]
    r124 = strict_document(
        ROUND124,
        "cm2.round124.rank3-exact-seed-standard-family-operator-f15.v1",
    )["result"]
    r124v = strict_document(
        ROUND124_VERIFICATION,
        "cm2.round124.rank3-exact-seed-standard-family-operator-f15-verification.v1",
    )["result"]
    r43 = strict_round43_manifest()["result"]
    require(
        r124v["status"] == "PASS"
        and r124v["semantic_mutation_test_count"] == 154
        and r124v["strict_json_attack_count"] == 15,
        "Round124 verified state",
    )
    require(
        r124["rank3_seed_child_field_maturity"] == "16/18"
        and r124["count_ledger"]["combined_child_local_slot_count"] == 1920
        and r124["gate5_actual_child_field_status"]["F17"]
        == "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
        "Round124 F17 frontier",
    )
    require(
        r124["gate5_global_maturity"] == "10/18"
        and r124["complete_18_field_block_count"] == 0
        and r124["gate5_block_count"] == 0
        and r124["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "Round124 safety state",
    )
    require(
        len(r121["common_refinement_rows"]) == 24
        and len(r122["child_face_incidence_rows"]) == 24
        and len(r122["recut_face_trace_rows"]) == 48
        and len(r123["merged_internal_cut_rows"]) == 215
        and len(r123["stage3_output_fragment_rows"]) == 216
        and len(r124["standard_family_leg_operator_rows"]) == 72
        and len(r124["gate5_F15_slot_rows"]) == 120,
        "upstream census",
    )
    relevant = (
        (r122["child_face_incidence_rows"], "Round122 incidence"),
        (r122["recut_face_trace_rows"], "Round122 trace"),
        (r122["stationary_outer_face_rows"], "Round122 outer face"),
        (r122["parameterized_recut_face_rows"], "Round122 recut face"),
        (r123["stage3_output_fragment_rows"], "Round123 fragment"),
        (r124["standard_family_leg_operator_rows"], "Round124 family"),
        (r124["gate5_F15_slot_rows"], "Round124 F15"),
    )
    for rows, label in relevant:
        for row in rows:
            validate_row(row, label)
    rank_law = r43["one_step_area_eulerian_generator"]
    require(
        rank_law["cross_colour_pointwise_bounds"]["incidence_rank"]
        == "1/c_target<=2^B"
        and rank_law["cross_colour_pointwise_bounds"]["l1_generator"]
        == "abs_X_r+abs_X_p<=25*2^B"
        and rank_law["same_colour_branch"] == "X_s=0",
        "Round43 generator laws",
    )
    return r121, r122, r123, r124, r124v, r43


def graph_current_leg_id(child: str, stage: int) -> str:
    return "round125-graph-current-leg:" + digest(
        ["round125-graph-current-leg-v1", child, stage]
    )


def recipient_component_id(component_key: str) -> str:
    return "round125-recipient-component:" + digest(
        ["round125-recipient-component-v1", component_key]
    )


def recipient_pullback_map_id(child: str, stage: int) -> str:
    return "round125-recipient-pullback-map:" + digest(
        ["round125-recipient-pullback-map-v1", child, stage]
    )


def source_injection_contract_id(stage: int) -> str:
    return "round125-source-injection-contract:" + digest(
        ["round125-source-injection-contract-v1", stage]
    )


def source_injection_derivation_id(stage: int) -> str:
    return "round125-source-injection-derivation:" + digest(
        ["round125-source-injection-derivation-v2", stage]
    )


def input_trace_id(
    child: str, stage: int, side: str, source_trace: str
) -> str:
    return "round125-input-artificial-trace:" + digest(
        [
            "round125-input-artificial-trace-v1",
            child,
            stage,
            side,
            source_trace,
        ]
    )


def output_trace_id(fragment: str, side: str) -> str:
    return "round125-stage3-output-trace:" + digest(
        ["round125-stage3-output-trace-v1", fragment, side]
    )


def stage3_velocity_witness_id(
    endpoint: str, cut_canonical_sha256: str
) -> str:
    return "round125-stage3-endpoint-velocity-witness:" + digest(
        [
            "round125-stage3-endpoint-velocity-witness-v2",
            endpoint,
            cut_canonical_sha256,
        ]
    )


def stage3_density_witness_id(
    child: str,
    input_materialized_recut_instance_id: str,
    input_member_tag_template: str,
    endpoint: str,
    cut_canonical_sha256: str,
) -> str:
    return "round125-stage3-unnormalized-density-witness:" + digest(
        [
            "round125-stage3-unnormalized-density-witness-v2",
            child,
            input_materialized_recut_instance_id,
            input_member_tag_template,
            endpoint,
            cut_canonical_sha256,
        ]
    )


def f17_slot_id(immutable_key: list[Any]) -> str:
    return "round125-gate5-f17-slot:" + digest(
        ["round125-gate5-f17-slot-v1", immutable_key]
    )


def incidence_rank_from_f11(value: int) -> int:
    require(type(value) is int and value > 0, "positive integer F11")
    require(value % 150 == 0, "F11 divisible by 150")
    quotient = value // 150
    require(
        quotient > 0 and quotient & (quotient - 1) == 0,
        "F11 quotient power of two",
    )
    return quotient.bit_length() - 1


def build_input_traces(
    r121: dict[str, Any],
    r122: dict[str, Any],
    r124: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    adapted = r121["stage_adapted_coordinate_contract"]
    require(
        r121["source_adapted_cell_rows"][0]["u0_x_derivative_exact"]
        == "1e-90",
        "source adapted derivative",
    )
    require(
        Q(
            adapted["whole_cell_normalized_derivative_enclosures"][
                "U1_prime_over_delta"
            ][1]
        )
        < 7,
        "U1 derivative",
    )
    require(
        Q(
            adapted["whole_cell_normalized_derivative_enclosures"][
                "U2_prime_over_delta"
            ][1]
        )
        < 18,
        "U2 derivative",
    )
    incidences = sorted(
        r122["child_face_incidence_rows"],
        key=lambda row: row["common_rank"],
    )
    require(
        [row["common_rank"] for row in incidences] == list(range(24)),
        "input child rank order",
    )
    trace_map = {
        row["trace_id"]: row for row in r122["recut_face_trace_rows"]
    }
    face_map = {
        row["face_id"]: row
        for row in (
            r122["stationary_outer_face_rows"]
            + r122["parameterized_recut_face_rows"]
        )
    }
    family_map = {
        (row["common_child_id"], row["stage"]): row
        for row in r124["standard_family_leg_operator_rows"]
    }
    rows: list[dict[str, Any]] = []
    lookup: dict[tuple[int, int, str], dict[str, Any]] = {}
    for incidence in incidences:
        rank = incidence["common_rank"]
        child = incidence["common_child_id"]
        for stage in range(3):
            family = family_map[(child, stage)]
            input_contract = family["input_member_contract"]
            require(
                input_contract["geometry_carrier"]
                == family["input_materialized_recut_instance_id"]
                and input_contract["tag"]
                == "<input-standard-family-member-id>",
                "Round124 input family contract",
            )
            for side, orientation in (("lower", -1), ("upper", 1)):
                source_trace = incidence[f"{side}_trace_id"]
                source_row = trace_map[source_trace]
                face = face_map[incidence[f"{side}_face_id"]]
                actual_speed = Q(
                    face["implicit_x_s_first_derivative_actual_abs_upper"]
                )
                jacobian = ADAPTED_X_DERIVATIVE[stage]
                coefficient = actual_speed * jacobian
                require(
                    0 <= actual_speed < 13
                    and 0 < jacobian < 1
                    and coefficient < 13,
                    "input trace coefficient",
                )
                row = {
                    "trace_id": input_trace_id(
                        child, stage, side, source_trace
                    ),
                    "trace_id_semantics": (
                        "geometry/operator template; an actual trace instance"
                        " additionally carries an immutable source-family-member tag"
                    ),
                    "trace_instance_id_constructor": (
                        "sha256(round125-input-trace-instance-v1,"
                        " trace_id,source_family_member_tag)"
                    ),
                    "common_child_id": child,
                    "common_rank": rank,
                    "stage": stage,
                    "round124_standard_family_leg_operator_row_id":
                        family["standard_family_leg_operator_row_id"],
                    "round124_standard_family_leg_operator_row_sha256":
                        family["row_sha256"],
                    "input_materialized_recut_instance_id":
                        family["input_materialized_recut_instance_id"],
                    "source_family_member_tag_template":
                        input_contract["tag"],
                    "source_family_tag_domain_id":
                        "round125-input-family-tag-domain:"
                        + digest(
                            [
                                "round125-input-family-tag-domain-v1",
                                family[
                                    "standard_family_leg_operator_row_id"
                                ],
                                family[
                                    "input_materialized_recut_instance_id"
                                ],
                                input_contract["tag"],
                            ]
                        ),
                    "round124_input_member_contract_canonical_sha256":
                        digest(input_contract),
                    "side": side,
                    "orientation_sign": orientation,
                    "round122_source_trace_id": source_trace,
                    "round122_face_id": face["face_id"],
                    "round122_trace_row_sha256": source_row["row_sha256"],
                    "source_face_speed_actual_abs_upper": qstr(actual_speed),
                    "source_face_speed_claimed_strict_upper": "13",
                    "stage_adapted_coordinate_id":
                        ADAPTED_COORDINATE[stage],
                    "stage_adapted_coordinate_x_derivative_bound_value":
                        qstr(jacobian),
                    "stage_adapted_coordinate_x_derivative_bound_semantics":
                        "EXACT" if stage == 0 else "STRICT_UPPER",
                    "source_x_to_adapted_trace_coefficient_formula": (
                        "|v_face^(x)|*J_*^in,"
                        " J_*^in=|partial_x ell_*|"
                    ),
                    "source_x_to_adapted_trace_coefficient_actual_upper":
                        qstr(coefficient),
                    "source_x_to_adapted_trace_coefficient_strict_upper":
                        "13",
                    "exact_typed_trace_atom": (
                        "push orientation_sign*v_face^(x)*J_*^in*M_i*rho_i"
                        " at the source-x face through the materialized stage"
                        " embedding into the physical chart"
                    ),
                    "unnormalized_trace_density": (
                        "orientation_sign*v_face^(x)*J_*^in*M_i*rho_i"
                        " restricted to the face"
                    ),
                    "source_x_face_velocity_symbol":
                        "v_face^(x)=d_s x_face",
                    "adapted_input_density_jacobian_symbol":
                        "J_*^in=|partial_x ell_*|",
                    "adapted_jacobian_factor_is_not_omitted": True,
                    "bulk_motion_and_cut_face_motion_are_separately_typed":
                        True,
                    "source_family_member_tag_is_preserved": True,
                    "source_family_member_tag_is_bound_to_Round124_input_member_contract":
                        True,
                    "cross_family_member_tag_cancellation_allowed": False,
                    "normalized_density_and_carrier_length_below_one_imply":
                        "M_i<=M_i*||rho_i||_infinity",
                    "artificial_not_physical": True,
                    "physical_empty_crosswalk_does_not_erase_this_trace":
                        True,
                    "retained_until_an_opposite_equal_unnormalized_trace_is_joined":
                        True,
                }
                row["row_sha256"] = digest(row)
                rows.append(row)
                lookup[(rank, stage, side)] = row

    incidence_rows: list[dict[str, Any]] = []
    for stage in range(3):
        for rank in range(23):
            left = lookup[(rank, stage, "upper")]
            right = lookup[(rank + 1, stage, "lower")]
            require(
                left["round122_face_id"] == right["round122_face_id"],
                "adjacent input face",
            )
            require(
                left["source_family_tag_domain_id"]
                != right["source_family_tag_domain_id"],
                "distinct adjacent input family tag domains",
            )
            row = {
                "incidence_id": "round125-input-trace-incidence:" + digest(
                    [
                        "round125-input-trace-incidence-v1",
                        stage,
                        rank,
                        left["trace_id"],
                        right["trace_id"],
                    ]
                ),
                "stage": stage,
                "lower_common_rank": rank,
                "upper_common_rank": rank + 1,
                "shared_round122_face_id": left["round122_face_id"],
                "left_upper_trace_id": left["trace_id"],
                "right_lower_trace_id": right["trace_id"],
                "left_input_materialized_recut_instance_id": left[
                    "input_materialized_recut_instance_id"
                ],
                "right_input_materialized_recut_instance_id": right[
                    "input_materialized_recut_instance_id"
                ],
                "left_round124_family_row_sha256": left[
                    "round124_standard_family_leg_operator_row_sha256"
                ],
                "right_round124_family_row_sha256": right[
                    "round124_standard_family_leg_operator_row_sha256"
                ],
                "left_and_right_input_geometric_carriers_are_distinct":
                    left["input_materialized_recut_instance_id"]
                    != right["input_materialized_recut_instance_id"],
                "left_source_family_tag_domain_id": left[
                    "source_family_tag_domain_id"
                ],
                "right_source_family_tag_domain_id": right[
                    "source_family_tag_domain_id"
                ],
                "left_and_right_are_distinct_input_family_tag_domains":
                    True,
                "orientations_are_opposite": True,
                "adapted_jacobian_factor_present_on_both_trace_rows": True,
                "cancellation_before_total_variation_iff_unnormalized_densities_match":
                    True,
                "arbitrary_densities_on_distinct_input_children_are_assumed_equal":
                    False,
                "unconditional_cancellation_claimed": False,
                "both_traces_remain_typed": True,
                "trace_instances_are_compared_only_with_equal_source_family_member_tag":
                    True,
                "cross_tag_cancellation_forbidden": True,
            }
            row["row_sha256"] = digest(row)
            incidence_rows.append(row)
    require(
        len(rows) == len({row["trace_id"] for row in rows}) == 144,
        "input trace census",
    )
    require(
        len(incidence_rows)
        == len({row["incidence_id"] for row in incidence_rows})
        == 69,
        "input incidence census",
    )
    return rows, incidence_rows


def build_output_traces(
    r123: dict[str, Any],
    r122: dict[str, Any],
    r124: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fragments = sorted(
        r123["stage3_output_fragment_rows"],
        key=lambda row: row["fragment_rank"],
    )
    require(
        [row["fragment_rank"] for row in fragments] == list(range(216)),
        "output fragment order",
    )
    cut_map = {
        row["endpoint_id"]: row for row in r123["merged_internal_cut_rows"]
    }
    source_incidence = {
        row["common_child_id"]: row
        for row in r122["child_face_incidence_rows"]
    }
    source_faces = {
        row["face_id"]: row
        for row in (
            r122["stationary_outer_face_rows"]
            + r122["parameterized_recut_face_rows"]
        )
    }
    stage2_family_map = {
        row["common_child_id"]: row
        for row in r124["standard_family_leg_operator_rows"]
        if row["stage"] == 2
    }
    require(len(stage2_family_map) == 24, "Round124 stage2 families")
    rows: list[dict[str, Any]] = []
    lookup: dict[tuple[int, str], dict[str, Any]] = {}
    for fragment in fragments:
        for side, orientation in (("lower", -1), ("upper", 1)):
            endpoint = fragment[f"source_x_{side}_endpoint_id"]
            family = stage2_family_map[
                fragment["input_common_child_id"]
            ]
            input_contract = family["input_member_contract"]
            require(
                input_contract["geometry_carrier"]
                == family["input_materialized_recut_instance_id"]
                and input_contract["tag"]
                == "<input-standard-family-member-id>",
                "Round124 stage2 input family contract",
            )
            old_incidence = source_incidence[
                fragment["input_common_child_id"]
            ]
            old_face_id = old_incidence[f"{side}_face_id"]
            old_trace_id = old_incidence[f"{side}_trace_id"]
            old_face = source_faces[old_face_id]
            is_new = (
                endpoint in cut_map
                and cut_map[endpoint]["origin"]
                == "ROUND123_STAGE3_OUTPUT_CUT"
            )
            cut = cut_map.get(endpoint)
            cut_canonical_sha256 = digest(cut) if cut is not None else None
            if is_new:
                face_id = None
                trace_id = None
                face_sha = None
                velocity_contract = (
                    "v_endpoint=-(partial_s U3)/(partial_x U3) at the unique"
                    " U3=j*delta root on this tagged input member; the same"
                    " root velocity is used by its two sides"
                )
                endpoint_evidence = cut_canonical_sha256
            else:
                require(
                    old_face["round121_s0_endpoint_id"] == endpoint,
                    "old source-face endpoint crosswalk",
                )
                face_id = old_face_id
                trace_id = old_trace_id
                face_sha = old_face["row_sha256"]
                velocity_contract = (
                    "stage3 physical pushforward of the pinned Round122"
                    " source-face trace and its exact implicit-root velocity"
                )
                endpoint_evidence = (
                    cut_canonical_sha256
                    if cut_canonical_sha256 is not None
                    else old_face["row_sha256"]
                )
            require(
                type(endpoint_evidence) is str,
                "output endpoint evidence digest",
            )
            row = {
                "trace_id": output_trace_id(
                    fragment["output_fragment_id"], side
                ),
                "trace_id_semantics": (
                    "geometry/operator template; an actual trace instance"
                    " additionally carries an immutable source-family-member tag"
                ),
                "trace_instance_id_constructor": (
                    "sha256(round125-stage3-trace-instance-v1,"
                    " trace_id,source_family_member_tag)"
                ),
                "fragment_id": fragment["output_fragment_id"],
                "fragment_rank": fragment["fragment_rank"],
                "input_common_child_id":
                    fragment["input_common_child_id"],
                "input_common_rank": fragment["input_common_rank"],
                "side": side,
                "orientation_sign": orientation,
                "source_x_endpoint_id": endpoint,
                "stage3_output_recut_instance_id": fragment[
                    "stage3_output_recut_instance_id"
                ],
                "round124_stage2_standard_family_leg_operator_row_id":
                    family["standard_family_leg_operator_row_id"],
                "round124_stage2_standard_family_leg_operator_row_sha256":
                    family["row_sha256"],
                "source_input_materialized_recut_instance_id":
                    family["input_materialized_recut_instance_id"],
                "source_input_family_member_tag_template":
                    input_contract["tag"],
                "source_input_family_tag_domain_id":
                    "round125-stage2-input-family-tag-domain:"
                    + digest(
                        [
                            "round125-stage2-input-family-tag-domain-v1",
                            family[
                                "standard_family_leg_operator_row_id"
                            ],
                            family[
                                "input_materialized_recut_instance_id"
                            ],
                            input_contract["tag"],
                        ]
                    ),
                "round124_stage2_input_member_contract_canonical_sha256":
                    digest(input_contract),
                "round122_source_face_id": face_id,
                "round122_source_trace_id": trace_id,
                "round122_source_face_row_sha256": face_sha,
                "round123_merged_cut_origin":
                    cut["origin"] if cut is not None else None,
                "round123_merged_cut_natural_index_j":
                    cut["natural_index_j"] if cut is not None else None,
                "round123_merged_cut_x_dyadic_bracket":
                    cut["x_dyadic_bracket"] if cut is not None else None,
                "round123_merged_cut_canonical_sha256":
                    cut_canonical_sha256,
                "endpoint_evidence_canonical_sha256":
                    endpoint_evidence,
                "trace_velocity_contract": velocity_contract,
                "endpoint_velocity_witness_id":
                    stage3_velocity_witness_id(
                        endpoint, endpoint_evidence
                    ),
                "unnormalized_density_witness_id":
                    stage3_density_witness_id(
                        fragment["input_common_child_id"],
                        family["input_materialized_recut_instance_id"],
                        input_contract["tag"],
                        endpoint,
                        endpoint_evidence,
                    ),
                "endpoint_velocity_witness_instance_id_constructor": (
                    "sha256(round125-stage3-velocity-instance-v1,"
                    " endpoint_velocity_witness_id,"
                    " source_family_member_tag)"
                ),
                "unnormalized_density_witness_instance_id_constructor": (
                    "sha256(round125-stage3-density-instance-v1,"
                    " unnormalized_density_witness_id,"
                    " source_family_member_tag)"
                ),
                "witness_instance_requires_equal_source_family_member_tag":
                    True,
                "cancellation_uses_Round124_input_member_tag_before_output_fragment_tagging":
                    True,
                "unnormalized_trace_density": (
                    "orientation_sign*v_endpoint*M_fragment*rho_fragment"
                    " = orientation_sign*v_endpoint*M_input*rho_input/J_star"
                ),
                "output_density_jacobian_symbol":
                    "J_star=|partial ell_*^out/partial ell_*^in|",
                "Jacobian_factor_is_present_in_unnormalized_density": True,
                "conditional_normalization_is_undone_by_fragment_mass":
                    True,
                "source_family_member_tag_is_preserved": True,
                "source_family_member_tag_is_bound_to_Round124_stage2_input_contract":
                    True,
                "cross_family_member_tag_cancellation_allowed": False,
                "artificial_not_physical": True,
                "row_source_sha256": fragment["row_sha256"],
            }
            row["row_sha256"] = digest(row)
            rows.append(row)
            lookup[(fragment["fragment_rank"], side)] = row

    incidence_rows: list[dict[str, Any]] = []
    cancelled = retained = 0
    for rank in range(215):
        left = lookup[(rank, "upper")]
        right = lookup[(rank + 1, "lower")]
        endpoint = left["source_x_endpoint_id"]
        require(
            endpoint == right["source_x_endpoint_id"],
            "shared output endpoint",
        )
        cut = cut_map[endpoint]
        same_input = (
            left["input_common_child_id"]
            == right["input_common_child_id"]
        )
        new_cut = cut["origin"] == "ROUND123_STAGE3_OUTPUT_CUT"
        require(same_input == new_cut, "output incidence typing")
        same_input_recut = (
            left["source_input_materialized_recut_instance_id"]
            == right["source_input_materialized_recut_instance_id"]
        )
        same_input_family = (
            left[
                "round124_stage2_standard_family_leg_operator_row_sha256"
            ]
            == right[
                "round124_stage2_standard_family_leg_operator_row_sha256"
            ]
        )
        same_input_tag_domain = (
            left["source_input_family_tag_domain_id"]
            == right["source_input_family_tag_domain_id"]
        )
        distinct_output_cells = (
            left["stage3_output_recut_instance_id"]
            != right["stage3_output_recut_instance_id"]
        )
        require(
            distinct_output_cells == same_input,
            "output natural-cell distinction",
        )
        require(
            (not same_input or same_input_recut)
            and same_input_family == same_input
            and same_input_tag_domain == same_input,
            "output input-family typing",
        )
        cut_canonical_sha256 = digest(cut)
        require(
            left["round123_merged_cut_canonical_sha256"]
            == right["round123_merged_cut_canonical_sha256"]
            == cut_canonical_sha256,
            "output shared cut digest",
        )
        cancelled += int(same_input)
        retained += int(not same_input)
        velocity_equal = (
            left["endpoint_velocity_witness_id"]
            == right["endpoint_velocity_witness_id"]
        )
        density_equal = (
            left["unnormalized_density_witness_id"]
            == right["unnormalized_density_witness_id"]
        )
        require(velocity_equal, "velocity witness equality")
        require(density_equal == same_input, "density witness equality")
        row = {
            "incidence_id": "round125-stage3-output-incidence:" + digest(
                [
                    "round125-stage3-output-incidence-v1",
                    endpoint,
                    left["trace_id"],
                    right["trace_id"],
                ]
            ),
            "cut_rank": rank,
            "endpoint_id": endpoint,
            "cut_origin": cut["origin"],
            "left_fragment_id": left["fragment_id"],
            "right_fragment_id": right["fragment_id"],
            "left_stage3_output_recut_instance_id":
                left["stage3_output_recut_instance_id"],
            "right_stage3_output_recut_instance_id":
                right["stage3_output_recut_instance_id"],
            "adjacent_output_natural_cells_are_distinct":
                distinct_output_cells,
            "new_stage3_cut_iff_distinct_adjacent_output_natural_cells":
                new_cut == distinct_output_cells,
            "left_upper_trace_id": left["trace_id"],
            "right_lower_trace_id": right["trace_id"],
            "orientations_are_opposite": True,
            "same_input_common_child": same_input,
            "left_source_input_materialized_recut_instance_id": left[
                "source_input_materialized_recut_instance_id"
            ],
            "right_source_input_materialized_recut_instance_id": right[
                "source_input_materialized_recut_instance_id"
            ],
            "same_input_materialized_recut_instance":
                same_input_recut,
            "left_round124_stage2_family_row_id": left[
                "round124_stage2_standard_family_leg_operator_row_id"
            ],
            "right_round124_stage2_family_row_id": right[
                "round124_stage2_standard_family_leg_operator_row_id"
            ],
            "left_round124_stage2_family_row_sha256": left[
                "round124_stage2_standard_family_leg_operator_row_sha256"
            ],
            "right_round124_stage2_family_row_sha256": right[
                "round124_stage2_standard_family_leg_operator_row_sha256"
            ],
            "same_round124_stage2_input_family_row":
                same_input_family,
            "source_input_family_member_tag_template": left[
                "source_input_family_member_tag_template"
            ],
            "left_source_input_family_tag_domain_id": left[
                "source_input_family_tag_domain_id"
            ],
            "right_source_input_family_tag_domain_id": right[
                "source_input_family_tag_domain_id"
            ],
            "same_Round124_input_family_tag_domain":
                same_input_tag_domain,
            "round123_merged_cut_canonical_sha256":
                cut_canonical_sha256,
            "round123_merged_cut_natural_index_j":
                cut["natural_index_j"],
            "cut_root_velocity_law": (
                "v_endpoint=-(partial_s U3)/(partial_x U3)"
                " at U3=j*delta"
                if new_cut
                else "pinned Round121 input-cut velocity pushed through stage3"
            ),
            "unnormalized_density_match_certified": (
                same_input
                and same_input_family
                and same_input_tag_domain
            ),
            "endpoint_velocity_match_certified": True,
            "left_endpoint_velocity_witness_id":
                left["endpoint_velocity_witness_id"],
            "right_endpoint_velocity_witness_id":
                right["endpoint_velocity_witness_id"],
            "endpoint_velocity_witness_ids_equal": velocity_equal,
            "left_endpoint_velocity_witness_instance_id_constructor":
                left[
                    "endpoint_velocity_witness_instance_id_constructor"
                ],
            "right_endpoint_velocity_witness_instance_id_constructor":
                right[
                    "endpoint_velocity_witness_instance_id_constructor"
                ],
            "left_unnormalized_density_witness_id":
                left["unnormalized_density_witness_id"],
            "right_unnormalized_density_witness_id":
                right["unnormalized_density_witness_id"],
            "unnormalized_density_witness_ids_equal": density_equal,
            "left_unnormalized_density_witness_instance_id_constructor":
                left[
                    "unnormalized_density_witness_instance_id_constructor"
                ],
            "right_unnormalized_density_witness_instance_id_constructor":
                right[
                    "unnormalized_density_witness_instance_id_constructor"
                ],
            "conditional_normalized_densities_need_not_match": True,
            "cancelled_before_total_variation": same_input,
            "retained_as_two_typed_traces_when_not_matched":
                not same_input,
            "cancellation_is_fibrewise_in_one_source_family_member_tag":
                True,
            "equal_source_family_member_tag_is_required": True,
            "cancellation_occurs_before_distinct_output_member_tags_are_assigned":
                True,
            "witness_instance_comparison_rule": (
                "compare velocity and unnormalized-density witness instances"
                " only after adjoining the same immutable source-family tag"
            ),
            "cross_tag_cancellation_forbidden": True,
        }
        row["row_sha256"] = digest(row)
        incidence_rows.append(row)
    require(
        len(rows) == len({row["trace_id"] for row in rows}) == 432,
        "output trace census",
    )
    require(
        len(incidence_rows)
        == len({row["incidence_id"] for row in incidence_rows})
        == 215
        and (cancelled, retained) == (192, 23),
        "output incidence census",
    )
    return rows, incidence_rows


def build_source_injection_contracts(
    r43: dict[str, Any],
) -> list[dict[str, Any]]:
    rank_law = r43["one_step_area_eulerian_generator"][
        "cross_colour_pointwise_bounds"
    ]
    require(
        rank_law["incidence_rank"] == "1/c_target<=2^B"
        and rank_law["l1_generator"]
        == "abs_X_r+abs_X_p<=25*2^B",
        "source injection contract Round43 laws",
    )
    rows: list[dict[str, Any]] = []
    for stage in range(3):
        rank = RAW_INCIDENCE_RANK[stage]
        generator_budget = 25 * (1 << rank)
        trace_budget = 27
        total = generator_budget + trace_budget
        require(total == SOURCE_INJECTION[stage], "source contract total")
        row = {
            "source_injection_contract_row_id":
                source_injection_contract_id(stage),
            "stage": stage,
            "round43_manifest_sha256": UPSTREAM_PINS[
                "deliverables/cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
            ],
            "round43_incidence_rank_law": rank_law["incidence_rank"],
            "round43_generator_l1_law": rank_law["l1_generator"],
            "incidence_rank_B": rank,
            "incidence_rank_is_paid_by_each_leg_positive_cosine_lower":
                True,
            "bulk_generator_budget_per_M_rho_infinity":
                str(generator_budget),
            "bulk_budget_formula": f"25*2^{rank}",
            "two_artificial_trace_budget_per_M_rho_infinity":
                str(trace_budget),
            "source_graph_current_injection_strict_upper": str(total),
            "source_graph_current_injection_formula":
                f"25*2^{rank}+27={total}",
            "hash_dependency_direction": (
                "contract -> graph leg -> stage derivation -> F17 slot"
            ),
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(len(rows) == 3, "source injection contract census")
    return rows


def common_child_intervals(
    r121: dict[str, Any],
) -> list[tuple[dict[str, Any], Q, Q]]:
    endpoints = {
        row["endpoint_id"]: tuple(map(Q, row["x_dyadic_bracket"]))
        for row in r121["pullback_endpoint_rows"]
    }
    result: list[tuple[dict[str, Any], Q, Q]] = []
    for child in r121["common_refinement_rows"]:
        lower_id = child["source_x_lower_endpoint_id"]
        upper_id = child["source_x_upper_endpoint_id"]
        lower = (
            Q(0)
            if "source-left-endpoint" in lower_id
            else endpoints[lower_id][0]
        )
        upper = (
            Q(1)
            if "source-right-endpoint" in upper_id
            else endpoints[upper_id][1]
        )
        require(0 <= lower < upper <= 1, "common child interval")
        result.append((child, lower, upper))
    result.sort(key=lambda item: item[0]["common_rank"])
    require(
        [item[0]["common_rank"] for item in result] == list(range(24)),
        "common child order",
    )
    return result


def stored_contains_fresh(
    stored: Any, fresh: arb, label: str
) -> tuple[Q, Q]:
    lower, upper = parse_interval(stored, label)
    fresh_lower, fresh_upper = v122.arb_pair(fresh)
    require(
        lower <= fresh_lower <= fresh_upper <= upper,
        f"{label} complete fresh containment",
    )
    return lower, upper


def fresh_generator_geometry(
    r121: dict[str, Any],
) -> dict[tuple[str, int], dict[str, arb]]:
    ctx.prec = VERIFIER_BITS
    values = v122.load_inputs()
    indexes = v122.seed_indexes(values)
    theta_star = v122.isolate_anchor(indexes)
    result: dict[tuple[str, int], dict[str, arb]] = {}
    for child, lower, upper in common_child_intervals(r121):
        x = v122.Jet2(v122.interval(lower, upper), x=arb(1))
        s = v122.Jet2(
            v122.interval(-v122.PARAMETER_RADIUS, v122.PARAMETER_RADIUS),
            s=arb(1),
        )
        state = v122.source_and_collisions(theta_star, x, s)
        for stage in range(3):
            nx, ny, momentum, cosine = state["collisions"][stage + 1]
            eta = v122.aq(Q(RELATIVE_CENTER_ETA[stage]))
            radius = v122.aq(TARGET_RADII[stage])
            x_r = eta * (
                ny - (momentum / cosine) * nx
            )
            x_p = (eta / radius) * (
                cosine * ny - momentum * nx
            )
            result[(child["common_child_id"], stage)] = {
                "nx": nx.value,
                "ny": ny.value,
                "p": momentum.value,
                "c": cosine.value,
                "x_r": x_r.value,
                "x_p": x_p.value,
            }
    require(len(result) == 72, "fresh generator geometry census")
    return result


def chart_free_formula() -> dict[str, Any]:
    return {
        "coordinates": "(r=R*theta,p=sin(phi))",
        "area_form": "dr dp",
        "c": "sqrt(1-p^2)",
        "incoming_ray": "u=-c*n+p*J*n",
        "relative_center_derivative": "d_s=eta*e_x",
        "flight_root_derivative": "tau_s=-eta*n_x/c",
        "normal_derivative":
            "R*n_s=-eta*e_x-(eta*n_x/c)*u",
        "X_r": "eta*(n_y-(p/c)*n_x)",
        "X_p": "(eta/R)*(c*n_y-p*n_x)",
        "partial_r_X_r": "(eta/R)*(n_x+(p/c)*n_y)",
        "partial_p_X_p": "-(eta/R)*(n_x+(p/c)*n_y)",
        "divergence_dr_dp": "0 exactly",
    }


def build_generator_rows(
    candidate_rows: Any,
    r121: dict[str, Any],
    r122: dict[str, Any],
    r124: dict[str, Any],
    input_traces: list[dict[str, Any]],
    source_contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    require(type(candidate_rows) is list, "generator rows type")
    for row in candidate_rows:
        validate_row(row, "generator row")
    require(
        len(candidate_rows)
        == len({row["graph_current_leg_row_id"]
                for row in candidate_rows})
        == 72,
        "generator row census",
    )
    candidate_map = {
        (row["common_child_id"], row["stage"]): row
        for row in candidate_rows
    }
    require(len(candidate_map) == 72, "generator coordinate uniqueness")
    fresh = fresh_generator_geometry(r121)
    trace_map: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for row in input_traces:
        trace_map.setdefault(
            (row["common_child_id"], row["stage"]), []
        ).append(row)
    slots122 = {
        (coordinate(row), row["field_index"]): row
        for row in r122["gate5_F7_F13_F16_slot_rows"]
    }
    slots124 = {
        coordinate(row): row for row in r124["gate5_F15_slot_rows"]
    }
    boundary_rows = {
        (row["common_child_id"], row["stage"]): row
        for row in r122["physical_face_typed_empty_audit"][
            "child_stage_boundary_rows"
        ]
    }
    require(len(boundary_rows) == 72, "Round122 boundary row census")
    source_contracts = {row["stage"]: row for row in source_contract_rows}
    require(len(source_contracts) == 3, "source contract stage census")
    expected_rows: list[dict[str, Any]] = []
    maximum = {0: Q(0), 1: Q(0), 2: Q(0)}
    for family in sorted(
        r124["standard_family_leg_operator_rows"],
        key=lambda row: (row["common_rank"], row["stage"]),
    ):
        child = family["common_child_id"]
        stage = family["stage"]
        stored = candidate_map[(child, stage)]
        geometry = fresh[(child, stage)]
        boundary = boundary_rows[(child, stage)]
        source_component = {
            key: (owner, chart)
            for key, owner, chart in RECIPIENT_COMPONENTS
        }[SOURCE_COMPONENT_BY_STAGE[stage]]
        require(
            boundary["source_owner"] == source_component[0]
            and boundary["source_chart"] == source_component[1]
            and boundary["actual_next_owner"]
            == family["actual_collision_owner"],
            "generator boundary geometry",
        )
        stored_intervals: dict[str, list[str]] = {}
        for field, fresh_key in (
            ("target_normal_x_enclosure", "nx"),
            ("target_normal_y_enclosure", "ny"),
            ("target_momentum_p_enclosure", "p"),
            ("target_cosine_c_enclosure", "c"),
            ("X_r_enclosure", "x_r"),
            ("X_p_enclosure", "x_p"),
        ):
            stored_contains_fresh(
                stored[field],
                geometry[fresh_key],
                f"generator {child}:{stage}:{field}",
            )
            stored_intervals[field] = stored[field]
        x_r_pair = parse_interval(
            stored["X_r_enclosure"], "stored X_r"
        )
        x_p_pair = parse_interval(
            stored["X_p_enclosure"], "stored X_p"
        )
        x_r_upper = max(abs(x_r_pair[0]), abs(x_r_pair[1]))
        x_p_upper = max(abs(x_p_pair[0]), abs(x_p_pair[1]))
        l1_upper = x_r_upper + x_p_upper
        c_pair = parse_interval(
            stored["target_cosine_c_enclosure"], "stored target cosine"
        )
        c_lower = c_pair[0]
        require(c_lower > 0, "positive target cosine lower")
        reciprocal_c_upper = Q(1) / c_lower
        require(
            parse_q(stored["actual_abs_X_r_upper"], nonnegative=True)
            == x_r_upper
            and parse_q(
                stored["actual_abs_X_p_upper"], nonnegative=True
            )
            == x_p_upper
            and parse_q(
                stored["actual_l1_generator_upper"], nonnegative=True
            )
            == l1_upper,
            "guarded absolute upper derivation",
        )
        diagnostic = (Q(8), Q(2), Q(0))[stage]
        if stage < 2:
            require(l1_upper < diagnostic, "generator strict diagnostic")
        else:
            require(
                x_r_pair == (Q(0), Q(0))
                and x_p_pair == (Q(0), Q(0))
                and v122.arb_pair(geometry["x_r"]) == (Q(0), Q(0))
                and v122.arb_pair(geometry["x_p"]) == (Q(0), Q(0)),
                "same-colour exact zero",
            )
        maximum[stage] = max(maximum[stage], l1_upper)

        roof_coordinates = [
            (
                family["official_word_key_id"],
                family["refined_homogeneous_subbranch_id"],
                roof,
            )
            for roof in family["roof_level_js"]
        ]
        f11_rows = [slots122[(key, 11)] for key in roof_coordinates]
        f13_rows = [slots122[(key, 13)] for key in roof_coordinates]
        f15_rows = [slots124[key] for key in roof_coordinates]
        require(
            all(
                Q(row["field_value_or_contract"])
                == F17_BY_STAGE[stage]
                for row in f11_rows
            ),
            "generator F11 crosswalk",
        )
        require(
            all(
                row["field_value_or_contract"] == "0"
                and row["field_bound_semantics"]
                == "EXACT_EMPTY_PHYSICAL_CURRENT_AND_TWO_TRACES"
                for row in f13_rows
            ),
            "generator F13 crosswalk",
        )
        rank = incidence_rank_from_f11(F17_BY_STAGE[stage])
        require(
            reciprocal_c_upper <= (1 << rank),
            "generator actual incidence rank",
        )
        source_contract = source_contracts[stage]
        require(
            source_contract["incidence_rank_B"] == rank
            and source_contract[
                "source_graph_current_injection_strict_upper"
            ]
            == str(SOURCE_INJECTION[stage]),
            "generator source contract",
        )
        traces = sorted(
            trace_map[(child, stage)], key=lambda row: row["side"]
        )
        require(len(traces) == 2, "two generator input traces")
        row = {
            "graph_current_leg_row_id":
                graph_current_leg_id(child, stage),
            "common_child_id": child,
            "common_rank": family["common_rank"],
            "stage": stage,
            "official_word_key_id": family["official_word_key_id"],
            "refined_homogeneous_subbranch_id":
                family["refined_homogeneous_subbranch_id"],
            "roof_level_js": family["roof_level_js"],
            "source_collision_owner": boundary["source_owner"],
            "source_collision_chart": boundary["source_chart"],
            "source_recipient_component_key":
                SOURCE_COMPONENT_BY_STAGE[stage],
            "target_collision_owner": family["actual_collision_owner"],
            "target_collision_chart": family["actual_collision_chart"],
            "target_recipient_component_key":
                TARGET_COMPONENT_BY_STAGE[stage],
            "target_radius": qstr(TARGET_RADII[stage]),
            "horizontal_W_motion_source_velocity": (0, 1, 0)[stage],
            "horizontal_W_motion_target_velocity": (1, 0, 0)[stage],
            "relative_center_velocity_eta":
                RELATIVE_CENTER_ETA[stage],
            "eulerian_generator_definition": (
                "X_i=(partial_s F_(i,s)) composed with F_(i,0)^(-1)"
            ),
            "chart_free_generator_formula": chart_free_formula(),
            "cross_precision_enclosure_guard": qstr(ENCLOSURE_GUARD),
            "cross_precision_guard_contract": (
                "each stored nonzero Arb interval is widened on both sides by"
                " delta/10^6; the independent verifier must require complete"
                " containment of its fresh enclosure"
            ),
            **stored_intervals,
            "guarded_target_cosine_strict_lower": qstr(c_lower),
            "guarded_reciprocal_cosine_upper":
                qstr(reciprocal_c_upper),
            "actual_leg_incidence_rank_inequality":
                f"1/c_lower<={1 << rank}=2^{rank}",
            "actual_leg_incidence_rank_inequality_verified": True,
            "actual_abs_X_r_upper": qstr(x_r_upper),
            "actual_abs_X_p_upper": qstr(x_p_upper),
            "actual_abs_uppers_are_derived_from_stored_guarded_intervals":
                True,
            "actual_l1_generator_upper": qstr(l1_upper),
            "actual_l1_generator_diagnostic_bound_semantics":
                "STRICT_UPPER" if stage < 2 else "EXACT",
            "actual_l1_generator_diagnostic_value": qstr(diagnostic),
            "actual_same_colour_generator_is_zero": stage == 2,
            "admitted_density": (
                "arbitrary positive normalized Round123 curve density rho_i"
                " with Reg_(1/3)(rho_i)<=500000000000000000000000000"
            ),
            "admitted_curve_measure": (
                "mu_i=M_i*rho_i*d ell_* on the materialized stage carrier"
            ),
            "bulk_vector_measure": "K_i=X_i*mu_i",
            "input_artificial_trace_ids": [
                item["trace_id"] for item in traces
            ],
            "artificial_two_side_trace_coefficient_strict_upper": "27",
            "artificial_trace_payment": (
                "two oriented sides, each source graph speed <13;"
                " hence total <26<27 per M_i*||rho_i||_infinity"
            ),
            "raw_incidence_rank_B": rank,
            "raw_incidence_rank_derivation": (
                f"Round43 1/c_target<=2^{rank};"
                f" F11/(150)=2^{rank} is an independent"
                " same-stage consistency crosswalk"
            ),
            "round43_rank_law": "1/c_target<=2^B",
            "round43_generator_l1_law":
                "abs_X_r+abs_X_p<=25*2^B",
            "round43_manifest_sha256": UPSTREAM_PINS[
                "deliverables/cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
            ],
            "raw_generator_coefficient_strict_upper":
                f"25*2^{rank}",
            "raw_source_graph_current_injection_per_M_rho_infinity_strict_upper":
                str(SOURCE_INJECTION[stage]),
            "source_injection_contract_row_id":
                source_contract["source_injection_contract_row_id"],
            "source_injection_contract_row_sha256":
                source_contract["row_sha256"],
            "source_injection_arithmetic":
                f"25*2^{rank}+27={SOURCE_INJECTION[stage]}",
            "source_injection_closure": (
                "TV(K_i)<=25*2^B*M_i"
                "<=25*2^B*M_i*||rho_i||_infinity and"
                " TV(B_i)<27*M_i*||rho_i||_infinity"
            ),
            "input_density_is_normalized_in_adapted_length": True,
            "input_carrier_adapted_length_less_or_equal_delta":
                family["input_adapted_length_less_or_equal_delta"],
            "normalization_length_implies_sup_density_lower": (
                "1=integral rho_i d ell_*"
                "<=L_i*||rho_i||_infinity and L_i<=delta<1,"
                " hence ||rho_i||_infinity>=1/L_i>1"
            ),
            "round122_same_key_F11_slot_ids": [
                item["slot_id"] for item in f11_rows
            ],
            "round122_same_key_F13_slot_ids": [
                item["slot_id"] for item in f13_rows
            ],
            "round124_same_key_F15_slot_ids": [
                item["slot_id"] for item in f15_rows
            ],
            "physical_trace_count": 0,
            "physical_trace_zero_only_by_Round122_empty_crosswalk": True,
            "round122_physical_empty_audit_sha256":
                r122["physical_face_typed_empty_audit_sha256"],
            "round122_child_stage_boundary_row_sha256":
                boundary["row_sha256"],
            "round122_child_stage_boundary_source_owner":
                boundary["source_owner"],
            "round122_child_stage_boundary_source_chart":
                boundary["source_chart"],
            "round122_child_stage_boundary_actual_next_owner":
                boundary["actual_next_owner"],
            "artificial_traces_are_not_physical_F13_traces": True,
            "dynamic_test_suffix_strict_upper":
                str(F17_BY_STAGE[stage]),
            "raw_source_to_target_response_per_M_rho_infinity_strict_upper":
                str(END_TO_END[stage]),
            "source_to_target_arithmetic": (
                f"{SOURCE_INJECTION[stage]}*{F17_BY_STAGE[stage]}"
                f"={END_TO_END[stage]}"
            ),
            "input_materialized_recut_instance_id":
                family["input_materialized_recut_instance_id"],
            "output_geometry_member_ids":
                family["output_geometry_member_ids"],
            "output_member_count": family["output_member_count"],
            "transparent_wall_roof_split_adds_no_current_or_suffix_factor":
                True,
            "bypass_designated_b3_is_a_collision_angle": False,
        }
        row["row_sha256"] = digest(row)
        expected_rows.append(row)
    require(
        maximum[0] < 8 and maximum[1] < 2 and maximum[2] == 0,
        "all generator strict margins",
    )
    require(
        canonical(candidate_rows) == canonical(expected_rows),
        "complete reconstructed generator rows",
    )
    return expected_rows


def build_recipient_components() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (component_key, owner, chart) in enumerate(
        RECIPIENT_COMPONENTS
    ):
        row = {
            "recipient_component_id": recipient_component_id(component_key),
            "component_index": index,
            "component_key": component_key,
            "collision_owner": owner,
            "collision_chart": chart,
            "test_pre_space": (
                "Round122 full-phase physical C1 plus"
                " dynamic-Holder-alpha tests restricted to this compact"
                " exact-seed component"
            ),
            "alpha_scope": "0<alpha<=1",
            "component_test_norm": (
                "the unchanged Round122 authoritative full-phase"
                " C1/dynamic-Holder-alpha norm on this component"
            ),
            "dual_recipient": (
                "the vector-current/artificial-trace dual of this component"
                " test pre-space"
            ),
            "physical_C1_observable_inclusion": "CONTINUOUS_BY_DEFINITION",
            "physical_C1_observable_inclusion_constant": "1",
            "both_collision_area_components_are_tested": True,
            "artificial_trace_tests_share_the_same_component_recipient": True,
            "finite_exact_seed_only": True,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows)
        == len({row["recipient_component_id"] for row in rows})
        == 4,
        "recipient component census",
    )
    return rows


def build_recipient_pullback_maps(
    r122: dict[str, Any],
    r124: dict[str, Any],
    generator_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    components = {row["component_key"]: row for row in component_rows}
    f11_slots = {
        coordinate(row): row
        for row in r122["gate5_F7_F13_F16_slot_rows"]
        if row["field_index"] == 11
    }
    dynamic_rows = {row["stage"]: row for row in r122["dynamic_F11_rows"]}
    family_rows = {
        (row["common_child_id"], row["stage"]): row
        for row in r124["standard_family_leg_operator_rows"]
    }
    boundary_rows = {
        (row["common_child_id"], row["stage"]): row
        for row in r122["physical_face_typed_empty_audit"][
            "child_stage_boundary_rows"
        ]
    }
    require(len(boundary_rows) == 72, "recipient boundary row census")
    rows: list[dict[str, Any]] = []
    for generator in sorted(
        generator_rows,
        key=lambda row: (row["common_rank"], row["stage"]),
    ):
        child = generator["common_child_id"]
        stage = generator["stage"]
        family = family_rows[(child, stage)]
        boundary = boundary_rows[(child, stage)]
        source = components[SOURCE_COMPONENT_BY_STAGE[stage]]
        target = components[TARGET_COMPONENT_BY_STAGE[stage]]
        require(
            target["collision_owner"] == family["actual_collision_owner"]
            and target["collision_chart"]
            == family["actual_collision_chart"],
            "recipient target geometry",
        )
        require(
            source["collision_owner"] == generator["source_collision_owner"]
            and source["collision_chart"]
            == generator["source_collision_chart"]
            and boundary["source_owner"] == source["collision_owner"]
            and boundary["source_chart"] == source["collision_chart"]
            and boundary["actual_next_owner"] == target["collision_owner"]
            and generator["source_recipient_component_key"]
            == source["component_key"]
            and generator["target_recipient_component_key"]
            == target["component_key"],
            "recipient source geometry",
        )
        coordinates = [
            (
                generator["official_word_key_id"],
                generator["refined_homogeneous_subbranch_id"],
                roof,
            )
            for roof in generator["roof_level_js"]
        ]
        f11_rows = [f11_slots[key] for key in coordinates]
        value = F17_BY_STAGE[stage]
        require(
            all(
                Q(item["field_value_or_contract"]) == value
                and item["field_bound_semantics"] == "STRICT_UPPER"
                and item["F11_uses_full_phase_authoritative_envelope"] is True
                for item in f11_rows
            ),
            "pullback F11 crosswalk",
        )
        dynamic = dynamic_rows[stage]
        require(
            Q(
                dynamic[
                    "full_phase_dynamic_Holder_test_pullback_strict_upper"
                ]
            )
            == value,
            "pullback dynamic row",
        )
        row = {
            "recipient_pullback_map_row_id":
                recipient_pullback_map_id(child, stage),
            "common_child_id": child,
            "common_rank": generator["common_rank"],
            "stage": stage,
            "official_word_key_id": generator["official_word_key_id"],
            "refined_homogeneous_subbranch_id":
                generator["refined_homogeneous_subbranch_id"],
            "roof_level_js": generator["roof_level_js"],
            "source_recipient_component_id":
                source["recipient_component_id"],
            "source_recipient_component_key": source["component_key"],
            "source_recipient_component_row_sha256": source["row_sha256"],
            "target_recipient_component_id":
                target["recipient_component_id"],
            "target_recipient_component_key": target["component_key"],
            "target_recipient_component_row_sha256": target["row_sha256"],
            "physical_branch_map":
                f"{source['component_key']}->{target['component_key']}",
            "input_materialized_recut_instance_id":
                family["input_materialized_recut_instance_id"],
            "target_collision_owner": family["actual_collision_owner"],
            "target_collision_chart": family["actual_collision_chart"],
            "round122_child_stage_boundary_row_sha256":
                boundary["row_sha256"],
            "round122_child_stage_boundary_source_owner":
                boundary["source_owner"],
            "round122_child_stage_boundary_source_chart":
                boundary["source_chart"],
            "round122_child_stage_boundary_actual_next_owner":
                boundary["actual_next_owner"],
            "standard_family_leg_operator_row_id":
                family["standard_family_leg_operator_row_id"],
            "standard_family_leg_operator_row_sha256": family["row_sha256"],
            "graph_current_leg_row_id":
                generator["graph_current_leg_row_id"],
            "graph_current_leg_row_sha256": generator["row_sha256"],
            "round122_same_key_F11_slot_ids": [
                item["slot_id"] for item in f11_rows
            ],
            "round122_same_key_F11_slot_canonical_sha256s": [
                digest(item) for item in f11_rows
            ],
            "round122_dynamic_F11_stage_row_sha256": digest(dynamic),
            "pullback_action_on_tests": "phi -> phi composed S_i",
            "full_phase_C1_dynamic_Holder_pullback_strict_upper":
                str(value),
            "source_physical_C1_observable_inclusion":
                "CONTINUOUS_BY_COMPONENT_DEFINITION",
            "target_physical_C1_observable_inclusion":
                "CONTINUOUS_BY_COMPONENT_DEFINITION",
            "piola_vector_measure_push": "K -> S_i#(DS_i*K)",
            "boundary_trace_push": "B -> S_i#B",
            "graph_current_intertwining": (
                "S_i#T_(K,B)=T_(S_i#(DS_i*K),S_i#B)"
            ),
            "area_coordinate_determinant": "1",
            "round43_area_generator_contract": (
                "X_s=(partial_s F_s) composed F_s^-1 and"
                " div_(dr dp) X_s=0 on a regular branch"
            ),
            "round43_manifest_sha256": UPSTREAM_PINS[
                "deliverables/cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
            ],
            "both_Eulerian_vector_components_are_received": True,
            "physical_and_artificial_traces_are_separately_typed": True,
            "transparent_roof_levels_share_one_physical_map": True,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows)
        == len({row["recipient_pullback_map_row_id"] for row in rows})
        == 72,
        "recipient pullback census",
    )
    require(
        Counter(row["stage"] for row in rows) == {0: 24, 1: 24, 2: 24},
        "recipient pullback stages",
    )
    return rows


def build_source_injection_rows(
    r43: dict[str, Any],
    generator_rows: list[dict[str, Any]],
    source_contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rank_law = r43["one_step_area_eulerian_generator"][
        "cross_colour_pointwise_bounds"
    ]
    require(
        rank_law["incidence_rank"] == "1/c_target<=2^B"
        and rank_law["l1_generator"]
        == "abs_X_r+abs_X_p<=25*2^B",
        "source injection Round43 laws",
    )
    contracts = {row["stage"]: row for row in source_contract_rows}
    require(len(contracts) == 3, "source derivation contracts")
    rows: list[dict[str, Any]] = []
    for stage in range(3):
        legs = [row for row in generator_rows if row["stage"] == stage]
        require(len(legs) == 24, "source injection leg census")
        f11_value = F17_BY_STAGE[stage]
        rank = incidence_rank_from_f11(f11_value)
        generator_budget = 25 * (1 << rank)
        trace_budget = 27
        total = generator_budget + trace_budget
        require(total == SOURCE_INJECTION[stage], "source injection total")
        actual_upper = max(
            parse_q(row["actual_l1_generator_upper"], nonnegative=True)
            for row in legs
        )
        minimum_cosine = min(
            parse_q(
                row["guarded_target_cosine_strict_lower"],
                nonnegative=False,
            )
            for row in legs
        )
        maximum_reciprocal = max(
            parse_q(
                row["guarded_reciprocal_cosine_upper"],
                nonnegative=False,
            )
            for row in legs
        )
        require(
            minimum_cosine > 0
            and maximum_reciprocal <= (1 << rank),
            "source derivation incidence ranks",
        )
        if stage < 2:
            require(
                actual_upper < generator_budget,
                "actual generator rank budget",
            )
        else:
            require(actual_upper == 0, "same-colour source injection")
        row = {
            "source_injection_derivation_row_id":
                source_injection_derivation_id(stage),
            "stage": stage,
            "leg_count": 24,
            "source_injection_contract_row_id":
                contracts[stage]["source_injection_contract_row_id"],
            "source_injection_contract_row_sha256":
                contracts[stage]["row_sha256"],
            "graph_current_leg_row_ids": [
                item["graph_current_leg_row_id"] for item in legs
            ],
            "graph_current_leg_row_sha256s": [
                item["row_sha256"] for item in legs
            ],
            "graph_current_leg_rows_canonical_sha256": digest(legs),
            "round43_manifest_sha256": UPSTREAM_PINS[
                "deliverables/cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
            ],
            "round43_incidence_rank_law": rank_law["incidence_rank"],
            "round43_generator_l1_law": rank_law["l1_generator"],
            "F11_full_phase_strict_upper": str(f11_value),
            "F11_rank_identity_consistency_crosswalk":
                f"{f11_value}=150*2^{rank}",
            "derived_incidence_rank_B": rank,
            "incidence_rank_provenance": (
                "Round43 1/c_target<=2^B, verified separately on every"
                " guarded positive cosine lower; the F11 identity is only"
                " a same-stage consistency crosswalk"
            ),
            "minimum_guarded_target_cosine_strict_lower":
                qstr(minimum_cosine),
            "maximum_guarded_reciprocal_cosine_upper":
                qstr(maximum_reciprocal),
            "all_24_positive_cosine_rank_inequalities_verified": True,
            "maximum_guarded_actual_l1_generator_upper":
                qstr(actual_upper),
            "bulk_generator_budget_per_M_rho_infinity":
                str(generator_budget),
            "bulk_budget_formula": f"25*2^{rank}",
            "input_density_normalization": (
                "integral rho_i d ell_*=1 on a carrier of adapted length"
                " <=delta"
            ),
            "normalization_length_sup_chain": (
                "1<=L_i*||rho_i||_infinity with L_i<=delta<1;"
                " therefore M_i<=M_i*||rho_i||_infinity"
            ),
            "bulk_TV_chain": (
                f"TV(K_i)<=25*2^{rank}*M_i"
                f"<=25*2^{rank}*M_i*||rho_i||_infinity"
            ),
            "two_artificial_trace_budget_per_M_rho_infinity":
                str(trace_budget),
            "trace_budget_formula": (
                "2*(source face x-speed <13)*(adapted Jacobian <1)"
                " <26<27"
            ),
            "source_graph_current_injection_strict_upper": str(total),
            "source_graph_current_injection_formula":
                f"25*2^{rank}+27={total}",
            "all_24_leg_rows_bind_this_derivation": all(
                item["raw_incidence_rank_B"] == rank
                and item[
                    "raw_source_graph_current_injection_per_M_rho_infinity_strict_upper"
                ]
                == str(total)
                and item["input_density_is_normalized_in_adapted_length"]
                is True
                and item[
                    "input_carrier_adapted_length_less_or_equal_delta"
                ]
                is True
                and item[
                    "actual_leg_incidence_rank_inequality_verified"
                ]
                is True
                and item["source_injection_contract_row_id"]
                == contracts[stage]["source_injection_contract_row_id"]
                and item["source_injection_contract_row_sha256"]
                == contracts[stage]["row_sha256"]
                for item in legs
            ),
        }
        require(
            row["all_24_leg_rows_bind_this_derivation"],
            "source injection binding",
        )
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(len(rows) == 3, "source injection census")
    return rows


def common_recipient_theorem() -> dict[str, Any]:
    require(
        SOURCE_INJECTION == {0: 819227, 1: 409627, 2: 409627},
        "source injection arithmetic",
    )
    require(
        END_TO_END
        == {
            0: 4026664550400,
            1: 1006699315200,
            2: 1006699315200,
        },
        "end-to-end arithmetic",
    )
    require(
        THREE_LEG_PRODUCT == 29686813949952000000,
        "three-leg arithmetic",
    )
    require(
        all(Q(value) > GLOBAL_THRESHOLD for value in F17_BY_STAGE.values()),
        "global threshold fail-closed",
    )
    return {
        "status":
            "CERTIFIED_FINITE_EXACT_SEED_PHYSICAL_GRAPH_CURRENT_RECIPIENT",
        "physical_test_carrier": (
            "disjoint union of the four actual collision chart components"
            " G:W, W:N, G:S and G:N restricted to the exact-seed branches"
        ),
        "test_pre_space": (
            "the Round122 authoritative full-phase physical C1 plus"
            " dynamic-Holder-alpha test space on every one of the finitely"
            " many materialized chart branches"
        ),
        "alpha_scope": "0<alpha<=1",
        "common_test_norm": (
            "componentwise Round122 full-phase C1/dynamic-Holder-alpha norm,"
            " followed by the max direct-sum norm over the finite exact-seed"
            " chart/component registry"
        ),
        "common_recipient": (
            "D_seed is that finite componentwise test space;"
            " Y_seed=D_seed^* is its vector-current/trace dual"
        ),
        "recipient_component_count": 4,
        "recipient_component_keys": [
            item[0] for item in RECIPIENT_COMPONENTS
        ],
        "physical_leg_component_routes": [
            "G:W->W:N",
            "W:N->G:S",
            "G:S->G:N",
        ],
        "recipient_pullback_map_row_count": 72,
        "all_source_and_target_routes_are_pinned_to_Round122_child_stage_boundary_rows":
            True,
        "physical_C1_tests_are_contained": True,
        "containment_reason": (
            "only 72 materialized compact regular leg restrictions occur and"
            " the final Round122 F11 constants bound every actual pullback"
        ),
        "graph_current": {
            "pair": "(K,B)",
            "functional": (
                "T_(K,B)(phi)=integral grad(phi) dot dK+B(phi)"
            ),
            "distributional_name": "-div(K)+B",
            "source_injection":
                "||T_(K,B)||_(Y_seed)<=TV(K)+TV(B)",
            "bulk_type": (
                "K is a two-component vector Radon measure supported on the"
                " materialized standard curve, not an ambient area density"
            ),
            "boundary_type": (
                "B is the signed atomic/trace measure on separately typed"
                " artificial carrier boundaries"
            ),
            "both_vector_components_are_tested": True,
            "stable_tangential_scalar_tests_only": False,
            "incidence_rank_payment": (
                "every leg has a positive guarded cosine lower and directly"
                " verifies 1/c_lower<=2^B before 25*2^B is used"
            ),
            "source_injection_hash_DAG": (
                "3 stage contracts -> 72 graph-current legs -> 3 complete"
                " stage derivations -> 120 F17 slots"
            ),
        },
        "source_trace_coordinate_payment": {
            "source_parameter": (
                "the common Round121 x parameter, with each typed artificial"
                " face represented by the Round122 analytic graph x_face(s)"
            ),
            "stage_adapted_coordinate_x_derivative_bounds": {
                "stage0": {
                    "semantics": "EXACT",
                    "value": qstr(ADAPTED_X_DERIVATIVE[0]),
                },
                "stage1": {
                    "semantics": "STRICT_UPPER",
                    "value": qstr(ADAPTED_X_DERIVATIVE[1]),
                },
                "stage2": {
                    "semantics": "STRICT_UPPER",
                    "value": qstr(ADAPTED_X_DERIVATIVE[2]),
                },
            },
            "all_stage_adapted_derivative_bounds_below_one": True,
            "round122_face_x_s_strict_upper": "13",
            "one_side_adapted_trace_coefficient_strict_upper": "13",
            "two_side_trace_coefficient_strict_upper": "27",
            "exact_input_trace_density": (
                "orientation*v_face^(x)*|partial_x ell_*|*M_i*rho_i"
            ),
            "adapted_density_Jacobian_is_mandatory": True,
            "trace_atom_is_pushed_to_the_physical_endpoint": True,
            "trace_templates_are_parameterized_by_source_family_member_tag":
                True,
            "cross_tag_cancellation_forbidden": True,
        },
        "piola_intertwining": {
            "actual_branch": (
                "the materialized regular billiard branch S;"
                " det(DS)=1 in collision-area coordinates"
            ),
            "vector_push":
                "Piola_S K=S_#(DS*K) as a vector Radon measure",
            "boundary_push": "B maps to S_*B",
            "identity": "S_*T_(K,B)=T_(Piola_S K,S_*B)",
            "pairing_replay": (
                "T_(Piola_S K,S_*B)(phi)=T_(K,B)(phi composed S)"
            ),
            "dual_bound": (
                "Round122 gives ||phi composed S_i||_Dsource"
                " < C_i ||phi||_Dtarget, hence"
                " ||S_i* T||_Ytarget < C_i ||T||_Ysource"
            ),
            "normal_flux_identity":
                "DS^T*cof(DS)=det(DS)*I=I",
        },
        "stage_suffix_strict_uppers": {
            "stage0": str(F17_BY_STAGE[0]),
            "stage1": str(F17_BY_STAGE[1]),
            "stage2": str(F17_BY_STAGE[2]),
        },
        "stage_source_injection_strict_uppers": {
            "stage0": str(SOURCE_INJECTION[0]),
            "stage1": str(SOURCE_INJECTION[1]),
            "stage2": str(SOURCE_INJECTION[2]),
        },
        "stage_end_to_end_response_strict_uppers": {
            "stage0": str(END_TO_END[0]),
            "stage1": str(END_TO_END[1]),
            "stage2": str(END_TO_END[2]),
        },
        "generic_three_physical_leg_compositional_bound":
            str(THREE_LEG_PRODUCT),
        "three_leg_product_arithmetic": (
            "4915200*2457600*2457600"
            "=29686813949952000000"
        ),
        "three_leg_product_is_not_a_one_step_slot": True,
        "transparent_roof_level_count": 5,
        "physical_collision_factor_count": 3,
        "roof_split_does_not_change_three_factors_to_five": True,
        "global_threshold_audit": {
            "required_for_old_global_quarter_route":
                "C_dyn<7961063/7800000",
            "threshold": qstr(GLOBAL_THRESHOLD),
            "all_local_F17_values_exceed_threshold": True,
            "C_dyn_equals_one_claimed": False,
            "global_F17_or_strong_F13_inferred": False,
        },
    }


def trace_cancellation_theorem() -> dict[str, Any]:
    return {
        "rule": (
            "cancel an internal artificial trace before total"
            " variation iff the two orientations oppose and the"
            " unnormalized trace densities agree"
        ),
        "normalized_conditional_density_equality_is_not_required": True,
        "mass_times_conditional_density_recovers_unnormalized_density": True,
        "endpoint_velocity_must_also_match": True,
        "cancellation_is_fibrewise_in_one_source_family_member_tag": True,
        "cross_family_member_tag_cancellation_allowed": False,
        "source_family_tag_is_pinned_to_Round124_stage2_input_member_contract":
            True,
        "cancellation_precedes_distinct_output_fragment_member_tags": True,
        "Round123_new_stage3_cut_count": 192,
        "new_stage3_cuts_are_within_one_input_child": True,
        "new_stage3_cut_rows_are_bound_by_canonical_sha256": True,
        "new_stage3_root_velocity_law": (
            "v_endpoint=-(partial_s U3)/(partial_x U3)"
            " at U3=j*delta"
        ),
        "new_stage3_cut_velocity_is_shared_by_both_sides": True,
        "shared_endpoint_velocity_witness_id_is_reconstructed": True,
        "shared_unnormalized_density_witness_id_is_reconstructed": True,
        "output_Jacobian_factor_is_present_before_cancellation": True,
        "new_stage3_cuts_cancelled_before_TV": 192,
        "old_Round121_inter_child_cut_count": 23,
        "old_inter_child_densities_assumed_equal": False,
        "old_inter_child_incidences_cancelled_unconditionally": 0,
        "old_inter_child_trace_sides_retained": 46,
        "outer_trace_sides_retained": 2,
        "retained_typed_stage3_trace_count": 48,
        "physical_trace_empty_statement_erases_artificial_traces": False,
    }


def build_f17_slots(
    r122: dict[str, Any],
    r124: dict[str, Any],
    generator_rows: list[dict[str, Any]],
    recipient_maps: list[dict[str, Any]],
    source_derivation_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generators = {
        (row["common_child_id"], row["stage"]): row
        for row in generator_rows
    }
    map_lookup = {
        (row["common_child_id"], row["stage"]): row
        for row in recipient_maps
    }
    derivations = {row["stage"]: row for row in source_derivation_rows}
    require(len(derivations) == 3, "F17 source derivation census")
    f11 = {
        coordinate(row): row
        for row in r122["gate5_F7_F13_F16_slot_rows"]
        if row["field_index"] == 11
    }
    rows: list[dict[str, Any]] = []
    keys: set[str] = set()
    for f15 in sorted(
        r124["gate5_F15_slot_rows"],
        key=lambda row: (
            row["common_child_id"],
            row["stage"],
            row["roof_level_j"],
        ),
    ):
        key3 = coordinate(f15)
        generator = generators[(f15["common_child_id"], f15["stage"])]
        recipient_map = map_lookup[
            (f15["common_child_id"], f15["stage"])
        ]
        derivation = derivations[f15["stage"]]
        require(
            any(
                row_id == generator["graph_current_leg_row_id"]
                and row_sha == generator["row_sha256"]
                for row_id, row_sha in zip(
                    derivation["graph_current_leg_row_ids"],
                    derivation["graph_current_leg_row_sha256s"],
                    strict=True,
                )
            ),
            "F17 derivation graph binding",
        )
        immutable_key = [
            f15["official_word_key_id"],
            f15["refined_homogeneous_subbranch_id"],
            f15["roof_level_j"],
            "dynamic_test_operator_cost",
        ]
        key_text = canonical(immutable_key)
        require(key_text not in keys, "unique F17 immutable key")
        keys.add(key_text)
        f11_row = f11[key3]
        value = F17_BY_STAGE[f15["stage"]]
        require(
            Q(f11_row["field_value_or_contract"]) == value,
            "F11/F17 numeric crosswalk",
        )
        row = {
            "slot_id": f17_slot_id(immutable_key),
            "immutable_slot_key": immutable_key,
            "official_word_key_id": f15["official_word_key_id"],
            "refined_homogeneous_subbranch_id":
                f15["refined_homogeneous_subbranch_id"],
            "roof_level_j": f15["roof_level_j"],
            "field_index": 17,
            "field_name": "dynamic_test_operator_cost",
            "field_bound_semantics": "STRICT_UPPER",
            "field_value_or_contract": str(value),
            "slot_status": "CERTIFIED_ON_THIS_EXACT_SEED_COMMON_CHILD",
            "common_child_id": f15["common_child_id"],
            "stage": f15["stage"],
            "graph_current_leg_row_id":
                generator["graph_current_leg_row_id"],
            "graph_current_leg_row_sha256": generator["row_sha256"],
            "source_injection_contract_row_id":
                generator["source_injection_contract_row_id"],
            "source_injection_contract_row_sha256":
                generator["source_injection_contract_row_sha256"],
            "source_injection_derivation_row_id":
                derivation["source_injection_derivation_row_id"],
            "source_injection_derivation_row_sha256":
                derivation["row_sha256"],
            "recipient_pullback_map_row_id":
                recipient_map["recipient_pullback_map_row_id"],
            "recipient_pullback_map_row_sha256":
                recipient_map["row_sha256"],
            "source_recipient_component_id":
                recipient_map["source_recipient_component_id"],
            "target_recipient_component_id":
                recipient_map["target_recipient_component_id"],
            "round122_same_key_F11_slot_id": f11_row["slot_id"],
            "round124_same_key_F15_slot_id": f15["slot_id"],
            "F17_is_not_a_rename_of_F11": True,
            "F11_role": (
                "numeric physical pullback bound used only after the"
                " Round125 vector-current recipient/Piola layer"
            ),
            "both_Eulerian_vector_components_included": True,
            "physical_trace_zero_crosswalk_included": True,
            "artificial_trace_registry_retained": True,
            "transparent_wall_roof_split_adds_no_F17_factor": True,
            "roof_slot_value_is_one_step_not_three_leg_product": True,
            "C_dyn_equals_one_claimed": False,
            "global_quarter_threshold_passed": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows)
        == len({row["slot_id"] for row in rows})
        == len(keys)
        == 120,
        "F17 slot census",
    )
    require(
        Counter(row["stage"] for row in rows) == {0: 48, 1: 24, 2: 48},
        "F17 stage census",
    )
    return rows


def expected_result(
    r121: dict[str, Any],
    r122: dict[str, Any],
    r123: dict[str, Any],
    r124: dict[str, Any],
    r43: dict[str, Any],
    candidate_generator_rows: Any,
) -> dict[str, Any]:
    source_contracts = build_source_injection_contracts(r43)
    input_traces, input_incidences = build_input_traces(
        r121, r122, r124
    )
    output_traces, output_incidences = build_output_traces(
        r123, r122, r124
    )
    generator_rows = build_generator_rows(
        candidate_generator_rows,
        r121,
        r122,
        r124,
        input_traces,
        source_contracts,
    )
    component_rows = build_recipient_components()
    recipient_maps = build_recipient_pullback_maps(
        r122, r124, generator_rows, component_rows
    )
    source_rows = build_source_injection_rows(
        r43, generator_rows, source_contracts
    )
    f17_rows = build_f17_slots(
        r122,
        r124,
        generator_rows,
        recipient_maps,
        source_rows,
    )

    inherited = r124["combined_installed_child_local_slot_registry"]
    require(
        inherited["combined_slot_count"] == 1920,
        "Round124 combined registry",
    )
    new_ids = [row["slot_id"] for row in f17_rows]
    require(len(new_ids) == len(set(new_ids)) == 120, "new F17 IDs")

    result = copy.deepcopy(r124)
    for key in (
        "status",
        "strict_scope",
        "strict_nonclaims",
        "upstream_and_helper_pins",
    ):
        result.pop(key)
    gate_status = dict(r124["gate5_actual_child_field_status"])
    gate_status["F17"] = (
        "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN"
    )
    count = dict(r124["count_ledger"])
    count.update(
        {
            "graph_current_leg_row_count": 72,
            "recipient_component_row_count": 4,
            "recipient_pullback_map_row_count": 72,
            "source_injection_contract_row_count": 3,
            "source_injection_derivation_row_count": 3,
            "input_artificial_trace_row_count": 144,
            "input_internal_incidence_row_count": 69,
            "stage3_output_trace_row_count": 432,
            "stage3_output_internal_incidence_row_count": 215,
            "stage3_output_cancelled_same_input_incidence_count": 192,
            "stage3_output_retained_inter_child_incidence_count": 23,
            "stage3_output_outer_trace_count": 2,
            "stage3_output_retained_typed_trace_count_after_certified_cancellation":
                48,
            "new_F17_slot_count": 120,
            "inherited_Round124_slot_count": 1920,
            "combined_child_local_slot_count": 2040,
            "certified_child_local_field_count": 17,
            "complete_18_field_block_count": 0,
        }
    )
    result.update(
        {
            "status": (
                "CERTIFIED_EXACT_SEED_PHYSICAL_GRAPH_CURRENT_DYNAMIC_TEST"
                "__F17_INSTALLED"
            ),
            "precision_bits": PRODUCER_BITS,
            "round124_contract": {
                "producer_sha256": UPSTREAM_PINS[
                    "deliverables/cm2_round124_rank3_exact_seed_standard_family_operator_f15.py"
                ],
                "certificate_sha256": UPSTREAM_PINS[
                    "deliverables/cm2-round124-rank3-exact-seed-standard-family-operator-f15-2026-07-23.json"
                ],
                "verifier_sha256": UPSTREAM_PINS[
                    "deliverables/cm2_round124_rank3_exact_seed_standard_family_operator_f15_verifier.py"
                ],
                "verification_sha256": UPSTREAM_PINS[
                    "deliverables/cm2-round124-rank3-exact-seed-standard-family-operator-f15-verification-2026-07-23.json"
                ],
                "result_sha256":
                    "fe8a0c7e2b25452246748b46e3a73b256b0942606e55568979e38b7815ad2124",
                "actual_child_count": 24,
                "family_leg_row_count": 72,
                "inherited_slot_count": 1920,
                "inherited_child_local_maturity": "16/18",
            },
            "cross_precision_enclosure_contract": {
                "producer_precision_bits": PRODUCER_BITS,
                "independent_verifier_precision_bits": VERIFIER_BITS,
                "rational_guard_each_side": qstr(ENCLOSURE_GUARD),
                "guard_identity": "delta/10^6",
                "guarded_fields": [
                    "target_normal_x_enclosure",
                    "target_normal_y_enclosure",
                    "target_momentum_p_enclosure",
                    "target_cosine_c_enclosure",
                    "X_r_enclosure",
                    "X_p_enclosure",
                ],
                "fresh_independent_enclosure_must_be_completely_contained":
                    True,
                "actual_abs_uppers_are_recomputed_from_guarded_intervals":
                    True,
                "same_colour_X_r_X_p_are_exact_zero_without_guard": True,
            },
            "physical_graph_current_recipient_and_Piola_theorem":
                common_recipient_theorem(),
            "recipient_component_rows": component_rows,
            "recipient_component_rows_sha256": digest(component_rows),
            "recipient_pullback_map_rows": recipient_maps,
            "recipient_pullback_map_rows_sha256": digest(recipient_maps),
            "source_injection_derivation_rows": source_rows,
            "source_injection_derivation_rows_sha256": digest(source_rows),
            "source_injection_contract_rows": source_contracts,
            "source_injection_contract_rows_sha256":
                digest(source_contracts),
            "graph_current_leg_rows": generator_rows,
            "graph_current_leg_rows_sha256": digest(generator_rows),
            "input_artificial_trace_rows": input_traces,
            "input_artificial_trace_rows_sha256": digest(input_traces),
            "input_internal_trace_incidence_rows": input_incidences,
            "input_internal_trace_incidence_rows_sha256":
                digest(input_incidences),
            "stage3_output_artificial_trace_rows": output_traces,
            "stage3_output_artificial_trace_rows_sha256":
                digest(output_traces),
            "stage3_output_trace_incidence_rows": output_incidences,
            "stage3_output_trace_incidence_rows_sha256":
                digest(output_incidences),
            "trace_cancellation_theorem": trace_cancellation_theorem(),
            "gate5_F17_slot_rows": f17_rows,
            "gate5_F17_slot_rows_sha256": digest(f17_rows),
            "combined_installed_child_local_slot_registry_after_F17": {
                "Round124_inherited_slot_count": 1920,
                "Round123_combined_slot_ids_sha256":
                    inherited["Round123_combined_slot_ids_sha256"],
                "Round124_new_F15_slot_ids_sha256":
                    inherited["new_F15_slot_ids_sha256"],
                "new_F17_slot_count": 120,
                "new_F17_slot_ids_sha256": digest(new_ids),
                "combined_slot_count": 2040,
                "slot_count_per_certified_field": 120,
                "certified_field_indices": list(range(1, 18)),
                "uninstalled_field_indices": [18],
                "combined_registry_chain_sha256": digest(
                    [
                        inherited["Round123_combined_slot_ids_sha256"],
                        inherited["new_F15_slot_ids_sha256"],
                        new_ids,
                    ]
                ),
                "all_keys_are_full_word_subbranch_roof_field_keys": True,
                "stage3_trace_and_fragment_payloads_are_not_source_slot_keys":
                    True,
            },
            "count_ledger": count,
            "gate5_actual_child_field_status": gate_status,
            "rank3_seed_child_field_maturity": "17/18",
            "remaining_uninstalled_child_fields": ["F18"],
            "gate5_global_maturity": "10/18",
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "cm2_verdict": "NO-GO_FOR_CLAIM",
            "strict_scope": (
                "one Round121 exact-b seed, its 24 materialized common"
                " children, 72 actual physical collision-leg graph currents,"
                " four typed recipient components, 72 source-target"
                " pullback maps, and their finite exact-seed physical"
                " C1/dynamic-Holder recipient"
            ),
            "strict_nonclaims": [
                "no renaming of scalar F11 slots as vector-current F17 slots",
                "no C_dyn=1 physical F17 claim",
                "no satisfaction of the old global C_dyn<7961063/7800000 threshold",
                "no automatic cancellation of unequal inter-child traces",
                "no erasure of artificial traces by the physical-empty audit",
                "no strong global F13 or arbitrary-return-depth F17 theorem",
                "no extension of the four-component exact-seed recipient to the global Borel key universe",
                "no global power-Orlicz, owner drift, or strong cemetery theorem",
                "no F18 operator phase block",
                "no complete 18-field block",
                "no global Gate5 maturity upgrade",
                "no endpoint-inclusive physical collar or cross-trace union reach",
                "no CM2 claim",
            ],
            "upstream_and_helper_pins":
                dict(sorted(UPSTREAM_PINS.items())),
        }
    )
    return result


def evaluate_document(
    document: dict[str, Any],
    r121: dict[str, Any],
    r122: dict[str, Any],
    r123: dict[str, Any],
    r124: dict[str, Any],
    r43: dict[str, Any],
    expected_cached: dict[str, Any] | None = None,
) -> dict[str, Any]:
    require(type(document) is dict, "certificate document type")
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict, "certificate result type")
    require(
        document["result_sha256"] == digest(result),
        "certificate result digest",
    )
    expected = (
        expected_cached
        if expected_cached is not None
        else expected_result(
            r121,
            r122,
            r123,
            r124,
            r43,
            result.get("graph_current_leg_rows"),
        )
    )
    require(set(result) == set(expected), "closed result schema")

    replaced = {
        "status",
        "precision_bits",
        "round124_contract",
        "cross_precision_enclosure_contract",
        "physical_graph_current_recipient_and_Piola_theorem",
        "recipient_component_rows",
        "recipient_component_rows_sha256",
        "recipient_pullback_map_rows",
        "recipient_pullback_map_rows_sha256",
        "source_injection_derivation_rows",
        "source_injection_derivation_rows_sha256",
        "source_injection_contract_rows",
        "source_injection_contract_rows_sha256",
        "graph_current_leg_rows",
        "graph_current_leg_rows_sha256",
        "input_artificial_trace_rows",
        "input_artificial_trace_rows_sha256",
        "input_internal_trace_incidence_rows",
        "input_internal_trace_incidence_rows_sha256",
        "stage3_output_artificial_trace_rows",
        "stage3_output_artificial_trace_rows_sha256",
        "stage3_output_trace_incidence_rows",
        "stage3_output_trace_incidence_rows_sha256",
        "trace_cancellation_theorem",
        "gate5_F17_slot_rows",
        "gate5_F17_slot_rows_sha256",
        "combined_installed_child_local_slot_registry_after_F17",
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
    inherited_excluded = {
        "status",
        "strict_scope",
        "strict_nonclaims",
        "upstream_and_helper_pins",
    }
    for key in set(r124) - inherited_excluded - replaced:
        require(
            canonical(result[key]) == canonical(r124[key]),
            f"inherited Round124 field:{key}",
        )
    require(
        canonical(result["upstream_and_helper_pins"])
        == canonical(dict(sorted(UPSTREAM_PINS.items()))),
        "upstream pin table",
    )
    require(
        canonical(result["round124_contract"])
        == canonical(expected["round124_contract"]),
        "Round124 contract",
    )
    require(
        canonical(result["cross_precision_enclosure_contract"])
        == canonical(expected["cross_precision_enclosure_contract"]),
        "cross precision contract",
    )

    arrays = (
        (
            "recipient_component_rows",
            "recipient_component_rows_sha256",
            "recipient_component_id",
            4,
        ),
        (
            "recipient_pullback_map_rows",
            "recipient_pullback_map_rows_sha256",
            "recipient_pullback_map_row_id",
            72,
        ),
        (
            "source_injection_contract_rows",
            "source_injection_contract_rows_sha256",
            "source_injection_contract_row_id",
            3,
        ),
        (
            "source_injection_derivation_rows",
            "source_injection_derivation_rows_sha256",
            "source_injection_derivation_row_id",
            3,
        ),
        (
            "graph_current_leg_rows",
            "graph_current_leg_rows_sha256",
            "graph_current_leg_row_id",
            72,
        ),
        (
            "input_artificial_trace_rows",
            "input_artificial_trace_rows_sha256",
            "trace_id",
            144,
        ),
        (
            "input_internal_trace_incidence_rows",
            "input_internal_trace_incidence_rows_sha256",
            "incidence_id",
            69,
        ),
        (
            "stage3_output_artificial_trace_rows",
            "stage3_output_artificial_trace_rows_sha256",
            "trace_id",
            432,
        ),
        (
            "stage3_output_trace_incidence_rows",
            "stage3_output_trace_incidence_rows_sha256",
            "incidence_id",
            215,
        ),
        (
            "gate5_F17_slot_rows",
            "gate5_F17_slot_rows_sha256",
            "slot_id",
            120,
        ),
    )
    for rows_key, digest_key, id_key, count in arrays:
        rows = result[rows_key]
        require(type(rows) is list, f"{rows_key} type")
        for row in rows:
            validate_row(row, rows_key)
        require(result[digest_key] == digest(rows), f"{rows_key} digest")
        require(
            len(rows) == len({row[id_key] for row in rows}) == count,
            f"{rows_key} census",
        )

    components = result["recipient_component_rows"]
    require(
        [row["component_index"] for row in components] == list(range(4)),
        "recipient component order",
    )
    maps = result["recipient_pullback_map_rows"]
    generators = result["graph_current_leg_rows"]
    source_rows = result["source_injection_derivation_rows"]
    source_contracts = result["source_injection_contract_rows"]
    input_rows = result["input_artificial_trace_rows"]
    input_incidences = result["input_internal_trace_incidence_rows"]
    output_rows = result["stage3_output_artificial_trace_rows"]
    output_incidences = result["stage3_output_trace_incidence_rows"]
    f17_rows = result["gate5_F17_slot_rows"]
    require(
        Counter(row["stage"] for row in maps) == {0: 24, 1: 24, 2: 24}
        and Counter(row["stage"] for row in generators)
        == {0: 24, 1: 24, 2: 24}
        and Counter(row["stage"] for row in source_rows)
        == {0: 1, 1: 1, 2: 1}
        and Counter(row["stage"] for row in source_contracts)
        == {0: 1, 1: 1, 2: 1}
        and Counter(row["stage"] for row in f17_rows)
        == {0: 48, 1: 24, 2: 48},
        "stage censuses",
    )
    require(
        Counter(row["stage"] for row in input_rows)
        == {0: 48, 1: 48, 2: 48},
        "input trace stage census",
    )
    for row in generators:
        stage = row["stage"]
        require(type(stage) is int and stage in (0, 1, 2),
                "generator stage type")
        require(
            row["actual_l1_generator_diagnostic_bound_semantics"]
            == ("STRICT_UPPER" if stage < 2 else "EXACT"),
            "generator diagnostic semantics",
        )
        diagnostic = parse_q(
            row["actual_l1_generator_diagnostic_value"],
            nonnegative=True,
        )
        require(
            diagnostic == (Q(8), Q(2), Q(0))[stage],
            "generator diagnostic value",
        )
        actual_l1 = parse_q(
            row["actual_l1_generator_upper"], nonnegative=True
        )
        require(
            (stage < 2 and actual_l1 < diagnostic)
            or (stage == 2 and actual_l1 == diagnostic == 0),
            "generator diagnostic inequality",
        )
    require(
        sum(row["cancelled_before_total_variation"] for row in output_incidences)
        == 192
        and sum(
            row["retained_as_two_typed_traces_when_not_matched"]
            for row in output_incidences
        )
        == 23,
        "output cancellation census",
    )
    require(
        all(
            row["adapted_jacobian_factor_is_not_omitted"] is True
            and row["source_family_member_tag_is_preserved"] is True
            for row in input_rows
        )
        and all(
            row["Jacobian_factor_is_present_in_unnormalized_density"] is True
            and row["source_family_member_tag_is_preserved"] is True
            for row in output_rows
        ),
        "trace Jacobian and tag contracts",
    )
    require(
        all(
            row["adapted_jacobian_factor_present_on_both_trace_rows"] is True
            and row["unconditional_cancellation_claimed"] is False
            for row in input_incidences
        ),
        "input incidence fail-closed state",
    )
    for row in f17_rows:
        require(
            type(row["roof_level_j"]) is int
            and type(row["field_index"]) is int
            and type(row["stage"]) is int,
            "F17 integer fields",
        )
        require(
            row["immutable_slot_key"]
            == [
                row["official_word_key_id"],
                row["refined_homogeneous_subbranch_id"],
                row["roof_level_j"],
                "dynamic_test_operator_cost",
            ],
            "F17 immutable key",
        )
        require(
            row["slot_id"] == f17_slot_id(row["immutable_slot_key"]),
            "F17 slot constructor",
        )
    require(
        canonical(result["physical_graph_current_recipient_and_Piola_theorem"])
        == canonical(common_recipient_theorem()),
        "recipient/Piola theorem",
    )
    require(
        canonical(result["trace_cancellation_theorem"])
        == canonical(trace_cancellation_theorem()),
        "trace cancellation theorem",
    )

    for key in (
        "recipient_component_rows",
        "recipient_pullback_map_rows",
        "source_injection_derivation_rows",
        "source_injection_contract_rows",
        "graph_current_leg_rows",
        "input_artificial_trace_rows",
        "input_internal_trace_incidence_rows",
        "stage3_output_artificial_trace_rows",
        "stage3_output_trace_incidence_rows",
        "gate5_F17_slot_rows",
        "combined_installed_child_local_slot_registry_after_F17",
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
            f"independent reconstructed field:{key}",
        )
    require(canonical(result) == canonical(expected), "complete result")
    return {
        "graph_current_leg_row_count": len(generators),
        "recipient_component_row_count": len(components),
        "recipient_pullback_map_row_count": len(maps),
        "source_injection_derivation_row_count": len(source_rows),
        "source_injection_contract_row_count": len(source_contracts),
        "input_artificial_trace_row_count": len(input_rows),
        "input_internal_incidence_row_count": len(input_incidences),
        "stage3_output_trace_row_count": len(output_rows),
        "stage3_output_internal_incidence_row_count":
            len(output_incidences),
        "stage3_cancelled_same_input_incidence_count": 192,
        "stage3_retained_inter_child_incidence_count": 23,
        "F17_slot_count": len(f17_rows),
        "F17_stage_slot_counts": {
            str(stage): sum(row["stage"] == stage for row in f17_rows)
            for stage in range(3)
        },
        "combined_child_local_slot_count":
            result["count_ledger"]["combined_child_local_slot_count"],
        "rank3_seed_child_field_maturity":
            result["rank3_seed_child_field_maturity"],
        "gate5_global_maturity": result["gate5_global_maturity"],
        "complete_18_field_block_count":
            result["complete_18_field_block_count"],
        "cm2_verdict": result["cm2_verdict"],
    }


def resign(document: dict[str, Any]) -> None:
    """Re-sign all Round125 nested digests after a semantic mutation."""
    result = document.get("result")
    if type(result) is not dict:
        return

    row_arrays = (
        ("recipient_component_rows", "recipient_component_rows_sha256"),
        (
            "source_injection_contract_rows",
            "source_injection_contract_rows_sha256",
        ),
        ("graph_current_leg_rows", "graph_current_leg_rows_sha256"),
        (
            "input_artificial_trace_rows",
            "input_artificial_trace_rows_sha256",
        ),
        (
            "input_internal_trace_incidence_rows",
            "input_internal_trace_incidence_rows_sha256",
        ),
        (
            "stage3_output_artificial_trace_rows",
            "stage3_output_artificial_trace_rows_sha256",
        ),
        (
            "stage3_output_trace_incidence_rows",
            "stage3_output_trace_incidence_rows_sha256",
        ),
        (
            "source_injection_derivation_rows",
            "source_injection_derivation_rows_sha256",
        ),
    )
    for rows_key, dataset_key in row_arrays:
        rows = result.get(rows_key)
        if type(rows) is not list:
            continue
        for row in rows:
            if type(row) is dict and "row_sha256" in row:
                row["row_sha256"] = digest(
                    {k: v for k, v in row.items() if k != "row_sha256"}
                )
        result[dataset_key] = digest(rows)

    components = result.get("recipient_component_rows")
    generators = result.get("graph_current_leg_rows")
    contracts = result.get("source_injection_contract_rows")
    contract_map = (
        {
            row.get("stage"): row
            for row in contracts
            if type(row) is dict
        }
        if type(contracts) is list
        else {}
    )
    if type(generators) is list:
        for row in generators:
            if type(row) is not dict:
                continue
            contract = contract_map.get(row.get("stage"))
            if contract is not None:
                row["source_injection_contract_row_sha256"] = contract.get(
                    "row_sha256"
                )
            if "row_sha256" in row:
                row["row_sha256"] = digest(
                    {k: v for k, v in row.items() if k != "row_sha256"}
                )
        result["graph_current_leg_rows_sha256"] = digest(generators)
    component_map = (
        {
            row.get("recipient_component_id"): row
            for row in components
            if type(row) is dict
        }
        if type(components) is list
        else {}
    )
    generator_map = (
        {
            row.get("graph_current_leg_row_id"): row
            for row in generators
            if type(row) is dict
        }
        if type(generators) is list
        else {}
    )
    derivations = result.get("source_injection_derivation_rows")
    if type(derivations) is list:
        by_stage: dict[Any, list[dict[str, Any]]] = {}
        if type(generators) is list:
            for row in generators:
                if type(row) is dict:
                    by_stage.setdefault(row.get("stage"), []).append(row)
        for row in derivations:
            if type(row) is not dict:
                continue
            stage = row.get("stage")
            contract = contract_map.get(stage)
            legs = by_stage.get(stage, [])
            if contract is not None:
                row["source_injection_contract_row_sha256"] = contract.get(
                    "row_sha256"
                )
            row["graph_current_leg_row_ids"] = [
                item.get("graph_current_leg_row_id") for item in legs
            ]
            row["graph_current_leg_row_sha256s"] = [
                item.get("row_sha256") for item in legs
            ]
            row["graph_current_leg_rows_canonical_sha256"] = digest(legs)
            if "row_sha256" in row:
                row["row_sha256"] = digest(
                    {k: v for k, v in row.items() if k != "row_sha256"}
                )
        result["source_injection_derivation_rows_sha256"] = digest(
            derivations
        )
    derivation_map = (
        {
            row.get("stage"): row
            for row in derivations
            if type(row) is dict
        }
        if type(derivations) is list
        else {}
    )
    maps = result.get("recipient_pullback_map_rows")
    if type(maps) is list:
        for row in maps:
            if type(row) is not dict:
                continue
            source = component_map.get(
                row.get("source_recipient_component_id")
            )
            target = component_map.get(
                row.get("target_recipient_component_id")
            )
            generator = generator_map.get(
                row.get("graph_current_leg_row_id")
            )
            if source is not None:
                row["source_recipient_component_row_sha256"] = source.get(
                    "row_sha256"
                )
            if target is not None:
                row["target_recipient_component_row_sha256"] = target.get(
                    "row_sha256"
                )
            if generator is not None:
                row["graph_current_leg_row_sha256"] = generator.get(
                    "row_sha256"
                )
            if "row_sha256" in row:
                row["row_sha256"] = digest(
                    {k: v for k, v in row.items() if k != "row_sha256"}
                )
        result["recipient_pullback_map_rows_sha256"] = digest(maps)
    map_lookup = (
        {
            row.get("recipient_pullback_map_row_id"): row
            for row in maps
            if type(row) is dict
        }
        if type(maps) is list
        else {}
    )
    f17_rows = result.get("gate5_F17_slot_rows")
    if type(f17_rows) is list:
        for row in f17_rows:
            if type(row) is not dict:
                continue
            generator = generator_map.get(
                row.get("graph_current_leg_row_id")
            )
            pullback = map_lookup.get(
                row.get("recipient_pullback_map_row_id")
            )
            if generator is not None:
                row["graph_current_leg_row_sha256"] = generator.get(
                    "row_sha256"
                )
            if pullback is not None:
                row["recipient_pullback_map_row_sha256"] = pullback.get(
                    "row_sha256"
                )
            contract = contract_map.get(row.get("stage"))
            derivation = derivation_map.get(row.get("stage"))
            if contract is not None:
                row["source_injection_contract_row_sha256"] = contract.get(
                    "row_sha256"
                )
            if derivation is not None:
                row["source_injection_derivation_row_sha256"] = derivation.get(
                    "row_sha256"
                )
            if "row_sha256" in row:
                row["row_sha256"] = digest(
                    {k: v for k, v in row.items() if k != "row_sha256"}
                )
        result["gate5_F17_slot_rows_sha256"] = digest(f17_rows)

    registry = result.get(
        "combined_installed_child_local_slot_registry_after_F17"
    )
    if type(registry) is dict and type(f17_rows) is list:
        new_ids = [
            row.get("slot_id") for row in f17_rows if type(row) is dict
        ]
        registry["new_F17_slot_ids_sha256"] = digest(new_ids)
        if (
            "Round123_combined_slot_ids_sha256" in registry
            and "Round124_new_F15_slot_ids_sha256" in registry
        ):
            registry["combined_registry_chain_sha256"] = digest(
                [
                    registry["Round123_combined_slot_ids_sha256"],
                    registry["Round124_new_F15_slot_ids_sha256"],
                    new_ids,
                ]
            )
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
    r121: dict[str, Any],
    r122: dict[str, Any],
    r123: dict[str, Any],
    r124: dict[str, Any],
    r43: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    cases: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def setter(label: str, path: tuple[Any, ...], value: Any) -> None:
        cases.append(
            (label, lambda doc, p=path, v=value: set_path(doc, p, v))
        )

    def deleter(label: str, path: tuple[Any, ...]) -> None:
        cases.append((label, lambda doc, p=path: delete_path(doc, p)))

    def swapper(label: str, path: tuple[Any, ...], a: int, b: int) -> None:
        def mutate(doc: dict[str, Any]) -> None:
            target: Any = doc
            for part in path:
                target = target[part]
            target[a], target[b] = target[b], target[a]
        cases.append((label, mutate))

    def duplicator(label: str, path: tuple[Any, ...], index: int) -> None:
        def mutate(doc: dict[str, Any]) -> None:
            target: Any = doc
            for part in path:
                target = target[part]
            target.append(copy.deepcopy(target[index]))
        cases.append((label, mutate))

    def remover(label: str, path: tuple[Any, ...], index: int) -> None:
        def mutate(doc: dict[str, Any]) -> None:
            target: Any = doc
            for part in path:
                target = target[part]
            target.pop(index)
        cases.append((label, mutate))

    r = ("result",)
    setter("schema swap", ("schema",), "cm2.round125.mutant.v2")
    deleter("missing status", r + ("status",))
    setter("unknown result key", r + ("mutant_unknown",), True)
    setter("status frontier", r + ("status",), "FRONTIER_ONLY")
    setter("producer precision mutation", r + ("precision_bits",), 3072)
    setter(
        "local maturity virtual complete",
        r + ("rank3_seed_child_field_maturity",),
        "18/18",
    )
    setter(
        "global maturity virtual eleven",
        r + ("gate5_global_maturity",),
        "11/18",
    )
    setter(
        "complete block virtual one",
        r + ("complete_18_field_block_count",),
        1,
    )
    setter("gate block virtual one", r + ("gate5_block_count",), 1)
    setter("CM2 virtual GO", r + ("cm2_verdict",), "GO_FOR_CLAIM")
    setter(
        "F17 uninstalled",
        r + ("gate5_actual_child_field_status", "F17"),
        "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
    )
    setter(
        "F18 virtual install",
        r + ("gate5_actual_child_field_status", "F18"),
        "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN",
    )
    setter(
        "remaining fields empty",
        r + ("remaining_uninstalled_child_fields",),
        [],
    )
    for key, value in (
        ("graph_current_leg_row_count", 71),
        ("recipient_component_row_count", 5),
        ("recipient_pullback_map_row_count", 71),
        ("source_injection_derivation_row_count", 4),
        ("input_artificial_trace_row_count", 143),
        ("input_internal_incidence_row_count", 68),
        ("stage3_output_trace_row_count", 431),
        ("stage3_output_internal_incidence_row_count", 214),
        ("new_F17_slot_count", 121),
        ("combined_child_local_slot_count", 2041),
        ("certified_child_local_field_count", 18),
    ):
        setter(
            f"count ledger {key}",
            r + ("count_ledger", key),
            value,
        )
    setter(
        "upstream Round43 pin",
        r
        + (
            "upstream_and_helper_pins",
            "deliverables/cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json",
        ),
        "0" * 64,
    )
    setter(
        "Round124 contract producer pin",
        r + ("round124_contract", "producer_sha256"),
        "0" * 64,
    )
    setter(
        "Round124 contract result pin",
        r + ("round124_contract", "result_sha256"),
        "0" * 64,
    )
    setter(
        "cross precision verifier bits",
        r
        + (
            "cross_precision_enclosure_contract",
            "independent_verifier_precision_bits",
        ),
        1536,
    )
    setter(
        "cross precision guard identity",
        r + ("cross_precision_enclosure_contract", "guard_identity"),
        "delta/10^5",
    )
    setter(
        "cross precision containment false",
        r
        + (
            "cross_precision_enclosure_contract",
            "fresh_independent_enclosure_must_be_completely_contained",
        ),
        False,
    )

    theorem = r + ("physical_graph_current_recipient_and_Piola_theorem",)
    theorem_mutations = (
        (("status",), "FRONTIER_ONLY"),
        (("recipient_component_count",), 3),
        (("physical_C1_tests_are_contained",), False),
        (("graph_current", "both_vector_components_are_tested"), False),
        (("graph_current", "stable_tangential_scalar_tests_only"), True),
        (
            (
                "source_trace_coordinate_payment",
                "adapted_density_Jacobian_is_mandatory",
            ),
            False,
        ),
        (
            (
                "source_trace_coordinate_payment",
                "cross_tag_cancellation_forbidden",
            ),
            False,
        ),
        (
            (
                "source_trace_coordinate_payment",
                "stage_adapted_coordinate_x_derivative_bounds",
                "stage0",
                "semantics",
            ),
            "STRICT_UPPER",
        ),
        (
            (
                "source_trace_coordinate_payment",
                "stage_adapted_coordinate_x_derivative_bounds",
                "stage0",
                "value",
            ),
            qstr(2 * DELTA),
        ),
        (("piola_intertwining", "area_coordinate_determinant"), "2"),
        (
            ("piola_intertwining", "normal_flux_identity"),
            "DS^T*cof(DS)=0",
        ),
        (("stage_suffix_strict_uppers", "stage0"), "4915199"),
        (
            ("stage_source_injection_strict_uppers", "stage1"),
            "409626",
        ),
        (
            ("stage_end_to_end_response_strict_uppers", "stage2"),
            "1006699315199",
        ),
        (
            ("generic_three_physical_leg_compositional_bound",),
            "29686813949951999999",
        ),
        (("three_leg_product_is_not_a_one_step_slot",), False),
        (("physical_collision_factor_count",), 5),
        (
            ("global_threshold_audit", "all_local_F17_values_exceed_threshold"),
            False,
        ),
        (
            ("global_threshold_audit", "C_dyn_equals_one_claimed"),
            True,
        ),
        (
            ("global_threshold_audit", "global_F17_or_strong_F13_inferred"),
            True,
        ),
    )
    for index, (path, value) in enumerate(theorem_mutations):
        setter(f"recipient theorem mutation {index}", theorem + path, value)

    cancellation = r + ("trace_cancellation_theorem",)
    cancellation_mutations = (
        (("normalized_conditional_density_equality_is_not_required",), False),
        (("endpoint_velocity_must_also_match",), False),
        (("cross_family_member_tag_cancellation_allowed",), True),
        (("Round123_new_stage3_cut_count",), 191),
        (("new_stage3_cuts_are_within_one_input_child",), False),
        (("new_stage3_cut_velocity_is_shared_by_both_sides",), False),
        (("output_Jacobian_factor_is_present_before_cancellation",), False),
        (("new_stage3_cuts_cancelled_before_TV",), 191),
        (("old_inter_child_incidences_cancelled_unconditionally",), 23),
        (("retained_typed_stage3_trace_count",), 46),
        (("physical_trace_empty_statement_erases_artificial_traces",), True),
    )
    for index, (path, value) in enumerate(cancellation_mutations):
        setter(
            f"cancellation theorem mutation {index}",
            cancellation + path,
            value,
        )

    components = r + ("recipient_component_rows",)
    for index in range(4):
        setter(
            f"component {index} key",
            components + (index, "component_key"),
            f"mutant:{index}",
        )
        setter(
            f"component {index} both vector components",
            components
            + (index, "both_collision_area_components_are_tested"),
            False,
        )
    swapper("component row reorder", components, 0, 1)
    duplicator("component row duplicate", components, 0)
    remover("component row missing", components, 0)

    maps = r + ("recipient_pullback_map_rows",)
    map_fields = (
        ("source_recipient_component_key", "mutant-source"),
        ("target_recipient_component_key", "mutant-target"),
        ("physical_branch_map", "G:W->G:N"),
        ("full_phase_C1_dynamic_Holder_pullback_strict_upper", "1"),
        ("piola_vector_measure_push", "scalar push"),
        ("boundary_trace_push", "DROP"),
        ("graph_current_intertwining", "BROKEN"),
        ("area_coordinate_determinant", "2"),
        ("both_Eulerian_vector_components_are_received", False),
        ("physical_and_artificial_traces_are_separately_typed", False),
        ("transparent_roof_levels_share_one_physical_map", False),
    )
    for index, (field, value) in enumerate(map_fields):
        setter(
            f"pullback map field {field}",
            maps + (index, field),
            value,
        )
    setter(
        "pullback map F11 slot link",
        maps + (11, "round122_same_key_F11_slot_ids", 0),
        "mutant-slot",
    )
    setter(
        "pullback map dynamic F11 hash",
        maps + (12, "round122_dynamic_F11_stage_row_sha256"),
        "0" * 64,
    )
    swapper("pullback map reorder", maps, 0, 1)
    duplicator("pullback map duplicate", maps, 0)
    remover("pullback map missing", maps, 0)

    sources = r + ("source_injection_derivation_rows",)
    contracts = r + ("source_injection_contract_rows",)
    for stage in range(3):
        setter(
            f"source contract {stage} rank",
            contracts + (stage, "incidence_rank_B"),
            RAW_INCIDENCE_RANK[stage] + 1,
        )
        setter(
            f"source contract {stage} positive cosine payment",
            contracts
            + (
                stage,
                "incidence_rank_is_paid_by_each_leg_positive_cosine_lower",
            ),
            False,
        )
        setter(
            f"source contract {stage} injection",
            contracts
            + (stage, "source_graph_current_injection_strict_upper"),
            str(SOURCE_INJECTION[stage] - 1),
        )
        setter(
            f"source contract {stage} hash direction",
            contracts + (stage, "hash_dependency_direction"),
            "circular",
        )
    swapper("source contract reorder", contracts, 0, 1)
    duplicator("source contract duplicate", contracts, 0)
    remover("source contract missing", contracts, 0)

    for stage in range(3):
        setter(
            f"source derivation {stage} rank",
            sources + (stage, "derived_incidence_rank_B"),
            RAW_INCIDENCE_RANK[stage] + 1,
        )
        setter(
            f"source derivation {stage} injection",
            sources
            + (stage, "source_graph_current_injection_strict_upper"),
            str(SOURCE_INJECTION[stage] - 1),
        )
        setter(
            f"source derivation {stage} normalization",
            sources + (stage, "normalization_length_sup_chain"),
            "missing",
        )
        setter(
            f"source derivation {stage} binding",
            sources + (stage, "all_24_leg_rows_bind_this_derivation"),
            False,
        )
        setter(
            f"source derivation {stage} positive cosine audit",
            sources
            + (
                stage,
                "all_24_positive_cosine_rank_inequalities_verified",
            ),
            False,
        )
        setter(
            f"source derivation {stage} minimum cosine",
            sources
            + (stage, "minimum_guarded_target_cosine_strict_lower"),
            "0",
        )
    swapper("source derivation reorder", sources, 0, 1)
    duplicator("source derivation duplicate", sources, 0)

    generators = r + ("graph_current_leg_rows",)
    generator_fields = (
        ("source_collision_owner", "G[9,9]"),
        ("source_recipient_component_key", "mutant"),
        ("target_collision_owner", "G[9,9]"),
        ("target_recipient_component_key", "mutant"),
        ("relative_center_velocity_eta", 2),
        ("cross_precision_enclosure_guard", qstr(2 * ENCLOSURE_GUARD)),
        ("target_radius", "1"),
        ("actual_abs_uppers_are_derived_from_stored_guarded_intervals", False),
        ("actual_l1_generator_diagnostic_bound_semantics", "UNSAFE"),
        ("actual_same_colour_generator_is_zero", True),
        ("input_density_is_normalized_in_adapted_length", False),
        ("normalization_length_implies_sup_density_lower", "missing"),
        ("raw_incidence_rank_B", 1),
        (
            "raw_source_graph_current_injection_per_M_rho_infinity_strict_upper",
            "1",
        ),
        ("physical_trace_count", 2),
        ("artificial_traces_are_not_physical_F13_traces", False),
        ("dynamic_test_suffix_strict_upper", "1"),
        ("transparent_wall_roof_split_adds_no_current_or_suffix_factor", False),
    )
    for index, (field, value) in enumerate(generator_fields):
        setter(
            f"generator field {field}",
            generators + (index, field),
            value,
        )
    setter(
        "generator guarded normal lower narrowed",
        generators + (20, "target_normal_x_enclosure", 0),
        "0",
    )
    setter(
        "generator guarded momentum upper narrowed",
        generators + (21, "target_momentum_p_enclosure", 1),
        "0",
    )
    setter(
        "generator guarded Xr upper narrowed",
        generators + (22, "X_r_enclosure", 1),
        "0",
    )
    setter(
        "generator stage2 diagnostic false strict",
        generators
        + (2, "actual_l1_generator_diagnostic_bound_semantics"),
        "STRICT_UPPER",
    )
    setter(
        "generator positive cosine lower",
        generators + (23, "guarded_target_cosine_strict_lower"),
        "0",
    )
    setter(
        "generator reciprocal cosine rank",
        generators + (24, "guarded_reciprocal_cosine_upper"),
        "999999999",
    )
    setter(
        "generator incidence inequality verified",
        generators
        + (25, "actual_leg_incidence_rank_inequality_verified"),
        False,
    )
    setter(
        "generator Round122 boundary source chart",
        generators
        + (26, "round122_child_stage_boundary_source_chart"),
        "mutant-chart",
    )
    setter(
        "generator source contract id",
        generators + (27, "source_injection_contract_row_id"),
        "mutant-contract",
    )
    swapper("generator row reorder", generators, 0, 1)
    duplicator("generator row duplicate", generators, 0)
    remover("generator row missing", generators, 0)

    input_rows = r + ("input_artificial_trace_rows",)
    input_fields = (
        ("orientation_sign", 1),
        ("source_face_speed_claimed_strict_upper", "12"),
        ("stage_adapted_coordinate_id", "wrong"),
        ("stage_adapted_coordinate_x_derivative_bound_value", "1"),
        (
            "stage_adapted_coordinate_x_derivative_bound_semantics",
            "EXACT",
        ),
        ("adapted_jacobian_factor_is_not_omitted", False),
        ("source_family_member_tag_is_preserved", False),
        ("cross_family_member_tag_cancellation_allowed", True),
        ("artificial_not_physical", False),
        ("physical_empty_crosswalk_does_not_erase_this_trace", False),
        ("trace_instance_id_constructor", "tag omitted"),
    )
    for index, (field, value) in enumerate(input_fields):
        setter(
            f"input trace field {field}",
            input_rows + (index, field),
            value,
        )
    swapper("input trace reorder", input_rows, 0, 1)
    duplicator("input trace duplicate", input_rows, 0)
    remover("input trace missing", input_rows, 0)

    input_inc = r + ("input_internal_trace_incidence_rows",)
    input_inc_fields = (
        ("orientations_are_opposite", False),
        ("adapted_jacobian_factor_present_on_both_trace_rows", False),
        (
            "cancellation_before_total_variation_iff_unnormalized_densities_match",
            False,
        ),
        (
            "arbitrary_densities_on_distinct_input_children_are_assumed_equal",
            True,
        ),
        ("unconditional_cancellation_claimed", True),
        ("both_traces_remain_typed", False),
        (
            "trace_instances_are_compared_only_with_equal_source_family_member_tag",
            False,
        ),
        ("cross_tag_cancellation_forbidden", False),
    )
    for index, (field, value) in enumerate(input_inc_fields):
        setter(
            f"input incidence field {field}",
            input_inc + (index, field),
            value,
        )
    swapper("input incidence reorder", input_inc, 0, 1)
    duplicator("input incidence duplicate", input_inc, 0)
    remover("input incidence missing", input_inc, 0)

    output_rows = r + ("stage3_output_artificial_trace_rows",)
    output_fields = (
        ("orientation_sign", 1),
        ("endpoint_velocity_witness_id", "mutant"),
        ("unnormalized_density_witness_id", "mutant"),
        ("endpoint_velocity_witness_instance_id_constructor", "tag omitted"),
        (
            "unnormalized_density_witness_instance_id_constructor",
            "tag omitted",
        ),
        (
            "witness_instance_requires_equal_source_family_member_tag",
            False,
        ),
        ("Jacobian_factor_is_present_in_unnormalized_density", False),
        ("conditional_normalization_is_undone_by_fragment_mass", False),
        ("source_family_member_tag_is_preserved", False),
        ("cross_family_member_tag_cancellation_allowed", True),
        ("artificial_not_physical", False),
        ("row_source_sha256", "0" * 64),
        ("round123_merged_cut_canonical_sha256", "0" * 64),
        ("endpoint_evidence_canonical_sha256", "0" * 64),
        (
            "round124_stage2_input_member_contract_canonical_sha256",
            "0" * 64,
        ),
        (
            "source_family_member_tag_is_bound_to_Round124_stage2_input_contract",
            False,
        ),
    )
    for index, (field, value) in enumerate(output_fields):
        setter(
            f"output trace field {field}",
            output_rows + (index, field),
            value,
        )
    swapper("output trace reorder", output_rows, 0, 1)
    duplicator("output trace duplicate", output_rows, 0)
    remover("output trace missing", output_rows, 0)

    output_inc = r + ("stage3_output_trace_incidence_rows",)
    output_inc_fields = (
        ("orientations_are_opposite", False),
        ("same_input_common_child", False),
        ("unnormalized_density_match_certified", False),
        ("endpoint_velocity_match_certified", False),
        ("endpoint_velocity_witness_ids_equal", False),
        ("unnormalized_density_witness_ids_equal", False),
        ("conditional_normalized_densities_need_not_match", False),
        ("cancelled_before_total_variation", False),
        ("retained_as_two_typed_traces_when_not_matched", True),
        (
            "cancellation_is_fibrewise_in_one_source_family_member_tag",
            False,
        ),
        ("equal_source_family_member_tag_is_required", False),
        ("witness_instance_comparison_rule", "tag ignored"),
        ("cross_tag_cancellation_forbidden", False),
        ("round123_merged_cut_canonical_sha256", "0" * 64),
        ("same_Round124_input_family_tag_domain", False),
        (
            "cancellation_occurs_before_distinct_output_member_tags_are_assigned",
            False,
        ),
    )
    for index, (field, value) in enumerate(output_inc_fields):
        setter(
            f"output incidence field {field}",
            output_inc + (index, field),
            value,
        )
    swapper("output incidence reorder", output_inc, 0, 1)
    duplicator("output incidence duplicate", output_inc, 0)
    remover("output incidence missing", output_inc, 0)

    f17 = r + ("gate5_F17_slot_rows",)
    f17_fields = (
        ("field_index", 11),
        ("field_name", "physical_pullback"),
        ("field_bound_semantics", "EXACT"),
        ("field_value_or_contract", "1"),
        ("slot_status", "FRONTIER_ONLY"),
        ("F17_is_not_a_rename_of_F11", False),
        ("both_Eulerian_vector_components_included", False),
        ("physical_trace_zero_crosswalk_included", False),
        ("artificial_trace_registry_retained", False),
        ("transparent_wall_roof_split_adds_no_F17_factor", False),
        ("roof_slot_value_is_one_step_not_three_leg_product", False),
        ("C_dyn_equals_one_claimed", True),
        ("global_quarter_threshold_passed", True),
        ("source_recipient_component_id", "mutant"),
        ("target_recipient_component_id", "mutant"),
        ("round122_same_key_F11_slot_id", "mutant"),
        ("round124_same_key_F15_slot_id", "mutant"),
    )
    for index, (field, value) in enumerate(f17_fields):
        setter(
            f"F17 slot field {field}",
            f17 + (index, field),
            value,
        )
    setter(
        "F17 immutable key field tag",
        f17 + (18, "immutable_slot_key", 3),
        "physical_pullback_bound",
    )
    setter("F17 slot ID", f17 + (19, "slot_id"), "mutant")
    setter(
        "F17 source contract link",
        f17 + (20, "source_injection_contract_row_id"),
        "mutant-contract",
    )
    setter(
        "F17 source derivation link",
        f17 + (21, "source_injection_derivation_row_id"),
        "mutant-derivation",
    )
    swapper("F17 slot reorder", f17, 0, 1)
    duplicator("F17 slot duplicate", f17, 0)
    remover("F17 slot missing", f17, 0)

    registry = r + (
        "combined_installed_child_local_slot_registry_after_F17",
    )
    registry_mutations = (
        (("Round124_inherited_slot_count",), 1919),
        (("new_F17_slot_count",), 119),
        (("combined_slot_count",), 2039),
        (("slot_count_per_certified_field",), 119),
        (("certified_field_indices",), list(range(1, 19))),
        (("uninstalled_field_indices",), []),
        (("all_keys_are_full_word_subbranch_roof_field_keys",), False),
        (
            ("stage3_trace_and_fragment_payloads_are_not_source_slot_keys",),
            False,
        ),
    )
    for index, (path, value) in enumerate(registry_mutations):
        setter(f"combined registry mutation {index}", registry + path, value)

    require(
        len(cases) >= 140
        and len({label for label, _mutate in cases}) == len(cases),
        "semantic mutation suite size and labels",
    )
    rejected: list[str] = []
    for label, mutate in cases:
        mutant = copy.deepcopy(certificate)
        mutate(mutant)
        resign(mutant)
        try:
            evaluate_document(
                mutant,
                r121,
                r122,
                r123,
                r124,
                r43,
                expected,
            )
        except Exception:
            rejected.append(label)
            continue
        raise VerificationError(f"semantic mutation accepted:{label}")
    require(
        len(rejected) == len(cases),
        "all semantic mutations rejected",
    )
    return rejected


def strict_json_attacks(
    certificate: dict[str, Any],
    r121: dict[str, Any],
    r122: dict[str, Any],
    r123: dict[str, Any],
    r124: dict[str, Any],
    r43: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    full = canonical(certificate).encode("utf-8")

    def resigned(path: tuple[Any, ...], value: Any) -> bytes:
        document = copy.deepcopy(certificate)
        set_path(document, path, value)
        resign(document)
        return canonical(document).encode("utf-8")

    attacks: list[tuple[str, bytes]] = [
        (
            "duplicate top-level key",
            b'{"schema":"x","schema":"y","result":{},'
            b'"result_sha256":"z"}',
        ),
        (
            "duplicate deep key",
            (
                b'{"schema":"'
                + CERTIFICATE_SCHEMA.encode("utf-8")
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
                ("result", "count_ledger", "graph_current_leg_row_count"),
                True,
            ),
        ),
        (
            "noncanonical fraction",
            resigned(
                (
                    "result",
                    "cross_precision_enclosure_contract",
                    "rational_guard_each_side",
                ),
                "2/2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            ),
        ),
        (
            "zero-denominator fraction",
            resigned(
                (
                    "result",
                    "cross_precision_enclosure_contract",
                    "rational_guard_each_side",
                ),
                "1/0",
            ),
        ),
    ]
    labels: list[str] = []
    for label, raw in attacks:
        try:
            value = parse_strict_bytes(raw)
            require(type(value) is dict, "strict attack top object")
            evaluate_document(
                value,
                r121,
                r122,
                r123,
                r124,
                r43,
                expected,
            )
        except Exception:
            labels.append(label)
            continue
        raise VerificationError(f"strict JSON attack accepted:{label}")
    require(
        len(labels) == len(set(labels)) == 15,
        "strict JSON attack census",
    )
    return labels


def verification_document(
    certificate_path: Path,
    certificate: dict[str, Any],
    r121: dict[str, Any],
    r122: dict[str, Any],
    r123: dict[str, Any],
    r124: dict[str, Any],
    r43: dict[str, Any],
) -> dict[str, Any]:
    expected = expected_result(
        r121,
        r122,
        r123,
        r124,
        r43,
        certificate["result"]["graph_current_leg_rows"],
    )
    counts = evaluate_document(
        certificate,
        r121,
        r122,
        r123,
        r124,
        r43,
        expected,
    )
    semantic_labels = semantic_mutations(
        certificate,
        r121,
        r122,
        r123,
        r124,
        r43,
        expected,
    )
    strict_labels = strict_json_attacks(
        certificate,
        r121,
        r122,
        r123,
        r124,
        r43,
        expected,
    )
    result = {
        "status": "PASS",
        "verifier_precision_bits": VERIFIER_BITS,
        "independence_contract": {
            "imports_Round125_producer": False,
            "imports_upstream_producer_modules": False,
            "Round125_producer_is_byte_pinned_but_not_executed": True,
            "Round121_through_Round124_are_strict_parsed_as_frozen_data":
                True,
            "imports_only_byte_pinned_independent_Round122_verifier_for_geometry":
                True,
            "fresh_3072_bit_anchor_and_child_geometry_recomputed": True,
            "all_six_guarded_fields_require_complete_enclosure_containment":
                True,
            "all_72_graph_current_leg_rows_reconstructed": True,
            "all_4_recipient_components_reconstructed": True,
            "all_72_recipient_pullback_maps_reconstructed": True,
            "all_3_source_injection_contracts_reconstructed": True,
            "all_3_source_injection_derivations_reconstructed": True,
            "all_144_input_trace_rows_reconstructed": True,
            "all_69_input_incidence_rows_reconstructed": True,
            "all_432_output_trace_rows_reconstructed": True,
            "all_215_output_incidence_rows_reconstructed": True,
            "all_120_full_key_F17_slots_reconstructed": True,
            "all_2040_combined_keys_accounted_for": True,
        },
        "producer_sha256": ROUND125_PRODUCER_SHA256,
        "verifier_sha256": sha256(Path(__file__).resolve()),
        "certificate_sha256": sha256(certificate_path),
        "certificate_result_sha256": certificate["result_sha256"],
        "upstream_byte_pin_count": len(UPSTREAM_PINS),
        "independent_verifier_byte_pin_count":
            len(INDEPENDENT_VERIFIER_PINS),
        "reconstructed_counts": counts,
        "cross_precision_geometry_audit": {
            "producer_precision_bits": PRODUCER_BITS,
            "verifier_precision_bits": VERIFIER_BITS,
            "delta": qstr(DELTA),
            "rational_guard_each_side": qstr(ENCLOSURE_GUARD),
            "guard_identity": "delta/10^6",
            "guarded_field_count": 6,
            "guarded_fields": [
                "target_normal_x_enclosure",
                "target_normal_y_enclosure",
                "target_momentum_p_enclosure",
                "target_cosine_c_enclosure",
                "X_r_enclosure",
                "X_p_enclosure",
            ],
            "complete_containment_on_all_72_legs": "PASS",
            "stage0_l1_strict_upper": "8",
            "stage1_l1_strict_upper": "2",
            "stage2_X_r_X_p_exact_zero": True,
        },
        "graph_current_and_trace_audit": {
            "recipient_component_routes": [
                "G:W->W:N",
                "W:N->G:S",
                "G:S->G:N",
            ],
            "both_Eulerian_vector_components_received": "PASS",
            "Piola_graph_current_intertwining": "PASS",
            "input_adapted_Jacobian_present": "PASS",
            "stage0_adapted_derivative_semantics": "EXACT",
            "stage1_stage2_adapted_derivative_semantics": "STRICT_UPPER",
            "source_density_normalization_to_sup_chain": "PASS",
            "tag_aware_witness_instance_constructors": "PASS",
            "stage3_same_child_cancellations": 192,
            "stage3_inter_child_incidences_retained": 23,
            "retained_typed_stage3_trace_count": 48,
            "cross_tag_cancellation_forbidden": True,
        },
        "exact_arithmetic_audit": {
            "stage_F17_strict_uppers": {
                "0": str(F17_BY_STAGE[0]),
                "1": str(F17_BY_STAGE[1]),
                "2": str(F17_BY_STAGE[2]),
            },
            "stage_source_injection_strict_uppers": {
                "0": str(SOURCE_INJECTION[0]),
                "1": str(SOURCE_INJECTION[1]),
                "2": str(SOURCE_INJECTION[2]),
            },
            "stage_end_to_end_strict_uppers": {
                "0": str(END_TO_END[0]),
                "1": str(END_TO_END[1]),
                "2": str(END_TO_END[2]),
            },
            "three_leg_product": str(THREE_LEG_PRODUCT),
            "global_quarter_threshold": qstr(GLOBAL_THRESHOLD),
            "all_local_F17_values_exceed_global_threshold": True,
            "global_threshold_route_passed": False,
        },
        "semantic_mutation_test_count": len(semantic_labels),
        "semantic_mutation_rejection_labels": semantic_labels,
        "strict_json_attack_count": len(strict_labels),
        "strict_json_attack_rejection_labels": strict_labels,
        "determinism_contract": {
            "canonical_JSON":
                "sort_keys=True, indent=2, allow_nan=False, final newline",
            "stable_sort_order": (
                "common_rank,stage for legs/maps;"
                " fragment_rank,side for output traces;"
                " child,stage,roof for F17 slots"
            ),
            "PYTHONHASHSEED_independent": True,
        },
        "safety_state": {
            "rank3_seed_child_field_maturity": "17/18",
            "remaining_uninstalled_child_fields": ["F18"],
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
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    certificate_value = parse_strict_bytes(args.certificate.read_bytes())
    require(type(certificate_value) is dict, "certificate top object")
    r121, r122, r123, r124, _r124v, r43 = load_upstream()
    verification = verification_document(
        args.certificate,
        certificate_value,
        r121,
        r122,
        r123,
        r124,
        r43,
    )
    text = json.dumps(
        verification,
        sort_keys=True,
        indent=2,
        allow_nan=False,
    ) + "\n"
    args.output.write_text(text, encoding="utf-8")
    print(canonical({
        "status": verification["result"]["status"],
        "output": str(args.output),
        "result_sha256": verification["result_sha256"],
        "semantic_mutation_test_count":
            verification["result"]["semantic_mutation_test_count"],
        "strict_json_attack_count":
            verification["result"]["strict_json_attack_count"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
