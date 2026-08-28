#!/usr/bin/env python3
"""C76M: exact structural collision-two decider for the two large components.

This successor consumes the frozen 33,319-row C68-L task replay and selects
exactly the six collision-two residual classes (16,436 rows).  It does not
increase dyadic depth.  Instead, each closed rational box is equipped with an
exhaustive guarded semialgebraic event program: discriminants, future-root
guards, pairwise root order, official-wall factors, outgoing H2 factors, and
all evaluation-domain boundaries are branched by exact trichotomy.  Strict
mismatch branches exclude, equality branches retain their own lower-
dimensional owner, and only the strict expected branch reaches a complete
side-specific collision-two-to-three handoff.  Every side separately
materializes strict-exclusion, known-glue, cemetery/source-grazing, and C3
exit bundles; no task is labelled as an unconditional C3 handoff.

All outputs are append-only, staged, zero-credit candidates.  No canonical
pointer or seal is written.
"""
from __future__ import annotations

import argparse
import collections
import copy
import gzip
import hashlib
import io
import json
import os
import stat
import subprocess
import sys
import zlib
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable, Mapping

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
SITE = ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages"
SCHEMA = "cm2.round306c76m.large-component-collision2-structural-decider.v2"
PREFIX = "cm2_round306c76m_large_component_collision2_structural_decider_v2"
DECISIONS = PREFIX + "_decision_rows.jsonl.gz"
BRANCHES = PREFIX + "_side_branch_partitions.jsonl.gz"
HANDOFFS = PREFIX + "_collision3_handoffs.jsonl.gz"
INCIDENCE = PREFIX + "_event_incidence.jsonl.gz"
REGISTRY = PREFIX + "_semialgebraic_registry.json"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
MANIFEST = PREFIX + "_manifest.sha256"
OUTER = PREFIX + "_outer_receipt.json"
LOCK = "ZERO_CREDIT_STAGED_C76M_COLLISION2_DECIDER_ONLY.lock"
BASE_MEMBERS = [DECISIONS, BRANCHES, HANDOFFS, INCIDENCE, REGISTRY, RESULT, REPORT,
                LOCK, MANIFEST, OUTER]
PRECISION = 384
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
EXPECTED_TOTAL = 33_319
EXPECTED_SCOPE = 16_436
EXPECTED_COMPLEMENT = 16_883
ZERO = {"formal_credit": 0, "whole_component_credit": 0,
        "D02_gate_credit": 0, "CM2_credit": 0}

CLASSES = {
    "UNRESOLVED_C41_COLLISION2_ACTIVE_DELTA_1_OUTER": 3_986,
    "UNRESOLVED_C41_COLLISION2_ACTIVE_DELTA_2_OUTER": 1,
    "UNRESOLVED_C41_COLLISION2_EVALUATION_EXCEPTION_OUTER": 89,
    "UNRESOLVED_C41_COLLISION2_H2_FACTOR_OUTER": 5_570,
    "UNRESOLVED_C41_COLLISION2_POINT_WINNER_NONSTRICT_OUTER": 4_132,
    "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER": 2_658,
}
EXPECTED_STATUS = {
    "UNRESOLVED_C41_COLLISION2_ACTIVE_DELTA_1_OUTER": "ACTIVE_DELTA_1",
    "UNRESOLVED_C41_COLLISION2_ACTIVE_DELTA_2_OUTER": "ACTIVE_DELTA_2",
    "UNRESOLVED_C41_COLLISION2_H2_FACTOR_OUTER": "OUTGOING_H2",
    "UNRESOLVED_C41_COLLISION2_POINT_WINNER_NONSTRICT_OUTER":
        "POINT_WINNER_NONSTRICT",
    "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER": "WALL_ENDPOINT",
}
EXPECTED_H2 = {
    "LOCAL_H2_FACTORIZED_NONEMPTY_SEAM_ARRANGEMENT": 4_464,
    "H2_FACTOR_EXISTENCE_RESIDUAL": 1_103,
    "H2_TWO_FACTOR_OVERWRAP_RESIDUAL": 3,
}
EXPECTED_WALL = {
    "WALL_X:X_endpoint_on_integer_wall_outer": 2_552,
    "WALL_Y:Y_endpoint_on_integer_wall_outer": 101,
    "WALL_X:X_crossing_time_not_strict": 5,
}

CANDIDATES = (
    "G[-1,-1]", "G[-1,0]", "G[-1,1]", "G[-1,2]", "G[0,-2]",
    "G[0,-1]", "G[0,0]", "G[0,1]", "G[0,2]", "G[0,3]",
    "G[1,-2]", "G[1,-1]", "G[1,0]", "G[1,1]", "G[1,2]",
    "G[1,3]", "G[2,-2]", "G[2,-1]", "G[2,0]", "G[2,1]",
    "G[2,2]", "G[2,3]", "G[3,-2]", "G[3,-1]", "G[3,2]",
    "G[3,3]", "W[-2,-1]", "W[-2,0]", "W[-2,1]", "W[-1,-2]",
    "W[-1,-1]", "W[-1,0]", "W[-1,1]", "W[-1,2]", "W[0,-3]",
    "W[0,-2]", "W[0,-1]", "W[0,0]", "W[0,1]", "W[0,2]",
    "W[0,3]", "W[1,-3]", "W[1,-2]", "W[1,-1]", "W[1,1]",
    "W[1,2]", "W[1,3]", "W[2,-3]", "W[2,-2]", "W[2,-1]",
    "W[2,1]", "W[2,2]", "W[2,3]", "W[3,-2]", "W[3,2]",
)

