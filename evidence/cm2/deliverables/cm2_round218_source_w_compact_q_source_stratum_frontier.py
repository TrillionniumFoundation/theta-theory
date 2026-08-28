#!/usr/bin/env python3
"""Bounded source-stratum probe for the frozen compact-q source-W cohort.

The probe selects the 54 COMPACT_Q_PRESENT origins from the frozen,
outcome-blind Round184 registry.  It independently replays their Round176
frontier and Round180 depth-four refinement, rechecks the Round201
exact-behind outer reduction, and then studies the original compact-q
source-grazing roots in

    q = sqrt(1023/262144) * r,
    p = sign * sqrt(1 - (1023/262144) * r^2),  r in [0, 1].

The open r>0 stratum is three-dimensional.  The r=0 face is kept as a
two-dimensional proof object with deterministic half-open ownership of every
atomic edge and corner.  A bounded depth-ten q tree records the maximally
closed 3D cells and exact residual obstruction.  No cell, volume, face, edge,
corner, or source-grazing stratum is converted into whole-origin credit.

This is a read-only probe.  It has no output argument, performs no filesystem
writes, prints progress to stderr, and emits one canonical JSON object to
stdout.
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
from typing import Any

sys.dont_write_bytecode = True

from flint import ctx


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round218.source-w-compact-q-source-stratum-frontier.v1"

ROUND215_PROBE = (
    "cm2_round215_source_w_mixed_algebraic_blocker_probe.py"
)
ROUND215_PROBE_SHA256 = (
    "463dfe832b32459b356bdfa0602c5eacea82569734f7ad1016c97ffa9d6c40c1"
)
ROUND215_PREFIX = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion"
)
ROUND215_MANIFEST = f"{ROUND215_PREFIX}_manifest.sha256"
ROUND215_MANIFEST_SHA256 = (
    "6a6463c2574b971ce6909593886f6ad4c23bddb232772fdacebb4ecca70a405a"
)
ROUND215_CERTIFICATE_RESULT_SHA256 = (
    "39d38cda12566e25b341b861e0e1ee379138aa465424254a6b60ea35da5629ee"
)
ROUND215_VERIFICATION_RESULT_SHA256 = (
    "f6fd2b6927d003f216dac1caf24452149283286227475cab423aa8fde77e960d"
)

COMPACT_CLASS = "COMPACT_Q_PRESENT"
Q_CATEGORY = "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
EXPECTED_COMPACT_KEYS_SHA256 = (
    "d5fd64dc6d287982b6bf6739295869a21991b758917754eea3aa55476e504e7b"
)
EXPECTED_INITIAL_CATEGORY_COUNT = {
    "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH": 164,
    "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY": 762,
    "MULTI_DISCRIMINANT_2_TO_5_TARGETS": 460,
    "SOURCE_GRAZING_COMPACT_Q_RESIDUAL": 844,
}
EXPECTED_FINAL_CATEGORY_COUNT = {
    "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH": 1_658,
    "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY": 8_428,
    "MULTI_DISCRIMINANT_2_TO_5_TARGETS": 5_210,
    "SOURCE_GRAZING_COMPACT_Q_RESIDUAL": 5_862,
    "TYPED_TANGENCY_PLUS_OUTGOING_SEAM_DOUBLE_GRAPH": 176,
}
EXPECTED_COMPACT_ORIGINS = 54
EXPECTED_PRECLOSED_FRONTIER = 114
EXPECTED_INITIAL_RESIDUAL_ROOTS = 2_230
EXPECTED_FINAL_CHILDREN = 21_334
EXPECTED_GEOMETRIC_CLOSED = 18_782
EXPECTED_GEOMETRIC_RESIDUAL = 2_552
EXPECTED_DELETED_CANDIDATES = 35_852
EXPECTED_FAILED_CANDIDATES = 3_692
MAX_Q_DEPTH = 10


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


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


def progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def map_counter(value: Counter[Any]) -> dict[str, int]:
    return {
        str(key): value[key]
        for key in sorted(value, key=lambda item: str(item))
    }


def fraction_map(value: dict[str, Q]) -> dict[str, str]:
    return {key: str(item) for key, item in sorted(value.items())}


def read_regular(path: Path, maximum: int = 16 * 1024 * 1024) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent == HERE, f"input parent:{absolute.name}")
    require(
        absolute.parent.resolve() == HERE,
        f"input parent resolution:{absolute.name}",
    )
    status = absolute.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and not absolute.is_symlink()
        and status.st_nlink == 1,
        f"input regular singleton:{absolute.name}",
    )
    require(0 < status.st_size <= maximum, f"input size:{absolute.name}")
    descriptor = os.open(
        absolute, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino)
            == (status.st_dev, status.st_ino)
            and stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_size == status.st_size,
            f"input race/type:{absolute.name}",
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            require(bool(chunk), f"short read:{absolute.name}")
            chunks.append(chunk)
            remaining -= len(chunk)
        require(not os.read(descriptor, 1), f"growing input:{absolute.name}")
    finally:
        os.close(descriptor)
    raw = b"".join(chunks)
    require(len(raw) == status.st_size, f"byte count:{absolute.name}")
    return raw


def check_manifest() -> dict[str, str]:
    raw = read_regular(HERE / ROUND215_MANIFEST, 16 * 1024)
    require(
        hashlib.sha256(raw).hexdigest() == ROUND215_MANIFEST_SHA256,
        "Round215 manifest pin",
    )
    entries: dict[str, str] = {}
    for line in raw.decode("ascii", "strict").splitlines():
        value, filename = line.split("  ", 1)
        require(
            len(value) == 64
            and filename not in entries
            and "/" not in filename,
            f"Round215 manifest line:{filename}",
        )
        entries[filename] = value
    require(len(entries) == 6, "Round215 six-entry manifest")
    for filename, expected in entries.items():
        require(
            hashlib.sha256(read_regular(HERE / filename)).hexdigest()
            == expected,
            f"Round215 manifest entry:{filename}",
        )
    return entries


require(
    hashlib.sha256(read_regular(HERE / ROUND215_PROBE, 256 * 1024))
    .hexdigest()
    == ROUND215_PROBE_SHA256,
    "Round215 probe pre-import pin",
)
if os.fspath(HERE) not in sys.path:
    sys.path.insert(0, os.fspath(HERE))
p215 = importlib.import_module(ROUND215_PROBE[:-3])
require(
    Path(p215.__file__).resolve() == (HERE / ROUND215_PROBE).resolve(),
    "Round215 probe module identity",
)
require(
    hashlib.sha256(read_regular(HERE / ROUND215_PROBE, 256 * 1024))
    .hexdigest()
    == ROUND215_PROBE_SHA256,
    "Round215 probe post-import pin",
)
r201 = p215.r201
r180 = p215.r180
r176 = p215.r176


class StreamDigest:
    def __init__(self) -> None:
        self._state = hashlib.sha256()
        self._state.update(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self._state.update(b",")
        self._state.update(canonical(value).encode())
        self.count += 1

    def finish(self) -> str:
        self._state.update(b"]")
        return self._state.hexdigest()


def frozen_state() -> dict[str, Any]:
    entries = check_manifest()
    certificate = p215.strict_json(
        HERE / f"{ROUND215_PREFIX}_certificate.json"
    )
    verification = p215.strict_json(
        HERE / f"{ROUND215_PREFIX}_verification.json"
    )
    require(
        certificate["result_sha256"]
        == ROUND215_CERTIFICATE_RESULT_SHA256
        and verification["result_sha256"]
        == ROUND215_VERIFICATION_RESULT_SHA256
        and verification["result"]["status"]
        == "PASS_PARTIAL_FORMAL_ROUND215"
        and verification["result"]["verdict"] == "PASS"
        and verification["result"]["verified_ledger"][
            "combined_whole_record_excluded"
        ]
        == 74_584
        and verification["result"]["verified_ledger"][
            "combined_conservative_live"
        ]
        == 2_248
        and verification["result"]["verified_ledger"][
            "remaining_priority_origins"
        ]
        == 252,
        "Round215 verified state",
    )
    upstream = r201.check_upstream()
    return {
        "Round215_manifest_sha256": ROUND215_MANIFEST_SHA256,
        "Round215_manifest_entries_replayed": len(entries),
        "Round215_probe_sha256": ROUND215_PROBE_SHA256,
        "Round215_certificate_result_sha256":
            ROUND215_CERTIFICATE_RESULT_SHA256,
        "Round215_verification_result_sha256":
            ROUND215_VERIFICATION_RESULT_SHA256,
        "Round215_verified_ledger": {
            "excluded": 74_584,
            "conservative_live": 2_248,
            "total": 76_832,
            "remaining": 252,
            "remaining_partition": {
                "incomplete_mixed": 198,
                "compact_q": 54,
            },
        },
        "upstream": upstream,
    }


def q_face_evidence(row: Any) -> dict[str, Any]:
    require(
        row.box.p1 == 1 or row.box.p0 == -1,
        f"compact endpoint sign:{row.key}",
    )
    p_sign = 1 if row.box.p1 == 1 else -1
    face = r176.QBox(
        row.box.t0,
        row.box.t1,
        Q(0),
        Q(0),
        row.box.s0,
        row.box.s1,
        0,
    )
    geometry = r176.q_geometry(row.chart_id, p_sign, face)
    records = [
        r176.root_from_geometry(geometry, target)
        for target in row.active_targets
    ]
    classification, selected = r176.q_classify(
        row.chart_id, p_sign, face, row.active_targets
    )
    record_rows = []
    for record in sorted(records, key=lambda item: item.target_id):
        record_rows.append({
            "target": record.target_id,
            "classification": record.classification,
            "ell_sign": p215.sign_name(record.ell),
            "Delta_sign": p215.sign_name(record.discriminant),
            "near_sign": (
                None if record.near is None
                else p215.sign_name(record.near)
            ),
            "far_sign": (
                None if record.far is None
                else p215.sign_name(record.far)
            ),
        })
    result = {
        "origin_key": row.origin_key,
        "root_key": row.key,
        "source_chart_id": row.chart_id,
        "p_sign": p_sign,
        "face_box": {
            "t": [str(row.box.t0), str(row.box.t1)],
            "r": ["0", "0"],
            "s": [str(row.box.s0), str(row.box.s1)],
        },
        "ambient_dimension": 2,
        "classification": classification,
        "selected_or_active_targets": list(selected),
        "root_records": record_rows,
        "closed_face_exactly_classified":
            not classification.startswith("UNRESOLVED"),
        "excluded_face":
            classification.startswith("EXCLUDED"),
        "whole_origin_integer_credit": 0,
    }
    result["row_sha256"] = digest(result)
    return result


def source_face_owner_audit(
    rows: list[Any],
    evidence_by_key: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    groups: dict[tuple[str, str, int], list[Any]] = defaultdict(list)
    for row in rows:
        p_sign = evidence_by_key[row.key]["p_sign"]
        groups[(row.origin_key, row.chart_id, p_sign)].append(row)

    face_incidence: dict[str, set[str]] = defaultdict(set)
    face_geometry: dict[str, dict[str, Any]] = {}
    face_classifications: dict[str, set[str]] = defaultdict(set)
    edge_incidence: dict[str, set[str]] = defaultdict(set)
    edge_geometry: dict[str, dict[str, Any]] = {}
    corner_incidence: dict[str, set[str]] = defaultdict(set)
    corner_geometry: dict[str, dict[str, Any]] = {}

    for group, group_rows in sorted(groups.items()):
        origin, chart, p_sign = group
        t_cuts = sorted({
            value
            for row in group_rows
            for value in (row.box.t0, row.box.t1)
        })
        s_cuts = sorted({
            value
            for row in group_rows
            for value in (row.box.s0, row.box.s1)
        })
        for row in sorted(group_rows, key=lambda item: item.key):
            face = {
                "origin_key": origin,
                "source_chart_id": chart,
                "p_sign": p_sign,
                "t": [str(row.box.t0), str(row.box.t1)],
                "s": [str(row.box.s0), str(row.box.s1)],
            }
            face_id = canonical(face)
            face_geometry[face_id] = face
            face_incidence[face_id].add(row.key)
            face_classifications[face_id].add(
                evidence_by_key[row.key]["classification"]
            )

            local_t = [
                value for value in t_cuts
                if row.box.t0 <= value <= row.box.t1
            ]
            local_s = [
                value for value in s_cuts
                if row.box.s0 <= value <= row.box.s1
            ]
            for fixed_s in (row.box.s0, row.box.s1):
                for lower, upper in zip(local_t, local_t[1:]):
                    edge = {
                        "origin_key": origin,
                        "source_chart_id": chart,
                        "p_sign": p_sign,
                        "axis": "t",
                        "interval": [str(lower), str(upper)],
                        "fixed_s": str(fixed_s),
                    }
                    edge_id = canonical(edge)
                    edge_geometry[edge_id] = edge
                    edge_incidence[edge_id].add(face_id)
                    for t_value in (lower, upper):
                        corner = {
                            "origin_key": origin,
                            "source_chart_id": chart,
                            "p_sign": p_sign,
                            "t": str(t_value),
                            "s": str(fixed_s),
                        }
                        corner_id = canonical(corner)
                        corner_geometry[corner_id] = corner
                        corner_incidence[corner_id].add(face_id)
            for fixed_t in (row.box.t0, row.box.t1):
                for lower, upper in zip(local_s, local_s[1:]):
                    edge = {
                        "origin_key": origin,
                        "source_chart_id": chart,
                        "p_sign": p_sign,
                        "axis": "s",
                        "interval": [str(lower), str(upper)],
                        "fixed_t": str(fixed_t),
                    }
                    edge_id = canonical(edge)
                    edge_geometry[edge_id] = edge
                    edge_incidence[edge_id].add(face_id)
                    for s_value in (lower, upper):
                        corner = {
                            "origin_key": origin,
                            "source_chart_id": chart,
                            "p_sign": p_sign,
                            "t": str(fixed_t),
                            "s": str(s_value),
                        }
                        corner_id = canonical(corner)
                        corner_geometry[corner_id] = corner
                        corner_incidence[corner_id].add(face_id)

    def disposition(face_ids: set[str]) -> str:
        classifications = {
            classification
            for face_id in face_ids
            for classification in face_classifications[face_id]
        }
        if classifications and all(
            value.startswith("EXCLUDED") for value in classifications
        ):
            return "EXCLUDED"
        if any(value.startswith("LIVE") for value in classifications):
            return "NONEXCLUDED_LIVE"
        return "NONEXCLUDED_UNRESOLVED_OR_CONFLICT"

    face_rows = []
    for face_id in sorted(face_geometry):
        owners = sorted(face_incidence[face_id])
        classes = sorted(face_classifications[face_id])
        face_rows.append({
            "geometry": face_geometry[face_id],
            "owner": owners[0],
            "coincident_root_keys": owners,
            "classifications": classes,
            "disposition": disposition({face_id}),
        })
    edge_rows = []
    for edge_id in sorted(edge_geometry):
        incidents = edge_incidence[edge_id]
        owners = sorted(
            min(face_incidence[face_id]) for face_id in incidents
        )
        edge_rows.append({
            "geometry": edge_geometry[edge_id],
            "owner": owners[0],
            "incident_2D_face_count": len(incidents),
            "boundary_class":
                "OUTER_OR_CUT_BOUNDARY" if len(incidents) == 1
                else "INTERNAL_SHARED",
            "disposition": disposition(incidents),
        })
    corner_rows = []
    for corner_id in sorted(corner_geometry):
        incidents = corner_incidence[corner_id]
        owners = sorted(
            min(face_incidence[face_id]) for face_id in incidents
        )
        corner_rows.append({
            "geometry": corner_geometry[corner_id],
            "owner": owners[0],
            "incident_2D_face_count": len(incidents),
            "disposition": disposition(incidents),
        })

    face_dispositions = Counter(
        row["disposition"] for row in face_rows
    )
    edge_dispositions = Counter(
        row["disposition"] for row in edge_rows
    )
    corner_dispositions = Counter(
        row["disposition"] for row in corner_rows
    )
    return {
        "half_open_rule":
            "coincident 2D patch, atomic 1D edge, and 0D corner are "
            "owned by the lexicographically least incident root key",
        "atomic_edge_refinement_uses_all_exact_group_endpoints": True,
        "2D_input_root_face_count": len(rows),
        "2D_unique_physical_patch_count": len(face_rows),
        "2D_duplicate_representation_count":
            len(rows) - len(face_rows),
        "2D_owner_rows_sha256": digest(face_rows),
        "2D_disposition_count": map_counter(face_dispositions),
        "1D_atomic_edge_count": len(edge_rows),
        "1D_owner_rows_sha256": digest(edge_rows),
        "1D_disposition_count": map_counter(edge_dispositions),
        "0D_atomic_corner_count": len(corner_rows),
        "0D_owner_rows_sha256": digest(corner_rows),
        "0D_disposition_count": map_counter(corner_dispositions),
        "all_2D_1D_0D_integer_credit": 0,
    }


def split_axis(parent: Any, lower: Any) -> tuple[str, Q]:
    if lower.t1 != parent.t1:
        return "t", lower.t1
    if lower.r1 != parent.r1:
        return "r", lower.r1
    require(lower.s1 != parent.s1, "q split axis")
    return "s", lower.s1


def q_depth10_profile(
    rows: list[Any],
    face_by_key: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    face_counts: Counter[str] = Counter()
    terminal_counts: Counter[str] = Counter()
    terminal_depths: Counter[int] = Counter()
    terminal_volume: dict[str, Q] = defaultdict(Q)
    residual_counts: Counter[str] = Counter()
    residual_volume = Q(0)
    closed_roots: list[str] = []
    obstruction_rows: list[dict[str, Any]] = []
    per_origin: dict[str, dict[str, Any]] = {}
    origin_terminal: dict[str, Counter[str]] = defaultdict(Counter)
    origin_residual: dict[str, Counter[str]] = defaultdict(Counter)
    origin_excluded_volume: defaultdict[str, Q] = defaultdict(Q)
    split_rows = StreamDigest()
    leaf_rows = StreamDigest()

    for index, row in enumerate(sorted(rows, key=lambda item: item.key), 1):
        p_sign = face_by_key[row.key]["p_sign"]
        face_counts[face_by_key[row.key]["classification"]] += 1
        root = r176.QBox(
            row.box.t0,
            row.box.t1,
            Q(0),
            Q(1),
            row.box.s0,
            row.box.s1,
            0,
        )
        pending = [(root, row.active_targets, "")]
        root_residual = False
        root_kinds: set[str] = set()
        root_obstructions: list[dict[str, Any]] = []
        while pending:
            box, targets, path = pending.pop()
            classification, active = r176.q_classify(
                row.chart_id, p_sign, box, targets
            )
            if not classification.startswith("UNRESOLVED"):
                terminal_counts[classification] += 1
                terminal_depths[box.depth] += 1
                terminal_volume[classification] += Q(
                    1, 2 ** box.depth
                )
                origin_terminal[row.origin_key][classification] += 1
                kind = (
                    "EXCLUDED"
                    if classification.startswith("EXCLUDED")
                    else "LIVE"
                )
                root_kinds.add(kind)
                if kind == "EXCLUDED":
                    origin_excluded_volume[row.origin_key] += Q(
                        1, 2 ** box.depth
                    )
                else:
                    root_obstructions.append({
                        "origin_key": row.origin_key,
                        "root_key": row.key,
                        "q_path": path,
                        "extra_depth": box.depth,
                        "classification": classification,
                        "active_targets": list(active),
                        "ambient_dimension": 3,
                    })
                leaf_rows.add({
                    "origin_key": row.origin_key,
                    "root_key": row.key,
                    "q_path": path,
                    "extra_depth": box.depth,
                    "classification": classification,
                    "box": {
                        "t": [str(box.t0), str(box.t1)],
                        "r": [str(box.r0), str(box.r1)],
                        "s": [str(box.s0), str(box.s1)],
                    },
                })
            elif box.depth < MAX_Q_DEPTH:
                lower, upper = r176.q_split(box)
                axis, coordinate = split_axis(box, lower)
                split_rows.add({
                    "origin_key": row.origin_key,
                    "root_key": row.key,
                    "q_path": path,
                    "split_axis": axis,
                    "split_coordinate": str(coordinate),
                    "half_open_owner": path + "0",
                    "other_child": path + "1",
                    "2D_split_face_owned_once": True,
                    "1D_edge_incidence_count": 4,
                    "0D_corner_incidence_count": 4,
                })
                inherited = active or targets
                pending.extend([
                    (lower, inherited, path + "0"),
                    (upper, inherited, path + "1"),
                ])
            else:
                root_residual = True
                residual_counts[classification] += 1
                residual_volume += Q(1, 2 ** box.depth)
                origin_residual[row.origin_key][classification] += 1
                obstruction = {
                    "origin_key": row.origin_key,
                    "root_key": row.key,
                    "q_path": path,
                    "extra_depth": box.depth,
                    "classification": classification,
                    "active_targets": list(active),
                    "ambient_dimension": 3,
                }
                root_obstructions.append(obstruction)
                leaf_rows.add({
                    **obstruction,
                    "box": {
                        "t": [str(box.t0), str(box.t1)],
                        "r": [str(box.r0), str(box.r1)],
                        "s": [str(box.s0), str(box.s1)],
                    },
                })
        if (
            not root_residual
            and root_kinds
            and root_kinds == {"EXCLUDED"}
        ):
            closed_roots.append(row.key)
        else:
            require(root_obstructions, f"q root obstruction:{row.key}")
            obstruction_rows.append(
                min(
                    root_obstructions,
                    key=lambda item: (
                        item["root_key"],
                        item["q_path"],
                        item["classification"],
                    ),
                )
            )
        if index % 100 == 0 or index == len(rows):
            progress(f"Round218 q depth10 roots {index}/{len(rows)}")

    for origin in sorted({
        row.origin_key for row in rows
    }):
        witnesses = [
            row for row in obstruction_rows
            if row["origin_key"] == origin
        ]
        require(witnesses, f"compact origin q obstruction:{origin}")
        face_witnesses = sorted(
            (
                face_by_key[row.key]
                for row in rows
                if (
                    row.origin_key == origin
                    and not face_by_key[row.key][
                        "classification"
                    ].startswith("EXCLUDED")
                )
            ),
            key=lambda item: item["root_key"],
        )
        per_origin[origin] = {
            "q_root_count": sum(
                row.origin_key == origin for row in rows
            ),
            "terminal_count_by_disposition":
                map_counter(origin_terminal[origin]),
            "residual_count_by_type":
                map_counter(origin_residual[origin]),
            "excluded_q_root_equivalent_volume":
                str(origin_excluded_volume[origin]),
            "minimal_3D_obstruction": min(
                witnesses,
                key=lambda item: (
                    item["root_key"],
                    item["q_path"],
                    item["classification"],
                ),
            ),
            "minimal_nonexcluded_q0_face": (
                None if not face_witnesses
                else {
                    key: face_witnesses[0][key]
                    for key in (
                        "root_key",
                        "classification",
                        "selected_or_active_targets",
                        "row_sha256",
                    )
                }
            ),
            "whole_origin_credit": 0,
        }
        per_origin[origin]["row_sha256"] = digest(per_origin[origin])

    obstruction_rows.sort(
        key=lambda item: (
            item["origin_key"],
            item["root_key"],
            item["q_path"],
        )
    )
    per_origin_rows = [
        {"origin_key": key, **per_origin[key]}
        for key in sorted(per_origin)
    ]
    origins_with_nonexcluded_q0_face = [
        row["origin_key"] for row in per_origin_rows
        if row["minimal_nonexcluded_q0_face"] is not None
    ]
    origins_with_all_q0_faces_excluded = [
        row["origin_key"] for row in per_origin_rows
        if row["minimal_nonexcluded_q0_face"] is None
    ]
    require(
        not closed_roots
        and len(per_origin_rows) == EXPECTED_COMPACT_ORIGINS
        and (
            len(origins_with_nonexcluded_q0_face)
            + len(origins_with_all_q0_faces_excluded)
        )
        == EXPECTED_COMPACT_ORIGINS,
        "all compact origins retain q obstruction",
    )
    return {
        "input_initial_source_grazing_root_count": len(rows),
        "max_extra_q_depth": MAX_Q_DEPTH,
        "coordinate": {
            "r_interval": "[0,1]",
            "q": "sqrt(1023/262144)*r",
            "p": "sign*sqrt(1-(1023/262144)*r^2)",
        },
        "3D_open_source_stratum": {
            "predicate": "r>0",
            "dimension": 3,
        },
        "2D_grazing_face_stratum": {
            "predicate": "r=0",
            "dimension": 2,
            "classification_count": map_counter(face_counts),
        },
        "terminal_count_by_disposition": map_counter(terminal_counts),
        "terminal_count_by_extra_depth": map_counter(terminal_depths),
        "terminal_volume_by_disposition":
            fraction_map(terminal_volume),
        "residual_count_by_type": map_counter(residual_counts),
        "residual_q_cell_count": sum(residual_counts.values()),
        "residual_initial_root_equivalent_volume":
            str(residual_volume),
        "closed_initial_q_root_count": len(closed_roots),
        "closed_initial_q_root_keys_sha256": digest(closed_roots),
        "split_2D_face_owner_row_count": split_rows.count,
        "split_2D_face_owner_rows_sha256": split_rows.finish(),
        "split_face_1D_edge_incidence_count": split_rows.count * 4,
        "split_face_0D_corner_incidence_count": split_rows.count * 4,
        "3D_terminal_or_residual_leaf_count": leaf_rows.count,
        "3D_terminal_or_residual_leaf_rows_sha256":
            leaf_rows.finish(),
        "one_minimal_3D_obstruction_per_q_root_count":
            len(obstruction_rows),
        "minimal_3D_obstruction_rows_sha256":
            digest(obstruction_rows),
        "per_origin_obstruction_row_count": len(per_origin_rows),
        "per_origin_obstruction_rows_sha256":
            digest(per_origin_rows),
        "per_origin_obstruction_rows": per_origin_rows,
        "origin_with_nonexcluded_q0_face_count":
            len(origins_with_nonexcluded_q0_face),
        "origin_with_nonexcluded_q0_face_keys_sha256":
            digest(origins_with_nonexcluded_q0_face),
        "origin_with_all_q0_faces_excluded_count":
            len(origins_with_all_q0_faces_excluded),
        "origin_with_all_q0_faces_excluded_keys_sha256":
            digest(origins_with_all_q0_faces_excluded),
        "all_54_origins_retain_3D_q_tree_obstruction": True,
        "q_tree_internal_2D_faces_have_unique_half_open_owner": True,
        "q_tree_split_face_edges_and_corners_are_incidence_ledger_only":
            True,
        "complete_cross_root_3D_2D_1D_0D_owner_partition_claimed":
            False,
        "whole_origin_integer_credit": 0,
    }


def rebuild() -> dict[str, Any]:
    frozen = frozen_state()
    upstream = frozen.pop("upstream")
    registry_rows = upstream["certificate"]["result"][
        "priority_registry"
    ]["rows"]
    registry = sorted(
        (
            row for row in registry_rows
            if row["priority_class"] == COMPACT_CLASS
        ),
        key=lambda row: row["priority_ordinal"],
    )
    compact_keys = sorted(row["origin_key"] for row in registry)
    require(
        len(registry) == EXPECTED_COMPACT_ORIGINS
        and digest(compact_keys) == EXPECTED_COMPACT_KEYS_SHA256
        and all(
            row["selection_uses_new_closure_outcome"] is False
            for row in registry
        ),
        "outcome-blind compact54 selection",
    )

    compact_set = set(compact_keys)
    progress("Round218 replay frozen Round176 frontier")
    replay = r176.replay_frontier()
    residual_roots: dict[str, list[Any]] = defaultdict(list)
    preclosed = Counter()
    preclosed_kinds: dict[str, set[str]] = defaultdict(set)
    preclosed_kinds.update({
        origin: set(kinds)
        for origin, kinds in replay["origin_kinds"].items()
        if origin in compact_set
    })
    for row in replay["frontier"]:
        if row.origin_key not in compact_set:
            continue
        kind, _evidence = r176.closure(row)
        if kind is None:
            residual_roots[row.origin_key].append(row)
        else:
            preclosed[row.origin_key] += 1
            preclosed_kinds[row.origin_key].add(kind)
    for rows in residual_roots.values():
        rows.sort(key=lambda row: row.key)
    require(
        set(residual_roots) == compact_set,
        "all compact origins have residual roots",
    )

    initial_categories = Counter()
    source_grazing_rows: list[Any] = []
    for rows in residual_roots.values():
        for row in rows:
            category = r180.initial_category(row)
            initial_categories[category] += 1
            if category == Q_CATEGORY:
                source_grazing_rows.append(row)
    source_grazing_rows.sort(key=lambda row: row.key)
    require(
        sum(preclosed.values()) == EXPECTED_PRECLOSED_FRONTIER
        and sum(len(rows) for rows in residual_roots.values())
        == EXPECTED_INITIAL_RESIDUAL_ROOTS
        and map_counter(initial_categories)
        == EXPECTED_INITIAL_CATEGORY_COUNT
        and len(source_grazing_rows)
        == EXPECTED_INITIAL_CATEGORY_COUNT[Q_CATEGORY],
        "compact initial frontier census",
    )

    final_categories = Counter()
    final_children = 0
    geometric_closed = 0
    geometric_residual = 0
    deleted_candidates = 0
    failed_candidates = 0
    compact_residual_by_origin: Counter[str] = Counter()
    for index, row_registry in enumerate(registry, 1):
        origin = row_registry["origin_key"]
        require(
            len(residual_roots[origin])
            == row_registry["Round176_residual_root_count"]
            and preclosed[origin]
            == row_registry["Round176_preclosed_frontier_count"]
            and sorted(preclosed_kinds[origin])
            == row_registry["Round176_preclosed_kinds"],
            f"Round176 compact registry replay:{origin}",
        )
        refinement = r180.refine_origin(residual_roots[origin], 4)
        final_rows = sorted(
            refinement["final_residual_rows"],
            key=lambda row: row.key,
        )
        categories = Counter(
            r180.residual_category(row) for row in final_rows
        )
        require(
            len(final_rows)
            == row_registry["Round180_residual_child_count"]
            and digest([row.key for row in final_rows])
            == row_registry["Round180_residual_child_keys_sha256"]
            and map_counter(categories)
            == row_registry["Round180_residual_category_count"],
            f"Round180 compact registry replay:{origin}",
        )
        final_categories.update(categories)
        for row in final_rows:
            reduction = p215.exact_behind_reduce(
                row, r180.residual_category(row)
            )
            final_children += 1
            deleted_candidates += len(reduction["eligible_targets"])
            if reduction["closed"]:
                geometric_closed += 1
            else:
                geometric_residual += 1
                compact_residual_by_origin[origin] += 1
            failed_candidates += sum(
                (
                    not evidence["eligible_exact_behind"]
                    and not evidence["ell_strict_negative"]
                )
                for evidence in reduction["candidate_evidence"]
            )
        if index % 10 == 0 or index == len(registry):
            progress(
                f"Round218 compact outer origins {index}/{len(registry)}"
            )

    require(
        map_counter(final_categories) == EXPECTED_FINAL_CATEGORY_COUNT
        and final_children == EXPECTED_FINAL_CHILDREN
        and geometric_closed == EXPECTED_GEOMETRIC_CLOSED
        and geometric_residual == EXPECTED_GEOMETRIC_RESIDUAL
        and deleted_candidates == EXPECTED_DELETED_CANDIDATES
        and failed_candidates == EXPECTED_FAILED_CANDIDATES
        and geometric_closed + geometric_residual == final_children,
        "compact outer exact conservation",
    )

    progress("Round218 classify exact q=0 source faces")
    face_rows = [
        q_face_evidence(row) for row in source_grazing_rows
    ]
    face_by_key = {
        row["root_key"]: row for row in face_rows
    }
    face_classes = Counter(
        row["classification"] for row in face_rows
    )
    owner_audit = source_face_owner_audit(
        source_grazing_rows, face_by_key
    )
    q_profile = q_depth10_profile(
        source_grazing_rows, face_by_key
    )

    compact_origins_with_residual = sorted(compact_residual_by_origin)
    require(
        set(compact_origins_with_residual) <= compact_set
        and sum(compact_residual_by_origin.values())
        == EXPECTED_GEOMETRIC_RESIDUAL,
        "compact geometric residual origin support",
    )
    compact_origins_without_outer_residual = sorted(
        compact_set - set(compact_origins_with_residual)
    )
    result = {
        "status":
            "BOUNDED_COMPACT_Q_SOURCE_STRATUM_FRONTIER__"
            "NO_WHOLE_ORIGIN_PROMOTION",
        "verdict": "PASS_BOUNDED_NONPROMOTIONAL_PROBE",
        "frozen_state": frozen,
        "selection": {
            "priority_class": COMPACT_CLASS,
            "selection_is_outcome_blind": True,
            "origin_count": len(registry),
            "origin_keys_sha256": digest(compact_keys),
            "seam2_and_mixed198_strictly_separate": True,
        },
        "independent_outer_reconstruction": {
            "Round176_preclosed_frontier_count":
                sum(preclosed.values()),
            "Round176_initial_residual_root_count":
                sum(len(rows) for rows in residual_roots.values()),
            "initial_category_count":
                map_counter(initial_categories),
            "Round180_final_child_count": final_children,
            "final_category_count": map_counter(final_categories),
            "geometric_closed_cell_count": geometric_closed,
            "geometric_residual_cell_count": geometric_residual,
            "deleted_candidate_count": deleted_candidates,
            "failed_candidate_count": failed_candidates,
            "origin_with_geometric_residual_count":
                len(compact_origins_with_residual),
            "origin_with_geometric_residual_keys_sha256":
                digest(compact_origins_with_residual),
            "origin_without_outer_3D_residual_count":
                len(compact_origins_without_outer_residual),
            "origin_without_outer_3D_residual_keys":
                compact_origins_without_outer_residual,
            "origin_without_outer_3D_residual_keys_sha256":
                digest(compact_origins_without_outer_residual),
            "all_54_origins_retain_q_stratum_obstruction": True,
            "compact_residual_count_by_origin_sha256":
                digest([
                    {
                        "origin_key": key,
                        "residual_count":
                            compact_residual_by_origin[key],
                    }
                    for key in compact_keys
                ]),
        },
        "source_grazing_face_analysis": {
            "input_root_count": len(face_rows),
            "classification_count": map_counter(face_classes),
            "face_evidence_rows_sha256": digest(face_rows),
            "closed_face_classification_uses_exact_interval_root_order":
                True,
            "face_rows": face_rows,
        },
        "source_grazing_half_open_owner_audit": owner_audit,
        "bounded_q_depth10_frontier": q_profile,
        "outer_conservation_650_equals_596_plus_54": {
            "frozen_Round215_mixed_origin_count": 596,
            "independently_rebuilt_compact_q_origin_count": 54,
            "total_origin_count": 650,
            "exact_origin_partition": True,
        },
        "dimension_safe_nonpromotion": {
            "compact_q_child_or_volume_credit": 0,
            "source_grazing_2D_face_credit": 0,
            "source_grazing_1D_edge_credit": 0,
            "source_grazing_0D_corner_credit": 0,
            "whole_origin_credit": 0,
            "ledger_unchanged": True,
            "combined_whole_record_excluded": 74_584,
            "combined_conservative_live": 2_248,
            "remaining_priority_origins": 252,
            "remaining_priority_partition": {
                "incomplete_mixed": 198,
                "compact_q": 54,
            },
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate":
            "resolve the exact per-origin q-tree 3D obstruction and "
            "complete cross-root 3D/2D/1D/0D owner gluing before any "
            "whole-origin credit",
    }
    return result


def main() -> int:
    ctx.prec = 192
    result = rebuild()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    print(canonical(document))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
