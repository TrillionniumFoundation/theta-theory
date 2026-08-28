#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from pathlib import Path

import cm2_round151_dual_boundary_event_census_engine as engine


HERE = Path(__file__).resolve().parent
CERTIFICATE = (
    HERE
    / "cm2-round151-dual-boundary-event-census-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round151-dual-boundary-event-census-verification-2026-07-24.json"
)
CERT_SCHEMA = "cm2.round151.dual-boundary-event-census.v1"
SCHEMA = "cm2.round151.dual-boundary-event-census-verification.v1"
STATUS = (
    "CERTIFIED_GLOBAL_DUAL_EVENT_GRAPH_CENSUS_ON_CONNECTED_X_CORRIDOR"
    "__D02_STILL_BLOCKED"
)
CERT_UPSTREAM_PINS = {
    "cm2_round151_dual_boundary_event_census_engine.py":
        "dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085",
    "cm2-round150-connected-2d-corridor-atlas-2026-07-24.json":
        "6bb182760205190ad635ef34c21eca6221d2224e2dcdb585f70c157fad76321c",
    "cm2-round150-connected-2d-corridor-atlas-verification-2026-07-24.json":
        "686e236dbe998c111a0307e3edfd34d0b26185b6f52ec54fa33e340725655ee5",
}
VERIFIER_PINS = {
    **CERT_UPSTREAM_PINS,
    "cm2_round151_dual_boundary_event_census.py":
        "16eac5a2f8974b8908fc2c4f66c1c6625ae2f7b9da31750c47dd715c8b100acb",
}
SPEC_ROWS = [
    ("1", "2", "-409", "-403", "1", "7"),
    ("2", "4", "-409", "-394", "4", "13"),
    ("4", "8", "-406", "-380", "10", "24"),
    ("8", "16", "-401", "-352", "21", "46"),
    ("16", "32", "-395", "-290", "43", "91"),
    ("32", "48", "-350", "-246", "88", "136"),
    ("48", "64", "-305", "-201", "133", "181"),
    ("64", "80", "-260", "-156", "178", "226"),
    ("80", "96", "-215", "-111", "223", "271"),
    ("96", "112", "-170", "-66", "268", "316"),
    ("112", "128", "-126", "-21", "313", "361"),
    ("128", "136", "-64", "-15", "358", "383"),
    ("136", "140", "-36", "-10", "380", "395"),
    ("140", "144", "-25", "2", "391", "406"),
    ("144", "145", "-10", "1", "403", "409"),
    ("145", "291/2", "-5", "0", "406", "410"),
    ("291/2", "583/4", "-3", "0", "407", "411"),
    ("583/4", "146", "-3", "1", "408", "411"),
    ("146", "2337/16", "-2", "1", "408", "412"),
    ("2337/16", "4675/32", "-2", "1", "408", "412"),
    ("4675/32", "1169/8", "-2", "2", "409", "412"),
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
        raise ValueError(label)


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
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=reject,
    )
    require(type(value) is dict, "top object")
    return value


def strict_load(path):
    return strict_load_raw(path.read_bytes())


def check_pins():
    for name, expected in VERIFIER_PINS.items():
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        require(actual == expected, f"pin mismatch:{name}")
    verification = strict_load(
        HERE
        / "cm2-round150-connected-2d-corridor-atlas-verification-2026-07-24.json"
    )
    require(verification["result"]["status"] == "PASS", "Round150 verification")


def independent_specs():
    c24 = []
    d3 = []
    for row in SPEC_ROWS:
        abs_lower, abs_upper, c24_lower, c24_upper, d3_lower, d3_upper = row
        c24.append({
            "abs_x_lower_h": abs_lower,
            "abs_x_upper_h": abs_upper,
            "beta_lower_h": c24_lower,
            "beta_upper_h": c24_upper,
        })
        d3.append({
            "abs_x_lower_h": abs_lower,
            "abs_x_upper_h": abs_upper,
            "beta_lower_h": d3_lower,
            "beta_upper_h": d3_upper,
        })
    return c24, d3