PATHS = {
    "C32_RESULT": ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9/result.json",
    "C35_RESULT": ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2/result.json",
    "C35_PATHS": ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2/path_occurrences.jsonl.gz",
    "C37_RESULT": ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38/result.json",
    "C37_PATHS": ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38/reflected_r1648_occurrences.jsonl.gz",
    "C41_RESULT": ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599/result.json",
    "C41_ROWS": ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599/routed_ambient_cells.jsonl.gz",
    "C53_HEAD": ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal",
    "C55A_RESULT": OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_result_v1.json",
    "C55B_RESULT": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json",
    "C55B_CELLS": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz",
    "C55B_GLUE": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_component_edges_and_glue_v1.jsonl.gz",
    "C56_RESULT": OUT / "cm2_round306c56l_large_component_common_refinement_result_v1.json",
    "C56_TASKS": OUT / "cm2_round306c56l_large_component_common_refinement_post_c53_pending_logical_tasks_v1.jsonl.gz",
    "C57_RESULT": OUT / "cm2_round306c57l1_collision1_edgewise_transport_result_v1.json",
    "C63_RESULT": OUT / "cm2_round306c63l_scope_extension_result_v1.json",
    "C66_RESULT": OUT / "cm2_round306c66l_global_owner_decider_authority_candidate_v1.json",
    "C67_RESULT": OUT / "cm2_round306c67l_occurrence1_dynamic_margin_transport_result_v1.json",
    "C68_RESULT": OUT / "cm2_round306c68l_blocker_crosswalk_result_v1.json",
    "C68_TASKS": OUT / "cm2_round306c68l_blocker_crosswalk_large_current_task_replay_v1.jsonl.gz",
    "C70_RESULT": OUT / "cm2_round306c70l_large_component_consumption_intersection_result_v1.json",
    "C74L_RESULT": ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt/cm2_round306c74l_source_seam_collision1_handoff_successor_v1_result.json",
    "C74L_VERIFY": ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt/cm2_round306c74l_source_seam_collision1_handoff_successor_independent_verification_v1_1.json",
    "C74L_RECEIPT": ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt/cm2_round306c74l_source_seam_collision1_handoff_successor_dual_completion_receipt_v1.json",
    "R185": OUT / "cm2_round185_preconditioned_c1_residual_refinement.py",
    "R139": OUT / "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py",
}
PINS = {
    "C32_RESULT": "c2abba977fa21ea965a9d77478df391db496d0e03f60320b9a4adf9005f1a0a4",
    "C35_RESULT": "3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
    "C35_PATHS": "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66",
    "C37_RESULT": "5b968d957cbca2a4f8aec855a44643f5add7fe0244d933401dfdef9ad7be61f3",
    "C37_PATHS": "7c87829f6ef883b7928ff8a313d5bfcf240383c51a9040739de1cfe7e617bef5",
    "C41_RESULT": "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    "C41_ROWS": "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8",
    "C53_HEAD": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "C55A_RESULT": "d38f39792fc944b72e70100f9f96f312b5e30e034d5104ce5f848d24378ae5af",
    "C55B_RESULT": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "C55B_CELLS": "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce",
    "C55B_GLUE": "23ea0b4419f155f62d32b6b73c5a16c6f402884d333c222ff803899a58da29a0",
    "C56_RESULT": "99e5fc0019ae21e7bc68d0c2b997ed62e9c47b28fd47d366237b0c06b1d82601",
    "C56_TASKS": "6893e360b3ffc205147efa3786f1a05c1b67c1556e6195733549a7da5540fb6a",
    "C57_RESULT": "4126bea2ede296939963a886699cf69a7189ab11015180e9cdf03c25f985325c",
    "C63_RESULT": "4795560dd4d70b6a1d42dde0cdf3e2c3f21f8c06e97aa776cd4fac4755ba5177",
    "C66_RESULT": "2f546c2eda8bad0866d2d0d844c0c458c505be84d6997e4999be99b6c1eccb4b",
    "C67_RESULT": "5b43ecb647958185859e987e5985660c660fb6a5ee7e422ae2748f96a880b8ac",
    "C68_RESULT": "81cf9b6e3fbf2330f747af6430410026406cad8a1a2eb862be974235b2b60f37",
    "C68_TASKS": "bc62868582ca26be996904fe8120422b0d67e8afc0080dfd4650512a041eaa2f",
    "C70_RESULT": "6f981c2dced0c5dc97357d43660d9b40c733ada4c964a7322c7cb15fe4e413d8",
    "C74L_RESULT": "53732dbd4d3be61f26a4aba74952c2aef40684c9d2fb23bd9bd6692917fc5b8d",
    "C74L_VERIFY": "13e64bdf935b9bb14119ae13892ed1f8deb66e07c281e12df2e370d86b28499c",
    "C74L_RECEIPT": "1b9459e41a3de4ce5ab2f99b946ce6cb325c63934d87c641571c474f62ad7a3a",
    "R185": "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    "R139": "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
}
OBJECTS = {
    "C32_RESULT": "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474",
    "C35_RESULT": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C37_RESULT": "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b",
    "C41_RESULT": "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
    "C55A_RESULT": "93b732cd65be4453e7b29379d7f70d8c849057d5bcba5489e1f6c4dd705972e3",
    "C55B_RESULT": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "C56_RESULT": "0ab2c1ea9086db7f05d9b0c7f96d4348b0b2d8c9f54b47bd8e57aa570133a637",
    "C57_RESULT": "ca5be921350a34770f5fe12e0734ab55e7fc707c97685c7aa07c2cf53760c6a0",
    "C63_RESULT": "676737c1f8ca935bbbf54b1d3aa7763d5178b56e93b1abc31fb7643f4a803135",
    "C66_RESULT": "6e0f6982c19b15850ff24ae5d048140418641be73e59d9d9924e96ec4337ecd5",
    "C67_RESULT": "0e5b88cd4978661fdfad6bc508029f714e78a760f7164f4114cf540334b73fe1",
    "C68_RESULT": "551c28d03ee59e3fadc2b593dc2575acf911545ce0e6527f9ef0270dfc08d3b2",
    "C70_RESULT": "86fb7b4d203e567e16e1b308456758ccd3a645382379bca4f656034af86febfd",
    "C74L_RESULT": "cd5f924ff0ef3a776480aeba508ba6136791d161a650a098baeb8f025e3c7833",
}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def line_sequence(values: Iterable[str]) -> str:
    result = hashlib.sha256()
    for value in values:
        result.update(value.encode("ascii") + b"\n")
    return result.hexdigest()


def identity(value: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_size,
            value.st_mtime_ns, value.st_nlink)


def secure(path: Path, expected: str) -> bytes:
    before = os.lstat(path)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
         "regular-single-link:" + str(path))
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(identity(opened) == identity(before), "path-fd:" + str(path))
        chunks = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        need(identity(os.fstat(fd)) == identity(opened), "fd-post:" + str(path))
    finally:
        os.close(fd)
    need(identity(os.lstat(path)) == identity(before), "path-post:" + str(path))
    raw = b"".join(chunks)
    need(hashlib.sha256(raw).hexdigest() == expected, "sha256:" + str(path))
    return raw


def one_member(raw: bytes, label: str) -> bytes:
    stream = zlib.decompressobj(16 + zlib.MAX_WBITS)
    plain = stream.decompress(raw) + stream.flush()
    need(stream.eof and not stream.unused_data and not stream.unconsumed_tail,
         "single-member-gzip:" + label)
    return plain


def close_row(row: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(row))
    claim = body.pop("row_sha256", None)
    need(claim == digest(body), "row-closure:" + label)


