#!/usr/bin/env python3
"""Exact zero-credit oracle for every C72 child with OUTGOING_STATE witness.

The old route reconstructed the collision-one radial factor as ``sqrt(1-p^2)``
after forming the interval ``p``.  On the target boxes that dependency-expanded
quantity was not strictly positive even though the already selected collision
root had a strictly positive discriminant.  This oracle keeps the input boxes
unchanged and reconstructs the radial factor as ``sqrt(Delta)/R`` from a
centered mean-value enclosure of that same discriminant.  It separately proves
the frozen W outgoing chart from centered H1 and a strict negative nx margin,
then resumes the exact official-word / next-owner route.

No upstream producer is imported or executed.  Published/staged upstream data
are consumed as inert pinned bytes.  Only the pinned numerical certificate
modules are imported.  Outputs are deterministic, zero-credit, and created in
a new caller-supplied directory with no-replace semantics.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
from dataclasses import dataclass
from fractions import Fraction as Q
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Iterator, Mapping
import zlib

from flint import arb, ctx

import cm2_round185_preconditioned_c1_residual_refinement as r185
import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139


ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
SELF = Path(__file__).resolve()
SCHEMA = "cm2.round306c72o.collision1-outgoing-state-oracle.v1"
PREFIX = "cm2_round306c72o_collision1_outgoing_state_oracle_v1"
LEDGER_NAME = PREFIX + ".jsonl.gz"
RESULT_NAME = PREFIX + "_result.json"
REPORT_NAME = PREFIX + "_report.md"
LOCK_NAME = "ZERO_CREDIT_STAGED_OUTGOING_ORACLE_ONLY.lock"
PRECISION_BITS = 384
FROZEN_OWNER = "W[1,0]"
CORE_INDEX = {"W:E": 14, "W:N": 17, "W:S": 20, "W:W": 23}

C38_DIR = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C35_DIR = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C37_DIR = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"

C72_FILES = {
    "result": PREFIX.replace("c72o_collision1_outgoing_state_oracle", "c72_structural_child_obligation_atlas") + "_result.json",
    "ledger": PREFIX.replace("c72o_collision1_outgoing_state_oracle", "c72_structural_child_obligation_atlas") + ".jsonl.gz",
    "verification": "cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json",
}

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
    "C35_RESULT": "3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
    "C35_PATH": "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66",
    "C37_RESULT": "5b968d957cbca2a4f8aec855a44643f5add7fe0244d933401dfdef9ad7be61f3",
    "C37_PATH": "7c87829f6ef883b7928ff8a313d5bfcf240383c51a9040739de1cfe7e617bef5",
}

OBJECT_PINS = {
    "C72_RESULT": "a6aa0cfd8e1ee1b7a02d92af066acb23abffb22b0b7276b7e233d2ff7d92f9f4",
    "C72_VERIFY": "8ae20b71916ee1f6d1d28e633b1fbc080f4cb277eed7b6bb54937f8538ae7994",
    "C65_RESULT": "79185dbca48f0d228977a006583eb545525cff2d9418160fb190c1f9c5b6c393",
    "C65_VERIFY": "8b8c1c64adf5485709b68e904bfb935f552539c53771ff5dd7b5a5f3ac1987ba",
    "C65_SELFTEST": "540654f9f959f13a25d664e404655fa2570c67a7e1e9e4e6e0022c601a7007d1",
    "C65_REPLAY": "9bd2c1c378066f5e4fb5c86bc83caee721962001c666c7187c9e39693fed7327",
    "C65_OUTER": "5e7e21d9be14fa52ec5e3663bd9863ac023e8beffe8e80dc28925aaeb3ed074d",
    "C69_RESULT": "e52904a7d8ba73c855e69e390cd3cf29c233ffe492e6fae74efdf0b6d4d0a6a5",
    "C69_VERIFY": "fd25accfd8c5669d13a09b5f335ae265a751a1fb7f069ac21c64e069a0fc2b29",
    "C69_OUTER": "921a5b16d4102b356f1e2e903a71df5e872c869caa668903bb210fe0dbfed1f3",
    "C38_RESULT": "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434",
    "C35_RESULT": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C37_RESULT": "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b",
}

NUMERIC_SOURCE_PINS = {
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

EXPECTED_SOURCE_CENSUS = {
    "COLLISION1_OUTGOING_STATE": 423,
    "REGULAR_BOUNDARY_ARRANGEMENT": 18_245,
}
EXPECTED_OUTCOME_CENSUS = {
    "STRICT_EXCLUSION_COLLISION1_WORD_MISMATCH": 8_321,
    "STRICT_EXCLUSION_COLLISION2_OWNER_MISMATCH": 10_347,
}
EXPECTED_SELECTED_OWNER_CENSUS = {"W[1,-1]": 5_851, "W[1,1]": 4_496}


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


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate key:" + key)
        result[key] = value
    return result


def parse_line(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         label + ":framing")
    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=no_duplicates,
                       parse_constant=lambda token: (_ for _ in ()).throw(Reject(token)))
    need(type(value) is dict and canonical(value) == raw, label + ":canonical")
    return value


def close_row(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":row closure")


def close_object(value: Mapping[str, Any], expected: str, label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(claim == expected and claim == digest(body), label + ":object closure")


@dataclass(frozen=True)
class Identity:
    dev: int
    ino: int
    mode: int
    nlink: int
    size: int
    mtime_ns: int
    ctime_ns: int


def identity(value: os.stat_result) -> Identity:
    return Identity(value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                    value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def open_regular(path: Path) -> tuple[int, Identity]:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                         getattr(os, "O_NOFOLLOW", 0))
    first = os.fstat(descriptor)
    need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1,
         "regular single-link:" + str(path))
    return descriptor, identity(first)


def finish_read(path: Path, descriptor: int, first: Identity,
                observed: str, expected: str) -> None:
    need(identity(os.fstat(descriptor)) == first ==
         identity(os.stat(path, follow_symlinks=False)), "TOCTOU:" + str(path))
    need(observed == expected, "file pin:" + str(path))


def secure_bytes(path: Path, expected: str, maximum: int = 16 << 20) -> bytes:
    descriptor, first = open_regular(path)
    try:
        payload = bytearray()
        hasher = hashlib.sha256()
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
            payload.extend(block)
            need(len(payload) <= maximum, "bounded read:" + str(path))
        finish_read(path, descriptor, first, hasher.hexdigest(), expected)
        return bytes(payload)
    finally:
        os.close(descriptor)


def secure_json(path: Path, expected_file: str, expected_object: str) -> dict[str, Any]:
    raw = secure_bytes(path, expected_file)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "JSON newline:" + str(path))
    value = parse_line(raw[:-1], str(path))
    close_object(value, expected_object, str(path))
    return value


def iter_secure_jsonl(path: Path, expected: str, rows: int,
                      maximum_uncompressed: int = 1 << 30) -> Iterator[dict[str, Any]]:
    descriptor, first = open_regular(path)
    hasher = hashlib.sha256()
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    pending = bytearray()
    count = 0
    expanded = 0
    try:
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
            decoded = decoder.decompress(block)
            expanded += len(decoded)
            need(expanded <= maximum_uncompressed, "gzip expansion:" + str(path))
            pending.extend(decoded)
            while True:
                newline = pending.find(b"\n")
                if newline < 0:
                    break
                raw = bytes(pending[:newline])
                del pending[:newline + 1]
                value = parse_line(raw, f"{path}:{count + 1}")
                close_row(value, f"{path}:{count + 1}")
                count += 1
                yield value
        pending.extend(decoder.flush())
        need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
             "single gzip member:" + str(path))
        need(not pending and count == rows, "JSONL closure:" + str(path))
        finish_read(path, descriptor, first, hasher.hexdigest(), expected)
    finally:
        os.close(descriptor)


def file_sha256(path: Path) -> str:
    descriptor, first = open_regular(path)
    hasher = hashlib.sha256()
    try:
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
        need(identity(os.fstat(descriptor)) == first ==
             identity(os.stat(path, follow_symlinks=False)), "hash TOCTOU:" + str(path))
        return hasher.hexdigest()
    finally:
        os.close(descriptor)


def numeric_source_pins() -> dict[str, str]:
    modules = {
        "r185": r185, "r178": r185.r178, "atlas": r185.atlas,
        "ge": r185.ge, "registry": r185.registry, "r139": r139,
        "lower": r139.lower, "round136": r139.lower.round136,
        "time3": r139.lower.time3, "time2": r139.lower.time3.time2_cert,
        "core": r139.lower.core_cert, "step1": r139.lower.step1,
    }
    observed = {name: file_sha256(Path(module.__file__).resolve())
                for name, module in modules.items()}
    need(observed == NUMERIC_SOURCE_PINS, "numeric source pins")
    need(getattr(sys.modules["flint"], "__version__", None) == "0.9.0", "flint version")
    return observed


def exact_dyadic(point: arb) -> Q:
    mantissa, exponent = point.man_exp()
    return Q(int(mantissa)) * (Q(2) ** int(exponent))


def power_two(exponent: int) -> Q:
    return Q(2 ** exponent) if exponent >= 0 else Q(1, 2 ** (-exponent))


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def strict_depth(value: arb) -> int:
    lower = exact_dyadic(value.lower())
    need(lower > 0, "strict positive margin")
    exponent = lower.numerator.bit_length() - lower.denominator.bit_length()
    while power_two(exponent) > lower:
        exponent -= 1
    while power_two(exponent + 1) <= lower:
        exponent += 1
    if lower == power_two(exponent):
        exponent -= 1
    depth = -exponent
    need(bool(value > r139.lower.step1.arbq(power_two(-depth))),
         "dyadic margin replay")
    return depth


def box_from_row(row: Mapping[str, Any]) -> Any:
    box = row["exact_representative_box"]
    return r185.atlas.AtlasBox(
        Q(box["t"][0]), Q(box["t"][1]), Q(box["p"][0]), Q(box["p"][1]),
        Q(box["s"][0]), Q(box["s"][1]), len(row["child_path"]), row["child_path"],
    )


def centered_delta(parent_key: str, box: Any) -> tuple[Any, arb]:
    raw = r185.ad_root(r185.ad_initial_geometry(parent_key, box), FROZEN_OWNER)
    centered = r185.centered_enclosure(
        r185.collision0_delta_ad, parent_key, box, FROZEN_OWNER, raw["Delta"]
    )
    need(bool(centered > 0), "centered Delta positive")
    return raw, centered


def centered_w_chart(parent_key: str, box: Any) -> tuple[arb, arb]:
    full, nx, _ny = r185.collision1_h1_ad(parent_key, box, FROZEN_OWNER)
    h1 = r185.centered_enclosure(
        r185.collision1_h1_ad, parent_key, box, FROZEN_OWNER, full
    )
    need(bool(h1 > 0) and bool(nx.value < 0), "centered strict W chart")
    return h1, -nx.value


def collision1_owner_and_state(parent_key: str, box: Any, atom: Any,
                               state: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, int]]:
    raw, delta = centered_delta(parent_key, box)
    target = FROZEN_OWNER
    radius = raw["radius"].value
    radical = delta.sqrt()
    transverse = raw["transverse"].value
    near = raw["ell"].value - radical
    need(bool(near > 0), "collision1 near positive")
    tau = r139.lower.time3.time2_cert.step1.arbq(
        r139.lower.time3.time2_cert.first_hit.TAU_MAX
    )
    need(bool(near < tau), "collision1 near below tau")
    nx = (-radical * state["outgoing_x"] +
          transverse * state["outgoing_y"]) / radius
    ny = (-radical * state["outgoing_y"] -
          transverse * state["outgoing_x"]) / radius
    p = transverse / radius
    radial = radical / radius
    h1, minus_nx = centered_w_chart(parent_key, box)
    need(bool(radial > 0), "radial positive")
    cx, cy = r139.lower.time3.time2_cert.target_center(target, state["s"])
    outgoing = {
        "contact_x": cx + radius * nx,
        "contact_y": cy + radius * ny,
        "outgoing_x": radial * nx - p * ny,
        "outgoing_y": radial * ny + p * nx,
        "s": state["s"], "chart": "W", "normal_x": nx,
        "normal_y": ny, "p": p,
    }
    owner = {
        "selected_target_id": target, "selected_root": near,
        "normal_x": nx, "normal_y": ny, "p": p, "cosine": radial,
    }
    margins = {
        "centered_Delta": strict_depth(delta),
        "radial_Delta_over_R2": strict_depth(delta / (radius * radius)),
        "centered_H1": strict_depth(h1),
        "negative_nx": strict_depth(minus_nx),
        "near_root": strict_depth(near),
        "tau_minus_near": strict_depth(tau - near),
    }
    return owner, outgoing, margins


def strict_next_owner(state: dict[str, Any], current: str) -> tuple[dict[str, Any], dict[str, Any]]:
    time2 = r139.lower.time3.time2_cert
    qx, qy = state["contact_x"], state["contact_y"]
    ux, uy, s = state["outgoing_x"], state["outgoing_y"], state["s"]
    candidates = list(time2.translated_candidate_ids(current, state["chart"]))
    counts: Counter[str] = Counter()
    future: list[tuple[str, dict[str, Any]]] = []
    for identifier in candidates:
        row = time2.candidate_root(qx, qy, ux, uy, s, identifier)
        kind = row["classification"]
        need(kind in {"no_real_intersection", "intersection_strictly_behind",
                      "strict_future_near_root"}, "collision2 unresolved competitor")
        counts[kind] += 1
        if kind == "strict_future_near_root":
            future.append((identifier, row))
    winners = [(identifier, row) for identifier, row in future if all(
        identifier == other or bool(row["near"] < other_row["near"])
        for other, other_row in future
    )]
    need(len(winners) == 1, "collision2 strict unique owner")
    selected_id, selected = winners[0]
    gaps = [other["near"] - selected["near"] for identifier, other in future
            if identifier != selected_id]
    need(all(bool(gap > 0) for gap in gaps), "collision2 order gaps")
    tau = time2.step1.arbq(time2.first_hit.TAU_MAX)
    need(bool(selected["near"] < tau), "collision2 tau")
    radius, radical, transverse = (
        selected["radius"], selected["radical"], selected["transverse"]
    )
    nx = (-radical * ux + transverse * uy) / radius
    ny = (-radical * uy - transverse * ux) / radius
    owner = {
        "selected_target_id": selected_id, "selected_root": selected["near"],
        "normal_x": nx, "normal_y": ny, "p": transverse / radius,
        "time2_target_chart_id": f"{current[0]}:{state['chart']}",
    }
    evidence = {
        "retained_candidate_count": len(candidates),
        "classification_census": dict(sorted(counts.items())),
        "strict_future_candidate_count": len(future),
        "selected_root_dyadic_depth": strict_depth(selected["near"]),
        "selected_tau_margin_dyadic_depth": strict_depth(tau - selected["near"]),
        "minimum_root_order_gap_dyadic_depth": (
            max(strict_depth(gap) for gap in gaps) if gaps else None
        ),
    }
    return owner, evidence


def read_authorities(c72_dir: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]],
                                                    dict[str, dict[str, Any]], dict[int, dict[str, str]],
                                                    list[dict[str, Any]], list[dict[str, Any]], dict[str, str]]:
    c72_result = secure_json(c72_dir / C72_FILES["result"], PINS["C72_RESULT"],
                             OBJECT_PINS["C72_RESULT"])
    c72_verify = secure_json(c72_dir / C72_FILES["verification"], PINS["C72_VERIFY"],
                             OBJECT_PINS["C72_VERIFY"])
    need(c72_result["ledger"]["sha256"] == PINS["C72_LEDGER"] and
         c72_result["ledger"]["row_count"] == 134_155, "C72 ledger descriptor")
    need(c72_verify["candidate_object_sha256"] == OBJECT_PINS["C72_RESULT"],
         "C72 independent verification binding")
    targets: list[dict[str, Any]] = []
    source_census: Counter[str] = Counter()
    for row in iter_secure_jsonl(c72_dir / C72_FILES["ledger"], PINS["C72_LEDGER"], 134_155):
        if row["child_route_witness"] == "OUTGOING_STATE":
            need(row["child_route_classification"] ==
                 "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE",
                 "C72 target classification")
            targets.append(row)
            source_census[row["structural_category"]] += 1
    need(len(targets) == 18_668 and dict(source_census) == EXPECTED_SOURCE_CENSUS,
         "C72 capability census")

    c65_result = secure_json(DELIVERABLES / "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json",
                             PINS["C65_RESULT"], OBJECT_PINS["C65_RESULT"])
    c69_result = secure_json(DELIVERABLES / "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json",
                             PINS["C69_RESULT"], OBJECT_PINS["C69_RESULT"])
    need(c65_result["ledgers"]["aggregate_leaves"]["row_count"] == 358_919,
         "C65 census")
    need(c69_result["ledgers"]["blockers"]["row_count"] == 18_523, "C69 census")
    wanted_c65 = {row["C65_aggregate_child_row_sha256"] for row in targets}
    wanted_c69 = {row["C69c_blocker_row_sha256"] for row in targets}
    c65: dict[str, dict[str, Any]] = {}
    for row in iter_secure_jsonl(
        DELIVERABLES / "cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz",
        PINS["C65_LEAVES"], 358_919,
    ):
        if row["row_sha256"] in wanted_c65:
            c65[row["row_sha256"]] = row
    c69: dict[str, dict[str, Any]] = {}
    for row in iter_secure_jsonl(
        DELIVERABLES / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz",
        PINS["C69_BLOCKERS"], 18_523,
    ):
        if row["row_sha256"] in wanted_c69:
            c69[row["row_sha256"]] = row
    need(set(c65) == wanted_c65 and set(c69) == wanted_c69, "lineage row inventory")

    c38_result = secure_json(C38_DIR / "result.json", PINS["C38_RESULT"],
                             OBJECT_PINS["C38_RESULT"])
    need(c38_result["ledgers"]["collision1_2_child_pairs"]["sha256"] == PINS["C38_CHILDREN"],
         "C38 descriptor")
    target_pairs = {row["pair_index"] for row in targets}
    origins: dict[int, dict[str, str]] = {}
    for row in iter_secure_jsonl(C38_DIR / "collision1_2_child_pairs.jsonl.gz",
                                 PINS["C38_CHILDREN"], 10_486):
        pair = row["pair_index"]
        if pair not in target_pairs:
            continue
        current = {
            "parent_key": row["representative_origin_key"],
            "representative_cell_id": row["representative_cell_id"],
            "representative_parent_row_sha256": row["representative_parent_row_sha256"],
        }
        need(pair not in origins or origins[pair] == current, "C38 origin consistency")
        origins[pair] = current
    need(set(origins) == target_pairs and len(origins) == 12, "C38 target origins")

    c35_result = secure_json(C35_DIR / "result.json", PINS["C35_RESULT"],
                             OBJECT_PINS["C35_RESULT"])
    c37_result = secure_json(C37_DIR / "result.json", PINS["C37_RESULT"],
                             OBJECT_PINS["C37_RESULT"])
    original: list[dict[str, Any]] = []
    for index, row in enumerate(iter_secure_jsonl(C35_DIR / "path_occurrences.jsonl.gz",
                                                  PINS["C35_PATH"], 1_648)):
        if index < 2:
            original.append(row)
    reflected: list[dict[str, Any]] = []
    for index, row in enumerate(iter_secure_jsonl(C37_DIR / "reflected_r1648_occurrences.jsonl.gz",
                                                  PINS["C37_PATH"], 1_648)):
        if index < 2:
            reflected.append(row)
    need(len(original) == len(reflected) == 2, "event prefix")
    need(original[0]["row_sha256"] == "815af4b7fd77b884f70178c9a706de9be94be219b66488c9da48fe7b470b8250" and
         original[0]["selected_absolute_owner_id"] == FROZEN_OWNER and
         original[0]["outgoing_chart"] == "W", "collision1 event authority")
    need({original[1]["selected_absolute_owner_id"], reflected[1]["selected_absolute_owner_id"]}
         == {"G[0,1]", "G[0,0]"}, "collision2 expected owner set")
    authority_hashes = {
        "C35_collision1_event_row_sha256": original[0]["row_sha256"],
        "C35_collision2_event_row_sha256": original[1]["row_sha256"],
        "C37_reflected_collision2_event_row_sha256": reflected[1]["row_sha256"],
    }
    return targets, c65, c69, origins, original, reflected, authority_hashes


def validate_lineage(atlas: dict[str, Any], c65: dict[str, Any],
                     c69: dict[str, Any], event_row_sha: str) -> None:
    need(c65["row_sha256"] == atlas["C65_aggregate_child_row_sha256"], "C65 row hash")
    need(c69["row_sha256"] == atlas["C69c_blocker_row_sha256"], "C69 row hash")
    for name in ("pair_index", "source_path"):
        need(c65[name] == atlas[name], "C65 atlas " + name)
    need(c65["path"] == atlas["child_path"] and
         c65["exact_representative_box"] == atlas["exact_representative_box"],
         "C65 atlas child box")
    need(c65["source_C61_aggregate_leaf_row_sha256"] ==
         atlas["C61_aggregate_leaf_row_sha256"], "C65 C61 lineage")
    need(c69["C61_aggregate_leaf_row_sha256"] ==
         atlas["C61_aggregate_leaf_row_sha256"] and
         c69["path"] == atlas["source_path"] and
         c69["pair_index"] == atlas["pair_index"], "C69 atlas lineage")
    need(c69["structural_graph_kind"] == atlas["structural_category"],
         "C69 structural category")
    continuation = c65["continuation"]
    need(type(continuation) is dict and
         continuation["collision1_original_owner"] == FROZEN_OWNER and
         continuation["collision1_history_row_sha256"] == event_row_sha and
         continuation["collision1_event_order"]["outgoing_chart"] == "W" and
         continuation["exact_representative_box"] == atlas["exact_representative_box"],
         "C65 collision1 continuation lineage")


class LedgerWriter:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.raw: Any = None
        self.stream: Any = None
        self.count = 0
        self.sequence = hashlib.sha256()

    def __enter__(self) -> "LedgerWriter":
        descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                             getattr(os, "O_CLOEXEC", 0), 0o644)
        self.raw = os.fdopen(descriptor, "wb")
        self.stream = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        return self

    def write(self, value: dict[str, Any]) -> None:
        need("row_sha256" not in value, "open output row")
        row_sha = digest(value)
        self.stream.write(canonical({**value, "row_sha256": row_sha}) + b"\n")
        self.sequence.update((row_sha + "\n").encode("ascii"))
        self.count += 1

    def __exit__(self, *_args: Any) -> None:
        self.stream.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": "C72_ATLAS_ORDER_FILTERED_BY_CHILD_ROUTE_WITNESS_OUTGOING_STATE",
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha256(self.path), "size": self.path.stat().st_size,
        }


def write_exclusive(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_CLOEXEC", 0), 0o644)
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "short output write")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def recapture(paths: Iterable[tuple[Path, str]]) -> None:
    for path, expected in paths:
        need(file_sha256(path) == expected, "terminal input recapture:" + str(path))


def build(c72_dir: Path, output: Path) -> dict[str, Any]:
    need(c72_dir.is_dir(), "C72 stage directory")
    need(not output.exists(), "output exists")
    output.mkdir(mode=0o755)
    numeric = numeric_source_pins()
    ctx.prec = PRECISION_BITS
    pair_index, pattern_index, registry_sha = r139.lower.component_cert.key_index_tables()
    cores = tuple(r139.lower.core_cert.physical_cores())
    targets, c65_rows, c69_rows, origins, original, reflected, history = read_authorities(c72_dir)
    expected_word1 = original[0]["official_word_key_id"]
    expected_owner2 = {
        original[1]["selected_absolute_owner_id"],
        reflected[1]["selected_absolute_owner_id"],
    }

    outcomes: Counter[str] = Counter()
    categories: Counter[str] = Counter()
    selected_owners: Counter[str] = Counter()
    pairs: Counter[int] = Counter()
    worst_margins: dict[str, int] = {}
    writer = LedgerWriter(output / LEDGER_NAME)
    with writer:
        for atlas in targets:
            c65 = c65_rows[atlas["C65_aggregate_child_row_sha256"]]
            c69 = c69_rows[atlas["C69c_blocker_row_sha256"]]
            validate_lineage(atlas, c65, c69, history["C35_collision1_event_row_sha256"])
            origin = origins[atlas["pair_index"]]
            parent_key = origin["parent_key"]
            box = box_from_row(atlas)
            chart_id = ":".join(parent_key.split(":")[:2])
            need(chart_id in CORE_INDEX, "target chart")
            atom = r139.lower.step1.Atom(
                CORE_INDEX[chart_id], cores[CORE_INDEX[chart_id]],
                box.t0, box.t1, box.p0, box.p1, Q(0), Q(0), "c72o",
            )
            initial = r139.lower.round136.initial_state(atom)
            owner1, outgoing1, margins = collision1_owner_and_state(
                parent_key, box, atom, initial
            )
            word1, word_error = r139.lower.round136.translation_normalized_official_word(
                initial, "W[0,0]", owner1, pair_index, pattern_index
            )
            need(word1 is not None and word_error is None, "collision1 official word")
            compact1 = r139.lower.round136.compact_key(word1["key"])
            word1_id = compact1["official_word_key_id"]
            owner2_id: str | None = None
            owner2_evidence: dict[str, Any] | None = None
            if word1_id != expected_word1:
                outcome = "STRICT_EXCLUSION_COLLISION1_WORD_MISMATCH"
                witness = word1_id
            else:
                owner2, owner2_evidence = strict_next_owner(outgoing1, FROZEN_OWNER)
                owner2_id = owner2["selected_target_id"]
                need(owner2_id not in expected_owner2, "expected collision2 owner is not exclusion")
                outcome = "STRICT_EXCLUSION_COLLISION2_OWNER_MISMATCH"
                witness = owner2_id
                selected_owners[owner2_id] += 1
            for name, depth in margins.items():
                worst_margins[name] = max(worst_margins.get(name, depth), depth)
            if owner2_evidence is not None:
                for name in ("selected_root_dyadic_depth", "selected_tau_margin_dyadic_depth",
                             "minimum_root_order_gap_dyadic_depth"):
                    depth = owner2_evidence[name]
                    if depth is not None:
                        worst_margins["collision2_" + name] = max(
                            worst_margins.get("collision2_" + name, depth), depth
                        )
            semantic = {
                "schema": SCHEMA + ".oracle-row",
                "C72_atlas_row_sha256": atlas["row_sha256"],
                "C65_aggregate_child_row_sha256": c65["row_sha256"],
                "C69c_blocker_row_sha256": c69["row_sha256"],
                "C61_aggregate_leaf_row_sha256": atlas["C61_aggregate_leaf_row_sha256"],
                "C38_representative_cell_id": origin["representative_cell_id"],
                "C38_representative_parent_row_sha256": origin["representative_parent_row_sha256"],
                "collision1_history_row_sha256": history["C35_collision1_event_row_sha256"],
                "pair_index": atlas["pair_index"], "source_path": atlas["source_path"],
                "child_path": atlas["child_path"], "parent_key": parent_key,
                "exact_representative_box": atlas["exact_representative_box"],
                "source_structural_category": atlas["structural_category"],
                "source_route_classification": atlas["source_route_classification"],
                "child_route_classification": atlas["child_route_classification"],
                "child_route_witness": "OUTGOING_STATE",
                "proof_method": "CENTERED_DELTA_OVER_R2_RADIAL__CENTERED_H1_NEGATIVE_NX_W_CHART__EXACT_ROUTE",
                "additional_dyadic_depth": 0,
                "collision1_owner": FROZEN_OWNER,
                "collision1_chart": "W",
                "collision1_margin_dyadic_depths": margins,
                "collision1_computed_official_word_key_id": word1_id,
                "collision1_expected_official_word_key_id": expected_word1,
                "collision1_registry_row_sha256": compact1["registry_row_sha256"],
                "collision1_ordered_clean_wall_record": word1["ordered_clean_wall_record"],
                "collision2_selected_owner": owner2_id,
                "collision2_expected_owner_set": sorted(expected_owner2),
                "collision2_owner_order_evidence": owner2_evidence,
                "exit_class": "STRICT_EXCLUSION",
                "strict_exclusion_reason": outcome,
                "strict_exclusion_witness": witness,
                "current_disposition": "STAGED_ZERO_CREDIT_STRICT_EXCLUSION_CANDIDATE",
                "formal_credit": 0, "whole_parent_credit": 0,
                "D02_gate_credit": 0, "CM2_credit": 0,
            }
            writer.write(semantic)
            outcomes[outcome] += 1
            categories[atlas["structural_category"]] += 1
            pairs[atlas["pair_index"]] += 1

    need(writer.count == 18_668 and dict(outcomes) == EXPECTED_OUTCOME_CENSUS,
         "output outcome census")
    need(dict(categories) == EXPECTED_SOURCE_CENSUS, "output category census")
    need(dict(selected_owners) == EXPECTED_SELECTED_OWNER_CENSUS,
         "collision2 selected-owner census")
    need(set(pairs) == set(origins) and len(pairs) == 12, "pair coverage")

    recapture([
        (c72_dir / C72_FILES["result"], PINS["C72_RESULT"]),
        (c72_dir / C72_FILES["ledger"], PINS["C72_LEDGER"]),
        (c72_dir / C72_FILES["verification"], PINS["C72_VERIFY"]),
        (DELIVERABLES / "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json", PINS["C65_RESULT"]),
        (DELIVERABLES / "cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz", PINS["C65_LEAVES"]),
        (DELIVERABLES / "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json", PINS["C69_RESULT"]),
        (DELIVERABLES / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz", PINS["C69_BLOCKERS"]),
        (C38_DIR / "result.json", PINS["C38_RESULT"]),
        (C38_DIR / "collision1_2_child_pairs.jsonl.gz", PINS["C38_CHILDREN"]),
        (C35_DIR / "result.json", PINS["C35_RESULT"]),
        (C35_DIR / "path_occurrences.jsonl.gz", PINS["C35_PATH"]),
        (C37_DIR / "result.json", PINS["C37_RESULT"]),
        (C37_DIR / "reflected_r1648_occurrences.jsonl.gz", PINS["C37_PATH"]),
    ])

    source_hash = file_sha256(SELF)
    result: dict[str, Any] = {
        "schema": SCHEMA + ".result",
        "status": "PASS_18668_OF_18668_OUTGOING_STATE_WITNESS_CHILDREN_STRICTLY_EXCLUDED__ZERO_CREDIT",
        "producer_file_sha256": source_hash,
        "precision_bits": PRECISION_BITS, "python_flint_version": "0.9.0",
        "numeric_source_sha256": numeric,
        "input_file_sha256": dict(sorted(PINS.items())),
        "input_object_sha256": dict(sorted(OBJECT_PINS.items())),
        "authority_row_sha256": history,
        "official_registry_sha256": registry_sha,
        "capability_scope": {
            "selector": "child_route_witness == OUTGOING_STATE",
            "target_child_count": 18_668,
            "source_structural_category_census": dict(sorted(categories.items())),
            "original_COLLISION1_OUTGOING_STATE_category_child_count": 423,
            "same_capability_cross_category_child_count": 18_245,
            "same_capability_pending_child_count": 0,
            "additional_dyadic_depth": 0,
        },
        "outcome_census": dict(sorted(outcomes.items())),
        "collision2_selected_owner_census": dict(sorted(selected_owners.items())),
        "pair_census": {str(key): value for key, value in sorted(pairs.items())},
        "worst_strict_margin_dyadic_depths": dict(sorted(worst_margins.items())),
        "ledger": writer.descriptor(),
        "strict_boundary": {
            "candidate_is_authority": False, "formal_credit": 0,
            "whole_parent_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
            "global_consumption_ready": False,
            "remaining_C72_atlas_children_outside_this_capability": 115_487,
            "only_later_no_producer_global_consumer_may_promote": True,
        },
    }
    result["object_sha256"] = digest(result)
    write_exclusive(output / RESULT_NAME, canonical(result) + b"\n")
    report = (
        "# C72o exact collision-one outgoing-state oracle\n\n"
        "- Selector: `child_route_witness == OUTGOING_STATE`.\n"
        "- Closed without subdivision: 18,668 / 18,668 children.\n"
        "- Strict exclusions: 8,321 collision-one official-word mismatches; "
        "10,347 collision-two strict-owner mismatches.\n"
        "- Source-category split: 423 outgoing-state category + 18,245 "
        "boundary-source children with the same child-level capability.\n"
        "- This staged object grants zero formal, whole-parent, D02, or CM2 credit.\n"
    ).encode("utf-8")
    write_exclusive(output / REPORT_NAME, report)
    write_exclusive(output / LOCK_NAME,
                    b"STAGED ZERO-CREDIT ORACLE ONLY; NO AUTHORITY OR GLOBAL PROMOTION.\n")
    for path in (output / LEDGER_NAME, output / RESULT_NAME,
                 output / REPORT_NAME, output / LOCK_NAME):
        descriptor, first = open_regular(path)
        try:
            while os.read(descriptor, 1 << 20):
                pass
            need(identity(os.fstat(descriptor)) == first ==
                 identity(os.stat(path, follow_symlinks=False)),
                 "terminal output replay:" + path.name)
        finally:
            os.close(descriptor)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--c72-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.c72_dir.resolve(), args.output_dir.resolve())
    print(json.dumps({"status": result["status"],
                      "object_sha256": result["object_sha256"],
                      "ledger_sha256": result["ledger"]["sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
