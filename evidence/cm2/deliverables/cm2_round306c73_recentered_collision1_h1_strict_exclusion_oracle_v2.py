#!/usr/bin/env python3
"""C73 v2: exact-recenter all 1,163 C72 children carrying the broad C39 sqrt-exception witness.

The legacy C39 router caught every exception raised by a natural interval
``sqrt(Delta_1)`` and labelled the result as requiring a source-grazing
endpoint chart.  That label was deliberately fail-closed, but it was not a
proof that ``Delta_1=0`` occurred.

This no-upstream-producer oracle reads only frozen inert ledgers.  For each of
the 1,163 C72 rows carrying that exact child-level witness it independently
evaluates the collision-one equations at
384-bit Arb precision.  A centered mean-value enclosure proves Delta_1>0 on
the complete child, after which the square root, first-root ordering, impact
normal and H1 outgoing chart are all evaluated on that same complete box.
Every row has the frozen owner W[1,0] as the strict first hit, but its outgoing
chart is N or S rather than the required W.  Consequently all 1,163 rows are
strict whole-child exclusions.  The evidence remains zero formal/D02 credit
until consumed by the frozen global no-producer consumer.

No C72 file or frozen upstream file is modified.  Outputs use O_EXCL in a
caller-supplied empty staging directory; the outer receipt is emitted last.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from fractions import Fraction as Q
import gzip
import hashlib
import io
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
SCHEMA = "cm2.round306c73.recentered-collision1-h1-strict-exclusion-oracle.v2"
PREFIX = "cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2"
LEDGER_NAME = PREFIX + ".jsonl.gz"
RESULT_NAME = PREFIX + "_result.json"
REPORT_NAME = PREFIX + "_report.md"
MANIFEST_NAME = PREFIX + "_manifest.sha256"
OUTER_NAME = PREFIX + "_outer_receipt.json"

PRECISION_BITS = 384
EXPECTED_C72_LEDGER_SHA = "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370"
EXPECTED_C72_LEDGER_SIZE = 23_266_147
EXPECTED_C72_ROWS = 134_155
EXPECTED_C72_SEQUENCE = "2cd348f1821c5d2158008bc8fda4c500388902e385a31e87e281cd6a69be587b"
EXPECTED_C72_VERIFICATION_SHA = "63105e380d37d49bd655e094d41e15d3ed0d182380a44a4a16709ba3308edaf0"
EXPECTED_C72_VERIFICATION_SIZE = 8_307
EXPECTED_C72_VERIFICATION_OBJECT = "8ae20b71916ee1f6d1d28e633b1fbc080f4cb277eed7b6bb54937f8538ae7994"
EXPECTED_C37_LEDGER_SHA = "902ccd3a8744a3a4cf851b5f96e1bf9a8c351ace24ce36ae9cb40355079d7dc8"
EXPECTED_C37_LEDGER_SIZE = 216_067
EXPECTED_C37_ROWS = 862
EXPECTED_C37_SEQUENCE = "b2b1c903abd44a5bd6aa6d85535a52f6d17ee91e6de8ee68c25ec354432fecda"
EXPECTED_C32_LEDGER_SHA = "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8"
EXPECTED_C32_LEDGER_SIZE = 11_222_049
EXPECTED_C32_ROWS = 76_832
EXPECTED_C32_SEQUENCE = "e2f33100491adadda1045c37be735a80cc8bc7e914132b5647e3df13913ac726"

EXPECTED_BROAD_EXCEPTION_CATEGORY_CENSUS = {
    "REGULAR_MULTI_GRAPH_FIRST_TANGENCY": 459,
    "REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED": 685,
    "SOURCE_GRAZING_ENDPOINT_CHART": 19,
}
EXPECTED_REQUIRED_DECIDER = {
    "REGULAR_MULTI_GRAPH_FIRST_TANGENCY": "EXACT_FIRST_TANGENCY_ORACLE",
    "REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED":
        "EXACT_MULTI_GRAPH_ORDER_ORACLE",
    "SOURCE_GRAZING_ENDPOINT_CHART": "EXACT_SOURCE_GRAZING_ENDPOINT_ORACLE",
}

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
# Keep the actual authority path explicit rather than resolving a mutable
# current-token pointer.
DEFAULT_C37 = ROOT / (
    ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38/"
    "ordinary_cell_reflection_pairs.jsonl.gz"
)
DEFAULT_C32 = ROOT / (
    ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9/"
    "compact_cells.jsonl.gz"
)

PAIR_LINEAGE: dict[int, dict[str, Any]] = {
    31: {
        "origin_key": "W:E:00.14.01010111",
        "representative_cell_id": "c32-compact-cell:041f34144b44a873bb333fc801014d0b238faaf33d616f20e8cea534effb8a09",
        "C37_pair_row_sha256": "8178ec54920466e8caf33b267a898e72f5c91b16c6f70cdee9734c7cdcc13b11",
        "C32_cell_row_sha256": "00f0e2db93a2816b5b696cadd7646be1d22e8644f8880621d4d1a9beea528993",
        "active_candidates": ["G[2,1]", "W[1,0]"],
        "competitor": "G[2,1]",
        "expected_chart": "N",
        "expected_count": 9,
    },
    200: {
        "origin_key": "W:E:07.01.01101001",
        "representative_cell_id": "c32-compact-cell:1d466d3e68922feaa50c3db01ba42cc16e1aa90e4ae2af0f8d7abbfff78b79a8",
        "C37_pair_row_sha256": "74e97bf9b7346152eac77b3057b0c816eb24cda4c531194ef3f2e0e843d02f03",
        "C32_cell_row_sha256": "e65303c5fd089c6bbec794f49d1c9fc35e041ad47ea70cce52813521ac221924",
        "active_candidates": ["G[2,0]", "W[1,0]"],
        "competitor": "G[2,0]",
        "expected_chart": "S",
        "expected_count": 4,
    },
    270: {
        "origin_key": "W:E:07.01.01101010",
        "representative_cell_id": "c32-compact-cell:2c5fb436107089292c28f4ab2167a0b1423c0fb6d64a327c164ff42739ad071d",
        "C37_pair_row_sha256": "8ec98ae61d743ec5f3f88b061acf19ede2a70a12b490aff88753f8fdfc903830",
        "C32_cell_row_sha256": "4ae4a43c8e6b7a9769b85ccba42b473e3d86a878e00f78c87560a266c0b4508e",
        "active_candidates": ["G[2,0]", "W[1,0]"],
        "competitor": "G[2,0]",
        "expected_chart": "S",
        "expected_count": 11,
    },
    711: {
        "origin_key": "W:E:00.14.01011011",
        "representative_cell_id": "c32-compact-cell:8ee1ada7008271e1806d517118a8c0f2b9932a97b190d7d84770c9925afd62d6",
        "C37_pair_row_sha256": "e66037c00d654cae65bd3a6a6cf56ae8be2a85f29eabc615d7323517d92ea9d4",
        "C32_cell_row_sha256": "367136ed6dac99757e78a92d5c53b26dbb09a83d8b4c5dcacaa437f129ab9025",
        "active_candidates": ["G[2,1]", "W[1,0]"],
        "competitor": "G[2,1]",
        "expected_chart": "N",
        "expected_count": 6,
    },
}


class Rejected(RuntimeError):
    """Fail-closed input, analytic, or publication rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def object_sha(value: Any) -> str:
    return sha_bytes(canonical(value))


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    need("object_sha256" not in result, "object hash field absent")
    result["object_sha256"] = object_sha(result)
    return result


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    need("row_sha256" not in result, "row hash field absent")
    result["row_sha256"] = object_sha(result)
    return result


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def parse_json_line(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         label + ":framing")
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"), object_pairs_hook=reject_duplicates,
            parse_constant=lambda token: (_ for _ in ()).throw(Rejected(token)),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Rejected(label + ":strict JSON:" + str(error)) from error
    need(type(value) is dict and canonical(value) == raw, label + ":canonical")
    return value


