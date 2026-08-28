#!/usr/bin/env python3
"""Exact zero-credit multi-graph order and tangency-stratum oracle.

This successor consumes the exact 42,926-row C72 child-witness scope.  It
does not refine the dyadic boxes.  Instead it reconstructs the two active
collision-one roots, isolates the single regular discriminant graph by its
strict gradient and corner signs, proves the competing roots never tie, and
seals the two open slabs plus the graph stratum separately.  Physical future
tangency graphs are retained as cemetery terminals rather than being erased
as bulk exclusions.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
from dataclasses import dataclass
import gzip
import hashlib
import json
from fractions import Fraction as Q
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterator

from flint import arb, ctx


ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
sys.path.insert(0, str(DELIVERABLES))

import cm2_round306c41_d02_lower_strata_depth3_closure_v1 as c41  # noqa: E402


C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C72 = ROOT / ".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"
C65 = DELIVERABLES / "cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz"
C58 = DELIVERABLES / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"
SELECTOR = "inherited interval ordering or boundary type not isolated"
SELF = Path(__file__).resolve()
SCHEMA = "cm2.round306c74.exact-multi-graph-order-oracle.v1"
PREFIX = "cm2_round306c74_exact_multi_graph_order_oracle_v1"
LEDGER_NAME = PREFIX + ".jsonl.gz"
ENDPOINT_LEDGER_NAME = PREFIX + "_endpoint_incidence.jsonl.gz"
RESULT_NAME = PREFIX + "_result.json"
REPORT_NAME = PREFIX + "_report.md"
MANIFEST_NAME = PREFIX + "_manifest.sha256"
OUTER_NAME = PREFIX + "_outer_receipt.json"
PRECISION_BITS = 384

C72_DIRS = (
    ROOT / ".cm2-runtime/c72-build-a.ZWGF2f",
    ROOT / ".cm2-runtime/c72-build-b.6NX5S7",
)
C72_LEDGER_NAME = "cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"
C72_RESULT_NAME = "cm2_round306c72_structural_child_obligation_atlas_v1_result.json"
C72_VERIFY_NAME = "cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json"
C72O_DIRS = (ROOT / ".cm2-runtime/c72o-build-a2.v1", ROOT / ".cm2-runtime/c72o-build-b.v1")
C72O_LEDGER_NAME = "cm2_round306c72o_collision1_outgoing_state_oracle_v1.jsonl.gz"
C72O_RESULT_NAME = "cm2_round306c72o_collision1_outgoing_state_oracle_v1_result.json"
C72O_VERIFY = ROOT / ".cm2-runtime/c72o-independent-verification-v2.json"
C73_DIRS = (ROOT / ".cm2-runtime/c73v2-build-a.QOYACE", ROOT / ".cm2-runtime/c73v2-build-b.8OTdPR")
C73_LEDGER_NAME = "cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2.jsonl.gz"
C73_RESULT_NAME = "cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2_result.json"
C73_VERIFIES = (
    ROOT / ".cm2-runtime/c73v2-audit-a.W2AYpD/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_independent_verification_v2.json",
    ROOT / ".cm2-runtime/c73v2-audit-b.rzmvxS/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_independent_verification_v2.json",
)

FILE_PINS = {
    "C72_LEDGER": "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370",
    "C72_RESULT": "55318b7c3ee778cb8a0e41d612c9c2caa44790e6fff816a6104116268258f01e",
    "C72_VERIFY": "63105e380d37d49bd655e094d41e15d3ed0d182380a44a4a16709ba3308edaf0",
    "C65_RESULT": "1ca46fb81cc104b727b31d3bb0adbb439ab8dae9123b8cbe05d3c60de0e75457",
    "C65_LEAVES": "4ff1c36a0a6331510da3afb988738f128a3cada04ddd297ac58584579115437d",
    "C65_VERIFY": "7d4e97bd641da7c5ccc64e8c2ad3d59f21ba3ebd73eb0e4d55c88ad617ee23b4",
    "C65_SELFTEST": "f0609dc4835346e078b5299007b1b31210d28cbf772ac41bb0f390f7047ad274",
    "C65_REPLAY": "c7d99ba4fea05fbd7a3b478f025323c77e5335951e4ff08743ad37ba47fa8e85",
    "C65_MANIFEST": "96b0f082688f16f821104402bc9aba1b7778df36f084a300d978dac95faf43c5",
    "C65_OUTER": "20a52a4c16c84ffd524833c0ee872edfeb6fdec538a1368f619244199814fb1d",
    "C69_RESULT": "607fc73ebe3333ca172eb15c0831b8c3d98192c86e20eec7a59a69c4ae4737d4",
    "C69_BLOCKERS": "69b3ec294f95cb5ce377e553ae875daab10a5bdb33e860363f6bae122022e606",
    "C69_VERIFY": "b0490ed50de8d615039d864db1071792df0809b928a663fcd4a89981eaf326b6",
    "C69_MANIFEST": "c231941ca4f5f76a95faa81e8390e3f11b5d1af84b645605c52245e6ff214749",
    "C69_OUTER": "2baac1cf22ca8be0163f9027d0365e948107b535df917a25334626110bf2916c",
    "C58_RESULT": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "C58_LEAVES": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "C40_RESULT": "f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "C72O_LEDGER": "e3125863adcf3ef6489dce741337622b1d70b2ce7655d8d06237c1612ff19355",
    "C72O_RESULT": "fd9ca6489f5fedef85fb55de6906a62ecadc417c72d7eb938a6268e7f402302a",
    "C72O_VERIFY": "2d34c25b5fd9f2b3a1e8b30d184b40d8a93ffce8c192d193b75715e0d7a68ccb",
    "C73_LEDGER": "ed0a3d26f4984e6eced899a01f58aa8329bb1db72b7d0bfb9fe17ee3a4eef6fc",
    "C73_RESULT": "5de9d37c69ed4d13d972eff8845ed55ad695ab040d6c1beda01626c0c065c615",
    "C73_VERIFY": "784505135d105fcdf05cc2d6e37779ea896f7d1bbe06e75dd1019b67ae951fe1",
}

EXPECTED_PAIR_CENSUS = {31: 5898, 200: 2957, 270: 160, 321: 11153,
                        410: 4839, 631: 158, 711: 7781, 787: 9980}
EXPECTED_ORDER_CENSUS = {
    "FROZEN_W_STRICT_BEFORE_OTHER_ON_REAL_STRATUM": 16796,
    "GRAPH_COMPETITOR_STRICT_BEHIND_ON_REAL_STRATUM": 25559,
    "GRAPH_COMPETITOR_STRICT_BEFORE_FROZEN_W_ON_REAL_STRATUM": 571,
}


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(body)
    value["row_sha256"] = object_sha(value)
    return value


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(body)
    value["object_sha256"] = object_sha(value)
    return value


def verify_row(value: dict[str, Any], label: str) -> None:
    body = copy.deepcopy(value)
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == object_sha(body), label + ":row closure")


def verify_object(value: dict[str, Any], label: str) -> None:
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(type(claim) is str and claim == object_sha(body), label + ":object closure")


def sha_file(path: Path) -> str:
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and not path.is_symlink(),
         "regular single-link:" + str(path))
    digest = hashlib.sha256()
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        need((opened.st_dev, opened.st_ino, opened.st_size) ==
             (before.st_dev, before.st_ino, before.st_size), "path/fd:" + str(path))
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            digest.update(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    final = path.lstat()
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
          before.st_ctime_ns) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
          after.st_ctime_ns) ==
         (final.st_dev, final.st_ino, final.st_size, final.st_mtime_ns,
          final.st_ctime_ns), "TOCTOU:" + str(path))
    return digest.hexdigest()


def pinned(path: Path, expected: str) -> None:
    need(sha_file(path) == expected, "file pin:" + str(path))


def strict_json(path: Path, expected: str) -> dict[str, Any]:
    pinned(path, expected)
    raw = path.read_bytes()
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "JSON framing:" + str(path))
    value = json.loads(raw.decode("utf-8", "strict"))
    need(type(value) is dict and canonical(value) == raw[:-1], "canonical JSON:" + str(path))
    if "object_sha256" in value:
        verify_object(value, str(path))
    return value


def iter_closed_rows(path: Path, expected: str, expected_count: int) -> Iterator[dict[str, Any]]:
    pinned(path, expected)
    count = 0
    with gzip.open(path, "rb") as stream:
        for raw in stream:
            count += 1
            need(raw.endswith(b"\n") and raw != b"\n", "ledger framing:" + str(path))
            value = json.loads(raw[:-1].decode("utf-8", "strict"))
            need(type(value) is dict and canonical(value) == raw[:-1],
                 "canonical ledger row:" + str(path))
            verify_row(value, str(path) + ":" + str(count))
            yield value
    need(count == expected_count, "ledger count:" + str(path))


def emit_new(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), 0o644)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "write:" + path.name)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    replay = path.read_bytes()
    need(replay == raw and (not raw or replay[-1:] == raw[-1:]),
         "terminal-byte replay:" + path.name)


class LedgerWriter:
    def __init__(self, path: Path, order: str =
                 "C72_ATLAS_ORDER_FILTERED_BY_EXACT_CURRENT_CHILD_WITNESS"):
        self.path = path
        self.order = order
        self.raw = path.open("xb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def write(self, row: dict[str, Any]) -> None:
        raw = canonical(row) + b"\n"
        self.gz.write(raw)
        self.sequence.update((row["row_sha256"] + "\n").encode("ascii"))
        self.count += 1

    def close(self) -> None:
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": sha_file(self.path),
            "size": self.path.stat().st_size,
        }


def arb_bounds(value: arb) -> dict[str, str]:
    return {"lower": str(value.lower()), "upper": str(value.upper())}


def strict_sign(value: arb) -> int:
    return 1 if bool(value > 0) else -1 if bool(value < 0) else 0


def rows(path: Path):
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def exact_dyadic(value: arb) -> Q:
    mantissa, exponent = value.man_exp()
    return Q(int(mantissa)) * (Q(2) ** int(exponent))


def strict_dyadic_depth(value: arb) -> int:
    """Return d with the independently checkable witness value > 2^-d."""
    need(bool(value > 0), "strict positive dyadic margin")
    lower = exact_dyadic(value.lower())
    need(lower > 0, "positive exact lower endpoint")
    depth = 0
    while not lower > Q(1, 2 ** depth):
        depth += 1
    return depth


def exact_faces(pair_index: int, exact_box: dict[str, Any]) -> dict[str, dict[str, Any]]:
    t0, t1 = exact_box["t"]
    p0, p1 = exact_box["p"]
    return {
        "t_lower": {"pair_index": pair_index, "fixed_axis": "t",
                    "fixed_value": t0, "varying_axis": "p",
                    "varying_interval": [p0, p1]},
        "t_upper": {"pair_index": pair_index, "fixed_axis": "t",
                    "fixed_value": t1, "varying_axis": "p",
                    "varying_interval": [p0, p1]},
        "p_lower": {"pair_index": pair_index, "fixed_axis": "p",
                    "fixed_value": p0, "varying_axis": "t",
                    "varying_interval": [t0, t1]},
        "p_upper": {"pair_index": pair_index, "fixed_axis": "p",
                    "fixed_value": p1, "varying_axis": "t",
                    "varying_interval": [t0, t1]},
    }


def exact_face_key(spec: dict[str, Any]) -> str:
    return object_sha({"schema": SCHEMA + ".exact-physical-face-key", **spec})


def endpoint_root_id(spec: dict[str, Any], target: str) -> str:
    return object_sha({
        "schema": SCHEMA + ".unique-discriminant-face-root",
        "collision1_target": target,
        "equation": "CENTERED_COLLISION1_DISCRIMINANT_EQUALS_ZERO",
        **spec,
    })


def conditional_owner_geometry(c39, parent_key, box):
    geometry = c39.round185.ad_initial_geometry(parent_key, box)
    raw = c39.round185.ad_root(geometry, c39.FROZEN_OWNER)
    centered_delta = c39.round185.centered_enclosure(
        c39.collision0_delta, parent_key, box, c39.FROZEN_OWNER, raw["Delta"]
    )
    if bool(centered_delta < 0):
        return {"owner_absent": True}
    upper = centered_delta.upper()
    if not bool(upper > 0):
        return {"owner_absent": False, "degenerate_delta": True}
    radical_upper_q = exact_dyadic(upper.sqrt().upper())
    radical = c39.round185.BASE.arb_interval(Q(0), radical_upper_q)
    _qx, _qy, ux_ad, uy_ad, _s = geometry
    ux, uy = ux_ad.value, uy_ad.value
    transverse, radius = raw["transverse"].value, raw["radius"].value
    h1 = (
        (radius * radius - 2 * transverse * transverse) * (ux * ux - uy * uy)
        - 4 * radical * transverse * ux * uy
    ) / (radius * radius)
    nx = (-radical * ux + transverse * uy) / radius
    ny = (-radical * uy - transverse * ux) / radius
    strict_chart = None
    if bool(h1 < 0) and bool(ny > 0):
        chart = "N_OR_S_STRICT_NOT_W"
        strict_chart = "N"
    elif bool(h1 < 0) and bool(ny < 0):
        chart = "N_OR_S_STRICT_NOT_W"
        strict_chart = "S"
    elif bool(h1 > 0) and bool(nx > 0):
        chart = "E_STRICT_NOT_W"
    elif bool(h1 > 0) and bool(nx < 0):
        chart = "W_STRICT"
    else:
        chart = "CHART_UNRESOLVED"
    return {
        "owner_absent": False,
        "centered_delta": str(centered_delta),
        "radical_conditional": str(radical),
        "H1_conditional": str(h1),
        "nx_conditional": str(nx),
        "ny_conditional": str(ny),
        "chart": chart,
        "strict_outgoing_chart": strict_chart,
        "raw": raw,
    }


def real_root_bounds(c39: Any, parent_key: str, box: Any,
                     target: str) -> tuple[dict[str, Any], Any, arb]:
    raw = c39.round185.ad_root(c39.round185.ad_initial_geometry(parent_key, box), target)
    delta = c39.round185.centered_enclosure(
        c39.collision0_delta, parent_key, box, target, raw["Delta"]
    )
    need(strict_sign(delta) == 0 and bool(delta.upper() > 0),
         "graph discriminant spans zero")
    radical_upper = delta.upper().sqrt().upper()
    return {
        "Delta": arb_bounds(delta),
        "near_lower": arb_bounds(raw["ell"].value.lower() - radical_upper),
        "near_upper": arb_bounds(raw["ell"].value.upper()),
        "far_upper": arb_bounds(raw["ell"].value.upper() + radical_upper),
    }, raw, delta


def graph_arrangement(c39: Any, parent_key: str, box: Any, target: str,
                      cell: dict[str, Any], pair_index: int,
                      exact_box: dict[str, Any]) -> tuple[dict[str, Any], Any, arb]:
    root_bounds, raw, delta = real_root_bounds(c39, parent_key, box, target)
    derivative_signs = [strict_sign(raw["Delta"].derivative[index]) for index in (0, 1)]
    need(all(sign != 0 for sign in derivative_signs), "strict graph gradient")
    corners: dict[tuple[int, int], dict[str, Any]] = {}
    for ti, t in enumerate((box.t0, box.t1)):
        for pi, p in enumerate((box.p0, box.p1)):
            point = c39.round185.point_box(box, t, p, box.s0, ".c74-corner")
            value = c39.collision0_delta(parent_key, point, target).value
            sign = strict_sign(value)
            need(sign != 0, "graph avoids every exact child corner")
            corners[(ti, pi)] = {
                "t": str(t), "p": str(p), "Delta": arb_bounds(value),
                "sign": "POSITIVE" if sign > 0 else "NEGATIVE",
            }
    need({1, -1} == {1 if row["sign"] == "POSITIVE" else -1
                     for row in corners.values()}, "graph has both corner signs")
    face_ends = {
        "t_lower": ((0, 0), (0, 1)), "t_upper": ((1, 0), (1, 1)),
        "p_lower": ((0, 0), (1, 0)), "p_upper": ((0, 1), (1, 1)),
    }
    base_t = tuple(Q(value["value"]) for value in cell["physical_t_interval"])
    base_p = tuple(Q(value) for value in cell["physical_p_interval"])
    physical_faces = exact_faces(pair_index, exact_box)
    boundary_incidence = []
    for face, endpoints in face_ends.items():
        signs = [1 if corners[key]["sign"] == "POSITIVE" else -1 for key in endpoints]
        if signs[0] * signs[1] >= 0:
            continue
        axis = face[0]
        side = face.split("_")[1]
        coordinate = (box.t0 if face == "t_lower" else box.t1 if face == "t_upper"
                      else box.p0 if face == "p_lower" else box.p1)
        base = base_t if axis == "t" else base_p
        external = coordinate == (base[0] if side == "lower" else base[1])
        role = ("SOURCE_CELL_BOUNDARY_ENDPOINT" if external else
                "EXCLUDES_DUPLICATE_SHARED_FACE" if side == "lower" else
                "OWNS_SHARED_FACE")
        exact_face = physical_faces[face]
        face_key = exact_face_key(exact_face)
        boundary_incidence.append({
            "face": face, "exact_face_coordinate": str(coordinate),
            "exact_face": exact_face,
            "face_key_sha256": face_key,
            "endpoint_root_id": endpoint_root_id(exact_face, target),
            "collision1_target": target,
            "endpoint_corner_signs": [corners[key]["sign"] for key in endpoints],
            "unique_endpoint_definition":
                "UNIQUE_ZERO_OF_PINNED_DISCRIMINANT_ON_RATIONAL_FACE",
            "strict_tangential_derivative_sign": (
                derivative_signs[1] if axis == "t" else derivative_signs[0]
            ),
            "half_open_or_source_boundary_role": role,
            "source_cell_boundary": external,
        })
    need(len(boundary_incidence) == 2, "exact graph has two noncorner face endpoints")
    return {
        "graph_target": target,
        "centered_Delta": arb_bounds(delta),
        "strict_gradient": {
            "dt": arb_bounds(raw["Delta"].derivative[0]),
            "dp": arb_bounds(raw["Delta"].derivative[1]),
            "dt_sign": derivative_signs[0], "dp_sign": derivative_signs[1],
        },
        "root_interval_on_real_stratum": root_bounds,
        "corner_census": [corners[key] for key in sorted(corners)],
        "boundary_incidence": boundary_incidence,
        "corner_tie_count": 0,
        "graph_dimension": 1,
        "ambient_child_dimension": 2,
    }, raw, delta


def decision_row(c39: Any, atlas: dict[str, Any], source: dict[str, Any],
                 task: dict[str, Any]) -> dict[str, Any]:
    box, active = c39.reconstruct_box(task["cell"], atlas["child_path"])
    need(len(active) == 2 and c39.FROZEN_OWNER in active, "two active roots including W")
    _stage, natural = c39.c38.round166.classify_active(
        task["cell"]["gate3_chart"], box, active
    )
    enhanced = [c39.enhanced_record(
        task["c38_source"]["representative_origin_key"], box, record
    )[0] for record in natural]
    future = [record for record in enhanced if record.classification == "strict_future_root"]
    unresolved = [record for record in enhanced
                  if record.classification == "unresolved_discriminant"]
    need(len(future) == len(unresolved) == 1, "one strict root and one graph root")
    graph_record, strict_record = unresolved[0], future[0]
    parent_key = task["c38_source"]["representative_origin_key"]
    arrangement, graph_raw, _delta = graph_arrangement(
        c39, parent_key, box, graph_record.target_id, task["cell"],
        atlas["pair_index"], atlas["exact_representative_box"]
    )
    graph_bounds = arrangement["root_interval_on_real_stratum"]
    graph_near_lower = graph_raw["ell"].value.lower() - _delta.upper().sqrt().upper()
    graph_near_upper = graph_raw["ell"].value.upper()
    graph_far_upper = graph_raw["ell"].value.upper() + _delta.upper().sqrt().upper()
    physical_tangency_terminal = False
    physical_future_margin: dict[str, Any] | None = None
    conditional_h1: dict[str, Any]
    if graph_record.target_id == c39.FROZEN_OWNER:
        need(strict_record.target_id != c39.FROZEN_OWNER and
             bool(graph_near_upper < strict_record.near),
             "W graph strictly before other root on its real stratum")
        relation = "FROZEN_W_STRICT_BEFORE_OTHER_ON_REAL_STRATUM"
        gap = strict_record.near - graph_near_upper
        conditional = conditional_owner_geometry(c39, parent_key, box)
        need(conditional["chart"] == "N_OR_S_STRICT_NOT_W" and
             conditional["strict_outgoing_chart"] in {"N", "S"},
             "conditional W-real outgoing mismatch")
        conditional_h1 = {key: value for key, value in conditional.items() if key != "raw"}
        physical_tangency_terminal = True
    else:
        need(strict_record.target_id == c39.FROZEN_OWNER, "strict root is frozen W")
        h1 = c39.h1_route(parent_key, box)
        need(h1["kind"] == "STRICT_SIDE" and h1["chart"] in {"N", "S"},
             "whole-child outgoing mismatch")
        conditional_h1 = {
            "method": h1["method"], "kind": h1["kind"], "chart": h1["chart"],
            "H1_centered": h1["H1_centered"], "H1_natural": h1["H1_natural"],
            "normal_signs": h1["normal_signs"],
        }
        if bool(graph_far_upper < 0):
            relation = "GRAPH_COMPETITOR_STRICT_BEHIND_ON_REAL_STRATUM"
            gap = -graph_far_upper
        elif bool(graph_near_upper < strict_record.near):
            relation = "GRAPH_COMPETITOR_STRICT_BEFORE_FROZEN_W_ON_REAL_STRATUM"
            gap = strict_record.near - graph_near_upper
            physical_tangency_terminal = True
        elif bool(strict_record.near < graph_near_lower):
            relation = "FROZEN_W_STRICT_BEFORE_GRAPH_COMPETITOR_ON_REAL_STRATUM"
            gap = graph_near_lower - strict_record.near
        else:
            raise Rejected("root equality not excluded")
    need(bool(gap > 0), "strict root-order gap")
    if physical_tangency_terminal:
        need(bool(graph_near_lower > 0), "physical tangency strict future margin")
        future_depth = strict_dyadic_depth(graph_near_lower)
        physical_future_margin = {
            "near_root_lower": arb_bounds(graph_near_lower),
            "strict_dyadic_depth": future_depth,
            "strict_lower_bound": "2^(-" + str(future_depth) + ")",
        }
    arrangement["physical_future_tangency"] = physical_tangency_terminal
    arrangement["physical_future_margin"] = physical_future_margin
    for incidence in arrangement["boundary_incidence"]:
        incidence["retained_terminal_endpoint_occurrence"] = physical_tangency_terminal
    zero_exit = ("CEMETERY_OR_SOURCE_GRAZING_TERMINAL"
                 if physical_tangency_terminal else "STRICT_EXCLUSION")
    zero_disposition = ("CEMETERY_TANGENCY_TERMINAL"
                        if physical_tangency_terminal else
                        "STRICT_EXCLUSION_NONFUTURE_GRAPH_AND_OUTGOING_MISMATCH")
    return close_row({
        "schema": SCHEMA + ".decision-row",
        "C72_obligation_row_sha256": atlas["row_sha256"],
        "C65_aggregate_child_row_sha256": atlas["C65_aggregate_child_row_sha256"],
        "C61_aggregate_leaf_row_sha256": atlas["C61_aggregate_leaf_row_sha256"],
        "C68_structural_task_row_sha256": atlas["C68_structural_task_row_sha256"],
        "C69c_blocker_row_sha256": atlas["C69c_blocker_row_sha256"],
        "C58_source_row_sha256": source["source_C58_leaf_row_sha256"],
        "pair_index": atlas["pair_index"], "source_path": atlas["source_path"],
        "child_path": atlas["child_path"],
        "parent_volume_fraction": atlas["parent_volume_fraction"],
        "exact_representative_box": atlas["exact_representative_box"],
        "exact_reflected_box": atlas["exact_reflected_box"],
        "source_structural_category": atlas["structural_category"],
        "legacy_child_route_witness": atlas["child_route_witness"],
        "parent_key": parent_key, "gate3_chart": task["cell"]["gate3_chart"],
        "active_targets": list(active),
        "strict_root": {
            "target": strict_record.target_id, "ell": arb_bounds(strict_record.ell),
            "Delta": arb_bounds(strict_record.discriminant),
            "near": arb_bounds(strict_record.near), "far": arb_bounds(strict_record.far),
        },
        "discriminant_graph": arrangement,
        "root_order": {
            "relation": relation, "strict_gap": arb_bounds(gap),
            "root_equality_realizable": False,
            "exact_order_partition": [
                "GRAPH_TARGET_ABSENT", "GRAPH_TARGET_NONFUTURE",
                "GRAPH_TARGET_STRICT_BEFORE_FROZEN_W",
                "FROZEN_W_STRICT_BEFORE_OTHER",
            ],
            "first_contact_precedence_closed": True,
        },
        "outgoing_evidence": conditional_h1,
        "sealed_strata": [
            {"stratum": "DELTA_GRAPH_TARGET_NEGATIVE_OPEN_SLAB",
             "exit_class": "STRICT_EXCLUSION",
             "disposition": "FROZEN_WORD_OWNER_OR_OUTGOING_MISMATCH"},
            {"stratum": "DELTA_GRAPH_TARGET_ZERO_GRAPH",
             "exit_class": zero_exit, "disposition": zero_disposition,
             "physical_future_tangency": physical_tangency_terminal},
            {"stratum": "DELTA_GRAPH_TARGET_POSITIVE_OPEN_SLAB",
             "exit_class": "STRICT_EXCLUSION",
             "disposition": "STRICT_ROOT_ORDER_AND_OUTGOING_WORD_MISMATCH"},
        ],
        "complete_child_decision": "SEALED_TWO_OPEN_SLABS_PLUS_EXACT_GRAPH_STRATUM",
        "additional_dyadic_depth_used": 0,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "global_unresolved_decrement": 0,
    })


def probe_main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--pairs")
    parser.add_argument("--per-pair", type=int)
    parser.add_argument("--progress", type=int, default=1000)
    args = parser.parse_args()
    ctx.prec = 384
    targets = [row for row in rows(C72) if row["child_route_witness"] == SELECTOR]
    if args.pairs:
        wanted_pairs = {int(value) for value in args.pairs.split(",")}
        targets = [row for row in targets if row["pair_index"] in wanted_pairs]
    if args.per_pair is not None:
        retained = []
        retained_counts = Counter()
        for row in targets:
            if retained_counts[row["pair_index"]] < args.per_pair:
                retained.append(row)
                retained_counts[row["pair_index"]] += 1
        targets = retained
    if args.limit is not None:
        targets = targets[:args.limit]
    wanted_c65 = {row["C65_aggregate_child_row_sha256"] for row in targets}
    c65 = {row["row_sha256"]: row for row in rows(C65) if row["row_sha256"] in wanted_c65}
    wanted_c58 = {row["source_C58_leaf_row_sha256"] for row in c65.values()}
    c58 = {row["row_sha256"]: row for row in rows(C58) if row["row_sha256"] in wanted_c58}

    context = c41.load_context(C40, None, formal=False)
    c41.install_complete_immutable_cache()
    config = c41.decode_worker_config(context["config"])
    c40_rows = c41.c38.read_ledger(C40, context["result"]["ledgers"]["routed_leaf_cells"])
    c40_index = {row["row_sha256"]: (index, row) for index, row in enumerate(c40_rows)}
    task_cache = {}

    census = Counter()
    by_pair = Counter()
    by_pair_outcome = Counter()
    by_active = Counter()
    by_unresolved = Counter()
    competitor_winners = Counter()
    minimum_gap = None
    examples = {}
    pair_examples = {}
    c39 = c41.c39
    for ordinal, atlas in enumerate(targets, 1):
        source = c65[atlas["C65_aggregate_child_row_sha256"]]
        c58_source = c58[source["source_C58_leaf_row_sha256"]]
        c40_hash = c58_source["C40_source_row_sha256"]
        task = task_cache.get(c40_hash)
        if task is None:
            c40_ordinal, c40_source = c40_index[c40_hash]
            task = c41.task_for_row(c40_ordinal, c40_source, context)
            task_cache[c40_hash] = task
        box, active = c39.reconstruct_box(task["cell"], atlas["child_path"])
        stage, natural = c39.c38.round166.classify_active(task["cell"]["gate3_chart"], box, active)
        enhanced = []
        evidence = []
        for record in natural:
            replacement, detail = c39.enhanced_record(
                task["c38_source"]["representative_origin_key"], box, record
            )
            enhanced.append(replacement)
            if detail is not None:
                evidence.append(detail)
        leaf = c39.c38.round166.classify_from_records(
            task["cell"]["gate3_chart"], box, enhanced
        )
        future = [record for record in enhanced if record.classification == "strict_future_root"]
        unresolved = [record for record in enhanced if record.classification in {
            "unresolved_discriminant", "unresolved_root_sign"
        }]
        owner = next((record for record in future if record.target_id == c39.FROZEN_OWNER), None)
        owner_any = next((record for record in enhanced if record.target_id == c39.FROZEN_OWNER), None)
        earlier = [] if owner is None else [
            record for record in future
            if record.target_id != c39.FROZEN_OWNER and bool(record.near < owner.near)
        ]
        conditional_earlier = []
        conditional_debug = None
        conditional_geometry = None
        owner_real_region_near_lower = None
        if owner is None and owner_any is not None and owner_any.classification in {
            "unresolved_discriminant", "unresolved_root_sign"
        }:
            parent_key = task["c38_source"]["representative_origin_key"]
            conditional_geometry = conditional_owner_geometry(c39, parent_key, box)
            raw_owner = c39.round185.ad_root(
                c39.round185.ad_initial_geometry(parent_key, box), c39.FROZEN_OWNER
            )
            centered_delta = c39.round185.centered_enclosure(
                c39.collision0_delta, parent_key, box, c39.FROZEN_OWNER,
                raw_owner["Delta"],
            )
            if not bool(centered_delta < 0):
                delta_upper = centered_delta.upper()
                if bool(delta_upper > 0):
                    owner_real_region_near_lower = (
                        raw_owner["ell"].value.lower() - delta_upper.sqrt()
                    )
                    conditional_earlier = [
                        record for record in future
                        if record.target_id != c39.FROZEN_OWNER
                        and bool(record.near < owner_real_region_near_lower)
                    ]
                    conditional_debug = {
                        "owner_real_region_near_lower": str(owner_real_region_near_lower),
                        "future_near": {
                            record.target_id: str(record.near)
                            for record in future
                        },
                    }
        conditional_competitors_behind = []
        if owner is not None:
            parent_key = task["c38_source"]["representative_origin_key"]
            for unresolved_record in unresolved:
                if unresolved_record.target_id == c39.FROZEN_OWNER:
                    continue
                raw_other = c39.round185.ad_root(
                    c39.round185.ad_initial_geometry(parent_key, box),
                    unresolved_record.target_id,
                )
                delta_other = c39.round185.centered_enclosure(
                    c39.collision0_delta, parent_key, box,
                    unresolved_record.target_id, raw_other["Delta"],
                )
                if bool(delta_other < 0):
                    conditional_competitors_behind.append(unresolved_record.target_id)
                    continue
                upper_other = delta_other.upper()
                if bool(upper_other > 0):
                    far_upper = raw_other["ell"].value.upper() + upper_other.sqrt().upper()
                    if bool(far_upper < 0):
                        conditional_competitors_behind.append(unresolved_record.target_id)
        resumed = None
        if owner is not None and unresolved:
            parent_key = task["c38_source"]["representative_origin_key"]
            h1 = c39.h1_route(parent_key, box)
            resumed = {"H1_kind": h1["kind"], "H1_chart": h1["chart"]}
            if h1["kind"] == "STRICT_SIDE" and h1["chart"] != "W":
                resumed["outcome"] = "STRICT_EXCLUSION_OUTGOING_CHART_MISMATCH"
            elif (h1["kind"] == "STRICT_SIDE" and h1["chart"] == "W" and
                  len(conditional_competitors_behind) == len(unresolved)):
                route, witness, collision = c39.downstream_route(
                    task["c38_source"], box,
                    config["original_path"], config["reflected_path"],
                    config["pair_index"], config["pattern_index"], config["cores"],
                )
                resumed.update({"downstream_route": route, "witness": witness,
                                "collision": collision})
                if route.startswith("EXCLUDED_"):
                    resumed["outcome"] = "STRICT_EXCLUSION_DOWNSTREAM"
                elif route.startswith("LIVE_"):
                    resumed["outcome"] = "SEALED_COLLISION3_HANDOFF_CANDIDATE"
                else:
                    resumed["outcome"] = "EXACT_DOWNSTREAM_BLOCKER"
            else:
                resumed["outcome"] = (
                    "EXACT_ROOT_ORDER_BLOCKER"
                    if h1["kind"] == "STRICT_SIDE" and h1["chart"] == "W"
                    else "EXACT_H1_GRAPH_OR_BOUNDARY_BLOCKER"
                )
        if earlier:
            outcome = "STRICT_EXCLUSION_ANY_COMPETITOR_BEFORE_FROZEN_OWNER"
            winner = min(earlier, key=lambda item: float(item.near.mid()))
            competitor_winners[winner.target_id] += 1
            gap = owner.near - winner.near
            lower = str(gap.lower())
            if minimum_gap is None or float(gap.lower()) < minimum_gap[0]:
                minimum_gap = (float(gap.lower()), lower, atlas["row_sha256"], winner.target_id)
        elif conditional_earlier:
            outcome = "STRICT_EXCLUSION_FROZEN_OWNER_ABSENT_OR_COMPETITOR_BEFORE_ON_REAL_REGION"
            winner = min(conditional_earlier, key=lambda item: float(item.near.mid()))
            competitor_winners[winner.target_id] += 1
            gap = owner_real_region_near_lower - winner.near
            lower = str(gap.lower())
            if minimum_gap is None or float(gap.lower()) < minimum_gap[0]:
                minimum_gap = (float(gap.lower()), lower, atlas["row_sha256"], winner.target_id)
        elif resumed is not None and resumed["outcome"] not in {
            "EXACT_DOWNSTREAM_BLOCKER", "EXACT_H1_GRAPH_OR_BOUNDARY_BLOCKER",
            "EXACT_ROOT_ORDER_BLOCKER",
        }:
            outcome = resumed["outcome"]
        elif (conditional_geometry is not None and
              conditional_geometry.get("chart") in {
                  "N_OR_S_STRICT_NOT_W", "E_STRICT_NOT_W"
              }):
            # On Delta_W<0 the frozen first owner is absent.  On Delta_W>=0
            # this interval formula proves that its outgoing chart is not W.
            outcome = "STRICT_EXCLUSION_OWNER_ABSENT_OR_CONDITIONAL_OUTGOING_CHART_MISMATCH"
        elif leaf.classification == "no_future_root":
            outcome = "STRICT_EXCLUSION_NO_FUTURE_ROOT"
        elif leaf.classification == "unique_first" and leaf.owner_target != c39.FROZEN_OWNER:
            outcome = "STRICT_EXCLUSION_UNIQUE_FIRST_OWNER_MISMATCH"
        elif leaf.classification == "unique_first" and leaf.owner_target == c39.FROZEN_OWNER:
            outcome = "FROZEN_OWNER_UNIQUE_FIRST"
        elif owner is None:
            outcome = "FROZEN_OWNER_NOT_STRICT_FUTURE"
        elif unresolved:
            outcome = "EXACT_GRAPH_OR_ROOT_SIGN_ARRANGEMENT_REQUIRED"
        else:
            outcome = "STRICT_FUTURE_INTERVAL_ORDER_TIE"
        census[outcome] += 1
        by_pair[atlas["pair_index"]] += 1
        by_pair_outcome[(atlas["pair_index"], outcome)] += 1
        by_active[len(active)] += 1
        by_unresolved[(len(unresolved), tuple(sorted(row.classification for row in unresolved)))] += 1
        if outcome not in examples:
            examples[outcome] = {
                "C72_row_sha256": atlas["row_sha256"],
                "pair_index": atlas["pair_index"],
                "child_path": atlas["child_path"],
                "active_count": len(active),
                "future_targets": [record.target_id for record in future],
                "unresolved": [[record.target_id, record.classification] for record in unresolved],
                "enhanced_leaf": leaf.classification,
                "enhanced_owner": leaf.owner_target,
                "regular_surface_evidence_count": len(evidence),
                "conditional_debug": conditional_debug,
                "conditional_geometry": None if conditional_geometry is None else {
                    key: value for key, value in conditional_geometry.items() if key != "raw"
                },
                "conditional_competitors_behind": conditional_competitors_behind,
                "resumed": resumed,
            }
        if atlas["pair_index"] not in pair_examples:
            pair_examples[atlas["pair_index"]] = {
                "outcome": outcome,
                "C72_row_sha256": atlas["row_sha256"],
                "child_path": atlas["child_path"],
                "parent_key": task["c38_source"]["representative_origin_key"],
                "chart": task["cell"]["gate3_chart"],
                "active_targets": list(active),
                "records": [
                    {
                        "target": record.target_id,
                        "classification": record.classification,
                        "ell": str(record.ell),
                        "Delta": str(record.discriminant),
                        "near": None if record.near is None else str(record.near),
                    }
                    for record in enhanced
                ],
                "conditional_competitors_behind": conditional_competitors_behind,
                "resumed": resumed,
            }
        if args.progress and ordinal % args.progress == 0:
            print(json.dumps({"processed": ordinal, "census": dict(census)}, sort_keys=True), flush=True)

    result = {
        "scope_count": len(targets),
        "source_count": len({row["C61_aggregate_leaf_row_sha256"] for row in targets}),
        "task_count": len(task_cache),
        "outcome_census": dict(sorted(census.items())),
        "pair_census": {str(key): value for key, value in sorted(by_pair.items())},
        "pair_outcome_census": {
            str(pair) + ":" + outcome: count
            for (pair, outcome), count in sorted(by_pair_outcome.items())
        },
        "active_count_census": {str(key): value for key, value in sorted(by_active.items())},
        "unresolved_record_census": {
            str(key): value for key, value in sorted(by_unresolved.items(), key=lambda item: str(item[0]))
        },
        "strict_competitor_census": dict(sorted(competitor_winners.items())),
        "minimum_strict_order_gap": minimum_gap,
        "examples": examples,
        "pair_examples": pair_examples,
    }
    print("FINAL " + json.dumps(result, sort_keys=True), flush=True)
    return 0


def validate_upstreams() -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    for directory in C72_DIRS:
        pinned(directory / C72_LEDGER_NAME, FILE_PINS["C72_LEDGER"])
        strict_json(directory / C72_RESULT_NAME, FILE_PINS["C72_RESULT"])
        strict_json(directory / C72_VERIFY_NAME, FILE_PINS["C72_VERIFY"])
    for directory in C72O_DIRS:
        pinned(directory / C72O_LEDGER_NAME, FILE_PINS["C72O_LEDGER"])
        strict_json(directory / C72O_RESULT_NAME, FILE_PINS["C72O_RESULT"])
    strict_json(C72O_VERIFY, FILE_PINS["C72O_VERIFY"])
    for directory in C73_DIRS:
        pinned(directory / C73_LEDGER_NAME, FILE_PINS["C73_LEDGER"])
        strict_json(directory / C73_RESULT_NAME, FILE_PINS["C73_RESULT"])
    for path in C73_VERIFIES:
        strict_json(path, FILE_PINS["C73_VERIFY"])

    fixed_files = {
        "C65_RESULT": DELIVERABLES / "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json",
        "C65_LEAVES": C65,
        "C65_VERIFY": DELIVERABLES / "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v9.json",
        "C65_SELFTEST": DELIVERABLES / "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json",
        "C65_REPLAY": DELIVERABLES / "cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v9.json",
        "C65_MANIFEST": DELIVERABLES / "cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256",
        "C65_OUTER": DELIVERABLES / "cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json",
        "C69_RESULT": DELIVERABLES / "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json",
        "C69_BLOCKERS": DELIVERABLES / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz",
        "C69_VERIFY": DELIVERABLES / "cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json",
        "C69_MANIFEST": DELIVERABLES / "cm2_round306c69c_descriptor_repair_supersession_independent_manifest_v1.sha256",
        "C69_OUTER": DELIVERABLES / "cm2_round306c69c_descriptor_repair_supersession_independent_outer_publication_receipt_v1.json",
        "C58_RESULT": DELIVERABLES / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json",
        "C58_LEAVES": C58,
        "C40_RESULT": C40 / "result.json",
    }
    for key, path in fixed_files.items():
        pinned(path, FILE_PINS[key])
    c65_result = strict_json(fixed_files["C65_RESULT"], FILE_PINS["C65_RESULT"])
    c58_result = strict_json(fixed_files["C58_RESULT"], FILE_PINS["C58_RESULT"])
    need(c65_result["ledgers"]["aggregate_leaves"]["row_count"] == 358_919 and
         c58_result["ledgers"]["leaves"]["row_count"] == 5_548,
         "C65/C58 descriptor census")

    targets = []
    selector_census = Counter()
    for row in iter_closed_rows(C72_DIRS[0] / C72_LEDGER_NAME,
                                FILE_PINS["C72_LEDGER"], 134_155):
        selector_census[row["child_route_witness"]] += 1
        if row["child_route_witness"] == SELECTOR:
            targets.append(row)
    need(len(targets) == 42_926, "exact current-child multi-order selector")
    target_ids = {row["row_sha256"] for row in targets}
    need(len(target_ids) == len(targets), "target identities unique")
    outgoing_ids = {
        row["C72_atlas_row_sha256"]
        for row in iter_closed_rows(C72O_DIRS[0] / C72O_LEDGER_NAME,
                                    FILE_PINS["C72O_LEDGER"], 18_668)
    }
    grazing_ids = {
        row["C72_obligation_row_sha256"]
        for row in iter_closed_rows(C73_DIRS[0] / C73_LEDGER_NAME,
                                    FILE_PINS["C73_LEDGER"], 1_163)
    }
    need(len(outgoing_ids) == 18_668 and len(grazing_ids) == 1_163 and
         target_ids.isdisjoint(outgoing_ids) and target_ids.isdisjoint(grazing_ids) and
         outgoing_ids.isdisjoint(grazing_ids), "C72o/C73v2 exact scope disjointness")
    return targets, c65_result, c58_result


def endpoint_occurrence_identifier(decision: dict[str, Any],
                                   incidence: dict[str, Any]) -> str:
    return object_sha({
        "schema": SCHEMA + ".endpoint-occurrence-id",
        "C74_decision_row_sha256": decision["row_sha256"],
        "endpoint_root_id": incidence["endpoint_root_id"],
        "face": incidence["face"],
    })


def build_endpoint_incidence(output: Path,
                             physical_decisions: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Close every retained graph endpoint against the complete pinned C72 atlas."""
    drafts: list[dict[str, Any]] = []
    by_root: dict[str, list[dict[str, Any]]] = {}
    root_specs: dict[str, dict[str, Any]] = {}
    roots_by_face: dict[str, set[str]] = {}
    for decision in physical_decisions:
        need(decision["sealed_strata"][1]["physical_future_tangency"] is True,
             "endpoint source is retained physical tangency")
        incidences = decision["discriminant_graph"]["boundary_incidence"]
        need(len(incidences) == 2, "two retained endpoint occurrences")
        for incidence in incidences:
            need(incidence["retained_terminal_endpoint_occurrence"] is True,
                 "retained endpoint marker")
            identifier = endpoint_occurrence_identifier(decision, incidence)
            draft = {
                "endpoint_occurrence_id": identifier,
                "endpoint_root_id": incidence["endpoint_root_id"],
                "face_key_sha256": incidence["face_key_sha256"],
                "exact_face": incidence["exact_face"],
                "collision1_target": incidence["collision1_target"],
                "face": incidence["face"],
                "source_cell_boundary": incidence["source_cell_boundary"],
                "C74_decision_row_sha256": decision["row_sha256"],
                "C72_atlas_row_sha256": decision["C72_obligation_row_sha256"],
                "C65_aggregate_child_row_sha256": decision["C65_aggregate_child_row_sha256"],
                "C61_aggregate_leaf_row_sha256": decision["C61_aggregate_leaf_row_sha256"],
                "C68_structural_task_row_sha256": decision["C68_structural_task_row_sha256"],
                "C69c_blocker_row_sha256": decision["C69c_blocker_row_sha256"],
                "C58_source_row_sha256": decision["C58_source_row_sha256"],
                "parent_key": decision["parent_key"],
                "source_path": decision["source_path"],
                "child_path": decision["child_path"],
                "unique_root_proof": {
                    "equation": "CENTERED_COLLISION1_DISCRIMINANT_EQUALS_ZERO",
                    "rational_face_end_signs": incidence["endpoint_corner_signs"],
                    "strict_tangential_derivative_sign":
                        incidence["strict_tangential_derivative_sign"],
                    "corner_incidence": False,
                    "unique_root_on_exact_face": True,
                },
            }
            root_id = incidence["endpoint_root_id"]
            spec = {"face_key_sha256": incidence["face_key_sha256"],
                    "exact_face": incidence["exact_face"],
                    "collision1_target": incidence["collision1_target"]}
            if root_id in root_specs:
                need(root_specs[root_id] == spec, "endpoint root specification consistency")
            else:
                root_specs[root_id] = spec
            drafts.append(draft)
            by_root.setdefault(root_id, []).append(draft)
            roots_by_face.setdefault(incidence["face_key_sha256"], set()).add(root_id)
    need(len(drafts) == 34_734, "exact retained endpoint occurrence census")
    need(len({row["endpoint_occurrence_id"] for row in drafts}) == len(drafts),
         "endpoint occurrence identities unique")

    atlas_incidents: dict[str, list[dict[str, Any]]] = {
        identifier: [] for identifier in root_specs
    }
    for atlas in iter_closed_rows(C72_DIRS[0] / C72_LEDGER_NAME,
                                  FILE_PINS["C72_LEDGER"], 134_155):
        for face, spec in exact_faces(atlas["pair_index"],
                                      atlas["exact_representative_box"]).items():
            key = exact_face_key(spec)
            for root_id in roots_by_face.get(key, ()):
                atlas_incidents[root_id].append({
                    "C72_atlas_row_sha256": atlas["row_sha256"],
                    "face": face,
                    "face_side": "HIGH" if face.endswith("upper") else "LOW",
                    "child_route_witness": atlas["child_route_witness"],
                    "required_decider": atlas["required_decider"],
                    "child_route_classification": atlas["child_route_classification"],
                    "C65_aggregate_child_row_sha256":
                        atlas["C65_aggregate_child_row_sha256"],
                    "C68_structural_task_row_sha256":
                        atlas["C68_structural_task_row_sha256"],
                    "C69c_blocker_row_sha256": atlas["C69c_blocker_row_sha256"],
                    "compact_chart_shadow":
                        atlas["exact_reflected_box"]["compact_chart"],
                })

    occurrence_by_id = {row["endpoint_occurrence_id"]: row for row in drafts}
    occurrence_identity_by_face = {
        (row["C72_atlas_row_sha256"], row["face"], row["endpoint_root_id"]):
            row["endpoint_occurrence_id"] for row in drafts
    }
    class_census = Counter()
    root_class_census = Counter()
    internal_pair_root_count = 0
    cross_scope_root_count = 0
    source_boundary_root_count = 0
    atlas_boundary_root_count = 0
    rows_to_write: list[dict[str, Any]] = []
    for root_id in sorted(by_root):
        selected = sorted(by_root[root_id], key=lambda row: row["endpoint_occurrence_id"])
        incidents = sorted(atlas_incidents[root_id], key=lambda row:
                           (row["C72_atlas_row_sha256"], row["face"]))
        need(1 <= len(incidents) <= 2, "one or two complete-atlas face incidences")
        need(len({(row["C72_atlas_row_sha256"], row["face"]) for row in incidents}) ==
             len(incidents), "atlas incidence identity unique")
        selected_keys = {(row["C72_atlas_row_sha256"], row["face"]) for row in selected}
        incident_keys = {(row["C72_atlas_row_sha256"], row["face"]) for row in incidents}
        need(selected_keys <= incident_keys and 1 <= len(selected) <= 2,
             "selected endpoints embedded in complete-atlas incidence")
        high = [row for row in incidents if row["face_side"] == "HIGH"]
        if len(incidents) == 2:
            need(len(high) == 1 and {row["face_side"] for row in incidents} == {"HIGH", "LOW"},
                 "shared face has one canonical high-face owner")
            owner = high[0]
        else:
            owner = incidents[0]
        owner_occurrence = occurrence_identity_by_face.get(
            (owner["C72_atlas_row_sha256"], owner["face"], root_id)
        )
        if len(selected) == 2:
            need(len(incidents) == 2 and selected_keys == incident_keys,
                 "internal C74 endpoint pair closes complete face incidence")
            incidence_class = "PAIRED_INTERNAL_C74_ENDPOINT"
            internal_pair_root_count += 1
        elif len(incidents) == 2:
            incidence_class = "ADJACENT_C72_CROSS_SCOPE_GLUE"
            cross_scope_root_count += 1
        elif selected[0]["source_cell_boundary"]:
            incidence_class = "SOURCE_CELL_BOUNDARY_CONSUMER"
            source_boundary_root_count += 1
        else:
            incidence_class = "ATLAS_COMPLEMENT_BOUNDARY_CONSUMER"
            atlas_boundary_root_count += 1
        root_class_census[incidence_class] += 1
        selected_ids = [row["endpoint_occurrence_id"] for row in selected]
        for draft in selected:
            adjacent = [row for row in incidents
                        if (row["C72_atlas_row_sha256"], row["face"]) !=
                           (draft["C72_atlas_row_sha256"], draft["face"])]
            counterparts = [identifier for identifier in selected_ids
                            if identifier != draft["endpoint_occurrence_id"]]
            if incidence_class == "PAIRED_INTERNAL_C74_ENDPOINT":
                need(len(counterparts) == len(adjacent) == 1,
                     "one internal counterpart and adjacent face")
                consumer = {"kind": incidence_class,
                            "counterpart_endpoint_occurrence_id": counterparts[0],
                            "counterpart_C74_decision_row_sha256":
                                occurrence_by_id[counterparts[0]]["C74_decision_row_sha256"]}
            elif incidence_class == "ADJACENT_C72_CROSS_SCOPE_GLUE":
                need(not counterparts and len(adjacent) == 1,
                     "one adjacent cross-scope consumer")
                consumer = {"kind": incidence_class,
                            "adjacent_C72_face": adjacent[0]}
            else:
                need(not counterparts and not adjacent,
                     "explicit singleton source/atlas boundary consumer")
                consumer = {
                    "kind": incidence_class,
                    "boundary_face_key_sha256": draft["face_key_sha256"],
                    "authority_chain": {
                        "C72_atlas_row_sha256": draft["C72_atlas_row_sha256"],
                        "C65_aggregate_child_row_sha256":
                            draft["C65_aggregate_child_row_sha256"],
                        "C68_structural_task_row_sha256":
                            draft["C68_structural_task_row_sha256"],
                        "C69c_blocker_row_sha256": draft["C69c_blocker_row_sha256"],
                    },
                }
            body = {
                "schema": SCHEMA + ".endpoint-incidence-row",
                **draft,
                "complete_C72_face_incidence": incidents,
                "complete_C72_face_incidence_count": len(incidents),
                "incidence_class": incidence_class,
                "consumer": consumer,
                "canonical_half_open_owner": {
                    "C72_atlas_row_sha256": owner["C72_atlas_row_sha256"],
                    "face": owner["face"],
                    "selected_C74_endpoint_occurrence_id": owner_occurrence,
                    "rule": "LOWER_COORDINATE_CHILD_HIGH_FACE_ELSE_SINGLE_ATLAS_BOUNDARY_FACE",
                    "unique": True,
                },
                "coordinate_and_seam_authority": {
                    "physical_face_coordinates": "PINNED_C72_EXACT_REPRESENTATIVE_BOX",
                    "compact_chart_shadow": "PINNED_C72_EXACT_REFLECTED_BOX",
                    "history_and_scope": "PINNED_C65_C68_C69C_ROW_CHAIN",
                    "local_cross_chart_or_source_seam_reinterpretation": False,
                },
                "same_physical_trace_duplicate_unassigned": False,
                "endpoint_incidence_closed": True,
                "formal_credit": 0,
                "whole_parent_credit": 0,
                "D02_gate_credit": 0,
                "global_unresolved_decrement": 0,
            }
            rows_to_write.append(close_row(body))
            class_census[incidence_class] += 1
    need(len(rows_to_write) == 34_734 and sum(class_census.values()) == 34_734,
         "all endpoint occurrences assigned exactly once")
    need(2 * internal_pair_root_count + cross_scope_root_count +
         source_boundary_root_count + atlas_boundary_root_count == 34_734,
         "root multiplicity/occurrence conservation")
    writer = LedgerWriter(output / ENDPOINT_LEDGER_NAME,
                          "ENDPOINT_ROOT_ID_THEN_C74_ENDPOINT_OCCURRENCE_ID")
    try:
        for row in sorted(rows_to_write, key=lambda value:
                          (value["endpoint_root_id"], value["endpoint_occurrence_id"])):
            writer.write(row)
    finally:
        writer.close()
    summary = {
        "endpoint_occurrence_count": 34_734,
        "unique_endpoint_root_count": len(by_root),
        "incidence_class_occurrence_census": dict(sorted(class_census.items())),
        "incidence_class_root_census": dict(sorted(root_class_census.items())),
        "internal_pair_root_count": internal_pair_root_count,
        "cross_scope_root_count": cross_scope_root_count,
        "source_boundary_root_count": source_boundary_root_count,
        "atlas_boundary_root_count": atlas_boundary_root_count,
        "canonical_half_open_owner_count": len(by_root),
        "dangling_duplicate_count": 0,
        "unassigned_endpoint_occurrence_count": 0,
        "cross_chart_or_source_seam_locally_reinterpreted_count": 0,
        "incidence_closed": True,
    }
    return writer.descriptor(), summary


