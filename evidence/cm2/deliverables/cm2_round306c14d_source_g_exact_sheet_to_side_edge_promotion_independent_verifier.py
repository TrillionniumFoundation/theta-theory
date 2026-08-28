#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Final, Iterator

ROOT: Final = Path(__file__).resolve().parent
PREFIX: Final = "cm2_round306c14d_source_g_exact_sheet_to_side_edge_promotion"
EDGES: Final = PREFIX + "_edge_promotion_ledger.jsonl.gz"
NEGATIVE: Final = PREFIX + "_negative_disposition_ledger.jsonl.gz"
RESULT: Final = PREFIX + "_result.json"
MANIFEST: Final = PREFIX + "_manifest.sha256"
PRODUCER: Final = PREFIX + "_producer.py"
PRODUCER_SHA: Final = "de768c53f87b11a51dbf53d6515bd7dd425a9b19563ced48dda3f6a55bce79e4"


class Rejected(RuntimeError): pass


def need(v: bool, label: str) -> None:
    if type(v) is not bool or not v: raise Rejected(label)


def canonical(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def obj(v: Any) -> str: return hashlib.sha256(canonical(v)).hexdigest()


def fsha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as s:
        while b := s.read(1048576): h.update(b)
    return h.hexdigest()


def source_rows(p: Path, label: str) -> Iterator[dict[str, Any]]:
    with gzip.open(p, "rt", encoding="utf-8", newline="") as s:
        for line in s:
            r = json.loads(line); claimed = r.pop("row_sha256", None)
            need(claimed == obj(r), label + ":closure"); r["row_sha256"] = claimed
            yield r


def candidate_rows(p: Path, d: dict[str, Any], label: str) -> list[dict[str, Any]]:
    raw = p.read_bytes()
    need(len(raw) == d["size"] and fsha(p) == d["sha256"], label + ":wire")
    h = hashlib.sha256(); out = []
    with gzip.open(p, "rb") as s:
        for line in s:
            h.update(line); r = json.loads(line); claimed = r.pop("row_sha256", None)
            need(claimed == obj(r), label + ":closure"); r["row_sha256"] = claimed; out.append(r)
    need(len(out) == d["row_count"] and h.hexdigest() == d["uncompressed_sha256"],
         label + ":descriptor")
    return out


def manifest_members() -> dict[str, str]:
    out = {}
    for line in (ROOT / MANIFEST).read_text(encoding="ascii").splitlines():
        digest, name = line.split("  ", 1); need(name not in out and len(digest) == 64, "manifest")
        out[name] = digest
    return out


def verify(candidate: Path, manifest_first: bool) -> dict[str, Any]:
    if manifest_first:
        m = manifest_members()
        need(len(m) == 9 and all((ROOT / n).is_file() and fsha(ROOT / n) == h for n, h in m.items()),
             "manifest members")
    raw = (candidate / RESULT).read_bytes(); result = json.loads(raw); core = dict(result)
    claimed = core.pop("result_sha256", None)
    need(raw == canonical(result) and claimed == obj(core), "result closure")
    need(result["producer_source"] == {"filename": PRODUCER, "size": 13605,
                                      "sha256": PRODUCER_SHA} and
         (ROOT / PRODUCER).stat().st_size == 13605 and fsha(ROOT / PRODUCER) == PRODUCER_SHA,
         "producer pin")
    pins = result["source_pins"]
    need(len(pins) == 5 and len({p["name"] for p in pins}) == 5, "pins")
    src = {p["name"]: ROOT / p["filename"] for p in pins}
    need(all(p.is_file() and not p.is_symlink() for p in src.values()), "source paths")
    edges = candidate_rows(candidate / EDGES, result["edge_promotion_ledger"], "edges")
    negative = candidate_rows(candidate / NEGATIVE, result["negative_disposition_ledger"], "negative")
    need(len(edges) == 8864 and not negative, "candidate census")
    need(result["formal_edge_authority_census"]["promoted_edges"] == 8864 and
         result["formal_edge_authority_census"]["negative_dispositions"] == 0 and
         result["strict_nonpromotion"]["fresh_DSU_applied_edges"] == 0 and
         result["strict_nonpromotion"]["representation_pullback"] == 0,
         "result preflight")
    for r in edges:
        need(r["edge_promotion_credit"] == 1 and r["negative_disposition_required"] is False and
             r["fed_to_fresh_DSU_pending"] is True and r["fresh_DSU_application_credit"] == 0 and
             r["DSU_union_or_component_credit"] == 0 and
             r["composition_certificate"]["graph_equals_new_exact_sheet"] is True and
             r["composition_certificate"]["graph_in_relative_closure_of_side"] is True and
             r["composition_certificate"]["one_sided_trace_to_graph"] is True and
             r["composition_certificate"]["new_exact_sheet_in_relative_closure_of_side"] is True,
             "edge preflight")
    for p in pins:
        q = src[p["name"]]
        need(q.stat().st_size == p["size"] and fsha(q) == p["sha256"], "source pin:" + p["name"])

    admissions = {}
    for r in source_rows(src["C14C_ADMISSION"], "C14c"):
        need(r["graph_id"] not in admissions and r["registry_member_admission_credit"] == 1 and
             r["self_root_authority_credit"] == 1, "C14c scope")
        admissions[r["graph_id"]] = r
    need(len(admissions) == 4432, "C14c count")
    kernels = {}; side_ids = set(); c11_count = 0; per_graph = {}
    for r in source_rows(src["C11A_KERNEL"], "C11a"):
        c11_count += 1
        if r["graph_id"] in admissions:
            key = (r["graph_id"], r["side_member_id"])
            need(key not in kernels and r["scoped_credit"] == {
                "local_graph_side_physical_incidence": 1, "one_sided_trace": 1}, "C11a scope")
            kernels[key] = r; side_ids.add(r["side_member_id"])
            per_graph[r["graph_id"]] = per_graph.get(r["graph_id"], 0) + 1
    need(c11_count == 9422 and len(kernels) == 8864 and set(per_graph.values()) == {2} and
         len(per_graph) == 4432 and len(side_ids) == 8864, "C11a exhaustion")
    sides = {}; c6_count = 0; collisions = 0
    new_ids = {r["new_exact_sheet_member_id"] for r in admissions.values()}
    for r in source_rows(src["C6_MEMBER"], "C6"):
        c6_count += 1; member = r["registry_member_id"]
        if member in new_ids: collisions += 1
        if member in side_ids:
            need(member not in sides, "side unique"); sides[member] = r
    need(c6_count == 497772 and collisions == 0 and len(sides) == 8864, "C6 exhaustion")

    by_key = {(r["graph_id"], r["side_member_id"]): r for r in edges}
    need(len(by_key) == 8864 and set(by_key) == set(kernels), "candidate join keys")
    ordinals = set(); edge_ids = set(); pairs = set(); roots = set(); components = set(); keymatch = 0
    for key, kernel in kernels.items():
        graph, side_id = key; admission = admissions[graph]; side = sides[side_id]; row = by_key[key]
        new = admission["new_exact_sheet_member_id"]; new_root = admission["self_base_root_id"]
        side_root = side["new_base_root_id"]; pair = tuple(sorted((new_root, side_root)))
        edge_id = "round306c14d-exact-sheet-side-edge:" + obj([new, side_id, graph, kernel["side_role"]])
        cert_hash = obj([admission["row_sha256"], kernel["row_sha256"], side["row_sha256"], pair])
        need(row["promoted_edge_id"] == edge_id and row["new_exact_sheet_member_id"] == new and
             row["side_role"] == kernel["side_role"] and row["new_exact_sheet_self_root_id"] == new_root and
             row["side_existing_base_root_id"] == side_root and
             row["projected_base_root_pair"] == list(pair) and
             row["C14c_admission_ref"] == {"row_id": admission["row_id"], "row_sha256": admission["row_sha256"]} and
             row["C11a_local_theorem_ref"] == {"row_id": kernel["row_id"], "row_sha256": kernel["row_sha256"]} and
             row["C6_side_member_ref"] == {"row_id": side["row_id"], "row_sha256": side["row_sha256"]} and
             row["composition_certificate"]["certificate_sha256"] == cert_hash and
             row["row_id"] == PREFIX + ":edge-promotion:" + obj([edge_id, pair]),
             "edge reconstruction")
        ordinals.add(row["edge_ordinal"]); edge_ids.add(edge_id); pairs.add(pair)
        roots.add(side_root); components.add(side["fresh_component_id"])
        if admission["official_key_id"] == side["official_key_id"]: keymatch += 1
    need(ordinals == set(range(8864)) and len(edge_ids) == len(pairs) == 8864 and
         len(roots) == 6920 and len(components) == 4172 and keymatch == 4432,
         "edge census")
    need(result["formal_edge_authority_census"] == {
        "promoted_edges": 8864, "negative_dispositions": 0,
        "new_exact_sheet_endpoints": 4432, "side_member_endpoints": 8864,
        "distinct_existing_side_roots": 6920, "distinct_existing_side_components": 4172,
        "same_official_key_edges": 4432, "cross_official_key_edges": 4432}, "formal census")
    need(result["conditional_not_yet_credited_fresh_DSU_census_if_all_sealed_edges_are_applied"] == {
        "member_count": 502204, "base_root_count": 339036, "applied_edge_count": 484982,
        "rank_reduction": 281160, "component_count": 57876,
        "cross_component_pair_denominator": 125616475670, "formal_credit": 0},
         "conditional DSU boundary")
    return {"status": "PASS_INDEPENDENT_C14D_VERIFICATION", "result_sha256": claimed,
            "promoted_edges": 8864, "negative_dispositions": 0,
            "graphs": 4432, "side_roots": 6920, "old_components": 4172}


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    p = argparse.ArgumentParser(); p.add_argument("--candidate-dir"); p.add_argument("--manifest-first", action="store_true")
    a = p.parse_args(); need(not (a.candidate_dir and a.manifest_first), "mode")
    candidate = ROOT if a.manifest_first or a.candidate_dir is None else Path(a.candidate_dir).resolve()
    print(json.dumps(verify(candidate, a.manifest_first), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except (Rejected, KeyError, ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)}, sort_keys=True,
                         separators=(",", ":")), file=sys.stderr); raise SystemExit(1)
