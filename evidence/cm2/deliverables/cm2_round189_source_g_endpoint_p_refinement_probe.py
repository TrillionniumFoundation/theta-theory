#!/usr/bin/env python3
"""Read-only feasibility spike for the 288 Round188 endpoint residual faces.

Round188 resolves 15,844 of the 16,132 Round186 no-bracket factor faces by a
complete rectangle-boundary arrangement.  The remaining 288 faces touch
``p = -1`` or ``p = +1``.  Consequently the full-face p derivative is
unavailable while the s derivative is strict.

This probe asks one narrow question: does bounded p bisection make those 288
faces resolvable by the existing Round186 and Round188 face tests?  It emits
diagnostic JSON to stdout and progress to stderr.  It writes no certificate,
issues no whole-leaf or global credit, and does not solve the U|U cross-t glue
or the wall-G tail.

Probe-only trust boundary: Round188 imports Round186 before this module can
check their hashes.  Both imported modules and the complete pinned Round182
chain are therefore verified immediately after import, but this is not an
adversarial import sandbox.  A formal verifier must pin inert bytes before
loading any independent evaluator.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

from flint import ctx

import cm2_round188_source_g_factor_face_boundary_arrangement_probe as r188


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round189.source-g-endpoint-p-refinement-probe.v1"

ROUND188_SOURCE = (
    "cm2_round188_source_g_factor_face_boundary_arrangement_probe.py"
)
ROUND188_SOURCE_SHA256 = (
    "11e033c726a51bab875f42c371682814a84f46871f1a45797d5c68aa3b3149de"
)
ROUND186_SOURCE = "cm2_round186_source_g_factor_face_probe.py"
ROUND186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)

ROUND182_RESULT_SHA256 = (
    "e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d"
)
ROUND182_VERIFICATION_RESULT_SHA256 = (
    "61715ef39e232937d821ba1c634181f905454b758abbe98d889c768ddc809797"
)
ROUND182_PINS = {
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement.py":
        "8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_certificate.json":
        "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json":
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verifier.py":
        "790b17cf6dadebc37b889fff63c6ecde985cccf53c95523cd6c2bc39d12db566",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json":
        "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_report.md":
        "708272e9425bef74f3f4639c76fd17078f509d3acc5d324325c224e743985f0c",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_cold_replay.md":
        "c0fd075a0ba56de5380c6cc89620dc82fa640c0466b118565cf1755aedf61f99",
}
ROUND182_MANIFEST = (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_manifest.sha256"
)
ROUND182_MANIFEST_SHA256 = (
    "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5"
)

EXPECTED_OUTGOING_RESIDUAL_LEAVES = 18_324
EXPECTED_OUTGOING_ORIGINS = 8_268
EXPECTED_RETAINED_CHILDREN = 11_960
EXPECTED_OUTGOING_VOLUME = Q(861459, 419430400000)
EXPECTED_UNRESOLVED_FACES = 18_412
EXPECTED_ROUND186_NO_BRACKET_FACES = 16_132
EXPECTED_ROUND188_RESOLVED_FACES = 15_844
EXPECTED_ENDPOINT_RESIDUAL_FACES = 288
EXPECTED_TWO_SIDED_U_LEAVES = 88
EXPECTED_WALL_G_RESIDUAL_LEAVES = 64

NO_BRACKET = "ONE_ACTIVE_FACTOR_STRICT_DERIVATIVE_NO_BRACKET"
ROUND188_RESOLVED = "UNIQUE_TWO_ENDPOINT_FACTOR_CURVE"
ROUND188_RESIDUAL = "BOUNDARY_ENDPOINT_COUNT_RESIDUAL"
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
FACE_LEVEL_RESOLVED = {
    "BOTH_FACTORS_STRICT",
    "ONE_ACTIVE_FACTOR_ABSENT",
    "ONE_ACTIVE_FACTOR_FULL_GRAPH",
    ROUND188_RESOLVED,
}


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


def regular_file_bytes(path: Path) -> bytes:
    """Read a single-link regular file without following a final symlink."""

    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), f"not regular:{path.name}")
    require(before.st_nlink == 1, f"unexpected link count:{path.name}")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino, opened.st_size)
            == (before.st_dev, before.st_ino, before.st_size),
            f"file changed before read:{path.name}",
        )
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
            (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
            == (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            ),
            f"file changed during read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def pinned_sha256(path: Path, expected: str) -> bytes:
    content = regular_file_bytes(path)
    require(
        hashlib.sha256(content).hexdigest() == expected,
        f"sha256 pin:{path.name}",
    )
    return content


def check_inputs() -> dict[str, Any]:
    """Pin imported probe sources and every file in the Round182 manifest."""

    r186 = r188.r186
    require(
        Path(r188.__file__).resolve() == (HERE / ROUND188_SOURCE).resolve(),
        "Round188 module identity",
    )
    require(
        Path(r186.__file__).resolve() == (HERE / ROUND186_SOURCE).resolve(),
        "Round186 module identity",
    )
    pinned_sha256(HERE / ROUND188_SOURCE, ROUND188_SOURCE_SHA256)
    pinned_sha256(HERE / ROUND186_SOURCE, ROUND186_SOURCE_SHA256)

    for name, expected in ROUND182_PINS.items():
        pinned_sha256(HERE / name, expected)
    manifest_bytes = pinned_sha256(
        HERE / ROUND182_MANIFEST,
        ROUND182_MANIFEST_SHA256,
    )
    manifest: dict[str, str] = {}
    for line in manifest_bytes.decode("ascii").splitlines():
        value, name = line.split("  ", 1)
        require(name not in manifest, f"manifest duplicate:{name}")
        manifest[name] = value
    require(manifest == ROUND182_PINS, "Round182 manifest exact entries")

    certificate = json.loads(
        regular_file_bytes(
            HERE
            / "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
              "_certificate.json"
        )
    )
    verification = json.loads(
        regular_file_bytes(
            HERE
            / "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
              "_verification.json"
        )
    )
    require(
        certificate["result_sha256"] == ROUND182_RESULT_SHA256,
        "Round182 result pin",
    )
    require(
        verification["result_sha256"]
        == ROUND182_VERIFICATION_RESULT_SHA256
        and verification["result"]["status"] == "PASS",
        "Round182 verification result",
    )
    return {
        "Round182_manifest_sha256": ROUND182_MANIFEST_SHA256,
        "Round182_result_sha256": ROUND182_RESULT_SHA256,
        "Round182_rows_sha256": ROUND182_PINS[
            "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
        ],
        "Round182_verification_result_sha256":
            ROUND182_VERIFICATION_RESULT_SHA256,
        "Round186_probe_source_sha256": ROUND186_SOURCE_SHA256,
        "Round188_probe_source_sha256": ROUND188_SOURCE_SHA256,
        "probe_only_import_before_pin_boundary": True,
    }


def face_area(box: Any) -> Q:
    value = (box.p1 - box.p0) * (box.s1 - box.s0)
    require(value > 0, f"strict face area:{box.path}")
    return value


def classify_face(
    collar: dict[str, Any],
    box: Any,
    upper: bool,
) -> tuple[str, str, dict[str, Any]]:
    """Apply Round186 first and Round188 only to its no-bracket residual."""

    r186 = r188.r186
    profile, normal_excluded = r186.face_profile(
        collar["chart"],
        collar["owner_target"],
        box,
        upper,
    )
    require(normal_excluded, f"target normal exclusion:{box.path}")
    label = r186.resolution(profile)
    if label != NO_BRACKET:
        return label, "ROUND186_RESOLUTION", {}
    arrangement = r188.boundary_arrangement(
        collar,
        box,
        upper,
        profile,
    )
    return (
        arrangement["status"],
        "ROUND188_BOUNDARY_ARRANGEMENT",
        arrangement,
    )


def load_scope() -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    r186 = r188.r186
    wrapper = json.loads(regular_file_bytes(r186.ROWS))
    source = wrapper["result"]
    schemas = source["row_column_schemas"]
    collars = r186.unpack(
        source["collar_occurrence_rows"],
        schemas["collar_occurrence_rows"],
    )
    collar_by_occurrence = {
        row["Round179_occurrence_row_id"]: row
        for row in collars
    }
    leaves = r186.unpack(
        source["collar_leaf_rows"],
        schemas["collar_leaf_rows"],
    )
    residual = [
        row
        for row in leaves
        if Q(row["residual_3d_collar_volume"]) > 0
    ]
    outgoing = [
        row
        for row in residual
        if collar_by_occurrence[row["occurrence_row_id"]]["kind"]
        == "OUTGOING"
    ]
    require(
        len(outgoing) == EXPECTED_OUTGOING_RESIDUAL_LEAVES,
        "outgoing residual leaf count",
    )
    require(
        len({
            collar_by_occurrence[row["occurrence_row_id"]]["origin_row_id"]
            for row in outgoing
        })
        == EXPECTED_OUTGOING_ORIGINS,
        "outgoing origin count",
    )
    require(
        len({row["retained_child_row_id"] for row in outgoing})
        == EXPECTED_RETAINED_CHILDREN,
        "retained child count",
    )
    require(
        sum(
            (Q(row["residual_3d_collar_volume"]) for row in outgoing),
            Q(0),
        )
        == EXPECTED_OUTGOING_VOLUME,
        "outgoing exact coordinate volume",
    )
    return outgoing, collar_by_occurrence, source


def reconstruct_endpoint_cohort(
    outgoing: list[dict[str, Any]],
    collar_by_occurrence: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Rebuild Round188's exact 16,132 -> 15,844 + 288 census."""

    r186 = r188.r186
    baseline_classes: Counter[str] = Counter()
    boundary_statuses: Counter[str] = Counter()
    derivative_pairs: Counter[str] = Counter()
    endpoint_sides: Counter[str] = Counter()
    side_counts: Counter[str] = Counter()
    endpoint_faces: list[dict[str, Any]] = []
    two_sided_u_leaves = 0

    for index, row in enumerate(outgoing, 1):
        collar = collar_by_occurrence[row["occurrence_row_id"]]
        box = r186.r179.r174.atlas.AtlasBox(
            *(Q(value) for value in row["box"]),
            0,
            row["row_id"],
        )
        unresolved_sides = [
            (side, upper)
            for side, status, upper in (
                ("LOWER", row["lower_t_face_status"], False),
                ("UPPER", row["upper_t_face_status"], True),
            )
            if status == "U"
        ]
        require(unresolved_sides, f"outgoing unresolved face:{row['row_id']}")
        if len(unresolved_sides) == 2:
            two_sided_u_leaves += 1
        require(
            len(unresolved_sides) in {1, 2},
            f"unresolved side count:{row['row_id']}",
        )

        for side, upper in unresolved_sides:
            profile, normal_excluded = r186.face_profile(
                collar["chart"],
                collar["owner_target"],
                box,
                upper,
            )
            require(
                normal_excluded,
                f"normal exclusion:{row['row_id']}:{side}",
            )
            label = r186.resolution(profile)
            baseline_classes[label] += 1
            if label != NO_BRACKET:
                continue
            arrangement = r188.boundary_arrangement(
                collar,
                box,
                upper,
                profile,
            )
            boundary_statuses[arrangement["status"]] += 1
            if arrangement["status"] != ROUND188_RESIDUAL:
                continue

            require(
                arrangement["dp_sign"] == "UNAVAILABLE",
                f"endpoint residual dp:{row['row_id']}:{side}",
            )
            require(
                arrangement["ds_sign"] in STRICT_SIGNS,
                f"endpoint residual ds:{row['row_id']}:{side}",
            )
            require(
                arrangement["graph_axis"] == "s",
                f"endpoint residual graph axis:{row['row_id']}:{side}",
            )
            touches_negative = box.p0 == Q(-1)
            touches_positive = box.p1 == Q(1)
            require(
                touches_negative or touches_positive,
                f"endpoint residual does not touch p endpoint:"
                f"{row['row_id']}:{side}",
            )
            require(
                not (touches_negative and touches_positive),
                f"endpoint residual touches both p endpoints:"
                f"{row['row_id']}:{side}",
            )
            endpoint_label = "p=-1" if touches_negative else "p=+1"
            endpoint_sides[endpoint_label] += 1
            derivative_pairs[
                arrangement["dp_sign"] + "|" + arrangement["ds_sign"]
            ] += 1
            side_counts[side] += 1
            endpoint_faces.append({
                "leaf_row": row,
                "collar": collar,
                "box": box,
                "side": side,
                "upper": upper,
                "initial_arrangement": arrangement,
                "endpoint": endpoint_label,
                "two_sided_U_leaf": len(unresolved_sides) == 2,
            })
        if index % 2000 == 0 or index == len(outgoing):
            print(
                f"cohort {index}/{len(outgoing)}",
                file=sys.stderr,
                flush=True,
            )

    require(
        sum(baseline_classes.values()) == EXPECTED_UNRESOLVED_FACES,
        "unresolved face conservation",
    )
    require(
        baseline_classes[NO_BRACKET]
        == EXPECTED_ROUND186_NO_BRACKET_FACES,
        "Round186 no-bracket face census",
    )
    require(
        boundary_statuses[ROUND188_RESOLVED]
        == EXPECTED_ROUND188_RESOLVED_FACES,
        "Round188 resolved face census",
    )
    require(
        boundary_statuses[ROUND188_RESIDUAL]
        == EXPECTED_ENDPOINT_RESIDUAL_FACES
        and len(endpoint_faces) == EXPECTED_ENDPOINT_RESIDUAL_FACES,
        "Round188 endpoint residual face census",
    )
    require(
        set(boundary_statuses) == {ROUND188_RESOLVED, ROUND188_RESIDUAL},
        "Round188 exact status support",
    )
    require(
        EXPECTED_ROUND188_RESOLVED_FACES
        + EXPECTED_ENDPOINT_RESIDUAL_FACES
        == EXPECTED_ROUND186_NO_BRACKET_FACES,
        "Round188 binary face census",
    )
    require(
        two_sided_u_leaves == EXPECTED_TWO_SIDED_U_LEAVES,
        "two-sided U leaf census",
    )

    distinct_leaves = {
        item["leaf_row"]["row_id"] for item in endpoint_faces
    }
    distinct_origins = {
        item["collar"]["origin_row_id"] for item in endpoint_faces
    }
    two_sided_faces = sum(
        item["two_sided_U_leaf"] for item in endpoint_faces
    )
    return endpoint_faces, {
        "Round186_baseline_face_classes":
            dict(sorted(baseline_classes.items())),
        "Round188_boundary_status_count":
            dict(sorted(boundary_statuses.items())),
        "Round188_binary_census": (
            f"{EXPECTED_ROUND186_NO_BRACKET_FACES}="
            f"{EXPECTED_ROUND188_RESOLVED_FACES}+"
            f"{EXPECTED_ENDPOINT_RESIDUAL_FACES}"
        ),
        "endpoint_residual_face_count": len(endpoint_faces),
        "endpoint_residual_distinct_leaf_count": len(distinct_leaves),
        "endpoint_residual_distinct_origin_count": len(distinct_origins),
        "endpoint_residual_face_side_count":
            dict(sorted(side_counts.items())),
        "endpoint_residual_p_endpoint_count":
            dict(sorted(endpoint_sides.items())),
        "endpoint_residual_dp_ds_sign_pair_count":
            dict(sorted(derivative_pairs.items())),
        "endpoint_residual_faces_on_two_sided_U_leaves": two_sided_faces,
        "all_endpoint_residual_faces_touch_exactly_one_of_p=-1_or_p=+1":
            True,
    }


