#!/usr/bin/env python3
"""Independent verifier for Round176 whole-parent exclusion credit.

This verifier imports only the pinned Gate3 candidate/geometry registry.
It does not import or execute the Round165, Round166, Round170, or Round176
producer.  Atlas construction, the owner-active 2,616-parent selection,
depth-8-to-14 replay, H cells, Delta cells, compact-q cells, physical source
clipping, origin summaries, ledger composition, and exact-key layers are
implemented locally.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable, Iterable

from flint import arb, ctx


HERE = Path(__file__).resolve().parent
DELIVERABLES = HERE
sys.path.insert(0, str(HERE))

import cm2_gate3_candidate_first_hit_cert as base


CERTIFICATE = (
    HERE
    / "cm2_round176_dimension_safe_multi_origin_parent_exclusion_certificate.json"
)
OUTPUT = (
    HERE
    / "cm2_round176_dimension_safe_multi_origin_parent_exclusion_verification.json"
)
SCHEMA = (
    "cm2.round176.dimension-safe-multi-origin-parent-exclusion."
    "verification.v1"
)
CERTIFICATE_SCHEMA = (
    "cm2.round176.dimension-safe-multi-origin-parent-exclusion.v1"
)
PRODUCER = (
    HERE / "cm2_round176_dimension_safe_multi_origin_parent_exclusion.py"
)
# Filled after the final producer replay.
PRODUCER_SHA256 = (
    "dc1668d868687bb1c6bb2cc458f2aed8cf35308c852d7ba92e75eddc7e848086"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "bb255bf9dbf1c6cb6680ea32b57ad31c03f108a8af5c345a2f7ca3ab88a22fa8"
)
EXPECTED_CERTIFICATE_RESULT_SHA256 = (
    "3090fb2f58fff50f0c9ab89b7a228042f49d5d929cd53e9c358e31a4d977254e"
)
MAX_INPUT_BYTES = 4 * 1024 * 1024
PINS = {
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate3_ge_interval_atlas_cert.py":
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json":
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
    "cm2_round166_multi_candidate_refinement_prototype.py":
        "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
    "cm2_round170_bounded_dimension_safe_graph_cells.py":
        "952ac26c6729a02e3c5c364c8dda89cdc19b756ac46f7d5da01786fa1b7ca75f",
    "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning.py":
        "81f147cf6106d7436df282de106fc47e793e8f97a43282b35719e28182e07980",
    "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning_certificate.json":
        "3185188c476a64d3e732674fa724ce9a49afe84c61abab448f746a5a3555b66c",
    "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning_verification.json":
        "d095ecdd1b59a6577f96f0317f8a30122e8cd3f6baf73ed550c5d227ed1811c3",
    "cm2_round175_dimension_safe_tangency_arrangement.py":
        "16122dcc7c39b140d45139a01bac6d6f41d7cbb60da2499ecc50fbeac2766355",
    "cm2_round175_dimension_safe_tangency_arrangement_certificate.json":
        "a2a69b3d4559fadb647d8f9ea6a06ef4c1625647965423cdb25f53fa08d2deee",
    "cm2_round175_dimension_safe_tangency_arrangement_verifier.py":
        "2c8a5906806adef423ba5d409cbf294c4988db72a1b9cfdf26a61ee9a7d290e6",
    "cm2_round175_dimension_safe_tangency_arrangement_verification.json":
        "6f1d8e515be0cdc977445e7e0d8633df510c793ff99e0f76cf3b4578d2d2bfca",
    "cm2_round175_dimension_safe_tangency_arrangement_manifest.sha256":
        "0ad7140947512de88f5ff4badd5a925c78b9f605be1f519841485f41b9139dc3",
}
ROUND172_RESULT = (
    "a436b4a82b1e8d5c617fe576e0e4e76b6f6f38ad8ac3eda4ddde544c2769a776"
)
ROUND172_VERIFICATION_RESULT = (
    "aa0fb2c28176cf46b058506658a21070679e0a91a4f94ed65245fb378e088603"
)
ROUND175_RESULT = (
    "827d6f674dd4a5291bf08f5ffd65b31187faa1c9fe977e1b7e7da10cd1166d72"
)
ROUND175_VERIFICATION_RESULT = (
    "ed5fd96874a65b49a1e05d5589e2dd9711f224d08a99123e582bc54bce294f6a"
)


ctx.prec = 192
T_LOWER = Q(-177, 250)
T_UPPER = Q(177, 250)
P_LOWER = Q(-1)
P_UPPER = Q(1)
S_LOWER = -base.EPS
S_UPPER = base.EPS
INITIAL_T = 8
INITIAL_P = 16
MAX_DEPTH = 8
FROZEN_OWNER = "W[1,0]"
FROZEN_CHART = "W"
CHARTS = ("W:E", "W:N", "W:S")

CANDIDATES = {
    chart: tuple(base.candidate_ids(chart)) for chart in CHARTS
}
TARGETS = {target.target_id: target for target in base.TARGETS}


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def validate_json_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(
                type(key) is str
                and "\x00" not in key
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in key
                ),
                f"JSON key:{path}",
            )
            validate_json_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_json_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require(
            "\x00" not in value
            and not any(
                0xD800 <= ord(character) <= 0xDFFF
                for character in value
            ),
            f"JSON string:{path}",
        )


def strict_parse(raw: bytes, label: str) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"encoding:{label}",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate:{label}:{key}")
            result[key] = value
        return result

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )
    validate_json_tree(value)
    require(type(value) is dict, f"top:{label}")
    return value


def strict_load(path: Path) -> dict[str, Any]:
    return strict_parse(path.read_bytes(), path.name)


def read_regular(
    path: Path,
    expected_sha256: str | None = None,
) -> bytes:
    status = path.lstat()
    require(stat.S_ISREG(status.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(status.st_nlink == 1, f"hardlink:{path.name}")
    require(status.st_size <= MAX_INPUT_BYTES, f"size:{path.name}")
    raw = path.read_bytes()
    if expected_sha256 is not None:
        require(
            hashlib.sha256(raw).hexdigest() == expected_sha256,
            f"pin:{path.name}",
        )
    return raw


def parse_envelope(
    raw: bytes,
    *,
    label: str,
    expected_schema: str | None = None,
    canonical_pretty: bool = False,
) -> dict[str, Any]:
    value = strict_parse(raw, label)
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"envelope:{label}",
    )
    if expected_schema is not None:
        require(value["schema"] == expected_schema, f"schema:{label}")
    require(
        value["result_sha256"] == digest(value["result"]),
        f"result digest:{label}",
    )
    if canonical_pretty:
        require(raw == pretty_bytes(value), f"canonical bytes:{label}")
    return value


def map_counter(value: Counter[Any]) -> dict[str, int]:
    return {
        str(key): count for key, count in sorted(value.items())
    }


def fraction_map(value: dict[str, Q]) -> dict[str, str]:
    return {
        key: str(item) for key, item in sorted(value.items())
    }


def hull(lower: arb, upper: arb) -> arb:
    middle = (lower + upper) / 2
    radius = (upper - lower) / 2
    return middle + arb(0, radius.upper())


def sqrt_one_minus_square(lower: Q, upper: Q) -> arb:
    require(Q(-1) <= lower <= upper <= Q(1), "sqrt domain")
    maximum_abs = max(abs(lower), abs(upper))
    minimum_abs = (
        Q(0) if lower <= 0 <= upper else min(abs(lower), abs(upper))
    )
    lo = base.arbq(1 - maximum_abs * maximum_abs).sqrt()
    hi = base.arbq(1 - minimum_abs * minimum_abs).sqrt()
    return hull(lo.lower(), hi.upper())


@dataclass(frozen=True)
class Box:
    t0: Q
    t1: Q
    p0: Q
    p1: Q
    s0: Q
    s1: Q
    depth: int
    path: str


@dataclass(frozen=True)
class Root:
    target_id: str
    classification: str
    ell: arb
    discriminant: arb
    near: arb | None
    far: arb | None
    transverse: arb


@dataclass(frozen=True)
class Leaf:
    box: Box
    classification: str
    owner_target: str | None
    active_targets: tuple[str, ...]
    tangency_targets: tuple[str, ...]


@dataclass(frozen=True)
class Node:
    chart_id: str
    box: Box
    active_targets: tuple[str, ...]
    origin_path: str


@dataclass(frozen=True)
class Frontier:
    chart_id: str
    box: Box
    active_targets: tuple[str, ...]
    origin_key: str
    failure: str

    @property
    def key(self) -> str:
        return f"{self.chart_id}:{self.box.path}"


def geometry(chart_id: str, box: Box):
    source, cell = chart_id.split(":")
    require(source == "W", "source W")
    t = base.arb_interval(box.t0, box.t1)
    p = base.arb_interval(box.p0, box.p1)
    s = base.arb_interval(box.s0, box.s1)
    rt = sqrt_one_minus_square(box.t0, box.t1)
    rp = sqrt_one_minus_square(box.p0, box.p1)
    if cell == "E":
        nx, ny = rt, t
    elif cell == "N":
        nx, ny = t, rt
    elif cell == "S":
        nx, ny = t, -rt
    else:
        raise ValueError(cell)
    ux = rp * nx - p * ny
    uy = rp * ny + p * nx
    cx = base.arbq(Q(1, 2)) + s
    cy = base.arbq(Q(1, 2))
    radius = base.arbq(base.RADIUS["W"])
    return cx + radius * nx, cy + radius * ny, ux, uy, s, rp


def root_from_geometry(geom, target_id: str) -> Root:
    qx, qy, ux, uy, s, _rp = geom
    target = TARGETS[target_id]
    ax, ay = base.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = base.arbq(base.RADIUS[target.obstacle])
    delta = radius * radius - transverse * transverse
    if bool(delta < 0):
        return Root(
            target_id, "no_real_intersection", ell, delta,
            None, None, transverse,
        )
    if not bool(delta > 0):
        return Root(
            target_id, "unresolved_discriminant", ell, delta,
            None, None, transverse,
        )
    radical = delta.sqrt()
    near, far = ell - radical, ell + radical
    classification = (
        "intersection_behind"
        if bool(far < 0)
        else (
            "strict_future_root"
            if bool(near > 0)
            else "unresolved_root_sign"
        )
    )
    return Root(
        target_id, classification, ell, delta,
        near, far, transverse,
    )


def records_for(
    chart_id: str,
    box: Box,
    target_ids: Iterable[str],
) -> list[Root]:
    geom = geometry(chart_id, box)
    return [
        root_from_geometry(geom, target_id)
        for target_id in target_ids
    ]


def root_at_p(
    chart_id: str,
    box: Box,
    target_id: str,
    p: Q,
) -> Root:
    face = Box(
        box.t0, box.t1, p, p, box.s0, box.s1,
        box.depth, box.path,
    )
    return records_for(chart_id, face, (target_id,))[0]


def earliest_lower(record: Root) -> arb | None:
    if record.classification in {
        "no_real_intersection",
        "intersection_behind",
    }:
        return None
    if (
        record.classification == "strict_future_root"
        and record.near is not None
    ):
        return record.near.lower()
    upper = record.discriminant.upper()
    if not bool(upper > 0):
        return None
    return record.ell.lower() - upper.sqrt().upper()


def physical_tangency(
    chart_id: str,
    box: Box,
    candidate: Root,
    records: list[Root],
) -> bool:
    if candidate.classification != "unresolved_discriminant":
        return False
    if box.p0 <= -1 or box.p1 >= 1:
        return False
    *_unused, rp = geometry(chart_id, box)
    if not (
        bool(rp > 0)
        and bool(candidate.ell > 0)
        and bool(candidate.ell < base.arbq(base.TAU_MAX))
    ):
        return False
    derivative = 2 * candidate.transverse * candidate.ell / rp
    if not (bool(derivative > 0) or bool(derivative < 0)):
        return False
    low = root_at_p(
        chart_id, box, candidate.target_id, box.p0
    ).discriminant
    high = root_at_p(
        chart_id, box, candidate.target_id, box.p1
    ).discriminant
    if bool(derivative > 0):
        if not (bool(low < 0) and bool(high > 0)):
            return False
    elif not (bool(low > 0) and bool(high < 0)):
        return False
    for other in records:
        if other.target_id == candidate.target_id:
            continue
        if other.classification in {
            "no_real_intersection",
            "intersection_behind",
        }:
            continue
        lower = earliest_lower(other)
        if lower is None or not bool(candidate.ell < lower):
            return False
    return True


def classify_records(
    chart_id: str,
    box: Box,
    records: list[Root],
) -> Leaf:
    strict = [
        record for record in records
        if record.classification == "strict_future_root"
    ]
    unresolved = [
        record for record in records
        if record.classification in {
            "unresolved_discriminant",
            "unresolved_root_sign",
        }
    ]
    if not strict and not unresolved:
        return Leaf(box, "no_future_root", None, (), ())
    for candidate in strict:
        require(candidate.near is not None, "near")
        if all(
            other.target_id == candidate.target_id
            or other.classification in {
                "no_real_intersection",
                "intersection_behind",
            }
            or (
                (lower := earliest_lower(other)) is not None
                and bool(candidate.near < lower)
            )
            for other in records
        ):
            return Leaf(
                box, "unique_first", candidate.target_id,
                (candidate.target_id,), (),
            )
    tangencies = tuple(
        record.target_id
        for record in unresolved
        if physical_tangency(
            chart_id, box, record, records
        )
    )
    if len(tangencies) == 1:
        return Leaf(
            box, "tangency_graph", tangencies[0],
            tangencies, tangencies,
        )
    active: set[str] = set()
    for candidate in strict + unresolved:
        lower = earliest_lower(candidate)
        if lower is None or not any(
            other.target_id != candidate.target_id
            and other.near is not None
            and bool(other.near < lower)
            for other in strict
        ):
            active.add(candidate.target_id)
    return Leaf(
        box, "multi_candidate", None,
        tuple(sorted(active)), tangencies,
    )


def classify(
    chart_id: str,
    box: Box,
    targets: Iterable[str],
) -> tuple[Leaf, list[Root]]:
    records = records_for(chart_id, box, targets)
    return classify_records(chart_id, box, records), records


def split(box: Box, axis: int | None = None) -> tuple[Box, Box]:
    widths = (
        box.t1 - box.t0,
        box.p1 - box.p0,
        box.s1 - box.s0,
    )
    if axis is None:
        axis = max(range(3), key=lambda index: widths[index])
    depth = box.depth + 1
    if axis == 0:
        middle = (box.t0 + box.t1) / 2
        return (
            Box(
                box.t0, middle, box.p0, box.p1,
                box.s0, box.s1, depth, box.path + "0",
            ),
            Box(
                middle, box.t1, box.p0, box.p1,
                box.s0, box.s1, depth, box.path + "1",
            ),
        )
    if axis == 1:
        middle = (box.p0 + box.p1) / 2
        return (
            Box(
                box.t0, box.t1, box.p0, middle,
                box.s0, box.s1, depth, box.path + "0",
            ),
            Box(
                box.t0, box.t1, middle, box.p1,
                box.s0, box.s1, depth, box.path + "1",
            ),
        )
    middle = (box.s0 + box.s1) / 2
    return (
        Box(
            box.t0, box.t1, box.p0, box.p1,
            box.s0, middle, depth, box.path + "0",
        ),
        Box(
            box.t0, box.t1, box.p0, box.p1,
            middle, box.s1, depth, box.path + "1",
        ),
    )


def initial_boxes() -> list[Box]:
    return [
        Box(
            T_LOWER + (T_UPPER - T_LOWER) * Q(i, INITIAL_T),
            T_LOWER + (T_UPPER - T_LOWER) * Q(i + 1, INITIAL_T),
            P_LOWER + (P_UPPER - P_LOWER) * Q(j, INITIAL_P),
            P_LOWER + (P_UPPER - P_LOWER) * Q(j + 1, INITIAL_P),
            S_LOWER,
            S_UPPER,
            0,
            f"{i:02d}.{j:02d}.",
        )
        for i in range(INITIAL_T)
        for j in range(INITIAL_P)
    ]


def build_atlas(chart_id: str) -> list[Leaf]:
    pending = initial_boxes()
    leaves: list[Leaf] = []
    while pending:
        box = pending.pop()
        leaf, _records = classify(
            chart_id, box, CANDIDATES[chart_id]
        )
        if leaf.classification in {
            "unique_first", "tangency_graph", "no_future_root",
        } or box.depth >= MAX_DEPTH:
            leaves.append(leaf)
        else:
            pending.extend(split(box))
    return sorted(leaves, key=lambda leaf: leaf.box.path)


def target_parts(target_id: str) -> tuple[str, int, int]:
    target = TARGETS[target_id]
    return target.obstacle, target.ix, target.iy


def reflected_target(source: str, value: str) -> str:
    obstacle, ix, iy = target_parts(value)
    if source == "G":
        reflected_iy = -iy if obstacle == "G" else -iy - 1
    else:
        reflected_iy = 1 - iy if obstacle == "G" else -iy
    return f"{obstacle}[{ix},{reflected_iy}]"


def reflect_horizontal(leaf: Leaf) -> Leaf:
    box = leaf.box
    mapped = Box(
        box.t0, box.t1, -box.p1, -box.p0,
        box.s0, box.s1, box.depth, "H." + box.path,
    )
    mapper = lambda value: reflected_target("W", value)
    return Leaf(
        mapped,
        leaf.classification,
        (
            None
            if leaf.owner_target is None
            else mapper(leaf.owner_target)
        ),
        tuple(sorted(mapper(value) for value in leaf.active_targets)),
        tuple(sorted(mapper(value) for value in leaf.tangency_targets)),
    )


def outgoing_generic(
    chart_id: str,
    box: Box,
) -> tuple[str | None, dict[str, arb]]:
    record = records_for(
        chart_id, box, (FROZEN_OWNER,)
    )[0]
    require(
        record.classification == "strict_future_root"
        and record.near is not None,
        "owner root",
    )
    qx, qy, ux, uy, s, _rp = geometry(chart_id, box)
    target = TARGETS[FROZEN_OWNER]
    cx, cy = base.target_center(target, s)
    radius = base.arbq(base.RADIUS["W"])
    nx = (qx + record.near * ux - cx) / radius
    ny = (qy + record.near * uy - cy) / radius
    margins = {
        "E.first": nx - ny,
        "E.second": nx + ny,
        "W.first": -nx - ny,
        "W.second": -nx + ny,
        "N.first": ny - nx,
        "N.second": ny + nx,
        "S.first": -ny - nx,
        "S.second": -ny + nx,
    }
    for cell in ("E", "W", "N", "S"):
        if (
            bool(margins[f"{cell}.first"] > 0)
            and bool(margins[f"{cell}.second"] > 0)
        ):
            return cell, margins
    return None, margins


def terminal_disposition(
    chart_id: str,
    leaf: Leaf,
) -> tuple[str | None, dict[str, arb] | None]:
    if leaf.classification == "no_future_root":
        return "EXCLUDED_NO_INHERITED_FUTURE_ROOT", None
    if leaf.classification == "tangency_graph":
        return None, None
    if leaf.classification != "unique_first":
        return None, None
    if leaf.owner_target != FROZEN_OWNER:
        return "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH", None
    cell, margins = outgoing_generic(chart_id, leaf.box)
    if cell is None:
        return None, margins
    if cell == FROZEN_CHART:
        return "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH", margins
    return "EXCLUDED_OUTGOING_CHART_MISMATCH", margins


def grazing(box: Box) -> bool:
    return box.p0 == -1 or box.p1 == 1


def failure_type(
    leaf: Leaf,
    records: list[Root],
    seam_margins: dict[str, arb] | None,
) -> str:
    if leaf.classification == "tangency_graph":
        return (
            "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR"
            if leaf.owner_target == FROZEN_OWNER
            else "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR"
        )
    if leaf.classification == "unique_first":
        require(seam_margins is not None, "seam margins")
        ambiguous = [
            value
            for value in (
                seam_margins["E.first"],
                seam_margins["E.second"],
            )
            if not bool(value > 0) and not bool(value < 0)
        ]
        return (
            "OUTGOING_CHART_CORNER_OVERWRAP"
            if len(ambiguous) == 2
            else "OUTGOING_CHART_SEAM_OVERWRAP"
        )
    if grazing(leaf.box):
        return "SOURCE_GRAZING_ENDPOINT_COLLAR"
    classes = Counter(record.classification for record in records)
    if classes["unresolved_root_sign"]:
        return "UNRESOLVED_ROOT_SIGN"
    if classes["unresolved_discriminant"]:
        return "UNTYPED_DISCRIMINANT_COLLAR"
    if classes["strict_future_root"] >= 2:
        return "STRICT_ROOT_ORDER_OVERLAP"
    return "MIXED_INTERVAL_DEPENDENCY"


def replay_frontier() -> dict[str, Any]:
    direct_e = build_atlas("W:E")
    direct_n = build_atlas("W:N")
    charts = {
        "W:E": direct_e,
        "W:N": direct_n,
        "W:S": [reflect_horizontal(leaf) for leaf in direct_n],
    }
    counts = {
        chart: Counter(leaf.classification for leaf in leaves)
        for chart, leaves in charts.items()
    }
    require(
        len(direct_e) == 18930
        and len(direct_n) == 19484
        and counts["W:E"]["multi_candidate"] == 12388
        and counts["W:N"]["multi_candidate"] == 12896,
        "baseline census",
    )
    pending: list[Node] = []
    origins: dict[str, dict[str, Any]] = {}
    for chart_id, leaves in charts.items():
        for leaf in leaves:
            if (
                leaf.classification == "multi_candidate"
                and FROZEN_OWNER in leaf.active_targets
            ):
                key = f"{chart_id}:{leaf.box.path}"
                require(key not in origins, f"duplicate origin:{key}")
                origins[key] = {
                    "chart_id": chart_id,
                    "path": leaf.box.path,
                    "box": leaf.box,
                    "active_targets": tuple(leaf.active_targets),
                }
                pending.append(
                    Node(
                        chart_id,
                        leaf.box,
                        leaf.active_targets,
                        leaf.box.path,
                    )
                )
    require(len(pending) == 2616, f"owner active:{len(pending)}")
    frontier: list[Frontier] = []
    origin_kinds: dict[str, set[str]] = defaultdict(set)
    prior: dict[str, list[dict[str, Any]]] = defaultdict(list)
    terminal_counts: Counter[str] = Counter()
    evaluated_by_origin: Counter[str] = Counter()
    evaluated_boxes = 0
    evaluated_records = 0
    for relative_depth in range(7):
        next_pending: list[Node] = []
        for node in pending:
            origin = f"{node.chart_id}:{node.origin_path}"
            evaluated_by_origin[origin] += 1
            leaf, records = classify(
                node.chart_id, node.box, node.active_targets
            )
            evaluated_boxes += 1
            evaluated_records += len(node.active_targets)
            disposition, margins = terminal_disposition(
                node.chart_id, leaf
            )
            if disposition is not None:
                terminal_counts[disposition] += 1
                evidence: dict[str, Any] = {
                    "leaf_key": f"{node.chart_id}:{node.box.path}",
                    "relative_depth": relative_depth,
                    "dimension": 3,
                    "disposition": disposition,
                    "coverage_numerator_64":
                        2 ** (6 - relative_depth),
                }
                if margins is not None:
                    evidence["closed_interval_outgoing_margin_signs"] = {
                        key: (
                            "POSITIVE"
                            if bool(value > 0)
                            else (
                                "NEGATIVE"
                                if bool(value < 0)
                                else "OVERWRAPPED"
                            )
                        )
                        for key, value in sorted(margins.items())
                    }
                prior[origin].append(evidence)
                origin_kinds[origin].add(
                    "EXCLUDED"
                    if disposition.startswith("EXCLUDED")
                    else "LIVE"
                )
                continue
            failure = failure_type(leaf, records, margins)
            if leaf.classification == "unique_first":
                inherited = (FROZEN_OWNER,)
            elif leaf.classification == "tangency_graph":
                inherited = node.active_targets
            else:
                inherited = leaf.active_targets
            if relative_depth == 6:
                frontier.append(
                    Frontier(
                        node.chart_id,
                        node.box,
                        inherited,
                        origin,
                        failure,
                    )
                )
            else:
                axis = max(
                    range(3),
                    key=lambda index: (
                        node.box.t1 - node.box.t0,
                        node.box.p1 - node.box.p0,
                        node.box.s1 - node.box.s0,
                    )[index],
                )
                next_pending.extend(
                    Node(
                        node.chart_id,
                        child,
                        inherited,
                        node.origin_path,
                    )
                    for child in split(node.box, axis)
                )
        pending = next_pending
    require(
        len(frontier) == 56780
        and evaluated_boxes == 167984
        and evaluated_records == 415570,
        "frontier workload",
    )
    return {
        "frontier": frontier,
        "origin_kinds": origin_kinds,
        "origins": origins,
        "prior": prior,
        "terminal_counts": terminal_counts,
        "evaluated_by_origin": evaluated_by_origin,
        "workload": {
            "evaluated_box_count": evaluated_boxes,
            "evaluated_target_record_count": evaluated_records,
        },
    }


def sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def source_frame(chart_id: str, box: Box):
    cell = chart_id.split(":")[1]
    t = base.arb_interval(box.t0, box.t1)
    p = base.arb_interval(box.p0, box.p1)
    rt = sqrt_one_minus_square(box.t0, box.t1)
    rp = sqrt_one_minus_square(box.p0, box.p1)
    require(bool(rt > 0), "frame radical")
    if cell == "E":
        nx, ny = rt, t
        dnx, dny = -t / rt, arb(1)
    elif cell == "N":
        nx, ny = t, rt
        dnx, dny = arb(1), -t / rt
    elif cell == "S":
        nx, ny = t, -rt
        dnx, dny = arb(1), t / rt
    else:
        raise ValueError(cell)
    ux = rp * nx - p * ny
    uy = rp * ny + p * nx
    dux = rp * dnx - p * dny
    duy = rp * dny + p * dnx
    return nx, ny, dnx, dny, ux, uy, dux, duy


def tight_contact(chart_id: str, box: Box):
    nx, ny, _dnx, _dny, ux, uy, _dux, _duy = source_frame(
        chart_id, box
    )
    radius = base.arbq(base.RADIUS["W"])
    dx = arb(1) - radius * nx
    dy = -radius * ny
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    delta = radius * radius - transverse * transverse
    require(bool(delta > 0), "tight delta")
    radical = delta.sqrt()
    near = ell - radical
    require(bool(near > 0), "tight near")
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    tests = {
        "E": (normal_x - normal_y, normal_x + normal_y),
        "W": (-normal_x - normal_y, -normal_x + normal_y),
        "N": (normal_y - normal_x, normal_y + normal_x),
        "S": (-normal_y - normal_x, -normal_y + normal_x),
    }
    for cell in ("E", "W", "N", "S"):
        if bool(tests[cell][0] > 0) and bool(tests[cell][1] > 0):
            return cell, normal_x, normal_y
    return None, normal_x, normal_y


SEAMS = {
    "NW": {
        "signs": (-1, 1),
        "adjacent": "N",
        "normal": lambda nx, ny: nx + ny,
        "other": lambda nx, ny: nx - ny,
    },
    "SW": {
        "signs": (-1, -1),
        "adjacent": "S",
        "normal": lambda nx, ny: nx - ny,
        "other": lambda nx, ny: nx + ny,
    },
}


def point_box(
    box: Box,
    t_value: Q | None = None,
    p_value: Q | None = None,
) -> Box:
    return Box(
        box.t0 if t_value is None else t_value,
        box.t1 if t_value is None else t_value,
        box.p0 if p_value is None else p_value,
        box.p1 if p_value is None else p_value,
        box.s0,
        box.s1,
        box.depth,
        box.path,
    )


def seam_values(chart_id: str, box: Box, seam_id: str):
    data = SEAMS[seam_id]
    inv = base.arbq(Q(1, 2)).sqrt()
    mx = data["signs"][0] * inv
    my = data["signs"][1] * inv
    nx, ny, dnx, dny, ux, uy, dux, duy = source_frame(
        chart_id, box
    )
    radius = base.arbq(base.RADIUS["W"])
    dx = arb(1) + radius * mx - radius * nx
    dy = radius * my - radius * ny
    ddx, ddy = -radius * dnx, -radius * dny
    cross = ux * dy - uy * dx
    forward = ux * dx + uy * dy
    inward = -(ux * mx + uy * my)
    dt = dux * dy - duy * dx + ux * ddy - uy * ddx
    rp = sqrt_one_minus_square(box.p0, box.p1)
    dp = -forward / rp
    return {
        "H": cross,
        "forward": forward,
        "inward": inward,
        "dt": dt,
        "dp": dp,
    }


def seam_terminal(chart_id: str, box: Box) -> str | None:
    cell, nx, ny = tight_contact(chart_id, box)
    if cell is not None:
        return (
            "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE"
            if cell != FROZEN_CHART
            else "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE"
        )
    separated: list[str] = []
    typed = 0
    for seam_id, data in SEAMS.items():
        normal = data["normal"](nx, ny)
        other = data["other"](nx, ny)
        if sign(normal) != 0 or not bool(other < 0):
            continue
        values = seam_values(chart_id, box, seam_id)
        if not (
            bool(values["forward"] > 0)
            and bool(values["inward"] > 0)
            and bool(values["dp"] < 0)
        ):
            continue
        corners = [
            seam_values(
                chart_id,
                point_box(box, t_value=t, p_value=p),
                seam_id,
            )["H"]
            for t in (box.t0, box.t1)
            for p in (box.p0, box.p1)
        ]
        corner_signs = [sign(value) for value in corners]
        dt_sign = sign(values["dt"])
        if (
            dt_sign != 0
            and (
                all(value == 1 for value in corner_signs)
                or all(value == -1 for value in corner_signs)
            )
        ):
            h_sign = corner_signs[0]
            outgoing = (
                ("W" if h_sign > 0 else "N")
                if seam_id == "NW"
                else ("W" if h_sign < 0 else "S")
            )
            separated.append(
                (
                    "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE"
                    if outgoing != "W"
                    else "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE"
                )
            )
            continue
        low = seam_values(
            chart_id, point_box(box, p_value=box.p0), seam_id
        )["H"]
        high = seam_values(
            chart_id, point_box(box, p_value=box.p1), seam_id
        )["H"]
        full_graph = bool(low > 0) and bool(high < 0)
        clipped = (
            dt_sign != 0
            and 1 in corner_signs
            and -1 in corner_signs
        )
        if full_graph or clipped:
            typed += 1
    if len(separated) == 1 and typed == 0:
        return separated[0]
    if typed == 1 and not separated:
        return "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES"
    return None


H_EXCLUDED = {
    "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE",
    "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE",
}
H_LIVE = {
    "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
    "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
}


def h_partition(
    row: Frontier,
) -> tuple[str | None, Counter[str], Counter[int]]:
    pending = [(row.box, 0)]
    classes: Counter[str] = Counter()
    depths: Counter[int] = Counter()
    while pending:
        box, depth = pending.pop()
        classification = seam_terminal(row.chart_id, box)
        if classification is not None:
            classes[classification] += 1
            depths[depth] += 1
            continue
        if depth >= 4:
            return None, classes, depths
        t_width = (box.t1 - box.t0) / (T_UPPER - T_LOWER)
        p_width = (box.p1 - box.p0) / (P_UPPER - P_LOWER)
        axis = 0 if t_width >= p_width else 1
        pending.extend(
            (child, depth + 1) for child in split(box, axis)
        )
    kinds = set(classes)
    if kinds <= H_EXCLUDED:
        return "EXCLUDED", classes, depths
    if kinds <= H_LIVE:
        return "LIVE", classes, depths
    return "MIXED", classes, depths


def remove_disposition(
    row: Frontier,
    records: list[Root],
    target_id: str,
) -> str | None:
    leaf = classify_records(
        row.chart_id,
        row.box,
        [
            record for record in records
            if record.target_id != target_id
        ],
    )
    disposition, _margins = terminal_disposition(
        row.chart_id, leaf
    )
    return disposition


def target_positive_first(candidate: Root, records: list[Root]) -> bool:
    radius = base.arbq(
        base.RADIUS[TARGETS[candidate.target_id].obstacle]
    )
    if not (
        bool(candidate.ell - radius > 0)
        and bool(candidate.ell < base.arbq(base.TAU_MAX))
    ):
        return False
    return all(
        other.target_id == candidate.target_id
        or other.classification in {
            "no_real_intersection",
            "intersection_behind",
        }
        or (
            (lower := earliest_lower(other)) is not None
            and bool(candidate.ell < lower)
        )
        for other in records
    )


def positive_chart(row: Frontier, candidate: Root) -> str | None:
    _qx, _qy, ux, uy, _s, _rp = geometry(
        row.chart_id, row.box
    )
    upper = candidate.discriminant.upper()
    if not bool(upper > 0):
        return None
    h = hull(arb(0), upper.sqrt().upper())
    radius = base.arbq(
        base.RADIUS[TARGETS[candidate.target_id].obstacle]
    )
    transverse = candidate.transverse
    nx = (transverse * uy - h * ux) / radius
    ny = (-transverse * ux - h * uy) / radius
    tests = {
        "E": (nx - ny, nx + ny),
        "W": (-nx - ny, -nx + ny),
        "N": (ny - nx, ny + nx),
        "S": (-ny - nx, -ny + nx),
    }
    cells = [
        cell for cell, values in tests.items()
        if bool(values[0] > 0) and bool(values[1] > 0)
    ]
    return cells[0] if len(cells) == 1 else None


def graph_faces(row: Frontier, candidate: Root):
    *_unused, rp = geometry(row.chart_id, row.box)
    derivative = (
        2 * candidate.transverse * candidate.ell / rp
        if bool(rp > 0)
        else arb(0)
    )
    ds = sign(derivative)
    low = root_at_p(
        row.chart_id, row.box, candidate.target_id, row.box.p0
    ).discriminant
    high = root_at_p(
        row.chart_id, row.box, candidate.target_id, row.box.p1
    ).discriminant
    full = (
        ds > 0 and bool(low < 0) and bool(high > 0)
    ) or (
        ds < 0 and bool(low > 0) and bool(high < 0)
    )
    return ds, low, high, full


def close_tangency(row: Frontier) -> tuple[bool, str]:
    records = records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = [
        record for record in records
        if record.classification == "unresolved_discriminant"
    ]
    if len(unresolved) != 1:
        return False, "NOT_SINGLE_DISCRIMINANT"
    candidate = unresolved[0]
    ds, _low, _high, full = graph_faces(row, candidate)
    if ds == 0 or not full or not target_positive_first(
        candidate, records
    ):
        return False, "NOT_FULL_MONOTONE_OR_NOT_STRICT_FIRST"
    negative = remove_disposition(
        row, records, candidate.target_id
    )
    if negative is None or not negative.startswith("EXCLUDED"):
        return False, "NEGATIVE_OPEN_SIDE_NOT_WHOLE_EXCLUDED"
    if candidate.target_id != FROZEN_OWNER:
        positive = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
        graph = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
        return True, (
            f"NEGATIVE={negative}|GRAPH={graph}|POSITIVE={positive}"
        )
    chart = positive_chart(row, candidate)
    if chart is None or chart == FROZEN_CHART:
        return False, "POSITIVE_OR_GRAPH_OUTGOING_NOT_MISMATCH"
    positive = "EXCLUDED_OUTGOING_CHART_MISMATCH"
    graph = "EXCLUDED_OUTGOING_CHART_MISMATCH"
    return True, (
        f"NEGATIVE={negative}|GRAPH={graph}|POSITIVE={positive}"
    )


def enhanced_record(
    candidate: Root,
    low: arb,
    high: arb,
    ds: int,
) -> Root:
    delta = (
        hull(low.lower(), high.upper())
        if ds > 0
        else hull(high.lower(), low.upper())
    )
    if bool(delta < 0):
        return Root(
            candidate.target_id,
            "no_real_intersection",
            candidate.ell,
            delta,
            None,
            None,
            candidate.transverse,
        )
    require(bool(delta > 0), "enhanced delta")
    radical = delta.sqrt()
    near, far = candidate.ell - radical, candidate.ell + radical
    classification = (
        "intersection_behind"
        if bool(far < 0)
        else (
            "strict_future_root"
            if bool(near > 0)
            else "unresolved_root_sign"
        )
    )
    return Root(
        candidate.target_id, classification, candidate.ell,
        delta, near, far, candidate.transverse,
    )


def close_same_sign(row: Frontier) -> tuple[str | None, str]:
    records = records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = [
        record for record in records
        if record.classification == "unresolved_discriminant"
    ]
    if len(unresolved) != 1:
        return None, "NOT_SINGLE_DISCRIMINANT"
    candidate = unresolved[0]
    ds, low, high, _full = graph_faces(row, candidate)
    if not (
        ds != 0 and sign(low) != 0 and sign(low) == sign(high)
    ):
        return None, "NOT_SAME_STRICT_FACE_SIGN"
    enhanced = enhanced_record(candidate, low, high, ds)
    leaf = classify_records(
        row.chart_id,
        row.box,
        [
            enhanced if record.target_id == candidate.target_id
            else record
            for record in records
        ],
    )
    if leaf.classification == "no_future_root":
        return "EXCLUDED", "NO_INHERITED_FUTURE_ROOT"
    if leaf.classification != "unique_first":
        return None, f"ENHANCED_{leaf.classification}"
    if leaf.owner_target != FROZEN_OWNER:
        return "EXCLUDED", "UNIQUE_FIRST_OWNER_MISMATCH"
    if candidate.target_id == FROZEN_OWNER:
        chart = positive_chart(row, enhanced)
        if chart is None:
            return None, "ENHANCED_FROZEN_OUTGOING_UNRESOLVED"
        return (
            "LIVE" if chart == FROZEN_CHART else "EXCLUDED"
        ), f"ENHANCED_FROZEN_OUTGOING_{chart}"
    chart, _margins = outgoing_generic(row.chart_id, row.box)
    if chart is not None:
        return (
            "LIVE" if chart == FROZEN_CHART else "EXCLUDED"
        ), f"UNCHANGED_FROZEN_OUTGOING_{chart}"
    kind, _classes, _depths = h_partition(row)
    return kind, "FOLLOWUP_H_PARTITION"


@dataclass(frozen=True)
class QBox:
    t0: Q
    t1: Q
    r0: Q
    r1: Q
    s0: Q
    s1: Q
    depth: int


def q_geometry(chart_id: str, p_sign: int, box: QBox):
    t = base.arb_interval(box.t0, box.t1)
    r = base.arb_interval(box.r0, box.r1)
    s = base.arb_interval(box.s0, box.s1)
    rt = sqrt_one_minus_square(box.t0, box.t1)
    cell = chart_id.split(":")[1]
    nx, ny = t, rt if cell == "N" else -rt
    k = Q(1023, 262144)
    compact_q = base.arbq(k).sqrt() * r
    p_low = base.arbq(1 - k * box.r1 * box.r1).sqrt()
    p_high = base.arbq(1 - k * box.r0 * box.r0).sqrt()
    p_abs = hull(p_low.lower(), p_high.upper())
    p = p_abs if p_sign > 0 else -p_abs
    ux = compact_q * nx - p * ny
    uy = compact_q * ny + p * nx
    cx = base.arbq(Q(1, 2)) + s
    cy = base.arbq(Q(1, 2))
    radius = base.arbq(base.RADIUS["W"])
    return (
        cx + radius * nx,
        cy + radius * ny,
        ux,
        uy,
        s,
        compact_q,
    )


def q_classify(
    chart_id: str,
    p_sign: int,
    box: QBox,
    targets: tuple[str, ...],
) -> tuple[str, tuple[str, ...]]:
    geom = q_geometry(chart_id, p_sign, box)
    records = [
        root_from_geometry(geom, target_id)
        for target_id in targets
    ]
    strict = [
        record for record in records
        if record.classification == "strict_future_root"
    ]
    unresolved = [
        record for record in records
        if record.classification in {
            "unresolved_discriminant",
            "unresolved_root_sign",
        }
    ]
    if not strict and not unresolved:
        return "EXCLUDED_NO_INHERITED_FUTURE_ROOT", ()
    for candidate in strict:
        if all(
            other.target_id == candidate.target_id
            or other.classification in {
                "no_real_intersection",
                "intersection_behind",
            }
            or (
                (lower := earliest_lower(other)) is not None
                and bool(candidate.near < lower)
            )
            for other in records
        ):
            if candidate.target_id != FROZEN_OWNER:
                return (
                    "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH",
                    (candidate.target_id,),
                )
            qx, qy, ux, uy, s, _q = geom
            target = TARGETS[FROZEN_OWNER]
            cx, cy = base.target_center(target, s)
            radius = base.arbq(base.RADIUS["W"])
            nx = (qx + candidate.near * ux - cx) / radius
            ny = (qy + candidate.near * uy - cy) / radius
            tests = {
                "E": (nx - ny, nx + ny),
                "W": (-nx - ny, -nx + ny),
                "N": (ny - nx, ny + nx),
                "S": (-ny - nx, -ny + nx),
            }
            cells = [
                cell for cell, values in tests.items()
                if bool(values[0] > 0) and bool(values[1] > 0)
            ]
            if len(cells) == 1:
                return (
                    "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH"
                    if cells[0] == FROZEN_CHART
                    else "EXCLUDED_OUTGOING_CHART_MISMATCH"
                ), (candidate.target_id,)
            return "UNRESOLVED_OUTGOING_SEAM", (
                candidate.target_id,
            )
    active: set[str] = set()
    for candidate in strict + unresolved:
        lower = earliest_lower(candidate)
        if lower is None or not any(
            other.target_id != candidate.target_id
            and other.near is not None
            and bool(other.near < lower)
            for other in strict
        ):
            active.add(candidate.target_id)
    return "UNRESOLVED_MULTI", tuple(sorted(active))


def q_split(box: QBox) -> tuple[QBox, QBox]:
    widths = (
        (box.t1 - box.t0) / (T_UPPER - T_LOWER),
        box.r1 - box.r0,
        (box.s1 - box.s0) / (2 * base.EPS),
    )
    axis = max(range(3), key=lambda index: widths[index])
    depth = box.depth + 1
    if axis == 0:
        middle = (box.t0 + box.t1) / 2
        return (
            QBox(
                box.t0, middle, box.r0, box.r1,
                box.s0, box.s1, depth,
            ),
            QBox(
                middle, box.t1, box.r0, box.r1,
                box.s0, box.s1, depth,
            ),
        )
    if axis == 1:
        middle = (box.r0 + box.r1) / 2
        return (
            QBox(
                box.t0, box.t1, box.r0, middle,
                box.s0, box.s1, depth,
            ),
            QBox(
                box.t0, box.t1, middle, box.r1,
                box.s0, box.s1, depth,
            ),
        )
    middle = (box.s0 + box.s1) / 2
    return (
        QBox(
            box.t0, box.t1, box.r0, box.r1,
            box.s0, middle, depth,
        ),
        QBox(
            box.t0, box.t1, box.r0, box.r1,
            middle, box.s1, depth,
        ),
    )


def q_profile(row: Frontier) -> dict[str, Any]:
    p_sign = 1 if row.box.p1 == 1 else -1
    root = QBox(
        row.box.t0, row.box.t1, Q(0), Q(1),
        row.box.s0, row.box.s1, 0,
    )
    face = QBox(
        row.box.t0, row.box.t1, Q(0), Q(0),
        row.box.s0, row.box.s1, 0,
    )
    face_classification, _face_active = q_classify(
        row.chart_id, p_sign, face, row.active_targets
    )
    pending = [(root, row.active_targets)]
    terminal_counts: Counter[str] = Counter()
    terminal_depths: Counter[int] = Counter()
    terminal_volume: dict[str, Q] = defaultdict(Q)
    residual_counts: Counter[str] = Counter()
    residual_volume = Q(0)
    kinds: list[str] = []
    while pending:
        box, targets = pending.pop()
        classification, active = q_classify(
            row.chart_id, p_sign, box, targets
        )
        if not classification.startswith("UNRESOLVED"):
            terminal_counts[classification] += 1
            terminal_depths[box.depth] += 1
            terminal_volume[classification] += Q(1, 2 ** box.depth)
            kinds.append(
                "EXCLUDED" if classification.startswith("EXCLUDED")
                else "LIVE"
            )
        elif box.depth < 8:
            inherited = active or targets
            pending.extend(
                (child, inherited) for child in q_split(box)
            )
        else:
            residual_counts[classification] += 1
            residual_volume += Q(1, 2 ** box.depth)
    classified = sum(terminal_volume.values(), Q(0))
    require(classified + residual_volume == 1, "q coverage")
    if residual_counts:
        parent_kind = None
    elif set(kinds) == {"EXCLUDED"}:
        parent_kind = "EXCLUDED"
    elif set(kinds) == {"LIVE"}:
        parent_kind = "LIVE"
    else:
        parent_kind = "MIXED"
    return {
        "face_classification": face_classification,
        "terminal_counts": terminal_counts,
        "terminal_depths": terminal_depths,
        "terminal_volume": terminal_volume,
        "residual_counts": residual_counts,
        "residual_volume": residual_volume,
        "classified_volume": classified,
        "parent_kind": parent_kind,
    }


def coarse(disposition: str) -> str:
    if disposition.startswith("EXCLUDED"):
        return "EXCLUDED"
    if disposition.startswith("LIVE"):
        return "LIVE"
    raise RuntimeError(f"coarse disposition:{disposition}")


def box_row(box: Box) -> dict[str, Any]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
        "ambient_dimension": 3,
    }


def check_chain() -> dict[str, Any]:
    for name, expected in PINS.items():
        require(
            hashlib.sha256(read_regular(HERE / name)).hexdigest()
            == expected,
            f"upstream pin:{name}",
        )
    r172 = strict_load(
        HERE
        / "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning_certificate.json"
    )
    r172v = strict_load(
        HERE
        / "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning_verification.json"
    )
    require(
        r172["result_sha256"] == ROUND172_RESULT,
        "Round172 result identity",
    )
    require(
        r172v["result_sha256"] == ROUND172_VERIFICATION_RESULT
        and r172v["result"]["status"] == "PASS",
        "Round172 verification identity",
    )
    composition = r172["result"]["Round168_to_Round172_composition"]
    require(
        composition["combined_whole_record_excluded"] == 73172
        and composition["Round172_conservative_live"] == 3660,
        "Round172 ledger",
    )
    r175 = strict_load(
        HERE
        / "cm2_round175_dimension_safe_tangency_arrangement_certificate.json"
    )
    r175v = strict_load(
        HERE
        / "cm2_round175_dimension_safe_tangency_arrangement_verification.json"
    )
    require(
        r175["result_sha256"] == ROUND175_RESULT,
        "Round175 result identity",
    )
    require(
        r175v["result_sha256"] == ROUND175_VERIFICATION_RESULT
        and r175v["result"]["status"] == "PASS",
        "Round175 verification identity",
    )
    ledger = r175v["result"]["ledger_reconstruction"]
    require(
        ledger["combined_whole_record_excluded"] == 73178
        and ledger["Round175_conservative_live"] == 3654
        and ledger["Round175_new_whole_parent_excluded"] == 6,
        "Round175 ledger",
    )
    manifest_rows: dict[str, str] = {}
    for line in (
        HERE
        / "cm2_round175_dimension_safe_tangency_arrangement_manifest.sha256"
    ).read_text().splitlines():
        value, name = line.split("  ", 1)
        require(name not in manifest_rows, f"manifest duplicate:{name}")
        manifest_rows[name] = value
    expected_manifest_rows = {
        "cm2_round175_dimension_safe_tangency_arrangement.py":
            PINS["cm2_round175_dimension_safe_tangency_arrangement.py"],
        "cm2_round175_dimension_safe_tangency_arrangement_certificate.json":
            PINS[
                "cm2_round175_dimension_safe_tangency_arrangement_certificate.json"
            ],
        "cm2_round175_dimension_safe_tangency_arrangement_verifier.py":
            PINS[
                "cm2_round175_dimension_safe_tangency_arrangement_verifier.py"
            ],
        "cm2_round175_dimension_safe_tangency_arrangement_verification.json":
            PINS[
                "cm2_round175_dimension_safe_tangency_arrangement_verification.json"
            ],
        "cm2_round175_dimension_safe_tangency_arrangement_report.md":
            "bfdb125f9b77a4d2abeb1eaa8229dbd8bff163c5ed642cc317129c6bc9f48ae4",
    }
    require(manifest_rows == expected_manifest_rows, "Round175 manifest")
    require(
        all(
            hashlib.sha256(read_regular(HERE / name)).hexdigest() == value
            for name, value in manifest_rows.items()
        ),
        "Round175 manifest replay",
    )
    return {
        "file_sha256": dict(sorted(PINS.items())),
        "Round172_result_sha256": ROUND172_RESULT,
        "Round172_verification_result_sha256":
            ROUND172_VERIFICATION_RESULT,
        "Round175_result_sha256": ROUND175_RESULT,
        "Round175_verification_result_sha256":
            ROUND175_VERIFICATION_RESULT,
        "Round175_manifest_entries_replayed": True,
    }


def closure(row: Frontier) -> tuple[str | None, dict[str, Any]]:
    basic = {
        "leaf_key": row.key,
        "failure": row.failure,
        "ambient_parent_dimension": 3,
    }
    if row.failure == "OUTGOING_CHART_SEAM_OVERWRAP":
        kind, classes, depths = h_partition(row)
        terminal_count = sum(classes.values())
        volume = sum(
            Q(count, 2 ** depth)
            for depth, count in depths.items()
        )
        require(kind is not None and volume == 1, "H closure")
        return kind, {
            **basic,
            "method": "OUTGOING_H_CLOSED_RECTANGLE_TREE",
            "outcome": kind,
            "terminal_evidence": map_counter(classes),
            "terminal_count_by_extra_depth": map_counter(depths),
            "terminal_closed_3D_cell_count": terminal_count,
            "internal_split_2D_face_count": terminal_count - 1,
            "relative_3D_coverage": str(volume),
        }
    if row.failure in {
        "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR",
        "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR",
    }:
        records = records_for(
            row.chart_id, row.box, row.active_targets
        )
        unresolved = [
            record for record in records
            if record.classification == "unresolved_discriminant"
        ]
        closed, witness = close_tangency(row)
        return (
            "EXCLUDED" if closed else None,
            {
                **basic,
                "method": "TYPED_DELTA_THREE_STRATUM",
                "outcome": "EXCLUDED" if closed else "RESIDUAL",
                "target": (
                    unresolved[0].target_id
                    if len(unresolved) == 1
                    else "NONUNIQUE"
                ),
                "active_target_count": len(records),
                "terminal_evidence": witness,
                "strata": [
                    {"predicate": "Delta<0", "dimension": 3},
                    {"predicate": "Delta=0", "dimension": 2},
                    {"predicate": "Delta>0", "dimension": 3},
                ],
                "graph_boundary": {
                    "one_dimensional_edge_count": 4,
                    "zero_dimensional_corner_count": 4,
                    "p_faces_met": False,
                },
                "relative_3D_coverage": "1",
            },
        )
    if row.failure == "UNTYPED_DISCRIMINANT_COLLAR":
        records = records_for(
            row.chart_id, row.box, row.active_targets
        )
        unresolved = [
            record for record in records
            if record.classification == "unresolved_discriminant"
        ]
        if len(unresolved) != 1:
            return None, {
                **basic,
                "method": "MULTI_DELTA_RESIDUAL",
                "outcome": "RESIDUAL",
                "unresolved_target_count": len(unresolved),
            }
        candidate = unresolved[0]
        derivative_sign, lower, upper, full = graph_faces(
            row, candidate
        )
        same_sign = (
            derivative_sign != 0
            and sign(lower) != 0
            and sign(lower) == sign(upper)
        )
        if not same_sign:
            return None, {
                **basic,
                "method": (
                    "FULL_P_DELTA_GRAPH_RESIDUAL"
                    if full
                    else "CLIPPED_DELTA_RESIDUAL"
                ),
                "outcome": "RESIDUAL",
                "target": candidate.target_id,
            }
        kind, witness = close_same_sign(row)
        require(kind is not None, "same-sign closure")
        return kind, {
            **basic,
            "method": "SAME_SIGN_MONOTONE_DELTA_RECTANGLE",
            "outcome": kind,
            "target": candidate.target_id,
            "strict_derivative_sign":
                "POSITIVE" if derivative_sign > 0 else "NEGATIVE",
            "strict_common_p_face_sign":
                "POSITIVE" if sign(lower) > 0 else "NEGATIVE",
            "terminal_evidence": witness,
            "delta_zero_graph_present": False,
            "terminal_closed_3D_cell_count": 1,
            "relative_3D_coverage": "1",
        }
    require(
        row.failure == "SOURCE_GRAZING_ENDPOINT_COLLAR",
        f"failure dispatch:{row.failure}",
    )
    profile = q_profile(row)
    kind = profile["parent_kind"]
    terminal_count = sum(profile["terminal_counts"].values())
    return kind, {
        **basic,
        "method": "COMPACT_Q_CLOSED_CELL_TREE",
        "outcome": kind if kind is not None else "RESIDUAL",
        "coordinate": {
            "r": "[0,1]",
            "q": "sqrt(1023/262144)*r",
            "p": "sign*sqrt(1-(1023/262144)*r^2)",
        },
        "grazing_face": {
            "predicate": "r=0",
            "dimension": 2,
            "classification": profile["face_classification"],
        },
        "interior_predicate": "r>0",
        "interior_dimension": 3,
        "terminal_evidence": map_counter(profile["terminal_counts"]),
        "terminal_count_by_extra_depth":
            map_counter(profile["terminal_depths"]),
        "terminal_closed_3D_cell_count": terminal_count,
        "internal_split_2D_face_count":
            terminal_count + sum(profile["residual_counts"].values()) - 1,
        "terminal_volume_by_disposition":
            fraction_map(profile["terminal_volume"]),
        "classified_relative_3D_coverage":
            str(profile["classified_volume"]),
        "residual_relative_3D_coverage":
            str(profile["residual_volume"]),
        "relative_3D_coverage": str(
            profile["classified_volume"] + profile["residual_volume"]
        ),
    }


def physical_domain(chart_id: str, box: Box) -> dict[str, Any]:
    minimum_abs = (
        Q(0)
        if box.t0 <= 0 <= box.t1
        else min(abs(box.t0), abs(box.t1))
    )
    maximum_abs = max(abs(box.t0), abs(box.t1))
    if 2 * maximum_abs * maximum_abs < 1:
        classification = "STRICT_PHYSICAL_CHART_INTERIOR"
    elif 2 * minimum_abs * minimum_abs > 1:
        classification = "RATIONAL_GUARD_ONLY"
    else:
        classification = "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
    return {
        "classification": classification,
        "physical_interior_predicate": "2*t^2<1",
        "source_seam_predicate": "2*t^2=1",
        "source_seam_dimension": (
            2
            if classification
            == "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
            else None
        ),
        "source_seam_half_open_owner": (
            "E"
            if classification
            == "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
            else None
        ),
        "guard_predicate": "2*t^2>1",
        "guard_outside_exterior_credit": 0,
        "guard_only_parent": classification == "RATIONAL_GUARD_ONLY",
        "physical_positive_volume_present":
            classification != "RATIONAL_GUARD_ONLY",
    }


def origin_summary(
    key: str,
    meta: dict[str, Any],
    prior: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    evaluated_count: int,
) -> dict[str, Any]:
    prior_counts = Counter(row["disposition"] for row in prior)
    prior_depths = Counter(row["relative_depth"] for row in prior)
    prior_units = sum(row["coverage_numerator_64"] for row in prior)
    frontier_count = len(evidence)
    require(prior_units + frontier_count == 64, f"coverage:{key}")
    terminal_leaf_count = len(prior) + frontier_count
    require(
        evaluated_count == 2 * terminal_leaf_count - 1,
        f"binary tree:{key}",
    )
    methods = Counter(row["method"] for row in evidence)
    proof_classes: Counter[str] = Counter()
    dimension_counts: Counter[int] = Counter()
    needed: set[str] = set()
    for row in prior:
        dimension_counts[3] += 1
        proof_classes[f"PRIOR:{row['disposition']}"] += 1
    for row in evidence:
        method = row["method"]
        proof_classes[f"{method}:{row['outcome']}"] += 1
        if method == "OUTGOING_H_CLOSED_RECTANGLE_TREE":
            dimension_counts[3] += row["terminal_closed_3D_cell_count"]
            dimension_counts[2] += row["internal_split_2D_face_count"]
            needed.add(
                "closed split faces and their lower-dimensional intersections"
            )
        elif method == "TYPED_DELTA_THREE_STRATUM":
            dimension_counts[3] += 2
            dimension_counts[2] += 1
            dimension_counts[1] += 4
            dimension_counts[0] += 4
            needed.add("Delta=0 graph, graph edges, and graph corners")
        elif method == "SAME_SIGN_MONOTONE_DELTA_RECTANGLE":
            dimension_counts[3] += 1
        elif method == "COMPACT_Q_CLOSED_CELL_TREE":
            dimension_counts[3] += row["terminal_closed_3D_cell_count"]
            dimension_counts[2] += (
                row["internal_split_2D_face_count"] + 1
            )
            needed.add("r=0 grazing face and closed q-tree split faces")
        else:
            raise RuntimeError(f"credited method:{method}")
    source = physical_domain(meta["chart_id"], meta["box"])
    if source["source_seam_dimension"] == 2:
        dimension_counts[2] += 1
        needed.add(
            "physical source seam and all dimension-at-most-one "
            "intersections with analytic/split strata"
        )
    row = {
        "origin_key": key,
        "chart_id": meta["chart_id"],
        "atlas_path": meta["path"],
        "parent_box": box_row(meta["box"]),
        "source_chart_domain": source,
        "initial_active_target_count": len(meta["active_targets"]),
        "initial_active_targets_sha256":
            digest(list(meta["active_targets"])),
        "dyadic_replacement_tree": {
            "root_relative_depth": 0,
            "frontier_relative_depth": 6,
            "maximum_absolute_atlas_depth": 14,
            "evaluated_node_count": evaluated_count,
            "internal_binary_split_count": terminal_leaf_count - 1,
            "terminal_leaf_count": terminal_leaf_count,
            "prior_terminal_cell_count": len(prior),
            "prior_terminal_count_by_relative_depth":
                map_counter(prior_depths),
            "prior_terminal_count_by_disposition":
                map_counter(prior_counts),
            "depth14_frontier_cell_count": frontier_count,
            "coverage_numerator_64": prior_units + frontier_count,
            "coverage_denominator": 64,
            "coverage_identity": f"{prior_units}+{frontier_count}=64",
            "lower_child_owns_each_split_face": True,
            "closed_interval_enclosures_used_for_both_children": True,
        },
        "analytic_replacement": {
            "frontier_closure_count_by_method": map_counter(methods),
            "terminal_or_required_stratum_count_by_dimension": {
                str(dimension): count
                for dimension, count in sorted(dimension_counts.items())
            },
            "needed_lower_dimensional_strata": sorted(needed),
            "all_3D_descendants_excluded": True,
            "all_needed_2D_graphs_and_faces_excluded": True,
            "all_needed_1D_and_0D_intersections_excluded": True,
            "closed_interval_strict_proofs_inherit_to_owned_faces": True,
            "terminal_proof_class_counts": map_counter(proof_classes),
        },
        "terminal_evidence_row_count": len(prior) + len(evidence),
        "terminal_evidence_rows_sha256": digest(
            sorted(
                prior + evidence,
                key=lambda item: item["leaf_key"],
            )
        ),
        "whole_origin_disposition": "EXCLUDED",
        "whole_origin_integer_credit": 1,
    }
    row["row_sha256"] = digest(row)
    return row


def build_expected_result(producer_sha256: str) -> tuple[
    dict[str, Any],
    dict[str, Any],
]:
    upstream = check_chain()
    replay = replay_frontier()
    frontier: list[Frontier] = replay["frontier"]
    require(
        Counter(row.failure for row in frontier)
        == {
            "OUTGOING_CHART_SEAM_OVERWRAP": 7510,
            "SOURCE_GRAZING_ENDPOINT_COLLAR": 1632,
            "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR": 80,
            "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR": 1140,
            "UNTYPED_DISCRIMINANT_COLLAR": 46418,
        },
        "frontier type census",
    )
    require(
        replay["terminal_counts"]
        == {
            "EXCLUDED_OUTGOING_CHART_MISMATCH": 6520,
            "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH": 13472,
            "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH": 8528,
        },
        "prior terminal census",
    )
    origin_kinds: dict[str, set[str]] = replay["origin_kinds"]
    evidence_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    closed_by_origin: Counter[str] = Counter()
    category_keys: dict[str, list[str]] = defaultdict(list)
    residual_keys: list[str] = []
    for row in frontier:
        kind, evidence = closure(row)
        if kind is None:
            residual_keys.append(row.key)
            continue
        category_keys[kind].append(row.key)
        evidence_by_origin[row.origin_key].append(evidence)
        closed_by_origin[row.origin_key] += 1
        origin_kinds[row.origin_key].add(kind)
    for values in category_keys.values():
        values.sort()
    residual_keys.sort()
    require(
        {
            key: len(values)
            for key, values in sorted(category_keys.items())
        }
        == {"EXCLUDED": 6250, "LIVE": 3590, "MIXED": 2900}
        and len(residual_keys) == 44040,
        "closure census",
    )
    frontier_by_origin = Counter(row.origin_key for row in frontier)
    fully = [
        key for key in sorted(replay["origins"])
        if closed_by_origin[key] == frontier_by_origin[key]
    ]
    by_kind: dict[str, list[str]] = defaultdict(list)
    for key in fully:
        kinds = origin_kinds[key]
        category = (
            "WHOLE_ORIGIN_PARENT_EXCLUDED"
            if kinds == {"EXCLUDED"}
            else (
                "WHOLE_ORIGIN_PARENT_LIVE"
                if kinds == {"LIVE"}
                else "RESOLVED_MIXED_OR_ANALYTIC_PARTITION"
            )
        )
        by_kind[category].append(key)
    require(
        {
            key: len(values)
            for key, values in sorted(by_kind.items())
        }
        == {
            "RESOLVED_MIXED_OR_ANALYTIC_PARTITION": 36,
            "WHOLE_ORIGIN_PARENT_EXCLUDED": 182,
            "WHOLE_ORIGIN_PARENT_LIVE": 236,
        },
        "origin aggregation",
    )
    credited = by_kind["WHOLE_ORIGIN_PARENT_EXCLUDED"]
    require(
        digest(credited)
        == "bfb29d76ced106a3d69a3d4c1ebb2271c45a1567197a3e7da93e883cae6c91b3",
        "182 exact keys",
    )
    summaries = [
        origin_summary(
            key,
            replay["origins"][key],
            replay["prior"].get(key, []),
            evidence_by_origin[key],
            replay["evaluated_by_origin"][key],
        )
        for key in credited
    ]
    prior_only_origin_keys: list[str] = []
    analytic_origin_keys: list[str] = []
    analytic_origin_keys_by_method: dict[str, list[str]] = defaultdict(list)
    analytic_frontier_counts: Counter[str] = Counter()
    for row in summaries:
        methods = row["analytic_replacement"][
            "frontier_closure_count_by_method"
        ]
        if not methods:
            prior_only_origin_keys.append(row["origin_key"])
        else:
            require(len(methods) == 1, "one analytic method")
            method = next(iter(methods))
            analytic_origin_keys.append(row["origin_key"])
            analytic_origin_keys_by_method[method].append(row["origin_key"])
            analytic_frontier_counts.update(methods)
    require(
        len(prior_only_origin_keys) == 164
        and len(analytic_origin_keys) == 18
        and {
            key: len(values)
            for key, values in sorted(
                analytic_origin_keys_by_method.items()
            )
        }
        == {
            "OUTGOING_H_CLOSED_RECTANGLE_TREE": 8,
            "SAME_SIGN_MONOTONE_DELTA_RECTANGLE": 8,
            "TYPED_DELTA_THREE_STRATUM": 2,
        }
        and analytic_frontier_counts
        == {
            "OUTGOING_H_CLOSED_RECTANGLE_TREE": 60,
            "SAME_SIGN_MONOTONE_DELTA_RECTANGLE": 14,
            "TYPED_DELTA_THREE_STRATUM": 32,
        },
        "164/18 decomposition",
    )
    guard_counts = Counter(
        row["source_chart_domain"]["classification"]
        for row in summaries
    )
    crossing = [
        row["origin_key"] for row in summaries
        if row["source_chart_domain"]["classification"]
        == "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
    ]
    require(
        guard_counts
        == {
            "STRICT_PHYSICAL_CHART_INTERIOR": 180,
            "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE": 2,
        }
        and crossing
        == [
            "W:E:00.15.00000100",
            "W:E:07.00.11111011",
        ],
        "physical source guard census",
    )
    r172 = strict_load(
        HERE
        / "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning_certificate.json"
    )
    round172_keys = sorted(
        r172["result"]["whole_parent_frozen_owner_absence_credit"][
            "exact_excluded_parent_keys"
        ]
    )
    r175 = strict_load(
        HERE
        / "cm2_round175_dimension_safe_tangency_arrangement_certificate.json"
    )
    round175_keys = sorted(
        r175["result"]["new_whole_parent_exclusion_credit"][
            "exact_parent_keys"
        ]
    )
    require(
        len(round172_keys) == 10
        and len(round175_keys) == 6
        and not (set(round172_keys) & set(round175_keys)),
        "cumulative tangency keys",
    )
    cumulative_tangency_keys = sorted(
        set(round172_keys) | set(round175_keys)
    )
    require(
        not (set(cumulative_tangency_keys) & set(credited)),
        "tangency/multi exact-key disjointness",
    )
    all_frontier = sorted(row.key for row in frontier)
    all_origins = sorted(replay["origins"])
    result = {
        "status": (
            "CERTIFIED_182_WHOLE_MULTI_CANDIDATE_PARENT_EXCLUSIONS__"
            "DIMENSION_SAFE__D02_STILL_BLOCKED"
        ),
        "scope": {
            "source_obstacle": "W",
            "frozen_owner": "W[1,0]",
            "frozen_outgoing_chart": "W",
            "original_parent_dimension": 3,
            "integer_credit_unit": "one completely replaced depth8 parent",
            "child_or_volume_count_used_as_integer_credit": False,
            "guard_rejection_used_as_exterior_credit": False,
            "Round170_candidate_digest_used_as_truth": False,
            "not_D02_closure": True,
        },
        "upstream_verified_chain": upstream,
        "independent_reconstruction_target": {
            **replay["workload"],
            "owner_active_depth8_parent_count": 2616,
            "depth14_frontier_cell_count": 56780,
            "closed_depth14_cell_count_by_disposition": {
                key: len(values)
                for key, values in sorted(category_keys.items())
            },
            "residual_depth14_cell_count": len(residual_keys),
            "fully_replaced_origin_count": len(fully),
            "fully_replaced_origin_count_by_disposition": {
                key: len(values)
                for key, values in sorted(by_kind.items())
            },
        },
        "new_whole_parent_exclusion_credit": {
            "count": 182,
            "exact_origin_keys": credited,
            "exact_origin_keys_sha256": digest(credited),
            "origin_summaries": summaries,
            "origin_summaries_sha256": digest(summaries),
            "every_summary_row_self_digest_valid": all(
                row["row_sha256"]
                == digest({
                    key: value for key, value in row.items()
                    if key != "row_sha256"
                })
                for row in summaries
            ),
            "prior_strict_terminal_only_origin_count":
                len(prior_only_origin_keys),
            "prior_strict_terminal_only_origin_keys_sha256":
                digest(prior_only_origin_keys),
            "analytic_closure_origin_count": len(analytic_origin_keys),
            "analytic_closure_origin_keys": analytic_origin_keys,
            "analytic_closure_origin_keys_sha256":
                digest(analytic_origin_keys),
            "analytic_origin_count_by_method": {
                key: len(values)
                for key, values in sorted(
                    analytic_origin_keys_by_method.items()
                )
            },
            "analytic_origin_keys_by_method": {
                key: values
                for key, values in sorted(
                    analytic_origin_keys_by_method.items()
                )
            },
            "analytic_frontier_closure_count_by_method":
                map_counter(analytic_frontier_counts),
        },
        "physical_source_chart_audit": {
            "count_by_classification": map_counter(guard_counts),
            "guard_only_origin_count": 0,
            "crossing_origin_count": 2,
            "exact_crossing_origin_keys": crossing,
            "exact_crossing_origin_keys_sha256": digest(crossing),
            "source_boundary_dimension": 2,
            "source_boundary_analytic_graph_intersection_dimension_at_most":
                1,
            "source_boundary_multiple_graph_intersection_dimension_at_most":
                0,
            "E_owns_source_diagonal_half_open_seam": True,
            "rational_guard_band_exterior_credit": 0,
        },
        "partition_semantics": {
            "dyadic_closed_overlap_evaluation": True,
            "dyadic_disjoint_ledger_owner":
                "lower child owns each split equality face",
            "multiple_split_face_owner":
                "recursive lexicographic lower-child ownership",
            "strict_closed_box_exclusion_inherits_to_all_owned_faces": True,
            "Delta_partition": [
                {"predicate": "Delta<0", "dimension": 3},
                {"predicate": "Delta=0", "dimension": 2},
                {"predicate": "Delta>0", "dimension": 3},
            ],
            "compact_q_partition": [
                {"predicate": "r>0", "dimension": 3},
                {"predicate": "r=0", "dimension": 2},
            ],
            "graph_edge_dimension": 1,
            "graph_corner_dimension": 0,
            "all_dimensions_must_be_excluded_for_parent_credit": True,
        },
        "disjoint_composition": {
            "Round172_tangency_credit_key_count": len(round172_keys),
            "Round172_tangency_credit_keys_sha256": digest(round172_keys),
            "Round175_new_tangency_credit_key_count": len(round175_keys),
            "Round175_new_tangency_credit_keys_sha256":
                digest(round175_keys),
            "Round175_cumulative_tangency_credit_key_count":
                len(cumulative_tangency_keys),
            "Round175_cumulative_tangency_credit_keys_sha256":
                digest(cumulative_tangency_keys),
            "Round176_multi_credit_key_count": len(credited),
            "Round176_multi_credit_keys_sha256": digest(credited),
            "exact_key_intersection": [],
            "exact_key_intersection_sha256": digest([]),
            "classification_namespace_reason":
                "Round172/Round175 keys are Gate3 tangency_graph parents; "
                "Round176 keys are owner-active multi_candidate parents",
            "sets_proved_disjoint": True,
        },
        "ledger_composition": {
            "base_round": 175,
            "base_whole_record_excluded": 73178,
            "base_conservative_live": 3654,
            "Round176_new_whole_parent_excluded": 182,
            "combined_whole_record_excluded": 73360,
            "combined_conservative_live": 3472,
            "refined_source_W_record_count": 76832,
            "conservation_identity": "73360+3472=76832",
            "analytic_internal_strata_added_to_integer_record_count": False,
            "guard_outside_added_to_integer_record_count": False,
        },
        "layer_exact_key_digests": {
            "owner_active_depth8_origins_sha256": digest(all_origins),
            "all_depth14_frontier_keys_sha256": digest(all_frontier),
            "closed_EXCLUDED_depth14_keys_sha256":
                digest(category_keys["EXCLUDED"]),
            "closed_LIVE_depth14_keys_sha256":
                digest(category_keys["LIVE"]),
            "closed_MIXED_depth14_keys_sha256":
                digest(category_keys["MIXED"]),
            "residual_depth14_keys_sha256": digest(residual_keys),
            "whole_excluded_origin_keys_sha256": digest(credited),
            "whole_live_origin_keys_sha256":
                digest(by_kind["WHOLE_ORIGIN_PARENT_LIVE"]),
            "whole_mixed_origin_keys_sha256":
                digest(by_kind["RESOLVED_MIXED_OR_ANALYTIC_PARTITION"]),
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "remaining_multi_candidate_original_parents": 2434,
            "remaining_live_after_composition": 3472,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "close the remaining multi-Delta, full/clipped Delta, "
            "tangency/seam double-graph, and compact-q arrangements"
        ),
        "provenance": {
            "producer": PRODUCER.name,
            "producer_sha256": producer_sha256,
            "python_flint_version": "0.9.0",
            "arb_precision_bits": 192,
            "producer_imports_pinned_Round166_and_Round170_geometry": True,
            "verifier_must_not_import_or_execute_Round165_166_170": True,
            "older_round_files_modified": False,
        },
    }
    audit = {
        "owner_active_keys": all_origins,
        "frontier_keys": all_frontier,
        "category_keys": dict(category_keys),
        "residual_keys": residual_keys,
        "by_kind": dict(by_kind),
        "analytic_origin_keys": analytic_origin_keys,
        "prior_only_origin_keys": prior_only_origin_keys,
        "summaries": summaries,
    }
    return result, audit


def validate_document(
    document: dict[str, Any],
    expected_result: dict[str, Any],
    *,
    enforce_frozen_result_digest: bool = True,
) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "document exact keys",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(
        document["result_sha256"] == digest(document["result"]),
        "certificate result digest",
    )
    if enforce_frozen_result_digest:
        require(
            document["result_sha256"]
            == EXPECTED_CERTIFICATE_RESULT_SHA256,
            "certificate pinned result digest",
        )
    require(
        canonical(document["result"]) == canonical(expected_result),
        "full expected canonical equality",
    )


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def update_row_digest(row: dict[str, Any]) -> None:
    row["row_sha256"] = digest({
        key: value for key, value in row.items()
        if key != "row_sha256"
    })


def semantic_attacks(
    document: dict[str, Any],
    expected_result: dict[str, Any],
    analytic_keys: list[str],
) -> dict[str, Any]:
    credit = document["result"]["new_whole_parent_exclusion_credit"]
    summaries = credit["origin_summaries"]
    by_key = {
        row["origin_key"]: index for index, row in enumerate(summaries)
    }
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("schema", lambda d: d.__setitem__("schema", "forged")),
        (
            "status",
            lambda d: d["result"].__setitem__("status", "PROMOTED"),
        ),
        (
            "owner-active census",
            lambda d: d["result"]["independent_reconstruction_target"].
                __setitem__("owner_active_depth8_parent_count", 2615),
        ),
        (
            "frontier census",
            lambda d: d["result"]["independent_reconstruction_target"].
                __setitem__("depth14_frontier_cell_count", 56779),
        ),
        (
            "excluded cell census",
            lambda d: d["result"]["independent_reconstruction_target"][
                "closed_depth14_cell_count_by_disposition"
            ].__setitem__("EXCLUDED", 6251),
        ),
        (
            "residual cell census",
            lambda d: d["result"]["independent_reconstruction_target"].
                __setitem__("residual_depth14_cell_count", 44039),
        ),
        (
            "whole parent credit",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"].
                __setitem__("count", 183),
        ),
        (
            "182 exact key",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"][
                "exact_origin_keys"
            ].__setitem__(0, "W:E:forged"),
        ),
        (
            "182 exact-key digest",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"].
                __setitem__("exact_origin_keys_sha256", "0" * 64),
        ),
        (
            "prior-only count",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"].
                __setitem__("prior_strict_terminal_only_origin_count", 163),
        ),
        (
            "analytic count",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"].
                __setitem__("analytic_closure_origin_count", 17),
        ),
        (
            "analytic method count",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"][
                "analytic_origin_count_by_method"
            ].__setitem__("TYPED_DELTA_THREE_STRATUM", 3),
        ),
        (
            "physical guard equation",
            lambda d: d["result"]["physical_source_chart_audit"].
                __setitem__("rational_guard_band_exterior_credit", 1),
        ),
        (
            "physical seam owner",
            lambda d: d["result"]["physical_source_chart_audit"].
                __setitem__("E_owns_source_diagonal_half_open_seam", False),
        ),
        (
            "physical crossing key",
            lambda d: d["result"]["physical_source_chart_audit"][
                "exact_crossing_origin_keys"
            ].__setitem__(0, "W:E:forged"),
        ),
        (
            "dyadic owner",
            lambda d: d["result"]["partition_semantics"].
                __setitem__(
                    "dyadic_disjoint_ledger_owner",
                    "upper child owns",
                ),
        ),
        (
            "closed overlap",
            lambda d: d["result"]["partition_semantics"].
                __setitem__("dyadic_closed_overlap_evaluation", False),
        ),
        (
            "Delta graph dimension",
            lambda d: d["result"]["partition_semantics"][
                "Delta_partition"
            ][1].__setitem__("dimension", 3),
        ),
        (
            "graph edge dimension",
            lambda d: d["result"]["partition_semantics"].
                __setitem__("graph_edge_dimension", 2),
        ),
        (
            "graph corner dimension",
            lambda d: d["result"]["partition_semantics"].
                __setitem__("graph_corner_dimension", 1),
        ),
        (
            "all dimensions guard",
            lambda d: d["result"]["partition_semantics"].
                __setitem__(
                    "all_dimensions_must_be_excluded_for_parent_credit",
                    False,
                ),
        ),
        (
            "tangency multi disjointness",
            lambda d: d["result"]["disjoint_composition"].
                __setitem__("sets_proved_disjoint", False),
        ),
        (
            "fake key intersection",
            lambda d: d["result"]["disjoint_composition"].
                __setitem__("exact_key_intersection", ["forged"]),
        ),
        (
            "base round",
            lambda d: d["result"]["ledger_composition"].
                __setitem__("base_round", 172),
        ),
        (
            "base excluded",
            lambda d: d["result"]["ledger_composition"].
                __setitem__("base_whole_record_excluded", 73172),
        ),
        (
            "combined excluded",
            lambda d: d["result"]["ledger_composition"].
                __setitem__("combined_whole_record_excluded", 73361),
        ),
        (
            "combined live",
            lambda d: d["result"]["ledger_composition"].
                __setitem__("combined_conservative_live", 3471),
        ),
        (
            "conservation",
            lambda d: d["result"]["ledger_composition"].
                __setitem__("conservation_identity", "forged"),
        ),
        (
            "analytic strata integer credit",
            lambda d: d["result"]["ledger_composition"].
                __setitem__(
                    "analytic_internal_strata_added_to_integer_record_count",
                    True,
                ),
        ),
        (
            "guard integer credit",
            lambda d: d["result"]["ledger_composition"].
                __setitem__(
                    "guard_outside_added_to_integer_record_count",
                    True,
                ),
        ),
        (
            "owner layer digest",
            lambda d: d["result"]["layer_exact_key_digests"].
                __setitem__("owner_active_depth8_origins_sha256", "0" * 64),
        ),
        (
            "frontier layer digest",
            lambda d: d["result"]["layer_exact_key_digests"].
                __setitem__("all_depth14_frontier_keys_sha256", "0" * 64),
        ),
        (
            "excluded layer digest",
            lambda d: d["result"]["layer_exact_key_digests"].
                __setitem__(
                    "closed_EXCLUDED_depth14_keys_sha256",
                    "0" * 64,
                ),
        ),
        (
            "residual layer digest",
            lambda d: d["result"]["layer_exact_key_digests"].
                __setitem__("residual_depth14_keys_sha256", "0" * 64),
        ),
        (
            "D02 promotion",
            lambda d: d["result"]["strict_nonpromotion"].
                __setitem__("D02", "READY"),
        ),
        (
            "D03 authorization",
            lambda d: d["result"]["strict_nonpromotion"].
                __setitem__("D03_negative_oracle", "AUTHORIZED"),
        ),
        (
            "Gate5 promotion",
            lambda d: d["result"]["strict_nonpromotion"].
                __setitem__("global_Gate5_fields", "18/18"),
        ),
        (
            "CM2 promotion",
            lambda d: d["result"]["strict_nonpromotion"].
                __setitem__("CM2", "GO"),
        ),
        (
            "producer import contract",
            lambda d: d["result"]["provenance"].
                __setitem__(
                    "verifier_must_not_import_or_execute_Round165_166_170",
                    False,
                ),
        ),
        (
            "producer pin",
            lambda d: d["result"]["provenance"].
                __setitem__("producer_sha256", "0" * 64),
        ),
        (
            "recursive extra key",
            lambda d: d["result"]["scope"].__setitem__("forged", True),
        ),
    ]
    for key in analytic_keys:
        index = by_key[key]

        def method_mutation(
            d: dict[str, Any],
            index: int = index,
        ) -> None:
            row = d["result"]["new_whole_parent_exclusion_credit"][
                "origin_summaries"
            ][index]
            methods = row["analytic_replacement"][
                "frontier_closure_count_by_method"
            ]
            method = next(iter(methods))
            methods[method] += 1
            update_row_digest(row)
            credit = d["result"]["new_whole_parent_exclusion_credit"]
            credit["origin_summaries_sha256"] = digest(
                credit["origin_summaries"]
            )
            credit["analytic_frontier_closure_count_by_method"][
                method
            ] += 1

        def strata_mutation(
            d: dict[str, Any],
            index: int = index,
        ) -> None:
            row = d["result"]["new_whole_parent_exclusion_credit"][
                "origin_summaries"
            ][index]
            dimensions = row["analytic_replacement"][
                "terminal_or_required_stratum_count_by_dimension"
            ]
            dimensions["2"] = dimensions.get("2", 0) + 1
            update_row_digest(row)
            credit = d["result"]["new_whole_parent_exclusion_credit"]
            credit["origin_summaries_sha256"] = digest(
                credit["origin_summaries"]
            )

        def coverage_mutation(
            d: dict[str, Any],
            index: int = index,
        ) -> None:
            row = d["result"]["new_whole_parent_exclusion_credit"][
                "origin_summaries"
            ][index]
            tree = row["dyadic_replacement_tree"]
            tree["coverage_numerator_64"] = 63
            tree["coverage_identity"] = "forged=63"
            update_row_digest(row)
            credit = d["result"]["new_whole_parent_exclusion_credit"]
            credit["origin_summaries_sha256"] = digest(
                credit["origin_summaries"]
            )

        attacks.extend([
            (f"{key}:analytic method", method_mutation),
            (f"{key}:analytic strata", strata_mutation),
            (f"{key}:analytic coverage", coverage_mutation),
        ])
    rejected: list[str] = []
    for name, mutate in attacks:
        candidate = copy.deepcopy(document)
        mutate(candidate)
        resign(candidate)
        try:
            validate_document(
                candidate,
                expected_result,
                enforce_frozen_result_digest=False,
            )
        except Exception:
            rejected.append(name)
        else:
            raise RuntimeError(f"semantic attack accepted:{name}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == len(attacks),
        "re_signed_result_digest_each_time": True,
        "analytic_origin_attack_count": 3 * len(analytic_keys),
        "each_of_18_analytic_origins_method_strata_coverage_attacked": True,
        "rejected_attack_names": rejected,
    }


def strict_json_attacks() -> dict[str, Any]:
    empty_digest = digest({})
    attacks = {
        "duplicate envelope key":
            b'{"schema":"x","schema":"y","result":{},'
            b'"result_sha256":"0"}',
        "duplicate nested key":
            b'{"schema":"x","result":{"a":1,"a":1},'
            b'"result_sha256":"0"}',
        "floating number":
            b'{"schema":"x","result":{"a":1.0},"result_sha256":"0"}',
        "exponent number":
            b'{"schema":"x","result":{"a":1e2},"result_sha256":"0"}',
        "NaN constant":
            b'{"schema":"x","result":{"a":NaN},"result_sha256":"0"}',
        "UTF8 BOM": b'\xef\xbb\xbf{"schema":"x"}',
        "raw NUL": b'{"schema":"x","result":{}\x00}',
        "invalid UTF8": b"\xff",
        "noncanonical whitespace":
            (
                b'{ "schema":"x","result":{},"result_sha256":"'
                + empty_digest.encode()
                + b'"}\n'
            ),
    }
    rejected: list[str] = []
    for name, raw in attacks.items():
        try:
            value = parse_envelope(
                raw,
                label=f"JSON attack:{name}",
                canonical_pretty=True,
            )
            require(raw == pretty_bytes(value), f"canonical:{name}")
        except Exception:
            rejected.append(name)
        else:
            raise RuntimeError(f"JSON attack accepted:{name}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == len(attacks),
        "rejected_attack_names": rejected,
    }


def safe_atomic_write(
    path: Path,
    raw: bytes,
    protected: set[Path],
) -> None:
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.parent.resolve() == HERE, "output directory")
    if path.exists() or path.is_symlink():
        status = path.lstat()
        require(stat.S_ISREG(status.st_mode), "output regular")
        require(not path.is_symlink(), "output symlink")
        require(status.st_nlink == 1, "output hardlink")
    require(
        path.resolve(strict=False) not in protected,
        "protected output",
    )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def expect_rejection(
    name: str,
    operation: Callable[[], Any],
) -> str:
    try:
        operation()
    except Exception:
        return name
    raise RuntimeError(f"path attack accepted:{name}")


def path_safety_attacks(certificate_path: Path) -> dict[str, Any]:
    rejected: list[str] = []
    scratch = Path(tempfile.mkdtemp(prefix=".round176-path.", dir=HERE))
    symlink_output = HERE / f".round176-symlink-output.{os.getpid()}"
    hard_base = HERE / f".round176-hard-base.{os.getpid()}"
    hard_link = HERE / f".round176-hard-link.{os.getpid()}"
    outside = HERE.parent / f".round176-escape.{os.getpid()}"
    try:
        source = scratch / "source"
        source.write_bytes(b"{}\n")
        symlink_input = scratch / "symlink-input"
        symlink_input.symlink_to(source)
        rejected.append(expect_rejection(
            "symlink input",
            lambda: read_regular(symlink_input),
        ))
        hard_input = scratch / "hard-input"
        os.link(source, hard_input)
        rejected.append(expect_rejection(
            "hardlink input",
            lambda: read_regular(hard_input),
        ))
        oversized = scratch / "oversized"
        with oversized.open("wb") as handle:
            handle.truncate(MAX_INPUT_BYTES + 1)
        rejected.append(expect_rejection(
            "oversized sparse input",
            lambda: read_regular(oversized),
        ))
        protected = {
            certificate_path.resolve(),
            PRODUCER.resolve(),
            Path(__file__).resolve(),
        }
        symlink_output.symlink_to(source)
        rejected.append(expect_rejection(
            "symlink output",
            lambda: safe_atomic_write(symlink_output, b"x", protected),
        ))
        hard_base.write_bytes(b"x")
        os.link(hard_base, hard_link)
        rejected.append(expect_rejection(
            "hardlink output",
            lambda: safe_atomic_write(hard_link, b"x", protected),
        ))
        rejected.append(expect_rejection(
            "protected certificate output",
            lambda: safe_atomic_write(certificate_path, b"x", protected),
        ))
        rejected.append(expect_rejection(
            "parent directory escape",
            lambda: safe_atomic_write(outside, b"x", protected),
        ))
    finally:
        for path in (symlink_output, hard_link, hard_base, outside):
            if path.exists() or path.is_symlink():
                path.unlink()
        shutil.rmtree(scratch)
    return {
        "attack_count": 7,
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == 7,
        "rejected_attack_names": rejected,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    ctx.prec = 192
    certificate_path = Path(
        os.path.abspath(os.fspath(arguments.certificate))
    )
    require(
        certificate_path.parent.resolve() == HERE,
        "certificate directory",
    )
    producer_raw = read_regular(PRODUCER, PRODUCER_SHA256)
    certificate_raw = read_regular(
        certificate_path,
        EXPECTED_CERTIFICATE_SHA256,
    )
    document = parse_envelope(
        certificate_raw,
        label=certificate_path.name,
        expected_schema=CERTIFICATE_SCHEMA,
        canonical_pretty=True,
    )
    expected_result, audit = build_expected_result(
        hashlib.sha256(producer_raw).hexdigest()
    )
    validate_document(document, expected_result)
    semantic = semantic_attacks(
        document,
        expected_result,
        audit["analytic_origin_keys"],
    )
    strict = strict_json_attacks()
    paths = path_safety_attacks(certificate_path)
    result = {
        "status": "PASS",
        "certificate_sha256": hashlib.sha256(certificate_raw).hexdigest(),
        "certificate_result_sha256": document["result_sha256"],
        "producer_sha256": hashlib.sha256(producer_raw).hexdigest(),
        "verifier_sha256":
            hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "independence_contract": {
            "Round176_producer_imported_or_executed": False,
            "Round165_Round166_Round170_imported_or_executed": False,
            "only_pinned_Gate3_base_geometry_imported": True,
            "owner_active_2616_selection_independently_reconstructed": True,
            "depth8_to_depth14_tree_independently_reconstructed": True,
            "all_56780_frontier_cells_reclassified": True,
            "Delta_H_and_compact_q_closures_independently_reconstructed":
                True,
            "all_3D_cells_and_required_2D_1D_0D_strata_accounted": True,
            "closed_split_lower_child_ownership_enforced": True,
            "physical_2t_squared_equals_1_guard_enforced": True,
            "full_expected_result_independently_reconstructed": True,
            "full_expected_canonical_equality": True,
        },
        "recomputed_census": {
            "owner_active_depth8_parents": 2616,
            "depth14_frontier_cells": 56780,
            "frontier_closed_EXCLUDED": 6250,
            "frontier_closed_LIVE": 3590,
            "frontier_closed_MIXED": 2900,
            "frontier_residual": 44040,
            "fully_replaced_origins": 454,
            "whole_origin_excluded": 182,
            "whole_origin_live": 236,
            "whole_origin_mixed": 36,
            "exact_182_key_digest":
                "bfb29d76ced106a3d69a3d4c1ebb2271c45a1567197a3e7da93e883cae6c91b3",
            "difference_from_Round170_candidate_set": 0,
        },
        "credited_origin_risk_split": {
            "prior_strict_terminal_only": 164,
            "requires_new_analytic_closure": 18,
            "analytic_origin_count_by_method": {
                "OUTGOING_H_CLOSED_RECTANGLE_TREE": 8,
                "SAME_SIGN_MONOTONE_DELTA_RECTANGLE": 8,
                "TYPED_DELTA_THREE_STRATUM": 2,
            },
            "all_18_individually_attacked_for_method_strata_coverage":
                True,
        },
        "physical_source_guard_audit": {
            "strict_physical_interior_origins": 180,
            "source_seam_and_guard_composite_origins": 2,
            "guard_only_origins": 0,
            "guard_outside_exterior_credit": 0,
            "equation": "2*t^2=1",
        },
        "ledger_reconstruction": {
            "Round175_whole_record_excluded": 73178,
            "Round175_conservative_live": 3654,
            "Round176_new_whole_parent_excluded": 182,
            "combined_whole_record_excluded": 73360,
            "combined_conservative_live": 3472,
            "refined_source_W_record_count": 76832,
            "conservation_identity": "73360+3472=76832",
            "Round175_tangency_and_Round176_multi_sets_disjoint": True,
        },
        "semantic_mutation_attack_suite": semantic,
        "strict_json_attack_suite": strict,
        "path_safety_attack_suite": paths,
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    protected = {
        PRODUCER.resolve(),
        certificate_path.resolve(),
        Path(__file__).resolve(),
        *((HERE / name).resolve() for name in PINS),
    }
    safe_atomic_write(
        arguments.output,
        pretty_bytes(envelope),
        protected,
    )
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
