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

import cm2_round160_sheared_scale_jump_engine as engine


HERE = Path(__file__).resolve().parent
CERTIFICATE = (
    HERE
    / "cm2-round160-sheared-macro-scale-jump-to-100000h-2026-07-25.json"
)
OUTPUT = (
    HERE
    / "cm2-round160-sheared-macro-scale-jump-to-100000h-verification-"
    "2026-07-25.json"
)
CERTIFICATE_SCHEMA = "cm2.round160.sheared-macro-scale-jump-to-100000h.v1"
SCHEMA = (
    "cm2.round160.sheared-macro-scale-jump-to-100000h.verification.v1"
)
STATUS = (
    "CERTIFIED_SHEARED_MACRO_SCALE_JUMP_TO_100000H__D02_STILL_BLOCKED"
)
PRIOR_CERTIFICATE = (
    "cm2-round159-upper-endpoint-continuation-to-352h-2026-07-25.json"
)
PRIOR_VERIFICATION = (
    "cm2-round159-upper-endpoint-continuation-to-352h-verification-"
    "2026-07-25.json"
)
PRODUCER = "cm2_round160_sheared_macro_scale_jump_to_100000h.py"
ENGINE = "cm2_round160_sheared_scale_jump_engine.py"
PINS = {
    PRODUCER:
        "dcc73eb24b893b65f6919640843fa289b849ad483ca38e3923849b12a21a901d",
    ENGINE:
        "1de1fe55020fbb7de975c4fa04cd820723e9296a4d69db493092fe9b3f579122",
    PRIOR_CERTIFICATE:
        "9af879463f5e300f07d3ec88642757c86a8cca214986eb8f1f908a511f39f142",
    PRIOR_VERIFICATION:
        "d3a787d242e2cb485955553b52e1a95c9044b8075291b981f933973bfbfac059",
}
PART_NAMES = ("c24", "bridge", "d3")
NEXT_CORE_GATE = (
    "continue beyond 100000h by dyadic sheared-slope recentering "
    "toward the first certified chart, owner, event, or terminal "
    "face; then exhaust disconnected exterior sheets on the "
    "fundamental compact angular domain"
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
        == "cm2.round159.upper-endpoint-continuation-to-352h.v1"
        and prior_document["result_sha256"]
        == digest(prior_document["result"]),
        "prior certificate wrapper",
    )
    require(
        set(verification_document) == {"schema", "result", "result_sha256"}
        and verification_document["schema"]
        == "cm2.round159.upper-endpoint-continuation-to-352h.verification.v1"
        and verification_document["result_sha256"]
        == digest(verification_document["result"])
        and verification_document["result"]["status"] == "PASS"
        and verification_document["result"]["certificate_result_sha256"]
        == prior_document["result_sha256"],
        "prior verification wrapper",
    )
    prior = prior_document["result"]
    require(
        prior["status"]
        == "CERTIFIED_TYPED_UPPER_ENDPOINT_CONTINUATION_TO_352H__D02_STILL_BLOCKED"
        and same(
            prior["certified_abs_delta_x_corridor_in_h_units"],
            ["0", "352"],
        )
        and same(
            prior["combined_typed_atlas"],
            {
                "connected": True,
                "interior_untyped_event_cell_count": 0,
                "lower_symmetry_axis_terminal": True,
                "slab_count": 73,
                "typed_box_count": 219,
                "upper_endpoint_in_h_units": "352",
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


def expected_inherited_adjacency(
    prior: dict[str, Any],
    specifications: dict[str, dict[str, str]],
) -> dict[str, Any]:
    previous = prior["new_upper_continuation"]["new_rows"][-1]
    require(
        same(previous["abs_delta_x_in_h_units"], ["348", "352"]),
        "prior terminal slab",
    )
    prior_faces = {
        "C24_EVENT": previous["c24_frontier"][
            "delta_beta_event_box_in_h_units"
        ],
        "STRICT_RETURN_BRIDGE": previous["strict_return_bridge"][
            "delta_beta_in_h_units"
        ],
        "D3_EVENT": previous["d3_frontier"][
            "delta_beta_event_box_in_h_units"
        ],
    }
    spec_for_kind = {
        "C24_EVENT": specifications["c24"],
        "STRICT_RETURN_BRIDGE": specifications["bridge"],
        "D3_EVENT": specifications["d3"],
    }
    records: dict[str, Any] = {}
    for kind in ("C24_EVENT", "STRICT_RETURN_BRIDGE", "D3_EVENT"):
        macro_face = engine.physical_beta_face(spec_for_kind[kind], Q(352))
        records[kind] = {
            "prior_beta_face_in_h_units": prior_faces[kind],
            "macro_beta_face_in_h_units": macro_face,
            "strict_beta_overlap_in_h_units": overlap(
                prior_faces[kind],
                macro_face,
            ),
        }
    return {
        "shared_u_face_in_h_units": "352",
        "prior_coordinate_system": "AXIS_ALIGNED_PHYSICAL_COORDINATES",
        "macro_coordinate_system": "SHEARED_COMPACT_ANGLE_LIFT",
        "all_three_typed_boxes_have_strict_physical_beta_overlap": True,
        "typed_box_overlaps": records,
    }


def validate_parts(
    parts: dict[str, dict[str, Any]],
    specifications: dict[str, dict[str, str]],
) -> None:
    require(type(parts) is dict and set(parts) == set(PART_NAMES), "part names")
    require(
        set(parts["c24"]) == {"frontier", "full_audit"}
        and set(parts["bridge"]) == {"full_audit"}
        and set(parts["d3"]) == {"frontier", "full_audit"},
        "part wrappers",
    )
    records = (
        (parts["c24"]["frontier"], specifications["c24"], False),
        (parts["c24"]["full_audit"], specifications["c24"], True),
        (parts["bridge"]["full_audit"], specifications["bridge"], True),
        (parts["d3"]["frontier"], specifications["d3"], False),
        (parts["d3"]["full_audit"], specifications["d3"], True),
    )
    for record, specification, full in records:
        require(
            type(record) is dict
            and record["status"] == "PASS"
            and same(
                record["u_in_h_units"],
                [
                    specification["u_lower_h"],
                    specification["u_upper_h"],
                ],
            )
            and same(
                record["w_in_h_units"],
                [
                    specification["w_lower_h"],
                    specification["w_upper_h"],
                ],
            )
            and record["slope_s"]
            == specification["slope_beta_per_abs_x"],
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
    integer_fields = (
        (c24, "full_radius4_candidate_test_count"),
        (bridge, "full_radius4_candidate_test_count"),
        (d3, "fully_audited_prefix_radius4_candidate_test_count"),
        (d3, "collision3_full_radius4_candidate_test_count"),
    )
    require(
        all(
            type(record[field]) is int and record[field] >= 0
            for record, field in integer_fields
        ),
        "candidate census integer types",
    )


def expected_census(parts: dict[str, dict[str, Any]]) -> dict[str, int]:
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


def specifications() -> dict[str, dict[str, str]]:
    result = engine.specs()
    require(
        set(result) == set(PART_NAMES)
        and all(
            set(result[name])
            == {
                "kind",
                "u_lower_h",
                "u_upper_h",
                "slope_beta_per_abs_x",
                "w_lower_h",
                "w_upper_h",
            }
            for name in PART_NAMES
        )
        and all(
            type(value) is str
            for specification in result.values()
            for value in specification.values()
        ),
        "specification schema",
    )
    require(
        same(
            result,
            {
                "c24": {
                    "kind": "C24_EVENT",
                    "u_lower_h": "352",
                    "u_upper_h": "100000",
                    "slope_beta_per_abs_x": "2807/1000",
                    "w_lower_h": "-420",
                    "w_upper_h": "-405",
                },
                "bridge": {
                    "kind": "STRICT_RETURN_BRIDGE",
                    "u_lower_h": "352",
                    "u_upper_h": "100000",
                    "slope_beta_per_abs_x": "2807/1000",
                    "w_lower_h": "-405",
                    "w_upper_h": "-10",
                },
                "d3": {
                    "kind": "D3_EVENT",
                    "u_lower_h": "352",
                    "u_upper_h": "100000",
                    "slope_beta_per_abs_x": "2807/1000",
                    "w_lower_h": "-10",
                    "w_upper_h": "10",
                },
            },
        ),
        "fixed sheared macro specification",
    )
    return result


def expected_result(
    parts: dict[str, dict[str, Any]],
    prior_document: dict[str, Any],
    verification_document: dict[str, Any],
) -> dict[str, Any]:
    specs = specifications()
    validate_parts(parts, specs)
    u0 = Q(specs["c24"]["u_lower_h"])
    u1 = Q(specs["c24"]["u_upper_h"])
    width = u1 - u0
    require(
        u0 == 352
        and u1 == 100000
        and width == 99648
        and width.denominator == 1
        and width.numerator % 4 == 0,
        "macro endpoint arithmetic",
    )
    equivalent_4h_slabs = width.numerator // 4
    require(equivalent_4h_slabs == 24912, "equivalent 4h slab arithmetic")

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
        "label": "sheared-macro-352-to-100000",
        "u_in_h_units": [engine.qstr(u0), engine.qstr(u1)],
        "u_width_in_h_units": engine.qstr(width),
        "coordinate_map": {
            "coordinate_system": "SHEARED_COMPACT_ANGLE_LIFT",
            "u_definition": "u=abs(delta_x)/h=-delta_x/h",
            "w_definition": "w=delta_beta/h-s*u",
            "slope_s": specs["c24"]["slope_beta_per_abs_x"],
        },
        "equivalent_exact_4h_slab_count": equivalent_4h_slabs,
        "typed_box_count": len(w_chain),
        "typed_box_audits": parts,
        "typed_box_audits_sha256": digest(parts),
        "w_typed_box_chain": w_chain,
        "exact_w_face_adjacencies": [
            {
                "left_kind": w_chain[0]["kind"],
                "right_kind": w_chain[1]["kind"],
                "shared_w_face_in_h_units": w_chain[0][
                    "w_in_h_units"
                ][1],
            },
            {
                "left_kind": w_chain[1]["kind"],
                "right_kind": w_chain[2]["kind"],
                "shared_w_face_in_h_units": w_chain[1][
                    "w_in_h_units"
                ][1],
            },
        ],
        "w_faces_gap_free": True,
        "interior_event_cells_untyped": 0,
    }
    prior = prior_document["result"]
    prior_atlas = prior["combined_typed_atlas"]
    return {
        "status": STATUS,
        "physical_coordinate_scale": "h=2^-4296",
        "inherited_round159_result_sha256": prior_document["result_sha256"],
        "inherited_round159_verification_result_sha256":
            verification_document["result_sha256"],
        "certified_abs_delta_x_corridor_in_h_units": ["0", "100000"],
        "new_sheared_macro_scale_jump": {
            "new_typed_slab_count": 1,
            "new_typed_box_count": len(w_chain),
            "new_macro_slabs": [macro_slab],
            "new_macro_slabs_sha256": digest([macro_slab]),
            "inherited_exact_face_adjacency_at_352h":
                expected_inherited_adjacency(prior, specs),
            "new_event_family_count": 0,
            "upper_endpoint_continuation_complete": False,
        },
        "combined_typed_atlas": {
            "slab_count": prior_atlas["slab_count"] + 1,
            "typed_box_count": prior_atlas["typed_box_count"] + len(w_chain),
            "connected": True,
            "interior_untyped_event_cell_count": 0,
            "lower_symmetry_axis_terminal": True,
            "upper_endpoint_in_h_units": "100000",
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
    require(
        type(result) is dict
        and set(result)
        == {
            "status",
            "physical_coordinate_scale",
            "inherited_round159_result_sha256",
            "inherited_round159_verification_result_sha256",
            "certified_abs_delta_x_corridor_in_h_units",
            "new_sheared_macro_scale_jump",
            "combined_typed_atlas",
            "audit_census",
            "strict_nonpromotion",
            "next_core_gate",
        },
        "result keys",
    )
    specs = specifications()
    validate_parts(parts, specs)
    expected = expected_result(
        parts,
        prior_document,
        verification_document,
    )
    jump = result["new_sheared_macro_scale_jump"]
    require(
        type(jump) is dict
        and set(jump)
        == {
            "new_typed_slab_count",
            "new_typed_box_count",
            "new_macro_slabs",
            "new_macro_slabs_sha256",
            "inherited_exact_face_adjacency_at_352h",
            "new_event_family_count",
            "upper_endpoint_continuation_complete",
        },
        "macro jump keys",
    )
    require(
        type(jump["new_macro_slabs"]) is list
        and len(jump["new_macro_slabs"]) == 1,
        "one macro slab",
    )
    slab = jump["new_macro_slabs"][0]
    require(
        type(slab) is dict
        and set(slab)
        == {
            "label",
            "u_in_h_units",
            "u_width_in_h_units",
            "coordinate_map",
            "equivalent_exact_4h_slab_count",
            "typed_box_count",
            "typed_box_audits",
            "typed_box_audits_sha256",
            "w_typed_box_chain",
            "exact_w_face_adjacencies",
            "w_faces_gap_free",
            "interior_event_cells_untyped",
        },
        "macro slab keys",
    )
    require(
        same(slab["u_in_h_units"], ["352", "100000"])
        and slab["u_width_in_h_units"] == engine.qstr(Q(100000) - Q(352))
        and type(slab["equivalent_exact_4h_slab_count"]) is int
        and slab["equivalent_exact_4h_slab_count"]
        == (100000 - 352) // 4
        == 24912,
        "macro endpoints and 4h equivalence",
    )
    require(
        same(
            slab["coordinate_map"],
            {
                "coordinate_system": "SHEARED_COMPACT_ANGLE_LIFT",
                "u_definition": "u=abs(delta_x)/h=-delta_x/h",
                "w_definition": "w=delta_beta/h-s*u",
                "slope_s": "2807/1000",
            },
        ),
        "coordinate map",
    )
    expected_chain = expected["new_sheared_macro_scale_jump"][
        "new_macro_slabs"
    ][0]["w_typed_box_chain"]
    require(
        same(slab["w_typed_box_chain"], expected_chain)
        and slab["w_faces_gap_free"] is True
        and same(
            slab["exact_w_face_adjacencies"],
            expected["new_sheared_macro_scale_jump"]["new_macro_slabs"][0][
                "exact_w_face_adjacencies"
            ],
        ),
        "gap-free w faces",
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
        == digest(
            expected["new_sheared_macro_scale_jump"]["new_macro_slabs"]
        ),
        "macro slab self digest",
    )
    require(
        same(
            jump["inherited_exact_face_adjacency_at_352h"],
            expected["new_sheared_macro_scale_jump"][
                "inherited_exact_face_adjacency_at_352h"
            ],
        ),
        "inherited 352h physical beta overlaps",
    )
    require(
        same(
            result["combined_typed_atlas"],
            {
                "slab_count": 74,
                "typed_box_count": 222,
                "connected": True,
                "interior_untyped_event_cell_count": 0,
                "lower_symmetry_axis_terminal": True,
                "upper_endpoint_in_h_units": "100000",
                "upper_endpoint_terminal": False,
            },
        ),
        "combined atlas",
    )
    require(
        same(result["audit_census"], expected_census(parts)),
        "dynamic audit census",
    )
    require(
        same(
            result["strict_nonpromotion"],
            {
                "D02_status": "BLOCKED",
                "D03_authorized": False,
                "global_gate5_maturity": "10/18",
                "global_complete_18_field_block_count": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
        ),
        "strict nonpromotion",
    )
    require(
        result["status"] == STATUS
        and result["physical_coordinate_scale"] == "h=2^-4296"
        and same(
            result["certified_abs_delta_x_corridor_in_h_units"],
            ["0", "100000"],
        )
        and result["next_core_gate"] == NEXT_CORE_GATE,
        "fixed certificate semantics",
    )
    require(
        result["inherited_round159_result_sha256"]
        == prior_document["result_sha256"]
        and result["inherited_round159_verification_result_sha256"]
        == verification_document["result_sha256"],
        "inherited result digests",
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


def result_attacks(
    result: dict[str, Any],
    parts: dict[str, dict[str, Any]],
    prior_document: dict[str, Any],
    verification_document: dict[str, Any],
) -> list[str]:
    labels = [
        "wrong_status",
        "tamper_scale",
        "tamper_prior_result_digest",
        "tamper_prior_verification_digest",
        "tamper_corridor_lower",
        "tamper_corridor_upper",
        "tamper_new_slab_count",
        "tamper_new_box_count",
        "delete_macro_slab",
        "tamper_macro_label",
        "tamper_u_lower",
        "tamper_u_upper",
        "tamper_u_width",
        "tamper_slope",
        "tamper_w_definition",
        "tamper_equivalent_4h_count",
        "tamper_macro_box_count",
        "tamper_typed_audit",
        "tamper_typed_audit_digest",
        "tamper_c24_w_face",
        "tamper_bridge_w_face",
        "tamper_exact_w_adjacency",
        "deny_gap_free",
        "invent_untyped_macro_cell",
        "tamper_macro_slabs_digest",
        "tamper_shared_352_face",
        "tamper_prior_beta_face",
        "tamper_macro_beta_face",
        "tamper_strict_overlap",
        "deny_all_three_overlap",
        "invent_event_family",
        "claim_continuation_complete",
        "tamper_atlas_slab_count",
        "tamper_atlas_box_count",
        "disconnect_atlas",
        "invent_atlas_untyped_cell",
        "deny_lower_terminal",
        "tamper_upper_endpoint",
        "claim_upper_terminal",
        "tamper_census_component",
        "tamper_census_total",
        "deny_runtime_adapter_restored",
        "bool_int_type_confusion",
        "int_bool_type_confusion",
        "close_D02",
        "authorize_D03",
        "promote_gate5",
        "create_global_block",
        "promote_CM2",
        "tamper_next_gate",
        "extra_result_field",
    ]
    rejected: list[str] = []
    for label in labels:
        candidate = copy.deepcopy(result)
        jump = candidate["new_sheared_macro_scale_jump"]
        slab = jump["new_macro_slabs"][0]
        if label == "wrong_status":
            candidate["status"] = "PASS"
        elif label == "tamper_scale":
            candidate["physical_coordinate_scale"] = "h=2^-4295"
        elif label == "tamper_prior_result_digest":
            candidate["inherited_round159_result_sha256"] = "0" * 64
        elif label == "tamper_prior_verification_digest":
            candidate[
                "inherited_round159_verification_result_sha256"
            ] = "0" * 64
        elif label == "tamper_corridor_lower":
            candidate["certified_abs_delta_x_corridor_in_h_units"][0] = "1"
        elif label == "tamper_corridor_upper":
            candidate["certified_abs_delta_x_corridor_in_h_units"][1] = "99999"
        elif label == "tamper_new_slab_count":
            jump["new_typed_slab_count"] = 2
        elif label == "tamper_new_box_count":
            jump["new_typed_box_count"] = 4
        elif label == "delete_macro_slab":
            jump["new_macro_slabs"].clear()
        elif label == "tamper_macro_label":
            slab["label"] = "sheared-macro-352-to-99999"
        elif label == "tamper_u_lower":
            slab["u_in_h_units"][0] = "351"
        elif label == "tamper_u_upper":
            slab["u_in_h_units"][1] = "100001"
        elif label == "tamper_u_width":
            slab["u_width_in_h_units"] = "99649"
        elif label == "tamper_slope":
            slab["coordinate_map"]["slope_s"] = "2808/1000"
        elif label == "tamper_w_definition":
            slab["coordinate_map"]["w_definition"] = "w=delta_beta/h+s*u"
        elif label == "tamper_equivalent_4h_count":
            slab["equivalent_exact_4h_slab_count"] = 24913
        elif label == "tamper_macro_box_count":
            slab["typed_box_count"] = 4
        elif label == "tamper_typed_audit":
            slab["typed_box_audits"]["c24"]["frontier"]["status"] = "FAIL"
        elif label == "tamper_typed_audit_digest":
            slab["typed_box_audits_sha256"] = "0" * 64
        elif label == "tamper_c24_w_face":
            slab["w_typed_box_chain"][0]["w_in_h_units"][1] = "-404"
        elif label == "tamper_bridge_w_face":
            slab["w_typed_box_chain"][1]["w_in_h_units"][1] = "-9"
        elif label == "tamper_exact_w_adjacency":
            slab["exact_w_face_adjacencies"][0][
                "shared_w_face_in_h_units"
            ] = "-404"
        elif label == "deny_gap_free":
            slab["w_faces_gap_free"] = False
        elif label == "invent_untyped_macro_cell":
            slab["interior_event_cells_untyped"] = 1
        elif label == "tamper_macro_slabs_digest":
            jump["new_macro_slabs_sha256"] = "0" * 64
        elif label == "tamper_shared_352_face":
            jump["inherited_exact_face_adjacency_at_352h"][
                "shared_u_face_in_h_units"
            ] = "353"
        elif label == "tamper_prior_beta_face":
            jump["inherited_exact_face_adjacency_at_352h"][
                "typed_box_overlaps"
            ]["C24_EVENT"]["prior_beta_face_in_h_units"][0] = "0"
        elif label == "tamper_macro_beta_face":
            jump["inherited_exact_face_adjacency_at_352h"][
                "typed_box_overlaps"
            ]["STRICT_RETURN_BRIDGE"]["macro_beta_face_in_h_units"][0] = "0"
        elif label == "tamper_strict_overlap":
            jump["inherited_exact_face_adjacency_at_352h"][
                "typed_box_overlaps"
            ]["D3_EVENT"]["strict_beta_overlap_in_h_units"][0] = "0"
        elif label == "deny_all_three_overlap":
            jump["inherited_exact_face_adjacency_at_352h"][
                "all_three_typed_boxes_have_strict_physical_beta_overlap"
            ] = False
        elif label == "invent_event_family":
            jump["new_event_family_count"] = 1
        elif label == "claim_continuation_complete":
            jump["upper_endpoint_continuation_complete"] = True
        elif label == "tamper_atlas_slab_count":
            candidate["combined_typed_atlas"]["slab_count"] = 75
        elif label == "tamper_atlas_box_count":
            candidate["combined_typed_atlas"]["typed_box_count"] = 223
        elif label == "disconnect_atlas":
            candidate["combined_typed_atlas"]["connected"] = False
        elif label == "invent_atlas_untyped_cell":
            candidate["combined_typed_atlas"][
                "interior_untyped_event_cell_count"
            ] = 1
        elif label == "deny_lower_terminal":
            candidate["combined_typed_atlas"][
                "lower_symmetry_axis_terminal"
            ] = False
        elif label == "tamper_upper_endpoint":
            candidate["combined_typed_atlas"][
                "upper_endpoint_in_h_units"
            ] = "99999"
        elif label == "claim_upper_terminal":
            candidate["combined_typed_atlas"]["upper_endpoint_terminal"] = True
        elif label == "tamper_census_component":
            candidate["audit_census"][
                "new_R1648_path_radius4_candidate_tests"
            ] -= 1
        elif label == "tamper_census_total":
            candidate["audit_census"]["new_total_radius4_candidate_tests"] -= 1
        elif label == "deny_runtime_adapter_restored":
            slab["typed_box_audits"]["bridge"]["full_audit"][
                "runtime_adapter_restored"
            ] = False
        elif label == "bool_int_type_confusion":
            candidate["combined_typed_atlas"]["connected"] = 1
        elif label == "int_bool_type_confusion":
            candidate["combined_typed_atlas"]["slab_count"] = True
        elif label == "close_D02":
            candidate["strict_nonpromotion"]["D02_status"] = "CERTIFIED"
        elif label == "authorize_D03":
            candidate["strict_nonpromotion"]["D03_authorized"] = True
        elif label == "promote_gate5":
            candidate["strict_nonpromotion"]["global_gate5_maturity"] = "18/18"
        elif label == "create_global_block":
            candidate["strict_nonpromotion"][
                "global_complete_18_field_block_count"
            ] = 1
        elif label == "promote_CM2":
            candidate["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
        elif label == "tamper_next_gate":
            candidate["next_core_gate"] = "promote now"
        else:
            candidate["unexpected"] = True
        try:
            validate(
                candidate,
                parts,
                prior_document,
                verification_document,
            )
        except Exception:
            rejected.append(label)
    require(rejected == labels, "result attacks")
    return rejected


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
        "coherent_slope_and_hashes",
        "coherent_typed_audit_and_hashes",
        "coherent_macro_list_digest",
        "coherent_w_chain_and_adjacency",
        "coherent_overlap_and_result_digest",
        "coherent_census_components_and_total",
        "coherent_atlas_counts",
        "coherent_corridor_and_upper_endpoint",
        "coherent_runtime_adapter_and_hashes",
        "coherent_inheritance",
        "coherent_nonpromotion",
        "coherent_event_and_completion",
        "coherent_result_type_confusion",
    ]
    rejected: list[str] = []
    for label in labels:
        candidate = copy.deepcopy(document)
        result = candidate["result"]
        jump = result["new_sheared_macro_scale_jump"]
        slab = jump["new_macro_slabs"][0]
        if label == "wrapper_wrong_schema":
            candidate["schema"] = "cm2.round160.invalid"
        elif label == "wrapper_result_digest":
            candidate["result_sha256"] = "0" * 64
        elif label == "wrapper_extra_key":
            candidate["unexpected"] = True
        elif label == "coherent_slope_and_hashes":
            slab["coordinate_map"]["slope_s"] = "2808/1000"
            jump["new_macro_slabs_sha256"] = digest(jump["new_macro_slabs"])
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_typed_audit_and_hashes":
            slab["typed_box_audits"]["d3"]["frontier"][
                "upper_w_edge_D3_strict_positive"
            ] = False
            slab["typed_box_audits_sha256"] = digest(
                slab["typed_box_audits"]
            )
            jump["new_macro_slabs_sha256"] = digest(jump["new_macro_slabs"])
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_macro_list_digest":
            slab["u_width_in_h_units"] = "99649"
            jump["new_macro_slabs_sha256"] = digest(jump["new_macro_slabs"])
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_w_chain_and_adjacency":
            slab["w_typed_box_chain"][0]["w_in_h_units"][1] = "-404"
            slab["w_typed_box_chain"][1]["w_in_h_units"][0] = "-404"
            slab["exact_w_face_adjacencies"][0][
                "shared_w_face_in_h_units"
            ] = "-404"
            jump["new_macro_slabs_sha256"] = digest(jump["new_macro_slabs"])
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_overlap_and_result_digest":
            jump["inherited_exact_face_adjacency_at_352h"][
                "typed_box_overlaps"
            ]["C24_EVENT"]["strict_beta_overlap_in_h_units"][0] = "569"
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_census_components_and_total":
            result["audit_census"][
                "new_R1648_path_radius4_candidate_tests"
            ] -= 1
            result["audit_census"]["new_total_radius4_candidate_tests"] -= 1
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_atlas_counts":
            result["combined_typed_atlas"]["slab_count"] += 1
            result["combined_typed_atlas"]["typed_box_count"] += 3
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_corridor_and_upper_endpoint":
            result["certified_abs_delta_x_corridor_in_h_units"][1] = "99999"
            result["combined_typed_atlas"][
                "upper_endpoint_in_h_units"
            ] = "99999"
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_runtime_adapter_and_hashes":
            slab["typed_box_audits"]["c24"]["full_audit"][
                "runtime_adapter_restored"
            ] = False
            slab["typed_box_audits_sha256"] = digest(
                slab["typed_box_audits"]
            )
            jump["new_macro_slabs_sha256"] = digest(jump["new_macro_slabs"])
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_inheritance":
            result["inherited_round159_result_sha256"] = "0" * 64
            result["inherited_round159_verification_result_sha256"] = "1" * 64
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_nonpromotion":
            result["strict_nonpromotion"]["D02_status"] = "CERTIFIED"
            result["strict_nonpromotion"]["global_gate5_maturity"] = "18/18"
            result["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
            candidate["result_sha256"] = digest(result)
        elif label == "coherent_event_and_completion":
            jump["new_event_family_count"] = 1
            jump["upper_endpoint_continuation_complete"] = True
            candidate["result_sha256"] = digest(result)
        else:
            result["combined_typed_atlas"]["connected"] = 1
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
        "equivalent_exact_4h_slab_count_recomputed": 24912,
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
        "combined_typed_atlas_slab_count_recomputed": 74,
        "combined_typed_box_count_recomputed": 222,
        "combined_interior_untyped_event_cell_count_recomputed": 0,
        "upper_endpoint_reached_in_h_units": "100000",
        "w_face_adjacency_count_recomputed": 2,
        "inherited_352h_typed_box_overlap_count_recomputed": 3,
        "semantic_mutation_rejection_labels": rejected,
        "semantic_mutation_rejection_count": len(rejected),
        "strict_json_attack_rejection_count": strict_rejected,
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
