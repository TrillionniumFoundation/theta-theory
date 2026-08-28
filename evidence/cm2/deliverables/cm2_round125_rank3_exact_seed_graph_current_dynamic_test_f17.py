#!/usr/bin/env python3
"""Round125 exact-seed physical graph-current recipient and installed F17.

Round124 installs F15 on the twenty-four materialized Round121 exact-seed
children.  This producer supplies the missing, genuinely vector-valued F17
interface on those same children.  It does not rename the scalar F11 slots.

For each of the 24 children and each of the three physical collision maps we
construct the two-component Eulerian generator in collision area coordinates
``(r,p)``,

    X_i = (partial_s F_(i,s)) composed with F_(i,0)^(-1),

for the horizontal translation of every W obstacle.  An admitted Round123
curve measure ``mu_i=M_i rho_i d ell_*`` gives the vector Radon measure
``K_i=X_i mu_i``.  Together with the separately typed artificial-cut traces
this defines the graph current
``T_(K,B)=-div(K)+B`` on an explicit common physical C1/dynamic-Holder dual
recipient.  The area-preserving Piola identity intertwines this current with
each actual suffix.  The finite exact-seed F11 pullback bounds therefore give
the F17 values 4915200, 2457600 and 2457600.

The certificate materializes four recipient components and all 72
source-to-target pullback maps.  Stored geometry intervals carry an explicit
``delta/10^6`` cross-precision guard, and artificial source traces retain the
mandatory adapted-density Jacobian.  Stage-3 cancellation is keyed by shared
endpoint-velocity and unnormalized-density witnesses plus the immutable
source-family tag.

Physical traces are zero only by the final Round122 physical-empty
crosswalk.  Artificial traces are never erased by that statement.  At the
Round123 stage-3 output, exactly the 192 new within-child recut incidences
cancel before total variation; the 23 older inter-child incidences remain
typed unless their unnormalized densities are explicitly equal.

The result is child-local 17/18 on one exact-b seed.  It does not satisfy the
global C_dyn threshold, does not install F18, and does not promote global
Gate5 or CM2.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_round121_rank3_exact_seed_three_leg_recut_f5f6 as r121
import cm2_round122_rank3_exact_seed_physical_face_field_bridge as r122
from cm2_round76_r2_numeric_fields_generator import aq


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round125.rank3-exact-seed-graph-current-dynamic-test-f17.v2"
OUTPUT = (
    HERE
    / "cm2-round125-rank3-exact-seed-graph-current-dynamic-test-f17-2026-07-23.json"
)
PRECISION_BITS = 1536
DELTA = Q(1, 10**90)
# The independent verifier re-isolates the same exact analytic seed at a
# different precision.  Arb enclosures produced from two independently
# isolated boxes need not be nested even though both contain the exact
# quantity.  Every stored nonzero geometric interval is therefore widened by
# this explicit rational guard.  It is more than eight times larger than the largest
# 1536/3072/4096-bit cross-precision endpoint escape observed in the complete
# 72-leg replay, while remaining negligible compared with the strict
# generator margins below 8 and 2.
ENCLOSURE_GUARD = DELTA / 10**6

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
ROUND43 = (
    HERE
    / "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
)


# The Round124 producer/certificate and independent verifier/verification are
# mathematical inputs.  Narrative freeze-pack artifacts are appended once
# their canonical bytes exist.
PINS = {
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


F17_BY_STAGE = {0: 4915200, 1: 2457600, 2: 2457600}
RELATIVE_CENTER_ETA = {0: 1, 1: -1, 2: 0}
TARGET_RADII = {0: Q(4, 25), 1: Q(9, 25), 2: Q(9, 25)}
RAW_INCIDENCE_RANK = {0: 15, 1: 14, 2: 14}
ARTIFICIAL_TWO_SIDE_TRACE_STRICT_UPPER = 27
ADAPTED_X_DERIVATIVE_BOUND = {
    0: DELTA,
    1: 7 * DELTA,
    2: 18 * DELTA,
}
ADAPTED_COORDINATE_BY_STAGE = {
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
SOURCE_INJECTION_BY_STAGE = {
    stage: 25 * (1 << RAW_INCIDENCE_RANK[stage])
    + ARTIFICIAL_TWO_SIDE_TRACE_STRICT_UPPER
    for stage in range(3)
}
END_TO_END_BY_STAGE = {
    stage: SOURCE_INJECTION_BY_STAGE[stage] * F17_BY_STAGE[stage]
    for stage in range(3)
}
THREE_LEG_PRODUCT = (
    F17_BY_STAGE[0] * F17_BY_STAGE[1] * F17_BY_STAGE[2]
)
GLOBAL_QUARTER_THRESHOLD = Q(7961063, 7800000)


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


def qstr(value: Q | int) -> str:
    return str(Q(value))


def incidence_rank_from_f11(value: int) -> int:
    require(value > 0 and value % 150 == 0, "F11 rank quotient")
    quotient = value // 150
    require(
        quotient & (quotient - 1) == 0,
        "F11 rank quotient is a power of two",
    )
    return quotient.bit_length() - 1


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
    value = json.loads(
        raw.decode("utf-8", errors="strict"),
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


def validate_row(row: dict[str, Any], label: str) -> None:
    require(type(row) is dict and type(row.get("row_sha256")) is str, label)
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    require(row["row_sha256"] == digest(payload), f"{label} digest")


def verify_pins() -> None:
    for relative, expected in PINS.items():
        path = HERE.parent / relative
        require(path.is_file() and not path.is_symlink(), f"pin:{relative}")
        require(sha256(path) == expected, f"byte pin:{relative}")


def coordinate(row: dict[str, Any]) -> tuple[str, str, int]:
    return (
        row["official_word_key_id"],
        row["refined_homogeneous_subbranch_id"],
        row["roof_level_j"],
    )


def load_inputs() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    verify_pins()
    round121 = strict_document(
        ROUND121,
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
    )["result"]
    round122 = strict_document(
        ROUND122,
        "cm2.round122.rank3-exact-seed-physical-face-field-bridge.v1",
    )["result"]
    round123 = strict_document(
        ROUND123,
        "cm2.round123.rank3-exact-seed-stage3-output-properization-f14.v1",
    )["result"]
    round124 = strict_document(
        ROUND124,
        "cm2.round124.rank3-exact-seed-standard-family-operator-f15.v1",
    )["result"]
    round43_document = strict_json(ROUND43)
    require(
        round43_document["result"]["schema"]
        == "cm2.gate5.round43-duhamel-eulerian-charge-frontier.v1",
        "Round43 schema",
    )
    round43 = round43_document["result"]
    generator_contract = round43["one_step_area_eulerian_generator"]
    require(
        generator_contract["cross_colour_pointwise_bounds"][
            "l1_generator"
        ] == "abs_X_r+abs_X_p<=25*2^B"
        and generator_contract["same_colour_branch"] == "X_s=0",
        "Round43 generator semantics",
    )
    require(
        round124["rank3_seed_child_field_maturity"] == "16/18"
        and round124["count_ledger"]["combined_child_local_slot_count"] == 1920,
        "final Round124 local state",
    )
    require(
        round124["gate5_actual_child_field_status"]["F17"]
        == "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
        "Round124 F17 frontier",
    )
    require(
        round124["gate5_global_maturity"] == "10/18"
        and round124["complete_18_field_block_count"] == 0
        and round124["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "Round124 strict state",
    )
    require(
        len(round124["standard_family_leg_operator_rows"]) == 72
        and len(round124["gate5_F15_slot_rows"]) == 120,
        "Round124 row census",
    )
    require(
        len(round123["merged_internal_cut_rows"]) == 215
        and len(round123["stage3_output_fragment_rows"]) == 216,
        "Round123 incidence census",
    )
    require(
        len(round122["recut_face_trace_rows"]) == 48
        and len(round122["child_face_incidence_rows"]) == 24,
        "Round122 artificial trace census",
    )
    for rows, label in (
        (round124["standard_family_leg_operator_rows"], "Round124 family row"),
        (round124["gate5_F15_slot_rows"], "Round124 F15 row"),
        (round123["stage3_output_fragment_rows"], "Round123 fragment row"),
        (round122["recut_face_trace_rows"], "Round122 trace row"),
        (
            round122["physical_face_typed_empty_audit"][
                "child_stage_boundary_rows"
            ],
            "Round122 child-stage boundary row",
        ),
    ):
        for row in rows:
            validate_row(row, label)
    return round121, round122, round123, round124, round43


def arb_interval(
    value: Any,
    guard: Q = ENCLOSURE_GUARD,
) -> list[str]:
    lower, upper = r121.arb_pair(value)
    return [qstr(lower - guard), qstr(upper + guard)]


def guarded_abs_upper(value: Any) -> Q:
    """Upper absolute value of the stored guarded interval."""

    lower, upper = r121.arb_pair(value)
    return max(abs(lower - ENCLOSURE_GUARD), abs(upper + ENCLOSURE_GUARD))


def graph_current_leg_id(common_child_id: str, stage: int) -> str:
    return "round125-graph-current-leg:" + digest(
        ["round125-graph-current-leg-v1", common_child_id, stage]
    )


def recipient_component_id(component_key: str) -> str:
    return "round125-recipient-component:" + digest(
        ["round125-recipient-component-v1", component_key]
    )


def recipient_pullback_map_id(common_child_id: str, stage: int) -> str:
    return "round125-recipient-pullback-map:" + digest(
        ["round125-recipient-pullback-map-v1", common_child_id, stage]
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
    common_child_id: str, stage: int, side: str, source_trace_id: str
) -> str:
    return "round125-input-artificial-trace:" + digest(
        [
            "round125-input-artificial-trace-v1",
            common_child_id,
            stage,
            side,
            source_trace_id,
        ]
    )


def output_trace_id(fragment_id: str, side: str) -> str:
    return "round125-stage3-output-trace:" + digest(
        ["round125-stage3-output-trace-v1", fragment_id, side]
    )


def stage3_velocity_witness_id(
    endpoint_id: str,
    cut_canonical_sha256: str,
) -> str:
    return "round125-stage3-endpoint-velocity-witness:" + digest(
        [
            "round125-stage3-endpoint-velocity-witness-v2",
            endpoint_id,
            cut_canonical_sha256,
        ]
    )


def stage3_density_witness_id(
    common_child_id: str,
    input_materialized_recut_instance_id: str,
    input_member_tag_template: str,
    endpoint_id: str,
    cut_canonical_sha256: str,
) -> str:
    return "round125-stage3-unnormalized-density-witness:" + digest(
        [
            "round125-stage3-unnormalized-density-witness-v2",
            common_child_id,
            input_materialized_recut_instance_id,
            input_member_tag_template,
            endpoint_id,
            cut_canonical_sha256,
        ]
    )


def build_input_trace_rows(
    round121: dict[str, Any],
    round122: dict[str, Any],
    round124: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    adapted = round121["stage_adapted_coordinate_contract"]
    require(
        round121["source_adapted_cell_rows"][0][
            "u0_x_derivative_exact"
        ] == "1e-90",
        "source adapted derivative",
    )
    require(
        Q(adapted["whole_cell_normalized_derivative_enclosures"][
            "U1_prime_over_delta"
        ][1]) < 7,
        "U1 derivative below 7 delta",
    )
    require(
        Q(adapted["whole_cell_normalized_derivative_enclosures"][
            "U2_prime_over_delta"
        ][1]) < 18,
        "U2 derivative below 18 delta",
    )
    incidences = sorted(
        round122["child_face_incidence_rows"],
        key=lambda row: row["common_rank"],
    )
    trace_map = {
        row["trace_id"]: row for row in round122["recut_face_trace_rows"]
    }
    face_map = {
        row["face_id"]: row
        for row in (
            round122["stationary_outer_face_rows"]
            + round122["parameterized_recut_face_rows"]
        )
    }
    family_map = {
        (row["common_child_id"], row["stage"]): row
        for row in round124["standard_family_leg_operator_rows"]
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
                require(actual_speed < 13, "artificial face speed below 13")
                adapted_jacobian = ADAPTED_X_DERIVATIVE_BOUND[
                    stage
                ]
                trace_coefficient = actual_speed * adapted_jacobian
                require(
                    adapted_jacobian < 1 and trace_coefficient < 13,
                    "adapted trace coefficient below 13",
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
                    "round124_standard_family_leg_operator_row_id": family[
                        "standard_family_leg_operator_row_id"
                    ],
                    "round124_standard_family_leg_operator_row_sha256":
                        family["row_sha256"],
                    "input_materialized_recut_instance_id": family[
                        "input_materialized_recut_instance_id"
                    ],
                    "source_family_member_tag_template": input_contract[
                        "tag"
                    ],
                    "source_family_tag_domain_id":
                        "round125-input-family-tag-domain:" + digest(
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
                        ADAPTED_COORDINATE_BY_STAGE[stage],
                    "stage_adapted_coordinate_x_derivative_bound_value":
                        qstr(adapted_jacobian),
                    "stage_adapted_coordinate_x_derivative_bound_semantics":
                        "EXACT" if stage == 0 else "STRICT_UPPER",
                    "source_x_to_adapted_trace_coefficient_formula": (
                        "|v_face^(x)|*J_*^in,"
                        " J_*^in=|partial_x ell_*|"
                    ),
                    "source_x_to_adapted_trace_coefficient_actual_upper":
                        qstr(trace_coefficient),
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
                    "source_x_face_velocity_symbol": "v_face^(x)=d_s x_face",
                    "adapted_input_density_jacobian_symbol": (
                        "J_*^in=|partial_x ell_*|"
                    ),
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
                    "physical_empty_crosswalk_does_not_erase_this_trace": True,
                    "retained_until_an_opposite_equal_unnormalized_trace_is_joined":
                        True,
                }
                row["row_sha256"] = digest(row)
                rows.append(row)
                lookup[(rank, stage, side)] = row

    cancellation_rows: list[dict[str, Any]] = []
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
                "adjacent input traces belong to distinct family tag domains",
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
                "left_and_right_input_geometric_carriers_are_distinct": (
                    left["input_materialized_recut_instance_id"]
                    != right["input_materialized_recut_instance_id"]
                ),
                "left_source_family_tag_domain_id": left[
                    "source_family_tag_domain_id"
                ],
                "right_source_family_tag_domain_id": right[
                    "source_family_tag_domain_id"
                ],
                "left_and_right_are_distinct_input_family_tag_domains": True,
                "orientations_are_opposite": True,
                "adapted_jacobian_factor_present_on_both_trace_rows": (
                    left["adapted_jacobian_factor_is_not_omitted"]
                    and right["adapted_jacobian_factor_is_not_omitted"]
                ),
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
            cancellation_rows.append(row)
    require(len(rows) == 144, "144 input artificial traces")
    require(len(cancellation_rows) == 69, "69 input incidence rows")
    return rows, cancellation_rows


def build_stage3_output_traces(
    round123: dict[str, Any],
    round122: dict[str, Any],
    round124: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fragments = sorted(
        round123["stage3_output_fragment_rows"],
        key=lambda row: row["fragment_rank"],
    )
    require(
        [row["fragment_rank"] for row in fragments] == list(range(216)),
        "ordered stage3 fragments",
    )
    cut_map = {
        row["endpoint_id"]: row for row in round123["merged_internal_cut_rows"]
    }
    round122_incidence = {
        row["common_child_id"]: row
        for row in round122["child_face_incidence_rows"]
    }
    round122_faces = {
        row["face_id"]: row
        for row in (
            round122["stationary_outer_face_rows"]
            + round122["parameterized_recut_face_rows"]
        )
    }
    stage2_family_map = {
        row["common_child_id"]: row
        for row in round124["standard_family_leg_operator_rows"]
        if row["stage"] == 2
    }
    require(len(stage2_family_map) == 24, "24 Round124 stage2 families")
    rows: list[dict[str, Any]] = []
    lookup: dict[tuple[int, str], dict[str, Any]] = {}
    for fragment in fragments:
        for side, orientation in (("lower", -1), ("upper", 1)):
            endpoint = fragment[f"source_x_{side}_endpoint_id"]
            family = stage2_family_map[fragment["input_common_child_id"]]
            input_contract = family["input_member_contract"]
            require(
                input_contract["geometry_carrier"]
                == family["input_materialized_recut_instance_id"]
                and input_contract["tag"]
                == "<input-standard-family-member-id>",
                "Round124 stage2 input family contract",
            )
            old_source_incidence = round122_incidence[
                fragment["input_common_child_id"]
            ]
            old_source_face_id = old_source_incidence[f"{side}_face_id"]
            old_source_trace_id = old_source_incidence[f"{side}_trace_id"]
            old_source_face = round122_faces[old_source_face_id]
            is_round123_cut = endpoint in cut_map and (
                cut_map[endpoint]["origin"] == "ROUND123_STAGE3_OUTPUT_CUT"
            )
            cut = cut_map.get(endpoint)
            cut_canonical_sha256 = digest(cut) if cut is not None else None
            if is_round123_cut:
                source_face_id: str | None = None
                source_trace_id: str | None = None
                source_face_sha256: str | None = None
                velocity_contract = (
                    "v_endpoint=-(partial_s U3)/(partial_x U3) at the unique"
                    " U3=j*delta root on this tagged input member; the same"
                    " root velocity is used by its two sides"
                )
                endpoint_evidence_sha256 = cut_canonical_sha256
            else:
                require(
                    old_source_face["round121_s0_endpoint_id"] == endpoint,
                    "Round122 source-face endpoint crosswalk",
                )
                source_face_id = old_source_face_id
                source_trace_id = old_source_trace_id
                source_face_sha256 = old_source_face["row_sha256"]
                velocity_contract = (
                    "stage3 physical pushforward of the pinned Round122"
                    " source-face trace and its exact implicit-root velocity"
                )
                endpoint_evidence_sha256 = (
                    cut_canonical_sha256
                    if cut_canonical_sha256 is not None
                    else old_source_face["row_sha256"]
                )
            require(
                type(endpoint_evidence_sha256) is str,
                "stage3 endpoint evidence digest",
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
                "input_common_child_id": fragment["input_common_child_id"],
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
                "source_input_materialized_recut_instance_id": family[
                    "input_materialized_recut_instance_id"
                ],
                "source_input_family_member_tag_template": input_contract[
                    "tag"
                ],
                "source_input_family_tag_domain_id":
                    "round125-stage2-input-family-tag-domain:" + digest(
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
                "round122_source_face_id": source_face_id,
                "round122_source_trace_id": source_trace_id,
                "round122_source_face_row_sha256": source_face_sha256,
                "round123_merged_cut_origin":
                    cut["origin"] if cut is not None else None,
                "round123_merged_cut_natural_index_j":
                    cut["natural_index_j"] if cut is not None else None,
                "round123_merged_cut_x_dyadic_bracket":
                    cut["x_dyadic_bracket"] if cut is not None else None,
                "round123_merged_cut_canonical_sha256":
                    cut_canonical_sha256,
                "endpoint_evidence_canonical_sha256":
                    endpoint_evidence_sha256,
                "trace_velocity_contract": velocity_contract,
                "endpoint_velocity_witness_id":
                    stage3_velocity_witness_id(
                        endpoint, endpoint_evidence_sha256
                    ),
                "unnormalized_density_witness_id":
                    stage3_density_witness_id(
                        fragment["input_common_child_id"],
                        family["input_materialized_recut_instance_id"],
                        input_contract["tag"],
                        endpoint,
                        endpoint_evidence_sha256,
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
                "output_density_jacobian_symbol": (
                    "J_star=|partial ell_*^out/partial ell_*^in|"
                ),
                "Jacobian_factor_is_present_in_unnormalized_density": True,
                "conditional_normalization_is_undone_by_fragment_mass": True,
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
        require(endpoint == right["source_x_endpoint_id"], "shared output cut")
        cut = cut_map[endpoint]
        same_input = (
            left["input_common_child_id"] == right["input_common_child_id"]
        )
        new_stage3_cut = cut["origin"] == "ROUND123_STAGE3_OUTPUT_CUT"
        require(same_input == new_stage3_cut, "stage3 cut/input typing")
        same_input_recut = (
            left["source_input_materialized_recut_instance_id"]
            == right["source_input_materialized_recut_instance_id"]
        )
        same_input_family_row = (
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
            "new cut splits cells; old input cut preserves one output cell",
        )
        require(
            (not same_input or same_input_recut)
            and same_input_family_row == same_input
            and same_input_tag_domain == same_input,
            "stage3 input-family witness typing",
        )
        cut_canonical_sha256 = digest(cut)
        require(
            left["round123_merged_cut_canonical_sha256"]
            == right["round123_merged_cut_canonical_sha256"]
            == cut_canonical_sha256,
            "shared Round123 cut-row digest",
        )
        if same_input:
            cancelled += 1
        else:
            retained += 1
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
            "left_stage3_output_recut_instance_id": left[
                "stage3_output_recut_instance_id"
            ],
            "right_stage3_output_recut_instance_id": right[
                "stage3_output_recut_instance_id"
            ],
            "adjacent_output_natural_cells_are_distinct":
                distinct_output_cells,
            "new_stage3_cut_iff_distinct_adjacent_output_natural_cells":
                new_stage3_cut == distinct_output_cells,
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
            "same_input_materialized_recut_instance": same_input_recut,
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
                same_input_family_row,
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
                if new_stage3_cut
                else "pinned Round121 input-cut velocity pushed through stage3"
            ),
            "unnormalized_density_match_certified": (
                same_input
                and same_input_family_row
                and same_input_tag_domain
            ),
            "endpoint_velocity_match_certified": True,
            "left_endpoint_velocity_witness_id": left[
                "endpoint_velocity_witness_id"
            ],
            "right_endpoint_velocity_witness_id": right[
                "endpoint_velocity_witness_id"
            ],
            "endpoint_velocity_witness_ids_equal": (
                left["endpoint_velocity_witness_id"]
                == right["endpoint_velocity_witness_id"]
            ),
            "left_endpoint_velocity_witness_instance_id_constructor": left[
                "endpoint_velocity_witness_instance_id_constructor"
            ],
            "right_endpoint_velocity_witness_instance_id_constructor":
                right[
                    "endpoint_velocity_witness_instance_id_constructor"
                ],
            "left_unnormalized_density_witness_id": left[
                "unnormalized_density_witness_id"
            ],
            "right_unnormalized_density_witness_id": right[
                "unnormalized_density_witness_id"
            ],
            "unnormalized_density_witness_ids_equal": (
                left["unnormalized_density_witness_id"]
                == right["unnormalized_density_witness_id"]
            ),
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
            "retained_as_two_typed_traces_when_not_matched": not same_input,
            "cancellation_is_fibrewise_in_one_source_family_member_tag": True,
            "equal_source_family_member_tag_is_required": True,
            "cancellation_occurs_before_distinct_output_member_tags_are_assigned":
                True,
            "witness_instance_comparison_rule": (
                "compare velocity and unnormalized-density witness instances"
                " only after adjoining the same immutable source-family tag"
            ),
            "cross_tag_cancellation_forbidden": True,
        }
        require(
            row["endpoint_velocity_witness_ids_equal"],
            "shared endpoint velocity witness",
        )
        require(
            row["unnormalized_density_witness_ids_equal"] == same_input,
            "same-child unnormalized density witness",
        )
        row["row_sha256"] = digest(row)
        incidence_rows.append(row)
    require(len(rows) == 432, "432 output traces")
    require(len(incidence_rows) == 215, "215 output incidences")
    require((cancelled, retained) == (192, 23), "192/23 incidence split")
    return rows, incidence_rows


def build_source_injection_contract_rows(
    round43: dict[str, Any],
) -> list[dict[str, Any]]:
    """Acyclic stage contracts bound by every graph-current leg.

    The later derivation rows enumerate the 24 actual leg hashes per stage.
    Keeping this finite theorem contract separate avoids a circular hash
    dependency: graph rows bind the contract hash, while F17 slots bind the
    post-graph derivation hash.
    """

    rank_law = round43["one_step_area_eulerian_generator"][
        "cross_colour_pointwise_bounds"
    ]
    require(
        rank_law["incidence_rank"] == "1/c_target<=2^B"
        and rank_law["l1_generator"]
        == "abs_X_r+abs_X_p<=25*2^B",
        "Round43 source injection contract laws",
    )
    rows: list[dict[str, Any]] = []
    for stage in range(3):
        rank = RAW_INCIDENCE_RANK[stage]
        generator_budget = 25 * (1 << rank)
        trace_budget = ARTIFICIAL_TWO_SIDE_TRACE_STRICT_UPPER
        total = generator_budget + trace_budget
        require(
            total == SOURCE_INJECTION_BY_STAGE[stage],
            "source injection contract arithmetic",
        )
        row = {
            "source_injection_contract_row_id":
                source_injection_contract_id(stage),
            "stage": stage,
            "round43_manifest_sha256": PINS[
                "deliverables/cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
            ],
            "round43_incidence_rank_law": rank_law["incidence_rank"],
            "round43_generator_l1_law": rank_law["l1_generator"],
            "incidence_rank_B": rank,
            "incidence_rank_is_paid_by_each_leg_positive_cosine_lower":
                True,
            "bulk_generator_budget_per_M_rho_infinity": str(
                generator_budget
            ),
            "bulk_budget_formula": f"25*2^{rank}",
            "two_artificial_trace_budget_per_M_rho_infinity": str(
                trace_budget
            ),
            "source_graph_current_injection_strict_upper": str(total),
            "source_graph_current_injection_formula":
                f"25*2^{rank}+27={total}",
            "hash_dependency_direction": (
                "contract -> graph leg -> stage derivation -> F17 slot"
            ),
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(len(rows) == 3, "three source injection contracts")
    return rows


def build_generator_rows(
    precision_bits: int,
    round121: dict[str, Any],
    round122: dict[str, Any],
    round124: dict[str, Any],
    input_traces: list[dict[str, Any]],
    source_injection_contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    ctx.prec = precision_bits
    inherited = r121.load_inputs()
    seed = r121.locate_seed(inherited)
    root_lower, root_upper, _ls, _us = r121.isolate_anchor_root(seed)
    intervals = {
        child["common_child_id"]: (child, lower, upper)
        for child, lower, upper in r122.common_child_intervals(round121)
    }
    family_rows = {
        (row["common_child_id"], row["stage"]): row
        for row in round124["standard_family_leg_operator_rows"]
    }
    boundary_rows = {
        (row["common_child_id"], row["stage"]): row
        for row in round122["physical_face_typed_empty_audit"][
            "child_stage_boundary_rows"
        ]
    }
    require(len(boundary_rows) == 72, "72 Round122 boundary rows")
    injection_contracts = {
        row["stage"]: row for row in source_injection_contract_rows
    }
    require(len(injection_contracts) == 3, "three injection contracts")
    input_trace_map: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for row in input_traces:
        input_trace_map.setdefault(
            (row["common_child_id"], row["stage"]), []
        ).append(row)
    slots122 = {
        (coordinate(row), row["field_index"]): row
        for row in round122["gate5_F7_F13_F16_slot_rows"]
    }
    slots124 = {
        coordinate(row): row for row in round124["gate5_F15_slot_rows"]
    }
    rows: list[dict[str, Any]] = []
    actual_bounds_by_stage: dict[int, Q] = {0: Q(0), 1: Q(0), 2: Q(0)}
    for family in sorted(
        round124["standard_family_leg_operator_rows"],
        key=lambda row: (row["common_rank"], row["stage"]),
    ):
        child = family["common_child_id"]
        stage = family["stage"]
        _child_row, x_lower, x_upper = intervals[child]
        geometry = r122.moving_geometry(
            seed, (root_lower, root_upper), x_lower, x_upper
        )
        nx, ny, p, c = geometry["collisions"][stage + 1]
        eta = Q(RELATIVE_CENTER_ETA[stage])
        radius = TARGET_RADII[stage]
        x_r = aq(eta) * (ny - (p / c) * nx)
        x_p = aq(eta / radius) * (c * ny - p * nx)
        if stage == 2:
            require(
                r121.arb_pair(x_r.value) == (Q(0), Q(0))
                and r121.arb_pair(x_p.value) == (Q(0), Q(0)),
                "same-colour exact zero before storage",
            )
            x_r_upper = Q(0)
            x_p_upper = Q(0)
        else:
            x_r_upper = guarded_abs_upper(x_r.value)
            x_p_upper = guarded_abs_upper(x_p.value)
        l1_upper = x_r_upper + x_p_upper
        diagnostic_bound = (Q(8), Q(2), Q(0))[stage]
        if stage < 2:
            require(l1_upper < diagnostic_bound, "actual generator diagnostic")
        else:
            require(l1_upper == 0, "same-colour generator zero")
        actual_bounds_by_stage[stage] = max(
            actual_bounds_by_stage[stage], l1_upper
        )

        roof_slot_coordinates = [
            (
                family["official_word_key_id"],
                family["refined_homogeneous_subbranch_id"],
                roof,
            )
            for roof in family["roof_level_js"]
        ]
        f11_rows = [
            slots122[(key, 11)] for key in roof_slot_coordinates
        ]
        f13_rows = [
            slots122[(key, 13)] for key in roof_slot_coordinates
        ]
        f15_rows = [slots124[key] for key in roof_slot_coordinates]
        require(
            all(
                Q(row["field_value_or_contract"]) == F17_BY_STAGE[stage]
                for row in f11_rows
            ),
            "same-stage F11 values",
        )
        derived_rank = incidence_rank_from_f11(F17_BY_STAGE[stage])
        require(
            derived_rank == RAW_INCIDENCE_RANK[stage],
            "F11-derived incidence rank",
        )
        boundary = boundary_rows[(child, stage)]
        source_component_contract = {
            key: (owner, chart)
            for key, owner, chart in RECIPIENT_COMPONENTS
        }[SOURCE_COMPONENT_BY_STAGE[stage]]
        require(
            boundary["source_owner"] == source_component_contract[0]
            and boundary["source_chart"] == source_component_contract[1]
            and boundary["actual_next_owner"]
            == family["actual_collision_owner"],
            "Round122 source/target recipient geometry",
        )
        injection_contract = injection_contracts[stage]
        require(
            injection_contract["incidence_rank_B"] == derived_rank
            and injection_contract[
                "source_graph_current_injection_strict_upper"
            ] == str(SOURCE_INJECTION_BY_STAGE[stage]),
            "stage source injection contract",
        )
        nx_enclosure = arb_interval(nx.value)
        ny_enclosure = arb_interval(ny.value)
        p_enclosure = arb_interval(p.value)
        c_enclosure = arb_interval(c.value)
        c_lower = Q(c_enclosure[0])
        require(c_lower > 0, "positive guarded cosine lower")
        reciprocal_c_upper = Q(1) / c_lower
        require(
            reciprocal_c_upper <= (1 << derived_rank),
            "actual leg pays Round43 incidence rank",
        )
        require(
            all(
                row["field_value_or_contract"] == "0"
                and row["field_bound_semantics"]
                == "EXACT_EMPTY_PHYSICAL_CURRENT_AND_TWO_TRACES"
                for row in f13_rows
            ),
            "Round122 physical trace zero crosswalk",
        )
        traces = sorted(
            input_trace_map[(child, stage)], key=lambda row: row["side"]
        )
        require(len(traces) == 2, "two input traces")
        row = {
            "graph_current_leg_row_id": graph_current_leg_id(child, stage),
            "common_child_id": child,
            "common_rank": family["common_rank"],
            "stage": stage,
            "official_word_key_id": family["official_word_key_id"],
            "refined_homogeneous_subbranch_id": family[
                "refined_homogeneous_subbranch_id"
            ],
            "roof_level_js": family["roof_level_js"],
            "source_collision_owner": (
                boundary["source_owner"]
            ),
            "source_collision_chart": boundary["source_chart"],
            "source_recipient_component_key":
                SOURCE_COMPONENT_BY_STAGE[stage],
            "target_collision_owner": boundary["actual_next_owner"],
            "target_collision_chart": family["actual_collision_chart"],
            "target_recipient_component_key":
                TARGET_COMPONENT_BY_STAGE[stage],
            "target_radius": qstr(radius),
            "horizontal_W_motion_source_velocity": (0, 1, 0)[stage],
            "horizontal_W_motion_target_velocity": (1, 0, 0)[stage],
            "relative_center_velocity_eta": int(eta),
            "eulerian_generator_definition": (
                "X_i=(partial_s F_(i,s)) composed with F_(i,0)^(-1)"
            ),
            "chart_free_generator_formula": {
                "coordinates": "(r=R*theta,p=sin(phi))",
                "area_form": "dr dp",
                "c": "sqrt(1-p^2)",
                "incoming_ray": "u=-c*n+p*J*n",
                "relative_center_derivative": "d_s=eta*e_x",
                "flight_root_derivative": "tau_s=-eta*n_x/c",
                "normal_derivative": (
                    "R*n_s=-eta*e_x-(eta*n_x/c)*u"
                ),
                "X_r": "eta*(n_y-(p/c)*n_x)",
                "X_p": "(eta/R)*(c*n_y-p*n_x)",
                "partial_r_X_r": "(eta/R)*(n_x+(p/c)*n_y)",
                "partial_p_X_p": "-(eta/R)*(n_x+(p/c)*n_y)",
                "divergence_dr_dp": "0 exactly",
            },
            "cross_precision_enclosure_guard": qstr(ENCLOSURE_GUARD),
            "cross_precision_guard_contract": (
                "each stored nonzero Arb interval is widened on both sides by"
                " delta/10^6; the independent verifier must require complete"
                " containment of its fresh enclosure"
            ),
            "target_normal_x_enclosure": nx_enclosure,
            "target_normal_y_enclosure": ny_enclosure,
            "target_momentum_p_enclosure": p_enclosure,
            "target_cosine_c_enclosure": c_enclosure,
            "guarded_target_cosine_strict_lower": qstr(c_lower),
            "guarded_reciprocal_cosine_upper": qstr(
                reciprocal_c_upper
            ),
            "actual_leg_incidence_rank_inequality":
                f"1/c_lower<={1 << derived_rank}=2^{derived_rank}",
            "actual_leg_incidence_rank_inequality_verified": True,
            "X_r_enclosure": arb_interval(
                x_r.value, Q(0) if stage == 2 else ENCLOSURE_GUARD
            ),
            "X_p_enclosure": arb_interval(
                x_p.value, Q(0) if stage == 2 else ENCLOSURE_GUARD
            ),
            "actual_abs_X_r_upper": qstr(x_r_upper),
            "actual_abs_X_p_upper": qstr(x_p_upper),
            "actual_abs_uppers_are_derived_from_stored_guarded_intervals":
                True,
            "actual_l1_generator_upper": qstr(l1_upper),
            "actual_l1_generator_diagnostic_bound_semantics": (
                "STRICT_UPPER" if stage < 2 else "EXACT"
            ),
            "actual_l1_generator_diagnostic_value": qstr(diagnostic_bound),
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
                trace["trace_id"] for trace in traces
            ],
            "artificial_two_side_trace_coefficient_strict_upper": str(
                ARTIFICIAL_TWO_SIDE_TRACE_STRICT_UPPER
            ),
            "artificial_trace_payment": (
                "two oriented sides, each source graph speed <13;"
                " hence total <26<27 per M_i*||rho_i||_infinity"
            ),
            "raw_incidence_rank_B": derived_rank,
            "raw_incidence_rank_derivation": (
                f"Round43 1/c_target<=2^{derived_rank};"
                f" F11/(150)=2^{derived_rank} is an independent"
                " same-stage consistency crosswalk"
            ),
            "round43_rank_law": "1/c_target<=2^B",
            "round43_generator_l1_law": (
                "abs_X_r+abs_X_p<=25*2^B"
            ),
            "round43_manifest_sha256": PINS[
                "deliverables/cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
            ],
            "raw_generator_coefficient_strict_upper": (
                f"25*2^{derived_rank}"
            ),
            "raw_source_graph_current_injection_per_M_rho_infinity_strict_upper":
                str(SOURCE_INJECTION_BY_STAGE[stage]),
            "source_injection_contract_row_id": injection_contract[
                "source_injection_contract_row_id"
            ],
            "source_injection_contract_row_sha256":
                injection_contract["row_sha256"],
            "source_injection_arithmetic": (
                f"25*2^{derived_rank}+27"
                f"={SOURCE_INJECTION_BY_STAGE[stage]}"
            ),
            "source_injection_closure": (
                "TV(K_i)<=25*2^B*M_i"
                "<=25*2^B*M_i*||rho_i||_infinity and"
                " TV(B_i)<27*M_i*||rho_i||_infinity"
            ),
            "input_density_is_normalized_in_adapted_length": True,
            "input_carrier_adapted_length_less_or_equal_delta": family[
                "input_adapted_length_less_or_equal_delta"
            ],
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
            "round122_physical_empty_audit_sha256": round122[
                "physical_face_typed_empty_audit_sha256"
            ],
            "round122_child_stage_boundary_row_sha256": boundary[
                "row_sha256"
            ],
            "round122_child_stage_boundary_source_owner": boundary[
                "source_owner"
            ],
            "round122_child_stage_boundary_source_chart": boundary[
                "source_chart"
            ],
            "round122_child_stage_boundary_actual_next_owner": boundary[
                "actual_next_owner"
            ],
            "artificial_traces_are_not_physical_F13_traces": True,
            "dynamic_test_suffix_strict_upper": str(F17_BY_STAGE[stage]),
            "raw_source_to_target_response_per_M_rho_infinity_strict_upper": str(
                END_TO_END_BY_STAGE[stage]
            ),
            "source_to_target_arithmetic": (
                f"{SOURCE_INJECTION_BY_STAGE[stage]}"
                f"*{F17_BY_STAGE[stage]}"
                f"={END_TO_END_BY_STAGE[stage]}"
            ),
            "input_materialized_recut_instance_id": family[
                "input_materialized_recut_instance_id"
            ],
            "output_geometry_member_ids": family[
                "output_geometry_member_ids"
            ],
            "output_member_count": family["output_member_count"],
            "transparent_wall_roof_split_adds_no_current_or_suffix_factor":
                True,
            "bypass_designated_b3_is_a_collision_angle": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows)
        == len({row["graph_current_leg_row_id"] for row in rows})
        == 72,
        "72 graph-current leg rows",
    )
    require(actual_bounds_by_stage[0] < 8, "stage0 actual X")
    require(actual_bounds_by_stage[1] < 2, "stage1 actual X")
    require(actual_bounds_by_stage[2] == 0, "stage2 exact X")
    return rows


def build_recipient_component_rows() -> list[dict[str, Any]]:
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
        "four recipient components",
    )
    return rows


def build_recipient_pullback_map_rows(
    round122: dict[str, Any],
    round124: dict[str, Any],
    generator_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    components = {
        row["component_key"]: row for row in component_rows
    }
    f11_slots: dict[tuple[str, str, int], dict[str, Any]] = {
        coordinate(row): row
        for row in round122["gate5_F7_F13_F16_slot_rows"]
        if row["field_index"] == 11
    }
    dynamic_rows = {
        row["stage"]: row for row in round122["dynamic_F11_rows"]
    }
    family_rows = {
        (row["common_child_id"], row["stage"]): row
        for row in round124["standard_family_leg_operator_rows"]
    }
    boundary_rows = {
        (row["common_child_id"], row["stage"]): row
        for row in round122["physical_face_typed_empty_audit"][
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
            and target["collision_chart"] == family["actual_collision_chart"],
            "recipient target geometry crosswalk",
        )
        require(
            source["collision_owner"] == generator[
                "source_collision_owner"
            ]
            and source["collision_chart"] == generator[
                "source_collision_chart"
            ]
            and boundary["source_owner"] == source["collision_owner"]
            and boundary["source_chart"] == source["collision_chart"]
            and boundary["actual_next_owner"]
            == target["collision_owner"]
            and generator["source_recipient_component_key"]
            == source["component_key"]
            and generator["target_recipient_component_key"]
            == target["component_key"],
            "recipient source geometry crosswalk",
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
        expected = F17_BY_STAGE[stage]
        require(
            all(
                Q(item["field_value_or_contract"]) == expected
                and item["field_bound_semantics"] == "STRICT_UPPER"
                and item["F11_uses_full_phase_authoritative_envelope"] is True
                for item in f11_rows
            ),
            "recipient map F11 rows",
        )
        dynamic = dynamic_rows[stage]
        require(
            Q(dynamic[
                "full_phase_dynamic_Holder_test_pullback_strict_upper"
            ]) == expected,
            "recipient map dynamic row",
        )
        row = {
            "recipient_pullback_map_row_id":
                recipient_pullback_map_id(child, stage),
            "common_child_id": child,
            "common_rank": generator["common_rank"],
            "stage": stage,
            "official_word_key_id": generator["official_word_key_id"],
            "refined_homogeneous_subbranch_id": generator[
                "refined_homogeneous_subbranch_id"
            ],
            "roof_level_js": generator["roof_level_js"],
            "source_recipient_component_id": source[
                "recipient_component_id"
            ],
            "source_recipient_component_key": source["component_key"],
            "source_recipient_component_row_sha256": source["row_sha256"],
            "target_recipient_component_id": target[
                "recipient_component_id"
            ],
            "target_recipient_component_key": target["component_key"],
            "target_recipient_component_row_sha256": target["row_sha256"],
            "physical_branch_map": (
                f"{source['component_key']}->{target['component_key']}"
            ),
            "input_materialized_recut_instance_id": family[
                "input_materialized_recut_instance_id"
            ],
            "target_collision_owner": family["actual_collision_owner"],
            "target_collision_chart": family["actual_collision_chart"],
            "round122_child_stage_boundary_row_sha256": boundary[
                "row_sha256"
            ],
            "round122_child_stage_boundary_source_owner": boundary[
                "source_owner"
            ],
            "round122_child_stage_boundary_source_chart": boundary[
                "source_chart"
            ],
            "round122_child_stage_boundary_actual_next_owner": boundary[
                "actual_next_owner"
            ],
            "standard_family_leg_operator_row_id": family[
                "standard_family_leg_operator_row_id"
            ],
            "standard_family_leg_operator_row_sha256": family["row_sha256"],
            "graph_current_leg_row_id": generator[
                "graph_current_leg_row_id"
            ],
            "graph_current_leg_row_sha256": generator["row_sha256"],
            "round122_same_key_F11_slot_ids": [
                item["slot_id"] for item in f11_rows
            ],
            "round122_same_key_F11_slot_canonical_sha256s": [
                digest(item) for item in f11_rows
            ],
            "round122_dynamic_F11_stage_row_sha256": digest(dynamic),
            "pullback_action_on_tests": "phi -> phi composed S_i",
            "full_phase_C1_dynamic_Holder_pullback_strict_upper": str(
                expected
            ),
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
            "round43_manifest_sha256": PINS[
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
        "72 recipient pullback maps",
    )
    require(
        {
            stage: sum(row["stage"] == stage for row in rows)
            for stage in range(3)
        }
        == {0: 24, 1: 24, 2: 24},
        "recipient pullback map census",
    )
    return rows


def build_source_injection_derivation_rows(
    round43: dict[str, Any],
    generator_rows: list[dict[str, Any]],
    source_injection_contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rank_law = round43["one_step_area_eulerian_generator"][
        "cross_colour_pointwise_bounds"
    ]
    require(
        rank_law["incidence_rank"] == "1/c_target<=2^B"
        and rank_law["l1_generator"]
        == "abs_X_r+abs_X_p<=25*2^B",
        "Round43 source injection laws",
    )
    contracts = {
        row["stage"]: row for row in source_injection_contract_rows
    }
    require(len(contracts) == 3, "source injection derivation contracts")
    rows: list[dict[str, Any]] = []
    for stage in range(3):
        legs = [row for row in generator_rows if row["stage"] == stage]
        require(len(legs) == 24, "source injection stage legs")
        f11_value = F17_BY_STAGE[stage]
        rank = incidence_rank_from_f11(f11_value)
        generator_budget = 25 * (1 << rank)
        trace_budget = ARTIFICIAL_TWO_SIDE_TRACE_STRICT_UPPER
        total = generator_budget + trace_budget
        require(total == SOURCE_INJECTION_BY_STAGE[stage],
                "source injection total")
        actual_upper = max(
            Q(row["actual_l1_generator_upper"]) for row in legs
        )
        minimum_cosine_lower = min(
            Q(row["guarded_target_cosine_strict_lower"])
            for row in legs
        )
        maximum_reciprocal_cosine_upper = max(
            Q(row["guarded_reciprocal_cosine_upper"])
            for row in legs
        )
        require(
            minimum_cosine_lower > 0
            and maximum_reciprocal_cosine_upper <= (1 << rank),
            "all stage legs pay the incidence rank",
        )
        if stage < 2:
            require(actual_upper < 25 * (1 << rank),
                    "actual generator inside rank budget")
        else:
            require(actual_upper == 0, "same-colour actual generator")
        row = {
            "source_injection_derivation_row_id":
                source_injection_derivation_id(stage),
            "stage": stage,
            "leg_count": 24,
            "source_injection_contract_row_id": contracts[stage][
                "source_injection_contract_row_id"
            ],
            "source_injection_contract_row_sha256": contracts[stage][
                "row_sha256"
            ],
            "graph_current_leg_row_ids": [
                item["graph_current_leg_row_id"] for item in legs
            ],
            "graph_current_leg_row_sha256s": [
                item["row_sha256"] for item in legs
            ],
            "graph_current_leg_rows_canonical_sha256": digest(legs),
            "round43_manifest_sha256": PINS[
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
            "minimum_guarded_target_cosine_strict_lower": qstr(
                minimum_cosine_lower
            ),
            "maximum_guarded_reciprocal_cosine_upper": qstr(
                maximum_reciprocal_cosine_upper
            ),
            "all_24_positive_cosine_rank_inequalities_verified": True,
            "maximum_guarded_actual_l1_generator_upper": qstr(
                actual_upper
            ),
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
            "source_graph_current_injection_formula": (
                f"25*2^{rank}+27={total}"
            ),
            "all_24_leg_rows_bind_this_derivation": all(
                item["raw_incidence_rank_B"] == rank
                and item[
                    "raw_source_graph_current_injection_per_M_rho_infinity_strict_upper"
                ] == str(total)
                and item["input_density_is_normalized_in_adapted_length"]
                is True
                and item[
                    "input_carrier_adapted_length_less_or_equal_delta"
                ] is True
                and item[
                    "actual_leg_incidence_rank_inequality_verified"
                ] is True
                and item["source_injection_contract_row_id"]
                == contracts[stage]["source_injection_contract_row_id"]
                and item["source_injection_contract_row_sha256"]
                == contracts[stage]["row_sha256"]
                for item in legs
            ),
        }
        require(
            row["all_24_leg_rows_bind_this_derivation"],
            "source injection leg binding",
        )
        row["row_sha256"] = digest(row)
        rows.append(row)
    return rows


def common_recipient_theorem() -> dict[str, Any]:
    require(
        SOURCE_INJECTION_BY_STAGE
        == {0: 819227, 1: 409627, 2: 409627},
        "source injection arithmetic",
    )
    require(
        END_TO_END_BY_STAGE
        == {
            0: 4026664550400,
            1: 1006699315200,
            2: 1006699315200,
        },
        "end-to-end arithmetic",
    )
    require(
        THREE_LEG_PRODUCT == 29686813949952000000,
        "three-leg F17 product",
    )
    require(
        all(Q(value) > GLOBAL_QUARTER_THRESHOLD
            for value in F17_BY_STAGE.values()),
        "global quarter threshold failure",
    )
    return {
        "status": (
            "CERTIFIED_FINITE_EXACT_SEED_PHYSICAL_GRAPH_CURRENT_RECIPIENT"
        ),
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
            "source_injection": (
                "||T_(K,B)||_(Y_seed)<=TV(K)+TV(B)"
            ),
            "source_injection_hash_DAG": (
                "3 stage contracts -> 72 graph-current legs ->"
                " 3 complete stage derivations -> 120 F17 slots"
            ),
            "incidence_rank_payment": (
                "every leg has a positive guarded cosine lower and directly"
                " verifies 1/c_lower<=2^B before 25*2^B is used"
            ),
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
        },
        "source_trace_coordinate_payment": {
            "source_parameter": (
                "the common Round121 x parameter, with each typed artificial"
                " face represented by the Round122 analytic graph x_face(s)"
            ),
            "stage_adapted_coordinate_x_derivative_bounds": {
                "stage0": {
                    "semantics": "EXACT",
                    "value": qstr(ADAPTED_X_DERIVATIVE_BOUND[0]),
                },
                "stage1": {
                    "semantics": "STRICT_UPPER",
                    "value": qstr(ADAPTED_X_DERIVATIVE_BOUND[1]),
                },
                "stage2": {
                    "semantics": "STRICT_UPPER",
                    "value": qstr(ADAPTED_X_DERIVATIVE_BOUND[2]),
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
            "vector_push": (
                "Piola_S K=S_#(DS*K) as a vector Radon measure"
            ),
            "boundary_push": "B maps to S_*B",
            "identity": (
                "S_*T_(K,B)=T_(Piola_S K,S_*B)"
            ),
            "pairing_replay": (
                "T_(Piola_S K,S_*B)(phi)=T_(K,B)(phi composed S)"
            ),
            "dual_bound": (
                "Round122 gives ||phi composed S_i||_Dsource"
                " < C_i ||phi||_Dtarget, hence"
                " ||S_i* T||_Ytarget < C_i ||T||_Ysource"
            ),
            "normal_flux_identity": (
                "DS^T*cof(DS)=det(DS)*I=I"
            ),
        },
        "stage_suffix_strict_uppers": {
            "stage0": str(F17_BY_STAGE[0]),
            "stage1": str(F17_BY_STAGE[1]),
            "stage2": str(F17_BY_STAGE[2]),
        },
        "stage_source_injection_strict_uppers": {
            "stage0": str(SOURCE_INJECTION_BY_STAGE[0]),
            "stage1": str(SOURCE_INJECTION_BY_STAGE[1]),
            "stage2": str(SOURCE_INJECTION_BY_STAGE[2]),
        },
        "stage_end_to_end_response_strict_uppers": {
            "stage0": str(END_TO_END_BY_STAGE[0]),
            "stage1": str(END_TO_END_BY_STAGE[1]),
            "stage2": str(END_TO_END_BY_STAGE[2]),
        },
        "generic_three_physical_leg_compositional_bound": str(
            THREE_LEG_PRODUCT
        ),
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
            "threshold": qstr(GLOBAL_QUARTER_THRESHOLD),
            "all_local_F17_values_exceed_threshold": True,
            "C_dyn_equals_one_claimed": False,
            "global_F17_or_strong_F13_inferred": False,
        },
    }


def f17_slot_id(immutable_key: list[Any]) -> str:
    return "round125-gate5-f17-slot:" + digest(
        ["round125-gate5-f17-slot-v1", immutable_key]
    )


def build_f17_slots(
    round122: dict[str, Any],
    round124: dict[str, Any],
    generator_rows: list[dict[str, Any]],
    recipient_pullback_map_rows: list[dict[str, Any]],
    source_injection_derivation_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generators = {
        (row["common_child_id"], row["stage"]): row
        for row in generator_rows
    }
    recipient_maps = {
        (row["common_child_id"], row["stage"]): row
        for row in recipient_pullback_map_rows
    }
    source_injection_derivations = {
        row["stage"]: row for row in source_injection_derivation_rows
    }
    require(
        len(source_injection_derivations) == 3,
        "three F17 source injection derivations",
    )
    f11 = {
        coordinate(row): row
        for row in round122["gate5_F7_F13_F16_slot_rows"]
        if row["field_index"] == 11
    }
    rows: list[dict[str, Any]] = []
    keys: set[str] = set()
    for f15 in sorted(
        round124["gate5_F15_slot_rows"],
        key=lambda row: (
            row["common_child_id"], row["stage"], row["roof_level_j"]
        ),
    ):
        key3 = coordinate(f15)
        generator = generators[(f15["common_child_id"], f15["stage"])]
        recipient_map = recipient_maps[
            (f15["common_child_id"], f15["stage"])
        ]
        injection_derivation = source_injection_derivations[
            f15["stage"]
        ]
        require(
            any(
                row_id == generator["graph_current_leg_row_id"]
                and row_sha == generator["row_sha256"]
                for row_id, row_sha in zip(
                    injection_derivation["graph_current_leg_row_ids"],
                    injection_derivation[
                        "graph_current_leg_row_sha256s"
                    ],
                    strict=True,
                )
            ),
            "F17 source injection derivation binds graph leg",
        )
        immutable_key = [
            f15["official_word_key_id"],
            f15["refined_homogeneous_subbranch_id"],
            f15["roof_level_j"],
            "dynamic_test_operator_cost",
        ]
        key_text = canonical(immutable_key)
        require(key_text not in keys, "unique F17 key")
        keys.add(key_text)
        f11_row = f11[key3]
        value = F17_BY_STAGE[f15["stage"]]
        require(Q(f11_row["field_value_or_contract"]) == value,
                "F11/F17 numeric crosswalk")
        row = {
            "slot_id": f17_slot_id(immutable_key),
            "immutable_slot_key": immutable_key,
            "official_word_key_id": f15["official_word_key_id"],
            "refined_homogeneous_subbranch_id": f15[
                "refined_homogeneous_subbranch_id"
            ],
            "roof_level_j": f15["roof_level_j"],
            "field_index": 17,
            "field_name": "dynamic_test_operator_cost",
            "field_bound_semantics": "STRICT_UPPER",
            "field_value_or_contract": str(value),
            "slot_status": "CERTIFIED_ON_THIS_EXACT_SEED_COMMON_CHILD",
            "common_child_id": f15["common_child_id"],
            "stage": f15["stage"],
            "graph_current_leg_row_id": generator[
                "graph_current_leg_row_id"
            ],
            "graph_current_leg_row_sha256": generator["row_sha256"],
            "source_injection_contract_row_id": generator[
                "source_injection_contract_row_id"
            ],
            "source_injection_contract_row_sha256": generator[
                "source_injection_contract_row_sha256"
            ],
            "source_injection_derivation_row_id": injection_derivation[
                "source_injection_derivation_row_id"
            ],
            "source_injection_derivation_row_sha256":
                injection_derivation["row_sha256"],
            "recipient_pullback_map_row_id": recipient_map[
                "recipient_pullback_map_row_id"
            ],
            "recipient_pullback_map_row_sha256": recipient_map[
                "row_sha256"
            ],
            "source_recipient_component_id": recipient_map[
                "source_recipient_component_id"
            ],
            "target_recipient_component_id": recipient_map[
                "target_recipient_component_id"
            ],
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
        len(rows) == len({row["slot_id"] for row in rows}) == 120,
        "120 F17 slots",
    )
    require(
        {
            stage: sum(row["stage"] == stage for row in rows)
            for stage in range(3)
        }
        == {0: 48, 1: 24, 2: 48},
        "F17 stage census",
    )
    return rows


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    require(precision_bits >= 1024, "producer precision")
    round121, round122, round123, round124, round43 = load_inputs()
    source_injection_contract_rows = (
        build_source_injection_contract_rows(round43)
    )
    input_traces, input_incidences = build_input_trace_rows(
        round121, round122, round124
    )
    output_traces, output_incidences = build_stage3_output_traces(
        round123, round122, round124
    )
    generator_rows = build_generator_rows(
        precision_bits,
        round121,
        round122,
        round124,
        input_traces,
        source_injection_contract_rows,
    )
    recipient_component_rows = build_recipient_component_rows()
    recipient_pullback_map_rows = build_recipient_pullback_map_rows(
        round122,
        round124,
        generator_rows,
        recipient_component_rows,
    )
    source_injection_rows = build_source_injection_derivation_rows(
        round43, generator_rows, source_injection_contract_rows
    )
    f17_rows = build_f17_slots(
        round122,
        round124,
        generator_rows,
        recipient_pullback_map_rows,
        source_injection_rows,
    )

    inherited_digest = round124[
        "combined_installed_child_local_slot_registry"
    ]
    require(inherited_digest["combined_slot_count"] == 1920,
            "Round124 combined registry")
    new_ids = [row["slot_id"] for row in f17_rows]
    require(len(new_ids) == len(set(new_ids)) == 120, "new F17 IDs")

    base = dict(round124)
    for key in (
        "status",
        "strict_scope",
        "strict_nonclaims",
        "upstream_and_helper_pins",
    ):
        base.pop(key)
    gate_status = dict(round124["gate5_actual_child_field_status"])
    gate_status["F17"] = (
        "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN"
    )
    count_ledger = dict(round124["count_ledger"])
    count_ledger.update(
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
    base.update(
        {
            "status": (
                "CERTIFIED_EXACT_SEED_PHYSICAL_GRAPH_CURRENT_DYNAMIC_TEST"
                "__F17_INSTALLED"
            ),
            "precision_bits": precision_bits,
            "round124_contract": {
                "producer_sha256": PINS[
                    "deliverables/cm2_round124_rank3_exact_seed_standard_family_operator_f15.py"
                ],
                "certificate_sha256": PINS[
                    "deliverables/cm2-round124-rank3-exact-seed-standard-family-operator-f15-2026-07-23.json"
                ],
                "verifier_sha256": PINS[
                    "deliverables/cm2_round124_rank3_exact_seed_standard_family_operator_f15_verifier.py"
                ],
                "verification_sha256": PINS[
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
                "producer_precision_bits": precision_bits,
                "independent_verifier_precision_bits": 3072,
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
            "recipient_component_rows": recipient_component_rows,
            "recipient_component_rows_sha256": digest(
                recipient_component_rows
            ),
            "recipient_pullback_map_rows": recipient_pullback_map_rows,
            "recipient_pullback_map_rows_sha256": digest(
                recipient_pullback_map_rows
            ),
            "source_injection_derivation_rows": source_injection_rows,
            "source_injection_derivation_rows_sha256": digest(
                source_injection_rows
            ),
            "source_injection_contract_rows":
                source_injection_contract_rows,
            "source_injection_contract_rows_sha256": digest(
                source_injection_contract_rows
            ),
            "graph_current_leg_rows": generator_rows,
            "graph_current_leg_rows_sha256": digest(generator_rows),
            "input_artificial_trace_rows": input_traces,
            "input_artificial_trace_rows_sha256": digest(input_traces),
            "input_internal_trace_incidence_rows": input_incidences,
            "input_internal_trace_incidence_rows_sha256": digest(
                input_incidences
            ),
            "stage3_output_artificial_trace_rows": output_traces,
            "stage3_output_artificial_trace_rows_sha256": digest(output_traces),
            "stage3_output_trace_incidence_rows": output_incidences,
            "stage3_output_trace_incidence_rows_sha256": digest(
                output_incidences
            ),
            "trace_cancellation_theorem": {
                "rule": (
                    "cancel an internal artificial trace before total"
                    " variation iff the two orientations oppose and the"
                    " unnormalized trace densities agree"
                ),
                "normalized_conditional_density_equality_is_not_required":
                    True,
                "mass_times_conditional_density_recovers_unnormalized_density":
                    True,
                "endpoint_velocity_must_also_match": True,
                "cancellation_is_fibrewise_in_one_source_family_member_tag":
                    True,
                "cross_family_member_tag_cancellation_allowed": False,
                "source_family_tag_is_pinned_to_Round124_stage2_input_member_contract":
                    True,
                "cancellation_precedes_distinct_output_fragment_member_tags":
                    True,
                "Round123_new_stage3_cut_count": 192,
                "new_stage3_cuts_are_within_one_input_child": True,
                "new_stage3_cut_rows_are_bound_by_canonical_sha256": True,
                "new_stage3_root_velocity_law": (
                    "v_endpoint=-(partial_s U3)/(partial_x U3)"
                    " at U3=j*delta"
                ),
                "new_stage3_cut_velocity_is_shared_by_both_sides": True,
                "shared_endpoint_velocity_witness_id_is_reconstructed":
                    True,
                "shared_unnormalized_density_witness_id_is_reconstructed":
                    True,
                "output_Jacobian_factor_is_present_before_cancellation":
                    True,
                "new_stage3_cuts_cancelled_before_TV": 192,
                "old_Round121_inter_child_cut_count": 23,
                "old_inter_child_densities_assumed_equal": False,
                "old_inter_child_incidences_cancelled_unconditionally": 0,
                "old_inter_child_trace_sides_retained": 46,
                "outer_trace_sides_retained": 2,
                "retained_typed_stage3_trace_count": 48,
                "physical_trace_empty_statement_erases_artificial_traces":
                    False,
            },
            "gate5_F17_slot_rows": f17_rows,
            "gate5_F17_slot_rows_sha256": digest(f17_rows),
            "combined_installed_child_local_slot_registry_after_F17": {
                "Round124_inherited_slot_count": 1920,
                "Round123_combined_slot_ids_sha256": inherited_digest[
                    "Round123_combined_slot_ids_sha256"
                ],
                "Round124_new_F15_slot_ids_sha256": inherited_digest[
                    "new_F15_slot_ids_sha256"
                ],
                "new_F17_slot_count": 120,
                "new_F17_slot_ids_sha256": digest(new_ids),
                "combined_slot_count": 2040,
                "slot_count_per_certified_field": 120,
                "certified_field_indices": list(range(1, 18)),
                "uninstalled_field_indices": [18],
                "combined_registry_chain_sha256": digest(
                    [
                        inherited_digest[
                            "Round123_combined_slot_ids_sha256"
                        ],
                        inherited_digest["new_F15_slot_ids_sha256"],
                        new_ids,
                    ]
                ),
                "all_keys_are_full_word_subbranch_roof_field_keys": True,
                "stage3_trace_and_fragment_payloads_are_not_source_slot_keys":
                    True,
            },
            "count_ledger": count_ledger,
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
    args = parser.parse_args()
    document = build(args.precision_bits)
    args.output.write_text(
        json.dumps(document, sort_keys=True, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.output}")
    print(f"result_sha256={document['result_sha256']}")
    print("ROUND125_EXACT_SEED_FIELD_MATURITY=17/18")
    print("GLOBAL_GATE5=10/18")
    print("CM2=NO-GO_FOR_CLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
