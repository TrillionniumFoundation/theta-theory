#!/usr/bin/env python3
"""Deterministic Round306C0 corrected fresh-freeze candidate producer.

The producer consumes the complete sealed Round306A transcript and the final
nine-role R235D seal strictly as data.  It applies the R235D selected-row R248
correction overlay, excludes exactly 32 invalid registry members, deletes 16
empty roots, rekeys four nonempty roots, remaps all 478,718 admitted edge
applications, and rebuilds the quotient from an empty DSU in both directions.

Every emitted artifact is still zero-credit candidate material.  Only a later
independent verifier, which must not import or execute this file, may mint the
corrected-universe and corrected-DSU credit.
"""

from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import io
import json
import os
import stat
import sys
import zlib
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Final, Iterable, Iterator


class ProductionBlocked(RuntimeError):
    """Raised before any candidate filesystem access while pins are absent."""


ENCODER: Final = json.JSONEncoder(
    ensure_ascii=True,
    allow_nan=False,
    sort_keys=True,
    separators=(",", ":"),
)


def canonical_bytes(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _reject_float(_: str) -> Any:
    raise ProductionBlocked("nonintegral JSON number")


def _reject_constant(_: str) -> Any:
    raise ProductionBlocked("nonfinite JSON number")


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ProductionBlocked("duplicate JSON key: " + key)
        result[key] = value
    return result


def strict_canonical_json(raw: bytes, label: str) -> Any:
    if raw.endswith(b"\n"):
        raw = raw[:-1]
        if raw.endswith(b"\n"):
            raise ProductionBlocked("multiple trailing newlines: " + label)
    try:
        value = json.loads(
            raw.decode("ascii"),
            object_pairs_hook=_strict_object,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProductionBlocked("strict JSON failure: " + label) from exc
    if canonical_bytes(value) != raw:
        raise ProductionBlocked("noncanonical JSON bytes: " + label)
    return value


def _same_typed(left: Any, right: Any) -> bool:
    """Recursive equality that never aliases bool with int."""

    if type(left) is not type(right):
        return False
    if type(left) is dict:
        if len(left) != len(right):
            return False
        unmatched = list(right.items())
        for left_key, left_value in left.items():
            matches = [
                index
                for index, (right_key, _) in enumerate(unmatched)
                if _same_typed(left_key, right_key)
            ]
            if len(matches) != 1:
                return False
            index = matches[0]
            _, right_value = unmatched.pop(index)
            if not _same_typed(left_value, right_value):
                return False
        return not unmatched
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(
            _same_typed(a, b) for a, b in zip(left, right)
        )
    return bool(left == right)


@dataclass(frozen=True)
class FrozenPin:
    role: str
    filename: str
    size: int
    sha256: str


PREFIX: Final = "cm2_round306c0_source_g_r235d_corrected_fresh_freeze"
SCHEMA: Final = "cm2.round306c0.source-g-r235d-corrected-fresh-freeze.v1"
COMPONENT_NAMESPACE: Final = "round306c0-fresh-legal-component:"
CORRECTED_ROOT_NAMESPACE: Final = "round306c0-corrected-base-root:"
MAX_DECODED_ROW_BYTES: Final = 8 * 1024 * 1024
FIXED_EXTERNAL_SPILL_ROOT: Final = "/tmp/cm2-round306c0-spill"


def _require_isolated_runtime() -> None:
    if type(sys.flags.isolated) is not int or sys.flags.isolated != 1:
        raise ProductionBlocked("run with python3 -I -B: isolated mode is required")
    if sys.dont_write_bytecode is not True:
        raise ProductionBlocked(
            "run with python3 -I -B: bytecode writes must be disabled"
        )

ROUND306A_MANIFEST: Final = FrozenPin(
    "ROUND306A_MANIFEST",
    "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_manifest.sha256",
    1_982,
    "35da99af5bb4c424284af2d7b396fc94b82dd6c6aa468c6a43a139107f9d9efc",
)

# The entire thirteen-member Round306A manifest is the old, sealed authority
# frontier.  C0 consumes its ledgers as data and never imports either producer.
ROUND306A_MANIFEST_MEMBERS: Final = (
    FrozenPin("ROUND306A_PRODUCER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild.py", 74_003, "ab798332c82f7aa3656c61e3b31698a30b0fa1a83d24900432e076e445d6f5d5"),
    FrozenPin("ROUND306A_EDGE_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_edge_application_ledger.json.gz", 118_345_367, "6da4620a100c980f921350f162fda064580e603f8ff7221eeed768b8bd091d1f"),
    FrozenPin("ROUND306A_MEMBER_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_member_component_ledger.json.gz", 107_900_487, "710ebb660a7e7fad6a691c03bf845cf0081037ed09cc49a885c94c4bc472c276"),
    FrozenPin("ROUND306A_R305B_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_r305b_promoted_edge_application_ledger.json.gz", 5_012, "08f9ff2f5df0210cedd8cb3f8d998846e3722bd6bb0a2216d8d6c24a95a64a41"),
    FrozenPin("ROUND306A_R300A_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_r300a_reprojection_ledger.json.gz", 961_815, "c3e62f9833c333fb89758edd5c3f1648364a70b91bd1ed85650241a4cd10b673"),
    FrozenPin("ROUND306A_WTAIL_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_wtail_disposition_ledger.json.gz", 3_667, "6bdcc231b3cfd67f18ff3c62c27af08fdc9eb562a2c4e24a601798c0ad6d2556"),
    FrozenPin("ROUND306A_RESIDUAL_LEDGER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_residual_gate_ledger.json.gz", 797, "1e79d529f3ca1fcefa170263a5d8b88929361ea27c0eeb3c6de108b870f9d8b8"),
    FrozenPin("ROUND306A_RESULT", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_result.json", 9_827, "febe77da4285791b54e098c80a4b868c1e5dc6e43e98a7553bfff5e065075010"),
    FrozenPin("ROUND306A_VERIFIER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_promotion_verifier.py", 134_516, "60cc0f9cec6c8f4121f7ed7fde45b11e1b72bd9adc897364d9c0937c92a54c72"),
    FrozenPin("ROUND306A_ATTACK", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_attack_suite.json", 18_537, "9e3f2bcf3f39af739bc05ca2f3acef2828f96e6f19402fe6a85bb3353f5fc25e"),
    FrozenPin("ROUND306A_VERIFICATION", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_verification.json", 9_311, "38fd7f9d41dcf39a2ec887d72b31da3d003cf03eda154da34d3a5d87ff12ba7e"),
    FrozenPin("ROUND306A_REPORT", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_report.md", 9_175, "d2bd7d808736c333a4bb9b9af55d55d72e61e38023b1723c976d10eaae54671b"),
    FrozenPin("ROUND306A_COLD_REPLAY", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_cold_replay.md", 8_118, "ce3cb89ccf84ee6e6349afd5c3a9d92d6e981c3138b05fe3da791558d56c974e"),
)

ROUND306A_AUTHORITY_EXPECTATION: Final = {
    "verification_status": "PASS_EXACT_CACHELESS_ROUND306A_FRESH_LEGAL_COMPONENT_DSU_REBUILD",
    "formal_Round306A_promotion_permitted": True,
    "verification_last_and_sole_credit_marker": True,
    "member_ledger": {
        "row_count": 564_492,
        "ledger_sha256": "42d02c90e9e607f2d1c6ae53f5d2f67f0205c023f918a40fb1b64bec0213cafc",
        "row_ids_sha256": "befaf5ae8a8ae109912649201e5efd90a03898edc02b5518cadec93e1f835165",
        "row_hashes_sha256": "003ecfe414434477a404c7b1912bfd117e98fc4883faee36119144b877f923ad",
        "rows_sha256": "43bc3ca15f58b6dd089b776c6c21f68fb246eb6af0590974129e20beef93eabd",
    },
    "edge_ledger": {
        "row_count": 478_718,
        "ledger_sha256": "d253106bf33d892e254fa49dcd63a1e470600e827b61a20a34d401701303be1d",
        "row_ids_sha256": "31a9000f3e93f38698cf5f114a2f237924b381e3a3b2a143ce9cdcd01d254df5",
        "row_hashes_sha256": "dfd479ca56965f7b63644b296596587560b74ef0ace88999f2132918e689794d",
        "rows_sha256": "e3bf699433e828b345cc7da624b03f2768e5e427ce6bdf12b10543d08a718d4a",
    },
    "old_universe": {
        "member_count": 564_492,
        "base_root_count": 367_964,
        "component_count": 92_688,
        "rank_reduction": 275_276,
        "partition_sha256": "a3f7ce1e28a956a46803ef466709ded0053633f5e104746c6d1e6e51b873e19c",
    },
    "formal_credit_boundary": {
        "admitted_edge_applications": 478_718,
        "admitted_rank_reductions": 275_276,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    },
}

# Complete final R235D seal.  The manifest itself is first and its eight
# ordered members follow exactly in manifest order.
R235D_FINAL_PINS: Final[tuple[FrozenPin, ...]] = (
    FrozenPin("R235D_MANIFEST", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_manifest.sha256", 1_276, "0aa2128655e7f90eaeeda47a66901ea45e0908a6f569dc7760ead49ac539e7c0"),
    FrozenPin("R235D_PRODUCER", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_producer.py", 84_128, "d6d78b8ffb60c52a70294a83ff575c9d45efac4a1e618743e96ff503a15e7423"),
    FrozenPin("R235D_AUTHORITY_AND_INVALIDATION_LEDGER", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_row_commitment_ledger.jsonl.gz", 144_211, "6eaeee6a158ad7c0c3d62380214e1ae24ac2a63cb7678b312401cca91cb4cfe0"),
    FrozenPin("R235D_RESULT", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_result.json", 45_075, "3856a04a5b88574f1ffd6aac7f4fda42c014eac401c2a73efbc6c0ea10c9e5ff"),
    FrozenPin("R235D_INDEPENDENT_VERIFIER", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_independent_verifier.py", 88_342, "cc80855562d8ea8022881314647e6fe974ea8060b41e2c49c8ab48a28ac18559"),
    FrozenPin("R235D_ATTACK_SUITE", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_attack_suite.json", 1_340, "238309c6fea17edbcbe383e966383e57f8dd9bf888baff152bd09a0a28cd5236"),
    FrozenPin("R235D_VERIFICATION", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_verification.json", 1_740, "865f2aab8fab721aa24c0772d516806968555a28eb5529056e3cb6438d9d1468"),
    FrozenPin("R235D_REPORT", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_report.md", 3_893, "bd5604653adab6edb5c584b43d80e76001a6e324cf615fed269263e22d0fb192"),
    FrozenPin("R235D_COLD_REPLAY", "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_cold_replay.md", 1_134, "c36dbdf77460ebadec55d476d6d6401bed05466f569f627c583b55afd124aedd"),
)
R235D_REQUIRED_ROLES: Final = (
    "R235D_MANIFEST",
    "R235D_PRODUCER",
    "R235D_AUTHORITY_AND_INVALIDATION_LEDGER",
    "R235D_RESULT",
    "R235D_INDEPENDENT_VERIFIER",
    "R235D_ATTACK_SUITE",
    "R235D_VERIFICATION",
    "R235D_REPORT",
    "R235D_COLD_REPLAY",
)

EXPECTED_CENSUS: Final = {
    "old_member_count": 564_492,
    "invalid_member_count": 32,
    "invalid_target_sheet_count": 16,
    "invalid_target_only_side_count": 16,
    "corrected_member_count": 564_460,
    "old_base_root_count": 367_964,
    "affected_old_base_root_count": 20,
    "deleted_empty_base_root_count": 16,
    "rekeyed_nonempty_base_root_count": 4,
    "rekey_old_member_count_each": 2_878,
    "rekey_deleted_member_count_each": 4,
    "rekey_retained_member_count_each": 2_874,
    "corrected_base_root_count": 367_948,
    "legal_edge_application_count": 478_718,
    "fresh_rank_reduction_count": 275_276,
    "corrected_component_count": 92_672,
    "cross_component_pair_denominator": 158_820_108_554,
    "all_unordered_member_pairs": 159_307_263_570,
    "within_component_unordered_member_pairs": 487_155_016,
    "corrected_member_count_squared": 318_615_091_600,
    "sum_corrected_component_member_count_squared": 974_874_492,
    "old_all_unordered_member_pairs": 159_325_326_786,
    "old_within_component_unordered_member_pairs": 487_242_432,
    "old_member_count_squared": 318_651_218_064,
    "sum_old_component_member_count_squared": 975_049_356,
    "old_cross_component_pair_denominator": 158_838_084_354,
    "all_pair_decrease": 18_063_216,
    "within_component_pair_decrease": 87_416,
    "cross_component_pair_decrease": 17_975_800,
    "rekey_affected_old_component_member_sizes": [5_442, 5_442, 5_490, 5_490],
    "rekey_affected_corrected_component_member_sizes": [5_438, 5_438, 5_486, 5_486],
}

ROOT_DISPOSITION_CONTRACT: Final = {
    "old_base_root_disposition_row_count": 367_964,
    "disposition_histogram": {
        "DELETE_ROOT": 16,
        "REKEY_ROOT": 4,
        "KEEP_ROOT": 367_944,
    },
    "DELETE_ROOT_corrected_root_emission_count_each": 0,
    "REKEY_ROOT_corrected_root_emission_count_each": 1,
    "KEEP_ROOT_corrected_root_emission_count_each": 1,
    "corrected_base_root_output_count": 367_948,
    "rekey_is_injective": True,
    "rekey_target_is_fresh_against_every_keep_target": True,
    "rekey_binds_full_retained_member_set_and_source_row_sequence": True,
    "delete_requires_zero_edge_and_occurrence_hits": True,
}

STRICT_NONPROMOTION: Final = {
    "Round306C0_candidate_artifact_credit": 0,
    "normalized_full_support_credit": 0,
    "representation_pullback_credit": 0,
    "A1_A2_credit": 0,
    "B1A_credit": 0,
    "transition_atlas_credit": 0,
    "pair_routing_credit": 0,
    "B2_credit": 0,
    "maximality_credit": 0,
    "fibre_credit": 0,
    "global_disposition_credit": 0,
    "CM2": "NO-GO_FOR_CLAIM",
}

# Diagnostic values are not pins.  They must be recomputed from the final
# R235D invalidation ledger by both producer and independent verifier.
READ_ONLY_DIAGNOSTIC: Final = {
    "status": "NONFORMAL_READ_ONLY_DIAGNOSTIC__MUST_RECOMPUTE_AFTER_R235D_SEAL",
    "invalid_member_ids_sha256": "9c95eae730d5a033d65dadf2d27828b9876325e943049dd788ac1ed740687e52",
    "delete_root_sorted_lines_sha256": "d17748b7c15348fa3a196d6f556e95507350b3141ba365c94f27e8290cc10f89",
    "rekey_root_sorted_lines_sha256": "97b097d4c7b51daf4ffd0c9c8d100d0be41c6bccc26ebec84ea032e696528d4b",
    "corrected_partition_sha256": "1ae914d4e2cff22d1fa6ddad4ffe4679c594bde3cdad27acf1480202b7a89434",
    "forward_rank_flag_mismatch_count": 0,
    "delete_root_edge_or_occurrence_hit_count": 0,
    "invalid_member_occurrence_endpoint_hit_count": 0,
    "distinct_root_remap_collision_count": 0,
    "old_projected_self_root_cycle_row_count": 15_932,
    "old_projected_self_root_cycle_application_indices_sha256": "a391791492f3c871f67dd652c7183f7c14e2f006a70a82d380e178479ace943c",
    "old_projected_self_root_cycles_are_legal_and_must_not_be_rejected": True,
    "rekey_per_root_edge_row_hits": 336,
    "rekey_per_root_projected_root_slots": 518,
    "rekey_per_root_exact_occurrence_root_slots": 96,
    "rekey_per_root_combined_bound_slots": 614,
}

CORRECTED_OBLIGATION_CONTRACT: Final = {
    "status": "DOWNSTREAM_C1_CONTRACT_ONLY__NOT_A_FEATURE_LEDGER_ROW_COUNT",
    "superseded_old_theorem_obligation_census": 824_864,
    "corrected_G1": 38_608,
    "corrected_G2A": 38_608,
    "corrected_G2B_references": 76_816,
    "corrected_root_obligations": 351_888,
    "corrected_dependent_obligations": 472_912,
    "corrected_total_theorem_obligation_census": 824_800,
}

OUTPUTS: Final = {
    "authority_frontier": PREFIX + "_authority_frontier.json",
    "member_invalidation": PREFIX + "_member_invalidation_ledger.jsonl.gz",
    "root_disposition": PREFIX + "_base_root_disposition_ledger.jsonl.gz",
    "edge_remap": PREFIX + "_edge_remap_application_ledger.jsonl.gz",
    "member_component": PREFIX + "_fresh_member_component_ledger.jsonl.gz",
    "base_root_component": PREFIX + "_fresh_base_root_component_ledger.jsonl.gz",
    "component_census": PREFIX + "_fresh_component_census.jsonl.gz",
    "pair_denominator": PREFIX + "_cross_component_pair_denominator.json",
    "result": PREFIX + "_result.json",
}
OUTPUT_ORDER: Final = (
    "authority_frontier", "member_invalidation", "root_disposition",
    "edge_remap", "member_component", "base_root_component",
    "component_census", "pair_denominator", "result",
)

ROW_SCHEMAS: Final = {
    "member_invalidation": SCHEMA + ".member-invalidation-row.v1",
    "root_disposition": SCHEMA + ".base-root-disposition-row.v1",
    "edge_remap": SCHEMA + ".edge-remap-application-row.v1",
    "member_component": SCHEMA + ".fresh-member-component-row.v1",
    "base_root_component": SCHEMA + ".fresh-base-root-component-row.v1",
    "component_census": SCHEMA + ".fresh-component-census-row.v1",
}

ROW_FIELDS: Final = {
    "member_invalidation": (
        "schema", "row_id", "invalidation_role", "registry_member_id",
        "source_R235D_authority_ordinal", "source_R235D_invalidation_row_id",
        "source_R235D_invalidation_row_sha256",
        "source_Round306A_member_row_ordinal",
        "source_Round306A_member_row_id",
        "source_Round306A_member_row_wire_sha256",
        "source_Round306A_member_row_sha256", "old_base_root_id",
        "old_component_id",
        "formal_R248_correction_overlay_credit_without_independent_verification_marker",
        "row_sha256",
    ),
    "root_disposition": (
        "schema", "row_id", "old_base_root_id", "disposition",
        "old_member_count", "deleted_member_count", "deleted_member_ids",
        "deleted_member_ids_sha256",
        "retained_member_count", "retained_member_ids_sha256",
        "retained_source_row_sha256_sequence_sha256", "official_key_id",
        "canonical_input_commitment_sha256",
        "corrected_base_root_id_or_null", "old_component_id",
        "candidate_complete_selected_row_R248_correction_overlay",
        "formal_corrected_root_credit_without_independent_verification_marker",
        "row_sha256",
    ),
    "edge_remap": (
        "schema", "row_id", "application_index", "source_Round306A_row_id",
        "source_Round306A_row_wire_sha256", "source_Round306A_row_sha256",
        "source_channel", "source_row_id",
        "old_canonical_occurrence_endpoint_pair",
        "corrected_canonical_occurrence_endpoint_pair",
        "old_projected_base_root_pair",
        "corrected_projected_base_root_pair", "delete_root_hit_count",
        "invalid_member_endpoint_hit_count", "distinct_root_remap_collision",
        "forward_rank_reduction", "old_forward_rank_flag_match",
        "reverse_application_index", "reverse_rank_reduction",
        "formal_corrected_DSU_credit_without_independent_verification_marker",
        "row_sha256",
    ),
    "member_component": (
        "schema", "row_id", "registry_member_id",
        "source_Round306A_row_ordinal", "source_Round306A_row_id",
        "source_Round306A_row_wire_sha256", "source_Round306A_row_sha256",
        "old_base_root_id",
        "corrected_base_root_id", "root_disposition", "official_key_id",
        "corrected_component_id", "member_identity_preserved",
        "formal_corrected_member_universe_credit_without_independent_verification_marker",
        "formal_corrected_DSU_credit_without_independent_verification_marker",
        "row_sha256",
    ),
    "base_root_component": (
        "schema", "row_id", "corrected_base_root_id", "old_base_root_id",
        "root_disposition", "member_count", "member_ids_sha256",
        "official_key_id", "corrected_component_id", "edge_row_hit_count",
        "projected_root_slot_hit_count", "exact_occurrence_root_slot_hit_count",
        "formal_corrected_DSU_credit_without_independent_verification_marker",
        "row_sha256",
    ),
    "component_census": (
        "schema", "row_id", "corrected_component_id", "base_root_count",
        "base_root_ids_sha256", "member_count", "member_ids_sha256",
        "formal_corrected_DSU_credit_without_independent_verification_marker",
        "row_sha256",
    ),
}

ROW_ID_NAMESPACES: Final = {
    "member_invalidation": "round306c0-member-invalidation:",
    "root_disposition": "round306c0-base-root-disposition:",
    "edge_remap": "round306c0-edge-remap-application:",
    "member_component": "round306c0-member-component:",
    "base_root_component": "round306c0-base-root-component:",
    "component_census": "round306c0-component-census:",
}

LEDGER_ROW_COUNTS: Final = {
    "member_invalidation": 32,
    "root_disposition": 367_964,
    "edge_remap": 478_718,
    "member_component": 564_460,
    "base_root_component": 367_948,
    "component_census": 92_672,
}

REKEY_INPUT_SCHEMA: Final = "cm2.round306c0.corrected-base-root-rekey-input.v1"
R235D_ROW_SCHEMA: Final = (
    "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.row.v1"
)
ROUND306A_MEMBER_ROW_SCHEMA: Final = (
    "cm2.round306a.source-g-r305b-fresh-legal-component-dsu-rebuild.v1."
    "fresh-member-component-row.v1"
)
ROUND306A_EDGE_ROW_SCHEMA: Final = (
    "cm2.round306a.source-g-r305b-fresh-legal-component-dsu-rebuild.v1."
    "fresh-edge-application-row.v1"
)

REQUIRED_ATTACKS: Final = (
    "missing_or_mutated_R235D_invalidation_row",
    "sheet_side_role_swap_or_duplicate_member",
    "delete_only_sheets_and_silently_keep_target_only_sides",
    "delete_root_with_one_edge_or_occurrence_hit",
    "invalid_member_used_as_canonical_occurrence_endpoint",
    "omitted_rekey_or_noninjective_rekey_mapping",
    "projected_root_remapped_but_exact_occurrence_root_left_stale",
    "rekey_target_collision_with_existing_root",
    "cross_rekey_merge_or_distinct_pair_remap_collision",
    "incorrectly_rejecting_an_old_projected_self_root_cycle",
    "forward_rank_flag_mismatch",
    "forward_reverse_partition_mismatch",
    "wrong_component_namespace_or_stale_Round306A_component_id",
    "wrong_pair_denominator_or_component_size_square_sum",
    "wrong_all_within_cross_pair_delta_or_affected_component_size",
    "bool_int_alias_in_any_credit_or_count_field",
    "duplicate_json_key_nonintegral_number_or_noncanonical_separator",
    "gzip_multimember_trailing_bytes_or_decoded_row_over_8MiB",
    "manifest_substitution_symlink_hardlink_TOCTOU_or_late_first_pin",
    "TMPDIR_redirected_spill_into_deliverables",
    "seed_dependent_candidate_bytes",
    "default_contract_self_test_or_failed_preflight_writes_any_path",
)

ATTACK_MATRIX: Final = (
    ("A01", "R235D_ROW_DELETE", "R235D_EXACT_16_ROW_COVER", "REJECT"),
    ("A02", "INVALID_MEMBER_DUPLICATE", "EXACT_32_MEMBER_PARTITION", "REJECT"),
    ("A03", "SHEET_SIDE_ROLE_SWAP", "TYPED_INVALIDATION_ROLE", "REJECT"),
    ("A04", "KEEP_TARGET_ONLY_SIDE", "EXACT_INVALID_MEMBER_UNION", "REJECT"),
    ("A05", "DELETE_ROOT_EDGE_HIT_ONE", "DELETE_ROOT_ZERO_HIT", "REJECT"),
    ("A06", "INVALID_MEMBER_OCCURRENCE_ENDPOINT", "EDGE_ENDPOINT_EXCLUSION", "REJECT"),
    ("A07", "OMIT_ONE_REKEY", "EXACT_20_ROOT_DISPOSITION", "REJECT"),
    ("A08", "REKEY_COLLIDES_EXISTING_ROOT", "REKEY_TARGET_FRESHNESS", "REJECT"),
    ("A09", "TWO_OLD_ROOTS_REKEY_TO_ONE", "REKEY_INJECTIVITY", "REJECT"),
    ("A10", "LEAVE_EXACT_OCCURRENCE_ROOT_STALE", "BOTH_EDGE_ROOT_FIELDS_REMAP", "REJECT"),
    ("A11", "OLD_DISTINCT_TO_NEW_EQUAL", "DISTINCT_REMAP_COLLISION", "REJECT"),
    ("A12", "OLD_EQUAL_TO_NEW_EQUAL", "LEGAL_PROJECTED_SELF_CYCLE", "ACCEPT"),
    ("A13", "FORWARD_RANK_FLAG_FLIP", "EXACT_FORWARD_TRANSCRIPT", "REJECT"),
    ("A14", "REVERSE_PARTITION_CHANGE", "FORWARD_REVERSE_PARTITION", "REJECT"),
    ("A15", "STALE_COMPONENT_NAMESPACE", "ROUND306C0_NAMESPACE", "REJECT"),
    ("A16", "COMPONENT_SIZE_PLUS_ONE", "PAIR_ARITHMETIC", "REJECT"),
    ("A17", "CROSS_DENOMINATOR_MINUS_ONE", "PAIR_ARITHMETIC", "REJECT"),
    ("A18", "BOOLEAN_USED_AS_INTEGER_ONE", "TYPE_STRICT_SCALARS", "REJECT"),
    ("A19", "SECOND_GZIP_MEMBER", "SINGLE_GZIP_MEMBER", "REJECT"),
    ("A20", "FINAL_DECODED_ROW_OVER_8MIB", "POST_DECODE_ROW_CAP", "REJECT"),
    ("A21", "PIN_PATH_SYMLINK_OR_NLINK_TWO", "HELD_FD_PIN_IDENTITY", "REJECT"),
    ("A22", "LATE_FIRST_PIN_REPLACEMENT", "FINAL_ALL_PIN_REVALIDATION", "REJECT"),
    ("A23", "TMPDIR_POINTS_INTO_DELIVERABLES", "FIXED_EXTERNAL_SPILL_ROOT", "REJECT"),
    ("A24", "SECOND_SEED_CHANGES_ONE_BYTE", "DUAL_SEED_BYTE_IDENTITY", "REJECT"),
    ("A25", "FAILED_PREFLIGHT_CREATES_CANDIDATE_PATH", "PREPATH_NO_WRITE", "REJECT"),
)


def _strict_int(value: Any, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ProductionBlocked("non-strict nonnegative integer: " + label)
    return value


def _strict_bool(value: Any, label: str) -> bool:
    if type(value) is not bool:
        raise ProductionBlocked("non-strict boolean: " + label)
    return value


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _fixed_spill_root_ignoring_tmpdir(tmpdir_value: Any, deliverables: Path) -> str:
    if type(tmpdir_value) is not str:
        raise ProductionBlocked("TMPDIR type")
    fixed = os.path.abspath(FIXED_EXTERNAL_SPILL_ROOT)
    parent = os.path.abspath(os.fspath(deliverables))
    if os.path.commonpath((fixed, parent)) == parent:
        raise ProductionBlocked("fixed spill root lies inside deliverables")
    return fixed


def _is_distinct_root_remap_collision(
    old_pair: tuple[str, str], corrected_pair: tuple[str, str]
) -> bool:
    if (
        type(old_pair) is not tuple
        or type(corrected_pair) is not tuple
        or len(old_pair) != 2
        or len(corrected_pair) != 2
        or not all(type(item) is str for item in old_pair + corrected_pair)
    ):
        raise ProductionBlocked("malformed root pair")
    return old_pair[0] != old_pair[1] and corrected_pair[0] == corrected_pair[1]


def _pair_arithmetic_from_n_and_square_sum(n: Any, square_sum: Any) -> dict[str, int]:
    n = _strict_int(n, "member count")
    square_sum = _strict_int(square_sum, "component size square sum")
    if n < 0 or square_sum < n or (square_sum - n) % 2:
        raise ProductionBlocked("invalid pair arithmetic inputs")
    all_pairs = n * (n - 1) // 2
    within = (square_sum - n) // 2
    cross = (n * n - square_sum) // 2
    if cross != all_pairs - within:
        raise ProductionBlocked("pair arithmetic identity")
    return {
        "member_count": n,
        "member_count_squared": n * n,
        "component_size_square_sum": square_sum,
        "all_pairs": all_pairs,
        "within": within,
        "cross": cross,
    }


def _census_self_check(
    census: Any = EXPECTED_CENSUS,
    diagnostic: Any = READ_ONLY_DIAGNOSTIC,
    root_contract: Any = ROOT_DISPOSITION_CONTRACT,
) -> dict[str, Any]:
    if type(census) is not dict or type(diagnostic) is not dict:
        raise AssertionError("census or diagnostic type")
    if type(root_contract) is not dict:
        raise AssertionError("root disposition contract type")
    if not _same_typed(census, EXPECTED_CENSUS):
        raise AssertionError("exact type-strict C0 census vector")
    if not _same_typed(diagnostic, READ_ONLY_DIAGNOSTIC):
        raise AssertionError("exact type-strict read-only diagnostic vector")
    if not _same_typed(root_contract, ROOT_DISPOSITION_CONTRACT):
        raise AssertionError("exact type-strict root disposition contract")

    exact_scalars = {
        "old_member_count": 564_492,
        "invalid_member_count": 32,
        "corrected_member_count": 564_460,
        "old_base_root_count": 367_964,
        "affected_old_base_root_count": 20,
        "deleted_empty_base_root_count": 16,
        "rekeyed_nonempty_base_root_count": 4,
        "corrected_base_root_count": 367_948,
        "legal_edge_application_count": 478_718,
        "fresh_rank_reduction_count": 275_276,
        "corrected_component_count": 92_672,
        "cross_component_pair_denominator": 158_820_108_554,
        "corrected_member_count_squared": 318_615_091_600,
        "sum_corrected_component_member_count_squared": 974_874_492,
    }
    for key, expected in exact_scalars.items():
        if _strict_int(census.get(key), key) != expected:
            raise AssertionError("exact corrected census scalar: " + key)
    if census["old_member_count"] - census["invalid_member_count"] != census[
        "corrected_member_count"
    ]:
        raise AssertionError("member correction equation")
    if census["old_base_root_count"] - census[
        "deleted_empty_base_root_count"
    ] != census["corrected_base_root_count"]:
        raise AssertionError("base-root correction equation")
    if census["affected_old_base_root_count"] != (
        census["deleted_empty_base_root_count"]
        + census["rekeyed_nonempty_base_root_count"]
    ):
        raise AssertionError("affected root equation")
    if census["corrected_base_root_count"] - census[
        "fresh_rank_reduction_count"
    ] != census["corrected_component_count"]:
        raise AssertionError("fresh DSU rank equation")
    if census["rekey_old_member_count_each"] - census[
        "rekey_deleted_member_count_each"
    ] != census["rekey_retained_member_count_each"]:
        raise AssertionError("rekey retained-member equation")

    corrected = _pair_arithmetic_from_n_and_square_sum(
        census["corrected_member_count"],
        census["sum_corrected_component_member_count_squared"],
    )
    old = _pair_arithmetic_from_n_and_square_sum(
        census["old_member_count"], census["sum_old_component_member_count_squared"]
    )
    corrected_expected = {
        "member_count": census["corrected_member_count"],
        "member_count_squared": census["corrected_member_count_squared"],
        "component_size_square_sum": census[
            "sum_corrected_component_member_count_squared"
        ],
        "all_pairs": census["all_unordered_member_pairs"],
        "within": census["within_component_unordered_member_pairs"],
        "cross": census["cross_component_pair_denominator"],
    }
    old_expected = {
        "member_count": census["old_member_count"],
        "member_count_squared": census["old_member_count_squared"],
        "component_size_square_sum": census[
            "sum_old_component_member_count_squared"
        ],
        "all_pairs": census["old_all_unordered_member_pairs"],
        "within": census["old_within_component_unordered_member_pairs"],
        "cross": census["old_cross_component_pair_denominator"],
    }
    if not _same_typed(corrected, corrected_expected):
        raise AssertionError("corrected pair arithmetic")
    if not _same_typed(old, old_expected):
        raise AssertionError("old pair arithmetic")
    deltas = {
        "all": old["all_pairs"] - corrected["all_pairs"],
        "within": old["within"] - corrected["within"],
        "cross": old["cross"] - corrected["cross"],
    }
    expected_deltas = {
        "all": census["all_pair_decrease"],
        "within": census["within_component_pair_decrease"],
        "cross": census["cross_component_pair_decrease"],
    }
    if not _same_typed(deltas, expected_deltas):
        raise AssertionError("old/corrected pair deltas")

    old_sizes = census["rekey_affected_old_component_member_sizes"]
    corrected_sizes = census["rekey_affected_corrected_component_member_sizes"]
    if not _same_typed(old_sizes, [5_442, 5_442, 5_490, 5_490]):
        raise AssertionError("affected old component sizes")
    if not _same_typed(corrected_sizes, [5_438, 5_438, 5_486, 5_486]):
        raise AssertionError("affected corrected component sizes")
    if any(old_size - new_size != 4 for old_size, new_size in zip(old_sizes, corrected_sizes)):
        raise AssertionError("affected component deletion count")
    choose2 = lambda value: value * (value - 1) // 2
    affected_within_delta = sum(
        choose2(old_size) - choose2(new_size)
        for old_size, new_size in zip(old_sizes, corrected_sizes)
    )
    if affected_within_delta != census["within_component_pair_decrease"]:
        raise AssertionError("affected component within-pair delta")

    expected_histogram = {
        "DELETE_ROOT": 16,
        "REKEY_ROOT": 4,
        "KEEP_ROOT": 367_944,
    }
    if not _same_typed(
        root_contract.get("disposition_histogram"), expected_histogram
    ):
        raise AssertionError("exact root disposition histogram")
    if _strict_int(
        root_contract.get("old_base_root_disposition_row_count"),
        "root disposition rows",
    ) != census["old_base_root_count"]:
        raise AssertionError("root disposition row count")
    if sum(expected_histogram.values()) != census["old_base_root_count"]:
        raise AssertionError("root disposition cover")
    emitted_roots = (
        expected_histogram["REKEY_ROOT"]
        * _strict_int(
            root_contract.get("REKEY_ROOT_corrected_root_emission_count_each"),
            "rekey emission",
        )
        + expected_histogram["KEEP_ROOT"]
        * _strict_int(
            root_contract.get("KEEP_ROOT_corrected_root_emission_count_each"),
            "keep emission",
        )
        + expected_histogram["DELETE_ROOT"]
        * _strict_int(
            root_contract.get("DELETE_ROOT_corrected_root_emission_count_each"),
            "delete emission",
        )
    )
    if emitted_roots != census["corrected_base_root_count"]:
        raise AssertionError("corrected root emission equation")
    for key in (
        "rekey_is_injective",
        "rekey_target_is_fresh_against_every_keep_target",
        "rekey_binds_full_retained_member_set_and_source_row_sequence",
        "delete_requires_zero_edge_and_occurrence_hits",
    ):
        if _strict_bool(root_contract.get(key), key) is not True:
            raise AssertionError("root disposition boolean: " + key)
    if root_contract.get("corrected_base_root_output_count") != census[
        "corrected_base_root_count"
    ]:
        raise AssertionError("root output count")

    if diagnostic.get("corrected_partition_sha256") != (
        "1ae914d4e2cff22d1fa6ddad4ffe4679c594bde3cdad27acf1480202b7a89434"
    ):
        raise AssertionError("corrected partition diagnostic")
    if not _is_sha256(diagnostic["corrected_partition_sha256"]):
        raise AssertionError("corrected partition digest format")
    diagnostic_zero_keys = (
        "forward_rank_flag_mismatch_count",
        "delete_root_edge_or_occurrence_hit_count",
        "invalid_member_occurrence_endpoint_hit_count",
        "distinct_root_remap_collision_count",
    )
    for key in diagnostic_zero_keys:
        if _strict_int(diagnostic.get(key), key) != 0:
            raise AssertionError("nonzero diagnostic gap: " + key)
    if _strict_int(
        diagnostic.get("old_projected_self_root_cycle_row_count"),
        "old self-root cycles",
    ) != 15_932:
        raise AssertionError("old self-root cycle count")
    if _strict_bool(
        diagnostic.get(
            "old_projected_self_root_cycles_are_legal_and_must_not_be_rejected"
        ),
        "old self-root cycle legality",
    ) is not True:
        raise AssertionError("old self-root cycle legality")
    return {
        "corrected_pair_arithmetic": corrected,
        "old_pair_arithmetic": old,
        "pair_deltas": deltas,
        "root_disposition_histogram": expected_histogram,
        "affected_four_component_within_delta": affected_within_delta,
        "corrected_partition_sha256": diagnostic["corrected_partition_sha256"],
    }


def _run_pure_contract_attacks() -> dict[str, Any]:
    census = _census_self_check()
    accepted_self_cycle = not _is_distinct_root_remap_collision(
        ("old-a", "old-a"), ("new-a", "new-a")
    )
    rejected_distinct_collision = _is_distinct_root_remap_collision(
        ("old-a", "old-b"), ("new-z", "new-z")
    )
    boolean_rejected = False
    try:
        _strict_int(True, "bool alias attack")
    except ProductionBlocked:
        boolean_rejected = True
    malformed_pair_rejections = 0
    for old_pair, corrected_pair in (
        (["old-a", "old-b"], ("new-a", "new-b")),
        (("old-a",), ("new-a", "new-b")),
        (("old-a", True), ("new-a", "new-b")),
    ):
        try:
            _is_distinct_root_remap_collision(old_pair, corrected_pair)  # type: ignore[arg-type]
        except ProductionBlocked:
            malformed_pair_rejections += 1
    if not (accepted_self_cycle and rejected_distinct_collision and boolean_rejected):
        raise AssertionError("pure mutation predicates")
    if malformed_pair_rejections != 3:
        raise AssertionError("malformed root pair mutations")
    return {
        "status": "PASS_PURE_C0_CONTRACT_MUTATION_PREDICATES",
        "executed_case_count": 9,
        "legal_old_projected_self_cycle_accepted": True,
        "old_distinct_to_new_equal_rejected": True,
        "boolean_integer_alias_rejected": True,
        "malformed_root_pair_mutations_rejected": malformed_pair_rejections,
        "census_equations": census,
    }


def _file_identity(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def _held_fd_hash(path: Path) -> tuple[str, tuple[int, ...]]:
    before = path.stat(follow_symlinks=False)
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise ProductionBlocked("pin is not a one-link regular file: " + path.name)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        opened = os.fstat(fd)
        if _file_identity(opened) != _file_identity(before):
            raise ProductionBlocked("pin changed before held-FD open: " + path.name)
        hasher = hashlib.sha256()
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
        after_fd = os.fstat(fd)
    finally:
        os.close(fd)
    after_path = path.stat(follow_symlinks=False)
    identity = _file_identity(opened)
    if _file_identity(after_fd) != identity or _file_identity(after_path) != identity:
        raise ProductionBlocked("pin changed during held-FD hash: " + path.name)
    return hasher.hexdigest(), identity


def _held_fd_read_exact(path: Path, expected_identity: tuple[int, ...]) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    chunks: list[bytes] = []
    try:
        opened = os.fstat(fd)
        if _file_identity(opened) != expected_identity:
            raise ProductionBlocked("pin changed before exact held-FD read: " + path.name)
        while True:
            chunk = os.read(fd, 64 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after_fd = os.fstat(fd)
    finally:
        os.close(fd)
    after_path = path.stat(follow_symlinks=False)
    if (
        _file_identity(after_fd) != expected_identity
        or _file_identity(after_path) != expected_identity
    ):
        raise ProductionBlocked("pin changed during exact held-FD read: " + path.name)
    return b"".join(chunks)


def audit_round306a_pins_read_only() -> dict[str, Any]:
    """Two-pass exact stat/hash audit; never imports or executes an upstream file."""

    data = Path(__file__).resolve(strict=True).parent
    pins = (ROUND306A_MANIFEST, *ROUND306A_MANIFEST_MEMBERS)
    if len(ROUND306A_MANIFEST_MEMBERS) != 13 or len(pins) != 14:
        raise ProductionBlocked("Round306A exact thirteen-member frontier")
    if len({pin.role for pin in pins}) != len(pins):
        raise ProductionBlocked("duplicate Round306A pin role")
    if len({pin.filename for pin in pins}) != len(pins):
        raise ProductionBlocked("duplicate Round306A pin filename")
    for pin in pins:
        candidate = Path(pin.filename)
        if (
            type(pin.role) is not str
            or type(pin.filename) is not str
            or not pin.role
            or not pin.filename
            or candidate.is_absolute()
            or len(candidate.parts) != 1
            or candidate.name != pin.filename
            or type(pin.size) is not int
            or pin.size < 0
            or not _is_sha256(pin.sha256)
        ):
            raise ProductionBlocked("malformed Round306A pin: " + str(pin.role))
    first: dict[str, tuple[str, tuple[int, ...]]] = {}
    for pin in pins:
        path = data / pin.filename
        actual_hash, identity = _held_fd_hash(path)
        if identity[4] != pin.size or actual_hash != pin.sha256:
            raise ProductionBlocked("Round306A frozen pin mismatch: " + pin.role)
        first[pin.role] = (actual_hash, identity)
    for pin in reversed(pins):
        actual_hash, identity = _held_fd_hash(data / pin.filename)
        if first[pin.role] != (actual_hash, identity):
            raise ProductionBlocked("Round306A two-pass mismatch: " + pin.role)
    manifest_bytes = _held_fd_read_exact(
        data / ROUND306A_MANIFEST.filename,
        first[ROUND306A_MANIFEST.role][1],
    )
    if hashlib.sha256(manifest_bytes).hexdigest() != ROUND306A_MANIFEST.sha256:
        raise ProductionBlocked("Round306A manifest changed before exact parse")
    manifest_lines = manifest_bytes.decode("ascii").splitlines()
    expected_lines = [
        pin.sha256 + "  " + pin.filename for pin in ROUND306A_MANIFEST_MEMBERS
    ]
    if manifest_lines != expected_lines:
        raise ProductionBlocked("Round306A manifest exact ordered member mismatch")
    by_role = {pin.role: pin for pin in pins}
    result_bytes = _held_fd_read_exact(
        data / by_role["ROUND306A_RESULT"].filename,
        first["ROUND306A_RESULT"][1],
    )
    verification_bytes = _held_fd_read_exact(
        data / by_role["ROUND306A_VERIFICATION"].filename,
        first["ROUND306A_VERIFICATION"][1],
    )
    result = strict_canonical_json(result_bytes, "ROUND306A_RESULT")
    verification = strict_canonical_json(
        verification_bytes, "ROUND306A_VERIFICATION"
    )
    observed_authority = {
        "verification_status": verification["status"],
        "formal_Round306A_promotion_permitted": verification[
            "formal_Round306A_promotion_permitted"
        ],
        "verification_last_and_sole_credit_marker": verification[
            "formal_credit_marker_definition"
        ]["verification_last_and_sole_credit_marker"],
        "member_ledger": {
            key: result["output_ledgers"]["member"][key]
            for key in (
                "row_count", "ledger_sha256", "row_ids_sha256",
                "row_hashes_sha256", "rows_sha256",
            )
        },
        "edge_ledger": {
            key: result["output_ledgers"]["edge"][key]
            for key in (
                "row_count", "ledger_sha256", "row_ids_sha256",
                "row_hashes_sha256", "rows_sha256",
            )
        },
        "old_universe": {
            "member_count": result["member_universe"]["member_count"],
            "base_root_count": result["member_universe"]["base_root_count"],
            "component_count": result["fresh_forward_application"]["component_count"],
            "rank_reduction": result["fresh_forward_application"]["rank_reduction"],
            "partition_sha256": result["fresh_forward_application"]["partition_sha256"],
        },
        "formal_credit_boundary": {
            "admitted_edge_applications": verification[
                "formal_credit_transition_at_this_verification_commit_marker"
            ]["officially_admitted_fresh_legal_component_edge_application_count"],
            "admitted_rank_reductions": verification[
                "formal_credit_transition_at_this_verification_commit_marker"
            ]["officially_admitted_fresh_DSU_rank_reduction_count"],
            "formal_maximality_credit": verification[
                "formal_credit_transition_at_this_verification_commit_marker"
            ]["formal_maximality_credit"],
            "formal_fibre_credit": verification[
                "formal_credit_transition_at_this_verification_commit_marker"
            ]["formal_fibre_credit"],
            "formal_global_disposition_credit": verification[
                "formal_credit_transition_at_this_verification_commit_marker"
            ]["formal_global_disposition_credit"],
        },
    }
    if canonical_bytes(observed_authority) != canonical_bytes(
        ROUND306A_AUTHORITY_EXPECTATION
    ):
        raise ProductionBlocked("Round306A semantic authority marker mismatch")
    forward_reverse_keys = (
        "component_count", "rank_reduction", "partition_sha256"
    )
    forward_snapshot = {
        key: result["fresh_forward_application"][key]
        for key in forward_reverse_keys
    }
    reverse_snapshot = {
        key: result["fresh_reverse_application"][key]
        for key in forward_reverse_keys
    }
    if not _same_typed(forward_snapshot, reverse_snapshot):
        raise ProductionBlocked("Round306A forward/reverse seal mismatch")

    # The final reverse-order all-path pass closes the late-first-pin window
    # after manifest and semantic parsing.  Identity contains mode, nlink,
    # size, mtime and ctime in addition to device/inode.
    for pin in reversed(pins):
        current = (data / pin.filename).stat(follow_symlinks=False)
        if _file_identity(current) != first[pin.role][1]:
            raise ProductionBlocked("Round306A late first-pin replacement: " + pin.role)
    return {
        "status": "PASS_TWO_PASS_HELD_FD_EXACT_ROUND306A_PIN_AUDIT",
        "pin_count_including_manifest": len(pins),
        "manifest_member_count": len(ROUND306A_MANIFEST_MEMBERS),
        "total_bytes": sum(pin.size for pin in pins),
        "manifest_sha256": ROUND306A_MANIFEST.sha256,
        "producer_or_verifier_imported_or_executed": False,
        "two_pass_held_fd_and_final_all_path_identity_revalidation": True,
        "symlink_and_hardlink_fail_close": True,
        "semantic_authority_status": "PASS_FORMAL_ROUND306A_REPLACEMENT_CERTIFICATE_BOUNDARY",
        "semantic_authority_expectation_sha256": digest(
            ROUND306A_AUTHORITY_EXPECTATION
        ),
    }


ROUND306A_MEMBER_FIELDS: Final = frozenset({
    "Round306A_fresh_member_component_row_id", "schema",
    "registry_occurrence_id", "base_root_id", "official_key_id",
    "final_component_id", "member_identity_preserved",
    "formal_maximality_credit", "formal_fibre_credit",
    "formal_global_disposition_credit", "row_sha256",
})
ROUND306A_EDGE_FIELDS: Final = frozenset({
    "Round306A_fresh_edge_application_row_id", "schema", "application_index",
    "source_channel", "source_row_id", "source_row_sha256",
    "canonical_occurrence_endpoint_pair", "projected_base_root_pair",
    "fed_to_new_empty_DSU", "forward_rank_reduction",
    "forward_cycle_or_redundant", "candidate_DSU_rank_reduction",
    "serialized_Round304_partition_used_as_state",
    "formal_credit_without_independent_verification_marker",
    "formal_maximality_credit", "formal_fibre_credit",
    "formal_global_disposition_credit", "row_sha256",
})
ROUND306A_LEDGER_FIELDS: Final = frozenset({
    "schema", "schema_snapshot_sha256", "status", "row_count",
    "row_ids_sha256", "row_hashes_sha256", "rows_sha256", "ledger_sha256",
})
SOURCE_DECODE_CAP: Final = 768 * 1024 * 1024


def _digest_canonical_sequence(values: Iterable[Any]) -> str:
    state = hashlib.sha256(b"[")
    first = True
    for value in values:
        if not first:
            state.update(b",")
        state.update(canonical_bytes(value))
        first = False
    state.update(b"]")
    return state.hexdigest()


def _strict_gzip_single_member(raw: bytes, label: str, cap: int) -> bytes:
    if type(raw) is not bytes or not raw:
        raise ProductionBlocked("empty gzip input: " + label)
    inflater = zlib.decompressobj(16 + zlib.MAX_WBITS)
    decoded = inflater.decompress(raw, cap + 1)
    if len(decoded) > cap or inflater.unconsumed_tail:
        raise ProductionBlocked("decoded gzip cap exceeded: " + label)
    decoded += inflater.flush()
    if len(decoded) > cap:
        raise ProductionBlocked("decoded gzip cap exceeded after final decode: " + label)
    if not inflater.eof or inflater.unused_data:
        raise ProductionBlocked("gzip multimember or trailing bytes: " + label)
    return decoded


def _pin_vector_audit(
    label: str,
    manifest: FrozenPin,
    members: tuple[FrozenPin, ...],
) -> tuple[dict[str, tuple[str, tuple[int, ...]]], dict[str, Any]]:
    data = Path(__file__).resolve(strict=True).parent
    pins = (manifest, *members)
    if len({pin.role for pin in pins}) != len(pins):
        raise ProductionBlocked(label + " duplicate pin role")
    if len({pin.filename for pin in pins}) != len(pins):
        raise ProductionBlocked(label + " duplicate pin filename")
    for pin in pins:
        lexical = Path(pin.filename)
        if (
            type(pin.role) is not str
            or type(pin.filename) is not str
            or not pin.role
            or not pin.filename
            or lexical.is_absolute()
            or len(lexical.parts) != 1
            or lexical.name != pin.filename
            or type(pin.size) is not int
            or pin.size < 0
            or not _is_sha256(pin.sha256)
        ):
            raise ProductionBlocked(label + " malformed pin: " + str(pin.role))
    first: dict[str, tuple[str, tuple[int, ...]]] = {}
    for pin in pins:
        actual_hash, identity = _held_fd_hash(data / pin.filename)
        if actual_hash != pin.sha256 or identity[4] != pin.size:
            raise ProductionBlocked(label + " pin mismatch: " + pin.role)
        first[pin.role] = (actual_hash, identity)
    for pin in reversed(pins):
        actual_hash, identity = _held_fd_hash(data / pin.filename)
        if first[pin.role] != (actual_hash, identity):
            raise ProductionBlocked(label + " two-pass pin mismatch: " + pin.role)
    manifest_raw = _held_fd_read_exact(
        data / manifest.filename, first[manifest.role][1]
    )
    expected_lines = [pin.sha256 + "  " + pin.filename for pin in members]
    try:
        observed_lines = manifest_raw.decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        raise ProductionBlocked(label + " non-ASCII manifest") from exc
    if observed_lines != expected_lines:
        raise ProductionBlocked(label + " ordered manifest mismatch")
    receipt = {
        "status": "PASS_EXACT_TWO_PASS_HELD_FD_PIN_AUDIT",
        "pin_count_including_manifest": len(pins),
        "manifest_member_count": len(members),
        "total_bytes": sum(pin.size for pin in pins),
        "manifest_sha256": manifest.sha256,
        "manifest_ordered_member_lines_sha256": digest(expected_lines),
        "producer_or_verifier_imported_or_executed": False,
        "symlink_and_hardlink_fail_close": True,
        "final_all_pin_path_revalidation_required": True,
    }
    return first, receipt


def _final_all_pin_path_revalidation(
    states: tuple[
        tuple[tuple[FrozenPin, ...], dict[str, tuple[str, tuple[int, ...]]]], ...
    ]
) -> None:
    data = Path(__file__).resolve(strict=True).parent
    for pins, first in states:
        for pin in reversed(pins):
            observed_hash, observed_identity = _held_fd_hash(data / pin.filename)
            if first[pin.role] != (observed_hash, observed_identity):
                raise ProductionBlocked("late first-pin replacement: " + pin.role)


def _read_pinned(
    pin: FrozenPin,
    first: dict[str, tuple[str, tuple[int, ...]]],
) -> bytes:
    data = Path(__file__).resolve(strict=True).parent
    raw = _held_fd_read_exact(data / pin.filename, first[pin.role][1])
    if len(raw) != pin.size or hashlib.sha256(raw).hexdigest() != pin.sha256:
        raise ProductionBlocked("pinned read mismatch: " + pin.role)
    return raw


def _semantic_r235d_audit(
    first: dict[str, tuple[str, tuple[int, ...]]]
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    by_role = {pin.role: pin for pin in R235D_FINAL_PINS}
    result = strict_canonical_json(
        _read_pinned(by_role["R235D_RESULT"], first), "R235D_RESULT"
    )
    verification = strict_canonical_json(
        _read_pinned(by_role["R235D_VERIFICATION"], first), "R235D_VERIFICATION"
    )
    if (
        result.get("schema")
        != "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.result.v1"
        or result.get("result_sha256")
        != "abe7b63dc02f5d3772fa50add64030d3822b3832a33df8a05fcf98926b0dfbbe"
    ):
        raise ProductionBlocked("R235D exact result marker")
    result_payload = result.get("result")
    if type(result_payload) is not dict or digest(result_payload) != result["result_sha256"]:
        raise ProductionBlocked("R235D result digest closure")
    if (
        verification.get("schema")
        != "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.verification.v1"
        or verification.get("result_sha256")
        != "b0b43f4acb3da02e9e4615e2670dfaeab511a3437b2449c834d68bf0faa46867"
    ):
        raise ProductionBlocked("R235D exact verification marker")
    verification_payload = verification.get("result")
    if (
        type(verification_payload) is not dict
        or digest(verification_payload) != verification["result_sha256"]
        or verification_payload.get("status")
        != "PASS_INDEPENDENT_16_ROW_THEOREM_AND_32_MEMBER_20_ROOT_OLD_FREEZE_INVALIDATION_REPLAY__ZERO_GLOBAL_CREDIT"
        or verification_payload.get("manifest_first_sealed_validation") is not True
        or verification_payload.get("producer_imported_or_executed") is not False
        or verification_payload.get("K1_imported_or_executed") is not False
        or verification_payload.get("independent_invalid_members") != 32
        or verification_payload.get("independent_old_root_dispositions") != 20
        or verification_payload.get("independent_package_wide_invalidation_claimed") is not False
    ):
        raise ProductionBlocked("R235D independent verification semantics")
    authority = result_payload.get("authority_ledger")
    expected_authority = {
        "compression": "gzip-mtime-zero",
        "filename": by_role["R235D_AUTHORITY_AND_INVALIDATION_LEDGER"].filename,
        "ordered_conclusion_sha256_sequence_sha256": "80696026c4e0330018aea5ef42790817c38de145e0d13dff0ab9891c50d37a99",
        "ordered_row_sha256_sequence_sha256": "5e86ab1a1aac133875c13b4fde344fa1b8db42fee770d23b0ba716c7e0b5571d",
        "row_count": 16,
        "row_schema": R235D_ROW_SCHEMA,
        "sha256": by_role["R235D_AUTHORITY_AND_INVALIDATION_LEDGER"].sha256,
    }
    if not _same_typed(authority, expected_authority):
        raise ProductionBlocked("R235D authority-ledger descriptor")
    compressed = _read_pinned(
        by_role["R235D_AUTHORITY_AND_INVALIDATION_LEDGER"], first
    )
    decoded = _strict_gzip_single_member(compressed, "R235D_LEDGER", 64 * 1024 * 1024)
    if not decoded.endswith(b"\n") or decoded.endswith(b"\n\n"):
        raise ProductionBlocked("R235D exact JSONL terminal newline")
    rows: list[dict[str, Any]] = []
    for ordinal, line in enumerate(decoded[:-1].split(b"\n")):
        if len(line) > MAX_DECODED_ROW_BYTES:
            raise ProductionBlocked("R235D decoded row cap")
        row = strict_canonical_json(line, "R235D_ROW_" + str(ordinal))
        if (
            type(row) is not dict
            or row.get("schema") != R235D_ROW_SCHEMA
            or row.get("authority_ordinal") != ordinal
            or type(row.get("authority_row_id")) is not str
            or not _is_sha256(row.get("conclusion_sha256"))
        ):
            raise ProductionBlocked("R235D row schema/order")
        rows.append(row)
    row_wire_hashes = [hashlib.sha256(canonical_bytes(row)).hexdigest() for row in rows]
    conclusion_hashes = [row["conclusion_sha256"] for row in rows]
    if (
        len(rows) != 16
        or _digest_canonical_sequence(row_wire_hashes)
        != authority["ordered_row_sha256_sequence_sha256"]
        or _digest_canonical_sequence(conclusion_hashes)
        != authority["ordered_conclusion_sha256_sequence_sha256"]
    ):
        raise ProductionBlocked("R235D exact row commitment sequence")
    downstream = result_payload.get("downstream_invalidation")
    if type(downstream) is not dict:
        raise ProductionBlocked("R235D downstream invalidation object")
    mandatory = downstream.get("mandatory_rebuild")
    selected_scope = downstream.get("selected_pinned_artifact_invalidation_scope")
    if (
        type(mandatory) is not dict
        or mandatory.get("fresh_Round306A_forward_and_reverse_DSU_required") is not True
        or mandatory.get("legal_edge_application_count_to_replay") != 478_718
        or mandatory.get("regenerate_R248_from_corrected_partition") is not True
        or mandatory.get("old_component_and_pair_projection_may_not_be_minted") is not True
        or type(selected_scope) is not dict
        or selected_scope.get("package_wide_invalidation_claimed") is not False
        or selected_scope.get("unhashed_package_members_are_not_asserted_invalid") is not True
        or downstream.get("old_freeze_invalidated") is not True
    ):
        raise ProductionBlocked("R235D selected-row invalidation scope")
    receipt = {
        "status": "PASS_FINAL_R235D_SELECTED_ROW_INVALIDATION_AUTHORITY",
        "result_sha256": result["result_sha256"],
        "verification_result_sha256": verification["result_sha256"],
        "authority_ledger_sha256": authority["sha256"],
        "authority_row_count": 16,
        "invalid_member_count": 32,
        "affected_old_root_count": 20,
        "package_wide_invalidation_claimed": False,
        "fresh_R248_correction_overlay_required": True,
        "producer_or_verifier_imported_or_executed": False,
    }
    return result, verification, rows, receipt


def _validate_round306a_ledger(
    document: Any,
    key: str,
    table: str,
    row_schema: str,
    fields: frozenset[str],
    id_field: str,
    expected: dict[str, Any],
) -> list[dict[str, Any]]:
    if type(document) is not dict or set(document) != ROUND306A_LEDGER_FIELDS | {table}:
        raise ProductionBlocked("Round306A " + key + " ledger fields")
    rows = document.get(table)
    if type(rows) is not list or document.get("row_count") != len(rows):
        raise ProductionBlocked("Round306A " + key + " row count")
    if document.get("row_count") != expected["row_count"]:
        raise ProductionBlocked("Round306A " + key + " expected count")
    ids: list[str] = []
    hashes: list[str] = []
    previous_member_id: str | None = None
    for ordinal, row in enumerate(rows):
        if (
            type(row) is not dict
            or set(row) != fields
            or row.get("schema") != row_schema
            or type(row.get(id_field)) is not str
            or not _is_sha256(row.get("row_sha256"))
        ):
            raise ProductionBlocked("Round306A " + key + " row schema")
        if len(canonical_bytes(row)) > MAX_DECODED_ROW_BYTES:
            raise ProductionBlocked("Round306A " + key + " decoded row cap")
        row_payload = dict(row)
        claimed = row_payload.pop("row_sha256")
        if digest(row_payload) != claimed:
            raise ProductionBlocked("Round306A " + key + " row self hash")
        row_id = row[id_field]
        if key == "member":
            member_id = row.get("registry_occurrence_id")
            if (
                type(member_id) is not str
                or (
                    previous_member_id is not None
                    and member_id <= previous_member_id
                )
            ):
                raise ProductionBlocked("Round306A registry-member row order")
            previous_member_id = member_id
        if key == "edge" and row.get("application_index") != ordinal:
            raise ProductionBlocked("Round306A edge application order")
        ids.append(row_id)
        hashes.append(claimed)
    observed = {
        "row_count": len(rows),
        "row_ids_sha256": _digest_canonical_sequence(ids),
        "row_hashes_sha256": _digest_canonical_sequence(hashes),
        "rows_sha256": _digest_canonical_sequence(rows),
        "ledger_sha256": document.get("ledger_sha256"),
    }
    expected_observed = {name: expected[name] for name in observed}
    if not _same_typed(observed, expected_observed):
        raise ProductionBlocked("Round306A " + key + " commitment mismatch")
    if len(ids) != len(set(ids)):
        raise ProductionBlocked("Round306A " + key + " duplicate row id")
    return rows


def _load_round306a_ledgers(
    first: dict[str, tuple[str, tuple[int, ...]]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_role = {
        pin.role: pin for pin in (ROUND306A_MANIFEST, *ROUND306A_MANIFEST_MEMBERS)
    }
    member_plain = _strict_gzip_single_member(
        _read_pinned(by_role["ROUND306A_MEMBER_LEDGER"], first),
        "ROUND306A_MEMBER_LEDGER", SOURCE_DECODE_CAP,
    )
    member_document = strict_canonical_json(member_plain, "ROUND306A_MEMBER_LEDGER")
    del member_plain
    member_rows = _validate_round306a_ledger(
        member_document, "member", "fresh_member_component_rows",
        ROUND306A_MEMBER_ROW_SCHEMA, ROUND306A_MEMBER_FIELDS,
        "Round306A_fresh_member_component_row_id",
        ROUND306A_AUTHORITY_EXPECTATION["member_ledger"],
    )
    edge_plain = _strict_gzip_single_member(
        _read_pinned(by_role["ROUND306A_EDGE_LEDGER"], first),
        "ROUND306A_EDGE_LEDGER", SOURCE_DECODE_CAP,
    )
    edge_document = strict_canonical_json(edge_plain, "ROUND306A_EDGE_LEDGER")
    del edge_plain
    edge_rows = _validate_round306a_ledger(
        edge_document, "edge", "fresh_edge_application_rows",
        ROUND306A_EDGE_ROW_SCHEMA, ROUND306A_EDGE_FIELDS,
        "Round306A_fresh_edge_application_row_id",
        ROUND306A_AUTHORITY_EXPECTATION["edge_ledger"],
    )
    return member_rows, edge_rows


class _DSU:
    def __init__(self, items: list[str]):
        self.items = items
        self.index = {item: index for index, item in enumerate(items)}
        if len(self.index) != len(items):
            raise ProductionBlocked("duplicate DSU item")
        self.parent = list(range(len(items)))
        self.size = [1] * len(items)

    def find_index(self, index: int) -> int:
        while self.parent[index] != index:
            self.parent[index] = self.parent[self.parent[index]]
            index = self.parent[index]
        return index

    def union(self, left: str, right: str) -> int:
        try:
            a = self.find_index(self.index[left])
            b = self.find_index(self.index[right])
        except KeyError as exc:
            raise ProductionBlocked("edge references missing corrected root") from exc
        if a == b:
            return 0
        if self.size[a] < self.size[b] or (
            self.size[a] == self.size[b] and self.items[a] > self.items[b]
        ):
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return 1

    def partition(self) -> list[list[str]]:
        grouped: dict[int, list[str]] = defaultdict(list)
        for index, item in enumerate(self.items):
            grouped[self.find_index(index)].append(item)
        return sorted(sorted(group) for group in grouped.values())


def _strict_zero(value: Any, label: str) -> None:
    if type(value) is not int or value != 0:
        raise ProductionBlocked("nonzero or bool-aliased credit: " + label)


def _exact_pair(value: Any, label: str, *, distinct: bool = False) -> tuple[str, str]:
    if (
        type(value) is not list
        or len(value) != 2
        or not all(type(item) is str and item for item in value)
    ):
        raise ProductionBlocked("malformed pair: " + label)
    pair = (value[0], value[1])
    if list(pair) != sorted(pair):
        raise ProductionBlocked("noncanonical pair order: " + label)
    if distinct and pair[0] == pair[1]:
        raise ProductionBlocked("pair endpoints not distinct: " + label)
    return pair


def _rekey_input(
    old_root: str,
    old_member_count: int,
    deleted_member_ids: list[str],
    retained_member_ids: list[str],
    retained_source_hashes: list[str],
    official_key_id: str,
) -> dict[str, Any]:
    return {
        "schema": REKEY_INPUT_SCHEMA,
        "old_base_root_id": old_root,
        "old_member_count": old_member_count,
        "deleted_member_ids": deleted_member_ids,
        "deleted_member_count": len(deleted_member_ids),
        "retained_member_count": len(retained_member_ids),
        "retained_member_ids_sha256": digest(retained_member_ids),
        "retained_source_row_sha256_sequence_sha256": digest(retained_source_hashes),
        "official_key_id": official_key_id,
    }


def _source_member_reference(
    reference: Any,
    member_rows: list[dict[str, Any]],
    member_wire_hashes: list[str],
    expected_member_id: str,
    label: str,
) -> tuple[int, dict[str, Any]]:
    if (
        type(reference) is not list
        or len(reference) != 4
        or type(reference[0]) is not int
        or reference[0] < 0
        or type(reference[1]) is not str
        or not _is_sha256(reference[2])
        or not _is_sha256(reference[3])
    ):
        raise ProductionBlocked("malformed Round306A member reference: " + label)
    ordinal = reference[0]
    if ordinal >= len(member_rows):
        raise ProductionBlocked("Round306A member reference ordinal: " + label)
    row = member_rows[ordinal]
    observed = [
        ordinal,
        row["Round306A_fresh_member_component_row_id"],
        member_wire_hashes[ordinal],
        row["row_sha256"],
    ]
    if not _same_typed(observed, reference):
        raise ProductionBlocked("Round306A member reference mismatch: " + label)
    if row["registry_occurrence_id"] != expected_member_id:
        raise ProductionBlocked("Round306A reference/member mismatch: " + label)
    return ordinal, row


def _build_reconstruction(
    round_first: dict[str, tuple[str, tuple[int, ...]]],
    r235d_first: dict[str, tuple[str, tuple[int, ...]]],
    round_receipt: dict[str, Any],
    r235d_pin_receipt: dict[str, Any],
    r235d_result: dict[str, Any],
    r235d_rows: list[dict[str, Any]],
    r235d_semantic_receipt: dict[str, Any],
) -> dict[str, Any]:
    member_rows, edge_rows = _load_round306a_ledgers(round_first)
    if len(member_rows) != EXPECTED_CENSUS["old_member_count"]:
        raise ProductionBlocked("old member census")
    if len(edge_rows) != EXPECTED_CENSUS["legal_edge_application_count"]:
        raise ProductionBlocked("old edge census")
    member_wire_hashes = [
        hashlib.sha256(canonical_bytes(row)).hexdigest() for row in member_rows
    ]
    edge_wire_hashes = [
        hashlib.sha256(canonical_bytes(row)).hexdigest() for row in edge_rows
    ]
    r235d_wire_hashes = [
        hashlib.sha256(canonical_bytes(row)).hexdigest() for row in r235d_rows
    ]

    member_by_id: dict[str, dict[str, Any]] = {}
    member_ordinal: dict[str, int] = {}
    root_members: dict[str, list[str]] = defaultdict(list)
    root_official_key: dict[str, str] = {}
    root_old_component: dict[str, str] = {}
    root_source_hash_by_member: dict[str, str] = {}
    old_component_member_count: dict[str, int] = defaultdict(int)
    for ordinal, row in enumerate(member_rows):
        member_id = row["registry_occurrence_id"]
        root = row["base_root_id"]
        key = row["official_key_id"]
        old_component = row["final_component_id"]
        if (
            type(member_id) is not str
            or type(root) is not str
            or type(key) is not str
            or type(old_component) is not str
            or row["member_identity_preserved"] is not True
        ):
            raise ProductionBlocked("Round306A member semantics")
        for field in (
            "formal_maximality_credit", "formal_fibre_credit",
            "formal_global_disposition_credit",
        ):
            _strict_zero(row[field], "Round306A member " + field)
        if member_id in member_by_id:
            raise ProductionBlocked("duplicate Round306A registry member")
        member_by_id[member_id] = row
        member_ordinal[member_id] = ordinal
        root_members[root].append(member_id)
        root_source_hash_by_member[member_id] = row["row_sha256"]
        old_component_member_count[old_component] += 1
        if root in root_official_key and root_official_key[root] != key:
            raise ProductionBlocked("base root has multiple official keys")
        if root in root_old_component and root_old_component[root] != old_component:
            raise ProductionBlocked("base root crosses old components")
        root_official_key[root] = key
        root_old_component[root] = old_component
    if len(root_members) != EXPECTED_CENSUS["old_base_root_count"]:
        raise ProductionBlocked("old base-root census")
    if len(old_component_member_count) != 92_688:
        raise ProductionBlocked("old component label census")
    for members in root_members.values():
        members.sort()

    invalid_records: list[dict[str, Any]] = []
    invalid_role_by_member: dict[str, str] = {}
    r248_sheet_bindings: list[Any] = []
    r248_bulk_bindings: list[Any] = []
    for r235d_ordinal, authority_row in enumerate(r235d_rows):
        downstream = authority_row.get("downstream_invalidation")
        if type(downstream) is not dict:
            raise ProductionBlocked("R235D downstream row")
        if downstream.get("old_freeze_invalidated") is not True:
            raise ProductionBlocked("R235D old-freeze marker")
        _strict_zero(
            downstream.get("corrected_universe_or_DSU_credit"),
            "R235D corrected universe/DSU credit",
        )
        r248_sheet_bindings.append(downstream.get("R248_target_sheet_owner_row"))
        r248_bulk_bindings.append(downstream.get("R248_target_only_bulk_row"))
        for role, member_field, reference_field in (
            (
                "TARGET_SHEET", "invalid_TARGET_SHEET_member_id",
                "Round306A_invalid_TARGET_SHEET_member_row",
            ),
            (
                "TARGET_ONLY_SIDE", "invalid_TARGET_ONLY_SIDE_member_id",
                "Round306A_invalid_TARGET_ONLY_SIDE_member_row",
            ),
        ):
            member_id = downstream.get(member_field)
            if type(member_id) is not str or member_id in invalid_role_by_member:
                raise ProductionBlocked("R235D duplicate or malformed invalid member")
            source_ordinal, source_row = _source_member_reference(
                downstream.get(reference_field), member_rows, member_wire_hashes,
                member_id, role,
            )
            invalid_role_by_member[member_id] = role
            invalid_records.append({
                "invalidation_role": role,
                "registry_member_id": member_id,
                "source_R235D_authority_ordinal": r235d_ordinal,
                "source_R235D_invalidation_row_id": authority_row["authority_row_id"],
                "source_R235D_invalidation_row_sha256": r235d_wire_hashes[r235d_ordinal],
                "source_Round306A_member_row_ordinal": source_ordinal,
                "source_Round306A_member_row_id": source_row[
                    "Round306A_fresh_member_component_row_id"
                ],
                "source_Round306A_member_row_wire_sha256": member_wire_hashes[
                    source_ordinal
                ],
                "source_Round306A_member_row_sha256": source_row["row_sha256"],
                "old_base_root_id": source_row["base_root_id"],
                "old_component_id": source_row["final_component_id"],
                "formal_R248_correction_overlay_credit_without_independent_verification_marker": 0,
            })
    invalid_records.sort(key=lambda row: (row["registry_member_id"], row["invalidation_role"]))
    invalid_ids = sorted(invalid_role_by_member)
    invalid_sheets = sorted(
        member for member, role in invalid_role_by_member.items()
        if role == "TARGET_SHEET"
    )
    invalid_sides = sorted(
        member for member, role in invalid_role_by_member.items()
        if role == "TARGET_ONLY_SIDE"
    )
    downstream_result = r235d_result["result"]["downstream_invalidation"]
    result_invalid = downstream_result["invalid_member_sets"]
    exact_invalid = {
        "TARGET_SHEET": (invalid_sheets, "0163d9c564b74b8cff5a9d5f309a25037d461b3874ca4805161cf639aeec73f4"),
        "TARGET_ONLY_SIDE": (invalid_sides, "f6f5acf3a89bb0a09f83b7f0ac783019fddc5b36ca7d8df833d6c052cc20e957"),
        "UNION": (invalid_ids, "9c95eae730d5a033d65dadf2d27828b9876325e943049dd788ac1ed740687e52"),
    }
    for role, (ids, expected_hash) in exact_invalid.items():
        observed = result_invalid.get(role)
        if (
            type(observed) is not dict
            or observed.get("count") != len(ids)
            or observed.get("sorted_member_ids") != ids
            or observed.get("sorted_member_ids_sha256") != expected_hash
            or digest(ids) != expected_hash
        ):
            raise ProductionBlocked("R235D invalid member set: " + role)
    if len(invalid_ids) != 32 or len(invalid_sheets) != 16 or len(invalid_sides) != 16:
        raise ProductionBlocked("exact invalid member partition")

    invalid_by_root: dict[str, list[str]] = defaultdict(list)
    for member_id in invalid_ids:
        invalid_by_root[member_by_id[member_id]["base_root_id"]].append(member_id)
    for members in invalid_by_root.values():
        members.sort()
    affected_summary = downstream_result["old_Round306A_base_root_dispositions"]
    expected_summary_rows = affected_summary.get("rows")
    if (
        type(expected_summary_rows) is not list
        or affected_summary.get("affected_root_count") != 20
        or affected_summary.get("DELETE_ROOT_count") != 16
        or affected_summary.get("REKEY_ROOT_count") != 4
        or affected_summary.get("rows_sha256")
        != "779b65663d4fc1954cf79144670ad367e35e913a96c82678674d89b84f667d17"
        or digest(expected_summary_rows) != affected_summary["rows_sha256"]
    ):
        raise ProductionBlocked("R235D affected-root summary")

    corrected_root_by_old: dict[str, str | None] = {}
    root_disposition: dict[str, str] = {}
    rekey_input_by_old: dict[str, dict[str, Any]] = {}
    computed_affected_rows: list[dict[str, Any]] = []
    for old_root in sorted(root_members):
        old_members = root_members[old_root]
        deleted = invalid_by_root.get(old_root, [])
        retained = [member for member in old_members if member not in invalid_role_by_member]
        if not deleted:
            disposition = "KEEP_ROOT"
            corrected: str | None = old_root
        elif not retained:
            disposition = "DELETE_ROOT"
            corrected = None
        else:
            disposition = "REKEY_ROOT"
            retained_hashes = [root_source_hash_by_member[member] for member in retained]
            rekey_input = _rekey_input(
                old_root, len(old_members), deleted, retained, retained_hashes,
                root_official_key[old_root],
            )
            rekey_input_by_old[old_root] = rekey_input
            corrected = CORRECTED_ROOT_NAMESPACE + digest(rekey_input)
        corrected_root_by_old[old_root] = corrected
        root_disposition[old_root] = disposition
        if deleted:
            computed_affected_rows.append({
                "invalid_member_count": len(deleted),
                "invalid_member_ids": deleted,
                "old_base_root_id": old_root,
                "old_member_count": len(old_members),
                "removal_only_projected_member_count": len(retained),
                "required_disposition": disposition,
            })
    if not _same_typed(computed_affected_rows, expected_summary_rows):
        raise ProductionBlocked("computed R235D affected roots")
    histogram = {
        disposition: sum(1 for value in root_disposition.values() if value == disposition)
        for disposition in ("DELETE_ROOT", "REKEY_ROOT", "KEEP_ROOT")
    }
    if not _same_typed(histogram, ROOT_DISPOSITION_CONTRACT["disposition_histogram"]):
        raise ProductionBlocked("root disposition histogram")
    corrected_roots = sorted(
        root for root in corrected_root_by_old.values() if root is not None
    )
    if (
        len(corrected_roots) != len(set(corrected_roots))
        or len(corrected_roots) != EXPECTED_CENSUS["corrected_base_root_count"]
    ):
        raise ProductionBlocked("corrected-root injectivity/count")
    keep_roots = {
        old for old, disposition in root_disposition.items()
        if disposition == "KEEP_ROOT"
    }
    if any(
        corrected_root_by_old[old] in keep_roots for old in rekey_input_by_old
    ):
        raise ProductionBlocked("rekey root collides with keep root")

    forward = _DSU(corrected_roots)
    corrected_edge_pairs: list[tuple[str, str]] = []
    corrected_occurrence_pairs: list[tuple[str, str]] = []
    forward_flags: list[int] = []
    edge_row_hits: dict[str, int] = defaultdict(int)
    projected_slot_hits: dict[str, int] = defaultdict(int)
    occurrence_root_slot_hits: dict[str, int] = defaultdict(int)
    old_self_indices: list[int] = []
    forward_mismatch = 0
    invalid_endpoint_hits = 0
    delete_hits = 0
    collision_count = 0
    for index, row in enumerate(edge_rows):
        for field in (
            "formal_credit_without_independent_verification_marker",
            "formal_maximality_credit", "formal_fibre_credit",
            "formal_global_disposition_credit",
        ):
            _strict_zero(row[field], "Round306A edge " + field)
        old_occurrence = _exact_pair(
            row["canonical_occurrence_endpoint_pair"],
            "Round306A canonical occurrence", distinct=True,
        )
        old_projected = _exact_pair(
            row["projected_base_root_pair"], "Round306A projected roots"
        )
        if not all(root in corrected_root_by_old for root in old_projected):
            raise ProductionBlocked("edge projected root outside member universe")
        corrected_projected_list: list[str] = []
        for root in old_projected:
            projected_slot_hits[root] += 1
            corrected = corrected_root_by_old[root]
            if corrected is None:
                delete_hits += 1
                raise ProductionBlocked("deleted root occurs in edge projection")
            corrected_projected_list.append(corrected)
        corrected_projected = tuple(sorted(corrected_projected_list))
        corrected_occurrence_list: list[str] = []
        row_root_hits = set(old_projected)
        for endpoint in old_occurrence:
            if endpoint in invalid_role_by_member:
                invalid_endpoint_hits += 1
                raise ProductionBlocked("invalid member occurs as edge endpoint")
            if endpoint in corrected_root_by_old:
                occurrence_root_slot_hits[endpoint] += 1
                row_root_hits.add(endpoint)
                corrected = corrected_root_by_old[endpoint]
                if corrected is None:
                    delete_hits += 1
                    raise ProductionBlocked("deleted root occurs as exact endpoint")
                corrected_occurrence_list.append(corrected)
            else:
                corrected_occurrence_list.append(endpoint)
        corrected_occurrence = tuple(sorted(corrected_occurrence_list))
        if corrected_occurrence[0] == corrected_occurrence[1]:
            raise ProductionBlocked("corrected occurrence endpoints collapsed")
        for root in row_root_hits:
            edge_row_hits[root] += 1
        collision = _is_distinct_root_remap_collision(
            old_projected, corrected_projected
        )
        collision_count += int(collision)
        if collision:
            raise ProductionBlocked("distinct projected roots remap to one")
        if old_projected[0] == old_projected[1]:
            old_self_indices.append(index)
        reduced = forward.union(*corrected_projected)
        old_flag = row.get("forward_rank_reduction")
        if type(old_flag) is not int or old_flag not in (0, 1):
            raise ProductionBlocked("Round306A forward flag type")
        if (
            row.get("fed_to_new_empty_DSU") is not True
            or row.get("serialized_Round304_partition_used_as_state") is not False
            or row.get("candidate_DSU_rank_reduction") != old_flag
            or row.get("forward_cycle_or_redundant") != 1 - old_flag
        ):
            raise ProductionBlocked("Round306A edge admission semantics")
        forward_mismatch += int(reduced != old_flag)
        corrected_edge_pairs.append(corrected_projected)
        corrected_occurrence_pairs.append(corrected_occurrence)
        forward_flags.append(reduced)
    if (
        sum(forward_flags) != EXPECTED_CENSUS["fresh_rank_reduction_count"]
        or forward_mismatch != 0
        or delete_hits != 0
        or invalid_endpoint_hits != 0
        or collision_count != 0
        or len(old_self_indices) != READ_ONLY_DIAGNOSTIC[
            "old_projected_self_root_cycle_row_count"
        ]
        or digest(old_self_indices)
        != READ_ONLY_DIAGNOSTIC[
            "old_projected_self_root_cycle_application_indices_sha256"
        ]
    ):
        raise ProductionBlocked("edge remap diagnostic vector")

    reverse = _DSU(corrected_roots)
    reverse_flags = [0] * len(edge_rows)
    for reverse_index, source_index in enumerate(range(len(edge_rows) - 1, -1, -1)):
        reverse_flags[source_index] = reverse.union(*corrected_edge_pairs[source_index])
        if reverse_index != len(edge_rows) - 1 - source_index:
            raise ProductionBlocked("reverse application index")
    forward_partition = forward.partition()
    reverse_partition = reverse.partition()
    partition_sha = digest(forward_partition)
    if (
        sum(reverse_flags) != EXPECTED_CENSUS["fresh_rank_reduction_count"]
        or not _same_typed(forward_partition, reverse_partition)
        or partition_sha != READ_ONLY_DIAGNOSTIC["corrected_partition_sha256"]
        or len(forward_partition) != EXPECTED_CENSUS["corrected_component_count"]
    ):
        raise ProductionBlocked("fresh forward/reverse DSU partition")

    component_by_root: dict[str, str] = {}
    component_roots: dict[str, list[str]] = {}
    for roots in forward_partition:
        component_id = COMPONENT_NAMESPACE + digest(roots)
        if component_id in component_roots:
            raise ProductionBlocked("component-id collision")
        component_roots[component_id] = roots
        for root in roots:
            component_by_root[root] = component_id
    old_by_corrected = {
        corrected: old for old, corrected in corrected_root_by_old.items()
        if corrected is not None
    }
    component_members: dict[str, list[str]] = defaultdict(list)
    retained_members: list[str] = []
    for member_id in sorted(member_by_id):
        if member_id in invalid_role_by_member:
            continue
        old_root = member_by_id[member_id]["base_root_id"]
        corrected_root = corrected_root_by_old[old_root]
        if corrected_root is None:
            raise ProductionBlocked("retained member under deleted root")
        component_id = component_by_root[corrected_root]
        component_members[component_id].append(member_id)
        retained_members.append(member_id)
    if len(retained_members) != EXPECTED_CENSUS["corrected_member_count"]:
        raise ProductionBlocked("corrected member census")
    for members in component_members.values():
        members.sort()
    if set(component_members) != set(component_roots):
        raise ProductionBlocked("empty or orphan corrected component")
    component_ids = sorted(component_roots)
    # These are canonical namespace-independent size-multiset vectors.  Their
    # order is ascending numeric size, not corrected-component-id order.
    member_size_vector = sorted(
        len(component_members[item]) for item in component_ids
    )
    root_size_vector = sorted(len(component_roots[item]) for item in component_ids)
    member_size_vector_sha = digest(member_size_vector)
    root_size_vector_sha = digest(root_size_vector)
    if member_size_vector_sha != "9093ba64d0b01a8ba3be390aafaf633161c50a474326d6c178a60d487af96e3e":
        raise ProductionBlocked("ascending component member-size multiset vector")
    if root_size_vector_sha != "8551fa4905c023f5e680ff210822121055146d8a082efdd1665bfc2f523c31ce":
        raise ProductionBlocked("ascending component root-size multiset vector")
    square_sum = sum(size * size for size in member_size_vector)
    arithmetic = _pair_arithmetic_from_n_and_square_sum(len(retained_members), square_sum)
    expected_arithmetic = {
        "member_count": EXPECTED_CENSUS["corrected_member_count"],
        "member_count_squared": EXPECTED_CENSUS["corrected_member_count_squared"],
        "component_size_square_sum": EXPECTED_CENSUS[
            "sum_corrected_component_member_count_squared"
        ],
        "all_pairs": EXPECTED_CENSUS["all_unordered_member_pairs"],
        "within": EXPECTED_CENSUS["within_component_unordered_member_pairs"],
        "cross": EXPECTED_CENSUS["cross_component_pair_denominator"],
    }
    if not _same_typed(arithmetic, expected_arithmetic):
        raise ProductionBlocked("corrected pair arithmetic")
    old_square_sum = sum(
        count * count for count in old_component_member_count.values()
    )
    old_arithmetic = _pair_arithmetic_from_n_and_square_sum(
        len(member_rows), old_square_sum
    )
    expected_old_arithmetic = {
        "member_count": EXPECTED_CENSUS["old_member_count"],
        "member_count_squared": EXPECTED_CENSUS["old_member_count_squared"],
        "component_size_square_sum": EXPECTED_CENSUS[
            "sum_old_component_member_count_squared"
        ],
        "all_pairs": EXPECTED_CENSUS["old_all_unordered_member_pairs"],
        "within": EXPECTED_CENSUS["old_within_component_unordered_member_pairs"],
        "cross": EXPECTED_CENSUS["old_cross_component_pair_denominator"],
    }
    if not _same_typed(old_arithmetic, expected_old_arithmetic):
        raise ProductionBlocked("old sealed pair arithmetic")
    observed_deltas = {
        "all": old_arithmetic["all_pairs"] - arithmetic["all_pairs"],
        "within": old_arithmetic["within"] - arithmetic["within"],
        "cross": old_arithmetic["cross"] - arithmetic["cross"],
    }
    expected_deltas = {
        "all": EXPECTED_CENSUS["all_pair_decrease"],
        "within": EXPECTED_CENSUS["within_component_pair_decrease"],
        "cross": EXPECTED_CENSUS["cross_component_pair_decrease"],
    }
    if not _same_typed(observed_deltas, expected_deltas):
        raise ProductionBlocked("old-to-corrected pair deltas")
    affected_old_components = sorted({
        root_old_component[member_by_id[member_id]["base_root_id"]]
        for member_id in invalid_ids
    })
    if len(affected_old_components) != 20:
        raise ProductionBlocked("complete affected old component census")
    delete_old_roots = sorted(
        old for old, disposition in root_disposition.items()
        if disposition == "DELETE_ROOT"
    )
    delete_component_transitions = sorted(
        (old_component_member_count[root_old_component[old]], 0)
        for old in delete_old_roots
    )
    if delete_component_transitions != [(1, 0)] * 16:
        raise ProductionBlocked("deleted singleton component transitions")
    rekey_old_components = sorted({
        root_old_component[old] for old in rekey_input_by_old
    })
    rekey_new_components = sorted({
        component_by_root[corrected_root_by_old[old]]
        for old in rekey_input_by_old
    })
    if len(rekey_old_components) != 4 or len(rekey_new_components) != 4:
        raise ProductionBlocked("distinct rekey old/new component census")
    affected_old_sizes = sorted(old_component_member_count[item] for item in rekey_old_components)
    affected_new_sizes = sorted(len(component_members[item]) for item in rekey_new_components)
    if (
        affected_old_sizes
        != EXPECTED_CENSUS["rekey_affected_old_component_member_sizes"]
        or affected_new_sizes
        != EXPECTED_CENSUS["rekey_affected_corrected_component_member_sizes"]
    ):
        raise ProductionBlocked("affected component sizes")
    for old in rekey_input_by_old:
        if (
            edge_row_hits.get(old, 0) != READ_ONLY_DIAGNOSTIC["rekey_per_root_edge_row_hits"]
            or projected_slot_hits.get(old, 0)
            != READ_ONLY_DIAGNOSTIC["rekey_per_root_projected_root_slots"]
            or occurrence_root_slot_hits.get(old, 0)
            != READ_ONLY_DIAGNOSTIC["rekey_per_root_exact_occurrence_root_slots"]
        ):
            raise ProductionBlocked("rekey edge binding census")
    for old, disposition in root_disposition.items():
        if disposition == "DELETE_ROOT" and (
            edge_row_hits.get(old, 0)
            or projected_slot_hits.get(old, 0)
            or occurrence_root_slot_hits.get(old, 0)
        ):
            raise ProductionBlocked("delete-root edge hit")

    return {
        "member_rows": member_rows,
        "member_wire_hashes": member_wire_hashes,
        "member_by_id": member_by_id,
        "member_ordinal": member_ordinal,
        "edge_rows": edge_rows,
        "edge_wire_hashes": edge_wire_hashes,
        "invalid_records": invalid_records,
        "invalid_ids": invalid_ids,
        "invalid_sheets": invalid_sheets,
        "invalid_sides": invalid_sides,
        "invalid_role_by_member": invalid_role_by_member,
        "root_members": dict(root_members),
        "root_official_key": root_official_key,
        "root_old_component": root_old_component,
        "root_source_hash_by_member": root_source_hash_by_member,
        "root_disposition": root_disposition,
        "corrected_root_by_old": corrected_root_by_old,
        "rekey_input_by_old": rekey_input_by_old,
        "corrected_roots": corrected_roots,
        "corrected_edge_pairs": corrected_edge_pairs,
        "corrected_occurrence_pairs": corrected_occurrence_pairs,
        "forward_flags": forward_flags,
        "reverse_flags": reverse_flags,
        "component_by_root": component_by_root,
        "component_roots": component_roots,
        "component_members": dict(component_members),
        "component_ids": component_ids,
        "old_by_corrected": old_by_corrected,
        "edge_row_hits": dict(edge_row_hits),
        "projected_slot_hits": dict(projected_slot_hits),
        "occurrence_root_slot_hits": dict(occurrence_root_slot_hits),
        "partition_sha256": partition_sha,
        "member_size_vector_sha256": member_size_vector_sha,
        "root_size_vector_sha256": root_size_vector_sha,
        "pair_arithmetic": arithmetic,
        "old_pair_arithmetic": old_arithmetic,
        "pair_deltas": observed_deltas,
        "affected_old_components": affected_old_components,
        "delete_component_transitions": delete_component_transitions,
        "rekey_old_components": rekey_old_components,
        "rekey_new_components": rekey_new_components,
        "affected_old_sizes": affected_old_sizes,
        "affected_new_sizes": affected_new_sizes,
        "r248_sheet_bindings_sha256": digest(r248_sheet_bindings),
        "r248_bulk_bindings_sha256": digest(r248_bulk_bindings),
        "r235d_authority_row_sha256_sequence_sha256": digest(r235d_wire_hashes),
        "round306a_pin_receipt": round_receipt,
        "r235d_pin_receipt": r235d_pin_receipt,
        "r235d_semantic_receipt": r235d_semantic_receipt,
    }


def _make_output_row(kind: str, core: dict[str, Any]) -> dict[str, Any]:
    if kind not in ROW_SCHEMAS or "schema" in core or "row_id" in core or "row_sha256" in core:
        raise ProductionBlocked("output row closure boundary: " + kind)
    payload = {"schema": ROW_SCHEMAS[kind], **core}
    row_id = ROW_ID_NAMESPACES[kind] + digest(payload)
    row = {"schema": ROW_SCHEMAS[kind], "row_id": row_id, **core}
    row["row_sha256"] = digest(row)
    if tuple(sorted(row)) != tuple(sorted(ROW_FIELDS[kind])):
        raise ProductionBlocked("output row exact fields: " + kind)
    return row


def _iter_member_invalidation_rows(reconstruction: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for core in reconstruction["invalid_records"]:
        yield _make_output_row("member_invalidation", core)


def _root_disposition_core(reconstruction: dict[str, Any], old_root: str) -> dict[str, Any]:
    old_members = reconstruction["root_members"][old_root]
    deleted = sorted(
        member for member in old_members
        if member in reconstruction["invalid_role_by_member"]
    )
    deleted_set = set(deleted)
    retained = [member for member in old_members if member not in deleted_set]
    retained_source_hashes = [
        reconstruction["root_source_hash_by_member"][member] for member in retained
    ]
    disposition = reconstruction["root_disposition"][old_root]
    commitment_payload = {
        "schema": SCHEMA + ".base-root-disposition-input.v1",
        "old_base_root_id": old_root,
        "disposition": disposition,
        "old_component_id": reconstruction["root_old_component"][old_root],
        "old_member_count": len(old_members),
        "deleted_member_ids": deleted,
        "deleted_member_count": len(deleted),
        "deleted_member_ids_sha256": digest(deleted),
        "retained_member_count": len(retained),
        "retained_member_ids_sha256": digest(retained),
        "retained_source_row_sha256_sequence_sha256": digest(
            retained_source_hashes
        ),
        "official_key_id": reconstruction["root_official_key"][old_root],
    }
    return {
        "old_base_root_id": old_root,
        "disposition": disposition,
        "old_member_count": len(old_members),
        "deleted_member_count": len(deleted),
        "deleted_member_ids": deleted,
        "deleted_member_ids_sha256": digest(deleted),
        "retained_member_count": len(retained),
        "retained_member_ids_sha256": digest(retained),
        "retained_source_row_sha256_sequence_sha256": digest(
            retained_source_hashes
        ),
        "official_key_id": reconstruction["root_official_key"][old_root],
        "canonical_input_commitment_sha256": digest(commitment_payload),
        "corrected_base_root_id_or_null": reconstruction[
            "corrected_root_by_old"
        ][old_root],
        "old_component_id": reconstruction["root_old_component"][old_root],
        "candidate_complete_selected_row_R248_correction_overlay": True,
        "formal_corrected_root_credit_without_independent_verification_marker": 0,
    }


def _iter_root_disposition_rows(reconstruction: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for old_root in sorted(reconstruction["root_members"]):
        yield _make_output_row(
            "root_disposition", _root_disposition_core(reconstruction, old_root)
        )


def _edge_corrected_occurrence_pair(
    reconstruction: dict[str, Any], old_occurrence: tuple[str, str]
) -> tuple[str, str]:
    mapped: list[str] = []
    for endpoint in old_occurrence:
        if endpoint in reconstruction["corrected_root_by_old"]:
            corrected = reconstruction["corrected_root_by_old"][endpoint]
            if corrected is None:
                raise ProductionBlocked("deleted root in exact occurrence endpoint")
            mapped.append(corrected)
        else:
            mapped.append(endpoint)
    corrected_pair = tuple(sorted(mapped))
    if corrected_pair[0] == corrected_pair[1]:
        raise ProductionBlocked("exact occurrence endpoint collapse")
    return corrected_pair


def _iter_edge_remap_rows(reconstruction: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for index, source in enumerate(reconstruction["edge_rows"]):
        old_occurrence = _exact_pair(
            source["canonical_occurrence_endpoint_pair"],
            "output old occurrence", distinct=True,
        )
        old_projected = _exact_pair(
            source["projected_base_root_pair"], "output old projected"
        )
        corrected_occurrence = _edge_corrected_occurrence_pair(
            reconstruction, old_occurrence
        )
        if corrected_occurrence != reconstruction["corrected_occurrence_pairs"][index]:
            raise ProductionBlocked("corrected occurrence replay drift")
        corrected_projected = reconstruction["corrected_edge_pairs"][index]
        delete_hits = sum(
            reconstruction["root_disposition"].get(item) == "DELETE_ROOT"
            for item in (*old_occurrence, *old_projected)
        )
        invalid_hits = sum(
            item in reconstruction["invalid_role_by_member"] for item in old_occurrence
        )
        yield _make_output_row("edge_remap", {
            "application_index": index,
            "source_Round306A_row_id": source[
                "Round306A_fresh_edge_application_row_id"
            ],
            "source_Round306A_row_wire_sha256": reconstruction[
                "edge_wire_hashes"
            ][index],
            "source_Round306A_row_sha256": source["row_sha256"],
            "source_channel": source["source_channel"],
            "source_row_id": source["source_row_id"],
            "old_canonical_occurrence_endpoint_pair": list(old_occurrence),
            "corrected_canonical_occurrence_endpoint_pair": list(
                corrected_occurrence
            ),
            "old_projected_base_root_pair": list(old_projected),
            "corrected_projected_base_root_pair": list(corrected_projected),
            "delete_root_hit_count": delete_hits,
            "invalid_member_endpoint_hit_count": invalid_hits,
            "distinct_root_remap_collision": _is_distinct_root_remap_collision(
                old_projected, corrected_projected
            ),
            "forward_rank_reduction": reconstruction["forward_flags"][index],
            "old_forward_rank_flag_match": (
                reconstruction["forward_flags"][index]
                == source["forward_rank_reduction"]
            ),
            "reverse_application_index": len(reconstruction["edge_rows"]) - 1 - index,
            "reverse_rank_reduction": reconstruction["reverse_flags"][index],
            "formal_corrected_DSU_credit_without_independent_verification_marker": 0,
        })


def _iter_member_component_rows(reconstruction: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for member_id in sorted(reconstruction["member_by_id"]):
        if member_id in reconstruction["invalid_role_by_member"]:
            continue
        source = reconstruction["member_by_id"][member_id]
        ordinal = reconstruction["member_ordinal"][member_id]
        old_root = source["base_root_id"]
        corrected_root = reconstruction["corrected_root_by_old"][old_root]
        if type(corrected_root) is not str:
            raise ProductionBlocked("retained member corrected root")
        yield _make_output_row("member_component", {
            "registry_member_id": member_id,
            "source_Round306A_row_ordinal": ordinal,
            "source_Round306A_row_id": source[
                "Round306A_fresh_member_component_row_id"
            ],
            "source_Round306A_row_wire_sha256": reconstruction[
                "member_wire_hashes"
            ][ordinal],
            "source_Round306A_row_sha256": source["row_sha256"],
            "old_base_root_id": old_root,
            "corrected_base_root_id": corrected_root,
            "root_disposition": reconstruction["root_disposition"][old_root],
            "official_key_id": source["official_key_id"],
            "corrected_component_id": reconstruction["component_by_root"][
                corrected_root
            ],
            "member_identity_preserved": True,
            "formal_corrected_member_universe_credit_without_independent_verification_marker": 0,
            "formal_corrected_DSU_credit_without_independent_verification_marker": 0,
        })


def _iter_base_root_component_rows(
    reconstruction: dict[str, Any]
) -> Iterator[dict[str, Any]]:
    for corrected_root in reconstruction["corrected_roots"]:
        old_root = reconstruction["old_by_corrected"][corrected_root]
        members = [
            member for member in reconstruction["root_members"][old_root]
            if member not in reconstruction["invalid_role_by_member"]
        ]
        yield _make_output_row("base_root_component", {
            "corrected_base_root_id": corrected_root,
            "old_base_root_id": old_root,
            "root_disposition": reconstruction["root_disposition"][old_root],
            "member_count": len(members),
            "member_ids_sha256": digest(members),
            "official_key_id": reconstruction["root_official_key"][old_root],
            "corrected_component_id": reconstruction["component_by_root"][
                corrected_root
            ],
            "edge_row_hit_count": reconstruction["edge_row_hits"].get(old_root, 0),
            "projected_root_slot_hit_count": reconstruction[
                "projected_slot_hits"
            ].get(old_root, 0),
            "exact_occurrence_root_slot_hit_count": reconstruction[
                "occurrence_root_slot_hits"
            ].get(old_root, 0),
            "formal_corrected_DSU_credit_without_independent_verification_marker": 0,
        })


def _iter_component_census_rows(reconstruction: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for component_id in reconstruction["component_ids"]:
        roots = reconstruction["component_roots"][component_id]
        members = reconstruction["component_members"][component_id]
        yield _make_output_row("component_census", {
            "corrected_component_id": component_id,
            "base_root_count": len(roots),
            "base_root_ids_sha256": digest(roots),
            "member_count": len(members),
            "member_ids_sha256": digest(members),
            "formal_corrected_DSU_credit_without_independent_verification_marker": 0,
        })


ROW_ITERATORS: Final = {
    "member_invalidation": _iter_member_invalidation_rows,
    "root_disposition": _iter_root_disposition_rows,
    "edge_remap": _iter_edge_remap_rows,
    "member_component": _iter_member_component_rows,
    "base_root_component": _iter_base_root_component_rows,
    "component_census": _iter_component_census_rows,
}


def _schema_snapshot() -> dict[str, Any]:
    return {
        "schema": SCHEMA + ".schema-snapshot.v1",
        "output_files": OUTPUTS,
        "output_order": list(OUTPUT_ORDER),
        "row_schemas": ROW_SCHEMAS,
        "row_fields": {key: list(value) for key, value in ROW_FIELDS.items()},
        "row_id_namespaces": ROW_ID_NAMESPACES,
        "row_id_derivation": (
            "namespace+sha256(canonical_json({schema,...core_without_row_id_or_row_sha256}))"
        ),
        "row_sha256_derivation": (
            "sha256(canonical_json(row_without_row_sha256))"
        ),
        "jsonl_ledger_serialization": (
            "one canonical ASCII JSON row plus LF; gzip level 9; mtime 0; empty filename; single member"
        ),
        "corrected_root_derivation": {
            "KEEP_ROOT": "corrected_base_root_id=old_base_root_id",
            "DELETE_ROOT": "corrected_base_root_id_or_null=null",
            "REKEY_ROOT": "round306c0-corrected-base-root:+sha256(canonical_json(rekey_input))",
            "rekey_input_schema": REKEY_INPUT_SCHEMA,
            "rekey_input_fields": [
                "schema", "old_base_root_id", "old_member_count",
                "deleted_member_ids", "deleted_member_count",
                "retained_member_count", "retained_member_ids_sha256",
                "retained_source_row_sha256_sequence_sha256", "official_key_id",
            ],
        },
        "base_root_disposition_input_commitment": {
            "uniform_for_KEEP_DELETE_REKEY": True,
            "schema": SCHEMA + ".base-root-disposition-input.v1",
            "fields": [
                "schema", "old_base_root_id", "disposition",
                "old_component_id", "old_member_count", "deleted_member_ids",
                "deleted_member_count", "deleted_member_ids_sha256",
                "retained_member_count", "retained_member_ids_sha256",
                "retained_source_row_sha256_sequence_sha256", "official_key_id",
            ],
            "REKEY_corrected_root_id_uses_separate_strict_rekey_input": True,
        },
        "component_id_derivation": (
            "round306c0-fresh-legal-component:+sha256(canonical_json(sorted_corrected_root_ids))"
        ),
        "component_size_vector_definition": (
            "ascending-numeric sorted size multiset; namespace/order independent; "
            "component-id-to-count mapping remains in component_census ledger"
        ),
        "formal_credit_rule": (
            "all producer artifacts are zero credit; independent verification is last and sole marker"
        ),
    }


def _authority_frontier_document(
    reconstruction: dict[str, Any], producer_sha256: str
) -> dict[str, Any]:
    snapshot = _schema_snapshot()
    round_pins = (ROUND306A_MANIFEST, *ROUND306A_MANIFEST_MEMBERS)
    round_by_role = {pin.role: pin for pin in round_pins}
    invalid_ids = reconstruction["invalid_ids"]
    affected_roots = sorted(
        old for old, disposition in reconstruction["root_disposition"].items()
        if disposition != "KEEP_ROOT"
    )
    payload = {
        "schema": SCHEMA + ".authority-frontier.v1",
        "status": "PASS_COMPLETE_SELECTED_ROW_R248_CORRECTION_OVERLAY_AND_FRESH_REPLAY_FRONTIER_CANDIDATE__ZERO_CREDIT",
        "producer_file_sha256": producer_sha256,
        "construction_source": reconstruction["construction_source_receipt"],
        "schema_snapshot": snapshot,
        "schema_snapshot_sha256": digest(snapshot),
        "authority_priority": [
            {
                "priority": 1,
                "authority": "SEALED_R235D_SELECTED_ROW_INVALIDATION",
                "scope": "EXACT_32_MEMBER_20_ROOT_R248_CORRECTION_OVERLAY",
            },
            {
                "priority": 2,
                "authority": "SEALED_ROUND306A_MEMBER_AND_EDGE_TRANSCRIPTS",
                "scope": "ALL_OLD_ROWS_MINUS_EXACT_PRIORITY_1_EXCLUSIONS",
            },
            {
                "priority": 3,
                "authority": "ROUND306C0_EMPTY_DSU_FORWARD_REVERSE_REPLAY",
                "scope": "CORRECTED_ROOT_COMPONENT_AND_PAIR_IDENTITIES",
            },
        ],
        "round306a_frontier": {
            "manifest_and_members": [asdict(pin) for pin in round_pins],
            "pin_audit": reconstruction["round306a_pin_receipt"],
            "consumption_mode": "DATA_ONLY__NO_PRODUCER_OR_VERIFIER_IMPORT_OR_EXEC",
            "member_table_path": (
                round_by_role["ROUND306A_MEMBER_LEDGER"].filename
                + "#/fresh_member_component_rows"
            ),
            "edge_table_path": (
                round_by_role["ROUND306A_EDGE_LEDGER"].filename
                + "#/fresh_edge_application_rows"
            ),
            "member_order_commitments": ROUND306A_AUTHORITY_EXPECTATION[
                "member_ledger"
            ],
            "edge_order_commitments": ROUND306A_AUTHORITY_EXPECTATION[
                "edge_ledger"
            ],
        },
        "r235d_frontier": {
            "manifest_and_members": [asdict(pin) for pin in R235D_FINAL_PINS],
            "pin_audit": reconstruction["r235d_pin_receipt"],
            "semantic_audit": reconstruction["r235d_semantic_receipt"],
            "authority_jsonl_path": (
                R235D_FINAL_PINS[2].filename + "#/<ordered-canonical-jsonl-row>"
            ),
            "ordered_authority_row_sha256_sequence_sha256": reconstruction[
                "r235d_authority_row_sha256_sequence_sha256"
            ],
            "R248_target_sheet_owner_binding_sequence_sha256": reconstruction[
                "r248_sheet_bindings_sha256"
            ],
            "R248_target_only_bulk_binding_sequence_sha256": reconstruction[
                "r248_bulk_bindings_sha256"
            ],
        },
        "complete_formal_R248_correction_overlay": {
            "scope": "SELECTED_PINNED_ROWS_ONLY",
            "complete_for_selected_invalid_member_rows": True,
            "invalid_member_count": 32,
            "invalid_member_ids_sha256": digest(invalid_ids),
            "invalid_TARGET_SHEET_count": 16,
            "invalid_TARGET_SHEET_ids_sha256": digest(
                reconstruction["invalid_sheets"]
            ),
            "invalid_TARGET_ONLY_SIDE_count": 16,
            "invalid_TARGET_ONLY_SIDE_ids_sha256": digest(
                reconstruction["invalid_sides"]
            ),
            "affected_old_root_count": 20,
            "affected_old_root_ids_sha256": digest(affected_roots),
            "Round306A_member_rows_not_revoked_by_exact_priority_overlay": 564_460,
            "preservation_rule": (
                "priority overlay keeps every sealed Round306A member row not in the exact R235D invalid-member union"
            ),
            "transitively_binds_full_pinned_R248_through_complete_R235D_seal": True,
            "package_wide_regenerated_R248_certificate_claimed": False,
            "unhashed_R248_package_members_asserted_invalid": False,
            "old_selected_R248_rows_reused_as_current_authority": False,
        },
        "corrected_identity_contract": {
            "corrected_member_count": 564_460,
            "corrected_base_root_count": 367_948,
            "fresh_component_count": 92_672,
            "partition_sha256": reconstruction["partition_sha256"],
            "old_component_ids_have_zero_corrected_identity_authority": True,
        },
        "input_and_output_safety": {
            "complete_pin_count": 23,
            "two_pass_held_fd_hashing": True,
            "final_all_pin_path_identity_revalidation_before_publication": True,
            "symlink_and_hardlink_fail_close": True,
            "decoded_row_cap_bytes_enforced_after_final_decode": MAX_DECODED_ROW_BYTES,
            "single_gzip_member_no_trailing_bytes": True,
            "TMPDIR_ignored": True,
            "fixed_external_spill_root": FIXED_EXTERNAL_SPILL_ROOT,
            "candidate_result_committed_last_O_EXCL": True,
        },
        "formal_credit_without_independent_verification_marker": {
            "corrected_member_universe": 0,
            "corrected_base_root_universe": 0,
            "corrected_DSU": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "CM2": 0,
        },
    }
    return {**payload, "authority_frontier_sha256": digest(payload)}


def _pair_denominator_document(reconstruction: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema": SCHEMA + ".cross-component-pair-denominator.v1",
        "status": "PASS_EXACT_CORRECTED_COMPONENT_PAIR_ARITHMETIC_CANDIDATE__ZERO_MAXIMALITY_CREDIT",
        "corrected_member_count": 564_460,
        "corrected_member_count_squared": 318_615_091_600,
        "corrected_component_count": 92_672,
        "component_size_vector_definition": (
            "ascending-numeric sorted size multiset; component mapping is in component_census ledger"
        ),
        "corrected_component_member_count_vector_sha256": reconstruction[
            "member_size_vector_sha256"
        ],
        "corrected_component_base_root_count_vector_sha256": reconstruction[
            "root_size_vector_sha256"
        ],
        "sum_corrected_component_member_count_squared": 974_874_492,
        "all_unordered_member_pairs": 159_307_263_570,
        "within_component_unordered_member_pairs": 487_155_016,
        "cross_component_pair_denominator": 158_820_108_554,
        "old_to_corrected_deltas": {
            "all_pair_decrease": 18_063_216,
            "within_component_pair_decrease": 87_416,
            "cross_component_pair_decrease": 17_975_800,
        },
        "rekey_affected_old_component_member_sizes": reconstruction[
            "affected_old_sizes"
        ],
        "rekey_affected_corrected_component_member_sizes": reconstruction[
            "affected_new_sizes"
        ],
        "arithmetic_identity": (
            "cross=(N*N-sum(component_member_count*component_member_count))//2"
        ),
        "formal_pair_routing_credit_without_independent_verification_marker": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
    }
    return {**payload, "pair_denominator_sha256": digest(payload)}


@dataclass
class _HeldDirectory:
    path: Path
    fd: int
    identity: tuple[int, ...]


def _directory_identity(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        stat.S_IFMT(info.st_mode),
        stat.S_IMODE(info.st_mode),
        info.st_uid,
        info.st_gid,
    )


def _open_absolute_directory_without_symlinks(path: Path) -> _HeldDirectory:
    absolute = Path(os.path.abspath(os.fspath(path)))
    if not absolute.is_absolute():
        raise ProductionBlocked("absolute directory normalization")
    flags = (
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    current_fd = os.open("/", flags)
    try:
        for part in absolute.parts[1:]:
            next_fd = os.open(part, flags, dir_fd=current_fd)
            os.close(current_fd)
            current_fd = next_fd
        info = os.fstat(current_fd)
        if not stat.S_ISDIR(info.st_mode):
            raise ProductionBlocked("not a directory: " + os.fspath(absolute))
        return _HeldDirectory(absolute, current_fd, _directory_identity(info))
    except BaseException:
        os.close(current_fd)
        raise


def _held_directory_path_identity(directory: _HeldDirectory) -> None:
    reopened = _open_absolute_directory_without_symlinks(directory.path)
    try:
        if (
            _directory_identity(os.fstat(directory.fd)) != directory.identity
            or _directory_identity(os.fstat(reopened.fd)) != directory.identity
        ):
            raise ProductionBlocked("held directory path identity changed")
    finally:
        os.close(reopened.fd)


def _held_at_hash(
    directory: _HeldDirectory, filename: str
) -> tuple[str, tuple[int, ...]]:
    before = os.stat(filename, dir_fd=directory.fd, follow_symlinks=False)
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise ProductionBlocked("output is not one-link regular file: " + filename)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(filename, flags, dir_fd=directory.fd)
    try:
        opened = os.fstat(fd)
        if _file_identity(opened) != _file_identity(before):
            raise ProductionBlocked("output changed before held-FD open: " + filename)
        state = hashlib.sha256()
        while True:
            block = os.read(fd, 1024 * 1024)
            if not block:
                break
            state.update(block)
        after = os.fstat(fd)
    finally:
        os.close(fd)
    final = os.stat(filename, dir_fd=directory.fd, follow_symlinks=False)
    identity = _file_identity(before)
    if _file_identity(after) != identity or _file_identity(final) != identity:
        raise ProductionBlocked("output changed during held-FD hash: " + filename)
    return state.hexdigest(), identity


def _write_exclusive_bytes(
    directory: _HeldDirectory, filename: str, raw: bytes
) -> None:
    flags = (
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    fd = os.open(filename, flags, 0o600, dir_fd=directory.fd)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(fd, view)
            if written <= 0:
                raise ProductionBlocked("short exclusive write: " + filename)
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)


def _file_descriptor(
    directory: _HeldDirectory, filename: str, *, schema: str, role: str
) -> dict[str, Any]:
    actual_hash, identity = _held_at_hash(directory, filename)
    return {
        "role": role,
        "filename": filename,
        "schema": schema,
        "size": identity[4],
        "sha256": actual_hash,
    }


def _write_json_document(
    directory: _HeldDirectory,
    key: str,
    document: dict[str, Any],
    self_hash_field: str,
) -> dict[str, Any]:
    if not _is_sha256(document.get(self_hash_field)):
        raise ProductionBlocked("JSON document self hash field: " + key)
    payload = dict(document)
    claimed = payload.pop(self_hash_field)
    if digest(payload) != claimed:
        raise ProductionBlocked("JSON document digest closure: " + key)
    raw = canonical_bytes(document)
    if len(raw) > MAX_DECODED_ROW_BYTES:
        raise ProductionBlocked("JSON document decoded cap: " + key)
    filename = OUTPUTS[key]
    _write_exclusive_bytes(directory, filename, raw)
    return _file_descriptor(
        directory, filename, schema=document["schema"], role=key
    )


def _write_jsonl_gzip_ledger(
    directory: _HeldDirectory,
    kind: str,
    rows: Iterator[dict[str, Any]],
) -> dict[str, Any]:
    filename = OUTPUTS[kind]
    raw_state = hashlib.sha256()
    id_state = hashlib.sha256(b"[")
    row_hash_state = hashlib.sha256(b"[")
    rows_state = hashlib.sha256(b"[")
    row_count = 0
    seen_row_ids: set[str] = set()
    flags = (
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    fd = os.open(filename, flags, 0o600, dir_fd=directory.fd)
    try:
        with os.fdopen(fd, "wb", closefd=False) as raw_stream:
            with gzip.GzipFile(
                filename="", mode="wb", fileobj=raw_stream,
                mtime=0, compresslevel=9,
            ) as stream:
                for row in rows:
                    if (
                        type(row) is not dict
                        or tuple(sorted(row)) != tuple(sorted(ROW_FIELDS[kind]))
                        or row.get("schema") != ROW_SCHEMAS[kind]
                        or type(row.get("row_id")) is not str
                        or not _is_sha256(row.get("row_sha256"))
                    ):
                        raise ProductionBlocked("generated ledger row schema: " + kind)
                    payload = dict(row)
                    claimed = payload.pop("row_sha256")
                    if digest(payload) != claimed:
                        raise ProductionBlocked("generated row digest: " + kind)
                    row_id = row["row_id"]
                    if row_id in seen_row_ids:
                        raise ProductionBlocked("duplicate output row id: " + kind)
                    seen_row_ids.add(row_id)
                    encoded = canonical_bytes(row)
                    if len(encoded) > MAX_DECODED_ROW_BYTES:
                        raise ProductionBlocked("output decoded row cap: " + kind)
                    line = encoded + b"\n"
                    stream.write(line)
                    raw_state.update(line)
                    if row_count:
                        id_state.update(b",")
                        row_hash_state.update(b",")
                        rows_state.update(b",")
                    id_state.update(canonical_bytes(row_id))
                    row_hash_state.update(canonical_bytes(claimed))
                    rows_state.update(encoded)
                    row_count += 1
            raw_stream.flush()
            os.fsync(raw_stream.fileno())
    finally:
        os.close(fd)
    id_state.update(b"]")
    row_hash_state.update(b"]")
    rows_state.update(b"]")
    if row_count != LEDGER_ROW_COUNTS[kind]:
        raise ProductionBlocked("generated exact row count: " + kind)
    descriptor = _file_descriptor(
        directory, filename,
        schema=SCHEMA + "." + kind.replace("_", "-") + "-jsonl-ledger.v1",
        role=kind,
    )
    descriptor.update({
        "compression": "gzip-level-9-mtime-zero-empty-filename-single-member",
        "decoded_serialization": "canonical-jsonl-final-LF",
        "row_schema": ROW_SCHEMAS[kind],
        "row_count": row_count,
        "ordered_row_id_sequence_sha256": id_state.hexdigest(),
        "ordered_row_sha256_sequence_sha256": row_hash_state.hexdigest(),
        "ordered_rows_sha256": rows_state.hexdigest(),
        "decoded_jsonl_sha256": raw_state.hexdigest(),
    })
    return descriptor


def _seed_schedule_validation(reconstruction: dict[str, Any], seed: int) -> None:
    roots = sorted(reconstruction["root_members"])
    if not roots:
        raise ProductionBlocked("empty seed schedule")
    offset = seed % len(roots)
    visited = 0
    for index in range(len(roots)):
        old_root = roots[(offset + index) % len(roots)]
        if old_root not in reconstruction["root_disposition"]:
            raise ProductionBlocked("seed schedule root orphan")
        visited += 1
    if visited != len(roots):
        raise ProductionBlocked("seed schedule coverage")


def _candidate_result_document(
    reconstruction: dict[str, Any],
    producer_sha256: str,
    artifact_descriptors: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    payload = {
        "schema": SCHEMA + ".result.v1",
        "status": "PASS_DETERMINISTIC_ROUND306C0_SELECTED_ROW_R248_CORRECTION_OVERLAY_AND_FRESH_FORWARD_REVERSE_DSU_CANDIDATE__ZERO_CREDIT",
        "producer_file_sha256": producer_sha256,
        "construction_source": reconstruction["construction_source_receipt"],
        "any_upstream_producer_or_verifier_imported_or_executed": False,
        "authority_frontier": {
            "filename": artifact_descriptors["authority_frontier"]["filename"],
            "sha256": artifact_descriptors["authority_frontier"]["sha256"],
            "size": artifact_descriptors["authority_frontier"]["size"],
        },
        "selected_row_R248_correction_overlay": {
            "status": "COMPLETE_FOR_EXACT_SELECTED_32_MEMBER_20_ROOT_SCOPE",
            "invalid_member_count": 32,
            "affected_old_root_count": 20,
            "deleted_singleton_component_count": 16,
            "surviving_rekey_component_count": 4,
            "Round306A_member_rows_not_revoked_by_exact_priority_overlay": 564_460,
            "transitively_binds_full_pinned_R248_via_sealed_R235D": True,
            "package_wide_regenerated_R248_certificate_claimed": False,
        },
        "corrected_member_and_root_universe": {
            "member_count": 564_460,
            "base_root_count": 367_948,
            "root_disposition_histogram": ROOT_DISPOSITION_CONTRACT[
                "disposition_histogram"
            ],
        },
        "fresh_forward_application": {
            "edge_application_count": 478_718,
            "rank_reduction": 275_276,
            "component_count": 92_672,
            "partition_sha256": reconstruction["partition_sha256"],
            "forward_rank_flag_mismatch_count": 0,
            "delete_root_hit_count": 0,
            "invalid_member_endpoint_hit_count": 0,
            "distinct_root_remap_collision_count": 0,
            "old_projected_self_root_cycle_row_count": 15_932,
        },
        "fresh_reverse_application": {
            "edge_application_count": 478_718,
            "rank_reduction": sum(reconstruction["reverse_flags"]),
            "component_count": 92_672,
            "partition_sha256": reconstruction["partition_sha256"],
            "same_partition_as_forward": True,
        },
        "affected_component_census": {
            "total_affected_old_component_count": len(
                reconstruction["affected_old_components"]
            ),
            "deleted_singleton_old_component_count": len(
                reconstruction["delete_component_transitions"]
            ),
            "deleted_singleton_old_to_corrected_sizes": [
                list(item) for item in reconstruction["delete_component_transitions"]
            ],
            "surviving_rekey_old_component_count": len(
                reconstruction["rekey_old_components"]
            ),
            "surviving_rekey_new_component_count": len(
                reconstruction["rekey_new_components"]
            ),
            "surviving_rekey_old_member_sizes": reconstruction[
                "affected_old_sizes"
            ],
            "surviving_rekey_corrected_member_sizes": reconstruction[
                "affected_new_sizes"
            ],
        },
        "pair_denominator": {
            "cross_component_pair_denominator": 158_820_108_554,
            "all_unordered_member_pairs": 159_307_263_570,
            "within_component_unordered_member_pairs": 487_155_016,
            "component_member_count_vector_sha256": reconstruction[
                "member_size_vector_sha256"
            ],
            "component_base_root_count_vector_sha256": reconstruction[
                "root_size_vector_sha256"
            ],
            "component_size_vector_definition": (
                "ascending-numeric sorted size multiset; mapping remains in component_census ledger"
            ),
        },
        "output_artifacts_in_publication_order_before_result": [
            artifact_descriptors[key] for key in OUTPUT_ORDER[:-1]
        ],
        "dual_distinct_explicit_traversal_seed_candidate_bytes_identical": True,
        "separate_interpreter_randomized_hash_replay_required_before_promotion": True,
        "candidate_result_committed_last_without_clobber": True,
        "final_all_23_pin_path_identity_revalidation_before_publication": True,
        "formal_credit_without_independent_verification_marker": {
            "corrected_member_universe": 0,
            "corrected_base_root_universe": 0,
            "corrected_DSU": 0,
            "pair_routing": 0,
            "normalized_full_support": 0,
            "representation_pullback": 0,
            "A1_A2": 0,
            "B1A": 0,
            "transition_atlas": 0,
            "B2": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "CM2": 0,
        },
        "candidate_credit_if_and_only_if_independently_verified": {
            "corrected_member_universe": 564_460,
            "corrected_base_root_universe": 367_948,
            "fresh_legal_edge_applications": 478_718,
            "fresh_DSU_rank_reductions": 275_276,
            "fresh_components": 92_672,
            "cross_component_pair_denominator": 158_820_108_554,
        },
        "downstream_nonpromotion": STRICT_NONPROMOTION,
    }
    return {**payload, "result_sha256": digest(payload)}


def _write_candidate_set(
    directory: _HeldDirectory,
    reconstruction: dict[str, Any],
    producer_sha256: str,
    seed: int,
) -> dict[str, dict[str, Any]]:
    _seed_schedule_validation(reconstruction, seed)
    descriptors: dict[str, dict[str, Any]] = {}
    authority = _authority_frontier_document(reconstruction, producer_sha256)
    descriptors["authority_frontier"] = _write_json_document(
        directory, "authority_frontier", authority, "authority_frontier_sha256"
    )
    for kind in (
        "member_invalidation", "root_disposition", "edge_remap",
        "member_component", "base_root_component", "component_census",
    ):
        descriptors[kind] = _write_jsonl_gzip_ledger(
            directory, kind, ROW_ITERATORS[kind](reconstruction)
        )
    pair = _pair_denominator_document(reconstruction)
    descriptors["pair_denominator"] = _write_json_document(
        directory, "pair_denominator", pair, "pair_denominator_sha256"
    )
    result = _candidate_result_document(reconstruction, producer_sha256, descriptors)
    descriptors["result"] = _write_json_document(
        directory, "result", result, "result_sha256"
    )
    if tuple(descriptors) != OUTPUT_ORDER:
        raise ProductionBlocked("candidate output publication order")
    return descriptors


def _fixed_spill_directories() -> tuple[
    _HeldDirectory, _HeldDirectory, _HeldDirectory
]:
    deliverables = Path(__file__).resolve(strict=True).parent
    fixed = Path(_fixed_spill_root_ignoring_tmpdir(os.environ.get("TMPDIR", ""), deliverables))
    parent = _open_absolute_directory_without_symlinks(fixed.parent)
    try:
        try:
            os.mkdir(fixed.name, 0o700, dir_fd=parent.fd)
        except FileExistsError:
            pass
        fixed_flags = (
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        )
        fixed_fd = os.open(fixed.name, fixed_flags, dir_fd=parent.fd)
    finally:
        _held_directory_path_identity(parent)
        os.close(parent.fd)
    fixed_info = os.fstat(fixed_fd)
    if (
        not stat.S_ISDIR(fixed_info.st_mode)
        or fixed_info.st_uid != os.getuid()
        or stat.S_IMODE(fixed_info.st_mode) != 0o700
    ):
        os.close(fixed_fd)
        raise ProductionBlocked("fixed spill root ownership/mode")
    fixed_directory = _HeldDirectory(
        fixed, fixed_fd, _directory_identity(fixed_info)
    )

    def create(prefix: str) -> _HeldDirectory:
        for _ in range(128):
            name = prefix + os.urandom(12).hex()
            try:
                os.mkdir(name, 0o700, dir_fd=fixed_directory.fd)
            except FileExistsError:
                continue
            flags = (
                os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
            )
            fd = os.open(name, flags, dir_fd=fixed_directory.fd)
            info = os.fstat(fd)
            if (
                not stat.S_ISDIR(info.st_mode)
                or info.st_uid != os.getuid()
                or stat.S_IMODE(info.st_mode) != 0o700
            ):
                os.close(fd)
                raise ProductionBlocked("private spill child ownership/mode")
            return _HeldDirectory(fixed / name, fd, _directory_identity(info))
        raise ProductionBlocked("unable to allocate private spill child")

    try:
        first = create("seed-a-")
        second = create("seed-b-")
    except BaseException:
        os.close(fixed_directory.fd)
        raise
    _held_directory_path_identity(fixed_directory)
    return first, second, fixed_directory


def _read_at(directory: _HeldDirectory, filename: str) -> int:
    return os.open(
        filename,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        dir_fd=directory.fd,
    )


def _assert_candidate_sets_byte_identical(
    first: _HeldDirectory, second: _HeldDirectory
) -> None:
    for key in OUTPUT_ORDER:
        filename = OUTPUTS[key]
        left_hash, left_identity = _held_at_hash(first, filename)
        right_hash, right_identity = _held_at_hash(second, filename)
        if left_identity[4] != right_identity[4] or left_hash != right_hash:
            raise ProductionBlocked("dual-seed candidate mismatch: " + key)
        left_fd = _read_at(first, filename)
        right_fd = _read_at(second, filename)
        try:
            while True:
                left_block = os.read(left_fd, 1024 * 1024)
                right_block = os.read(right_fd, 1024 * 1024)
                if left_block != right_block:
                    raise ProductionBlocked("dual-seed byte mismatch: " + key)
                if not left_block:
                    break
        finally:
            os.close(left_fd)
            os.close(right_fd)
    _held_directory_path_identity(first)
    _held_directory_path_identity(second)


def _candidate_directory(path_value: Any) -> _HeldDirectory:
    lexical = Path(os.path.abspath(os.fspath(path_value)))
    candidate = _open_absolute_directory_without_symlinks(lexical)
    info = os.fstat(candidate.fd)
    if (
        not stat.S_ISDIR(info.st_mode)
        or info.st_uid != os.getuid()
        or stat.S_IMODE(info.st_mode) != 0o700
    ):
        os.close(candidate.fd)
        raise ProductionBlocked("candidate directory must be owned mode-0700 directory")
    deliverables = Path(__file__).resolve(strict=True).parent
    if os.path.commonpath((os.fspath(lexical), os.fspath(deliverables))) == os.fspath(deliverables):
        os.close(candidate.fd)
        raise ProductionBlocked("candidate directory inside deliverables")
    for key in OUTPUT_ORDER:
        try:
            os.stat(OUTPUTS[key], dir_fd=candidate.fd, follow_symlinks=False)
        except FileNotFoundError:
            continue
        else:
            os.close(candidate.fd)
            raise ProductionBlocked("candidate output already exists: " + OUTPUTS[key])
    return candidate


def _publish_candidate_set(
    source: _HeldDirectory, candidate_value: Any
) -> dict[str, Any]:
    candidate = _candidate_directory(candidate_value)
    published: list[dict[str, Any]] = []
    try:
        for key in OUTPUT_ORDER:
            filename = OUTPUTS[key]
            source_hash, source_identity = _held_at_hash(source, filename)
            source_fd = _read_at(source, filename)
            flags = (
                os.O_WRONLY | os.O_CREAT | os.O_EXCL
                | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
            )
            destination_fd = os.open(
                filename, flags, 0o600, dir_fd=candidate.fd
            )
            try:
                while True:
                    block = os.read(source_fd, 1024 * 1024)
                    if not block:
                        break
                    view = memoryview(block)
                    while view:
                        written = os.write(destination_fd, view)
                        if written <= 0:
                            raise ProductionBlocked("short candidate publication write")
                        view = view[written:]
                os.fsync(destination_fd)
            finally:
                os.close(source_fd)
                os.close(destination_fd)
            target_hash, target_identity = _held_at_hash(candidate, filename)
            if target_hash != source_hash or target_identity[4] != source_identity[4]:
                raise ProductionBlocked("candidate publication byte mismatch")
            published.append({
                "role": key, "filename": filename,
                "size": target_identity[4], "sha256": target_hash,
            })
        os.fsync(candidate.fd)
        for item in reversed(published):
            target_hash, target_identity = _held_at_hash(
                candidate, item["filename"]
            )
            if (
                target_hash != item["sha256"]
                or target_identity[4] != item["size"]
                or target_identity[3] != 1
            ):
                raise ProductionBlocked(
                    "post-result reverse candidate revalidation: " + item["role"]
                )
        _held_directory_path_identity(candidate)
    finally:
        os.close(candidate.fd)
    return {
        "status": "PASS_CANDIDATE_PUBLICATION_RESULT_COMMITTED_LAST",
        "candidate_directory": os.fspath(candidate.path),
        "artifact_count": len(published),
        "artifacts_in_publication_order": published,
        "result_was_last": published[-1]["role"] == "result",
        "no_clobber_O_EXCL": True,
    }


def _static_duplicate_literal_key_check() -> int:
    source = Path(__file__).resolve(strict=True).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=__file__)
    dictionary_count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        dictionary_count += 1
        seen: set[str] = set()
        for key in node.keys:
            if isinstance(key, ast.Constant) and type(key.value) is str:
                if key.value in seen:
                    raise ProductionBlocked(
                        "duplicate literal dict key: " + key.value
                        + " at line " + str(node.lineno)
                    )
                seen.add(key.value)
    return dictionary_count


def _hold_construction_source() -> tuple[
    _HeldDirectory, str, tuple[int, ...], dict[str, Any]
]:
    lexical = Path(os.path.abspath(__file__))
    direct = lexical.stat(follow_symlinks=False)
    if lexical.is_symlink() or not stat.S_ISREG(direct.st_mode) or direct.st_nlink != 1:
        raise ProductionBlocked(
            "construction source must be invoked as a one-link regular non-symlink file"
        )
    parent = _open_absolute_directory_without_symlinks(lexical.parent)
    source_hash, source_identity = _held_at_hash(parent, lexical.name)
    if source_identity != _file_identity(direct):
        os.close(parent.fd)
        raise ProductionBlocked("construction source changed before held-dirfd bind")
    receipt = {
        "status": "PASS_HELD_DIRFD_ONE_LINK_CONSTRUCTION_SOURCE_BINDING",
        "filename": lexical.name,
        "size": source_identity[4],
        "sha256": source_hash,
        "invocation_symlink_rejected": True,
        "final_path_identity_revalidation_required": True,
    }
    return parent, source_hash, source_identity, receipt


def _revalidate_construction_source(
    parent: _HeldDirectory,
    expected_hash: str,
    expected_identity: tuple[int, ...],
) -> None:
    observed_hash, observed_identity = _held_at_hash(parent, Path(__file__).name)
    if observed_hash != expected_hash or observed_identity != expected_identity:
        raise ProductionBlocked("late construction-source replacement")
    _held_directory_path_identity(parent)


def production_contract(
    round_receipt: dict[str, Any] | None = None,
    r235d_pin_receipt: dict[str, Any] | None = None,
    r235d_semantic_receipt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _require_isolated_runtime()
    (
        source_parent, source_hash, source_identity,
        construction_source_receipt,
    ) = _hold_construction_source()
    if round_receipt is None or r235d_pin_receipt is None or r235d_semantic_receipt is None:
        round_first, round_receipt = _pin_vector_audit(
            "ROUND306A", ROUND306A_MANIFEST, ROUND306A_MANIFEST_MEMBERS
        )
        r235d_first, r235d_pin_receipt = _pin_vector_audit(
            "R235D", R235D_FINAL_PINS[0], R235D_FINAL_PINS[1:]
        )
        _, _, _, r235d_semantic_receipt = _semantic_r235d_audit(r235d_first)
        _final_all_pin_path_revalidation((
            ((ROUND306A_MANIFEST, *ROUND306A_MANIFEST_MEMBERS), round_first),
            (R235D_FINAL_PINS, r235d_first),
        ))
    snapshot = _schema_snapshot()
    payload = {
        "schema": SCHEMA + ".producer-contract.v2",
        "status": "PRODUCTION_READY_EXACT_23_PIN_SELECTED_ROW_R248_OVERLAY_AND_FRESH_DSU_IMPLEMENTED",
        "production_ready": True,
        "construction_source": construction_source_receipt,
        "complete_pin_count": 23,
        "round306a_pin_audit": round_receipt,
        "r235d_pin_audit": r235d_pin_receipt,
        "r235d_semantic_audit": r235d_semantic_receipt,
        "r235d_required_roles": list(R235D_REQUIRED_ROLES),
        "r235d_final_pins": [asdict(pin) for pin in R235D_FINAL_PINS],
        "schema_snapshot": snapshot,
        "schema_snapshot_sha256": digest(snapshot),
        "candidate_output_order": list(OUTPUT_ORDER),
        "candidate_result_committed_last": True,
        "dual_distinct_explicit_traversal_seed_byte_identity_required": True,
        "separate_interpreter_randomized_hash_replay_required_before_promotion": True,
        "complete_selected_row_R248_overlay_not_package_wide_regeneration": True,
        "independent_verifier_last_and_sole_credit_marker": True,
        "strict_nonpromotion": STRICT_NONPROMOTION,
    }
    document = {**payload, "contract_sha256": digest(payload)}
    _revalidate_construction_source(
        source_parent, source_hash, source_identity
    )
    os.close(source_parent.fd)
    return document


def production_self_test() -> dict[str, Any]:
    _require_isolated_runtime()
    source_parent, source_hash, source_identity, source_receipt = (
        _hold_construction_source()
    )
    dictionary_count = _static_duplicate_literal_key_check()
    pure_contract_attacks = _run_pure_contract_attacks()
    round_first, round_receipt = _pin_vector_audit(
        "ROUND306A", ROUND306A_MANIFEST, ROUND306A_MANIFEST_MEMBERS
    )
    r235d_first, r235d_pin_receipt = _pin_vector_audit(
        "R235D", R235D_FINAL_PINS[0], R235D_FINAL_PINS[1:]
    )
    _, _, _, r235d_semantic_receipt = _semantic_r235d_audit(r235d_first)
    _final_all_pin_path_revalidation((
        ((ROUND306A_MANIFEST, *ROUND306A_MANIFEST_MEMBERS), round_first),
        (R235D_FINAL_PINS, r235d_first),
    ))
    document = production_contract(
        round_receipt, r235d_pin_receipt, r235d_semantic_receipt
    )
    payload = dict(document)
    claimed = payload.pop("contract_sha256")
    if digest(payload) != claimed or document.get("production_ready") is not True:
        raise ProductionBlocked("production contract self-check")
    if tuple(pin.role for pin in R235D_FINAL_PINS) != R235D_REQUIRED_ROLES:
        raise ProductionBlocked("R235D exact role order")
    if tuple(OUTPUTS) != OUTPUT_ORDER:
        raise ProductionBlocked("output map/order mismatch")
    for kind in ROW_FIELDS:
        if len(ROW_FIELDS[kind]) != len(set(ROW_FIELDS[kind])):
            raise ProductionBlocked("duplicate row field: " + kind)
    test_raw = canonical_bytes({"x": 1})
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as stream:
        stream.write(test_raw)
    if _strict_gzip_single_member(buffer.getvalue(), "self-test", 1024) != test_raw:
        raise ProductionBlocked("single gzip self-test")
    second = buffer.getvalue() + buffer.getvalue()
    rejected_multimember = False
    try:
        _strict_gzip_single_member(second, "multimember", 1024)
    except ProductionBlocked:
        rejected_multimember = True
    if not rejected_multimember:
        raise ProductionBlocked("gzip multimember accepted")
    _revalidate_construction_source(
        source_parent, source_hash, source_identity
    )
    os.close(source_parent.fd)
    return {
        "schema": SCHEMA + ".self-test.v2",
        "status": "PASS_PRODUCTION_READY_EXACT_23_PIN_NO_WRITE_SELF_TEST",
        "python_runtime_isolated": True,
        "python_runtime_dont_write_bytecode": True,
        "complete_pin_count": 23,
        "static_literal_dictionary_count_checked": dictionary_count,
        "duplicate_literal_dict_key_count": 0,
        "pure_contract_attacks": pure_contract_attacks,
        "R235D_exact_role_order": True,
        "single_gzip_member_enforced": True,
        "candidate_filesystem_write_attempted": False,
        "construction_source": source_receipt,
        "contract_sha256": document["contract_sha256"],
    }


def _cleanup_private_spill(
    directories: tuple[_HeldDirectory, _HeldDirectory],
    fixed_directory: _HeldDirectory,
) -> None:
    cleanup_error: BaseException | None = None
    for directory in directories:
        try:
            for filename in OUTPUTS.values():
                try:
                    info = os.stat(
                        filename, dir_fd=directory.fd, follow_symlinks=False
                    )
                except FileNotFoundError:
                    continue
                if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                    raise ProductionBlocked(
                        "refuse unsafe spill cleanup target: " + filename
                    )
                os.unlink(filename, dir_fd=directory.fd)
            if os.listdir(directory.fd):
                raise ProductionBlocked("unexpected private spill entry")
            current = os.stat(
                directory.path.name,
                dir_fd=fixed_directory.fd,
                follow_symlinks=False,
            )
            if _directory_identity(current) != directory.identity:
                raise ProductionBlocked("spill child path identity changed")
        except BaseException as exc:
            cleanup_error = cleanup_error or exc
        finally:
            os.close(directory.fd)
        if cleanup_error is None:
            os.rmdir(directory.path.name, dir_fd=fixed_directory.fd)
    try:
        _held_directory_path_identity(fixed_directory)
    except BaseException as exc:
        cleanup_error = cleanup_error or exc
    os.close(fixed_directory.fd)
    if cleanup_error is not None:
        raise cleanup_error


def _production_entry_with_held_source(
    candidate_value: Any | None,
    no_write: bool,
    seed: int,
    source_parent: _HeldDirectory,
    producer_sha256: str,
    source_identity: tuple[int, ...],
    source_receipt: dict[str, Any],
) -> dict[str, Any]:
    round_first, round_receipt = _pin_vector_audit(
        "ROUND306A", ROUND306A_MANIFEST, ROUND306A_MANIFEST_MEMBERS
    )
    r235d_first, r235d_pin_receipt = _pin_vector_audit(
        "R235D", R235D_FINAL_PINS[0], R235D_FINAL_PINS[1:]
    )
    r235d_result, _, r235d_rows, r235d_semantic_receipt = _semantic_r235d_audit(
        r235d_first
    )
    reconstruction = _build_reconstruction(
        round_first, r235d_first, round_receipt, r235d_pin_receipt,
        r235d_result, r235d_rows, r235d_semantic_receipt,
    )
    reconstruction["construction_source_receipt"] = source_receipt
    first_spill, second_spill, fixed_directory = _fixed_spill_directories()
    try:
        first_descriptors = _write_candidate_set(
            first_spill, reconstruction, producer_sha256, seed
        )
        second_seed = seed ^ 0x5A5A5A5A5A5A5A5A
        _write_candidate_set(second_spill, reconstruction, producer_sha256, second_seed)
        _assert_candidate_sets_byte_identical(first_spill, second_spill)
        _final_all_pin_path_revalidation((
            ((ROUND306A_MANIFEST, *ROUND306A_MANIFEST_MEMBERS), round_first),
            (R235D_FINAL_PINS, r235d_first),
        ))
        _revalidate_construction_source(
            source_parent, producer_sha256, source_identity
        )
        if no_write:
            return {
                "schema": SCHEMA + ".no-write-replay-receipt.v1",
                "status": "PASS_FULL_RECONSTRUCTION_DUAL_SEED_BYTE_IDENTITY_NO_CANDIDATE_PUBLICATION",
                "artifact_count": 9,
                "candidate_publication_attempted": False,
                "dual_seed_a": seed,
                "dual_seed_b": second_seed,
                "same_interpreter_values_are_explicit_traversal_seeds_not_Python_hash_seeds": True,
                "separate_interpreter_randomized_hash_replay_still_required_for_final_promotion": True,
                "artifact_descriptors": [
                    first_descriptors[key] for key in OUTPUT_ORDER
                ],
                "corrected_partition_sha256": reconstruction["partition_sha256"],
            }
        if candidate_value is None:
            raise ProductionBlocked("candidate directory required unless --no-write")
        return _publish_candidate_set(first_spill, candidate_value)
    finally:
        _cleanup_private_spill(
            (first_spill, second_spill), fixed_directory
        )


def production_entry(
    candidate_value: Any | None, no_write: bool, seed: int
) -> dict[str, Any]:
    source_parent, source_hash, source_identity, source_receipt = (
        _hold_construction_source()
    )
    try:
        return _production_entry_with_held_source(
            candidate_value, no_write, seed, source_parent,
            source_hash, source_identity, source_receipt,
        )
    finally:
        os.close(source_parent.fd)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--candidate-dir")
    return parser.parse_args()


def main() -> int:
    _require_isolated_runtime()
    args = parse_args()
    if type(args.seed) is not int or not 0 <= args.seed < 2**63:
        raise SystemExit("seed must be an integer in [0, 2**63)")
    selected_modes = sum((
        int(args.contract), int(args.self_test), int(args.no_write),
        int(args.candidate_dir is not None),
    ))
    if selected_modes > 1:
        raise SystemExit(
            "choose exactly one of --contract, --self-test, --no-write, --candidate-dir"
        )
    if args.self_test:
        print(ENCODER.encode(production_self_test()))
        return 0
    if args.no_write:
        print(ENCODER.encode(production_entry(None, True, args.seed)))
        return 0
    if args.candidate_dir is not None:
        print(ENCODER.encode(production_entry(args.candidate_dir, False, args.seed)))
        return 0
    print(ENCODER.encode(production_contract()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
