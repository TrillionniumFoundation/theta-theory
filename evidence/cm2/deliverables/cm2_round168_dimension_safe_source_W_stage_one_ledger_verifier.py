#!/usr/bin/env python3
"""Independent verifier for the Round168 dimension-safe source-W ledger.

The producer is byte-pinned but is never imported or executed.  This verifier
independently validates the admitted Round164/165/166 evidence, reconstructs
the complete certificate result, enforces recursive exact keys and canonical
bytes, and exercises re-signed semantic, strict-JSON, and path-safety attacks.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PRODUCER = HERE / "cm2_round168_dimension_safe_source_W_stage_one_ledger.py"
CERTIFICATE = (
    HERE
    / "cm2_round168_dimension_safe_source_W_stage_one_ledger_certificate.json"
)
OUTPUT = (
    HERE
    / "cm2_round168_dimension_safe_source_W_stage_one_ledger_verification.json"
)

CERTIFICATE_SCHEMA = "cm2.round168.dimension-safe-source-W-stage-one-ledger.v1"
VERIFICATION_SCHEMA = (
    "cm2.round168.dimension-safe-source-W-stage-one-ledger.verification.v1"
)
MAX_INPUT_BYTES = 8 * 1024 * 1024

R164_CERT = "cm2_round164_tangency_strata_pruning_certificate.json"
R164_VER = "cm2_round164_tangency_strata_pruning_verification.json"
R165_CERT = "cm2_round165_adaptive_typed_seam_census_certificate.json"
R165_VER = "cm2_round165_adaptive_typed_seam_census_verification.json"
R165_VERIFIER = "cm2_round165_adaptive_typed_seam_census_verifier.py"
R166_VER = "cm2_round166_multi_candidate_refinement_prototype_verification.json"
R166_VERIFIER = "cm2_round166_multi_candidate_refinement_prototype_verifier.py"

PINS: dict[str, str] = {
    R164_CERT:
        "2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092",
    R164_VER:
        "850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0",
    R165_CERT:
        "2cbd69e8cbde66966d78764c0d5b34518c2ec55891d0238a62f40073ae4876a8",
    R165_VER:
        "af684b956c40c97e26fdd5f9ddacea85b9c693b0b9a935d387ed1a5142ffa3b5",
    R165_VERIFIER:
        "1967147d98075792dc6821ff72e46b2f33251ba98950d1660d10280bf0ef298e",
    R166_VER:
        "66f61b657eb72a0db90291d390d1021859c65ab059fdeaedabee95170102d1af",
    R166_VERIFIER:
        "b069bc640d6bcf7d6eb16570d5844ce88504e00abc587cee958b59a775c68cdf",
}

EXPECTED_PRODUCER_SHA256 = (
    "4b867ad8acf8ea8ff7ca1b2a0b0e510fcef1f7a22a31eccb30f2d2bc97644abe"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "adbdcc3ffbd791126dd759a5699bf65902ebb8529b173db52e4b45e5f299494e"
)
EXPECTED_CERTIFICATE_RESULT_SHA256 = (
    "1544a7b865df882bab92dbec333e723fea28dd382567945e09ad609e7a811201"
)
R164_RESULT = "0f6d7f47ac20734ed294dd04cd7720ccbb9c0a1d4236980f814dd2ea2d5e79d9"
R164_VER_RESULT = "bb2e51bdbbd457a5782038efc527000cbf89b73c8645fd6facd126fa453af8c4"
R165_RESULT = "93e2899d0a9a79a82e1b193158f3733e891e2c5b4c9ce83f970aff40bf75c270"
R165_VER_RESULT = "86356b4b778fc8e2f74ab1edec30c96346027a9c17ade38c6f5aef269d6e5786"
R166_STATS_RESULT = "6972926f909815e041842fe5582f89898d1589ab69b54a801f5e28fdfa19e548"
R166_VER_RESULT = "bf88161e1310db2dc3531e300b0a20af9b7f1c008c0909824b8bfcf64b14097f"


class VerificationError(RuntimeError):
    """Fail-closed verification error."""


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
            require(type(key) is str, f"JSON key type:{path}")
            require("\x00" not in key, f"NUL key:{path}")
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


def validate_admitted_inputs(
    docs: dict[str, dict[str, Any]],
) -> dict[str, int]:
    r164 = docs[R164_CERT]
    v164 = docs[R164_VER]
    require(
        r164["schema"]
        == "cm2.round164.dimension-safe-tangency-graph-typing.v2",
        "Round164 schema",
    )
    require(r164["result_sha256"] == R164_RESULT, "Round164 result")
    require(v164["result_sha256"] == R164_VER_RESULT, "Round164 verification")
    require(v164["result"]["status"] == "PASS", "Round164 PASS")
    require(
        v164["result"]["certificate_result_sha256"] == R164_RESULT,
        "Round164 verified certificate",
    )
    ambient = r164["result"]["ambient_frozen_prefix_census"]
    expected_ambient = {
        "prior_recordwise_excluded_ambient_leaf_count": 37480,
        "remaining_ambient_unresolved_leaf_count": 39348,
        "remaining_prefix_stage_one_match": 518,
        "remaining_outgoing_chart_seam_unresolved": 618,
        "remaining_tangency_ambient_leaf_bulk": 32,
        "remaining_multi_candidate": 38180,
        "component_sum": 39348,
        "new_full_dimensional_ambient_leaf_exclusion_count": 0,
    }
    for key, expected in expected_ambient.items():
        require(ambient[key] == expected, f"Round164 ambient:{key}")

    r165 = docs[R165_CERT]
    v165 = docs[R165_VER]
    require(
        r165["schema"]
        == "cm2.round165.adaptive-typed-seam-census.prototype.v1",
        "Round165 schema",
    )
    require(r165["result_sha256"] == R165_RESULT, "Round165 result")
    require(v165["result_sha256"] == R165_VER_RESULT, "Round165 verification")
    v165r = v165["result"]
    require(v165r["status"] == "PASS", "Round165 PASS")
    require(
        v165r["certificate_result_sha256"] == R165_RESULT,
        "Round165 verified certificate",
    )
    for key in (
        "full_document_exactly_matched",
        "recursive_exact_key_tree_matched",
        "all_618_seam_parents_reconstructed",
        "all_622_terminal_records_reconstructed",
        "all_280_three_stratum_partitions_recomputed",
    ):
        require(v165r[key] is True, f"Round165 verifier:{key}")
    require(
        v165r["round165_producer_imported_or_executed"] is False,
        "Round165 verifier independence",
    )
    require(
        v165r["semantic_attack_suite"]["all_rejected"] is True
        and v165r["strict_json_attack_suite"]["all_rejected"] is True,
        "Round165 attack suites",
    )
    seam = r165["result"]["adaptive_seam_census"]
    require(seam["input_parent_leaf_count"] == 618, "Round165 inputs")
    require(seam["terminal_record_count"] == 622, "Round165 terminals")
    require(
        seam["strict_mismatch_rectangle_count"] == 118,
        "Round165 whole mismatches",
    )
    require(
        seam["strict_match_rectangle_count"] == 224,
        "Round165 W rectangles",
    )
    require(seam["typed_graph_collar_count"] == 280, "Round165 collars")
    require(
        seam["typed_collar_whole_leaf_exclusion_count"] == 0,
        "Round165 collar noncredit",
    )
    require(
        seam["adaptive_depth_limit_unresolved_count"] == 0
        and seam["all_618_inputs_semantically_chart_typed"] is True,
        "Round165 resolution",
    )
    require(
        seam["input_parent_resolution_counts"]
        == {
            "PARENT_WITH_DEPTH_LIMIT_RESIDUAL": 0,
            "PARENT_WITH_TYPED_SEAM_THREE_STRATUM_PARTITION": 280,
            "WHOLE_PARENT_OUTGOING_CHART_MISMATCH": 118,
            "WHOLE_PARENT_PREFIX_STAGE_ONE_MATCH": 220,
        },
        "Round165 parent partition",
    )
    refined = r165["result"]["refined_recordwise_census"]
    require(
        refined["round163_total_source_W_records"] == 76828
        and refined["round163_seam_parent_records_replaced"] == 618
        and refined["refined_total_records"] == 76832
        and refined["new_strict_mismatch_child_rectangles"] == 118
        and refined["refined_excluded_records"] == 37598
        and refined["refined_live_records"] == 39234,
        "Round165 refined ledger",
    )
    require(
        refined[
            "typed_analytic_strata_not_added_to_rectangular_record_count"
        ] is True
        and refined[
            "refined_live_records_is_conservative_rectangle_or_collar_count"
        ] is True,
        "Round165 dimension-safe ledger",
    )

    v166 = docs[R166_VER]
    require(
        v166["schema"]
        == (
            "cm2.round166.multi-candidate-refinement-prototype."
            "limited-independent-verification.v1"
        ),
        "Round166 schema",
    )
    require(v166["result_sha256"] == R166_VER_RESULT, "Round166 verification")
    v166r = v166["result"]
    require(
        v166r["status"]
        == "PASS_LIMITED_BASELINE_WITNESS_AND_CONSERVATION_VERIFICATION",
        "Round166 limited PASS",
    )
    require(v166r["producer_imported"] is False, "Round166 independence")
    require(
        v166r["certificate_result_sha256"] == R166_STATS_RESULT,
        "Round166 stats result provenance",
    )
    require(
        v166r["scope"]["six_level_refinement_tree_independently_replayed"]
        is False
        and v166r["scope"]["prototype_fully_promoted"] is False
        and v166r["scope"]["D02"] == "BLOCKED"
        and v166r["scope"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round166 limited scope",
    )
    immediate = v166r["independent_baseline_replay"]
    require(immediate["multi_candidate_count"] == 38180, "Round166 inputs")
    require(
        immediate["immediate_whole_parent_prefix_exclusion_count"] == 35564,
        "Round166 immediate exclusions",
    )
    require(
        immediate["owner_active_subdivision_input_count"] == 2616,
        "Round166 owner-active",
    )
    require(
        immediate["witness_types"]
        == {
            "owner_dominated_by_strict_future_root": 76,
            "owner_intersection_behind": 1178,
            "owner_no_real_intersection": 34310,
        },
        "Round166 witness partition",
    )
    require(
        sum(immediate["witness_types"].values()) == 35564
        and 35564 + 2616 == 38180,
        "Round166 independent conservation",
    )
    require(
        v166r["dependency_sha256"][
            "cm2_round166_multi_candidate_refinement_prototype.py"
        ] == "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c",
        "Round166 producer provenance",
    )
    require(
        v166r["dependency_sha256"][
            "cm2_round166_multi_candidate_refinement_prototype_stats.json"
        ] == "ffa028ff9e46219a48b3950a49a7c8f8d111fb54e7c3322aa4387366a2870999",
        "Round166 stats provenance",
    )
    return {
        "baseline_excluded": 37480,
        "baseline_remaining": 39348,
        "stage_one_match": 518,
        "seam_parents": 618,
        "tangency_bulk": 32,
        "multi_parents": 38180,
        "refined_total": 76832,
        "seam_whole_mismatch": 118,
        "seam_match_rectangles": 224,
        "seam_typed_collars": 280,
        "multi_immediate_excluded": 35564,
        "multi_owner_active": 2616,
    }


def independently_reconstruct_result(
    docs: dict[str, dict[str, Any]],
    producer_sha256: str,
) -> dict[str, Any]:
    values = validate_admitted_inputs(docs)
    baseline_rows = [
        closed_row({
            "class_id": "ROUND164_ALREADY_EXCLUDED",
            "ambient_parent_record_count": values["baseline_excluded"],
            "disposition": "EXCLUDED_BEFORE_ROUND165_REFINEMENT",
            "downstream_input": "NONE",
        }),
        closed_row({
            "class_id": "ROUND164_PREFIX_STAGE_ONE_MATCH",
            "ambient_parent_record_count": values["stage_one_match"],
            "disposition": "CONSERVATIVE_LIVE",
            "downstream_input": "LATER_FROZEN_PREFIX_STAGES",
        }),
        closed_row({
            "class_id": "ROUND164_OUTGOING_CHART_SEAM",
            "ambient_parent_record_count": values["seam_parents"],
            "disposition": "REPLACED_BY_ROUND165_TERMINALS",
            "downstream_input": "ROUND165",
        }),
        closed_row({
            "class_id": "ROUND164_TANGENCY_AMBIENT_BULK",
            "ambient_parent_record_count": values["tangency_bulk"],
            "disposition": "CONSERVATIVE_LIVE_OFF_GRAPH_BULK",
            "downstream_input": "TANGENCY_THREE_STRATUM_RECUT",
        }),
        closed_row({
            "class_id": "ROUND164_MULTI_CANDIDATE",
            "ambient_parent_record_count": values["multi_parents"],
            "disposition": "PARTITIONED_BY_ROUND166_IMMEDIATE_WITNESSES",
            "downstream_input": "ROUND166_LIMITED_BASELINE_ONLY",
        }),
    ]
    require(
        sum(row["ambient_parent_record_count"] for row in baseline_rows)
        == 76828,
        "Round164 full record partition",
    )

    credit_rows = [
        closed_row({
            "credit_id": "PRIOR_DIMENSION_SAFE_RECORDWISE_EXCLUSIONS",
            "whole_record_exclusion_count": values["baseline_excluded"],
            "source": R164_CERT,
            "scope": "ROUND164_V2_AMBIENT_BASELINE",
        }),
        closed_row({
            "credit_id": "ROUND165_WHOLE_RECTANGLE_SEAM_MISMATCH",
            "whole_record_exclusion_count": values["seam_whole_mismatch"],
            "source": R165_VER,
            "scope": "WHOLE_TERMINAL_RECTANGLES_ONLY",
        }),
        closed_row({
            "credit_id": "ROUND166_IMMEDIATE_WHOLE_PARENT_PREFIX_EXCLUSION",
            "whole_record_exclusion_count":
                values["multi_immediate_excluded"],
            "source": R166_VER,
            "scope": "IMMEDIATE_INDEPENDENT_BASELINE_WITNESSES_ONLY",
        }),
    ]
    combined_excluded = sum(
        row["whole_record_exclusion_count"] for row in credit_rows
    )
    require(combined_excluded == 73162, "combined whole-record credit")

    seam_live = (
        values["seam_match_rectangles"] + values["seam_typed_collars"]
    )
    live_rows = [
        closed_row({
            "live_id": "ORIGINAL_PREFIX_STAGE_ONE_MATCH",
            "conservative_live_record_or_composite_count":
                values["stage_one_match"],
            "kind": "WHOLE_PARENT_RECORD",
        }),
        closed_row({
            "live_id": "ROUND165_SEAM_LIVE_COMPOSITES",
            "conservative_live_record_or_composite_count": seam_live,
            "kind": "224_W_RECTANGLES_PLUS_280_TYPED_COLLAR_COMPOSITES",
        }),
        closed_row({
            "live_id": "ROUND164_TANGENCY_AMBIENT_BULK",
            "conservative_live_record_or_composite_count":
                values["tangency_bulk"],
            "kind": "WHOLE_PARENT_OFF_GRAPH_BULK",
        }),
        closed_row({
            "live_id": "ROUND166_OWNER_ACTIVE_MULTI",
            "conservative_live_record_or_composite_count":
                values["multi_owner_active"],
            "kind": "WHOLE_MULTI_PARENT_RECORD",
        }),
    ]
    conservative_live = sum(
        row["conservative_live_record_or_composite_count"]
        for row in live_rows
    )
    require(seam_live == 504, "seam live composites")
    require(conservative_live == 3670, "conservative live total")
    require(
        combined_excluded + conservative_live == values["refined_total"],
        "refined total conservation",
    )
    require(
        values["stage_one_match"]
        + values["seam_parents"]
        + values["tangency_bulk"]
        + values["multi_parents"]
        == values["baseline_remaining"],
        "disjoint Round164 remaining partition",
    )

    return {
        "status": (
            "CERTIFIED_DIMENSION_SAFE_SOURCE_W_COMBINED_STAGE_ONE_LEDGER__"
            "D02_STILL_BLOCKED"
        ),
        "record_space": {
            "Round164_original_source_W_record_count": 76828,
            "Round165_seam_parent_records_replaced": 618,
            "Round165_terminal_rectangle_or_collar_count": 622,
            "Round165_refinement_record_delta": 4,
            "refined_source_W_record_count": values["refined_total"],
        },
        "Round164_disjoint_baseline_partition": {
            "rows": baseline_rows,
            "rows_sha256": digest(baseline_rows),
            "pairwise_disjoint_by_pinned_classification": True,
            "remaining_component_sum": values["baseline_remaining"],
            "full_record_space_sum": 76828,
        },
        "admitted_whole_record_credit": {
            "rows": credit_rows,
            "rows_sha256": digest(credit_rows),
            "three_credit_blocks_pairwise_disjoint": True,
            "prior_recordwise_excluded": values["baseline_excluded"],
            "Round165_new_whole_rectangle_excluded":
                values["seam_whole_mismatch"],
            "Round166_new_immediate_whole_parent_excluded":
                values["multi_immediate_excluded"],
            "combined_whole_record_excluded": combined_excluded,
        },
        "conservative_live_ledger": {
            "rows": live_rows,
            "rows_sha256": digest(live_rows),
            "original_stage_one_match": values["stage_one_match"],
            "Round165_seam_live_composites": seam_live,
            "Round165_seam_live_breakdown": {
                "whole_W_rectangles": values["seam_match_rectangles"],
                "typed_collar_composites": values["seam_typed_collars"],
                "typed_collar_counting_rule":
                    "one conservative live composite per collar",
            },
            "tangency_ambient_bulk": values["tangency_bulk"],
            "owner_active_multi": values["multi_owner_active"],
            "conservative_live_total": conservative_live,
        },
        "dimension_safe_noncredit": {
            "Round164_typed_tangency_graph_whole_parent_credit": 0,
            "Round165_typed_collar_mismatch_open_side_whole_record_credit": 0,
            "Round165_typed_collar_count": values["seam_typed_collars"],
            "Round165_typed_collar_remains_one_live_composite_each": True,
            "Round166_deep_refinement_profile_imported": False,
            "Round166_deep_refinement_profile_whole_record_credit": 0,
            "Round166_limited_scope_six_level_tree_independently_replayed":
                False,
            "Round166_limited_scope_prototype_fully_promoted": False,
        },
        "conservation": {
            "refined_total": values["refined_total"],
            "whole_record_excluded": combined_excluded,
            "conservative_live": conservative_live,
            "excluded_plus_live_equals_refined_total": True,
            "identity": "73162+3670=76832",
        },
        "upstream_verified_chain": {
            "Round164_v2": {
                "certificate_result_sha256": R164_RESULT,
                "verification_result_sha256": R164_VER_RESULT,
                "status": "PASS",
            },
            "Round165_full": {
                "certificate_result_sha256": R165_RESULT,
                "verification_result_sha256": R165_VER_RESULT,
                "status": "PASS",
                "full_document_exactly_matched": True,
            },
            "Round166_limited": {
                "stats_result_sha256": R166_STATS_RESULT,
                "verification_result_sha256": R166_VER_RESULT,
                "status":
                    "PASS_LIMITED_BASELINE_WITNESS_AND_CONSERVATION_VERIFICATION",
                "only_immediate_independent_baseline_consumed": True,
            },
        },
        "scope": {
            "source_obstacle": "W",
            "frozen_collision_index": 1,
            "frozen_owner": "W[1,0]",
            "frozen_outgoing_chart": "W",
            "stage_one_only": True,
            "not_later_prefix_resolution": True,
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
            "continue later frozen-prefix stages on the 224 whole-W "
            "rectangles; first materialize and separately ledger each of the "
            "280 collars as its W-open side, adjacent mismatch side, and "
            "W-owned graph, then continue later-prefix resolution only on "
            "live strata; materialize the 32 tangency ambient recuts; and "
            "resolve the 2,616 owner-active multi parents without unverified "
            "deep-profile credit"
        ),
        "provenance": {
            "schema": CERTIFICATE_SCHEMA,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "admitted_input_documents": [
                R164_CERT,
                R164_VER,
                R165_CERT,
                R165_VER,
                R166_VER,
            ],
            "verification_source_pins": [R165_VERIFIER, R166_VERIFIER],
            "Round166_stats_or_producer_opened_by_Round168": False,
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
        "certificate result digest",
    )
    require(
        document["result_sha256"] == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "frozen certificate result digest",
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
    attacks: dict[str, Callable[[dict[str, Any]], None]] = {
        "schema": lambda d: d.__setitem__("schema", "mutated"),
        "status": lambda d: d["result"].__setitem__("status", "PASS"),
        "record total": lambda d: d["result"]["record_space"].__setitem__(
            "refined_source_W_record_count", 76831
        ),
        "seam replacement": lambda d: d["result"]["record_space"].__setitem__(
            "Round165_seam_parent_records_replaced", 617
        ),
        "terminal record count":
            lambda d: d["result"]["record_space"].__setitem__(
                "Round165_terminal_rectangle_or_collar_count", 621
            ),
        "refinement record delta":
            lambda d: d["result"]["record_space"].__setitem__(
                "Round165_refinement_record_delta", 3
            ),
        "baseline row count":
            lambda d: d["result"]["Round164_disjoint_baseline_partition"][
                "rows"
            ][0].__setitem__("ambient_parent_record_count", 37479),
        "baseline row digest":
            lambda d: d["result"]["Round164_disjoint_baseline_partition"][
                "rows"
            ][0].__setitem__("row_sha256", "0" * 64),
        "baseline rows digest":
            lambda d: d["result"][
                "Round164_disjoint_baseline_partition"
            ].__setitem__("rows_sha256", "0" * 64),
        "baseline disjointness":
            lambda d: d["result"][
                "Round164_disjoint_baseline_partition"
            ].__setitem__("pairwise_disjoint_by_pinned_classification", False),
        "prior credit":
            lambda d: d["result"]["admitted_whole_record_credit"].__setitem__(
                "prior_recordwise_excluded", 37479
            ),
        "Round165 mismatch credit":
            lambda d: d["result"]["admitted_whole_record_credit"].__setitem__(
                "Round165_new_whole_rectangle_excluded", 398
            ),
        "Round166 immediate credit":
            lambda d: d["result"]["admitted_whole_record_credit"].__setitem__(
                "Round166_new_immediate_whole_parent_excluded", 167984
            ),
        "combined exclusion":
            lambda d: d["result"]["admitted_whole_record_credit"].__setitem__(
                "combined_whole_record_excluded", 205582
            ),
        "credit blocks disjoint":
            lambda d: d["result"]["admitted_whole_record_credit"].__setitem__(
                "three_credit_blocks_pairwise_disjoint", False
            ),
        "credit row source":
            lambda d: d["result"]["admitted_whole_record_credit"]["rows"][
                2
            ].__setitem__(
                "source",
                "cm2_round166_multi_candidate_refinement_prototype_stats.json",
            ),
        "credit row scope":
            lambda d: d["result"]["admitted_whole_record_credit"]["rows"][
                2
            ].__setitem__("scope", "SIX_LEVEL_PROFILE"),
        "credit rows digest":
            lambda d: d["result"]["admitted_whole_record_credit"].__setitem__(
                "rows_sha256", "0" * 64
            ),
        "stage-one live":
            lambda d: d["result"]["conservative_live_ledger"].__setitem__(
                "original_stage_one_match", 517
            ),
        "seam live total":
            lambda d: d["result"]["conservative_live_ledger"].__setitem__(
                "Round165_seam_live_composites", 784
            ),
        "W rectangle live":
            lambda d: d["result"]["conservative_live_ledger"][
                "Round165_seam_live_breakdown"
            ].__setitem__("whole_W_rectangles", 223),
        "typed collar count":
            lambda d: d["result"]["conservative_live_ledger"][
                "Round165_seam_live_breakdown"
            ].__setitem__("typed_collar_composites", 560),
        "typed collar counting rule":
            lambda d: d["result"]["conservative_live_ledger"][
                "Round165_seam_live_breakdown"
            ].__setitem__(
                "typed_collar_counting_rule",
                "two full-dimensional open sides per collar",
            ),
        "tangency live":
            lambda d: d["result"]["conservative_live_ledger"].__setitem__(
                "tangency_ambient_bulk", 0
            ),
        "owner-active live":
            lambda d: d["result"]["conservative_live_ledger"].__setitem__(
                "owner_active_multi", 0
            ),
        "live total":
            lambda d: d["result"]["conservative_live_ledger"].__setitem__(
                "conservative_live_total", 3390
            ),
        "live row kind":
            lambda d: d["result"]["conservative_live_ledger"]["rows"][
                1
            ].__setitem__(
                "kind", "224_W_RECTANGLES_PLUS_560_OPEN_SIDES"
            ),
        "live row count":
            lambda d: d["result"]["conservative_live_ledger"]["rows"][
                1
            ].__setitem__(
                "conservative_live_record_or_composite_count", 784
            ),
        "live row digest":
            lambda d: d["result"]["conservative_live_ledger"]["rows"][
                1
            ].__setitem__("row_sha256", "0" * 64),
        "live rows digest":
            lambda d: d["result"]["conservative_live_ledger"].__setitem__(
                "rows_sha256", "0" * 64
            ),
        "tangency graph credit":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "Round164_typed_tangency_graph_whole_parent_credit", 32
            ),
        "collar mismatch-side credit":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "Round165_typed_collar_mismatch_open_side_whole_record_credit",
                280,
            ),
        "collar composite guard":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "Round165_typed_collar_remains_one_live_composite_each", False
            ),
        "deep profile imported":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "Round166_deep_refinement_profile_imported", True
            ),
        "deep profile credit":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "Round166_deep_refinement_profile_whole_record_credit", 167984
            ),
        "six-level replay":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "Round166_limited_scope_six_level_tree_independently_replayed",
                True,
            ),
        "prototype promotion":
            lambda d: d["result"]["dimension_safe_noncredit"].__setitem__(
                "Round166_limited_scope_prototype_fully_promoted", True
            ),
        "conservation excluded":
            lambda d: d["result"]["conservation"].__setitem__(
                "whole_record_excluded", 73163
            ),
        "conservation live":
            lambda d: d["result"]["conservation"].__setitem__(
                "conservative_live", 3669
            ),
        "conservation identity":
            lambda d: d["result"]["conservation"].__setitem__(
                "identity", "73163+3669=76832"
            ),
        "Round164 chain":
            lambda d: d["result"]["upstream_verified_chain"][
                "Round164_v2"
            ].__setitem__("status", "FAIL"),
        "Round165 chain":
            lambda d: d["result"]["upstream_verified_chain"][
                "Round165_full"
            ].__setitem__("full_document_exactly_matched", False),
        "Round166 limited status":
            lambda d: d["result"]["upstream_verified_chain"][
                "Round166_limited"
            ].__setitem__("status", "PASS"),
        "Round166 limited consumption":
            lambda d: d["result"]["upstream_verified_chain"][
                "Round166_limited"
            ].__setitem__("only_immediate_independent_baseline_consumed", False),
        "source obstacle":
            lambda d: d["result"]["scope"].__setitem__("source_obstacle", "G"),
        "stage-one scope":
            lambda d: d["result"]["scope"].__setitem__(
                "stage_one_only", False
            ),
        "D02 promotion":
            lambda d: d["result"]["strict_nonpromotion"].__setitem__(
                "D02", "CLOSED"
            ),
        "CM2 promotion":
            lambda d: d["result"]["strict_nonpromotion"].__setitem__(
                "CM2", "GO"
            ),
        "Gate5 promotion":
            lambda d: d["result"]["strict_nonpromotion"].__setitem__(
                "global_Gate5_fields", "18/18"
            ),
        "producer pin":
            lambda d: d["result"]["provenance"].__setitem__(
                "producer_sha256", "0" * 64
            ),
        "dependency pin":
            lambda d: d["result"]["provenance"]["dependency_sha256"].__setitem__(
                R166_VER, "0" * 64
            ),
        "admit Round166 stats":
            lambda d: d["result"]["provenance"][
                "admitted_input_documents"
            ].append("cm2_round166_multi_candidate_refinement_prototype_stats.json"),
        "claim Round166 profile opened":
            lambda d: d["result"]["provenance"].__setitem__(
                "Round166_stats_or_producer_opened_by_Round168", True
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
    scratch = Path(tempfile.mkdtemp(prefix=".cm2_round168_path_attack.", dir=HERE))
    symlink_output = HERE / f".cm2_round168_symlink_output.{os.getpid()}"
    hard_output_base = HERE / f".cm2_round168_hard_output_base.{os.getpid()}"
    hard_output_link = HERE / f".cm2_round168_hard_output_link.{os.getpid()}"
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


def build_verification(
    certificate_path: Path,
) -> dict[str, Any]:
    docs = {
        name: load_pinned(name)
        for name in (R164_CERT, R164_VER, R165_CERT, R165_VER, R166_VER)
    }
    for name in (R165_VERIFIER, R166_VERIFIER):
        read_regular(HERE / name, PINS[name])
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
            "Round168_producer_imported": False,
            "Round168_producer_executed": False,
            "full_result_independently_reconstructed": True,
            "full_expected_canonical_equality": True,
            "recursive_exact_key_tree_matched": True,
            "Round164_baseline_replayed_from_pinned_verified_certificate": True,
            "Round165_dimension_safe_counts_replayed_from_full_verification":
                True,
            "Round166_only_limited_independent_immediate_baseline_consumed":
                True,
            "Round166_stats_opened": False,
            "Round166_producer_opened": False,
            "Round166_six_level_tree_independently_replayed": False,
            "Round166_prototype_fully_promoted": False,
        },
        "recomputed_ledger": {
            "refined_source_W_record_count": 76832,
            "three_disjoint_whole_record_credit_blocks": [37480, 118, 35564],
            "combined_whole_record_excluded": 73162,
            "conservative_live_components": [518, 504, 32, 2616],
            "conservative_live_total": 3670,
            "Round165_seam_live_breakdown": [224, 280],
            "each_typed_collar_counts_as_one_live_composite": True,
            "typed_collar_mismatch_side_whole_record_credit": 0,
            "Round166_deep_profile_whole_record_credit": 0,
            "conservation_identity": "73162+3670=76832",
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
    data = canonical_bytes(verification) + b"\n"
    protected = {(HERE / name).resolve() for name in PINS}
    protected.update({
        PRODUCER.resolve(),
        Path(__file__).resolve(),
        arguments.certificate.resolve(),
    })
    safe_atomic_write(arguments.output, data, protected)
    print(verification["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