def verify_row(value: dict[str, Any], label: str) -> None:
    body = copy.deepcopy(value)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == object_sha(body), label + ":row closure")


def verify_object(value: dict[str, Any], expected: str, label: str) -> None:
    body = copy.deepcopy(value)
    claimed = body.pop("object_sha256", None)
    need(claimed == expected == object_sha(body), label + ":object closure")


def identity(item: os.stat_result) -> tuple[int, ...]:
    return (
        item.st_dev, item.st_ino, item.st_mode, item.st_nlink, item.st_uid,
        item.st_gid, item.st_size, item.st_mtime_ns, item.st_ctime_ns,
    )


def secure_bytes(path: Path, expected_sha: str, expected_size: int) -> bytes:
    before = path.lstat()
    need(
        stat.S_ISREG(before.st_mode) and before.st_nlink == 1
        and before.st_uid == os.getuid() and before.st_size == expected_size
        and not before.st_mode & stat.S_IWOTH,
        "secure file shape:" + str(path),
    )
    descriptor = os.open(
        path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        need(identity(opened) == identity(before), "path/fd identity:" + str(path))
        blocks: list[bytes] = []
        remaining = expected_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            need(bool(block), "short read:" + str(path))
            blocks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "extra byte:" + str(path))
        after_fd = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    after_path = path.lstat()
    need(identity(before) == identity(after_fd) == identity(after_path),
         "TOCTOU:" + str(path))
    raw = b"".join(blocks)
    need(sha_bytes(raw) == expected_sha, "file hash:" + str(path))
    return raw


