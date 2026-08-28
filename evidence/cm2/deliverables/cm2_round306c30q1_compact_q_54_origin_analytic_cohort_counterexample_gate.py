#!/usr/bin/env python3
"""Fail-closed, zero-credit cohort census for all 54 compact-q origins.

This additive probe does not promote an origin and does not modify a ledger.
It selects the compact-q cohort from the outcome-blind Round184 registry,
replays the pinned Round176/Round180/P215 complement, reconstructs every
Round218 source-grazing root, and tests the representative C30q0 analytic
criterion on every exact root domain.  A failed root or a non-unique residual
is an explicit counterexample to extending the representative theorem.

All input files are captured once through no-follow directory descriptors
before use and are recaptured after the computation.  The output is one
canonical JSON document on stdout; progress is written to stderr.
"""

from __future__ import annotations

from collections import Counter, defaultdict
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

from flint import arb, ctx


HERE = Path(__file__).absolute().parent
WORKSPACE = HERE.parent
SCHEMA = (
    "cm2.round306c30q1.compact-q-54-origin-analytic-cohort-"
    "counterexample-gate.v1"
)
COMPACT_CLASS = "COMPACT_Q_PRESENT"
COMPACT_CATEGORY = "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
FROZEN_OWNER = "W[1,0]"
EXPECTED_ORIGINS = 54
EXPECTED_KEYS_SHA256 = (
    "d5fd64dc6d287982b6bf6739295869a21991b758917754eea3aa55476e504e7b"
)
EXPECTED_FACE_ROOTS = 844
EXPECTED_FINAL_CHILDREN = 21_334
EXPECTED_CLOSED_CHILDREN = 18_782
EXPECTED_RESIDUAL_CHILDREN = 2_552

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
    HERE / "cm2_round218_source_w_compact_q_source_stratum_frontier_result.json"
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
ROUND215_PROBE = HERE / "cm2_round215_source_w_mixed_algebraic_blocker_probe.py"
ROUND215_PROBE_SHA256 = (
    "463dfe832b32459b356bdfa0602c5eacea82569734f7ad1016c97ffa9d6c40c1"
)
ROUND180_VERIFIER = (
    HERE / "cm2_round180_full_multi_residual_dimension_safe_partial_verifier.py"
)
ROUND180_VERIFIER_SHA256 = (
    "12e25ebe0bae92cd8bda5cc3c00c7c3c94dda01ded5042c6e7a09152f840d6a4"
)
ROUND176_VERIFIER = (
    HERE / "cm2_round176_dimension_safe_multi_origin_parent_exclusion_verifier.py"
)
ROUND176_VERIFIER_SHA256 = (
    "f1297881f724cb0a2087ebbfa6961a95750dffa751c003879eb2e14714581796"
)
GEOMETRY_REGISTRY = HERE / "cm2_gate3_candidate_first_hit_cert.py"
GEOMETRY_REGISTRY_SHA256 = (
    "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
)

DIRECT_PINS = {
    ROUND184_MANIFEST: ROUND184_MANIFEST_SHA256,
    ROUND184_CERTIFICATE: ROUND184_CERTIFICATE_SHA256,
    ROUND218_MANIFEST: ROUND218_MANIFEST_SHA256,
    ROUND218_RESULT: ROUND218_RESULT_SHA256,
    ROUND218_REPLAY: ROUND218_REPLAY_SHA256,
    ROUND215_PROBE: ROUND215_PROBE_SHA256,
    ROUND180_VERIFIER: ROUND180_VERIFIER_SHA256,
    ROUND176_VERIFIER: ROUND176_VERIFIER_SHA256,
    GEOMETRY_REGISTRY: GEOMETRY_REGISTRY_SHA256,
}


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


def progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


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


