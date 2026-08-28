#!/usr/bin/env python3
"""Exact whole-origin analytic probe for one frozen compact-q origin.

This additive, read-only probe addresses the first Round306 compact-q core
gate without extending the bounded subdivision tree.  It selects the fixed
Round184 ``COMPACT_Q_PRESENT`` origin ``W:N:03.15.01111111``, binds the 16
source-grazing root boxes recorded by the pinned Round218 probe, and proves a
uniform geometric statement on their entire compact-q domain.

For every point in the domain, the frozen desired target ``W[1,0]`` has
strictly negative forward projection, while ``W[-1,0]`` has a strict future
line-circle root before time one.  Hence a first collision exists and cannot
have the frozen owner.  The proof is insensitive to ordering/tie surfaces
between non-frozen targets.  A complete atomic product decomposition assigns
all cross-root 3D, 2D, 1D, and 0D strata to the lexicographically least
incident root.

This is deliberately a representative-origin theorem only.  It changes no
ledger, grants no formal credit, writes no file, and emits one canonical JSON
object to stdout.
"""

from __future__ import annotations

from collections import Counter
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

HERE = Path(__file__).resolve().parent
SCHEMA = (
    "cm2.round306c30q0.compact-q-representative-origin-analytic-probe.v1"
)
ORIGIN = "W:N:03.15.01111111"
SOURCE_CHART = "W:N"
FROZEN_TARGET = "W[1,0]"
CERTIFIED_FUTURE_TARGET = "W[-1,0]"
OTHER_RECORDED_TARGET = "G[0,1]"

ROUND184_MANIFEST = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
    "manifest.sha256"
)
ROUND184_MANIFEST_SHA256 = (
    "3c2a50663dc47479f67435109b737362895e53a2c1b4c29991fe875c5ac68cd1"
)
ROUND184_CERTIFICATE = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
    "certificate.json"
)
ROUND184_CERTIFICATE_SHA256 = (
    "292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f"
)
ROUND184_CERTIFICATE_RESULT_SHA256 = (
    "70026cc9e52cfe0adee0be2ff8daf0f4519a2f1947338e902399461039b82dbe"
)
ROUND184_ROW_SHA256 = (
    "08b40a2c8f716b462649f97fa776f33a3d33eeca7152a6a87e57ceb2e42dfc25"
)

ROUND218_MANIFEST = (
    "cm2_round218_source_w_compact_q_source_stratum_frontier_"
    "probe_manifest.sha256"
)
ROUND218_MANIFEST_SHA256 = (
    "5cde966f9fbdca1ab60e414fd649b8649f1babee92f0b27136be207f0bb92602"
)
ROUND218_RESULT = (
    "cm2_round218_source_w_compact_q_source_stratum_frontier_result.json"
)
ROUND218_RESULT_SHA256 = (
    "dc4d86f68393736c314005aff27ea2febb8072e3224c892090d8a7cf54844887"
)
ROUND218_INNER_RESULT_SHA256 = (
    "f440ee0ac043067a48b8ed8e217a827ed8c0e5072778e84931090df8cd4f7000"
)
ROUND218_PROBE = (
    "cm2_round218_source_w_compact_q_source_stratum_frontier.py"
)
ROUND218_PROBE_SHA256 = (
    "1dadb46be62853391898314b4a9fbbf5aae2750e70a21e3d891e975f45a3cfbf"
)

T_CUTS = tuple(Q(value) for value in (
    "-1593/16000",
    "-12567/128000",
    "-1239/12800",
    "-12213/128000",
    "-3009/32000",
    "-11859/128000",
    "-5841/64000",
    "-2301/25600",
    "-177/2000",
))
R_CUTS = (Q(0), Q(1))
S_CUTS = (Q(-1, 400), Q(0), Q(1, 400))

