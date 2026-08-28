#!/usr/bin/env python3
"""Independent verifier for Round172 frozen-owner absence pruning.

The Round172 producer is byte-pinned but never imported or executed.  This
verifier independently rebuilds the source-W atlas at 192-bit precision,
reconstructs all 32 tangency parents and the exact 12/10/2/20 partition,
replays both Round164 live regressions, and compares the full certificate to
an independently constructed expected document.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from typing import Any, Callable

import flint
import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas


HERE = Path(__file__).resolve().parent
PRODUCER = (
    HERE
    / (
        "cm2_round172_dimension_safe_tangency_parent_"
        "frozen_owner_absence_pruning.py"
    )
)
CERTIFICATE = (
    HERE
    / (
        "cm2_round172_dimension_safe_tangency_parent_"
        "frozen_owner_absence_pruning_certificate.json"
    )
)
OUTPUT = (
    HERE
    / (
        "cm2_round172_dimension_safe_tangency_parent_"
        "frozen_owner_absence_pruning_verification.json"
    )
)
CERTIFICATE_SCHEMA = (
    "cm2.round172.dimension-safe-tangency-parent-"
    "frozen-owner-absence-pruning.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round172.dimension-safe-tangency-parent-"
    "frozen-owner-absence-pruning.verification.v1"
)
MAX_INPUT_BYTES = 8 * 1024 * 1024
FROZEN_OWNER = "W[1,0]"
FROZEN_OUTGOING_CHART = "W"
CHARTS = ("W:E", "W:N", "W:S")

ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
BASE_SOURCE = "cm2_gate3_candidate_first_hit_cert.py"
GE_SOURCE = "cm2_gate3_ge_interval_atlas_cert.py"
R164_CERT = "cm2_round164_tangency_strata_pruning_certificate.json"
R164_VER = "cm2_round164_tangency_strata_pruning_verification.json"
R164_VERIFIER = "cm2_round164_tangency_strata_pruning_verifier.py"
R168_CERT = (
    "cm2_round168_dimension_safe_source_W_stage_one_ledger_certificate.json"
)
R168_VER = (
    "cm2_round168_dimension_safe_source_W_stage_one_ledger_verification.json"
)
R168_VERIFIER = (
    "cm2_round168_dimension_safe_source_W_stage_one_ledger_verifier.py"
)

PINS: dict[str, str] = {
    ATLAS_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    BASE_SOURCE:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    GE_SOURCE:
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    R164_CERT:
        "2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092",
    R164_VER:
        "850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0",
    R164_VERIFIER:
        "67da9c414d0bf37574696c851c45476e8ae5f695f3af6c21b3a7718b19822dbc",
    R168_CERT:
        "adbdcc3ffbd791126dd759a5699bf65902ebb8529b173db52e4b45e5f299494e",
    R168_VER:
        "994037b25d321e731e4cf4b61c92610fa99fadfccfa2d15ce2a38ccbe20a5cc9",
    R168_VERIFIER:
        "087134652c7950ce2956557dc5be6b6255b38d69bc04c2498a9b36b09d08b17d",
}

EXPECTED_PRODUCER_SHA256 = (
    "81f147cf6106d7436df282de106fc47e793e8f97a43282b35719e28182e07980"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "3185188c476a64d3e732674fa724ce9a49afe84c61abab448f746a5a3555b66c"
)
EXPECTED_CERTIFICATE_RESULT_SHA256 = (
    "a436b4a82b1e8d5c617fe576e0e4e76b6f6f38ad8ac3eda4ddde544c2769a776"
)
R164_RESULT = "0f6d7f47ac20734ed294dd04cd7720ccbb9c0a1d4236980f814dd2ea2d5e79d9"
R164_VER_RESULT = "bb2e51bdbbd457a5782038efc527000cbf89b73c8645fd6facd126fa453af8c4"
R168_RESULT = "1544a7b865df882bab92dbec333e723fea28dd382567945e09ad609e7a811201"
R168_VER_RESULT = "07f9bcc6fd42f5439322e1090b281a3f0780c3a706bb19ceeb9f51b666280031"

EXPECTED_ABSENT_KEYS = (
    "W:E:00.14.11111",
    "W:E:00.15.0011101",
    "W:E:07.00.1100010",
    "W:E:07.01.00000",
    "W:N:00.00.0110111",
    "W:N:02.15.11011001",
    "W:N:07.15.1001000",
    "W:S:H.00.00.0110111",
    "W:S:H.02.15.11011001",
    "W:S:H.07.15.1001000",
)
EXPECTED_EXCEPTION_KEYS = (
    "W:N:05.00.00100110",
    "W:S:H.05.00.00100110",
)

REPLAY_CANDIDATE_IDS = {
    chart_id: tuple(base.candidate_ids(chart_id))
    for chart_id in CHARTS
}
REPLAY_TARGETS = {
    target.target_id: target for target in base.TARGETS
}


class VerificationError(RuntimeError):
    """Fail-closed independent verification error."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_noninteger_number(value: str) -> None:
    raise VerificationError(f"non-integer JSON number:{value}")


def validate_json_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(type(key) is str and "\x00" not in key, f"JSON key:{path}")
            require(
                not any(0xD800 <= ord(char) <= 0xDFFF for char in key),
                f"surrogate key:{path}",
            )
            validate_json_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_json_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require("\x00" not in value, f"NUL string:{path}")
        require(
            not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            f"surrogate string:{path}",
        )


def read_regular(path: Path, expected_sha256: str | None = None) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"not regular:{path.name}")
    require(not path.is_symlink(), f"symlink rejected:{path.name}")
    require(st.st_nlink == 1, f"multiply linked rejected:{path.name}")
    require(st.st_size <= MAX_INPUT_BYTES, f"oversized:{path.name}")
    data = path.read_bytes()
    if expected_sha256 is not None:
        require(sha256_bytes(data) == expected_sha256, f"pin:{path.name}")
    return data


def parse_envelope(
    data: bytes,
    *,
    label: str,
    expected_schema: str | None = None,
    require_canonical: bool,
) -> dict[str, Any]:
    require(not data.startswith(b"\xef\xbb\xbf"), f"BOM:{label}")
    require(b"\x00" not in data, f"raw NUL:{label}")
    try:
        value = json.loads(
            data.decode("utf-8", "strict"),
            object_pairs_hook=reject_duplicate_keys,
            parse_float=reject_noninteger_number,
            parse_constant=reject_noninteger_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"invalid JSON:{label}:{exc}") from exc
    validate_json_tree(value)
    require(type(value) is dict, f"top object:{label}")
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"envelope keys:{label}",
    )
    if expected_schema is not None:
        require(value["schema"] == expected_schema, f"schema:{label}")
    require(
        value["result_sha256"] == digest(value["result"]),
        f"result digest:{label}",
    )
    if require_canonical:
        require(
            data == canonical_bytes(value) + b"\n",
            f"canonical single-newline bytes:{label}",
        )
    return value