def secure_json(path: Path, expected_sha: str, expected_size: int) -> dict[str, Any]:
    raw = secure_bytes(path, expected_sha, expected_size)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "JSON newline:" + str(path))
    return parse_json_line(raw[:-1], str(path))


def iter_secure_gzip(
    path: Path,
    expected_sha: str,
    expected_size: int,
    expected_rows: int,
    expected_sequence: str,
) -> Iterator[dict[str, Any]]:
    raw = secure_bytes(path, expected_sha, expected_size)
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    expanded = decoder.decompress(raw) + decoder.flush()
    need(decoder.eof and decoder.unused_data == b"" and decoder.unconsumed_tail == b"",
         "single complete gzip member:" + str(path))
    need(expanded.endswith(b"\n") and not expanded.endswith(b"\n\n"),
         "gzip line framing:" + str(path))
    lines = expanded[:-1].split(b"\n")
    need(len(lines) == expected_rows, "gzip row count:" + str(path))
    sequence = hashlib.sha256()
    for ordinal, line in enumerate(lines, 1):
        value = parse_json_line(line, f"{path}:{ordinal}")
        verify_row(value, f"{path}:{ordinal}")
        sequence.update((value["row_sha256"] + "\n").encode("ascii"))
        yield value
    need(sequence.hexdigest() == expected_sequence, "row sequence:" + str(path))


def aq(value: Q | int) -> arb:
    fraction = Q(value)
    return arb(fraction.numerator) / fraction.denominator


def ai(lower: Q, upper: Q) -> arb:
    need(lower <= upper, "ordered rational interval")
    middle = (lower + upper) / 2
    radius = (upper - lower) / 2
    return aq(middle) + arb(0, aq(radius).upper())


@dataclass(frozen=True)
class AD2:
    value: arb
    derivative: tuple[arb, arb]

    def __add__(self, other: Any) -> "AD2":
        right = ad(other)
        return AD2(
            self.value + right.value,
            tuple(a + b for a, b in zip(self.derivative, right.derivative)),
        )

    __radd__ = __add__

    def __neg__(self) -> "AD2":
        return AD2(-self.value, tuple(-value for value in self.derivative))

    def __sub__(self, other: Any) -> "AD2":
        return self + (-ad(other))

    def __rsub__(self, other: Any) -> "AD2":
        return ad(other) - self

    def __mul__(self, other: Any) -> "AD2":
        right = ad(other)
        return AD2(
            self.value * right.value,
            tuple(
                a * right.value + self.value * b
                for a, b in zip(self.derivative, right.derivative)
            ),
        )

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> "AD2":
        right = ad(other)
        denominator = right.value * right.value
        return AD2(
            self.value / right.value,
            tuple(
                (a * right.value - self.value * b) / denominator
                for a, b in zip(self.derivative, right.derivative)
            ),
        )

    def sqrt(self) -> "AD2":
        need(bool(self.value > 0), "strict square-root domain")
        root = self.value.sqrt()
        return AD2(root, tuple(value / (2 * root) for value in self.derivative))


def ad(value: Any) -> AD2:
    if isinstance(value, AD2):
        return value
    enclosed = value if isinstance(value, arb) else aq(Q(value))
    return AD2(enclosed, (arb(0), arb(0)))


Box = tuple[Q, Q, Q, Q]


def variables(box: Box) -> tuple[AD2, AD2]:
    t0, t1, p0, p1 = box
    return (
        AD2(ai(t0, t1), (arb(1), arb(0))),
        AD2(ai(p0, p1), (arb(0), arb(1))),
    )


def target(identifier: str) -> tuple[Q, Q, Q]:
    if identifier == "W[1,0]":
        return Q(3, 2), Q(1, 2), Q(4, 25)
    if identifier == "G[2,1]":
        return Q(2), Q(1), Q(9, 25)
    if identifier == "G[2,0]":
        return Q(2), Q(0), Q(9, 25)
    raise Rejected("unknown target:" + identifier)


def initial_geometry(box: Box) -> tuple[AD2, AD2, AD2, AD2]:
    t, p = variables(box)
    normal_x = (ad(1) - t * t).sqrt()
    normal_y = t
    cosine = (ad(1) - p * p).sqrt()
    velocity_x = cosine * normal_x - p * normal_y
    velocity_y = cosine * normal_y + p * normal_x
    source_radius = ad(Q(4, 25))
    return (
        ad(Q(1, 2)) + source_radius * normal_x,
        ad(Q(1, 2)) + source_radius * normal_y,
        velocity_x,
        velocity_y,
    )


