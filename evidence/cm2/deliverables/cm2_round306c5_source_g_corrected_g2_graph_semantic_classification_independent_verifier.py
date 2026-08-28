#!/usr/bin/env python3
"""Independently replay every corrected G2 graph semantic classification."""

from __future__ import annotations

import argparse
import io
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
import gzip
import hashlib
import json
from math import isqrt, sqrt
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
from typing import Any, Final, Iterable


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification"
RESULT_NAME: Final = PREFIX + "_result.json"
LEDGER_NAME: Final = PREFIX + "_row_ledger.jsonl.gz"
SCHEMA: Final = "cm2.round306c5.source-g-corrected-g2-graph-semantic-classification.v1"
ROW_SCHEMA: Final = SCHEMA + ".row.v1"
STATUS: Final = "PASS_5264_POSITIVE_G2_GRAPH_DEFINITIONS__33344_R235_EMPTY_GRAPH_DISPOSITIONS__FRESH_DSU_REQUIRED"
SQRT_BITS: Final = 160
OWNER_RE: Final = re.compile(r"^([GW])\[(-?[0-9]+),(-?[0-9]+)\]$")


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("C3_MANIFEST", "cm2_round306c3_source_g_corrected_g2_exact_join_filter_manifest.sha256", 956, "f05f172ec8fc25564067539091f77f39bc33395dd5e0232f38bde9c587493761"),
    Pin("C3_RESULT", "cm2_round306c3_source_g_corrected_g2_exact_join_filter_result.json", 6_458, "66df0b03fdc9f432e330f55eeedc3f49fad0fa2f12fbb6d94689e06a6cc9d8a0"),
    Pin("C4_MANIFEST", "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_manifest.sha256", 1_177, "5550eb9cf4e474a8d08086062e28538e909f6e1c7e499ba10a78a2d24e683de6"),
    Pin("C4_RESULT", "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_result.json", 6_204, "1396fadf4ef85340bdc0b1ca3b191a67a8266ed40cc3ee9a3dcc8f9650ffb8da"),
    Pin("C4_LEDGER", "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz", 101_147, "3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),
    Pin("B1G0_MANIFEST", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256", 1_959, "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8"),
    Pin("B1G0_GRAPH", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz", 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"),
    Pin("B1G0_SHEET", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),
    Pin("B1G0_SIDE", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),
    Pin("R234_MANIFEST", "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_manifest.sha256", 574, "f8714ecdf804657fc6633136544f567b07e7d8503095d17fcda19226feefc432"),
    Pin("R234_CERT", "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    Pin("R235_MANIFEST", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_manifest.sha256", 566, "cf58b7d2f419ea252c3398665302fe6f5ff06436af20a56beaaa47e5ef822ea0"),
    Pin("R235_CERT", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json", 67_765_471, "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"),
    Pin("R242_MANIFEST", "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_manifest.sha256", 897, "6da30fe3f9438ec73dc9c7d1aac770d8e9730aa9564ab0c535f1596cdc09ef2f"),
    Pin("R242_CERT", "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json", 13_734_655, "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e"),
)

PRODUCER_PIN: Final = Pin("PRODUCER", "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_producer.py", 46_747, "b81e848661610a16058de15f8b7e6ea25d6b2ad7487006f45907916800880d51")
PRODUCER_NAME: Final = PRODUCER_PIN.filename
VERIFIER_NAME: Final = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_independent_verifier.py"
ATTACK_NAME: Final = PREFIX + "_attack_suite.json"
VERIFICATION_NAME: Final = PREFIX + "_verification.json"
REPORT_NAME: Final = PREFIX + "_report.md"
COLD_NAME: Final = PREFIX + "_cold_replay.md"
MANIFEST_NAME: Final = PREFIX + "_manifest.sha256"
CANDIDATE_RESULT_SIZE: Final = 6_975
CANDIDATE_RESULT_SHA256: Final = "0da7931e1a46d68ae8da69a7de1534a3955c83a8d6f5d8ab0170be7a34dc6320"
CANDIDATE_LEDGER_SIZE: Final = 78_082_824
CANDIDATE_LEDGER_SHA256: Final = "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"
PACKAGE_MEMBERS: Final = (PRODUCER_NAME, LEDGER_NAME, RESULT_NAME, VERIFIER_NAME, ATTACK_NAME, VERIFICATION_NAME, REPORT_NAME, COLD_NAME)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def hash_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    while True:
        block = os.read(fd, 1_048_576)
        if not block:
            return digest.hexdigest()
        digest.update(block)


class Snapshot:
    def __init__(self) -> None:
        self.dirfd = -1
        self.fds: dict[str, int] = {}
        self.ids: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "Snapshot":
        before = os.stat(ROOT, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not ROOT.is_symlink(), "deliverables directory")
        self.dirfd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for pin in (*PINS, PRODUCER_PIN):
            info = os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == pin.size, "pin identity:" + pin.role)
            fd = os.open(pin.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            opened = os.fstat(fd)
            need(identity(opened) == identity(info), "pin race:" + pin.role)
            need(hash_fd(fd) == hash_fd(fd) == pin.sha256, "pin digest:" + pin.role)
            self.fds[pin.role] = fd
            self.ids[pin.role] = identity(opened)
        return self

    def bytes(self, role: str) -> bytes:
        fd = self.fds[role]
        os.lseek(fd, 0, os.SEEK_SET)
        blocks: list[bytes] = []
        while True:
            block = os.read(fd, 1_048_576)
            if not block:
                return b"".join(blocks)
            blocks.append(block)

    def duplicate(self, role: str) -> int:
        fd = os.dup(self.fds[role])
        os.lseek(fd, 0, os.SEEK_SET)
        return fd

    def final(self) -> None:
        for pin in reversed((*PINS, PRODUCER_PIN)):
            fd = self.fds[pin.role]
            need(identity(os.fstat(fd)) == self.ids[pin.role], "final fd:" + pin.role)
            need(identity(os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.ids[pin.role], "final path:" + pin.role)
            need(hash_fd(fd) == pin.sha256, "final digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            os.close(self.dirfd)


def direct(snapshot: Snapshot, role: str) -> dict[str, Any]:
    raw = snapshot.bytes(role)
    value = json.loads(raw)
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"}, "canonical direct:" + role)
    if "result_sha256" in value:
        body = dict(value)
        claimed = body.pop("result_sha256")
        need(claimed == objsha(body) or (set(value) == {"schema", "result", "result_sha256"} and claimed == objsha(value["result"])), "direct closure:" + role)
    return value


def gzip_doc(snapshot: Snapshot, role: str) -> dict[str, Any]:
    fd = snapshot.duplicate(role)
    try:
        with os.fdopen(fd, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            value = json.load(stream)
        need(type(value) is dict, "gzip document:" + role)
        return value
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def jsonl(snapshot: Snapshot, role: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    fd = snapshot.duplicate(role)
    try:
        with os.fdopen(fd, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            for ordinal, line in enumerate(stream):
                row = json.loads(line)
                need(type(row) is dict and line.endswith(b"\n") and canonical(row) + b"\n" == line, "canonical JSONL:" + role + ":" + str(ordinal))
                rows.append(row)
        return rows
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def manifest_entries(snapshot: Snapshot, role: str) -> dict[str, str]:
    raw = snapshot.bytes(role)
    need(raw.endswith(b"\n"), "manifest newline:" + role)
    output: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        digest, path = line.split("  ")
        name = os.path.basename(path)
        need(len(digest) == 64 and path in {name, "deliverables/" + name} and name not in output, "manifest entry:" + role)
        output[name] = digest
    return output


def qwire(value: Q | int) -> dict[str, int]:
    rational = Q(value)
    return {"numerator": rational.numerator, "denominator": rational.denominator}


@dataclass(frozen=True)
class Interval:
    lower: Q
    upper: Q

    def __post_init__(self) -> None:
        need(type(self.lower) is Q and type(self.upper) is Q and self.lower <= self.upper, "interval")

    @classmethod
    def point(cls, value: Q | int) -> "Interval":
        rational = Q(value)
        return cls(rational, rational)

    def __add__(self, other: Any) -> "Interval":
        rhs = other if type(other) is Interval else Interval.point(other)
        return Interval(self.lower + rhs.lower, self.upper + rhs.upper)

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval(-self.upper, -self.lower)

    def __sub__(self, other: Any) -> "Interval":
        return self + (-other)

    def __rsub__(self, other: Any) -> "Interval":
        return Interval.point(other) + (-self)

    def __mul__(self, other: Any) -> "Interval":
        rhs = other if type(other) is Interval else Interval.point(other)
        values = (self.lower * rhs.lower, self.lower * rhs.upper, self.upper * rhs.lower, self.upper * rhs.upper)
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def square(self) -> "Interval":
        values = (self.lower * self.lower, self.upper * self.upper)
        return Interval(Q(0) if self.lower <= 0 <= self.upper else min(values), max(values))

    def divide(self, other: Any) -> "Interval":
        rhs = other if type(other) is Interval else Interval.point(other)
        need(not rhs.lower <= 0 <= rhs.upper, "interval division")
        reciprocal = Interval(min(Q(1, rhs.lower), Q(1, rhs.upper)), max(Q(1, rhs.lower), Q(1, rhs.upper)))
        return self * reciprocal

    def sign(self) -> str:
        if self.lower > 0:
            return "STRICT_POSITIVE"
        if self.upper < 0:
            return "STRICT_NEGATIVE"
        return "OVERWRAP"

    def wire(self) -> dict[str, Any]:
        return {"lower": qwire(self.lower), "upper": qwire(self.upper)}


def sqrt_interval(value: Interval) -> Interval:
    need(value.lower > 0, "sqrt domain")
    scale = 1 << SQRT_BITS

    def floor_sqrt(rational: Q) -> Q:
        return Q(isqrt((rational.numerator * scale * scale) // rational.denominator), scale)

    lower = floor_sqrt(value.lower)
    upper = floor_sqrt(value.upper)
    if upper * upper < value.upper:
        upper += Q(1, scale)
    return Interval(lower, upper)


@dataclass(frozen=True)
class Dual:
    value: Interval
    derivative: Interval

    @classmethod
    def constant(cls, value: Interval | Q | int) -> "Dual":
        interval = value if type(value) is Interval else Interval.point(value)
        return cls(interval, Interval.point(0))

    def __add__(self, other: Any) -> "Dual":
        rhs = other if type(other) is Dual else Dual.constant(other)
        return Dual(self.value + rhs.value, self.derivative + rhs.derivative)

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other: Any) -> "Dual":
        return self + (-other)

    def __rsub__(self, other: Any) -> "Dual":
        return Dual.constant(other) + (-self)

    def __mul__(self, other: Any) -> "Dual":
        rhs = other if type(other) is Dual else Dual.constant(other)
        return Dual(self.value * rhs.value, self.derivative * rhs.value + self.value * rhs.derivative)

    __rmul__ = __mul__


def sqrt_dual(value: Dual) -> Dual:
    root = sqrt_interval(value.value)
    return Dual(root, value.derivative.divide(root * 2))


def owner_xy(owner: str) -> tuple[str, int, int]:
    match = OWNER_RE.fullmatch(owner)
    need(match is not None, "owner")
    return match.group(1), int(match.group(2)), int(match.group(3))


def geometry(chart: str, owner: str, t_bounds: tuple[Q, Q], p_bounds: tuple[Q, Q], variable: str | None) -> dict[str, Interval | Dual]:
    owner_kind, owner_x, owner_y = owner_xy(owner)
    need(chart in {"G:E", "G:W", "G:N", "G:S"} and owner_kind == "G", "G geometry")
    t_interval = Interval(*t_bounds)
    p_interval = Interval(*p_bounds)
    if variable is None:
        t: Interval | Dual = t_interval
        p: Interval | Dual = p_interval
        one: Interval | Dual = Interval.point(1)
        normal_root = sqrt_interval(one - t.square())
        phase_root = sqrt_interval(one - p.square())
    else:
        need(variable in {"t", "p"}, "dual variable")
        t = Dual(t_interval, Interval.point(1 if variable == "t" else 0))
        p = Dual(p_interval, Interval.point(1 if variable == "p" else 0))
        one = Dual.constant(1)
        normal_root = sqrt_dual(one - t * t)
        phase_root = sqrt_dual(one - p * p)
    cell = chart[-1]
    if cell == "E":
        normal_x, normal_y = normal_root, t
    elif cell == "W":
        normal_x, normal_y = -normal_root, t
    elif cell == "N":
        normal_x, normal_y = t, normal_root
    else:
        normal_x, normal_y = t, -normal_root
    tangent_x = phase_root * normal_x - p * normal_y
    tangent_y = phase_root * normal_y + p * normal_x
    radius = Q(9, 25)
    source_x, source_y = radius * normal_x, radius * normal_y
    delta_x, delta_y = owner_x - source_x, owner_y - source_y
    transverse = -(tangent_y * delta_x) + tangent_x * delta_y
    radical_input = Dual.constant(radius * radius) - transverse * transverse if variable is not None else Interval.point(radius * radius) - transverse.square()
    radical = sqrt_dual(radical_input) if variable is not None else sqrt_interval(radical_input)
    hit_x = owner_x - radical * tangent_x + transverse * tangent_y
    hit_y = owner_y - radical * tangent_y - transverse * tangent_x
    return {"source_x": source_x, "source_y": source_y, "hit_x": hit_x, "hit_y": hit_y}


def endpoint_spec(frontier: dict[str, Any]) -> tuple[str, int]:
    kind, axis, wall_text = frontier["reason_labels"][0].split(":")
    need(kind == "wall_endpoint_or_count_transition" and axis in {"X", "Y"}, "endpoint reason")
    return axis, int(wall_text)


def target_factor(frontier: dict[str, Any], t_bounds: tuple[Q, Q], p_bounds: tuple[Q, Q], variable: str | None = None) -> Interval | Dual:
    axis, wall = endpoint_spec(frontier)
    value = geometry(frontier["chart"], frontier["owner_target"], t_bounds, p_bounds, variable)["hit_x" if axis == "X" else "hit_y"]
    return value - wall


def strict_target_derivative(frontier: dict[str, Any], expected: str) -> dict[str, Any]:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    stack = [(t0, t1, p0, p1, 0)]
    cells = 0
    maximum_depth = 0
    while stack:
        ta, tb, pa, pb, depth = stack.pop()
        dual = target_factor(frontier, (ta, tb), (pa, pb), "t")
        need(type(dual) is Dual, "target t dual")
        sign = dual.derivative.sign()
        if sign == expected:
            cells += 1
            maximum_depth = max(maximum_depth, depth)
            continue
        need(depth < 8, "target t derivative unresolved")
        if depth % 2 == 0:
            middle = (pa + pb) / 2
            stack.extend(((ta, tb, pa, middle, depth + 1), (ta, tb, middle, pb, depth + 1)))
        else:
            middle = (ta + tb) / 2
            stack.extend(((ta, middle, pa, pb, depth + 1), (middle, tb, pa, pb, depth + 1)))
    return {"strict_t_derivative_sign": expected, "proof_cell_count": cells, "maximum_split_depth": maximum_depth}


def face_factor(frontier: dict[str, Any], t_value: Q, p_bounds: tuple[Q, Q], variable: str | None = None) -> Interval | Dual:
    return target_factor(frontier, (t_value, t_value), p_bounds, variable)


def parent_face_sign_proof(frontier: dict[str, Any], t_value: Q, p0: Q, p1: Q, wanted: str) -> dict[str, Any] | None:
    dual = face_factor(frontier, t_value, (p0, p1), "p")
    need(type(dual) is Dual, "face p dual")
    if dual.value.sign() == wanted:
        return {"method": "DIRECT_PARENT_P_INTERVAL", "face_t": qwire(t_value), "factor_sign": wanted, "factor_interval": dual.value.wire(), "p_derivative_sign": dual.derivative.sign()}
    derivative_sign = dual.derivative.sign()
    if derivative_sign not in {"STRICT_POSITIVE", "STRICT_NEGATIVE"}:
        return None
    endpoint = p0 if (wanted == "STRICT_POSITIVE") == (derivative_sign == "STRICT_POSITIVE") else p1
    value = face_factor(frontier, t_value, (endpoint, endpoint))
    need(type(value) is Interval, "face endpoint")
    if value.sign() != wanted:
        return None
    return {"method": "STRICT_P_MONOTONICITY_AND_EXTREMAL_ENDPOINT", "face_t": qwire(t_value), "factor_sign": wanted, "p_derivative_sign": derivative_sign, "p_derivative_interval": dual.derivative.wire(), "extremal_p": qwire(endpoint), "extremal_factor_interval": value.wire()}


def empty_target_proof(frontier: dict[str, Any], t_derivative_sign: str) -> tuple[str, dict[str, Any]] | None:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    if t_derivative_sign == "STRICT_POSITIVE":
        attempts = ((t0, "STRICT_POSITIVE", "STRICT_POSITIVE"), (t1, "STRICT_NEGATIVE", "STRICT_NEGATIVE"))
    else:
        attempts = ((t0, "STRICT_NEGATIVE", "STRICT_NEGATIVE"), (t1, "STRICT_POSITIVE", "STRICT_POSITIVE"))
    for face_t, wanted, full_sign in attempts:
        proof = parent_face_sign_proof(frontier, face_t, p0, p1, wanted)
        if proof is not None:
            proof["strict_t_derivative_sign"] = t_derivative_sign
            proof["connected_complete_domain_implies_fixed_factor_sign"] = full_sign
            return full_sign, proof
    return None


def float_hit(frontier: dict[str, Any], t: float, p: float) -> float:
    _, owner_x, owner_y = owner_xy(frontier["owner_target"])
    normal_root = sqrt(1.0 - t * t)
    phase_root = sqrt(1.0 - p * p)
    cell = frontier["chart"][-1]
    normal_x, normal_y = {"E": (normal_root, t), "W": (-normal_root, t), "N": (t, normal_root), "S": (t, -normal_root)}[cell]
    tangent_x = phase_root * normal_x - p * normal_y
    tangent_y = phase_root * normal_y + p * normal_x
    radius = 9.0 / 25.0
    source_x, source_y = radius * normal_x, radius * normal_y
    delta_x, delta_y = owner_x - source_x, owner_y - source_y
    transverse = -tangent_y * delta_x + tangent_x * delta_y
    radical = sqrt(max(0.0, radius * radius - transverse * transverse))
    hit_x = owner_x - radical * tangent_x + transverse * tangent_y
    hit_y = owner_y - radical * tangent_y - transverse * tangent_x
    axis, wall = endpoint_spec(frontier)
    return (hit_x if axis == "X" else hit_y) - wall


def positive_target_witness(frontier: dict[str, Any], t_derivative_sign: str) -> dict[str, Any]:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    positive = t_derivative_sign == "STRICT_POSITIVE"
    best: tuple[float, int, int] | None = None
    for denominator in (128, 4096):
        for index in range(denominator + 1):
            p_value = float(p0) + (float(p1) - float(p0)) * index / denominator
            lower = float_hit(frontier, float(t0), p_value)
            upper = float_hit(frontier, float(t1), p_value)
            margin = min(-lower, upper) if positive else min(lower, -upper)
            if best is None or margin > best[0]:
                best = (margin, denominator, index)
        need(best is not None, "numeric locator")
        if best[0] <= 0:
            continue
        _, selected_denominator, selected_index = best
        center = p0 + (p1 - p0) * Q(selected_index, selected_denominator)
        minimum_depth = 8 if selected_denominator == 128 else 13
        for depth in range(minimum_depth, 27):
            radius = (p1 - p0) * Q(1, 1 << depth)
            lower_p, upper_p = max(p0, center - radius), min(p1, center + radius)
            if lower_p == upper_p:
                continue
            lower_face = face_factor(frontier, t0, (lower_p, upper_p))
            upper_face = face_factor(frontier, t1, (lower_p, upper_p))
            need(type(lower_face) is Interval and type(upper_face) is Interval, "witness faces")
            expected = ("STRICT_NEGATIVE", "STRICT_POSITIVE") if positive else ("STRICT_POSITIVE", "STRICT_NEGATIVE")
            if (lower_face.sign(), upper_face.sign()) == expected:
                s0, s1 = map(Q, frontier["box"][4:6])
                need(lower_p < upper_p and s0 < s1, "positive base area")
                return {"exact_base_domain_predicate": "LOWER_AND_UPPER_T_FACE_SIGNS_OPPOSE_WITH_DECLARED_T_ORIENTATION", "witness_locator_grid_denominator": selected_denominator, "witness_shrink_depth": depth, "closed_p_interval": [qwire(lower_p), qwire(upper_p)], "closed_s_interval": [qwire(s0), qwire(s1)], "exact_positive_base_area": qwire((upper_p - lower_p) * (s1 - s0)), "lower_t_face_factor_interval": lower_face.wire(), "lower_t_face_factor_sign": lower_face.sign(), "upper_t_face_factor_interval": upper_face.wire(), "upper_t_face_factor_sign": upper_face.sign(), "unique_graph_point_for_every_base_point_in_exact_domain": True, "graph_local_dimension": 2}
    raise Rejected("positive target witness unresolved:" + frontier["frontier_row_id"])


def row_ref(ordinal: int, row: dict[str, Any], field: str) -> list[Any]:
    need(type(row.get(field)) is str, "row ref:" + field)
    return [ordinal, row[field], hashlib.sha256(canonical(row)).hexdigest()]


def closed_ref(ordinal: int, row: dict[str, Any], field: str) -> list[Any]:
    need(type(row.get(field)) is str and type(row.get("row_sha256")) is str, "closed ref:" + field)
    body = dict(row)
    claimed = body.pop("row_sha256")
    need(claimed == objsha(body), "closed row:" + field)
    return [ordinal, row[field], hashlib.sha256(canonical(row)).hexdigest(), claimed]


def sequence_sha(values: Iterable[Any]) -> str:
    digest = hashlib.sha256()
    digest.update(b"[")
    first = True
    for value in values:
        if not first:
            digest.update(b",")
        digest.update(canonical(value))
        first = False
    digest.update(b"]")
    return digest.hexdigest()


def gzip_rows(rows: list[dict[str, Any]]) -> tuple[bytes, bytes]:
    plain = b"".join(canonical(row) + b"\n" for row in rows)
    return gzip.compress(plain, compresslevel=9, mtime=0), plain


def table_rows(document: dict[str, Any], field: str) -> list[dict[str, Any]]:
    value = document["result"][field]
    if type(value) is list:
        return value
    need(type(value) is dict and type(value.get("rows")) is list and value["row_count"] == len(value["rows"]), "table:" + field)
    return value["rows"]


def build() -> tuple[dict[str, Any], bytes]:
    with Snapshot() as snapshot:
        pin_by_role = {pin.role: pin for pin in PINS}
        manifest_roles = ("C3_MANIFEST", "C4_MANIFEST", "B1G0_MANIFEST", "R234_MANIFEST", "R235_MANIFEST", "R242_MANIFEST")
        manifests = {role: manifest_entries(snapshot, role) for role in manifest_roles}
        bindings = {
            "C3_MANIFEST": ("C3_RESULT",),
            "C4_MANIFEST": ("C4_RESULT", "C4_LEDGER"),
            "B1G0_MANIFEST": ("B1G0_GRAPH", "B1G0_SHEET", "B1G0_SIDE"),
            "R234_MANIFEST": ("R234_CERT",),
            "R235_MANIFEST": ("R235_CERT",),
            "R242_MANIFEST": ("R242_CERT",),
        }
        for manifest_role, file_roles in bindings.items():
            for file_role in file_roles:
                pin = pin_by_role[file_role]
                need(manifests[manifest_role][pin.filename] == pin.sha256, "manifest binding:" + manifest_role + ":" + file_role)

        c3 = direct(snapshot, "C3_RESULT")
        need(c3["corrected_census"] == {"graph_definition_rows": 38_624, "G2A_sheet_members": 38_608, "G2B_side_references": 76_832, "G2B_side_distinct_members": 76_816, "duplicate_side_reference_excess": 16, "physical_incidence_relations": 115_440, "semantic_obligation_rows": 154_064}, "C3 census")
        c4 = direct(snapshot, "C4_RESULT")
        need(c4["result_sha256"] == "3f015251bf03fbf1e9cdb3b9dc766d67f361df87e0aa3ecf7ba729901a8aa5a6", "C4 result")
        c4_rows = jsonl(snapshot, "C4_LEDGER")
        need(len(c4_rows) == 16, "C4 rows")

        r234 = direct(snapshot, "R234_CERT")
        frontier_rows = table_rows(r234, "depth6_frontier_rows")
        frontier_index = {row["frontier_row_id"]: (ordinal, row) for ordinal, row in enumerate(frontier_rows)}
        need(len(frontier_index) == len(frontier_rows), "R234 frontier unique")
        r235 = direct(snapshot, "R235_CERT")
        r235_rows = table_rows(r235, "single_endpoint_graph_partition_rows")
        need(len(r235_rows) == 38_328, "R235 rows")
        r235_index = {row["endpoint_graph_partition_row_id"]: (ordinal, row) for ordinal, row in enumerate(r235_rows)}
        need(len(r235_index) == len(r235_rows), "R235 unique")
        r242 = direct(snapshot, "R242_CERT")
        r242_rows = table_rows(r242, "formal_positive_2D_transition_sheet_patch_ledger")
        need(len(r242_rows) == 264 and all(row["local_positive_2D_transition_sheet_patch_credit"] == 1 for row in r242_rows), "R242 positive rows")
        r242_index = {row["transition_sheet_patch_row_id"]: (ordinal, row) for ordinal, row in enumerate(r242_rows)}
        need(len(r242_index) == len(r242_rows), "R242 unique")

        graphs = gzip_doc(snapshot, "B1G0_GRAPH")["graph_source_inventory_rows"]
        sheets = gzip_doc(snapshot, "B1G0_SHEET")["graph_sheet_join_rows"]
        sides = gzip_doc(snapshot, "B1G0_SIDE")["graph_side_join_rows"]
        graph_by_id = {row["graph_id"]: (ordinal, row) for ordinal, row in enumerate(graphs)}
        sheet_by_graph: dict[str, tuple[int, dict[str, Any]]] = {}
        sides_by_graph: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
        for ordinal, row in enumerate(sheets):
            key = row["graph_source_inventory_row_id"]
            need(key not in sheet_by_graph, "one sheet per graph")
            sheet_by_graph[key] = (ordinal, row)
        for ordinal, row in enumerate(sides):
            sides_by_graph[row["graph_source_inventory_row_id"]].append((ordinal, row))
        need(len(graph_by_id) == len(graphs) == 38_624 and len(sheets) == 38_624 and len(sides) == 76_848, "B1G0 census")

        output: list[tuple[int, dict[str, Any]]] = []
        classification = Counter()
        source_zero_faces = Counter()
        target_witness_depths = Counter()
        target_witness_grids = Counter()
        derivative_cells = Counter()
        derivative_depths = Counter()
        empty_signs = Counter()
        empty_methods = Counter()
        invalid_sheet_members: set[str] = set()
        invalid_side_members: set[str] = set()
        surviving_empty_side_members: set[str] = set()
        positive_sheet_members: set[str] = set()
        positive_side_members: set[str] = set()

        for source_ordinal, source in enumerate(r235_rows):
            frontier_ordinal, frontier = frontier_index[source["Round234_frontier_row_id"]]
            graph_ordinal, graph = graph_by_id[source["endpoint_graph_partition_row_id"]]
            graph_row_id = graph["Round306B1G0_graph_source_inventory_row_id"]
            need(graph["graph_family"] == "R235_SINGLE_ENDPOINT_GRAPH" and graph["endpoint_factor"] == source["active_endpoint_factor"], "R235 graph join")
            sheet = sheet_by_graph[graph_row_id]
            graph_sides = sorted(sides_by_graph[graph_row_id], key=lambda item: item[1]["side_role"])
            need(len(graph_sides) in {1, 2}, "R235 side count")
            input_commitment = {"R235_partition_row": row_ref(source_ordinal, source, "endpoint_graph_partition_row_id"), "R234_frontier_row": row_ref(frontier_ordinal, frontier, "frontier_row_id"), "B1G0_graph_row": closed_ref(graph_ordinal, graph, "Round306B1G0_graph_source_inventory_row_id"), "B1G0_sheet_row": closed_ref(*sheet, "Round306B1G0_graph_sheet_join_row_id"), "B1G0_side_rows": [closed_ref(*item, "Round306B1G0_graph_side_join_row_id") for item in graph_sides]}
            domain = {"coordinate_parameter": "TPS", "box": frontier["box"], "half_open_owner_lineage": "R234_DEPTH6_FRONTIER"}
            if source["active_endpoint_factor"] == "source":
                axis, wall = endpoint_spec(frontier)
                t0, t1 = map(Q, frontier["box"][:2])
                need(wall == 0 and ((axis == "X" and frontier["chart"][-1] in "NS") or (axis == "Y" and frontier["chart"][-1] in "EW")), "source exact factor")
                need((t0 == 0) ^ (t1 == 0) and source["active_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE", "source zero face")
                zero_face = "LOWER" if t0 == 0 else "UPPER"
                source_zero_faces[zero_face] += 1
                semantic = {"classification": "POSITIVE_GRAPH", "kernel": "EXACT_SOURCE_COORDINATE_MINUS_ZERO_EQUALS_9_OVER_25_TIMES_T", "complete_parameter_domain": domain, "source_factor_ast": {"op": "MUL", "args": [{"op": "CONST_Q", "value": qwire(Q(9, 25))}, {"op": "VAR", "name": "t"}]}, "strict_t_derivative_exact": qwire(Q(9, 25)), "zero_face": zero_face, "zero_set": "EXACT_T_EQUALS_ZERO_FACE_TIMES_FULL_P_S_BASE", "exact_positive_base_area": qwire((Q(frontier["box"][3]) - Q(frontier["box"][2])) * (Q(frontier["box"][5]) - Q(frontier["box"][4]))), "graph_local_dimension": 2, "graph_definition_credit": 1}
                classification["R235_SOURCE_POSITIVE"] += 1
            else:
                need(owner_xy(frontier["owner_target"])[0] == "G", "target G owner")
                need(len(graph_sides) == 2 and {item[1]["side_role"] for item in graph_sides} == {"EVENT_ABSENT", "EVENT_PRESENT"}, "R235 target side roles")
                derivative = strict_target_derivative(frontier, source["active_factor_strict_t_derivative_sign"])
                derivative_cells[derivative["proof_cell_count"]] += 1
                derivative_depths[derivative["maximum_split_depth"]] += 1
                empty = empty_target_proof(frontier, source["active_factor_strict_t_derivative_sign"])
                if empty is None:
                    witness = positive_target_witness(frontier, source["active_factor_strict_t_derivative_sign"])
                    target_witness_depths[witness["witness_shrink_depth"]] += 1
                    target_witness_grids[witness["witness_locator_grid_denominator"]] += 1
                    semantic = {"classification": "POSITIVE_GRAPH", "kernel": "G_TARGET_FIRST_HIT_COORDINATE_MINUS_INTEGER_WALL_V1", "kernel_parameters": {"source_chart": frontier["chart"], "target_owner": frontier["owner_target"], "wall_axis": endpoint_spec(frontier)[0], "integer_wall": endpoint_spec(frontier)[1], "source_radius": qwire(Q(9, 25)), "target_radius": qwire(Q(9, 25))}, "complete_parameter_domain": domain, "strict_t_derivative_proof": derivative, "exact_graph_base_domain": "BASE_POINTS_WHERE_ORIENTED_T_FACE_SIGNS_OPPOSE_OR_TOUCH", "positive_base_witness": witness, "graph_local_dimension": 2, "graph_definition_credit": 1}
                    classification["R235_TARGET_POSITIVE"] += 1
                else:
                    factor_sign, proof = empty
                    empty_signs[factor_sign] += 1
                    empty_methods[proof["method"]] += 1
                    fixed_source_sign = source["fixed_endpoint_factor_sign"]
                    need(fixed_source_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, "fixed source sign")
                    surviving_role = "EVENT_ABSENT" if factor_sign == fixed_source_sign else "EVENT_PRESENT"
                    side_index = {item[1]["side_role"]: item for item in graph_sides}
                    surviving_side = side_index[surviving_role]
                    invalid_side = side_index["EVENT_PRESENT" if surviving_role == "EVENT_ABSENT" else "EVENT_ABSENT"]
                    invalid_sheet_members.add(sheet[1]["sheet_member_id"])
                    invalid_side_members.add(invalid_side[1]["side_member_id"])
                    surviving_empty_side_members.add(surviving_side[1]["side_member_id"])
                    semantic = {"classification": "EMPTY_GRAPH", "kernel": "G_TARGET_FIRST_HIT_COORDINATE_MINUS_INTEGER_WALL_V1", "kernel_parameters": {"source_chart": frontier["chart"], "target_owner": frontier["owner_target"], "wall_axis": endpoint_spec(frontier)[0], "integer_wall": endpoint_spec(frontier)[1], "source_radius": qwire(Q(9, 25)), "target_radius": qwire(Q(9, 25))}, "complete_parameter_domain": domain, "strict_t_derivative_proof": derivative, "fixed_factor_sign_on_complete_domain": factor_sign, "empty_graph_proof": proof, "graph_definition_disposition_credit": 1, "invalid_sheet_member_candidate": sheet[1]["sheet_member_id"], "invalid_side_member_candidate": invalid_side[1]["side_member_id"], "invalid_side_role": invalid_side[1]["side_role"], "surviving_side_member": surviving_side[1]["side_member_id"], "surviving_side_role": surviving_side[1]["side_role"], "fresh_DSU_application_credit": 0}
                    classification["R235_TARGET_EMPTY"] += 1
            if semantic["classification"] == "POSITIVE_GRAPH":
                positive_sheet_members.add(sheet[1]["sheet_member_id"])
                positive_side_members.update(item[1]["side_member_id"] for item in graph_sides)
            core = {"schema": ROW_SCHEMA, "semantic_row_id": PREFIX + ":" + objsha([graph_row_id, semantic["classification"]]), "graph_inventory_ordinal": graph_ordinal, "graph_inventory_row_id": graph_row_id, "graph_id": graph["graph_id"], "graph_family": graph["graph_family"], "canonical_input_commitment": input_commitment, "canonical_input_commitment_sha256": objsha(input_commitment), "semantic_classification": semantic, "strict_nonpromotion": {"physical_incidence": 0, "representation_pullback": 0, "one_sided_trace": 0, "normalized_support": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0}}
            core["row_sha256"] = objsha(core)
            output.append((graph_ordinal, core))

        for c4_ordinal, bridge in enumerate(c4_rows):
            reference = bridge["canonical_input_commitment"]["B1G0_source_graph_row"]
            graph_ordinal, graph = reference[0], graphs[reference[0]]
            need(graph["Round306B1G0_graph_source_inventory_row_id"] == reference[1] and graph["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH" and graph["endpoint_factor"] == "source", "C4 source graph")
            sheet = sheet_by_graph[reference[1]]
            graph_sides = sorted(sides_by_graph[reference[1]], key=lambda item: item[1]["side_role"])
            need(len(graph_sides) == 2, "C4 source sides")
            semantic_source = bridge["semantic_reconstruction"]
            need(semantic_source["source_zero_set"] == "EXACT_FACE_GRAPH_t_EQUALS_0" and semantic_source["source_graph_dimension"] == 2, "C4 source theorem")
            input_commitment = {"C4_bridge_row": row_ref(c4_ordinal, bridge, "bridge_row_id"), "B1G0_graph_row": closed_ref(graph_ordinal, graph, "Round306B1G0_graph_source_inventory_row_id"), "B1G0_sheet_row": closed_ref(*sheet, "Round306B1G0_graph_sheet_join_row_id"), "B1G0_side_rows": [closed_ref(*item, "Round306B1G0_graph_side_join_row_id") for item in graph_sides]}
            semantic = {"classification": "POSITIVE_GRAPH", "kernel": "SEALED_C4_R235D_SOURCE_EXACT_FACE_GRAPH_BRIDGE", "C4_source_semantic_commitment_sha256": objsha(semantic_source), "source_zero_set": semantic_source["source_zero_set"], "source_graph_dimension": semantic_source["source_graph_dimension"], "graph_definition_credit": 1}
            positive_sheet_members.add(sheet[1]["sheet_member_id"])
            positive_side_members.update(item[1]["side_member_id"] for item in graph_sides)
            classification["R235D_SOURCE_POSITIVE"] += 1
            core = {"schema": ROW_SCHEMA, "semantic_row_id": PREFIX + ":" + objsha([reference[1], "POSITIVE_GRAPH"]), "graph_inventory_ordinal": graph_ordinal, "graph_inventory_row_id": reference[1], "graph_id": graph["graph_id"], "graph_family": graph["graph_family"], "canonical_input_commitment": input_commitment, "canonical_input_commitment_sha256": objsha(input_commitment), "semantic_classification": semantic, "strict_nonpromotion": {"physical_incidence": 0, "representation_pullback": 0, "one_sided_trace": 0, "normalized_support": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0}}
            core["row_sha256"] = objsha(core)
            output.append((graph_ordinal, core))

        for source_id, (source_ordinal, source) in r242_index.items():
            graph_ordinal, graph = graph_by_id[source_id]
            graph_row_id = graph["Round306B1G0_graph_source_inventory_row_id"]
            need(graph["graph_family"] == "R242_UNIQUE_TRANSITION_GRAPH", "R242 graph join")
            sheet = sheet_by_graph[graph_row_id]
            graph_sides = sorted(sides_by_graph[graph_row_id], key=lambda item: item[1]["side_role"])
            need(len(graph_sides) == 2 and source["unique_graph_point_for_every_closed_base_point"] is True and Q(source["exact_positive_base_projection_area"]) > 0, "R242 theorem")
            input_commitment = {"R242_positive_patch_row": closed_ref(source_ordinal, source, "transition_sheet_patch_row_id"), "B1G0_graph_row": closed_ref(graph_ordinal, graph, "Round306B1G0_graph_source_inventory_row_id"), "B1G0_sheet_row": closed_ref(*sheet, "Round306B1G0_graph_sheet_join_row_id"), "B1G0_side_rows": [closed_ref(*item, "Round306B1G0_graph_side_join_row_id") for item in graph_sides]}
            semantic = {"classification": "POSITIVE_GRAPH", "kernel": "SEALED_R242_UNIQUE_TRANSITION_GRAPH_PATCH_BRIDGE", "equation": source["equation"], "parameterization": source["parameterization"], "closed_witness_box": source["closed_witness_box"], "exact_positive_base_projection_area": source["exact_positive_base_projection_area"], "strict_t_derivative_sign": source["strict_t_derivative_sign"], "lower_t_face_F_sign": source["lower_t_face_F_sign"], "upper_t_face_F_sign": source["upper_t_face_F_sign"], "graph_local_dimension": 2, "graph_definition_credit": 1}
            positive_sheet_members.add(sheet[1]["sheet_member_id"])
            positive_side_members.update(item[1]["side_member_id"] for item in graph_sides)
            classification["R242_POSITIVE"] += 1
            core = {"schema": ROW_SCHEMA, "semantic_row_id": PREFIX + ":" + objsha([graph_row_id, "POSITIVE_GRAPH"]), "graph_inventory_ordinal": graph_ordinal, "graph_inventory_row_id": graph_row_id, "graph_id": graph["graph_id"], "graph_family": graph["graph_family"], "canonical_input_commitment": input_commitment, "canonical_input_commitment_sha256": objsha(input_commitment), "semantic_classification": semantic, "strict_nonpromotion": {"physical_incidence": 0, "representation_pullback": 0, "one_sided_trace": 0, "normalized_support": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0}}
            core["row_sha256"] = objsha(core)
            output.append((graph_ordinal, core))

        output.sort(key=lambda item: item[0])
        rows = [row for _, row in output]
        need([row["graph_inventory_ordinal"] for row in rows] == sorted(row["graph_inventory_ordinal"] for row in rows), "ordered graph inventory")
        need(len(rows) == 38_608 and len({row["graph_inventory_row_id"] for row in rows}) == 38_608, "surviving graph exhaustion")
        need(classification == {"R235_SOURCE_POSITIVE": 552, "R235_TARGET_POSITIVE": 4_432, "R235_TARGET_EMPTY": 33_344, "R235D_SOURCE_POSITIVE": 16, "R242_POSITIVE": 264}, "classification census")
        need(target_witness_grids == {128: 4_384, 4096: 48}, "target witness grid census")
        need(len(invalid_sheet_members) == len(invalid_side_members) == len(surviving_empty_side_members) == 33_344, "invalid member census")
        need(invalid_sheet_members.isdisjoint(invalid_side_members | positive_sheet_members | positive_side_members | surviving_empty_side_members), "invalid sheet disjoint")
        need(invalid_side_members.isdisjoint(positive_side_members | surviving_empty_side_members), "invalid side disjoint")
        need(len(positive_sheet_members) == 5_264 and len(positive_side_members) == 10_128, "positive member census")
        need(sum(derivative_cells.values()) == 37_776 and sum(derivative_depths.values()) == 37_776, "target derivative census")
        need(sum(empty_signs.values()) == sum(empty_methods.values()) == 33_344, "empty proof census")

        ledger_wire, plain = gzip_rows(rows)
        ledger = {"filename": LEDGER_NAME, "compression": "gzip-level9-mtime-zero", "row_schema": ROW_SCHEMA, "row_count": len(rows), "compressed_size": len(ledger_wire), "compressed_sha256": hashlib.sha256(ledger_wire).hexdigest(), "uncompressed_size": len(plain), "uncompressed_sha256": hashlib.sha256(plain).hexdigest(), "ordered_row_ids_sha256": sequence_sha(row["semantic_row_id"] for row in rows), "ordered_row_hashes_sha256": sequence_sha(row["row_sha256"] for row in rows), "ordered_rows_sha256": sequence_sha(rows)}
        body = {"schema": SCHEMA, "status": STATUS, "source_pins": [pin.__dict__ for pin in PINS], "upstream_seal_bindings": {}, "classification_census": dict(sorted(classification.items())), "semantic_effect": {"C3_graph_inventory_rows": 38_624, "C4_empty_R235D_target_graphs": 16, "C5_surviving_graph_rows_classified": 38_608, "positive_graph_definition_rows": 5_264, "new_empty_R235_target_graph_dispositions": 33_344, "total_empty_graph_dispositions_after_C4_C5": 33_360, "corrected_G2A_sheet_members_pending_fresh_DSU": 5_264, "corrected_G2B_side_incidence_references": 10_128, "corrected_G2B_side_distinct_members": 10_128, "corrected_physical_incidence_relation_denominator": 15_392, "corrected_G2_semantic_obligation_denominator": 20_656, "new_invalid_sheet_member_candidates": 33_344, "new_invalid_side_member_candidates": 33_344, "new_invalid_distinct_member_candidates": 66_688, "projected_member_universe_before_fresh_DSU": 497_772, "old_corrected_DSU_and_C1_C2_C3_component_bound_outputs_superseded": True}, "proof_histograms": {"source_zero_face": dict(sorted(source_zero_faces.items())), "target_positive_witness_shrink_depth": {str(key): value for key, value in sorted(target_witness_depths.items())}, "target_positive_witness_locator_grid": {str(key): value for key, value in sorted(target_witness_grids.items())}, "target_derivative_proof_cell_count": {str(key): value for key, value in sorted(derivative_cells.items())}, "target_derivative_maximum_split_depth": {str(key): value for key, value in sorted(derivative_depths.items())}, "empty_target_fixed_sign": dict(sorted(empty_signs.items())), "empty_target_parent_proof_method": dict(sorted(empty_methods.items()))}, "row_ledger": ledger, "scope": {"positive_graph_definition_credit": 5_264, "empty_graph_disposition_credit": 33_344, "member_invalidation_candidate_credit": 66_688, "fresh_DSU_credit": 0, "physical_incidence_credit": 0, "representation_pullback_credit": 0, "one_sided_trace_credit": 0, "normalized_support_credit": 0}, "required_next": {"seal_this_semantic_classification": True, "materialize_and_independently_verify_66688_member_invalidations": True, "recompute_fresh_DSU": True, "replay_C1_C2_C3_C4_and_all_later_component_bound_outputs": True, "B1A": "NOT_AUTHORIZED", "B2": "NOT_AUTHORIZED"}, "formal_credit": {"graph_definition": 5_264, "empty_graph_disposition": 33_344, "fresh_DSU": 0, "physical_incidence": 0, "representation_pullback": 0, "one_sided_trace": 0, "normalized_support": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0}, "CM2": "NO-GO_FOR_CLAIM"}
        body["upstream_seal_bindings"] = {"C3_manifest_sha256": pin_by_role["C3_MANIFEST"].sha256, "C4_manifest_sha256": pin_by_role["C4_MANIFEST"].sha256, "B1G0_manifest_sha256": pin_by_role["B1G0_MANIFEST"].sha256, "R234_manifest_sha256": pin_by_role["R234_MANIFEST"].sha256, "R235_manifest_sha256": pin_by_role["R235_MANIFEST"].sha256, "R242_manifest_sha256": pin_by_role["R242_MANIFEST"].sha256}
        result = {**body, "result_sha256": objsha(body)}
        snapshot.final()
        return result, ledger_wire



class CandidateFiles:
    def __init__(self, directory: Path, pinned: bool = True) -> None:
        self.directory = Path(os.path.abspath(directory))
        self.pinned = pinned
        self.dirfd = -1
        self.directory_identity: tuple[int, ...] = ()
        self.fds: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}
        self.raw: dict[str, bytes] = {}

    def __enter__(self) -> "CandidateFiles":
        resolved = self.directory.resolve()
        need(os.path.commonpath((str(resolved), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
        info = os.stat(self.directory, follow_symlinks=False)
        need(stat.S_ISDIR(info.st_mode), "candidate directory identity")
        self.dirfd = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        opened_directory = os.fstat(self.dirfd)
        need(identity(opened_directory) == identity(info), "candidate directory race")
        self.directory_identity = identity(opened_directory)
        need(set(os.listdir(self.dirfd)) == {RESULT_NAME, LEDGER_NAME}, "candidate exact set")
        expected = {RESULT_NAME: (CANDIDATE_RESULT_SIZE, CANDIDATE_RESULT_SHA256), LEDGER_NAME: (CANDIDATE_LEDGER_SIZE, CANDIDATE_LEDGER_SHA256)}
        for filename in (RESULT_NAME, LEDGER_NAME):
            before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "candidate identity:" + filename)
            fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            opened = os.fstat(fd)
            need(identity(opened) == identity(before), "candidate race:" + filename)
            first = hash_fd(fd)
            need(first == hash_fd(fd), "candidate digest stability:" + filename)
            os.lseek(fd, 0, os.SEEK_SET)
            blocks: list[bytes] = []
            while True:
                block = os.read(fd, 1_048_576)
                if not block:
                    break
                blocks.append(block)
            raw = b"".join(blocks)
            need(len(raw) == before.st_size and hashlib.sha256(raw).hexdigest() == first, "candidate read:" + filename)
            if self.pinned:
                need((len(raw), first) == expected[filename], "candidate pin:" + filename)
            self.fds[filename] = fd
            self.identities[filename] = identity(opened)
            self.raw[filename] = raw
        return self

    def final(self) -> None:
        for filename in (LEDGER_NAME, RESULT_NAME):
            fd = self.fds[filename]
            need(identity(os.fstat(fd)) == self.identities[filename], "candidate final fd:" + filename)
            need(identity(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.identities[filename], "candidate final path:" + filename)
            need(hash_fd(fd) == hashlib.sha256(self.raw[filename]).hexdigest(), "candidate final digest:" + filename)
        need(identity(os.fstat(self.dirfd)) == self.directory_identity, "candidate final directory fd")
        need(identity(os.stat(self.directory, follow_symlinks=False)) == self.directory_identity, "candidate final directory path")
        need(set(os.listdir(self.dirfd)) == {RESULT_NAME, LEDGER_NAME}, "candidate final exact set")

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            os.close(self.dirfd)


def decode_payloads(result_raw: bytes, ledger_raw: bytes) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    result = json.loads(result_raw)
    need(type(result) is dict and canonical(result) == result_raw, "candidate result canonical")
    body = dict(result)
    need(body.pop("result_sha256", None) == objsha(body), "candidate result closure")
    try:
        plain = gzip.decompress(ledger_raw)
    except Exception as error:
        raise Rejected("candidate ledger gzip") from error
    need(gzip.compress(plain, compresslevel=9, mtime=0) == ledger_raw and plain.endswith(b"\n"), "candidate deterministic gzip")
    rows: list[dict[str, Any]] = []
    for ordinal, line in enumerate(plain.splitlines()):
        row = json.loads(line)
        need(type(row) is dict and canonical(row) == line, "candidate row canonical:" + str(ordinal))
        row_body = dict(row)
        need(row_body.pop("row_sha256", None) == objsha(row_body), "candidate row closure:" + str(ordinal))
        need(row["schema"] == ROW_SCHEMA and row["graph_inventory_ordinal"] >= 0, "candidate row identity:" + str(ordinal))
        rows.append(row)
    need(len(rows) == 38_608, "candidate row census")
    return result, rows


def compare_payloads(result_raw: bytes, ledger_raw: bytes, expected_result: dict[str, Any], expected_ledger: bytes) -> dict[str, Any]:
    candidate_result, candidate_rows = decode_payloads(result_raw, ledger_raw)
    need(ledger_raw == expected_ledger, "candidate ledger exact comparator")
    need(result_raw == canonical(expected_result) and candidate_result == expected_result, "candidate result exact comparator")
    return {"status": "PASS_INDEPENDENT_38608_ROW_CORRECTED_G2_GRAPH_SEMANTIC_REPLAY__FRESH_DSU_REQUIRED", "candidate_result_file_sha256": hashlib.sha256(result_raw).hexdigest(), "candidate_ledger_file_sha256": hashlib.sha256(ledger_raw).hexdigest(), "result_sha256": candidate_result["result_sha256"], "row_count": len(candidate_rows), "positive_graph_definition_rows": 5_264, "empty_graph_disposition_rows": 33_344, "new_invalid_distinct_member_candidates": 66_688, "projected_member_universe_before_fresh_DSU": 497_772, "producer_imported_or_executed_or_parsed": False, "formal_credit": candidate_result["formal_credit"], "CM2": "NO-GO_FOR_CLAIM"}


def replay_directory(directory: Path, pinned: bool = True, expected: tuple[dict[str, Any], bytes] | None = None) -> tuple[dict[str, Any], dict[str, bytes]]:
    expected_result, expected_ledger = build() if expected is None else expected
    with CandidateFiles(directory, pinned=pinned) as candidate:
        receipt = compare_payloads(candidate.raw[RESULT_NAME], candidate.raw[LEDGER_NAME], expected_result, expected_ledger)
        candidate.final()
        return receipt, dict(candidate.raw)


def publish_bytes(name: str, raw: bytes) -> None:
    fd = os.open(ROOT / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        offset = 0
        while offset < len(raw):
            offset += os.write(fd, raw[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)
    info = os.stat(ROOT / name, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(raw), "published:" + name)


def promote(directory: Path) -> dict[str, Any]:
    expected = build()
    with CandidateFiles(directory) as candidate:
        receipt = compare_payloads(candidate.raw[RESULT_NAME], candidate.raw[LEDGER_NAME], *expected)
        raw = dict(candidate.raw)
        publish_bytes(LEDGER_NAME, raw[LEDGER_NAME])
        publish_bytes(RESULT_NAME, raw[RESULT_NAME])
        candidate.final()
    for filename in (RESULT_NAME, LEDGER_NAME):
        info = os.stat(ROOT / filename, follow_symlinks=False)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == hashlib.sha256(raw[filename]).hexdigest(), "reverse promotion verification:" + filename)
    return {**receipt, "status": "PASS_CANDIDATE_PROMOTED_LEDGER_FIRST_RESULT_LAST_WITH_REVERSE_IDENTITY_NLINK_SHA256_VERIFICATION"}


def verifier_sha256() -> str:
    path = Path(__file__)
    before = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "verifier identity")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        need(identity(os.fstat(fd)) == identity(before), "verifier race")
        value = hash_fd(fd)
        need(value == hash_fd(fd), "verifier digest stability")
        return value
    finally:
        os.close(fd)


def mutate_result(path: Path, mutation: Any) -> None:
    value = json.loads(path.read_bytes())
    mutation(value)
    body = dict(value)
    body.pop("result_sha256", None)
    path.write_bytes(canonical({**body, "result_sha256": objsha(body)}))


def mutate_first_ledger_row(directory: Path, mutation: Any) -> None:
    ledger_path = directory / LEDGER_NAME
    plain = gzip.decompress(ledger_path.read_bytes())
    lines = plain.splitlines()
    need(len(lines) == 38_608, "attack ledger row census")
    first = json.loads(lines[0])
    mutation(first)
    first_body = dict(first)
    first_body.pop("row_sha256", None)
    first = {**first_body, "row_sha256": objsha(first_body)}
    lines[0] = canonical(first)
    mutated_plain = b"\n".join(lines) + b"\n"
    mutated_ledger = gzip.compress(mutated_plain, compresslevel=9, mtime=0)
    rows = [json.loads(line) for line in lines]
    ledger_path.write_bytes(mutated_ledger)
    result_path = directory / RESULT_NAME
    result = json.loads(result_path.read_bytes())
    result["row_ledger"] = {
        "filename": LEDGER_NAME,
        "compression": "gzip-level9-mtime-zero",
        "row_schema": ROW_SCHEMA,
        "row_count": len(rows),
        "compressed_size": len(mutated_ledger),
        "compressed_sha256": hashlib.sha256(mutated_ledger).hexdigest(),
        "uncompressed_size": len(mutated_plain),
        "uncompressed_sha256": hashlib.sha256(mutated_plain).hexdigest(),
        "ordered_row_ids_sha256": sequence_sha(row["semantic_row_id"] for row in rows),
        "ordered_row_hashes_sha256": sequence_sha(row["row_sha256"] for row in rows),
        "ordered_rows_sha256": sequence_sha(rows),
    }
    body = dict(result)
    body.pop("result_sha256", None)
    result_path.write_bytes(canonical({**body, "result_sha256": objsha(body)}))


def coherent_attacks(candidate_directory: Path) -> dict[str, Any]:
    expected = build()
    baseline, _ = replay_directory(candidate_directory, expected=expected)
    work = Path(tempfile.mkdtemp(prefix="cm2-c5-g2-classification-attacks-"))
    attacks: list[dict[str, Any]] = []

    def restore() -> None:
        for path in work.iterdir():
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
        shutil.copyfile(candidate_directory / RESULT_NAME, work / RESULT_NAME)
        shutil.copyfile(candidate_directory / LEDGER_NAME, work / LEDGER_NAME)

    def execute(attack_id: str, mutation: Any, cleanup: Any | None = None) -> None:
        restore()
        rejection = None
        try:
            mutation()
            replay_directory(work, pinned=False, expected=expected)
        except (Rejected, OSError, EOFError, json.JSONDecodeError, KeyError, ValueError) as error:
            rejection = type(error).__name__ + ":" + str(error)
        finally:
            if cleanup is not None:
                cleanup()
        need(rejection is not None, "attack accepted:" + attack_id)
        body = {"attack_id": attack_id, "rejected": True, "rejection_boundary": rejection}
        attacks.append({**body, "row_sha256": objsha(body)})

    try:
        execute("A01_EXTRA_FILE", lambda: (work / "foreign").write_bytes(b"x"))
        execute("A02_MISSING_RESULT", lambda: (work / RESULT_NAME).unlink())
        execute("A03_MISSING_LEDGER", lambda: (work / LEDGER_NAME).unlink())
        execute("A04_SYMLINK_RESULT", lambda: ((work / RESULT_NAME).unlink(), (work / RESULT_NAME).symlink_to(candidate_directory / RESULT_NAME)))
        hard_target = work.parent / (work.name + "-hard-target")

        def hardlink_ledger() -> None:
            (work / LEDGER_NAME).unlink()
            shutil.copyfile(candidate_directory / LEDGER_NAME, hard_target)
            os.link(hard_target, work / LEDGER_NAME)

        execute("A05_HARDLINK_LEDGER", hardlink_ledger, lambda: hard_target.unlink(missing_ok=True))
        execute("A06_POSITIVE_GRAPH_DENOMINATOR", lambda: mutate_result(work / RESULT_NAME, lambda value: value["semantic_effect"].__setitem__("positive_graph_definition_rows", 5_265)))
        execute("A07_INVALID_MEMBER_DENOMINATOR", lambda: mutate_result(work / RESULT_NAME, lambda value: value["semantic_effect"].__setitem__("new_invalid_distinct_member_candidates", 66_687)))
        execute("A08_FRESH_DSU_INJECTION", lambda: mutate_result(work / RESULT_NAME, lambda value: value["formal_credit"].__setitem__("fresh_DSU", 1)))
        execute("A09_INCIDENCE_INJECTION", lambda: mutate_result(work / RESULT_NAME, lambda value: value["formal_credit"].__setitem__("physical_incidence", 1)))
        execute("A10_NORMALIZED_SUPPORT_INJECTION", lambda: mutate_result(work / RESULT_NAME, lambda value: value["formal_credit"].__setitem__("normalized_support", 1)))
        execute("A11_SOURCE_PIN_SUBSTITUTION", lambda: mutate_result(work / RESULT_NAME, lambda value: value["source_pins"][0].__setitem__("sha256", "0" * 64)))
        execute("A12_NONCANONICAL_RESULT", lambda: (work / RESULT_NAME).write_bytes((work / RESULT_NAME).read_bytes() + b"\n"))
        execute("A13_LEDGER_TRAILING_GARBAGE", lambda: (work / LEDGER_NAME).write_bytes((work / LEDGER_NAME).read_bytes() + b"x"))
        execute("A14_LEDGER_TRUNCATION", lambda: (work / LEDGER_NAME).write_bytes((work / LEDGER_NAME).read_bytes()[:-1]))

        def corrupt_ledger() -> None:
            raw = bytearray((work / LEDGER_NAME).read_bytes())
            raw[len(raw) // 2] ^= 1
            (work / LEDGER_NAME).write_bytes(raw)

        execute("A15_LEDGER_COMPRESSED_BYTE_CORRUPTION", corrupt_ledger)
        execute("A16_RECLOSED_ROW_SEMANTIC_MUTATION", lambda: mutate_first_ledger_row(work, lambda row: row["strict_nonpromotion"].__setitem__("normalized_support", 1)))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    need(len(attacks) == 16, "attack census")
    body = {
        "schema": SCHEMA + ".coherent-attack-suite.v1",
        "status": "PASS_16_OF_16_COHERENT_ATTACKS_REJECTED",
        "verifier_filename": VERIFIER_NAME,
        "verifier_file_sha256": verifier_sha256(),
        "attack_count": 16,
        "rejected_count": 16,
        "all_rejected": True,
        "baseline_result_file_sha256": baseline["candidate_result_file_sha256"],
        "baseline_ledger_file_sha256": baseline["candidate_ledger_file_sha256"],
        "attacks": attacks,
    }
    return {**body, "attack_suite_sha256": objsha(body)}


def closed_json(raw: bytes, closure: str, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) == raw, "closed JSON canonical:" + label)
    body = dict(value)
    need(body.pop(closure, None) == objsha(body), "closed JSON closure:" + label)
    return value


def verification_document(receipt: dict[str, Any], attack_raw: bytes | None = None) -> dict[str, Any]:
    raw = (ROOT / ATTACK_NAME).read_bytes() if attack_raw is None else attack_raw
    suite = closed_json(raw, "attack_suite_sha256", "attack suite")
    need(suite["verifier_file_sha256"] == verifier_sha256(), "attack verifier binding")
    need((suite["attack_count"], suite["rejected_count"], suite["all_rejected"]) == (16, 16, True), "attack suite census")
    body = {
        "schema": SCHEMA + ".verification.v1",
        **receipt,
        "attack_suite": {
            "filename": ATTACK_NAME,
            "file_sha256": hashlib.sha256(raw).hexdigest(),
            "object_self_sha256": suite["attack_suite_sha256"],
            "attack_count": 16,
            "rejected_count": 16,
            "all_rejected": True,
        },
        "formal_credit_marker": {
            "graph_definition": 5_264,
            "empty_graph_disposition": 33_344,
            "fresh_DSU": 0,
            "normalized_support": 0,
            "B1A": 0,
            "B2": 0,
            "CM2": 0,
        },
    }
    return {**body, "verification_sha256": objsha(body)}


class ManifestPackage:
    def __init__(self) -> None:
        self.dirfd = -1
        self.manifest_fd = -1
        self.manifest_identity: tuple[int, ...] = ()
        self.fds: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}
        self.hashes: dict[str, str] = {}

    def __enter__(self) -> "ManifestPackage":
        self.dirfd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        before = os.stat(MANIFEST_NAME, dir_fd=self.dirfd, follow_symlinks=False)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "manifest identity")
        self.manifest_fd = os.open(MANIFEST_NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
        opened = os.fstat(self.manifest_fd)
        need(identity(opened) == identity(before), "manifest race")
        self.manifest_identity = identity(opened)
        os.lseek(self.manifest_fd, 0, os.SEEK_SET)
        raw = os.read(self.manifest_fd, before.st_size)
        lines = raw.decode("ascii").splitlines()
        need(raw.endswith(b"\n") and len(lines) == len(PACKAGE_MEMBERS), "manifest structure")
        for line, filename in zip(lines, PACKAGE_MEMBERS, strict=True):
            declared_hash, declared_name = line.split("  ")
            need(declared_name == filename and len(declared_hash) == 64, "manifest order:" + filename)
            info = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "manifest member identity:" + filename)
            fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            member = os.fstat(fd)
            need(identity(member) == identity(info) and hash_fd(fd) == hash_fd(fd) == declared_hash, "manifest member digest:" + filename)
            self.fds[filename] = fd
            self.identities[filename] = identity(member)
            self.hashes[filename] = declared_hash
        return self

    def read(self, filename: str) -> bytes:
        fd = self.fds[filename]
        os.lseek(fd, 0, os.SEEK_SET)
        return os.read(fd, self.identities[filename][4])

    def final(self) -> None:
        for filename in reversed(PACKAGE_MEMBERS):
            need(identity(os.fstat(self.fds[filename])) == self.identities[filename], "manifest final fd:" + filename)
            need(identity(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.identities[filename], "manifest final path:" + filename)
            need(hash_fd(self.fds[filename]) == self.hashes[filename], "manifest final digest:" + filename)
        need(identity(os.fstat(self.manifest_fd)) == self.manifest_identity, "manifest final fd")
        need(identity(os.stat(MANIFEST_NAME, dir_fd=self.dirfd, follow_symlinks=False)) == self.manifest_identity, "manifest final path")

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.manifest_fd >= 0:
            os.close(self.manifest_fd)
        if self.dirfd >= 0:
            os.close(self.dirfd)


def manifest_first_replay() -> dict[str, Any]:
    with ManifestPackage() as package:
        need(package.hashes[VERIFIER_NAME] == verifier_sha256(), "manifest verifier binding")
        expected = build()
        receipt = compare_payloads(package.read(RESULT_NAME), package.read(LEDGER_NAME), *expected)
        need(package.read(VERIFICATION_NAME) == canonical(verification_document(receipt, package.read(ATTACK_NAME))), "manifest verification byte identity")
        package.final()
    return {
        "status": "PASS_MANIFEST_FIRST_HELD_FD_38608_ROW_CORRECTED_G2_GRAPH_SEMANTIC_REPLAY__ZERO_WRITES",
        "manifest_filename": MANIFEST_NAME,
        "manifest_member_count": len(PACKAGE_MEMBERS),
        "result_sha256": receipt["result_sha256"],
        "positive_graph_definition_rows": 5_264,
        "empty_graph_disposition_rows": 33_344,
        "new_invalid_distinct_member_candidates": 66_688,
        "deliverables_write_syscalls": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-dir")
    parser.add_argument("--verify-no-write", action="store_true")
    parser.add_argument("--promote", action="store_true")
    parser.add_argument("--attack-publish", action="store_true")
    parser.add_argument("--verify-publish", action="store_true")
    parser.add_argument("--manifest-first-no-write", action="store_true")
    args = parser.parse_args()
    need(sum((args.verify_no_write, args.promote, args.attack_publish, args.verify_publish, args.manifest_first_no_write)) == 1, "exactly one mode")
    if args.manifest_first_no_write:
        result = manifest_first_replay()
    else:
        need(args.candidate_dir is not None, "candidate required")
        candidate_directory = Path(args.candidate_dir)
        if args.promote:
            result = promote(candidate_directory)
        elif args.attack_publish:
            suite = coherent_attacks(candidate_directory)
            publish_bytes(ATTACK_NAME, canonical(suite))
            result = {"status": suite["status"], "attack_count": 16, "attack_suite_sha256": suite["attack_suite_sha256"]}
        else:
            receipt, _ = replay_directory(candidate_directory)
            result = receipt
            if args.verify_publish:
                publish_bytes(VERIFICATION_NAME, canonical(verification_document(receipt)))
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
