#!/usr/bin/env python3
"""Independently verify the scoped R235D-to-G2 orphan-graph bridge."""

from __future__ import annotations

import argparse
from collections import defaultdict
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
import shutil
import stat
import sys
import tempfile
from typing import Any, Final, Iterable, Mapping


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise VerificationError(label)


HERE: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge"
RESULT_NAME: Final = PREFIX + "_result.json"
LEDGER_NAME: Final = PREFIX + "_row_ledger.jsonl.gz"
PRODUCER_NAME: Final = PREFIX + "_producer.py"
ATTACK_NAME: Final = PREFIX + "_attack_suite.json"
VERIFICATION_NAME: Final = PREFIX + "_verification.json"
REPORT_NAME: Final = PREFIX + "_report.md"
COLD_NAME: Final = PREFIX + "_cold_replay.md"
MANIFEST_NAME: Final = PREFIX + "_manifest.sha256"
SCHEMA: Final = "cm2.round306c4.source-g-r235d-to-g2-orphan-graph-semantic-bridge.v1"
ROW_SCHEMA: Final = SCHEMA + ".row.v1"
STATUS: Final = "PASS_16_R235D_TO_G2_ORPHAN_TARGET_GRAPH_EMPTY_DISPOSITIONS__ZERO_INCIDENCE_PULLBACK_TRACE_SUPPORT_CREDIT"
OWNER_PATTERN: Final = re.compile(r"^G\[(-?[0-9]+),(-?[0-9]+)\]$")
ROOT_BITS: Final = 128


@dataclass(frozen=True)
class InputPin:
    role: str
    filename: str
    size: int
    sha256: str


