#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from pathlib import Path

import cm2_round151_dual_boundary_event_census_engine as boundary_engine
import cm2_round152_open_strip_bridge_engine as bridge_engine


HERE = Path(__file__).resolve().parent
CERTIFICATE = (
    HERE / "cm2-round159-upper-endpoint-continuation-to-352h-2026-07-25.json"
)
OUTPUT = (
    HERE
    / "cm2-round159-upper-endpoint-continuation-to-352h-verification-2026-07-25.json"
)
CERTIFICATE_SCHEMA = "cm2.round159.upper-endpoint-continuation-to-352h.v1"
SCHEMA = "cm2.round159.upper-endpoint-continuation-to-352h.verification.v1"
STATUS = "CERTIFIED_TYPED_UPPER_ENDPOINT_CONTINUATION_TO_352H__D02_STILL_BLOCKED"
PINS = {
    "cm2_round151_dual_boundary_event_census_engine.py": "dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085",
    "cm2_round152_open_strip_bridge_engine.py": "21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738",
    "cm2_round159_upper_endpoint_continuation_to_352h.py": "0f09860ba205110c99aed379fc7e1b5349c005635644737a5bc9fe903ee4bda9",
    "cm2-round158-upper-endpoint-continuation-to-320h-2026-07-25.json": "9b7196d43f608a1a83f9eb98116fa8a3f7b4c41e3bc89fee2724f51dcecf53c6",
    "cm2-round158-upper-endpoint-continuation-to-320h-verification-2026-07-25.json": "5c814d68f68732a527fd769db773a955f3281fc733d88fd585ffac249f03fd9b",
}
SLABS = [
    ("upper-44", "320", "324", "465", "517", "888", "914"),
    ("upper-45", "324", "328", "476", "528", "899", "925"),
    ("upper-46", "328", "332", "487", "539", "910", "936"),
    ("upper-47", "332", "336", "498", "550", "921", "947"),
    ("upper-48", "336", "340", "509", "561", "932", "958"),
    ("upper-49", "340", "344", "520", "572", "943", "969"),
    ("upper-50", "344", "348", "531", "583", "954", "980"),
    ("upper-51", "348", "352", "542", "594", "965", "991"),
]


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def normalize(value):
    return json.loads(canonical(value))


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def same(actual, expected):
    return canonical(actual) == canonical(expected)


def strict_load_raw(raw):
    def reject(value):
        raise ValueError(value)

    def reject_float(value):
        raise ValueError(value)

    def unique(pairs):
        result = {}
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
    def check_strings(value):
        if type(value) is str:
            require(
                "\x00" not in value
                and not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
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


def strict_load(path):
    return strict_load_raw(path.read_bytes())


def check_pins():
    require(
        Path(boundary_engine.__file__).resolve()
        == (HERE / "cm2_round151_dual_boundary_event_census_engine.py").resolve()
        and Path(bridge_engine.__file__).resolve()
        == (HERE / "cm2_round152_open_strip_bridge_engine.py").resolve(),
        "engine module identity",
    )
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            name,
        )


def specs():
    result = []
    for label, x0, x1, c0, c1, d0, d1 in SLABS:
        result.append(
            {
                "label": label,
                "c24": {
                    "abs_x_lower_h": x0,
                    "abs_x_upper_h": x1,
                    "beta_lower_h": c0,
                    "beta_upper_h": c1,
                },
                "bridge": {
                    "abs_x_lower_h": x0,
                    "abs_x_upper_h": x1,
                    "beta_lower_h": c1,
                    "beta_upper_h": d0,
                },
                "d3": {
                    "abs_x_lower_h": x0,
                    "abs_x_upper_h": x1,
                    "beta_lower_h": d0,
                    "beta_upper_h": d1,
                },
            }
        )
    return result


def reconstruct(row):
    c24_frontier = boundary_engine.c24_frontier(row["c24"])
    d3_frontier = boundary_engine.d3_frontier(row["d3"])
    c24_audit = boundary_engine.audit_c24_event_box(row["c24"])
    bridge_audit = bridge_engine.audit_bridge_cell(row["bridge"])
    d3_audit = boundary_engine.audit_d3_event_box(row["d3"])
    return normalize(
        {
            "label": row["label"],
            "abs_delta_x_in_h_units": bridge_audit[
                "abs_delta_x_in_h_units"
            ],
            "c24_frontier": c24_frontier,
            "c24_full_audit": c24_audit,
            "strict_return_bridge": bridge_audit,
            "d3_frontier": d3_frontier,
            "d3_full_audit": d3_audit,
            "vertical_chain_has_no_gap": True,
            "interior_event_cells_untyped": 0,
        }
    )


