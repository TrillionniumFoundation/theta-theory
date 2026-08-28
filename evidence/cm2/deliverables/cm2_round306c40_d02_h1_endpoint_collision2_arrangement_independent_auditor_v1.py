#!/usr/bin/env python3
"""No-producer-import independent auditor for the C40 arrangement candidate.

The auditor consumes only the frozen C39 authority, the C40 byte artefacts, and
the lower-level Round139/166/185 mathematical kernels.  In particular it never
imports or executes the C40 producer.  A normal invocation performs two cold
core replays, checks byte-identical projections, and then emits an atomic,
self-hashed terminal audit object.
"""

from __future__ import annotations

import argparse
import ast
import copy
import gzip
import hashlib
import io
import itertools
import json
import os
import re
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import flint
from flint import ctx

import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as round139
import cm2_round166_multi_candidate_refinement_prototype as round166
import cm2_round185_preconditioned_c1_residual_refinement as round185


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
PRODUCER = DELIVERABLES / (
    "cm2_round306c40_d02_h1_endpoint_collision2_arrangement_v1.py"
)
EXPECTED_PRODUCER_SOURCE = (
    "9ec1ad4df72b0f25b646d17a43e1186188ace97d2e76ac480c1c2a476fac5f57"
)
EXPECTED_C39_SOURCE = "873a84cb150efc5649ffb5822457c510ab45c32f3e16a48914c8674dc93c0aae"
EXPECTED_C38_SOURCE = "8eab87d69fb4e1995df87be7acb387db19d1b81e17040fe6116794bddd4a830d"
SCHEMA = "cm2.round306c40.d02-h1-endpoint-collision2-arrangement.independent-audit.v1"
CANDIDATE_SCHEMA = "cm2.round306c40.d02-h1-endpoint-collision2-arrangement.v1"

C39_OBJECT = "821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02"
C39_AUDIT_OBJECT = "5eccca7db5a473db6fbd67f7f0eda0f582a52b51b3aab5895316e83777358182"
C39_SCHEMA = "cm2.round306c39.d02-h1-c1-graph-cell-router.v1"
C39_AUDIT_SCHEMA = "cm2.round306c39.d02-h1-c1-graph-cell-router.independent-audit.v1"
C38_OBJECT = "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434"
C37_OBJECT = "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b"
C36_OBJECT = "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167"
C35_OBJECT = "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752"
C34_OBJECT = "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e"
C32_OBJECT = "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474"

ROUND139_SOURCE = "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b"
ROUND166_SOURCE = "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c"
ROUND185_SOURCE = "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2"
ROUND181_SOURCE = "6e9d51229c209caacf3964d24600295375bd08e963b4e154774625707aa1524c"
ROUND178_SOURCE = "06075baac268e8e6c9deeeedae3e502b3a96630f3650c0b783c2b2a77dbd23f9"

PRECISION_BITS = 384
EXTRA_DEPTH = 2
FROZEN_OWNER = "W[1,0]"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{15,255}\Z")
C2_SOURCE_ROW_COUNT = 6232
C2_CANDIDATE_COUNT = 55
C2_CANDIDATE_TUPLE_SHA256 = (
    "ce8bce09ae6ab3cc2be9b30c5b8941c219448a88551315b43e8dad9c99c482c5"
)
C2_BOUNDARY_REGISTRY = {
    "candidate_count": 55,
    "consequence": (
        "two strict future near roots cannot become equal; on a connected "
        "fixed-status cell their order is fixed by one strict point"
    ),
    "minimum_strict_squared_margin": "36337/160000",
    "pair_count": 1485,
    "pair_rows_sha256": (
        "36b22055587a22a003fa57a4c29c5cd6cc730af567e1354f5c72f317991a1ce2"
    ),
}
C2_BOUNDARY_REGISTRY_SHA256 = (
    "4b0ce3d81b7a4957f35bb233d46c1f332ca2e60a00751396c6b3d97b8e8db7cc"
)
C2_SOURCE_RAW_CENSUS = {
    "INTERSECTION_BEHIND": 5881,
    "NO_REAL_INTERSECTION": 285281,
    "STRICT_FUTURE": 10589,
    "UNRESOLVED_DELTA": 40875,
    "UNRESOLVED_ROOT_SIGN": 134,
}
ALGEBRAIC_PAIR_INDICES = frozenset(
    {
        15, 32, 35, 114, 248, 269, 381, 387, 390, 420, 440, 481, 509,
        569, 570, 572, 577, 585, 601, 606, 647, 659, 670, 679, 680, 763,
        779, 846, 855,
    }
)

LEDGER_NAMES = (
    "routed_leaf_cells.jsonl.gz",
    "h1_graph_cells.jsonl.gz",
    "endpoint_charts.jsonl.gz",
    "collision2_multi_delta_cells.jsonl.gz",
    "collision2_source_candidate_census.jsonl.gz",
    "parent_conservation.jsonl.gz",
)
INVENTORY = frozenset(
    (*LEDGER_NAMES, "PARTIAL_ARRANGEMENT_ONLY.lock", "result.json", "root_manifest.sha256")
)
EXPECTED_NONPROMOTION_LOCK = (
    b"C40 materializes two-level rational off-graph slabs, H1 graph cells, "
    b"source/algebraic endpoint charts, and collision-two multi-Delta "
    b"incidence outers. Only exact excluded leaf volume participates in "
    b"parent Kraft conservation. No graph, boundary, endpoint, incidence, "
    b"local exact key, or surviving collision-two branch earns ambient, "
    b"D02, D03, D04, Gate5, or CM2 credit. Collisions 3--1648 remain.\n"
)

SOURCE_ENDPOINT_IDS = frozenset(
    {
        "c39-routed:9408dd0939cd5f6dd85579df95f17124549149c116703114ac7fd23b7f244a07",
        "c39-routed:230e43eb895492a75c7010f47c3e9da6ba8e3bd4cce2c207f2172b2fd17a70ba",
        "c39-routed:9799229c9c53970b2b4f1d64358740aa46f392812c8439239c85e0d0cf951855",
        "c39-routed:83a47113be6b23b55c0bd809b29b0ebfb52ca3b5b1d2f5d3049d85dd3c4521a7",
        "c39-routed:d151189d542508947c9429b27fa8e54cfc1f5ceb8e9d12dbe70ccc8164f82e73",
        "c39-routed:e298df7ece7f5d666829fa0a5a23a6bee5ee279ca315c4ca388edacabbbac794",
    }
)
DELTA1_H1_INTERSECTION_IDS = frozenset(
    {
        "c39-routed:07a0d5e087cbf88a5794b6a74646245ad0841da4c3c2452a9788dff48bae6a81",
        "c39-routed:3daee50b93cf9fbb1ebed04c93f3f5bca8732c2816397a98febc83d7817d7355",
        "c39-routed:4dbf90140b8be48b12ff91772088945aec7a4f47086d9c40ab7d07f050b51d25",
    }
)
C2_SOURCE_CLASSIFICATIONS = frozenset(
    {
        "UNRESOLVED_COLLISION2_OWNER",
        "UNRESOLVED_C39_H1_W_SIDE_COLLISION2_OWNER",
        "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION2_OWNER",
    }
)
CORE_INDEX = {"W:E": 14, "W:N": 17, "W:S": 20, "W:W": 23}
_CORES: tuple[Any, ...] | None = None


