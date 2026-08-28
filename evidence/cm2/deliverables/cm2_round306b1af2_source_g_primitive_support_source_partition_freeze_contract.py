#!/usr/bin/env python3
"""Round306B1AF2 exact primitive-support source-partition freeze.

This zero-credit contract freezes a narrow result needed before a formal B1A
feature/support schema can be designed: every Round306B0 member is assigned,
exactly once, to the upstream primitive-support family from which its eventual
normalized support must be reconstructed or proved.

The partition is not a normalized-full-support proof.  It does not make the
824,864 typed theorem obligations into a complete feature ledger, does not
install a producer, and does not authorize a candidate or formal package.
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
import stat
import subprocess
import sys
import tempfile
from typing import Any, Callable, NoReturn
from unittest import mock


class ContractBlocked(RuntimeError):
    """Fail-closed partition-freeze violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ContractBlocked(label)


SCHEMA = "cm2.round306b1af2.source-g-primitive-support-source-partition-freeze.v1"
STATUS = (
    "PASS_ZERO_CREDIT_EXACT_PRIMITIVE_SOURCE_PARTITION__NORMALIZED_FULL_SUPPORT_"
    "TYPED_WIRE_AND_COMPLETE_CONSTRUCTION_ADMISSION_BLOCKED"
)
CANDIDATE_BLOCK_REASON = (
    "Round306B1AF2 freezes only a zero-credit source partition; candidate mode "
    "is blocked before every filesystem or output action"
)

# Filled only after the canonical document is finalized.  The validator checks
# this external-style literal instead of deriving an expectation from a second
# mutable copy of the document.
EXPECTED_CONTRACT_SHA256 = "ed4dfaf07636dfdc25a5c0b6ed3a4900b9091d684a0b272f804a34a001317cd5"

MEMBER_COUNT = 564_492
OCCURRENCE_MEMBER_COUNT = 431_208
VIRTUAL_MEMBER_COUNT = 133_284
FEATURE_OBLIGATION_COUNT = 824_864


PARTITION_INPUT_PINS = (
    (
        "Round306B0_MEMBER_SUPPORT_SOURCE_INDEX",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz",
        162_499_140,
        "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af",
    ),
    (
        "Round306B1R0_MEMBER_UNION",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz",
        123_019_951,
        "4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7",
    ),
    (
        "Round306B1G0_GRAPH_SHEET_JOIN",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz",
        13_922_080,
        "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3",
    ),
    (
        "Round306B1G0_GRAPH_SIDE_JOIN",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz",
        25_932_945,
        "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1",
    ),
    (
        "Round245_RETAINED_STRATUM_SOURCE",
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json",
        20_683_081,
        "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
    ),
    (
        "Round246_RETAINED_STRATUM_SOURCE",
        "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json",
        18_283_721,
        "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9",
    ),
    (
        "Round247_RETAINED_STRATUM_SOURCE",
        "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json",
        13_400_149,
        "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
    ),
    (
        "Round248_WALL_BULK_AND_SHEET_SOURCE",
        "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json",
        205_148_977,
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    ),
    (
        "Round266_EXPANDED_AND_VIRTUAL_FRONTIERS",
        "cm2_round266_source_g_expanded_curved_face_closure_certificate.json",
        934_776_249,
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    ),
    (
        "Round294_OCCURRENCE_REGISTRY",
        "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz",
        262_951_902,
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    ),
)

GOVERNANCE_PINS = (
    (
        "Round306B0_MANIFEST",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256",
        1_760,
        "9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269",
    ),
    (
        "Round306B0_RESULT",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json",
        9_450,
        "badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735",
    ),
    (
        "Round306B0_VERIFICATION",
        "cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json",
        7_003,
        "f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590",
    ),
    (
        "Round306B1R0_MANIFEST",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_manifest.sha256",
        1_571,
        "f23f4639629e920596e1ecadbb1cd7708f93308dc5780a0f82c196edc0f46aec",
    ),
    (
        "Round306B1R0_RESULT",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_result.json",
        3_019,
        "ca66501d42894dce364ff905045ae69f67cf52c9142ba8f7b45973f857966f04",
    ),
    (
        "Round306B1R0_VERIFICATION",
        "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_verification.json",
        11_531,
        "2242732077165e085f6f2e50f2d061a532a3b43d9e9bc0efc17afac3d45df040",
    ),
    (
        "Round306B1G0_MANIFEST",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256",
        1_959,
        "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8",
    ),
    (
        "Round306B1G0_RESULT",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_result.json",
        5_006,
        "3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e",
    ),
    (
        "Round306B1G0_VERIFICATION",
        "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_verification.json",
        11_575,
        "65b7a01fd82535f357dbb44b8c68a68c86afcbb75b1c1c9b9159b71f9815139a",
    ),
    (
        "Round306B1AF1_PRE_SCHEMA_ADMISSION",
        "cm2_round306b1af1_source_g_formal_full_feature_cover_pre_schema_admission_contract.py",
        30_391,
        "93d35ed11c98b3721f8ec24ec8c440278e5e947b8f5e63a7dbdc4b1d66380e39",
    ),
)


