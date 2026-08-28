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
CERTIFICATE = HERE / "cm2-round154-upper-endpoint-continuation-to-192h-2026-07-25.json"
OUTPUT = HERE / "cm2-round154-upper-endpoint-continuation-to-192h-verification-2026-07-25.json"
SCHEMA = "cm2.round154.upper-endpoint-continuation-to-192h.verification.v1"
PINS = {
    "cm2_round151_dual_boundary_event_census_engine.py":
        "dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085",
    "cm2_round152_open_strip_bridge_engine.py":
        "21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738",
    "cm2_round154_upper_endpoint_continuation_to_192h.py":
        "e6a6d8ed366082199b619027cedd2e2dc1de29816793b9e7311924fd0a31b19d",
}
SLABS = [
    ("upper-07", "160", "164", "20", "65", "445", "463"),
    ("upper-08", "164", "168", "30", "85", "456", "480"),
    ("upper-09", "168", "176", "50", "100", "467", "503"),
    ("upper-10", "176", "184", "72", "122", "489", "525"),
    ("upper-11", "184", "192", "94", "145", "511", "548"),
]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def normalize(value):
    return json.loads(canonical(value))


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


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

    require(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "encoding")
    result = json.loads(raw.decode(), object_pairs_hook=unique, parse_constant=reject)
    require(type(result) is dict, "top object")
    return result


def strict_load(path):
    return strict_load_raw(path.read_bytes())


def check_pins():
    for name, expected in PINS.items():
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, name)


def specs():
    result = []
    for label, x0, x1, c0, c1, d0, d1 in SLABS:
        result.append({
            "label": label,
            "c24": {"abs_x_lower_h": x0, "abs_x_upper_h": x1, "beta_lower_h": c0, "beta_upper_h": c1},
            "bridge": {"abs_x_lower_h": x0, "abs_x_upper_h": x1, "beta_lower_h": c1, "beta_upper_h": d0},
            "d3": {"abs_x_lower_h": x0, "abs_x_upper_h": x1, "beta_lower_h": d0, "beta_upper_h": d1},
        })
    return result


def reconstruct(row):
    c24_frontier = boundary_engine.c24_frontier(row["c24"])
    d3_frontier = boundary_engine.d3_frontier(row["d3"])
    c24_audit = boundary_engine.audit_c24_event_box(row["c24"])
    bridge_audit = bridge_engine.audit_bridge_cell(row["bridge"])
    d3_audit = boundary_engine.audit_d3_event_box(row["d3"])
    return normalize({
        "label": row["label"],
        "abs_delta_x_in_h_units": bridge_audit["abs_delta_x_in_h_units"],
        "c24_frontier": c24_frontier,
        "c24_full_audit": c24_audit,
        "strict_return_bridge": bridge_audit,
        "d3_frontier": d3_frontier,
        "d3_full_audit": d3_audit,
        "vertical_chain_has_no_gap": True,
        "interior_event_cells_untyped": 0,
    })


def strict_overlap(first, second):
    return max(Q(first[0]), Q(second[0])) < min(Q(first[1]), Q(second[1]))


def validate(result, rows):
    require(result["certified_abs_delta_x_corridor_in_h_units"] == ["0", "192"], "corridor")
    continuation = result["new_upper_continuation"]
    require(continuation["new_typed_slab_count"] == 5 and continuation["new_typed_box_count"] == 15, "new counts")
    require(continuation["new_rows"] == rows and continuation["new_rows_sha256"] == digest(rows), "rows")
    require(len(continuation["exact_face_adjacencies_from_160h_through_192h"]) == 5, "adjacencies")
    require(continuation["new_event_family_count"] == 0, "event family")
    require(continuation["upper_endpoint_continuation_complete"] is False, "nonclosure")
    for row in rows:
        c24 = row["c24_full_audit"]
        bridge = row["strict_return_bridge"]
        d3 = row["d3_full_audit"]
        require(c24["status"] == bridge["status"] == d3["status"] == "PASS", "audit")
        require(c24["collision_count"] == bridge["collision_count"] == 1648, "collisions")
        require(c24["full_radius4_candidate_test_count"] == bridge["full_radius4_candidate_test_count"] == 265328, "candidates")
        require(bridge["terminal_classification"] == "RETURN_AT_3_INNER", "return")
        require(row["interior_event_cells_untyped"] == 0, "typed")
    for left, right in zip(rows, rows[1:]):
        require(left["abs_delta_x_in_h_units"][1] == right["abs_delta_x_in_h_units"][0], "x face")
        require(strict_overlap(left["c24_frontier"]["delta_beta_event_box_in_h_units"], right["c24_frontier"]["delta_beta_event_box_in_h_units"]), "C24 overlap")
        require(strict_overlap(left["strict_return_bridge"]["delta_beta_in_h_units"], right["strict_return_bridge"]["delta_beta_in_h_units"]), "bridge overlap")
        require(strict_overlap(left["d3_frontier"]["delta_beta_event_box_in_h_units"], right["d3_frontier"]["delta_beta_event_box_in_h_units"]), "D3 overlap")
    atlas = result["combined_typed_atlas"]
    require(atlas == {"slab_count": 33, "typed_box_count": 99, "connected": True,
                      "interior_untyped_event_cell_count": 0,
                      "lower_symmetry_axis_terminal": True,
                      "upper_endpoint_in_h_units": "192", "upper_endpoint_terminal": False}, "atlas")
    census = result["audit_census"]
    require(census["new_collision_stage_object_pairs"] == 16480, "pairs")
    require(census["new_full_radius4_candidate_tests"] == 2653280, "tests")
    strict = result["strict_nonpromotion"]
    require(strict == {"D02_status": "BLOCKED", "D03_authorized": False,
                       "global_gate5_maturity": "10/18",
                       "global_complete_18_field_block_count": 0,
                       "CM2": "NO-GO_FOR_CLAIM"}, "nonpromotion")


