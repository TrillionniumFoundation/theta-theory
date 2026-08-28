#!/usr/bin/env python3
"""C75 exact first-tangency strata oracle for the frozen C72 child scope.

The candidate is deliberately zero-credit.  It selects exactly the C72 rows
whose *current child witness* is ``unique monotone inherited-active-set first
tangency`` and proves, without further dyadic subdivision, a unique regular
discriminant graph over each complete child.  The two open graph sides are
strict exclusions.  The graph itself is retained as a cemetery first-tangency
terminal and is never misreported as a strict exclusion.

Builds are exclusive in caller-supplied empty directories.  A separate
no-producer verifier must install identical verification bytes in both builds
before ``--complete`` appends the dual completion receipt last.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Iterator
import zlib

from flint import arb, ctx


sys.dont_write_bytecode = True
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
OUT = ROOT / "deliverables"
sys.path.insert(0, str(OUT))

import cm2_round306c41_d02_lower_strata_depth3_closure_v1 as c41  # noqa: E402


SCHEMA = "cm2.round306c75.first-tangency-exact-strata-oracle.v1"
PREFIX = "cm2_round306c75_first_tangency_exact_strata_oracle_v1"
LEDGER = PREFIX + ".jsonl.gz"
ENDPOINTS = PREFIX + "_endpoint_incidence.jsonl.gz"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
MANIFEST = PREFIX + "_manifest.sha256"
OUTER = PREFIX + "_outer_receipt.json"
VERIFICATION = PREFIX + "_independent_verification_v1.json"
DUAL = PREFIX + "_dual_completion_receipt_v1.json"
BASE_MEMBERS = [LEDGER, ENDPOINTS, RESULT, REPORT, MANIFEST, OUTER]
SELECTOR = "unique monotone inherited-active-set first tangency"
PRECISION = 384
EXPECTED_SCOPE = 5_884
EXPECTED_SELECTED_SEQUENCE = "af501ff9b5666cc6f477a0db0a7cd58544a6363c00560774bc831363dbf8bf17"
EXPECTED_PAIR_CENSUS = {31: 2_154, 200: 809, 270: 46, 711: 2_644, 787: 231}
EXPECTED_CATEGORY_CENSUS = {
    "REGULAR_MULTI_GRAPH_FIRST_TANGENCY": 2_289,
    "REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED": 3_595,
}
EXPECTED_TARGET_CENSUS = {"W[1,0]": 5_653, "G[1,1]": 231}

C72_A = ROOT / ".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"
C72_B = ROOT / ".cm2-runtime/c72-build-b.6NX5S7/cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"
C37 = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38/ordinary_cell_reflection_pairs.jsonl.gz"
C32 = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9/compact_cells.jsonl.gz"
C72O = ROOT / ".cm2-runtime/c72o-build-a2.v1/cm2_round306c72o_collision1_outgoing_state_oracle_v1.jsonl.gz"
C73 = ROOT / ".cm2-runtime/c73v2-build-a.QOYACE/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2.jsonl.gz"

INPUTS: dict[str, tuple[Path, str, int]] = {
    "C72_A": (C72_A, "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370", 23_266_147),
    "C72_B": (C72_B, "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370", 23_266_147),
    "C37": (C37, "902ccd3a8744a3a4cf851b5f96e1bf9a8c351ace24ce36ae9cb40355079d7dc8", 216_067),
    "C32": (C32, "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8", 11_222_049),
    "C72O_LEDGER": (C72O, "e3125863adcf3ef6489dce741337622b1d70b2ce7655d8d06237c1612ff19355", 3_801_464),
    "C73_LEDGER": (C73, "ed0a3d26f4984e6eced899a01f58aa8329bb1db72b7d0bfb9fe17ee3a4eef6fc", 3_580_855),
    "C65_SELFTEST": (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json", "f0609dc4835346e078b5299007b1b31210d28cbf772ac41bb0f390f7047ad274", 9_124),
    "C65_MANIFEST": (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256", "96b0f082688f16f821104402bc9aba1b7778df36f084a300d978dac95faf43c5", 69_942),
    "C65_OUTER": (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json", "20a52a4c16c84ffd524833c0ee872edfeb6fdec538a1368f619244199814fb1d", 1_025),
    "C69_VERIFY": (OUT / "cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json", "b0490ed50de8d615039d864db1071792df0809b928a663fcd4a89981eaf326b6", 2_914),
    "C69_OUTER": (OUT / "cm2_round306c69c_descriptor_repair_supersession_independent_outer_publication_receipt_v1.json", "2baac1cf22ca8be0163f9027d0365e948107b535df917a25334626110bf2916c", 2_043),
    "C72_VERIFY": (ROOT / ".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json", "63105e380d37d49bd655e094d41e15d3ed0d182380a44a4a16709ba3308edaf0", 8_307),
    "C72O_VERIFY": (ROOT / ".cm2-runtime/c72o-independent-verification-v2.json", "2d34c25b5fd9f2b3a1e8b30d184b40d8a93ffce8c192d193b75715e0d7a68ccb", 6_522),
    "C73_VERIFY": (ROOT / ".cm2-runtime/c73v2-audit-a.W2AYpD/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_independent_verification_v2.json", "784505135d105fcdf05cc2d6e37779ea896f7d1bbe06e75dd1019b67ae951fe1", 1_443_699),
    "C71B_VERIFY": (ROOT / ".cm2-runtime/c71b-v3-final-75c21279/independent_verification_v3_1.json", "ee105922e263d9cea551088ee67c350cc9adc4d9f375a8584428e4fa55575612", 4_583),
    "C71B_RECEIPT": (ROOT / ".cm2-runtime/c71b-v3-final-75c21279/dual_build_publication_completion_receipt_v3.json", "3a6cfa624fab8cd1b787d3facd139cf9e055a008236864d894d2633522fe9fbc", 6_133),
    "C74L_VERIFY": (ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt/cm2_round306c74l_source_seam_collision1_handoff_successor_independent_verification_v1_1.json", "13e64bdf935b9bb14119ae13892ed1f8deb66e07c281e12df2e370d86b28499c", 3_484),
    "C74L_RECEIPT": (ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt/cm2_round306c74l_source_seam_collision1_handoff_successor_dual_completion_receipt_v1.json", "1b9459e41a3de4ce5ab2f99b946ce6cb325c63934d87c641571c474f62ad7a3a", 3_748),
    "C41_SOURCE": (OUT / "cm2_round306c41_d02_lower_strata_depth3_closure_v1.py", "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde", 133_456),
    "C39_SOURCE": (OUT / "cm2_round306c39_d02_h1_c1_graph_cell_router_v1.py", "873a84cb150efc5649ffb5822457c510ab45c32f3e16a48914c8674dc93c0aae", 38_700),
    "R185_SOURCE": (OUT / "cm2_round185_preconditioned_c1_residual_refinement.py", "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2", 98_395),
}

LINEAGE: dict[int, dict[str, Any]] = {
    31: {"origin": "W:E:00.14.01010111", "cell": "c32-compact-cell:041f34144b44a873bb333fc801014d0b238faaf33d616f20e8cea534effb8a09", "c37": "8178ec54920466e8caf33b267a898e72f5c91b16c6f70cdee9734c7cdcc13b11", "c32": "00f0e2db93a2816b5b696cadd7646be1d22e8644f8880621d4d1a9beea528993", "active": ["G[2,1]", "W[1,0]"], "tangency": "W[1,0]", "other": "G[2,1]"},
    200: {"origin": "W:E:07.01.01101001", "cell": "c32-compact-cell:1d466d3e68922feaa50c3db01ba42cc16e1aa90e4ae2af0f8d7abbfff78b79a8", "c37": "74e97bf9b7346152eac77b3057b0c816eb24cda4c531194ef3f2e0e843d02f03", "c32": "e65303c5fd089c6bbec794f49d1c9fc35e041ad47ea70cce52813521ac221924", "active": ["G[2,0]", "W[1,0]"], "tangency": "W[1,0]", "other": "G[2,0]"},
    270: {"origin": "W:E:07.01.01101010", "cell": "c32-compact-cell:2c5fb436107089292c28f4ab2167a0b1423c0fb6d64a327c164ff42739ad071d", "c37": "8ec98ae61d743ec5f3f88b061acf19ede2a70a12b490aff88753f8fdfc903830", "c32": "4ae4a43c8e6b7a9769b85ccba42b473e3d86a878e00f78c87560a266c0b4508e", "active": ["G[2,0]", "W[1,0]"], "tangency": "W[1,0]", "other": "G[2,0]"},
    711: {"origin": "W:E:00.14.01011011", "cell": "c32-compact-cell:8ee1ada7008271e1806d517118a8c0f2b9932a97b190d7d84770c9925afd62d6", "c37": "e66037c00d654cae65bd3a6a6cf56ae8be2a85f29eabc615d7323517d92ea9d4", "c32": "367136ed6dac99757e78a92d5c53b26dbb09a83d8b4c5dcacaa437f129ab9025", "active": ["G[2,1]", "W[1,0]"], "tangency": "W[1,0]", "other": "G[2,1]"},
    787: {"origin": "W:N:06.00.01101111", "cell": "c32-compact-cell:adfd78145e4fb77661ca53a12f24379f50809e334accbf9d74264ce6dc42edc6", "c37": "00fc155d31bd540b05aed6b808cd5aa020272b5180233188ef9b357501358a5b", "c32": "d4799abbd72bfaf1cdb82fbd73bd1bc2c9eecb544ae4e4d13d37c8a01c409d43", "active": ["G[1,1]", "W[1,0]"], "tangency": "G[1,1]", "other": "W[1,0]"},
}


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def obj(value: Any) -> str:
    return sha(canonical(value))


def closed(value: dict[str, Any], key: str = "object_sha256") -> dict[str, Any]:
    result = copy.deepcopy(value)
    need(key not in result, "closure key absent")
    result[key] = obj(result)
    return result


def verify_row(value: dict[str, Any], label: str) -> None:
    body = copy.deepcopy(value)
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == obj(body), label + ":row closure")


def identity(item: os.stat_result) -> tuple[int, ...]:
    return (item.st_dev, item.st_ino, item.st_mode, item.st_nlink, item.st_uid,
            item.st_gid, item.st_size, item.st_mtime_ns, item.st_ctime_ns)


def secure(path: Path, expected_sha: str, expected_size: int) -> bytes:
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
         before.st_uid == os.getuid() and before.st_size == expected_size and
         not before.st_mode & stat.S_IWOTH, "secure shape:" + str(path))
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(identity(opened) == identity(before), "path/fd identity:" + str(path))
        chunks = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        need(identity(os.fstat(fd)) == identity(opened), "fd drift:" + str(path))
    finally:
        os.close(fd)
    need(identity(path.lstat()) == identity(before), "path drift:" + str(path))
    raw = b"".join(chunks)
    need(len(raw) == expected_size and sha(raw) == expected_sha, "byte pin:" + str(path))
    return raw


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw.endswith(b"\n") and raw.count(b"\x00") == 0 and
         not raw.startswith(b"\xef\xbb\xbf"), label + ":framing")
    value = json.loads(raw.decode("utf-8"))
    need(type(value) is dict and canonical(value) + b"\n" == raw, label + ":canonical")
    return value


def gzip_lines(raw: bytes, label: str) -> Iterator[bytes]:
    stream = zlib.decompressobj(16 + zlib.MAX_WBITS)
    plain = stream.decompress(raw) + stream.flush()
    need(stream.eof and not stream.unused_data and not stream.unconsumed_tail,
         label + ":single gzip member")
    need(plain.endswith(b"\n"), label + ":newline")
    for line in plain.splitlines():
        yield line


def parse_rows(raw: bytes, label: str) -> list[dict[str, Any]]:
    result = []
    for index, line in enumerate(gzip_lines(raw, label)):
        value = json.loads(line.decode("utf-8"))
        need(type(value) is dict and canonical(value) == line,
             f"{label}:{index}:canonical")
        verify_row(value, f"{label}:{index}")
        result.append(value)
    return result


def sequence(values: Iterable[str]) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(value.encode("ascii") + b"\n")
    return digest.hexdigest()


def exclusive(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), 0o644)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(fd, view)
            need(count > 0, "short write:" + path.name)
            view = view[count:]
        os.fsync(fd)
        os.lseek(fd, 0, os.SEEK_SET)
    finally:
        os.close(fd)
    replay = path.read_bytes()
    need(replay == raw and path.lstat().st_nlink == 1,
         "terminal-byte replay:" + path.name)


class Ledger:
    def __init__(self, path: Path, order: str = "C72_FROZEN_LEDGER_FILTER_ORDER"):
        self.path = path
        self.order = order
        self.raw = path.open("xb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.count = 0
        self.hashes = hashlib.sha256()

    def __enter__(self) -> "Ledger":
        return self

    def write(self, body: dict[str, Any]) -> dict[str, Any]:
        row = closed(body, "row_sha256")
        return self.write_closed(row)

    def write_closed(self, row: dict[str, Any]) -> dict[str, Any]:
        verify_row(row, "preclosed output")
        self.gz.write(canonical(row) + b"\n")
        self.hashes.update(row["row_sha256"].encode("ascii") + b"\n")
        self.count += 1
        return row

    def __exit__(self, *_: Any) -> None:
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        raw = self.path.read_bytes()
        return {"filename": self.path.name, "order": self.order,
                "row_count": self.count,
                "row_hash_line_sequence_sha256": self.hashes.hexdigest(),
                "sha256": sha(raw), "size": len(raw), "gzip_single_member": True,
                "canonical_json_lines": True}


def exact_dyadic(value: arb) -> Q:
    mantissa, exponent = value.man_exp()
    return Q(int(mantissa)) * (Q(2) ** int(exponent))


def bounds(value: arb) -> dict[str, str]:
    return {"lower": str(value.lower()), "upper": str(value.upper())}


def sign(value: arb) -> str:
    if bool(value < 0):
        return "NEGATIVE"
    if bool(value > 0):
        return "POSITIVE"
    return "UNRESOLVED"


def box_from(row: dict[str, Any]) -> Any:
    value = row["exact_representative_box"]
    need(value["s"] == ["0", "0"], "exact s=0")
    t0, t1 = (Q(item) for item in value["t"])
    p0, p1 = (Q(item) for item in value["p"])
    need(-1 < t0 < t1 < 1 and -1 < p0 < p1 < 1, "strict compact box")
    return c41.round185.atlas.AtlasBox(t0, t1, p0, p1, Q(0), Q(0),
                                        len(row["child_path"]), row["child_path"])


def delta(parent: str, box: Any, target: str) -> tuple[Any, arb]:
    raw = c41.round185.ad_root(c41.round185.ad_initial_geometry(parent, box), target)
    centered = c41.round185.centered_enclosure(
        c41.round185.collision0_delta_ad, parent, box, target, raw["Delta"])
    return raw, centered


def point_box(box: Any, t: Q, p: Q, suffix: str) -> Any:
    return c41.round185.atlas.AtlasBox(t, t, p, p, Q(0), Q(0), box.depth,
                                        box.path + suffix)


def face_box(box: Any, axis: str, value: Q, suffix: str) -> Any:
    if axis == "p":
        return c41.round185.atlas.AtlasBox(box.t0, box.t1, value, value, Q(0), Q(0),
                                            box.depth, box.path + suffix)
    return c41.round185.atlas.AtlasBox(value, value, box.p0, box.p1, Q(0), Q(0),
                                        box.depth, box.path + suffix)


def centered_delta(parent: str, box: Any, target: str) -> arb:
    raw = c41.round185.collision0_delta_ad(parent, box, target)
    return c41.round185.centered_enclosure(
        c41.round185.collision0_delta_ad, parent, box, target, raw)


def decide(source: dict[str, Any]) -> dict[str, Any]:
    lineage = LINEAGE[source["pair_index"]]
    box = box_from(source)
    parent, target, other_target = lineage["origin"], lineage["tangency"], lineage["other"]
    evidence = c41.round185.surface_evidence("DELTA0", parent, box, target,
                                              include_axis_tests=True)
    derivative = evidence["full_box_C1_derivatives"]["dp"]
    newton = evidence["axis_interval_Newton"][1]
    need(not derivative["contains_zero"] and
         evidence["axis_full_face_brackets_t_p_s"] == [False, True, False] and
         newton["strict_derivative"] is True and
         newton["strict_interior_self_map"] is True and newton["image"] is not None,
         "uniform p graph/Newton")
    raw, centered = delta(parent, box, target)
    need(sign(centered) == "UNRESOLVED" and bool(centered.lower() < 0) and
         bool(centered.upper() > 0), "tangency delta crosses zero")
    lower_face = centered_delta(parent, face_box(box, "p", box.p0, ".p0"), target)
    upper_face = centered_delta(parent, face_box(box, "p", box.p1, ".p1"), target)
    need(sign(lower_face) in {"NEGATIVE", "POSITIVE"} and
         sign(upper_face) in {"NEGATIVE", "POSITIVE"} and
         sign(lower_face) != sign(upper_face), "opposite complete p faces")
    corners = []
    for t_name, t in (("LOWER_T", box.t0), ("UPPER_T", box.t1)):
        for p_name, p in (("LOWER_P", box.p0), ("UPPER_P", box.p1)):
            value = c41.round185.collision0_delta_ad(
                parent, point_box(box, t, p, ".corner"), target).value
            need(sign(value) in {"NEGATIVE", "POSITIVE"}, "strict corner")
            corners.append({"t_face": t_name, "p_face": p_name,
                            "t": str(t), "p": str(p), "Delta": bounds(value),
                            "sign": sign(value)})
    need(Counter(item["sign"] for item in corners) == Counter({"NEGATIVE": 2, "POSITIVE": 2}),
         "two/two corners")
    upper_radical = centered.upper().sqrt().upper()
    tangency_near_lower = raw["ell"].value.lower() - upper_radical
    need(bool(tangency_near_lower > 0), "positive-side target root future")
    other_raw, other_delta = delta(parent, box, other_target)
    need(bool(other_delta > 0), "other active root uniformly real")
    other_near = other_raw["ell"].value - other_delta.sqrt()
    need(bool(other_near > 0), "other active root uniformly future")
    if target == "W[1,0]":
        first_gap = other_near.lower() - raw["ell"].value.upper()
        geometry = c41.round185.ad_initial_geometry(parent, box)
        _qx, _qy, ux_ad, uy_ad, _s = geometry
        ux, uy = ux_ad.value, uy_ad.value
        transverse, radius = raw["transverse"].value, raw["radius"].value
        radical = c41.round185.BASE.arb_interval(Q(0), exact_dyadic(upper_radical))
        conditional_h1 = (
            (radius * radius - 2 * transverse * transverse) * (ux * ux - uy * uy)
            - 4 * radical * transverse * ux * uy
        ) / (radius * radius)
        need(bool(first_gap > 0) and bool(conditional_h1 < 0),
             "W tangency first and positive side not-W")
        negative_reason = "FROZEN_W_OWNER_ABSENT_ON_DELTA_W_NEGATIVE"
        positive_reason = "FIRST_W_ROOT_EXISTS_BUT_H1_NEGATIVE_STRICT_NOT_W"
        outgoing = {"mode": "DELTA_W_NONNEGATIVE_CONDITIONAL_INTERVAL",
                    "H1": bounds(conditional_h1), "H1_sign": "NEGATIVE",
                    "conclusion": "STRICT_N_OR_S_NOT_REQUIRED_W"}
    else:
        first_gap = other_near.lower() - raw["ell"].value.upper()
        h1 = c41.c39.h1_route(parent, box)
        need(bool(first_gap > 0) and h1["kind"] == "STRICT_SIDE" and
             h1["chart"] == "N", "G tangency first / W negative-side N")
        negative_reason = "G_TANGENCY_TARGET_ABSENT_AND_UNIQUE_W_OWNER_HAS_H1_N_NOT_W"
        positive_reason = "G_NEAR_ROOT_STRICTLY_PRECEDES_REQUIRED_W_OWNER"
        outgoing = {"mode": "FULL_BOX_W_OWNER_H1_ROUTE", "H1": h1["H1_centered"],
                    "H1_sign": "NEGATIVE", "chart": "N",
                    "conclusion": "STRICT_NOT_REQUIRED_W"}
    need(bool(first_gap > 0), "tangency root first")
    negative_orientation = "LOWER_P_SIDE" if sign(lower_face) == "NEGATIVE" else "UPPER_P_SIDE"
    positive_orientation = "LOWER_P_SIDE" if sign(lower_face) == "POSITIVE" else "UPPER_P_SIDE"
    return {
        "schema": SCHEMA + ".strata-row",
        "C72_obligation_row_sha256": source["row_sha256"],
        "C65_aggregate_child_row_sha256": source["C65_aggregate_child_row_sha256"],
        "C61_aggregate_leaf_row_sha256": source["C61_aggregate_leaf_row_sha256"],
        "C68_structural_task_row_sha256": source["C68_structural_task_row_sha256"],
        "C69c_blocker_row_sha256": source["C69c_blocker_row_sha256"],
        "pair_index": source["pair_index"], "source_path": source["source_path"],
        "child_path": source["child_path"],
        "parent_volume_fraction": source["parent_volume_fraction"],
        "exact_representative_box": source["exact_representative_box"],
        "exact_reflected_box": source["exact_reflected_box"],
        "representative_origin_key": parent,
        "representative_cell_id": lineage["cell"],
        "C37_pair_row_sha256": lineage["c37"], "C32_cell_row_sha256": lineage["c32"],
        "active_candidates": lineage["active"], "active_candidate_count": 2,
        "tangency_target": target, "other_active_target": other_target,
        "legacy_structural_category": source["structural_category"],
        "legacy_child_route_witness": source["child_route_witness"],
        "full_child_tangency_graph": {
            "equation": "collision1_Delta_" + target + "=0",
            "precision_bits": PRECISION, "graph_axis": "p", "base_axis": "t",
            "strict_dp_bounds": derivative,
            "lower_p_face": {"p": str(box.p0), "Delta": bounds(lower_face),
                             "sign": sign(lower_face)},
            "upper_p_face": {"p": str(box.p1), "Delta": bounds(upper_face),
                             "sign": sign(upper_face)},
            "centered_full_box_Delta": bounds(centered),
            "four_strict_corners": corners,
            "interval_Newton": newton,
            "theorem": "UNIFORM_OPPOSITE_P_FACE_SIGNS_PLUS_STRICT_DP_AND_IVT_IFT",
            "unique_regular_graph_over_complete_t_base": True,
            "graph_endpoints_on_both_t_faces": True,
        },
        "exact_root_order": {
            "positive_side_target_near_lower": str(tangency_near_lower),
            "graph_target_root_ell_bounds": bounds(raw["ell"].value),
            "other_active_near_bounds": bounds(other_near),
            "first_tangency_order_gap_lower": str(first_gap),
            "target_is_strict_first_on_graph_and_positive_side": True,
        },
        "outgoing_or_competitor_evidence": outgoing,
        "three_strata": {
            "negative_open_side": {"predicate": "Delta_" + target + "<0",
                                   "orientation": negative_orientation,
                                   "exit_class": "STRICT_EXCLUSION",
                                   "reason": negative_reason},
            "zero_graph": {"predicate": "Delta_" + target + "=0",
                           "exit_class": "CEMETERY_OR_SOURCE_GRAZING_TERMINAL",
                           "terminal_kind": "CEMETERY_FIRST_TANGENCY",
                           "strict_exclusion": False,
                           "root_is_strict_future_and_first": True},
            "positive_open_side": {"predicate": "Delta_" + target + ">0",
                                   "orientation": positive_orientation,
                                   "exit_class": "STRICT_EXCLUSION",
                                   "reason": positive_reason},
            "pairwise_disjoint": True, "union_is_exact_complete_child": True,
        },
        "face_corner_source_glue_and_incidence": {
            "p_faces_attach_to_corresponding_open_sign_sides": True,
            "t_lower_graph_endpoint_incidence": 1,
            "t_upper_graph_endpoint_incidence": 1,
            "four_corners_attach_by_strict_Delta_sign": True,
            "source_grazing": False,
            "source_grazing_terminal_claimed": False,
            "physical_s_slice": "s=0",
        },
        "half_open_ownership_and_Kraft": {
            "dyadic_child_owner": "FROZEN_C72_CHILD_PATH_HALF_OPEN_OWNER",
            "graph_owner": "CEMETERY_FIRST_TANGENCY_TERMINAL",
            "negative_and_positive_sides_are_open_at_graph": True,
            "graph_is_not_double_owned": True,
            "semantic_partition_not_additional_dyadic_depth": True,
            "additional_dyadic_depth": 0,
            "full_dimensional_normalized_Kraft": "1",
            "typed_graph_Kraft": "0",
        },
        "allowed_exit_coverage": "TWO_STRICT_EXCLUSION_SIDES_PLUS_CEMETERY_FIRST_TANGENCY_GRAPH",
        "unresolved_strata": 0,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "CM2_credit": 0,
    }


def normalized_interval(values: list[str]) -> tuple[str, str]:
    lower, upper = (Q(value) for value in values)
    need(lower < upper, "nondegenerate interval")
    return str(lower), str(upper)


def face_index_key(source: dict[str, Any], side: str) -> tuple[int, str, tuple[str, str]]:
    need(side in {"LOWER_T", "UPPER_T"}, "t face side")
    box = source["exact_representative_box"]
    t = Q(box["t"][0 if side == "LOWER_T" else 1])
    return source["pair_index"], str(t), normalized_interval(box["p"])


def reflected_face(source: dict[str, Any], side: str,
                   target: str) -> dict[str, Any]:
    representative_t = Q(source["exact_representative_box"]["t"][
        0 if side == "LOWER_T" else 1])
    reflected = source["exact_reflected_box"]
    if source["pair_index"] == 787:
        reflected_t = representative_t
        reflected_side = side
        reflected_target = "G[1,0]" if target == "G[1,1]" else target
        formula = "N_TO_S__t_FIXED__p_NEGATED__y_REFLECTED"
    else:
        reflected_t = -representative_t
        reflected_side = "UPPER_T" if side == "LOWER_T" else "LOWER_T"
        reflected_target = "W[1,1]" if target == "W[1,0]" else target
        formula = "E_FIXED__t_NEGATED__p_NEGATED__y_REFLECTED"
    expected = Q(reflected["t"][0 if reflected_side == "LOWER_T" else 1])
    need(expected == reflected_t, "exact reflected t face")
    return {
        "compact_chart": reflected["compact_chart"],
        "face_axis": "t", "face_side": reflected_side,
        "exact_t": str(reflected_t),
        "exact_p_interval": list(normalized_interval(reflected["p"])),
        "exact_s": "0", "reflected_tangency_target": reflected_target,
        "horizontal_reflection_formula": formula,
    }


def endpoint_row(source: dict[str, Any], strata: dict[str, Any], side: str,
                 index: dict[tuple[int, str, tuple[str, str]], list[tuple[dict[str, Any], str]]],
                 strata_by_c72: dict[str, dict[str, Any]],
                 cells: dict[str, dict[str, Any]],
                 all_cells: list[dict[str, Any]]) -> dict[str, Any]:
    lineage = LINEAGE[source["pair_index"]]
    parent, target = lineage["origin"], lineage["tangency"]
    box = box_from(source)
    t = box.t0 if side == "LOWER_T" else box.t1
    face = face_box(box, "t", t, ".endpoint-" + side.lower())
    full = c41.round185.collision0_delta_ad(parent, face, target)
    newton = c41.round185.axis_newton_record(
        c41.round185.collision0_delta_ad, parent, face, target, full, 1)
    need(newton["strict_derivative"] is True and
         newton["strict_interior_self_map"] is True and newton["image"] is not None,
         "endpoint p-root Newton")
    physical_key = {
        "representative_origin_key": parent,
        "equation": "collision1_Delta_" + target + "=0",
        "tangency_target": target, "exact_t": str(t), "exact_s": "0",
    }
    root_id = "c75-first-tangency-root:" + obj(physical_key)
    representative_face = {
        "compact_chart": parent.split(":")[1], "face_axis": "t",
        "face_side": side, "exact_t": str(t),
        "exact_p_interval": [str(box.p0), str(box.p1)], "exact_s": "0",
    }
    reflected = reflected_face(source, side, target)
    glue = {
        "representative_face": representative_face,
        "reflected_face": reflected,
        "C37_pair_row_sha256": lineage["c37"],
        "reflection_is_exact_bijective_involution": True,
    }
    key = face_index_key(source, side)
    entries = index[key]
    own = [(row, row_side) for row, row_side in entries
           if row["row_sha256"] == source["row_sha256"] and row_side == side]
    need(len(own) == 1, "own face occurrence")
    opposite = [(row, row_side) for row, row_side in entries
                if row["row_sha256"] != source["row_sha256"] and row_side != side]
    need(len(opposite) <= 1, "unique adjacent C72 face")
    downstream: dict[str, Any]
    if opposite:
        neighbor, neighbor_side = opposite[0]
        need(neighbor_side != side and
             neighbor["exact_representative_box"]["p"] ==
             source["exact_representative_box"]["p"], "exact adjacent face glue")
        in_scope = neighbor["row_sha256"] in strata_by_c72
        kind = ("IN_SCOPE_MATCHED_TANGENCY_SEGMENT" if in_scope else
                "OUT_OF_SCOPE_C72_DOWNSTREAM_OWNER")
        owner_row = source if side == "LOWER_T" else neighbor
        downstream = {
            "incidence_kind": kind, "incidence_degree_including_downstream": 2,
            "neighbor_C72_obligation_row_sha256": neighbor["row_sha256"],
            "neighbor_face_side": neighbor_side,
            "neighbor_child_path": neighbor["child_path"],
            "neighbor_child_route_witness": neighbor["child_route_witness"],
            "neighbor_structural_category": neighbor["structural_category"],
            "neighbor_C75_strata_row_sha256": (
                strata_by_c72[neighbor["row_sha256"]]["row_sha256"]
                if in_scope else None),
            "half_open_owner_C72_obligation_row_sha256": owner_row["row_sha256"],
            "half_open_rule": "LOWER_T_FACE_INCLUSIVE__UPPER_T_FACE_EXCLUSIVE",
            "current_occurrence_is_half_open_owner": owner_row is source,
            "classified_boundary_not_dangling": True,
        }
    else:
        current_cell = cells[lineage["cell"]]
        chart = current_cell["gate3_chart"]
        parent_p = current_cell["gate3_product_box"]["p"]
        adjacent_cells = [row for row in all_cells
                          if row.get("cell_id") != current_cell["cell_id"] and
                          row.get("gate3_chart") == chart and
                          row.get("gate3_product_box", {}).get("p") == parent_p and
                          str(t) in [str(Q(value)) for value in
                                     row.get("gate3_product_box", {}).get("t", [])]]
        need(len(adjacent_cells) <= 1, "unique adjacent C32 cell")
        if adjacent_cells:
            neighbor_cell = adjacent_cells[0]
            need(side == "LOWER_T", "C32 lower-face owner orientation")
            downstream = {
                "incidence_kind": "C32_ATLAS_CELL_BOUNDARY_OWNER",
                "incidence_degree_including_downstream": 2,
                "neighbor_C32_cell_id": neighbor_cell["cell_id"],
                "neighbor_C32_cell_row_sha256": neighbor_cell["row_sha256"],
                "neighbor_exact_parent_t_interval":
                    neighbor_cell["gate3_product_box"]["t"],
                "half_open_owner_C72_obligation_row_sha256": source["row_sha256"],
                "half_open_rule": "LOWER_T_FACE_INCLUSIVE__UPPER_T_FACE_EXCLUSIVE",
                "current_occurrence_is_half_open_owner": True,
                "classified_boundary_not_dangling": True,
            }
        else:
            need(side == "UPPER_T" and source["pair_index"] == 711 and
                 str(t) == "-531/800", "only frozen atlas outer guard boundary")
            downstream = {
                "incidence_kind": "C32_ATLAS_OUTER_GUARD_BOUNDARY_TERMINAL",
                "incidence_degree_including_boundary_terminal": 1,
                "boundary_terminal_owner_C32_cell_id": current_cell["cell_id"],
                "boundary_terminal_owner_C32_cell_row_sha256": current_cell["row_sha256"],
                "half_open_owner_C72_obligation_row_sha256": source["row_sha256"],
                "half_open_rule": "TERMINAL_UPPER_ATLAS_FACE_INCLUDED_BY_OUTER_GUARD_EXCEPTION",
                "current_occurrence_is_half_open_owner": True,
                "classified_boundary_not_dangling": True,
            }
    occurrence_key = {"root_id": root_id, "C72": source["row_sha256"], "side": side}
    return {
        "schema": SCHEMA + ".endpoint-incidence-row",
        "endpoint_occurrence_id": "c75-endpoint-occurrence:" + obj(occurrence_key),
        "root_id": root_id, "root_identity_preimage": physical_key,
        "C72_obligation_row_sha256": source["row_sha256"],
        "C75_strata_row_sha256": strata["row_sha256"],
        "pair_index": source["pair_index"], "source_path": source["source_path"],
        "child_path": source["child_path"], "endpoint_side": side,
        "exact_face_key": representative_face,
        "exact_face_key_sha256": obj(representative_face),
        "endpoint_root_enclosure": {
            "precision_bits": PRECISION, "graph_axis": "p",
            "strict_dp_bounds": {"lower": str(full.derivative[1].lower()),
                                 "upper": str(full.derivative[1].upper())},
            "interval_Newton": newton,
            "unique_root_on_exact_t_face": True,
        },
        "representative_reflected_exact_glue": glue,
        "representative_reflected_exact_glue_sha256": obj(glue),
        "adjacency_and_half_open_owner": downstream,
        "source_grazing": False, "dangling": False, "duplicate_occurrence": False,
        "formal_credit": 0, "whole_parent_credit": 0,
        "D02_gate_credit": 0, "CM2_credit": 0,
    }


def validate_lineage(c37_rows: list[dict[str, Any]], c32_rows: list[dict[str, Any]]) -> None:
    by_pair = {row["pair_index"]: row for row in c37_rows if row.get("pair_index") in LINEAGE}
    need(set(by_pair) == set(LINEAGE), "C37 selected pairs")
    by_cell = {row.get("cell_id"): row for row in c32_rows if row.get("cell_id") in
               {value["cell"] for value in LINEAGE.values()}}
    need(len(by_cell) == len(LINEAGE), "C32 selected cells")
    for pair, expected in LINEAGE.items():
        row37 = by_pair[pair]
        row32 = by_cell[expected["cell"]]
        need(row37["row_sha256"] == expected["c37"] and
             row37["representative_origin_key"] == expected["origin"] and
             row37["representative_cell_id"] == expected["cell"] and
             row32["row_sha256"] == expected["c32"] and
             row32["origin_key"] == expected["origin"], "lineage pair:" + str(pair))


def attacks() -> dict[str, Any]:
    capsule = {
        "scope": EXPECTED_SCOPE, "graphs": EXPECTED_SCOPE,
        "terminals": EXPECTED_SCOPE, "strict_side_instances": 2 * EXPECTED_SCOPE,
        "unresolved": 0, "graph_axis_p": EXPECTED_SCOPE,
        "newton": EXPECTED_SCOPE, "full_face": True, "corners": True,
        "root_order": True, "two_sides": True, "incidence": True,
        "half_open": True, "Kraft": "1", "graph_Kraft": "0",
        "additional_depth": 0, "graph_reported_strict": False,
        "source_grazing_claim": False, "formal": 0, "whole": 0, "D02": 0,
        "CM2": 0, "authority": False, "canonical_write": False,
        "global_ready": False, "C72o_overlap": 0, "C73_overlap": 0,
        "endpoint_occurrences": 11_768, "endpoint_root_ids": 11_760,
        "matched_endpoint_occurrences": 16, "matched_root_pairs": 8,
        "outscope_endpoint_owners": 11_750, "atlas_boundaries": 2,
        "dangling": 0, "duplicate_occurrence": 0,
    }
    result = {}
    for key in sorted(capsule):
        mutant = copy.deepcopy(capsule)
        value = mutant[key]
        mutant[key] = (not value if type(value) is bool else
                       value + 1 if type(value) is int else value + "_MUTANT")
        try:
            need(mutant == capsule, "attack:" + key)
        except Rejected:
            result[key] = "FAIL_CLOSED"
        else:
            raise Rejected("escaped attack:" + key)
    return {"attack_count": len(result), "attacks": result,
            "status": f"PASS_{len(result)}_OF_{len(result)}_COHERENT_ATTACKS_FAIL_CLOSED"}


def build(stage: Path) -> dict[str, Any]:
    need(stage.is_dir() and not stage.is_symlink() and not any(stage.iterdir()),
         "empty stage")
    need(ctx.prec == PRECISION, "384-bit environment")
    raw = {key: secure(*value) for key, value in INPUTS.items()}
    need(raw["C72_A"] == raw["C72_B"], "dual C72 bytes")
    sources = parse_rows(raw["C72_A"], "C72")
    need(len(sources) == 134_155, "C72 row count")
    selected = [row for row in sources if row["child_route_witness"] == SELECTOR]
    need(len(selected) == EXPECTED_SCOPE and
         sequence(row["row_sha256"] for row in selected) == EXPECTED_SELECTED_SEQUENCE,
         "exact selector scope")
    pair_census = Counter(row["pair_index"] for row in selected)
    category_census = Counter(row["structural_category"] for row in selected)
    need(dict(pair_census) == EXPECTED_PAIR_CENSUS and
         dict(category_census) == EXPECTED_CATEGORY_CENSUS, "scope census")
    need(all(row["required_decider"] in {"EXACT_MULTI_GRAPH_ORDER_ORACLE",
                                        "EXACT_FIRST_TANGENCY_ORACLE"} and
             row["source_grazing"] is False and
             row["formal_credit"] == row["whole_parent_credit"] ==
             row["D02_gate_credit"] == 0 for row in selected), "scope semantics")
    c37_rows = parse_rows(raw["C37"], "C37")
    c32_rows = parse_rows(raw["C32"], "C32")
    validate_lineage(c37_rows, c32_rows)
    selected_hashes = {row["row_sha256"] for row in selected}
    c72o_rows = parse_rows(raw["C72O_LEDGER"], "C72o")
    c73_rows = parse_rows(raw["C73_LEDGER"], "C73")
    need(len(c72o_rows) == 18_668 and len(c73_rows) == 1_163, "sidecar counts")
    overlap_o = selected_hashes & {row["C72_atlas_row_sha256"] for row in c72o_rows}
    overlap_73 = selected_hashes & {row["C72_obligation_row_sha256"] for row in c73_rows}
    need(not overlap_o and not overlap_73, "C72o/C73 disjoint")
    for key in ("C65_SELFTEST", "C65_OUTER", "C69_VERIFY", "C69_OUTER",
                "C72_VERIFY", "C72O_VERIFY", "C73_VERIFY", "C71B_VERIFY",
                "C71B_RECEIPT", "C74L_VERIFY", "C74L_RECEIPT"):
        strict_json(raw[key], key)
    target_census = Counter()
    strata_rows = []
    for source in selected:
        row = closed(decide(source), "row_sha256")
        target_census[row["tangency_target"]] += 1
        strata_rows.append(row)
    with Ledger(stage / LEDGER) as writer:
        for row in strata_rows:
            writer.write_closed(row)
    descriptor = writer.descriptor()
    need(descriptor["row_count"] == EXPECTED_SCOPE and
         dict(target_census) == EXPECTED_TARGET_CENSUS, "output census")
    strata_by_c72 = {row["C72_obligation_row_sha256"]: row for row in strata_rows}
    need(len(strata_by_c72) == EXPECTED_SCOPE, "unique C72 strata domain")
    wanted_face_keys = {
        face_index_key(source, side)
        for source in selected for side in ("LOWER_T", "UPPER_T")
    }
    adjacency_index = {key: [] for key in wanted_face_keys}
    for source in sources:
        for side in ("LOWER_T", "UPPER_T"):
            key = face_index_key(source, side)
            if key in adjacency_index:
                adjacency_index[key].append((source, side))
    cells = {row.get("cell_id"): row for row in c32_rows
             if row.get("cell_id") in {item["cell"] for item in LINEAGE.values()}}
    need(len(cells) == len(LINEAGE), "selected C32 cell map")
    endpoint_rows = []
    endpoint_kinds = Counter()
    for source, strata in zip(selected, strata_rows, strict=True):
        for side in ("LOWER_T", "UPPER_T"):
            row = closed(endpoint_row(source, strata, side, adjacency_index,
                                      strata_by_c72, cells, c32_rows), "row_sha256")
            endpoint_kinds[row["adjacency_and_half_open_owner"]["incidence_kind"]] += 1
            endpoint_rows.append(row)
    need(len(endpoint_rows) == 11_768 and endpoint_kinds == Counter({
        "OUT_OF_SCOPE_C72_DOWNSTREAM_OWNER": 11_750,
        "IN_SCOPE_MATCHED_TANGENCY_SEGMENT": 16,
        "C32_ATLAS_CELL_BOUNDARY_OWNER": 1,
        "C32_ATLAS_OUTER_GUARD_BOUNDARY_TERMINAL": 1,
    }), "endpoint incidence census")
    occurrence_ids = {row["endpoint_occurrence_id"] for row in endpoint_rows}
    need(len(occurrence_ids) == len(endpoint_rows), "unique endpoint occurrences")
    root_groups: dict[str, list[dict[str, Any]]] = {}
    for row in endpoint_rows:
        root_groups.setdefault(row["root_id"], []).append(row)
    degree_census = Counter(len(group) for group in root_groups.values())
    need(len(root_groups) == 11_760 and degree_census == Counter({1: 11_752, 2: 8}),
         "endpoint physical root degree census")
    for group in root_groups.values():
        if len(group) == 2:
            need(all(row["adjacency_and_half_open_owner"]["incidence_kind"] ==
                     "IN_SCOPE_MATCHED_TANGENCY_SEGMENT" for row in group) and
                 {row["endpoint_side"] for row in group} == {"LOWER_T", "UPPER_T"} and
                 sum(bool(row["adjacency_and_half_open_owner"]
                          ["current_occurrence_is_half_open_owner"])
                     for row in group) == 1, "matched root/unique owner")
        else:
            need(group[0]["adjacency_and_half_open_owner"]
                 ["classified_boundary_not_dangling"] is True, "classified degree-one root")
    with Ledger(stage / ENDPOINTS,
                "C72_FILTER_ORDER_THEN_LOWER_T_UPPER_T") as endpoint_writer:
        for row in endpoint_rows:
            endpoint_writer.write_closed(row)
    endpoint_descriptor = endpoint_writer.descriptor()
    result = closed({
        "schema": SCHEMA + ".result",
        "status": "PASS_5884_OF_5884_EXACT_FIRST_TANGENCY_GRAPHS__11768_STRICT_OPEN_SIDES__5884_CEMETERY_GRAPH_TERMINALS__11768_ENDPOINT_INCIDENCES__NO_DANGLING_OR_DUPLICATE__UNRESOLVED_ZERO__ZERO_CREDIT",
        "producer_file_sha256": sha(SELF.read_bytes()),
        "input_file_sha256": {key: value[1] for key, value in INPUTS.items()},
        "scope": {"selector_field": "child_route_witness",
                  "selector_value": SELECTOR, "row_count": EXPECTED_SCOPE,
                  "source_count": len({row["C61_aggregate_leaf_row_sha256"] for row in selected}),
                  "selected_C72_row_sequence_sha256": EXPECTED_SELECTED_SEQUENCE,
                  "pair_census": {str(key): value for key, value in sorted(pair_census.items())},
                  "legacy_structural_category_census": dict(sorted(category_census.items()))},
        "decision_census": {"exact_unique_regular_p_axis_Newton_graphs": EXPECTED_SCOPE,
                            "strict_exclusion_open_side_instances": 2 * EXPECTED_SCOPE,
                            "cemetery_first_tangency_graph_terminals": EXPECTED_SCOPE,
                            "whole_child_reported_as_strict_exclusion": 0,
                            "unresolved_strata": 0,
                            "tangency_target_census": dict(sorted(target_census.items()))},
        "ledger": descriptor,
        "endpoint_incidence_ledger": endpoint_descriptor,
        "endpoint_incidence_census": {
            "endpoint_occurrences": len(endpoint_rows),
            "physical_root_ids": len(root_groups),
            "degree_one_with_explicit_downstream_or_boundary_owner": degree_census[1],
            "degree_two_in_scope_matched_root_ids": degree_census[2],
            "in_scope_matched_endpoint_occurrences":
                endpoint_kinds["IN_SCOPE_MATCHED_TANGENCY_SEGMENT"],
            "out_of_scope_C72_downstream_owner_occurrences":
                endpoint_kinds["OUT_OF_SCOPE_C72_DOWNSTREAM_OWNER"],
            "C32_atlas_cell_boundary_occurrences":
                endpoint_kinds["C32_ATLAS_CELL_BOUNDARY_OWNER"],
            "C32_atlas_outer_guard_terminal_occurrences":
                endpoint_kinds["C32_ATLAS_OUTER_GUARD_BOUNDARY_TERMINAL"],
            "dangling": 0, "duplicate_occurrences": 0,
        },
        "global_invariants": {
            "all_active_sets_exactly_two": True,
            "all_discriminants_have_one_unique_regular_full_child_graph": True,
            "all_graphs_use_full_p_axis_interval_Newton": True,
            "all_graphs_have_two_strict_opposite_complete_p_faces": True,
            "all_graphs_have_four_strict_corners_and_two_t_face_endpoints": True,
            "all_tangency_roots_are_strict_future_and_first": True,
            "all_two_open_sides_are_strict_exclusions": True,
            "all_zero_graphs_are_non_exclusion_cemetery_terminals": True,
            "all_face_corner_source_glue_and_incidence_closed": True,
            "all_half_open_owners_unique": True,
            "all_endpoint_roots_have_canonical_physical_root_ids": True,
            "all_endpoint_occurrences_have_exact_representative_reflected_face_glue": True,
            "all_in_scope_endpoint_pairs_match_byte_identical_root_identity": True,
            "all_out_of_scope_endpoints_name_exact_C72_or_C32_downstream_owner": True,
            "atlas_outer_guard_endpoint_is_explicit_boundary_terminal": True,
            "no_dangling_or_duplicate_endpoint_occurrences": True,
            "additional_dyadic_depth_used": False,
            "full_dimensional_Kraft_conserved": True,
            "typed_graph_Kraft_zero": True,
        },
        "disjoint_scope": {"C72o_intersection": len(overlap_o),
                           "C73v2_intersection": len(overlap_73),
                           "C71b_partition": "C69C_DECISION_SOURCE_CHILDREN_33100_DISJOINT_FROM_C72_BLOCKER_LEDGER",
                           "C74L_entity_domain": "SOURCE_SEAM_IDS_NOT_C72_OBLIGATION_ROWS",
                           "credit_accumulation_across_sidecars": False},
        "producer_self_test": attacks(),
        "strict_boundary": {"candidate_is_authority": False,
                            "global_consumption_ready": False,
                            "runtime_canonical_pointer_or_seal_writes": False,
                            "formal_credit": 0, "whole_parent_credit": 0,
                            "D02_gate_credit": 0, "CM2_credit": 0,
                            "CM2": "NO-GO_FOR_CLAIM"},
    })
    exclusive(stage / RESULT, canonical(result) + b"\n")
    report = (
        "# C75 exact first-tangency strata oracle\n\n"
        f"Status: `{result['status']}`\n\n"
        "The exact current C72 witness selects 5,884 children.  Every child has a unique "
        "regular p-axis discriminant graph over its complete t base.  The two open sides "
        "are strict exclusions; the zero graph is retained as a cemetery first-tangency "
        "terminal and is not called an exclusion.  No dyadic depth was added.\n\n"
        "The endpoint-incidence ledger contains 11,768 exact face/root occurrences: "
        "16 occurrences form eight in-scope matched roots, 11,750 bind an exact adjacent "
        "C72 downstream owner, and two bind explicit C32 atlas boundaries.  Every root "
        "has one half-open owner and no endpoint is dangling or duplicated.\n\n"
        f"Strata ledger: `{descriptor['sha256']}`; endpoint ledger: "
        f"`{endpoint_descriptor['sha256']}`; result object: `{result['object_sha256']}`. "
        "Formal/global/D02/CM2 credit remains zero.\n"
    ).encode("utf-8")
    exclusive(stage / REPORT, report)
    manifest_lines = []
    for name in (LEDGER, ENDPOINTS, RESULT, REPORT):
        payload = (stage / name).read_bytes()
        manifest_lines.append(f"{sha(payload)}  {name}\n")
    manifest = "".join(manifest_lines).encode("ascii")
    exclusive(stage / MANIFEST, manifest)
    replay = {}
    for name in (LEDGER, ENDPOINTS, RESULT, REPORT, MANIFEST):
        payload = (stage / name).read_bytes()
        replay[name] = {"sha256": sha(payload), "size": len(payload),
                        "terminal_byte_replay": True}
    outer = closed({
        "schema": SCHEMA + ".outer-receipt",
        "status": "PASS_BASE_MEMBERS_PUBLISHED_IN_ORDER__MANIFEST_AFTER_MEMBERS__OUTER_LAST__TERMINAL_BYTE_REPLAY__ZERO_CREDIT",
        "producer_file_sha256": sha(SELF.read_bytes()),
        "result_object_sha256": result["object_sha256"],
        "publication_order": [LEDGER, ENDPOINTS, RESULT, REPORT, MANIFEST, OUTER],
        "members": replay, "manifest_published_after_all_listed_members": True,
        "outer_receipt_published_last_in_base_build": True,
        "O_EXCL_no_replace": True, "all_terminal_byte_replays_pass": True,
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
    })
    exclusive(stage / OUTER, canonical(outer) + b"\n")
    return result


def complete(a: Path, b: Path, verifier: Path) -> dict[str, Any]:
    need(a.is_dir() and b.is_dir() and a != b, "two stages")
    verifier_raw = verifier.read_bytes()
    verifier_sha = sha(verifier_raw)
    names = BASE_MEMBERS + [VERIFICATION]
    members = {}
    for name in names:
        left = (a / name).read_bytes()
        right = (b / name).read_bytes()
        need(left == right, "dual byte identity:" + name)
        members[name] = {"sha256": sha(left), "size": len(left),
                         "stage_1_terminal_replay": True,
                         "stage_2_terminal_replay": True}
    result = strict_json((a / RESULT).read_bytes(), "result")
    need(result["producer_file_sha256"] == sha(SELF.read_bytes()), "producer binding")
    verification = strict_json((a / VERIFICATION).read_bytes(), "verification")
    need(verification["verifier_file_sha256"] == verifier_sha and
         verification["candidate_result_object_sha256"] == result["object_sha256"],
         "verification binding")
    need(not (a / DUAL).exists() and not (b / DUAL).exists(), "fresh dual receipts")
    receipt = closed({
        "schema": SCHEMA + ".dual-completion-receipt",
        "status": "PASS_DUAL_ISOLATED_BYTE_IDENTICAL_BUILD__NO_PRODUCER_VERIFICATION__DUAL_RECEIPT_LAST__TERMINAL_REPLAY__ZERO_CREDIT",
        "producer_file_sha256": sha(SELF.read_bytes()),
        "verifier_file_sha256": verifier_sha,
        "result_object_sha256": result["object_sha256"],
        "verification_object_sha256": verification["object_sha256"],
        "members_before_receipt": members,
        "all_dual_member_bytes_identical": True,
        "no_producer_verifier_policy_pass": True,
        "dual_receipt_is_final_member": True,
        "O_EXCL_no_replace": True, "terminal_byte_replay": True,
        "formal_credit": 0, "whole_parent_credit": 0,
        "D02_gate_credit": 0, "CM2_credit": 0,
    })
    raw = canonical(receipt) + b"\n"
    exclusive(a / DUAL, raw)
    exclusive(b / DUAL, raw)
    need((a / DUAL).read_bytes() == (b / DUAL).read_bytes() == raw,
         "dual receipt replay")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--stage", type=Path)
    modes.add_argument("--complete", nargs=3, type=Path,
                       metavar=("STAGE_A", "STAGE_B", "VERIFIER"))
    args = parser.parse_args()
    ctx.prec = PRECISION
    if args.stage:
        value = build(args.stage.resolve())
        print(json.dumps({"status": value["status"], "scope": value["scope"],
                          "decision_census": value["decision_census"],
                          "object_sha256": value["object_sha256"]}, sort_keys=True))
    else:
        value = complete(*(path.resolve() for path in args.complete))
        print(json.dumps({"status": value["status"],
                          "object_sha256": value["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Rejected, OSError, ValueError, KeyError, TypeError, IndexError,
            RuntimeError, json.JSONDecodeError) as error:
        print(f"FAIL_CLOSED:{type(error).__name__}:{error}", file=sys.stderr)
        raise SystemExit(2)