def capture_no_follow(
    path: Path,
    label: str,
    maximum: int = 64 << 20,
) -> tuple[bytes, dict[str, Any]]:
    """Capture one regular file while anchoring every ancestor descriptor."""
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.is_relative_to(WORKSPACE), "workspace path:" + label)
    parts = absolute.parts
    need(parts and parts[0] == os.sep and len(parts) > 1, "absolute path:" + label)
    flags_dir = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_DIRECTORY", 0)
    flags_file = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    directory = os.open(os.sep, flags_dir)
    chain: list[tuple[str, tuple[int, int, int, int, int, int, int]]] = []
    try:
        chain.append((os.sep, stat_identity(os.fstat(directory))))
        for component in parts[1:-1]:
            need(component not in {"", ".", ".."}, "ancestor component:" + label)
            child = os.open(
                component,
                flags_dir | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=directory,
            )
            os.close(directory)
            directory = child
            status = os.fstat(directory)
            need(stat.S_ISDIR(status.st_mode), "ancestor directory:" + label)
            chain.append((component, stat_identity(status)))
        parent_before = stat_identity(os.fstat(directory))
        name = parts[-1]
        before_path = os.stat(name, dir_fd=directory, follow_symlinks=False)
        need(
            stat.S_ISREG(before_path.st_mode)
            and before_path.st_nlink == 1
            and 0 < before_path.st_size <= maximum,
            "regular singleton bounds:" + label,
        )
        descriptor = os.open(name, flags_file, dir_fd=directory)
        try:
            before = os.fstat(descriptor)
            need(
                stat_identity(before) == stat_identity(before_path),
                "path/fd identity:" + label,
            )
            chunks: list[bytes] = []
            size = 0
            while block := os.read(descriptor, 1 << 20):
                chunks.append(block)
                size += len(block)
                need(size <= maximum, "capture maximum:" + label)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        after_path = os.stat(name, dir_fd=directory, follow_symlinks=False)
        parent_after = stat_identity(os.fstat(directory))
    except OSError as error:
        raise Reject("no-follow capture:" + label) from error
    finally:
        os.close(directory)
    raw = b"".join(chunks)
    identity = stat_identity(before)
    need(
        identity == stat_identity(after) == stat_identity(after_path)
        and parent_before == parent_after
        and len(raw) == before.st_size,
        "stable capture:" + label,
    )
    return raw, {
        "file": list(identity),
        "parent": list(parent_before),
        "ancestor_chain_sha256": digest(
            [[name, list(item)] for name, item in chain]
        ),
    }


def capture_direct_pins() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path, expected in sorted(DIRECT_PINS.items(), key=lambda item: item[0].name):
        raw, identity = capture_no_follow(path, "direct pin:" + path.name)
        actual = sha256(raw)
        need(actual == expected, "direct byte pin:" + path.name)
        result[path.name] = {"sha256": actual, "identity": identity}
    return result


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def decode_json(raw: bytes, label: str) -> dict[str, Any]:
    def reject(value: str) -> None:
        raise Reject("invalid JSON number:" + label + ":" + value)

    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique_object,
            parse_constant=reject,
            parse_float=reject,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, Reject) as error:
        raise Reject("strict JSON:" + label) from error
    need(type(value) is dict, "JSON object:" + label)
    return value


def parse_fraction(value: Any, label: str) -> Q:
    need(type(value) is str, "rational string:" + label)
    try:
        result = Q(value)
    except (ValueError, ZeroDivisionError) as error:
        raise Reject("rational parse:" + label) from error
    need(str(result) == value, "canonical rational:" + label)
    return result


def verify_manifest(path: Path, expected_hash: str, label: str) -> dict[str, str]:
    raw, _identity = capture_no_follow(path, label + " manifest", 128 << 10)
    need(sha256(raw) == expected_hash, label + " manifest pin")
    try:
        lines = raw.decode("ascii", "strict").splitlines()
    except UnicodeDecodeError as error:
        raise Reject(label + " manifest ASCII") from error
    need(bool(lines) and raw.endswith(b"\n"), label + " manifest syntax")
    entries: dict[str, str] = {}
    for line in lines:
        parts = line.split("  ", 1)
        need(len(parts) == 2, label + " manifest line")
        value, filename = parts
        need(
            len(value) == 64
            and all(character in "0123456789abcdef" for character in value)
            and filename not in entries
            and filename not in {".", ".."}
            and "/" not in filename
            and "\\" not in filename,
            label + " manifest member",
        )
        member, _member_identity = capture_no_follow(
            HERE / filename, label + " member:" + filename
        )
        need(sha256(member) == value, label + " member pin:" + filename)
        entries[filename] = value
    return entries


