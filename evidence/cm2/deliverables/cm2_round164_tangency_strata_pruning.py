#!/usr/bin/env python3
"""Round164 v2: type tangency graphs without pruning ambient leaves."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round164_tangency_strata_pruning_certificate.json"
SCHEMA = "cm2.round164.dimension-safe-tangency-graph-typing.v2"
FROZEN_OWNER = "W[1,0]"
FROZEN_OUTGOING_CHART = "W"
CHARTS = ("W:E", "W:N", "W:S")
PINS = {
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_round163_outgoing_chart_pruning_certificate.json":
        "90d3313004be90049efb116a44731aef2554056661ce83b85afafdf3e3738539",
    "cm2_round163_outgoing_chart_pruning_verification.json":
        "28ab965bffb0ab04d4fd839f1f7f895dbbab3a8e5be250a17fa95b7a8cc825d6",
}

REPLAY_CANDIDATE_IDS = {
    chart_id: tuple(base.candidate_ids(chart_id))
    for chart_id in CHARTS
}
REPLAY_TARGETS = {
    target.target_id: target for target in base.TARGETS
}


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "encoding")

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, "duplicate key")
            result[key] = value
        return result

    value = json.loads(
        raw.decode(), object_pairs_hook=unique,
        parse_constant=reject, parse_float=reject,
    )

    def check_strings(item: Any) -> None:
        if type(item) is str:
            require(
                "\x00" not in item
                and not any(0xD800 <= ord(character) <= 0xDFFF for character in item),
                "decoded string encoding",
            )
        elif type(item) is list:
            for child in item:
                check_strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                check_strings(key)
                check_strings(child)

    check_strings(value)
    require(type(value) is dict, "top object")
    return value


def check_chain() -> tuple[dict[str, Any], dict[str, Any]]:
    require(Path(atlas.__file__).resolve() == (HERE / next(iter(PINS))).resolve(), "atlas identity")
    require(Path(base.__file__).resolve() == (HERE / list(PINS)[1]).resolve(), "base identity")
    for name, expected in PINS.items():
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, f"pin:{name}")
    prior = strict_load(HERE / "cm2_round163_outgoing_chart_pruning_certificate.json")
    verification = strict_load(HERE / "cm2_round163_outgoing_chart_pruning_verification.json")
    require(
        prior["result_sha256"] == "d64b5fab6b599a8fb4d6665c8abb902d79f86afd0370610845a5f7558d848102"
        and verification["result_sha256"] == "183b30155016229f27ba35293ad98d4b1b779af19c84dab5fec583862c8ef8a9"
        and verification["result"]["status"] == "PASS",
        "Round163 chain",
    )
    return prior, verification


def replay_records(
    chart_id: str,
    box: atlas.AtlasBox,
) -> list[atlas.RootRecord]:
    """Algebraically identical root replay with one geometry call per box."""

    qx, qy, ux, uy, s, _radial = atlas.geometry(chart_id, box)
    rows: list[atlas.RootRecord] = []
    for target_id in REPLAY_CANDIDATE_IDS[chart_id]:
        target = REPLAY_TARGETS[target_id]
        ax, ay = base.target_center(target, s)
        dx, dy = ax - qx, ay - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = base.arbq(base.RADIUS[target.obstacle])
        discriminant = radius * radius - transverse * transverse
        if bool(discriminant < 0):
            rows.append(atlas.RootRecord(
                target_id, "no_real_intersection", ell,
                discriminant, None, None, transverse,
            ))
            continue
        if not bool(discriminant > 0):
            rows.append(atlas.RootRecord(
                target_id, "unresolved_discriminant", ell,
                discriminant, None, None, transverse,
            ))
            continue
        radical = discriminant.sqrt()
        near, far = ell - radical, ell + radical
        if bool(far < 0):
            classification = "intersection_behind"
        elif bool(near > 0):
            classification = "strict_future_root"
        else:
            classification = "unresolved_root_sign"
        rows.append(atlas.RootRecord(
            target_id, classification, ell,
            discriminant, near, far, transverse,
        ))
    return rows


def build_atlases() -> dict[str, list[atlas.Leaf]]:
    original_records = atlas.records
    atlas.records = replay_records
    try:
        direct_e = atlas.build_atlas("W:E")
        direct_n = atlas.build_atlas("W:N")
    finally:
        atlas.records = original_records
    return {
        "W:E": direct_e,
        "W:N": direct_n,
        "W:S": [atlas.reflect_leaf("W:N", "horizontal", leaf) for leaf in direct_n],
    }


def witness(chart_id: str, leaf: atlas.Leaf) -> dict[str, Any]:
    require(leaf.classification == "tangency_graph", "tangency classification")
    require(len(leaf.tangency_targets) == 1, "single tangency target")
    target_id = leaf.tangency_targets[0]
    records = replay_records(chart_id, leaf.box)
    record = next(row for row in records if row.target_id == target_id)
    require(atlas.physical_tangency_graph(chart_id, leaf.box, record, records), "graph replay")
    *_unused, radial = atlas.geometry(chart_id, leaf.box)
    derivative = 2 * record.transverse * record.ell / radial
    lower = atlas.root_at_fixed_p(chart_id, leaf.box, target_id, leaf.box.p0).discriminant
    upper = atlas.root_at_fixed_p(chart_id, leaf.box, target_id, leaf.box.p1).discriminant
    require(bool(derivative > 0) or bool(derivative < 0), "strict derivative")
    require(
        (bool(lower < 0) and bool(upper > 0))
        or (bool(lower > 0) and bool(upper < 0)),
        "opposite face signs",
    )
    derivative_sign = "POSITIVE" if bool(derivative > 0) else "NEGATIVE"
    lower_sign = "POSITIVE" if bool(lower > 0) else "NEGATIVE"
    upper_sign = "POSITIVE" if bool(upper > 0) else "NEGATIVE"
    owner_matches = target_id == FROZEN_OWNER
    return {
        "ambient_leaf_key": f"{chart_id}:{leaf.box.path}",
        "chart_id": chart_id,
        "tangency_target": target_id,
        "graph_disposition": (
            "TYPED_FROZEN_OWNER_TANGENCY_GRAPH"
            if owner_matches
            else "TYPED_PREFIX_MISMATCH_TANGENCY_GRAPH"
        ),
        "credit_scope": "CODIMENSION_ONE_GRAPH_ONLY",
        "ambient_parameter_dimension": 3,
        "typed_graph_dimension": 2,
        "graph_equation": f"DISCRIMINANT[{target_id}]=0",
        "graph_base_variables": ["t", "s"],
        "graph_variable": "p",
        "ambient_leaf_bulk_disposition": "UNRESOLVED_OFF_GRAPH_BULK",
        "derivative_sign": derivative_sign,
        "lower_p_face_discriminant_sign": lower_sign,
        "upper_p_face_discriminant_sign": upper_sign,
        "derivative_arb_display_outer": str(derivative),
        "lower_p_face_discriminant_arb_display_outer": str(lower),
        "upper_p_face_discriminant_arb_display_outer": str(upper),
        "display_outers_are_not_sign_witnesses": True,
    }


def point_outgoing_chart(
    chart_id: str,
    box: atlas.AtlasBox,
) -> tuple[str, Any, Any]:
    record = atlas.root_record(chart_id, box, FROZEN_OWNER)
    require(
        record.classification == "strict_future_root"
        and record.near is not None,
        "counterexample frozen root",
    )
    qx, qy, ux, uy, s, _radial = atlas.geometry(chart_id, box)
    target = REPLAY_TARGETS[FROZEN_OWNER]
    center_x, center_y = base.target_center(target, s)
    radius = base.arbq(base.RADIUS[target.obstacle])
    normal_x = (qx + record.near * ux - center_x) / radius
    normal_y = (qy + record.near * uy - center_y) / radius
    tests = {
        "E": (normal_x - normal_y, normal_x + normal_y),
        "W": (-normal_x - normal_y, -normal_x + normal_y),
        "N": (normal_y - normal_x, normal_y + normal_x),
        "S": (-normal_y - normal_x, -normal_y + normal_x),
    }
    for cell in ("E", "W", "N", "S"):
        first, second = tests[cell]
        if bool(first > 0) and bool(second > 0):
            return cell, first, second
    raise RuntimeError("counterexample outgoing chart unresolved")


def live_off_graph_counterexample(
    chart_id: str,
    ambient_leaf: atlas.Leaf,
    tangency_target: str,
    t: Q,
    p: Q,
) -> dict[str, Any]:
    box = ambient_leaf.box
    require(
        box.t0 < t < box.t1
        and box.p0 < p < box.p1
        and box.s0 < 0 < box.s1,
        "strict ambient interior",
    )
    point = atlas.AtlasBox(
        t, t, p, p, Q(0), Q(0),
        box.depth, box.path + ".live-regression",
    )
    original_records = atlas.records
    atlas.records = replay_records
    try:
        classification = atlas.classify_box(chart_id, point)
    finally:
        atlas.records = original_records
    require(
        classification.classification == "unique_first"
        and classification.owner_target == FROZEN_OWNER,
        "live frozen owner regression",
    )
    tangency_record = atlas.root_record(
        chart_id, point, tangency_target,
    )
    require(
        tangency_record.classification == "no_real_intersection"
        and bool(tangency_record.discriminant < 0),
        "strictly off tangency graph",
    )
    outgoing, first, second = point_outgoing_chart(chart_id, point)
    require(
        outgoing == FROZEN_OUTGOING_CHART
        and bool(first > 0)
        and bool(second > 0),
        "live frozen outgoing chart regression",
    )
    return {
        "ambient_leaf_key": f"{chart_id}:{box.path}",
        "strict_interior_point": {
            "t": str(t), "p": str(p), "s": "0",
        },
        "tangency_target": tangency_target,
        "tangency_target_point_classification":
            "no_real_intersection",
        "tangency_target_discriminant_sign": "NEGATIVE",
        "tangency_target_discriminant_arb_display_outer":
            str(tangency_record.discriminant),
        "point_first_hit_classification": "unique_first",
        "point_first_owner": FROZEN_OWNER,
        "point_outgoing_chart": outgoing,
        "outgoing_margin_one_sign": "POSITIVE",
        "outgoing_margin_two_sign": "POSITIVE",
        "outgoing_margin_one_arb_display_outer": str(first),
        "outgoing_margin_two_arb_display_outer": str(second),
        "proves_ambient_leaf_cannot_be_pruned_from_graph_only": True,
    }


def build_result() -> dict[str, Any]:
    prior, verification = check_chain()
    atlases = build_atlases()
    rows = [
        witness(chart_id, leaf)
        for chart_id, leaves in atlases.items()
        for leaf in leaves
        if leaf.classification == "tangency_graph"
    ]
    rows.sort(key=lambda row: row["ambient_leaf_key"])
    require(len(rows) == 32, "outside-W:W tangency count")
    mismatch_graphs = sum(
        row["graph_disposition"]
        == "TYPED_PREFIX_MISMATCH_TANGENCY_GRAPH"
        for row in rows
    )
    frozen_owner_graphs = len(rows) - mismatch_graphs
    require(
        (mismatch_graphs, frozen_owner_graphs) == (12, 20),
        "tangency graph census",
    )
    leaf_index = {
        (chart_id, leaf.box.path): leaf
        for chart_id, leaves in atlases.items()
        for leaf in leaves
    }
    live_regressions = [
        live_off_graph_counterexample(
            "W:N",
            leaf_index[("W:N", "05.00.00100110")],
            "G[1,1]",
            Q(7611, 32000),
            Q(-12599, 12800),
        ),
        live_off_graph_counterexample(
            "W:S",
            leaf_index[("W:S", "H.05.00.00100110")],
            "G[1,0]",
            Q(7611, 32000),
            Q(12599, 12800),
        ),
    ]
    live_regressions.sort(
        key=lambda row: row["ambient_leaf_key"],
    )
    combined = prior["result"]["combined_frozen_prefix_census"]
    remaining = combined["remaining_leaf_count"]
    component_sum = (
        combined["remaining_prefix_stage_one_match"]
        + combined["remaining_outgoing_chart_seam_unresolved"]
        + len(rows)
        + combined["remaining_multi_candidate"]
    )
    require(remaining == component_sum == 39348, "ambient census identity")
    return {
        "status": (
            "CERTIFIED_DIMENSION_SAFE_OUTSIDE_W_W_TANGENCY_GRAPH_TYPING__"
            "NO_WHOLE_LEAF_PRUNING__D02_STILL_BLOCKED"
        ),
        "tangency_graph_typing": {
            "ambient_parent_leaf_count": len(rows),
            "typed_codimension_one_graph_count": len(rows),
            "prefix_mismatch_graph_count": mismatch_graphs,
            "frozen_owner_graph_count": frozen_owner_graphs,
            "new_full_dimensional_parent_leaf_exclusion_count": 0,
            "remaining_off_graph_ambient_parent_count": len(rows),
            "ambient_parameter_dimension": 3,
            "typed_graph_dimension": 2,
            "full_dimensional_parent_replacement_completed": False,
            "D_negative_D_zero_D_positive_partition_materialized":
                False,
            "all_physical_first_tangency_graphs_replayed": True,
            "all_rows_sha256": digest(rows),
            "rows": rows,
        },
        "ambient_frozen_prefix_census": {
            "prior_recordwise_excluded_ambient_leaf_count":
                combined["combined_recordwise_excluded_leaf_count"],
            "new_full_dimensional_ambient_leaf_exclusion_count": 0,
            "combined_recordwise_excluded_ambient_leaf_count":
                combined["combined_recordwise_excluded_leaf_count"],
            "prior_ambient_unresolved_leaf_count": remaining,
            "remaining_ambient_unresolved_leaf_count": remaining,
            "remaining_prefix_stage_one_match":
                combined["remaining_prefix_stage_one_match"],
            "remaining_outgoing_chart_seam_unresolved":
                combined["remaining_outgoing_chart_seam_unresolved"],
            "remaining_tangency_ambient_leaf_bulk": len(rows),
            "remaining_multi_candidate":
                combined["remaining_multi_candidate"],
            "component_sum": component_sum,
            "ambient_leaf_count_identity_verified": True,
            "unresolved_zero": False,
        },
        "v1_correction": {
            "superseded_schema":
                "cm2.round164.tangency-strata-pruning.v1",
            "superseded_result_sha256":
                "1111deaa4221a4b1df94e8bed9b5cc9eed7e45ca615db1558ad556ecf3d59f23",
            "withdrawn_combined_recordwise_excluded_leaf_count": 37492,
            "withdrawn_remaining_leaf_count": 39336,
            "correction_reason": (
                "a typed codimension-one tangency graph does not classify "
                "or remove its three-dimensional ambient parent leaf"
            ),
            "live_off_graph_regression_count": len(live_regressions),
            "all_live_off_graph_regressions_sha256":
                digest(live_regressions),
            "live_off_graph_regressions": live_regressions,
        },
        "scope": {
            "typed_graphs_are_terminal_codimension_one_strata": True,
            "typed_graphs_do_not_remove_ambient_parent_leaves": True,
            "off_graph_sides_remain_unresolved": True,
            "arb_display_outers_are_not_used_as_sign_witnesses": True,
            "not_full_exterior_sheet_exhaustion": True,
            "not_D02_closure": True,
        },
        "provenance": {
            "dependency_sha256": PINS,
            "round163_result_sha256": prior["result_sha256"],
            "round163_verification_result_sha256": verification["result_sha256"],
            "source_W_atlas_replayed_at_192_bits": True,
            "one_geometry_evaluation_per_box_root_replay": True,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "materialize D<0, D=0 and D>0 replacements for all 32 "
            "tangency ambient parents; subdivide 618 outgoing-chart seam "
            "leaves and 38,180 outside-W:W multi-candidate leaves"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build_result()
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    args.output.write_text(canonical(document) + "\n")
    print(document["result_sha256"])


if __name__ == "__main__":
    main()