def overlap(first, second):
    lower = max(Q(first[0]), Q(second[0]))
    upper = min(Q(first[1]), Q(second[1]))
    require(lower < upper, "strict overlap")
    return [
        bridge_engine.r139.qstr(lower),
        bridge_engine.r139.qstr(upper),
    ]


def adjacency(previous, row):
    require(
        previous["abs_delta_x_in_h_units"][1]
        == row["abs_delta_x_in_h_units"][0],
        "x face",
    )
    return {
        "shared_abs_delta_x_face_in_h_units": row[
            "abs_delta_x_in_h_units"
        ][0],
        "C24_beta_overlap": overlap(
            previous["c24_frontier"]["delta_beta_event_box_in_h_units"],
            row["c24_frontier"]["delta_beta_event_box_in_h_units"],
        ),
        "bridge_beta_overlap": overlap(
            previous["strict_return_bridge"]["delta_beta_in_h_units"],
            row["strict_return_bridge"]["delta_beta_in_h_units"],
        ),
        "D3_beta_overlap": overlap(
            previous["d3_frontier"]["delta_beta_event_box_in_h_units"],
            row["d3_frontier"]["delta_beta_event_box_in_h_units"],
        ),
    }


def expected_adjacencies(prior, rows):
    previous = prior["new_upper_continuation"]["new_rows"][-1]
    result = []
    for row in rows:
        result.append(adjacency(previous, row))
        previous = row
    return result


def expected_census(rows):
    r1648_tests = sum(
        row["c24_full_audit"]["full_radius4_candidate_test_count"]
        + row["strict_return_bridge"]["full_radius4_candidate_test_count"]
        for row in rows
    )
    d3_tests = sum(
        row["d3_full_audit"][
            "fully_audited_prefix_radius4_candidate_test_count"
        ]
        + row["d3_full_audit"][
            "collision3_full_radius4_candidate_test_count"
        ]
        for row in rows
    )
    return {
        "new_full_R1648_C24_audits": len(rows),
        "new_full_R1648_bridge_audits": len(rows),
        "new_collision_stage_object_pairs": sum(
            row["c24_full_audit"]["collision_count"]
            + row["strict_return_bridge"]["collision_count"]
            for row in rows
        ),
        "new_R1648_path_radius4_candidate_tests": r1648_tests,
        "new_full_D3_event_box_audits": len(rows),
        "new_D3_event_box_radius4_candidate_tests": d3_tests,
        "new_total_radius4_candidate_tests": r1648_tests + d3_tests,
    }


