#!/usr/bin/env python3
import argparse
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from pathlib import Path

import cm2_round150_connected_2d_corridor_engine as engine


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2-round150-connected-2d-corridor-atlas-2026-07-24.json"
)
SCHEMA = "cm2.round150.connected-2d-corridor-atlas.v1"
STATUS = (
    "CERTIFIED_CONNECTED_PHYSICAL_2D_CORRIDOR_AND_UNIQUE_TERMINAL_C24_GRAPH"
    "__D02_STILL_BLOCKED"
)
PINS = {
    "cm2_round150_connected_2d_corridor_engine.py":
        "4d80a8e3cef5e3e754e1b10221716239bc123aa228c6ab27a30b9fc76af336fc",
    "cm2-round146-physical-centered-jet-2d-frontier-2026-07-24.json":
        "38ad7cdd5a2af7cda94792a31a8a83275022f943e8e6b9801ee4bece73b04eac",
    "cm2-round146-physical-centered-jet-2d-frontier-verification-2026-07-24.json":
        "c25646413467deb2c1c5ea68f92e97116546eb62333596afc61973430e002dd4",
    "cm2-round148-atomic-future-input-admission-2026-07-24.json":
        "7ab3a83998b34811f6af38ea50630a94a3a32a3e43f889b75331e2db716800e3",
    "cm2-round148-atomic-future-input-admission-verification-2026-07-24.json":
        "dacaf48cb0ae968983ce28dd1006f11fc7ebfc1a24c2b2bd2589b72ffd4c6842",
    "cm2-round149-terminal-c24-two-sided-frontier-2026-07-24.json":
        "4748f90bee1c8f82a79fa7aeb936d9e13d766ad456cb95bf7f792e41107c53b7",
    "cm2-round149-terminal-c24-two-sided-frontier-verification-2026-07-24.json":
        "c668db505c6be2c6c06e25d2610a68c68c7a38c0f6dec393b19c826969fd071a",
}
REGULAR_SPECS = [
    {
        "role": "return_02_04",
        "x_power": 4295,
        "x_cell_index": 1,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_04_08",
        "x_power": 4294,
        "x_cell_index": 1,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_08_16",
        "x_power": 4293,
        "x_cell_index": 1,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_16_32",
        "x_power": 4292,
        "x_cell_index": 1,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_32_64",
        "x_power": 4291,
        "x_cell_index": 1,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_64_96",
        "x_power": 4291,
        "x_cell_index": 2,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_96_128",
        "x_power": 4291,
        "x_cell_index": 3,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_128_136",
        "x_power": 4293,
        "x_cell_index": 16,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_136_140",
        "x_power": 4294,
        "x_cell_index": 34,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_140_144",
        "x_power": 4294,
        "x_cell_index": 35,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_144_145",
        "x_power": 4296,
        "x_cell_index": 144,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_145_145p5",
        "x_power": 4297,
        "x_cell_index": 290,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_145p5_145p75",
        "x_power": 4298,
        "x_cell_index": 582,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_145p75_146",
        "x_power": 4298,
        "x_cell_index": 583,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_146_146p0625",
        "x_power": 4300,
        "x_cell_index": 2336,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "return_146p0625_146p09375",
        "x_power": 4301,
        "x_cell_index": 4674,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "RETURN_AT_3_INNER",
        "precision": 8192,
    },
    {
        "role": "survive_146p125_146p12890625",
        "x_power": 4304,
        "x_cell_index": 37408,
        "beta_power": 4304,
        "beta_cell_index": 0,
        "expected_terminal_classification": "SURVIVE_THROUGH_3_INNER",
        "precision": 8192,
    },
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
    for name in (
        "cm2-round146-physical-centered-jet-2d-frontier-verification-2026-07-24.json",
        "cm2-round148-atomic-future-input-admission-verification-2026-07-24.json",
        "cm2-round149-terminal-c24-two-sided-frontier-verification-2026-07-24.json",
    ):
        document = strict_load(HERE / name)
        require(document["result"]["status"] == "PASS", f"verification:{name}")


def spec_abs_bounds_in_h(spec):
    width = Q(2) ** (engine.POWER - spec["x_power"])
    lower = spec["x_cell_index"] * width
    return lower, lower + width


def run_spec(spec):
    row = engine.audit_regular_cell(spec)
    lower, upper = spec_abs_bounds_in_h(spec)
    return {
        "role": spec["role"],
        "cell_id": "round150-regular-2d-cell:" + digest({
            "role": spec["role"],
            "x_power": spec["x_power"],
            "x_cell_index": spec["x_cell_index"],
            "beta_power": spec["beta_power"],
            "beta_cell_index": spec["beta_cell_index"],
            "terminal": spec["expected_terminal_classification"],
        }),
        "abs_delta_x_in_h_units": [
            engine.r139.qstr(lower),
            engine.r139.qstr(upper),
        ],
        "delta_beta_in_h_units": ["-1/256", "1/256"],
        **row,
    }


def build_result():
    check_pins()
    with ProcessPoolExecutor(max_workers=len(REGULAR_SPECS) + 1) as pool:
        regular_future = pool.map(run_spec, REGULAR_SPECS)
        event_future = pool.submit(engine.audit_terminal_event_box)
        regular = list(regular_future)
        event_audit = event_future.result()
    regular.sort(key=lambda row: Q(row["abs_delta_x_in_h_units"][0]))
    return_rows = [
        row
        for row in regular
        if row["terminal_classification"] == "RETURN_AT_3_INNER"
    ]
    survive_rows = [
        row
        for row in regular
        if row["terminal_classification"] == "SURVIVE_THROUGH_3_INNER"
    ]
    require(len(return_rows) == 16 and len(survive_rows) == 1, "regular census")
    require(
        Q(return_rows[0]["abs_delta_x_in_h_units"][0]) == Q(2),
        "corridor left endpoint",
    )
    for left, right in zip(return_rows, return_rows[1:]):
        require(
            left["abs_delta_x_in_h_units"][1]
            == right["abs_delta_x_in_h_units"][0],
            "return corridor exact face",
        )
    require(
        return_rows[-1]["abs_delta_x_in_h_units"][1] == "4675/32",
        "return corridor event attachment",
    )
    require(
        survive_rows[0]["abs_delta_x_in_h_units"][0] == "1169/8",
        "survive corridor event attachment",
    )
    official_hashes = {
        row["official_sequence_sha256"]
        for row in regular
    } | {event_audit["official_sequence_sha256"]}
    require(len(official_hashes) == 1, "same official path")
    event_frontier = engine.terminal_event_frontier()
    r146 = strict_load(
        HERE
        / "cm2-round146-physical-centered-jet-2d-frontier-2026-07-24.json"
    )["result"]
    r149 = strict_load(
        HERE
        / "cm2-round149-terminal-c24-two-sided-frontier-2026-07-24.json"
    )["result"]
    d3 = r146["positive_transverse_event_frontier"]
    require(
        d3["unique_beta_root_for_every_fixed_delta_x"] is True
        and d3["event_curve_is_local_not_exhaustive_global_frontier"] is True,
        "Round146 D3 frontier",
    )
    adjacency = [{
        "left": r146["local_connected_two_cell_atlas"]["cells"][1]["cell_id"],
        "right": return_rows[0]["cell_id"],
        "shared_face_abs_delta_x_in_h_units": "2",
        "shared_face_delta_beta_in_h_units": ["-1/256", "1/256"],
        "kind": "UPSTREAM_CENTRAL_CELL_TO_REFINED_CORRIDOR",
    }]
    adjacency.extend({
        "left": left["cell_id"],
        "right": right["cell_id"],
        "shared_face_abs_delta_x_in_h_units":
            left["abs_delta_x_in_h_units"][1],
        "shared_face_delta_beta_in_h_units": ["-1/256", "1/256"],
        "kind": "EXACT_ARTIFICIAL_DYADIC_FACE",
    } for left, right in zip(return_rows, return_rows[1:]))
    adjacency.append({
        "left": return_rows[-1]["cell_id"],
        "right": event_frontier["terminal_event_graph_id"],
        "shared_face_abs_delta_x_in_h_units": "4675/32",
        "shared_face_delta_beta_in_h_units": ["-1/256", "1/256"],
        "kind": "RETURN_CELL_TO_EVENT_BOX",
    })
    adjacency.append({
        "left": event_frontier["terminal_event_graph_id"],
        "right": survive_rows[0]["cell_id"],
        "shared_face_abs_delta_x_in_h_units": "1169/8",
        "shared_face_delta_beta_in_h_units": ["-1/256", "1/256"],
        "kind": "EVENT_BOX_TO_SURVIVE_CELL",
    })
    require(len(adjacency) == 18, "adjacency count")
    audited_object_count = len(regular) + 1
    tests_per_object = 161 * 1648
    return {
        "status": STATUS,
        "physical_coordinate_scale": "h=2^-4296",
        "physical_generators": ["delta_x", "delta_beta"],
        "upstream_seed_attachment": {
            "Round146_central_cell_id":
                r146["local_connected_two_cell_atlas"]["cells"][1]["cell_id"],
            "Round146_central_cell_abs_delta_x_in_h_units": ["1", "2"],
            "Round146_central_cell_delta_beta_in_h_units": ["-1", "1"],
            "new_corridor_shares_exact_face_at_abs_delta_x_in_h_units": "2",
        },
        "connected_regular_corridor": {
            "shared_delta_beta_strip_in_h_units": ["-1/256", "1/256"],
            "new_regular_cell_count": len(regular),
            "strict_return_cell_count": len(return_rows),
            "strict_survive_cell_count": len(survive_rows),
            "regular_cell_rows": regular,
            "regular_cell_rows_sha256": digest(regular),
            "return_side_abs_delta_x_union_in_h_units":
                ["2", "4675/32"],
            "survive_side_abs_delta_x_interval_in_h_units":
                survive_rows[0]["abs_delta_x_in_h_units"],
            "exact_face_adjacency_rows": adjacency,
            "exact_face_adjacency_rows_sha256": digest(adjacency),
            "connected_to_Round146_central_cell": True,
            "connected_through_terminal_event_box": True,
        },
        "terminal_C24_event_box_full_audit": event_audit,
        "terminal_C24_unique_event_graph": event_frontier,
        "Round149_upgrade": {
            "previous_strict_unclassified_x_gap_in_h_units":
                r149["strict_unclassified_x_gap_in_h_units"],
            "current_unclassified_x_gap_in_event_box": None,
            "all_beta_fibres_in_shared_strip_have_unique_root": True,
            "continuity_only_frontier_replaced_by_parametric_interval_Newton_graph":
                True,
        },
        "joined_local_frontier_skeleton": {
            "collision3_D0_event_kind": d3["event_kind"],
            "collision3_D0_event_frontier_sha256": digest(d3),
            "terminal_C24_event_kind": event_frontier["event_kind"],
            "terminal_C24_event_graph_id":
                event_frontier["terminal_event_graph_id"],
            "both_frontier_types_attached_to_one_connected_certified_skeleton":
                True,
            "collision3_to_seed_attachment_uses_Round146_monotone_D3_corridor":
                True,
            "seed_to_terminal_attachment_uses_new_full_R1648_corridor":
                True,
        },
        "audit_census": {
            "new_full_R1648_audited_object_count": audited_object_count,
            "new_collision_stage_object_pairs":
                audited_object_count * 1648,
            "full_radius4_candidate_tests_per_object": tests_per_object,
            "new_full_radius4_candidate_tests_total":
                audited_object_count * tests_per_object,
            "same_complete_owner_word_chart_homogeneity_incidence_path": True,
            "official_sequence_sha256": next(iter(official_hashes)),
            "terminal_classification_census": {
                "RETURN_AT_3_INNER": 16,
                "UNRESOLVED_TIME3_OUTER_EVENT_BOX": 1,
                "SURVIVE_THROUGH_3_INNER": 1,
            },
        },
        "Round144_DAG_effect": {
            "D02_status_before": "BLOCKED",
            "D02_status_after": "BLOCKED",
            "D02_progress":
                "connected physical 2D corridor and unique terminal C24 graph certified",
            "remaining_D02_blocker":
                "maximal-component beta extent, every component exit, and every competing physical event family are not exhausted",
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
            "the connected corridor is not claimed to be the maximal two-dimensional component",
            "the narrow beta strip does not exhaust the component beta extent",
            "the collision-three and terminal-C24 graphs do not exhaust every competing event family",
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