def raw_root(box: Box, identifier: str) -> dict[str, AD2]:
    qx, qy, ux, uy = initial_geometry(box)
    ax, ay, radius_q = target(identifier)
    dx, dy = ad(ax) - qx, ad(ay) - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = ad(radius_q)
    delta = radius * radius - transverse * transverse
    return {
        "qx": qx, "qy": qy, "ux": ux, "uy": uy,
        "ell": ell, "transverse": transverse, "radius": radius,
        "Delta": delta,
    }


def centered_value(function: Callable[[Box], AD2], box: Box, full: AD2) -> arb:
    t0, t1, p0, p1 = box
    tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
    center = function((tc, tc, pc, pc)).value
    widths = ((t1 - t0) / 2, (p1 - p0) / 2)
    enclosure = center
    for derivative, width in zip(full.derivative, widths):
        enclosure += derivative * ai(-width, width)
    return enclosure


def preconditioned_root(box: Box, identifier: str) -> dict[str, AD2]:
    raw = raw_root(box, identifier)
    centered_delta = centered_value(lambda item: raw_root(item, identifier)["Delta"],
                                    box, raw["Delta"])
    delta = AD2(centered_delta, raw["Delta"].derivative)
    radical = delta.sqrt()
    return {**raw, "Delta_natural": raw["Delta"], "Delta": delta,
            "radical": radical, "near": raw["ell"] - radical,
            "far": raw["ell"] + radical}


def collision1_h1(box: Box) -> tuple[AD2, AD2, AD2, dict[str, AD2]]:
    root = preconditioned_root(box, "W[1,0]")
    radical, transverse, radius = root["radical"], root["transverse"], root["radius"]
    ux, uy = root["ux"], root["uy"]
    nx = (-radical * ux + transverse * uy) / radius
    ny = (-radical * uy - transverse * ux) / radius
    return nx * nx - ny * ny, nx, ny, root


def bounds(value: arb) -> dict[str, str]:
    return {"lower": str(value.lower()), "upper": str(value.upper())}


def ad_evidence(value: AD2) -> dict[str, Any]:
    return {
        "value": bounds(value.value),
        "derivative_dt": bounds(value.derivative[0]),
        "derivative_dp": bounds(value.derivative[1]),
    }


def box_from_row(row: dict[str, Any]) -> Box:
    payload = row["exact_representative_box"]
    need(payload["s"] == ["0", "0"], "C73 requires exact s=0")
    t0, t1 = (Q(value) for value in payload["t"])
    p0, p1 = (Q(value) for value in payload["p"])
    need(-1 < p0 < p1 < 1 and -1 < t0 < t1 < 1, "strict chart interior")
    return t0, t1, p0, p1


def corner_evidence(box: Box) -> list[dict[str, Any]]:
    t0, t1, p0, p1 = box
    result = []
    for t in (t0, t1):
        for p in (p0, p1):
            value = raw_root((t, t, p, p), "W[1,0]")["Delta"].value
            need(bool(value > 0), "strict positive Delta corner")
            result.append({"t": str(t), "p": str(p), "Delta1": bounds(value),
                           "sign": "STRICT_POSITIVE"})
    return result


