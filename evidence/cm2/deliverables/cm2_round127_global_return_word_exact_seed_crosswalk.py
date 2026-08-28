#!/usr/bin/env python3
"""Round127 fail-closed global-registry/exact-seed crosswalk.

The frozen Gate5 return-word manifest declares 441,280 immutable symbolic
candidate word keys and 3,286,976 symbolic word/roof positions.  Round113
materializes one verified rank-three path used later by Round121--Round126.
This producer pins and strictly parses those artifacts and records the exact
join:

* three Round113 official word rows are members of the symbolic registry;
* the path has five symbolic word/roof positions (return lengths 2, 1, 2);
* Round121 refines one exact seed into 24 half-open common children;
* Round126 binds the three words to 72 word/subbranch operator carriers,
  120 seed-local word/subbranch/roof base keys, and 2,160 exact-once
  seed-local field slots.

The resulting 3/441280 and 5/3286976 numbers are registry incidence counts,
not domain, measure, or physical coverage ratios.  The 120 local base keys
contain an additional exact-seed subbranch coordinate and therefore are not
divided by the global symbolic word/roof count.  No seed-local level or packet
is promoted to a global Gate5 block.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round127.global-return-word-exact-seed-crosswalk.v1"
OUTPUT = (
    HERE
    / "cm2-round127-global-return-word-exact-seed-crosswalk-2026-07-24.json"
)

GLOBAL_MANIFEST = (
    HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
)
ROUND113 = (
    HERE
    / "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
)
ROUND113_VERIFICATION = (
    HERE
    / "cm2-round113-rank3-endpoint-sheet-owner-ordering-verification-2026-07-23.json"
)
ROUND117 = (
    HERE
    / "cm2-round117-rank3-countable-homogeneity-operator-cells-2026-07-23.json"
)
ROUND117_VERIFICATION = (
    HERE
    / "cm2-round117-rank3-countable-homogeneity-operator-cells-verification-2026-07-23.json"
)
ROUND121 = (
    HERE
    / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
)
ROUND121_VERIFICATION = (
    HERE
    / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json"
)
ROUND126 = (
    HERE
    / "cm2-round126-rank3-exact-seed-operator-phase-block-f18-2026-07-23.json"
)
ROUND126_VERIFICATION = (
    HERE
    / "cm2-round126-rank3-exact-seed-operator-phase-block-f18-verification-2026-07-23.json"
)

BYTE_PINS = {
    GLOBAL_MANIFEST.name:
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    ROUND113.name:
        "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181",
    ROUND113_VERIFICATION.name:
        "bcd3f5ddf1763d58a256b117a757f3db076d03b1b7a8441c34dfa7b467a55bc0",
    ROUND117.name:
        "31b6535e21886d825d5a4658f2c9d3ccc8c5525c2b9d2fb181f88baa7dcf9eb0",
    ROUND117_VERIFICATION.name:
        "06647b5b6f81ad0e8098f5885e9aa2b2c926991faaa34102e0646c058da0764f",
    ROUND121.name:
        "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e",
    ROUND121_VERIFICATION.name:
        "ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80",
    ROUND126.name:
        "5980d0714aade1d71b32d3fa280d157e98dc97cefca2dd1e8e614f5203a8897e",
    ROUND126_VERIFICATION.name:
        "bfbee771cc25cfb623297fe5e5c63483cbd296c372c1c4a143b247c834046f4b",
}

SCHEMAS = {
    ROUND113.name: "cm2.round113.rank3-endpoint-sheet-owner-ordering.v1",
    ROUND113_VERIFICATION.name:
        "cm2.round113.rank3-endpoint-sheet-owner-ordering.verification.v1",
    ROUND117.name:
        "cm2.round117.rank3-countable-homogeneity-operator-cells.v1",
    ROUND117_VERIFICATION.name:
        "cm2.round117.rank3-countable-homogeneity-operator-cells-verification.v1",
    ROUND121.name:
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
    ROUND121_VERIFICATION.name:
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6-verification.v1",
    ROUND126.name:
        "cm2.round126.rank3-exact-seed-operator-phase-block-f18.v1",
    ROUND126_VERIFICATION.name:
        "cm2.round126.rank3-exact-seed-operator-phase-block-f18-verification.v1",
}

RESULT_PINS = {
    ROUND113.name:
        "33f564bd6afea1ba346ed0048a4bc61fa1a1bf91ebbbac546a32b051643bda67",
    ROUND113_VERIFICATION.name:
        "c87d20aee8d652f45a52ca4bd8e9b58753de536036ec6373b2067ef381c972b9",
    ROUND117.name:
        "d8e759c9397c595a011476661cb6144130f708116198886645366288788d2b0f",
    ROUND117_VERIFICATION.name:
        "eb2f83bbf6b0a08e2b803e40b7422688339852eae3f840c6936ac0cd56e769d2",
    ROUND121.name:
        "962db517d76b18e7681c411734b568491e600776dbf5317d9ebff8494a9aebd8",
    ROUND121_VERIFICATION.name:
        "8c830e2e26d9b4cce6f034ad382420bf7c7aac0b422979b14e88888fe1b888e5",
    ROUND126.name:
        "0a15b8afe9e6434fa2766ffa55159b5f7944eb7d2a3d3a39a31d67261effd63a",
    ROUND126_VERIFICATION.name:
        "6ac2ff5a80d08b1e0a133599ca35836bd087b9c8a831ce9128a7225c0dba63fd",
}

GLOBAL_PRODUCER_SHA256 = (
    "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695"
)
GLOBAL_VERIFIER_SHA256 = (
    "0384acdd1f912b0d4b3bee84ff530358d9693893d1c5c64a1deabaede8e0867b"
)
GLOBAL_WORD_ROWS_STREAM_SHA256 = (
    "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
)
GLOBAL_FIELD_SCHEMA_SHA256 = (
    "bc7f3bfd5ff896e5de853cfa6f96327ec21fb983359becb40da9526be98c51a5"
)

PARENT_ID = "round113-cell:08b7ca8449af5f6e8d4e3abce98803656664ed7ec957aba62406763b68b2fea6"
SHEET_ID = "round112-bypass-sheet:82388860fd9a24f85561682533f70ba8789125b13ea29deb027aa3bcb293201f"
PATH_ID = "gate5-rank3-endpoint-sheet-path:9f335e832599b906ffef1f29b1751e5250309a48501b948598115a92ac44b5f7"
OPERATOR_CELL_ID = (
    "round117-operator-cell:dca0117235e58b6a0cbc8b9db55ed846b8f26939041fa7eaffd3b68184d54ae1"
)
EXACT_SEED_ID = (
    "round121-exact-parent-W:41462c4f6815ad00fd5d4456e5c13885feeab5e8343b009b8872b72d15cf18c8"
)
EXPECTED_BRANCH = [7, "G[0,0]", "W[-1,-2]", 1]
EXPECTED_OWNERS = ["W[-1,-1]", "G[0,0]", "G[-1,-2]"]
EXPECTED_COLLISION_CHARTS = ["N", "S", "N"]
EXPECTED_RELATIVE_TARGETS = ["W[-1,-1]", "G[1,1]", "G[-1,-2]"]
EXPECTED_WORDS = [
    {
        "ordinal_zero_based": 102441,
        "retained_chart_target_pair_ordinal_zero_based": 104,
        "crossing_pattern_ordinal_zero_based": 1,
        "row": ["G:W", "W[-1,-1]", ["Y-"], 2],
        "row_sha256":
            "3ef7afa1895a984d7edeab7005cfcb7daed7ae8aa07f0767bdd9144da94749ba",
        "word_key_id":
            "gate5-word:102441:3ef7afa1895a984d7edeab7005cfcb7daed7ae8aa07f0767bdd9144da94749ba",
    },
    {
        "ordinal_zero_based": 346720,
        "retained_chart_target_pair_ordinal_zero_based": 352,
        "crossing_pattern_ordinal_zero_based": 0,
        "row": ["W:N", "G[1,1]", [], 1],
        "row_sha256":
            "53f03ff6fc716b0187c62b5e3cc7971c9e030686426d13ff5eee585f33daeb3e",
        "word_key_id":
            "gate5-word:346720:53f03ff6fc716b0187c62b5e3cc7971c9e030686426d13ff5eee585f33daeb3e",
    },
    {
        "ordinal_zero_based": 180256,
        "retained_chart_target_pair_ordinal_zero_based": 183,
        "crossing_pattern_ordinal_zero_based": 1,
        "row": ["G:S", "G[-1,-2]", ["Y-"], 2],
        "row_sha256":
            "564ba69e20fe29980fb28d97a50efa2326d024c92c36c930bdb4a2157c3335c8",
        "word_key_id":
            "gate5-word:180256:564ba69e20fe29980fb28d97a50efa2326d024c92c36c930bdb4a2157c3335c8",
    },
]

FIELD_NAMES = {
    1: "nonempty_or_empty_domain_proof",
    2: "physical_homogeneity_subbranch_table",
    3: "homogeneous_prefix_chart",
    4: "homogeneous_suffix_chart",
    5: "inverse_Jacobian_bound",
    6: "log_Jacobian_distortion_sum",
    7: "one_step_cut_growth_Z_sum",
    8: "face_transversality_lower",
    9: "face_C2_atlas_bound",
    10: "coarea_density_regular_bound",
    11: "dynamic_Holder_test_pullback_bound",
    12: "C1_face_trace_pullback_bound",
    13: "moving_boundary_DQ_current_and_two_traces",
    14: "regular_density_operator_cost",
    15: "standard_family_operator_cost",
    16: "flux_face_operator_cost",
    17: "dynamic_test_operator_cost",
    18: "operator_phase_block",
}
SOURCE_ROUND_BY_FIELD = {
    **{field: 121 for field in range(1, 7)},
    **{field: 122 for field in list(range(7, 14)) + [16]},
    14: 125,
    15: 125,
    17: 125,
    18: 126,
}
STAGE_RETURN_LENGTH = {0: 2, 1: 1, 2: 2}
ROOF_LEVELS_BY_STAGE = {0: [0, 1], 1: [0], 2: [0, 1]}
EXPECTED_BASE_STAGE_COUNTS = Counter({0: 48, 1: 24, 2: 48})


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def is_int(value: Any) -> bool:
    return type(value) is int


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_float(token: str) -> Any:
    raise ValueError(f"floating-point JSON token forbidden:{token}")


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key:{key}")
        value[key] = item
    return value


def strict_json(path: Path) -> Any:
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM:{path.name}")
    return json.loads(
        raw.decode("utf-8", errors="strict"),
        object_pairs_hook=strict_pairs,
        parse_float=reject_float,
        parse_constant=reject_float,
    )


def strict_document(path: Path) -> dict[str, Any]:
    document = strict_json(path)
    require(type(document) is dict, f"top-level object:{path.name}")
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"closed envelope:{path.name}",
    )
    require(document["schema"] == SCHEMAS[path.name], f"schema:{path.name}")
    require(type(document["result"]) is dict, f"result object:{path.name}")
    require(
        document["result_sha256"] == digest(document["result"]),
        f"result digest:{path.name}",
    )
    require(
        document["result_sha256"] == RESULT_PINS[path.name],
        f"result pin:{path.name}",
    )
    return document


def validate_payload_hashed_row(row: Any, label: str) -> None:
    require(type(row) is dict, f"{label}:object")
    require(type(row.get("row_sha256")) is str, f"{label}:row hash type")
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    require(row["row_sha256"] == digest(payload), f"{label}:row hash")


def row_id(prefix: str, payload: Any) -> str:
    return f"{prefix}:{digest([prefix, payload])}"


def verify_byte_pins() -> None:
    for name, expected in BYTE_PINS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"regular input:{name}")
        require(sha256(path) == expected, f"byte pin:{name}")


def validate_global_manifest(manifest: Any) -> dict[str, Any]:
    require(type(manifest) is dict, "global manifest object")
    require(
        set(manifest)
        == {
            "schema",
            "certificate_sha256",
            "verifier_sha256",
            "dependencies",
            "result",
            "verdict",
        },
        "global manifest closed top level",
    )
    require(
        manifest["schema"]
        == "cm2.gate5.return-word-three-norm-frontier.manifest.v1",
        "global manifest schema",
    )
    require(
        manifest["certificate_sha256"] == GLOBAL_PRODUCER_SHA256
        and manifest["verifier_sha256"] == GLOBAL_VERIFIER_SHA256,
        "global manifest embedded producer/verifier pins",
    )
    result = manifest["result"]
    require(
        type(result) is dict
        and result.get("schema")
        == "cm2.gate5.return-word-three-norm-frontier.v1",
        "global manifest result",
    )
    registry = result["immutable_candidate_key_registry"]
    factor = registry["prefix_suffix_factor_contract"]
    fields = result["required_operator_field_schema"]
    require(
        registry["candidate_return_word_key_count"] == 441280
        and registry["candidate_word_key_rows_sha256"]
        == GLOBAL_WORD_ROWS_STREAM_SHA256
        and registry["retained_chart_target_pair_count"] == 448
        and registry["crossing_pattern_count_per_pair"] == 985,
        "global word registry",
    )
    require(
        registry["roof_histogram"]
        == {
            "1": 448,
            "2": 1792,
            "3": 5376,
            "4": 12544,
            "5": 26880,
            "6": 53760,
            "7": 89600,
            "8": 125440,
            "9": 125440,
        },
        "global roof histogram",
    )
    require(
        factor["roof_level_prefix_suffix_factor_pair_count"] == 3286976
        and factor["roof_level_index"] == "0<=j<r(w)"
        and factor["symbolic_factorisation_complete_on_every_candidate_key"]
        is True
        and factor["homogeneous_subbranch_index_instantiated"] is False,
        "global symbolic roof registry",
    )
    require(
        fields["required_field_count_per_physical_homogeneous_level"] == 18
        and fields["required_fields"]
        == [FIELD_NAMES[field] for field in range(1, 19)]
        and fields["required_field_schema_sha256"]
        == GLOBAL_FIELD_SCHEMA_SHA256
        and fields["homogeneous_subbranch_ids_materialized"] is False
        and fields["all_required_fields_populated"] is False,
        "global 18-field schema",
    )
    require(
        registry["exact_nonempty_candidate_key_count"] is None
        and registry["complete_physical_operator_block_count"] == 0,
        "global unknown nonempty census and zero blocks",
    )
    completion = result["completion"]
    require(
        completion["complete_regular_return_word_candidate_key_envelope"] is True
        and completion["complete_nonempty_return_word_domain_decisions"] is False
        and completion["physical_homogeneous_subbranch_registry"] is False
        and completion["immutable_complete_return_word_operator_registry"] is False
        and completion["gate5_certified"] is False,
        "global fail-closed completion",
    )
    require(
        manifest["verdict"]["gate5"] == "NOT_CERTIFIED"
        and manifest["verdict"]["physical_homogeneous_operator_registry"]
        == "NOT_CERTIFIED",
        "global fail-closed verdict",
    )
    return result


def validate_verifications(
    documents: dict[str, dict[str, Any]],
) -> None:
    v113 = documents[ROUND113_VERIFICATION.name]["result"]
    v117 = documents[ROUND117_VERIFICATION.name]["result"]
    v121 = documents[ROUND121_VERIFICATION.name]["result"]
    v126 = documents[ROUND126_VERIFICATION.name]["result"]
    require(
        v113["verification_status"] == "PASS"
        and v113["certificate_sha256"] == BYTE_PINS[ROUND113.name]
        and v113["independent_verifier_does_not_import_round113_producer_or_engine"]
        is True,
        "Round113 verification PASS",
    )
    require(
        v117["verdict"] == "PASS"
        and v117["certificate_sha256"] == BYTE_PINS[ROUND117.name]
        and v117["producer_module_imported"] is False,
        "Round117 verification PASS",
    )
    require(
        v121["verdict"] == "PASS"
        and v121["certificate_sha256"] == BYTE_PINS[ROUND121.name]
        and v121["upstream_R113_R117_R120_seed_crosswalk_verified"] is True
        and v121["official_candidate_registry_rows_sha256"]
        == GLOBAL_WORD_ROWS_STREAM_SHA256
        and v121["independently_replayed_common_child_count"] == 24
        and v121["independently_replayed_refined_subbranch_count"] == 24
        and v121["independently_replayed_full_key_slot_count"] == 720,
        "Round121 verification PASS",
    )
    require(
        v126["status"] == "PASS"
        and v126["certificate_sha256"] == BYTE_PINS[ROUND126.name]
        and v126["certificate_result_sha256"] == RESULT_PINS[ROUND126.name]
        and v126["reconstructed_counts"]["actual_child_count"] == 24
        and v126["reconstructed_counts"]["preexisting_F1_F17_same_key_map_row_count"]
        == 120
        and v126["reconstructed_counts"]["rebuilt_preexisting_slot_count"]
        == 2040
        and v126["reconstructed_counts"]["F18_slot_count"] == 120
        and v126["reconstructed_counts"]["combined_child_local_slot_count"]
        == 2160,
        "Round126 verification PASS",
    )
    safety = v126["safety_state"]
    require(
        safety["rank3_seed_child_field_maturity"] == "18/18"
        and safety["seed_local_complete_18_field_level_block_count"] == 120
        and safety["seed_local_complete_18_field_child_packet_count"] == 24
        and safety["global_complete_18_field_block_count"] == 0
        and safety["complete_18_field_block_count"] == 0
        and safety["gate5_block_count"] == 0
        and safety["gate5_global_maturity"] == "10/18"
        and safety["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "Round126 verified safety state",
    )


def load_inputs() -> tuple[
    dict[str, Any],
    dict[str, dict[str, Any]],
]:
    verify_byte_pins()
    manifest = validate_global_manifest(strict_json(GLOBAL_MANIFEST))
    documents = {
        path.name: strict_document(path)
        for path in (
            ROUND113,
            ROUND113_VERIFICATION,
            ROUND117,
            ROUND117_VERIFICATION,
            ROUND121,
            ROUND121_VERIFICATION,
            ROUND126,
            ROUND126_VERIFICATION,
        )
    }
    validate_verifications(documents)
    return manifest, documents


def exact_path_inputs(
    r113: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    require(
        r113["official_registry_candidate_key_count"] == 441280
        and r113["official_registry_rows_sha256"]
        == GLOBAL_WORD_ROWS_STREAM_SHA256,
        "Round113 global registry crosslink",
    )
    require(
        r113["sheet_rows_sha256"] == digest(r113["sheet_rows"]),
        "Round113 sheet row aggregate hash",
    )
    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for sheet in r113["sheet_rows"]:
        require(type(sheet) is dict, "Round113 sheet object")
        for cell in sheet["certified_cells"]:
            if cell.get("cell_id") == PARENT_ID:
                matches.append((sheet, cell))
    require(len(matches) == 1, "unique Round113 exact parent")
    sheet, cell = matches[0]
    require(
        sheet["sheet_id"] == SHEET_ID
        and sheet["sheet_kind"] == "BYPASS"
        and sheet["source_chart"] == "G:W"
        and sheet["branch_key"] == EXPECTED_BRANCH,
        "Round113 exact parent sheet",
    )
    expected_ids = [word["word_key_id"] for word in EXPECTED_WORDS]
    require(
        cell["official_path_id"] == PATH_ID
        and cell["official_word_key_ids"] == expected_ids
        and cell["ordered_regular_relative_interior_owner_ids"]
        == EXPECTED_OWNERS
        and len(cell["leg_audits"]) == 3,
        "Round113 exact path",
    )
    leg_inputs: list[dict[str, Any]] = []
    for stage, (leg, expected) in enumerate(
        zip(cell["leg_audits"], EXPECTED_WORDS, strict=True)
    ):
        official = leg["official_word_key"]
        require(
            set(official)
            == {"ordinal_zero_based", "row", "row_sha256", "word_key_id"},
            f"Round113 official word closed row:{stage}",
        )
        require(
            official["ordinal_zero_based"] == expected["ordinal_zero_based"]
            and official["row"] == expected["row"]
            and official["row_sha256"] == expected["row_sha256"]
            and official["word_key_id"] == expected["word_key_id"],
            f"Round113 official word identity:{stage}",
        )
        require(
            official["row_sha256"] == digest(official["row"]),
            f"Round113 official word row hash:{stage}",
        )
        require(
            official["word_key_id"]
            == (
                f"gate5-word:{official['ordinal_zero_based']:06d}:"
                f"{official['row_sha256']}"
            ),
            f"Round113 official word stable ID:{stage}",
        )
        pair_ordinal = expected[
            "retained_chart_target_pair_ordinal_zero_based"
        ]
        pattern_ordinal = expected["crossing_pattern_ordinal_zero_based"]
        require(
            official["ordinal_zero_based"] == pair_ordinal * 985 + pattern_ordinal,
            f"global registry ordinal decomposition:{stage}",
        )
        require(
            leg["official_relative_target_id"] == EXPECTED_RELATIVE_TARGETS[stage]
            and leg["selected_collision_chart"] == EXPECTED_COLLISION_CHARTS[stage]
            and leg["ordered_clean_wall_record"] == official["row"][2],
            f"Round113 leg data:{stage}",
        )
        leg_inputs.append(
            {
                "stage": stage,
                "official": official,
                "relative_registry_target_id":
                    leg["official_relative_target_id"],
                "absolute_owner_id": EXPECTED_OWNERS[stage],
                "selected_collision_chart":
                    leg["selected_collision_chart"],
                "retained_pair_ordinal": pair_ordinal,
                "pattern_ordinal": pattern_ordinal,
            }
        )
    require(
        leg_inputs[1]["relative_registry_target_id"] == "G[1,1]"
        and leg_inputs[1]["absolute_owner_id"] == "G[0,0]",
        "relative/absolute second-leg separation",
    )
    return cell, leg_inputs


def validate_round117_join(
    r117: dict[str, Any],
    word_ids: list[str],
) -> dict[str, Any]:
    require(
        r117["common_refinement_rows_sha256"]
        == digest(r117["common_refinement_rows"]),
        "Round117 common refinement aggregate hash",
    )
    parents = [
        row
        for row in r117["common_refinement_rows"]
        if row.get("parent_round113_cell_id") == PARENT_ID
    ]
    require(len(parents) == 1, "unique Round117 parent join")
    parent = parents[0]
    require(
        parent["parent_round113_sheet_id"] == SHEET_ID
        and parent["branch_key"] == EXPECTED_BRANCH
        and parent["sheet_kind"] == "BYPASS"
        and parent["official_path_id_inherited"] == PATH_ID
        and parent["official_word_key_ids_inherited"] == word_ids
        and parent["actual_third_collision_owner_id"] == "G[-1,-2]"
        and parent["actual_third_collision_homogeneity_label"] == "H0_CENTRAL",
        "Round117 inherited exact path",
    )
    samples = [
        family
        for family in parent["generator_families"]
        if family.get("stable_id_interface_sample", {}).get("operator_cell_id")
        == OPERATOR_CELL_ID
    ]
    require(len(samples) == 1, "unique Round117 operator-cell sample")
    sample = samples[0]
    require(
        sample["family"]
        == "BYPASS_SOURCE_CENTRAL_OUTER__ACTUAL_THIRD_H0"
        and sample["source_label_domain"] == "H0_CENTRAL_OUTER"
        and sample["stable_id_interface_sample"][
            "sample_is_certified_nonempty_for_this_parent"
        ]
        is True,
        "Round117 exact operator cell",
    )
    return parent


def validate_round121_join(
    r121: dict[str, Any],
    word_ids: list[str],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    seed = r121["exact_seed_contract"]
    replay = r121["whole_seed_owner_candidate_replay"]
    require(
        seed["round113_parent_id"] == PARENT_ID
        and seed["round117_operator_cell_id"] == OPERATOR_CELL_ID
        and seed["exact_parent_W_seed_id"] == EXACT_SEED_ID
        and seed["branch_key"] == EXPECTED_BRANCH
        and seed["sheet_kind"] == "BYPASS"
        and seed["source_chart"] == "G:W",
        "Round121 exact seed root",
    )
    require(
        replay["official_path_id"] == PATH_ID
        and replay["official_word_key_ids"] == word_ids
        and replay["ordered_owner_ids"] == EXPECTED_OWNERS
        and replay["selected_collision_charts"] == EXPECTED_COLLISION_CHARTS,
        "Round121 whole seed replay",
    )
    require(
        r121["refined_homogeneous_subbranch_rows_sha256"]
        == digest(r121["refined_homogeneous_subbranch_rows"])
        and r121["common_refinement_rows_sha256"]
        == digest(r121["common_refinement_rows"])
        and len(r121["refined_homogeneous_subbranch_rows"]) == 24
        and len(r121["common_refinement_rows"]) == 24,
        "Round121 child/subbranch aggregate hashes",
    )
    refined_by_id: dict[str, dict[str, Any]] = {}
    child_by_id: dict[str, dict[str, Any]] = {}
    ranks: set[int] = set()
    for refined in r121["refined_homogeneous_subbranch_rows"]:
        validate_payload_hashed_row(refined, "Round121 refined subbranch")
        subbranch = refined["refined_homogeneous_subbranch_id"]
        rank = refined["common_rank"]
        require(
            type(subbranch) is str
            and is_int(rank)
            and refined["exact_parent_W_seed_id"] == EXACT_SEED_ID
            and refined["round117_operator_cell_id"] == OPERATOR_CELL_ID,
            "Round121 refined subbranch root",
        )
        require(
            subbranch not in refined_by_id and rank not in ranks,
            "Round121 unique refined subbranch",
        )
        refined_by_id[subbranch] = refined
        ranks.add(rank)
    require(ranks == set(range(24)), "Round121 subbranch ranks")
    for child in r121["common_refinement_rows"]:
        validate_payload_hashed_row(child, "Round121 common child")
        child_id = child["common_child_id"]
        subbranch = child["refined_homogeneous_subbranch_id"]
        rank = child["common_rank"]
        require(
            type(child_id) is str
            and child_id not in child_by_id
            and subbranch in refined_by_id
            and child_id == refined_by_id[subbranch]["common_child_id"]
            and rank == refined_by_id[subbranch]["common_rank"],
            "Round121 child/subbranch join",
        )
        require(
            child["official_path_id"] == PATH_ID
            and child["round117_operator_cell_id"] == OPERATOR_CELL_ID
            and child["actual_standard_curve_child_installed"] is True
            and child[
                "all_three_inputs_contained_in_one_materialized_canonical_cell"
            ]
            is True
            and child["lower_closed"] is True
            and child["upper_closed"] is False,
            "Round121 half-open common child",
        )
        child_by_id[child_id] = child
    require(len(child_by_id) == 24, "Round121 common child census")
    return refined_by_id, child_by_id


def validate_round126_rows(
    r126: dict[str, Any],
    word_ids: list[str],
    refined_by_id: dict[str, dict[str, Any]],
    child_by_id: dict[str, dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    dict[tuple[str, str, int], dict[str, Any]],
    list[str],
]:
    require(
        r126["preexisting_F1_F17_same_key_map_rows_sha256"]
        == digest(r126["preexisting_F1_F17_same_key_map_rows"])
        and r126["gate5_F18_slot_rows_sha256"]
        == digest(r126["gate5_F18_slot_rows"])
        and len(r126["preexisting_F1_F17_same_key_map_rows"]) == 120
        and len(r126["gate5_F18_slot_rows"]) == 120,
        "Round126 map/F18 aggregate hashes",
    )
    safety = {
        "rank3_seed_child_field_maturity":
            r126["rank3_seed_child_field_maturity"],
        "seed_local_complete_18_field_level_block_count":
            r126["seed_local_complete_18_field_level_block_count"],
        "seed_local_complete_18_field_child_packet_count":
            r126["seed_local_complete_18_field_child_packet_count"],
        "global_complete_18_field_block_count":
            r126["global_complete_18_field_block_count"],
        "complete_18_field_block_count":
            r126["complete_18_field_block_count"],
        "gate5_block_count": r126["gate5_block_count"],
        "gate5_global_maturity": r126["gate5_global_maturity"],
        "cm2_verdict": r126["cm2_verdict"],
    }
    require(
        safety
        == {
            "rank3_seed_child_field_maturity": "18/18",
            "seed_local_complete_18_field_level_block_count": 120,
            "seed_local_complete_18_field_child_packet_count": 24,
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_global_maturity": "10/18",
            "cm2_verdict": "NO-GO_FOR_CLAIM",
        },
        "Round126 certificate safety state",
    )
    expected_stage = {word: stage for stage, word in enumerate(word_ids)}
    maps: dict[tuple[str, str, int], dict[str, Any]] = {}
    map_ids: set[str] = set()
    source_slot_ids: set[str] = set()
    field_census: Counter[int] = Counter()
    child_base_census: Counter[str] = Counter()
    stage_base_census: Counter[int] = Counter()
    for map_row in r126["preexisting_F1_F17_same_key_map_rows"]:
        validate_payload_hashed_row(map_row, "Round126 F1-F17 map")
        base = map_row["immutable_base_key"]
        require(
            type(base) is list
            and len(base) == 3
            and type(base[0]) is str
            and type(base[1]) is str
            and is_int(base[2]),
            "Round126 immutable base key",
        )
        key = (base[0], base[1], base[2])
        stage = map_row["stage"]
        require(
            key not in maps
            and map_row["same_key_map_row_id"] not in map_ids
            and base[0] in expected_stage
            and stage == expected_stage[base[0]]
            and base[2] in ROOF_LEVELS_BY_STAGE[stage],
            "Round126 unique base coordinate",
        )
        require(
            map_row["official_word_key_id"] == base[0]
            and map_row["refined_homogeneous_subbranch_id"] == base[1]
            and map_row["roof_level_j"] == base[2]
            and base[1] in refined_by_id,
            "Round126 base coordinate fields",
        )
        refined = refined_by_id[base[1]]
        child_id = map_row["common_child_id"]
        require(
            child_id == refined["common_child_id"]
            and child_id in child_by_id
            and map_row["common_rank"] == refined["common_rank"]
            and map_row["each_preexisting_field_bound_exactly_once"] is True
            and map_row[
                "all_preexisting_fields_share_child_stage_input_and_operator_carrier"
            ]
            is True,
            "Round126 map root join",
        )
        bindings = map_row["bound_preexisting_F1_F17_slots"]
        require(
            type(bindings) is list
            and len(bindings) == 17
            and map_row["bound_preexisting_field_count"] == 17
            and map_row["bound_preexisting_field_indices"]
            == list(range(1, 18))
            and map_row["bound_preexisting_F1_F17_slots_sha256"]
            == digest(bindings),
            "Round126 F1-F17 bindings",
        )
        seen_fields: set[int] = set()
        for binding in bindings:
            require(
                type(binding) is dict
                and set(binding)
                == {
                    "field_index",
                    "field_name",
                    "slot_id",
                    "source_certificate_round",
                    "source_slot_canonical_sha256",
                },
                "Round126 closed binding",
            )
            field = binding["field_index"]
            slot_id = binding["slot_id"]
            require(
                is_int(field)
                and 1 <= field <= 17
                and field not in seen_fields
                and binding["field_name"] == FIELD_NAMES[field]
                and binding["source_certificate_round"]
                == SOURCE_ROUND_BY_FIELD[field]
                and type(slot_id) is str
                and slot_id not in source_slot_ids
                and type(binding["source_slot_canonical_sha256"]) is str
                and len(binding["source_slot_canonical_sha256"]) == 64,
                "Round126 binding identity",
            )
            seen_fields.add(field)
            source_slot_ids.add(slot_id)
            field_census[field] += 1
        require(seen_fields == set(range(1, 18)), "Round126 exact F1-F17")
        maps[key] = map_row
        map_ids.add(map_row["same_key_map_row_id"])
        child_base_census[child_id] += 1
        stage_base_census[stage] += 1
    require(
        len(maps) == len(map_ids) == 120
        and len(source_slot_ids) == 2040
        and field_census == Counter({field: 120 for field in range(1, 18)})
        and child_base_census
        == Counter({child_id: 5 for child_id in child_by_id})
        and stage_base_census == EXPECTED_BASE_STAGE_COUNTS,
        "Round126 F1-F17 full census",
    )

    f18_by_base: dict[tuple[str, str, int], dict[str, Any]] = {}
    f18_slot_ids: set[str] = set()
    for f18 in r126["gate5_F18_slot_rows"]:
        validate_payload_hashed_row(f18, "Round126 F18 slot")
        immutable = f18["immutable_slot_key"]
        require(
            type(immutable) is list
            and len(immutable) == 4
            and immutable[3] == FIELD_NAMES[18],
            "Round126 F18 immutable key",
        )
        key = (immutable[0], immutable[1], immutable[2])
        require(
            key in maps
            and key not in f18_by_base
            and f18["slot_id"] not in f18_slot_ids,
            "Round126 unique F18 base binding",
        )
        map_row = maps[key]
        stage = map_row["stage"]
        roof = key[2]
        return_length = STAGE_RETURN_LENGTH[stage]
        require(
            f18["official_word_key_id"] == key[0]
            and f18["refined_homogeneous_subbranch_id"] == key[1]
            and f18["roof_level_j"] == roof
            and f18["field_index"] == 18
            and f18["field_name"] == FIELD_NAMES[18]
            and f18["common_child_id"] == map_row["common_child_id"]
            and f18["common_rank"] == map_row["common_rank"]
            and f18["stage"] == stage
            and f18["input_materialized_recut_instance_id"]
            == map_row["input_materialized_recut_instance_id"]
            and f18["standard_family_leg_operator_row_id"]
            == map_row["standard_family_leg_operator_row_id"]
            and f18["standard_family_leg_operator_row_sha256"]
            == map_row["standard_family_leg_operator_row_sha256"]
            and f18["preexisting_F1_F17_same_key_map_row_id"]
            == map_row["same_key_map_row_id"]
            and f18["preexisting_F1_F17_same_key_map_row_sha256"]
            == map_row["row_sha256"],
            "Round126 F18 same-root join",
        )
        require(
            f18["stage_return_length_r"] == return_length
            and f18["prefix_length_j"] == roof
            and f18["suffix_length_r_minus_j"] == return_length - roof
            and f18["field_bound_semantics"] == "STRUCTURAL_REGISTRATION"
            and f18["structural_registration_only"] is True
            and f18["operator_Wiener_invertibility_claimed"] is False
            and f18["operator_Wiener_aperiodicity_claimed"] is False
            and f18["Kac_closure_claimed"] is False
            and f18["global_operator_phase_block_claimed"] is False
            and f18["CM2_claimed"] is False,
            "Round126 F18 nonpromotion",
        )
        f18_by_base[key] = f18
        f18_slot_ids.add(f18["slot_id"])
    require(
        set(f18_by_base) == set(maps)
        and len(f18_slot_ids) == 120
        and source_slot_ids.isdisjoint(f18_slot_ids),
        "Round126 complete disjoint F1-F18 census",
    )
    ordered_keys = sorted(
        maps,
        key=lambda key: (
            maps[key]["common_rank"],
            maps[key]["stage"],
            key[2],
        ),
    )
    all_slot_ids = [
        slot_id
        for key in ordered_keys
        for slot_id in (
            [
                binding["slot_id"]
                for binding in maps[key]["bound_preexisting_F1_F17_slots"]
            ]
            + [f18_by_base[key]["slot_id"]]
        )
    ]
    require(
        len(all_slot_ids) == len(set(all_slot_ids)) == 2160,
        "Round126 2160 unique slots",
    )
    return [maps[key] for key in ordered_keys], f18_by_base, all_slot_ids


def base_crosswalk_id(base: tuple[str, str, int]) -> str:
    return row_id("round127-seed-local-base-key", list(base))


def carrier_crosswalk_id(word: str, subbranch: str) -> str:
    return row_id("round127-word-subbranch-carrier", [word, subbranch])


def build_base_crosswalk_rows(
    map_rows: list[dict[str, Any]],
    f18_by_base: dict[tuple[str, str, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for map_row in map_rows:
        base_list = map_row["immutable_base_key"]
        base = (base_list[0], base_list[1], base_list[2])
        f18 = f18_by_base[base]
        bindings = [
            {
                "field_index": binding["field_index"],
                "field_name": binding["field_name"],
                "slot_id": binding["slot_id"],
                "source_certificate_round":
                    binding["source_certificate_round"],
                "source_slot_canonical_sha256":
                    binding["source_slot_canonical_sha256"],
            }
            for binding in map_row["bound_preexisting_F1_F17_slots"]
        ]
        bindings.append(
            {
                "field_index": 18,
                "field_name": FIELD_NAMES[18],
                "slot_id": f18["slot_id"],
                "source_certificate_round": 126,
                "source_slot_canonical_sha256": f18["row_sha256"],
            }
        )
        require(
            [binding["field_index"] for binding in bindings]
            == list(range(1, 19)),
            "Round127 ordered 18 bindings",
        )
        row = {
            "seed_local_base_key_crosswalk_id": base_crosswalk_id(base),
            "immutable_seed_local_base_key": list(base),
            "official_word_key_id": base[0],
            "refined_homogeneous_subbranch_id": base[1],
            "roof_level_j": base[2],
            "stage": map_row["stage"],
            "stage_return_length_r":
                STAGE_RETURN_LENGTH[map_row["stage"]],
            "common_child_id": map_row["common_child_id"],
            "common_rank": map_row["common_rank"],
            "input_materialized_recut_instance_id":
                map_row["input_materialized_recut_instance_id"],
            "word_subbranch_operator_carrier_crosswalk_id":
                carrier_crosswalk_id(base[0], base[1]),
            "standard_family_leg_operator_row_id":
                map_row["standard_family_leg_operator_row_id"],
            "standard_family_leg_operator_row_sha256":
                map_row["standard_family_leg_operator_row_sha256"],
            "round126_preexisting_F1_F17_same_key_map_row_id":
                map_row["same_key_map_row_id"],
            "round126_preexisting_F1_F17_same_key_map_row_sha256":
                map_row["row_sha256"],
            "round126_F18_slot_id": f18["slot_id"],
            "round126_F18_slot_row_sha256": f18["row_sha256"],
            "field_slot_bindings": bindings,
            "field_slot_bindings_sha256": digest(bindings),
            "field_indices_exactly_once": list(range(1, 19)),
            "field_slot_count": 18,
            "all_18_fields_share_word_subbranch_roof_child_stage_recut_and_operator_carrier":
                True,
            "scope": "ROUND121_EXACT_SEED_LOCAL_LEVEL_ONLY",
            "global_level_or_block_claimed": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows)
        == len({row["seed_local_base_key_crosswalk_id"] for row in rows})
        == 120,
        "Round127 base crosswalk census",
    )
    return rows


def build_carrier_crosswalk_rows(
    base_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for base in base_rows:
        grouped[
            (
                base["official_word_key_id"],
                base["refined_homogeneous_subbranch_id"],
            )
        ].append(base)
    require(len(grouped) == 72, "Round127 72 carrier groups")
    rows: list[dict[str, Any]] = []
    for (word, subbranch), levels in grouped.items():
        levels.sort(key=lambda row: row["roof_level_j"])
        first = levels[0]
        stage = first["stage"]
        roofs = [row["roof_level_j"] for row in levels]
        require(roofs == ROOF_LEVELS_BY_STAGE[stage], "carrier roof census")
        invariant_keys = (
            "stage",
            "common_child_id",
            "common_rank",
            "input_materialized_recut_instance_id",
            "standard_family_leg_operator_row_id",
            "standard_family_leg_operator_row_sha256",
        )
        require(
            all(
                all(level[key] == first[key] for key in invariant_keys)
                for level in levels
            ),
            "carrier invariant root",
        )
        row = {
            "word_subbranch_operator_carrier_crosswalk_id":
                carrier_crosswalk_id(word, subbranch),
            "official_word_key_id": word,
            "refined_homogeneous_subbranch_id": subbranch,
            "stage": stage,
            "stage_return_length_r": STAGE_RETURN_LENGTH[stage],
            "roof_level_js": roofs,
            "common_child_id": first["common_child_id"],
            "common_rank": first["common_rank"],
            "input_materialized_recut_instance_id":
                first["input_materialized_recut_instance_id"],
            "standard_family_leg_operator_row_id":
                first["standard_family_leg_operator_row_id"],
            "standard_family_leg_operator_row_sha256":
                first["standard_family_leg_operator_row_sha256"],
            "seed_local_base_key_crosswalk_ids": [
                level["seed_local_base_key_crosswalk_id"]
                for level in levels
            ],
            "seed_local_base_key_count": len(levels),
            "seed_local_field_slot_count": 18 * len(levels),
            "one_operator_carrier_shared_across_its_symbolic_roof_splits":
                True,
            "scope": "ONE_WORD_ON_ONE_ROUND121_EXACT_SEED_SUBBRANCH",
            "global_physical_carrier_claimed": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    rows.sort(key=lambda row: (row["common_rank"], row["stage"]))
    require(
        len(rows)
        == len(
            {
                row["word_subbranch_operator_carrier_crosswalk_id"]
                for row in rows
            }
        )
        == 72
        and Counter(row["stage"] for row in rows)
        == Counter({0: 24, 1: 24, 2: 24}),
        "Round127 carrier crosswalk census",
    )
    return rows


def build_subbranch_crosswalk_rows(
    refined_by_id: dict[str, dict[str, Any]],
    child_by_id: dict[str, dict[str, Any]],
    carrier_rows: list[dict[str, Any]],
    base_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    carriers_by_subbranch: dict[str, list[dict[str, Any]]] = defaultdict(list)
    bases_by_subbranch: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for carrier in carrier_rows:
        carriers_by_subbranch[
            carrier["refined_homogeneous_subbranch_id"]
        ].append(carrier)
    for base in base_rows:
        bases_by_subbranch[
            base["refined_homogeneous_subbranch_id"]
        ].append(base)
    rows: list[dict[str, Any]] = []
    for subbranch, refined in refined_by_id.items():
        child = child_by_id[refined["common_child_id"]]
        carriers = sorted(
            carriers_by_subbranch[subbranch],
            key=lambda row: row["stage"],
        )
        bases = sorted(
            bases_by_subbranch[subbranch],
            key=lambda row: (row["stage"], row["roof_level_j"]),
        )
        require(
            [row["stage"] for row in carriers] == [0, 1, 2]
            and len(bases) == 5
            and sum(row["field_slot_count"] for row in bases) == 90,
            "Round127 subbranch local census",
        )
        row = {
            "refined_subbranch_crosswalk_id":
                row_id("round127-refined-subbranch", subbranch),
            "refined_homogeneous_subbranch_id": subbranch,
            "common_child_id": refined["common_child_id"],
            "common_rank": refined["common_rank"],
            "exact_parent_W_seed_id": EXACT_SEED_ID,
            "round117_operator_cell_id": OPERATOR_CELL_ID,
            "round121_refined_subbranch_row_sha256":
                refined["row_sha256"],
            "round121_common_child_row_sha256": child["row_sha256"],
            "physical_homogeneity": refined["physical_homogeneity"],
            "word_subbranch_operator_carrier_crosswalk_ids": [
                carrier["word_subbranch_operator_carrier_crosswalk_id"]
                for carrier in carriers
            ],
            "seed_local_base_key_crosswalk_ids": [
                base["seed_local_base_key_crosswalk_id"] for base in bases
            ],
            "word_subbranch_operator_carrier_count": 3,
            "seed_local_base_key_count": 5,
            "seed_local_field_slot_count": 90,
            "child_interval_ownership": "[lower,upper)",
            "scope": "ONE_ROUND121_EXACT_SEED_COMMON_CHILD",
            "global_homogeneous_subbranch_claimed": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    rows.sort(key=lambda row: row["common_rank"])
    require(
        len(rows) == 24
        and [row["common_rank"] for row in rows] == list(range(24)),
        "Round127 refined subbranch census",
    )
    return rows


def build_word_crosswalk_rows(
    leg_inputs: list[dict[str, Any]],
    carrier_rows: list[dict[str, Any]],
    base_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    carriers_by_word: dict[str, list[dict[str, Any]]] = defaultdict(list)
    bases_by_word: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for carrier in carrier_rows:
        carriers_by_word[carrier["official_word_key_id"]].append(carrier)
    for base in base_rows:
        bases_by_word[base["official_word_key_id"]].append(base)
    rows: list[dict[str, Any]] = []
    for leg in leg_inputs:
        stage = leg["stage"]
        official = leg["official"]
        word = official["word_key_id"]
        carriers = sorted(
            carriers_by_word[word],
            key=lambda row: row["common_rank"],
        )
        bases = sorted(
            bases_by_word[word],
            key=lambda row: (row["common_rank"], row["roof_level_j"]),
        )
        return_length = official["row"][3]
        require(
            len(carriers) == 24
            and len(bases) == 24 * return_length
            and all(carrier["stage"] == stage for carrier in carriers)
            and all(base["stage"] == stage for base in bases),
            "Round127 word incidence census",
        )
        row = {
            "official_word_registry_incidence_row_id":
                row_id("round127-official-word-registry-incidence", word),
            "path_position_zero_based": stage,
            "stage": stage,
            "official_word_key_id": word,
            "global_candidate_registry_ordinal_zero_based":
                official["ordinal_zero_based"],
            "retained_chart_target_pair_ordinal_zero_based":
                leg["retained_pair_ordinal"],
            "crossing_pattern_ordinal_zero_based":
                leg["pattern_ordinal"],
            "global_word_row": official["row"],
            "global_word_row_sha256": official["row_sha256"],
            "source_normal_chart": official["row"][0],
            "relative_registry_target_id":
                leg["relative_registry_target_id"],
            "absolute_physical_owner_id": leg["absolute_owner_id"],
            "relative_registry_target_and_absolute_owner_are_distinct_namespaces":
                True,
            "ordered_clean_wall_record": official["row"][2],
            "selected_collision_chart": leg["selected_collision_chart"],
            "return_length_r": return_length,
            "symbolic_roof_level_js": list(range(return_length)),
            "global_registry_membership_basis":
                "PINNED_ROUND113_OFFICIAL_WORD_ROW_AND_GLOBAL_STREAM_DIGEST",
            "word_subbranch_operator_carrier_crosswalk_ids": [
                carrier["word_subbranch_operator_carrier_crosswalk_id"]
                for carrier in carriers
            ],
            "seed_local_base_key_crosswalk_ids": [
                base["seed_local_base_key_crosswalk_id"] for base in bases
            ],
            "round121_exact_seed_refined_subbranch_incidence_count": 24,
            "round126_word_subbranch_operator_carrier_count": 24,
            "round126_seed_local_base_key_count": len(bases),
            "round126_seed_local_field_slot_count": 18 * len(bases),
            "complete_global_domain_decision_claimed": False,
            "global_physical_coverage_claimed": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(
        len(rows) == 3
        and sum(len(row["symbolic_roof_level_js"]) for row in rows) == 5
        and sum(row["round126_word_subbranch_operator_carrier_count"]
                for row in rows) == 72
        and sum(row["round126_seed_local_base_key_count"]
                for row in rows) == 120
        and sum(row["round126_seed_local_field_slot_count"]
                for row in rows) == 2160,
        "Round127 word incidence totals",
    )
    return rows


def build() -> dict[str, Any]:
    global_result, documents = load_inputs()
    r113 = documents[ROUND113.name]["result"]
    r117 = documents[ROUND117.name]["result"]
    r121 = documents[ROUND121.name]["result"]
    r126 = documents[ROUND126.name]["result"]

    _cell, leg_inputs = exact_path_inputs(r113)
    word_ids = [leg["official"]["word_key_id"] for leg in leg_inputs]
    _parent117 = validate_round117_join(r117, word_ids)
    refined_by_id, child_by_id = validate_round121_join(r121, word_ids)
    map_rows, f18_by_base, all_slot_ids = validate_round126_rows(
        r126,
        word_ids,
        refined_by_id,
        child_by_id,
    )
    base_rows = build_base_crosswalk_rows(map_rows, f18_by_base)
    carrier_rows = build_carrier_crosswalk_rows(base_rows)
    subbranch_rows = build_subbranch_crosswalk_rows(
        refined_by_id,
        child_by_id,
        carrier_rows,
        base_rows,
    )
    word_rows = build_word_crosswalk_rows(
        leg_inputs,
        carrier_rows,
        base_rows,
    )

    base_stage_counts = Counter(row["stage"] for row in base_rows)
    slot_field_counts = Counter(
        binding["field_index"]
        for base in base_rows
        for binding in base["field_slot_bindings"]
    )
    require(
        base_stage_counts == EXPECTED_BASE_STAGE_COUNTS
        and slot_field_counts
        == Counter({field: 120 for field in range(1, 19)}),
        "Round127 stage/field census",
    )

    global_registry = global_result["immutable_candidate_key_registry"]
    global_roof_count = global_registry[
        "prefix_suffix_factor_contract"
    ]["roof_level_prefix_suffix_factor_pair_count"]
    result = {
        "status": "REGISTRY_MEMBERSHIP_AND_SEED_LOCAL_SLOT_CENSUS",
        "symbolic_registry_incidence": {
            "terminology":
                "MEMBERSHIP_AND_INCIDENCE_NOT_DOMAIN_MEASURE_OR_PHYSICAL_COVERAGE",
            "global_symbolic_candidate_word_key_count": 441280,
            "exact_seed_path_referenced_unique_word_key_count": 3,
            "word_key_registry_incidence_fraction": "3/441280",
            "word_keys_unjoined_to_this_exact_seed_path_incidence": 441277,
            "unjoined_word_semantics":
                "not present in this exact-seed path incidence; no emptiness or uncovered-domain conclusion",
            "global_symbolic_word_roof_position_count": global_roof_count,
            "exact_seed_path_referenced_unique_symbolic_word_roof_position_count":
                5,
            "word_roof_registry_incidence_fraction": "5/3286976",
            "word_roof_positions_unjoined_to_this_exact_seed_path_incidence":
                3286971,
            "unjoined_word_roof_semantics":
                "not present in this exact-seed path incidence; no physical coverage conclusion",
            "round126_seed_local_word_subbranch_roof_base_key_count": 120,
            "seed_local_base_keys_are_not_divided_by_global_word_roof_positions":
                True,
            "reason_120_has_no_global_incidence_denominator":
                "each local base key includes one of 24 Round121 exact-seed refined subbranches",
            "global_exact_nonempty_candidate_key_count":
                global_registry["exact_nonempty_candidate_key_count"],
            "global_complete_nonempty_or_empty_domain_decisions": False,
            "global_physical_or_measure_coverage_claimed": False,
        },
        "exact_path_root_contract": {
            "round113_parent_cell_id": PARENT_ID,
            "round113_parent_sheet_id": SHEET_ID,
            "round113_official_path_id": PATH_ID,
            "round113_branch_key": EXPECTED_BRANCH,
            "round113_ordered_absolute_owner_ids": EXPECTED_OWNERS,
            "round113_relative_registry_target_ids":
                EXPECTED_RELATIVE_TARGETS,
            "round113_selected_collision_charts":
                EXPECTED_COLLISION_CHARTS,
            "second_leg_relative_registry_target_id": "G[1,1]",
            "second_leg_absolute_owner_id": "G[0,0]",
            "second_leg_relative_target_is_not_relabelled_as_absolute_owner":
                True,
            "round117_operator_cell_id": OPERATOR_CELL_ID,
            "round117_family":
                "BYPASS_SOURCE_CENTRAL_OUTER__ACTUAL_THIRD_H0",
            "round121_exact_parent_W_seed_id": EXACT_SEED_ID,
            "round121_actual_common_child_count": 24,
            "round121_refined_homogeneous_subbranch_count": 24,
            "stage_return_lengths": {"0": 2, "1": 1, "2": 2},
            "stage_symbolic_roof_levels":
                {"0": [0, 1], "1": [0], "2": [0, 1]},
        },
        "exact_path_official_word_registry_incidence_rows": word_rows,
        "exact_path_official_word_registry_incidence_rows_sha256":
            digest(word_rows),
        "seed_local_refined_subbranch_crosswalk_rows": subbranch_rows,
        "seed_local_refined_subbranch_crosswalk_rows_sha256":
            digest(subbranch_rows),
        "word_subbranch_operator_carrier_crosswalk_rows": carrier_rows,
        "word_subbranch_operator_carrier_crosswalk_rows_sha256":
            digest(carrier_rows),
        "seed_local_base_key_crosswalk_rows": base_rows,
        "seed_local_base_key_crosswalk_rows_sha256": digest(base_rows),
        "slot_census": {
            "round126_preexisting_F1_F17_slot_count": 2040,
            "round126_F18_slot_count": 120,
            "round126_total_seed_local_slot_count": 2160,
            "round127_materialized_slot_binding_count": sum(
                row["field_slot_count"] for row in base_rows
            ),
            "round127_base_major_all_slot_ids_sha256": digest(
                [
                    binding["slot_id"]
                    for base in base_rows
                    for binding in base["field_slot_bindings"]
                ]
            ),
            "round126_validated_unique_slot_id_count": len(set(all_slot_ids)),
            "slot_count_per_field": {
                str(field): slot_field_counts[field]
                for field in range(1, 19)
            },
            "all_18_fields_exactly_once_on_each_of_120_seed_local_base_keys":
                True,
            "all_fields_share_same_word_subbranch_roof_child_stage_recut_and_operator_carrier_per_base":
                True,
        },
        "count_ledger": {
            "exact_path_count": 1,
            "exact_path_unique_official_word_count": 3,
            "exact_path_symbolic_word_roof_position_count": 5,
            "round121_exact_seed_common_child_count": 24,
            "round121_exact_seed_refined_subbranch_count": 24,
            "word_subbranch_operator_carrier_count": 72,
            "word_subbranch_operator_carrier_stage_counts":
                {"0": 24, "1": 24, "2": 24},
            "seed_local_base_key_count": 120,
            "seed_local_base_key_stage_counts":
                {"0": 48, "1": 24, "2": 48},
            "seed_local_field_slot_count": 2160,
            "seed_local_field_slot_count_per_field": 120,
            "seed_local_complete_18_field_level_block_count": 120,
            "seed_local_complete_18_field_child_packet_count": 24,
            "global_complete_18_field_block_count": 0,
            "complete_18_field_block_count": 0,
            "gate5_block_count": 0,
        },
        "root_separation_and_nonpromotion": {
            "symbolic_global_registry_root":
                "441280 candidate word keys; empty fibres allowed; no materialized homogeneous subbranches",
            "round113_root":
                "one verified regular relative-interior rank-three path on one endpoint-sheet cell",
            "round117_root":
                "one nonempty source/operator-cell sample inherited from the Round113 parent",
            "round121_root":
                "one exact rational-anchor parent-W seed with 24 half-open common children",
            "round126_root":
                "120 exact-seed local word/subbranch/roof levels and their structural direct-standard-N carriers",
            "installed_identifications": [
                "the three Round113 official word IDs and rows are pinned symbolic-registry members",
                "Round117 inherits the same Round113 parent, path, and three word IDs",
                "Round121 pins the Round113 parent and Round117 operator-cell sample",
                "Round126 pins the same three words on all 24 Round121 refined subbranches",
                "each of 120 seed-local base keys binds F1 through F18 exactly once",
            ],
            "forbidden_identifications": [
                "seed-local refined subbranch is not a global homogeneous-subbranch registry entry",
                "seed-local level block is not a global physical complete block",
                "24 derived child packets are not materialized global blocks",
                "symbolic word membership is not a full D_w domain decision",
                "symbolic word/roof incidence is not domain, measure, or physical coverage",
                "relative registry target IDs are not absolute physical owner IDs",
            ],
        },
        "global_safety_state": {
            "rank3_seed_child_field_maturity": "18/18",
            "seed_local_complete_18_field_level_block_count": 120,
            "seed_local_complete_18_field_child_packet_count": 24,
            "gate5_global_maturity": "10/18",
            "complete_18_field_block_count": 0,
            "global_complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_status": "NOT_CERTIFIED",
            "cm2_verdict": "NO-GO_FOR_CLAIM",
        },
        "strict_scope": (
            "symbolic-registry membership for the three-word Round113 path and "
            "an exact census/crosswalk of its Round121--Round126 one-seed local "
            "subbranches, carriers, base keys, and field slots"
        ),
        "strict_nonclaims": [
            "no complete nonempty-or-empty decision for all 441280 candidate word domains",
            "no claim that the three referenced D_w are covered maximally or over their full parameter fibres",
            "no all-homogeneity-subbranch or all-parameter-fibre registry",
            "no arbitrary-return-depth or all-Borel-key physical registration",
            "no domain, measure, probability, or physical coverage ratio",
            "no division of 120 seed-local base keys by 3286976 global symbolic word-roof positions",
            "no claim that five symbolic roof positions are five collisions",
            "no global inverse-Jacobian or all-record distortion theorem",
            "no global dynamic-test embedding or common strong recipient",
            "no global raw-Z, power-Orlicz, owner-drift, or positive all-time cemetery theorem",
            "no global all-input oriented vector-current recipient",
            "no operator Wiener invertibility or aperiodicity theorem",
            "no Kac return-wide closure theorem",
            "no global complete 18-field block",
            "no global Gate5 maturity upgrade",
            "no CM2 claim",
        ],
        "upstream_artifact_byte_pins": dict(sorted(BYTE_PINS.items())),
        "upstream_closed_result_sha256_pins":
            dict(sorted(RESULT_PINS.items())),
        "global_manifest_embedded_pins": {
            "producer_sha256": GLOBAL_PRODUCER_SHA256,
            "verifier_sha256": GLOBAL_VERIFIER_SHA256,
            "candidate_word_rows_stream_sha256":
                GLOBAL_WORD_ROWS_STREAM_SHA256,
            "required_18_field_schema_sha256":
                GLOBAL_FIELD_SCHEMA_SHA256,
        },
    }
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    document = build()
    args.output.write_text(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.output}")
    print(f"result_sha256={document['result_sha256']}")
    print("SYMBOLIC_WORD_INCIDENCE=3/441280")
    print("SYMBOLIC_WORD_ROOF_INCIDENCE=5/3286976")
    print("SEED_LOCAL_SUBBRANCHES=24")
    print("WORD_SUBBRANCH_CARRIERS=72")
    print("SEED_LOCAL_BASE_KEYS=120")
    print("SEED_LOCAL_SLOTS=2160")
    print("GLOBAL_GATE5=10/18")
    print("GLOBAL_COMPLETE_BLOCKS=0")
    print("CM2=NO-GO_FOR_CLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