def reconstruct_job(job):
    family, slab_index, spec = job
    if family == "C24":
        frontier = engine.c24_frontier(spec)
        audit = engine.audit_c24_event_box(spec)
    else:
        require(family == "D3", "job family")
        frontier = engine.d3_frontier(spec)
        audit = engine.audit_d3_event_box(spec)
    require(frontier["event_box_id"] == audit["event_box_id"], "event id")
    return {
        "slab_index": slab_index,
        "spec": spec,
        "frontier": frontier,
        "full_audit": audit,
    }


def adjacency_for(rows, family):
    result = []
    for left, right in zip(rows, rows[1:]):
        left_frontier = left["frontier"]
        right_frontier = right["frontier"]
        require(
            left_frontier["abs_delta_x_in_h_units"][1]
            == right_frontier["abs_delta_x_in_h_units"][0],
            f"{family} x face",
        )
        left_beta = left_frontier["delta_beta_event_box_in_h_units"]
        right_beta = right_frontier["delta_beta_event_box_in_h_units"]
        lower = max(Q(left_beta[0]), Q(right_beta[0]))
        upper = min(Q(left_beta[1]), Q(right_beta[1]))
        require(lower < upper, f"{family} beta overlap")
        result.append({
            "left_event_box_id": left_frontier["event_box_id"],
            "right_event_box_id": right_frontier["event_box_id"],
            "shared_face_abs_delta_x_in_h_units":
                left_frontier["abs_delta_x_in_h_units"][1],
            "overlapping_event_beta_boxes_on_shared_face_in_h_units": [
                engine.r139.qstr(lower),
                engine.r139.qstr(upper),
            ],
            "same_event_function_and_unique_root_force_graph_connection": True,
        })
    return result


def verify_c24_rows(rows):
    require(len(rows) == 21, "C24 count")
    official_hashes = set()
    unresolved_cores = set()
    for row in rows:
        frontier = row["frontier"]
        audit = row["full_audit"]
        terminal = audit["terminal_event"]
        require(
            audit["status"] == "PASS"
            and audit["collision_count"] == 1648
            and audit["full_radius4_candidate_test_count"] == 265328,
            "C24 full audit",
        )
        require(
            frontier["event_kind"] == "COLLISION1648_TERMINAL_C24_P0_ZERO"
            and frontier["unique_beta_root_for_every_fixed_delta_x"] is True
            and frontier["both_partial_derivatives_strict_positive"] is True,
            "C24 graph",
        )
        require(
            terminal["classification"] == "UNRESOLVED_TIME3_OUTER"
            and terminal["all_other_core_constraints_strict"] is True
            and terminal["sole_unresolved_core"]
            == frontier["sole_unresolved_terminal_core"],
            "C24 terminal core",
        )
        official_hashes.add(audit["official_sequence_sha256"])
        unresolved_cores.add(terminal["sole_unresolved_core"])
    require(len(official_hashes) == len(unresolved_cores) == 1, "C24 identity")
    return next(iter(official_hashes)), next(iter(unresolved_cores))


def verify_d3_rows(rows):
    require(len(rows) == 21, "D3 count")
    for row in rows:
        frontier = row["frontier"]
        audit = row["full_audit"]
        require(
            audit["status"] == "PASS"
            and audit["collision3_anchor_is_immediate_owner_switch"] is True,
            "D3 audit",
        )
        require(
            frontier["event_kind"] == "COLLISION3_D0_TANGENCY_D3_ZERO"
            and frontier["anchor_candidate"] == "W[0,0]"
            and frontier["unique_beta_root_for_every_fixed_delta_x"] is True
            and frontier["D3_strictly_increasing_in_delta_x"] is True
            and frontier["D3_strictly_increasing_in_delta_beta"] is True,
            "D3 graph",
        )
        retained = audit["collision3_retained_candidate_event_census"]
        full = audit["collision3_full_radius4_candidate_event_census"]
        require(
            retained["candidate_count"] == 57
            and full["candidate_count"] == 161,
            "D3 candidate counts",
        )
        for census in (retained, full):
            require(
                census["sole_unresolved_candidate"] == "W[0,0]"
                and census["sole_unresolved_event"] == "D3=0"
                and census["frozen_winner_excluding_anchor"] == "W[0,-1]"
                and census[
                    "anchor_double_root_strictly_preempts_frozen_winner"
                ] is True,
                "D3 preemption",
            )
        require(
            audit["fully_audited_prefix_radius4_candidate_test_count"] == 322
            and audit["collision3_full_radius4_candidate_test_count"] == 161,
            "D3 tests",
        )


