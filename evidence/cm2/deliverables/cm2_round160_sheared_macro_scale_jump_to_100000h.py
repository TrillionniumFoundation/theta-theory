#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_round160_sheared_scale_jump_engine as engine


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2-round160-sheared-macro-scale-jump-to-100000h-2026-07-25.json"
)
SCHEMA = "cm2.round160.sheared-macro-scale-jump-to-100000h.v1"
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
PINS = {
    "cm2_round160_sheared_scale_jump_engine.py":
        "1de1fe55020fbb7de975c4fa04cd820723e9296a4d69db493092fe9b3f579122",
    PRIOR_CERTIFICATE:
        "9af879463f5e300f07d3ec88642757c86a8cca214986eb8f1f908a511f39f142",
    PRIOR_VERIFICATION:
        "d3a787d242e2cb485955553b52e1a95c9044b8075291b981f933973bfbfac059",
}
PART_NAMES = ("c24", "bridge", "d3")


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


def strict_load(path: Path) -> dict[str, Any]:
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

    raw = path.read_bytes()
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


def check_pins() -> tuple[dict[str, Any], dict[str, Any]]:
    require(
        Path(engine.__file__).resolve()
        == (HERE / "cm2_round160_sheared_scale_jump_engine.py").resolve(),
        "engine module identity",
    )
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
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
        and prior["certified_abs_delta_x_corridor_in_h_units"] == ["0", "352"]
        and prior["combined_typed_atlas"]
        == {
            "connected": True,
            "interior_untyped_event_cell_count": 0,
            "lower_symmetry_axis_terminal": True,
            "slab_count": 73,
            "typed_box_count": 219,
            "upper_endpoint_in_h_units": "352",
            "upper_endpoint_terminal": False,
        }
        and prior["strict_nonpromotion"]
        == {
            "D02_status": "BLOCKED",
            "D03_authorized": False,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "prior strict state",
    )
    return prior_document, verification_document


def overlap(
    prior_face: list[str],
    macro_face: list[str],
) -> list[str]:
    require(
        type(prior_face) is list
        and type(macro_face) is list
        and len(prior_face) == len(macro_face) == 2
        and all(type(value) is str for value in prior_face + macro_face),
        "face schema",
    )
    lower = max(Q(prior_face[0]), Q(macro_face[0]))
    upper = min(Q(prior_face[1]), Q(macro_face[1]))
    require(lower < upper, "strict inherited beta overlap")
    return [engine.qstr(lower), engine.qstr(upper)]