def result_validator(value: dict[str, Any]) -> None:
    verify_object(value, "C74 result")
    need(value["status"] ==
         "PASS_42926_OF_42926_EXACT_MULTI_GRAPH_ARRANGEMENTS__ROOT_EQUALITY_EMPTY__25559_PURE_EXCLUSION__17367_CEMETERY_TANGENCY_GRAPHS__34734_ENDPOINT_OCCURRENCES_INCIDENCE_CLOSED__ZERO_CREDIT",
         "result status")
    need(value["scope"]["selected_child_count"] == 42_926 and
         value["scope"]["active_roots_per_child"] == 2 and
         value["scope"]["unresolved_discriminant_graphs_per_child"] == 1,
         "result scope")
    need(value["pair_census"] == {str(key): count for key, count in EXPECTED_PAIR_CENSUS.items()},
         "result pair census")
    need(value["root_order_census"] == EXPECTED_ORDER_CENSUS and
         value["root_equality_realizable_count"] == 0, "result root order")
    need(value["arrangement_census"] == {
        "PURE_STRICT_EXCLUSION_WITH_NONFUTURE_GRAPH": 25_559,
        "EXCLUSION_SLABS_PLUS_CEMETERY_TANGENCY_GRAPH": 17_367,
        "SEALED_CHILD_ARRANGEMENTS": 42_926,
    }, "result arrangement census")
    margin = value["physical_future_tangency_margin"]
    need(margin["terminal_graph_count"] == 17_367 and
         type(margin["maximum_dyadic_depth"]) is int and
         margin["maximum_dyadic_depth"] >= 0 and
         margin["uniform_strict_lower_bound"] ==
             "2^(-" + str(margin["maximum_dyadic_depth"]) + ")" and
         margin["all_graph_near_lower_strict_positive"] is True,
         "physical future tangency margin")
    incidence = value["endpoint_incidence_closure"]
    root_counts = incidence["incidence_class_root_census"]
    occurrence_counts = incidence["incidence_class_occurrence_census"]
    need(incidence["endpoint_occurrence_count"] == 34_734 and
         sum(occurrence_counts.values()) == 34_734 and
         sum(root_counts.values()) == incidence["unique_endpoint_root_count"] and
         2 * incidence["internal_pair_root_count"] +
             incidence["cross_scope_root_count"] +
             incidence["source_boundary_root_count"] +
             incidence["atlas_boundary_root_count"] == 34_734 and
         incidence["canonical_half_open_owner_count"] ==
             incidence["unique_endpoint_root_count"] and
         incidence["dangling_duplicate_count"] == 0 and
         incidence["unassigned_endpoint_occurrence_count"] == 0 and
         incidence["cross_chart_or_source_seam_locally_reinterpreted_count"] == 0 and
         incidence["incidence_closed"] is True and
         value["endpoint_incidence_ledger"]["row_count"] == 34_734,
         "endpoint incidence closure")
    need(value["strict_boundary"] == {
        "candidate_is_global_authority": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "global_unresolved_decrement": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }, "result credit boundary")


