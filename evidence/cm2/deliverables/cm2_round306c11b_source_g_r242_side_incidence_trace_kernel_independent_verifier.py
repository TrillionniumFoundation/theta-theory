#!/usr/bin/env python3
"""Independent verifier for the round306c11b R242 local incidence kernel."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterator


ROOT = Path(__file__).parent
PREFIX = "cm2_round306c11b_source_g_r242_side_incidence_trace_kernel"
RESULT = PREFIX + "_result.json"
INTERFACES = PREFIX + "_interface_kernel_ledger.jsonl.gz"
RELATIONS = PREFIX + "_relation_theorem_ledger.jsonl.gz"
C10_SUPPORT = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
C11_ROUTING = "cm2_round306c11_source_g_graph_side_local_theorem_disposition_disposition_ledger.jsonl.gz"
EXPECTED_PRODUCER_SHA = "45922610bac5465f97b7398e093ee821d0360625d45086905f7a15e14289174a"
MANIFEST = PREFIX + "_manifest.sha256"


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            need(type(row) is dict, f"row object:{path.name}:{ordinal}")
            core = dict(row)
            claimed = core.pop("row_sha256", None)
            need(type(claimed) is str and claimed == object_sha(core), f"row closure:{path.name}:{ordinal}")
            yield row


def ref(row: dict[str, Any]) -> dict[str, str]:
    return {"row_id": row["row_id"], "row_sha256": row["row_sha256"]}


def validate_file(path: Path, descriptor: dict[str, Any]) -> None:
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "regular candidate:" + path.name)
    need(info.st_size == descriptor["compressed_size"], "candidate size:" + path.name)
    need(file_sha(path) == descriptor["compressed_sha256"], "candidate digest:" + path.name)


def validate_ast(node: Any, label: str) -> None:
    need(type(node) is dict and type(node.get("op")) is str, "AST node:" + label)
    op = node["op"]
    if op == "RATIONAL_CONSTANT":
        need(set(node) == {"op", "value"} and type(node["value"]) is str, "AST rational:" + label)
    elif op == "COORDINATE":
        need(set(node) == {"op", "name"} and node["name"] in {"t", "p", "s"}, "AST coordinate:" + label)
    elif op in {"ADD", "MUL", "AND"}:
        need(set(node) == {"op", "args"} and type(node["args"]) is list and bool(node["args"]), "AST nary:" + label)
        for ordinal, child in enumerate(node["args"]):
            validate_ast(child, label + ":" + str(ordinal))
    elif op in {"NEG", "SQUARE"}:
        need(set(node) == {"op", "arg"}, "AST unary:" + label)
        validate_ast(node["arg"], label + ":arg")
    elif op == "SQRT_PRINCIPAL_NONNEGATIVE":
        need(set(node) == {"op", "radicand"}, "AST sqrt:" + label)
        validate_ast(node["radicand"], label + ":radicand")
    elif op in {"EQ", "LT", "GT"}:
        need(set(node) == {"op", "left", "right"}, "AST binary:" + label)
        validate_ast(node["left"], label + ":left")
        validate_ast(node["right"], label + ":right")
    elif op in {"CLOSED_INTERVAL", "OPEN_INTERVAL"}:
        need(set(node) == {"op", "coordinate", "lower", "upper"} and node["coordinate"] in {"t", "p", "s"}, "AST interval:" + label)
    else:
        raise Rejected("AST operation:" + label + ":" + op)


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir")
    parser.add_argument("--manifest-first-no-write", action="store_true")
    args = parser.parse_args()
    need((args.candidate_dir is None) != (args.manifest_first_no_write is False), "exactly one verifier mode")
    manifest_mode = args.manifest_first_no_write
    candidate = ROOT.resolve() if manifest_mode else Path(args.candidate_dir).resolve()
    need(candidate.is_dir(), "candidate directory")
    if manifest_mode:
        expected_names = {
            PREFIX + "_producer.py",
            PREFIX + "_independent_verifier.py",
            PREFIX + "_attack_harness.py",
            INTERFACES,
            RELATIONS,
            RESULT,
            PREFIX + "_verification.json",
            PREFIX + "_report.md",
            PREFIX + "_cold_replay.md",
        }
        entries: dict[str, str] = {}
        for line in (ROOT / MANIFEST).read_text(encoding="ascii").splitlines():
            digest, marker, name = line.partition("  ")
            need(marker == "  " and len(digest) == 64 and name not in entries, "manifest syntax")
            entries[name] = digest
        need(set(entries) == expected_names, "manifest member exhaustion")
        for name, digest in entries.items():
            need(file_sha(ROOT / name) == digest, "manifest member digest:" + name)

    producer = ROOT / (PREFIX + "_producer.py")
    need(file_sha(producer) == EXPECTED_PRODUCER_SHA, "producer pin")
    result_path = candidate / RESULT
    result = json.loads(result_path.read_bytes())
    core = dict(result)
    claimed = core.pop("result_sha256", None)
    need(type(claimed) is str and claimed == object_sha(core), "result closure")
    need(result_path.read_bytes() == canonical(result), "canonical result")
    need(result["producer_source"]["sha256"] == EXPECTED_PRODUCER_SHA, "result producer binding")
    need(result["census"]["R242_graphs"] == 264 and result["census"]["local_graph_side_relations"] == 528, "result census")
    need(result["scoped_credit"] == {"local_graph_side_physical_incidence": 528, "one_sided_trace": 528}, "scoped credit")
    need(all(value == 0 for value in result["formal_credit"].values()), "downstream zero")

    interface_path = candidate / INTERFACES
    relation_path = candidate / RELATIONS
    validate_file(interface_path, result["interface_kernel_ledger"])
    validate_file(relation_path, result["relation_theorem_ledger"])

    supports: dict[str, dict[str, Any]] = {}
    for row in rows(ROOT / C10_SUPPORT):
        if row["graph_class"] == "R242_UNIQUE_GRAPH_FULL_PATCH":
            need(row["graph_id"] not in supports, "C10 R242 uniqueness")
            supports[row["graph_id"]] = row
    need(len(supports) == 264, "C10 R242 exhaustion")

    routing: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in rows(ROOT / C11_ROUTING):
        if row["graph_class"] != "R242_UNIQUE_GRAPH_FULL_PATCH":
            continue
        key = (row["graph_id"], row["side_role"], row["side_member_id"])
        need(key not in routing, "routing subject uniqueness")
        need(row["candidate_ready_routing"] is True and row["disposition"] == "CANDIDATE_READY_ROUTING", "routing ready")
        need(row["local_graph_side_physical_incidence_proved"] is False and row["one_sided_trace_proved"] is False, "routing pending")
        need(row["DSU_edge_or_union_authorized"] is False and all(value == 0 for value in row["formal_credit"].values()), "routing zero boundary")
        routing[key] = row
    need(len(routing) == 528, "routing R242 exhaustion")

    interfaces: dict[str, dict[str, Any]] = {}
    derivative = Counter()
    for row in rows(interface_path):
        graph_id = row["graph_id"]
        need(graph_id in supports and graph_id not in interfaces, "interface graph binding")
        support = supports[graph_id]
        need(row["C10_exact_support_ref"] == ref(support), "interface C10 support ref")
        need(
            row["edge_kind_exhaustion"]
            == ["OWNER_BULK_TO_HALF_OPEN_SHEET", "RESOLVED_TO_MATCHING_GRAPH_SIDE_BULK", "SHADOW_BULK_TO_HALF_OPEN_SHEET"]
            and set(row["three_edge_bundle"])
            == {"owner_bulk_to_half_open_sheet", "resolved_to_matching_graph_side_bulk", "shadow_bulk_to_half_open_sheet"},
            "interface three-edge exhaustion",
        )
        need(row["graph_sheet_set_equality_proved"] is False and row["representation_pullback_proved"] is False, "interface nonpromotion")
        need(row["DSU_edge_or_union_authorized"] is False and all(value == 0 for value in row["downstream_nonpromotion"].values()), "interface downstream zero")
        derivative[row["strict_t_derivative_sign"]] += 1
        interfaces[graph_id] = row
    need(len(interfaces) == 264 and derivative == {"STRICT_POSITIVE": 132, "STRICT_NEGATIVE": 132}, "interface exhaustion")

    seen_subjects: set[tuple[str, str, str]] = set()
    roles = Counter()
    directions = Counter()
    for row in rows(relation_path):
        graph_id = row["graph_id"]
        key = (graph_id, row["side_role"], row["side_member_id"])
        need(key in routing and key not in seen_subjects, "relation routing subject")
        seen_subjects.add(key)
        support = supports[graph_id]
        interface = interfaces[graph_id]
        route = routing[key]
        need(row["C11_routing_disposition_ref"] == ref(route), "relation C11 routing ref")
        need(row["C10_exact_support_ref"] == ref(support), "relation C10 support ref")
        need(row["interface_kernel_ref"] == ref(interface), "relation interface ref")
        for name in ("exact_side_carrier_ast", "sealed_signature_witness_corridor_ast", "common_boundary_graph_ast"):
            validate_ast(row[name], graph_id + ":" + name)
            need(row["ast_sha256"][name] == object_sha(row[name]), "relation AST digest:" + name)
        need(row["common_boundary_graph_ast"] == support["exact_support_ast"], "exact common boundary")
        need(row["local_graph_side_physical_incidence_proved"] is True and row["one_sided_trace_proved"] is True, "local theorem credit")
        need(row["graph_sheet_set_equality_proved"] is False and row["representation_pullback_proved"] is False, "relation nonpromotion")
        need(row["DSU_edge_or_union_authorized"] is False, "relation DSU boundary")
        credit = row["formal_credit"]
        need(credit["local_graph_side_physical_incidence"] == credit["one_sided_trace"] == 1, "relation scoped credit")
        need(all(value == 0 for key_name, value in credit.items() if key_name not in {"local_graph_side_physical_incidence", "one_sided_trace"}), "relation downstream zero")
        direction = row["one_sided_direction_receipt"]["direction_from_graph"]
        role = row["side_role"]
        need((role, direction) in {("OWNER_OPEN_BULK", "DECREASING_T_FROM_GRAPH"), ("OWNER_OPEN_BULK", "INCREASING_T_FROM_GRAPH"), ("SHADOW_OPEN_BULK", "DECREASING_T_FROM_GRAPH"), ("SHADOW_OPEN_BULK", "INCREASING_T_FROM_GRAPH")}, "direction vocabulary")
        roles[role] += 1
        directions[direction] += 1
    need(seen_subjects == set(routing), "relation routing exhaustion")
    need(roles == {"OWNER_OPEN_BULK": 264, "SHADOW_OPEN_BULK": 264}, "role census")
    need(directions == {"DECREASING_T_FROM_GRAPH": 264, "INCREASING_T_FROM_GRAPH": 264}, "direction census")

    status = "PASS_MANIFEST_FIRST_NO_WRITE_C11B_264_INTERFACES_528_RELATIONS" if manifest_mode else "PASS_INDEPENDENT_C11B_264_INTERFACES_528_RELATIONS"
    print(json.dumps({"status": status, "result_sha256": claimed}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
