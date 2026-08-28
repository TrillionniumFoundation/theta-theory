#!/usr/bin/env python3
"""Compose the dimension-safe source-W frozen stage-one ledger.

Only three independently verified credit blocks are admitted:

* the Round164-v2 ambient baseline;
* Round165 whole-rectangle seam mismatch credit;
* Round166 immediate whole-parent multi-candidate exclusions.

Round165 mismatch open sides inside typed collars and every Round166 deeper
profiling statistic receive zero whole-record credit.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = (
    HERE / "cm2_round168_dimension_safe_source_W_stage_one_ledger_certificate.json"
)
SCHEMA = "cm2.round168.dimension-safe-source-W-stage-one-ledger.v1"
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

R164_RESULT = "0f6d7f47ac20734ed294dd04cd7720ccbb9c0a1d4236980f814dd2ea2d5e79d9"
R164_VER_RESULT = "bb2e51bdbbd457a5782038efc527000cbf89b73c8645fd6facd126fa453af8c4"
R165_RESULT = "93e2899d0a9a79a82e1b193158f3733e891e2c5b4c9ce83f970aff40bf75c270"
R165_VER_RESULT = "86356b4b778fc8e2f74ab1edec30c96346027a9c17ade38c6f5aef269d6e5786"
R166_STATS_RESULT = "6972926f909815e041842fe5582f89898d1589ab69b54a801f5e28fdfa19e548"
R166_VER_RESULT = "bf88161e1310db2dc3531e300b0a20af9b7f1c008c0909824b8bfcf64b14097f"


class LedgerError(RuntimeError):
    """Fail-closed composition error."""


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
        raise LedgerError(label)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_float(value: str) -> None:
    raise LedgerError(f"non-integer JSON number:{value}")


def read_regular(path: Path, expected_sha256: str) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"not regular:{path.name}")
    require(not path.is_symlink(), f"symlink rejected:{path.name}")
    require(st.st_nlink == 1, f"multiply linked rejected:{path.name}")
    require(st.st_size <= MAX_INPUT_BYTES, f"oversized:{path.name}")
    data = path.read_bytes()
    require(sha256_bytes(data) == expected_sha256, f"pin:{path.name}")
    return data


def parse_envelope(data: bytes, label: str) -> dict[str, Any]:
    require(not data.startswith(b"\xef\xbb\xbf"), f"BOM:{label}")
    require(b"\x00" not in data, f"NUL:{label}")
    try:
        value = json.loads(
            data.decode("utf-8", "strict"),
            object_pairs_hook=reject_duplicate_keys,
            parse_float=reject_float,
            parse_constant=reject_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LedgerError(f"invalid JSON:{label}:{exc}") from exc
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


def validate_inputs(
    docs: dict[str, dict[str, Any]],
) -> dict[str, int]:
    r164 = docs[R164_CERT]
    v164 = docs[R164_VER]
    require(
        r164["schema"]
        == "cm2.round164.dimension-safe-tangency-graph-typing.v2"
        and r164["result_sha256"] == R164_RESULT
        and v164["result_sha256"] == R164_VER_RESULT
        and v164["result"]["status"] == "PASS"
        and v164["result"]["certificate_result_sha256"] == R164_RESULT,
        "Round164-v2 verified chain",
    )
    ambient = r164["result"]["ambient_frozen_prefix_census"]
    require(
        ambient["prior_recordwise_excluded_ambient_leaf_count"] == 37480
        and ambient["remaining_ambient_unresolved_leaf_count"] == 39348
        and ambient["remaining_prefix_stage_one_match"] == 518
        and ambient["remaining_outgoing_chart_seam_unresolved"] == 618
        and ambient["remaining_tangency_ambient_leaf_bulk"] == 32
        and ambient["remaining_multi_candidate"] == 38180
        and ambient["component_sum"] == 39348
        and ambient["new_full_dimensional_ambient_leaf_exclusion_count"] == 0,
        "Round164-v2 ambient baseline",
    )

    r165 = docs[R165_CERT]
    v165 = docs[R165_VER]
    require(
        r165["schema"]
        == "cm2.round165.adaptive-typed-seam-census.prototype.v1"
        and r165["result_sha256"] == R165_RESULT
        and v165["result_sha256"] == R165_VER_RESULT
        and v165["result"]["status"] == "PASS"
        and v165["result"]["certificate_result_sha256"] == R165_RESULT
        and v165["result"]["round165_producer_imported_or_executed"] is False
        and v165["result"]["full_document_exactly_matched"] is True
        and v165["result"]["recursive_exact_key_tree_matched"] is True
        and v165["result"]["all_618_seam_parents_reconstructed"] is True
        and v165["result"]["all_622_terminal_records_reconstructed"] is True
        and v165["result"]["all_280_three_stratum_partitions_recomputed"]
        is True
        and v165["result"]["semantic_attack_suite"]["all_rejected"] is True
        and v165["result"]["strict_json_attack_suite"]["all_rejected"] is True,
        "Round165 full independent verification",
    )
    seam = r165["result"]["adaptive_seam_census"]
    refined = r165["result"]["refined_recordwise_census"]
    require(
        seam["input_parent_leaf_count"] == 618
        and seam["terminal_record_count"] == 622
        and seam["strict_mismatch_rectangle_count"] == 118
        and seam["strict_match_rectangle_count"] == 224
        and seam["typed_graph_collar_count"] == 280
        and seam["typed_collar_whole_leaf_exclusion_count"] == 0
        and seam["adaptive_depth_limit_unresolved_count"] == 0
        and seam["all_618_inputs_semantically_chart_typed"] is True
        and seam["input_parent_resolution_counts"]
        == {
            "PARENT_WITH_DEPTH_LIMIT_RESIDUAL": 0,
            "PARENT_WITH_TYPED_SEAM_THREE_STRATUM_PARTITION": 280,
            "WHOLE_PARENT_OUTGOING_CHART_MISMATCH": 118,
            "WHOLE_PARENT_PREFIX_STAGE_ONE_MATCH": 220,
        }
        and refined["round163_total_source_W_records"] == 76828
        and refined["round163_seam_parent_records_replaced"] == 618
        and refined["refined_total_records"] == 76832
        and refined["new_strict_mismatch_child_rectangles"] == 118
        and refined["refined_excluded_records"] == 37598
        and refined["refined_live_records"] == 39234
        and refined[
            "typed_analytic_strata_not_added_to_rectangular_record_count"
        ] is True
        and refined[
            "refined_live_records_is_conservative_rectangle_or_collar_count"
        ] is True,
        "Round165 dimension-safe seam ledger",
    )

    v166 = docs[R166_VER]
    require(
        v166["schema"]
        == (
            "cm2.round166.multi-candidate-refinement-prototype."
            "limited-independent-verification.v1"
        )
        and v166["result_sha256"] == R166_VER_RESULT
        and v166["result"]["status"]
        == "PASS_LIMITED_BASELINE_WITNESS_AND_CONSERVATION_VERIFICATION"
        and v166["result"]["producer_imported"] is False
        and v166["result"]["certificate_result_sha256"] == R166_STATS_RESULT
        and v166["result"]["scope"][
            "six_level_refinement_tree_independently_replayed"
        ] is False
        and v166["result"]["scope"]["prototype_fully_promoted"] is False
        and v166["result"]["scope"]["D02"] == "BLOCKED"
        and v166["result"]["scope"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round166 limited verification scope",
    )
    immediate = v166["result"]["independent_baseline_replay"]
    require(
        immediate["multi_candidate_count"] == 38180
        and immediate["immediate_whole_parent_prefix_exclusion_count"]
        == 35564
        and immediate["owner_active_subdivision_input_count"] == 2616
        and immediate["witness_types"]
        == {
            "owner_dominated_by_strict_future_root": 76,
            "owner_intersection_behind": 1178,
            "owner_no_real_intersection": 34310,
        }
        and sum(immediate["witness_types"].values()) == 35564
        and 35564 + 2616 == 38180,
        "Round166 independently replayed immediate census",
    )
    require(
        v166["result"]["dependency_sha256"][
            "cm2_round166_multi_candidate_refinement_prototype.py"
        ] == "6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c"
        and v166["result"]["dependency_sha256"][
            "cm2_round166_multi_candidate_refinement_prototype_stats.json"
        ] == "ffa028ff9e46219a48b3950a49a7c8f8d111fb54e7c3322aa4387366a2870999",
        "Round166 stable upstream provenance",
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


def build_result(
    docs: dict[str, dict[str, Any]],
    producer_sha256: str,
) -> dict[str, Any]:
    values = validate_inputs(docs)
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
        "Round164 total",
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
            "whole_record_exclusion_count": values["multi_immediate_excluded"],
            "source": R166_VER,
            "scope": "IMMEDIATE_INDEPENDENT_BASELINE_WITNESSES_ONLY",
        }),
    ]
    combined_excluded = sum(
        row["whole_record_exclusion_count"] for row in credit_rows
    )
    require(combined_excluded == 73162, "combined excluded")

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
    require(
        seam_live == 504
        and conservative_live == 3670
        and combined_excluded + conservative_live == values["refined_total"],
        "refined conservation",
    )
    require(
        values["stage_one_match"]
        + values["seam_parents"]
        + values["tangency_bulk"]
        + values["multi_parents"]
        == values["baseline_remaining"],
        "baseline disjoint partition",
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
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "admitted_input_documents": [
                R164_CERT,
                R164_VER,
                R165_CERT,
                R165_VER,
                R166_VER,
            ],
            "verification_source_pins": [
                R165_VERIFIER,
                R166_VERIFIER,
            ],
            "Round166_stats_or_producer_opened_by_Round168": False,
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
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()
    docs = {
        name: load_pinned(name)
        for name in (R164_CERT, R164_VER, R165_CERT, R165_VER, R166_VER)
    }
    # Pin the independent verifier sources without importing or executing them.
    for name in (R165_VERIFIER, R166_VERIFIER):
        read_regular(HERE / name, PINS[name])
    producer_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result = build_result(docs, producer_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    data = canonical_bytes(envelope) + b"\n"
    protected = {(HERE / name).resolve() for name in PINS}
    protected.add(Path(__file__).resolve())
    safe_atomic_write(arguments.output, data, protected)
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