TABLE_COMMITMENTS = (
    (
        "Round306B0.member_support_source_rows",
        564_492,
        "87b4d34c40c3c1caf053ccb9b4c6c6c32cf6a33ac184f6181864105b500b6d3a",
        "382e7a7ae0e857b812635e0d4bb10571d1aa459a27acd178d81b12f9c68d6285",
        "c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5",
        "58ad4ebe98be5023f31870a0d0d3e0d135d153553393aa56a67f4ef1760f68a3",
    ),
    (
        "Round306B1R0.member_union_rows",
        295_336,
        "6c136186cd30608304293cc91185615ba6bec6418cb2c43a48ac833055c69bfe",
        "d106b9e68817aa9504ec176be9c679f2e4fd29948c3614f7c109030a893f289f",
        "6665fc8e72824fba7dbd1d1b7462ae419bb31c25149037da3183d74569b62a3d",
        "28c6e7944f440f9fee06f9ade150de2566a3aaa85b40c49d63e3721ec4a4c4c5",
    ),
    (
        "Round306B1G0.graph_sheet_join_rows",
        38_624,
        "b36ca314b15b8b8297dfeda9cb4fe37360ff20339e7603a6388ac172cfb87300",
        "a3c606a9ba302ced5593d941529946729da5d160a32384ca37060b20011a01f5",
        "9238a05af9a97002488576d3648ce06ee750858f156638c314ba2e0a24fe3e1f",
        "3686f3b90a77195dbecd08750707a32f98e07f9fdff5f59d57f09c1178a48fda",
    ),
    (
        "Round306B1G0.graph_side_join_rows",
        76_848,
        "9e2a2c015372aa22e5f2cfa1f11ae268496831b3118da5bd5087fc6d7f403f53",
        "2090d073d45f0097df68a60b36085786de0db51d76219b562734465bbf6daff6",
        "43ee8ffd2b77231c43c0af10198bbcc1f1def12f2e6bfd28f82c66ea26a207b2",
        "108bdcbe1c124de15d8f48f82a3cdb7aa545f6f61294be34e3e5b07979d6670e",
    ),
    (
        "Round245.formal_retained_stratum_node_ledger",
        3_664,
        "ef81a9a7d264961541edfb9ba9e8e4c37ddbf7dea01efa3eb72d500a82b44ed5",
        "86bad0d45642388bcac65633d47088b93184d77abdb2be68096cb139e192110c",
        "38583b1aa3f37e37dc03c2b59b2a31c18346462d3d918e001040d6651b11401b",
        None,
    ),
    (
        "Round246.formal_new_whole_signature_retained_stratum_node_ledger",
        2_220,
        "488711dda41780ef47dbe34834ab8e3a41995a471260d7743b562c0190b6c86f",
        "f43d31209c552f275144ede960e49bd1ee4044cb40ee3050340e23d6d38bc671",
        "476a4fe0955fd1672ba5ba1177e65f479bf10a2bfdb62d6443f3d702c1649414",
        None,
    ),
    (
        "Round247.formal_new_crossing_and_source_seam_retained_stratum_node_ledger",
        504,
        "8896ff95e8e1c4dd5eb7f53ce3dcf9f39abbcd883c2641846b69129fc7040143",
        "23e3495f9f481cc3f1d037741b27403d7bc4c0be8afe118201ba52a6fc4ce9a7",
        "737b59a2a4a9e67664b9e0a080034083190b67c614849bac9b87b5b4ecaf9629",
        None,
    ),
    (
        "Round248.formal_wall_positive_volume_bulk_ledger",
        88_936,
        "6106c39894a7947293934b0b061bcae04e1a2902976b63ccd1756d7790cb6154",
        "e46f242e15bcba4111e14aac3c1dc5d82a5350e9e1514f2b9f90cdbc853e525d",
        "aff5ea1401a6919529d1d54fe54bb9b8d378456fa48f88a75043505b5ee7b8b0",
        None,
    ),
    (
        "Round248.formal_wall_half_open_sheet_owner_ledger",
        38_360,
        "fbb15ef7122367925c72f9d0e396141d3f04a271b78064af41e1f68d9d06cd61",
        "be2e8b880f3a0c8fb833a7ba8dce0bd86d5526b400569377f0fcb66692a8c7e0",
        "e61754dc51732c4c82876d1c2e83fa040747d23253addd64350728169f5ae44b",
        None,
    ),
    (
        "Round266.formal_post_Round266_expanded_occurrence_frontier_ledger",
        126_468,
        "db01addd10a5112d56109695684d64994b927ce009e71b5e39dc95de2846acce",
        "08fa74d62a0673cb02339bae0df05007e7f4cb9d452d69feef79a958ceaa5ad9",
        "441cde017675dc279a55d52f47c24c31721309ad1cb03e1ea831e6984569f351",
        None,
    ),
    (
        "Round266.formal_post_Round266_valid_virtual_node_frontier_ledger",
        133_284,
        "2d42533f48f864f01e6bd4a46470e7266c1a2cec590380483cfb7cbfb84634f2",
        "9c31ba929e13eeaea29a9f6abe7cf324222eacb25d123a9b12252b386c12a32e",
        "8c394c1d1b2b42025c25a00ef24ecba748981ed93c75b9aba20ddf15ff8597d5",
        None,
    ),
    (
        "Round266.formal_post_Round266_component_member_frontier_ledger",
        259_752,
        "f064d177c25985b38c899c651923b83ba47ee36b465902cca85a4c21e0c33ca6",
        "1f28c84d14cf3fabb38d0f2d1fdf862ce8f6a4559552d68fd9c0a5bd0a3ed3ee",
        "28398acde446047ff4a210b2fa0831d2c44e3758f7e9239b5ec63cecc386b257",
        None,
    ),
    (
        "Round294.occurrence_registry_rows",
        431_208,
        "bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509",
        "ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56",
        "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
        None,
    ),
)