def closed_row(row: dict[str, Any], label: str) -> None:
    need(type(row.get("row_sha256")) is str, label + " digest field")
    body = {key: value for key, value in row.items() if key != "row_sha256"}
    need(digest(body) == row["row_sha256"], label + " digest")


def bounds(value: arb) -> dict[str, str]:
    return {
        "enclosure": str(value),
        "lower": str(value.lower()),
        "upper": str(value.upper()),
    }


def map_counter(value: Counter[Any]) -> dict[str, int]:
    return {str(key): value[key] for key in sorted(value, key=lambda item: str(item))}


def box_row(box: Any) -> dict[str, list[str]]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
    }


def contained(child: Any, parent: Any) -> bool:
    return (
        parent.t0 <= child.t0 <= child.t1 <= parent.t1
        and parent.p0 <= child.p0 <= child.p1 <= parent.p1
        and parent.s0 <= child.s0 <= child.s1 <= parent.s1
    )


def load_authorities() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    entries184 = verify_manifest(ROUND184_MANIFEST, ROUND184_MANIFEST_SHA256, "Round184")
    entries218 = verify_manifest(ROUND218_MANIFEST, ROUND218_MANIFEST_SHA256, "Round218")
    need(
        entries184.get(ROUND184_CERTIFICATE.name) == ROUND184_CERTIFICATE_SHA256,
        "Round184 certificate manifest binding",
    )
    need(
        entries218.get(ROUND218_RESULT.name) == ROUND218_RESULT_SHA256
        and entries218.get(ROUND218_REPLAY.name) == ROUND218_REPLAY_SHA256,
        "Round218 result/replay manifest binding",
    )
    raw184, _ = capture_no_follow(ROUND184_CERTIFICATE, "Round184 certificate")
    raw218, _ = capture_no_follow(ROUND218_RESULT, "Round218 result")
    document184 = decode_json(raw184, "Round184 certificate")
    document218 = decode_json(raw218, "Round218 result")
    need(
        document184.get("result_sha256") == ROUND184_RESULT_SHA256
        and digest(document184.get("result")) == ROUND184_RESULT_SHA256,
        "Round184 inner result closure",
    )
    need(
        document218.get("result_sha256") == ROUND218_INNER_SHA256
        and digest(document218.get("result")) == ROUND218_INNER_SHA256,
        "Round218 inner result closure",
    )
    all_registry = document184["result"]["priority_registry"]["rows"]
    registry = sorted(
        (row for row in all_registry if row.get("priority_class") == COMPACT_CLASS),
        key=lambda row: row["priority_ordinal"],
    )
    keys = sorted(row["origin_key"] for row in registry)
    need(
        len(registry) == EXPECTED_ORIGINS
        and len(set(keys)) == EXPECTED_ORIGINS
        and digest(keys) == EXPECTED_KEYS_SHA256
        and all(row.get("selection_uses_new_closure_outcome") is False for row in registry),
        "outcome-blind Round184 compact54 census",
    )
    faces = document218["result"]["source_grazing_face_analysis"]["face_rows"]
    need(len(faces) == EXPECTED_FACE_ROOTS, "Round218 face row count")
    for row in faces:
        closed_row(row, "Round218 face row")
        need(
            row.get("origin_key") in set(keys)
            and row.get("face_box", {}).get("r") == ["0", "0"]
            and row.get("whole_origin_integer_credit") == 0,
            "Round218 face semantics",
        )
    need(
        digest(faces)
        == document218["result"]["source_grazing_face_analysis"]["face_evidence_rows_sha256"],
        "Round218 face list closure",
    )
    return registry, sorted(faces, key=lambda row: row["root_key"]), {
        "Round184_manifest_sha256": ROUND184_MANIFEST_SHA256,
        "Round184_manifest_member_count": len(entries184),
        "Round184_result_sha256": ROUND184_RESULT_SHA256,
        "Round218_manifest_sha256": ROUND218_MANIFEST_SHA256,
        "Round218_manifest_member_count": len(entries218),
        "Round218_result_file_sha256": ROUND218_RESULT_SHA256,
        "Round218_result_sha256": ROUND218_INNER_SHA256,
    }


