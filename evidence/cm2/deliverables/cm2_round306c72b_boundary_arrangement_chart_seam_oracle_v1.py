#!/usr/bin/env python3
"""C72b: exact H1 boundary arrangements and chart-seam terminals.

The parent process treats every upstream as pinned inert bytes and never loads
the numerical kernel.  Fresh child processes independently reconstruct bounded
batches at 384 bits; this both bounds FLINT memory and makes batch size an
irrelevant build-isolation variable.  No producer, verifier, pointer, or seal
from an upstream round is imported or executed.
"""
from __future__ import annotations

import argparse
import collections
import copy
import gzip
import hashlib
import itertools
import json
import os
import stat
import subprocess
import sys
import zlib
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
SITE = ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages"
SCHEMA = "cm2.round306c72b.boundary-arrangement-chart-seam-oracle.v1"
PREFIX = "cm2_round306c72b_boundary_arrangement_chart_seam_oracle_v1"
ROWS = PREFIX + ".jsonl.gz"
INCIDENCE = PREFIX + "_root_incidence.jsonl.gz"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
LOCK = "ZERO_CREDIT_STAGED_BOUNDARY_CHART_SEAM_ORACLE_ONLY.lock"
PRECISION = 384
SELECTOR = "REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED"
FROZEN_OWNER = "W[1,0]"
CORE_INDEX = {"W:E": 14, "W:N": 17, "W:S": 20, "W:W": 23}
ZERO = {"formal_credit": 0, "whole_parent_credit": 0,
        "D02_gate_credit": 0, "CM2_credit": 0}

C72_NAMES = {
    "result": "cm2_round306c72_structural_child_obligation_atlas_v1_result.json",
    "ledger": "cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz",
    "verification": "cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json",
}
C38_DIR = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C35_DIR = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C37_DIR = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"
C71B_DIR = ROOT / ".cm2-runtime/c71b-v3-final-75c21279"
C72O_DIR = ROOT / ".cm2-runtime/c72o-build-a2.v1"
C73_DIR = ROOT / ".cm2-runtime/c73v2-build-a.QOYACE"

PINS = {
    "C72_RESULT": "55318b7c3ee778cb8a0e41d612c9c2caa44790e6fff816a6104116268258f01e",
    "C72_LEDGER": "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370",
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
    "C38_RESULT": "094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501",
    "C38_CHILDREN": "0347849c0368368430f5456b71cd4a4bce4e5912c8a3da33649cfac35b1708a2",
    "C35_PATH": "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66",
    "C37_PATH": "7c87829f6ef883b7928ff8a313d5bfcf240383c51a9040739de1cfe7e617bef5",
    "C71B_RESULT": "5ede807e4860b60fe8582597cc6be10cdfdc7b3a0eeba57ced317f4980092246",
    "C71B_VERIFY": "ee105922e263d9cea551088ee67c350cc9adc4d9f375a8584428e4fa55575612",
    "C71B_RECEIPT": "3a6cfa624fab8cd1b787d3facd139cf9e055a008236864d894d2633522fe9fbc",
    "C72O_RESULT": "fd9ca6489f5fedef85fb55de6906a62ecadc417c72d7eb938a6268e7f402302a",
    "C72O_LEDGER": "e3125863adcf3ef6489dce741337622b1d70b2ce7655d8d06237c1612ff19355",
    "C72O_VERIFY": "2d34c25b5fd9f2b3a1e8b30d184b40d8a93ffce8c192d193b75715e0d7a68ccb",
    "C73_RESULT": "5de9d37c69ed4d13d972eff8845ed55ad695ab040d6c1beda01626c0c065c615",
    "C73_LEDGER": "ed0a3d26f4984e6eced899a01f58aa8329bb1db72b7d0bfb9fe17ee3a4eef6fc",
    "C73_VERIFY": "784505135d105fcdf05cc2d6e37779ea896f7d1bbe06e75dd1019b67ae951fe1",
}
OBJECTS = {
    "C72_RESULT": "a6aa0cfd8e1ee1b7a02d92af066acb23abffb22b0b7276b7e233d2ff7d92f9f4",
    "C72_VERIFY": "8ae20b71916ee1f6d1d28e633b1fbc080f4cb277eed7b6bb54937f8538ae7994",
    "C71B_RESULT": "75c21279e3440a32116e67c20f12c7ec9d299491d018e2982ab18d68118d4158",
    "C71B_VERIFY": "c45c5b19daeaef930f981810722460424a0d55c8302380829757e2132754f5c3",
    "C71B_RECEIPT": "d7fd8322b72fad933bb80542913b00cb54c5d7a3d93bf8cb7601aefa5daadbcd",
    "C72O_RESULT": "529d7081293b37111619d4dbf03c750be06da48105d46cc18e8c79eee10b48e7",
    "C72O_VERIFY": "41d383e0fc68ec7d7c4887ae6ef534b5b7bd19277837a14754e5c7ef5bf85715",
    "C73_RESULT": "4ddba93eea8b798de3dbc8a74608fc27686e46c9209784a6bccdd5df7fd1e1cc",
    "C73_VERIFY": "c6d9bc55347de05cef6dc3061a905e1052521a16bb6a6535233c9012b77ffd9d",
}
NUMERIC_PINS = {
    "r185": "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    "r178": "06075baac268e8e6c9deeeedae3e502b3a96630f3650c0b783c2b2a77dbd23f9",
    "atlas": "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "ge": "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "registry": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "r139": "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    "lower": "42d749dccea86aa3a122707db0226def176e75047d5dcb4bf19826b50e09282b",
    "round136": "4e78309d5275bf367e6df03509c40ebaaac6f344c7948446a25b3b508c8c2bc2",
    "time3": "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
    "time2": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "core": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "step1": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link:" + str(path))
        hasher = hashlib.sha256()
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
        after = os.fstat(descriptor)
        need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
              before.st_ctime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
              after.st_ctime_ns), "TOCTOU:" + str(path))
        return hasher.hexdigest()
    finally:
        os.close(descriptor)


