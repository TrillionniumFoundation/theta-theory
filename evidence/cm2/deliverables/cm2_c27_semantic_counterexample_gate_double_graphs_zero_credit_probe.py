#!/usr/bin/env python3
"""Independent zero-credit semantic counterexample gate for DOUBLE_GRAPHS.

This development probe deliberately does not import Round306C27, copy its
``FAMILIES`` table, or consume any C6/C14D/C15 edge ledger.  It reconstructs
the corrected double-endpoint graph population from the pinned C15 member
universe, binds exact supports through C25/C26, and re-evaluates the primitive
graph/sheet/side geometry in C10/C24A/C24B and R234/R236/R248.

The probe is counterexample-first.  A geometrically legal candidate whose
endpoints lie in different C15 components is preserved as a minimal witness
and makes the result fail closed.  A clean result is diagnostic only: all
formal credits are exactly zero and no existing C27/C28/C29 authority is
modified or upgraded.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Iterator, TextIO


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_c27_semantic_counterexample_gate_double_graphs_zero_credit_v2"
LEDGER = PREFIX + "_candidate_partition_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
MANIFEST = PREFIX + "_manifest.json"
AUDIT_ROOT = ROOT.parent / ".cm2-runtime" / "audit"
SUPERSEDED_OUTPUT = (
    AUDIT_ROOT / "c27-semantic-double-graphs-zero-credit-seed-30627001"
)

C10_LEDGER = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
C15_MEMBER = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C24A_LEDGER = "cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz"
C24B_LEDGER = "cm2_round306c24b_source_g_168_negative_nonincidence_empty_support_and_representation_kernel_ledger.jsonl.gz"
C25_MEMBER = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26_FEATURE = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"
R234_CERT = "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"
R236_CERT = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R248_CERT = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R182_ROWS = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R272_CERT = "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json"
R291_LEDGER = "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_ledger.json.gz"
R295A_LEDGER = "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_physical_witness_incidence_binding_ledger.json.gz"
C22B_LEDGER = "cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel_ledger.jsonl.gz"

INPUT_PINS = {
    "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_manifest.sha256": "b7277863feb9edc5f35906b04af2a9a256becb7ee9f1f1df6558b897184029ca",
    C10_LEDGER: "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c",
    "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_manifest.sha256": "a1eea2c41123d2ff7f7d3e1f35f1deabc5bae9d93b24f825b4831f6324c1e2c4",
    C15_MEMBER: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_result.json": "851d047d92b8ded8949e6182837ac93fc390aabb9bc7b325aba7ea14889dc333",
    "cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_manifest.sha256": "2e17d522cef9a32a971c28a7d0e6aaeab97e66da367fedf92c2bb6b418aaeacb",
    C24A_LEDGER: "ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58",
    "cm2_round306c24b_source_g_168_negative_nonincidence_empty_support_and_representation_kernel_manifest.sha256": "9a5b8dea2ed9093070c4434bbac7af9169691d02c2c5315974f597b6927b3d13",
    C24B_LEDGER: "788f16cf6c8e67cdd5c1f3bcdb89e6cde00047bda19531a9a42c56339a31e380",
    "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_manifest.sha256": "8885eb09f4e0aef3107654996ef520cca3ce59f59fc5b5d8a1652d44f9bb9a81",
    C25_MEMBER: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_result.json": "6f3d46b460b6a03a1a461bbcf7b44dfc389d63a15fa26a6263a6150fc483d701",
    "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_manifest.sha256": "dd30d22bec3f9ab2f95dcf123bab47b7e8c4f0bc2013732f6d12c4e3e1441b3b",
    C26_FEATURE: "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e",
    "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_result.json": "75aa29cc0c1e73f12b97b4ec4a779dee07e84c64ec03dba08c6e6f147935a9ec",
    "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_manifest.sha256": "f8714ecdf804657fc6633136544f567b07e7d8503095d17fcda19226feefc432",
    R234_CERT: "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac",
    "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_manifest.sha256": "28f6f6d2f5b0f10edba5cd473b4126a8fed098874849c2f579eadd92b30d324c",
    R236_CERT: "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256": "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07",
    R248_CERT: "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_manifest.sha256": "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5",
    R182_ROWS: "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_manifest.sha256": "82124ccbc3fa88fadb1f2a3239634dca332ccc959f7338c44cd27908e4957e5a",
    R272_CERT: "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",
    "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_manifest.sha256": "d655907a45cfb7b47ebdc822d35a0e604fc27fa38547c300139c116d7a2191ce",
    R291_LEDGER: "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_manifest.sha256": "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    R295A_LEDGER: "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    "cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel_manifest.sha256": "cd6ed594efe7cd24ddc5e267c564ad650f48f3289e06da658337743a1469399e",
    C22B_LEDGER: "c0f3d3a9fc6002f0af23271f7483aeff7eac0b0cc92399fc3785b0a5b9291f97",
    "cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel_result.json": "218a64732da853bf426f4882c84633f8421511a3490b2f0b830bed5484d83506",
}

EXPECTED_ROWS = {
    C10_LEDGER: 5_264,
    C15_MEMBER: 502_204,
    C24A_LEDGER: 15_224,
    C24B_LEDGER: 168,
    C25_MEMBER: 502_204,
    C26_FEATURE: 691_424,
    C22B_LEDGER: 302_624,
}


class GateFailure(RuntimeError):
    pass


INPUT_SNAPSHOTS: dict[str, dict[str, Any]] = {}


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise GateFailure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            state.update(block)
    return state.hexdigest()


def guarded_snapshot(path: Path) -> dict[str, Any]:
    need(path.parent == ROOT, "direct-child input:" + path.name)
    parent = ROOT.resolve(strict=True)
    need(path.parent.resolve(strict=True) == parent, "resolved input parent:" + path.name)
    before = os.lstat(path)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        need(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_size > 0
            and (before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino),
            "nofollow regular input:" + path.name,
        )
        state = hashlib.sha256()
        while True:
            block = os.read(descriptor, 8 << 20)
            if not block:
                break
            state.update(block)
        return {
            "device": opened.st_dev,
            "inode": opened.st_ino,
            "mode": stat.S_IMODE(opened.st_mode),
            "nlink": opened.st_nlink,
            "size": opened.st_size,
            "mtime_ns": opened.st_mtime_ns,
            "ctime_ns": opened.st_ctime_ns,
            "sha256": state.hexdigest(),
        }
    finally:
        os.close(descriptor)


def guard_input(name: str, expected: str) -> None:
    path = ROOT / name
    snapshot = guarded_snapshot(path)
    need(snapshot["sha256"] == expected, "byte pin:" + name)
    INPUT_SNAPSHOTS[name] = snapshot


def recheck_input_snapshots() -> None:
    need(set(INPUT_SNAPSHOTS) == set(INPUT_PINS), "complete input snapshot set")
    for name, expected in sorted(INPUT_SNAPSHOTS.items()):
        need(guarded_snapshot(ROOT / name) == expected, "stable input snapshot:" + name)


def check_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), "row closure:" + label)


def closed_wrapper(name: str) -> dict[str, Any]:
    document = json.loads((ROOT / name).read_bytes())
    need(type(document) is dict and type(document.get("result")) is dict, "closed wrapper:" + name)
    need(document.get("result_sha256") == digest(document["result"]), "wrapper closure:" + name)
    return document["result"]


def jsonl_rows(name: str) -> Iterator[dict[str, Any]]:
    count = 0
    with gzip.open(ROOT / name, "rb") as stream:
        for raw in stream:
            need(raw.endswith(b"\n"), "jsonl newline:" + name)
            row = json.loads(raw[:-1])
            count += 1
            yield row
    need(count == EXPECTED_ROWS[name], "jsonl row count:" + name)


def stream_array(
    stream: TextIO,
    *,
    marker: str,
    nested_rows: bool,
    expected_type: type = dict,
) -> Iterator[Any]:
    """Stream one pinned JSON array without retaining its surrounding file."""
    buffer = ""
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing marker:" + marker)
        buffer = (buffer + block)[-(len(marker) + (2 << 20)) :]
    buffer = buffer.split(marker, 1)[1]
    if nested_rows:
        while '"rows":[' not in buffer:
            block = stream.read(1 << 20)
            need(bool(block), "missing nested rows:" + marker)
            buffer += block
        buffer = buffer.split('"rows":[', 1)[1]
    else:
        while not buffer.lstrip().startswith("["):
            block = stream.read(1 << 20)
            need(bool(block), "missing array opener:" + marker)
            buffer += block
        buffer = buffer.lstrip()[1:]
    decoder = json.JSONDecoder(
        parse_float=lambda token: (_ for _ in ()).throw(GateFailure("float:" + token)),
        parse_constant=lambda token: (_ for _ in ()).throw(GateFailure("constant:" + token)),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated array:" + marker)
            buffer = block
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                value, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated row:" + marker)
                buffer += block
        need(type(value) is expected_type, "array row type:" + marker)
        yield value
        buffer = buffer[end:]


def plain_array(
    name: str,
    marker: str,
    nested_rows: bool = False,
    expected_type: type = dict,
) -> Iterator[Any]:
    with (ROOT / name).open("rt", encoding="utf-8") as stream:
        yield from stream_array(
            stream,
            marker=marker,
            nested_rows=nested_rows,
            expected_type=expected_type,
        )


def gzip_array(name: str, marker: str = '"rows":') -> Iterator[dict[str, Any]]:
    with gzip.open(ROOT / name, "rt", encoding="utf-8") as stream:
        yield from stream_array(stream, marker=marker, nested_rows=False)


def interval_map(ast: dict[str, Any]) -> dict[str, tuple[Fraction, Fraction]]:
    need(ast.get("op") == "AND" and type(ast.get("args")) is list, "interval conjunction")
    output: dict[str, tuple[Fraction, Fraction]] = {}
    for item in ast["args"]:
        need(item.get("op") == "CLOSED_INTERVAL", "closed interval")
        coordinate = item.get("coordinate")
        need(coordinate in {"t", "p", "s"} and coordinate not in output, "unique interval coordinate")
        lower, upper = Fraction(item["lower"]), Fraction(item["upper"])
        need(lower < upper, "positive interval")
        output[coordinate] = (lower, upper)
    return output


def exact_sheet_base(ast: dict[str, Any]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    intervals = interval_map(ast)
    need(set(intervals) == {"p", "s"}, "sheet p/s support")
    return (*intervals["p"], *intervals["s"])


def mul_coefficient_t(ast: dict[str, Any]) -> Fraction:
    if ast.get("op") == "COORDINATE":
        need(ast.get("name") == "t", "t coordinate")
        return Fraction(1)
    if ast.get("op") == "RATIONAL_CONSTANT":
        return Fraction(ast["value"])
    need(ast.get("op") == "MUL" and type(ast.get("args")) is list, "linear multiply")
    coefficient = Fraction(1)
    coordinate_count = 0
    for item in ast["args"]:
        if item.get("op") == "COORDINATE":
            need(item.get("name") == "t", "linear coordinate")
            coordinate_count += 1
        else:
            coefficient *= mul_coefficient_t(item)
    need(coordinate_count <= 1, "linear coordinate multiplicity")
    return coefficient


def one_sided_trace_base(ast: dict[str, Any]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    need(ast.get("op") == "AND" and len(ast.get("args", [])) == 2, "side support conjunction")
    domain, predicate = ast["args"]
    intervals = interval_map(domain)
    need(set(intervals) == {"t", "p", "s"}, "side t/p/s support")
    need(predicate.get("op") == "GT", "strict side predicate")
    need(predicate.get("right") == {"op": "RATIONAL_CONSTANT", "value": "0"}, "strict side zero")
    coefficient = mul_coefficient_t(predicate["left"])
    need(coefficient != 0, "nonzero side coefficient")
    lower, upper = intervals["t"]
    need(lower == 0 or upper == 0, "trace face t=0")
    midpoint = (lower + upper) / 2
    need(coefficient * midpoint > 0, "strict side nonempty interior")
    return (*intervals["p"], *intervals["s"])


def graph_base(ast: dict[str, Any]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return exact_sheet_base(ast)


def cardinal_normal_at_source_factor_zero(chart: str) -> tuple[Fraction, Fraction]:
    """Rebuild the primitive source-G normal on the exact t=0 wall face.

    Round272 identifies the source transverse wall factor with (9/25)*t,
    up to the recorded chart sign.  Hence both an endpoint graph sheet and
    the closure trace of its strict one-sided G2B support lie on t=0.  The
    primitive atlas map then has the four distinct cardinal normals below.
    This is a physical phase-space calculation, not a chart-name filter.
    """
    need(chart.startswith("G:"), "double graph is source-G geometry")
    cell = chart.split(":", 1)[1]
    normals = {
        "E": (Fraction(1), Fraction(0)),
        "W": (Fraction(-1), Fraction(0)),
        "N": (Fraction(0), Fraction(1)),
        "S": (Fraction(0), Fraction(-1)),
    }
    need(cell in normals, "primitive four-chart registry")
    return normals[cell]


def cross_chart_t0_phase_nonincidence(
    sheet_chart: str,
    side_chart: str,
) -> dict[str, Any]:
    """Solve equality of the two t=0 source-G phase representations exactly."""
    need(sheet_chart != side_chart, "cross-chart t0 equation")
    sheet_normal = cardinal_normal_at_source_factor_zero(sheet_chart)
    side_normal = cardinal_normal_at_source_factor_zero(side_chart)
    need(sheet_normal != side_normal, "distinct source-G cardinal normals")
    radius = Fraction(9, 25)
    sheet_position = tuple(radius * value for value in sheet_normal)
    side_position = tuple(radius * value for value in side_normal)
    need(sheet_position != side_position, "distinct primitive source-G positions")
    return {
        "sheet_t": "0",
        "side_closure_trace_t": "0",
        "source_G_radius": str(radius),
        "sheet_primitive_normal": [str(value) for value in sheet_normal],
        "side_primitive_normal": [str(value) for value in side_normal],
        "sheet_primitive_position": [str(value) for value in sheet_position],
        "side_primitive_position": [str(value) for value in side_position],
        "normal_equality_solution_set": "EMPTY",
        "position_equality_solution_set": "EMPTY",
        "same_physical_phase_point": False,
        "proof_basis": (
            "R272 source factor=(9/25)*t plus the primitive source-G phase map "
            "q=(9/25)n at t=0"
        ),
    }


def rectangle_relation(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> str:
    need(len(left) == len(right) == 4, "rectangle dimension")
    if left == right:
        return "EXACT_EQUAL"
    overlap_p = min(left[1], right[1]) - max(left[0], right[0])
    overlap_s = min(left[3], right[3]) - max(left[2], right[2])
    if overlap_p > 0 and overlap_s > 0:
        return "STRICT_POSITIVE_AREA_INTERSECTION"
    if overlap_p >= 0 and overlap_s >= 0:
        return "CLOSED_BOUNDARY_CONTACT_ONLY"
    return "DISJOINT"


def rectangle_metrics(
    left: tuple[Fraction, ...],
    right: tuple[Fraction, ...],
) -> tuple[str, Fraction, Fraction]:
    relation = rectangle_relation(left, right)
    overlap_p = min(left[1], right[1]) - max(left[0], right[0])
    overlap_s = min(left[3], right[3]) - max(left[2], right[2])
    return relation, overlap_p, overlap_s


def list_sequence_hash(values: list[Any]) -> str:
    return digest(values)


def load_raw_graphs() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    r236 = closed_wrapper(R236_CERT)
    partitions = r236["double_endpoint_partition_rows"]
    need(len(partitions) == 16 and len({row["double_endpoint_partition_row_id"] for row in partitions}) == 16, "R236 double partition census")
    partition_map = {row["double_endpoint_partition_row_id"]: row for row in partitions}
    frontier_ids = {row["Round234_frontier_row_id"] for row in partitions}
    frontiers: dict[str, dict[str, Any]] = {}
    total_frontiers = 0
    for row in plain_array(R234_CERT, '"depth6_frontier_rows":'):
        total_frontiers += 1
        if row["frontier_row_id"] in frontier_ids:
            need(row["frontier_row_id"] not in frontiers, "R234 frontier uniqueness")
            frontiers[row["frontier_row_id"]] = row
    need(total_frontiers == 38_376 and set(frontiers) == frontier_ids, "R234 complete selected frontier join")
    for partition in partitions:
        frontier = frontiers[partition["Round234_frontier_row_id"]]
        need(partition["Round220_split_interface_id"] == frontier["Round220_split_interface_id"], "R234/R236 interface")
        need(partition["source_factor_strict_t_derivative_sign"] == partition["target_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE", "R236 derivative signs")
        partition["_frontier"] = frontier

    sheets: list[dict[str, Any]] = []
    sheet_kind_census: Counter[str] = Counter()
    for row in plain_array(R248_CERT, '"formal_wall_half_open_sheet_owner_ledger":', nested_rows=True):
        kind = row["source_partition_kind"]
        sheet_kind_census[kind] += 1
        if row["source_partition_row_id"] in partition_map:
            check_row(row, "R248 selected sheet")
            sheets.append(row)
    need(sheet_kind_census == {"ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328, "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32}, "R248 complete sheet census")
    need(len(sheets) == 32, "R248 double sheets")

    bulks: list[dict[str, Any]] = []
    bulk_kind_census: Counter[str] = Counter()
    for row in plain_array(R248_CERT, '"formal_wall_positive_volume_bulk_ledger":', nested_rows=True):
        bulk_kind_census[row["source_partition_kind"]] += 1
        if row["source_partition_row_id"] in partition_map:
            check_row(row, "R248 selected bulk")
            bulks.append(row)
    need(bulk_kind_census["ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH"] == 48, "R248 double bulk complete census")
    need(len(bulks) == 48, "R248 double bulks")

    by_partition_sheet: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    by_partition_bulk: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in sheets:
        pid, endpoint = row["source_partition_row_id"], row["endpoint_factor"]
        need(endpoint in {"source", "target"} and endpoint not in by_partition_sheet[pid], "R248 sheet factor uniqueness")
        by_partition_sheet[pid][endpoint] = row
    for row in bulks:
        pid, branch = row["source_partition_row_id"], row["branch_label"]
        need(branch in {"SAME_SIGN_EVENT_ABSENT", "NEGATIVE_TO_POSITIVE", "POSITIVE_TO_NEGATIVE"} and branch not in by_partition_bulk[pid], "R248 bulk branch uniqueness")
        by_partition_bulk[pid][branch] = row
    for pid, partition in partition_map.items():
        need(set(by_partition_sheet[pid]) == {"source", "target"}, "two R248 sheets per double partition")
        need(set(by_partition_bulk[pid]) == {"SAME_SIGN_EVENT_ABSENT", "NEGATIVE_TO_POSITIVE", "POSITIVE_TO_NEGATIVE"}, "three R248 bulks per double partition")
        for sheet in by_partition_sheet[pid].values():
            need(sheet["Round220_split_interface_id"] == partition["Round220_split_interface_id"], "sheet interface")
            need(sheet["owner_wall_bulk_node_id"] == by_partition_bulk[pid]["SAME_SIGN_EVENT_ABSENT"]["wall_bulk_node_id"], "sheet owner source lineage")
            need(tuple(Fraction(x) for x in sheet["exact_closed_base_rectangle"]) == tuple(Fraction(x) for x in partition["_frontier"]["box"][2:6]), "sheet/R234 exact base")
    return partition_map, sheets, bulks


def load_lower_frontier(
    raw_sheets: list[dict[str, Any]],
    partitions: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], set[str]]:
    """Partition the complete current-sheet x R291 frontier without lineage filters.

    Retained-child identity is evidence, never a candidate-generation filter.
    Same-chart rational geometry is evaluated directly.  Cross-chart pairs and
    cells whose exact support is not present in R291 remain fail-closed rather
    than being declared nonedges by identifier mismatch.
    """
    source_sheets = [row for row in raw_sheets if row["endpoint_factor"] == "source"]
    need(len(source_sheets) == 16, "current source double-sheet census")
    sheet_geometry: list[dict[str, Any]] = []
    for sheet in source_sheets:
        frontier = partitions[sheet["source_partition_row_id"]]["_frontier"]
        sheet_geometry.append({
            "row": sheet,
            "chart": frontier["chart"],
            "retained_child_row_id": frontier["Round179_retained_child_row_id"],
            "base": tuple(Fraction(x) for x in sheet["exact_closed_base_rectangle"]),
        })

    exact_graph_contacts: list[dict[str, Any]] = []
    t0_contacts_by_key: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    physical_keys: set[tuple[str, int]] = set()
    physical_sequence: list[str] = []
    route_census: Counter[str] = Counter()
    kind_census: Counter[str] = Counter()
    disposition_count = 0
    physical_cell_count = 0
    t0_kinds = {
        "SOURCE_EXACT_T0_SHEET_CELL",
        "ROUND179_POSITIVE_T0_RETAINED_OWNER",
        "ROUND179_NEGATIVE_T0_SHADOW_PATCH",
    }

    for disposition in gzip_array(R291_LEDGER):
        check_row(disposition, "R291 disposition")
        disposition_count += 1
        disposition_id = disposition["complete_lower_stratum_local_disposition_row_id"]
        chart = disposition["source_chart"]
        for index, cell in enumerate(disposition["physical_witness_cells"]):
            key = (disposition_id, index)
            need(key not in physical_keys, "unique R291 physical cell key")
            physical_keys.add(key)
            physical_sequence.append(digest([disposition_id, index, cell]))
            physical_cell_count += 1
            kind = cell["witness_kind"]
            kind_census[kind] += 1
            for sheet_item in sheet_geometry:
                sheet = sheet_item["row"]
                if sheet_item["chart"] != chart:
                    route_census["UNRESOLVED_CROSS_CHART_REPRESENTATION_HANDOFF"] += 1
                    continue

                if kind == "ROUND182_GRAPH_SHEET_LEAF":
                    box = cell.get("exact_box")
                    need(type(box) is list and len(box) == 6, "R182 exact graph box")
                    bounds = tuple(Fraction(x) for x in box)
                    if not (bounds[0] == 0 or bounds[1] == 0):
                        route_census["EXACT_NONINCIDENCE_T_COORDINATE_DISJOINT"] += 1
                        continue
                    relation, overlap_p, overlap_s = rectangle_metrics(
                        sheet_item["base"], bounds[2:6]
                    )
                    if relation == "DISJOINT":
                        route_census["EXACT_NONINCIDENCE_BASE_RECTANGLE_DISJOINT"] += 1
                        continue
                    contact = {
                        "sheet_member_id": sheet["wall_sheet_node_id"],
                        "sheet_source_partition_row_id": sheet["source_partition_row_id"],
                        "sheet_owner_official_key_id": sheet["owner_official_key_id"],
                        "sheet_owner_signature_sha256": sheet["owner_signature_sha256"],
                        "sheet_exact_closed_base_rectangle": sheet["exact_closed_base_rectangle"],
                        "sheet_chart": sheet_item["chart"],
                        "sheet_R179_retained_child_row_id": sheet_item["retained_child_row_id"],
                        "R291_disposition_row_id": disposition_id,
                        "R291_disposition_row_sha256": disposition["row_sha256"],
                        "R291_canonical_support_row_id": disposition["canonical_support_row_id"],
                        "R291_predicate_equation": disposition["predicate_equation"],
                        "physical_witness_cell_index": index,
                        "physical_witness_cell": cell,
                        "base_relation": relation,
                        "overlap_p": str(overlap_p),
                        "overlap_s": str(overlap_s),
                        "t0_face": "LOWER" if bounds[0] == 0 else "UPPER",
                    }
                    exact_graph_contacts.append(contact)
                    continue

                if kind == "ROUND208_DIRECT_GRAPH_SIDE_REGION":
                    box = cell.get("exact_leaf_box")
                    need(type(box) is list and len(box) == 6, "R208 exact leaf box")
                    bounds = tuple(Fraction(x) for x in box)
                    if not (bounds[0] <= 0 <= bounds[1]):
                        route_census["EXACT_NONINCIDENCE_T_COORDINATE_DISJOINT"] += 1
                    else:
                        route_census["UNRESOLVED_R208_REGION_TOUCHING_T0"] += 1
                    continue

                if kind in t0_kinds:
                    box = cell.get("exact_ambient_bounds", cell.get("exact_bounds"))
                    need(type(box) is list and len(box) == 6, "exact t0 cell bounds")
                    bounds = tuple(Fraction(x) for x in box)
                    need(bounds[0] == bounds[1] == 0, "exact t0 cell")
                    relation, overlap_p, overlap_s = rectangle_metrics(
                        sheet_item["base"], bounds[2:6]
                    )
                    if relation == "DISJOINT":
                        route_census["EXACT_NONINCIDENCE_BASE_RECTANGLE_DISJOINT"] += 1
                        continue
                    t0_contacts_by_key[key].append({
                        "sheet_member_id": sheet["wall_sheet_node_id"],
                        "sheet_source_partition_row_id": sheet["source_partition_row_id"],
                        "sheet_owner_official_key_id": sheet["owner_official_key_id"],
                        "sheet_owner_signature_sha256": sheet["owner_signature_sha256"],
                        "sheet_exact_closed_base_rectangle": sheet["exact_closed_base_rectangle"],
                        "sheet_chart": sheet_item["chart"],
                        "sheet_R179_retained_child_row_id": sheet_item["retained_child_row_id"],
                        "R291_disposition_row_id": disposition_id,
                        "R291_disposition_row_sha256": disposition["row_sha256"],
                        "R291_canonical_support_kind": disposition["canonical_support_kind"],
                        "R291_canonical_support_row_id": disposition["canonical_support_row_id"],
                        "R291_local_disposition": disposition["local_disposition"],
                        "R291_evidence_basis": disposition["evidence_basis"],
                        "R291_predicate_equation": disposition["predicate_equation"],
                        "physical_witness_cell_index": index,
                        "physical_witness_cell": cell,
                        "base_relation": relation,
                        "overlap_p": str(overlap_p),
                        "overlap_s": str(overlap_s),
                    })
                    continue

                need(kind == "ROUND182_TRANSVERSE_1D_LINE", "known R291 witness kind")
                route_census["UNRESOLVED_TRANSVERSE_1D_SUPPORT_WITHOUT_EXACT_TPS_BOX"] += 1

    need(disposition_count == 55_428 and physical_cell_count == 113_452, "R291 complete physical frontier census")
    need(kind_census == {
        "ROUND182_GRAPH_SHEET_LEAF": 111_524,
        "ROUND208_DIRECT_GRAPH_SIDE_REGION": 608,
        "ROUND179_NEGATIVE_T0_SHADOW_PATCH": 544,
        "ROUND179_POSITIVE_T0_RETAINED_OWNER": 440,
        "SOURCE_EXACT_T0_SHEET_CELL": 224,
        "ROUND182_TRANSVERSE_1D_LINE": 112,
    }, "R291 witness-kind census")
    need(len(exact_graph_contacts) == 96, "R182 closed-box t0 contact census")
    need(sum(map(len, t0_contacts_by_key.values())) == 88, "exact t0 contact census")

    leaf_ids = {row["physical_witness_cell"]["leaf_row_id"] for row in exact_graph_contacts}
    leaf_rows: dict[str, dict[str, Any]] = {}
    leaf_columns = (
        "row_id", "occurrence_row_id", "retained_child_row_id",
        "base_refinement_path", "box", "coordinate_volume",
        "base_coordinate_area", "lower_t_face_status", "upper_t_face_status",
        "graph_classification", "two_dimensional_graph_sheet_count",
        "one_dimensional_clipping_curve_segment_count",
        "zero_dimensional_boundary_endpoint_incidence_count",
        "closed_3d_side_union_volume", "residual_3d_collar_volume",
    )
    total_leaf_rows = 0
    for packed in plain_array(
        R182_ROWS,
        '"collar_leaf_rows":',
        expected_type=list,
    ):
        total_leaf_rows += 1
        need(len(packed) == len(leaf_columns), "R182 packed leaf width")
        if packed[0] in leaf_ids:
            need(packed[0] not in leaf_rows, "selected R182 leaf uniqueness")
            leaf_rows[packed[0]] = dict(zip(leaf_columns, packed, strict=True))
    need(total_leaf_rows == 202_840 and set(leaf_rows) == leaf_ids, "R182 selected leaf cover")

    r272 = closed_wrapper(R272_CERT)
    r272_by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in r272["formal_side_signature_ledger"]["rows"]:
        check_row(row, "R272 side signature")
        if row["Round182_leaf_row_id"] in leaf_ids:
            r272_by_leaf[row["Round182_leaf_row_id"]].append(row)

    graph_contact_rows: list[dict[str, Any]] = []
    for contact in exact_graph_contacts:
        leaf_id = contact["physical_witness_cell"]["leaf_row_id"]
        leaf = leaf_rows[leaf_id]
        need(leaf["box"] == contact["physical_witness_cell"]["exact_box"], "R291/R182 exact box")
        face_field = "lower_t_face_status" if contact["t0_face"] == "LOWER" else "upper_t_face_status"
        t0_status = leaf[face_field]
        need(
            type(t0_status) is str
            and (t0_status.startswith("A") or t0_status.startswith("S")),
            "R182 target graph absent on t0 face",
        )
        r272_rows = r272_by_leaf.get(leaf_id, [])
        need(
            r272_rows
            and all(
                row["exact_source_factor_identity"]
                == "source transverse wall factor = (9/25)*t with chart-dependent sign"
                and row["excluded_zero_face"] == "t=0"
                for row in r272_rows
            ),
            "R272 exact source t0 exclusion",
        )
        route_census["EXACT_NONINCIDENCE_R182_TARGET_GRAPH_ABSENT_ON_T0_FACE"] += 1
        graph_contact_rows.append({
            **contact,
            "route": "EXACT_NONINCIDENCE_R182_TARGET_GRAPH_ABSENT_ON_T0_FACE",
            "closed_box_contact_is_not_physical_graph_intersection": True,
            "R182_t0_face_status": t0_status,
            "R182_opposite_face_status": leaf[
                "upper_t_face_status" if face_field == "lower_t_face_status" else "lower_t_face_status"
            ],
            "R182_graph_classification": leaf["graph_classification"],
            "R272_selected_row_sha256s": sorted(row["row_sha256"] for row in r272_rows),
            "same_physical_point_proven": False,
        })

    binding_keys: set[tuple[str, int]] = set()
    target_ids: set[str] = set()
    binding_count = 0
    for binding in gzip_array(R295A_LEDGER):
        check_row(binding, "R295A binding")
        binding_count += 1
        key = (
            binding["Round291_local_disposition_row_id"],
            binding["physical_witness_cell_index"],
        )
        need(key not in binding_keys, "unique R295A physical key")
        binding_keys.add(key)
        for contact in t0_contacts_by_key.get(key, []):
            contact["R295A_binding"] = {
                "row_id": binding["Round295A_R291_physical_incidence_binding_row_id"],
                "row_sha256": binding["row_sha256"],
                "classification": binding["Round295A_binding_classification"],
                "source_binding_classification": binding["source_Round293_binding_classification"],
                "exact_witness_covered_by_named_registry_supports": binding["exact_witness_covered_by_named_registry_supports"],
                "target_rows": binding["target_Round294_registry_rows"],
            }
            target_ids.update(binding["target_Round294_registry_occurrence_ids"])
    need(binding_count == 113_452 and binding_keys == physical_keys, "R291/R295A complete bijection")
    need(
        all("R295A_binding" in row for rows in t0_contacts_by_key.values() for row in rows),
        "all t0 contacts bound",
    )

    raw_product = len(source_sheets) * physical_cell_count
    need(sum(route_census.values()) + 88 == raw_product, "lower Cartesian preliminary partition")
    state = {
        "R291_disposition_count": disposition_count,
        "R291_physical_cell_count": physical_cell_count,
        "R291_witness_kind_census": dict(sorted(kind_census.items())),
        "R295A_binding_count": binding_count,
        "current_double_source_sheet_count": len(source_sheets),
        "current_sheet_by_physical_cell_cartesian_count": raw_product,
        "pre_component_route_census": dict(sorted(route_census.items())),
        "R182_closed_box_t0_contact_count": len(graph_contact_rows),
        "R182_closed_box_contacts_rejected_by_exact_face_status_count": len(graph_contact_rows),
        "exact_t0_contact_count": sum(map(len, t0_contacts_by_key.values())),
        "graph_contact_rows": sorted(graph_contact_rows, key=canonical),
        "t0_contact_rows": sorted(
            [row for rows in t0_contacts_by_key.values() for row in rows],
            key=canonical,
        ),
        "source_sheet_geometry": sorted([
            {
                "member_id": item["row"]["wall_sheet_node_id"],
                "chart": item["chart"],
                "base": [str(value) for value in item["base"]],
            }
            for item in sheet_geometry
        ], key=canonical),
        "physical_cell_sequence_sha256": list_sequence_hash(physical_sequence),
    }
    return state, target_ids


def collect_current_members(target_ids: set[str]) -> tuple[dict[str, dict[str, Any]], int]:
    output: dict[str, dict[str, Any]] = {}
    count = 0
    for row in jsonl_rows(C15_MEMBER):
        count += 1
        member = row["registry_member_id"]
        if member in target_ids:
            check_row(row, "selected C15 member")
            need(member not in output, "selected C15 member uniqueness")
            output[member] = row
    return output, count


def collect_c25(target_ids: set[str]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for row in jsonl_rows(C25_MEMBER):
        member = row["member_id"]
        if member in target_ids:
            check_row(row, "selected C25 member")
            need(member not in output, "selected C25 member uniqueness")
            output[member] = row
    return output


def collect_c22b(target_ids: set[str]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for row in jsonl_rows(C22B_LEDGER):
        member = row["member_id"]
        if member in target_ids:
            check_row(row, "selected C22B member support")
            need(member not in output, "selected C22B member uniqueness")
            output[member] = row
    return output


def finalize_lower_frontier(
    state: dict[str, Any],
    c15: dict[str, dict[str, Any]],
    lower_c25: dict[str, dict[str, Any]],
    lower_c22b: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    routes = Counter(state["pre_component_route_census"])
    finalized: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    confirmed_witnesses: list[dict[str, Any]] = []

    for contact in state["t0_contact_rows"]:
        sheet_id = contact["sheet_member_id"]
        binding = contact["R295A_binding"]
        targets = binding["target_rows"]
        need(len(targets) == 1, "unique t0 target registry row")
        target = targets[0]
        target_id = target["registry_occurrence_id"]
        need(sheet_id in c15 and target_id in c15, "t0 endpoints in C15")
        need(target_id in lower_c25, "t0 target C25 support binding")
        sheet_component = c15[sheet_id]["fresh_component_id"]
        target_component = c15[target_id]["fresh_component_id"]
        signature_match = (
            target["complete_10_field_return_signature_sha256"]
            == contact["sheet_owner_signature_sha256"]
            and target["official_key_id"] == contact["sheet_owner_official_key_id"]
        )
        same_component = sheet_component == target_component
        kind = contact["physical_witness_cell"]["witness_kind"]
        evidence: dict[str, Any] = {
            **contact,
            "target_registry_occurrence_id": target_id,
            "target_registry_row": target,
            "target_C25_row_sha256": lower_c25[target_id]["row_sha256"],
            "sheet_component_id": sheet_component,
            "target_component_id": target_component,
            "cross_component": not same_component,
            "owner_signature_and_official_key_match": signature_match,
        }

        if signature_match:
            need(same_component, "matched t0 owner must already be connected")
            route = "KNOWN_T0_OWNER_INCIDENCE__SIGNATURE_MATCH__WITHIN_C15_COMPONENT"
            evidence.update({
                "route": route,
                "same_physical_support_owner_proven": True,
                "same_physical_point_proven": True,
            })
        elif kind == "SOURCE_EXACT_T0_SHEET_CELL":
            need(same_component, "mismatched R204 sheet boundary stays within component")
            route = "KNOWN_BOUNDARY_TRANSFER__R204_EXACT_T0_SHEET__WITHIN_C15_COMPONENT"
            evidence.update({
                "route": route,
                "same_physical_point_proven": False,
                "boundary_transfer_already_within_C15_component": True,
            })
        else:
            need(kind == "ROUND179_NEGATIVE_T0_SHADOW_PATCH", "only negative shadow mismatch remains")
            need(not same_component, "negative shadow mismatch expected cross component")
            need(target_id in lower_c22b, "cross-component shadow C22B support")
            support = lower_c22b[target_id]
            ast = support["normalized_support_ast"]
            need(
                ast.get("kind") == "OPEN_RATIONAL_BOX"
                and ast.get("coordinates") == ["t", "p", "s"]
                and ast.get("coordinate_chart") == contact["sheet_chart"],
                "cross shadow open support AST",
            )
            target_bounds = tuple(Fraction(x) for x in ast["bounds"])
            cell_bounds = tuple(Fraction(x) for x in contact["physical_witness_cell"]["exact_bounds"])
            need(
                target_bounds[0] == 0 < target_bounds[1]
                and target_bounds[2:] == cell_bounds[2:],
                "shadow closure/open-target boundary equality",
            )
            sheet_base = tuple(Fraction(x) for x in contact["sheet_exact_closed_base_rectangle"])
            p0, p1 = max(sheet_base[0], cell_bounds[2]), min(sheet_base[1], cell_bounds[3])
            s0, s1 = max(sheet_base[2], cell_bounds[4]), min(sheet_base[3], cell_bounds[5])
            need(p0 <= p1 and s0 <= s1 and (p0 == p1 or s0 == s1), "shadow boundary-only contact")
            point = (
                Fraction(0),
                p0 if p0 == p1 else (p0 + p1) / 2,
                s0 if s0 == s1 else (s0 + s1) / 2,
            )
            sheet_contains = (
                sheet_base[0] <= point[1] <= sheet_base[1]
                and sheet_base[2] <= point[2] <= sheet_base[3]
            )
            shadow_closure_contains = (
                cell_bounds[2] <= point[1] <= cell_bounds[3]
                and cell_bounds[4] <= point[2] <= cell_bounds[5]
            )
            target_open_contains = all(
                target_bounds[2 * axis] < point[axis] < target_bounds[2 * axis + 1]
                for axis in range(3)
            )
            need(sheet_contains and shadow_closure_contains and not target_open_contains, "codimension-two membership evaluation")
            covering = []
            cover_intervals: list[tuple[Fraction, Fraction]] = []
            for owner in state["source_sheet_geometry"]:
                if owner["chart"] != contact["sheet_chart"]:
                    continue
                owner_base = tuple(Fraction(value) for value in owner["base"])
                if not (owner_base[0] <= point[1] <= owner_base[1]):
                    continue
                lower, upper = max(s0, owner_base[2]), min(s1, owner_base[3])
                if lower > upper:
                    continue
                member = owner["member_id"]
                need(member in c15, "t0 covering source sheet in C15")
                covering.append({
                    **owner,
                    "component_id": c15[member]["fresh_component_id"],
                    "C15_row_sha256": c15[member]["row_sha256"],
                })
                cover_intervals.append((lower, upper))
            need(
                bool(covering),
                "nonempty complete t0 owner cover:"
                + contact["sheet_chart"] + ":" + str(point[1]) + ":" + str(s0) + ":" + str(s1),
            )
            cover_intervals.sort()
            merged: list[list[Fraction]] = []
            for lower, upper in cover_intervals:
                if not merged or lower > merged[-1][1]:
                    merged.append([lower, upper])
                else:
                    merged[-1][1] = max(merged[-1][1], upper)
            need(merged == [[s0, s1]], "complete t0 owner locus cover")
            owner_components = {row["component_id"] for row in covering}
            need(owner_components == {sheet_component}, "unique t0 owner component equals source")
            route = (
                "EXACT_NONEDGE__TARGET_OPEN_SUPPORT_EXCLUDES_CONTACT__"
                "COMPLETE_T0_OWNER_COVER_HAS_SOURCE_SHEET_COMPONENT"
            )
            evidence.update({
                "route": route,
                "candidate_discovery_family": "DOUBLE_GRAPHS",
                "most_likely_semantic_family": "REPRESENTATION_ALIASES_OR_LOWER_DIMENSIONAL_OWNER_TRANSFER",
                "C22B_support_row_sha256": support["row_sha256"],
                "target_normalized_support_ast": ast,
                "closure_contact_point_t_p_s": [str(x) for x in point],
                "sheet_closed_support_contains_contact_point": sheet_contains,
                "R291_shadow_cell_closure_contains_contact_point": shadow_closure_contains,
                "target_OPEN_RATIONAL_BOX_contains_contact_point": target_open_contains,
                "same_physical_point_proven": False,
                "complete_t0_owner_covering_member_ids": sorted(row["member_id"] for row in covering),
                "complete_t0_owner_covering_member_count": len(covering),
                "complete_t0_owner_covering_intervals": [
                    [str(lower), str(upper)] for lower, upper in cover_intervals
                ],
                "complete_t0_owner_unique_component_id": sheet_component,
                "complete_t0_owner_component_count": 1,
                "target_component_is_t0_owner_component": False,
                "why_not_counterexample": (
                    "the target open support excludes the contact and the complete R248 t=0 "
                    "owner cover lies in the source-sheet C15 component"
                ),
            })

        routes[route] += 1
        finalized.append(evidence)

    need(Counter(row["route"] for row in finalized) == {
        "KNOWN_T0_OWNER_INCIDENCE__SIGNATURE_MATCH__WITHIN_C15_COMPONENT": 40,
        "KNOWN_BOUNDARY_TRANSFER__R204_EXACT_T0_SHEET__WITHIN_C15_COMPONENT": 24,
        "EXACT_NONEDGE__TARGET_OPEN_SUPPORT_EXCLUDES_CONTACT__COMPLETE_T0_OWNER_COVER_HAS_SOURCE_SHEET_COMPONENT": 24,
    }, "final t0 route census")
    need(not unresolved and not confirmed_witnesses, "cross shadow owner-component closure")
    need(sum(routes.values()) == state["current_sheet_by_physical_cell_cartesian_count"], "complete lower Cartesian partition")

    summary = {
        key: value
        for key, value in state.items()
        if key not in {"graph_contact_rows", "t0_contact_rows", "pre_component_route_census"}
    }
    summary.update({
        "route_census": dict(sorted(routes.items())),
        "partition_sum": sum(routes.values()),
        "each_pair_has_exactly_one_route": True,
        "R182_rejected_closed_box_contact_rows_sha256": digest(state["graph_contact_rows"]),
        "t0_finalized_contact_rows_sha256": digest(finalized),
        "t0_owner_signature_match_same_component_count": 40,
        "t0_signature_mismatch_same_component_count": 24,
        "t0_negative_shadow_cross_component_unresolved_count": 0,
        "t0_negative_shadow_exact_nonedge_owner_component_count": 24,
        "confirmed_legal_cross_component_witness_count": 0,
        "unresolved_candidate_count": len(unresolved),
    })
    evidence_rows = [
        candidate_row({
            "schema": "cm2.c27-semantic-counterexample-gate.double-graphs.zero-credit.v2.lower-candidate-row.v1",
            "candidate_class": "R182_CLOSED_BOX_T0_CONTACT_REJECTED_BY_FACE_STATUS",
            **row,
            "formal_credit": 0,
        })
        for row in state["graph_contact_rows"]
    ] + [
        candidate_row({
            "schema": "cm2.c27-semantic-counterexample-gate.double-graphs.zero-credit.v2.lower-candidate-row.v1",
            "candidate_class": "EXACT_T0_CONTACT",
            **row,
            "formal_credit": 0,
        })
        for row in finalized
    ]
    return summary, evidence_rows, unresolved


def collect_features(target_members: set[str]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    roots: dict[str, dict[str, Any]] = {}
    dependents: dict[str, dict[str, Any]] = {}
    for row in jsonl_rows(C26_FEATURE):
        owner = row["owner_member_id"]
        if owner not in target_members:
            continue
        check_row(row, "selected C26 feature")
        if row["node_id"] == "G1":
            need(owner not in roots, "unique selected G1")
            roots[owner] = row
        elif row["node_id"] in {"G2A", "G2B"}:
            need(owner not in dependents, "unique selected G2")
            dependents[owner] = row
    return roots, dependents


def collect_supports(target_members: set[str]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    graphs: dict[str, dict[str, Any]] = {}
    positive: dict[str, dict[str, Any]] = {}
    empty: dict[str, dict[str, Any]] = {}
    for row in jsonl_rows(C10_LEDGER):
        member = row["sheet_member_id"]
        if member in target_members:
            check_row(row, "selected C10 graph")
            need(member not in graphs, "unique selected C10 graph")
            graphs[member] = row
    for row in jsonl_rows(C24A_LEDGER):
        member = row["member_id"]
        if member in target_members:
            check_row(row, "selected C24A support")
            need(member not in positive, "unique selected C24A support")
            positive[member] = row
    for row in jsonl_rows(C24B_LEDGER):
        member = row["member_id"]
        if member in target_members:
            check_row(row, "selected C24B support")
            need(member not in empty, "unique selected C24B support")
            empty[member] = row
    return graphs, positive, empty


def candidate_row(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def reconstruct() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated no-bytecode runtime")
    for name, expected in INPUT_PINS.items():
        guard_input(name, expected)

    partitions, raw_sheets, raw_bulks = load_raw_graphs()
    lower_state, lower_target_ids = load_lower_frontier(raw_sheets, partitions)

    raw_feature_ids = {row["wall_sheet_node_id"] for row in raw_sheets} | {row["wall_bulk_node_id"] for row in raw_bulks}
    all_current_targets = raw_feature_ids | lower_target_ids
    c15, c15_count = collect_current_members(all_current_targets)
    need(c15_count == 502_204, "C15 member census")

    source_sheets = [row for row in raw_sheets if row["endpoint_factor"] == "source"]
    target_sheets = [row for row in raw_sheets if row["endpoint_factor"] == "target"]
    same_sides = [row for row in raw_bulks if row["branch_label"] == "SAME_SIGN_EVENT_ABSENT"]
    source_other_sides = [row for row in raw_bulks if row["branch_label"] == "NEGATIVE_TO_POSITIVE"]
    target_other_sides = [row for row in raw_bulks if row["branch_label"] == "POSITIVE_TO_NEGATIVE"]
    need(len(source_sheets) == len(target_sheets) == len(same_sides) == len(source_other_sides) == len(target_other_sides) == 16, "raw double feature partition")
    present_source_ids = {row["wall_sheet_node_id"] for row in source_sheets}
    present_same_ids = {row["wall_bulk_node_id"] for row in same_sides}
    present_source_other_ids = {row["wall_bulk_node_id"] for row in source_other_sides}
    missing_target_ids = {row["wall_sheet_node_id"] for row in target_sheets} | {row["wall_bulk_node_id"] for row in target_other_sides}
    corrected_ids = present_source_ids | present_same_ids | present_source_other_ids
    need(set(c15) & raw_feature_ids == corrected_ids, "C15 corrected double feature population 48=16+16+16")
    need(not (set(c15) & missing_target_ids), "superseded target features absent from C15")

    c25_all = collect_c25(corrected_ids | lower_target_ids)
    c25 = {member: row for member, row in c25_all.items() if member in corrected_ids}
    lower_c25 = {member: row for member, row in c25_all.items() if member in lower_target_ids}
    need(set(c25) == corrected_ids, "C25 corrected double support cover")
    need(set(lower_c25) == lower_target_ids, "C25 lower-target support cover")
    for member, row in c25.items():
        need(row["fresh_component_id"] == c15[member]["fresh_component_id"], "C15/C25 component binding")
        need(row["source_bindings"]["C15_member_row_sha256"] == c15[member]["row_sha256"], "C15/C25 row binding")
    for member, row in lower_c25.items():
        need(row["fresh_component_id"] == c15[member]["fresh_component_id"], "lower C15/C25 component binding")
        need(row["source_bindings"]["C15_member_row_sha256"] == c15[member]["row_sha256"], "lower C15/C25 row binding")
    c22b_target_ids = {
        member
        for member, row in lower_c25.items()
        if row["source_bindings"]["support_kernel"] == "C22B"
    }
    lower_c22b = collect_c22b(c22b_target_ids)
    need(set(lower_c22b) == c22b_target_ids, "C22B selected target support cover")
    lower_summary, lower_evidence_rows, lower_unresolved = finalize_lower_frontier(
        lower_state,
        c15,
        lower_c25,
        lower_c22b,
    )

    roots, dependents = collect_features(corrected_ids)
    need(set(roots) == present_source_ids and set(dependents) == corrected_ids, "C26 G1/G2 selected cover")
    need(all(row["obligation_kind"] == "G1_EXACT_GRAPH_DEFINITION" and row["obligation_role"] == "INDEPENDENT_DEFINITION_ROOT" and row["depends_on_node_ids"] == [] for row in roots.values()), "C26 G1 definition roots")
    need(sum(row["node_id"] == "G2A" for row in dependents.values()) == 16 and sum(row["node_id"] == "G2B" for row in dependents.values()) == 32, "C26 G2 type census")

    graphs, positive_supports, empty_supports = collect_supports(corrected_ids)
    need(set(graphs) == present_source_ids, "C10 exact graph cover")
    need(set(positive_supports) == present_source_ids | present_same_ids, "C24A graph/sheet plus positive-side cover")
    need(set(empty_supports) == present_source_other_ids, "C24B empty-side cover")

    by_pid_sheet = {row["source_partition_row_id"]: row for row in source_sheets}
    by_pid_same = {row["source_partition_row_id"]: row for row in same_sides}
    by_pid_other = {row["source_partition_row_id"]: row for row in source_other_sides}
    member_pid: dict[str, str] = {}
    member_role: dict[str, str] = {}
    for pid in sorted(partitions):
        sheet, same, other = by_pid_sheet[pid], by_pid_same[pid], by_pid_other[pid]
        member_pid[sheet["wall_sheet_node_id"]] = pid
        member_pid[same["wall_bulk_node_id"]] = pid
        member_pid[other["wall_bulk_node_id"]] = pid
        member_role[sheet["wall_sheet_node_id"]] = "SOURCE_GRAPH_SHEET"
        member_role[same["wall_bulk_node_id"]] = "SAME_SIGN_EVENT_ABSENT_SIDE"
        member_role[other["wall_bulk_node_id"]] = "NEGATIVE_TO_POSITIVE_SIDE"

    intrinsic: dict[tuple[str, str], dict[str, Any]] = {}
    cross_witnesses: list[dict[str, Any]] = []
    for pid in sorted(partitions):
        partition = partitions[pid]
        frontier = partition["_frontier"]
        sheet = by_pid_sheet[pid]
        same = by_pid_same[pid]
        other = by_pid_other[pid]
        sheet_id = sheet["wall_sheet_node_id"]
        same_id = same["wall_bulk_node_id"]
        other_id = other["wall_bulk_node_id"]
        graph = graphs[sheet_id]
        sheet_support = positive_supports[sheet_id]
        same_support = positive_supports[same_id]
        empty_support = empty_supports[other_id]
        graph_id = graph["graph_id"]

        need(graph["graph_class"] == "R235D_SOURCE_EXACT_FACE_FULL_BASE", "C10 corrected double graph class")
        need(graph["sheet_member_id"] == sheet_id and roots[sheet_id]["feature_id"] == graph_id, "C10/C26 G1 graph identity")
        need(roots[sheet_id]["source_bindings"]["source_row_sha256"] == graph["row_sha256"], "C10/C26 G1 row binding")
        need(graph["carrier_domain_ast"] == {"op": "AND", "args": [
            {"coordinate": "t", "lower": frontier["box"][0], "op": "CLOSED_INTERVAL", "upper": frontier["box"][1]},
            {"coordinate": "p", "lower": frontier["box"][2], "op": "CLOSED_INTERVAL", "upper": frontier["box"][3]},
            {"coordinate": "s", "lower": frontier["box"][4], "op": "CLOSED_INTERVAL", "upper": frontier["box"][5]},
        ]}, "C10/R234 exact carrier")
        base = graph_base(graph["base_domain_ast"])
        raw_base = tuple(Fraction(x) for x in sheet["exact_closed_base_rectangle"])
        need(base == raw_base == exact_sheet_base(sheet_support["normalized_support_ast"]), "C10/C24A/R248 exact sheet base")
        need(sheet_support["graph_id"] == same_support["graph_id"] == empty_support["graph_id"] == graph_id, "one graph ID owns all three corrected features")
        need(sheet_support["row_kind"] == "G2A_GRAPH_TO_SHEET_MEMBER_AND_REPRESENTATION_SET_EQUALITY", "G2A sheet support kind")
        need(same_support["row_kind"] == "G2B_RELATION_BACKED_SIDE_MEMBER_AND_REPRESENTATION_SET_EQUALITY", "G2B positive side support kind")
        need(empty_support["normalized_support_ast"] == {"ambient_coordinates": ["t", "p", "s"], "coordinate_parameter": "TPS", "kind": "EMPTY_SET"}, "G2B exact empty support")
        need(one_sided_trace_base(same_support["normalized_support_ast"]) == base, "positive side closure trace equals graph sheet")
        need(c25[sheet_id]["source_bindings"]["support_kernel_row_sha256"] == sheet_support["row_sha256"], "C25 sheet support binding")
        need(c25[same_id]["source_bindings"]["support_kernel_row_sha256"] == same_support["row_sha256"], "C25 positive side support binding")
        need(c25[other_id]["source_bindings"]["support_kernel_row_sha256"] == empty_support["row_sha256"], "C25 empty side support binding")
        need(dependents[sheet_id]["obligation_kind"] == "G2A_GRAPH_TO_SHEET_IDENTIFICATION", "C26 G2A kind")
        need(dependents[same_id]["obligation_kind"] == "G2B_GRAPH_TO_SIDE_PHYSICAL_INCIDENCE", "C26 positive G2B kind")
        need(dependents[other_id]["obligation_kind"] == "G2B_GRAPH_TO_SIDE_EXACT_NONINCIDENCE", "C26 empty G2B kind")

        same_cross = c15[sheet_id]["fresh_component_id"] != c15[same_id]["fresh_component_id"]
        positive = {
            "sheet_member_id": sheet_id,
            "side_member_id": same_id,
            "graph_id": graph_id,
            "source_partition_row_id": pid,
            "classification": "LEGAL_ONE_SIDED_GRAPH_TRACE__KNOWN_SHEET_OWNER_RELATION",
            "sheet_component_id": c15[sheet_id]["fresh_component_id"],
            "side_component_id": c15[same_id]["fresh_component_id"],
            "cross_component": same_cross,
            "support_evidence": {
                "graph_row_sha256": graph["row_sha256"],
                "sheet_support_row_sha256": sheet_support["row_sha256"],
                "side_support_row_sha256": same_support["row_sha256"],
                "exact_base": [str(x) for x in base],
            },
        }
        intrinsic[(sheet_id, same_id)] = positive
        if same_cross:
            cross_witnesses.append(positive)
        intrinsic[(sheet_id, other_id)] = {
            "sheet_member_id": sheet_id,
            "side_member_id": other_id,
            "graph_id": graph_id,
            "source_partition_row_id": pid,
            "classification": "EXACT_NONEDGE__SIDE_NORMALIZED_SUPPORT_IS_EMPTY_SET",
            "sheet_component_id": c15[sheet_id]["fresh_component_id"],
            "side_component_id": c15[other_id]["fresh_component_id"],
            "cross_component": c15[sheet_id]["fresh_component_id"] != c15[other_id]["fresh_component_id"],
            "support_evidence": {
                "graph_row_sha256": graph["row_sha256"],
                "empty_support_row_sha256": empty_support["row_sha256"],
                "empty_support_ast_sha256": empty_support["normalized_support_ast_sha256"],
            },
        }

    rows: list[dict[str, Any]] = []
    classification_census: Counter[str] = Counter()
    graph_side_unresolved: list[dict[str, Any]] = []
    corrected_sheets_sorted = sorted(present_source_ids)
    corrected_sides_sorted = sorted(present_same_ids | present_source_other_ids)
    source_sheet_by_id = {row["wall_sheet_node_id"]: row for row in source_sheets}
    same_side_by_id = {row["wall_bulk_node_id"]: row for row in same_sides}
    ordinal = 0
    for sheet_id in corrected_sheets_sorted:
        for side_id in corrected_sides_sorted:
            sheet_pid = member_pid[sheet_id]
            side_pid = member_pid[side_id]
            sheet_component = c15[sheet_id]["fresh_component_id"]
            side_component = c15[side_id]["fresh_component_id"]
            cross_component = sheet_component != side_component
            support_evidence: dict[str, Any]

            if side_id in present_source_other_ids:
                classification = "EXACT_NONEDGE__SIDE_NORMALIZED_SUPPORT_IS_EMPTY_SET"
                empty = empty_supports[side_id]
                support_evidence = {
                    "empty_support_row_sha256": empty["row_sha256"],
                    "empty_support_ast_sha256": empty["normalized_support_ast_sha256"],
                    "empty_support_is_global_across_partitions_and_charts": True,
                }
            else:
                need(side_id in present_same_ids, "known corrected side role")
                sheet = source_sheet_by_id[sheet_id]
                side = same_side_by_id[side_id]
                sheet_frontier = partitions[sheet_pid]["_frontier"]
                side_frontier = partitions[side_pid]["_frontier"]
                sheet_base = tuple(Fraction(x) for x in sheet["exact_closed_base_rectangle"])
                side_base = one_sided_trace_base(positive_supports[side_id]["normalized_support_ast"])
                if sheet_frontier["chart"] != side_frontier["chart"]:
                    classification = "EXACT_NONINCIDENCE_CROSS_CHART_T0_GLOBAL_PHASE_MISMATCH"
                    support_evidence = {
                        "sheet_chart": sheet_frontier["chart"],
                        "side_chart": side_frontier["chart"],
                        "sheet_exact_base": [str(x) for x in sheet_base],
                        "side_closure_trace_exact_base": [str(x) for x in side_base],
                        "different_chart_identifier_alone_used_as_nonincidence_proof": False,
                        "exact_global_phase_equation": cross_chart_t0_phase_nonincidence(
                            sheet_frontier["chart"], side_frontier["chart"]
                        ),
                    }
                else:
                    relation, overlap_p, overlap_s = rectangle_metrics(sheet_base, side_base)
                    if relation in {"EXACT_EQUAL", "STRICT_POSITIVE_AREA_INTERSECTION"}:
                        need(sheet_pid == side_pid and not cross_component, "same-partition full trace relation")
                        classification = "LEGAL_ONE_SIDED_GRAPH_TRACE__KNOWN_SHEET_OWNER_RELATION"
                    elif relation == "CLOSED_BOUNDARY_CONTACT_ONLY":
                        need(sheet_pid != side_pid and not cross_component, "cross-partition boundary contact already connected")
                        classification = "KNOWN_SAME_COMPONENT_CROSS_PARTITION_BOUNDARY_CLOSURE_CONTACT"
                    else:
                        classification = "EXACT_NONINCIDENCE_SAME_CHART_BASE_RECTANGLE_DISJOINT"
                    support_evidence = {
                        "chart": sheet_frontier["chart"],
                        "sheet_exact_base": [str(x) for x in sheet_base],
                        "side_closure_trace_exact_base": [str(x) for x in side_base],
                        "base_relation": relation,
                        "overlap_p": str(overlap_p),
                        "overlap_s": str(overlap_s),
                        "side_support_row_sha256": positive_supports[side_id]["row_sha256"],
                    }

            body = {
                "schema": "cm2.c27-semantic-counterexample-gate.double-graphs.zero-credit.v2.graph-side-row.v1",
                "candidate_ordinal": ordinal,
                "sheet_member_id": sheet_id,
                "side_member_id": side_id,
                "sheet_source_partition_row_id": sheet_pid,
                "side_source_partition_row_id": side_pid,
                "sheet_role": member_role[sheet_id],
                "side_role": member_role[side_id],
                "route": classification,
                "cross_component": cross_component,
                "sheet_component_id": sheet_component,
                "side_component_id": side_component,
                "support_evidence": support_evidence,
                "formal_credit": 0,
            }
            classification_census[classification] += 1
            row = candidate_row(body)
            rows.append(row)
            if classification.startswith("UNRESOLVED_"):
                graph_side_unresolved.append(row)
            ordinal += 1
    need(len(rows) == 512 and classification_census == {
        "EXACT_NONEDGE__SIDE_NORMALIZED_SUPPORT_IS_EMPTY_SET": 256,
        "EXACT_NONINCIDENCE_CROSS_CHART_T0_GLOBAL_PHASE_MISMATCH": 192,
        "EXACT_NONINCIDENCE_SAME_CHART_BASE_RECTANGLE_DISJOINT": 32,
        "LEGAL_ONE_SIDED_GRAPH_TRACE__KNOWN_SHEET_OWNER_RELATION": 16,
        "KNOWN_SAME_COMPONENT_CROSS_PARTITION_BOUNDARY_CLOSURE_CONTACT": 16,
    }, "complete graph-side geometric Cartesian partition")
    need(not cross_witnesses, "no confirmed intrinsic cross-component witness")

    rows.extend(lower_evidence_rows)
    lower_aggregate_unresolved_count = sum(
        count
        for route, count in lower_summary["route_census"].items()
        if route.startswith("UNRESOLVED_")
    )
    unresolved_candidate_count = len(graph_side_unresolved) + lower_aggregate_unresolved_count
    need(unresolved_candidate_count > 0 and not lower_unresolved, "only non-t0 residual buckets remain fail-closed")
    strongest_unresolved = None
    minimal_witness = None
    status = (
        "REJECT_ZERO_CREDIT__C27_SEMANTIC_FAMILY_EXHAUSTION_NOT_PROVEN__"
        "DOUBLE_GRAPH_GRAPH_SIDE_AND_LOWER_OWNER_BUCKETS_CLOSED__"
        "EMBEDDED_ALIAS_AND_TRANSVERSE_BUCKETS_REQUIRE_SEPARATE_SUBGATE_COMPOSITION"
    )
    recheck_input_snapshots()
    result_body = {
        "schema": "cm2.c27-semantic-counterexample-gate.double-graphs.zero-credit.result.v2",
        "status": status,
        "gate_decision": "REJECT_C27_C28_C29_FOR_UNCONDITIONAL_PHYSICAL_MAXIMALITY",
        "scope": {
            "family": "DOUBLE_GRAPHS",
            "candidate_discovery_family_may_differ_from_final_semantic_family": True,
            "C27_source_or_family_table_imported": False,
            "C6_or_C14D_or_C15_edge_ledger_consumed": False,
            "different_lineage_or_partition_used_as_nonincidence_filter": False,
            "candidate_generation_basis": [
                "R234/R236/R248 source-partition and exact rational geometry",
                "C10 exact graph support AST",
                "C24A one-sided trace and C24B exact empty support AST",
                "C15 current member/component partition",
                "C25 exact support binding",
                "C26 independent G1 and dependent G2 obligation cover",
                "complete R291 physical-cell and R295A binding frontier",
                "R182 exact t-face graph status and R272 source-factor identity",
                "C22B open-box support membership for cross-component shadow targets",
            ],
        },
        "corrected_double_graph_census": {
            "R236_double_partitions": 16,
            "raw_R248_sheets": 32,
            "raw_R248_side_bulks": 48,
            "C15_present_source_graph_sheets": 16,
            "C15_present_same_sign_sides": 16,
            "C15_present_negative_to_positive_sides": 16,
            "C15_absent_superseded_target_sheets": 16,
            "C15_absent_superseded_positive_to_negative_sides": 16,
            "C10_G1_graph_definitions": 16,
            "C24A_positive_supports": 32,
            "C24B_exact_empty_supports": 16,
            "C25_support_bindings": 48,
            "C26_G1_roots": 16,
            "C26_G2_dependents": 48,
        },
        "graph_side_cartesian_partition": {
            "sheet_count": 16,
            "side_count": 32,
            "cartesian_pair_count": 512,
            "classification_census": dict(sorted(classification_census.items())),
            "partition_sum": sum(classification_census.values()),
            "each_pair_has_exactly_one_route": True,
        },
        "lower_physical_attachment_partition": lower_summary,
        "confirmed_legal_cross_component_witness_count": 0,
        "cross_component_witness_count": 0,
        "minimal_witness": minimal_witness,
        "unresolved_candidate_count": unresolved_candidate_count,
        "strongest_unresolved_candidate": strongest_unresolved,
        "strongest_unresolved_candidate_is_not_a_counterexample": None,
        "strongest_unresolved_candidate_blocker": (
            "the embedded scan still leaves cross-chart R291 cells and transverse-1D rows "
            "to their separately sealed zero-credit semantic subgates"
        ),
        "superseded_prior_diagnostic": {
            "path": str(SUPERSEDED_OUTPUT.relative_to(ROOT.parent)),
            "claimed_result_object_sha256": "65b42088a9f5699d95336e0225909893041b835035c8baa1e8ae453478336639",
            "superseded": True,
            "invalid_for_evidence": True,
            "reasons": [
                "it used same retained-child/chart identity as a candidate-generation filter",
                "it classified 480 different-partition graph/side pairs by identifier mismatch instead of geometry",
            ],
        },
        "input_pins": [{"filename": name, "sha256": value} for name, value in sorted(INPUT_PINS.items())],
        "input_capture": {
            "open_mode": "O_RDONLY|O_CLOEXEC|O_NOFOLLOW",
            "pre_and_post_full_sha256_and_inode_snapshot_equal": True,
            "all_inputs_direct_children_of_deliverables": True,
        },
        "ledger": {
            "filename": LEDGER,
            "row_count": len(rows),
            "graph_side_row_count": 512,
            "R182_rejected_closed_box_contact_row_count": 96,
            "exact_t0_contact_row_count": 88,
            "rows_sha256": digest(rows),
            "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        },
        "formal_credit": {
            "transition_family_exhaustion": 0,
            "transition_theorem": 0,
            "new_DSU_edge": 0,
            "new_DSU_union": 0,
            "pair_routing": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "nonpromotion": {
            "development_diagnostic_only": True,
            "does_not_modify_or_upgrade_C27_C28_C29": True,
            "explicitly_rejects_using_C27_C28_C29_as_unconditional_maximality_authority": True,
            "does_not_claim_other_19_transition_families": True,
            "cross_family_face_and_rechart_equivalence_still_requires_independent_gates": True,
        },
        "required_next": [
            "run a second independent implementation of the 192 cross-chart t0 phase equations",
            "only after zero unresolved buckets, run a second implementation and coherent attacks before any PASS",
        ],
    }
    return rows, {**result_body, "result_sha256": digest(result_body)}


def gzip_rows(rows: list[dict[str, Any]]) -> bytes:
    import io
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, compresslevel=9, mtime=0) as stream:
        for row in rows:
            stream.write(canonical(row) + b"\n")
    return buffer.getvalue()


def exclusive_write(path: Path, payload: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
        0o400,
    )
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "exclusive write progress:" + path.name)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def verify_publication(
    output_dir: Path,
    expected_rows: list[dict[str, Any]],
    expected_result: dict[str, Any],
    expected_manifest: dict[str, Any],
) -> None:
    result_raw = (output_dir / RESULT).read_bytes()
    result = json.loads(result_raw)
    need(result_raw == canonical(result), "published result canonical")
    result_body = dict(result)
    result_sha = result_body.pop("result_sha256", None)
    need(result == expected_result and result_sha == digest(result_body), "published result closure")

    observed_rows: list[dict[str, Any]] = []
    with gzip.open(output_dir / LEDGER, "rb") as stream:
        for ordinal, raw in enumerate(stream):
            need(raw.endswith(b"\n"), "published ledger newline")
            row = json.loads(raw[:-1])
            need(canonical(row) == raw[:-1], "published ledger canonical row")
            check_row(row, "published ledger row:" + str(ordinal))
            observed_rows.append(row)
    need(observed_rows == expected_rows, "published ledger byte-semantic equality")
    need(
        len(observed_rows) == expected_result["ledger"]["row_count"]
        and digest(observed_rows) == expected_result["ledger"]["rows_sha256"]
        and digest([row["row_sha256"] for row in observed_rows])
        == expected_result["ledger"]["row_hashes_sha256"],
        "published ledger descriptor",
    )

    manifest_raw = (output_dir / MANIFEST).read_bytes()
    manifest = json.loads(manifest_raw)
    need(manifest_raw == canonical(manifest), "published manifest canonical")
    manifest_body = dict(manifest)
    manifest_sha = manifest_body.pop("manifest_sha256", None)
    need(
        manifest == expected_manifest and manifest_sha == digest(manifest_body),
        "published manifest closure",
    )
    actual_files = []
    for filename in (LEDGER, RESULT):
        path = output_dir / filename
        actual_files.append({
            "filename": filename,
            "size": path.stat().st_size,
            "sha256": file_hash(path),
        })
    need(actual_files == manifest["files"], "published manifest file map")


def publish(output_dir: Path, rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
    need(not output_dir.exists(), "exclusive output directory")
    output_dir.mkdir(mode=0o700, parents=False, exist_ok=False)
    ledger_bytes = gzip_rows(rows)
    result_bytes = canonical(result)
    manifest_body = {
        "schema": "cm2.c27-semantic-counterexample-gate.double-graphs.zero-credit.publication-manifest.v2",
        "result_object_sha256": result["result_sha256"],
        "files": [
            {"filename": LEDGER, "size": len(ledger_bytes), "sha256": hashlib.sha256(ledger_bytes).hexdigest()},
            {"filename": RESULT, "size": len(result_bytes), "sha256": hashlib.sha256(result_bytes).hexdigest()},
        ],
        "formal_credit": 0,
    }
    manifest = {**manifest_body, "manifest_sha256": digest(manifest_body)}
    exclusive_write(output_dir / LEDGER, ledger_bytes)
    exclusive_write(output_dir / RESULT, result_bytes)
    exclusive_write(output_dir / MANIFEST, canonical(manifest))
    directory_fd = os.open(output_dir, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    verify_publication(output_dir, rows, result, manifest)
    for filename in (LEDGER, RESULT, MANIFEST):
        os.chmod(output_dir / filename, 0o444)
    os.chmod(output_dir, 0o555)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--seed", required=True, help="bookkeeping only; output must be seed-independent")
    args = parser.parse_args()
    need(re.fullmatch(r"[0-9]{1,20}", args.seed) is not None, "numeric seed")
    requested = Path(args.output_dir)
    need(".." not in requested.parts, "output path traversal")
    audit_info = os.lstat(AUDIT_ROOT)
    need(
        stat.S_ISDIR(audit_info.st_mode)
        and not AUDIT_ROOT.is_symlink()
        and AUDIT_ROOT.resolve(strict=True) == AUDIT_ROOT,
        "fixed audit root",
    )
    output = requested.resolve(strict=False)
    need(
        output.parent == AUDIT_ROOT
        and re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,126}", output.name) is not None,
        "safe direct-child audit output",
    )
    rows, result = reconstruct()
    publish(output, rows, result)
    print(canonical({
        "status": result["status"],
        "result_sha256": result["result_sha256"],
        "cross_component_witness_count": result["cross_component_witness_count"],
        "unresolved_candidate_count": result["unresolved_candidate_count"],
        "seed_affects_output": False,
        "formal_credit": 0,
    }).decode("ascii"))
    if result["minimal_witness"] is not None:
        return 1
    return 2 if result["unresolved_candidate_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