SOURCE_RADIUS = Q(4, 25)
TARGET_RADIUS = Q(4, 25)
K = Q(1023, 262144)
Q_STRICT_UPPER = Q(1, 16)
T_ABS_STRICT_UPPER = Q(1, 8)


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


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant:{value}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def read_regular(path: Path, maximum: int = 32 * 1024 * 1024) -> bytes:
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
        absolute,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
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


def strict_json(path: Path) -> dict[str, Any]:
    raw = read_regular(path)
    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), f"JSON object:{path.name}")
    return value


def verify_manifest(name: str, expected_sha256: str) -> dict[str, str]:
    raw = read_regular(HERE / name, 64 * 1024)
    require(
        hashlib.sha256(raw).hexdigest() == expected_sha256,
        f"manifest pin:{name}",
    )
    entries: dict[str, str] = {}
    for line in raw.decode("ascii", "strict").splitlines():
        value, filename = line.split("  ", 1)
        require(
            len(value) == 64
            and all(character in "0123456789abcdef" for character in value)
            and filename not in entries
            and "/" not in filename
            and filename not in {".", ".."},
            f"manifest line:{name}:{filename}",
        )
        entries[filename] = value
    require(entries, f"nonempty manifest:{name}")
    for filename, expected in entries.items():
        actual = hashlib.sha256(read_regular(HERE / filename)).hexdigest()
        require(actual == expected, f"manifest member:{name}:{filename}")
    return entries


def fraction(value: str) -> Q:
    parsed = Q(value)
    require(str(parsed) == value, f"canonical rational:{value}")
    return parsed


def frozen_inputs() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    round184_entries = verify_manifest(
        ROUND184_MANIFEST,
        ROUND184_MANIFEST_SHA256,
    )
    round218_entries = verify_manifest(
        ROUND218_MANIFEST,
        ROUND218_MANIFEST_SHA256,
    )
    require(
        round184_entries[ROUND184_CERTIFICATE]
        == ROUND184_CERTIFICATE_SHA256,
        "Round184 certificate manifest pin",
    )
    require(
        round218_entries[ROUND218_RESULT] == ROUND218_RESULT_SHA256,
        "Round218 result manifest pin",
    )

    round184 = strict_json(HERE / ROUND184_CERTIFICATE)
    require(
        round184.get("result_sha256")
        == ROUND184_CERTIFICATE_RESULT_SHA256
        and digest(round184.get("result"))
        == ROUND184_CERTIFICATE_RESULT_SHA256,
        "Round184 inner result pin",
    )
    registry_rows = round184["result"]["priority_registry"]["rows"]
    selected = [row for row in registry_rows if row["origin_key"] == ORIGIN]
    require(len(selected) == 1, "unique Round184 representative origin")
    registry = selected[0]
    require(
        registry == {
            "Round176_preclosed_frontier_count": 2,
            "Round176_preclosed_kinds": ["EXCLUDED"],
            "Round176_residual_root_count": 44,
            "Round180_residual_category_count": {
                "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH": 15,
                "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY": 96,
                "MULTI_DISCRIMINANT_2_TO_5_TARGETS": 216,
                "SOURCE_GRAZING_COMPACT_Q_RESIDUAL": 1,
            },
            "Round180_residual_category_support": [
                "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH",
                "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY",
                "MULTI_DISCRIMINANT_2_TO_5_TARGETS",
                "SOURCE_GRAZING_COMPACT_Q_RESIDUAL",
            ],
            "Round180_residual_child_count": 328,
            "Round180_residual_child_keys_sha256": (
                "f655175358ab1b519cceea498f87e470d2f6547d93764b6cf89caf2575b46c3f"
            ),
            "Round180_residual_child_volume": "7257/52428800000",
            "initial_residual_category_count": {
                "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH": 4,
                "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY": 4,
                "MULTI_DISCRIMINANT_2_TO_5_TARGETS": 20,
                "SOURCE_GRAZING_COMPACT_Q_RESIDUAL": 16,
            },
            "origin_key": ORIGIN,
            "priority_class": "COMPACT_Q_PRESENT",
            "priority_class_rank": 3,
            "priority_key": [3, 328, ORIGIN],
            "priority_ordinal": 1406,
            "row_sha256": ROUND184_ROW_SHA256,
            "selection_uses_new_closure_outcome": False,
        },
        "exact Round184 representative registry row",
    )

    round218 = strict_json(HERE / ROUND218_RESULT)
    require(
        hashlib.sha256(read_regular(HERE / ROUND218_RESULT)).hexdigest()
        == ROUND218_RESULT_SHA256
        and round218.get("result_sha256") == ROUND218_INNER_RESULT_SHA256
        and digest(round218.get("result")) == ROUND218_INNER_RESULT_SHA256,
        "Round218 result pins",
    )
    face_rows = [
        row
        for row in round218["result"]["source_grazing_face_analysis"][
            "face_rows"
        ]
        if row["origin_key"] == ORIGIN
    ]
    face_rows.sort(key=lambda row: row["root_key"])
    require(len(face_rows) == 16, "representative 16 q roots")
    return registry, face_rows, {
        "Round184_manifest_sha256": ROUND184_MANIFEST_SHA256,
        "Round184_manifest_member_count": len(round184_entries),
        "Round184_certificate_sha256": ROUND184_CERTIFICATE_SHA256,
        "Round184_certificate_result_sha256":
            ROUND184_CERTIFICATE_RESULT_SHA256,
        "Round218_manifest_sha256": ROUND218_MANIFEST_SHA256,
        "Round218_manifest_member_count": len(round218_entries),
        "Round218_result_file_sha256": ROUND218_RESULT_SHA256,
        "Round218_result_sha256": ROUND218_INNER_RESULT_SHA256,
    }