TABLE_LOCATORS = (
    ("Round306B0.member_support_source_rows", PARTITION_INPUT_PINS[0][1], ".member_support_source_rows", "Round306B0_member_support_source_row_id"),
    ("Round306B1R0.member_union_rows", PARTITION_INPUT_PINS[1][1], ".member_union_rows", "Round306B1R0_member_union_row_id"),
    ("Round306B1G0.graph_sheet_join_rows", PARTITION_INPUT_PINS[2][1], ".graph_sheet_join_rows", "Round306B1G0_graph_sheet_join_row_id"),
    ("Round306B1G0.graph_side_join_rows", PARTITION_INPUT_PINS[3][1], ".graph_side_join_rows", "Round306B1G0_graph_side_join_row_id"),
    ("Round245.formal_retained_stratum_node_ledger", PARTITION_INPUT_PINS[4][1], ".result.formal_retained_stratum_node_ledger.rows", "retained_stratum_node_id"),
    ("Round246.formal_new_whole_signature_retained_stratum_node_ledger", PARTITION_INPUT_PINS[5][1], ".result.formal_new_whole_signature_retained_stratum_node_ledger.rows", "retained_stratum_node_id"),
    ("Round247.formal_new_crossing_and_source_seam_retained_stratum_node_ledger", PARTITION_INPUT_PINS[6][1], ".result.formal_new_crossing_and_source_seam_retained_stratum_node_ledger.rows", "retained_stratum_node_id"),
    ("Round248.formal_wall_positive_volume_bulk_ledger", PARTITION_INPUT_PINS[7][1], ".result.formal_wall_positive_volume_bulk_ledger.rows", "wall_bulk_node_id"),
    ("Round248.formal_wall_half_open_sheet_owner_ledger", PARTITION_INPUT_PINS[7][1], ".result.formal_wall_half_open_sheet_owner_ledger.rows", "wall_sheet_node_id"),
    ("Round266.formal_post_Round266_expanded_occurrence_frontier_ledger", PARTITION_INPUT_PINS[8][1], ".result.formal_post_Round266_expanded_occurrence_frontier_ledger.rows", "post_Round266_expanded_occurrence_frontier_row_id"),
    ("Round266.formal_post_Round266_valid_virtual_node_frontier_ledger", PARTITION_INPUT_PINS[8][1], ".result.formal_post_Round266_valid_virtual_node_frontier_ledger.rows", "post_Round266_valid_virtual_node_frontier_row_id"),
    ("Round266.formal_post_Round266_component_member_frontier_ledger", PARTITION_INPUT_PINS[8][1], ".result.formal_post_Round266_component_member_frontier_ledger.rows", "post_Round266_component_member_frontier_row_id"),
    ("Round294.occurrence_registry_rows", PARTITION_INPUT_PINS[9][1], ".rows", "Round294_occurrence_registry_row_id"),
)

R294_OCCURRENCE_IDS_SHA256 = (
    "169869b5755eda22f1527e7393a5bef0a77a842eefbdf45ab34d315b0dad1936"
)

FINE_PARTITION = (
    ("PRESERVED_ROUND174_RESOLVED", 72_500),
    ("PRESERVED_ROUND179_RESOLVED", 17_192),
    ("PRESERVED_ROUND204_REGION", 736),
    ("PRESERVED_ROUND208_REGION", 36_040),
    ("R245_GRAPH_SHEET_REQUIRES_G2A_SUPPORT", 264),
    ("R245_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT", 528),
    ("R245_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION", 2_872),
    ("R246_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION", 2_220),
    ("R247_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION", 504),
    ("R248_GRAPH_SHEET_REQUIRES_G2A_SUPPORT", 38_360),
    ("R248_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT", 76_304),
    ("R248_NON_GRAPH_BULK_REQUIRES_SOURCE_SUPPORT_RECONSTRUCTION", 12_232),
    ("R288_DYNAMIC_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION", 274_176),
    ("R288_ISOLATED_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION", 21_160),
    ("R292_EXACT_T2PS_REFINEMENT_CELL_UNION", 9_404),
)

COARSE_PARTITION = (
    ("direct_preserved_source_geometry", 126_468),
    ("R2_predicate_union_members", 295_336),
    ("R292_transformed_cell_union_members", 9_404),
    ("G2a_graph_sheet_members", 38_624),
    ("G2b_graph_side_members", 76_832),
    ("non_graph_virtual_bulk_members", 17_828),
)

PARTITION_STREAM_SHA256 = (
    "36775c189e20ecdbc933572175954a62753bcd9c5515561fb13aab454d6caab3"
)
PARTITION_INPUT_PIN_SET_SHA256 = "5a42c479d0785794e67d6fa1d7dbeffad8d0fba41a7cbc22faf889ec02843966"
GOVERNANCE_PIN_SET_SHA256 = "d92859e956de57825dd026c04daa9c62e30b9a8d6f56efa074025f0636041c53"
TABLE_COMMITMENTS_SHA256 = "38bbb15e0d6885f3cb9a681f1b625adcf8dba608e6722edf4fea09220640dee8"
TABLE_LOCATORS_SHA256 = "8605cdcd72980733925931b9fa6904ac5e91a3ef98c755dae4494c5c50660de6"
PARTITION_ALGORITHM_SHA256 = "ad8cbb6907a4f6ee19e70c983f0df9cac83f0f6d54cb1b41d8e9868b2782acee"
REPLAY_RESULT_SHA256 = "2d311625d3aa2170aa508ff4a20259c31ac91ddc3c700d7c5ba95c11276205ba"

REPLAY_EVIDENCE_PINS = (
    (
        "PRIMARY_REPLAY_SOURCE",
        "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_replay.py",
        20_783,
        "b7fcae488bd1e9e301f7191e65ade22f87c393a083a1335147ccf1bc92cddb27",
    ),
    (
        "PRIMARY_REPLAY_RESULT",
        "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_result.json",
        2_540,
        "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb",
    ),
    (
        "INDEPENDENT_REPLAY_SOURCE",
        "cm2_round306b1af2_source_g_primitive_support_source_partition_independent_replay.py",
        23_694,
        "38551c822f9aa74989b54749a3e05e8fe9bdce205fb12efb12eaa7382e6ccab4",
    ),
    (
        "INDEPENDENT_REPLAY_RESULT",
        "cm2_round306b1af2_source_g_primitive_support_source_partition_independent_result.json",
        2_540,
        "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb",
    ),
)
REPLAY_EVIDENCE_PIN_SET_SHA256 = "075a2caa61bc5f5a58a6fcba1d5425ee02d98cf915e30e2a780ece9e99f35ace"


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def _pin_rows(pins: tuple[tuple[str, str, int, str], ...]) -> list[dict[str, Any]]:
    return [
        {"label": label, "filename": name, "exact_size": size, "sha256": sha}
        for label, name, size, sha in pins
    ]


def _table_rows() -> list[dict[str, Any]]:
    return [
        {
            "table": table,
            "row_count": count,
            "row_ids_sha256": row_ids,
            "row_hashes_sha256": row_hashes,
            "rows_sha256": rows,
            "ledger_sha256": ledger,
        }
        for table, count, row_ids, row_hashes, rows, ledger in TABLE_COMMITMENTS
    ]


def _table_locator_rows() -> list[dict[str, str]]:
    return [
        {
            "table": table,
            "input_filename": filename,
            "json_path": json_path,
            "row_id_field": row_id_field,
            "commitment_interpretation": (
                "opaque upstream canonical row/order commitment locked by exact file SHA; "
                "F2 replay independently reconstructs joins and its own assignment stream"
            ),
        }
        for table, filename, json_path, row_id_field in TABLE_LOCATORS
    ]