def decide(row: dict[str, Any], lineage: dict[str, Any]) -> dict[str, Any]:
    box = box_from_row(row)
    h1, nx, ny, owner = collision1_h1(box)
    h1_centered = centered_value(lambda item: collision1_h1(item)[0], box, h1)
    competitor = preconditioned_root(box, lineage["competitor"])
    order = competitor["near"] - owner["near"]
    corners = corner_evidence(box)

    need(bool(owner["Delta"].value > 0), "whole-child centered Delta1 positive")
    need(bool(owner["near"].value > 0) and bool(owner["far"].value > 0),
         "whole-child W owner strict future")
    need(bool(competitor["Delta"].value > 0)
         and bool(competitor["near"].value > 0), "competitor strict future")
    need(bool(order.value > 0), "W owner strictly earlier than active competitor")
    need(bool(h1.value < 0) and bool(h1_centered < 0), "whole-child H1 negative")
    if bool(ny.value > 0):
        chart = "N"
    elif bool(ny.value < 0):
        chart = "S"
    else:
        raise Rejected("normal-y sign unresolved")
    need(chart == lineage["expected_chart"] and chart != "W", "strict outgoing mismatch")

    return close_row({
        "schema": SCHEMA + ".decision-row",
        "C72_obligation_row_sha256": row["row_sha256"],
        "C65_aggregate_child_row_sha256": row["C65_aggregate_child_row_sha256"],
        "C61_aggregate_leaf_row_sha256": row["C61_aggregate_leaf_row_sha256"],
        "C68_structural_task_row_sha256": row["C68_structural_task_row_sha256"],
        "C69c_blocker_row_sha256": row["C69c_blocker_row_sha256"],
        "pair_index": row["pair_index"],
        "source_path": row["source_path"],
        "child_path": row["child_path"],
        "parent_volume_fraction": row["parent_volume_fraction"],
        "exact_representative_box": row["exact_representative_box"],
        "exact_reflected_box": row["exact_reflected_box"],
        "representative_origin_key": lineage["origin_key"],
        "representative_cell_id": lineage["representative_cell_id"],
        "C37_pair_row_sha256": lineage["C37_pair_row_sha256"],
        "C32_cell_row_sha256": lineage["C32_cell_row_sha256"],
        "active_candidates": lineage["active_candidates"],
        "frozen_collision1_owner": "W[1,0]",
        "required_collision1_outgoing_chart": "W",
        "legacy_structural_category": row["structural_category"],
        "legacy_route_witness": row["child_route_witness"],
        "diagnosis": "LEGACY_BROAD_SQRT_EXCEPTION_FALSE_POSITIVE__NOT_DELTA1_ZERO__NOT_SOURCE_P_ENDPOINT",
        "source_parameter_endpoint_guard": {
            "p_interval": row["exact_representative_box"]["p"],
            "strictly_inside_minus1_plus1": True,
            "s_interval": ["0", "0"],
        },
        "collision1_owner_evidence": {
            "Delta1_natural": ad_evidence(owner["Delta_natural"]),
            "Delta1_centered_mean_value": ad_evidence(owner["Delta"]),
            "four_distinct_tp_corners": corners,
            "eight_degenerate_s_lifted_corners_strict_positive": True,
            "sqrt_Delta1": ad_evidence(owner["radical"]),
            "ell1": ad_evidence(owner["ell"]),
            "near_root1": ad_evidence(owner["near"]),
            "far_root1": ad_evidence(owner["far"]),
        },
        "active_competitor_evidence": {
            "target": lineage["competitor"],
            "Delta_centered_mean_value": ad_evidence(competitor["Delta"]),
            "near_root": ad_evidence(competitor["near"]),
            "competitor_near_minus_owner_near": ad_evidence(order),
            "frozen_owner_is_strict_unique_first": True,
        },
        "outgoing_evidence": {
            "normal_x": ad_evidence(nx),
            "normal_y": ad_evidence(ny),
            "H1_natural_after_Delta_recenter": ad_evidence(h1),
            "H1_centered_mean_value": bounds(h1_centered),
            "H1_sign": "STRICT_NEGATIVE",
            "strict_outgoing_chart": chart,
            "required_chart": "W",
            "strict_chart_mismatch": True,
        },
        "allowed_exit_class": "STRICT_EXCLUSION",
        "disposition": "STRICT_EXCLUSION_COLLISION1_OUTGOING_CHART_MISMATCH",
        "complete_child_decision": True,
        "additional_dyadic_depth_used": 0,
        "blowup_or_endpoint_graph_required": False,
        "local_strict_terminal": True,
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
    })


def load_c72(path: Path) -> tuple[list[dict[str, Any]], str]:
    selected: list[dict[str, Any]] = []
    selection = hashlib.sha256()
    for row in iter_secure_gzip(
        path, EXPECTED_C72_LEDGER_SHA, EXPECTED_C72_LEDGER_SIZE,
        EXPECTED_C72_ROWS, EXPECTED_C72_SEQUENCE,
    ):
        if row.get("child_route_witness") != "SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED":
            continue
        category = row.get("structural_category")
        need(category in EXPECTED_REQUIRED_DECIDER
             and row.get("required_decider") == EXPECTED_REQUIRED_DECIDER[category]
             and row.get("child_route_classification")
             == "UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY"
             and row.get("formal_credit") == row.get("whole_parent_credit")
             == row.get("D02_gate_credit") == 0, "C72 broad-exception boundary")
        selected.append(row)
        selection.update((row["row_sha256"] + "\n").encode("ascii"))
    need(len(selected) == 1_163, "exact C72 broad-exception child count")
    census: dict[str, int] = {}
    for row in selected:
        category = row["structural_category"]
        census[category] = census.get(category, 0) + 1
    need(census == EXPECTED_BROAD_EXCEPTION_CATEGORY_CENSUS,
         "exact C72 broad-exception category census")
    return selected, selection.hexdigest()