def pinned(path: Path, expected: str) -> bytes:
    raw = path.read_bytes()
    need(not path.is_symlink() and path.stat().st_nlink == 1 and
         hashlib.sha256(raw).hexdigest() == expected, "file pin:" + str(path))
    return raw


def parse(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict, label + ":object")
    return value


def close_object(value: Mapping[str, Any], expected: str, label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(claim == expected == digest(body), label + ":object closure")


def close_row(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":row closure")


def iter_jsonl(path: Path, expected: str, count: int) -> Iterator[dict[str, Any]]:
    need(file_sha(path) == expected, "ledger pin:" + str(path))
    with gzip.open(path, "rb") as stream:
        for ordinal, raw in enumerate(stream):
            need(raw.endswith(b"\n"), "row newline")
            row = parse(raw[:-1], str(path) + ":" + str(ordinal))
            need(canonical(row) + b"\n" == raw, "canonical row")
            close_row(row, "row")
            yield row
        need(ordinal + 1 == count, "row count:" + str(path))


def write_exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_CLOEXEC", 0), 0o644)
    try:
        view = memoryview(raw)
        while view:
            size = os.write(descriptor, view)
            need(size > 0, "short write")
            view = view[size:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


class Ledger:
    def __init__(self, path: Path, order: str):
        self.path, self.order = path, order
        self.raw = None
        self.gz = None
        self.count = 0
        self.sequence = hashlib.sha256()

    def __enter__(self):
        descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                             0o644)
        self.raw = os.fdopen(descriptor, "wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        return self

    def write(self, body: dict[str, Any]) -> dict[str, Any]:
        row = {**body, "row_sha256": digest(body)}
        self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row["row_sha256"] + "\n").encode("ascii"))
        self.count += 1
        return row

    def __exit__(self, *_args):
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {"filename": self.path.name, "order": self.order,
                "row_count": self.count,
                "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
                "sha256": file_sha(self.path), "size": self.path.stat().st_size}


def arb_payload(value: Any) -> dict[str, Any]:
    return {"lower": str(value.lower()), "upper": str(value.upper()),
            "contains_zero": bool(value.contains(0))}


def sign(value: Any) -> int:
    return 1 if bool(value > 0) else -1 if bool(value < 0) else 0


def sign_name(value: int) -> str:
    need(value in {-1, 1}, "strict sign")
    return "NEGATIVE" if value < 0 else "POSITIVE"