def load_pinned(name: str) -> dict[str, Any]:
    return parse_envelope(
        read_regular(HERE / name, PINS[name]),
        label=name,
        require_canonical=False,
    )


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def independently_validate_chain(
    docs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    require(
        Path(atlas.__file__).resolve() == (HERE / ATLAS_SOURCE).resolve(),
        "atlas module identity",
    )
    require(
        Path(base.__file__).resolve() == (HERE / BASE_SOURCE).resolve(),
        "base module identity",
    )
    require(
        Path(atlas.ge.__file__).resolve() == (HERE / GE_SOURCE).resolve(),
        "GE atlas module identity",
    )
    require(
        flint.__version__ == "0.9.0" and atlas.ctx.prec == 192,
        "192-bit python-flint environment",
    )
    r164 = docs[R164_CERT]
    v164 = docs[R164_VER]
    require(
        r164["schema"]
        == "cm2.round164.dimension-safe-tangency-graph-typing.v2"
        and r164["result_sha256"] == R164_RESULT,
        "Round164 certificate",
    )
    v164r = v164["result"]
    require(
        v164["schema"]
        == "cm2.round164.dimension-safe-tangency-graph-typing.verification.v2"
        and v164["result_sha256"] == R164_VER_RESULT
        and v164r["status"] == "PASS"
        and v164r["certificate_result_sha256"] == R164_RESULT
        and v164r["round164_producer_imported_or_executed"] is False,
        "Round164 verification chain",
    )
    for key in (
        "all_32_tangency_graphs_reconstructed",
        "all_graph_disposition_rows_recomputed",
        "both_live_off_graph_regressions_replayed",
        "full_document_exactly_matched",
    ):
        require(v164r[key] is True, f"Round164 verification:{key}")
    require(
        v164r["semantic_attack_suite"]["all_rejected"] is True
        and v164r["strict_json_attack_suite"]["all_rejected"] is True,
        "Round164 attacks",
    )
    tangency = r164["result"]["tangency_graph_typing"]
    require(
        tangency["ambient_parent_leaf_count"] == 32
        and tangency["typed_codimension_one_graph_count"] == 32
        and tangency["prefix_mismatch_graph_count"] == 12
        and tangency["frozen_owner_graph_count"] == 20
        and tangency["new_full_dimensional_parent_leaf_exclusion_count"] == 0
        and tangency["remaining_off_graph_ambient_parent_count"] == 32
        and tangency["ambient_parameter_dimension"] == 3
        and tangency["typed_graph_dimension"] == 2
        and tangency[
            "D_negative_D_zero_D_positive_partition_materialized"
        ] is False
        and tangency["all_physical_first_tangency_graphs_replayed"] is True
        and tangency["all_rows_sha256"] == digest(tangency["rows"])
        and len(tangency["rows"]) == 32,
        "Round164 tangency census",
    )
    correction = r164["result"]["v1_correction"]
    require(
        correction["live_off_graph_regression_count"] == 2
        and correction["all_live_off_graph_regressions_sha256"]
        == digest(correction["live_off_graph_regressions"])
        and {
            row["ambient_leaf_key"]
            for row in correction["live_off_graph_regressions"]
        } == set(EXPECTED_EXCEPTION_KEYS),
        "Round164 regressions",
    )

    r168 = docs[R168_CERT]
    v168 = docs[R168_VER]
    require(
        r168["schema"]
        == "cm2.round168.dimension-safe-source-W-stage-one-ledger.v1"
        and r168["result_sha256"] == R168_RESULT,
        "Round168 certificate",
    )
    v168r = v168["result"]
    require(
        v168["schema"]
        == (
            "cm2.round168.dimension-safe-source-W-stage-one-ledger."
            "verification.v1"
        )
        and v168["result_sha256"] == R168_VER_RESULT
        and v168r["status"] == "PASS"
        and v168r["certificate_result_sha256"] == R168_RESULT,
        "Round168 verification chain",
    )
    independence = v168r["independence_contract"]
    require(
        independence["full_result_independently_reconstructed"] is True
        and independence["full_expected_canonical_equality"] is True
        and independence["recursive_exact_key_tree_matched"] is True,
        "Round168 independent reconstruction",
    )
    require(
        v168r["semantic_mutation_attack_suite"]["all_rejected"] is True
        and v168r["strict_json_attack_suite"]["all_rejected"] is True
        and v168r["path_safety_attack_suite"]["all_rejected"] is True,
        "Round168 attacks",
    )
    ledger = r168["result"]
    require(
        ledger["record_space"]["refined_source_W_record_count"] == 76832
        and ledger["admitted_whole_record_credit"][
            "combined_whole_record_excluded"
        ] == 73162
        and ledger["conservative_live_ledger"][
            "conservative_live_total"
        ] == 3670
        and ledger["conservative_live_ledger"]["original_stage_one_match"]
        == 518
        and ledger["conservative_live_ledger"][
            "Round165_seam_live_composites"
        ] == 504
        and ledger["conservative_live_ledger"]["tangency_ambient_bulk"] == 32
        and ledger["conservative_live_ledger"]["owner_active_multi"] == 2616
        and ledger["dimension_safe_noncredit"][
            "Round164_typed_tangency_graph_whole_parent_credit"
        ] == 0
        and ledger["dimension_safe_noncredit"][
            "Round166_deep_refinement_profile_whole_record_credit"
        ] == 0
        and ledger["conservation"]["identity"] == "73162+3670=76832"
        and ledger["strict_nonpromotion"]["D02"] == "BLOCKED"
        and ledger["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round168 ledger",
    )
    return r164


def independently_replay_records(
    chart_id: str,
    box: atlas.AtlasBox,
) -> list[atlas.RootRecord]:
    qx, qy, ux, uy, s, _radial = atlas.geometry(chart_id, box)
    result: list[atlas.RootRecord] = []
    for target_id in REPLAY_CANDIDATE_IDS[chart_id]:
        target = REPLAY_TARGETS[target_id]
        center_x, center_y = base.target_center(target, s)
        dx, dy = center_x - qx, center_y - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = base.arbq(base.RADIUS[target.obstacle])
        discriminant = radius * radius - transverse * transverse
        if bool(discriminant < 0):
            result.append(atlas.RootRecord(
                target_id,
                "no_real_intersection",
                ell,
                discriminant,
                None,
                None,
                transverse,
            ))
            continue
        if not bool(discriminant > 0):
            result.append(atlas.RootRecord(
                target_id,
                "unresolved_discriminant",
                ell,
                discriminant,
                None,
                None,
                transverse,
            ))
            continue
        radical = discriminant.sqrt()
        near = ell - radical
        far = ell + radical
        if bool(far < 0):
            classification = "intersection_behind"
        elif bool(near > 0):
            classification = "strict_future_root"
        else:
            classification = "unresolved_root_sign"
        result.append(atlas.RootRecord(
            target_id,
            classification,
            ell,
            discriminant,
            near,
            far,
            transverse,
        ))
    return result


def independently_build_atlases() -> dict[str, list[atlas.Leaf]]:
    original_records = atlas.records
    atlas.records = independently_replay_records
    try:
        east = atlas.build_atlas("W:E")
        north = atlas.build_atlas("W:N")
    finally:
        atlas.records = original_records
    return {
        "W:E": east,
        "W:N": north,
        "W:S": [
            atlas.reflect_leaf("W:N", "horizontal", leaf)
            for leaf in north
        ],
    }


def independently_classify_outgoing(
    chart_id: str,
    point: atlas.AtlasBox,
) -> tuple[str, Any, Any]:
    frozen = next(
        record for record in independently_replay_records(chart_id, point)
        if record.target_id == FROZEN_OWNER
    )
    require(
        frozen.classification == "strict_future_root"
        and frozen.near is not None,
        "regression strict future",
    )
    qx, qy, ux, uy, s, _radial = atlas.geometry(chart_id, point)
    target = REPLAY_TARGETS[FROZEN_OWNER]
    center_x, center_y = base.target_center(target, s)
    radius = base.arbq(base.RADIUS[target.obstacle])
    nx = (qx + frozen.near * ux - center_x) / radius
    ny = (qy + frozen.near * uy - center_y) / radius
    margins = {
        "E": (nx - ny, nx + ny),
        "W": (-nx - ny, -nx + ny),
        "N": (ny - nx, ny + nx),
        "S": (-ny - nx, -ny + nx),
    }
    for cell in ("E", "W", "N", "S"):
        first, second = margins[cell]
        if bool(first > 0) and bool(second > 0):
            return cell, first, second
    raise VerificationError("regression outgoing unresolved")


def independently_replay_regression(
    chart_id: str,
    leaf: atlas.Leaf,
    tangency_target: str,
    upstream: dict[str, Any],
) -> dict[str, Any]:
    point_data = upstream["strict_interior_point"]
    t = Q(point_data["t"])
    p = Q(point_data["p"])
    s = Q(point_data["s"])
    box = leaf.box
    require(
        box.t0 < t < box.t1
        and box.p0 < p < box.p1
        and box.s0 < s < box.s1,
        "strict regression interior",
    )
    point = atlas.AtlasBox(
        t,
        t,
        p,
        p,
        s,
        s,
        box.depth,
        box.path + ".round172-regression",
    )
    original_records = atlas.records
    atlas.records = independently_replay_records
    try:
        classification = atlas.classify_box(chart_id, point)
    finally:
        atlas.records = original_records
    require(
        classification.classification == "unique_first"
        and classification.owner_target == FROZEN_OWNER,
        "regression unique first",
    )
    tangency_record = next(
        record for record in independently_replay_records(chart_id, point)
        if record.target_id == tangency_target
    )
    require(
        tangency_record.classification == "no_real_intersection"
        and bool(tangency_record.discriminant < 0),
        "regression off mismatch graph",
    )
    outgoing, first, second = independently_classify_outgoing(chart_id, point)
    require(
        outgoing == FROZEN_OUTGOING_CHART
        and bool(first > 0)
        and bool(second > 0),
        "regression outgoing W",
    )
    require(
        upstream["tangency_target"] == tangency_target
        and upstream["point_first_hit_classification"] == "unique_first"
        and upstream["point_first_owner"] == FROZEN_OWNER
        and upstream["point_outgoing_chart"] == FROZEN_OUTGOING_CHART
        and upstream[
            "proves_ambient_leaf_cannot_be_pruned_from_graph_only"
        ] is True,
        "upstream regression binding",
    )
    return {
        "Round164_regression_row_sha256": digest(upstream),
        "strict_interior_point": copy.deepcopy(point_data),
        "independently_replayed_at_192_bits": True,
        "point_first_hit_classification": "unique_first",
        "point_first_owner": FROZEN_OWNER,
        "point_outgoing_chart": outgoing,
        "mismatch_tangency_target": tangency_target,
        "mismatch_tangency_target_point_classification":
            "no_real_intersection",
        "mismatch_tangency_target_discriminant_sign": "STRICT_NEGATIVE",
        "outgoing_margin_one_sign": "STRICT_POSITIVE",
        "outgoing_margin_two_sign": "STRICT_POSITIVE",
        "proves_exception_parent_must_remain_live": True,
    }


def independently_reconstruct_rows(
    r164: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    atlases = independently_build_atlases()
    upstream_rows = {
        row["ambient_leaf_key"]: row
        for row in r164["result"]["tangency_graph_typing"]["rows"]
    }
    upstream_regressions = {
        row["ambient_leaf_key"]: row
        for row in r164["result"]["v1_correction"][
            "live_off_graph_regressions"
        ]
    }
    leaves = [
        (chart_id, leaf)
        for chart_id, chart_leaves in atlases.items()
        for leaf in chart_leaves
        if leaf.classification == "tangency_graph"
    ]
    require(len(leaves) == 32, "32 independent tangency leaves")
    rows: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []
    for chart_id, leaf in leaves:
        key = f"{chart_id}:{leaf.box.path}"
        require(key in upstream_rows, f"Round164 row:{key}")
        require(len(leaf.tangency_targets) == 1, f"unique graph:{key}")
        tangency_target = leaf.tangency_targets[0]
        records = independently_replay_records(chart_id, leaf.box)
        tangency_record = next(
            record for record in records
            if record.target_id == tangency_target
        )
        require(
            atlas.physical_tangency_graph(
                chart_id,
                leaf.box,
                tangency_record,
                records,
            ),
            f"physical graph:{key}",
        )
        upstream = upstream_rows[key]
        require(
            upstream["tangency_target"] == tangency_target
            and upstream["ambient_parameter_dimension"] == 3
            and upstream["typed_graph_dimension"] == 2
            and upstream["ambient_leaf_bulk_disposition"]
            == "UNRESOLVED_OFF_GRAPH_BULK",
            f"Round164 row semantics:{key}",
        )
        frozen = next(
            record for record in records
            if record.target_id == FROZEN_OWNER
        )
        owner_is_graph = tangency_target == FROZEN_OWNER
        binding: dict[str, Any] | None = None
        if owner_is_graph:
            require(
                upstream["graph_disposition"]
                == "TYPED_FROZEN_OWNER_TANGENCY_GRAPH"
                and frozen.classification == "unresolved_discriminant",
                f"owner graph:{key}",
            )
            resolution = "LIVE_FROZEN_OWNER_TANGENCY_COMPOSITE"
            discriminant_sign = "UNRESOLVED_ACROSS_TYPED_GRAPH"
            excluded = False
        elif (
            frozen.classification == "no_real_intersection"
            and bool(frozen.discriminant < 0)
        ):
            require(
                upstream["graph_disposition"]
                == "TYPED_PREFIX_MISMATCH_TANGENCY_GRAPH",
                f"mismatch absence:{key}",
            )
            resolution = "EXCLUDED_FROZEN_OWNER_ABSENT_ON_WHOLE_PARENT"
            discriminant_sign = "STRICT_NEGATIVE"
            excluded = True
        else:
            require(
                upstream["graph_disposition"]
                == "TYPED_PREFIX_MISMATCH_TANGENCY_GRAPH"
                and key in EXPECTED_EXCEPTION_KEYS
                and frozen.classification == "strict_future_root"
                and bool(frozen.discriminant > 0)
                and frozen.near is not None
                and bool(frozen.near > 0),
                f"strict future exception:{key}",
            )
            resolution = "LIVE_PREFIX_MISMATCH_STRICT_FUTURE_EXCEPTION"
            discriminant_sign = "STRICT_POSITIVE"
            excluded = False
            binding = independently_replay_regression(
                chart_id,
                leaf,
                tangency_target,
                upstream_regressions[key],
            )
            bindings.append(closed_row({
                "ambient_leaf_key": key,
                **binding,
            }))
        rows.append(closed_row({
            "ambient_leaf_key": key,
            "chart_id": chart_id,
            "atlas_path": leaf.box.path,
            "ambient_parameter_dimension": 3,
            "Round164_tangency_target": tangency_target,
            "Round164_graph_disposition": upstream["graph_disposition"],
            "Round164_graph_dimension": 2,
            "frozen_owner": FROZEN_OWNER,
            "frozen_owner_is_tangency_target": owner_is_graph,
            "frozen_owner_whole_parent_record_classification":
                frozen.classification,
            "frozen_owner_discriminant_sign": discriminant_sign,
            "frozen_owner_discriminant_arb_display_outer":
                str(frozen.discriminant),
            "frozen_owner_near_root_sign": (
                "STRICT_POSITIVE"
                if frozen.near is not None and bool(frozen.near > 0)
                else "NOT_APPLICABLE"
            ),
            "frozen_owner_near_root_arb_display_outer": (
                str(frozen.near) if frozen.near is not None else None
            ),
            "arb_display_outers_are_not_sign_witnesses": True,
            "record_scope": "ENTIRE_3D_AMBIENT_PARENT_BOX",
            "resolution": resolution,
            "whole_parent_frozen_prefix_excluded": excluded,
            "remaining_live_composite": not excluded,
            "whole_parent_exclusion_basis": (
                "FROZEN_OWNER_DISCRIMINANT_STRICTLY_NEGATIVE_ON_ENTIRE_3D_PARENT"
                if excluded
                else "NONE"
            ),
            "tangency_graph_mismatch_used_as_exclusion_evidence": False,
            "Round164_live_regression_binding": binding,
        }))
    rows.sort(key=lambda row: row["ambient_leaf_key"])
    bindings.sort(key=lambda row: row["ambient_leaf_key"])
    require(
        set(upstream_rows) == {row["ambient_leaf_key"] for row in rows},
        "all Round164 parent keys",
    )
    return rows, bindings


def independently_reconstruct_result(
    docs: dict[str, dict[str, Any]],
    producer_sha256: str,
) -> dict[str, Any]:
    r164 = independently_validate_chain(docs)
    rows, regressions = independently_reconstruct_rows(r164)
    absent_rows = [
        row for row in rows
        if row["resolution"]
        == "EXCLUDED_FROZEN_OWNER_ABSENT_ON_WHOLE_PARENT"
    ]
    exception_rows = [
        row for row in rows
        if row["resolution"]
        == "LIVE_PREFIX_MISMATCH_STRICT_FUTURE_EXCEPTION"
    ]
    owner_graph_rows = [
        row for row in rows
        if row["resolution"] == "LIVE_FROZEN_OWNER_TANGENCY_COMPOSITE"
    ]
    mismatch_rows = [
        row for row in rows
        if not row["frozen_owner_is_tangency_target"]
    ]
    absent_keys = tuple(row["ambient_leaf_key"] for row in absent_rows)
    exception_keys = tuple(row["ambient_leaf_key"] for row in exception_rows)
    require(absent_keys == EXPECTED_ABSENT_KEYS, "exact ten keys")
    require(exception_keys == EXPECTED_EXCEPTION_KEYS, "exact exceptions")
    require(
        (
            len(rows),
            len(mismatch_rows),
            len(absent_rows),
            len(exception_rows),
            len(owner_graph_rows),
            len(regressions),
        ) == (32, 12, 10, 2, 20, 2),
        "32/12/10/2/20 independent census",
    )
    require(
        all(
            row["frozen_owner_whole_parent_record_classification"]
            == "no_real_intersection"
            and row["frozen_owner_discriminant_sign"] == "STRICT_NEGATIVE"
            and row["record_scope"] == "ENTIRE_3D_AMBIENT_PARENT_BOX"
            and row["whole_parent_frozen_prefix_excluded"] is True
            and row["tangency_graph_mismatch_used_as_exclusion_evidence"]
            is False
            for row in absent_rows
        ),
        "ten dimension-safe exclusions",
    )
    require(
        all(
            row["frozen_owner_whole_parent_record_classification"]
            == "strict_future_root"
            and row["remaining_live_composite"] is True
            and row["Round164_live_regression_binding"] is not None
            for row in exception_rows
        ),
        "two live exceptions",
    )
    prior_excluded = 73162
    new_excluded = 10
    combined_excluded = 73172
    remaining_tangency = 22
    live_components = {
        "original_stage_one_match": 518,
        "Round165_seam_live_composites": 504,
        "remaining_tangency_parent_composites": remaining_tangency,
        "Round166_owner_active_multi": 2616,
    }
    combined_live = sum(live_components.values())
    require(
        prior_excluded + new_excluded == combined_excluded
        and combined_live == 3660
        and combined_excluded + combined_live == 76832,
        "Round172 conservation",
    )
    return {
        "status": (
            "CERTIFIED_10_WHOLE_TANGENCY_PARENT_FROZEN_OWNER_ABSENCE_"
            "EXCLUSIONS__D02_STILL_BLOCKED"
        ),
        "frozen_prefix": {
            "source_obstacle": "W",
            "collision_index": 1,
            "required_owner": FROZEN_OWNER,
            "required_outgoing_chart": FROZEN_OUTGOING_CHART,
            "stage_one_only": True,
        },
        "independent_192_bit_atlas_replay": {
            "precision_bits": 192,
            "source_W_charts": list(CHARTS),
            "Round164_tangency_parent_count": len(rows),
            "Round164_prefix_mismatch_graph_parent_count":
                len(mismatch_rows),
            "Round164_frozen_owner_graph_parent_count":
                len(owner_graph_rows),
            "frozen_owner_whole_parent_no_real_intersection_count":
                len(absent_rows),
            "frozen_owner_strict_future_exception_count":
                len(exception_rows),
            "all_32_parent_rows_sha256": digest(rows),
            "all_32_parent_rows": rows,
        },
        "whole_parent_frozen_owner_absence_credit": {
            "new_whole_parent_exclusion_count": new_excluded,
            "ambient_parent_dimension": 3,
            "frozen_owner": FROZEN_OWNER,
            "required_record_classification": "no_real_intersection",
            "required_discriminant_sign": "STRICT_NEGATIVE",
            "required_scope": "ENTIRE_3D_AMBIENT_PARENT_BOX",
            "exclusion_is_independent_of_mismatch_tangency_graph": True,
            "mismatch_tangency_graph_credit": 0,
            "exact_excluded_parent_keys": list(absent_keys),
            "exact_excluded_parent_keys_sha256": digest(list(absent_keys)),
            "credited_parent_rows_sha256": digest(absent_rows),
        },
        "strict_future_exception_ledger": {
            "exception_count": len(exception_rows),
            "exact_exception_parent_keys": list(exception_keys),
            "exact_exception_parent_keys_sha256":
                digest(list(exception_keys)),
            "both_remain_live_composites": True,
            "both_bound_to_Round164_live_regressions": True,
            "regression_bindings_sha256": digest(regressions),
            "regression_bindings": regressions,
        },
        "remaining_tangency_composites": {
            "frozen_owner_graph_parent_count": len(owner_graph_rows),
            "prefix_mismatch_strict_future_exception_count":
                len(exception_rows),
            "remaining_parent_composite_count": remaining_tangency,
            "all_require_D_negative_D_zero_D_positive_recut": True,
            "all_require_outgoing_processing_on_live_strata": True,
            "frozen_owner_graph_parent_keys": [
                row["ambient_leaf_key"] for row in owner_graph_rows
            ],
            "frozen_owner_graph_parent_keys_sha256": digest([
                row["ambient_leaf_key"] for row in owner_graph_rows
            ]),
        },
        "Round168_to_Round172_composition": {
            "refined_source_W_record_count": 76832,
            "Round168_whole_record_excluded": prior_excluded,
            "Round172_new_whole_parent_excluded": new_excluded,
            "combined_whole_record_excluded": combined_excluded,
            "new_credit_disjoint_from_all_Round168_credit_blocks": True,
            "Round168_conservative_live": 3670,
            "Round172_conservative_live": combined_live,
            "live_components": live_components,
            "conservation_identity": "73172+3660=76832",
            "refined_total_unchanged": True,
        },
        "dimension_safe_noncredit": {
            "Round164_tangency_graph_mismatch_whole_parent_credit": 0,
            "Round164_typed_graph_only_credit": 0,
            "two_strict_future_exception_whole_parent_credit": 0,
            "twenty_frozen_owner_graph_parent_whole_parent_credit": 0,
            "Round165_typed_collar_mismatch_side_whole_record_credit": 0,
            "Round166_deep_refinement_profile_whole_record_credit": 0,
        },
        "upstream_verified_chain": {
            "Round164_v2": {
                "certificate_result_sha256": R164_RESULT,
                "verification_result_sha256": R164_VER_RESULT,
                "status": "PASS",
                "all_32_tangency_graphs_reconstructed": True,
            },
            "Round168": {
                "certificate_result_sha256": R168_RESULT,
                "verification_result_sha256": R168_VER_RESULT,
                "status": "PASS",
                "full_expected_canonical_equality": True,
            },
        },
        "scope": {
            "whole_parent_credit_requires_frozen_owner_absence": True,
            "codimension_one_graph_mismatch_never_implies_parent_exclusion":
                True,
            "arb_display_outers_are_not_sign_witnesses": True,
            "not_later_frozen_prefix_resolution": True,
            "not_exterior_sheet_exhaustion": True,
            "not_D02_closure": True,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "materialize and separately ledger D<0, D=0, and D>0 strata "
            "for all 22 remaining tangency parent composites, then perform "
            "outgoing-chart and later frozen-prefix processing only on their "
            "live strata; continue the 224 whole-W rectangles and resolve "
            "the 2,616 owner-active multi parents"
        ),
        "provenance": {
            "schema": CERTIFICATE_SCHEMA,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "source_W_atlas_replayed_at_192_bits": True,
            "python_flint_version": flint.__version__,
            "arb_context_precision_bits": atlas.ctx.prec,
            "one_geometry_evaluation_per_parent_root_replay": True,
            "Round164_and_Round168_producers_imported_or_executed": False,
            "verification_source_pins": [R164_VERIFIER, R168_VERIFIER],
            "older_round_files_modified": False,
        },
    }


def exact_key_tree(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"type:{path}")
    if type(expected) is dict:
        require(set(actual) == set(expected), f"keys:{path}")
        for key in expected:
            exact_key_tree(actual[key], expected[key], f"{path}.{key}")
    elif type(expected) is list:
        require(len(actual) == len(expected), f"list length:{path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            exact_key_tree(left, right, f"{path}[{index}]")


def validate_certificate_document(
    document: dict[str, Any],
    expected_document: dict[str, Any],
) -> None:
    exact_key_tree(document, expected_document)
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(
        document["result_sha256"] == digest(document["result"]),
        "certificate digest",
    )
    require(
        document["result_sha256"] == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "frozen certificate result",
    )
    require(
        canonical_bytes(document) == canonical_bytes(expected_document),
        "full expected canonical equality",
    )


def resigned(
    document: dict[str, Any],
    mutate: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    candidate = copy.deepcopy(document)
    mutate(candidate)
    candidate["result_sha256"] = digest(candidate["result"])
    return candidate


def semantic_attacks(
    document: dict[str, Any],
    expected_document: dict[str, Any],
) -> dict[str, Any]:
    rows = document["result"]["independent_192_bit_atlas_replay"][
        "all_32_parent_rows"
    ]
    absent_index = next(
        index for index, row in enumerate(rows)
        if row["whole_parent_frozen_prefix_excluded"]
    )
    exception_index = next(
        index for index, row in enumerate(rows)
        if row["resolution"]
        == "LIVE_PREFIX_MISMATCH_STRICT_FUTURE_EXCEPTION"
    )
    graph_index = next(
        index for index, row in enumerate(rows)
        if row["resolution"] == "LIVE_FROZEN_OWNER_TANGENCY_COMPOSITE"
    )
    attacks: dict[str, Callable[[dict[str, Any]], None]] = {
        "schema": lambda d: d.__setitem__("schema", "mutated"),
        "status": lambda d: d["result"].__setitem__("status", "PASS"),
        "source obstacle":
            lambda d: d["result"]["frozen_prefix"].__setitem__(
                "source_obstacle", "G"
            ),
        "frozen owner":
            lambda d: d["result"]["frozen_prefix"].__setitem__(
                "required_owner", "G[1,0]"
            ),
        "outgoing chart":
            lambda d: d["result"]["frozen_prefix"].__setitem__(
                "required_outgoing_chart", "N"
            ),
        "precision":
            lambda d: d["result"]["independent_192_bit_atlas_replay"].__setitem__(
                "precision_bits", 191
            ),
        "parent count":
            lambda d: d["result"]["independent_192_bit_atlas_replay"].__setitem__(
                "Round164_tangency_parent_count", 31
            ),
        "mismatch count":
            lambda d: d["result"]["independent_192_bit_atlas_replay"].__setitem__(
                "Round164_prefix_mismatch_graph_parent_count", 11
            ),
        "owner graph count":
            lambda d: d["result"]["independent_192_bit_atlas_replay"].__setitem__(
                "Round164_frozen_owner_graph_parent_count", 19
            ),
        "absence count":
            lambda d: d["result"]["independent_192_bit_atlas_replay"].__setitem__(
                "frozen_owner_whole_parent_no_real_intersection_count", 11
            ),
        "exception count":
            lambda d: d["result"]["independent_192_bit_atlas_replay"].__setitem__(
                "frozen_owner_strict_future_exception_count", 1
            ),
        "all rows digest":
            lambda d: d["result"]["independent_192_bit_atlas_replay"].__setitem__(
                "all_32_parent_rows_sha256", "0" * 64
            ),
        "absence row key":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][absent_index].__setitem__("ambient_leaf_key", "forged"),
        "absence row dimension":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][absent_index].__setitem__("ambient_parameter_dimension", 2),
        "absence tangency target":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][absent_index].__setitem__("Round164_tangency_target", FROZEN_OWNER),
        "absence frozen record":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][absent_index].__setitem__(
                "frozen_owner_whole_parent_record_classification",
                "unresolved_discriminant",
            ),
        "absence discriminant sign":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][absent_index].__setitem__(
                "frozen_owner_discriminant_sign", "UNRESOLVED"
            ),
        "absence record scope":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][absent_index].__setitem__(
                "record_scope", "CODIMENSION_ONE_GRAPH"
            ),
        "absence resolution":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][absent_index].__setitem__(
                "resolution", "EXCLUDED_BY_GRAPH_MISMATCH"
            ),
        "absence credit flag":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][absent_index].__setitem__(
                "whole_parent_frozen_prefix_excluded", False
            ),
        "absence basis":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][absent_index].__setitem__(
                "whole_parent_exclusion_basis", "TANGENCY_GRAPH_MISMATCH"
            ),
        "mismatch used as evidence":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][absent_index].__setitem__(
                "tangency_graph_mismatch_used_as_exclusion_evidence", True
            ),
        "absence row digest":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][absent_index].__setitem__("row_sha256", "0" * 64),
        "exception frozen record":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][exception_index].__setitem__(
                "frozen_owner_whole_parent_record_classification",
                "no_real_intersection",
            ),
        "exception near sign":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][exception_index].__setitem__(
                "frozen_owner_near_root_sign", "NOT_APPLICABLE"
            ),
        "exception fake exclusion":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][exception_index].__setitem__(
                "whole_parent_frozen_prefix_excluded", True
            ),
        "exception remove regression":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][exception_index].__setitem__(
                "Round164_live_regression_binding", None
            ),
        "owner graph fake exclusion":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][graph_index].__setitem__(
                "whole_parent_frozen_prefix_excluded", True
            ),
        "owner graph fake negative":
            lambda d: d["result"]["independent_192_bit_atlas_replay"][
                "all_32_parent_rows"
            ][graph_index].__setitem__(
                "frozen_owner_discriminant_sign", "STRICT_NEGATIVE"
            ),
        "credit count":
            lambda d: d["result"][
                "whole_parent_frozen_owner_absence_credit"
            ].__setitem__("new_whole_parent_exclusion_count", 12),
        "credit dimension":
            lambda d: d["result"][
                "whole_parent_frozen_owner_absence_credit"
            ].__setitem__("ambient_parent_dimension", 2),
        "credit classification":
            lambda d: d["result"][
                "whole_parent_frozen_owner_absence_credit"
            ].__setitem__(
                "required_record_classification", "tangency_graph"
            ),
        "credit scope":
            lambda d: d["result"][
                "whole_parent_frozen_owner_absence_credit"
            ].__setitem__("required_scope", "D_ZERO_GRAPH"),
        "credit independence":
            lambda d: d["result"][
                "whole_parent_frozen_owner_absence_credit"
            ].__setitem__(
                "exclusion_is_independent_of_mismatch_tangency_graph", False
            ),
        "mismatch graph credit":
            lambda d: d["result"][
                "whole_parent_frozen_owner_absence_credit"
            ].__setitem__("mismatch_tangency_graph_credit", 12),
        "excluded key":
            lambda d: d["result"][
                "whole_parent_frozen_owner_absence_credit"
            ]["exact_excluded_parent_keys"].__setitem__(0, "forged"),
        "excluded keys digest":
            lambda d: d["result"][
                "whole_parent_frozen_owner_absence_credit"
            ].__setitem__("exact_excluded_parent_keys_sha256", "0" * 64),
        "credited rows digest":
            lambda d: d["result"][
                "whole_parent_frozen_owner_absence_credit"
            ].__setitem__("credited_parent_rows_sha256", "0" * 64),
        "exception ledger count":
            lambda d: d["result"]["strict_future_exception_ledger"].__setitem__(
                "exception_count", 1
            ),
        "exception key":
            lambda d: d["result"]["strict_future_exception_ledger"][
                "exact_exception_parent_keys"
            ].__setitem__(0, "forged"),
        "exception live guard":
            lambda d: d["result"]["strict_future_exception_ledger"].__setitem__(
                "both_remain_live_composites", False
            ),
        "exception regression guard":
            lambda d: d["result"]["strict_future_exception_ledger"].__setitem__(
                "both_bound_to_Round164_live_regressions", False
            ),
        "regression row":
            lambda d: d["result"]["strict_future_exception_ledger"][
                "regression_bindings"
            ][0].__setitem__("point_first_owner", "G[1,0]"),
        "regression outgoing":
            lambda d: d["result"]["strict_future_exception_ledger"][
                "regression_bindings"
            ][0].__setitem__("point_outgoing_chart", "N"),
        "regression live proof":
            lambda d: d["result"]["strict_future_exception_ledger"][
                "regression_bindings"
            ][0].__setitem__(
                "proves_exception_parent_must_remain_live", False
            ),
        "regression digest":
            lambda d: d["result"]["strict_future_exception_ledger"].__setitem__(
                "regression_bindings_sha256", "0" * 64
            ),
        "remaining owner graphs":
            lambda d: d["result"]["remaining_tangency_composites"].__setitem__(
                "frozen_owner_graph_parent_count", 19
            ),
        "remaining exceptions":
            lambda d: d["result"]["remaining_tangency_composites"].__setitem__(
                "prefix_mismatch_strict_future_exception_count", 1
            ),
        "remaining total":
            lambda d: d["result"]["remaining_tangency_composites"].__setitem__(
                "remaining_parent_composite_count", 20
            ),
        "disable recut":
            lambda d: d["result"]["remaining_tangency_composites"].__setitem__(
                "all_require_D_negative_D_zero_D_positive_recut", False
            ),
        "disable outgoing":
            lambda d: d["result"]["remaining_tangency_composites"].__setitem__(
                "all_require_outgoing_processing_on_live_strata", False
            ),
        "Round168 exclusion":
            lambda d: d["result"]["Round168_to_Round172_composition"].__setitem__(
                "Round168_whole_record_excluded", 73172
            ),
        "Round172 exclusion":
            lambda d: d["result"]["Round168_to_Round172_composition"].__setitem__(
                "Round172_new_whole_parent_excluded", 0
            ),
        "combined exclusion":
            lambda d: d["result"]["Round168_to_Round172_composition"].__setitem__(
                "combined_whole_record_excluded", 73182
            ),
        "credit disjointness":
            lambda d: d["result"]["Round168_to_Round172_composition"].__setitem__(
                "new_credit_disjoint_from_all_Round168_credit_blocks", False
            ),
        "Round172 live":
            lambda d: d["result"]["Round168_to_Round172_composition"].__setitem__(
                "Round172_conservative_live", 3650
            ),
        "tangency live component":
            lambda d: d["result"]["Round168_to_Round172_composition"][
                "live_components"
            ].__setitem__("remaining_tangency_parent_composites", 12),
        "owner active component":
            lambda d: d["result"]["Round168_to_Round172_composition"][
                "live_components"
            ].__setitem__("Round166_owner_active_multi", 0),
        "conservation":
            lambda d: d["result"]["Round168_to_Round172_composition"].__setitem__(
                "conservation_identity", "73182+3650=76832"
            ),
        "graph mismatch noncredit":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "Round164_tangency_graph_mismatch_whole_parent_credit", 12
            ),
        "exception noncredit":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "two_strict_future_exception_whole_parent_credit", 2
            ),
        "owner graph noncredit":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "twenty_frozen_owner_graph_parent_whole_parent_credit", 20
            ),
        "Round165 dimension mix":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "Round165_typed_collar_mismatch_side_whole_record_credit", 280
            ),
        "Round166 deep profile":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "Round166_deep_refinement_profile_whole_record_credit", 167984
            ),
        "Round164 upstream":
            lambda d: d["result"]["upstream_verified_chain"][
                "Round164_v2"
            ].__setitem__("status", "FAIL"),
        "Round168 upstream":
            lambda d: d["result"]["upstream_verified_chain"][
                "Round168"
            ].__setitem__("full_expected_canonical_equality", False),
        "whole-parent scope guard":
            lambda d: d["result"]["scope"].__setitem__(
                "whole_parent_credit_requires_frozen_owner_absence", False
            ),
        "codimension guard":
            lambda d: d["result"]["scope"].__setitem__(
                "codimension_one_graph_mismatch_never_implies_parent_exclusion",
                False,
            ),
        "D02 promotion":
            lambda d: d["result"]["strict_nonpromotion"].__setitem__(
                "D02", "CLOSED"
            ),
        "CM2 promotion":
            lambda d: d["result"]["strict_nonpromotion"].__setitem__(
                "CM2", "GO"
            ),
        "producer pin":
            lambda d: d["result"]["provenance"].__setitem__(
                "producer_sha256", "0" * 64
            ),
        "dependency pin":
            lambda d: d["result"]["provenance"]["dependency_sha256"].__setitem__(
                R164_CERT, "0" * 64
            ),
        "replay provenance":
            lambda d: d["result"]["provenance"].__setitem__(
                "source_W_atlas_replayed_at_192_bits", False
            ),
        "flint version provenance":
            lambda d: d["result"]["provenance"].__setitem__(
                "python_flint_version", "0.8.0"
            ),
        "Arb precision provenance":
            lambda d: d["result"]["provenance"].__setitem__(
                "arb_context_precision_bits", 191
            ),
        "claim producer execution":
            lambda d: d["result"]["provenance"].__setitem__(
                "Round164_and_Round168_producers_imported_or_executed", True
            ),
        "next gate":
            lambda d: d["result"].__setitem__("next_core_gate", "D02 closed"),
        "extra key": lambda d: d["result"].__setitem__("extra", True),
    }
    rejected: list[str] = []
    for name, mutate in attacks.items():
        candidate = resigned(document, mutate)
        require(
            candidate["result_sha256"] == digest(candidate["result"]),
            f"mutation not re-signed:{name}",
        )
        try:
            validate_certificate_document(candidate, expected_document)
        except Exception:
            rejected.append(name)
        else:
            raise VerificationError(f"semantic attack accepted:{name}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == len(attacks),
        "every_mutation_result_digest_resigned": True,
        "rejected_attack_names": rejected,
    }


