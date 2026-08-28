#!/usr/bin/env python3
"""Produce sixteen scoped R235D-to-G2 orphan-graph semantic dispositions."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import gzip
import hashlib
from itertools import product
import json
from math import isqrt
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Final, Iterable, Mapping


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge"
RESULT_NAME: Final = PREFIX + "_result.json"
LEDGER_NAME: Final = PREFIX + "_row_ledger.jsonl.gz"
SCHEMA: Final = "cm2.round306c4.source-g-r235d-to-g2-orphan-graph-semantic-bridge.v1"
ROW_SCHEMA: Final = SCHEMA + ".row.v1"
STATUS: Final = "PASS_16_R235D_TO_G2_ORPHAN_TARGET_GRAPH_EMPTY_DISPOSITIONS__ZERO_INCIDENCE_PULLBACK_TRACE_SUPPORT_CREDIT"
OWNER_RE: Final = re.compile(r"^G\[(-?[0-9]+),(-?[0-9]+)\]$")
SQRT_BITS: Final = 128


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("C3_MANIFEST", "cm2_round306c3_source_g_corrected_g2_exact_join_filter_manifest.sha256", 956, "f05f172ec8fc25564067539091f77f39bc33395dd5e0232f38bde9c587493761"),
    Pin("C3_RESULT", "cm2_round306c3_source_g_corrected_g2_exact_join_filter_result.json", 6_458, "66df0b03fdc9f432e330f55eeedc3f49fad0fa2f12fbb6d94689e06a6cc9d8a0"),
    Pin("C0_MANIFEST", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_manifest.sha256", 2_182, "9ddb6e0ad37b634de8b2edf8573247e7c1263a5c3693c77a7d001241712b25f8"),
    Pin("C0_INVALID", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_member_invalidation_ledger.jsonl.gz", 11_867, "865185d9b49d4e220459cb083683fd5a074f63eff4f7f2f8217a5c5204991eae"),
    Pin("R235D_MANIFEST", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_manifest.sha256", 1_276, "0aa2128655e7f90eaeeda47a66901ea45e0908a6f569dc7760ead49ac539e7c0"),
    Pin("R235D_RESULT", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_result.json", 45_075, "3856a04a5b88574f1ffd6aac7f4fda42c014eac401c2a73efbc6c0ea10c9e5ff"),
    Pin("R235D_LEDGER", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_row_commitment_ledger.jsonl.gz", 144_211, "6eaeee6a158ad7c0c3d62380214e1ae24ac2a63cb7678b312401cca91cb4cfe0"),
    Pin("B1G0_MANIFEST", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256", 1_959, "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8"),
    Pin("B1G0_GRAPH", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz", 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"),
    Pin("B1G0_SHEET", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),
    Pin("B1G0_SIDE", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),
    Pin("R234_CERT", "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    Pin("R235_CERT", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json", 67_765_471, "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"),
    Pin("R236_CERT", "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", 2_061_199, "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
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
        parts: list[bytes] = []
        while True:
            block = os.read(fd, 1_048_576)
            if not block:
                return b"".join(parts)
            parts.append(block)

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
    entries: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        digest, path = line.split("  ")
        name = os.path.basename(path)
        need(len(digest) == 64 and path in {name, "deliverables/" + name} and name not in entries, "manifest entry:" + role)
        entries[name] = digest
    return entries


def qwire(value: Q | int) -> dict[str, int]:
    rational = Q(value)
    return {"numerator": rational.numerator, "denominator": rational.denominator}


def qread(value: Mapping[str, Any]) -> Q:
    need(type(value) is dict and set(value) == {"numerator", "denominator"}, "rational wire")
    numerator, denominator = value["numerator"], value["denominator"]
    need(type(numerator) is int and type(denominator) is int and denominator > 0, "rational type")
    rational = Q(numerator, denominator)
    need((rational.numerator, rational.denominator) == (numerator, denominator), "reduced rational")
    return rational


def const(value: Q | int) -> dict[str, Any]:
    return {"op": "CONST_Q", "value": qwire(value)}


def var(name: str) -> dict[str, Any]:
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


def differentiate(node: Mapping[str, Any], variable: str) -> dict[str, Any]:
    op = node["op"]
    if op == "CONST_Q":
        return const(0)
    if op == "VAR":
        return const(1 if node["name"] == variable else 0)
    if op == "NEG":
        return neg(differentiate(node["arg"], variable))
    if op == "ADD":
        return add(*(differentiate(arg, variable) for arg in node["args"]))
    if op == "SUB":
        return sub(differentiate(node["left"], variable), differentiate(node["right"], variable))
    if op == "MUL":
        return add(*(mul(*(differentiate(arg, variable) if index == position else arg for position, arg in enumerate(node["args"]))) for index in range(len(node["args"]))))
    if op == "SQUARE":
        return mul(const(2), node["arg"], differentiate(node["arg"], variable))
    if op == "DIV_NONZERO":
        return div_nonzero(sub(mul(differentiate(node["left"], variable), node["right"]), mul(node["left"], differentiate(node["right"], variable))), square(node["right"]))
    if op == "SQRT_POSITIVE":
        return div_nonzero(differentiate(node["arg"], variable), mul(const(2), node))
    raise Rejected("unsupported derivative op:" + str(op))


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

    def neg(self) -> "Interval":
        return Interval(-self.upper, -self.lower)

    def add(self, other: "Interval") -> "Interval":
        return Interval(self.lower + other.lower, self.upper + other.upper)

    def sub(self, other: "Interval") -> "Interval":
        return self.add(other.neg())

    def mul(self, other: "Interval") -> "Interval":
        products = (self.lower * other.lower, self.lower * other.upper, self.upper * other.lower, self.upper * other.upper)
        return Interval(min(products), max(products))

    def square(self) -> "Interval":
        squares = (self.lower * self.lower, self.upper * self.upper)
        return Interval(Q(0) if self.lower <= 0 <= self.upper else min(squares), max(squares))

    def div(self, other: "Interval") -> "Interval":
        need(not other.lower <= 0 <= other.upper, "interval division by zero")
        reciprocal = Interval(min(Q(1, other.lower), Q(1, other.upper)), max(Q(1, other.lower), Q(1, other.upper)))
        return self.mul(reciprocal)

    def excludes_zero(self) -> bool:
        return self.upper < 0 or self.lower > 0

    def wire(self) -> dict[str, Any]:
        return {"lower": qwire(self.lower), "upper": qwire(self.upper)}


def sqrt_interval(value: Interval) -> Interval:
    need(value.lower > 0, "sqrt domain")
    scale = 1 << SQRT_BITS

    def floor_sqrt(rational: Q) -> Q:
        return Q(isqrt((rational.numerator * scale * scale) // rational.denominator), scale)

    lower, upper = floor_sqrt(value.lower), floor_sqrt(value.upper)
    if upper * upper != value.upper:
        upper += Q(1, scale)
    need(lower * lower <= value.lower and upper * upper >= value.upper, "sqrt enclosure")
    return Interval(lower, upper)


def evaluate(node: Mapping[str, Any], environment: Mapping[str, Interval]) -> Interval:
    op = node["op"]
    if op == "CONST_Q":
        return Interval.point(qread(node["value"]))
    if op == "VAR":
        need(node["name"] in environment, "bound variable")
        return environment[node["name"]]
    if op == "NEG":
        return evaluate(node["arg"], environment).neg()
    if op == "ADD":
        output = Interval.point(0)
        for arg in node["args"]:
            output = output.add(evaluate(arg, environment))
        return output
    if op == "SUB":
        return evaluate(node["left"], environment).sub(evaluate(node["right"], environment))
    if op == "MUL":
        output = Interval.point(1)
        for arg in node["args"]:
            output = output.mul(evaluate(arg, environment))
        return output
    if op == "SQUARE":
        return evaluate(node["arg"], environment).square()
    if op == "DIV_NONZERO":
        return evaluate(node["left"], environment).div(evaluate(node["right"], environment))
    if op == "SQRT_POSITIVE":
        return sqrt_interval(evaluate(node["arg"], environment))
    raise Rejected("unsupported interval op:" + str(op))


def factor_asts(endpoint: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    kind, axis, wall_text = endpoint["reason_labels"][0].split(":")
    need(kind == "wall_endpoint_or_count_transition" and axis in {"X", "Y"} and int(wall_text) == 0, "endpoint reason")
    chart = endpoint["chart"]
    need(chart in {"G:E", "G:W", "G:N", "G:S"}, "source chart")
    owner = OWNER_RE.fullmatch(endpoint["owner_target"])
    need(owner is not None, "owner target")
    owner_x, owner_y = Q(int(owner.group(1))), Q(int(owner.group(2)))
    t, p = var("t"), var("p")
    normal_root = sqrt_positive(sub(const(1), square(t)))
    phase_root = sqrt_positive(sub(const(1), square(p)))
    cell = chart[-1]
    if cell == "E":
        normal_x, normal_y = normal_root, t
    elif cell == "W":
        normal_x, normal_y = neg(normal_root), t
    elif cell == "N":
        normal_x, normal_y = t, normal_root
    else:
        normal_x, normal_y = t, neg(normal_root)
    tangent_x = sub(mul(phase_root, normal_x), mul(p, normal_y))
    tangent_y = add(mul(phase_root, normal_y), mul(p, normal_x))
    radius = Q(9, 25)
    source_x, source_y = mul(const(radius), normal_x), mul(const(radius), normal_y)
    delta_x, delta_y = sub(const(owner_x), source_x), sub(const(owner_y), source_y)
    transverse = add(neg(mul(tangent_y, delta_x)), mul(tangent_x, delta_y))
    radical = sqrt_positive(sub(const(radius * radius), square(transverse)))
    hit_x = add(const(owner_x), neg(mul(radical, tangent_x)), mul(transverse, tangent_y))
    hit_y = add(const(owner_y), neg(mul(radical, tangent_y)), neg(mul(transverse, tangent_x)))
    source = source_x if axis == "X" else source_y
    target = hit_x if axis == "X" else hit_y
    return sub(source, const(0)), sub(target, const(0))


def box_wire(bounds: list[tuple[Q, Q]], closures: list[tuple[bool, bool]]) -> dict[str, Any]:
    return {"wire_id": "RATIONAL_INTERVAL_BOX_V1", "coordinate_parameter": "TPS", "axes": [{"axis": axis, "lower": qwire(lower), "lower_closed": lower_closed, "upper": qwire(upper), "upper_closed": upper_closed} for axis, (lower, upper), (lower_closed, upper_closed) in zip("tps", bounds, closures, strict=True)]}


def proof_domain(endpoint: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    t0, t1, p0, p1, s0, s1 = map(Q, endpoint["box"])
    t_mid, p_mid = (t0 + t1) / 2, (p0 + p1) / 2
    parent = box_wire([(t0, t1), (p0, p1), (s0, s1)], [(True, True)] * 3)
    cells: list[dict[str, Any]] = []
    for t_index, p_index in product(range(2), repeat=2):
        t_bounds = (t0, t_mid) if t_index == 0 else (t_mid, t1)
        p_bounds = (p0, p_mid) if p_index == 0 else (p_mid, p1)
        cells.append(box_wire([t_bounds, p_bounds, (s0, s1)], [(True, False) if t_index == 0 else (True, True), (True, False) if p_index == 0 else (True, True), (True, True)]))
    need(len(cells) == 4, "domain cell count")
    return parent, cells


def environment(box: dict[str, Any]) -> dict[str, Interval]:
    return {axis["axis"]: Interval(qread(axis["lower"]), qread(axis["upper"])) for axis in box["axes"]}


def row_ref(ordinal: int, row: dict[str, Any], field: str) -> list[Any]:
    need(type(row.get(field)) is str, "row identifier:" + field)
    return [ordinal, row[field], hashlib.sha256(canonical(row)).hexdigest()]


def closed_ref(ordinal: int, row: dict[str, Any], field: str) -> list[Any]:
    need(type(row.get(field)) is str and type(row.get("row_sha256")) is str, "closed row shape:" + field)
    body = dict(row)
    claimed = body.pop("row_sha256")
    need(claimed == objsha(body), "closed row digest:" + field)
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


def index_unique(rows: list[dict[str, Any]], fields: tuple[str, ...], label: str) -> dict[tuple[Any, ...], tuple[int, dict[str, Any]]]:
    output: dict[tuple[Any, ...], tuple[int, dict[str, Any]]] = {}
    for ordinal, row in enumerate(rows):
        key = tuple(row[field] for field in fields)
        need(key not in output, "duplicate index:" + label)
        output[key] = (ordinal, row)
    return output


def build() -> tuple[dict[str, Any], bytes]:
    with Snapshot() as snapshot:
        pin_by_role = {pin.role: pin for pin in PINS}
        manifests = {role: manifest_entries(snapshot, role) for role in ("C3_MANIFEST", "C0_MANIFEST", "R235D_MANIFEST", "B1G0_MANIFEST")}
        for manifest_role, file_roles in {
            "C3_MANIFEST": ("C3_RESULT",),
            "C0_MANIFEST": ("C0_INVALID",),
            "R235D_MANIFEST": ("R235D_RESULT", "R235D_LEDGER"),
            "B1G0_MANIFEST": ("B1G0_GRAPH", "B1G0_SHEET", "B1G0_SIDE"),
        }.items():
            for file_role in file_roles:
                pin = pin_by_role[file_role]
                need(manifests[manifest_role][pin.filename] == pin.sha256, "manifest binding:" + manifest_role + ":" + file_role)

        c3 = direct(snapshot, "C3_RESULT")
        need(c3["schema"] == "cm2.round306c3.source-g-corrected-g2-exact-join-filter.v1" and c3["result_sha256"] == "6a51130ddc5e2cfcf175abd8b20f0de310353ccf7cd7b7037f86bf5cab24d882", "C3 result")
        need(c3["corrected_census"] == {"graph_definition_rows": 38_624, "G2A_sheet_members": 38_608, "G2B_side_references": 76_832, "G2B_side_distinct_members": 76_816, "duplicate_side_reference_excess": 16, "physical_incidence_relations": 115_440, "semantic_obligation_rows": 154_064}, "C3 census")
        need(c3["formal_blockers"]["source_graph_definition_theorems_pending"] == 38_624, "C3 graph blockers")

        r235d_result = direct(snapshot, "R235D_RESULT")
        need(r235d_result["schema"] == "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.result.v1", "R235D schema")
        need(r235d_result["result"]["authority_ledger"]["sha256"] == pin_by_role["R235D_LEDGER"].sha256 and r235d_result["result"]["authority_ledger"]["row_count"] == 16, "R235D ledger binding")
        authority_rows = jsonl(snapshot, "R235D_LEDGER")
        need(len(authority_rows) == 16 and [row["authority_ordinal"] for row in authority_rows] == list(range(16)), "R235D row census")

        invalid_rows = jsonl(snapshot, "C0_INVALID")
        invalid = {row["registry_member_id"] for row in invalid_rows}
        need(len(invalid_rows) == len(invalid) == 32, "C0 invalid census")

        r234_doc = direct(snapshot, "R234_CERT")
        r234_rows = r234_doc["result"]["depth6_frontier_rows"]
        r234_index = {row["frontier_row_id"]: (ordinal, row) for ordinal, row in enumerate(r234_rows)}
        need(len(r234_index) == len(r234_rows), "R234 unique frontier")

        r235_doc = direct(snapshot, "R235_CERT")
        deferred = r235_doc["result"]["double_endpoint_deferred_rows"]
        deferred_ids = {row["Round234_frontier_row_id"] for row in deferred}
        need(len(deferred) == len(deferred_ids) == 16, "R235 deferred census")

        r236_doc = direct(snapshot, "R236_CERT")
        r236_rows = r236_doc["result"]["double_endpoint_partition_rows"]
        r236_index = index_unique(r236_rows, ("Round220_split_interface_id",), "R236 interface")
        r236_by_interface = {key[0]: value for key, value in r236_index.items()}
        need(len(r236_rows) == len(r236_by_interface) == 16, "R236 double census")

        sheet_doc = gzip_doc(snapshot, "B1G0_SHEET")
        all_sheets = sheet_doc["graph_sheet_join_rows"]
        surviving_sheets = [row for row in all_sheets if row["sheet_member_id"] not in invalid]
        sheet_graph_ids = {row["graph_source_inventory_row_id"] for row in surviving_sheets}
        selected_sheets = [(ordinal, row) for ordinal, row in enumerate(all_sheets) if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH"]
        sheet_index = {(row["Round220_split_interface_id"], row["endpoint_factor"]): (ordinal, row) for ordinal, row in selected_sheets}
        need(len(selected_sheets) == len(sheet_index) == 32, "R236 sheet census")

        side_doc = gzip_doc(snapshot, "B1G0_SIDE")
        all_sides = side_doc["graph_side_join_rows"]
        surviving_sides = [row for row in all_sides if row["side_member_id"] not in invalid]
        side_graph_ids = {row["graph_source_inventory_row_id"] for row in surviving_sides}
        orphan_graph_ids = sorted(side_graph_ids - sheet_graph_ids)
        selected_sides = [(ordinal, row) for ordinal, row in enumerate(all_sides) if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH"]
        sides_by_interface: dict[str, dict[str, tuple[int, dict[str, Any]]]] = {}
        for ordinal, row in selected_sides:
            interface = row["Round220_split_interface_id"]
            role = row["side_role"]
            need(role not in sides_by_interface.setdefault(interface, {}), "duplicate side role")
            sides_by_interface[interface][role] = (ordinal, row)
        need(len(selected_sides) == 64 and len(orphan_graph_ids) == 16, "R236 side/orphan census")

        graph_doc = gzip_doc(snapshot, "B1G0_GRAPH")
        all_graphs = graph_doc["graph_source_inventory_rows"]
        selected_graphs = [(ordinal, row) for ordinal, row in enumerate(all_graphs) if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH"]
        graph_index = {(row["Round220_split_interface_id"], row["endpoint_factor"]): (ordinal, row) for ordinal, row in selected_graphs}
        need(len(selected_graphs) == len(graph_index) == 32, "R236 graph census")

        authority_by_interface: dict[str, tuple[int, dict[str, Any]]] = {}
        for ordinal, row in enumerate(authority_rows):
            interface = row["canonical_input_commitment"]["R220_interface"][1]
            need(interface not in authority_by_interface, "R235D unique interface")
            authority_by_interface[interface] = (ordinal, row)
        need(set(authority_by_interface) == set(r236_by_interface), "R235D/R236 interface exhaustion")
        need({row["Round234_frontier_row_id"] for row in authority_rows} == deferred_ids, "R235D/R235 deferred exhaustion")

        output_rows: list[dict[str, Any]] = []
        target_sign_hist: dict[str, int] = {}
        derivative_sign_hist: dict[str, int] = {}
        zero_face_hist: dict[str, int] = {}
        for interface in sorted(authority_by_interface):
            authority_ordinal, authority = authority_by_interface[interface]
            frontier_id = authority["Round234_frontier_row_id"]
            frontier_ordinal, endpoint = r234_index[frontier_id]
            r236_ordinal, r236 = r236_by_interface[interface]
            need(r236["Round234_frontier_row_id"] == frontier_id and r236["double_endpoint_partition_row_id"] == authority["downstream_invalidation"]["R236_double_endpoint_partition_row"][1], "R236 bridge join")

            source_ast, target_ast = factor_asts(endpoint)
            source_dt = differentiate(source_ast, "t")
            target_dp = differentiate(target_ast, "p")
            parent, cells = proof_domain(endpoint)
            source_interval = evaluate(source_dt, environment(parent))
            need(source_interval == Interval.point(Q(9, 25)), "source derivative exact")
            t0, t1 = map(Q, endpoint["box"][:2])
            need((t0 == 0) ^ (t1 == 0), "source zero face")
            zero_face = "LOWER" if t0 == 0 else "UPPER"
            zero_face_hist[zero_face] = zero_face_hist.get(zero_face, 0) + 1
            cell_receipts = []
            for cell_index, cell in enumerate(cells):
                cell_environment = environment(cell)
                target_interval = evaluate(target_ast, cell_environment)
                derivative_interval = evaluate(target_dp, cell_environment)
                need(target_interval.excludes_zero() and derivative_interval.excludes_zero(), "target exclusion")
                target_sign = "STRICT_POSITIVE" if target_interval.lower > 0 else "STRICT_NEGATIVE"
                derivative_sign = "STRICT_POSITIVE" if derivative_interval.lower > 0 else "STRICT_NEGATIVE"
                cell_receipts.append({"cell_index": cell_index, "cell": cell, "target_factor_interval": target_interval.wire(), "target_factor_sign": target_sign, "target_p_derivative_interval": derivative_interval.wire(), "target_p_derivative_sign": derivative_sign})
            target_signs = {cell["target_factor_sign"] for cell in cell_receipts}
            derivative_signs = {cell["target_p_derivative_sign"] for cell in cell_receipts}
            need(len(target_signs) == len(derivative_signs) == 1, "uniform target signs")
            target_sign = next(iter(target_signs))
            derivative_sign = next(iter(derivative_signs))
            target_sign_hist[target_sign] = target_sign_hist.get(target_sign, 0) + 1
            derivative_sign_hist[derivative_sign] = derivative_sign_hist.get(derivative_sign, 0) + 1

            theorem = authority["local_theorem"]
            need(theorem["source_factor_ast"] == source_ast and theorem["source_t_derivative_ast"] == source_dt, "R235D source AST")
            need(theorem["target_factor_ast"] == target_ast and theorem["target_p_derivative_ast"] == target_dp, "R235D target AST")
            need(theorem["source_t_derivative_exact_interval"] == source_interval.wire() and theorem["source_zero_face"] == zero_face, "R235D source theorem")
            need(theorem["rational_cover"] == {"domain_box": parent, "cell_count": 4, "cells": [{"cell_index": item["cell_index"], "cell": item["cell"], "excluded_factor": "TARGET", "target_factor_interval": item["target_factor_interval"], "target_factor_sign": item["target_factor_sign"], "target_p_derivative_interval": item["target_p_derivative_interval"], "target_p_derivative_sign": item["target_p_derivative_sign"]} for item in cell_receipts]}, "R235D rational cover")
            need(theorem["source_zero_set"] == "EXACT_FACE_GRAPH_t_EQUALS_0" and theorem["source_graph_dimension"] == 2 and theorem["target_zero_set_on_domain"] == "EMPTY" and theorem["source_target_codim2_intersection"] == "EMPTY", "R235D semantic conclusion")
            need(theorem["target_factor_fixed_sign"] == target_sign and theorem["target_p_derivative_fixed_sign"] == derivative_sign, "R235D sign conclusion")
            need(authority["local_source_only_endpoint_graph_key_authority_credit"] == 1 and authority["G2_authority_credit"] == 0 and authority["physical_incidence_equivalence_credit"] == 0 and authority["representation_pullback_credit"] == 0, "R235D scope")

            target_graph = graph_index[(interface, "target")]
            source_graph = graph_index[(interface, "source")]
            target_sheet = sheet_index[(interface, "target")]
            source_sheet = sheet_index[(interface, "source")]
            roles = sides_by_interface[interface]
            need(set(roles) == {"target:SAME_SIGN_EVENT_ABSENT", "target:POSITIVE_TO_NEGATIVE", "source:SAME_SIGN_EVENT_ABSENT", "source:NEGATIVE_TO_POSITIVE"}, "side role exhaustion")
            target_shared = roles["target:SAME_SIGN_EVENT_ABSENT"]
            source_shared = roles["source:SAME_SIGN_EVENT_ABSENT"]
            target_only = roles["target:POSITIVE_TO_NEGATIVE"]
            source_only = roles["source:NEGATIVE_TO_POSITIVE"]
            target_graph_id = target_graph[1]["Round306B1G0_graph_source_inventory_row_id"]
            need(target_graph_id in orphan_graph_ids and target_graph_id == authority["downstream_invalidation"]["B1G0_invalid_target_graph_inventory_row"][1], "target orphan graph join")
            need(target_graph[1]["source_row_id"] == source_graph[1]["source_row_id"] == r236["double_endpoint_partition_row_id"], "graph/R236 source join")
            need(target_sheet[1]["sheet_member_id"] in invalid and source_sheet[1]["sheet_member_id"] not in invalid, "sheet correction")
            need(target_only[1]["side_member_id"] in invalid and source_only[1]["side_member_id"] not in invalid, "one-sided correction")
            need(target_shared[1]["side_member_id"] == source_shared[1]["side_member_id"] and target_shared[1]["side_member_id"] not in invalid, "shared side survivor")
            need(target_shared[1]["graph_source_inventory_row_id"] == target_graph_id and source_shared[1]["graph_source_inventory_row_id"] == source_graph[1]["Round306B1G0_graph_source_inventory_row_id"], "shared side graph joins")
            need(target_shared[1]["Round306B1G0_graph_side_join_row_id"] != source_shared[1]["Round306B1G0_graph_side_join_row_id"], "distinct shared-side incidences")
            downstream = authority["downstream_invalidation"]
            need(downstream["B1G0_target_sheet_join_row"][1] == target_sheet[1]["Round306B1G0_graph_sheet_join_row_id"], "R235D target sheet join")
            need(downstream["B1G0_target_shared_side_row"][1] == target_shared[1]["Round306B1G0_graph_side_join_row_id"], "R235D target shared join")
            need(downstream["B1G0_source_shared_side_row"][1] == source_shared[1]["Round306B1G0_graph_side_join_row_id"], "R235D source shared join")
            need(downstream["B1G0_target_only_side_row"][1] == target_only[1]["Round306B1G0_graph_side_join_row_id"], "R235D target-only join")

            input_commitment = {
                "R235D_authority_row": row_ref(authority_ordinal, authority, "authority_row_id"),
                "R234_frontier_row": row_ref(frontier_ordinal, endpoint, "frontier_row_id"),
                "R236_double_endpoint_partition_row": row_ref(r236_ordinal, r236, "double_endpoint_partition_row_id"),
                "B1G0_target_graph_row": closed_ref(*target_graph, "Round306B1G0_graph_source_inventory_row_id"),
                "B1G0_source_graph_row": closed_ref(*source_graph, "Round306B1G0_graph_source_inventory_row_id"),
                "B1G0_target_sheet_row": closed_ref(*target_sheet, "Round306B1G0_graph_sheet_join_row_id"),
                "B1G0_source_sheet_row": closed_ref(*source_sheet, "Round306B1G0_graph_sheet_join_row_id"),
                "B1G0_target_shared_side_row": closed_ref(*target_shared, "Round306B1G0_graph_side_join_row_id"),
                "B1G0_source_shared_side_row": closed_ref(*source_shared, "Round306B1G0_graph_side_join_row_id"),
                "B1G0_target_only_side_row": closed_ref(*target_only, "Round306B1G0_graph_side_join_row_id"),
                "B1G0_source_only_side_row": closed_ref(*source_only, "Round306B1G0_graph_side_join_row_id"),
            }
            semantic = {
                "complete_parameter_domain": parent,
                "complete_domain_partition_kind": "EXACT_2_BY_2_TP_HALF_OPEN_PARTITION_WITH_FULL_S_INTERVAL",
                "complete_domain_partition_cell_count": 4,
                "complete_domain_partition_verified": True,
                "source_factor_ast": source_ast,
                "source_t_derivative_ast": source_dt,
                "source_t_derivative_exact_interval": source_interval.wire(),
                "source_zero_face": zero_face,
                "source_zero_set": "EXACT_FACE_GRAPH_t_EQUALS_0",
                "source_graph_dimension": 2,
                "target_factor_ast": target_ast,
                "target_p_derivative_ast": target_dp,
                "target_factor_fixed_sign": target_sign,
                "target_p_derivative_fixed_sign": derivative_sign,
                "target_zero_set_on_complete_domain": "EMPTY",
                "source_target_codimension_two_intersection": "EMPTY",
                "cell_receipts": cell_receipts,
            }
            disposition = {
                "C3_orphan_target_graph_inventory_row_id": target_graph_id,
                "C3_orphan_target_graph_id": target_graph[1]["graph_id"],
                "disposition": "EMPTY_GRAPH_ON_COMPLETE_PARAMETER_DOMAIN",
                "disposition_basis": "INDEPENDENT_R235D_FACTOR_RECONSTRUCTION_AND_EXACT_DOMAIN_COVER",
                "C3_graph_definition_blocker_resolved": 1,
                "positive_graph_definition_credit": 0,
                "target_shared_side_incidence_credit": 0,
                "source_shared_side_incidence_credit": 0,
                "representation_pullback_credit": 0,
                "one_sided_trace_credit": 0,
                "R236_codimension_two_disposition_credit": 0,
                "normalized_support_credit": 0,
            }
            core = {
                "schema": ROW_SCHEMA,
                "bridge_ordinal": len(output_rows),
                "bridge_row_id": "round306c4-g2-orphan-disposition:" + objsha([interface, target_graph_id]),
                "Round220_split_interface_id": interface,
                "canonical_input_commitment": input_commitment,
                "canonical_input_commitment_sha256": objsha(input_commitment),
                "semantic_reconstruction": semantic,
                "G2_orphan_graph_disposition": disposition,
                "strict_nonpromotion": {"physical_incidence": 0, "representation_pullback": 0, "one_sided_trace": 0, "R236_codimension_two_disposition": 0, "normalized_support": 0, "representation_cover": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
            }
            core["row_sha256"] = objsha(core)
            output_rows.append(core)

        need(len(output_rows) == 16 and {row["G2_orphan_graph_disposition"]["C3_orphan_target_graph_inventory_row_id"] for row in output_rows} == set(orphan_graph_ids), "orphan disposition exhaustion")
        need(target_sign_hist == {"STRICT_NEGATIVE": 8, "STRICT_POSITIVE": 8}, "target sign histogram")
        need(sum(derivative_sign_hist.values()) == 16 and sum(zero_face_hist.values()) == 16, "semantic histograms")
        ledger_wire, plain = gzip_rows(output_rows)
        ledger = {
            "filename": LEDGER_NAME,
            "compression": "gzip-level9-mtime-zero",
            "row_schema": ROW_SCHEMA,
            "row_count": 16,
            "compressed_size": len(ledger_wire),
            "compressed_sha256": hashlib.sha256(ledger_wire).hexdigest(),
            "uncompressed_size": len(plain),
            "uncompressed_sha256": hashlib.sha256(plain).hexdigest(),
            "ordered_row_ids_sha256": sequence_sha(row["bridge_row_id"] for row in output_rows),
            "ordered_row_hashes_sha256": sequence_sha(row["row_sha256"] for row in output_rows),
            "ordered_rows_sha256": sequence_sha(output_rows),
        }
        body = {
            "schema": SCHEMA,
            "status": STATUS,
            "source_pins": [pin.__dict__ for pin in PINS],
            "upstream_seal_bindings": {"C3_manifest_sha256": pin_by_role["C3_MANIFEST"].sha256, "C0_manifest_sha256": pin_by_role["C0_MANIFEST"].sha256, "R235D_manifest_sha256": pin_by_role["R235D_MANIFEST"].sha256, "B1G0_manifest_sha256": pin_by_role["B1G0_MANIFEST"].sha256},
            "census": {"R235D_authority_rows": 16, "R235_deferred_rows": 16, "R236_double_endpoint_rows": 16, "C3_orphan_target_graph_rows": 16, "complete_parameter_domains": 16, "rational_cover_cells": 64, "source_exact_derivative_rows": 16, "target_empty_rows": 16, "surviving_shared_side_members": 16, "distinct_shared_side_incidence_rows": 32},
            "semantic_effect": {"C3_graph_definition_root_denominator": 38_624, "empty_target_graph_dispositions_sealed": 16, "positive_graph_definition_theorems_still_pending": 38_608, "C3_physical_incidence_relation_denominator_unchanged": 115_440, "C3_representation_pullback_denominator_unchanged": 115_440, "C3_one_sided_trace_denominator_unchanged": 76_832, "R236_codimension_two_dispositions_still_pending": 16, "relation_rows_are_not_member_deduplicated": True},
            "semantic_histograms": {"target_factor_sign": target_sign_hist, "target_p_derivative_sign": derivative_sign_hist, "source_zero_face": zero_face_hist},
            "row_ledger": ledger,
            "scope": {"positive_authority": "16_C3_ORPHAN_TARGET_GRAPH_EMPTY_DISPOSITIONS_ONLY", "source_graph_existence_reconstruction_used_to_isolate_the_remaining_factor": True, "target_graph_positive_existence_credit": 0, "side_incidence_credit": 0, "pullback_credit": 0, "trace_credit": 0, "codimension_two_credit": 0, "normalized_support_credit": 0},
            "required_next": {"G2_positive_graph_definition_theorems": 38_608, "G2_physical_incidence_and_pullback_theorems": 115_440, "G2_one_sided_trace_theorems": 76_832, "R236_codimension_two_dispositions": 16, "B1A": "NOT_AUTHORIZED", "B2": "NOT_AUTHORIZED"},
            "formal_credit": {"C3_orphan_graph_semantic_disposition": 16, "positive_graph_definition": 0, "physical_incidence": 0, "representation_pullback": 0, "one_sided_trace": 0, "R236_codimension_two_disposition": 0, "normalized_support": 0, "representation_cover": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
            "CM2": "NO-GO_FOR_CLAIM",
        }
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