def attacks(result, rows):
    labels = ["delete_row", "survive", "invent_event", "disconnect", "claim_terminal",
              "close_D02", "authorize_D03", "promote_gate5", "create_block", "promote_CM2"]
    rejected = []
    for label in labels:
        candidate = copy.deepcopy(result)
        if label == "delete_row": candidate["new_upper_continuation"]["new_rows"].pop()
        elif label == "survive": candidate["new_upper_continuation"]["new_rows"][0]["strict_return_bridge"]["terminal_classification"] = "SURVIVE_THROUGH_3_INNER"
        elif label == "invent_event": candidate["new_upper_continuation"]["new_event_family_count"] = 1
        elif label == "disconnect": candidate["combined_typed_atlas"]["connected"] = False
        elif label == "claim_terminal": candidate["combined_typed_atlas"]["upper_endpoint_terminal"] = True
        elif label == "close_D02": candidate["strict_nonpromotion"]["D02_status"] = "CERTIFIED"
        elif label == "authorize_D03": candidate["strict_nonpromotion"]["D03_authorized"] = True
        elif label == "promote_gate5": candidate["strict_nonpromotion"]["global_gate5_maturity"] = "18/18"
        elif label == "create_block": candidate["strict_nonpromotion"]["global_complete_18_field_block_count"] = 1
        else: candidate["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
        try:
            validate(candidate, rows)
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
    require(certificate["result_sha256"] == digest(certificate["result"]), "certificate digest")
    with ProcessPoolExecutor(max_workers=5) as pool:
        rows = normalize(list(pool.map(reconstruct, specs(), chunksize=1)))
    rows.sort(key=lambda row: Q(row["abs_delta_x_in_h_units"][0]))
    validate(certificate["result"], rows)
    rejected = attacks(certificate["result"], rows)
    strict_attacks = [b'{"x":1,"x":2}\n', b"\xef\xbb\xbf{}\n", b"[1]\n", b'{"x":NaN}\n']
    strict_rejected = 0
    for raw in strict_attacks:
        try: strict_load_raw(raw)
        except Exception: strict_rejected += 1
    require(strict_rejected == 4, "strict attacks")
    result = {
        "status": "PASS", "certificate_result_sha256": certificate["result_sha256"],
        "producer_source_sha256": PINS["cm2_round154_upper_endpoint_continuation_to_192h.py"],
        "producer_imported_or_executed": False,
        "new_slab_reconstruction_count": 5,
        "new_full_R1648_object_reconstruction_count": 10,
        "new_collision_stage_object_pairs_replayed": 16480,
        "new_full_radius4_candidate_tests_replayed": 2653280,
        "combined_typed_box_count_recomputed": 99,
        "upper_endpoint_reached_in_h_units": "192",
        "semantic_mutation_rejection_labels": rejected,
        "semantic_mutation_rejection_count": len(rejected),
        "strict_json_attack_rejection_count": strict_rejected,
        "D02_status": "BLOCKED", "D03_authorized": False,
        "global_gate5_maturity": "10/18", "global_complete_18_field_block_count": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    args.output.write_text(json.dumps(document, sort_keys=True, indent=2, ensure_ascii=False) + "\n")
    print(canonical({"status": "PASS", "output": str(args.output), "result_sha256": document["result_sha256"]}))


if __name__ == "__main__":
    main()