def load_definitions() -> Any:
    if os.fspath(HERE) not in sys.path:
        sys.path.insert(0, os.fspath(HERE))
    module = importlib.import_module(ROUND218_REPLAY.stem)
    need(Path(module.__file__).absolute() == ROUND218_REPLAY, "Round218 module identity")
    need(Path(module.p215.__file__).absolute() == ROUND215_PROBE, "P215 module identity")
    need(Path(module.r180.__file__).absolute() == ROUND180_VERIFIER, "Round180 module identity")
    need(Path(module.r176.__file__).absolute() == ROUND176_VERIFIER, "Round176 module identity")
    need(
        Path(module.r176.base.__file__).absolute() == GEOMETRY_REGISTRY,
        "geometry registry module identity",
    )
    for path, expected in DIRECT_PINS.items():
        raw, _identity = capture_no_follow(path, "post-import pin:" + path.name)
        need(sha256(raw) == expected, "post-import byte pin:" + path.name)
    need(module.r176.FROZEN_OWNER == FROZEN_OWNER, "frozen owner definition")
    return module


def replay_complement(
    probe: Any,
    registry: list[dict[str, Any]],
    pinned_faces: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], Q, dict[str, Any]]:
    compact = {row["origin_key"]: row for row in registry}
    progress("C30q1 replay Round176 compact54 frontier")
    state = probe.r176.replay_frontier()
    frontier: dict[str, list[Any]] = defaultdict(list)
    preclosed: Counter[str] = Counter()
    preclosed_kinds: dict[str, set[str]] = defaultdict(set)
    preclosed_kinds.update({
        key: set(value)
        for key, value in state["origin_kinds"].items()
        if key in compact
    })
    for row in state["frontier"]:
        if row.origin_key not in compact:
            continue
        kind, _evidence = probe.r176.closure(row)
        if kind is None:
            frontier[row.origin_key].append(row)
        else:
            preclosed[row.origin_key] += 1
            preclosed_kinds[row.origin_key].add(kind)
    need(set(frontier) == set(compact), "all compact origins replayed")
    for rows in frontier.values():
        rows.sort(key=lambda row: row.key)

    analytic_roots: list[Any] = []
    for rows in frontier.values():
        analytic_roots.extend(
            row for row in rows
            if probe.r180.initial_category(row) == COMPACT_CATEGORY
        )
    analytic_roots.sort(key=lambda row: row.key)
    need(len(analytic_roots) == EXPECTED_FACE_ROOTS, "dynamic source-grazing root count")
    dynamic_faces = sorted(
        (probe.q_face_evidence(row) for row in analytic_roots),
        key=lambda row: row["root_key"],
    )
    need(canonical(dynamic_faces) == canonical(pinned_faces), "dynamic Round218 face replay")

    k_values: set[Q] = set()
    for row in analytic_roots:
        need(row.box.p1 == 1 or row.box.p0 == -1, "compact endpoint sign:" + row.key)
        lower_abs = row.box.p0 if row.box.p1 == 1 else -row.box.p1
        need(Q(0) < lower_abs < 1, "compact p endpoint:" + row.key)
        k_values.add(Q(1) - lower_abs * lower_abs)
    need(len(k_values) == 1, "single dynamically derived q-squared scale")
    k = next(iter(k_values))
    roots_by_origin: dict[str, list[Any]] = defaultdict(list)
    for row in analytic_roots:
        roots_by_origin[row.origin_key].append(row)

    origin_rows: list[dict[str, Any]] = []
    total_final = total_closed = total_residual = 0
    all_residual_containment = Counter()
    for index, origin in enumerate(sorted(compact), 1):
        authority = compact[origin]
        unresolved = frontier[origin]
        need(
            len(unresolved) == authority["Round176_residual_root_count"]
            and preclosed[origin] == authority["Round176_preclosed_frontier_count"]
            and sorted(preclosed_kinds[origin]) == authority["Round176_preclosed_kinds"],
            "Round176 registry replay:" + origin,
        )
        refinement = probe.r180.refine_origin(unresolved, 4)
        children = sorted(refinement["final_residual_rows"], key=lambda row: row.key)
        categories = Counter(probe.r180.residual_category(row) for row in children)
        need(
            len(children) == authority["Round180_residual_child_count"]
            and digest([row.key for row in children])
            == authority["Round180_residual_child_keys_sha256"]
            and map_counter(categories) == authority["Round180_residual_category_count"],
            "Round180 registry replay:" + origin,
        )
        residual: list[dict[str, Any]] = []
        closed = 0
        for child in children:
            category = probe.r180.residual_category(child)
            reduction = probe.p215.exact_behind_reduce(child, category)
            if reduction["closed"]:
                closed += 1
                continue
            containers = sorted(
                root.key for root in roots_by_origin[origin]
                if contained(child.box, root.box)
            )
            all_residual_containment[len(containers)] += 1
            residual.append({
                "cell_key": child.key,
                "category": category,
                "active_targets": list(child.active_targets),
                "box": box_row(child.box),
                "analytic_root_container_count": len(containers),
                "analytic_root_containers": containers,
                "residual_reason": reduction["residual_reason"],
            })
        total_final += len(children)
        total_closed += closed
        total_residual += len(residual)
        unique = (
            len(residual) == 1
            and residual[0]["category"] == COMPACT_CATEGORY
            and residual[0]["analytic_root_container_count"] == 1
        )
        origin_rows.append({
            "origin_key": origin,
            "Round176_frontier_root_count": len(unresolved) + preclosed[origin],
            "Round176_preclosed_root_count": preclosed[origin],
            "Round176_residual_root_count": len(unresolved),
            "source_grazing_root_count": len(roots_by_origin[origin]),
            "Round180_final_child_count": len(children),
            "Round180_final_category_count": map_counter(categories),
            "P215_exact_behind_closed_child_count": closed,
            "P215_residual_child_count": len(residual),
            "P215_residual_category_count": map_counter(Counter(row["category"] for row in residual)),
            "residual_rows_sha256": digest(residual),
            "residual_witnesses": residual[:3],
            "unique_compact_residual_in_exactly_one_root_box": unique,
        })
        if index % 6 == 0 or index == EXPECTED_ORIGINS:
            progress(f"C30q1 complement origins {index}/{EXPECTED_ORIGINS}")
    need(
        total_final == EXPECTED_FINAL_CHILDREN
        and total_closed == EXPECTED_CLOSED_CHILDREN
        and total_residual == EXPECTED_RESIDUAL_CHILDREN,
        "Round218 complement conservation",
    )
    root_rows = [
        {
            "origin_key": row.origin_key,
            "root_key": row.key,
            "source_chart": row.chart_id,
            "p_sign": 1 if row.box.p1 == 1 else -1,
            "active_targets": list(row.active_targets),
            "box": box_row(row.box),
        }
        for row in analytic_roots
    ]
    return origin_rows, root_rows, k, {
        "Round176_source_grazing_root_count": len(analytic_roots),
        "Round180_final_child_count": total_final,
        "P215_exact_behind_closed_child_count": total_closed,
        "P215_residual_child_count": total_residual,
        "residual_analytic_root_container_multiplicity": map_counter(all_residual_containment),
    }


