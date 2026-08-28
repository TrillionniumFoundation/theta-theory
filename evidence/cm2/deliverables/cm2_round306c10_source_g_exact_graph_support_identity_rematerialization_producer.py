#!/usr/bin/env python3
"""Produce the scoped C10 exact G2A feature-support and identity overlay.

This producer deliberately does not prove graph-to-sheet set equality, physical
incidence, representation pullback, one-sided trace, global normalized support,
B1A, B2, maximality, or CM2.  Its only positive credits are one exact feature
support AST and one support-independent natural-key preservation decision for
each of the 5,264 positive G2 graph sheets.
"""

from __future__ import annotations

import argparse
from collections import Counter
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
from typing import Any, Final, Iterator


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization"
SCHEMA: Final = "cm2.round306c10.source-g-exact-graph-support-identity-rematerialization.v1"
SUPPORT_ROW_SCHEMA: Final = SCHEMA + ".exact-graph-support-row.v1"
IDENTITY_ROW_SCHEMA: Final = SCHEMA + ".member-identity-disposition-row.v1"
SUPPORT_LEDGER_NAME: Final = PREFIX + "_exact_graph_support_ledger.jsonl.gz"
IDENTITY_LEDGER_NAME: Final = PREFIX + "_member_identity_disposition_ledger.jsonl.gz"
RESULT_NAME: Final = PREFIX + "_result.json"
STATUS: Final = (
    "PASS_5264_EXACT_G2_FEATURE_SUPPORT_ASTS__"
    "5264_NATURAL_KEY_IDENTITIES_PRESERVED__"
    "ZERO_PHYSICAL_PULLBACK_TRACE_GLOBAL_SUPPORT_CREDIT"
)
SQRT_BITS: Final = 224
ROOT_ISOLATION_STEPS: Final = 48
OWNER_RE: Final = re.compile(r"^([GW])\[(-?[0-9]+),(-?[0-9]+)\]$")

C9_MANIFEST: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_manifest.sha256"
C9_RESULT: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_result.json"
C9_GRAPH: Final = "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_graph_domain_audit_ledger.jsonl.gz"
C7_MANIFEST: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_manifest.sha256"
C7_MEMBER: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_member_identity_support_ledger.jsonl.gz"
C7_REPRESENTATION: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_representation_ledger.jsonl.gz"
C6_MANIFEST: Final = "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_manifest.sha256"
C6_MEMBER_COMPONENT: Final = "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C5_MANIFEST: Final = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_manifest.sha256"
C5_SEMANTIC: Final = "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz"
C4_MANIFEST: Final = "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_manifest.sha256"
C4_LEDGER: Final = "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz"
R234_MANIFEST: Final = "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_manifest.sha256"
R234_CERT: Final = "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json"
R248_MANIFEST: Final = "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256"
R248_CERT: Final = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R245_MANIFEST: Final = "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_manifest.sha256"
R245_CERT: Final = "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json"
R242_MANIFEST: Final = "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_manifest.sha256"
R242_CERT: Final = "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("C9_MANIFEST", C9_MANIFEST, 1_396, "8921fb3eadd5d8b4aec1afe3af91c938b2c5568e9f9ef3be64002e4146152d04"),
    Pin("C9_RESULT", C9_RESULT, 8_845, "31d8da4e4a3e6ad703bd24fd7456f801d3fd90293e171d9784b2280d393b76a8"),
    Pin("C9_GRAPH", C9_GRAPH, 2_488_534, "955d8930fc321ca4f2556d66af488e4b9391f91002b65ecf8eaace6fbd3a7d50"),
    Pin("C7_MANIFEST", C7_MANIFEST, 2_184, "4e534e412a760d13fe7eb278ca063e86ac2a7164bbfdb3b14a3142219267c0c6"),
    Pin("C7_MEMBER", C7_MEMBER, 269_633_111, "de85e6f26b64299d70c5006df76c5e4a242dc46d5b4885bca1f37b13d923c4e0"),
    Pin("C7_REPRESENTATION", C7_REPRESENTATION, 240_400_592, "1dc805b60f15ec8491b5200ccf9f04a239ce1532f6845a026045709feaaaa468"),
    Pin("C6_MANIFEST", C6_MANIFEST, 2_211, "d9c3261421a966f62eeb027517f0f0e58ab2f3f72d856fed5cdcced55ff158f2"),
    Pin("C6_MEMBER_COMPONENT", C6_MEMBER_COMPONENT, 213_125_489, "730a1501402d29f9689655b0093edd4d7e499f3a34c6b65e9f21ee6f3f5ffce2"),
    Pin("C5_MANIFEST", C5_MANIFEST, 1_193, "aefe82ef88c2ddf5f241d76e0f0f7483e230d68219ace6639f7389adbcb14134"),
    Pin("C5_SEMANTIC", C5_SEMANTIC, 78_082_824, "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"),
    Pin("C4_MANIFEST", C4_MANIFEST, 1_177, "5550eb9cf4e474a8d08086062e28538e909f6e1c7e499ba10a78a2d24e683de6"),
    Pin("C4_LEDGER", C4_LEDGER, 101_147, "3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),
    Pin("R234_MANIFEST", R234_MANIFEST, 574, "f8714ecdf804657fc6633136544f567b07e7d8503095d17fcda19226feefc432"),
    Pin("R234_CERT", R234_CERT, 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    Pin("R248_MANIFEST", R248_MANIFEST, 885, "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07"),
    Pin("R248_CERT", R248_CERT, 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
    Pin("R245_MANIFEST", R245_MANIFEST, 897, "1aff29f3a42b618ca85e5a1d3c537307e32326f8d5092b82d4253a5bf6e1c4ac"),
    Pin("R245_CERT", R245_CERT, 20_683_081, "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"),
    Pin("R242_MANIFEST", R242_MANIFEST, 897, "6da30fe3f9438ec73dc9c7d1aac770d8e9730aa9564ab0c535f1596cdc09ef2f"),
    Pin("R242_CERT", R242_CERT, 13_734_655, "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e"),
)
PIN_BY_ROLE: Final = {pin.role: pin for pin in PINS}

CLASS_CENSUS: Final = {
    "R235_TARGET_POSITIVE_PARTIAL_BASE": 4_432,
    "R235_SOURCE_EXACT_FACE_FULL_BASE": 552,
    "R235D_SOURCE_EXACT_FACE_FULL_BASE": 16,
    "R242_UNIQUE_GRAPH_FULL_PATCH": 264,
}
TARGET_TOPOLOGY_CENSUS: Final = {
    "INTERNAL_P_BAND": 3_960,
    "LOWER_P_ATTACHED": 236,
    "UPPER_P_ATTACHED": 236,
    "FULL_P_INTERVAL": 0,
}
DOWNSTREAM_ZERO: Final = {
    "graph_sheet_set_equality": 0,
    "physical_incidence": 0,
    "representation_pullback": 0,
    "one_sided_trace": 0,
    "member_normalized_support": 0,
    "global_normalized_support": 0,
    "A1_A2": 0,
    "transition": 0,
    "B1A": 0,
    "B2": 0,
    "maximality": 0,
    "fibre": 0,
    "global_disposition": 0,
    "CM2": 0,
}


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


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
    blocks = []
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
        self.directory_descriptor = os.open(
            ROOT,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        for pin in PINS:
            info = os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)
            need(
                stat.S_ISREG(info.st_mode)
                and info.st_nlink == 1
                and info.st_size == pin.size,
                "pin identity:" + pin.role,
            )
            descriptor = os.open(
                pin.filename,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=self.directory_descriptor,
            )
            opened = os.fstat(descriptor)
            need(identity(opened) == identity(info), "pin race:" + pin.role)
            need(hash_fd(descriptor) == hash_fd(descriptor) == pin.sha256, "pin digest:" + pin.role)
            self.file_descriptors[pin.role] = descriptor
            self.identities[pin.role] = identity(opened)
        return self

    def read(self, role: str) -> bytes:
        return read_fd(self.file_descriptors[role])

    def duplicate(self, role: str) -> int:
        descriptor = os.dup(self.file_descriptors[role])
        os.lseek(descriptor, 0, os.SEEK_SET)
        return descriptor

    def final(self) -> None:
        for pin in reversed(PINS):
            descriptor = self.file_descriptors[pin.role]
            need(identity(os.fstat(descriptor)) == self.identities[pin.role], "final fd:" + pin.role)
            need(
                identity(os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False))
                == self.identities[pin.role],
                "final path:" + pin.role,
            )
            need(hash_fd(descriptor) == pin.sha256, "final digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for descriptor in self.file_descriptors.values():
            try:
                os.close(descriptor)
            except OSError:
                pass
        if self.directory_descriptor >= 0:
            os.close(self.directory_descriptor)


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    need(raw.endswith(b"\n"), "manifest newline:" + label)
    records: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ")
        need(len(parts) == 2 and len(parts[0]) == 64, "manifest line:" + label)
        int(parts[0], 16)
        name = Path(parts[1]).name
        need(
            parts[1] in {name, "deliverables/" + name}
            and name not in records,
            "manifest name:" + label,
        )
        records[name] = parts[0]
    return records


def bind_manifest(snapshot: Snapshot, manifest_role: str, member_roles: tuple[str, ...]) -> None:
    records = parse_manifest(snapshot.read(manifest_role), manifest_role)
    for role in member_roles:
        pin = PIN_BY_ROLE[role]
        need(records.get(pin.filename) == pin.sha256, "manifest member binding:" + manifest_role + ":" + role)


def exact_closed_document(raw: bytes, field: str, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) == raw, "canonical document:" + label)
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == object_sha(body), "document closure:" + label)
    return value