def _expected_replay_result() -> dict[str, Any]:
    return {
        "schema": "cm2.round306b1af2.source-g-primitive-support-source-partition.replay-result.v1",
        "input_pin_set_sha256": PARTITION_INPUT_PIN_SET_SHA256,
        "table_commitments_sha256": TABLE_COMMITMENTS_SHA256,
        "table_locators_sha256": TABLE_LOCATORS_SHA256,
        "partition_algorithm_sha256": PARTITION_ALGORITHM_SHA256,
        "status": "PASS_EXACT_564492_MEMBER_SOURCE_PARTITION__FORMAL_FULL_SUPPORT_NO_GO",
        "member_count": MEMBER_COUNT,
        "fine_partition": [
            {"family": family, "member_count": count}
            for family, count in FINE_PARTITION
        ],
        "coarse_partition": {family: count for family, count in COARSE_PARTITION},
        "G2b": {
            "reference_count": 76_848,
            "distinct_member_count": 76_832,
            "member_reference_multiplicity_histogram": {"1": 76_816, "2": 16},
        },
        "R2": {
            "predicate_cell_reference_count": 295_340,
            "distinct_member_count": 295_336,
            "member_cell_multiplicity_histogram": {"1": 295_332, "2": 4},
        },
        "partition_stream": {
            "order": "ROUND306B0_MEMBER_LEDGER_ORDER",
            "wire": "canonical_json([member_id,family])+LF",
            "sha256": PARTITION_STREAM_SHA256,
        },
        "R248_raw_virtual_count": 127_296,
        "R248_final_virtual_count": 126_896,
        "R248_raw_minus_final_virtual_count": 400,
        "formal_credit": 0,
    }