def validate(result, rows, prior, prior_verification):
    require(
        set(result)
        == {
            "status",
            "physical_coordinate_scale",
            "inherited_round158_result_sha256",
            "inherited_round158_verification_result_sha256",
            "certified_abs_delta_x_corridor_in_h_units",
            "new_upper_continuation",
            "combined_typed_atlas",
            "audit_census",
            "strict_nonpromotion",
            "next_core_gate",
        },
        "result keys",
    )
    require(result["status"] == STATUS, "status")
    require(result["physical_coordinate_scale"] == "h=2^-4296", "scale")
    require(
        result["inherited_round158_result_sha256"] == digest(prior),
        "inherited result",
    )
    require(
        result["inherited_round158_verification_result_sha256"]
        == prior_verification["result_sha256"],
        "inherited verification",
    )
    require(
        result["certified_abs_delta_x_corridor_in_h_units"] == ["0", "352"],
        "corridor",
    )
    continuation = result["new_upper_continuation"]
    require(
        set(continuation)
        == {
            "new_typed_slab_count",
            "new_typed_box_count",
            "new_rows",
            "new_rows_sha256",
            "exact_face_adjacencies_from_320h_through_352h",
            "new_event_family_count",
            "upper_endpoint_continuation_complete",
        },
        "continuation keys",
    )
    require(
        same(continuation["new_typed_slab_count"], len(rows)),
        "slab count",
    )
    require(
        same(continuation["new_typed_box_count"], 3 * len(rows)),
        "box count",
    )
    require(
        same(continuation["new_rows"], rows)
        and continuation["new_rows_sha256"]
        == digest(continuation["new_rows"])
        == digest(rows),
        "rows",
    )
    require(
        same(
            continuation["exact_face_adjacencies_from_320h_through_352h"],
            expected_adjacencies(prior, rows),
        ),
        "adjacencies",
    )
    require(
        same(continuation["new_event_family_count"], 0)
        and same(continuation["upper_endpoint_continuation_complete"], False),
        "events",
    )
    for row in rows:
        c24 = row["c24_full_audit"]
        bridge = row["strict_return_bridge"]
        d3 = row["d3_full_audit"]
        require(c24["status"] == bridge["status"] == d3["status"] == "PASS", "audit")
        require(same(c24["collision_count"], 1648), "C24 collision count")
        require(same(bridge["collision_count"], 1648), "bridge collision count")
        require(
            same(c24["full_radius4_candidate_test_count"], 265328),
            "C24 candidates",
        )
        require(
            same(bridge["full_radius4_candidate_test_count"], 265328),
            "bridge candidates",
        )
        require(
            same(d3["fully_audited_prefix_collision_count"], 2)
            and same(d3["fully_audited_prefix_radius4_candidate_test_count"], 322)
            and same(d3["collision3_full_radius4_candidate_test_count"], 161),
            "D3 candidates",
        )
        require(
            bridge["terminal_classification"] == "RETURN_AT_3_INNER"
            and same(row["vertical_chain_has_no_gap"], True)
            and same(row["interior_event_cells_untyped"], 0),
            "typed return",
        )
        require(
            same(
                row["abs_delta_x_in_h_units"],
                row["c24_frontier"]["abs_delta_x_in_h_units"],
            )
            and same(
                row["abs_delta_x_in_h_units"],
                row["strict_return_bridge"]["abs_delta_x_in_h_units"],
            )
            and same(
                row["abs_delta_x_in_h_units"],
                row["d3_frontier"]["abs_delta_x_in_h_units"],
            ),
            "common x slab",
        )
        require(
            row["c24_frontier"]["delta_beta_event_box_in_h_units"][1]
            == row["strict_return_bridge"]["delta_beta_in_h_units"][0]
            and row["strict_return_bridge"]["delta_beta_in_h_units"][1]
            == row["d3_frontier"]["delta_beta_event_box_in_h_units"][0],
            "gap-free beta chain",
        )
    require(
        same(
            result["combined_typed_atlas"],
            {
                "slab_count":
                    prior["combined_typed_atlas"]["slab_count"] + len(rows),
                "typed_box_count":
                    prior["combined_typed_atlas"]["typed_box_count"]
                    + 3 * len(rows),
                "connected": True,
                "interior_untyped_event_cell_count": 0,
                "lower_symmetry_axis_terminal": True,
                "upper_endpoint_in_h_units": "352",
                "upper_endpoint_terminal": False,
            },
        ),
        "atlas",
    )
    require(
        same(
            result["audit_census"],
            expected_census(rows),
        ),
        "census",
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
        "nonpromotion",
    )
    require(
        result["next_core_gate"]
        == (
            "continue beyond 352h with 4h C24-controlled slabs until terminal "
            "exit or typed new event, then exclude exterior sheets"
        ),
        "next gate",
    )


def validate_document(document, rows, prior, prior_verification):
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "certificate keys",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(
        document["result_sha256"] == digest(document["result"]),
        "certificate digest",
    )
    validate(document["result"], rows, prior, prior_verification)