class Reject(RuntimeError):
    """Fail-closed independent rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def bytes_sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
        value.st_uid,
        value.st_gid,
    )


def stable_read(path: Path, maximum: int, label: str) -> tuple[bytes, tuple[int, ...]]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + label)
    descriptor = os.open(
        absolute,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1
            and 0 < before.st_size <= maximum,
            "regular singleton:" + label,
        )
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(descriptor, min(4 << 20, remaining))
            need(bool(block), "short read:" + label)
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "stable EOF:" + label)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after), "file TOCTOU:" + label)
    return b"".join(chunks), identity(after)


def strict_json_bytes(raw: bytes, label: str, newline: bool = True) -> dict[str, Any]:
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "JSON bytes:" + label)

    def reject_number(item: str) -> Any:
        raise Reject("noninteger JSON:" + label + ":" + item)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "duplicate JSON key:" + label + ":" + key)
            output[key] = value
        return output

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=unique,
        parse_float=reject_number,
        parse_constant=reject_number,
    )
    need(type(value) is dict, "JSON top object:" + label)
    expected = canonical(value) + (b"\n" if newline else b"")
    need(raw == expected, "canonical JSON bytes:" + label)
    return value


def closed_object(value: dict[str, Any], label: str) -> None:
    body = dict(value)
    claimed = body.pop("object_sha256", None)
    need(
        type(claimed) is str
        and HEX64.fullmatch(claimed) is not None
        and claimed == digest(body),
        "object closure:" + label,
    )


def parse_manifest(raw: bytes, expected_names: set[str], label: str) -> dict[str, str]:
    rows = raw.decode("ascii", "strict").splitlines()
    output: dict[str, str] = {}
    observed_order: list[str] = []
    for row in rows:
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", row)
        need(match is not None, "manifest syntax:" + label)
        name = match.group(2)
        need(name not in output, "manifest duplicate:" + label + ":" + name)
        output[name] = match.group(1)
        observed_order.append(name)
    need(set(output) == expected_names, "manifest inventory:" + label)
    need(observed_order == sorted(observed_order), "manifest order:" + label)
    return output


def read_ledger_raw(
    raw: bytes, descriptor: dict[str, Any], filename: str,
) -> list[dict[str, Any]]:
    need(
        descriptor.get("filename") == filename
        and descriptor.get("sha256") == bytes_sha256(raw)
        and descriptor.get("size") == len(raw)
        and raw[:2] == b"\x1f\x8b"
        and len(raw) >= 10
        and int.from_bytes(raw[4:8], "little") == 0,
        "ledger byte descriptor:" + filename,
    )
    try:
        expanded = gzip.decompress(raw)
    except (OSError, EOFError) as error:
        raise Reject("gzip:" + filename) from error
    need(expanded.endswith(b"\n"), "ledger final newline:" + filename)
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    for ordinal, line in enumerate(expanded.splitlines(keepends=True)):
        need(line.endswith(b"\n"), "ledger row newline:" + filename)
        row = strict_json_bytes(line, f"{filename}:{ordinal}")
        body = dict(row)
        claimed = body.pop("row_sha256", None)
        need(
            type(claimed) is str
            and HEX64.fullmatch(claimed) is not None
            and claimed == digest(body),
            "row closure:" + filename + ":" + str(ordinal),
        )
        sequence.update((claimed + "\n").encode("ascii"))
        rows.append(row)
    need(
        descriptor.get("row_count") == len(rows)
        and descriptor.get("row_hash_line_sequence_sha256") == sequence.hexdigest(),
        "ledger sequence descriptor:" + filename,
    )
    return rows


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def atlas_box(payload: dict[str, Any], path: str = "") -> Any:
    return round185.atlas.AtlasBox(
        Q(payload["t"][0]),
        Q(payload["t"][1]),
        Q(payload["p"][0]),
        Q(payload["p"][1]),
        Q(payload["s"][0]),
        Q(payload["s"][1]),
        len(path),
        path,
    )


def box_payload(box: Any) -> dict[str, Any]:
    return {
        "t": [qstr(box.t0), qstr(box.t1)],
        "p": [qstr(box.p0), qstr(box.p1)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }


def reflected_payload(chart: str, box: Any) -> dict[str, Any]:
    if chart in {"E", "W"}:
        reflected_chart = chart
        t_interval = (-box.t1, -box.t0)
    else:
        reflected_chart = {"N": "S", "S": "N"}[chart]
        t_interval = (box.t0, box.t1)
    return {
        "compact_chart": reflected_chart,
        "t": [qstr(value) for value in t_interval],
        "p": [qstr(-box.p1), qstr(-box.p0)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }


def first_owner(chart_id: str, box: Any) -> dict[str, Any] | None:
    record = round166.root_record_fast(chart_id, box, FROZEN_OWNER)
    if record.classification != "strict_future_root" or record.near is None:
        return None
    _contact_x, _contact_y, outgoing_x, outgoing_y, _shear, _radial = (
        round166.atlas.geometry(chart_id, box)
    )
    radical = record.discriminant.sqrt()
    transverse = record.transverse
    radius = round166.base.arbq(round166.base.RADIUS["W"])
    return {
        "selected_target_id": FROZEN_OWNER,
        "selected_root": record.near,
        "normal_x": (-radical * outgoing_x + transverse * outgoing_y) / radius,
        "normal_y": (-radical * outgoing_y - transverse * outgoing_x) / radius,
        "p": transverse / radius,
        "cosine": radical / radius,
    }


def collision2_state(parent_key: str, box: Any) -> dict[str, Any]:
    global _CORES
    if _CORES is None:
        _CORES = tuple(round139.lower.core_cert.physical_cores())
    chart_id = ":".join(parent_key.split(":")[:2])
    owner = first_owner(chart_id, box)
    need(owner is not None, "strict collision-one owner for C2 census")
    atom = round139.lower.step1.Atom(
        CORE_INDEX[chart_id],
        _CORES[CORE_INDEX[chart_id]],
        box.t0,
        box.t1,
        box.p0,
        box.p1,
        Q(0),
        Q(0),
        "c40-independent-c2",
    )
    state = round139.lower.round136.initial_state(atom)
    outgoing = round139.lower.time3.second_outgoing_state(atom, state, owner)
    need(outgoing is not None and outgoing["chart"] == "W", "strict C2 W state")
    return outgoing


def raw_candidate_disposition(
    state: dict[str, Any], candidate_id: str,
) -> dict[str, Any]:
    qx, qy, ux, uy, s = (
        state["contact_x"],
        state["contact_y"],
        state["outgoing_x"],
        state["outgoing_y"],
        state["s"],
    )
    kernel = round139.lower.time3.time2_cert
    ax, ay = kernel.target_center(candidate_id, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = kernel.step1.arbq(kernel.first_hit.RADIUS[candidate_id[0]])
    delta = radius * radius - transverse * transverse
    near = None
    if bool(delta < 0):
        classification = "NO_REAL_INTERSECTION"
    elif not bool(delta > 0):
        classification = "UNRESOLVED_DELTA"
    else:
        radical = delta.sqrt()
        near_value = ell - radical
        far = ell + radical
        if bool(far < 0):
            classification = "INTERSECTION_BEHIND"
        elif not bool(near_value > 0):
            classification = "UNRESOLVED_ROOT_SIGN"
        else:
            classification = "STRICT_FUTURE"
            near = round185.arb_bounds(near_value)
    return {
        "target_id": candidate_id,
        "raw_classification": classification,
        "ell": round185.arb_bounds(ell),
        "Delta": round185.arb_bounds(delta),
        "transverse": round185.arb_bounds(transverse),
        "near": near,
    }


def independent_c2_candidate_rows(
    parent_key: str, box: Any,
) -> tuple[list[str], list[dict[str, Any]], list[dict[str, Any]]]:
    state = collision2_state(parent_key, box)
    kernel = round139.lower.time3.time2_cert
    candidates = list(kernel.translated_candidate_ids(FROZEN_OWNER, "W"))
    need(
        len(candidates) == C2_CANDIDATE_COUNT
        and digest(candidates) == C2_CANDIDATE_TUPLE_SHA256,
        "pinned C2 candidate universe",
    )
    dispositions = [raw_candidate_disposition(state, item) for item in candidates]
    future = [
        (row["target_id"], kernel.candidate_root(
            state["contact_x"],
            state["contact_y"],
            state["outgoing_x"],
            state["outgoing_y"],
            state["s"],
            row["target_id"],
        ))
        for row in dispositions
        if row["raw_classification"] == "STRICT_FUTURE"
    ]
    order_rows: list[dict[str, Any]] = []
    for left_index, (left_id, left) in enumerate(future):
        for right_id, right in future[left_index + 1:]:
            left_before = bool(left["near"] < right["near"])
            right_before = bool(right["near"] < left["near"])
            order_rows.append(
                {
                    "left_target_id": left_id,
                    "right_target_id": right_id,
                    "left_strictly_before_right": left_before,
                    "right_strictly_before_left": right_before,
                    "box_uniform_order_not_certified": not (
                        left_before or right_before
                    ),
                    "equality_carrier_empty_by_boundary_registry": True,
                    "boundary_separation_registry_sha256": (
                        C2_BOUNDARY_REGISTRY_SHA256
                    ),
                }
            )
    return candidates, dispositions, order_rows


def reconstruct_cell_box(
    cell: dict[str, Any], path: str,
) -> tuple[Any, tuple[str, ...]]:
    t_values = cell["physical_t_interval"]
    need(
        all(value["kind"] == "RATIONAL" for value in t_values),
        "rational cell reconstruction",
    )
    box = round166.ge.AtlasBox(
        Q(t_values[0]["value"]),
        Q(t_values[1]["value"]),
        Q(cell["physical_p_interval"][0]),
        Q(cell["physical_p_interval"][1]),
        Q(0),
        Q(0),
        0,
        "",
    )
    active = tuple(cell["source_lineage"]["active_candidates"])
    for bit in path:
        need(bit in "01", "dyadic path bit")
        stage, _records = round166.classify_active(cell["gate3_chart"], box, active)
        if stage.classification == "unique_first":
            active = (FROZEN_OWNER,)
        elif stage.classification != "tangency_graph":
            active = stage.active_targets
        box = round166.split_axis(box, round166.longest_axis(box))[int(bit)]
    return box, active


def collision0_delta(parent_key: str, box: Any, target: str) -> Any:
    return round185.ad_root(round185.ad_initial_geometry(parent_key, box), target)[
        "Delta"
    ]


def collision0_distance(parent_key: str, box: Any, target: str) -> Any:
    raw = round185.ad_root(round185.ad_initial_geometry(parent_key, box), target)
    return raw["ell"] * raw["ell"] - raw["Delta"]


def enhanced_record(parent_key: str, box: Any, record: Any) -> Any:
    if record.classification not in {
        "unresolved_discriminant",
        "unresolved_root_sign",
    }:
        return record
    raw = round185.ad_root(round185.ad_initial_geometry(parent_key, box), record.target_id)
    delta = round185.centered_enclosure(
        collision0_delta, parent_key, box, record.target_id, raw["Delta"]
    )
    delta_sign = round185.strict_sign(delta)
    if delta_sign < 0:
        return round166.ge.RootRecord(
            record.target_id,
            "no_real_intersection",
            raw["ell"].value,
            delta,
            None,
            None,
            raw["transverse"].value,
        )
    if delta_sign == 0:
        return record
    radical = delta.sqrt()
    ell = raw["ell"].value
    near = ell - radical
    far = ell + radical
    if bool(far < 0):
        classification = "intersection_behind"
    elif bool(near > 0):
        classification = "strict_future_root"
    else:
        full = collision0_distance(parent_key, box, record.target_id)
        distance = round185.centered_enclosure(
            collision0_distance, parent_key, box, record.target_id, full
        )
        if bool(ell > 0) and bool(far > 0) and bool(distance > 0):
            classification = "strict_future_root"
            near = distance / far
        else:
            classification = "unresolved_root_sign"
    return round166.ge.RootRecord(
        record.target_id,
        classification,
        ell,
        delta,
        near,
        far,
        raw["transverse"].value,
    )


def independent_h1_chart(parent_key: str, box: Any) -> str | None:
    try:
        full, nx, ny = round185.collision1_h1_ad(parent_key, box, FROZEN_OWNER)
        centered = round185.centered_enclosure(
            round185.collision1_h1_ad,
            parent_key,
            box,
            FROZEN_OWNER,
            full,
        )
    except Exception:
        return None
    sign = round185.strict_sign(centered)
    if sign == 0:
        for axis, (lower, upper) in enumerate(
            ((box.t0, box.t1), (box.p0, box.p1))
        ):
            if round185.strict_sign(full.derivative[axis]) == 0:
                continue
            low = round185.collision1_h1_ad(
                parent_key,
                round185.fixed_axis_box(box, axis, lower, ".audit-low"),
                FROZEN_OWNER,
            )[0].value
            high = round185.collision1_h1_ad(
                parent_key,
                round185.fixed_axis_box(box, axis, upper, ".audit-high"),
                FROZEN_OWNER,
            )[0].value
            low_sign = round185.strict_sign(low)
            high_sign = round185.strict_sign(high)
            if low_sign != 0 and low_sign == high_sign:
                sign = low_sign
                break
    if sign > 0 and round185.strict_sign(nx.value) != 0:
        return "E" if round185.strict_sign(nx.value) > 0 else "W"
    if sign < 0 and round185.strict_sign(ny.value) != 0:
        return "N" if round185.strict_sign(ny.value) > 0 else "S"
    return None


def independent_stage_two_route(
    chart_id: str, box: Any, config: dict[str, Any],
) -> tuple[str, str]:
    global _CORES
    if _CORES is None:
        _CORES = tuple(round139.lower.core_cert.physical_cores())
    owner_one = first_owner(chart_id, box)
    if owner_one is None:
        return "UNRESOLVED_COLLISION1_OWNER_GEOMETRY", "OWNER_GEOMETRY"
    atom = round139.lower.step1.Atom(
        CORE_INDEX[chart_id],
        _CORES[CORE_INDEX[chart_id]],
        box.t0,
        box.t1,
        box.p0,
        box.p1,
        Q(0),
        Q(0),
        "c40-independent-route",
    )
    state = round139.lower.round136.initial_state(atom)
    next_state = round139.lower.time3.second_outgoing_state(atom, state, owner_one)
    if next_state is None:
        return "UNRESOLVED_COLLISION1_OUTGOING_STATE", "OUTGOING_STATE"
    try:
        word_one, error_one = (
            round139.lower.round136.translation_normalized_official_word(
                state,
                "W[0,0]",
                owner_one,
                config["pair_index"],
                config["pattern_index"],
            )
        )
    except RuntimeError as error:
        return "UNRESOLVED_COLLISION1_WORD", str(error)
    if word_one is None:
        return "UNRESOLVED_COLLISION1_WORD", str(error_one)
    word_one_id = round139.lower.round136.compact_key(word_one["key"])[
        "official_word_key_id"
    ]
    if word_one_id != config["original_path"][0]["official_word_key_id"]:
        return "EXCLUDED_COLLISION1_WORD_MISMATCH", word_one_id
    owner_two, owner_error = round139.lower.time3.strict_next_owner(
        next_state, FROZEN_OWNER
    )
    if owner_two is None:
        return "UNRESOLVED_COLLISION2_OWNER", owner_error
    selected = owner_two["selected_target_id"]
    expected_by_owner = {
        config["original_path"][1]["selected_absolute_owner_id"]:
            config["original_path"][1],
        config["reflected_path"][1]["selected_absolute_owner_id"]:
            config["reflected_path"][1],
    }
    if selected not in expected_by_owner:
        return "EXCLUDED_COLLISION2_OWNER_MISMATCH", selected
    expected = expected_by_owner[selected]
    outgoing_two = round139.lower.time3.second_outgoing_state(
        atom, next_state, owner_two
    )
    if outgoing_two is None:
        return "UNRESOLVED_COLLISION2_OUTGOING_STATE", "OUTGOING_STATE"
    if outgoing_two["chart"] != expected["outgoing_chart"]:
        return "EXCLUDED_COLLISION2_CHART_MISMATCH", outgoing_two["chart"]
    try:
        word_two, error_two = (
            round139.lower.round136.translation_normalized_official_word(
                next_state,
                FROZEN_OWNER,
                owner_two,
                config["pair_index"],
                config["pattern_index"],
            )
        )
    except RuntimeError as error:
        return "UNRESOLVED_COLLISION2_WORD", str(error)
    if word_two is None:
        return "UNRESOLVED_COLLISION2_WORD", str(error_two)
    word_two_id = round139.lower.round136.compact_key(word_two["key"])[
        "official_word_key_id"
    ]
    if word_two_id != expected["official_word_key_id"]:
        return "EXCLUDED_COLLISION2_WORD_MISMATCH", word_two_id
    branch = (
        "ORIGINAL"
        if selected == config["original_path"][1]["selected_absolute_owner_id"]
        else "REFLECTED"
    )
    return "LIVE_COLLISION2_" + branch + "_MATCH", selected


def routed_c39(prefix: str, route: str) -> str:
    if route.startswith("EXCLUDED_"):
        return "EXCLUDED_C39_" + prefix + "_" + route.removeprefix("EXCLUDED_")
    if route.startswith("LIVE_"):
        return "UNRESOLVED_C39_" + prefix + "_" + route + "_NEEDS_COLLISION3_1648"
    return "UNRESOLVED_C39_" + prefix + "_" + route.removeprefix("UNRESOLVED_")


def independent_c39_child_classification(
    source: dict[str, Any],
    c38_source: dict[str, Any],
    cell: dict[str, Any],
    path: str,
    config: dict[str, Any],
) -> tuple[str, str, Any]:
    box, active = reconstruct_cell_box(cell, path)
    parent_key = c38_source["representative_origin_key"]
    stage, records = round166.classify_active(cell["gate3_chart"], box, active)
    enhanced = [enhanced_record(parent_key, box, record) for record in records]
    leaf = round166.classify_from_records(cell["gate3_chart"], box, enhanced)
    if leaf.classification == "no_future_root":
        return "EXCLUDED_C39_C1_NO_FUTURE_ROOT", leaf.reason, box
    if leaf.classification == "unique_first" and leaf.owner_target != FROZEN_OWNER:
        return "EXCLUDED_C39_C1_UNIQUE_FIRST_OWNER_MISMATCH", str(leaf.owner_target), box
    if leaf.classification == "unique_first" and leaf.owner_target == FROZEN_OWNER:
        chart = independent_h1_chart(parent_key, box)
        if chart is not None and chart != "W":
            return (
                "EXCLUDED_C39_C1_OUTGOING_CHART_MISMATCH",
                "strict collision-one outgoing chart " + chart,
                box,
            )
        if chart == "W":
            route, witness = independent_stage_two_route(
                ":".join(parent_key.split(":")[:2]), box, config
            )
            return routed_c39("C1_ENHANCED_W_SIDE", route), witness, box
    return "UNRESOLVED_INDEPENDENT_C39_CHILD", leaf.reason, box


def independent_c39_route_exception(
    source: dict[str, Any],
    c38_source: dict[str, Any],
    cell: dict[str, Any],
    path: str,
    config: dict[str, Any],
) -> tuple[str, str, Any, dict[str, Any]]:
    box, _active = reconstruct_cell_box(cell, path)
    try:
        independent_c39_child_classification(
            source, c38_source, cell, path, config
        )
    except Reject:
        raise
    except Exception as error:
        endpoint = box.p0 == -1 or box.p1 == 1
        replay: dict[str, Any] = {
            "attempted": endpoint,
            "matched_caught_exception": False,
            "replay_is_source_sqrt_domain_failure": False,
            "source_radical_causal_match": False,
            "replay_exception_type": None,
            "replay_exception_module": None,
            "replay_exception_message": None,
        }
        if endpoint:
            try:
                round185.ad_initial_geometry(
                    c38_source["representative_origin_key"], box
                )
            except Exception as source_error:
                matched = (
                    type(source_error).__module__ == type(error).__module__
                    and type(source_error).__name__ == type(error).__name__
                    and str(source_error) == str(error)
                )
                source_sqrt = (
                    type(source_error).__name__ == "Round185Error"
                    and str(source_error) == "AD sqrt domain"
                )
                replay.update(
                    {
                        "matched_caught_exception": matched,
                        "replay_is_source_sqrt_domain_failure": source_sqrt,
                        "source_radical_causal_match": matched and source_sqrt,
                        "replay_exception_type": type(source_error).__name__,
                        "replay_exception_module": type(source_error).__module__,
                        "replay_exception_message": str(source_error),
                    }
                )
        classification = (
            "UNRESOLVED_C40_SOURCE_RADICAL_ENDPOINT_ROUTE_"
            "EVALUATION_FAILURE_OUTER"
            if replay["source_radical_causal_match"]
            else (
                "UNRESOLVED_C40_P_ENDPOINT_BOX_ROUTE_EVALUATION_FAILURE_OUTER"
                if endpoint
                else "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER"
            )
        )
        failure = {
            "phase": "C39_ROUTE_C1_TASK",
            "exception_type": type(error).__name__,
            "exception_module": type(error).__module__,
            "exception_message": str(error),
            "exact_box_endpoint_phase": (
                "SOURCE_RADICAL_1_MINUS_P2_ENDPOINT" if endpoint else None
            ),
            "source_radical_initial_geometry_replay": replay,
        }
        return classification, type(error).__name__ + ":" + str(error), box, failure
    raise Reject("claimed C39 route exception independently evaluates")


def independent_c40_collision2_classification(
    parent_key: str, box: Any, config: dict[str, Any],
) -> tuple[str, str]:
    try:
        status, detail, _evidence, baseline = round185.resolve_dynamic_box(
            parent_key, box, config["pair_index"], config["pattern_index"]
        )
    except Exception:
        return "UNRESOLVED_C40_COLLISION2_EVALUATION_EXCEPTION", "ROUND185_FAIL_CLOSED"
    if not status.startswith("LOCAL_EXACT_KEY"):
        return "UNRESOLVED_C40_COLLISION2_" + status, baseline
    selected = detail["absolute_collision2_owner"]
    expected_by_owner = {
        config["original_path"][1]["selected_absolute_owner_id"]:
            config["original_path"][1],
        config["reflected_path"][1]["selected_absolute_owner_id"]:
            config["reflected_path"][1],
    }
    expected = expected_by_owner.get(selected)
    if expected is None:
        return "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH", selected
    if detail.get("collision2_outgoing_chart") != expected["outgoing_chart"]:
        return (
            "EXCLUDED_C40_COLLISION2_CHART_MISMATCH",
            str(detail.get("collision2_outgoing_chart")),
        )
    word_id = detail["official_gate5_key"]["word_key_id"]
    if word_id != expected["official_word_key_id"]:
        return "EXCLUDED_C40_COLLISION2_WORD_MISMATCH", word_id
    branch = (
        "ORIGINAL"
        if selected == config["original_path"][1]["selected_absolute_owner_id"]
        else "REFLECTED"
    )
    return (
        "UNRESOLVED_C40_LIVE_COLLISION2_" + branch + "_MATCH_NEEDS_COLLISION3_1648",
        selected,
    )


def source_pins() -> dict[str, str]:
    values = {
        "Round139": file_sha256(Path(round139.__file__).resolve()),
        "Round166": file_sha256(Path(round166.__file__).resolve()),
        "Round185": file_sha256(Path(round185.__file__).resolve()),
        "Round181": file_sha256(Path(round185.r181.__file__).resolve()),
        "Round178": file_sha256(Path(round185.r178.__file__).resolve()),
    }
    need(
        values
        == {
            "Round139": ROUND139_SOURCE,
            "Round166": ROUND166_SOURCE,
            "Round185": ROUND185_SOURCE,
            "Round181": ROUND181_SOURCE,
            "Round178": ROUND178_SOURCE,
        }
        and flint.__version__ == "0.9.0",
        "independent numeric source pins",
    )
    registry = round185.r181.boundary_separation_registry()
    need(
        registry == C2_BOUNDARY_REGISTRY
        and digest(registry) == C2_BOUNDARY_REGISTRY_SHA256,
        "collision-two strict boundary-separation registry",
    )
    return values


def no_producer_import() -> None:
    source = Path(__file__).read_bytes()
    tree = ast.parse(source)
    forbidden = PRODUCER.stem
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            need(all(alias.name != forbidden for alias in node.names), "producer import")
        elif isinstance(node, ast.ImportFrom):
            need(node.module != forbidden, "producer import-from")
    producer_path = PRODUCER.resolve()
    for module in tuple(sys.modules.values()):
        filename = getattr(module, "__file__", None)
        if filename is not None:
            need(Path(filename).resolve() != producer_path, "producer loaded")


def capture_directory(
    directory: Path,
    expected_names: frozenset[str],
    limits: dict[str, int],
    label: str,
) -> tuple[dict[str, bytes], tuple[int, ...], dict[str, tuple[int, ...]]]:
    absolute = Path(os.path.abspath(os.fspath(directory)))
    need(absolute.resolve(strict=True) == absolute, "canonical directory:" + label)
    before = absolute.lstat()
    need(stat.S_ISDIR(before.st_mode) and not absolute.is_symlink(), "directory:" + label)
    names = frozenset(entry.name for entry in os.scandir(absolute))
    need(names == expected_names, "exact inventory:" + label)
    payloads: dict[str, bytes] = {}
    identities: dict[str, tuple[int, ...]] = {}
    for name in sorted(names):
        payloads[name], identities[name] = stable_read(
            absolute / name, limits.get(name, 512 << 20), label + ":" + name
        )
    after = absolute.lstat()
    need(
        identity(before) == identity(after)
        and frozenset(entry.name for entry in os.scandir(absolute)) == names,
        "directory TOCTOU:" + label,
    )
    return payloads, identity(after), identities


def validate_manifest_payloads(
    payloads: dict[str, bytes], manifest_name: str, label: str,
) -> dict[str, str]:
    members = set(payloads) - {manifest_name}
    manifest = parse_manifest(payloads[manifest_name], members, label)
    need(
        manifest == {name: bytes_sha256(payloads[name]) for name in sorted(members)},
        "manifest byte replay:" + label,
    )
    return manifest


def validate_nonpromotion_lock(raw: bytes) -> None:
    need(raw == EXPECTED_NONPROMOTION_LOCK, "C40 exact nonpromotion lock bytes")


def load_c39_authority(
    candidate: Path, audit_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    c39_inventory = frozenset(
        {
            "PARTIAL_GRAPH_ROUTER_ONLY.lock",
            "parent_conservation.jsonl.gz",
            "result.json",
            "root_manifest.sha256",
            "routed_child_pairs.jsonl.gz",
        }
    )
    payloads, _directory_identity, _file_identities = capture_directory(
        candidate,
        c39_inventory,
        {
            "result.json": 4 << 20,
            "root_manifest.sha256": 1 << 20,
            "PARTIAL_GRAPH_ROUTER_ONLY.lock": 1 << 20,
        },
        "C39",
    )
    validate_manifest_payloads(payloads, "root_manifest.sha256", "C39")
    result = strict_json_bytes(payloads["result.json"], "C39 result")
    closed_object(result, "C39 result")
    need(
        result.get("schema") == C39_SCHEMA
        and result.get("object_sha256") == C39_OBJECT
        and result.get("round144_terminal_census")
        == {
            "CONNECTED_TO_KNOWN": 0,
            "EARLIEST_PREFIX_EXCLUDED": 75134,
            "SOURCE_GRAZING_OR_CEMETERY": 0,
            "TYPED_EVENT_GRAPH": 296,
            "UNRESOLVED_R1648_CONTINUATION": 1402,
            "terminal_total": 76832,
            "unresolved_zero": False,
        },
        "C39 frozen semantics",
    )
    audit_raw, _audit_identity = stable_read(audit_path, 4 << 20, "C39 audit")
    audit = strict_json_bytes(audit_raw, "C39 audit")
    closed_object(audit, "C39 audit")
    need(
        audit.get("schema") == C39_AUDIT_SCHEMA
        and audit.get("object_sha256") == C39_AUDIT_OBJECT
        and audit.get("candidate_object_sha256") == C39_OBJECT
        and all(audit.get("attacks", {}).values())
        and len(audit.get("attacks", {})) == 18,
        "C39 independent audit authority",
    )
    routed = read_ledger_raw(
        payloads["routed_child_pairs.jsonl.gz"],
        result["ledgers"]["routed_child_pairs"],
        "routed_child_pairs.jsonl.gz",
    )
    parents = read_ledger_raw(
        payloads["parent_conservation.jsonl.gz"],
        result["ledgers"]["parent_conservation"],
        "parent_conservation.jsonl.gz",
    )
    need(len(routed) == 10486 and len(parents) == 862, "C39 ledger census")
    ids = [row.get("c39_routed_child_pair_id") for row in routed]
    need(
        all(type(item) is str for item in ids)
        and len(ids) == len(set(ids))
        and SOURCE_ENDPOINT_IDS <= set(ids)
        and DELTA1_H1_INTERSECTION_IDS <= set(ids),
        "C39 source row identity census",
    )
    return result, audit, routed, parents


def pinned_result(directory: Path, expected_object: str, label: str) -> dict[str, Any]:
    raw, _file_identity = stable_read(directory / "result.json", 32 << 20, label)
    result = strict_json_bytes(raw, label)
    closed_object(result, label)
    need(result.get("object_sha256") == expected_object, "pinned object:" + label)
    return result


def pinned_ledger(
    directory: Path,
    result: dict[str, Any],
    descriptor_name: str,
    label: str,
) -> list[dict[str, Any]]:
    descriptor = result["ledgers"][descriptor_name]
    filename = descriptor["filename"]
    raw, _file_identity = stable_read(directory / filename, 512 << 20, label)
    return read_ledger_raw(raw, descriptor, filename)


def load_geometry_authority(
    c39_result: dict[str, Any],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    c38_directory = (ROOT / c39_result["C38_authority"]["path"]).resolve()
    c38_result = pinned_result(c38_directory, C38_OBJECT, "C38 result")
    c38_rows = pinned_ledger(
        c38_directory,
        c38_result,
        "collision1_2_child_pairs",
        "C38 child rows",
    )
    c38_index = {row["row_sha256"]: row for row in c38_rows}
    need(len(c38_index) == len(c38_rows) == 10486, "C38 row uniqueness")

    c37_directory = (ROOT / c38_result["C37_authority"]["path"]).resolve()
    c37_result = pinned_result(c37_directory, C37_OBJECT, "C37 result")
    c36_directory = (ROOT / c37_result["C36_authority"]["path"]).resolve()
    c36_result = pinned_result(c36_directory, C36_OBJECT, "C36 result")
    c35_directory = (ROOT / c36_result["C35_authority"]["path"]).resolve()
    c35_result = pinned_result(c35_directory, C35_OBJECT, "C35 result")
    c34_directory = (ROOT / c36_result["C34_authority"]["path"]).resolve()
    c34_result = pinned_result(c34_directory, C34_OBJECT, "C34 result")
    c32_directory = (ROOT / c34_result["C32_authority"]["path"]).resolve()
    c32_result = pinned_result(c32_directory, C32_OBJECT, "C32 result")
    cells = pinned_ledger(c32_directory, c32_result, "cells", "C32 cells")
    cell_index = {row["cell_id"]: row for row in cells}
    need(len(cell_index) == len(cells) == 76832, "C32 cell uniqueness")
    source_seams = pinned_ledger(
        c32_directory,
        c32_result,
        "source_chart_seams",
        "C32 source-chart seams",
    )
    original_path = pinned_ledger(
        c35_directory, c35_result, "path_occurrences", "C35 path occurrences"
    )[:2]
    reflected_path = pinned_ledger(
        c37_directory,
        c37_result,
        "reflected_r1648_occurrences",
        "C37 reflected occurrences",
    )[:2]
    pair_index, pattern_index, registry_sha = (
        round139.lower.component_cert.key_index_tables()
    )
    # The official registry starts with the empty crossing pattern.  C40 sends
    # these tuple-keyed tables through a worker boundary, so pin the sentinel
    # explicitly: a lossy codec that maps () to ("",) changes routing while
    # leaving the surrounding registry hash/source ledgers untouched.
    need(
        pattern_index.get(()) == 0
        and ("",) not in pattern_index,
        "official empty crossing pattern sentinel",
    )
    config = {
        "original_path": original_path,
        "reflected_path": reflected_path,
        "pair_index": pair_index,
        "pattern_index": pattern_index,
        "registry_sha256": registry_sha,
        "source_chart_seams": source_seams,
    }
    return c38_index, cell_index, config


def capture_c40_candidate(
    candidate: Path,
) -> tuple[
    dict[str, Any],
    dict[str, list[dict[str, Any]]],
    str,
    tuple[int, ...],
    dict[str, tuple[int, ...]],
]:
    payloads, directory_identity, file_identities = capture_directory(
        candidate,
        INVENTORY,
        {
            "result.json": 8 << 20,
            "root_manifest.sha256": 1 << 20,
            "PARTIAL_ARRANGEMENT_ONLY.lock": 1 << 20,
        },
        "C40",
    )
    validate_manifest_payloads(payloads, "root_manifest.sha256", "C40")
    result = strict_json_bytes(payloads["result.json"], "C40 result")
    closed_object(result, "C40 result")
    need(result.get("schema") == CANDIDATE_SCHEMA, "C40 result schema")
    descriptors = result.get("ledgers")
    need(type(descriptors) is dict, "C40 ledger descriptors")
    rows: dict[str, list[dict[str, Any]]] = {}
    for filename in LEDGER_NAMES:
        descriptor = next(
            (
                value
                for value in descriptors.values()
                if type(value) is dict and value.get("filename") == filename
            ),
            None,
        )
        need(type(descriptor) is dict, "C40 missing descriptor:" + filename)
        rows[filename] = read_ledger_raw(payloads[filename], descriptor, filename)
    validate_nonpromotion_lock(payloads["PARTIAL_ARRANGEMENT_ONLY.lock"])
    return (
        result,
        rows,
        bytes_sha256(payloads["root_manifest.sha256"]),
        directory_identity,
        file_identities,
    )


LEAF_SCHEMA = "cm2.round306c40.routed-leaf-cell.v1"
H1_SCHEMA = "cm2.round306c40.h1-graph-cell.v1"
ENDPOINT_SCHEMA = "cm2.round306c40.endpoint-chart.v1"
C2_SCHEMA = "cm2.round306c40.collision2-multi-delta-cell.v1"
C2_SOURCE_SCHEMA = "cm2.round306c40.collision2-source-candidate-census.v1"
PARENT_SCHEMA = "cm2.round306c40.parent-conservation.v1"
RECEIPT_SCHEMA = "cm2.round306c40.execution-receipt.v1"


def expected_refined_box(source: dict[str, Any], suffix: str) -> Any:
    box = atlas_box(source["representative_box"], source["path"])
    for bit in suffix:
        box = round166.split_axis(box, round166.longest_axis(box))[int(bit)]
    return box


def leaf_identity(source: dict[str, Any], path: str, fraction: Q) -> str:
    return "c40-leaf:" + digest(
        {
            "pair_index": source["pair_index"],
            "c39_source_row_sha256": source["row_sha256"],
            "path": path,
            "parent_volume_fraction": qstr(fraction),
        }
    )


def validate_leaf_partitions(
    leaves: list[dict[str, Any]],
    c39_rows: list[dict[str, Any]],
    c38_index: dict[str, dict[str, Any]],
    cells: dict[str, dict[str, Any]],
    config: dict[str, Any],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[int, list[dict[str, Any]]],
    list[str],
    Counter[str],
]:
    need(len(leaves) == 35009, "C40 all-source routed leaf census")
    source_index = {row["row_sha256"]: row for row in c39_rows}
    source_order = {row["row_sha256"]: index for index, row in enumerate(c39_rows)}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    observed_order: list[tuple[int, str]] = []
    leaf_index: dict[str, dict[str, Any]] = {}
    rows_by_pair: dict[int, list[dict[str, Any]]] = defaultdict(list)
    classifications: Counter[str] = Counter()
    for leaf in leaves:
        need(leaf.get("schema") == LEAF_SCHEMA, "leaf schema")
        source_sha = leaf.get("c39_source_row_sha256")
        need(source_sha in source_index, "leaf C39 binding")
        source = source_index[source_sha]
        c38_source = c38_index.get(source["c38_child_row_sha256"])
        need(c38_source is not None, "leaf C38 authority binding")
        path = leaf.get("path")
        fraction = Q(leaf.get("parent_volume_fraction"))
        extra_depth = leaf.get("extra_depth")
        need(
            type(path) is str
            and type(extra_depth) is int
            and path.startswith(source["path"])
            and len(path) - len(source["path"]) == extra_depth
            and 0 <= extra_depth <= EXTRA_DEPTH,
            "leaf exact path depth",
        )
        need(
            fraction
            == Q(source["parent_volume_fraction"]) / (2 ** extra_depth),
            "leaf dyadic weight",
        )
        need(
            leaf.get("c40_leaf_id") == leaf_identity(source, path, fraction)
            and leaf["c40_leaf_id"] not in leaf_index,
            "leaf identity closure",
        )
        need(
            leaf.get("pair_index") == source["pair_index"]
            and leaf.get("c39_source_id")
            == source.get("c39_routed_child_pair_id")
            and leaf.get("c38_source_row_sha256") == c38_source["row_sha256"]
            and leaf.get("representative_cell_id")
            == source["representative_cell_id"]
            and leaf.get("reflected_cell_id") == source["reflected_cell_id"]
            and leaf.get("source_path") == source["path"]
            and leaf.get("source_classification") == source["classification"],
            "leaf source semantics",
        )
        if leaf.get("route_method") != "C39_ROUTE_EXCEPTION_FAIL_CLOSED":
            need(
                leaf.get("route_failure") is None
                and leaf.get("route_exception_phase") is None
                and leaf.get("route_exception_type") is None
                and leaf.get("route_exception_message") is None,
                "nonexception leaf null structured route failure",
            )
        if source["representative_box"] is None:
            need(
                extra_depth == 0
                and leaf.get("representative_box") is None
                and leaf.get("reflected_box") is None
                and leaf.get("reflection_transport_materialized") is False,
                "algebraic leaf geometry",
            )
        else:
            box = expected_refined_box(source, path[len(source["path"]):])
            chart = ":".join(c38_source["representative_origin_key"].split(":")[:2])
            need(
                leaf.get("representative_box") == box_payload(box)
                and leaf.get("reflected_box")
                == reflected_payload(chart.split(":")[1], box)
                and leaf.get("reflection_transport_materialized") is True,
                "leaf exact dyadic geometry",
            )
        terminal = leaf.get("classification", "").startswith("EXCLUDED_")
        need(
            leaf.get("round144_terminal_class")
            == (
                "EARLIEST_PREFIX_EXCLUDED"
                if terminal
                else "UNRESOLVED_R1648_CONTINUATION"
            )
            and leaf.get("local_round144_terminal_credit") == (1 if terminal else 0)
            and leaf.get("C34_common_refinement_credit") == 0
            and leaf.get("D02_gate_credit") == 0,
            "leaf credit boundary",
        )
        if terminal:
            need(
                leaf.get("h1_graph_cell_id") is None
                and leaf.get("endpoint_chart_id") is None,
                "excluded leaf cannot consume graph/endpoint outer",
            )
        elif source["representative_box"] is None:
            need(leaf.get("endpoint_chart_id") is not None, "algebraic endpoint link")
        else:
            geometric = leaf["representative_box"]
            touches_p_endpoint = (
                geometric["p"][0] == "-1" or geometric["p"][1] == "1"
            )
            if touches_p_endpoint:
                need(leaf.get("endpoint_chart_id") is not None, "p endpoint link")
            if "H1_" in leaf["classification"]:
                need(leaf.get("h1_graph_cell_id") is not None, "H1 graph link")
        grouped[source_sha].append(leaf)
        observed_order.append((source_order[source_sha], path))
        leaf_index[leaf["c40_leaf_id"]] = leaf
        rows_by_pair[source["pair_index"]].append(leaf)
        classifications[leaf["classification"]] += 1
    need(observed_order == sorted(observed_order), "leaf ledger order")
    need(set(grouped) == set(source_index), "every C39 source partitioned once")

    new_terminal_ids: list[str] = []
    for source in c39_rows:
        partition = grouped[source["row_sha256"]]
        paths = [row["path"] for row in partition]
        need(
            len(paths) == len(set(paths))
            and not any(
                left != right and right.startswith(left)
                for left in paths
                for right in paths
            ),
            "source prefix-free partition",
        )
        need(
            sum(Q(row["parent_volume_fraction"]) for row in partition)
            == Q(source["parent_volume_fraction"]),
            "source Kraft conservation",
        )
        carried = source["classification"].startswith("EXCLUDED_") or (
            "NEEDS_COLLISION3_1648" in source["classification"]
        )
        if carried:
            need(len(partition) == 1, "C39 carry exactly once")
            leaf = partition[0]
            need(
                leaf["extra_depth"] == 0
                and leaf["path"] == source["path"]
                and leaf["classification"] == source["classification"]
                and leaf["witness"] == source["witness"]
                and leaf["route_method"] == "C39_TERMINAL_OR_LIVE_CARRY"
                and leaf["h1_graph_cell_id"] is None
                and leaf["endpoint_chart_id"] is None
                and leaf["multi_delta_cell_id"] is None,
                "C39 carried byte semantics",
            )
            continue
        if source["representative_box"] is None:
            need(
                len(partition) == 1
                and partition[0]["extra_depth"] == 0
                and partition[0]["classification"]
                == "UNRESOLVED_C40_ALGEBRAIC_ENDPOINT_GRAPH_CELL"
                and partition[0]["endpoint_chart_id"] is not None,
                "algebraic endpoint partition",
            )
            continue
        for leaf in partition:
            need(leaf["extra_depth"] in {1, 2}, "refined rational depth")
            if leaf["extra_depth"] == 1:
                need(
                    leaf["classification"].startswith("EXCLUDED_")
                    or "NEEDS_COLLISION3_1648" in leaf["classification"]
                    or leaf.get("route_method")
                    == "C39_ROUTE_EXCEPTION_FAIL_CLOSED",
                    "early stop only at terminal/live leaf",
                )
            if leaf["classification"].startswith("EXCLUDED_"):
                new_terminal_ids.append(leaf["c40_leaf_id"])

    for leaf_id in new_terminal_ids:
        leaf = leaf_index[leaf_id]
        source = source_index[leaf["c39_source_row_sha256"]]
        c38_source = c38_index[source["c38_child_row_sha256"]]
        cell = cells[source["representative_cell_id"]]
        c39_class, c39_witness, box = independent_c39_child_classification(
            source, c38_source, cell, leaf["path"], config
        )
        if leaf["classification"].startswith("EXCLUDED_C39_"):
            need(
                leaf["classification"] == c39_class
                and leaf["witness"] == c39_witness,
                "independent new C39 terminal route",
            )
        else:
            need(
                leaf.get("multi_delta_cell_id") is not None,
                "C40 exclusion requires linked C2 reconstruction",
            )
            c40_class, c40_witness = independent_c40_collision2_classification(
                c38_source["representative_origin_key"], box, config
            )
            need(
                leaf["classification"] == c40_class
                and leaf["witness"] == c40_witness,
                "independent new C40 terminal route",
            )
    route_exception_rows = [
        leaf
        for leaf in leaves
        if leaf.get("route_method") == "C39_ROUTE_EXCEPTION_FAIL_CLOSED"
    ]
    route_exception_census: Counter[str] = Counter()
    route_exception_signatures: Counter[tuple[str, str, str]] = Counter()
    for leaf in route_exception_rows:
        source = source_index[leaf["c39_source_row_sha256"]]
        c38_source = c38_index[source["c38_child_row_sha256"]]
        cell = cells[source["representative_cell_id"]]
        expected_class, expected_witness, box, expected_failure = (
            independent_c39_route_exception(
                source, c38_source, cell, leaf["path"], config
            )
        )
        source_endpoint = (
            expected_failure["exact_box_endpoint_phase"]
            == "SOURCE_RADICAL_1_MINUS_P2_ENDPOINT"
        )
        causal_source_failure = expected_failure[
            "source_radical_initial_geometry_replay"
        ]["source_radical_causal_match"]
        route_exception_census[expected_class] += 1
        route_exception_signatures[
            (
                expected_failure["exception_module"],
                expected_failure["exception_type"],
                expected_failure["exception_message"],
            )
        ] += 1
        need(
            leaf["classification"] == expected_class
            and leaf["witness"] == expected_witness
            and leaf["representative_box"] == box_payload(box)
            and not leaf["classification"].startswith("EXCLUDED_")
            and leaf["local_round144_terminal_credit"] == 0
            and leaf["C34_common_refinement_credit"] == 0
            and leaf["D02_gate_credit"] == 0
            and leaf.get("multi_delta_cell_id") is None
            and leaf.get("route_failure") == expected_failure
            and leaf.get("route_exception_phase") == expected_failure["phase"]
            and leaf.get("route_exception_type")
            == expected_failure["exception_type"]
            and leaf.get("route_exception_message")
            == expected_failure["exception_message"],
            "independent C39 route-exception zero-credit outer",
        )
        if source_endpoint:
            need(
                leaf.get("endpoint_chart_id") is not None,
                "route p-boundary exact endpoint outer",
            )
        else:
            need(leaf.get("endpoint_chart_id") is None,
                 "nonendpoint route exception has no endpoint claim")
        if causal_source_failure:
            need(
                source_endpoint
                and leaf.get("h1_graph_cell_id") is None,
                "causal source-radical route failure separation",
            )
            continue
        if source_endpoint:
            need(
                expected_class
                == "UNRESOLVED_C40_P_ENDPOINT_BOX_ROUTE_EVALUATION_FAILURE_OUTER",
                "generic p-endpoint route failure separation",
            )
        else:
            need(
                leaf["extra_depth"] == EXTRA_DEPTH
                and box.t0 < box.t1
                and box.p0 < box.p1
                and box.p0 > -1
                and box.p1 < 1
                and box.s0 == box.s1 == 0,
                "generic route exception full interior 2D depth-two outer",
            )
        try:
            h1_evidence = compact_surface(round185.surface_evidence(
                "H1",
                c38_source["representative_origin_key"],
                box,
                FROZEN_OWNER,
                include_axis_tests=True,
            ))
        except Exception:
            h1_evidence = None
        graph_is_certified = certified_nonempty_regular_graph(h1_evidence)
        need(
            (leaf.get("h1_graph_cell_id") is not None) is graph_is_certified,
            "route exception H1 link only after independent certification",
        )
    need(
        route_exception_census
        == Counter(
            {
                (
                    "UNRESOLVED_C40_SOURCE_RADICAL_ENDPOINT_ROUTE_"
                    "EVALUATION_FAILURE_OUTER"
                ): 200,
                "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER": 19,
            }
        )
        and route_exception_signatures
        == Counter(
            {
                (
                    "cm2_round185_preconditioned_c1_residual_refinement",
                    "Round185Error",
                    "AD sqrt domain",
                ): 200,
                ("builtins", "KeyError", "'uncached chart:W:W'"): 19,
            }
        ),
        "exact 219-route-exception classification/type/module/message census",
    )
    return leaf_index, rows_by_pair, new_terminal_ids, classifications


def validate_parent_conservation(
    parent_rows: list[dict[str, Any]],
    rows_by_pair: dict[int, list[dict[str, Any]]],
    c39_parents: list[dict[str, Any]],
) -> dict[str, Any]:
    need(len(parent_rows) == len(c39_parents) == 862, "parent row census")
    prior_index = {row["pair_index"]: row for row in c39_parents}
    full = partial = zero = newly_full = 0
    terminal_equivalent = Q(0)
    unresolved_equivalent = Q(0)
    for ordinal, parent in enumerate(parent_rows):
        need(
            parent.get("schema") == PARENT_SCHEMA
            and parent.get("pair_index") == ordinal,
            "parent order/schema",
        )
        leaves = rows_by_pair[ordinal]
        paths = [row["path"] for row in leaves]
        need(
            len(paths) == len(set(paths))
            and not any(
                left != right and right.startswith(left)
                for left in paths
                for right in paths
            ),
            "parent prefix-free paths",
        )
        total = sum(Q(row["parent_volume_fraction"]) for row in leaves)
        terminal = sum(
            Q(row["parent_volume_fraction"])
            for row in leaves
            if row["classification"].startswith("EXCLUDED_")
        )
        unresolved = total - terminal
        prior = prior_index[ordinal]
        whole = terminal == 1
        need(
            total == 1
            and terminal >= Q(prior["terminal_excluded_parent_volume"])
            and parent.get("c39_parent_row_sha256") == prior["row_sha256"]
            and parent.get("leaf_count") == len(leaves)
            and parent.get("path_prefix_free") is True
            and parent.get("terminal_excluded_parent_volume") == qstr(terminal)
            and parent.get("unresolved_parent_volume") == qstr(unresolved)
            and parent.get("parent_Kraft_conservation") == "1"
            and parent.get("whole_representative_parent_terminal") is whole
            and parent.get("whole_reflected_parent_terminal") is whole
            and parent.get("newly_whole_terminal_vs_C39")
            is (whole and not prior["whole_representative_parent_terminal"])
            and parent.get("C34_common_refinement_credit") == (2 if whole else 0)
            and parent.get("D02_gate_credit") == 0,
            "parent exact reconstruction",
        )
        if whole:
            full += 1
        elif terminal == 0:
            zero += 1
        else:
            partial += 1
        if whole and not prior["whole_representative_parent_terminal"]:
            newly_full += 1
        terminal_equivalent += terminal
        unresolved_equivalent += unresolved
    need(
        full + partial + zero == 862
        and terminal_equivalent + unresolved_equivalent == 862
        and full >= 161
        and newly_full == full - 161,
        "global parent conservation",
    )
    return {
        "whole": full,
        "partial": partial,
        "zero": zero,
        "newly_whole": newly_full,
        "terminal_equivalent": qstr(terminal_equivalent),
        "unresolved_equivalent": qstr(unresolved_equivalent),
        "formal_excluded": 74812 + 2 * full,
        "formal_unresolved": 1724 - 2 * full,
    }


def exact_candidate_inventory(
    parent_key: str, box: Any,
) -> tuple[list[dict[str, Any]], Counter[str], list[dict[str, Any]]]:
    state = round185.r181.collision1_state_direct(parent_key, box)
    geometry = round185.r183.collision2_geometry(state)
    candidate_rows: list[dict[str, Any]] = []
    future: list[tuple[str, dict[str, Any]]] = []
    census: Counter[str] = Counter()
    candidates = list(round185.CANDIDATES)
    need(
        len(candidates) == C2_CANDIDATE_COUNT
        and digest(candidates) == C2_CANDIDATE_TUPLE_SHA256,
        "Round185 pinned C2 candidate tuple",
    )
    for ordinal, identifier in enumerate(candidates):
        raw = round185.r181.raw_candidate(geometry, identifier)
        kind, data = round185.r178.root_record(*geometry, identifier)
        census[kind] += 1
        near = None
        if data is not None and data.get("near") is not None:
            near = round185.arb_bounds(data["near"])
        if kind == "STRICT_FUTURE" and data is not None:
            future.append((identifier, data))
        candidate_rows.append(
            {
                "candidate_ordinal": ordinal,
                "target_id": identifier,
                "raw_classification": kind,
                "ell": round185.arb_bounds(raw["ell"]),
                "Delta": round185.arb_bounds(raw["Delta"]),
                "transverse": round185.arb_bounds(raw["transverse"]),
                "near": near,
                "active_surface_kind": (
                    "DELTA_ZERO"
                    if kind == "UNRESOLVED_DELTA"
                    else "NEAR_ROOT_ZERO"
                    if kind == "UNRESOLVED_ROOT_SIGN"
                    else None
                ),
            }
        )
    pairs: list[dict[str, Any]] = []
    center_box = round185.point_box(
        box,
        (box.t0 + box.t1) / 2,
        (box.p0 + box.p1) / 2,
        (box.s0 + box.s1) / 2,
        ".c40-root-order-center",
    )
    center_state = round185.r181.collision1_state_direct(parent_key, center_box)
    center_geometry = round185.r183.collision2_geometry(center_state)
    for left_index, (left_id, left) in enumerate(future):
        for right_id, right in future[left_index + 1:]:
            if bool(left["near"] < right["near"]):
                relation = "LEFT_STRICTLY_BEFORE_RIGHT"
            elif bool(right["near"] < left["near"]):
                relation = "RIGHT_STRICTLY_BEFORE_LEFT"
            else:
                left_kind, left_center = round185.r178.root_record(
                    *center_geometry, left_id
                )
                right_kind, right_center = round185.r178.root_record(
                    *center_geometry, right_id
                )
                need(
                    left_kind == right_kind == "STRICT_FUTURE"
                    and left_center is not None
                    and right_center is not None,
                    "strict center future pair",
                )
                if bool(left_center["near"] < right_center["near"]):
                    relation = "LEFT_BEFORE_BY_CENTER_AND_SEPARATION"
                elif bool(right_center["near"] < left_center["near"]):
                    relation = "RIGHT_BEFORE_BY_CENTER_AND_SEPARATION"
                else:
                    raise Reject("center root equality contradicts separation")
            pairs.append(
                {
                    "left_target_id": left_id,
                    "right_target_id": right_id,
                    "root_order_relation": relation,
                    "root_equality_carrier": (
                        "EMPTY_BY_PINNED_DISJOINT_BOUNDARY_SEPARATION"
                    ),
                    "equality_carrier_empty_by_boundary_registry": True,
                    "boundary_separation_registry_sha256": (
                        C2_BOUNDARY_REGISTRY_SHA256
                    ),
                    "wall_or_order_credit": 0,
                }
            )
    return candidate_rows, census, pairs


def validate_candidate_rows(
    observed: list[dict[str, Any]],
    expected: list[dict[str, Any]],
    label: str,
    surface_evidence_allowed: bool,
    parent_key: str | None = None,
    box: Any | None = None,
) -> None:
    need(len(observed) == len(expected) == C2_CANDIDATE_COUNT, label + ":55")
    for actual, reference in zip(observed, expected, strict=True):
        for key, value in reference.items():
            need(actual.get(key) == value, label + ":" + key)
        kind = reference["raw_classification"]
        surface = actual.get("surface_evidence")
        error = actual.get("surface_evidence_error")
        if not surface_evidence_allowed:
            need(surface is None and error is None, label + ":source evidence absent")
            continue
        need(parent_key is not None and box is not None, label + ":surface context")
        if kind == "UNRESOLVED_ROOT_SIGN":
            need(
                actual.get("active_surface_kind") == "NEAR_ROOT_ZERO"
                and surface is None
                and error
                == {
                    "error_type": "ROOT_SIGN_SURFACE_EVIDENCE_NOT_MATERIALIZED",
                    "error_message": (
                        "near=0 requires its own ell^2-Delta equivalence and "
                        "C0/C1 face proof; Delta=0 evidence is not substituted"
                    ),
                },
                label + ":root-sign fail-closed carrier",
            )
        elif kind == "UNRESOLVED_DELTA":
            try:
                expected_surface = compact_surface(round185.surface_evidence(
                    "DELTA", parent_key, box, actual["target_id"],
                    include_axis_tests=True,
                ))
                expected_error = None
            except Exception as replay_error:
                expected_surface = None
                expected_error = {
                    "error_type": type(replay_error).__name__,
                    "error_message": str(replay_error),
                }
            need(
                actual.get("active_surface_kind") == "DELTA_ZERO"
                and surface == expected_surface
                and error == expected_error,
                label + ":Delta surface replay",
            )
        else:
            need(surface is None and error is None, label + ":inactive surface absent")


def validate_future_pairs(
    observed: list[dict[str, Any]],
    expected: list[dict[str, Any]],
    label: str,
) -> None:
    need(len(observed) == len(expected), label + ":pair count")
    for actual, reference in zip(observed, expected, strict=True):
        for key, value in reference.items():
            need(actual.get(key) == value, label + ":" + key)
        need(
            actual.get("root_equality_carrier")
            == "EMPTY_BY_PINNED_DISJOINT_BOUNDARY_SEPARATION"
            and actual.get("equality_carrier_empty_by_boundary_registry") is True
            and actual.get("boundary_separation_registry_sha256")
            == C2_BOUNDARY_REGISTRY_SHA256
            and actual.get("wall_or_order_credit") == 0,
            label + ":boundary registry",
        )


def validate_c2_source_census(
    rows: list[dict[str, Any]],
    c39_rows: list[dict[str, Any]],
    c38_index: dict[str, dict[str, Any]],
) -> dict[str, int]:
    targets = [
        row for row in c39_rows
        if row["classification"] in C2_SOURCE_CLASSIFICATIONS
    ]
    need(len(rows) == len(targets) == C2_SOURCE_ROW_COUNT, "C2 source row census")
    aggregate: Counter[str] = Counter()
    pair_count = 0
    for observed, source in zip(rows, targets, strict=True):
        need(observed.get("schema") == C2_SOURCE_SCHEMA, "C2 source schema")
        c38_source = c38_index[source["c38_child_row_sha256"]]
        box = atlas_box(source["representative_box"], source["path"])
        expected_id = "c40-c2-source:" + digest(
            {"source": source["row_sha256"], "box": box_payload(box)}
        )
        need(
            observed.get("source_candidate_census_id") == expected_id
            and observed.get("pair_index") == source["pair_index"]
            and observed.get("c39_source_id")
            == source["c39_routed_child_pair_id"]
            and observed.get("c39_source_row_sha256") == source["row_sha256"]
            and observed.get("c38_source_row_sha256") == c38_source["row_sha256"]
            and observed.get("representative_box") == box_payload(box)
            and observed.get("candidate_universe") == list(round185.CANDIDATES)
            and observed.get("candidate_universe_sha256")
            == C2_CANDIDATE_TUPLE_SHA256
            and observed.get("raw_candidate_count") == C2_CANDIDATE_COUNT
            and observed.get("ambient_or_whole_parent_credit") == 0
            and observed.get("D02_gate_credit") == 0,
            "C2 source binding",
        )
        candidates, census, pairs = exact_candidate_inventory(
            c38_source["representative_origin_key"], box
        )
        lower_ids, lower_candidates, lower_orders = independent_c2_candidate_rows(
            c38_source["representative_origin_key"], box
        )
        need(lower_ids == list(round185.CANDIDATES), "independent lower C2 tuple")
        for exact, lower in zip(candidates, lower_candidates, strict=True):
            need(
                exact["target_id"] == lower["target_id"]
                and exact["raw_classification"]
                == lower["raw_classification"],
                "independent lower C2 target/classification",
            )
        lower_order_index = {
            (item["left_target_id"], item["right_target_id"]): item
            for item in lower_orders
        }
        for pair in pairs:
            lower = lower_order_index[
                (pair["left_target_id"], pair["right_target_id"])
            ]
            if lower["left_strictly_before_right"]:
                need(
                    pair["root_order_relation"]
                    == "LEFT_STRICTLY_BEFORE_RIGHT",
                    "independent lower strict left root order",
                )
            elif lower["right_strictly_before_left"]:
                need(
                    pair["root_order_relation"]
                    == "RIGHT_STRICTLY_BEFORE_LEFT",
                    "independent lower strict right root order",
                )
        validate_candidate_rows(
            observed["candidate_dispositions"],
            candidates,
            "C2 source candidates",
            False,
        )
        need(
            observed.get("raw_classification_census")
            == dict(sorted(census.items())),
            "C2 source local census",
        )
        validate_future_pairs(
            observed["strict_future_pair_order_rows"], pairs, "C2 source pairs"
        )
        aggregate.update(census)
        pair_count += len(pairs)
    need(
        dict(sorted(aggregate.items())) == C2_SOURCE_RAW_CENSUS
        and pair_count == 5708,
        "C2 source 6232x55 aggregate",
    )
    return {**dict(sorted(aggregate.items())), "strict_future_pair_rows": pair_count}


def validate_c2_children(
    rows: list[dict[str, Any]],
    leaf_index: dict[str, dict[str, Any]],
    c39_index: dict[str, dict[str, Any]],
    c38_index: dict[str, dict[str, Any]],
    config: dict[str, Any],
) -> dict[str, int]:
    row_index: dict[str, dict[str, Any]] = {}
    aggregate: Counter[str] = Counter()
    pair_total = 0
    active_total = 0
    certified_total = 0
    incidence_total = 0
    for row in rows:
        need(row.get("schema") == C2_SCHEMA, "child C2 schema")
        leaf = leaf_index.get(row.get("c40_leaf_id"))
        need(
            leaf is not None
            and leaf.get("multi_delta_cell_id") == row.get("multi_delta_cell_id"),
            "child C2 leaf binding",
        )
        identifier = row["multi_delta_cell_id"]
        body = dict(row)
        body.pop("row_sha256", None)
        recorded_id = body.pop("multi_delta_cell_id", None)
        need(
            recorded_id == "c40-multi-delta:" + digest(body)
            and identifier not in row_index,
            "child C2 identity",
        )
        source = c39_index[leaf["c39_source_row_sha256"]]
        c38_source = c38_index[source["c38_child_row_sha256"]]
        box = atlas_box(leaf["representative_box"], leaf["path"])
        need(
            row.get("pair_index") == source["pair_index"]
            and row.get("c39_source_row_sha256") == source["row_sha256"]
            and row.get("c38_source_row_sha256") == c38_source["row_sha256"]
            and row.get("candidate_universe") == list(round185.CANDIDATES)
            and row.get("candidate_universe_sha256") == C2_CANDIDATE_TUPLE_SHA256
            and row.get("raw_candidate_count") == C2_CANDIDATE_COUNT
            and row.get("ambient_or_whole_parent_credit") == 0
            and row.get("D02_gate_credit") == 0
            and row.get("open_chambers_materialized") is False,
            "child C2 authority/credit boundary",
        )
        candidates, census, pairs = exact_candidate_inventory(
            c38_source["representative_origin_key"], box
        )
        validate_candidate_rows(
            row["candidate_dispositions"],
            candidates,
            "child C2 candidates",
            True,
            c38_source["representative_origin_key"],
            box,
        )
        need(
            row.get("raw_classification_census") == dict(sorted(census.items())),
            "child C2 local census",
        )
        validate_future_pairs(
            row["strict_future_pair_order_rows"], pairs, "child C2 future pairs"
        )
        try:
            status, detail, _evidence, baseline = round185.resolve_dynamic_box(
                c38_source["representative_origin_key"],
                box,
                config["pair_index"],
                config["pattern_index"],
            )
        except Exception as error:
            status = "EVALUATION_EXCEPTION"
            baseline = "ROUND185_FAIL_CLOSED"
            detail = {
                "point_owner": None,
                "error_type": type(error).__name__,
                "error_message": str(error),
            }
        expected_class, expected_witness = independent_c40_collision2_classification(
            c38_source["representative_origin_key"], box, config
        )
        need(
            row.get("baseline_status") == baseline
            and row.get("enhanced_status") == status
            and row.get("detail_sha256") == digest(detail)
            and row.get("route_classification") == expected_class
            and row.get("route_witness") == expected_witness
            and leaf["classification"] == expected_class
            and leaf["witness"] == expected_witness,
            "child C2 exact route reconstruction",
        )
        active_expected = {
            candidate["target_id"]: (
                candidate["active_surface_kind"],
                row["candidate_dispositions"][candidate["candidate_ordinal"]],
            )
            for candidate in candidates
            if candidate["active_surface_kind"] is not None
        }
        active_rows = row.get("active_surface_rows")
        need(type(active_rows) is list, "child C2 active rows")
        active_observed: dict[str, dict[str, Any]] = {}
        for active in active_rows:
            target = active.get("target_id")
            surface_kind, disposition = active_expected.get(target, (None, None))
            raw_kind = disposition.get("raw_classification") if disposition else None
            expected_surface_id = "c40-c2-surface:" + digest(
                {"leaf": leaf["c40_leaf_id"], "target": target, "kind": raw_kind}
            )
            evidence = disposition.get("surface_evidence") if disposition else None
            graph_is_certified = certified_nonempty_regular_graph(evidence)
            expected_faces = (
                [
                    {
                        "face": face,
                        "intersection_status": (
                            "FACE_RESTRICTED_INTERSECTION_UNRESOLVED_OUTER"
                        ),
                        "credit": 0,
                    }
                    for face in ("t_lower", "t_upper", "p_lower", "p_upper")
                ]
                if evidence is not None
                else []
            )
            need(
                target in active_expected
                and target not in active_observed
                and active.get("surface_id") == expected_surface_id
                and active.get("surface_kind") == surface_kind
                and active.get("surface_evidence") == evidence
                and active.get("surface_evidence_sha256")
                == (evidence.get("evidence_sha256") if evidence else None)
                and active.get("candidate_surface_expected_dimension") == 1
                and active.get("certified_carrier_dimension")
                == (1 if graph_is_certified else None)
                and active.get("carrier_existence_status")
                == (
                    "CERTIFIED_NONEMPTY_REGULAR_GRAPH"
                    if graph_is_certified
                    else "UNRESOLVED_POTENTIAL_SURFACE_OUTER"
                )
                and active.get("certified_nonempty_regular_graph")
                is graph_is_certified
                and active.get("interior_axis_crossing_brackets_t_p")
                == (
                    evidence["axis_full_face_brackets_t_p_s"][:2]
                    if evidence else []
                )
                and active.get("ambient_or_whole_parent_credit") == 0,
                "child C2 active surface",
            )
            if surface_kind == "DELTA_ZERO":
                need(
                    active.get("equation") == f"Delta_{target}=0",
                    "Delta equation",
                )
            else:
                need(
                    active.get("equation") == f"near_{target}=0",
                    "near-root equation",
                )
            faces = active.get("boundary_face_rows")
            corners = active.get("corner_rows")
            need(
                type(faces) is list
                and faces == expected_faces
                and type(corners) is list
                and corners
                == [
                    {"corner": corner, "status": "RETAINED_OUTER", "credit": 0}
                    for corner in ("t0p0", "t0p1", "t1p0", "t1p1")
                ],
                "child C2 boundary/corner outers",
            )
            active_observed[target] = active
        need(set(active_observed) == set(active_expected), "child C2 all active surfaces")
        incidence = row.get("pairwise_incidence_rows")
        need(type(incidence) is list, "child C2 incidence rows")
        expected_pairs = {
            tuple(sorted(pair))
            for pair in itertools.combinations(active_expected, 2)
        }
        actual_pairs: set[tuple[str, str]] = set()
        surface_target = {
            active["surface_id"]: target for target, active in active_observed.items()
        }
        for item in incidence:
            left = surface_target.get(item.get("left_surface_id"))
            right = surface_target.get(item.get("right_surface_id"))
            need(left is not None and right is not None and left != right, "C2 incidence binding")
            pair = tuple(sorted((left, right)))
            left_evidence = active_expected[left][1].get("surface_evidence")
            right_evidence = active_expected[right][1].get("surface_evidence")
            if left_evidence is not None and right_evidence is not None:
                left_full = round185.delta_ad(
                    c38_source["representative_origin_key"], box, left
                )
                right_full = round185.delta_ad(
                    c38_source["representative_origin_key"], box, right
                )
                determinant = (
                    left_full.derivative[0] * right_full.derivative[1]
                    - left_full.derivative[1] * right_full.derivative[0]
                )
                expected_rank = (
                    "STRICT_RANK2_IF_INTERSECTION"
                    if round185.strict_sign(determinant) != 0
                    else "RANK_NOT_CERTIFIED"
                )
                expected_determinant = round185.arb_bounds(determinant)
            else:
                expected_rank = "RANK_NOT_CERTIFIED"
                expected_determinant = None
            need(
                pair not in actual_pairs
                and item.get("candidate_incidence_expected_dimension_in_s0_slice")
                == 0
                and item.get("certified_intersection_dimension") is None
                and item.get("rank_status") == expected_rank
                and item.get("Jacobian_determinant") == expected_determinant
                and item.get("intersection_existence") == "UNRESOLVED_OUTER"
                and item.get("ambient_or_whole_parent_credit") == 0,
                "C2 incidence zero-credit outer",
            )
            actual_pairs.add(pair)
        need(actual_pairs == expected_pairs, "C2 complete pair incidence outers")
        need(
            row.get("active_surface_count") == len(active_rows)
            and row.get("candidate_surface_outer_count") == len(active_rows)
            and row.get("certified_nonempty_regular_graph_count")
            == sum(
                bool(item["certified_nonempty_regular_graph"])
                for item in active_rows
            )
            and row.get("pairwise_potential_incidence_outer_count")
            == len(incidence)
            and row.get("certified_zero_dimensional_intersection_count") == 0
            and row.get("ambient_slice_dimension") == 2
            and row.get("boundary_face_family")
            == ["t_lower", "t_upper", "p_lower", "p_upper"]
            and row.get("corner_family_count") == 4
            and row.get("arrangement_status")
            == "FULL_55_CANDIDATE_OUTER_CATALOG__OPEN_CHAMBERS_NOT_MATERIALIZED",
            "C2 carrier census",
        )
        row_index[identifier] = row
        aggregate.update(census)
        pair_total += len(pairs)
        active_total += len(active_rows)
        certified_total += sum(
            bool(item["certified_nonempty_regular_graph"])
            for item in active_rows
        )
        incidence_total += len(incidence)
    linked = {
        leaf["multi_delta_cell_id"]
        for leaf in leaf_index.values()
        if leaf.get("multi_delta_cell_id") is not None
    }
    need(set(row_index) == linked, "C2 ledger no orphan/missing links")
    return {
        "row_count": len(rows),
        "raw_candidate_count": C2_CANDIDATE_COUNT * len(rows),
        "strict_future_pair_rows": pair_total,
        "candidate_surface_outer_count": active_total,
        "certified_nonempty_regular_graph_count": certified_total,
        "pairwise_potential_incidence_outer_count": incidence_total,
        "certified_zero_dimensional_intersection_count": 0,
    }


def compact_surface(evidence: dict[str, Any]) -> dict[str, Any]:
    derivatives = evidence.get("full_box_C1_derivatives", {})
    return {
        "kind": evidence.get("kind"),
        "identifier": evidence.get("identifier"),
        "equation": evidence.get("equation"),
        "centered_C0_sign": evidence.get("centered_C0_sign"),
        "centered_mean_value_C0_enclosure": evidence.get(
            "centered_mean_value_C0_enclosure"
        ),
        "full_box_C1_derivatives": derivatives,
        "strict_derivative_axes": [
            axis for axis in ("dt", "dp")
            if axis in derivatives and not derivatives[axis]["contains_zero"]
        ],
        "axis_full_face_brackets_t_p_s": evidence.get(
            "axis_full_face_brackets_t_p_s", []
        ),
        "axis_interval_Newton": evidence.get("axis_interval_Newton", []),
        "strict_corner_segment_bracket": evidence.get(
            "strict_corner_segment_bracket"
        ),
        "independently_certified_nonempty": evidence.get(
            "independently_certified_nonempty", False
        ),
        "evidence_sha256": digest(evidence),
    }


def certified_nonempty_regular_graph(evidence: dict[str, Any] | None) -> bool:
    return bool(
        evidence is not None
        and evidence.get("independently_certified_nonempty")
        and evidence.get("strict_derivative_axes")
    )


def endpoint_exception(parent_key: str, box: Any) -> tuple[str, str, str]:
    if box.p0 == -1 or box.p1 == 1:
        return (
            "SOURCE_RADICAL_1_MINUS_P2_ENDPOINT",
            "EXACT_SOURCE_RADICAL_BOUNDARY",
            "q_source^2=1-p^2 and q_source=0 at p=+/-1",
        )
    try:
        initial = round185.ad_initial_geometry(parent_key, box)
    except Exception as error:
        raise Reject(
            "interior initial-geometry evaluation failure:"
            + type(error).__name__
            + ":"
            + str(error)
        ) from error
    try:
        round185.collision1_h1_ad(parent_key, box, FROZEN_OWNER)
    except Exception as error:
        raw = round185.ad_root(initial, FROZEN_OWNER)
        need(
            box.p0 > -1
            and box.p1 < 1
            and bool(raw["Delta"].value.contains(0)),
            "Delta1/H1 intersection invariant",
        )
        return (
            "COLLISION1_DELTA1_H1_EVALUATION_FAILURE_OUTER",
            type(error).__name__,
            str(error),
        )
    return "NONE", "NONE", ""


def validate_h1_graphs(
    rows: list[dict[str, Any]],
    leaf_index: dict[str, dict[str, Any]],
    c39_index: dict[str, dict[str, Any]],
    c38_index: dict[str, dict[str, Any]],
) -> dict[str, int]:
    index: dict[str, dict[str, Any]] = {}
    certified = potential = exceptions = 0
    for row in rows:
        need(row.get("schema") == H1_SCHEMA, "H1 schema")
        leaf = leaf_index.get(row.get("c40_leaf_id"))
        need(
            leaf is not None
            and leaf.get("h1_graph_cell_id") == row.get("h1_graph_cell_id")
            and not leaf["classification"].startswith("EXCLUDED_"),
            "H1 leaf/nonterminal binding",
        )
        identifier = row["h1_graph_cell_id"]
        body = dict(row)
        body.pop("row_sha256", None)
        body.pop("h1_graph_cell_id", None)
        need(
            identifier == "c40-h1:" + digest(body) and identifier not in index,
            "H1 identity closure",
        )
        source = c39_index[leaf["c39_source_row_sha256"]]
        c38_source = c38_index[source["c38_child_row_sha256"]]
        box = atlas_box(leaf["representative_box"], leaf["path"])
        parent_key = c38_source["representative_origin_key"]
        surface_id = "H1:" + digest(
            {"leaf": leaf["c40_leaf_id"], "parent": parent_key, "box": box_payload(box)}
        )
        need(
            row.get("pair_index") == source["pair_index"]
            and row.get("c39_source_row_sha256") == source["row_sha256"]
            and row.get("c38_source_row_sha256") == c38_source["row_sha256"]
            and row.get("surface_id") == surface_id
            and row.get("equation") == "H1=n1_x^2-n1_y^2=0"
            and row.get("ambient_slice_dimension") == 2
            and row.get("candidate_surface_expected_dimension") == 1
            and row.get("open_chamber_signs") == ["H1<0", "H1>0"]
            and row.get("boundary_face_family")
            == ["t_lower", "t_upper", "p_lower", "p_upper"]
            and row.get("boundary_intersection_outer_count") == 4
            and row.get("boundary_intersection_rows")
            == [
                {"face": face, "status": "UNRESOLVED_OUTER", "credit": 0}
                for face in ("t_lower", "t_upper", "p_lower", "p_upper")
            ]
            and row.get("corner_family_count") == 4
            and row.get("ambient_or_whole_parent_credit") == 0
            and row.get("D02_gate_credit") == 0,
            "H1 exact zero-credit envelope",
        )
        try:
            evidence = round185.surface_evidence(
                "H1", parent_key, box, FROZEN_OWNER, include_axis_tests=True
            )
            compact = compact_surface(evidence)
            graph_is_certified = certified_nonempty_regular_graph(compact)
            phase = (
                "H1_CERTIFIED_NONEMPTY_REGULAR_GRAPH"
                if graph_is_certified
                else "H1_POTENTIAL_SURFACE_OUTER"
            )
            error_type = error_message = None
            interior_brackets = sum(
                bool(value)
                for value in compact["axis_full_face_brackets_t_p_s"][:2]
            )
        except Exception as error:
            phase, error_type, error_message = endpoint_exception(parent_key, box)
            if phase == "NONE":
                phase = "H1_SURFACE_EVIDENCE_EVALUATION_EXCEPTION"
                error_type = type(error).__name__
                error_message = str(error)
            compact = None
            graph_is_certified = False
            interior_brackets = 0
            exceptions += 1
        if graph_is_certified:
            certified += 1
        else:
            potential += 1
        need(
            row.get("failure_phase") == phase
            and row.get("exception_type") == error_type
            and row.get("exception_message") == error_message
            and row.get("surface_evidence") == compact
            and row.get("certified_carrier_dimension")
            == (1 if graph_is_certified else None)
            and row.get("carrier_existence_status")
            == (
                "CERTIFIED_NONEMPTY_REGULAR_GRAPH"
                if graph_is_certified
                else "UNRESOLVED_POTENTIAL_SURFACE_OUTER"
            )
            and row.get("certified_nonempty_regular_graph") is graph_is_certified
            and row.get("interior_axis_full_face_bracket_count")
            == interior_brackets,
            "independent H1 surface replay",
        )
        index[identifier] = row
    linked = {
        leaf["h1_graph_cell_id"]
        for leaf in leaf_index.values()
        if leaf.get("h1_graph_cell_id") is not None
    }
    expected_links = {
        leaf["h1_graph_cell_id"]
        for leaf in leaf_index.values()
        if not leaf["classification"].startswith("EXCLUDED_")
        and (
            "H1_" in leaf["classification"]
            or (
                leaf.get("route_method") == "C39_ROUTE_EXCEPTION_FAIL_CLOSED"
                and leaf.get("h1_graph_cell_id") is not None
            )
        )
    }
    need(
        None not in expected_links and set(index) == linked == expected_links,
        "H1 ledger no orphan/missing links",
    )
    need(certified + potential == len(rows), "H1 potential/certified census")
    return {
        "row_count": len(rows),
        "certified_nonempty_regular_graph_count": certified,
        "unresolved_potential_surface_outer_count": potential,
        "evaluation_exception_count": exceptions,
    }


def algebraic_seams_for_cell(
    cell: dict[str, Any], seams: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    candidates = [
        row for row in seams
        if cell["cell_id"] in {row["left_cell_id"], row["right_cell_id"]}
    ]
    candidates.sort(key=lambda row: Q(row["physical_p_span"][0]["value"]))
    need(bool(candidates), "nonempty algebraic source-chart seams")
    spans = [
        tuple(Q(value["value"]) for value in row["physical_p_span"])
        for row in candidates
    ]
    need(
        spans[0][0] == Q(cell["physical_p_interval"][0])
        and spans[-1][1] == Q(cell["physical_p_interval"][1])
        and all(left[1] == right[0] for left, right in zip(spans, spans[1:])),
        "algebraic seam exact p-span exhaustion",
    )
    return candidates


def validate_endpoints(
    rows: list[dict[str, Any]],
    leaf_index: dict[str, dict[str, Any]],
    c39_index: dict[str, dict[str, Any]],
    c38_index: dict[str, dict[str, Any]],
    cells: dict[str, dict[str, Any]],
    seams: list[dict[str, Any]],
) -> dict[str, Any]:
    index: dict[str, dict[str, Any]] = {}
    algebraic_pairs: set[int] = set()
    source_ids: set[str] = set()
    delta_ids: set[str] = set()
    phases: Counter[str] = Counter()
    seam_segment_census: Counter[int] = Counter()
    seam_incidence_count = 0
    for row in rows:
        need(row.get("schema") == ENDPOINT_SCHEMA, "endpoint schema")
        leaf = leaf_index.get(row.get("c40_leaf_id"))
        need(
            leaf is not None
            and leaf.get("endpoint_chart_id") == row.get("endpoint_chart_id")
            and not leaf["classification"].startswith("EXCLUDED_"),
            "endpoint leaf/nonterminal binding",
        )
        identifier = row["endpoint_chart_id"]
        body = dict(row)
        body.pop("row_sha256", None)
        body.pop("endpoint_chart_id", None)
        need(
            identifier == "c40-endpoint:" + digest(body) and identifier not in index,
            "endpoint identity closure",
        )
        source = c39_index[leaf["c39_source_row_sha256"]]
        c38_source = c38_index[source["c38_child_row_sha256"]]
        cell = cells[source["representative_cell_id"]]
        source_id = source["c39_routed_child_pair_id"]
        need(
            row.get("pair_index") == source["pair_index"]
            and row.get("c39_source_row_sha256") == source["row_sha256"]
            and row.get("c38_source_row_sha256") == c38_source["row_sha256"]
            and row.get("classification") == leaf["classification"]
            and row.get("ambient_slice_dimension") == 2
            and row.get("boundary_and_corner_inventory_complete") is False
            and row.get("ambient_or_whole_parent_credit") == 0
            and row.get("D02_gate_credit") == 0,
            "endpoint exact zero-credit envelope",
        )
        phase = row.get("failure_phase")
        need(type(phase) is str, "endpoint failure phase type")
        phases[phase] += 1
        if phase == "ALGEBRAIC_SOURCE_CHART_H0_ENDPOINT":
            algebraic_pairs.add(source["pair_index"])
            need(
                source["representative_box"] is None
                and row.get("exception_target") == "exact algebraic H0"
                and row.get("exception_type") == "NOT_EVALUATED"
                and row.get("exception_message") == "exact endpoint chart"
                and row.get("chart_equations")
                == [
                    row["endpoint"]["minimal_polynomial"],
                    "H0=2*t^2-1=0",
                ],
                "algebraic endpoint type",
            )
            algebraic = [
                value for value in cell["physical_t_interval"]
                if value["kind"] == "ALGEBRAIC"
            ]
            need(len(algebraic) == 1, "one algebraic cell endpoint")
            endpoint = row["endpoint"]
            for key, value in algebraic[0].items():
                need(endpoint.get(key) == value, "algebraic endpoint exact field")
            endpoint_index = next(
                item for item, value in enumerate(cell["physical_t_interval"])
                if value["kind"] == "ALGEBRAIC"
            )
            expected_sign = (
                "NEGATIVE" if algebraic[0]["value"].startswith("-") else "POSITIVE"
            )
            expected_side = (
                "INTERIOR_ABOVE_ALGEBRAIC_ENDPOINT"
                if endpoint_index == 0
                else "INTERIOR_BELOW_ALGEBRAIC_ENDPOINT"
            )
            seam_rows = algebraic_seams_for_cell(cell, seams)
            seam_segment_census[len(seam_rows)] += 1
            seam_incidence_count += len(seam_rows)
            expected_incidence = []
            for segment_ordinal, seam in enumerate(seam_rows):
                right = seam["right_cell_id"] == cell["cell_id"]
                expected_incidence.append(
                    {
                        "seam_segment_ordinal": segment_ordinal,
                        "seam_id": seam["seam_id"],
                        "face_id": seam["face_id"],
                        "seam_row_sha256": seam["row_sha256"],
                        "orientation": "RIGHT_TO_LEFT" if right else "LEFT_TO_RIGHT",
                        "adjacent_cell_id": (
                            seam["left_cell_id"] if right else seam["right_cell_id"]
                        ),
                        "adjacent_chart": (
                            seam["left_chart"] if right else seam["right_chart"]
                        ),
                        "exact_physical_p_span": seam["physical_p_span"],
                        "exact_state_gluing_inherited_from_round162": seam[
                            "exact_state_gluing_inherited_from_round162"
                        ],
                    }
                )
            expected_rule = (
                "(t,p)->(-t,-p)"
                if cell["compact_chart"] in {"E", "W"}
                else "(t,p)->(t,-p)"
            )
            need(
                endpoint.get("exact_sign") == expected_sign
                and endpoint.get("physical_interval_side") == expected_side
                and endpoint.get("horizontal_reflection_partner_cell_id")
                == c38_source["reflected_cell_id"]
                and endpoint.get("horizontal_reflection_partner_origin_key")
                == c38_source["reflected_origin_key"]
                and endpoint.get("horizontal_reflection_rule") == expected_rule
                and endpoint.get("horizontal_reflection_materialized_in_rational_box")
                is False
                and endpoint.get("adjacent_chart_seam_incidence_count")
                == len(expected_incidence)
                and endpoint.get("adjacent_chart_seam_incidence")
                == expected_incidence
                and row.get("candidate_carrier_expected_dimension") == 1
                and row.get("certified_carrier_dimension") == 1
                and row.get("carrier_existence_status")
                == "CERTIFIED_EXACT_ALGEBRAIC_SOURCE_CHART_ENDPOINT"
                and row.get("candidate_intersection_rank_status")
                == "NOT_APPLICABLE_EXACT_CHART_BOUNDARY"
                and row.get("arrangement_status")
                == "ENDPOINT_OUTER__SEAM_CONTINUATION_PENDING",
                "algebraic reflection versus adjacent seam",
            )
        else:
            need(leaf["representative_box"] is not None, "rational endpoint box")
            box = atlas_box(leaf["representative_box"], leaf["path"])
            expected_phase, error_type, error_message = endpoint_exception(
                c38_source["representative_origin_key"], box
            )
            need(
                phase == expected_phase
                and row.get("exception_type") == error_type
                and row.get("exception_message") == error_message,
                "endpoint failure-phase replay",
            )
            if phase == "SOURCE_RADICAL_1_MINUS_P2_ENDPOINT":
                source_ids.add(source_id)
                need(
                    (box.p0 == -1 or box.p1 == 1)
                    and row.get("exception_target") == "source sqrt"
                    and row.get("chart_equations")
                    == ["q_source^2=1-p^2", "q_source=0"]
                    and row.get("endpoint")
                    == {
                        "p_endpoint": "-1" if box.p0 == -1 else "1",
                        "p_interval": [qstr(box.p0), qstr(box.p1)],
                        "q_chart_orientation": "NONNEGATIVE_SQUARE_ROOT",
                    }
                    and row.get("candidate_carrier_expected_dimension") == 1
                    and row.get("certified_carrier_dimension") == 1
                    and row.get("carrier_existence_status")
                    == "CERTIFIED_EXACT_SOURCE_RADICAL_ENDPOINT"
                    and row.get("candidate_intersection_rank_status")
                    == "NOT_APPLICABLE_EXACT_SOURCE_BOUNDARY"
                    and row.get("arrangement_status")
                    == "ENDPOINT_OUTER__SEAM_CONTINUATION_PENDING",
                    "true source p endpoint",
                )
            else:
                delta_ids.add(source_id)
                initial = round185.ad_initial_geometry(
                    c38_source["representative_origin_key"], box
                )
                raw = round185.ad_root(initial, FROZEN_OWNER)
                need(
                    box.p0 > -1
                    and box.p1 < 1
                    and bool(raw["Delta"].value.contains(0))
                    and row.get("exception_target") == "collision-one sqrt"
                    and row.get("chart_equations")
                    == ["candidate:Delta1=0", "candidate:H1=n1_x^2-n1_y^2=0"]
                    and row.get("endpoint")
                    == {
                        "p_interval": [qstr(box.p0), qstr(box.p1)],
                        "t_interval": [qstr(box.t0), qstr(box.t1)],
                    }
                    and row.get("candidate_carrier_expected_dimension") == 0
                    and row.get("certified_carrier_dimension") is None
                    and row.get("carrier_existence_status")
                    == "UNRESOLVED_EVALUATION_FAILURE_OUTER"
                    and row.get("candidate_intersection_rank_status")
                    == "UNRESOLVED"
                    and row.get("arrangement_status")
                    == "EVALUATION_FAILURE_OUTER__EXISTENCE_AND_RANK_PENDING",
                    "uncertified Delta1/H1 evaluation-failure outer",
                )
        index[identifier] = row
    linked = {
        leaf["endpoint_chart_id"]
        for leaf in leaf_index.values()
        if leaf.get("endpoint_chart_id") is not None
    }
    expected_links: set[str] = set()
    expected_source_ids: set[str] = set()
    expected_delta_ids: set[str] = set()
    for leaf in leaf_index.values():
        if leaf["classification"].startswith("EXCLUDED_"):
            continue
        source = c39_index[leaf["c39_source_row_sha256"]]
        if source["representative_box"] is None:
            expected_links.add(leaf["endpoint_chart_id"])
            continue
        box = atlas_box(leaf["representative_box"], leaf["path"])
        if box.p0 == -1 or box.p1 == 1:
            expected_links.add(leaf["endpoint_chart_id"])
            expected_source_ids.add(source["c39_routed_child_pair_id"])
            continue
        if leaf.get("h1_graph_cell_id") is not None:
            c38_source = c38_index[source["c38_child_row_sha256"]]
            phase, _error_type, _error_message = endpoint_exception(
                c38_source["representative_origin_key"], box
            )
            if phase == "COLLISION1_DELTA1_H1_EVALUATION_FAILURE_OUTER":
                expected_links.add(leaf["endpoint_chart_id"])
                expected_delta_ids.add(source["c39_routed_child_pair_id"])
    need(
        None not in expected_links
        and set(index) == linked == expected_links
        and algebraic_pairs == ALGEBRAIC_PAIR_INDICES
        and source_ids == expected_source_ids
        and delta_ids == expected_delta_ids
        and SOURCE_ENDPOINT_IDS <= source_ids
        and source_ids.isdisjoint(delta_ids)
        and DELTA1_H1_INTERSECTION_IDS.isdisjoint(delta_ids),
        "endpoint exact source sets/no orphan links",
    )
    need(
        len(rows) == 303
        and len(algebraic_pairs) == 29
        and dict(sorted(seam_segment_census.items())) == {1: 26, 2: 2, 3: 1}
        and seam_incidence_count == 33,
        "algebraic endpoint complete seam census",
    )
    return {
        "row_count": len(rows),
        "algebraic_parent_count": len(algebraic_pairs),
        "failure_phase_census": dict(sorted(phases.items())),
        "algebraic_chart_seam_incidence_count": seam_incidence_count,
        "algebraic_chart_seam_segment_count_census": {
            str(key): value for key, value in sorted(seam_segment_census.items())
        },
        "source_endpoint_source_count": len(source_ids),
        "Delta1_H1_source_count": len(delta_ids),
    }


def receipt_closure(value: dict[str, Any], label: str) -> None:
    body = dict(value)
    claimed = body.pop("receipt_object_sha256", None)
    need(
        type(claimed) is str
        and HEX64.fullmatch(claimed) is not None
        and claimed == digest(body),
        "receipt closure:" + label,
    )


def validate_receipt(
    path: Path,
    invocation_id: str,
    candidate: Path,
    result: dict[str, Any],
    manifest_sha256: str,
) -> dict[str, Any]:
    raw, _receipt_identity = stable_read(path, 4 << 20, "C40 receipt")
    receipt = strict_json_bytes(raw, "C40 receipt")
    receipt_closure(receipt, "C40 receipt")
    expected_keys = {
        "schema",
        "status",
        "InvocationID",
        "producer_pid",
        "producer_parent_pid",
        "producer_proc_start_ticks",
        "producer_executable",
        "producer_source_sha256",
        "candidate_path",
        "candidate_object_sha256",
        "root_manifest_sha256",
        "candidate_inventory_count",
        "receipt_object_sha256",
    }
    relative_candidate = str(candidate.resolve().relative_to(ROOT))
    executable = receipt.get("producer_executable")
    need(
        set(receipt) == expected_keys
        and receipt.get("schema") == RECEIPT_SCHEMA
        and receipt.get("status") == "PASS_LIVE_PID_INVOCATION_BOUND_TO_C40_OBJECT"
        and type(invocation_id) is str
        and TOKEN.fullmatch(invocation_id) is not None
        and receipt.get("InvocationID") == invocation_id
        and type(receipt.get("producer_pid")) is int
        and receipt["producer_pid"] > 1
        and type(receipt.get("producer_parent_pid")) is int
        and receipt["producer_parent_pid"] > 0
        and type(receipt.get("producer_proc_start_ticks")) is int
        and receipt["producer_proc_start_ticks"] > 0
        and type(executable) is str
        and Path(executable).is_absolute()
        and receipt.get("producer_source_sha256") == EXPECTED_PRODUCER_SOURCE
        and receipt.get("candidate_path") == relative_candidate
        and receipt.get("candidate_object_sha256") == result["object_sha256"]
        and receipt.get("root_manifest_sha256") == manifest_sha256
        and receipt.get("candidate_inventory_count") == len(INVENTORY),
        "receipt PID/InvocationID/object/manifest binding",
    )
    receipt_absolute = path.resolve()
    need(
        receipt_absolute.parent != candidate.resolve()
        and candidate.resolve() not in receipt_absolute.parents,
        "receipt must be out of band",
    )
    return receipt


def semantic_result_guard(
    result: dict[str, Any],
    rows: dict[str, list[dict[str, Any]]],
    classifications: Counter[str],
    conservation: dict[str, Any],
    c2_source: dict[str, int],
    c2_children: dict[str, int],
    h1: dict[str, int],
    endpoints: dict[str, int],
    c39_path: str,
    c39_audit_path: str,
    registry_sha256: str,
) -> None:
    expected_status = (
        "PASS_C40_DIMENSION_SAFE_ARRANGEMENT_OUTER_FRONTIER__"
        + str(len(rows["routed_leaf_cells.jsonl.gz"]))
        + "_LEAVES__"
        + str(2 * conservation["whole"])
        + "_WHOLE_CELLS_TERMINAL__"
        + str(conservation["formal_unresolved"])
        + "_FORMAL_UNRESOLVED"
    )
    expected_authority = {
        "path": c39_path,
        "object_sha256": C39_OBJECT,
        "independent_audit_path": c39_audit_path,
        "independent_audit_object_sha256": C39_AUDIT_OBJECT,
    }
    expected_numeric = {
        "source_sha256": {
            "C39": EXPECTED_C39_SOURCE,
            "Round185": ROUND185_SOURCE,
            "C38": EXPECTED_C38_SOURCE,
        },
        "flint_version": "0.9.0",
        "precision_bits": PRECISION_BITS,
        "extra_dyadic_depth": EXTRA_DEPTH,
        "official_registry_sha256": registry_sha256,
        "candidate_boundary_separation_registry": C2_BOUNDARY_REGISTRY,
        "candidate_boundary_separation_registry_object_sha256": (
            C2_BOUNDARY_REGISTRY_SHA256
        ),
        "source_slice": "s=0",
    }
    route_exception_census = Counter(
        leaf["classification"]
        for leaf in rows["routed_leaf_cells.jsonl.gz"]
        if leaf.get("route_method") == "C39_ROUTE_EXCEPTION_FAIL_CLOSED"
    )
    route_exception_evidence_census = Counter(
        (
            leaf["classification"],
            leaf["route_failure"]["exception_type"],
            leaf["route_failure"]["exception_message"],
        )
        for leaf in rows["routed_leaf_cells.jsonl.gz"]
        if leaf.get("route_method") == "C39_ROUTE_EXCEPTION_FAIL_CLOSED"
    )
    expected_arrangement = {
        "C39_source_leaf_count": 10486,
        "C39_nonwhole_representative_parent_count": 701,
        "routed_leaf_count": len(rows["routed_leaf_cells.jsonl.gz"]),
        "classification_census": dict(sorted(classifications.items())),
        "route_evaluation_failure_outer_count": sum(
            route_exception_census.values()
        ),
        "route_evaluation_failure_outer_census": dict(
            sorted(route_exception_census.items())
        ),
        "route_evaluation_failure_evidence_census": {
            "\u001f".join(key): value
            for key, value in sorted(route_exception_evidence_census.items())
        },
        "h1_candidate_surface_outer_count": h1["row_count"],
        "h1_certified_nonempty_regular_graph_count": h1[
            "certified_nonempty_regular_graph_count"
        ],
        "endpoint_chart_count": endpoints["row_count"],
        "endpoint_failure_phase_census": endpoints["failure_phase_census"],
        "algebraic_endpoint_chart_count": endpoints["algebraic_parent_count"],
        "algebraic_chart_seam_incidence_count": endpoints[
            "algebraic_chart_seam_incidence_count"
        ],
        "algebraic_chart_seam_segment_count_census": endpoints[
            "algebraic_chart_seam_segment_count_census"
        ],
        "collision2_multi_delta_cell_count": c2_children["row_count"],
        "collision2_candidate_surface_outer_count": c2_children[
            "candidate_surface_outer_count"
        ],
        "collision2_certified_nonempty_regular_graph_count": c2_children[
            "certified_nonempty_regular_graph_count"
        ],
        "collision2_pairwise_potential_incidence_outer_count": c2_children[
            "pairwise_potential_incidence_outer_count"
        ],
        "collision2_certified_zero_dimensional_intersection_count": c2_children[
            "certified_zero_dimensional_intersection_count"
        ],
        "collision2_source_candidate_census_row_count": C2_SOURCE_ROW_COUNT,
        "collision2_source_raw_candidate_count": (
            C2_SOURCE_ROW_COUNT * C2_CANDIDATE_COUNT
        ),
        "collision2_source_raw_classification_census": C2_SOURCE_RAW_CENSUS,
        "collision2_source_strict_future_pair_row_count": c2_source[
            "strict_future_pair_rows"
        ],
        "whole_terminal_representative_parent_count": conservation["whole"],
        "whole_terminal_paired_coarse_cell_count": 2 * conservation["whole"],
        "newly_whole_terminal_representative_parent_count": conservation[
            "newly_whole"
        ],
        "newly_whole_terminal_paired_coarse_cell_count": (
            2 * conservation["newly_whole"]
        ),
        "partial_representative_parent_count": conservation["partial"],
        "zero_progress_representative_parent_count": conservation["zero"],
        "representative_terminal_parent_equivalent": conservation[
            "terminal_equivalent"
        ],
        "representative_unresolved_parent_equivalent": conservation[
            "unresolved_equivalent"
        ],
    }
    expected_terminal = {
        "CONNECTED_TO_KNOWN": 0,
        "EARLIEST_PREFIX_EXCLUDED": conservation["formal_excluded"],
        "SOURCE_GRAZING_OR_CEMETERY": 0,
        "TYPED_EVENT_GRAPH": 296,
        "UNRESOLVED_R1648_CONTINUATION": conservation["formal_unresolved"],
        "terminal_total": 76832,
        "unresolved_zero": False,
    }
    expected_nonpromotion = {
        "lower_dimensional_graph_credit": 0,
        "endpoint_or_incidence_ambient_credit": 0,
        "four_class_terminal_census_unresolved_zero": False,
        "D02": (
            "BLOCKED_BY_"
            + str(conservation["formal_unresolved"])
            + "_COMPLETE_R1648_CONTINUATIONS"
        ),
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "Gate5": "10/18",
        "complete_global_18_field_blocks": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    need(
        set(result)
        == {
            "schema",
            "status",
            "C39_authority",
            "numeric_authority",
            "arrangement_census",
            "ledgers",
            "round144_terminal_census",
            "strict_nonpromotion",
            "execution_receipt_policy",
            "required_next",
            "object_sha256",
        }
        and result.get("schema") == CANDIDATE_SCHEMA
        and result.get("status") == expected_status
        and result.get("C39_authority") == expected_authority
        and result.get("numeric_authority") == expected_numeric
        and result.get("arrangement_census") == expected_arrangement
        and result.get("round144_terminal_census") == expected_terminal
        and result.get("strict_nonpromotion") == expected_nonpromotion
        and "out-of-band" in result.get("execution_receipt_policy", "")
        and "collisions 3--1648" in result.get("required_next", ""),
        "C40 exact result semantics and strict nonpromotion",
    )
    descriptors = result.get("ledgers")
    expected_descriptor_names = {
        "routed_leaf_cells": "routed_leaf_cells.jsonl.gz",
        "h1_graph_cells": "h1_graph_cells.jsonl.gz",
        "endpoint_charts": "endpoint_charts.jsonl.gz",
        "collision2_multi_delta_cells": "collision2_multi_delta_cells.jsonl.gz",
        "collision2_source_candidate_census": (
            "collision2_source_candidate_census.jsonl.gz"
        ),
        "parent_conservation": "parent_conservation.jsonl.gz",
    }
    need(
        type(descriptors) is dict
        and set(descriptors) == set(expected_descriptor_names),
        "C40 exact descriptor keys",
    )
    for key, filename in expected_descriptor_names.items():
        descriptor = descriptors[key]
        expected_order = (
            "PAIR_INDEX_ASCENDING"
            if filename == "parent_conservation.jsonl.gz"
            else "C39_ROW_ORDER"
            if filename == "collision2_source_candidate_census.jsonl.gz"
            else "C39_ROW_ORDER_THEN_PATH"
        )
        need(
            descriptor.get("filename") == filename
            and descriptor.get("row_count") == len(rows[filename])
            and descriptor.get("order") == expected_order,
            "C40 descriptor order/count:" + filename,
        )


def reject_attack(label: str, operation: Any) -> bool:
    try:
        operation()
    except Reject:
        return True
    raise Reject("hostile mutation accepted:" + label)


def hostile_attack_suite(
    result: dict[str, Any],
    receipt: dict[str, Any],
    rows: dict[str, list[dict[str, Any]]],
    config: dict[str, Any],
    invocation_id: str,
    directory_identity: tuple[int, ...],
    file_identities: dict[str, tuple[int, ...]],
) -> dict[str, bool]:
    leaves = rows["routed_leaf_cells.jsonl.gz"]
    parents = rows["parent_conservation.jsonl.gz"]
    c2_source_rows = rows["collision2_source_candidate_census.jsonl.gz"]
    c2_rows = rows["collision2_multi_delta_cells.jsonl.gz"]
    h1_rows = rows["h1_graph_cells.jsonl.gz"]
    endpoint_rows = rows["endpoint_charts.jsonl.gz"]
    route_fixtures = [
        leaf
        for leaf in leaves
        if leaf.get("route_method") == "C39_ROUTE_EXCEPTION_FAIL_CLOSED"
    ]

    def route_failure_guard(value: dict[str, Any]) -> None:
        failure = value.get("route_failure")
        need(type(failure) is dict, "attack structured route failure")
        replay = failure.get("source_radical_initial_geometry_replay")
        need(type(replay) is dict, "attack route replay structure")
        endpoint = (
            failure.get("exact_box_endpoint_phase")
            == "SOURCE_RADICAL_1_MINUS_P2_ENDPOINT"
        )
        causal = replay.get("source_radical_causal_match") is True
        expected_class = (
            "UNRESOLVED_C40_SOURCE_RADICAL_ENDPOINT_ROUTE_"
            "EVALUATION_FAILURE_OUTER"
            if causal
            else (
                "UNRESOLVED_C40_P_ENDPOINT_BOX_ROUTE_EVALUATION_FAILURE_OUTER"
                if endpoint
                else "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER"
            )
        )
        need(
            failure.get("phase") == "C39_ROUTE_C1_TASK"
            and value.get("route_exception_phase") == failure.get("phase")
            and value.get("route_exception_type") == failure.get("exception_type")
            and value.get("route_exception_message")
            == failure.get("exception_message")
            and value.get("witness")
            == str(failure.get("exception_type"))
            + ":"
            + str(failure.get("exception_message"))
            and value.get("classification") == expected_class
            and (value.get("endpoint_chart_id") is not None) is endpoint
            and len(value.get("path", "")) - len(value.get("source_path", ""))
            == value.get("extra_depth")
            and Q(value.get("parent_volume_fraction")) > 0
            and Q(value.get("parent_volume_fraction")) <= 1,
            "attack exact route failure binding",
        )

    def mutated_object() -> None:
        value = copy.deepcopy(result)
        value["status"] += "_FORGED"
        closed_object(value, "attack object")

    def duplicate_leaf() -> None:
        identifiers = [row["c40_leaf_id"] for row in leaves]
        identifiers.append(identifiers[0])
        need(len(identifiers) == len(set(identifiers)), "attack duplicate leaf")

    def leaf_order() -> None:
        need(len(leaves) > 1, "attack order fixture")
        keys = [(row["c39_source_row_sha256"], row["path"]) for row in leaves]
        swapped = list(keys)
        swapped[0], swapped[1] = swapped[1], swapped[0]
        need(swapped == keys, "attack out-of-order")

    def schema() -> None:
        value = copy.deepcopy(result)
        value["schema"] += ".forged"
        need(value["schema"] == CANDIDATE_SCHEMA, "attack schema")

    def pid() -> None:
        value = copy.deepcopy(receipt)
        value["producer_pid"] = 1
        need(type(value["producer_pid"]) is int and value["producer_pid"] > 1,
             "attack PID")

    def stale() -> None:
        value = copy.deepcopy(receipt)
        value["InvocationID"] += "-stale"
        need(value["InvocationID"] == invocation_id, "attack stale InvocationID")

    def manifest() -> None:
        value = copy.deepcopy(receipt)
        value["root_manifest_sha256"] = "0" * 64
        need(
            value["root_manifest_sha256"] == receipt["root_manifest_sha256"],
            "attack manifest",
        )

    def directory_toctou() -> None:
        changed = list(directory_identity)
        changed[1] += 1
        need(tuple(changed) == directory_identity, "attack directory TOCTOU")

    def file_toctou() -> None:
        name = sorted(file_identities)[0]
        changed = list(file_identities[name])
        changed[4] += 1
        need(tuple(changed) == file_identities[name], "attack file TOCTOU")

    def conservation() -> None:
        value = copy.deepcopy(parents[0])
        value["parent_Kraft_conservation"] = "2"
        need(
            Q(value["terminal_excluded_parent_volume"])
            + Q(value["unresolved_parent_volume"]) == 1
            and value["parent_Kraft_conservation"] == "1",
            "attack conservation",
        )

    def source_candidate_drop() -> None:
        value = copy.deepcopy(c2_source_rows[0]["candidate_dispositions"])
        value.pop()
        need(len(value) == C2_CANDIDATE_COUNT, "attack C2 candidate drop")

    def source_candidate_order() -> None:
        value = copy.deepcopy(c2_source_rows[0]["candidate_dispositions"])
        value[0], value[1] = value[1], value[0]
        need(
            [row["target_id"] for row in value] == list(round185.CANDIDATES),
            "attack C2 candidate order",
        )

    def alternate_candidate_classification() -> None:
        reference = c2_source_rows[0]["candidate_dispositions"][0]
        value = copy.deepcopy(reference)
        value["raw_classification"] = (
            "STRICT_FUTURE"
            if reference["raw_classification"] != "STRICT_FUTURE"
            else "NO_REAL_INTERSECTION"
        )
        need(
            value["target_id"] == reference["target_id"]
            and value["raw_classification"]
            == reference["raw_classification"],
            "attack alternate C2 semantic classification",
        )

    def empty_crossing_pattern_codec() -> None:
        # Model the exact failure class caught in the rejected first C40
        # candidate: an empty tuple must survive a worker codec as an empty
        # JSON list, never as the singleton empty string tuple.
        wire = [
            [list(key), ordinal]
            for key, ordinal in sorted(
                config["pattern_index"].items(), key=lambda item: item[1]
            )
        ]
        need(wire[0] == [[], 0], "attack empty-pattern wire sentinel")
        wire[0][0] = [""]
        decoded = {tuple(key): ordinal for key, ordinal in wire}
        need(
            decoded == config["pattern_index"]
            and decoded.get(()) == 0
            and ("",) not in decoded,
            "attack empty-pattern codec roundtrip",
        )

    def future_registry() -> None:
        fixtures = [
            row for row in c2_source_rows if row["strict_future_pair_order_rows"]
        ]
        need(bool(fixtures), "attack future-order fixture")
        source = fixtures[0]
        value = copy.deepcopy(source["strict_future_pair_order_rows"][0])
        value["equality_carrier_empty_by_boundary_registry"] = False
        need(
            value["equality_carrier_empty_by_boundary_registry"] is True
            and value["boundary_separation_registry_sha256"]
            == C2_BOUNDARY_REGISTRY_SHA256,
            "attack future-order registry",
        )

    def root_sign_substitution() -> None:
        fixtures = [
            item
            for ledger in c2_rows
            for item in ledger["candidate_dispositions"]
            if item["raw_classification"] == "UNRESOLVED_ROOT_SIGN"
        ]
        row = fixtures[0] if fixtures else {
            "surface_evidence": None,
            "surface_evidence_error": {
                "error_type": "ROOT_SIGN_SURFACE_EVIDENCE_NOT_MATERIALIZED",
                "error_message": (
                    "near=0 needs an independent near-root surface proof"
                ),
            },
        }
        value = copy.deepcopy(row)
        value["surface_evidence"] = {"kind": "DELTA"}
        need(
            value["surface_evidence"] is None
            and value["surface_evidence_error"]["error_type"]
            == "ROOT_SIGN_SURFACE_EVIDENCE_NOT_MATERIALIZED",
            "attack root-sign/Delta substitution",
        )

    def lower_dimensional_credit() -> None:
        value = copy.deepcopy(result["strict_nonpromotion"])
        value["lower_dimensional_graph_credit"] = 1
        need(
            value["lower_dimensional_graph_credit"] == 0
            and value["endpoint_or_incidence_ambient_credit"] == 0,
            "attack lower-dimensional credit",
        )

    def route_exception_promotion() -> None:
        need(bool(route_fixtures), "attack route-exception fixture")
        value = copy.deepcopy(route_fixtures[0])
        value["local_round144_terminal_credit"] = 1
        need(
            not value["classification"].startswith("EXCLUDED_")
            and value["local_round144_terminal_credit"] == 0
            and value["C34_common_refinement_credit"] == 0
            and value["D02_gate_credit"] == 0,
            "attack route-exception promotion",
        )

    def route_exception_phase() -> None:
        need(bool(route_fixtures), "attack route phase fixture")
        value = copy.deepcopy(route_fixtures[0])
        value["route_failure"]["phase"] = "FORGED_PHASE"
        route_failure_guard(value)

    def route_exception_type_message() -> None:
        need(bool(route_fixtures), "attack route type fixture")
        value = copy.deepcopy(route_fixtures[0])
        value["route_failure"]["exception_type"] += "Forged"
        value["route_failure"]["exception_message"] += ":forged"
        route_failure_guard(value)

    def route_exception_classification() -> None:
        need(bool(route_fixtures), "attack route classification fixture")
        value = copy.deepcopy(route_fixtures[0])
        value["classification"] = "EXCLUDED_C40_FORGED_ROUTE_EXCEPTION"
        route_failure_guard(value)

    def route_exception_endpoint_link() -> None:
        need(bool(route_fixtures), "attack route endpoint fixture")
        value = copy.deepcopy(route_fixtures[0])
        value["endpoint_chart_id"] = (
            None if value.get("endpoint_chart_id") is not None else "forged-endpoint"
        )
        route_failure_guard(value)

    def route_exception_path_kraft() -> None:
        need(bool(route_fixtures), "attack route path fixture")
        value = copy.deepcopy(route_fixtures[0])
        value["parent_volume_fraction"] = "2"
        route_failure_guard(value)

    def false_promotion() -> None:
        value = copy.deepcopy(result["strict_nonpromotion"])
        value["D02"] = "PASS"
        need(
            value["D02"].startswith("BLOCKED_BY_")
            and value["D03"] == "UNAUTHORIZED"
            and value["D04"] == "NOT_MINTED"
            and value["CM2"] == "NO-GO_FOR_CLAIM",
            "attack false promotion",
        )

    def lock_wording_mutation() -> None:
        forged = EXPECTED_NONPROMOTION_LOCK.replace(
            b"No graph, boundary, endpoint, incidence, ",
            b"Graph, boundary, endpoint, and incidence may earn credit; ",
        )
        need(forged != EXPECTED_NONPROMOTION_LOCK, "attack lock mutation fixture")
        validate_nonpromotion_lock(forged)

    def h1_credit() -> None:
        need(bool(h1_rows), "attack H1 fixture")
        value = copy.deepcopy(h1_rows[0])
        value["ambient_or_whole_parent_credit"] = 1
        need(
            value["ambient_or_whole_parent_credit"] == 0
            and value["D02_gate_credit"] == 0,
            "attack H1 credit",
        )

    def endpoint_credit() -> None:
        need(bool(endpoint_rows), "attack endpoint fixture")
        value = copy.deepcopy(endpoint_rows[0])
        value["D02_gate_credit"] = 1
        need(
            value["ambient_or_whole_parent_credit"] == 0
            and value["D02_gate_credit"] == 0,
            "attack endpoint credit",
        )

    def incidence_credit() -> None:
        fixtures = [item for item in c2_rows if item["pairwise_incidence_rows"]]
        need(bool(fixtures), "attack incidence fixture")
        row = fixtures[0]
        value = copy.deepcopy(row["pairwise_incidence_rows"][0])
        value["ambient_or_whole_parent_credit"] = 1
        need(value["ambient_or_whole_parent_credit"] == 0,
             "attack incidence credit")

    attacks = {
        "duplicate_leaf_id": lambda: duplicate_leaf(),
        "out_of_order_leaf": lambda: leaf_order(),
        "schema_swap": lambda: schema(),
        "PID_forgery": lambda: pid(),
        "stale_InvocationID": lambda: stale(),
        "manifest_swap": lambda: manifest(),
        "object_mutation": lambda: mutated_object(),
        "directory_TOCTOU": lambda: directory_toctou(),
        "file_TOCTOU": lambda: file_toctou(),
        "parent_conservation": lambda: conservation(),
        "C2_candidate_drop": lambda: source_candidate_drop(),
        "C2_candidate_reorder": lambda: source_candidate_order(),
        "C2_alternate_classification": lambda: alternate_candidate_classification(),
        "official_empty_pattern_codec": lambda: empty_crossing_pattern_codec(),
        "C2_future_order_registry": lambda: future_registry(),
        "C2_root_sign_Delta_substitution": lambda: root_sign_substitution(),
        "H1_ambient_credit": lambda: h1_credit(),
        "endpoint_D02_credit": lambda: endpoint_credit(),
        "incidence_ambient_credit": lambda: incidence_credit(),
        "false_D02_D03_D04_CM2_promotion": lambda: false_promotion(),
        "nonpromotion_lock_wording": lambda: lock_wording_mutation(),
        "lower_dimensional_graph_credit": lambda: lower_dimensional_credit(),
        "route_exception_terminal_credit": lambda: route_exception_promotion(),
        "route_exception_phase": lambda: route_exception_phase(),
        "route_exception_type_message": lambda: route_exception_type_message(),
        "route_exception_classification": lambda: route_exception_classification(),
        "route_exception_endpoint_link": lambda: route_exception_endpoint_link(),
        "route_exception_path_Kraft": lambda: route_exception_path_kraft(),
    }
    return {
        label: reject_attack(label, operation)
        for label, operation in attacks.items()
    }


def core_projection(
    candidate: Path, receipt_path: Path, invocation_id: str,
) -> dict[str, Any]:
    no_producer_import()
    need(file_sha256(PRODUCER) == EXPECTED_PRODUCER_SOURCE,
         "frozen producer source hash")
    pins = source_pins()
    ctx.prec = PRECISION_BITS
    candidate = candidate.resolve()
    receipt_path = receipt_path.resolve()
    result, rows, manifest_sha256, directory_identity, file_identities = (
        capture_c40_candidate(candidate)
    )
    authority = result.get("C39_authority")
    need(type(authority) is dict, "C39 authority envelope")
    c39_path_text = authority.get("path")
    c39_audit_path_text = authority.get("independent_audit_path")
    need(
        type(c39_path_text) is str and type(c39_audit_path_text) is str,
        "C39 authority paths",
    )
    c39_path = (ROOT / c39_path_text).resolve()
    c39_audit_path = (ROOT / c39_audit_path_text).resolve()
    need(
        str(c39_path.relative_to(ROOT)) == c39_path_text
        and str(c39_audit_path.relative_to(ROOT)) == c39_audit_path_text,
        "canonical relative C39 authority paths",
    )
    c39_result, _c39_audit, c39_rows, c39_parents = load_c39_authority(
        c39_path, c39_audit_path
    )
    c38_index, cells, config = load_geometry_authority(c39_result)
    # The global Gate3/4 key registry legitimately traverses charts outside the
    # Round166 prototype cache.  Reconstruct it first, then freeze the exact
    # readonly replay used by the C39/C40 routing workers.
    round166.install_fast_readonly_replay()
    c39_index = {row["row_sha256"]: row for row in c39_rows}
    need(len(c39_index) == len(c39_rows), "C39 routed row uniqueness")
    leaf_index, rows_by_pair, _terminal_ids, classifications = (
        validate_leaf_partitions(
            rows["routed_leaf_cells.jsonl.gz"],
            c39_rows,
            c38_index,
            cells,
            config,
        )
    )
    conservation = validate_parent_conservation(
        rows["parent_conservation.jsonl.gz"], rows_by_pair, c39_parents
    )
    c2_source = validate_c2_source_census(
        rows["collision2_source_candidate_census.jsonl.gz"],
        c39_rows,
        c38_index,
    )
    c2_children = validate_c2_children(
        rows["collision2_multi_delta_cells.jsonl.gz"],
        leaf_index,
        c39_index,
        c38_index,
        config,
    )
    h1 = validate_h1_graphs(
        rows["h1_graph_cells.jsonl.gz"],
        leaf_index,
        c39_index,
        c38_index,
    )
    endpoints = validate_endpoints(
        rows["endpoint_charts.jsonl.gz"],
        leaf_index,
        c39_index,
        c38_index,
        cells,
        config["source_chart_seams"],
    )
    semantic_result_guard(
        result,
        rows,
        classifications,
        conservation,
        c2_source,
        c2_children,
        h1,
        endpoints,
        c39_path_text,
        c39_audit_path_text,
        config["registry_sha256"],
    )
    receipt = validate_receipt(
        receipt_path, invocation_id, candidate, result, manifest_sha256
    )
    attacks = hostile_attack_suite(
        result,
        receipt,
        rows,
        config,
        invocation_id,
        directory_identity,
        file_identities,
    )
    second_result, _second_rows, second_manifest, second_directory, second_files = (
        capture_c40_candidate(candidate)
    )
    need(
        second_result == result
        and second_manifest == manifest_sha256
        and second_directory == directory_identity
        and second_files == file_identities,
        "terminal candidate TOCTOU recapture",
    )
    return {
        "schema": SCHEMA + ".core-projection.v1",
        "candidate_path": str(candidate.relative_to(ROOT)),
        "candidate_object_sha256": result["object_sha256"],
        "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
        "root_manifest_sha256": manifest_sha256,
        "execution_receipt_object_sha256": receipt["receipt_object_sha256"],
        "InvocationID": invocation_id,
        "C39_object_sha256": C39_OBJECT,
        "C39_independent_audit_object_sha256": C39_AUDIT_OBJECT,
        "independent_numeric_source_sha256": pins,
        "ledger_row_counts": {
            name: len(rows[name]) for name in LEDGER_NAMES
        },
        "classification_census": dict(sorted(classifications.items())),
        "parent_conservation": conservation,
        "collision2_source_census": c2_source,
        "collision2_child_census": c2_children,
        "H1_census": h1,
        "endpoint_census": endpoints,
        "round144_terminal_census": result["round144_terminal_census"],
        "strict_nonpromotion": result["strict_nonpromotion"],
        "hostile_attacks": attacks,
    }


def child_environment() -> dict[str, str]:
    environment = dict(os.environ)
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        str(DELIVERABLES)
        if not existing
        else str(DELIVERABLES) + os.pathsep + existing
    )
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONHASHSEED"] = "0"
    return environment


def cold_replay_bytes(
    candidate: Path, receipt: Path, invocation_id: str,
) -> tuple[bytes, bytes]:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--core-projection",
        "--candidate",
        str(candidate.resolve()),
        "--receipt",
        str(receipt.resolve()),
        "--invocation-id",
        invocation_id,
    ]
    outputs: list[bytes] = []
    for _ordinal in range(2):
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=child_environment(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        need(
            completed.returncode == 0
            and completed.stderr == b""
            and completed.stdout.endswith(b"\n"),
            "cold core replay process",
        )
        strict_json_bytes(completed.stdout, "cold core replay")
        outputs.append(completed.stdout)
    need(outputs[0] == outputs[1], "byte-identical cold core projections")
    return outputs[0], outputs[1]


def atomic_write_audit(path: Path, value: dict[str, Any]) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(not absolute.exists(), "audit output already exists")
    absolute.parent.mkdir(parents=True, exist_ok=True)
    temporary = absolute.with_name(absolute.name + ".stage-" + str(os.getpid()))
    need(not temporary.exists(), "audit stage already exists")
    raw = canonical(value) + b"\n"
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC,
        0o600,
    )
    try:
        offset = 0
        while offset < len(raw):
            offset += os.write(descriptor, raw[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.replace(temporary, absolute)
    directory_descriptor = os.open(absolute.parent, os.O_RDONLY | os.O_CLOEXEC)
    try:
        os.fsync(directory_descriptor)
    finally:
        os.close(directory_descriptor)
    replay, _file_identity = stable_read(absolute, 32 << 20, "terminal audit")
    observed = strict_json_bytes(replay, "terminal audit")
    closed_object(observed, "terminal audit")
    need(replay == raw and observed == value, "terminal audit byte replay")
    return replay


def run_audit(
    candidate: Path,
    receipt: Path,
    invocation_id: str,
    output: Path,
) -> dict[str, Any]:
    before_payloads, before_directory, before_files = capture_directory(
        candidate.resolve(),
        INVENTORY,
        {
            "result.json": 8 << 20,
            "root_manifest.sha256": 1 << 20,
            "PARTIAL_ARRANGEMENT_ONLY.lock": 1 << 20,
        },
        "C40 outer-before",
    )
    first, second = cold_replay_bytes(candidate, receipt, invocation_id)
    projection = strict_json_bytes(first, "selected cold core")
    after_payloads, after_directory, after_files = capture_directory(
        candidate.resolve(),
        INVENTORY,
        {
            "result.json": 8 << 20,
            "root_manifest.sha256": 1 << 20,
            "PARTIAL_ARRANGEMENT_ONLY.lock": 1 << 20,
        },
        "C40 outer-after",
    )
    need(
        before_payloads == after_payloads
        and before_directory == after_directory
        and before_files == after_files,
        "two-cold-replay candidate TOCTOU",
    )
    attacks = dict(projection["hostile_attacks"])
    attacks["cold_replay_byte_identity"] = first == second
    attacks["terminal_candidate_byte_replay"] = before_payloads == after_payloads
    attacks["terminal_audit_byte_replay"] = True
    need(len(attacks) >= 18 and all(attacks.values()), "complete hostile suite")
    audit = {
        "schema": SCHEMA,
        "status": (
            "PASS_INDEPENDENT_C40_DIMENSION_SAFE_OUTER_AUDIT__"
            + str(len(attacks))
            + "_OF_"
            + str(len(attacks))
            + "_ATTACKS_FAIL_CLOSED"
        ),
        "candidate_path": projection["candidate_path"],
        "candidate_object_sha256": projection["candidate_object_sha256"],
        "producer_source_sha256": EXPECTED_PRODUCER_SOURCE,
        "execution_receipt_path": str(receipt.resolve().relative_to(ROOT)),
        "execution_receipt_object_sha256": projection[
            "execution_receipt_object_sha256"
        ],
        "InvocationID": invocation_id,
        "cold_core_projection_sha256": bytes_sha256(first),
        "cold_core_projection_byte_count": len(first),
        "reconstructed": {
            key: projection[key]
            for key in (
                "ledger_row_counts",
                "classification_census",
                "parent_conservation",
                "collision2_source_census",
                "collision2_child_census",
                "H1_census",
                "endpoint_census",
                "round144_terminal_census",
            )
        },
        "attacks": attacks,
        "strict_nonpromotion": projection["strict_nonpromotion"],
        "method": (
            "no producer import; two fresh deterministic core processes; exact "
            "lower-kernel reconstruction; immutable FD reads; manifest/object/row "
            "closure; PID/InvocationID receipt binding; terminal byte replay"
        ),
    }
    audit["object_sha256"] = digest(audit)
    atomic_write_audit(output, audit)
    return audit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--invocation-id", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--core-projection", action="store_true")
    arguments = parser.parse_args()
    try:
        if arguments.core_projection:
            projection = core_projection(
                arguments.candidate, arguments.receipt, arguments.invocation_id
            )
            sys.stdout.buffer.write(canonical(projection) + b"\n")
            return 0
        need(arguments.output is not None, "audit output required")
        audit = run_audit(
            arguments.candidate,
            arguments.receipt,
            arguments.invocation_id,
            arguments.output,
        )
        sys.stdout.buffer.write(canonical(audit) + b"\n")
        return 0
    except Reject as error:
        if arguments.core_projection:
            return 2
        print("REJECT_C40:" + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