def validate_lineage(c37_path: Path, c32_path: Path) -> None:
    pairs: dict[int, dict[str, Any]] = {}
    for row in iter_secure_gzip(
        c37_path, EXPECTED_C37_LEDGER_SHA, EXPECTED_C37_LEDGER_SIZE,
        EXPECTED_C37_ROWS, EXPECTED_C37_SEQUENCE,
    ):
        if row.get("pair_index") in PAIR_LINEAGE:
            pairs[row["pair_index"]] = row
    need(set(pairs) == set(PAIR_LINEAGE), "four C37 pair rows")
    for pair_index, expected in PAIR_LINEAGE.items():
        row = pairs[pair_index]
        need(row["row_sha256"] == expected["C37_pair_row_sha256"]
             and row["representative_cell_id"] == expected["representative_cell_id"]
             and row["representative_origin_key"] == expected["origin_key"],
             "C37 exact lineage:" + str(pair_index))

    cells: dict[str, dict[str, Any]] = {}
    wanted = {value["representative_cell_id"] for value in PAIR_LINEAGE.values()}
    for row in iter_secure_gzip(
        c32_path, EXPECTED_C32_LEDGER_SHA, EXPECTED_C32_LEDGER_SIZE,
        EXPECTED_C32_ROWS, EXPECTED_C32_SEQUENCE,
    ):
        if row.get("cell_id") in wanted:
            cells[row["cell_id"]] = row
    need(set(cells) == wanted, "four C32 cells")
    for pair_index, expected in PAIR_LINEAGE.items():
        row = cells[expected["representative_cell_id"]]
        need(row["row_sha256"] == expected["C32_cell_row_sha256"]
             and row["origin_key"] == expected["origin_key"]
             and row["gate3_chart"] == "W:E"
             and row["physical_slice"] == "s=0"
             and row["source_lineage"]["active_candidates"] == expected["active_candidates"],
             "C32 exact active lineage:" + str(pair_index))


def deterministic_gzip(lines: list[bytes]) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as stream:
        for line in lines:
            stream.write(line + b"\n")
    return buffer.getvalue()


