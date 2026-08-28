#!/usr/bin/env python3
import argparse
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from pathlib import Path

import cm2_round152_open_strip_bridge_engine as engine


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2-round152-open-strip-bridge-atlas-2026-07-24.json"
)
SCHEMA = "cm2.round152.open-strip-bridge-atlas.v1"
STATUS = (
    "CERTIFIED_63_BOX_TYPED_OPEN_STRIP_ATLAS_AND_INTERIOR_EVENT_EXHAUSTION"
    "_ON_X_CORRIDOR__D02_STILL_BLOCKED"
)
PINS = {
    "cm2_round152_open_strip_bridge_engine.py":
        "21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738",
    "cm2-round151-dual-boundary-event-census-2026-07-24.json":
        "593188b5e9996cfa8151cd15c318a7a6136c108dba123cc91e421c83f7aea821",
    "cm2-round151-dual-boundary-event-census-verification-2026-07-24.json":
        "61e053ca782cd030bb6d3a182e7ff4f032e4d6bb2fadf1fa82682789908ae1cd",
}
BRIDGE_TUPLES = [
    ("1", "2", "-403", "1"),
    ("2", "4", "-394", "4"),
    ("4", "8", "-380", "10"),
    ("8", "16", "-352", "21"),
    ("16", "32", "-290", "43"),
    ("32", "48", "-246", "88"),
    ("48", "64", "-201", "133"),
    ("64", "80", "-156", "178"),
    ("80", "96", "-111", "223"),
    ("96", "112", "-66", "268"),
    ("112", "128", "-21", "313"),
    ("128", "136", "-15", "358"),
    ("136", "140", "-10", "380"),
    ("140", "144", "2", "391"),
    ("144", "145", "1", "403"),
    ("145", "291/2", "0", "406"),
    ("291/2", "583/4", "0", "407"),
    ("583/4", "146", "1", "408"),
    ("146", "2337/16", "1", "408"),
    ("2337/16", "4675/32", "1", "408"),
    ("4675/32", "1169/8", "2", "409"),
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
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=reject,
    )
    require(type(value) is dict, "top object")
    return value


def check_pins():
    for name, expected in PINS.items():
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        require(actual == expected, f"pin mismatch:{name}")
    verification = strict_load(
        HERE
        / "cm2-round151-dual-boundary-event-census-verification-2026-07-24.json"
    )
    require(verification["result"]["status"] == "PASS", "Round151 verification")


def specs():
    return [{
        "abs_x_lower_h": abs_lower,
        "abs_x_upper_h": abs_upper,
        "beta_lower_h": beta_lower,
        "beta_upper_h": beta_upper,
    } for abs_lower, abs_upper, beta_lower, beta_upper in BRIDGE_TUPLES]


def run_spec(index_spec):
    slab_index, spec = index_spec
    return {
        "slab_index": slab_index,
        "spec": spec,
        **engine.audit_bridge_cell(spec),
    }


