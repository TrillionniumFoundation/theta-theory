#!/usr/bin/env python3
"""Append-only, zero-credit singleton-parent consumer over frozen evidence bytes.

This program deliberately never opens, imports, decodes, compiles, or executes an
upstream producer.  It consumes only published ledgers, results, manifests,
receipts, and independent-verification objects.  C65's 446-member manifest is
parsed and pinned as an attested snapshot; its member sources are not opened.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import stat
import zlib
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
SCHEMA = "cm2.round306c77s.singleton-parent-no-producer-consumer.v1"
BASE = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1"
PAIR_IDS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)

# Immutable anchors.  Dual stage-B files are required to equal their pinned A
# counterpart byte-for-byte and are therefore not repeated here.
PINS = {
    "deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_leaf_ledger_v1.jsonl.gz": "918899a914ad4fbb05c1095cac9f42f6c46d02f0acdad366538a395021aeaee6",
    "deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_parent_ledger_v1.jsonl.gz": "8817069967798042bd87315f57e7c3cea279c6564c0e50a5ac927ca4f765e510",
    "deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_result_v1.json": "9881c22ac4a8630b90b8eb16d81c1670bb6f544e5f4666197d0e6047771d8c4c",
    "deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_independent_verification_v1.json": "e1c9849aed542eebdb83856446eba0325af35211c8a9ce714f991b0385918d15",
    "deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_manifest_v1.sha256": "4427e1376811454ad3b6ec5478c1687064cea81f5d33ebd0c13284952928ced0",
    "deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256": "96b0f082688f16f821104402bc9aba1b7778df36f084a300d978dac95faf43c5",
    "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json": "20a52a4c16c84ffd524833c0ee872edfeb6fdec538a1368f619244199814fb1d",
    "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v9.json": "c7d99ba4fea05fbd7a3b478f025323c77e5335951e4ff08743ad37ba47fa8e85",
    "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json": "f0609dc4835346e078b5299007b1b31210d28cbf772ac41bb0f390f7047ad274",
    "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v9.json": "7d4e97bd641da7c5ccc64e8c2ad3d59f21ba3ebd73eb0e4d55c88ad617ee23b4",
    "deliverables/cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json": "1ca46fb81cc104b727b31d3bb0adbb439ab8dae9123b8cbe05d3c60de0e75457",
    "deliverables/cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz": "4ff1c36a0a6331510da3afb988738f128a3cada04ddd297ac58584579115437d",
    "deliverables/cm2_round306c65s18_depth18_64shard_aggregate_source_summary_v1.jsonl.gz": "de8fa908cbe46e379ff05564c5d8ed0ea97de2875eca05792ad3abf63287f432",
    "deliverables/cm2_round306c65s18_depth18_64shard_aggregate_parent_summary_v1.jsonl.gz": "91adb1e9e5e7e7dfdc1cbf674d5713d218851a4b5f15602ced2664972280bc4b",
    "deliverables/cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
    "deliverables/cm2_round306c61s12_depth12_16shard_aggregate_parent_summary_v4.jsonl.gz": "2206c817f49312c519a720e14bc2e152cde5362ed884cbe83d32349a7ff5bab2",
    "deliverables/cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_handoff_summary_v1.jsonl.gz": "d7fa7095dfc5c44d699adf30e19971ddc0be722ddddaf096e0ece0d9bc6cec9c",
    "deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_parent_summary_v1.jsonl.gz": "6f3a8fa4501cb872a33d7446a14d804eeb352bb6d049158f3c7ee88893b7872d",
    "deliverables/cm2_round306c69b_singleton_h1_graph_slab_decider_v2_decisions.jsonl.gz": "b9bc1cd359c77ee6a5246011925090e5d5557cd88e90d1f5c67fa70a452d1eba",
    "deliverables/cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz": "69b3ec294f95cb5ce377e553ae875daab10a5bdb33e860363f6bae122022e606",
    "deliverables/cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json": "607fc73ebe3333ca172eb15c0831b8c3d98192c86e20eec7a59a69c4ae4737d4",
    "deliverables/cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json": "b0490ed50de8d615039d864db1071792df0809b928a663fcd4a89981eaf326b6",
    ".cm2-runtime/c71b-v3-final-75c21279/cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_rows.jsonl.gz": "f9f04044809e46b9811d52abef94844d84b058a2f0c3fb6f5b9f97f2302cbec6",
    ".cm2-runtime/c71b-v3-final-75c21279/cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_result.json": "5ede807e4860b60fe8582597cc6be10cdfdc7b3a0eeba57ced317f4980092246",
    ".cm2-runtime/c71b-v3-final-75c21279/independent_verification_v3_1.json": "ee105922e263d9cea551088ee67c350cc9adc4d9f375a8584428e4fa55575612",
    ".cm2-runtime/c71b-v3-final-75c21279/dual_build_publication_completion_receipt_v3.json": "3a6cfa624fab8cd1b787d3facd139cf9e055a008236864d894d2633522fe9fbc",
    ".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz": "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370",
    ".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_v1_result.json": "55318b7c3ee778cb8a0e41d612c9c2caa44790e6fff816a6104116268258f01e",
    ".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json": "63105e380d37d49bd655e094d41e15d3ed0d182380a44a4a16709ba3308edaf0",
    ".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2.jsonl.gz": "58f876b6f926e152efbd695651af0505d73b74dbfe57aa7dc169887bd082b3b2",
    ".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_root_incidence.jsonl.gz": "840efb65d45175d5f0449becfbe6260167188b2b7a9c1e5560549d4f66c4ae8d",
    ".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_result.json": "0c8c56a86d3293dd08bc1fef95a72fe0aedc3a35edb20ff0ec9c6e19cd69d1f3",
    ".cm2-runtime/c72b2-independent-a.v2-3212bb3d.json": "21988ad9b5d746495489e506fadfdf537848eeae6a788a64c6bca3b11c2c9252",
    ".cm2-runtime/c72b2-completion-outer-receipt.v2-a53e5319.json": "e0d6da2518d48278a42ffea5e6a676b11001d531e971fdc59da39f3b524dec62",
    ".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1.jsonl.gz": "3c636d4e2151203eced98d514567d47bc50aaed83aeadf0454da7c6a1aae6772",
    ".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1_endpoint_incidence.jsonl.gz": "1b35ef3cde3d57fc7ef25f010fdf74089d63a5e5519c7d5a01b80fb01956c2c7",
    ".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1_result.json": "8d2372de67a5ed0d87a6699845778c9e4d05e183cd21b599a3fd6287032e27b1",
    ".cm2-runtime/c74-audit-a.cazCPb/cm2_round306c74_exact_multi_graph_order_oracle_v1_independent_verification_v1.json": "eb4fbefba436ca827a6a60ceb9a3978c496fdbf9798a7eed29333e2067d256cb",
    ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1.jsonl.gz": "e1e30a36f75c2ec71b0c4ec51da33e3c09fb5570426aa356f0c815406e251229",
    ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_endpoint_incidence.jsonl.gz": "db50b71ff364a1f1e132ca0804bd5eb8b027d0c9138f93ee95cfe55e71afb0f2",
    ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_result.json": "1d9d4b2f8b7a4bfb6133ce7b23c22765ef9097c133cc47dc199dd0479f478366",
    ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_independent_verification_v1.json": "8f620e4e7312828dcbcee23cf3f33280c8583bd414ded493b7996b2279131a4c",
    ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_dual_completion_receipt_v1.json": "dbbad4ea8d807b6bcb8b7f121acc57f782925be7e00c9267b9edf011e3eba2b1",
    ".cm2-runtime/c72o-build-a2.v1/cm2_round306c72o_collision1_outgoing_state_oracle_v1.jsonl.gz": "e3125863adcf3ef6489dce741337622b1d70b2ce7655d8d06237c1612ff19355",
    ".cm2-runtime/c72o-build-a2.v1/cm2_round306c72o_collision1_outgoing_state_oracle_v1_result.json": "fd9ca6489f5fedef85fb55de6906a62ecadc417c72d7eb938a6268e7f402302a",
    ".cm2-runtime/c72o-independent-verification-v2.json": "2d34c25b5fd9f2b3a1e8b30d184b40d8a93ffce8c192d193b75715e0d7a68ccb",
    ".cm2-runtime/c73v2-build-a.QOYACE/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2.jsonl.gz": "ed0a3d26f4984e6eced899a01f58aa8329bb1db72b7d0bfb9fe17ee3a4eef6fc",
    ".cm2-runtime/c73v2-build-a.QOYACE/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2_result.json": "5de9d37c69ed4d13d972eff8845ed55ad695ab040d6c1beda01626c0c065c615",
    ".cm2-runtime/c73v2-audit-a.W2AYpD/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_independent_verification_v2.json": "784505135d105fcdf05cc2d6e37779ea896f7d1bbe06e75dd1019b67ae951fe1",
    ".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1.jsonl.gz": "46bb3ac40d5fcadd98463f4de73c404760dd0e5a0ff0a11b48e69a2adbef13b7",
    ".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1_root_incidence.jsonl.gz": "b9e6724c73f051eddcc7bd6fd633fea0ad0346d5f8056712b44c12280d8787b7",
    ".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1_result.json": "8a4be7b059416a88878f26461d38ee39a6b9a8b84b31837b3abcd93ee200f446",
    ".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1_independent_verification_v1.json": "0036b7ec4f18be4c6b488a078e347abafe98f5c7a8a407e5775af965bab4f508",
    ".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1_dual_completion_receipt_v1.json": "4a1774d760cf31ce5d6491e468d74560ababcb1de827f3c735bb9391896a5c92",
    "deliverables/cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz": "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce",
    "deliverables/cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz": "bebc49f66efb01c0b980ec10258a60d7aead9d4d2006d28bdd169c9a9ae38a04",
    "deliverables/cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
}

DUALS = [
    (".cm2-runtime/c72-build-a.ZWGF2f", ".cm2-runtime/c72-build-b.6NX5S7", [
        "cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz",
        "cm2_round306c72_structural_child_obligation_atlas_v1_result.json",
        "cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json"]),
    (".cm2-runtime/c72b2-build-a.v2-3eb4d9c9", ".cm2-runtime/c72b2-build-b.v2-3eb4d9c9", [
        "cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2.jsonl.gz",
        "cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_root_incidence.jsonl.gz",
        "cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_result.json"]),
    (".cm2-runtime/c74-final-a.AzIjhj", ".cm2-runtime/c74-final-b.c56bny", [
        "cm2_round306c74_exact_multi_graph_order_oracle_v1.jsonl.gz",
        "cm2_round306c74_exact_multi_graph_order_oracle_v1_endpoint_incidence.jsonl.gz",
        "cm2_round306c74_exact_multi_graph_order_oracle_v1_result.json"]),
    (".cm2-runtime/c75-build-a2.TG7bbZ", ".cm2-runtime/c75-build-b2.TVSL9k", [
        "cm2_round306c75_first_tangency_exact_strata_oracle_v1.jsonl.gz",
        "cm2_round306c75_first_tangency_exact_strata_oracle_v1_endpoint_incidence.jsonl.gz",
        "cm2_round306c75_first_tangency_exact_strata_oracle_v1_result.json",
        "cm2_round306c75_first_tangency_exact_strata_oracle_v1_independent_verification_v1.json",
        "cm2_round306c75_first_tangency_exact_strata_oracle_v1_dual_completion_receipt_v1.json"]),
    (".cm2-runtime/c72o-build-a2.v1", ".cm2-runtime/c72o-build-b.v1", [
        "cm2_round306c72o_collision1_outgoing_state_oracle_v1.jsonl.gz",
        "cm2_round306c72o_collision1_outgoing_state_oracle_v1_result.json"]),
    (".cm2-runtime/c73v2-build-a.QOYACE", ".cm2-runtime/c73v2-build-b.8OTdPR", [
        "cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2.jsonl.gz",
        "cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2_result.json"]),
    (".cm2-runtime/c76-build-a.final-3284b6ef", ".cm2-runtime/c76-build-b.final-3284b6ef", [
        "cm2_round306c76_full_face_h1_physical_glue_oracle_v1.jsonl.gz",
        "cm2_round306c76_full_face_h1_physical_glue_oracle_v1_root_incidence.jsonl.gz",
        "cm2_round306c76_full_face_h1_physical_glue_oracle_v1_result.json",
        "cm2_round306c76_full_face_h1_physical_glue_oracle_v1_independent_verification_v1.json",
        "cm2_round306c76_full_face_h1_physical_glue_oracle_v1_dual_completion_receipt_v1.json"]),
]


class Reject(RuntimeError):
    pass


CAPTURES: dict[str, dict[str, Any]] = {}


def need(ok: bool, message: str) -> None:
    if not ok:
        raise Reject(message)


def cbytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def object_hash(obj: dict[str, Any]) -> str:
    d = dict(obj)
    d.pop("object_sha256", None)
    return sha(cbytes(d))


def box_hash(box: Any) -> str:
    return sha(cbytes(box))


def parse_json(raw: bytes, *, compact: bool = True) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        d: dict[str, Any] = {}
        for k, v in items:
            need(k not in d, "duplicate JSON key")
            d[k] = v
        return d
    obj = json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(Reject(x)))
    if compact:
        need(raw in (cbytes(obj), cbytes(obj) + b"\n"), "noncanonical JSON")
    if isinstance(obj, dict) and "object_sha256" in obj:
        need(obj["object_sha256"] == object_hash(obj), "object hash mismatch")
    return obj


def read_stable(rel: str, expected: str | None = None) -> bytes:
    path = ROOT / rel
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        a = os.fstat(fd)
        need(stat.S_ISREG(a.st_mode) and a.st_nlink == 1, f"unsafe file: {rel}")
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b)
        bstat = os.fstat(fd)
    finally:
        os.close(fd)
    c = os.stat(path, follow_symlinks=False)
    ident = (a.st_dev, a.st_ino, a.st_mode, a.st_nlink, a.st_size, a.st_mtime_ns)
    need(ident == (bstat.st_dev, bstat.st_ino, bstat.st_mode, bstat.st_nlink, bstat.st_size, bstat.st_mtime_ns), f"TOCTOU fd: {rel}")
    need(ident == (c.st_dev, c.st_ino, c.st_mode, c.st_nlink, c.st_size, c.st_mtime_ns), f"TOCTOU path: {rel}")
    raw = b"".join(chunks)
    digest = sha(raw)
    if expected is not None:
        need(digest == expected, f"pin mismatch: {rel}")
    CAPTURES[rel] = {"sha256": digest, "size": len(raw), "identity": list(ident)}
    return raw


def one_gzip(raw: bytes) -> None:
    d = zlib.decompressobj(16 + zlib.MAX_WBITS)
    for i in range(0, len(raw), 1 << 20):
        d.decompress(raw[i:i + (1 << 20)])
        if d.unused_data:
            raise Reject("gzip multiple member or trailing bytes")
    d.flush()
    need(d.eof and not d.unused_data and not d.unconsumed_tail, "invalid single-member gzip")


def iter_rows(rel: str, expected: str | None = None) -> Iterable[dict[str, Any]]:
    raw = read_stable(rel, expected or PINS.get(rel))
    one_gzip(raw)
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as z:
        ordinal = 0
        for line in z:
            ordinal += 1
            need(line.endswith(b"\n"), f"missing row newline: {rel}:{ordinal}")
            row = parse_json(line[:-1])
            need(isinstance(row, dict) and isinstance(row.get("row_sha256"), str), f"bad row: {rel}:{ordinal}")
            expected_row = row["row_sha256"]
            payload = dict(row)
            payload.pop("row_sha256")
            need(sha(cbytes(payload)) == expected_row, f"row hash: {rel}:{ordinal}")
            yield row


def read_obj(rel: str, expected: str | None = None) -> dict[str, Any]:
    obj = parse_json(read_stable(rel, expected or PINS.get(rel)))
    need(isinstance(obj, dict), f"not object: {rel}")
    return obj


def frac(v: str) -> Fraction:
    return Fraction(v)


def add_row_hash(row: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in row, "row already hashed")
    out = dict(row)
    out["row_sha256"] = sha(cbytes(row))
    return out


def add_object_hash(obj: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in obj, "object already hashed")
    out = dict(obj)
    out["object_sha256"] = sha(cbytes(obj))
    return out


def write_exclusive(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o444)
    try:
        view = memoryview(data)
        while view:
            n = os.write(fd, view)
            view = view[n:]
        os.fsync(fd)
    finally:
        os.close(fd)


def gzip_bytes(rows: list[dict[str, Any]]) -> tuple[bytes, str]:
    raw = b"".join(cbytes(r) + b"\n" for r in rows)
    sink = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=sink, mtime=0) as z:
        z.write(raw)
    hashes = "".join(r["row_sha256"] + "\n" for r in rows).encode()
    return sink.getvalue(), sha(hashes)


def validate_duals() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for a, b, names in DUALS:
        for name in names:
            ar, br = f"{a}/{name}", f"{b}/{name}"
            araw = read_stable(ar, PINS.get(ar))
            braw = read_stable(br, sha(araw))
            need(araw == braw, f"dual mismatch: {ar}")
            out[f"{a}|{b}|{name}"] = sha(araw)
    # Independent audits not located inside both build stages.
    pairs = [
        (".cm2-runtime/c72b2-independent-a.v2-3212bb3d.json", ".cm2-runtime/c72b2-independent-b.v2-3212bb3d.json"),
        (".cm2-runtime/c74-audit-a.cazCPb/cm2_round306c74_exact_multi_graph_order_oracle_v1_independent_verification_v1.json", ".cm2-runtime/c74-audit-b.ZsSfhU/cm2_round306c74_exact_multi_graph_order_oracle_v1_independent_verification_v1.json"),
        (".cm2-runtime/c73v2-audit-a.W2AYpD/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_independent_verification_v2.json", ".cm2-runtime/c73v2-audit-b.rzmvxS/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_independent_verification_v2.json"),
    ]
    for a, b in pairs:
        araw = read_stable(a, PINS.get(a))
        braw = read_stable(b, sha(araw))
        need(araw == braw, f"dual audit mismatch: {a}")
        out[f"{a}|{b}"] = sha(araw)
    return out


def validate_release() -> dict[str, Any]:
    manifest_rel = "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256"
    raw = read_stable(manifest_rel, PINS[manifest_rel])
    need(raw.endswith(b"\n"), "C65 manifest newline")
    entries: list[tuple[str, str]] = []
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ")
        need(len(parts) == 2 and len(parts[0]) == 64 and all(c in "0123456789abcdef" for c in parts[0]), "C65 manifest syntax")
        entries.append((parts[1], parts[0]))
    need(len(entries) == 446 and len({x for x, _ in entries}) == 446, "C65 manifest 446 unique")
    md = dict(entries)
    for rel in [
        "deliverables/cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json",
        "deliverables/cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz",
        "deliverables/cm2_round306c65s18_depth18_64shard_aggregate_source_summary_v1.jsonl.gz",
        "deliverables/cm2_round306c65s18_depth18_64shard_aggregate_parent_summary_v1.jsonl.gz",
        "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json",
        "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v9.json",
        "deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v9.json",
    ]:
        alias = rel.replace("/", "__")
        need(md.get(alias) == PINS[rel], f"C65 manifest pin missing: {rel}")
    outer = read_obj("deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json")
    selftest = read_obj("deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json")
    verify = read_obj("deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v9.json")
    replay = read_obj("deliverables/cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v9.json")
    need(outer.get("manifest_member_count") == 446 and outer.get("outer_receipt_published_last") is True, "C65 outer")
    need(outer.get("manifest_file_sha256") == PINS[manifest_rel], "C65 outer manifest")
    tests = selftest.get("tests")
    need(selftest.get("test_count") == 134 and isinstance(tests, dict) and len(tests) == 134 and all(v is True for v in tests.values()), "C65 134/134")
    need("PASS_134_OF_134" in selftest.get("status", ""), "C65 v9 status")
    agg = verify.get("aggregate", {})
    need(agg.get("leaf_ledger_sha256") == PINS["deliverables/cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz"], "C65 leaf pin")
    need(agg.get("source_summary_sha256") == PINS["deliverables/cm2_round306c65s18_depth18_64shard_aggregate_source_summary_v1.jsonl.gz"], "C65 source pin")
    need(agg.get("parent_summary_sha256") == PINS["deliverables/cm2_round306c65s18_depth18_64shard_aggregate_parent_summary_v1.jsonl.gz"], "C65 parent pin")
    need(replay.get("full_validation_reused_at_release") is True and replay.get("manifest_and_outer_receipt_published_after_this_result") is True, "C65 replay")
    return {"manifest_member_count": 446, "selftest_passed": 134, "manifest_sha256": sha(raw), "outer_object_sha256": outer["object_sha256"]}


def validate_semantic_results() -> None:
    c57 = read_obj("deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_result_v1.json")
    c57v = read_obj("deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_independent_verification_v1.json")
    c57_manifest = read_stable("deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_manifest_v1.sha256", PINS["deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_manifest_v1.sha256"])
    need(c57["coverage"]["C41_leaf_rows"] == 781 and c57["coverage"]["C41_terminal_rows"] == 462 and c57["coverage"]["C41_residual_outer_rows"] == 319, "C57 result census")
    need(c57["invariants"]["all_12_parent_Kraft_sums_equal_one"] is True and c57["invariants"]["all_12_parent_path_sets_prefix_free"] is True, "C57 result Kraft")
    need(c57v["coverage"]["strict_terminal_leaves"] == 462 and c57v["coverage"]["exact_collision2_handoffs"] == 319, "C57 verification census")
    need(c57v["independence"]["producer_executed"] is False and c57v["independence"]["producer_imported"] is False, "C57 verification independence")
    manifest_entries = {}
    for line in c57_manifest.decode("ascii").splitlines():
        digest, name = line.split("  ")
        manifest_entries[name] = digest
    need(manifest_entries.get("cm2_round306c57s1_singleton_collision1_common_refinement_leaf_ledger_v1.jsonl.gz") == PINS["deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_leaf_ledger_v1.jsonl.gz"], "C57 manifest leaf")
    need(manifest_entries.get("cm2_round306c57s1_singleton_collision1_common_refinement_parent_ledger_v1.jsonl.gz") == PINS["deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_parent_ledger_v1.jsonl.gz"], "C57 manifest parent")

    c58 = read_obj("deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json")
    need(c58["routing"]["input_C57_handoffs"] == 319 and c58["routing"]["disposition_census"] == {"COLLISION2_HANDOFF": 2599, "COLLISION3_READY": 0, "STRICT_TERMINAL": 2949}, "C58 result census")
    c61 = read_obj("deliverables/cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json")
    need(c61["coverage"]["carried_C57_terminal_leaves"] == 462 and c61["coverage"]["carried_C58_terminal_leaves"] == 2949, "C61 early carry")
    need(c61["invariants"]["all_12_combined_parents_prefix_free_and_Kraft_one"] is True, "C61 result Kraft")

    c69 = read_obj("deliverables/cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json")
    c69v = read_obj("deliverables/cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json")
    need(c69["object_sha256"] == "e52904a7d8ba73c855e69e390cd3cf29c233ffe492e6fae74efdf0b6d4d0a6a5", "C69c object")
    need(c69v.get("producer_executed") is False and c69v.get("producer_imported") is False and c69v.get("producer_or_wrapper_source_read_or_decoded") is False, "C69c no producer")
    c71 = read_obj(".cm2-runtime/c71b-v3-final-75c21279/cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_result.json")
    c71v = read_obj(".cm2-runtime/c71b-v3-final-75c21279/independent_verification_v3_1.json")
    c71r = read_obj(".cm2-runtime/c71b-v3-final-75c21279/dual_build_publication_completion_receipt_v3.json")
    need(c71["object_sha256"] == "75c21279e3440a32116e67c20f12c7ec9d299491d018e2982ab18d68118d4158", "C71 object")
    need(c71v.get("producer_source_imported_read_decoded_compiled_or_executed") is False and c71v.get("coherent_attacks", {}).get("rejected") == 28, "C71 verifier")
    need(c71r.get("object_sha256") == "d7fd8322b72fad933bb80542913b00cb54c5d7a3d93bf8cb7601aefa5daadbcd", "C71 receipt")
    c72 = read_obj(".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_v1_result.json")
    c72v = read_obj(".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json")
    need(c72["object_sha256"] == "a6aa0cfd8e1ee1b7a02d92af066acb23abffb22b0b7276b7e233d2ff7d92f9f4", "C72 object")
    need(c72v.get("object_sha256") == "8ae20b71916ee1f6d1d28e633b1fbc080f4cb277eed7b6bb54937f8538ae7994", "C72 verify")
    for rel, count, word in [
        (".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_result.json", 55216, "55216"),
        (".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1_result.json", 42926, "42926"),
        (".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_result.json", 5884, "5884"),
        (".cm2-runtime/c72o-build-a2.v1/cm2_round306c72o_collision1_outgoing_state_oracle_v1_result.json", 18668, "18668"),
        (".cm2-runtime/c73v2-build-a.QOYACE/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2_result.json", 1163, "1163"),
        (".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1_result.json", 10298, "10298"),
    ]:
        obj = read_obj(rel)
        need(word in obj.get("status", ""), f"oracle result count {count}")
        for key in ("formal_credit", "D02_gate_credit", "whole_parent_credit"):
            need(obj.get(key, 0) == 0, f"oracle credit: {rel}")


def load_chain() -> tuple[dict[str, Any], dict[str, Any]]:
    # Rebuild the complete pair frontiers.  A C58 refinement ledger contains
    # only replacements for C57 handoffs; its strict rows are not the earlier
    # C57 terminal carry.  Therefore all four disjoint layers are materialized:
    # C57 strict carry + C58 strict carry + C61 strict carry + C65 replacements.
    final_paths: dict[int, list[tuple[str, Fraction, str]]] = defaultdict(list)
    pair_counts: dict[int, Counter] = defaultdict(Counter)
    pair_volumes: dict[int, dict[str, Fraction]] = defaultdict(lambda: defaultdict(Fraction))

    def checked_path(row: dict[str, Any], label: str) -> tuple[str, Fraction]:
        path = row["path"]
        volume = frac(row["parent_volume_fraction"])
        need(isinstance(path, str) and path and set(path) <= {"0", "1"}, f"{label} binary path")
        need(volume == Fraction(1, 1 << len(path)), f"{label} path/volume")
        return path, volume

    c57_handoffs: dict[str, dict[str, Any]] = {}
    c57_pair_all_paths: dict[int, list[str]] = defaultdict(list)
    for row in iter_rows("deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_leaf_ledger_v1.jsonl.gz"):
        p = row["pair_index"]
        need(p in PAIR_IDS and row["owner_rows_complete"] is True and row["event_order_bound_to_C35_collision1"] is True, "C57 owner/history")
        need(row["D02_gate_credit"] == 0 and row["whole_parent_credit"] == 0, "C57 zero credit")
        path, volume = checked_path(row, "C57")
        c57_pair_all_paths[p].append(path)
        pair_counts[p]["C57_ALL"] += 1
        pair_volumes[p]["C57_ALL"] += volume
        if row["leaf_disposition"] == "STRICT_TERMINAL":
            need(row["collision2_handoff"] is None and row["local_terminal_credit"] == 1 and isinstance(row["strict_terminal_class"], str), "C57 strict carry")
            final_paths[p].append((path, volume, "C57_STRICT_CARRY"))
            pair_counts[p]["C57_STRICT_CARRY"] += 1
            pair_volumes[p]["C57_STRICT_CARRY"] += volume
        else:
            need(row["leaf_disposition"] == "COLLISION2_HANDOFF" and row["local_terminal_credit"] == 0 and row["strict_terminal_class"] is None, "C57 handoff")
            handoff = row["collision2_handoff"]
            need(isinstance(handoff, dict) and handoff["next_collision_index"] == 2 and handoff["handoff_credit"] == 0, "C57 handoff object")
            need(handoff["exact_representative_box"] == row["exact_representative_box"] and handoff["exact_reflected_box"] == row["exact_reflected_box"], "C57 handoff boxes")
            h = row["row_sha256"]
            need(h not in c57_handoffs, "C57 duplicate handoff")
            c57_handoffs[h] = {"row": row, "path": path, "volume": volume, "pair_index": p, "handoff_object_sha256": handoff["handoff_object_sha256"]}
            pair_counts[p]["C57_HANDOFF"] += 1
            pair_volumes[p]["C57_HANDOFF"] += volume
    need(sum(pair_counts[p]["C57_ALL"] for p in PAIR_IDS) == 781 and len(c57_handoffs) == 319, "C57 781/319 census")

    c57_parent_rows: dict[int, dict[str, Any]] = {}
    for row in iter_rows("deliverables/cm2_round306c57s1_singleton_collision1_common_refinement_parent_ledger_v1.jsonl.gz"):
        p = row["pair_index"]
        need(p in PAIR_IDS and p not in c57_parent_rows, "C57 parent scope")
        need(row["path_prefix_free"] is True and row["parent_Kraft_conservation"] == "1", "C57 parent certificate")
        need(row["leaf_count"] == pair_counts[p]["C57_ALL"] and row["terminal_leaf_count"] == pair_counts[p]["C57_STRICT_CARRY"] and row["collision2_handoff_leaf_count"] == pair_counts[p]["C57_HANDOFF"], "C57 parent census")
        need(prefix_free(c57_pair_all_paths[p]) and pair_volumes[p]["C57_ALL"] == 1, "C57 parent independently rebuilt")
        c57_parent_rows[p] = row
    need(set(c57_parent_rows) == set(PAIR_IDS), "C57 12 parents")

    c58_by_c57: dict[str, list[tuple[str, Fraction, str]]] = defaultdict(list)
    c58_c2: dict[str, dict[str, Any]] = {}
    for row in iter_rows("deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"):
        source = row["source_C57_leaf_row_sha256"]
        need(source in c57_handoffs, "C58/C57 source link")
        src = c57_handoffs[source]
        p = row["pair_index"]
        path, volume = checked_path(row, "C58")
        need(p == src["pair_index"] and row["source_C57_handoff_object_sha256"] == src["handoff_object_sha256"], "C58/C57 lineage")
        need(path.startswith(src["path"]) and len(path) > len(src["path"]), "C58 descendant path")
        need(row["parent_path"] == path[:-1] and row["parent_path"].startswith(src["path"]) and row["additional_depth"] == len(path) - len(src["path"]), "C58 refinement path")
        c58_by_c57[source].append((path, volume, row["disposition"]))
        pair_counts[p]["C58_ALL"] += 1
        pair_volumes[p]["C58_ALL"] += volume
        if row["disposition"] == "STRICT_TERMINAL":
            need(row["collision2_handoff"] is None and row["collision3_ready"] is None and row["local_terminal_credit"] == 1, "C58 strict carry")
            final_paths[p].append((path, volume, "C58_STRICT_CARRY"))
            pair_counts[p]["C58_STRICT_CARRY"] += 1
            pair_volumes[p]["C58_STRICT_CARRY"] += volume
        else:
            need(row["disposition"] == "COLLISION2_HANDOFF" and isinstance(row["collision2_handoff"], dict) and row["collision3_ready"] is None, "C58 disposition")
            h = row["row_sha256"]
            need(h not in c58_c2, "C58 duplicate C2")
            c58_c2[h] = {"row": row, "path": path, "volume": volume, "pair_index": p}
            pair_counts[p]["C58_C2"] += 1
            pair_volumes[p]["C58_C2"] += volume
    need(len(c58_by_c57) == 319 and len(c58_c2) == 2599, "C58 319 sources/2599 C2")
    for source, src in c57_handoffs.items():
        leaves = c58_by_c57[source]
        need(prefix_free([x[0] for x in leaves]) and sum((x[1] for x in leaves), Fraction()) == src["volume"], "C58 source prefix/Kraft")

    c58_summary_seen: set[str] = set()
    for row in iter_rows("deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_handoff_summary_v1.jsonl.gz"):
        source = row["source_C57_leaf_row_sha256"]
        need(source in c57_handoffs and source not in c58_summary_seen, "C58 summary source")
        src, leaves = c57_handoffs[source], c58_by_c57[source]
        census = Counter(x[2] for x in leaves)
        need(row["pair_index"] == src["pair_index"] and row["source_path"] == src["path"] and frac(row["source_parent_volume_fraction"]) == src["volume"], "C58 summary lineage")
        need(row["refined_leaf_count"] == len(leaves) and row["strict_terminal_leaf_count"] == census["STRICT_TERMINAL"] and row["collision2_handoff_leaf_count"] == census["COLLISION2_HANDOFF"], "C58 summary census")
        need(frac(row["Kraft_conservation"]) == src["volume"] and row["path_prefix_free"] is True, "C58 summary Kraft")
        c58_summary_seen.add(source)
    need(c58_summary_seen == set(c57_handoffs), "C58 summaries exhaustive")

    c58_parent_rows: dict[int, dict[str, Any]] = {}
    for row in iter_rows("deliverables/cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_parent_summary_v1.jsonl.gz"):
        p = row["pair_index"]
        need(p in PAIR_IDS and p not in c58_parent_rows, "C58 parent scope")
        need(row["path_prefix_free"] is True and row["parent_Kraft_conservation"] == "1", "C58 parent certificate")
        need(row["strict_terminal_leaf_count"] == pair_counts[p]["C57_STRICT_CARRY"] + pair_counts[p]["C58_STRICT_CARRY"], "C58 parent strict carry")
        need(row["collision2_handoff_leaf_count"] == pair_counts[p]["C58_C2"] and row["collision3_ready_leaf_count"] == 0, "C58 parent residual")
        need(row["combined_leaf_count"] == pair_counts[p]["C57_STRICT_CARRY"] + pair_counts[p]["C58_ALL"], "C58 parent combined")
        c58_parent_rows[p] = row
    need(set(c58_parent_rows) == set(PAIR_IDS), "C58 12 parents")

    c61_sources: dict[str, dict[str, Any]] = {}
    c61_by_c58: dict[str, list[tuple[str, Fraction, str]]] = defaultdict(list)
    for row in iter_rows("deliverables/cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"):
        source = row["source_C58_leaf_row_sha256"]
        need(source in c58_c2, "C61/C58 source link")
        src = c58_c2[source]
        p = row["pair_index"]
        need(p == src["pair_index"] and row["source_path"] == src["path"], "C61/C58 lineage")
        path, volume = checked_path(row, "C61")
        need(path.startswith(src["path"]) and len(path) > len(src["path"]), "C61 descendant path")
        c61_by_c58[source].append((path, volume, row["disposition"]))
        pair_counts[p]["C61_ALL"] += 1
        pair_volumes[p]["C61_ALL"] += volume
        if row["disposition"] == "COLLISION2_HANDOFF":
            h = row["row_sha256"]
            need(h not in c61_sources and isinstance(row["continuation"], dict), "C61 unique C2")
            c61_sources[h] = {"pair_index": p, "path": path, "box": row["exact_representative_box"], "volume": volume, "row": row}
            pair_counts[p]["C61_C2"] += 1
            pair_volumes[p]["C61_C2"] += volume
        else:
            need(row["disposition"] == "STRICT_TERMINAL" and row["continuation"] is None and row["local_terminal_credit"] == 1, "C61 disposition")
            final_paths[p].append((path, volume, "C61_STRICT_CARRY"))
            pair_counts[p]["C61_STRICT_CARRY"] += 1
            pair_volumes[p]["C61_STRICT_CARRY"] += volume
    need(len(c61_by_c58) == 2599 and len(c61_sources) == 20879, "C61 2599 sources/20879 C2")
    for source, src in c58_c2.items():
        leaves = c61_by_c58[source]
        need(prefix_free([x[0] for x in leaves]) and sum((x[1] for x in leaves), Fraction()) == src["volume"], "C61 source prefix/Kraft")

    c61_parent_rows: dict[int, dict[str, Any]] = {}
    for row in iter_rows("deliverables/cm2_round306c61s12_depth12_16shard_aggregate_parent_summary_v4.jsonl.gz"):
        p = row["pair_index"]
        need(p in PAIR_IDS and p not in c61_parent_rows, "C61 parent scope")
        need(row["path_prefix_free"] is True and row["parent_Kraft_conservation"] == "1", "C61 parent certificate")
        early = pair_counts[p]["C57_STRICT_CARRY"] + pair_counts[p]["C58_STRICT_CARRY"]
        need(row["strict_terminal_leaf_count"] == early + pair_counts[p]["C61_STRICT_CARRY"], "C61 parent strict carry")
        need(row["collision2_handoff_leaf_count"] == pair_counts[p]["C61_C2"] and row["collision3_ready_leaf_count"] == 0, "C61 parent residual")
        need(row["combined_leaf_count"] == early + pair_counts[p]["C61_ALL"], "C61 parent combined")
        c61_parent_rows[p] = row
    need(set(c61_parent_rows) == set(PAIR_IDS), "C61 12 parents")

    c69_by_c61: dict[str, dict[str, Any]] = {}
    for kind, rel in [
        ("DECISION", "deliverables/cm2_round306c69b_singleton_h1_graph_slab_decider_v2_decisions.jsonl.gz"),
        ("BLOCKER", "deliverables/cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz"),
    ]:
        for row in iter_rows(rel):
            key = row["C61_aggregate_leaf_row_sha256"]
            need(key in c61_sources and key not in c69_by_c61, "C69 partition/link")
            src = c61_sources[key]
            need(row["pair_index"] == src["pair_index"] and row["path"] == src["path"], "C69 source lineage")
            need(row["parent_volume_fraction"] == str(src["volume"]), "C69 source volume")
            if kind == "DECISION":
                need(row["decision"] == "STRICT_UNIQUE_H1_GRAPH_AND_TWO_OFF_GRAPH_SLABS_AVAILABLE", "C69 decision semantic")
                need(row["terminal_disposition_credit"] == 0 and row["whole_parent_credit"] == 0, "C69 decision zero terminal")
                need(row["exact_representative_box"] == src["box"], "C69 decision box")
                slabs = row["off_graph_slabs"]
                need(slabs["three_strata_pairwise_disjoint"] is True and slabs["three_strata_union_exact_input_box"] is True, "C69 decision strata")
            else:
                need(row["capability_decision_available"] is False and row["additional_dyadic_source_depth_recommended"] is False, "C69 blocker semantic")
                need(row["exact_representative_box_object_sha256"] == box_hash(src["box"]), "C69 blocker box")
            c69_by_c61[key] = {"kind": kind, "row": row}
    need(len(c69_by_c61) == 20879 and Counter(x["kind"] for x in c69_by_c61.values()) == {"BLOCKER": 18523, "DECISION": 2356}, "C69 exact partition")

    source_order: list[str] = []
    sources: dict[str, dict[str, Any]] = {}
    for row in iter_rows("deliverables/cm2_round306c65s18_depth18_64shard_aggregate_source_summary_v1.jsonl.gz"):
        key = row["source_C61_aggregate_leaf_row_sha256"]
        need(key in c61_sources and key not in sources, "C65 source link")
        src = c61_sources[key]
        need(row["pair_index"] == src["pair_index"] and row["source_path"] == src["path"], "C65 source identity")
        need(frac(row["source_Kraft_conservation"]) == src["volume"] and row["path_prefix_free"] is True, "C65 source Kraft")
        sources[key] = {"summary": row, "carry": 0, "carry_volume": Fraction(0), "children": [], "leaf_volume": Fraction(0)}
        source_order.append(key)
    need(len(sources) == 20879, "C65 source count")

    children: dict[str, dict[str, Any]] = {}
    child_order: list[str] = []
    c65_counts = Counter()
    for row in iter_rows("deliverables/cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz"):
        key = row["source_C61_aggregate_leaf_row_sha256"]
        need(key in sources, "C65 leaf source")
        src = sources[key]
        p = row["pair_index"]
        need(p == src["summary"]["pair_index"] and row["source_path"] == src["summary"]["source_path"], "C65 leaf source identity")
        path, v = checked_path(row, "C65")
        need(path.startswith(row["source_path"]) and len(path) > len(row["source_path"]), "C65 leaf lineage")
        src["leaf_volume"] += v
        final_paths[p].append((path, v, "C65_REPLACEMENT"))
        pair_counts[p]["C65_REPLACEMENT"] += 1
        pair_volumes[p]["C65_REPLACEMENT"] += v
        c65_counts[row["disposition"]] += 1
        if row["disposition"] == "STRICT_TERMINAL":
            src["carry"] += 1
            src["carry_volume"] += v
        else:
            need(row["disposition"] == "COLLISION2_HANDOFF", "C65 disposition")
            h = row["row_sha256"]
            need(h not in children, "C65 duplicate child")
            children[h] = {"c65": row, "source": key}
            child_order.append(h)
            src["children"].append(h)
    need(c65_counts == {"COLLISION2_HANDOFF": 167255, "STRICT_TERMINAL": 191664}, "C65 leaf census")
    for key, src in sources.items():
        s = src["summary"]
        need(src["leaf_volume"] == frac(s["source_Kraft_conservation"]), "source leaf Kraft")
        need(src["carry"] == s["strict_terminal_leaf_count"] and len(src["children"]) == s["collision2_handoff_leaf_count"], "source count rollup")

    c65_parent_rows: dict[int, dict[str, Any]] = {}
    for row in iter_rows("deliverables/cm2_round306c65s18_depth18_64shard_aggregate_parent_summary_v1.jsonl.gz"):
        p = row["pair_index"]
        need(p in PAIR_IDS and p not in c65_parent_rows, "C65 parent scope")
        need(row["path_prefix_free"] is True and row["parent_Kraft_conservation"] == "1" and row["parent_prefix_Kraft_preserved_by_base_certificate_and_exact_source_partitions"] is True, "C65 parent certificate")
        early = pair_counts[p]["C57_STRICT_CARRY"] + pair_counts[p]["C58_STRICT_CARRY"]
        c65_strict = sum(s["carry"] for s in sources.values() if s["summary"]["pair_index"] == p)
        c65_c2 = sum(len(s["children"]) for s in sources.values() if s["summary"]["pair_index"] == p)
        need(row["C57_C58_earlier_terminal_carry_leaf_count"] == early, "C65 parent early carry")
        need(row["C61_aggregate_ledger_strict_terminal_leaf_count"] == pair_counts[p]["C61_STRICT_CARRY"], "C65 parent C61 carry")
        need(row["C61_full_base_strict_terminal_leaf_count"] == early + pair_counts[p]["C61_STRICT_CARRY"], "C65 parent base strict")
        need(row["C61_full_base_collision2_sources_replaced"] == pair_counts[p]["C61_C2"], "C65 parent replaced sources")
        need(row["C65_replacement_leaf_count"] == pair_counts[p]["C65_REPLACEMENT"], "C65 parent replacement count")
        need(row["strict_terminal_leaf_count"] == early + pair_counts[p]["C61_STRICT_CARRY"] + c65_strict, "C65 parent final strict")
        need(row["collision2_handoff_leaf_count"] == c65_c2 and row["collision3_ready_leaf_count"] == 0, "C65 parent final residual")
        need(row["combined_leaf_count"] == early + pair_counts[p]["C61_STRICT_CARRY"] + pair_counts[p]["C65_REPLACEMENT"], "C65 parent final combined")
        need(row["C61_full_base_parent_row_sha256"] == c61_parent_rows[p]["row_sha256"], "C65/C61 parent row link")
        c65_parent_rows[p] = row
    need(set(c65_parent_rows) == set(PAIR_IDS), "C65 12 parents")

    c71_seen: set[str] = set()
    for row in iter_rows(".cm2-runtime/c71b-v3-final-75c21279/cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_rows.jsonl.gz"):
        h = row["C65_aggregate_leaf_row_sha256"]
        need(h in children and h not in c71_seen, "C71 child link")
        c = children[h]
        src_kind = c69_by_c61[c["source"]]["kind"]
        need(row["child_path"] == c["c65"]["path"] and row["source_path"] == c["c65"]["source_path"] and row["pair_index"] == c["c65"]["pair_index"], "C71 exact lineage")
        need(row["exact_representative_box"] == c["c65"]["exact_representative_box"], "C71 exact child box")
        if src_kind == "DECISION":
            need(row["child_level_H1_full_box_closed"] is True and row["consumer_review_ready"] is True and row["remaining_blocker_codes"] == [], "C71 decision H1")
            need(row["terminal_disposition_credit"] == 0 and row["global_consumption_ready"] is False, "C71 is not terminal")
        else:
            need(row["v2_disposition"] == "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE" and row["consumer_review_ready"] is False, "C71 blocker fail closed")
        c["c71"] = row["row_sha256"]
        c71_seen.add(h)
    need(len(c71_seen) == 167255, "C71 exhaustive")

    atlas_seen: set[str] = set()
    atlas_by_child: dict[str, dict[str, Any]] = {}
    for row in iter_rows(".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"):
        h = row["C65_aggregate_child_row_sha256"]
        need(h in children and c69_by_c61[children[h]["source"]]["kind"] == "BLOCKER" and h not in atlas_seen, "C72 scope")
        c = children[h]
        need(row["child_path"] == c["c65"]["path"] and row["source_path"] == c["c65"]["source_path"], "C72 lineage")
        need(row["exact_representative_box"] == c["c65"]["exact_representative_box"] and row["C61_aggregate_leaf_row_sha256"] == c["source"], "C72 box/source")
        need(row["current_disposition"] == "FAIL_CLOSED_STRUCTURAL_OBLIGATION", "C72 fail closed")
        atlas_seen.add(h)
        atlas_by_child[h] = row
    need(len(atlas_seen) == 134155, "C72 exhaustive blocker scope")
    return {"c61": c61_sources, "c69": c69_by_c61, "sources": sources, "source_order": source_order,
            "children": children, "child_order": child_order, "atlas": atlas_by_child, "final_paths": final_paths,
            "pair_stage_counts": pair_counts, "pair_stage_volumes": pair_volumes,
            "parent_row_sha256": {p: {"C57": c57_parent_rows[p]["row_sha256"], "C58": c58_parent_rows[p]["row_sha256"],
                                          "C61": c61_parent_rows[p]["row_sha256"], "C65": c65_parent_rows[p]["row_sha256"]}
                                  for p in PAIR_IDS}}, {}


def load_oracles(chain: dict[str, Any]) -> dict[str, Any]:
    children, atlas, c69 = chain["children"], chain["atlas"], chain["c69"]
    dispositions: dict[str, dict[str, Any]] = {}
    counts = Counter()

    specs = [
        ("C72B2", ".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2.jsonl.gz"),
        ("C74", ".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1.jsonl.gz"),
        ("C75", ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1.jsonl.gz"),
        ("C72O", ".cm2-runtime/c72o-build-a2.v1/cm2_round306c72o_collision1_outgoing_state_oracle_v1.jsonl.gz"),
        ("C73V2", ".cm2-runtime/c73v2-build-a.QOYACE/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2.jsonl.gz"),
        ("C76", ".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1.jsonl.gz"),
    ]
    for oracle, rel in specs:
        for row in iter_rows(rel):
            h = row["C65_aggregate_child_row_sha256"]
            need(h in atlas and h not in dispositions, f"{oracle} overlap/link")
            c, a = children[h], atlas[h]
            atlas_hash = row.get("C72_atlas_row_sha256", row.get("C72_obligation_row_sha256"))
            need(atlas_hash == a["row_sha256"] and row["child_path"] == c["c65"]["path"] and row["source_path"] == c["c65"]["source_path"], f"{oracle} lineage")
            need(row["pair_index"] == c["c65"]["pair_index"] and row.get("formal_credit", 0) == 0 and row.get("D02_gate_credit", 0) == 0 and row.get("whole_parent_credit", 0) == 0, f"{oracle} credit")
            if oracle in ("C72B2", "C76"):
                need(row["H1_geometry_closed"] is True and row["physical_chart_glue_closed"] is True and row["allowed_exit_closed_for_every_stratum"] is True, f"{oracle} glue")
                need(row["whole_child_strict_exclusion_closed"] is True and all(x["exit_class"] == "STRICT_EXCLUSION" for x in row["stratum_exits"]), f"{oracle} exclusion")
                terminal = "STRICT_EXCLUSION"
            elif oracle == "C74":
                strata = row["sealed_strata"]
                need(len(strata) == 3 and row["complete_child_decision"] == "SEALED_TWO_OPEN_SLABS_PLUS_EXACT_GRAPH_STRATUM", "C74 strata")
                exits = [x["exit_class"] for x in strata]
                future = row["discriminant_graph"]["physical_future_tangency"]
                if future:
                    need(exits == ["STRICT_EXCLUSION", "CEMETERY_OR_SOURCE_GRAZING_TERMINAL", "STRICT_EXCLUSION"], "C74 cemetery")
                    terminal = "CEMETERY_TANGENCY_TERMINAL"
                else:
                    need(exits == ["STRICT_EXCLUSION"] * 3, "C74 exclusion")
                    terminal = "STRICT_EXCLUSION"
            elif oracle == "C75":
                exits = row["three_strata"]
                need(row["unresolved_strata"] == 0 and row["allowed_exit_coverage"] == "TWO_STRICT_EXCLUSION_SIDES_PLUS_CEMETERY_FIRST_TANGENCY_GRAPH", "C75 closure")
                need(exits["negative_open_side"]["exit_class"] == "STRICT_EXCLUSION" and exits["positive_open_side"]["exit_class"] == "STRICT_EXCLUSION", "C75 sides")
                need(exits["zero_graph"]["exit_class"] == "CEMETERY_OR_SOURCE_GRAZING_TERMINAL" and exits["zero_graph"]["root_is_strict_future_and_first"] is True, "C75 graph")
                terminal = "CEMETERY_TANGENCY_TERMINAL"
            elif oracle == "C72O":
                need(row["exit_class"] == "STRICT_EXCLUSION" and row["current_disposition"] == "STAGED_ZERO_CREDIT_STRICT_EXCLUSION_CANDIDATE", "C72o exclusion")
                need(isinstance(row.get("collision1_history_row_sha256"), str) and isinstance(row.get("collision1_registry_row_sha256"), str), "C72o owner/history")
                terminal = "STRICT_EXCLUSION"
            else:
                need(row["allowed_exit_class"] == "STRICT_EXCLUSION" and row["complete_child_decision"] is True and row["local_strict_terminal"] is True, "C73 exclusion")
                terminal = "STRICT_EXCLUSION"
            dispositions[h] = {"oracle": oracle, "oracle_row_sha256": row["row_sha256"], "terminal": terminal}
            counts[(oracle, terminal)] += 1
    need(len(dispositions) == 134155, "oracle exhaustive")
    expected = {
        ("C72B2", "STRICT_EXCLUSION"): 55216,
        ("C74", "STRICT_EXCLUSION"): 25559,
        ("C74", "CEMETERY_TANGENCY_TERMINAL"): 17367,
        ("C75", "CEMETERY_TANGENCY_TERMINAL"): 5884,
        ("C72O", "STRICT_EXCLUSION"): 18668,
        ("C73V2", "STRICT_EXCLUSION"): 1163,
        ("C76", "STRICT_EXCLUSION"): 10298,
    }
    need(dict(counts) == expected, f"oracle census: {counts}")
    return {"dispositions": dispositions, "counts": counts}


def incidence_audit(chain: dict[str, Any]) -> dict[str, Any]:
    def root_scope(rel: str, expected_degree: dict[int, int]) -> tuple[dict[str, Any], dict[tuple[str, str], tuple[str, tuple[str, ...], str]]]:
        degree = Counter()
        boundary_authority = Counter()
        shared_degree_one: dict[tuple[str, str], tuple[str, tuple[str, ...], str]] = {}
        occurrences = 0
        roots = 0
        for row in iter_rows(rel):
            roots += 1
            d = row["incidence_count"]
            degree[d] += 1
            occurrences += d
            need(d in (1, 2) and len(row["target_graph_endpoint_occurrences"]) == d, "root incidence degree")
            need(row["incidence_closed"] is True and row["unique_half_open_dyadic_face_owner"] and row["root_is_graph_endpoint_not_physical_terminal"] is True, "root owner closure")
            need(row["same_physical_trace_duplicate_identified_not_added"] is True and row["paired_N_or_S_representation_is_shadow_only"] is True, "physical trace glue")
            # Degree one is a classified half-open owner, never a dangling root.
            if d == 1:
                need(row["atlas_face_incidence_count"] in (1, 2) and row["atlas_face_incidence_class"] in ("SHARED_FACE", "ATLAS_SCOPE_BOUNDARY_FACE"), "degree-one owner binding")
                if row["atlas_face_incidence_class"] == "SHARED_FACE":
                    need(row["atlas_face_incidence_count"] == 2 and len(row["incident_C72_atlas_faces"]) == 2, "shared degree-one two physical faces")
                    key = (row["root_id"], row["face_key_sha256"])
                    need(key not in shared_degree_one, "shared physical root duplicate")
                    shared_degree_one[key] = (
                        sha(cbytes(row["exact_face"])),
                        tuple(x["C72_atlas_row_sha256"] for x in row["incident_C72_atlas_faces"]),
                        row["unique_half_open_dyadic_face_owner"]["C72_atlas_row_sha256"],
                    )
                else:
                    need(row["atlas_face_incidence_count"] == 1 and len(row["incident_C72_atlas_faces"]) == 1, "atlas boundary single authority")
                    owner = row["unique_half_open_dyadic_face_owner"]
                    need(owner["C72_atlas_row_sha256"] == row["incident_C72_atlas_faces"][0]["C72_atlas_row_sha256"], "atlas boundary owner authority")
                    boundary_authority["ATLAS_SCOPE_BOUNDARY_FACE"] += 1
        need(dict(degree) == expected_degree, f"root degree census {rel}: {degree}")
        return ({"unique_physical_root_count": roots, "endpoint_occurrence_count": occurrences, "degree_census": {str(k): v for k, v in sorted(degree.items())}, "degree_one_shared_face_count": len(shared_degree_one), "degree_one_atlas_scope_boundary_authority_count": boundary_authority["ATLAS_SCOPE_BOUNDARY_FACE"], "degree_one_is_classified_half_open_owner_not_dangling": True}, shared_degree_one)

    c72b2, c72b2_shared = root_scope(".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_root_incidence.jsonl.gz", {1: 18098, 2: 46164})
    c76, c76_shared = root_scope(".cm2-runtime/c76-build-a.final-3284b6ef/cm2_round306c76_full_face_h1_physical_glue_oracle_v1_root_incidence.jsonl.gz", {1: 17370, 2: 1613})
    need(len(c72b2_shared) == len(c76_shared) == 15841 and c72b2_shared == c76_shared, "C72b2/C76 reciprocal shared physical roots/faces/owners")

    cross: dict[tuple[str, int, str, str, str, tuple[str, ...]], dict[str, Any]] = {}
    c74c = Counter()
    for row in iter_rows(".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1_endpoint_incidence.jsonl.gz"):
        kind = row["incidence_class"]
        c74c[kind] += 1
        need(row["endpoint_incidence_closed"] is True and row["same_physical_trace_duplicate_unassigned"] is False, "C74 incidence")
        if kind == "ADJACENT_C72_CROSS_SCOPE_GLUE":
            adj = row["consumer"]["adjacent_C72_face"]
            face = row["exact_face"]
            key = (adj["C72_atlas_row_sha256"], face["pair_index"], row["collision1_target"], face["fixed_axis"], face["fixed_value"], tuple(face["varying_interval"]))
            need(key not in cross, "C74 cross duplicate")
            physical_digest = sha(cbytes({"pair_index": face["pair_index"], "collision1_target": row["collision1_target"], "equation": "CENTERED_COLLISION1_DISCRIMINANT_EQUALS_ZERO", "exact_s": "0", "exact_t": face["fixed_value"], "exact_p_interval": face["varying_interval"]}))
            cross[key] = {"C74_C72": row["C72_atlas_row_sha256"], "face": face, "native_root": row["endpoint_root_id"], "canonical_physical_root_digest": physical_digest}
        if kind == "SOURCE_CELL_BOUNDARY_CONSUMER":
            need(row["source_cell_boundary"] is True, "C74 source boundary")
    need(c74c == {"PAIRED_INTERNAL_C74_ENDPOINT": 22976, "ADJACENT_C72_CROSS_SCOPE_GLUE": 11750, "SOURCE_CELL_BOUNDARY_CONSUMER": 8}, f"C74 incidence census {c74c}")

    c75c = Counter()
    matched = 0
    seen_c75_cross: set[tuple[str, int, str, str, str, tuple[str, ...]]] = set()
    in_scope_owner_flags: dict[str, list[bool]] = defaultdict(list)
    for row in iter_rows(".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_endpoint_incidence.jsonl.gz"):
        need(row["dangling"] is False and row["duplicate_occurrence"] is False, "C75 dangling/duplicate")
        a = row["adjacency_and_half_open_owner"]
        kind = a["incidence_kind"]
        c75c[kind] += 1
        need(a["classified_boundary_not_dangling"] is True and isinstance(a["current_occurrence_is_half_open_owner"], bool), "C75 classified owner")
        if kind == "OUT_OF_SCOPE_C72_DOWNSTREAM_OWNER":
            need(a["incidence_degree_including_downstream"] == 2, "C75 cross-scope degree")
            ef = row["exact_face_key"]
            target = row["root_identity_preimage"]["tangency_target"]
            key = (row["C72_obligation_row_sha256"], row["pair_index"], target, ef["face_axis"], ef["exact_t"], tuple(ef["exact_p_interval"]))
            need(key in cross, "C74/C75 missing cross")
            need(key not in seen_c75_cross, "C75 cross duplicate physical occurrence")
            seen_c75_cross.add(key)
            x = cross[key]
            need(x["C74_C72"] == a["neighbor_C72_obligation_row_sha256"], "C74/C75 reciprocal C72")
            xf = x["face"]
            need(ef["face_axis"] == xf["fixed_axis"] == "t" and ef["exact_t"] == xf["fixed_value"] and ef["exact_p_interval"] == xf["varying_interval"], "C74/C75 exact physical face")
            physical_digest = sha(cbytes({"pair_index": row["pair_index"], "collision1_target": target, "equation": "CENTERED_COLLISION1_DISCRIMINANT_EQUALS_ZERO", "exact_s": "0", "exact_t": ef["exact_t"], "exact_p_interval": ef["exact_p_interval"]}))
            need(physical_digest == x["canonical_physical_root_digest"] and isinstance(row["root_id"], str) and isinstance(x["native_root"], str), "C74/C75 canonical physical root")
            matched += 1
        elif kind == "IN_SCOPE_MATCHED_TANGENCY_SEGMENT":
            need(a["incidence_degree_including_downstream"] == 2 and isinstance(a.get("neighbor_C75_strata_row_sha256"), str), "C75 in-scope pairing")
            in_scope_owner_flags[row["root_id"]].append(a["current_occurrence_is_half_open_owner"])
        elif kind == "C32_ATLAS_CELL_BOUNDARY_OWNER":
            need(a["current_occurrence_is_half_open_owner"] is True and a["incidence_degree_including_downstream"] == 2, "C75 C32 boundary owner")
        elif kind == "C32_ATLAS_OUTER_GUARD_BOUNDARY_TERMINAL":
            need(a["current_occurrence_is_half_open_owner"] is True, "C75 outer guard owner")
    need(c75c == {"OUT_OF_SCOPE_C72_DOWNSTREAM_OWNER": 11750, "IN_SCOPE_MATCHED_TANGENCY_SEGMENT": 16, "C32_ATLAS_CELL_BOUNDARY_OWNER": 1, "C32_ATLAS_OUTER_GUARD_BOUNDARY_TERMINAL": 1}, f"C75 incidence census {c75c}")
    need(len(in_scope_owner_flags) == 8 and all(len(v) == 2 and sum(v) == 1 for v in in_scope_owner_flags.values()), "C75 in-scope half-open owners")
    need(matched == len(cross) == len(seen_c75_cross) == 11750 and seen_c75_cross == set(cross), "C74/C75 reciprocal occurrence multiset exhaustive")
    return {
        "C72B2_physical_H1_graph_roots": c72b2,
        "C76_physical_H1_graph_roots": c76,
        "C72B2_C76_reciprocal_shared_face_half_open_owner_count": 15841,
        "C72B2_C76_reciprocal_shared_face_root_face_owner_identity": True,
        "C74_endpoint_incidence_census": dict(sorted(c74c.items())),
        "C75_endpoint_incidence_census": dict(sorted(c75c.items())),
        "C74_C75_reciprocal_cross_scope_occurrences": matched,
        "C74_C75_canonical_physical_face_root_occurrence_multisets_equal": True,
        "C74_source_boundary_occurrences": 8,
        "C75_C32_or_outer_boundary_occurrences": 2,
        "face_corner_source_seam_incidence_closed": True,
    }


def prefix_free(paths: list[str]) -> bool:
    s = sorted(paths)
    return all(not b.startswith(a) for a, b in zip(s, s[1:]))


def build_rollups(chain: dict[str, Any], oracle: dict[str, Any], singleton_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    children, sources, c69 = chain["children"], chain["sources"], chain["c69"]
    disp = oracle["dispositions"]
    child_rows: list[dict[str, Any]] = []
    source_stats: dict[str, Counter] = defaultdict(Counter)
    for ordinal, h in enumerate(chain["child_order"], 1):
        c, source = children[h], children[h]["source"]
        kind = c69[source]["kind"]
        if kind == "DECISION":
            terminal = "RESIDUAL_SEALED_NEXT_DECIDER_REQUIRED"
            oracle_id = "NONE_C71_H1_ONLY"
            oracle_sha = None
            source_stats[source]["residual"] += 1
        else:
            d = disp[h]
            terminal, oracle_id, oracle_sha = d["terminal"], d["oracle"], d["oracle_row_sha256"]
            source_stats[source]["blocker_terminal"] += 1
            source_stats[source][terminal] += 1
        row = add_row_hash({
            "schema": SCHEMA + ".child-disposition-row",
            "ordinal": ordinal,
            "pair_index": c["c65"]["pair_index"],
            "source_path": c["c65"]["source_path"],
            "child_path": c["c65"]["path"],
            "parent_volume_fraction": c["c65"]["parent_volume_fraction"],
            "C61_source_row_sha256": source,
            "C65_child_row_sha256": h,
            "C71b_H1_row_sha256": c["c71"],
            "C72_atlas_row_sha256": chain["atlas"].get(h, {}).get("row_sha256"),
            "C69c_source_kind": kind,
            "consuming_oracle": oracle_id,
            "consuming_oracle_row_sha256": oracle_sha,
            "disposition": terminal,
            "terminal_predicate_present": kind == "BLOCKER",
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "whole_parent_credit": 0,
            "global_unresolved_decrement": 0,
        })
        child_rows.append(row)

    source_rows: list[dict[str, Any]] = []
    source_census = Counter()
    for ordinal, key in enumerate(chain["source_order"], 1):
        src, c69row = sources[key], c69[key]
        stats = source_stats[key]
        residual = stats["residual"]
        terminal = residual == 0
        source_census[(c69row["kind"], "TERMINAL" if terminal else "RESIDUAL")] += 1
        selected_volume = sum((frac(children[h]["c65"]["parent_volume_fraction"]) for h in src["children"]), Fraction(0))
        total = src["carry_volume"] + selected_volume
        need(total == frac(src["summary"]["source_Kraft_conservation"]), "source selected+carry Kraft")
        source_rows.append(add_row_hash({
            "schema": SCHEMA + ".source-rollup-row",
            "ordinal": ordinal,
            "pair_index": src["summary"]["pair_index"],
            "source_path": src["summary"]["source_path"],
            "C61_source_row_sha256": key,
            "C65_source_summary_row_sha256": src["summary"]["row_sha256"],
            "C69c_source_row_sha256": c69row["row"]["row_sha256"],
            "C69c_source_kind": c69row["kind"],
            "C65_strict_terminal_carry_leaf_count": src["carry"],
            "selected_collision2_child_count": len(src["children"]),
            "selected_blocker_terminal_child_count": stats["blocker_terminal"],
            "selected_decision_residual_child_count": residual,
            "selected_child_Kraft": str(selected_volume),
            "C65_strict_terminal_carry_Kraft": str(src["carry_volume"]),
            "full_source_Kraft": str(total),
            "source_prefix_free_and_Kraft_closed": True,
            "whole_source_terminal": terminal,
            "residual_reason": None if terminal else "C71B_H1_FULL_BOX_CLOSURE_HAS_NO_FROZEN_DOWNSTREAM_TERMINAL_PREDICATE",
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "whole_parent_credit": 0,
        }))

    pair_rows: list[dict[str, Any]] = []
    pair_residual: dict[int, int] = Counter()
    pair_block_terminal: dict[int, int] = Counter()
    pair_cemetery: dict[int, int] = Counter()
    for h, c in children.items():
        p = c["c65"]["pair_index"]
        if c69[c["source"]]["kind"] == "DECISION":
            pair_residual[p] += 1
        else:
            pair_block_terminal[p] += 1
            if disp[h]["terminal"] == "CEMETERY_TANGENCY_TERMINAL":
                pair_cemetery[p] += 1
    for p in PAIR_IDS:
        leaves = chain["final_paths"][p]
        need(prefix_free([x[0] for x in leaves]), f"pair {p} prefix")
        kraft = sum((x[1] for x in leaves), Fraction(0))
        need(kraft == 1, f"pair {p} Kraft")
        stage_counts = chain["pair_stage_counts"][p]
        stage_volumes = chain["pair_stage_volumes"][p]
        need(len(leaves) == stage_counts["C57_STRICT_CARRY"] + stage_counts["C58_STRICT_CARRY"] + stage_counts["C61_STRICT_CARRY"] + stage_counts["C65_REPLACEMENT"], f"pair {p} four-layer count")
        need(kraft == stage_volumes["C57_STRICT_CARRY"] + stage_volumes["C58_STRICT_CARRY"] + stage_volumes["C61_STRICT_CARRY"] + stage_volumes["C65_REPLACEMENT"], f"pair {p} four-layer volume")
        source_count = sum(1 for s in sources.values() if s["summary"]["pair_index"] == p)
        pair_rows.append(add_row_hash({
            "schema": SCHEMA + ".pair-rollup-row",
            "pair_index": p,
            "reflection_cell_count": 2,
            "C69c_source_task_count": source_count,
            "final_prefix_leaf_count": len(leaves),
            "C57_strict_terminal_carry_leaf_count": stage_counts["C57_STRICT_CARRY"],
            "C58_strict_terminal_carry_leaf_count": stage_counts["C58_STRICT_CARRY"],
            "C61_strict_terminal_carry_leaf_count": stage_counts["C61_STRICT_CARRY"],
            "C65_replacement_leaf_count": stage_counts["C65_REPLACEMENT"],
            "C57_strict_terminal_carry_Kraft": str(stage_volumes["C57_STRICT_CARRY"]),
            "C58_strict_terminal_carry_Kraft": str(stage_volumes["C58_STRICT_CARRY"]),
            "C61_strict_terminal_carry_Kraft": str(stage_volumes["C61_STRICT_CARRY"]),
            "C65_replacement_Kraft": str(stage_volumes["C65_REPLACEMENT"]),
            "frozen_parent_row_sha256": chain["parent_row_sha256"][p],
            "blocker_terminal_child_count": pair_block_terminal[p],
            "cemetery_graph_child_count": pair_cemetery[p],
            "decision_residual_child_count": pair_residual[p],
            "parent_prefix_free": True,
            "parent_Kraft": "1",
            "whole_reflection_pair_terminal": pair_residual[p] == 0,
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "whole_parent_credit": 0,
        }))

    cell_rows: list[dict[str, Any]] = []
    by_pair = defaultdict(list)
    for row in singleton_rows:
        by_pair[row["pair_index"]].append(row)
    need(set(by_pair) == set(PAIR_IDS) and all(len(v) == 2 for v in by_pair.values()), "24 cells/12 pairs")
    for p in PAIR_IDS:
        a, b = sorted(by_pair[p], key=lambda x: x["cell_id"])
        need(a["reflection_partner_cell_id"] == b["cell_id"] and b["reflection_partner_cell_id"] == a["cell_id"], "reflection bijection")
        for row in (a, b):
            cell_rows.append(add_row_hash({
                "schema": SCHEMA + ".singleton-cell-rollup-row",
                "component_index": row["component_index"],
                "component_id": row["component_id"],
                "cell_id": row["cell_id"],
                "reflection_partner_cell_id": row["reflection_partner_cell_id"],
                "pair_index": p,
                "origin_key": row["origin_key"],
                "blocker_terminal_child_count_on_reflection_pair": pair_block_terminal[p],
                "decision_residual_child_count_on_reflection_pair": pair_residual[p],
                "candidate_whole_cell_terminal": pair_residual[p] == 0,
                "candidate_terminal_class": "STRICT_EXCLUSION_OR_CEMETERY_STRATIFIED_BY_FROZEN_CHILD_PARTITION" if pair_residual[p] == 0 else None,
                "residual_reason": None if pair_residual[p] == 0 else "DECISION_SOURCE_CHILDREN_REQUIRE_FROZEN_DOWNSTREAM_ROUTE_DECIDER",
                "candidate_public_unresolved_decrement": 0,
                "formal_credit": 0,
                "D02_gate_credit": 0,
                "whole_parent_credit": 0,
            }))

    closed_cells = sum(r["candidate_whole_cell_terminal"] for r in cell_rows)
    need(closed_cells < 24, "unexpected all singleton cells closed")
    summary = {
        "source_census": {f"{k[0]}_{k[1]}": v for k, v in sorted(source_census.items())},
        "closed_singleton_cell_count": closed_cells,
        "residual_singleton_cell_count": 24 - closed_cells,
        "whole_reflection_pair_terminal_count": sum(r["whole_reflection_pair_terminal"] for r in pair_rows),
        "residual_reflection_pair_count": sum(not r["whole_reflection_pair_terminal"] for r in pair_rows),
    }
    return child_rows, source_rows, pair_rows, cell_rows, summary


def load_singletons() -> list[dict[str, Any]]:
    components = {}
    for row in iter_rows("deliverables/cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz"):
        if row["cell_count"] == 1:
            need(row["known_sheet_anchor"] is None and row["whole_component_terminal_class"] is None, "frozen singleton baseline")
            components[row["component_id"]] = row
    need(len(components) == 24, "singleton component count")
    cells = []
    for row in iter_rows("deliverables/cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz"):
        if row["component_id"] in components:
            need(row["current_effective_disposition"] == "UNRESOLVED_R1648_CONTINUATION", "singleton frozen disposition")
            cells.append(row)
    need(len(cells) == 24 and {r["pair_index"] for r in cells} == set(PAIR_IDS), "singleton cell mapping")
    baseline = read_obj("deliverables/cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json")
    need(baseline["C53_effective_authority"]["effective_checkpoint_object_sha256"] == "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab", "global checkpoint")
    return cells


def publish(outdir: Path, result: dict[str, Any], incidence: dict[str, Any], row_groups: list[tuple[str, list[dict[str, Any]]]]) -> dict[str, Any]:
    outdir.mkdir(mode=0o755, parents=False, exist_ok=False)
    members: dict[str, dict[str, Any]] = {}
    lock_name = "ZERO_CREDIT_CANDIDATE_SINGLETON_PARENT_CONSUMER_ONLY.lock"
    lock = b"candidate=true\nauthority=false\nformal_credit=0\nD02_gate_credit=0\nglobal_installed_credit=0\n"
    write_exclusive(outdir / lock_name, lock)
    members[lock_name] = {"sha256": sha(lock), "size": len(lock)}
    descriptors = {}
    for name, rows in row_groups:
        data, sequence = gzip_bytes(rows)
        filename = f"{BASE}_{name}.jsonl.gz"
        write_exclusive(outdir / filename, data)
        members[filename] = {"sha256": sha(data), "size": len(data)}
        descriptors[name] = {"filename": filename, "row_count": len(rows), "sha256": sha(data), "size": len(data), "row_hash_line_sequence_sha256": sequence}
    incidence_obj = add_object_hash({"schema": SCHEMA + ".incidence-audit", **incidence, "formal_credit": 0, "D02_gate_credit": 0, "global_installed_credit": 0})
    incidence_name = f"{BASE}_incidence_audit.json"
    incidence_raw = cbytes(incidence_obj) + b"\n"
    write_exclusive(outdir / incidence_name, incidence_raw)
    members[incidence_name] = {"sha256": sha(incidence_raw), "size": len(incidence_raw)}
    result["ledgers"] = descriptors
    result["incidence_audit_object_sha256"] = incidence_obj["object_sha256"]
    result_obj = add_object_hash(result)
    result_name = f"{BASE}_result.json"
    result_raw = cbytes(result_obj) + b"\n"
    write_exclusive(outdir / result_name, result_raw)
    members[result_name] = {"sha256": sha(result_raw), "size": len(result_raw)}
    report_name = f"{BASE}_report.md"
    report = (
        "# C77s singleton-parent no-producer consumer v1\n\n"
        "Frozen blocker evidence closes 134,155 children as 110,904 whole-child strict exclusions and "
        "23,251 cemetery tangency terminals. The 33,100 decision-source children retain an exact residual: "
        "C69c/C71b prove only H1 full-box partition geometry and publish no downstream terminal predicate.\n\n"
        f"Whole singleton cells closed by this candidate: {result['singleton_cells']['candidate_whole_terminal']}/24. "
        "Because the requested singleton decrement is atomic, candidate public decrement is 0. All formal, D02, "
        "CM2, and installed global credits remain zero.\n"
    ).encode()
    write_exclusive(outdir / report_name, report)
    members[report_name] = {"sha256": sha(report), "size": len(report)}
    manifest_name = f"{BASE}_manifest.sha256"
    manifest_raw = b"".join(f"{meta['sha256']}  {name}\n".encode() for name, meta in members.items())
    write_exclusive(outdir / manifest_name, manifest_raw)
    manifest_meta = {"sha256": sha(manifest_raw), "size": len(manifest_raw)}
    # Outer receipt is deliberately the final publication member.
    outer = add_object_hash({
        "schema": SCHEMA + ".outer-receipt",
        "status": "PASS_APPEND_ONLY_NO_PRODUCER_SINGLETON_PARENT_CONSUMER__EXACT_BLOCKER_CLOSURE__DECISION_RESIDUAL_FAIL_CLOSED__ZERO_CREDIT",
        "candidate_is_authority": False,
        "manifest_filename": manifest_name,
        "manifest_file_sha256": manifest_meta["sha256"],
        "manifest_member_count": len(members),
        "outer_receipt_published_last": True,
        "all_members_terminal_byte_replayed": True,
        "formal_credit": 0,
        "D02_gate_credit": 0,
        "CM2_credit": 0,
        "global_installed_credit": 0,
        "candidate_public_unresolved_decrement": 0,
        "result_object_sha256": result_obj["object_sha256"],
    })
    outer_name = f"{BASE}_outer_receipt.json"
    outer_raw = cbytes(outer) + b"\n"
    write_exclusive(outdir / outer_name, outer_raw)
    # Fresh terminal-byte recapture of every member, manifest, and outer.
    replay = {}
    for name, meta in {**members, manifest_name: manifest_meta, outer_name: {"sha256": sha(outer_raw), "size": len(outer_raw)}}.items():
        raw = read_stable(str((outdir / name).relative_to(ROOT)), meta["sha256"])
        need(len(raw) == meta["size"], "output size replay")
        replay[name] = meta["sha256"]
    return {"result": result_obj, "outer": outer, "members": members, "manifest": manifest_meta, "terminal_replay": replay}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()
    outdir = Path(args.output_dir)
    if not outdir.is_absolute():
        outdir = ROOT / outdir
    need(ROOT in outdir.parents, "output must be below workspace")
    need(not outdir.exists(), "append-only output exists")

    release = validate_release()
    validate_semantic_results()
    duals = validate_duals()
    chain, _ = load_chain()
    oracles = load_oracles(chain)
    incidence = incidence_audit(chain)
    singleton_rows = load_singletons()
    child_rows, source_rows, pair_rows, cell_rows, roll = build_rollups(chain, oracles, singleton_rows)

    exclusion = sum(v for (o, t), v in oracles["counts"].items() if t == "STRICT_EXCLUSION")
    cemetery = sum(v for (o, t), v in oracles["counts"].items() if t == "CEMETERY_TANGENCY_TERMINAL")
    need((exclusion, cemetery, exclusion + cemetery) == (110904, 23251, 134155), "blocker terminal census")
    decision_residual = sum(r["disposition"] == "RESIDUAL_SEALED_NEXT_DECIDER_REQUIRED" for r in child_rows)
    need(decision_residual == 33100, "decision residual census")
    source_census = roll["source_census"]
    result = {
        "schema": SCHEMA + ".result",
        "status": "PASS_EXACT_167255_CHILD_RECONSTRUCTION__134155_BLOCKERS_TERMINAL__33100_DECISION_CHILDREN_RESIDUAL__ATOMIC_SINGLETON_DECREMENT_ZERO__ZERO_CREDIT",
        "candidate_is_authority": False,
        "upstream_producer_policy": {"opened": False, "read": False, "parsed": False, "decoded": False, "imported": False, "compiled": False, "executed": False},
        "C65_v9_release": release,
        "partition": {"total_collision2_handoff_children": 167255, "decision_source_children": 33100, "blocker_source_children": 134155, "identity": "167255=33100+134155"},
        "blocker_terminal_census": {"whole_child_strict_exclusion": exclusion, "cemetery_tangency_terminal": cemetery, "sealed_collision3_handoff": 0, "residual": 0, "identity": "134155=110904+23251"},
        "decision_source_disposition": {"H1_full_box_closed": 33100, "frozen_downstream_terminal_predicate_present": 0, "sealed_collision3_handoff": 0, "residual": decision_residual, "reason": "C69C_C71B_H1_GEOMETRY_IS_CONSUMER_REVIEW_READY_NOT_A_TERMINAL"},
        "sources": {"total": 20879, "C69c_decision": 2356, "C69c_blocker": 18523, **source_census},
        "reflection_pairs": {"total": 12, "candidate_whole_terminal": roll["whole_reflection_pair_terminal_count"], "residual": roll["residual_reflection_pair_count"], "prefix_free_and_Kraft_one": 12},
        "singleton_cells": {"total": 24, "candidate_whole_terminal": roll["closed_singleton_cell_count"], "residual": roll["residual_singleton_cell_count"], "atomic_install_condition": "24_OF_24_REQUIRED"},
        "public_global_unresolved_before": 1148,
        "candidate_public_unresolved_decrement": 0,
        "candidate_public_unresolved_after": 1148,
        "credit_boundary": {"formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0, "global_installed_credit": 0, "whole_parent_credit": 0},
        "canonical_pointer_or_seal_written": False,
        "prepublication_fail_closed_history": [
            {"attempt": 1, "output_created": False, "reason": "CONSUMER_ENUMERATION_EXPECTED_SCOPE_BOUNDARY_BUT_FROZEN_ENUMERATION_IS_ATLAS_SCOPE_BOUNDARY_FACE", "superseded_by_this_source": True},
            {"attempt": 2, "output_created": False, "reason": "C74_C75_CROSS_SCOPE_KEY_USED_ONLY_CHILD_ID_INSTEAD_OF_PHYSICAL_CHILD_PLUS_EXACT_FACE", "superseded_by_this_source": True},
            {"attempt": 3, "output_created": False, "reason": "C74_ENDPOINT_PAIR_INDEX_IS_NESTED_IN_EXACT_FACE_NOT_TOP_LEVEL", "superseded_by_this_source": True},
            {"attempt": 4, "output_created": False, "reason": "PAIR_KRAFT_FRONTIER_OMITTED_PUBLISHED_C57_STRICT_TERMINAL_CARRY_AND_USED_ONLY_C58_REFINEMENT_OUTPUTS", "superseded_by_this_source": True},
        ],
        "preflight_fail_closed_history": [
            {"output_created": False, "reason": "C75_CURRENT_OCCURRENCE_HALF_OPEN_OWNER_IS_FALSE_ON_LEGITIMATE_NONOWNER_SIDE_OF_DEGREE_TWO_INCIDENCE", "corrected_by_pairwise_OWNER_VALIDATION": True},
            {"output_created": False, "reason": "C58_PARENT_PATH_NAMES_IMMEDIATE_REFINEMENT_PARENT_NOT_C57_SOURCE_ROOT", "corrected_by_exact_ancestor_and_additional_depth_validation": True},
        ],
        "dual_input_stage_bytes_identical_count": len(duals),
        "input_pin_count": len(CAPTURES),
        "input_capture_order_sha256": sha(cbytes([[k, v["sha256"]] for k, v in CAPTURES.items()])),
        "producer_file_sha256": sha(Path(__file__).read_bytes()),
    }
    bundle = publish(outdir, result, incidence, [
        ("child_dispositions", child_rows),
        ("source_rollups", source_rows),
        ("reflection_pair_rollups", pair_rows),
        ("singleton_cell_rollups", cell_rows),
    ])
    print(cbytes({
        "status": "PASS",
        "output_dir": str(outdir),
        "result_file_sha256": sha(cbytes(bundle["result"]) + b"\n"),
        "result_object_sha256": bundle["result"]["object_sha256"],
        "manifest_file_sha256": bundle["manifest"]["sha256"],
        "outer_file_sha256": sha(cbytes(bundle["outer"]) + b"\n"),
        "outer_object_sha256": bundle["outer"]["object_sha256"],
        "candidate_public_unresolved_decrement": 0,
    }).decode())


if __name__ == "__main__":
    main()
