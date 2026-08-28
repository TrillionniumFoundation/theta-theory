#!/usr/bin/env python3
"""Append-only zero-credit exact route oracle for the 33,100 C71b children.

The diagnostic C77 probe is deliberately not an input.  This program pins the
accepted C65/C69c/C71/C71b releases and the already independently checked C72b2
route capability, then freshly reconstructs every exact child at 384 bits.
It publishes only a staged candidate; a separate no-producer verifier must
rebuild the mathematics before any downstream consumer may use the bytes.
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
import sys
import zlib
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
SITE = ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages"
SCHEMA = "cm2.round306c77d.decision-child-exact-route-strict-exclusion.v1"
CORE_SCHEMA = "cm2.round306c72x.implicit-h1-root-physical-glue-core.v1"
PREFIX = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1"
ROWS = PREFIX + "_rows.jsonl.gz"
INCIDENCE = PREFIX + "_root_incidence.jsonl.gz"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
CANDIDATE_MANIFEST = PREFIX + "_candidate_manifest.sha256"
LOCK = "ZERO_CREDIT_STAGED_C77D_DECISION_ROUTE_STRICT_EXCLUSION_ONLY.lock"
PRECISION = 384
EXPECTED_SCOPE = 33_100
EXPECTED_INPUT = {
    "LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX": 1,
    "LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX": 7_352,
    "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS": 8_093,
    "LOCAL_H1_CLIPPED_GRAPH_AND_TWO_OFF_GRAPH_REGIONS": 17_654,
}
EXPECTED_GEOMETRY = {"STRICT_NEGATIVE": 1, "STRICT_POSITIVE": 7_352,
                     "CLIPPED": 25_747}
EXPECTED_ROUTE = {"COLLISION1_OUTGOING_CHART_MISMATCH": 1,
                  "COLLISION1_OFFICIAL_WORD_MISMATCH": 31_338,
                  "COLLISION2_STRICT_OWNER_MISMATCH": 1_761}
EXPECTED_DISPOSITION_ROUTE = {
    "LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX|COLLISION1_OUTGOING_CHART_MISMATCH": 1,
    "LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX|COLLISION1_OFFICIAL_WORD_MISMATCH": 6_956,
    "LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX|COLLISION2_STRICT_OWNER_MISMATCH": 396,
    "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS|COLLISION1_OFFICIAL_WORD_MISMATCH": 7_999,
    "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS|COLLISION2_STRICT_OWNER_MISMATCH": 94,
    "LOCAL_H1_CLIPPED_GRAPH_AND_TWO_OFF_GRAPH_REGIONS|COLLISION1_OFFICIAL_WORD_MISMATCH": 16_383,
    "LOCAL_H1_CLIPPED_GRAPH_AND_TWO_OFF_GRAPH_REGIONS|COLLISION2_STRICT_OWNER_MISMATCH": 1_271,
}
ZERO = {"formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0}

C71B_DIR = ROOT / ".cm2-runtime/c71b-v3-final-75c21279"
C71_DIR = ROOT / ".cm2-runtime/c71v2-final-193c3f9f"
C35_DIR = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C37_DIR = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"
C38_DIR = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C35_AUDIT = ROOT / ".cm2-runtime/audit/c35-independent-audit-20260810T145205Z-1583ed4d15344427/independent_audit.json"
C37_AUDIT = ROOT / ".cm2-runtime/audit/c37-independent-audit-20260810T155248Z-49ba0249b7685f58/independent_audit.json"
C38_AUDIT = ROOT / ".cm2-runtime/audit/c38-independent-audit-20260810T180628Z-c149ee1692741ec7/independent_audit.json"
C72B2_DIR = ROOT / ".cm2-runtime/c72b2-build-a.v2-3eb4d9c9"
C72B2_VERIFY = ROOT / ".cm2-runtime/c72b2-independent-a.v2-3212bb3d.json"
C72B2_RECEIPT = ROOT / ".cm2-runtime/c72b2-completion-outer-receipt.v2-a53e5319.json"
PURE_CORE = OUT / "cm2_round306c72x_implicit_h1_root_physical_glue_core_v1.py"
CHART_MANIFEST = OUT / "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"

PIN_FILES = {
    OUT / "cm2_round306c77d_decision_child_exact_route_strict_exclusion_contract_v1.json":
        "0245ceb9b76d7d5a0271f92002b2a6d54fff6451155b1f99ccb8af8a467e6c8a",
    OUT / "cm2_round306c77d_decision_child_exact_route_strict_exclusion_closed_schemas_v1.json":
        "ccfc507e65996a31d568bf7fe22142ce2c05338d34627b480202a7d2b804529c",
    OUT / "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json":
        "1ca46fb81cc104b727b31d3bb0adbb439ab8dae9123b8cbe05d3c60de0e75457",
    OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v9.json":
        "7d4e97bd641da7c5ccc64e8c2ad3d59f21ba3ebd73eb0e4d55c88ad617ee23b4",
    OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json":
        "f0609dc4835346e078b5299007b1b31210d28cbf772ac41bb0f390f7047ad274",
    OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v9.json":
        "c7d99ba4fea05fbd7a3b478f025323c77e5335951e4ff08743ad37ba47fa8e85",
    OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256":
        "96b0f082688f16f821104402bc9aba1b7778df36f084a300d978dac95faf43c5",
    OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json":
        "20a52a4c16c84ffd524833c0ee872edfeb6fdec538a1368f619244199814fb1d",
    OUT / "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json":
        "607fc73ebe3333ca172eb15c0831b8c3d98192c86e20eec7a59a69c4ae4737d4",
    OUT / "cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json":
        "b0490ed50de8d615039d864db1071792df0809b928a663fcd4a89981eaf326b6",
    OUT / "cm2_round306c69c_descriptor_repair_supersession_independent_manifest_v1.sha256":
        "c231941ca4f5f76a95faa81e8390e3f11b5d1af84b645605c52245e6ff214749",
    OUT / "cm2_round306c69c_descriptor_repair_supersession_independent_outer_publication_receipt_v1.json":
        "2baac1cf22ca8be0163f9027d0365e948107b535df917a25334626110bf2916c",
    C71_DIR / "cm2_round306c71_c65v9_c69c_c70_child_h1_successor_v2_intersection_rows.jsonl.gz":
        "d0c84a873682268d4c61514620debd18ac9e9f93411d23c4f99c1e166876c71b",
    C71_DIR / "cm2_round306c71_c65v9_c69c_c70_child_h1_successor_v2_result.json":
        "22d2001a7045a8960b07e2ec4ad4ddf8cb5efd44064e7563d50c4b2c4a8c0bda",
    C71_DIR / "independent_verification_v2.json":
        "db1f60b6ddcd538aaeee0f3dbf8c195af6e877ea3b93dd7789316631d57145f9",
    C71B_DIR / "cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_rows.jsonl.gz":
        "f9f04044809e46b9811d52abef94844d84b058a2f0c3fb6f5b9f97f2302cbec6",
    C71B_DIR / "cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_result.json":
        "5ede807e4860b60fe8582597cc6be10cdfdc7b3a0eeba57ced317f4980092246",
    C71B_DIR / "independent_verification_v3_1.json":
        "ee105922e263d9cea551088ee67c350cc9adc4d9f375a8584428e4fa55575612",
    C71B_DIR / "dual_build_publication_completion_receipt_v3.json":
        "3a6cfa624fab8cd1b787d3facd139cf9e055a008236864d894d2633522fe9fbc",
    C35_DIR / "path_occurrences.jsonl.gz":
        "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66",
    C35_DIR / "result.json":
        "3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
    C35_DIR / "root_manifest.sha256":
        "bdb9bcc7dd9a60aa8fc28dc5e344a656b3c64b4127de8f39e07b4343eb3b2135",
    C35_AUDIT: "d45582baed7dea4246864afd42664df9442c6e6e45afa4562bc36ae0c8050efe",
    C37_DIR / "reflected_r1648_occurrences.jsonl.gz":
        "7c87829f6ef883b7928ff8a313d5bfcf240383c51a9040739de1cfe7e617bef5",
    C37_DIR / "result.json":
        "5b968d957cbca2a4f8aec855a44643f5add7fe0244d933401dfdef9ad7be61f3",
    C37_DIR / "root_manifest.sha256":
        "2ab4d1f12f01cb306007eb832124dda11bc9eb289a19e4e9a5e530b1bee27faf",
    C37_AUDIT: "e707314bc21032af0b344b664825ab683d411f1391c041cb92efc35d6807d7eb",
    C38_DIR / "collision1_2_child_pairs.jsonl.gz":
        "0347849c0368368430f5456b71cd4a4bce4e5912c8a3da33649cfac35b1708a2",
    C38_DIR / "result.json":
        "094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501",
    C38_DIR / "root_manifest.sha256":
        "570da7d92cb331a71275541ee968d295f48cef7605e2b1b80e7b3a885ec6db03",
    C38_AUDIT: "e3fa567b3553415f5357ead66feb00b860c050a6ea687aeb7719666362ffac79",
    C72B2_DIR / "cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_result.json":
        "0c8c56a86d3293dd08bc1fef95a72fe0aedc3a35edb20ff0ec9c6e19cd69d1f3",
    C72B2_VERIFY: "21988ad9b5d746495489e506fadfdf537848eeae6a788a64c6bca3b11c2c9252",
    C72B2_RECEIPT: "e0d6da2518d48278a42ffea5e6a676b11001d531e971fdc59da39f3b524dec62",
    PURE_CORE: "98f13225cbd9caf886242fbedf5071846b77df192727a7bdbc4075eb89a8adc8",
    CHART_MANIFEST: "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
}

CHART_CERTIFICATE_PIN = "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1"
CHART_DEPENDENCIES = {
    "cm2-gate3-endpoint-identity-refinement-manifest-2026-07-15.json":
        "dc394ee38b1e1c36a3cabf27d69279576a8f58f40705537c38c04524781b37d7",
    "cm2-gate3-first-miss-stratification-manifest-2026-07-15.json":
        "58f2460f7bbfb5bab6c0c7cb48c706482359ffb423dc35abcbd2069220db1388",
    "cm2-v52-manifest.sha256":
        "5cef5b8e60f0cfe2291da6bb34b2c57eed6cf2d1a13d164b74b566f752b6b368",
    "cm2_gate3_endpoint_identity_refinement_cert.py":
        "547c48d1b350fb1781719f936634b72c5664b4842e1f33fddb02c33bcbdf7563",
    "cm2_gate3_global_physical_subrow_atlas_cert.py":
        "0445331455e5cc8d17c3393108e997712502cdb606f65ac57de6e0b698b3c1fc",
}
NUMERIC_PINS = {
    "r185": "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    "r178": "06075baac268e8e6c9deeeedae3e502b3a96630f3650c0b783c2b2a77dbd23f9",
    "atlas": "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "ge": "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "registry": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "r139": "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    "lower": "42d749dccea86aa3a122707db0226def176e75047d5dcb4bf19826b50e09282b",
    "round136": "4e78309d5275bf367e6df03509c40ebaaac6f344c7948446a25b3b508c8c2bc2",
    "time3": "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
    "time2": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "core": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "step1": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
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


def file_sha(path: Path) -> str:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link:" + str(path))
        h = hashlib.sha256()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            h.update(block)
        after = os.fstat(fd)
        need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
              before.st_ctime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
              after.st_ctime_ns), "TOCTOU:" + str(path))
        return h.hexdigest()
    finally:
        os.close(fd)


def pinned(path: Path, expected: str | None = None) -> bytes:
    claim = expected if expected is not None else PIN_FILES[path]
    need(file_sha(path) == claim, "pin:" + str(path))
    return path.read_bytes()


def close_row(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":row")


def close_object(value: Mapping[str, Any], expected: str, label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(type(claim) is str and claim == expected == digest(body), label + ":object")


def parse_json(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict, label + ":dict")
    return value


def one_gzip(path: Path, expected: str) -> None:
    need(file_sha(path) == expected, "gzip pin:" + str(path))
    dec = zlib.decompressobj(16 + zlib.MAX_WBITS)
    with path.open("rb") as stream:
        while True:
            block = stream.read(1 << 20)
            if not block:
                break
            dec.decompress(block)
            need(dec.unused_data == b"", "gzip multiple/trailing:" + str(path))
    dec.flush()
    need(dec.eof and not dec.unused_data and not dec.unconsumed_tail,
         "gzip closure:" + str(path))


def iter_rows(path: Path, expected: str) -> Iterator[dict[str, Any]]:
    one_gzip(path, expected)
    with gzip.open(path, "rb") as stream:
        for ordinal, raw in enumerate(stream, 1):
            need(raw.endswith(b"\n"), f"newline:{path}:{ordinal}")
            row = json.loads(raw)
            need(canonical(row) + b"\n" == raw, f"canonical:{path}:{ordinal}")
            close_row(row, f"{path}:{ordinal}")
            yield row


def add_row(value: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in value, "new row unhashed")
    return {**value, "row_sha256": digest(value)}


def add_object(value: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in value, "new object unhashed")
    return {**value, "object_sha256": digest(value)}


def write_exclusive(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), 0o444)
    try:
        view = memoryview(raw)
        while view:
            size = os.write(fd, view)
            need(size > 0, "short write")
            view = view[size:]
        os.fsync(fd)
    finally:
        os.close(fd)


class LedgerWriter:
    def __init__(self, path: Path, order: str):
        self.path, self.order = path, order
        self.raw = open(path, "xb")
        self.stream = gzip.GzipFile(filename="", mode="wb", compresslevel=9,
                                    fileobj=self.raw, mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def write(self, row: dict[str, Any]) -> None:
        closed = add_row(row)
        self.stream.write(canonical(closed) + b"\n")
        self.sequence.update((closed["row_sha256"] + "\n").encode("ascii"))
        self.count += 1

    def close(self) -> None:
        self.stream.close()
        self.raw.flush()
        os.fsync(self.raw.fileno())
        self.raw.close()
        os.chmod(self.path, 0o444)

    def descriptor(self) -> dict[str, Any]:
        return {"filename": self.path.name, "order": self.order,
                "row_count": self.count,
                "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
                "sha256": file_sha(self.path), "size": self.path.stat().st_size}


def exact_faces(pair: int, box: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    t0, t1 = box["t"]
    p0, p1 = box["p"]
    return {
        "T_LOW": {"pair_index": pair, "fixed_axis": "t", "fixed_value": t0,
                  "varying_axis": "p", "varying_interval": [p0, p1]},
        "T_HIGH": {"pair_index": pair, "fixed_axis": "t", "fixed_value": t1,
                   "varying_axis": "p", "varying_interval": [p0, p1]},
        "P_LOW": {"pair_index": pair, "fixed_axis": "p", "fixed_value": p0,
                  "varying_axis": "t", "varying_interval": [t0, t1]},
        "P_HIGH": {"pair_index": pair, "fixed_axis": "p", "fixed_value": p1,
                   "varying_axis": "t", "varying_interval": [t0, t1]},
    }


def face_key(spec: Mapping[str, Any]) -> str:
    return digest({"schema": CORE_SCHEMA + ".exact-face-key", **dict(spec)})


def numeric_modules(r185: Any, r139: Any) -> dict[str, str]:
    modules = {"r185": r185, "r178": r185.r178, "atlas": r185.atlas,
               "ge": r185.ge, "registry": r185.registry, "r139": r139,
               "lower": r139.lower, "round136": r139.lower.round136,
               "time3": r139.lower.time3,
               "time2": r139.lower.time3.time2_cert,
               "core": r139.lower.core_cert, "step1": r139.lower.step1}
    observed = {name: file_sha(Path(module.__file__).resolve())
                for name, module in modules.items()}
    need(observed == NUMERIC_PINS, "numeric source pins")
    return observed


def chart_authority() -> dict[str, Any]:
    manifest = parse_json(pinned(CHART_MANIFEST), "chart manifest")
    need(manifest["certificate_sha256"] == CHART_CERTIFICATE_PIN and
         manifest["dependencies"] == CHART_DEPENDENCIES and
         manifest["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED",
         "chart certificate")
    rule = manifest["result"]["unique_half_open_owner_rule"]
    need(rule["diagonal_tie"] == "E or W owns; N or S excludes" and
         rule["same_physical_normal_on_paired_representations"] is True and
         rule["duplicate_trace_is_identified_not_added"] is True and
         manifest["result"]["scope_limits"]
             ["ownership_rule_applies_to_analytic_strata"] is True,
         "chart analytic ownership")
    for name, expected in CHART_DEPENDENCIES.items():
        pinned(OUT / name, expected)
    return {
        "manifest_file_sha256": PIN_FILES[CHART_MANIFEST],
        "certificate_sha256": CHART_CERTIFICATE_PIN,
        "eight_chart_seam_ownership": "CERTIFIED",
        "diagonal_tie": "E or W owns; N or S excludes",
        "same_physical_normal_on_paired_representations": True,
        "duplicate_trace_is_identified_not_added": True,
    }


def validate_release() -> dict[str, Any]:
    for path, expected in PIN_FILES.items():
        pinned(path, expected)
    contract = parse_json(pinned(
        OUT / "cm2_round306c77d_decision_child_exact_route_strict_exclusion_contract_v1.json"),
        "contract")
    schemas = parse_json(pinned(
        OUT / "cm2_round306c77d_decision_child_exact_route_strict_exclusion_closed_schemas_v1.json"),
        "schemas")
    close_object(contract, "5fffc6b21e30970bb3805b1945a744b4d24ca9056eae40d1bb1363b61d6d66d4", "contract")
    close_object(schemas, "684764629f81a6ad96110f9061f5a2e9e9de740e8725597bfd6b1ca26348638c", "schemas")

    c65 = parse_json(pinned(OUT / "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json"), "C65")
    need(c65["object_sha256"] == "79185dbca48f0d228977a006583eb545525cff2d9418160fb190c1f9c5b6c393" and
         c65["coverage"]["complete_parent_disposition_census"]["COLLISION2_HANDOFF"] == 167_255 and
         c65["formal_credit"] == c65["D02_gate_credit"] == 0, "C65 release")
    c69 = parse_json(pinned(OUT / "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json"), "C69")
    need(c69["object_sha256"] == "e52904a7d8ba73c855e69e390cd3cf29c233ffe492e6fae74efdf0b6d4d0a6a5" and
         c69["scope"]["decision_count"] == 2_356 and
         c69["strict_boundary"]["decisions_are_terminal_dispositions"] is False,
         "C69 release")
    c71 = parse_json(pinned(C71_DIR / "cm2_round306c71_c65v9_c69c_c70_child_h1_successor_v2_result.json"), "C71")
    c71v = parse_json(pinned(C71_DIR / "independent_verification_v2.json"), "C71 verify")
    need(c71["object_sha256"] == "193c3f9f1a41bc0e59240ad410f170bba14f338e257d21c3d4dd071c8e4caa0d" and
         c71v["object_sha256"] == "1734a72579e110abcbdb476ff30baa3af99045bce9b48a0a0f7b06af925ce697" and
         c71["coverage"]["decision_source_child_count"] == EXPECTED_SCOPE,
         "C71 release")
    c71b = parse_json(pinned(C71B_DIR / "cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_result.json"), "C71b")
    c71bv = parse_json(pinned(C71B_DIR / "independent_verification_v3_1.json"), "C71b verify")
    c71br = parse_json(pinned(C71B_DIR / "dual_build_publication_completion_receipt_v3.json"), "C71b receipt")
    need(c71b["object_sha256"] == "75c21279e3440a32116e67c20f12c7ec9d299491d018e2982ab18d68118d4158" and
         c71bv["object_sha256"] == "c45c5b19daeaef930f981810722460424a0d55c8302380829757e2132754f5c3" and
         c71br["object_sha256"] == "d7fd8322b72fad933bb80542913b00cb54c5d7a3d93bf8cb7601aefa5daadbcd" and
         c71b["coverage"]["child_level_H1_full_box_closed_count"] == EXPECTED_SCOPE and
         c71br["supersession"]["rejected_output_may_be_consumed"] is False,
         "C71b accepted corrected release")
    c72 = parse_json(pinned(C72B2_DIR / "cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_result.json"), "C72b2")
    c72v = parse_json(pinned(C72B2_VERIFY), "C72b2 verify")
    c72r = parse_json(pinned(C72B2_RECEIPT), "C72b2 receipt")
    need(c72["object_sha256"] == "a53e531998c8fe4a6ffbcaf11a2b4cfa8741e39c6aa4a979ebb45d10f807e241" and
         c72v["object_sha256"] == "4b09ea6358600fd25ab5bb51dc59e30d7cac200fefb4ad5e446425bc3a7112f5" and
         c72r["object_sha256"] == "9479d8d9aae7bf22e76f9a8bc203bd26093ef87ac42b8450a4e97b3ce40a8e27" and
         c72v["producer_source_imported_read_decoded_compiled_or_executed"] is False,
         "C72b2 route capability")
    for path, expected_object in (
        (C35_DIR / "result.json", "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752"),
        (C35_AUDIT, "914b1440a311a922819e488e4ed4ef39cb87df74b884f2fe7821336f7cb8d33a"),
        (C37_DIR / "result.json", "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b"),
        (C37_AUDIT, "b5be1e8d97337ff90f514695f06bbb1156c606324a50b05766ed080a261d8044"),
        (C38_DIR / "result.json", "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434"),
        (C38_AUDIT, "5e6d0a7a0d1f2216014ac5ef5858ddda6738802a1a02e5749a1f674f766eddf2"),
    ):
        value = parse_json(pinned(path), str(path))
        close_object(value, expected_object, str(path))
    return {"pin_count": len(PIN_FILES) + len(CHART_DEPENDENCIES),
            "C65_v9": True, "C69c": True, "C71_v2": True,
            "C71b_v3": True, "C72b2_route_capability": True,
            "C35_C37_C38_audited": True}


def first_two(path: Path, expected: str) -> list[dict[str, Any]]:
    result = []
    for row in iter_rows(path, expected):
        result.append(row)
        if len(result) == 2:
            return result
    raise Reject("short occurrence ledger")


def selected_rows() -> tuple[list[dict[str, Any]], collections.Counter[str]]:
    path = C71B_DIR / "cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_rows.jsonl.gz"
    expected = PIN_FILES[path]
    selected, census = [], collections.Counter()
    seen = set()
    for row in iter_rows(path, expected):
        need(row["C65_aggregate_leaf_row_sha256"] not in seen, "C71b child duplicate")
        seen.add(row["C65_aggregate_leaf_row_sha256"])
        if row["child_numeric_domain"] is True:
            need(row["child_level_H1_full_box_closed"] is True and
                 row["consumer_review_ready"] is True and
                 row["global_consumption_ready"] is False and
                 row["remaining_blocker_codes"] == [] and
                 all(row[key] == 0 for key in
                     ("formal_credit", "D02_gate_credit",
                      "terminal_disposition_credit", "whole_parent_credit")),
                 "C71b selected semantics")
            census[row["arrangement_disposition"]] += 1
            selected.append(row)
        else:
            need(row["arrangement_disposition"] ==
                 "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE", "C71b blocked scope")
    need(len(seen) == 167_255 and len(selected) == EXPECTED_SCOPE and
         dict(census) == EXPECTED_INPUT, "C71b exact partition")
    return selected, census


def origins_for(pairs: set[int]) -> dict[int, str]:
    path = C38_DIR / "collision1_2_child_pairs.jsonl.gz"
    origins: dict[int, str] = {}
    for row in iter_rows(path, PIN_FILES[path]):
        pair = row["pair_index"]
        if pair in pairs:
            value = row["representative_origin_key"]
            need(pair not in origins or origins[pair] == value, "C38 origin drift")
            origins[pair] = value
    need(set(origins) == pairs, "C38 origin coverage")
    return origins


def build_incidence(root_occurrences: dict[str, dict[str, Any]],
                    needed_faces: set[str]) -> list[dict[str, Any]]:
    path = C71B_DIR / "cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_rows.jsonl.gz"
    atlas: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in iter_rows(path, PIN_FILES[path]):
        for edge_id, spec in exact_faces(row["pair_index"], row["exact_representative_box"]).items():
            key = face_key(spec)
            if key in needed_faces:
                atlas[key].append({"C71b_arrangement_row_sha256": row["row_sha256"],
                                   "C65_aggregate_child_row_sha256": row["C65_aggregate_leaf_row_sha256"],
                                   "child_path": row["child_path"], "edge_id": edge_id,
                                   "exact_face": spec})
    output = []
    for root_id in sorted(root_occurrences):
        item = root_occurrences[root_id]
        targets = item["occurrences"]
        faces = atlas[item["face_key_sha256"]]
        need(len(targets) in (1, 2) and len(faces) in (1, 2), "root/face degree")
        need(all(row["exact_face"] == item["exact_face"] for row in targets + faces),
             "root exact face identity")
        if len(faces) == 2:
            highs = [row for row in faces if row["edge_id"].endswith("HIGH")]
            need(len(highs) == 1, "shared face high owner")
            owner = highs[0]
            face_class = "SHARED_C71B_FACE"
        else:
            owner = faces[0]
            face_class = "C71B_SCOPE_BOUNDARY_FACE"
        output.append(add_row({
            "schema": SCHEMA + ".root-incidence-row",
            "root_id": root_id,
            "face_key_sha256": item["face_key_sha256"],
            "exact_face": item["exact_face"],
            "target_graph_endpoint_occurrences": targets,
            "incidence_count": len(targets),
            "incidence_class": "TARGET_GRAPH_SHARED_FACE" if len(targets) == 2
                               else "TARGET_GRAPH_SINGLE_ENDPOINT_OCCURRENCE",
            "incident_C71b_faces": faces,
            "atlas_face_incidence_count": len(faces),
            "atlas_face_incidence_class": face_class,
            "unique_half_open_dyadic_face_owner": owner,
            "dyadic_face_owner_rule":
                "LOWER_COORDINATE_CHILD_HIGH_FACE_ELSE_SCOPE_BOUNDARY_ONLY_FACE",
            "corner_incidence": False,
            "physical_chart_owner": "W",
            "paired_N_or_S_representation_is_shadow_only": True,
            "same_physical_trace_duplicate_identified_not_added": True,
            "root_is_graph_endpoint_not_physical_terminal": True,
            "full_dimensional_Kraft_weight": "0",
            "incidence_closed": True,
            **ZERO,
        }))
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output = Path(args.output_dir)
    if not output.is_absolute():
        output = ROOT / output
    need(ROOT in output.parents and not output.exists(), "fresh workspace stage")
    output.mkdir(mode=0o755)

    release = validate_release()
    authority = chart_authority()
    selected, input_census = selected_rows()
    pairs = {row["pair_index"] for row in selected}
    origins = origins_for(pairs)
    original = first_two(C35_DIR / "path_occurrences.jsonl.gz",
                         PIN_FILES[C35_DIR / "path_occurrences.jsonl.gz"])
    reflected = first_two(C37_DIR / "reflected_r1648_occurrences.jsonl.gz",
                          PIN_FILES[C37_DIR / "reflected_r1648_occurrences.jsonl.gz"])
    expected_word = original[0]["official_word_key_id"]
    expected_owners = {original[1]["selected_absolute_owner_id"],
                       reflected[1]["selected_absolute_owner_id"]}
    need(expected_word ==
         "gate5-word:266945:f86c66902f1acc76521086a8d15abc55cf7a1d77a13bf03fb64dffbf9eb47ea8" and
         expected_owners == {"G[0,0]", "G[0,1]"}, "expected route target")

    sys.path.insert(0, str(SITE))
    sys.path.insert(0, str(OUT))
    from flint import ctx
    ctx.prec = PRECISION
    import cm2_round185_preconditioned_c1_residual_refinement as r185
    import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
    import cm2_round306c72x_implicit_h1_root_physical_glue_core_v1 as physical_core
    numeric = numeric_modules(r185, r139)
    need(file_sha(Path(physical_core.__file__).resolve()) == PIN_FILES[PURE_CORE],
         "pure core worker pin")
    pair_index, pattern_index, registry = r139.lower.component_cert.key_index_tables()
    cores = tuple(r139.lower.core_cert.physical_cores())

    lock_raw = ("candidate=true\nauthority=false\nformal_credit=0\nD02_gate_credit=0\n"
                "CM2_credit=0\nglobal_installed_credit=0\n").encode("ascii")
    write_exclusive(output / LOCK, lock_raw)
    writer = LedgerWriter(output / ROWS, "C71B_ACCEPTED_ROW_ORDER_FILTER_CHILD_NUMERIC_DOMAIN")
    geometry_census = collections.Counter()
    route_census = collections.Counter()
    disposition_route = collections.Counter()
    pair_route = collections.Counter()
    roots: dict[str, dict[str, Any]] = {}
    needed_faces: set[str] = set()

    for ordinal, atlas in enumerate(selected, 1):
        raw_box = atlas["exact_representative_box"]
        box = r185.atlas.AtlasBox(Q(raw_box["t"][0]), Q(raw_box["t"][1]),
                                  Q(raw_box["p"][0]), Q(raw_box["p"][1]),
                                  Q(0), Q(0), len(atlas["child_path"]),
                                  atlas["child_path"])
        origin = origins[atlas["pair_index"]]
        certificate, root_ids, kind = physical_core.geometry_and_roots(
            r185, origin, box, atlas)
        expected_kind = {
            "LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX": "STRICT_NEGATIVE",
            "LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX": "STRICT_POSITIVE",
            "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS": "CLIPPED",
            "LOCAL_H1_CLIPPED_GRAPH_AND_TWO_OFF_GRAPH_REGIONS": "CLIPPED",
        }[atlas["arrangement_disposition"]]
        need(kind == expected_kind, "C71b/fresh geometry agreement")
        geometry_census[kind] += 1
        nx_sign = certificate["normal_component_signs"]["nx"]
        ny_sign = certificate["normal_component_signs"]["ny"]
        route = None
        if kind == "STRICT_NEGATIVE":
            need(ny_sign != 0, "negative chart selector")
            chart = "N" if ny_sign > 0 else "S"
            outcome = "COLLISION1_OUTGOING_CHART_MISMATCH"
            exits = [{"stratum": "EXACT_CHILD", "exit_class": "STRICT_EXCLUSION",
                      "reason": outcome, "actual_outgoing_chart": chart,
                      "expected_outgoing_chart": "W"}]
            glue_kind = "STRICT_NON_W_CHART_NO_DIAGONAL_SEAM"
        else:
            need(nx_sign < 0, "expected W positive/graph stratum")
            route = physical_core.downstream_W_closed_box(
                r185, r139, origin, box, expected_word, expected_owners,
                pair_index, pattern_index, cores)
            outcome = route["outcome"]
            need(outcome in {"COLLISION1_OFFICIAL_WORD_MISMATCH",
                             "COLLISION2_STRICT_OWNER_MISMATCH"},
                 "strict route mismatch")
            if outcome == "COLLISION2_STRICT_OWNER_MISMATCH":
                need(route["selected_collision2_owner"] not in expected_owners,
                     "no expected owner match")
            if kind == "STRICT_POSITIVE":
                exits = [{"stratum": "EXACT_CHILD", "exit_class": "STRICT_EXCLUSION",
                          "chart": "W", "downstream": route}]
                glue_kind = "STRICT_W_CHART_NO_DIAGONAL_SEAM"
            else:
                need(len(root_ids) == 2 and ny_sign != 0, "graph roots/chart")
                shadow = "N" if ny_sign > 0 else "S"
                glue = physical_core.implicit_graph_state_glue(
                    certificate["normal_component_signs"], root_ids, route, authority)
                exits = [
                    {"stratum": "H1_LT_0", "exit_class": "STRICT_EXCLUSION",
                     "reason": "COLLISION1_OUTGOING_CHART_MISMATCH",
                     "actual_outgoing_chart": shadow,
                     "expected_outgoing_chart": "W"},
                    {"stratum": "H1_GT_0", "exit_class": "STRICT_EXCLUSION",
                     "chart": "W", "downstream": route},
                    {"stratum": "H1_EQ_0", "exit_class": "STRICT_EXCLUSION",
                     "chart": "W", "physical_chart_glue": glue,
                     "graph_is_not_a_terminal": True, "downstream": route},
                ]
                glue_kind = "W_HALF_OPEN_GRAPH_OWNER_WITH_N_OR_S_SHADOW"
                by_id = {row["root_id"]: row for row in certificate["boundary_roots"]}
                for identifier in root_ids:
                    spec = by_id[identifier]
                    current = roots.setdefault(identifier, {
                        "face_key_sha256": spec["face_key_sha256"],
                        "exact_face": spec["exact_face"], "occurrences": []})
                    need(current["face_key_sha256"] == spec["face_key_sha256"] and
                         current["exact_face"] == spec["exact_face"], "root identity")
                    current["occurrences"].append({
                        "C71b_arrangement_row_sha256": atlas["row_sha256"],
                        "C65_aggregate_child_row_sha256":
                            atlas["C65_aggregate_leaf_row_sha256"],
                        "child_path": atlas["child_path"],
                        "edge_id": spec["edge_id"],
                        "exact_face": spec["exact_face"]})
                    needed_faces.add(spec["face_key_sha256"])
        route_census[outcome] += 1
        disposition_route[(atlas["arrangement_disposition"], outcome)] += 1
        pair_route[(atlas["pair_index"], outcome)] += 1
        writer.write({
            "schema": SCHEMA + ".decision-row", "ordinal": ordinal,
            "C71b_arrangement_row_sha256": atlas["row_sha256"],
            "C65_aggregate_child_row_sha256": atlas["C65_aggregate_leaf_row_sha256"],
            "C61_aggregate_leaf_row_sha256":
                atlas["source_C61_aggregate_leaf_row_sha256"],
            "pair_index": atlas["pair_index"], "source_path": atlas["source_path"],
            "child_path": atlas["child_path"], "parent_key": origin,
            "exact_representative_box": raw_box,
            "input_arrangement_disposition": atlas["arrangement_disposition"],
            "fresh_geometry_kind": kind, "H1_geometry": certificate,
            "stratum_exits": exits, "route_outcome": outcome,
            "closed_box_downstream_evidence": route,
            "physical_chart_glue_kind": glue_kind,
            "whole_child_strict_exclusion_closed": True,
            "physical_chart_glue_closed": True,
            "allowed_exit_closed_for_every_stratum": True,
            "explicit_residual_strata": 0,
            "sealed_collision3_handoff_count": 0,
            "collision3_handoff": None,
            "current_disposition":
                "STAGED_ZERO_CREDIT_WHOLE_CHILD_STRICT_EXCLUSION",
            "candidate_is_authority": False,
            "global_consumption_ready": False,
            "additional_dyadic_depth": 0,
            "official_registry_sha256": registry,
            **ZERO,
        })
        if ordinal % 1000 == 0:
            print(json.dumps({"progress": ordinal,
                              "route_census": dict(route_census)}, sort_keys=True),
                  file=sys.stderr, flush=True)
    writer.close()

    need(dict(geometry_census) == EXPECTED_GEOMETRY and
         dict(route_census) == EXPECTED_ROUTE and
         {f"{key[0]}|{key[1]}": value for key, value in disposition_route.items()}
            == EXPECTED_DISPOSITION_ROUTE,
         "frozen exact census")
    incidence_rows = build_incidence(roots, needed_faces)
    incidence_writer = LedgerWriter(output / INCIDENCE, "ROOT_ID_ASCENDING")
    degree = collections.Counter()
    for row in incidence_rows:
        closed = dict(row)
        claim = closed.pop("row_sha256")
        need(claim == digest(closed), "incidence preclosed")
        incidence_writer.write(closed)
        degree[row["incidence_count"]] += 1
    incidence_writer.close()
    need(sum(key * value for key, value in degree.items()) == 2 * 25_747,
         "graph endpoint conservation")

    result = add_object({
        "schema": SCHEMA + ".result",
        "status":
            "PASS_33100_DECISION_CHILD_EXACT_ROUTES__33100_WHOLE_CHILD_STRICT_EXCLUSIONS__NO_C3_HANDOFF_OR_RESIDUAL__ZERO_CREDIT",
        "candidate_is_authority": False,
        "producer_file_sha256": file_sha(SELF),
        "contract_file_sha256": PIN_FILES[
            OUT / "cm2_round306c77d_decision_child_exact_route_strict_exclusion_contract_v1.json"],
        "contract_object_sha256":
            "5fffc6b21e30970bb3805b1945a744b4d24ca9056eae40d1bb1363b61d6d66d4",
        "closed_schemas_file_sha256": PIN_FILES[
            OUT / "cm2_round306c77d_decision_child_exact_route_strict_exclusion_closed_schemas_v1.json"],
        "closed_schemas_object_sha256":
            "684764629f81a6ad96110f9061f5a2e9e9de740e8725597bfd6b1ca26348638c",
        "pure_core_file_sha256": PIN_FILES[PURE_CORE],
        "numeric_source_pins": numeric,
        "chart_seam_quotient_manifest_file_sha256": PIN_FILES[CHART_MANIFEST],
        "chart_seam_certificate_sha256": CHART_CERTIFICATE_PIN,
        "frozen_input_release": release,
        "scope": {"target_child_count": EXPECTED_SCOPE,
                  "pair_count": len(pairs), "additional_dyadic_depth": 0},
        "input_arrangement_disposition_census": dict(sorted(input_census.items())),
        "fresh_geometry_census": dict(sorted(geometry_census.items())),
        "route_census": dict(sorted(route_census.items())),
        "disposition_route_census": {
            f"{key[0]}|{key[1]}": value
            for key, value in sorted(disposition_route.items())},
        "pair_route_census": {
            f"{key[0]}|{key[1]}": value for key, value in sorted(pair_route.items())},
        "expected_official_word_key_id": expected_word,
        "expected_collision2_owner_set": sorted(expected_owners),
        "expected_owner_match_count": 0,
        "whole_child_strict_exclusion_count": EXPECTED_SCOPE,
        "sealed_collision3_handoff_count": 0,
        "explicit_residual_child_count": 0,
        "graph_child_count": 25_747,
        "graph_endpoint_occurrence_count": 2 * 25_747,
        "unique_graph_boundary_root_count": len(incidence_rows),
        "target_graph_root_degree_census":
            {str(key): value for key, value in sorted(degree.items())},
        "all_graph_endpoints_have_classified_half_open_face_owner": True,
        "duplicate_physical_graph_traces_added": 0,
        "ledgers": {"decision_rows": writer.descriptor(),
                    "root_incidence": incidence_writer.descriptor()},
        "runtime_canonical_pointer_or_seal_writes": False,
        "global_consumption_ready": False,
        **ZERO,
    })
    result_raw = canonical(result) + b"\n"
    write_exclusive(output / RESULT, result_raw)
    report_raw = (
        "# C77d decision-child exact route strict-exclusion v1\n\n"
        "All 33,100 accepted C71b numeric children were freshly reconstructed at 384 bits. "
        "The exact route census is 1 collision-1 outgoing-chart mismatch, 31,338 collision-1 "
        "official-word mismatches, and 1,761 collision-2 strict-owner mismatches. Every child "
        "is a staged whole-child strict exclusion; collision-3 handoff and residual counts are zero.\n\n"
        "This stage is not authority and carries no formal, D02, CM2, whole-parent, or global-installed credit.\n"
    ).encode("utf-8")
    write_exclusive(output / REPORT, report_raw)
    members = [LOCK, ROWS, INCIDENCE, RESULT, REPORT]
    manifest_raw = b"".join(
        f"{file_sha(output / name)}  {name}\n".encode("ascii") for name in members)
    write_exclusive(output / CANDIDATE_MANIFEST, manifest_raw)
    for name in members + [CANDIDATE_MANIFEST]:
        before = file_sha(output / name)
        need(before == file_sha(output / name), "terminal byte replay:" + name)
    print(canonical({"status": result["status"],
                     "result_object_sha256": result["object_sha256"],
                     "output_dir": str(output),
                     "candidate_manifest_sha256": file_sha(output / CANDIDATE_MANIFEST),
                     "terminal_replay_member_count": 6}).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
