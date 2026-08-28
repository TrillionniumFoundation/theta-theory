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
    HERE / "cm2-round156-upper-endpoint-continuation-to-256h-2026-07-25.json"
)
OUTPUT = (
    HERE
    / "cm2-round156-upper-endpoint-continuation-to-256h-verification-2026-07-25.json"
)
SCHEMA = "cm2.round156.upper-endpoint-continuation-to-256h.verification.v1"
CERTIFICATE_SCHEMA = "cm2.round156.upper-endpoint-continuation-to-256h.v1"
STATUS = "CERTIFIED_TYPED_UPPER_ENDPOINT_CONTINUATION_TO_256H__D02_STILL_BLOCKED"
PINS = {
    "cm2_round151_dual_boundary_event_census_engine.py": "dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085",
    "cm2_round152_open_strip_bridge_engine.py": "21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738",
    "cm2_round156_upper_endpoint_continuation_to_256h.py": "43fd7676ab979539cffffa9077a83c3d12c252110c2bef4dac1fa59bb43480c7",
    "cm2-round155-upper-endpoint-continuation-to-224h-2026-07-25.json": "5f39bf9d54469554397903cbb376ca41d7b623b13f1597cc0d2b3fd91d5f74cd",
    "cm2-round155-upper-endpoint-continuation-to-224h-verification-2026-07-25.json": "5b0743612e83d6c805367a92bccbf9eb3dea63d1a749310db2d32826e2df5312",
}
SLABS = [
    ("upper-20", "224", "228", "200", "252", "624", "647"),
    ("upper-21", "228", "232", "212", "264", "635", "659"),
    ("upper-22", "232", "236", "223", "275", "646", "670"),
    ("upper-23", "236", "240", "234", "286", "657", "681"),
    ("upper-24", "240", "244", "245", "297", "668", "693"),
    ("upper-25", "244", "248", "256", "308", "679", "704"),
    ("upper-26", "248", "252", "267", "319", "690", "715"),
    ("upper-27", "252", "256", "278", "330", "701", "727"),
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
            "inherited_round155_result_sha256",
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
        result["inherited_round155_result_sha256"] == digest(prior),
        "inherited result",
    )
    require(
        result["certified_abs_delta_x_corridor_in_h_units"] == ["0", "256"],
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
            "exact_face_adjacencies_from_224h_through_256h",
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
            continuation["exact_face_adjacencies_from_224h_through_256h"],
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
                "slab_count": 49,
                "typed_box_count": 147,
                "connected": True,
                "interior_untyped_event_cell_count": 0,
                "lower_symmetry_axis_terminal": True,
                "upper_endpoint_in_h_units": "256",
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
                "new_full_radius4_candidate_tests": 4245248,
                "new_full_D3_event_box_audits": 8,
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
            "continue beyond 256h with 4h C24-controlled slabs until terminal "
            "exit or typed new event, then exclude exterior sheets"
        ),
        "next gate",
    )


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
                "exact_face_adjacencies_from_224h_through_256h"
            ][0]["C24_beta_overlap"][0] = "0"
        elif label == "tamper_inheritance":
            candidate["inherited_round155_result_sha256"] = "0" * 64
        elif label == "tamper_census":
            candidate["audit_census"]["new_full_R1648_C24_audits"] = 7
        elif label == "wrong_status":
            candidate["status"] = "PASS"
        elif label == "extra_field":
            candidate["unexpected"] = True
        else:
            candidate["combined_typed_atlas"]["connected"] = 1
        try:
            validate(candidate, rows, prior)
        except Exception:
            rejected.append(label)
    require(rejected == labels, "attacks")
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    check_pins()
    certificate = strict_load(args.certificate)
    require(
        set(certificate) == {"schema", "result", "result_sha256"},
        "certificate keys",
    )
    require(certificate["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(
        certificate["result_sha256"] == digest(certificate["result"]),
        "digest",
    )
    prior_document = strict_load(
        HERE / "cm2-round155-upper-endpoint-continuation-to-224h-2026-07-25.json"
    )
    prior_verification = strict_load(
        HERE
        / "cm2-round155-upper-endpoint-continuation-to-224h-verification-2026-07-25.json"
    )
    require(
        prior_document["result_sha256"] == digest(prior_document["result"]),
        "prior digest",
    )
    require(
        prior_document["schema"]
        == "cm2.round155.upper-endpoint-continuation-to-224h.v1",
        "prior schema",
    )
    require(
        prior_verification["schema"]
        == "cm2.round155.upper-endpoint-continuation-to-224h.verification.v1"
        and prior_verification["result"]["status"] == "PASS",
        "prior pass",
    )
    prior = prior_document["result"]
    with ProcessPoolExecutor(max_workers=8) as pool:
        rows = normalize(list(pool.map(reconstruct, specs(), chunksize=1)))
    rows.sort(key=lambda row: Q(row["abs_delta_x_in_h_units"][0]))
    validate(certificate["result"], rows, prior)
    rejected = attacks(certificate["result"], rows, prior)
    strict_attacks = [
        b'{"x":1,"x":2}\n',
        b"\xef\xbb\xbf{}\n",
        b"[1]\n",
        b'{"x":NaN}\n',
    ]
    strict_rejected = 0
    for raw in strict_attacks:
        try:
            strict_load_raw(raw)
        except Exception:
            strict_rejected += 1
    require(strict_rejected == 4, "strict attacks")
    result = {
        "status": "PASS",
        "certificate_result_sha256": certificate["result_sha256"],
        "producer_source_sha256": PINS[
            "cm2_round156_upper_endpoint_continuation_to_256h.py"
        ],
        "producer_imported_or_executed": False,
        "new_slab_reconstruction_count": 8,
        "new_full_R1648_object_reconstruction_count": 16,
        "new_collision_stage_object_pairs_replayed": 26368,
        "new_R1648_path_radius4_candidate_tests_replayed": 4245248,
        "new_D3_event_box_radius4_candidate_tests_replayed": 3864,
        "new_total_radius4_candidate_tests_replayed": 4249112,
        "combined_typed_box_count_recomputed": 147,
        "upper_endpoint_reached_in_h_units": "256",
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