def strict_json_attacks() -> dict[str, Any]:
    attacks: dict[str, bytes] = {
        "duplicate key":
            b'{"schema":"x","result":{},"result":{},"result_sha256":"x"}',
        "float":
            b'{"schema":"x","result":{"x":1.0},"result_sha256":"x"}',
        "NaN":
            b'{"schema":"x","result":{"x":NaN},"result_sha256":"x"}',
        "BOM":
            b'\xef\xbb\xbf{"schema":"x","result":{},"result_sha256":"x"}',
        "raw NUL":
            b'{"schema":"x","result":{},"result_sha256":"x"}\x00',
        "escaped NUL":
            b'{"schema":"x","result":{"x":"\\u0000"},"result_sha256":"x"}',
        "surrogate":
            b'{"schema":"x","result":{"x":"\\ud800"},"result_sha256":"x"}',
        "trailing document":
            b'{"schema":"x","result":{},"result_sha256":"x"}{}',
        "top array": b'[]',
    }
    rejected: list[str] = []
    for name, raw in attacks.items():
        try:
            parse_envelope(
                raw,
                label=f"strict attack:{name}",
                require_canonical=False,
            )
        except Exception:
            rejected.append(name)
        else:
            raise VerificationError(f"strict JSON attack accepted:{name}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == len(attacks),
        "rejected_attack_names": rejected,
    }