def reconstruct():
    check_pins()
    c24_specs, d3_specs = independent_specs()
    jobs = [
        ("C24", index, spec)
        for index, spec in enumerate(c24_specs, start=1)
    ] + [
        ("D3", index, spec)
        for index, spec in enumerate(d3_specs, start=1)
    ]
    with ProcessPoolExecutor(max_workers=len(jobs)) as pool:
        rows = normalize(list(pool.map(reconstruct_job, jobs, chunksize=1)))
    c24_rows = sorted(
        (row for row in rows if row["frontier"]["event_kind"].startswith(
            "COLLISION1648"
        )),
        key=lambda row: row["slab_index"],
    )
    d3_rows = sorted(
        (row for row in rows if row["frontier"]["event_kind"].startswith(
            "COLLISION3_"
        )),
        key=lambda row: row["slab_index"],
    )
    require(
        c24_rows[0]["frontier"]["abs_delta_x_in_h_units"][0] == "1"
        and c24_rows[-1]["frontier"]["abs_delta_x_in_h_units"][1] == "1169/8",
        "C24 endpoints",
    )
    require(
        d3_rows[0]["frontier"]["abs_delta_x_in_h_units"][0] == "1"
        and d3_rows[-1]["frontier"]["abs_delta_x_in_h_units"][1] == "1169/8",
        "D3 endpoints",
    )
    official_hash, unresolved_core = verify_c24_rows(c24_rows)
    verify_d3_rows(d3_rows)
    c24_adjacency = adjacency_for(c24_rows, "C24")
    d3_adjacency = adjacency_for(d3_rows, "D3")
    separation_rows = []
    for c24_row, d3_row in zip(c24_rows, d3_rows):
        require(
            c24_row["slab_index"] == d3_row["slab_index"]
            and c24_row["frontier"]["abs_delta_x_in_h_units"]
            == d3_row["frontier"]["abs_delta_x_in_h_units"],
            "aligned slabs",
        )
        c24_newton = c24_row["frontier"][
            "parametric_interval_newton_beta_in_h_units_outer"
        ]
        d3_newton = d3_row["frontier"][
            "parametric_interval_newton_beta_in_h_units_outer"
        ]
        separation = Q(d3_newton[0]) - Q(c24_newton[1])
        require(separation > 300, "graph separation")
        separation_rows.append({
            "slab_index": c24_row["slab_index"],
            "abs_delta_x_in_h_units":
                c24_row["frontier"]["abs_delta_x_in_h_units"],
            "lower_C24_newton_upper_in_h_units": c24_newton[1],
            "upper_D3_newton_lower_in_h_units": d3_newton[0],
            "certified_graph_separation_lower_bound_in_h_units":
                engine.r139.qstr(separation),
        })
    minimum_separation = min(
        Q(row["certified_graph_separation_lower_bound_in_h_units"])
        for row in separation_rows
    )
    r150 = strict_load(
        HERE / "cm2-round150-connected-2d-corridor-atlas-2026-07-24.json"
    )["result"]
    require(r150["status"].endswith("__D02_STILL_BLOCKED"), "Round150")
    c24_test_count = len(c24_rows) * 265328
    d3_test_count = len(d3_rows) * 483
    return {
        "status": STATUS,
        "physical_coordinate_scale": "h=2^-4296",
        "physical_generators": ["delta_x", "delta_beta"],
        "certified_abs_delta_x_corridor_in_h_units": ["1", "1169/8"],
        "aligned_abs_delta_x_slab_count": len(c24_rows),
        "lower_terminal_C24_boundary_graph": {
            "role": "LOWER_BETA_BOUNDARY",
            "event_kind": "COLLISION1648_TERMINAL_C24_P0_ZERO",
            "event_box_rows": c24_rows,
            "event_box_rows_sha256": digest(c24_rows),
            "exact_face_graph_adjacency_rows": c24_adjacency,
            "exact_face_graph_adjacency_rows_sha256": digest(c24_adjacency),
            "event_box_count": len(c24_rows),
            "exact_face_graph_adjacency_count": len(c24_adjacency),
            "unique_beta_root_on_every_fixed_x_fibre": True,
            "globally_face_connected_over_certified_x_corridor": True,
            "sole_unresolved_terminal_core": unresolved_core,
            "all_other_terminal_constraints_strict_on_every_box": True,
            "official_sequence_sha256": official_hash,
        },
        "upper_collision3_D3_boundary_graph": {
            "role": "UPPER_BETA_BOUNDARY",
            "event_kind": "COLLISION3_D0_TANGENCY_D3_ZERO",
            "event_box_rows": d3_rows,
            "event_box_rows_sha256": digest(d3_rows),
            "exact_face_graph_adjacency_rows": d3_adjacency,
            "exact_face_graph_adjacency_rows_sha256": digest(d3_adjacency),
            "event_box_count": len(d3_rows),
            "exact_face_graph_adjacency_count": len(d3_adjacency),
            "unique_beta_root_on_every_fixed_x_fibre": True,
            "globally_face_connected_over_certified_x_corridor": True,
            "sole_unresolved_collision3_candidate": "W[0,0]",
            "frozen_winner_excluding_anchor": "W[0,-1]",
            "anchor_double_root_is_immediate_owner_switch_on_every_box": True,
            "all_other_radius4_candidate_decisions_strict_on_every_box": True,
        },
        "dual_boundary_strip": {
            "lower_graph": "COLLISION1648_TERMINAL_C24_P0_ZERO",
            "upper_graph": "COLLISION3_D0_TANGENCY_D3_ZERO",
            "aligned_slab_count": len(separation_rows),
            "separation_rows": separation_rows,
            "separation_rows_sha256": digest(separation_rows),
            "minimum_computed_parametric_newton_separation_lower_bound_in_h_units":
                engine.r139.qstr(minimum_separation),
            "certified_uniform_graph_separation_strict_lower_bound_in_h_units":
                "300",
            "two_unique_transverse_nonintersecting_graphs_over_full_x_corridor":
                True,
            "interior_region_between_graphs_fully_tiled": False,
            "all_possible_interior_event_surfaces_exhausted": False,
        },
        "Round150_upgrade": {
            "previous_frontier_skeleton_only": True,
            "current_C24_graph_continued_over_full_x_corridor": True,
            "current_D3_graph_continued_over_full_x_corridor": True,
            "both_local_boundary_families_now_global_on_certified_x_corridor": True,
            "endpoint_continuation_beyond_certified_x_corridor_complete": False,
        },
        "audit_census": {
            "C24_full_R1648_event_box_count": len(c24_rows),
            "C24_collision_stage_event_box_pairs": len(c24_rows) * 1648,
            "C24_full_radius4_candidate_tests": c24_test_count,
            "D3_event_box_count": len(d3_rows),
            "D3_collision_stage_event_box_pairs": len(d3_rows) * 3,
            "D3_full_radius4_candidate_tests": d3_test_count,
            "total_event_box_count": len(c24_rows) + len(d3_rows),
            "total_collision_stage_event_box_pairs":
                len(c24_rows) * 1648 + len(d3_rows) * 3,
            "total_full_radius4_candidate_tests":
                c24_test_count + d3_test_count,
        },
        "Round144_DAG_effect": {
            "D02_status_before": "BLOCKED",
            "D02_status_after": "BLOCKED",
            "D02_progress":
                "both first beta-direction boundary families are globally continued over the certified x corridor",
            "remaining_D02_blocker":
                "the open strip between the two graphs is not yet exhaustively tiled, interior competing event surfaces are not excluded, and endpoint continuation is incomplete",
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
            "the two boundary graphs do not prove that the intervening strip is event-free",
            "the certified x corridor is not claimed to exhaust either graph globally",
            "no complete maximal two-dimensional component atlas is claimed",
            "Round144 D02 remains blocked and D03 remains unauthorized",
            "no versioned component, parent-W, restriction, Gate5 block, or CM2 theorem is minted",
        ],
        "upstream_sha256": {**CERT_UPSTREAM_PINS, **engine.PINS},
    }