SOURCE_PINS: Final = (
    InputPin("C3_MANIFEST", "cm2_round306c3_source_g_corrected_g2_exact_join_filter_manifest.sha256", 956, "f05f172ec8fc25564067539091f77f39bc33395dd5e0232f38bde9c587493761"),
    InputPin("C3_RESULT", "cm2_round306c3_source_g_corrected_g2_exact_join_filter_result.json", 6_458, "66df0b03fdc9f432e330f55eeedc3f49fad0fa2f12fbb6d94689e06a6cc9d8a0"),
    InputPin("C0_MANIFEST", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_manifest.sha256", 2_182, "9ddb6e0ad37b634de8b2edf8573247e7c1263a5c3693c77a7d001241712b25f8"),
    InputPin("C0_INVALID", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_member_invalidation_ledger.jsonl.gz", 11_867, "865185d9b49d4e220459cb083683fd5a074f63eff4f7f2f8217a5c5204991eae"),
    InputPin("R235D_MANIFEST", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_manifest.sha256", 1_276, "0aa2128655e7f90eaeeda47a66901ea45e0908a6f569dc7760ead49ac539e7c0"),
    InputPin("R235D_RESULT", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_result.json", 45_075, "3856a04a5b88574f1ffd6aac7f4fda42c014eac401c2a73efbc6c0ea10c9e5ff"),
    InputPin("R235D_LEDGER", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_row_commitment_ledger.jsonl.gz", 144_211, "6eaeee6a158ad7c0c3d62380214e1ae24ac2a63cb7678b312401cca91cb4cfe0"),
    InputPin("B1G0_MANIFEST", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256", 1_959, "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8"),
    InputPin("B1G0_GRAPH", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz", 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"),
    InputPin("B1G0_SHEET", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),
    InputPin("B1G0_SIDE", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),
    InputPin("R234_CERT", "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    InputPin("R235_CERT", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json", 67_765_471, "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"),
    InputPin("R236_CERT", "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", 2_061_199, "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
)
PRODUCER_PIN: Final = InputPin("PRODUCER", PRODUCER_NAME, 41_872, "f6b99f4377431edc82cd1e164db10a349642676015377c3840900029b14acd55")
ALL_PINS: Final = (*SOURCE_PINS, PRODUCER_PIN)
PACKAGE_MEMBERS: Final = (PRODUCER_NAME, LEDGER_NAME, RESULT_NAME, Path(__file__).name, ATTACK_NAME, VERIFICATION_NAME, REPORT_NAME, COLD_NAME)


def wire(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest_object(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def file_identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def digest_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    state = hashlib.sha256()
    while True:
        chunk = os.read(fd, 1_048_576)
        if not chunk:
            return state.hexdigest()
        state.update(chunk)


class FrozenSources:
    def __init__(self) -> None:
        self.dirfd = -1
        self.fds: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "FrozenSources":
        before = os.stat(HERE, follow_symlinks=False)
        require(stat.S_ISDIR(before.st_mode) and not HERE.is_symlink(), "source directory")
        self.dirfd = os.open(HERE, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for pin in ALL_PINS:
            path_info = os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)
            require(stat.S_ISREG(path_info.st_mode) and path_info.st_nlink == 1 and path_info.st_size == pin.size, "source identity:" + pin.role)
            fd = os.open(pin.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            opened = os.fstat(fd)
            require(file_identity(opened) == file_identity(path_info), "source race:" + pin.role)
            require(digest_fd(fd) == digest_fd(fd) == pin.sha256, "source digest:" + pin.role)
            self.fds[pin.role] = fd
            self.identities[pin.role] = file_identity(opened)
        return self

    def duplicate(self, role: str) -> int:
        fd = os.dup(self.fds[role])
        os.lseek(fd, 0, os.SEEK_SET)
        return fd

    def read(self, role: str) -> bytes:
        fd = self.fds[role]
        os.lseek(fd, 0, os.SEEK_SET)
        pieces: list[bytes] = []
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                return b"".join(pieces)
            pieces.append(chunk)

    def final(self) -> None:
        for pin in reversed(ALL_PINS):
            fd = self.fds[pin.role]
            require(file_identity(os.fstat(fd)) == self.identities[pin.role], "source final fd:" + pin.role)
            require(file_identity(os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.identities[pin.role], "source final path:" + pin.role)
            require(digest_fd(fd) == pin.sha256, "source final digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            os.close(self.dirfd)


def load_direct(sources: FrozenSources, role: str) -> dict[str, Any]:
    raw = sources.read(role)
    value = json.loads(raw)
    require(type(value) is dict and raw in {wire(value), wire(value) + b"\n"}, "direct canonical:" + role)
    if "result_sha256" in value:
        body = dict(value)
        claimed = body.pop("result_sha256")
        require(claimed == digest_object(body) or (set(value) == {"schema", "result", "result_sha256"} and claimed == digest_object(value["result"])), "direct closure:" + role)
    return value


def load_gzip_document(sources: FrozenSources, role: str) -> dict[str, Any]:
    fd = sources.duplicate(role)
    try:
        with os.fdopen(fd, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            value = json.load(stream)
        require(type(value) is dict, "gzip document:" + role)
        return value
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def load_jsonl(sources: FrozenSources, role: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    fd = sources.duplicate(role)
    try:
        with os.fdopen(fd, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            for ordinal, line in enumerate(stream):
                row = json.loads(line)
                require(type(row) is dict and line.endswith(b"\n") and wire(row) + b"\n" == line, "source JSONL:" + role + ":" + str(ordinal))
                rows.append(row)
        return rows
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def read_manifest(sources: FrozenSources, role: str) -> dict[str, str]:
    raw = sources.read(role)
    require(raw.endswith(b"\n"), "manifest newline:" + role)
    entries: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        file_hash, path = line.split("  ")
        filename = os.path.basename(path)
        require(len(file_hash) == 64 and path in {filename, "deliverables/" + filename} and filename not in entries, "manifest row:" + role)
        entries[filename] = file_hash
    return entries


def rational_wire(value: Q | int) -> dict[str, int]:
    rational = Q(value)
    return {"numerator": rational.numerator, "denominator": rational.denominator}


def rational_read(value: Mapping[str, Any]) -> Q:
    require(type(value) is dict and set(value) == {"numerator", "denominator"}, "rational shape")
    numerator, denominator = value["numerator"], value["denominator"]
    require(type(numerator) is int and type(denominator) is int and denominator > 0, "rational scalar")
    rational = Q(numerator, denominator)
    require((rational.numerator, rational.denominator) == (numerator, denominator), "rational reduction")
    return rational


def C(value: Q | int) -> dict[str, Any]:
    return {"op": "CONST_Q", "value": rational_wire(value)}


def V(name: str) -> dict[str, Any]:
    return {"op": "VAR", "name": name}


def N(arg: Any) -> dict[str, Any]:
    return {"op": "NEG", "arg": arg}


def A(*args: Any) -> dict[str, Any]:
    return {"op": "ADD", "args": list(args)}


def S(left: Any, right: Any) -> dict[str, Any]:
    return {"op": "SUB", "left": left, "right": right}


def M(*args: Any) -> dict[str, Any]:
    return {"op": "MUL", "args": list(args)}


def Sq(arg: Any) -> dict[str, Any]:
    return {"op": "SQUARE", "arg": arg}


def Rt(arg: Any) -> dict[str, Any]:
    return {"op": "SQRT_POSITIVE", "arg": arg}


def D(left: Any, right: Any) -> dict[str, Any]:
    return {"op": "DIV_NONZERO", "left": left, "right": right}


def derivative(node: Mapping[str, Any], variable: str) -> dict[str, Any]:
    operation = node["op"]
    if operation == "CONST_Q":
        return C(0)
    if operation == "VAR":
        return C(1 if node["name"] == variable else 0)
    if operation == "NEG":
        return N(derivative(node["arg"], variable))
    if operation == "ADD":
        return A(*(derivative(arg, variable) for arg in node["args"]))
    if operation == "SUB":
        return S(derivative(node["left"], variable), derivative(node["right"], variable))
    if operation == "MUL":
        return A(*(M(*(derivative(arg, variable) if factor_index == derivative_index else arg for factor_index, arg in enumerate(node["args"]))) for derivative_index in range(len(node["args"]))))
    if operation == "SQUARE":
        return M(C(2), node["arg"], derivative(node["arg"], variable))
    if operation == "DIV_NONZERO":
        return D(S(M(derivative(node["left"], variable), node["right"]), M(node["left"], derivative(node["right"], variable))), Sq(node["right"]))
    if operation == "SQRT_POSITIVE":
        return D(derivative(node["arg"], variable), M(C(2), node))
    raise VerificationError("unsupported derivative:" + str(operation))


@dataclass(frozen=True)
class Bounds:
    low: Q
    high: Q

    def __post_init__(self) -> None:
        require(type(self.low) is Q and type(self.high) is Q and self.low <= self.high, "bounds")

    @classmethod
    def singleton(cls, value: Q | int) -> "Bounds":
        rational = Q(value)
        return cls(rational, rational)

    def negative(self) -> "Bounds":
        return Bounds(-self.high, -self.low)

    def plus(self, other: "Bounds") -> "Bounds":
        return Bounds(self.low + other.low, self.high + other.high)

    def minus(self, other: "Bounds") -> "Bounds":
        return self.plus(other.negative())

    def times(self, other: "Bounds") -> "Bounds":
        values = (self.low * other.low, self.low * other.high, self.high * other.low, self.high * other.high)
        return Bounds(min(values), max(values))

    def squared(self) -> "Bounds":
        values = (self.low * self.low, self.high * self.high)
        return Bounds(Q(0) if self.low <= 0 <= self.high else min(values), max(values))

    def divided(self, other: "Bounds") -> "Bounds":
        require(not other.low <= 0 <= other.high, "bounds division")
        inverse = Bounds(min(Q(1, other.low), Q(1, other.high)), max(Q(1, other.low), Q(1, other.high)))
        return self.times(inverse)

    def avoids_zero(self) -> bool:
        return self.high < 0 or self.low > 0

    def encode(self) -> dict[str, Any]:
        return {"lower": rational_wire(self.low), "upper": rational_wire(self.high)}


def root_bounds(value: Bounds) -> Bounds:
    require(value.low > 0, "positive radical")
    scale = 1 << ROOT_BITS

    def floor_root(rational: Q) -> Q:
        return Q(isqrt((rational.numerator * scale * scale) // rational.denominator), scale)

    lower, upper = floor_root(value.low), floor_root(value.high)
    if upper * upper != value.high:
        upper += Q(1, scale)
    require(lower * lower <= value.low and upper * upper >= value.high, "root enclosure")
    return Bounds(lower, upper)


def bound_expression(node: Mapping[str, Any], bindings: Mapping[str, Bounds]) -> Bounds:
    operation = node["op"]
    if operation == "CONST_Q":
        return Bounds.singleton(rational_read(node["value"]))
    if operation == "VAR":
        require(node["name"] in bindings, "expression binding")
        return bindings[node["name"]]
    if operation == "NEG":
        return bound_expression(node["arg"], bindings).negative()
    if operation == "ADD":
        result = Bounds.singleton(0)
        for arg in node["args"]:
            result = result.plus(bound_expression(arg, bindings))
        return result
    if operation == "SUB":
        return bound_expression(node["left"], bindings).minus(bound_expression(node["right"], bindings))
    if operation == "MUL":
        result = Bounds.singleton(1)
        for arg in node["args"]:
            result = result.times(bound_expression(arg, bindings))
        return result
    if operation == "SQUARE":
        return bound_expression(node["arg"], bindings).squared()
    if operation == "DIV_NONZERO":
        return bound_expression(node["left"], bindings).divided(bound_expression(node["right"], bindings))
    if operation == "SQRT_POSITIVE":
        return root_bounds(bound_expression(node["arg"], bindings))
    raise VerificationError("unsupported expression:" + str(operation))


def independently_derive_factors(endpoint: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    reason_kind, axis, wall = endpoint["reason_labels"][0].split(":")
    require(reason_kind == "wall_endpoint_or_count_transition" and axis in {"X", "Y"} and int(wall) == 0, "endpoint event")
    chart = endpoint["chart"]
    require(chart in {"G:E", "G:W", "G:N", "G:S"}, "endpoint chart")
    owner = OWNER_PATTERN.fullmatch(endpoint["owner_target"])
    require(owner is not None, "endpoint owner")
    owner_x, owner_y = Q(int(owner.group(1))), Q(int(owner.group(2)))
    t, p = V("t"), V("p")
    normal_radical = Rt(S(C(1), Sq(t)))
    phase_radical = Rt(S(C(1), Sq(p)))
    direction = chart[-1]
    if direction == "E":
        normal_x, normal_y = normal_radical, t
    elif direction == "W":
        normal_x, normal_y = N(normal_radical), t
    elif direction == "N":
        normal_x, normal_y = t, normal_radical
    else:
        normal_x, normal_y = t, N(normal_radical)
    tangent_x = S(M(phase_radical, normal_x), M(p, normal_y))
    tangent_y = A(M(phase_radical, normal_y), M(p, normal_x))
    radius = Q(9, 25)
    source_x, source_y = M(C(radius), normal_x), M(C(radius), normal_y)
    delta_x, delta_y = S(C(owner_x), source_x), S(C(owner_y), source_y)
    transverse = A(N(M(tangent_y, delta_x)), M(tangent_x, delta_y))
    length = Rt(S(C(radius * radius), Sq(transverse)))
    hit_x = A(C(owner_x), N(M(length, tangent_x)), M(transverse, tangent_y))
    hit_y = A(C(owner_y), N(M(length, tangent_y)), N(M(transverse, tangent_x)))
    source_axis = source_x if axis == "X" else source_y
    target_axis = hit_x if axis == "X" else hit_y
    return S(source_axis, C(0)), S(target_axis, C(0))


def encoded_box(bounds: list[tuple[Q, Q]], closures: list[tuple[bool, bool]]) -> dict[str, Any]:
    return {"wire_id": "RATIONAL_INTERVAL_BOX_V1", "coordinate_parameter": "TPS", "axes": [{"axis": axis, "lower": rational_wire(lower), "lower_closed": lower_closed, "upper": rational_wire(upper), "upper_closed": upper_closed} for axis, (lower, upper), (lower_closed, upper_closed) in zip("tps", bounds, closures, strict=True)]}


def exact_cover(endpoint: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    t0, t1, p0, p1, s0, s1 = map(Q, endpoint["box"])
    tm, pm = (t0 + t1) / 2, (p0 + p1) / 2
    domain = encoded_box([(t0, t1), (p0, p1), (s0, s1)], [(True, True)] * 3)
    cells: list[dict[str, Any]] = []
    for ti, pi in product(range(2), repeat=2):
        tb = (t0, tm) if ti == 0 else (tm, t1)
        pb = (p0, pm) if pi == 0 else (pm, p1)
        cells.append(encoded_box([tb, pb, (s0, s1)], [(True, False) if ti == 0 else (True, True), (True, False) if pi == 0 else (True, True), (True, True)]))
    require(len(cells) == 4, "cover cardinality")
    return domain, cells


def box_bindings(box: dict[str, Any]) -> dict[str, Bounds]:
    return {axis["axis"]: Bounds(rational_read(axis["lower"]), rational_read(axis["upper"])) for axis in box["axes"]}


def ordinary_reference(ordinal: int, row: dict[str, Any], identifier: str) -> list[Any]:
    require(type(row.get(identifier)) is str, "ordinary reference")
    return [ordinal, row[identifier], hashlib.sha256(wire(row)).hexdigest()]


def sealed_reference(ordinal: int, row: dict[str, Any], identifier: str) -> list[Any]:
    require(type(row.get(identifier)) is str and type(row.get("row_sha256")) is str, "sealed reference")
    body = dict(row)
    claimed = body.pop("row_sha256")
    require(claimed == digest_object(body), "sealed row closure")
    return [ordinal, row[identifier], hashlib.sha256(wire(row)).hexdigest(), claimed]


def ordered_sha(values: Iterable[Any]) -> str:
    state = hashlib.sha256()
    state.update(b"[")
    first = True
    for value in values:
        if not first:
            state.update(b",")
        state.update(wire(value))
        first = False
    state.update(b"]")
    return state.hexdigest()


def deterministic_ledger(rows: list[dict[str, Any]]) -> tuple[bytes, bytes]:
    plain = b"".join(wire(row) + b"\n" for row in rows)
    return gzip.compress(plain, compresslevel=9, mtime=0), plain


def unique_index(rows: list[dict[str, Any]], fields: tuple[str, ...], label: str) -> dict[tuple[Any, ...], tuple[int, dict[str, Any]]]:
    result: dict[tuple[Any, ...], tuple[int, dict[str, Any]]] = {}
    for ordinal, row in enumerate(rows):
        key = tuple(row[field] for field in fields)
        require(key not in result, "duplicate index:" + label)
        result[key] = (ordinal, row)
    return result


def rebuild_expected() -> tuple[dict[str, Any], list[dict[str, Any]], bytes]:
    with FrozenSources() as sources:
        pins = {pin.role: pin for pin in SOURCE_PINS}
        for manifest_role, bound_roles in {
            "C3_MANIFEST": ("C3_RESULT",),
            "C0_MANIFEST": ("C0_INVALID",),
            "R235D_MANIFEST": ("R235D_RESULT", "R235D_LEDGER"),
            "B1G0_MANIFEST": ("B1G0_GRAPH", "B1G0_SHEET", "B1G0_SIDE"),
        }.items():
            entries = read_manifest(sources, manifest_role)
            for bound_role in bound_roles:
                pin = pins[bound_role]
                require(entries[pin.filename] == pin.sha256, "upstream manifest binding:" + bound_role)

        c3 = load_direct(sources, "C3_RESULT")
        require(c3["schema"] == "cm2.round306c3.source-g-corrected-g2-exact-join-filter.v1" and c3["result_sha256"] == "6a51130ddc5e2cfcf175abd8b20f0de310353ccf7cd7b7037f86bf5cab24d882", "C3 identity")
        require(c3["corrected_census"] == {"graph_definition_rows": 38_624, "G2A_sheet_members": 38_608, "G2B_side_references": 76_832, "G2B_side_distinct_members": 76_816, "duplicate_side_reference_excess": 16, "physical_incidence_relations": 115_440, "semantic_obligation_rows": 154_064}, "C3 relational census")
        require(c3["formal_blockers"]["source_graph_definition_theorems_pending"] == 38_624, "C3 blocker census")

        r235d_result = load_direct(sources, "R235D_RESULT")
        require(r235d_result["schema"] == "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.result.v1", "R235D result schema")
        require(r235d_result["result"]["authority_ledger"]["sha256"] == pins["R235D_LEDGER"].sha256 and r235d_result["result"]["authority_ledger"]["row_count"] == 16, "R235D result binding")
        authority_rows = load_jsonl(sources, "R235D_LEDGER")
        require(len(authority_rows) == 16 and [row["authority_ordinal"] for row in authority_rows] == list(range(16)), "R235D authority census")
        invalid_rows = load_jsonl(sources, "C0_INVALID")
        invalid = {row["registry_member_id"] for row in invalid_rows}
        require(len(invalid_rows) == len(invalid) == 32, "invalid member census")

        r234_rows = load_direct(sources, "R234_CERT")["result"]["depth6_frontier_rows"]
        r234_index = {row["frontier_row_id"]: (ordinal, row) for ordinal, row in enumerate(r234_rows)}
        require(len(r234_index) == len(r234_rows), "R234 unique rows")
        r235_deferred = load_direct(sources, "R235_CERT")["result"]["double_endpoint_deferred_rows"]
        deferred_ids = {row["Round234_frontier_row_id"] for row in r235_deferred}
        require(len(r235_deferred) == len(deferred_ids) == 16, "R235 deferred")
        r236_rows = load_direct(sources, "R236_CERT")["result"]["double_endpoint_partition_rows"]
        r236_tuple_index = unique_index(r236_rows, ("Round220_split_interface_id",), "R236")
        r236_by_interface = {key[0]: value for key, value in r236_tuple_index.items()}
        require(len(r236_rows) == len(r236_by_interface) == 16, "R236 double rows")

        all_sheets = load_gzip_document(sources, "B1G0_SHEET")["graph_sheet_join_rows"]
        surviving_sheet_graphs = {row["graph_source_inventory_row_id"] for row in all_sheets if row["sheet_member_id"] not in invalid}
        r236_sheets = [(ordinal, row) for ordinal, row in enumerate(all_sheets) if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH"]
        sheet_index = {(row["Round220_split_interface_id"], row["endpoint_factor"]): (ordinal, row) for ordinal, row in r236_sheets}
        require(len(r236_sheets) == len(sheet_index) == 32, "R236 sheets")

        all_sides = load_gzip_document(sources, "B1G0_SIDE")["graph_side_join_rows"]
        surviving_sides = [row for row in all_sides if row["side_member_id"] not in invalid]
        surviving_side_graphs = {row["graph_source_inventory_row_id"] for row in surviving_sides}
        orphan_graph_ids = sorted(surviving_side_graphs - surviving_sheet_graphs)
        r236_sides = [(ordinal, row) for ordinal, row in enumerate(all_sides) if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH"]
        sides_by_interface: dict[str, dict[str, tuple[int, dict[str, Any]]]] = defaultdict(dict)
        for ordinal, row in r236_sides:
            role = row["side_role"]
            require(role not in sides_by_interface[row["Round220_split_interface_id"]], "R236 side role uniqueness")
            sides_by_interface[row["Round220_split_interface_id"]][role] = (ordinal, row)
        require(len(r236_sides) == 64 and len(orphan_graph_ids) == 16, "R236 sides and orphans")

        all_graphs = load_gzip_document(sources, "B1G0_GRAPH")["graph_source_inventory_rows"]
        r236_graphs = [(ordinal, row) for ordinal, row in enumerate(all_graphs) if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH"]
        graph_index = {(row["Round220_split_interface_id"], row["endpoint_factor"]): (ordinal, row) for ordinal, row in r236_graphs}
        require(len(r236_graphs) == len(graph_index) == 32, "R236 graph roots")

        authority_by_interface: dict[str, tuple[int, dict[str, Any]]] = {}
        for ordinal, row in enumerate(authority_rows):
            interface = row["canonical_input_commitment"]["R220_interface"][1]
            require(interface not in authority_by_interface, "R235D interface uniqueness")
            authority_by_interface[interface] = (ordinal, row)
        require(set(authority_by_interface) == set(r236_by_interface), "R235D/R236 exhaustion")
        require({row["Round234_frontier_row_id"] for row in authority_rows} == deferred_ids, "R235D/R235 exhaustion")

        rebuilt_rows: list[dict[str, Any]] = []
        target_histogram: dict[str, int] = {}
        derivative_histogram: dict[str, int] = {}
        face_histogram: dict[str, int] = {}
        for interface in sorted(authority_by_interface):
            authority_ordinal, authority = authority_by_interface[interface]
            frontier_ordinal, endpoint = r234_index[authority["Round234_frontier_row_id"]]
            r236_ordinal, r236 = r236_by_interface[interface]
            require(r236["Round234_frontier_row_id"] == endpoint["frontier_row_id"] and r236["double_endpoint_partition_row_id"] == authority["downstream_invalidation"]["R236_double_endpoint_partition_row"][1], "R236 semantic join")
            source_factor, target_factor = independently_derive_factors(endpoint)
            source_derivative = derivative(source_factor, "t")
            target_derivative = derivative(target_factor, "p")
            domain, cells = exact_cover(endpoint)
            source_bounds = bound_expression(source_derivative, box_bindings(domain))
            require(source_bounds == Bounds.singleton(Q(9, 25)), "source derivative theorem")
            t0, t1 = map(Q, endpoint["box"][:2])
            require((t0 == 0) ^ (t1 == 0), "source face")
            zero_face = "LOWER" if t0 == 0 else "UPPER"
            face_histogram[zero_face] = face_histogram.get(zero_face, 0) + 1
            receipts: list[dict[str, Any]] = []
            for cell_index, cell in enumerate(cells):
                bindings = box_bindings(cell)
                target_bounds = bound_expression(target_factor, bindings)
                derivative_bounds = bound_expression(target_derivative, bindings)
                require(target_bounds.avoids_zero() and derivative_bounds.avoids_zero(), "target empty theorem")
                target_sign = "STRICT_POSITIVE" if target_bounds.low > 0 else "STRICT_NEGATIVE"
                derivative_sign = "STRICT_POSITIVE" if derivative_bounds.low > 0 else "STRICT_NEGATIVE"
                receipts.append({"cell_index": cell_index, "cell": cell, "target_factor_interval": target_bounds.encode(), "target_factor_sign": target_sign, "target_p_derivative_interval": derivative_bounds.encode(), "target_p_derivative_sign": derivative_sign})
            target_signs = {receipt["target_factor_sign"] for receipt in receipts}
            derivative_signs = {receipt["target_p_derivative_sign"] for receipt in receipts}
            require(len(target_signs) == len(derivative_signs) == 1, "uniform signs")
            target_sign = next(iter(target_signs))
            derivative_sign = next(iter(derivative_signs))
            target_histogram[target_sign] = target_histogram.get(target_sign, 0) + 1
            derivative_histogram[derivative_sign] = derivative_histogram.get(derivative_sign, 0) + 1

            prior_theorem = authority["local_theorem"]
            require(prior_theorem["source_factor_ast"] == source_factor and prior_theorem["source_t_derivative_ast"] == source_derivative, "R235D source reconstruction")
            require(prior_theorem["target_factor_ast"] == target_factor and prior_theorem["target_p_derivative_ast"] == target_derivative, "R235D target reconstruction")
            require(prior_theorem["source_t_derivative_exact_interval"] == source_bounds.encode() and prior_theorem["source_zero_face"] == zero_face, "R235D source binding")
            prior_cover = {"domain_box": domain, "cell_count": 4, "cells": [{"cell_index": receipt["cell_index"], "cell": receipt["cell"], "excluded_factor": "TARGET", "target_factor_interval": receipt["target_factor_interval"], "target_factor_sign": receipt["target_factor_sign"], "target_p_derivative_interval": receipt["target_p_derivative_interval"], "target_p_derivative_sign": receipt["target_p_derivative_sign"]} for receipt in receipts]}
            require(prior_theorem["rational_cover"] == prior_cover, "R235D cover binding")
            require(prior_theorem["source_zero_set"] == "EXACT_FACE_GRAPH_t_EQUALS_0" and prior_theorem["source_graph_dimension"] == 2 and prior_theorem["target_zero_set_on_domain"] == "EMPTY" and prior_theorem["source_target_codim2_intersection"] == "EMPTY", "R235D theorem scope")
            require(prior_theorem["target_factor_fixed_sign"] == target_sign and prior_theorem["target_p_derivative_fixed_sign"] == derivative_sign, "R235D signs")
            require(authority["local_source_only_endpoint_graph_key_authority_credit"] == 1 and authority["G2_authority_credit"] == authority["physical_incidence_equivalence_credit"] == authority["representation_pullback_credit"] == 0, "R235D nonpromotion")

            target_graph = graph_index[(interface, "target")]
            source_graph = graph_index[(interface, "source")]
            target_sheet = sheet_index[(interface, "target")]
            source_sheet = sheet_index[(interface, "source")]
            role_rows = sides_by_interface[interface]
            require(set(role_rows) == {"target:SAME_SIGN_EVENT_ABSENT", "target:POSITIVE_TO_NEGATIVE", "source:SAME_SIGN_EVENT_ABSENT", "source:NEGATIVE_TO_POSITIVE"}, "side role exhaustion")
            target_shared = role_rows["target:SAME_SIGN_EVENT_ABSENT"]
            target_only = role_rows["target:POSITIVE_TO_NEGATIVE"]
            source_shared = role_rows["source:SAME_SIGN_EVENT_ABSENT"]
            source_only = role_rows["source:NEGATIVE_TO_POSITIVE"]
            target_inventory_id = target_graph[1]["Round306B1G0_graph_source_inventory_row_id"]
            require(target_inventory_id in orphan_graph_ids and target_inventory_id == authority["downstream_invalidation"]["B1G0_invalid_target_graph_inventory_row"][1], "orphan graph join")
            require(target_graph[1]["source_row_id"] == source_graph[1]["source_row_id"] == r236["double_endpoint_partition_row_id"], "graph source join")
            require(target_sheet[1]["sheet_member_id"] in invalid and source_sheet[1]["sheet_member_id"] not in invalid, "sheet validity")
            require(target_only[1]["side_member_id"] in invalid and source_only[1]["side_member_id"] not in invalid, "side validity")
            require(target_shared[1]["side_member_id"] == source_shared[1]["side_member_id"] and target_shared[1]["side_member_id"] not in invalid, "shared side identity")
            require(target_shared[1]["graph_source_inventory_row_id"] == target_inventory_id and source_shared[1]["graph_source_inventory_row_id"] == source_graph[1]["Round306B1G0_graph_source_inventory_row_id"], "shared side graph identity")
            require(target_shared[1]["Round306B1G0_graph_side_join_row_id"] != source_shared[1]["Round306B1G0_graph_side_join_row_id"], "shared side relation identity")
            downstream = authority["downstream_invalidation"]
            require(downstream["B1G0_target_sheet_join_row"][1] == target_sheet[1]["Round306B1G0_graph_sheet_join_row_id"], "target sheet backbinding")
            require(downstream["B1G0_target_shared_side_row"][1] == target_shared[1]["Round306B1G0_graph_side_join_row_id"], "target shared backbinding")
            require(downstream["B1G0_source_shared_side_row"][1] == source_shared[1]["Round306B1G0_graph_side_join_row_id"], "source shared backbinding")
            require(downstream["B1G0_target_only_side_row"][1] == target_only[1]["Round306B1G0_graph_side_join_row_id"], "target only backbinding")

            inputs = {
                "R235D_authority_row": ordinary_reference(authority_ordinal, authority, "authority_row_id"),
                "R234_frontier_row": ordinary_reference(frontier_ordinal, endpoint, "frontier_row_id"),
                "R236_double_endpoint_partition_row": ordinary_reference(r236_ordinal, r236, "double_endpoint_partition_row_id"),
                "B1G0_target_graph_row": sealed_reference(*target_graph, "Round306B1G0_graph_source_inventory_row_id"),
                "B1G0_source_graph_row": sealed_reference(*source_graph, "Round306B1G0_graph_source_inventory_row_id"),
                "B1G0_target_sheet_row": sealed_reference(*target_sheet, "Round306B1G0_graph_sheet_join_row_id"),
                "B1G0_source_sheet_row": sealed_reference(*source_sheet, "Round306B1G0_graph_sheet_join_row_id"),
                "B1G0_target_shared_side_row": sealed_reference(*target_shared, "Round306B1G0_graph_side_join_row_id"),
                "B1G0_source_shared_side_row": sealed_reference(*source_shared, "Round306B1G0_graph_side_join_row_id"),
                "B1G0_target_only_side_row": sealed_reference(*target_only, "Round306B1G0_graph_side_join_row_id"),
                "B1G0_source_only_side_row": sealed_reference(*source_only, "Round306B1G0_graph_side_join_row_id"),
            }
            semantics = {
                "complete_parameter_domain": domain,
                "complete_domain_partition_kind": "EXACT_2_BY_2_TP_HALF_OPEN_PARTITION_WITH_FULL_S_INTERVAL",
                "complete_domain_partition_cell_count": 4,
                "complete_domain_partition_verified": True,
                "source_factor_ast": source_factor,
                "source_t_derivative_ast": source_derivative,
                "source_t_derivative_exact_interval": source_bounds.encode(),
                "source_zero_face": zero_face,
                "source_zero_set": "EXACT_FACE_GRAPH_t_EQUALS_0",
                "source_graph_dimension": 2,
                "target_factor_ast": target_factor,
                "target_p_derivative_ast": target_derivative,
                "target_factor_fixed_sign": target_sign,
                "target_p_derivative_fixed_sign": derivative_sign,
                "target_zero_set_on_complete_domain": "EMPTY",
                "source_target_codimension_two_intersection": "EMPTY",
                "cell_receipts": receipts,
            }
            disposition = {
                "C3_orphan_target_graph_inventory_row_id": target_inventory_id,
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
                "bridge_ordinal": len(rebuilt_rows),
                "bridge_row_id": "round306c4-g2-orphan-disposition:" + digest_object([interface, target_inventory_id]),
                "Round220_split_interface_id": interface,
                "canonical_input_commitment": inputs,
                "canonical_input_commitment_sha256": digest_object(inputs),
                "semantic_reconstruction": semantics,
                "G2_orphan_graph_disposition": disposition,
                "strict_nonpromotion": {"physical_incidence": 0, "representation_pullback": 0, "one_sided_trace": 0, "R236_codimension_two_disposition": 0, "normalized_support": 0, "representation_cover": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
            }
            core["row_sha256"] = digest_object(core)
            rebuilt_rows.append(core)

        require(len(rebuilt_rows) == 16 and {row["G2_orphan_graph_disposition"]["C3_orphan_target_graph_inventory_row_id"] for row in rebuilt_rows} == set(orphan_graph_ids), "orphan disposition exhaustion")
        require(target_histogram == {"STRICT_NEGATIVE": 8, "STRICT_POSITIVE": 8}, "target sign histogram")
        require(sum(derivative_histogram.values()) == sum(face_histogram.values()) == 16, "semantic histogram totals")
        ledger_wire, plain = deterministic_ledger(rebuilt_rows)
        ledger = {"filename": LEDGER_NAME, "compression": "gzip-level9-mtime-zero", "row_schema": ROW_SCHEMA, "row_count": 16, "compressed_size": len(ledger_wire), "compressed_sha256": hashlib.sha256(ledger_wire).hexdigest(), "uncompressed_size": len(plain), "uncompressed_sha256": hashlib.sha256(plain).hexdigest(), "ordered_row_ids_sha256": ordered_sha(row["bridge_row_id"] for row in rebuilt_rows), "ordered_row_hashes_sha256": ordered_sha(row["row_sha256"] for row in rebuilt_rows), "ordered_rows_sha256": ordered_sha(rebuilt_rows)}
        body = {
            "schema": SCHEMA,
            "status": STATUS,
            "source_pins": [pin.__dict__ for pin in SOURCE_PINS],
            "upstream_seal_bindings": {"C3_manifest_sha256": pins["C3_MANIFEST"].sha256, "C0_manifest_sha256": pins["C0_MANIFEST"].sha256, "R235D_manifest_sha256": pins["R235D_MANIFEST"].sha256, "B1G0_manifest_sha256": pins["B1G0_MANIFEST"].sha256},
            "census": {"R235D_authority_rows": 16, "R235_deferred_rows": 16, "R236_double_endpoint_rows": 16, "C3_orphan_target_graph_rows": 16, "complete_parameter_domains": 16, "rational_cover_cells": 64, "source_exact_derivative_rows": 16, "target_empty_rows": 16, "surviving_shared_side_members": 16, "distinct_shared_side_incidence_rows": 32},
            "semantic_effect": {"C3_graph_definition_root_denominator": 38_624, "empty_target_graph_dispositions_sealed": 16, "positive_graph_definition_theorems_still_pending": 38_608, "C3_physical_incidence_relation_denominator_unchanged": 115_440, "C3_representation_pullback_denominator_unchanged": 115_440, "C3_one_sided_trace_denominator_unchanged": 76_832, "R236_codimension_two_dispositions_still_pending": 16, "relation_rows_are_not_member_deduplicated": True},
            "semantic_histograms": {"target_factor_sign": target_histogram, "target_p_derivative_sign": derivative_histogram, "source_zero_face": face_histogram},
            "row_ledger": ledger,
            "scope": {"positive_authority": "16_C3_ORPHAN_TARGET_GRAPH_EMPTY_DISPOSITIONS_ONLY", "source_graph_existence_reconstruction_used_to_isolate_the_remaining_factor": True, "target_graph_positive_existence_credit": 0, "side_incidence_credit": 0, "pullback_credit": 0, "trace_credit": 0, "codimension_two_credit": 0, "normalized_support_credit": 0},
            "required_next": {"G2_positive_graph_definition_theorems": 38_608, "G2_physical_incidence_and_pullback_theorems": 115_440, "G2_one_sided_trace_theorems": 76_832, "R236_codimension_two_dispositions": 16, "B1A": "NOT_AUTHORIZED", "B2": "NOT_AUTHORIZED"},
            "formal_credit": {"C3_orphan_graph_semantic_disposition": 16, "positive_graph_definition": 0, "physical_incidence": 0, "representation_pullback": 0, "one_sided_trace": 0, "R236_codimension_two_disposition": 0, "normalized_support": 0, "representation_cover": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
            "CM2": "NO-GO_FOR_CLAIM",
        }
        expected_result = {**body, "result_sha256": digest_object(body)}
        sources.final()
        return expected_result, rebuilt_rows, ledger_wire


class CandidateFiles:
    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.dirfd = -1
        self.fds: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}
        self.raw: dict[str, bytes] = {}

    def __enter__(self) -> "CandidateFiles":
        resolved = self.directory.resolve()
        require(os.path.commonpath((str(resolved), str(HERE.resolve()))) != str(HERE.resolve()), "candidate outside deliverables")
        info = os.stat(resolved, follow_symlinks=False)
        require(stat.S_ISDIR(info.st_mode) and set(os.listdir(resolved)) == {RESULT_NAME, LEDGER_NAME}, "candidate exact set")
        self.dirfd = os.open(resolved, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for filename in (LEDGER_NAME, RESULT_NAME):
            before = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "candidate identity:" + filename)
            fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            opened = os.fstat(fd)
            require(file_identity(opened) == file_identity(before), "candidate race:" + filename)
            first = digest_fd(fd)
            require(first == digest_fd(fd), "candidate digest stability:" + filename)
            os.lseek(fd, 0, os.SEEK_SET)
            raw = os.read(fd, before.st_size)
            require(len(raw) == before.st_size, "candidate read:" + filename)
            self.fds[filename] = fd
            self.identities[filename] = file_identity(opened)
            self.raw[filename] = raw
        return self

    def final(self) -> None:
        for filename in (RESULT_NAME, LEDGER_NAME):
            fd = self.fds[filename]
            require(file_identity(os.fstat(fd)) == self.identities[filename], "candidate final fd:" + filename)
            require(file_identity(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.identities[filename], "candidate final path:" + filename)
            require(digest_fd(fd) == hashlib.sha256(self.raw[filename]).hexdigest(), "candidate final digest:" + filename)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            os.close(self.dirfd)


def decode_candidate(result_raw: bytes, ledger_raw: bytes) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    result = json.loads(result_raw)
    require(type(result) is dict and wire(result) == result_raw, "candidate result canonical")
    body = dict(result)
    require(body.pop("result_sha256", None) == digest_object(body), "candidate result closure")
    try:
        plain = gzip.decompress(ledger_raw)
    except (OSError, EOFError) as error:
        raise VerificationError("candidate ledger gzip") from error
    require(gzip.compress(plain, compresslevel=9, mtime=0) == ledger_raw and plain.endswith(b"\n"), "candidate ledger deterministic")
    rows: list[dict[str, Any]] = []
    for ordinal, line in enumerate(plain.splitlines()):
        row = json.loads(line)
        require(type(row) is dict and wire(row) == line, "candidate row canonical:" + str(ordinal))
        row_body = dict(row)
        require(row_body.pop("row_sha256", None) == digest_object(row_body), "candidate row closure:" + str(ordinal))
        require(row["bridge_ordinal"] == ordinal and row["schema"] == ROW_SCHEMA, "candidate row identity:" + str(ordinal))
        rows.append(row)
    require(len(rows) == 16, "candidate row census")
    return result, rows


def replay_payloads(result_raw: bytes, ledger_raw: bytes) -> dict[str, Any]:
    candidate_result, candidate_rows = decode_candidate(result_raw, ledger_raw)
    expected_result, expected_rows, expected_ledger = rebuild_expected()
    require(candidate_rows == expected_rows and ledger_raw == expected_ledger, "candidate ledger exact comparator")
    require(candidate_result == expected_result and result_raw == wire(expected_result), "candidate result exact comparator")
    return {"status": "PASS_INDEPENDENT_16_ROW_R235D_TO_G2_ORPHAN_GRAPH_SEMANTIC_REPLAY__ZERO_INCIDENCE_PULLBACK_TRACE_SUPPORT_CREDIT", "candidate_result_file_sha256": hashlib.sha256(result_raw).hexdigest(), "candidate_ledger_file_sha256": hashlib.sha256(ledger_raw).hexdigest(), "result_sha256": candidate_result["result_sha256"], "row_count": 16, "rational_cover_cell_count": 64, "empty_target_graph_disposition_count": 16, "positive_graph_definition_theorems_still_pending": 38_608, "physical_incidence_relations_still_pending": 115_440, "producer_imported_or_executed": False, "formal_credit": candidate_result["formal_credit"], "CM2": "NO-GO_FOR_CLAIM"}


def replay_directory(directory: Path) -> tuple[dict[str, Any], dict[str, bytes]]:
    with CandidateFiles(directory) as candidate:
        receipt = replay_payloads(candidate.raw[RESULT_NAME], candidate.raw[LEDGER_NAME])
        candidate.final()
        return receipt, dict(candidate.raw)


def verifier_sha256() -> str:
    path = Path(__file__)
    before = os.stat(path, follow_symlinks=False)
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "verifier identity")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        require(file_identity(os.fstat(fd)) == file_identity(before), "verifier race")
        value = digest_fd(fd)
        require(value == digest_fd(fd), "verifier digest stability")
        return value
    finally:
        os.close(fd)


def publish_bytes(filename: str, raw: bytes, mode: int = 0o600) -> None:
    path = HERE / filename
    require(not path.exists(), "publish no-clobber:" + filename)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, mode)
    try:
        offset = 0
        while offset < len(raw):
            offset += os.write(fd, raw[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)
    info = os.stat(path, follow_symlinks=False)
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == len(raw), "published identity:" + filename)


def promote(directory: Path) -> dict[str, Any]:
    with CandidateFiles(directory) as candidate:
        receipt = replay_payloads(candidate.raw[RESULT_NAME], candidate.raw[LEDGER_NAME])
        publish_bytes(LEDGER_NAME, candidate.raw[LEDGER_NAME])
        publish_bytes(RESULT_NAME, candidate.raw[RESULT_NAME])
        candidate.final()
    for filename, raw in ((RESULT_NAME, candidate.raw[RESULT_NAME]), (LEDGER_NAME, candidate.raw[LEDGER_NAME])):
        info = os.stat(HERE / filename, follow_symlinks=False)
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and hashlib.sha256((HERE / filename).read_bytes()).hexdigest() == hashlib.sha256(raw).hexdigest(), "promoted reverse verification:" + filename)
    return {**receipt, "status": "PASS_CANDIDATE_PROMOTED_LEDGER_FIRST_RESULT_LAST_WITH_REVERSE_IDENTITY_NLINK_SHA256_VERIFICATION"}


def mutate_result(path: Path, mutation: Any) -> None:
    value = json.loads(path.read_bytes())
    mutation(value)
    body = dict(value)
    body.pop("result_sha256", None)
    value = {**body, "result_sha256": digest_object(body)}
    path.write_bytes(wire(value))


def mutate_ledger(directory: Path, mutation: Any) -> None:
    ledger_path = directory / LEDGER_NAME
    plain = gzip.decompress(ledger_path.read_bytes())
    rows = [json.loads(line) for line in plain.splitlines()]
    mutation(rows)
    for ordinal, row in enumerate(rows):
        row["bridge_ordinal"] = ordinal
        body = dict(row)
        body.pop("row_sha256", None)
        row["row_sha256"] = digest_object(body)
    ledger_raw, plain = deterministic_ledger(rows)
    ledger_path.write_bytes(ledger_raw)
    result_path = directory / RESULT_NAME
    result = json.loads(result_path.read_bytes())
    result["row_ledger"] = {"filename": LEDGER_NAME, "compression": "gzip-level9-mtime-zero", "row_schema": ROW_SCHEMA, "row_count": len(rows), "compressed_size": len(ledger_raw), "compressed_sha256": hashlib.sha256(ledger_raw).hexdigest(), "uncompressed_size": len(plain), "uncompressed_sha256": hashlib.sha256(plain).hexdigest(), "ordered_row_ids_sha256": ordered_sha(row["bridge_row_id"] for row in rows), "ordered_row_hashes_sha256": ordered_sha(row["row_sha256"] for row in rows), "ordered_rows_sha256": ordered_sha(rows)}
    body = dict(result)
    body.pop("result_sha256", None)
    result["result_sha256"] = digest_object(body)
    result_path.write_bytes(wire(result))


def coherent_attacks(candidate_directory: Path) -> dict[str, Any]:
    baseline, _ = replay_directory(candidate_directory)
    work = Path(tempfile.mkdtemp(prefix="cm2-c4-g2-bridge-attacks-"))
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
            replay_directory(work)
        except (VerificationError, OSError, json.JSONDecodeError, KeyError, ValueError) as error:
            rejection = type(error).__name__ + ":" + str(error)
        finally:
            if cleanup is not None:
                cleanup()
        require(rejection is not None, "attack accepted:" + attack_id)
        body = {"attack_id": attack_id, "rejected": True, "rejection_boundary": rejection}
        attacks.append({**body, "row_sha256": digest_object(body)})

    try:
        execute("A01_EXTRA_FILE", lambda: (work / "foreign").write_bytes(b"x"), lambda: (work / "foreign").unlink(missing_ok=True))
        execute("A02_MISSING_RESULT", lambda: (work / RESULT_NAME).unlink())
        execute("A03_MISSING_LEDGER", lambda: (work / LEDGER_NAME).unlink())
        execute("A04_SYMLINK_RESULT", lambda: ((work / RESULT_NAME).unlink(), (work / RESULT_NAME).symlink_to(candidate_directory / RESULT_NAME)))
        hard_target = work.parent / (work.name + "-hard-target")
        def hardlink_ledger() -> None:
            (work / LEDGER_NAME).unlink()
            shutil.copyfile(candidate_directory / LEDGER_NAME, hard_target)
            os.link(hard_target, work / LEDGER_NAME)
        execute("A05_HARDLINK_LEDGER", hardlink_ledger, lambda: hard_target.unlink(missing_ok=True))
        execute("A06_POSITIVE_GRAPH_CREDIT", lambda: mutate_ledger(work, lambda rows: rows[0]["G2_orphan_graph_disposition"].__setitem__("positive_graph_definition_credit", 1)))
        execute("A07_INCIDENCE_CREDIT", lambda: mutate_ledger(work, lambda rows: rows[0]["G2_orphan_graph_disposition"].__setitem__("target_shared_side_incidence_credit", 1)))
        execute("A08_PULLBACK_CREDIT", lambda: mutate_ledger(work, lambda rows: rows[0]["G2_orphan_graph_disposition"].__setitem__("representation_pullback_credit", 1)))
        execute("A09_DOMAIN_CELL_MUTATION", lambda: mutate_ledger(work, lambda rows: rows[0]["semantic_reconstruction"]["cell_receipts"][0]["cell"]["axes"][0].__setitem__("upper_closed", True)))
        execute("A10_TARGET_SIGN_MUTATION", lambda: mutate_ledger(work, lambda rows: rows[0]["semantic_reconstruction"].__setitem__("target_factor_fixed_sign", "STRICT_POSITIVE" if rows[0]["semantic_reconstruction"]["target_factor_fixed_sign"] == "STRICT_NEGATIVE" else "STRICT_NEGATIVE")))
        execute("A11_DROP_ROW", lambda: mutate_ledger(work, lambda rows: rows.pop()))
        execute("A12_DUPLICATE_ROW", lambda: mutate_ledger(work, lambda rows: rows.append(dict(rows[-1]))))
        execute("A13_OLD_GRAPH_DENOMINATOR", lambda: mutate_result(work / RESULT_NAME, lambda value: value["semantic_effect"].__setitem__("positive_graph_definition_theorems_still_pending", 38_624)))
        execute("A14_DEDUP_INCIDENCE_DENOMINATOR", lambda: mutate_result(work / RESULT_NAME, lambda value: value["semantic_effect"].__setitem__("C3_physical_incidence_relation_denominator_unchanged", 115_424)))
        execute("A15_SOURCE_PIN_SUBSTITUTION", lambda: mutate_result(work / RESULT_NAME, lambda value: value["source_pins"][0].__setitem__("sha256", "0" * 64)))
        execute("A16_NORMALIZED_SUPPORT_INJECTION", lambda: mutate_result(work / RESULT_NAME, lambda value: value["formal_credit"].__setitem__("normalized_support", 1)))
        execute("A17_CODIM2_INJECTION", lambda: mutate_result(work / RESULT_NAME, lambda value: value["formal_credit"].__setitem__("R236_codimension_two_disposition", 16)))
        execute("A18_NONCANONICAL_RESULT", lambda: (work / RESULT_NAME).write_bytes((work / RESULT_NAME).read_bytes() + b"\n"))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    require(len(attacks) == 18, "attack census")
    body = {"schema": SCHEMA + ".coherent-attack-suite.v1", "status": "PASS_18_OF_18_COHERENT_ATTACKS_REJECTED", "verifier_filename": Path(__file__).name, "verifier_file_sha256": verifier_sha256(), "attack_count": 18, "rejected_count": 18, "all_rejected": True, "baseline_result_file_sha256": baseline["candidate_result_file_sha256"], "baseline_ledger_file_sha256": baseline["candidate_ledger_file_sha256"], "attacks": attacks}
    return {**body, "attack_suite_sha256": digest_object(body)}


def closed_json(raw: bytes, closure: str, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    require(type(value) is dict and wire(value) == raw, "closed JSON canonical:" + label)
    body = dict(value)
    require(body.pop(closure, None) == digest_object(body), "closed JSON closure:" + label)
    return value


def verification_document(receipt: dict[str, Any], attack_raw: bytes | None = None) -> dict[str, Any]:
    raw = (HERE / ATTACK_NAME).read_bytes() if attack_raw is None else attack_raw
    suite = closed_json(raw, "attack_suite_sha256", "attack suite")
    require(suite["verifier_file_sha256"] == verifier_sha256() and (suite["attack_count"], suite["rejected_count"], suite["all_rejected"]) == (18, 18, True), "attack suite binding")
    body = {"schema": SCHEMA + ".verification.v1", **receipt, "attack_suite": {"filename": ATTACK_NAME, "file_sha256": hashlib.sha256(raw).hexdigest(), "object_self_sha256": suite["attack_suite_sha256"], "attack_count": 18, "rejected_count": 18, "all_rejected": True}, "formal_credit_marker": {"C3_orphan_graph_semantic_disposition": 16, "normalized_support": 0, "B1A": 0, "B2": 0, "CM2": 0}}
    return {**body, "verification_sha256": digest_object(body)}


class ManifestPackage:
    def __init__(self) -> None:
        self.dirfd = -1
        self.manifest_fd = -1
        self.manifest_identity: tuple[int, ...] = ()
        self.fds: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}
        self.hashes: dict[str, str] = {}

    def __enter__(self) -> "ManifestPackage":
        self.dirfd = os.open(HERE, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        before = os.stat(MANIFEST_NAME, dir_fd=self.dirfd, follow_symlinks=False)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "manifest identity")
        self.manifest_fd = os.open(MANIFEST_NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
        opened = os.fstat(self.manifest_fd)
        require(file_identity(opened) == file_identity(before), "manifest race")
        self.manifest_identity = file_identity(opened)
        os.lseek(self.manifest_fd, 0, os.SEEK_SET)
        raw = os.read(self.manifest_fd, before.st_size)
        lines = raw.decode("ascii").splitlines()
        require(raw.endswith(b"\n") and len(lines) == len(PACKAGE_MEMBERS), "manifest structure")
        for line, filename in zip(lines, PACKAGE_MEMBERS, strict=True):
            declared_hash, declared_name = line.split("  ")
            require(declared_name == filename and len(declared_hash) == 64, "manifest order:" + filename)
            info = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "manifest member identity:" + filename)
            fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            member = os.fstat(fd)
            require(file_identity(member) == file_identity(info) and digest_fd(fd) == digest_fd(fd) == declared_hash, "manifest member digest:" + filename)
            self.fds[filename] = fd
            self.identities[filename] = file_identity(member)
            self.hashes[filename] = declared_hash
        return self

    def read(self, filename: str) -> bytes:
        fd = self.fds[filename]
        os.lseek(fd, 0, os.SEEK_SET)
        return os.read(fd, self.identities[filename][4])

    def final(self) -> None:
        for filename in reversed(PACKAGE_MEMBERS):
            require(file_identity(os.fstat(self.fds[filename])) == self.identities[filename], "manifest final fd:" + filename)
            require(file_identity(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.identities[filename], "manifest final path:" + filename)
            require(digest_fd(self.fds[filename]) == self.hashes[filename], "manifest final digest:" + filename)
        require(file_identity(os.fstat(self.manifest_fd)) == self.manifest_identity and file_identity(os.stat(MANIFEST_NAME, dir_fd=self.dirfd, follow_symlinks=False)) == self.manifest_identity, "manifest final identity")

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
        require(package.hashes[Path(__file__).name] == verifier_sha256(), "manifest verifier binding")
        receipt = replay_payloads(package.read(RESULT_NAME), package.read(LEDGER_NAME))
        require(package.read(VERIFICATION_NAME) == wire(verification_document(receipt, package.read(ATTACK_NAME))), "manifest verification byte identity")
        package.final()
    return {"status": "PASS_MANIFEST_FIRST_HELD_FD_16_ROW_R235D_TO_G2_ORPHAN_GRAPH_SEMANTIC_REPLAY__ZERO_WRITES", "manifest_filename": MANIFEST_NAME, "manifest_member_count": len(PACKAGE_MEMBERS), "result_sha256": receipt["result_sha256"], "empty_target_graph_disposition_count": 16, "positive_graph_definition_theorems_still_pending": 38_608, "deliverables_write_syscalls": 0, "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-dir")
    parser.add_argument("--verify-no-write", action="store_true")
    parser.add_argument("--promote", action="store_true")
    parser.add_argument("--attack-publish", action="store_true")
    parser.add_argument("--verify-publish", action="store_true")
    parser.add_argument("--manifest-first-no-write", action="store_true")
    args = parser.parse_args()
    require(sum((args.verify_no_write, args.promote, args.attack_publish, args.verify_publish, args.manifest_first_no_write)) == 1, "exactly one mode")
    if args.manifest_first_no_write:
        result = manifest_first_replay()
    else:
        require(args.candidate_dir is not None, "candidate required")
        candidate_directory = Path(args.candidate_dir)
        if args.promote:
            result = promote(candidate_directory)
        elif args.attack_publish:
            suite = coherent_attacks(candidate_directory)
            publish_bytes(ATTACK_NAME, wire(suite))
            result = {"status": suite["status"], "attack_count": 18, "attack_suite_sha256": suite["attack_suite_sha256"]}
        else:
            receipt, _ = replay_directory(candidate_directory)
            result = receipt
            if args.verify_publish:
                publish_bytes(VERIFICATION_NAME, wire(verification_document(receipt)))
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
