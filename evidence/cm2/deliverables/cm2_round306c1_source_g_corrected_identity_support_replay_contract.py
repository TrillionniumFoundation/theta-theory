#!/usr/bin/env python3
"""Round306C1 corrected identity/support replay no-production contract.

This executable is deliberately a contract skeleton, not a producer.  The
complete final R235D invalidation theorem package and complete final Round306C0
fresh freeze package are pinned below.  Candidate paths remain rejected before
any path operation until this skeleton is replaced by an independently
verifiable implementation.

The legacy AF2, B1G0, and K2I0--K2I4 artifacts are audited here only to freeze
the migration boundary.  Their old component identifiers, component-derived
rows, row identifiers, and formal-credit state are expressly superseded.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import stat
import sys
import zlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Final


class ProductionBlocked(RuntimeError):
    """Fail-closed contract or pre-production gate."""


ENCODER: Final = json.JSONEncoder(
    ensure_ascii=True,
    allow_nan=False,
    sort_keys=True,
    separators=(",", ":"),
)
MAX_DECODED_ROW_BYTES: Final = 8 * 1024 * 1024


def canonical_bytes(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


@dataclass(frozen=True)
class FrozenPin:
    role: str
    filename: str
    size: int
    sha256: str


PREFIX: Final = "cm2_round306c1_source_g_corrected_identity_support_replay"
SCHEMA: Final = "cm2.round306c1.source-g-corrected-identity-support-replay.v1"
CORRECTED_COMPONENT_NAMESPACE: Final = "round306c0-fresh-legal-component:"
ROW_NAMESPACE: Final = "round306c1-corrected-identity-support:"
FIXED_EXTERNAL_SPILL_ROOT: Final = "/tmp/cm2-round306c1-spill"


def _require_isolated_runtime() -> None:
    if type(sys.flags.isolated) is not int or sys.flags.isolated != 1:
        raise ProductionBlocked("run with python3 -I -B: isolated mode is required")
    if sys.dont_write_bytecode is not True:
        raise ProductionBlocked("run with python3 -I -B: bytecode writes must be disabled")


# These small, immutable files are migration-audit evidence only.  They do not
# confer authority on an old component id or an old K2I-derived output row.
LEGACY_AUDIT_PINS: Final = (
    FrozenPin("AF2_CONTRACT", "cm2_round306b1af2_source_g_primitive_support_source_partition_freeze_contract.py", 52_538, "a91578a8bef1c4a72f940f7ebc71aea4c0ebc1ddac08ddbb3889a2da6cdd00f5"),
    FrozenPin("AF2_PRIMARY_REPLAY", "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_replay.py", 20_783, "b7fcae488bd1e9e301f7191e65ade22f87c393a083a1335147ccf1bc92cddb27"),
    FrozenPin("AF2_PRIMARY_RESULT", "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_result.json", 2_540, "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb"),
    FrozenPin("AF2_INDEPENDENT_REPLAY", "cm2_round306b1af2_source_g_primitive_support_source_partition_independent_replay.py", 23_694, "38551c822f9aa74989b54749a3e05e8fe9bdce205fb12efb12eaa7382e6ccab4"),
    FrozenPin("AF2_INDEPENDENT_RESULT", "cm2_round306b1af2_source_g_primitive_support_source_partition_independent_result.json", 2_540, "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb"),
    FrozenPin("B1G0_MANIFEST", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256", 1_959, "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8"),
    FrozenPin("B1G0_RESULT", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_result.json", 5_006, "3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e"),
    FrozenPin("I0_MANIFEST", "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_manifest.sha256", 1_438, "38510f1ec1c1c9ddcc73cb6f3f95b015faed98c295227d9c627564ff8fabc5fc"),
    FrozenPin("I0_RESULT", "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_result.json", 7_208, "ac88dd5157de65f82cba7478e62e7cd45df122b2548923bb799e4c059765f5af"),
    FrozenPin("I1_MANIFEST", "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_manifest.sha256", 1_631, "e06efae8395e96cf3c1d0489c4de58cbc5e05357b6789f6fb1e56906b6026970"),
    FrozenPin("I1_RESULT", "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_result.json", 9_160, "65ed7a13792edfe7609662126e4357b9e1ebff39b7d749a959b5a19cb3d5e96a"),
    FrozenPin("I2_MANIFEST", "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_manifest.sha256", 1_650, "32309d3649e50e5e79b2c9b6a91a97d4fc53c8fe352c5516425a03f33ffd57b4"),
    FrozenPin("I2_RESULT", "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_result.json", 14_562, "4cd7c9982cdd9a72f34a912d78b6dd061fd8351b31581c84b5aaf20a70893e82"),
    FrozenPin("I3_MANIFEST", "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_manifest.sha256", 1_840, "304db35c33fa6c1ab989885b4aecde6d1ccc6d38d2578282a62365ef760f7a26"),
    FrozenPin("I3_RESULT", "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_result.json", 8_648, "ad2b74c0d886513efdee1d7a0c0d6346f4dd5d13584ce98822556f19fdc5ae5a"),
    FrozenPin("I4_MANIFEST", "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_manifest.sha256", 2_176, "53b84967618f80c0781c6728ceef4f0e88df7862bd37c5f4cae4055caf960051"),
    FrozenPin("I4_RESULT", "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_result.json", 30_666, "cf13c5163fcde7415f39529f11002cefaad5d211abdac72613bdeab620d49753"),
)

LEGACY_MANIFEST_EXPECTATIONS: Final = {
    "B1G0_MANIFEST": {"line_count": 13, "result_role": "B1G0_RESULT"},
    "I0_MANIFEST": {"line_count": 9, "result_role": "I0_RESULT"},
    "I1_MANIFEST": {"line_count": 10, "result_role": "I1_RESULT"},
    "I2_MANIFEST": {"line_count": 10, "result_role": "I2_RESULT"},
    "I3_MANIFEST": {"line_count": 12, "result_role": "I3_RESULT"},
    "I4_MANIFEST": {"line_count": 12, "result_role": "I4_RESULT"},
}

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

C0_FINAL_PINS: Final[tuple[FrozenPin, ...]] = (
    FrozenPin("C0_MANIFEST", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_manifest.sha256", 2_182, "9ddb6e0ad37b634de8b2edf8573247e7c1263a5c3693c77a7d001241712b25f8"),
    FrozenPin("C0_PRODUCER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_producer.py", 150_188, "35055dbdbe6562f3720c48a253d19089dd7263d8aed4243b0aa8b09dacad15a4"),
    FrozenPin("C0_AUTHORITY_FRONTIER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_authority_frontier.json", 18_227, "ea0b2078c6561907674948bc3dac7d868260b3ee2b5ae2d51d0e2bf36d257035"),
    FrozenPin("C0_MEMBER_INVALIDATION_LEDGER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_member_invalidation_ledger.jsonl.gz", 11_867, "865185d9b49d4e220459cb083683fd5a074f63eff4f7f2f8217a5c5204991eae"),
    FrozenPin("C0_BASE_ROOT_DISPOSITION_LEDGER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_base_root_disposition_ledger.jsonl.gz", 115_696_187, "6c8e84a6f247a00470f4abd2b6bb7c4caff6ff813236c3e63f04b884998eccdb"),
    FrozenPin("C0_EDGE_REMAP_LEDGER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_edge_remap_application_ledger.jsonl.gz", 165_250_881, "26c941631a839d757fb764486f5334fb913146a5cfaa8f65622e9b71b204b907"),
    FrozenPin("C0_MEMBER_COMPONENT_LEDGER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_fresh_member_component_ledger.jsonl.gz", 188_288_564, "81c5a772b12dfb0cf9196b13319bbdff7b07806f6df22d9966a4fc9399bed12e"),
    FrozenPin("C0_BASE_ROOT_COMPONENT_LEDGER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_fresh_base_root_component_ledger.jsonl.gz", 83_303_270, "a7c003f0ca87c02a8f21adb4ce4cac2b0e632dbfa1cfe3046cbdd484659025b3"),
    FrozenPin("C0_COMPONENT_CENSUS_LEDGER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_fresh_component_census.jsonl.gz", 14_156_321, "127f57a139d824b55723199fc299fbb8e9449902f1c45d4b3ced714ac61c3b5d"),
    FrozenPin("C0_PAIR_DENOMINATOR", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_cross_component_pair_denominator.json", 1_486, "df9af25ea83cb52d78c6f4d9c3ed357d6af1feaefc09a132c1074dd920118d49"),
    FrozenPin("C0_RESULT", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_result.json", 10_689, "4adcc91dd6bcaf71853d429e16f91d7ed93d04641097d12abe0ebc5a7e8864a1"),
    FrozenPin("C0_INDEPENDENT_VERIFIER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_independent_verifier.py", 101_099, "bcabf0a64c0813f7d883d1380d313a1b51d82396796bf5304fb6f53d34e54f50"),
    FrozenPin("C0_ATTACK_SUITE", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_attack_suite.json", 5_994, "efd3631209c9cccdd8a3e43acebe99011687cbab2ccf67666ac2ae7a5013daad"),
    FrozenPin("C0_VERIFICATION", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_verification.json", 4_413, "9aee2aae01d116c6c6967c4aec1a9d80c9728eff3d3bdc8f7fc4d836c9f07eb2"),
    FrozenPin("C0_REPORT", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_report.md", 4_649, "6288d860189e71367358d3a7726b2403646f25865aeab4255439591fa02c99d2"),
    FrozenPin("C0_COLD_REPLAY", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_cold_replay.md", 1_415, "e3977647e498853a5eb444032891ec3491c708ca630d2f4d1cb4d4a7a4aabe43"),
)
C0_REQUIRED_ROLES: Final = (
    "C0_MANIFEST",
    "C0_PRODUCER",
    "C0_AUTHORITY_FRONTIER",
    "C0_MEMBER_INVALIDATION_LEDGER",
    "C0_BASE_ROOT_DISPOSITION_LEDGER",
    "C0_EDGE_REMAP_LEDGER",
    "C0_MEMBER_COMPONENT_LEDGER",
    "C0_BASE_ROOT_COMPONENT_LEDGER",
    "C0_COMPONENT_CENSUS_LEDGER",
    "C0_PAIR_DENOMINATOR",
    "C0_RESULT",
    "C0_INDEPENDENT_VERIFIER",
    "C0_ATTACK_SUITE",
    "C0_VERIFICATION",
    "C0_REPORT",
    "C0_COLD_REPLAY",
)

OLD_AUDIT_CENSUS: Final = {
    "members": {
        "PRESERVED": 126_468,
        "NON_GRAPH": 17_828,
        "R2": 295_336,
        "R292": 9_404,
        "G2A": 38_624,
        "G2B": 76_832,
    },
    "representations": {
        "PRESERVED": 165_744,
        "NON_GRAPH": 17_828,
        "R2": 302_624,
        "R292": 10_252,
        "G2A": 38_624,
        "G2B": 76_832,
    },
    "member_count": 564_492,
    "representation_count": 611_904,
    "G2B_reference_count": 76_848,
    "B1G0_graph_count": 38_624,
    "B1G0_sheet_count": 38_624,
    "B1G0_side_reference_count": 76_848,
    "B1G0_distinct_member_backbinding_count": 115_456,
    "B1G0_physical_incidence_reference_count": 115_472,
    "B1G0_gap_count": 154_096,
    "theorem_obligation_census_not_feature_rows": 824_864,
}

CORRECTED_CENSUS: Final = {
    "members": {
        "PRESERVED": 126_468,
        "NON_GRAPH": 17_828,
        "R2": 295_336,
        "R292": 9_404,
        "G2A": 38_608,
        "G2B": 76_816,
    },
    "representations": {
        "PRESERVED": 165_744,
        "NON_GRAPH": 17_828,
        "R2": 302_624,
        "R292": 10_252,
        "G2A": 38_608,
        "G2B": 76_816,
    },
    "member_count": 564_460,
    "representation_count": 611_872,
    "fresh_component_count": 92_672,
    "G2A_graph_and_sheet_count": 38_608,
    "G2B_reference_count": 76_816,
    "G2B_distinct_member_count": 76_816,
    "G2B_duplicate_reference_excess": 0,
    "physical_incidence_reference_count": 115_424,
    "B1G0_member_backbinding_count": 115_424,
    "B1G0_gap_count": 154_032,
}

# Acceptance expectations for the future sealed C0 input.  These values are
# not minted by C1 and cannot substitute for the absent C0 manifest and final
# independent verification marker.
C0_MIGRATION_EXPECTATION: Final = {
    "status": "EXPECTED_FROM_FINAL_C0__MUST_BE_RECOMPUTED_AND_PINNED_BEFORE_C1_PRODUCTION",
    "member_count": 564_460,
    "base_root_count": 367_948,
    "legal_edge_application_count": 478_718,
    "fresh_component_count": 92_672,
    "corrected_partition_sha256": "1ae914d4e2cff22d1fa6ddad4ffe4679c594bde3cdad27acf1480202b7a89434",
    "cross_component_pair_denominator": 158_820_108_554,
    "C1_minted_any_of_these_facts": False,
}

CORRECTED_OBLIGATION_CENSUS: Final = {
    "status": "EXACT_THEOREM_OBLIGATION_CENSUS_ONLY__NOT_FEATURE_LEDGER_ROWS",
    "superseded_old_total": 824_864,
    "root": {
        "preserved_non_graph_A1_A2": 17_940,
        "R2_predicate_cells": 295_340,
        "G2_graph_definitions": 38_608,
        "total": 351_888,
    },
    "dependent": {
        "preserved_non_graph_A1_A2": 62_152,
        "R2_member_pullbacks": 295_336,
        "G2_graph_sheet_identifications": 38_608,
        "G2_graph_side_incidences": 76_816,
        "total": 472_912,
    },
    "corrected_total": 824_800,
    "old_to_corrected_decrease": 64,
    "known_final_feature_ledger_row_count": None,
}

FRESH_COMPONENT_REBIND: Final = {
    "scope": "SURVIVORS_IN_FOUR_REKEYED_OLD_COMPONENTS_ONLY",
    "member_count": 21_848,
    "members_by_family": {
        "PRESERVED": 14_400,
        "NON_GRAPH": 1_776,
        "R2": 800,
        "R292": 3_776,
        "G2A": 584,
        "G2B": 512,
    },
    "old_component_ids_are_provenance_only": True,
    "all_564460_member_rows_bind_fresh_C0_component_ids": True,
}

OUTPUTS: Final = {
    "authority_frontier": PREFIX + "_authority_frontier.json",
    "family_census": PREFIX + "_family_census.jsonl.gz",
    "member": PREFIX + "_member_identity_support_ledger.jsonl.gz",
    "representation": PREFIX + "_representation_ledger.jsonl.gz",
    "physical_incidence": PREFIX + "_physical_incidence_statement_ledger.jsonl.gz",
    "gap": PREFIX + "_semantic_gap_ledger.jsonl.gz",
    "component_rebind": PREFIX + "_affected_component_rebind_ledger.jsonl.gz",
    "transition_handle": PREFIX + "_transition_ready_handle_ledger.jsonl.gz",
    "obligation_census": PREFIX + "_theorem_obligation_census.json",
    "result": PREFIX + "_result.json",
}

ROW_SCHEMAS: Final = {
    "family_census": SCHEMA + ".family-census-row.v1",
    "member": SCHEMA + ".member-identity-support-row.v1",
    "representation": SCHEMA + ".representation-row.v1",
    "physical_incidence": SCHEMA + ".physical-incidence-statement-row.v1",
    "gap": SCHEMA + ".semantic-gap-row.v1",
    "component_rebind": SCHEMA + ".affected-component-rebind-row.v1",
    "transition_handle": SCHEMA + ".transition-ready-handle-row.v1",
}

ROW_FIELDS: Final = {
    "family_census": (
        "schema", "row_id", "coarse_family", "member_count",
        "representation_count", "member_ids_sha256",
        "representation_ids_sha256", "source_authority_commitment_sha256",
        "canonical_input_commitment_sha256", "formal_credit", "row_sha256",
    ),
    "member": (
        "schema", "row_id", "member_id", "coarse_family",
        "primitive_source_kind", "source_authority_role", "source_filename",
        "source_table", "source_path", "source_row_id", "source_row_sha256",
        "r235d_disposition", "c0_member_component_row_id",
        "c0_member_component_row_sha256", "corrected_component_id",
        "typed_support_ast", "certificate_grammar",
        "mechanical_representation_count", "mechanical_representation_ids_sha256",
        "primary_mechanical_representation_id", "support_semantic_state",
        "canonical_input_commitment_sha256", "formal_credit", "row_sha256",
    ),
    "representation": (
        "schema", "row_id", "representation_id", "owner_member_id",
        "coarse_family", "representation_role", "source_authority_role",
        "source_filename", "source_table", "source_path", "source_row_id",
        "source_row_sha256", "typed_representation_ast",
        "certificate_grammar", "pullback_semantic_state",
        "owner_member_row_id", "owner_member_row_sha256",
        "canonical_input_commitment_sha256", "formal_credit", "row_sha256",
    ),
    "physical_incidence": (
        "schema", "row_id", "graph_id", "incidence_role", "member_id",
        "coarse_family", "source_graph_row_id", "source_graph_row_sha256",
        "source_incidence_row_id", "source_incidence_row_sha256",
        "member_row_id", "member_row_sha256", "incidence_statement_ast",
        "theorem_semantic_state", "canonical_input_commitment_sha256",
        "formal_credit", "row_sha256",
    ),
    "gap": (
        "schema", "row_id", "gap_kind", "subject_kind", "subject_row_id",
        "member_id", "coarse_family", "required_closure",
        "source_statement_row_id", "source_statement_row_sha256",
        "blocking_credit_kinds", "canonical_input_commitment_sha256",
        "formal_credit", "row_sha256",
    ),
    "component_rebind": (
        "schema", "row_id", "member_id", "coarse_family",
        "old_component_id_provenance_only", "old_component_row_sha256",
        "c0_member_component_row_id", "c0_member_component_row_sha256",
        "corrected_component_id", "rebind_reason",
        "canonical_input_commitment_sha256", "formal_credit", "row_sha256",
    ),
    "transition_handle": (
        "schema", "row_id", "member_id", "coarse_family",
        "member_row_id", "member_row_sha256", "typed_support_ast_sha256",
        "representation_set_sha256", "corrected_component_id",
        "transition_syntax_ready", "transition_semantics_ready",
        "canonical_input_commitment_sha256", "formal_credit", "row_sha256",
    ),
}

TYPE_RULES: Final = {
    "all_object_keys": "exact schema field set; no extras and no omissions",
    "count": "type(value) is int and value >= 0; bool is rejected",
    "boolean": "type(value) is bool; integers 0 and 1 are rejected",
    "identifier": "nonempty ASCII string in the declared namespace",
    "sha256": "exactly 64 lowercase hexadecimal characters",
    "formal_credit": "exact-key object whose values have type int and equal 0",
    "typed_support_ast": {
        "allowed_roots": [
            "PRESERVED_CONSTRUCTION",
            "NON_GRAPH_BULK_CONSTRUCTION",
            "R2_PREDICATE_CELL_UNION",
            "R292_REFINEMENT_PULLBACK",
            "G2A_GRAPH_SHEET",
            "G2B_GRAPH_SIDE",
        ],
        "outer_envelope_is_full_support": False,
        "inner_witness_is_full_support": False,
        "source_and_all_children_are_input_committed": True,
    },
    "certificate_grammar": {
        "domain_guards_are_raw_and_type_strict": True,
        "A1_A2_incidence_equivalence_and_pullback_are_distinct_nodes": True,
        "result_digest_binds_full_canonical_input_and_result": True,
    },
}

REQUIRED_ATTACKS: Final = (
    "missing_partial_or_wrong_order_R235D_complete_seal",
    "missing_partial_or_wrong_order_C0_complete_seal",
    "candidate_path_probe_before_both_complete_seals",
    "keep_one_of_32_R235D_invalid_members",
    "drop_one_of_564460_corrected_members",
    "reuse_old_Round306A_component_id_as_corrected_identity",
    "copy_old_I0_I1_I2_I3_or_I4_derived_row_as_formal_row",
    "omit_one_of_21848_affected_component_rebinds",
    "wrong_six_family_member_or_representation_census",
    "restore_old_G2A_or_G2B_count",
    "restore_old_G2B_duplicate_reference_excess",
    "wrong_115424_physical_incidence_census",
    "wrong_154032_B1G0_gap_census",
    "call_824800_a_feature_ledger_row_count",
    "canonical_result_digest_does_not_bind_complete_input",
    "member_representation_or_incidence_orphan_duplicate_or_overlap",
    "duplicate_json_key_float_nonfinite_or_noncanonical_separator",
    "bool_int_alias_in_count_credit_or_contract_equality",
    "second_gzip_member_trailing_bytes_or_final_decoded_row_over_8MiB",
    "pin_symlink_hardlink_held_fd_TOCTOU_or_late_first_pin_replacement",
    "TMPDIR_redirects_spill_into_deliverables",
    "second_hash_seed_changes_candidate_bytes",
    "independent_verifier_imports_or_executes_producer",
    "result_committed_before_any_ledger_or_clobbers_existing_path",
    "default_contract_self_test_or_failed_preflight_writes_any_path",
    "nonisolated_python_or_bytecode_writes_enabled",
)

ATTACK_MATRIX: Final = tuple(
    (f"C1A{index:02d}", mutation, "REJECT")
    for index, mutation in enumerate(REQUIRED_ATTACKS, 1)
)


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
        text = raw.decode("ascii")
        value = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProductionBlocked("strict JSON failure: " + label) from exc
    if canonical_bytes(value) != raw:
        raise ProductionBlocked("noncanonical JSON bytes: " + label)
    return value


def _strict_int(value: Any, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ProductionBlocked("non-strict nonnegative integer: " + label)
    return value


def _strict_bool(value: Any, label: str) -> bool:
    if type(value) is not bool:
        raise ProductionBlocked("non-strict boolean: " + label)
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
                index for index, (right_key, _) in enumerate(unmatched)
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


def _strict_zero_credit_map(value: Any, label: str) -> None:
    if type(value) is not dict or not value:
        raise ProductionBlocked("formal-credit object: " + label)
    for key, credit in value.items():
        if type(key) is not str or not key:
            raise ProductionBlocked("formal-credit key: " + label)
        if type(credit) is not int or credit != 0:
            raise ProductionBlocked("nonzero or aliased formal credit: " + label)


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


def _held_fd_read(path: Path) -> tuple[bytes, tuple[int, ...]]:
    try:
        before = path.stat(follow_symlinks=False)
    except OSError as exc:
        raise ProductionBlocked("missing audit pin: " + path.name) from exc
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise ProductionBlocked("pin is not a one-link regular file: " + path.name)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise ProductionBlocked("held-FD open failure: " + path.name) from exc
    chunks: list[bytes] = []
    try:
        opened = os.fstat(fd)
        identity = _file_identity(opened)
        if identity != _file_identity(before):
            raise ProductionBlocked("pin changed before held-FD open: " + path.name)
        while True:
            chunk = os.read(fd, 64 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after_fd = os.fstat(fd)
    finally:
        os.close(fd)
    after_path = path.stat(follow_symlinks=False)
    if _file_identity(after_fd) != identity or _file_identity(after_path) != identity:
        raise ProductionBlocked("pin changed during held-FD read: " + path.name)
    return b"".join(chunks), identity


_MANIFEST_LINE = re.compile(rb"([0-9a-f]{64})  ([!-~]+)")


def _parse_manifest(raw: bytes, label: str, expected_lines: int) -> dict[str, str]:
    lines = raw.splitlines()
    if len(lines) != expected_lines or raw != b"\n".join(lines) + b"\n":
        raise ProductionBlocked("manifest line framing mismatch: " + label)
    members: dict[str, str] = {}
    for line in lines:
        match = _MANIFEST_LINE.fullmatch(line)
        if match is None:
            raise ProductionBlocked("manifest syntax: " + label)
        sha = match.group(1).decode("ascii")
        filename = match.group(2).decode("ascii")
        candidate = Path(filename)
        if candidate.is_absolute() or ".." in candidate.parts or filename in members:
            raise ProductionBlocked("unsafe or duplicate manifest filename: " + label)
        members[filename] = sha
    return members


def _manifest_contains_result(
    members: dict[str, str], result_pin: FrozenPin, label: str
) -> None:
    matches = [
        sha for filename, sha in members.items()
        if Path(filename).name == result_pin.filename
    ]
    if matches != [result_pin.sha256]:
        raise ProductionBlocked("manifest/result binding mismatch: " + label)


def _legacy_semantic_snapshot(documents: dict[str, Any]) -> dict[str, Any]:
    af2 = documents["AF2_PRIMARY_RESULT"]
    b1 = documents["B1G0_RESULT"]
    i0 = documents["I0_RESULT"]
    i1 = documents["I1_RESULT"]
    i2 = documents["I2_RESULT"]
    i3 = documents["I3_RESULT"]
    i4 = documents["I4_RESULT"]
    if type(af2["formal_credit"]) is not int or af2["formal_credit"] != 0:
        raise ProductionBlocked("AF2 formal credit is nonzero or bool-aliased")
    if b1["audit"]["all_output_formal_credit_zero"] is not True:
        raise ProductionBlocked("B1G0 audit zero-credit marker")
    if b1["strict_boundary"]["all_output_formal_credit_zero"] is not True:
        raise ProductionBlocked("B1G0 boundary zero-credit marker")
    b1_credit_keys = (
        "formal_fibre_credit",
        "formal_full_support_credit",
        "formal_global_disposition_credit",
        "formal_graph_definition_credit",
        "formal_maximality_credit",
        "formal_physical_incidence_credit",
    )
    for key in b1_credit_keys:
        credit = b1["strict_boundary"][key]
        if type(credit) is not int or credit != 0:
            raise ProductionBlocked("B1G0 nonzero or aliased credit: " + key)
    for label, document in (
        ("I0", i0), ("I1", i1), ("I2", i2), ("I3", i3), ("I4", i4),
    ):
        _strict_zero_credit_map(document["formal_credit"], label)
    obligation_boundary = i4["semantic_boundary"][
        "theorem_obligation_census_824864_is_not_feature_ledger_row_count"
    ]
    if _strict_bool(obligation_boundary, "I4 obligation boundary") is not True:
        raise ProductionBlocked("I4 obligation boundary is false")
    return {
        "statuses": {
            "AF2": af2["status"],
            "B1G0": b1["status"],
            "I0": i0["status"],
            "I1": i1["status"],
            "I2": i2["status"],
            "I3": i3["status"],
            "I4": i4["status"],
        },
        "old_census": {
            "members": i4["exact_census"]["member_counts_by_family"],
            "representations": i4["exact_census"]["representation_counts_by_family"],
            "member_count": i4["exact_census"]["member_count"],
            "representation_count": i4["exact_census"]["representation_count"],
            "G2B_reference_count": i3["exact_census"]["G2b_references"],
            "B1G0_graph_count": b1["output_ledgers"]["graph"]["row_count"],
            "B1G0_sheet_count": b1["output_ledgers"]["sheet"]["row_count"],
            "B1G0_side_reference_count": b1["output_ledgers"]["side"]["row_count"],
            "B1G0_distinct_member_backbinding_count": b1["output_ledgers"]["member"]["row_count"],
            "B1G0_physical_incidence_reference_count": b1["audit"]["physical_incidence_count"],
            "B1G0_gap_count": b1["output_ledgers"]["gap"]["row_count"],
            "theorem_obligation_census_not_feature_rows": 824_864,
        },
        "lane_receipts": {
            "R292_members": i0["exact_census"]["R292_member_count"],
            "R292_representations": i0["exact_census"]["R292_uncovered_representation_cell_count"],
            "R2_cells": i1["exact_census"]["R2_predicate_source_cell_count"],
            "R2_members": i1["exact_census"]["R2_member_count"],
            "R2_representations": i1["exact_census"]["R2_representation_count"],
            "preserved_non_graph_members": i2["exact_census"]["member_count"],
            "preserved_non_graph_representations": i2["exact_census"]["representation_candidate_count"],
            "G2_distinct_members": i3["exact_census"]["G2_distinct_members"],
        },
        "AF2_primary_independent_byte_identical": True,
        "all_legacy_formal_credit_is_nonpromoting": True,
    }


EXPECTED_LEGACY_STATUSES: Final = {
    "AF2": "PASS_EXACT_564492_MEMBER_SOURCE_PARTITION__FORMAL_FULL_SUPPORT_NO_GO",
    "B1G0": "PRIVATE_ZERO_CREDIT_GRAPH_SOURCE_INVENTORY_AND_JOIN_FREEZE_CANDIDATE",
    "I0": "PASS_PARTIAL_R292_IDENTITY_OWNER_INDEX__ZERO_THEOREM_CREDIT__FIVE_FAMILIES_PENDING",
    "I1": "PASS_EXACT_R2_MECHANICAL_IDENTITY_REPRESENTATION_INDEX__ZERO_THEOREM_CREDIT",
    "I2": "PASS_MECHANICAL_144296_MEMBER_183572_REPRESENTATION_INDEX__ZERO_THEOREM_CREDIT",
    "I3": "PASS_G2_MECHANICAL_IDENTITY_REPRESENTATION_INDEX__SEMANTIC_GAPS_NONZERO__ZERO_FORMAL_CREDIT",
    "I4": "PASS_EXACT_GLOBAL_SIX_FAMILY_MECHANICAL_IDENTITY_REPRESENTATION_CENSUS__ZERO_THEOREM_CREDIT",
}


def audit_legacy_boundary_read_only() -> dict[str, Any]:
    data = Path(__file__).resolve(strict=True).parent
    pins_by_role = {pin.role: pin for pin in LEGACY_AUDIT_PINS}
    if len(pins_by_role) != len(LEGACY_AUDIT_PINS):
        raise ProductionBlocked("duplicate legacy pin role")
    if len({pin.filename for pin in LEGACY_AUDIT_PINS}) != len(LEGACY_AUDIT_PINS):
        raise ProductionBlocked("duplicate legacy pin filename")

    first: dict[str, tuple[bytes, tuple[int, ...]]] = {}
    for pin in LEGACY_AUDIT_PINS:
        raw, identity = _held_fd_read(data / pin.filename)
        if len(raw) != pin.size or hashlib.sha256(raw).hexdigest() != pin.sha256:
            raise ProductionBlocked("legacy frozen pin mismatch: " + pin.role)
        first[pin.role] = (raw, identity)

    for pin in reversed(LEGACY_AUDIT_PINS):
        raw, identity = _held_fd_read(data / pin.filename)
        if first[pin.role] != (raw, identity):
            raise ProductionBlocked("legacy two-pass pin mismatch: " + pin.role)

    # Final all-path identity pass catches a late mutation of an early pin.
    for pin in LEGACY_AUDIT_PINS:
        current = (data / pin.filename).stat(follow_symlinks=False)
        if _file_identity(current) != first[pin.role][1]:
            raise ProductionBlocked("late first-pin replacement: " + pin.role)

    documents: dict[str, Any] = {}
    for role in (
        "AF2_PRIMARY_RESULT", "AF2_INDEPENDENT_RESULT", "B1G0_RESULT",
        "I0_RESULT", "I1_RESULT", "I2_RESULT", "I3_RESULT", "I4_RESULT",
    ):
        documents[role] = strict_canonical_json(first[role][0], role)
    if first["AF2_PRIMARY_RESULT"][0] != first["AF2_INDEPENDENT_RESULT"][0]:
        raise ProductionBlocked("AF2 primary/independent result byte mismatch")

    manifest_receipts: dict[str, Any] = {}
    for role, expectation in LEGACY_MANIFEST_EXPECTATIONS.items():
        members = _parse_manifest(
            first[role][0], role, _strict_int(expectation["line_count"], role)
        )
        result_role = expectation["result_role"]
        if type(result_role) is not str:
            raise ProductionBlocked("manifest result role type")
        _manifest_contains_result(members, pins_by_role[result_role], role)
        manifest_receipts[role] = {
            "member_count": len(members),
            "manifest_sha256": pins_by_role[role].sha256,
            "result_role": result_role,
            "result_sha256": pins_by_role[result_role].sha256,
        }

    snapshot = _legacy_semantic_snapshot(documents)
    if not _same_typed(snapshot["statuses"], EXPECTED_LEGACY_STATUSES):
        raise ProductionBlocked("legacy status boundary mismatch")
    if not _same_typed(snapshot["old_census"], OLD_AUDIT_CENSUS):
        raise ProductionBlocked("legacy census boundary mismatch")

    return {
        "status": "PASS_READ_ONLY_LEGACY_MIGRATION_BOUNDARY_AUDIT",
        "pin_count": len(LEGACY_AUDIT_PINS),
        "total_bytes": sum(pin.size for pin in LEGACY_AUDIT_PINS),
        "two_pass_held_fd_and_final_all_path_revalidation": True,
        "manifest_receipts": manifest_receipts,
        "semantic_snapshot": snapshot,
        "producer_or_verifier_imported_or_executed": False,
        "authority_granted_to_legacy_derived_rows": False,
    }


def _post_decode_row_cap(rows: list[bytes]) -> None:
    for index, row in enumerate(rows):
        if len(row) > MAX_DECODED_ROW_BYTES:
            raise ProductionBlocked(f"decoded row {index} exceeds final 8MiB cap")


def _decode_single_gzip_member_test_only(blob: bytes) -> list[bytes]:
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        decoded = decoder.decompress(blob) + decoder.flush()
    except zlib.error as exc:
        raise ProductionBlocked("gzip decode") from exc
    if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise ProductionBlocked("second gzip member or trailing bytes")
    if not decoded.endswith(b"\n"):
        raise ProductionBlocked("JSONL final LF missing")
    rows = decoded[:-1].split(b"\n")
    _post_decode_row_cap(rows)
    return rows


def _bound_result_digest(canonical_input: Any, result: Any) -> str:
    return digest({
        "domain": SCHEMA + ".input-bound-result-digest.v1",
        "canonical_input": canonical_input,
        "result": result,
    })


def _fixed_spill_root_ignoring_tmpdir(tmpdir_value: str, deliverables: Path) -> str:
    if type(tmpdir_value) is not str:
        raise ProductionBlocked("TMPDIR type")
    fixed = os.path.abspath(FIXED_EXTERNAL_SPILL_ROOT)
    parent = os.path.abspath(os.fspath(deliverables))
    if os.path.commonpath((fixed, parent)) == parent:
        raise ProductionBlocked("fixed spill root lies inside deliverables")
    return fixed


def _validate_final_pin_vector(
    pins: tuple[FrozenPin, ...], required_roles: tuple[str, ...], label: str
) -> None:
    roles = tuple(pin.role for pin in pins)
    if roles != required_roles:
        raise ProductionBlocked(label + " complete role vector absent")
    if len({pin.filename for pin in pins}) != len(pins):
        raise ProductionBlocked(label + " duplicate filename")
    for pin in pins:
        if type(pin.role) is not str or type(pin.filename) is not str:
            raise ProductionBlocked(label + " non-string frozen pin field")
        candidate = Path(pin.filename)
        if (
            not pin.filename
            or candidate.is_absolute()
            or ".." in candidate.parts
            or candidate.name != pin.filename
        ):
            raise ProductionBlocked(label + " unsafe frozen pin filename")
        if (
            type(pin.size) is not int
            or pin.size <= 0
            or type(pin.sha256) is not str
            or re.fullmatch(r"[0-9a-f]{64}", pin.sha256) is None
        ):
            raise ProductionBlocked(label + " malformed frozen pin")


def assert_production_ready_before_candidate_path_access() -> None:
    _validate_final_pin_vector(R235D_FINAL_PINS, R235D_REQUIRED_ROLES, "R235D")
    _validate_final_pin_vector(C0_FINAL_PINS, C0_REQUIRED_ROLES, "C0")
    raise ProductionBlocked(
        "R235D/C0 pins exist but the full C1 producer has not replaced the skeleton"
    )


def production_entry(candidate_path: Any) -> None:
    # This call must precede os.fspath/exists/stat/resolve/mkdir/open.
    assert_production_ready_before_candidate_path_access()
    os.fspath(candidate_path)  # pragma: no cover - deliberately unreachable


def _corrected_census_self_check(
    corrected_census: Any = None,
    c0_expectation: Any = None,
    obligation_census: Any = None,
    component_rebind: Any = None,
) -> dict[str, Any]:
    corrected_census = CORRECTED_CENSUS if corrected_census is None else corrected_census
    c0_expectation = C0_MIGRATION_EXPECTATION if c0_expectation is None else c0_expectation
    obligation_census = (
        CORRECTED_OBLIGATION_CENSUS if obligation_census is None else obligation_census
    )
    component_rebind = FRESH_COMPONENT_REBIND if component_rebind is None else component_rebind
    expected_corrected = {
        "members": {
            "PRESERVED": 126_468, "NON_GRAPH": 17_828, "R2": 295_336,
            "R292": 9_404, "G2A": 38_608, "G2B": 76_816,
        },
        "representations": {
            "PRESERVED": 165_744, "NON_GRAPH": 17_828, "R2": 302_624,
            "R292": 10_252, "G2A": 38_608, "G2B": 76_816,
        },
        "member_count": 564_460,
        "representation_count": 611_872,
        "fresh_component_count": 92_672,
        "G2A_graph_and_sheet_count": 38_608,
        "G2B_reference_count": 76_816,
        "G2B_distinct_member_count": 76_816,
        "G2B_duplicate_reference_excess": 0,
        "physical_incidence_reference_count": 115_424,
        "B1G0_member_backbinding_count": 115_424,
        "B1G0_gap_count": 154_032,
    }
    expected_c0 = {
        "status": "EXPECTED_FROM_FINAL_C0__MUST_BE_RECOMPUTED_AND_PINNED_BEFORE_C1_PRODUCTION",
        "member_count": 564_460,
        "base_root_count": 367_948,
        "legal_edge_application_count": 478_718,
        "fresh_component_count": 92_672,
        "corrected_partition_sha256": "1ae914d4e2cff22d1fa6ddad4ffe4679c594bde3cdad27acf1480202b7a89434",
        "cross_component_pair_denominator": 158_820_108_554,
        "C1_minted_any_of_these_facts": False,
    }
    expected_obligation = {
        "status": "EXACT_THEOREM_OBLIGATION_CENSUS_ONLY__NOT_FEATURE_LEDGER_ROWS",
        "superseded_old_total": 824_864,
        "root": {
            "preserved_non_graph_A1_A2": 17_940,
            "R2_predicate_cells": 295_340,
            "G2_graph_definitions": 38_608,
            "total": 351_888,
        },
        "dependent": {
            "preserved_non_graph_A1_A2": 62_152,
            "R2_member_pullbacks": 295_336,
            "G2_graph_sheet_identifications": 38_608,
            "G2_graph_side_incidences": 76_816,
            "total": 472_912,
        },
        "corrected_total": 824_800,
        "old_to_corrected_decrease": 64,
        "known_final_feature_ledger_row_count": None,
    }
    expected_rebind = {
        "scope": "SURVIVORS_IN_FOUR_REKEYED_OLD_COMPONENTS_ONLY",
        "member_count": 21_848,
        "members_by_family": {
            "PRESERVED": 14_400, "NON_GRAPH": 1_776, "R2": 800,
            "R292": 3_776, "G2A": 584, "G2B": 512,
        },
        "old_component_ids_are_provenance_only": True,
        "all_564460_member_rows_bind_fresh_C0_component_ids": True,
    }
    for actual, expected, label in (
        (corrected_census, expected_corrected, "corrected census"),
        (c0_expectation, expected_c0, "C0 migration expectation"),
        (obligation_census, expected_obligation, "obligation census"),
        (component_rebind, expected_rebind, "component rebind"),
    ):
        if not _same_typed(actual, expected):
            raise AssertionError(label + " exact type-strict mismatch")
    member_sum = sum(
        _strict_int(value, "corrected member family count")
        for value in corrected_census["members"].values()
    )
    representation_sum = sum(
        _strict_int(value, "corrected representation family count")
        for value in corrected_census["representations"].values()
    )
    rebind_sum = sum(
        _strict_int(value, "fresh component rebind family count")
        for value in component_rebind["members_by_family"].values()
    )
    root = obligation_census["root"]
    dependent = obligation_census["dependent"]
    if member_sum != 564_460 or representation_sum != 611_872:
        raise AssertionError("corrected six-family sum")
    if type(corrected_census["fresh_component_count"]) is not int or corrected_census["fresh_component_count"] != 92_672:
        raise AssertionError("fresh C0 component count")
    if corrected_census["G2A_graph_and_sheet_count"] + corrected_census["G2B_reference_count"] != corrected_census["physical_incidence_reference_count"]:
        raise AssertionError("corrected physical incidence equation")
    if 2 * corrected_census["G2A_graph_and_sheet_count"] + corrected_census["G2B_reference_count"] != corrected_census["B1G0_gap_count"]:
        raise AssertionError("corrected gap equation")
    if rebind_sum != 21_848:
        raise AssertionError("affected component rebind equation")
    if (
        root["preserved_non_graph_A1_A2"]
        + root["R2_predicate_cells"]
        + root["G2_graph_definitions"]
        != root["total"]
    ):
        raise AssertionError("root obligation equation")
    if (
        dependent["preserved_non_graph_A1_A2"]
        + dependent["R2_member_pullbacks"]
        + dependent["G2_graph_sheet_identifications"]
        + dependent["G2_graph_side_incidences"]
        != dependent["total"]
    ):
        raise AssertionError("dependent obligation equation")
    if root["total"] + dependent["total"] != 824_800:
        raise AssertionError("corrected obligation total")
    return {
        "member_sum": member_sum,
        "representation_sum": representation_sum,
        "fresh_component_count": 92_672,
        "base_root_count": c0_expectation["base_root_count"],
        "legal_edge_application_count": c0_expectation["legal_edge_application_count"],
        "corrected_partition_sha256": c0_expectation["corrected_partition_sha256"],
        "cross_component_pair_denominator": c0_expectation["cross_component_pair_denominator"],
        "physical_incidence_sum": 115_424,
        "gap_sum": 154_032,
        "affected_component_rebind_sum": rebind_sum,
        "obligation_sum": 824_800,
    }


def contract(legacy_audit: dict[str, Any] | None = None) -> dict[str, Any]:
    _require_isolated_runtime()
    if legacy_audit is None:
        legacy_audit = audit_legacy_boundary_read_only()
    payload = {
        "schema": SCHEMA + ".contract.v1",
        "status": "HARD_NO_PRODUCTION_PENDING_INDEPENDENTLY_VERIFIABLE_C1_IMPLEMENTATION",
        "production_ready": False,
        "scope": "CORRECTED_POST_C0_IDENTITY_REPRESENTATION_INCIDENCE_GAP_AND_COMPONENT_REBIND_REPLAY_CONTRACT_ONLY",
        "authority_priority": [
            {
                "priority": 1,
                "authority": "FINAL_R235D_SOURCE_ONLY_THEOREM_AND_EXACT_32_MEMBER_INVALIDATION",
                "controls": "EXCLUSION_AND_SOURCE_ONLY_SEMANTICS",
            },
            {
                "priority": 2,
                "authority": "FINAL_ROUND306C0_FRESH_MEMBER_ROOT_EDGE_AND_COMPONENT_FREEZE",
                "controls": "EXACT_564460_SURVIVOR_UNIVERSE_AND_ONLY_VALID_COMPONENT_IDS",
            },
            {
                "priority": 3,
                "authority": "FRESHLY_PINNED_PRIMITIVE_CONSTRUCTION_SOURCE_ROWS_AND_SEMANTIC_THEOREM_PACKAGES",
                "controls": "TYPED_SUPPORT_AST_REPRESENTATION_PULLBACK_AND_PHYSICAL_INCIDENCE",
            },
            {
                "priority": 4,
                "authority": "FRESH_C1_FAMILY_REPLAYS_THEN_FRESH_GLOBAL_MERGE",
                "controls": "NEW_ROWS_NEW_COMMITMENTS_AND_NEW_TRANSITION_HANDLES",
            },
            {
                "priority": 5,
                "authority": "LEGACY_AF2_B1G0_K2I0_TO_K2I4_MIGRATION_REFERENCE_ONLY",
                "controls": "SCHEMA_AND_DELTA_AUDIT_ONLY__ZERO_FORMAL_AUTHORITY",
            },
        ],
        "r235d_required_roles": list(R235D_REQUIRED_ROLES),
        "r235d_final_pins": [asdict(pin) for pin in R235D_FINAL_PINS],
        "c0_required_roles": list(C0_REQUIRED_ROLES),
        "c0_final_pins": [asdict(pin) for pin in C0_FINAL_PINS],
        "candidate_gate": {
            "candidate_path_access_before_complete_upstream_seals": False,
            "candidate_path_operations_forbidden_before_gate": [
                "os.fspath", "exists", "stat", "resolve", "mkdir", "open",
            ],
            "complete_R235D_and_C0_seals_are_now_pinned": True,
            "skeleton_remains_blocked_until_implementation_replaces_it": True,
        },
        "legacy_boundary": {
            "pins": [asdict(pin) for pin in LEGACY_AUDIT_PINS],
            "audit": legacy_audit,
            "old_census": OLD_AUDIT_CENSUS,
            "old_component_ids_have_formal_authority": False,
            "old_I0_I1_I2_I3_I4_derived_rows_have_formal_authority": False,
            "old_rows_may_only_appear_as_explicit_provenance": True,
            "old_row_bytes_or_row_ids_may_not_be_copied_into_C1": True,
            "explicitly_superseded": [
                "AF2_OLD_564492_MEMBER_PARTITION_STREAM_AND_CENSUS",
                "B1G0_OLD_B0_BACKBINDINGS_GRAPH_SHEET_SIDE_GAP_AND_RESULT_CENSUS",
                "K2I0_OLD_COMPONENT_BOUND_R292_ROWS",
                "K2I1_OLD_COMPONENT_BOUND_R2_ROWS",
                "K2I2_OLD_COMPONENT_BOUND_PRESERVED_NON_GRAPH_ROWS",
                "K2I3_OLD_G2_ROWS_HANDLES_GAPS_AND_COMPONENT_BINDINGS",
                "K2I4_OLD_GLOBAL_MEMBER_REPRESENTATION_HANDLE_GAP_AND_FAMILY_ROWS",
            ],
        },
        "corrected_census": CORRECTED_CENSUS,
        "c0_migration_expectation_not_C1_minted": C0_MIGRATION_EXPECTATION,
        "corrected_obligation_census": CORRECTED_OBLIGATION_CENSUS,
        "fresh_component_rebind": FRESH_COMPONENT_REBIND,
        "component_contract": {
            "namespace": CORRECTED_COMPONENT_NAMESPACE,
            "every_member_row_binds_a_fresh_C0_member_component_row": True,
            "affected_21848_rebind_rows_are_an_additional_closed_subset": True,
            "old_component_id_is_never_an_output_identity_or_routing_key": True,
        },
        "row_namespace": ROW_NAMESPACE,
        "outputs": OUTPUTS,
        "output_row_counts": {
            "family_census": 6,
            "member": 564_460,
            "representation": 611_872,
            "physical_incidence": 115_424,
            "gap": 154_032,
            "component_rebind": 21_848,
            "transition_handle": 564_460,
            "obligation_census_is_single_document_not_feature_rows": True,
        },
        "row_schemas": ROW_SCHEMAS,
        "row_fields": {key: list(value) for key, value in ROW_FIELDS.items()},
        "type_rules": TYPE_RULES,
        "semantic_boundary": {
            "mechanical_replay_does_not_mint_normalized_support_credit": True,
            "physical_incidence_statement_row_is_not_a_theorem": True,
            "gap_rows_are_exact_pending_obligations_not_credit": True,
            "transition_syntax_ready_is_not_transition_semantics_ready": True,
            "outer_envelope_or_inner_witness_cannot_stand_for_full_support": True,
            "theorem_obligation_census_824800_is_not_feature_ledger_rows": True,
            "normalized_support_credit": 0,
            "representation_cover_credit": 0,
            "A1_A2_credit": 0,
            "B1A_credit": 0,
            "B2_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "publication_contract": {
            "required_python_flags": "-I -B",
            "python_runtime_requires_isolated_mode": True,
            "python_runtime_requires_dont_write_bytecode": True,
            "strict_canonical_JSON_and_exact_field_sets": True,
            "duplicate_keys_floats_nonfinite_and_bool_int_alias_rejected": True,
            "single_gzip_member_no_trailing_bytes": True,
            "decoded_row_cap_enforced_after_final_decode_bytes": MAX_DECODED_ROW_BYTES,
            "two_pass_held_FD_hash_and_final_all_path_identity_revalidation": True,
            "symlink_and_hardlink_fail_close": True,
            "fixed_external_spill_root": FIXED_EXTERNAL_SPILL_ROOT,
            "TMPDIR_ignored": True,
            "spill_parent_must_be_held_FD_verified_outside_deliverables": True,
            "two_distinct_hash_seeds_produce_byte_identical_candidates": True,
            "seed_is_not_serialized_and_does_not_affect_order_or_ids": True,
            "independent_verifier_does_not_import_or_execute_producer": True,
            "independent_verifier_has_its_own_static_upstream_and_producer_pins": True,
            "every_result_digest_binds_full_canonical_input_and_result": True,
            "all_gap_missing_orphan_duplicate_overlap_counters_are_exact": True,
            "result_committed_last_without_clobber": True,
            "default_contract_self_test_and_failed_preflight_are_no_write": True,
        },
        "required_attacks": list(REQUIRED_ATTACKS),
        "attack_matrix": [
            {"attack_id": attack_id, "mutation": mutation, "expected": expected}
            for attack_id, mutation, expected in ATTACK_MATRIX
        ],
        "attack_matrix_sha256": digest(ATTACK_MATRIX),
    }
    return {**payload, "contract_sha256": digest(payload)}


def _contract_self_check(document: Any) -> dict[str, Any]:
    if type(document) is not dict:
        raise AssertionError("contract document type")
    payload = dict(document)
    claimed_digest = payload.pop("contract_sha256", None)
    if (
        type(claimed_digest) is not str
        or re.fullmatch(r"[0-9a-f]{64}", claimed_digest) is None
        or claimed_digest != digest(payload)
    ):
        raise AssertionError("contract digest closure")
    if document["production_ready"] is not False:
        raise AssertionError("production readiness must be strict false")
    if not _same_typed(document["r235d_required_roles"], list(R235D_REQUIRED_ROLES)):
        raise AssertionError("R235D required role vector")
    if not _same_typed(document["c0_required_roles"], list(C0_REQUIRED_ROLES)):
        raise AssertionError("C0 required role vector")
    if not _same_typed(document["r235d_final_pins"], [asdict(pin) for pin in R235D_FINAL_PINS]):
        raise AssertionError("R235D complete pin vector")
    if not _same_typed(document["c0_final_pins"], [asdict(pin) for pin in C0_FINAL_PINS]):
        raise AssertionError("C0 complete pin vector")
    expected_supersession = [
        "AF2_OLD_564492_MEMBER_PARTITION_STREAM_AND_CENSUS",
        "B1G0_OLD_B0_BACKBINDINGS_GRAPH_SHEET_SIDE_GAP_AND_RESULT_CENSUS",
        "K2I0_OLD_COMPONENT_BOUND_R292_ROWS",
        "K2I1_OLD_COMPONENT_BOUND_R2_ROWS",
        "K2I2_OLD_COMPONENT_BOUND_PRESERVED_NON_GRAPH_ROWS",
        "K2I3_OLD_G2_ROWS_HANDLES_GAPS_AND_COMPONENT_BINDINGS",
        "K2I4_OLD_GLOBAL_MEMBER_REPRESENTATION_HANDLE_GAP_AND_FAMILY_ROWS",
    ]
    if not _same_typed(
        document["legacy_boundary"]["explicitly_superseded"],
        expected_supersession,
    ):
        raise AssertionError("legacy supersession vector")
    expected_semantic_boundary = {
        "mechanical_replay_does_not_mint_normalized_support_credit": True,
        "physical_incidence_statement_row_is_not_a_theorem": True,
        "gap_rows_are_exact_pending_obligations_not_credit": True,
        "transition_syntax_ready_is_not_transition_semantics_ready": True,
        "outer_envelope_or_inner_witness_cannot_stand_for_full_support": True,
        "theorem_obligation_census_824800_is_not_feature_ledger_rows": True,
        "normalized_support_credit": 0,
        "representation_cover_credit": 0,
        "A1_A2_credit": 0,
        "B1A_credit": 0,
        "B2_credit": 0,
        "maximality_credit": 0,
        "fibre_credit": 0,
        "global_disposition_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    if not _same_typed(document["semantic_boundary"], expected_semantic_boundary):
        raise AssertionError("semantic boundary exact type-strict mismatch")
    expected_output_counts = {
        "family_census": 6,
        "member": 564_460,
        "representation": 611_872,
        "physical_incidence": 115_424,
        "gap": 154_032,
        "component_rebind": 21_848,
        "transition_handle": 564_460,
        "obligation_census_is_single_document_not_feature_rows": True,
    }
    if not _same_typed(document["output_row_counts"], expected_output_counts):
        raise AssertionError("output row counts exact type-strict mismatch")
    runtime_contract = document["publication_contract"]
    if runtime_contract["required_python_flags"] != "-I -B":
        raise AssertionError("required Python flags")
    if runtime_contract["python_runtime_requires_isolated_mode"] is not True:
        raise AssertionError("isolated runtime contract")
    if runtime_contract["python_runtime_requires_dont_write_bytecode"] is not True:
        raise AssertionError("no-bytecode runtime contract")
    zero_credit_keys = (
        "normalized_support_credit",
        "representation_cover_credit",
        "A1_A2_credit",
        "B1A_credit",
        "B2_credit",
        "maximality_credit",
        "fibre_credit",
        "global_disposition_credit",
    )
    for key in zero_credit_keys:
        value = document["semantic_boundary"][key]
        if type(value) is not int or value != 0:
            raise AssertionError("nonzero or aliased contract credit: " + key)
    return {
        "contract_digest_closed": True,
        "empty_upstream_pin_vectors": True,
        "legacy_supersession_count": len(expected_supersession),
        "strict_zero_credit_field_count": len(zero_credit_keys),
        "isolated_no_bytecode_runtime_required": True,
    }


def _coherent_mutation_regression_self_check() -> dict[str, str]:
    base = {
        "corrected": CORRECTED_CENSUS,
        "c0": C0_MIGRATION_EXPECTATION,
        "obligation": CORRECTED_OBLIGATION_CENSUS,
        "rebind": FRESH_COMPONENT_REBIND,
    }
    mutations = (
        ("physical_count_bool_alias", "corrected", ("physical_incidence_reference_count",), True),
        ("gap_wrong_count", "corrected", ("B1G0_gap_count",), 154_033),
        ("member_count_bool_alias", "corrected", ("member_count",), True),
        ("restore_old_G2A_count", "corrected", ("members", "G2A"), 38_624),
        ("base_root_wrong_count", "c0", ("base_root_count",), 0),
        ("partition_wrong_sha", "c0", ("corrected_partition_sha256",), "0" * 64),
        ("cross_wrong_count", "c0", ("cross_component_pair_denominator",), 0),
        ("C1_minted_bool_int_alias", "c0", ("C1_minted_any_of_these_facts",), 0),
        ("obligation_restore_old_total", "obligation", ("corrected_total",), 824_864),
        ("rebind_member_wrong_count", "rebind", ("member_count",), 0),
    )
    results: dict[str, str] = {}
    for name, section, path, replacement in mutations:
        candidate = json.loads(ENCODER.encode(base))
        cursor = candidate[section]
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
        try:
            _corrected_census_self_check(
                candidate["corrected"],
                candidate["c0"],
                candidate["obligation"],
                candidate["rebind"],
            )
        except (AssertionError, ProductionBlocked):
            results[name] = "REJECT"
        else:
            raise AssertionError("coherent mutation accepted: " + name)
    return results


class _BombCandidatePath:
    def __fspath__(self) -> str:
        raise AssertionError("candidate path was touched before the hard gate")


def self_test() -> dict[str, Any]:
    _require_isolated_runtime()
    blocked_prepath = False
    try:
        production_entry(_BombCandidatePath())
    except ProductionBlocked:
        blocked_prepath = True
    if not blocked_prepath:
        raise AssertionError("candidate path gate did not block")

    legacy_audit = audit_legacy_boundary_read_only()
    census = _corrected_census_self_check()

    strict_mutations_rejected = 0
    for raw in (b'{"x":1,"x":2}', b'{"x":1.0}', b'{"x":NaN}', b'{ "x":1}'):
        try:
            strict_canonical_json(raw, "mutation")
        except ProductionBlocked:
            strict_mutations_rejected += 1
    if strict_mutations_rejected != 4:
        raise AssertionError("strict JSON mutation count")

    alias_rejections = 0
    for function, value in ((_strict_int, True), (_strict_bool, 0)):
        try:
            function(value, "alias mutation")
        except ProductionBlocked:
            alias_rejections += 1
    if alias_rejections != 2:
        raise AssertionError("bool/int aliases")

    good_gzip = gzip.compress(b'{"x":1}\n', mtime=0)
    if _decode_single_gzip_member_test_only(good_gzip) != [b'{"x":1}']:
        raise AssertionError("single gzip member")
    concatenated_rejected = False
    try:
        _decode_single_gzip_member_test_only(good_gzip + good_gzip)
    except ProductionBlocked:
        concatenated_rejected = True
    row_cap_rejected = False
    try:
        _post_decode_row_cap([b"x" * (MAX_DECODED_ROW_BYTES + 1)])
    except ProductionBlocked:
        row_cap_rejected = True
    if not (concatenated_rejected and row_cap_rejected):
        raise AssertionError("gzip or post-decode row cap")

    same_result = {"status": "PASS"}
    if _bound_result_digest({"owner": "a"}, same_result) == _bound_result_digest(
        {"owner": "b"}, same_result
    ):
        raise AssertionError("result digest failed to bind its input")

    deliverables = Path(__file__).resolve(strict=True).parent
    spill = _fixed_spill_root_ignoring_tmpdir(os.fspath(deliverables), deliverables)
    if spill != FIXED_EXTERNAL_SPILL_ROOT:
        raise AssertionError("TMPDIR influenced fixed spill root")

    document = contract(legacy_audit)
    contract_checks = _contract_self_check(document)
    coherent_mutations = _coherent_mutation_regression_self_check()
    seed_zero = canonical_bytes(document)
    seed_other = canonical_bytes(document)
    if seed_zero != seed_other or document["production_ready"] is not False:
        raise AssertionError("seed independence or readiness")
    if (
        _same_typed(True, 1)
        or _same_typed(False, 0)
        or _same_typed({1: "value"}, {True: "value"})
    ):
        raise AssertionError("recursive bool/int alias")

    return {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS_HARD_NO_PRODUCTION_NO_WRITE_C1_CONTRACT_SELF_TEST",
        "python_runtime_isolated": sys.flags.isolated == 1,
        "python_runtime_dont_write_bytecode": sys.dont_write_bytecode is True,
        "production_gate_blocked_before_candidate_path_access": True,
        "filesystem_write_attempted": False,
        "legacy_boundary_audit": legacy_audit,
        "corrected_census_equations": census,
        "contract_invariants": contract_checks,
        "coherent_mutation_regressions": coherent_mutations,
        "strict_JSON_mutations_rejected": strict_mutations_rejected,
        "bool_int_alias_mutations_rejected": alias_rejections,
        "single_gzip_member_accepted": True,
        "concatenated_gzip_rejected": concatenated_rejected,
        "post_decode_8MiB_row_cap_rejected": row_cap_rejected,
        "input_bound_result_digest_distinguishes_equal_results": True,
        "TMPDIR_ignored_and_fixed_spill_root_lexically_outside_deliverables": True,
        "spill_parent_held_FD_boundary_is_a_future_producer_requirement": True,
        "two_seed_contract_bytes_identical": True,
        "attack_matrix_case_count": len(ATTACK_MATRIX),
        "attack_matrix_sha256": digest(ATTACK_MATRIX),
        "contract_sha256": document["contract_sha256"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--candidate-dir")
    return parser.parse_args()


def main() -> int:
    _require_isolated_runtime()
    args = parse_args()
    if type(args.seed) is not int or not 0 <= args.seed < 2**63:
        raise SystemExit("seed must be an integer in [0, 2**63)")
    if args.candidate_dir is not None:
        # Deliberately before os.fspath/exists/stat/resolve/mkdir/open.
        production_entry(args.candidate_dir)
    if args.self_test:
        print(ENCODER.encode(self_test()))
        return 0
    print(ENCODER.encode(contract()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
