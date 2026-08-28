#!/usr/bin/env python3
"""Formal outgoing-W direct local-signature materialization.

This producer materializes strict open 3D local signature rows only.
Lower-dimensional ownership and global exact-key disposition stay at zero.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gc
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any

from flint import ctx, __version__ as FLINT_VERSION


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round208_source_g_outgoing_direct_signature_materialization"
    "_certificate.json"
)
SCHEMA = (
    "cm2.round208.source-g-outgoing-direct-signature-materialization.v1"
)
STATUS = (
    "CERTIFIED_LOCAL_SOURCE_G_OUTGOING_W_DIRECT_SIGNATURE_ROWS__"
    "NO_LOWER_DIMENSIONAL_OR_GLOBAL_EXACT_KEY_DISPOSITION"
)
MAX_INPUT_BYTES = 400 * 1024 * 1024

R207_SOURCE = (
    "cm2_round207_source_g_whole_region_direct_signature_probe.py"
)
R207_REPORT = (
    "cm2_round207_source_g_whole_region_direct_signature_spike_report.md"
)
R207_SOURCE_SHA256 = (
    "0262235b43d74084c37b742b8b4fc435b82e752663d5f816e092faf14e64404a"
)
R207_REPORT_SHA256 = (
    "27b75a8848787fc60b9cd7d0ee57c20ffb96eb4687711adc93597e929f7e90ea"
)
R207_RESULT_SHA256 = (
    "d49b3c9cef0738a03bca8f6477121c7b27aa63e3be8b9ac5854c2521f97448ce"
)
R207_DOCUMENT_SHA256 = (
    "21b388fbd147219f5f52fbdcbe8528b7b9afc06590f2bb997e70042a759f5277"
)

R182_PREFIX = "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
R182_MANIFEST = f"{R182_PREFIX}_manifest.sha256"
R182_MANIFEST_SHA256 = (
    "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5"
)
R182_RESULT_SHA256 = (
    "e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d"
)
R182_VERIFICATION_RESULT_SHA256 = (
    "61715ef39e232937d821ba1c634181f905454b758abbe98d889c768ddc809797"
)

EXPECTED_LEAVES = 18_324
EXPECTED_CANDIDATES = 36_040
EXPECTED_ORIGINS = 8_268
EXPECTED_PARENTS = 912
EXPECTED_RETAINED_CHILDREN = 11_960
EXPECTED_U2_LEAVES = 88
EXPECTED_U2_ORIGINS = 76
EXPECTED_U2_CANDIDATES = 176
EXPECTED_UNRESOLVED_FACE_INCIDENCES = 18_412
EXPECTED_OUTGOING_VOLUME = Q(861459, 419430400000)
EXPECTED_SOURCE_G_KEY_COUNT = 224_580
EXPECTED_FINAL_FACE_ROWS_SHA256 = (
    "0efb78285bc7836c84860f157ab4ec45593029aa523a95fd62171d307d7a5396"
)
EXPECTED_LEAF_ROWS_SHA256 = (
    "0370fb57e9d2881a8bc2d0e66351a6c551e147d483558c682f051153924f88b5"
)
EXPECTED_U2_ROWS_SHA256 = (
    "12fbc70f82645ae2ad252b4e88587a7841814a03fda1972a0241cd63c45d6ee0"
)
EXPECTED_DIRECT_LEAF_ROWS_SHA256 = (
    "4d541ea5bfc4b9db30e78f994e36177dee7112b4c4057c71d6d6376650e20e9e"
)
EXPECTED_ASSIGNMENT_ROWS_SHA256 = (
    "e46fc7e35f2728e48a81e47cd0266cf25c07ad63e534a9fd5b57cc8b0007bb72"
)
EXPECTED_U2_ASSIGNMENT_ROWS_SHA256 = (
    "de20109df8b913a12627b42340ccdacb88e633a5c96cd56bcdd8bafe410fee53"
)
EXPECTED_FACE_METHODS = {
    "ROUND186_BOTH_FACTORS_STRICT_ZERO_ABSENT": 4,
    "ROUND186_ONE_ACTIVE_FACTOR_STRICT_ZERO_ABSENT": 1_172,
    "ROUND186_ONE_ACTIVE_FACTOR_FULL_GRAPH": 1_104,
    "ROUND188_UNIQUE_TWO_ENDPOINT_FACTOR_CURVE": 15_844,
    "ROUND191_STRICT_MONOTONE_ACTIVE_FACTOR_ABSENT": 32,
    "ROUND191_UNIQUE_TWO_ENDPOINT_STEREOGRAPHIC_FACTOR_CURVE": 256,
}
EXPECTED_LEAF_CLASSES = {
    "CLIPPED_2D_BOUNDARY_1D": 17_308,
    "EMPTY": 608,
    "FULL_2D": 408,
}
EXPECTED_OUTGOING_COUNTS = {
    "E": 9_008,
    "N": 9_012,
    "S": 9_012,
    "W": 9_008,
}


class Round208Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round208Error(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def regular_bytes(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(before.st_nlink == 1, f"hardlink:{path.name}")
    require(0 < before.st_size <= maximum, f"size:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            )
            == (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ),
            f"stable-open:{path.name}",
        )
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            require(total <= maximum, f"bounded-read:{path.name}")
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
            f"stable-read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def pinned_bytes(path: Path, expected: str) -> bytes:
    raw = regular_bytes(path)
    require(
        hashlib.sha256(raw).hexdigest() == expected,
        f"pin:{path.name}",
    )
    return raw


def load_evaluator() -> tuple[Any, dict[str, Any]]:
    """Pin Round207 before import and bind its verified formal base chain."""

    pinned_bytes(HERE / R207_SOURCE, R207_SOURCE_SHA256)
    pinned_bytes(HERE / R207_REPORT, R207_REPORT_SHA256)
    pinned_bytes(HERE / R182_MANIFEST, R182_MANIFEST_SHA256)
    module = importlib.import_module(
        "cm2_round207_source_g_whole_region_direct_signature_probe"
    )
    require(
        Path(module.__file__).resolve() == (HERE / R207_SOURCE).resolve(),
        "Round207 module identity",
    )
    require(
        module.EXPECTED_PROBE_RESULT_SHA256 == R207_RESULT_SHA256
        and module.EXPECTED_DOCUMENT_SHA256 == R207_DOCUMENT_SHA256,
        "Round207 final result/document pins",
    )
    upstream = module.check_inputs()
    require(
        upstream["Round182_manifest_sha256"] == R182_MANIFEST_SHA256
        and upstream["Round182_result_sha256"] == R182_RESULT_SHA256
        and upstream["Round182_verification_result_sha256"]
        == R182_VERIFICATION_RESULT_SHA256,
        "Round182 verified-chain binding",
    )
    return module, upstream


def materialize(
    r207: Any,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    r203 = r207.r203
    r198 = r203.r198
    r195 = r198.r195
    r186 = r195.r191.r189.r188.r186
    r174 = r186.r179.r174

    frozen = r174.load_frozen_inputs()
    registry = r174.rebuild_registry(frozen["gate5"])
    global_census = frozen["r169"][
        "source_G_exact_key_coverage_census"
    ]
    require(
        global_census["candidate_exact_key_envelope_count"]
        == EXPECTED_SOURCE_G_KEY_COUNT
        and global_census[
            "global_geometric_exact_key_disposition_count"
        ] == 0
        and global_census[
            "keys_without_a_global_geometric_disposition_count"
        ] == EXPECTED_SOURCE_G_KEY_COUNT
        and len(registry["pairs"]) == 448
        and len(registry["patterns"]) == 985,
        "rebuilt registry/global source-G census",
    )
    del frozen
    outgoing, collars, source = r195.r191.r189.load_scope()
    del source
    gc.collect()
    require(len(outgoing) == EXPECTED_LEAVES, "outgoing leaf census")
    require(
        sum((Q(row["coordinate_volume"]) for row in outgoing), Q(0))
        == EXPECTED_OUTGOING_VOLUME,
        "outgoing exact volume",
    )

    raw_face_rows: list[dict[str, Any]] = []
    raw_leaf_rows: list[dict[str, Any]] = []
    raw_u2_rows: list[dict[str, Any]] = []
    raw_direct_leaf_rows: list[dict[str, Any]] = []
    raw_assignment_rows: list[dict[str, Any]] = []
    formal_region_rows: list[dict[str, Any]] = []

    for index, raw in enumerate(outgoing, 1):
        collar = collars[raw["occurrence_row_id"]]
        require(
            collar["kind"] == "OUTGOING"
            and collar["target_obstacle"] == "W",
            f"outgoing-W collar:{raw['row_id']}",
        )
        box = r174.atlas.AtlasBox(
            *(Q(value) for value in raw["box"]),
            0,
            raw["row_id"],
        )
        final_faces: dict[str, dict[str, Any]] = {}
        for side, upper, encoded in (
            ("LOWER", False, raw["lower_t_face_status"]),
            ("UPPER", True, raw["upper_t_face_status"]),
        ):
            if encoded == "U":
                face = r195.final_unresolved_face(
                    raw,
                    collar,
                    box,
                    side,
                    upper,
                )
                final_faces[side] = face
                raw_face_rows.append(face)
        lower = (
            r195.side_summary(final_faces["LOWER"])
            if "LOWER" in final_faces
            else r195.decode_round182_face(raw["lower_t_face_status"])
        )
        upper = (
            r195.side_summary(final_faces["UPPER"])
            if "UPPER" in final_faces
            else r195.decode_round182_face(raw["upper_t_face_status"])
        )
        leaf = r195.classify_leaf(raw, collar, box, lower, upper)
        raw_leaf_rows.append(leaf)
        if len(final_faces) == 2:
            raw_u2_rows.append(r195.audit_u2_leaf(
                leaf,
                raw,
                collar,
                box,
                final_faces["LOWER"],
                final_faces["UPPER"],
            ))

        geometry_rows = r198.factor_region_rows(
            leaf,
            raw,
            collar,
            box,
            list(final_faces.values()),
            None,
            set(),
            {},
            None,
        )
        base, reasons = r207.direct_leaf_signature_base(
            collar["chart"],
            box,
            registry,
        )
        target_matches = (
            base is not None
            and base["target_lift"] == collar["owner_target"]
        )
        direct_leaf = {
            "leaf_row_id": leaf["leaf_row_id"],
            "origin_row_id": leaf["origin_row_id"],
            "parent_id": collar["parent_id"],
            "chart": collar["chart"],
            "box": raw["box"],
            "candidate_region_count": len(geometry_rows),
            "direct_base_status": (
                "DIRECT_WHOLE_LEAF_BASE_CERTIFIED"
                if base is not None and target_matches
                else "DIRECT_WHOLE_LEAF_BASE_RESIDUAL"
            ),
            "direct_failure_reasons": reasons,
            "direct_target_lift":
                None if base is None else base["target_lift"],
            "frozen_collar_owner_target_for_posthoc_comparison":
                collar["owner_target"],
            "direct_target_matches_frozen_collar": target_matches,
            "frozen_owner_used_as_direct_target_selection_input": False,
            "direct_signature_base": base,
        }
        raw_direct_leaf_rows.append(direct_leaf)
        require(
            base is not None and target_matches and not reasons,
            f"whole-leaf direct signature base:{leaf['leaf_row_id']}",
        )

        face_ids = sorted(
            face["face_row_id"] for face in final_faces.values()
        )
        for geometry in geometry_rows:
            cell = geometry["outgoing_cell"]
            require(
                (
                    geometry["HPLUS_sign"],
                    geometry["HMINUS_sign"],
                )
                == r203.CELL_SIGNS[cell],
                f"strict factor cell:{geometry['candidate_region_id']}",
            )
            signature = {
                "source_chart": base["source_chart"],
                "target_lift": base["target_lift"],
                "ordered_integer_wall_events":
                    base["ordered_integer_wall_events"],
                "signed_wall_word": base["signed_wall_word"],
                "roof": base["roof"],
                "outgoing_cell": cell,
                "target_chart":
                    f"{base['target_lift'].split('[', 1)[0]}:{cell}",
                "official_key_row": base["official_key_row"],
                "official_key_ordinal": base["official_key_ordinal"],
                "official_key_id": base["official_key_id"],
            }
            require(
                signature["official_key_row"]
                == [
                    signature["source_chart"],
                    signature["target_lift"],
                    signature["signed_wall_word"],
                    signature["roof"],
                ],
                f"official key row:{geometry['candidate_region_id']}",
            )
            raw_assignment_rows.append({
                "candidate_region_id": geometry["candidate_region_id"],
                "leaf_row_id": geometry["leaf_row_id"],
                "origin_row_id": geometry["origin_row_id"],
                "parent_id": collar["parent_id"],
                "leaf_classification":
                    geometry["leaf_classification"],
                "F_sign": geometry["F_sign"],
                "HPLUS_sign": geometry["HPLUS_sign"],
                "HMINUS_sign": geometry["HMINUS_sign"],
                "outgoing_cell": cell,
                "whole_region_outgoing_chart_proof":
                    "STRICT_HPLUS_HMINUS_SIGN_PAIR_ON_R195_REGION",
                "containing_leaf_certifies_target_and_wall_fields": True,
                "frozen_owner_used_as_signature_input": False,
                "resolved_anchor_or_component_used_as_signature_input":
                    False,
                "direct_failure_reasons": [],
                "assignment_status":
                    "DIRECT_WHOLE_REGION_SIGNATURE_CERTIFIED",
                "local_return_signature": signature,
                "formal_signature_row_materialized": False,
                "single_point_evaluation_used": False,
                "global_exact_key_disposition_credit": 0,
            })
            formal_region_rows.append(closed_row({
                "region_row_id": geometry["candidate_region_id"],
                "leaf_row_id": geometry["leaf_row_id"],
                "origin_row_id": geometry["origin_row_id"],
                "parent_id": collar["parent_id"],
                "occurrence_row_id": geometry["occurrence_row_id"],
                "retained_child_row_id":
                    leaf["retained_child_row_id"],
                "Round182_leaf_box": raw["box"],
                "Round182_leaf_coordinate_volume":
                    raw["coordinate_volume"],
                "leaf_classification":
                    geometry["leaf_classification"],
                "incident_final_face_row_ids": face_ids,
                "F_sign": geometry["F_sign"],
                "HPLUS_sign": geometry["HPLUS_sign"],
                "HMINUS_sign": geometry["HMINUS_sign"],
                "outgoing_cell": cell,
                "whole_box_factor_C0":
                    geometry["whole_box_factor_C0"],
                "inactive_factor": geometry["inactive_factor"],
                "strict_open_3D_region_exists": True,
                "whole_region_outgoing_chart_proof":
                    "STRICT_HPLUS_HMINUS_SIGN_PAIR",
                "containing_leaf_direct_target_and_wall_proof_row_id":
                    leaf["leaf_row_id"],
                "local_return_signature": signature,
                "complete_retained_target_count":
                    base["complete_retained_target_count"],
                "target_selected_from_complete_list_without_frozen_owner":
                    True,
                "frozen_owner_posthoc_match": True,
                "target_root_strict_future_nongrazing_below_three": True,
                "wall_endpoint_count_and_order_strict_on_leaf": True,
                "resolved_anchor_used": False,
                "parent_signature_guess_used": False,
                "adjacency_or_component_propagation_used": False,
                "single_point_evaluation_used": False,
                "formal_local_open_3D_signature_credit": 1,
                "lower_dimensional_half_open_owner_credit": 0,
                "whole_original_tube_credit": 0,
                "global_exact_key_disposition_credit": 0,
            }))
        if index % 1000 == 0 or index == EXPECTED_LEAVES:
            print(
                f"Round208 materialization {index}/{EXPECTED_LEAVES}",
                file=sys.stderr,
                flush=True,
            )

    raw_face_rows.sort(key=lambda row: row["face_row_id"])
    raw_leaf_rows.sort(key=lambda row: row["leaf_row_id"])
    raw_u2_rows.sort(key=lambda row: row["leaf_row_id"])
    raw_direct_leaf_rows.sort(key=lambda row: row["leaf_row_id"])
    raw_assignment_rows.sort(key=lambda row: row["candidate_region_id"])
    formal_region_rows.sort(key=lambda row: row["region_row_id"])
    require(
        len(raw_face_rows) == EXPECTED_UNRESOLVED_FACE_INCIDENCES
        and len({row["face_row_id"] for row in raw_face_rows})
        == EXPECTED_UNRESOLVED_FACE_INCIDENCES
        and digest(raw_face_rows) == EXPECTED_FINAL_FACE_ROWS_SHA256,
        "final face exact pin",
    )
    require(
        len(raw_leaf_rows) == EXPECTED_LEAVES
        and len({row["leaf_row_id"] for row in raw_leaf_rows})
        == EXPECTED_LEAVES
        and digest(raw_leaf_rows) == EXPECTED_LEAF_ROWS_SHA256,
        "final leaf exact pin",
    )
    require(
        len(raw_u2_rows) == EXPECTED_U2_LEAVES
        and digest(raw_u2_rows) == EXPECTED_U2_ROWS_SHA256,
        "U|U exact pin",
    )
    require(
        digest(raw_direct_leaf_rows)
        == EXPECTED_DIRECT_LEAF_ROWS_SHA256,
        "direct leaf exact pin",
    )
    require(
        len(raw_assignment_rows) == EXPECTED_CANDIDATES
        and len({
            row["candidate_region_id"] for row in raw_assignment_rows
        }) == EXPECTED_CANDIDATES
        and len({
            row["region_row_id"] for row in formal_region_rows
        }) == EXPECTED_CANDIDATES
        and digest(raw_assignment_rows)
        == EXPECTED_ASSIGNMENT_ROWS_SHA256,
        "direct assignment exact pin",
    )
    u2_leaf_ids = {
        row["leaf_row_id"] for row in raw_u2_rows
    }
    require(
        digest([
            row for row in raw_assignment_rows
            if row["leaf_row_id"] in u2_leaf_ids
        ])
        == EXPECTED_U2_ASSIGNMENT_ROWS_SHA256,
        "U|U assignment exact pin",
    )

    face_rows = [closed_row(row) for row in raw_face_rows]
    leaf_rows = [
        closed_row({
            **row,
            "formal_final_geometry_row_materialized": True,
        })
        for row in raw_leaf_rows
    ]
    u2_rows = [
        closed_row({
            **row,
            "both_strict_sides_formally_signature_materialized": True,
        })
        for row in raw_u2_rows
    ]
    direct_leaf_rows = [
        closed_row({
            **row,
            "formal_direct_signature_base_materialized": True,
            "formal_local_credit": 1,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        for row in raw_direct_leaf_rows
    ]
    return (
        face_rows,
        leaf_rows,
        u2_rows,
        direct_leaf_rows,
        formal_region_rows,
        raw_assignment_rows,
    )


def build_origin_rows(
    leaf_rows: list[dict[str, Any]],
    region_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    leaves: dict[str, list[dict[str, Any]]] = defaultdict(list)
    regions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in leaf_rows:
        leaves[row["origin_row_id"]].append(row)
    for row in region_rows:
        regions[row["origin_row_id"]].append(row)
    output: list[dict[str, Any]] = []
    for origin_id in sorted(leaves):
        origin_leaves = leaves[origin_id]
        origin_regions = regions[origin_id]
        require(
            len({row["parent_id"] for row in origin_regions}) == 1,
            f"origin parent identity:{origin_id}",
        )
        output.append(closed_row({
            "origin_row_id": origin_id,
            "parent_id": origin_regions[0]["parent_id"],
            "leaf_row_count": len(origin_leaves),
            "leaf_row_ids": sorted(
                row["leaf_row_id"] for row in origin_leaves
            ),
            "strict_open_3D_signature_region_count":
                len(origin_regions),
            "strict_open_3D_signature_region_row_ids": sorted(
                row["region_row_id"] for row in origin_regions
            ),
            "exact_outer_coordinate_volume": qstr(sum(
                (Q(row["coordinate_volume"]) for row in origin_leaves),
                Q(0),
            )),
            "leaf_classification_count": dict(sorted(Counter(
                row["final_graph_classification"]
                for row in origin_leaves
            ).items())),
            "distinct_local_signature_count": len({
                digest(row["local_return_signature"])
                for row in origin_regions
            }),
            "all_leaves_have_direct_signature_bases": True,
            "all_strict_open_3D_regions_have_formal_signatures": True,
            "formal_local_open_3D_origin_coverage_credit": 1,
            "lower_dimensional_half_open_ownership_materialized": False,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    require(
        len(output) == EXPECTED_ORIGINS
        and sum(
            (Q(row["exact_outer_coordinate_volume"]) for row in output),
            Q(0),
        ) == EXPECTED_OUTGOING_VOLUME
        and all(
            row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            for row in output
        ),
        "origin local completion",
    )
    return output


def build_key_rows(
    region_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in region_rows:
        grouped[row["local_return_signature"]["official_key_id"]].append(row)
    output: list[dict[str, Any]] = []
    for key_id, rows in grouped.items():
        signature = rows[0]["local_return_signature"]
        require(
            all(
                row["local_return_signature"]["official_key_id"] == key_id
                and row["local_return_signature"]["official_key_ordinal"]
                == signature["official_key_ordinal"]
                and row["local_return_signature"]["official_key_row"]
                == signature["official_key_row"]
                for row in rows
            ),
            f"local exact-key join:{key_id}",
        )
        output.append(closed_row({
            "official_key_id": key_id,
            "official_key_ordinal":
                signature["official_key_ordinal"],
            "official_key_row": signature["official_key_row"],
            "local_region_occurrence_count": len(rows),
            "local_region_row_ids": sorted(
                row["region_row_id"] for row in rows
            ),
            "join_cardinality_per_local_region": 1,
            "formal_local_join_materialized": True,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }))
    output.sort(key=lambda row: row["official_key_ordinal"])
    require(
        len(output) == 24
        and sum(
            row["local_region_occurrence_count"] for row in output
        ) == EXPECTED_CANDIDATES
        and all(
            row["global_exact_key_disposition_credit"] == 0
            for row in output
        ),
        "24 local exact-key joins",
    )
    return output


def build_result(producer_sha256: str) -> dict[str, Any]:
    ctx.prec = 256
    print("Round208 pinning evaluator chain", file=sys.stderr, flush=True)
    r207, upstream = load_evaluator()
    print("Round208 rebuilding all formal rows", file=sys.stderr, flush=True)
    (
        face_rows,
        leaf_rows,
        u2_rows,
        direct_leaf_rows,
        region_rows,
        raw_assignment_rows,
    ) = materialize(r207)
    origin_rows = build_origin_rows(leaf_rows, region_rows)
    key_rows = build_key_rows(region_rows)

    parent_ids = {row["parent_id"] for row in region_rows}
    retained_ids = {
        row["retained_child_row_id"] for row in region_rows
    }
    u2_leaf_ids = {row["leaf_row_id"] for row in u2_rows}
    u2_region_rows = [
        row for row in region_rows if row["leaf_row_id"] in u2_leaf_ids
    ]
    signatures = [
        row["local_return_signature"] for row in region_rows
    ]
    signature_digests = sorted({digest(row) for row in signatures})
    exact_key_ids = sorted({
        row["official_key_id"] for row in signatures
    })
    exact_key_ordinals = sorted({
        row["official_key_ordinal"] for row in signatures
    })
    face_methods = Counter(
        row["final_method"] for row in face_rows
    )
    leaf_classes = Counter(
        row["final_graph_classification"] for row in leaf_rows
    )
    outgoing_counts = Counter(
        row["outgoing_cell"] for row in region_rows
    )
    word_lengths = Counter(
        len(row["signed_wall_word"]) for row in signatures
    )
    complete_target_counts = Counter(
        row["direct_signature_base"]["complete_retained_target_count"]
        for row in direct_leaf_rows
    )
    require(
        len(parent_ids) == EXPECTED_PARENTS
        and len(retained_ids) == EXPECTED_RETAINED_CHILDREN
        and len(u2_region_rows) == EXPECTED_U2_CANDIDATES
        and len({row["origin_row_id"] for row in u2_rows})
        == EXPECTED_U2_ORIGINS
        and dict(sorted(face_methods.items())) == EXPECTED_FACE_METHODS
        and dict(sorted(leaf_classes.items())) == EXPECTED_LEAF_CLASSES
        and dict(sorted(outgoing_counts.items())) == EXPECTED_OUTGOING_COUNTS
        and word_lengths == {0: 30_080, 1: 5_960}
        and complete_target_counts == {57: EXPECTED_LEAVES}
        and all(
            row["direct_base_status"]
            == "DIRECT_WHOLE_LEAF_BASE_CERTIFIED"
            and row["direct_target_matches_frozen_collar"] is True
            and row["direct_failure_reasons"] == []
            for row in direct_leaf_rows
        )
        and len(signature_digests) == 52
        and len(exact_key_ids) == len(exact_key_ordinals) == 24,
        "formal census pins",
    )

    return {
        "status": STATUS,
        "formal_input_binding": {
            "Round182_manifest_sha256": R182_MANIFEST_SHA256,
            "Round182_result_sha256": R182_RESULT_SHA256,
            "Round182_verification_result_sha256":
                R182_VERIFICATION_RESULT_SHA256,
            "Round207_source_sha256": R207_SOURCE_SHA256,
            "Round207_report_sha256": R207_REPORT_SHA256,
            "Round207_probe_result_sha256": R207_RESULT_SHA256,
            "Round207_probe_document_sha256": R207_DOCUMENT_SHA256,
            "Round207_used_as_producer_side_evaluator": True,
            "independent_verifier_must_not_import_Round207": True,
            "upstream_chain": upstream,
        },
        "formal_scope_contract": {
            "source_obstacle": "G",
            "target_obstacle": "W",
            "Round182_outgoing_residual_leaf_count": EXPECTED_LEAVES,
            "outgoing_origin_count": EXPECTED_ORIGINS,
            "parent_count": len(parent_ids),
            "retained_child_count": len(retained_ids),
            "exact_outer_coordinate_volume": qstr(
                EXPECTED_OUTGOING_VOLUME
            ),
            "strict_open_3D_candidate_region_count":
                EXPECTED_CANDIDATES,
            "formal_local_open_3D_signature_row_count":
                len(region_rows),
            "all_local_open_3D_signature_rows_materialized": True,
            "lower_dimensional_half_open_ownership_materialized": False,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "formal_final_factor_face_ledger": {
            "row_count": len(face_rows),
            "rows_sha256": digest(face_rows),
            "rows": face_rows,
            "method_count": dict(sorted(face_methods.items())),
            "raw_Round195_rows_sha256":
                EXPECTED_FINAL_FACE_ROWS_SHA256,
            "all_target_normal_zeros_excluded": True,
            "local_face_residual_count": 0,
        },
        "formal_leaf_geometry_ledger": {
            "row_count": len(leaf_rows),
            "rows_sha256": digest(leaf_rows),
            "rows": leaf_rows,
            "classification_count": dict(sorted(leaf_classes.items())),
            "raw_Round195_rows_sha256": EXPECTED_LEAF_ROWS_SHA256,
            "strict_open_3D_candidate_region_count":
                EXPECTED_CANDIDATES,
            "local_geometric_residual_leaf_count": 0,
        },
        "formal_direct_leaf_signature_base_ledger": {
            "row_count": len(direct_leaf_rows),
            "rows_sha256": digest(direct_leaf_rows),
            "rows": direct_leaf_rows,
            "raw_Round207_rows_sha256":
                EXPECTED_DIRECT_LEAF_ROWS_SHA256,
            "complete_target_list_size_histogram":
                {
                    str(key): value
                    for key, value in sorted(
                        complete_target_counts.items()
                    )
                },
            "all_direct_targets_match_frozen_collars_posthoc": True,
            "all_target_and_wall_fields_strict_on_whole_leaf": True,
            "direct_residual_count": 0,
        },
        "formal_local_open_3D_signature_ledger": {
            "row_count": len(region_rows),
            "rows_sha256": digest(region_rows),
            "rows": region_rows,
            "raw_Round207_assignment_rows_sha256":
                digest(raw_assignment_rows),
            "distinct_local_signature_count":
                len(signature_digests),
            "distinct_local_signature_digests_sha256":
                digest(signature_digests),
            "involved_exact_key_count": len(exact_key_ids),
            "involved_exact_key_ids_sha256": digest(exact_key_ids),
            "involved_exact_key_ordinals_sha256":
                digest(exact_key_ordinals),
            "signed_wall_word_length_count":
                dict(sorted(word_lengths.items())),
            "outgoing_cell_count":
                dict(sorted(outgoing_counts.items())),
            "formal_local_open_3D_signature_credit":
                len(region_rows),
            "lower_dimensional_half_open_owner_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "formal_U_pipe_U_side_specific_ledger": {
            "leaf_row_count": len(u2_rows),
            "rows_sha256": digest(u2_rows),
            "rows": u2_rows,
            "raw_Round195_rows_sha256": EXPECTED_U2_ROWS_SHA256,
            "side_specific_region_row_count": len(u2_region_rows),
            "side_specific_region_rows_sha256":
                digest(u2_region_rows),
            "raw_Round207_assignment_rows_sha256":
                EXPECTED_U2_ASSIGNMENT_ROWS_SHA256,
            "both_sides_formally_materialized_leaf_count":
                EXPECTED_U2_LEAVES,
            "cross_t_signature_copy_used": False,
        },
        "formal_origin_local_completion_ledger": {
            "row_count": len(origin_rows),
            "rows_sha256": digest(origin_rows),
            "rows": origin_rows,
            "formal_local_open_3D_origin_coverage_credit":
                len(origin_rows),
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "formal_exact_key_local_join_ledger": {
            "row_count": len(key_rows),
            "rows_sha256": digest(key_rows),
            "rows": key_rows,
            "all_local_regions_join_exactly_one_immutable_key": True,
            "no_global_exact_key_fibre_exhausted": True,
            "global_source_G_exact_key_fibre_count":
                EXPECTED_SOURCE_G_KEY_COUNT,
            "global_source_G_exact_key_disposition_count": 0,
        },
        "exact_dimension_and_volume_conservation": {
            "input_leaf_count": EXPECTED_LEAVES,
            "input_exact_outer_coordinate_volume":
                qstr(EXPECTED_OUTGOING_VOLUME),
            "formal_output_leaf_cover_count": EXPECTED_LEAVES,
            "formal_output_exact_outer_coordinate_volume":
                qstr(EXPECTED_OUTGOING_VOLUME),
            "strict_open_3D_region_count": EXPECTED_CANDIDATES,
            "individual_curved_region_volumes_not_summed": True,
            "each_leaf_outer_volume_counted_exactly_once": True,
            "2D_1D_0D_strata_have_zero_ambient_3D_volume": True,
            "integer_leaf_delta": 0,
            "exact_coordinate_volume_delta": "0",
        },
        "method_independence_contract": {
            "complete_target_list_recomputed_per_leaf": True,
            "frozen_owner_used_only_posthoc": True,
            "resolved_signature_anchor_used": False,
            "parent_signature_base_used": False,
            "Round198_adjacency_assignment_used": False,
            "Round203_component_assignment_used": False,
            "single_point_evaluation_used": False,
            "target_and_wall_fields_certified_on_containing_leaf": True,
            "outgoing_chart_certified_on_each_strict_region": True,
        },
        "formal_local_materialization_and_strict_nonpromotion": {
            "formal_local_open_3D_signature_count":
                EXPECTED_CANDIDATES,
            "formal_local_open_3D_origin_coverage_count":
                EXPECTED_ORIGINS,
            "separate_wall_G_local_replacement_is_out_of_scope": True,
            "lower_dimensional_half_open_ownership": "NOT_MATERIALIZED",
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions":
                f"0/{EXPECTED_SOURCE_G_KEY_COUNT}",
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate":
            "independently verify every row, join with the separately "
            "formalized wall-G local replacement, then materialize all "
            "lower-dimensional half-open owners before any complete "
            "global exact-key fibre coverage/exclusion claim",
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_flint_version": FLINT_VERSION,
            "effective_Arb_precision_bits": ctx.prec,
            "producer_side_evaluator":
                "pinned Round207 probe chain rooted in verified Round182",
            "formal_upstream_files_modified": False,
        },
    }


def validate_output(path: Path) -> Path:
    require(
        not any(part == ".." for part in path.parts),
        "output parent alias",
    )
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        "output exact directory",
    )
    allowed = (
        absolute.name == OUTPUT.name
        or (
            absolute.name.startswith(".cm2_round208_")
            and absolute.name.endswith("_certificate.json")
        )
    )
    require(allowed, "output allowlist")
    protected = {
        Path(__file__).resolve(),
        (HERE / R207_SOURCE).resolve(),
        (HERE / R207_REPORT).resolve(),
        (HERE / R182_MANIFEST).resolve(),
    }
    require(
        absolute.resolve(strict=False) not in protected,
        "protected output",
    )
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "output type",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    absolute = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{absolute.name}.",
        suffix=".tmp",
        dir=absolute.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, absolute)
        directory_descriptor = os.open(
            os.fspath(absolute.parent),
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    producer_sha256 = hashlib.sha256(
        regular_bytes(Path(__file__), 5_000_000)
    ).hexdigest()
    result = build_result(producer_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical_bytes(envelope) + b"\n")
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
