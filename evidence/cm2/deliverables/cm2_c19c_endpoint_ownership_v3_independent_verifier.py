#!/usr/bin/env python3
"""Independent verifier for the append-only C19C v3 face authority.

The verifier does not import the producer.  It rebuilds the relevant forest
topology and an independent face-neighbor index, then checks every face atom,
all six bits, and the C19C -> C25 -> C26 additive replay.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import random
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_c19c_endpoint_ownership_v3"
AUTHORITY_LEDGER = PREFIX + "_authority_ledger.jsonl.gz"
FACE_ATOM_LEDGER = PREFIX + "_face_atom_ledger.jsonl.gz"
JUNCTION1_LEDGER = PREFIX + "_codimension1_in_face_junction_1d_ledger.jsonl.gz"
JUNCTION0_LEDGER = PREFIX + "_codimension2_in_face_junction_0d_ledger.jsonl.gz"
C19_REPLAY_LEDGER = PREFIX + "_c19c_additive_replay_ledger.jsonl.gz"
C25_REPLAY_LEDGER = PREFIX + "_c25_additive_replay_ledger.jsonl.gz"
C26_REPLAY_LEDGER = PREFIX + "_c26_additive_replay_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"

R171 = "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
R171_VERIFIER = "cm2_round171_compact_gate3_source_g_coordinate_bridge_verifier.py"
SEAM_PRODUCER = "cm2_gate3_chart_seam_quotient_cert.py"
SEAM_VERIFIER = "cm2_gate3_chart_seam_quotient_verifier.py"
GATE3_ATLAS = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
GATE3_SPLIT = "cm2_gate3_ge_interval_atlas_cert.py"
R174_ROWS = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
R174_CERT = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_certificate.json"
R179_ROWS = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R234_CERT = "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"
R235_CERT = "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
C19 = "cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz"
C5 = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_transition_ready_handle_ledger.jsonl.gz"

PINS = {
    R171: "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5",
    R171_VERIFIER: "aee7b3cc3f1468b6a46e7a90e1bb219bd609bddfe54075c6c73e124d98eda7e0",
    SEAM_PRODUCER: "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1",
    SEAM_VERIFIER: "3eb5b5525eab0d2e4935374e6d9fa453717de13634613afa579cd1ae30dbcea6",
    GATE3_ATLAS: "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    GATE3_SPLIT: "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    R174_ROWS: "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R174_CERT: "10221141c58c044b42e43009beb34ae4705995925a88deaa70ff2eba2ea852c7",
    R179_ROWS: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R234_CERT: "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    R235_CERT: "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
    C19: "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84",
    C5: "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333",
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C26: "498088be8302efdf0ed95fb5eca6847fa5d7d3b004af45b9efdf77deaaf80575",
}

T0, T1 = Q(-177, 250), Q(177, 250)
P0, P1 = Q(-1), Q(1)
S0, S1 = Q(-1, 400), Q(1, 400)
GLOBAL = (T0, T1, P0, P1, S0, S1)
AXES = ("t", "p", "s")
FACES = ("t_lower", "t_upper", "p_lower", "p_upper", "s_lower", "s_upper")
BITS = tuple(name + "_closed" for name in FACES)


class Reject(RuntimeError):
    pass


def demand(flag: bool, label: str) -> None:
    if type(flag) is not bool or not flag:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def qbox(values: Iterable[str]) -> tuple[Q, ...]:
    box = tuple(map(Q, values))
    demand(len(box) == 6 and all(box[2 * k] < box[2 * k + 1] for k in range(3)), "box")
    return box


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def row_stream(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for line in stream:
            demand(line.endswith(b"\n"), "row newline")
            raw = line[:-1]
            item = json.loads(raw)
            demand(encode(item) == raw, "canonical row")
            body = dict(item)
            claimed = body.pop("row_sha256", None)
            demand(claimed == digest(body), "closed row")
            yield item


def rows(path: Path) -> list[dict[str, Any]]:
    return list(row_stream(path))


def unpack(document: dict[str, Any], name: str) -> list[dict[str, Any]]:
    columns = document["result"]["row_column_schemas"][name]
    return [dict(zip(columns, packed, strict=True)) for packed in document["result"][name]]


def signs(chart: str) -> tuple[int, int, int]:
    return {"G:E": (1, 1, 1), "G:N": (1, 1, 1), "G:W": (1, -1, -1), "G:S": (1, -1, 1)}[chart]


def orient(chart: str, box: tuple[Q, ...]) -> tuple[Q, ...]:
    answer: list[Q] = []
    for k, sign in enumerate(signs(chart)):
        lo, hi = box[2 * k], box[2 * k + 1]
        answer.extend((lo, hi) if sign == 1 else (-hi, -lo))
    return tuple(answer)


def bisect_box(box: tuple[Q, ...], axis: int, child: int) -> tuple[Q, ...]:
    values = list(box)
    mid = (values[2 * axis] + values[2 * axis + 1]) / 2
    values[2 * axis + (1 if child == 0 else 0)] = mid
    return tuple(values)


def token(value: str) -> tuple[int, int]:
    demand(type(value) is str and len(value) == 2 and value[0] in "tps" and value[1] in "01", "token")
    return "tps".index(value[0]), int(value[1])


def replay(box: tuple[Q, ...], path: Iterable[str]) -> tuple[Q, ...]:
    for item in path:
        axis, child = token(item)
        box = bisect_box(box, axis, child)
    return box


def verify_tree(path_list: list[tuple[str, ...]], label: str) -> tuple[int, int]:
    terminal = set(path_list)
    demand(len(terminal) == len(path_list), label + " duplicate")
    stack = [()]
    seen_internal = 0
    seen_terminal = 0
    while stack:
        prefix = stack.pop()
        if prefix in terminal:
            demand(not any(len(path) > len(prefix) and path[:len(prefix)] == prefix for path in terminal), label + " prefix")
            seen_terminal += 1
            continue
        next_tokens = {path[len(prefix)] for path in terminal if len(path) > len(prefix) and path[:len(prefix)] == prefix}
        demand(bool(next_tokens), label + " hole")
        axes = {token(item)[0] for item in next_tokens}
        demand(len(axes) == 1, label + " axes")
        axis = next(iter(axes))
        expected = {AXES[axis] + "0", AXES[axis] + "1"}
        demand(next_tokens == expected, label + " sibling")
        seen_internal += 1
        stack.extend(prefix + (item,) for item in expected)
    return seen_terminal, seen_internal


@dataclass(frozen=True)
class Leaf:
    identifier: str
    chart: str
    box: tuple[Q, ...]
    disposition: str


@dataclass
class INode:
    pivot: Q
    crossing: list[Leaf]
    smaller: "INode | None"
    larger: "INode | None"


@dataclass
class BVH:
    bounds: tuple[Q, ...]
    left: "BVH | None" = None
    right: "BVH | None" = None
    content: list[Leaf] | None = None


def make_bvh(content: list[Leaf]) -> BVH:
    demand(bool(content), "BVH content")
    bounds = tuple(
        value
        for axis in range(3)
        for value in (
            min(leaf.box[2 * axis] for leaf in content),
            max(leaf.box[2 * axis + 1] for leaf in content),
        )
    )
    if len(content) <= 16:
        return BVH(bounds=bounds, content=content)
    spans = [bounds[2 * axis + 1] - bounds[2 * axis] for axis in range(3)]
    axis = max(range(3), key=spans.__getitem__)
    ordered = sorted(content, key=lambda leaf: (leaf.box[2 * axis] + leaf.box[2 * axis + 1], leaf.identifier))
    middle = len(ordered) // 2
    return BVH(bounds=bounds, left=make_bvh(ordered[:middle]), right=make_bvh(ordered[middle:]))


def point_query(node: BVH, point: tuple[Q, Q, Q], output: list[Leaf]) -> None:
    if any(not (node.bounds[2 * axis] <= point[axis] <= node.bounds[2 * axis + 1]) for axis in range(3)):
        return
    if node.content is not None:
        output.extend(
            leaf for leaf in node.content
            if all(leaf.box[2 * axis] <= point[axis] <= leaf.box[2 * axis + 1] for axis in range(3))
        )
        return
    demand(node.left is not None and node.right is not None, "BVH children")
    point_query(node.left, point, output)
    point_query(node.right, point, output)


def line_query(
    node: BVH,
    fixed: dict[int, Q],
    variable_axis: int,
    lo: Q,
    hi: Q,
    output: list[Leaf],
) -> None:
    if not (node.bounds[2 * variable_axis] < hi and lo < node.bounds[2 * variable_axis + 1]):
        return
    if any(not (node.bounds[2 * axis] <= value <= node.bounds[2 * axis + 1]) for axis, value in fixed.items()):
        return
    if node.content is not None:
        for leaf in node.content:
            if not (leaf.box[2 * variable_axis] < hi and lo < leaf.box[2 * variable_axis + 1]):
                continue
            if all(leaf.box[2 * axis] <= value <= leaf.box[2 * axis + 1] for axis, value in fixed.items()):
                output.append(leaf)
        return
    demand(node.left is not None and node.right is not None, "BVH children")
    line_query(node.left, fixed, variable_axis, lo, hi, output)
    line_query(node.right, fixed, variable_axis, lo, hi, output)


def endpoint_included(chart: str, leaf: Leaf, axis: int, coordinate: Q) -> bool:
    sign = signs(chart)[axis]
    oriented_box = orient(chart, leaf.box)
    oriented_coordinate = sign * coordinate
    lo, hi = oriented_box[2 * axis], oriented_box[2 * axis + 1]
    demand(lo <= oriented_coordinate <= hi, "endpoint containment")
    if lo < oriented_coordinate < hi:
        return True
    if oriented_coordinate == lo:
        return True
    return axis in {1, 2} and hi == GLOBAL[2 * axis + 1]


def interval_tree(content: list[Leaf], axis: int) -> INode | None:
    if not content:
        return None
    midpoints = sorted((leaf.box[2 * axis] + leaf.box[2 * axis + 1]) / 2 for leaf in content)
    pivot = midpoints[len(midpoints) // 2]
    smaller: list[Leaf] = []
    larger: list[Leaf] = []
    crossing: list[Leaf] = []
    for leaf in content:
        lo, hi = leaf.box[2 * axis], leaf.box[2 * axis + 1]
        if hi <= pivot:
            smaller.append(leaf)
        elif lo >= pivot:
            larger.append(leaf)
        else:
            crossing.append(leaf)
    demand(bool(crossing), "interval tree progress")
    return INode(pivot, crossing, interval_tree(smaller, axis), interval_tree(larger, axis))


def find_intervals(node: INode | None, axis: int, lo: Q, hi: Q, answer: list[Leaf]) -> None:
    if node is None:
        return
    answer.extend(
        leaf for leaf in node.crossing
        if leaf.box[2 * axis] < hi and lo < leaf.box[2 * axis + 1]
    )
    if lo < node.pivot:
        find_intervals(node.smaller, axis, lo, hi, answer)
    if node.pivot < hi:
        find_intervals(node.larger, axis, lo, hi, answer)


def ledger_meta(path: Path, content: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "filename": path.name,
        "row_count": len(content),
        "sha256": file_digest(path),
        "size": path.stat().st_size,
        "row_sequence_sha256": digest([row["row_sha256"] for row in content]),
    }


def verify(candidate: Path, seed: int) -> dict[str, Any]:
    demand(type(seed) is int and seed > 0, "seed")
    for name, pin in PINS.items():
        demand(file_digest(HERE / name) == pin, "input pin:" + name)
    result = read_json(candidate / RESULT)
    body = dict(result)
    claimed = body.pop("result_sha256", None)
    demand(claimed == digest(body), "result closure")
    demand(result["status"] == "PASS_APPEND_ONLY_ENDPOINT_OWNER_AUTHORITY__ZERO_FORMAL_CREDIT", "result status")
    demand(result["input_pins"] == {name: PINS[name] for name in sorted(PINS)}, "result pins")
    demand(result["strict_nonpromotion"]["formal_credit"] == 0 and result["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM", "nonpromotion")
    demand(result["authority"]["direct_charts"] == ["G:E", "G:N"], "direct charts")
    demand(result["authority"]["direct_rule"] == "oriented [lower,upper) on internal faces", "direct owner rule")
    demand(result["authority"]["transported_axis_signs"] == {
        "G:E": [1, 1, 1], "G:N": [1, 1, 1],
        "G:W": [1, -1, -1], "G:S": [1, -1, 1],
    }, "transported axis signs")
    demand(result["authority"]["closed_physical_outer_rule"] == "both p endpoints and both s endpoints included", "outer rule")
    demand(result["authority"]["source_chart_seam_rule"] == "E or W owns; N or S excludes", "seam rule")

    authority = rows(candidate / AUTHORITY_LEDGER)
    atoms = rows(candidate / FACE_ATOM_LEDGER)
    junction1 = rows(candidate / JUNCTION1_LEDGER)
    junction0 = rows(candidate / JUNCTION0_LEDGER)
    replay19 = rows(candidate / C19_REPLAY_LEDGER)
    replay25 = rows(candidate / C25_REPLAY_LEDGER)
    replay26 = rows(candidate / C26_REPLAY_LEDGER)
    actual_ledgers = {
        "authority": ledger_meta(candidate / AUTHORITY_LEDGER, authority),
        "face_atoms": ledger_meta(candidate / FACE_ATOM_LEDGER, atoms),
        "junction_1d": ledger_meta(candidate / JUNCTION1_LEDGER, junction1),
        "junction_0d": ledger_meta(candidate / JUNCTION0_LEDGER, junction0),
        "C19C_additive_replay": ledger_meta(candidate / C19_REPLAY_LEDGER, replay19),
        "C25_additive_replay": ledger_meta(candidate / C25_REPLAY_LEDGER, replay25),
        "C26_additive_replay": ledger_meta(candidate / C26_REPLAY_LEDGER, replay26),
    }
    demand(actual_ledgers == result["ledgers"], "ledger metadata")
    demand(len(authority) == len(replay19) == len(replay25) == len(replay26) == 33_344, "ledger censuses")

    old19 = rows(HERE / C19)
    demand(len(old19) == 33_344, "old C19C census")
    old19_by_mid = {row["member_id"]: row for row in old19}
    target = set(old19_by_mid)
    old25 = {row["member_id"]: row for row in row_stream(HERE / C25) if row["member_id"] in target}
    old26 = {row["owner_member_id"]: row for row in row_stream(HERE / C26) if row["owner_member_id"] in target}
    demand(set(old25) == set(old26) == target, "old replay joins")

    # Full forest topology, rebuilt independently.
    r174 = read_json(HERE / R174_ROWS)
    parents = unpack(r174, "parent_rows")
    parent_by_id = {row["parent_id"]: row for row in parents}
    resolved174 = unpack(r174, "resolved_3d_occurrence_rows")
    residual174 = unpack(r174, "residual_3d_tube_rows")
    guards174 = unpack(r174, "chart_guard_rejection_rows")
    residual_by_id = {row["row_id"]: row for row in residual174}
    terminal_by_parent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in resolved174 + residual174 + guards174:
        terminal_by_parent[row["parent_id"]].append(row)
    shuffled_parents = list(parents)
    random.Random(seed ^ 0xA174).shuffle(shuffled_parents)
    total174_terminal = total174_internal = 0
    for parent in shuffled_parents:
        box = orient(parent["chart"], qbox(parent["box"]))
        paths = [tuple(row["refinement_path"]) for row in terminal_by_parent[parent["parent_id"]]]
        tcount, icount = verify_tree(paths, "R174")
        total174_terminal += tcount
        total174_internal += icount
        for row in terminal_by_parent[parent["parent_id"]]:
            demand(replay(box, row["refinement_path"]) == orient(parent["chart"], qbox(row["box"])), "R174 box replay")

    r179 = read_json(HERE / R179_ROWS)
    origins179 = unpack(r179, "origin_tube_rows")
    resolved179 = unpack(r179, "resolved_3d_child_rows")
    retained179 = unpack(r179, "retained_3d_child_rows")
    guards179 = unpack(r179, "chart_guard_child_rows")
    retained_by_id = {row["row_id"]: row for row in retained179}
    child_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in resolved179 + retained179 + guards179:
        child_index[row["origin_row_id"]].append(row)
    shuffled_origins = list(origins179)
    random.Random(seed ^ 0xA179).shuffle(shuffled_origins)
    for summary in shuffled_origins:
        origin = residual_by_id[summary["origin_row_id"]]
        children = child_index[summary["origin_row_id"]]
        demand(len(children) == 2 and {row["child_index"] for row in children} == {0, 1}, "R179 siblings")
        axis = AXES.index(summary["chosen_split_axis"])
        for child in children:
            demand(bisect_box(qbox(origin["box"]), axis, child["child_index"]) == qbox(child["box"]), "R179 replay")

    r234 = read_json(HERE / R234_CERT)["result"]
    selected = {row["Round179_retained_child_row_id"] for row in r234["root_summary_rows"]}
    grouped234: dict[str, list[tuple[tuple[str, ...], dict[str, Any], str]]] = defaultdict(list)
    for disposition, collection in (
        ("R234_RESOLVED", r234["resolved_descendant_rows"]),
        ("R234_GUARD", r234["guard_descendant_rows"]),
        ("R234_FRONTIER", r234["depth6_frontier_rows"]),
    ):
        for row in collection:
            grouped234[row["Round179_retained_child_row_id"]].append((tuple("t" + str(bit) for bit in row["binary_t_path"]), row, disposition))
    total234_terminal = total234_internal = 0
    for root_id in sorted(selected):
        root = retained_by_id[root_id]
        tcount, icount = verify_tree([item[0] for item in grouped234[root_id]], "R234")
        total234_terminal += tcount
        total234_internal += icount
        for path, row, _disp in grouped234[root_id]:
            demand(replay(qbox(root["box"]), path) == qbox(row["box"]), "R234 replay")

    leaves: list[Leaf] = []
    for disposition, collection, key in (
        ("R174_RESOLVED", resolved174, "row_id"),
        ("R174_CHART_GUARD", guards174, "row_id"),
        ("R179_RESOLVED", resolved179, "row_id"),
        ("R179_CHART_GUARD", guards179, "row_id"),
    ):
        leaves.extend(Leaf(row[key], row["chart"], qbox(row["box"]), disposition) for row in collection)
    leaves.extend(Leaf(row["row_id"], row["chart"], qbox(row["box"]), "R179_RETAINED_OTHER_KERNEL") for row in retained179 if row["row_id"] not in selected)
    for disposition, collection, key in (
        ("R234_RESOLVED", r234["resolved_descendant_rows"], "materialized_row_id"),
        ("R234_GUARD", r234["guard_descendant_rows"], "materialized_row_id"),
        ("R234_FRONTIER", r234["depth6_frontier_rows"], "frontier_row_id"),
    ):
        leaves.extend(Leaf(row[key], row["chart"], qbox(row["box"]), disposition) for row in collection)
    demand(len(leaves) == 245_188, "terminal leaf census")

    # Independent virtual depth-eight complement construction.
    prefixes: dict[tuple[str, int, int], list[str]] = defaultdict(list)
    for parent in parents:
        raw = parent["leaf_id"][2:] if parent["leaf_id"].startswith(("V.", "H.")) else parent["leaf_id"]
        a, b, path = raw.split(".")
        prefixes[(parent["chart"], int(a), int(b))].append(path)
    for chart in ("G:E", "G:W", "G:N", "G:S"):
        for i in range(8):
            for j in range(16):
                base = (T0 + (T1 - T0) * Q(i, 8), T0 + (T1 - T0) * Q(i + 1, 8), P0 + (P1 - P0) * Q(j, 16), P0 + (P1 - P0) * Q(j + 1, 16), S0, S1)
                for value in range(256):
                    bits = format(value, "08b")
                    if any(bits.startswith(prefix) for prefix in prefixes[(chart, i, j)]):
                        continue
                    box = base
                    for bit in bits:
                        widths = [box[2 * k + 1] - box[2 * k] for k in range(3)]
                        axis = max(range(3), key=widths.__getitem__)
                        box = bisect_box(box, axis, int(bit))
                    identifier = f"v3-gate3-other-kernel-microcell:{chart}:{i:02d}:{j:02d}:{bits}"
                    leaves.append(Leaf(identifier, chart, orient(chart, box), "GATE3_OTHER_SUPPORT_KERNEL_VIRTUAL_DEPTH8_COMPLEMENT"))

    leaf_by_id = {leaf.identifier: leaf for leaf in leaves}
    demand(len(leaf_by_id) == len(leaves), "terminal/complement leaf identifiers")
    chart_bvh = {
        chart: make_bvh([leaf for leaf in leaves if leaf.chart == chart])
        for chart in ("G:E", "G:W", "G:N", "G:S")
    }

    auth_by_mid = {row["member_id"]: row for row in authority}
    demand(len(auth_by_mid) == len(authority) and set(auth_by_mid) == target, "authority member set")
    atoms_by_face: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for atom in atoms:
        atoms_by_face[(atom["member_id"], atom["face"])].append(atom)
    demand(len(atoms_by_face) == 33_344 * 6, "face atom group census")

    # Build an independent face index only for coordinates used by authority.
    need_keys: set[tuple[str, int, Q, int]] = set()
    for row in authority:
        box = qbox(row["bounds"])
        chart = row["chart"]
        for face_index, disposition in enumerate(row["face_dispositions"]):
            axis, side = divmod(face_index, 2)
            if not disposition["physical_outer"]:
                need_keys.add((chart, axis, box[2 * axis + side], 1 - side))
    face_index: dict[tuple[str, int, Q, int], list[Leaf]] = defaultdict(list)
    for leaf in leaves:
        for axis in range(3):
            for side in (0, 1):
                key = (leaf.chart, axis, leaf.box[2 * axis + side], side)
                if key in need_keys:
                    face_index[key].append(leaf)
    face_trees: dict[tuple[str, int, Q, int], tuple[int, INode | None]] = {}
    for key, content in face_index.items():
        normal = key[1]
        first_tangent = next(axis for axis in range(3) if axis != normal)
        face_trees[key] = (first_tangent, interval_tree(content, first_tangent))

    shuffled_auth = list(authority)
    random.Random(seed ^ 0xBEEF).shuffle(shuffled_auth)
    total_atoms_checked = 0
    other_kernel_checked = 0
    outer_checked = 0
    expected_lines_by_mid: dict[str, set[tuple[int, Q, Q, int, Q, int, Q]]] = defaultdict(set)
    expected_points_by_mid: dict[str, set[tuple[Q, Q, Q]]] = defaultdict(set)
    for auth in shuffled_auth:
        mid = auth["member_id"]
        source = old19_by_mid[mid]
        demand(auth["ordinal"] == source["ordinal"] and auth["C19C_row_sha256"] == source["row_sha256"], "authority/C19C")
        box = qbox(auth["bounds"])
        demand(auth["bounds"] == source["support_ast"]["bounds"], "authority bounds")
        demand(2 * max(abs(box[0]), abs(box[1])) ** 2 < 1, "seam strict interior")
        chart = auth["chart"]
        self_terminal_id = auth["R234_frontier_row_id"]
        demand(self_terminal_id in leaf_by_id, "authority self terminal")
        expected_bits: dict[str, bool] = {}
        demand(len(auth["face_dispositions"]) == 6, "six face dispositions")
        for face_index, disposition in enumerate(auth["face_dispositions"]):
            axis, side = divmod(face_index, 2)
            demand(disposition["face"] == FACES[face_index] and disposition["axis"] == AXES[axis], "face order")
            physical_outer = axis in {1, 2} and box[2 * axis + side] == GLOBAL[2 * axis + side]
            demand(disposition["physical_outer"] is physical_outer, "outer predicate")
            expected_closed = True if physical_outer else ((side if signs(chart)[axis] == 1 else 1 - side) == 0)
            expected_bits[BITS[face_index]] = expected_closed
            demand(disposition["closed"] is expected_closed, "face bit")
            group = sorted(atoms_by_face[(mid, FACES[face_index])], key=lambda row: row["face_atom_ordinal"])
            demand([row["face_atom_ordinal"] for row in group] == list(range(len(group))), "atom ordinals")
            demand(disposition["face_atom_count"] == len(group), "atom count binding")
            demand(disposition["face_atom_row_sequence_sha256"] == digest([row["row_sha256"] for row in group]), "atom sequence binding")
            tangential = [k for k in range(3) if k != axis]
            rect = (box[2 * tangential[0]], box[2 * tangential[0] + 1], box[2 * tangential[1]], box[2 * tangential[1] + 1])
            atom_rectangles: list[tuple[Q, Q, Q, Q]] = []
            for atom in group:
                total_atoms_checked += 1
                demand(atom["member_id"] == mid and atom["chart"] == chart and atom["normal_axis"] == AXES[axis], "atom identity")
                demand(Q(atom["face_coordinate"]) == box[2 * axis + side], "atom coordinate")
                cell = tuple(map(Q, atom["tangential_bounds"]))
                demand(len(cell) == 4 and rect[0] <= cell[0] < cell[1] <= rect[1] and rect[2] <= cell[2] < cell[3] <= rect[3], "atom containment")
                demand(Q(atom["exact_relative_interior_area"]) == (cell[1] - cell[0]) * (cell[3] - cell[2]), "atom area")
                atom_rectangles.append(cell)
                if physical_outer:
                    outer_checked += 1
                    demand(atom["neighbor_terminal_id"] is None and atom["neighbor_disposition"] == "PHYSICAL_OUTER_COMPLEMENT_EMPTY", "outer neighbor")
                    demand(atom["owner_terminal_id"] == self_terminal_id and atom["owner_member_id_if_C19C"] == mid and atom["owner_disposition"] == "SELF_BY_CLOSED_PHYSICAL_OUTER_OVERRIDE", "outer owner")
                else:
                    neighbor_id = atom["neighbor_terminal_id"]
                    demand(neighbor_id in leaf_by_id, "atom neighbor id")
                    neighbor = leaf_by_id[neighbor_id]
                    demand(atom["neighbor_disposition"] == neighbor.disposition and atom["neighbor_box"] == [qstr(value) for value in neighbor.box], "neighbor binding")
                    search_key = (chart, axis, box[2 * axis + side], 1 - side)
                    demand(search_key in face_trees, "face tree key")
                    first_tangent, search_tree = face_trees[search_key]
                    tangent_position = tangential.index(first_tangent)
                    possible_neighbors: list[Leaf] = []
                    find_intervals(
                        search_tree, first_tangent,
                        cell[2 * tangent_position], cell[2 * tangent_position + 1],
                        possible_neighbors,
                    )
                    candidates = []
                    for possible in possible_neighbors:
                        if possible.box[2 * tangential[0]] <= cell[0] and cell[1] <= possible.box[2 * tangential[0] + 1] and possible.box[2 * tangential[1]] <= cell[2] and cell[3] <= possible.box[2 * tangential[1] + 1]:
                            candidates.append(possible.identifier)
                    demand(candidates == [neighbor_id], "unique geometric neighbor on atom")
                    expected_owner = self_terminal_id if expected_closed else neighbor_id
                    demand(atom["owner_terminal_id"] == expected_owner, "atom unique owner")
                    demand(atom["owner_member_id_if_C19C"] == (mid if expected_closed else None), "atom owner member binding")
                    if neighbor.disposition == "GATE3_OTHER_SUPPORT_KERNEL_VIRTUAL_DEPTH8_COMPLEMENT":
                        other_kernel_checked += 1
            # Exact common-refinement coverage, independent of area sum.
            xcuts = sorted({rect[0], rect[1]} | {v for cell in atom_rectangles for v in cell[:2]})
            ycuts = sorted({rect[2], rect[3]} | {v for cell in atom_rectangles for v in cell[2:]})
            for i in range(len(xcuts) - 1):
                for j in range(len(ycuts) - 1):
                    cell = (xcuts[i], xcuts[i + 1], ycuts[j], ycuts[j + 1])
                    covering = [atom for atom in atom_rectangles if atom[0] <= cell[0] and cell[1] <= atom[1] and atom[2] <= cell[2] and cell[3] <= atom[3]]
                    demand(len(covering) == 1, "atom common refinement no gap/no overlap")
            normal_coordinate = box[2 * axis + side]
            for fixed0 in xcuts:
                for index in range(len(ycuts) - 1):
                    fixed = sorted(((axis, normal_coordinate), (tangential[0], fixed0)))
                    expected_lines_by_mid[mid].add((
                        tangential[1], ycuts[index], ycuts[index + 1],
                        fixed[0][0], fixed[0][1], fixed[1][0], fixed[1][1],
                    ))
            for fixed1 in ycuts:
                for index in range(len(xcuts) - 1):
                    fixed = sorted(((axis, normal_coordinate), (tangential[1], fixed1)))
                    expected_lines_by_mid[mid].add((
                        tangential[0], xcuts[index], xcuts[index + 1],
                        fixed[0][0], fixed[0][1], fixed[1][0], fixed[1][1],
                    ))
            for fixed0 in xcuts:
                for fixed1 in ycuts:
                    point = [Q(0), Q(0), Q(0)]
                    point[axis] = normal_coordinate
                    point[tangential[0]] = fixed0
                    point[tangential[1]] = fixed1
                    expected_points_by_mid[mid].add(tuple(point))
        demand(auth["endpoint_inclusion_bits"] == expected_bits, "six-bit vector")

    # Independent codimension-2/3 audit.  A geometric BVH, rather than the
    # producer's subdivision-tree query, recomputes all incident leaves.
    junction1_by_mid: dict[str, list[dict[str, Any]]] = defaultdict(list)
    junction0_by_mid: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in junction1:
        junction1_by_mid[row["member_id"]].append(row)
    for row in junction0:
        junction0_by_mid[row["member_id"]].append(row)
    demand(set(junction1_by_mid) == set(junction0_by_mid) == target, "junction member sets")

    def merged(intervals: list[tuple[Q, Q]], require_disjoint: bool) -> list[tuple[Q, Q]]:
        ordered = sorted(intervals)
        answer: list[tuple[Q, Q]] = []
        for lo, hi in ordered:
            demand(lo < hi, "junction positive interval")
            if not answer or answer[-1][1] < lo:
                answer.append((lo, hi))
                continue
            if require_disjoint:
                demand(answer[-1][1] <= lo, "junction interval overlap")
            answer[-1] = (answer[-1][0], max(answer[-1][1], hi))
        return answer

    checked_junction1 = 0
    checked_junction0 = 0
    for mid in sorted(target):
        auth = auth_by_mid[mid]
        chart = auth["chart"]
        self_terminal = auth["R234_frontier_row_id"]
        local1 = sorted(junction1_by_mid[mid], key=lambda row: row["junction_1d_ordinal"])
        local0 = sorted(junction0_by_mid[mid], key=lambda row: row["junction_0d_ordinal"])
        demand([row["junction_1d_ordinal"] for row in local1] == list(range(len(local1))), "junction1 ordinals")
        demand([row["junction_0d_ordinal"] for row in local0] == list(range(len(local0))), "junction0 ordinals")
        demand(auth["junction_1d_count"] == len(local1) and auth["junction_1d_row_sequence_sha256"] == digest([row["row_sha256"] for row in local1]), "authority junction1 binding")
        demand(auth["junction_0d_count"] == len(local0) and auth["junction_0d_row_sequence_sha256"] == digest([row["row_sha256"] for row in local0]), "authority junction0 binding")

        expected_by_key: dict[tuple[int, int, Q, int, Q], list[tuple[Q, Q]]] = defaultdict(list)
        for var_axis, lo, hi, fixed_axis0, fixed0, fixed_axis1, fixed1 in expected_lines_by_mid[mid]:
            expected_by_key[(var_axis, fixed_axis0, fixed0, fixed_axis1, fixed1)].append((lo, hi))
        actual_by_key: dict[tuple[int, int, Q, int, Q], list[tuple[Q, Q]]] = defaultdict(list)
        expected_points = set(expected_points_by_mid[mid])
        for row in local1:
            checked_junction1 += 1
            demand(row["schema"] == "cm2.c19c-endpoint-ownership-v3.junction-1d-row.v1" and row["member_ordinal"] == auth["ordinal"] and row["formal_credit"] == 0 and row["exactly_one_owner"] is True, "junction1 schema/ordinal")
            var_axis = AXES.index(row["variable_axis"])
            lo, hi = map(Q, row["variable_bounds"])
            fixed_items = sorted((AXES.index(axis), Q(value)) for axis, value in row["fixed_coordinates"].items())
            demand(len(fixed_items) == 2 and var_axis not in {fixed_items[0][0], fixed_items[1][0]}, "junction1 axes")
            key = (var_axis, fixed_items[0][0], fixed_items[0][1], fixed_items[1][0], fixed_items[1][1])
            actual_by_key[key].append((lo, hi))
            fixed = dict(fixed_items)
            incident: list[Leaf] = []
            line_query(chart_bvh[chart], fixed, var_axis, lo, hi, incident)
            covering = [
                leaf for leaf in incident
                if leaf.box[2 * var_axis] <= lo and hi <= leaf.box[2 * var_axis + 1]
            ]
            demand(row["incident_terminal_ids"] == sorted(leaf.identifier for leaf in covering), "junction1 incident set")
            demand(row["incident_terminal_count"] == len(covering), "junction1 incident count")
            owning = [
                leaf for leaf in covering
                if all(endpoint_included(chart, leaf, axis, coordinate) for axis, coordinate in fixed.items())
            ]
            demand(len(owning) == 1, "junction1 exactly one owner")
            owner = owning[0]
            demand(row["owner_terminal_id"] == owner.identifier and row["owner_disposition"] == owner.disposition, "junction1 owner binding")
            demand(row["owner_member_id_if_C19C"] == (mid if owner.identifier == self_terminal else None), "junction1 owner member")
            point0 = [Q(0), Q(0), Q(0)]
            point1 = [Q(0), Q(0), Q(0)]
            point0[var_axis], point1[var_axis] = lo, hi
            for axis, coordinate in fixed.items():
                point0[axis] = point1[axis] = coordinate
            expected_points.add(tuple(point0))
            expected_points.add(tuple(point1))
        demand(set(actual_by_key) == set(expected_by_key), "junction1 line-key completeness")
        for key in expected_by_key:
            demand(merged(actual_by_key[key], True) == merged(expected_by_key[key], False), "junction1 exact line coverage")

        actual_points: set[tuple[Q, Q, Q]] = set()
        for row in local0:
            checked_junction0 += 1
            demand(row["schema"] == "cm2.c19c-endpoint-ownership-v3.junction-0d-row.v1" and row["member_ordinal"] == auth["ordinal"] and row["formal_credit"] == 0 and row["exactly_one_owner"] is True, "junction0 schema/ordinal")
            point = tuple(Q(row["point"][axis]) for axis in AXES)
            demand(point not in actual_points, "junction0 duplicate point")
            actual_points.add(point)
            incident: list[Leaf] = []
            point_query(chart_bvh[chart], point, incident)
            demand(row["incident_terminal_ids"] == sorted(leaf.identifier for leaf in incident), "junction0 incident set")
            demand(row["incident_terminal_count"] == len(incident), "junction0 incident count")
            owning = [
                leaf for leaf in incident
                if all(endpoint_included(chart, leaf, axis, point[axis]) for axis in range(3))
            ]
            demand(len(owning) == 1, "junction0 exactly one owner")
            owner = owning[0]
            demand(row["owner_terminal_id"] == owner.identifier and row["owner_disposition"] == owner.disposition, "junction0 owner binding")
            demand(row["owner_member_id_if_C19C"] == (mid if owner.identifier == self_terminal else None), "junction0 owner member")
        demand(actual_points == expected_points, "junction0 all face-grid and T-break points")

    # Additive replay closure.
    a19 = {row["member_id"]: row for row in replay19}
    a25 = {row["member_id"]: row for row in replay25}
    a26 = {row["member_id"]: row for row in replay26}
    demand(set(a19) == set(a25) == set(a26) == target, "additive replay member sets")
    for mid in sorted(target):
        auth = auth_by_mid[mid]
        old = old19_by_mid[mid]
        expected_ast = {
            "kind": "HALF_OPEN_RATIONAL_BOX_WITH_V3_ENDPOINT_AUTHORITY",
            "coordinates": ["t", "p", "s"],
            "bounds": old["support_ast"]["bounds"],
            "endpoint_inclusion_bits": auth["endpoint_inclusion_bits"],
            "exact_volume": old["support_ast"]["exact_volume"],
            "lineage": old["support_ast"]["lineage"],
            "endpoint_authority_row_sha256": auth["row_sha256"],
        }
        demand(a19[mid]["support_ast"] == expected_ast and a19[mid]["support_ast_sha256"] == digest(expected_ast), "C19C replay")
        demand(a19[mid]["original_C19C_row_sha256"] == old["row_sha256"], "C19C old binding")
        demand(a25[mid]["original_C25_member_row_sha256"] == old25[mid]["row_sha256"] and a25[mid]["v3_C19C_replay_row_sha256"] == a19[mid]["row_sha256"] and a25[mid]["v3_normalized_support_ast_sha256"] == a19[mid]["support_ast_sha256"], "C25 replay")
        demand(a26[mid]["original_C26_handle_row_sha256"] == old26[mid]["row_sha256"] and a26[mid]["v3_C25_replay_row_sha256"] == a25[mid]["row_sha256"] and a26[mid]["v3_owner_normalized_support_ast_sha256"] == a19[mid]["support_ast_sha256"] and a26[mid]["transition_theorem_claimed"] is False, "C26 replay")

    demand(result["forest_proofs"]["R174_prefix_free_sibling_complete"] == {"parent_count": len(parents), "terminal_count": total174_terminal, "internal_count": total174_internal}, "R174 result stats")
    demand(result["forest_proofs"]["R234_prefix_free_sibling_complete"] == {"root_count": len(selected), "terminal_count": total234_terminal, "internal_count": total234_internal}, "R234 result stats")
    demand(result["face_gluing"]["face_atom_count"] == total_atoms_checked, "result atom count")
    demand(result["face_gluing"]["other_support_kernel_face_atom_count"] == other_kernel_checked, "result other-kernel atoms")
    demand(result["face_gluing"]["junction_1d_atom_count"] == checked_junction1 == len(junction1), "result junction1 count")
    demand(result["face_gluing"]["junction_0d_atom_count"] == checked_junction0 == len(junction0), "result junction0 count")

    semantic = {
        "schema": "cm2.c19c-endpoint-ownership-v3.independent-verification.v1",
        "status": "PASS",
        "verification_seed": seed,
        "verified_result_sha256": result["result_sha256"],
        "verified_ledgers": actual_ledgers,
        "randomized_authority_order_sha256": digest([row["member_id"] for row in shuffled_auth]),
        "checks": {
            "R174_prefix_free_sibling_complete": True,
            "R179_exact_two_child_gluing": True,
            "R234_prefix_free_sibling_complete": True,
            "Gate3_other_support_kernel_virtual_completion": True,
            "face_common_refinement_no_gap_no_overlap": True,
            "unique_terminal_neighbor_per_internal_face_atom": True,
            "unique_owner_per_face_atom": True,
            "junction_1d_exact_set_exhaustion": True,
            "junction_1d_incident_sets_rebuilt_by_independent_BVH": True,
            "junction_1d_unique_owner": True,
            "junction_0d_exact_set_exhaustion_including_T_breakpoints": True,
            "junction_0d_incident_sets_rebuilt_by_independent_BVH": True,
            "junction_0d_unique_owner": True,
            "closed_s_outer_override": True,
            "Jx_Jy_axiswise_bit_transport": True,
            "C19C_C25_C26_additive_replay": True,
        },
        "census": {
            "authority_rows": len(authority),
            "face_atoms": total_atoms_checked,
            "outer_face_atoms": outer_checked,
            "other_support_kernel_face_atoms": other_kernel_checked,
            "junction_1d_atoms": checked_junction1,
            "junction_0d_atoms": checked_junction0,
        },
        "formal_credit": 0,
    }
    return {**semantic, "verification_sha256": digest(semantic)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    verification = verify(Path(args.candidate_dir).resolve(), args.seed)
    if args.output:
        Path(args.output).resolve().write_bytes(encode(verification))
    print(encode({"status": verification["status"], "verification_sha256": verification["verification_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