def validate_candidate(candidate, expected):
    require(
        set(candidate) == {"schema", "result", "result_sha256"},
        "envelope",
    )
    require(candidate["schema"] == CERT_SCHEMA, "schema")
    require(candidate["result"] == expected, "independent reconstruction")
    require(candidate["result_sha256"] == digest(expected), "result digest")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    require(
        args.certificate.is_file() and not args.certificate.is_symlink(),
        "certificate type",
    )
    certificate = strict_load(args.certificate)
    expected = reconstruct()
    validate_candidate(certificate, expected)
    labels = (
        "flip_C24_uniqueness",
        "delete_slab",
        "alter_graph_separation",
        "change_D3_anchor",
        "disable_preemption",
        "close_D02",
        "authorize_D03",
        "mint_component",
        "promote_Gate5",
        "claim_CM2",
    )
    rejected = []
    for label in labels:
        candidate = copy.deepcopy(certificate)
        result = candidate["result"]
        if label == "flip_C24_uniqueness":
            result["lower_terminal_C24_boundary_graph"][
                "unique_beta_root_on_every_fixed_x_fibre"
            ] = False
        elif label == "delete_slab":
            result["upper_collision3_D3_boundary_graph"][
                "event_box_rows"
            ].pop()
        elif label == "alter_graph_separation":
            result["dual_boundary_strip"][
                "certified_uniform_graph_separation_strict_lower_bound_in_h_units"
            ] = "500"
        elif label == "change_D3_anchor":
            result["upper_collision3_D3_boundary_graph"][
                "sole_unresolved_collision3_candidate"
            ] = "W[1,0]"
        elif label == "disable_preemption":
            result["upper_collision3_D3_boundary_graph"][
                "anchor_double_root_is_immediate_owner_switch_on_every_box"
            ] = False
        elif label == "close_D02":
            result["Round144_DAG_effect"]["D02_status_after"] = "CERTIFIED"
        elif label == "authorize_D03":
            result["Round144_DAG_effect"][
                "D03_least_rank_negative_oracle_authorized"
            ] = True
        elif label == "mint_component":
            result["strict_nonpromotion"]["component_v1_id"] = "component-v1:fake"
        elif label == "promote_Gate5":
            result["strict_nonpromotion"]["global_gate5_maturity"] = "18/18"
        else:
            result["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
        candidate["result_sha256"] = digest(result)
        try:
            validate_candidate(candidate, expected)
        except Exception:
            rejected.append(label)
    require(rejected == list(labels), "semantic mutation rejection")
    strict_attacks = [
        b'{"schema":"x","schema":"y"}\n',
        b"\xef\xbb\xbf{}\n",
        b"[1,2]\n",
        b'{"x":NaN}\n',
    ]
    strict_rejected = 0
    for raw in strict_attacks:
        try:
            strict_load_raw(raw)
        except Exception:
            strict_rejected += 1
    require(strict_rejected == len(strict_attacks), "strict attacks")
    result = {
        "status": "PASS",
        "certificate_result_sha256": certificate["result_sha256"],
        "producer_source_sha256":
            VERIFIER_PINS["cm2_round151_dual_boundary_event_census.py"],
        "producer_imported_or_executed": False,
        "shared_pinned_mathematical_engine_used": True,
        "C24_event_box_reconstruction_count": 21,
        "D3_event_box_reconstruction_count": 21,
        "total_event_box_reconstruction_count": 42,
        "C24_full_R1648_collision_stage_reconstruction_count": 21 * 1648,
        "full_radius4_candidate_tests_replayed": 5582031,
        "both_parametric_interval_Newton_graphs_recomputed": True,
        "all_exact_face_graph_adjacencies_recomputed": True,
        "uniform_graph_separation_recomputed": True,
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
        "status": "PASS",
        "output": str(args.output),
        "result_sha256": document["result_sha256"],
    }))


if __name__ == "__main__":
    main()
