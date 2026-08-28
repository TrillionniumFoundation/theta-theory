#!/usr/bin/env python3
"""Round306B1AF3 full-support construction-source authority freeze.

This document freezes only the authority frontier that a later formal B1A
full-feature-cover construction must consume.  It does not construct a
normalized support, does not define an analytic AST, and grants no theorem,
incidence, transition, routing, maximality, fibre, or CM2 credit.

The contract is intentionally UNSEALED until two independently implemented
read-only replays and their byte-identical canonical results have exact
filename/size/SHA-256 pins below.  Candidate and production entry points are
permanently blocked before every filesystem, subprocess, or output action.
"""

from __future__ import annotations

import argparse
import builtins
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
from typing import Any, Callable, NoReturn
from unittest import mock


class ContractBlocked(RuntimeError):
    """Fail-closed contract, authority, evidence, or admission violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ContractBlocked(label)


SCHEMA = (
    "cm2.round306b1af3.source-g-full-support-construction-source-"
    "authority-frontier-freeze.v1"
)
REPLAY_RESULT_SCHEMA = (
    "cm2.round306b1af3.source-g-full-support-construction-source-"
    "authority-frontier.replay-result.v1"
)
UNSEALED_STATUS = (
    "UNSEALED_ZERO_CREDIT_AUTHORITY_FRONTIER_STRUCTURE__AWAITING_EXACT_"
    "PRIMARY_AND_INDEPENDENT_REPLAY_SOURCE_AND_RESULT_PINS"
)
SEALED_STATUS = (
    "PASS_ZERO_CREDIT_EXACT_FULL_SUPPORT_CONSTRUCTION_SOURCE_AUTHORITY_"
    "FRONTIER_FREEZE__ANALYTIC_AST_AND_FORMAL_B1A_BLOCKED"
)
CANDIDATE_BLOCK_REASON = (
    "Round306B1AF3 is a non-production zero-credit authority freeze; "
    "candidate mode is blocked before every filesystem or output action"
)
PRODUCTION_BLOCK_REASON = (
    "Round306B1AF3 does not authorize a production or formal package; "
    "production mode is blocked before every filesystem or output action"
)

HEX64 = re.compile(r"^[0-9a-f]{64}$")
ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=True,
    allow_nan=False,
)

MEMBER_COUNT = 564_492
REPRESENTATION_COUNT = 611_904
FEATURE_OBLIGATION_CENSUS = 824_864
REPLAY_ZERO_FORMAL_CREDIT: dict[str, Any] = {
    "normalized_full_support_members": 0,
    "normalized_full_support_denominator": 564_492,
    "representation_cover": 0,
    "representation_cover_denominator": 611_904,
    "formal_B1A": False,
    "transition_atlas_families": 0,
    "transition_atlas_denominator": 20,
    "known_edge_geometry_first_rediscovery": 0,
    "known_edge_geometry_first_denominator": 478_718,
    "pair_routing": 0,
    "pair_routing_denominator": 158_838_084_354,
    "component_maximality_credit": 0,
    "official_fibre_credit": 0,
    "source_G_disposition_credit": 0,
    "D02": "BLOCKED",
    "D03": "NOT_REACHED",
    "D04": "NOT_MINTED",
    "CM2": "NO-GO_FOR_CLAIM",
}
AUTHORITY_ROOT_COUNT = 36
TRANSITIVE_FILE_COUNT = 143
TRANSITIVE_FILE_BYTES = 3_201_364_049
INVENTORY_ROWS_SHA256 = (
    "40d971a646e59ffbc6854913c1c9dbc831253ba80d00451f79524fd371c8097a"
)
INVENTORY_HASH_DOMAIN: dict[str, Any] = {
    "catalog_domain": "36_ROOTS_UNION_RECURSIVE_EXACT_TOP_LEVEL_PINS_KEYS",
    "root_count": 36,
    "accepted_assignment_name": "PINS",
    "similarly_named_assignments_ignored": True,
    "all_PINS_key_file_types_enter_catalog": True,
    "only_dot_py_PINS_keys_are_recursed": True,
    "tuple_or_list_value_file_sha256_index": 0,
    "direct_string_value_is_file_sha256": True,
    "row_fields_exact": ["filename", "exact_size", "sha256", "root_source"],
    "root_source_semantics": "BOOLEAN_FILENAME_IS_MEMBER_OF_36_ROOTS",
    "row_order": "FILENAME_ASCII_ASCENDING",
    "canonical_json_sort_keys": True,
    "canonical_json_separators": [",", ":"],
    "canonical_json_ensure_ascii": True,
    "canonical_json_allow_nan": False,
    "final_LF": False,
}

# Governance anchors are pinned directly by exact basename, byte length, and
# SHA-256.  They constrain the lineage and zero-credit admission boundary, but
# they do not substitute for the 36-root/143-file authority-inventory replay
# and do not seal this AF3 contract.
GOVERNANCE_SEAL_PINS: tuple[tuple[str, str, int, str], ...] = (
    (
        "B0_MANIFEST",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256",
        1_760,
        "9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269",
    ),
    (
        "B0_RESULT",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json",
        9_450,
        "badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735",
    ),
    (
        "B0_VERIFICATION",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json",
        7_003,
        "f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590",
    ),
    (
        "B1R0_MANIFEST",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_manifest.sha256",
        1_571,
        "f23f4639629e920596e1ecadbb1cd7708f93308dc5780a0f82c196edc0f46aec",
    ),
    (
        "B1R0_RESULT",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_result.json",
        3_019,
        "ca66501d42894dce364ff905045ae69f67cf52c9142ba8f7b45973f857966f04",
    ),
    (
        "B1R0_VERIFICATION",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_verification.json",
        11_531,
        "2242732077165e085f6f2e50f2d061a532a3b43d9e9bc0efc17afac3d45df040",
    ),
    (
        "B1G0_MANIFEST",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256",
        1_959,
        "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8",
    ),
    (
        "B1G0_RESULT",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_result.json",
        5_006,
        "3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e",
    ),
    (
        "B1G0_VERIFICATION",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_verification.json",
        11_575,
        "65b7a01fd82535f357dbb44b8c68a68c86afcbb75b1c1c9b9159b71f9815139a",
    ),
    (
        "AF0_CONTRACT",
        "cm2_round306b1af0_source_g_formal_full_feature_cover_schema_contract.py",
        46_865,
        "d2edaf5247e90ad1e9344261e18b29612ed37b8d928bd1f715c5a6fab3a70e04",
    ),
    (
        "AF1_CONTRACT",
        "cm2_round306b1af1_source_g_formal_full_feature_cover_pre_schema_admission_contract.py",
        30_391,
        "93d35ed11c98b3721f8ec24ec8c440278e5e947b8f5e63a7dbdc4b1d66380e39",
    ),
    (
        "AF2_CONTRACT",
        "cm2_round306b1af2_source_g_primitive_support_source_partition_freeze_contract.py",
        52_538,
        "a91578a8bef1c4a72f940f7ebc71aea4c0ebc1ddac08ddbb3889a2da6cdd00f5",
    ),
    (
        "AF2_PRIMARY_REPLAY_SOURCE",
        "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_replay.py",
        20_783,
        "b7fcae488bd1e9e301f7191e65ade22f87c393a083a1335147ccf1bc92cddb27",
    ),
    (
        "AF2_PRIMARY_REPLAY_RESULT",
        "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_result.json",
        2_540,
        "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb",
    ),
    (
        "AF2_INDEPENDENT_REPLAY_SOURCE",
        "cm2_round306b1af2_source_g_primitive_support_source_partition_independent_replay.py",
        23_694,
        "38551c822f9aa74989b54749a3e05e8fe9bdce205fb12efb12eaa7382e6ccab4",
    ),
    (
        "AF2_INDEPENDENT_REPLAY_RESULT",
        "cm2_round306b1af2_source_g_primitive_support_source_partition_independent_result.json",
        2_540,
        "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb",
    ),
    (
        "OLD_B2C0_INERT_CONTRACT",
        "cm2_round306b2c0_source_g_feature_transition_pair_routing_contract.py",
        53_212,
        "6a4fbbc3c614b7adaf275d0870a0205360827ed9fe89b8e26748e966a04f4d69",
    ),
)
GOVERNANCE_SEAL_COUNT = 17
GOVERNANCE_SEAL_BYTES = 285_437

# Every byte source named by TABLE_AUTHORITIES is independently pinned here.
# This domain is deliberately separate from the 143-file transitive PINS
# catalog: several generated ledgers are authority inputs but are not members
# of that source-code dependency closure.
AUTHORITY_FILE_PINS: tuple[tuple[str, int, str], ...] = (
    ("cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json", 113_656_620, "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54"),
    ("cm2_round179_source_g_residual_tube_arrangement_rows.json", 131_273_924, "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"),
    ("cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json", 158_815_476, "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c"),
    ("cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json", 7_157_575, "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818"),
    ("cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json", 193_161_618, "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"),
    ("cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json", 140_690_802, "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"),
    ("cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json", 294_422_681, "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"),
    ("cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json", 3_596_500, "a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0"),
    ("cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    ("cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json", 67_765_471, "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"),
    ("cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", 2_061_199, "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    ("cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json", 346_302, "5fa46f8c6d8074770ebbf8cbdb2f0590dbdf5710254d05c6a0a3aca0953359f3"),
    ("cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json", 399_196, "8200ba9c35ba32c938eb66beb7a4040908db9b81fc449881a55b09e67b517446"),
    ("cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json", 13_734_655, "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e"),
    ("cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json", 95_999_515, "5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f"),
    ("cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json", 20_683_081, "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"),
    ("cm2_round246_source_g_whole_signature_retained_quotient_certificate.json", 18_283_721, "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9"),
    ("cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json", 13_400_149, "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7"),
    ("cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json", 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
    ("cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json", 406_539_851, "ac9e9451e12621fd236fea39bc686e13b41ade62e5255de9c9cd98230763236f"),
    ("cm2_round266_source_g_expanded_curved_face_closure_certificate.json", 934_776_249, "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf"),
    ("cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json", 319_672_585, "472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3"),
    ("cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json", 56_705_100, "72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea"),
    ("cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json", 112_741_715, "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747"),
    ("cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json", 1_250_159, "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2"),
    ("cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json", 35_517_526, "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386"),
    ("cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz", 112_858_007, "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe"),
    ("cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz", 92_749_868, "bc1b976c0609c3271690e3d52c9bae85571f1a7661f404d7bc2e65bb707a2695"),
    ("cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz", 7_529_109, "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a"),
    ("cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz", 134_114_861, "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a"),
    ("cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_existing_overlap_relations.json.gz", 7_237_078, "d76d27c436735511dc34056d9237a2772decd30129e3019b74c5a02a118ab24e"),
    ("cm2_round290_source_g_isolated_atom_inner_support_closure_inner_support_ledger.json.gz", 9_576_526, "9c2a596f3b981d24baa039e02c72e5270889d145dc146963532f3dedebc94025"),
    ("cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz", 5_544_437, "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab"),
    ("cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz", 262_951_902, "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb"),
    ("cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz", 26_672_326, "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833"),
    ("cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz", 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"),
    ("cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz", 32_731_854, "79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b"),
    ("cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz", 23_240_985, "2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809"),
    ("cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),
    ("cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),
    ("cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz", 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"),
    ("cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz", 140_958, "834b687845a156328873888e405793f52a12df9d6286ae07d8a572c6163a361a"),
    ("cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_gap.json.gz", 108_363_350, "c6b1de08fc62e39d5c5cfc2d98ba5b558d467e1592cc101c19ebdbc9fab66c56"),
    ("cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz", 123_019_951, "4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7"),
    ("cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz", 105_989_322, "19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96"),
)
AUTHORITY_FILE_COUNT = 45
AUTHORITY_FILE_BYTES = 4_665_362_689
AUTHORITY_FILE_CATALOG_SHA256 = (
    "13993a345ec98b14d84faf6db8d29c1f5e23dbfbc1ae47e44798adea931caa0a"
)
TABLE_AUTHORITY_COUNT = 82
TABLE_AUTHORITY_CATALOG_SHA256 = (
    "a49a38afbea65b5a8e837bc4932328447ad0ee553f18596cdff5ea788a879678"
)
AUTHORITY_ROLE_CATALOG_SHA256 = (
    "807e5502f5329577fc6f3c823bf835879c637f4b083fd417ff69e27cc3190117"
)

# These four exact pins close the previously UNSEALED replay-evidence gate.
# The two sources are distinct implementations; both exact CLI stdout result
# files are byte-identical canonical JSON with exactly one terminal LF.
REPLAY_EVIDENCE_PINS: tuple[tuple[str, str, int, str], ...] = (
    (
        "PRIMARY_REPLAY_SOURCE",
        "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_primary_replay.py",
        183_616,
        "aaa14995ef822be78cff1abe7ee7d0c4592f6fc98624b7ad664139b22af6dba2",
    ),
    (
        "PRIMARY_REPLAY_RESULT",
        "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_primary_replay_result.json",
        198_283,
        "5b9a4ba7920fb4fc98615fa9b69fb3dd6e4201ef76c4d2005fde6f85e777071f",
    ),
    (
        "INDEPENDENT_REPLAY_SOURCE",
        "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_independent_replay.py",
        213_098,
        "128d5e8b4689f041292ff2f342115b1cd583c5bc1d395cd9fda36eb4f2e33215",
    ),
    (
        "INDEPENDENT_REPLAY_RESULT",
        "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_independent_replay_result.json",
        198_283,
        "5b9a4ba7920fb4fc98615fa9b69fb3dd6e4201ef76c4d2005fde6f85e777071f",
    ),
)
EXPECTED_REPLAY_RESULT_SHA256: str | None = (
    "5b9a4ba7920fb4fc98615fa9b69fb3dd6e4201ef76c4d2005fde6f85e777071f"
)
EXPECTED_CONTRACT_SHA256: str | None = (
    "959c9e314e86585e73ad4bcb09a536f38d1d53b6ce8acfbcf2ebdc0cc00109d4"
)


COARSE_PARTITION = (
    ("direct_preserved_source_geometry", 126_468),
    ("R2_predicate_union_members", 295_336),
    ("R292_transformed_cell_union_members", 9_404),
    ("G2a_graph_sheet_members", 38_624),
    ("G2b_graph_side_members", 76_832),
    ("non_graph_virtual_bulk_members", 17_828),
)

FINE_PARTITION = (
    ("PRESERVED_ROUND174_RESOLVED", 72_500),
    ("PRESERVED_ROUND179_RESOLVED", 17_192),
    ("PRESERVED_ROUND204_REGION", 736),
    ("PRESERVED_ROUND208_REGION", 36_040),
    ("R288_DYNAMIC_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION", 274_176),
    ("R288_ISOLATED_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION", 21_160),
    ("R292_EXACT_T2PS_REFINEMENT_CELL_UNION", 9_404),
    ("R245_GRAPH_SHEET_REQUIRES_G2A_SUPPORT", 264),
    ("R248_GRAPH_SHEET_REQUIRES_G2A_SUPPORT", 38_360),
    ("R245_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT", 528),
    ("R248_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT", 76_304),
    ("R245_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION", 2_872),
    ("R246_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION", 2_220),
    ("R247_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION", 504),
    ("R248_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION", 12_232),
)


# row_count, row_ids_sha256, row_hashes_sha256, rows_sha256, ledger_sha256.
# None denotes an upstream whole-array commitment without closed row hashes.
TABLE_AUTHORITIES: tuple[
    tuple[str, str, str, str, int, str | None, str | None, str, str | None], ...
] = (
    # Lower coordinate/event lineage consumed by graph and non-graph sources.
    (
        "R182.collar_leaf_rows",
        "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json",
        ".result.collar_leaf_rows[]",
        "row_id (packed column 0)",
        202_840,
        None,
        None,
        "ced6d2764a7e1f5d404c1d56249e428f0754e53e7dded620e5904f9eb80b694c",
        None,
    ),
    (
        "R220.coordinate_corner_rows",
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json",
        ".result.coordinate_boundary_atlas.tables.coordinate_corner_rows.rows[]",
        "corner_id (packed column 0)",
        137_536,
        "032a80a350c671341ed4a231f92319fe6af3ccd48297f401170e789d6d0a9868",
        None,
        "226fb12c2c3f6ac1a59e4e6a2d9f32a2b257d33f6edcb229f81954e4506e8efd",
        None,
    ),
    (
        "R220.coordinate_edge_rows",
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json",
        ".result.coordinate_boundary_atlas.tables.coordinate_edge_rows.rows[]",
        "edge_id (packed column 0)",
        206_304,
        "7511a3ecb63328b0389bdc9eab0dd7fa2560f476c50d8b78c18d3410848c0408",
        None,
        "cfb3b2a341695b8b0a7d741931ca1494787dc3cfdec53031c59b23cb12c53977",
        None,
    ),
    (
        "R220.coordinate_face_rows",
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json",
        ".result.coordinate_boundary_atlas.tables.coordinate_face_rows.rows[]",
        "face_id (packed column 0)",
        103_152,
        "b6ac692bb13db5519a83c21d433159f124748cc32f1a85d550e8fd8a0f64a402",
        None,
        "9eb5d5eb90757d2a724302c1682929eacc6638bcd197aaac80fddd3f59207b34",
        None,
    ),
    (
        "R220.formal_coordinate_adjacency_rows",
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json",
        ".result.coordinate_boundary_atlas.tables.formal_coordinate_adjacency_rows.rows[]",
        "coordinate_adjacency_id (packed column 0)",
        10_384,
        "ab8fbea5baaac034b905d4ad2760519f87da25378cd8c2782015e8081ebd68cf",
        None,
        "dca8ddbb66b73ef615f1b1cd2c4b7ee453737ff18ed44e03e2ac222d5005d88f",
        None,
    ),
    (
        "R220.one_step_split_interface_rows",
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json",
        ".result.coordinate_boundary_atlas.tables.one_step_split_interface_rows.rows[]",
        "split_interface_id (packed column 0)",
        13_076,
        "6c907805c3980146287fd765fafa4f279c4ecedf19b314947b2e975b458c3297",
        None,
        "221b5568223c452c9c590157afd592dfdc0f244e1322c275d55263b747d18f57",
        None,
    ),
    (
        "R220.rejected_exact_coordinate_coincidence_rows",
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json",
        ".result.coordinate_boundary_atlas.tables.rejected_exact_coordinate_coincidence_rows.rows[]",
        "candidate_id (packed column 0)",
        9_830,
        "289f8995be84c457d8e55cb7d17313c4fa57dd65019d4cd85784018c8f03921a",
        None,
        "e61aae78e76404959074465e299a256e24c778d195d2902a452db8fed2d21092",
        None,
    ),
    (
        "R220.resolved_child_rows",
        "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json",
        ".result.coordinate_boundary_atlas.tables.resolved_child_rows.rows[]",
        "atlas_child_id (packed column 0)",
        17_192,
        "a966de2c22eabfcfe695ae3d66ee88b1908047e916f3345ea65c80be1b42edb1",
        None,
        "30d27f8d112331412a8db92e12acc69b2184b881a7ff1a256148ab335aa30ed2",
        None,
    ),
    (
        "R232.whole_origin_promotion_rows",
        "cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json",
        ".result.whole_origin_promotion_rows[]",
        "whole_origin_promotion_row_id",
        2_220,
        None,
        None,
        "65ff4166409729d6678e40b7435c137096bab158d8f41ce47c1588c0329f74ca",
        None,
    ),
    (
        "R234.root_summary_rows",
        "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json",
        ".result.root_summary_rows[]",
        "root_summary_id",
        2_640,
        None,
        None,
        "9a1887e1b7caf00cf5c6d247f71fc8af5c06e7dc1025d5a9f06cc4c287019361",
        None,
    ),
    (
        "R234.resolved_descendant_rows",
        "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json",
        ".result.resolved_descendant_rows[]",
        "materialized_row_id",
        12_200,
        None,
        None,
        "04700e272242cd97ae7851ffcd7cdb255afdb0921d3e681373a4fc8b1edcd3a0",
        None,
    ),
    (
        "R234.depth6_frontier_rows",
        "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json",
        ".result.depth6_frontier_rows[]",
        "frontier_row_id",
        38_376,
        None,
        None,
        "a1b3bf193ad10045f52244c3e40c52f78e0aeacffa3ba52c262bc8912fc9b5a6",
        None,
    ),
    (
        "R237.whole_origin_promotion_rows",
        "cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json",
        ".result.whole_origin_promotion_rows[]",
        "whole_origin_promotion_row_id",
        240,
        None,
        None,
        "fcec0a5790b05960acc1cdf9aa3f2cc9838264ee7583a70a445da1e0dba792f4",
        None,
    ),
    (
        "R238.whole_origin_promotion_rows",
        "cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json",
        ".result.whole_origin_promotion_rows[]",
        "whole_origin_promotion_row_id",
        264,
        None,
        None,
        "e2e69aafa1444ba504b006a53ff44fe51c81dba52aa8edd3a2fff746c6fdec30",
        None,
    ),
    (
        "R244.formal_Round244_known_connectivity_block_carry_ledger",
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json",
        ".result.formal_Round244_known_connectivity_block_carry_ledger.rows[]",
        "block_carry_row_id",
        7_388,
        "ccd7d9d5be04889105e43fe00a71511d10e249bf2cd8a1e1c38560e3b1cb79d2",
        "5f7469b8952e782838b4636b2c6e2d25f37b2d128efe7fdca357e2c92fdb398f",
        "748d83634271e0e45df55c840291a85d67fe1c4b4f5aacca2d8976197977ace4",
        None,
    ),
    (
        "R244.formal_cross_parent_same_chart_bulk_edge_ledger",
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json",
        ".result.formal_cross_parent_same_chart_bulk_edge_ledger.rows[]",
        "cross_parent_bulk_edge_row_id",
        328,
        "327dbfdf6c9b221173d23dfcb237114a07a53f9da9133f9a158f6fbc81fb1641",
        "936e5f039960d168d5a4f4866335ad4b6f4cd27752e4f562a434ea3042b5ed47",
        "17c1f65799070a1549ca4158eeb133d4ff39d924e361c1076780580144593ac8",
        None,
    ),
    (
        "R244.formal_different_parent_candidate_reconciliation_ledger",
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json",
        ".result.formal_different_parent_candidate_reconciliation_ledger.rows[]",
        "candidate_reconciliation_row_id",
        9_830,
        "c22aac287a6ad9da8c2842ed9c8e9b5ee1bddc97a1ce0bf0de298e239e4aee19",
        "fc3cf7ec9af53b7cf9a191fea8f15d634858ff5293de5723e2478eeab2d98e0d",
        "a8642fbdff97dda0f321829af22442b8a6e1e952390c12761e760b2f634c08dc",
        None,
    ),
    (
        "R244.formal_occurrence_known_block_incidence_delta_ledger",
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json",
        ".result.formal_occurrence_known_block_incidence_delta_ledger.rows[]",
        "incidence_delta_row_id",
        20,
        "23c5165548a2916f1aefa5dd0a8cc0fb895a3a3796ebf24c554af3b29bbd06e9",
        "1969564950552cf1d832bb3e02cdd3b014d943f456fa191938b4bcb2648ff700",
        "a877293b6ce57915ddb3a0e6092cded34eb597f4e4e81d1c2c583889d880f397",
        None,
    ),
    (
        "R244.formal_post_Round244_key_frontier_ledger",
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json",
        ".result.formal_post_Round244_key_frontier_ledger.rows[]",
        "key_frontier_row_id",
        116,
        "8734c757768db678eea09be5c05cbcdb5c688b4bfd8d19240d6171007bfb5b9f",
        "1c4c8ade9c8f0c3393e2be83ca5252c90bc3d6c7e58f6f347ddbbec698918230",
        "4200e1b4d58013403610f1d002bf75934d35e8830df7fa142bd44411ff444cec",
        None,
    ),
    (
        "R244.formal_post_Round244_occurrence_known_block_frontier_ledger",
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json",
        ".result.formal_post_Round244_occurrence_known_block_frontier_ledger.rows[]",
        "post_frontier_row_id",
        53_968,
        "1df792189eac227bb8cd61b111f408a67650da1a28b875f95257deee10b4e547",
        "a69039a0ba44a832664ff4ad29193c282fcfc5ae240baa115b10ac69986f2edb",
        "3deef6442de789fe29b8866e08fb1056ed2f4c2c68c986a297c2f25faf7b1211",
        None,
    ),
    (
        "R244.formal_resolved_bulk_component_ledger",
        "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json",
        ".result.formal_resolved_bulk_component_ledger.rows[]",
        "resolved_bulk_component_row_id",
        8_148,
        "d19bcbd02bb583fd242485eb037fbbf28db3e23a587a3729d1a4b6fd56bb8e23",
        "52fb16c30fa7c30b8e844a2777b44ecc6721c2ea5d424b07690e2e0b86ce2c78",
        "7a65957c962885f9e67d3aff19349744360211f2923e99fdf7313996d28116a1",
        None,
    ),
    (
        "R235.single_endpoint_graph_partition_rows",
        "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json",
        ".result.single_endpoint_graph_partition_rows[]",
        "endpoint_graph_partition_row_id",
        38_328,
        None,
        None,
        "e9a3794540170bf013160fb713acfbb1a65d42afedfb7b972cbfdad290549731",
        None,
    ),
    (
        "R236.double_endpoint_partition_rows",
        "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json",
        ".result.double_endpoint_partition_rows[]",
        "double_endpoint_partition_row_id",
        16,
        None,
        None,
        "68f41212de0da7f3468a321a682978daa052cb65a611d756a901ca095bcc0bf6",
        None,
    ),
    (
        "R236.crossing_dependency_discharge_rows",
        "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json",
        ".result.crossing_dependency_discharge_rows[]",
        "crossing_dependency_discharge_row_id",
        32,
        None,
        None,
        "26a8e54cb98f181d79d868ba446dd5cce32e3f9ab00104b4a05616623740e71d",
        None,
    ),
    (
        "R242.formal_positive_2D_transition_sheet_patch_ledger",
        "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json",
        ".result.formal_positive_2D_transition_sheet_patch_ledger.rows[]",
        "transition_sheet_patch_row_id",
        264,
        "0f03acdd1fa621e64a89a79181c83af802a6a3ff338290132acbf0641155baa8",
        "6ed321a2f28be8b51b83b48cb3bff50f4ab67a3020170b8f63d5bac934ab9407",
        "aaf7a94af40427dd8e1b805f2aa5c8c0532e7dc5b2420c803e165d39ba5c0a0f",
        None,
    ),
    (
        "R245.formal_retained_stratum_node_ledger",
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json",
        ".result.formal_retained_stratum_node_ledger.rows[]",
        "retained_stratum_node_id",
        3_664,
        "ef81a9a7d264961541edfb9ba9e8e4c37ddbf7dea01efa3eb72d500a82b44ed5",
        "86bad0d45642388bcac65633d47088b93184d77abdb2be68096cb139e192110c",
        "38583b1aa3f37e37dc03c2b59b2a31c18346462d3d918e001040d6651b11401b",
        None,
    ),
    (
        "R246.formal_new_whole_signature_retained_stratum_node_ledger",
        "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json",
        ".result.formal_new_whole_signature_retained_stratum_node_ledger.rows[]",
        "retained_stratum_node_id",
        2_220,
        "488711dda41780ef47dbe34834ab8e3a41995a471260d7743b562c0190b6c86f",
        "f43d31209c552f275144ede960e49bd1ee4044cb40ee3050340e23d6d38bc671",
        "476a4fe0955fd1672ba5ba1177e65f479bf10a2bfdb62d6443f3d702c1649414",
        None,
    ),
    (
        "R247.formal_new_crossing_and_source_seam_retained_stratum_node_ledger",
        "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json",
        ".result.formal_new_crossing_and_source_seam_retained_stratum_node_ledger.rows[]",
        "retained_stratum_node_id",
        504,
        "8896ff95e8e1c4dd5eb7f53ce3dcf9f39abbcd883c2641846b69129fc7040143",
        "23e3495f9f481cc3f1d037741b27403d7bc4c0be8afe118201ba52a6fc4ce9a7",
        "737b59a2a4a9e67664b9e0a080034083190b67c614849bac9b87b5b4ecaf9629",
        None,
    ),
    (
        "R248.formal_wall_positive_volume_bulk_ledger",
        "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json",
        ".result.formal_wall_positive_volume_bulk_ledger.rows[]",
        "wall_bulk_node_id",
        88_936,
        "6106c39894a7947293934b0b061bcae04e1a2902976b63ccd1756d7790cb6154",
        "e46f242e15bcba4111e14aac3c1dc5d82a5350e9e1514f2b9f90cdbc853e525d",
        "aff5ea1401a6919529d1d54fe54bb9b8d378456fa48f88a75043505b5ee7b8b0",
        None,
    ),
    (
        "R248.formal_wall_half_open_sheet_owner_ledger",
        "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json",
        ".result.formal_wall_half_open_sheet_owner_ledger.rows[]",
        "wall_sheet_node_id",
        38_360,
        "fbb15ef7122367925c72f9d0e396141d3f04a271b78064af41e1f68d9d06cd61",
        "be2e8b880f3a0c8fb833a7ba8dce0bd86d5526b400569377f0fcb66692a8c7e0",
        "e61754dc51732c4c82876d1c2e83fa040747d23253addd64350728169f5ae44b",
        None,
    ),
    (
        "R264.formal_endpoint_empty_branch_correction_disposition_ledger",
        "cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json",
        ".result.formal_endpoint_empty_branch_correction_disposition_ledger.rows[]",
        "endpoint_empty_branch_disposition_row_id",
        400,
        "9b6b78f9feb488bf6e35ed3821e40066e8a665d007145601330ed22f97d89c09",
        "3d3e744252a300176a464f1de9e8369d580d6732e50eae292bd0d51176028e3a",
        "fdf499ca22f287866a24685a7671f8cfe950015be72c3da03db2331db7e38285",
        None,
    ),
    (
        "R266.formal_post_Round266_valid_virtual_node_frontier_ledger",
        "cm2_round266_source_g_expanded_curved_face_closure_certificate.json",
        ".result.formal_post_Round266_valid_virtual_node_frontier_ledger.rows[]",
        "post_Round266_valid_virtual_node_frontier_row_id",
        133_284,
        "2d42533f48f864f01e6bd4a46470e7266c1a2cec590380483cfb7cbfb84634f2",
        "9c31ba929e13eeaea29a9f6abe7cf324222eacb25d123a9b12252b386c12a32e",
        "8c394c1d1b2b42025c25a00ef24ecba748981ed93c75b9aba20ddf15ff8597d5",
        None,
    ),
    (
        "R266.formal_post_Round266_component_member_frontier_ledger",
        "cm2_round266_source_g_expanded_curved_face_closure_certificate.json",
        ".result.formal_post_Round266_component_member_frontier_ledger.rows[]",
        "post_Round266_component_member_frontier_row_id",
        259_752,
        "f064d177c25985b38c899c651923b83ba47ee36b465902cca85a4c21e0c33ca6",
        "1f28c84d14cf3fabb38d0f2d1fdf862ce8f6a4559552d68fd9c0a5bd0a3ed3ee",
        "28398acde446047ff4a210b2fa0831d2c44e3758f7e9239b5ec63cecc386b257",
        None,
    ),
    (
        "B1G0.graph_source_inventory_rows",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz",
        ".graph_source_inventory_rows[]",
        "Round306B1G0_graph_source_inventory_row_id",
        38_624,
        "982ee86845f92368cee72b74c52e401eecfb6dd225a4b198910b89ce34a8a7dc",
        "7fde3bb652a469eb3b04fe31a80c365d010d914700348954c5d917ac1162dace",
        "beda6faaf7d3be25075d8f2a7f292cba97f591d6255758b6b16efc141339673f",
        "a684dad14281e44c9dc02a0f825af661ef152f86a436c827fc0b113d25b4d6a0",
    ),
    (
        "B1G0.graph_sheet_join_rows",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz",
        ".graph_sheet_join_rows[]",
        "Round306B1G0_graph_sheet_join_row_id",
        38_624,
        "b36ca314b15b8b8297dfeda9cb4fe37360ff20339e7603a6388ac172cfb87300",
        "a3c606a9ba302ced5593d941529946729da5d160a32384ca37060b20011a01f5",
        "9238a05af9a97002488576d3648ce06ee750858f156638c314ba2e0a24fe3e1f",
        "3686f3b90a77195dbecd08750707a32f98e07f9fdff5f59d57f09c1178a48fda",
    ),
    (
        "B1G0.graph_side_join_rows",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz",
        ".graph_side_join_rows[]",
        "Round306B1G0_graph_side_join_row_id",
        76_848,
        "9e2a2c015372aa22e5f2cfa1f11ae268496831b3118da5bd5087fc6d7f403f53",
        "2090d073d45f0097df68a60b36085786de0db51d76219b562734465bbf6daff6",
        "43ee8ffd2b77231c43c0af10198bbcc1f1def12f2e6bfd28f82c66ea26a207b2",
        "108bdcbe1c124de15d8f48f82a3cdb7aa545f6f61294be34e3e5b07979d6670e",
    ),
    (
        "B1G0.r264_correction_disposition_rows",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz",
        ".r264_correction_disposition_rows[]",
        "Round306B1G0_R264_correction_disposition_row_id",
        400,
        "b3dec2b9ef34fd5ebc3701201593ca90146f6d6150e5b593284a2a974a1d8caf",
        "f172394acdc909f6bc58f59fd1f361c4a4c5b00d06b2a8e8369b7638a6e6c592",
        "a3df5bc8c8a86ea6958daefa7ec9b99013a04152378e5bcb18991ec4860cac67",
        "a4af6f87737028981be9dccae9c2c28236408aa1f112f507418b6e4516eeb671",
    ),
    (
        "B1G0.b0_member_backbinding_rows",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz",
        ".b0_member_backbinding_rows[]",
        "Round306B1G0_B0_member_backbinding_row_id",
        115_456,
        "ff6c659209636eec5235a375e8f8ba1cd5bf69c39df6630e6dfaeb95b0945d72",
        "88026547b175b4ee968f738fe1276163d364b4482d164dbc2e84377039088eae",
        "35189ef67c69078e44bbd440be37ef870935a8fd67817501ae995cceae383ea6",
        "65493ba72be6047b7c1c4ea64045460ad8160ab05440d02204393d3697a4d541",
    ),
    (
        "B1G0.gap_rows",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz",
        ".gap_rows[]",
        "Round306B1G0_gap_row_id",
        154_096,
        "f1c3bf0bb9991f1298a3bc8ce90d55871122ef81b679f32fca21b81087ee1421",
        "ca9e836b8ca114ba2843a9196748128b6194adb3bd801bb9a28dfff44d28af35",
        "d47d29e9eccc04374851cf12a3bc08fbe62837673fe8beb5dd1c9382337ad27b",
        "5324319ce7b3f90f67b3e12af6848f851008fd52c7cbd7c8d433cd0652c52f9e",
    ),
    # Identity and preserved-occurrence authority.
    (
        "B0.member_support_source_rows",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz",
        ".member_support_source_rows[]",
        "Round306B0_member_support_source_row_id",
        564_492,
        "87b4d34c40c3c1caf053ccb9b4c6c6c32cf6a33ac184f6181864105b500b6d3a",
        "382e7a7ae0e857b812635e0d4bb10571d1aa459a27acd178d81b12f9c68d6285",
        "c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5",
        "58ad4ebe98be5023f31870a0d0d3e0d135d153553393aa56a67f4ef1760f68a3",
    ),
    (
        "R294.occurrence_registry_rows",
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz",
        ".rows[]",
        "Round294_occurrence_registry_row_id",
        431_208,
        "bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509",
        "ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56",
        "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
        None,
    ),
    (
        "R294.representation_binding_rows",
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz",
        ".rows[]",
        "Round294_occurrence_representation_binding_row_id",
        46_288,
        "1a03d7c6d95d6144d4b271e46eb6b83ab4c577f7eb5b9f94d34de692247e50ff",
        "538ddd3aaa79da6ff5dd0738523bcc7bb6c6c192051ada1f96131053fd8190b3",
        "ece198bf5e8b95448b09f60061677feafca3416525ba80f3b88a51e766414be7",
        None,
    ),
    (
        "R266.formal_post_Round266_expanded_occurrence_frontier_ledger",
        "cm2_round266_source_g_expanded_curved_face_closure_certificate.json",
        ".result.formal_post_Round266_expanded_occurrence_frontier_ledger.rows[]",
        "post_Round266_expanded_occurrence_frontier_row_id",
        126_468,
        "db01addd10a5112d56109695684d64994b927ce009e71b5e39dc95de2846acce",
        "08fa74d62a0673cb02339bae0df05007e7f4cb9d452d69feef79a958ceaa5ad9",
        "441cde017675dc279a55d52f47c24c31721309ad1cb03e1ea831e6984569f351",
        None,
    ),
    (
        "R174.resolved_3d_occurrence_rows",
        "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json",
        ".result.resolved_3d_occurrence_rows[]",
        "packed column 0 row_id",
        72_500,
        "3748e6a910c2d009d984d5402ad8310f81ac0c4b33b618ce3a420924e4ede496",
        None,
        "bbd6c0742f16314f4d865e5ba7d3f693939d77764fca11978bb984a5fdb181d5",
        None,
    ),
    (
        "R179.resolved_3d_child_rows",
        "cm2_round179_source_g_residual_tube_arrangement_rows.json",
        ".result.resolved_3d_child_rows[]",
        "packed column 0 row_id",
        17_192,
        "51294c66bb9e48c95c97dab1547380f288d3eaaa902b1ee71ec6d2f224b05a5d",
        None,
        "3b62a6e259b99484a6a398bc1b1e961dcaae2b4c1dc3671375134aff893b8936",
        None,
    ),
    (
        "R204.formal_local_open_3D_region_ledger",
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json",
        ".result.formal_local_open_3D_region_ledger.rows[]",
        "region_row_id",
        736,
        "814edddc1d7ccb6bcd83cd7a6784fe16e1e85a1f8f3948bc26e591fa63095b60",
        "3be5e63b0ba9e11e77ac8c828c7d8212e9edb74735e475024bcafcdcdbf0a85a",
        "8a1141a6890fc5165adf4e6accf4130750107ec1336bb8177150c08825785d08",
        None,
    ),
    (
        "R208.formal_local_open_3D_signature_ledger",
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json",
        ".result.formal_local_open_3D_signature_ledger.rows[]",
        "region_row_id",
        36_040,
        "85c6ae741dcee053d8fa4a37eceb2c97b1ad5859b7636194086a03947969b1d0",
        "df3eccd71d413522e516177bf65f9369ffc7c0fc1f3ebfcec1aecc5165095297",
        "59dd5ee4159b093709f9d484302aba0133e0af52f16adac646b44c83ace8237f",
        None,
    ),
    # A1/A2 authority remains theorem-obligation material, not support credit.
    (
        "R204.formal_2D_sheet_lineage.target_sheet_rows",
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json",
        ".result.formal_2D_sheet_lineage.target_sheet_rows[]",
        "sheet_row_id",
        224,
        "2efad6307c5601e2ddb040fe36df17b5525461fc22598874ab8feaab54f4dc43",
        "ce9c795e707e5aad2c8adb81bdff107153bbc07e648440750948fde2a13571f3",
        "bece147e2a055cefec795808eedfb488ca2febbf072160cff887c12421d24d07",
        None,
    ),
    (
        "R208.formal_direct_leaf_signature_base_ledger",
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json",
        ".result.formal_direct_leaf_signature_base_ledger.rows[]",
        "leaf_row_id",
        18_324,
        "cd36d56f3e4b408a9470e55656a7b2a6979b705041500549698efa6b8330316a",
        "5ee61b8ecdf998d7a92783d43ca36e934b27b574b2f2538104e67e36f9666b62",
        "db6d4b0ddab0ea74774fe62d0dc1c9ef474336c7bb310ca26b0ad2f593e0a36d",
        None,
    ),
    (
        "R208.formal_leaf_geometry_ledger",
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json",
        ".result.formal_leaf_geometry_ledger.rows[]",
        "leaf_row_id",
        18_324,
        "cd36d56f3e4b408a9470e55656a7b2a6979b705041500549698efa6b8330316a",
        "1bd19072c4093b5175dc7d4fbb6838159aaed775c870aeb2ddbb1b90e19d1bd3",
        "da21fae5a5a5734690f152526958d30e1baf2f0aa64077a89febf4bbdbcf55a0",
        None,
    ),
    (
        "R208.formal_final_factor_face_ledger",
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json",
        ".result.formal_final_factor_face_ledger.rows[]",
        "face_row_id",
        18_412,
        "a04fa242a668f5cd7d389701c149b1347ca15b4c3a2f2efddd31ed136745dbec",
        "7c63ea6f4786e5b9702d7ef5054dffbae4a6287615c4f3aace0331930aa666c8",
        "1530fd15aff865fd7d6c3b0c2425b5429e886e780d63af5e52136495f8e84fbd",
        None,
    ),
    (
        "R211.formal_2D_sheet_owner_ledger",
        "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json",
        ".result.formal_2D_sheet_owner_ledger.rows[]",
        "sheet_row_id",
        17_716,
        "bb25748d3c7bc46043f9588983788ecc3cb4a38faa8d40c6ea13383c262570aa",
        "97e1b400d0df06228239f5bda23051cdae8b0b0caa1be0fdb64d8b4bc5527c7e",
        "ed26068a92d4ed74f54cd724680da5bc9cafa811d553415380999ae69ea7fdeb",
        None,
    ),
    (
        "R204.filtered_target_graph_curve_incidence_rows",
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json",
        ".result.formal_1D_boundary_and_intersection_lineage.rows[] | select(.exact_source_target_intersection == true)",
        "edge_row_id",
        504,
        "b1eb2b37951706889aec96208218605e8cf28bdc836e314a64b066a487072baa",
        "734e76aad1d6e6e3c71a94d52e3760f308d5254229d7fbaa45ade55ea8e3cc71",
        "220aeb46880c96144592ce6f1789b20275c0e497916a60d5dbfb0f260283890a",
        None,
    ),
    (
        "R204.filtered_target_graph_point_incidence_rows",
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json",
        ".result.formal_0D_endpoint_and_corner_lineage.rows[] | select(.exact_source_target_intersection_endpoint == true)",
        "point_row_id",
        280,
        "7fc15d641a88eca6f347e8e6108dbae21fedbf043a72031e0e64fe433ac746cc",
        "d4e18500ac0a0fa8733ac7347e69c27bf9e83cc965dd5142da9bad03c0077272",
        "c3b6b05c84bbeaa1f4787024803cfa46b5d9d93fc6b320df127e1967d9582127",
        None,
    ),
    (
        "R211.formal_1D_curve_incidence_owner_ledger",
        "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json",
        ".result.formal_1D_curve_incidence_owner_ledger.rows[]",
        "curve_row_id",
        20_456,
        "a9d68f724a257ae768657dff51767207277a9fff6eebd345d539434789b88270",
        "3d93dd7860c1025bb68acf3568a0b4b66e3106189776aae4bafa12d3902a8522",
        "c604ff7fee7d12c7bb39f5f670848f673e1afa0a44b9fad75d829f264e8fbb71",
        None,
    ),
    (
        "R211.formal_0D_endpoint_incidence_owner_ledger",
        "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json",
        ".result.formal_0D_endpoint_incidence_owner_ledger.rows[]",
        "endpoint_row_id",
        40_912,
        "dd9b72a5e03904dcf649a54e5828aa1e3fa41aa6f453b88a32f7b2abd3005e39",
        "e5466d386b45ea8ab473a8483b5a90a244592491cdb9ecbcdf01b7a40c87d712",
        "de9c48038c7da03671941bd713b9f393a4a5a5b89a0dc53f76bd418a8cd13ed8",
        None,
    ),
    # R2 construction cells and their exact member union.
    (
        "R269.formal_direct_side_signature_ledger",
        "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json",
        ".result.formal_direct_side_signature_ledger.rows[]",
        "signed_region_row_id",
        187_128,
        "30d17682e40900b86780ba0c001c95fd81ec85a00df4d02d0281e1dc14291ec4",
        "bad6026508e3bcc0ef23e84638b4c4be76903bbabe5f1d041a759bac50f4c416",
        "992392cc52465cd5ea427e7776fc16fd889048553950b5338042581c14d98755",
        None,
    ),
    (
        "R269.formal_failclosed_leaf_ledger",
        "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json",
        ".result.formal_failclosed_leaf_ledger.rows[]",
        "failclosed_leaf_row_id",
        70_420,
        "ebcc6fd540a72ea862ab0cdc4c6544f1a0920263d534d0c1554b54552bcfc5e9",
        "467b5b1076dadcc264b9d2f60aeaf5290e1c9dec9a1e0119d706342ddff3b275",
        "e76ea912adb01d0f82a7fc7779d4504577b40acca7ba1fba09ec94565120e109",
        None,
    ),
    (
        "R270.formal_direct_side_signature_ledger",
        "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json",
        ".result.formal_direct_side_signature_ledger.rows[]",
        "signed_region_row_id",
        37_712,
        "da02199cd0fd960d6b9b635414c6261f92634a6e96373322ccb4805ffceb265a",
        "04baca4f94ee7a95ba441e95974240d4de323e08713e183e9a543408792f1e84",
        "6f23d7d545ff8c3add454fe01da64d095f237222228c1dd382ca9b19420d746e",
        None,
    ),
    (
        "R270.formal_failclosed_leaf_ledger",
        "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json",
        ".result.formal_failclosed_leaf_ledger.rows[]",
        "failclosed_leaf_row_id",
        8,
        "4ec77e44a85ed2e42f4560225f0c96363243921a6f2eae9ce63bbc3d373a2a03",
        "2766aff887de89b4389408585d01fbb7adbb6f9b24fbb3eeb6cef25f4daa291f",
        "e4e3807c3fb2c53b18a02ec5edfd5891283d38e48d0b57bdabcf70a373435361",
        None,
    ),
    (
        "R271.formal_side_signature_ledger",
        "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json",
        ".result.formal_side_signature_ledger.rows[]",
        "signed_region_row_id",
        70_420,
        "b71b0d65e1b0511829856e2c5dc42b002a7fc1ad8b7afe4230bcf29b8c338901",
        "f8601678041dd7f79bc276b926ca565995e87d79075b5dd4210af18787ab6da0",
        "cec8a0318385127d8ee5d7968c016f8f6b7ee103596fbce5258cc3b25c4930b8",
        None,
    ),
    (
        "R271.formal_failclosed_leaf_ledger",
        "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json",
        ".result.formal_failclosed_leaf_ledger.rows[]",
        "failclosed_leaf_row_id",
        496,
        "327e884fb879227d171895bc7b87759aad2f6aa70102874850ceb536596510ef",
        "59b2500b739714c2799bdae507559c490cbf1a15693c9a3d3340ca31ae76a74e",
        "4820153f78f785914c33b3738885f136b987cf8c2d3b01b509692454d32d6491",
        None,
    ),
    (
        "R272.formal_side_signature_ledger",
        "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json",
        ".result.formal_side_signature_ledger.rows[]",
        "signed_region_row_id",
        720,
        "9fc1d777079646ddedab5f5a308bf08bccb5ec8088de2b1f5d168bf5cb8a3247",
        "4c41486591353204f59929f6f8288bbcfca09f7a1f767831ac376b0d878b4069",
        "f23f389e39a9715f67fa827026072db638aee34c6f1e539b5ec36bf225e075da",
        None,
    ),
    # Atom identity/disposition authority.  These rows bind R2 cells to the
    # existing occurrence registry; they do not themselves define support.
    (
        "R279.canonical_atom_rows",
        "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz",
        ".rows[]",
        "canonical_atom_id",
        332_016,
        "a685a017d5ae1a4d735a84142b3a2f2c3ed1b3cd2be3c41ad3dca3297f0acbe3",
        "52aed35a8b1b423da27c7b6f05bc6f6721398c606ebe7ec3239770ada9f8887f",
        "d2680baed100e4e1a236aa929999c7d93be5eeddabb2cc0660fca5e756882105",
        None,
    ),
    (
        "R279.formal_face_edge_witness_rows",
        "cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz",
        ".rows[]",
        "formal_face_edge_witness_row_id",
        330_724,
        "5ef215767717f96cab2f4efb29851f41f2efbe8f5aec1c63e4ddef486abe8e92",
        "29efd6ba3b9b1a04580cf2a2593496bd5c1ddabffdb0eab9eaea9f0ac2762b78",
        "bfcb9979545b6abb2e85d54e0200f4394b6e967dbb888e3bcda7ee726cdc6bf7",
        None,
    ),
    (
        "R288.atom_disposition_rows",
        "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz",
        ".rows[]",
        "Round288_atom_disposition_row_id",
        332_016,
        "09a0039e5d9e82413c949823697c794fc65095c1f71d2e6c2f576df0699ec13b",
        "30a167baab36fab7e3e37fd0014c35b9fd94b5491494d21c83dc39080e191f50",
        "8007b0c96e44c76bea6038fed8430134f9f424c7a81508f843d72d473f768849",
        None,
    ),
    (
        "R288.existing_overlap_relation_rows",
        "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_existing_overlap_relations.json.gz",
        ".rows[]",
        "Round288_existing_overlap_relation_row_id",
        36_680,
        "ee2af535c82a4c79042c0e0c55797fb35db22a74d618ee79b2ed4e2c4a25bca6",
        "4ef685a10bbcea11132eff991224dff8a89c137759d1707330faa3aaa5fd2f59",
        "8a93bc24e836f2aca8cf59869217851be8dbedb8c930b325549ded7e8098cb7e",
        None,
    ),
    (
        "R290.inner_support_rows",
        "cm2_round290_source_g_isolated_atom_inner_support_closure_inner_support_ledger.json.gz",
        ".rows[]",
        "Round290_inner_support_row_id",
        21_160,
        "90364fbc92c8ec21100eba1d7ba5cb8ceeb616506f138dfdc21315e63709edb1",
        "925b4c51ea0c6ee2142a4b4fdf4c20cedb351fb24044c953fa5faf3652cefc81",
        "3ab9344c1fa492d87eee4937d11659872ea848c6ff9bf02419c10ae77a0636cd",
        None,
    ),
    (
        "B1R0.predicate_source_cell_rows",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz",
        ".predicate_source_cell_rows[]",
        "Round306B1R0_predicate_source_cell_row_id",
        295_340,
        "b3fb242c0c130122b0e2e7e0c1e38f866f214e332aea93dc6ce03e705201fe9a",
        "33ce0c07cf6eeeb7e8d3d10129dad7652aec94e3d30d18d807499380b35f279d",
        "b89220807eef10bc8412be19c5037ea75fa3c6fdf4321c27938afec0c68c9246",
        "f473914afa7d9dab1598a3259be8a4ec2b08ab7992d7a7039cff8bde5f19512b",
    ),
    (
        "B1R0.member_union_rows",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz",
        ".member_union_rows[]",
        "Round306B1R0_member_union_row_id",
        295_336,
        "6c136186cd30608304293cc91185615ba6bec6418cb2c43a48ac833055c69bfe",
        "d106b9e68817aa9504ec176be9c679f2e4fd29948c3614f7c109030a893f289f",
        "6665fc8e72824fba7dbd1d1b7462ae419bb31c25149037da3183d74569b62a3d",
        "28c6e7944f440f9fee06f9ade150de2566a3aaa85b40c49d63e3721ec4a4c4c5",
    ),
    (
        "B1R0.gap_rows",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_gap.json.gz",
        ".gap_rows[]",
        "Round306B1R0_gap_row_id",
        590_676,
        "98aca1023d164e131c4755b0f35c777f3a984c8ffac6b58aaf1640bddb2dfdba",
        "713e8415b88299f6db95446574f160b864f99a93ef8b12b14c8176cd12904df7",
        "c6bc641ea84b5a25ed851b0d13cef3b8694fcf4224b59868e641a3339496cf3d",
        "6a61506040c6f48236d8f35ee393f3a1d08dc36dbbcfd5a6d58b9290ef1e8904",
    ),
    # R292 transformed-support construction lineage.
    (
        "R275.strict_region_ledger",
        "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json",
        ".result.strict_region_ledger.rows[]",
        "reverse_rechart_region_row_id",
        5_288,
        "f4700e1b6e69ec15b6a7a13189d0b57c9eaa205b6791d944748ee1bd71d1d3bd",
        "dcd6f565597f2ca5f60f767362a1907cfee6fc8b43affdb9bdae1c424fd5cbe5",
        "f1fc71b904d3dd060173c48480c09f2c7960dee2ad51db935d4d80966e0b38b6",
        None,
    ),
    (
        "R275.arrangement_region_ledger",
        "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json",
        ".result.arrangement_region_ledger.rows[]",
        "reverse_rechart_region_row_id",
        8_500,
        "6826e35ff8d9e2bd7c75196dc602082817b4bebe5f0751334fa4a4bd2726060f",
        "936960229d026545d07fd5a5db1586499cb2812852b89af04e149410be004da9",
        "6ef756cfb1d5b1f5226643142e77ba897b5dcac326edb301c5d2d01963470ba5",
        None,
    ),
    (
        "R275.guard_closure_ledger",
        "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json",
        ".result.guard_closure_ledger.rows[]",
        "reverse_rechart_guard_closure_row_id",
        880,
        "49722a30fb6c78931b7d5b7ee19cb74e0f8a77ec1f67f3c41533dd417d92d06c",
        "6c52c6225fee422e5c01bc6b87dc65ff6eb292818d8ec1dbc612ce0f754983c1",
        "fcf3671715938cf106e27a04a7677dbb12821dd64fb7c9b8ce615b42670d7dc8",
        None,
    ),
    (
        "R287.region_rows",
        "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz",
        ".region_rows[]",
        "Round287_region_disposition_row_id",
        13_788,
        None,
        None,
        "7d07e90c481b1c511ccce1d56df67f95140aa8d9b5cf5ea30b1d962ace5d8765",
        None,
    ),
    (
        "R287.refinement_cell_rows",
        "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz",
        ".refinement_cell_rows[]",
        "Round287_refinement_cell_disposition_row_id",
        7_616,
        None,
        None,
        "951e8d912a4bf9494c928fbbdc99663485c019cee79580df98f838e0157555c9",
        None,
    ),
    (
        "R287.valid_internal_physical_face_rows",
        "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz",
        ".valid_internal_physical_face_rows[]",
        "Round287_internal_physical_face_row_id",
        648,
        None,
        None,
        "9a05d9a41aa0877a5066d2477e376706a7a5e296b71e7f2209e9825c25fca2b3",
        None,
    ),
    (
        "R287.potential_new_support_union_rows",
        "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz",
        ".potential_new_support_union_rows[]",
        "Round287_potential_new_support_union_id",
        10_020,
        None,
        None,
        "2185915efd9a8d52ab13a5edea05e0d4e711f1d5cfce1e3f43a7a183a9326800",
        None,
    ),
    (
        "R287.mutually_exclusive_outer_overlap_pair_rows",
        "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz",
        ".mutually_exclusive_outer_overlap_pair_rows[]",
        "Round287_mutually_exclusive_outer_overlap_pair_row_id",
        3_488,
        None,
        None,
        "5477ecd5518ba0bb7f89f6ee3e1fcb55d82f4ee8f895d4f03136b8ccb71b3848",
        None,
    ),
    (
        "R292.complete_heterogeneous_probe_rows",
        "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz",
        ".rows[]",
        "NO_UNIFORM_ROW_ID__SEE_ROW_SCHEMA_CONTRACT",
        22_820,
        None,
        None,
        "556bd0ed95709fe43ff7837522d8729582ce0e7c9679879a57365f864f6ba055",
        None,
    ),
    (
        "R292.exact_refinement_cell_rows",
        "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz",
        ".rows[] | select(has(\"Round292_R287_existing_overlap_refinement_cell_id\"))",
        "Round292_R287_existing_overlap_refinement_cell_id",
        11_852,
        "331a400d3ee35f70fd1ffd52137cdb80d601886f05b4fe6c1e45d9d653d73068",
        "abae741fe7aef5d6aa4ede7ac188d66a6edb6052ffb2b3a4e7d3b89ffd572f0c",
        "77c674fa6c5a72ef085b0f36568d17fb10a10d4721fa5734d3b35ab0fe4eacf0",
        None,
    ),
    (
        "R292.refined_new_support_component_rows",
        "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz",
        ".rows[] | select(has(\"member_refinement_cell_ids\"))",
        "Round292_refined_new_support_component_id",
        9_404,
        "e5ff9eb634175c893c6422a961e1a32c0a7dfa290c967cd6846e641ce963d33f",
        "597d18bff0717f82bd2cc6def5884b5b7055f87366b52c5c1c36dade2dbcb709",
        "696d484a174f1e5a53a874c4bd5109f00824a8c9a4f090c225e7ab17a7005fc2",
        None,
    ),
)

TABLE_AUXILIARY_COMMITMENTS: dict[str, dict[str, str]] = {
    "R182.collar_leaf_rows": {
        "native_attachment_result_sha256": "9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269",
    },
    "R279.formal_face_edge_witness_rows": {
        "candidate_indices_sha256": "855b6fa614c281074513344934fa3cc3c044495f3dd752589c21d1f977bd7cfb",
    },
    "R294.occurrence_registry_rows": {
        "occurrence_ids_sha256": "169869b5755eda22f1527e7393a5bef0a77a842eefbdf45ab34d315b0dad1936",
    },
    "R292.refined_new_support_component_rows": {
        "component_map_sha256": "1128b9b7e23be09390db715d06b73e0f71828aa396792c29c2b587b483046378",
    },
}

TABLE_ROW_SCHEMA_CONTRACTS: dict[str, dict[str, Any]] = {
    "R290.inner_support_rows": {
        "role": "DIAGNOSTIC_ONLY_INNER_WITNESS",
        "forbidden_as_normalized_full_support": True,
        "forbidden_as_outer_support_equivalence_certificate": True,
    },
    "R292.complete_heterogeneous_probe_rows": {
        "whole_table_stored_order_commitment_only": True,
        "uniform_row_id_field": None,
        "row_shapes": [
            {
                "shape": "REGISTRY_OVERLAP",
                "selector": "has(Round292_registry_overlap_row_id)",
                "row_count": 1_564,
                "row_id_field": "Round292_registry_overlap_row_id",
            },
            {
                "shape": "EXACT_REFINEMENT_CELL",
                "selector": "has(Round292_R287_existing_overlap_refinement_cell_id)",
                "row_count": 11_852,
                "row_id_field": "Round292_R287_existing_overlap_refinement_cell_id",
            },
            {
                "shape": "REFINED_NEW_SUPPORT_COMPONENT",
                "selector": "has(member_refinement_cell_ids)",
                "row_count": 9_404,
                "row_id_field": "Round292_refined_new_support_component_id",
            },
        ],
    },
}


AUTHORITY_ROLE_ORDER = (
    "IDENTITY_BINDING",
    "SUPPORT_ROW_SOURCE",
    "ANALYTIC_LINEAGE",
    "CONSTRUCTION_LINEAGE",
    "PROOF_EVIDENCE",
    "OUTER_ENVELOPE_ONLY",
    "DIAGNOSTIC_ONLY",
)

# A role admits bytes only to the stated stage of the later constructor.  It
# never mints normalized support or theorem credit.  `forbidden_as` is copied
# onto every file/table catalog row so a consumer cannot infer permissions by
# looking only at a filename or at a broad authority-family heading.
AUTHORITY_ROLE_POLICIES: dict[str, dict[str, Any]] = {
    "IDENTITY_BINDING": {
        "admitted_for_construction": True,
        "forbidden_as": (
            "NORMALIZED_FULL_SUPPORT",
            "SUPPORT_GEOMETRY",
            "PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM",
            "FORMAL_B1A_OR_CM2_CREDIT",
        ),
    },
    "SUPPORT_ROW_SOURCE": {
        "admitted_for_construction": True,
        "forbidden_as": (
            "NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE",
            "FORMAL_B1A_OR_CM2_CREDIT",
        ),
    },
    "ANALYTIC_LINEAGE": {
        "admitted_for_construction": True,
        "forbidden_as": (
            "PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE",
            "NORMALIZED_FULL_SUPPORT",
            "FORMAL_B1A_OR_CM2_CREDIT",
        ),
    },
    "CONSTRUCTION_LINEAGE": {
        "admitted_for_construction": True,
        "forbidden_as": (
            "NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE",
            "PHYSICAL_INCIDENCE_THEOREM",
            "FORMAL_B1A_OR_CM2_CREDIT",
        ),
    },
    "PROOF_EVIDENCE": {
        "admitted_for_construction": False,
        "forbidden_as": (
            "CONSTRUCTION_ROW_SOURCE",
            "NORMALIZED_FULL_SUPPORT",
            "MAXIMALITY_OR_CM2_CREDIT",
        ),
    },
    "OUTER_ENVELOPE_ONLY": {
        "admitted_for_construction": False,
        "forbidden_as": (
            "INNER_SUPPORT",
            "NORMALIZED_FULL_SUPPORT",
            "EXISTENCE_OR_EQUIVALENCE_THEOREM",
        ),
    },
    "DIAGNOSTIC_ONLY": {
        "admitted_for_construction": False,
        "forbidden_as": (
            "CONSTRUCTION_ROW_SOURCE",
            "NORMALIZED_FULL_SUPPORT",
            "OUTER_SUPPORT_EQUIVALENCE_CERTIFICATE",
            "FORMAL_B1A_OR_CM2_CREDIT",
        ),
    },
}

TABLE_AUTHORITY_ROLE_GROUPS: dict[str, tuple[str, ...]] = {
    "IDENTITY_BINDING": (
        "B0.member_support_source_rows",
        "B1G0.b0_member_backbinding_rows",
        "B1G0.graph_sheet_join_rows",
        "B1G0.graph_side_join_rows",
        "B1G0.graph_source_inventory_rows",
        "B1G0.r264_correction_disposition_rows",
        "B1R0.member_union_rows",
        "R264.formal_endpoint_empty_branch_correction_disposition_ledger",
        "R266.formal_post_Round266_component_member_frontier_ledger",
        "R266.formal_post_Round266_expanded_occurrence_frontier_ledger",
        "R266.formal_post_Round266_valid_virtual_node_frontier_ledger",
        "R279.canonical_atom_rows",
        "R288.atom_disposition_rows",
        "R288.existing_overlap_relation_rows",
        "R294.occurrence_registry_rows",
        "R294.representation_binding_rows",
    ),
    "SUPPORT_ROW_SOURCE": (
        "B1R0.predicate_source_cell_rows",
        "R174.resolved_3d_occurrence_rows",
        "R179.resolved_3d_child_rows",
        "R204.formal_local_open_3D_region_ledger",
        "R208.formal_local_open_3D_signature_ledger",
        "R269.formal_direct_side_signature_ledger",
        "R269.formal_failclosed_leaf_ledger",
        "R270.formal_direct_side_signature_ledger",
        "R270.formal_failclosed_leaf_ledger",
        "R271.formal_failclosed_leaf_ledger",
        "R271.formal_side_signature_ledger",
        "R272.formal_side_signature_ledger",
    ),
    "ANALYTIC_LINEAGE": (
        "R182.collar_leaf_rows",
        "R204.filtered_target_graph_curve_incidence_rows",
        "R204.filtered_target_graph_point_incidence_rows",
        "R204.formal_2D_sheet_lineage.target_sheet_rows",
        "R208.formal_direct_leaf_signature_base_ledger",
        "R208.formal_final_factor_face_ledger",
        "R208.formal_leaf_geometry_ledger",
        "R211.formal_0D_endpoint_incidence_owner_ledger",
        "R211.formal_1D_curve_incidence_owner_ledger",
        "R211.formal_2D_sheet_owner_ledger",
        "R220.coordinate_corner_rows",
        "R220.coordinate_edge_rows",
        "R220.coordinate_face_rows",
        "R220.formal_coordinate_adjacency_rows",
        "R220.one_step_split_interface_rows",
        "R220.resolved_child_rows",
        "R275.arrangement_region_ledger",
        "R275.guard_closure_ledger",
        "R275.strict_region_ledger",
    ),
    "CONSTRUCTION_LINEAGE": (
        "R232.whole_origin_promotion_rows",
        "R234.depth6_frontier_rows",
        "R234.resolved_descendant_rows",
        "R234.root_summary_rows",
        "R235.single_endpoint_graph_partition_rows",
        "R236.double_endpoint_partition_rows",
        "R237.whole_origin_promotion_rows",
        "R238.whole_origin_promotion_rows",
        "R242.formal_positive_2D_transition_sheet_patch_ledger",
        "R245.formal_retained_stratum_node_ledger",
        "R246.formal_new_whole_signature_retained_stratum_node_ledger",
        "R247.formal_new_crossing_and_source_seam_retained_stratum_node_ledger",
        "R248.formal_wall_half_open_sheet_owner_ledger",
        "R248.formal_wall_positive_volume_bulk_ledger",
        "R292.exact_refinement_cell_rows",
        "R292.refined_new_support_component_rows",
    ),
    "PROOF_EVIDENCE": (
        "B1G0.gap_rows",
        "B1R0.gap_rows",
        "R220.rejected_exact_coordinate_coincidence_rows",
        "R236.crossing_dependency_discharge_rows",
        "R244.formal_Round244_known_connectivity_block_carry_ledger",
        "R244.formal_cross_parent_same_chart_bulk_edge_ledger",
        "R244.formal_different_parent_candidate_reconciliation_ledger",
        "R244.formal_occurrence_known_block_incidence_delta_ledger",
        "R244.formal_post_Round244_key_frontier_ledger",
        "R244.formal_post_Round244_occurrence_known_block_frontier_ledger",
        "R244.formal_resolved_bulk_component_ledger",
        "R279.formal_face_edge_witness_rows",
    ),
    "OUTER_ENVELOPE_ONLY": (
        "R287.mutually_exclusive_outer_overlap_pair_rows",
        "R287.potential_new_support_union_rows",
        "R287.refinement_cell_rows",
        "R287.region_rows",
        "R287.valid_internal_physical_face_rows",
        "R292.complete_heterogeneous_probe_rows",
    ),
    "DIAGNOSTIC_ONLY": (
        "R290.inner_support_rows",
    ),
}

TABLE_AUTHORITY_ROLES: dict[str, str] = {
    authority: role
    for role, authorities in TABLE_AUTHORITY_ROLE_GROUPS.items()
    for authority in authorities
}

AUTHORITY_FILE_ROLES: dict[str, tuple[str, ...]] = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json": ("SUPPORT_ROW_SOURCE",),
    "cm2_round179_source_g_residual_tube_arrangement_rows.json": ("SUPPORT_ROW_SOURCE",),
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json": ("ANALYTIC_LINEAGE",),
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json": ("SUPPORT_ROW_SOURCE", "ANALYTIC_LINEAGE"),
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json": ("SUPPORT_ROW_SOURCE", "ANALYTIC_LINEAGE"),
    "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json": ("ANALYTIC_LINEAGE",),
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json": ("ANALYTIC_LINEAGE", "PROOF_EVIDENCE"),
    "cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json": ("CONSTRUCTION_LINEAGE",),
    "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json": ("CONSTRUCTION_LINEAGE",),
    "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json": ("CONSTRUCTION_LINEAGE",),
    "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json": ("CONSTRUCTION_LINEAGE", "PROOF_EVIDENCE"),
    "cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json": ("CONSTRUCTION_LINEAGE",),
    "cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json": ("CONSTRUCTION_LINEAGE",),
    "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json": ("CONSTRUCTION_LINEAGE",),
    "cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json": ("PROOF_EVIDENCE",),
    "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json": ("CONSTRUCTION_LINEAGE",),
    "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json": ("CONSTRUCTION_LINEAGE",),
    "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json": ("CONSTRUCTION_LINEAGE",),
    "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json": ("CONSTRUCTION_LINEAGE",),
    "cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json": ("IDENTITY_BINDING",),
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json": ("IDENTITY_BINDING",),
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json": ("SUPPORT_ROW_SOURCE",),
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json": ("SUPPORT_ROW_SOURCE",),
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json": ("SUPPORT_ROW_SOURCE",),
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json": ("SUPPORT_ROW_SOURCE",),
    "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json": ("ANALYTIC_LINEAGE",),
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz": ("IDENTITY_BINDING",),
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz": ("PROOF_EVIDENCE",),
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz": ("OUTER_ENVELOPE_ONLY",),
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz": ("IDENTITY_BINDING",),
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_existing_overlap_relations.json.gz": ("IDENTITY_BINDING",),
    "cm2_round290_source_g_isolated_atom_inner_support_closure_inner_support_ledger.json.gz": ("DIAGNOSTIC_ONLY",),
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz": ("CONSTRUCTION_LINEAGE", "OUTER_ENVELOPE_ONLY"),
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz": ("IDENTITY_BINDING",),
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz": ("IDENTITY_BINDING",),
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz": ("IDENTITY_BINDING",),
    "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz": ("IDENTITY_BINDING",),
    "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz": ("PROOF_EVIDENCE",),
    "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz": ("IDENTITY_BINDING",),
    "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz": ("IDENTITY_BINDING",),
    "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz": ("IDENTITY_BINDING",),
    "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz": ("IDENTITY_BINDING",),
    "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_gap.json.gz": ("PROOF_EVIDENCE",),
    "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz": ("IDENTITY_BINDING",),
    "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz": ("SUPPORT_ROW_SOURCE",),
}


FIELD_PRECEDENCE = (
    "R264_CORRECTION_OVERRIDES_R248_RAW_BULK_AND_OWNER_EDGE_VALIDITY",
    "R245_R248_PRIMITIVE_ROWS_PLUS_PINNED_CONSTRUCTION_LINEAGE_DEFINE_ONLY_SOURCE_CANDIDATES",
    "R266_VALID_AND_COMPONENT_MEMBER_FRONTIERS_DEFINE_SURVIVOR_IDENTITY_NOT_SUPPORT_GEOMETRY",
    "B1G0_SOURCE_JOINS_AND_B0_BACKBINDINGS_DEFINE_IDENTITY_NOT_GRAPH_OR_INCIDENCE_THEOREMS",
    "OFFICIAL_KEY_IS_POST_LINEAGE_METADATA_ONLY_AND_NEVER_A_JOIN_ROUTING_OR_GLUE_FILTER",
    "AF3_TYPED_AST_AND_INDEPENDENT_EQUIVALENCE_CERTIFICATES_ARE_REQUIRED_BEFORE_FULL_SUPPORT_CREDIT",
)

EXCLUDED_SUBSTITUTIONS = (
    "INNER_WITNESS_AS_NORMALIZED_FULL_SUPPORT",
    "OUTER_ENVELOPE_AS_NORMALIZED_FULL_SUPPORT",
    "COORDINATE_GUARD_AS_PHYSICAL_SUPPORT",
    "R182_CLIPPED_ARRANGEMENT_AS_NORMALIZED_FULL_SUPPORT",
    "R220_COORDINATE_ATLAS_AS_PHYSICAL_GLUE_OR_NORMALIZED_FULL_SUPPORT",
    "R244_KNOWN_CONNECTIVITY_LOWER_BOUND_AS_MAXIMALITY_OR_NORMALIZED_FULL_SUPPORT",
    "R279_FACE_EDGE_WITNESS_AS_NORMALIZED_FULL_SUPPORT_OR_INCIDENCE_THEOREM",
    "R288_IDENTITY_DISPOSITION_AS_NORMALIZED_FULL_SUPPORT",
    "R290_INNER_LEDGER_AS_NORMALIZED_FULL_SUPPORT",
    "KEY_EQUALITY_AS_PHYSICAL_GLUE_OR_INCIDENCE",
    "B1G0_JOIN_AS_GRAPH_DEFINITION_OR_INCIDENCE_THEOREM",
    "R266_SURVIVOR_IDENTITY_AS_SUPPORT_GEOMETRY",
    "R248_RAW_EMPTY_BULK_AS_VALID_MEMBER",
    "R236_REFERENCE_DEDUPLICATION_AS_INCIDENCE_EXHAUSTION",
    "824864_THEOREM_OBLIGATIONS_AS_FINAL_FEATURE_LEDGER_ROWS",
    "IMPORT_OR_EXECUTE_UPSTREAM_OR_REPLAY_CODE_IN_THE_CONTRACT_PROCESS",
)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def _partition_rows(values: tuple[tuple[str, int], ...]) -> list[dict[str, Any]]:
    return [{"family": family, "member_count": count} for family, count in values]


def _role_metadata(role: str) -> dict[str, Any]:
    policy = AUTHORITY_ROLE_POLICIES[role]
    return {
        "authority_role": role,
        "admitted_for_construction": policy["admitted_for_construction"],
        "forbidden_as": list(policy["forbidden_as"]),
    }


def _file_role_metadata(roles: tuple[str, ...]) -> dict[str, Any]:
    return {
        "authority_roles": list(roles),
        "admitted_for_construction": any(
            AUTHORITY_ROLE_POLICIES[role]["admitted_for_construction"]
            for role in roles
        ),
        "forbidden_as": sorted(
            {
                forbidden
                for role in roles
                for forbidden in AUTHORITY_ROLE_POLICIES[role]["forbidden_as"]
            }
        ),
    }


def _role_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "authority_role": role,
            "admitted_for_construction": (
                AUTHORITY_ROLE_POLICIES[role]["admitted_for_construction"]
            ),
            "forbidden_as": list(AUTHORITY_ROLE_POLICIES[role]["forbidden_as"]),
        }
        for role in AUTHORITY_ROLE_ORDER
    ]


def _table_rows() -> list[dict[str, Any]]:
    file_pins = {
        filename: (size, sha256)
        for filename, size, sha256 in AUTHORITY_FILE_PINS
    }
    return [
        {
            "authority": authority,
            "filename": filename,
            "source_exact_size": file_pins[filename][0],
            "source_sha256": file_pins[filename][1],
            "json_path": json_path,
            "row_id_field": row_id_field,
            "row_count": row_count,
            "row_ids_sha256": row_ids,
            "row_hashes_sha256": row_hashes,
            "rows_sha256": rows,
            "ledger_sha256": ledger,
            **_role_metadata(TABLE_AUTHORITY_ROLES[authority]),
            "auxiliary_commitments": dict(
                TABLE_AUXILIARY_COMMITMENTS.get(authority, {})
            ),
            "row_schema_contract": deepcopy(
                TABLE_ROW_SCHEMA_CONTRACTS.get(authority, {})
            ),
        }
        for (
            authority,
            filename,
            json_path,
            row_id_field,
            row_count,
            row_ids,
            row_hashes,
            rows,
            ledger,
        ) in TABLE_AUTHORITIES
    ]


def _authority_file_pin_rows() -> list[dict[str, Any]]:
    return [
        {"filename": filename, "exact_size": size, "sha256": sha256}
        for filename, size, sha256 in AUTHORITY_FILE_PINS
    ]


def _authority_file_rows() -> list[dict[str, Any]]:
    return [
        {
            "filename": filename,
            "exact_size": size,
            "sha256": sha256,
            **_file_role_metadata(AUTHORITY_FILE_ROLES[filename]),
        }
        for filename, size, sha256 in AUTHORITY_FILE_PINS
    ]


def _role_catalog() -> dict[str, Any]:
    return {
        "role_policies": _role_policy_rows(),
        "authority_files": [
            {
                "filename": filename,
                **_file_role_metadata(AUTHORITY_FILE_ROLES[filename]),
            }
            for filename, _size, _sha256 in AUTHORITY_FILE_PINS
        ],
        "table_authorities": [
            {
                "authority": authority,
                "filename": filename,
                **_role_metadata(TABLE_AUTHORITY_ROLES[authority]),
            }
            for authority, filename, *_rest in TABLE_AUTHORITIES
        ],
    }


def _pin_rows() -> list[dict[str, Any]]:
    return [
        {"label": label, "filename": filename, "exact_size": size, "sha256": sha256}
        for label, filename, size, sha256 in REPLAY_EVIDENCE_PINS
    ]


def _governance_rows() -> list[dict[str, Any]]:
    return [
        {"label": label, "filename": filename, "exact_size": size, "sha256": sha256}
        for label, filename, size, sha256 in GOVERNANCE_SEAL_PINS
    ]


def _contract_document() -> dict[str, Any]:
    sealed = len(REPLAY_EVIDENCE_PINS) == 4
    return {
        "schema": SCHEMA,
        "status": SEALED_STATUS if sealed else UNSEALED_STATUS,
        "sealed": sealed,
        "non_production": True,
        "candidate_is_formal": False,
        "exact_claim_boundary": {
            "authority_frontier_only": True,
            "construction_sources_identified": True,
            "construction_sources_byte_inventory_independently_replayed": sealed,
            "analytic_AST_frozen": False,
            "normalized_full_support_proved": 0,
            "normalized_full_support_denominator": MEMBER_COUNT,
            "representation_cover_proved": 0,
            "representation_cover_denominator": REPRESENTATION_COUNT,
            "formal_B1A": False,
            "B2_authorized": False,
            "feature_obligation_census": FEATURE_OBLIGATION_CENSUS,
            "feature_obligation_census_is_final_feature_ledger_row_count": False,
        },
        "authority_inventory": {
            "direct_root_count": AUTHORITY_ROOT_COUNT,
            "transitive_file_count": TRANSITIVE_FILE_COUNT,
            "transitive_file_bytes": TRANSITIVE_FILE_BYTES,
            "canonical_inventory_rows_sha256": INVENTORY_ROWS_SHA256,
            "canonical_inventory_rows_order_and_wire_are_replay_bound": True,
            "canonical_inventory_hash_domain": deepcopy(INVENTORY_HASH_DOMAIN),
            "inventory_complete_for_freeze_claim": sealed,
            "authority_role_policies": _role_policy_rows(),
            "authority_role_catalog_sha256": AUTHORITY_ROLE_CATALOG_SHA256,
            "table_authorities": _table_rows(),
            "table_authority_count": TABLE_AUTHORITY_COUNT,
            "table_authority_catalog_sha256": TABLE_AUTHORITY_CATALOG_SHA256,
            "authority_files": _authority_file_rows(),
            "authority_file_count": AUTHORITY_FILE_COUNT,
            "authority_file_bytes": AUTHORITY_FILE_BYTES,
            "authority_file_catalog_sha256": AUTHORITY_FILE_CATALOG_SHA256,
            "authority_file_catalog_wire": (
                "canonical_json(list sorted by filename of "
                "projection {filename,exact_size,sha256}); sort_keys compact ASCII no LF; "
                "role metadata is separately bound by authority_role_catalog_sha256"
            ),
        },
        "governance_seals": {
            "required": True,
            "pin_count": GOVERNANCE_SEAL_COUNT,
            "exact_total_bytes": GOVERNANCE_SEAL_BYTES,
            "pins": _governance_rows(),
            "lineage_only_not_authority_inventory_completion": True,
            "lineage_only_not_theorem_credit": True,
            "old_B2C0_is_inert_and_not_current_support_census": True,
            "AF2_results_are_byte_identical": True,
        },
        "exact_member_partition": {
            "member_count": MEMBER_COUNT,
            "coarse_partition": _partition_rows(COARSE_PARTITION),
            "fine_partition": _partition_rows(FINE_PARTITION),
            "G2a": {
                "sheet_reference_count": 38_624,
                "distinct_member_count": 38_624,
                "R245_member_count": 264,
                "R248_member_count": 38_360,
                "graph_family_histogram": {
                    "R235_SINGLE_ENDPOINT_GRAPH": 38_328,
                    "R236_DOUBLE_ENDPOINT_GRAPH": 32,
                    "R242_UNIQUE_TRANSITION_GRAPH": 264,
                },
            },
            "G2b": {
                "side_reference_count": 76_848,
                "distinct_member_count": 76_832,
                "R245_distinct_member_count": 528,
                "R248_distinct_member_count": 76_304,
                "member_reference_multiplicity_histogram": {"1": 76_816, "2": 16},
                "graph_family_reference_histogram": {
                    "R235_SINGLE_ENDPOINT_GRAPH": 76_256,
                    "R236_DOUBLE_ENDPOINT_GRAPH": 64,
                    "R242_UNIQUE_TRANSITION_GRAPH": 528,
                },
            },
            "non_graph_bulk": {
                "distinct_member_count": 17_828,
                "source_histogram": {
                    "R245_WHOLE_ROOT_ZERO_ABSENCE_BULK": 2_872,
                    "R246_WHOLE_SIGNATURE_RETAINED_BULK": 2_220,
                    "R247_CROSSING_AND_SOURCE_SEAM_RETAINED_BULK": 504,
                    "R248_R234_AND_R236_EXACT_BOX_BULK": 12_232,
                },
            },
        },
        "Round264_empty_bulk_guardrail": {
            "R248_raw_bulk_count": 88_936,
            "R248_sheet_count": 38_360,
            "R248_raw_virtual_count": 127_296,
            "empty_bulk_correction_count": 400,
            "empty_EVENT_ABSENT_bulk_count": 184,
            "empty_EVENT_PRESENT_singleton_phantom_count": 216,
            "invalid_absent_owner_edge_count": 184,
            "retained_t0_sheet_count_across_corrections": 400,
            "R248_final_bulk_count": 88_536,
            "R248_final_virtual_count": 126_896,
            "all_virtual_member_count_after_R245_R247_inheritance": 133_284,
            "empty_bulk_ids_excluded_from_G2b": True,
            "empty_bulk_ids_excluded_from_non_graph_bulk": True,
            "invalid_owner_edges_may_not_be_restored": True,
            "phantom_components_may_not_be_restored": True,
        },
        "authority_semantics": {
            "field_precedence": list(FIELD_PRECEDENCE),
            "excluded_substitutions": list(EXCLUDED_SUBSTITUTIONS),
            "official_key_used_as_join_or_routing_filter": False,
            "witness_fields_are_full_support_by_default": False,
            "outer_envelopes_are_full_support_by_default": False,
            "R266_defines_support_geometry": False,
            "B1G0_grants_graph_or_incidence_credit": False,
            "upstream_or_replay_modules_imported_or_executed_in_process": False,
        },
        "explicit_unclosed_theorems": {
            "source_free_graph_definition": 38_624,
            "graph_to_sheet_physical_identification": 38_624,
            "graph_side_positive_3D_physical_incidence": 76_848,
            "total_B1G0_gap_rows": 154_096,
            "all_remain_zero_credit": True,
        },
        "independent_replay_evidence": {
            "required": True,
            "completed": sealed,
            "pins": _pin_rows(),
            "pin_count": len(REPLAY_EVIDENCE_PINS),
            "primary_and_independent_sources_must_differ": True,
            "primary_and_independent_results_must_be_byte_identical": True,
            "expected_canonical_result_sha256": EXPECTED_REPLAY_RESULT_SHA256,
            "in_process_import_or_exec_forbidden": True,
            "execution_if_requested": (
                "only an exact-SHA-pinned source may be passed to a subprocess; "
                "stdout must equal the pinned canonical result bytes, stderr must be empty, "
                "and primary/independent stdout must be byte-identical"
            ),
        },
        "remaining_required_work": [
            "seal two independent authority-inventory replay sources and byte-identical results",
            "freeze typed analytic support AST and certificate grammar",
            "construct and prove normalized support for all 564492 members",
            "prove representation pullback cover for all 611904 representations",
            "close 38624 graph definitions 38624 sheet identifications and 76848 side incidences",
            "admit a new independently audited formal B1A package schema",
            "only after formal B1A publish a fresh B2 contract and authorize heavy routing",
        ],
        "candidate_mode": {
            "enabled": False,
            "blocked_before_path_inspection": True,
            "blocked_before_input_open": True,
            "blocked_before_subprocess": True,
            "blocked_before_stdout_or_stderr": True,
            "blocked_before_temp_directory_or_write": True,
        },
        "production_mode": {
            "enabled": False,
            "blocked_before_path_inspection": True,
            "blocked_before_input_open": True,
            "blocked_before_subprocess": True,
            "blocked_before_stdout_or_stderr": True,
            "blocked_before_temp_directory_or_write": True,
        },
        "formal_credit": {
            "feature_definition": 0,
            "normalized_member_support": 0,
            "representation_cover": 0,
            "graph_definition": 0,
            "physical_incidence": 0,
            "transition": 0,
            "pair_routing": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "D02": "BLOCKED",
            "D03": "NOT_REACHED",
            "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "emission_accounting": {
            "support_rows_written": 0,
            "representation_rows_written": 0,
            "candidate_files_written": 0,
            "production_files_written": 0,
            "formal_files_written": 0,
        },
    }


def _as_map(rows: list[dict[str, Any]]) -> dict[str, int]:
    return {str(row["family"]): int(row["member_count"]) for row in rows}


def validate_contract(document: dict[str, Any]) -> None:
    sealed = len(REPLAY_EVIDENCE_PINS) == 4
    need(document.get("schema") == SCHEMA, "schema")
    need(document.get("sealed") is sealed, "sealed state")
    need(document.get("status") == (SEALED_STATUS if sealed else UNSEALED_STATUS), "status")
    need(document.get("non_production") is True, "non-production")
    need(document.get("candidate_is_formal") is False, "candidate non-formal")
    if EXPECTED_CONTRACT_SHA256 is not None:
        need(digest(document) == EXPECTED_CONTRACT_SHA256, "canonical contract digest")

    boundary = document["exact_claim_boundary"]
    need(boundary["authority_frontier_only"] is True, "authority only")
    need(boundary["construction_sources_byte_inventory_independently_replayed"] is sealed, "replay-bound inventory")
    need(boundary["analytic_AST_frozen"] is False, "analytic AST blocked")
    need((boundary["normalized_full_support_proved"], boundary["normalized_full_support_denominator"]) == (0, MEMBER_COUNT), "support zero")
    need((boundary["representation_cover_proved"], boundary["representation_cover_denominator"]) == (0, REPRESENTATION_COUNT), "representation zero")
    need(boundary["formal_B1A"] is False, "formal B1A blocked")
    need(boundary["B2_authorized"] is False, "B2 unauthorized")
    need(boundary["feature_obligation_census"] == FEATURE_OBLIGATION_CENSUS, "obligation census")
    need(boundary["feature_obligation_census_is_final_feature_ledger_row_count"] is False, "obligation not rows")

    inventory = document["authority_inventory"]
    need(inventory["direct_root_count"] == AUTHORITY_ROOT_COUNT, "root count")
    need(inventory["transitive_file_count"] == TRANSITIVE_FILE_COUNT, "transitive count")
    need(inventory["transitive_file_bytes"] == TRANSITIVE_FILE_BYTES, "transitive bytes")
    need(inventory["canonical_inventory_rows_sha256"] == INVENTORY_ROWS_SHA256, "inventory digest")
    need(inventory["canonical_inventory_hash_domain"] == INVENTORY_HASH_DOMAIN, "inventory hash domain")
    domain = inventory["canonical_inventory_hash_domain"]
    need(domain["accepted_assignment_name"] == "PINS", "exact PINS assignment")
    need(domain["similarly_named_assignments_ignored"] is True, "ignore similar pin assignments")
    need(domain["all_PINS_key_file_types_enter_catalog"] is True, "all PINS file types")
    need(domain["only_dot_py_PINS_keys_are_recursed"] is True, "only Python recursion")
    need(domain["row_fields_exact"] == ["filename", "exact_size", "sha256", "root_source"], "inventory row fields")
    need(domain["root_source_semantics"] == "BOOLEAN_FILENAME_IS_MEMBER_OF_36_ROOTS", "root source membership")
    need(domain["row_order"] == "FILENAME_ASCII_ASCENDING", "inventory order")
    need(domain["final_LF"] is False, "inventory no LF")
    need(inventory["inventory_complete_for_freeze_claim"] is sealed, "inventory seal")
    need(inventory["authority_role_policies"] == _role_policy_rows(), "authority role policies")
    need(inventory["authority_role_catalog_sha256"] == AUTHORITY_ROLE_CATALOG_SHA256, "authority role catalog sha")
    need(HEX64.fullmatch(AUTHORITY_ROLE_CATALOG_SHA256) is not None, "authority role catalog sha syntax")
    need(digest(_role_catalog()) == AUTHORITY_ROLE_CATALOG_SHA256, "authority role catalog digest")
    need(inventory["table_authorities"] == _table_rows(), "table authorities")
    need(inventory["table_authority_count"] == TABLE_AUTHORITY_COUNT == len(TABLE_AUTHORITIES), "table authority count")
    need(inventory["table_authority_catalog_sha256"] == TABLE_AUTHORITY_CATALOG_SHA256, "table authority catalog sha")
    need(HEX64.fullmatch(TABLE_AUTHORITY_CATALOG_SHA256) is not None, "table authority catalog sha syntax")
    need(digest(_table_rows()) == TABLE_AUTHORITY_CATALOG_SHA256, "table authority catalog digest")
    need(len(AUTHORITY_FILE_PINS) == AUTHORITY_FILE_COUNT == 45, "authority file count constant")
    need(sum(row[1] for row in AUTHORITY_FILE_PINS) == AUTHORITY_FILE_BYTES, "authority file bytes constant")
    need([row[0] for row in AUTHORITY_FILE_PINS] == sorted(row[0] for row in AUTHORITY_FILE_PINS), "authority file order")
    need(len({row[0] for row in AUTHORITY_FILE_PINS}) == AUTHORITY_FILE_COUNT, "unique authority filenames")
    for filename, size, sha256 in AUTHORITY_FILE_PINS:
        need(filename not in {"", ".", ".."} and "/" not in filename, "simple authority filename")
        need(type(size) is int and size > 0, "authority file size")
        need(HEX64.fullmatch(sha256) is not None, "authority file sha")
    need(HEX64.fullmatch(AUTHORITY_FILE_CATALOG_SHA256) is not None, "authority catalog sha syntax")
    need(digest(_authority_file_pin_rows()) == AUTHORITY_FILE_CATALOG_SHA256, "authority file catalog digest")
    need(inventory["authority_files"] == _authority_file_rows(), "authority file pins")
    need(inventory["authority_file_count"] == AUTHORITY_FILE_COUNT, "authority file count")
    need(inventory["authority_file_bytes"] == AUTHORITY_FILE_BYTES, "authority file bytes")
    need(inventory["authority_file_catalog_sha256"] == AUTHORITY_FILE_CATALOG_SHA256, "authority file catalog sha")
    need({row[1] for row in TABLE_AUTHORITIES} == {row[0] for row in AUTHORITY_FILE_PINS}, "every table file exactly pinned")
    authority_labels = [row[0] for row in TABLE_AUTHORITIES]
    need(len(authority_labels) == len(set(authority_labels)), "unique table authority labels")
    need(tuple(AUTHORITY_ROLE_POLICIES) == AUTHORITY_ROLE_ORDER, "authority role policy order")
    need(set(TABLE_AUTHORITY_ROLE_GROUPS) == set(AUTHORITY_ROLE_ORDER), "table role group coverage")
    role_rank = {role: index for index, role in enumerate(AUTHORITY_ROLE_ORDER)}
    for role in AUTHORITY_ROLE_ORDER:
        policy = AUTHORITY_ROLE_POLICIES[role]
        need(type(policy["admitted_for_construction"]) is bool, "role admission boolean")
        forbidden_as = policy["forbidden_as"]
        need(type(forbidden_as) is tuple and bool(forbidden_as), "role forbidden-as tuple")
        need(len(forbidden_as) == len(set(forbidden_as)), "unique role prohibitions")
        need(all(type(value) is str and bool(value) for value in forbidden_as), "role prohibition strings")
    grouped_labels = [
        authority
        for role in AUTHORITY_ROLE_ORDER
        for authority in TABLE_AUTHORITY_ROLE_GROUPS[role]
    ]
    need(len(grouped_labels) == len(set(grouped_labels)) == TABLE_AUTHORITY_COUNT, "one role per table authority")
    need(set(grouped_labels) == set(authority_labels), "table role exact coverage")
    need(set(TABLE_AUTHORITY_ROLES) == set(authority_labels), "flattened table role coverage")
    authority_filenames = {row[0] for row in AUTHORITY_FILE_PINS}
    need(set(AUTHORITY_FILE_ROLES) == authority_filenames, "file role exact coverage")
    table_roles_by_filename: dict[str, set[str]] = {
        filename: set() for filename in authority_filenames
    }
    for authority, filename, *_rest in TABLE_AUTHORITIES:
        table_roles_by_filename[filename].add(TABLE_AUTHORITY_ROLES[authority])
    for filename, roles in AUTHORITY_FILE_ROLES.items():
        need(bool(roles) and len(roles) == len(set(roles)), "nonempty unique file roles")
        need(all(role in role_rank for role in roles), "known file roles")
        need(roles == tuple(sorted(roles, key=role_rank.__getitem__)), "canonical file role order")
        need(set(roles) == table_roles_by_filename[filename], "file roles equal table roles")
    required_authority_labels = {
        "R182.collar_leaf_rows",
        "B0.member_support_source_rows",
        "R294.occurrence_registry_rows",
        "R294.representation_binding_rows",
        "R266.formal_post_Round266_expanded_occurrence_frontier_ledger",
        "R174.resolved_3d_occurrence_rows",
        "R179.resolved_3d_child_rows",
        "R204.formal_local_open_3D_region_ledger",
        "R208.formal_local_open_3D_signature_ledger",
        "R204.formal_2D_sheet_lineage.target_sheet_rows",
        "R208.formal_direct_leaf_signature_base_ledger",
        "R208.formal_leaf_geometry_ledger",
        "R208.formal_final_factor_face_ledger",
        "R211.formal_2D_sheet_owner_ledger",
        "R204.filtered_target_graph_curve_incidence_rows",
        "R204.filtered_target_graph_point_incidence_rows",
        "R211.formal_1D_curve_incidence_owner_ledger",
        "R211.formal_0D_endpoint_incidence_owner_ledger",
        "R269.formal_direct_side_signature_ledger",
        "R270.formal_direct_side_signature_ledger",
        "R271.formal_side_signature_ledger",
        "R272.formal_side_signature_ledger",
        "B1R0.predicate_source_cell_rows",
        "B1R0.member_union_rows",
        "B1R0.gap_rows",
        "R275.strict_region_ledger",
        "R275.arrangement_region_ledger",
        "R287.region_rows",
        "R287.refinement_cell_rows",
        "R287.valid_internal_physical_face_rows",
        "R287.potential_new_support_union_rows",
        "R287.mutually_exclusive_outer_overlap_pair_rows",
        "R292.complete_heterogeneous_probe_rows",
        "R292.exact_refinement_cell_rows",
        "R292.refined_new_support_component_rows",
        "R279.canonical_atom_rows",
        "R279.formal_face_edge_witness_rows",
        "R288.atom_disposition_rows",
        "R288.existing_overlap_relation_rows",
        "R290.inner_support_rows",
        "R235.single_endpoint_graph_partition_rows",
        "R242.formal_positive_2D_transition_sheet_patch_ledger",
        "R245.formal_retained_stratum_node_ledger",
        "R248.formal_wall_positive_volume_bulk_ledger",
        "R264.formal_endpoint_empty_branch_correction_disposition_ledger",
        "B1G0.graph_source_inventory_rows",
        "B1G0.graph_sheet_join_rows",
        "B1G0.graph_side_join_rows",
        "B1G0.r264_correction_disposition_rows",
        "B1G0.b0_member_backbinding_rows",
        "B1G0.gap_rows",
    }
    need(required_authority_labels <= set(authority_labels), "complete authority family coverage")
    for authority, filename, json_path, row_id_field, row_count, row_ids, row_hashes, rows, ledger in TABLE_AUTHORITIES:
        need(bool(authority) and bool(row_id_field), "table authority identity")
        need(filename not in {"", ".", ".."} and "/" not in filename, "simple table filename")
        need(json_path.startswith("."), "table JSON path")
        need(type(row_count) is int and row_count > 0, "positive table row count")
        for commitment in (row_ids, row_hashes, rows, ledger):
            need(commitment is None or HEX64.fullmatch(commitment) is not None, "exact table commitment")
    need(set(TABLE_AUXILIARY_COMMITMENTS) <= set(authority_labels), "auxiliary table authority labels")
    for commitments in TABLE_AUXILIARY_COMMITMENTS.values():
        need(bool(commitments), "nonempty auxiliary commitments")
        need(all(HEX64.fullmatch(value) is not None for value in commitments.values()), "exact auxiliary commitments")
    need(set(TABLE_ROW_SCHEMA_CONTRACTS) <= set(authority_labels), "row schema authority labels")
    inner = TABLE_ROW_SCHEMA_CONTRACTS["R290.inner_support_rows"]
    need(inner["role"] == "DIAGNOSTIC_ONLY_INNER_WITNESS", "R290 diagnostic role")
    need(inner["forbidden_as_normalized_full_support"] is True, "R290 not full support")
    need(inner["forbidden_as_outer_support_equivalence_certificate"] is True, "R290 not equivalence")
    need(TABLE_AUTHORITY_ROLES["R290.inner_support_rows"] == "DIAGNOSTIC_ONLY", "R290 table role")
    heterogeneous = TABLE_ROW_SCHEMA_CONTRACTS["R292.complete_heterogeneous_probe_rows"]
    need(heterogeneous["whole_table_stored_order_commitment_only"] is True, "R292 stored order")
    need(heterogeneous["uniform_row_id_field"] is None, "R292 no uniform row id")
    need(sum(row["row_count"] for row in heterogeneous["row_shapes"]) == 22_820, "R292 shape census")
    need(len({row["shape"] for row in heterogeneous["row_shapes"]}) == 3, "R292 unique shapes")
    need(len({row["row_id_field"] for row in heterogeneous["row_shapes"]}) == 3, "R292 shape id fields")

    governance = document["governance_seals"]
    need(len(GOVERNANCE_SEAL_PINS) == GOVERNANCE_SEAL_COUNT == 17, "governance seal count constant")
    need(sum(row[2] for row in GOVERNANCE_SEAL_PINS) == GOVERNANCE_SEAL_BYTES, "governance seal bytes constant")
    need(governance["required"] is True, "governance seals required")
    need(governance["pin_count"] == GOVERNANCE_SEAL_COUNT, "governance pin count")
    need(governance["exact_total_bytes"] == GOVERNANCE_SEAL_BYTES, "governance bytes")
    need(governance["pins"] == _governance_rows(), "governance pins")
    need(len({row[0] for row in GOVERNANCE_SEAL_PINS}) == GOVERNANCE_SEAL_COUNT, "unique governance labels")
    need(len({row[1] for row in GOVERNANCE_SEAL_PINS}) == GOVERNANCE_SEAL_COUNT, "unique governance filenames")
    for _label, filename, size, sha256 in GOVERNANCE_SEAL_PINS:
        need(filename not in {"", ".", ".."} and "/" not in filename, "simple governance filename")
        need(type(size) is int and size > 0, "governance size")
        need(HEX64.fullmatch(sha256) is not None, "governance sha")
    need(GOVERNANCE_SEAL_PINS[13][3] == GOVERNANCE_SEAL_PINS[15][3], "AF2 result byte identity pin")
    for key in (
        "lineage_only_not_authority_inventory_completion",
        "lineage_only_not_theorem_credit",
        "old_B2C0_is_inert_and_not_current_support_census",
        "AF2_results_are_byte_identical",
    ):
        need(governance[key] is True, "governance boundary:" + key)

    exact = document["exact_member_partition"]
    need(exact["member_count"] == MEMBER_COUNT, "member count")
    need(exact["coarse_partition"] == _partition_rows(COARSE_PARTITION), "coarse partition")
    need(exact["fine_partition"] == _partition_rows(FINE_PARTITION), "fine partition")
    coarse = _as_map(exact["coarse_partition"])
    fine = _as_map(exact["fine_partition"])
    need(sum(coarse.values()) == MEMBER_COUNT, "coarse sum")
    need(sum(fine.values()) == MEMBER_COUNT, "fine sum")
    need(sum(value for key, value in fine.items() if key.startswith("PRESERVED_")) == coarse["direct_preserved_source_geometry"], "preserved equation")
    need(sum(value for key, value in fine.items() if key.startswith("R288_")) == coarse["R2_predicate_union_members"], "R2 equation")
    need(fine["R292_EXACT_T2PS_REFINEMENT_CELL_UNION"] == coarse["R292_transformed_cell_union_members"], "R292 equation")
    need(fine["R245_GRAPH_SHEET_REQUIRES_G2A_SUPPORT"] + fine["R248_GRAPH_SHEET_REQUIRES_G2A_SUPPORT"] == coarse["G2a_graph_sheet_members"], "G2a equation")
    need(fine["R245_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT"] + fine["R248_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT"] == coarse["G2b_graph_side_members"], "G2b equation")
    need(sum(value for key, value in fine.items() if "NON_GRAPH_BULK" in key) == coarse["non_graph_virtual_bulk_members"], "bulk equation")

    g2a = exact["G2a"]
    need(g2a["sheet_reference_count"] == g2a["distinct_member_count"] == 38_624, "G2a count")
    need(g2a["R245_member_count"] + g2a["R248_member_count"] == 38_624, "G2a source split")
    need(sum(g2a["graph_family_histogram"].values()) == 38_624, "G2a family sum")
    g2b = exact["G2b"]
    need((g2b["side_reference_count"], g2b["distinct_member_count"]) == (76_848, 76_832), "G2b count")
    need(g2b["R245_distinct_member_count"] + g2b["R248_distinct_member_count"] == 76_832, "G2b source split")
    need(g2b["member_reference_multiplicity_histogram"] == {"1": 76_816, "2": 16}, "G2b multiplicity")
    need(sum(g2b["member_reference_multiplicity_histogram"].values()) == 76_832, "G2b distinct equation")
    need(sum(int(key) * value for key, value in g2b["member_reference_multiplicity_histogram"].items()) == 76_848, "G2b reference equation")
    need(sum(g2b["graph_family_reference_histogram"].values()) == 76_848, "G2b family sum")
    bulk = exact["non_graph_bulk"]
    need(bulk["distinct_member_count"] == 17_828, "bulk count")
    need(sum(bulk["source_histogram"].values()) == 17_828, "bulk source sum")

    r264 = document["Round264_empty_bulk_guardrail"]
    need(r264["R248_raw_bulk_count"] + r264["R248_sheet_count"] == r264["R248_raw_virtual_count"] == 127_296, "R248 raw equation")
    need(r264["empty_EVENT_ABSENT_bulk_count"] + r264["empty_EVENT_PRESENT_singleton_phantom_count"] == r264["empty_bulk_correction_count"] == 400, "R264 split")
    need(r264["R248_raw_bulk_count"] - r264["empty_bulk_correction_count"] == r264["R248_final_bulk_count"] == 88_536, "R248 bulk correction")
    need(r264["R248_final_bulk_count"] + r264["R248_sheet_count"] == r264["R248_final_virtual_count"] == 126_896, "R248 final equation")
    need(r264["R248_final_virtual_count"] + 6_388 == r264["all_virtual_member_count_after_R245_R247_inheritance"] == 133_284, "virtual frontier equation")
    for key in ("empty_bulk_ids_excluded_from_G2b", "empty_bulk_ids_excluded_from_non_graph_bulk", "invalid_owner_edges_may_not_be_restored", "phantom_components_may_not_be_restored"):
        need(r264[key] is True, "R264 exclusion:" + key)

    semantics = document["authority_semantics"]
    need(semantics["field_precedence"] == list(FIELD_PRECEDENCE), "field precedence")
    need(semantics["excluded_substitutions"] == list(EXCLUDED_SUBSTITUTIONS), "excluded substitutions")
    for key in ("official_key_used_as_join_or_routing_filter", "witness_fields_are_full_support_by_default", "outer_envelopes_are_full_support_by_default", "R266_defines_support_geometry", "B1G0_grants_graph_or_incidence_credit", "upstream_or_replay_modules_imported_or_executed_in_process"):
        need(semantics[key] is False, "semantic exclusion:" + key)

    gaps = document["explicit_unclosed_theorems"]
    need(gaps["source_free_graph_definition"] == 38_624, "graph gaps")
    need(gaps["graph_to_sheet_physical_identification"] == 38_624, "sheet gaps")
    need(gaps["graph_side_positive_3D_physical_incidence"] == 76_848, "side gaps")
    need(sum(gaps[key] for key in ("source_free_graph_definition", "graph_to_sheet_physical_identification", "graph_side_positive_3D_physical_incidence")) == gaps["total_B1G0_gap_rows"] == 154_096, "gap sum")
    need(gaps["all_remain_zero_credit"] is True, "gap zero credit")

    replay = document["independent_replay_evidence"]
    need(replay["required"] is True and replay["completed"] is sealed, "replay completion")
    need(replay["pins"] == _pin_rows() and replay["pin_count"] == len(REPLAY_EVIDENCE_PINS), "replay pins")
    need(replay["in_process_import_or_exec_forbidden"] is True, "replay isolation")
    if sealed:
        labels = [row[0] for row in REPLAY_EVIDENCE_PINS]
        need(labels == ["PRIMARY_REPLAY_SOURCE", "PRIMARY_REPLAY_RESULT", "INDEPENDENT_REPLAY_SOURCE", "INDEPENDENT_REPLAY_RESULT"], "replay labels")
        for _label, filename, size, sha256 in REPLAY_EVIDENCE_PINS:
            need(filename not in {"", ".", ".."} and "/" not in filename, "simple replay filename")
            need(type(size) is int and size > 0, "replay size")
            need(HEX64.fullmatch(sha256) is not None, "replay sha")
        need(REPLAY_EVIDENCE_PINS[0][3] != REPLAY_EVIDENCE_PINS[2][3], "independent replay source")
        need(REPLAY_EVIDENCE_PINS[1][3] == REPLAY_EVIDENCE_PINS[3][3], "byte-identical result pins")
        need(EXPECTED_REPLAY_RESULT_SHA256 is not None and HEX64.fullmatch(EXPECTED_REPLAY_RESULT_SHA256) is not None, "expected replay result")
    else:
        need(REPLAY_EVIDENCE_PINS == (), "unsealed replay pins empty")
        need(EXPECTED_REPLAY_RESULT_SHA256 is None, "unsealed result digest absent")

    need(document["candidate_mode"]["enabled"] is False, "candidate blocked")
    need(document["production_mode"]["enabled"] is False, "production blocked")
    for section in (document["candidate_mode"], document["production_mode"]):
        for key, value in section.items():
            if key != "enabled":
                need(value is True, "pre-action block:" + key)
    credit = document["formal_credit"]
    need(all(value == 0 for key, value in credit.items() if key not in {"D02", "D03", "D04", "CM2"}), "zero formal credit")
    need(credit["D02"] == "BLOCKED", "D02")
    need(credit["D03"] == "NOT_REACHED", "D03")
    need(credit["D04"] == "NOT_MINTED", "D04")
    need(credit["CM2"] == "NO-GO_FOR_CLAIM", "CM2")
    need(all(value == 0 for value in document["emission_accounting"].values()), "zero emission")


def contract() -> dict[str, Any]:
    document = _contract_document()
    validate_contract(document)
    return document


def build_private_candidate(_candidate: Path) -> NoReturn:
    raise ContractBlocked(CANDIDATE_BLOCK_REASON)


def build_production_package(_production: Path) -> NoReturn:
    raise ContractBlocked(PRODUCTION_BLOCK_REASON)


def _set_path(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: Any = document
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = value


def _mutation_suite() -> tuple[int, int]:
    attacks: tuple[tuple[tuple[Any, ...], Any], ...] = (
        (("status",), "PASS_FORMAL"),
        (("sealed",), not (len(REPLAY_EVIDENCE_PINS) == 4)),
        (("non_production",), False),
        (("candidate_is_formal",), True),
        (("exact_claim_boundary", "analytic_AST_frozen"), True),
        (("exact_claim_boundary", "normalized_full_support_proved"), 1),
        (("exact_claim_boundary", "normalized_full_support_denominator"), MEMBER_COUNT - 1),
        (("exact_claim_boundary", "representation_cover_proved"), 1),
        (("exact_claim_boundary", "representation_cover_denominator"), REPRESENTATION_COUNT - 1),
        (("exact_claim_boundary", "formal_B1A"), True),
        (("exact_claim_boundary", "B2_authorized"), True),
        (("exact_claim_boundary", "feature_obligation_census_is_final_feature_ledger_row_count"), True),
        (("authority_inventory", "direct_root_count"), 35),
        (("authority_inventory", "transitive_file_count"), 142),
        (("authority_inventory", "transitive_file_bytes"), TRANSITIVE_FILE_BYTES - 1),
        (("authority_inventory", "canonical_inventory_rows_sha256"), "0" * 64),
        (("authority_inventory", "canonical_inventory_hash_domain", "accepted_assignment_name"), "ANY_NAME_CONTAINING_PINS"),
        (("authority_inventory", "canonical_inventory_hash_domain", "all_PINS_key_file_types_enter_catalog"), False),
        (("authority_inventory", "canonical_inventory_hash_domain", "row_fields_exact"), ["filename", "sha256"]),
        (("authority_inventory", "canonical_inventory_hash_domain", "root_source_semantics"), "ROOT_FILENAME_STRING"),
        (("authority_inventory", "canonical_inventory_hash_domain", "final_LF"), True),
        (("authority_inventory", "authority_role_policies", 0, "admitted_for_construction"), False),
        (("authority_inventory", "authority_role_catalog_sha256"), "0" * 64),
        (("authority_inventory", "authority_file_count"), 32),
        (("authority_inventory", "authority_file_bytes"), AUTHORITY_FILE_BYTES - 1),
        (("authority_inventory", "authority_file_catalog_sha256"), "0" * 64),
        (("authority_inventory", "authority_files", 0, "exact_size"), AUTHORITY_FILE_PINS[0][1] - 1),
        (("authority_inventory", "authority_files", 0, "authority_roles"), ["DIAGNOSTIC_ONLY"]),
        (("authority_inventory", "table_authorities", 0, "row_count"), 38_327),
        (("authority_inventory", "table_authorities", 0, "source_sha256"), "0" * 64),
        (("authority_inventory", "table_authorities", 0, "authority_role"), "SUPPORT_ROW_SOURCE"),
        (("authority_inventory", "table_authority_catalog_sha256"), "0" * 64),
        (("authority_inventory", "table_authorities", -1, "auxiliary_commitments", "component_map_sha256"), "0" * 64),
        (("authority_inventory", "table_authorities", -3, "row_schema_contract", "uniform_row_id_field"), "fake_uniform_id"),
        (("governance_seals", "pin_count"), 16),
        (("governance_seals", "exact_total_bytes"), GOVERNANCE_SEAL_BYTES - 1),
        (("governance_seals", "pins", 0, "exact_size"), 1_759),
        (("governance_seals", "pins", 16, "sha256"), "0" * 64),
        (("governance_seals", "lineage_only_not_theorem_credit"), False),
        (("governance_seals", "old_B2C0_is_inert_and_not_current_support_census"), False),
        (("exact_member_partition", "member_count"), MEMBER_COUNT - 1),
        (("exact_member_partition", "coarse_partition", 0, "member_count"), 126_467),
        (("exact_member_partition", "fine_partition", 0, "member_count"), 72_499),
        (("exact_member_partition", "G2a", "distinct_member_count"), 38_623),
        (("exact_member_partition", "G2b", "side_reference_count"), 76_832),
        (("exact_member_partition", "G2b", "distinct_member_count"), 76_304),
        (("exact_member_partition", "G2b", "member_reference_multiplicity_histogram", "2"), 15),
        (("exact_member_partition", "non_graph_bulk", "distinct_member_count"), 17_827),
        (("Round264_empty_bulk_guardrail", "empty_bulk_correction_count"), 399),
        (("Round264_empty_bulk_guardrail", "empty_EVENT_ABSENT_bulk_count"), 183),
        (("Round264_empty_bulk_guardrail", "empty_bulk_ids_excluded_from_G2b"), False),
        (("Round264_empty_bulk_guardrail", "invalid_owner_edges_may_not_be_restored"), False),
        (("authority_semantics", "official_key_used_as_join_or_routing_filter"), True),
        (("authority_semantics", "witness_fields_are_full_support_by_default"), True),
        (("authority_semantics", "R266_defines_support_geometry"), True),
        (("authority_semantics", "B1G0_grants_graph_or_incidence_credit"), True),
        (("authority_semantics", "excluded_substitutions", 0), "ALLOW_WITNESS_AS_SUPPORT"),
        (("explicit_unclosed_theorems", "source_free_graph_definition"), 0),
        (("explicit_unclosed_theorems", "graph_side_positive_3D_physical_incidence"), 0),
        (("independent_replay_evidence", "in_process_import_or_exec_forbidden"), False),
        (("candidate_mode", "enabled"), True),
        (("production_mode", "enabled"), True),
        (("formal_credit", "normalized_member_support"), 1),
        (("formal_credit", "representation_cover"), 1),
        (("formal_credit", "pair_routing"), 1),
        (("formal_credit", "D02"), "PASS"),
        (("formal_credit", "CM2"), "GO"),
        (("emission_accounting", "candidate_files_written"), 1),
        (("emission_accounting", "production_files_written"), 1),
    )
    rejected = 0
    for path, value in attacks:
        mutated = deepcopy(_contract_document())
        _set_path(mutated, path, value)
        try:
            validate_contract(mutated)
        except ContractBlocked:
            rejected += 1
    return rejected, len(attacks)


def _blocked_entry_probe(entry: Callable[[Path], NoReturn], reason: str) -> dict[str, Any]:
    calls: dict[str, int] = {}

    def touched(name: str) -> Callable[..., Any]:
        calls[name] = 0

        def inner(*_args: Any, **_kwargs: Any) -> Any:
            calls[name] += 1
            raise AssertionError("blocked entry crossed boundary:" + name)

        return inner

    os_names = (
        "stat", "lstat", "fstat", "open", "fdopen", "read", "write", "listdir",
        "scandir", "walk", "mkdir", "makedirs", "link", "symlink", "readlink",
        "rename", "replace", "unlink", "remove", "chmod", "fchmod", "truncate",
        "ftruncate", "utime", "fsync", "access", "rmdir", "chdir", "system",
    )
    path_names = (
        "stat", "lstat", "open", "exists", "is_dir", "is_file", "iterdir", "mkdir",
        "rename", "replace", "unlink", "read_bytes", "read_text", "write_bytes",
        "write_text", "touch", "resolve", "glob", "rglob", "chmod", "readlink",
        "symlink_to", "hardlink_to",
    )
    with ExitStack() as stack:
        for name in os_names:
            stack.enter_context(mock.patch.object(os, name, side_effect=touched("os." + name)))
        for name in path_names:
            stack.enter_context(mock.patch.object(Path, name, side_effect=touched("Path." + name)))
        stack.enter_context(mock.patch.object(tempfile, "TemporaryFile", side_effect=touched("tempfile.TemporaryFile")))
        stack.enter_context(mock.patch.object(tempfile, "NamedTemporaryFile", side_effect=touched("tempfile.NamedTemporaryFile")))
        stack.enter_context(mock.patch.object(tempfile, "mkdtemp", side_effect=touched("tempfile.mkdtemp")))
        stack.enter_context(mock.patch.object(builtins, "open", side_effect=touched("builtins.open")))
        stack.enter_context(mock.patch.object(builtins, "print", side_effect=touched("builtins.print")))
        stack.enter_context(mock.patch.object(sys.stdout, "write", side_effect=touched("sys.stdout.write")))
        stack.enter_context(mock.patch.object(sys.stderr, "write", side_effect=touched("sys.stderr.write")))
        stack.enter_context(mock.patch.object(sys.stdout.buffer, "write", side_effect=touched("sys.stdout.buffer.write")))
        stack.enter_context(mock.patch.object(sys.stderr.buffer, "write", side_effect=touched("sys.stderr.buffer.write")))
        stack.enter_context(mock.patch.object(subprocess, "Popen", side_effect=touched("subprocess.Popen")))
        stack.enter_context(mock.patch.object(subprocess, "run", side_effect=touched("subprocess.run")))
        stack.enter_context(mock.patch.object(subprocess, "call", side_effect=touched("subprocess.call")))
        blocked = False
        try:
            entry(Path("/forbidden"))
        except ContractBlocked as error:
            blocked = str(error) == reason
    need(blocked, "blocked entry reason")
    need(all(value == 0 for value in calls.values()), "blocked entry pre-action boundary")
    return {
        "blocked": True,
        "patched_operation_count": len(calls),
        "observed_operation_count": sum(calls.values()),
    }


def self_test() -> dict[str, Any]:
    document = contract()
    for entry, reason in (
        (build_private_candidate, CANDIDATE_BLOCK_REASON),
        (build_production_package, PRODUCTION_BLOCK_REASON),
    ):
        code = entry.__code__
        need(code.co_argcount == 1, "blocked entry arity")
        need(set(code.co_names) <= {"ContractBlocked", "CANDIDATE_BLOCK_REASON", "PRODUCTION_BLOCK_REASON"}, "blocked entry globals")
    rejected, total = _mutation_suite()
    need(rejected == total, "all semantic mutations rejected")
    candidate_probe = _blocked_entry_probe(build_private_candidate, CANDIDATE_BLOCK_REASON)
    production_probe = _blocked_entry_probe(build_production_package, PRODUCTION_BLOCK_REASON)
    result = {
        "schema": SCHEMA + ".self-test.v1",
        "status": (
            "PASS_SEALED_ZERO_CREDIT_AUTHORITY_FREEZE_SELF_TEST"
            if document["sealed"]
            else "PASS_UNSEALED_FAIL_CLOSED_AUTHORITY_FREEZE_STRUCTURE_SELF_TEST"
        ),
        "contract_sha256": digest(document),
        "semantic_mutations_rejected": rejected,
        "semantic_mutation_count": total,
        "candidate_boundary_probe": candidate_probe,
        "production_boundary_probe": production_probe,
        "upstream_or_replay_files_opened": 0,
        "subprocesses_started": 0,
        "stdout_or_stderr_writes_inside_blocked_entries": 0,
        "candidate_or_production_files_written": 0,
        "formal_credit": 0,
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**result, "self_test_sha256": digest(result)}


def _fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_uid,
        info.st_gid,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def _read_exact_pinned_files(
    directory_fd: int,
    pins: tuple[tuple[str, str, int, str], ...],
) -> dict[str, bytes]:
    # Open every evidence object first, then keep every descriptor live until
    # every byte and every final pathname/fd fingerprint has been rechecked.
    # This makes cross-file replacement races fail closed as one held-fd set.
    opened: list[tuple[str, str, int, str, int, tuple[int, ...]]] = []
    try:
        for label, filename, size, expected_sha256 in pins:
            need(filename not in {"", ".", ".."} and "/" not in filename, "simple evidence filename")
            before = os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)
            need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular single-link evidence")
            need(before.st_size == size, "evidence size")
            descriptor = os.open(
                filename,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=directory_fd,
            )
            opened.append(
                (label, filename, size, expected_sha256, descriptor, _fingerprint(before))
            )
            need(_fingerprint(os.fstat(descriptor)) == _fingerprint(before), "evidence fd binding")

        payloads: dict[str, bytes] = {}
        for label, _filename, size, expected_sha256, descriptor, opened_fingerprint in opened:
            chunks: list[bytes] = []
            total = 0
            state = hashlib.sha256()
            while True:
                block = os.read(descriptor, 1 << 20)
                if not block:
                    break
                total += len(block)
                need(total <= size, "bounded evidence read")
                chunks.append(block)
                state.update(block)
            need(total == size and state.hexdigest() == expected_sha256, "evidence byte pin")
            need(_fingerprint(os.fstat(descriptor)) == opened_fingerprint, "stable evidence fd")
            payloads[label] = b"".join(chunks)

        for _label, filename, _size, _sha256, descriptor, opened_fingerprint in opened:
            need(_fingerprint(os.fstat(descriptor)) == opened_fingerprint, "final stable evidence fd set")
            need(
                _fingerprint(
                    os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)
                )
                == opened_fingerprint,
                "final stable evidence pathname set",
            )
        return payloads
    finally:
        for _label, _filename, _size, _sha256, descriptor, _fingerprint_row in opened:
            os.close(descriptor)


def verify_replay_evidence() -> dict[str, Any]:
    need(len(REPLAY_EVIDENCE_PINS) == 4, "replay evidence remains UNSEALED")
    document = contract()
    need(document["sealed"] is True, "sealed contract required")
    data = Path(__file__).absolute().parent
    before = os.stat(data, follow_symlinks=False)
    need(stat.S_ISDIR(before.st_mode), "deliverables directory")
    directory_fd = os.open(data, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        need(_fingerprint(os.fstat(directory_fd)) == _fingerprint(before), "deliverables dirfd binding")
        payloads = _read_exact_pinned_files(directory_fd, REPLAY_EVIDENCE_PINS)
        need(payloads["PRIMARY_REPLAY_RESULT"] == payloads["INDEPENDENT_REPLAY_RESULT"], "replay result byte equality")
        result_bytes = payloads["PRIMARY_REPLAY_RESULT"]
        need(hashlib.sha256(result_bytes).hexdigest() == EXPECTED_REPLAY_RESULT_SHA256, "canonical replay result SHA")
        parsed = json.loads(result_bytes)
        canonical_result = canonical(parsed)
        need(result_bytes in {canonical_result, canonical_result + b"\n"}, "canonical replay result bytes")
        need(type(parsed) is dict, "replay result object")
        need(parsed.get("schema") == REPLAY_RESULT_SCHEMA, "replay result schema")
        need(parsed.get("status") == "ZERO_FULL_SUPPORT_CREDIT", "replay zero-credit status")
        need(parsed["direct_root_count"] == AUTHORITY_ROOT_COUNT, "replay root count")
        need(parsed["transitive_file_count"] == TRANSITIVE_FILE_COUNT, "replay file count")
        need(parsed["transitive_file_bytes"] == TRANSITIVE_FILE_BYTES, "replay bytes")
        need(parsed["inventory_rows_sha256"] == INVENTORY_ROWS_SHA256, "replay inventory digest")
        authority = parsed.get("authority_contract")
        need(type(authority) is dict, "replay authority contract")
        need(authority.get("authority_file_count") == AUTHORITY_FILE_COUNT, "replay authority file count")
        need(authority.get("authority_file_bytes") == AUTHORITY_FILE_BYTES, "replay authority file bytes")
        need(
            authority.get("authority_file_catalog_sha256")
            == AUTHORITY_FILE_CATALOG_SHA256,
            "replay authority file catalog digest",
        )
        need(authority.get("authority_files") == _authority_file_rows(), "replay authority file rows and roles")
        authority_file_projection = [
            {
                "filename": row["filename"],
                "exact_size": row["exact_size"],
                "sha256": row["sha256"],
            }
            for row in authority["authority_files"]
        ]
        need(
            digest(authority_file_projection) == AUTHORITY_FILE_CATALOG_SHA256,
            "replay authority file projection digest",
        )
        need(
            authority.get("authority_role_policies") == _role_policy_rows(),
            "replay authority role policies",
        )
        need(
            authority.get("authority_role_catalog_sha256")
            == AUTHORITY_ROLE_CATALOG_SHA256,
            "replay authority role catalog digest",
        )
        need(
            authority.get("table_authority_count") == TABLE_AUTHORITY_COUNT,
            "replay table authority count",
        )
        need(
            authority.get("table_authority_catalog_sha256")
            == TABLE_AUTHORITY_CATALOG_SHA256,
            "replay table authority catalog digest",
        )
        need(authority.get("table_authorities") == _table_rows(), "replay expanded table authorities")
        replay_role_catalog = {
            "role_policies": authority["authority_role_policies"],
            "authority_files": [
                {
                    key: row[key]
                    for key in (
                        "filename",
                        "authority_roles",
                        "admitted_for_construction",
                        "forbidden_as",
                    )
                }
                for row in authority["authority_files"]
            ],
            "table_authorities": [
                {
                    key: row[key]
                    for key in (
                        "authority",
                        "filename",
                        "authority_role",
                        "admitted_for_construction",
                        "forbidden_as",
                    )
                }
                for row in authority["table_authorities"]
            ],
        }
        need(digest(replay_role_catalog) == AUTHORITY_ROLE_CATALOG_SHA256, "replay role projection digest")
        need(parsed.get("formal_credit") == REPLAY_ZERO_FORMAL_CREDIT, "replay exact zero formal credit")
        safety = parsed.get("safety")
        need(type(safety) is dict, "replay safety object")
        for key in (
            "read_only",
            "held_fd_SHA256",
            "two_pass_same_fd_SHA256",
            "all_domain_fds_held_until_global_reaudit",
            "O_NOFOLLOW",
            "regular_file_required",
            "nlink_one_required",
            "pre_post_fstat_required",
            "same_fd_hash_required",
            "directory_fd_held_and_reaudited",
            "TOCTOU_fail_close",
        ):
            need(safety.get(key) is True, "replay safety:" + key)
        need(safety.get("candidate_files_written") == 0, "replay no candidate writes")
        need(safety.get("filesystem_write_calls") == 0, "replay no filesystem writes")
        need(_fingerprint(os.fstat(directory_fd)) == _fingerprint(before), "deliverables dirfd stable")
        need(_fingerprint(os.stat(data, follow_symlinks=False)) == _fingerprint(before), "deliverables pathname stable")
    finally:
        os.close(directory_fd)
    result = {
        "schema": SCHEMA + ".replay-evidence-verification.v1",
        "status": "PASS_EXACT_PINNED_BYTE_IDENTICAL_REPLAY_RESULTS__ZERO_SUPPORT_CREDIT",
        "checked_file_count": 4,
        "result_bytes_identical": True,
        "replay_result_sha256": EXPECTED_REPLAY_RESULT_SHA256,
        "inventory_rows_sha256": INVENTORY_ROWS_SHA256,
        "authority_file_count": AUTHORITY_FILE_COUNT,
        "authority_file_bytes": AUTHORITY_FILE_BYTES,
        "authority_file_catalog_sha256": AUTHORITY_FILE_CATALOG_SHA256,
        "authority_role_catalog_sha256": AUTHORITY_ROLE_CATALOG_SHA256,
        "table_authority_count": TABLE_AUTHORITY_COUNT,
        "table_authority_catalog_sha256": TABLE_AUTHORITY_CATALOG_SHA256,
        "candidate_or_production_files_written": 0,
        "formal_credit": 0,
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**result, "verification_sha256": digest(result)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-replay-evidence", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--production-dir", type=Path)
    args = parser.parse_args()
    need(
        sum(
            (
                args.print_contract,
                args.self_test,
                args.verify_replay_evidence,
                args.candidate_dir is not None,
                args.production_dir is not None,
            )
        )
        == 1,
        "choose exactly one mode",
    )
    if args.print_contract:
        print(canonical(contract()).decode("ascii"))
    elif args.self_test:
        print(canonical(self_test()).decode("ascii"))
    elif args.verify_replay_evidence:
        try:
            print(canonical(verify_replay_evidence()).decode("ascii"))
        except ContractBlocked:
            raise SystemExit(1) from None
    elif args.candidate_dir is not None:
        try:
            build_private_candidate(args.candidate_dir)
        except ContractBlocked:
            raise SystemExit(1) from None
    else:
        assert args.production_dir is not None
        try:
            build_production_package(args.production_dir)
        except ContractBlocked:
            raise SystemExit(1) from None


if __name__ == "__main__":
    main()
