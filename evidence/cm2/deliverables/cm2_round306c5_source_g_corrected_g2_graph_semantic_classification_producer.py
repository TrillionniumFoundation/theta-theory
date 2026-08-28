#!/usr/bin/env python3
"""Classify every surviving G2 graph root by executable semantics."""

from __future__ import annotations

import argparse
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
import stat
import sys
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
        for pin in PINS:
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
        for pin in reversed(PINS):
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


def write_once(directory: Path, name: str, data: bytes) -> None:
    path = directory / name
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        written = 0
        while written < len(data):
            written += os.write(fd, data[written:])
        os.fsync(fd)
    finally:
        os.close(fd)
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(data), "published file:" + name)


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-result", action="store_true")
    parser.add_argument("--candidate-dir")
    args = parser.parse_args()
    need(args.print_result != (args.candidate_dir is not None), "exactly one mode")
    result, ledger_wire = build()
    result_wire = canonical(result)
    if args.print_result:
        sys.stdout.buffer.write(result_wire + b"\n")
    else:
        directory = Path(args.candidate_dir).resolve()
        need(os.path.commonpath((str(directory), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
        directory.mkdir(mode=0o700, exist_ok=False)
        write_once(directory, LEDGER_NAME, ledger_wire)
        write_once(directory, RESULT_NAME, result_wire)
        print(json.dumps({"status": result["status"], "result_filename": RESULT_NAME, "result_size": len(result_wire), "result_file_sha256": hashlib.sha256(result_wire).hexdigest(), "result_sha256": result["result_sha256"], "ledger_filename": LEDGER_NAME, "ledger_size": len(ledger_wire), "ledger_sha256": hashlib.sha256(ledger_wire).hexdigest()}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
