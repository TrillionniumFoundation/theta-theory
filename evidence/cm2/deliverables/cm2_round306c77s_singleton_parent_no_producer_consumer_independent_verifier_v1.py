#!/usr/bin/env python3
"""Independent, no-producer verifier/finalizer for the C77s v1 consumer.

The candidate producer is bound only by a hard-coded SHA-256 declaration.  Its
source path is prohibited input: this verifier never opens, reads, parses,
decodes, imports, compiles, or executes that source.  It reconstructs the
candidate from frozen published data bytes and two isolated candidate stages.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
import os
import stat
import tempfile
import zlib
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
SCHEMA = "cm2.round306c77s.singleton-parent-no-producer-consumer.independent-verification.v1"
BASE = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1"
VERIFY_NAME = "cm2_round306c77s_singleton_parent_no_producer_consumer_independent_verification_v1.json"
FINAL_MANIFEST = "cm2_round306c77s_singleton_parent_no_producer_consumer_final_manifest_v1.sha256"
FINAL_OUTER = "cm2_round306c77s_singleton_parent_no_producer_consumer_final_outer_receipt_v1.json"
PRODUCER_BASENAME = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1.py"
PRODUCER_DECLARATION_SHA256 = "6189c5efce2227b85bb5b5ffb0886c96862da106a3d8c63313605eb64fd51136"
PAIR_IDS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)

BASE_PINS = {
    "ZERO_CREDIT_CANDIDATE_SINGLETON_PARENT_CONSUMER_ONLY.lock": "e30e853c4ad0824f514959da072a71e53d7de63b303e8cd2c92201aa3fdd2061",
    f"{BASE}_child_dispositions.jsonl.gz": "a58448ef25656b4eed89fd3eef99405990f935778a395219e2465e6634c7a5c0",
    f"{BASE}_source_rollups.jsonl.gz": "e7e2c2ba2e8ddde0eae60d648248ba4a6eea3708323253662b1bf2a344254fbd",
    f"{BASE}_reflection_pair_rollups.jsonl.gz": "1f46044689c41fa33c752865077ce33b405a37e2f5118070e06433dc54d0568b",
    f"{BASE}_singleton_cell_rollups.jsonl.gz": "bedd2b48fd0be9a76c72bd6337eb91697b3ab851674f630dfadc30a2f6678af9",
    f"{BASE}_incidence_audit.json": "a3ab3095da090dd99376fc34963fcc9d807e118d74b31ae1e2676f1834b6d5a3",
    f"{BASE}_result.json": "7544d6137a878ac8a4d1ce69ea13d63d8928d6c6db4bc1ab91bcaa8f7671963e",
    f"{BASE}_report.md": "a277ddbc10f67bb021e576037d1449949d95294fb33362519bdf32a111dc8e1d",
    f"{BASE}_manifest.sha256": "65021332c03328b3ce69a59179bb88a75016117a32c92a562d242286c552ca8d",
    f"{BASE}_outer_receipt.json": "257b3f362b81e32061cae49375967da6cf0b50d42bf67b979f46222d8ec1ac83",
}

PINS = {
    "deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_leaf_ledger_v1.jsonl.gz": "918899a914ad4fbb05c1095cac9f42f6c46d02f0acdad366538a395021aeaee6",
    "deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_parent_ledger_v1.jsonl.gz": "8817069967798042bd87315f57e7c3cea279c6564c0e50a5ac927ca4f765e510",
    "deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_parent_summary_v1.jsonl.gz": "6f3a8fa4501cb872a33d7446a14d804eeb352bb6d049158f3c7ee88893b7872d",
    "deliverables/cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
    "deliverables/cm2_round306c61s12_depth12_16shard_aggregate_parent_summary_v4.jsonl.gz": "2206c817f49312c519a720e14bc2e152cde5362ed884cbe83d32349a7ff5bab2",
    "deliverables/cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz": "4ff1c36a0a6331510da3afb988738f128a3cada04ddd297ac58584579115437d",
    "deliverables/cm2_round306c65s18_depth18_64shard_aggregate_source_summary_v1.jsonl.gz": "de8fa908cbe46e379ff05564c5d8ed0ea97de2875eca05792ad3abf63287f432",
    "deliverables/cm2_round306c65s18_depth18_64shard_aggregate_parent_summary_v1.jsonl.gz": "91adb1e9e5e7e7dfdc1cbf674d5713d218851a4b5f15602ced2664972280bc4b",
    "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256": "96b0f082688f16f821104402bc9aba1b7778df36f084a300d978dac95faf43c5",
    "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json": "f0609dc4835346e078b5299007b1b31210d28cbf772ac41bb0f390f7047ad274",
    "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json": "20a52a4c16c84ffd524833c0ee872edfeb6fdec538a1368f619244199814fb1d",
    "deliverables/cm2_round306c69b_singleton_h1_graph_slab_decider_v2_decisions.jsonl.gz": "b9bc1cd359c77ee6a5246011925090e5d5557cd88e90d1f5c67fa70a452d1eba",
    "deliverables/cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz": "69b3ec294f95cb5ce377e553ae875daab10a5bdb33e860363f6bae122022e606",
    ".cm2-runtime/c71b-v3-final-75c21279/cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_rows.jsonl.gz": "f9f04044809e46b9811d52abef94844d84b058a2f0c3fb6f5b9f97f2302cbec6",
    ".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz": "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370",
    ".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2.jsonl.gz": "58f876b6f926e152efbd695651af0505d73b74dbfe57aa7dc169887bd082b3b2",
    ".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_root_incidence.jsonl.gz": "840efb65d45175d5f0449becfbe6260167188b2b7a9c1e5560549d4f66c4ae8d",
    ".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1.jsonl.gz": "3c636d4e2151203eced98d514567d47bc50aaed83aeadf0454da7c6a1aae6772",
    ".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1_endpoint_incidence.jsonl.gz": "1b35ef3cde3d57fc7ef25f010fdf74089d63a5e5519c7d5a01b80fb01956c2c7",
    ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1.jsonl.gz": "e1e30a36f75c2ec71b0c4ec51da33e3c09fb5570426aa356f0c815406e251229",
    ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_endpoint_incidence.jsonl.gz": "db50b71ff364a1f1e132ca0804bd5eb8b027d0c9138f93ee95cfe55e71afb0f2",
    ".cm2-runtime/c72o-build-a2.v1/cm2_round306c72o_collision1_outgoing_state_oracle_v1.jsonl.gz": "e3125863adcf3ef6489dce741337622b1d70b2ce7655d8d06237c1612ff19355",
    ".cm2-runtime/c73v2-build-a.QOYACE/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2.jsonl.gz": "ed0a3d26f4984e6eced899a01f58aa8329bb1db72b7d0bfb9fe17ee3a4eef6fc",
    ".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1.jsonl.gz": "46bb3ac40d5fcadd98463f4de73c404760dd0e5a0ff0a11b48e69a2adbef13b7",
    ".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1_root_incidence.jsonl.gz": "b9e6724c73f051eddcc7bd6fd633fea0ad0346d5f8056712b44c12280d8787b7",
    "deliverables/cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz": "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce",
    "deliverables/cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz": "bebc49f66efb01c0b980ec10258a60d7aead9d4d2006d28bdd169c9a9ae38a04",
}


class Reject(RuntimeError):
    pass


def require(ok: bool, why: str) -> None:
    if not ok:
        raise Reject(why)


def compact(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def object_digest(obj: dict[str, Any]) -> str:
    x = dict(obj)
    x.pop("object_sha256", None)
    return digest(compact(x))


def with_row_hash(obj: dict[str, Any]) -> dict[str, Any]:
    out = dict(obj)
    out["row_sha256"] = digest(compact(obj))
    return out


def with_object_hash(obj: dict[str, Any]) -> dict[str, Any]:
    out = dict(obj)
    out["object_sha256"] = digest(compact(obj))
    return out


def parse(raw: bytes, *, canonical: bool = True) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out = {}
        for key, value in items:
            require(key not in out, "duplicate JSON key")
            out[key] = value
        return out
    obj = json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(Reject(x)))
    if canonical:
        require(raw in (compact(obj), compact(obj) + b"\n"), "noncanonical JSON")
    if isinstance(obj, dict) and "object_sha256" in obj:
        require(obj["object_sha256"] == object_digest(obj), "object closure")
    return obj


def safe_read_path(path: Path, expected: str | None = None) -> bytes:
    require(path.name != PRODUCER_BASENAME, "candidate producer source prohibited")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "unsafe input file")
        blocks = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            blocks.append(block)
        after = os.fstat(fd)
    finally:
        os.close(fd)
    named = os.stat(path, follow_symlinks=False)
    ident = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns)
    require(ident(before) == ident(after) == ident(named), "input TOCTOU")
    raw = b"".join(blocks)
    if expected is not None:
        require(digest(raw) == expected, f"input pin: {path}")
    return raw


def upstream(rel: str) -> bytes:
    require(rel in PINS and not rel.endswith(".py"), "unapproved or producer-like upstream input")
    return safe_read_path(ROOT / rel, PINS[rel])


def one_member(raw: bytes) -> None:
    dec = zlib.decompressobj(16 + zlib.MAX_WBITS)
    for off in range(0, len(raw), 1 << 20):
        dec.decompress(raw[off:off + (1 << 20)])
        require(not dec.unused_data, "multiple-member/trailing gzip")
    dec.flush()
    require(dec.eof and not dec.unused_data and not dec.unconsumed_tail, "incomplete gzip")


def rows_from_bytes(raw: bytes, label: str) -> list[dict[str, Any]]:
    one_member(raw)
    out = []
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
        for ordinal, line in enumerate(stream, 1):
            require(line.endswith(b"\n"), f"row newline {label}:{ordinal}")
            row = parse(line[:-1])
            require(isinstance(row, dict) and isinstance(row.get("row_sha256"), str), f"row shape {label}:{ordinal}")
            claim = row["row_sha256"]
            body = dict(row)
            body.pop("row_sha256")
            require(digest(compact(body)) == claim, f"row closure {label}:{ordinal}")
            out.append(row)
    return out


def upstream_rows(rel: str) -> list[dict[str, Any]]:
    return rows_from_bytes(upstream(rel), rel)


def candidate_rows(stage: Path, name: str) -> list[dict[str, Any]]:
    return rows_from_bytes(safe_read_path(stage / name, BASE_PINS[name]), name)


def fraction(value: str) -> Fraction:
    return Fraction(value)


def binary_path(row: dict[str, Any]) -> tuple[str, Fraction]:
    path = row["path"]
    volume = fraction(row["parent_volume_fraction"])
    require(isinstance(path, str) and path and set(path) <= {"0", "1"}, "binary path")
    require(volume == Fraction(1, 1 << len(path)), "path volume")
    return path, volume


def prefix_free(paths: Iterable[str]) -> bool:
    ordered = sorted(paths)
    return all(not b.startswith(a) for a, b in zip(ordered, ordered[1:]))


def validate_base_stages(a: Path, b: Path) -> dict[str, bytes]:
    require(a.is_dir() and b.is_dir() and a != b, "two distinct candidate stages required")
    require({p.name for p in a.iterdir()} == set(BASE_PINS), "stage A base member set")
    require({p.name for p in b.iterdir()} == set(BASE_PINS), "stage B base member set")
    common = {}
    for name, pin in BASE_PINS.items():
        ar = safe_read_path(a / name, pin)
        br = safe_read_path(b / name, pin)
        require(ar == br, f"dual candidate byte drift: {name}")
        common[name] = ar
    manifest = common[f"{BASE}_manifest.sha256"]
    entries = {}
    for line in manifest.decode("ascii").splitlines():
        claimed, name = line.split("  ")
        require(name not in entries and name in BASE_PINS, "base manifest member")
        entries[name] = claimed
    expected_manifest_members = set(BASE_PINS) - {f"{BASE}_manifest.sha256", f"{BASE}_outer_receipt.json"}
    require(set(entries) == expected_manifest_members and all(entries[n] == BASE_PINS[n] for n in entries), "base manifest closure")
    outer = parse(common[f"{BASE}_outer_receipt.json"])
    require(outer["manifest_file_sha256"] == BASE_PINS[f"{BASE}_manifest.sha256"] and outer["manifest_member_count"] == 8, "base outer manifest")
    require(outer["outer_receipt_published_last"] is True and outer["all_members_terminal_byte_replayed"] is True, "base outer/replay")
    require(all(outer[k] == 0 for k in ("formal_credit", "D02_gate_credit", "CM2_credit", "global_installed_credit", "candidate_public_unresolved_decrement")), "base outer zero credit")
    return common


def reconstruct_frontier() -> dict[str, Any]:
    final: dict[int, list[tuple[str, Fraction, str]]] = defaultdict(list)
    counts: dict[int, Counter] = defaultdict(Counter)
    volumes: dict[int, dict[str, Fraction]] = defaultdict(lambda: defaultdict(Fraction))
    c57_handoff = {}
    c57_all: dict[int, list[str]] = defaultdict(list)
    for row in upstream_rows("deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_leaf_ledger_v1.jsonl.gz"):
        p = row["pair_index"]
        path, vol = binary_path(row)
        require(p in PAIR_IDS and row["owner_rows_complete"] and row["event_order_bound_to_C35_collision1"], "C57 semantics")
        c57_all[p].append(path); counts[p]["C57_ALL"] += 1; volumes[p]["C57_ALL"] += vol
        if row["leaf_disposition"] == "STRICT_TERMINAL":
            require(row["collision2_handoff"] is None and row["local_terminal_credit"] == 1, "C57 strict")
            final[p].append((path, vol, "C57_STRICT_CARRY")); counts[p]["C57_STRICT_CARRY"] += 1; volumes[p]["C57_STRICT_CARRY"] += vol
        else:
            h = row["collision2_handoff"]
            require(row["leaf_disposition"] == "COLLISION2_HANDOFF" and h["next_collision_index"] == 2 and h["handoff_credit"] == 0, "C57 handoff")
            c57_handoff[row["row_sha256"]] = (p, path, vol, h["handoff_object_sha256"])
            counts[p]["C57_HANDOFF"] += 1
    require(sum(x["C57_STRICT_CARRY"] for x in counts.values()) == 462 and len(c57_handoff) == 319, "C57 census")
    c57_parents = {}
    for row in upstream_rows("deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_parent_ledger_v1.jsonl.gz"):
        p = row["pair_index"]
        require(p not in c57_parents and row["terminal_leaf_count"] == counts[p]["C57_STRICT_CARRY"] and row["collision2_handoff_leaf_count"] == counts[p]["C57_HANDOFF"], "C57 parent counts")
        require(prefix_free(c57_all[p]) and sum((Fraction(1, 1 << len(x)) for x in c57_all[p]), Fraction()) == 1, "C57 parent Kraft")
        c57_parents[p] = row["row_sha256"]
    by57: dict[str, list[tuple[str, Fraction]]] = defaultdict(list)
    c58_c2 = {}
    for row in upstream_rows("deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"):
        source = row["source_C57_leaf_row_sha256"]
        require(source in c57_handoff, "C58 source")
        p, root, source_vol, handoff_hash = c57_handoff[source]
        path, vol = binary_path(row)
        require(row["pair_index"] == p and row["source_C57_handoff_object_sha256"] == handoff_hash, "C58 lineage")
        require(path.startswith(root) and row["parent_path"] == path[:-1] and row["additional_depth"] == len(path) - len(root), "C58 refinement")
        by57[source].append((path, vol)); counts[p]["C58_ALL"] += 1; volumes[p]["C58_ALL"] += vol
        if row["disposition"] == "STRICT_TERMINAL":
            final[p].append((path, vol, "C58_STRICT_CARRY")); counts[p]["C58_STRICT_CARRY"] += 1; volumes[p]["C58_STRICT_CARRY"] += vol
        else:
            require(row["disposition"] == "COLLISION2_HANDOFF" and isinstance(row["collision2_handoff"], dict), "C58 C2")
            c58_c2[row["row_sha256"]] = (p, path, vol)
            counts[p]["C58_C2"] += 1
    require(len(by57) == 319 and len(c58_c2) == 2599, "C58 census")
    for source, (_, _, source_vol, _) in c57_handoff.items():
        leaves = by57[source]
        require(prefix_free(x[0] for x in leaves) and sum((x[1] for x in leaves), Fraction()) == source_vol, "C58 source Kraft")
    c58_parents = {}
    for row in upstream_rows("deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_parent_summary_v1.jsonl.gz"):
        p = row["pair_index"]
        require(row["strict_terminal_leaf_count"] == counts[p]["C57_STRICT_CARRY"] + counts[p]["C58_STRICT_CARRY"] and row["collision2_handoff_leaf_count"] == counts[p]["C58_C2"], "C58 parent")
        c58_parents[p] = row["row_sha256"]
    by58: dict[str, list[tuple[str, Fraction]]] = defaultdict(list)
    c61_c2 = {}
    for row in upstream_rows("deliverables/cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"):
        source = row["source_C58_leaf_row_sha256"]
        require(source in c58_c2, "C61 source")
        p, root, source_vol = c58_c2[source]
        path, vol = binary_path(row)
        require(row["pair_index"] == p and row["source_path"] == root and path.startswith(root), "C61 lineage")
        by58[source].append((path, vol)); counts[p]["C61_ALL"] += 1; volumes[p]["C61_ALL"] += vol
        if row["disposition"] == "STRICT_TERMINAL":
            final[p].append((path, vol, "C61_STRICT_CARRY")); counts[p]["C61_STRICT_CARRY"] += 1; volumes[p]["C61_STRICT_CARRY"] += vol
        else:
            require(row["disposition"] == "COLLISION2_HANDOFF", "C61 C2")
            c61_c2[row["row_sha256"]] = {"pair": p, "path": path, "volume": vol, "box": row["exact_representative_box"]}
            counts[p]["C61_C2"] += 1
    require(len(by58) == 2599 and len(c61_c2) == 20879, "C61 census")
    for source, (_, _, source_vol) in c58_c2.items():
        leaves = by58[source]
        require(prefix_free(x[0] for x in leaves) and sum((x[1] for x in leaves), Fraction()) == source_vol, "C61 source Kraft")
    c61_parents = {}
    for row in upstream_rows("deliverables/cm2_round306c61s12_depth12_16shard_aggregate_parent_summary_v4.jsonl.gz"):
        p = row["pair_index"]
        early = counts[p]["C57_STRICT_CARRY"] + counts[p]["C58_STRICT_CARRY"]
        require(row["strict_terminal_leaf_count"] == early + counts[p]["C61_STRICT_CARRY"] and row["collision2_handoff_leaf_count"] == counts[p]["C61_C2"], "C61 parent")
        c61_parents[p] = row["row_sha256"]
    source_order = []
    sources = {}
    for row in upstream_rows("deliverables/cm2_round306c65s18_depth18_64shard_aggregate_source_summary_v1.jsonl.gz"):
        key = row["source_C61_aggregate_leaf_row_sha256"]
        require(key in c61_c2 and key not in sources, "C65 source")
        src = c61_c2[key]
        require(row["pair_index"] == src["pair"] and row["source_path"] == src["path"] and fraction(row["source_Kraft_conservation"]) == src["volume"], "C65 source lineage")
        sources[key] = {"summary": row, "carry": 0, "carry_volume": Fraction(), "children": [], "volume": Fraction()}
        source_order.append(key)
    require(len(sources) == 20879, "C65 source census")
    children = {}; child_order = []
    for row in upstream_rows("deliverables/cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz"):
        source = row["source_C61_aggregate_leaf_row_sha256"]
        require(source in sources, "C65 leaf source")
        path, vol = binary_path(row); p = row["pair_index"]
        require(row["source_path"] == sources[source]["summary"]["source_path"] and path.startswith(row["source_path"]), "C65 leaf lineage")
        final[p].append((path, vol, "C65_REPLACEMENT")); counts[p]["C65_REPLACEMENT"] += 1; volumes[p]["C65_REPLACEMENT"] += vol
        sources[source]["volume"] += vol
        if row["disposition"] == "STRICT_TERMINAL":
            sources[source]["carry"] += 1; sources[source]["carry_volume"] += vol
        else:
            require(row["disposition"] == "COLLISION2_HANDOFF", "C65 C2")
            h = row["row_sha256"]
            children[h] = {"row": row, "source": source}
            child_order.append(h); sources[source]["children"].append(h)
    require(len(children) == 167255, "C65 child census")
    for key, source in sources.items():
        s = source["summary"]
        require(source["volume"] == fraction(s["source_Kraft_conservation"]), "C65 source Kraft")
        require(source["carry"] == s["strict_terminal_leaf_count"] and len(source["children"]) == s["collision2_handoff_leaf_count"], "C65 source counts")
    c65_parents = {}
    for row in upstream_rows("deliverables/cm2_round306c65s18_depth18_64shard_aggregate_parent_summary_v1.jsonl.gz"):
        p = row["pair_index"]
        require(row["C61_full_base_parent_row_sha256"] == c61_parents[p] and row["C65_replacement_leaf_count"] == counts[p]["C65_REPLACEMENT"], "C65 parent link")
        c65_parents[p] = row["row_sha256"]
    for p in PAIR_IDS:
        require(prefix_free(x[0] for x in final[p]) and sum((x[1] for x in final[p]), Fraction()) == 1, f"final pair Kraft {p}")
    return {"final": final, "counts": counts, "volumes": volumes, "parents": {p: {"C57": c57_parents[p], "C58": c58_parents[p], "C61": c61_parents[p], "C65": c65_parents[p]} for p in PAIR_IDS}, "sources": sources, "source_order": source_order, "children": children, "child_order": child_order, "c61": c61_c2}


def reconstruct_dispositions(chain: dict[str, Any]) -> dict[str, Any]:
    kind = {}
    c69row = {}
    for label, rel in [("DECISION", "deliverables/cm2_round306c69b_singleton_h1_graph_slab_decider_v2_decisions.jsonl.gz"), ("BLOCKER", "deliverables/cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz")]:
        for row in upstream_rows(rel):
            source = row["C61_aggregate_leaf_row_sha256"]
            require(source in chain["sources"] and source not in kind, "C69 partition")
            src = chain["c61"][source]
            require(row["pair_index"] == src["pair"] and row["path"] == src["path"], "C69 lineage")
            kind[source] = label; c69row[source] = row["row_sha256"]
    require(Counter(kind.values()) == {"DECISION": 2356, "BLOCKER": 18523}, "C69 census")
    c71 = {}
    for row in upstream_rows(".cm2-runtime/c71b-v3-final-75c21279/cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_rows.jsonl.gz"):
        child = row["C65_aggregate_leaf_row_sha256"]
        require(child in chain["children"] and child not in c71, "C71 child")
        c = chain["children"][child]["row"]; source = chain["children"][child]["source"]
        require(row["child_path"] == c["path"] and row["source_path"] == c["source_path"] and row["pair_index"] == c["pair_index"], "C71 lineage")
        if kind[source] == "DECISION":
            require(row["child_level_H1_full_box_closed"] is True and row["consumer_review_ready"] is True and row["remaining_blocker_codes"] == [], "C71 decision H1")
            require(row["terminal_disposition_credit"] == 0 and row["global_consumption_ready"] is False, "C71 decision zero terminal")
        else:
            require(row["consumer_review_ready"] is False and row["v2_disposition"] == "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE", "C71 blocker")
        c71[child] = row["row_sha256"]
    require(len(c71) == 167255, "C71 exhaustive")
    atlas = {}
    for row in upstream_rows(".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"):
        child = row["C65_aggregate_child_row_sha256"]
        require(child in chain["children"] and kind[chain["children"][child]["source"]] == "BLOCKER" and child not in atlas, "C72 blocker scope")
        require(row["current_disposition"] == "FAIL_CLOSED_STRUCTURAL_OBLIGATION", "C72 disposition")
        atlas[child] = row
    require(len(atlas) == 134155, "C72 exhaustive")
    dispositions = {}; census = Counter()
    specs = [
        ("C72B2", ".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2.jsonl.gz"),
        ("C74", ".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1.jsonl.gz"),
        ("C75", ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1.jsonl.gz"),
        ("C72O", ".cm2-runtime/c72o-build-a2.v1/cm2_round306c72o_collision1_outgoing_state_oracle_v1.jsonl.gz"),
        ("C73V2", ".cm2-runtime/c73v2-build-a.QOYACE/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2.jsonl.gz"),
        ("C76", ".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1.jsonl.gz"),
    ]
    for oracle, rel in specs:
        for row in upstream_rows(rel):
            child = row["C65_aggregate_child_row_sha256"]
            require(child in atlas and child not in dispositions, "oracle scope/overlap")
            a = atlas[child]; c = chain["children"][child]["row"]
            require(row.get("C72_atlas_row_sha256", row.get("C72_obligation_row_sha256")) == a["row_sha256"], "oracle atlas link")
            require(row["child_path"] == c["path"] and row["source_path"] == c["source_path"] and row["pair_index"] == c["pair_index"], "oracle lineage")
            if oracle in ("C72B2", "C76"):
                require(row["H1_geometry_closed"] and row["physical_chart_glue_closed"] and row["whole_child_strict_exclusion_closed"], "physical H1 oracle")
                terminal = "STRICT_EXCLUSION"
            elif oracle == "C74":
                require(len(row["sealed_strata"]) == 3, "C74 strata")
                terminal = "CEMETERY_TANGENCY_TERMINAL" if row["discriminant_graph"]["physical_future_tangency"] else "STRICT_EXCLUSION"
            elif oracle == "C75":
                require(row["unresolved_strata"] == 0 and row["three_strata"]["zero_graph"]["root_is_strict_future_and_first"] is True, "C75 graph")
                terminal = "CEMETERY_TANGENCY_TERMINAL"
            elif oracle == "C72O":
                require(row["exit_class"] == "STRICT_EXCLUSION" and isinstance(row["collision1_history_row_sha256"], str), "C72o route")
                terminal = "STRICT_EXCLUSION"
            else:
                require(row["allowed_exit_class"] == "STRICT_EXCLUSION" and row["complete_child_decision"] is True, "C73 route")
                terminal = "STRICT_EXCLUSION"
            dispositions[child] = (oracle, row["row_sha256"], terminal)
            census[(oracle, terminal)] += 1
    expected = {("C72B2", "STRICT_EXCLUSION"): 55216, ("C74", "STRICT_EXCLUSION"): 25559, ("C74", "CEMETERY_TANGENCY_TERMINAL"): 17367, ("C75", "CEMETERY_TANGENCY_TERMINAL"): 5884, ("C72O", "STRICT_EXCLUSION"): 18668, ("C73V2", "STRICT_EXCLUSION"): 1163, ("C76", "STRICT_EXCLUSION"): 10298}
    require(dict(census) == expected and len(dispositions) == 134155, "oracle exact partition")
    return {"kind": kind, "c69row": c69row, "c71": c71, "atlas": atlas, "dispositions": dispositions, "census": census}


def verify_candidate_rows(stage: Path, chain: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    actual_children = candidate_rows(stage, f"{BASE}_child_dispositions.jsonl.gz")
    require(len(actual_children) == 167255, "candidate child count")
    source_stats: dict[str, Counter] = defaultdict(Counter)
    pair_residual = Counter(); pair_block = Counter(); pair_cemetery = Counter()
    first_by_disposition = {}
    for ordinal, (child, actual) in enumerate(zip(chain["child_order"], actual_children), 1):
        c = chain["children"][child]["row"]; source = chain["children"][child]["source"]; source_kind = decision["kind"][source]
        if source_kind == "DECISION":
            disposition = "RESIDUAL_SEALED_NEXT_DECIDER_REQUIRED"; oracle = "NONE_C71_H1_ONLY"; oracle_row = None; atlas_row = None
            source_stats[source]["residual"] += 1; pair_residual[c["pair_index"]] += 1
        else:
            oracle, oracle_row, disposition = decision["dispositions"][child]; atlas_row = decision["atlas"][child]["row_sha256"]
            source_stats[source]["blocker_terminal"] += 1; source_stats[source][disposition] += 1; pair_block[c["pair_index"]] += 1
            if disposition == "CEMETERY_TANGENCY_TERMINAL": pair_cemetery[c["pair_index"]] += 1
        expected = with_row_hash({"schema": "cm2.round306c77s.singleton-parent-no-producer-consumer.v1.child-disposition-row", "ordinal": ordinal, "pair_index": c["pair_index"], "source_path": c["source_path"], "child_path": c["path"], "parent_volume_fraction": c["parent_volume_fraction"], "C61_source_row_sha256": source, "C65_child_row_sha256": child, "C71b_H1_row_sha256": decision["c71"][child], "C72_atlas_row_sha256": atlas_row, "C69c_source_kind": source_kind, "consuming_oracle": oracle, "consuming_oracle_row_sha256": oracle_row, "disposition": disposition, "terminal_predicate_present": source_kind == "BLOCKER", "formal_credit": 0, "D02_gate_credit": 0, "whole_parent_credit": 0, "global_unresolved_decrement": 0})
        require(actual == expected, f"candidate child reconstruction {ordinal}")
        first_by_disposition.setdefault(disposition, expected)
    actual_sources = candidate_rows(stage, f"{BASE}_source_rollups.jsonl.gz")
    require(len(actual_sources) == 20879, "candidate source count")
    source_census = Counter()
    for ordinal, (source, actual) in enumerate(zip(chain["source_order"], actual_sources), 1):
        src = chain["sources"][source]; s = src["summary"]; source_kind = decision["kind"][source]; stats = source_stats[source]
        residual = stats["residual"]; terminal = residual == 0; source_census[(source_kind, "TERMINAL" if terminal else "RESIDUAL")] += 1
        selected = sum((fraction(chain["children"][h]["row"]["parent_volume_fraction"]) for h in src["children"]), Fraction())
        total = src["carry_volume"] + selected
        expected = with_row_hash({"schema": "cm2.round306c77s.singleton-parent-no-producer-consumer.v1.source-rollup-row", "ordinal": ordinal, "pair_index": s["pair_index"], "source_path": s["source_path"], "C61_source_row_sha256": source, "C65_source_summary_row_sha256": s["row_sha256"], "C69c_source_row_sha256": decision["c69row"][source], "C69c_source_kind": source_kind, "C65_strict_terminal_carry_leaf_count": src["carry"], "selected_collision2_child_count": len(src["children"]), "selected_blocker_terminal_child_count": stats["blocker_terminal"], "selected_decision_residual_child_count": residual, "selected_child_Kraft": str(selected), "C65_strict_terminal_carry_Kraft": str(src["carry_volume"]), "full_source_Kraft": str(total), "source_prefix_free_and_Kraft_closed": True, "whole_source_terminal": terminal, "residual_reason": None if terminal else "C71B_H1_FULL_BOX_CLOSURE_HAS_NO_FROZEN_DOWNSTREAM_TERMINAL_PREDICATE", "formal_credit": 0, "D02_gate_credit": 0, "whole_parent_credit": 0})
        require(actual == expected, f"candidate source reconstruction {ordinal}")
    actual_pairs = candidate_rows(stage, f"{BASE}_reflection_pair_rollups.jsonl.gz")
    require(len(actual_pairs) == 12, "candidate pair count")
    pair_terminal = {}
    for p, actual in zip(PAIR_IDS, actual_pairs):
        c = chain["counts"][p]; v = chain["volumes"][p]; leaves = chain["final"][p]
        expected = with_row_hash({"schema": "cm2.round306c77s.singleton-parent-no-producer-consumer.v1.pair-rollup-row", "pair_index": p, "reflection_cell_count": 2, "C69c_source_task_count": sum(1 for s in chain["sources"].values() if s["summary"]["pair_index"] == p), "final_prefix_leaf_count": len(leaves), "C57_strict_terminal_carry_leaf_count": c["C57_STRICT_CARRY"], "C58_strict_terminal_carry_leaf_count": c["C58_STRICT_CARRY"], "C61_strict_terminal_carry_leaf_count": c["C61_STRICT_CARRY"], "C65_replacement_leaf_count": c["C65_REPLACEMENT"], "C57_strict_terminal_carry_Kraft": str(v["C57_STRICT_CARRY"]), "C58_strict_terminal_carry_Kraft": str(v["C58_STRICT_CARRY"]), "C61_strict_terminal_carry_Kraft": str(v["C61_STRICT_CARRY"]), "C65_replacement_Kraft": str(v["C65_REPLACEMENT"]), "frozen_parent_row_sha256": chain["parents"][p], "blocker_terminal_child_count": pair_block[p], "cemetery_graph_child_count": pair_cemetery[p], "decision_residual_child_count": pair_residual[p], "parent_prefix_free": True, "parent_Kraft": "1", "whole_reflection_pair_terminal": pair_residual[p] == 0, "formal_credit": 0, "D02_gate_credit": 0, "whole_parent_credit": 0})
        require(actual == expected, f"candidate pair reconstruction {p}")
        pair_terminal[p] = pair_residual[p] == 0
    components = set()
    for row in upstream_rows("deliverables/cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz"):
        if row["cell_count"] == 1:
            require(row["known_sheet_anchor"] is None and row["whole_component_terminal_class"] is None, "singleton baseline")
            components.add(row["component_id"])
    cells = []
    for row in upstream_rows("deliverables/cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz"):
        if row["component_id"] in components:
            require(row["current_effective_disposition"] == "UNRESOLVED_R1648_CONTINUATION", "singleton baseline disposition")
            cells.append(row)
    by_pair = defaultdict(list)
    for row in cells: by_pair[row["pair_index"]].append(row)
    actual_cells = candidate_rows(stage, f"{BASE}_singleton_cell_rollups.jsonl.gz")
    expected_cells = []
    for p in PAIR_IDS:
        pair_cells = sorted(by_pair[p], key=lambda x: x["cell_id"])
        require(len(pair_cells) == 2 and pair_cells[0]["reflection_partner_cell_id"] == pair_cells[1]["cell_id"] and pair_cells[1]["reflection_partner_cell_id"] == pair_cells[0]["cell_id"], "reflection bijection")
        for row in pair_cells:
            expected_cells.append(with_row_hash({"schema": "cm2.round306c77s.singleton-parent-no-producer-consumer.v1.singleton-cell-rollup-row", "component_index": row["component_index"], "component_id": row["component_id"], "cell_id": row["cell_id"], "reflection_partner_cell_id": row["reflection_partner_cell_id"], "pair_index": p, "origin_key": row["origin_key"], "blocker_terminal_child_count_on_reflection_pair": pair_block[p], "decision_residual_child_count_on_reflection_pair": pair_residual[p], "candidate_whole_cell_terminal": pair_terminal[p], "candidate_terminal_class": "STRICT_EXCLUSION_OR_CEMETERY_STRATIFIED_BY_FROZEN_CHILD_PARTITION" if pair_terminal[p] else None, "residual_reason": None if pair_terminal[p] else "DECISION_SOURCE_CHILDREN_REQUIRE_FROZEN_DOWNSTREAM_ROUTE_DECIDER", "candidate_public_unresolved_decrement": 0, "formal_credit": 0, "D02_gate_credit": 0, "whole_parent_credit": 0}))
    require(actual_cells == expected_cells and len(actual_cells) == 24, "candidate singleton cell reconstruction")
    return {"children": actual_children, "sources": actual_sources, "pairs": actual_pairs, "cells": actual_cells, "first": first_by_disposition, "source_census": source_census, "pair_terminal": pair_terminal}


def incidence_reconstruction() -> dict[str, Any]:
    def roots(rel: str, expected: dict[int, int]) -> tuple[dict[str, Any], dict[tuple[str, str], tuple[str, tuple[str, ...], str]]]:
        degree = Counter(); boundary = 0; shared = {}; occurrences = 0; total = 0
        for row in upstream_rows(rel):
            total += 1; d = row["incidence_count"]; degree[d] += 1; occurrences += d
            require(d in (1, 2) and len(row["target_graph_endpoint_occurrences"]) == d, "root degree")
            require(row["incidence_closed"] and row["unique_half_open_dyadic_face_owner"] and row["root_is_graph_endpoint_not_physical_terminal"], "root incidence")
            if d == 1 and row["atlas_face_incidence_class"] == "SHARED_FACE":
                require(row["atlas_face_incidence_count"] == 2 and len(row["incident_C72_atlas_faces"]) == 2, "shared root")
                key = (row["root_id"], row["face_key_sha256"])
                shared[key] = (digest(compact(row["exact_face"])), tuple(x["C72_atlas_row_sha256"] for x in row["incident_C72_atlas_faces"]), row["unique_half_open_dyadic_face_owner"]["C72_atlas_row_sha256"])
            elif d == 1:
                require(row["atlas_face_incidence_class"] == "ATLAS_SCOPE_BOUNDARY_FACE" and row["atlas_face_incidence_count"] == 1, "boundary root")
                boundary += 1
        require(dict(degree) == expected, "root degree census")
        return {"unique_physical_root_count": total, "endpoint_occurrence_count": occurrences, "degree_census": {str(k): v for k, v in sorted(degree.items())}, "degree_one_shared_face_count": len(shared), "degree_one_atlas_scope_boundary_authority_count": boundary, "degree_one_is_classified_half_open_owner_not_dangling": True}, shared
    a, ashared = roots(".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_root_incidence.jsonl.gz", {1: 18098, 2: 46164})
    b, bshared = roots(".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1_root_incidence.jsonl.gz", {1: 17370, 2: 1613})
    require(len(ashared) == 15841 and ashared == bshared, "C72b2/C76 reciprocal roots")
    cross = {}; c74 = Counter()
    for row in upstream_rows(".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1_endpoint_incidence.jsonl.gz"):
        kind = row["incidence_class"]; c74[kind] += 1
        if kind == "ADJACENT_C72_CROSS_SCOPE_GLUE":
            adj = row["consumer"]["adjacent_C72_face"]; face = row["exact_face"]
            key = (adj["C72_atlas_row_sha256"], face["pair_index"], row["collision1_target"], face["fixed_axis"], face["fixed_value"], tuple(face["varying_interval"]))
            require(key not in cross, "C74 physical duplicate")
            cross[key] = (row["C72_atlas_row_sha256"], digest(compact({"pair_index": face["pair_index"], "collision1_target": row["collision1_target"], "equation": "CENTERED_COLLISION1_DISCRIMINANT_EQUALS_ZERO", "exact_s": "0", "exact_t": face["fixed_value"], "exact_p_interval": face["varying_interval"]})))
    require(c74 == {"PAIRED_INTERNAL_C74_ENDPOINT": 22976, "ADJACENT_C72_CROSS_SCOPE_GLUE": 11750, "SOURCE_CELL_BOUNDARY_CONSUMER": 8}, "C74 incidence census")
    c75 = Counter(); seen = set(); owners = defaultdict(list)
    for row in upstream_rows(".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_endpoint_incidence.jsonl.gz"):
        require(row["dangling"] is False and row["duplicate_occurrence"] is False, "C75 incidence")
        owner = row["adjacency_and_half_open_owner"]; kind = owner["incidence_kind"]; c75[kind] += 1
        if kind == "OUT_OF_SCOPE_C72_DOWNSTREAM_OWNER":
            face = row["exact_face_key"]; target = row["root_identity_preimage"]["tangency_target"]
            key = (row["C72_obligation_row_sha256"], row["pair_index"], target, face["face_axis"], face["exact_t"], tuple(face["exact_p_interval"]))
            require(key in cross and key not in seen and cross[key][0] == owner["neighbor_C72_obligation_row_sha256"], "C74/C75 reciprocal occurrence")
            physical = digest(compact({"pair_index": row["pair_index"], "collision1_target": target, "equation": "CENTERED_COLLISION1_DISCRIMINANT_EQUALS_ZERO", "exact_s": "0", "exact_t": face["exact_t"], "exact_p_interval": face["exact_p_interval"]}))
            require(physical == cross[key][1], "C74/C75 physical digest"); seen.add(key)
        elif kind == "IN_SCOPE_MATCHED_TANGENCY_SEGMENT":
            owners[row["root_id"]].append(owner["current_occurrence_is_half_open_owner"])
    require(c75 == {"OUT_OF_SCOPE_C72_DOWNSTREAM_OWNER": 11750, "IN_SCOPE_MATCHED_TANGENCY_SEGMENT": 16, "C32_ATLAS_CELL_BOUNDARY_OWNER": 1, "C32_ATLAS_OUTER_GUARD_BOUNDARY_TERMINAL": 1}, "C75 incidence census")
    require(seen == set(cross) and len(owners) == 8 and all(len(v) == 2 and sum(v) == 1 for v in owners.values()), "C74/C75 exhaustive owners")
    return {"C72B2_physical_H1_graph_roots": a, "C76_physical_H1_graph_roots": b, "C72B2_C76_reciprocal_shared_face_half_open_owner_count": 15841, "C72B2_C76_reciprocal_shared_face_root_face_owner_identity": True, "C74_endpoint_incidence_census": dict(sorted(c74.items())), "C75_endpoint_incidence_census": dict(sorted(c75.items())), "C74_C75_reciprocal_cross_scope_occurrences": 11750, "C74_C75_canonical_physical_face_root_occurrence_multisets_equal": True, "C74_source_boundary_occurrences": 8, "C75_C32_or_outer_boundary_occurrences": 2, "face_corner_source_seam_incidence_closed": True}


def validate_result(common: dict[str, bytes], rebuilt: dict[str, Any], incidence: dict[str, Any]) -> dict[str, Any]:
    result = parse(common[f"{BASE}_result.json"])
    require(result["producer_file_sha256"] == PRODUCER_DECLARATION_SHA256, "declared producer hash")
    require(all(v is False for v in result["upstream_producer_policy"].values()), "producer policy")
    require(result["partition"] == {"total_collision2_handoff_children": 167255, "decision_source_children": 33100, "blocker_source_children": 134155, "identity": "167255=33100+134155"}, "result partition")
    require(result["blocker_terminal_census"]["whole_child_strict_exclusion"] == 110904 and result["blocker_terminal_census"]["cemetery_tangency_terminal"] == 23251 and result["blocker_terminal_census"]["residual"] == 0, "result blocker closure")
    require(result["decision_source_disposition"]["residual"] == 33100 and result["decision_source_disposition"]["frozen_downstream_terminal_predicate_present"] == 0, "result decision residual")
    require(result["reflection_pairs"] == {"total": 12, "candidate_whole_terminal": 4, "residual": 8, "prefix_free_and_Kraft_one": 12}, "result pairs")
    require(result["singleton_cells"] == {"total": 24, "candidate_whole_terminal": 8, "residual": 16, "atomic_install_condition": "24_OF_24_REQUIRED"}, "result cells")
    require(result["candidate_public_unresolved_decrement"] == 0 and result["candidate_public_unresolved_after"] == result["public_global_unresolved_before"] == 1148, "result unresolved")
    require(all(v == 0 for v in result["credit_boundary"].values()) and result["canonical_pointer_or_seal_written"] is False, "result zero credit")
    for key, name in [("child_dispositions", f"{BASE}_child_dispositions.jsonl.gz"), ("source_rollups", f"{BASE}_source_rollups.jsonl.gz"), ("reflection_pair_rollups", f"{BASE}_reflection_pair_rollups.jsonl.gz"), ("singleton_cell_rollups", f"{BASE}_singleton_cell_rollups.jsonl.gz")]:
        require(result["ledgers"][key]["sha256"] == BASE_PINS[name] and result["ledgers"][key]["row_count"] == len(rebuilt[{"child_dispositions": "children", "source_rollups": "sources", "reflection_pair_rollups": "pairs", "singleton_cell_rollups": "cells"}[key]]), "result ledger descriptor")
    expected_incidence = with_object_hash({"schema": "cm2.round306c77s.singleton-parent-no-producer-consumer.v1.incidence-audit", **incidence, "formal_credit": 0, "D02_gate_credit": 0, "global_installed_credit": 0})
    actual_incidence = parse(common[f"{BASE}_incidence_audit.json"])
    require(actual_incidence == expected_incidence and result["incidence_audit_object_sha256"] == expected_incidence["object_sha256"], "candidate incidence reconstruction")
    return result


def run_attacks(result: dict[str, Any], rebuilt: dict[str, Any], incidence: dict[str, Any], common: dict[str, bytes]) -> dict[str, Any]:
    rejected = {}
    def expect(name: str, fn) -> None:
        try:
            fn()
        except (Reject, OSError, ValueError, KeyError, TypeError, AssertionError):
            rejected[name] = "FAIL_CLOSED"
        else:
            raise Reject(f"attack accepted: {name}")
    def exact(actual, expected): require(actual == expected, "independent exact reconstruction mismatch")
    mutations = [
        ("partition_total", ("partition", "total_collision2_handoff_children"), 167254), ("partition_decision", ("partition", "decision_source_children"), 33099),
        ("partition_blocker", ("partition", "blocker_source_children"), 134156), ("strict_census", ("blocker_terminal_census", "whole_child_strict_exclusion"), 110903),
        ("cemetery_census", ("blocker_terminal_census", "cemetery_tangency_terminal"), 23250), ("blocker_residual", ("blocker_terminal_census", "residual"), 1),
        ("decision_residual", ("decision_source_disposition", "residual"), 33099), ("fake_terminal_predicate", ("decision_source_disposition", "frozen_downstream_terminal_predicate_present"), 1),
        ("pair_terminal", ("reflection_pairs", "candidate_whole_terminal"), 5), ("pair_kraft", ("reflection_pairs", "prefix_free_and_Kraft_one"), 11),
        ("cell_terminal", ("singleton_cells", "candidate_whole_terminal"), 9), ("cell_atomic_condition", ("singleton_cells", "atomic_install_condition"), "8_OF_24"),
        ("unresolved_decrement", ("candidate_public_unresolved_decrement",), 24), ("unresolved_after", ("candidate_public_unresolved_after",), 1124),
        ("formal_credit", ("credit_boundary", "formal_credit"), 1), ("D02_credit", ("credit_boundary", "D02_gate_credit"), 1),
        ("CM2_credit", ("credit_boundary", "CM2_credit"), 1), ("global_credit", ("credit_boundary", "global_installed_credit"), 1),
        ("whole_parent_credit", ("credit_boundary", "whole_parent_credit"), 1), ("canonical_seal", ("canonical_pointer_or_seal_written",), True),
    ]
    for name, path, value in mutations:
        altered = copy.deepcopy(result); cursor = altered
        for key in path[:-1]: cursor = cursor[key]
        cursor[path[-1]] = value
        expect(name, lambda a=altered: exact(a, result))
    row_attacks = []
    for label, disposition in [("decision", "RESIDUAL_SEALED_NEXT_DECIDER_REQUIRED"), ("strict", "STRICT_EXCLUSION"), ("cemetery", "CEMETERY_TANGENCY_TERMINAL")]:
        row = rebuilt["first"][disposition]
        for field, value in [("formal_credit", 1), ("D02_gate_credit", 1), ("whole_parent_credit", 1), ("global_unresolved_decrement", 1), ("child_path", row["child_path"] + "0"), ("C65_child_row_sha256", "0" * 64), ("C71b_H1_row_sha256", "1" * 64), ("terminal_predicate_present", not row["terminal_predicate_present"]), ("disposition", "SEALED_COLLISION3_HANDOFF")]:
            bad = dict(row); bad[field] = value
            row_attacks.append((f"{label}_{field}", bad, row))
    for name, bad, good in row_attacks:
        expect(name, lambda b=bad, g=good: exact(b, g))
    pair = rebuilt["pairs"][0]
    for field, value in [("parent_Kraft", "255/256"), ("parent_prefix_free", False), ("C57_strict_terminal_carry_leaf_count", pair["C57_strict_terminal_carry_leaf_count"] - 1), ("decision_residual_child_count", pair["decision_residual_child_count"] + 1), ("frozen_parent_row_sha256", {})]:
        bad = dict(pair); bad[field] = value; expect(f"pair_{field}", lambda b=bad, g=pair: exact(b, g))
    cell = rebuilt["cells"][0]
    for field, value in [("candidate_public_unresolved_decrement", 1), ("formal_credit", 1), ("reflection_partner_cell_id", cell["cell_id"]), ("candidate_whole_cell_terminal", not cell["candidate_whole_cell_terminal"])]:
        bad = dict(cell); bad[field] = value; expect(f"cell_{field}", lambda b=bad, g=cell: exact(b, g))
    bad_inc = copy.deepcopy(incidence); bad_inc["C72B2_C76_reciprocal_shared_face_half_open_owner_count"] -= 1
    expect("incidence_shared_root_loss", lambda: exact(bad_inc, incidence))
    bad_inc = copy.deepcopy(incidence); bad_inc["C74_C75_reciprocal_cross_scope_occurrences"] -= 1
    expect("incidence_cross_scope_loss", lambda: exact(bad_inc, incidence))
    expect("candidate_byte_drift", lambda: require(common[f"{BASE}_result.json"][:-1] == common[f"{BASE}_result.json"], "byte drift"))
    expect("noncanonical_json", lambda: parse(b'{"b":1,"a":2}'))
    expect("duplicate_json_key", lambda: parse(b'{"a":1,"a":2}'))
    gz = io.BytesIO()
    with gzip.GzipFile(fileobj=gz, mode="wb", mtime=0) as z: z.write(b"{}\n")
    expect("multiple_gzip_members", lambda: one_member(gz.getvalue() + gz.getvalue()))
    expect("trailing_gzip_bytes", lambda: one_member(gz.getvalue() + b"x"))
    expect("producer_source_path", lambda: safe_read_path(ROOT / "deliverables" / PRODUCER_BASENAME))
    scratch = Path(tempfile.mkdtemp(prefix="c77s-attack-", dir=ROOT / ".cm2-runtime"))
    try:
        base = scratch / "base"; base.write_bytes(b"x")
        symlink = scratch / "symlink"; symlink.symlink_to(base)
        hardlink = scratch / "hardlink"; os.link(base, hardlink)
        expect("nofollow_symlink", lambda: safe_read_path(symlink))
        expect("single_link_required", lambda: safe_read_path(base))
    finally:
        for path in scratch.iterdir(): path.unlink()
        scratch.rmdir()
    require(len(rejected) >= 60 and len(rejected) == len(set(rejected)), "attack coverage")
    return {"attack_count": len(rejected), "rejected": len(rejected), "results": dict(sorted(rejected.items())), "status": f"PASS_{len(rejected)}_OF_{len(rejected)}_COHERENT_FILE_POLICY_ATTACKS_FAIL_CLOSED"}


def write_exclusive(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o444)
    try:
        view = memoryview(raw)
        while view:
            view = view[os.write(fd, view):]
        os.fsync(fd)
    finally:
        os.close(fd)


def verifier_source_sha() -> str:
    path = Path(__file__).resolve()
    require(path.name == "cm2_round306c77s_singleton_parent_no_producer_consumer_independent_verifier_v1.py", "verifier self path")
    return digest(safe_read_path(path))


def finalize(a: Path, b: Path, verification: dict[str, Any]) -> dict[str, Any]:
    verification = with_object_hash(verification)
    verify_raw = compact(verification) + b"\n"
    for stage in (a, b): write_exclusive(stage / VERIFY_NAME, verify_raw)
    require(safe_read_path(a / VERIFY_NAME, digest(verify_raw)) == safe_read_path(b / VERIFY_NAME, digest(verify_raw)), "verification dual bytes")
    members = dict(BASE_PINS); members[VERIFY_NAME] = digest(verify_raw)
    # Preserve the exact base publication order, then append independent
    # verification as the final pre-manifest member.
    manifest_raw = b"".join(f"{pin}  {name}\n".encode() for name, pin in members.items())
    for stage in (a, b): write_exclusive(stage / FINAL_MANIFEST, manifest_raw)
    # Recapture all pre-outer members in both stages before the final outer.
    for name, pin in {**members, FINAL_MANIFEST: digest(manifest_raw)}.items():
        require(safe_read_path(a / name, pin) == safe_read_path(b / name, pin), f"preouter dual replay {name}")
    outer = with_object_hash({"schema": SCHEMA + ".final-outer-receipt", "status": "PASS_DUAL_ISOLATED_BYTE_IDENTICAL__INDEPENDENT_NO_PRODUCER_RECONSTRUCTION__FINAL_OUTER_LAST__ZERO_CREDIT", "candidate_is_authority": False, "producer_file_sha256_declaration_only": PRODUCER_DECLARATION_SHA256, "producer_source_opened_read_parsed_decoded_imported_compiled_or_executed": False, "verification_filename": VERIFY_NAME, "verification_file_sha256": digest(verify_raw), "verification_object_sha256": verification["object_sha256"], "final_manifest_filename": FINAL_MANIFEST, "final_manifest_file_sha256": digest(manifest_raw), "final_manifest_member_count": len(members), "final_manifest_order": list(members), "base_outer_was_last_in_base_publication": True, "base_outer_receipt_role": "VALID_CANDIDATE_STAGE_RECEIPT_SUPERSEDED_ONLY_FOR_FINAL_BUNDLE_ORDERING_NOT_INVALIDATED_OR_DELETED", "append_only_finalization_supersedes_base_outer_last_scope": True, "final_outer_receipt_published_last_in_each_stage": True, "terminal_byte_replay_member_count_per_stage": len(members) + 2, "all_final_members_terminal_byte_replayed_in_both_stages": True, "all_final_stage_bytes_identical": True, "candidate_public_unresolved_decrement": 0, "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0, "global_installed_credit": 0, "whole_parent_credit": 0})
    outer_raw = compact(outer) + b"\n"
    for stage in (a, b): write_exclusive(stage / FINAL_OUTER, outer_raw)
    all_members = {**members, FINAL_MANIFEST: digest(manifest_raw), FINAL_OUTER: digest(outer_raw)}
    for name, pin in all_members.items():
        require(safe_read_path(a / name, pin) == safe_read_path(b / name, pin), f"terminal dual replay {name}")
    require({p.name for p in a.iterdir()} == set(all_members) and {p.name for p in b.iterdir()} == set(all_members), "final member set")
    return {"verification_file_sha256": digest(verify_raw), "verification_object_sha256": verification["object_sha256"], "final_manifest_file_sha256": digest(manifest_raw), "final_outer_file_sha256": digest(outer_raw), "final_outer_object_sha256": outer["object_sha256"], "final_member_count": len(all_members)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage-a", required=True)
    parser.add_argument("--stage-b", required=True)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    a = Path(args.stage_a); b = Path(args.stage_b)
    if not a.is_absolute(): a = ROOT / a
    if not b.is_absolute(): b = ROOT / b
    require(ROOT in a.parents and ROOT in b.parents, "stages below workspace")
    common = validate_base_stages(a, b)
    # Pin the C65 v9 release without opening any manifest-listed producer.
    c65_manifest = upstream("deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256")
    require(len(c65_manifest.decode("ascii").splitlines()) == 446, "C65 v9 manifest 446")
    c65_test = parse(upstream("deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json"))
    c65_outer = parse(upstream("deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json"))
    require(c65_test["test_count"] == 134 and all(c65_test["tests"].values()), "C65 v9 134/134")
    require(c65_outer["manifest_member_count"] == 446 and c65_outer["outer_receipt_published_last"] is True, "C65 v9 outer")
    chain = reconstruct_frontier()
    decision = reconstruct_dispositions(chain)
    rebuilt = verify_candidate_rows(a, chain, decision)
    incidence = incidence_reconstruction()
    result = validate_result(common, rebuilt, incidence)
    attacks = run_attacks(result, rebuilt, incidence, common)
    verification = {"schema": SCHEMA, "status": "PASS_FULL_167255_CHILD_RECONSTRUCTION__134155_BLOCKER_TERMINALS__33100_DECISION_RESIDUAL__12_PAIR_KRAFT__8_OF_24_CELL_CANDIDATES__DECREMENT_ZERO", "candidate_is_authority": False, "producer_file_sha256_declaration_only": PRODUCER_DECLARATION_SHA256, "producer_source_policy": {"opened": False, "read": False, "parsed": False, "decoded": False, "imported": False, "compiled": False, "executed": False}, "verifier_file_sha256": verifier_source_sha(), "dual_isolated_candidate_builds": {"base_member_count": len(BASE_PINS), "all_base_members_byte_identical": True, "stage_a": str(a.relative_to(ROOT)), "stage_b": str(b.relative_to(ROOT))}, "C65_v9": {"manifest_members": 446, "hostile_self_test": "134/134", "outer_last": True}, "reconstruction": {"children": 167255, "decision_residual": 33100, "blocker_terminal": 134155, "whole_child_strict_exclusion": 110904, "cemetery_tangency_terminal": 23251, "sources": 20879, "source_census": {f"{k[0]}_{k[1]}": v for k, v in sorted(rebuilt["source_census"].items())}, "reflection_pairs": 12, "pair_prefix_free_and_exact_Kraft_one": 12, "candidate_whole_terminal_pairs": sum(rebuilt["pair_terminal"].values()), "singleton_cells": 24, "candidate_whole_terminal_cells": sum(x["candidate_whole_cell_terminal"] for x in rebuilt["cells"]), "atomic_singleton_decrement": 0}, "incidence": incidence, "coherent_attacks": attacks, "credit_boundary": {"formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0, "global_installed_credit": 0, "whole_parent_credit": 0, "candidate_public_unresolved_decrement": 0}, "canonical_pointer_or_seal_written": False}
    if not args.emit:
        print(compact({"status": "PASS_AUDIT_ONLY_NO_WRITES", "attacks": attacks["status"], "producer_source_read": False, "candidate_public_unresolved_decrement": 0}).decode())
        return
    for stage in (a, b):
        for name in (VERIFY_NAME, FINAL_MANIFEST, FINAL_OUTER): require(not (stage / name).exists(), "append-only final target exists")
    completion = finalize(a, b, verification)
    print(compact({"status": "PASS", "attacks": attacks["status"], **completion}).decode())


if __name__ == "__main__":
    main()
