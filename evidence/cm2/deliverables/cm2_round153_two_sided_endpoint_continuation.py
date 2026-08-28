#!/usr/bin/env python3
import argparse
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from pathlib import Path

import cm2_round151_dual_boundary_event_census_engine as boundary_engine
import cm2_round152_open_strip_bridge_engine as bridge_engine


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2-round153-two-sided-endpoint-continuation-2026-07-25.json"
SCHEMA = "cm2.round153.two-sided-endpoint-continuation.v1"
STATUS = (
    "CERTIFIED_TWO_SIDED_TYPED_STRIP_CONTINUATION_TO_SYMMETRY_AXIS_AND_160H"
    "__D02_STILL_BLOCKED"
)
PINS = {
    "cm2_round151_dual_boundary_event_census_engine.py":
        "dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085",
    "cm2_round152_open_strip_bridge_engine.py":
        "21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738",
    "cm2-round152-open-strip-bridge-atlas-2026-07-24.json":
        "f5f3ff201706ecd27bee6d3c668e67fa6a549cdcdf484ae7759ccf31eb45118f",
    "cm2-round152-open-strip-bridge-atlas-verification-2026-07-24.json":
        "0cadd6786867906a1afc4eae290fa19b9e241f72b0a4505ebb95a699060b5600",
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
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    )


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def normalize(value):
    return json.loads(canonical(value))


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def strict_load(path):
    def reject(value):
        raise ValueError(value)

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result

    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "encoding")
    result = json.loads(
        raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=reject,
    )
    require(type(result) is dict, "top object")
    return result


def check_pins():
    for name, expected in PINS.items():
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, name)
    inherited = strict_load(
        HERE / "cm2-round152-open-strip-bridge-atlas-2026-07-24.json"
    )
    verification = strict_load(
        HERE / "cm2-round152-open-strip-bridge-atlas-verification-2026-07-24.json"
    )
    require(inherited["result_sha256"] == digest(inherited["result"]), "inherited digest")
    require(verification["result"]["status"] == "PASS", "inherited verification")


def slab_specs():
    rows = []
    for label, x0, x1, c0, c1, d0, d1 in SLABS:
        rows.append({
            "label": label,
            "c24": {"abs_x_lower_h": x0, "abs_x_upper_h": x1,
                    "beta_lower_h": c0, "beta_upper_h": c1},
            "bridge": {"abs_x_lower_h": x0, "abs_x_upper_h": x1,
                       "beta_lower_h": c1, "beta_upper_h": d0},
            "d3": {"abs_x_lower_h": x0, "abs_x_upper_h": x1,
                   "beta_lower_h": d0, "beta_upper_h": d1},
        })
    return rows


def run_slab(row):
    c24_frontier = boundary_engine.c24_frontier(row["c24"])
    d3_frontier = boundary_engine.d3_frontier(row["d3"])
    c24_audit = boundary_engine.audit_c24_event_box(row["c24"])
    bridge_audit = bridge_engine.audit_bridge_cell(row["bridge"])
    d3_audit = boundary_engine.audit_d3_event_box(row["d3"])
    require(c24_audit["status"] == bridge_audit["status"] == d3_audit["status"] == "PASS", "audit")
    require(
        bridge_audit["delta_beta_in_h_units"][0]
        == c24_frontier["delta_beta_event_box_in_h_units"][1],
        "lower face",
    )
    require(
        bridge_audit["delta_beta_in_h_units"][1]
        == d3_frontier["delta_beta_event_box_in_h_units"][0],
        "upper face",
    )
    return {
        "label": row["label"],
        "abs_delta_x_in_h_units": bridge_audit["abs_delta_x_in_h_units"],
        "c24_frontier": c24_frontier,
        "c24_full_audit": c24_audit,
        "strict_return_bridge": bridge_audit,
        "d3_frontier": d3_frontier,
        "d3_full_audit": d3_audit,
        "vertical_chain_has_no_gap": True,
        "interior_event_cells_untyped": 0,
    }


def overlap(left, right, left_key, right_key):
    left_interval = left[left_key]
    right_interval = right[right_key]
    lower = max(Q(left_interval[0]), Q(right_interval[0]))
    upper = min(Q(left_interval[1]), Q(right_interval[1]))
    require(lower < upper, "strict face overlap")
    return [bridge_engine.r139.qstr(lower), bridge_engine.r139.qstr(upper)]


