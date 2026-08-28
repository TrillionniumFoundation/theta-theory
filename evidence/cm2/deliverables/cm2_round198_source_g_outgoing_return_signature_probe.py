#!/usr/bin/env python3
"""Read-only side-specific return-signature feasibility probe.

Round195 leaves no local outgoing-W geometric residual and identifies 36,040
strict candidate regions.  This spike asks whether every such region can
receive one unique frozen local return signature without evaluating a
single point.

The reconstruction uses:

* same-Gate3-parent strict closed-box occurrence anchors from Round174 and
  bounded strict child anchors from Round179;
* the Round179 outgoing normal form carried by each Round182 occurrence;
* whole-leaf interval signs of HPLUS/HMINUS to determine the exact outgoing
  cell of each Round195 candidate region; and
* an independent reconstruction of the frozen Gate5 key row, ordinal, and
  identifier.

Within every relevant parent, anchor fields other than outgoing cell/target
chart must be unique.  The outgoing cell is derived from the strict
factor-sign pair, not sampled.  Assignment is fail-closed unless a strict
same-cell resolved anchor shares a positive two-dimensional box face with
the candidate leaf and strict factor enclosures certify a compatible
relative-open cell patch on that shared face.  The Gate5 key does not
contain the outgoing cell; its exact row is
[source chart, target lift, signed wall word, roof].

Probe only: no attachment/certificate/output-path, no global fibre join, and
zero global exact-key disposition credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gc
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from flint import ctx

import cm2_round195_source_g_outgoing_assembly_and_u2_order_probe as r195


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round198.source-g-outgoing-return-signature-probe.v1"

ROUND174_MANIFEST = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization"
    "_manifest.sha256"
)
ROUND174_MANIFEST_SHA256 = (
    "9e92db7748a2c0acdce532c830f899ce153765de64a59e9f372df3099ac91b76"
)
ROUND174_PINS = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py":
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_certificate.json":
        "10221141c58c044b42e43009beb34ae4705995925a88deaa70ff2eba2ea852c7",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json":
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py":
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verification.json":
        "1f65b5e02b1d1e63bd7e41d6a88d5eb180e2be92620af4b8afa2141c9f6e344c",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_report.md":
        "d9a098b344ac008ca921018d80a4490202ff5ba55c26b419943bfccdd99744c7",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_cold_replay.md":
        "19c24d2c9d909c9eac0be6e0b47929356486c181b80589b10f44f944273afd67",
}
ROUND179_MANIFEST = (
    "cm2_round179_source_g_residual_tube_arrangement_manifest.sha256"
)
ROUND179_MANIFEST_SHA256 = (
    "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76"
)
ROUND179_PINS = {
    "cm2_round179_source_g_residual_tube_arrangement.py":
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    "cm2_round179_source_g_residual_tube_arrangement_certificate.json":
        "edc2c538dc04a93c2b873f53e07b5c97c6b395a1d107e7ed2de4cf2c4bd35111",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round179_source_g_residual_tube_arrangement_verifier.py":
        "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
    "cm2_round179_source_g_residual_tube_arrangement_verification.json":
        "37eaa14cd870df64a12c2434deafe5fdead5cec303f5530208f07c11836736bc",
    "cm2_round179_source_g_residual_tube_arrangement_report.md":
        "c656cd3106fbe6c0562ff8ba00205e9d6bb6beac7883094d8f400f33c0389053",
    "cm2_round179_source_g_residual_tube_arrangement_cold_replay.md":
        "125cf5447fb99404b48c5bae27963f935ed19005e55e38f0aa84c89e6898fef1",
}
ROUND182_MANIFEST = (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_manifest.sha256"
)
ROUND182_MANIFEST_SHA256 = (
    "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5"
)
ROUND195_SOURCE = (
    "cm2_round195_source_g_outgoing_assembly_and_u2_order_probe.py"
)
ROUND195_SOURCE_SHA256 = (
    "f70734937ed2630f4357b9e1d860e862c1a932c573c1f93c45788cd5697ee4e1"
)
ROUND195_REPORT = (
    "cm2_round195_source_g_outgoing_assembly_and_u2_order_spike_report.md"
)
ROUND195_REPORT_SHA256 = (
    "2f4318f381b79c28c457ce3e2f54e0b6e843c649738789c6d0f95dc8a6332dac"
)

ROUND174_ROWS = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization"
    "_rows.json"
)
ROUND179_ROWS = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
ROUND174_VERIFICATION = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization"
    "_verification.json"
)
ROUND179_VERIFICATION = (
    "cm2_round179_source_g_residual_tube_arrangement_verification.json"
)

EXPECTED_LEAVES = 18_324
EXPECTED_ORIGINS = 8_268
EXPECTED_PARENTS = 912
EXPECTED_REGIONS = 36_040
EXPECTED_U2_LEAVES = 88
EXPECTED_U2_REGIONS = 176
EXPECTED_R195_LEAF_ROWS_SHA256 = (
    "0370fb57e9d2881a8bc2d0e66351a6c551e147d483558c682f051153924f88b5"
)
EXPECTED_R195_U2_ROWS_SHA256 = (
    "12fbc70f82645ae2ad252b4e88587a7841814a03fda1972a0241cd63c45d6ee0"
)
EXPECTED_SIGNATURE_STATUS_COUNT = {
    "NO_SAME_CELL_STRICT_RESOLVED_ANCHOR_RESIDUAL": 6_388,
    "SAME_CELL_ANCHOR_WITHOUT_FACE_ADJACENCY_RESIDUAL": 26_388,
    "UNIQUE_RECONSTRUCTED_LOCAL_SIGNATURE": 3_264,
}
EXPECTED_CANDIDATE_REGION_ROWS_SHA256 = (
    "e2d8acbfaa3c8377106ea42a72bdd43d11025d43417f7513fe48e6d07677c259"
)
EXPECTED_U2_REGION_ROWS_SHA256 = (
    "9743e4b22ac4f9a89aa7590d79af56c7e5721a28a0a558c173626050a3bfd65c"
)
EXPECTED_PARENT_JOIN_ROWS_SHA256 = (
    "7c9a5e79876b4142e757bc4ebb41c701785f71dfc137ba01365c53a2c1664c19"
)
EXPECTED_PROBE_RESULT_SHA256 = (
    "b6f1660dfe18613ac2b3443c68f56a05f9399d3715c4e7f301fdc0482be459d5"
)
EXPECTED_DOCUMENT_SHA256 = (
    "5d3ddddd6445bc364f7b4febd5f81adcb311d085bce636f9ec74c7a54d3711ee"
)

STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


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


def unpack(document: dict[str, Any], name: str) -> list[dict[str, Any]]:
    columns = document["result"]["row_column_schemas"][name]
    return [
        dict(zip(columns, row, strict=True))
        for row in document["result"][name]
    ]


def check_manifest(
    name: str,
    expected_manifest_sha256: str,
    expected_entries: dict[str, str],
) -> None:
    r189 = r195.r191.r189
    content = r189.pinned_sha256(HERE / name, expected_manifest_sha256)
    entries: dict[str, str] = {}
    for line in content.decode("ascii").splitlines():
        value, filename = line.split("  ", 1)
        require(filename not in entries, f"manifest duplicate:{name}:{filename}")
        entries[filename] = value
    require(entries == expected_entries, f"manifest exact entries:{name}")
    for filename, expected in expected_entries.items():
        r189.pinned_sha256(HERE / filename, expected)


def check_inputs() -> dict[str, Any]:
    r189 = r195.r191.r189
    require(
        Path(r195.__file__).resolve() == (HERE / ROUND195_SOURCE).resolve(),
        "Round195 module identity",
    )
    r189.pinned_sha256(HERE / ROUND195_SOURCE, ROUND195_SOURCE_SHA256)
    r189.pinned_sha256(HERE / ROUND195_REPORT, ROUND195_REPORT_SHA256)
    check_manifest(
        ROUND174_MANIFEST,
        ROUND174_MANIFEST_SHA256,
        ROUND174_PINS,
    )
    check_manifest(
        ROUND179_MANIFEST,
        ROUND179_MANIFEST_SHA256,
        ROUND179_PINS,
    )
    require(
        r189.pinned_sha256(
            HERE / ROUND182_MANIFEST,
            ROUND182_MANIFEST_SHA256,
        ),
        "Round182 manifest bytes",
    )
    upstream = r195.check_inputs()
    for filename, expected_result in (
        (
            ROUND174_VERIFICATION,
            "d45f05458c42189cf0ebc51e258356d13278ba40845cce80b6a072ffbc8cf09b",
        ),
        (
            ROUND179_VERIFICATION,
            "0f57284c11c617349fe66877552c401f426efafbc75faa08948f099166e9cde3",
        ),
    ):
        document = json.loads(r189.regular_file_bytes(HERE / filename))
        require(
            document["result"]["status"] == "PASS"
            and document["result"]["certificate_result_sha256"]
            == expected_result,
            f"verification PASS/result:{filename}",
        )
    return {
        **upstream,
        "Round174_manifest_sha256": ROUND174_MANIFEST_SHA256,
        "Round179_manifest_sha256": ROUND179_MANIFEST_SHA256,
        "Round182_manifest_sha256": ROUND182_MANIFEST_SHA256,
        "Round195_probe_source_sha256": ROUND195_SOURCE_SHA256,
        "Round195_probe_report_sha256": ROUND195_REPORT_SHA256,
        "probe_only_import_before_pin_boundary": True,
    }


def anchor_base(row: dict[str, Any]) -> dict[str, Any]:
    pattern = list(row["signed_wall_word"])
    events = row["ordered_integer_wall_events"]
    require(
        [event[0] for event in events] == pattern,
        f"anchor ordered events/pattern:{row['row_id']}",
    )
    require(
        row["roof"] == len(pattern) + 1,
        f"anchor roof:{row['row_id']}",
    )
    require(
        row["official_key_row"]
        == [
            row["chart"],
            row["owner_target"],
            pattern,
            row["roof"],
        ],
        f"anchor exact key row shape:{row['row_id']}",
    )
    expected_identifier = (
        f"gate5-word:{row['official_key_ordinal']:06d}:"
        f"{digest(row['official_key_row'])}"
    )
    require(
        row["official_key_id"] == expected_identifier,
        f"anchor exact key identifier:{row['row_id']}",
    )
    target_obstacle = row["owner_target"].split("[", 1)[0]
    require(
        row["target_chart"]
        == f"{target_obstacle}:{row['outgoing_cell']}",
        f"anchor target chart:{row['row_id']}",
    )
    return {
        "source_chart": row["chart"],
        "target_lift": row["owner_target"],
        "ordered_integer_wall_events": events,
        "signed_wall_word": pattern,
        "roof": row["roof"],
        "official_key_row": row["official_key_row"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_id": row["official_key_id"],
    }


def load_anchor_ledger(
    relevant_parents: set[str],
    relevant_occurrences: set[str],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    """Load compact same-parent anchors and Round179 carried forms."""

    parent_meta: dict[str, dict[str, Any]] = {}
    base_candidates: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    anchor_cells: dict[str, set[str]] = defaultdict(set)
    anchor_geometry: dict[
        str, dict[str, list[dict[str, Any]]]
    ] = defaultdict(lambda: defaultdict(list))
    anchor_ids: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: {"ROUND174": [], "ROUND179": []}
    )
    anchor_counts: Counter[str] = Counter()

    round174 = json.load((HERE / ROUND174_ROWS).open())
    for row in unpack(round174, "parent_rows"):
        if row["parent_id"] in relevant_parents:
            parent_meta[row["parent_id"]] = {
                "parent_id": row["parent_id"],
                "chart": row["chart"],
                "Gate3_leaf_id": row["leaf_id"],
                "owner_target": row["owner_target"],
            }
    for row in unpack(round174, "resolved_3d_occurrence_rows"):
        if row["parent_id"] not in relevant_parents:
            continue
        base = anchor_base(row)
        base_candidates[row["parent_id"]][digest(base)] = base
        anchor_cells[row["parent_id"]].add(row["outgoing_cell"])
        anchor_geometry[row["parent_id"]][row["outgoing_cell"]].append({
            "source": "ROUND174",
            "row_id": row["row_id"],
            "box": row["box"],
        })
        anchor_ids[row["parent_id"]]["ROUND174"].append(row["row_id"])
        anchor_counts["ROUND174"] += 1
    del round174
    gc.collect()

    carried_forms: dict[str, dict[str, Any]] = {}
    round179 = json.load((HERE / ROUND179_ROWS).open())
    for row in unpack(round179, "resolved_3d_child_rows"):
        if row["parent_id"] not in relevant_parents:
            continue
        base = anchor_base(row)
        base_candidates[row["parent_id"]][digest(base)] = base
        anchor_cells[row["parent_id"]].add(row["outgoing_cell"])
        anchor_geometry[row["parent_id"]][row["outgoing_cell"]].append({
            "source": "ROUND179",
            "row_id": row["row_id"],
            "box": row["box"],
        })
        anchor_ids[row["parent_id"]]["ROUND179"].append(row["row_id"])
        anchor_counts["ROUND179"] += 1
        require(
            row["global_geometric_disposition_credit"] == 0,
            "Round179 anchor zero global credit",
        )
    for row in unpack(round179, "outgoing_normal_form_rows"):
        if row["row_id"] not in relevant_occurrences:
            continue
        require(
            row["gradient_axis"] == "t"
            and row["gradient_sign"] in STRICT_SIGNS
            and row["whole_origin_credit"] == 0
            and row["global_geometric_disposition_credit"] == 0,
            f"Round179 carried outgoing form:{row['row_id']}",
        )
        carried_forms[row["row_id"]] = {
            "row_id": row["row_id"],
            "origin_row_id": row["origin_row_id"],
            "parent_id": row["parent_id"],
            "chart": row["chart"],
            "equation": row["equation"],
            "gradient_axis": row["gradient_axis"],
            "gradient_sign": row["gradient_sign"],
            "face_classification": row["face_classification"],
            "zero_set_dimension_account":
                row["zero_set_dimension_account"],
        }
    del round179
    gc.collect()

    require(
        len(parent_meta) == len(relevant_parents) == EXPECTED_PARENTS,
        "relevant Round174 parent metadata census",
    )
    require(
        len(carried_forms) == len(relevant_occurrences),
        "Round179 carried outgoing occurrence census",
    )

    parent_anchor_rows: list[dict[str, Any]] = []
    bases: dict[str, dict[str, Any]] = {}
    conflicts = 0
    missing = 0
    for parent_id in sorted(relevant_parents):
        candidates = base_candidates.get(parent_id, {})
        if not candidates:
            missing += 1
        elif len(candidates) != 1:
            conflicts += 1
        else:
            bases[parent_id] = next(iter(candidates.values()))
        ids174 = sorted(anchor_ids[parent_id]["ROUND174"])
        ids179 = sorted(anchor_ids[parent_id]["ROUND179"])
        parent_anchor_rows.append({
            **parent_meta[parent_id],
            "base_signature_candidate_count": len(candidates),
            "base_signature_sha256":
                next(iter(candidates)) if len(candidates) == 1 else None,
            "strict_anchor_outgoing_cells":
                sorted(anchor_cells[parent_id]),
            "Round174_anchor_count": len(ids174),
            "Round174_anchor_row_ids_sha256": digest(ids174),
            "Round179_anchor_count": len(ids179),
            "Round179_anchor_row_ids_sha256": digest(ids179),
        })
    diagnostics = {
        "Round174_anchor_count": anchor_counts["ROUND174"],
        "Round179_anchor_count": anchor_counts["ROUND179"],
        "parent_base_signature_missing_count": missing,
        "parent_base_signature_conflict_count": conflicts,
        "parent_base_signature_unique_count": len(bases),
        "parent_anchor_cell_count":
            dict(sorted(Counter(
                len(anchor_cells[parent])
                for parent in relevant_parents
            ).items())),
        "parent_anchor_cell_set_count":
            dict(sorted(Counter(
                "|".join(sorted(anchor_cells[parent]))
                for parent in relevant_parents
            ).items())),
        "strict_anchor_geometry_row_count": sum(
            len(rows)
            for by_cell in anchor_geometry.values()
            for rows in by_cell.values()
        ),
    }
    return bases, parent_meta, parent_anchor_rows, {
        "anchor_cells": {
            parent: set(anchor_cells[parent])
            for parent in relevant_parents
        },
        "anchor_geometry": {
            parent: {
                cell: sorted(rows, key=lambda row: row["row_id"])
                for cell, rows in by_cell.items()
            }
            for parent, by_cell in anchor_geometry.items()
        },
        "carried_forms": carried_forms,
        "diagnostics": diagnostics,
    }


def selected_factor_profiles(
    collar: dict[str, Any],
    box: Any,
) -> dict[str, dict[str, str]]:
    r186 = r195.r191.r189.r188.r186
    geometry = r186.factor_geometry(
        collar["chart"],
        collar["owner_target"],
        box,
    )
    profiles: dict[str, dict[str, str]] = {}
    for kind in ("HPLUS", "HMINUS"):
        direct_sign = r186.r179.arb_sign(geometry[kind][0])
        centered_sign = r186.r179.arb_sign(r186.centered_value(
            collar["chart"],
            collar["owner_target"],
            box,
            kind,
        ))
        profiles[kind] = {
            "direct_sign": direct_sign,
            "centered_sign": centered_sign,
            "selected_sign": (
                direct_sign
                if direct_sign in STRICT_SIGNS
                else centered_sign
            ),
        }
    return profiles


def outgoing_cell(hplus_sign: str, hminus_sign: str) -> str:
    require(
        hplus_sign in STRICT_SIGNS and hminus_sign in STRICT_SIGNS,
        "strict factor-sign pair",
    )
    return {
        ("STRICT_POSITIVE", "STRICT_POSITIVE"): "E",
        ("STRICT_NEGATIVE", "STRICT_NEGATIVE"): "W",
        ("STRICT_POSITIVE", "STRICT_NEGATIVE"): "N",
        ("STRICT_NEGATIVE", "STRICT_POSITIVE"): "S",
    }[(hplus_sign, hminus_sign)]


def positive_two_dimensional_face_intersection(
    left_box: list[str],
    right_box: list[str],
) -> dict[str, Any] | None:
    """Return an exact positive-2D shared box face, or ``None``."""

    require(
        len(left_box) == len(right_box) == 6,
        "three-dimensional anchor/candidate boxes",
    )
    left = [Q(value) for value in left_box]
    right = [Q(value) for value in right_box]
    touching: list[tuple[int, str, str]] = []
    intersection: list[Q] = []
    for axis in range(3):
        left_lo, left_hi = left[2 * axis:2 * axis + 2]
        right_lo, right_hi = right[2 * axis:2 * axis + 2]
        overlap_lo = max(left_lo, right_lo)
        overlap_hi = min(left_hi, right_hi)
        if overlap_hi < overlap_lo:
            return None
        if overlap_hi == overlap_lo:
            if left_hi == right_lo:
                touching.append((axis, "UPPER", "LOWER"))
            elif right_hi == left_lo:
                touching.append((axis, "LOWER", "UPPER"))
            else:
                return None
        intersection.extend((overlap_lo, overlap_hi))
    if len(touching) != 1:
        return None
    axis, candidate_side, anchor_side = touching[0]
    return {
        "axis": ("t", "p", "s")[axis],
        "candidate_side": candidate_side,
        "anchor_side": anchor_side,
        "box": [str(value) for value in intersection],
    }


def compatible_strict_cell_patch(
    collar: dict[str, Any],
    face: dict[str, Any],
    hplus_sign: str,
    hminus_sign: str,
    path: str,
) -> dict[str, Any]:
    """Certify a full relative-open shared-face patch in the target cell."""

    r186 = r195.r191.r189.r188.r186
    face_box = r186.r179.r174.atlas.AtlasBox(
        *(Q(value) for value in face["box"]),
        0,
        path,
    )
    profiles = selected_factor_profiles(collar, face_box)
    compatible = (
        profiles["HPLUS"]["selected_sign"] == hplus_sign
        and profiles["HMINUS"]["selected_sign"] == hminus_sign
        and hplus_sign in STRICT_SIGNS
        and hminus_sign in STRICT_SIGNS
    )
    return {
        **face,
        "HPLUS_C0": profiles["HPLUS"],
        "HMINUS_C0": profiles["HMINUS"],
        "classification": (
            "FULL_RELATIVE_OPEN_STRICT_FACTOR_CELL_PATCH"
            "__NO_EQUALITY_CARRIER"
            if compatible
            else
            "FULL_STRICT_COMPATIBLE_CELL_PATCH_NOT_CERTIFIED"
            "__RESIDUAL"
        ),
        "compatible_nonempty_relative_open_cell_patch": compatible,
    }


def factor_region_rows(
    leaf: dict[str, Any],
    raw: dict[str, Any],
    collar: dict[str, Any],
    box: Any,
    final_faces: list[dict[str, Any]],
    base: dict[str, Any] | None,
    anchor_cells: set[str],
    anchor_geometry: dict[str, list[dict[str, Any]]],
    carried: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    profiles = selected_factor_profiles(collar, box)
    strict = {
        kind: profile["selected_sign"]
        for kind, profile in profiles.items()
        if profile["selected_sign"] in STRICT_SIGNS
    }
    classification = leaf["final_graph_classification"]
    if classification == "EMPTY":
        require(len(strict) in {1, 2}, f"empty strict factor:{leaf['leaf_row_id']}")
    else:
        require(
            len(strict) == 1,
            f"sheet has one strict inactive factor:{leaf['leaf_row_id']}",
        )

    active_from_faces = {
        face["active_factor"]
        for face in final_faces
        if face["active_factor"] is not None
    }
    if len(strict) == 1:
        inactive_factor, inactive_sign = next(iter(strict.items()))
        active_factor = (
            "HMINUS" if inactive_factor == "HPLUS" else "HPLUS"
        )
        require(
            not active_from_faces or active_from_faces == {active_factor},
            f"face/whole-box active factor agreement:{leaf['leaf_row_id']}",
        )
    else:
        inactive_factor = None
        inactive_sign = None
        active_factor = None

    region_rows = []
    shared_face_proof_cache: dict[
        tuple[tuple[str, ...], str, str], dict[str, Any]
    ] = {}
    for f_sign in leaf["candidate_region_signs"]:
        require(f_sign in STRICT_SIGNS, "strict region F sign")
        if len(strict) == 2:
            hplus_sign = strict["HPLUS"]
            hminus_sign = strict["HMINUS"]
        else:
            assert inactive_factor is not None
            assert inactive_sign is not None
            assert active_factor is not None
            active_sign = r195.multiply_signs(f_sign, inactive_sign)
            hplus_sign = (
                active_sign if active_factor == "HPLUS" else inactive_sign
            )
            hminus_sign = (
                active_sign if active_factor == "HMINUS" else inactive_sign
            )
        require(
            r195.multiply_signs(hplus_sign, hminus_sign) == f_sign,
            f"factorized region F sign:{leaf['leaf_row_id']}",
        )
        cell = outgoing_cell(hplus_sign, hminus_sign)
        same_cell_anchors = anchor_geometry.get(cell, [])
        box_face_adjacencies: list[dict[str, Any]] = []
        compatible_patch_anchors: list[dict[str, Any]] = []
        for anchor in same_cell_anchors:
            face = positive_two_dimensional_face_intersection(
                raw["box"],
                anchor["box"],
            )
            if face is None:
                continue
            cache_key = (
                tuple(face["box"]),
                hplus_sign,
                hminus_sign,
            )
            if cache_key not in shared_face_proof_cache:
                shared_face_proof_cache[cache_key] = (
                    compatible_strict_cell_patch(
                        collar,
                        face,
                        hplus_sign,
                        hminus_sign,
                        (
                            f"{leaf['leaf_row_id']}:shared-face:"
                            f"{digest(cache_key)}"
                        ),
                    )
                )
            proof = shared_face_proof_cache[cache_key]
            record = {
                "source": anchor["source"],
                "row_id": anchor["row_id"],
                "shared_face_proof": proof,
            }
            box_face_adjacencies.append(record)
            if proof[
                "compatible_nonempty_relative_open_cell_patch"
            ]:
                compatible_patch_anchors.append(record)
        if base is None or carried is None:
            signature_status = (
                "MISSING_PARENT_BASE_ANCHOR"
                if base is None
                else "MISSING_ROUND179_CARRIED_FORM"
            )
            signature = None
            reconstruction_mode = None
        elif not compatible_patch_anchors:
            require(
                base["source_chart"] == collar["chart"]
                and base["target_lift"] == collar["owner_target"],
                f"frozen chart/target anchor binding:{leaf['leaf_row_id']}",
            )
            require(
                carried["origin_row_id"] == collar["origin_row_id"]
                and carried["parent_id"] == collar["parent_id"]
                and carried["chart"] == collar["chart"]
                and carried["gradient_sign"]
                == leaf["whole_leaf_outgoing_t_derivative_sign"],
                f"Round179 carried-form binding:{leaf['leaf_row_id']}",
            )
            signature_status = (
                "NO_SAME_CELL_STRICT_RESOLVED_ANCHOR_RESIDUAL"
                if cell not in anchor_cells
                else (
                    "SAME_CELL_ANCHOR_WITHOUT_FACE_ADJACENCY_RESIDUAL"
                    if not box_face_adjacencies
                    else
                    "BOX_FACE_ADJACENT_SAME_CELL_ANCHOR_WITHOUT_"
                    "COMPATIBLE_STRICT_SIGN_PATCH_RESIDUAL"
                )
            )
            signature = None
            reconstruction_mode = (
                "WHOLE_REGION_FACTOR_CELL_DERIVED_BUT_NOT_PROMOTED"
            )
        else:
            require(
                base["source_chart"] == collar["chart"]
                and base["target_lift"] == collar["owner_target"],
                f"frozen chart/target anchor binding:{leaf['leaf_row_id']}",
            )
            require(
                carried["origin_row_id"] == collar["origin_row_id"]
                and carried["parent_id"] == collar["parent_id"]
                and carried["chart"] == collar["chart"]
                and carried["gradient_sign"]
                == leaf["whole_leaf_outgoing_t_derivative_sign"],
                f"Round179 carried-form binding:{leaf['leaf_row_id']}",
            )
            signature = {
                **base,
                "outgoing_cell": cell,
                "target_chart":
                    f"{base['target_lift'].split('[', 1)[0]}:{cell}",
            }
            signature_status = "UNIQUE_RECONSTRUCTED_LOCAL_SIGNATURE"
            reconstruction_mode = (
                "DIRECT_COMPATIBLE_STRICT_SHARED_FACE_PATCH_ANCHOR"
            )
        region_rows.append({
            "candidate_region_id":
                leaf["leaf_row_id"] + ":" + f_sign,
            "leaf_row_id": leaf["leaf_row_id"],
            "origin_row_id": leaf["origin_row_id"],
            "parent_id": collar["parent_id"],
            "occurrence_row_id": leaf["occurrence_row_id"],
            "leaf_classification": classification,
            "F_sign": f_sign,
            "HPLUS_sign": hplus_sign,
            "HMINUS_sign": hminus_sign,
            "outgoing_cell": cell,
            "whole_box_factor_C0": profiles,
            "inactive_factor": inactive_factor,
            "Round179_carried_form_row_id":
                None if carried is None else carried["row_id"],
            "anchor_cell_directly_observed": cell in anchor_cells,
            "same_cell_strict_anchor_count": len(same_cell_anchors),
            "box_face_adjacent_same_cell_strict_anchor_count":
                len(box_face_adjacencies),
            "box_face_adjacent_axis_count": dict(sorted(Counter(
                anchor["shared_face_proof"]["axis"]
                for anchor in box_face_adjacencies
            ).items())),
            "box_face_adjacent_same_cell_strict_anchor_proofs_sha256":
                digest(box_face_adjacencies),
            "compatible_strict_shared_face_patch_anchor_count":
                len(compatible_patch_anchors),
            "compatible_strict_shared_face_patch_axis_count":
                dict(sorted(Counter(
                    anchor["shared_face_proof"]["axis"]
                    for anchor in compatible_patch_anchors
                ).items())),
            "compatible_strict_shared_face_patch_source_count":
                dict(sorted(Counter(
                    anchor["source"]
                    for anchor in compatible_patch_anchors
                ).items())),
            "compatible_strict_shared_face_patch_proofs_sha256":
                digest(compatible_patch_anchors),
            "signature_status": signature_status,
            "reconstruction_mode": reconstruction_mode,
            "local_return_signature": signature,
            "single_point_evaluation_used": False,
            "side_specific_signature_materialized_as_formal_row": False,
            "global_exact_key_disposition_credit": 0,
        })
    require(
        len(region_rows)
        == leaf["side_specific_signature_candidate_region_count"],
        f"candidate-region conservation:{leaf['leaf_row_id']}",
    )
    return region_rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only Round198 outgoing-W side-specific return-signature "
            "feasibility probe; no output path and zero global credit."
        )
    )
    parser.parse_args()
    ctx.prec = 256
    pins = check_inputs()

    outgoing, collar_by_occurrence, source = r195.r191.r189.load_scope()
    del source
    gc.collect()
    require(len(outgoing) == EXPECTED_LEAVES, "Round195 leaf input census")
    relevant_parents = {
        collar_by_occurrence[row["occurrence_row_id"]]["parent_id"]
        for row in outgoing
    }
    relevant_occurrences = {row["occurrence_row_id"] for row in outgoing}
    relevant_origins = {
        collar_by_occurrence[row["occurrence_row_id"]]["origin_row_id"]
        for row in outgoing
    }
    require(
        len(relevant_parents) == EXPECTED_PARENTS
        and len(relevant_origins) == EXPECTED_ORIGINS,
        "relevant parent/origin census",
    )
    (
        bases,
        parent_meta,
        parent_anchor_rows,
        anchor_aux,
    ) = load_anchor_ledger(relevant_parents, relevant_occurrences)
    anchor_cells = anchor_aux["anchor_cells"]
    anchor_geometry = anchor_aux["anchor_geometry"]
    carried_forms = anchor_aux["carried_forms"]
    anchor_diagnostics = anchor_aux["diagnostics"]

    # Independently rebuild every frozen exact key used by a parent base.
    r174v = r195.r191.r189.r188.r186.r179.r174
    frozen = r174v.load_frozen_inputs()
    registry = r174v.rebuild_registry(frozen["gate5"])
    del frozen
    for parent_id, base in bases.items():
        expected = r174v.exact_key(
            base["source_chart"],
            base["target_lift"],
            tuple(base["signed_wall_word"]),
            registry,
        )
        require(
            expected == {
                "row": base["official_key_row"],
                "ordinal": base["official_key_ordinal"],
                "identifier": base["official_key_id"],
            },
            f"independent Gate5 exact key:{parent_id}",
        )

    leaf_rows: list[dict[str, Any]] = []
    u2_audit_rows: list[dict[str, Any]] = []
    region_rows: list[dict[str, Any]] = []
    u2_leaf_ids: set[str] = set()
    r186 = r195.r191.r189.r188.r186
    for index, raw in enumerate(outgoing, 1):
        collar = collar_by_occurrence[raw["occurrence_row_id"]]
        box = r186.r179.r174.atlas.AtlasBox(
            *(Q(value) for value in raw["box"]),
            0,
            raw["row_id"],
        )
        final_face_rows: dict[str, dict[str, Any]] = {}
        for side, upper, encoded in (
            ("LOWER", False, raw["lower_t_face_status"]),
            ("UPPER", True, raw["upper_t_face_status"]),
        ):
            if encoded == "U":
                final_face_rows[side] = r195.final_unresolved_face(
                    raw,
                    collar,
                    box,
                    side,
                    upper,
                )
        lower = (
            r195.side_summary(final_face_rows["LOWER"])
            if "LOWER" in final_face_rows
            else r195.decode_round182_face(raw["lower_t_face_status"])
        )
        upper = (
            r195.side_summary(final_face_rows["UPPER"])
            if "UPPER" in final_face_rows
            else r195.decode_round182_face(raw["upper_t_face_status"])
        )
        leaf = r195.classify_leaf(raw, collar, box, lower, upper)
        leaf_rows.append(leaf)
        is_u2 = (
            raw["lower_t_face_status"] == "U"
            and raw["upper_t_face_status"] == "U"
        )
        if is_u2:
            u2_leaf_ids.add(raw["row_id"])
            u2_audit_rows.append(r195.audit_u2_leaf(
                leaf,
                raw,
                collar,
                box,
                final_face_rows["LOWER"],
                final_face_rows["UPPER"],
            ))
        parent_id = collar["parent_id"]
        region_rows.extend(factor_region_rows(
            leaf,
            raw,
            collar,
            box,
            list(final_face_rows.values()),
            bases.get(parent_id),
            anchor_cells[parent_id],
            anchor_geometry.get(parent_id, {}),
            carried_forms.get(raw["occurrence_row_id"]),
        ))
        if index % 2000 == 0 or index == len(outgoing):
            print(
                f"return-signature {index}/{len(outgoing)}",
                file=sys.stderr,
                flush=True,
            )

    leaf_rows.sort(key=lambda row: row["leaf_row_id"])
    u2_audit_rows.sort(key=lambda row: row["leaf_row_id"])
    region_rows.sort(key=lambda row: row["candidate_region_id"])
    require(
        digest(leaf_rows) == EXPECTED_R195_LEAF_ROWS_SHA256,
        "Round195 leaf-row reconstruction pin",
    )
    require(
        len(u2_audit_rows) == EXPECTED_U2_LEAVES
        and digest(u2_audit_rows) == EXPECTED_R195_U2_ROWS_SHA256,
        "Round195 U|U audit reconstruction pin",
    )
    require(len(region_rows) == EXPECTED_REGIONS, "candidate region census")

    status_counts = Counter(row["signature_status"] for row in region_rows)
    require(
        dict(sorted(status_counts.items()))
        == EXPECTED_SIGNATURE_STATUS_COUNT,
        "frozen signature-status census",
    )
    require(
        digest(region_rows) == EXPECTED_CANDIDATE_REGION_ROWS_SHA256,
        "candidate-region row digest pin",
    )
    mode_counts = Counter(str(row["reconstruction_mode"]) for row in region_rows)
    cell_counts = Counter(row["outgoing_cell"] for row in region_rows)
    sign_counts = Counter(row["F_sign"] for row in region_rows)
    class_region_counts = Counter(
        row["leaf_classification"] for row in region_rows
    )
    involved_origins = {row["origin_row_id"] for row in region_rows}
    involved_parents = {row["parent_id"] for row in region_rows}
    signatures = [
        row["local_return_signature"]
        for row in region_rows
        if row["local_return_signature"] is not None
    ]
    distinct_signature_sha256 = {
        digest(signature) for signature in signatures
    }
    assigned_exact_key_ordinals = sorted({
        signature["official_key_ordinal"] for signature in signatures
    })
    assigned_exact_key_ids = sorted({
        signature["official_key_id"] for signature in signatures
    })
    exact_key_ordinals = sorted({
        base["official_key_ordinal"] for base in bases.values()
    })
    exact_key_ids = sorted({
        base["official_key_id"] for base in bases.values()
    })
    require(
        len(exact_key_ordinals) == len(exact_key_ids),
        "exact key ordinal/id bijection in scope",
    )
    require(
        len(assigned_exact_key_ordinals) == len(assigned_exact_key_ids),
        "assigned exact key ordinal/id bijection",
    )
    residual_rows = [
        row
        for row in region_rows
        if row["local_return_signature"] is None
    ]
    residual_class_counts = Counter(
        row["leaf_classification"] for row in residual_rows
    )
    residual_cell_counts = Counter(
        row["outgoing_cell"] for row in residual_rows
    )
    residual_origin_count = len({
        row["origin_row_id"] for row in residual_rows
    })
    residual_parent_count = len({
        row["parent_id"] for row in residual_rows
    })
    residual_leaf_count = len({
        row["leaf_row_id"] for row in residual_rows
    })
    box_face_adjacent_region_count = sum(
        row["box_face_adjacent_same_cell_strict_anchor_count"] > 0
        for row in region_rows
    )
    compatible_patch_region_count = sum(
        row["compatible_strict_shared_face_patch_anchor_count"] > 0
        for row in region_rows
    )
    box_face_axis_counts: Counter[str] = Counter()
    compatible_patch_axis_counts: Counter[str] = Counter()
    compatible_patch_source_counts: Counter[str] = Counter()
    for row in region_rows:
        box_face_axis_counts.update(row["box_face_adjacent_axis_count"])
        compatible_patch_axis_counts.update(
            row["compatible_strict_shared_face_patch_axis_count"]
        )
        compatible_patch_source_counts.update(
            row["compatible_strict_shared_face_patch_source_count"]
        )
    u2_region_rows = [
        row for row in region_rows if row["leaf_row_id"] in u2_leaf_ids
    ]
    require(
        len(u2_region_rows) == EXPECTED_U2_REGIONS,
        "U|U signature-region census",
    )
    require(
        digest(u2_region_rows) == EXPECTED_U2_REGION_ROWS_SHA256,
        "U|U signature-region digest pin",
    )
    u2_status = Counter(row["signature_status"] for row in u2_region_rows)

    candidate_cells_by_parent: dict[str, set[str]] = defaultdict(set)
    region_count_by_parent: Counter[str] = Counter()
    assigned_count_by_parent: Counter[str] = Counter()
    residual_count_by_parent: Counter[str] = Counter()
    for row in region_rows:
        candidate_cells_by_parent[row["parent_id"]].add(
            row["outgoing_cell"]
        )
        region_count_by_parent[row["parent_id"]] += 1
        if row["local_return_signature"] is None:
            residual_count_by_parent[row["parent_id"]] += 1
        else:
            assigned_count_by_parent[row["parent_id"]] += 1
    parent_join_rows = []
    invalid_cell_unions = 0
    valid_adjacent_sets = {
        ("E",),
        ("W",),
        ("N",),
        ("S",),
        ("E", "N"),
        ("E", "S"),
        ("N", "W"),
        ("S", "W"),
    }
    for row in parent_anchor_rows:
        parent_id = row["parent_id"]
        candidate_cells = sorted(candidate_cells_by_parent[parent_id])
        anchor_set = set(row["strict_anchor_outgoing_cells"])
        union = tuple(sorted(anchor_set | set(candidate_cells)))
        if union not in valid_adjacent_sets:
            invalid_cell_unions += 1
        parent_join_rows.append({
            **row,
            "candidate_region_outgoing_cells": candidate_cells,
            "anchor_and_candidate_cell_union": list(union),
            "candidate_cell_count": len(candidate_cells),
            "candidate_cells_without_direct_anchor":
                sorted(set(candidate_cells) - anchor_set),
            "candidate_region_count": region_count_by_parent[parent_id],
            "face_adjacent_assigned_candidate_region_count":
                assigned_count_by_parent[parent_id],
            "residual_candidate_region_count":
                residual_count_by_parent[parent_id],
            "base_signature_unique": (
                row["base_signature_candidate_count"] == 1
            ),
        })
    require(
        digest(parent_join_rows) == EXPECTED_PARENT_JOIN_ROWS_SHA256,
        "parent join row digest pin",
    )
    require(
        compatible_patch_region_count
        == status_counts["UNIQUE_RECONSTRUCTED_LOCAL_SIGNATURE"]
        == box_face_adjacent_region_count
        and len(signatures) + len(residual_rows) == EXPECTED_REGIONS
        and sum(box_face_axis_counts.values())
        == sum(compatible_patch_axis_counts.values())
        == sum(compatible_patch_source_counts.values()),
        "strict shared-face assignment conservation",
    )

    verdict = (
        "VALIDATED"
        if (
            status_counts
            == {"UNIQUE_RECONSTRUCTED_LOCAL_SIGNATURE": EXPECTED_REGIONS}
            and len(involved_origins) == EXPECTED_ORIGINS
            and len(involved_parents) == EXPECTED_PARENTS
            and u2_status
            == {
                "UNIQUE_RECONSTRUCTED_LOCAL_SIGNATURE":
                    EXPECTED_U2_REGIONS
            }
            and invalid_cell_unions == 0
        )
        else "PARTIAL"
    )
    probe_result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_SOURCE_G_OUTGOING_RETURN_SIGNATURE_PROBE",
        "question":
            "Can every one of the 36,040 Round195 strict outgoing-W "
            "candidate regions receive one unique frozen local return "
            "signature from same-parent strict anchors and carried forms, "
            "without a single-point guess?",
        "verdict": verdict,
        "verdict_scope":
            "local side-specific signature feasibility only; rows are not "
            "a formal attachment and no global exact-key fibre is disposed",
        "input_chain": pins,
        "anchor_ledger": {
            **anchor_diagnostics,
            "relevant_parent_count": len(parent_anchor_rows),
            "parent_anchor_rows_sha256": digest(parent_anchor_rows),
            "Round179_carried_outgoing_form_count": len(carried_forms),
            "Round179_carried_outgoing_forms_sha256":
                digest([carried_forms[key] for key in sorted(carried_forms)]),
            "all_parent_base_signatures_unique":
                anchor_diagnostics[
                    "parent_base_signature_unique_count"
                ]
                == EXPECTED_PARENTS,
            "single_point_evaluation_used": False,
            "anchor_evidence_kind":
                "strict positive-volume closed-enclosure occurrence rows",
            "candidate_anchor_adjacency_definition":
                "same Gate3 parent, same certified outgoing cell, and "
                "exact box closures share one positive-2D face patch on "
                "which pinned whole-face HPLUS/HMINUS enclosures are both "
                "strict with the candidate cell signs",
            "shared_face_patch_proof_strength":
                "full strict compatible relative-open patch; equality-only "
                "or merely box-adjacent contacts remain residual",
            "parent_base_plus_unobserved_cell_extrapolation_allowed": False,
        },
        "Gate5_exact_key_reconstruction": {
            "registry_pair_count": len(registry["pairs"]),
            "registry_pattern_count": len(registry["patterns"]),
            "involved_exact_key_count": len(exact_key_ids),
            "involved_exact_key_ordinals_sha256": digest(exact_key_ordinals),
            "involved_exact_key_ids_sha256": digest(exact_key_ids),
            "assigned_region_exact_key_count":
                len(assigned_exact_key_ids),
            "assigned_region_exact_key_ordinals_sha256":
                digest(assigned_exact_key_ordinals),
            "assigned_region_exact_key_ids_sha256":
                digest(assigned_exact_key_ids),
            "every_parent_base_key_independently_rebuilt": True,
            "key_row_fields":
                "[source_chart,target_lift,signed_wall_word,roof]",
            "outgoing_cell_is_not_a_Gate5_exact_key_row_field": True,
        },
        "signature_reconstruction": {
            "candidate_region_count": len(region_rows),
            "candidate_region_rows_sha256": digest(region_rows),
            "signature_status_count": dict(sorted(status_counts.items())),
            "reconstruction_mode_count": dict(sorted(mode_counts.items())),
            "leaf_classification_region_count":
                dict(sorted(class_region_counts.items())),
            "F_sign_count": dict(sorted(sign_counts.items())),
            "outgoing_cell_count": dict(sorted(cell_counts.items())),
            "covered_origin_count": len(involved_origins),
            "covered_parent_count": len(involved_parents),
            "assigned_signature_count": len(signatures),
            "distinct_local_signature_count":
                len(distinct_signature_sha256),
            "distinct_local_signature_digests_sha256":
                digest(sorted(distinct_signature_sha256)),
            "missing_signature_count":
                len(residual_rows),
            "conflicting_signature_count":
                status_counts.get("CONFLICTING_PARENT_BASE_ANCHORS", 0),
            "unique_signature_assignment_count":
                status_counts[
                    "UNIQUE_RECONSTRUCTED_LOCAL_SIGNATURE"
                ],
            "box_face_adjacent_candidate_region_count":
                box_face_adjacent_region_count,
            "compatible_strict_shared_face_patch_candidate_region_count":
                compatible_patch_region_count,
            "box_face_adjacent_anchor_axis_count":
                dict(sorted(box_face_axis_counts.items())),
            "compatible_strict_shared_face_patch_anchor_axis_count":
                dict(sorted(compatible_patch_axis_counts.items())),
            "compatible_strict_shared_face_patch_anchor_source_count":
                dict(sorted(compatible_patch_source_counts.items())),
            "all_factor_signs_certified_on_whole_leaf_boxes": True,
            "all_outgoing_cells_derived_from_HPLUS_HMINUS_signs": True,
            "residual_leaf_classification_count":
                dict(sorted(residual_class_counts.items())),
            "residual_outgoing_cell_count":
                dict(sorted(residual_cell_counts.items())),
            "residual_leaf_count": residual_leaf_count,
            "residual_origin_count": residual_origin_count,
            "residual_parent_count": residual_parent_count,
            "single_point_signature_guess_count": 0,
            "unanchored_cell_signature_guess_count": 0,
            "side_specific_signature_rows_formally_materialized": False,
        },
        "U_pipe_U_signature_glue": {
            "U_pipe_U_leaf_count": len(u2_leaf_ids),
            "candidate_region_count": len(u2_region_rows),
            "signature_status_count": dict(sorted(u2_status.items())),
            "region_rows_sha256": digest(u2_region_rows),
            "Round195_cross_t_ordering_rebuilt": True,
            "both_sides_receive_unique_signatures": (
                u2_status
                == {
                    "UNIQUE_RECONSTRUCTED_LOCAL_SIGNATURE":
                        EXPECTED_U2_REGIONS
                }
            ),
        },
        "parent_cell_join_audit": {
            "parent_join_row_count": len(parent_join_rows),
            "parent_join_rows_sha256": digest(parent_join_rows),
            "invalid_nonadjacent_anchor_candidate_cell_union_count":
                invalid_cell_unions,
            "parents_with_residual_candidate_regions": sum(
                count > 0 for count in residual_count_by_parent.values()
            ),
            "candidate_cells_derived_from_whole_region_factor_signs": True,
            "missing_nonadjacent_or_sign_incompatible_anchor_cells_promoted":
                False,
        },
        "remaining_global_fibre_join_gap": {
            "local_outgoing_W_signature_feasibility_complete":
                verdict == "VALIDATED",
            "separate_wall_G_residual_leaf_count": 64,
            "wall_G_signatures_processed_here": False,
            "formal_signature_attachment_emitted": False,
            "local_signature_residual_candidate_region_count":
                len(residual_rows),
            "local_signature_residual_origin_count":
                residual_origin_count,
            "local_signature_residual_parent_count":
                residual_parent_count,
            "half_open_boundary_ownership_materialized": False,
            "global_source_G_exact_key_fibre_count": 224580,
            "global_fibre_occurrence_join_and_deduplication_performed": False,
            "fibre_wide_all_occurrences_covered_or_excluded": False,
            "required_next":
                "first materialize strict same-cell adjacency anchors for "
                "every residual outgoing-W candidate region (without "
                "parent-base extrapolation), then formalize the local rows, "
                "close the 64 wall-G leaves, and join every source-G "
                "occurrence by official key across parents/charts/transports "
                "with half-open ownership to prove each full fibre covered "
                "or excluded",
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "runtime_filesystem_writes": 0,
            "output_path_option_exists": False,
            "local_signature_assignment_is_not_global_disposition": True,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator": 224580,
            "D02": "UNCHANGED_BLOCKED",
            "global_Gate5_fields": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
        },
    }
    probe_result_sha256 = digest(probe_result)
    require(
        probe_result_sha256 == EXPECTED_PROBE_RESULT_SHA256,
        "probe result digest pin",
    )
    document = {
        "schema": SCHEMA,
        "probe_result": probe_result,
        "probe_result_sha256": probe_result_sha256,
    }
    output = (
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    require(
        hashlib.sha256(output.encode()).hexdigest()
        == EXPECTED_DOCUMENT_SHA256,
        "probe JSON byte digest pin",
    )
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
