#!/usr/bin/env python3
"""Audit fresh G2 relation admissibility and legacy support-envelope scope."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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
from typing import Any, Final


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit"
RESULT_NAME: Final = PREFIX + "_result.json"
GRAPH_LEDGER_NAME: Final = PREFIX + "_graph_domain_audit_ledger.jsonl.gz"
RELATION_LEDGER_NAME: Final = PREFIX + "_relation_disposition_ledger.jsonl.gz"
SCHEMA: Final = "cm2.round306c9.source-g-g2-relation-admissibility-and-envelope-audit.v1"
GRAPH_ROW_SCHEMA: Final = SCHEMA + ".graph-domain-audit-row.v1"
RELATION_ROW_SCHEMA: Final = SCHEMA + ".relation-disposition-row.v1"
STATUS: Final = "PASS_5264_GRAPH_DOMAIN_AUDITS__15392_MECHANICAL_RELATION_DISPOSITIONS__15382_POSITIVE_GRAPH_RELATION_CANDIDATES__10_EMPTY_GRAPH_NO_INCIDENCE__ZERO_SUPPORT_CREDIT"
SQRT_BITS: Final = 160
OWNER_RE: Final = re.compile(r"^([GW])\[(-?[0-9]+),(-?[0-9]+)\]$")

C8_MANIFEST: Final = "cm2_round306c8_source_g_fresh_full_support_authority_frontier_manifest.sha256"
C8_FRONTIER: Final = "cm2_round306c8_source_g_fresh_full_support_authority_frontier.json"
C7_MANIFEST: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_manifest.sha256"
C7_RESULT: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_result.json"
C7_PHYSICAL: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_physical_incidence_statement_ledger.jsonl.gz"
C7_GAPS: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_semantic_gap_ledger.jsonl.gz"
C5_MANIFEST: Final = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_manifest.sha256"
C5_RESULT: Final = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_result.json"
C5_LEDGER: Final = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz"
C4_MANIFEST: Final = "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_manifest.sha256"
C4_LEDGER: Final = "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz"
R234_MANIFEST: Final = "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_manifest.sha256"
R234_CERT: Final = "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"
R248_MANIFEST: Final = "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256"
R248_CERT: Final = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("C8_MANIFEST", C8_MANIFEST, 998, "fb712d98c4a7c13185778f62381f04d75546b7f20ab322c9eac667b1e80883a1"),
    Pin("C8_FRONTIER", C8_FRONTIER, 98_772, "1ec052ba9a6c26929d3a8242f3d12f405640f6399c331977acf51a315e201792"),
    Pin("C7_MANIFEST", C7_MANIFEST, 2_184, "4e534e412a760d13fe7eb278ca063e86ac2a7164bbfdb3b14a3142219267c0c6"),
    Pin("C7_RESULT", C7_RESULT, 10_231, "497838e082d7e48dc1a28d9da829b78bd20e39827d1d54815400ec8d3e78abee"),
    Pin("C7_PHYSICAL", C7_PHYSICAL, 9_771_275, "e6450435f74f038f3de2ada64935fc1f72bec6eb4323f2dc5ad8069bf3ea490e"),
    Pin("C7_GAPS", C7_GAPS, 4_483_110, "1d02b2f36e7e701d8e11821d3f575e474ccb99cb43d839bbb3ec14ef17fdd4bc"),
    Pin("C5_MANIFEST", C5_MANIFEST, 1_193, "aefe82ef88c2ddf5f241d76e0f0f7483e230d68219ace6639f7389adbcb14134"),
    Pin("C5_RESULT", C5_RESULT, 6_975, "0da7931e1a46d68ae8da69a7de1534a3955c83a8d6f5d8ab0170be7a34dc6320"),
    Pin("C5_LEDGER", C5_LEDGER, 78_082_824, "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"),
    Pin("C4_MANIFEST", C4_MANIFEST, 1_177, "5550eb9cf4e474a8d08086062e28538e909f6e1c7e499ba10a78a2d24e683de6"),
    Pin("C4_LEDGER", C4_LEDGER, 101_147, "3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),
    Pin("R234_MANIFEST", R234_MANIFEST, 574, "f8714ecdf804657fc6633136544f567b07e7d8503095d17fcda19226feefc432"),
    Pin("R234_CERT", R234_CERT, 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    Pin("R248_MANIFEST", R248_MANIFEST, 885, "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07"),
    Pin("R248_CERT", R248_CERT, 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
)

ZERO_CREDIT: Final = {
    "normalized_support": 0,
    "representation_cover": 0,
    "A1_A2": 0,
    "physical_incidence": 0,
    "pullback_equivalence": 0,
    "one_sided_trace": 0,
    "transition": 0,
    "B1A": 0,
    "B2": 0,
    "maximality": 0,
    "fibre": 0,
    "global_disposition": 0,
    "CM2": 0,
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def hash_fd(file_descriptor: int) -> str:
    os.lseek(file_descriptor, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    while True:
        block = os.read(file_descriptor, 1_048_576)
        if not block:
            return digest.hexdigest()
        digest.update(block)


def read_fd(file_descriptor: int) -> bytes:
    os.lseek(file_descriptor, 0, os.SEEK_SET)
    blocks: list[bytes] = []
    while True:
        block = os.read(file_descriptor, 1_048_576)
        if not block:
            return b"".join(blocks)
        blocks.append(block)


class Snapshot:
    def __init__(self) -> None:
        self.directory_descriptor = -1
        self.file_descriptors: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "Snapshot":
        before = os.stat(ROOT, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not ROOT.is_symlink(), "deliverables directory")
        self.directory_descriptor = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for pin in PINS:
            info = os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == pin.size, "pin identity:" + pin.role)
            file_descriptor = os.open(pin.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.directory_descriptor)
            opened = os.fstat(file_descriptor)
            need(identity(opened) == identity(info), "pin race:" + pin.role)
            need(hash_fd(file_descriptor) == hash_fd(file_descriptor) == pin.sha256, "pin digest:" + pin.role)
            self.file_descriptors[pin.role] = file_descriptor
            self.identities[pin.role] = identity(opened)
        return self

    def read(self, role: str) -> bytes:
        return read_fd(self.file_descriptors[role])

    def duplicate(self, role: str) -> int:
        duplicate = os.dup(self.file_descriptors[role])
        os.lseek(duplicate, 0, os.SEEK_SET)
        return duplicate

    def final(self) -> None:
        for pin in reversed(PINS):
            file_descriptor = self.file_descriptors[pin.role]
            need(identity(os.fstat(file_descriptor)) == self.identities[pin.role], "final fd:" + pin.role)
            need(identity(os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)) == self.identities[pin.role], "final path:" + pin.role)
            need(hash_fd(file_descriptor) == pin.sha256, "final digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for file_descriptor in self.file_descriptors.values():
            try:
                os.close(file_descriptor)
            except OSError:
                pass
        if self.directory_descriptor >= 0:
            os.close(self.directory_descriptor)


def exact_document(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict and raw in (canonical(value), canonical(value) + b"\n"), "canonical document:" + label)
    body = dict(value)
    closure = None
    for candidate in ("result_sha256", "authority_frontier_sha256"):
        if candidate in body:
            closure = body.pop(candidate)
            break
    need(type(closure) is str and closure == object_sha(body), "document closure:" + label)
    return value


def json_document(snapshot: Snapshot, role: str) -> dict[str, Any]:
    value = json.loads(snapshot.read(role))
    need(type(value) is dict, "JSON document:" + role)
    return value


def jsonl_rows(snapshot: Snapshot, role: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    duplicate = snapshot.duplicate(role)
    try:
        with os.fdopen(duplicate, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            for ordinal, line in enumerate(stream):
                row = json.loads(line)
                need(type(row) is dict and line.endswith(b"\n") and line == canonical(row) + b"\n", "canonical JSONL:" + role + ":" + str(ordinal))
                body = dict(row)
                claimed = body.pop("row_sha256", None)
                need(type(claimed) is str and claimed == object_sha(body), "row closure:" + role + ":" + str(ordinal))
                rows.append(row)
        return rows
    finally:
        try:
            os.close(duplicate)
        except OSError:
            pass


def producer_record() -> dict[str, Any]:
    info = os.stat(__file__, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "producer identity")
    file_descriptor = os.open(__file__, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(file_descriptor)
        need(identity(opened) == identity(info), "producer race")
        digest = hash_fd(file_descriptor)
        need(digest == hash_fd(file_descriptor), "producer digest")
        return {"filename": Path(__file__).name, "size": info.st_size, "sha256": digest}
    finally:
        os.close(file_descriptor)


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
        right = other if type(other) is Interval else Interval.point(other)
        return Interval(self.lower + right.lower, self.upper + right.upper)

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval(-self.upper, -self.lower)

    def __sub__(self, other: Any) -> "Interval":
        return self + (-other)

    def __rsub__(self, other: Any) -> "Interval":
        return Interval.point(other) + (-self)

    def __mul__(self, other: Any) -> "Interval":
        right = other if type(other) is Interval else Interval.point(other)
        values = (self.lower * right.lower, self.lower * right.upper, self.upper * right.lower, self.upper * right.upper)
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def square(self) -> "Interval":
        values = (self.lower * self.lower, self.upper * self.upper)
        return Interval(Q(0) if self.lower <= 0 <= self.upper else min(values), max(values))

    def divide(self, other: Any) -> "Interval":
        right = other if type(other) is Interval else Interval.point(other)
        need(not right.lower <= 0 <= right.upper, "interval division")
        reciprocal = Interval(min(Q(1, right.lower), Q(1, right.upper)), max(Q(1, right.lower), Q(1, right.upper)))
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

    def floor_root(rational: Q) -> Q:
        return Q(isqrt((rational.numerator * scale * scale) // rational.denominator), scale)

    lower = floor_root(value.lower)
    upper = floor_root(value.upper)
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
        right = other if type(other) is Dual else Dual.constant(other)
        return Dual(self.value + right.value, self.derivative + right.derivative)

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other: Any) -> "Dual":
        return self + (-other)

    def __rsub__(self, other: Any) -> "Dual":
        return Dual.constant(other) + (-self)

    def __mul__(self, other: Any) -> "Dual":
        right = other if type(other) is Dual else Dual.constant(other)
        return Dual(self.value * right.value, self.derivative * right.value + self.value * right.derivative)

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
    return {"hit_x": hit_x, "hit_y": hit_y}


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
        if dual.derivative.sign() == expected:
            cells += 1
            maximum_depth = max(maximum_depth, depth)
            continue
        need(depth < 8, "target derivative unresolved")
        if depth % 2 == 0:
            middle = (pa + pb) / 2
            stack.extend(((ta, tb, pa, middle, depth + 1), (ta, tb, middle, pb, depth + 1)))
        else:
            middle = (ta + tb) / 2
            stack.extend(((ta, middle, pa, pb, depth + 1), (middle, tb, pa, pb, depth + 1)))
    return {"strict_t_derivative_sign": expected, "proof_cell_count": cells, "maximum_split_depth": maximum_depth}


def no_graph_endpoint(frontier: dict[str, Any]) -> dict[str, Any]:
    t0, t1, p0, p1, s0, s1 = map(Q, frontier["box"])
    for p_side, p_value in (("LOWER_P", p0), ("UPPER_P", p1)):
        lower = target_factor(frontier, (t0, t0), (p_value, p_value))
        upper = target_factor(frontier, (t1, t1), (p_value, p_value))
        need(type(lower) is Interval and type(upper) is Interval, "endpoint factors")
        lower_sign = lower.sign()
        upper_sign = upper.sign()
        if lower_sign == upper_sign and lower_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}:
            return {
                "p_endpoint": p_side,
                "p_value": qwire(p_value),
                "lower_t_face_factor_sign": lower_sign,
                "upper_t_face_factor_sign": upper_sign,
                "lower_t_face_factor_interval_sha256": object_sha(lower.wire()),
                "upper_t_face_factor_interval_sha256": object_sha(upper.wire()),
                "full_s_interval": [qwire(s0), qwire(s1)],
                "conclusion": "NO_GRAPH_POINT_FOR_THIS_BASE_ENDPOINT_AND_ANY_S",
            }
    raise Rejected("missing no-graph base endpoint")


def gzip_rows(rows: list[dict[str, Any]]) -> tuple[bytes, bytes]:
    plain = b"".join(canonical(row) + b"\n" for row in rows)
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=buffer, mtime=0) as stream:
        stream.write(plain)
    return buffer.getvalue(), plain


def sequence_sha(values: Any) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(canonical(value))
        digest.update(b"\n")
    return digest.hexdigest()


def ledger_descriptor(filename: str, row_schema: str, rows: list[dict[str, Any]], wire: bytes, plain: bytes) -> dict[str, Any]:
    return {
        "filename": filename,
        "compression": "gzip-level9-mtime-zero",
        "row_schema": row_schema,
        "row_count": len(rows),
        "compressed_size": len(wire),
        "compressed_sha256": hashlib.sha256(wire).hexdigest(),
        "uncompressed_size": len(plain),
        "uncompressed_sha256": hashlib.sha256(plain).hexdigest(),
        "ordered_row_ids_sha256": sequence_sha(row["row_id"] for row in rows),
        "ordered_row_hashes_sha256": sequence_sha(row["row_sha256"] for row in rows),
        "ordered_rows_sha256": sequence_sha(rows),
    }


def closed_row(core: dict[str, Any]) -> dict[str, Any]:
    return {**core, "row_sha256": object_sha(core)}


def validate_sources(c8: dict[str, Any], c7: dict[str, Any], c5: dict[str, Any]) -> None:
    need(c8["fresh_partition"]["member_count"] == 497_772 and c8["fresh_partition"]["component_count"] == 61_928, "C8 fresh base")
    need(c8["fresh_partition"]["physical_incidence_relation_count"] == 15_392 and all(value == 0 for value in c8["formal_credit"].values()), "C8 mechanical denominator")
    need(c8["migration_rules"]["outer_envelope_or_inner_witness_may_equal_full_support"] is False, "C8 envelope boundary")
    need(c7["fresh_census"]["physical_incidence_count"] == 15_392 and c7["fresh_census"]["semantic_gap_count"] == 15_392, "C7 relation census")
    need(c7["fresh_census"]["member_count"] == 497_772 and c7["fresh_census"]["representation_count"] == 545_184, "C7 fresh census")
    need(all(value == 0 for value in c7["formal_credit"].values()), "C7 zero credit")
    effect = c5["semantic_effect"]
    need(effect["positive_graph_definition_rows"] == 5_264 and effect["new_empty_R235_target_graph_dispositions"] == 33_344, "C5 graph census")
    need(effect["corrected_physical_incidence_relation_denominator"] == 15_392 and c5["formal_credit"]["physical_incidence"] == 0, "C5 mechanical relation boundary")


def build() -> tuple[dict[str, Any], bytes, bytes]:
    source_pin_catalog = [pin.__dict__ for pin in PINS]
    with Snapshot() as snapshot:
        c8 = exact_document(snapshot.read("C8_FRONTIER"), "C8 frontier")
        c7 = exact_document(snapshot.read("C7_RESULT"), "C7 result")
        c5_result = exact_document(snapshot.read("C5_RESULT"), "C5 result")
        validate_sources(c8, c7, c5_result)

        c5_rows = jsonl_rows(snapshot, "C5_LEDGER")
        c4_rows = jsonl_rows(snapshot, "C4_LEDGER")
        physical_rows = jsonl_rows(snapshot, "C7_PHYSICAL")
        gap_rows = jsonl_rows(snapshot, "C7_GAPS")
        need(len(c5_rows) == 38_608 and len(c4_rows) == 16 and len(physical_rows) == len(gap_rows) == 15_392, "source row census")
        need({row["subject_row_id"] for row in gap_rows} == {row["row_id"] for row in physical_rows}, "C7 gap relation bijection")

        r234_document = json_document(snapshot, "R234_CERT")
        r248_document = json_document(snapshot, "R248_CERT")
        r234_rows = r234_document["result"]["depth6_frontier_rows"]
        r248_rows = r248_document["result"]["formal_wall_half_open_sheet_owner_ledger"]["rows"]
        need(len(r234_rows) == 38_376 and len(r248_rows) == 38_360, "legacy geometry row census")
        r248_by_member = {row["wall_sheet_node_id"]: row for row in r248_rows}
        need(len(r248_by_member) == len(r248_rows), "R248 member uniqueness")

        c4_by_id = {row["bridge_row_id"]: row for row in c4_rows}
        empty_target_by_graph = {row["G2_orphan_graph_disposition"]["C3_orphan_target_graph_id"]: row for row in c4_rows}
        need(len(c4_by_id) == len(empty_target_by_graph) == 16, "C4 graph uniqueness")

        sheet_relation_by_graph: dict[str, dict[str, Any]] = {}
        relations_by_graph: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for relation in physical_rows:
            relations_by_graph[relation["graph_id"]].append(relation)
            if relation["incidence_role"] == "GRAPH_TO_SHEET":
                need(relation["graph_id"] not in sheet_relation_by_graph, "one sheet relation per graph")
                sheet_relation_by_graph[relation["graph_id"]] = relation

        graph_rows: list[dict[str, Any]] = []
        graph_class_by_id: dict[str, str] = {}
        graph_audit_by_id: dict[str, dict[str, Any]] = {}
        graph_class_census = Counter()
        endpoint_histogram = Counter()
        positive_rows = [row for row in c5_rows if row["semantic_classification"]["classification"] == "POSITIVE_GRAPH"]
        need(len(positive_rows) == 5_264, "C5 positive graph census")

        for source in positive_rows:
            semantic = source["semantic_classification"]
            graph_id = source["graph_id"]
            kernel = semantic["kernel"]
            sheet_relation = sheet_relation_by_graph.get(graph_id)
            need(sheet_relation is not None and sheet_relation["graph_semantic_authority_row_id"] == source["semantic_row_id"], "positive graph sheet relation")
            sheet_member = sheet_relation["member_id"]
            exact_receipt: dict[str, Any]
            old_geometry: dict[str, Any]
            if kernel == "G_TARGET_FIRST_HIT_COORDINATE_MINUS_INTEGER_WALL_V1":
                graph_class = "R235_TARGET_POSITIVE_PARTIAL_BASE"
                frontier_ref = source["canonical_input_commitment"]["R234_frontier_row"]
                frontier = r234_rows[frontier_ref[0]]
                need(frontier["frontier_row_id"] == frontier_ref[1] and object_sha(frontier) == frontier_ref[2], "R234 target frontier binding")
                need(semantic["complete_parameter_domain"]["box"] == frontier["box"], "target complete domain")
                derivative = strict_target_derivative(frontier, semantic["strict_t_derivative_proof"]["strict_t_derivative_sign"])
                need(derivative == semantic["strict_t_derivative_proof"], "independent target derivative replay")
                endpoint = no_graph_endpoint(frontier)
                endpoint_histogram[(endpoint["p_endpoint"], endpoint["lower_t_face_factor_sign"])] += 1
                r248 = r248_by_member[sheet_member]
                r248_core = dict(r248)
                claimed_r248_sha = r248_core.pop("row_sha256")
                need(claimed_r248_sha == object_sha(r248_core), "R248 target row closure")
                need(r248["source_partition_row_id"] == graph_id and r248["endpoint_factor"] == "target", "R248 target source binding")
                need(r248["exact_closed_base_rectangle"] == frontier["box"][2:6], "R248 complete base rectangle")
                need(semantic["exact_graph_base_domain"] == "BASE_POINTS_WHERE_ORIENTED_T_FACE_SIGNS_OPPOSE_OR_TOUCH", "target exact domain predicate")
                need(Q(semantic["positive_base_witness"]["exact_positive_base_area"]["numerator"], semantic["positive_base_witness"]["exact_positive_base_area"]["denominator"]) > 0, "target positive witness")
                exact_receipt = {
                    "domain_state": "PROVED_NONEMPTY_PARTIAL_BASE_DOMAIN",
                    "exact_graph_base_domain_predicate": semantic["exact_graph_base_domain"],
                    "positive_base_witness_sha256": object_sha(semantic["positive_base_witness"]),
                    "strict_t_derivative_proof": derivative,
                    "strict_t_derivative_proof_sha256": object_sha(derivative),
                    "no_graph_base_endpoint": endpoint,
                }
                old_geometry = {
                    "member_id": sheet_member,
                    "source": "R248_EXACT_CLOSED_BASE_RECTANGLE",
                    "R248_row_sha256": claimed_r248_sha,
                    "rectangle": r248["exact_closed_base_rectangle"],
                    "disposition": "OUTER_ENVELOPE_ONLY__NOT_FULL_GRAPH_SUPPORT",
                }
            elif kernel == "EXACT_SOURCE_COORDINATE_MINUS_ZERO_EQUALS_9_OVER_25_TIMES_T":
                graph_class = "R235_SOURCE_EXACT_FACE_FULL_BASE"
                need(semantic["zero_set"] == "EXACT_T_EQUALS_ZERO_FACE_TIMES_FULL_P_S_BASE", "R235 source zero set")
                need(semantic["strict_t_derivative_exact"] == qwire(Q(9, 25)), "R235 source derivative")
                r248 = r248_by_member[sheet_member]
                r248_core = dict(r248)
                claimed_r248_sha = r248_core.pop("row_sha256")
                need(claimed_r248_sha == object_sha(r248_core), "R248 source row closure")
                need(r248["source_partition_row_id"] == graph_id and r248["endpoint_factor"] == "source", "R248 source binding")
                need(r248["exact_closed_base_rectangle"] == semantic["complete_parameter_domain"]["box"][2:6], "R248 source base rectangle")
                exact_receipt = {"domain_state": "SEALED_EXACT_FACE_TIMES_FULL_BASE", "zero_face": semantic["zero_face"], "zero_set": semantic["zero_set"], "exact_positive_base_area": semantic["exact_positive_base_area"]}
                old_geometry = {"member_id": sheet_member, "source": "R248_EXACT_CLOSED_BASE_RECTANGLE", "R248_row_sha256": claimed_r248_sha, "rectangle": r248["exact_closed_base_rectangle"], "disposition": "EXACT_BASE_GEOMETRY_AVAILABLE__PHYSICAL_PULLBACK_PENDING"}
            elif kernel == "SEALED_C4_R235D_SOURCE_EXACT_FACE_GRAPH_BRIDGE":
                graph_class = "R235D_SOURCE_EXACT_FACE_FULL_BASE"
                bridge_ref = source["canonical_input_commitment"]["C4_bridge_row"]
                bridge = c4_by_id[bridge_ref[1]]
                need(object_sha(bridge) == bridge_ref[2], "C4 source bridge binding")
                reconstruction = bridge["semantic_reconstruction"]
                need(reconstruction["source_zero_set"] == "EXACT_FACE_GRAPH_t_EQUALS_0" and reconstruction["complete_domain_partition_verified"] is True, "C4 source exact domain")
                r248 = r248_by_member[sheet_member]
                r248_core = dict(r248)
                claimed_r248_sha = r248_core.pop("row_sha256")
                need(claimed_r248_sha == object_sha(r248_core), "R248 R235D row closure")
                need(r248["source_partition_kind"] == "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET", "R248 R235D source kind")
                exact_receipt = {"domain_state": "SEALED_EXACT_FACE_TIMES_FULL_BASE", "C4_bridge_row_sha256": bridge["row_sha256"], "complete_parameter_domain_sha256": object_sha(reconstruction["complete_parameter_domain"]), "zero_face": reconstruction["source_zero_face"], "zero_set": reconstruction["source_zero_set"]}
                old_geometry = {"member_id": sheet_member, "source": "R248_EXACT_CLOSED_BASE_RECTANGLE", "R248_row_sha256": claimed_r248_sha, "rectangle": r248["exact_closed_base_rectangle"], "disposition": "EXACT_BASE_GEOMETRY_AVAILABLE__PHYSICAL_PULLBACK_PENDING"}
            elif kernel == "SEALED_R242_UNIQUE_TRANSITION_GRAPH_PATCH_BRIDGE":
                graph_class = "R242_UNIQUE_GRAPH_FULL_PATCH"
                need(semantic["graph_local_dimension"] == 2 and Q(semantic["exact_positive_base_projection_area"]) > 0, "R242 positive patch")
                need(semantic["lower_t_face_F_sign"] != semantic["upper_t_face_F_sign"], "R242 opposing faces")
                exact_receipt = {"domain_state": "SEALED_UNIQUE_GRAPH_OVER_FULL_CLOSED_WITNESS_BASE", "closed_witness_box": semantic["closed_witness_box"], "exact_positive_base_projection_area": semantic["exact_positive_base_projection_area"], "strict_t_derivative_sign": semantic["strict_t_derivative_sign"]}
                old_geometry = {"member_id": sheet_member, "source": "R245_RETAINED_STRATUM", "disposition": "EXACT_PATCH_GEOMETRY_AVAILABLE__PHYSICAL_PULLBACK_PENDING"}
            else:
                raise Rejected("unknown positive graph kernel:" + kernel)

            graph_class_by_id[graph_id] = graph_class
            graph_class_census[graph_class] += 1
            core = {
                "schema": GRAPH_ROW_SCHEMA,
                "row_id": PREFIX + ":graph-domain:" + object_sha([graph_id, graph_class]),
                "graph_id": graph_id,
                "graph_inventory_ordinal": source["graph_inventory_ordinal"],
                "graph_inventory_row_id": source["graph_inventory_row_id"],
                "C5_semantic_row_id": source["semantic_row_id"],
                "C5_semantic_row_sha256": source["row_sha256"],
                "graph_class": graph_class,
                "sheet_member_id": sheet_member,
                "exact_graph_domain_receipt": exact_receipt,
                "legacy_sheet_geometry_scope": old_geometry,
                "required_next": "MATERIALIZE_EXACT_GRAPH_SUPPORT_AST_AND_PROVE_PHYSICAL_PULLBACK_AND_ONE_SIDED_TRACE",
                "formal_credit": ZERO_CREDIT,
            }
            row = closed_row(core)
            graph_rows.append(row)
            graph_audit_by_id[graph_id] = row

        graph_rows.sort(key=lambda row: row["graph_inventory_ordinal"])
        need(len(graph_rows) == len(graph_class_by_id) == len(graph_audit_by_id) == 5_264, "graph audit exhaustion")
        need(graph_class_census == {"R235_TARGET_POSITIVE_PARTIAL_BASE": 4_432, "R235_SOURCE_EXACT_FACE_FULL_BASE": 552, "R235D_SOURCE_EXACT_FACE_FULL_BASE": 16, "R242_UNIQUE_GRAPH_FULL_PATCH": 264}, "graph audit class census")
        need(endpoint_histogram == {("LOWER_P", "STRICT_NEGATIVE"): 2_098, ("LOWER_P", "STRICT_POSITIVE"): 2_098, ("UPPER_P", "STRICT_NEGATIVE"): 118, ("UPPER_P", "STRICT_POSITIVE"): 118}, "partial-domain endpoint histogram")

        relation_rows: list[dict[str, Any]] = []
        relation_census = Counter()
        relation_class_role_census = Counter()
        for ordinal, source in enumerate(physical_rows):
            graph_id = source["graph_id"]
            relation_class_role_census[(graph_class_by_id.get(graph_id, "C4_EMPTY_TARGET"), source["incidence_role"])] += 1
            if source["graph_semantic_authority_kind"] == "C4_ORPHAN_TARGET_EMPTY_GRAPH_DISPOSITION":
                bridge = empty_target_by_graph.get(graph_id)
                need(bridge is not None and bridge["bridge_row_id"] == source["graph_semantic_authority_row_id"] and bridge["row_sha256"] == source["graph_semantic_authority_row_sha256"], "empty graph authority binding")
                need(bridge["G2_orphan_graph_disposition"]["disposition"] == "EMPTY_GRAPH_ON_COMPLETE_PARAMETER_DOMAIN", "empty graph disposition")
                disposition = "EMPTY_GRAPH_NO_PHYSICAL_INCIDENCE"
                relation_candidate = 0
                graph_audit_ref = None
                required_next = "REMOVE_FROM_PHYSICAL_INCIDENCE_DENOMINATOR_AND_RETAIN_NON_GRAPH_DISPOSITION"
            else:
                need(source["graph_semantic_authority_kind"] == "C5_POSITIVE_GRAPH_DEFINITION", "positive graph authority kind")
                audit = graph_audit_by_id.get(graph_id)
                need(audit is not None and audit["C5_semantic_row_id"] == source["graph_semantic_authority_row_id"] and audit["C5_semantic_row_sha256"] == source["graph_semantic_authority_row_sha256"], "positive graph audit binding")
                graph_class = audit["graph_class"]
                relation_candidate = 1
                graph_audit_ref = {"row_id": audit["row_id"], "row_sha256": audit["row_sha256"]}
                if source["incidence_role"] == "GRAPH_TO_SHEET" and graph_class == "R235_TARGET_POSITIVE_PARTIAL_BASE":
                    disposition = "LEGACY_COMPLETE_RECTANGLE_IS_OUTER_ENVELOPE_NOT_FULL_GRAPH_SUPPORT"
                    required_next = "REMATERIALIZE_EXACT_SIGN_STRADDLE_GRAPH_DOMAIN_BEFORE_PHYSICAL_PULLBACK"
                elif source["incidence_role"] == "GRAPH_TO_SHEET":
                    disposition = "EXACT_GRAPH_SUPPORT_AVAILABLE__PHYSICAL_IDENTIFICATION_AND_PULLBACK_PENDING"
                    required_next = "PROVE_GRAPH_EQUALS_MEMBER_SUPPORT_AND_REPRESENTATION_PULLBACK"
                else:
                    need(source["incidence_role"] == "GRAPH_TO_SIDE", "relation role")
                    disposition = "EXACT_ONE_SIDED_SIGN_STRATUM_AND_TRACE_PENDING"
                    required_next = "REMATERIALIZE_EXACT_SIDE_SIGN_STRATUM_AND_PROVE_ONE_SIDED_TRACE"
            relation_census[disposition] += 1
            core = {
                "schema": RELATION_ROW_SCHEMA,
                "row_id": PREFIX + ":relation-disposition:" + object_sha([source["row_id"], disposition]),
                "mechanical_relation_ordinal": ordinal,
                "C7_relation_row_id": source["row_id"],
                "C7_relation_row_sha256": source["row_sha256"],
                "graph_id": graph_id,
                "member_id": source["member_id"],
                "coarse_family": source["coarse_family"],
                "incidence_role": source["incidence_role"],
                "graph_domain_audit_ref": graph_audit_ref,
                "disposition": disposition,
                "positive_graph_physical_relation_candidate": relation_candidate,
                "physical_incidence_proved": False,
                "representation_pullback_proved": False,
                "one_sided_trace_proved": False,
                "required_next": required_next,
                "formal_credit": ZERO_CREDIT,
            }
            relation_rows.append(closed_row(core))

        need(len(relation_rows) == 15_392, "relation disposition exhaustion")
        need(relation_census == {"LEGACY_COMPLETE_RECTANGLE_IS_OUTER_ENVELOPE_NOT_FULL_GRAPH_SUPPORT": 4_432, "EXACT_GRAPH_SUPPORT_AVAILABLE__PHYSICAL_IDENTIFICATION_AND_PULLBACK_PENDING": 832, "EXACT_ONE_SIDED_SIGN_STRATUM_AND_TRACE_PENDING": 10_118, "EMPTY_GRAPH_NO_PHYSICAL_INCIDENCE": 10}, "relation disposition census")
        need(relation_class_role_census == {("R235_TARGET_POSITIVE_PARTIAL_BASE", "GRAPH_TO_SHEET"): 4_432, ("R235_TARGET_POSITIVE_PARTIAL_BASE", "GRAPH_TO_SIDE"): 8_864, ("R235_SOURCE_EXACT_FACE_FULL_BASE", "GRAPH_TO_SHEET"): 552, ("R235_SOURCE_EXACT_FACE_FULL_BASE", "GRAPH_TO_SIDE"): 704, ("R235D_SOURCE_EXACT_FACE_FULL_BASE", "GRAPH_TO_SHEET"): 16, ("R235D_SOURCE_EXACT_FACE_FULL_BASE", "GRAPH_TO_SIDE"): 22, ("R242_UNIQUE_GRAPH_FULL_PATCH", "GRAPH_TO_SHEET"): 264, ("R242_UNIQUE_GRAPH_FULL_PATCH", "GRAPH_TO_SIDE"): 528, ("C4_EMPTY_TARGET", "GRAPH_TO_SIDE"): 10}, "relation class-role census")
        need(sum(row["positive_graph_physical_relation_candidate"] for row in relation_rows) == 15_382, "positive relation candidate denominator")

        graph_wire, graph_plain = gzip_rows(graph_rows)
        relation_wire, relation_plain = gzip_rows(relation_rows)
        graph_descriptor = ledger_descriptor(GRAPH_LEDGER_NAME, GRAPH_ROW_SCHEMA, graph_rows, graph_wire, graph_plain)
        relation_descriptor = ledger_descriptor(RELATION_LEDGER_NAME, RELATION_ROW_SCHEMA, relation_rows, relation_wire, relation_plain)
        body = {
            "schema": SCHEMA,
            "status": STATUS,
            "producer_source": producer_record(),
            "source_pins": source_pin_catalog,
            "upstream_seal_bindings": {
                "C8_manifest_sha256": PINS[0].sha256,
                "C7_manifest_sha256": PINS[2].sha256,
                "C5_manifest_sha256": PINS[6].sha256,
                "C4_manifest_sha256": PINS[9].sha256,
                "R234_manifest_sha256": PINS[11].sha256,
                "R248_manifest_sha256": PINS[13].sha256,
            },
            "fresh_base": {"members": 497_772, "representations": 545_184, "components": 61_928},
            "audit_census": {
                "positive_graph_domain_audit_rows": 5_264,
                "mechanical_relation_statement_rows": 15_392,
                "positive_graph_physical_relation_candidates": 15_382,
                "empty_graph_no_incidence_dispositions": 10,
                "remaining_physical_incidence_theorem_rows": 15_382,
                "remaining_pullback_theorem_rows": 15_382,
                "remaining_one_sided_trace_rows": 10_118,
            },
            "graph_class_census": dict(sorted(graph_class_census.items())),
            "target_partial_domain_endpoint_histogram": {side + ":" + sign: count for (side, sign), count in sorted(endpoint_histogram.items())},
            "relation_disposition_census": dict(sorted(relation_census.items())),
            "relation_class_role_census": {graph_class + ":" + role: count for (graph_class, role), count in sorted(relation_class_role_census.items())},
            "denominator_correction": {
                "C7_mechanical_statement_count": 15_392,
                "C9_positive_graph_relation_candidate_count": 15_382,
                "removed_empty_graph_statement_count": 10,
                "historical_115440_denominator_reused": False,
                "historical_76832_denominator_reused": False,
                "C8_15392_may_be_called_proved_physical_incidence_count": False,
            },
            "support_scope_correction": {
                "R235_target_positive_graph_count": 4_432,
                "all_R235_target_positive_graphs_have_nonempty_partial_base_domain": True,
                "R248_complete_closed_base_rectangles_are_outer_envelopes_for_these_graphs": True,
                "outer_envelope_may_be_promoted_to_full_support": False,
                "abstract_member_identity_may_be_retained_without_exact_support_rematerialization": False,
                "rekey_requirement_decided_by_this_audit": False,
            },
            "graph_domain_audit_ledger": graph_descriptor,
            "relation_disposition_ledger": relation_descriptor,
            "required_next": {
                "materialize_5264_exact_graph_support_ASTs": True,
                "prove_15382_physical_incidence_relations": True,
                "prove_15382_representation_pullbacks": True,
                "prove_10118_one_sided_traces": True,
                "decide_identity_preservation_or_rekey_under_exact_support": True,
                "fresh_DSU_reclosure_if_rekey_or_new_edge_occurs": True,
                "B1A": "NOT_AUTHORIZED",
                "B2": "NOT_AUTHORIZED",
            },
            "formal_credit": ZERO_CREDIT,
            "normalized_support_sealed": False,
            "B1A_permitted": False,
            "B2_permitted": False,
            "CM2": "NO-GO_FOR_CLAIM",
            "seed_serialized_or_semantically_used": False,
        }
        result = {**body, "result_sha256": object_sha(body)}
        snapshot.final()
    return result, graph_wire, relation_wire


def write_once(directory: Path, filename: str, payload: bytes) -> None:
    path = directory / filename
    need(not path.exists(), "publish no-clobber:" + filename)
    file_descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(file_descriptor, payload[offset:])
        os.fsync(file_descriptor)
    finally:
        os.close(file_descriptor)
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(payload), "published file:" + filename)


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-result", action="store_true")
    parser.add_argument("--candidate-dir")
    parser.add_argument("--publish", action="store_true")
    arguments = parser.parse_args()
    need(sum((arguments.print_result, arguments.candidate_dir is not None, arguments.publish)) == 1, "exactly one mode")
    result, graph_wire, relation_wire = build()
    result_wire = canonical(result)
    if arguments.print_result:
        sys.stdout.buffer.write(result_wire + b"\n")
    else:
        if arguments.publish:
            directory = ROOT
        else:
            directory = Path(arguments.candidate_dir).resolve()
            need(os.path.commonpath((str(directory), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
            directory.mkdir(mode=0o700, parents=False, exist_ok=False)
        write_once(directory, GRAPH_LEDGER_NAME, graph_wire)
        write_once(directory, RELATION_LEDGER_NAME, relation_wire)
        write_once(directory, RESULT_NAME, result_wire)
        records = []
        for filename, payload in ((GRAPH_LEDGER_NAME, graph_wire), (RELATION_LEDGER_NAME, relation_wire), (RESULT_NAME, result_wire)):
            records.append({"filename": filename, "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
        for record in reversed(records):
            info = os.stat(directory / record["filename"], follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == record["size"], "reverse publication identity")
            with open(directory / record["filename"], "rb") as stream:
                need(hashlib.sha256(stream.read()).hexdigest() == record["sha256"], "reverse publication digest")
        print(json.dumps({"status": result["status"], "result_sha256": result["result_sha256"], "published_result_last": True, "files": records}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
