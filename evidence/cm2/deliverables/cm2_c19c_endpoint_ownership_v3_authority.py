#!/usr/bin/env python3
"""Append-only endpoint-owner authority for the 33,344 C19C boxes.

The old C19C/C25/C26 files are immutable inputs.  This program constructs a
new, zero-credit authority and additive replay.  Its face rule is not a
per-row default: it is the standard lower-closed/upper-open rule in the two
direct Gate3 coordinate charts, transported exactly through the existing
Jx/Jy chart involutions.  Closed physical outer faces are explicit
exceptions.  Every C19C face is glued to a terminal neighbor (or to a closed
physical outer face) through an exact two-dimensional common refinement.

This program never reads C27 FAMILIES or a transition-edge ledger.
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
FACES = (
    "t_lower", "t_upper", "p_lower", "p_upper", "s_lower", "s_upper",
)
BIT_NAMES = tuple(name + "_closed" for name in FACES)


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def filesha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def qbox(values: Iterable[str]) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(len(result) == 6, "box arity")
    need(all(result[2 * i] < result[2 * i + 1] for i in range(3)), "positive box")
    return result


def sbox(values: Iterable[Q]) -> list[str]:
    return [qstr(value) for value in values]


def volume(box: tuple[Q, ...]) -> Q:
    return (box[1] - box[0]) * (box[3] - box[2]) * (box[5] - box[4])


def area(box: tuple[Q, Q, Q, Q]) -> Q:
    return (box[1] - box[0]) * (box[3] - box[2])


def strict_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def closed_rows(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rb") as handle:
        for line in handle:
            need(line.endswith(b"\n"), "unterminated row:" + path.name)
            raw = line[:-1]
            row = json.loads(raw)
            need(canonical(row) == raw, "noncanonical row:" + path.name)
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(claimed == objsha(body), "row closure:" + path.name)
            yield row


def table(document: dict[str, Any], name: str) -> list[dict[str, Any]]:
    columns = document["result"]["row_column_schemas"][name]
    return [dict(zip(columns, packed, strict=True)) for packed in document["result"][name]]


def write_rows(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    raw = b"".join(canonical(row) + b"\n" for row in rows)
    with path.open("wb") as raw_handle:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw_handle, mtime=0) as handle:
            handle.write(raw)
    return {
        "filename": path.name,
        "row_count": len(rows),
        "sha256": filesha(path),
        "size": path.stat().st_size,
        "row_sequence_sha256": objsha([row["row_sha256"] for row in rows]),
    }


def orientation(chart: str) -> tuple[int, int, int]:
    # u is the direct-chart coordinate.  Jx: (t,p,s)->(t,-p,-s);
    # Jy: (t,p,s)->(t,-p,s).
    return {
        "G:E": (1, 1, 1),
        "G:N": (1, 1, 1),
        "G:W": (1, -1, -1),
        "G:S": (1, -1, 1),
    }[chart]


def to_oriented(chart: str, box: tuple[Q, ...]) -> tuple[Q, ...]:
    output: list[Q] = []
    for axis, sign in enumerate(orientation(chart)):
        lo, hi = box[2 * axis], box[2 * axis + 1]
        output.extend((lo, hi) if sign == 1 else (-hi, -lo))
    return tuple(output)


def from_oriented(chart: str, box: tuple[Q, ...]) -> tuple[Q, ...]:
    return to_oriented(chart, box)  # all signs are involutions


def split(box: tuple[Q, ...], axis: int, child: int) -> tuple[Q, ...]:
    need(axis in {0, 1, 2} and child in {0, 1}, "split selector")
    values = list(box)
    middle = (values[2 * axis] + values[2 * axis + 1]) / 2
    if child == 0:
        values[2 * axis + 1] = middle
    else:
        values[2 * axis] = middle
    return tuple(values)


def split_widest(box: tuple[Q, ...], child: int) -> tuple[int, tuple[Q, ...]]:
    widths = tuple(box[2 * i + 1] - box[2 * i] for i in range(3))
    axis = max(range(3), key=lambda i: widths[i])
    return axis, split(box, axis, child)


def parse_token(token: str) -> tuple[int, int]:
    need(type(token) is str and len(token) == 2, "token shape")
    need(token[0] in "tps" and token[1] in "01", "token value")
    return "tps".index(token[0]), int(token[1])


def replay_tokens(box: tuple[Q, ...], tokens: Iterable[str]) -> tuple[Q, ...]:
    current = box
    for token in tokens:
        axis, child = parse_token(token)
        current = split(current, axis, child)
    return current


def complete_binary_trie(paths: list[tuple[str, ...]], label: str) -> dict[str, int]:
    root: dict[Any, Any] = {}
    for path in paths:
        node = root
        for token in path:
            node = node.setdefault(token, {})
        need("_terminal" not in node, label + ":duplicate path")
        node["_terminal"] = True

    internal = 0
    terminal = 0

    def visit(node: dict[Any, Any], prefix: tuple[str, ...]) -> None:
        nonlocal internal, terminal
        children = {key: value for key, value in node.items() if key != "_terminal"}
        if node.get("_terminal"):
            need(not children, label + ":terminal prefix")
            terminal += 1
            return
        need(bool(children), label + ":empty internal")
        axes = {parse_token(key)[0] for key in children}
        need(len(axes) == 1, label + ":mixed split axes")
        axis = next(iter(axes))
        names = {AXES[axis] + "0", AXES[axis] + "1"}
        need(set(children) == names, label + ":missing sibling")
        internal += 1
        for key in sorted(children):
            visit(children[key], prefix + (key,))

    visit(root, ())
    return {"terminal_count": terminal, "internal_count": internal}


def gate3_leaf_replay(chart: str, leaf_id: str) -> tuple[tuple[Q, ...], list[dict[str, Any]]]:
    raw = leaf_id
    if raw.startswith("V.") or raw.startswith("H."):
        raw = raw[2:]
    pieces = raw.split(".")
    need(len(pieces) == 3, "Gate3 leaf id")
    i, j = int(pieces[0]), int(pieces[1])
    bits = pieces[2]
    need(0 <= i < 8 and 0 <= j < 16 and len(bits) <= 8 and set(bits) <= {"0", "1"}, "Gate3 path")
    box = (
        T0 + (T1 - T0) * Q(i, 8), T0 + (T1 - T0) * Q(i + 1, 8),
        P0 + (P1 - P0) * Q(j, 16), P0 + (P1 - P0) * Q(j + 1, 16),
        S0, S1,
    )
    trace: list[dict[str, Any]] = []
    for depth, bit_text in enumerate(bits, 1):
        axis, child_box = split_widest(box, int(bit_text))
        middle = box[2 * axis + 1] if int(bit_text) == 0 else box[2 * axis]
        trace.append({
            "level": "GATE3_ADAPTIVE",
            "depth": depth,
            "axis": AXES[axis],
            "oriented_child": int(bit_text),
            "interface_coordinate_u": qstr(middle),
            "prefix": bits[:depth],
        })
        box = child_box
    return box, trace


@dataclass(frozen=True)
class Leaf:
    leaf_id: str
    chart: str
    box: tuple[Q, ...]
    disposition: str
    source_row_sha256: str | None = None


@dataclass
class IntervalNode:
    center: Q
    crossing: list[Leaf]
    left: "IntervalNode | None"
    right: "IntervalNode | None"


@dataclass
class BSPNode:
    box_u: tuple[Q, ...]
    axis: int | None = None
    split_u: Q | None = None
    lower: "BSPNode | None" = None
    upper: "BSPNode | None" = None
    leaf: Leaf | None = None


def endpoint_included_u(box_u: tuple[Q, ...], axis: int, coordinate: Q) -> bool:
    lo, hi = box_u[2 * axis], box_u[2 * axis + 1]
    need(lo <= coordinate <= hi, "junction coordinate containment")
    if lo < coordinate < hi:
        return True
    if coordinate == lo:
        return True  # standard oriented [lower,upper)
    # Only p and s have serialized closed physical outer endpoints.  C19C is
    # strictly inside the true t chart seam, so conservative t outer is never
    # queried by the junction audit.
    return axis in {1, 2} and hi == GLOBAL[2 * axis + 1]


def collect_line_leaves(
    node: BSPNode,
    fixed_u: dict[int, Q],
    variable_axis: int,
    variable_lo: Q,
    variable_hi: Q,
    output: list[Leaf],
) -> None:
    box = node.box_u
    if not (box[2 * variable_axis] < variable_hi and variable_lo < box[2 * variable_axis + 1]):
        return
    if any(not (box[2 * axis] <= value <= box[2 * axis + 1]) for axis, value in fixed_u.items()):
        return
    if node.leaf is not None:
        output.append(node.leaf)
        return
    need(node.lower is not None and node.upper is not None, "BSP internal children")
    collect_line_leaves(node.lower, fixed_u, variable_axis, variable_lo, variable_hi, output)
    collect_line_leaves(node.upper, fixed_u, variable_axis, variable_lo, variable_hi, output)


def collect_point_leaves(node: BSPNode, point_u: tuple[Q, Q, Q], output: list[Leaf]) -> None:
    box = node.box_u
    if any(not (box[2 * axis] <= point_u[axis] <= box[2 * axis + 1]) for axis in range(3)):
        return
    if node.leaf is not None:
        output.append(node.leaf)
        return
    need(node.lower is not None and node.upper is not None, "BSP internal children")
    collect_point_leaves(node.lower, point_u, output)
    collect_point_leaves(node.upper, point_u, output)


def make_interval_tree(leaves: list[Leaf], tangential_axis: int) -> IntervalNode | None:
    if not leaves:
        return None
    centers = sorted(
        (leaf.box[2 * tangential_axis] + leaf.box[2 * tangential_axis + 1]) / 2
        for leaf in leaves
    )
    center = centers[len(centers) // 2]
    left: list[Leaf] = []
    right: list[Leaf] = []
    crossing: list[Leaf] = []
    for leaf in leaves:
        lo, hi = leaf.box[2 * tangential_axis], leaf.box[2 * tangential_axis + 1]
        if hi <= center:
            left.append(leaf)
        elif lo >= center:
            right.append(leaf)
        else:
            crossing.append(leaf)
    need(bool(crossing), "interval-tree progress")
    return IntervalNode(
        center, crossing,
        make_interval_tree(left, tangential_axis),
        make_interval_tree(right, tangential_axis),
    )


def interval_query(
    node: IntervalNode | None,
    tangential_axis: int,
    lo: Q,
    hi: Q,
    output: list[Leaf],
) -> None:
    if node is None:
        return
    for leaf in node.crossing:
        if leaf.box[2 * tangential_axis] < hi and lo < leaf.box[2 * tangential_axis + 1]:
            output.append(leaf)
    if lo < node.center:
        interval_query(node.left, tangential_axis, lo, hi, output)
    if node.center < hi:
        interval_query(node.right, tangential_axis, lo, hi, output)


def row_identity(row: dict[str, Any], key: str) -> str:
    value = row[key]
    need(type(value) is str, "row identity")
    return value


def build(candidate_dir: Path, seed: int) -> dict[str, Any]:
    need(type(seed) is int and seed > 0, "positive execution seed")
    for name, expected in PINS.items():
        need(filesha(HERE / name) == expected, "input pin:" + name)

    r171 = strict_json(HERE / R171)["result"]
    need(r171["scope"]["adjoined_parameter_domain"] == "s in [-1/400,1/400]", "closed s domain")
    need(
        r171["scope"]["gate3_conservative_domain"]
        == "t in [-177/250,177/250], p in [-1,1], s in [-1/400,1/400]",
        "conservative domain",
    )
    need(r171["exact_source_G_coordinate_bridge"]["p_map_monotone_on_closed_domain"] is True, "closed p domain")
    r174_cert = strict_json(HERE / R174_CERT)["result"]
    need(
        r174_cert["adaptive_recut_contract"]["source_chart_diagonal_half_open_rule"]
        == "E or W owns; N or S excludes",
        "chart seam owner",
    )

    # Immutable C19C targets.
    c19_rows = list(closed_rows(HERE / C19))
    need(len(c19_rows) == 33_344, "C19C census")
    c19_by_mid: dict[str, dict[str, Any]] = {}
    for ordinal, row in enumerate(c19_rows):
        need(row["ordinal"] == ordinal, "C19C order")
        ast = row["support_ast"]
        need(ast["kind"] == "HALF_OPEN_RATIONAL_BOX" and len(ast["bounds"]) == 6, "C19C AST")
        need(all(bit not in ast for bit in BIT_NAMES), "old C19C has no bits")
        need(row["member_id"] not in c19_by_mid, "C19C member uniqueness")
        c19_by_mid[row["member_id"]] = row
    target_ids = set(c19_by_mid)

    # Canonical C5 -> R234 binding.
    r234_doc = strict_json(HERE / R234_CERT)["result"]
    front_index = {row["frontier_row_id"]: row for row in r234_doc["depth6_frontier_rows"]}
    need(len(front_index) == len(r234_doc["depth6_frontier_rows"]) == 38_376, "R234 frontier uniqueness")
    r235_doc = strict_json(HERE / R235_CERT)["result"]
    part_index = {row["endpoint_graph_partition_row_id"]: row for row in r235_doc["single_endpoint_graph_partition_rows"]}
    need(len(part_index) == len(r235_doc["single_endpoint_graph_partition_rows"]) == 38_328, "R235 partition uniqueness")
    c5: dict[str, dict[str, Any]] = {}
    fronts: dict[str, dict[str, Any]] = {}
    for row in closed_rows(HERE / C5):
        semantic = row["semantic_classification"]
        mid = semantic.get("surviving_side_member")
        if mid not in target_ids:
            continue
        need(mid not in c5, "C5 uniqueness")
        need(semantic["classification"] == "EMPTY_GRAPH", "C5 empty graph")
        fref = row["canonical_input_commitment"]["R234_frontier_row"]
        pref = row["canonical_input_commitment"]["R235_partition_row"]
        need(len(fref) == len(pref) == 3 and fref[1] in front_index and pref[1] in part_index, "C5 commitments")
        front = front_index[fref[1]]
        part = part_index[pref[1]]
        need(fref[2] == objsha(front) and pref[2] == objsha(part), "C5 commitment hashes")
        need(part["Round234_frontier_row_id"] == front["frontier_row_id"], "R234/R235 join")
        need(semantic["complete_parameter_domain"]["box"] == front["box"], "C5/R234 bounds")
        need(c19_by_mid[mid]["support_ast"]["bounds"] == front["box"], "C19C/R234 bounds")
        c5[mid], fronts[mid] = row, front
    need(set(c5) == target_ids, "C5 exact target join")

    # Old C25 and C26 rows: one row/handle for every C19C member.
    c25: dict[str, dict[str, Any]] = {}
    for row in closed_rows(HERE / C25):
        mid = row["member_id"]
        if mid in target_ids:
            need(mid not in c25, "C25 uniqueness")
            need(row["source_bindings"]["support_kernel"] == "C19C", "C25 kernel")
            need(row["source_bindings"]["support_kernel_row_sha256"] == c19_by_mid[mid]["row_sha256"], "C25/C19 binding")
            c25[mid] = row
    need(set(c25) == target_ids, "C25 target join")
    c26: dict[str, dict[str, Any]] = {}
    for row in closed_rows(HERE / C26):
        mid = row["owner_member_id"]
        if mid in target_ids:
            need(mid not in c26, "one C26 handle per C19C member")
            need(row["owner_normalized_support_ast_sha256"] == c25[mid]["normalized_support_ast_sha256"], "C26/C25 support binding")
            c26[mid] = row
    need(set(c26) == target_ids, "C26 target join")

    # Unpack the three exact rectangular forests.
    r174 = strict_json(HERE / R174_ROWS)
    parents = table(r174, "parent_rows")
    parent_by_id = {row["parent_id"]: row for row in parents}
    need(len(parent_by_id) == len(parents) == 21_232, "R174 parent uniqueness")
    r174_resolved = table(r174, "resolved_3d_occurrence_rows")
    r174_residual = table(r174, "residual_3d_tube_rows")
    r174_guards = table(r174, "chart_guard_rejection_rows")
    residual_by_id = {row["row_id"]: row for row in r174_residual}
    need(len(residual_by_id) == len(r174_residual) == 62_012, "R174 residual uniqueness")

    forest_r174_stats = {"parent_count": len(parents), "terminal_count": 0, "internal_count": 0}
    leaves_by_parent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in r174_resolved + r174_residual + r174_guards:
        leaves_by_parent[row["parent_id"]].append(row)
    order = list(parents)
    random.Random(seed ^ 0x174).shuffle(order)
    for parent in order:
        chart = parent["chart"]
        parent_x = qbox(parent["box"])
        parent_u = to_oriented(chart, parent_x)
        replayed, _trace = gate3_leaf_replay(chart, parent["leaf_id"])
        need(replayed == parent_u, "Gate3 parent path replay")
        rows = leaves_by_parent[parent["parent_id"]]
        need(len(rows) == parent["resolved_child_count"] + parent["residual_tube_count"] + parent["guard_rejection_count"], "R174 parent census")
        paths: list[tuple[str, ...]] = []
        for row in rows:
            path = tuple(row["refinement_path"])
            paths.append(path)
            need(replay_tokens(parent_u, path) == to_oriented(chart, qbox(row["box"])), "R174 exact oriented replay")
        stats = complete_binary_trie(paths, "R174:" + parent["parent_id"])
        forest_r174_stats["terminal_count"] += stats["terminal_count"]
        forest_r174_stats["internal_count"] += stats["internal_count"]

    r179 = strict_json(HERE / R179_ROWS)
    r179_origins = table(r179, "origin_tube_rows")
    r179_resolved = table(r179, "resolved_3d_child_rows")
    r179_retained = table(r179, "retained_3d_child_rows")
    r179_guards = table(r179, "chart_guard_child_rows")
    retained_by_id = {row["row_id"]: row for row in r179_retained}
    children_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in r179_resolved + r179_retained + r179_guards:
        children_by_origin[row["origin_row_id"]].append(row)
    need(len(r179_origins) == len(residual_by_id) == 62_012, "R179 origin census")
    order179 = list(r179_origins)
    random.Random(seed ^ 0x179).shuffle(order179)
    for summary in order179:
        oid = summary["origin_row_id"]
        need(oid in residual_by_id, "R179 origin join")
        origin = residual_by_id[oid]
        children = children_by_origin[oid]
        need(len(children) == 2 and {row["child_index"] for row in children} == {0, 1}, "R179 exact siblings")
        axis = AXES.index(summary["chosen_split_axis"])
        origin_x = qbox(origin["box"])
        for child in children:
            need(child["refinement_path"][:-1] == origin["refinement_path"], "R179 path prefix")
            tok_axis, tok_child = parse_token(child["refinement_path"][-1])
            need(tok_axis == axis and tok_child == child["child_index"], "R179 path child")
            need(split(origin_x, axis, child["child_index"]) == qbox(child["box"]), "R179 exact x replay")

    selected_r179 = {row["Round179_retained_child_row_id"] for row in r234_doc["root_summary_rows"]}
    need(len(selected_r179) == len(r234_doc["root_summary_rows"]) == 2_640, "R234 root uniqueness")
    need(selected_r179 <= set(retained_by_id), "R234/R179 roots")
    r234_leaves_by_root: dict[str, list[tuple[tuple[str, ...], dict[str, Any], str]]] = defaultdict(list)
    for disposition, rows in (
        ("R234_RESOLVED", r234_doc["resolved_descendant_rows"]),
        ("R234_GUARD", r234_doc["guard_descendant_rows"]),
        ("R234_FRONTIER", r234_doc["depth6_frontier_rows"]),
    ):
        for row in rows:
            path = tuple("t" + str(bit) for bit in row["binary_t_path"])
            r234_leaves_by_root[row["Round179_retained_child_row_id"]].append((path, row, disposition))
    forest_r234_stats = {"root_count": len(selected_r179), "terminal_count": 0, "internal_count": 0}
    for root_id in sorted(selected_r179):
        root = retained_by_id[root_id]
        packed = r234_leaves_by_root[root_id]
        stats = complete_binary_trie([item[0] for item in packed], "R234:" + root_id)
        forest_r234_stats["terminal_count"] += stats["terminal_count"]
        forest_r234_stats["internal_count"] += stats["internal_count"]
        for path, row, _disposition in packed:
            need(replay_tokens(qbox(root["box"]), path) == qbox(row["box"]), "R234 exact replay")

    # The downstream terminal forest replacing every R174 residual and every
    # selected R179 retained root.  This is a genuine leaf set, not merely a
    # volume calculation.
    terminal_leaves: list[Leaf] = []
    for disposition, rows, id_key in (
        ("R174_RESOLVED", r174_resolved, "row_id"),
        ("R174_CHART_GUARD", r174_guards, "row_id"),
        ("R179_RESOLVED", r179_resolved, "row_id"),
        ("R179_CHART_GUARD", r179_guards, "row_id"),
    ):
        for row in rows:
            terminal_leaves.append(Leaf(row[id_key], row["chart"], qbox(row["box"]), disposition))
    for row in r179_retained:
        if row["row_id"] not in selected_r179:
            terminal_leaves.append(Leaf(row["row_id"], row["chart"], qbox(row["box"]), "R179_RETAINED_OTHER_KERNEL"))
    for disposition, rows, id_key in (
        ("R234_RESOLVED", r234_doc["resolved_descendant_rows"], "materialized_row_id"),
        ("R234_GUARD", r234_doc["guard_descendant_rows"], "materialized_row_id"),
        ("R234_FRONTIER", r234_doc["depth6_frontier_rows"], "frontier_row_id"),
    ):
        for row in rows:
            terminal_leaves.append(Leaf(row[id_key], row["chart"], qbox(row["box"]), disposition))
    need(len(terminal_leaves) == 245_188, "terminal forest census")
    parent_total = sum((volume(qbox(row["box"])) for row in parents), Q(0))
    terminal_total = sum((volume(row.box) for row in terminal_leaves), Q(0))
    need(parent_total == terminal_total, "hierarchical terminal volume check")

    # Virtual fixed-depth completion of the upstream Gate3 forest.  Cells
    # covered by a unique-first parent are replaced by the terminal forest;
    # every remaining microcell is a precise OTHER_SUPPORT_KERNEL neighbor.
    # This avoids treating an unmaterialized old support kernel as "outer".
    parent_prefixes: dict[tuple[str, int, int], list[str]] = defaultdict(list)
    for parent in parents:
        raw = parent["leaf_id"]
        if raw.startswith("V.") or raw.startswith("H."):
            raw = raw[2:]
        i_text, j_text, bits = raw.split(".")
        parent_prefixes[(parent["chart"], int(i_text), int(j_text))].append(bits)
    complement_leaves: list[Leaf] = []
    unique_microcells = 0
    complement_histogram: dict[str, int] = defaultdict(int)
    for chart in ("G:E", "G:W", "G:N", "G:S"):
        for i in range(8):
            for j in range(16):
                prefixes = parent_prefixes[(chart, i, j)]
                for value in range(1 << 8):
                    bits = format(value, "08b")
                    if any(bits.startswith(prefix) for prefix in prefixes):
                        unique_microcells += 1
                        continue
                    ubox = (
                        T0 + (T1 - T0) * Q(i, 8), T0 + (T1 - T0) * Q(i + 1, 8),
                        P0 + (P1 - P0) * Q(j, 16), P0 + (P1 - P0) * Q(j + 1, 16),
                        S0, S1,
                    )
                    for bit in bits:
                        _axis, ubox = split_widest(ubox, int(bit))
                    leaf_id = f"v3-gate3-other-kernel-microcell:{chart}:{i:02d}:{j:02d}:{bits}"
                    complement_leaves.append(Leaf(
                        leaf_id, chart, from_oriented(chart, ubox),
                        "GATE3_OTHER_SUPPORT_KERNEL_VIRTUAL_DEPTH8_COMPLEMENT",
                    ))
                    complement_histogram[chart] += 1
    need(unique_microcells + len(complement_leaves) == 4 * 8 * 16 * 256, "Gate3 virtual completion census")

    # Build a second, explicit BSP representation of the complete hierarchy.
    # It is used below to enumerate real 1D/0D junction atoms, rather than
    # inferring their ownership from the face-relative-interior area ledger.
    all_leaf_by_id = {leaf.leaf_id: leaf for leaf in terminal_leaves + complement_leaves}
    need(len(all_leaf_by_id) == len(terminal_leaves) + len(complement_leaves), "global leaf id uniqueness")
    r174_kind: dict[str, str] = {}
    for row in r174_resolved:
        r174_kind[row["row_id"]] = "terminal"
    for row in r174_guards:
        r174_kind[row["row_id"]] = "terminal"
    for row in r174_residual:
        r174_kind[row["row_id"]] = "residual"
    r179_kind: dict[str, str] = {}
    for row in r179_resolved + r179_guards:
        r179_kind[row["row_id"]] = "terminal"
    for row in r179_retained:
        r179_kind[row["row_id"]] = "selected" if row["row_id"] in selected_r179 else "terminal"

    def split_node(box_u: tuple[Q, ...], axis: int, lower: BSPNode, upper: BSPNode) -> BSPNode:
        middle = (box_u[2 * axis] + box_u[2 * axis + 1]) / 2
        return BSPNode(box_u=box_u, axis=axis, split_u=middle, lower=lower, upper=upper)

    def terminal_node(identifier: str, box_u: tuple[Q, ...]) -> BSPNode:
        need(identifier in all_leaf_by_id, "BSP terminal id")
        leaf = all_leaf_by_id[identifier]
        need(to_oriented(leaf.chart, leaf.box) == box_u, "BSP terminal box")
        return BSPNode(box_u=box_u, leaf=leaf)

    def path_tree(
        box_u: tuple[Q, ...],
        path_rows: dict[tuple[str, ...], Any],
        attach: Any,
        prefix: tuple[str, ...] = (),
    ) -> BSPNode:
        if prefix in path_rows:
            need(not any(len(path) > len(prefix) and path[:len(prefix)] == prefix for path in path_rows), "BSP terminal prefix")
            return attach(path_rows[prefix], box_u)
        next_tokens = {path[len(prefix)] for path in path_rows if len(path) > len(prefix) and path[:len(prefix)] == prefix}
        need(bool(next_tokens), "BSP path hole")
        axes = {parse_token(item)[0] for item in next_tokens}
        need(len(axes) == 1, "BSP path axes")
        axis = next(iter(axes))
        need(next_tokens == {AXES[axis] + "0", AXES[axis] + "1"}, "BSP path siblings")
        lower_box, upper_box = split(box_u, axis, 0), split(box_u, axis, 1)
        lower = path_tree(lower_box, path_rows, attach, prefix + (AXES[axis] + "0",))
        upper = path_tree(upper_box, path_rows, attach, prefix + (AXES[axis] + "1",))
        return split_node(box_u, axis, lower, upper)

    def build_r234_tree(row: dict[str, Any], box_u: tuple[Q, ...]) -> BSPNode:
        root_id = row["row_id"]
        packed = r234_leaves_by_root[root_id]
        mapping = {path: (leaf_row, disposition) for path, leaf_row, disposition in packed}

        def attach_r234(item: tuple[dict[str, Any], str], leaf_box_u: tuple[Q, ...]) -> BSPNode:
            leaf_row, disposition = item
            identifier = leaf_row["frontier_row_id"] if disposition == "R234_FRONTIER" else leaf_row["materialized_row_id"]
            return terminal_node(identifier, leaf_box_u)

        return path_tree(box_u, mapping, attach_r234)

    def build_r179_tree(origin: dict[str, Any], box_u: tuple[Q, ...]) -> BSPNode:
        children = children_by_origin[origin["row_id"]]
        need(len(children) == 2, "BSP R179 children")
        axis = parse_token(children[0]["refinement_path"][-1])[0]
        arranged: list[tuple[tuple[Q, ...], dict[str, Any]]] = []
        for child in children:
            child_u = to_oriented(child["chart"], qbox(child["box"]))
            arranged.append((child_u, child))
        arranged.sort(key=lambda item: item[0][2 * axis])
        need(arranged[0][0] == split(box_u, axis, 0) and arranged[1][0] == split(box_u, axis, 1), "BSP R179 oriented children")

        def attach_child(item: tuple[tuple[Q, ...], dict[str, Any]]) -> BSPNode:
            child_u, child = item
            kind = r179_kind[child["row_id"]]
            if kind == "selected":
                return build_r234_tree(child, child_u)
            return terminal_node(child["row_id"], child_u)

        return split_node(box_u, axis, attach_child(arranged[0]), attach_child(arranged[1]))

    def build_r174_tree(parent: dict[str, Any], box_u: tuple[Q, ...]) -> BSPNode:
        mapping = {tuple(row["refinement_path"]): row for row in leaves_by_parent[parent["parent_id"]]}

        def attach_r174(row: dict[str, Any], leaf_box_u: tuple[Q, ...]) -> BSPNode:
            if r174_kind[row["row_id"]] == "residual":
                return build_r179_tree(row, leaf_box_u)
            return terminal_node(row["row_id"], leaf_box_u)

        return path_tree(box_u, mapping, attach_r174)

    parent_at_prefix: dict[tuple[str, int, int, str], dict[str, Any]] = {}
    for parent in parents:
        raw = parent["leaf_id"]
        if raw.startswith("V.") or raw.startswith("H."):
            raw = raw[2:]
        i_text, j_text, bits = raw.split(".")
        key = (parent["chart"], int(i_text), int(j_text), bits)
        need(key not in parent_at_prefix, "Gate3 parent prefix uniqueness")
        parent_at_prefix[key] = parent

    def gate3_tree(chart: str, i: int, j: int, box_u: tuple[Q, ...], prefix: str = "") -> BSPNode:
        parent = parent_at_prefix.get((chart, i, j, prefix))
        if parent is not None:
            return build_r174_tree(parent, box_u)
        if len(prefix) == 8:
            identifier = f"v3-gate3-other-kernel-microcell:{chart}:{i:02d}:{j:02d}:{prefix}"
            return terminal_node(identifier, box_u)
        widths = tuple(box_u[2 * axis + 1] - box_u[2 * axis] for axis in range(3))
        axis = max(range(3), key=lambda value: widths[value])
        return split_node(
            box_u, axis,
            gate3_tree(chart, i, j, split(box_u, axis, 0), prefix + "0"),
            gate3_tree(chart, i, j, split(box_u, axis, 1), prefix + "1"),
        )

    def initial_grid_tree(
        chart: str,
        box_u: tuple[Q, ...],
        i0: int,
        i1: int,
        j0: int,
        j1: int,
    ) -> BSPNode:
        if i1 - i0 > 1:
            im = (i0 + i1) // 2
            cut = T0 + (T1 - T0) * Q(im, 8)
            lower_box = tuple([*box_u[:1], cut, *box_u[2:]])
            upper_box = tuple([cut, *box_u[1:]])
            return BSPNode(
                box_u=box_u, axis=0, split_u=cut,
                lower=initial_grid_tree(chart, lower_box, i0, im, j0, j1),
                upper=initial_grid_tree(chart, upper_box, im, i1, j0, j1),
            )
        if j1 - j0 > 1:
            jm = (j0 + j1) // 2
            cut = P0 + (P1 - P0) * Q(jm, 16)
            lower_values = list(box_u)
            upper_values = list(box_u)
            lower_values[3] = cut
            upper_values[2] = cut
            return BSPNode(
                box_u=box_u, axis=1, split_u=cut,
                lower=initial_grid_tree(chart, tuple(lower_values), i0, i1, j0, jm),
                upper=initial_grid_tree(chart, tuple(upper_values), i0, i1, jm, j1),
            )
        return gate3_tree(chart, i0, j0, box_u)

    chart_bsp = {
        chart: initial_grid_tree(chart, GLOBAL, 0, 8, 0, 16)
        for chart in ("G:E", "G:W", "G:N", "G:S")
    }

    # Precompute final target boxes and the neighbor face keys actually needed.
    target_order = list(c19_rows)
    random.Random(seed ^ 0xC19C).shuffle(target_order)
    needed_keys: set[tuple[str, int, Q, int]] = set()
    target_meta: dict[str, dict[str, Any]] = {}
    outer_touch = defaultdict(int)
    for source in target_order:
        mid = source["member_id"]
        front = fronts[mid]
        chart = front["chart"]
        box = qbox(front["box"])
        need(2 * max(abs(box[0]), abs(box[1])) ** 2 < 1, "C19C strictly inside chart seam")
        face_meta: list[dict[str, Any]] = []
        signs = orientation(chart)
        for axis in range(3):
            for side in (0, 1):
                face_index = 2 * axis + side
                coord = box[face_index]
                is_outer = axis in {1, 2} and coord == GLOBAL[face_index]
                need(not (axis == 0 and coord in {T0, T1}), "C19C must not touch conservative t outer")
                if is_outer:
                    outer_touch[FACES[face_index]] += 1
                    closed = True
                    owner_side = "SELF_BY_CLOSED_PHYSICAL_OUTER_OVERRIDE"
                else:
                    # In u coordinates the positive side owns.  x lower maps
                    # to u lower for sign+ and to u upper for sign-.
                    u_side = side if signs[axis] == 1 else 1 - side
                    closed = u_side == 0
                    owner_side = "SELF" if closed else "ADJACENT_COMPLEMENT"
                    needed_keys.add((chart, axis, coord, 1 - side))
                face_meta.append({
                    "face": FACES[face_index],
                    "axis": AXES[axis],
                    "x_side": "lower" if side == 0 else "upper",
                    "coordinate": qstr(coord),
                    "physical_outer": is_outer,
                    "closed": closed,
                    "owner_side": owner_side,
                })
        target_meta[mid] = {"chart": chart, "box": box, "face_meta": face_meta}
    need(dict(outer_touch) == {
        "s_lower": 18_048,
        "s_upper": 18_048,
    }, "C19C outer-boundary census")

    # Index only the terminal faces that can neighbor a C19C face.
    neighbor_index: dict[tuple[str, int, Q, int], list[Leaf]] = defaultdict(list)
    for leaf in terminal_leaves + complement_leaves:
        for axis in range(3):
            for side in (0, 1):
                key = (leaf.chart, axis, leaf.box[2 * axis + side], side)
                if key in needed_keys:
                    neighbor_index[key].append(leaf)
    neighbor_trees: dict[tuple[str, int, Q, int], tuple[int, IntervalNode | None]] = {}
    for key, candidates in neighbor_index.items():
        normal_axis = key[1]
        first_tangential = next(axis for axis in range(3) if axis != normal_axis)
        neighbor_trees[key] = (
            first_tangential,
            make_interval_tree(candidates, first_tangential),
        )

    authority_rows: list[dict[str, Any]] = []
    atom_rows: list[dict[str, Any]] = []
    junction1_rows: list[dict[str, Any]] = []
    junction0_rows: list[dict[str, Any]] = []
    c19_replay_rows: list[dict[str, Any]] = []
    c25_replay_rows: list[dict[str, Any]] = []
    c26_replay_rows: list[dict[str, Any]] = []
    tjunction_faces = 0
    max_atoms = 0
    other_kernel_atoms = 0

    # Canonical output is original C19C ordinal order; the randomized order
    # above was consumed by the independent forest/face-key traversal.
    for source in c19_rows:
        mid = source["member_id"]
        ordinal = source["ordinal"]
        front = fronts[mid]
        chart = target_meta[mid]["chart"]
        box = target_meta[mid]["box"]
        per_face: list[dict[str, Any]] = []
        bits: dict[str, bool] = {}
        line_specs: set[tuple[int, Q, Q, int, Q, int, Q]] = set()
        point_specs: set[tuple[Q, Q, Q]] = set()
        self_terminal_id = front["frontier_row_id"]
        for face_index, face in enumerate(target_meta[mid]["face_meta"]):
            axis, side = divmod(face_index, 2)
            bits[BIT_NAMES[face_index]] = face["closed"]
            tangential = [value for value in range(3) if value != axis]
            face_rect = (
                box[2 * tangential[0]], box[2 * tangential[0] + 1],
                box[2 * tangential[1]], box[2 * tangential[1] + 1],
            )
            local_atoms: list[dict[str, Any]] = []
            if face["physical_outer"]:
                atom_body = {
                    "schema": "cm2.c19c-endpoint-ownership-v3.face-atom.v1",
                    "member_ordinal": ordinal,
                    "member_id": mid,
                    "face": face["face"],
                    "face_atom_ordinal": 0,
                    "chart": chart,
                    "normal_axis": AXES[axis],
                    "face_coordinate": face["coordinate"],
                    "tangential_axes": [AXES[value] for value in tangential],
                    "tangential_bounds": sbox(face_rect),
                    "exact_relative_interior_area": qstr(area(face_rect)),
                    "neighbor_terminal_id": None,
                    "neighbor_disposition": "PHYSICAL_OUTER_COMPLEMENT_EMPTY",
                    "owner_terminal_id": self_terminal_id,
                    "owner_member_id_if_C19C": mid,
                    "owner_disposition": "SELF_BY_CLOSED_PHYSICAL_OUTER_OVERRIDE",
                    "codimension_2_and_3_boundary_rule": "TRANSPORTED_ORIENTED_PRODUCT_HALF_OPEN_RULE",
                    "formal_credit": 0,
                }
                local_atoms.append({**atom_body, "row_sha256": objsha(atom_body)})
            else:
                key = (chart, axis, box[2 * axis + side], 1 - side)
                need(key in neighbor_trees, "neighbor search key")
                first_tangential, tree = neighbor_trees[key]
                first_position = tangential.index(first_tangential)
                candidates: list[Leaf] = []
                interval_query(
                    tree, first_tangential,
                    face_rect[2 * first_position],
                    face_rect[2 * first_position + 1],
                    candidates,
                )
                overlaps: list[tuple[tuple[Q, Q, Q, Q], Leaf]] = []
                for neighbor in candidates:
                    rect = (
                        max(face_rect[0], neighbor.box[2 * tangential[0]]),
                        min(face_rect[1], neighbor.box[2 * tangential[0] + 1]),
                        max(face_rect[2], neighbor.box[2 * tangential[1]]),
                        min(face_rect[3], neighbor.box[2 * tangential[1] + 1]),
                    )
                    if rect[0] < rect[1] and rect[2] < rect[3]:
                        overlaps.append((rect, neighbor))
                need(bool(overlaps), "face has an adjacent terminal/complement")
                breaks0 = sorted({face_rect[0], face_rect[1]} | {value for rect, _leaf in overlaps for value in rect[:2]})
                breaks1 = sorted({face_rect[2], face_rect[3]} | {value for rect, _leaf in overlaps for value in rect[2:]})
                atom_ordinal = 0
                for i in range(len(breaks0) - 1):
                    for j in range(len(breaks1) - 1):
                        cell = (breaks0[i], breaks0[i + 1], breaks1[j], breaks1[j + 1])
                        if cell[0] >= cell[1] or cell[2] >= cell[3]:
                            continue
                        owners = [leaf for rect, leaf in overlaps if rect[0] <= cell[0] and cell[1] <= rect[1] and rect[2] <= cell[2] and cell[3] <= rect[3]]
                        need(len(owners) == 1, "face common refinement has gap/overlap")
                        neighbor = owners[0]
                        owner_id = self_terminal_id if face["closed"] else neighbor.leaf_id
                        owner_disposition = "SELF_BY_ORIENTED_INTERNAL_RULE" if face["closed"] else "NEIGHBOR_BY_ORIENTED_INTERNAL_RULE"
                        atom_body = {
                            "schema": "cm2.c19c-endpoint-ownership-v3.face-atom.v1",
                            "member_ordinal": ordinal,
                            "member_id": mid,
                            "face": face["face"],
                            "face_atom_ordinal": atom_ordinal,
                            "chart": chart,
                            "normal_axis": AXES[axis],
                            "face_coordinate": face["coordinate"],
                            "tangential_axes": [AXES[value] for value in tangential],
                            "tangential_bounds": sbox(cell),
                            "exact_relative_interior_area": qstr(area(cell)),
                            "neighbor_terminal_id": neighbor.leaf_id,
                            "neighbor_disposition": neighbor.disposition,
                            "neighbor_box": sbox(neighbor.box),
                            "owner_terminal_id": owner_id,
                            "owner_member_id_if_C19C": mid if face["closed"] else None,
                            "owner_disposition": owner_disposition,
                            "codimension_2_and_3_boundary_rule": "TRANSPORTED_ORIENTED_PRODUCT_HALF_OPEN_RULE",
                            "formal_credit": 0,
                        }
                        local_atoms.append({**atom_body, "row_sha256": objsha(atom_body)})
                        atom_ordinal += 1
                        if neighbor.disposition == "GATE3_OTHER_SUPPORT_KERNEL_VIRTUAL_DEPTH8_COMPLEMENT":
                            other_kernel_atoms += 1
                need(sum((Q(row["exact_relative_interior_area"]) for row in local_atoms), Q(0)) == area(face_rect), "face exact area coverage")
            max_atoms = max(max_atoms, len(local_atoms))
            if len(local_atoms) > 1:
                tjunction_faces += 1
            atom_rows.extend(local_atoms)
            atom_rectangles = [tuple(map(Q, row["tangential_bounds"])) for row in local_atoms]
            breaks0 = sorted({face_rect[0], face_rect[1]} | {value for rect in atom_rectangles for value in rect[:2]})
            breaks1 = sorted({face_rect[2], face_rect[3]} | {value for rect in atom_rectangles for value in rect[2:]})
            normal_coordinate = box[2 * axis + side]
            for fixed0 in breaks0:
                for index in range(len(breaks1) - 1):
                    fixed = sorted(((axis, normal_coordinate), (tangential[0], fixed0)))
                    line_specs.add((
                        tangential[1], breaks1[index], breaks1[index + 1],
                        fixed[0][0], fixed[0][1], fixed[1][0], fixed[1][1],
                    ))
            for fixed1 in breaks1:
                for index in range(len(breaks0) - 1):
                    fixed = sorted(((axis, normal_coordinate), (tangential[1], fixed1)))
                    line_specs.add((
                        tangential[0], breaks0[index], breaks0[index + 1],
                        fixed[0][0], fixed[0][1], fixed[1][0], fixed[1][1],
                    ))
            for fixed0 in breaks0:
                for fixed1 in breaks1:
                    point = [Q(0), Q(0), Q(0)]
                    point[axis] = normal_coordinate
                    point[tangential[0]] = fixed0
                    point[tangential[1]] = fixed1
                    point_specs.add(tuple(point))
            per_face.append({
                **face,
                "face_atom_count": len(local_atoms),
                "face_atom_row_sequence_sha256": objsha([row["row_sha256"] for row in local_atoms]),
                "exact_face_area": qstr(area(face_rect)),
                "relative_interior_gluing": "EXACT_NO_GAP_NO_OVERLAP",
                "tangential_T_junction_rule": "COMMON_REFINEMENT_ATOMS_PLUS_ORIENTED_PRODUCT_BOUNDARY_OWNER",
            })

        # Explicit 1D junction audit.  Every boundary line of every face-atom
        # grid is queried against the complete BSP.  The incident leaves can
        # add further breakpoints, which are materialized before ownership is
        # tested.  This includes C19C edges and interior T-junction lines.
        local_junction1: list[dict[str, Any]] = []
        local_line_ordinal = 0
        chart_signs = orientation(chart)
        line_intervals: dict[tuple[int, int, Q, int, Q], list[tuple[Q, Q]]] = defaultdict(list)
        for var_axis, var_lo_x, var_hi_x, fixed_axis0, fixed_x0, fixed_axis1, fixed_x1 in line_specs:
            line_intervals[(var_axis, fixed_axis0, fixed_x0, fixed_axis1, fixed_x1)].append((var_lo_x, var_hi_x))
        normalized_line_specs: list[tuple[int, Q, Q, int, Q, int, Q]] = []
        for key, intervals in line_intervals.items():
            merged: list[tuple[Q, Q]] = []
            for lo, hi in sorted(intervals):
                if not merged or merged[-1][1] < lo:
                    merged.append((lo, hi))
                else:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
            var_axis, fixed_axis0, fixed_x0, fixed_axis1, fixed_x1 = key
            normalized_line_specs.extend(
                (var_axis, lo, hi, fixed_axis0, fixed_x0, fixed_axis1, fixed_x1)
                for lo, hi in merged
            )
        for spec in sorted(normalized_line_specs):
            var_axis, var_lo_x, var_hi_x, fixed_axis0, fixed_x0, fixed_axis1, fixed_x1 = spec
            fixed_x = {fixed_axis0: fixed_x0, fixed_axis1: fixed_x1}
            fixed_u = {axis: chart_signs[axis] * value for axis, value in fixed_x.items()}
            u_endpoints = sorted((chart_signs[var_axis] * var_lo_x, chart_signs[var_axis] * var_hi_x))
            incident: list[Leaf] = []
            collect_line_leaves(chart_bsp[chart], fixed_u, var_axis, u_endpoints[0], u_endpoints[1], incident)
            need(bool(incident), "junction line incident leaves")
            cuts = {u_endpoints[0], u_endpoints[1]}
            for leaf in incident:
                leaf_u = to_oriented(chart, leaf.box)
                cuts.add(max(u_endpoints[0], leaf_u[2 * var_axis]))
                cuts.add(min(u_endpoints[1], leaf_u[2 * var_axis + 1]))
            ordered_cuts = sorted(value for value in cuts if u_endpoints[0] <= value <= u_endpoints[1])
            for index in range(len(ordered_cuts) - 1):
                lo_u, hi_u = ordered_cuts[index], ordered_cuts[index + 1]
                if lo_u >= hi_u:
                    continue
                covering: list[Leaf] = []
                owning: list[Leaf] = []
                for leaf in incident:
                    leaf_u = to_oriented(chart, leaf.box)
                    if not (leaf_u[2 * var_axis] <= lo_u and hi_u <= leaf_u[2 * var_axis + 1]):
                        continue
                    covering.append(leaf)
                    if all(endpoint_included_u(leaf_u, axis, coordinate) for axis, coordinate in fixed_u.items()):
                        owning.append(leaf)
                need(bool(covering), "junction line coverage")
                need(len(owning) == 1, "junction line exactly one owner")
                owner = owning[0]
                x_segment = sorted((chart_signs[var_axis] * lo_u, chart_signs[var_axis] * hi_u))
                body = {
                    "schema": "cm2.c19c-endpoint-ownership-v3.junction-1d-row.v1",
                    "member_ordinal": ordinal,
                    "member_id": mid,
                    "junction_1d_ordinal": local_line_ordinal,
                    "chart": chart,
                    "variable_axis": AXES[var_axis],
                    "variable_bounds": sbox(x_segment),
                    "fixed_coordinates": {AXES[axis]: qstr(value) for axis, value in sorted(fixed_x.items())},
                    "exact_open_segment_length": qstr(hi_u - lo_u),
                    "incident_terminal_ids": sorted(leaf.leaf_id for leaf in covering),
                    "incident_terminal_count": len(covering),
                    "owner_terminal_id": owner.leaf_id,
                    "owner_disposition": owner.disposition,
                    "owner_member_id_if_C19C": mid if owner.leaf_id == self_terminal_id else None,
                    "exactly_one_owner": True,
                    "formal_credit": 0,
                }
                local_junction1.append({**body, "row_sha256": objsha(body)})
                local_line_ordinal += 1
                for endpoint_u in (lo_u, hi_u):
                    point = [Q(0), Q(0), Q(0)]
                    point[var_axis] = chart_signs[var_axis] * endpoint_u
                    for axis, value in fixed_x.items():
                        point[axis] = value
                    point_specs.add(tuple(point))

        # Every face-grid vertex and every added 1D breakpoint is checked as
        # an actual 0D junction against all incident leaves.
        local_junction0: list[dict[str, Any]] = []
        for point_ordinal, point_x in enumerate(sorted(point_specs)):
            point_u = tuple(chart_signs[axis] * point_x[axis] for axis in range(3))
            incident: list[Leaf] = []
            collect_point_leaves(chart_bsp[chart], point_u, incident)
            need(bool(incident), "junction point incident leaves")
            owning = [
                leaf for leaf in incident
                if all(endpoint_included_u(to_oriented(chart, leaf.box), axis, point_u[axis]) for axis in range(3))
            ]
            need(len(owning) == 1, "junction point exactly one owner")
            owner = owning[0]
            body = {
                "schema": "cm2.c19c-endpoint-ownership-v3.junction-0d-row.v1",
                "member_ordinal": ordinal,
                "member_id": mid,
                "junction_0d_ordinal": point_ordinal,
                "chart": chart,
                "point": {AXES[axis]: qstr(point_x[axis]) for axis in range(3)},
                "incident_terminal_ids": sorted(leaf.leaf_id for leaf in incident),
                "incident_terminal_count": len(incident),
                "owner_terminal_id": owner.leaf_id,
                "owner_disposition": owner.disposition,
                "owner_member_id_if_C19C": mid if owner.leaf_id == self_terminal_id else None,
                "exactly_one_owner": True,
                "formal_credit": 0,
            }
            local_junction0.append({**body, "row_sha256": objsha(body)})
        junction1_rows.extend(local_junction1)
        junction0_rows.extend(local_junction0)

        authority_body = {
            "schema": "cm2.c19c-endpoint-ownership-v3.authority-row.v1",
            "ordinal": ordinal,
            "member_id": mid,
            "chart": chart,
            "C19C_row_sha256": source["row_sha256"],
            "C5_row_sha256": c5[mid]["row_sha256"],
            "R234_frontier_row_id": front["frontier_row_id"],
            "R234_frontier_row_sha256": objsha(front),
            "bounds": sbox(box),
            "endpoint_inclusion_bits": bits,
            "face_dispositions": per_face,
            "junction_1d_count": len(local_junction1),
            "junction_1d_row_sequence_sha256": objsha([row["row_sha256"] for row in local_junction1]),
            "junction_0d_count": len(local_junction0),
            "junction_0d_row_sequence_sha256": objsha([row["row_sha256"] for row in local_junction0]),
            "authority_rule": "DIRECT_EN_ORIENTED_LOWER_CLOSED_UPPER_OPEN__JX_JY_EXACT_TRANSPORT__CLOSED_PHYSICAL_OUTER_OVERRIDE",
            "source_chart_seam_disposition": "STRICT_INTERIOR_2T2_MINUS_1_NEGATIVE__NO_C19C_FACE_ON_SEAM",
            "all_six_faces_uniquely_disposed": True,
            "formal_credit": 0,
        }
        authority = {**authority_body, "row_sha256": objsha(authority_body)}
        authority_rows.append(authority)

        old_ast = source["support_ast"]
        new_ast = {
            "kind": "HALF_OPEN_RATIONAL_BOX_WITH_V3_ENDPOINT_AUTHORITY",
            "coordinates": ["t", "p", "s"],
            "bounds": old_ast["bounds"],
            "endpoint_inclusion_bits": bits,
            "exact_volume": old_ast["exact_volume"],
            "lineage": old_ast["lineage"],
            "endpoint_authority_row_sha256": authority["row_sha256"],
        }
        c19_body = {
            "schema": "cm2.c19c-endpoint-ownership-v3.c19c-additive-replay-row.v1",
            "ordinal": ordinal,
            "member_id": mid,
            "representation_id": source["representation_id"],
            "original_C19C_row_sha256": source["row_sha256"],
            "endpoint_authority_row_sha256": authority["row_sha256"],
            "support_ast": new_ast,
            "support_ast_sha256": objsha(new_ast),
            "additive_only_old_row_unchanged": True,
            "formal_credit": 0,
        }
        c19_replay = {**c19_body, "row_sha256": objsha(c19_body)}
        c19_replay_rows.append(c19_replay)

        old25 = c25[mid]
        c25_body = {
            "schema": "cm2.c19c-endpoint-ownership-v3.c25-additive-replay-row.v1",
            "ordinal": ordinal,
            "member_id": mid,
            "original_C25_member_row_sha256": old25["row_sha256"],
            "v3_C19C_replay_row_sha256": c19_replay["row_sha256"],
            "v3_normalized_support_ast_sha256": c19_replay["support_ast_sha256"],
            "semantic_kind": old25["support_semantic_kind"],
            "additive_only_old_row_unchanged": True,
            "formal_credit": 0,
        }
        c25_replay = {**c25_body, "row_sha256": objsha(c25_body)}
        c25_replay_rows.append(c25_replay)

        old26 = c26[mid]
        c26_body = {
            "schema": "cm2.c19c-endpoint-ownership-v3.c26-additive-replay-row.v1",
            "ordinal": ordinal,
            "member_id": mid,
            "representation_id": old26["representation_id"],
            "original_C26_handle_row_sha256": old26["row_sha256"],
            "v3_C25_replay_row_sha256": c25_replay["row_sha256"],
            "v3_owner_normalized_support_ast_sha256": c19_replay["support_ast_sha256"],
            "transition_theorem_claimed": False,
            "additive_only_old_row_unchanged": True,
            "formal_credit": 0,
        }
        c26_replay_rows.append({**c26_body, "row_sha256": objsha(c26_body)})

    need(len(authority_rows) == len(c19_replay_rows) == len(c25_replay_rows) == len(c26_replay_rows) == 33_344, "replay census")
    atom_rows.sort(key=lambda row: (row["member_ordinal"], FACES.index(row["face"]), row["face_atom_ordinal"]))
    junction1_rows.sort(key=lambda row: (row["member_ordinal"], row["junction_1d_ordinal"]))
    junction0_rows.sort(key=lambda row: (row["member_ordinal"], row["junction_0d_ordinal"]))
    candidate_dir.mkdir(parents=True, exist_ok=True)
    ledgers = {
        "authority": write_rows(candidate_dir / AUTHORITY_LEDGER, authority_rows),
        "face_atoms": write_rows(candidate_dir / FACE_ATOM_LEDGER, atom_rows),
        "junction_1d": write_rows(candidate_dir / JUNCTION1_LEDGER, junction1_rows),
        "junction_0d": write_rows(candidate_dir / JUNCTION0_LEDGER, junction0_rows),
        "C19C_additive_replay": write_rows(candidate_dir / C19_REPLAY_LEDGER, c19_replay_rows),
        "C25_additive_replay": write_rows(candidate_dir / C25_REPLAY_LEDGER, c25_replay_rows),
        "C26_additive_replay": write_rows(candidate_dir / C26_REPLAY_LEDGER, c26_replay_rows),
    }

    semantic = {
        "schema": "cm2.c19c-endpoint-ownership-v3.result.v1",
        "status": "PASS_APPEND_ONLY_ENDPOINT_OWNER_AUTHORITY__ZERO_FORMAL_CREDIT",
        "execution_seed": seed,
        "execution_order_attestation": {
            "C19C_randomized_order_sha256": objsha([row["member_id"] for row in target_order]),
            "R174_randomized_parent_order_sha256": objsha([row["parent_id"] for row in order]),
            "R179_randomized_origin_order_sha256": objsha([row["origin_row_id"] for row in order179]),
        },
        "input_pins": {name: PINS[name] for name in sorted(PINS)},
        "authority": {
            "direct_charts": ["G:E", "G:N"],
            "direct_rule": "oriented [lower,upper) on internal faces",
            "transported_axis_signs": {
                "G:E": [1, 1, 1], "G:N": [1, 1, 1],
                "G:W": [1, -1, -1], "G:S": [1, -1, 1],
            },
            "Jx": "(t,p,s)->(t,-p,-s)",
            "Jy": "(t,p,s)->(t,-p,s)",
            "closed_physical_outer_rule": "both p endpoints and both s endpoints included",
            "source_chart_seam_rule": "E or W owns; N or S excludes",
            "C19C_rows_strictly_inside_source_chart_seam": 33_344,
            "C19C_s_lower_outer_faces": outer_touch["s_lower"],
            "C19C_s_upper_outer_faces": outer_touch["s_upper"],
            "C19C_p_outer_faces": 0,
            "C19C_conservative_t_outer_faces": 0,
        },
        "forest_proofs": {
            "R174_prefix_free_sibling_complete": forest_r174_stats,
            "R179_origins_with_exactly_two_geometric_children": len(r179_origins),
            "R234_prefix_free_sibling_complete": forest_r234_stats,
            "hierarchical_terminal_leaf_count": len(terminal_leaves),
            "Gate3_virtual_depth8_unique_first_microcells": unique_microcells,
            "Gate3_virtual_depth8_other_support_kernel_microcells": len(complement_leaves),
            "Gate3_other_kernel_chart_histogram": dict(sorted(complement_histogram.items())),
            "face_gluing_is_not_inferred_from_volume": True,
        },
        "face_gluing": {
            "C19C_face_count": 33_344 * 6,
            "face_atom_count": len(atom_rows),
            "T_junction_or_multi_neighbor_face_count": tjunction_faces,
            "maximum_face_atom_count": max_atoms,
            "other_support_kernel_face_atom_count": other_kernel_atoms,
            "every_face_relative_interior_exactly_tiled": True,
            "every_internal_face_atom_has_one_terminal_neighbor": True,
            "every_face_atom_has_exactly_one_owner": True,
            "junction_1d_atom_count": len(junction1_rows),
            "junction_0d_atom_count": len(junction0_rows),
            "every_actual_1d_junction_atom_enumerated_and_has_one_owner": True,
            "every_actual_0d_junction_atom_enumerated_and_has_one_owner": True,
            "T_junction_breakpoints_included_in_0d_ledger": True,
        },
        "ledgers": ledgers,
        "additive_replay": {
            "C19C_rows": 33_344,
            "C25_rows": 33_344,
            "C26_rows": 33_344,
            "old_files_modified": False,
        },
        "strict_nonpromotion": {
            "formal_credit": 0,
            "twenty_family_gate": "OPEN_PENDING_INDEPENDENT_TOTALITY_INTEGRATION",
            "C27": "REBUILD_REQUIRED_AND_NOT_AUTHORIZED",
            "C28": "REJECT",
            "C29": "REJECT",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result = {**semantic, "result_sha256": objsha(semantic)}
    (candidate_dir / RESULT).write_bytes(canonical(result))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    result = build(Path(args.candidate_dir).resolve(), args.seed)
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
