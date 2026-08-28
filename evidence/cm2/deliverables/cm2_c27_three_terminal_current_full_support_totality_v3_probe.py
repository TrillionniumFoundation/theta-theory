#!/usr/bin/env python3
"""C27-independent current-support diagnostic and fail-closed blocker probe.

The probe consumes the v3 C19 external identity crosswalk plus the current
C20A/C22A/C23A kernels, C15/C25 identities, and the pinned R294/R299A
occurrence identities.  It enumerates every strict positive-volume contact
between one of the 304,740 current-new C22A/C23A occurrences and the complete
51,172-row current C19A/B/C carrier universe.  Candidate generation is
partitioned only by the external physical chart; return signature and key are
audited attributes, never prefilters.  Geometry is decided by exact rational
interval arithmetic, including the signed t-squared branch transform.

No C27 artifact and no edge ledger is opened.  In particular, R300C is used
only as a validation set: it is never treated as the C24A candidate universe.
The complete 9,960-row G2B C24A interval-envelope universe is scanned against
all current-new targets with a physical-chart-only prefilter.  Because each
C24A support is its interval envelope AND a strict nonlinear relation, an
envelope hit is only a candidate and never positive-support credit.  The probe
therefore remains deliberately fail-closed until every envelope-only residual
has an exact strict-relation disposition and the 5,264 G2A supports have a
separate relative-2D terminal route.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent

C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C5 = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz"
C10 = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
R235 = "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
R236 = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R242 = "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"
C4 = "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz"
C20A = "cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz"
C22A = "cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz"
C23A = "cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz"
C24A = "cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz"
R294 = "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz"
R299A = "cm2_round299a_source_g_refined_occurrence_official_key_binding_closure_ledger.json.gz"
R300C = "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_volume_edge_promotion_witness_ledger.json.gz"
SIGNED = "cm2_round299_source_g_r292_signed_support_face_classifier_independent_probe_ledger.json.gz"
SIGNED_RESULT = "cm2_round299_source_g_r292_signed_support_face_classifier_independent_probe_result.json"
COMPLETE = "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_face_inventory.json.gz"
COMPLETE_RESULT = "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_result.json"

PINS = {
    C5: "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333",
    C10: "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c",
    R235: "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",
    R236: "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    R242: "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e",
    C4: "3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db",
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C20A: "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922",
    C22A: "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb",
    C23A: "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528",
    C24A: "ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58",
    R294: "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R299A: "ffea8120af2179990d5c9e7ff385193e2c5a08bed161cf5b570aa28b1f8b1ee0",
    R300C: "bbb690ba8236230bb99fa8c2dcf569f97c758d546c1ec56ae6d3f6c9d880c7e2",
    SIGNED: "9797d486eaf96ce8352883093c24637b5eb9cb27af60fd79e5ee03a6585d27a9",
    SIGNED_RESULT: "07427f743ace170d6d7d832c67658d8d27eca2d51092049625c117abfc8efcdb",
    COMPLETE: "443f26bdbed929d873972be0d2232809bf022feed1a5709001ee8f2dda49ac2d",
    COMPLETE_RESULT: "142a5bd878f0e52ee994e41fa7e1b59863cc70ce609a8ed8a8a15f1be346e82d",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def stat_fingerprint(path: Path) -> tuple[int, int, int, int, int, int, int, int]:
    value = path.stat()
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_mode, value.st_uid, value.st_gid,
    )


def close_check(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":closure")


def jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"{path.name}:newline:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw,
                 f"{path.name}:canonical:{ordinal}")
            close_check(row, f"{path.name}:{ordinal}")
            yield row


def document_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        marker = '"rows":['
        buffer = ""
        while marker not in buffer:
            piece = stream.read(1 << 20)
            need(bool(piece), path.name + ":rows marker")
            buffer += piece
            if len(buffer) > (6 << 20):
                buffer = buffer[-(3 << 20):]
        buffer = buffer.split(marker, 1)[1]
        decoder = json.JSONDecoder()
        ordinal = 0
        while True:
            buffer = buffer.lstrip()
            if not buffer:
                piece = stream.read(1 << 20)
                need(bool(piece), path.name + ":EOF")
                buffer = piece
                continue
            if buffer[0] == ",":
                buffer = buffer[1:]
                continue
            if buffer[0] == "]":
                return
            try:
                row, end = decoder.raw_decode(buffer)
            except json.JSONDecodeError:
                piece = stream.read(1 << 20)
                need(bool(piece), path.name + ":malformed")
                buffer += piece
                continue
            need(type(row) is dict, path.name + ":row object")
            close_check(row, f"{path.name}:{ordinal}")
            yield row
            ordinal += 1
            buffer = buffer[end:]


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    need("row_sha256" not in row, "fresh row")
    row["row_sha256"] = digest(row)
    return row


def qbox(values: Iterable[str]) -> tuple[Fraction, ...]:
    result = tuple(Fraction(value) for value in values)
    need(len(result) == 6 and all(result[2*i] < result[2*i+1] for i in range(3)),
         "positive box")
    return result


def qtext(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def box_text(values: tuple[Fraction, ...]) -> list[str]:
    return [qtext(value) for value in values]


def box_contains(outer: tuple[Fraction, ...], inner: tuple[Fraction, ...]) -> bool:
    return all(
        outer[2*axis] <= inner[2*axis]
        and inner[2*axis+1] <= outer[2*axis+1]
        for axis in range(3)
    )


def exact_interval_box_from_ast(ast: Any) -> tuple[Fraction, ...] | None:
    """Find the unique explicit (t,p,s) interval conjunct in a support AST."""
    found: list[tuple[Fraction, ...]] = []

    def visit(node: Any) -> None:
        if type(node) is dict:
            args = node.get("args")
            if node.get("op") == "AND" and type(args) is list:
                intervals = {
                    item.get("coordinate"): item
                    for item in args if type(item) is dict
                    and item.get("op") in {"OPEN_INTERVAL", "CLOSED_INTERVAL"}
                    and item.get("coordinate") in {"t", "p", "s"}
                }
                if set(intervals) == {"t", "p", "s"}:
                    found.append(tuple(
                        Fraction(intervals[coordinate][bound])
                        for coordinate in ("t", "p", "s")
                        for bound in ("lower", "upper")
                    ))
            for value in node.values():
                visit(value)
        elif type(node) is list:
            for value in node:
                visit(value)

    visit(ast)
    unique = list(dict.fromkeys(found))
    need(len(unique) <= 1, "support AST unique explicit tps interval box")
    return unique[0] if unique else None


def strict_predicate_from_ast(ast: Any) -> dict[str, Any]:
    found: list[dict[str, Any]] = []

    def visit(node: Any) -> None:
        if type(node) is dict:
            if node.get("op") in {"LT", "GT"}:
                found.append(node)
            else:
                for value in node.values():
                    visit(value)
        elif type(node) is list:
            for value in node:
                visit(value)

    visit(ast)
    need(len(found) == 1, "support AST unique strict predicate")
    return found[0]


def intersection(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...] | None:
    result: list[Fraction] = []
    for axis in range(3):
        lower = max(left[2*axis], right[2*axis])
        upper = min(left[2*axis+1], right[2*axis+1])
        if lower >= upper:
            return None
        result.extend((lower, upper))
    return tuple(result)


def transformed_intersection(
    sign: int,
    cell: tuple[Fraction, ...],
    carrier: tuple[Fraction, ...],
) -> tuple[Fraction, ...] | None:
    need(sign in {-1, 1}, "physical t sign")
    p0, p1 = max(cell[2], carrier[2]), min(cell[3], carrier[3])
    s0, s1 = max(cell[4], carrier[4]), min(cell[5], carrier[5])
    if p0 >= p1 or s0 >= s1:
        return None
    if sign == 1:
        if carrier[1] <= 0:
            return None
        lower, upper = max(carrier[0], Fraction(0)) ** 2, carrier[1] ** 2
    else:
        if carrier[0] >= 0:
            return None
        lower, upper = min(carrier[1], Fraction(0)) ** 2, carrier[0] ** 2
    t0, t1 = max(cell[0], lower), min(cell[1], upper)
    if t0 >= t1:
        return None
    return (t0, t1, p0, p1, s0, s1)


@dataclass(frozen=True, slots=True)
class Atom:
    atom_id: str
    member_id: str
    component_id: str
    kernel: str
    semantic: str
    source: str
    row_sha256: str
    signature_sha256: str
    official_key_id: str
    chart: str
    box: tuple[Fraction, ...]
    coordinate_kind: str
    physical_t_sign: int | None
    is_current_new: bool


@dataclass(slots=True)
class IntervalNode:
    center: Fraction
    crossing_lower: list[Atom]
    crossing_upper_desc: list[Atom]
    left: "IntervalNode | None"
    right: "IntervalNode | None"
    axis: int


def build_tree(rows: list[Atom], axis: int) -> IntervalNode | None:
    if not rows:
        return None
    centers = sorted((row.box[2*axis] + row.box[2*axis+1]) / 2 for row in rows)
    center = centers[len(centers)//2]
    left: list[Atom] = []
    right: list[Atom] = []
    crossing: list[Atom] = []
    for row in rows:
        if row.box[2*axis+1] <= center:
            left.append(row)
        elif row.box[2*axis] >= center:
            right.append(row)
        else:
            crossing.append(row)
    need(bool(crossing), "interval pivot")
    return IntervalNode(
        center,
        sorted(crossing, key=lambda row: (row.box[2*axis], row.atom_id)),
        sorted(crossing, key=lambda row: (row.box[2*axis+1], row.atom_id), reverse=True),
        build_tree(left, axis), build_tree(right, axis), axis,
    )


def query_tree(node: IntervalNode | None, lower: Fraction, upper: Fraction) -> Iterator[Atom]:
    if node is None:
        return
    axis = node.axis
    if upper <= node.center:
        for row in node.crossing_lower:
            if row.box[2*axis] >= upper:
                break
            yield row
        yield from query_tree(node.left, lower, upper)
    elif lower >= node.center:
        for row in node.crossing_upper_desc:
            if row.box[2*axis+1] <= lower:
                break
            yield row
        yield from query_tree(node.right, lower, upper)
    else:
        yield from node.crossing_lower
        yield from query_tree(node.left, lower, upper)
        yield from query_tree(node.right, lower, upper)


def unordered(left: str, right: str) -> tuple[str, str]:
    return (left, right) if left < right else (right, left)


def write_rows(path: Path, rows: Iterable[dict[str, Any]]) -> tuple[str, str, int]:
    state = hashlib.sha256()
    count = 0
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as stream:
            for row in rows:
                payload = canonical(row)
                state.update(payload)
                stream.write(payload + b"\n")
                count += 1
    return file_hash(path), state.hexdigest(), count


def result_object(name: str) -> dict[str, Any]:
    value = json.loads((ROOT / name).read_bytes())
    need(type(value) is dict and canonical(value) + b"\n" == (ROOT / name).read_bytes(),
         name + ":canonical")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == digest(body), name + ":closure")
    return value


def certificate_result(name: str) -> dict[str, Any]:
    document = json.loads((ROOT / name).read_bytes())
    need(
        type(document) is dict
        and set(document) == {"schema", "result", "result_sha256"}
        and document["result_sha256"] == digest(document["result"]),
        name + ":certificate closure",
    )
    return document["result"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--crosswalk", required=True)
    parser.add_argument("--crosswalk-sha256", required=True)
    parser.add_argument("--identity-result", required=True)
    parser.add_argument("--identity-result-sha256", required=True)
    parser.add_argument("--scratch-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=False)
    scratch = Path(args.scratch_dir)
    scratch.mkdir(parents=True, exist_ok=False)
    crosswalk_path = Path(args.crosswalk)
    identity_result_path = Path(args.identity_result)
    crosswalk_pre_stat = stat_fingerprint(crosswalk_path)
    identity_pre_stat = stat_fingerprint(identity_result_path)
    need(file_hash(crosswalk_path) == args.crosswalk_sha256, "crosswalk pin")
    need(file_hash(identity_result_path) == args.identity_result_sha256, "identity result file pin")
    for name, expected in PINS.items():
        need(file_hash(ROOT / name) == expected, "input pin:" + name)

    identity_raw = identity_result_path.read_bytes()
    identity_result = json.loads(identity_raw)
    need(canonical(identity_result) + b"\n" == identity_raw, "identity result canonical")
    identity_body = dict(identity_result)
    identity_claimed = identity_body.pop("result_sha256", None)
    need(identity_claimed == digest(identity_body), "identity result closure")
    need(
        identity_result["R300C_withheld_disposition"]["wall_sheet_unresolved_identity_count"] == 0
        and identity_result["R300C_withheld_disposition"]["inherited_2D_count"] == 264
        and identity_result["current_C19_external_crosswalk"]["identity_chart_signature_gap"] == 0,
        "v3 identity predecessor",
    )
    predecessor_crosswalk = identity_result["current_C19_external_crosswalk"]
    need(
        predecessor_crosswalk["ledger_filename"] == crosswalk_path.name
        and predecessor_crosswalk["ledger_file_sha256"] == args.crosswalk_sha256,
        "identity result exact crosswalk file binding",
    )
    signed_result = result_object(SIGNED_RESULT)
    complete_result = result_object(COMPLETE_RESULT)
    need(signed_result["status"] == "PASS_ZERO_CREDIT__ALL_43092_SIGNED_FACE_CONTACTS_CLASSIFIED",
         "signed result")
    need(complete_result["status"] == "PASS_FORMAL_FULL_FACE_INVENTORY_CLOSED__10416_CANONICAL_NOVEL_COMPONENT_EDGES__ZERO_DSU_RANK_CREDIT",
         "complete result")

    r235_result = certificate_result(R235)
    r235_chart = {
        row["endpoint_graph_partition_row_id"]: row["source_chart"]
        for row in r235_result["single_endpoint_graph_partition_rows"]
    }
    need(len(r235_chart) == 38_328, "R235 graph/chart census")
    del r235_result

    r242_result = certificate_result(R242)
    r242_rows = r242_result["formal_positive_2D_transition_sheet_patch_ledger"]["rows"]
    r242_chart_box = {
        row["transition_sheet_patch_row_id"]: (
            row["source_chart"], qbox(row["closed_witness_box"]), row["row_sha256"]
        ) for row in r242_rows
    }
    need(len(r242_chart_box) == 264, "R242 graph/chart census")
    del r242_result, r242_rows

    r236_result = certificate_result(R236)
    r236_chart = {
        row["double_endpoint_partition_row_id"]: (
            row["same_sign_event_absent_signature"]["source_chart"],
            row["same_sign_event_absent_signature"]["target_chart"],
        )
        for row in r236_result["double_endpoint_partition_rows"]
    }
    need(
        len(r236_chart) == 16
        and all(source != target for source, target in r236_chart.values()),
        "R236 double-endpoint source/target chart census",
    )
    del r236_result

    c4_by_bridge: dict[int, dict[str, Any]] = {}
    c4_source_ordinals: set[int] = set()
    c4_target_ordinals: set[int] = set()
    for ordinal, row in enumerate(jsonl(ROOT / C4)):
        need(row["bridge_ordinal"] == ordinal, "C4 ordinal")
        commitment = row["canonical_input_commitment"]
        source_graph_row = commitment["B1G0_source_graph_row"]
        target_graph_row = commitment["B1G0_target_graph_row"]
        r236_id = row["canonical_input_commitment"]["R236_double_endpoint_partition_row"][1]
        need(
            r236_id in r236_chart
            and source_graph_row[0] not in c4_source_ordinals
            and target_graph_row[0] not in c4_target_ordinals
            and source_graph_row[0] != target_graph_row[0]
            and row["G2_orphan_graph_disposition"]["C3_orphan_target_graph_inventory_row_id"]
                == target_graph_row[1],
            "C4/R236 double-endpoint source/target closure",
        )
        c4_source_ordinals.add(source_graph_row[0])
        c4_target_ordinals.add(target_graph_row[0])
        c4_by_bridge[ordinal] = {
            "bridge_row_id": row["bridge_row_id"],
            "full_row_sha256": digest(row),
            "source_chart": r236_chart[r236_id][0],
            "source_graph_row": source_graph_row,
            "target_chart": r236_chart[r236_id][1],
            "target_graph_row": target_graph_row,
        }
    need(
        len(c4_by_bridge) == 16
        and len(c4_source_ordinals) == len(c4_target_ordinals) == 16
        and c4_source_ordinals.isdisjoint(c4_target_ordinals),
        "C4 exact 16-source/16-target double-endpoint partition",
    )

    c5_graphs: dict[str, dict[str, Any]] = {}
    c5_classes: Counter[str] = Counter()
    c5_all_rows = 0
    c5_inventory_ordinals: set[int] = set()
    for ordinal, row in enumerate(jsonl(ROOT / C5)):
        inventory_ordinal = row["graph_inventory_ordinal"]
        need(
            type(inventory_ordinal) is int
            and inventory_ordinal not in c5_inventory_ordinals,
            "C5 unique inventory ordinal",
        )
        c5_inventory_ordinals.add(inventory_ordinal)
        c5_all_rows += 1
        graph_id = row["graph_id"]
        semantic = row["semantic_classification"]
        if semantic["classification"] != "POSITIVE_GRAPH":
            continue
        need(graph_id not in c5_graphs, "C5 unique positive graph")
        positive_chart = None
        if semantic["kernel"] == "SEALED_C4_R235D_SOURCE_EXACT_FACE_GRAPH_BRIDGE":
            commitment = row["canonical_input_commitment"]
            bridge_ref = commitment["C4_bridge_row"]
            need(
                type(bridge_ref) is list and len(bridge_ref) == 3
                and bridge_ref[0] in c4_by_bridge,
                "C5/C4 source bridge ref",
            )
            c4 = c4_by_bridge[bridge_ref[0]]
            need(
                bridge_ref == [
                    bridge_ref[0], c4["bridge_row_id"], c4["full_row_sha256"]
                ]
                and commitment["B1G0_graph_row"] == c4["source_graph_row"]
                and inventory_ordinal == c4["source_graph_row"][0],
                "C5 positive R235D graph is exact C4 source endpoint",
            )
            positive_chart = c4["source_chart"]
        c5_graphs[graph_id] = {
            "chart": positive_chart,
            "graph_inventory_ordinal": inventory_ordinal,
            "row_id": row["semantic_row_id"],
            "row_sha256": row["row_sha256"],
        }
        c5_classes[semantic["kernel"]] += 1
    need(
        c5_all_rows == 38_608 and len(c5_graphs) == 5_264
        and min(c5_inventory_ordinals) == 0
        and max(c5_inventory_ordinals) == 38_623
        and set(range(38_624)) - c5_inventory_ordinals == c4_target_ordinals
        and c4_source_ordinals <= c5_inventory_ordinals,
        "C5 pinned sparse graph-inventory ordinal cover",
    )

    c10_graphs: dict[str, dict[str, Any]] = {}
    c10_classes: Counter[str] = Counter()
    c10_graph_ordinals: set[int] = set()
    previous_c10_graph_ordinal = -1
    for ordinal, row in enumerate(jsonl(ROOT / C10)):
        graph_ordinal = row["graph_ordinal"]
        need(
            type(graph_ordinal) is int
            and graph_ordinal > previous_c10_graph_ordinal
            and graph_ordinal not in c10_graph_ordinals,
            "C10 strictly increasing unique sparse graph ordinal",
        )
        previous_c10_graph_ordinal = graph_ordinal
        c10_graph_ordinals.add(graph_ordinal)
        graph_id = row["graph_id"]
        need(graph_id in c5_graphs and graph_id not in c10_graphs, "C10/C5 graph join")
        c5 = c5_graphs[graph_id]
        c5_ref = row["C5_semantic_ref"]
        carrier = exact_interval_box_from_ast(row["carrier_domain_ast"])
        graph_class = row["graph_class"]
        if graph_class in {
            "R235_TARGET_POSITIVE_PARTIAL_BASE", "R235_SOURCE_EXACT_FACE_FULL_BASE"
        }:
            chart = r235_chart.get(graph_id)
        elif graph_class == "R242_UNIQUE_GRAPH_FULL_PATCH":
            chart = r242_chart_box.get(graph_id, (None, None, None))[0]
            need(r242_chart_box[graph_id][1] == carrier, "R242/C10 carrier equality")
        else:
            need(graph_class == "R235D_SOURCE_EXACT_FACE_FULL_BASE", "known C10 graph class")
            chart = c5["chart"]
        need(
            chart in {"G:N", "G:S", "G:E", "G:W"}
            and graph_ordinal == c5["graph_inventory_ordinal"]
            and c5_ref == {"row_id": c5["row_id"], "row_sha256": c5["row_sha256"]}
            and row["exact_support_ast"] == {
                "op": "AND",
                "args": [row["carrier_domain_ast"], row["base_domain_ast"], row["equation_ast"]],
            },
            "C10 exact carrier/support/C5 binding",
        )
        c10_graphs[graph_id] = {
            "carrier_box": carrier,
            "chart": chart,
            "graph_class": graph_class,
            "row_sha256": row["row_sha256"],
        }
        c10_classes[graph_class] += 1
    need(c10_classes == {
        "R235_TARGET_POSITIVE_PARTIAL_BASE": 4_432,
        "R235_SOURCE_EXACT_FACE_FULL_BASE": 552,
        "R235D_SOURCE_EXACT_FACE_FULL_BASE": 16,
        "R242_UNIQUE_GRAPH_FULL_PATCH": 264,
    }, "C10 graph class census")
    need(
        set(c10_graphs) == set(c5_graphs)
        and c10_graph_ordinals
            == {row["graph_inventory_ordinal"] for row in c5_graphs.values()},
        "C5/C10 exact positive graph and sparse-ordinal totality",
    )

    c15: dict[str, tuple[str, str, str]] = {}
    for ordinal, row in enumerate(jsonl(ROOT / C15)):
        need(row["member_ordinal"] == ordinal, "C15 ordinal")
        c15[row["registry_member_id"]] = (
            row["fresh_component_id"], row["official_key_id"], row["row_sha256"]
        )
    need(len(c15) == 502_204, "C15 census")
    c25: dict[str, tuple[str, str, str, str]] = {}
    for ordinal, row in enumerate(jsonl(ROOT / C25)):
        need(row["member_ordinal"] == ordinal, "C25 ordinal")
        member = row["member_id"]
        need(member in c15, "C25 join")
        c25[member] = (
            row["source_bindings"]["support_kernel"],
            row["support_semantic_kind"],
            row["normalized_support_ast_sha256"],
            row["source_bindings"]["support_kernel_row_sha256"],
        )
    need(len(c25) == 502_204, "C25 census")
    c24a: dict[str, tuple[dict[str, Any], tuple[Fraction, ...] | None]] = {}
    c24_family_census: Counter[str] = Counter()
    c24_support_kind_census: Counter[str] = Counter()
    c24_authority_role_census: Counter[str] = Counter()
    for ordinal, row in enumerate(jsonl(ROOT / C24A)):
        need(row["ordinal"] == ordinal, "C24A ordinal")
        member = row["member_id"]
        graph_id = row["graph_id"]
        family = row["coarse_family"]
        theorem = row["semantic_theorem_ast"]
        support_kind = theorem["support_kind"]
        envelope = exact_interval_box_from_ast(row["normalized_support_ast"])
        need(
            member in c15 and member in c25 and c25[member][0] == "C24A"
            and graph_id in c10_graphs
            and c25[member][2] == row["normalized_support_ast_sha256"]
            and c25[member][3] == row["row_sha256"],
            "C24A exact C25 binding",
        )
        need(
            theorem["exact_source_support_equals_member_normalized_support"] is True
            and theorem["canonical_endpoint_representation_set_equals_member_normalized_support"] is True,
            "C24A sealed support equality",
        )
        if family == "G2A":
            need(envelope is None and support_kind in {
                "G2A_EXISTING_EXACT_BASE_SHEET", "G2A_NEW_EXACT_PARTIAL_BASE_SHEET"
            }, "C24A G2A relative-2D support")
        else:
            strict_predicate = strict_predicate_from_ast(row["normalized_support_ast"])
            need(
                family == "G2B" and envelope is not None
                and support_kind in {
                    "G2B_EXACT_STRICT_SIGN_SIDE_STRATUM", "G2B_EXACT_R242_SIDE_CARRIER"
                }
                and row["normalized_support_ast"]["op"] == "AND"
                and strict_predicate["op"] in {"LT", "GT"},
                "C24A G2B envelope plus strict nonlinear predicate",
            )
            need(
                box_contains(c10_graphs[graph_id]["carrier_box"], envelope),
                "C24A G2B envelope inside C10 carrier",
            )
        c24a[member] = (row, envelope)
        c24_family_census[family] += 1
        c24_support_kind_census[support_kind] += 1
        c24_authority_role_census[
            theorem["sealed_exact_support_authority"]["role"]
        ] += 1
    need(len(c24a) == 15_224, "C24A census")
    need(c24_family_census == {"G2A": 5_264, "G2B": 9_960}, "C24A family census")
    need(c24_support_kind_census == {
        "G2A_EXISTING_EXACT_BASE_SHEET": 832,
        "G2A_NEW_EXACT_PARTIAL_BASE_SHEET": 4_432,
        "G2B_EXACT_R242_SIDE_CARRIER": 528,
        "G2B_EXACT_STRICT_SIGN_SIDE_STRATUM": 9_432,
    }, "C24A support-kind census")

    refined_key: dict[str, tuple[str, int]] = {}
    for row in document_rows(ROOT / R299A):
        refined_key[row["registry_occurrence_id"]] = (
            row["official_key_id"], row["official_key_ordinal"]
        )
    need(len(refined_key) == 9_404, "R299A census")

    identity: dict[str, dict[str, Any]] = {}
    identity_kinds: Counter[str] = Counter()
    new_members: set[str] = set()
    preserved_members: set[str] = set()
    for row in document_rows(ROOT / R294):
        member = row["registry_occurrence_id"]
        need(member not in identity and member in c15, "R294 current unique join")
        kind = row["registry_entry_kind"]
        key = row["official_key_id"]
        ordinal = row["official_key_ordinal"]
        if kind == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT":
            need(key is None and ordinal is None and member in refined_key, "R292 refined key")
            key, ordinal = refined_key[member]
        need(key == c15[member][1], "R294/C15 exact key")
        identity[member] = {
            "signature": row["complete_10_field_return_signature_sha256"],
            "key": key,
            "key_ordinal": ordinal,
            "chart": row["physical_support_chart"],
            "kind": kind,
            "row_sha256": row["row_sha256"],
        }
        identity_kinds[kind] += 1
        if kind == "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE":
            preserved_members.add(member)
        else:
            new_members.add(member)
    need(identity_kinds == {
        "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
        "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
        "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT": 9_404,
    }, "R294 kind census")
    need(len(identity) == 431_208 and len(new_members) == 304_740, "R294 census")

    groups: dict[str, dict[str, list[Atom]]] = defaultdict(
        lambda: {"physical": [], "t2": [], "targets": []}
    )
    source_census: Counter[str] = Counter()
    current_owner_sets: dict[str, set[str]] = defaultdict(set)
    current_new_atoms: dict[str, list[Atom]] = defaultdict(list)

    crosswalk_rows_state = hashlib.sha256()
    crosswalk_count = 0
    for row in jsonl(crosswalk_path):
        crosswalk_rows_state.update(canonical(row))
        crosswalk_count += 1
        member = row["member_id"]
        need(member in c15 and member in c25, "C19 current join")
        source = row["current_C19_source"]
        need(c25[member][0] == source and c15[member][0] == row["current_C15_component_id"],
             "C19 C15/C25 binding")
        need(c15[member][1] == row["official_key_id"], "C19 key")
        atom = Atom(
            source + ":" + row["current_C19_support_row_sha256"], member,
            c15[member][0], c25[member][0], c25[member][1], source,
            row["current_C19_support_row_sha256"],
            row["complete_10_field_return_signature_sha256"],
            row["official_key_id"], row["source_chart"],
            qbox(row["support_bounds_t_p_s"]), "PHYSICAL_T_P_S", None, False,
        )
        groups[atom.chart]["physical"].append(atom)
        source_census[source] += 1
        current_owner_sets[source].add(member)
    need(
        crosswalk_count == predecessor_crosswalk["row_count"] == 51_172
        and crosswalk_rows_state.hexdigest()
        == predecessor_crosswalk["ledger_rows_sha256"],
        "identity result exact crosswalk row-sequence binding",
    )

    for source, filename, expected, is_new, coordinate_kind in (
        ("C20A", C20A, 126_468, False, "PHYSICAL_T_P_S"),
        ("C22A", C22A, 295_340, True, "PHYSICAL_T_P_S"),
        ("C23A", C23A, 10_252, True, "T_SQUARED_P_S"),
    ):
        for ordinal, row in enumerate(jsonl(ROOT / filename)):
            need(row["ordinal"] == ordinal, source + ":ordinal")
            member = row.get("member_id", row.get("owner_member_id"))
            component = row.get("fresh_component_id", row.get("owner_fresh_component_id"))
            need(member in identity and member in c15 and member in c25, source + ":join")
            expected_kernel = {"C20A": "C20A", "C22A": "C22B", "C23A": "C23B"}[source]
            need(c25[member][0] == expected_kernel and c15[member][0] == component,
                 source + ":current binding")
            support = row["support_ast"]
            item = identity[member]
            chart = support.get("coordinate_chart", support.get("recharted_target_chart"))
            need(chart == item["chart"], source + ":R294 chart")
            sign = support.get("physical_t_sign")
            if source == "C23A":
                need(sign in {-1, 1}, "C23 sign")
            else:
                need(sign is None, source + ":physical coordinates")
            atom = Atom(
                source + ":" + row["row_sha256"], member, component,
                c25[member][0], c25[member][1], source, row["row_sha256"],
                item["signature"], item["key"], chart, qbox(support["bounds"]),
                coordinate_kind, sign, is_new,
            )
            if is_new:
                groups[atom.chart]["targets"].append(atom)
                current_new_atoms[member].append(atom)
            source_census[source] += 1
            current_owner_sets[source].add(member)
        need(source_census[source] == expected, source + ":census")

    need(source_census == {
        "C19A": 5_596, "C19B": 12_232, "C19C": 33_344,
        "C20A": 126_468, "C22A": 295_340, "C23A": 10_252,
    }, "six kernel atom census")
    need(current_owner_sets["C20A"] == preserved_members, "C20 preserved owner set")
    need(current_owner_sets["C22A"] | current_owner_sets["C23A"] == new_members,
         "new owner union")
    need(len(set().union(*current_owner_sets.values())) == 482_380, "six kernel owner census")
    c19_members = (
        current_owner_sets["C19A"]
        | current_owner_sets["C19B"]
        | current_owner_sets["C19C"]
    )
    need(len(c19_members) == 51_172, "current C19 carrier owner census")

    explicit_pairs: set[tuple[str, str]] = set()
    explicit_incident: set[str] = set()
    explicit_by_occurrence: dict[str, set[str]] = defaultdict(set)
    explicit_witness: dict[tuple[str, str], dict[str, Any]] = {}
    for row in document_rows(ROOT / R300C):
        occurrence_id = row["Round294_registry_occurrence_id"]
        virtual_id = row["virtual_stratum_node_id"]
        pair = unordered(virtual_id, occurrence_id)
        need(pair not in explicit_witness, "R300C unique primitive pair witness")
        explicit_witness[pair] = row
        explicit_pairs.add(pair)
        explicit_incident.add(occurrence_id)
        explicit_by_occurrence[occurrence_id].add(virtual_id)
    need(len(explicit_pairs) == 6_322 and len(explicit_incident) == 6_314,
         "R300C explicit census")
    explicit_multiplicity = Counter(len(values) for values in explicit_by_occurrence.values())
    need(explicit_multiplicity == {1: 6_306, 2: 8}, "R300C 6322-vs-6314 reconciliation")

    database_path = scratch / "pair_universe.sqlite"
    db = sqlite3.connect(database_path)
    db.execute("PRAGMA journal_mode=OFF")
    db.execute("PRAGMA synchronous=OFF")
    db.execute("PRAGMA temp_store=MEMORY")
    db.execute("PRAGMA locking_mode=EXCLUSIVE")
    db.execute("""
        CREATE TABLE pairs(
          left_id TEXT NOT NULL,
          right_id TEXT NOT NULL,
          left_component TEXT NOT NULL,
          right_component TEXT NOT NULL,
          left_kernel TEXT NOT NULL,
          right_kernel TEXT NOT NULL,
          representative_left_atom TEXT NOT NULL,
          representative_right_atom TEXT NOT NULL,
          representative_left_source TEXT NOT NULL,
          representative_right_source TEXT NOT NULL,
          source_pair TEXT NOT NULL,
          intersection_coordinate_system TEXT NOT NULL,
          exact_positive_intersection_box_json TEXT NOT NULL,
          atom_overlap_witness_count INTEGER NOT NULL,
          R300C_explicit_pair INTEGER NOT NULL,
          same_complete_signature INTEGER NOT NULL,
          same_official_key INTEGER NOT NULL,
          PRIMARY KEY(left_id,right_id)
        ) WITHOUT ROWID
    """)
    db.execute("""
        CREATE TABLE c24_envelope_pairs(
          left_id TEXT NOT NULL,
          right_id TEXT NOT NULL,
          c24_member_id TEXT NOT NULL,
          target_member_id TEXT NOT NULL,
          c24_component TEXT NOT NULL,
          target_component TEXT NOT NULL,
          c24_graph_id TEXT NOT NULL,
          c24_support_kind TEXT NOT NULL,
          c24_predicate_op TEXT NOT NULL,
          c24_row_sha256 TEXT NOT NULL,
          target_atom_id TEXT NOT NULL,
          target_source TEXT NOT NULL,
          target_row_sha256 TEXT NOT NULL,
          physical_chart TEXT NOT NULL,
          intersection_coordinate_system TEXT NOT NULL,
          exact_envelope_intersection_box_json TEXT NOT NULL,
          atom_envelope_witness_count INTEGER NOT NULL,
          R300C_validation_pair INTEGER NOT NULL,
          PRIMARY KEY(left_id,right_id)
        ) WITHOUT ROWID
    """)
    insert_sql = """
      INSERT INTO pairs VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
      ON CONFLICT(left_id,right_id) DO UPDATE SET
        atom_overlap_witness_count=atom_overlap_witness_count+1
    """
    comparison_census: Counter[str] = Counter()
    overlap_census: Counter[str] = Counter()

    def record(target: Atom, candidate: Atom, overlap: tuple[Fraction, ...], system: str) -> None:
        if target.member_id == candidate.member_id:
            return
        if candidate.is_current_new and target.member_id > candidate.member_id:
            return
        left_id, right_id = unordered(target.member_id, candidate.member_id)
        left_atom, right_atom = (
            (target, candidate) if target.member_id < candidate.member_id
            else (candidate, target)
        )
        source_pair = "|".join(sorted((left_atom.source, right_atom.source)))
        db.execute(insert_sql, (
            left_id, right_id, left_atom.component_id, right_atom.component_id,
            left_atom.kernel, right_atom.kernel, left_atom.atom_id, right_atom.atom_id,
            left_atom.source, right_atom.source, source_pair, system,
            canonical(box_text(overlap)).decode("ascii"), 1,
            int((left_id, right_id) in explicit_pairs),
            int(left_atom.signature_sha256 == right_atom.signature_sha256),
            int(left_atom.official_key_id == right_atom.official_key_id),
        ))
        overlap_census[system] += 1

    for group_key in sorted(groups):
        group = groups[group_key]
        if not group["targets"]:
            continue
        physical = sorted(group["physical"], key=lambda row: row.atom_id)
        physical_t = build_tree(physical, 0)
        physical_p = build_tree(physical, 1)
        for target in sorted(group["targets"], key=lambda row: row.atom_id):
            if target.coordinate_kind == "PHYSICAL_T_P_S":
                for candidate in query_tree(physical_t, target.box[0], target.box[1]):
                    comparison_census["PHYSICAL_PHYSICAL"] += 1
                    overlap = intersection(target.box, candidate.box)
                    if overlap is not None:
                        record(target, candidate, overlap, "(t,p,s)")
            else:
                for candidate in query_tree(physical_p, target.box[2], target.box[3]):
                    comparison_census["T2_PHYSICAL"] += 1
                    overlap = transformed_intersection(
                        target.physical_t_sign, target.box, candidate.box
                    )
                    if overlap is not None:
                        record(target, candidate, overlap, "(t_squared,p,s)")
        db.commit()

    c24_envelopes_by_chart: dict[str, list[Atom]] = defaultdict(list)
    for member in sorted(c24a):
        row, envelope = c24a[member]
        if row["coarse_family"] != "G2B":
            continue
        need(envelope is not None, "C24A G2B envelope materialized")
        graph = c10_graphs[row["graph_id"]]
        c24_envelopes_by_chart[graph["chart"]].append(Atom(
            "C24A:" + row["row_sha256"], member, c15[member][0],
            "C24A", c25[member][1], "C24A", row["row_sha256"],
            "", row["official_key_id"], graph["chart"], envelope,
            "PHYSICAL_T_P_S", None, False,
        ))
    need(sum(map(len, c24_envelopes_by_chart.values())) == 9_960,
         "all C24A G2B envelopes chart-partitioned")

    c24_insert = """
      INSERT INTO c24_envelope_pairs VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
      ON CONFLICT(left_id,right_id) DO UPDATE SET
        atom_envelope_witness_count=atom_envelope_witness_count+1
    """
    c24_comparison_census: Counter[str] = Counter()
    c24_atom_overlap_census: Counter[str] = Counter()

    def record_c24_envelope(
        target: Atom,
        carrier: Atom,
        overlap: tuple[Fraction, ...],
        system: str,
    ) -> None:
        need(target.member_id != carrier.member_id, "C24A/target distinct members")
        left_id, right_id = unordered(target.member_id, carrier.member_id)
        row = c24a[carrier.member_id][0]
        predicate = strict_predicate_from_ast(row["normalized_support_ast"])
        db.execute(c24_insert, (
            left_id, right_id, carrier.member_id, target.member_id,
            carrier.component_id, target.component_id, row["graph_id"],
            row["semantic_theorem_ast"]["support_kind"], predicate["op"],
            carrier.row_sha256, target.atom_id, target.source,
            target.row_sha256, carrier.chart, system,
            canonical(box_text(overlap)).decode("ascii"), 1,
            int((left_id, right_id) in explicit_pairs),
        ))
        c24_atom_overlap_census[system] += 1

    for chart in sorted(c24_envelopes_by_chart):
        envelopes = sorted(c24_envelopes_by_chart[chart], key=lambda row: row.atom_id)
        envelope_t = build_tree(envelopes, 0)
        envelope_p = build_tree(envelopes, 1)
        for target in sorted(groups[chart]["targets"], key=lambda row: row.atom_id):
            if target.coordinate_kind == "PHYSICAL_T_P_S":
                for carrier in query_tree(envelope_t, target.box[0], target.box[1]):
                    c24_comparison_census["C24_ENVELOPE_PHYSICAL_TARGET"] += 1
                    overlap = intersection(target.box, carrier.box)
                    if overlap is not None:
                        record_c24_envelope(target, carrier, overlap, "(t,p,s)")
            else:
                for carrier in query_tree(envelope_p, target.box[2], target.box[3]):
                    c24_comparison_census["C24_ENVELOPE_T2_TARGET"] += 1
                    overlap = transformed_intersection(
                        target.physical_t_sign, target.box, carrier.box
                    )
                    if overlap is not None:
                        record_c24_envelope(target, carrier, overlap, "(t_squared,p,s)")
        db.commit()

    pair_count, same_component, cross_component = db.execute(
        "SELECT count(*),sum(left_component=right_component),sum(left_component<>right_component) FROM pairs"
    ).fetchone()
    pair_count = int(pair_count or 0)
    same_component = int(same_component or 0)
    cross_component = int(cross_component or 0)
    source_pair_census: dict[str, dict[str, int]] = {}
    for source_pair, total, same, cross, same_signature, same_key in db.execute(
        """
        SELECT source_pair,count(*),sum(left_component=right_component),
               sum(left_component<>right_component),sum(same_complete_signature),
               sum(same_official_key)
        FROM pairs GROUP BY source_pair ORDER BY source_pair
        """
    ):
        source_pair_census[source_pair] = {
            "distinct_member_pair_count": int(total),
            "same_current_C15_component_pair_count": int(same),
            "cross_current_C15_component_pair_count": int(cross),
            "same_complete_signature_pair_count": int(same_signature),
            "same_official_key_pair_count": int(same_key),
        }

    degrees: dict[str, list[int]] = {member: [0, 0, 0] for member in new_members}
    current_c19_neighbors: dict[str, set[str]] = defaultdict(set)
    for left, right, left_component, right_component in db.execute(
        "SELECT left_id,right_id,left_component,right_component FROM pairs ORDER BY left_id,right_id"
    ):
        same = int(left_component == right_component)
        for member in (left, right):
            if member in degrees:
                other = right if member == left else left
                current_c19_neighbors[member].add(other)
                degrees[member][0] += 1
                degrees[member][1] += same
                degrees[member][2] += 1 - same

    occurrence_census: Counter[str] = Counter()
    occurrence_rows: list[dict[str, Any]] = []
    for member in sorted(new_members):
        degree, same_degree, cross_degree = degrees[member]
        old_incident = member in explicit_incident
        current_scan_disposition = (
            "CURRENT_C19_CROSS_COMPONENT_POSITIVE_VOLUME_WITNESS"
            if cross_degree else
            "CURRENT_C19_SAME_COMPONENT_POSITIVE_VOLUME_INCIDENT"
            if degree else
            "EXACT_NO_DISTINCT_CURRENT_C19_CARRIER_POSITIVE_VOLUME_OVERLAP_IN_PHYSICAL_CHART"
        )
        if cross_degree:
            disposition = "CURRENT_C19_CROSS_COMPONENT_POSITIVE_VOLUME_WITNESS"
        elif degree:
            disposition = "CURRENT_C19_SAME_COMPONENT_POSITIVE_VOLUME_INCIDENT"
        elif old_incident:
            disposition = "R300C_EXPLICIT_POSITIVE_INCIDENT_OUTSIDE_CURRENT_C19_CARRIER_SCAN"
        else:
            disposition = current_scan_disposition
        old_class = "R300C_EXPLICIT_INCIDENT" if old_incident else "R300C_EXPLICIT_NONINCIDENT"
        final_positive_neighbors = (
            current_c19_neighbors[member] | explicit_by_occurrence.get(member, set())
        )
        occurrence_census[old_class + "|" + disposition] += 1
        occurrence_rows.append(closed({
            "current_C15_component_id": c15[member][0],
            "current_C25_support_kernel": c25[member][0],
            "current_C25_support_semantic_kind": c25[member][1],
            "current_C19_cross_component_pair_degree": cross_degree,
            "current_C19_distinct_member_positive_pair_degree": degree,
            "current_C19_same_component_pair_degree": same_degree,
            "current_C19_scan_disposition": current_scan_disposition,
            "disposition": disposition,
            "final_positive_terminal_distinct_pair_degree": len(final_positive_neighbors),
            "member_id": member,
            "R300C_explicit_incident": old_incident,
            "R300C_explicit_scope_class": old_class,
            "physical_chart_partition_complete_without_signature_or_key_prefilter": True,
        }))
    occurrence_path = out / "current_304740_new_occurrence_vs_51172_C19_carrier_disposition.jsonl.gz"
    occurrence_file, occurrence_rows_sha, occurrence_count = write_rows(
        occurrence_path, occurrence_rows
    )

    def pair_output_rows() -> Iterator[dict[str, Any]]:
        for values in db.execute("SELECT * FROM pairs ORDER BY left_id,right_id"):
            (
                left, right, left_component, right_component, left_kernel, right_kernel,
                left_atom, right_atom, left_source, right_source, source_pair,
                system, overlap_json, multiplicity, explicit,
                same_signature, same_key,
            ) = values
            yield closed({
                "R300C_explicit_pair": bool(explicit),
                "atom_overlap_witness_count": multiplicity,
                "current_C15_components": [left_component, right_component],
                "current_C25_support_kernels": [left_kernel, right_kernel],
                "exact_positive_intersection_box": json.loads(overlap_json),
                "intersection_coordinate_system": system,
                "left_member_id": left,
                "positive_volume_physical_overlap": True,
                "representative_atom_ids": [left_atom, right_atom],
                "representative_sources": [left_source, right_source],
                "source_pair": source_pair,
                "right_member_id": right,
                "same_current_C15_component": left_component == right_component,
                "same_complete_signature": bool(same_signature),
                "same_official_key": bool(same_key),
                "same_physical_chart": True,
            })
    pair_path = out / "current_new_C19_carrier_exact_positive_pair_universe.jsonl.gz"
    pair_file, pair_rows_sha, written_pair_count = write_rows(pair_path, pair_output_rows())
    need(written_pair_count == pair_count, "pair ledger count")

    c24_validation_pairs = {
        pair for pair in explicit_pairs
        if ((pair[0] in c24a and c24a[pair[0]][0]["coarse_family"] == "G2B"
             and pair[1] in new_members)
            or (pair[1] in c24a and c24a[pair[1]][0]["coarse_family"] == "G2B"
                and pair[0] in new_members))
    }
    need(len(c24_validation_pairs) == 906, "R300C exact C24A-G2B validation census")
    c24_envelope_pairs = {
        (left, right) for left, right in db.execute(
            "SELECT left_id,right_id FROM c24_envelope_pairs ORDER BY left_id,right_id"
        )
    }
    need(c24_validation_pairs <= c24_envelope_pairs,
         "every R300C C24A validation pair is independently envelope-discovered")

    def c24_envelope_output_rows() -> Iterator[dict[str, Any]]:
        for values in db.execute(
            "SELECT * FROM c24_envelope_pairs ORDER BY left_id,right_id"
        ):
            (
                left, right, c24_member, target_member, c24_component,
                target_component, graph_id, support_kind, predicate_op,
                c24_row_sha, target_atom_id, target_source, target_row_sha,
                chart, system, overlap_json, multiplicity, validation,
            ) = values
            c24_row = c24a[c24_member][0]
            predicate = strict_predicate_from_ast(c24_row["normalized_support_ast"])
            yield closed({
                "R300C_validation_pair": bool(validation),
                "c24_C15_component_id": c24_component,
                "c24_C25_support_kernel": c25[c24_member][0],
                "c24_C25_support_semantic_kind": c25[c24_member][1],
                "c24_graph_id": graph_id,
                "c24_member_id": c24_member,
                "c24_normalized_support_ast_sha256": c24_row["normalized_support_ast_sha256"],
                "c24_predicate_ast_sha256": digest(predicate),
                "c24_predicate_op": predicate_op,
                "c24_row_sha256": c24_row_sha,
                "c24_semantic_theorem_ast_sha256": c24_row["semantic_theorem_ast_sha256"],
                "c24_support_kind": support_kind,
                "candidate_status": "ENVELOPE_ONLY__EXACT_STRICT_RELATION_DISPOSITION_REQUIRED",
                "current_C15_components_equal": c24_component == target_component,
                "exact_envelope_intersection_box": json.loads(overlap_json),
                "intersection_coordinate_system": system,
                "left_member_id": left,
                "physical_chart": chart,
                "right_member_id": right,
                "target_atom_envelope_witness_count": multiplicity,
                "target_atom_id": target_atom_id,
                "target_C15_component_id": target_component,
                "target_C25_support_kernel": c25[target_member][0],
                "target_C25_support_semantic_kind": c25[target_member][1],
                "target_member_id": target_member,
                "target_row_sha256": target_row_sha,
                "target_source": target_source,
            })

    c24_envelope_path = out / "C24A_9960_G2B_interval_envelope_vs_current_target_candidates.jsonl.gz"
    c24_envelope_file, c24_envelope_rows_sha, c24_envelope_count = write_rows(
        c24_envelope_path, c24_envelope_output_rows()
    )
    need(c24_envelope_count == len(c24_envelope_pairs), "C24 envelope ledger count")

    g2a_rows: list[dict[str, Any]] = []
    for member in sorted(c24a):
        c24_row, envelope = c24a[member]
        if c24_row["coarse_family"] != "G2A":
            continue
        graph = c10_graphs[c24_row["graph_id"]]
        need(envelope is None, "G2A lacks ambient tps volume envelope")
        g2a_rows.append(closed({
            "c24_C15_component_id": c15[member][0],
            "c24_C25_support_kernel": c25[member][0],
            "c24_C25_support_semantic_kind": c25[member][1],
            "c24_graph_id": c24_row["graph_id"],
            "c24_member_id": member,
            "c24_normalized_support_ast_sha256": c24_row["normalized_support_ast_sha256"],
            "c24_row_sha256": c24_row["row_sha256"],
            "c24_semantic_theorem_ast_sha256": c24_row["semantic_theorem_ast_sha256"],
            "c24_support_kind": c24_row["semantic_theorem_ast"]["support_kind"],
            "disposition": "RELATIVE_2D_COMPLETE_OR_OTHER_DIMENSIONAL_UNIQUE_ROUTE_OPEN",
            "physical_chart": graph["chart"],
            "why_not_positive_volume": "EXACT_SUPPORT_HAS_ONLY_P_S_BASE_DOMAIN_AND_GRAPH_RELATION__NO_AMBIENT_TPS_VOLUME_BOX",
        }))
    g2a_path = out / "C24A_5264_G2A_relative_2D_open_routes.jsonl.gz"
    g2a_file, g2a_rows_sha, g2a_count = write_rows(g2a_path, g2a_rows)
    need(g2a_count == 5_264, "G2A open-route ledger count")

    c24_same, c24_cross, c24_validation = db.execute(
        "SELECT sum(c24_component=target_component),sum(c24_component<>target_component),sum(R300C_validation_pair) FROM c24_envelope_pairs"
    ).fetchone()
    c24_same = int(c24_same or 0)
    c24_cross = int(c24_cross or 0)
    c24_validation = int(c24_validation or 0)
    c24_difference = c24_envelope_pairs - c24_validation_pairs

    blocker_result: dict[str, Any] = {
        "C27_FAMILIES_imported_or_read": False,
        "CM2": "NO-GO_FOR_CLAIM",
        "edge_ledger_used_as_candidate_universe": False,
        "formal_credit": 0,
        "input_pins": {**dict(sorted(PINS.items())),
                       "v3_crosswalk": args.crosswalk_sha256,
                       "v3_identity_result": args.identity_result_sha256},
        "invocation_seed": args.seed,
        "C24A_exact_support_partition": {
            "authority_role_census": dict(sorted(c24_authority_role_census.items())),
            "family_census": dict(sorted(c24_family_census.items())),
            "support_kind_census": dict(sorted(c24_support_kind_census.items())),
            "G2A_relative_2D_route_status": "OPEN",
            "G2A_open_route_ledger_filename": g2a_path.name,
            "G2A_open_route_ledger_file_sha256": g2a_file,
            "G2A_open_route_ledger_rows_sha256": g2a_rows_sha,
            "G2B_strict_relation_route_status": "OPEN",
        },
        "C24A_G2B_interval_envelope_scan": {
            "candidate_prefilter": "PHYSICAL_CHART_ONLY",
            "complete_signature_and_official_key_used_as_candidate_prefilter": False,
            "atom_candidate_comparison_census": dict(sorted(c24_comparison_census.items())),
            "atom_envelope_overlap_census": dict(sorted(c24_atom_overlap_census.items())),
            "distinct_envelope_candidate_pair_count": c24_envelope_count,
            "same_current_C15_component_candidate_pair_count": c24_same,
            "cross_current_C15_component_candidate_pair_count": c24_cross,
            "R300C_validation_pair_count": c24_validation,
            "R300C_validation_set_is_subset_of_envelope_candidates": True,
            "envelope_candidate_minus_R300C_validation_pair_count": len(c24_difference),
            "ledger_filename": c24_envelope_path.name,
            "ledger_file_sha256": c24_envelope_file,
            "ledger_rows_sha256": c24_envelope_rows_sha,
            "outer_envelope_is_not_full_support": True,
            "exact_strict_nonlinear_predicate_disposition_closed": False,
        },
        "independent_current_C19_scan": {
            "distinct_member_positive_pair_count": pair_count,
            "same_current_C15_component_pair_count": same_component,
            "cross_current_C15_component_pair_count": cross_component,
            "source_pair_census": source_pair_census,
            "pair_ledger_filename": pair_path.name,
            "pair_ledger_file_sha256": pair_file,
            "pair_ledger_rows_sha256": pair_rows_sha,
        },
        "hard_blockers": [
            "C24A_G2B_9960_ENVELOPE_CANDIDATES_REQUIRE_EXACT_STRICT_RELATION_DISPOSITION",
            "C24A_G2A_5264_REQUIRE_RELATIVE_2D_COMPLETE_OR_OTHER_DIMENSIONAL_UNIQUE_ROUTE",
            "ROOT_INPUT_CAPTURE_IS_PATH_HASH_THEN_REOPEN_NOT_SINGLE_STABLE_FD",
            "DUAL_VERIFIER_DOUBLE_SEED_AND_COHERENT_ATTACKS_NOT_RUN",
        ],
        "C27_C28_C29": "REBUILD_REQUIRED_CROSS_COMPONENT_WITNESS__POSITIVE_TERMINAL_STILL_OPEN",
        "strict_nonpromotion": {
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
        },
        "status": "BLOCKED_ZERO_CREDIT__C24A_ENVELOPE_SCAN_MATERIALIZED__EXACT_RELATION_AND_RELATIVE_2D_ROUTES_OPEN",
    }
    semantic_blocker = dict(blocker_result)
    semantic_blocker.pop("invocation_seed")
    blocker_result["semantic_projection_sha256"] = digest(semantic_blocker)
    blocker_result["result_sha256"] = digest(blocker_result)
    need(
        stat_fingerprint(crosswalk_path) == crosswalk_pre_stat
        and stat_fingerprint(identity_result_path) == identity_pre_stat
        and file_hash(crosswalk_path) == args.crosswalk_sha256
        and file_hash(identity_result_path) == args.identity_result_sha256,
        "predecessor bundle post-read TOCTOU",
    )
    (out / "result.json").write_bytes(canonical(blocker_result) + b"\n")
    db.close()
    return 0

    signed_pairs: set[tuple[str, str]] = set()
    signed_rows = signed_self = 0
    signed_decisions: Counter[str] = Counter()
    for row in document_rows(ROOT / SIGNED):
        signed_rows += 1
        signed_decisions[row["decision"]] += 1
        if row["decision"].startswith("ACCEPT_"):
            left, right = row["left_formal_occurrence_id"], row["right_formal_occurrence_id"]
            if left == right:
                signed_self += 1
            else:
                signed_pairs.add(unordered(left, right))
    need(signed_rows == 43_092 and signed_self == 2_092 and len(signed_pairs) == 25_452,
         "signed expansion")

    complete_pairs: set[tuple[str, str]] = set()
    complete_rows = complete_self = complete_raw_nonself = 0
    for row in document_rows(ROOT / COMPLETE):
        complete_rows += 1
        if row["decision"].startswith("ACCEPT_"):
            for left in row["left_formal_occurrence_endpoints"]:
                for right in row["right_formal_occurrence_endpoints"]:
                    if left == right:
                        complete_self += 1
                    else:
                        complete_raw_nonself += 1
                        complete_pairs.add(unordered(left, right))
    need(
        complete_rows == 62_548 and complete_self == 15_056
        and complete_raw_nonself == 91_760 and len(complete_pairs) == 36_140
        and signed_pairs <= complete_pairs,
        "complete expansion",
    )

    positive_pairs = {
        (left, right) for left, right in db.execute(
            "SELECT left_id,right_id FROM pairs ORDER BY left_id,right_id"
        )
    }
    multi_rows: list[dict[str, Any]] = []
    for occurrence_id in sorted(explicit_by_occurrence):
        virtual_ids = sorted(explicit_by_occurrence[occurrence_id])
        if len(virtual_ids) == 1:
            continue
        pair_ids = [unordered(occurrence_id, virtual_id) for virtual_id in virtual_ids]
        multi_rows.append(closed({
            "current_full_support_reproduced_pair_count": sum(
                pair in positive_pairs for pair in pair_ids
            ),
            "explicit_distinct_pair_count": len(pair_ids),
            "explicit_pair_member_ids": [list(pair) for pair in pair_ids],
            "occurrence_id": occurrence_id,
            "reason_6322_pairs_exceed_6314_occurrences": (
                "ONE_OCCURRENCE_HAS_TWO_DISTINCT_VIRTUAL_MEMBER_PAIRS"
            ),
            "virtual_member_ids": virtual_ids,
        }))
    need(len(multi_rows) == 8, "R300C eight multi-pair occurrences")
    multi_path = out / "R300C_6322_pairs_6314_occurrences_eight_multi_pair_reconciliation.jsonl.gz"
    multi_file, multi_rows_sha, multi_count = write_rows(multi_path, multi_rows)
    need(multi_count == 8, "multi-pair ledger count")

    explicit_c19_pairs = {
        pair for pair in explicit_pairs
        if ((pair[0] in c19_members and pair[1] in new_members)
            or (pair[1] in c19_members and pair[0] in new_members))
    }
    need(explicit_c19_pairs <= positive_pairs, "all explicit current-C19 pairs reproduced")
    outside_c19_rows: list[dict[str, Any]] = []
    outside_kernel_census: Counter[str] = Counter()
    outside_occurrences: set[str] = set()
    for left, right in sorted(explicit_pairs - explicit_c19_pairs):
        if left in new_members:
            occurrence_id, virtual_id = left, right
        else:
            occurrence_id, virtual_id = right, left
        need(occurrence_id in new_members and virtual_id in c15 and virtual_id in c25,
             "R300C outside-C19 current endpoints")
        kernel = c25[virtual_id][0]
        outside_kernel_census[kernel] += 1
        outside_occurrences.add(occurrence_id)
        outside_c19_rows.append(closed({
            "current_virtual_C15_component_id": c15[virtual_id][0],
            "current_virtual_C25_support_kernel": kernel,
            "current_virtual_C25_support_semantic_kind": c25[virtual_id][1],
            "disposition": "R300C_EXPLICIT_PAIR_ENDPOINT_IS_OUTSIDE_CURRENT_C19A_B_C_CARRIER_SCOPE",
            "occurrence_id": occurrence_id,
            "pair_member_ids": [left, right],
            "virtual_member_id": virtual_id,
        }))
    outside_path = out / "R300C_explicit_pairs_outside_current_C19_carrier_scope.jsonl.gz"
    outside_file, outside_rows_sha, outside_count = write_rows(outside_path, outside_c19_rows)
    candidate_universe = complete_pairs | positive_pairs
    assignment_census: Counter[str] = Counter()
    priority_rows: list[dict[str, Any]] = []
    for left, right in sorted(candidate_universe):
        terminal = (
            "SIGNED_BOUNDARY_FACES" if (left, right) in signed_pairs else
            "COMPLETE_BOUNDARY_FACES" if (left, right) in complete_pairs else
            "POSITIVE_VOLUME_CARRIERS"
        )
        need(left in c15 and right in c15 and left in c25 and right in c25,
             "priority current endpoint")
        assignment_census[terminal] += 1
        priority_rows.append(closed({
            "assigned_terminal": terminal,
            "current_C15_components": [c15[left][0], c15[right][0]],
            "current_C25_support_kernels": [c25[left][0], c25[right][0]],
            "left_member_id": left,
            "pair_assignment_rule": "FIRST_MATCH_SIGNED_THEN_COMPLETE_THEN_POSITIVE",
            "raw_complete_face_evidence": (left, right) in complete_pairs,
            "raw_current_full_support_positive_volume_evidence": (left, right) in positive_pairs,
            "raw_signed_face_evidence": (left, right) in signed_pairs,
            "right_member_id": right,
            "same_current_C15_component": c15[left][0] == c15[right][0],
        }))
    priority_path = out / "current_total_candidate_universe_unique_priority_routes.jsonl.gz"
    priority_file, priority_rows_sha, priority_count = write_rows(priority_path, priority_rows)
    need(priority_count == len(candidate_universe), "priority count")

    explicit_current_endpoint_pairs = {
        pair for pair in explicit_pairs if pair[0] in c15 and pair[1] in c15
    }
    cross_examples = []
    for values in db.execute(
        "SELECT left_id,right_id,left_component,right_component,intersection_coordinate_system,exact_positive_intersection_box_json FROM pairs WHERE left_component<>right_component ORDER BY left_id,right_id LIMIT 32"
    ):
        cross_examples.append({
            "left_member_id": values[0], "right_member_id": values[1],
            "left_component_id": values[2], "right_component_id": values[3],
            "intersection_coordinate_system": values[4],
            "exact_positive_intersection_box": json.loads(values[5]),
        })

    result: dict[str, Any] = {
        "C27_FAMILIES_imported_or_read": False,
        "CM2": "NO-GO_FOR_CLAIM",
        "edge_ledger_used_as_candidate_universe": False,
        "formal_credit": 0,
        "input_pins": {**dict(sorted(PINS.items())),
                       "v3_crosswalk": args.crosswalk_sha256,
                       "v3_identity_result": args.identity_result_sha256},
        "invocation_seed": args.seed,
        "six_kernel_current_support": {
            "atom_census": dict(sorted(source_census.items())),
            "atom_count": sum(source_census.values()),
            "distinct_owner_count": len(set().union(*current_owner_sets.values())),
            "identity_group_count": len(groups),
            "current_new_occurrence_count": len(new_members),
        },
        "exact_current_new_full_support_scan": {
            "atom_candidate_comparison_census": dict(sorted(comparison_census.items())),
            "atom_positive_overlap_census": dict(sorted(overlap_census.items())),
            "distinct_member_positive_pair_count": pair_count,
            "same_current_C15_component_pair_count": same_component,
            "cross_current_C15_component_pair_count": cross_component,
            "source_pair_census": source_pair_census,
            "cross_component_examples": cross_examples,
            "all_304740_new_occurrences_scanned_against_all_51172_current_C19_carriers": True,
            "candidate_prefilter": "PHYSICAL_CHART_ONLY",
            "complete_signature_and_official_key_used_only_as_output_classifiers": True,
            "pair_ledger_filename": pair_path.name,
            "pair_ledger_file_sha256": pair_file,
            "pair_ledger_rows_sha256": pair_rows_sha,
            "occurrence_disposition_census": dict(sorted(occurrence_census.items())),
            "occurrence_ledger_filename": occurrence_path.name,
            "occurrence_ledger_file_sha256": occurrence_file,
            "occurrence_ledger_rows_sha256": occurrence_rows_sha,
        },
        "R300C_reconciliation": {
            "explicit_pair_count": len(explicit_pairs),
            "explicit_incident_occurrence_count": len(explicit_incident),
            "explicit_occurrence_distinct_pair_multiplicity_census": {
                str(key): value for key, value in sorted(explicit_multiplicity.items())
            },
            "eight_multi_pair_occurrence_ledger_filename": multi_path.name,
            "eight_multi_pair_occurrence_ledger_file_sha256": multi_file,
            "eight_multi_pair_occurrence_ledger_rows_sha256": multi_rows_sha,
            "explicit_pairs_with_both_current_C15_endpoints": len(explicit_current_endpoint_pairs),
            "explicit_pairs_with_current_C19_carrier_endpoint": len(explicit_c19_pairs),
            "explicit_current_C19_pairs_reproduced_by_full_support_scan": len(
                explicit_c19_pairs & positive_pairs
            ),
            "explicit_pairs_outside_current_C19_carrier_scope": outside_count,
            "outside_current_C19_scope_distinct_occurrence_count": len(outside_occurrences),
            "outside_current_C19_scope_support_kernel_census": dict(
                sorted(outside_kernel_census.items())
            ),
            "outside_current_C19_scope_ledger_filename": outside_path.name,
            "outside_current_C19_scope_ledger_file_sha256": outside_file,
            "outside_current_C19_scope_ledger_rows_sha256": outside_rows_sha,
        },
        "three_terminal_priority": {
            "raw_signed_pair_count": len(signed_pairs),
            "raw_complete_pair_count": len(complete_pairs),
            "raw_current_full_support_positive_pair_count": len(positive_pairs),
            "signed_positive_overlap_pair_count": len(signed_pairs & positive_pairs),
            "complete_positive_overlap_pair_count": len(complete_pairs & positive_pairs),
            "total_candidate_pair_count": len(candidate_universe),
            "unique_priority_assignment_census": dict(sorted(assignment_census.items())),
            "unique_priority_assignment_closed": priority_count == len(candidate_universe),
            "total_candidate_universe_materialized": True,
            "route_ledger_filename": priority_path.name,
            "route_ledger_file_sha256": priority_file,
            "route_ledger_rows_sha256": priority_rows_sha,
        },
        "C27_C28_C29": (
            "REBUILD_REQUIRED_CROSS_COMPONENT_WITNESS"
            if cross_component else "REJECT_PENDING_INDEPENDENT_VERIFIER_AND_ATTACKS"
        ),
        "strict_nonpromotion": {
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
        },
        "evidence_tree_hygiene": {
            "scratch_SQLite_excluded_from_candidate_tree": True,
            "candidate_tree_contains_only_canonical_closed_JSON_or_JSONL_gzip": True,
        },
        "status": (
            "PASS_TOTAL_CURRENT_CANDIDATE_UNIVERSE_AND_UNIQUE_PRIORITY__CROSS_COMPONENT_WITNESS_REBUILD_REQUIRED__ZERO_CREDIT"
            if cross_component else
            "PASS_TOTAL_CURRENT_CANDIDATE_UNIVERSE_AND_UNIQUE_PRIORITY__ALL_PAIRS_ALREADY_SAME_COMPONENT__ZERO_CREDIT"
        ),
    }
    semantic = dict(result)
    semantic.pop("invocation_seed")
    result["semantic_projection_sha256"] = digest(semantic)
    result["result_sha256"] = digest(result)
    need(
        stat_fingerprint(crosswalk_path) == crosswalk_pre_stat
        and stat_fingerprint(identity_result_path) == identity_pre_stat
        and file_hash(crosswalk_path) == args.crosswalk_sha256
        and file_hash(identity_result_path) == args.identity_result_sha256,
        "predecessor bundle post-read TOCTOU",
    )
    (out / "result.json").write_bytes(canonical(result) + b"\n")
    db.close()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print("FAIL:" + str(error))
        raise SystemExit(2)
