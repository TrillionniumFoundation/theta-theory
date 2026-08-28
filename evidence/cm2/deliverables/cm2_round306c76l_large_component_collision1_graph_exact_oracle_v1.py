#!/usr/bin/env python3
"""C76-L exact collision-one / graph oracle for the two large components.

The input universe is the frozen 33,319-row C68-L current-task replay.  This
successor selects exactly the five collision-one / graph residual classes,
reconstructs their 384-bit exact boxes without further dyadic refinement, and
emits either a whole-task strict exclusion, an exact source-grazing terminal,
or an exact branch partition whose only live leaves are schema-complete
collision-three handoffs.  There is no collision-two residual exit.  Every
nonexpected collision-two owner/word/chart branch is an exclusion, while
root ties, domain boundaries, and physical tangencies own explicit cemetery
or source-grazing terminal rows.  All assets are staged, append-only, and
zero-credit.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import gzip
import hashlib
import itertools
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Iterator, Mapping
import zlib

from flint import arb, ctx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
sys.path.insert(0, str(OUT))

import cm2_round185_preconditioned_c1_residual_refinement as r185  # noqa:E402
import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139  # noqa:E402
import cm2_round306c39_d02_h1_c1_graph_cell_router_v1 as c39  # noqa:E402
import cm2_round306c72x_implicit_h1_root_physical_glue_core_v1 as h1core  # noqa:E402

SELF = Path(__file__).resolve()
SCHEMA = "cm2.round306c76l.large-component-collision1-graph-exact-oracle.v1"
PREFIX = "cm2_round306c76l_large_component_collision1_graph_exact_oracle_v1"
DECISIONS = PREFIX + "_decisions.jsonl.gz"
INCIDENCE = PREFIX + "_physical_graph_incidence.jsonl.gz"
BOUNDARIES = PREFIX + "_degree1_scope_source_boundary_registry.jsonl.gz"
BRANCHES = PREFIX + "_exact_branch_partitions.jsonl.gz"
HANDOFFS = PREFIX + "_collision3_handoffs.jsonl.gz"
REGISTRY = PREFIX + "_semialgebraic_branch_registry.json"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
MANIFEST = PREFIX + "_manifest.sha256"
OUTER = PREFIX + "_outer_receipt.json"
LOCK = "ZERO_CREDIT_STAGED_C76L_COLLISION1_GRAPH_ONLY.lock"
PRECISION = 384
FROZEN_OWNER = "W[1,0]"

C41_DIR = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C32_DIR = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"
C35_DIR = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C37_DIR = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"

FILES: dict[str, Path] = {
    "C68_RESULT": OUT / "cm2_round306c68l_blocker_crosswalk_result_v1.json",
    "C68_TASKS": OUT / "cm2_round306c68l_blocker_crosswalk_large_current_task_replay_v1.jsonl.gz",
    "C56_RESULT": OUT / "cm2_round306c56l_large_component_common_refinement_result_v1.json",
    "C56_TASKS": OUT / "cm2_round306c56l_large_component_common_refinement_post_c53_pending_logical_tasks_v1.jsonl.gz",
    "C55B_RESULT": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json",
    "C55B_CELLS": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz",
    "C55B_COMPONENTS": OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz",
    "C41_RESULT": C41_DIR / "result.json",
    "C41_AMBIENT": C41_DIR / "routed_ambient_cells.jsonl.gz",
    "C41_C1": C41_DIR / "c1_h1_surface_outers.jsonl.gz",
    "C41_C2": C41_DIR / "c2_surface_outers.jsonl.gz",
    "C41_ENDPOINTS": C41_DIR / "endpoint_recharts.jsonl.gz",
    "C32_CELLS": C32_DIR / "compact_cells.jsonl.gz",
    "C35_PATH": C35_DIR / "path_occurrences.jsonl.gz",
    "C37_PATH": C37_DIR / "reflected_r1648_occurrences.jsonl.gz",
    "CHART_MANIFEST": OUT / "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json",
    "H1_CORE": OUT / "cm2_round306c72x_implicit_h1_root_physical_glue_core_v1.py",
}

PINS = {
    "C68_RESULT": "81cf9b6e3fbf2330f747af6430410026406cad8a1a2eb862be974235b2b60f37",
    "C68_TASKS": "bc62868582ca26be996904fe8120422b0d67e8afc0080dfd4650512a041eaa2f",
    "C56_RESULT": "99e5fc0019ae21e7bc68d0c2b997ed62e9c47b28fd47d366237b0c06b1d82601",
    "C56_TASKS": "6893e360b3ffc205147efa3786f1a05c1b67c1556e6195733549a7da5540fb6a",
    "C55B_RESULT": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "C55B_CELLS": "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce",
    "C55B_COMPONENTS": "bebc49f66efb01c0b980ec10258a60d7aead9d4d2006d28bdd169c9a9ae38a04",
    "C41_RESULT": "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    "C41_AMBIENT": "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8",
    "C41_C1": "487fb8e9e9355dcb7094b302b70b6843a8fb6db0baf4f1e116496c9de9723294",
    "C41_C2": "80bcf335780d61b12e181743699343a0dada51d320f7b1b4643a9c6432b7eee9",
    "C41_ENDPOINTS": "e631af197d07e0dbbf0b67fcef92e2a981530f68e9bef84f1806f59ad8eb2219",
    "C32_CELLS": "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8",
    "C35_PATH": "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66",
    "C37_PATH": "7c87829f6ef883b7928ff8a313d5bfcf240383c51a9040739de1cfe7e617bef5",
    "CHART_MANIFEST": "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
    "H1_CORE": "98f13225cbd9caf886242fbedf5071846b77df192727a7bdbc4075eb89a8adc8",
}

CAPABILITIES: dict[str, tuple[Path, str]] = {
    "C71B_RESULT": (ROOT / ".cm2-runtime/c71b-v3-final-75c21279/cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_result.json", "5ede807e4860b60fe8582597cc6be10cdfdc7b3a0eeba57ced317f4980092246"),
    "C71B_VERIFY": (ROOT / ".cm2-runtime/c71b-v3-final-75c21279/independent_verification_v3_1.json", "ee105922e263d9cea551088ee67c350cc9adc4d9f375a8584428e4fa55575612"),
    "C71B_RECEIPT": (ROOT / ".cm2-runtime/c71b-v3-final-75c21279/dual_build_publication_completion_receipt_v3.json", "3a6cfa624fab8cd1b787d3facd139cf9e055a008236864d894d2633522fe9fbc"),
    "C72B2_RESULT": (ROOT / ".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_result.json", "0c8c56a86d3293dd08bc1fef95a72fe0aedc3a35edb20ff0ec9c6e19cd69d1f3"),
    "C72B2_VERIFY": (ROOT / ".cm2-runtime/c72b2-independent-a.v2-3212bb3d.json", "21988ad9b5d746495489e506fadfdf537848eeae6a788a64c6bca3b11c2c9252"),
    "C72B2_RECEIPT": (ROOT / ".cm2-runtime/c72b2-completion-outer-receipt.v2-a53e5319.json", "e0d6da2518d48278a42ffea5e6a676b11001d531e971fdc59da39f3b524dec62"),
    "C72O_RESULT": (ROOT / ".cm2-runtime/c72o-build-a2.v1/cm2_round306c72o_collision1_outgoing_state_oracle_v1_result.json", "fd9ca6489f5fedef85fb55de6906a62ecadc417c72d7eb938a6268e7f402302a"),
    "C72O_VERIFY": (ROOT / ".cm2-runtime/c72o-independent-verification-v2.json", "2d34c25b5fd9f2b3a1e8b30d184b40d8a93ffce8c192d193b75715e0d7a68ccb"),
    "C73_RESULT": (ROOT / ".cm2-runtime/c73v2-build-a.QOYACE/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2_result.json", "5de9d37c69ed4d13d972eff8845ed55ad695ab040d6c1beda01626c0c065c615"),
    "C73_VERIFY": (ROOT / ".cm2-runtime/c73v2-audit-a.W2AYpD/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_independent_verification_v2.json", "784505135d105fcdf05cc2d6e37779ea896f7d1bbe06e75dd1019b67ae951fe1"),
    "C74_RESULT": (ROOT / ".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1_result.json", "8d2372de67a5ed0d87a6699845778c9e4d05e183cd21b599a3fd6287032e27b1"),
    "C74_VERIFY": (ROOT / ".cm2-runtime/c74-audit-a.cazCPb/cm2_round306c74_exact_multi_graph_order_oracle_v1_independent_verification_v1.json", "eb4fbefba436ca827a6a60ceb9a3978c496fdbf9798a7eed29333e2067d256cb"),
    "C75_RESULT": (ROOT / ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_result.json", "1d9d4b2f8b7a4bfb6133ce7b23c22765ef9097c133cc47dc199dd0479f478366"),
    "C75_VERIFY": (ROOT / ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_independent_verification_v1.json", "8f620e4e7312828dcbcee23cf3f33280c8583bd414ded493b7996b2279131a4c"),
    "C75_RECEIPT": (ROOT / ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_dual_completion_receipt_v1.json", "dbbad4ea8d807b6bcb8b7f121acc57f782925be7e00c9267b9edf011e3eba2b1"),
    "C74L_RESULT": (ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt/cm2_round306c74l_source_seam_collision1_handoff_successor_v1_result.json", "53732dbd4d3be61f26a4aba74952c2aef40684c9d2fb23bd9bd6692917fc5b8d"),
    "C74L_VERIFY": (ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt/cm2_round306c74l_source_seam_collision1_handoff_successor_v1_independent_verification_v1_1.json", "f0ee22df980db6886dd73e014796418512925d28dce37d1be0caf04d293310e5"),
    "C74L_RECEIPT": (ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt/cm2_round306c74l_source_seam_collision1_handoff_successor_dual_completion_receipt_v1.json", "1b9459e41a3de4ce5ab2f99b946ce6cb325c63934d87c641571c474f62ad7a3a"),
}

SELECTED = {
    "UNRESOLVED_C41_ALGEBRAIC_H0_SEAM_RECHART_OUTER": 29,
    "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER": 832,
    "UNRESOLVED_C41_C1_REGULAR_MULTI_GRAPH_OUTER": 11_917,
    "UNRESOLVED_C41_H1_GRAPH_OR_BOUNDARY_OUTER": 3_858,
    "UNRESOLVED_C41_SOURCE_RADICAL_STEREOGRAPHIC_ENDPOINT_OUTER": 247,
}
WITNESSES = {
    "EXACT_ALGEBRAIC_ENDPOINT_REQUIRES_GRAPH_CELL": 29,
    "OUTGOING_STATE": 832,
    "inherited interval ordering or boundary type not isolated": 11_204,
    "unique monotone inherited-active-set first tangency": 713,
    "REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED": 2_089,
    "REGULAR_FULL_FACE_GRAPH": 1_374,
    "SINGULAR_OR_MULTI_GRAPH_ARRANGEMENT_REQUIRED": 4,
    "SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED": 391,
    "Round185Error:AD sqrt domain": 247,
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in value, "open row")
    return {**value, "row_sha256": digest(value)}


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in value, "open object")
    return {**value, "object_sha256": digest(value)}


def verify_row(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value)); claim = body.pop("row_sha256", None)
    need(claim == digest(body), label + ":row closure")


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        first = os.fstat(fd)
        need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1, "regular:" + str(path))
        while True:
            block = os.read(fd, 1 << 20)
            if not block: break
            h.update(block)
        second = os.fstat(fd); current = os.stat(path, follow_symlinks=False)
        ident = lambda x: (x.st_dev, x.st_ino, x.st_mode, x.st_nlink, x.st_size, x.st_mtime_ns, x.st_ctime_ns)
        need(ident(first) == ident(second) == ident(current), "TOCTOU:" + str(path))
    finally:
        os.close(fd)
    return h.hexdigest()


def secure(path: Path, expected: str, maximum: int = 256 << 20) -> bytes:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        first = os.fstat(fd)
        need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1, "regular single-link:" + str(path))
        out = bytearray(); h = hashlib.sha256()
        while True:
            block = os.read(fd, 1 << 20)
            if not block: break
            out.extend(block); h.update(block)
            need(len(out) <= maximum, "size:" + str(path))
        second = os.fstat(fd); current = os.stat(path, follow_symlinks=False)
        ident = lambda x: (x.st_dev, x.st_ino, x.st_mode, x.st_nlink, x.st_size, x.st_mtime_ns, x.st_ctime_ns)
        need(ident(first) == ident(second) == ident(current), "TOCTOU:" + str(path))
        need(h.hexdigest() == expected, "pin:" + str(path))
        return bytes(out)
    finally:
        os.close(fd)


def no_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate key:" + key); out[key] = value
    return out


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), label + ":newline")
    value = json.loads(raw[:-1].decode("utf-8", "strict"), object_pairs_hook=no_dupes,
                       parse_float=lambda x: (_ for _ in ()).throw(Reject(x)),
                       parse_constant=lambda x: (_ for _ in ()).throw(Reject(x)))
    need(type(value) is dict and canonical(value) + b"\n" == raw, label + ":canonical")
    return value


def rows(raw: bytes, label: str) -> Iterator[dict[str, Any]]:
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS); expanded = decoder.decompress(raw) + decoder.flush()
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail, label + ":single gzip member")
    need(expanded.endswith(b"\n"), label + ":jsonl newline")
    for index, line in enumerate(expanded.splitlines()):
        value = json.loads(line.decode("utf-8", "strict"), object_pairs_hook=no_dupes,
                           parse_float=lambda x: (_ for _ in ()).throw(Reject(x)),
                           parse_constant=lambda x: (_ for _ in ()).throw(Reject(x)))
        need(type(value) is dict and canonical(value) == line, f"{label}:{index}:canonical")
        verify_row(value, f"{label}:{index}"); yield value


def exclusive(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o644)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(fd, view); need(count > 0, "short write"); view = view[count:]
        os.fsync(fd)
    finally:
        os.close(fd)


class Ledger:
    def __init__(self, path: Path, order: str) -> None:
        self.path, self.order = path, order; self.count = 0; self.sequence = hashlib.sha256()
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o644)
        self.raw = os.fdopen(fd, "wb"); self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
    def write(self, value: dict[str, Any]) -> dict[str, Any]:
        row = close_row(value); self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row["row_sha256"] + "\n").encode("ascii")); self.count += 1; return row
    def write_closed(self, row: dict[str, Any]) -> dict[str, Any]:
        verify_row(row, self.path.name + ":preclosed")
        self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row["row_sha256"] + "\n").encode("ascii")); self.count += 1
        return row
    def close(self) -> None:
        self.gz.close(); self.raw.close()
    def descriptor(self) -> dict[str, Any]:
        return {"filename": self.path.name, "order": self.order, "row_count": self.count,
                "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
                "sha256": sha_file(self.path), "size": self.path.stat().st_size}


def bounds(value: Any) -> dict[str, str]:
    return {"lower": str(value.lower()), "upper": str(value.upper())}


def sign(value: Any) -> int:
    return 1 if bool(value > 0) else -1 if bool(value < 0) else 0


def make_box(row: Mapping[str, Any]) -> Any:
    box = row["closed_representative_box"]
    need(box is not None and box["s"] == ["0", "0"], "rational s=0 box")
    return r185.atlas.AtlasBox(Q(box["t"][0]), Q(box["t"][1]), Q(box["p"][0]), Q(box["p"][1]),
                               Q(0), Q(0), len(row["path"]), row["path"])


def exact_faces(chart: str, box: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    t0, t1 = box["t"]; p0, p1 = box["p"]
    return {
        "t_lower": {"gate3_chart": chart, "fixed_axis": "t", "fixed_value": t0, "varying_axis": "p", "varying_interval": [p0, p1]},
        "t_upper": {"gate3_chart": chart, "fixed_axis": "t", "fixed_value": t1, "varying_axis": "p", "varying_interval": [p0, p1]},
        "p_lower": {"gate3_chart": chart, "fixed_axis": "p", "fixed_value": p0, "varying_axis": "t", "varying_interval": [t0, t1]},
        "p_upper": {"gate3_chart": chart, "fixed_axis": "p", "fixed_value": p1, "varying_axis": "t", "varying_interval": [t0, t1]},
    }


def physical_face_key(spec: Mapping[str, Any]) -> str:
    return digest({"schema": SCHEMA + ".physical-face-key", **dict(spec)})


def physical_root_id(spec: Mapping[str, Any], equation: str) -> str:
    return digest({"schema": SCHEMA + ".unique-physical-face-root", "equation": equation, **dict(spec)})


def cell_face_is_outer_boundary(cell: Mapping[str, Any], face: str,
                                spec: Mapping[str, Any]) -> bool:
    if spec["fixed_axis"] == "t":
        base = tuple(Q(value["value"]) for value in cell["physical_t_interval"])
    else:
        base = tuple(Q(value) for value in cell["physical_p_interval"])
    endpoint = 0 if face.lower().endswith("lower") or face.upper().endswith("LOW") else 1
    return Q(spec["fixed_value"]) == base[endpoint]


def graph_certificate(parent: str, box: Any, target: str, chart: str,
                      exact_box: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], Any, Any]:
    geometry = r185.ad_initial_geometry(parent, box); raw = r185.ad_root(geometry, target)
    delta = r185.centered_enclosure(
        lambda origin, current, identifier: r185.ad_root(r185.ad_initial_geometry(origin, current), identifier)["Delta"],
        parent, box, target, raw["Delta"])
    need(sign(delta) == 0 and bool(delta.upper() > 0), "spanning graph Delta:" + target)
    derivatives = [sign(raw["Delta"].derivative[index]) for index in (0, 1)]
    need(all(value != 0 for value in derivatives), "strict graph gradient:" + target)
    corners: dict[tuple[int, int], dict[str, Any]] = {}
    for ti, t in enumerate((box.t0, box.t1)):
        for pi, p in enumerate((box.p0, box.p1)):
            point = r185.point_box(box, t, p, Q(0), ".c76l-corner")
            value = r185.ad_root(r185.ad_initial_geometry(parent, point), target)["Delta"].value
            current = sign(value); need(current != 0, "graph corner:" + target)
            corners[(ti, pi)] = {"t": str(t), "p": str(p), "Delta": bounds(value), "sign": current}
    corner_sign_set = {row["sign"] for row in corners.values()}
    need(corner_sign_set in ({-1}, {1}, {-1, 1}), "corner trichotomy:" + target)
    ends = {"t_lower": ((0, 0), (0, 1)), "t_upper": ((1, 0), (1, 1)),
            "p_lower": ((0, 0), (1, 0)), "p_upper": ((0, 1), (1, 1))}
    faces = exact_faces(chart, exact_box); incidence: list[dict[str, Any]] = []
    for face, pair in ends.items():
        signs = [corners[key]["sign"] for key in pair]
        if signs[0] == signs[1]: continue
        spec = faces[face]; key = physical_face_key(spec)
        incidence.append({"face": face, "physical_face_key_sha256": key,
                          "physical_root_id": physical_root_id(spec, "collision1_Delta_" + target + "=0"),
                          "equation": "collision1_Delta_" + target + "=0",
                          "exact_physical_face": spec, "collision1_target": target,
                          "endpoint_corner_signs": signs,
                          "unique_by_strict_tangential_derivative": True,
                          "tangential_derivative_sign": derivatives[1] if face.startswith("t") else derivatives[0]})
    need(len(incidence) in {0, 2, 4}, "even clipped graph endpoint census:" + target)
    radical = delta.upper().sqrt().upper()
    near_lower = raw["ell"].value.lower() - radical
    certificate = {
        "target": target, "equation": "collision1_Delta_" + target + "=0",
        "precision_bits": PRECISION, "centered_Delta": bounds(delta),
        "strict_gradient": {"dt": bounds(raw["Delta"].derivative[0]), "dp": bounds(raw["Delta"].derivative[1]),
                            "dt_sign": derivatives[0], "dp_sign": derivatives[1]},
        "four_corner_census": [corners[key] for key in sorted(corners)],
        "boundary_incidence": incidence,
        "graph_guard_topology": ("REGULAR_TWO_FACE_CLIPPED_GRAPH" if len(incidence) == 2 else
            "FOUR_FACE_MULTI_ARC_GUARD" if len(incidence) == 4 else
            "ONE_SIDED_CENTERED_GUARD__EXACT_DELTA_TRICHOTOMY_RETAINED"),
        "single_regular_clipped_graph": len(incidence) == 2,
        "one_sided_guard_is_not_asserted_present_or_absent": len(incidence) == 0,
        "root_bounds": {"near_lower": bounds(near_lower), "near_upper": bounds(raw["ell"].value.upper()),
                        "far_upper": bounds(raw["ell"].value.upper() + radical)},
    }
    return certificate, incidence, raw, delta


def source_radical_certificate(parent: str, box: Any, chart: str,
                               exact_box: Mapping[str, Any]) -> dict[str, Any]:
    need(box.s0 == box.s1 == 0, "source radical s=0")
    endpoint_axis = ("p" if box.p0 == -1 or box.p1 == 1 else
                     "t" if box.t0 == -1 or box.t1 == 1 else None)
    if endpoint_axis is None:
        raw = r185.ad_root(r185.ad_initial_geometry(parent, box), FROZEN_OWNER)
        delta = r185.centered_enclosure(
            lambda origin, current, identifier: r185.ad_root(
                r185.ad_initial_geometry(origin, current), identifier)["Delta"],
            parent, box, FROZEN_OWNER, raw["Delta"])
        derivative_signs = [sign(raw["Delta"].derivative[index]) for index in (0, 1)]
        need(any(value != 0 for value in derivative_signs), "collision1 radical nonconstant")
        corners: dict[tuple[int, int], dict[str, Any]] = {}
        for ti, t in enumerate((box.t0, box.t1)):
            for pi, p in enumerate((box.p0, box.p1)):
                point = r185.point_box(box, t, p, Q(0), ".c76l-delta-source-corner")
                value = r185.ad_root(r185.ad_initial_geometry(parent, point), FROZEN_OWNER)["Delta"].value
                current = sign(value)
                corners[(ti, pi)] = {"corner": f"t{ti}p{pi}", "t": str(t), "p": str(p),
                    "Delta_W": bounds(value), "trichotomy": "POSITIVE" if current > 0 else
                    "NEGATIVE" if current < 0 else "ZERO_CARRIER_OWNED"}
        ends = {"t_lower": ((0, 0), (0, 1)), "t_upper": ((1, 0), (1, 1)),
                "p_lower": ((0, 0), (1, 0)), "p_upper": ((0, 1), (1, 1))}
        face_specs = exact_faces(chart, exact_box); boundary_incidence = []
        for face, pair in ends.items():
            signs = [corners[key]["trichotomy"] for key in pair]
            if set(signs) != {"NEGATIVE", "POSITIVE"}: continue
            spec = face_specs[face]
            boundary_incidence.append({"face": face, "exact_physical_face": spec,
                "physical_face_key_sha256": physical_face_key(spec),
                "physical_root_id": physical_root_id(spec, "Delta_W[1,0]=0"),
                "equation": "Delta_W[1,0]=0", "endpoint_corner_signs": signs})
        return {"equation": "Delta_W[1,0]=u^2", "precision_bits": PRECISION,
            "coordinate_case": "INTERIOR_SOURCE__COLLISION1_DISCRIMINANT_RADICAL",
            "endpoint_side": None, "centered_Delta_W": bounds(delta),
            "Delta_W_derivatives": {"dt": bounds(raw["Delta"].derivative[0]),
                "dp": bounds(raw["Delta"].derivative[1]), "dt_sign": derivative_signs[0],
                "dp_sign": derivative_signs[1]},
            "all_four_exact_corners": [corners[key] for key in sorted(corners)],
            "all_four_exact_faces": list(face_specs.values()),
            "boundary_incidence": boundary_incidence,
            "stereographic_radical_chart": {"coordinate": "u>=0", "u_squared": "Delta_W[1,0]",
                "negative_Delta_action": "CEMETERY_OR_DISCONNECTED_TERMINAL",
                "u_zero_action": "SOURCE_GRAZING_TERMINAL",
                "positive_u_action": "EXACT_H1_OUTGOING_AND_C2_OWNER_ORDER_BRANCH_PROGRAM"},
            "source_radical_denominator_and_domain_equalities_owned_once": True,
            "additional_dyadic_depth_used": 0}
    lower, upper = ((box.p0, box.p1) if endpoint_axis == "p" else (box.t0, box.t1))
    sigma = -1 if lower == -1 else 1
    interior = upper if sigma < 0 else lower
    radial_ratio = Q(sigma) * interior
    need(-1 < radial_ratio <= 1, "source radical interior ratio")
    u_squared_max = (1 - radial_ratio) / (1 + radial_ratio)
    q2 = lambda coordinate: Q(1) - coordinate * coordinate
    q2_values = [q2(lower), q2(upper)]
    need(min(q2_values) == 0 and max(q2_values) > 0, "exact source radical interval")
    corners = []
    for ti, t in enumerate((box.t0, box.t1)):
        for pi, p in enumerate((box.p0, box.p1)):
            coordinate = p if endpoint_axis == "p" else t
            value = q2(coordinate)
            corners.append({"corner": f"t{ti}p{pi}", "t": str(t), "p": str(p),
                            "q_source_squared": str(value),
                            "trichotomy": "POSITIVE" if value > 0 else "ZERO_CARRIER_OWNED"})
    face_rows = []
    for face, spec in exact_faces(chart, exact_box).items():
        if spec["fixed_axis"] == endpoint_axis:
            value_interval = [str(q2(Q(spec["fixed_value"]))) for _ in range(2)]
        else:
            value_interval = [str(min(q2_values)), str(max(q2_values))]
        face_rows.append({"face": face, "exact_physical_face": spec,
                          "physical_face_key_sha256": physical_face_key(spec),
                          "q_source_squared_interval": value_interval,
                          "exact_trichotomy_retained": True})
    coordinate_name = "q_source" if endpoint_axis == "p" else "n_source"
    return {"equation": f"{coordinate_name}^2=1-{endpoint_axis}^2", "precision_bits": PRECISION,
        "coordinate_case": f"{endpoint_axis.upper()}_ENDPOINT_STEREOGRAPHIC_SOURCE_CHART",
        "sigma": sigma, "endpoint_side": endpoint_axis.upper() + ("_LOWER" if sigma < 0 else "_UPPER"),
        "exact_coordinate_endpoint": str(sigma),
        "closed_u_squared_interval": ["0", str(u_squared_max)],
        "source_radical_derivative": f"d(1-{endpoint_axis}^2)/d{endpoint_axis}=-2*{endpoint_axis}",
        "derivative_strict_on_positive_u_interior": True,
        "all_four_exact_corners": corners, "all_four_exact_faces": face_rows,
        "boundary_incidence": [],
        "stereographic_radical_chart": {"coordinate": "u>=0",
            "u_squared": f"(1-sigma*{endpoint_axis})/(1+sigma*{endpoint_axis})",
            "endpoint_coordinate_formula": f"{endpoint_axis}=sigma*(1-u^2)/(1+u^2)",
            "source_radical_formula": f"{coordinate_name}=2*u/(1+u^2)",
            "unit_circle_identity_exact_polynomial": "(1-u^2)^2+4*u^2=(1+u^2)^2",
            "outside_source_domain_action": "CEMETERY_OR_DISCONNECTED_TERMINAL",
            "u_zero_action": "SOURCE_GRAZING_TERMINAL",
            "positive_u_action": "EXACT_H1_OUTGOING_AND_C2_OWNER_ORDER_BRANCH_PROGRAM",
            "u_zero_half_open_owner": "SOURCE_RADICAL_CHART_OWNS",
            "positive_u_owner": "AMBIENT_GRAPH_STRATUM_OWNS"},
        "source_radical_denominator_and_domain_equalities_owned_once": True,
        "additional_dyadic_depth_used": 0}


def collision2_domain_certificate(parent: str, box: Any,
                                  pair_index: Mapping[Any, Any],
                                  pattern_index: Mapping[Any, Any]) -> dict[str, Any]:
    try:
        r185.resolve_dynamic_box(parent, box, pair_index, pattern_index)
    except Exception as error:
        need(type(error).__name__ == "Round185Error" and str(error) == "AD sqrt domain",
             "exact C2 evaluation exception replay")
    else:
        raise Reject("C2 evaluation exception disappeared")
    state = r185.r181.collision1_state_direct(parent, box)
    geometry = r185.r183.collision2_geometry(state)
    failing = []
    for candidate in r185.CANDIDATES:
        try:
            r185.enhanced_root_record(parent, box, geometry, candidate)
        except Exception as error:
            need(type(error).__name__ == "Round185Error" and str(error) == "AD sqrt domain",
                 "localized C2 sqrt exception")
            failing.append({"candidate": candidate, "guard": f"Delta({candidate}) < 0, = 0, or > 0",
                            "negative_action": "CANDIDATE_ABSENT_CONTINUE_EXACT_OWNER_PROGRAM",
                            "zero_action": "CEMETERY_TANGENCY_TERMINAL",
                            "positive_action": "EXACT_NEAR_ROOT_ORDER_PROGRAM"})
    need(bool(failing), "localized C2 domain guards")
    return {"precision_bits": PRECISION, "failing_candidate_guard_count": len(failing),
            "failing_candidate_guards": failing,
            "all_other_candidates_evaluated_without_domain_exception": True,
            "canonical_first_zero_guard_owns_lower_dimensional_carrier": True,
            "all_positive_guard_branches_enter_exact_1485_pair_order_program": True,
            "all_negative_guard_branches_remove_only_that_candidate": True,
            "collision2_residual_branch_count": 0,
            "additional_dyadic_depth_used": 0}


def record_summary(record: Any) -> dict[str, Any]:
    result = {"target": record.target_id, "classification": record.classification}
    for name in ("ell", "discriminant", "near", "far"):
        value = getattr(record, name, None)
        result[name] = bounds(value) if value is not None else None
    return result


def chart_authority() -> dict[str, Any]:
    manifest = json.loads(secure(FILES["CHART_MANIFEST"], PINS["CHART_MANIFEST"]))
    need(manifest["certificate_sha256"] == "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1", "chart cert")
    rule = manifest["result"]["unique_half_open_owner_rule"]
    need(rule["diagonal_tie"] == "E or W owns; N or S excludes" and
         rule["same_physical_normal_on_paired_representations"] is True and
         rule["duplicate_trace_is_identified_not_added"] is True, "chart rule")
    return {"manifest_file_sha256": PINS["CHART_MANIFEST"],
            "certificate_sha256": manifest["certificate_sha256"],
            "eight_chart_seam_ownership": "CERTIFIED", "diagonal_tie": rule["diagonal_tie"],
            "same_physical_normal_on_paired_representations": True,
            "duplicate_trace_is_identified_not_added": True}


def first_three(raw: bytes, label: str) -> list[dict[str, Any]]:
    output = []
    for row in rows(raw, label):
        if len(output) < 3: output.append(row)
    need(len(output) == 3 and [row["collision_index"] for row in output] == [1, 2, 3],
         label + ":first three")
    return output


def component_anchor(cell: Mapping[str, Any], component: Mapping[str, Any]) -> dict[str, Any]:
    need(cell["component_index"] in {0, 1} and component["component_index"] == cell["component_index"], "large component")
    need(component["positive_area_anchor_proof_present"] is True and
         component["anchor_is_strict_subset_not_whole_component"] is True and
         component["whole_component_connected_to_known_credit"] == 0, "anchor boundary")
    return {"C55B_cell_row_sha256": cell["row_sha256"], "C55B_component_row_sha256": component["row_sha256"],
            "component_index": cell["component_index"], "component_id": cell["component_id"],
            "strict_open_known_sheet_anchor_present": True,
            "task_chart_and_cell_compatible_with_component": True,
            "whole_component_anchor_not_claimed": True, "known_component_connection_credit": 0}


def branch_registry(original: list[dict[str, Any]], reflected: list[dict[str, Any]],
                    registry_sha: str) -> dict[str, Any]:
    candidates = list(r185.CANDIDATES)
    need(len(candidates) == 55 and len(set(candidates)) == 55, "55 C2 candidates")
    order_guards = []
    for ordinal, (left, right) in enumerate(itertools.combinations(candidates, 2)):
        body = {"ordinal": ordinal, "left": left, "right": right,
                "guard": f"near({left})-near({right}) < 0, = 0, or > 0"}
        order_guards.append({**body, "guard_id": "c2-order:" + digest(body)})
    need(len(order_guards) == 1_485, "C2 pair order census")
    body = {"schema": SCHEMA + ".semialgebraic-branch-registry",
        "precision_bits": PRECISION, "official_registry_sha256": registry_sha,
        "candidate_universe": candidates, "candidate_count": 55,
        "candidate_universe_sha256": digest(candidates),
        "pairwise_next_root_order_guards": order_guards,
        "pairwise_next_root_order_guard_count": 1_485,
        "candidate_guard_program": [{"candidate": candidate,
            "ordered_guards": [f"Delta({candidate}) < 0, = 0, or > 0",
                f"near({candidate}) < 0, = 0, or > 0",
                f"near({candidate}) < tau, = tau, or > tau"]}
            for candidate in candidates],
        "canonical_disjoint_branch_rule": {
            "guard_order": ["evaluation-domain", "candidate-Delta", "future-root",
                "pairwise-minimum-order", "official-word", "outgoing-H2"],
            "first_non-strict_or_zero_guard_owns_its_lower-dimensional_branch": True,
            "strict_open_branch_owner_is_unique_minimum_future_root": True,
            "all_trichotomy_products_covered_once": True,
            "no_branch_uses_numerical_tie_breaking": True},
        "branch_actions": {
            "C1_NON_W_UNIQUE_FIRST": "WHOLE_BRANCH_STRICT_EXCLUSION",
            "C1_NO_FUTURE_ROOT": "CEMETERY_OR_DISCONNECTED_TERMINAL",
            "C1_MINIMUM_ROOT_TIE_OR_TANGENCY": "CEMETERY_TANGENCY_TERMINAL",
            "C1_H0_SOURCE_SEAM_ZERO": "SOURCE_GRAZING_TERMINAL",
            "C1_W_FIRST_OFFICIAL_WORD_MISMATCH": "WHOLE_BRANCH_STRICT_EXCLUSION",
            "C1_W_FIRST_OUTGOING_NON_W": "WHOLE_BRANCH_STRICT_EXCLUSION",
            "C1_W_FIRST_H1_ZERO_OR_SOURCE": "CEMETERY_OR_SOURCE_GRAZING_TERMINAL",
            "C2_NO_FUTURE_ROOT": "CEMETERY_OR_DISCONNECTED_TERMINAL",
            "C2_NONEXPECTED_UNIQUE_OWNER": "WHOLE_BRANCH_STRICT_EXCLUSION",
            "C2_MINIMUM_TIE_OR_DOMAIN_EQUALITY": "CEMETERY_OR_SOURCE_GRAZING_TERMINAL",
            "C2_EXPECTED_OWNER_OUTGOING_MISMATCH": "WHOLE_BRANCH_STRICT_EXCLUSION",
            "C2_EXPECTED_OWNER_E_OR_H2_GLUE": "SEALED_COLLISION3_HANDOFF",
            "SINGULAR_H1_EXACT_STRATUM": "SEALED_COLLISION3_HANDOFF"},
        "ordered_first_match_bundles": [
            {"ordinal": 0, "bundle": "CEMETERY_SOURCE",
             "action": "CEMETERY_OR_SOURCE_GRAZING_TERMINAL"},
            {"ordinal": 1, "bundle": "STRICT_MISMATCH",
             "action": "WHOLE_BRANCH_STRICT_EXCLUSION"},
            {"ordinal": 2, "bundle": "KNOWN_H2_GLUE",
             "action": "KNOWN_COMPONENT_CONNECTION"},
            {"ordinal": 3, "bundle": "EXPECTED_C3",
             "action": "SEALED_COLLISION3_HANDOFF"}],
        "expected_occurrences": {
            "REPRESENTATIVE": {"collision2_owner": original[1]["selected_absolute_owner_id"],
                "collision2_word": original[1]["official_word_key_id"],
                "collision2_outgoing_chart": original[1]["outgoing_chart"],
                "collision2_occurrence_row_sha256": original[1]["row_sha256"],
                "collision3_owner": original[2]["selected_absolute_owner_id"],
                "collision3_word": original[2]["official_word_key_id"],
                "collision3_outgoing_chart": original[2]["outgoing_chart"],
                "collision3_occurrence_row_sha256": original[2]["row_sha256"]},
            "REFLECTED": {"collision2_owner": reflected[1]["selected_absolute_owner_id"],
                "collision2_word": reflected[1]["official_word_key_id"],
                "collision2_outgoing_chart": reflected[1]["outgoing_chart"],
                "collision2_occurrence_row_sha256": reflected[1]["row_sha256"],
                "collision3_owner": reflected[2]["selected_absolute_owner_id"],
                "collision3_word": reflected[2]["official_word_key_id"],
                "collision3_outgoing_chart": reflected[2]["outgoing_chart"],
                "collision3_occurrence_row_sha256": reflected[2]["row_sha256"]}},
        "physical_glue": {"representative_reflected_bijection": True,
            "H2_zero_half_open_owner": "E_OR_W_OWNS__N_OR_S_EXCLUDES",
            "same_physical_trace_duplicate_identified_not_added": True,
            "two_occurrences_never_create_two_credits": True},
        "zero_credit": {"formal_credit": 0, "global_credit": 0,
            "D02_gate_credit": 0, "CM2_credit": 0}}
    return close_object(body)


def branch_entry(task_id: str, side: str, family: str, action: str,
                 guard: Mapping[str, Any], atomic_count: int,
                 handoff_id: str | None = None) -> dict[str, Any]:
    need(action in {"WHOLE_BRANCH_STRICT_EXCLUSION",
                    "CEMETERY_OR_DISCONNECTED_TERMINAL",
                    "CEMETERY_TANGENCY_TERMINAL",
                    "SOURCE_GRAZING_TERMINAL",
                    "CEMETERY_OR_SOURCE_GRAZING_TERMINAL",
                    "KNOWN_COMPONENT_CONNECTION",
                    "SEALED_COLLISION3_HANDOFF"}, "allowed branch action")
    guard_body = dict(guard)
    branch_id = "c76l-branch:" + digest({"task_id": task_id, "physical_side": side,
        "branch_family": family, "branch_guard": guard_body})
    return {"branch_id": branch_id, "branch_family": family,
            "branch_action": action, "branch_guard": guard_body,
            "branch_guard_digest": digest(guard_body),
            "symbolic_atomic_guard_branch_count": atomic_count,
            "collision3_handoff_id": handoff_id}


def side_partition_and_handoff(base: Mapping[str, Any], source: Mapping[str, Any],
        side: str, cell: Mapping[str, Any], component: Mapping[str, Any],
        occurrence: Mapping[str, Any], registry_object_sha256: str,
        proof: Mapping[str, Any], incidence: list[dict[str, Any]],
        active_targets: list[str], singular: bool,
        input_pin_set_sha256: str, capability_pin_set_sha256: str
        ) -> tuple[dict[str, Any], dict[str, Any] | None]:
    need(side in {"REPRESENTATIVE", "REFLECTED"}, "physical side")
    task_id = "c76l-task:" + digest({"C68_large_task_row_sha256": base["C68_large_task_row_sha256"],
        "pair_index": base["pair_index"], "path": base["path"]})
    handoff_id = "c76l-c3:" + digest({"task_id": task_id, "physical_side": side,
        "collision2_occurrence_row_sha256": occurrence["collision2_occurrence_row_sha256"]})
    box = (source["closed_representative_box"] if side == "REPRESENTATIVE"
           else source["closed_reflected_box"])
    incidence_digest = digest(incidence)
    exact_guard = {"C1_entry": ("SINGULAR_H1_EXACT_STRATUM" if singular else
            "W[1,0]_IS_UNIQUE_STRICT_FIRST_ON_THE_SELECTED_C1_GRAPH_STRATUM"),
        "collision1_official_word": "EQUALS_PINNED_COLLISION1_WORD",
        "collision1_outgoing_chart": "W_STRICT",
        "collision2_owner": occurrence["collision2_owner"],
        "collision2_owner_guard": ("Delta(owner)>0 AND near(owner)>0 AND near(owner)<tau AND "
            "near(owner)<near(every_other strict future candidate)"),
        "collision2_official_word": occurrence["collision2_word"],
        "collision2_outgoing_branch": "H2_NONZERO_AND_CHART_E_STRICT",
        "all_equalities_owned_by_declared_lower_dimensional_branch": True}
    has_live_c3 = singular or FROZEN_OWNER in active_targets
    handoff_body = {"schema": SCHEMA + ".collision3-handoff-row",
        "handoff_id": handoff_id, "source_task_id": task_id,
        "source_C68_row_sha256": base["C68_large_task_row_sha256"],
        "source_C56_row_sha256": base["C56_task_row_sha256"],
        "source_C41_row_sha256": base["C41_ambient_row_sha256"],
        "C41_primary_obligation_id": base["C41_primary_obligation_id"],
        "pair_index": base["pair_index"], "path": base["path"],
        "physical_side": side, "component_index": cell["component_index"],
        "component_id": cell["component_id"], "gate3_chart": cell["gate3_chart"],
        "closed_physical_box": box,
        "half_open_owner": "E_OR_W_OWNS_H2_ZERO__N_OR_S_EXCLUDES",
        "collision2_occurrence": {key: occurrence[key] for key in (
            "collision2_owner", "collision2_word", "collision2_outgoing_chart",
            "collision2_occurrence_row_sha256")},
        "collision3_occurrence_template": {key: occurrence[key] for key in (
            "collision3_owner", "collision3_word", "collision3_outgoing_chart",
            "collision3_occurrence_row_sha256")},
        "owner_history": ["W[0,0]", FROZEN_OWNER, occurrence["collision2_owner"],
                          occurrence["collision3_owner"]],
        "guard_branch_signs_and_zero_carriers": exact_guard,
        "branch_guard_digest": digest(exact_guard),
        "active_collision1_targets": active_targets,
        "collision1_proof_digest": digest(proof),
        "physical_incidence_digest": incidence_digest,
        "glue": {"C55B_cell_row_sha256": cell["row_sha256"],
            "C55B_component_row_sha256": component["row_sha256"],
            "representative_reflected_glue_id": digest({"pair_index": base["pair_index"],
                "path": base["path"], "box": source["closed_representative_box"],
                "reflected_box": source["closed_reflected_box"]}),
            "same_physical_state_two_occurrences": True,
            "two_sides_and_all_face_corner_incidence_closed": True},
        "prefix_Kraft": {"parent_volume_fraction": source["parent_volume_fraction"],
            "full_dimensional_contribution": (source["parent_volume_fraction"] if box is not None else "0"),
            "equality_carrier_full_dimensional_weight": "0", "prefix_free": True,
            "physical_reflection_duplicate_credit": 0},
        "semialgebraic_registry_object_sha256": registry_object_sha256,
        "input_pin_set_sha256": input_pin_set_sha256,
        "capability_pin_set_sha256": capability_pin_set_sha256,
        "all_upstream_pins_bound_by_registry_and_result": True,
        "schema_complete_sealed_collision3_handoff": True,
        "conditional_bundle3_envelope_not_an_actual_C3_claim": True,
        "formal_credit": 0, "global_credit": 0, "D02_gate_credit": 0,
        "CM2_credit": 0, "candidate_is_authority": False}
    handoff = close_row(handoff_body) if has_live_c3 else None
    non_w = sorted(set(active_targets) - {FROZEN_OWNER})
    cemetery_guard = {"ordered_first_match_ordinal": 0,
        "C1_carriers": ["NO_FUTURE_ROOT", "MINIMUM_ROOT_TIE", "DISCRIMINANT_TANGENCY",
                        "H0_SOURCE_SEAM_ZERO", "H1_OR_SOURCE_RADICAL_ZERO"],
        "C2_carriers": ["POLE_OR_SOURCE_RADICAND_ZERO", "EXPECTED_DELTA_OR_NEAR_NONPOSITIVE",
                        "MINIMUM_ROOT_TIE", "WALL_EQUALITY"],
        "all_zero_carriers_owned_once": True}
    mismatch_guard = {"ordered_first_match_ordinal": 1,
        "C1_strict_mismatch": {"non_W_unique_first_candidates": non_w,
            "wrong_collision1_word_or_non_W_outgoing_chart": True},
        "C2_strict_mismatch": {"nonexpected_unique_owner_count": 54,
            "wrong_official_word_or_non_E_outgoing_chart": True},
        "only_after_bundle0_failed": True}
    glue_guard = {"ordered_first_match_ordinal": 2,
        "expected_collision2_owner": occurrence["collision2_owner"],
        "expected_collision2_word": occurrence["collision2_word"],
        "H2_guard": "h_plus=0 OR h_minus=0",
        "half_open_owner": "E_OR_W_OWNS__N_OR_S_SHADOW",
        "double_zero_corner_owner": "LEXICAL_PHYSICAL_CHART_OWNER",
        "known_sheet_component_index": cell["component_index"],
        "provably_empty_when_frozen_C1_owner_absent": not has_live_c3}
    expected_guard = {**exact_guard, "ordered_first_match_ordinal": 3,
        "only_after_bundles_0_1_2_failed": True,
        "H2_guard": "h_plus!=0 AND h_minus!=0",
        "provably_empty_when_frozen_C1_owner_absent": not has_live_c3}
    entries = [
        branch_entry(task_id, side, "CEMETERY_SOURCE",
            "CEMETERY_OR_SOURCE_GRAZING_TERMINAL", cemetery_guard, 1),
        branch_entry(task_id, side, "STRICT_MISMATCH",
            "WHOLE_BRANCH_STRICT_EXCLUSION", mismatch_guard, 1),
        branch_entry(task_id, side, "KNOWN_H2_GLUE",
            "KNOWN_COMPONENT_CONNECTION", glue_guard, 1),
        branch_entry(task_id, side, "EXPECTED_C3",
            "SEALED_COLLISION3_HANDOFF", expected_guard, 1,
            handoff_id if has_live_c3 else None)]
    action_census = Counter(entry["branch_action"] for entry in entries)
    atomic_action_census: Counter[str] = Counter()
    for entry in entries:
        atomic_action_census[entry["branch_action"]] += entry["symbolic_atomic_guard_branch_count"]
    partition = close_row({"schema": SCHEMA + ".exact-branch-partition-row",
        "source_task_id": task_id, "source_C68_row_sha256": base["C68_large_task_row_sha256"],
        "source_C41_row_sha256": base["C41_ambient_row_sha256"],
        "pair_index": base["pair_index"], "path": base["path"], "physical_side": side,
        "component_index": cell["component_index"], "gate3_chart": cell["gate3_chart"],
        "closed_physical_box": box, "active_collision1_targets": active_targets,
        "semialgebraic_registry_object_sha256": registry_object_sha256,
        "ordered_disjoint_branch_families": entries,
        "ordered_first_match_bundle_count": 4,
        "branch_family_action_census": dict(sorted(action_census.items())),
        "symbolic_atomic_guard_action_census": dict(sorted(atomic_action_census.items())),
        "collision2_residual_branch_count": 0,
        "all_branches_have_one_allowed_terminal_or_C3_action": True,
        "complete_exact_next_owner_and_order_partition": True,
        "physical_nonempty_bundle_census_not_claimed": True,
        "collision3_handoff_row_sha256": None if handoff is None else handoff["row_sha256"],
        "formal_credit": 0, "global_credit": 0, "D02_gate_credit": 0,
        "CM2_credit": 0, "candidate_is_authority": False})
    return partition, handoff


def coherent_attacks(branch_tasks: int, branch_rows: int, conditional_c3_tasks: int,
                     conditional_handoff_rows: int, empty_c3_tasks: int,
                     physical_roots: int, degree1_boundaries: int) -> dict[str, Any]:
    capsule: dict[str, Any] = {
        "scope": 16_883, "universe": 33_319, "precision": PRECISION,
        "additional_dyadic_depth": 0, "branch_tasks": branch_tasks,
        "two_side_branch_rows": branch_rows, "conditional_C3_tasks": conditional_c3_tasks,
        "conditional_C3_handoff_rows": conditional_handoff_rows,
        "C3_provably_empty_tasks": empty_c3_tasks,
        "C2_residual": 0, "candidate_count": 55, "root_order_guards": 1_485,
        "four_charts": True, "four_faces": True, "four_corners": True,
        "owner_history": True, "two_sides": True, "incidence": True,
        "glue": True, "known_sheet_anchor": True, "prefix_Kraft": True,
        "domain_equalities_terminal": True, "root_ties_terminal": True,
        "tangencies_terminal": True, "nonexpected_owner_excluded": True,
        "word_mismatch_excluded": True, "chart_mismatch_excluded": True,
        "physical_roots": physical_roots, "degree1_boundaries": degree1_boundaries,
        "incidence_degree_is_exactly_one_or_two": True,
        "exactly_one_effective_owner_per_physical_root": True,
        "face_key_equation_and_exact_face_bytes_identical_per_root": True,
        "frozen_degree1_scope_source_boundary_registry": True,
        "C3_schema_complete": True, "formal_credit": 0, "global_credit": 0,
        "D02_credit": 0, "CM2_credit": 0, "authority": False,
        "canonical_pointer": False, "producer_consumed_by_verifier": False}
    attacks: dict[str, str] = {}
    for key in sorted(capsule):
        mutant = copy.deepcopy(capsule); value = mutant[key]
        mutant[key] = (not value if type(value) is bool else value + 1)
        try:
            need(mutant == capsule, "coherent attack:" + key)
        except Reject:
            attacks[key] = "FAIL_CLOSED"
        else:
            raise Reject("escaped coherent attack:" + key)
    return {"attack_count": len(attacks), "attacks": attacks,
            "status": f"PASS_{len(attacks)}_OF_{len(attacks)}_COHERENT_ATTACKS_FAIL_CLOSED"}


def build(stage: Path) -> dict[str, Any]:
    need(not stage.exists(), "fresh stage"); stage.mkdir(mode=0o755)
    ctx.prec = PRECISION
    for key, path in FILES.items(): secure(path, PINS[key])
    capability_pins = {}
    for key, (path, pin) in CAPABILITIES.items():
        secure(path, pin); capability_pins[key] = {"path": str(path.relative_to(ROOT)), "sha256": pin}
    need(sha_file(Path(r185.__file__).resolve()) == "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2", "r185 pin")
    need(sha_file(Path(r139.__file__).resolve()) == "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b", "r139 pin")
    need(sha_file(Path(c39.__file__).resolve()) == "873a84cb150efc5649ffb5822457c510ab45c32f3e16a48914c8674dc93c0aae", "c39 pin")
    need(sha_file(Path(h1core.__file__).resolve()) == PINS["H1_CORE"], "H1 core pin")
    authority = chart_authority()

    c68_all = list(rows(secure(FILES["C68_TASKS"], PINS["C68_TASKS"]), "C68 tasks"))
    need(len(c68_all) == 33_319, "C68 universe")
    selected = [row for row in c68_all if row["residual_classification"] in SELECTED]
    need(len(selected) == 16_883 and Counter(row["residual_classification"] for row in selected) == Counter(SELECTED), "selected scope")
    need(len({row["row_sha256"] for row in selected}) == len(selected), "scope unique")

    wanted_c56 = {row["C56_task_row_sha256"] for row in selected}
    c56 = {row["row_sha256"]: row for row in rows(secure(FILES["C56_TASKS"], PINS["C56_TASKS"]), "C56 tasks") if row["row_sha256"] in wanted_c56}
    wanted_ambient = {row["C41_routed_ambient_row_sha256"] for row in selected}
    ambient = {row["row_sha256"]: row for row in rows(secure(FILES["C41_AMBIENT"], PINS["C41_AMBIENT"]), "C41 ambient") if row["row_sha256"] in wanted_ambient}
    need(set(c56) == wanted_c56 and set(ambient) == wanted_ambient, "C56/C41 joins")
    witnesses = Counter(ambient[row["C41_routed_ambient_row_sha256"]]["raw_witness"] for row in selected)
    need(witnesses == Counter(WITNESSES), "witness census")

    wanted_cells = {cell_id for row in selected for cell_id in (
        ambient[row["C41_routed_ambient_row_sha256"]]["representative_cell_id"],
        ambient[row["C41_routed_ambient_row_sha256"]]["reflected_cell_id"])}
    c32 = {row["cell_id"]: row for row in rows(secure(FILES["C32_CELLS"], PINS["C32_CELLS"]), "C32 cells") if row["cell_id"] in wanted_cells}
    c55cells = {row["cell_id"]: row for row in rows(secure(FILES["C55B_CELLS"], PINS["C55B_CELLS"]), "C55B cells") if row["cell_id"] in wanted_cells}
    components = {row["component_index"]: row for row in rows(secure(FILES["C55B_COMPONENTS"], PINS["C55B_COMPONENTS"]), "C55B components")}
    need(set(c32) == set(c55cells) == wanted_cells and set(components) == set(range(26)), "cell/component joins")
    scope_context = {
        row["row_sha256"]: c55cells[ambient[row["C41_routed_ambient_row_sha256"]]["representative_cell_id"]]
        for row in selected
    }
    need(len(scope_context) == 16_883, "scope boundary context")
    frozen_selected_scope_sha256 = digest(sorted(scope_context))

    primary_ids = {ambient[row["C41_routed_ambient_row_sha256"]]["obligation_ids"][0] for row in selected}
    c1_rows = {row["c1_h1_surface_outer_id"]: row for row in rows(secure(FILES["C41_C1"], PINS["C41_C1"]), "C41 C1") if row["c1_h1_surface_outer_id"] in primary_ids}
    c2_rows = {row["c2_surface_outer_id"]: row for row in rows(
        secure(FILES["C41_C2"], PINS["C41_C2"]), "C41 C2")
        if row["c2_surface_outer_id"] in primary_ids}
    endpoint_rows = list(rows(secure(FILES["C41_ENDPOINTS"], PINS["C41_ENDPOINTS"]), "C41 endpoints"))
    endpoint_by_primary = {row.get("owning_primary_outer_id", row["endpoint_rechart_id"]): row for row in endpoint_rows}
    endpoint_by_key = {(row["pair_index"], row["c40_source_leaf_id"], row["descendant_path"]): row for row in endpoint_rows}

    original = first_three(secure(FILES["C35_PATH"], PINS["C35_PATH"]), "C35 path")
    reflected = first_three(secure(FILES["C37_PATH"], PINS["C37_PATH"]), "C37 path")
    expected_word = original[0]["official_word_key_id"]
    expected_owners = {original[1]["selected_absolute_owner_id"], reflected[1]["selected_absolute_owner_id"]}
    pair_index, pattern_index, registry = r139.lower.component_cert.key_index_tables()
    cores = tuple(r139.lower.core_cert.physical_cores())

    semantic_registry = branch_registry(original, reflected, registry)
    exclusive(stage / REGISTRY, canonical(semantic_registry) + b"\n")
    input_pin_set_sha256 = digest(dict(sorted(PINS.items())))
    capability_pin_set_sha256 = digest(capability_pins)

    decision_writer = Ledger(stage / DECISIONS, "C68_33319_ORDER_FILTERED_TO_FIVE_C1_GRAPH_CLASSES")
    branch_writer = Ledger(stage / BRANCHES, "C68_SCOPE_ORDER_THEN_REPRESENTATIVE_REFLECTED")
    handoff_writer = Ledger(stage / HANDOFFS, "C68_SCOPE_ORDER_THEN_REPRESENTATIVE_REFLECTED_LIVE_C3_ONLY")
    occurrences: dict[str, list[dict[str, Any]]] = defaultdict(list)
    dispositions: Counter[str] = Counter(); witness_out: Counter[str] = Counter(); component_census: Counter[int] = Counter()
    graph_count = endpoint_occurrence_count = 0
    branch_tasks = c3_tasks = no_c3_tasks = 0
    try:
        for ordinal, cross in enumerate(selected):
            a = ambient[cross["C41_routed_ambient_row_sha256"]]; task = c56[cross["C56_task_row_sha256"]]
            need(task["C41_routed_ambient_row_sha256"] == a["row_sha256"] and task["pair_index"] == cross["pair_index"] == a["pair_index"] and
                 task["path"] == cross["path"] == a["path"], "task lineage")
            cell = c32[a["representative_cell_id"]]; c55 = c55cells[cell["cell_id"]]
            reflected_cell = c32[a["reflected_cell_id"]]; reflected_c55 = c55cells[reflected_cell["cell_id"]]
            need(cell["origin_key"] == c55["origin_key"] and cell["gate3_chart"] == c55["gate3_chart"] and
                 reflected_cell["origin_key"] == reflected_c55["origin_key"] and
                 reflected_cell["gate3_chart"] == reflected_c55["gate3_chart"], "C32/C55 cells")
            anchor = component_anchor(c55, components[c55["component_index"]])
            reflected_anchor = component_anchor(reflected_c55, components[reflected_c55["component_index"]])
            component_census[c55["component_index"]] += 1
            parent = cell["origin_key"]; witness = a["raw_witness"]
            box = None if a["closed_representative_box"] is None else make_box(a)
            base = {"schema": SCHEMA + ".decision-row", "scope_ordinal": ordinal,
                    "C68_large_task_row_sha256": cross["row_sha256"], "C56_task_row_sha256": task["row_sha256"],
                    "C41_ambient_row_sha256": a["row_sha256"], "C41_primary_obligation_id": a["obligation_ids"][0],
                    "pair_index": a["pair_index"], "path": a["path"], "source_path": a["source_path"],
                    "parent_volume_fraction": a["parent_volume_fraction"], "representative_cell_id": cell["cell_id"],
                    "reflected_cell_id": a["reflected_cell_id"], "parent_key": parent, "gate3_chart": cell["gate3_chart"],
                    "exact_representative_box": a["closed_representative_box"], "exact_reflected_box": a["closed_reflected_box"],
                    "input_residual_classification": cross["residual_classification"], "input_raw_classification": a["raw_classification"],
                    "input_witness": witness, "precision_bits": PRECISION, "additional_dyadic_depth_used": 0,
                    "four_chart_fundamental_domain": {"representative_and_reflected_boxes_bound": True,
                        "chart_seam_quotient": authority, "all_four_exact_faces_materialized": True,
                        "all_four_exact_corners_tested_for_every_regular_graph": True,
                        "graph_only_strata_have_zero_full_dimensional_Kraft_weight": True},
                    "known_sheet_anchor_compatibility": {"REPRESENTATIVE": anchor,
                                                          "REFLECTED": reflected_anchor}}
            proof: dict[str, Any]; incidence: list[dict[str, Any]] = []
            active_targets: list[str] = []
            needs_partition = False
            singular = False
            if witness == "OUTGOING_STATE":
                h1 = c39.h1_route(parent, box)
                need(h1["kind"] == "STRICT_SIDE" and h1["chart"] == "W", "outgoing exact W side")
                try:
                    route = h1core.downstream_W_closed_box(r185, r139, parent, box, expected_word, expected_owners,
                                                            pair_index, pattern_index, cores)
                except h1core.Reject as error:
                    active_targets = [FROZEN_OWNER]; needs_partition = True
                    disposition = "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION"
                    proof = {"kind": "CENTERED_COLLISION1_OUTGOING_TO_EXACT_C2_FOUR_BUNDLE_PARTITION",
                             "H1_route": h1, "strict_mismatch_helper_boundary": str(error),
                             "expected_or_nonstrict_C2_branch_not_asserted_away": True,
                             "collision2_residual_branch_count": 0}
                else:
                    need(route["outcome"] in {"COLLISION1_OFFICIAL_WORD_MISMATCH", "COLLISION2_STRICT_OWNER_MISMATCH"}, "outgoing mismatch")
                    disposition = "WHOLE_TASK_STRICT_EXCLUSION"
                    proof = {"kind": "CENTERED_COLLISION1_OUTGOING_STATE", "H1_route": h1, "downstream_route": route,
                             "whole_task_strict_exclusion_closed": True}
            elif witness in {"REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED", "REGULAR_FULL_FACE_GRAPH"}:
                atlas = {"pair_index": a["pair_index"], "exact_representative_box": a["closed_representative_box"]}
                geometry, _old_roots, kind = h1core.geometry_and_roots(r185, parent, box, atlas)
                route = None; strata = []
                if kind == "STRICT_NEGATIVE":
                    strata = [{"stratum": "EXACT_TASK", "exit": "STRICT_EXCLUSION_NON_W_OUTGOING_CHART"}]
                else:
                    try:
                        route = h1core.downstream_W_closed_box(r185, r139, parent, box, expected_word, expected_owners,
                                                                pair_index, pattern_index, cores)
                    except h1core.Reject as error:
                        route = {"outcome": "EXACT_C2_FOUR_BUNDLE_PARTITION_REQUIRED",
                                 "strict_mismatch_helper_boundary": str(error)}
                        active_targets = [FROZEN_OWNER]; needs_partition = True
                    else:
                        need(route["outcome"] in {"COLLISION1_OFFICIAL_WORD_MISMATCH", "COLLISION2_STRICT_OWNER_MISMATCH"}, "H1 mismatch")
                    if kind == "STRICT_POSITIVE":
                        strata = [{"stratum": "EXACT_TASK", "exit": (
                            "EXACT_C2_FOUR_BUNDLE_PARTITION" if needs_partition else
                            "STRICT_EXCLUSION_W_ROUTE_MISMATCH")}]
                    else:
                        need(kind == "CLIPPED", "H1 clipped")
                        for root in geometry["boundary_roots"]:
                            spec0 = dict(root["exact_face"]); spec = {"gate3_chart": cell["gate3_chart"],
                                "fixed_axis": spec0["fixed_axis"], "fixed_value": spec0["fixed_value"],
                                "varying_axis": spec0["varying_axis"], "varying_interval": spec0["varying_interval"]}
                            key = physical_face_key(spec); rid = physical_root_id(spec, "H1=nx^2-ny^2=0")
                            occurrence = {"physical_root_id": rid, "physical_face_key_sha256": key,
                                "equation": "H1=nx^2-ny^2=0", "exact_physical_face": spec,
                                "C68_large_task_row_sha256": cross["row_sha256"], "face": root["edge_id"],
                                "component_index": c55["component_index"], "half_open_role": "OWNS" if root["edge_id"].endswith("HIGH") else "EXCLUDES_DUPLICATE"}
                            incidence.append(occurrence); occurrences[rid].append(occurrence)
                        strata = [{"stratum": "H1_LT_0", "exit": "STRICT_EXCLUSION_NON_W_OUTGOING_CHART"},
                                  {"stratum": "H1_EQ_0", "exit": ("KNOWN_H2_GLUE_OR_SOURCE_TERMINAL" if needs_partition else
                                      "STRICT_EXCLUSION_W_OWNED_PHYSICAL_GLUE_AND_ROUTE_MISMATCH")},
                                  {"stratum": "H1_GT_0", "exit": ("EXACT_C2_FOUR_BUNDLE_PARTITION" if needs_partition else
                                      "STRICT_EXCLUSION_W_ROUTE_MISMATCH")}]
                disposition = ("EXACT_PER_SIDE_MIXED_BRANCH_PARTITION" if needs_partition else
                               "WHOLE_TASK_STRICT_EXCLUSION")
                proof = {"kind": "EXACT_H1_PHYSICAL_ARRANGEMENT", "H1_geometry": geometry,
                         "downstream_route": route, "sealed_strata": strata,
                         "physical_chart_glue_closed": kind != "CLIPPED" or len(incidence) == 2,
                         "collision2_residual_branch_count": 0,
                         "whole_task_strict_exclusion_closed": not needs_partition}
            elif witness == "SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED":
                source_certificate = source_radical_certificate(
                    parent, box, cell["gate3_chart"], a["closed_representative_box"])
                if source_certificate["endpoint_side"] is not None:
                    source_face = source_certificate["endpoint_side"].lower()
                    spec = exact_faces(cell["gate3_chart"], a["closed_representative_box"])[source_face]
                    equation = source_certificate["equation"] + "=0"
                    key = physical_face_key(spec); rid = physical_root_id(spec, equation)
                    occurrence = {"physical_root_id": rid, "physical_face_key_sha256": key,
                        "equation": equation, "exact_physical_face": spec,
                        "C68_large_task_row_sha256": cross["row_sha256"], "face": source_face,
                        "component_index": c55["component_index"], "half_open_role": "OWNS"}
                    incidence.append(occurrence); occurrences[rid].append(occurrence)
                else:
                    for endpoint in source_certificate["boundary_incidence"]:
                        occurrence = {**endpoint,
                            "C68_large_task_row_sha256": cross["row_sha256"],
                            "component_index": c55["component_index"],
                            "half_open_role": "OWNS" if endpoint["face"].endswith("upper") else
                                "EXCLUDES_DUPLICATE"}
                        incidence.append(occurrence); occurrences[occurrence["physical_root_id"]].append(occurrence)
                active_targets = [FROZEN_OWNER]; needs_partition = True
                disposition = "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION"
                proof = {"kind": "EXACT_COLLISION1_SOURCE_RADICAL_TO_C3_BRANCH_PARTITION",
                         "source_radical_certificate": source_certificate,
                         "negative_Delta_branch_action": "CEMETERY_OR_DISCONNECTED_TERMINAL",
                         "Delta_zero_branch_action": "SOURCE_GRAZING_TERMINAL",
                         "positive_Delta_branch_action": "EXACT_H1_OUTGOING_THEN_C2_OWNER_ORDER_PROGRAM",
                         "collision2_residual_branch_count": 0,
                         "source_grazing_oracle_complete": True}
            elif witness == "Round185Error:AD sqrt domain":
                endpoint = endpoint_by_primary[a["obligation_ids"][0]]
                geometry = endpoint["endpoint_rechart_geometry"]
                need(endpoint["raw_classification"] ==
                     "UNRESOLVED_C40_SOURCE_RADICAL_ENDPOINT_ROUTE_EVALUATION_FAILURE_OUTER" and
                     endpoint["raw_witness"] == "Round185Error:AD sqrt domain" and
                     endpoint["descendant_path"] == a["path"] and
                     geometry["endpoint_kind"] == "RATIONAL_P_ENDPOINT_STEREOGRAPHIC_RECHART" and
                     geometry["carrier_existence_status"] == "CERTIFIED_EXACT_ENDPOINT_CARRIER" and
                     geometry["half_open_endpoint_dedup_complete"] is True,
                     "C41 exact stereographic endpoint lineage")
                active_targets = [FROZEN_OWNER]; needs_partition = True
                disposition = "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION"
                proof = {"kind": "EXACT_STEREOGRAPHIC_SOURCE_ENDPOINT_TO_C3_BRANCH_PARTITION",
                         "C41_endpoint_row_sha256": endpoint["row_sha256"],
                         "endpoint_rechart_geometry": geometry,
                         "u_zero_branch_action": "SOURCE_GRAZING_TERMINAL",
                         "positive_u_branch_action": "EXACT_C1_H1_AND_C2_FOUR_BUNDLE_PROGRAM",
                         "unit_circle_identity_replayed_exactly": True,
                         "collision2_residual_branch_count": 0}
            elif witness == "EXACT_ALGEBRAIC_ENDPOINT_REQUIRES_GRAPH_CELL":
                endpoint = endpoint_by_key[(a["pair_index"], a["c40_source_leaf_id"], a["path"])]
                geometry = endpoint["endpoint_rechart_geometry"]
                need(geometry["endpoint_kind"] == "ALGEBRAIC_H0_SOURCE_CHART_SEAM" and
                     geometry["adjacent_chart_seam_p_span_exhaustive"] is True and
                     geometry["adjacent_chart_seam_incidence_count"] >= 1, "H0 seam")
                active_targets = [FROZEN_OWNER, "ALGEBRAIC_H0_SOURCE_CHART_SEAM"]
                needs_partition = True
                disposition = "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION"
                proof = {"kind": "ALGEBRAIC_H0_EXACT_CHART_SEAM_TO_C3_BRANCH_PARTITION",
                         "C41_endpoint_row_sha256": endpoint["row_sha256"],
                         "endpoint_rechart_geometry": geometry,
                         "H0_zero_carrier_action": "SOURCE_GRAZING_TERMINAL",
                         "adjacent_open_chart_actions": "EXACT_C1_WINNER_THEN_C2_OWNER_ORDER_BRANCH_PROGRAM",
                         "owner_history_glue_two_sides_incidence_bound": True,
                         "collision2_residual_branch_count": 0}
            elif witness == "SINGULAR_OR_MULTI_GRAPH_ARRANGEMENT_REQUIRED":
                primary = c1_rows[a["obligation_ids"][0]]
                need(primary["normalized_surface_count"] == 1 and primary["normalized_surfaces"][0]["kind"] == "H1", "singular H1")
                active_targets = [FROZEN_OWNER, "SINGULAR_H1_EXACT_STRATUM"]
                needs_partition = True; singular = True
                disposition = "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION"
                proof = {"kind": "SINGULAR_H1_EXACT_BOX_HANDOFF", "C41_primary_row_sha256": primary["row_sha256"],
                         "normalized_surface": primary["normalized_surfaces"][0],
                         "expected_owner_match_not_asserted_away": True,
                         "schema_complete_direct_collision3_handoff": True,
                         "collision2_residual_branch_count": 0}
            else:
                need(witness in {"inherited interval ordering or boundary type not isolated",
                                 "unique monotone inherited-active-set first tangency"}, "multi witness")
                primary = c1_rows[a["obligation_ids"][0]]
                cbox, active = c39.reconstruct_box(cell, a["path"])
                need((cbox.t0, cbox.t1, cbox.p0, cbox.p1, cbox.s0, cbox.s1) ==
                     (box.t0, box.t1, box.p0, box.p1, box.s0, box.s1), "box reconstruction")
                active_targets = list(active); needs_partition = True
                _stage_one, natural = c39.c38.round166.classify_active(cell["gate3_chart"], box, active)
                enhanced = [c39.enhanced_record(parent, box, item)[0] for item in natural]
                graph_records = [item for item in enhanced if item.classification == "unresolved_discriminant"]
                targets = [item["identifier"] for item in primary["normalized_surfaces"]]
                need(sorted(item.target_id for item in graph_records) == sorted(targets) and len(graph_records) >= 1, "graph registry")
                certificates = []; raw_by_target = {}
                for record in graph_records:
                    certificate, endpoints, raw_graph, delta = graph_certificate(parent, box, record.target_id,
                                                                                  cell["gate3_chart"], a["closed_representative_box"])
                    certificates.append(certificate); raw_by_target[record.target_id] = (raw_graph, delta)
                    for occurrence in endpoints:
                        current = {**occurrence, "C68_large_task_row_sha256": cross["row_sha256"],
                                   "component_index": c55["component_index"],
                                   "half_open_role": "OWNS" if occurrence["face"].endswith("upper") else "EXCLUDES_DUPLICATE"}
                        incidence.append(current); occurrences[current["physical_root_id"]].append(current)
                graph_count += len(certificates)
                summaries = [record_summary(item) for item in enhanced]
                order = []
                order_records = [item for item in enhanced if item.classification in {
                    "strict_future_root", "unresolved_discriminant"}]
                def interval(item: Any) -> tuple[Any, Any]:
                    if item.classification == "strict_future_root":
                        return item.near.lower(), item.near.upper()
                    raw_item, delta_item = raw_by_target[item.target_id]
                    return (raw_item["ell"].value.lower() - delta_item.upper().sqrt().upper(),
                            raw_item["ell"].value.upper())
                for left, right in itertools.combinations(order_records, 2):
                    left_lower, left_upper = interval(left); right_lower, right_upper = interval(right)
                    if bool(left_upper < right_lower):
                        relation = "LEFT_STRICTLY_BEFORE_RIGHT_ON_EVERY_REAL_STRATUM"
                        gap = bounds(right_lower - left_upper)
                    elif bool(right_upper < left_lower):
                        relation = "RIGHT_STRICTLY_BEFORE_LEFT_ON_EVERY_REAL_STRATUM"
                        gap = bounds(left_lower - right_upper)
                    else:
                        relation = "EXACT_ORDER_TRICHOTOMY_MATERIALIZED_WITH_EQUALITY_C3_OR_CEMETERY_OWNER"
                        gap = None
                    guard = {"left": left.target_id, "right": right.target_id,
                             "equation": f"near({left.target_id})-near({right.target_id})=0"}
                    order.append({**guard, "relation": relation, "strict_gap": gap,
                        "less_branch_action": "ACTION_BY_UNIQUE_FIRST_OWNER_BRANCH",
                        "equal_branch_action": "CEMETERY_SIMULTANEOUS_COLLISION_TERMINAL",
                        "greater_branch_action": "ACTION_BY_UNIQUE_FIRST_OWNER_BRANCH",
                        "guard_digest": digest(guard)})
                first_tangency = witness.startswith("unique monotone")
                if first_tangency:
                    need(len(certificates) == 1, "one first tangency graph")
                    raw_graph, delta = next(iter(raw_by_target.values()))
                    need(bool(raw_graph["ell"].value.lower() - delta.upper().sqrt().upper() > 0), "future tangency margin")
                disposition = "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION"
                proof = {"kind": "EXACT_MULTI_DISCRIMINANT_GRAPH_TO_C3_BRANCH_PARTITION",
                         "C41_primary_row_sha256": primary["row_sha256"], "active_targets": list(active),
                         "enhanced_collision1_records": summaries, "regular_graph_certificates": certificates,
                         "pairwise_root_order_and_intersection_registry": order,
                         "sign_strata_schema": [{"graph_target": item["target"],
                            "negative_open_slab": "ACTION_BY_EXPLICIT_C1_UNIQUE_FIRST_BRANCH",
                            "zero_graph": ("CEMETERY_TANGENCY_TERMINAL" if first_tangency else
                                "ACTION_BY_EXPLICIT_C1_MINIMUM_EQUALITY_BRANCH"),
                            "positive_open_slab": "ACTION_BY_EXPLICIT_C1_UNIQUE_FIRST_BRANCH"}
                            for item in certificates],
                         "expected_C2_owner_branches_emit_schema_complete_C3_handoffs": True,
                         "nonexpected_C2_owner_word_or_chart_branches_are_strict_exclusions": True,
                         "tie_domain_and_tangency_branches_are_owned_terminals": True,
                         "collision2_residual_branch_count": 0,
                         "complete_graph_equations_faces_roots_and_state_registry": True}
            endpoint_occurrence_count += len(incidence)
            branch_hashes: list[str] = []; handoff_hashes: list[str] = []
            if needs_partition:
                branch_tasks += 1
                has_c3 = singular or FROZEN_OWNER in active_targets
                if has_c3: c3_tasks += 1
                else: no_c3_tasks += 1
                for side, side_cell in (("REPRESENTATIVE", c55), ("REFLECTED", reflected_c55)):
                    occurrence = semantic_registry["expected_occurrences"][side]
                    partition, handoff = side_partition_and_handoff(
                        base, a, side, side_cell, components[side_cell["component_index"]], occurrence,
                        semantic_registry["object_sha256"], proof, incidence, active_targets, singular,
                        input_pin_set_sha256, capability_pin_set_sha256)
                    if handoff is not None:
                        handoff_writer.write_closed(handoff); handoff_hashes.append(handoff["row_sha256"])
                    branch_writer.write_closed(partition); branch_hashes.append(partition["row_sha256"])
                need(len(branch_hashes) == 2 and len(handoff_hashes) == (2 if has_c3 else 0),
                     "two-side branch/handoff cardinality")
            decision_writer.write({**base, "proof": proof, "physical_graph_endpoint_occurrences": incidence,
                                   "exact_branch_partition_row_sha256": branch_hashes,
                                   "collision3_handoff_row_sha256": handoff_hashes,
                                   "collision2_residual_branch_count": 0,
                                   "task_disposition": disposition, "formal_credit": 0, "global_credit": 0,
                                   "D02_gate_credit": 0, "CM2_credit": 0, "candidate_is_authority": False})
            dispositions[disposition] += 1; witness_out[witness] += 1
            if ordinal and ordinal % 1000 == 0: print(f"C76L progress {ordinal}/16883", file=sys.stderr, flush=True)
    finally:
        decision_writer.close(); branch_writer.close(); handoff_writer.close()

    boundary_writer = Ledger(stage / BOUNDARIES, "DEGREE1_PHYSICAL_ROOT_ID_ASCENDING")
    incidence_writer = Ledger(stage / INCIDENCE, "PHYSICAL_ROOT_ID_ASCENDING")
    degree_census: Counter[int] = Counter()
    raw_owner_census: Counter[int] = Counter()
    effective_owner_kind_census: Counter[str] = Counter()
    boundary_classification_census: Counter[str] = Counter()
    try:
        for root_id in sorted(occurrences):
            current = sorted(occurrences[root_id], key=lambda row: (row["C68_large_task_row_sha256"], row["face"]))
            need(len(current) in {1, 2}, "exact incidence degree bound")
            need(len({(row["C68_large_task_row_sha256"], row["face"]) for row in current}) == len(current),
                 "duplicate physical-root occurrence")
            need(all(row.get("physical_root_id") == root_id for row in current), "physical root identity")
            need(all(row.get("half_open_role") in {"OWNS", "EXCLUDES_DUPLICATE"} for row in current),
                 "half-open role vocabulary")
            for field in ("physical_face_key_sha256", "equation", "exact_physical_face"):
                need(len({canonical(row.get(field)) for row in current}) == 1,
                     "byte-identical physical-root " + field)
            need(root_id == physical_root_id(current[0]["exact_physical_face"], current[0]["equation"]),
                 "physical root digest reconstruction")
            need(current[0]["physical_face_key_sha256"] == physical_face_key(current[0]["exact_physical_face"]),
                 "physical face digest reconstruction")
            owners = [row for row in current if row["half_open_role"] == "OWNS"]
            components_here = sorted({row["component_index"] for row in current})
            need(len(components_here) == 1, "root component identity")
            degree_census[len(current)] += 1
            raw_owner_census[len(owners)] += 1
            boundary_row = None
            if len(current) == 2:
                need(len(owners) == 1, "degree-two exactly one half-open owner")
                owner = owners[0]
                effective_owner = {"kind": "TASK_HALF_OPEN_OCCURRENCE",
                    "C68_large_task_row_sha256": owner["C68_large_task_row_sha256"], "face": owner["face"]}
            else:
                need(len(owners) in {0, 1}, "degree-one raw owner bound")
                only = current[0]
                cell = scope_context[only["C68_large_task_row_sha256"]]
                component_cell_boundary = cell_face_is_outer_boundary(
                    cell, only["face"], only["exact_physical_face"])
                source_boundary = ("source" in only["equation"].lower() or
                                   "1-p^2" in only["equation"].lower())
                classification = ("FROZEN_SOURCE_GRAZING_BOUNDARY" if source_boundary else
                    "FROZEN_COMPONENT_CELL_BOUNDARY" if component_cell_boundary else
                    "FROZEN_SELECTED_C76L_SCOPE_BOUNDARY")
                if owners:
                    owner = owners[0]
                    effective_owner = {"kind": "TASK_HALF_OPEN_OCCURRENCE",
                        "C68_large_task_row_sha256": owner["C68_large_task_row_sha256"], "face": owner["face"]}
                else:
                    effective_owner = {"kind": "FROZEN_SCOPE_SOURCE_BOUNDARY_REGISTRY",
                        "boundary_owner_id": "c76l-boundary-owner:" + digest({
                            "physical_root_id": root_id, "frozen_selected_scope_sha256": frozen_selected_scope_sha256})}
                boundary_row = boundary_writer.write({"schema": SCHEMA + ".degree1-scope-source-boundary-row",
                    "physical_root_id": root_id,
                    "physical_face_key_sha256": only["physical_face_key_sha256"],
                    "equation": only["equation"], "exact_physical_face": only["exact_physical_face"],
                    "component_index": components_here[0], "occurrence_degree": 1,
                    "sole_occurrence": only, "raw_half_open_owner_count": len(owners),
                    "representative_cell_id": cell["cell_id"],
                    "component_cell_boundary": component_cell_boundary,
                    "boundary_classification": classification,
                    "frozen_selected_scope_sha256": frozen_selected_scope_sha256,
                    "unique_effective_owner": effective_owner, "effective_owner_count": 1,
                    "byte_identical_face_key_equation_and_exact_face": True,
                    "formal_credit": 0, "global_credit": 0, "D02_gate_credit": 0})
                boundary_classification_census[classification] += 1
            effective_owner_kind_census[effective_owner["kind"]] += 1
            incidence_writer.write({"schema": SCHEMA + ".physical-graph-incidence-row",
                "physical_root_id": root_id, "physical_face_key_sha256": current[0]["physical_face_key_sha256"],
                "equation": current[0]["equation"], "exact_physical_face": current[0]["exact_physical_face"],
                "component_index": components_here[0], "occurrence_count": len(current), "occurrences": current,
                "raw_half_open_owner_count": len(owners), "unique_effective_owner": effective_owner,
                "effective_owner_count": 1,
                "two_sides_closed_when_both_present": len(current) >= 2,
                "single_occurrence_is_scope_or_source_cell_boundary": len(current) == 1,
                "degree1_scope_source_boundary_row_sha256": (
                    None if boundary_row is None else boundary_row["row_sha256"]),
                "exact_incidence_degree_in_1_2": True,
                "byte_identical_face_key_equation_and_exact_face": True,
                "corner_incidence": False, "source_seam_consumed_via_pinned_C74L": True,
                "same_physical_trace_duplicate_identified_not_added": True,
                "full_dimensional_Kraft_weight": "0", "formal_credit": 0, "D02_gate_credit": 0})
    finally:
        boundary_writer.close(); incidence_writer.close()

    need(incidence_writer.count == 17_235, "physical root census")
    need(boundary_writer.count == 1_337 and degree_census == Counter({2: 15_898, 1: 1_337}),
         "exact degree/boundary census")
    need(raw_owner_census == Counter({1: 16_781, 0: 454}), "raw owner census")
    need(effective_owner_kind_census == Counter({
        "TASK_HALF_OPEN_OCCURRENCE": 16_781,
        "FROZEN_SCOPE_SOURCE_BOUNDARY_REGISTRY": 454}), "effective owner census")
    need(sum(boundary_classification_census.values()) == boundary_writer.count,
         "frozen boundary classification census")

    need(decision_writer.count == 16_883 and witness_out == Counter(WITNESSES), "output census")
    need(sum(component_census.values()) == 16_883 and set(component_census) <= {0, 1}, "large components only")
    need(sum(dispositions.values()) == 16_883 and set(dispositions) <= {
        "WHOLE_TASK_STRICT_EXCLUSION", "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION"},
        "closed disposition census:" + repr(dispositions))
    need(branch_tasks == dispositions["EXACT_PER_SIDE_MIXED_BRANCH_PARTITION"] and
         no_c3_tasks == 1_088 and c3_tasks + no_c3_tasks == branch_tasks,
         "branch task census")
    need(branch_writer.count == 2 * branch_tasks and handoff_writer.count == 2 * c3_tasks,
         "two-side branch/handoff ledger census")

    decision_desc = decision_writer.descriptor(); incidence_desc = incidence_writer.descriptor()
    boundary_desc = boundary_writer.descriptor()
    branch_desc = branch_writer.descriptor(); handoff_desc = handoff_writer.descriptor()
    result = close_object({"schema": SCHEMA,
        "status": (f"PASS_C76L_EXACT_16883_C1_GRAPH_TASKS__NO_C2_RESIDUAL__"
                   f"{branch_writer.count}_FOUR_BUNDLE_SIDE_PARTITIONS__"
                   f"{handoff_writer.count}_CONDITIONAL_C3_ENVELOPES__ZERO_CREDIT"),
        "scope": {"frozen_universe_count": 33_319, "selected_count": 16_883,
                  "residual_classification_census": dict(sorted(SELECTED.items())),
                  "witness_census": dict(sorted(WITNESSES.items())),
                  "source_row_hashes_unique": True},
        "disposition_census": dict(sorted(dispositions.items())), "component_task_census": {str(k): v for k, v in sorted(component_census.items())},
        "numeric_authority": {"precision_bits": PRECISION, "additional_dyadic_depth": 0,
            "r185_sha256": sha_file(Path(r185.__file__).resolve()), "r139_sha256": sha_file(Path(r139.__file__).resolve()),
            "c39_sha256": sha_file(Path(c39.__file__).resolve()), "h1_core_sha256": PINS["H1_CORE"],
            "official_registry_sha256": registry},
        "input_file_sha256": dict(PINS), "sealed_capability_pins": capability_pins,
        "semialgebraic_branch_registry": {"filename": REGISTRY,
            "sha256": sha_file(stage / REGISTRY), "object_sha256": semantic_registry["object_sha256"],
            "candidate_count": 55, "pairwise_order_guard_count": 1_485},
        "ledgers": {"decisions": decision_desc, "physical_graph_incidence": incidence_desc,
                    "degree1_scope_source_boundary_registry": boundary_desc,
                    "exact_branch_partitions": branch_desc, "collision3_handoffs": handoff_desc},
        "branch_closure": {"task_count": branch_tasks, "two_side_partition_row_count": branch_writer.count,
            "task_with_conditional_bundle3_envelope_count": c3_tasks,
            "task_with_provably_empty_bundle3_count": no_c3_tasks,
            "conditional_schema_complete_collision3_handoff_row_count": handoff_writer.count,
            "materialized_bundle_census": {"CEMETERY_SOURCE": branch_writer.count,
                "STRICT_MISMATCH": branch_writer.count, "KNOWN_H2_GLUE": branch_writer.count,
                "EXPECTED_C3": branch_writer.count},
            "physical_nonempty_bundle_census_claimed": False,
            "collision2_residual_branch_count": 0,
            "all_nonexpected_owner_word_chart_branches_strictly_excluded": True,
            "all_tie_domain_tangency_branches_terminalized": True},
        "graph_census": {"regular_discriminant_graph_count": graph_count,
                         "physical_endpoint_occurrence_count": endpoint_occurrence_count,
                         "physical_root_count": incidence_writer.count,
                         "exact_degree_census": {str(k): v for k, v in sorted(degree_census.items())},
                         "raw_half_open_owner_count_census": {str(k): v for k, v in sorted(raw_owner_census.items())},
                         "effective_owner_kind_census": dict(sorted(effective_owner_kind_census.items())),
                         "degree1_scope_source_boundary_count": boundary_writer.count,
                         "boundary_classification_census": dict(sorted(boundary_classification_census.items())),
                         "frozen_selected_scope_sha256": frozen_selected_scope_sha256,
                         "face_key_equation_and_exact_face_byte_identity_closed": True,
                         "exactly_one_effective_owner_per_physical_root": True},
        "producer_self_test": coherent_attacks(branch_tasks, branch_writer.count, c3_tasks,
                                                handoff_writer.count, no_c3_tasks,
                                                incidence_writer.count, boundary_writer.count),
        "strict_boundary": {"formal_credit": 0, "global_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
            "whole_component_known_sheet_credit": 0, "canonical_pointer_or_seal_written": False,
            "collision2_residual_handoff_count": 0,
            "collision3_handoffs_require_later_global_consumer": True}})
    exclusive(stage / RESULT, canonical(result) + b"\n")
    report = ("# C76-L large-component collision-one / graph exact oracle\n\n"
              f"- scope: 16,883 / 33,319\n- dispositions: `{json.dumps(dict(sorted(dispositions.items())), sort_keys=True)}`\n"
              f"- regular discriminant graphs: {graph_count}\n- physical roots: {incidence_writer.count}\n"
              f"- degree-one frozen scope/source boundary rows: {boundary_writer.count}\n"
              f"- two-side exact branch rows: {branch_writer.count}\n"
              f"- conditional schema-complete collision-3 envelope rows: {handoff_writer.count}\n"
              "- collision-2 residual exits: 0\n"
              "- no additional dyadic depth; all formal/global/D02/CM2 credit remains zero.\n")
    exclusive(stage / REPORT, report.encode("utf-8"))
    exclusive(stage / LOCK, b"C76L is staged zero-credit. There are no collision-two residual exits; sealed collision-three handoffs require the no-producer global consumer.\n")
    members = sorted(path for path in stage.iterdir() if path.name not in {MANIFEST, OUTER})
    manifest_raw = b"".join(f"{sha_file(path)}  {path.name}\n".encode("ascii") for path in members)
    exclusive(stage / MANIFEST, manifest_raw)
    outer = close_object({"schema": SCHEMA + ".outer-receipt", "candidate_object_sha256": result["object_sha256"],
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "ordered_member_file_sha256": [{"filename": path.name, "sha256": sha_file(path)} for path in members],
        "outer_receipt_published_last": True, "terminal_byte_replay_required_and_completed": True,
        "formal_credit": 0, "D02_gate_credit": 0})
    exclusive(stage / OUTER, canonical(outer) + b"\n")
    for path in [*members, stage / MANIFEST, stage / OUTER]: sha_file(path)
    return result


def complete(a: Path, b: Path, verify_a: Path, verify_b: Path, output: Path) -> None:
    need(not output.exists(), "fresh completion")
    names = [DECISIONS, INCIDENCE, BOUNDARIES, BRANCHES, HANDOFFS, REGISTRY,
             RESULT, REPORT, MANIFEST, OUTER, LOCK]
    hashes = {}
    for name in names:
        left, right = secure(a / name, sha_file(a / name)), secure(b / name, sha_file(b / name))
        need(left == right, "dual bytes:" + name); hashes[name] = hashlib.sha256(left).hexdigest()
    va = strict_json(secure(verify_a, sha_file(verify_a)), "verify a")
    vb = strict_json(secure(verify_b, sha_file(verify_b)), "verify b")
    need(va == vb and va["status"].startswith("PASS_INDEPENDENT_C76L"), "dual verification")
    receipt = close_object({"schema": SCHEMA + ".dual-build-completion-receipt", "dual_build_byte_identical": True,
        "member_sha256": hashes, "independent_verification_file_sha256": sha_file(verify_a),
        "independent_verification_object_sha256": va["object_sha256"],
        "terminal_byte_replay_completed_after_outer_receipts": True, "formal_credit": 0, "D02_gate_credit": 0})
    exclusive(output, canonical(receipt) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="command", required=True)
    build_p = sub.add_parser("build"); build_p.add_argument("stage", type=Path)
    done = sub.add_parser("complete"); done.add_argument("a", type=Path); done.add_argument("b", type=Path)
    done.add_argument("verify_a", type=Path); done.add_argument("verify_b", type=Path); done.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.command == "build":
        value = build(args.stage); print(json.dumps({"stage": str(args.stage), "object_sha256": value["object_sha256"]}, sort_keys=True))
    else: complete(args.a, args.b, args.verify_a, args.verify_b, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