def _contract_document() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "candidate_is_formal": False,
        "claim_boundary": {
            "exact_claim": (
                "all 564492 Round306B0 members have exactly one frozen "
                "primitive-support source-family assignment"
            ),
            "partition_is_member_identity_exhaustive": True,
            "partition_is_normalized_full_support_proof": False,
            "partition_is_feature_definition_ledger": False,
            "partition_is_transition_atlas": False,
            "partition_is_pair_routing": False,
            "partition_may_grant_formal_consumability": False,
            "824864_is_typed_theorem_obligation_census": True,
            "824864_is_complete_feature_definition_count": False,
            "complete_feature_definition_count": None,
        },
        "input_freeze": {
            "partition_data_inputs": _pin_rows(PARTITION_INPUT_PINS),
            "partition_data_input_count": len(PARTITION_INPUT_PINS),
            "partition_data_input_bytes": sum(row[2] for row in PARTITION_INPUT_PINS),
            "partition_data_input_pin_set_sha256": PARTITION_INPUT_PIN_SET_SHA256,
            "governance_inputs": _pin_rows(GOVERNANCE_PINS),
            "governance_input_count": len(GOVERNANCE_PINS),
            "governance_input_pin_set_sha256": GOVERNANCE_PIN_SET_SHA256,
            "replay_evidence_inputs": _pin_rows(REPLAY_EVIDENCE_PINS),
            "replay_evidence_input_count": len(REPLAY_EVIDENCE_PINS),
            "replay_evidence_pin_set_sha256": REPLAY_EVIDENCE_PIN_SET_SHA256,
            "all_checked_input_bytes": sum(
                row[2]
                for row in PARTITION_INPUT_PINS + GOVERNANCE_PINS + REPLAY_EVIDENCE_PINS
            ),
            "consumed_table_commitments": _table_rows(),
            "consumed_table_commitments_sha256": TABLE_COMMITMENTS_SHA256,
            "consumed_table_locators": _table_locator_rows(),
            "consumed_table_locators_sha256": TABLE_LOCATORS_SHA256,
            "R294_occurrence_ids_sha256": R294_OCCURRENCE_IDS_SHA256,
            "declared_partition_source_byte_pin_set_complete": True,
            "partition_reconstruction_requires_replay_evidence": True,
            "input_set_complete_for_full_support_construction": False,
            "producer_authorized": False,
        },
        "partition_algorithm": {
            "algorithm_version": "ROUND306B1AF2_EXACT_SOURCE_PARTITION_V1",
            "iteration_order": "Round306B0.member_support_source_rows ledger order",
            "assignment_hash_domain": (
                "for each member exactly once: canonical_json([member_id,family]) "
                "encoded ASCII plus one LF"
            ),
            "canonical_json": (
                "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=True)"
            ),
            "R294_preserved_binding": (
                "B0 primary source row -> R294 row -> R266 expanded occurrence; "
                "member, source row id/hash, and geometry row id/hash all equal"
            ),
            "B0_primary_source_package_field": "primary_source_package",
            "B0_primary_source_package_enums": ["R266", "R294"],
            "R294_registry_entry_kind_field": "registry_entry_kind",
            "R294_registry_entry_kind_enums": [
                "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE",
                "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM",
                "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT",
            ],
            "R294_R288_support_representation_kind_field": "support_representation_kind",
            "R294_R288_support_representation_kind_to_family": {
                "ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR_INNER_SUPPORT":
                    "R288_DYNAMIC_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION",
                "ROUND290_ISOLATED_ATOM_RATIONAL_INNER_SUPPORT":
                    "R288_ISOLATED_ATOM_REQUIRES_R2_FULL_SUPPORT_UNION",
            },
            "R294_R292_support_representation_kind":
                "EXACT_T2_P_S_CONNECTED_UNCOVERED_REFINEMENT_CELL_UNION",
            "R294_R288_binding": (
                "R294 canonical atom support kind selects dynamic or isolated R2 family; "
                "R2 member set and B0 row backbindings are exact"
            ),
            "R294_R292_binding": (
                "R294 refined occurrence support kind is exact T2PS connected "
                "uncovered refinement-cell union"
            ),
            "R266_virtual_binding": (
                "B0 virtual member -> R266 component row -> R266 valid frontier -> "
                "exact R245/R246/R247/R248 row id/hash"
            ),
            "virtual_primitive_source_tables": {
                "R245": "Round245.formal_retained_stratum_node_ledger",
                "R246": "Round246.formal_new_whole_signature_retained_stratum_node_ledger",
                "R247": "Round247.formal_new_crossing_and_source_seam_retained_stratum_node_ledger",
                "R248_BULK": "Round248.formal_wall_positive_volume_bulk_ledger",
                "R248_SHEET": "Round248.formal_wall_half_open_sheet_owner_ledger",
            },
            "G2a_member_field": "sheet_member_id",
            "G2b_member_field": "side_member_id",
            "B0_backbinding_fields": [
                "Round306B0_member_support_source_row_id",
                "Round306B0_member_source_row_id",
            ],
            "graph_sheet_assignment": (
                "dimension-2 virtual member iff present exactly once in B1G0 G2a sheet join"
            ),
            "graph_side_assignment": (
                "positive-3D virtual member is graph-side iff present in B1G0 G2b side join"
            ),
            "non_graph_bulk_assignment": (
                "remaining positive-3D virtual members retain exact primitive source "
                "and require later full-support reconstruction"
            ),
            "all_B0_members_unique": True,
            "all_R294_occurrence_members_exhausted": True,
            "all_R266_valid_virtual_members_exhausted": True,
            "missing_or_orphan_or_duplicate_member_count": 0,
            "R292_family_label_is_source_representation_not_support_theorem": True,
        },
        "exact_partition": {
            "member_count": MEMBER_COUNT,
            "occurrence_member_count": OCCURRENCE_MEMBER_COUNT,
            "virtual_member_count": VIRTUAL_MEMBER_COUNT,
            "fine_family_count": len(FINE_PARTITION),
            "fine_partition": [
                {"family": family, "member_count": count}
                for family, count in FINE_PARTITION
            ],
            "coarse_partition": [
                {"family": family, "member_count": count}
                for family, count in COARSE_PARTITION
            ],
            "R266_preserved_source_histogram": {
                "ROUND174_RESOLVED": 72_500,
                "ROUND179_RESOLVED": 17_192,
                "ROUND204_REGION": 736,
                "ROUND208_REGION": 36_040,
            },
            "R2_cell_reference_count": 295_340,
            "R2_distinct_member_count": 295_336,
            "R2_member_cell_multiplicity_histogram": {"1": 295_332, "2": 4},
            "G2a_sheet_reference_and_distinct_member_count": 38_624,
            "G2b_reference_count": 76_848,
            "G2b_distinct_member_count": 76_832,
            "G2b_member_reference_multiplicity_histogram": {"1": 76_816, "2": 16},
            "G2b_family_reference_histogram": {
                "R235_SINGLE_ENDPOINT_GRAPH": 76_256,
                "R236_DOUBLE_ENDPOINT_GRAPH": 64,
                "R242_UNIQUE_TRANSITION_GRAPH": 528,
            },
            "R245_G2b_distinct_member_count": 528,
            "R248_G2b_distinct_member_count": 76_304,
            "all_G2b_distinct_members_are_not_76304": True,
            "R248_raw_virtual_count": 127_296,
            "R248_final_virtual_count": 126_896,
            "R248_raw_minus_final_virtual_count": 400,
            "R264_empty_bulk_causation_claimed_by_F2": False,
            "partition_stream_sha256": PARTITION_STREAM_SHA256,
            "replay_result_sha256": REPLAY_RESULT_SHA256,
        },
        "independent_replay": {
            "required": True,
            "completed": True,
            "implementation_independent_from_primary_probe": True,
            "primary_source_filename": REPLAY_EVIDENCE_PINS[0][1],
            "primary_source_sha256": REPLAY_EVIDENCE_PINS[0][3],
            "primary_result_filename": REPLAY_EVIDENCE_PINS[1][1],
            "primary_result_file_sha256": REPLAY_EVIDENCE_PINS[1][3],
            "independent_source_filename": REPLAY_EVIDENCE_PINS[2][1],
            "independent_source_sha256": REPLAY_EVIDENCE_PINS[2][3],
            "independent_result_filename": REPLAY_EVIDENCE_PINS[3][1],
            "independent_result_file_sha256": REPLAY_EVIDENCE_PINS[3][3],
            "source_sha256_values_are_distinct": True,
            "result_files_are_byte_identical": True,
            "canonical_result": _expected_replay_result(),
            "canonical_result_sha256": REPLAY_RESULT_SHA256,
            "input_pin_set_sha256_match": True,
            "table_commitments_sha256_match": True,
            "table_locators_sha256_match": True,
            "partition_algorithm_sha256_match": True,
            "exact_counts_match": True,
            "fine_partition_match": True,
            "coarse_partition_match": True,
            "partition_stream_sha256_match": True,
            "external_source_hash_required_before_freeze_claim": True,
        },
        "schema_consequences": {
            "inline_member_support_source_handles_structurally_exhaustive": True,
            "member_cover_schema_may_omit_source_family": False,
            "member_cover_schema_may_treat_source_handle_as_full_support": False,
            "feature_obligation_count": FEATURE_OBLIGATION_COUNT,
            "feature_obligation_count_may_be_used_as_complete_feature_ledger_count": False,
            "normalized_support_AST_grammar_frozen": False,
            "R2_union_equivalence_certificate_frozen": False,
            "G2a_G2b_physical_support_certificate_frozen": False,
            "direct_source_geometry_equivalence_frozen": False,
            "non_graph_bulk_full_support_reconstruction_frozen": False,
            "family_discriminated_wire_schema_frozen": False,
            "formal_B1A_schema_admitted": False,
        },
        "remaining_closure_order": [
            "externally freeze and independently audit the final F2 source bytes",
            "freeze complete full-support construction sources and their authority pins",
            "reconstruct direct preserved and 17828 non-graph bulk normalized supports",
            "prove R2 union and G2a/G2b physical-support equivalence",
            "freeze typed support AST certificate member representation and transition-handle schemas",
            "freeze ledger result verification attack manifest wire and publication schemas",
            "issue independently audited B1A implementable schema",
            "only then implement two byte-identical private candidates and independent promotion",
        ],
        "candidate_mode": {
            "enabled": False,
            "block_before_any_path_inspection": True,
            "block_before_any_input_open": True,
            "block_before_any_temp_or_directory_creation": True,
            "block_before_any_output_or_metadata_write": True,
            "candidate_files": [],
        },
        "formal_credit": {
            "feature_definition": 0,
            "member_support": 0,
            "representation_cover": 0,
            "transition": 0,
            "pair_routing": 0,
            "component_union": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "D02": "BLOCKED",
            "D03": "NOT_REACHED",
            "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "emission_accounting": {
            "feature_rows_emitted": 0,
            "member_rows_emitted": 0,
            "representation_rows_emitted": 0,
            "candidate_files_written": 0,
            "formal_files_written": 0,
        },
    }