def metric(probe: Any, geometry: tuple[Any, ...], target_id: str) -> dict[str, Any]:
    qx, qy, ux, uy, s, _compact_q = geometry
    target = probe.r176.TARGETS[target_id]
    ax, ay = probe.r176.base.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    radius = probe.r176.base.arbq(probe.r176.base.RADIUS[target.obstacle])
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    f0 = dx * dx + dy * dy - radius * radius
    f1 = (dx - ux) * (dx - ux) + (dy - uy) * (dy - uy) - radius * radius
    discriminant = radius * radius - transverse * transverse
    transverse_margin = radius - abs(transverse)
    return {
        "target": target_id,
        "target_definition": {
            "obstacle": target.obstacle,
            "ix": target.ix,
            "iy": target.iy,
            "radius": str(probe.r176.base.RADIUS[target.obstacle]),
        },
        "forward_projection_ell": bounds(ell),
        "f_at_0": bounds(f0),
        "f_at_1": bounds(f1),
        "transverse": bounds(transverse),
        "radius_minus_abs_transverse": bounds(transverse_margin),
        "discriminant": bounds(discriminant),
        "strict": {
            "ell_negative": bool(ell < 0),
            "f_at_0_positive": bool(f0 > 0),
            "f_at_1_negative": bool(f1 < 0),
            "transverse_margin_positive": bool(transverse_margin > 0),
            "discriminant_positive": bool(discriminant > 0),
        },
    }