def attacks(result, rows, prior, prior_verification):
    labels = [
        "delete_row",
        "survive",
        "invent_event",
        "disconnect",
        "claim_terminal",
        "close_D02",
        "authorize_D03",
        "promote_gate5",
        "create_block",
        "promote_CM2",
        "tamper_adjacency",
        "tamper_inheritance",
        "tamper_verification_inheritance",
        "tamper_census",
        "wrong_status",
        "extra_field",
        "type_confusion",
        "nested_type_confusion",
        "claim_continuation_complete",
        "tamper_corridor",
        "tamper_scale",
        "tamper_next_gate",
    ]
    rejected = []
    for label in labels:
        candidate = copy.deepcopy(result)
        if label == "delete_row":
            candidate["new_upper_continuation"]["new_rows"].pop()
        elif label == "survive":
            candidate["new_upper_continuation"]["new_rows"][0][
                "strict_return_bridge"
            ]["terminal_classification"] = "SURVIVE_THROUGH_3_INNER"
        elif label == "invent_event":
            candidate["new_upper_continuation"]["new_event_family_count"] = 1
        elif label == "disconnect":
            candidate["combined_typed_atlas"]["connected"] = False
        elif label == "claim_terminal":
            candidate["combined_typed_atlas"]["upper_endpoint_terminal"] = True
        elif label == "close_D02":
            candidate["strict_nonpromotion"]["D02_status"] = "CERTIFIED"
        elif label == "authorize_D03":
            candidate["strict_nonpromotion"]["D03_authorized"] = True
        elif label == "promote_gate5":
            candidate["strict_nonpromotion"]["global_gate5_maturity"] = "18/18"
        elif label == "create_block":
            candidate["strict_nonpromotion"][
                "global_complete_18_field_block_count"
            ] = 1
        elif label == "promote_CM2":
            candidate["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
        elif label == "tamper_adjacency":
            candidate["new_upper_continuation"][
                "exact_face_adjacencies_from_320h_through_352h"
            ][0]["C24_beta_overlap"][0] = "0"
        elif label == "tamper_inheritance":
            candidate["inherited_round158_result_sha256"] = "0" * 64
        elif label == "tamper_verification_inheritance":
            candidate[
                "inherited_round158_verification_result_sha256"
            ] = "0" * 64
        elif label == "tamper_census":
            candidate["audit_census"][
                "new_R1648_path_radius4_candidate_tests"
            ] -= 1
        elif label == "wrong_status":
            candidate["status"] = "PASS"
        elif label == "extra_field":
            candidate["unexpected"] = True
        elif label == "type_confusion":
            candidate["combined_typed_atlas"]["connected"] = 1
        elif label == "nested_type_confusion":
            candidate["new_upper_continuation"]["new_rows"][0][
                "interior_event_cells_untyped"
            ] = False
        elif label == "claim_continuation_complete":
            candidate["new_upper_continuation"][
                "upper_endpoint_continuation_complete"
            ] = True
        elif label == "tamper_corridor":
            candidate["certified_abs_delta_x_corridor_in_h_units"][1] = "353"
        elif label == "tamper_scale":
            candidate["physical_coordinate_scale"] = "h=2^-4295"
        else:
            candidate["next_core_gate"] = "promote now"
        try:
            validate(candidate, rows, prior, prior_verification)
        except Exception:
            rejected.append(label)
    require(rejected == labels, "attacks")
    return rejected


def document_attacks(document, rows, prior, prior_verification):
    labels = [
        "wrapper_wrong_schema",
        "wrapper_result_sha",
        "wrapper_extra_key",
        "coherent_row_tamper",
        "coherent_first_seam_tamper",
        "coherent_census_total_tamper",
        "coherent_row_reorder",
        "coherent_inheritance_tamper",
        "coherent_verification_inheritance_tamper",
        "coherent_atlas_count_tamper",
        "coherent_continuation_count_tamper",
        "coherent_internal_adjacency_tamper",
        "coherent_census_components_and_total_tamper",
    ]
    rejected = []
    for label in labels:
        candidate = copy.deepcopy(document)
        if label == "wrapper_wrong_schema":
            candidate["schema"] = "cm2.round159.invalid"
        elif label == "wrapper_result_sha":
            candidate["result_sha256"] = "0" * 64
        elif label == "wrapper_extra_key":
            candidate["unexpected"] = True
        elif label == "coherent_row_tamper":
            rows_value = candidate["result"]["new_upper_continuation"]["new_rows"]
            rows_value[0]["interior_event_cells_untyped"] = 1
            candidate["result"]["new_upper_continuation"][
                "new_rows_sha256"
            ] = digest(rows_value)
            candidate["result_sha256"] = digest(candidate["result"])
        elif label == "coherent_first_seam_tamper":
            candidate["result"]["new_upper_continuation"][
                "exact_face_adjacencies_from_320h_through_352h"
            ][0]["C24_beta_overlap"][0] = "0"
            candidate["result_sha256"] = digest(candidate["result"])
        elif label == "coherent_census_total_tamper":
            candidate["result"]["audit_census"][
                "new_total_radius4_candidate_tests"
            ] -= 1
            candidate["result_sha256"] = digest(candidate["result"])
        elif label == "coherent_row_reorder":
            rows_value = candidate["result"]["new_upper_continuation"]["new_rows"]
            rows_value[0], rows_value[1] = rows_value[1], rows_value[0]
            candidate["result"]["new_upper_continuation"][
                "new_rows_sha256"
            ] = digest(rows_value)
            candidate["result_sha256"] = digest(candidate["result"])
        elif label == "coherent_inheritance_tamper":
            candidate["result"]["inherited_round158_result_sha256"] = "0" * 64
            candidate["result_sha256"] = digest(candidate["result"])
        elif label == "coherent_verification_inheritance_tamper":
            candidate["result"][
                "inherited_round158_verification_result_sha256"
            ] = "0" * 64
            candidate["result_sha256"] = digest(candidate["result"])
        elif label == "coherent_atlas_count_tamper":
            candidate["result"]["combined_typed_atlas"]["slab_count"] += 1
            candidate["result"]["combined_typed_atlas"]["typed_box_count"] += 3
            candidate["result_sha256"] = digest(candidate["result"])
        elif label == "coherent_continuation_count_tamper":
            candidate["result"]["new_upper_continuation"][
                "new_typed_slab_count"
            ] += 1
            candidate["result"]["new_upper_continuation"][
                "new_typed_box_count"
            ] += 3
            candidate["result_sha256"] = digest(candidate["result"])
        elif label == "coherent_internal_adjacency_tamper":
            candidate["result"]["new_upper_continuation"][
                "exact_face_adjacencies_from_320h_through_352h"
            ][4]["bridge_beta_overlap"][0] = "0"
            candidate["result_sha256"] = digest(candidate["result"])
        else:
            census = candidate["result"]["audit_census"]
            census["new_R1648_path_radius4_candidate_tests"] -= 1
            census["new_total_radius4_candidate_tests"] -= 1
            candidate["result_sha256"] = digest(candidate["result"])
        try:
            validate_document(candidate, rows, prior, prior_verification)
        except Exception:
            rejected.append(label)
    require(rejected == labels, "document attacks")
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    check_pins()
    certificate = strict_load(args.certificate)
    prior_document = strict_load(
        HERE / "cm2-round158-upper-endpoint-continuation-to-320h-2026-07-25.json"
    )
    prior_verification = strict_load(
        HERE
        / "cm2-round158-upper-endpoint-continuation-to-320h-verification-2026-07-25.json"
    )
    require(
        set(prior_document) == {"schema", "result", "result_sha256"}
        and prior_document["schema"]
        == "cm2.round158.upper-endpoint-continuation-to-320h.v1"
        and prior_document["result_sha256"] == digest(prior_document["result"]),
        "prior certificate",
    )
    require(
        set(prior_verification) == {"schema", "result", "result_sha256"}
        and prior_verification["schema"]
        == "cm2.round158.upper-endpoint-continuation-to-320h.verification.v1"
        and prior_verification["result_sha256"]
        == digest(prior_verification["result"])
        and prior_verification["result"]["status"] == "PASS"
        and prior_verification["result"]["certificate_result_sha256"]
        == prior_document["result_sha256"],
        "prior verification",
    )
    prior = prior_document["result"]
    with ProcessPoolExecutor(max_workers=8) as pool:
        rows = normalize(list(pool.map(reconstruct, specs(), chunksize=1)))
    rows.sort(key=lambda row: Q(row["abs_delta_x_in_h_units"][0]))
    validate_document(certificate, rows, prior, prior_verification)
    rejected = attacks(certificate["result"], rows, prior, prior_verification)
    rejected += document_attacks(
        certificate,
        rows,
        prior,
        prior_verification,
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
    census = expected_census(rows)
    result = {
        "status": "PASS",
        "certificate_result_sha256": certificate["result_sha256"],
        "prior_certificate_result_sha256": prior_document["result_sha256"],
        "prior_verification_result_sha256": prior_verification["result_sha256"],
        "producer_source_sha256": PINS[
            "cm2_round159_upper_endpoint_continuation_to_352h.py"
        ],
        "producer_imported_or_executed": False,
        "engine_module_identity_checked": True,
        "new_slab_reconstruction_count": len(rows),
        "new_full_R1648_object_reconstruction_count": 2 * len(rows),
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
        "combined_typed_box_count_recomputed":
            prior["combined_typed_atlas"]["typed_box_count"] + 3 * len(rows),
        "upper_endpoint_reached_in_h_units": "352",
        "exact_face_adjacency_count_recomputed": len(rows),
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
    args.output.write_text(
        json.dumps(document, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        canonical(
            {
                "status": "PASS",
                "output": str(args.output),
                "result_sha256": document["result_sha256"],
            }
        )
    )


if __name__ == "__main__":
    main()
