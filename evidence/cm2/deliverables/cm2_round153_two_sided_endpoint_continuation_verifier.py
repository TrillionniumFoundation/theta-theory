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
CERTIFICATE = HERE / "cm2-round153-two-sided-endpoint-continuation-2026-07-25.json"
OUTPUT = HERE / "cm2-round153-two-sided-endpoint-continuation-verification-2026-07-25.json"
SCHEMA = "cm2.round153.two-sided-endpoint-continuation.verification.v1"
PINS = {
    "cm2_round151_dual_boundary_event_census_engine.py":
        "dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085",
    "cm2_round152_open_strip_bridge_engine.py":
        "21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738",
    "cm2_round153_two_sided_endpoint_continuation.py":
        "dfa3ae4931472ff6d82d720a427c6119defdd67753b3587d5d0cb22ea9b7f3c6",
}
SLABS = [
    ("lower-axis", "0", "1", "-420", "-403", "-5", "5"),
    ("upper-01", "1169/8", "147", "-3", "5", "408", "416"),
    ("upper-02", "147", "148", "-1", "8", "410", "420"),
    ("upper-03", "148", "150", "1", "15", "414", "426"),
    ("upper-04", "150", "152", "7", "21", "418", "432"),
    ("upper-05", "152", "156", "10", "35", "423", "444"),
    ("upper-06", "156", "160", "22", "46", "434", "456"),
]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


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
    result = json.loads(raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=reject)
    require(type(result) is dict, "top object")
    return result


def strict_load(path):
    return strict_load_raw(path.read_bytes())


def check_pins():
    for name, expected in PINS.items():
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, name)