def safe_atomic_write(
    path: Path,
    data: bytes,
    protected_paths: set[Path],
) -> None:
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.parent.resolve() == HERE, "output must remain in deliverables")
    if path.exists() or path.is_symlink():
        st = path.lstat()
        require(stat.S_ISREG(st.st_mode), "output is not regular")
        require(not path.is_symlink(), "symlink output rejected")
        require(st.st_nlink == 1, "multiply linked output rejected")
    require(
        path.resolve(strict=False) not in protected_paths,
        "output aliases protected input",
    )
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def expect_rejection(name: str, operation: Callable[[], Any]) -> str:
    try:
        operation()
    except Exception:
        return name
    raise VerificationError(f"path-safety attack accepted:{name}")


def path_safety_attacks(certificate_path: Path) -> dict[str, Any]:
    rejected: list[str] = []
    scratch = Path(tempfile.mkdtemp(prefix=".cm2_round172_path_attack.", dir=HERE))
    symlink_output = HERE / f".cm2_round172_symlink_output.{os.getpid()}"
    hard_output_base = HERE / f".cm2_round172_hard_output_base.{os.getpid()}"
    hard_output_link = HERE / f".cm2_round172_hard_output_link.{os.getpid()}"
    try:
        source = scratch / "source"
        source.write_bytes(b"{}\n")
        symlink_input = scratch / "symlink-input"
        symlink_input.symlink_to(source)
        rejected.append(expect_rejection(
            "symlink input",
            lambda: read_regular(symlink_input),
        ))
        hard_input = scratch / "hard-input"
        os.link(source, hard_input)
        rejected.append(expect_rejection(
            "hardlink input",
            lambda: read_regular(hard_input),
        ))
        oversized = scratch / "oversized"
        with oversized.open("wb") as handle:
            handle.truncate(MAX_INPUT_BYTES + 1)
        rejected.append(expect_rejection(
            "oversized sparse input",
            lambda: read_regular(oversized),
        ))
        protected = {
            certificate_path.resolve(),
            PRODUCER.resolve(),
            Path(__file__).resolve(),
        }
        rejected.append(expect_rejection(
            "outside-directory output",
            lambda: safe_atomic_write(
                scratch / "outside-output.json", b"{}\n", protected
            ),
        ))
        rejected.append(expect_rejection(
            "protected certificate alias",
            lambda: safe_atomic_write(certificate_path, b"{}\n", protected),
        ))
        symlink_target = scratch / "symlink-target"
        symlink_target.write_bytes(b"unchanged")
        symlink_output.symlink_to(symlink_target)
        rejected.append(expect_rejection(
            "symlink output",
            lambda: safe_atomic_write(symlink_output, b"changed", protected),
        ))
        require(
            symlink_target.read_bytes() == b"unchanged",
            "symlink target changed",
        )
        hard_output_base.write_bytes(b"unchanged")
        os.link(hard_output_base, hard_output_link)
        rejected.append(expect_rejection(
            "hardlink output",
            lambda: safe_atomic_write(hard_output_link, b"changed", protected),
        ))
        require(
            hard_output_base.read_bytes() == b"unchanged",
            "hardlink target changed",
        )
    finally:
        if symlink_output.exists() or symlink_output.is_symlink():
            symlink_output.unlink()
        if hard_output_link.exists():
            hard_output_link.unlink()
        if hard_output_base.exists():
            hard_output_base.unlink()
        shutil.rmtree(scratch)
    return {
        "attack_count": 7,
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == 7,
        "rejected_attack_names": rejected,
        "inputs_regular_single_link_non_symlink_and_size_bounded": True,
        "outputs_confined_nonalias_atomic_fsync_replace": True,
    }