def build_result():
    check_pins()
    specs = slab_specs()
    with ProcessPoolExecutor(max_workers=7) as pool:
        new_rows = normalize(list(pool.map(run_slab, specs, chunksize=1)))
    new_rows.sort(key=lambda row: Q(row["abs_delta_x_in_h_units"][0]))
    inherited = strict_load(
        HERE / "cm2-round152-open-strip-bridge-atlas-2026-07-24.json"
    )["result"]
    old_bridges = inherited["typed_open_strip_atlas"]["strict_return_bridge_rows"]
    lower = new_rows[0]
    upper = new_rows[1:]
    require(lower["abs_delta_x_in_h_units"] == ["0", "1"], "lower endpoint")
    require(upper[-1]["abs_delta_x_in_h_units"][1] == "160", "upper endpoint")
    lower_connections = {
        "C24_beta_overlap": overlap(
            lower["c24_frontier"],
            strict_load(HERE / "cm2-round151-dual-boundary-event-census-2026-07-24.json")["result"]
            ["lower_terminal_C24_boundary_graph"]["event_box_rows"][0]["frontier"],
            "delta_beta_event_box_in_h_units", "delta_beta_event_box_in_h_units",
        ),
        "bridge_beta_overlap": overlap(
            lower["strict_return_bridge"], old_bridges[0],
            "delta_beta_in_h_units", "delta_beta_in_h_units",
        ),
        "D3_beta_overlap": overlap(
            lower["d3_frontier"],
            strict_load(HERE / "cm2-round151-dual-boundary-event-census-2026-07-24.json")["result"]
            ["upper_collision3_D3_boundary_graph"]["event_box_rows"][0]["frontier"],
            "delta_beta_event_box_in_h_units", "delta_beta_event_box_in_h_units",
        ),
    }
    upper_adjacencies = []
    previous = {
        "c24_frontier": strict_load(HERE / "cm2-round151-dual-boundary-event-census-2026-07-24.json")["result"]
        ["lower_terminal_C24_boundary_graph"]["event_box_rows"][-1]["frontier"],
        "strict_return_bridge": old_bridges[-1],
        "d3_frontier": strict_load(HERE / "cm2-round151-dual-boundary-event-census-2026-07-24.json")["result"]
        ["upper_collision3_D3_boundary_graph"]["event_box_rows"][-1]["frontier"],
    }
    for row in upper:
        require(
            previous["strict_return_bridge"]["abs_delta_x_in_h_units"][1]
            == row["abs_delta_x_in_h_units"][0], "upper exact x face",
        )
        upper_adjacencies.append({
            "shared_abs_delta_x_face_in_h_units": row["abs_delta_x_in_h_units"][0],
            "C24_beta_overlap": overlap(previous["c24_frontier"], row["c24_frontier"],
                                        "delta_beta_event_box_in_h_units", "delta_beta_event_box_in_h_units"),
            "bridge_beta_overlap": overlap(previous["strict_return_bridge"], row["strict_return_bridge"],
                                           "delta_beta_in_h_units", "delta_beta_in_h_units"),
            "D3_beta_overlap": overlap(previous["d3_frontier"], row["d3_frontier"],
                                       "delta_beta_event_box_in_h_units", "delta_beta_event_box_in_h_units"),
        })
        previous = row
    new_count = len(new_rows)
    return {
        "status": STATUS,
        "physical_coordinate_scale": "h=2^-4296",
        "inherited_round152_result_sha256": digest(inherited),
        "certified_abs_delta_x_corridor_in_h_units": ["0", "160"],
        "new_endpoint_continuation": {
            "new_typed_slab_count": new_count,
            "new_typed_box_count": 3 * new_count,
            "new_rows": new_rows,
            "new_rows_sha256": digest(new_rows),
            "lower_axis_connection": lower_connections,
            "upper_exact_face_adjacencies": upper_adjacencies,
            "lower_endpoint_is_abs_delta_x_symmetry_axis": True,
            "lower_endpoint_terminal_by_abs_coordinate_domain": True,
            "upper_endpoint_continuation_complete": False,
        },
        "combined_typed_atlas": {
            "slab_count": 21 + new_count,
            "typed_box_count": 3 * (21 + new_count),
            "connected": True,
            "interior_untyped_event_cell_count": 0,
            "boundary_event_families": [
                "COLLISION1648_TERMINAL_C24_P0_ZERO",
                "COLLISION3_D0_TANGENCY_D3_ZERO",
            ],
            "new_event_family_count": 0,
        },
        "audit_census": {
            "new_full_R1648_C24_audits": new_count,
            "new_full_R1648_bridge_audits": new_count,
            "new_collision_stage_object_pairs": 2 * new_count * 1648,
            "new_full_radius4_candidate_tests": 2 * new_count * 161 * 1648,
            "new_full_D3_event_box_audits": new_count,
        },
        "strict_nonpromotion": {
            "D02_status": "BLOCKED",
            "D03_authorized": False,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "continue the upper endpoint beyond abs(delta_x)/h=160 until a certified "
            "terminal exit or a newly typed event family is reached, and exclude disconnected exterior sheets"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build_result()
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    args.output.write_text(json.dumps(document, sort_keys=True, indent=2, ensure_ascii=False) + "\n")
    print(canonical({"status": "PASS", "output": str(args.output), "result_sha256": document["result_sha256"]}))


if __name__ == "__main__":
    main()
