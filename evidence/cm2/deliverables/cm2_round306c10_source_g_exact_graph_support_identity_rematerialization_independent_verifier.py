#!/usr/bin/env python3
"""Independent verifier for Round306C10 exact G2 support rematerialization.

The verifier deliberately does not import, execute, or parse the producer.  It
reconstructs the semantic support and identity obligations directly from held,
hash-pinned upstream artifacts.  Candidate rows, theorem-credit fields, and
nonpromotion fields are closed and fail-closed.
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
import shutil
import stat
import sys
import tempfile
from typing import Any, Final, Iterator, Mapping


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
STATUS: Final = (
    "PASS_5264_EXACT_G2_FEATURE_SUPPORT_ASTS__5264_NATURAL_KEY_IDENTITIES_"
    "PRESERVED__ZERO_PHYSICAL_PULLBACK_TRACE_GLOBAL_SUPPORT_CREDIT"
)

PRODUCER_NAME: Final = PREFIX + "_producer.py"
SUPPORT_NAME: Final = PREFIX + "_exact_graph_support_ledger.jsonl.gz"
IDENTITY_NAME: Final = PREFIX + "_member_identity_disposition_ledger.jsonl.gz"
RESULT_NAME: Final = PREFIX + "_result.json"
ATTACK_NAME: Final = PREFIX + "_attack_suite.json"
VERIFICATION_NAME: Final = PREFIX + "_verification.json"
REPORT_NAME: Final = PREFIX + "_report.md"
COLD_NAME: Final = PREFIX + "_cold_replay.md"
MANIFEST_NAME: Final = PREFIX + "_manifest.sha256"
OUTPUT_NAMES: Final = (SUPPORT_NAME, IDENTITY_NAME, RESULT_NAME)

CLASS_COUNTS: Final = {
    "R235_TARGET_POSITIVE_PARTIAL_BASE": 4_432,
    "R235_SOURCE_EXACT_FACE_FULL_BASE": 552,
    "R235D_SOURCE_EXACT_FACE_FULL_BASE": 16,
    "R242_UNIQUE_GRAPH_FULL_PATCH": 264,
}

TARGET_TOPOLOGY_COUNTS: Final = {
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

SQRT_BITS: Final = 224
ROOT_ISOLATION_STEPS: Final = 48
OWNER_RE: Final = re.compile(r"^([GW])\[(-?[0-9]+),(-?[0-9]+)\]$")


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


# C10's authority is intentionally narrow.  C9 supplies the live positive
# graph census; C7/C6 supply current identities; C5/R234 supply formula and
# domain semantics; R248/R245 supply the two current natural-key constructors.
SOURCE_PINS: Final = (
    Pin("C9_MANIFEST", "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_manifest.sha256", 1_396, "8921fb3eadd5d8b4aec1afe3af91c938b2c5568e9f9ef3be64002e4146152d04"),
    Pin("C9_RESULT", "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_result.json", 8_845, "31d8da4e4a3e6ad703bd24fd7456f801d3fd90293e171d9784b2280d393b76a8"),
    Pin("C9_GRAPH", "cm2_round306c9_source_g_g2_relation_admissibility_and_envelope_audit_graph_domain_audit_ledger.jsonl.gz", 2_488_534, "955d8930fc321ca4f2556d66af488e4b9391f91002b65ecf8eaace6fbd3a7d50"),
    Pin("C7_MANIFEST", "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_manifest.sha256", 2_184, "4e534e412a760d13fe7eb278ca063e86ac2a7164bbfdb3b14a3142219267c0c6"),
    Pin("C7_MEMBER", "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_member_identity_support_ledger.jsonl.gz", 269_633_111, "de85e6f26b64299d70c5006df76c5e4a242dc46d5b4885bca1f37b13d923c4e0"),
    Pin("C7_REPRESENTATION", "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_representation_ledger.jsonl.gz", 240_400_592, "1dc805b60f15ec8491b5200ccf9f04a239ce1532f6845a026045709feaaaa468"),
    Pin("C6_MANIFEST", "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_manifest.sha256", 2_211, "d9c3261421a966f62eeb027517f0f0e58ab2f3f72d856fed5cdcced55ff158f2"),
    Pin("C6_MEMBER_COMPONENT", "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_component_ledger.jsonl.gz", 213_125_489, "730a1501402d29f9689655b0093edd4d7e499f3a34c6b65e9f21ee6f3f5ffce2"),
    Pin("C5_MANIFEST", "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_manifest.sha256", 1_193, "aefe82ef88c2ddf5f241d76e0f0f7483e230d68219ace6639f7389adbcb14134"),
    Pin("C5_SEMANTIC", "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz", 78_082_824, "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"),
    Pin("C4_MANIFEST", "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_manifest.sha256", 1_177, "5550eb9cf4e474a8d08086062e28538e909f6e1c7e499ba10a78a2d24e683de6"),
    Pin("C4_LEDGER", "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz", 101_147, "3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),
    Pin("R234_MANIFEST", "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_manifest.sha256", 574, "f8714ecdf804657fc6633136544f567b07e7d8503095d17fcda19226feefc432"),
    Pin("R234_CERT", "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    Pin("R248_MANIFEST", "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256", 885, "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07"),
    Pin("R248_CERT", "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json", 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
    Pin("R245_MANIFEST", "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_manifest.sha256", 897, "1aff29f3a42b618ca85e5a1d3c537307e32326f8d5092b82d4253a5bf6e1c4ac"),
    Pin("R245_CERT", "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json", 20_683_081, "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"),
    Pin("R242_MANIFEST", "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_manifest.sha256", 897, "6da30fe3f9438ec73dc9c7d1aac770d8e9730aa9564ab0c535f1596cdc09ef2f"),
    Pin("R242_CERT", "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json", 13_734_655, "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e"),
)
PIN_BY_ROLE: Final = {pin.role: pin for pin in SOURCE_PINS}

# This is a byte pin only.  The verifier never opens the producer as source
# code, and never imports, executes, or parses it.  Update only if the reviewed
# producer source itself changes before sealing.
PRODUCER_RECORD: Final = {
    "filename": PRODUCER_NAME,
    "size": 85_372,
    "sha256": "04a54693c944a66d8371ce7fc9910f39f42adf98d0e1bca5fb68757ce3289628",
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


class Sources:
    def __init__(self) -> None:
        self.directory_descriptor = -1
        self.file_descriptors: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "Sources":
        info = os.stat(ROOT, follow_symlinks=False)
        need(stat.S_ISDIR(info.st_mode) and not ROOT.is_symlink(), "source root")
        self.directory_descriptor = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for pin in SOURCE_PINS:
            before = os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)
            need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == pin.size, "source identity:" + pin.role)
            file_descriptor = os.open(pin.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.directory_descriptor)
            opened = os.fstat(file_descriptor)
            need(identity(opened) == identity(before), "source race:" + pin.role)
            need(hash_fd(file_descriptor) == hash_fd(file_descriptor) == pin.sha256, "source digest:" + pin.role)
            self.file_descriptors[pin.role] = file_descriptor
            self.identities[pin.role] = identity(opened)
        return self

    def duplicate(self, role: str) -> int:
        duplicate = os.dup(self.file_descriptors[role])
        os.lseek(duplicate, 0, os.SEEK_SET)
        return duplicate

    def read(self, role: str) -> bytes:
        return read_fd(self.file_descriptors[role])

    def final(self) -> None:
        for pin in reversed(SOURCE_PINS):
            file_descriptor = self.file_descriptors[pin.role]
            need(identity(os.fstat(file_descriptor)) == self.identities[pin.role], "source final fd:" + pin.role)
            need(identity(os.stat(pin.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)) == self.identities[pin.role], "source final path:" + pin.role)
            need(hash_fd(file_descriptor) == pin.sha256, "source final digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for file_descriptor in self.file_descriptors.values():
            try:
                os.close(file_descriptor)
            except OSError:
                pass
        if self.directory_descriptor >= 0:
            os.close(self.directory_descriptor)


def source_jsonl(sources: Sources, role: str) -> Iterator[dict[str, Any]]:
    duplicate = sources.duplicate(role)
    try:
        with os.fdopen(duplicate, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            for ordinal, line in enumerate(stream):
                row = json.loads(line)
                need(type(row) is dict and line.endswith(b"\n") and line == canonical(row) + b"\n", "source canonical row:" + role + ":" + str(ordinal))
                body = dict(row)
                claimed = body.pop("row_sha256", None)
                need(type(claimed) is str and claimed == object_sha(body), "source row closure:" + role + ":" + str(ordinal))
                yield row
    finally:
        try:
            os.close(duplicate)
        except OSError:
            pass


def source_document(sources: Sources, role: str, closure: str | None = None) -> dict[str, Any]:
    raw = sources.read(role)
    value = json.loads(raw)
    need(type(value) is dict, "source document:" + role)
    if closure is not None:
        body = dict(value)
        claimed = body.pop(closure, None)
        need(type(claimed) is str and claimed == object_sha(body), "source document closure:" + role)
    return value


def legacy_result(sources: Sources, role: str) -> dict[str, Any]:
    document = source_document(sources, role)
    need(set(document) == {"schema", "result", "result_sha256"}, "legacy envelope:" + role)
    need(document["result_sha256"] == object_sha(document["result"]), "legacy result closure:" + role)
    return document["result"]


def row_ref(row: Mapping[str, Any], id_field: str = "row_id") -> dict[str, str]:
    need(type(row.get(id_field)) is str and type(row.get("row_sha256")) is str, "closed row reference")
    return {"row_id": row[id_field], "row_sha256": row["row_sha256"]}


def qtext(value: Any) -> str:
    if type(value) is str:
        return value
    if type(value) is int:
        return str(value)
    need(type(value) is dict and set(value) == {"numerator", "denominator"}, "rational wire")
    numerator, denominator = value["numerator"], value["denominator"]
    need(type(numerator) is int and type(denominator) is int and denominator > 0, "rational values")
    return str(numerator) if denominator == 1 else str(numerator) + "/" + str(denominator)


def recursive_contains(value: Any, target: Any) -> bool:
    if value == target:
        return True
    if type(value) is dict:
        return any(recursive_contains(item, target) for item in value.values())
    if type(value) is list:
        return any(recursive_contains(item, target) for item in value)
    return False


def verify_embedded_ref(value: Any, row: Mapping[str, Any], id_field: str = "row_id") -> None:
    need(recursive_contains(value, row[id_field]) and recursive_contains(value, row["row_sha256"]), "embedded closed reference:" + row[id_field])


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    need(raw.endswith(b"\n"), "source manifest newline:" + label)
    records: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        pieces = line.split("  ")
        need(len(pieces) == 2 and len(pieces[0]) == 64, "source manifest line:" + label)
        int(pieces[0], 16)
        name = Path(pieces[1]).name
        need(
            pieces[1] in {name, "deliverables/" + name}
            and name not in records,
            "source manifest name:" + label,
        )
        records[name] = pieces[0]
    return records


def bind_manifest(sources: Sources, manifest_role: str, member_roles: tuple[str, ...]) -> None:
    records = parse_manifest(sources.read(manifest_role), manifest_role)
    for role in member_roles:
        pin = PIN_BY_ROLE[role]
        need(records.get(pin.filename) == pin.sha256, "source manifest binding:" + manifest_role + ":" + role)


def exact_closed_document(sources: Sources, role: str, closure: str) -> dict[str, Any]:
    raw = sources.read(role)
    value = json.loads(raw)
    need(type(value) is dict and raw == canonical(value), "source exact document:" + role)
    body = dict(value)
    claimed = body.pop(closure, None)
    need(type(claimed) is str and claimed == object_sha(body), "source exact closure:" + role)
    return value


def qstr(value: Q | int | str) -> str:
    rational = Q(value)
    return str(rational.numerator) if rational.denominator == 1 else str(rational.numerator) + "/" + str(rational.denominator)


def qwire(value: Q | int | str) -> dict[str, int]:
    rational = Q(value)
    return {"numerator": rational.numerator, "denominator": rational.denominator}


def rational_from_wire(value: Any, label: str) -> Q:
    need(type(value) is dict and set(value) == {"numerator", "denominator"}, "rational wire:" + label)
    numerator, denominator = value["numerator"], value["denominator"]
    need(type(numerator) is int and type(denominator) is int and denominator > 0, "rational values:" + label)
    rational = Q(numerator, denominator)
    need((rational.numerator, rational.denominator) == (numerator, denominator), "reduced rational:" + label)
    return rational


@dataclass(frozen=True)
class Range:
    lower: Q
    upper: Q

    def __post_init__(self) -> None:
        need(type(self.lower) is Q and type(self.upper) is Q and self.lower <= self.upper, "range")

    @classmethod
    def point(cls, value: Q | int | str) -> "Range":
        rational = Q(value)
        return cls(rational, rational)

    def __add__(self, other: Any) -> "Range":
        right = other if type(other) is Range else Range.point(other)
        return Range(self.lower + right.lower, self.upper + right.upper)

    __radd__ = __add__

    def __neg__(self) -> "Range":
        return Range(-self.upper, -self.lower)

    def __sub__(self, other: Any) -> "Range":
        return self + (-other)

    def __rsub__(self, other: Any) -> "Range":
        return Range.point(other) + (-self)

    def __mul__(self, other: Any) -> "Range":
        right = other if type(other) is Range else Range.point(other)
        values = (
            self.lower * right.lower,
            self.lower * right.upper,
            self.upper * right.lower,
            self.upper * right.upper,
        )
        return Range(min(values), max(values))

    __rmul__ = __mul__

    def square(self) -> "Range":
        endpoints = (self.lower * self.lower, self.upper * self.upper)
        return Range(Q(0) if self.lower <= 0 <= self.upper else min(endpoints), max(endpoints))

    def divide(self, other: Any) -> "Range":
        right = other if type(other) is Range else Range.point(other)
        need(not right.lower <= 0 <= right.upper, "range division")
        reciprocal = Range(min(Q(1, right.lower), Q(1, right.upper)), max(Q(1, right.lower), Q(1, right.upper)))
        return self * reciprocal

    def sign(self) -> str:
        if self.lower > 0:
            return "STRICT_POSITIVE"
        if self.upper < 0:
            return "STRICT_NEGATIVE"
        return "OVERWRAP"

    def wire(self) -> dict[str, Any]:
        return {"lower": qwire(self.lower), "upper": qwire(self.upper)}


def positive_square_root(value: Range) -> Range:
    need(value.lower > 0, "sqrt domain")
    scale = 1 << SQRT_BITS

    def floor_root(rational: Q) -> Q:
        return Q(isqrt((rational.numerator * scale * scale) // rational.denominator), scale)

    lower = floor_root(value.lower)
    upper = floor_root(value.upper)
    if upper * upper < value.upper:
        upper += Q(1, scale)
    return Range(lower, upper)


@dataclass(frozen=True)
class Differential:
    value: Range
    derivative: Range

    @classmethod
    def constant(cls, value: Range | Q | int) -> "Differential":
        interval = value if type(value) is Range else Range.point(value)
        return cls(interval, Range.point(0))

    def __add__(self, other: Any) -> "Differential":
        right = other if type(other) is Differential else Differential.constant(other)
        return Differential(self.value + right.value, self.derivative + right.derivative)

    __radd__ = __add__

    def __neg__(self) -> "Differential":
        return Differential(-self.value, -self.derivative)

    def __sub__(self, other: Any) -> "Differential":
        return self + (-other)

    def __rsub__(self, other: Any) -> "Differential":
        return Differential.constant(other) + (-self)

    def __mul__(self, other: Any) -> "Differential":
        right = other if type(other) is Differential else Differential.constant(other)
        return Differential(self.value * right.value, self.derivative * right.value + self.value * right.derivative)

    __rmul__ = __mul__


def differential_square_root(value: Differential) -> Differential:
    root = positive_square_root(value.value)
    return Differential(root, value.derivative.divide(root * 2))


def owner_xy(owner: str) -> tuple[str, int, int]:
    match = OWNER_RE.fullmatch(owner)
    need(match is not None, "owner syntax")
    return match.group(1), int(match.group(2)), int(match.group(3))


def independent_geometry(
    chart: str,
    owner: str,
    t_bounds: tuple[Q, Q],
    p_bounds: tuple[Q, Q],
    variable: str | None,
) -> dict[str, Range | Differential]:
    owner_kind, owner_x, owner_y = owner_xy(owner)
    need(chart in {"G:E", "G:W", "G:N", "G:S"} and owner_kind == "G", "G chart geometry")
    t_range, p_range = Range(*t_bounds), Range(*p_bounds)
    if variable is None:
        t: Range | Differential = t_range
        p: Range | Differential = p_range
        one: Range | Differential = Range.point(1)
        normal_radicand: Range | Differential = one - t.square()
        phase_radicand: Range | Differential = one - p.square()
        normal_root = positive_square_root(normal_radicand)
        phase_root = positive_square_root(phase_radicand)
    else:
        need(variable in {"t", "p"}, "differential variable")
        t = Differential(t_range, Range.point(1 if variable == "t" else 0))
        p = Differential(p_range, Range.point(1 if variable == "p" else 0))
        one = Differential.constant(1)
        normal_radicand = one - t * t
        phase_radicand = one - p * p
        normal_root = differential_square_root(normal_radicand)
        phase_root = differential_square_root(phase_radicand)
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
        hit_radicand: Range | Differential = Range.point(radius * radius) - transverse.square()
        radical = positive_square_root(hit_radicand)
    else:
        hit_radicand = Differential.constant(radius * radius) - transverse * transverse
        radical = differential_square_root(hit_radicand)
    hit_x = owner_x - radical * tangent_x + transverse * tangent_y
    hit_y = owner_y - radical * tangent_y - transverse * tangent_x
    return {
        "hit_x": hit_x,
        "hit_y": hit_y,
        "normal_radicand": normal_radicand,
        "phase_radicand": phase_radicand,
        "hit_radicand": hit_radicand,
    }


def endpoint_spec(frontier: Mapping[str, Any]) -> tuple[str, int]:
    kind, axis, wall_text = frontier["reason_labels"][0].split(":")
    need(kind == "wall_endpoint_or_count_transition" and axis in {"X", "Y"}, "endpoint reason")
    return axis, int(wall_text)


def wall_factor(
    frontier: Mapping[str, Any],
    t_bounds: tuple[Q, Q],
    p_bounds: tuple[Q, Q],
    variable: str | None = None,
) -> Range | Differential:
    axis, wall = endpoint_spec(frontier)
    values = independent_geometry(frontier["chart"], frontier["owner_target"], t_bounds, p_bounds, variable)
    return values["hit_x" if axis == "X" else "hit_y"] - wall


def t_derivative_receipt(frontier: Mapping[str, Any], expected: str) -> dict[str, Any]:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    pending = [(t0, t1, p0, p1, 0)]
    cells = 0
    maximum_depth = 0
    while pending:
        ta, tb, pa, pb, depth = pending.pop()
        value = wall_factor(frontier, (ta, tb), (pa, pb), "t")
        need(type(value) is Differential, "t derivative type")
        if value.derivative.sign() == expected:
            cells += 1
            maximum_depth = max(maximum_depth, depth)
            continue
        need(depth < 8, "t derivative unresolved")
        if depth % 2 == 0:
            middle = (pa + pb) / 2
            pending.extend(((ta, tb, pa, middle, depth + 1), (ta, tb, middle, pb, depth + 1)))
        else:
            middle = (ta + tb) / 2
            pending.extend(((ta, middle, pa, pb, depth + 1), (middle, tb, pa, pb, depth + 1)))
    return {"strict_t_derivative_sign": expected, "proof_cell_count": cells, "maximum_split_depth": maximum_depth}


def face_p_derivative_receipt(frontier: Mapping[str, Any], face: str) -> dict[str, Any]:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    t_value = t0 if face == "LOWER_T_FACE" else t1
    pending = [(p0, p1, 0)]
    cells: list[dict[str, Any]] = []
    signs: set[str] = set()
    maximum_depth = 0
    while pending:
        pa, pb, depth = pending.pop()
        value = wall_factor(frontier, (t_value, t_value), (pa, pb), "p")
        need(type(value) is Differential, "face p derivative type")
        sign = value.derivative.sign()
        if sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}:
            cells.append({
                "p_interval": [qwire(pa), qwire(pb)],
                "derivative_interval_sha256": object_sha(value.derivative.wire()),
                "sign": sign,
            })
            signs.add(sign)
            maximum_depth = max(maximum_depth, depth)
            continue
        need(depth < 12, "face p derivative unresolved")
        middle = (pa + pb) / 2
        pending.extend(((pa, middle, depth + 1), (middle, pb, depth + 1)))
    need(len(signs) == 1, "face p derivative sign")
    ordered = sorted(cells, key=lambda row: Q(row["p_interval"][0]["numerator"], row["p_interval"][0]["denominator"]))
    return {
        "face": face,
        "t_value": qwire(t_value),
        "strict_p_derivative_sign": next(iter(signs)),
        "proof_cell_count": len(cells),
        "maximum_split_depth": maximum_depth,
        "ordered_cell_receipts_sha256": object_sha(ordered),
    }


def corner_receipt(frontier: Mapping[str, Any], face: str, p_side: str) -> dict[str, Any]:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    t_value = t0 if face == "LOWER_T_FACE" else t1
    p_value = p0 if p_side == "LOWER_P" else p1
    value = wall_factor(frontier, (t_value, t_value), (p_value, p_value))
    need(type(value) is Range and value.sign() in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, "strict target corner")
    return {
        "face": face,
        "p_side": p_side,
        "t_value": qwire(t_value),
        "p_value": qwire(p_value),
        "factor_sign": value.sign(),
        "factor_interval_sha256": object_sha(value.wire()),
    }


def root_descriptor(
    graph_id: str,
    frontier: Mapping[str, Any],
    face: str,
    derivative_sign: str,
) -> dict[str, Any] | None:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    t_value = t0 if face == "LOWER_T_FACE" else t1
    left, right = p0, p1
    left_value = wall_factor(frontier, (t_value, t_value), (left, left))
    right_value = wall_factor(frontier, (t_value, t_value), (right, right))
    need(type(left_value) is Range and type(right_value) is Range, "root endpoint type")
    left_sign, right_sign = left_value.sign(), right_value.sign()
    need(left_sign != "OVERWRAP" and right_sign != "OVERWRAP", "root endpoint sign")
    if left_sign == right_sign:
        return None
    need({left_sign, right_sign} == {"STRICT_NEGATIVE", "STRICT_POSITIVE"}, "root sign change")
    need(
        (derivative_sign == "STRICT_POSITIVE" and left_sign == "STRICT_NEGATIVE")
        or (derivative_sign == "STRICT_NEGATIVE" and left_sign == "STRICT_POSITIVE"),
        "root monotone orientation",
    )
    for _ in range(ROOT_ISOLATION_STEPS):
        middle = (left + right) / 2
        middle_value = wall_factor(frontier, (t_value, t_value), (middle, middle))
        need(type(middle_value) is Range and middle_value.sign() != "OVERWRAP", "root midpoint")
        if middle_value.sign() == left_sign:
            left, left_value = middle, middle_value
        else:
            right, right_value = middle, middle_value
    need(left < right and left_value.sign() != right_value.sign(), "isolated root")
    core = {
        "descriptor_id": PREFIX + ":implicit-cut-root:" + object_sha([graph_id, face]),
        "face": face,
        "t_value": qwire(t_value),
        "equation_role": "PRIMITIVE_TARGET_FACTOR_AST_EQUALS_ZERO",
        "strict_p_derivative_sign": derivative_sign,
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


def radical_receipts(frontier: Mapping[str, Any]) -> list[dict[str, Any]]:
    t0, t1, p0, p1 = map(Q, frontier["box"][:4])
    values = independent_geometry(frontier["chart"], frontier["owner_target"], (t0, t1), (p0, p1), None)
    receipts = []
    for name in ("normal_radicand", "phase_radicand", "hit_radicand"):
        value = values[name]
        need(type(value) is Range and value.lower > 0, "radical positivity:" + name)
        receipts.append({"radicand": name, "strictly_positive_on_carrier": True, "interval_sha256": object_sha(value.wire())})
    return receipts


def topology_certificate(
    graph_id: str,
    frontier: Mapping[str, Any],
    lower_proof: dict[str, Any],
    upper_proof: dict[str, Any],
) -> dict[str, Any]:
    need(lower_proof["strict_p_derivative_sign"] == upper_proof["strict_p_derivative_sign"], "same face derivative sign")
    sign = lower_proof["strict_p_derivative_sign"]
    corners = [
        corner_receipt(frontier, face, side)
        for face in ("LOWER_T_FACE", "UPPER_T_FACE")
        for side in ("LOWER_P", "UPPER_P")
    ]
    by_key = {(row["face"], row["p_side"]): row["factor_sign"] for row in corners}
    domain_lower = by_key[("LOWER_T_FACE", "LOWER_P")] != by_key[("UPPER_T_FACE", "LOWER_P")]
    domain_upper = by_key[("LOWER_T_FACE", "UPPER_P")] != by_key[("UPPER_T_FACE", "UPPER_P")]
    roots = [
        descriptor
        for face in ("LOWER_T_FACE", "UPPER_T_FACE")
        for descriptor in (root_descriptor(graph_id, frontier, face, sign),)
        if descriptor is not None
    ]
    roots.sort(key=lambda row: Q(row["isolation_interval"][0]["numerator"], row["isolation_interval"][0]["denominator"]))
    if len(roots) == 2:
        need(not domain_lower and not domain_upper, "internal band")
        left_upper = Q(roots[0]["isolation_interval"][1]["numerator"], roots[0]["isolation_interval"][1]["denominator"])
        right_lower = Q(roots[1]["isolation_interval"][0]["numerator"], roots[1]["isolation_interval"][0]["denominator"])
        need(left_upper < right_lower, "separated cut roots")
        topology, inherited = "INTERNAL_P_BAND", []
    elif len(roots) == 1 and domain_lower and not domain_upper:
        topology, inherited = "LOWER_P_ATTACHED", ["LOWER_P"]
    elif len(roots) == 1 and domain_upper and not domain_lower:
        topology, inherited = "UPPER_P_ATTACHED", ["UPPER_P"]
    elif len(roots) == 0 and domain_lower and domain_upper:
        topology, inherited = "FULL_P_INTERVAL", ["LOWER_P", "UPPER_P"]
    else:
        raise Rejected("unexpected target topology")
    return {
        "topology": topology,
        "connected_sign_straddle_p_interval": True,
        "strict_same_sign_face_p_derivative": sign,
        "lower_t_face_p_derivative_proof": lower_proof,
        "upper_t_face_p_derivative_proof": upper_proof,
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


def interval_ast(coordinate: str, lower: str, upper: str) -> dict[str, Any]:
    need(Q(lower) <= Q(upper), "AST interval")
    return {"op": "CLOSED_INTERVAL", "coordinate": coordinate, "lower": qstr(lower), "upper": qstr(upper)}


def conjunction(*arguments: dict[str, Any]) -> dict[str, Any]:
    return {"op": "AND", "args": list(arguments)}


def rational_node(value: Q | int | str) -> dict[str, Any]:
    return {"op": "RATIONAL_CONSTANT", "value": qstr(value)}


def coordinate_node(name: str) -> dict[str, Any]:
    need(name in {"t", "p", "s"}, "primitive coordinate")
    return {"op": "COORDINATE", "name": name}


def sum_node(*arguments: dict[str, Any]) -> dict[str, Any]:
    return {"op": "ADD", "args": list(arguments)}


def product_node(*arguments: dict[str, Any]) -> dict[str, Any]:
    return {"op": "MUL", "args": list(arguments)}


def negative_node(argument: dict[str, Any]) -> dict[str, Any]:
    return {"op": "NEG", "arg": argument}


def square_node(argument: dict[str, Any]) -> dict[str, Any]:
    return {"op": "SQUARE", "arg": argument}


def principal_root_node(radicand: dict[str, Any]) -> dict[str, Any]:
    return {"op": "SQRT_PRINCIPAL_NONNEGATIVE", "radicand": radicand}


def independent_source_frame(
    chart: str,
    t_node: dict[str, Any],
    p_node: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    one = rational_node(1)
    normal_radicand = sum_node(one, negative_node(square_node(t_node)))
    phase_radicand = sum_node(one, negative_node(square_node(p_node)))
    normal_root = principal_root_node(normal_radicand)
    phase_root = principal_root_node(phase_radicand)
    need(chart in {"G:E", "G:W", "G:N", "G:S"}, "primitive source chart")
    cell = chart[-1]
    if cell == "E":
        normal_x, normal_y = normal_root, t_node
    elif cell == "W":
        normal_x, normal_y = negative_node(normal_root), t_node
    elif cell == "N":
        normal_x, normal_y = t_node, normal_root
    else:
        normal_x, normal_y = t_node, negative_node(normal_root)
    tangent_x = sum_node(product_node(phase_root, normal_x), negative_node(product_node(p_node, normal_y)))
    tangent_y = sum_node(product_node(phase_root, normal_y), product_node(p_node, normal_x))
    return {
        "normal_x": normal_x,
        "normal_y": normal_y,
        "tangent_x": tangent_x,
        "tangent_y": tangent_y,
        "normal_radicand": normal_radicand,
        "phase_radicand": phase_radicand,
    }


def independent_target_factor(
    semantic: Mapping[str, Any],
    fixed_t: str | None = None,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    parameters = semantic["kernel_parameters"]
    need(parameters["source_radius"] == qwire(Q(9, 25)) and parameters["target_radius"] == qwire(Q(9, 25)), "target 9/25 radii")
    t_node = coordinate_node("t") if fixed_t is None else rational_node(fixed_t)
    p_node = coordinate_node("p")
    frame = independent_source_frame(parameters["source_chart"], t_node, p_node)
    owner_kind, owner_x, owner_y = owner_xy(parameters["target_owner"])
    need(owner_kind == "G", "target G obstacle")
    source_x = product_node(rational_node(Q(9, 25)), frame["normal_x"])
    source_y = product_node(rational_node(Q(9, 25)), frame["normal_y"])
    delta_x = sum_node(rational_node(owner_x), negative_node(source_x))
    delta_y = sum_node(rational_node(owner_y), negative_node(source_y))
    transverse = sum_node(
        product_node(negative_node(frame["tangent_y"]), delta_x),
        product_node(frame["tangent_x"], delta_y),
    )
    hit_radicand = sum_node(rational_node(Q(81, 625)), negative_node(square_node(transverse)))
    radical = principal_root_node(hit_radicand)
    hit_x = sum_node(
        rational_node(owner_x),
        negative_node(product_node(radical, frame["tangent_x"])),
        product_node(transverse, frame["tangent_y"]),
    )
    hit_y = sum_node(
        rational_node(owner_y),
        negative_node(product_node(radical, frame["tangent_y"])),
        negative_node(product_node(transverse, frame["tangent_x"])),
    )
    need(parameters["wall_axis"] in {"X", "Y"}, "target wall axis")
    hit = hit_x if parameters["wall_axis"] == "X" else hit_y
    factor = sum_node(hit, negative_node(rational_node(parameters["integer_wall"])))
    return factor, {
        "normal_radicand": frame["normal_radicand"],
        "phase_radicand": frame["phase_radicand"],
        "hit_radicand": hit_radicand,
    }


def independent_r242_factor(
    source_chart: str,
    target_lift: str,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    t_node, p_node, s_node = coordinate_node("t"), coordinate_node("p"), coordinate_node("s")
    frame = independent_source_frame(source_chart, t_node, p_node)
    owner_kind, owner_x, owner_y = owner_xy(target_lift)
    source_x = product_node(rational_node(Q(9, 25)), frame["normal_x"])
    source_y = product_node(rational_node(Q(9, 25)), frame["normal_y"])
    if owner_kind == "G":
        center_x, center_y = rational_node(owner_x), rational_node(owner_y)
        target_radius = Q(9, 25)
    else:
        need(owner_kind == "W", "R242 target obstacle kind")
        center_x = sum_node(rational_node(Q(2 * owner_x + 1, 2)), s_node)
        center_y = rational_node(Q(2 * owner_y + 1, 2))
        target_radius = Q(4, 25)
    delta_x = sum_node(center_x, negative_node(source_x))
    delta_y = sum_node(center_y, negative_node(source_y))
    transverse = sum_node(
        product_node(negative_node(frame["tangent_y"]), delta_x),
        product_node(frame["tangent_x"], delta_y),
    )
    target_radicand = sum_node(rational_node(target_radius * target_radius), negative_node(square_node(transverse)))
    radical = principal_root_node(target_radicand)
    inverse_radius = rational_node(1 / target_radius)
    outgoing_x = product_node(
        inverse_radius,
        sum_node(negative_node(product_node(radical, frame["tangent_x"])), product_node(transverse, frame["tangent_y"])),
    )
    outgoing_y = product_node(
        inverse_radius,
        sum_node(negative_node(product_node(radical, frame["tangent_y"])), negative_node(product_node(transverse, frame["tangent_x"]))),
    )
    factor = sum_node(square_node(outgoing_x), negative_node(square_node(outgoing_y)))
    return factor, {
        "normal_radicand": frame["normal_radicand"],
        "phase_radicand": frame["phase_radicand"],
        "target_hit_radicand": target_radicand,
    }


def zero_equation(factor: dict[str, Any]) -> dict[str, Any]:
    return {"op": "EQ", "left": factor, "right": rational_node(0)}


def target_base(semantic: Mapping[str, Any], box: list[str]) -> dict[str, Any]:
    lower_face = independent_target_factor(semantic, qstr(box[0]))[0]
    upper_face = independent_target_factor(semantic, qstr(box[1]))[0]
    zero = rational_node(0)
    cases = [
        {"case": "LOWER_NEGATIVE_UPPER_POSITIVE", "predicate": conjunction({"op": "LT", "left": lower_face, "right": zero}, {"op": "GT", "left": upper_face, "right": zero})},
        {"case": "LOWER_POSITIVE_UPPER_NEGATIVE", "predicate": conjunction({"op": "GT", "left": lower_face, "right": zero}, {"op": "LT", "left": upper_face, "right": zero})},
        {"case": "LOWER_ZERO", "predicate": {"op": "EQ", "left": lower_face, "right": zero}},
        {"case": "UPPER_ZERO", "predicate": {"op": "EQ", "left": upper_face, "right": zero}},
    ]
    return conjunction(
        interval_ast("p", box[2], box[3]),
        interval_ast("s", box[4], box[5]),
        {"op": "OR_DISJOINT", "cases": cases},
    )


def closed_box_from_wire(domain: Mapping[str, Any], label: str) -> tuple[dict[str, Any], dict[str, Any]]:
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
            "closed box axis:" + label,
        )
        name = axis["axis"]
        need(name not in axes, "unique box axis:" + label)
        lower = rational_from_wire(axis["lower"], label + ":" + name + ":lower")
        upper = rational_from_wire(axis["upper"], label + ":" + name + ":upper")
        need(lower <= upper, "ordered box axis:" + label)
        axes[name] = (lower, upper)
    need(set(axes) == {"t", "p", "s"}, "complete box axes:" + label)
    carrier = conjunction(*(interval_ast(name, *axes[name]) for name in ("t", "p", "s")))
    base = conjunction(*(interval_ast(name, *axes[name]) for name in ("p", "s")))
    return carrier, base


def closed_row(core: dict[str, Any]) -> dict[str, Any]:
    return {**core, "row_sha256": object_sha(core)}


def sequence_sha(values: Iterator[Any] | list[Any]) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(canonical(value))
        digest.update(b"\n")
    return digest.hexdigest()


def deterministic_gzip(rows: list[dict[str, Any]]) -> tuple[bytes, bytes]:
    plain = b"".join(canonical(row) + b"\n" for row in rows)
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=buffer, mtime=0) as stream:
        stream.write(plain)
    return buffer.getvalue(), plain


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
        "ordered_rows_sha256": sequence_sha(iter(rows)),
    }


def collect_current_identity_rows(
    sources: Sources,
    member_ids: set[str],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    members: dict[str, dict[str, Any]] = {}
    family_count = 0
    for row in source_jsonl(sources, "C7_MEMBER"):
        if row["coarse_family"] == "G2A":
            family_count += 1
            need(row["member_id"] in member_ids, "unexpected current G2A member")
        if row["member_id"] in member_ids:
            member_id = row["member_id"]
            need(member_id not in members and row["coarse_family"] == "G2A", "current member bijection")
            need(row["support_semantic_state"] == "FRESH_MECHANICAL_IDENTITY_ONLY__FULL_SUPPORT_NOT_PROVED", "C7 support boundary")
            need(row["typed_support_ast"]["full_support_materialized"] is False, "C7 unmaterialized support")
            members[member_id] = row
    need(family_count == len(members) == 5_264 and set(members) == member_ids, "C7 G2A member exhaustion")

    representations: dict[str, dict[str, Any]] = {}
    family_count = 0
    for row in source_jsonl(sources, "C7_REPRESENTATION"):
        if row["coarse_family"] == "G2A":
            family_count += 1
            need(row["owner_member_id"] in member_ids, "unexpected current G2A representation")
        if row["owner_member_id"] in member_ids:
            member_id = row["owner_member_id"]
            need(member_id not in representations and row["coarse_family"] == "G2A", "current representation bijection")
            need(row["representation_role"] == "G2A_GRAPH_SHEET_IDENTITY", "current representation role")
            need(row["pullback_semantic_state"] == "PULLBACK_EQUIVALENCE_NOT_PROVED", "C7 pullback boundary")
            representations[member_id] = row
    need(family_count == len(representations) == 5_264 and set(representations) == member_ids, "C7 representation exhaustion")

    components: dict[str, dict[str, Any]] = {}
    for row in source_jsonl(sources, "C6_MEMBER_COMPONENT"):
        member_id = row["registry_member_id"]
        if member_id in member_ids:
            need(member_id not in components and row["member_identity_preserved"] is True, "C6 current member component")
            components[member_id] = row
    need(len(components) == 5_264 and set(components) == member_ids, "C6 component exhaustion")
    return members, representations, components


def validate_c9_boundary(result: Mapping[str, Any]) -> None:
    census = result["audit_census"]
    need(census["positive_graph_domain_audit_rows"] == 5_264, "C9 graph census")
    need(census["mechanical_relation_statement_rows"] == 15_392, "C9 relation denominator")
    need(census["positive_graph_physical_relation_candidates"] == 15_382, "C9 positive relation denominator")
    need(census["empty_graph_no_incidence_dispositions"] == 10, "C9 empty relation denominator")
    need(all(value == 0 for value in result["formal_credit"].values()), "C9 no semantic credit")


def independently_reconstruct() -> tuple[dict[str, Any], bytes, bytes]:
    with Sources() as sources:
        bind_manifest(sources, "C9_MANIFEST", ("C9_RESULT", "C9_GRAPH"))
        bind_manifest(sources, "C7_MANIFEST", ("C7_MEMBER", "C7_REPRESENTATION"))
        bind_manifest(sources, "C6_MANIFEST", ("C6_MEMBER_COMPONENT",))
        bind_manifest(sources, "C5_MANIFEST", ("C5_SEMANTIC",))
        bind_manifest(sources, "C4_MANIFEST", ("C4_LEDGER",))
        bind_manifest(sources, "R234_MANIFEST", ("R234_CERT",))
        bind_manifest(sources, "R248_MANIFEST", ("R248_CERT",))
        bind_manifest(sources, "R245_MANIFEST", ("R245_CERT",))
        bind_manifest(sources, "R242_MANIFEST", ("R242_CERT",))

        c9_result = exact_closed_document(sources, "C9_RESULT", "result_sha256")
        validate_c9_boundary(c9_result)
        c9_rows = list(source_jsonl(sources, "C9_GRAPH"))
        need(len(c9_rows) == 5_264, "C9 exact graph row count")
        c9_rows.sort(key=lambda row: row["graph_inventory_ordinal"])
        need(len({row["graph_inventory_ordinal"] for row in c9_rows}) == 5_264, "C9 graph ordinal uniqueness")

        c5_rows: dict[str, dict[str, Any]] = {}
        positive_count = 0
        for row in source_jsonl(sources, "C5_SEMANTIC"):
            if row["semantic_classification"]["classification"] == "POSITIVE_GRAPH":
                positive_count += 1
                semantic_id = row["semantic_row_id"]
                need(semantic_id not in c5_rows, "C5 positive semantic uniqueness")
                c5_rows[semantic_id] = row
        need(positive_count == len(c5_rows) == 5_264, "C5 positive graph exhaustion")

        c4_rows = list(source_jsonl(sources, "C4_LEDGER"))
        need(len(c4_rows) == 16, "C4 bridge census")
        c4_rows.sort(key=lambda row: row["bridge_ordinal"])
        need([row["bridge_ordinal"] for row in c4_rows] == list(range(16)), "C4 bridge ordinal closure")
        c4_by_id = {row["bridge_row_id"]: row for row in c4_rows}
        need(len(c4_by_id) == 16, "C4 bridge uniqueness")

        r234_result = legacy_result(sources, "R234_CERT")
        r234_rows = r234_result["depth6_frontier_rows"]
        need(len(r234_rows) == 38_376, "R234 frontier census")
        r248_result = legacy_result(sources, "R248_CERT")
        r248_rows = r248_result["formal_wall_half_open_sheet_owner_ledger"]["rows"]
        need(len(r248_rows) == 38_360, "R248 sheet census")
        r248_by_member = {row["wall_sheet_node_id"]: row for row in r248_rows}
        need(len(r248_by_member) == len(r248_rows), "R248 sheet uniqueness")
        r245_result = legacy_result(sources, "R245_CERT")
        r245_by_member = {
            row["retained_stratum_node_id"]: row
            for row in r245_result["formal_retained_stratum_node_ledger"]["rows"]
            if row["stratum_kind"] == "HALF_OPEN_TRANSITION_SHEET"
        }
        need(len(r245_by_member) == 264, "R245 transition sheet census")
        r242_result = legacy_result(sources, "R242_CERT")
        r242_rows = r242_result["formal_positive_2D_transition_sheet_patch_ledger"]["rows"]
        need(len(r242_rows) == 264, "R242 transition patch census")
        r242_by_id: dict[str, dict[str, Any]] = {}
        for row in r242_rows:
            row_id = row["transition_sheet_patch_row_id"]
            need(row_id not in r242_by_id, "R242 row uniqueness")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == object_sha(body), "R242 row closure")
            need(row["official_key_ordinal"] >= 0, "R242 official key ordinal")
            r242_by_id[row_id] = row

        graph_ids = [row["graph_id"] for row in c9_rows]
        member_ids = [row["sheet_member_id"] for row in c9_rows]
        semantic_ids = [row["C5_semantic_row_id"] for row in c9_rows]
        need(len(set(graph_ids)) == len(set(member_ids)) == len(set(semantic_ids)) == 5_264, "C9 graph/member/semantic bijection")
        c7_members, c7_representations, c6_components = collect_current_identity_rows(sources, set(member_ids))

        support_rows: list[dict[str, Any]] = []
        support_by_graph: dict[str, dict[str, Any]] = {}
        class_counts: Counter[str] = Counter()
        topology_counts: Counter[str] = Counter()
        face_sign_counts: Counter[str] = Counter()
        t_sign_counts: Counter[str] = Counter()
        root_count = 0
        inherited_boundary_count = 0

        for c9_row in c9_rows:
            graph_id = c9_row["graph_id"]
            graph_class = c9_row["graph_class"]
            member_id = c9_row["sheet_member_id"]
            c5_row = c5_rows.get(c9_row["C5_semantic_row_id"])
            need(c5_row is not None and c5_row["row_sha256"] == c9_row["C5_semantic_row_sha256"], "C9-C5 exact binding")
            need(c5_row["graph_id"] == graph_id, "C5 graph identity")
            semantic = c5_row["semantic_classification"]
            class_counts[graph_class] += 1
            legacy_refs: dict[str, Any]
            side_conditions: list[dict[str, Any]] = []

            if graph_class == "R235_TARGET_POSITIVE_PARTIAL_BASE":
                need(semantic["kernel"] == "G_TARGET_FIRST_HIT_COORDINATE_MINUS_INTEGER_WALL_V1", "target semantic kernel")
                box = semantic["complete_parameter_domain"]["box"]
                frontier_ref = c5_row["canonical_input_commitment"]["R234_frontier_row"]
                need(type(frontier_ref) is list and len(frontier_ref) == 3, "target R234 reference")
                frontier = r234_rows[frontier_ref[0]]
                need(frontier["frontier_row_id"] == frontier_ref[1] and object_sha(frontier) == frontier_ref[2], "target R234 closed binding")
                need(frontier["box"] == box, "target exact carrier")
                expected_sign = c9_row["exact_graph_domain_receipt"]["strict_t_derivative_proof"]["strict_t_derivative_sign"]
                t_proof = t_derivative_receipt(frontier, expected_sign)
                need(t_proof == c9_row["exact_graph_domain_receipt"]["strict_t_derivative_proof"], "independent C9 t derivative replay")
                lower_proof = face_p_derivative_receipt(frontier, "LOWER_T_FACE")
                upper_proof = face_p_derivative_receipt(frontier, "UPPER_T_FACE")
                topology = topology_certificate(graph_id, frontier, lower_proof, upper_proof)
                topology_counts[topology["topology"]] += 1
                face_sign_counts[topology["strict_same_sign_face_p_derivative"]] += 1
                t_sign_counts[expected_sign] += 1
                root_count += topology["implicit_cut_root_count"]
                inherited_boundary_count += topology["inherited_carrier_p_boundary_count"]
                factor, symbolic_radicands = independent_target_factor(semantic)
                equation = zero_equation(factor)
                carrier = conjunction(
                    interval_ast("t", box[0], box[1]),
                    interval_ast("p", box[2], box[3]),
                    interval_ast("s", box[4], box[5]),
                )
                base = target_base(semantic, box)
                support = conjunction(carrier, base, equation)
                numeric_receipts = radical_receipts(frontier)
                need({row["radicand"] for row in numeric_receipts} == set(symbolic_radicands), "target symbolic radicand names")
                side_conditions = [
                    {
                        **receipt,
                        "primitive_radicand_ast_sha256": object_sha(symbolic_radicands[receipt["radicand"]]),
                        "principal_nonnegative_square_root_semantics": True,
                    }
                    for receipt in numeric_receipts
                ]
                monotone = {
                    "kind": "STRICT_T_MONOTONE_IMPLICIT_GRAPH_OVER_CONNECTED_SIGN_STRADDLE_BASE",
                    "strict_t_derivative_proof": t_proof,
                    "unique_t_for_every_exact_base_point": True,
                    "face_p_topology_certificate": topology,
                }
                legacy_refs = {
                    "R234_frontier": {"ordinal": frontier_ref[0], "row_id": frontier_ref[1], "row_sha256": frontier_ref[2]},
                    "R248_outer_envelope": c9_row["legacy_sheet_geometry_scope"],
                }
                need(legacy_refs["R248_outer_envelope"]["disposition"] == "OUTER_ENVELOPE_ONLY__NOT_FULL_GRAPH_SUPPORT", "target envelope nonpromotion")
                properties = {
                    "nonempty": True,
                    "connected": True,
                    "one_graph_point_per_exact_base_point": True,
                    "s_independent_equation": True,
                    "R248_rectangle_used_as_support": False,
                }
            elif graph_class == "R235_SOURCE_EXACT_FACE_FULL_BASE":
                need(semantic["kernel"] == "EXACT_SOURCE_COORDINATE_MINUS_ZERO_EQUALS_9_OVER_25_TIMES_T", "R235 source kernel")
                box = semantic["complete_parameter_domain"]["box"]
                carrier = conjunction(
                    interval_ast("t", box[0], box[1]),
                    interval_ast("p", box[2], box[3]),
                    interval_ast("s", box[4], box[5]),
                )
                base = conjunction(interval_ast("p", box[2], box[3]), interval_ast("s", box[4], box[5]))
                equation = zero_equation(product_node(rational_node(Q(9, 25)), coordinate_node("t")))
                support = conjunction(carrier, base, equation)
                need(semantic["strict_t_derivative_exact"] == qwire(Q(9, 25)), "R235 exact derivative")
                monotone = {
                    "kind": "EXPLICIT_T_EQUALS_ZERO_FULL_BASE_GRAPH",
                    "strict_t_derivative_exact": semantic["strict_t_derivative_exact"],
                    "unique_t_for_every_exact_base_point": True,
                }
                legacy_refs = {"R248_identity_and_exact_base_lineage": c9_row["legacy_sheet_geometry_scope"]}
                properties = {
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
                    "C4 bridge exact binding",
                )
                source_graph_ref = bridge["canonical_input_commitment"]["B1G0_source_graph_row"]
                need(
                    source_graph_ref[0] == c9_row["graph_inventory_ordinal"]
                    and source_graph_ref[1] == c9_row["graph_inventory_row_id"],
                    "C4 source graph binding",
                )
                reconstruction = bridge["semantic_reconstruction"]
                expected_c4_factor = {
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
                expected_c4_derivative = {
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
                    and reconstruction["source_factor_ast"] == expected_c4_factor
                    and reconstruction["source_t_derivative_ast"] == expected_c4_derivative
                    and reconstruction["source_zero_set"] == "EXACT_FACE_GRAPH_t_EQUALS_0"
                    and reconstruction["source_zero_face"] in {"LOWER", "UPPER"}
                    and reconstruction["source_graph_dimension"] == 2
                    and reconstruction["complete_domain_partition_verified"] is True
                    and reconstruction["complete_domain_partition_cell_count"] == 4,
                    "C4 source semantic closure",
                )
                derivative = reconstruction["source_t_derivative_exact_interval"]
                need(
                    rational_from_wire(derivative["lower"], "C4 derivative lower") == Q(9, 25)
                    and rational_from_wire(derivative["upper"], "C4 derivative upper") == Q(9, 25),
                    "C4 exact derivative",
                )
                complete_domain = reconstruction["complete_parameter_domain"]
                carrier, base = closed_box_from_wire(complete_domain, "C4 complete parameter domain")
                rectangle = c9_row["legacy_sheet_geometry_scope"]["rectangle"]
                need(type(rectangle) is list and len(rectangle) == 4, "R235D exact rectangle")
                axes = {axis["axis"]: axis for axis in complete_domain["axes"]}
                need(
                    rectangle == [
                        qstr(rational_from_wire(axes["p"]["lower"], "C4 p lower")),
                        qstr(rational_from_wire(axes["p"]["upper"], "C4 p upper")),
                        qstr(rational_from_wire(axes["s"]["lower"], "C4 s lower")),
                        qstr(rational_from_wire(axes["s"]["upper"], "C4 s upper")),
                    ],
                    "C4-R248 base coordinate binding",
                )
                equation = zero_equation(product_node(rational_node(Q(9, 25)), coordinate_node("t")))
                support = conjunction(carrier, base, equation)
                need(
                    c9_row["exact_graph_domain_receipt"]["C4_bridge_row_sha256"] == bridge["row_sha256"]
                    and c9_row["exact_graph_domain_receipt"]["complete_parameter_domain_sha256"] == object_sha(complete_domain),
                    "C9-C4 exact domain receipt",
                )
                bridge_ref = {
                    "ordinal": bridge["bridge_ordinal"],
                    "row_id": bridge["bridge_row_id"],
                    "row_sha256": bridge["row_sha256"],
                    "full_row_sha256": object_sha(bridge),
                }
                monotone = {
                    "kind": "SEALED_EXPLICIT_T_EQUALS_ZERO_FULL_BASE_GRAPH",
                    "C4_bridge_ref": bridge_ref,
                    "strict_t_derivative_exact": qwire(Q(9, 25)),
                    "C9_exact_domain_receipt": c9_row["exact_graph_domain_receipt"],
                    "unique_t_for_every_exact_base_point": True,
                }
                legacy_refs = {
                    "C4_exact_source_semantic_authority": bridge_ref,
                    "R248_identity_and_base_coordinate_lineage": c9_row["legacy_sheet_geometry_scope"],
                }
                properties = {
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
                    "R242 patch exact binding",
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
                retained_source = r245_by_member.get(member_id)
                need(retained_source is not None, "R242 retained identity source")
                local_signature = retained_source["local_return_signature"]
                need(
                    local_signature["source_chart"] == r242_row["source_chart"]
                    and local_signature["target_lift"] == r242_row["target_lift"]
                    and retained_source["Round220_split_interface_id"] == r242_row["Round220_split_interface_id"]
                    and retained_source["Round179_retained_child_row_id"] == r242_row["Round179_retained_child_row_id"],
                    "R242-R245 chart/lift lineage",
                )
                carrier = conjunction(
                    interval_ast("t", box[0], box[1]),
                    interval_ast("p", box[2], box[3]),
                    interval_ast("s", box[4], box[5]),
                )
                base = conjunction(interval_ast("p", box[2], box[3]), interval_ast("s", box[4], box[5]))
                factor, symbolic_radicands = independent_r242_factor(r242_row["source_chart"], r242_row["target_lift"])
                equation = zero_equation(factor)
                support = conjunction(carrier, base, equation)
                r242_bound_ref = {
                    "ordinal": r242_ref[0],
                    "row_id": r242_row["transition_sheet_patch_row_id"],
                    "row_sha256": r242_row["row_sha256"],
                    "full_row_sha256": object_sha(r242_row),
                }
                side_conditions = []
                for radicand_name, radicand_node in symbolic_radicands.items():
                    side_conditions.append({
                        "radicand": radicand_name,
                        "strictly_positive_on_carrier": True,
                        "primitive_radicand_ast_sha256": object_sha(radicand_node),
                        "sealed_R242_patch_ref": r242_bound_ref,
                        "principal_nonnegative_square_root_semantics": True,
                    })
                monotone = {
                    "kind": "SEALED_R242_STRICT_T_MONOTONE_UNIQUE_FULL_PATCH_GRAPH",
                    "strict_t_derivative_sign": semantic["strict_t_derivative_sign"],
                    "lower_t_face_F_sign": semantic["lower_t_face_F_sign"],
                    "upper_t_face_F_sign": semantic["upper_t_face_F_sign"],
                    "unique_t_for_every_exact_base_point": True,
                }
                legacy_refs = {
                    "R242_exact_patch_authority": r242_bound_ref,
                    "R245_retained_stratum_identity_lineage": {
                        "member_id": member_id,
                        "row_sha256": retained_source["row_sha256"],
                    },
                }
                properties = {
                    "nonempty": True,
                    "connected": True,
                    "one_graph_point_per_exact_base_point": True,
                    "s_independent_equation": False,
                    "R248_rectangle_used_as_support": False,
                }
            else:
                raise Rejected("unknown graph class:" + graph_class)

            for ast_name, ast_value in (
                ("carrier", carrier),
                ("base", base),
                ("equation", equation),
                ("support", support),
            ):
                validate_primitive_ast(ast_value, graph_id + ":" + ast_name)
            ast_hashes = {
                "carrier_domain_ast_sha256": object_sha(carrier),
                "base_domain_ast_sha256": object_sha(base),
                "equation_ast_sha256": object_sha(equation),
                "exact_support_ast_sha256": object_sha(support),
            }
            core = {
                "schema": SUPPORT_ROW_SCHEMA,
                "row_id": PREFIX + ":exact-graph-support:" + object_sha([graph_id, member_id]),
                "graph_ordinal": c9_row["graph_inventory_ordinal"],
                "graph_id": graph_id,
                "graph_class": graph_class,
                "sheet_member_id": member_id,
                "C9_graph_ref": row_ref(c9_row),
                "C5_semantic_ref": {"row_id": c5_row["semantic_row_id"], "row_sha256": c5_row["row_sha256"]},
                "legacy_source_refs": legacy_refs,
                "coordinate_parameter": "TPS",
                "carrier_domain_ast": carrier,
                "base_domain_ast": base,
                "equation_ast": equation,
                "exact_support_ast": support,
                "ast_sha256": ast_hashes,
                "radical_side_condition_receipts": side_conditions,
                "monotone_graph_certificate": monotone,
                "source_lineage_certificate": {
                    "C9_graph_row_bound": True,
                    "C5_positive_graph_row_bound": True,
                    "fresh_member_universe": "ROUND306C6",
                    "legacy_geometry_role": "CONSTRUCTION_OR_IDENTITY_LINEAGE_ONLY",
                },
                "support_properties": properties,
                "scoped_credit": {"exact_G2_feature_support_AST": 1, "member_natural_key_preservation": 0},
                "downstream_nonpromotion": DOWNSTREAM_ZERO,
            }
            support_row = closed_row(core)
            need(graph_id not in support_by_graph, "support graph uniqueness")
            support_rows.append(support_row)
            support_by_graph[graph_id] = support_row

        need(len(support_rows) == len(support_by_graph) == 5_264, "support exhaustion")
        need(dict(class_counts) == CLASS_COUNTS, "support class census")
        need(dict(topology_counts) == {key: value for key, value in TARGET_TOPOLOGY_COUNTS.items() if value}, "target topology census")
        need(face_sign_counts == {"STRICT_POSITIVE": 2_216, "STRICT_NEGATIVE": 2_216}, "target face derivative census")
        need(t_sign_counts == {"STRICT_POSITIVE": 3_932, "STRICT_NEGATIVE": 500}, "target t derivative census")
        need(root_count == 8_392 and inherited_boundary_count == 472, "target boundary census")

        identity_rows: list[dict[str, Any]] = []
        natural_key_hashes: set[str] = set()
        identity_source_counts: Counter[str] = Counter()
        for support_row in support_rows:
            graph_id = support_row["graph_id"]
            member_id = support_row["sheet_member_id"]
            graph_class = support_row["graph_class"]
            if graph_class == "R242_UNIQUE_GRAPH_FULL_PATCH":
                source = r245_by_member.get(member_id)
                need(source is not None, "R245 natural-key source")
                source_body = dict(source)
                claimed = source_body.pop("row_sha256", None)
                need(type(claimed) is str and claimed == object_sha(source_body), "R245 row closure")
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
                identity_source_counts["R245"] += 1
            else:
                source = r248_by_member.get(member_id)
                need(source is not None, "R248 natural-key source")
                source_body = dict(source)
                claimed = source_body.pop("row_sha256", None)
                need(type(claimed) is str and claimed == object_sha(source_body), "R248 row closure")
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
                identity_source_counts["R248"] += 1
            natural_key_sha = object_sha(natural_key)
            need(natural_key_sha not in natural_key_hashes, "natural-key uniqueness")
            natural_key_hashes.add(natural_key_sha)
            need(recomputed == member_id, "natural-key member identity")
            c7_member = c7_members[member_id]
            c7_representation = c7_representations[member_id]
            c6_component = c6_components[member_id]
            need(c7_member["C6_member_component_row_id"] == c6_component["row_id"], "C7-C6 component binding")
            need(c7_representation["owner_member_row_id"] == c7_member["row_id"], "C7 representation owner binding")
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

        need(len(identity_rows) == len(natural_key_hashes) == 5_264, "identity exhaustion")
        need(identity_source_counts == {"R248": 5_000, "R245": 264}, "identity source census")

        support_wire, support_plain = deterministic_gzip(support_rows)
        identity_wire, identity_plain = deterministic_gzip(identity_rows)
        support_descriptor = ledger_descriptor(SUPPORT_NAME, SUPPORT_ROW_SCHEMA, support_rows, support_wire, support_plain)
        identity_descriptor = ledger_descriptor(IDENTITY_NAME, IDENTITY_ROW_SCHEMA, identity_rows, identity_wire, identity_plain)
        body = {
            "schema": SCHEMA,
            "status": STATUS,
            "producer_source": PRODUCER_RECORD,
            "source_pins": [pin.__dict__ for pin in SOURCE_PINS],
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
                "graph_class_census": CLASS_COUNTS,
                "R235_target_topology_census": TARGET_TOPOLOGY_COUNTS,
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
            "scoped_credit": {"exact_G2_feature_support_AST": 5_264, "member_natural_key_preservation": 5_264},
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
        sources.final()
    return result, support_wire, identity_wire


PRIMITIVE_AST_OPS: Final = {
    "ADD",
    "AND",
    "CLOSED_INTERVAL",
    "COORDINATE",
    "EQ",
    "GT",
    "LT",
    "MUL",
    "NEG",
    "OR_DISJOINT",
    "RATIONAL_CONSTANT",
    "SQUARE",
    "SQRT_PRINCIPAL_NONNEGATIVE",
}


def validate_primitive_ast(value: Any, label: str) -> None:
    """Fail closed on opaque mathematical macros and expression strings."""
    need(type(value) is dict and type(value.get("op")) is str, "AST node:" + label)
    operation = value["op"]
    need(operation in PRIMITIVE_AST_OPS, "AST primitive allowlist:" + label + ":" + operation)
    need("expression" not in value and "kernel_parameters" not in value and "variables" not in value, "AST no opaque payload:" + label)
    if operation == "RATIONAL_CONSTANT":
        need(set(value) == {"op", "value"} and qstr(value["value"]) == value["value"], "AST rational:" + label)
    elif operation == "COORDINATE":
        need(set(value) == {"op", "name"} and value["name"] in {"t", "p", "s"}, "AST coordinate:" + label)
    elif operation in {"NEG", "SQUARE"}:
        need(set(value) == {"op", "arg"}, "AST unary shape:" + label)
        validate_primitive_ast(value["arg"], label + ".arg")
    elif operation == "SQRT_PRINCIPAL_NONNEGATIVE":
        need(set(value) == {"op", "radicand"}, "AST square-root shape:" + label)
        validate_primitive_ast(value["radicand"], label + ".radicand")
    elif operation in {"ADD", "MUL", "AND"}:
        need(set(value) == {"op", "args"} and type(value["args"]) is list and len(value["args"]) >= 1, "AST variadic shape:" + label)
        for ordinal, argument in enumerate(value["args"]):
            validate_primitive_ast(argument, label + ".args[" + str(ordinal) + "]")
    elif operation in {"EQ", "LT", "GT"}:
        need(set(value) == {"op", "left", "right"}, "AST comparison shape:" + label)
        validate_primitive_ast(value["left"], label + ".left")
        validate_primitive_ast(value["right"], label + ".right")
    elif operation == "CLOSED_INTERVAL":
        need(set(value) == {"op", "coordinate", "lower", "upper"}, "AST interval shape:" + label)
        need(value["coordinate"] in {"t", "p", "s"}, "AST interval coordinate:" + label)
        need(qstr(value["lower"]) == value["lower"] and qstr(value["upper"]) == value["upper"] and Q(value["lower"]) <= Q(value["upper"]), "AST interval bounds:" + label)
    else:
        need(operation == "OR_DISJOINT" and set(value) == {"op", "cases"}, "AST disjunction shape:" + label)
        cases = value["cases"]
        need(type(cases) is list and len(cases) >= 1, "AST disjunction cases:" + label)
        allowed = {"LOWER_NEGATIVE_UPPER_POSITIVE", "LOWER_POSITIVE_UPPER_NEGATIVE", "LOWER_ZERO", "UPPER_ZERO"}
        names: set[str] = set()
        for ordinal, case in enumerate(cases):
            need(type(case) is dict and set(case) == {"case", "predicate"} and case["case"] in allowed, "AST disjunction case:" + label)
            need(case["case"] not in names, "AST disjunction unique case:" + label)
            names.add(case["case"])
            validate_primitive_ast(case["predicate"], label + ".cases[" + str(ordinal) + "]")


def parse_candidate_ledger(
    wire: bytes,
    descriptor: Mapping[str, Any],
    expected_schema: str,
) -> list[dict[str, Any]]:
    need(type(descriptor) is dict, "candidate ledger descriptor")
    need(len(wire) == descriptor["compressed_size"] and hashlib.sha256(wire).hexdigest() == descriptor["compressed_sha256"], "candidate compressed ledger binding")
    with gzip.GzipFile(fileobj=io.BytesIO(wire), mode="rb") as stream:
        plain = stream.read()
    need(len(plain) == descriptor["uncompressed_size"] and hashlib.sha256(plain).hexdigest() == descriptor["uncompressed_sha256"], "candidate uncompressed ledger binding")
    rows: list[dict[str, Any]] = []
    for ordinal, line in enumerate(plain.splitlines(keepends=True)):
        need(line.endswith(b"\n"), "candidate ledger newline")
        row = json.loads(line)
        need(type(row) is dict and line == canonical(row) + b"\n", "candidate canonical ledger row:" + str(ordinal))
        need(row.get("schema") == expected_schema, "candidate row schema:" + str(ordinal))
        body = dict(row)
        claimed = body.pop("row_sha256", None)
        need(type(claimed) is str and claimed == object_sha(body), "candidate row closure:" + str(ordinal))
        rows.append(row)
    need(len(rows) == descriptor["row_count"], "candidate ledger row count")
    need(sequence_sha(row["row_id"] for row in rows) == descriptor["ordered_row_ids_sha256"], "candidate row-id order commitment")
    need(sequence_sha(row["row_sha256"] for row in rows) == descriptor["ordered_row_hashes_sha256"], "candidate row-hash order commitment")
    need(sequence_sha(iter(rows)) == descriptor["ordered_rows_sha256"], "candidate row order commitment")
    return rows


def closed_candidate_result(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict and raw == canonical(value), "candidate canonical result")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == object_sha(body), "candidate result closure")
    need(value.get("schema") == SCHEMA and value.get("status") == STATUS, "candidate result contract")
    need(value.get("producer_source") == PRODUCER_RECORD, "candidate producer byte pin")
    need(value.get("source_pins") == [pin.__dict__ for pin in SOURCE_PINS], "candidate source pin closure")
    need(value.get("scoped_credit") == {"exact_G2_feature_support_AST": 5_264, "member_natural_key_preservation": 5_264}, "candidate exact scoped credit")
    need(value.get("formal_credit") == DOWNSTREAM_ZERO, "candidate downstream zero credit")
    need(value.get("strict_nonpromotion") == {
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
    }, "candidate strict nonpromotion")
    need(value.get("C9_denominator_preserved") == {
        "mechanical_relation_statements": 15_392,
        "positive_graph_relation_candidates": 15_382,
        "empty_graph_no_incidence_dispositions": 10,
        "remaining_physical_incidence_theorem_rows": 15_382,
        "remaining_representation_pullback_theorem_rows": 15_382,
        "remaining_one_sided_trace_rows": 10_118,
    }, "candidate C9 denominator")
    return value


def validate_candidate_payloads(result_raw: bytes, support_wire: bytes, identity_wire: bytes) -> dict[str, Any]:
    result = closed_candidate_result(result_raw)
    support_rows = parse_candidate_ledger(support_wire, result["exact_graph_support_ledger"], SUPPORT_ROW_SCHEMA)
    identity_rows = parse_candidate_ledger(identity_wire, result["member_identity_disposition_ledger"], IDENTITY_ROW_SCHEMA)
    need(len(support_rows) == len(identity_rows) == 5_264, "candidate ledger census")
    need(Counter(row["graph_class"] for row in support_rows) == CLASS_COUNTS, "candidate support class census")
    need([row["graph_ordinal"] for row in support_rows] == [row["graph_ordinal"] for row in identity_rows], "candidate aligned ordinals")
    need(len({row["graph_id"] for row in support_rows}) == len({row["sheet_member_id"] for row in support_rows}) == 5_264, "candidate support bijection")
    need(len({row["natural_key_preimage_sha256"] for row in identity_rows}) == 5_264, "candidate natural-key uniqueness")
    support_by_graph = {row["graph_id"]: row for row in support_rows}
    for ordinal, row in enumerate(support_rows):
        need(row["coordinate_parameter"] == "TPS", "candidate coordinate parameter")
        validate_primitive_ast(row["carrier_domain_ast"], "support[" + str(ordinal) + "].carrier")
        validate_primitive_ast(row["base_domain_ast"], "support[" + str(ordinal) + "].base")
        validate_primitive_ast(row["equation_ast"], "support[" + str(ordinal) + "].equation")
        validate_primitive_ast(row["exact_support_ast"], "support[" + str(ordinal) + "].support")
        need(row["ast_sha256"] == {
            "carrier_domain_ast_sha256": object_sha(row["carrier_domain_ast"]),
            "base_domain_ast_sha256": object_sha(row["base_domain_ast"]),
            "equation_ast_sha256": object_sha(row["equation_ast"]),
            "exact_support_ast_sha256": object_sha(row["exact_support_ast"]),
        }, "candidate AST hashes")
        need(row["scoped_credit"] == {"exact_G2_feature_support_AST": 1, "member_natural_key_preservation": 0}, "candidate row support credit")
        need(row["downstream_nonpromotion"] == DOWNSTREAM_ZERO, "candidate support nonpromotion")
    for row in identity_rows:
        support = support_by_graph.get(row["graph_id"])
        need(support is not None and row["sheet_member_id"] == support["sheet_member_id"], "candidate identity-support pairing")
        need(row["exact_support_ref"] == row_ref(support), "candidate identity support reference")
        need(row["natural_key_preimage_sha256"] == object_sha(row["natural_key_preimage"]), "candidate natural-key hash")
        need(row["recomputed_member_id"] == row["sheet_member_id"], "candidate recomputed member")
        need(row["disposition"] == "PRESERVE_EXISTING_MEMBER_ID" and row["member_natural_key_preservation_credit"] == 1, "candidate natural-key preservation credit")
        need(row["set_equality_proved"] is False and row["physical_incidence_proved"] is False and row["identity_representation_pullback_proved"] is False, "candidate identity nonpromotion")
        prerequisites = row["identity_prerequisites"]
        need("graph_to_sheet_key_bijection" not in prerequisites and "one_graph_per_sheet" not in prerequisites, "candidate no set-like key claim")
        need(prerequisites["one_graph_inventory_row_per_member_natural_key"] is True and prerequisites["natural_key_graph_member_pair_bijection"] is True, "candidate scoped natural-key pairing")
        need(row["downstream_nonpromotion"] == DOWNSTREAM_ZERO, "candidate identity nonpromotion ledger")
    return result


@dataclass(frozen=True)
class CandidateRecord:
    filename: str
    size: int
    sha256: str


class CandidateBundle:
    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.directory_descriptor = -1
        self.file_descriptors: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}
        self.records: dict[str, CandidateRecord] = {}
        self.payloads: dict[str, bytes] = {}

    def __enter__(self) -> "CandidateBundle":
        resolved = self.directory.resolve()
        need(os.path.commonpath((str(resolved), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
        before = os.stat(self.directory, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not self.directory.is_symlink() and set(os.listdir(self.directory)) == set(OUTPUT_NAMES), "candidate exact directory")
        self.directory_descriptor = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for filename in OUTPUT_NAMES:
            info = os.stat(filename, dir_fd=self.directory_descriptor, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "candidate file identity:" + filename)
            descriptor = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.directory_descriptor)
            opened = os.fstat(descriptor)
            need(identity(opened) == identity(info), "candidate file race:" + filename)
            digest = hash_fd(descriptor)
            need(digest == hash_fd(descriptor), "candidate two-pass digest:" + filename)
            self.file_descriptors[filename] = descriptor
            self.identities[filename] = identity(opened)
            self.records[filename] = CandidateRecord(filename, info.st_size, digest)
            self.payloads[filename] = read_fd(descriptor)
        validate_candidate_payloads(self.payloads[RESULT_NAME], self.payloads[SUPPORT_NAME], self.payloads[IDENTITY_NAME])
        return self

    def final(self) -> None:
        for filename in reversed(OUTPUT_NAMES):
            need(identity(os.fstat(self.file_descriptors[filename])) == self.identities[filename], "candidate final fd:" + filename)
            need(identity(os.stat(filename, dir_fd=self.directory_descriptor, follow_symlinks=False)) == self.identities[filename], "candidate final path:" + filename)
            need(hash_fd(self.file_descriptors[filename]) == self.records[filename].sha256, "candidate final digest:" + filename)

    def __exit__(self, *_: Any) -> None:
        for descriptor in self.file_descriptors.values():
            try:
                os.close(descriptor)
            except OSError:
                pass
        if self.directory_descriptor >= 0:
            os.close(self.directory_descriptor)


def receipt(records: Mapping[str, CandidateRecord], expected: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "status": "PASS_INDEPENDENT_5264_EXACT_PRIMITIVE_G2_SUPPORT_ASTS__5264_NATURAL_KEYS_PRESERVED__ZERO_DOWNSTREAM_CREDIT",
        "candidate_files": [records[name].__dict__ for name in OUTPUT_NAMES],
        "result_sha256": expected["result_sha256"],
        "exact_G2_feature_support_AST_rows": 5_264,
        "member_natural_key_preservation_rows": 5_264,
        "producer_imported_or_executed_or_parsed": False,
        "scoped_credit": {"exact_G2_feature_support_AST": 5_264, "member_natural_key_preservation": 5_264},
        "formal_credit": DOWNSTREAM_ZERO,
    }


def verify(candidate_dir: Path, expected_bundle: tuple[dict[str, Any], bytes, bytes] | None = None) -> dict[str, Any]:
    expected = independently_reconstruct() if expected_bundle is None else expected_bundle
    with CandidateBundle(candidate_dir) as candidate:
        need(candidate.payloads[RESULT_NAME] == canonical(expected[0]), "candidate independently reconstructed result")
        need(candidate.payloads[SUPPORT_NAME] == expected[1], "candidate independently reconstructed support ledger")
        need(candidate.payloads[IDENTITY_NAME] == expected[2], "candidate independently reconstructed identity ledger")
        result = receipt(candidate.records, expected[0])
        candidate.final()
    return result


def self_sha() -> str:
    info = os.stat(__file__, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "verifier identity")
    descriptor = os.open(__file__, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        need(identity(os.fstat(descriptor)) == identity(info), "verifier race")
        digest = hash_fd(descriptor)
        need(digest == hash_fd(descriptor), "verifier two-pass digest")
        return digest
    finally:
        os.close(descriptor)


def close_result(value: dict[str, Any]) -> bytes:
    body = dict(value)
    body.pop("result_sha256", None)
    return canonical({**body, "result_sha256": object_sha(body)})


def rewrite_result(path: Path, mutator: Any) -> None:
    value = json.loads(path.read_bytes())
    need(type(value) is dict, "attack result")
    mutator(value)
    path.write_bytes(close_result(value))


def coherent_ledger_mutation(
    directory: Path,
    filename: str,
    descriptor_field: str,
    mutator: Any,
) -> None:
    result_path = directory / RESULT_NAME
    result = json.loads(result_path.read_bytes())
    source_path = directory / filename
    temporary_path = directory / (filename + ".attack-tmp")
    plain_digest = hashlib.sha256()
    ordered_row_ids_digest = hashlib.sha256()
    ordered_row_hashes_digest = hashlib.sha256()
    ordered_rows_digest = hashlib.sha256()
    row_count = 0
    plain_size = 0
    row_schema = None
    try:
        with gzip.open(source_path, "rb") as source, temporary_path.open("wb") as raw_target:
            with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=raw_target, mtime=0) as target:
                for line in source:
                    need(line.endswith(b"\n"), "attack canonical ledger line")
                    row = json.loads(line)
                    if row_count == 0:
                        mutator(row)
                        body = dict(row)
                        body.pop("row_sha256", None)
                        row = {**body, "row_sha256": object_sha(body)}
                        row_schema = row["schema"]
                    canonical_line = canonical(row) + b"\n"
                    target.write(canonical_line)
                    plain_digest.update(canonical_line)
                    plain_size += len(canonical_line)
                    ordered_row_ids_digest.update(canonical(row["row_id"]) + b"\n")
                    ordered_row_hashes_digest.update(canonical(row["row_sha256"]) + b"\n")
                    ordered_rows_digest.update(canonical_line)
                    row_count += 1
        need(row_count > 0 and type(row_schema) is str, "attack nonempty ledger")
        os.replace(temporary_path, source_path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
    wire_size = source_path.stat().st_size
    wire_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()
    result[descriptor_field] = {
        "filename": filename,
        "compression": "gzip-level9-mtime-zero",
        "row_schema": row_schema,
        "row_count": row_count,
        "compressed_size": wire_size,
        "compressed_sha256": wire_sha256,
        "uncompressed_size": plain_size,
        "uncompressed_sha256": plain_digest.hexdigest(),
        "ordered_row_ids_sha256": ordered_row_ids_digest.hexdigest(),
        "ordered_row_hashes_sha256": ordered_row_hashes_digest.hexdigest(),
        "ordered_rows_sha256": ordered_rows_digest.hexdigest(),
    }
    result_path.write_bytes(close_result(result))


def flip_last_byte(path: Path) -> None:
    payload = bytearray(path.read_bytes())
    need(len(payload) > 8, "attack payload")
    payload[-1] ^= 1
    path.write_bytes(payload)


def attack_suite(candidate_dir: Path) -> dict[str, Any]:
    expected = independently_reconstruct()
    baseline = verify(candidate_dir, expected)
    work = Path(tempfile.mkdtemp(prefix="cm2-c10-support-identity-attacks-"))
    attacks: list[dict[str, Any]] = []

    def restore() -> None:
        for path in work.iterdir():
            if path.is_symlink() or path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
        for filename in OUTPUT_NAMES:
            shutil.copyfile(candidate_dir / filename, work / filename)

    def execute(attack_id: str, mutation: Any, cleanup: Any | None = None) -> None:
        restore()
        try:
            mutation()
            rejection = None
            try:
                verify(work, expected)
            except (Rejected, OSError, EOFError, gzip.BadGzipFile, json.JSONDecodeError, UnicodeDecodeError, KeyError, ValueError) as error:
                rejection = type(error).__name__ + ":" + str(error)
            need(rejection is not None, "attack accepted:" + attack_id)
            core = {"attack_id": attack_id, "rejected": True, "rejection_boundary": rejection}
            attacks.append({**core, "row_sha256": object_sha(core)})
        finally:
            if cleanup is not None:
                cleanup()

    try:
        execute("A01_EXTRA_FILE", lambda: (work / "foreign").write_bytes(b"x"), lambda: (work / "foreign").unlink())
        execute("A02_MISSING_RESULT", lambda: (work / RESULT_NAME).unlink())
        execute("A03_RESULT_SYMLINK", lambda: ((work / RESULT_NAME).unlink(), (work / RESULT_NAME).symlink_to(candidate_dir / RESULT_NAME)))

        hardlink_target = work.parent / (work.name + "-hardlink")

        def hardlink_result() -> None:
            (work / RESULT_NAME).unlink()
            shutil.copyfile(candidate_dir / RESULT_NAME, hardlink_target)
            os.link(hardlink_target, work / RESULT_NAME)

        execute("A04_RESULT_HARDLINK", hardlink_result, lambda: hardlink_target.unlink())
        execute("A05_RESULT_SCHEMA", lambda: rewrite_result(work / RESULT_NAME, lambda value: value.__setitem__("schema", "foreign")))
        execute("A06_PRODUCER_PIN", lambda: rewrite_result(work / RESULT_NAME, lambda value: value["producer_source"].__setitem__("sha256", "0" * 64)))
        execute("A07_SOURCE_PIN", lambda: rewrite_result(work / RESULT_NAME, lambda value: value["source_pins"][0].__setitem__("sha256", "0" * 64)))
        execute("A08_SUPPORT_CREDIT_COUNT", lambda: rewrite_result(work / RESULT_NAME, lambda value: value["scoped_credit"].__setitem__("exact_G2_feature_support_AST", 5_263)))
        execute("A09_IDENTITY_CREDIT_COUNT", lambda: rewrite_result(work / RESULT_NAME, lambda value: value["scoped_credit"].__setitem__("member_natural_key_preservation", 5_263)))
        execute("A10_PHYSICAL_CREDIT", lambda: rewrite_result(work / RESULT_NAME, lambda value: value["formal_credit"].__setitem__("physical_incidence", 1)))
        execute("A11_PULLBACK_CREDIT", lambda: rewrite_result(work / RESULT_NAME, lambda value: value["formal_credit"].__setitem__("representation_pullback", 1)))
        execute("A12_B1A_CREDIT", lambda: rewrite_result(work / RESULT_NAME, lambda value: value["strict_nonpromotion"].__setitem__("B1A_permitted", True)))
        execute("A13_CM2_PROMOTION", lambda: rewrite_result(work / RESULT_NAME, lambda value: value["strict_nonpromotion"].__setitem__("CM2", "PASS")))
        execute("A14_DENOMINATOR", lambda: rewrite_result(work / RESULT_NAME, lambda value: value["C9_denominator_preserved"].__setitem__("remaining_physical_incidence_theorem_rows", 15_381)))

        def opaque_macro(row: dict[str, Any]) -> None:
            row["equation_ast"] = {"op": "TARGET_FIRST_HIT_WALL_FACTOR", "variables": ["t", "p"]}

        execute("A15_OPAQUE_TARGET_MACRO", lambda: coherent_ledger_mutation(work, SUPPORT_NAME, "exact_graph_support_ledger", opaque_macro))

        def expression_string(row: dict[str, Any]) -> None:
            row["equation_ast"] = {"op": "R242_TRANSITION_FACTOR", "expression": "target_normal_x^2-target_normal_y^2"}

        execute("A16_EXPRESSION_STRING", lambda: coherent_ledger_mutation(work, SUPPORT_NAME, "exact_graph_support_ledger", expression_string))
        execute("A17_SUPPORT_ROW_CREDIT", lambda: coherent_ledger_mutation(work, SUPPORT_NAME, "exact_graph_support_ledger", lambda row: row["scoped_credit"].__setitem__("exact_G2_feature_support_AST", 0)))
        execute("A18_SUPPORT_PHYSICAL_PROMOTION", lambda: coherent_ledger_mutation(work, SUPPORT_NAME, "exact_graph_support_ledger", lambda row: row["downstream_nonpromotion"].__setitem__("physical_incidence", 1)))
        execute("A19_NATURAL_KEY_PREIMAGE", lambda: coherent_ledger_mutation(work, IDENTITY_NAME, "member_identity_disposition_ledger", lambda row: row["natural_key_preimage"].append("support-geometry")))
        execute("A20_SET_EQUALITY", lambda: coherent_ledger_mutation(work, IDENTITY_NAME, "member_identity_disposition_ledger", lambda row: row.__setitem__("set_equality_proved", True)))
        execute("A21_PHYSICAL_INCIDENCE", lambda: coherent_ledger_mutation(work, IDENTITY_NAME, "member_identity_disposition_ledger", lambda row: row.__setitem__("physical_incidence_proved", True)))
        execute("A22_SETLIKE_KEY_BIJECTION", lambda: coherent_ledger_mutation(work, IDENTITY_NAME, "member_identity_disposition_ledger", lambda row: row["identity_prerequisites"].__setitem__("graph_to_sheet_key_bijection", True)))
        execute("A23_SUPPORT_WIRE_MUTATION", lambda: flip_last_byte(work / SUPPORT_NAME))
        execute("A24_IDENTITY_WIRE_MUTATION", lambda: flip_last_byte(work / IDENTITY_NAME))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    need(len(attacks) == 24, "attack count")
    body = {
        "schema": SCHEMA + ".coherent-attack-suite.v1",
        "status": "PASS_24_OF_24_COHERENT_ATTACKS_REJECTED",
        "verifier_filename": Path(__file__).name,
        "verifier_file_sha256": self_sha(),
        "attack_count": 24,
        "rejected_count": 24,
        "all_rejected": True,
        "baseline_result_file_sha256": next(row["sha256"] for row in baseline["candidate_files"] if row["filename"] == RESULT_NAME),
        "attacks": attacks,
    }
    return {**body, "attack_suite_sha256": object_sha(body)}


def read_closed(path: Path, closure: str) -> tuple[dict[str, Any], bytes]:
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "closed document identity:" + path.name)
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(descriptor)
        need(identity(opened) == identity(info), "closed document race:" + path.name)
        raw = read_fd(descriptor)
        need(hash_fd(descriptor) == hash_fd(descriptor), "closed document two-pass:" + path.name)
    finally:
        os.close(descriptor)
    value = json.loads(raw)
    need(type(value) is dict and raw == canonical(value), "closed canonical document:" + path.name)
    body = dict(value)
    claimed = body.pop(closure, None)
    need(type(claimed) is str and claimed == object_sha(body), "closed document closure:" + path.name)
    return value, raw


def verification_document(
    result: dict[str, Any],
    attack_raw: bytes | None = None,
    verifier_digest: str | None = None,
) -> dict[str, Any]:
    if attack_raw is None:
        suite, raw = read_closed(ROOT / ATTACK_NAME, "attack_suite_sha256")
    else:
        raw = attack_raw
        suite = json.loads(raw)
        need(type(suite) is dict and raw == canonical(suite), "held attack canonical")
        body = dict(suite)
        claimed = body.pop("attack_suite_sha256", None)
        need(type(claimed) is str and claimed == object_sha(body), "held attack closure")
    expected_verifier = self_sha() if verifier_digest is None else verifier_digest
    need(suite["verifier_file_sha256"] == expected_verifier, "attack-verifier binding")
    need((suite["attack_count"], suite["rejected_count"], suite["all_rejected"]) == (24, 24, True), "attack suite census")
    body = {
        "schema": SCHEMA + ".verification.v1",
        **result,
        "attack_suite": {
            "filename": ATTACK_NAME,
            "file_sha256": hashlib.sha256(raw).hexdigest(),
            "object_self_sha256": suite["attack_suite_sha256"],
            "attack_count": 24,
            "rejected_count": 24,
            "all_rejected": True,
        },
        "formal_credit_marker": DOWNSTREAM_ZERO,
    }
    return {**body, "verification_sha256": object_sha(body)}


MANIFEST_MEMBERS: Final = (
    PRODUCER_NAME,
    SUPPORT_NAME,
    IDENTITY_NAME,
    RESULT_NAME,
    Path(__file__).name,
    ATTACK_NAME,
    VERIFICATION_NAME,
    REPORT_NAME,
    COLD_NAME,
)


class ManifestBundle:
    def __init__(self) -> None:
        self.directory_descriptor = -1
        self.manifest_descriptor = -1
        self.manifest_identity: tuple[int, ...] = ()
        self.file_descriptors: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}
        self.hashes: dict[str, str] = {}
        self.payloads: dict[str, bytes] = {}

    def __enter__(self) -> "ManifestBundle":
        self.directory_descriptor = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        info = os.stat(MANIFEST_NAME, dir_fd=self.directory_descriptor, follow_symlinks=False)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "manifest identity")
        self.manifest_descriptor = os.open(MANIFEST_NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.directory_descriptor)
        opened = os.fstat(self.manifest_descriptor)
        need(identity(opened) == identity(info), "manifest race")
        self.manifest_identity = identity(opened)
        raw = read_fd(self.manifest_descriptor)
        need(raw.endswith(b"\n"), "manifest newline")
        lines = raw.decode("ascii").splitlines()
        need(len(lines) == len(MANIFEST_MEMBERS), "manifest member count")
        for line, filename in zip(lines, MANIFEST_MEMBERS):
            pieces = line.split("  ")
            need(len(pieces) == 2 and pieces[1] == filename and len(pieces[0]) == 64, "manifest ordered member:" + filename)
            int(pieces[0], 16)
            member_info = os.stat(filename, dir_fd=self.directory_descriptor, follow_symlinks=False)
            need(stat.S_ISREG(member_info.st_mode) and member_info.st_nlink == 1, "manifest member identity:" + filename)
            descriptor = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.directory_descriptor)
            member_opened = os.fstat(descriptor)
            need(identity(member_opened) == identity(member_info), "manifest member race:" + filename)
            digest = hash_fd(descriptor)
            need(digest == hash_fd(descriptor) == pieces[0], "manifest member digest:" + filename)
            self.file_descriptors[filename] = descriptor
            self.identities[filename] = identity(member_opened)
            self.hashes[filename] = digest
            self.payloads[filename] = read_fd(descriptor)
        need(self.identities[PRODUCER_NAME][4] == PRODUCER_RECORD["size"] and self.hashes[PRODUCER_NAME] == PRODUCER_RECORD["sha256"], "manifest producer byte pin")
        return self

    def final(self) -> None:
        for filename in reversed(MANIFEST_MEMBERS):
            need(identity(os.fstat(self.file_descriptors[filename])) == self.identities[filename], "manifest final fd:" + filename)
            need(identity(os.stat(filename, dir_fd=self.directory_descriptor, follow_symlinks=False)) == self.identities[filename], "manifest final path:" + filename)
            need(hash_fd(self.file_descriptors[filename]) == self.hashes[filename], "manifest final digest:" + filename)
        need(identity(os.fstat(self.manifest_descriptor)) == self.manifest_identity, "manifest final descriptor")
        need(identity(os.stat(MANIFEST_NAME, dir_fd=self.directory_descriptor, follow_symlinks=False)) == self.manifest_identity, "manifest final path")

    def __exit__(self, *_: Any) -> None:
        for descriptor in self.file_descriptors.values():
            try:
                os.close(descriptor)
            except OSError:
                pass
        if self.manifest_descriptor >= 0:
            os.close(self.manifest_descriptor)
        if self.directory_descriptor >= 0:
            os.close(self.directory_descriptor)


def manifest_first() -> dict[str, Any]:
    with ManifestBundle() as bundle:
        verifier_digest = bundle.hashes[Path(__file__).name]
        need(verifier_digest == self_sha(), "manifest verifier binding")
        validate_candidate_payloads(bundle.payloads[RESULT_NAME], bundle.payloads[SUPPORT_NAME], bundle.payloads[IDENTITY_NAME])
        expected = independently_reconstruct()
        need(bundle.payloads[RESULT_NAME] == canonical(expected[0]), "manifest independently reconstructed result")
        need(bundle.payloads[SUPPORT_NAME] == expected[1], "manifest independently reconstructed support ledger")
        need(bundle.payloads[IDENTITY_NAME] == expected[2], "manifest independently reconstructed identity ledger")
        records = {
            filename: CandidateRecord(filename, bundle.identities[filename][4], bundle.hashes[filename])
            for filename in OUTPUT_NAMES
        }
        result = receipt(records, expected[0])
        need(bundle.payloads[VERIFICATION_NAME] == canonical(verification_document(result, bundle.payloads[ATTACK_NAME], verifier_digest)), "manifest verification byte identity")
        bundle.final()
    return {
        "status": "PASS_MANIFEST_FIRST_HELD_FD_5264_EXACT_PRIMITIVE_G2_SUPPORT_ASTS__5264_NATURAL_KEYS__ZERO_WRITES_ZERO_DOWNSTREAM_CREDIT",
        "manifest_filename": MANIFEST_NAME,
        "manifest_member_count": len(MANIFEST_MEMBERS),
        "result_sha256": expected[0]["result_sha256"],
        "exact_G2_feature_support_AST_rows": 5_264,
        "member_natural_key_preservation_rows": 5_264,
        "producer_imported_or_executed_or_parsed": False,
        "deliverables_write_syscalls": 0,
        "formal_credit": DOWNSTREAM_ZERO,
    }


def publish_document(filename: str, value: dict[str, Any]) -> None:
    path = ROOT / filename
    need(not path.exists(), "publish no-clobber:" + filename)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        payload = canonical(value)
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            need(written > 0, "publish progress:" + filename)
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-dir")
    parser.add_argument("--verify-no-write", action="store_true")
    parser.add_argument("--attack-publish", action="store_true")
    parser.add_argument("--verify-publish", action="store_true")
    parser.add_argument("--manifest-first-no-write", action="store_true")
    arguments = parser.parse_args()
    need(sum((arguments.verify_no_write, arguments.attack_publish, arguments.verify_publish, arguments.manifest_first_no_write)) == 1, "exactly one mode")
    if arguments.manifest_first_no_write:
        result = manifest_first()
    else:
        need(arguments.candidate_dir is not None, "candidate required")
        candidate_dir = Path(arguments.candidate_dir)
        if arguments.attack_publish:
            suite = attack_suite(candidate_dir)
            publish_document(ATTACK_NAME, suite)
            result = {"status": suite["status"], "attack_count": 24, "attack_suite_sha256": suite["attack_suite_sha256"]}
        else:
            result = verify(candidate_dir)
            if arguments.verify_publish:
                publish_document(VERIFICATION_NAME, verification_document(result))
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