def coherent_attacks(base: dict[str, Any]) -> dict[str, Any]:
    attacks: dict[str, bool] = {}
    def attack(name: str, mutation: Any) -> None:
        body = copy.deepcopy(base)
        body.pop("object_sha256")
        mutation(body)
        try:
            result_validator(close_object(body))
        except Exception:
            attacks[name] = True
        else:
            attacks[name] = False
    attack("status", lambda value: value.__setitem__("status", "PASS"))
    attack("scope", lambda value: value["scope"].__setitem__("selected_child_count", 42_925))
    attack("active", lambda value: value["scope"].__setitem__("active_roots_per_child", 3))
    attack("graphs", lambda value: value["scope"].__setitem__("unresolved_discriminant_graphs_per_child", 0))
    attack("pair", lambda value: value["pair_census"].__setitem__("787", 9_979))
    for relation in EXPECTED_ORDER_CENSUS:
        attack("order_" + relation, lambda value, key=relation:
               value["root_order_census"].__setitem__(key,
                    value["root_order_census"][key] - 1))
    attack("tie", lambda value: value.__setitem__("root_equality_realizable_count", 1))
    for key in ("PURE_STRICT_EXCLUSION_WITH_NONFUTURE_GRAPH",
                "EXCLUSION_SLABS_PLUS_CEMETERY_TANGENCY_GRAPH",
                "SEALED_CHILD_ARRANGEMENTS"):
        attack("arrangement_" + key, lambda value, item=key:
               value["arrangement_census"].__setitem__(item,
                    value["arrangement_census"][item] - 1))
    for key in ("formal_credit", "whole_parent_credit", "D02_gate_credit",
                "global_unresolved_decrement"):
        attack(key, lambda value, item=key: value["strict_boundary"].__setitem__(item, 1))
    attack("authority", lambda value: value["strict_boundary"].__setitem__(
        "candidate_is_global_authority", True))
    attack("pointer", lambda value: value["strict_boundary"].__setitem__(
        "runtime_canonical_pointer_or_seal_writes", True))
    attack("future_terminal_count", lambda value:
           value["physical_future_tangency_margin"].__setitem__("terminal_graph_count", 17_366))
    attack("future_uniform_bound", lambda value:
           value["physical_future_tangency_margin"].__setitem__("uniform_strict_lower_bound", "2^(-999)"))
    attack("endpoint_occurrence_count", lambda value:
           value["endpoint_incidence_closure"].__setitem__("endpoint_occurrence_count", 34_733))
    attack("endpoint_dangling_duplicate", lambda value:
           value["endpoint_incidence_closure"].__setitem__("dangling_duplicate_count", 1))
    attack("endpoint_incidence_closed", lambda value:
           value["endpoint_incidence_closure"].__setitem__("incidence_closed", False))
    corrupted = copy.deepcopy(base); corrupted["object_sha256"] = "0" * 64
    try:
        result_validator(corrupted)
    except Exception:
        attacks["object_closure"] = True
    else:
        attacks["object_closure"] = False
    need(all(attacks.values()) and len(attacks) == 24, "24 coherent attacks")
    return {"status": "PASS_24_OF_24_COHERENT_SCOPE_ORDER_TIE_STRATA_INCIDENCE_AND_CREDIT_ATTACKS_FAIL_CLOSED",
            "attack_count": 24, "attacks": dict(sorted(attacks.items()))}