def validate_contract(document: dict[str, Any]) -> None:
    need(document.get("schema") == SCHEMA, "schema")
    need(document.get("status") == STATUS, "status")
    need(digest(document) == EXPECTED_CONTRACT_SHA256, "canonical contract digest")
    exact = document["exact_partition"]
    frozen_input = document["input_freeze"]
    need(digest(_pin_rows(PARTITION_INPUT_PINS)) == PARTITION_INPUT_PIN_SET_SHA256, "partition input pin-set digest")
    need(digest(_pin_rows(GOVERNANCE_PINS)) == GOVERNANCE_PIN_SET_SHA256, "governance pin-set digest")
    need(digest(_table_rows()) == TABLE_COMMITMENTS_SHA256, "table commitment-set digest")
    need(digest(_table_locator_rows()) == TABLE_LOCATORS_SHA256, "table locator-set digest")
    need(digest(_pin_rows(REPLAY_EVIDENCE_PINS)) == REPLAY_EVIDENCE_PIN_SET_SHA256, "replay evidence pin-set digest")
    need(digest(document["partition_algorithm"]) == PARTITION_ALGORITHM_SHA256, "partition algorithm digest")
    need(frozen_input["partition_data_input_pin_set_sha256"] == PARTITION_INPUT_PIN_SET_SHA256, "document partition pin digest")
    need(frozen_input["governance_input_pin_set_sha256"] == GOVERNANCE_PIN_SET_SHA256, "document governance pin digest")
    need(frozen_input["consumed_table_commitments_sha256"] == TABLE_COMMITMENTS_SHA256, "document table digest")
    need(frozen_input["consumed_table_locators_sha256"] == TABLE_LOCATORS_SHA256, "document locator digest")
    need(frozen_input["replay_evidence_pin_set_sha256"] == REPLAY_EVIDENCE_PIN_SET_SHA256, "document replay evidence digest")
    need(sum(row["member_count"] for row in exact["fine_partition"]) == MEMBER_COUNT, "fine member sum")
    need(sum(row["member_count"] for row in exact["coarse_partition"]) == MEMBER_COUNT, "coarse member sum")
    need(exact["occurrence_member_count"] + exact["virtual_member_count"] == MEMBER_COUNT, "B0 tranche sum")
    need(exact["R2_cell_reference_count"] == 295_340, "R2 references")
    need(exact["R2_distinct_member_count"] == 295_336, "R2 members")
    need(exact["G2b_reference_count"] == 76_848, "G2b references")
    need(exact["G2b_distinct_member_count"] == 76_832, "G2b distinct members")
    need(exact["R245_G2b_distinct_member_count"] + exact["R248_G2b_distinct_member_count"] == 76_832, "G2b source split")
    need(exact["fine_partition"] == [{"family": family, "member_count": count} for family, count in FINE_PARTITION], "exact fine partition")
    need(exact["coarse_partition"] == [{"family": family, "member_count": count} for family, count in COARSE_PARTITION], "exact coarse partition")
    fine = {row["family"]: row["member_count"] for row in exact["fine_partition"]}
    coarse = {row["family"]: row["member_count"] for row in exact["coarse_partition"]}
    need(sum(value for key, value in fine.items() if key.startswith("PRESERVED_")) == coarse["direct_preserved_source_geometry"], "preserved coarse equation")
    need(sum(value for key, value in fine.items() if key.startswith("R288_")) == coarse["R2_predicate_union_members"], "R2 coarse equation")
    need(fine["R292_EXACT_T2PS_REFINEMENT_CELL_UNION"] == coarse["R292_transformed_cell_union_members"], "R292 coarse equation")
    need(fine["R245_GRAPH_SHEET_REQUIRES_G2A_SUPPORT"] + fine["R248_GRAPH_SHEET_REQUIRES_G2A_SUPPORT"] == coarse["G2a_graph_sheet_members"], "G2a coarse equation")
    need(fine["R245_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT"] + fine["R248_GRAPH_SIDE_MEMBER_REQUIRES_G2B_SUPPORT"] == coarse["G2b_graph_side_members"], "G2b coarse equation")
    need(sum(value for key, value in fine.items() if "NON_GRAPH_BULK" in key) == coarse["non_graph_virtual_bulk_members"], "bulk coarse equation")
    need(exact["R2_member_cell_multiplicity_histogram"] == {"1": 295_332, "2": 4}, "R2 multiplicity")
    need(sum(exact["R2_member_cell_multiplicity_histogram"].values()) == exact["R2_distinct_member_count"], "R2 distinct equation")
    need(sum(int(key) * value for key, value in exact["R2_member_cell_multiplicity_histogram"].items()) == exact["R2_cell_reference_count"], "R2 multiplicity equation")
    need(exact["G2b_member_reference_multiplicity_histogram"] == {"1": 76_816, "2": 16}, "G2b multiplicity")
    need(sum(exact["G2b_member_reference_multiplicity_histogram"].values()) == exact["G2b_distinct_member_count"], "G2b distinct equation")
    need(sum(int(key) * value for key, value in exact["G2b_member_reference_multiplicity_histogram"].items()) == exact["G2b_reference_count"], "G2b multiplicity equation")
    need(sum(exact["G2b_family_reference_histogram"].values()) == exact["G2b_reference_count"], "G2b family reference equation")
    need(exact["R248_raw_virtual_count"] - exact["R248_raw_minus_final_virtual_count"] == exact["R248_final_virtual_count"], "R248 raw/final equation")
    need(exact["R264_empty_bulk_causation_claimed_by_F2"] is False, "no unpinned R264 causation")
    replay = document["independent_replay"]
    need(replay["required"] is True and replay["completed"] is True, "independent replay completed")
    need(replay["implementation_independent_from_primary_probe"] is True, "independent implementation")
    need((replay["primary_source_filename"], replay["primary_source_sha256"]) == (REPLAY_EVIDENCE_PINS[0][1], REPLAY_EVIDENCE_PINS[0][3]), "primary replay source pin")
    need((replay["primary_result_filename"], replay["primary_result_file_sha256"]) == (REPLAY_EVIDENCE_PINS[1][1], REPLAY_EVIDENCE_PINS[1][3]), "primary replay result pin")
    need((replay["independent_source_filename"], replay["independent_source_sha256"]) == (REPLAY_EVIDENCE_PINS[2][1], REPLAY_EVIDENCE_PINS[2][3]), "independent replay source pin")
    need((replay["independent_result_filename"], replay["independent_result_file_sha256"]) == (REPLAY_EVIDENCE_PINS[3][1], REPLAY_EVIDENCE_PINS[3][3]), "independent replay result pin")
    need(replay["primary_source_sha256"] != replay["independent_source_sha256"], "distinct replay source identities")
    need(replay["source_sha256_values_are_distinct"] is True, "distinct source marker")
    need(replay["primary_result_file_sha256"] == replay["independent_result_file_sha256"] == REPLAY_EVIDENCE_PINS[1][3], "byte-identical result hashes")
    need(replay["result_files_are_byte_identical"] is True, "byte-identical result marker")
    need(replay["canonical_result"] == _expected_replay_result(), "exact replay result")
    need(replay["canonical_result_sha256"] == digest(replay["canonical_result"]) == REPLAY_RESULT_SHA256, "replay result digest")
    for gate in (
        "input_pin_set_sha256_match",
        "table_commitments_sha256_match",
        "table_locators_sha256_match",
        "partition_algorithm_sha256_match",
        "exact_counts_match",
        "fine_partition_match",
        "coarse_partition_match",
        "partition_stream_sha256_match",
    ):
        need(replay[gate] is True, "replay gate:" + gate)
    need(document["claim_boundary"]["partition_is_normalized_full_support_proof"] is False, "no full-support claim")
    need(document["schema_consequences"]["formal_B1A_schema_admitted"] is False, "schema blocked")
    need(document["input_freeze"]["producer_authorized"] is False, "producer blocked")
    need(document["candidate_mode"]["enabled"] is False, "candidate blocked")
    need(all(value == 0 for key, value in document["formal_credit"].items() if key not in {"D02", "D03", "D04", "CM2"}), "zero credit")
    need(document["formal_credit"]["D02"] == "BLOCKED", "D02")
    need(document["formal_credit"]["CM2"] == "NO-GO_FOR_CLAIM", "CM2")