def inherited_face_adjacency(
    prior: dict[str, Any],
    specifications: dict[str, dict[str, str]],
) -> dict[str, Any]:
    previous = prior["new_upper_continuation"]["new_rows"][-1]
    require(
        previous["abs_delta_x_in_h_units"] == ["348", "352"],
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
        macro_face = engine.physical_beta_face(
            spec_for_kind[kind],
            Q(352),
        )
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
    require(set(parts) == set(PART_NAMES), "audit part names")
    require(
        set(parts["c24"]) == {"frontier", "full_audit"}
        and set(parts["bridge"]) == {"full_audit"}
        and set(parts["d3"]) == {"frontier", "full_audit"},
        "audit part wrappers",
    )
    records = (
        (parts["c24"]["frontier"], specifications["c24"], False),
        (parts["c24"]["full_audit"], specifications["c24"], True),
        (parts["bridge"]["full_audit"], specifications["bridge"], True),
        (parts["d3"]["frontier"], specifications["d3"], False),
        (parts["d3"]["full_audit"], specifications["d3"], True),
    )
    for record, spec, full in records:
        require(
            record["status"] == "PASS"
            and record["u_in_h_units"]
            == [spec["u_lower_h"], spec["u_upper_h"]]
            and record["w_in_h_units"]
            == [spec["w_lower_h"], spec["w_upper_h"]]
            and record["slope_s"] == spec["slope_beta_per_abs_x"],
            "audit coordinate identity",
        )
        if full:
            require(
                record["runtime_adapter_restored"] is True,
                "runtime adapter restoration",
            )
    require(
        parts["c24"]["frontier"]["event_kind"]
        == "COLLISION1648_TERMINAL_C24_P0_ZERO"
        and parts["c24"]["full_audit"]["collision_count"] == 1648
        and parts["bridge"]["full_audit"]["collision_count"] == 1648
        and parts["bridge"]["full_audit"]["terminal_classification"]
        == "RETURN_AT_3_INNER"
        and parts["d3"]["frontier"]["event_kind"]
        == "COLLISION3_D0_TANGENCY_D3_ZERO",
        "typed audit semantics",
    )


def census(parts: dict[str, dict[str, Any]]) -> dict[str, int]:
    c24 = parts["c24"]["full_audit"]
    bridge = parts["bridge"]["full_audit"]
    d3 = parts["d3"]["full_audit"]
    integer_fields = (
        (c24, "collision_count"),
        (c24, "full_radius4_candidate_test_count"),
        (bridge, "collision_count"),
        (bridge, "full_radius4_candidate_test_count"),
        (d3, "fully_audited_prefix_radius4_candidate_test_count"),
        (d3, "collision3_full_radius4_candidate_test_count"),
    )
    require(
        all(
            type(record[field]) is int and record[field] >= 0
            for record, field in integer_fields
        ),
        "audit census integer fields",
    )
    r1648_tests = (
        c24["full_radius4_candidate_test_count"]
        + bridge["full_radius4_candidate_test_count"]
    )
    d3_tests = (
        d3["fully_audited_prefix_radius4_candidate_test_count"]
        + d3["collision3_full_radius4_candidate_test_count"]
    )
    return {
        "new_full_R1648_C24_audits": int(c24["status"] == "PASS"),
        "new_full_R1648_bridge_audits": int(bridge["status"] == "PASS"),
        "new_collision_stage_object_pairs":
            c24["collision_count"] + bridge["collision_count"],
        "new_R1648_path_radius4_candidate_tests": r1648_tests,
        "new_full_D3_event_box_audits": int(d3["status"] == "PASS"),
        "new_D3_event_box_radius4_candidate_tests": d3_tests,
        "new_total_radius4_candidate_tests": r1648_tests + d3_tests,
    }


def build_result() -> dict[str, Any]:
    prior_document, verification_document = check_pins()
    specifications = engine.specs()
    require(
        set(specifications) == set(PART_NAMES)
        and specifications["c24"]["u_lower_h"]
        == specifications["bridge"]["u_lower_h"]
        == specifications["d3"]["u_lower_h"]
        == "352"
        and specifications["c24"]["u_upper_h"]
        == specifications["bridge"]["u_upper_h"]
        == specifications["d3"]["u_upper_h"]
        == "100000",
        "macro slab domain",
    )
    with ProcessPoolExecutor(max_workers=3) as pool:
        raw_parts = list(
            pool.map(engine.audit_part, PART_NAMES, chunksize=1)
        )
    parts = normalize(dict(zip(PART_NAMES, raw_parts, strict=True)))
    validate_parts(parts, specifications)

    w_chain = [
        {
            "kind": specifications[name]["kind"],
            "w_in_h_units": [
                specifications[name]["w_lower_h"],
                specifications[name]["w_upper_h"],
            ],
        }
        for name in PART_NAMES
    ]
    require(
        w_chain[0]["w_in_h_units"][1] == w_chain[1]["w_in_h_units"][0]
        and w_chain[1]["w_in_h_units"][1]
        == w_chain[2]["w_in_h_units"][0],
        "gap-free w faces",
    )
    u0 = Q(specifications["c24"]["u_lower_h"])
    u1 = Q(specifications["c24"]["u_upper_h"])
    width = u1 - u0
    require(
        width.denominator == 1
        and width.numerator % 4 == 0,
        "4h equivalent width",
    )
    equivalent_4h_slabs = width.numerator // 4
    prior = prior_document["result"]
    adjacency = inherited_face_adjacency(prior, specifications)
    macro_slab = {
        "label": "sheared-macro-352-to-100000",
        "u_in_h_units": [engine.qstr(u0), engine.qstr(u1)],
        "u_width_in_h_units": engine.qstr(width),
        "coordinate_map": {
            "coordinate_system": "SHEARED_COMPACT_ANGLE_LIFT",
            "u_definition": "u=abs(delta_x)/h=-delta_x/h",
            "w_definition": "w=delta_beta/h-s*u",
            "slope_s": specifications["c24"][
                "slope_beta_per_abs_x"
            ],
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
    prior_atlas = prior["combined_typed_atlas"]
    audit_census = census(parts)
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
            "inherited_exact_face_adjacency_at_352h": adjacency,
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
        "audit_census": audit_census,
        "strict_nonpromotion": {
            "D02_status": "BLOCKED",
            "D03_authorized": False,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "continue beyond 100000h by dyadic sheared-slope recentering "
            "toward the first certified chart, owner, event, or terminal "
            "face; then exhaust disconnected exterior sheets on the "
            "fundamental compact angular domain"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    result = build_result()
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