def refine_endpoint_faces(
    endpoint_faces: list[dict[str, Any]],
    maximum_depth: int,
) -> dict[str, Any]:
    """Adaptively split only residual faces, with exact per-root area checks."""

    r186 = r188.r186
    node_statuses_by_depth: Counter[tuple[int, str]] = Counter()
    node_methods: Counter[str] = Counter()
    terminal_statuses_by_depth: Counter[tuple[int, str, str]] = Counter()
    split_nodes_by_depth: Counter[int] = Counter()
    child_nodes_by_depth: Counter[int] = Counter()
    endpoint_terminal_counts: Counter[str] = Counter()
    root_audit_rows: list[dict[str, Any]] = []
    total_input_area = Q(0)
    total_resolved_area = Q(0)
    total_residual_area = Q(0)
    resolved_original_faces = 0
    residual_original_faces = 0

    for index, item in enumerate(endpoint_faces, 1):
        root = item["box"]
        upper = item["upper"]
        collar = item["collar"]
        root_area = face_area(root)
        total_input_area += root_area
        queue: list[tuple[Any, int]] = [(root, 0)]
        root_terminal_area = Q(0)
        root_resolved_area = Q(0)
        root_residual_area = Q(0)
        root_split_nodes = 0
        root_child_nodes = 0
        root_terminal_nodes = 0
        root_statuses: Counter[str] = Counter()

        while queue:
            box, depth = queue.pop()
            label, method, _details = classify_face(
                collar,
                box,
                upper,
            )
            resolved = label in FACE_LEVEL_RESOLVED
            node_statuses_by_depth[(depth, label)] += 1
            node_methods[method] += 1
            root_statuses[label] += 1
            if resolved or depth == maximum_depth:
                disposition = "RESOLVED" if resolved else "RESIDUAL"
                area = face_area(box)
                root_terminal_area += area
                root_terminal_nodes += 1
                terminal_statuses_by_depth[
                    (depth, disposition, label)
                ] += 1
                if resolved:
                    root_resolved_area += area
                    total_resolved_area += area
                else:
                    root_residual_area += area
                    total_residual_area += area
                    endpoint_terminal_counts[
                        "touches_p=-1"
                        if box.p0 == Q(-1)
                        else "touches_p=+1"
                        if box.p1 == Q(1)
                        else "strict_interior_p"
                    ] += 1
                continue

            left, right = r186.r179.r174.bisect(box, 1)
            require(
                left.p1 == right.p0,
                f"exact p split edge:{box.path}",
            )
            require(
                left.p0 == box.p0
                and right.p1 == box.p1
                and left.s0 == right.s0 == box.s0
                and left.s1 == right.s1 == box.s1,
                f"exact child bounds:{box.path}",
            )
            require(
                face_area(left) + face_area(right) == face_area(box),
                f"exact split area conservation:{box.path}",
            )
            split_nodes_by_depth[depth] += 1
            child_nodes_by_depth[depth + 1] += 2
            root_split_nodes += 1
            root_child_nodes += 2
            queue.append((right, depth + 1))
            queue.append((left, depth + 1))

        require(
            root_terminal_area == root_area,
            f"per-root exact face area conservation:{root.path}",
        )
        require(
            root_resolved_area + root_residual_area == root_area,
            f"per-root resolved/residual area conservation:{root.path}",
        )
        require(
            root_child_nodes == 2 * root_split_nodes,
            f"per-root binary child census:{root.path}",
        )
        require(
            root_terminal_nodes == root_split_nodes + 1,
            f"per-root full binary tree census:{root.path}",
        )
        if root_residual_area:
            residual_original_faces += 1
        else:
            resolved_original_faces += 1
        root_audit_rows.append({
            "leaf_row_id": item["leaf_row"]["row_id"],
            "origin_row_id": collar["origin_row_id"],
            "side": item["side"],
            "endpoint": item["endpoint"],
            "input_area": str(root_area),
            "resolved_area": str(root_resolved_area),
            "residual_area": str(root_residual_area),
            "split_node_count": root_split_nodes,
            "child_node_count": root_child_nodes,
            "terminal_node_count": root_terminal_nodes,
            "node_status_count": dict(sorted(root_statuses.items())),
        })
        if index % 50 == 0 or index == len(endpoint_faces):
            print(
                f"refinement {index}/{len(endpoint_faces)}",
                file=sys.stderr,
                flush=True,
            )

    total_split_nodes = sum(split_nodes_by_depth.values())
    total_child_nodes = sum(child_nodes_by_depth.values())
    total_terminal_nodes = sum(terminal_statuses_by_depth.values())
    require(
        total_resolved_area + total_residual_area == total_input_area,
        "global exact face area conservation",
    )
    require(
        total_child_nodes == 2 * total_split_nodes,
        "global binary child census",
    )
    require(
        total_terminal_nodes
        == total_split_nodes + EXPECTED_ENDPOINT_RESIDUAL_FACES,
        "global full binary forest census",
    )
    require(
        resolved_original_faces + residual_original_faces
        == EXPECTED_ENDPOINT_RESIDUAL_FACES,
        "original face disposition census",
    )

    if residual_original_faces == 0:
        verdict = "VALIDATED"
        verdict_reason = (
            "bounded p refinement resolves all 288 Round188 endpoint "
            "residual faces at face level"
        )
    elif resolved_original_faces:
        verdict = "PARTIAL"
        verdict_reason = (
            "bounded p refinement resolves only part of the 288-face cohort"
        )
    else:
        verdict = "INVALIDATED"
        verdict_reason = (
            "bounded p refinement resolves none of the 288-face cohort"
        )

    return {
        "question":
            "Can bounded p bisection close the 288 Round188 faces whose "
            "full-face dp is unavailable at p=±1 while ds is strict?",
        "verdict": verdict,
        "verdict_scope": "288-face feasibility subquestion only",
        "verdict_reason": verdict_reason,
        "maximum_p_refinement_depth_requested": maximum_depth,
        "adaptive_stop_after_face_level_resolution": True,
        "input_original_face_count": len(endpoint_faces),
        "resolved_original_face_count": resolved_original_faces,
        "residual_original_face_count": residual_original_faces,
        "node_resolution_status_by_depth": {
            f"{label}@{depth}": count
            for (depth, label), count
            in sorted(node_statuses_by_depth.items())
        },
        "classification_method_count": dict(sorted(node_methods.items())),
        "terminal_status_by_depth": {
            f"{disposition}:{label}@{depth}": count
            for (depth, disposition, label), count
            in sorted(terminal_statuses_by_depth.items())
        },
        "split_node_count_by_depth": {
            str(depth): count
            for depth, count in sorted(split_nodes_by_depth.items())
        },
        "child_node_count_by_depth": {
            str(depth): count
            for depth, count in sorted(child_nodes_by_depth.items())
        },
        "total_split_node_count": total_split_nodes,
        "total_child_node_count": total_child_nodes,
        "total_terminal_node_count": total_terminal_nodes,
        "binary_census": {
            "child_nodes_equal_twice_split_nodes":
                total_child_nodes == 2 * total_split_nodes,
            "terminal_nodes_equal_split_nodes_plus_roots":
                total_terminal_nodes
                == total_split_nodes + len(endpoint_faces),
        },
        "exact_p_s_area": {
            "input": str(total_input_area),
            "resolved": str(total_resolved_area),
            "residual": str(total_residual_area),
            "conserved":
                total_resolved_area + total_residual_area
                == total_input_area,
            "per_original_face_conserved": True,
        },
        "residual_terminal_p_location_count":
            dict(sorted(endpoint_terminal_counts.items())),
        "original_face_audit_row_count": len(root_audit_rows),
        "original_face_audit_rows_sha256": digest(root_audit_rows),
        "internal_p_split_edge_contract": {
            "shared_closed_edge_count": total_split_nodes,
            "exact_child_edge_coincidence_checked": True,
            "measure_additive_area_conservation_checked": True,
            "half_open_ownership_materialized": False,
            "formal_glue_status":
                "PENDING_FORMAL_HALF_OPEN_EDGE_OWNERSHIP_AND_SIGNATURE_GLUE",
        },
        "formalization_warning":
            "face-level resolution does not by itself certify a 3D leaf, "
            "a side-specific return signature, or a global disposition",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--p-depth",
        type=int,
        default=2,
        choices=range(0, 5),
        help="maximum adaptive p-bisection depth (0..4; default: 2)",
    )
    args = parser.parse_args()
    ctx.prec = 256

    pins = check_inputs()
    outgoing, collar_by_occurrence, _source = load_scope()
    endpoint_faces, reconstruction = reconstruct_endpoint_cohort(
        outgoing,
        collar_by_occurrence,
    )
    refinement = refine_endpoint_faces(endpoint_faces, args.p_depth)
    probe_result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_ENDPOINT_P_REFINEMENT_PROBE",
        "input_chain": pins,
        "scope": {
            "source_obstacle": "G",
            "target_obstacle": "W",
            "outgoing_residual_leaf_count":
                EXPECTED_OUTGOING_RESIDUAL_LEAVES,
            "outgoing_origin_count": EXPECTED_OUTGOING_ORIGINS,
            "retained_child_count": EXPECTED_RETAINED_CHILDREN,
            "outgoing_exact_coordinate_volume":
                str(EXPECTED_OUTGOING_VOLUME),
            "Round186_unresolved_t_face_count":
                EXPECTED_UNRESOLVED_FACES,
        },
        "cohort_reconstruction": reconstruction,
        "p_refinement": refinement,
        "uncovered_tail": {
            "two_sided_U_leaf_count": EXPECTED_TWO_SIDED_U_LEAVES,
            "two_sided_U_cross_t_curve_ordering_processed_here": False,
            "wall_G_residual_leaf_count":
                EXPECTED_WALL_G_RESIDUAL_LEAVES,
            "wall_G_processed_here": False,
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "runtime_filesystem_writes": 0,
            "output_path_option_exists": False,
            "whole_leaf_credit_issued": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator": 224580,
            "D02": "UNCHANGED_BLOCKED",
            "global_Gate5_fields": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
            "required_next":
                "formal producer with complete child evidence, half-open "
                "p-edge glue, side-specific return signatures, U|U cross-t "
                "ordering, wall-G tail, and an independent verifier",
        },
    }
    document = {
        "schema": SCHEMA,
        "probe_result": probe_result,
        "probe_result_sha256": digest(probe_result),
    }
    sys.stdout.write(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
