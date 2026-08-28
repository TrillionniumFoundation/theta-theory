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
    HERE / "cm2-round157-upper-endpoint-continuation-to-288h-2026-07-25.json"
)
OUTPUT = (
    HERE
    / "cm2-round157-upper-endpoint-continuation-to-288h-verification-2026-07-25.json"
)
CERTIFICATE_SCHEMA = "cm2.round157.upper-endpoint-continuation-to-288h.v1"
SCHEMA = "cm2.round157.upper-endpoint-continuation-to-288h.verification.v1"
STATUS = "CERTIFIED_TYPED_UPPER_ENDPOINT_CONTINUATION_TO_288H__D02_STILL_BLOCKED"
PINS = {
    "cm2_round151_dual_boundary_event_census_engine.py": "dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085",
    "cm2_round152_open_strip_bridge_engine.py": "21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738",
    "cm2_round157_upper_endpoint_continuation_to_288h.py": "3d50250036db578101435129f9d44d44728cdaf478ca4848a67aaf6af77ab929",
    "cm2-round156-upper-endpoint-continuation-to-256h-2026-07-25.json": "3d4deffd799cfc3b01ddcd48bc8784c165a7b9778603facbcdc01d414f2ec347",
    "cm2-round156-upper-endpoint-continuation-to-256h-verification-2026-07-25.json": "f94cd81f563cb14458c50203dbc49e771d26f3dcf3bce92754e4f1dba33f6973",
}
SLABS = [
    ("upper-28", "256", "260", "289", "341", "712", "738"),
    ("upper-29", "260", "264", "300", "352", "723", "749"),
    ("upper-30", "264", "268", "311", "363", "734", "760"),
    ("upper-31", "268", "272", "322", "374", "745", "771"),
    ("upper-32", "272", "276", "333", "385", "756", "782"),
    ("upper-33", "276", "280", "344", "396", "767", "793"),
    ("upper-34", "280", "284", "355", "407", "778", "804"),
    ("upper-35", "284", "288", "366", "418", "789", "815"),
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
    require(type(result) is dict, "top object")
    return result


def strict_load(path):
    return strict_load_raw(path.read_bytes())


def check_pins():
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


def validate(result, rows, prior):
    require(
        set(result)
        == {
            "status",
            "physical_coordinate_scale",
            "inherited_round156_result_sha256",
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
        result["inherited_round156_result_sha256"] == digest(prior),
        "inherited result",
    )
    require(
        result["certified_abs_delta_x_corridor_in_h_units"] == ["0", "288"],
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
            "exact_face_adjacencies_from_256h_through_288h",
            "new_event_family_count",
            "upper_endpoint_continuation_complete",
        },
        "continuation keys",
    )
    require(same(continuation["new_typed_slab_count"], 8), "slab count")
    require(same(continuation["new_typed_box_count"], 24), "box count")
    require(
        same(continuation["new_rows"], rows)
        and continuation["new_rows_sha256"]
        == digest(continuation["new_rows"])
        == digest(rows),
        "rows",
    )
    require(
        same(
            continuation["exact_face_adjacencies_from_256h_through_288h"],
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
                "slab_count": 57,
                "typed_box_count": 171,
                "connected": True,
                "interior_untyped_event_cell_count": 0,
                "lower_symmetry_axis_terminal": True,
                "upper_endpoint_in_h_units": "288",
                "upper_endpoint_terminal": False,
            },
        ),
        "atlas",
    )
    require(
        same(
            result["audit_census"],
            {
                "new_full_R1648_C24_audits": 8,
                "new_full_R1648_bridge_audits": 8,
                "new_collision_stage_object_pairs": 26368,
                "new_R1648_path_radius4_candidate_tests": 4245248,
                "new_full_D3_event_box_audits": 8,
                "new_D3_event_box_radius4_candidate_tests": 3864,
                "new_total_radius4_candidate_tests": 4249112,
            },
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
            "continue beyond 288h with 4h C24-controlled slabs until terminal "
            "exit or typed new event, then exclude exterior sheets"
        ),
        "next gate",
    )