def legacy_document(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict and set(value) == {"schema", "result", "result_sha256"}, "legacy envelope:" + label)
    need(value["result_sha256"] == object_sha(value["result"]), "legacy closure:" + label)
    return value


def jsonl_rows(snapshot: Snapshot, role: str) -> Iterator[dict[str, Any]]:
    duplicate = snapshot.duplicate(role)
    try:
        with os.fdopen(duplicate, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            for ordinal, line in enumerate(stream):
                row = json.loads(line)
                need(
                    type(row) is dict and line.endswith(b"\n") and line == canonical(row) + b"\n",
                    "canonical JSONL:" + role + ":" + str(ordinal),
                )
                body = dict(row)
                claimed = body.pop("row_sha256", None)
                need(type(claimed) is str and claimed == object_sha(body), "row closure:" + role + ":" + str(ordinal))
                yield row
    finally:
        try:
            os.close(duplicate)
        except OSError:
            pass


def producer_record() -> dict[str, Any]:
    info = os.stat(__file__, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "producer identity")
    descriptor = os.open(__file__, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(descriptor)
        need(identity(opened) == identity(info), "producer race")
        digest = hash_fd(descriptor)
        need(digest == hash_fd(descriptor), "producer two-pass digest")
        return {"filename": Path(__file__).name, "size": info.st_size, "sha256": digest}
    finally:
        os.close(descriptor)


def qstr(value: Q | int | str) -> str:
    rational = Q(value)
    return str(rational.numerator) if rational.denominator == 1 else f"{rational.numerator}/{rational.denominator}"


def qwire(value: Q | int | str) -> dict[str, int]:
    rational = Q(value)
    return {"numerator": rational.numerator, "denominator": rational.denominator}


def rational_from_wire(value: dict[str, Any], label: str) -> Q:
    need(
        type(value) is dict
        and set(value) == {"numerator", "denominator"}
        and type(value["numerator"]) is int
        and type(value["denominator"]) is int
        and value["denominator"] > 0,
        "rational wire:" + label,
    )
    rational = Q(value["numerator"], value["denominator"])
    need(qwire(rational) == value, "reduced rational wire:" + label)
    return rational


@dataclass(frozen=True)
class Interval:
    lower: Q
    upper: Q

    def __post_init__(self) -> None:
        need(type(self.lower) is Q and type(self.upper) is Q and self.lower <= self.upper, "interval")

    @classmethod
    def point(cls, value: Q | int | str) -> "Interval":
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
        values = (
            self.lower * right.lower,
            self.lower * right.upper,
            self.upper * right.lower,
            self.upper * right.upper,
        )
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def square(self) -> "Interval":
        values = (self.lower * self.lower, self.upper * self.upper)
        return Interval(Q(0) if self.lower <= 0 <= self.upper else min(values), max(values))

    def divide(self, other: Any) -> "Interval":
        right = other if type(other) is Interval else Interval.point(other)
        need(not right.lower <= 0 <= right.upper, "interval division")
        reciprocal = Interval(
            min(Q(1, right.lower), Q(1, right.upper)),
            max(Q(1, right.lower), Q(1, right.upper)),
        )
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
        return Dual(
            self.value * right.value,
            self.derivative * right.value + self.value * right.derivative,
        )

    __rmul__ = __mul__


def sqrt_dual(value: Dual) -> Dual:
    root = sqrt_interval(value.value)
    return Dual(root, value.derivative.divide(root * 2))


def owner_xy(owner: str) -> tuple[str, int, int]:
    match = OWNER_RE.fullmatch(owner)
    need(match is not None, "owner")
    return match.group(1), int(match.group(2)), int(match.group(3))


def geometry(
    chart: str,
    owner: str,
    t_bounds: tuple[Q, Q],
    p_bounds: tuple[Q, Q],
    variable: str | None,
) -> dict[str, Interval | Dual]:
    owner_kind, owner_x, owner_y = owner_xy(owner)
    need(chart in {"G:E", "G:W", "G:N", "G:S"} and owner_kind == "G", "G geometry")
    t_interval = Interval(*t_bounds)
    p_interval = Interval(*p_bounds)
    if variable is None:
        t: Interval | Dual = t_interval
        p: Interval | Dual = p_interval
        one: Interval | Dual = Interval.point(1)
        normal_radicand: Interval | Dual = one - t.square()
        phase_radicand: Interval | Dual = one - p.square()
        normal_root = sqrt_interval(normal_radicand)
        phase_root = sqrt_interval(phase_radicand)
    else:
        need(variable in {"t", "p"}, "dual variable")
        t = Dual(t_interval, Interval.point(1 if variable == "t" else 0))
        p = Dual(p_interval, Interval.point(1 if variable == "p" else 0))
        one = Dual.constant(1)
        normal_radicand = one - t * t
        phase_radicand = one - p * p
        normal_root = sqrt_dual(normal_radicand)
        phase_root = sqrt_dual(phase_radicand)
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
    if variable is None:
        hit_radicand: Interval | Dual = Interval.point(radius * radius) - transverse.square()
        radical = sqrt_interval(hit_radicand)
    else:
        hit_radicand = Dual.constant(radius * radius) - transverse * transverse
        radical = sqrt_dual(hit_radicand)
    hit_x = owner_x - radical * tangent_x + transverse * tangent_y
    hit_y = owner_y - radical * tangent_y - transverse * tangent_x
    return {
        "hit_x": hit_x,
        "hit_y": hit_y,
        "normal_radicand": normal_radicand,
        "phase_radicand": phase_radicand,
        "hit_radicand": hit_radicand,
    }


def endpoint_spec(frontier: dict[str, Any]) -> tuple[str, int]:
    kind, axis, wall_text = frontier["reason_labels"][0].split(":")
    need(kind == "wall_endpoint_or_count_transition" and axis in {"X", "Y"}, "endpoint reason")
    return axis, int(wall_text)


def target_factor(
    frontier: dict[str, Any],
    t_bounds: tuple[Q, Q],
    p_bounds: tuple[Q, Q],
    variable: str | None = None,
) -> Interval | Dual:
    axis, wall = endpoint_spec(frontier)
    values = geometry(frontier["chart"], frontier["owner_target"], t_bounds, p_bounds, variable)
    coordinate = values["hit_x" if axis == "X" else "hit_y"]
    return coordinate - wall


def strict_target_t_derivative(frontier: dict[str, Any], expected: str) -> dict[str, Any]:
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
        need(depth < 8, "target t derivative unresolved")
        if depth % 2 == 0:
            middle = (pa + pb) / 2
            stack.extend(((ta, tb, pa, middle, depth + 1), (ta, tb, middle, pb, depth + 1)))
        else:
            middle = (ta + tb) / 2
            stack.extend(((ta, middle, pa, pb, depth + 1), (middle, tb, pa, pb, depth + 1)))
    return {
        "strict_t_derivative_sign": expected,
        "proof_cell_count": cells,
        "maximum_split_depth": maximum_depth,
    }


def strict_face_p_derivative(frontier: dict[str, Any], face: str) -> dict[str, Any]:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    t_value = t0 if face == "LOWER_T_FACE" else t1
    stack = [(p0, p1, 0)]
    cells: list[dict[str, Any]] = []
    signs: set[str] = set()
    maximum_depth = 0
    while stack:
        pa, pb, depth = stack.pop()
        dual = target_factor(frontier, (t_value, t_value), (pa, pb), "p")
        need(type(dual) is Dual, "target p dual")
        sign = dual.derivative.sign()
        if sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}:
            cells.append({
                "p_interval": [qwire(pa), qwire(pb)],
                "derivative_interval_sha256": object_sha(dual.derivative.wire()),
                "sign": sign,
            })
            signs.add(sign)
            maximum_depth = max(maximum_depth, depth)
            continue
        need(depth < 12, "target face p derivative unresolved")
        middle = (pa + pb) / 2
        stack.extend(((pa, middle, depth + 1), (middle, pb, depth + 1)))
    need(len(signs) == 1, "target face p derivative sign")
    return {
        "face": face,
        "t_value": qwire(t_value),
        "strict_p_derivative_sign": next(iter(signs)),
        "proof_cell_count": len(cells),
        "maximum_split_depth": maximum_depth,
        "ordered_cell_receipts_sha256": object_sha(sorted(cells, key=lambda row: Q(row["p_interval"][0]["numerator"], row["p_interval"][0]["denominator"]))),
    }


def face_factor_receipt(frontier: dict[str, Any], face: str, p_side: str) -> dict[str, Any]:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    t_value = t0 if face == "LOWER_T_FACE" else t1
    p_value = p0 if p_side == "LOWER_P" else p1
    value = target_factor(frontier, (t_value, t_value), (p_value, p_value))
    need(type(value) is Interval and value.sign() in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, "strict target corner")
    return {
        "face": face,
        "p_side": p_side,
        "t_value": qwire(t_value),
        "p_value": qwire(p_value),
        "factor_sign": value.sign(),
        "factor_interval_sha256": object_sha(value.wire()),
    }


def isolate_face_root(
    graph_id: str,
    frontier: dict[str, Any],
    face: str,
    strict_p_derivative_sign: str,
) -> dict[str, Any] | None:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    t_value = t0 if face == "LOWER_T_FACE" else t1
    left = p0
    right = p1
    left_value = target_factor(frontier, (t_value, t_value), (left, left))
    right_value = target_factor(frontier, (t_value, t_value), (right, right))
    need(type(left_value) is Interval and type(right_value) is Interval, "face root endpoint interval")
    left_sign = left_value.sign()
    right_sign = right_value.sign()
    need(left_sign != "OVERWRAP" and right_sign != "OVERWRAP", "face root endpoint sign")
    if left_sign == right_sign:
        return None
    need({left_sign, right_sign} == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, "face root sign change")
    need(
        (strict_p_derivative_sign == "STRICT_POSITIVE" and left_sign == "STRICT_NEGATIVE")
        or (strict_p_derivative_sign == "STRICT_NEGATIVE" and left_sign == "STRICT_POSITIVE"),
        "face root monotone orientation",
    )
    for _ in range(ROOT_ISOLATION_STEPS):
        middle = (left + right) / 2
        middle_value = target_factor(frontier, (t_value, t_value), (middle, middle))
        need(type(middle_value) is Interval and middle_value.sign() != "OVERWRAP", "dyadic root midpoint sign")
        if middle_value.sign() == left_sign:
            left = middle
            left_value = middle_value
        else:
            right = middle
            right_value = middle_value
    need(left < right and left_value.sign() != right_value.sign(), "dyadic root bracket")
    core = {
        "descriptor_id": PREFIX + ":implicit-cut-root:" + object_sha([graph_id, face]),
        "face": face,
        "t_value": qwire(t_value),
        "equation_role": "PRIMITIVE_TARGET_FACTOR_AST_EQUALS_ZERO",
        "strict_p_derivative_sign": strict_p_derivative_sign,
        "dyadic_isolation_steps": ROOT_ISOLATION_STEPS,
        "isolation_interval": [qwire(left), qwire(right)],
        "left_factor_sign": left_value.sign(),
        "right_factor_sign": right_value.sign(),
        "left_factor_interval_sha256": object_sha(left_value.wire()),
        "right_factor_interval_sha256": object_sha(right_value.wire()),
        "existence_by_opposite_endpoint_signs": True,
        "uniqueness_by_strict_p_monotonicity": True,
    }
    return {**core, "descriptor_sha256": object_sha(core)}


def radical_receipts(frontier: dict[str, Any]) -> list[dict[str, Any]]:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    values = geometry(frontier["chart"], frontier["owner_target"], (t0, t1), (p0, p1), None)
    receipts = []
    for name in ("normal_radicand", "phase_radicand", "hit_radicand"):
        value = values[name]
        need(type(value) is Interval and value.lower > 0, "strict radical side condition:" + name)
        receipts.append({
            "radicand": name,
            "strictly_positive_on_carrier": True,
            "interval_sha256": object_sha(value.wire()),
        })
    return receipts


def bind_symbolic_radicands(
    receipts: list[dict[str, Any]],
    radicands: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    need({receipt["radicand"] for receipt in receipts} == set(radicands), "symbolic radicand names")
    bound = []
    for receipt in receipts:
        radicand = radicands[receipt["radicand"]]
        validate_primitive_ast(radicand, "radicand:" + receipt["radicand"])
        bound.append({
            **receipt,
            "primitive_radicand_ast_sha256": object_sha(radicand),
            "principal_nonnegative_square_root_semantics": True,
        })
    return bound


def closed_interval_ast(coordinate: str, lower: str, upper: str) -> dict[str, Any]:
    need(Q(lower) <= Q(upper), "AST interval")
    return {"op": "CLOSED_INTERVAL", "coordinate": coordinate, "lower": qstr(lower), "upper": qstr(upper)}


def and_ast(*arguments: dict[str, Any]) -> dict[str, Any]:
    return {"op": "AND", "args": list(arguments)}


def rational_ast(value: Q | int | str) -> dict[str, Any]:
    return {"op": "RATIONAL_CONSTANT", "value": qstr(value)}


def coordinate_ast(name: str) -> dict[str, Any]:
    need(name in {"t", "p", "s"}, "AST coordinate")
    return {"op": "COORDINATE", "name": name}


def add_ast(*arguments: dict[str, Any]) -> dict[str, Any]:
    return {"op": "ADD", "args": list(arguments)}


def multiply_ast(*arguments: dict[str, Any]) -> dict[str, Any]:
    return {"op": "MUL", "args": list(arguments)}


def negate_ast(argument: dict[str, Any]) -> dict[str, Any]:
    return {"op": "NEG", "arg": argument}


def square_ast(argument: dict[str, Any]) -> dict[str, Any]:
    return {"op": "SQUARE", "arg": argument}


def sqrt_ast(argument: dict[str, Any]) -> dict[str, Any]:
    return {"op": "SQRT_PRINCIPAL_NONNEGATIVE", "radicand": argument}


def source_frame_ast(
    chart: str,
    t_node: dict[str, Any],
    p_node: dict[str, Any],
) -> dict[str, Any]:
    one = rational_ast(1)
    normal_radicand = add_ast(one, negate_ast(square_ast(t_node)))
    phase_radicand = add_ast(one, negate_ast(square_ast(p_node)))
    normal_root = sqrt_ast(normal_radicand)
    phase_root = sqrt_ast(phase_radicand)
    need(chart in {"G:E", "G:W", "G:N", "G:S"}, "AST source chart")
    cell = chart[-1]
    if cell == "E":
        normal_x, normal_y = normal_root, t_node
    elif cell == "W":
        normal_x, normal_y = negate_ast(normal_root), t_node
    elif cell == "N":
        normal_x, normal_y = t_node, normal_root
    else:
        normal_x, normal_y = t_node, negate_ast(normal_root)
    tangent_x = add_ast(
        multiply_ast(phase_root, normal_x),
        negate_ast(multiply_ast(p_node, normal_y)),
    )
    tangent_y = add_ast(
        multiply_ast(phase_root, normal_y),
        multiply_ast(p_node, normal_x),
    )
    return {
        "normal_x": normal_x,
        "normal_y": normal_y,
        "tangent_x": tangent_x,
        "tangent_y": tangent_y,
        "normal_radicand": normal_radicand,
        "phase_radicand": phase_radicand,
    }


def target_factor_ast(
    semantic: dict[str, Any],
    t_value: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    parameters = semantic["kernel_parameters"]
    need(parameters["source_radius"] == qwire(Q(9, 25)), "AST G source radius")
    need(parameters["target_radius"] == qwire(Q(9, 25)), "AST G target radius")
    t_node = coordinate_ast("t") if t_value is None else rational_ast(t_value)
    p_node = coordinate_ast("p")
    frame = source_frame_ast(parameters["source_chart"], t_node, p_node)
    owner_kind, owner_x, owner_y = owner_xy(parameters["target_owner"])
    need(owner_kind == "G", "AST G target owner")
    source_radius = rational_ast(Q(9, 25))
    source_x = multiply_ast(source_radius, frame["normal_x"])
    source_y = multiply_ast(source_radius, frame["normal_y"])
    delta_x = add_ast(rational_ast(owner_x), negate_ast(source_x))
    delta_y = add_ast(rational_ast(owner_y), negate_ast(source_y))
    transverse = add_ast(
        multiply_ast(negate_ast(frame["tangent_y"]), delta_x),
        multiply_ast(frame["tangent_x"], delta_y),
    )
    hit_radicand = add_ast(
        rational_ast(Q(81, 625)),
        negate_ast(square_ast(transverse)),
    )
    radical = sqrt_ast(hit_radicand)
    hit_x = add_ast(
        rational_ast(owner_x),
        negate_ast(multiply_ast(radical, frame["tangent_x"])),
        multiply_ast(transverse, frame["tangent_y"]),
    )
    hit_y = add_ast(
        rational_ast(owner_y),
        negate_ast(multiply_ast(radical, frame["tangent_y"])),
        negate_ast(multiply_ast(transverse, frame["tangent_x"])),
    )
    need(parameters["wall_axis"] in {"X", "Y"}, "AST wall axis")
    hit = hit_x if parameters["wall_axis"] == "X" else hit_y
    factor = add_ast(hit, negate_ast(rational_ast(parameters["integer_wall"])))
    return factor, {
        "normal_radicand": frame["normal_radicand"],
        "phase_radicand": frame["phase_radicand"],
        "hit_radicand": hit_radicand,
    }


def r242_factor_ast(source_chart: str, target_lift: str) -> tuple[dict[str, Any], dict[str, Any]]:
    t_node = coordinate_ast("t")
    p_node = coordinate_ast("p")
    s_node = coordinate_ast("s")
    frame = source_frame_ast(source_chart, t_node, p_node)
    owner_kind, owner_x, owner_y = owner_xy(target_lift)
    source_radius = rational_ast(Q(9, 25))
    source_x = multiply_ast(source_radius, frame["normal_x"])
    source_y = multiply_ast(source_radius, frame["normal_y"])
    if owner_kind == "G":
        center_x = rational_ast(owner_x)
        center_y = rational_ast(owner_y)
        target_radius = Q(9, 25)
    else:
        need(owner_kind == "W", "AST R242 target obstacle kind")
        center_x = add_ast(rational_ast(Q(2 * owner_x + 1, 2)), s_node)
        center_y = rational_ast(Q(2 * owner_y + 1, 2))
        target_radius = Q(4, 25)
    delta_x = add_ast(center_x, negate_ast(source_x))
    delta_y = add_ast(center_y, negate_ast(source_y))
    transverse = add_ast(
        multiply_ast(negate_ast(frame["tangent_y"]), delta_x),
        multiply_ast(frame["tangent_x"], delta_y),
    )
    target_radicand = add_ast(
        rational_ast(target_radius * target_radius),
        negate_ast(square_ast(transverse)),
    )
    radical = sqrt_ast(target_radicand)
    inverse_target_radius = rational_ast(1 / target_radius)
    outgoing_x = multiply_ast(
        inverse_target_radius,
        add_ast(
            negate_ast(multiply_ast(radical, frame["tangent_x"])),
            multiply_ast(transverse, frame["tangent_y"]),
        ),
    )
    outgoing_y = multiply_ast(
        inverse_target_radius,
        add_ast(
            negate_ast(multiply_ast(radical, frame["tangent_y"])),
            negate_ast(multiply_ast(transverse, frame["tangent_x"])),
        ),
    )
    factor = add_ast(square_ast(outgoing_x), negate_ast(square_ast(outgoing_y)))
    return factor, {
        "normal_radicand": frame["normal_radicand"],
        "phase_radicand": frame["phase_radicand"],
        "target_hit_radicand": target_radicand,
    }


def zero_equation_ast(factor: dict[str, Any]) -> dict[str, Any]:
    return {"op": "EQ", "left": factor, "right": rational_ast(0)}


def closed_box_ast_from_axes(domain: dict[str, Any], label: str) -> tuple[dict[str, Any], dict[str, Any]]:
    need(
        type(domain) is dict
        and domain.get("wire_id") == "RATIONAL_INTERVAL_BOX_V1"
        and domain.get("coordinate_parameter") == "TPS"
        and type(domain.get("axes")) is list,
        "rational box:" + label,
    )
    axes: dict[str, tuple[Q, Q]] = {}
    for axis in domain["axes"]:
        need(
            type(axis) is dict
            and axis.get("axis") in {"t", "p", "s"}
            and axis.get("lower_closed") is True
            and axis.get("upper_closed") is True,
            "closed rational box axis:" + label,
        )
        name = axis["axis"]
        need(name not in axes, "unique rational box axis:" + label)
        lower = rational_from_wire(axis["lower"], label + ":" + name + ":lower")
        upper = rational_from_wire(axis["upper"], label + ":" + name + ":upper")
        need(lower <= upper, "ordered rational box axis:" + label)
        axes[name] = (lower, upper)
    need(set(axes) == {"t", "p", "s"}, "complete rational box axes:" + label)
    carrier = and_ast(*(closed_interval_ast(name, *axes[name]) for name in ("t", "p", "s")))
    base = and_ast(*(closed_interval_ast(name, *axes[name]) for name in ("p", "s")))
    return carrier, base


def validate_primitive_ast(value: Any, label: str) -> None:
    need(type(value) is dict and type(value.get("op")) is str, "AST node:" + label)
    operation = value["op"]
    if operation == "RATIONAL_CONSTANT":
        need(set(value) == {"op", "value"} and type(value["value"]) is str, "AST rational:" + label)
        need(qstr(value["value"]) == value["value"], "AST reduced rational:" + label)
        return
    if operation == "COORDINATE":
        need(set(value) == {"op", "name"} and value["name"] in {"t", "p", "s"}, "AST coordinate:" + label)
        return
    if operation in {"ADD", "MUL", "AND"}:
        need(set(value) == {"op", "args"} and type(value["args"]) is list and len(value["args"]) >= 1, "AST nary:" + label)
        for ordinal, argument in enumerate(value["args"]):
            validate_primitive_ast(argument, label + ":" + str(ordinal))
        return
    if operation in {"NEG", "SQUARE"}:
        need(set(value) == {"op", "arg"}, "AST unary:" + label)
        validate_primitive_ast(value["arg"], label + ":arg")
        return
    if operation == "SQRT_PRINCIPAL_NONNEGATIVE":
        need(set(value) == {"op", "radicand"}, "AST sqrt:" + label)
        validate_primitive_ast(value["radicand"], label + ":radicand")
        return
    if operation in {"EQ", "LT", "GT"}:
        need(set(value) == {"op", "left", "right"}, "AST binary relation:" + label)
        validate_primitive_ast(value["left"], label + ":left")
        validate_primitive_ast(value["right"], label + ":right")
        return
    if operation == "CLOSED_INTERVAL":
        need(
            set(value) == {"op", "coordinate", "lower", "upper"}
            and value["coordinate"] in {"t", "p", "s"}
            and type(value["lower"]) is str
            and type(value["upper"]) is str
            and qstr(value["lower"]) == value["lower"]
            and qstr(value["upper"]) == value["upper"]
            and Q(value["lower"]) <= Q(value["upper"]),
            "AST closed interval:" + label,
        )
        return
    if operation == "OR_DISJOINT":
        need(
            set(value) == {"op", "cases"}
            and type(value["cases"]) is list
            and len(value["cases"]) > 0,
            "AST cases:" + label,
        )
        allowed_cases = {
            "LOWER_NEGATIVE_UPPER_POSITIVE",
            "LOWER_POSITIVE_UPPER_NEGATIVE",
            "LOWER_ZERO",
            "UPPER_ZERO",
        }
        seen = set()
        for ordinal, case in enumerate(value["cases"]):
            need(
                type(case) is dict
                and set(case) == {"case", "predicate"}
                and case["case"] in allowed_cases
                and case["case"] not in seen,
                "AST disjoint case:" + label,
            )
            seen.add(case["case"])
            validate_primitive_ast(case["predicate"], label + ":case:" + str(ordinal))
        return
    raise Rejected("unrecognized AST operation:" + label + ":" + operation)


def target_base_domain_ast(semantic: dict[str, Any], box: list[str]) -> dict[str, Any]:
    lower_face = target_factor_ast(semantic, qstr(box[0]))[0]
    upper_face = target_factor_ast(semantic, qstr(box[1]))[0]
    zero = rational_ast(0)
    cases = [
        {
            "case": "LOWER_NEGATIVE_UPPER_POSITIVE",
            "predicate": and_ast(
                {"op": "LT", "left": lower_face, "right": zero},
                {"op": "GT", "left": upper_face, "right": zero},
            ),
        },
        {
            "case": "LOWER_POSITIVE_UPPER_NEGATIVE",
            "predicate": and_ast(
                {"op": "GT", "left": lower_face, "right": zero},
                {"op": "LT", "left": upper_face, "right": zero},
            ),
        },
        {"case": "LOWER_ZERO", "predicate": {"op": "EQ", "left": lower_face, "right": zero}},
        {"case": "UPPER_ZERO", "predicate": {"op": "EQ", "left": upper_face, "right": zero}},
    ]
    return and_ast(
        closed_interval_ast("p", box[2], box[3]),
        closed_interval_ast("s", box[4], box[5]),
        {"op": "OR_DISJOINT", "cases": cases},
    )


def target_topology_certificate(
    graph_id: str,
    frontier: dict[str, Any],
    lower_p_proof: dict[str, Any],
    upper_p_proof: dict[str, Any],
) -> dict[str, Any]:
    need(
        lower_p_proof["strict_p_derivative_sign"] == upper_p_proof["strict_p_derivative_sign"],
        "same-sign face p derivatives",
    )
    sign = lower_p_proof["strict_p_derivative_sign"]
    corners = [
        face_factor_receipt(frontier, face, side)
        for face in ("LOWER_T_FACE", "UPPER_T_FACE")
        for side in ("LOWER_P", "UPPER_P")
    ]
    by_key = {(row["face"], row["p_side"]): row["factor_sign"] for row in corners}
    domain_lower = by_key[("LOWER_T_FACE", "LOWER_P")] != by_key[("UPPER_T_FACE", "LOWER_P")]
    domain_upper = by_key[("LOWER_T_FACE", "UPPER_P")] != by_key[("UPPER_T_FACE", "UPPER_P")]
    roots = [
        root
        for face in ("LOWER_T_FACE", "UPPER_T_FACE")
        for root in (isolate_face_root(graph_id, frontier, face, sign),)
        if root is not None
    ]
    roots.sort(
        key=lambda row: Q(
            row["isolation_interval"][0]["numerator"],
            row["isolation_interval"][0]["denominator"],
        )
    )
    if len(roots) == 2:
        need(not domain_lower and not domain_upper, "internal p band boundary")
        left_upper = Q(roots[0]["isolation_interval"][1]["numerator"], roots[0]["isolation_interval"][1]["denominator"])
        right_lower = Q(roots[1]["isolation_interval"][0]["numerator"], roots[1]["isolation_interval"][0]["denominator"])
        need(left_upper < right_lower, "separated implicit p roots")
        topology = "INTERNAL_P_BAND"
        inherited = []
    elif len(roots) == 1 and domain_lower and not domain_upper:
        topology = "LOWER_P_ATTACHED"
        inherited = ["LOWER_P"]
    elif len(roots) == 1 and domain_upper and not domain_lower:
        topology = "UPPER_P_ATTACHED"
        inherited = ["UPPER_P"]
    elif len(roots) == 0 and domain_lower and domain_upper:
        topology = "FULL_P_INTERVAL"
        inherited = ["LOWER_P", "UPPER_P"]
    else:
        raise Rejected("unexpected target p topology")
    return {
        "topology": topology,
        "connected_sign_straddle_p_interval": True,
        "strict_same_sign_face_p_derivative": sign,
        "lower_t_face_p_derivative_proof": lower_p_proof,
        "upper_t_face_p_derivative_proof": upper_p_proof,
        "corner_sign_receipts": corners,
        "corner_sign_receipts_sha256": object_sha(corners),
        "implicit_cut_root_descriptors": roots,
        "implicit_cut_root_count": len(roots),
        "inherited_carrier_p_boundaries": inherited,
        "inherited_carrier_p_boundary_count": len(inherited),
        "s_independence": {
            "proved_by_free_variable_analysis": True,
            "factor_variables": ["t", "p"],
            "full_s_interval_retained": True,
        },
    }


def closed_row(core: dict[str, Any]) -> dict[str, Any]:
    return {**core, "row_sha256": object_sha(core)}


def row_ref(row: dict[str, Any], id_field: str = "row_id") -> dict[str, str]:
    return {"row_id": row[id_field], "row_sha256": row["row_sha256"]}


def validate_c9_result(result: dict[str, Any]) -> None:
    need(result["audit_census"]["positive_graph_domain_audit_rows"] == 5_264, "C9 graph census")
    need(result["audit_census"]["mechanical_relation_statement_rows"] == 15_392, "C9 mechanical denominator")
    need(result["audit_census"]["positive_graph_physical_relation_candidates"] == 15_382, "C9 positive denominator")
    need(result["audit_census"]["empty_graph_no_incidence_dispositions"] == 10, "C9 empty dispositions")
    need(all(value == 0 for value in result["formal_credit"].values()), "C9 zero credit")


def collect_filtered_rows(
    snapshot: Snapshot,
    member_ids: set[str],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    members: dict[str, dict[str, Any]] = {}
    g2a_member_count = 0
    for row in jsonl_rows(snapshot, "C7_MEMBER"):
        if row["coarse_family"] == "G2A":
            g2a_member_count += 1
            need(row["member_id"] in member_ids, "unexpected C7 G2A member")
        if row["member_id"] in member_ids:
            need(row["member_id"] not in members and row["coarse_family"] == "G2A", "C7 member bijection")
            need(row["support_semantic_state"] == "FRESH_MECHANICAL_IDENTITY_ONLY__FULL_SUPPORT_NOT_PROVED", "C7 support boundary")
            need(row["typed_support_ast"]["full_support_materialized"] is False, "C7 no old support")
            members[row["member_id"]] = row
    need(g2a_member_count == len(members) == 5_264 and set(members) == member_ids, "C7 G2A member exhaustion")

    representations: dict[str, dict[str, Any]] = {}
    g2a_representation_count = 0
    for row in jsonl_rows(snapshot, "C7_REPRESENTATION"):
        if row["coarse_family"] == "G2A":
            g2a_representation_count += 1
            need(row["owner_member_id"] in member_ids, "unexpected C7 G2A representation")
        if row["owner_member_id"] in member_ids:
            owner = row["owner_member_id"]
            need(owner not in representations and row["coarse_family"] == "G2A", "C7 representation bijection")
            need(row["representation_role"] == "G2A_GRAPH_SHEET_IDENTITY", "C7 representation role")
            need(row["pullback_semantic_state"] == "PULLBACK_EQUIVALENCE_NOT_PROVED", "C7 pullback boundary")
            representations[owner] = row
    need(g2a_representation_count == len(representations) == 5_264 and set(representations) == member_ids, "C7 G2A representation exhaustion")

    components: dict[str, dict[str, Any]] = {}
    for row in jsonl_rows(snapshot, "C6_MEMBER_COMPONENT"):
        member_id = row["registry_member_id"]
        if member_id in member_ids:
            need(member_id not in components and row["member_identity_preserved"] is True, "C6 member component binding")
            components[member_id] = row
    need(len(components) == 5_264 and set(components) == member_ids, "C6 component exhaustion")
    return members, representations, components


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


def ledger_descriptor(
    filename: str,
    row_schema: str,
    rows: list[dict[str, Any]],
    wire: bytes,
    plain: bytes,
) -> dict[str, Any]:
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


def build() -> tuple[dict[str, Any], bytes, bytes]:
    with Snapshot() as snapshot:
        bind_manifest(snapshot, "C9_MANIFEST", ("C9_RESULT", "C9_GRAPH"))
        bind_manifest(snapshot, "C7_MANIFEST", ("C7_MEMBER", "C7_REPRESENTATION"))
        bind_manifest(snapshot, "C6_MANIFEST", ("C6_MEMBER_COMPONENT",))
        bind_manifest(snapshot, "C5_MANIFEST", ("C5_SEMANTIC",))
        bind_manifest(snapshot, "C4_MANIFEST", ("C4_LEDGER",))
        bind_manifest(snapshot, "R234_MANIFEST", ("R234_CERT",))
        bind_manifest(snapshot, "R248_MANIFEST", ("R248_CERT",))
        bind_manifest(snapshot, "R245_MANIFEST", ("R245_CERT",))
        bind_manifest(snapshot, "R242_MANIFEST", ("R242_CERT",))

        c9_result = exact_closed_document(snapshot.read("C9_RESULT"), "result_sha256", "C9 result")
        validate_c9_result(c9_result)
        c9_graph_rows = list(jsonl_rows(snapshot, "C9_GRAPH"))
        need(len(c9_graph_rows) == 5_264, "C9 graph row count")
        c9_graph_rows.sort(key=lambda row: row["graph_inventory_ordinal"])
        need([row["graph_inventory_ordinal"] for row in c9_graph_rows] == sorted(row["graph_inventory_ordinal"] for row in c9_graph_rows), "C9 graph order")

        c5_by_semantic_id: dict[str, dict[str, Any]] = {}
        positive_count = 0
        for row in jsonl_rows(snapshot, "C5_SEMANTIC"):
            if row["semantic_classification"]["classification"] == "POSITIVE_GRAPH":
                positive_count += 1
                semantic_id = row["semantic_row_id"]
                need(semantic_id not in c5_by_semantic_id, "C5 semantic uniqueness")
                c5_by_semantic_id[semantic_id] = row
        need(positive_count == len(c5_by_semantic_id) == 5_264, "C5 positive exhaustion")

        c4_rows = list(jsonl_rows(snapshot, "C4_LEDGER"))
        need(len(c4_rows) == 16, "C4 bridge census")
        c4_rows.sort(key=lambda row: row["bridge_ordinal"])
        need([row["bridge_ordinal"] for row in c4_rows] == list(range(16)), "C4 bridge ordinal closure")
        c4_by_id = {row["bridge_row_id"]: row for row in c4_rows}
        need(len(c4_by_id) == 16, "C4 bridge uniqueness")

        r234 = legacy_document(snapshot.read("R234_CERT"), "R234")
        r234_rows = r234["result"]["depth6_frontier_rows"]
        need(len(r234_rows) == 38_376, "R234 frontier census")
        r248 = legacy_document(snapshot.read("R248_CERT"), "R248")
        r248_rows = r248["result"]["formal_wall_half_open_sheet_owner_ledger"]["rows"]
        need(len(r248_rows) == 38_360, "R248 sheet census")
        r248_by_member = {row["wall_sheet_node_id"]: row for row in r248_rows}
        need(len(r248_by_member) == len(r248_rows), "R248 sheet uniqueness")
        r245 = legacy_document(snapshot.read("R245_CERT"), "R245")
        r245_rows = r245["result"]["formal_retained_stratum_node_ledger"]["rows"]
        r245_by_member = {
            row["retained_stratum_node_id"]: row
            for row in r245_rows
            if row["stratum_kind"] == "HALF_OPEN_TRANSITION_SHEET"
        }
        need(len(r245_by_member) == 264, "R245 transition-sheet census")
        r242 = legacy_document(snapshot.read("R242_CERT"), "R242")
        r242_rows = r242["result"]["formal_positive_2D_transition_sheet_patch_ledger"]["rows"]
        need(len(r242_rows) == 264, "R242 transition-patch census")
        r242_by_id: dict[str, dict[str, Any]] = {}
        for ordinal, row in enumerate(r242_rows):
            need(type(row) is dict and row["transition_sheet_patch_row_id"] not in r242_by_id, "R242 row uniqueness")
            core = dict(row)
            claimed = core.pop("row_sha256", None)
            need(type(claimed) is str and claimed == object_sha(core), "R242 row closure")
            need(row["official_key_ordinal"] >= 0, "R242 official key ordinal")
            r242_by_id[row["transition_sheet_patch_row_id"]] = row

        graph_ids = [row["graph_id"] for row in c9_graph_rows]
        member_ids = [row["sheet_member_id"] for row in c9_graph_rows]
        c5_ids = [row["C5_semantic_row_id"] for row in c9_graph_rows]
        need(len(set(graph_ids)) == len(set(member_ids)) == len(set(c5_ids)) == 5_264, "C9 graph/member/C5 bijection")
        target_members = set(member_ids)
        c7_members, c7_representations, c6_components = collect_filtered_rows(snapshot, target_members)

        support_rows: list[dict[str, Any]] = []
        support_by_graph: dict[str, dict[str, Any]] = {}
        class_census: Counter[str] = Counter()
        topology_census: Counter[str] = Counter()
        face_p_sign_census: Counter[str] = Counter()
        target_t_sign_census: Counter[str] = Counter()
        internal_cut_root_count = 0
        inherited_p_boundary_count = 0

        for c9_row in c9_graph_rows:
            graph_id = c9_row["graph_id"]
            graph_class = c9_row["graph_class"]
            sheet_member_id = c9_row["sheet_member_id"]
            c5_row = c5_by_semantic_id.get(c9_row["C5_semantic_row_id"])
            need(c5_row is not None and c5_row["row_sha256"] == c9_row["C5_semantic_row_sha256"], "C9-C5 binding")
            need(c5_row["graph_id"] == graph_id, "C5 graph binding")
            semantic = c5_row["semantic_classification"]
            class_census[graph_class] += 1
            legacy_refs: dict[str, Any] = {}
            radical_side_conditions: list[dict[str, Any]] = []

            if graph_class == "R235_TARGET_POSITIVE_PARTIAL_BASE":
                need(semantic["kernel"] == "G_TARGET_FIRST_HIT_COORDINATE_MINUS_INTEGER_WALL_V1", "target kernel")
                box = semantic["complete_parameter_domain"]["box"]
                frontier_ref = c5_row["canonical_input_commitment"]["R234_frontier_row"]
                frontier = r234_rows[frontier_ref[0]]
                need(frontier["frontier_row_id"] == frontier_ref[1] and object_sha(frontier) == frontier_ref[2], "R234 target binding")
                need(frontier["box"] == box, "target carrier binding")
                expected_t = c9_row["exact_graph_domain_receipt"]["strict_t_derivative_proof"]["strict_t_derivative_sign"]
                t_proof = strict_target_t_derivative(frontier, expected_t)
                need(t_proof == c9_row["exact_graph_domain_receipt"]["strict_t_derivative_proof"], "C9 target t derivative replay")
                lower_p_proof = strict_face_p_derivative(frontier, "LOWER_T_FACE")
                upper_p_proof = strict_face_p_derivative(frontier, "UPPER_T_FACE")
                topology = target_topology_certificate(graph_id, frontier, lower_p_proof, upper_p_proof)
                topology_census[topology["topology"]] += 1
                face_p_sign_census[topology["strict_same_sign_face_p_derivative"]] += 1
                target_t_sign_census[expected_t] += 1
                internal_cut_root_count += topology["implicit_cut_root_count"]
                inherited_p_boundary_count += topology["inherited_carrier_p_boundary_count"]
                factor_node, symbolic_radicands = target_factor_ast(semantic)
                equation_node = zero_equation_ast(factor_node)
                carrier_ast = and_ast(
                    closed_interval_ast("t", box[0], box[1]),
                    closed_interval_ast("p", box[2], box[3]),
                    closed_interval_ast("s", box[4], box[5]),
                )
                base_ast = target_base_domain_ast(semantic, box)
                support_ast = and_ast(carrier_ast, base_ast, equation_node)
                radical_side_conditions = bind_symbolic_radicands(
                    radical_receipts(frontier),
                    symbolic_radicands,
                )
                monotone_certificate = {
                    "kind": "STRICT_T_MONOTONE_IMPLICIT_GRAPH_OVER_CONNECTED_SIGN_STRADDLE_BASE",
                    "strict_t_derivative_proof": t_proof,
                    "unique_t_for_every_exact_base_point": True,
                    "face_p_topology_certificate": topology,
                }
                legacy_refs = {
                    "R234_frontier": {"ordinal": frontier_ref[0], "row_id": frontier_ref[1], "row_sha256": frontier_ref[2]},
                    "R248_outer_envelope": c9_row["legacy_sheet_geometry_scope"],
                }
                need(legacy_refs["R248_outer_envelope"]["disposition"] == "OUTER_ENVELOPE_ONLY__NOT_FULL_GRAPH_SUPPORT", "R248 target nonpromotion")
                support_properties = {
                    "nonempty": True,
                    "connected": True,
                    "one_graph_point_per_exact_base_point": True,
                    "s_independent_equation": True,
                    "R248_rectangle_used_as_support": False,
                }
            elif graph_class == "R235_SOURCE_EXACT_FACE_FULL_BASE":
                need(semantic["kernel"] == "EXACT_SOURCE_COORDINATE_MINUS_ZERO_EQUALS_9_OVER_25_TIMES_T", "R235 source kernel")
                box = semantic["complete_parameter_domain"]["box"]
                carrier_ast = and_ast(
                    closed_interval_ast("t", box[0], box[1]),
                    closed_interval_ast("p", box[2], box[3]),
                    closed_interval_ast("s", box[4], box[5]),
                )
                base_ast = and_ast(closed_interval_ast("p", box[2], box[3]), closed_interval_ast("s", box[4], box[5]))
                source_factor = multiply_ast(rational_ast(Q(9, 25)), coordinate_ast("t"))
                equation_node = zero_equation_ast(source_factor)
                support_ast = and_ast(carrier_ast, base_ast, equation_node)
                need(semantic["strict_t_derivative_exact"] == qwire(Q(9, 25)), "R235 exact derivative")
                monotone_certificate = {
                    "kind": "EXPLICIT_T_EQUALS_ZERO_FULL_BASE_GRAPH",
                    "strict_t_derivative_exact": semantic["strict_t_derivative_exact"],
                    "unique_t_for_every_exact_base_point": True,
                }
                legacy_refs = {"R248_identity_and_exact_base_lineage": c9_row["legacy_sheet_geometry_scope"]}
                support_properties = {
                    "nonempty": True,
                    "connected": True,
                    "one_graph_point_per_exact_base_point": True,
                    "s_independent_equation": True,
                    "R248_rectangle_used_as_support": False,
                    "R248_rectangle_used_as_base_coordinate_input": True,
                }
            elif graph_class == "R235D_SOURCE_EXACT_FACE_FULL_BASE":
                need(semantic["kernel"] == "SEALED_C4_R235D_SOURCE_EXACT_FACE_GRAPH_BRIDGE", "R235D source kernel")
                c4_ref = c5_row["canonical_input_commitment"]["C4_bridge_row"]
                need(type(c4_ref) is list and len(c4_ref) == 3, "C4 bridge reference shape")
                bridge = c4_by_id.get(c4_ref[1])
                need(
                    bridge is not None
                    and bridge["bridge_ordinal"] == c4_ref[0]
                    and object_sha(bridge) == c4_ref[2],
                    "C4 bridge reference binding",
                )
                source_graph_ref = bridge["canonical_input_commitment"]["B1G0_source_graph_row"]
                need(
                    source_graph_ref[0] == c9_row["graph_inventory_ordinal"]
                    and source_graph_ref[1] == c9_row["graph_inventory_row_id"],
                    "C4 source graph binding",
                )
                reconstruction = bridge["semantic_reconstruction"]
                expected_c4_source_factor_ast = {
                    "op": "SUB",
                    "left": {
                        "op": "MUL",
                        "args": [
                            {"op": "CONST_Q", "value": qwire(Q(9, 25))},
                            {"op": "VAR", "name": "t"},
                        ],
                    },
                    "right": {"op": "CONST_Q", "value": qwire(0)},
                }
                expected_c4_source_t_derivative_ast = {
                    "op": "SUB",
                    "left": {
                        "op": "ADD",
                        "args": [
                            {
                                "op": "MUL",
                                "args": [
                                    {"op": "CONST_Q", "value": qwire(0)},
                                    {"op": "VAR", "name": "t"},
                                ],
                            },
                            {
                                "op": "MUL",
                                "args": [
                                    {"op": "CONST_Q", "value": qwire(Q(9, 25))},
                                    {"op": "CONST_Q", "value": qwire(1)},
                                ],
                            },
                        ],
                    },
                    "right": {"op": "CONST_Q", "value": qwire(0)},
                }
                need(
                    semantic["C4_source_semantic_commitment_sha256"] == object_sha(reconstruction)
                    and reconstruction["source_factor_ast"] == expected_c4_source_factor_ast
                    and reconstruction["source_t_derivative_ast"] == expected_c4_source_t_derivative_ast
                    and reconstruction["source_zero_set"] == "EXACT_FACE_GRAPH_t_EQUALS_0"
                    and reconstruction["source_zero_face"] in {"LOWER", "UPPER"}
                    and reconstruction["source_graph_dimension"] == 2
                    and reconstruction["complete_domain_partition_verified"] is True
                    and reconstruction["complete_domain_partition_cell_count"] == 4,
                    "C4 source semantic closure",
                )
                derivative_interval = reconstruction["source_t_derivative_exact_interval"]
                need(
                    rational_from_wire(derivative_interval["lower"], "C4 derivative lower") == Q(9, 25)
                    and rational_from_wire(derivative_interval["upper"], "C4 derivative upper") == Q(9, 25),
                    "C4 exact source derivative",
                )
                complete_domain = reconstruction["complete_parameter_domain"]
                carrier_ast, base_ast = closed_box_ast_from_axes(complete_domain, "C4 complete parameter domain")
                rectangle = c9_row["legacy_sheet_geometry_scope"]["rectangle"]
                need(len(rectangle) == 4, "R235D rectangle")
                axes = {axis["axis"]: axis for axis in complete_domain["axes"]}
                need(
                    rectangle == [
                        qstr(rational_from_wire(axes["p"]["lower"], "C4 p lower")),
                        qstr(rational_from_wire(axes["p"]["upper"], "C4 p upper")),
                        qstr(rational_from_wire(axes["s"]["lower"], "C4 s lower")),
                        qstr(rational_from_wire(axes["s"]["upper"], "C4 s upper")),
                    ],
                    "C4-R248 exact base coordinate binding",
                )
                source_factor = multiply_ast(rational_ast(Q(9, 25)), coordinate_ast("t"))
                equation_node = zero_equation_ast(source_factor)
                support_ast = and_ast(carrier_ast, base_ast, equation_node)
                need(
                    c9_row["exact_graph_domain_receipt"]["C4_bridge_row_sha256"] == bridge["row_sha256"]
                    and c9_row["exact_graph_domain_receipt"]["complete_parameter_domain_sha256"] == object_sha(complete_domain),
                    "C9-C4 exact domain receipt",
                )
                monotone_certificate = {
                    "kind": "SEALED_EXPLICIT_T_EQUALS_ZERO_FULL_BASE_GRAPH",
                    "C4_bridge_ref": {
                        "ordinal": bridge["bridge_ordinal"],
                        "row_id": bridge["bridge_row_id"],
                        "row_sha256": bridge["row_sha256"],
                        "full_row_sha256": object_sha(bridge),
                    },
                    "strict_t_derivative_exact": qwire(Q(9, 25)),
                    "C9_exact_domain_receipt": c9_row["exact_graph_domain_receipt"],
                    "unique_t_for_every_exact_base_point": True,
                }
                legacy_refs = {
                    "C4_exact_source_semantic_authority": monotone_certificate["C4_bridge_ref"],
                    "R248_identity_and_base_coordinate_lineage": c9_row["legacy_sheet_geometry_scope"],
                }
                support_properties = {
                    "nonempty": True,
                    "connected": True,
                    "one_graph_point_per_exact_base_point": True,
                    "s_independent_equation": True,
                    "R248_rectangle_used_as_support": False,
                    "R248_rectangle_used_as_base_coordinate_input": True,
                }
            elif graph_class == "R242_UNIQUE_GRAPH_FULL_PATCH":
                need(semantic["kernel"] == "SEALED_R242_UNIQUE_TRANSITION_GRAPH_PATCH_BRIDGE", "R242 kernel")
                r242_ref = c5_row["canonical_input_commitment"]["R242_positive_patch_row"]
                need(type(r242_ref) is list and len(r242_ref) == 4, "R242 patch reference shape")
                r242_row = r242_by_id.get(r242_ref[1])
                need(
                    r242_row is not None
                    and r242_rows[r242_ref[0]] is r242_row
                    and object_sha(r242_row) == r242_ref[2]
                    and r242_row["row_sha256"] == r242_ref[3]
                    and r242_row["transition_sheet_patch_row_id"] == graph_id,
                    "R242 patch reference binding",
                )
                box = semantic["closed_witness_box"]
                need(
                    r242_row["closed_witness_box"] == box
                    and r242_row["equation"] == semantic["equation"] == "target_normal_x^2-target_normal_y^2=0"
                    and r242_row["strict_t_derivative_sign"] == semantic["strict_t_derivative_sign"]
                    and r242_row["lower_t_face_F_sign"] == semantic["lower_t_face_F_sign"]
                    and r242_row["upper_t_face_F_sign"] == semantic["upper_t_face_F_sign"]
                    and r242_row["unique_graph_point_for_every_closed_base_point"] is True,
                    "R242 patch semantic closure",
                )
                retained_source = r245_by_member.get(sheet_member_id)
                need(retained_source is not None, "R242 retained source")
                local_signature = retained_source["local_return_signature"]
                need(
                    local_signature["source_chart"] == r242_row["source_chart"]
                    and local_signature["target_lift"] == r242_row["target_lift"]
                    and retained_source["Round220_split_interface_id"] == r242_row["Round220_split_interface_id"]
                    and retained_source["Round179_retained_child_row_id"] == r242_row["Round179_retained_child_row_id"],
                    "R242-R245 chart/lift lineage",
                )
                carrier_ast = and_ast(
                    closed_interval_ast("t", box[0], box[1]),
                    closed_interval_ast("p", box[2], box[3]),
                    closed_interval_ast("s", box[4], box[5]),
                )
                base_ast = and_ast(closed_interval_ast("p", box[2], box[3]), closed_interval_ast("s", box[4], box[5]))
                factor_node, symbolic_radicands = r242_factor_ast(r242_row["source_chart"], r242_row["target_lift"])
                equation_node = zero_equation_ast(factor_node)
                support_ast = and_ast(carrier_ast, base_ast, equation_node)
                r242_bound_ref = {
                    "ordinal": r242_ref[0],
                    "row_id": r242_row["transition_sheet_patch_row_id"],
                    "row_sha256": r242_row["row_sha256"],
                    "full_row_sha256": object_sha(r242_row),
                }
                radical_side_conditions = []
                for radicand_name, radicand_node in symbolic_radicands.items():
                    validate_primitive_ast(radicand_node, "R242 radicand:" + radicand_name)
                    radical_side_conditions.append({
                        "radicand": radicand_name,
                        "strictly_positive_on_carrier": True,
                        "primitive_radicand_ast_sha256": object_sha(radicand_node),
                        "sealed_R242_patch_ref": r242_bound_ref,
                        "principal_nonnegative_square_root_semantics": True,
                    })
                monotone_certificate = {
                    "kind": "SEALED_R242_STRICT_T_MONOTONE_UNIQUE_FULL_PATCH_GRAPH",
                    "strict_t_derivative_sign": semantic["strict_t_derivative_sign"],
                    "lower_t_face_F_sign": semantic["lower_t_face_F_sign"],
                    "upper_t_face_F_sign": semantic["upper_t_face_F_sign"],
                    "unique_t_for_every_exact_base_point": True,
                }
                legacy_refs = {
                    "R242_exact_patch_authority": r242_bound_ref,
                    "R245_retained_stratum_identity_lineage": {
                        "member_id": sheet_member_id,
                        "row_sha256": retained_source["row_sha256"],
                    },
                }
                support_properties = {
                    "nonempty": True,
                    "connected": True,
                    "one_graph_point_per_exact_base_point": True,
                    "s_independent_equation": False,
                    "R248_rectangle_used_as_support": False,
                }
            else:
                raise Rejected("unknown C9 graph class:" + graph_class)

            for ast_name, ast_value in (
                ("carrier_domain", carrier_ast),
                ("base_domain", base_ast),
                ("equation", equation_node),
                ("exact_support", support_ast),
            ):
                validate_primitive_ast(ast_value, graph_id + ":" + ast_name)
            ast_hashes = {
                "carrier_domain_ast_sha256": object_sha(carrier_ast),
                "base_domain_ast_sha256": object_sha(base_ast),
                "equation_ast_sha256": object_sha(equation_node),
                "exact_support_ast_sha256": object_sha(support_ast),
            }
            core = {
                "schema": SUPPORT_ROW_SCHEMA,
                "row_id": PREFIX + ":exact-graph-support:" + object_sha([graph_id, sheet_member_id]),
                "graph_ordinal": c9_row["graph_inventory_ordinal"],
                "graph_id": graph_id,
                "graph_class": graph_class,
                "sheet_member_id": sheet_member_id,
                "C9_graph_ref": row_ref(c9_row),
                "C5_semantic_ref": {"row_id": c5_row["semantic_row_id"], "row_sha256": c5_row["row_sha256"]},
                "legacy_source_refs": legacy_refs,
                "coordinate_parameter": "TPS",
                "carrier_domain_ast": carrier_ast,
                "base_domain_ast": base_ast,
                "equation_ast": equation_node,
                "exact_support_ast": support_ast,
                "ast_sha256": ast_hashes,
                "radical_side_condition_receipts": radical_side_conditions,
                "monotone_graph_certificate": monotone_certificate,
                "source_lineage_certificate": {
                    "C9_graph_row_bound": True,
                    "C5_positive_graph_row_bound": True,
                    "fresh_member_universe": "ROUND306C6",
                    "legacy_geometry_role": "CONSTRUCTION_OR_IDENTITY_LINEAGE_ONLY",
                },
                "support_properties": support_properties,
                "scoped_credit": {
                    "exact_G2_feature_support_AST": 1,
                    "member_natural_key_preservation": 0,
                },
                "downstream_nonpromotion": DOWNSTREAM_ZERO,
            }
            support_row = closed_row(core)
            support_rows.append(support_row)
            support_by_graph[graph_id] = support_row

        need(len(support_rows) == len(support_by_graph) == 5_264, "support row exhaustion")
        need(dict(class_census) == CLASS_CENSUS, "support class census")
        need(dict(topology_census) == {key: value for key, value in TARGET_TOPOLOGY_CENSUS.items() if value}, "target topology census")
        need(face_p_sign_census == {"STRICT_POSITIVE": 2_216, "STRICT_NEGATIVE": 2_216}, "target face p sign census")
        need(target_t_sign_census == {"STRICT_POSITIVE": 3_932, "STRICT_NEGATIVE": 500}, "target t sign census")
        need(internal_cut_root_count == 8_392 and inherited_p_boundary_count == 472, "target cut boundary census")

        identity_rows: list[dict[str, Any]] = []
        natural_key_hashes: set[str] = set()
        identity_source_census: Counter[str] = Counter()
        for support_row in support_rows:
            graph_id = support_row["graph_id"]
            member_id = support_row["sheet_member_id"]
            graph_class = support_row["graph_class"]
            if graph_class == "R242_UNIQUE_GRAPH_FULL_PATCH":
                source = r245_by_member.get(member_id)
                need(source is not None, "R245 identity source")
                source_core = dict(source)
                claimed_source_sha = source_core.pop("row_sha256")
                need(claimed_source_sha == object_sha(source_core), "R245 identity source closure")
                natural_key = [
                    source["Round220_split_interface_id"],
                    source["Round179_retained_child_row_id"],
                    source["stratum_kind"],
                    source["local_return_signature"],
                ]
                recomputed = "round245-retained-stratum:" + object_sha(natural_key)
                legacy_source = {
                    "kind": "R245_RETAINED_STRATUM_NATURAL_KEY",
                    "row_id": source["retained_stratum_node_id"],
                    "row_sha256": source["row_sha256"],
                    "support_geometry_is_natural_key_input": False,
                }
                identity_source_census["R245"] += 1
            else:
                source = r248_by_member.get(member_id)
                need(source is not None, "R248 identity source")
                source_core = dict(source)
                claimed_source_sha = source_core.pop("row_sha256")
                need(claimed_source_sha == object_sha(source_core), "R248 identity source closure")
                natural_key = [
                    source["source_partition_kind"],
                    source["source_partition_row_id"],
                    source["endpoint_factor"],
                    source["owner_signature_sha256"],
                ]
                recomputed = "round248-wall-sheet:" + object_sha(natural_key)
                legacy_source = {
                    "kind": "R248_WALL_SHEET_NATURAL_KEY",
                    "row_id": source["wall_sheet_node_id"],
                    "row_sha256": source["row_sha256"],
                    "outer_envelope_rectangle_is_natural_key_input": False,
                }
                identity_source_census["R248"] += 1
            natural_key_sha = object_sha(natural_key)
            need(natural_key_sha not in natural_key_hashes, "natural key uniqueness")
            natural_key_hashes.add(natural_key_sha)
            need(recomputed == member_id, "natural key member replay")
            c7_member = c7_members[member_id]
            c7_representation = c7_representations[member_id]
            c6_component = c6_components[member_id]
            need(c7_member["C6_member_component_row_id"] == c6_component["row_id"], "C7-C6 member row binding")
            need(c7_representation["owner_member_row_id"] == c7_member["row_id"], "C7 representation-member binding")
            core = {
                "schema": IDENTITY_ROW_SCHEMA,
                "row_id": PREFIX + ":member-identity-disposition:" + object_sha([graph_id, member_id]),
                "graph_ordinal": support_row["graph_ordinal"],
                "graph_id": graph_id,
                "graph_class": graph_class,
                "sheet_member_id": member_id,
                "exact_support_ref": row_ref(support_row),
                "C7_member_ref": row_ref(c7_member),
                "C7_representation_ref": row_ref(c7_representation),
                "C6_member_component_ref": row_ref(c6_component),
                "legacy_identity_source": legacy_source,
                "natural_key_preimage": natural_key,
                "natural_key_preimage_sha256": natural_key_sha,
                "recomputed_member_id": recomputed,
                "identity_prerequisites": {
                    "exact_support_nonempty": support_row["support_properties"]["nonempty"],
                    "exact_support_connected": support_row["support_properties"]["connected"],
                    "one_graph_inventory_row_per_member_natural_key": True,
                    "natural_key_graph_member_pair_bijection": True,
                    "support_rematerialization_changes_natural_key": False,
                    "split_count": 0,
                    "merge_count": 0,
                },
                "disposition": "PRESERVE_EXISTING_MEMBER_ID",
                "member_natural_key_preservation_credit": 1,
                "set_equality_proved": False,
                "physical_incidence_proved": False,
                "identity_representation_pullback_proved": False,
                "downstream_nonpromotion": DOWNSTREAM_ZERO,
            }
            identity_rows.append(closed_row(core))

        need(len(identity_rows) == len(natural_key_hashes) == 5_264, "identity row exhaustion")
        need(identity_source_census == {"R248": 5_000, "R245": 264}, "identity source census")
        need(all(row["disposition"] == "PRESERVE_EXISTING_MEMBER_ID" for row in identity_rows), "identity preservation")

        support_wire, support_plain = gzip_rows(support_rows)
        identity_wire, identity_plain = gzip_rows(identity_rows)
        support_descriptor = ledger_descriptor(SUPPORT_LEDGER_NAME, SUPPORT_ROW_SCHEMA, support_rows, support_wire, support_plain)
        identity_descriptor = ledger_descriptor(IDENTITY_LEDGER_NAME, IDENTITY_ROW_SCHEMA, identity_rows, identity_wire, identity_plain)
        body = {
            "schema": SCHEMA,
            "status": STATUS,
            "producer_source": producer_record(),
            "source_pins": [pin.__dict__ for pin in PINS],
            "upstream_seal_bindings": {
                "C9_manifest_sha256": PIN_BY_ROLE["C9_MANIFEST"].sha256,
                "C7_manifest_sha256": PIN_BY_ROLE["C7_MANIFEST"].sha256,
                "C6_manifest_sha256": PIN_BY_ROLE["C6_MANIFEST"].sha256,
                "C5_manifest_sha256": PIN_BY_ROLE["C5_MANIFEST"].sha256,
                "C4_manifest_sha256": PIN_BY_ROLE["C4_MANIFEST"].sha256,
                "R234_manifest_sha256": PIN_BY_ROLE["R234_MANIFEST"].sha256,
                "R248_manifest_sha256": PIN_BY_ROLE["R248_MANIFEST"].sha256,
                "R245_manifest_sha256": PIN_BY_ROLE["R245_MANIFEST"].sha256,
                "R242_manifest_sha256": PIN_BY_ROLE["R242_MANIFEST"].sha256,
            },
            "support_census": {
                "exact_G2_feature_support_AST_rows": 5_264,
                "graph_class_census": CLASS_CENSUS,
                "R235_target_topology_census": TARGET_TOPOLOGY_CENSUS,
                "R235_target_face_p_derivative_sign_census": {"STRICT_POSITIVE": 2_216, "STRICT_NEGATIVE": 2_216},
                "R235_target_t_derivative_sign_census": {"STRICT_POSITIVE": 3_932, "STRICT_NEGATIVE": 500},
                "R235_target_internal_cut_root_descriptors": 8_392,
                "R235_target_inherited_p_boundaries": 472,
            },
            "identity_census": {
                "member_natural_key_preservation_rows": 5_264,
                "PRESERVE_EXISTING_MEMBER_ID": 5_264,
                "REKEY_REQUIRED": 0,
                "R248_natural_key_rows": 5_000,
                "R245_natural_key_rows": 264,
                "split_count": 0,
                "merge_count": 0,
            },
            "C9_denominator_preserved": {
                "mechanical_relation_statements": 15_392,
                "positive_graph_relation_candidates": 15_382,
                "empty_graph_no_incidence_dispositions": 10,
                "remaining_physical_incidence_theorem_rows": 15_382,
                "remaining_representation_pullback_theorem_rows": 15_382,
                "remaining_one_sided_trace_rows": 10_118,
            },
            "scoped_credit": {
                "exact_G2_feature_support_AST": 5_264,
                "member_natural_key_preservation": 5_264,
            },
            "formal_credit": DOWNSTREAM_ZERO,
            "strict_nonpromotion": {
                "graph_to_sheet_set_equality_proved": False,
                "physical_incidence_proved": False,
                "representation_pullback_proved": False,
                "one_sided_trace_proved": False,
                "C7_semantic_gap_rows_closed": 0,
                "member_normalized_support_sealed": False,
                "global_normalized_support_sealed": False,
                "B1A_permitted": False,
                "B2_permitted": False,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "exact_graph_support_ledger": support_descriptor,
            "member_identity_disposition_ledger": identity_descriptor,
            "required_next": {
                "prove_15382_graph_sheet_or_side_physical_relations": True,
                "prove_15382_representation_pullbacks": True,
                "prove_10118_one_sided_traces": True,
                "close_non_G2_family_support_kernels": True,
                "build_497772_member_normalized_support_ledger": True,
                "B1A": "NOT_AUTHORIZED",
                "B2": "NOT_AUTHORIZED",
            },
            "seed_serialized_or_semantically_used": False,
        }
        result = {**body, "result_sha256": object_sha(body)}
        snapshot.final()
    return result, support_wire, identity_wire


def write_once(directory: Path, filename: str, payload: bytes) -> None:
    path = directory / filename
    need(not path.exists(), "publish no-clobber:" + filename)
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
        0o600,
    )
    try:
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            need(written > 0, "publish progress:" + filename)
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    info = os.stat(path, follow_symlinks=False)
    need(
        stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(payload),
        "published file:" + filename,
    )


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-result", action="store_true")
    parser.add_argument("--candidate-dir")
    parser.add_argument("--publish", action="store_true")
    arguments = parser.parse_args()
    need(
        sum((arguments.print_result, arguments.candidate_dir is not None, arguments.publish)) == 1,
        "exactly one mode",
    )
    result, support_wire, identity_wire = build()
    result_wire = canonical(result)
    if arguments.print_result:
        sys.stdout.buffer.write(result_wire + b"\n")
        return 0
    if arguments.publish:
        directory = ROOT
    else:
        directory = Path(arguments.candidate_dir).resolve()
        need(
            os.path.commonpath((str(directory), str(ROOT.resolve()))) != str(ROOT.resolve()),
            "candidate outside deliverables",
        )
        directory.mkdir(mode=0o700, parents=False, exist_ok=False)
    payloads = (
        (SUPPORT_LEDGER_NAME, support_wire),
        (IDENTITY_LEDGER_NAME, identity_wire),
        (RESULT_NAME, result_wire),
    )
    records = []
    for filename, payload in payloads:
        write_once(directory, filename, payload)
        records.append({
            "filename": filename,
            "size": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
    for record in reversed(records):
        info = os.stat(directory / record["filename"], follow_symlinks=False)
        need(
            stat.S_ISREG(info.st_mode)
            and info.st_nlink == 1
            and info.st_size == record["size"],
            "reverse publication identity",
        )
        descriptor = os.open(
            directory / record["filename"],
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        try:
            need(hash_fd(descriptor) == record["sha256"], "reverse publication digest")
        finally:
            os.close(descriptor)
    print(json.dumps({
        "status": result["status"],
        "result_sha256": result["result_sha256"],
        "published_result_last": True,
        "files": records,
    }, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