def build_oracle(output: Path) -> dict[str, Any]:
    need(output.is_dir() and not any(output.iterdir()), "empty existing output directory")
    ctx.prec = PRECISION_BITS
    ctx.threads = 1
    ctx.pretty = True
    ctx.unicode = False
    targets, c65_result, c58_result = validate_upstreams()
    wanted_c65 = {row["C65_aggregate_child_row_sha256"] for row in targets}
    c65 = {row["row_sha256"]: row for row in iter_closed_rows(
        C65, FILE_PINS["C65_LEAVES"], 358_919) if row["row_sha256"] in wanted_c65}
    need(len(c65) == len(wanted_c65), "C65 target join")
    wanted_c58 = {row["source_C58_leaf_row_sha256"] for row in c65.values()}
    c58 = {row["row_sha256"]: row for row in iter_closed_rows(
        C58, FILE_PINS["C58_LEAVES"], 5_548) if row["row_sha256"] in wanted_c58}
    need(len(c58) == len(wanted_c58), "C58 target join")

    context = c41.load_context(C40, None, formal=False)
    c41.install_complete_immutable_cache()
    c40_rows = c41.c38.read_ledger(C40, context["result"]["ledgers"]["routed_leaf_cells"])
    c40_index = {row["row_sha256"]: (index, row) for index, row in enumerate(c40_rows)}
    task_cache: dict[str, dict[str, Any]] = {}
    pair_census = Counter(); order_census = Counter(); arrangement_census = Counter()
    category_census = Counter(); chart_census = Counter(); graph_target_census = Counter()
    physical_future_depths: list[int] = []
    physical_decisions: list[dict[str, Any]] = []
    c39 = c41.c39
    writer = LedgerWriter(output / LEDGER_NAME)
    try:
        for atlas in targets:
            source = c65[atlas["C65_aggregate_child_row_sha256"]]
            c58_source = c58[source["source_C58_leaf_row_sha256"]]
            c40_hash = c58_source["C40_source_row_sha256"]
            task = task_cache.get(c40_hash)
            if task is None:
                c40_ordinal, c40_source = c40_index[c40_hash]
                task = c41.task_for_row(c40_ordinal, c40_source, context)
                task_cache[c40_hash] = task
            row = decision_row(c39, atlas, source, task)
            writer.write(row)
            pair_census[row["pair_index"]] += 1
            relation = row["root_order"]["relation"]
            order_census[relation] += 1
            category_census[row["source_structural_category"]] += 1
            graph_target_census[row["discriminant_graph"]["graph_target"]] += 1
            chart = row["outgoing_evidence"].get("strict_outgoing_chart",
                    row["outgoing_evidence"].get("chart"))
            chart_census[chart] += 1
            if row["sealed_strata"][1]["physical_future_tangency"]:
                arrangement_census["EXCLUSION_SLABS_PLUS_CEMETERY_TANGENCY_GRAPH"] += 1
                margin = row["discriminant_graph"]["physical_future_margin"]
                need(type(margin) is dict and
                     type(margin["strict_dyadic_depth"]) is int,
                     "retained physical future margin row")
                physical_future_depths.append(margin["strict_dyadic_depth"])
                physical_decisions.append(row)
            else:
                arrangement_census["PURE_STRICT_EXCLUSION_WITH_NONFUTURE_GRAPH"] += 1
            arrangement_census["SEALED_CHILD_ARRANGEMENTS"] += 1
    finally:
        writer.close()
    need(dict(pair_census) == EXPECTED_PAIR_CENSUS, "exact pair census")
    need(dict(order_census) == EXPECTED_ORDER_CENSUS, "exact root-order census")
    need(dict(arrangement_census) == {
        "PURE_STRICT_EXCLUSION_WITH_NONFUTURE_GRAPH": 25_559,
        "EXCLUSION_SLABS_PLUS_CEMETERY_TANGENCY_GRAPH": 17_367,
        "SEALED_CHILD_ARRANGEMENTS": 42_926,
    }, "exact arrangement census")
    descriptor = writer.descriptor()
    need(len(physical_future_depths) == len(physical_decisions) == 17_367,
         "exact physical future tangency census")
    endpoint_descriptor, endpoint_summary = build_endpoint_incidence(
        output, physical_decisions
    )
    uniform_future_depth = max(physical_future_depths)
    result_body = {
        "schema": SCHEMA + ".result",
        "status": "PASS_42926_OF_42926_EXACT_MULTI_GRAPH_ARRANGEMENTS__ROOT_EQUALITY_EMPTY__25559_PURE_EXCLUSION__17367_CEMETERY_TANGENCY_GRAPHS__34734_ENDPOINT_OCCURRENCES_INCIDENCE_CLOSED__ZERO_CREDIT",
        "producer_file_sha256": sha_file(SELF),
        "numeric_context": {"precision_bits": PRECISION_BITS,
                            "python_flint_version": __import__("flint").__version__,
                            "flint_version": __import__("flint").__FLINT_VERSION__,
                            "threads": 1},
        "upstream_file_sha256": dict(FILE_PINS),
        "upstream_object_sha256": {
            "C65_RESULT": c65_result["object_sha256"],
            "C58_RESULT": c58_result["object_sha256"],
            "C72_RESULT": "a6aa0cfd8e1ee1b7a02d92af066acb23abffb22b0b7276b7e233d2ff7d92f9f4",
            "C72_VERIFY": "8ae20b71916ee1f6d1d28e633b1fbc080f4cb277eed7b6bb54937f8538ae7994",
            "C72O_RESULT": "529d7081293b37111619d4dbf03c750be06da48105d46cc18e8c79eee10b48e7",
            "C72O_VERIFY": "41d383e0fc68ec7d7c4887ae6ef534b5b7bd19277837a14754e5c7ef5bf85715",
            "C73_RESULT": "4ddba93eea8b798de3dbc8a74608fc27686e46c9209784a6bccdd5df7fd1e1cc",
            "C73_VERIFY": "c6d9bc55347de05cef6dc3061a905e1052521a16bb6a6535233c9012b77ffd9d",
        },
        "scope": {"selector": "child_route_witness == " + SELECTOR,
                  "selected_child_count": 42_926, "source_count": 6_101,
                  "active_roots_per_child": 2,
                  "unresolved_discriminant_graphs_per_child": 1,
                  "C72o_scope_disjoint": True, "C73v2_scope_disjoint": True},
        "pair_census": {str(key): value for key, value in sorted(pair_census.items())},
        "source_structural_category_census": dict(sorted(category_census.items())),
        "graph_target_census": dict(sorted(graph_target_census.items())),
        "outgoing_chart_census": dict(sorted(chart_census.items())),
        "root_order_census": dict(sorted(order_census.items())),
        "root_equality_realizable_count": 0,
        "arrangement_census": dict(sorted(arrangement_census.items())),
        "physical_future_tangency_margin": {
            "terminal_graph_count": 17_367,
            "maximum_dyadic_depth": uniform_future_depth,
            "uniform_strict_lower_bound":
                "2^(-" + str(uniform_future_depth) + ")",
            "all_graph_near_lower_strict_positive": True,
        },
        "endpoint_incidence_closure": endpoint_summary,
        "analytic_closure": {
            "strict_graph_gradient_on_every_child": True,
            "four_exact_corners_nonzero_on_every_child": True,
            "two_unique_noncorners_face_endpoints_on_every_graph": True,
            "root_total_or_partial_order_strictly_separated": True,
            "exact_root_tie_stratum_empty": True,
            "physical_future_tangency_graphs_retained_as_cemetery_terminals": True,
            "physical_future_margin_strictly_positive_on_every_retained_graph": True,
            "endpoint_incidence_closed_against_complete_C72_atlas": True,
            "source_and_atlas_boundary_consumers_explicit": True,
            "cross_chart_and_source_seam_coordinates_follow_pinned_authority": True,
            "half_open_endpoint_owner_unique": True,
            "no_additional_dyadic_depth": True,
        },
        "ledger": descriptor,
        "endpoint_incidence_ledger": endpoint_descriptor,
        "strict_boundary": {"candidate_is_global_authority": False,
            "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
            "global_unresolved_decrement": 0,
            "runtime_canonical_pointer_or_seal_writes": False},
    }
    provisional = close_object(result_body)
    result_body["producer_self_test"] = coherent_attacks(provisional)
    result = close_object(result_body)
    result_validator(result)
    result_raw = canonical(result) + b"\n"
    report_raw = (
        "# C74 exact multi-graph order oracle\n\n"
        "The exact current-child witness scope contains 42,926 children. Each has two "
        "active roots and one regular discriminant graph. Exact conditional root bounds "
        "exclude all root equalities: 16,796 W-before-other, 25,559 competitor-behind, "
        "and 571 competitor-before-W. The 17,367 physical future tangency graphs are "
        "strictly future and retained as cemetery terminals with both incident exclusion "
        "slabs; their 34,734 endpoint occurrences are closed against the complete C72 atlas "
        "by internal pairs, adjacent-scope glue, or explicit source/atlas boundary consumers. "
        "The remaining "
        "25,559 arrangements are pure strict exclusions with a nonfuture graph. All face "
        "incidence, unique noncorner root definitions, and half-open owners are materialized. "
        "Credits remain zero.\n"
    ).encode("utf-8")
    publication = [LEDGER_NAME, ENDPOINT_LEDGER_NAME]
    emit_new(output / RESULT_NAME, result_raw); publication.append(RESULT_NAME)
    emit_new(output / REPORT_NAME, report_raw); publication.append(REPORT_NAME)
    manifest_raw = "".join(
        f"{sha_file(output / name)}  {name}\n" for name in sorted(publication)
    ).encode("ascii")
    emit_new(output / MANIFEST_NAME, manifest_raw); publication.append(MANIFEST_NAME)
    outer = close_object({
        "schema": SCHEMA + ".outer-publication-receipt",
        "status": "PASS_OUTER_LAST__ALL_C74_MEMBERS_TERMINAL_BYTE_REPLAYED",
        "result_object_sha256": result["object_sha256"],
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "member_file_sha256": {name: sha_file(output / name) for name in publication},
        "publication_order": publication + [OUTER_NAME],
        "outer_receipt_published_last": True,
        "formal_credit": 0, "D02_gate_credit": 0,
    })
    outer_raw = canonical(outer) + b"\n"
    emit_new(output / OUTER_NAME, outer_raw); publication.append(OUTER_NAME)
    for name in publication:
        raw = (output / name).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == sha_file(output / name) and
             (not raw or raw[-1:] == (output / name).read_bytes()[-1:]),
             "postpublication terminal replay:" + name)
    return {"status": "PASS_C74_STAGE_BUILT_AND_REPLAYED",
            "result_object_sha256": result["object_sha256"],
            "ledger_sha256": descriptor["sha256"],
            "outer_receipt_sha256": hashlib.sha256(outer_raw).hexdigest(),
            "publication_order": publication}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = build_oracle(Path(args.output).absolute())
    except Exception as error:
        print(json.dumps({"status": "REJECTED", "error": str(error)}, sort_keys=True), flush=True)
        return 1
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