def build_verification(certificate_path: Path) -> dict[str, Any]:
    for name in (
        ATLAS_SOURCE,
        BASE_SOURCE,
        GE_SOURCE,
        R164_VERIFIER,
        R168_VERIFIER,
    ):
        read_regular(HERE / name, PINS[name])
    docs = {
        name: load_pinned(name)
        for name in (R164_CERT, R164_VER, R168_CERT, R168_VER)
    }
    producer_bytes = read_regular(PRODUCER, EXPECTED_PRODUCER_SHA256)
    producer_sha256 = sha256_bytes(producer_bytes)
    expected_result = independently_reconstruct_result(docs, producer_sha256)
    expected_document = {
        "schema": CERTIFICATE_SCHEMA,
        "result": expected_result,
        "result_sha256": digest(expected_result),
    }
    require(
        expected_document["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "independent frozen result",
    )
    certificate_bytes = read_regular(
        certificate_path,
        EXPECTED_CERTIFICATE_SHA256,
    )
    document = parse_envelope(
        certificate_bytes,
        label=certificate_path.name,
        expected_schema=CERTIFICATE_SCHEMA,
        require_canonical=True,
    )
    validate_certificate_document(document, expected_document)
    semantic = semantic_attacks(document, expected_document)
    strict_json = strict_json_attacks()
    path_safety = path_safety_attacks(certificate_path)
    require(
        semantic["all_rejected"]
        and strict_json["all_rejected"]
        and path_safety["all_rejected"],
        "attack suites",
    )
    verifier_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result = {
        "status": "PASS",
        "certificate_schema": document["schema"],
        "certificate_sha256": sha256_bytes(certificate_bytes),
        "certificate_result_sha256": document["result_sha256"],
        "producer_sha256": producer_sha256,
        "verifier_sha256": verifier_sha256,
        "independence_contract": {
            "Round172_producer_imported": False,
            "Round172_producer_executed": False,
            "Round164_and_Round168_producers_imported_or_executed": False,
            "source_W_atlas_independently_replayed_at_192_bits": True,
            "all_32_tangency_parents_reconstructed": True,
            "all_12_prefix_mismatch_graph_parents_reconstructed": True,
            "all_10_whole_parent_frozen_owner_absences_reconstructed": True,
            "both_strict_future_exceptions_reconstructed": True,
            "all_20_frozen_owner_graph_parents_reconstructed": True,
            "both_Round164_live_regressions_replayed": True,
            "full_result_independently_reconstructed": True,
            "full_expected_canonical_equality": True,
            "recursive_exact_key_tree_matched": True,
        },
        "recomputed_census": {
            "all_tangency_parents": 32,
            "prefix_mismatch_graph_parents": 12,
            "whole_parent_frozen_owner_no_real_intersection": 10,
            "strict_future_exceptions": 2,
            "frozen_owner_graph_parents": 20,
            "new_whole_parent_exclusions": 10,
            "remaining_tangency_composites": 22,
            "combined_whole_record_excluded": 73172,
            "conservative_live": 3660,
            "conservation_identity": "73172+3660=76832",
            "mismatch_tangency_graph_credit": 0,
            "all_22_remaining_require_recut_and_outgoing_processing": True,
        },
        "semantic_mutation_attack_suite": semantic,
        "strict_json_attack_suite": strict_json,
        "path_safety_attack_suite": path_safety,
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    verification = build_verification(arguments.certificate)
    protected = {(HERE / name).resolve() for name in PINS}
    protected.update({
        PRODUCER.resolve(),
        Path(__file__).resolve(),
        arguments.certificate.resolve(),
    })
    safe_atomic_write(
        arguments.output,
        canonical_bytes(verification) + b"\n",
        protected,
    )
    print(verification["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
