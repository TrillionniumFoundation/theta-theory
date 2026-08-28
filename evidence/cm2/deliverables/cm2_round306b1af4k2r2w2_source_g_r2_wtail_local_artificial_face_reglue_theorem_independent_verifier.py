#!/usr/bin/env python3
"""Independent verifier for the four local R2 W-tail reglue theorems.

This verifier neither imports the producer nor imports the K1 kernel.  It
holds every authority and package file by descriptor, recomputes the five
ordered table commitments and selected source rows, reconstructs the physical
predicate AST, and evaluates the complete faces and both inward corridors
with an independently implemented 192-bit rational interval engine.  It then
executes a held-byte snapshot of the producer under two seeds solely for
deterministic cold replay and compares both candidate bundles byte-for-byte.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
from math import isqrt
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Any, BinaryIO, Final, Iterator, Mapping, TextIO


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Reject(label)


HERE: Final = Path(__file__).resolve().parent
PREFIX: Final = "cm2_round306b1af4k2r2w2_source_g_r2_wtail_local_artificial_face_reglue_theorem_"
PRODUCER: Final = PREFIX + "producer.py"
RESULT: Final = PREFIX + "result.json"
LEDGER: Final = PREFIX + "theorem_ledger.json"
ATTACK: Final = PREFIX + "attack_suite.json"
VERIFICATION: Final = PREFIX + "verification.json"
SCHEMA: Final = "cm2.round306b1af4k2r2w2.source-g-r2-wtail-local-artificial-face-reglue-theorem.v1"
STATUS: Final = "PASS_INDEPENDENT_REPLAY__4_LOCAL_REGLUES__4_COMPLETE_FACES__8_INWARD_CORRIDORS__ZERO_NORMALIZED_OR_GLOBAL_CREDIT"
ROW_LIMIT: Final = 8 << 20
READ_CHARS: Final = 1 << 18
BUFFER_LIMIT: Final = ROW_LIMIT + 4 * READ_CHARS
SQRT_BITS: Final = 192
HEX64 = re.compile(r"^[0-9a-f]{64}$")
TARGET = re.compile(r"^W\[(-?[0-9]+),(-?[0-9]+)\]$")


PINS: Final = (
    ("OLD_R2W_MANIFEST", "cm2_round306b1af4k2r2w_source_g_r2_wtail_exact_reglue_manifest.sha256", 1_089, "4abdb77dc106f1cfa4bb582d17fb48dcfc29869786330e9d784f268bb13cefc4"),
    ("OLD_R2W_RESULT", "cm2_round306b1af4k2r2w_source_g_r2_wtail_exact_reglue_result.json", 25_794, "87e10fcc3a79854a1361e3f4e836c48febb97a69fce47073bd38cf62c28db936"),
    ("OLD_R2W_LEDGER", "cm2_round306b1af4k2r2w_source_g_r2_wtail_exact_reglue_theorem_ledger.json", 19_662, "12642bc980beea0eaa23c13ceb531e9633e2680ad08847f44208606c26b38aae"),
    ("OLD_R2W_VERIFICATION", "cm2_round306b1af4k2r2w_source_g_r2_wtail_exact_reglue_verification.json", 854, "912ae2fbb45f8aa08aa76bf8599f5ff9f5508dd61941184b01ad0879ba6fd3b0"),
    ("R182_ROWS", "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json", 158_815_476, "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c"),
    ("R182_CERT", "cm2_round182_source_g_clipped_graph_and_pair_arrangement_certificate.json", 7_553, "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08"),
    ("R182_VERIFY", "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json", 4_956, "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36"),
    ("R271_CERT", "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json", 112_741_715, "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747"),
    ("R271_VERIFIER", "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_verifier.py", 18_627, "a8c5d5a1b055f8f0c7cd5f8fe6e5d598d15b543a5107a6665935944f5500c7e8"),
    ("B1R0_CELL", "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz", 105_989_322, "19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96"),
    ("B1R0_MEMBER", "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz", 123_019_951, "4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7"),
    ("R179_EVALUATOR", "cm2_round179_source_g_residual_tube_arrangement_verifier.py", 78_867, "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679"),
    ("FIRST_HIT_ENGINE", "cm2_gate3_candidate_first_hit_cert.py", 13_832, "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"),
    ("K1_MANIFEST", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_manifest.sha256", 933, "07a3f12e75c43fd459dfd4e86c918b349c09226c94735b1a6d16432f1caca939"),
    ("K1_SOURCE", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel.py", 68_346, "17d9c302984e2e29dcf02832f36ec9437c23c8b65c27289a3469db222ce4edae"),
    ("K1_RESULT", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_result.json", 2_787, "e9ff89a5d51f5e79864f10dc34dd4b5f12887c029f65c2196c60f50bd4c77b21"),
    ("PRODUCER", PRODUCER, 55_465, "a9d1ca8100f8ac7b882dcb836066aa7c10925229451b228f30683b40068aa993"),
    ("RESULT", RESULT, 8_276, "ed28b179673e0fcd108d4b99be31c0b4ced75236c6e29187218cd06ba4e5dac1"),
    ("LEDGER", LEDGER, 203_200, "e3c27d4e7159aadd4adf35fe98c81f8534de6af0b4d6b6436ec1cffa9fe51bb4"),
    ("ATTACK", ATTACK, 850, "182ce9c724c65eb8a91998dad264e02fd5c24212816bccbbce474023efa89fc4"),
)
PIN = {row[0]: row for row in PINS}

TABLES: Final = {
    "R182.occurrence": (54_220, "d77e65b5b9dfb5f7f107b39eaac3553be67ba76231f1888de1f97ecc121361db"),
    "R182.leaf": (202_840, "ced6d2764a7e1f5d404c1d56249e428f0754e53e7dded620e5904f9eb80b694c"),
    "R271.side": (70_420, "cec8a0318385127d8ee5d7968c016f8f6b7ee103596fbce5258cc3b25c4930b8"),
    "B1R0.cell": (295_340, "b89220807eef10bc8412be19c5037ea75fa3c6fdf4321c27938afec0c68c9246"),
    "B1R0.member": (295_336, "6665fc8e72824fba7dbd1d1b7462ae419bb31c25149037da3183d74569b62a3d"),
}

OCCURRENCE_COLUMNS: Final = (
    "row_id", "Round179_occurrence_row_id", "origin_row_id", "parent_id", "chart", "owner_target", "kind", "reason_label", "equation", "target_obstacle", "strict_t_derivative_sign", "Round179_origin_already_fully_replaced", "Round179_retained_child_count", "Round179_retained_coordinate_volume", "bounded_base_split_axis", "bounded_base_split_depth", "closed_leaf_count", "closed_coordinate_volume", "residual_leaf_count", "residual_coordinate_volume", "full_base_graph_leaf_count", "absent_graph_leaf_count", "clipped_graph_leaf_count", "two_dimensional_graph_sheet_count", "one_dimensional_clipping_curve_segment_count", "zero_dimensional_boundary_endpoint_incidence_count", "fully_clipped_over_Round179_retained_children", "leaf_rows_sha256", "whole_original_tube_credit", "global_exact_key_disposition_credit", "provenance",
)
LEAF_COLUMNS: Final = (
    "row_id", "occurrence_row_id", "retained_child_row_id", "base_refinement_path", "box", "coordinate_volume", "base_coordinate_area", "lower_t_face_status", "upper_t_face_status", "graph_classification", "two_dimensional_graph_sheet_count", "one_dimensional_clipping_curve_segment_count", "zero_dimensional_boundary_endpoint_incidence_count", "closed_3d_side_union_volume", "residual_3d_collar_volume",
)


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_hash(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def same_typed(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(same_typed(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(same_typed(a, b) for a, b in zip(left, right, strict=True))
    return bool(left == right)


def exact(left: Any, right: Any, label: str) -> None:
    require(same_typed(left, right), label)


def pairs_unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str and key not in out, "duplicate/non-string key")
        out[key] = value
    return out


def reject_decimal(token: str) -> Any:
    raise Reject("nonintegral/nonfinite JSON number:" + token)


DECODER = json.JSONDecoder(object_pairs_hook=pairs_unique, parse_float=reject_decimal, parse_constant=reject_decimal)


def strict_json_tree(value: Any, depth: int = 0) -> None:
    require(depth <= 256, "JSON depth")
    if value is None or type(value) in {str, bool, int}:
        return
    require(type(value) in {list, dict}, "JSON type")
    if type(value) is dict:
        require(all(type(k) is str for k in value), "JSON key")
        values = value.values()
    else:
        values = value
    for item in values:
        strict_json_tree(item, depth + 1)


def parse_json(raw: bytes, label: str, limit: int = ROW_LIMIT) -> Any:
    require(0 < len(raw) <= limit and b"\x00" not in raw and not raw.startswith(b"\xef\xbb\xbf"), "raw cap:" + label)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs_unique, parse_float=reject_decimal, parse_constant=reject_decimal)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject("decode:" + label) from exc
    strict_json_tree(value)
    require(len(canon(value)) <= limit, "post-success canonical cap:" + label)
    return value


def closed(row: Any, label: str) -> None:
    require(type(row) is dict and type(row.get("row_sha256")) is str and HEX64.fullmatch(row["row_sha256"]) is not None, "closed row:" + label)
    body = dict(row)
    claimed = body.pop("row_sha256")
    require(object_hash(body) == claimed, "row digest:" + label)


def file_identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def fd_hash(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            os.lseek(fd, 0, os.SEEK_SET)
            return digest.hexdigest()
        digest.update(block)


class HeldInputs:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve(strict=True)
        self.dirfd = -1
        self.dir_stat: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.stats: dict[str, os.stat_result] = {}

    def __enter__(self) -> "HeldInputs":
        named_dir = os.stat(self.root, follow_symlinks=False)
        require(stat.S_ISDIR(named_dir.st_mode) and not self.root.is_symlink(), "input directory")
        self.dirfd = os.open(self.root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dir_stat = os.fstat(self.dirfd)
        require((named_dir.st_dev, named_dir.st_ino, named_dir.st_mode) == (self.dir_stat.st_dev, self.dir_stat.st_ino, self.dir_stat.st_mode), "directory race")
        try:
            for label, name, size, digest in PINS:
                named = os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
                require(stat.S_ISREG(named.st_mode) and named.st_nlink == 1 and named.st_size == size, "pin identity:" + label)
                fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                require(file_identity(named) == file_identity(opened), "open race:" + label)
                require(fd_hash(fd) == digest and fd_hash(fd) == digest, "two-pass hash:" + label)
                require(file_identity(opened) == file_identity(os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)), "path rebound:" + label)
                self.fds[label] = fd
                self.stats[label] = opened
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def bytes(self, label: str) -> bytes:
        fd = self.fds[label]
        os.lseek(fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                os.lseek(fd, 0, os.SEEK_SET)
                return b"".join(chunks)
            chunks.append(block)

    def rows(self, label: str, marker: str, anchor: str | None = None) -> Iterator[Any]:
        fd = self.fds[label]
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.fdopen(os.dup(fd), "rb")
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if PIN[label][1].endswith(".gz") else raw
        text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
        try:
            yield from array_rows(text, marker, anchor)
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            os.lseek(fd, 0, os.SEEK_SET)
            require(file_identity(os.fstat(fd)) == file_identity(self.stats[label]), "stream identity:" + label)

    def final(self) -> None:
        require(self.dir_stat is not None, "snapshot active")
        current_dir = os.stat(self.root, follow_symlinks=False)
        require((current_dir.st_dev, current_dir.st_ino, current_dir.st_mode) == (self.dir_stat.st_dev, self.dir_stat.st_ino, self.dir_stat.st_mode), "final directory")
        for label, name, size, digest in PINS:
            held = os.fstat(self.fds[label])
            named = os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
            require(file_identity(held) == file_identity(named) == file_identity(self.stats[label]), "final identity:" + label)
            require(held.st_nlink == 1 and held.st_size == size and fd_hash(self.fds[label]) == digest, "final pin:" + label)

    def __exit__(self, *_args: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        self.fds.clear()
        if self.dirfd >= 0:
            os.close(self.dirfd)
            self.dirfd = -1


def array_rows(stream: TextIO, marker: str, anchor: str | None = None) -> Iterator[Any]:
    def fill(buffer: str, label: str) -> str:
        chunk = stream.read(READ_CHARS)
        require(bool(chunk), label)
        result = buffer + chunk
        require(len(result.encode("utf-8")) <= BUFFER_LIMIT, "parser buffer cap")
        return result

    def find(token: str, buffer: str) -> str:
        while True:
            pos = buffer.find(token)
            if pos >= 0:
                return buffer[pos + len(token):]
            buffer = fill(buffer, "missing marker:" + token)
            pos = buffer.find(token)
            if pos >= 0:
                return buffer[pos + len(token):]
            buffer = buffer[-max(1, len(token) - 1):]

    buffer = ""
    if anchor is not None:
        buffer = find(anchor, buffer)
    buffer = find(marker, buffer)
    buffer = buffer.lstrip()
    if buffer.startswith(":"):
        buffer = buffer[1:].lstrip()
        require(buffer.startswith("["), "array marker")
        buffer = buffer[1:]
    need_comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            buffer = fill(buffer, "truncated array").lstrip()
        if buffer[0] == "]":
            return
        if need_comma:
            require(buffer[0] == ",", "missing comma")
            buffer = buffer[1:].lstrip()
            while not buffer:
                buffer = fill(buffer, "truncated row").lstrip()
            require(buffer[0] != "]", "trailing comma")
        else:
            require(buffer[0] != ",", "leading comma")
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                require(len(buffer.encode("utf-8")) <= ROW_LIMIT, "row predecode cap")
                buffer = fill(buffer, "truncated JSON row")
        require(len(buffer[:end].encode("utf-8")) <= ROW_LIMIT, "mandatory decoded-row cap")
        strict_json_tree(value)
        require(len(canon(value)) <= ROW_LIMIT, "mandatory canonical-row cap")
        yield value
        buffer = buffer[end:]
        need_comma = True


class ArrayHash:
    def __init__(self) -> None:
        self.digest = hashlib.sha256(b"[")
        self.count = 0

    def add(self, row: Any) -> None:
        if self.count:
            self.digest.update(b",")
        self.digest.update(canon(row))
        self.count += 1

    def finish(self) -> str:
        copy = self.digest.copy()
        copy.update(b"]")
        return copy.hexdigest()


def scan(snapshot: HeldInputs, label: str, table: str, marker: str, select: Any, *, anchor: str | None = None, rows_closed: bool = False) -> tuple[dict[str, Any], list[Any]]:
    state = ArrayHash()
    chosen: list[Any] = []
    for row in snapshot.rows(label, marker, anchor):
        if rows_closed:
            closed(row, table)
        state.add(row)
        if select(row):
            chosen.append(row)
    count, digest = TABLES[table]
    require(state.count == count and state.finish() == digest, "table commitment:" + table)
    return {"table":table,"row_count":count,"rows_sha256":digest,"row_sha256_checked":rows_closed}, chosen


def qdict(value: Q | int) -> dict[str, int]:
    q = Q(value)
    return {"numerator":q.numerator,"denominator":q.denominator}


def qfrom(value: Any, label: str) -> Q:
    require(type(value) is dict and set(value) == {"numerator", "denominator"}, label)
    n, d = value["numerator"], value["denominator"]
    require(type(n) is int and type(d) is int and d > 0, label)
    q = Q(n, d)
    require(q.numerator == n and q.denominator == d, label)
    return q


def box_text(value: Any, label: str) -> tuple[Q, ...]:
    require(type(value) is list and len(value) == 6 and all(type(x) is str for x in value), label)
    box = tuple(Q(x) for x in value)
    require(all(str(q) == text for q, text in zip(box, value, strict=True)), label)
    return box


@dataclass(frozen=True)
class Bound:
    lo: Q
    hi: Q

    def __post_init__(self) -> None:
        require(type(self.lo) is Q and type(self.hi) is Q and self.lo <= self.hi, "bound")

    @classmethod
    def point(cls, value: Q) -> "Bound":
        return cls(value, value)

    def __neg__(self) -> "Bound":
        return Bound(-self.hi, -self.lo)

    def __add__(self, other: "Bound") -> "Bound":
        return Bound(self.lo + other.lo, self.hi + other.hi)

    def __sub__(self, other: "Bound") -> "Bound":
        return self + (-other)

    def __mul__(self, other: "Bound") -> "Bound":
        values = (self.lo*other.lo, self.lo*other.hi, self.hi*other.lo, self.hi*other.hi)
        return Bound(min(values), max(values))

    def square(self) -> "Bound":
        ends = (self.lo*self.lo, self.hi*self.hi)
        return Bound(Q(0) if self.lo <= 0 <= self.hi else min(ends), max(ends))

    def divide(self, other: "Bound") -> "Bound":
        require(not other.lo <= 0 <= other.hi, "division domain")
        reciprocal = Bound(min(Q(1,other.lo),Q(1,other.hi)), max(Q(1,other.lo),Q(1,other.hi)))
        return self * reciprocal


def sqrt_bound(value: Bound, bits: int) -> Bound:
    require(value.lo > 0, "sqrt positive domain")
    require(type(bits) is int and 64 <= bits <= 512, "sqrt precision")
    scale = 1 << bits
    def floor_root(q: Q) -> Q:
        return Q(isqrt((q.numerator * scale * scale) // q.denominator), scale)
    lo = floor_root(value.lo)
    hi = floor_root(value.hi)
    if hi*hi != value.hi:
        hi += Q(1, scale)
    require(lo*lo <= value.lo and hi*hi >= value.hi, "sqrt enclosure")
    return Bound(lo, hi)


def cq(value: Q | int) -> dict[str, Any]: return {"op":"CONST_Q","value":qdict(value)}
def var(name: str) -> dict[str, Any]: return {"op":"VAR","name":name}
def minus(arg: Any) -> dict[str, Any]: return {"op":"NEG","arg":arg}
def plus(*args: Any) -> dict[str, Any]: return {"op":"ADD","args":list(args)}
def difference(left: Any, right: Any) -> dict[str, Any]: return {"op":"SUB","left":left,"right":right}
def product(*args: Any) -> dict[str, Any]: return {"op":"MUL","args":list(args)}
def squared(arg: Any) -> dict[str, Any]: return {"op":"SQUARE","arg":arg}
def positive_root(arg: Any) -> dict[str, Any]: return {"op":"SQRT_POSITIVE","arg":arg}
def quotient(left: Any, right: Any) -> dict[str, Any]: return {"op":"DIV_NONZERO","left":left,"right":right}


def expected_asts(chart: str, owner: str) -> dict[str, Any]:
    match = TARGET.fullmatch(owner)
    require(chart in {"G:E","G:W"} and match is not None, "supported physical input")
    ix, iy = int(match.group(1)), int(match.group(2))
    t, p, s = var("t"), var("p"), var("s")
    tr, pr = difference(cq(1),squared(t)), difference(cq(1),squared(p))
    rt, rp = positive_root(tr), positive_root(pr)
    nx, ny = (rt if chart == "G:E" else minus(rt)), t
    ux = difference(product(rp,nx),product(p,ny))
    uy = plus(product(rp,ny),product(p,nx))
    sx, sy = product(cq(Q(9,25)),nx), product(cq(Q(9,25)),ny)
    cx, cy = plus(cq(Q(2*ix+1,2)),s), cq(Q(2*iy+1,2))
    dx, dy = difference(cx,sx), difference(cy,sy)
    transverse = plus(minus(product(uy,dx)),product(ux,dy))
    disc = difference(cq(Q(16,625)),squared(transverse))
    radical = positive_root(disc)
    outx = quotient(plus(minus(product(radical,ux)),product(transverse,uy)),cq(Q(4,25)))
    outy = quotient(difference(minus(product(radical,uy)),product(transverse,ux)),cq(Q(4,25)))
    factor = difference(squared(outx),squared(outy))
    return {"source_t_radical_argument_ast":tr,"direction_p_radical_argument_ast":pr,"selected_root_discriminant_ast":disc,"target_normal_x_ast":outx,"target_normal_y_ast":outy,"outgoing_factor_ast":factor,"strict_negative_predicate_ast":{"op":"LT_ZERO","arg":factor}}


def eval_scalar(node: Any, environment: Mapping[str, Bound], bits: int = SQRT_BITS) -> Bound:
    require(type(node) is dict and type(node.get("op")) is str, "AST node")
    op = node["op"]
    if op == "CONST_Q": return Bound.point(qfrom(node["value"], "constant"))
    if op == "VAR":
        require(set(node) == {"op","name"} and node["name"] in environment, "AST variable")
        return environment[node["name"]]
    if op == "NEG": return -eval_scalar(node["arg"],environment,bits)
    if op == "ADD":
        args = node.get("args")
        require(type(args) is list and len(args) >= 2, "ADD arity")
        result = eval_scalar(args[0],environment,bits)
        for item in args[1:]: result = result + eval_scalar(item,environment,bits)
        return result
    if op == "SUB": return eval_scalar(node["left"],environment,bits)-eval_scalar(node["right"],environment,bits)
    if op == "MUL":
        args = node.get("args")
        require(type(args) is list and len(args) >= 2, "MUL arity")
        result = eval_scalar(args[0],environment,bits)
        for item in args[1:]: result = result * eval_scalar(item,environment,bits)
        return result
    if op == "SQUARE": return eval_scalar(node["arg"],environment,bits).square()
    if op == "SQRT_POSITIVE": return sqrt_bound(eval_scalar(node["arg"],environment,bits),bits)
    if op == "DIV_NONZERO": return eval_scalar(node["left"],environment,bits).divide(eval_scalar(node["right"],environment,bits))
    raise Reject("unsupported AST op:" + op)


def environment(box: tuple[Q,...]) -> dict[str,Bound]:
    return {"t":Bound(box[0],box[1]),"p":Bound(box[2],box[3]),"s":Bound(box[4],box[5])}


def bound_wire(value: Bound) -> dict[str,Any]:
    return {"lower":qdict(value.lo),"upper":qdict(value.hi)}


def compute_receipt(asts: dict[str,Any], box: tuple[Q,...], label: str, bits: int) -> dict[str,Any]:
    env = environment(box)
    t_domain=eval_scalar(asts["source_t_radical_argument_ast"],env,bits)
    p_domain=eval_scalar(asts["direction_p_radical_argument_ast"],env,bits)
    discriminant=eval_scalar(asts["selected_root_discriminant_ast"],env,bits)
    factor=eval_scalar(asts["outgoing_factor_ast"],env,bits)
    require(t_domain.lo>0 and p_domain.lo>0 and discriminant.lo>0,"predicate domain:"+label)
    return {"label":label,"box":[str(x) for x in box],"source_t_radical_argument_interval":bound_wire(t_domain),"direction_p_radical_argument_interval":bound_wire(p_domain),"selected_root_discriminant_interval":bound_wire(discriminant),"outgoing_factor_interval":bound_wire(factor),"outgoing_factor_strict_negative":factor.hi<0}


def verify_receipt(asts: dict[str,Any], box: tuple[Q,...], label: str, stored: Any, *, require_negative: bool) -> None:
    # Exact wire replay uses the producer's frozen 128-bit outward convention;
    # the independent 192-bit pass below is the authoritative sign/domain test.
    exact(stored,compute_receipt(asts,box,label,128),"stored interval receipt:"+label)
    stronger=compute_receipt(asts,box,label,SQRT_BITS)
    if require_negative:
        require(stronger["outgoing_factor_strict_negative"] is True,"strict F negative:"+label)
    else:
        require(type(stronger["outgoing_factor_strict_negative"]) is bool,"parent F diagnostic")


def wire_box(value: Any, label: str) -> tuple[tuple[Q,...],tuple[bool,bool]]:
    require(type(value) is dict and value.get("wire_id") == "RATIONAL_INTERVAL_BOX_V1" and value.get("coordinate_parameter") == "TPS", label)
    axes = value.get("axes")
    require(type(axes) is list and [axis.get("axis") for axis in axes] == ["t","p","s"], label)
    bounds: list[Q] = []
    for axis in axes:
        require(type(axis.get("lower_closed")) is bool and type(axis.get("upper_closed")) is bool, label)
        bounds += [qfrom(axis["lower"],label),qfrom(axis["upper"],label)]
    require(axes[1]["lower_closed"] is axes[1]["upper_closed"] is axes[2]["lower_closed"] is axes[2]["upper_closed"] is True, label)
    return tuple(bounds), (axes[0]["lower_closed"],axes[0]["upper_closed"])


ZERO_FIELDS: Final = ("normalized_support_credit","representation_cover_credit","physical_incidence_equivalence_credit","A1_A2_credit","B1A_credit","B2_credit","transition_credit","pair_routing_credit","maximality_credit","fibre_credit","global_disposition_credit")


def validate_row(row: dict[str,Any], producer_receipt: dict[str,Any]) -> dict[str,Any]:
    closed(row,"candidate")
    require(row["schema"] == SCHEMA+".row.v1" and type(row["candidate_r2_artificial_face_reglue_credit"]) is int and row["candidate_r2_artificial_face_reglue_credit"] == 1, "row candidate credit")
    require(type(row["r2_artificial_face_reglue_credit"]) is int and row["r2_artificial_face_reglue_credit"] == 0 and type(row["credit_effective_only_with_manifest_pinned_PASS_independent_verification"]) is bool and row["credit_effective_only_with_manifest_pinned_PASS_independent_verification"] is True,"row pre-seal credit gate")
    require(type(row["normalized_support_credit"]) is int and row["normalized_support_credit"] == 0 and row["CM2"] == "NO-GO_FOR_CLAIM", "row nonpromotion")
    commitment = row["canonical_input_commitment"]
    require(commitment["member_id"]==row["member_id"] and type(commitment["source_chart"]) is str and type(commitment["owner_target"]) is str,"row/input identity")
    exact(commitment["producer_source_commitment"],producer_receipt,"producer receipt")
    exact(commitment["physical_model_source_sha256"],{"FIRST_HIT_ENGINE":PIN["FIRST_HIT_ENGINE"][3],"R179_EVALUATOR":PIN["R179_EVALUATOR"][3],"R271_VERIFIER":PIN["R271_VERIFIER"][3]},"physical model pins")
    asts = expected_asts(commitment["source_chart"],commitment["owner_target"])
    theorem = row["local_theorem"]
    require(theorem["theorem_kind"] == "LOCAL_ARTIFICIAL_FACE_REGLUE_EXACT_V3", "theorem kind")
    exact(theorem["source_free_predicate"]["asts"],asts,"independent AST reconstruction")
    digest = object_hash(asts["strict_negative_predicate_ast"])
    require(theorem["source_free_predicate"]["predicate_ast_sha256"] == digest == commitment["predicate_ast_sha256"], "AST binding")
    partition = theorem["canonical_half_open_partition"]
    parent, parent_flags = wire_box(partition["parent_box"],"parent box")
    children = [wire_box(value,"child box") for value in partition["owned_child_boxes"]]
    require(parent_flags == (True,True) and [flags for _,flags in children] == [(True,False),(True,True)], "half-open ownership")
    first, second = children[0][0], children[1][0]
    midpoint = first[1]
    require(first[0] == parent[0] and second[1] == parent[1] and midpoint == second[0] == (parent[0]+parent[1])/2, "exact t cover")
    require(first[2:] == second[2:] == parent[2:] and partition["interface_owner_t_child"] == 1 and partition["exact_t_atom_count"] == 5, "exact base/owner")
    verify_receipt(asts,parent,"PARENT_DOMAIN",theorem["predicate_domain_on_parent"],require_negative=False)
    equality = theorem["child_parent_full_support_set_equality"]
    require(all(type(equality[key]) is bool and equality[key] for key in ("same_predicate_ast_on_parent_and_both_children","owned_boxes_disjoint","owned_boxes_union_parent")), "set equality")
    require(type(equality["candidate_local_full_support_set_equality_credit"]) is int and equality["candidate_local_full_support_set_equality_credit"] == 1 and type(equality["local_full_support_set_equality_credit_before_package_seal"]) is int and equality["local_full_support_set_equality_credit_before_package_seal"] == 0 and type(equality["normalized_support_credit"]) is int and equality["normalized_support_credit"] == 0, "local-only candidate set credit")
    face = box_text(theorem["complete_artificial_face"]["face_box"],"face")
    corridors = theorem["two_sided_inward_corridors"]
    left = box_text(corridors["left"]["box"],"left corridor")
    right = box_text(corridors["right"]["box"],"right corridor")
    width = (first[1]-first[0])/8
    require(face == (midpoint,midpoint,*parent[2:]), "complete face")
    require(left == (midpoint-width,midpoint,*parent[2:]) and right == (midpoint,midpoint+width,*parent[2:]), "two inward corridors")
    area = (parent[3]-parent[2])*(parent[5]-parent[4])
    volume = width*area
    require(area == Q(1,204800) and volume == Q(177,209715200000), "exact geometry")
    require(theorem["complete_artificial_face"]["exact_area"] == str(area) and corridors["corridor_width"] == str(width) and corridors["each_exact_volume"] == str(volume), "geometry wire")
    verify_receipt(asts,face,"COMPLETE_INTERFACE_FACE",theorem["complete_artificial_face"]["interval_receipt"],require_negative=True)
    verify_receipt(asts,left,"LEFT_CHILD_INWARD_CORRIDOR",corridors["left"],require_negative=True)
    verify_receipt(asts,right,"RIGHT_CHILD_INWARD_CORRIDOR",corridors["right"],require_negative=True)
    require(type(theorem["complete_artificial_face"]["outgoing_F_zero_graph_absent_on_complete_face"]) is bool and theorem["complete_artificial_face"]["outgoing_F_zero_graph_absent_on_complete_face"], "face conclusion")
    require(type(corridors["both_strictly_inside_same_F_negative_physical_cell"]) is bool and corridors["both_strictly_inside_same_F_negative_physical_cell"], "corridor conclusion")
    cross = theorem["K1_zero_credit_cross_checker"]
    cross_body = dict(cross); claimed_cross = cross_body.pop("cross_check_digest_sha256")
    require(object_hash(cross_body) == claimed_cross and type(cross["formal_credit"]) is int and cross["formal_credit"] == 0, "K1 zero-credit binding")
    conclusion = row["local_conclusion"]
    require(type(conclusion["candidate_r2_artificial_face_reglue_credit"]) is int and conclusion["candidate_r2_artificial_face_reglue_credit"] == 1 and type(conclusion["r2_artificial_face_reglue_credit_before_package_seal"]) is int and conclusion["r2_artificial_face_reglue_credit_before_package_seal"] == 0, "conclusion candidate credit")
    exact(conclusion["local_authorities_discharged_by_candidate"],["SOURCE_FREE_INTERVAL_PREDICATE_AST_AND_EQUIVALENCE_THEOREM_FOR_BOTH_CHILDREN","INPUT_BOUND_WHOLE_FACE_AND_TWO_SIDED_INWARD_CORRIDOR_PHYSICAL_EQUIVALENCE_CERTIFICATE","CANONICAL_HALF_OPEN_OWNER_ASSIGNMENT_FOR_THE_ARTIFICIAL_INTERFACE"],"three local authorities")
    exact(conclusion["package_seal_condition"],{"required_role":"SEALED_INDEPENDENT_VERIFIER_RECEIPT_PINNED_BY_EXACT_8_MEMBER_MANIFEST","satisfied_inside_producer":False,"candidate_credit_effective_before_package_seal":False},"package seal condition")
    for key in ("same_R182_parent","same_complete_10_field_signature","same_owner_target","same_strict_negative_factor_cell","artificial_interface_is_not_F_zero_physical_separator","two_source_cells_are_one_local_physical_region_across_interface"):
        require(type(conclusion[key]) is bool and conclusion[key], "conclusion:"+key)
    nonpromotion = row["strict_nonpromotion"]
    for key in ZERO_FIELDS:
        require(type(nonpromotion[key]) is int and nonpromotion[key] == 0, "zero:"+key)
    for key in ("old_global_universe_count_pinned","old_obligation_census_824864_pinned","corrected_global_schema_sealed"):
        require(type(nonpromotion[key]) is bool and nonpromotion[key] is False, "false:"+key)
    require(nonpromotion["D02"] == "BLOCKED" and nonpromotion["D03"] == "NOT_REACHED" and nonpromotion["D04"] == "NOT_MINTED" and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM", "global statuses")
    body = {"canonical_input_commitment":commitment,"local_theorem":theorem,"local_conclusion":conclusion,"strict_nonpromotion":nonpromotion}
    require(object_hash(body) == row["conclusion_sha256"] and row["theorem_row_id"] == "round306b1af4k2r2w2-local-reglue:"+row["conclusion_sha256"], "input-bound conclusion")
    parent_mutation=json.loads(json.dumps(theorem["predicate_domain_on_parent"]))
    parent_mutation["label"]="MUTATED_PARENT_DOMAIN"
    face_mutation=json.loads(json.dumps(theorem["complete_artificial_face"]["interval_receipt"]))
    face_mutation["outgoing_factor_interval"]["upper"]["numerator"] += 1
    require(not same_typed(parent_mutation,theorem["predicate_domain_on_parent"]) and not same_typed(face_mutation,theorem["complete_artificial_face"]["interval_receipt"]),"receipt mutation attacks")
    return {"member_id":row["member_id"],"parent":parent,"children":[first,second],"face_area":area,"two_corridor_volume":2*volume,"input_rows":commitment["input_rows"],"chart":commitment["source_chart"],"owner":commitment["owner_target"],"conclusion_sha256":row["conclusion_sha256"],"receipt_mutations_rejected":2}


def verify_upstream(snapshot: HeldInputs, rows: list[dict[str,Any]], summaries: list[dict[str,Any]], result: dict[str,Any]) -> None:
    old_doc = parse_json(snapshot.bytes("OLD_R2W_LEDGER"),"old ledger",100_000)
    require(old_doc["row_count"] == 4 and object_hash(old_doc["rows"]) == old_doc["rows_sha256"], "old ledger closure")
    old_by_member: dict[str,Any] = {}
    for old in old_doc["rows"]:
        closed(old,"old")
        require(old["status"] == "BLOCKED_MISSING_AUTHORITY" and type(old["r2_artificial_face_reglue_credit"]) is int and old["r2_artificial_face_reglue_credit"] == 0, "old blocked row")
        require(type(old["physical_support_equivalence_verified"]) is bool and old["physical_support_equivalence_verified"] is False,"old physical-equivalence gap")
        old_by_member[old["member_id"]] = old
    require(set(old_by_member) == {row["member_id"] for row in rows}, "old/candidate members")
    occurrences = {old["occurrence_id"] for old in old_by_member.values()}
    leaves = {old["parent_leaf_id"] for old in old_by_member.values()}
    children = {value for old in old_by_member.values() for value in old["ordered_children"]}
    members = set(old_by_member)
    receipts: list[dict[str,Any]] = []
    receipt, occurrence_rows = scan(snapshot,"R182_ROWS","R182.occurrence",'"collar_occurrence_rows"',lambda row:type(row) is list and len(row)==len(OCCURRENCE_COLUMNS) and row[1] in occurrences)
    receipts.append(receipt)
    receipt, leaf_rows = scan(snapshot,"R182_ROWS","R182.leaf",'"collar_leaf_rows"',lambda row:type(row) is list and len(row)==len(LEAF_COLUMNS) and row[0] in leaves)
    receipts.append(receipt)
    receipt, child_rows = scan(snapshot,"R271_CERT","R271.side",'"rows":[',lambda row:type(row) is dict and row.get("signed_region_row_id") in children,anchor='"formal_side_signature_ledger":{',rows_closed=True)
    receipts.append(receipt)
    receipt, cell_rows = scan(snapshot,"B1R0_CELL","B1R0.cell",'"predicate_source_cell_rows":[',lambda row:type(row) is dict and row.get("formal_member_id") in members,rows_closed=True)
    receipts.append(receipt)
    receipt, member_rows = scan(snapshot,"B1R0_MEMBER","B1R0.member",'"member_union_rows":[',lambda row:type(row) is dict and row.get("member_id") in members,rows_closed=True)
    receipts.append(receipt)
    exact(result["ordered_table_commitments"],receipts,"independent ordered commitments")
    occurrence_map = {row[1]:row for row in occurrence_rows}
    leaf_map = {row[0]:row for row in leaf_rows}
    child_map = {row["signed_region_row_id"]:row for row in child_rows}
    cells_by_member: dict[str,list[dict[str,Any]]] = {member:[] for member in members}
    for cell in cell_rows: cells_by_member[cell["formal_member_id"]].append(cell)
    member_map = {row["member_id"]:row for row in member_rows}
    require(len(occurrence_map)==len(leaf_map)==len(member_map)==4 and len(child_map)==len(cell_rows)==8, "selected source census")
    for row, summary in zip(rows,summaries,strict=True):
        old = old_by_member[row["member_id"]]
        inp = summary["input_rows"]
        require(inp["old_blocked_theorem_row_id"]==old["theorem_row_id"] and inp["old_blocked_theorem_row_sha256"]==old["row_sha256"], "old input binding")
        require(summary["chart"]==old["source_chart"] and summary["owner"]==old["owner_target"] and list(old["parent_box"])==[str(q) for q in summary["parent"]], "old geometry binding")
        occurrence_packed=occurrence_map[old["occurrence_id"]]
        leaf_packed=leaf_map[old["parent_leaf_id"]]
        occurrence=dict(zip(OCCURRENCE_COLUMNS,occurrence_packed,strict=True))
        leaf=dict(zip(LEAF_COLUMNS,leaf_packed,strict=True))
        require(inp["R182_occurrence_row_commitment_sha256"]==object_hash(occurrence_packed), "R182 occurrence commitment")
        require(inp["R182_leaf_row_commitment_sha256"]==object_hash(leaf_packed), "R182 leaf commitment")
        require(occurrence["Round179_occurrence_row_id"]==old["occurrence_id"] and occurrence["chart"]==old["source_chart"] and occurrence["owner_target"]==old["owner_target"],"R182 occurrence identity/chart/owner")
        require(occurrence["kind"]=="OUTGOING" and occurrence["equation"]=="target_normal_x^2-target_normal_y^2=0" and occurrence["target_obstacle"]=="W","R182 occurrence physical semantics")
        require(leaf["occurrence_row_id"]==old["occurrence_id"] and leaf["box"]==old["parent_box"] and leaf["graph_classification"]=="CLIPPED_2D_BOUNDARY_1D","R182 leaf semantics")
        source_children=sorted((child_map[value] for value in old["ordered_children"]),key=lambda child:child["t_child"])
        require([child["t_child"] for child in source_children]==[0,1],"R271 t children")
        child_boxes=[box_text(child["t_child_box"],"R271 child box") for child in source_children]
        parent=summary["parent"]
        midpoint=child_boxes[0][1]
        require(child_boxes[0][0]==parent[0] and child_boxes[1][1]==parent[1] and midpoint==child_boxes[1][0]==(parent[0]+parent[1])/2,"R271 exact t partition")
        require(child_boxes[0][2:]==child_boxes[1][2:]==parent[2:],"R271 complete base")
        require(child_boxes==summary["children"],"R271/theorem owned-box identity")
        require({child["graph_classification"] for child in source_children}=={"EMPTY","CLIPPED_2D_BOUNDARY_1D"},"R271 graph classes")
        signatures=[child["local_return_signature"] for child in source_children]
        require(same_typed(signatures[0],signatures[1]),"R271 complete signature equality")
        require(all(child["owner_target"]==old["owner_target"] and child["region_product_sign"]=="STRICT_NEGATIVE" for child in source_children),"R271 owner/sign")
        require(all(child["complete_10_field_return_signature_sha256"]==object_hash(signatures[0]) for child in source_children),"R271 signature digest")
        require(inp["R271_child_row_ids"]==[child["signed_region_row_id"] for child in source_children] and inp["R271_child_row_sha256"]==[child["row_sha256"] for child in source_children], "R271 children binding")
        cells = sorted(cells_by_member[row["member_id"]],key=lambda cell:cell["predicate_source_inventory"]["t_child"])
        require(inp["B1R0_cell_row_ids"]==[cell["Round306B1R0_predicate_source_cell_row_id"] for cell in cells] and inp["B1R0_cell_row_sha256"]==[cell["row_sha256"] for cell in cells], "B1R0 cell binding")
        require([cell["outer_carrier_box"] for cell in cells]==[child["t_child_box"] for child in source_children],"B1R0/R271 child boxes")
        for index,cell in enumerate(cells):
            require(cell["source_signature_row_id"]==source_children[index]["signed_region_row_id"],"B1R0 source signature")
            require(type(cell["source_free_interval_predicate_ast_materialized"]) is bool and cell["source_free_interval_predicate_ast_materialized"] is False,"B1R0 source-free gap")
            require(type(cell["outer_carrier_box_claimed_as_full_support"]) is bool and cell["outer_carrier_box_claimed_as_full_support"] is False,"B1R0 carrier disclaimer")
            exact(cell["predicate_source_inventory"],{"predicate_family":"OUTGOING_W_TAIL_CHILD_FACTOR_CELL","region_product_sign":"STRICT_NEGATIVE","t_child":index},"B1R0 predicate inventory")
        member = member_map[row["member_id"]]
        require(inp["B1R0_member_row_id"]==member["Round306B1R0_member_union_row_id"] and inp["B1R0_member_row_sha256"]==member["row_sha256"], "B1R0 member binding")
        normalization=member["Round271_W_tail_parent_normalization"]
        require(member["full_support_union_theorem_status"]=="PENDING_SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE","B1R0 pending status")
        require(type(normalization["interface_is_not_a_physical_support_boundary"]) is bool and normalization["interface_is_not_a_physical_support_boundary"] is True,"B1R0 artificial interface")
        require(normalization["normalized_parent_box"]==old["parent_box"],"B1R0 normalized parent")
        require(type(normalization["artificial_interface"]["value"]) is str and Q(normalization["artificial_interface"]["value"])==midpoint,"B1R0 midpoint")
        normalized_children=normalization["source_children"]
        require(type(normalized_children) is list and len(normalized_children)==2 and all(type(value) is str for value in normalized_children),"B1R0 source children grammar")
        require(sorted(normalized_children,key=lambda value:value.encode("ascii"))==sorted(old["ordered_children"],key=lambda value:value.encode("ascii")),"B1R0 source children exact multiplicity")


def replay(snapshot: HeldInputs, candidate: dict[str,Any]) -> dict[str,Any]:
    temp_root = Path(tempfile.mkdtemp(prefix="cm2-k2r2w2-independent-",dir="/tmp")).resolve(strict=True)
    deliverables = snapshot.root
    require(temp_root != deliverables and deliverables not in temp_root.parents and temp_root not in deliverables.parents, "temporary boundary")
    source = temp_root / PRODUCER
    try:
        with source.open("xb") as stream:
            stream.write(snapshot.bytes("PRODUCER"))
            stream.flush(); os.fsync(stream.fileno())
        require(source.stat().st_nlink==1 and hashlib.sha256(source.read_bytes()).hexdigest()==PIN["PRODUCER"][3], "producer snapshot")
        # This is a shared deliverables directory: unrelated theorem workers may
        # legitimately publish concurrently.  Track this package namespace;
        # every pinned input is separately held and final-path revalidated.
        before = {(p.name,p.stat().st_size,p.stat().st_mtime_ns) for p in deliverables.iterdir() if p.is_file() and p.name.startswith(PREFIX)}
        outputs: list[bytes] = []
        stderr_hashes: list[str] = []
        processes: list[tuple[subprocess.Popen[bytes],Path]] = []
        for index,seed in enumerate(("independent-seed-A-0123456789abcdef","independent-seed-B-fedcba9876543210")):
            env={"PATH":"/usr/bin:/bin","LANG":"C","LC_ALL":"C","TZ":"UTC","TMPDIR":str(deliverables)}
            trace_path=temp_root/f"seed-{index}.file-syscalls.log"
            command=["/usr/bin/strace","-f","-qq","-yy","-s","4096","-e","trace=open,openat,openat2,creat,rename,renameat,renameat2,unlink,unlinkat,mkdir,mkdirat,rmdir,link,linkat,symlink,symlinkat,truncate","-o",str(trace_path),sys.executable,"-I","-B","-S",str(source),"--full-replay","--seed",seed,"--input-dir",str(deliverables)]
            run=subprocess.Popen(command,cwd=temp_root,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            processes.append((run,trace_path))
        for run,trace_path in processes:
            stdout,stderr=run.communicate(timeout=900)
            require(run.returncode==0 and len(stdout)<=ROW_LIMIT and b"\x00" not in stdout, "producer cold replay")
            parse_json(stdout,"producer stdout")
            trace=trace_path.read_text("utf-8")
            forbidden=("O_WRONLY","O_RDWR","O_CREAT","O_TRUNC","creat(","rename(","renameat(","renameat2(","unlink(","unlinkat(","mkdir(","mkdirat(","rmdir(","link(","linkat(","symlink(","symlinkat(","truncate(")
            require(not any(str(deliverables) in line and any(token in line for token in forbidden) for line in trace.splitlines()),"strace deliverables write syscall")
            outputs.append(stdout)
            stderr_hashes.append(hashlib.sha256(stderr).hexdigest())
        require(outputs[0]==outputs[1], "dual-seed byte identity")
        bundle=parse_json(outputs[0],"replayed bundle")
        exact(bundle,candidate,"replayed candidate equality")
        after = {(p.name,p.stat().st_size,p.stat().st_mtime_ns) for p in deliverables.iterdir() if p.is_file() and p.name.startswith(PREFIX)}
        require(before==after,"no-write/TMPDIR mutation")
        return {"two_seed_outputs_byte_identical":True,"replayed_bundle_sha256":hashlib.sha256(outputs[0]).hexdigest(),"seed_output_sha256":[hashlib.sha256(value).hexdigest() for value in outputs],"stderr_sha256":stderr_hashes,"nondeterministic_timing_excluded_from_sealed_receipt":True,"producer_executed_only_for_cold_replay":True,"producer_imported":False,"K1_imported":False,"producer_runtime":{"launcher_flags":["-I","-B","-S"],"isolated":True,"dont_write_bytecode":True,"no_site":True,"python_environment_neutralized":True},"explicit_tmp_root":"/tmp","TMPDIR_inside_deliverables_attack_rejected":True,"strace_deliverables_write_create_rename_unlink_truncate_syscalls":0,"R2W2_namespace_unchanged":True,"entire_deliverables_unchanged_claimed":False}
    finally:
        shutil.rmtree(temp_root)


def verify(snapshot: HeldInputs) -> dict[str,Any]:
    result_doc=parse_json(snapshot.bytes("RESULT"),"result")
    ledger=parse_json(snapshot.bytes("LEDGER"),"ledger")
    attack=parse_json(snapshot.bytes("ATTACK"),"attack")
    result=result_doc["result"]
    require(result_doc["schema"]==SCHEMA+".result.v1" and object_hash(result)==result_doc["result_sha256"], "result closure")
    require(result["status"]=="CANDIDATE_4_LOCAL_R2_WTAIL_ARTIFICIAL_FACE_REGLUE_THEOREMS__PENDING_SEALED_INDEPENDENT_VERIFICATION__ZERO_NORMALIZED_OR_GLOBAL_CREDIT" and result["seed_affects_output"] is False, "conditional result status")
    exact(result["runtime_isolation"],{"sys_flags_isolated":1,"sys_flags_dont_write_bytecode":1,"sys_flags_no_site":1,"sys_dont_write_bytecode":True,"required_launcher":"python3 -I -B -S"},"producer runtime isolation")
    require(ledger["schema"]==SCHEMA+".theorem-ledger.v1" and ledger["row_count"]==4 and object_hash(ledger["rows"])==ledger["rows_sha256"], "ledger closure")
    require(object_hash([row["row_sha256"] for row in ledger["rows"]])==ledger["row_hashes_sha256"] and object_hash([row["conclusion_sha256"] for row in ledger["rows"]])==ledger["conclusion_hashes_sha256"], "ledger hash lists")
    exact(result["producer_source_commitment"],{"filename":PRODUCER,"exact_size":PIN["PRODUCER"][2],"sha256":PIN["PRODUCER"][3],"two_pass_held_fd":True},"result producer")
    require(result["theorem_ledger"]["file_sha256"]==PIN["LEDGER"][3] and result["theorem_ledger"]["exact_size"]==PIN["LEDGER"][2] and result["theorem_ledger"]["rows_sha256"]==ledger["rows_sha256"], "result/ledger binding")
    attack_body=dict(attack); attack_digest=attack_body.pop("attack_suite_sha256")
    require(attack["all_passed"] is True and attack["test_count"]==7 and object_hash(attack_body)==attack_digest, "attack closure")
    require(type(attack["tests"]) is list and len(attack["tests"])==7 and all(type(test.get("rejected_or_invariant_passed")) is bool and test["rejected_or_invariant_passed"] is True for test in attack["tests"]),"attack outcomes")
    frozen=result["frozen_input_pins"]
    require(type(frozen) is list and len(frozen)==16,"result frozen pin census")
    for claimed,expected in zip(frozen,PINS[:16],strict=True):
        label,name,size,digest=expected
        require(claimed["label"]==label and claimed["filename"]==name and claimed["exact_size"]==size and claimed["sha256"]==digest and type(claimed["two_pass_held_fd"]) is bool and claimed["two_pass_held_fd"] is True,"result frozen pin:"+label)
    scope=result["authority_scope"]
    require(scope["positive_authority"]=="4_INPUT_BOUND_LOCAL_ARTIFICIAL_FACE_REGLUE_THEOREM_CANDIDATES_CONDITIONAL_ON_MANIFEST_PINNED_PASS_VERIFICATION" and type(scope["independent_verifier_receipt_discharged_inside_producer"]) is bool and scope["independent_verifier_receipt_discharged_inside_producer"] is False,"conditional authority scope")
    for key in ("K1_is_zero_credit_cross_checker_only","local_full_support_set_equality_is_not_global_normalized_support","outer_carrier_box_alone_is_not_full_support","no_credit_from_graph_label_or_signature_equality_alone"):
        require(type(scope[key]) is bool and scope[key] is True,"authority scope:"+key)
    producer_receipt=result["producer_source_commitment"]
    summaries=[validate_row(row,producer_receipt) for row in ledger["rows"]]
    require(len({summary["member_id"] for summary in summaries})==4 and len({summary["conclusion_sha256"] for summary in summaries})==4, "four distinct rows")
    require(sum((summary["face_area"] for summary in summaries),Q(0))==Q(1,51200) and sum((summary["two_corridor_volume"] for summary in summaries),Q(0))==Q(177,26214400000), "aggregate exact geometry")
    census=result["census"]
    expected_census={"old_blocked_rows":4,"local_theorem_rows":4,"local_full_support_set_equalities":4,"complete_artificial_faces":4,"strict_negative_complete_faces":4,"strict_negative_inward_corridors":8,"canonical_half_open_interface_owners":4,"candidate_r2_artificial_face_reglue_credit":4,"r2_artificial_face_reglue_credit_before_package_seal":0}
    exact(census,expected_census,"result census")
    exact(result["exact_geometry"],{"complete_face_area_sum":"1/51200","inward_corridor_volume_sum":"177/26214400000","corridor_relative_denominator":8},"result exact geometry")
    for key in ZERO_FIELDS:
        require(type(result["strict_nonpromotion"][key]) is int and result["strict_nonpromotion"][key]==0,"result zero:"+key)
    for key in ("old_global_universe_count_pinned","old_obligation_census_824864_pinned","corrected_global_schema_sealed"):
        require(result["authority_scope"][key] is False and result["strict_nonpromotion"][key] is False,"result false:"+key)
    require(result["strict_nonpromotion"]["D02"]=="BLOCKED" and result["strict_nonpromotion"]["D03"]=="NOT_REACHED" and result["strict_nonpromotion"]["D04"]=="NOT_MINTED" and result["strict_nonpromotion"]["CM2"]=="NO-GO_FOR_CLAIM","result global statuses")
    verify_upstream(snapshot,ledger["rows"],summaries,result)
    candidate={"schema":SCHEMA+".candidate-bundle.v1","result_document":result_doc,"theorem_ledger":ledger,"attack_suite":attack}
    replay_receipt=replay(snapshot,candidate)
    snapshot.final()
    return {"schema":SCHEMA+".verification.v1","status":STATUS,"verifier_runtime":{"launcher_flags":["-I","-B","-S"],"sys_flags_isolated":1,"sys_flags_dont_write_bytecode":1,"sys_flags_no_site":1,"sys_dont_write_bytecode":True},"held_fd_two_pass_and_final_path_pins":len(PINS),"ordered_table_commitments_recomputed":5,"selected_authority_rows_recomputed":{"old_blocked":4,"R182_occurrence":4,"R182_leaf":4,"R271_child":8,"B1R0_cell":8,"B1R0_member":4},"independent_physical_checks":{"source_free_AST_reconstructed":4,"parent_predicate_domains_strict":4,"canonical_half_open_partitions":4,"complete_artificial_faces":4,"strict_negative_inward_corridors":8,"stored_interval_receipts_exactly_recomputed":16,"interval_receipt_wire_precision_bits":128,"independent_interval_precision_bits":SQRT_BITS,"receipt_mutation_attacks_rejected":sum(summary["receipt_mutations_rejected"] for summary in summaries)},"independent_source_semantics":{"R182_occurrence_and_leaf":4,"R271_child_pairs":4,"B1R0_cell_pairs":4,"B1R0_member_normalizations":4},"credit":{"r2_artificial_face_reglue":4,"normalized_support":0,"representation_cover":0,"B1A":0,"B2":0,"CM2":"NO-GO_FOR_CLAIM"},"global_schema":{"old_global_universe_count_pinned":False,"old_obligation_census_824864_pinned":False,"corrected_global_schema_sealed":False},"replay":replay_receipt,"result_sha256":PIN["RESULT"][3],"theorem_ledger_sha256":PIN["LEDGER"][3],"attack_suite_sha256":PIN["ATTACK"][3],"verifier_imported_producer_or_K1":False}


def atomic_write(directory: Path, name: str, payload: bytes) -> None:
    require(directory.resolve(strict=True)==HERE and name==os.path.basename(name),"write boundary")
    target=directory/name
    if target.exists() or target.is_symlink():
        named=os.stat(target,follow_symlinks=False)
        require(stat.S_ISREG(named.st_mode) and named.st_nlink==1 and named.st_size==len(payload),"existing output identity")
        existing=os.open(target,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0)|getattr(os,"O_CLOEXEC",0))
        try:
            require(file_identity(named)==file_identity(os.fstat(existing)) and fd_hash(existing)==hashlib.sha256(payload).hexdigest(),"existing output idempotent-exact")
        finally:
            os.close(existing)
        return
    fd,temp_name=tempfile.mkstemp(prefix="."+name+".",suffix=".tmp",dir=directory)
    temp=Path(temp_name)
    try:
        with os.fdopen(fd,"wb") as stream:
            stream.write(payload); stream.flush(); os.fsync(stream.fileno())
        try:
            os.link(temp,target,follow_symlinks=False)
        except FileExistsError:
            named=os.stat(target,follow_symlinks=False)
            require(stat.S_ISREG(named.st_mode) and named.st_nlink==1 and named.st_size==len(payload),"concurrent output identity")
            existing=os.open(target,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0)|getattr(os,"O_CLOEXEC",0))
            try:
                require(fd_hash(existing)==hashlib.sha256(payload).hexdigest(),"concurrent output idempotent-exact")
            finally:
                os.close(existing)
        else:
            temp.unlink(); temp=Path("")
            published=os.stat(target,follow_symlinks=False)
            require(stat.S_ISREG(published.st_mode) and published.st_nlink==1 and published.st_size==len(payload),"published output identity")
        dirfd=os.open(directory,os.O_RDONLY|getattr(os,"O_DIRECTORY",0))
        try: os.fsync(dirfd)
        finally: os.close(dirfd)
    finally:
        if temp!=Path("") and temp.exists(): temp.unlink()


def self_test() -> dict[str,Any]:
    first=expected_asts("G:E","W[1,-1]")
    second=expected_asts("G:W","W[1,-1]")
    require(object_hash(first)!=object_hash(second),"AST chart binding")
    rejected=0
    for raw in (b'{"x":1,"x":2}',b'{"x":false}',b'{"x":1.5}'):
        try:
            value=parse_json(raw,"attack",100)
            require(not (type(value.get("x")) is bool and value["x"]==0),"bool/int alias")
        except Reject:
            rejected+=1
    require(rejected==3,"self-test attacks")
    return {"status":"PASS","independent_AST":True,"bool_int_and_parser_attacks_rejected":3,"formal_credit":0}


def main() -> int:
    require(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1 and sys.flags.no_site==1 and sys.dont_write_bytecode is True,"verifier requires isolated no-site no-bytecode runtime: python3 -I -B -S")
    parser=argparse.ArgumentParser()
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--print-contract",action="store_true")
    modes.add_argument("--self-test",action="store_true")
    modes.add_argument("--verify",action="store_true")
    parser.add_argument("--input-dir",type=Path,default=HERE)
    parser.add_argument("--write",action="store_true")
    parser.add_argument("--output-dir",type=Path,default=HERE)
    args=parser.parse_args()
    if args.print_contract:
        output:Any={"schema":SCHEMA,"status":STATUS,"producer_imported":False,"K1_imported":False,"writes_only_with_explicit_flag":True,"post_success_row_cap":ROW_LIMIT,"required_launcher":"python3 -I -B -S"}
    elif args.self_test:
        output=self_test()
    else:
        with HeldInputs(args.input_dir) as snapshot:
            output=verify(snapshot)
        if args.write:
            atomic_write(args.output_dir,VERIFICATION,canon(output)+b"\n")
    sys.stdout.buffer.write(canon(output)+b"\n")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
