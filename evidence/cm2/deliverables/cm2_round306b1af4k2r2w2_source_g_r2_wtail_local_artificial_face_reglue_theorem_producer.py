#!/usr/bin/env python3
"""Produce four input-bound local R2 W-tail artificial-face reglue theorems.

The four Round271 pairs are not treated as closed boxes.  Each row is the
exact predicate set ``box AND (target_normal_x^2-target_normal_y^2 < 0)``.
The producer materializes that source-free predicate AST, proves that the two
canonically half-open child restrictions are a disjoint cover of the parent
restriction, and proves strict negativity on the complete artificial face and
on positive-volume inward corridors on both sides.  This mints exactly four
local reglue credits and no normalized-support or global credit.

K1 is loaded only from held, pinned bytes as a zero-credit cross-checker.  The
positive interval and set-theoretic conclusions are implemented here and are
independently reimplemented by the verifier.
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
import stat
import sys
import tempfile
import types
from typing import Any, BinaryIO, Final, Iterator, Mapping, TextIO


class Blocked(RuntimeError):
    pass


def need(ok: bool, label: str) -> None:
    if not ok:
        raise Blocked(label)


HERE: Final = Path(__file__).resolve().parent
PREFIX: Final = "cm2_round306b1af4k2r2w2_source_g_r2_wtail_local_artificial_face_reglue_theorem_"
RESULT_NAME: Final = PREFIX + "result.json"
LEDGER_NAME: Final = PREFIX + "theorem_ledger.json"
ATTACK_NAME: Final = PREFIX + "attack_suite.json"
SCHEMA: Final = "cm2.round306b1af4k2r2w2.source-g-r2-wtail-local-artificial-face-reglue-theorem.v1"
ROW_SCHEMA: Final = SCHEMA + ".row.v1"
STATUS: Final = "CANDIDATE_4_LOCAL_R2_WTAIL_ARTIFICIAL_FACE_REGLUE_THEOREMS__PENDING_SEALED_INDEPENDENT_VERIFICATION__ZERO_NORMALIZED_OR_GLOBAL_CREDIT"
ROW_CAP: Final = 8 << 20
READ_CHARS: Final = 1 << 18
BUFFER_CAP: Final = ROW_CAP + 4 * READ_CHARS
SQRT_BITS: Final = 128
CORRIDOR_DENOMINATOR: Final = 8
HEX64 = re.compile(r"^[0-9a-f]{64}$")
TARGET = re.compile(r"^W\[(-?[0-9]+),(-?[0-9]+)\]$")


PINS: Final = (
    ("OLD_R2W_MANIFEST", "cm2_round306b1af4k2r2w_source_g_r2_wtail_exact_reglue_manifest.sha256", 1_089, "4abdb77dc106f1cfa4bb582d17fb48dcfc29869786330e9d784f268bb13cefc4", "SEALED_PRIOR_NO_GO_PACKAGE"),
    ("OLD_R2W_RESULT", "cm2_round306b1af4k2r2w_source_g_r2_wtail_exact_reglue_result.json", 25_794, "87e10fcc3a79854a1361e3f4e836c48febb97a69fce47073bd38cf62c28db936", "PRIOR_AUTHORITY_GAP_AUDIT"),
    ("OLD_R2W_LEDGER", "cm2_round306b1af4k2r2w_source_g_r2_wtail_exact_reglue_theorem_ledger.json", 19_662, "12642bc980beea0eaa23c13ceb531e9633e2680ad08847f44208606c26b38aae", "FOUR_BLOCKED_SOURCE_JOINS"),
    ("OLD_R2W_VERIFICATION", "cm2_round306b1af4k2r2w_source_g_r2_wtail_exact_reglue_verification.json", 854, "912ae2fbb45f8aa08aa76bf8599f5ff9f5508dd61941184b01ad0879ba6fd3b0", "PRIOR_INDEPENDENT_RECEIPT"),
    ("R182_ROWS", "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json", 158_815_476, "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c", "PARENT_BOX_AND_OCCURRENCE_AUTHORITY"),
    ("R182_CERT", "cm2_round182_source_g_clipped_graph_and_pair_arrangement_certificate.json", 7_553, "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08", "R182_PHYSICAL_MODEL_BINDING"),
    ("R182_VERIFY", "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json", 4_956, "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36", "R182_INDEPENDENT_RECEIPT"),
    ("R271_CERT", "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json", 112_741_715, "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747", "CHILD_FACTOR_CELL_AND_SIGNATURE_AUTHORITY"),
    ("R271_VERIFIER", "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_verifier.py", 18_627, "a8c5d5a1b055f8f0c7cd5f8fe6e5d598d15b543a5107a6665935944f5500c7e8", "INERT_WTAIL_CONSTRUCTION_SEMANTICS"),
    ("B1R0_CELL", "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz", 105_989_322, "19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96", "CHILD_INVENTORY"),
    ("B1R0_MEMBER", "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz", 123_019_951, "4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7", "PARENT_NORMALIZATION"),
    ("R179_EVALUATOR", "cm2_round179_source_g_residual_tube_arrangement_verifier.py", 78_867, "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679", "INERT_PHYSICAL_FACTOR_REFERENCE"),
    ("FIRST_HIT_ENGINE", "cm2_gate3_candidate_first_hit_cert.py", 13_832, "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2", "INERT_RADIUS_AND_TARGET_CENTER_REFERENCE"),
    ("K1_MANIFEST", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_manifest.sha256", 933, "07a3f12e75c43fd459dfd4e86c918b349c09226c94735b1a6d16432f1caca939", "ZERO_CREDIT_CROSS_CHECKER_SEAL"),
    ("K1_SOURCE", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel.py", 68_346, "17d9c302984e2e29dcf02832f36ec9437c23c8b65c27289a3469db222ce4edae", "ZERO_CREDIT_CROSS_CHECKER"),
    ("K1_RESULT", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_result.json", 2_787, "e9ff89a5d51f5e79864f10dc34dd4b5f12887c029f65c2196c60f50bd4c77b21", "ZERO_CREDIT_CROSS_CHECKER_RECEIPT"),
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


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def type_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(type_equal(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(type_equal(a, b) for a, b in zip(left, right, strict=True))
    return bool(left == right)


def strict(left: Any, right: Any, label: str) -> None:
    need(type_equal(left, right), label)


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(type(key) is str and key not in result, "duplicate/non-string JSON key")
        result[key] = value
    return result


def reject_number(token: str) -> Any:
    raise Blocked("nonintegral/nonfinite number:" + token)


DECODER = json.JSONDecoder(object_pairs_hook=unique_pairs, parse_float=reject_number, parse_constant=reject_number)


def strict_tree(value: Any, depth: int = 0) -> None:
    need(depth <= 256, "JSON depth")
    if value is None or type(value) in {str, bool, int}:
        return
    need(type(value) in {dict, list}, "strict JSON type")
    values = value.values() if type(value) is dict else value
    if type(value) is dict:
        need(all(type(key) is str for key in value), "JSON key type")
    for item in values:
        strict_tree(item, depth + 1)


def decode(raw: bytes, label: str, maximum: int) -> Any:
    need(0 < len(raw) <= maximum and b"\x00" not in raw and not raw.startswith(b"\xef\xbb\xbf"), "raw:" + label)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs, parse_float=reject_number, parse_constant=reject_number)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Blocked("decode:" + label) from exc
    strict_tree(value)
    need(len(canonical(value)) <= maximum, "canonical decoded cap:" + label)
    return value


def check_closed(row: Any, label: str) -> None:
    need(type(row) is dict and type(row.get("row_sha256")) is str, "closed:" + label)
    payload = dict(row)
    claimed = payload.pop("row_sha256")
    need(HEX64.fullmatch(claimed) is not None and sha_object(payload) == claimed, "row digest:" + label)


def qtext(value: Q) -> str:
    return str(value)


def qw(value: Q | int) -> dict[str, int]:
    q = Q(value)
    return {"numerator": q.numerator, "denominator": q.denominator}


def as_q(value: Any, label: str) -> Q:
    need(type(value) is dict and set(value) == {"numerator", "denominator"}, label)
    n, d = value["numerator"], value["denominator"]
    need(type(n) is type(d) is int and d > 0, label)
    q = Q(n, d)
    need(q.numerator == n and q.denominator == d, label)
    return q


def fractions(values: Any, label: str) -> tuple[Q, ...]:
    need(type(values) is list and len(values) == 6 and all(type(x) is str for x in values), label)
    result = tuple(Q(x) for x in values)
    need(all(str(q) == x for q, x in zip(result, values, strict=True)), label)
    return result


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def hash_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    state = hashlib.sha256()
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            os.lseek(fd, 0, os.SEEK_SET)
            return state.hexdigest()
        state.update(block)


class Frozen:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve(strict=True)
        self.dirfd = -1
        self.dirstat: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.stats: dict[str, os.stat_result] = {}
        self.self_fd = -1
        self.self_stat: os.stat_result | None = None
        self.self_receipt: dict[str, Any] = {}

    def __enter__(self) -> "Frozen":
        before = os.stat(self.root, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not self.root.is_symlink(), "input directory")
        self.dirfd = os.open(self.root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dirstat = os.fstat(self.dirfd)
        need((before.st_dev, before.st_ino, before.st_mode) == (self.dirstat.st_dev, self.dirstat.st_ino, self.dirstat.st_mode), "directory race")
        try:
            for label, name, size, expected, _role in PINS:
                named = os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(named.st_mode) and named.st_nlink == 1 and named.st_size == size, "pin identity:" + label)
                fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(identity(named) == identity(opened), "pin open race:" + label)
                need(hash_fd(fd) == hash_fd(fd) == expected, "pin two-pass:" + label)
                need(identity(opened) == identity(os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)), "pin rebound:" + label)
                self.fds[label], self.stats[label] = fd, opened
            named = os.stat(__file__, follow_symlinks=False)
            need(stat.S_ISREG(named.st_mode) and named.st_nlink == 1, "producer source identity")
            self.self_fd = os.open(__file__, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
            self.self_stat = os.fstat(self.self_fd)
            need(identity(named) == identity(self.self_stat), "producer source race")
            first, second = hash_fd(self.self_fd), hash_fd(self.self_fd)
            need(first == second, "producer source two-pass")
            self.self_receipt = {"filename": Path(__file__).name, "exact_size": self.self_stat.st_size, "sha256": first, "two_pass_held_fd": True}
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def raw(self, label: str) -> bytes:
        fd = self.fds[label]
        os.lseek(fd, 0, os.SEEK_SET)
        parts: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                os.lseek(fd, 0, os.SEEK_SET)
                return b"".join(parts)
            parts.append(block)

    def stream(self, label: str, marker: str, anchor: str | None = None) -> Iterator[Any]:
        fd = self.fds[label]
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.fdopen(os.dup(fd), "rb")
        binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if PIN[label][1].endswith(".gz") else raw
        text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
        try:
            yield from iter_array(text, marker, anchor)
        finally:
            text.close()
            if not raw.closed:
                raw.close()
            os.lseek(fd, 0, os.SEEK_SET)
            need(identity(os.fstat(fd)) == identity(self.stats[label]), "parse FD identity:" + label)

    def load_k1(self) -> types.ModuleType:
        source = self.raw("K1_SOURCE")
        module = types.ModuleType("_sealed_k1_r2w2_cross_checker")
        module.__file__ = str(self.root / PIN["K1_SOURCE"][1])
        module.__package__ = ""
        old = sys.modules.get(module.__name__)
        sys.modules[module.__name__] = module
        try:
            exec(compile(source, module.__file__, "exec"), module.__dict__)
        finally:
            if old is None:
                sys.modules.pop(module.__name__, None)
            else:
                sys.modules[module.__name__] = old
        return module

    def final(self) -> None:
        need(self.dirstat is not None and self.self_stat is not None, "active snapshot")
        now = os.stat(self.root, follow_symlinks=False)
        need((now.st_dev, now.st_ino, now.st_mode) == (self.dirstat.st_dev, self.dirstat.st_ino, self.dirstat.st_mode), "final directory")
        for label, name, size, expected, _role in PINS:
            held = os.fstat(self.fds[label])
            path = os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
            need(identity(held) == identity(path) == identity(self.stats[label]) and held.st_nlink == 1 and held.st_size == size, "final path:" + label)
            need(hash_fd(self.fds[label]) == expected, "final hash:" + label)
        path = os.stat(__file__, follow_symlinks=False)
        need(identity(os.fstat(self.self_fd)) == identity(path) == identity(self.self_stat), "final producer path")
        need(hash_fd(self.self_fd) == self.self_receipt["sha256"], "final producer hash")

    def __exit__(self, *_args: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        self.fds.clear()
        if self.self_fd >= 0:
            os.close(self.self_fd)
            self.self_fd = -1
        if self.dirfd >= 0:
            os.close(self.dirfd)
            self.dirfd = -1


def iter_array(stream: TextIO, marker: str, anchor: str | None = None) -> Iterator[Any]:
    def append(buffer: str, label: str) -> str:
        block = stream.read(READ_CHARS)
        need(bool(block), label)
        output = buffer + block
        need(len(output.encode("utf-8")) <= BUFFER_CAP, "parser buffer cap")
        return output

    def seek(token: str, buffer: str) -> str:
        while True:
            position = buffer.find(token)
            if position >= 0:
                return buffer[position + len(token):]
            buffer = append(buffer, "missing marker:" + token)
            position = buffer.find(token)
            if position >= 0:
                return buffer[position + len(token):]
            buffer = buffer[-max(1, len(token) - 1):]

    buffer = ""
    if anchor is not None:
        buffer = seek(anchor, buffer)
    buffer = seek(marker, buffer)
    stripped = buffer.lstrip()
    if stripped.startswith(":"):
        stripped = stripped[1:].lstrip()
        need(stripped.startswith("["), "marker array")
        buffer = stripped[1:]
    comma = False
    while True:
        buffer = buffer.lstrip()
        while not buffer:
            buffer = append(buffer, "truncated array")
            buffer = buffer.lstrip()
        if buffer[0] == "]":
            return
        if comma:
            need(buffer[0] == ",", "missing comma")
            buffer = buffer[1:].lstrip()
            while not buffer:
                buffer = append(buffer, "truncated row")
                buffer = buffer.lstrip()
            need(buffer[0] != "]", "trailing comma")
        else:
            need(buffer[0] != ",", "leading comma")
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                need(len(buffer.encode("utf-8")) <= ROW_CAP, "row predecode cap")
                buffer = append(buffer, "truncated JSON row")
        # Mandatory post-success caps close the old decoded-row-cap hole.
        need(len(buffer[:end].encode("utf-8")) <= ROW_CAP, "decoded row cap")
        strict_tree(value)
        need(len(canonical(value)) <= ROW_CAP, "canonical row cap")
        yield value
        buffer = buffer[end:]
        comma = True


class ListDigest:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        self.state.update(canonical(value))
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def select_table(snapshot: Frozen, pin: str, table: str, marker: str, predicate: Any, *, anchor: str | None = None, closed: bool = False) -> tuple[dict[str, Any], list[Any]]:
    digest = ListDigest()
    selected: list[Any] = []
    for row in snapshot.stream(pin, marker, anchor):
        if closed:
            check_closed(row, table)
        digest.add(row)
        if predicate(row):
            selected.append(row)
    expected_count, expected_sha = TABLES[table]
    observed = digest.finish()
    need(digest.count == expected_count and observed == expected_sha, "table commitment:" + table)
    return {"table": table, "row_count": digest.count, "rows_sha256": observed, "row_sha256_checked": closed}, selected


@dataclass(frozen=True)
class IV:
    lower: Q
    upper: Q

    def __post_init__(self) -> None:
        need(type(self.lower) is Q and type(self.upper) is Q and self.lower <= self.upper, "interval")

    @classmethod
    def point(cls, value: Q) -> "IV":
        return cls(value, value)

    def neg(self) -> "IV":
        return IV(-self.upper, -self.lower)

    def add(self, other: "IV") -> "IV":
        return IV(self.lower + other.lower, self.upper + other.upper)

    def sub(self, other: "IV") -> "IV":
        return self.add(other.neg())

    def mul(self, other: "IV") -> "IV":
        values = (self.lower * other.lower, self.lower * other.upper, self.upper * other.lower, self.upper * other.upper)
        return IV(min(values), max(values))

    def square(self) -> "IV":
        values = (self.lower * self.lower, self.upper * self.upper)
        return IV(Q(0) if self.lower <= 0 <= self.upper else min(values), max(values))

    def div(self, other: "IV") -> "IV":
        need(not other.lower <= 0 <= other.upper, "division by interval containing zero")
        reciprocal = IV(min(Q(1, other.lower), Q(1, other.upper)), max(Q(1, other.lower), Q(1, other.upper)))
        return self.mul(reciprocal)

    def wire(self) -> dict[str, Any]:
        return {"lower": qw(self.lower), "upper": qw(self.upper)}


def sqrt_iv(value: IV) -> IV:
    need(value.lower > 0, "sqrt positive domain")
    scale = 1 << SQRT_BITS
    def floor(q: Q) -> Q:
        return Q(isqrt((q.numerator * scale * scale) // q.denominator), scale)
    lower, upper = floor(value.lower), floor(value.upper)
    if upper * upper != value.upper:
        upper += Q(1, scale)
    need(lower * lower <= value.lower and upper * upper >= value.upper, "outward sqrt")
    return IV(lower, upper)


def c(value: Q | int) -> dict[str, Any]:
    return {"op": "CONST_Q", "value": qw(value)}


def v(name: str) -> dict[str, Any]:
    return {"op": "VAR", "name": name}


def neg(arg: Any) -> dict[str, Any]:
    return {"op": "NEG", "arg": arg}


def add(*args: Any) -> dict[str, Any]:
    return {"op": "ADD", "args": list(args)}


def sub(left: Any, right: Any) -> dict[str, Any]:
    return {"op": "SUB", "left": left, "right": right}


def mul(*args: Any) -> dict[str, Any]:
    return {"op": "MUL", "args": list(args)}


def square(arg: Any) -> dict[str, Any]:
    return {"op": "SQUARE", "arg": arg}


def sqrt_positive(arg: Any) -> dict[str, Any]:
    return {"op": "SQRT_POSITIVE", "arg": arg}


def div_nonzero(left: Any, right: Any) -> dict[str, Any]:
    return {"op": "DIV_NONZERO", "left": left, "right": right}


def eval_ast(node: Any, env: Mapping[str, IV]) -> IV:
    need(type(node) is dict and type(node.get("op")) is str, "AST node")
    op = node["op"]
    if op == "CONST_Q":
        return IV.point(as_q(node["value"], "constant"))
    if op == "VAR":
        need(set(node) == {"op", "name"} and node["name"] in env, "variable")
        return env[node["name"]]
    if op == "NEG":
        return eval_ast(node["arg"], env).neg()
    if op == "ADD":
        values = [eval_ast(item, env) for item in node["args"]]
        need(len(values) >= 2, "add arity")
        result = values[0]
        for item in values[1:]:
            result = result.add(item)
        return result
    if op == "SUB":
        return eval_ast(node["left"], env).sub(eval_ast(node["right"], env))
    if op == "MUL":
        values = [eval_ast(item, env) for item in node["args"]]
        need(len(values) >= 2, "mul arity")
        result = values[0]
        for item in values[1:]:
            result = result.mul(item)
        return result
    if op == "SQUARE":
        return eval_ast(node["arg"], env).square()
    if op == "SQRT_POSITIVE":
        return sqrt_iv(eval_ast(node["arg"], env))
    if op == "DIV_NONZERO":
        return eval_ast(node["left"], env).div(eval_ast(node["right"], env))
    raise Blocked("unsupported scalar AST:" + op)


def physical_asts(chart: str, owner: str) -> dict[str, Any]:
    match = TARGET.fullmatch(owner)
    need(chart in {"G:E", "G:W"} and match is not None, "supported W-tail chart/target")
    ix, iy = int(match.group(1)), int(match.group(2))
    t, p, s = v("t"), v("p"), v("s")
    t_rad = sub(c(1), square(t))
    p_rad = sub(c(1), square(p))
    rt, rp = sqrt_positive(t_rad), sqrt_positive(p_rad)
    nx, ny = (rt if chart == "G:E" else neg(rt)), t
    ux = sub(mul(rp, nx), mul(p, ny))
    uy = add(mul(rp, ny), mul(p, nx))
    source_x, source_y = mul(c(Q(9, 25)), nx), mul(c(Q(9, 25)), ny)
    center_x, center_y = add(c(Q(2 * ix + 1, 2)), s), c(Q(2 * iy + 1, 2))
    dx, dy = sub(center_x, source_x), sub(center_y, source_y)
    transverse = add(neg(mul(uy, dx)), mul(ux, dy))
    discriminant = sub(c(Q(16, 625)), square(transverse))
    radical = sqrt_positive(discriminant)
    normal_x = div_nonzero(add(neg(mul(radical, ux)), mul(transverse, uy)), c(Q(4, 25)))
    normal_y = div_nonzero(sub(neg(mul(radical, uy)), mul(transverse, ux)), c(Q(4, 25)))
    factor = sub(square(normal_x), square(normal_y))
    return {
        "source_t_radical_argument_ast": t_rad,
        "direction_p_radical_argument_ast": p_rad,
        "selected_root_discriminant_ast": discriminant,
        "target_normal_x_ast": normal_x,
        "target_normal_y_ast": normal_y,
        "outgoing_factor_ast": factor,
        "strict_negative_predicate_ast": {"op": "LT_ZERO", "arg": factor},
    }


def environment(box: tuple[Q, ...]) -> dict[str, IV]:
    return {"t": IV(box[0], box[1]), "p": IV(box[2], box[3]), "s": IV(box[4], box[5])}


def box_wire(box: tuple[Q, ...], t_closed: tuple[bool, bool]) -> dict[str, Any]:
    flags = (t_closed, (True, True), (True, True))
    axes = []
    for name, lo, hi, (lc, uc) in zip(("t", "p", "s"), box[::2], box[1::2], flags, strict=True):
        axes.append({"axis": name, "lower": qw(lo), "lower_closed": lc, "upper": qw(hi), "upper_closed": uc})
    return {"wire_id": "RATIONAL_INTERVAL_BOX_V1", "coordinate_parameter": "TPS", "axes": axes}


def box_partition_atoms(parent: tuple[Q, ...], children: list[tuple[tuple[Q, ...], tuple[bool, bool]]]) -> int:
    ends = sorted({parent[0], parent[1], *(child[0][0] for child in children), *(child[0][1] for child in children)})
    atoms: list[tuple[str, Q, Q | None]] = []
    for index, point in enumerate(ends):
        atoms.append(("POINT", point, None))
        if index + 1 < len(ends):
            atoms.append(("OPEN", point, ends[index + 1]))
    def owns(child: tuple[tuple[Q, ...], tuple[bool, bool]], atom: tuple[str, Q, Q | None]) -> bool:
        box, flags = child
        kind, lo, hi = atom
        if kind == "OPEN":
            assert hi is not None
            return box[0] <= lo and hi <= box[1]
        return (box[0] < lo or (box[0] == lo and flags[0])) and (lo < box[1] or (lo == box[1] and flags[1]))
    count = 0
    for atom in atoms:
        lo, hi = atom[1], atom[2]
        inside = parent[0] <= lo <= parent[1] if hi is None else parent[0] <= lo < hi <= parent[1]
        if not inside:
            continue
        need(sum(owns(child, atom) for child in children) == 1, "half-open partition atom")
        count += 1
    need(count == 5, "canonical t atom census")
    return count


def interval_receipt(asts: dict[str, Any], box: tuple[Q, ...], label: str) -> dict[str, Any]:
    env = environment(box)
    t_domain = eval_ast(asts["source_t_radical_argument_ast"], env)
    p_domain = eval_ast(asts["direction_p_radical_argument_ast"], env)
    discriminant = eval_ast(asts["selected_root_discriminant_ast"], env)
    factor = eval_ast(asts["outgoing_factor_ast"], env)
    need(t_domain.lower > 0 and p_domain.lower > 0 and discriminant.lower > 0, "positive AST domains:" + label)
    return {"label": label, "box": [qtext(x) for x in box], "source_t_radical_argument_interval": t_domain.wire(), "direction_p_radical_argument_interval": p_domain.wire(), "selected_root_discriminant_interval": discriminant.wire(), "outgoing_factor_interval": factor.wire(), "outgoing_factor_strict_negative": factor.upper < 0}


def close(row: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in row, "unclosed row")
    row["row_sha256"] = sha_object(row)
    need(len(canonical(row)) <= ROW_CAP, "final row cap")
    return row


def validate_manifest(raw: bytes) -> None:
    text = raw.decode("ascii")
    rows = [line for line in text.splitlines() if line]
    need(len(rows) == 8 and all(re.fullmatch(r"[0-9a-f]{64}  [A-Za-z0-9_.-]+", row) for row in rows), "old manifest grammar")
    need(any(row == PIN["OLD_R2W_LEDGER"][3] + "  " + PIN["OLD_R2W_LEDGER"][1] for row in rows), "old ledger manifest binding")


def load_old(snapshot: Frozen) -> list[dict[str, Any]]:
    validate_manifest(snapshot.raw("OLD_R2W_MANIFEST"))
    ledger = decode(snapshot.raw("OLD_R2W_LEDGER"), "old ledger", 100_000)
    need(type(ledger) is dict and ledger["row_count"] == 4 and ledger["rows_sha256"] == sha_object(ledger["rows"]), "old ledger closure")
    need(ledger["row_hashes_sha256"] == sha_object([row["row_sha256"] for row in ledger["rows"]]), "old row-hash list")
    for row in ledger["rows"]:
        check_closed(row, "old R2W")
        strict(row["status"], "BLOCKED_MISSING_AUTHORITY", "old status")
        strict(row["r2_artificial_face_reglue_credit"], 0, "old zero credit")
        strict(row["physical_support_equivalence_verified"], False, "old support gap")
    result = decode(snapshot.raw("OLD_R2W_RESULT"), "old result", 100_000)
    need(result["result"]["theorem_ledger"]["rows_sha256"] == ledger["rows_sha256"], "old result/ledger")
    # The sealed prior receipt predates the integer-only output grammar and
    # contains a diagnostic wall-time decimal.  Its complete bytes are already
    # size/SHA pinned above, so bind the required status without normalizing or
    # accepting that legacy decimal into this producer's strict JSON domain.
    verification_raw = snapshot.raw("OLD_R2W_VERIFICATION")
    need(
        b'"status": "PASS_INDEPENDENT_REPLAY__FOUR_BLOCKED_ROWS__ZERO_REGLUE_CREDIT"'
        in verification_raw,
        "old verification status",
    )
    return ledger["rows"]


def build(snapshot: Frozen, seed: str) -> dict[str, Any]:
    need(type(seed) is str and 1 <= len(seed) <= 128, "seed")
    old_rows = load_old(snapshot)
    old_by_member = {row["member_id"]: row for row in old_rows}
    need(len(old_by_member) == 4, "four old members")
    leaf_ids = {row["parent_leaf_id"] for row in old_rows}
    occurrence_ids = {row["occurrence_id"] for row in old_rows}
    child_ids = {child for row in old_rows for child in row["ordered_children"]}
    member_ids = set(old_by_member)
    receipts = []

    receipt, occurrence_packed = select_table(snapshot, "R182_ROWS", "R182.occurrence", '"collar_occurrence_rows"', lambda row: type(row) is list and len(row) == len(OCCURRENCE_COLUMNS) and row[1] in occurrence_ids)
    receipts.append(receipt)
    receipt, leaf_packed = select_table(snapshot, "R182_ROWS", "R182.leaf", '"collar_leaf_rows"', lambda row: type(row) is list and len(row) == len(LEAF_COLUMNS) and row[0] in leaf_ids)
    receipts.append(receipt)
    receipt, children_list = select_table(snapshot, "R271_CERT", "R271.side", '"rows":[', lambda row: type(row) is dict and row.get("signed_region_row_id") in child_ids, anchor='"formal_side_signature_ledger":{', closed=True)
    receipts.append(receipt)
    receipt, cells_list = select_table(snapshot, "B1R0_CELL", "B1R0.cell", '"predicate_source_cell_rows":[', lambda row: type(row) is dict and row.get("formal_member_id") in member_ids, closed=True)
    receipts.append(receipt)
    receipt, members_list = select_table(snapshot, "B1R0_MEMBER", "B1R0.member", '"member_union_rows":[', lambda row: type(row) is dict and row.get("member_id") in member_ids, closed=True)
    receipts.append(receipt)

    occurrences = {row[1]: dict(zip(OCCURRENCE_COLUMNS, row, strict=True)) for row in occurrence_packed}
    leaves = {row[0]: dict(zip(LEAF_COLUMNS, row, strict=True)) for row in leaf_packed}
    children = {row["signed_region_row_id"]: row for row in children_list}
    members = {row["member_id"]: row for row in members_list}
    cells_by_member: dict[str, list[dict[str, Any]]] = {member: [] for member in member_ids}
    for row in cells_list:
        cells_by_member[row["formal_member_id"]].append(row)
    need(len(occurrences) == len(leaves) == len(members) == 4 and len(children) == len(cells_list) == 8, "selected census")

    k1_result = decode(snapshot.raw("K1_RESULT"), "K1 result", 10_000)
    strict(k1_result["decision"], "GO_ONLY_ZERO_CREDIT", "K1 decision")
    strict(k1_result["formal_credit"], {"B1A":0,"B2":0,"CM2":0,"D02":0,"fibre":0,"global_disposition":0,"maximality":0,"normalized_support":0,"pair_routing":0,"physical_incidence":0,"representation_cover":0,"transition":0}, "K1 credit")
    k1 = snapshot.load_k1()
    rows: list[dict[str, Any]] = []
    total_area = Q(0)
    total_corridor_volume = Q(0)
    k1_digests: set[str] = set()

    for member_id in sorted(member_ids, key=lambda value: value.encode("ascii")):
        old = old_by_member[member_id]
        occurrence = occurrences[old["occurrence_id"]]
        leaf = leaves[old["parent_leaf_id"]]
        source_children = sorted((children[value] for value in old["ordered_children"]), key=lambda row: row["t_child"])
        source_cells = sorted(cells_by_member[member_id], key=lambda row: row["predicate_source_inventory"]["t_child"])
        member = members[member_id]
        need([row["t_child"] for row in source_children] == [0, 1] and len(source_cells) == 2, "two ordered children")
        parent = fractions(old["parent_box"], "parent")
        child_boxes = [fractions(row["t_child_box"], "child") for row in source_children]
        midpoint = child_boxes[0][1]
        need(child_boxes[0][0] == parent[0] and child_boxes[1][1] == parent[1] and midpoint == child_boxes[1][0] == (parent[0] + parent[1]) / 2, "exact t partition")
        need(child_boxes[0][2:] == child_boxes[1][2:] == parent[2:], "complete base")
        need(occurrence["Round179_occurrence_row_id"] == old["occurrence_id"] and occurrence["chart"] == old["source_chart"] and occurrence["owner_target"] == old["owner_target"], "occurrence identity")
        need(occurrence["kind"] == "OUTGOING" and occurrence["equation"] == "target_normal_x^2-target_normal_y^2=0" and occurrence["target_obstacle"] == "W", "occurrence physical factor")
        need(leaf["occurrence_row_id"] == old["occurrence_id"] and leaf["box"] == old["parent_box"] and leaf["graph_classification"] == "CLIPPED_2D_BOUNDARY_1D", "parent leaf")
        need({row["graph_classification"] for row in source_children} == {"EMPTY", "CLIPPED_2D_BOUNDARY_1D"}, "child graph classes")
        signatures = [row["local_return_signature"] for row in source_children]
        need(signatures[0] == signatures[1] and all(row["owner_target"] == old["owner_target"] and row["region_product_sign"] == "STRICT_NEGATIVE" for row in source_children), "same signature/owner/F sign")
        need(all(row["complete_10_field_return_signature_sha256"] == sha_object(signatures[0]) for row in source_children), "signature hash")
        need([row["outer_carrier_box"] for row in source_cells] == [row["t_child_box"] for row in source_children], "B1R0 child boxes")
        for index, cell in enumerate(source_cells):
            need(cell["source_signature_row_id"] == source_children[index]["signed_region_row_id"] and cell["source_free_interval_predicate_ast_materialized"] is False and cell["outer_carrier_box_claimed_as_full_support"] is False, "B1R0 cell gap")
            need(cell["predicate_source_inventory"] == {"predicate_family":"OUTGOING_W_TAIL_CHILD_FACTOR_CELL","region_product_sign":"STRICT_NEGATIVE","t_child":index}, "B1R0 cell semantics")
        normalization = member["Round271_W_tail_parent_normalization"]
        need(member["full_support_union_theorem_status"] == "PENDING_SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE" and normalization["interface_is_not_a_physical_support_boundary"] is True and normalization["normalized_parent_box"] == old["parent_box"], "B1R0 member gap")
        need(Q(normalization["artificial_interface"]["value"]) == midpoint and set(normalization["source_children"]) == set(old["ordered_children"]), "B1R0 interface")

        asts = physical_asts(old["source_chart"], old["owner_target"])
        ast_digest = sha_object(asts["strict_negative_predicate_ast"])
        parent_domain = interval_receipt(asts, parent, "PARENT_DOMAIN")
        # The parent is intentionally allowed to overwrap F; only all sqrt domains must be strict.
        face = (midpoint, midpoint, *parent[2:])
        child_width = child_boxes[0][1] - child_boxes[0][0]
        corridor_width = child_width / CORRIDOR_DENOMINATOR
        left_corridor = (midpoint - corridor_width, midpoint, *parent[2:])
        right_corridor = (midpoint, midpoint + corridor_width, *parent[2:])
        face_receipt = interval_receipt(asts, face, "COMPLETE_INTERFACE_FACE")
        left_receipt = interval_receipt(asts, left_corridor, "LEFT_CHILD_INWARD_CORRIDOR")
        right_receipt = interval_receipt(asts, right_corridor, "RIGHT_CHILD_INWARD_CORRIDOR")
        need(face_receipt["outgoing_factor_strict_negative"] and left_receipt["outgoing_factor_strict_negative"] and right_receipt["outgoing_factor_strict_negative"], "face/corridor strict negative")
        area = (parent[3] - parent[2]) * (parent[5] - parent[4])
        volume = corridor_width * area
        need(area == Q(1, 204_800) and volume == Q(177, 209_715_200_000), "face/corridor census")
        total_area += area
        total_corridor_volume += 2 * volume

        parent_wire = box_wire(parent, (True, True))
        owned_boxes = [box_wire(child_boxes[0], (True, False)), box_wire(child_boxes[1], (True, True))]
        atom_count = box_partition_atoms(parent, [(child_boxes[0], (True, False)), (child_boxes[1], (True, True))])
        k1_partition = k1.check_box_partition(parent_wire, owned_boxes)
        strict(k1_partition["formal_credit"], 0, "K1 partition credit")
        k1_signs = []
        for receipt, box in ((face_receipt, face), (left_receipt, left_corridor), (right_receipt, right_corridor)):
            k1_interval = k1.eval_interval(asts["outgoing_factor_ast"], {"t": k1.Interval(box[0], box[1]), "p": k1.Interval(box[2], box[3]), "s": k1.Interval(box[4], box[5])})
            need(k1_interval.upper < 0, "K1 strict-negative cross-check")
            k1_signs.append({"label": receipt["label"], "outgoing_factor_interval": k1_interval.wire(), "strict_negative": True})
        k1_cross_body = {"k1_source_sha256": PIN["K1_SOURCE"][3], "predicate_ast_sha256": ast_digest, "box_partition_receipt": k1_partition, "interval_sign_receipts": k1_signs, "formal_credit": 0}
        k1_cross = {**k1_cross_body, "cross_check_digest_sha256": sha_object(k1_cross_body)}
        k1_digests.add(k1_cross["cross_check_digest_sha256"])

        input_rows = {
            "old_blocked_theorem_row_id": old["theorem_row_id"],
            "old_blocked_theorem_row_sha256": old["row_sha256"],
            "R182_occurrence_row_commitment_sha256": sha_object(occurrence_packed[[row[1] for row in occurrence_packed].index(old["occurrence_id"])]),
            "R182_leaf_row_commitment_sha256": sha_object(leaf_packed[[row[0] for row in leaf_packed].index(old["parent_leaf_id"])]),
            "R271_child_row_ids": [row["signed_region_row_id"] for row in source_children],
            "R271_child_row_sha256": [row["row_sha256"] for row in source_children],
            "B1R0_cell_row_ids": [row["Round306B1R0_predicate_source_cell_row_id"] for row in source_cells],
            "B1R0_cell_row_sha256": [row["row_sha256"] for row in source_cells],
            "B1R0_member_row_id": member["Round306B1R0_member_union_row_id"],
            "B1R0_member_row_sha256": member["row_sha256"],
        }
        canonical_input = {
            "producer_source_commitment": snapshot.self_receipt,
            "member_id": member_id,
            "source_chart": old["source_chart"],
            "owner_target": old["owner_target"],
            "input_rows": input_rows,
            "physical_model_source_sha256": {label: PIN[label][3] for label in ("R179_EVALUATOR", "FIRST_HIT_ENGINE", "R271_VERIFIER")},
            "predicate_ast_sha256": ast_digest,
        }
        theorem = {
            "theorem_kind": "LOCAL_ARTIFICIAL_FACE_REGLUE_EXACT_V3",
            "source_free_predicate": {"coordinate_parameter":"TPS","support_semantics":"POINT_IS_IN_CANONICAL_OWNED_BOX_AND_STRICT_NEGATIVE_PREDICATE_IS_TRUE","asts":asts,"predicate_ast_sha256":ast_digest},
            "predicate_domain_on_parent": parent_domain,
            "canonical_half_open_partition": {"rule":"[lower,upper)_in_t_except_parent_outer_upper_endpoint_is_owned","parent_box":parent_wire,"owned_child_boxes":owned_boxes,"interface_owner_t_child":1,"interface_owner_source_row_id":source_children[1]["signed_region_row_id"],"exact_t_atom_count":atom_count,"K1_zero_credit_partition_cross_check":k1_partition},
            "child_parent_full_support_set_equality": {"parent_set":"PARENT_BOX_RESTRICT_STRICT_NEGATIVE_AST","child_sets":["CHILD_0_OWNED_BOX_RESTRICT_SAME_AST","CHILD_1_OWNED_BOX_RESTRICT_SAME_AST"],"same_predicate_ast_on_parent_and_both_children":True,"owned_boxes_disjoint":True,"owned_boxes_union_parent":True,"set_identity":"(B0_INTERSECT_P)_DISJOINT_UNION_(B1_INTERSECT_P)=(B_INTERSECT_P)","candidate_local_full_support_set_equality_credit":1,"local_full_support_set_equality_credit_before_package_seal":0,"normalized_support_credit":0},
            "complete_artificial_face": {"face_box":[qtext(x) for x in face],"exact_area":qtext(area),"interval_receipt":face_receipt,"outgoing_F_zero_graph_absent_on_complete_face":True},
            "two_sided_inward_corridors": {"relative_width":f"1/{CORRIDOR_DENOMINATOR}_OF_EACH_CHILD_T_WIDTH","corridor_width":qtext(corridor_width),"each_exact_volume":qtext(volume),"left":left_receipt,"right":right_receipt,"both_strictly_inside_same_F_negative_physical_cell":True},
            "K1_zero_credit_cross_checker": k1_cross,
        }
        conclusion = {
            "local_authorities_discharged_by_candidate": ["SOURCE_FREE_INTERVAL_PREDICATE_AST_AND_EQUIVALENCE_THEOREM_FOR_BOTH_CHILDREN","INPUT_BOUND_WHOLE_FACE_AND_TWO_SIDED_INWARD_CORRIDOR_PHYSICAL_EQUIVALENCE_CERTIFICATE","CANONICAL_HALF_OPEN_OWNER_ASSIGNMENT_FOR_THE_ARTIFICIAL_INTERFACE"],
            "package_seal_condition": {"required_role":"SEALED_INDEPENDENT_VERIFIER_RECEIPT_PINNED_BY_EXACT_8_MEMBER_MANIFEST","satisfied_inside_producer":False,"candidate_credit_effective_before_package_seal":False},
            "same_R182_parent": True,
            "same_complete_10_field_signature": True,
            "same_owner_target": True,
            "same_strict_negative_factor_cell": True,
            "artificial_interface_is_not_F_zero_physical_separator": True,
            "two_source_cells_are_one_local_physical_region_across_interface": True,
            "candidate_r2_artificial_face_reglue_credit": 1,
            "r2_artificial_face_reglue_credit_before_package_seal": 0,
        }
        nonpromotion = {"normalized_support_credit":0,"representation_cover_credit":0,"physical_incidence_equivalence_credit":0,"A1_A2_credit":0,"B1A_credit":0,"B2_credit":0,"transition_credit":0,"pair_routing_credit":0,"maximality_credit":0,"fibre_credit":0,"global_disposition_credit":0,"old_global_universe_count_pinned":False,"old_obligation_census_824864_pinned":False,"corrected_global_schema_sealed":False,"D02":"BLOCKED","D03":"NOT_REACHED","D04":"NOT_MINTED","CM2":"NO-GO_FOR_CLAIM"}
        conclusion_sha = sha_object({"canonical_input_commitment":canonical_input,"local_theorem":theorem,"local_conclusion":conclusion,"strict_nonpromotion":nonpromotion})
        rows.append(close({"schema":ROW_SCHEMA,"theorem_row_id":"round306b1af4k2r2w2-local-reglue:"+conclusion_sha,"member_id":member_id,"canonical_input_commitment":canonical_input,"local_theorem":theorem,"local_conclusion":conclusion,"strict_nonpromotion":nonpromotion,"conclusion_sha256":conclusion_sha,"candidate_r2_artificial_face_reglue_credit":1,"r2_artificial_face_reglue_credit":0,"credit_effective_only_with_manifest_pinned_PASS_independent_verification":True,"normalized_support_credit":0,"CM2":"NO-GO_FOR_CLAIM"}))

    rows.sort(key=lambda row: row["theorem_row_id"].encode("ascii"))
    need(len(rows) == 4 and len(k1_digests) == 4, "four distinct theorem/K1 rows")
    need(total_area == Q(1, 51_200) and total_corridor_volume == Q(177, 26_214_400_000), "global local-geometry census")
    ledger = {"schema":SCHEMA+".theorem-ledger.v1","row_count":4,"rows_sha256":sha_object(rows),"row_hashes_sha256":sha_object([row["row_sha256"] for row in rows]),"conclusion_hashes_sha256":sha_object([row["conclusion_sha256"] for row in rows]),"rows":rows}
    ledger_bytes = canonical(ledger) + b"\n"
    input_pins = [{"label":label,"filename":name,"exact_size":size,"sha256":sha,"role":role,"two_pass_held_fd":True} for label,name,size,sha,role in PINS]
    result = {
        "status":STATUS,
        "schema":SCHEMA,
        "seed_affects_output":False,
        "runtime_isolation":{"sys_flags_isolated":1,"sys_flags_dont_write_bytecode":1,"sys_flags_no_site":1,"sys_dont_write_bytecode":True,"required_launcher":"python3 -I -B -S"},
        "census":{"old_blocked_rows":4,"local_theorem_rows":4,"local_full_support_set_equalities":4,"complete_artificial_faces":4,"strict_negative_complete_faces":4,"strict_negative_inward_corridors":8,"canonical_half_open_interface_owners":4,"candidate_r2_artificial_face_reglue_credit":4,"r2_artificial_face_reglue_credit_before_package_seal":0},
        "exact_geometry":{"complete_face_area_sum":qtext(total_area),"inward_corridor_volume_sum":qtext(total_corridor_volume),"corridor_relative_denominator":CORRIDOR_DENOMINATOR},
        "ordered_table_commitments":receipts,
        "frozen_input_pins":input_pins,
        "producer_source_commitment":snapshot.self_receipt,
        "theorem_ledger":{"filename":LEDGER_NAME,"file_sha256":hashlib.sha256(ledger_bytes).hexdigest(),"exact_size":len(ledger_bytes),"row_count":4,"rows_sha256":ledger["rows_sha256"],"row_hashes_sha256":ledger["row_hashes_sha256"],"conclusion_hashes_sha256":ledger["conclusion_hashes_sha256"]},
        "authority_scope":{"positive_authority":"4_INPUT_BOUND_LOCAL_ARTIFICIAL_FACE_REGLUE_THEOREM_CANDIDATES_CONDITIONAL_ON_MANIFEST_PINNED_PASS_VERIFICATION","independent_verifier_receipt_discharged_inside_producer":False,"K1_is_zero_credit_cross_checker_only":True,"local_full_support_set_equality_is_not_global_normalized_support":True,"outer_carrier_box_alone_is_not_full_support":True,"no_credit_from_graph_label_or_signature_equality_alone":True,"old_global_universe_count_pinned":False,"old_obligation_census_824864_pinned":False,"corrected_global_schema_sealed":False},
        "strict_nonpromotion":{"normalized_support_credit":0,"representation_cover_credit":0,"physical_incidence_equivalence_credit":0,"A1_A2_credit":0,"B1A_credit":0,"B2_credit":0,"transition_credit":0,"pair_routing_credit":0,"maximality_credit":0,"fibre_credit":0,"global_disposition_credit":0,"old_global_universe_count_pinned":False,"old_obligation_census_824864_pinned":False,"corrected_global_schema_sealed":False,"D02":"BLOCKED","D03":"NOT_REACHED","D04":"NOT_MINTED","CM2":"NO-GO_FOR_CLAIM"},
        "required_next":"consume these four local reglue rows inside the fresh R2 normalized-support reconstruction; do not promote the R2 family, the stale B0/DSU universe, or the stale 824864 obligation census; corrected global schema is not sealed",
    }
    result_doc = {"schema":SCHEMA+".result.v1","result":result,"result_sha256":sha_object(result)}
    attack = make_attack(rows)
    snapshot.final()
    return {"schema":SCHEMA+".candidate-bundle.v1","result_document":result_doc,"theorem_ledger":ledger,"attack_suite":attack}


def make_attack(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tests: list[dict[str, Any]] = []
    def record(label: str, ok: bool) -> None:
        need(type(ok) is bool and ok, "attack:" + label)
        tests.append({"test":label,"rejected_or_invariant_passed":True})
    first, second = rows[0], rows[1]
    record("different_member_different_conclusion_digest", first["conclusion_sha256"] != second["conclusion_sha256"])
    probe = json.loads(json.dumps(first))
    probe["canonical_input_commitment"] = second["canonical_input_commitment"]
    recomputed = sha_object({"canonical_input_commitment":probe["canonical_input_commitment"],"local_theorem":probe["local_theorem"],"local_conclusion":probe["local_conclusion"],"strict_nonpromotion":probe["strict_nonpromotion"]})
    record("cross_certificate_input_swap_breaks_conclusion", recomputed != first["conclusion_sha256"])
    probe = json.loads(json.dumps(first))
    probe["local_theorem"]["canonical_half_open_partition"]["interface_owner_t_child"] = 0
    recomputed = sha_object({"canonical_input_commitment":probe["canonical_input_commitment"],"local_theorem":probe["local_theorem"],"local_conclusion":probe["local_conclusion"],"strict_nonpromotion":probe["strict_nonpromotion"]})
    record("half_open_owner_mutation_breaks_conclusion", recomputed != first["conclusion_sha256"])
    probe = json.loads(json.dumps(first))
    probe["local_theorem"]["source_free_predicate"]["asts"]["strict_negative_predicate_ast"]["op"] = "LE_ZERO"
    recomputed = sha_object({"canonical_input_commitment":probe["canonical_input_commitment"],"local_theorem":probe["local_theorem"],"local_conclusion":probe["local_conclusion"],"strict_nonpromotion":probe["strict_nonpromotion"]})
    record("predicate_AST_mutation_breaks_conclusion", recomputed != first["conclusion_sha256"])
    record("four_distinct_K1_cross_check_digests", len({row["local_theorem"]["K1_zero_credit_cross_checker"]["cross_check_digest_sha256"] for row in rows}) == 4)
    record("all_global_credits_zero", all(row["normalized_support_credit"] == 0 and row["CM2"] == "NO-GO_FOR_CLAIM" for row in rows))
    record("explicit_tmp_policy_outside_deliverables", not (Path("/tmp").resolve() == HERE or HERE in Path("/tmp").resolve().parents))
    result = {"schema":SCHEMA+".attack-suite.v1","test_count":len(tests),"tests":tests,"all_passed":True}
    return {**result,"attack_suite_sha256":sha_object(result)}


def atomic_write(directory: Path, name: str, payload: bytes) -> None:
    need(directory.resolve(strict=True) == HERE and name == os.path.basename(name), "write boundary")
    target = directory / name
    if target.exists() or target.is_symlink():
        info = os.stat(target, follow_symlinks=False)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(payload), "existing output identity:" + name)
        fd = os.open(target, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
        try:
            opened = os.fstat(fd)
            need(identity(info) == identity(opened) and hash_fd(fd) == hashlib.sha256(payload).hexdigest(), "existing output must be idempotent-exact:" + name)
        finally:
            os.close(fd)
        return
    fd, temp_name = tempfile.mkstemp(prefix="."+name+".", suffix=".tmp", dir=directory)
    temp = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        # Publish without replacement.  A concurrent winner is accepted only
        # if it is byte-identical; any other pre-existing target fails closed.
        try:
            os.link(temp, target, follow_symlinks=False)
        except FileExistsError:
            info = os.stat(target, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(payload), "concurrent output identity:" + name)
            existing = os.open(target, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
            try:
                need(hash_fd(existing) == hashlib.sha256(payload).hexdigest(), "concurrent output must be idempotent-exact:" + name)
            finally:
                os.close(existing)
        else:
            temp.unlink()
            temp = Path("")
            published = os.stat(target, follow_symlinks=False)
            need(stat.S_ISREG(published.st_mode) and published.st_nlink == 1 and published.st_size == len(payload), "published output identity:" + name)
        dirfd = os.open(directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(dirfd)
        finally:
            os.close(dirfd)
    finally:
        if temp != Path("") and temp.exists():
            temp.unlink()


def write_bundle(bundle: dict[str, Any], output: Path) -> None:
    ledger_bytes = canonical(bundle["theorem_ledger"]) + b"\n"
    result_bytes = canonical(bundle["result_document"]) + b"\n"
    attack_bytes = canonical(bundle["attack_suite"]) + b"\n"
    atomic_write(output, LEDGER_NAME, ledger_bytes)
    atomic_write(output, RESULT_NAME, result_bytes)
    atomic_write(output, ATTACK_NAME, attack_bytes)


def self_test() -> dict[str, Any]:
    first = physical_asts("G:E", "W[1,-1]")
    second = physical_asts("G:E", "W[1,0]")
    need(sha_object(first) != sha_object(second), "AST input binding")
    parent = (Q(0),Q(2),Q(0),Q(1),Q(0),Q(1))
    need(box_partition_atoms(parent, [((Q(0),Q(1),Q(0),Q(1),Q(0),Q(1)),(True,False)),((Q(1),Q(2),Q(0),Q(1),Q(0),Q(1)),(True,True))]) == 5, "partition self-test")
    blocked = 0
    for bad in ("../x", "", "x/y"):
        try:
            need(bad == os.path.basename(bad) and bool(bad), "basename")
        except Blocked:
            blocked += 1
    need(blocked == 3, "path attacks")
    return {"status":"PASS","AST_digest_separation":True,"half_open_partition":True,"path_attacks_rejected":3,"formal_credit":0}


def main() -> int:
    need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.no_site == 1 and sys.dont_write_bytecode is True, "producer requires isolated no-site no-bytecode runtime: python3 -I -B -S")
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--print-contract", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--full-replay", action="store_true")
    parser.add_argument("--seed", default="r2w2-seed-0")
    parser.add_argument("--input-dir", type=Path, default=HERE)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    if args.print_contract:
        output: Any = {"schema":SCHEMA,"status":STATUS,"writes_only_with_explicit_flag":True,"seed_affects_output":False,"input_pin_count":len(PINS),"K1_role":"ZERO_CREDIT_CROSS_CHECKER_ONLY","required_launcher":"python3 -I -B -S"}
    elif args.self_test:
        output = self_test()
    else:
        with Frozen(args.input_dir) as snapshot:
            output = build(snapshot, args.seed)
        if args.write:
            write_bundle(output, args.output_dir)
    sys.stdout.buffer.write(canonical(output) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