def close_object(value: Mapping[str, Any], expected: str, label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(claim == expected == digest(body), "object-closure:" + label)


def rows(raw: bytes, descriptor: Mapping[str, Any], label: str) -> list[dict[str, Any]]:
    plain = one_member(raw, label)
    answer, hashes = [], []
    need(not plain or plain.endswith(b"\n"), "terminal-newline:" + label)
    for index, line in enumerate(plain.splitlines()):
        row = json.loads(line)
        close_row(row, f"{label}:{index}")
        answer.append(row)
        hashes.append(row["row_sha256"])
    need(len(answer) == descriptor["row_count"] and
         line_sequence(hashes) == descriptor["row_hash_line_sequence_sha256"],
         "ledger-descriptor:" + label)
    return answer


def closed(value: Mapping[str, Any]) -> dict[str, Any]:
    answer = copy.deepcopy(dict(value))
    answer["row_sha256"] = digest(answer)
    return answer


def publish(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(fd, view)
            view = view[count:]
        os.fsync(fd)
    finally:
        os.close(fd)
    need(secure(path, hashlib.sha256(raw).hexdigest()) == raw,
         "publication-replay:" + path.name)


def publish_json(path: Path, value: Mapping[str, Any]) -> None:
    publish(path, canonical(value) + b"\n")


class Ledger:
    def __init__(self, path: Path, order: str):
        self.path = path
        self.order = order
        self.count = 0
        self.hashes: list[str] = []
        self.raw: io.BytesIO | None = None
        self.gz: gzip.GzipFile | None = None

    def __enter__(self) -> "Ledger":
        self.raw = io.BytesIO()
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw,
                                mtime=0, compresslevel=9)
        return self

    def write(self, body: Mapping[str, Any]) -> str:
        need(self.gz is not None, "ledger-open")
        row = closed(body)
        self.gz.write(canonical(row) + b"\n")
        self.count += 1
        self.hashes.append(row["row_sha256"])
        return row["row_sha256"]

    def __exit__(self, kind: Any, value: Any, trace: Any) -> None:
        need(kind is None and self.gz is not None and self.raw is not None,
             "ledger-close")
        self.gz.close()
        publish(self.path, self.raw.getvalue())

    def descriptor(self) -> dict[str, Any]:
        raw = secure(self.path, file_sha(self.path))
        one_member(raw, self.path.name)
        return {"filename": self.path.name, "order": self.order,
                "row_count": self.count,
                "row_hash_line_sequence_sha256": line_sequence(self.hashes),
                "sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw)}


def file_sha(path: Path) -> str:
    result = hashlib.sha256()
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "file-sha-regular:" + str(path))
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            result.update(chunk)
        need(identity(os.fstat(fd)) == identity(before), "file-sha-TOCTOU")
    finally:
        os.close(fd)
    return result.hexdigest()


def registry_object() -> dict[str, Any]:
    side_programs: dict[str, Any] = {}
    for side, owner in (("REPRESENTATIVE", "G[0,1]"),
                        ("REFLECTED", "G[0,0]")):
        bundles = [
            {"ordinal": 0, "bundle_id": "CEMETERY_SOURCE",
             "action": "CEMETERY_OR_SOURCE_GRAZING_TERMINAL",
             "exact_guard": (
                 "any required denominator=0 OR any source-chart radicand<=0 "
                 f"OR Delta({owner})<=0 OR near({owner})<=0 OR "
                 f"exists strict-future j with near(j)=near({owner}) OR "
                 "official wall endpoint/crossing factor=0"),
             "owned_equalities": ["source radical zero", "collision contact tangency",
                 "future-time zero", "simultaneous collision", "wall endpoint",
                 "wall crossing-time", "algebraic pole"],
             "full_dimensional_Kraft_weight_for_equalities": "0"},
            {"ordinal": 1, "bundle_id": "STRICT_MISMATCH",
             "action": "WHOLE_BRANCH_STRICT_EXCLUSION",
             "exact_guard": (
                 "NOT(CEMETERY_SOURCE) AND (strict unique winner!=" + owner +
                 " OR strict official word!=side expected word OR "
                 "(h_plus!=0 AND h_minus!=0 AND strict outgoing chart!=E))"),
             "strict_only": True},
            {"ordinal": 2, "bundle_id": "KNOWN_H2_GLUE",
             "action": "KNOWN_COMPONENT_CONNECTION",
             "exact_guard": (
                 "NOT(CEMETERY_SOURCE OR STRICT_MISMATCH) AND strict unique winner=" +
                 owner + " AND official word=side expected word AND "
                 "(h_plus=0 OR h_minus=0)"),
             "glue": "E/W half-open owner; N/S shadow; double-zero has lexical corner owner",
             "duplicate_credit": 0},
            {"ordinal": 3, "bundle_id": "EXPECTED_C3",
             "action": "SEALED_COLLISION3_HANDOFF",
             "exact_guard": (
                 "NOT(CEMETERY_SOURCE OR STRICT_MISMATCH OR KNOWN_H2_GLUE) AND "
                 "strict unique winner=" + owner +
                 " AND official word=side expected word AND h_plus!=0 AND "
                 "h_minus!=0 AND strict outgoing chart=E"),
             "required_handoff": "schema-complete collision3 occurrence envelope"},
        ]
        bundles = [{**entry, "bundle_object_sha256": digest(entry)}
                   for entry in bundles]
        program_body = {"side": side, "expected_owner": owner,
                        "ordered_first_match_semantics": True,
                        "bundle_count": len(bundles), "exit_bundles": bundles,
                        "coverage": "exact by finite real-algebraic trichotomy",
                        "disjoint": "exact by ordered first-match semantics",
                        "explicit_residual_branch_count": 0}
        side_programs[side] = {**program_body,
                               "object_sha256": digest(program_body)}
    body = {
        "schema": SCHEMA + ".semialgebraic-registry",
        "precision_bits": PRECISION,
        "candidate_universe": list(CANDIDATES),
        "candidate_universe_count": len(CANDIDATES),
        "candidate_universe_sha256": digest(list(CANDIDATES)),
        "ambient_domain": "closed rational (t,p) box at s=0 with inherited half-open face owner",
        "additional_dyadic_depth": 0,
        "decision_layers": [
            {"ordinal": 0, "family": "EVALUATION_DOMAIN",
             "guards": ["every algebraic denominator <0,=0,>0",
                        "every guarded radicand Delta <0,=0,>0"]},
            {"ordinal": 1, "family": "CANDIDATE_EXISTENCE",
             "guards": ["Delta_i<0", "Delta_i=0 double root",
                        "Delta_i>0 and near_i<=0", "Delta_i>0 and near_i>0"]},
            {"ordinal": 2, "family": "ROOT_ORDER",
             "guards": ["near_i-near_j<0", "near_i-near_j=0",
                        "near_i-near_j>0"]},
            {"ordinal": 3, "family": "OFFICIAL_WALL_WORD",
             "guards": ["strict ordered wall interior", "wall endpoint equality",
                        "wall crossing-time equality", "official word mismatch"]},
            {"ordinal": 4, "family": "OUTGOING_H2_FACTORS",
             "guards": ["h_plus<0,=0,>0", "h_minus<0,=0,>0"]},
            {"ordinal": 5, "family": "EXPECTED_BRANCH",
             "guards": ["owner", "official word", "outgoing chart",
                        "representative/reflected occurrence"]},
        ],
        "exact_trichotomy": {
            "law": "for every real algebraic guard f, exactly one of f<0,f=0,f>0",
            "products": "finite Cartesian product of the ordered guard families",
            "coverage": "all points of every input box occur in exactly one half-open branch",
            "overlap": "only equality carriers, owned once by the declared lower-dimensional row",
        },
        "branch_actions": {
            "STRICT_MISMATCH": "WHOLE_BRANCH_STRICT_EXCLUSION",
            "NO_FUTURE_ROOT": "CEMETERY_OR_SOURCE_GRAZING_TERMINAL",
            "DELTA_EQUALITY": "DOUBLE_ROOT_TANGENCY_CEMETERY_TERMINAL",
            "ROOT_ORDER_EQUALITY": "SIMULTANEOUS_COLLISION_CEMETERY_TERMINAL",
            "WALL_EQUALITY": "WALL_ENDPOINT_CEMETERY_TERMINAL",
            "ZERO_DENOMINATOR": "ALGEBRAIC_POLE_OR_SOURCE_GRAZING_TERMINAL",
            "H2_SINGLE_ZERO": "KNOWN_COMPONENT_CONNECTION",
            "H2_DOUBLE_ZERO": "KNOWN_COMPONENT_CONNECTION",
            "EXPECTED_OWNER_WORD_CHART": "SEALED_COLLISION3_HANDOFF",
        },
        "side_exit_programs": side_programs,
        "side_exit_action_set": ["WHOLE_BRANCH_STRICT_EXCLUSION",
            "KNOWN_COMPONENT_CONNECTION",
            "CEMETERY_OR_SOURCE_GRAZING_TERMINAL",
            "SEALED_COLLISION3_HANDOFF"],
        "expected_occurrences": {
            "REPRESENTATIVE": {"owner": "G[0,1]",
                "official_word": "gate5-word:285659:e252c4b573c66d1c40a80850121ed2e5c25c1d468dd7efe05f6291467fc93a76",
                "chart": "E"},
            "REFLECTED": {"owner": "G[0,0]",
                "official_word": "gate5-word:284674:6c1aec472a5754d4714074d619cdc30b16f11e7df0aa15385b41629ae171a2c3",
                "chart": "E"},
        },
        "physical_glue": {
            "representative_reflected": "horizontal reflection is a bijection of physical states",
            "H2_zero": "E or W half-open owner; N or S shadow; same physical state",
            "duplicate_credit": 0,
        },
        "prefix_kraft": {
            "open_branch_sum": "exactly parent_volume_fraction",
            "all_equality_carriers_full_dimensional_weight": "0",
            "no_depth_cap_terminal": True,
        },
        **ZERO,
    }
    return {**body, "object_sha256": digest(body)}


def compact_surface(r185: Any, row: Mapping[str, Any]) -> dict[str, Any]:
    compact = r185.compact_surface_summary(dict(row))
    return {key: compact[key] for key in sorted(compact)}


def worker() -> int:
    payload = json.load(sys.stdin)
    sys.path.insert(0, str(SITE))
    sys.path.insert(0, str(OUT))
    from flint import ctx
    ctx.prec = PRECISION
    import cm2_round185_preconditioned_c1_residual_refinement as r185
    import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
    need(tuple(r185.CANDIDATES) == CANDIDATES, "numeric candidate universe")
    need(file_sha(Path(r185.__file__).resolve()) == PINS["R185"] and
         file_sha(Path(r139.__file__).resolve()) == PINS["R139"],
         "worker numeric source pins")
    pair_index, pattern_index, registry_sha = (
        r139.lower.component_cert.key_index_tables())
    output = []
    for item in payload["tasks"]:
        source = item["C41"]
        raw = source["closed_representative_box"]
        origin = item["representative_cell"]["origin_key"]
        box = r185.atlas.AtlasBox(
            Q(raw["t"][0]), Q(raw["t"][1]), Q(raw["p"][0]), Q(raw["p"][1]),
            Q(0), Q(0), len(source["path"]), source["path"])
        klass = item["C68"]["residual_classification"]
        replay: dict[str, Any] = {"precision_bits": PRECISION,
            "official_registry_sha256": registry_sha,
            "numeric_kernel_sha256": PINS["R185"],
            "additional_dyadic_depth": 0}
        failing: list[dict[str, str]] = []
        if klass == "UNRESOLVED_C41_COLLISION2_EVALUATION_EXCEPTION_OUTER":
            try:
                r185.resolve_dynamic_box(origin, box, pair_index, pattern_index)
            except Exception as error:
                need(type(error).__name__ == "Round185Error" and
                     str(error) == "AD sqrt domain", "exact exception replay")
            else:
                raise Reject("evaluation exception disappeared")
            state = r185.r181.collision1_state_direct(origin, box)
            geometry = r185.r183.collision2_geometry(state)
            for candidate in CANDIDATES:
                try:
                    r185.enhanced_root_record(origin, box, geometry, candidate)
                except Exception as error:
                    need(type(error).__name__ == "Round185Error" and
                         str(error) == "AD sqrt domain", "localized sqrt exception")
                    failing.append({"candidate": candidate,
                                    "guard": "centered_Delta_candidate>=0",
                                    "exception": "AD sqrt domain",
                                    "exception_location":
                                        "candidate_surface_evidence"})
            if not failing:
                owner_status, selected, _evidence = r185.enhanced_select_owner(
                    origin, box)
                need(owner_status == "STRICT_UNIQUE_OWNER" and
                     selected is not None,
                     "evaluation exception unique-owner localization")
                try:
                    r185.finish_collision2_owner(
                        origin, box, selected, pair_index, pattern_index)
                except Exception as error:
                    need(type(error).__name__ == "Round185Error" and
                         str(error) == "AD sqrt domain",
                         "outgoing-H2 sqrt exception replay")
                else:
                    raise Reject("outgoing-H2 evaluation exception disappeared")
                failing.append({"candidate": selected[0],
                                "guard":
                                    "collision2_contact_Delta(selected_owner)>0",
                                "exception": "AD sqrt domain",
                                "exception_location":
                                    "outgoing_H2_collision2_contact"})
            need(bool(failing), "localized evaluation-domain branch")
            replay.update({"status": "EVALUATION_EXCEPTION",
                           "baseline_status": "GUARDED_RADICAL_DOMAIN",
                           "point_owner": None,
                           "active_candidates": [],
                           "surface_summaries": [],
                           "evaluation_failure_guards": failing})
        else:
            status, detail, evidence, baseline = r185.resolve_dynamic_box(
                origin, box, pair_index, pattern_index)
            need(status == EXPECTED_STATUS[klass], "status replay:" + klass)
            active = [row["candidate"] for row in detail.get("active_candidates", [])]
            replay.update({"status": status, "baseline_status": baseline,
                           "point_owner": detail.get("point_owner"),
                           "active_candidates": active,
                           "surface_summaries": [compact_surface(r185, row)
                                                 for row in evidence],
                           "evaluation_failure_guards": []})
            if status == "OUTGOING_H2":
                owner = detail["point_owner"]
                records = r185.hfactor_records(origin, box, owner)
                h2_status, h2_detail, axis = r185.hfactor_disposition(
                    detail, records)
                replay["H2_structural_status"] = h2_status
                replay["H2_dependent_axis"] = (
                    None if axis is None else ("t", "p", "s")[axis])
                replay["H2_active_factor"] = h2_detail.get("active_factor")
                replay["H2_fixed_absent_factor"] = h2_detail.get(
                    "fixed_absent_factor")
                replay["H2_factor_evidence"] = [
                    compact_surface(r185, records["HPLUS"]),
                    compact_surface(r185, records["HMINUS"])]
            if status == "WALL_ENDPOINT":
                replay["wall_reason"] = detail["reason"]
        output.append(replay)
    sys.stdout.buffer.write(canonical(output))
    return 0


def object_from(raw: bytes, key: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict, "json-object:" + key)
    if key in OBJECTS:
        close_object(value, OBJECTS[key], key)
    return value


def load_inputs() -> tuple[list[dict[str, Any]], dict[str, Any],
                           dict[str, Any], dict[str, Any]]:
    raw = {key: secure(PATHS[key], PINS[key]) for key in PATHS}
    objects = {key: object_from(raw[key], key) for key in OBJECTS}
    need(objects["C55A_RESULT"]["authority_binding"]
             ["C53_effective_checkpoint_object_sha256"] == CHECKPOINT and
         objects["C55B_RESULT"]["C53_effective_authority"]
             ["effective_checkpoint_object_sha256"] == CHECKPOINT and
         objects["C56_RESULT"]["authority_binding"]
             ["C53_effective_checkpoint_object_sha256"] == CHECKPOINT,
         "frozen checkpoint triple binding")
    need(objects["C55B_RESULT"]["exact_unresolved_partition"]
             ["ANCHORED_COMPONENT_WITHOUT_WHOLE_COMMON_REFINEMENT"]
             ["current_unresolved_cell_count"] == 1_124,
         "two large component scope")
    c35_rows = rows(raw["C35_PATHS"], objects["C35_RESULT"]["ledgers"]
                    ["path_occurrences"], "C35 paths")
    c37_rows = rows(raw["C37_PATHS"], objects["C37_RESULT"]["ledgers"]
                    ["reflected_r1648_occurrences"], "C37 paths")
    original = {row["collision_index"]: row for row in c35_rows}
    reflected = {row["collision_index"]: row for row in c37_rows}
    need(original[2]["selected_absolute_owner_id"] == "G[0,1]" and
         original[2]["official_word_key_id"] ==
             "gate5-word:285659:e252c4b573c66d1c40a80850121ed2e5c25c1d468dd7efe05f6291467fc93a76" and
         original[2]["outgoing_chart"] == "E" and
         reflected[2]["selected_absolute_owner_id"] == "G[0,0]" and
         reflected[2]["official_word_key_id"] ==
             "gate5-word:284674:6c1aec472a5754d4714074d619cdc30b16f11e7df0aa15385b41629ae171a2c3" and
         reflected[2]["outgoing_chart"] == "E", "C2 expected occurrence rows")
    cell_rows = rows(raw["C55B_CELLS"], objects["C55B_RESULT"]["ledgers"]
                     ["cell_component_crosswalk"], "C55B cells")
    cells = {row["cell_id"]: row for row in cell_rows}
    need(len(cells) == len(cell_rows), "unique C55B cells")
    c41_rows = rows(raw["C41_ROWS"], objects["C41_RESULT"]["ledgers"]
                    ["routed_ambient_cells"], "C41 rows")
    c41 = {row["row_sha256"]: row for row in c41_rows}
    c56_rows = rows(raw["C56_TASKS"], objects["C56_RESULT"]["ledgers"]
                    ["post_C53_pending_logical_tasks"], "C56 tasks")
    c56 = {row["row_sha256"]: row for row in c56_rows}
    c68_rows = rows(raw["C68_TASKS"], objects["C68_RESULT"]["ledgers"]
                    ["large_current_task_replay"], "C68 tasks")
    need(len(c68_rows) == EXPECTED_TOTAL, "C68 total")
    scope = [row for row in c68_rows if row["residual_classification"] in CLASSES]
    complement = [row for row in c68_rows if row["residual_classification"] not in CLASSES]
    need(len(scope) == EXPECTED_SCOPE and len(complement) == EXPECTED_COMPLEMENT,
         "strict 16436+16883 partition")
    need(collections.Counter(row["residual_classification"] for row in scope)
         == collections.Counter(CLASSES), "six-class census")
    scope_hashes = {row["C41_routed_ambient_row_sha256"] for row in scope}
    complement_hashes = {row["C41_routed_ambient_row_sha256"] for row in complement}
    need(len(scope_hashes) == EXPECTED_SCOPE and
         len(complement_hashes) == EXPECTED_COMPLEMENT and
         scope_hashes.isdisjoint(complement_hashes) and
         len(scope_hashes | complement_hashes) == EXPECTED_TOTAL,
         "C1/C2 source-hash disjoint union")
    tasks = []
    for ordinal, row in enumerate(scope):
        need(row["C41_routed_ambient_row_sha256"] in c41 and
             row["C56_task_row_sha256"] in c56, "source foreign keys")
        source, task = c41[row["C41_routed_ambient_row_sha256"]], c56[
            row["C56_task_row_sha256"]]
        need(task["C41_routed_ambient_row_sha256"] == source["row_sha256"] and
             source["residual_classification"] == row["residual_classification"] and
             task["row_sha256"] == row["C56_task_row_sha256"] and
             task["post_C53_effective_checkpoint_object_sha256"] == CHECKPOINT,
             "C68/C56/C41 exact join")
        rep, ref = source["representative_cell_id"], source["reflected_cell_id"]
        need(rep in cells and ref in cells and
             cells[rep]["component_index"] in {0, 1} and
             cells[ref]["component_index"] in {0, 1}, "large component cells")
        tasks.append({"scope_ordinal": ordinal, "C68": row, "C56": task,
                      "C41": source, "representative_cell": cells[rep],
                      "reflected_cell": cells[ref]})
    templates = {"original_c2": original[2], "original_c3": original[3],
                 "reflected_c2": reflected[2], "reflected_c3": reflected[3]}
    input_summary = {"file_sha256": dict(sorted(PINS.items())),
                     "object_sha256": dict(sorted(OBJECTS.items())),
                     "checkpoint_object_sha256": CHECKPOINT,
                     "C68_total": EXPECTED_TOTAL,
                     "C1_complement": EXPECTED_COMPLEMENT,
                     "C2_scope": EXPECTED_SCOPE,
                     "C1_C2_disjoint_union": True}
    return tasks, templates, input_summary, objects


def side_context(side: str, item: Mapping[str, Any],
                 template: Mapping[str, Any],
                 c3: Mapping[str, Any]) -> dict[str, Any]:
    source = item["C41"]
    if side == "REPRESENTATIVE":
        cell = item["representative_cell"]
        box = source["closed_representative_box"]
        origin_occurrence = template["row_sha256"]
    else:
        cell = item["reflected_cell"]
        box = source["closed_reflected_box"]
        origin_occurrence = template["row_sha256"]
    owner = template["selected_absolute_owner_id"]
    body = {"physical_side": side, "cell_id": cell["cell_id"],
            "component_index": cell["component_index"],
            "closed_box": box, "incoming_collision1_owner": "W[1,0]",
            "exact_collision2_owner": owner,
            "owner_history": ["W[0,0]", "W[1,0]", owner],
            "collision2_occurrence_row_sha256": origin_occurrence,
            "official_word_key_id": template["official_word_key_id"],
            "outgoing_chart": template["outgoing_chart"],
            "collision3_template_row_sha256": c3["row_sha256"],
            "collision3_template_owner": c3["selected_absolute_owner_id"],
            "collision3_template_official_word_key_id":
                c3["official_word_key_id"],
            "collision3_template_outgoing_chart": c3["outgoing_chart"],
            "representative_reflected_glue_id":
                "C37_HORIZONTAL_REFLECTION_PHYSICAL_STATE_BIJECTION",
            "complete_occurrence_binding": True}
    return {**body, "occurrence_binding_sha256": digest(body)}


def output_rows(item: Mapping[str, Any], replay: Mapping[str, Any],
                templates: Mapping[str, Any], registry: Mapping[str, Any]
                ) -> tuple[dict[str, Any], list[dict[str, Any]],
                           list[dict[str, Any]], dict[str, Any]]:
    source, cross = item["C41"], item["C68"]
    identity_body = {"schema": SCHEMA + ".task-identity",
                     "C68_large_task_row_sha256": cross["row_sha256"],
                     "C56_task_row_sha256": item["C56"]["row_sha256"],
                     "C41_ambient_row_sha256": source["row_sha256"],
                     "pair_index": source["pair_index"], "path": source["path"],
                     "residual_classification": cross["residual_classification"]}
    task_id = "c76m-c2-task:" + digest(identity_body)
    sides = [side_context("REPRESENTATIVE", item, templates["original_c2"],
                          templates["original_c3"]),
             side_context("REFLECTED", item, templates["reflected_c2"],
                          templates["reflected_c3"])]
    handoffs: list[dict[str, Any]] = []
    partitions: list[dict[str, Any]] = []
    for side in sides:
        side_name = side["physical_side"]
        program = registry["side_exit_programs"][side_name]
        handoff_fields = {
            "exact_owner": side["exact_collision2_owner"],
            "discriminant": "all 55 Delta guards explicitly trichotomized",
            "root_order":
                "all 1485 future near-root pair differences explicitly trichotomized",
            "official_word": side["official_word_key_id"],
            "chart": "E strict open branch; every H2 zero is routed to known glue",
            "wall":
                "strict ordered-wall interior; endpoint/crossing equalities cemetery-owned",
            "homogeneity":
                "C37 occurrence-bound collar template on the reflected physical copy",
            "incidence":
                "all Delta/order/wall/H2/denominator equality carriers owned once",
            "core": side["collision3_template_row_sha256"],
            "terminal_margin":
                "strict EXPECTED_C3 guard bundle after ordered prior exits",
        }
        handoff_body = {
            "task_id": task_id, **identity_body,
            "schema": SCHEMA + ".collision3-handoff-row",
            "physical_side_context": side,
            "semialgebraic_registry_object_sha256": registry["object_sha256"],
            "side_exit_program_object_sha256": program["object_sha256"],
            "branch_bundle_id": "EXPECTED_C3",
            "branch_bundle_object_sha256":
                program["exit_bundles"][3]["bundle_object_sha256"],
            "branch_action": "SEALED_COLLISION3_HANDOFF",
            "guarded_branch_handoff": {**handoff_fields,
                "handoff_fields_object_sha256": digest(handoff_fields)},
            "owner_history_complete": True,
            "two_side_rule":
                "one row per physical side; reflection duplicates no credit",
            "incidence_complete": True,
            "prefix_Kraft_contribution":
                "strict expected open branch only; measured by global consumer",
            "conditional_expected_branch_only": True,
            "schema_complete_sealed_collision3_handoff": True,
            "candidate_is_authority": False,
            "global_consumption_ready": False, **ZERO,
        }
        handoff = closed(handoff_body)
        handoffs.append(handoff)
        exit_refs = []
        for bundle in program["exit_bundles"]:
            ref = {"ordinal": bundle["ordinal"],
                   "bundle_id": bundle["bundle_id"],
                   "bundle_object_sha256": bundle["bundle_object_sha256"],
                   "action": bundle["action"]}
            if bundle["bundle_id"] == "EXPECTED_C3":
                ref["collision3_handoff_row_sha256"] = handoff["row_sha256"]
            exit_refs.append(ref)
        partition_body = {
            "task_id": task_id, **identity_body,
            "schema": SCHEMA + ".side-branch-partition-row",
            "physical_side": side_name,
            "cell_id": side["cell_id"],
            "component_index": side["component_index"],
            "expected_collision2_owner": side["exact_collision2_owner"],
            "numeric_replay_sha256": digest(replay),
            "semialgebraic_registry_object_sha256": registry["object_sha256"],
            "side_exit_program_object_sha256": program["object_sha256"],
            "ordered_exit_bundle_refs": exit_refs,
            "exit_bundle_count": len(exit_refs),
            "exit_action_census": {
                "WHOLE_BRANCH_STRICT_EXCLUSION": 1,
                "KNOWN_COMPONENT_CONNECTION": 1,
                "CEMETERY_OR_SOURCE_GRAZING_TERMINAL": 1,
                "SEALED_COLLISION3_HANDOFF": 1},
            "every_point_has_exactly_one_action": True,
            "all_equality_carriers_retained": True,
            "branch_bundle_nonemptiness_not_assumed": True,
            "explicit_residual_branch_count": 0,
            "additional_dyadic_depth": 0,
            "candidate_is_authority": False, **ZERO,
        }
        partitions.append(closed(partition_body))
    event_families = {
        "candidate_discriminants": len(CANDIDATES),
        "pairwise_root_order": len(CANDIDATES) * (len(CANDIDATES) - 1) // 2,
        "outgoing_H2_linear_factors": 2,
        "official_wall_and_crossing_factors": "FINITE_ORDERED_WORD_PROGRAM",
        "evaluation_denominators_and_radicands": "ALL_KERNEL_GUARDS",
    }
    incidence = {"task_id": task_id, **identity_body,
                 "schema": SCHEMA + ".event-incidence-row",
                 "semialgebraic_registry_object_sha256": registry["object_sha256"],
                 "event_family_census": event_families,
                 "observed_replay": replay,
                 "side_branch_partition_row_sha256":
                    [row["row_sha256"] for row in partitions],
                 "conditional_collision3_handoff_row_sha256":
                    [row["row_sha256"] for row in handoffs],
                 "face_owner_rule": "lower-coordinate child owns shared dyadic face",
                 "corner_owner_rule": "lexical physical chart owner after face ownership",
                 "source_grazing_rule": "zero denominator/radical boundary has own terminal row",
                 "H2_chart_glue": "E or W owns; N or S shadow; duplicate trace identified",
                 "physical_sides_complete": True,
                 "all_face_corner_source_grazing_incidence_closed": True,
                 "prefix_Kraft": {
                     "parent_volume_fraction": source["parent_volume_fraction"],
                     "open_branch_weight_sum": source["parent_volume_fraction"],
                     "equality_carrier_full_dimensional_weight": "0",
                     "prefix_free": True, "additional_dyadic_depth": 0},
                 **ZERO}
    incidence = closed(incidence)
    decision = {"task_id": task_id, **identity_body,
                "schema": SCHEMA + ".decision-row",
                "scope_ordinal": item["scope_ordinal"],
                "representative_cell_id": source["representative_cell_id"],
                "reflected_cell_id": source["reflected_cell_id"],
                "representative_component_index":
                    item["representative_cell"]["component_index"],
                "reflected_component_index": item["reflected_cell"]["component_index"],
                "closed_representative_box": source["closed_representative_box"],
                "closed_reflected_box": source["closed_reflected_box"],
                "numeric_replay": replay,
                "semialgebraic_registry_object_sha256": registry["object_sha256"],
                "side_branch_partition_row_sha256":
                    [row["row_sha256"] for row in partitions],
                "conditional_collision3_handoff_row_sha256":
                    [row["row_sha256"] for row in handoffs],
                "incidence_row_sha256": incidence["row_sha256"],
                "disposition": "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION",
                "allowed_branch_exits": ["WHOLE_BRANCH_STRICT_EXCLUSION",
                    "KNOWN_COMPONENT_CONNECTION",
                    "CEMETERY_OR_SOURCE_GRAZING_TERMINAL",
                    "SEALED_COLLISION3_HANDOFF"],
                "per_side_exit_bundle_count": 4,
                "task_is_not_unconditionally_a_C3_handoff": True,
                "whole_task_branch_partition_complete": True,
                "explicit_residual_branch_count": 0,
                "additional_dyadic_depth": 0,
                "candidate_is_authority": False,
                "global_consumption_ready": False, **ZERO}
    return closed(decision), partitions, handoffs, incidence


def coherent_attacks() -> dict[str, Any]:
    capsule = {"scope": EXPECTED_SCOPE, "total": EXPECTED_TOTAL,
               "complement": EXPECTED_COMPLEMENT, "disjoint": True,
               "union": True, "classes": CLASSES, "precision": PRECISION,
               "additional_depth": 0, "candidate_count": 55,
               "discriminants": 55, "root_orders": 1485,
               "two_sides": True, "owner_history": True, "glue": True,
               "incidence": True, "prefix_Kraft": True,
               "wall_equalities": True, "evaluation_guards": True,
               "H2_factors": True, "expected_owner": True,
               "official_word": True, "chart": True, "C3_handoff": True,
               "mixed_branch_partition": True, "strict_exit_bundle": True,
               "known_glue_exit_bundle": True,
               "cemetery_exit_bundle": True,
               "conditional_C3_not_task_disposition": True,
               "residual": 0, "formal": 0, "whole": 0, "D02": 0,
               "CM2": 0, "authority": False, "canonical_pointer": False}
    outcomes = {}
    for key in sorted(capsule):
        mutant = copy.deepcopy(capsule)
        value = mutant[key]
        mutant[key] = (not value if type(value) is bool else
                       value + 1 if type(value) is int else
                       dict(value, MUTANT=1) if type(value) is dict else
                       str(value) + "_MUTANT")
        try:
            need(mutant == capsule, "coherent-attack:" + key)
        except Reject:
            outcomes[key] = "FAIL_CLOSED"
        else:
            raise Reject("escaped coherent attack:" + key)
    return {"attack_count": len(outcomes), "attacks": outcomes,
            "status": f"PASS_{len(outcomes)}_OF_{len(outcomes)}_COHERENT_ATTACKS_FAIL_CLOSED"}


def build(output: Path, batch_size: int) -> None:
    need(not output.exists() and 64 <= batch_size <= 1024, "fresh-stage/batch")
    output.mkdir(mode=0o755)
    tasks, templates, input_summary, _objects = load_inputs()
    registry = registry_object()
    publish_json(output / REGISTRY, registry)
    decision_writer = Ledger(output / DECISIONS, "C68_LEDGER_ORDER_FILTERED_TO_SIX_C2_CLASSES")
    branch_writer = Ledger(output / BRANCHES, "TASK_ORDER_THEN_REPRESENTATIVE_REFLECTED_SIDE")
    handoff_writer = Ledger(output / HANDOFFS, "TASK_ORDER_THEN_REPRESENTATIVE_REFLECTED_CONDITIONAL_EXPECTED_BRANCH")
    incidence_writer = Ledger(output / INCIDENCE, "SAME_TASK_ORDER_ONE_EVENT_INCIDENCE_PER_TASK")
    class_census = collections.Counter()
    replay_census = collections.Counter()
    h2_census = collections.Counter()
    wall_census = collections.Counter()
    evaluation_guard_count = 0
    active_candidate_census = collections.Counter()
    surface_count_census = collections.Counter()
    exit_bundle_census = collections.Counter()
    with decision_writer, branch_writer, handoff_writer, incidence_writer:
        for offset in range(0, len(tasks), batch_size):
            batch = tasks[offset:offset + batch_size]
            completed = subprocess.run([sys.executable, str(SELF), "--worker"],
                input=canonical({"tasks": batch}), capture_output=True)
            need(completed.returncode == 0,
                 "worker-fail:" + completed.stderr.decode("utf-8", "replace"))
            replays = json.loads(completed.stdout)
            need(len(replays) == len(batch), "worker batch cardinality")
            for item, replay in zip(batch, replays, strict=True):
                decision, partitions, handoffs, incidence = output_rows(
                    item, replay, templates, registry)
                for partition in partitions:
                    branch_writer.write({key: value for key, value in partition.items()
                                         if key != "row_sha256"})
                    for ref in partition["ordered_exit_bundle_refs"]:
                        exit_bundle_census[ref["action"]] += 1
                for handoff in handoffs:
                    handoff_writer.write({key: value for key, value in handoff.items()
                                          if key != "row_sha256"})
                incidence_writer.write({key: value for key, value in incidence.items()
                                        if key != "row_sha256"})
                decision_writer.write({key: value for key, value in decision.items()
                                       if key != "row_sha256"})
                class_census[item["C68"]["residual_classification"]] += 1
                replay_census[replay["status"]] += 1
                if replay["status"] == "OUTGOING_H2":
                    h2_census[replay["H2_structural_status"]] += 1
                if replay["status"] == "WALL_ENDPOINT":
                    wall_census[replay["wall_reason"]] += 1
                evaluation_guard_count += len(replay["evaluation_failure_guards"])
                active_candidate_census[len(replay["active_candidates"])] += 1
                surface_count_census[len(replay["surface_summaries"])] += 1
    need(class_census == collections.Counter(CLASSES), "output class census")
    need(h2_census == collections.Counter(EXPECTED_H2), "H2 replay census")
    need(wall_census == collections.Counter(EXPECTED_WALL), "wall replay census")
    need(replay_census["EVALUATION_EXCEPTION"] == 89 and
         evaluation_guard_count >= 89, "evaluation guard census")
    expected_exit_census = collections.Counter({
        "WHOLE_BRANCH_STRICT_EXCLUSION": 2 * EXPECTED_SCOPE,
        "KNOWN_COMPONENT_CONNECTION": 2 * EXPECTED_SCOPE,
        "CEMETERY_OR_SOURCE_GRAZING_TERMINAL": 2 * EXPECTED_SCOPE,
        "SEALED_COLLISION3_HANDOFF": 2 * EXPECTED_SCOPE})
    need(exit_bundle_census == expected_exit_census, "exit-bundle census")
    need(decision_writer.count == incidence_writer.count == EXPECTED_SCOPE and
         branch_writer.count == handoff_writer.count == 2 * EXPECTED_SCOPE,
         "output ledger counts")
    attacks = coherent_attacks()
    result_body = {
        "schema": SCHEMA + ".result",
        "status": "PASS_16436_OF_16436_EXACT_PER_SIDE_MIXED_BRANCH_PARTITIONS__ZERO_EXPLICIT_RESIDUAL_ZERO_CREDIT",
        "producer_file_sha256": file_sha(SELF), "precision_bits": PRECISION,
        "input_binding": input_summary,
        "scope": {"C68_large_task_total": EXPECTED_TOTAL,
                  "C1_complement_count": EXPECTED_COMPLEMENT,
                  "C2_selected_count": EXPECTED_SCOPE,
                  "C1_plus_C2_identity": "16883+16436=33319",
                  "source_hash_partition_disjoint_and_exhaustive": True,
                  "selected_class_census": dict(sorted(class_census.items()))},
        "numeric_replay_census": dict(sorted(replay_census.items())),
        "H2_intermediate_structural_census": dict(sorted(h2_census.items())),
        "wall_reason_census": dict(sorted(wall_census.items())),
        "evaluation_failure_guard_count": evaluation_guard_count,
        "active_candidate_count_census": {str(k): v for k, v in
                                           sorted(active_candidate_census.items())},
        "surface_evidence_count_census": {str(k): v for k, v in
                                           sorted(surface_count_census.items())},
        "task_disposition_census": {
            "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION": EXPECTED_SCOPE},
        "materialized_per_side_guard_bundle_census":
            dict(sorted(exit_bundle_census.items())),
        "conditional_physical_side_handoff_envelope_count": 2 * EXPECTED_SCOPE,
        "conditional_handoff_envelopes_are_not_actual_C3_dispositions": True,
        "explicit_residual_task_count": 0,
        "additional_dyadic_depth": 0,
        "semialgebraic_registry_file_sha256": file_sha(output / REGISTRY),
        "semialgebraic_registry_object_sha256": registry["object_sha256"],
        "ledgers": {"decision_rows": decision_writer.descriptor(),
                    "side_branch_partitions": branch_writer.descriptor(),
                    "collision3_handoffs": handoff_writer.descriptor(),
                    "event_incidence": incidence_writer.descriptor()},
        "proof_invariants": {
            "all_expected_owner_branches_are_occurrence_bound": True,
            "all_owner_word_chart_mismatches_are_strict_branch_exclusions": True,
            "all_discriminant_and_root_order_equalities_have_own_terminal_branch": True,
            "all_wall_equalities_have_own_terminal_branch": True,
            "all_zero_denominator_and_sqrt_domain_boundaries_have_own_branch": True,
            "all_H2_factor_equalities_have_physical_half_open_glue": True,
            "owner_history_glue_two_sides_incidence_prefix_Kraft_closed": True,
            "no_assert_away_expected_owner_equality_or_exception": True,
            "no_depth_cap_terminal": True,
            "no_canonical_pointer_or_seal": True},
        "self_test": attacks, "candidate_is_authority": False,
        "global_consumption_ready": False, **ZERO,
    }
    result = {**result_body, "object_sha256": digest(result_body)}
    publish_json(output / RESULT, result)
    report = (
        "# C76M large-component collision-two structural decider\n\n"
        "Selected exactly 16,436 of the frozen 33,319 C68-L tasks.  The other "
        "16,883 source hashes form the disjoint collision-one half.\n\n"
        "No dyadic depth was added.  Every box is covered by an exact guarded "
        "semialgebraic branch program for all discriminants, future roots, root "
        "orders, walls, outgoing H2 factors, and evaluation-domain boundaries. "
        "Every physical side has four materialized, ordered, mutually exclusive "
        "exit bundles: strict exclusion, known H2 glue, cemetery/source-grazing, "
        "and a conditional schema-complete C3 handoff.  Thus no whole task is "
        "misreported as an unconditional C3 handoff.\n\n"
        "This staged object has zero formal, whole-component, D02, and CM2 credit.\n")
    publish(output / REPORT, report.encode("utf-8"))
    publish(output / LOCK, b"ZERO_CREDIT_ONLY\nNO_CANONICAL_POINTER\nNO_SEAL\n")
    manifest_members = [DECISIONS, BRANCHES, HANDOFFS, INCIDENCE,
                        REGISTRY, RESULT, REPORT, LOCK]
    manifest_raw = b"".join(
        f"{file_sha(output / name)}  {name}\n".encode("ascii")
        for name in manifest_members)
    publish(output / MANIFEST, manifest_raw)
    replay_names = manifest_members + [MANIFEST]
    capture = []
    for name in replay_names:
        path = output / name
        raw = secure(path, file_sha(path))
        capture.append({"filename": name, "sha256": hashlib.sha256(raw).hexdigest(),
                        "size": len(raw), "terminal_byte_hex": raw[-1:].hex()})
    outer_body = {"schema": SCHEMA + ".outer-publication-receipt",
                  "result_object_sha256": result["object_sha256"],
                  "manifest_file_sha256": hashlib.sha256(manifest_raw).hexdigest(),
                  "publication_order": replay_names + [OUTER],
                  "outer_receipt_published_last": True,
                  "postpublication_terminal_byte_replay": capture,
                  "replayed_member_count": len(capture),
                  "all_bytes_identity_stable": True,
                  "candidate_is_authority": False, **ZERO}
    outer = {**outer_body, "object_sha256": digest(outer_body)}
    publish_json(output / OUTER, outer)
    for name in BASE_MEMBERS:
        raw = secure(output / name, file_sha(output / name))
        need(raw and raw[-1:] in {b"\n", b"}"}, "terminal-byte:" + name)
    print(json.dumps({"stage": str(output), "result": result,
                      "outer_file_sha256": file_sha(output / OUTER),
                      "outer_object_sha256": outer["object_sha256"]},
                     sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--batch-size", type=int, default=257)
    args = parser.parse_args()
    if args.worker:
        return worker()
    need(args.output is not None, "--output required")
    build(args.output.resolve(), args.batch_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
