#!/usr/bin/env python3
"""Independent verifier for the C30q0 representative compact-q theorem.

The candidate producer is never imported or executed.  Its source is captured
only as a pinned byte object.  This verifier instead reads the frozen Round184
and Round218 authorities, derives the face-grid cuts from their rows, rebuilds
the complete relative-open product stratification, derives the two target
inequalities from the original geometry registry, and replays the fixed
upstream complement for one representative origin.

Success remains a research-only, zero-formal-credit result.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
AUDIT_ROOT = WORKSPACE / ".cm2-runtime" / "audit"

ORIGIN = "W:N:03.15.01111111"
SOURCE_CHART = "W:N"
FROZEN_TARGET = "W[1,0]"
FUTURE_TARGET = "W[-1,0]"
OTHER_TARGET = "G[0,1]"

PRODUCER = (
    HERE
    / "cm2_round306c30q0_compact_q_representative_origin_analytic_probe.py"
)
PRODUCER_SHA256 = (
    "971a112581367f8263692ad18fe73f112dfe5473e58f307cb5e16824c7171e90"
)
DEFAULT_CANDIDATE = (
    AUDIT_ROOT
    / "c30q0-representative-analytic-v2-20260807T1021"
    / "stdout.json"
)
DEFAULT_CANDIDATE_SHA256 = (
    "bca0c9882db0fefe5fad65617c73418218330e8cdb651dbe04f8c64ff3725968"
)

ROUND184_MANIFEST = (
    HERE
    / "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
      "manifest.sha256"
)
ROUND184_MANIFEST_SHA256 = (
    "3c2a50663dc47479f67435109b737362895e53a2c1b4c29991fe875c5ac68cd1"
)
ROUND184_CERTIFICATE = (
    HERE
    / "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
      "certificate.json"
)
ROUND184_CERTIFICATE_SHA256 = (
    "292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f"
)
ROUND184_RESULT_SHA256 = (
    "70026cc9e52cfe0adee0be2ff8daf0f4519a2f1947338e902399461039b82dbe"
)

ROUND218_MANIFEST = (
    HERE
    / "cm2_round218_source_w_compact_q_source_stratum_frontier_"
      "probe_manifest.sha256"
)
ROUND218_MANIFEST_SHA256 = (
    "5cde966f9fbdca1ab60e414fd649b8649f1babee92f0b27136be207f0bb92602"
)
ROUND218_RESULT = (
    HERE
    / "cm2_round218_source_w_compact_q_source_stratum_frontier_result.json"
)
ROUND218_RESULT_SHA256 = (
    "dc4d86f68393736c314005aff27ea2febb8072e3224c892090d8a7cf54844887"
)
ROUND218_INNER_SHA256 = (
    "f440ee0ac043067a48b8ed8e217a827ed8c0e5072778e84931090df8cd4f7000"
)
ROUND218_REPLAY = (
    HERE / "cm2_round218_source_w_compact_q_source_stratum_frontier.py"
)
ROUND218_REPLAY_SHA256 = (
    "1dadb46be62853391898314b4a9fbbf5aae2750e70a21e3d891e975f45a3cfbf"
)
GEOMETRY_REGISTRY = HERE / "cm2_gate3_candidate_first_hit_cert.py"
GEOMETRY_REGISTRY_SHA256 = (
    "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
)

CANDIDATE_SCHEMA = (
    "cm2.round306c30q0.compact-q-representative-origin-analytic-probe.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round306c30q0.compact-q-representative-origin-analytic-"
    "independent-verification.v1"
)
PASS_STATUS = (
    "PASS_REPRESENTATIVE_COMPACT_Q_WHOLE_ORIGIN_ANALYTIC_THEOREM__"
    "ZERO_FORMAL_CREDIT"
)


class Reject(RuntimeError):
    pass


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


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def same(left: Any, right: Any) -> bool:
    try:
        return canonical(left) == canonical(right)
    except (TypeError, ValueError):
        return False


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise Reject("non-finite JSON constant:" + value)


def reject_float(value: str) -> None:
    raise Reject("floating JSON number:" + value)


def stat_identity(value: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def canonical_path(path: Path, label: str) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    try:
        resolved = absolute.resolve(strict=True)
    except OSError as error:
        raise Reject("canonical path:" + label) from error
    need(resolved == absolute, "canonical path:" + label)
    need(absolute.is_relative_to(WORKSPACE), "workspace path:" + label)
    return absolute


def capture_regular(
    path: Path,
    label: str,
    maximum: int = 64 << 20,
) -> tuple[bytes, tuple[int, int, int, int, int, int, int]]:
    absolute = canonical_path(path, label)
    before_path = absolute.lstat()
    need(
        stat.S_ISREG(before_path.st_mode)
        and before_path.st_nlink == 1
        and 0 < before_path.st_size <= maximum,
        "regular singleton bounds:" + label,
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        chunks: list[bytes] = []
        size = 0
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
            size += len(block)
            need(size <= maximum, "capture maximum:" + label)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = absolute.lstat()
    need(
        stat_identity(before_path)
        == stat_identity(before)
        == stat_identity(after)
        == stat_identity(current),
        "stable capture:" + label,
    )
    raw = b"".join(chunks)
    need(len(raw) == before.st_size, "capture byte count:" + label)
    need(absolute.resolve(strict=True) == absolute, "stable parent chain:" + label)
    return raw, stat_identity(before)


def capture_deliverable(path: Path, label: str, maximum: int = 64 << 20) -> bytes:
    need(path.parent == HERE, "deliverable parent:" + label)
    raw, _identity = capture_regular(path, label, maximum)
    return raw


def decode_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8", "strict")
        value = json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
            parse_float=reject_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    need(type(value) is dict, "JSON object:" + label)
    return value


def decode_candidate(raw: bytes) -> dict[str, Any]:
    document = decode_json(raw, "candidate")
    need(raw == canonical(document) + b"\n", "candidate canonical bytes")
    return document


def parse_fraction(value: Any, label: str) -> Q:
    need(type(value) is str, "rational string:" + label)
    try:
        result = Q(value)
    except (ValueError, ZeroDivisionError) as error:
        raise Reject("rational parse:" + label) from error
    need(str(result) == value, "canonical rational:" + label)
    return result


def verify_manifest(path: Path, expected_hash: str, label: str) -> dict[str, str]:
    raw = capture_deliverable(path, label, 128 << 10)
    need(sha256(raw) == expected_hash, label + " manifest pin")
    entries: dict[str, str] = {}
    try:
        lines = raw.decode("ascii", "strict").splitlines()
    except UnicodeDecodeError as error:
        raise Reject(label + " manifest ASCII") from error
    need(bool(lines) and raw.endswith(b"\n"), label + " manifest lines")
    for line in lines:
        parts = line.split("  ", 1)
        need(len(parts) == 2, label + " manifest syntax")
        value, filename = parts
        need(
            len(value) == 64
            and all(character in "0123456789abcdef" for character in value)
            and filename not in entries
            and filename not in {".", ".."}
            and "/" not in filename
            and "\\" not in filename,
            label + " manifest member name",
        )
        entries[filename] = value
    for filename, expected in sorted(entries.items()):
        member = capture_deliverable(HERE / filename, label + ":" + filename, 64 << 20)
        need(sha256(member) == expected, label + " manifest member:" + filename)
    return entries


def closed_row(row: dict[str, Any], label: str) -> None:
    need(type(row.get("row_sha256")) is str, label + " row digest field")
    body = {key: value for key, value in row.items() if key != "row_sha256"}
    need(digest(body) == row["row_sha256"], label + " row digest")


def dyadic_strict_upper(value: Q) -> Q:
    need(Q(0) <= value < Q(1), "dyadic bound domain")
    denominator = 1
    while Q(1, denominator * 2) > value:
        denominator *= 2
    result = Q(1, denominator)
    need(value < result and result / 2 <= value, "minimal dyadic strict upper")
    return result


def axis_atoms(cuts: tuple[Q, ...]) -> list[tuple[str, Q, Q]]:
    need(len(cuts) >= 2 and tuple(sorted(set(cuts))) == cuts, "ordered dynamic cuts")
    atoms: list[tuple[str, Q, Q]] = []
    for index, point in enumerate(cuts):
        atoms.append(("POINT", point, point))
        if index + 1 < len(cuts):
            atoms.append(("OPEN_INTERVAL", point, cuts[index + 1]))
    return atoms


def incident(
    box: dict[str, Any],
    atoms: dict[str, tuple[str, Q, Q]],
) -> bool:
    for axis in ("t", "r", "s"):
        kind, lower, upper = atoms[axis]
        left, right = box[axis]
        if kind == "POINT":
            if not left <= lower <= right:
                return False
        elif not left <= lower < upper <= right:
            return False
    return True


def geometry_object(atom: dict[str, tuple[str, Q, Q]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for axis in ("t", "r", "s"):
        kind, lower, upper = atom[axis]
        if kind == "POINT":
            result[axis] = {"kind": "POINT", "value": str(lower)}
        else:
            result[axis] = {
                "kind": "OPEN_INTERVAL",
                "lower": str(lower),
                "upper": str(upper),
            }
    return result


def derive_faces(round218: dict[str, Any]) -> dict[str, Any]:
    rows = [
        row
        for row in round218["result"]["source_grazing_face_analysis"]["face_rows"]
        if row.get("origin_key") == ORIGIN
    ]
    need(len(rows) == 16, "Round218 representative face count")
    for row in rows:
        closed_row(row, "Round218 representative face")
        need(
            row.get("source_chart_id") == SOURCE_CHART
            and row.get("p_sign") == 1
            and row.get("face_box", {}).get("r") == ["0", "0"]
            and row.get("classification")
            == "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
            and row.get("selected_or_active_targets") == [FUTURE_TARGET]
            and row.get("whole_origin_integer_credit") == 0,
            "Round218 representative face semantics",
        )
        records = row.get("root_records")
        need(
            type(records) is list
            and [record.get("target") for record in records]
            == [OTHER_TARGET, FUTURE_TARGET]
            and records[0].get("classification") == "no_real_intersection"
            and records[1].get("classification") == "strict_future_root",
            "Round218 representative face roots",
        )

    t_intervals = {
        tuple(parse_fraction(value, "face t") for value in row["face_box"]["t"])
        for row in rows
    }
    s_intervals = {
        tuple(parse_fraction(value, "face s") for value in row["face_box"]["s"])
        for row in rows
    }
    t_cuts = tuple(sorted({value for pair in t_intervals for value in pair}))
    s_cuts = tuple(sorted({value for pair in s_intervals for value in pair}))
    need(
        len(t_cuts) == 9
        and len(s_cuts) == 3
        and t_intervals
        == {(t_cuts[index], t_cuts[index + 1]) for index in range(8)}
        and s_intervals
        == {(s_cuts[index], s_cuts[index + 1]) for index in range(2)},
        "dynamic face cut cover",
    )
    actual_products = {
        (
            *(parse_fraction(value, "face product t") for value in row["face_box"]["t"]),
            *(parse_fraction(value, "face product s") for value in row["face_box"]["s"]),
        )
        for row in rows
    }
    expected_products = {
        (t_cuts[t_index], t_cuts[t_index + 1], s_cuts[s_index], s_cuts[s_index + 1])
        for t_index in range(len(t_cuts) - 1)
        for s_index in range(len(s_cuts) - 1)
    }
    need(actual_products == expected_products, "dynamic 8-by-2 face product")
    need(len({row["root_key"] for row in rows}) == 16, "unique face root keys")

    boxes = sorted((
        {
            "root_key": row["root_key"],
            "t": tuple(parse_fraction(value, "root t") for value in row["face_box"]["t"]),
            "r": (Q(0), Q(1)),
            "s": tuple(parse_fraction(value, "root s") for value in row["face_box"]["s"]),
            "Round218_q0_face_row_sha256": row["row_sha256"],
        }
        for row in rows
    ), key=lambda value: value["root_key"])
    serialized = [
        {
            "root_key": box["root_key"],
            "t": [str(value) for value in box["t"]],
            "r": [str(value) for value in box["r"]],
            "s": [str(value) for value in box["s"]],
            "Round218_q0_face_row_sha256": box["Round218_q0_face_row_sha256"],
        }
        for box in boxes
    ]
    return {
        "face_rows": sorted(rows, key=lambda value: value["root_key"]),
        "boxes": boxes,
        "serialized_boxes": serialized,
        "t_cuts": t_cuts,
        "s_cuts": s_cuts,
    }


def derive_atoms(face: dict[str, Any]) -> dict[str, Any]:
    boxes = face["boxes"]
    t_cuts = face["t_cuts"]
    r_cuts = (Q(0), Q(1))
    s_cuts = face["s_cuts"]
    rows: list[dict[str, Any]] = []
    for t_atom in axis_atoms(t_cuts):
        for r_atom in axis_atoms(r_cuts):
            for s_atom in axis_atoms(s_cuts):
                atom = {"t": t_atom, "r": r_atom, "s": s_atom}
                roots = sorted(
                    box["root_key"] for box in boxes if incident(box, atom)
                )
                need(bool(roots), "dynamic atom incident root")
                dimension = sum(
                    atom[axis][0] == "OPEN_INTERVAL" for axis in ("t", "r", "s")
                )
                rows.append({
                    "ambient_dimension": dimension,
                    "geometry": geometry_object(atom),
                    "owner_root_key": roots[0],
                    "incident_root_count": len(roots),
                    "incident_root_keys": roots,
                    "analytic_disposition": "EXCLUDED_FROZEN_OWNER_STRICTLY_BEHIND",
                })
    rows.sort(key=lambda row: canonical(row["geometry"]))
    by_dimension = Counter(row["ambient_dimension"] for row in rows)
    by_incidence = Counter(row["incident_root_count"] for row in rows)
    by_owner = Counter(row["owner_root_key"] for row in rows)

    t_points, t_open = len(t_cuts), len(t_cuts) - 1
    r_points, r_open = len(r_cuts), len(r_cuts) - 1
    s_points, s_open = len(s_cuts), len(s_cuts) - 1
    derived_dimensions = {
        3: t_open * r_open * s_open,
        2: (
            t_points * r_open * s_open
            + t_open * r_points * s_open
            + t_open * r_open * s_points
        ),
        1: (
            t_open * r_points * s_points
            + t_points * r_open * s_points
            + t_points * r_points * s_open
        ),
        0: t_points * r_points * s_points,
    }
    need(
        dict(by_dimension) == derived_dimensions
        and sum(derived_dimensions.values()) == len(rows) == 255
        and derived_dimensions == {3: 16, 2: 74, 1: 111, 0: 54}
        and all(
            row["incident_root_count"] == 1
            for row in rows
            if row["ambient_dimension"] == 3
        )
        and set(by_owner) == {box["root_key"] for box in boxes}
        and all(row["owner_root_key"] == min(row["incident_root_keys"]) for row in rows),
        "dynamic complete half-open owner partition",
    )
    return {
        "rule": (
            "each relative-open atomic product stratum is owned by the "
            "lexicographically least incident Round218 root key"
        ),
        "t_cut_count": len(t_cuts),
        "r_cut_count": len(r_cuts),
        "s_cut_count": len(s_cuts),
        "root_box_count": len(boxes),
        "atomic_stratum_count": len(rows),
        "atomic_stratum_count_by_dimension": {
            str(key): by_dimension[key] for key in sorted(by_dimension, reverse=True)
        },
        "incident_root_multiplicity_count": {
            str(key): by_incidence[key] for key in sorted(by_incidence)
        },
        "owner_root_count": len(by_owner),
        "owner_assignment_rows_sha256": digest(rows),
        "owner_assignment_rows": rows,
        "all_strata_owned_exactly_once": True,
        "all_analytic_dispositions_inherit_on_boundaries": True,
    }


def load_upstream() -> Any:
    replay_raw, replay_identity = capture_regular(
        ROUND218_REPLAY, "Round218 replay module", 512 << 10
    )
    need(sha256(replay_raw) == ROUND218_REPLAY_SHA256, "Round218 replay module pin")
    geometry_raw, geometry_identity = capture_regular(
        GEOMETRY_REGISTRY, "original geometry registry", 2 << 20
    )
    need(sha256(geometry_raw) == GEOMETRY_REGISTRY_SHA256, "geometry registry pin")
    need(PRODUCER.stem not in sys.modules, "candidate producer not preloaded")
    if os.fspath(HERE) not in sys.path:
        sys.path.insert(0, os.fspath(HERE))
    module = importlib.import_module(ROUND218_REPLAY.stem)
    need(
        Path(module.__file__).resolve(strict=True) == ROUND218_REPLAY
        and sha256(capture_regular(ROUND218_REPLAY, "Round218 replay module post", 512 << 10)[0])
        == ROUND218_REPLAY_SHA256,
        "Round218 replay imported identity",
    )
    geometry = module.r176.base
    need(
        Path(geometry.__file__).resolve(strict=True) == GEOMETRY_REGISTRY
        and sha256(capture_regular(GEOMETRY_REGISTRY, "geometry registry post", 2 << 20)[0])
        == GEOMETRY_REGISTRY_SHA256,
        "geometry registry imported identity",
    )
    need(
        replay_identity == capture_regular(ROUND218_REPLAY, "Round218 replay final", 512 << 10)[1]
        and geometry_identity == capture_regular(GEOMETRY_REGISTRY, "geometry registry final", 2 << 20)[1]
        and PRODUCER.stem not in sys.modules,
        "upstream module capture remained stable",
    )
    return module


def replay_complement(
    probe: Any,
    registry: dict[str, Any],
    face_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    need(probe.r176.FROZEN_OWNER == FROZEN_TARGET, "upstream frozen owner")
    state = probe.r176.replay_frontier()
    origin = state["origins"].get(ORIGIN)
    need(
        origin is not None
        and origin["chart_id"] == SOURCE_CHART
        and FROZEN_TARGET in origin["active_targets"],
        "frozen owner in upstream workload",
    )
    frontier = sorted(
        (row for row in state["frontier"] if row.origin_key == ORIGIN),
        key=lambda row: row.key,
    )
    preclosed: list[tuple[Any, str]] = []
    unresolved: list[Any] = []
    for row in frontier:
        kind, _evidence = probe.r176.closure(row)
        if kind is None:
            unresolved.append(row)
        else:
            preclosed.append((row, kind))
    need(
        len(frontier) == 46
        and len(preclosed) == 2
        and Counter(kind for _row, kind in preclosed) == Counter({"EXCLUDED": 2})
        and len(unresolved) == 44,
        "46-to-44 upstream complement",
    )

    grazing = sorted(
        (
            row for row in unresolved
            if probe.r180.residual_category(row)
            == "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
        ),
        key=lambda row: row.key,
    )
    need(len(grazing) == 16, "sixteen source-grazing bridge roots")
    p_intervals = {(row.box.p0, row.box.p1) for row in grazing}
    need(len(p_intervals) == 1, "common full-r bridge interval")
    p_lower, p_upper = next(iter(p_intervals))
    need(p_lower > 0 and p_upper == 1, "positive full-r bridge")
    k = Q(1) - p_lower * p_lower
    need(Q(0) < k < Q(1), "derived compact K")

    replayed_faces = sorted(
        (probe.q_face_evidence(row) for row in grazing),
        key=lambda row: row["root_key"],
    )
    need(same(replayed_faces, face_rows), "full-r bridge binds q0 faces")
    replayed_root_rows = [
        {
            "root_key": row.key,
            "source_chart_id": row.chart_id,
            "p_sign": 1,
            "face_box": {
                "t": [str(row.box.t0), str(row.box.t1)],
                "r": ["0", "0"],
                "s": [str(row.box.s0), str(row.box.s1)],
            },
            "active_targets": list(row.active_targets),
        }
        for row in grazing
    ]

    refinement = probe.r180.refine_origin(unresolved, 4)
    children = sorted(refinement["final_residual_rows"], key=lambda row: row.key)
    categories = Counter(probe.r180.residual_category(row) for row in children)
    need(len(children) == 328, "44-to-328 upstream refinement")
    need(
        registry["Round176_preclosed_frontier_count"] == len(preclosed)
        and sorted(registry["Round176_preclosed_kinds"])
        == sorted({kind for _row, kind in preclosed})
        and registry["Round176_residual_root_count"] == len(unresolved)
        and registry["Round180_residual_child_count"] == len(children)
        and registry["Round180_residual_child_keys_sha256"]
        == digest([row.key for row in children])
        and same(
            registry["Round180_residual_category_count"],
            {key: categories[key] for key in sorted(categories)},
        ),
        "Round184 registry binds targeted replay",
    )

    closed: list[dict[str, Any]] = []
    residual: list[dict[str, Any]] = []
    for row in children:
        category = probe.r180.residual_category(row)
        reduction = probe.p215.exact_behind_reduce(row, category)
        summary = {
            "cell_key": row.key,
            "category": category,
            "closed": reduction["closed"],
            "residual_reason": reduction["residual_reason"],
            "active_targets": list(row.active_targets),
            "box": {
                "t": [str(row.box.t0), str(row.box.t1)],
                "p": [str(row.box.p0), str(row.box.p1)],
                "s": [str(row.box.s0), str(row.box.s1)],
            },
        }
        (closed if reduction["closed"] else residual).append(summary)
    need(
        len(closed) == 327
        and len(residual) == 1
        and residual[0]["category"] == "SOURCE_GRAZING_COMPACT_Q_RESIDUAL",
        "328-to-327-plus-1 exact-behind complement",
    )
    return {
        "candidate": {
            "Round176_frontier_root_count": len(frontier),
            "Round176_preclosed_root_count": len(preclosed),
            "Round176_preclosed_disposition_count": {
                key: value
                for key, value in sorted(Counter(kind for _row, kind in preclosed).items())
            },
            "Round176_residual_root_count": len(unresolved),
            "Round176_source_grazing_full_r_root_count": len(grazing),
            "Round176_source_grazing_root_rows_sha256": digest(replayed_root_rows),
            "Round176_source_grazing_p_interval": [str(p_lower), str(p_upper)],
            "Round176_source_grazing_q_parameterization": (
                "q=sqrt(" + str(k) + ")*r, r in [0,1]"
            ),
            "Round180_final_child_count": len(children),
            "Round180_final_child_keys_sha256": digest([row.key for row in children]),
            "Round180_final_category_count": {
                key: categories[key] for key in sorted(categories)
            },
            "exact_behind_closed_child_count": len(closed),
            "exact_behind_closed_child_rows_sha256": digest(closed),
            "exact_behind_residual_child_count": len(residual),
            "exact_behind_residual_child": residual[0],
            "only_unclosed_complement_is_compact_q": True,
        },
        "k": k,
        "p_interval": (p_lower, p_upper),
        "frozen_owner_in_workload": True,
    }


def derive_analytic(
    probe: Any,
    face: dict[str, Any],
    complement: dict[str, Any],
) -> dict[str, Any]:
    geometry = probe.r176.base
    targets = {target.target_id: target for target in geometry.TARGETS}
    need(
        FROZEN_TARGET in targets
        and FUTURE_TARGET in targets
        and targets[FROZEN_TARGET].obstacle == "W"
        and targets[FROZEN_TARGET].ix == 1
        and targets[FROZEN_TARGET].iy == 0
        and targets[FUTURE_TARGET].obstacle == "W"
        and targets[FUTURE_TARGET].ix == -1
        and targets[FUTURE_TARGET].iy == 0,
        "original target geometry definitions",
    )
    rho = Q(geometry.RADIUS["W"])
    t_cuts = face["t_cuts"]
    s_cuts = face["s_cuts"]
    t_min, t_max = t_cuts[0], t_cuts[-1]
    k = complement["k"]

    # Avoid numerical radicals: select the minimal dyadic q-bound whose square
    # is above K and whose next half-square is not.
    denominator = 1
    while Q(1, (denominator * 2) ** 2) > k:
        denominator *= 2
    q_bound = Q(1, denominator)
    need(k < q_bound * q_bound and (q_bound / 2) ** 2 <= k, "derived q bound")
    t_bound = dyadic_strict_upper(max(abs(t_min), abs(t_max)))
    p_square_lower = Q(1) - q_bound * q_bound
    normal_square_lower = Q(1) - t_bound * t_bound
    pa_square_lower = p_square_lower * normal_square_lower
    need(pa_square_lower > Q(1, 4), "derived p-a half bound")

    t_radius_min = t_min + rho
    t_radius_max = t_max + rho
    need(t_radius_min > 0, "positive t plus radius domain")
    ell_lower = Q(1, 2) - q_bound * t_radius_max
    transverse_upper = q_bound + t_radius_max
    transverse_margin = rho - transverse_upper
    distance_margin = Q(1) + 2 * rho * t_min
    need(
        ell_lower > 0
        and transverse_margin > 0
        and distance_margin > 0,
        "strict nonfrozen future-root margins",
    )

    exact_pa_square_floor = (Q(1) - k) * (
        Q(1) - max(abs(t_min), abs(t_max)) ** 2
    )
    one_minus_pa_upper = Q(2, 3) * (Q(1) - exact_pa_square_floor)
    time_one_polynomial_half_upper = (
        one_minus_pa_upper + rho * t_max + q_bound * (t_max + rho)
    )
    need(
        exact_pa_square_floor > Q(1, 4)
        and time_one_polynomial_half_upper < 0,
        "strict near-root-before-one witness",
    )

    expected = {
        "coordinate_definitions": {
            "normal": "n=(t,a), a=sqrt(1-t^2)>0",
            "compact_velocity": "u=q*n+p*J(n)",
            "q": "sqrt(" + str(k) + ")*r, 0<=r<=1",
            "p": "sqrt(1-q^2)>0",
            "source_point": "(1/2+s,1/2)+(" + str(rho) + ")*n",
        },
        "exact_domain": {
            "t": [str(t_min), str(t_max)],
            "r": ["0", "1"],
            "s": [str(s_cuts[0]), str(s_cuts[-1])],
            "p_sign": 1,
            "source_chart": SOURCE_CHART,
        },
        "coarse_radical_witnesses": {
            "q_squared_strict_upper": str(q_bound * q_bound),
            "q_squared_exact_maximum": str(k),
            "q_squared_upper_gap": str(q_bound * q_bound - k),
            "absolute_t_strict_upper": str(t_bound),
            "p_squared_strict_lower": str(p_square_lower),
            "normal_y_squared_strict_lower": str(normal_square_lower),
            "p_times_normal_y_squared_strict_lower": str(pa_square_lower),
            "p_times_normal_y_strict_lower": "1/2",
        },
        "frozen_target_strictly_behind": {
            "target": FROZEN_TARGET,
            "center_displacement": "(1,0)-(" + str(rho) + ")*n",
            "forward_projection": "ell_F=q*(t-" + str(rho) + ")-p*a",
            "uniform_strict_upper": "-1/2",
            "proof": "q>=0 and t-" + str(rho) + "<0, while p*a>1/2",
            "future_root_possible": False,
        },
        "certified_nonfrozen_strict_future_root": {
            "target": FUTURE_TARGET,
            "center_displacement": "(-1,0)-(" + str(rho) + ")*n",
            "forward_projection": "ell_L=p*a-q*(t+" + str(rho) + ")",
            "forward_projection_strict_lower": str(ell_lower),
            "transverse": "z_L=q*a+p*(t+" + str(rho) + ")",
            "absolute_transverse_strict_upper": str(transverse_upper),
            "target_radius": str(rho),
            "radius_minus_absolute_transverse_strict_lower": str(transverse_margin),
            "discriminant_strictly_positive": True,
            "center_distance_squared_minus_target_radius_squared_strict_lower": str(distance_margin),
            "near_root_strictly_positive": True,
            "near_root_strict_upper": "1",
            "certified_time_horizon": "<1<3",
        },
        "first_hit_logic": {
            "one_strict_future_collision_exists_everywhere": True,
            "frozen_target_has_no_future_root_everywhere": True,
            "ties_or_order_switches_between_nonfrozen_targets_change_conclusion": False,
            "all_points_exclude_frozen_first_owner": True,
        },
    }
    return {
        "candidate": expected,
        "rho": rho,
        "q_bound": q_bound,
        "t_bound": t_bound,
        "ell_lower": ell_lower,
        "transverse_upper": transverse_upper,
        "transverse_margin": transverse_margin,
        "distance_margin": distance_margin,
        "time_one_polynomial_half_upper": time_one_polynomial_half_upper,
        "exact_pa_square_floor": exact_pa_square_floor,
    }


def reconstruct_reference() -> dict[str, Any]:
    producer_raw, producer_identity = capture_regular(
        PRODUCER, "candidate producer source", 2 << 20
    )
    need(sha256(producer_raw) == PRODUCER_SHA256, "candidate producer byte pin")
    need(PRODUCER.stem not in sys.modules, "candidate producer never imported")

    entries184 = verify_manifest(
        ROUND184_MANIFEST, ROUND184_MANIFEST_SHA256, "Round184"
    )
    entries218 = verify_manifest(
        ROUND218_MANIFEST, ROUND218_MANIFEST_SHA256, "Round218"
    )
    need(
        entries184.get(ROUND184_CERTIFICATE.name) == ROUND184_CERTIFICATE_SHA256,
        "Round184 certificate manifest binding",
    )
    need(
        entries218.get(ROUND218_RESULT.name) == ROUND218_RESULT_SHA256,
        "Round218 result manifest binding",
    )
    raw184 = capture_deliverable(ROUND184_CERTIFICATE, "Round184 certificate", 8 << 20)
    raw218 = capture_deliverable(ROUND218_RESULT, "Round218 result", 4 << 20)
    need(sha256(raw184) == ROUND184_CERTIFICATE_SHA256, "Round184 certificate pin")
    need(sha256(raw218) == ROUND218_RESULT_SHA256, "Round218 result pin")
    doc184 = decode_json(raw184, "Round184 certificate")
    doc218 = decode_json(raw218, "Round218 result")
    need(
        doc184.get("result_sha256") == ROUND184_RESULT_SHA256
        and digest(doc184.get("result")) == ROUND184_RESULT_SHA256,
        "Round184 inner result pin",
    )
    need(
        doc218.get("result_sha256") == ROUND218_INNER_SHA256
        and digest(doc218.get("result")) == ROUND218_INNER_SHA256,
        "Round218 inner result pin",
    )
    registry_rows = [
        row
        for row in doc184["result"]["priority_registry"]["rows"]
        if row.get("origin_key") == ORIGIN
    ]
    need(len(registry_rows) == 1, "unique representative registry row")
    registry = registry_rows[0]
    closed_row(registry, "Round184 representative registry")
    need(
        registry.get("priority_class") == "COMPACT_Q_PRESENT"
        and registry.get("selection_uses_new_closure_outcome") is False,
        "outcome-blind compact-q representative selection",
    )

    face = derive_faces(doc218)
    atoms = derive_atoms(face)
    probe = load_upstream()
    complement = replay_complement(probe, registry, face["face_rows"])
    analytic = derive_analytic(probe, face, complement)
    need(
        capture_regular(PRODUCER, "candidate producer source final", 2 << 20)[1]
        == producer_identity
        and PRODUCER.stem not in sys.modules,
        "candidate producer remained byte-only",
    )
    return {
        "producer_sha256": PRODUCER_SHA256,
        "producer_executed_or_imported": False,
        "candidate_sha256": DEFAULT_CANDIDATE_SHA256,
        "inputs": {
            "Round184_manifest_sha256": ROUND184_MANIFEST_SHA256,
            "Round184_manifest_member_count": len(entries184),
            "Round184_certificate_sha256": ROUND184_CERTIFICATE_SHA256,
            "Round184_certificate_result_sha256": ROUND184_RESULT_SHA256,
            "Round218_manifest_sha256": ROUND218_MANIFEST_SHA256,
            "Round218_manifest_member_count": len(entries218),
            "Round218_result_file_sha256": ROUND218_RESULT_SHA256,
            "Round218_result_sha256": ROUND218_INNER_SHA256,
        },
        "registry": registry,
        "face": face,
        "atoms": atoms,
        "complement": complement,
        "analytic": analytic,
    }


def validate_candidate(document: dict[str, Any], reference: dict[str, Any]) -> None:
    need(set(document) == {"schema", "result", "result_sha256"}, "candidate top-level keys")
    need(document.get("schema") == CANDIDATE_SCHEMA, "candidate schema")
    result = document.get("result")
    need(type(result) is dict, "candidate result object")
    need(
        type(document.get("result_sha256")) is str
        and digest(result) == document["result_sha256"],
        "candidate result self digest",
    )
    need(
        set(result) == {
            "status", "verdict", "frozen_inputs", "representative_selection",
            "root_box_partition", "analytic_whole_origin_certificate",
            "cross_root_half_open_owner_partition",
            "targeted_upstream_complement_replay", "representative_conclusion",
            "strict_nonpromotion", "next_core_gate",
        },
        "candidate result keys",
    )
    need(
        result.get("status") == PASS_STATUS
        and result.get("verdict") == "PASS_REPRESENTATIVE_THEOREM",
        "candidate status",
    )

    nonpromotion = result.get("strict_nonpromotion")
    need(type(nonpromotion) is dict, "candidate nonpromotion object")
    need(
        type(nonpromotion.get("formal_credit")) is int
        and not isinstance(nonpromotion.get("formal_credit"), bool)
        and nonpromotion.get("formal_credit") == 0,
        "candidate formal credit",
    )
    expected_nonpromotion = {
        "formal_credit": 0,
        "formal_remaining_origins": 80,
        "compact_q_formal_remaining_origins": 54,
        "ledger_unchanged": True,
        "D02": "BLOCKED",
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    need(same(nonpromotion, expected_nonpromotion), "candidate zero-credit boundary")
    need(same(result.get("frozen_inputs"), reference["inputs"]), "candidate frozen input pins")

    registry = reference["registry"]
    expected_selection = {
        "origin_key": ORIGIN,
        "Round184_priority_class": registry["priority_class"],
        "Round184_priority_ordinal": registry["priority_ordinal"],
        "selection_uses_new_closure_outcome": False,
        "representative_only": True,
    }
    need(same(result.get("representative_selection"), expected_selection), "candidate representative selection")

    analytic = result.get("analytic_whole_origin_certificate")
    expected_analytic = reference["analytic"]["candidate"]
    need(type(analytic) is dict, "candidate analytic object")
    frozen = analytic.get("frozen_target_strictly_behind")
    need(
        type(frozen) is dict
        and frozen.get("target") == FROZEN_TARGET,
        "candidate frozen target",
    )
    coarse = analytic.get("coarse_radical_witnesses")
    coordinate = analytic.get("coordinate_definitions")
    need(
        type(coarse) is dict
        and type(coordinate) is dict
        and coarse.get("q_squared_exact_maximum")
        == expected_analytic["coarse_radical_witnesses"]["q_squared_exact_maximum"]
        and coordinate.get("q") == expected_analytic["coordinate_definitions"]["q"],
        "candidate compact K",
    )
    need(
        same(analytic.get("exact_domain"), expected_analytic["exact_domain"]),
        "candidate domain cuts",
    )
    need(
        same(coordinate, expected_analytic["coordinate_definitions"])
        and same(coarse, expected_analytic["coarse_radical_witnesses"]),
        "candidate independent radical derivation",
    )
    need(
        same(frozen, expected_analytic["frozen_target_strictly_behind"]),
        "candidate frozen-behind inequality",
    )
    future = analytic.get("certified_nonfrozen_strict_future_root")
    need(
        type(future) is dict
        and future.get("target") == FUTURE_TARGET
        and future.get("radius_minus_absolute_transverse_strict_lower")
        == expected_analytic["certified_nonfrozen_strict_future_root"][
            "radius_minus_absolute_transverse_strict_lower"
        ]
        and future.get("forward_projection_strict_lower")
        == expected_analytic["certified_nonfrozen_strict_future_root"][
            "forward_projection_strict_lower"
        ],
        "candidate future-root margin",
    )
    need(
        same(future, expected_analytic["certified_nonfrozen_strict_future_root"]),
        "candidate future-root theorem",
    )
    need(
        same(analytic.get("first_hit_logic"), expected_analytic["first_hit_logic"]),
        "candidate first-hit logic",
    )

    boxes = result.get("root_box_partition")
    serialized_boxes = reference["face"]["serialized_boxes"]
    expected_boxes = {
        "root_box_count": len(serialized_boxes),
        "root_box_rows_sha256": digest(serialized_boxes),
        "root_box_rows": serialized_boxes,
        "exact_8_by_1_by_2_cartesian_cover": True,
    }
    need(same(boxes, expected_boxes), "candidate dynamic root boxes")

    ownership = result.get("cross_root_half_open_owner_partition")
    expected_ownership = reference["atoms"]
    need(type(ownership) is dict, "candidate owner partition object")
    need(ownership.get("rule") == expected_ownership["rule"], "candidate owner rule")
    need(
        same(ownership.get("owner_assignment_rows"), expected_ownership["owner_assignment_rows"]),
        "candidate atomic owner rows",
    )
    need(same(ownership, expected_ownership), "candidate atomic owner census")

    complement = result.get("targeted_upstream_complement_replay")
    expected_complement = reference["complement"]["candidate"]
    need(type(complement) is dict, "candidate complement object")
    need(
        complement.get("Round176_source_grazing_p_interval")
        == expected_complement["Round176_source_grazing_p_interval"]
        and complement.get("Round176_source_grazing_q_parameterization")
        == expected_complement["Round176_source_grazing_q_parameterization"]
        and complement.get("Round176_source_grazing_full_r_root_count") == 16,
        "candidate full-r bridge",
    )
    count_keys = (
        "Round176_frontier_root_count", "Round176_preclosed_root_count",
        "Round176_residual_root_count", "Round180_final_child_count",
        "exact_behind_closed_child_count", "exact_behind_residual_child_count",
    )
    need(
        all(complement.get(key) == expected_complement[key] for key in count_keys),
        "candidate complement counts",
    )
    need(same(complement, expected_complement), "candidate exact upstream complement")

    expected_conclusion = {
        "origin_key": ORIGIN,
        "analytic_disposition": "EXCLUDED_FROZEN_OWNER_STRICTLY_BEHIND",
        "whole_origin_domain_closed": True,
        "all_3D_2D_1D_0D_strata_closed": True,
        "Round176_preclosed_plus_Round180_exact_behind_plus_analytic_q_cover_is_complete": True,
        "conditional_research_transition": "54 -> 53",
        "scope": "one representative compact-q origin only",
    }
    need(same(result.get("representative_conclusion"), expected_conclusion), "candidate representative conclusion")
    next_gate = result.get("next_core_gate")
    need(
        type(next_gate) is str
        and "independently verify this representative theorem" in next_gate
        and "all 54 compact-q origins" in next_gate,
        "candidate no cohort overextension",
    )


def verify_candidate_path(
    path: Path,
    reference: dict[str, Any],
    require_default_pin: bool = True,
) -> tuple[dict[str, Any], str]:
    raw, _identity = capture_regular(path, "candidate stdout", 2 << 20)
    if require_default_pin:
        need(canonical_path(path, "candidate stdout authority") == DEFAULT_CANDIDATE, "candidate fixed path")
        need(sha256(raw) == DEFAULT_CANDIDATE_SHA256, "candidate byte pin")
    document = decode_candidate(raw)
    validate_candidate(document, reference)
    return document, sha256(raw)


def negative_smoke() -> dict[str, Any]:
    rejected: list[str] = []
    cases = {
        "duplicate_key": b'{"x":1,"x":2}\n',
        "trailing_document": b'{"x":1}\n{}\n',
        "noncanonical_space": b'{"x":1} \n',
        "floating_number": b'{"x":1.0}\n',
    }
    for name, raw in cases.items():
        try:
            decode_candidate(raw)
        except Reject:
            rejected.append(name)
        else:
            raise Reject("negative smoke accepted:" + name)
    need(len(rejected) == len(cases), "negative smoke count")
    return {
        "schema": VERIFICATION_SCHEMA + ".negative-smoke.v1",
        "status": "PASS_4_OF_4_NEGATIVE_SMOKE_CASES_REJECTED",
        "rejected": rejected,
        "formal_credit": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", nargs="?", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--smoke", action="store_true")
    arguments = parser.parse_args()
    if arguments.smoke:
        print(canonical(negative_smoke()).decode("utf-8"))
        return 0
    try:
        reference = reconstruct_reference()
        document, candidate_hash = verify_candidate_path(arguments.candidate, reference)
        self_raw, _identity = capture_regular(Path(__file__), "independent verifier source", 4 << 20)
        output = {
            "schema": VERIFICATION_SCHEMA,
            "status": (
                "PASS_INDEPENDENT_C30Q0_REPRESENTATIVE_ANALYTIC_THEOREM__"
                "16_ROOT_BOXES__255_ATOMIC_STRATA__46_TO_44_TO_328_TO_327_PLUS_1__"
                "ZERO_FORMAL_CREDIT"
            ),
            "verifier_sha256": sha256(self_raw),
            "candidate": {
                "path": os.fspath(canonical_path(arguments.candidate, "candidate output")),
                "sha256": candidate_hash,
                "result_sha256": document["result_sha256"],
            },
            "producer": {
                "path": PRODUCER.name,
                "sha256": reference["producer_sha256"],
                "imported_or_executed": reference["producer_executed_or_imported"],
            },
            "independent_reconstruction": {
                "origin_key": ORIGIN,
                "dynamic_t_cuts": [str(value) for value in reference["face"]["t_cuts"]],
                "dynamic_s_cuts": [str(value) for value in reference["face"]["s_cuts"]],
                "root_box_count": len(reference["face"]["boxes"]),
                "atomic_stratum_count": reference["atoms"]["atomic_stratum_count"],
                "atomic_stratum_count_by_dimension": reference["atoms"]["atomic_stratum_count_by_dimension"],
                "owner_assignment_rows_sha256": reference["atoms"]["owner_assignment_rows_sha256"],
                "derived_K": str(reference["complement"]["k"]),
                "frozen_owner_in_upstream_workload": reference["complement"]["frozen_owner_in_workload"],
                "frozen_projection_strict_upper": "-1/2",
                "future_projection_strict_lower": str(reference["analytic"]["ell_lower"]),
                "future_transverse_radius_margin": str(reference["analytic"]["transverse_margin"]),
                "future_time_one_polynomial_half_strict_upper": str(
                    reference["analytic"]["time_one_polynomial_half_upper"]
                ),
                "upstream_count_chain": [46, 44, 328, 327, 1],
            },
            "formal_credit": 0,
            "formal_remaining_origins": 80,
            "compact_q_formal_remaining_origins": 54,
            "conditional_research_transition_only": "54 -> 53",
            "CM2": "NO-GO_FOR_CLAIM",
        }
    except (Reject, OSError, KeyError, TypeError, ValueError) as error:
        print(canonical({
            "schema": VERIFICATION_SCHEMA,
            "status": "FAIL_CLOSED_INDEPENDENT_C30Q0_VERIFICATION",
            "error": type(error).__name__ + ":" + str(error),
            "formal_credit": 0,
        }).decode("utf-8"))
        return 1
    print(canonical(output).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