def emit_new(path: Path, raw: bytes) -> tuple[int, ...]:
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
        0o444,
    )
    try:
        offset = 0
        while offset < len(raw):
            offset += os.write(descriptor, raw[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    replay = secure_bytes(path, sha_bytes(raw), len(raw))
    need(replay == raw and (not raw or replay[-1:] == raw[-1:]),
         "terminal-byte replay:" + path.name)
    return identity(path.lstat())


def result_validator(value: dict[str, Any]) -> None:
    verify_object(value, value.get("object_sha256", ""), "C73 result")
    need(value["status"] ==
         "PASS_1163_OF_1163_C39_BROAD_SQRT_EXCEPTION_WITNESSES_ARE_STRICT_POSITIVE_DELTA1__972_N_PLUS_191_S_OUTGOING_MISMATCH__STRICT_EXCLUSION__ZERO_GLOBAL_CREDIT",
         "result status")
    need(value["input_domain"] == {
        "C72_CHILD_ROUTE_WITNESS_SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED": 1_163},
         "result input domain")
    need(value["legacy_structural_category_census"]
         == EXPECTED_BROAD_EXCEPTION_CATEGORY_CENSUS, "result category census")
    need(value["decision_census"] == {
        "STRICT_EXCLUSION_COLLISION1_OUTGOING_CHART_MISMATCH": 1_163,
        "outgoing_chart_N": 972, "outgoing_chart_S": 191,
    }, "result census")
    need(value["strict_boundary"] == {
        "candidate_is_global_authority": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "global_unresolved_decrement": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }, "result strict boundary")


def self_test(base: dict[str, Any]) -> dict[str, Any]:
    attacks: dict[str, bool] = {}

    def attack(name: str, mutation: Callable[[dict[str, Any]], None]) -> None:
        body = copy.deepcopy(base)
        body.pop("object_sha256")
        mutation(body)
        candidate = close_object(body)
        try:
            result_validator(candidate)
        except Exception:
            attacks[name] = True
        else:
            attacks[name] = False

    attack("status", lambda value: value.__setitem__("status", "PASS"))
    attack("input_count", lambda value: value["input_domain"].__setitem__(
        "C72_CHILD_ROUTE_WITNESS_SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED", 1_162))
    attack("decision_count", lambda value: value["decision_census"].__setitem__(
        "STRICT_EXCLUSION_COLLISION1_OUTGOING_CHART_MISMATCH", 18))
    attack("chart_N", lambda value: value["decision_census"].__setitem__(
        "outgoing_chart_N", 14))
    attack("chart_S", lambda value: value["decision_census"].__setitem__(
        "outgoing_chart_S", 5))
    for field in ("formal_credit", "whole_parent_credit", "D02_gate_credit",
                  "global_unresolved_decrement"):
        attack(field, lambda value, key=field: value["strict_boundary"].__setitem__(key, 1))
    attack("authority", lambda value: value["strict_boundary"].__setitem__(
        "candidate_is_global_authority", True))
    attack("pointer_write", lambda value: value["strict_boundary"].__setitem__(
        "runtime_canonical_pointer_or_seal_writes", True))
    corrupted = copy.deepcopy(base)
    corrupted["object_sha256"] = "0" * 64
    try:
        result_validator(corrupted)
    except Exception:
        attacks["object_hash"] = True
    else:
        attacks["object_hash"] = False
    need(all(attacks.values()) and len(attacks) == 12, "producer self-test")
    return {
        "status": "PASS_12_OF_12_COHERENT_SCOPE_CENSUS_AND_CREDIT_ATTACKS_FAIL_CLOSED",
        "attack_count": 12,
        "attacks": attacks,
    }


def build(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.output).absolute()
    need(output.is_dir() and not any(output.iterdir()), "empty existing output stage")
    need(flint.__version__ == "0.9.0" and flint.__FLINT_VERSION__ == "3.6.0",
         "sealed flint versions")
    ctx.dps = 115
    ctx.prec = PRECISION_BITS
    ctx.threads = 1
    ctx.pretty = True
    ctx.unicode = False

    verify_a = secure_json(Path(args.c72_verification_a), EXPECTED_C72_VERIFICATION_SHA,
                           EXPECTED_C72_VERIFICATION_SIZE)
    verify_b = secure_json(Path(args.c72_verification_b), EXPECTED_C72_VERIFICATION_SHA,
                           EXPECTED_C72_VERIFICATION_SIZE)
    verify_object(verify_a, EXPECTED_C72_VERIFICATION_OBJECT, "C72 verification A")
    verify_object(verify_b, EXPECTED_C72_VERIFICATION_OBJECT, "C72 verification B")
    need(verify_a == verify_b and verify_a["all_134155_rows_exactly_rebuilt"] is True
         and verify_a["dual_isolated_candidate_byte_identity"]
         == {"ledger": True, "report": True, "result": True},
         "C72 dual independent verification")

    rows_a, selection_a = load_c72(Path(args.c72_a))
    rows_b, selection_b = load_c72(Path(args.c72_b))
    need(rows_a == rows_b and selection_a == selection_b, "dual C72 selected rows identical")
    validate_lineage(Path(args.c37_pairs), Path(args.c32_cells))

    decision_rows = [decide(row, PAIR_LINEAGE[row["pair_index"]]) for row in rows_a]
    pair_census: dict[str, int] = {}
    chart_census = {"N": 0, "S": 0}
    sequence = hashlib.sha256()
    for row in decision_rows:
        key = str(row["pair_index"])
        pair_census[key] = pair_census.get(key, 0) + 1
        chart = row["outgoing_evidence"]["strict_outgoing_chart"]
        chart_census[chart] += 1
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    need(pair_census == {"31": 431, "200": 180, "270": 11, "711": 541}
         and chart_census == {"N": 972, "S": 191}, "C73 v2 decision census")

    ledger_raw = deterministic_gzip([canonical(row) for row in decision_rows])
    ledger_descriptor = {
        "filename": LEDGER_NAME,
        "order": "C72_FILTERED_LEDGER_ORDER",
        "row_count": 1_163,
        "row_hash_line_sequence_sha256": sequence.hexdigest(),
        "sha256": sha_bytes(ledger_raw),
        "size": len(ledger_raw),
    }
    result_body: dict[str, Any] = {
        "schema": SCHEMA + ".result",
        "status": "PASS_1163_OF_1163_C39_BROAD_SQRT_EXCEPTION_WITNESSES_ARE_STRICT_POSITIVE_DELTA1__972_N_PLUS_191_S_OUTGOING_MISMATCH__STRICT_EXCLUSION__ZERO_GLOBAL_CREDIT",
        "producer_file_sha256": sha_bytes(SELF.read_bytes()),
        "numeric_context": {
            "precision_bits": PRECISION_BITS,
            "python_flint_version": flint.__version__,
            "flint_version": flint.__FLINT_VERSION__,
            "threads": 1,
        },
        "upstream_file_sha256": {
            "C72_dual_candidate_ledger": EXPECTED_C72_LEDGER_SHA,
            "C72_dual_independent_verification": EXPECTED_C72_VERIFICATION_SHA,
            "C37_reflection_pairs": EXPECTED_C37_LEDGER_SHA,
            "C32_compact_cells": EXPECTED_C32_LEDGER_SHA,
        },
        "upstream_object_sha256": {
            "C72_independent_verification": EXPECTED_C72_VERIFICATION_OBJECT,
        },
        "C72_selected_row_hash_line_sequence_sha256": selection_a,
        "input_domain": {
            "C72_CHILD_ROUTE_WITNESS_SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED": 1_163},
        "legacy_structural_category_census":
            EXPECTED_BROAD_EXCEPTION_CATEGORY_CENSUS,
        "pair_census": pair_census,
        "decision_census": {
            "STRICT_EXCLUSION_COLLISION1_OUTGOING_CHART_MISMATCH": 1_163,
            "outgoing_chart_N": 972,
            "outgoing_chart_S": 191,
        },
        "analytic_lemmas": {
            "legacy_label_is_broad_exception_not_a_Delta1_zero_proof": True,
            "centered_mean_value_formula": "f(B) subset f(c)+sum_i derivative_i(B)*(B_i-c_i)",
            "all_centered_Delta1_enclosures_strict_positive": True,
            "all_four_distinct_tp_corners_and_eight_degenerate_s_lifts_strict_positive": True,
            "sqrt_Delta1_is_analytic_on_every_complete_child": True,
            "frozen_W10_near_root_strict_future_and_before_only_active_competitor": True,
            "H1_equals_nx_squared_minus_ny_squared_strict_negative": True,
            "strict_normal_y_sign_selects_N_or_S_never_required_W": True,
            "no_dyadic_refinement_or_endpoint_blowup_used": True,
        },
        "ledger": ledger_descriptor,
        "strict_boundary": {
            "candidate_is_global_authority": False,
            "formal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
            "global_unresolved_decrement": 0,
            "runtime_canonical_pointer_or_seal_writes": False,
        },
    }
    provisional = close_object(result_body)
    result_body["producer_self_test"] = self_test(provisional)
    result = close_object(result_body)
    result_validator(result)
    result_raw = canonical(result) + b"\n"
    report_raw = (
        "# C73 recentered collision-one H1 strict-exclusion oracle\n\n"
        "All 1,163 C72 children carrying child witness "
        "`SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED` are false positives "
        "of C39's broad exception handler. A 384-bit centered mean-value enclosure "
        "proves `Delta1 > 0` on every complete child. The recentered square root "
        "is therefore analytic; W[1,0] is the strict first hit, but the outgoing "
        "chart is N for 972 children and S for 191, never the frozen required W.\n\n"
        "Disposition: 1,163/1,163 `STRICT_EXCLUSION_COLLISION1_OUTGOING_CHART_MISMATCH`. "
        "No additional dyadic depth, endpoint graph, blow-up coordinate, formal "
        "credit, D02 credit, authority update, canonical pointer, or seal is used.\n"
    ).encode("utf-8")

    publication: list[str] = []
    emit_new(output / LEDGER_NAME, ledger_raw); publication.append(LEDGER_NAME)
    emit_new(output / RESULT_NAME, result_raw); publication.append(RESULT_NAME)
    emit_new(output / REPORT_NAME, report_raw); publication.append(REPORT_NAME)
    manifest_lines = [
        f"{sha_bytes((output / name).read_bytes())}  {name}\n"
        for name in sorted(publication)
    ]
    manifest_raw = "".join(manifest_lines).encode("ascii")
    emit_new(output / MANIFEST_NAME, manifest_raw); publication.append(MANIFEST_NAME)
    outer = close_object({
        "schema": SCHEMA + ".outer-publication-receipt",
        "status": "PASS_OUTER_RECEIPT_LAST__ALL_C73_STAGE_MEMBERS_TERMINAL_BYTE_REPLAYED",
        "result_object_sha256": result["object_sha256"],
        "manifest_sha256": sha_bytes(manifest_raw),
        "member_file_sha256": {
            name: sha_bytes((output / name).read_bytes()) for name in publication
        },
        "publication_order": publication + [OUTER_NAME],
        "outer_receipt_published_last": True,
        "formal_credit": 0,
        "D02_gate_credit": 0,
    })
    outer_raw = canonical(outer) + b"\n"
    emit_new(output / OUTER_NAME, outer_raw)
    publication.append(OUTER_NAME)
    for name in publication:
        raw = (output / name).read_bytes()
        need(secure_bytes(output / name, sha_bytes(raw), len(raw)) == raw,
             "postpublication replay:" + name)
    return {
        "status": "PASS_C73_STAGE_BUILT_AND_REPLAYED",
        "output": str(output),
        "result_object_sha256": result["object_sha256"],
        "ledger_sha256": ledger_descriptor["sha256"],
        "manifest_sha256": sha_bytes(manifest_raw),
        "outer_receipt_sha256": sha_bytes(outer_raw),
        "publication_order": publication,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--output", required=True)
    value.add_argument("--c72-a", default=str(DEFAULT_C72_A))
    value.add_argument("--c72-b", default=str(DEFAULT_C72_B))
    value.add_argument("--c72-verification-a", default=str(DEFAULT_C72_VERIFY_A))
    value.add_argument("--c72-verification-b", default=str(DEFAULT_C72_VERIFY_B))
    value.add_argument("--c37-pairs", default=str(DEFAULT_C37))
    value.add_argument("--c32-cells", default=str(DEFAULT_C32))
    return value


def main() -> int:
    try:
        outcome = build(parser().parse_args())
    except Exception as error:
        print(json.dumps({"status": "REJECTED", "error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps(outcome, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