def analytic_census(
    probe: Any,
    roots: list[dict[str, Any]],
    k: Q,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    progress("C30q1 evaluate exact analytic root domains")
    root_results: list[dict[str, Any]] = []
    for row in roots:
        source_box = row["box"]
        qbox = probe.r176.QBox(
            parse_fraction(source_box["t"][0], "root t0"),
            parse_fraction(source_box["t"][1], "root t1"),
            Q(0),
            Q(1),
            parse_fraction(source_box["s"][0], "root s0"),
            parse_fraction(source_box["s"][1], "root s1"),
            0,
        )
        geometry = probe.r176.q_geometry(row["source_chart"], row["p_sign"], qbox)
        frozen = metric(probe, geometry, FROZEN_OWNER)
        frozen_pass = (
            frozen["strict"]["f_at_0_positive"]
            and frozen["strict"]["ell_negative"]
        )
        future = [
            metric(probe, geometry, target)
            for target in row["active_targets"]
            if target != FROZEN_OWNER
        ]
        future_witnesses = [
            item["target"] for item in future
            if item["strict"]["f_at_0_positive"]
            and item["strict"]["f_at_1_negative"]
            and item["strict"]["transverse_margin_positive"]
            and item["strict"]["discriminant_positive"]
        ]
        failures: list[str] = []
        if not frozen["strict"]["f_at_0_positive"]:
            failures.append("FROZEN_F_AT_0_NOT_CERTIFIED_POSITIVE")
        if not frozen["strict"]["ell_negative"]:
            failures.append("FROZEN_NOT_CERTIFIED_STRICTLY_BEHIND")
        if not future_witnesses:
            failures.append("NO_NONFROZEN_F0_POSITIVE_F1_NEGATIVE_TRANSVERSE_WITNESS")
        p_abs_lower = row["box"]["p"][0] if row["p_sign"] > 0 else row["box"]["p"][1]
        root_results.append({
            "origin_key": row["origin_key"],
            "root_key": row["root_key"],
            "cohort_parameters": {
                "source_chart": row["source_chart"],
                "p_sign": row["p_sign"],
                "active_target_set": row["active_targets"],
                "exact_t_domain": row["box"]["t"],
                "exact_s_domain": row["box"]["s"],
                "exact_r_domain": ["0", "1"],
                "exact_q_squared_scale": str(k),
                "exact_q_parameterization": "q=sqrt(" + str(k) + ")*r",
                "exact_p_parameterization": (
                    ("+" if row["p_sign"] > 0 else "-")
                    + "sqrt(1-(" + str(k) + ")*r^2)"
                ),
                "source_p_endpoint_domain": row["box"]["p"],
                "derived_abs_p_endpoint_near_q0": p_abs_lower,
            },
            "frozen_target": frozen,
            "future_targets": future,
            "certified_future_witness_targets": future_witnesses,
            "analytic_root_applicable": frozen_pass and bool(future_witnesses),
            "failure_reasons": failures,
        })

    groups: dict[bytes, list[dict[str, Any]]] = defaultdict(list)
    for row in root_results:
        groups[canonical(row["cohort_parameters"])].append(row)
    cohorts: list[dict[str, Any]] = []
    for signature, members in sorted(groups.items(), key=lambda item: item[0]):
        first = members[0]
        inequality_bundle = {
            "frozen_target": first["frozen_target"],
            "future_targets": first["future_targets"],
            "certified_future_witness_targets": first["certified_future_witness_targets"],
        }
        need(
            all(
                canonical({
                    "frozen_target": row["frozen_target"],
                    "future_targets": row["future_targets"],
                    "certified_future_witness_targets": row["certified_future_witness_targets"],
                }) == canonical(inequality_bundle)
                for row in members
            ),
            "cohort geometric equality",
        )
        member_rows = sorted(
            ({"origin_key": row["origin_key"], "root_key": row["root_key"]} for row in members),
            key=lambda row: (row["origin_key"], row["root_key"]),
        )
        cohorts.append({
            "cohort_id": sha256(signature),
            "parameters": first["cohort_parameters"],
            "member_count": len(member_rows),
            "member_rows_sha256": digest(member_rows),
            "member_rows": member_rows,
            "inequality_bundle": inequality_bundle,
            "applicable": all(row["analytic_root_applicable"] for row in members),
            "failure_reason_count": map_counter(
                Counter(reason for row in members for reason in row["failure_reasons"])
            ),
        })
    cohorts.sort(key=lambda row: row["cohort_id"])

    origins: list[dict[str, Any]] = []
    for origin in sorted({row["origin_key"] for row in root_results}):
        selected = [row for row in root_results if row["origin_key"] == origin]
        failures = Counter(reason for row in selected for reason in row["failure_reasons"])
        origins.append({
            "origin_key": origin,
            "analytic_root_count": len(selected),
            "applicable_root_count": sum(row["analytic_root_applicable"] for row in selected),
            "frozen_behind_root_count": sum(
                row["frozen_target"]["strict"]["ell_negative"] for row in selected
            ),
            "future_witness_root_count": sum(
                bool(row["certified_future_witness_targets"]) for row in selected
            ),
            "failure_reason_count": map_counter(failures),
            "all_analytic_roots_applicable": all(
                row["analytic_root_applicable"] for row in selected
            ),
        })
    summary = {
        "analytic_root_count": len(root_results),
        "cohort_count": len(cohorts),
        "applicable_cohort_count": sum(row["applicable"] for row in cohorts),
        "applicable_root_count": sum(row["analytic_root_applicable"] for row in root_results),
        "fully_applicable_origin_count": sum(row["all_analytic_roots_applicable"] for row in origins),
        "fully_applicable_origin_keys": [
            row["origin_key"] for row in origins if row["all_analytic_roots_applicable"]
        ],
        "failure_reason_count": map_counter(
            Counter(reason for row in root_results for reason in row["failure_reasons"])
        ),
    }
    return origins, cohorts, {"summary": summary, "root_results": root_results}


def rebuild() -> dict[str, Any]:
    initial_direct = capture_direct_pins()
    registry, pinned_faces, authority = load_authorities()
    probe = load_definitions()
    complement_origins, roots, k, complement_summary = replay_complement(
        probe, registry, pinned_faces
    )
    analytic_origins, cohorts, analytic = analytic_census(probe, roots, k)
    final_direct = capture_direct_pins()
    need(initial_direct == final_direct, "all direct inputs byte/identity stable")

    complement_by_origin = {row["origin_key"]: row for row in complement_origins}
    combined: list[dict[str, Any]] = []
    for analytic_row in analytic_origins:
        origin = analytic_row["origin_key"]
        complement = complement_by_origin[origin]
        applicable = (
            analytic_row["all_analytic_roots_applicable"]
            and complement["unique_compact_residual_in_exactly_one_root_box"]
        )
        reasons: list[str] = []
        if not analytic_row["all_analytic_roots_applicable"]:
            reasons.append("ANALYTIC_ROOT_COHORT_NOT_COVERED")
        if complement["P215_residual_child_count"] != 1:
            reasons.append("P215_COMPLEMENT_RESIDUAL_NOT_UNIQUE")
        if not complement["unique_compact_residual_in_exactly_one_root_box"]:
            reasons.append("UNIQUE_COMPACT_RESIDUAL_ROOT_BOX_CONTAINMENT_FAILED")
        combined.append({
            "origin_key": origin,
            "conditional_origin_applicable": applicable,
            "rejection_reasons": reasons,
            "analytic": analytic_row,
            "complement": complement,
        })
    rejected = [row for row in combined if not row["conditional_origin_applicable"]]
    complete = not rejected
    first = None
    if rejected:
        witness_origin = rejected[0]["origin_key"]
        root_witness = next(
            (
                row for row in analytic["root_results"]
                if row["origin_key"] == witness_origin
                and not row["analytic_root_applicable"]
            ),
            None,
        )
        first = {
            "origin_key": witness_origin,
            "origin_rejection_reasons": rejected[0]["rejection_reasons"],
            "first_failed_analytic_root": root_witness,
            "complement_residual_witnesses": rejected[0]["complement"]["residual_witnesses"],
        }
    status = (
        "PASS_CONDITIONAL_ALL_54_COHORT_COVERAGE__ZERO_FORMAL_CREDIT"
        if complete
        else "REJECT_ALL_54_EXTENSION_WITH_ORIGIN_WITNESS__ZERO_FORMAL_CREDIT"
    )
    return {
        "status": status,
        "verdict": "CONDITIONAL_COHORT_COVERAGE" if complete else "REJECT",
        "scope": "census-and-counterexample-gate-only",
        "frozen_inputs": {
            **authority,
            "Round218_replay_sha256": ROUND218_REPLAY_SHA256,
            "Round215_probe_sha256": ROUND215_PROBE_SHA256,
            "Round180_verifier_sha256": ROUND180_VERIFIER_SHA256,
            "Round176_verifier_sha256": ROUND176_VERIFIER_SHA256,
            "original_geometry_registry_sha256": GEOMETRY_REGISTRY_SHA256,
            "all_direct_inputs_single_capture_and_ancestor_chain_stable": True,
            "direct_input_capture_sha256": digest(initial_direct),
        },
        "outcome_blind_selection": {
            "priority_class": COMPACT_CLASS,
            "origin_count": len(registry),
            "origin_keys_sha256": digest(sorted(row["origin_key"] for row in registry)),
            "selection_uses_new_closure_outcome": False,
        },
        "dynamically_derived_q_parameterization": {
            "q_squared_scale": str(k),
            "q": "sqrt(" + str(k) + ")*r",
            "r_domain": ["0", "1"],
            "not_a_copied_representative_constant": True,
        },
        "pinned_complement_replay": {
            **complement_summary,
            "origin_rows_sha256": digest(complement_origins),
            "origin_rows": complement_origins,
        },
        "analytic_cohort_census": {
            **analytic["summary"],
            "cohort_rows_sha256": digest(cohorts),
            "cohort_rows": cohorts,
            "root_results_sha256": digest(analytic["root_results"]),
            "root_results": analytic["root_results"],
        },
        "combined_origin_gate": {
            "origin_count": len(combined),
            "conditionally_applicable_origin_count": sum(
                row["conditional_origin_applicable"] for row in combined
            ),
            "rejected_origin_count": len(rejected),
            "origin_rows_sha256": digest(combined),
            "origin_rows": combined,
            "first_fail_closed_origin_witness": first,
            "all_54_covered": complete,
        },
        "strict_nonpromotion": {
            "formal_credit": 0,
            "formal_remaining_origins": 80,
            "compact_q_formal_remaining_origins": 54,
            "ledger_unchanged": True,
            "no_seal_or_release_authority": True,
            "D02": "BLOCKED",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "interpretation": (
            "A PASS is conditional cohort coverage only; a REJECT falsifies "
            "extension of the C30q0 representative sufficient criterion. "
            "Neither outcome grants formal credit."
        ),
    }


def main() -> int:
    ctx.prec = 192
    try:
        result = rebuild()
        document = {"schema": SCHEMA, "result": result}
        document["result_sha256"] = digest(result)
        sys.stdout.buffer.write(canonical(document) + b"\n")
        return 0
    except Reject as error:
        print("REJECT_C30Q1_PROBE_INTEGRITY:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