def build_result():
    check_pins()
    all_specs = specs()
    with ProcessPoolExecutor(max_workers=len(all_specs)) as pool:
        rows = normalize(list(pool.map(
            run_spec,
            enumerate(all_specs, start=1),
            chunksize=1,
        )))
    rows.sort(key=lambda row: row["slab_index"])
    require(len(rows) == 21, "bridge count")
    require(
        rows[0]["abs_delta_x_in_h_units"][0] == "1"
        and rows[-1]["abs_delta_x_in_h_units"][1] == "1169/8",
        "bridge endpoints",
    )
    official_hashes = set()
    compact_hashes = set()
    bridge_adjacency = []
    for row in rows:
        require(
            row["status"] == "PASS"
            and row["collision_count"] == 1648
            and row["full_radius4_candidate_test_count"] == 265328,
            "bridge full audit",
        )
        require(
            row["terminal_classification"] == "RETURN_AT_3_INNER"
            and row["terminal_destination_core"]
            == engine.r139.EXPECTED_DESTINATION_CORE_ID,
            "bridge terminal return",
        )
        require(
            row["collision3_physical_anchor_exclusion"][
                "D3_maximum_strict_negative"
            ] is True,
            "bridge anchor exclusion",
        )
        retained = row["collision3_retained_candidate_audit"]
        full = row["collision3_full_radius4_candidate_audit"]
        require(
            retained["candidate_count"] == 57
            and full["candidate_count"] == 161
            and retained["selected_target_id"]
            == full["selected_target_id"]
            == "W[0,-1]",
            "bridge collision3 census",
        )
        require(
            row["terminal_event_non_event_core_audit"][
                "all_other_core_constraints_strict"
            ] is True
            and row["terminal_return_monotonicity"][
                "terminal_event_strict_positive_on_entire_bridge"
            ] is True,
            "bridge terminal forcing",
        )
        official_hashes.add(row["official_sequence_sha256"])
        compact_hashes.add(row["compact_rows_sha256"])
    require(len(official_hashes) == 1, "official path")
    require(len(compact_hashes) == 1, "compact path")
    for left, right in zip(rows, rows[1:]):
        require(
            left["abs_delta_x_in_h_units"][1]
            == right["abs_delta_x_in_h_units"][0],
            "bridge exact x face",
        )
        lower = max(
            Q(left["delta_beta_in_h_units"][0]),
            Q(right["delta_beta_in_h_units"][0]),
        )
        upper = min(
            Q(left["delta_beta_in_h_units"][1]),
            Q(right["delta_beta_in_h_units"][1]),
        )
        require(lower < upper, "bridge face overlap")
        bridge_adjacency.append({
            "left_bridge_cell_id": left["bridge_cell_id"],
            "right_bridge_cell_id": right["bridge_cell_id"],
            "shared_face_abs_delta_x_in_h_units":
                left["abs_delta_x_in_h_units"][1],
            "overlapping_delta_beta_interval_in_h_units": [
                engine.r139.qstr(lower),
                engine.r139.qstr(upper),
            ],
            "kind": "EXACT_X_FACE_WITH_STRICT_BETA_OVERLAP",
        })
    r151 = strict_load(
        HERE
        / "cm2-round151-dual-boundary-event-census-2026-07-24.json"
    )["result"]
    c24_rows = r151["lower_terminal_C24_boundary_graph"]["event_box_rows"]
    d3_rows = r151["upper_collision3_D3_boundary_graph"]["event_box_rows"]
    require(len(c24_rows) == len(d3_rows) == len(rows), "boundary rows")
    boundary_attachments = []
    slab_cover_rows = []
    for bridge, c24, d3 in zip(rows, c24_rows, d3_rows):
        c24_frontier = c24["frontier"]
        d3_frontier = d3["frontier"]
        require(
            bridge["abs_delta_x_in_h_units"]
            == c24_frontier["abs_delta_x_in_h_units"]
            == d3_frontier["abs_delta_x_in_h_units"],
            "aligned x slab",
        )
        require(
            bridge["delta_beta_in_h_units"][0]
            == c24_frontier["delta_beta_event_box_in_h_units"][1],
            "C24 bridge face",
        )
        require(
            bridge["delta_beta_in_h_units"][1]
            == d3_frontier["delta_beta_event_box_in_h_units"][0],
            "D3 bridge face",
        )
        boundary_attachments.extend([
            {
                "event_box_id": c24_frontier["event_box_id"],
                "bridge_cell_id": bridge["bridge_cell_id"],
                "shared_beta_face_in_h_units":
                    bridge["delta_beta_in_h_units"][0],
                "abs_delta_x_face_interval_in_h_units":
                    bridge["abs_delta_x_in_h_units"],
                "kind": "LOWER_C24_EVENT_BOX_TO_RETURN_BRIDGE",
            },
            {
                "bridge_cell_id": bridge["bridge_cell_id"],
                "event_box_id": d3_frontier["event_box_id"],
                "shared_beta_face_in_h_units":
                    bridge["delta_beta_in_h_units"][1],
                "abs_delta_x_face_interval_in_h_units":
                    bridge["abs_delta_x_in_h_units"],
                "kind": "RETURN_BRIDGE_TO_UPPER_D3_EVENT_BOX",
            },
        ])
        slab_cover_rows.append({
            "slab_index": bridge["slab_index"],
            "abs_delta_x_in_h_units": bridge["abs_delta_x_in_h_units"],
            "lower_C24_event_box_beta_in_h_units":
                c24_frontier["delta_beta_event_box_in_h_units"],
            "strict_return_bridge_beta_in_h_units":
                bridge["delta_beta_in_h_units"],
            "upper_D3_event_box_beta_in_h_units":
                d3_frontier["delta_beta_event_box_in_h_units"],
            "vertical_chain_has_no_gap": True,
            "actual_graph_to_graph_strip_covered_by_typed_boxes": True,
        })
    require(
        len(bridge_adjacency) == 20
        and len(boundary_attachments) == 42,
        "atlas adjacency counts",
    )
    new_tests = len(rows) * 161 * 1648
    return {
        "status": STATUS,
        "physical_coordinate_scale": "h=2^-4296",
        "physical_generators": ["delta_x", "delta_beta"],
        "certified_abs_delta_x_corridor_in_h_units": ["1", "1169/8"],
        "typed_open_strip_atlas": {
            "inherited_lower_C24_event_box_count": len(c24_rows),
            "new_strict_return_bridge_cell_count": len(rows),
            "inherited_upper_D3_event_box_count": len(d3_rows),
            "total_typed_box_count": len(c24_rows) + len(rows) + len(d3_rows),
            "strict_return_bridge_rows": rows,
            "strict_return_bridge_rows_sha256": digest(rows),
            "bridge_exact_x_face_adjacency_rows": bridge_adjacency,
            "bridge_exact_x_face_adjacency_rows_sha256":
                digest(bridge_adjacency),
            "boundary_attachment_rows": boundary_attachments,
            "boundary_attachment_rows_sha256": digest(boundary_attachments),
            "per_slab_vertical_cover_rows": slab_cover_rows,
            "per_slab_vertical_cover_rows_sha256": digest(slab_cover_rows),
            "inherited_boundary_graph_x_adjacency_count": 40,
            "new_bridge_x_adjacency_count": len(bridge_adjacency),
            "new_boundary_attachment_count": len(boundary_attachments),
            "connected_typed_atlas": True,
            "actual_graph_to_graph_strip_fully_covered": True,
        },
        "interior_event_exhaustion": {
            "collision3_anchor_D3_strict_negative_on_every_bridge": True,
            "collision3_all_160_nonanchor_radius4_candidates_strict_on_every_bridge":
                True,
            "collision3_frozen_winner_on_every_bridge": "W[0,-1]",
            "all_other_collision_stage_radius4_candidate_decisions_strict":
                True,
            "all_official_wall_chart_homogeneity_incidence_constraints_strict":
                True,
            "all_preterminal_core_constraints_strict": True,
            "all_terminal_non_event_core_constraints_strict": True,
            "terminal_event_beta_derivative_strict_positive_on_every_bridge":
                True,
            "terminal_event_positive_on_every_bridge": True,
            "terminal_classification_on_every_bridge": "RETURN_AT_3_INNER",
            "untyped_interior_event_cell_count": 0,
            "interior_competing_event_surface_count": 0,
            "boundary_event_families": [
                "COLLISION1648_TERMINAL_C24_P0_ZERO",
                "COLLISION3_D0_TANGENCY_D3_ZERO",
            ],
            "boundary_event_families_typed_by_Round151": True,
        },
        "audit_census": {
            "new_full_R1648_bridge_audit_count": len(rows),
            "new_collision_stage_bridge_pairs": len(rows) * 1648,
            "new_full_radius4_candidate_tests": new_tests,
            "collision3_additional_retained_candidate_tests":
                len(rows) * 57,
            "official_sequence_sha256": next(iter(official_hashes)),
            "compact_rows_sha256": next(iter(compact_hashes)),
        },
        "Round151_upgrade": {
            "previous_two_boundary_graphs_only": True,
            "current_graph_to_graph_strip_fully_typed": True,
            "current_untyped_interior_event_cell_count": 0,
            "all_beta_direction_exits_typed_on_certified_x_corridor": True,
            "endpoint_continuation_beyond_certified_x_corridor_complete": False,
        },
        "Round144_DAG_effect": {
            "D02_status_before": "BLOCKED",
            "D02_status_after": "BLOCKED",
            "D02_progress":
                "the complete C24-to-D3 strip is now a finite connected typed atlas with no untyped interior event cells on the certified x corridor",
            "remaining_D02_blocker":
                "continuation beyond both x-corridor endpoints and proof that no additional maximal-component sheets lie outside the certified corridor remain incomplete",
            "D03_least_rank_negative_oracle_authorized": False,
        },
        "strict_nonpromotion": {
            "least_2d_basis_rank_of_maximal_component": None,
            "component_v1_id": None,
            "parent_W_v1_id": None,
            "restriction_v1_id": None,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "the typed strip atlas is restricted to the certified x corridor",
            "neither x endpoint is claimed to be a terminal maximal-component exit",
            "additional disconnected or exterior component sheets are not excluded",
            "Round144 D02 remains blocked and D03 remains unauthorized",
            "no versioned component, parent-W, restriction, Gate5 block, or CM2 theorem is minted",
        ],
        "upstream_sha256": {**PINS, **engine.PINS},
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
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )
    print(canonical({
        "status": result["status"],
        "output": str(args.output),
        "result_sha256": document["result_sha256"],
    }))


if __name__ == "__main__":
    main()