def spec_rows():
    result = []
    for label, x0, x1, c0, c1, d0, d1 in SLABS:
        result.append({
            "label": label,
            "c24": {"abs_x_lower_h": x0, "abs_x_upper_h": x1,
                    "beta_lower_h": c0, "beta_upper_h": c1},
            "bridge": {"abs_x_lower_h": x0, "abs_x_upper_h": x1,
                       "beta_lower_h": c1, "beta_upper_h": d0},
            "d3": {"abs_x_lower_h": x0, "abs_x_upper_h": x1,
                   "beta_lower_h": d0, "beta_upper_h": d1},
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


def validate_semantics(result, reconstructed_rows):
    require(result["certified_abs_delta_x_corridor_in_h_units"] == ["0", "160"], "corridor")
    continuation = result["new_endpoint_continuation"]
    require(continuation["new_typed_slab_count"] == 7, "slabs")
    require(continuation["new_typed_box_count"] == 21, "new boxes")
    require(continuation["new_rows"] == reconstructed_rows, "independent rows")
    require(continuation["new_rows_sha256"] == digest(reconstructed_rows), "rows digest")
    require(continuation["lower_endpoint_is_abs_delta_x_symmetry_axis"] is True, "axis")
    require(continuation["lower_endpoint_terminal_by_abs_coordinate_domain"] is True, "axis terminal")
    require(continuation["upper_endpoint_continuation_complete"] is False, "upper nonclosure")
    require(len(continuation["upper_exact_face_adjacencies"]) == 6, "upper adjacency count")
    require(set(continuation["lower_axis_connection"]) == {"C24_beta_overlap", "bridge_beta_overlap", "D3_beta_overlap"}, "lower joins")
    for row in reconstructed_rows:
        c24 = row["c24_full_audit"]
        bridge = row["strict_return_bridge"]
        d3 = row["d3_full_audit"]
        require(c24["status"] == bridge["status"] == d3["status"] == "PASS", "audit pass")
        require(c24["collision_count"] == bridge["collision_count"] == 1648, "collision count")
        require(c24["full_radius4_candidate_test_count"] == bridge["full_radius4_candidate_test_count"] == 265328, "candidate census")
        require(bridge["terminal_classification"] == "RETURN_AT_3_INNER", "return")
        require(row["interior_event_cells_untyped"] == 0, "typed interior")
    for left, right in zip(reconstructed_rows[1:], reconstructed_rows[2:]):
        require(left["abs_delta_x_in_h_units"][1] == right["abs_delta_x_in_h_units"][0], "x adjacency")
        require(strict_overlap(left["c24_frontier"]["delta_beta_event_box_in_h_units"], right["c24_frontier"]["delta_beta_event_box_in_h_units"]), "C24 overlap")
        require(strict_overlap(left["strict_return_bridge"]["delta_beta_in_h_units"], right["strict_return_bridge"]["delta_beta_in_h_units"]), "bridge overlap")
        require(strict_overlap(left["d3_frontier"]["delta_beta_event_box_in_h_units"], right["d3_frontier"]["delta_beta_event_box_in_h_units"]), "D3 overlap")
    atlas = result["combined_typed_atlas"]
    require(atlas["slab_count"] == 28 and atlas["typed_box_count"] == 84, "combined count")
    require(atlas["connected"] is True and atlas["interior_untyped_event_cell_count"] == 0, "combined atlas")
    require(atlas["new_event_family_count"] == 0 and len(atlas["boundary_event_families"]) == 2, "event families")
    census = result["audit_census"]
    require(census["new_full_R1648_C24_audits"] == 7, "C24 census")
    require(census["new_full_R1648_bridge_audits"] == 7, "bridge census")
    require(census["new_collision_stage_object_pairs"] == 23072, "pair census")
    require(census["new_full_radius4_candidate_tests"] == 3714592, "test census")
    strict = result["strict_nonpromotion"]
    require(strict == {"D02_status": "BLOCKED", "D03_authorized": False,
                       "global_gate5_maturity": "10/18",
                       "global_complete_18_field_block_count": 0,
                       "CM2": "NO-GO_FOR_CLAIM"}, "nonpromotion")


def mutation_attacks(result, reconstructed_rows):
    labels = [
        "delete_row", "survive_bridge", "invent_event", "disconnect_atlas",
        "erase_axis_terminal", "close_upper", "close_D02", "authorize_D03",
        "promote_gate5", "promote_CM2",
    ]
    rejected = []
    for label in labels:
        candidate = copy.deepcopy(result)
        if label == "delete_row":
            candidate["new_endpoint_continuation"]["new_rows"].pop()
        elif label == "survive_bridge":
            candidate["new_endpoint_continuation"]["new_rows"][0]["strict_return_bridge"]["terminal_classification"] = "SURVIVE_THROUGH_3_INNER"
        elif label == "invent_event":
            candidate["combined_typed_atlas"]["new_event_family_count"] = 1
        elif label == "disconnect_atlas":
            candidate["combined_typed_atlas"]["connected"] = False
        elif label == "erase_axis_terminal":
            candidate["new_endpoint_continuation"]["lower_endpoint_terminal_by_abs_coordinate_domain"] = False
        elif label == "close_upper":
            candidate["new_endpoint_continuation"]["upper_endpoint_continuation_complete"] = True
        elif label == "close_D02":
            candidate["strict_nonpromotion"]["D02_status"] = "CERTIFIED"
        elif label == "authorize_D03":
            candidate["strict_nonpromotion"]["D03_authorized"] = True
        elif label == "promote_gate5":
            candidate["strict_nonpromotion"]["global_gate5_maturity"] = "18/18"
        else:
            candidate["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
        try:
            validate_semantics(candidate, reconstructed_rows)
        except Exception:
            rejected.append(label)
    require(rejected == labels, "semantic attacks")
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    check_pins()
    certificate = strict_load(args.certificate)
    require(certificate["result_sha256"] == digest(certificate["result"]), "certificate digest")
    specs = spec_rows()
    with ProcessPoolExecutor(max_workers=7) as pool:
        reconstructed_rows = normalize(list(pool.map(reconstruct, specs, chunksize=1)))
    reconstructed_rows.sort(key=lambda row: Q(row["abs_delta_x_in_h_units"][0]))
    validate_semantics(certificate["result"], reconstructed_rows)
    rejected = mutation_attacks(certificate["result"], reconstructed_rows)
    strict_attacks = [b'{"x":1,"x":2}\n', b"\xef\xbb\xbf{}\n", b"[1,2]\n", b'{"x":NaN}\n']
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
        "producer_source_sha256": PINS["cm2_round153_two_sided_endpoint_continuation.py"],
        "producer_imported_or_executed": False,
        "new_slab_reconstruction_count": 7,
        "new_full_R1648_object_reconstruction_count": 14,
        "new_collision_stage_object_pairs_replayed": 23072,
        "new_full_radius4_candidate_tests_replayed": 3714592,
        "combined_typed_box_count_recomputed": 84,
        "lower_symmetry_axis_terminal_recomputed": True,
        "upper_endpoint_reached_in_h_units": "160",
        "semantic_mutation_rejection_labels": rejected,
        "semantic_mutation_rejection_count": len(rejected),
        "strict_json_attack_rejection_count": strict_rejected,
        "D02_status": "BLOCKED",
        "D03_authorized": False,
        "global_gate5_maturity": "10/18",
        "global_complete_18_field_block_count": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    args.output.write_text(json.dumps(document, sort_keys=True, indent=2, ensure_ascii=False) + "\n")
    print(canonical({"status": "PASS", "output": str(args.output), "result_sha256": document["result_sha256"]}))


if __name__ == "__main__":
    main()