def contract() -> dict[str, Any]:
    document = _contract_document()
    validate_contract(document)
    return document


def _fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_uid,
        value.st_gid,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def _open_and_hash_at(
    directory_fd: int, filename: str, expected_size: int
) -> tuple[str, int, tuple[int, ...]]:
    need("/" not in filename and filename not in {"", ".", ".."}, "simple filename")
    before = os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)
    need(stat.S_ISREG(before.st_mode), "regular input:" + filename)
    need(before.st_nlink == 1, "single-link input:" + filename)
    need(before.st_size == expected_size, "exact input size:" + filename)
    descriptor = os.open(
        filename,
        os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
        dir_fd=directory_fd,
    )
    try:
        opened = os.fstat(descriptor)
        need(_fingerprint(opened) == _fingerprint(before), "input open binding:" + filename)
        state = hashlib.sha256()
        total = 0
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= expected_size, "bounded input read:" + filename)
            state.update(block)
        after_fd = os.fstat(descriptor)
        after_name = os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)
        need(total == expected_size, "complete input read:" + filename)
        need(_fingerprint(after_fd) == _fingerprint(opened), "stable input fd:" + filename)
        need(_fingerprint(after_name) == _fingerprint(opened), "final pathname rebind:" + filename)
        return state.hexdigest(), descriptor, _fingerprint(opened)
    except BaseException:
        os.close(descriptor)
        raise


def verify_partition_inputs() -> dict[str, Any]:
    data = Path(__file__).absolute().parent
    before = os.stat(data, follow_symlinks=False)
    need(stat.S_ISDIR(before.st_mode), "deliverables directory")
    directory_fd = os.open(
        data, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    )
    opened: list[tuple[str, int, tuple[int, ...]]] = []
    checked: list[dict[str, Any]] = []
    try:
        directory_fingerprint = _fingerprint(before)
        need(_fingerprint(os.fstat(directory_fd)) == directory_fingerprint, "dirfd binding")
        for label, filename, size, expected_sha in (
            PARTITION_INPUT_PINS + GOVERNANCE_PINS + REPLAY_EVIDENCE_PINS
        ):
            actual, descriptor, opened_fingerprint = _open_and_hash_at(
                directory_fd, filename, size
            )
            opened.append((filename, descriptor, opened_fingerprint))
            need(actual == expected_sha, "input hash:" + filename)
            checked.append({"label": label, "filename": filename, "exact_size": size, "sha256": actual})
        for filename, descriptor, opened_fingerprint in opened:
            need(_fingerprint(os.fstat(descriptor)) == opened_fingerprint, "held fd unchanged:" + filename)
            need(_fingerprint(os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)) == opened_fingerprint, "held pathname rebound:" + filename)
        need(_fingerprint(os.stat(data, follow_symlinks=False)) == directory_fingerprint, "directory pathname unchanged")
        need(_fingerprint(os.fstat(directory_fd)) == directory_fingerprint, "directory fd unchanged")
    finally:
        for _filename, descriptor, _opened_fingerprint in reversed(opened):
            os.close(descriptor)
        os.close(directory_fd)
    result = {
        "schema": SCHEMA + ".input-verification.v1",
        "status": "PASS_EXACT_PARTITION_GOVERNANCE_AND_REPLAY_EVIDENCE_BYTE_PINS__NO_FULL_SUPPORT_ADMISSION",
        "checked_file_count": len(checked),
        "checked_byte_count": sum(
            row[2]
            for row in PARTITION_INPUT_PINS + GOVERNANCE_PINS + REPLAY_EVIDENCE_PINS
        ),
        "checked_rows_sha256": digest(checked),
        "proof_scope": "COMMON_HELD_FD_INTERVAL_BETWEEN_LAST_READ_AND_FIRST_FINAL_RECHECK_ONLY",
        "input_paths_claimed_immutable_after_return": False,
        "declared_partition_source_byte_pin_set_complete": True,
        "partition_reconstruction_performed_by_this_mode": False,
        "full_support_construction_set_complete": False,
        "candidate_or_formal_files_written": 0,
    }
    return {**result, "verification_sha256": digest(result)}


