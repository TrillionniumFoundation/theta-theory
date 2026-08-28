#!/usr/bin/env python3
"""Close Round261 residual faces with fixed-precision monotone interval proofs."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import importlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Callable

from flint import ctx, __version__ as FLINT_VERSION

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round262_source_g_monotone_deep_common_face_closure_certificate.json"
SCHEMA = "cm2.round262.source-g-monotone-deep-common-face-closure.v1"
MAX_DEPTH = 24
WORKERS = 40
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round204_source_g_wall_return_signature_local_replacement.py":
        "7e4b81846155c1edad0807362c7086a290702da7ce6680d7c449b7193635da77",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round208_source_g_outgoing_direct_signature_materialization.py":
        "c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round260_source_g_curved_region_common_face_refinement_certificate.json":
        "a86ec032c3acbb708fd606ea0aa340f9ad650b9a8ac5e77299fefb8fdd1a765b",
    "cm2_round261_source_g_adaptive_common_face_strict_separation_certificate.json":
        "6b69453c869d07737152c851d7716434dca16184433ef8be9023cb56027b162c",
}
G: dict[str, Any] = {}
STRICT = {"STRICT_POSITIVE", "STRICT_NEGATIVE"}


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def qtext(value: Fraction) -> str:
    return (
        str(value.numerator) if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def arbtext(value: Any) -> str:
    return value.repr()


def read_pinned(name: str) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode) and not path.is_symlink()
        and info.st_nlink == 1 and 0 < info.st_size <= 500_000_000,
        f"regular pinned input:{name}",
    )
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PINS[name], f"pin:{name}")
    return raw


def load_result(name: str) -> dict[str, Any]:
    document = json.loads(read_pinned(name))
    need(
        set(document) == {"schema", "result", "result_sha256"}
        and digest(document["result"]) == document["result_sha256"],
        f"envelope:{name}",
    )
    return document["result"]


def closed(row: dict[str, Any]) -> dict[str, Any]:
    output = dict(row)
    output["row_sha256"] = digest(output)
    return output


def ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    need(len(rows) == len({row[id_field] for row in rows}), f"unique:{id_field}")
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


class DSU:
    def __init__(self, values: list[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        if self.parent[value] != value:
            self.parent[value] = self.find(self.parent[value])
        return self.parent[value]

    def union(self, left: str, right: str) -> bool:
        left, right = self.find(left), self.find(right)
        if left == right:
            return False
        if left > right:
            left, right = right, left
        self.parent[right] = left
        return True


def load_geometry() -> None:
    need(FLINT_VERSION == "0.9.0", "python-flint 0.9.0")
    read_pinned("cm2_round204_source_g_wall_return_signature_local_replacement.py")
    read_pinned("cm2_round208_source_g_outgoing_direct_signature_materialization.py")
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    r208 = importlib.import_module(
        "cm2_round208_source_g_outgoing_direct_signature_materialization"
    )
    r204 = importlib.import_module(
        "cm2_round204_source_g_wall_return_signature_local_replacement"
    )
    r207, _ = r208.load_evaluator()
    r198 = r207.r203.r198
    r195 = r198.r195
    r186 = r195.r191.r189.r188.r186
    r174 = r186.r179.r174
    _, collars208, _ = r195.r191.r189.load_scope()
    formal = r204.load_formal_inputs()
    r179 = formal["evaluator"].r179
    r174_204 = r179.r174
    scope182 = r204.extract_round182_scope(formal["attachment182"])
    scope179 = r204.extract_round179_scope(
        formal["source179"], scope182["occurrence_ids"], scope182["origin_ids"]
    )
    c204 = load_result(
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
    )
    c208 = load_result(
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )
    reg204 = {
        row["region_row_id"]: row
        for row in c204["formal_local_open_3D_region_ledger"]["rows"]
    }
    reg208 = {
        row["region_row_id"]: row
        for row in c208["formal_local_open_3D_signature_ledger"]["rows"]
    }
    boxes = {
        region_id: tuple(Fraction(value) for value in row["leaf_exact_box"])
        for region_id, row in reg204.items()
    }
    boxes.update({
        region_id: tuple(Fraction(value) for value in row["Round182_leaf_box"])
        for region_id, row in reg208.items()
    })
    rows179 = load_result("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    columns = rows179["row_column_schemas"]["resolved_3d_child_rows"]
    for packed in rows179["resolved_3d_child_rows"]:
        row = dict(zip(columns, packed, strict=True))
        boxes[row["row_id"]] = tuple(Fraction(value) for value in row["box"])
    need(len(boxes) == 53_968, "53,968 exact boxes")
    G.update(
        r198=r198, r186=r186, r174=r174, collars208=collars208,
        r204=r204, r179=r179, r174_204=r174_204,
        scope182=scope182, scope179=scope179,
        reg204=reg204, reg208=reg208, boxes=boxes,
    )


def strict_evidence208(
    oid: str, values: list[Fraction], label: str
) -> tuple[str, dict[str, Any]]:
    reg = G["reg208"][oid]
    profiles = G["r198"].selected_factor_profiles(
        G["collars208"][reg["occurrence_row_id"]],
        G["r174"].atlas.AtlasBox(*values, 0, label),
    )
    actual = [
        profiles["HPLUS"]["selected_sign"],
        profiles["HMINUS"]["selected_sign"],
    ]
    expected = [reg["HPLUS_sign"], reg["HMINUS_sign"]]
    if actual == expected:
        state = "MATCH"
    elif any(
        value in STRICT and value != wanted
        for value, wanted in zip(actual, expected)
    ):
        state = "STRICT_EXCLUDE"
    else:
        state = "UNRESOLVED"
    return state, {
        "actual_selected_signs": actual,
        "expected_signs": expected,
        "selected_factor_profiles": profiles,
    }


def strict_state208(oid: str, values: list[Fraction], label: str) -> str:
    return strict_evidence208(oid, values, label)[0]


def strict_evidence204(
    oid: str, values: list[Fraction], label: str
) -> tuple[str, dict[str, Any]]:
    reg = G["reg204"][oid]
    collar = G["scope182"]["collars"][reg["occurrence_row_id"]]
    wall = G["scope179"]["walls"][reg["occurrence_row_id"]]
    r179 = G["r179"]
    geometry = r179.independent_geometry(
        collar["chart"], collar["owner_target"],
        G["r174_204"].atlas.AtlasBox(*values, 0, label),
    )
    source_name = G["r204"].CHART_CONTRACT[collar["chart"]][2]
    target_name = "hit_x" if wall["axis"] == "X" else "hit_y"
    actual = [
        r179.arb_sign(r179.subtract_wall(geometry[source_name], 0)[0]),
        r179.arb_sign(
            r179.subtract_wall(geometry[target_name], wall["integer_wall"])[0]
        ),
    ]
    expected = [
        "STRICT_" + reg["source_sign"],
        "STRICT_" + reg["target_factor_sign"],
    ]
    if actual == expected:
        state = "MATCH"
    elif any(
        value in STRICT and value != wanted
        for value, wanted in zip(actual, expected)
    ):
        state = "STRICT_EXCLUDE"
    else:
        state = "UNRESOLVED"
    return state, {
        "source_factor": source_name,
        "target_factor": target_name,
        "actual_selected_signs": actual,
        "expected_signs": expected,
    }


def strict_state204(oid: str, values: list[Fraction], label: str) -> str:
    return strict_evidence204(oid, values, label)[0]


def weak_opposite(value: Any, expected: str) -> bool:
    if expected == "STRICT_POSITIVE":
        return bool(value <= 0)
    if expected == "STRICT_NEGATIVE":
        return bool(value >= 0)
    raise RuntimeError(f"unexpected strict sign:{expected}")


def monotone_opposite(
    dual: tuple[Any, tuple[Any, ...]],
    expected: str,
    values: list[Fraction],
    point_value: Callable[[list[Fraction]], Any],
) -> dict[str, Any] | None:
    prove_nonpositive = expected == "STRICT_POSITIVE"
    prove_nonnegative = expected == "STRICT_NEGATIVE"
    need(prove_nonpositive or prove_nonnegative, "monotone expected sign")
    corner = list(values)
    derivative_rows = []
    for axis in range(3):
        lower, upper = values[2 * axis:2 * axis + 2]
        if lower == upper:
            derivative_rows.append([
                "FIXED",
                "NONE" if dual[1][axis] is None else arbtext(dual[1][axis]),
            ])
            continue
        derivative = dual[1][axis]
        if derivative is None:
            return None
        if bool(derivative > 0):
            derivative_sign = "STRICT_POSITIVE"
            coordinate = upper if prove_nonpositive else lower
        elif bool(derivative < 0):
            derivative_sign = "STRICT_NEGATIVE"
            coordinate = lower if prove_nonpositive else upper
        else:
            return None
        derivative_rows.append([derivative_sign, arbtext(derivative)])
        corner[2 * axis:2 * axis + 2] = [coordinate, coordinate]
    value = point_value(corner)
    if not weak_opposite(value, expected):
        return None
    return {
        "expected_strict_sign": expected,
        "derivative_axis_proofs": derivative_rows,
        "extremizing_corner": [qtext(value) for value in corner],
        "corner_value_enclosure": arbtext(value),
        "proved_weak_opposite_on_whole_cell": True,
    }


def relation208(
    oid: str, values: list[Fraction], label: str
) -> tuple[str, dict[str, Any]]:
    reg = G["reg208"][oid]
    collar = G["collars208"][reg["occurrence_row_id"]]
    r186 = G["r186"]
    box = G["r174"].atlas.AtlasBox(*values, 0, label)
    geometry = r186.factor_geometry(collar["chart"], collar["owner_target"], box)
    kinds = ("HPLUS", "HMINUS")
    direct = [geometry[kind][0] for kind in kinds]
    centered = [
        r186.centered_value(collar["chart"], collar["owner_target"], box, kind)
        for kind in kinds
    ]
    expected = [reg["HPLUS_sign"], reg["HMINUS_sign"]]
    sign = r186.r179.arb_sign
    selected = [
        sign(left) if sign(left) in STRICT else sign(right)
        for left, right in zip(direct, centered)
    ]
    if selected == expected:
        return "MATCH", {"actual": selected, "expected": expected}
    for kind, actual, wanted in zip(kinds, selected, expected):
        if actual in STRICT and actual != wanted:
            return "STRICT_EXCLUDE", {
                "factor": kind, "actual": actual, "expected": wanted,
            }
    for source, enclosures in (("DIRECT", direct), ("CENTERED", centered)):
        for kind, value, wanted in zip(kinds, enclosures, expected):
            if weak_opposite(value, wanted):
                return "WEAK_EXCLUDE", {
                    "factor": kind, "enclosure_source": source,
                    "enclosure": arbtext(value), "expected": wanted,
                }
    for kind, wanted in zip(kinds, expected):
        def at(point: list[Fraction], selected_kind: str = kind) -> Any:
            point_box = G["r174"].atlas.AtlasBox(
                *point, 0, label + ":monotone-corner"
            )
            return r186.factor_geometry(
                collar["chart"], collar["owner_target"], point_box
            )[selected_kind][0]
        proof = monotone_opposite(geometry[kind], wanted, values, at)
        if proof is not None:
            proof["factor"] = kind
            return "MONOTONE_EXCLUDE", proof
    return "UNRESOLVED", {"expected": expected}


def relation204(
    oid: str, values: list[Fraction], label: str
) -> tuple[str, dict[str, Any]]:
    reg = G["reg204"][oid]
    collar = G["scope182"]["collars"][reg["occurrence_row_id"]]
    wall = G["scope179"]["walls"][reg["occurrence_row_id"]]
    r179 = G["r179"]
    box = G["r174_204"].atlas.AtlasBox(*values, 0, label)
    geometry = r179.independent_geometry(
        collar["chart"], collar["owner_target"], box
    )
    source_name = G["r204"].CHART_CONTRACT[collar["chart"]][2]
    target_name = "hit_x" if wall["axis"] == "X" else "hit_y"
    names = (source_name, target_name)
    wall_values = (0, wall["integer_wall"])
    duals = [
        r179.subtract_wall(geometry[name], wall_value)
        for name, wall_value in zip(names, wall_values)
    ]
    expected = [
        "STRICT_" + reg["source_sign"],
        "STRICT_" + reg["target_factor_sign"],
    ]
    actual = [r179.arb_sign(dual[0]) for dual in duals]
    if actual == expected:
        return "MATCH", {"actual": actual, "expected": expected}
    for name, value, wanted in zip(names, actual, expected):
        if value in STRICT and value != wanted:
            return "STRICT_EXCLUDE", {
                "factor": name, "actual": value, "expected": wanted,
            }
    for name, dual, wanted in zip(names, duals, expected):
        if weak_opposite(dual[0], wanted):
            return "WEAK_EXCLUDE", {
                "factor": name, "enclosure": arbtext(dual[0]), "expected": wanted,
            }
    for name, wall_value, dual, wanted in zip(
        names, wall_values, duals, expected
    ):
        def at(
            point: list[Fraction],
            selected_name: str = name,
            selected_wall: int = wall_value,
        ) -> Any:
            point_box = G["r174_204"].atlas.AtlasBox(
                *point, 0, label + ":monotone-corner"
            )
            point_geometry = r179.independent_geometry(
                collar["chart"], collar["owner_target"], point_box
            )
            return r179.subtract_wall(
                point_geometry[selected_name], selected_wall
            )[0]
        proof = monotone_opposite(dual, wanted, values, at)
        if proof is not None:
            proof["factor"] = name
            return "MONOTONE_EXCLUDE", proof
    return "UNRESOLVED", {"expected": expected}


def face(row: dict[str, Any]) -> list[Fraction]:
    ids = row["occurrence_row_ids"]
    axis = row["face_axis"]
    coordinate = Fraction(row["face_coordinate"])
    left, right = G["boxes"][ids[0]], G["boxes"][ids[1]]
    output = []
    for index in range(3):
        output += (
            [coordinate, coordinate] if index == axis
            else [
                max(left[2 * index], right[2 * index]),
                min(left[2 * index + 1], right[2 * index + 1]),
            ]
        )
    return output


def cell(
    face_values: list[Fraction], axis: int, depth: int, i: int, j: int
) -> list[Fraction]:
    output = list(face_values)
    transverse = [index for index in range(3) if index != axis]
    pieces = 2 ** depth
    for index, cell_index in zip(transverse, (i, j)):
        lower = face_values[2 * index]
        step = (face_values[2 * index + 1] - lower) / pieces
        output[2 * index] = lower + cell_index * step
        output[2 * index + 1] = lower + (cell_index + 1) * step
    return output


def update_trace(
    hasher: Any, record: list[Any]
) -> None:
    encoded = canonical(record)
    hasher.update(len(encoded).to_bytes(8, "big"))
    hasher.update(encoded)


def classify(
    args: tuple[int, dict[str, Any], dict[str, Any]]
) -> dict[str, Any]:
    index, source, baseline = args
    ids = source["occurrence_row_ids"]
    axis = source["face_axis"]
    coordinate = Fraction(source["face_coordinate"])
    face_values = face(source)
    is208 = source["geometry_channel"] == "ROUND208_FACTOR_COMMON_FACE"
    strict_state = strict_state208 if is208 else strict_state204
    relation = relation208 if is208 else relation204
    channel = (
        "ROUND208_FACTOR_MONOTONE_DEEP_FACE"
        if is208 else "ROUND204_TARGET_GRAPH_MONOTONE_DEEP_FACE"
    )

    # Replay Round261 exactly at its inherited 53-bit precision.
    ctx.prec = 53
    eligible = [(0, 0)]
    baseline_trace = hashlib.sha256()
    update_trace(
        baseline_trace,
        [
            "cm2.round262.baseline-classification-trace.v1",
            source["Round258_boundary_face_candidate_id"],
            53,
        ],
    )
    baseline_evaluations = 0
    for depth in range(1, 9):
        children = []
        for parent_i, parent_j in eligible:
            for di, dj in ((0, 0), (0, 1), (1, 0), (1, 1)):
                i, j = 2 * parent_i + di, 2 * parent_j + dj
                box = cell(face_values, axis, depth, i, j)
                states = [
                    strict_state(
                        oid, box, f"round262-baseline:{index}:{depth}:{i}:{j}:{oid}"
                    )
                    for oid in ids
                ]
                baseline_evaluations += 2
                update_trace(baseline_trace, [depth, i, j, states])
                need(states != ["MATCH", "MATCH"], f"Round261 residual match:{index}")
                if "STRICT_EXCLUDE" not in states:
                    children.append((i, j))
        eligible = children
        need(eligible, f"Round261 residual exhausted:{index}:{depth}")
    need(
        len(eligible) == baseline["unresolved_depth_8_cell_count"],
        f"Round261 depth8 frontier replay:{index}",
    )
    need(
        baseline_evaluations == baseline["evaluated_cell_side_count"],
        f"Round261 evaluation-count replay:{index}",
    )
    baseline_depth8_count = len(eligible)

    # Re-evaluate that exact frontier at fixed 256-bit precision, then deepen.
    ctx.prec = 256
    enhanced_trace = hashlib.sha256()
    update_trace(
        enhanced_trace,
        [
            "cm2.round262.enhanced-classification-trace.v1",
            source["Round258_boundary_face_candidate_id"],
            256,
        ],
    )
    state_histogram: Counter[tuple[str, str]] = Counter()
    proof_kind_histogram: Counter[str] = Counter()
    enhanced_evaluations = 0

    def evaluate_box(
        depth: int, i: int, j: int, box: list[Fraction]
    ) -> tuple[list[str], list[dict[str, Any]]]:
        nonlocal enhanced_evaluations
        pairs = [
            relation(
                oid, box, f"round262-enhanced:{index}:{depth}:{i}:{j}:{oid}"
            )
            for oid in ids
        ]
        states = [pair[0] for pair in pairs]
        proofs = [pair[1] for pair in pairs]
        enhanced_evaluations += 2
        state_histogram[tuple(states)] += 1
        proof_kind_histogram.update(states)
        update_trace(
            enhanced_trace,
            [depth, i, j, [
                [state, digest(proof)] for state, proof in pairs
            ]],
        )
        return states, proofs

    def corridors(
        patch: list[Fraction], depth: int, i: int, j: int
    ) -> list[dict[str, Any]]:
        output = []
        for oid in ids:
            source_box = G["boxes"][oid]
            found = None
            for normal_depth in range(1, 41):
                candidate = list(patch)
                span = source_box[2 * axis + 1] - source_box[2 * axis]
                thickness = span / (2 ** normal_depth)
                if source_box[2 * axis + 1] == coordinate:
                    candidate[2 * axis:2 * axis + 2] = [
                        coordinate - thickness, coordinate,
                    ]
                    side = "LOWER_SIDE_CORRIDOR"
                elif source_box[2 * axis] == coordinate:
                    candidate[2 * axis:2 * axis + 2] = [
                        coordinate, coordinate + thickness,
                    ]
                    side = "UPPER_SIDE_CORRIDOR"
                else:
                    raise RuntimeError(f"incidence:{index}:{oid}")
                final_state, final_evidence = (
                    strict_evidence208(
                        oid, candidate,
                        f"round262-corridor:{index}:{depth}:{i}:{j}:{oid}:{normal_depth}",
                    )
                    if is208 else
                    strict_evidence204(
                        oid, candidate,
                        f"round262-corridor:{index}:{depth}:{i}:{j}:{oid}:{normal_depth}",
                    )
                )
                if final_state == "MATCH":
                    need(thickness > 0, f"positive corridor thickness:{index}:{oid}")
                    found = {
                        "occurrence_row_id": oid,
                        "corridor_side": side,
                        "dyadic_normal_depth": normal_depth,
                        "exact_normal_thickness": qtext(thickness),
                        "exact_corridor_box": [qtext(value) for value in candidate],
                        "strict_state": final_state,
                        "strict_state_evidence": final_evidence,
                        "strict_state_evidence_sha256": digest(final_evidence),
                    }
                    break
            need(found is not None, f"corridor depth40:{index}:{oid}")
            output.append(found)
        need(
            {row["corridor_side"] for row in output}
            == {"LOWER_SIDE_CORRIDOR", "UPPER_SIDE_CORRIDOR"},
            f"opposite corridor sides:{index}",
        )
        return output

    refined = []
    for i, j in eligible:
        box = cell(face_values, axis, 8, i, j)
        states, _ = evaluate_box(8, i, j, box)
        if states == ["MATCH", "MATCH"]:
            return {
                "source_id": source["Round258_boundary_face_candidate_id"],
                "status": "ACCEPT", "channel": channel, "face_depth": 8,
                "cell_index": [i, j],
                "cell": [qtext(value) for value in box],
                "corridors": corridors(box, 8, i, j),
                "baseline_depth8_cell_count": baseline_depth8_count,
                "baseline_evaluated_cell_side_count": baseline_evaluations,
                "baseline_trace_sha256": baseline_trace.hexdigest(),
                "enhanced_evaluated_cell_side_count": enhanced_evaluations,
                "enhanced_trace_sha256": enhanced_trace.hexdigest(),
                "state_pair_histogram": {
                    "|".join(key): value for key, value in sorted(state_histogram.items())
                },
                "proof_kind_histogram": dict(sorted(proof_kind_histogram.items())),
            }
        if not any(state.endswith("EXCLUDE") for state in states):
            refined.append((i, j))
    eligible = refined
    if not eligible:
        return {
            "source_id": source["Round258_boundary_face_candidate_id"],
            "status": "REJECT_MONOTONE_TREE_EXHAUSTED",
            "channel": channel, "exhaustion_depth": 8,
            "baseline_depth8_cell_count": baseline_depth8_count,
            "baseline_evaluated_cell_side_count": baseline_evaluations,
            "baseline_trace_sha256": baseline_trace.hexdigest(),
            "enhanced_evaluated_cell_side_count": enhanced_evaluations,
            "enhanced_trace_sha256": enhanced_trace.hexdigest(),
            "state_pair_histogram": {
                "|".join(key): value for key, value in sorted(state_histogram.items())
            },
            "proof_kind_histogram": dict(sorted(proof_kind_histogram.items())),
        }

    for depth in range(9, MAX_DEPTH + 1):
        children = []
        for parent_i, parent_j in eligible:
            for di, dj in ((0, 0), (0, 1), (1, 0), (1, 1)):
                i, j = 2 * parent_i + di, 2 * parent_j + dj
                box = cell(face_values, axis, depth, i, j)
                states, _ = evaluate_box(depth, i, j, box)
                if states == ["MATCH", "MATCH"]:
                    return {
                        "source_id": source["Round258_boundary_face_candidate_id"],
                        "status": "ACCEPT", "channel": channel,
                        "face_depth": depth, "cell_index": [i, j],
                        "cell": [qtext(value) for value in box],
                        "corridors": corridors(box, depth, i, j),
                        "baseline_depth8_cell_count": baseline_depth8_count,
                        "baseline_evaluated_cell_side_count": baseline_evaluations,
                        "baseline_trace_sha256": baseline_trace.hexdigest(),
                        "enhanced_evaluated_cell_side_count": enhanced_evaluations,
                        "enhanced_trace_sha256": enhanced_trace.hexdigest(),
                        "state_pair_histogram": {
                            "|".join(key): value
                            for key, value in sorted(state_histogram.items())
                        },
                        "proof_kind_histogram": dict(
                            sorted(proof_kind_histogram.items())
                        ),
                    }
                if not any(state.endswith("EXCLUDE") for state in states):
                    children.append((i, j))
        eligible = children
        if not eligible:
            return {
                "source_id": source["Round258_boundary_face_candidate_id"],
                "status": "REJECT_MONOTONE_TREE_EXHAUSTED",
                "channel": channel, "exhaustion_depth": depth,
                "baseline_depth8_cell_count": baseline_depth8_count,
                "baseline_evaluated_cell_side_count": baseline_evaluations,
                "baseline_trace_sha256": baseline_trace.hexdigest(),
                "enhanced_evaluated_cell_side_count": enhanced_evaluations,
                "enhanced_trace_sha256": enhanced_trace.hexdigest(),
                "state_pair_histogram": {
                    "|".join(key): value for key, value in sorted(state_histogram.items())
                },
                "proof_kind_histogram": dict(sorted(proof_kind_histogram.items())),
            }
    return {
        "source_id": source["Round258_boundary_face_candidate_id"],
        "status": "DEFER_UNRESOLVED_AFTER_MONOTONE_DEPTH_24",
        "channel": channel, "unresolved_depth_24_cell_count": len(eligible),
        "baseline_depth8_cell_count": baseline_depth8_count,
        "baseline_evaluated_cell_side_count": baseline_evaluations,
        "baseline_trace_sha256": baseline_trace.hexdigest(),
        "enhanced_evaluated_cell_side_count": enhanced_evaluations,
        "enhanced_trace_sha256": enhanced_trace.hexdigest(),
        "state_pair_histogram": {
            "|".join(key): value for key, value in sorted(state_histogram.items())
        },
        "proof_kind_histogram": dict(sorted(proof_kind_histogram.items())),
    }


def build(workers: int) -> dict[str, Any]:
    ctx.prec = 53
    round260 = load_result(
        "cm2_round260_source_g_curved_region_common_face_refinement_certificate.json"
    )
    round261 = load_result(
        "cm2_round261_source_g_adaptive_common_face_strict_separation_certificate.json"
    )
    need(
        round261["census"]["deferred_after_depth_8_face_count"] == 1_616
        and round261["census"]["deferred_Round208_face_count"] == 1_528
        and round261["census"]["deferred_Round204_face_count"] == 88
        and round261["census"]["unresolved_depth_8_cell_count"] == 182_072
        and round261["census"]["post_Round261_component_count"] == 68_748,
        "Round261 baseline",
    )
    load_geometry()
    source_by_id = {
        row["Round258_boundary_face_candidate_id"]: row
        for row in round260[
            "formal_deferred_deeper_common_face_refinement_ledger"
        ]["rows"]
    }
    deferred = round261["formal_deferred_depth_8_face_ledger"]["rows"]
    tasks = [
        (index, source_by_id[row["Round258_boundary_face_candidate_id"]], row)
        for index, row in enumerate(deferred, 1)
    ]
    with mp.get_context("fork").Pool(workers) as pool:
        results = list(pool.imap(classify, tasks, chunksize=2))

    map260 = {
        row["Round259_quotient_component_id"]:
            row["post_Round260_quotient_component_id"]
        for row in round260[
            "formal_Round259_to_Round260_component_map_ledger"
        ]["rows"]
    }
    map261 = {
        row["Round260_quotient_component_id"]:
            row["post_Round261_quotient_component_id"]
        for row in round261[
            "formal_Round260_to_Round261_component_map_ledger"
        ]["rows"]
    }
    accepted, rejected, remaining = [], [], []
    pairs: set[tuple[str, str]] = set()
    counts: Counter[str] = Counter()
    face_depths: Counter[tuple[str, int]] = Counter()
    rejection_depths: Counter[tuple[str, int]] = Counter()
    normal_depths: Counter[int] = Counter()
    proof_kinds: Counter[str] = Counter()
    baseline_evaluations = enhanced_evaluations = 0
    area = volume = Fraction(0)
    unresolved_cells = 0
    for result in results:
        source = source_by_id[result["source_id"]]
        counts[result["status"]] += 1
        counts[result["channel"] + ":" + result["status"]] += 1
        baseline_evaluations += result["baseline_evaluated_cell_side_count"]
        enhanced_evaluations += result["enhanced_evaluated_cell_side_count"]
        proof_kinds.update(result["proof_kind_histogram"])
        current = tuple(sorted(
            map261[map260[value]]
            for value in source["pre_Round260_component_ids"]
        ))
        common = {
            "Round258_boundary_face_candidate_id": result["source_id"],
            "official_key_id": source["official_key_id"],
            "source_chart": source["source_chart"],
            "face_axis": source["face_axis"],
            "face_coordinate": source["face_coordinate"],
            "occurrence_row_ids": source["occurrence_row_ids"],
            "pre_Round262_component_ids": list(current),
            "geometry_channel": result["channel"],
            "Round261_unresolved_depth_8_cell_count":
                result["baseline_depth8_cell_count"],
            "Round261_baseline_evaluated_cell_side_count":
                result["baseline_evaluated_cell_side_count"],
            "Round261_baseline_classification_trace_sha256":
                result["baseline_trace_sha256"],
            "Round262_enhanced_evaluated_cell_side_count":
                result["enhanced_evaluated_cell_side_count"],
            "Round262_enhanced_classification_trace_sha256":
                result["enhanced_trace_sha256"],
            "Round262_state_pair_histogram": result["state_pair_histogram"],
            "Round262_proof_kind_histogram": result["proof_kind_histogram"],
        }
        if result["status"] == "ACCEPT":
            if current[0] != current[1]:
                pairs.add(current)
            patch_area = Fraction(source["parent_exact_common_face_area"]) / (
                4 ** result["face_depth"]
            )
            need(patch_area > 0, f"positive patch area:{result['source_id']}")
            area += patch_area
            face_depths[(result["channel"], result["face_depth"])] += 1
            for corridor in result["corridors"]:
                normal_depths[corridor["dyadic_normal_depth"]] += 1
                volume += patch_area * Fraction(
                    corridor["exact_normal_thickness"]
                )
            accepted.append(closed({
                "accepted_monotone_deep_face_patch_row_id":
                    "round262-accepted-monotone-deep-face:" + digest(
                        [result["source_id"]]
                    ),
                **common,
                "dyadic_face_refinement_depth": result["face_depth"],
                "dyadic_face_cell_index": result["cell_index"],
                "exact_common_face_patch_box": result["cell"],
                "exact_common_face_patch_area": qtext(patch_area),
                "strict_two_sided_corridor_proofs": result["corridors"],
                "disposition":
                    "ACCEPT_FIXED_PRECISION_STRICT_COMMON_FACE_WITH_CORRIDORS",
                "physical_glue_credit": 1,
                "maximality_credit": 0,
            }))
        elif result["status"].startswith("REJECT"):
            rejection_depths[(result["channel"], result["exhaustion_depth"])] += 1
            rejected.append(closed({
                "monotone_exhausted_face_row_id":
                    "round262-monotone-exhausted-face:" + digest(
                        [result["source_id"]]
                    ),
                **common,
                "monotone_tree_exhaustion_depth": result["exhaustion_depth"],
                "disposition": result["status"],
                "physical_glue_credit": 0,
                "maximality_credit": 0,
            }))
        else:
            unresolved_cells += result["unresolved_depth_24_cell_count"]
            remaining.append(closed({
                "Round262_deferred_face_row_id":
                    "round262-deferred-face:" + digest([result["source_id"]]),
                **common,
                "unresolved_depth_24_cell_count":
                    result["unresolved_depth_24_cell_count"],
                "disposition": result["status"],
                "physical_glue_credit": 0,
                "maximality_credit": 0,
            }))
    accepted.sort(key=lambda row: row["accepted_monotone_deep_face_patch_row_id"])
    rejected.sort(key=lambda row: row["monotone_exhausted_face_row_id"])
    remaining.sort(key=lambda row: row["Round262_deferred_face_row_id"])
    need(
        len(accepted) + len(rejected) + len(remaining) == 1_616,
        "Round262 partition",
    )

    source_components = round261[
        "formal_post_Round261_component_commitment_ledger"
    ]["rows"]
    keys = {
        row["post_Round261_quotient_component_id"]:
            (row["official_key_id"], row["official_key_ordinal"])
        for row in source_components
    }
    dsu = DSU(sorted(keys))
    rank = 0
    for left, right in sorted(pairs):
        need(keys[left] == keys[right], "Round262 exact-key purity")
        rank += int(dsu.union(left, right))
    members: defaultdict[str, list[str]] = defaultdict(list)
    for component_id in sorted(keys):
        members[dsu.find(component_id)].append(component_id)
    post_by_old: dict[str, str] = {}
    rank_credit_by_old: dict[str, int] = {}
    component_rows = []
    for values in sorted(members.values(), key=lambda group: group[0]):
        key_rows = {keys[value] for value in values}
        need(len(key_rows) == 1, "post-Round262 key purity")
        key_id, ordinal = next(iter(key_rows))
        post = (
            values[0] if len(values) == 1
            else "round262-monotone-deep-face-component:" + digest(values)
        )
        for position, old in enumerate(values):
            post_by_old[old] = post
            rank_credit_by_old[old] = int(position > 0)
        component_rows.append(closed({
            "post_Round262_component_row_id":
                "round262-component-row:" + digest([post]),
            "post_Round262_quotient_component_id": post,
            "official_key_id": key_id,
            "official_key_ordinal": ordinal,
            "constituent_Round261_component_count": len(values),
            "constituent_Round261_component_ids": values,
            "constituent_Round261_component_ids_sha256": digest(values),
            "monotone_deep_face_patch_edge_count": sum(
                1 for pair in pairs if pair[0] in values and pair[1] in values
            ),
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
        }))
    component_rows.sort(key=lambda row: row["post_Round262_quotient_component_id"])
    need(
        len(component_rows) == 68_748 - rank
        and set(post_by_old) == set(keys)
        and sum(rank_credit_by_old.values()) == rank,
        "Round262 component/rank conservation",
    )
    map_rows = [
        closed({
            "Round261_to_Round262_component_map_row_id":
                "round262-component-map:" + digest([old]),
            "Round261_quotient_component_id": old,
            "post_Round262_quotient_component_id": post_by_old[old],
            "component_rank_reduction_credit": rank_credit_by_old[old],
        })
        for old in sorted(keys)
    ]
    frontier = []
    for row in round261["formal_post_Round261_occurrence_frontier_ledger"]["rows"]:
        output = dict(row)
        output.pop("row_sha256")
        old = row["post_Round261_quotient_component_id"]
        output["post_Round262_quotient_component_id"] = post_by_old[old]
        output["Round262_component_remap_indicator"] = int(
            old != post_by_old[old]
        )
        frontier.append(closed(output))
    frontier.sort(key=lambda row: row["post_frontier_row_id"])
    post_component_key = {
        row["post_Round262_quotient_component_id"]: row["official_key_id"]
        for row in component_rows
    }
    need(
        all(
            row["post_Round262_quotient_component_id"] in post_component_key
            and post_component_key[row["post_Round262_quotient_component_id"]]
            == row["official_key_id"]
            for row in frontier
        ),
        "Round262 occurrence frontier component/key conservation",
    )
    component_count = Counter(row["official_key_id"] for row in component_rows)
    accepted_by_key = Counter(row["official_key_id"] for row in accepted)
    rejected_by_key = Counter(row["official_key_id"] for row in rejected)
    deferred_by_key = Counter(row["official_key_id"] for row in remaining)
    key_rows = []
    for source in round261["formal_post_Round261_key_frontier_ledger"]["rows"]:
        key_id = source["official_key_id"]
        key_rows.append(closed({
            "post_Round262_key_frontier_row_id":
                "round262-key-frontier:" + digest([key_id]),
            "official_key_id": key_id,
            "official_key_ordinal": source["official_key_ordinal"],
            "local_occurrence_count": source["local_occurrence_count"],
            "post_Round262_quotient_component_count": component_count[key_id],
            "accepted_monotone_deep_face_patch_count": accepted_by_key[key_id],
            "monotone_exhausted_face_count": rejected_by_key[key_id],
            "deferred_after_depth_24_face_count": deferred_by_key[key_id],
            "occurrence_quotient_assignment_complete": True,
            "all_quotient_components_proved_maximal": False,
            "global_exact_key_fibre_exhausted": False,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    key_rows.sort(key=lambda row: row["official_key_ordinal"])
    need(len(frontier) == 53_968 and len(key_rows) == 116, "Round262 frontiers")

    census = {
        "Round261_residual_face_count": 1_616,
        "Round261_residual_Round208_face_count": 1_528,
        "Round261_residual_Round204_face_count": 88,
        "Round261_unresolved_depth_8_cell_count": 182_072,
        "accepted_monotone_deep_common_face_patch_count": len(accepted),
        "accepted_Round208_patch_count": sum(
            row["geometry_channel"].startswith("ROUND208") for row in accepted
        ),
        "accepted_Round204_patch_count": sum(
            row["geometry_channel"].startswith("ROUND204") for row in accepted
        ),
        "monotone_tree_exhausted_face_count": len(rejected),
        "remaining_fail_closed_face_count": len(remaining),
        "remaining_unresolved_depth_24_cell_count": unresolved_cells,
        "face_depth_histogram": {
            f"{channel}:{depth}": count
            for (channel, depth), count in sorted(face_depths.items())
        },
        "monotone_exhaustion_depth_histogram": {
            f"{channel}:{depth}": count
            for (channel, depth), count in sorted(rejection_depths.items())
        },
        "normal_corridor_depth_histogram": {
            str(depth): normal_depths[depth] for depth in sorted(normal_depths)
        },
        "proof_kind_histogram": dict(sorted(proof_kinds.items())),
        "Round261_baseline_replay_cell_side_count": baseline_evaluations,
        "Round262_enhanced_cell_side_count": enhanced_evaluations,
        "accepted_distinct_current_component_pair_count": len(pairs),
        "rank_reducing_component_pair_count": rank,
        "redundant_certified_component_pair_count": len(pairs) - rank,
        "post_Round261_component_count": 68_748,
        "post_Round262_component_count": len(component_rows),
        "exact_accepted_patch_area_sum": qtext(area),
        "exact_two_sided_corridor_volume_sum": qtext(volume),
        "accepted_candidate_ids_sha256": digest(sorted(
            row["Round258_boundary_face_candidate_id"] for row in accepted
        )),
        "rejected_candidate_ids_sha256": digest(sorted(
            row["Round258_boundary_face_candidate_id"] for row in rejected
        )),
        "deferred_candidate_ids_sha256": digest(sorted(
            row["Round258_boundary_face_candidate_id"] for row in remaining
        )),
        "occurrence_assignment_count": 53_968,
        "exact_key_count": 116,
        "maximal_component_assignment_count": 0,
        "exhausted_fibre_count": 0,
        "global_disposition_count": 0,
        "python_flint_version": FLINT_VERSION,
        "baseline_Arb_precision_bits": 53,
        "enhanced_Arb_precision_bits": 256,
        "maximum_face_refinement_depth": MAX_DEPTH,
    }
    status = (
        f"CERTIFIED_{len(accepted)}_MONOTONE_DEEP_COMMON_FACE_PATCHES__"
        f"{len(rejected)}_EXACT_BOUNDARY_EXHAUSTIONS__"
        f"{rank}_RANK_REDUCTIONS__QUOTIENT_68748_TO_{len(component_rows)}__"
        f"{len(remaining)}_FAIL_CLOSED"
    )
    return {
        "status": status,
        "census": census,
        "formal_input_binding": {name: PINS[name] for name in sorted(PINS)},
        "formal_accepted_monotone_deep_face_patch_ledger": ledger(
            accepted, "accepted_monotone_deep_face_patch_row_id"
        ),
        "formal_monotone_exhausted_face_ledger": ledger(
            rejected, "monotone_exhausted_face_row_id"
        ),
        "formal_deferred_after_depth_24_face_ledger": ledger(
            remaining, "Round262_deferred_face_row_id"
        ),
        "formal_Round261_to_Round262_component_map_ledger": ledger(
            map_rows, "Round261_to_Round262_component_map_row_id"
        ),
        "formal_post_Round262_component_commitment_ledger": ledger(
            component_rows, "post_Round262_component_row_id"
        ),
        "formal_post_Round262_occurrence_frontier_ledger": ledger(
            frontier, "post_frontier_row_id"
        ),
        "formal_post_Round262_key_frontier_ledger": ledger(
            key_rows, "post_Round262_key_frontier_row_id"
        ),
        "scope_contract": {
            "Round261_depth_8_frontier_replayed_at_original_53_bit_precision": True,
            "all_new_geometry_classifications_use_fixed_256_bit_Arb": True,
            "strict_opposite_weak_opposite_and_monotone_corner_cells_are_pruned": True,
            "monotone_corner_proof_requires_strict_derivative_sign_on_every_free_axis": True,
            "weak_opposite_bounds_safely_exclude_requested_strict_sign": True,
            "all_accepted_patches_have_exact_positive_area": True,
            "all_accepted_patches_have_two_sided_strict_3D_corridors": True,
            "all_unresolved_faces_remain_fail_closed": True,
            "common_face_closure_is_not_component_maximality": True,
        },
        "strict_nonpromotion": {
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "audit pinned same-point cross-chart transitions over the complete "
            "53968-occurrence universe"
            if not remaining else
            "apply exact root-order isolation to the remaining fail-closed faces"
        ),
    }


def safe_write(raw: bytes) -> None:
    fd, name = tempfile.mkstemp(prefix=f".{OUTPUT.name}.", dir=OUTPUT.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=WORKERS)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    need(1 <= args.workers <= 48, "workers")
    result = build(args.workers)
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    raw = canonical(document) + b"\n"
    if not args.no_write:
        safe_write(raw)
    print(result["status"])
    print(json.dumps(result["census"], sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