def root_boxes(face_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    boxes: list[dict[str, Any]] = []
    expected_products = {
        (T_CUTS[index], T_CUTS[index + 1], S_CUTS[side], S_CUTS[side + 1])
        for index in range(len(T_CUTS) - 1)
        for side in range(len(S_CUTS) - 1)
    }
    actual_products: set[tuple[Q, Q, Q, Q]] = set()
    for row in face_rows:
        require(
            row["source_chart_id"] == SOURCE_CHART
            and row["p_sign"] == 1
            and row["face_box"]["r"] == ["0", "0"]
            and row["classification"]
            == "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
            and row["selected_or_active_targets"]
            == [CERTIFIED_FUTURE_TARGET]
            and [record["target"] for record in row["root_records"]]
            == [OTHER_RECORDED_TARGET, CERTIFIED_FUTURE_TARGET]
            and row["whole_origin_integer_credit"] == 0,
            f"Round218 representative face row:{row['root_key']}",
        )
        t0, t1 = (fraction(value) for value in row["face_box"]["t"])
        s0, s1 = (fraction(value) for value in row["face_box"]["s"])
        actual_products.add((t0, t1, s0, s1))
        boxes.append({
            "root_key": row["root_key"],
            "t": [t0, t1],
            "r": [Q(0), Q(1)],
            "s": [s0, s1],
            "Round218_q0_face_row_sha256": row["row_sha256"],
        })
    require(
        actual_products == expected_products
        and len({box["root_key"] for box in boxes}) == 16,
        "exact 8x1x2 representative root-box product partition",
    )
    return sorted(boxes, key=lambda box: box["root_key"])


def axis_atoms(cuts: tuple[Q, ...]) -> list[tuple[str, Q, Q]]:
    require(tuple(sorted(set(cuts))) == cuts, "strictly ordered cuts")
    result: list[tuple[str, Q, Q]] = []
    for index, point in enumerate(cuts):
        result.append(("POINT", point, point))
        if index + 1 < len(cuts):
            result.append(("OPEN_INTERVAL", point, cuts[index + 1]))
    return result


def atom_incident(box: dict[str, Any], atom: dict[str, tuple[str, Q, Q]]) -> bool:
    for axis in ("t", "r", "s"):
        kind, lower, upper = atom[axis]
        box_lower, box_upper = box[axis]
        if kind == "POINT":
            if not box_lower <= lower <= box_upper:
                return False
        elif not box_lower <= lower < upper <= box_upper:
            return False
    return True


def atom_row(
    atom: dict[str, tuple[str, Q, Q]],
    boxes: list[dict[str, Any]],
) -> dict[str, Any]:
    incidents = sorted(
        box["root_key"] for box in boxes if atom_incident(box, atom)
    )
    require(incidents, "atomic stratum has an incident root")
    dimension = sum(atom[axis][0] == "OPEN_INTERVAL" for axis in atom)
    geometry = {
        axis: (
            {"kind": kind, "value": str(lower)}
            if kind == "POINT"
            else {
                "kind": kind,
                "lower": str(lower),
                "upper": str(upper),
            }
        )
        for axis, (kind, lower, upper) in atom.items()
    }
    return {
        "ambient_dimension": dimension,
        "geometry": geometry,
        "owner_root_key": incidents[0],
        "incident_root_count": len(incidents),
        "incident_root_keys": incidents,
        "analytic_disposition": "EXCLUDED_FROZEN_OWNER_STRICTLY_BEHIND",
    }


def half_open_partition(boxes: list[dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for t_atom in axis_atoms(T_CUTS):
        for r_atom in axis_atoms(R_CUTS):
            for s_atom in axis_atoms(S_CUTS):
                rows.append(atom_row(
                    {"t": t_atom, "r": r_atom, "s": s_atom},
                    boxes,
                ))
    rows.sort(key=lambda row: canonical(row["geometry"]))
    by_dimension = Counter(row["ambient_dimension"] for row in rows)
    by_incidence = Counter(row["incident_root_count"] for row in rows)
    owner_count = Counter(row["owner_root_key"] for row in rows)
    require(
        by_dimension == Counter({3: 16, 2: 74, 1: 111, 0: 54})
        and len(rows) == 255
        and all(row["incident_root_count"] == 1 for row in rows if row["ambient_dimension"] == 3)
        and set(owner_count) == {box["root_key"] for box in boxes}
        and all(
            row["owner_root_key"] == min(row["incident_root_keys"])
            for row in rows
        ),
        "complete exact 3D/2D/1D/0D owner partition",
    )
    return {
        "rule": "each relative-open atomic product stratum is owned by the lexicographically least incident Round218 root key",
        "t_cut_count": len(T_CUTS),
        "r_cut_count": len(R_CUTS),
        "s_cut_count": len(S_CUTS),
        "root_box_count": len(boxes),
        "atomic_stratum_count": len(rows),
        "atomic_stratum_count_by_dimension": {
            str(key): by_dimension[key] for key in sorted(by_dimension, reverse=True)
        },
        "incident_root_multiplicity_count": {
            str(key): by_incidence[key] for key in sorted(by_incidence)
        },
        "owner_root_count": len(owner_count),
        "owner_assignment_rows_sha256": digest(rows),
        "owner_assignment_rows": rows,
        "all_strata_owned_exactly_once": True,
        "all_analytic_dispositions_inherit_on_boundaries": True,
    }


def analytic_certificate() -> dict[str, Any]:
    t_min, t_max = T_CUTS[0], T_CUTS[-1]
    require(
        K < Q_STRICT_UPPER * Q_STRICT_UPPER
        and max(abs(t_min), abs(t_max)) < T_ABS_STRICT_UPPER,
        "compact and normal radical coarse bounds",
    )
    p_square_lower = Q(255, 256)
    normal_y_square_lower = Q(63, 64)
    pa_square_lower = p_square_lower * normal_y_square_lower
    require(pa_square_lower > Q(1, 4), "p*a strict half bound")

    t_plus_radius_lower = t_min + SOURCE_RADIUS
    t_plus_radius_upper = t_max + SOURCE_RADIUS
    require(
        t_plus_radius_lower == Q(967, 16000)
        and t_plus_radius_upper == Q(143, 2000)
        and t_plus_radius_lower > 0,
        "left-target t plus radius range",
    )
    left_ell_lower = Q(1, 2) - Q_STRICT_UPPER * t_plus_radius_upper
    left_transverse_upper = Q_STRICT_UPPER + t_plus_radius_upper
    transverse_margin = TARGET_RADIUS - left_transverse_upper
    distance_square_minus_target_radius_square = (
        Q(1) + 2 * SOURCE_RADIUS * t_min
    )
    require(
        left_ell_lower == Q(15857, 32000)
        and left_ell_lower > 0
        and left_transverse_upper == Q(67, 500)
        and transverse_margin == Q(13, 500)
        and distance_square_minus_target_radius_square == Q(48407, 50000)
        and distance_square_minus_target_radius_square > 0,
        "strict future-root rational witnesses",
    )

    return {
        "coordinate_definitions": {
            "normal": "n=(t,a), a=sqrt(1-t^2)>0",
            "compact_velocity": "u=q*n+p*J(n)",
            "q": "sqrt(1023/262144)*r, 0<=r<=1",
            "p": "sqrt(1-q^2)>0",
            "source_point": "(1/2+s,1/2)+(4/25)*n",
        },
        "exact_domain": {
            "t": [str(t_min), str(t_max)],
            "r": ["0", "1"],
            "s": [str(S_CUTS[0]), str(S_CUTS[-1])],
            "p_sign": 1,
            "source_chart": SOURCE_CHART,
        },
        "coarse_radical_witnesses": {
            "q_squared_strict_upper": str(Q(1, 256)),
            "q_squared_exact_maximum": str(K),
            "q_squared_upper_gap": str(Q(1, 256) - K),
            "absolute_t_strict_upper": str(T_ABS_STRICT_UPPER),
            "p_squared_strict_lower": str(p_square_lower),
            "normal_y_squared_strict_lower": str(normal_y_square_lower),
            "p_times_normal_y_squared_strict_lower": str(pa_square_lower),
            "p_times_normal_y_strict_lower": "1/2",
        },
        "frozen_target_strictly_behind": {
            "target": FROZEN_TARGET,
            "center_displacement": "(1,0)-(4/25)*n",
            "forward_projection": "ell_F=q*(t-4/25)-p*a",
            "uniform_strict_upper": "-1/2",
            "proof": "q>=0 and t-4/25<0, while p*a>1/2",
            "future_root_possible": False,
        },
        "certified_nonfrozen_strict_future_root": {
            "target": CERTIFIED_FUTURE_TARGET,
            "center_displacement": "(-1,0)-(4/25)*n",
            "forward_projection": "ell_L=p*a-q*(t+4/25)",
            "forward_projection_strict_lower": str(left_ell_lower),
            "transverse": "z_L=q*a+p*(t+4/25)",
            "absolute_transverse_strict_upper": str(left_transverse_upper),
            "target_radius": str(TARGET_RADIUS),
            "radius_minus_absolute_transverse_strict_lower": str(transverse_margin),
            "discriminant_strictly_positive": True,
            "center_distance_squared_minus_target_radius_squared_strict_lower": str(distance_square_minus_target_radius_square),
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


def targeted_outer_replay(
    registry: dict[str, Any],
    face_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Rebuild the non-q complement for this origin from pinned code.

    The Round218 JSON intentionally contains only an aggregate digest for the
    per-origin exact-behind residual counts.  A whole-origin statement must
    therefore not infer the representative complement from that aggregate.
    This targeted replay independently recovers the 46 Round176 frontier
    roots, the 328 Round180 children, and the unique surviving compact-q
    child for this fixed origin.
    """

    require(
        hashlib.sha256(read_regular(HERE / ROUND218_PROBE, 256 * 1024))
        .hexdigest()
        == ROUND218_PROBE_SHA256,
        "Round218 probe pre-import pin",
    )
    if os.fspath(HERE) not in sys.path:
        sys.path.insert(0, os.fspath(HERE))
    probe = importlib.import_module(ROUND218_PROBE[:-3])
    require(
        Path(probe.__file__).resolve() == (HERE / ROUND218_PROBE).resolve()
        and hashlib.sha256(
            read_regular(HERE / ROUND218_PROBE, 256 * 1024)
        ).hexdigest()
        == ROUND218_PROBE_SHA256,
        "Round218 probe imported identity",
    )
    require(
        probe.r176.FROZEN_OWNER == FROZEN_TARGET,
        "pinned upstream frozen-owner identity",
    )

    print("C30q0 targeted Round176 replay", file=sys.stderr, flush=True)
    replay = probe.r176.replay_frontier()
    origin = replay["origins"].get(ORIGIN)
    require(
        origin is not None
        and origin["chart_id"] == SOURCE_CHART
        and FROZEN_TARGET in origin["active_targets"],
        "representative originates in the pinned frozen-owner workload",
    )
    selected = sorted(
        (
            row for row in replay["frontier"]
            if row.origin_key == ORIGIN
        ),
        key=lambda row: row.key,
    )
    preclosed: list[tuple[Any, str]] = []
    unresolved: list[Any] = []
    for row in selected:
        kind, _evidence = probe.r176.closure(row)
        if kind is None:
            unresolved.append(row)
        else:
            preclosed.append((row, kind))
    require(
        len(selected) == 46
        and len(preclosed)
        == registry["Round176_preclosed_frontier_count"]
        and sorted({kind for _row, kind in preclosed})
        == registry["Round176_preclosed_kinds"]
        and len(unresolved) == registry["Round176_residual_root_count"],
        "representative Round176 complement replay",
    )

    source_grazing_roots = sorted(
        (
            row for row in unresolved
            if probe.r180.residual_category(row)
            == "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
        ),
        key=lambda row: row.key,
    )
    replayed_q_root_rows = [
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
        for row in source_grazing_roots
    ]
    replayed_face_rows = sorted(
        (probe.q_face_evidence(row) for row in source_grazing_roots),
        key=lambda row: row["root_key"],
    )
    require(
        len(source_grazing_roots) == 16
        and all(
            row.box.p0 == Q(511, 512) and row.box.p1 == Q(1)
            for row in source_grazing_roots
        )
        and replayed_face_rows
        == sorted(face_rows, key=lambda row: row["root_key"]),
        "replayed 16 full-r compact-q roots bind the pinned q=0 faces",
    )

    print("C30q0 targeted Round180 refinement", file=sys.stderr, flush=True)
    refinement = probe.r180.refine_origin(unresolved, 4)
    final_rows = sorted(
        refinement["final_residual_rows"],
        key=lambda row: row.key,
    )
    final_categories = Counter(
        probe.r180.residual_category(row) for row in final_rows
    )
    require(
        len(final_rows) == registry["Round180_residual_child_count"]
        and digest([row.key for row in final_rows])
        == registry["Round180_residual_child_keys_sha256"]
        and {
            key: final_categories[key] for key in sorted(final_categories)
        }
        == registry["Round180_residual_category_count"],
        "representative Round180 exact child replay",
    )

    print("C30q0 targeted exact-behind complement", file=sys.stderr, flush=True)
    closed_rows: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []
    for row in final_rows:
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
        (closed_rows if reduction["closed"] else residual_rows).append(summary)
    require(
        len(closed_rows) == 327
        and len(residual_rows) == 1
        and residual_rows[0]["category"]
        == "SOURCE_GRAZING_COMPACT_Q_RESIDUAL",
        "unique representative compact-q residual child",
    )
    return {
        "Round176_frontier_root_count": len(selected),
        "Round176_preclosed_root_count": len(preclosed),
        "Round176_preclosed_disposition_count": {
            key: value
            for key, value in sorted(
                Counter(kind for _row, kind in preclosed).items()
            )
        },
        "Round176_residual_root_count": len(unresolved),
        "Round176_source_grazing_full_r_root_count":
            len(source_grazing_roots),
        "Round176_source_grazing_root_rows_sha256":
            digest(replayed_q_root_rows),
        "Round176_source_grazing_p_interval": ["511/512", "1"],
        "Round176_source_grazing_q_parameterization":
            "q=sqrt(1023/262144)*r, r in [0,1]",
        "Round180_final_child_count": len(final_rows),
        "Round180_final_child_keys_sha256": digest(
            [row.key for row in final_rows]
        ),
        "Round180_final_category_count": {
            key: final_categories[key] for key in sorted(final_categories)
        },
        "exact_behind_closed_child_count": len(closed_rows),
        "exact_behind_closed_child_rows_sha256": digest(closed_rows),
        "exact_behind_residual_child_count": len(residual_rows),
        "exact_behind_residual_child": residual_rows[0],
        "only_unclosed_complement_is_compact_q": True,
    }


def rebuild() -> dict[str, Any]:
    registry, face_rows, pins = frozen_inputs()
    boxes = root_boxes(face_rows)
    analytic = analytic_certificate()
    ownership = half_open_partition(boxes)
    complement = targeted_outer_replay(registry, face_rows)
    serialized_boxes = [
        {
            "root_key": box["root_key"],
            "t": [str(value) for value in box["t"]],
            "r": [str(value) for value in box["r"]],
            "s": [str(value) for value in box["s"]],
            "Round218_q0_face_row_sha256":
                box["Round218_q0_face_row_sha256"],
        }
        for box in boxes
    ]
    return {
        "status": "PASS_REPRESENTATIVE_COMPACT_Q_WHOLE_ORIGIN_ANALYTIC_THEOREM__ZERO_FORMAL_CREDIT",
        "verdict": "PASS_REPRESENTATIVE_THEOREM",
        "frozen_inputs": pins,
        "representative_selection": {
            "origin_key": ORIGIN,
            "Round184_priority_class": registry["priority_class"],
            "Round184_priority_ordinal": registry["priority_ordinal"],
            "selection_uses_new_closure_outcome": False,
            "representative_only": True,
        },
        "root_box_partition": {
            "root_box_count": len(serialized_boxes),
            "root_box_rows_sha256": digest(serialized_boxes),
            "root_box_rows": serialized_boxes,
            "exact_8_by_1_by_2_cartesian_cover": True,
        },
        "analytic_whole_origin_certificate": analytic,
        "cross_root_half_open_owner_partition": ownership,
        "targeted_upstream_complement_replay": complement,
        "representative_conclusion": {
            "origin_key": ORIGIN,
            "analytic_disposition": "EXCLUDED_FROZEN_OWNER_STRICTLY_BEHIND",
            "whole_origin_domain_closed": True,
            "all_3D_2D_1D_0D_strata_closed": True,
            "Round176_preclosed_plus_Round180_exact_behind_plus_analytic_q_cover_is_complete": True,
            "conditional_research_transition": "54 -> 53",
            "scope": "one representative compact-q origin only",
        },
        "strict_nonpromotion": {
            "formal_credit": 0,
            "formal_remaining_origins": 80,
            "compact_q_formal_remaining_origins": 54,
            "ledger_unchanged": True,
            "D02": "BLOCKED",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": "independently verify this representative theorem, then determine and prove the exact parameter cohorts to which the two target inequalities apply before extending to all 54 compact-q origins",
    }


def main() -> int:
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