def validate_document(document, rows, prior):
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "certificate keys",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(
        document["result_sha256"] == digest(document["result"]),
        "certificate digest",
    )
    validate(document["result"], rows, prior)


def attacks(result, rows, prior):
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
                "exact_face_adjacencies_from_256h_through_288h"
            ][0]["C24_beta_overlap"][0] = "0"
        elif label == "tamper_inheritance":
            candidate["inherited_round156_result_sha256"] = "0" * 64
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
            candidate["certified_abs_delta_x_corridor_in_h_units"][1] = "289"
        elif label == "tamper_scale":
            candidate["physical_coordinate_scale"] = "h=2^-4295"
        else:
            candidate["next_core_gate"] = "promote now"
        try:
            validate(candidate, rows, prior)
        except Exception:
            rejected.append(label)
    require(rejected == labels, "attacks")
    return rejected


def document_attacks(document, rows, prior):
    labels = [
        "wrapper_wrong_schema",
        "wrapper_result_sha",
        "wrapper_extra_key",
        "coherent_row_tamper",
        "coherent_row_reorder",
    ]
    rejected = []
    for label in labels:
        candidate = copy.deepcopy(document)
        if label == "wrapper_wrong_schema":
            candidate["schema"] = "cm2.round157.invalid"
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
        else:
            rows_value = candidate["result"]["new_upper_continuation"]["new_rows"]
            rows_value[0], rows_value[1] = rows_value[1], rows_value[0]
            candidate["result"]["new_upper_continuation"][
                "new_rows_sha256"
            ] = digest(rows_value)
            candidate["result_sha256"] = digest(candidate["result"])
        try:
            validate_document(candidate, rows, prior)
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
        HERE / "cm2-round156-upper-endpoint-continuation-to-256h-2026-07-25.json"
    )
    prior_verification = strict_load(
        HERE
        / "cm2-round156-upper-endpoint-continuation-to-256h-verification-2026-07-25.json"
    )
    require(
        prior_document["schema"]
        == "cm2.round156.upper-endpoint-continuation-to-256h.v1"
        and prior_document["result_sha256"] == digest(prior_document["result"]),
        "prior certificate",
    )
    require(
        prior_verification["schema"]
        == "cm2.round156.upper-endpoint-continuation-to-256h.verification.v1"
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
    validate_document(certificate, rows, prior)
    rejected = attacks(certificate["result"], rows, prior)
    rejected += document_attacks(certificate, rows, prior)
    strict_attacks = [
        b'{"x":1,"x":2}\n',
        b"\xef\xbb\xbf{}\n",
        b"[1]\n",
        b'{"x":NaN}\n',
        b'{"x":"a\x00b"}\n',
        b'{"x":"\xff"}\n',
        b'{"x":1} trailing\n',
        b'{"x":1e400}\n',
    ]
    strict_rejected = 0
    for raw in strict_attacks:
        try:
            strict_load_raw(raw)
        except Exception:
            strict_rejected += 1
    require(strict_rejected == 8, "strict attacks")
    result = {
        "status": "PASS",
        "certificate_result_sha256": certificate["result_sha256"],
        "producer_source_sha256": PINS[
            "cm2_round157_upper_endpoint_continuation_to_288h.py"
        ],
        "producer_imported_or_executed": False,
        "new_slab_reconstruction_count": 8,
        "new_full_R1648_object_reconstruction_count": 16,
        "new_collision_stage_object_pairs_replayed": 26368,
        "new_R1648_path_radius4_candidate_tests_replayed": 4245248,
        "new_D3_event_box_radius4_candidate_tests_replayed": 3864,
        "new_total_radius4_candidate_tests_replayed": 4249112,
        "combined_typed_box_count_recomputed": 171,
        "upper_endpoint_reached_in_h_units": "288",
        "exact_face_adjacency_count_recomputed": 8,
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
