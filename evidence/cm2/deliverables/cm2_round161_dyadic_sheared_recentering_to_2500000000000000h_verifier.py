#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_round161_dyadic_sheared_recentering_engine as engine


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / (
    "cm2-round161-dyadic-sheared-recentering-to-"
    "2500000000000000h-2026-07-25.json"
)
OUTPUT = HERE / (
    "cm2-round161-dyadic-sheared-recentering-to-"
    "2500000000000000h-verification-2026-07-25.json"
)
CERTIFICATE_SCHEMA = (
    "cm2.round161.dyadic-sheared-recentering-to-"
    "2500000000000000h.v1"
)
SCHEMA = (
    "cm2.round161.dyadic-sheared-recentering-to-"
    "2500000000000000h.verification.v1"
)
STATUS = (
    "CERTIFIED_DYADIC_SHEARED_RECENTERING_TO_"
    "2500000000000000H__D02_STILL_BLOCKED"
)
PRIOR_CERTIFICATE = (
    "cm2-round160-sheared-macro-scale-jump-to-100000h-2026-07-25.json"
)
PRIOR_VERIFICATION = (
    "cm2-round160-sheared-macro-scale-jump-to-100000h-verification-"
    "2026-07-25.json"
)
PRODUCER = (
    "cm2_round161_dyadic_sheared_recentering_to_"
    "2500000000000000h.py"
)
ENGINE = "cm2_round161_dyadic_sheared_recentering_engine.py"
ROUND160_ENGINE = "cm2_round160_sheared_scale_jump_engine.py"
PINS = {
    PRODUCER:
        "7122fc6f38389657292160d7fb1a7248434163123853f5dcd5246b48b1efae73",
    ENGINE:
        "ae5c2ac7d22de85ae4a3d39b3ce42307c5c39e652ed1643a46c5630d746c050f",
    ROUND160_ENGINE:
        "1de1fe55020fbb7de975c4fa04cd820723e9296a4d69db493092fe9b3f579122",
    PRIOR_CERTIFICATE:
        "f2243caf5d14e5876388f48f468927b5846284c5997879e23d70d1456a6bca5f",
    PRIOR_VERIFICATION:
        "7495730c2be0df01470169469c4a91af659b1f926e6fb1748aaec220d072c731",
}
PRIOR_CERTIFICATE_RESULT_SHA256 = (
    "984855ea7a08fa5aea8728b7f51f5b5e3ed8a57ca840e7d2448c39adf0d7a4a0"
)
PRIOR_VERIFICATION_RESULT_SHA256 = (
    "a07050a832d7d0971c6e0dce43c14b2a958fdc48116444ef5ca7b1dd4b5f0279"
)
PART_NAMES = ("c24", "bridge", "d3")
U0 = Q(100000)
U1 = Q(2500000000000000)
OLD_SLOPE = Q(2807, 1000)
NEW_SLOPE = Q(1403486916994043, 500000000000000)
NEXT_CORE_GATE = (
    "continue dyadic sheared-slope recentering in compact angular "
    "coordinates to the first certified chart, owner, event, or terminal "
    "face; then exhaust disconnected exterior sheets on the fundamental "
    "compact angular domain"
)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def normalize(value: Any) -> Any:
    return json.loads(canonical(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def same(actual: Any, expected: Any) -> bool:
    """Canonical JSON equality is deliberately bool/int type-sensitive."""
    return canonical(actual) == canonical(expected)


def strict_load_raw(raw: bytes) -> dict[str, Any]:
    def reject(value: str) -> None:
        raise ValueError(value)

    def reject_float(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result

    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "encoding",
    )
    result = json.loads(
        raw.decode(),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject_float,
    )

    def check_strings(value: Any) -> None:
        if type(value) is str:
            require(
                "\x00" not in value
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in value
                ),
                "decoded string encoding",
            )
        elif type(value) is list:
            for item in value:
                check_strings(item)
        elif type(value) is dict:
            for key, item in value.items():
                check_strings(key)
                check_strings(item)

    check_strings(result)
    require(type(result) is dict, "top object")
    return result


def strict_load(path: Path) -> dict[str, Any]:
    return strict_load_raw(path.read_bytes())


def check_pins() -> None:
    require(
        Path(engine.__file__).resolve() == (HERE / ENGINE).resolve(),
        "engine module identity",
    )
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    engine.check_pins()


def load_prior() -> tuple[dict[str, Any], dict[str, Any]]:
    prior_document = strict_load(HERE / PRIOR_CERTIFICATE)
    verification_document = strict_load(HERE / PRIOR_VERIFICATION)
    require(
        set(prior_document) == {"schema", "result", "result_sha256"}
        and prior_document["schema"]
        == "cm2.round160.sheared-macro-scale-jump-to-100000h.v1"
        and prior_document["result_sha256"]
        == PRIOR_CERTIFICATE_RESULT_SHA256
        == digest(prior_document["result"]),
        "prior certificate wrapper",
    )
    require(
        set(verification_document)
        == {"schema", "result", "result_sha256"}
        and verification_document["schema"]
        == "cm2.round160.sheared-macro-scale-jump-to-100000h.verification.v1"
        and verification_document["result_sha256"]
        == PRIOR_VERIFICATION_RESULT_SHA256
        == digest(verification_document["result"])
        and verification_document["result"]["status"] == "PASS"
        and verification_document["result"]["certificate_result_sha256"]
        == prior_document["result_sha256"],
        "prior verification wrapper",
    )
    prior = prior_document["result"]
    require(
        prior["status"]
        == "CERTIFIED_SHEARED_MACRO_SCALE_JUMP_TO_100000H__D02_STILL_BLOCKED"
        and same(
            prior["certified_abs_delta_x_corridor_in_h_units"],
            ["0", "100000"],
        )
        and same(
            prior["combined_typed_atlas"],
            {
                "connected": True,
                "interior_untyped_event_cell_count": 0,
                "lower_symmetry_axis_terminal": True,
                "slab_count": 74,
                "typed_box_count": 222,
                "upper_endpoint_in_h_units": "100000",
                "upper_endpoint_terminal": False,
            },
        )
        and same(
            prior["strict_nonpromotion"],
            {
                "D02_status": "BLOCKED",
                "D03_authorized": False,
                "global_gate5_maturity": "10/18",
                "global_complete_18_field_block_count": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
        ),
        "prior strict state",
    )
    return prior_document, verification_document


def fixed_specifications() -> dict[str, dict[str, str]]:
    expected = {
        "c24": {
            "kind": "C24_EVENT",
            "u_lower_h": "100000",
            "u_upper_h": "2500000000000000",
            "slope_beta_per_abs_x":
                "1403486916994043/500000000000000",
            "w_lower_h": "-430",
            "w_upper_h": "-405",
        },
        "bridge": {
            "kind": "STRICT_RETURN_BRIDGE",
            "u_lower_h": "100000",
            "u_upper_h": "2500000000000000",
            "slope_beta_per_abs_x":
                "1403486916994043/500000000000000",
            "w_lower_h": "-405",
            "w_upper_h": "-350",
        },
        "d3": {
            "kind": "D3_EVENT",
            "u_lower_h": "100000",
            "u_upper_h": "2500000000000000",
            "slope_beta_per_abs_x":
                "1403486916994043/500000000000000",
            "w_lower_h": "-350",
            "w_upper_h": "134111000000",
        },
    }
    actual = engine.specs()
    require(
        type(actual) is dict
        and set(actual) == set(PART_NAMES)
        and all(
            type(spec) is dict
            and set(spec)
            == {
                "kind",
                "u_lower_h",
                "u_upper_h",
                "slope_beta_per_abs_x",
                "w_lower_h",
                "w_upper_h",
            }
            and all(type(value) is str for value in spec.values())
            for spec in actual.values()
        )
        and same(actual, expected),
        "fixed Round161 specification",
    )
    return expected


def validate_parts(
    parts: dict[str, dict[str, Any]],
    specs: dict[str, dict[str, str]],
) -> None:
    require(
        type(parts) is dict and set(parts) == set(PART_NAMES),
        "part names",
    )
    require(
        set(parts["c24"]) == {"frontier", "full_audit"}
        and set(parts["bridge"]) == {"full_audit"}
        and set(parts["d3"]) == {"frontier", "full_audit"},
        "part wrappers",
    )
    records = (
        (parts["c24"]["frontier"], specs["c24"], False),
        (parts["c24"]["full_audit"], specs["c24"], True),
        (parts["bridge"]["full_audit"], specs["bridge"], True),
        (parts["d3"]["frontier"], specs["d3"], False),
        (parts["d3"]["full_audit"], specs["d3"], True),
    )
    for record, spec, full in records:
        require(
            type(record) is dict
            and record["status"] == "PASS"
            and same(
                record["u_in_h_units"],
                [spec["u_lower_h"], spec["u_upper_h"]],
            )
            and same(
                record["w_in_h_units"],
                [spec["w_lower_h"], spec["w_upper_h"]],
            )
            and record["slope_s"] == spec["slope_beta_per_abs_x"],
            "audit coordinate identity",
        )
        if full:
            require(
                record["runtime_adapter_restored"] is True,
                "runtime adapter restoration",
            )
    c24 = parts["c24"]["full_audit"]
    bridge = parts["bridge"]["full_audit"]
    d3 = parts["d3"]["full_audit"]
    require(
        parts["c24"]["frontier"]["event_kind"]
        == "COLLISION1648_TERMINAL_C24_P0_ZERO"
        and parts["d3"]["frontier"]["event_kind"]
        == "COLLISION3_D0_TANGENCY_D3_ZERO"
        and type(c24["collision_count"]) is int
        and c24["collision_count"] == 1648
        and type(bridge["collision_count"]) is int
        and bridge["collision_count"] == 1648
        and bridge["terminal_classification"] == "RETURN_AT_3_INNER",
        "typed audit semantics",
    )
    require(
        all(
            type(record[field]) is str
            and record[field].startswith("round161-")
            and "round160" not in record[field]
            for record, field in (
                (parts["c24"]["frontier"], "event_box_id"),
                (c24, "event_box_id"),
                (bridge, "bridge_cell_id"),
                (parts["d3"]["frontier"], "event_box_id"),
                (d3, "event_box_id"),
            )
        ),
        "Round161 identifiers",
    )
    require(
        all(
            type(record[field]) is int and record[field] >= 0
            for record, field in (
                (c24, "full_radius4_candidate_test_count"),
                (bridge, "full_radius4_candidate_test_count"),
                (d3, "fully_audited_prefix_radius4_candidate_test_count"),
                (d3, "collision3_full_radius4_candidate_test_count"),
            )
        ),
        "candidate census integer types",
    )
    anchor = c24["collision3_correlated_anchor_exclusion"]
    correlated = c24["collision3_correlated_candidate_audits"]
    require(
        type(anchor) is dict
        and anchor["collision_index"] == 3
        and anchor["anchor_candidate"] == "W[0,0]"
        and anchor["D3_strictly_increasing_in_w"] is True
        and anchor["D3_upper_w_edge_in_h_units"] == "-405"
        and anchor["D3_upper_w_edge_strict_negative_for_all_u"] is True
        and anchor["D3_maximum_strict_negative"] is True
        and type(anchor["D3_miss_margin_dyadic_depth"]) is int
        and anchor[
            "applies_to_retained_and_full_radius4_candidate_universes"
        ] is True
        and anchor[
            "general_box_complete_owner_anchor_discriminant_overwraps_zero"
        ] is True
        and anchor["correlation_preserved_by_sheared_scalar_model"] is True
        and c24["collision3_correlated_adapter_restored"] is True,
        "C24 collision3 correlated anchor proof",
    )
    require(
        type(correlated) is dict
        and set(correlated) == {"retained", "full_radius4"}
        and all(
            type(record) is dict
            and record["anchor_candidate_count"] == 1
            and record["ambiguous_nonanchor_candidate_count"] == 0
            and record["selected_target_id"] == "W[0,-1]"
            and record["selected_target_matches_minus_branch"] is True
            and same(record["anchor"], anchor)
            for record in correlated.values()
        )
        and correlated["full_radius4"]["candidate_count"] == 161
        and correlated["full_radius4"]["nonanchor_candidate_count"] == 160,
        "C24 collision3 correlated candidate audits",
    )


def expected_census(
    parts: dict[str, dict[str, Any]],
) -> dict[str, int]:
    c24 = parts["c24"]["full_audit"]
    bridge = parts["bridge"]["full_audit"]
    d3 = parts["d3"]["full_audit"]
    r1648_tests = (
        c24["full_radius4_candidate_test_count"]
        + bridge["full_radius4_candidate_test_count"]
    )
    d3_tests = (
        d3["fully_audited_prefix_radius4_candidate_test_count"]
        + d3["collision3_full_radius4_candidate_test_count"]
    )
    return {
        "new_full_R1648_C24_audits": 1,
        "new_full_R1648_bridge_audits": 1,
        "new_collision_stage_object_pairs":
            c24["collision_count"] + bridge["collision_count"],
        "new_R1648_path_radius4_candidate_tests": r1648_tests,
        "new_full_D3_event_box_audits": 1,
        "new_D3_event_box_radius4_candidate_tests": d3_tests,
        "new_total_radius4_candidate_tests": r1648_tests + d3_tests,
    }


def overlap(first: list[str], second: list[str]) -> list[str]:
    require(
        type(first) is list
        and type(second) is list
        and len(first) == len(second) == 2
        and all(type(value) is str for value in first + second),
        "face schema",
    )
    lower = max(Q(first[0]), Q(second[0]))
    upper = min(Q(first[1]), Q(second[1]))
    require(lower < upper, "strict physical beta overlap")
    return [engine.qstr(lower), engine.qstr(upper)]


def physical_face(slope: Q, u: Q, w_face: list[str]) -> list[str]:
    require(
        type(w_face) is list
        and len(w_face) == 2
        and all(type(value) is str for value in w_face),
        "w face",
    )
    return [
        engine.qstr(slope * u + Q(w_face[0])),
        engine.qstr(slope * u + Q(w_face[1])),
    ]


def expected_inherited_adjacency(
    prior: dict[str, Any],
    specs: dict[str, dict[str, str]],
) -> dict[str, Any]:
    previous = prior["new_sheared_macro_scale_jump"][
        "new_macro_slabs"
    ][-1]
    require(
        same(previous["u_in_h_units"], ["352", "100000"]),
        "prior terminal macro slab",
    )
    previous_chain = previous["w_typed_box_chain"]
    expected_previous_chain = [
        {"kind": "C24_EVENT", "w_in_h_units": ["-420", "-405"]},
        {
            "kind": "STRICT_RETURN_BRIDGE",
            "w_in_h_units": ["-405", "-10"],
        },
        {"kind": "D3_EVENT", "w_in_h_units": ["-10", "10"]},
    ]
    require(
        same(previous_chain, expected_previous_chain)
        and Q(previous["coordinate_map"]["slope_s"]) == OLD_SLOPE,
        "prior terminal typed chain",
    )
    shift = (OLD_SLOPE - NEW_SLOPE) * U0
    require(
        shift
        == Q(13083005957, 5000000000),
        "exact slope shift",
    )
    prior_w = {
        record["kind"]: record["w_in_h_units"]
        for record in previous_chain
    }
    by_kind = {
        spec["kind"]: spec
        for spec in specs.values()
    }
    records: dict[str, Any] = {}
    for kind in ("C24_EVENT", "STRICT_RETURN_BRIDGE", "D3_EVENT"):
        prior_face = physical_face(OLD_SLOPE, U0, prior_w[kind])
        new_face = engine.physical_beta_face(by_kind[kind], U0)
        records[kind] = {
            "prior_w_face_in_h_units": prior_w[kind],
            "new_w_face_in_h_units": [
                by_kind[kind]["w_lower_h"],
                by_kind[kind]["w_upper_h"],
            ],
            "prior_physical_beta_face_in_h_units": prior_face,
            "new_physical_beta_face_in_h_units": new_face,
            "strict_physical_beta_overlap_in_h_units": overlap(
                prior_face,
                new_face,
            ),
        }
    return {
        "shared_u_face_in_h_units": "100000",
        "prior_coordinate_system": "SHEARED_COMPACT_ANGLE_LIFT",
        "new_coordinate_system": "SHEARED_COMPACT_ANGLE_LIFT",
        "prior_slope_s": engine.qstr(OLD_SLOPE),
        "new_slope_s": engine.qstr(NEW_SLOPE),
        "new_w_equals_prior_w_plus_slope_shift_u_in_h_units":
            engine.qstr(shift),
        "slope_change_applied_exactly": True,
        "all_three_typed_boxes_have_strict_physical_beta_overlap": True,
        "typed_box_overlaps": records,
    }


def expected_result(
    parts: dict[str, dict[str, Any]],
    prior_document: dict[str, Any],
    verification_document: dict[str, Any],
) -> dict[str, Any]:
    specs = fixed_specifications()
    validate_parts(parts, specs)
    width = U1 - U0
    require(
        width == Q(2499999999900000)
        and width.denominator == 1
        and width.numerator % 4 == 0,
        "huge endpoint arithmetic",
    )
    equivalent_4h_slabs = width.numerator // 4
    require(
        equivalent_4h_slabs == 624999999975000,
        "equivalent 4h arithmetic",
    )
    w_chain = [
        {
            "kind": specs[name]["kind"],
            "w_in_h_units": [
                specs[name]["w_lower_h"],
                specs[name]["w_upper_h"],
            ],
        }
        for name in PART_NAMES
    ]
    require(
        Q(w_chain[0]["w_in_h_units"][1])
        == Q(w_chain[1]["w_in_h_units"][0])
        and Q(w_chain[1]["w_in_h_units"][1])
        == Q(w_chain[2]["w_in_h_units"][0]),
        "gap-free w chain",
    )
    macro_slab = {
        "label":
            "dyadic-sheared-recentering-100000-to-2500000000000000",
        "u_in_h_units": [engine.qstr(U0), engine.qstr(U1)],
        "u_width_in_h_units": engine.qstr(width),
        "coordinate_map": {
            "coordinate_system": "SHEARED_COMPACT_ANGLE_LIFT",
            "u_definition": "u=abs(delta_x)/h=-delta_x/h",
            "w_definition": "w=delta_beta/h-s*u",
            "slope_s": engine.qstr(NEW_SLOPE),
        },
        "equivalent_exact_4h_slab_count": equivalent_4h_slabs,
        "typed_box_count": 3,
        "typed_box_audits": parts,
        "typed_box_audits_sha256": digest(parts),
        "w_typed_box_chain": w_chain,
        "exact_w_face_adjacencies": [
            {
                "left_kind": "C24_EVENT",
                "right_kind": "STRICT_RETURN_BRIDGE",
                "shared_w_face_in_h_units": "-405",
            },
            {
                "left_kind": "STRICT_RETURN_BRIDGE",
                "right_kind": "D3_EVENT",
                "shared_w_face_in_h_units": "-350",
            },
        ],
        "w_faces_gap_free": True,
        "interior_event_cells_untyped": 0,
    }
    prior = prior_document["result"]
    adjacency = expected_inherited_adjacency(prior, specs)
    return {
        "status": STATUS,
        "physical_coordinate_scale": "h=2^-4296",
        "inherited_round160_result_sha256": prior_document["result_sha256"],
        "inherited_round160_verification_result_sha256":
            verification_document["result_sha256"],
        "certified_abs_delta_x_corridor_in_h_units": [
            "0",
            "2500000000000000",
        ],
        "new_dyadic_sheared_recentering": {
            "new_typed_slab_count": 1,
            "new_typed_box_count": 3,
            "new_macro_slabs": [macro_slab],
            "new_macro_slabs_sha256": digest([macro_slab]),
            "inherited_exact_face_adjacency_at_100000h": adjacency,
            "new_event_family_count": 0,
            "upper_endpoint_continuation_complete": False,
        },
        "combined_typed_atlas": {
            "slab_count": 75,
            "typed_box_count": 225,
            "connected": True,
            "interior_untyped_event_cell_count": 0,
            "lower_symmetry_axis_terminal": True,
            "upper_endpoint_in_h_units": "2500000000000000",
            "upper_endpoint_terminal": False,
        },
        "audit_census": expected_census(parts),
        "strict_nonpromotion": {
            "D02_status": "BLOCKED",
            "D03_authorized": False,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": NEXT_CORE_GATE,
    }


def validate(
    result: dict[str, Any],
    parts: dict[str, dict[str, Any]],
    prior_document: dict[str, Any],
    verification_document: dict[str, Any],
) -> None:
    expected = expected_result(
        parts,
        prior_document,
        verification_document,
    )
    require(type(result) is dict, "result object")
    require(set(result) == set(expected), "result keys")
    jump = result["new_dyadic_sheared_recentering"]
    expected_jump = expected["new_dyadic_sheared_recentering"]
    require(
        type(jump) is dict and set(jump) == set(expected_jump),
        "jump keys",
    )
    require(
        type(jump["new_macro_slabs"]) is list
        and len(jump["new_macro_slabs"]) == 1,
        "one macro slab",
    )
    slab = jump["new_macro_slabs"][0]
    expected_slab = expected_jump["new_macro_slabs"][0]
    require(
        type(slab) is dict and set(slab) == set(expected_slab),
        "macro slab keys",
    )
    require(
        same(slab["u_in_h_units"], ["100000", "2500000000000000"])
        and slab["u_width_in_h_units"] == "2499999999900000"
        and type(slab["equivalent_exact_4h_slab_count"]) is int
        and slab["equivalent_exact_4h_slab_count"]
        == 624999999975000,
        "huge macro endpoints",
    )
    require(
        same(slab["coordinate_map"], expected_slab["coordinate_map"])
        and same(
            slab["w_typed_box_chain"],
            expected_slab["w_typed_box_chain"],
        )
        and same(
            slab["exact_w_face_adjacencies"],
            expected_slab["exact_w_face_adjacencies"],
        )
        and slab["w_faces_gap_free"] is True
        and slab["interior_event_cells_untyped"] == 0,
        "coordinate and typed chain",
    )
    require(
        same(slab["typed_box_audits"], parts)
        and slab["typed_box_audits_sha256"]
        == digest(slab["typed_box_audits"])
        == digest(parts),
        "independent audit reconstruction",
    )
    require(
        jump["new_macro_slabs_sha256"]
        == digest(jump["new_macro_slabs"])
        == digest(expected_jump["new_macro_slabs"]),
        "macro self digest",
    )
    require(
        same(
            jump["inherited_exact_face_adjacency_at_100000h"],
            expected_jump["inherited_exact_face_adjacency_at_100000h"],
        ),
        "slope-change seam",
    )
    require(
        same(result["audit_census"], expected_census(parts)),
        "dynamic census",
    )
    require(
        same(
            result["combined_typed_atlas"],
            expected["combined_typed_atlas"],
        )
        and result["combined_typed_atlas"]["upper_endpoint_terminal"]
        is False,
        "combined atlas",
    )
    require(
        same(
            result["strict_nonpromotion"],
            expected["strict_nonpromotion"],
        ),
        "strict nonpromotion",
    )
    require(
        result["next_core_gate"] == NEXT_CORE_GATE
        and "compact angular domain" in result["next_core_gate"]
        and "exhaust disconnected exterior sheets"
        in result["next_core_gate"],
        "next gate",
    )
    require(same(result, expected), "full canonical expected result")


def validate_document(
    document: dict[str, Any],
    parts: dict[str, dict[str, Any]],
    prior_document: dict[str, Any],
    verification_document: dict[str, Any],
) -> None:
    require(
        type(document) is dict
        and set(document) == {"schema", "result", "result_sha256"},
        "certificate keys",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(
        type(document["result_sha256"]) is str
        and document["result_sha256"] == digest(document["result"]),
        "certificate result digest",
    )
    validate(
        document["result"],
        parts,
        prior_document,
        verification_document,
    )


PathKey = str | int


def set_path(root: Any, path: tuple[PathKey, ...], value: Any) -> None:
    current = root
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = value


def result_attack_specs() -> list[tuple[str, tuple[PathKey, ...], Any]]:
    j = ("new_dyadic_sheared_recentering",)
    m = j + ("new_macro_slabs", 0)
    a = j + ("inherited_exact_face_adjacency_at_100000h",)
    o = a + ("typed_box_overlaps",)
    return [
        ("wrong_status", ("status",), "PASS"),
        ("tamper_scale", ("physical_coordinate_scale",), "h=2^-4295"),
        ("tamper_prior_result_digest",
         ("inherited_round160_result_sha256",), "0" * 64),
        ("tamper_prior_verification_digest",
         ("inherited_round160_verification_result_sha256",), "1" * 64),
        ("tamper_corridor_lower",
         ("certified_abs_delta_x_corridor_in_h_units", 0), "1"),
        ("tamper_corridor_huge_upper",
         ("certified_abs_delta_x_corridor_in_h_units", 1),
         "2500000000000001"),
        ("tamper_new_slab_count", j + ("new_typed_slab_count",), 2),
        ("tamper_new_box_count", j + ("new_typed_box_count",), 4),
        ("tamper_macro_label", m + ("label",), "invalid"),
        ("tamper_u_lower", m + ("u_in_h_units", 0), "99999"),
        ("tamper_u_upper", m + ("u_in_h_units", 1), "2500000000000001"),
        ("tamper_u_width", m + ("u_width_in_h_units",),
         "2499999999900001"),
        ("tamper_coordinate_system",
         m + ("coordinate_map", "coordinate_system"),
         "COMPACT_ANGULAR_FUNDAMENTAL_DOMAIN"),
        ("tamper_u_definition", m + ("coordinate_map", "u_definition"),
         "u=delta_x/h"),
        ("tamper_w_definition", m + ("coordinate_map", "w_definition"),
         "w=delta_beta/h+s*u"),
        ("tamper_recentered_slope", m + ("coordinate_map", "slope_s"),
         "2807/1000"),
        ("tamper_equivalent_count",
         m + ("equivalent_exact_4h_slab_count",), 624999999975001),
        ("equivalent_count_bool",
         m + ("equivalent_exact_4h_slab_count",), True),
        ("tamper_macro_box_count", m + ("typed_box_count",), 4),
        ("tamper_audit_status",
         m + ("typed_box_audits", "c24", "frontier", "status"), "FAIL"),
        ("tamper_audit_slope",
         m + ("typed_box_audits", "bridge", "full_audit", "slope_s"),
         "2807/1000"),
        ("tamper_c24_anchor_negative_proof",
         m + ("typed_box_audits", "c24", "full_audit",
              "collision3_correlated_anchor_exclusion",
              "D3_maximum_strict_negative"), False),
        ("tamper_c24_anchor_candidate",
         m + ("typed_box_audits", "c24", "full_audit",
              "collision3_correlated_anchor_exclusion",
              "anchor_candidate"), "W[1,0]"),
        ("tamper_c24_correlated_full_count",
         m + ("typed_box_audits", "c24", "full_audit",
              "collision3_correlated_candidate_audits",
              "full_radius4", "candidate_count"), 160),
        ("deny_c24_correlated_adapter_restored",
         m + ("typed_box_audits", "c24", "full_audit",
              "collision3_correlated_adapter_restored"), False),
        ("deny_runtime_restoration",
         m + ("typed_box_audits", "d3", "full_audit",
              "runtime_adapter_restored"), False),
        ("tamper_audit_digest", m + ("typed_box_audits_sha256",), "0" * 64),
        ("tamper_c24_lower_band",
         m + ("w_typed_box_chain", 0, "w_in_h_units", 0), "-431"),
        ("tamper_c24_bridge_face",
         m + ("w_typed_box_chain", 0, "w_in_h_units", 1), "-404"),
        ("tamper_bridge_d3_face",
         m + ("w_typed_box_chain", 1, "w_in_h_units", 1), "-349"),
        ("tamper_huge_d3_upper_band",
         m + ("w_typed_box_chain", 2, "w_in_h_units", 1),
         "134111000001"),
        ("tamper_first_adjacency",
         m + ("exact_w_face_adjacencies", 0,
              "shared_w_face_in_h_units"), "-404"),
        ("tamper_second_adjacency",
         m + ("exact_w_face_adjacencies", 1,
              "shared_w_face_in_h_units"), "-349"),
        ("deny_gap_free", m + ("w_faces_gap_free",), False),
        ("invent_untyped_cell", m + ("interior_event_cells_untyped",), 1),
        ("tamper_macro_digest", j + ("new_macro_slabs_sha256",), "0" * 64),
        ("tamper_shared_seam_u", a + ("shared_u_face_in_h_units",), "99999"),
        ("tamper_prior_coordinate", a + ("prior_coordinate_system",),
         "AXIS_ALIGNED_PHYSICAL_COORDINATES"),
        ("compact_domain_overclaim", a + ("new_coordinate_system",),
         "COMPACT_ANGULAR_FUNDAMENTAL_DOMAIN"),
        ("tamper_prior_slope", a + ("prior_slope_s",), "2808/1000"),
        ("tamper_new_slope", a + ("new_slope_s",), "2807/1000"),
        ("tamper_exact_slope_shift",
         a + ("new_w_equals_prior_w_plus_slope_shift_u_in_h_units",),
         "0"),
        ("deny_exact_slope_change",
         a + ("slope_change_applied_exactly",), False),
        ("deny_all_overlap",
         a + ("all_three_typed_boxes_have_strict_physical_beta_overlap",),
         False),
        ("tamper_c24_prior_w",
         o + ("C24_EVENT", "prior_w_face_in_h_units", 0), "-421"),
        ("tamper_c24_new_w",
         o + ("C24_EVENT", "new_w_face_in_h_units", 0), "-431"),
        ("tamper_bridge_prior_physical",
         o + ("STRICT_RETURN_BRIDGE",
              "prior_physical_beta_face_in_h_units", 0), "0"),
        ("tamper_bridge_new_physical",
         o + ("STRICT_RETURN_BRIDGE",
              "new_physical_beta_face_in_h_units", 0), "0"),
        ("tamper_d3_overlap",
         o + ("D3_EVENT", "strict_physical_beta_overlap_in_h_units", 0),
         "0"),
        ("invent_event_family", j + ("new_event_family_count",), 1),
        ("claim_continuation_complete",
         j + ("upper_endpoint_continuation_complete",), True),
        ("tamper_atlas_slab_count",
         ("combined_typed_atlas", "slab_count"), 76),
        ("tamper_atlas_box_count",
         ("combined_typed_atlas", "typed_box_count"), 226),
        ("disconnect_atlas",
         ("combined_typed_atlas", "connected"), False),
        ("bool_int_connected",
         ("combined_typed_atlas", "connected"), 1),
        ("int_bool_slab_count",
         ("combined_typed_atlas", "slab_count"), True),
        ("invent_atlas_untyped",
         ("combined_typed_atlas",
          "interior_untyped_event_cell_count"), 1),
        ("deny_lower_terminal",
         ("combined_typed_atlas", "lower_symmetry_axis_terminal"), False),
        ("tamper_atlas_upper",
         ("combined_typed_atlas", "upper_endpoint_in_h_units"),
         "2500000000000001"),
        ("claim_upper_terminal",
         ("combined_typed_atlas", "upper_endpoint_terminal"), True),
        ("tamper_census_pairs",
         ("audit_census", "new_collision_stage_object_pairs"), 3295),
        ("tamper_census_r1648",
         ("audit_census", "new_R1648_path_radius4_candidate_tests"),
         530655),
        ("tamper_census_d3",
         ("audit_census", "new_D3_event_box_radius4_candidate_tests"),
         482),
        ("tamper_census_total",
         ("audit_census", "new_total_radius4_candidate_tests"), 531138),
        ("close_D02", ("strict_nonpromotion", "D02_status"), "CERTIFIED"),
        ("authorize_D03", ("strict_nonpromotion", "D03_authorized"), True),
        ("promote_gate5",
         ("strict_nonpromotion", "global_gate5_maturity"), "18/18"),
        ("create_global_block",
         ("strict_nonpromotion",
          "global_complete_18_field_block_count"), 1),
        ("promote_CM2",
         ("strict_nonpromotion", "CM2"), "GO_FOR_CLAIM"),
        ("tamper_next_gate", ("next_core_gate",), "promote now"),
        ("terminal_face_overclaim", ("next_core_gate",),
         "first terminal face certified"),
    ]


def result_attacks(
    result: dict[str, Any],
    parts: dict[str, dict[str, Any]],
    prior_document: dict[str, Any],
    verification_document: dict[str, Any],
) -> list[str]:
    specs = result_attack_specs()
    rejected: list[str] = []
    for label, path, value in specs:
        candidate = copy.deepcopy(result)
        set_path(candidate, path, value)
        try:
            validate(
                candidate,
                parts,
                prior_document,
                verification_document,
            )
        except Exception:
            rejected.append(label)
    require(
        len(specs) >= 67 and rejected == [label for label, _, _ in specs],
        "result attacks",
    )
    return rejected


def rehash_macro(document: dict[str, Any]) -> None:
    jump = document["result"]["new_dyadic_sheared_recentering"]
    slab = jump["new_macro_slabs"][0]
    slab["typed_box_audits_sha256"] = digest(slab["typed_box_audits"])
    jump["new_macro_slabs_sha256"] = digest(jump["new_macro_slabs"])
    document["result_sha256"] = digest(document["result"])


def document_attacks(
    document: dict[str, Any],
    parts: dict[str, dict[str, Any]],
    prior_document: dict[str, Any],
    verification_document: dict[str, Any],
) -> list[str]:
    labels = [
        "wrapper_wrong_schema",
        "wrapper_result_digest",
        "wrapper_extra_key",
        "coherent_huge_endpoint_and_hashes",
        "coherent_recentered_slope_and_hashes",
        "coherent_huge_d3_band_and_hashes",
        "coherent_c24_anchor_proof_and_hashes",
        "coherent_typed_audit_and_hashes",
        "coherent_w_chain_and_adjacency",
        "coherent_slope_shift_seam",
        "coherent_physical_overlap",
        "coherent_census",
        "coherent_atlas",
        "coherent_corridor_and_upper",
        "coherent_inheritance",
        "coherent_nonpromotion",
        "coherent_event_completion",
        "coherent_compact_domain_overclaim",
        "coherent_terminal_overclaim",
        "coherent_type_confusion",
        "coherent_extra_result_key",
    ]
    rejected: list[str] = []
    for label in labels:
        candidate = copy.deepcopy(document)
        result = candidate["result"]
        jump = result["new_dyadic_sheared_recentering"]
        slab = jump["new_macro_slabs"][0]
        seam = jump["inherited_exact_face_adjacency_at_100000h"]
        if label == "wrapper_wrong_schema":
            candidate["schema"] = "cm2.round161.invalid"
        elif label == "wrapper_result_digest":
            candidate["result_sha256"] = "0" * 64
        elif label == "wrapper_extra_key":
            candidate["unexpected"] = True
        elif label == "coherent_huge_endpoint_and_hashes":
            slab["u_in_h_units"][1] = "2500000000000001"
            slab["u_width_in_h_units"] = "2499999999900001"
            rehash_macro(candidate)
        elif label == "coherent_recentered_slope_and_hashes":
            slab["coordinate_map"]["slope_s"] = "2807/1000"
            rehash_macro(candidate)
        elif label == "coherent_huge_d3_band_and_hashes":
            slab["w_typed_box_chain"][2]["w_in_h_units"][1] = (
                "134111000001"
            )
            rehash_macro(candidate)
        elif label == "coherent_c24_anchor_proof_and_hashes":
            slab["typed_box_audits"]["c24"]["full_audit"][
                "collision3_correlated_anchor_exclusion"
            ]["D3_maximum_strict_negative"] = False
            rehash_macro(candidate)
        elif label == "coherent_typed_audit_and_hashes":
            slab["typed_box_audits"]["d3"]["frontier"][
                "upper_w_edge_D3_strict_positive"
            ] = False
            rehash_macro(candidate)
        elif label == "coherent_w_chain_and_adjacency":
            slab["w_typed_box_chain"][0]["w_in_h_units"][1] = "-404"
            slab["w_typed_box_chain"][1]["w_in_h_units"][0] = "-404"
            slab["exact_w_face_adjacencies"][0][
                "shared_w_face_in_h_units"
            ] = "-404"
            rehash_macro(candidate)
        elif label == "coherent_slope_shift_seam":
            seam[
                "new_w_equals_prior_w_plus_slope_shift_u_in_h_units"
            ] = "0"
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_physical_overlap":
            seam["typed_box_overlaps"]["D3_EVENT"][
                "strict_physical_beta_overlap_in_h_units"
            ][0] = "0"
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_census":
            result["audit_census"][
                "new_D3_event_box_radius4_candidate_tests"
            ] -= 1
            result["audit_census"]["new_total_radius4_candidate_tests"] -= 1
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_atlas":
            result["combined_typed_atlas"]["slab_count"] += 1
            result["combined_typed_atlas"]["typed_box_count"] += 3
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_corridor_and_upper":
            result["certified_abs_delta_x_corridor_in_h_units"][1] = (
                "2500000000000001"
            )
            result["combined_typed_atlas"][
                "upper_endpoint_in_h_units"
            ] = "2500000000000001"
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_inheritance":
            result["inherited_round160_result_sha256"] = "0" * 64
            result["inherited_round160_verification_result_sha256"] = "1" * 64
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_nonpromotion":
            result["strict_nonpromotion"]["D02_status"] = "CERTIFIED"
            result["strict_nonpromotion"]["global_gate5_maturity"] = "18/18"
            result["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_event_completion":
            jump["new_event_family_count"] = 1
            jump["upper_endpoint_continuation_complete"] = True
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_compact_domain_overclaim":
            slab["coordinate_map"]["coordinate_system"] = (
                "COMPACT_ANGULAR_FUNDAMENTAL_DOMAIN"
            )
            rehash_macro(candidate)
        elif label == "coherent_terminal_overclaim":
            result["combined_typed_atlas"]["upper_endpoint_terminal"] = True
            result["next_core_gate"] = "D02 is closed"
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_type_confusion":
            result["combined_typed_atlas"]["connected"] = 1
            candidate["result_sha256"] = digest(result)
        else:
            result["unexpected"] = True
            candidate["result_sha256"] = digest(result)
        try:
            validate_document(
                candidate,
                parts,
                prior_document,
                verification_document,
            )
        except Exception:
            rejected.append(label)
    require(rejected == labels, "document attacks")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    check_pins()
    certificate = strict_load(arguments.certificate)
    prior_document, verification_document = load_prior()
    with ProcessPoolExecutor(max_workers=3) as pool:
        raw_parts = list(
            pool.map(engine.audit_part, PART_NAMES, chunksize=1)
        )
    parts = normalize(dict(zip(PART_NAMES, raw_parts, strict=True)))
    validate_document(
        certificate,
        parts,
        prior_document,
        verification_document,
    )
    rejected = result_attacks(
        certificate["result"],
        parts,
        prior_document,
        verification_document,
    )
    rejected += document_attacks(
        certificate,
        parts,
        prior_document,
        verification_document,
    )
    strict_attacks = [
        b'{"x":1,"x":2}\n',
        b"\xef\xbb\xbf{}\n",
        b"[1]\n",
        b'{"x":NaN}\n',
        b'{"x":"a\x00b"}\n',
        b'{"x":"\xff"}\n',
        b'{"x":1} trailing\n',
        b'{"x":1.0}\n',
        b'{"x":1e400}\n',
        b'{"x":"\\u0000"}\n',
        b'{"x":"\\ud800"}\n',
        b'{"x":"\\udfff"}\n',
    ]
    strict_rejected = 0
    for raw in strict_attacks:
        try:
            strict_load_raw(raw)
        except Exception:
            strict_rejected += 1
    require(strict_rejected == len(strict_attacks), "strict attacks")

    census = expected_census(parts)
    equivalent = (U1 - U0).numerator // 4
    result = {
        "status": "PASS",
        "certificate_result_sha256": certificate["result_sha256"],
        "prior_certificate_result_sha256": prior_document["result_sha256"],
        "prior_verification_result_sha256":
            verification_document["result_sha256"],
        "producer_source_sha256": PINS[PRODUCER],
        "producer_imported_or_executed": False,
        "engine_source_sha256": PINS[ENGINE],
        "engine_module_identity_checked": True,
        "new_macro_slab_reconstruction_count": 1,
        "new_typed_box_reconstruction_count": 3,
        "equivalent_exact_4h_slab_count_recomputed": equivalent,
        "huge_upper_endpoint_recomputed_in_h_units":
            engine.qstr(U1),
        "recentered_slope_recomputed":
            engine.qstr(NEW_SLOPE),
        "slope_change_seam_reconstruction_count": 3,
        "c24_collision3_correlated_anchor_exclusion_recomputed": True,
        "new_full_R1648_object_reconstruction_count": 2,
        "new_collision_stage_object_pairs_replayed": census[
            "new_collision_stage_object_pairs"
        ],
        "new_R1648_path_radius4_candidate_tests_replayed": census[
            "new_R1648_path_radius4_candidate_tests"
        ],
        "new_D3_event_box_radius4_candidate_tests_replayed": census[
            "new_D3_event_box_radius4_candidate_tests"
        ],
        "new_total_radius4_candidate_tests_replayed": census[
            "new_total_radius4_candidate_tests"
        ],
        "combined_typed_atlas_slab_count_recomputed": 75,
        "combined_typed_box_count_recomputed": 225,
        "combined_interior_untyped_event_cell_count_recomputed": 0,
        "upper_endpoint_reached_in_h_units": engine.qstr(U1),
        "w_face_adjacency_count_recomputed": 2,
        "inherited_100000h_typed_box_overlap_count_recomputed": 3,
        "semantic_mutation_rejection_labels": rejected,
        "semantic_mutation_rejection_count": len(rejected),
        "strict_json_attack_rejection_count": strict_rejected,
        "compact_angular_fundamental_domain_exhausted": False,
        "disconnected_exterior_sheets_exhausted": False,
        "D02_status": "BLOCKED",
        "D03_authorized": False,
        "global_gate5_maturity": "10/18",
        "global_complete_18_field_block_count": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    arguments.output.write_text(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )
    print(
        canonical(
            {
                "status": "PASS",
                "output": str(arguments.output),
                "result_sha256": document["result_sha256"],
            }
        )
    )


if __name__ == "__main__":
    main()