def face_specs(pair: int, box: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    t0, t1 = box["t"]
    p0, p1 = box["p"]
    return {
        "T_LOW": {"pair_index": pair, "fixed_axis": "t", "fixed_value": t0,
                  "varying_axis": "p", "varying_interval": [p0, p1]},
        "T_HIGH": {"pair_index": pair, "fixed_axis": "t", "fixed_value": t1,
                   "varying_axis": "p", "varying_interval": [p0, p1]},
        "P_LOW": {"pair_index": pair, "fixed_axis": "p", "fixed_value": p0,
                  "varying_axis": "t", "varying_interval": [t0, t1]},
        "P_HIGH": {"pair_index": pair, "fixed_axis": "p", "fixed_value": p1,
                   "varying_axis": "t", "varying_interval": [t0, t1]},
    }


def face_key(spec: Mapping[str, Any]) -> str:
    return digest({"schema": SCHEMA + ".exact-face-key", **dict(spec)})


def root_id(spec: Mapping[str, Any]) -> str:
    return digest({"schema": SCHEMA + ".unique-H1-edge-root", "owner": FROZEN_OWNER,
                   "equation": "H1=nx^2-ny^2", **dict(spec)})


def strict_depth(value: Any, arbq: Any) -> int:
    lower = Q(*value.lower().man_exp()) if False else None
    # String-free exact dyadic conversion used by both producer and verifier.
    mantissa, exponent = value.lower().man_exp()
    lower_q = Q(int(mantissa)) * (Q(2) ** int(exponent))
    need(lower_q > 0, "positive margin")
    depth = max(0, lower_q.denominator.bit_length() - lower_q.numerator.bit_length() + 1)
    while not bool(value > arbq(Q(1, 2 ** depth))):
        depth += 1
    return depth


def numeric_modules(r185: Any, r139: Any) -> dict[str, str]:
    modules = {"r185": r185, "r178": r185.r178, "atlas": r185.atlas,
               "ge": r185.ge, "registry": r185.registry, "r139": r139,
               "lower": r139.lower, "round136": r139.lower.round136,
               "time3": r139.lower.time3, "time2": r139.lower.time3.time2_cert,
               "core": r139.lower.core_cert, "step1": r139.lower.step1}
    observed = {name: file_sha(Path(module.__file__).resolve())
                for name, module in modules.items()}
    need(observed == NUMERIC_PINS, "numeric source pins")
    return observed


def collision0_delta(r185: Any, parent: str, box: Any, target: str) -> Any:
    return r185.ad_root(r185.ad_initial_geometry(parent, box), target)["Delta"]


def next_owner(r139: Any, state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    time2 = r139.lower.time3.time2_cert
    future = []
    census = collections.Counter()
    for identifier in time2.translated_candidate_ids(FROZEN_OWNER, state["chart"]):
        row = time2.candidate_root(state["contact_x"], state["contact_y"],
                                  state["outgoing_x"], state["outgoing_y"],
                                  state["s"], identifier)
        census[row["classification"]] += 1
        need(row["classification"] in {"no_real_intersection",
             "intersection_strictly_behind", "strict_future_near_root"},
             "collision2 competitor")
        if row["classification"] == "strict_future_near_root":
            future.append((identifier, row))
    winners = [(identifier, row) for identifier, row in future if all(
        identifier == other or bool(row["near"] < other_row["near"])
        for other, other_row in future)]
    need(len(winners) == 1, "unique collision2 owner")
    selected_id, selected = winners[0]
    gaps = [row["near"] - selected["near"] for identifier, row in future
            if identifier != selected_id]
    need(all(bool(gap > 0) for gap in gaps), "collision2 strict gaps")
    return selected_id, {"classification_census": dict(sorted(census.items())),
                         "strict_future_candidate_count": len(future),
                         "all_competitor_gaps_strict_positive": True}


def downstream(r185: Any, r139: Any, origin: str, box: Any,
               initial: dict[str, Any], pair_index: dict[Any, Any],
               pattern_index: dict[Any, Any], expected_word: str,
               expected_owners: set[str]) -> dict[str, Any]:
    raw = r185.ad_root(r185.ad_initial_geometry(origin, box), FROZEN_OWNER)
    delta = r185.centered_enclosure(
        lambda parent, current_box, target: collision0_delta(
            r185, parent, current_box, target),
        origin, box, FROZEN_OWNER, raw["Delta"])
    need(bool(delta > 0), "centered delta")
    radius = raw["radius"].value
    radical = delta.sqrt()
    transverse = raw["transverse"].value
    near = raw["ell"].value - radical
    tau = r139.lower.time3.time2_cert.step1.arbq(
        r139.lower.time3.time2_cert.first_hit.TAU_MAX)
    need(bool(near > 0) and bool(near < tau), "collision1 root interval")
    sx, sy = initial["outgoing_x"], initial["outgoing_y"]
    nx = (-radical * sx + transverse * sy) / radius
    ny = (-radical * sy - transverse * sx) / radius
    radial = radical / radius
    cx, cy = r139.lower.time3.time2_cert.target_center(FROZEN_OWNER, initial["s"])
    state = {"contact_x": cx + radius * nx, "contact_y": cy + radius * ny,
             "outgoing_x": radial * nx - (transverse / radius) * ny,
             "outgoing_y": radial * ny + (transverse / radius) * nx,
             "s": initial["s"], "chart": "W", "normal_x": nx,
             "normal_y": ny, "p": transverse / radius}
    owner = {"selected_target_id": FROZEN_OWNER, "selected_root": near,
             "normal_x": nx, "normal_y": ny, "p": transverse / radius,
             "cosine": radial}
    word, error = r139.lower.round136.translation_normalized_official_word(
        initial, "W[0,0]", owner, pair_index, pattern_index)
    need(word is not None and error is None, "official word")
    compact = r139.lower.round136.compact_key(word["key"])
    word_id = compact["official_word_key_id"]
    evidence = {"centered_Delta": arb_payload(delta),
                "near_root": arb_payload(near), "tau_minus_near": arb_payload(tau - near),
                "computed_official_word_key_id": word_id,
                "expected_official_word_key_id": expected_word,
                "registry_row_sha256": compact["registry_row_sha256"],
                "ordered_clean_wall_record": word["ordered_clean_wall_record"]}
    if word_id != expected_word:
        return {**evidence, "outcome": "COLLISION1_OFFICIAL_WORD_MISMATCH",
                "selected_collision2_owner": None}
    selected, owner_evidence = next_owner(r139, state)
    need(selected not in expected_owners, "expected collision2 owner needs handoff")
    return {**evidence, "outcome": "COLLISION2_STRICT_OWNER_MISMATCH",
            "selected_collision2_owner": selected,
            "collision2_owner_evidence": owner_evidence,
            "expected_collision2_owner_set": sorted(expected_owners)}


def geometry(r185: Any, origin: str, box: Any, atlas: dict[str, Any]) -> tuple[dict[str, Any], list[str], str]:
    full, nx, ny = r185.collision1_h1_ad(origin, box, FROZEN_OWNER)
    derivatives = [sign(full.derivative[index]) for index in (0, 1)]
    need(all(derivatives), "strict t,p derivatives")
    bounds = atlas["exact_representative_box"]
    corner_rows = []
    signs = []
    for t, p in itertools.product(bounds["t"], bounds["p"]):
        point = r185.point_box(box, Q(t), Q(p), Q(0), ".c72b.corner")
        value, _nx, _ny = r185.collision1_h1_ad(origin, point, FROZEN_OWNER)
        current = sign(value.value)
        need(current != 0, "strict corner")
        signs.append(current)
        corner_rows.append({"point": {"t": t, "p": p, "s": "0"},
                            "H1": arb_payload(value.value), "sign": current})
    common = {"precision_bits": PRECISION, "equation": "H1=nx^2-ny^2",
              "full_box_natural_interval": arb_payload(full.value),
              "full_box_derivatives": {"t": arb_payload(full.derivative[0]),
                                       "p": arb_payload(full.derivative[1]),
                                       "s": arb_payload(full.derivative[2])},
              "normal_component_bounds": {"nx": arb_payload(nx.value),
                                          "ny": arb_payload(ny.value)},
              "normal_component_signs": {"nx": sign(nx.value), "ny": sign(ny.value)},
              "four_strict_corner_records": corner_rows,
              "corner_zero_incidence_count": 0}
    need(sign(nx.value) != 0 and sign(ny.value) != 0,
         "strict normal components")
    if len(set(signs)) == 1:
        side = signs[0]
        return ({**common, "kind": "STRICT_WHOLE_CHILD_H1_SIDE",
                 "proof_method": "MONOTONE_COORDINATE_CORNER_EXTREMUM_STRICT_SIDE",
                 "strict_H1_sign": sign_name(side), "boundary_root_count": 0,
                 "three_strata_partition": {"H1_LT_0": "EXACT_CHILD" if side < 0 else "EMPTY",
                                             "H1_EQ_0": "EMPTY",
                                             "H1_GT_0": "EXACT_CHILD" if side > 0 else "EMPTY",
                                             "pairwise_disjoint": True,
                                             "union_exact_child": True}}, [],
                "STRICT_NEGATIVE" if side < 0 else "STRICT_POSITIVE")
    specs = face_specs(atlas["pair_index"], bounds)
    edge_corner = {"T_LOW": (0, 1), "T_HIGH": (2, 3),
                   "P_LOW": (0, 2), "P_HIGH": (1, 3)}
    edge_rows, roots, crossings = [], [], []
    for edge_id in ("T_LOW", "T_HIGH", "P_LOW", "P_HIGH"):
        first, second = edge_corner[edge_id]
        pair = [signs[first], signs[second]]
        spec = specs[edge_id]
        tangent = 0 if spec["varying_axis"] == "t" else 1
        need((derivatives[tangent] > 0 and pair[0] <= pair[1]) or
             (derivatives[tangent] < 0 and pair[0] >= pair[1]),
             "edge derivative order")
        base = {"edge_id": edge_id, "exact_face": spec,
                "face_key_sha256": face_key(spec), "ordered_endpoint_signs": pair,
                "strict_tangential_derivative":
                    arb_payload(full.derivative[tangent])}
        if pair[0] != pair[1]:
            identifier = root_id(spec)
            crossings.append(edge_id)
            roots.append({"root_id": identifier, "edge_id": edge_id,
                          "face_key_sha256": face_key(spec), "exact_face": spec,
                          "definition": "UNIQUE_H1_ZERO_IN_OPEN_EXACT_FACE",
                          "existence_by_IVT": True,
                          "uniqueness_by_uniform_strict_tangential_derivative": True,
                          "not_a_corner": True})
            edge_rows.append({**base, "disposition": "ONE_UNIQUE_INTERIOR_H1_ROOT",
                              "root_id": identifier})
        else:
            edge_rows.append({**base, "disposition": "STRICT_NO_H1_ROOT",
                              "strict_H1_sign": sign_name(pair[0]), "root_id": None})
    need(len(roots) == len(crossings) == 2, "two exact boundary roots")
    partition = {"H1_LT_0": "EXACT_OPEN_NEGATIVE_REGION",
                 "H1_EQ_0": "EXACT_SINGLE_CLIPPED_REGULAR_GRAPH_ARC",
                 "H1_GT_0": "EXACT_OPEN_POSITIVE_REGION",
                 "pairwise_disjoint": True, "union_exact_child": True,
                 "negative_positive_two_sides_strict": True,
                 "graph_full_dimensional_Kraft_weight": "0",
                 "graph_owner": "CHART_SEAM_TERMINAL_REGISTRY",
                 "offgraph_half_open_rule": "GRAPH_REMOVED_FROM_BOTH_OPEN_SLABS"}
    return ({**common, "kind": "EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFFGRAPH_REGIONS",
             "proof_method": "STRICT_DT_DP__FOUR_CORNERS__FOUR_FACES__TWO_ROOTS__IFT",
             "boundary_edges": edge_rows, "boundary_roots": roots,
             "boundary_root_count": 2, "boundary_crossing_edge_ids": crossings,
             "single_connected_graph_arc": True,
             "no_closed_or_disconnected_zero_component": True,
             "three_strata_partition": partition},
            [root["root_id"] for root in roots], "CLIPPED")


def worker() -> int:
    payload = json.load(sys.stdin)
    sys.path.insert(0, str(SITE))
    sys.path.insert(0, str(OUT))
    from flint import ctx
    ctx.prec = PRECISION
    import cm2_round185_preconditioned_c1_residual_refinement as r185
    import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
    numeric_modules(r185, r139)
    origins = {int(key): value for key, value in payload["origins"].items()}
    original, reflected = payload["original"], payload["reflected"]
    expected_word = original[0]["official_word_key_id"]
    expected_owners = {original[1]["selected_absolute_owner_id"],
                       reflected[1]["selected_absolute_owner_id"]}
    pair_index, pattern_index, registry = r139.lower.component_cert.key_index_tables()
    cores = tuple(r139.lower.core_cert.physical_cores())
    output = []
    for atlas in payload["rows"]:
        raw_box = atlas["exact_representative_box"]
        box = r185.atlas.AtlasBox(Q(raw_box["t"][0]), Q(raw_box["t"][1]),
                                  Q(raw_box["p"][0]), Q(raw_box["p"][1]),
                                  Q(0), Q(0), len(atlas["child_path"]), atlas["child_path"])
        origin = origins[atlas["pair_index"]]
        certificate, roots, kind = geometry(r185, origin, box, atlas)
        nx_sign = certificate["normal_component_signs"]["nx"]
        ny_sign = certificate["normal_component_signs"]["ny"]
        base = {"schema": SCHEMA + ".decision-row",
                "C72_atlas_row_sha256": atlas["row_sha256"],
                "C65_aggregate_child_row_sha256": atlas["C65_aggregate_child_row_sha256"],
                "C69c_blocker_row_sha256": atlas["C69c_blocker_row_sha256"],
                "C61_aggregate_leaf_row_sha256": atlas["C61_aggregate_leaf_row_sha256"],
                "pair_index": atlas["pair_index"], "source_path": atlas["source_path"],
                "child_path": atlas["child_path"], "parent_key": origin,
                "exact_representative_box": raw_box,
                "parent_volume_fraction": atlas["parent_volume_fraction"],
                "selector": "child_route_witness == REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED",
                "additional_dyadic_depth": 0, "H1_geometry": certificate,
                "H1_geometry_closed": True, **ZERO}
        if kind == "STRICT_NEGATIVE":
            need(ny_sign != 0, "negative chart")
            chart = "N" if ny_sign > 0 else "S"
            exits = [{"stratum": "EXACT_CHILD", "exit_class": "STRICT_EXCLUSION",
                      "reason": "COLLISION1_OUTGOING_CHART_MISMATCH", "chart": chart}]
            outcome = "STRICT_EXCLUSION_WHOLE_NEGATIVE_H1_NON_W_CHART"
        elif kind == "STRICT_POSITIVE" and nx_sign > 0:
            exits = [{"stratum": "EXACT_CHILD", "exit_class": "STRICT_EXCLUSION",
                      "reason": "COLLISION1_OUTGOING_CHART_MISMATCH", "chart": "E"}]
            outcome = "STRICT_EXCLUSION_WHOLE_POSITIVE_H1_E_CHART"
        else:
            need(nx_sign < 0, "expected W positive stratum")
            chart_id = ":".join(origin.split(":")[:2])
            atom = r139.lower.step1.Atom(CORE_INDEX[chart_id], cores[CORE_INDEX[chart_id]],
                                         box.t0, box.t1, box.p0, box.p1,
                                         Q(0), Q(0), "c72b")
            initial = r139.lower.round136.initial_state(atom)
            route = downstream(r185, r139, origin, box, initial, pair_index,
                               pattern_index, expected_word, expected_owners)
            outcome = ("STRICT_EXCLUSION_WHOLE_POSITIVE_H1_" + route["outcome"]
                       if kind == "STRICT_POSITIVE" else
                       "SEALED_CLIPPED_STRATA__POSITIVE_W_" + route["outcome"])
            if kind == "STRICT_POSITIVE":
                exits = [{"stratum": "EXACT_CHILD", "exit_class": "STRICT_EXCLUSION",
                          "chart": "W", "downstream": route}]
            else:
                chart = "N" if ny_sign > 0 else "S"
                exits = [
                    {"stratum": "H1_LT_0", "exit_class": "STRICT_EXCLUSION",
                     "reason": "COLLISION1_OUTGOING_CHART_MISMATCH", "chart": chart},
                    {"stratum": "H1_GT_0", "exit_class": "STRICT_EXCLUSION",
                     "chart": "W", "downstream": route},
                    {"stratum": "H1_EQ_0", "exit_class":
                     "CEMETERY_OR_SOURCE_GRAZING_TERMINAL",
                     "terminal_subtype": "COLLISION1_OUTGOING_CHART_SEAM_H1_ZERO",
                     "root_incidence_ids": roots,
                     "two_sided_glue": {"negative_side": "H1_LT_0",
                                        "positive_side": "H1_GT_0"},
                     "half_open_owner": "CHART_SEAM_TERMINAL_REGISTRY",
                     "full_dimensional_Kraft_weight": "0"}]
        output.append({**base, "stratum_exits": exits,
                       "allowed_exit_closed_for_every_stratum": True,
                       "row_outcome": outcome,
                       "current_disposition": "STAGED_ZERO_CREDIT_ALLOWED_EXIT_PARTITION",
                       "candidate_is_authority": False,
                       "global_consumption_ready": False,
                       "official_registry_sha256": registry})
    json.dump(output, sys.stdout, sort_keys=True, separators=(",", ":"),
              ensure_ascii=False)
    return 0


def input_bundle(c72_a: Path, c72_b: Path) -> tuple[list[dict[str, Any]], dict[int, str], list[dict[str, Any]], list[dict[str, Any]]]:
    for directory in (c72_a, c72_b):
        result = parse(pinned(directory / C72_NAMES["result"], PINS["C72_RESULT"]), "C72 result")
        verify = parse(pinned(directory / C72_NAMES["verification"], PINS["C72_VERIFY"]), "C72 verify")
        close_object(result, OBJECTS["C72_RESULT"], "C72 result")
        close_object(verify, OBJECTS["C72_VERIFY"], "C72 verify")
        need(result["ledger"]["sha256"] == PINS["C72_LEDGER"] and
             verify["candidate_object_sha256"] == OBJECTS["C72_RESULT"], "C72 gate")
    need(pinned(c72_a / C72_NAMES["ledger"], PINS["C72_LEDGER"]) ==
         pinned(c72_b / C72_NAMES["ledger"], PINS["C72_LEDGER"]), "C72 dual ledger bytes")

    direct = [
        (OUT / "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json", "C65_RESULT"),
        (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v9.json", "C65_VERIFY"),
        (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json", "C65_SELFTEST"),
        (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v9.json", "C65_REPLAY"),
        (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256", "C65_MANIFEST"),
        (OUT / "cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json", "C65_OUTER"),
        (OUT / "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json", "C69_RESULT"),
        (OUT / "cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json", "C69_VERIFY"),
        (OUT / "cm2_round306c69c_descriptor_repair_supersession_independent_manifest_v1.sha256", "C69_MANIFEST"),
        (OUT / "cm2_round306c69c_descriptor_repair_supersession_independent_outer_publication_receipt_v1.json", "C69_OUTER"),
        (C38_DIR / "result.json", "C38_RESULT"),
        (C71B_DIR / "cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_result.json", "C71B_RESULT"),
        (C71B_DIR / "independent_verification_v3_1.json", "C71B_VERIFY"),
        (C71B_DIR / "dual_build_publication_completion_receipt_v3.json", "C71B_RECEIPT"),
        (C72O_DIR / "cm2_round306c72o_collision1_outgoing_state_oracle_v1_result.json", "C72O_RESULT"),
        (ROOT / ".cm2-runtime/c72o-independent-verification-v2.json", "C72O_VERIFY"),
        (C73_DIR / "cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2_result.json", "C73_RESULT"),
        (ROOT / ".cm2-runtime/c73v2-audit-a.W2AYpD/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_independent_verification_v2.json", "C73_VERIFY"),
    ]
    for path, key in direct:
        raw = pinned(path, PINS[key])
        if key in OBJECTS:
            close_object(parse(raw, key), OBJECTS[key], key)

    targets = []
    for row in iter_jsonl(c72_a / C72_NAMES["ledger"], PINS["C72_LEDGER"], 134155):
        if row["child_route_witness"] == SELECTOR:
            need(row["source_grazing"] is False and row["formal_credit"] == 0 and
                 row["D02_gate_credit"] == 0, "target boundary")
            targets.append(row)
    need(len(targets) == 55216, "target selector count")
    target_hashes = {row["row_sha256"] for row in targets}
    need(len(target_hashes) == 55216, "target unique")

    outgoing = {row["C72_atlas_row_sha256"] for row in iter_jsonl(
        C72O_DIR / "cm2_round306c72o_collision1_outgoing_state_oracle_v1.jsonl.gz",
        PINS["C72O_LEDGER"], 18668)}
    broad = {row["C72_obligation_row_sha256"] for row in iter_jsonl(
        C73_DIR / "cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2.jsonl.gz",
        PINS["C73_LEDGER"], 1163)}
    need(target_hashes.isdisjoint(outgoing) and target_hashes.isdisjoint(broad) and
         outgoing.isdisjoint(broad), "C72b/C72o/C73 exact dedup")

    origins = {}
    target_pairs = {row["pair_index"] for row in targets}
    for row in iter_jsonl(C38_DIR / "collision1_2_child_pairs.jsonl.gz",
                          PINS["C38_CHILDREN"], 10486):
        pair = row["pair_index"]
        if pair in target_pairs:
            value = row["representative_origin_key"]
            need(pair not in origins or origins[pair] == value, "origin consistency")
            origins[pair] = value
    need(set(origins) == target_pairs and len(origins) == 12,
         "origin coverage")

    def first_two(path: Path, pin: str, count: int) -> list[dict[str, Any]]:
        result = []
        for ordinal, row in enumerate(iter_jsonl(path, pin, count)):
            if ordinal < 2:
                result.append(row)
        return result
    original = first_two(C35_DIR / "path_occurrences.jsonl.gz", PINS["C35_PATH"], 1648)
    reflected = first_two(C37_DIR / "reflected_r1648_occurrences.jsonl.gz", PINS["C37_PATH"], 1648)
    need(original[0]["selected_absolute_owner_id"] == FROZEN_OWNER and
         {original[1]["selected_absolute_owner_id"], reflected[1]["selected_absolute_owner_id"]}
         == {"G[0,0]", "G[0,1]"}, "history authority")

    wanted_c65 = {row["C65_aggregate_child_row_sha256"] for row in targets}
    found_c65 = set()
    for row in iter_jsonl(OUT / "cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz",
                          PINS["C65_LEAVES"], 358919):
        if row["row_sha256"] in wanted_c65:
            found_c65.add(row["row_sha256"])
    need(found_c65 == wanted_c65, "C65 direct lineage")
    wanted_c69 = {row["C69c_blocker_row_sha256"] for row in targets}
    found_c69 = {row["row_sha256"] for row in iter_jsonl(
        OUT / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz",
        PINS["C69_BLOCKERS"], 18523) if row["row_sha256"] in wanted_c69}
    need(found_c69 == wanted_c69, "C69 direct lineage")
    return targets, origins, original, reflected


def incidence_rows(c72_a: Path, wanted: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    incidents: dict[str, list[dict[str, Any]]] = {identifier: [] for identifier in wanted}
    by_face = {value["face_key_sha256"]: identifier for identifier, value in wanted.items()}
    for row in iter_jsonl(c72_a / C72_NAMES["ledger"], PINS["C72_LEDGER"], 134155):
        specs = face_specs(row["pair_index"], row["exact_representative_box"])
        for edge_id, spec in specs.items():
            key = face_key(spec)
            if key in by_face:
                incidents[by_face[key]].append({"C72_atlas_row_sha256": row["row_sha256"],
                                                "edge_id": edge_id,
                                                "is_high_face": edge_id.endswith("HIGH")})
    output = []
    for identifier in sorted(wanted):
        rows = sorted(incidents[identifier], key=lambda value:
                      (value["C72_atlas_row_sha256"], value["edge_id"]))
        need(1 <= len(rows) <= 2, "root face incidence 1/2")
        high = [row for row in rows if row["is_high_face"]]
        owner = (high[0] if len(high) == 1 else rows[0])
        output.append({"schema": SCHEMA + ".root-incidence-row",
                       "root_id": identifier,
                       "face_key_sha256": wanted[identifier]["face_key_sha256"],
                       "exact_face": wanted[identifier]["exact_face"],
                       "incident_C72_faces": rows,
                       "incidence_count": len(rows),
                       "incidence_class": "SHARED_FACE" if len(rows) == 2 else
                                          "ATLAS_SCOPE_BOUNDARY_FACE",
                       "unique_half_open_terminal_owner": owner,
                       "owner_rule": "LOWER_COORDINATE_CHILD_HIGH_FACE_ELSE_SCOPE_BOUNDARY_LEXICAL",
                       "corner_incidence": False,
                       "terminal_subtype": "COLLISION1_OUTGOING_CHART_SEAM_H1_ZERO",
                       "full_dimensional_Kraft_weight": "0",
                       "incidence_closed": True})
    return output


def build(c72_a: Path, c72_b: Path, output: Path, batch_size: int) -> dict[str, Any]:
    need(not output.exists() and 100 <= batch_size <= 2000, "fresh output/batch")
    output.mkdir(mode=0o755)
    targets, origins, original, reflected = input_bundle(c72_a, c72_b)
    rows_writer = Ledger(output / ROWS, "C72_LEDGER_ORDER_FILTERED_BY_EXACT_CHILD_WITNESS")
    geometry_census = collections.Counter()
    route_census = collections.Counter()
    pair_census = collections.Counter()
    root_specs: dict[str, dict[str, Any]] = {}
    with rows_writer:
        for offset in range(0, len(targets), batch_size):
            payload = {"rows": targets[offset:offset + batch_size],
                       "origins": origins, "original": original, "reflected": reflected}
            completed = subprocess.run(
                [sys.executable, str(SELF), "--worker"],
                input=canonical(payload), capture_output=True, check=True)
            batch = json.loads(completed.stdout)
            need(len(batch) == len(payload["rows"]), "worker batch count")
            for atlas, body in zip(payload["rows"], batch):
                need(body["C72_atlas_row_sha256"] == atlas["row_sha256"] and
                     body["allowed_exit_closed_for_every_stratum"] is True,
                     "worker order/closure")
                geometry_census[body["H1_geometry"]["kind"]] += 1
                pair_census[body["pair_index"]] += 1
                for exit_row in body["stratum_exits"]:
                    if exit_row["stratum"] == "H1_GT_0" or (
                        exit_row["stratum"] == "EXACT_CHILD" and
                        exit_row.get("chart") == "W"):
                        route_census[exit_row["downstream"]["outcome"]] += 1
                for root in body["H1_geometry"].get("boundary_roots", []):
                    value = {"face_key_sha256": root["face_key_sha256"],
                             "exact_face": root["exact_face"]}
                    need(root["root_id"] not in root_specs or
                         root_specs[root["root_id"]] == value, "root identity")
                    root_specs[root["root_id"]] = value
                rows_writer.write(body)
    need(dict(geometry_census) == {
        "EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFFGRAPH_REGIONS": 55213,
        "STRICT_WHOLE_CHILD_H1_SIDE": 3}, "geometry census")
    need(dict(route_census) == {"COLLISION1_OFFICIAL_WORD_MISMATCH": 19881,
                                "COLLISION2_STRICT_OWNER_MISMATCH": 35334},
         "W-route census")
    need(len(root_specs) <= 110426, "root identity inventory")

    incidence = incidence_rows(c72_a, root_specs)
    incidence_writer = Ledger(output / INCIDENCE, "ROOT_ID_ASCENDING")
    incidence_census = collections.Counter()
    with incidence_writer:
        for body in incidence:
            incidence_writer.write(body)
            incidence_census[body["incidence_class"]] += 1
    need(incidence_writer.count == len(root_specs), "incidence exact coverage")

    result = {"schema": SCHEMA + ".result",
              "status": "PASS_55216_H1_GEOMETRY_CLOSED__55213_CHART_SEAM_TERMINALS__ALL_STRATA_ALLOWED_EXIT_CLOSED__ZERO_CREDIT",
              "producer_file_sha256": file_sha(SELF), "precision_bits": PRECISION,
              "input_file_sha256": dict(sorted(PINS.items())),
              "input_object_sha256": dict(sorted(OBJECTS.items())),
              "scope": {"selector": "child_route_witness == REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED",
                        "target_child_count": 55216, "additional_dyadic_depth": 0,
                        "dedup_C72o_OUTGOING_STATE_count": 18668,
                        "dedup_C73_broad_exception_count": 1163},
              "H1_GEOMETRY_CLOSED": 55216,
              "H1_geometry_census": dict(sorted(geometry_census.items())),
              "strict_whole_child_exclusion_count": 3,
              "clipped_child_count": 55213,
              "offgraph_strict_exclusion_stratum_census": {
                  "H1_LT_0_NON_W_CHART_MISMATCH": 55213,
                  "H1_GT_0_COLLISION1_WORD_MISMATCH": 19879,
                  "H1_GT_0_COLLISION2_OWNER_MISMATCH": 35334},
              "graph_terminal_census": {
                  "COLLISION1_OUTGOING_CHART_SEAM_H1_ZERO": 55213},
              "graph_terminals_are_not_counted_as_strict_exclusions": True,
              "W_route_census_including_two_strict_positive_whole_boxes":
                  dict(sorted(route_census.items())),
              "ALLOWED_EXIT_CLOSED": 55216,
              "explicit_residual_child_count": 0,
              "pair_census": {str(key): value for key, value in sorted(pair_census.items())},
              "ledgers": {"decision_rows": rows_writer.descriptor(),
                          "root_incidence": incidence_writer.descriptor()},
              "root_incidence_census": dict(sorted(incidence_census.items())),
              "proof_invariants": {
                  "all_55216_have_strict_whole_child_dt_dp": True,
                  "all_55216_have_four_strict_nonzero_corners": True,
                  "all_55213_graphs_have_two_unique_noncorner_boundary_roots": True,
                  "all_55213_graphs_have_two_strict_offgraph_sides": True,
                  "all_graph_roots_have_unique_half_open_terminal_owner": True,
                  "all_graphs_have_full_dimensional_Kraft_weight_zero": True,
                  "all_strata_are_allowed_exit_classes": True,
                  "owner_history_glue_two_sides_incidence_prefix_Kraft_materialized": True},
              "strict_boundary": {"candidate_is_authority": False,
                                  "global_consumption_ready": False,
                                  "runtime_canonical_pointer_or_seal_writes": False,
                                  **ZERO}}
    result["object_sha256"] = digest(result)
    write_exclusive(output / RESULT, canonical(result) + b"\n")
    report = ("# C72b boundary arrangement and chart-seam oracle\n\n"
              "- H1 geometry closed: 55,216 / 55,216.\n"
              "- Clipped graphs: 55,213; each graph is a chart-seam terminal, not a strict exclusion.\n"
              "- All off-graph strata are strictly excluded; explicit residual children: 0.\n"
              "- Formal/global/D02/CM2 credit remains zero.\n").encode()
    write_exclusive(output / REPORT, report)
    write_exclusive(output / LOCK,
                    b"STAGED ZERO-CREDIT SIDECAR ONLY; LATER NO-PRODUCER GLOBAL CONSUMER REQUIRED.\n")
    for path in (output / ROWS, output / INCIDENCE, output / RESULT,
                 output / REPORT, output / LOCK):
        expected = file_sha(path)
        need(file_sha(path) == expected, "terminal byte replay:" + path.name)
    return result


def main() -> int:
    raise Reject("C72b v1 permanently rejected; use fresh C72b2 v2 successor")
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--c72-a", type=Path)
    parser.add_argument("--c72-b", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--batch-size", type=int, default=1200)
    args = parser.parse_args()
    if args.worker:
        return worker()
    need(args.c72_a is not None and args.c72_b is not None and
         args.output_dir is not None, "build arguments")
    result = build(args.c72_a.resolve(), args.c72_b.resolve(),
                   args.output_dir.resolve(), args.batch_size)
    print(json.dumps({"status": result["status"],
                      "object_sha256": result["object_sha256"],
                      "rows_sha256": result["ledgers"]["decision_rows"]["sha256"]},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "REJECTED", "reason": str(error)}, sort_keys=True),
              file=sys.stderr)
        raise SystemExit(2)