def build_private_candidate(_candidate: Path) -> NoReturn:
    raise ContractBlocked(CANDIDATE_BLOCK_REASON)


def _set_path(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: Any = document
    for item in path[:-1]:
        cursor = cursor[item]
    cursor[path[-1]] = value


def _mutation_suite() -> tuple[int, int]:
    attacks: tuple[tuple[tuple[Any, ...], Any], ...] = (
        (("status",), "PASS_FORMAL"),
        (("candidate_is_formal",), True),
        (("claim_boundary", "partition_is_normalized_full_support_proof"), True),
        (("claim_boundary", "824864_is_complete_feature_definition_count"), True),
        (("input_freeze", "input_set_complete_for_full_support_construction"), True),
        (("input_freeze", "producer_authorized"), True),
        (("partition_algorithm", "all_B0_members_unique"), False),
        (("partition_algorithm", "missing_or_orphan_or_duplicate_member_count"), 1),
        (("exact_partition", "member_count"), MEMBER_COUNT - 1),
        (("exact_partition", "fine_partition", 0, "member_count"), 72_499),
        (("exact_partition", "R2_cell_reference_count"), 295_336),
        (("exact_partition", "G2b_reference_count"), 76_832),
        (("exact_partition", "G2b_distinct_member_count"), 76_304),
        (("exact_partition", "all_G2b_distinct_members_are_not_76304"), False),
        (("exact_partition", "partition_stream_sha256"), "0" * 64),
        (("independent_replay", "completed"), False),
        (("independent_replay", "implementation_independent_from_primary_probe"), False),
        (("independent_replay", "source_sha256_values_are_distinct"), False),
        (("independent_replay", "result_files_are_byte_identical"), False),
        (("independent_replay", "canonical_result_sha256"), "0" * 64),
        (("independent_replay", "exact_counts_match"), False),
        (("independent_replay", "partition_stream_sha256_match"), False),
        (("schema_consequences", "member_cover_schema_may_treat_source_handle_as_full_support"), True),
        (("schema_consequences", "formal_B1A_schema_admitted"), True),
        (("remaining_closure_order", 0), "implement candidate now"),
        (("candidate_mode", "enabled"), True),
        (("candidate_mode", "block_before_any_path_inspection"), False),
        (("candidate_mode", "candidate_files"), ["forbidden"]),
        (("formal_credit", "member_support"), 1),
        (("formal_credit", "transition"), 1),
        (("formal_credit", "D02"), "PASS"),
        (("formal_credit", "CM2"), "GO"),
        (("emission_accounting", "candidate_files_written"), 1),
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


def _candidate_boundary_probe() -> dict[str, Any]:
    calls: dict[str, int] = {}

    def touched(name: str) -> Callable[..., Any]:
        calls[name] = 0

        def inner(*_args: Any, **_kwargs: Any) -> Any:
            calls[name] += 1
            raise AssertionError("candidate boundary crossed:" + name)
        return inner

    os_names = (
        "stat", "lstat", "fstat", "open", "fdopen", "read", "write", "listdir",
        "scandir", "walk", "mkdir", "makedirs", "link", "symlink", "readlink",
        "rename", "replace", "unlink", "remove", "chmod", "fchmod", "chown",
        "truncate", "ftruncate", "utime", "fsync", "access", "mkfifo", "mknod",
        "rmdir", "chdir", "system",
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
            build_private_candidate(Path("/forbidden"))
        except ContractBlocked as error:
            blocked = str(error) == CANDIDATE_BLOCK_REASON
    need(blocked, "candidate block reason")
    need(all(value == 0 for value in calls.values()), "candidate pre-filesystem boundary")
    return {
        "blocked": True,
        "patched_operation_count": len(calls),
        "observed_operation_count": sum(calls.values()),
    }


def self_test() -> dict[str, Any]:
    document = contract()
    code = build_private_candidate.__code__
    need(code.co_argcount == 1, "candidate entry arity")
    need(code.co_names == ("ContractBlocked", "CANDIDATE_BLOCK_REASON"), "candidate entry globals")
    need(code.co_consts == (None,), "candidate entry constants")
    need(
        code.co_code.hex()
        == "97007401000000000000000074020000000000000000ab010000000000008201",
        "candidate entry bytecode",
    )
    rejected, total = _mutation_suite()
    need(rejected == total, "all document mutations rejected")
    boundary = _candidate_boundary_probe()
    result = {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS_ZERO_CREDIT_PARTITION_FREEZE_DOCUMENT_AND_CANDIDATE_BOUNDARY_TEST",
        "contract_sha256": digest(document),
        "semantic_mutations_rejected": rejected,
        "semantic_mutation_count": total,
        "candidate_boundary_probe": boundary,
        "partition_or_construction_inputs_opened": 0,
        "candidate_or_formal_files_written": 0,
        "formal_credit": 0,
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**result, "self_test_sha256": digest(result)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-partition-inputs", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    args = parser.parse_args()
    need(
        sum((
            args.print_contract,
            args.self_test,
            args.verify_partition_inputs,
            args.candidate_dir is not None,
        )) == 1,
        "choose exactly one mode",
    )
    if args.print_contract:
        print(canonical(contract()).decode("ascii"))
    elif args.self_test:
        print(canonical(self_test()).decode("ascii"))
    elif args.verify_partition_inputs:
        print(canonical(verify_partition_inputs()).decode("ascii"))
    else:
        assert args.candidate_dir is not None
        try:
            build_private_candidate(args.candidate_dir)
        except ContractBlocked:
            raise SystemExit(1) from None


if __name__ == "__main__":
    main()
