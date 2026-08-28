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
OUTPUT = HERE / "cm2-round156-upper-endpoint-continuation-to-256h-2026-07-25.json"
SCHEMA = "cm2.round156.upper-endpoint-continuation-to-256h.v1"
STATUS = "CERTIFIED_TYPED_UPPER_ENDPOINT_CONTINUATION_TO_256H__D02_STILL_BLOCKED"
PINS = {
    "cm2_round151_dual_boundary_event_census_engine.py": "dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085",
    "cm2_round152_open_strip_bridge_engine.py": "21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738",
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


def check_pins():
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            name,
        )
    prior = strict_load(
        HERE / "cm2-round155-upper-endpoint-continuation-to-224h-2026-07-25.json"
    )
    verification = strict_load(
        HERE
        / "cm2-round155-upper-endpoint-continuation-to-224h-verification-2026-07-25.json"
    )
    require(prior["result_sha256"] == digest(prior["result"]), "prior digest")
    require(verification["result"]["status"] == "PASS", "prior verification")


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


def run_slab(row):
    c24_frontier = boundary_engine.c24_frontier(row["c24"])
    d3_frontier = boundary_engine.d3_frontier(row["d3"])
    c24_audit = boundary_engine.audit_c24_event_box(row["c24"])
    bridge_audit = bridge_engine.audit_bridge_cell(row["bridge"])
    d3_audit = boundary_engine.audit_d3_event_box(row["d3"])
    require(
        c24_audit["status"]
        == bridge_audit["status"]
        == d3_audit["status"]
        == "PASS",
        "audits",
    )
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


def strict_overlap(first, second):
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
        "C24_beta_overlap": strict_overlap(
            previous["c24_frontier"]["delta_beta_event_box_in_h_units"],
            row["c24_frontier"]["delta_beta_event_box_in_h_units"],
        ),
        "bridge_beta_overlap": strict_overlap(
            previous["strict_return_bridge"]["delta_beta_in_h_units"],
            row["strict_return_bridge"]["delta_beta_in_h_units"],
        ),
        "D3_beta_overlap": strict_overlap(
            previous["d3_frontier"]["delta_beta_event_box_in_h_units"],
            row["d3_frontier"]["delta_beta_event_box_in_h_units"],
        ),
    }


def build_result():
    check_pins()
    with ProcessPoolExecutor(max_workers=8) as pool:
        rows = normalize(list(pool.map(run_slab, specs(), chunksize=1)))
    rows.sort(key=lambda row: Q(row["abs_delta_x_in_h_units"][0]))
    prior = strict_load(
        HERE / "cm2-round155-upper-endpoint-continuation-to-224h-2026-07-25.json"
    )["result"]
    previous = prior["new_upper_continuation"]["new_rows"][-1]
    adjacencies = []
    for row in rows:
        adjacencies.append(adjacency(previous, row))
        previous = row
    require(
        rows[0]["abs_delta_x_in_h_units"][0] == "224"
        and rows[-1]["abs_delta_x_in_h_units"][1] == "256",
        "endpoints",
    )
    count = len(rows)
    return {
        "status": STATUS,
        "physical_coordinate_scale": "h=2^-4296",
        "inherited_round155_result_sha256": digest(prior),
        "certified_abs_delta_x_corridor_in_h_units": ["0", "256"],
        "new_upper_continuation": {
            "new_typed_slab_count": count,
            "new_typed_box_count": 3 * count,
            "new_rows": rows,
            "new_rows_sha256": digest(rows),
            "exact_face_adjacencies_from_224h_through_256h": adjacencies,
            "new_event_family_count": 0,
            "upper_endpoint_continuation_complete": False,
        },
        "combined_typed_atlas": {
            "slab_count": 41 + count,
            "typed_box_count": 3 * (41 + count),
            "connected": True,
            "interior_untyped_event_cell_count": 0,
            "lower_symmetry_axis_terminal": True,
            "upper_endpoint_in_h_units": "256",
            "upper_endpoint_terminal": False,
        },
        "audit_census": {
            "new_full_R1648_C24_audits": count,
            "new_full_R1648_bridge_audits": count,
            "new_collision_stage_object_pairs": 2 * count * 1648,
            "new_full_radius4_candidate_tests": 2 * count * 161 * 1648,
            "new_full_D3_event_box_audits": count,
        },
        "strict_nonpromotion": {
            "D02_status": "BLOCKED",
            "D03_authorized": False,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "continue beyond 256h with 4h C24-controlled slabs until terminal "
            "exit or typed new event, then exclude exterior sheets"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build_result()
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
