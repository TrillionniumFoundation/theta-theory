#!/usr/bin/env python3
"""Independent no-producer verifier for the C73 19-child exclusion oracle.

The verifier never opens, reads, decodes, imports, compiles, or executes the
C73 producer source.  It binds that source only through the hash declared in
the candidate result.  Two isolated C73 candidate directories must be byte
identical and match fixed file/object pins.

The analytic decision is reconstructed from the frozen C72, C37 and C32 inert
ledgers using a separately implemented 384-bit interval-AD kernel and the
closed collision equations.  Centered mean-value Delta_1, strict first-root
order, impact normal and H1 chart signs are recomputed for all 19 complete
children.  Candidate numeric claims, lineage, dispositions and zero-credit
boundaries are then checked row by row.  Only a new audit-stage verification
file may be emitted, using O_EXCL and terminal-byte replay.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Callable, Iterator
import zlib

import flint
from flint import arb, ctx


sys.dont_write_bytecode = True
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
SCHEMA = "cm2.round306c73.recentered-collision1-h1-strict-exclusion-oracle.independent-verification.v1"
PREFIX = "cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v1"
LEDGER_NAME = PREFIX + ".jsonl.gz"
RESULT_NAME = PREFIX + "_result.json"
REPORT_NAME = PREFIX + "_report.md"
MANIFEST_NAME = PREFIX + "_manifest.sha256"
OUTER_NAME = PREFIX + "_outer_receipt.json"
VERIFICATION_NAME = (
    "cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_"
    "independent_verification_v1.json"
)

PRECISION_BITS = 384
PRODUCER_SOURCE_SHA = "5671d625d555d99f5f3ec73e6dc6fe624a4405e076691335773fe13bec36f380"
CANDIDATE_PINS = {
    LEDGER_NAME: ("d8abc927ba85be202b46e6f284ec8c9d3864814125472cd13f76414b083697f3", 61_622),
    RESULT_NAME: ("f305578b5149dd9111b3081372d0e555520119ced52bf86d9929d0739e6c8696", 2_904),
    REPORT_NAME: ("da83dc844bbc065a98a8e92e083457befbb63424f525a6a3d6fb203efeb01f26", 638),
    MANIFEST_NAME: ("a5097e4ab5d1583c518358924168baba5f79ddc132b60e2e6c00ec333087dfaa", 433),
    OUTER_NAME: ("fb19f816953a67f7fbbd2adfc828a963f6266d69e2fc5b21a6c1569dac742c1e", 1_576),
}
CANDIDATE_RESULT_OBJECT = "68486e0200da762f47a5eec6f3b4ebf7e2f430f93bb04a57d76164d30b591d24"
CANDIDATE_OUTER_OBJECT = "1d00eeb195ef680b1232aabcde68e075d3171454ddd266d165b7be66f2eae9dd"
CANDIDATE_ROW_SEQUENCE = "e56bacb2cc3aaf2022538282a9f419def132d27eb7f7f694478153a76eded409"

C72_LEDGER_SHA = "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370"
C72_LEDGER_SIZE = 23_266_147
C72_ROWS = 134_155
C72_SEQUENCE = "2cd348f1821c5d2158008bc8fda4c500388902e385a31e87e281cd6a69be587b"
C72_VERIFY_SHA = "63105e380d37d49bd655e094d41e15d3ed0d182380a44a4a16709ba3308edaf0"
C72_VERIFY_SIZE = 8_307
C72_VERIFY_OBJECT = "8ae20b71916ee1f6d1d28e633b1fbc080f4cb277eed7b6bb54937f8538ae7994"
C37_SHA = "902ccd3a8744a3a4cf851b5f96e1bf9a8c351ace24ce36ae9cb40355079d7dc8"
C37_SIZE = 216_067
C37_ROWS = 862
C37_SEQUENCE = "b2b1c903abd44a5bd6aa6d85535a52f6d17ee91e6de8ee68c25ec354432fecda"
C32_SHA = "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8"
C32_SIZE = 11_222_049
C32_ROWS = 76_832
C32_SEQUENCE = "e2f33100491adadda1045c37be735a80cc8bc7e914132b5647e3df13913ac726"

DEFAULT_CANDIDATE_A = ROOT / ".cm2-runtime/c73-build-a.gxn72Q"
DEFAULT_CANDIDATE_B = ROOT / ".cm2-runtime/c73-build-b.Q6iw1T"
DEFAULT_C72_A = ROOT / ".cm2-runtime/c72-build-a.ZWGF2f" / (
    "cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"
)
DEFAULT_C72_B = ROOT / ".cm2-runtime/c72-build-b.6NX5S7" / (
    "cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"
)
DEFAULT_C72_VERIFY_A = ROOT / ".cm2-runtime/c72-build-a.ZWGF2f" / (
    "cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json"
)
DEFAULT_C72_VERIFY_B = ROOT / ".cm2-runtime/c72-build-b.6NX5S7" / (
    "cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json"
)
DEFAULT_C37 = ROOT / (
    ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38/"
    "ordinary_cell_reflection_pairs.jsonl.gz"
)
DEFAULT_C32 = ROOT / (
    ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9/"
    "compact_cells.jsonl.gz"
)

LINEAGE: dict[int, dict[str, Any]] = {
    31: {
        "origin": "W:E:00.14.01010111",
        "cell": "c32-compact-cell:041f34144b44a873bb333fc801014d0b238faaf33d616f20e8cea534effb8a09",
        "c37": "8178ec54920466e8caf33b267a898e72f5c91b16c6f70cdee9734c7cdcc13b11",
        "c32": "00f0e2db93a2816b5b696cadd7646be1d22e8644f8880621d4d1a9beea528993",
        "active": ["G[2,1]", "W[1,0]"], "competitor": "G[2,1]",
        "chart": "N", "count": 9,
    },
    200: {
        "origin": "W:E:07.01.01101001",
        "cell": "c32-compact-cell:1d466d3e68922feaa50c3db01ba42cc16e1aa90e4ae2af0f8d7abbfff78b79a8",
        "c37": "74e97bf9b7346152eac77b3057b0c816eb24cda4c531194ef3f2e0e843d02f03",
        "c32": "e65303c5fd089c6bbec794f49d1c9fc35e041ad47ea70cce52813521ac221924",
        "active": ["G[2,0]", "W[1,0]"], "competitor": "G[2,0]",
        "chart": "S", "count": 4,
    },
    711: {
        "origin": "W:E:00.14.01011011",
        "cell": "c32-compact-cell:8ee1ada7008271e1806d517118a8c0f2b9932a97b190d7d84770c9925afd62d6",
        "c37": "e66037c00d654cae65bd3a6a6cf56ae8be2a85f29eabc615d7323517d92ea9d4",
        "c32": "367136ed6dac99757e78a92d5c53b26dbb09a83d8b4c5dcacaa437f129ab9025",
        "active": ["G[2,1]", "W[1,0]"], "competitor": "G[2,1]",
        "chart": "N", "count": 6,
    },
}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def obj(value: Any) -> str:
    return sha(canonical(value))


def close(value: dict[str, Any], key: str = "object_sha256") -> dict[str, Any]:
    result = copy.deepcopy(value)
    need(key not in result, "close key absent")
    result[key] = obj(result)
    return result


def duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def parse_line(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and b"\x00" not in raw and not raw.startswith(b"\xef\xbb\xbf"),
         label + ":framing")
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"), object_pairs_hook=duplicate_guard,
            parse_constant=lambda token: (_ for _ in ()).throw(Reject(token)),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Reject(label + ":strict JSON:" + str(error)) from error
    need(type(value) is dict and canonical(value) == raw, label + ":canonical")
    return value


def verify_closed(value: dict[str, Any], key: str, expected: str, label: str) -> None:
    body = copy.deepcopy(value)
    claim = body.pop(key, None)
    need(claim == expected == obj(body), label + ":closure")


def ident(item: os.stat_result) -> tuple[int, ...]:
    return (item.st_dev, item.st_ino, item.st_mode, item.st_nlink, item.st_uid,
            item.st_gid, item.st_size, item.st_mtime_ns, item.st_ctime_ns)


def read_secure(path: Path, expected_sha: str, expected_size: int) -> tuple[bytes, tuple[int, ...]]:
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
         and before.st_uid == os.getuid() and before.st_size == expected_size
         and not before.st_mode & stat.S_IWOTH, "secure shape:" + str(path))
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(ident(opened) == ident(before), "fd/path identity:" + str(path))
        chunks: list[bytes] = []
        remaining = expected_size
        while remaining:
            block = os.read(fd, min(1 << 20, remaining))
            need(bool(block), "short read:" + str(path))
            chunks.append(block)
            remaining -= len(block)
        need(os.read(fd, 1) == b"", "extra byte:" + str(path))
        after_fd = os.fstat(fd)
    finally:
        os.close(fd)
    after_path = path.lstat()
    need(ident(before) == ident(after_fd) == ident(after_path), "TOCTOU:" + str(path))
    raw = b"".join(chunks)
    need(sha(raw) == expected_sha, "hash:" + str(path))
    return raw, ident(before)


def read_json(path: Path, expected_sha: str, expected_size: int) -> dict[str, Any]:
    raw, _identity = read_secure(path, expected_sha, expected_size)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "JSON newline")
    return parse_line(raw[:-1], str(path))


def gzip_rows(
    path: Path, expected_sha: str, expected_size: int, expected_count: int,
    expected_sequence: str,
) -> Iterator[dict[str, Any]]:
    raw, _identity = read_secure(path, expected_sha, expected_size)
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    expanded = decoder.decompress(raw) + decoder.flush()
    need(decoder.eof and decoder.unused_data == b"" and decoder.unconsumed_tail == b"",
         "single gzip member:" + str(path))
    need(expanded.endswith(b"\n") and not expanded.endswith(b"\n\n"), "gzip framing")
    lines = expanded[:-1].split(b"\n")
    need(len(lines) == expected_count, "row count:" + str(path))
    sequence = hashlib.sha256()
    for ordinal, line in enumerate(lines, 1):
        value = parse_line(line, f"{path}:{ordinal}")
        body = copy.deepcopy(value)
        claim = body.pop("row_sha256", None)
        need(type(claim) is str and claim == obj(body), "row closure:" + str(ordinal))
        sequence.update((claim + "\n").encode("ascii"))
        yield value
    need(sequence.hexdigest() == expected_sequence, "row sequence:" + str(path))


def rat(value: Q | int) -> arb:
    q = Q(value)
    return arb(q.numerator) / q.denominator


def interval(lower: Q, upper: Q) -> arb:
    need(lower <= upper, "interval order")
    middle, radius = (lower + upper) / 2, (upper - lower) / 2
    return rat(middle) + arb(0, rat(radius).upper())


@dataclass(frozen=True)
class Jet:
    v: arb
    d: tuple[arb, arb]

    def __add__(self, other: Any) -> "Jet":
        b = jet(other)
        return Jet(self.v + b.v, (self.d[0] + b.d[0], self.d[1] + b.d[1]))

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet(-self.v, (-self.d[0], -self.d[1]))

    def __sub__(self, other: Any) -> "Jet":
        return self + (-jet(other))

    def __rsub__(self, other: Any) -> "Jet":
        return jet(other) - self

    def __mul__(self, other: Any) -> "Jet":
        b = jet(other)
        return Jet(self.v * b.v,
                   (self.d[0] * b.v + self.v * b.d[0],
                    self.d[1] * b.v + self.v * b.d[1]))

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> "Jet":
        b = jet(other)
        den = b.v * b.v
        return Jet(self.v / b.v,
                   ((self.d[0] * b.v - self.v * b.d[0]) / den,
                    (self.d[1] * b.v - self.v * b.d[1]) / den))

    def sqrt(self) -> "Jet":
        need(bool(self.v > 0), "sqrt domain")
        root = self.v.sqrt()
        return Jet(root, (self.d[0] / (2 * root), self.d[1] / (2 * root)))


def jet(value: Any) -> Jet:
    if isinstance(value, Jet):
        return value
    enclosed = value if isinstance(value, arb) else rat(Q(value))
    return Jet(enclosed, (arb(0), arb(0)))


Box = tuple[Q, Q, Q, Q]


def frame(box: Box) -> tuple[Jet, Jet, Jet, Jet]:
    t0, t1, p0, p1 = box
    t = Jet(interval(t0, t1), (arb(1), arb(0)))
    p = Jet(interval(p0, p1), (arb(0), arb(1)))
    a = (jet(1) - t * t).sqrt()
    c = (jet(1) - p * p).sqrt()
    ux = c * a - p * t
    uy = c * t + p * a
    r = jet(Q(4, 25))
    return jet(Q(1, 2)) + r * a, jet(Q(1, 2)) + r * t, ux, uy


def target_data(identifier: str) -> tuple[Q, Q, Q]:
    values = {
        "W[1,0]": (Q(3, 2), Q(1, 2), Q(4, 25)),
        "G[2,1]": (Q(2), Q(1), Q(9, 25)),
        "G[2,0]": (Q(2), Q(0), Q(9, 25)),
    }
    need(identifier in values, "target identifier")
    return values[identifier]


def root_raw(box: Box, identifier: str) -> dict[str, Jet]:
    qx, qy, ux, uy = frame(box)
    ax, ay, rq = target_data(identifier)
    dx, dy = jet(ax) - qx, jet(ay) - qy
    ell = ux * dx + uy * dy
    eta = -uy * dx + ux * dy
    radius = jet(rq)
    delta = radius * radius - eta * eta
    return {"ux": ux, "uy": uy, "ell": ell, "eta": eta,
            "radius": radius, "delta": delta}


def mean_value(function: Callable[[Box], Jet], box: Box, full: Jet) -> arb:
    t0, t1, p0, p1 = box
    tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
    value = function((tc, tc, pc, pc)).v
    value += full.d[0] * interval(-(t1 - t0) / 2, (t1 - t0) / 2)
    value += full.d[1] * interval(-(p1 - p0) / 2, (p1 - p0) / 2)
    return value


def root_preconditioned(box: Box, identifier: str) -> dict[str, Jet]:
    raw = root_raw(box, identifier)
    centered = mean_value(lambda item: root_raw(item, identifier)["delta"],
                          box, raw["delta"])
    delta = Jet(centered, raw["delta"].d)
    radical = delta.sqrt()
    return {**raw, "delta": delta, "radical": radical,
            "near": raw["ell"] - radical, "far": raw["ell"] + radical}


def impact(box: Box) -> tuple[Jet, Jet, Jet, dict[str, Jet]]:
    root = root_preconditioned(box, "W[1,0]")
    z, eta, radius = root["radical"], root["eta"], root["radius"]
    ux, uy = root["ux"], root["uy"]
    nx = (-z * ux + eta * uy) / radius
    ny = (-z * uy - eta * ux) / radius
    return nx * nx - ny * ny, nx, ny, root


def parse_box(row: dict[str, Any]) -> Box:
    payload = row["exact_representative_box"]
    need(payload["s"] == ["0", "0"], "s=0")
    t0, t1 = map(Q, payload["t"])
    p0, p1 = map(Q, payload["p"])
    need(-1 < t0 < t1 < 1 and -1 < p0 < p1 < 1, "strict parameter interior")
    return t0, t1, p0, p1


def independently_decide(row: dict[str, Any], lineage: dict[str, Any]) -> dict[str, Any]:
    box = parse_box(row)
    h1, nx, ny, owner = impact(box)
    h1_centered = mean_value(lambda item: impact(item)[0], box, h1)
    other = root_preconditioned(box, lineage["competitor"])
    order = other["near"] - owner["near"]
    corner_count = 0
    t0, t1, p0, p1 = box
    for t in (t0, t1):
        for p in (p0, p1):
            need(bool(root_raw((t, t, p, p), "W[1,0]")["delta"].v > 0),
                 "corner Delta1")
            corner_count += 1
    need(corner_count == 4 and bool(owner["delta"].v > 0), "centered Delta1")
    need(bool(owner["near"].v > 0) and bool(owner["far"].v > 0), "owner future")
    need(bool(other["delta"].v > 0) and bool(other["near"].v > 0)
         and bool(order.v > 0), "unique first root order")
    need(bool(h1.v < 0) and bool(h1_centered < 0), "H1 negative")
    chart = "N" if bool(ny.v > 0) else "S" if bool(ny.v < 0) else "?"
    need(chart == lineage["chart"] and chart != "W", "outgoing mismatch")
    return {
        "chart": chart,
        "Delta1_lower": str(owner["delta"].v.lower()),
        "near1_lower": str(owner["near"].v.lower()),
        "root_order_lower": str(order.v.lower()),
        "H1_centered_upper": str(h1_centered.upper()),
        "normal_y_lower": str(ny.v.lower()),
        "normal_y_upper": str(ny.v.upper()),
    }


def claim_number(text: str, label: str) -> arb:
    need(type(text) is str and 0 < len(text) < 1024, label + ":string")
    try:
        return arb(text)
    except Exception as error:
        raise Reject(label + ":Arb parse") from error


def validate_candidate_row(candidate: dict[str, Any], source: dict[str, Any],
                           lineage: dict[str, Any], chart: str) -> None:
    need(candidate["C72_obligation_row_sha256"] == source["row_sha256"]
         and candidate["C65_aggregate_child_row_sha256"]
         == source["C65_aggregate_child_row_sha256"]
         and candidate["C61_aggregate_leaf_row_sha256"]
         == source["C61_aggregate_leaf_row_sha256"]
         and candidate["C68_structural_task_row_sha256"]
         == source["C68_structural_task_row_sha256"]
         and candidate["C69c_blocker_row_sha256"]
         == source["C69c_blocker_row_sha256"], "candidate upstream lineage")
    need(candidate["pair_index"] == source["pair_index"]
         and candidate["source_path"] == source["source_path"]
         and candidate["child_path"] == source["child_path"]
         and candidate["exact_representative_box"] == source["exact_representative_box"]
         and candidate["exact_reflected_box"] == source["exact_reflected_box"],
         "candidate exact child")
    need(candidate["representative_origin_key"] == lineage["origin"]
         and candidate["representative_cell_id"] == lineage["cell"]
         and candidate["C37_pair_row_sha256"] == lineage["c37"]
         and candidate["C32_cell_row_sha256"] == lineage["c32"]
         and candidate["active_candidates"] == lineage["active"], "candidate active lineage")
    need(candidate["diagnosis"] ==
         "LEGACY_BROAD_SQRT_EXCEPTION_FALSE_POSITIVE__NOT_DELTA1_ZERO__NOT_SOURCE_P_ENDPOINT"
         and candidate["legacy_structural_category"] == "SOURCE_GRAZING_ENDPOINT_CHART"
         and candidate["legacy_route_witness"] == "SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED",
         "candidate corrected diagnosis")
    need(candidate["frozen_collision1_owner"] == "W[1,0]"
         and candidate["required_collision1_outgoing_chart"] == "W"
         and candidate["active_competitor_evidence"]["target"] == lineage["competitor"]
         and candidate["active_competitor_evidence"]["frozen_owner_is_strict_unique_first"] is True,
         "candidate owner order")
    need(candidate["outgoing_evidence"]["strict_outgoing_chart"] == chart
         and candidate["outgoing_evidence"]["H1_sign"] == "STRICT_NEGATIVE"
         and candidate["outgoing_evidence"]["strict_chart_mismatch"] is True,
         "candidate outgoing conclusion")
    need(bool(claim_number(candidate["collision1_owner_evidence"]
                           ["Delta1_centered_mean_value"]["value"]["lower"],
                           "claimed Delta lower") > 0), "claimed Delta positive")
    need(bool(claim_number(candidate["active_competitor_evidence"]
                           ["competitor_near_minus_owner_near"]["value"]["lower"],
                           "claimed order lower") > 0), "claimed root order positive")
    need(bool(claim_number(candidate["outgoing_evidence"]
                           ["H1_centered_mean_value"]["upper"],
                           "claimed H1 upper") < 0), "claimed H1 negative")
    ny_value = candidate["outgoing_evidence"]["normal_y"]["value"]
    if chart == "N":
        need(bool(claim_number(ny_value["lower"], "claimed ny lower") > 0), "claimed N")
    else:
        need(bool(claim_number(ny_value["upper"], "claimed ny upper") < 0), "claimed S")
    need(candidate["disposition"] ==
         "STRICT_EXCLUSION_COLLISION1_OUTGOING_CHART_MISMATCH"
         and candidate["allowed_exit_class"] == "STRICT_EXCLUSION"
         and candidate["complete_child_decision"] is True
         and candidate["additional_dyadic_depth_used"] == 0
         and candidate["blowup_or_endpoint_graph_required"] is False
         and candidate["local_strict_terminal"] is True
         and candidate["formal_credit"] == candidate["whole_parent_credit"]
         == candidate["D02_gate_credit"] == 0, "candidate disposition boundary")


def read_candidate(directory: Path) -> tuple[dict[str, bytes], dict[str, tuple[int, ...]]]:
    need(directory.is_dir(), "candidate directory")
    raw: dict[str, bytes] = {}
    identities: dict[str, tuple[int, ...]] = {}
    for name, (expected_sha, expected_size) in CANDIDATE_PINS.items():
        raw[name], identities[name] = read_secure(directory / name, expected_sha, expected_size)
    need(set(path.name for path in directory.iterdir()) == set(CANDIDATE_PINS),
         "candidate exact member set")
    need(identities[OUTER_NAME][7] > identities[MANIFEST_NAME][7]
         and identities[MANIFEST_NAME][7] > max(
             identities[name][7] for name in (LEDGER_NAME, RESULT_NAME, REPORT_NAME)),
         "manifest then outer publication order")
    expected_manifest = "".join(
        f"{CANDIDATE_PINS[name][0]}  {name}\n"
        for name in sorted((LEDGER_NAME, RESULT_NAME, REPORT_NAME))
    ).encode("ascii")
    need(raw[MANIFEST_NAME] == expected_manifest, "one manifest exact")
    return raw, identities


def validate_lineage(c37: Path, c32: Path) -> None:
    found_pairs: dict[int, dict[str, Any]] = {}
    for row in gzip_rows(c37, C37_SHA, C37_SIZE, C37_ROWS, C37_SEQUENCE):
        if row.get("pair_index") in LINEAGE:
            found_pairs[row["pair_index"]] = row
    need(set(found_pairs) == set(LINEAGE), "C37 selected pairs")
    for pair, expected in LINEAGE.items():
        row = found_pairs[pair]
        need(row["row_sha256"] == expected["c37"]
             and row["representative_cell_id"] == expected["cell"]
             and row["representative_origin_key"] == expected["origin"], "C37 lineage")
    wanted = {value["cell"] for value in LINEAGE.values()}
    cells: dict[str, dict[str, Any]] = {}
    for row in gzip_rows(c32, C32_SHA, C32_SIZE, C32_ROWS, C32_SEQUENCE):
        if row.get("cell_id") in wanted:
            cells[row["cell_id"]] = row
    need(set(cells) == wanted, "C32 selected cells")
    for expected in LINEAGE.values():
        row = cells[expected["cell"]]
        need(row["row_sha256"] == expected["c32"]
             and row["origin_key"] == expected["origin"]
             and row["source_lineage"]["active_candidates"] == expected["active"]
             and row["gate3_chart"] == "W:E" and row["physical_slice"] == "s=0",
             "C32 lineage")


def selected_c72(path: Path) -> list[dict[str, Any]]:
    result = []
    for row in gzip_rows(path, C72_LEDGER_SHA, C72_LEDGER_SIZE, C72_ROWS, C72_SEQUENCE):
        if row.get("structural_category") == "SOURCE_GRAZING_ENDPOINT_CHART":
            need(row["required_decider"] == "EXACT_SOURCE_GRAZING_ENDPOINT_ORACLE"
                 and row["formal_credit"] == row["whole_parent_credit"]
                 == row["D02_gate_credit"] == 0, "C72 strict boundary")
            result.append(row)
    need(len(result) == 19, "C72 selected 19")
    return result


def result_semantics(value: dict[str, Any]) -> None:
    verify_closed(value, "object_sha256", value.get("object_sha256", ""), "candidate result")
    need(value["status"] ==
         "PASS_19_OF_19_LEGACY_SOURCE_GRAZING_LABELS_ARE_STRICT_POSITIVE_DELTA1__9_N_PLUS_4_S_PLUS_6_N_OUTGOING_MISMATCH__STRICT_EXCLUSION__ZERO_GLOBAL_CREDIT",
         "candidate result status")
    need(value["producer_file_sha256"] == PRODUCER_SOURCE_SHA, "producer declaration pin")
    need(value["input_domain"] == {"C72_SOURCE_GRAZING_ENDPOINT_CHART": 19}
         and value["pair_census"] == {"31": 9, "200": 4, "711": 6}
         and value["decision_census"] == {
             "STRICT_EXCLUSION_COLLISION1_OUTGOING_CHART_MISMATCH": 19,
             "outgoing_chart_N": 15, "outgoing_chart_S": 4,
         }, "candidate result census")
    need(value["ledger"] == {
        "filename": LEDGER_NAME, "order": "C72_FILTERED_LEDGER_ORDER",
        "row_count": 19, "row_hash_line_sequence_sha256": CANDIDATE_ROW_SEQUENCE,
        "sha256": CANDIDATE_PINS[LEDGER_NAME][0], "size": CANDIDATE_PINS[LEDGER_NAME][1],
    }, "candidate ledger descriptor")
    need(value["strict_boundary"] == {
        "candidate_is_global_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "global_unresolved_decrement": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }, "candidate result zero credit")
    need(value["producer_self_test"]["attack_count"] == 12
         and all(value["producer_self_test"]["attacks"].values()), "producer self-test")


def coherent_attacks(result: dict[str, Any], row: dict[str, Any],
                     source: dict[str, Any], lineage: dict[str, Any], chart: str) -> dict[str, Any]:
    attacks: dict[str, bool] = {}

    def row_attack(name: str, mutation: Callable[[dict[str, Any]], None]) -> None:
        candidate = copy.deepcopy(row)
        candidate.pop("row_sha256")
        mutation(candidate)
        candidate = close(candidate, "row_sha256")
        try:
            validate_candidate_row(candidate, source, lineage, chart)
        except Exception:
            attacks[name] = True
        else:
            attacks[name] = False

    row_attack("row_pair", lambda value: value.__setitem__("pair_index", 0))
    row_attack("row_C72", lambda value: value.__setitem__("C72_obligation_row_sha256", "0" * 64))
    row_attack("row_origin", lambda value: value.__setitem__("representative_origin_key", "W:E:bad"))
    row_attack("row_active", lambda value: value.__setitem__("active_candidates", ["W[1,0]"]))
    row_attack("row_diagnosis", lambda value: value.__setitem__("diagnosis", "REAL_GRAZING"))
    row_attack("row_chart", lambda value: value["outgoing_evidence"].__setitem__("strict_outgoing_chart", "W"))
    row_attack("row_disposition", lambda value: value.__setitem__("disposition", "SEALED_COLLISION3_HANDOFF"))
    row_attack("row_depth", lambda value: value.__setitem__("additional_dyadic_depth_used", 1))
    row_attack("row_blowup", lambda value: value.__setitem__("blowup_or_endpoint_graph_required", True))
    for field in ("formal_credit", "whole_parent_credit", "D02_gate_credit"):
        row_attack("row_" + field, lambda value, key=field: value.__setitem__(key, 1))

    def result_attack(name: str, mutation: Callable[[dict[str, Any]], None]) -> None:
        body = copy.deepcopy(result)
        body.pop("object_sha256")
        mutation(body)
        candidate = close(body)
        try:
            result_semantics(candidate)
        except Exception:
            attacks[name] = True
        else:
            attacks[name] = False

    result_attack("result_status", lambda value: value.__setitem__("status", "PASS"))
    result_attack("result_count", lambda value: value["input_domain"].__setitem__(
        "C72_SOURCE_GRAZING_ENDPOINT_CHART", 18))
    result_attack("result_pair", lambda value: value["pair_census"].__setitem__("31", 8))
    result_attack("result_decision", lambda value: value["decision_census"].__setitem__(
        "STRICT_EXCLUSION_COLLISION1_OUTGOING_CHART_MISMATCH", 18))
    result_attack("result_producer", lambda value: value.__setitem__("producer_file_sha256", "0" * 64))
    for field in ("formal_credit", "whole_parent_credit", "D02_gate_credit",
                  "global_unresolved_decrement"):
        result_attack("result_" + field,
                      lambda value, key=field: value["strict_boundary"].__setitem__(key, 1))
    result_attack("result_authority", lambda value: value["strict_boundary"].__setitem__(
        "candidate_is_global_authority", True))
    result_attack("result_pointer", lambda value: value["strict_boundary"].__setitem__(
        "runtime_canonical_pointer_or_seal_writes", True))
    need(len(attacks) == 23 and all(attacks.values()), "23 coherent attacks")
    return {"status": "PASS_23_OF_23_COHERENT_ROW_LINEAGE_DECISION_AND_CREDIT_ATTACKS_FAIL_CLOSED",
            "attack_count": 23, "attacks": attacks}


def emit(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_CLOEXEC", 0), 0o444)
    try:
        offset = 0
        while offset < len(raw):
            offset += os.write(fd, raw[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)
    replay, _identity = read_secure(path, sha(raw), len(raw))
    need(replay == raw and replay[-1:] == raw[-1:], "verification terminal replay")


def verify(args: argparse.Namespace) -> dict[str, Any]:
    need(flint.__version__ == "0.9.0" and flint.__FLINT_VERSION__ == "3.6.0",
         "flint versions")
    ctx.dps = 115
    ctx.prec = PRECISION_BITS
    ctx.threads = 1
    ctx.pretty = True
    ctx.unicode = False

    raw_a, ids_a = read_candidate(Path(args.candidate_a))
    raw_b, ids_b = read_candidate(Path(args.candidate_b))
    need(raw_a == raw_b, "dual isolated candidate byte identity")
    result = parse_line(raw_a[RESULT_NAME][:-1], "candidate result")
    verify_closed(result, "object_sha256", CANDIDATE_RESULT_OBJECT, "candidate result")
    result_semantics(result)
    outer = parse_line(raw_a[OUTER_NAME][:-1], "candidate outer")
    verify_closed(outer, "object_sha256", CANDIDATE_OUTER_OBJECT, "candidate outer")
    need(outer["result_object_sha256"] == CANDIDATE_RESULT_OBJECT
         and outer["manifest_sha256"] == CANDIDATE_PINS[MANIFEST_NAME][0]
         and outer["outer_receipt_published_last"] is True
         and outer["formal_credit"] == outer["D02_gate_credit"] == 0,
         "outer semantics")

    c72_verify_a = read_json(Path(args.c72_verification_a), C72_VERIFY_SHA, C72_VERIFY_SIZE)
    c72_verify_b = read_json(Path(args.c72_verification_b), C72_VERIFY_SHA, C72_VERIFY_SIZE)
    verify_closed(c72_verify_a, "object_sha256", C72_VERIFY_OBJECT, "C72 verification A")
    verify_closed(c72_verify_b, "object_sha256", C72_VERIFY_OBJECT, "C72 verification B")
    need(c72_verify_a == c72_verify_b
         and c72_verify_a["all_134155_rows_exactly_rebuilt"] is True
         and c72_verify_a["dual_isolated_candidate_byte_identity"]
         == {"ledger": True, "report": True, "result": True}, "C72 verified dual build")

    sources_a = selected_c72(Path(args.c72_a))
    sources_b = selected_c72(Path(args.c72_b))
    need(sources_a == sources_b, "dual C72 selected source identity")
    validate_lineage(Path(args.c37_pairs), Path(args.c32_cells))

    candidates = list(gzip_rows(
        Path(args.candidate_a) / LEDGER_NAME, CANDIDATE_PINS[LEDGER_NAME][0],
        CANDIDATE_PINS[LEDGER_NAME][1], 19, CANDIDATE_ROW_SEQUENCE,
    ))
    need(len(candidates) == len(sources_a) == 19, "candidate/source join count")
    proof_sequence = hashlib.sha256()
    pair_census: dict[str, int] = {}
    chart_census = {"N": 0, "S": 0}
    proof_rows = []
    for ordinal, (candidate, source) in enumerate(zip(candidates, sources_a), 1):
        need(candidate["C72_obligation_row_sha256"] == source["row_sha256"],
             "candidate C72 order")
        lineage = LINEAGE[source["pair_index"]]
        proof = independently_decide(source, lineage)
        validate_candidate_row(candidate, source, lineage, proof["chart"])
        proof_row = {
            "ordinal": ordinal,
            "candidate_row_sha256": candidate["row_sha256"],
            "C72_row_sha256": source["row_sha256"],
            "pair_index": source["pair_index"],
            "child_path": source["child_path"],
            **proof,
        }
        proof_hash = obj(proof_row)
        proof_sequence.update((proof_hash + "\n").encode("ascii"))
        proof_rows.append({**proof_row, "proof_row_sha256": proof_hash})
        key = str(source["pair_index"])
        pair_census[key] = pair_census.get(key, 0) + 1
        chart_census[proof["chart"]] += 1
    need(pair_census == {"31": 9, "200": 4, "711": 6}
         and chart_census == {"N": 15, "S": 4}, "independent decision census")

    attacks = coherent_attacks(result, candidates[0], sources_a[0], LINEAGE[31], "N")
    verification = close({
        "schema": SCHEMA,
        "status": "PASS_NO_C73_PRODUCER_READ_IMPORT_EXECUTION_OR_DECODE__DUAL_C73_BYTE_IDENTITY__19_OF_19_CENTERED_DELTA1_POSITIVE__STRICT_FIRST_W10__15_N_PLUS_4_S_MISMATCH__STRICT_EXCLUSION__ZERO_CREDIT",
        "verifier_file_sha256": sha(SELF.read_bytes()),
        "producer_file_sha256_bound_but_not_opened": PRODUCER_SOURCE_SHA,
        "producer_source_consumed": False,
        "producer_source_imported_or_executed": False,
        "numeric_context": {
            "precision_bits": PRECISION_BITS,
            "python_flint_version": flint.__version__,
            "flint_version": flint.__FLINT_VERSION__,
            "threads": 1,
        },
        "dual_candidate_file_sha256": {
            name: values[0] for name, values in CANDIDATE_PINS.items()
        },
        "dual_candidate_bytes_identical": True,
        "candidate_result_object_sha256": CANDIDATE_RESULT_OBJECT,
        "candidate_outer_object_sha256": CANDIDATE_OUTER_OBJECT,
        "candidate_manifest_then_outer_last": True,
        "upstream_file_sha256": {
            "C72_dual_ledger": C72_LEDGER_SHA,
            "C72_dual_verification": C72_VERIFY_SHA,
            "C37_pairs": C37_SHA,
            "C32_cells": C32_SHA,
        },
        "independent_reconstruction": {
            "complete_child_count": 19,
            "pair_census": pair_census,
            "outgoing_chart_census": chart_census,
            "all_centered_Delta1_strict_positive": True,
            "all_four_tp_corners_and_eight_degenerate_s_lifts_strict_positive": True,
            "all_W10_near_roots_strict_future": True,
            "all_W10_roots_strictly_before_only_active_G_competitor": True,
            "all_H1_centered_strict_negative": True,
            "all_outgoing_charts_strict_N_or_S_not_required_W": True,
            "all_dispositions_STRICT_EXCLUSION": True,
            "additional_dyadic_depth": 0,
            "endpoint_or_blowup_chart_used": False,
            "proof_row_hash_line_sequence_sha256": proof_sequence.hexdigest(),
            "proof_rows": proof_rows,
        },
        "legacy_diagnosis": {
            "C39_broad_except_did_not_prove_Delta1_zero": True,
            "actual_Delta1_zero_child_count": 0,
            "actual_source_p_endpoint_child_count": 0,
            "false_positive_legacy_label_child_count": 19,
        },
        "coherent_attacks": attacks,
        "strict_boundary": {
            "candidate_is_global_authority": False,
            "formal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
            "global_unresolved_decrement": 0,
            "runtime_canonical_pointer_or_seal_writes": False,
        },
        "all_input_and_candidate_files_regular_single_link_nofollow_TOCTOU_closed": True,
        "all_candidate_files_terminal_byte_replayed": True,
    })
    output = Path(args.output).absolute()
    need(output.is_dir() and not any(output.iterdir()), "empty output audit stage")
    raw = canonical(verification) + b"\n"
    emit(output / VERIFICATION_NAME, raw)
    return {
        "status": "PASS_C73_INDEPENDENT_VERIFICATION_STAGE_EMITTED",
        "output": str(output),
        "verification_file_sha256": sha(raw),
        "verification_object_sha256": verification["object_sha256"],
        "proof_row_hash_line_sequence_sha256": proof_sequence.hexdigest(),
    }


def arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-a", default=str(DEFAULT_CANDIDATE_A))
    parser.add_argument("--candidate-b", default=str(DEFAULT_CANDIDATE_B))
    parser.add_argument("--c72-a", default=str(DEFAULT_C72_A))
    parser.add_argument("--c72-b", default=str(DEFAULT_C72_B))
    parser.add_argument("--c72-verification-a", default=str(DEFAULT_C72_VERIFY_A))
    parser.add_argument("--c72-verification-b", default=str(DEFAULT_C72_VERIFY_B))
    parser.add_argument("--c37-pairs", default=str(DEFAULT_C37))
    parser.add_argument("--c32-cells", default=str(DEFAULT_C32))
    parser.add_argument("--output", required=True)
    return parser


def main() -> int:
    try:
        outcome = verify(arguments().parse_args())
    except Exception as error:
        print(json.dumps({"status": "REJECTED", "error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps(outcome, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
