#!/usr/bin/env python3
"""Append-only old-C15 component-edge adapter for the rebuilt 91,672 routes.

This adapter consumes only materialized, hash-pinned ledgers.  It does not
import the route producer, its geometry engine, C27 FAMILIES, or a historical
edge ledger as a candidate universe.  The strict-volume and G2A edge ledgers
are validation sets only.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


TERMINALS = (
    "SIGNED_BOUNDARY_FACES",
    "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS",
)


def canon(x: Any) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def obj_sha(x: Any) -> str:
    return hashlib.sha256(canon(x)).hexdigest()


def need(ok: bool, msg: str) -> None:
    if not ok:
        raise RuntimeError(msg)


def stat_tuple(st: os.stat_result) -> tuple[int, ...]:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns,
            st.st_mode, st.st_uid, st.st_gid)


class Capture:
    def __init__(self, label: str, path: Path, expected_sha: str):
        self.label = label
        self.path = path
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        self.fd = os.open(path, flags)
        self.before = stat_tuple(os.fstat(self.fd))
        h = hashlib.sha256()
        off = 0
        while True:
            b = os.pread(self.fd, 1 << 20, off)
            if not b:
                break
            h.update(b)
            off += len(b)
        self.sha256 = h.hexdigest()
        need(self.sha256 == expected_sha, f"{label}: sha256")
        self.after_hash = stat_tuple(os.fstat(self.fd))
        need(self.before == self.after_hash, f"{label}: changed during hash")

    def jsonl(self) -> Iterable[dict[str, Any]]:
        raw = os.fdopen(os.dup(self.fd), "rb")
        if self.path.name.endswith(".gz"):
            zipped = gzip.GzipFile(fileobj=raw, mode="rb")
            text = io.TextIOWrapper(zipped, encoding="utf-8")
        else:
            text = io.TextIOWrapper(raw, encoding="utf-8")
        try:
            for line in text:
                if line.strip():
                    yield json.loads(line)
        finally:
            text.close()

    def close(self) -> dict[str, Any]:
        after = stat_tuple(os.fstat(self.fd))
        os.close(self.fd)
        need(after == self.before, f"{self.label}: changed during parse")
        return {
            "path": str(self.path),
            "sha256": self.sha256,
            "stat_fingerprint": list(after),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }


def check_row_hash(row: dict[str, Any], label: str) -> None:
    got = row.get("row_sha256")
    body = dict(row)
    body.pop("row_sha256", None)
    need(got == obj_sha(body), f"{label}: row_sha256")


def write_jsonl_gz(path: Path, rows: list[dict[str, Any]]) -> tuple[str, str]:
    row_seq = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, filename="") as z:
            for row in rows:
                line = canon(row) + b"\n"
                z.write(line)
                row_seq.update(row["row_sha256"].encode() + b"\n")
    return hashlib.sha256(path.read_bytes()).hexdigest(), row_seq.hexdigest()


def edge_from(row: dict[str, Any], kind: str) -> tuple[str, str]:
    if kind == "strict":
        pair = row["component_pair"]
    elif kind == "g2a":
        pair = row["unordered_component_pair"]
    else:
        raise AssertionError(kind)
    need(len(pair) == 2 and pair[0] != pair[1], f"{kind}: proper component edge")
    return tuple(sorted(pair))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--priority", type=Path, required=True)
    ap.add_argument("--priority-sha256", required=True)
    ap.add_argument("--positive", type=Path, required=True)
    ap.add_argument("--positive-sha256", required=True)
    ap.add_argument("--c15", type=Path, required=True)
    ap.add_argument("--c15-sha256", required=True)
    ap.add_argument("--strict-edges", type=Path, required=True)
    ap.add_argument("--strict-edges-sha256", required=True)
    ap.add_argument("--g2a-edges", type=Path, required=True)
    ap.add_argument("--g2a-edges-sha256", required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--seed", type=int, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)

    caps = {
        "priority_routes": Capture("priority_routes", args.priority, args.priority_sha256),
        "positive_pairs": Capture("positive_pairs", args.positive, args.positive_sha256),
        "frozen_C15_member_components": Capture("frozen_C15_member_components", args.c15, args.c15_sha256),
        "strict_volume_edges_validation_only": Capture("strict_volume_edges", args.strict_edges, args.strict_edges_sha256),
        "G2A_edges_validation_only": Capture("G2A_edges", args.g2a_edges, args.g2a_edges_sha256),
    }

    c15: dict[str, str] = {}
    for row in caps["frozen_C15_member_components"].jsonl():
        check_row_hash(row, "C15")
        member, component = row["registry_member_id"], row["fresh_component_id"]
        need(member not in c15, "C15 duplicate member")
        c15[member] = component
    need(len(c15) == 502_204, "C15 census")

    positive: dict[tuple[str, str], dict[str, Any]] = {}
    for row in caps["positive_pairs"].jsonl():
        check_row_hash(row, "positive")
        pair = (row["left_member_id"], row["right_member_id"])
        need(pair[0] < pair[1] and pair not in positive, "positive canonical unique pair")
        need(row["positive_volume_physical_overlap"] is True, "positive evidence")
        need(row["current_C15_components"] == [c15[pair[0]], c15[pair[1]]], "positive C15 join")
        need(row["same_current_C15_component"] == (c15[pair[0]] == c15[pair[1]]), "positive same-C15 flag")
        positive[pair] = row
    need(len(positive) == 55_532, "positive census")

    route_counts = Counter()
    same_counts = Counter()
    cross_counts = Counter()
    terminal_edges: dict[str, set[tuple[str, str]]] = {t: set() for t in TERMINALS}
    seen_pairs: set[tuple[str, str]] = set()
    witness_drafts: list[dict[str, Any]] = []
    positive_seen: set[tuple[str, str]] = set()
    for row in caps["priority_routes"].jsonl():
        check_row_hash(row, "priority")
        pair = (row["left_member_id"], row["right_member_id"])
        need(pair[0] < pair[1] and pair not in seen_pairs, "priority canonical unique pair")
        seen_pairs.add(pair)
        terminal = row["assigned_terminal"]
        need(terminal in TERMINALS, "priority terminal")
        need(row["pair_assignment_rule"] == "FIRST_MATCH_SIGNED_THEN_COMPLETE_THEN_POSITIVE", "priority rule")
        comps = [c15[pair[0]], c15[pair[1]]]
        need(row["current_C15_components"] == comps, "priority C15 join")
        same = comps[0] == comps[1]
        need(row["same_current_C15_component"] == same, "priority same-C15 flag")
        s = row["raw_signed_face_evidence"]
        c = row["raw_complete_face_evidence"]
        p = row["raw_positive_C19_physical_support_evidence"]
        expected = ("SIGNED_BOUNDARY_FACES" if s else
                    "COMPLETE_BOUNDARY_FACES" if c else
                    "POSITIVE_VOLUME_CARRIERS" if p else None)
        need(terminal == expected, "priority evidence/terminal")
        if terminal == "POSITIVE_VOLUME_CARRIERS":
            need(pair in positive, "positive route has primitive row")
            need(row["positive_primitive_row_sha256"] == positive[pair]["row_sha256"], "positive row binding")
            need(row["positive_source_branch"] == "CURRENT_C19_PHYSICAL_SUPPORT", "positive branch")
            positive_seen.add(pair)
        else:
            need(row["positive_primitive_row_sha256"] is None and row["positive_source_branch"] is None,
                 "nonpositive has no positive binding")
        route_counts[terminal] += 1
        (same_counts if same else cross_counts)[terminal] += 1
        if not same:
            edge = tuple(sorted(comps))
            terminal_edges[terminal].add(edge)
            body = {
                "assigned_terminal": terminal,
                "formal_credit": 0,
                "member_pair": list(pair),
                "old_C15_component_pair": list(edge),
                "positive_primitive_row_sha256": row["positive_primitive_row_sha256"],
                "priority_route_row_sha256": row["row_sha256"],
                "schema": "cm2.c27-independent.current-support-91672.old-c15-cross-member-witness.row.v1",
            }
            body["row_sha256"] = obj_sha(body)
            witness_drafts.append(body)
    need(len(seen_pairs) == 91_672, "priority census")
    need(route_counts == {"SIGNED_BOUNDARY_FACES": 25_452,
                          "COMPLETE_BOUNDARY_FACES": 10_688,
                          "POSITIVE_VOLUME_CARRIERS": 55_532}, "terminal census")
    need(positive_seen == set(positive), "all positive primitive rows consumed once")

    strict: set[tuple[str, str]] = set()
    for row in caps["strict_volume_edges_validation_only"].jsonl():
        check_row_hash(row, "strict edge")
        need(row["witness_occurrence_count"] > 0
             and row["unique_member_pair_count"] > 0
             and sum(row["source_pair_census"].values()) == row["witness_occurrence_count"]
             and (row["edge_has_incremental_nonidentical_overlap"] is True
                  or row["edge_in_known_228_baseline"] is True),
             "strict edge baseline-or-incremental evidence")
        e = edge_from(row, "strict")
        need(e not in strict, "strict unique edge")
        strict.add(e)
    need(len(strict) == 14_772, "strict edge census")

    g2a: set[tuple[str, str]] = set()
    for row in caps["G2A_edges_validation_only"].jsonl():
        check_row_hash(row, "G2A edge")
        e = edge_from(row, "g2a")
        need(e not in g2a, "G2A unique edge")
        g2a.add(e)
    need(len(g2a) == 144, "G2A edge census")

    witness_drafts.sort(key=lambda r: (r["old_C15_component_pair"], r["member_pair"], r["assigned_terminal"]))
    by_edge: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in witness_drafts:
        by_edge[tuple(r["old_C15_component_pair"])].append(r)
    current_edges = set(by_edge)
    need(sum(cross_counts.values()) == 32_012, "cross member-pair census")
    need(cross_counts == {"POSITIVE_VOLUME_CARRIERS": 32_012}, "actual cross-terminal census")
    need(len(current_edges) == 14_620, "current unique old-C15 edges")
    need(current_edges <= strict and len(current_edges & strict) == 14_620, "current edges subset strict")
    need(len(current_edges & g2a) == 40, "current/G2A overlap")

    edge_rows: list[dict[str, Any]] = []
    cursor = 0
    for edge in sorted(current_edges):
        ws = by_edge[edge]
        tc = Counter(r["assigned_terminal"] for r in ws)
        seq = hashlib.sha256()
        for r in ws:
            seq.update(r["row_sha256"].encode() + b"\n")
        body = {
            "formal_credit": 0,
            "member_witness_ordinal_range": [cursor, cursor + len(ws)],
            "old_C15_component_pair": list(edge),
            "overlaps_G2A_component_edge": edge in g2a,
            "overlaps_strict_volume_component_edge": edge in strict,
            "schema": "cm2.c27-independent.current-support-91672.unique-old-c15-component-edge.row.v1",
            "source_terminal_member_pair_census": {t: tc.get(t, 0) for t in TERMINALS},
            "supporting_member_pair_count": len(ws),
            "supporting_witness_row_sequence_sha256": seq.hexdigest(),
            "unique_edge_key": "|".join(edge),
        }
        body["row_sha256"] = obj_sha(body)
        edge_rows.append(body)
        cursor += len(ws)
    need(cursor == len(witness_drafts), "edge slice closure")

    witness_path = args.out_dir / "current_support_91672_cross_old_C15_member_pair_witnesses.jsonl.gz"
    edge_path = args.out_dir / "current_support_91672_unique_old_C15_component_edges.jsonl.gz"
    witness_file_sha, witness_seq_sha = write_jsonl_gz(witness_path, witness_drafts)
    edge_file_sha, edge_seq_sha = write_jsonl_gz(edge_path, edge_rows)

    input_attestations = {label: cap.close() for label, cap in caps.items()}
    result = {
        "CM2": "NO-GO_FOR_CLAIM",
        "C27_C28_C29": "FULL_REBUILD_REQUIRED__NO_PATCH_PROMOTION",
        "adapter_role": "APPEND_ONLY_MATERIALIZATION_FROM_REBUILT_PRIORITY_AND_PRIMITIVE_POSITIVE_LEDGERS",
        "candidate_governance": {
            "C27_FAMILIES_imported_or_read": False,
            "historical_edge_ledger_used_as_candidate_universe": False,
            "strict_volume_and_G2A_edges_used_as_validation_only": True,
        },
        "formal_credit": 0,
        "input_capture": {
            "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
            "attestations": input_attestations,
        },
        "invocation_seed_excluded_from_canonical_semantics": True,
        "route_census": {
            "all": 91_672,
            "by_terminal": {t: route_counts[t] for t in TERMINALS},
            "same_old_C15_component_by_terminal": {t: same_counts[t] for t in TERMINALS},
            "cross_old_C15_component_by_terminal": {t: cross_counts[t] for t in TERMINALS},
            "cross_old_C15_component_member_pairs": len(witness_drafts),
            "unique_cross_old_C15_component_edges": len(edge_rows),
            "unique_cross_edges_by_terminal": {t: len(terminal_edges[t]) for t in TERMINALS},
        },
        "validation_set_relations": {
            "strict_volume_edges": len(strict),
            "current_edges_intersection_strict_volume": len(current_edges & strict),
            "current_edges_minus_strict_volume": len(current_edges - strict),
            "strict_volume_minus_current_edges": len(strict - current_edges),
            "G2A_edges": len(g2a),
            "current_edges_intersection_G2A": len(current_edges & g2a),
            "current_edges_minus_G2A": len(current_edges - g2a),
            "G2A_minus_current_edges": len(g2a - current_edges),
        },
        "outputs": {
            witness_path.name: {"row_count": len(witness_drafts), "file_sha256": witness_file_sha,
                                "row_sequence_sha256": witness_seq_sha},
            edge_path.name: {"row_count": len(edge_rows), "file_sha256": edge_file_sha,
                             "row_sequence_sha256": edge_seq_sha},
        },
        "qualification": {
            "G2A_5264": "OPEN_UNLESS_SEPARATELY_SEALED",
            "twenty_family_physical_totality": "OPEN",
            "C27": "UNAUTHORIZED",
            "C28": "UNAUTHORIZED",
            "C29": "UNAUTHORIZED",
            "Source_W_formal_remainder": 80,
        },
        "schema": "cm2.c27-independent.current-support-91672.old-c15-edge-adapter.result.v1",
        "status": "PASS_APPEND_ONLY_EDGE_MATERIALIZATION__ZERO_FORMAL_CREDIT",
    }
    result["result_sha256"] = obj_sha(result)
    result_path = args.out_dir / "result.json"
    result_path.write_bytes(canon(result) + b"\n")
    print(json.dumps({
        "result": str(result_path),
        "result_sha256": result["result_sha256"],
        "cross_member_pairs": len(witness_drafts),
        "unique_component_edges": len(edge_rows),
        "current_intersection_G2A": len(current_edges & g2a),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
