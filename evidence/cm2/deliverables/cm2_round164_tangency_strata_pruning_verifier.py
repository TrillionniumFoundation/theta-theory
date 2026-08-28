#!/usr/bin/env python3
"""Independent replay verifier for the Round164 tangency certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_round164_tangency_strata_pruning_certificate.json"
OUTPUT = HERE / "cm2_round164_tangency_strata_pruning_verification.json"
SCHEMA = (
    "cm2.round164.dimension-safe-tangency-graph-typing."
    "verification.v2"
)
CERTIFICATE_SCHEMA = (
    "cm2.round164.dimension-safe-tangency-graph-typing.v2"
)
FROZEN_OWNER = "W[1,0]"
FROZEN_OUTGOING_CHART = "W"
PRODUCER = "cm2_round164_tangency_strata_pruning.py"
PINS = {
    PRODUCER:
        "0d8afdd3c56bf3e4c955e938500a95b14d11cdd246b4c99f2215f4e122a0768a",
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_round163_outgoing_chart_pruning_certificate.json":
        "90d3313004be90049efb116a44731aef2554056661ce83b85afafdf3e3738539",
    "cm2_round163_outgoing_chart_pruning_verification.json":
        "28ab965bffb0ab04d4fd839f1f7f895dbbab3a8e5be250a17fa95b7a8cc825d6",
}
DEPENDENCY_PINS = {
    name: value for name, value in PINS.items() if name != PRODUCER
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


def strict_load_raw(raw: bytes) -> dict[str, Any]:
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


def strict_load(path: Path) -> dict[str, Any]:
    return strict_load_raw(path.read_bytes())


def check_pins() -> tuple[dict[str, Any], dict[str, Any]]:
    require(Path(atlas.__file__).resolve() == (HERE / "cm2_gate3_eight_cell_symmetry_atlas_cert.py").resolve(), "atlas identity")
    require(Path(base.__file__).resolve() == (HERE / "cm2_gate3_candidate_first_hit_cert.py").resolve(), "base identity")
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


REPLAY_CANDIDATE_IDS = {
    chart_id: tuple(base.candidate_ids(chart_id))
    for chart_id in ("W:E", "W:N", "W:S")
}
REPLAY_TARGETS = {
    target.target_id: target for target in base.TARGETS
}


def replay_records(
    chart_id: str,
    box: atlas.AtlasBox,
) -> list[atlas.RootRecord]:
    """Recompute all roots with one shared geometry evaluation per box.

    The pinned upstream implementation deliberately favors transparency and
    reevaluates the same geometry once per target.  This verifier uses the
    algebraically identical target loop below so a cold replay remains
    practical while retaining the same 192-bit outward Arb operations.
    """

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


def replay_classify_box(
    chart_id: str,
    box: atlas.AtlasBox,
) -> atlas.Leaf:
    records = replay_records(chart_id, box)
    strict = [
        record for record in records
        if record.classification == "strict_future_root"
    ]
    unresolved = [
        record for record in records
        if record.classification
        in {"unresolved_discriminant", "unresolved_root_sign"}
    ]
    if not strict and not unresolved:
        return atlas.Leaf(
            box, "no_future_root", None, (), (),
            "all roots absent or behind",
        )
    for candidate in strict:
        require(candidate.near is not None, "strict root payload")
        if all(
            other.target_id == candidate.target_id
            or other.classification
            in {"no_real_intersection", "intersection_behind"}
            or (
                (
                    lower := atlas.ge.earliest_possible_root_lower(other)
                ) is not None
                and bool(candidate.near < lower)
            )
            for other in records
        ):
            return atlas.Leaf(
                box, "unique_first", candidate.target_id,
                (candidate.target_id,), (),
                "selected incoming root strictly precedes every "
                "possible competitor root",
            )
    tangencies = tuple(
        record.target_id
        for record in unresolved
        if atlas.physical_tangency_graph(
            chart_id, box, record, records,
        )
    )
    if len(tangencies) == 1:
        return atlas.Leaf(
            box, "tangency_graph", tangencies[0],
            tangencies, tangencies,
            "unique monotone physical first-tangency graph in p",
        )
    active: set[str] = set()
    for candidate in strict + unresolved:
        lower = atlas.ge.earliest_possible_root_lower(candidate)
        if lower is None or not any(
            other.target_id != candidate.target_id
            and other.near is not None
            and bool(other.near < lower)
            for other in strict
        ):
            active.add(candidate.target_id)
    return atlas.Leaf(
        box, "multi_candidate", None,
        tuple(sorted(active)), tangencies,
        "interval root ordering or boundary type not isolated",
    )


def replay_build_atlas(chart_id: str) -> list[atlas.Leaf]:
    pending = atlas.initial_boxes()
    leaves: list[atlas.Leaf] = []
    while pending:
        box = pending.pop()
        leaf = replay_classify_box(chart_id, box)
        if leaf.classification in {
            "unique_first", "tangency_graph", "no_future_root",
        } or box.depth >= atlas.MAX_DEPTH:
            leaves.append(leaf)
        else:
            pending.extend(atlas.ge.split(box))
    return sorted(leaves, key=lambda leaf: leaf.box.path)


def build_atlases() -> dict[str, list[atlas.Leaf]]:
    direct_e = replay_build_atlas("W:E")
    direct_n = replay_build_atlas("W:N")
    return {
        "W:E": direct_e,
        "W:N": direct_n,
        "W:S": [atlas.reflect_leaf("W:N", "horizontal", leaf) for leaf in direct_n],
    }


def row(chart_id: str, leaf: atlas.Leaf) -> dict[str, Any]:
    require(leaf.classification == "tangency_graph" and len(leaf.tangency_targets) == 1, "typed tangency")
    target_id = leaf.tangency_targets[0]
    records = replay_records(chart_id, leaf.box)
    record = next(item for item in records if item.target_id == target_id)
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
    return {
        "ambient_leaf_key": f"{chart_id}:{leaf.box.path}",
        "chart_id": chart_id,
        "tangency_target": target_id,
        "graph_disposition": (
            "TYPED_FROZEN_OWNER_TANGENCY_GRAPH"
            if target_id == FROZEN_OWNER
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
    records = replay_records(chart_id, box)
    record = next(
        item for item in records if item.target_id == FROZEN_OWNER
    )
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
    classification = replay_classify_box(chart_id, point)
    require(
        classification.classification == "unique_first"
        and classification.owner_target == FROZEN_OWNER,
        "live frozen owner regression",
    )
    records = replay_records(chart_id, point)
    tangency_record = next(
        item for item in records
        if item.target_id == tangency_target
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


def reconstruct() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
    dict[str, Any],
]:
    prior, verification = check_pins()
    atlases = build_atlases()
    rows = [
        row(chart_id, leaf)
        for chart_id, leaves in atlases.items()
        for leaf in leaves
        if leaf.classification == "tangency_graph"
    ]
    rows.sort(key=lambda item: item["ambient_leaf_key"])
    require(len(rows) == 32, "row count")
    leaf_index = {
        (chart_id, leaf.box.path): leaf
        for chart_id, leaves in atlases.items()
        for leaf in leaves
    }
    regressions = [
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
    regressions.sort(key=lambda item: item["ambient_leaf_key"])
    return rows, regressions, prior, verification


def rebuild_expected(
    rows: list[dict[str, Any]],
    live_regressions: list[dict[str, Any]],
    prior: dict[str, Any],
    verification: dict[str, Any],
) -> dict[str, Any]:
    mismatch_graphs = sum(
        row["graph_disposition"]
        == "TYPED_PREFIX_MISMATCH_TANGENCY_GRAPH"
        for row in rows
    )
    frozen_owner_graphs = len(rows) - mismatch_graphs
    old = prior["result"]["combined_frozen_prefix_census"]
    remaining = old["remaining_leaf_count"]
    component_sum = (
        old["remaining_prefix_stage_one_match"]
        + old["remaining_outgoing_chart_seam_unresolved"]
        + len(rows)
        + old["remaining_multi_candidate"]
    )
    require(
        (mismatch_graphs, frozen_owner_graphs) == (12, 20)
        and remaining == component_sum == 39348,
        "dimension-safe census",
    )
    result = {
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
                old["combined_recordwise_excluded_leaf_count"],
            "new_full_dimensional_ambient_leaf_exclusion_count": 0,
            "combined_recordwise_excluded_ambient_leaf_count":
                old["combined_recordwise_excluded_leaf_count"],
            "prior_ambient_unresolved_leaf_count": remaining,
            "remaining_ambient_unresolved_leaf_count": remaining,
            "remaining_prefix_stage_one_match":
                old["remaining_prefix_stage_one_match"],
            "remaining_outgoing_chart_seam_unresolved":
                old["remaining_outgoing_chart_seam_unresolved"],
            "remaining_tangency_ambient_leaf_bulk": len(rows),
            "remaining_multi_candidate": old["remaining_multi_candidate"],
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
            "dependency_sha256": DEPENDENCY_PINS,
            "round163_result_sha256": prior["result_sha256"],
            "round163_verification_result_sha256":
                verification["result_sha256"],
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
    return {
        "schema": CERTIFICATE_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def validate(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    require(set(document) == {"schema", "result", "result_sha256"}, "document keys")
    require(document["schema"] == CERTIFICATE_SCHEMA, "schema")
    require(document["result_sha256"] == digest(document["result"]), "result digest")
    require(canonical(document) == canonical(expected), "full semantic document")


def semantic_attacks(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    mutations: list[
        tuple[str, Callable[[dict[str, Any]], None], bool]
    ] = [
        ("schema", lambda value: value.__setitem__("schema", "mutated"), False),
        ("result digest", lambda value: value.__setitem__("result_sha256", "0" * 64), False),
        ("status", lambda value: value["result"].__setitem__("status", "FORGED_D02_COMPLETE"), True),
        ("parent count", lambda value: value["result"]["tangency_graph_typing"].__setitem__("ambient_parent_leaf_count", 31), True),
        ("graph count", lambda value: value["result"]["tangency_graph_typing"].__setitem__("typed_codimension_one_graph_count", 31), True),
        ("mismatch graphs", lambda value: value["result"]["tangency_graph_typing"].__setitem__("prefix_mismatch_graph_count", 13), True),
        ("frozen graphs", lambda value: value["result"]["tangency_graph_typing"].__setitem__("frozen_owner_graph_count", 19), True),
        ("fake full-dimensional credit", lambda value: value["result"]["tangency_graph_typing"].__setitem__("new_full_dimensional_parent_leaf_exclusion_count", 12), True),
        ("dimension mix", lambda value: value["result"]["tangency_graph_typing"].__setitem__("typed_graph_dimension", 3), True),
        ("fake partition", lambda value: value["result"]["tangency_graph_typing"].__setitem__("D_negative_D_zero_D_positive_partition_materialized", True), True),
        ("graph flag", lambda value: value["result"]["tangency_graph_typing"].__setitem__("all_physical_first_tangency_graphs_replayed", False), True),
        ("row digest", lambda value: value["result"]["tangency_graph_typing"].__setitem__("all_rows_sha256", "0" * 64), True),
        ("row target", lambda value: value["result"]["tangency_graph_typing"]["rows"][0].__setitem__("tangency_target", "G[9,9]"), True),
        ("row bulk credit", lambda value: value["result"]["tangency_graph_typing"]["rows"][0].__setitem__("ambient_leaf_bulk_disposition", "EXCLUDED"), True),
        ("prior excluded", lambda value: value["result"]["ambient_frozen_prefix_census"].__setitem__("prior_recordwise_excluded_ambient_leaf_count", 37479), True),
        ("new ambient exclusion", lambda value: value["result"]["ambient_frozen_prefix_census"].__setitem__("new_full_dimensional_ambient_leaf_exclusion_count", 12), True),
        ("combined excluded", lambda value: value["result"]["ambient_frozen_prefix_census"].__setitem__("combined_recordwise_excluded_ambient_leaf_count", 37492), True),
        ("remaining", lambda value: value["result"]["ambient_frozen_prefix_census"].__setitem__("remaining_ambient_unresolved_leaf_count", 39336), True),
        ("stage-one", lambda value: value["result"]["ambient_frozen_prefix_census"].__setitem__("remaining_prefix_stage_one_match", 0), True),
        ("seam", lambda value: value["result"]["ambient_frozen_prefix_census"].__setitem__("remaining_outgoing_chart_seam_unresolved", 0), True),
        ("tangency bulk", lambda value: value["result"]["ambient_frozen_prefix_census"].__setitem__("remaining_tangency_ambient_leaf_bulk", 20), True),
        ("multi", lambda value: value["result"]["ambient_frozen_prefix_census"].__setitem__("remaining_multi_candidate", 0), True),
        ("component sum", lambda value: value["result"]["ambient_frozen_prefix_census"].__setitem__("component_sum", 39336), True),
        ("unresolved", lambda value: value["result"]["ambient_frozen_prefix_census"].__setitem__("unresolved_zero", True), True),
        ("withdraw correction", lambda value: value["result"]["v1_correction"].__setitem__("withdrawn_remaining_leaf_count", 39348), True),
        ("erase regression", lambda value: value["result"]["v1_correction"].__setitem__("live_off_graph_regression_count", 0), True),
        ("mutate regression point", lambda value: value["result"]["v1_correction"]["live_off_graph_regressions"][0]["strict_interior_point"].__setitem__("p", "0"), True),
        ("fake regression exclusion", lambda value: value["result"]["v1_correction"]["live_off_graph_regressions"][0].__setitem__("proves_ambient_leaf_cannot_be_pruned_from_graph_only", False), True),
        ("scope codimension confusion", lambda value: value["result"]["scope"].__setitem__("typed_graphs_do_not_remove_ambient_parent_leaves", False), True),
        ("dependency pin", lambda value: value["result"]["provenance"]["dependency_sha256"].__setitem__("cm2_gate3_candidate_first_hit_cert.py", "0" * 64), True),
        ("prior result", lambda value: value["result"]["provenance"].__setitem__("round163_result_sha256", "0" * 64), True),
        ("replay precision", lambda value: value["result"]["provenance"].__setitem__("source_W_atlas_replayed_at_192_bits", False), True),
        ("D02", lambda value: value["result"]["strict_nonpromotion"].__setitem__("D02", "PASS"), True),
        ("CM2", lambda value: value["result"]["strict_nonpromotion"].__setitem__("CM2", "GO"), True),
        ("next gate", lambda value: value["result"].__setitem__("next_core_gate", "ALL_DONE"), True),
        ("extra result key", lambda value: value["result"].__setitem__("forged", True), True),
    ]
    rejected = 0
    rejected_names: list[str] = []
    for name, mutate, resign in mutations:
        candidate = copy.deepcopy(document)
        mutate(candidate)
        if resign:
            candidate["result_sha256"] = digest(candidate["result"])
        try:
            validate(candidate, expected)
        except Exception:
            rejected += 1
            rejected_names.append(name)
    return {
        "attack_count": len(mutations),
        "rejected_count": rejected,
        "all_rejected": rejected == len(mutations),
        "all_result_mutations_resigned": True,
        "rejected_attack_names": rejected_names,
    }


def strict_json_attacks() -> dict[str, Any]:
    attacks = [
        b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}',
        b'\xef\xbb\xbf{"x":1}', b'{"x":"\\u0000"}',
        b'{"x":"\\ud800"}', b'{"x":1}\x00',
    ]
    rejected = 0
    for attack in attacks:
        try:
            strict_load_raw(attack)
        except Exception:
            rejected += 1
    return {"attack_count": len(attacks), "rejected_count": rejected, "all_rejected": rejected == len(attacks)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    document = strict_load(args.certificate)
    rows, live_regressions, prior, verification = reconstruct()
    expected = rebuild_expected(
        rows, live_regressions, prior, verification,
    )
    validate(document, expected)
    semantic = semantic_attacks(document, expected)
    strict_json = strict_json_attacks()
    require(semantic["all_rejected"] and strict_json["all_rejected"], "attack suites")
    result = {
        "status": "PASS",
        "certificate_schema": document["schema"],
        "certificate_result_sha256": document["result_sha256"],
        "round164_producer_imported_or_executed": False,
        "all_32_tangency_graphs_reconstructed": True,
        "all_physical_first_tangency_graphs_replayed": True,
        "all_graph_disposition_rows_recomputed": True,
        "dimension_safe_ambient_census_recomputed": True,
        "both_live_off_graph_regressions_replayed": True,
        "invalid_v1_whole_leaf_credit_rejected": True,
        "all_certificate_fields_semantically_reconstructed": True,
        "full_document_exactly_matched": True,
        "strict_nonpromotion_recomputed": True,
        "semantic_attack_suite": semantic,
        "strict_json_attack_suite": strict_json,
    }
    output = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    args.output.write_text(canonical(output) + "\n")
    print(output["result_sha256"])


if __name__ == "__main__":
    main()
