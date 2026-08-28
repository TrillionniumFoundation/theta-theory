#!/usr/bin/env python3
"""Prune tangency parents only by full-box frozen-owner absence.

The 32 Round164-v2 source-W tangency parents are replayed at 192-bit Arb
precision.  A whole parent receives new frozen-prefix exclusion credit only
when the frozen owner W[1,0] has strictly negative discriminant on the entire
three-dimensional parent box.  A mismatch label on another target's
codimension-one tangency graph is never used as exclusion evidence.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any

import flint
import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / (
        "cm2_round172_dimension_safe_tangency_parent_"
        "frozen_owner_absence_pruning_certificate.json"
    )
)
SCHEMA = (
    "cm2.round172.dimension-safe-tangency-parent-"
    "frozen-owner-absence-pruning.v1"
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


class PruningError(RuntimeError):
    """Fail-closed Round172 error."""


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
        raise PruningError(label)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_noninteger_number(value: str) -> None:
    raise PruningError(f"non-integer JSON number:{value}")


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


def parse_envelope(data: bytes, label: str) -> dict[str, Any]:
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
        raise PruningError(f"invalid JSON:{label}:{exc}") from exc
    validate_json_tree(value)
    require(type(value) is dict, f"top object:{label}")
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"envelope keys:{label}",
    )
    require(
        value["result_sha256"] == digest(value["result"]),
        f"result digest:{label}",
    )
    return value


def load_pinned(name: str) -> dict[str, Any]:
    return parse_envelope(read_regular(HERE / name, PINS[name]), name)


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def validate_chain(
    docs: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
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
        "Round164-v2 certificate",
    )
    require(
        v164["schema"]
        == "cm2.round164.dimension-safe-tangency-graph-typing.verification.v2"
        and v164["result_sha256"] == R164_VER_RESULT
        and v164["result"]["status"] == "PASS"
        and v164["result"]["certificate_result_sha256"] == R164_RESULT
        and v164["result"]["round164_producer_imported_or_executed"] is False
        and v164["result"]["all_32_tangency_graphs_reconstructed"] is True
        and v164["result"]["all_graph_disposition_rows_recomputed"] is True
        and v164["result"]["both_live_off_graph_regressions_replayed"] is True
        and v164["result"]["full_document_exactly_matched"] is True
        and v164["result"]["semantic_attack_suite"]["all_rejected"] is True
        and v164["result"]["strict_json_attack_suite"]["all_rejected"] is True,
        "Round164 independent verification",
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
    regressions = r164["result"]["v1_correction"]
    require(
        regressions["live_off_graph_regression_count"] == 2
        and regressions["all_live_off_graph_regressions_sha256"]
        == digest(regressions["live_off_graph_regressions"])
        and {
            row["ambient_leaf_key"]
            for row in regressions["live_off_graph_regressions"]
        } == set(EXPECTED_EXCEPTION_KEYS),
        "Round164 regression binding",
    )

    r168 = docs[R168_CERT]
    v168 = docs[R168_VER]
    require(
        r168["schema"]
        == "cm2.round168.dimension-safe-source-W-stage-one-ledger.v1"
        and r168["result_sha256"] == R168_RESULT,
        "Round168 certificate",
    )
    require(
        v168["schema"]
        == (
            "cm2.round168.dimension-safe-source-W-stage-one-ledger."
            "verification.v1"
        )
        and v168["result_sha256"] == R168_VER_RESULT
        and v168["result"]["status"] == "PASS"
        and v168["result"]["certificate_result_sha256"] == R168_RESULT
        and v168["result"]["independence_contract"][
            "full_result_independently_reconstructed"
        ] is True
        and v168["result"]["independence_contract"][
            "full_expected_canonical_equality"
        ] is True
        and v168["result"]["independence_contract"][
            "recursive_exact_key_tree_matched"
        ] is True
        and v168["result"]["semantic_mutation_attack_suite"][
            "all_rejected"
        ] is True
        and v168["result"]["strict_json_attack_suite"]["all_rejected"] is True
        and v168["result"]["path_safety_attack_suite"]["all_rejected"] is True,
        "Round168 independent verification",
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
        "Round168 dimension-safe ledger",
    )
    return r164, r168


def replay_records(
    chart_id: str,
    box: atlas.AtlasBox,
) -> list[atlas.RootRecord]:
    """Replay every retained target with one 192-bit geometry evaluation."""

    qx, qy, ux, uy, s, _radial = atlas.geometry(chart_id, box)
    records: list[atlas.RootRecord] = []
    for target_id in REPLAY_CANDIDATE_IDS[chart_id]:
        target = REPLAY_TARGETS[target_id]
        center_x, center_y = base.target_center(target, s)
        dx, dy = center_x - qx, center_y - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = base.arbq(base.RADIUS[target.obstacle])
        discriminant = radius * radius - transverse * transverse
        if bool(discriminant < 0):
            records.append(atlas.RootRecord(
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
            records.append(atlas.RootRecord(
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
        records.append(atlas.RootRecord(
            target_id,
            classification,
            ell,
            discriminant,
            near,
            far,
            transverse,
        ))
    return records


def build_atlases() -> dict[str, list[atlas.Leaf]]:
    original_records = atlas.records
    atlas.records = replay_records
    try:
        direct_e = atlas.build_atlas("W:E")
        direct_n = atlas.build_atlas("W:N")
    finally:
        atlas.records = original_records
    return {
        "W:E": direct_e,
        "W:N": direct_n,
        "W:S": [
            atlas.reflect_leaf("W:N", "horizontal", leaf)
            for leaf in direct_n
        ],
    }


def point_outgoing_chart(
    chart_id: str,
    point: atlas.AtlasBox,
) -> tuple[str, Any, Any]:
    frozen = next(
        row for row in replay_records(chart_id, point)
        if row.target_id == FROZEN_OWNER
    )
    require(
        frozen.classification == "strict_future_root"
        and frozen.near is not None,
        "regression frozen future root",
    )
    qx, qy, ux, uy, s, _radial = atlas.geometry(chart_id, point)
    target = REPLAY_TARGETS[FROZEN_OWNER]
    center_x, center_y = base.target_center(target, s)
    radius = base.arbq(base.RADIUS[target.obstacle])
    normal_x = (qx + frozen.near * ux - center_x) / radius
    normal_y = (qy + frozen.near * uy - center_y) / radius
    tests = {
        "E": (normal_x - normal_y, normal_x + normal_y),
        "W": (-normal_x - normal_y, -normal_x + normal_y),
        "N": (normal_y - normal_x, normal_y + normal_x),
        "S": (-normal_y - normal_x, -normal_y + normal_x),
    }
    for cell in ("E", "W", "N", "S"):
        first, second = tests[cell]
        if bool(first > 0) and bool(second > 0):
            return cell, first, second
    raise PruningError("regression outgoing chart unresolved")


def replay_exception_regression(
    chart_id: str,
    leaf: atlas.Leaf,
    tangency_target: str,
    upstream_row: dict[str, Any],
) -> dict[str, Any]:
    point_data = upstream_row["strict_interior_point"]
    t = Q(point_data["t"])
    p = Q(point_data["p"])
    s = Q(point_data["s"])
    box = leaf.box
    require(
        box.t0 < t < box.t1
        and box.p0 < p < box.p1
        and box.s0 < s < box.s1,
        "regression strict interior",
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
    atlas.records = replay_records
    try:
        classification = atlas.classify_box(chart_id, point)
    finally:
        atlas.records = original_records
    require(
        classification.classification == "unique_first"
        and classification.owner_target == FROZEN_OWNER,
        "regression frozen first owner",
    )
    tangency_record = next(
        row for row in replay_records(chart_id, point)
        if row.target_id == tangency_target
    )
    require(
        tangency_record.classification == "no_real_intersection"
        and bool(tangency_record.discriminant < 0),
        "regression strictly off mismatch graph",
    )
    outgoing, margin_one, margin_two = point_outgoing_chart(chart_id, point)
    require(
        outgoing == FROZEN_OUTGOING_CHART
        and bool(margin_one > 0)
        and bool(margin_two > 0),
        "regression frozen outgoing chart",
    )
    require(
        upstream_row["tangency_target"] == tangency_target
        and upstream_row["point_first_hit_classification"] == "unique_first"
        and upstream_row["point_first_owner"] == FROZEN_OWNER
        and upstream_row["point_outgoing_chart"] == FROZEN_OUTGOING_CHART
        and upstream_row[
            "proves_ambient_leaf_cannot_be_pruned_from_graph_only"
        ] is True,
        "Round164 regression semantics",
    )
    return {
        "Round164_regression_row_sha256": digest(upstream_row),
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


def reconstruct_parent_rows(
    r164: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    atlases = build_atlases()
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
    require(len(leaves) == 32, "replayed tangency parent count")
    rows: list[dict[str, Any]] = []
    regression_bindings: list[dict[str, Any]] = []
    for chart_id, leaf in leaves:
        key = f"{chart_id}:{leaf.box.path}"
        require(key in upstream_rows, f"Round164 parent key:{key}")
        require(
            leaf.classification == "tangency_graph"
            and len(leaf.tangency_targets) == 1,
            f"unique tangency graph:{key}",
        )
        tangency_target = leaf.tangency_targets[0]
        records = replay_records(chart_id, leaf.box)
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
            f"physical tangency graph:{key}",
        )
        upstream = upstream_rows[key]
        require(
            upstream["tangency_target"] == tangency_target
            and upstream["ambient_parameter_dimension"] == 3
            and upstream["typed_graph_dimension"] == 2
            and upstream["ambient_leaf_bulk_disposition"]
            == "UNRESOLVED_OFF_GRAPH_BULK",
            f"Round164 row binding:{key}",
        )
        frozen = next(
            record for record in records
            if record.target_id == FROZEN_OWNER
        )
        owner_is_graph = tangency_target == FROZEN_OWNER
        regression_binding: dict[str, Any] | None = None
        if owner_is_graph:
            require(
                upstream["graph_disposition"]
                == "TYPED_FROZEN_OWNER_TANGENCY_GRAPH"
                and frozen.classification == "unresolved_discriminant",
                f"frozen-owner graph:{key}",
            )
            resolution = "LIVE_FROZEN_OWNER_TANGENCY_COMPOSITE"
            discriminant_sign = "UNRESOLVED_ACROSS_TYPED_GRAPH"
            whole_parent_excluded = False
        else:
            require(
                upstream["graph_disposition"]
                == "TYPED_PREFIX_MISMATCH_TANGENCY_GRAPH",
                f"mismatch graph:{key}",
            )
            if (
                frozen.classification == "no_real_intersection"
                and bool(frozen.discriminant < 0)
            ):
                resolution = "EXCLUDED_FROZEN_OWNER_ABSENT_ON_WHOLE_PARENT"
                discriminant_sign = "STRICT_NEGATIVE"
                whole_parent_excluded = True
            else:
                require(
                    key in EXPECTED_EXCEPTION_KEYS
                    and frozen.classification == "strict_future_root"
                    and bool(frozen.discriminant > 0)
                    and frozen.near is not None
                    and bool(frozen.near > 0),
                    f"only strict-future exceptions:{key}",
                )
                resolution = "LIVE_PREFIX_MISMATCH_STRICT_FUTURE_EXCEPTION"
                discriminant_sign = "STRICT_POSITIVE"
                whole_parent_excluded = False
                regression_binding = replay_exception_regression(
                    chart_id,
                    leaf,
                    tangency_target,
                    upstream_regressions[key],
                )
                regression_bindings.append(closed_row({
                    "ambient_leaf_key": key,
                    **regression_binding,
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
            "whole_parent_frozen_prefix_excluded": whole_parent_excluded,
            "remaining_live_composite": not whole_parent_excluded,
            "whole_parent_exclusion_basis": (
                "FROZEN_OWNER_DISCRIMINANT_STRICTLY_NEGATIVE_ON_ENTIRE_3D_PARENT"
                if whole_parent_excluded
                else "NONE"
            ),
            "tangency_graph_mismatch_used_as_exclusion_evidence": False,
            "Round164_live_regression_binding": regression_binding,
        }))
    rows.sort(key=lambda row: row["ambient_leaf_key"])
    regression_bindings.sort(key=lambda row: row["ambient_leaf_key"])
    require(set(upstream_rows) == {row["ambient_leaf_key"] for row in rows}, "all Round164 rows")
    return rows, regression_bindings


def build_result(
    docs: dict[str, dict[str, Any]],
    producer_sha256: str,
) -> dict[str, Any]:
    r164, _r168 = validate_chain(docs)
    rows, regressions = reconstruct_parent_rows(r164)
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
    require(absent_keys == EXPECTED_ABSENT_KEYS, "exact ten absence keys")
    require(exception_keys == EXPECTED_EXCEPTION_KEYS, "exact two exceptions")
    require(
        len(rows) == 32
        and len(mismatch_rows) == 12
        and len(absent_rows) == 10
        and len(exception_rows) == 2
        and len(owner_graph_rows) == 20
        and len(regressions) == 2,
        "32/12/10/2/20 census",
    )
    require(
        all(
            row["frozen_owner_whole_parent_record_classification"]
            == "no_real_intersection"
            and row["frozen_owner_discriminant_sign"] == "STRICT_NEGATIVE"
            and row["whole_parent_frozen_prefix_excluded"] is True
            and row["tangency_graph_mismatch_used_as_exclusion_evidence"]
            is False
            for row in absent_rows
        ),
        "dimension-safe ten credits",
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
    new_excluded = len(absent_rows)
    combined_excluded = prior_excluded + new_excluded
    remaining_tangency = len(owner_graph_rows) + len(exception_rows)
    live_components = {
        "original_stage_one_match": 518,
        "Round165_seam_live_composites": 504,
        "remaining_tangency_parent_composites": remaining_tangency,
        "Round166_owner_active_multi": 2616,
    }
    combined_live = sum(live_components.values())
    require(
        combined_excluded == 73172
        and remaining_tangency == 22
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
            "schema": SCHEMA,
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
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
    producer_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result = build_result(docs, producer_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    protected = {(HERE / name).resolve() for name in PINS}
    protected.add(Path(__file__).resolve())
    safe_atomic_write(
        arguments.output,
        canonical_bytes(envelope) + b"\n",
        protected,
    )
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
