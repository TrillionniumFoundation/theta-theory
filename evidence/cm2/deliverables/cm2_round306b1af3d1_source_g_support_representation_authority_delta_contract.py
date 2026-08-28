#!/usr/bin/env python3
"""Round306B1AF3D1 zero-credit support/representation authority delta.

This module is deliberately a sealed, non-producing contract.  It adds seven
stored-order table authorities to the immutable AF3 authority frontier and
pins the missing Round286/Round295A governance bytes.  It does not construct a
support candidate, define a typed support AST, prove a pullback, or mint any
formal credit.
"""

from __future__ import annotations

import argparse
import builtins
from contextlib import ExitStack
from copy import deepcopy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from typing import Any, Callable, NoReturn
from unittest import mock


SCHEMA = "cm2.round306b1af3d1.source-g-support-representation-authority-delta.v1"
STATUS = (
    "PASS_SEALED_ZERO_CREDIT_SUPPORT_REPRESENTATION_AUTHORITY_DELTA__"
    "AF3_IMMUTABLE__FORMAL_B1A_AND_B2_BLOCKED"
)
CANDIDATE_BLOCK_REASON = (
    "Round306B1AF3D1 is an authority-delta contract; candidate mode is "
    "blocked before path lstat/open/temp/write/output"
)
PRODUCTION_BLOCK_REASON = (
    "Round306B1AF3D1 is non-production; production mode is blocked before "
    "path lstat/open/temp/write/output"
)


class ContractBlocked(RuntimeError):
    """Fail-closed contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ContractBlocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sequence_digest(values: Any) -> str:
    """Digest a JSON sequence without materialising its full wire image."""
    state = hashlib.sha256()
    state.update(b"[")
    first = True
    for value in values:
        if not first:
            state.update(b",")
        state.update(canonical(value))
        first = False
    state.update(b"]")
    return state.hexdigest()


AF3_SOURCE_FILENAME = (
    "cm2_round306b1af3_source_g_full_support_construction_source_"
    "authority_frontier_freeze_contract.py"
)
AF3_SOURCE_SIZE = 132_027
AF3_SOURCE_SHA256 = "b01098600a09988142aa3554a20cb4e5b73aa6da13281324f45c3da822c9be42"
AF3_SCHEMA = (
    "cm2.round306b1af3.source-g-full-support-construction-source-"
    "authority-frontier-freeze.v1"
)
AF3_STATUS = (
    "PASS_ZERO_CREDIT_EXACT_FULL_SUPPORT_CONSTRUCTION_SOURCE_AUTHORITY_"
    "FRONTIER_FREEZE__ANALYTIC_AST_AND_FORMAL_B1A_BLOCKED"
)
AF3_CANONICAL_DOCUMENT_SIZE = 107_560
AF3_CANONICAL_DOCUMENT_SHA256 = (
    "959c9e314e86585e73ad4bcb09a536f38d1d53b6ce8acfbcf2ebdc0cc00109d4"
)
AF3_PRINTED_STDOUT_SIZE = 107_561
AF3_PRINTED_STDOUT_SHA256 = (
    "4703bc14896fa1a68a205282b5309d38b3b5773e03d1db1dcfa54f9913640cfa"
)
AF3_AUTHORITY_FILE_COUNT = 45
AF3_AUTHORITY_FILE_BYTES = 4_665_362_689
AF3_AUTHORITY_FILE_CATALOG_SHA256 = (
    "13993a345ec98b14d84faf6db8d29c1f5e23dbfbc1ae47e44798adea931caa0a"
)
AF3_AUTHORITY_ROLE_CATALOG_SHA256 = (
    "807e5502f5329577fc6f3c823bf835879c637f4b083fd417ff69e27cc3190117"
)
AF3_TABLE_AUTHORITY_COUNT = 82
AF3_TABLE_AUTHORITY_CATALOG_SHA256 = (
    "a49a38afbea65b5a8e837bc4932328447ad0ee553f18596cdff5ea788a879678"
)
AF3_INVENTORY_ROWS_SHA256 = (
    "40d971a646e59ffbc6854913c1c9dbc831253ba80d00451f79524fd371c8097a"
)
AF3_TRANSITIVE_FILE_COUNT = 143
AF3_TRANSITIVE_FILE_BYTES = 3_201_364_049
AF3_REPLAY_RESULT_SHA256 = (
    "5b9a4ba7920fb4fc98615fa9b69fb3dd6e4201ef76c4d2005fde6f85e777071f"
)
AF3_REPLAY_RESULT_SCHEMA = (
    "cm2.round306b1af3.source-g-full-support-construction-source-"
    "authority-frontier.replay-result.v1"
)


# label, filename, exact size, SHA-256, pin origin, purpose
FILE_PINS: tuple[tuple[str, str, int, str, str, str], ...] = (
    (
        "AF3_FINAL_CONTRACT_SOURCE",
        AF3_SOURCE_FILENAME,
        AF3_SOURCE_SIZE,
        AF3_SOURCE_SHA256,
        "AF3_FINAL_SOURCE",
        "IMMUTABLE_UPSTREAM_CONTRACT",
    ),
    (
        "AF3_PRIMARY_REPLAY_SOURCE",
        "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_primary_replay.py",
        183_616,
        "aaa14995ef822be78cff1abe7ee7d0c4592f6fc98624b7ad664139b22af6dba2",
        "AF3_REPLAY_EVIDENCE",
        "IMMUTABLE_UPSTREAM_REPLAY",
    ),
    (
        "AF3_PRIMARY_REPLAY_RESULT",
        "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_primary_replay_result.json",
        198_283,
        AF3_REPLAY_RESULT_SHA256,
        "AF3_REPLAY_EVIDENCE",
        "IMMUTABLE_UPSTREAM_REPLAY_RESULT",
    ),
    (
        "AF3_INDEPENDENT_REPLAY_SOURCE",
        "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_independent_replay.py",
        213_098,
        "128d5e8b4689f041292ff2f342115b1cd583c5bc1d395cd9fda36eb4f2e33215",
        "AF3_REPLAY_EVIDENCE",
        "IMMUTABLE_UPSTREAM_REPLAY",
    ),
    (
        "AF3_INDEPENDENT_REPLAY_RESULT",
        "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_independent_replay_result.json",
        198_283,
        AF3_REPLAY_RESULT_SHA256,
        "AF3_REPLAY_EVIDENCE",
        "IMMUTABLE_UPSTREAM_REPLAY_RESULT",
    ),
    (
        "R179_ROWS",
        "cm2_round179_source_g_residual_tube_arrangement_rows.json",
        131_273_924,
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
        "AF3_AUTHORITY_INHERITED",
        "TABLE_SOURCE",
    ),
    (
        "R236_CERTIFICATE",
        "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json",
        2_061_199,
        "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
        "AF3_AUTHORITY_INHERITED",
        "TABLE_SOURCE",
    ),
    (
        "R242_CERTIFICATE",
        "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json",
        13_734_655,
        "8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e",
        "AF3_AUTHORITY_INHERITED",
        "TABLE_SOURCE",
    ),
    (
        "R245_CERTIFICATE",
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json",
        20_683_081,
        "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
        "AF3_AUTHORITY_INHERITED",
        "TABLE_SOURCE",
    ),
    (
        "R286_PRODUCER_SOURCE",
        "cm2_round286_source_g_partial_overlap_exact_refinement_probe.py",
        7_977,
        "2fa6a547f3bad0432f77b5fba75069c3599fcef2234b0f9d19547297ea670088",
        "AF3D1_DIRECT_GOVERNANCE_DELTA",
        "PROVENANCE_SOURCE",
    ),
    (
        "R286_REFINEMENT_LEDGER",
        "cm2_round286_source_g_partial_overlap_exact_refinement_probe_ledger.json.gz",
        1_617_322,
        "bb7e28cbe029e2bb414313ec4a08f6366acbbad88a519926ec2a3a424e679eda",
        "AF3_CLOSURE_INHERITED",
        "TABLE_SOURCE",
    ),
    (
        "R286_RESULT",
        "cm2_round286_source_g_partial_overlap_exact_refinement_probe_result.json",
        2_642,
        "a3b705c489eff9df4e1129bcdf960c6ea9de435e326c1d7e040e01d63352d29e",
        "AF3_CLOSURE_INHERITED",
        "SEALED_RESULT",
    ),
    (
        "R286_VERIFIER_SOURCE",
        "cm2_round286_source_g_partial_overlap_exact_refinement_probe_verifier.py",
        38_997,
        "4861302c8f3bb85ab32ddb8fecd54603a894c110ad8dfe88dcb47c7528facc65",
        "AF3D1_DIRECT_GOVERNANCE_DELTA",
        "INDEPENDENT_VERIFIER_SOURCE",
    ),
    (
        "R286_VERIFICATION",
        "cm2_round286_source_g_partial_overlap_exact_refinement_probe_verification.json",
        4_931,
        "817a212eeac8d855927a617dd07462747c636127e4f4b15ec709f9975a74698e",
        "AF3_CLOSURE_INHERITED",
        "INDEPENDENT_VERIFICATION",
    ),
    (
        "R286_MANIFEST",
        "cm2_round286_source_g_partial_overlap_exact_refinement_probe_manifest.sha256",
        832,
        "7751adc49c1263092e4f33841b66d93aabd6a6f3d033ef68ed95e8cbc4856ddc",
        "AF3D1_DIRECT_GOVERNANCE_DELTA",
        "SEALED_MANIFEST",
    ),
    (
        "R295A_PRODUCER_SOURCE",
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure.py",
        55_309,
        "d147b6299a5e37b0e2ec104af64920e9b61f8a00491eb616b6a0e0eed66d6d08",
        "AF3_ROOT_CLOSURE_INHERITED",
        "EXPLICIT_PRODUCER_CROSS_PIN",
    ),
    (
        "R295A_ALIAS_LEDGER",
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz",
        118_612,
        "5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f",
        "AF3D1_DIRECT_GOVERNANCE_DELTA",
        "TABLE_SOURCE",
    ),
    (
        "R295A_RESULT",
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_result.json",
        9_158,
        "0deb8b9c88595762df3844b988af777a6b5f55347acbb8b9e8784308c2d4381d",
        "AF3D1_DIRECT_GOVERNANCE_DELTA",
        "SEALED_RESULT",
    ),
    (
        "R295A_VERIFIER_SOURCE",
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_verifier.py",
        90_604,
        "fabfb91c8aa1245716066594e5cf3c7e09fe43bdd199f662022eeda38eafb55a",
        "AF3D1_DIRECT_GOVERNANCE_DELTA",
        "INDEPENDENT_VERIFIER_SOURCE",
    ),
    (
        "R295A_VERIFICATION",
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_verification.json",
        5_813,
        "1b5c3423ea3854a8ae206677c740f31f5f9133edf66926271a10eec96b052349",
        "AF3D1_DIRECT_GOVERNANCE_DELTA",
        "INDEPENDENT_VERIFICATION",
    ),
    (
        "R295A_ATTACK_SUITE",
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_attack_suite.json",
        2_072,
        "ecf3da6b5be1d6e790d39240ee93f5457651f7e3605c6388e05a69c9027ece16",
        "AF3D1_DIRECT_GOVERNANCE_DELTA",
        "ATTACK_SUITE",
    ),
    (
        "R295A_MANIFEST",
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_manifest.sha256",
        1_558,
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
        "AF3D1_DIRECT_GOVERNANCE_DELTA",
        "SEALED_MANIFEST",
    ),
)


ROLE_POLICIES: dict[str, dict[str, Any]] = {
    "ANALYTIC_LINEAGE": {
        "admitted_for_construction": True,
        "forbidden_as": [
            "DIRECT_MEMBER_SUPPORT",
            "NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE",
            "PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM",
            "FORMAL_B1A_OR_CM2_CREDIT",
        ],
    },
    "CONSTRUCTION_LINEAGE": {
        "admitted_for_construction": True,
        "forbidden_as": [
            "NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE",
            "PHYSICAL_INCIDENCE_THEOREM",
            "FORMAL_B1A_OR_CM2_CREDIT",
        ],
    },
    "IDENTITY_BINDING": {
        "admitted_for_construction": True,
        "forbidden_as": [
            "NORMALIZED_FULL_SUPPORT",
            "SUPPORT_GEOMETRY",
            "PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM",
            "FORMAL_B1A_OR_CM2_CREDIT",
        ],
    },
}


# authority, filename, JSON path, row ID, count, IDs SHA, row hashes SHA,
# rows SHA, role, row encoding, semantic note
TABLE_SPECS: tuple[
    tuple[str, str, str, str, int, str, str | None, str, str, str, str], ...
] = (
    (
        "R179.retained_3d_child_rows",
        "cm2_round179_source_g_residual_tube_arrangement_rows.json",
        ".result.retained_3d_child_rows[]",
        "packed column 0 row_id",
        106_680,
        "b6b26fe4b1be4f31986f9304cf1cba1305c3ec236bebd8dd4ad9b050a9cb6308",
        None,
        "276483255e2b1dda1c682641f5cdcefd67be9040cadad8f4eb810d0fd5cc0b79",
        "ANALYTIC_LINEAGE",
        "PACKED_COLUMN_ZERO",
        "RETAINED_OPEN_3D_CHILD_IS_ANALYTIC_LINEAGE_NOT_DIRECT_MEMBER_SUPPORT",
    ),
    (
        "R236.whole_root_finite_key_partition_rows",
        "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json",
        ".result.whole_root_finite_key_partition_rows[]",
        "whole_root_partition_row_id",
        2_640,
        "774197275c01421246b5229654fa9d4d8f42a2242608863b36a052de39735a36",
        None,
        "17cee8dcc86d2436b47f1605ca324f2006255ed983b57ac06938743b952dafd9",
        "CONSTRUCTION_LINEAGE",
        "OBJECT_ROWS_WITHOUT_PER_ROW_HASH",
        "FINITE_KEY_PARTITION_IS_NOT_SUPPORT_OR_PHYSICAL_INCIDENCE",
    ),
    (
        "R242.root_existence_classification_rows",
        "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json",
        ".result.formal_root_existence_classification_ledger.rows[]",
        "root_existence_row_id",
        3_136,
        "5d41bc251b05531e1e0c599b44a2a888983dd27a919453023bef498f19937bb2",
        "7294e84fa6e8a4ee88fea181eacab086f22062fd9d58ba9fffa6bd009930b53b",
        "39df731f100637b57945faeb907bcb219168f7083b32e876c8e09be5bfb189fa",
        "CONSTRUCTION_LINEAGE",
        "CLOSED_OBJECT_ROWS",
        "ROOT_CLASSIFICATION_REQUIRES_TYPED_AST_AND_EQUIVALENCE_BEFORE_SUPPORT",
    ),
    (
        "R242.zero_absence_base_partition_rows",
        "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json",
        ".result.formal_zero_absence_base_partition_ledger.rows[]",
        "zero_absence_leaf_row_id",
        8_400,
        "ce0d414b1a86b70576023535d91396dc8243930061034fe43218a8588048cb32",
        "62ae7882eadd5efb4c248f953e95d6e28b8a99b9a3e8fede9a84a246b10f0751",
        "2df003dbc57e1792c1ef09cc388224a6199d5bf8e206c4c8c294a1608cc4980b",
        "ANALYTIC_LINEAGE",
        "CLOSED_OBJECT_ROWS",
        "ZERO_ABSENCE_PARTITION_IS_WHOLE_ROOT_EQUALITY_EVIDENCE_NOT_DIRECT_MEMBER_SUPPORT",
    ),
    (
        "R245.mixed_sheet_physical_edge_rows",
        "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json",
        ".result.formal_mixed_sheet_physical_edge_ledger.rows[]",
        "mixed_sheet_edge_id",
        3_664,
        "c74e8c1f35529e9d90003ce08e4581e208a6e269c42bfb820a3c67e37a4d709b",
        "5536e74ac3a52284ab56a1be04e897ae8ea6d5f614b0a012449be49fec6827a9",
        "08da8a6331675f0fbb3fe6a01a9310dee8283f7de2673a7b08144bbf9f08e765",
        "CONSTRUCTION_LINEAGE",
        "CLOSED_OBJECT_ROWS",
        "LOWER_BOUND_EDGE_EVIDENCE_IS_NOT_MAXIMALITY_SUPPORT_OR_INCIDENCE_THEOREM",
    ),
    (
        "R286.refinement_rows",
        "cm2_round286_source_g_partial_overlap_exact_refinement_probe_ledger.json.gz",
        ".rows[]",
        "Round286_refinement_cell_id",
        7_616,
        "55524a5c5aba5bdb2502073beefbdc9faae3988e0ee85c0d0997d37211448e43",
        "41adbd60b6c19005336609112b0527dfa296c5bb0bd812ced8d4bd6ea38d4e39",
        "ef4529302d5a072b04133abb433ee4676acd4e8867a360fd09e05e28053917c6",
        "CONSTRUCTION_LINEAGE",
        "CLOSED_OBJECT_ROWS",
        "REFINEMENT_AND_OCCUPANCY_ROWS_REQUIRE_LATER_PHYSICAL_PULLBACK_CERTIFICATE",
    ),
    (
        "R295A.representation_alias_rows",
        "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz",
        ".rows[]",
        "Round295A_retained_continuation_alias_row_id",
        276,
        "3faee0fe36ed0d091a93d2679591815fd22a28e02dce8e7cfddd475e44286c02",
        "fb9a4a2dea4bbb3f1b9cc1d4b417e1d102987e8d74fb7d00e9ec23218694fcf4",
        "40047a170d2e89a9e9cf8422ff86e265166e921f86386ecb4df790e8210d09de",
        "IDENTITY_BINDING",
        "CLOSED_OBJECT_ROWS",
        "TPS_ALIAS_TO_EXISTING_MEMBER_NEVER_MINTS_SUPPORT_OR_MEMBER_IDENTITY",
    ),
)


def _pin_rows() -> list[dict[str, Any]]:
    return sorted(
        (
            {
                "label": label,
                "filename": filename,
                "exact_size": size,
                "sha256": sha256,
                "pin_origin": origin,
                "purpose": purpose,
            }
            for label, filename, size, sha256, origin, purpose in FILE_PINS
        ),
        key=lambda row: row["filename"],
    )


def _role_rows() -> list[dict[str, Any]]:
    return [
        {"authority_role": role, **ROLE_POLICIES[role]}
        for role in sorted(ROLE_POLICIES)
    ]


def _file_pin_map() -> dict[str, tuple[int, str]]:
    return {
        filename: (size, sha256)
        for _label, filename, size, sha256, _origin, _purpose in FILE_PINS
    }


def _table_rows() -> list[dict[str, Any]]:
    pins = _file_pin_map()
    rows: list[dict[str, Any]] = []
    for (
        authority,
        filename,
        json_path,
        row_id_field,
        row_count,
        row_ids_sha256,
        row_hashes_sha256,
        rows_sha256,
        role,
        row_encoding,
        semantic_note,
    ) in TABLE_SPECS:
        size, sha256 = pins[filename]
        policy = ROLE_POLICIES[role]
        rows.append(
            {
                "authority": authority,
                "filename": filename,
                "source_exact_size": size,
                "source_sha256": sha256,
                "json_path": json_path,
                "row_id_field": row_id_field,
                "row_count": row_count,
                "row_ids_sha256": row_ids_sha256,
                "row_hashes_sha256": row_hashes_sha256,
                "rows_sha256": rows_sha256,
                "authority_role": role,
                "admitted_for_construction": policy["admitted_for_construction"],
                "forbidden_as": list(policy["forbidden_as"]),
                "row_schema_contract": {
                    "row_encoding": row_encoding,
                    "stored_order_is_authoritative": True,
                    "semantic_boundary": semantic_note,
                },
            }
        )
    return sorted(rows, key=lambda row: row["authority"])


def _base_payload() -> dict[str, Any]:
    pins = _pin_rows()
    tables = _table_rows()
    roles = _role_rows()
    direct_governance = [
        row for row in pins if row["pin_origin"] == "AF3D1_DIRECT_GOVERNANCE_DELTA"
    ]
    inherited_closure = [
        row for row in pins if row["pin_origin"] == "AF3_CLOSURE_INHERITED"
    ]
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "sealed": True,
        "non_production": True,
        "candidate_is_formal": False,
        "af3_immutable_parent_commitment": {
            "required": True,
            "AF3_source_filename": AF3_SOURCE_FILENAME,
            "AF3_source_exact_size": AF3_SOURCE_SIZE,
            "AF3_source_sha256": AF3_SOURCE_SHA256,
            "AF3_schema": AF3_SCHEMA,
            "AF3_status": AF3_STATUS,
            "AF3_canonical_document_size_without_final_LF": AF3_CANONICAL_DOCUMENT_SIZE,
            "AF3_canonical_document_sha256": AF3_CANONICAL_DOCUMENT_SHA256,
            "AF3_printed_stdout_size_with_one_final_LF": AF3_PRINTED_STDOUT_SIZE,
            "AF3_printed_stdout_sha256": AF3_PRINTED_STDOUT_SHA256,
            "AF3_authority_file_count": AF3_AUTHORITY_FILE_COUNT,
            "AF3_authority_file_bytes": AF3_AUTHORITY_FILE_BYTES,
            "AF3_authority_file_catalog_sha256": AF3_AUTHORITY_FILE_CATALOG_SHA256,
            "AF3_authority_role_catalog_sha256": AF3_AUTHORITY_ROLE_CATALOG_SHA256,
            "AF3_table_authority_count": AF3_TABLE_AUTHORITY_COUNT,
            "AF3_table_authority_catalog_sha256": AF3_TABLE_AUTHORITY_CATALOG_SHA256,
            "AF3_inventory_rows_sha256": AF3_INVENTORY_ROWS_SHA256,
            "AF3_transitive_file_count": AF3_TRANSITIVE_FILE_COUNT,
            "AF3_transitive_file_bytes": AF3_TRANSITIVE_FILE_BYTES,
            "AF3_expected_replay_result_sha256": AF3_REPLAY_RESULT_SHA256,
            "AF3_source_or_document_modified_by_AF3D1": False,
            "AF3_source_executed_or_imported_by_contract_process": False,
        },
        "file_pin_catalog": {
            "file_count": len(pins),
            "exact_total_bytes": sum(row["exact_size"] for row in pins),
            "records": pins,
            "records_sha256": digest(pins),
            "direct_governance_delta_count": len(direct_governance),
            "direct_governance_delta_sha256": digest(direct_governance),
            "AF3_closure_inherited_count": len(inherited_closure),
            "AF3_closure_inherited_sha256": digest(inherited_closure),
        },
        "authority_role_policies": {
            "records": roles,
            "records_sha256": digest(roles),
        },
        "table_authority_delta": {
            "table_count": len(tables),
            "stored_order_row_count": sum(row["row_count"] for row in tables),
            "records": tables,
            "records_sha256": digest(tables),
            "AF3_table_authority_count_before": AF3_TABLE_AUTHORITY_COUNT,
            "effective_overlay_table_authority_count": AF3_TABLE_AUTHORITY_COUNT + len(tables),
            "AF3_authority_file_count_before": AF3_AUTHORITY_FILE_COUNT,
            "new_authority_files": [
                "cm2_round286_source_g_partial_overlap_exact_refinement_probe_ledger.json.gz",
                "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz",
            ],
            "new_authority_file_bytes": 1_735_934,
            "effective_overlay_authority_file_count": AF3_AUTHORITY_FILE_COUNT + 2,
            "effective_overlay_authority_file_bytes": AF3_AUTHORITY_FILE_BYTES + 1_735_934,
            "overlay_does_not_rewrite_AF3_catalog": True,
        },
        "representation_census_binding": {
            "representation_denominator": 611_904,
            "primary": 564_492,
            "refined_primary_extra_T2PS": 848,
            "R294_aliases": 46_288,
            "R295A_aliases": 276,
            "alias_total": 46_564,
            "T2PS_total": 11_852,
            "R295A_alias_coordinate_system": "TPS",
            "R295A_aliases_are_the_R292_T2PS_1600": False,
            "representation_cover_proved": 0,
            "one_primary_per_member_theorem_proved": False,
            "pullback_equivalence_theorem_proved": False,
        },
        "semantic_boundaries": {
            "delta_is_byte_and_table_authority_only": True,
            "typed_support_AST_frozen": False,
            "certificate_grammar_frozen": False,
            "normalized_full_support_proved": 0,
            "physical_incidence_proved": 0,
            "representation_cover_proved": 0,
            "formal_B1A": False,
            "B2_authorized": False,
            "R179_retained_box_is_full_support_by_default": False,
            "R179_retained_child_is_direct_member_support": False,
            "R236_or_R242_partition_is_full_support_by_default": False,
            "R242_zero_absence_whole_root_equality_evidence_is_direct_member_support": False,
            "R245_lower_bound_edge_is_physical_incidence_or_maximality": False,
            "R286_refinement_or_occupancy_is_support_equivalence": False,
            "R295A_alias_mints_member_identity": False,
            "R295A_alias_defines_support_geometry": False,
        },
        "authority_verifier_contract": {
            "read_only": True,
            "held_directory_fd": True,
            "all_file_fds_opened_before_byte_verification": True,
            "all_file_fds_held_until_global_reaudit": True,
            "O_NOFOLLOW": True,
            "regular_file_required": True,
            "nlink_one_required": True,
            "two_pass_same_fd_SHA256": True,
            "pre_post_fstat_required": True,
            "path_inode_replacement_fail_close": True,
            "strict_JSON_duplicate_and_nonfinite_rejection": True,
            "gzip_CRC_checked_for_table_sources": True,
            "upstream_modules_imported_or_executed": False,
            "candidate_or_production_files_written": 0,
        },
        "candidate_mode": {
            "enabled": False,
            "blocked_before_path_lstat": True,
            "blocked_before_path_open": True,
            "blocked_before_temp_creation": True,
            "blocked_before_write": True,
            "blocked_before_stdout_or_stderr": True,
        },
        "production_mode": {
            "enabled": False,
            "blocked_before_path_lstat": True,
            "blocked_before_path_open": True,
            "blocked_before_temp_creation": True,
            "blocked_before_write": True,
            "blocked_before_stdout_or_stderr": True,
        },
        "formal_credit": {
            "feature_definition": 0,
            "normalized_member_support": 0,
            "representation_cover": 0,
            "physical_incidence": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "transition": 0,
            "pair_routing": 0,
            "D02": "BLOCKED",
            "D03": "NOT_REACHED",
            "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "emission_accounting": {
            "candidate_files_written": 0,
            "production_files_written": 0,
            "other_files_written": 0,
        },
    }


def _contract_document() -> dict[str, Any]:
    payload = _base_payload()
    return {
        **payload,
        "canonical_payload_commitment": {
            "hash_domain": "canonical_json(all_document_fields_except_canonical_payload_commitment);sort_keys;compact_ASCII;no_LF",
            "exact_size": len(canonical(payload)),
            "sha256": digest(payload),
        },
    }


def validate_contract(document: dict[str, Any]) -> None:
    expected = _contract_document()
    need(canonical(document) == canonical(expected), "exact sealed AF3D1 document")
    need(document["schema"] == SCHEMA and document["status"] == STATUS, "schema/status")
    need(document["sealed"] is True and document["non_production"] is True, "sealed non-production")
    need(document["candidate_is_formal"] is False, "candidate non-formal")
    parent = document["af3_immutable_parent_commitment"]
    need(parent["AF3_source_sha256"] == AF3_SOURCE_SHA256, "AF3 source pin")
    need(parent["AF3_canonical_document_sha256"] == AF3_CANONICAL_DOCUMENT_SHA256, "AF3 document pin")
    need(parent["AF3_source_or_document_modified_by_AF3D1"] is False, "AF3 immutable")
    need(document["file_pin_catalog"]["records"] == _pin_rows(), "pin rows")
    need(document["file_pin_catalog"]["records_sha256"] == digest(_pin_rows()), "pin digest")
    need(document["authority_role_policies"]["records"] == _role_rows(), "role policies")
    tables = document["table_authority_delta"]
    need(tables["records"] == _table_rows(), "table rows")
    need(tables["table_count"] == 7 and tables["stored_order_row_count"] == 132_412, "table census")
    need(tables["effective_overlay_table_authority_count"] == 89, "effective table count")
    need(tables["effective_overlay_authority_file_count"] == 47, "effective file count")
    need(tables["effective_overlay_authority_file_bytes"] == 4_667_098_623, "effective file bytes")
    roles = {row["authority"]: row["authority_role"] for row in tables["records"]}
    need(roles["R179.retained_3d_child_rows"] == "ANALYTIC_LINEAGE", "R179 analytic role")
    need(
        roles["R242.zero_absence_base_partition_rows"] == "ANALYTIC_LINEAGE",
        "R242 zero-absence analytic role",
    )
    need(
        roles["R242.root_existence_classification_rows"] == "CONSTRUCTION_LINEAGE",
        "R242 root-existence construction role",
    )
    need(roles["R295A.representation_alias_rows"] == "IDENTITY_BINDING", "R295A role")
    need(all(
        roles[name] == "CONSTRUCTION_LINEAGE"
        for name in roles
        if name not in {
            "R179.retained_3d_child_rows",
            "R242.zero_absence_base_partition_rows",
            "R295A.representation_alias_rows",
        }
    ), "construction-lineage roles")
    representation = document["representation_census_binding"]
    need(
        representation["primary"]
        + representation["refined_primary_extra_T2PS"]
        + representation["R294_aliases"]
        + representation["R295A_aliases"]
        == representation["representation_denominator"]
        == 611_904,
        "representation equation",
    )
    need(representation["R295A_aliases_are_the_R292_T2PS_1600"] is False, "alias distinction")
    semantics = document["semantic_boundaries"]
    need(all(
        value in {False, 0}
        for key, value in semantics.items()
        if key.endswith("_proved")
        or key in {
            "typed_support_AST_frozen",
            "certificate_grammar_frozen",
            "formal_B1A",
            "B2_authorized",
        }
    ), "unclosed semantics")
    need(semantics["delta_is_byte_and_table_authority_only"] is True, "delta scope")
    for section in (document["candidate_mode"], document["production_mode"]):
        need(section["enabled"] is False, "mode disabled")
        need(all(value is True for key, value in section.items() if key != "enabled"), "pre-filesystem block")
    credit = document["formal_credit"]
    need(all(value == 0 for key, value in credit.items() if key not in {"D02", "D03", "D04", "CM2"}), "zero credit")
    need(credit["D02"] == "BLOCKED" and credit["CM2"] == "NO-GO_FOR_CLAIM", "D02/CM2")
    need(all(value == 0 for value in document["emission_accounting"].values()), "zero emission")
    commitment = document["canonical_payload_commitment"]
    payload = {key: value for key, value in document.items() if key != "canonical_payload_commitment"}
    need(commitment["exact_size"] == len(canonical(payload)), "payload size")
    need(commitment["sha256"] == digest(payload), "payload digest")


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
        (("sealed",), False),
        (("non_production",), False),
        (("candidate_is_formal",), True),
        (("af3_immutable_parent_commitment", "AF3_source_exact_size"), AF3_SOURCE_SIZE - 1),
        (("af3_immutable_parent_commitment", "AF3_source_sha256"), "0" * 64),
        (("af3_immutable_parent_commitment", "AF3_canonical_document_sha256"), "0" * 64),
        (("af3_immutable_parent_commitment", "AF3_printed_stdout_sha256"), "0" * 64),
        (("af3_immutable_parent_commitment", "AF3_table_authority_count"), 81),
        (("af3_immutable_parent_commitment", "AF3_source_or_document_modified_by_AF3D1"), True),
        (("file_pin_catalog", "file_count"), len(FILE_PINS) - 1),
        (("file_pin_catalog", "exact_total_bytes"), 1),
        (("file_pin_catalog", "records_sha256"), "0" * 64),
        (("file_pin_catalog", "records", 0, "sha256"), "0" * 64),
        (("file_pin_catalog", "records", -1, "exact_size"), 1),
        (("file_pin_catalog", "records", -1, "pin_origin"), "UNPINNED"),
        (("authority_role_policies", "records_sha256"), "0" * 64),
        (("authority_role_policies", "records", 0, "admitted_for_construction"), False),
        (("table_authority_delta", "table_count"), 6),
        (("table_authority_delta", "stored_order_row_count"), 132_411),
        (("table_authority_delta", "records_sha256"), "0" * 64),
        (("table_authority_delta", "records", 0, "row_count"), 2_639),
        (("table_authority_delta", "records", 0, "rows_sha256"), "0" * 64),
        (("table_authority_delta", "records", 0, "json_path"), ".rows[]"),
        (("table_authority_delta", "records", 0, "authority_role"), "SUPPORT_ROW_SOURCE"),
        (("table_authority_delta", "records", 0, "authority_role"), "CONSTRUCTION_LINEAGE"),
        (("table_authority_delta", "records", 2, "authority_role"), "ANALYTIC_LINEAGE"),
        (("table_authority_delta", "records", 3, "authority_role"), "SUPPORT_ROW_SOURCE"),
        (("table_authority_delta", "records", 3, "authority_role"), "CONSTRUCTION_LINEAGE"),
        (("table_authority_delta", "records", -1, "row_count"), 275),
        (("table_authority_delta", "records", -1, "authority_role"), "SUPPORT_ROW_SOURCE"),
        (("table_authority_delta", "records", -1, "admitted_for_construction"), False),
        (("table_authority_delta", "effective_overlay_table_authority_count"), 88),
        (("table_authority_delta", "effective_overlay_authority_file_count"), 46),
        (("table_authority_delta", "overlay_does_not_rewrite_AF3_catalog"), False),
        (("representation_census_binding", "representation_denominator"), 611_903),
        (("representation_census_binding", "R295A_aliases"), 275),
        (("representation_census_binding", "R295A_aliases_are_the_R292_T2PS_1600"), True),
        (("representation_census_binding", "representation_cover_proved"), 1),
        (("representation_census_binding", "pullback_equivalence_theorem_proved"), True),
        (("semantic_boundaries", "typed_support_AST_frozen"), True),
        (("semantic_boundaries", "normalized_full_support_proved"), 1),
        (("semantic_boundaries", "physical_incidence_proved"), 1),
        (("semantic_boundaries", "formal_B1A"), True),
        (("semantic_boundaries", "R179_retained_child_is_direct_member_support"), True),
        (("semantic_boundaries", "R242_zero_absence_whole_root_equality_evidence_is_direct_member_support"), True),
        (("semantic_boundaries", "R245_lower_bound_edge_is_physical_incidence_or_maximality"), True),
        (("semantic_boundaries", "R286_refinement_or_occupancy_is_support_equivalence"), True),
        (("semantic_boundaries", "R295A_alias_mints_member_identity"), True),
        (("authority_verifier_contract", "two_pass_same_fd_SHA256"), False),
        (("authority_verifier_contract", "path_inode_replacement_fail_close"), False),
        (("candidate_mode", "enabled"), True),
        (("production_mode", "enabled"), True),
        (("formal_credit", "normalized_member_support"), 1),
        (("formal_credit", "representation_cover"), 1),
        (("formal_credit", "physical_incidence"), 1),
        (("formal_credit", "D02"), "PASS"),
        (("formal_credit", "CM2"), "GO"),
        (("emission_accounting", "candidate_files_written"), 1),
        (("canonical_payload_commitment", "sha256"), "0" * 64),
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
    need(all(value == 0 for value in calls.values()), "blocked entry pre-filesystem boundary")
    return {
        "blocked": True,
        "patched_operation_count": len(calls),
        "observed_operation_count": sum(calls.values()),
    }


def self_test() -> dict[str, Any]:
    document = contract()
    for entry in (build_private_candidate, build_production_package):
        need(entry.__code__.co_argcount == 1, "blocked entry arity")
        need(set(entry.__code__.co_names) <= {
            "ContractBlocked", "CANDIDATE_BLOCK_REASON", "PRODUCTION_BLOCK_REASON"
        }, "blocked entry globals")
    rejected, total = _mutation_suite()
    need(rejected == total, "all semantic mutations rejected")
    candidate_probe = _blocked_entry_probe(build_private_candidate, CANDIDATE_BLOCK_REASON)
    production_probe = _blocked_entry_probe(build_production_package, PRODUCTION_BLOCK_REASON)
    result = {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS_SEALED_ZERO_CREDIT_AUTHORITY_DELTA_SELF_TEST",
        "contract_sha256": digest(document),
        "canonical_payload_sha256": document["canonical_payload_commitment"]["sha256"],
        "file_pin_catalog_sha256": document["file_pin_catalog"]["records_sha256"],
        "table_authority_catalog_sha256": document["table_authority_delta"]["records_sha256"],
        "authority_role_catalog_sha256": document["authority_role_policies"]["records_sha256"],
        "semantic_mutations_rejected": rejected,
        "semantic_mutation_count": total,
        "candidate_boundary_probe": candidate_probe,
        "production_boundary_probe": production_probe,
        "upstream_files_opened": 0,
        "subprocesses_started": 0,
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


def _hash_fd(descriptor: int, exact_size: int) -> tuple[str, int]:
    os.lseek(descriptor, 0, os.SEEK_SET)
    state = hashlib.sha256()
    total = 0
    while True:
        block = os.read(descriptor, 1 << 20)
        if not block:
            break
        total += len(block)
        need(total <= exact_size, "bounded authority read")
        state.update(block)
    return state.hexdigest(), total


def _read_fd(descriptor: int, exact_size: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    total = 0
    while True:
        block = os.read(descriptor, 1 << 20)
        if not block:
            break
        total += len(block)
        need(total <= exact_size, "bounded authority capture")
        chunks.append(block)
    need(total == exact_size, "exact authority capture size")
    return b"".join(chunks)


def _reject_constant(value: str) -> NoReturn:
    raise ContractBlocked("nonfinite JSON constant:" + value)


def _reject_float(value: str) -> NoReturn:
    raise ContractBlocked("JSON float prohibited in exact authority:" + value)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def _strict_json_bytes(payload: bytes) -> Any:
    return json.loads(
        payload,
        object_pairs_hook=_unique_object,
        parse_constant=_reject_constant,
        parse_float=_reject_float,
    )


def _strict_json_fd(descriptor: int, compressed: bool) -> Any:
    os.lseek(descriptor, 0, os.SEEK_SET)
    raw = os.fdopen(os.dup(descriptor), "rb")
    binary: Any = gzip.GzipFile(fileobj=raw, mode="rb") if compressed else raw
    text = io.TextIOWrapper(binary, encoding="utf-8", errors="strict", newline=None)
    try:
        return json.load(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
            parse_float=_reject_float,
        )
    finally:
        text.close()


def _table_source_rows(authority: str, document: dict[str, Any]) -> tuple[list[Any], dict[str, Any] | None]:
    if authority == "R179.retained_3d_child_rows":
        result = document["result"]
        need(result["row_column_schemas"]["retained_3d_child_rows"][0] == "row_id", "R179 packed row ID column")
        return result["retained_3d_child_rows"], result["table_census_and_sha256"]["retained_3d_child_rows"]
    if authority == "R236.whole_root_finite_key_partition_rows":
        return document["result"]["whole_root_finite_key_partition_rows"], None
    if authority == "R242.root_existence_classification_rows":
        ledger = document["result"]["formal_root_existence_classification_ledger"]
        return ledger["rows"], ledger
    if authority == "R242.zero_absence_base_partition_rows":
        ledger = document["result"]["formal_zero_absence_base_partition_ledger"]
        return ledger["rows"], ledger
    if authority == "R245.mixed_sheet_physical_edge_rows":
        ledger = document["result"]["formal_mixed_sheet_physical_edge_ledger"]
        return ledger["rows"], ledger
    if authority == "R286.refinement_rows" or authority == "R295A.representation_alias_rows":
        return document["rows"], document
    raise ContractBlocked("unknown table authority:" + authority)


def _row_id(row: Any, encoding: str, field: str) -> str:
    if encoding == "PACKED_COLUMN_ZERO":
        need(type(row) is list and len(row) > 0, "packed row shape")
        value = row[0]
    else:
        need(type(row) is dict, "object row shape")
        value = row[field]
    need(type(value) is str and value != "", "nonempty row ID")
    return value


def _verify_table(record: dict[str, Any], document: dict[str, Any]) -> dict[str, Any]:
    rows, ledger = _table_source_rows(record["authority"], document)
    need(type(rows) is list and len(rows) == record["row_count"], "table row count:" + record["authority"])
    if ledger is not None:
        if "row_count" in ledger:
            need(ledger["row_count"] == record["row_count"], "embedded row count:" + record["authority"])
        if "rows_sha256" in ledger:
            need(ledger["rows_sha256"] == record["rows_sha256"], "embedded rows SHA:" + record["authority"])
        if record["row_ids_sha256"] is not None and "row_ids_sha256" in ledger:
            need(ledger["row_ids_sha256"] == record["row_ids_sha256"], "embedded IDs SHA:" + record["authority"])
        if record["row_hashes_sha256"] is not None and "row_hashes_sha256" in ledger:
            need(ledger["row_hashes_sha256"] == record["row_hashes_sha256"], "embedded hashes SHA:" + record["authority"])
    encoding = record["row_schema_contract"]["row_encoding"]
    id_field = record["row_id_field"]
    if encoding == "PACKED_COLUMN_ZERO":
        id_field = "row_id"
    ids: list[str] = []
    hashes: list[str] = []
    for row in rows:
        row_id = _row_id(row, encoding, id_field)
        ids.append(row_id)
        if record["row_hashes_sha256"] is not None:
            need(type(row) is dict, "closed row object")
            row_hash = row.get("row_sha256")
            need(type(row_hash) is str and len(row_hash) == 64, "closed row hash")
            payload = dict(row)
            payload.pop("row_sha256")
            need(digest(payload) == row_hash, "per-row content closure:" + record["authority"])
            hashes.append(row_hash)
    need(len(set(ids)) == len(ids), "unique row IDs:" + record["authority"])
    need(sequence_digest(rows) == record["rows_sha256"], "stored-order rows digest:" + record["authority"])
    need(sequence_digest(ids) == record["row_ids_sha256"], "stored-order IDs digest:" + record["authority"])
    if record["row_hashes_sha256"] is not None:
        need(sequence_digest(hashes) == record["row_hashes_sha256"], "stored-order hashes digest:" + record["authority"])
    return {
        "authority": record["authority"],
        "row_count": len(rows),
        "rows_sha256": record["rows_sha256"],
        "row_ids_sha256": record["row_ids_sha256"],
        "row_hashes_sha256": record["row_hashes_sha256"],
    }


def _verify_af3_replay(primary: bytes, independent: bytes) -> None:
    need(primary == independent, "AF3 replay result byte equality")
    need(hashlib.sha256(primary).hexdigest() == AF3_REPLAY_RESULT_SHA256, "AF3 replay result SHA")
    parsed = _strict_json_bytes(primary)
    need(type(parsed) is dict, "AF3 replay object")
    need(parsed.get("schema") == AF3_REPLAY_RESULT_SCHEMA, "AF3 replay schema")
    need(parsed.get("status") == "ZERO_FULL_SUPPORT_CREDIT", "AF3 replay zero credit")
    need(parsed.get("direct_root_count") == 36, "AF3 root count")
    need(parsed.get("transitive_file_count") == AF3_TRANSITIVE_FILE_COUNT, "AF3 closure count")
    need(parsed.get("transitive_file_bytes") == AF3_TRANSITIVE_FILE_BYTES, "AF3 closure bytes")
    need(parsed.get("inventory_rows_sha256") == AF3_INVENTORY_ROWS_SHA256, "AF3 inventory digest")
    authority = parsed["authority_contract"]
    need(authority["authority_file_count"] == AF3_AUTHORITY_FILE_COUNT, "AF3 authority file count")
    need(authority["authority_file_bytes"] == AF3_AUTHORITY_FILE_BYTES, "AF3 authority file bytes")
    need(authority["authority_file_catalog_sha256"] == AF3_AUTHORITY_FILE_CATALOG_SHA256, "AF3 file catalog")
    need(authority["authority_role_catalog_sha256"] == AF3_AUTHORITY_ROLE_CATALOG_SHA256, "AF3 role catalog")
    need(authority["table_authority_count"] == AF3_TABLE_AUTHORITY_COUNT, "AF3 table count")
    need(authority["table_authority_catalog_sha256"] == AF3_TABLE_AUTHORITY_CATALOG_SHA256, "AF3 table catalog")
    credit = parsed["formal_credit"]
    need(credit["normalized_full_support_members"] == 0, "AF3 support credit")
    need(credit["representation_cover"] == 0, "AF3 representation credit")
    need(credit["D02"] == "BLOCKED" and credit["CM2"] == "NO-GO_FOR_CLAIM", "AF3 D02/CM2")


def _verify_governance_payloads(payloads: dict[str, bytes]) -> None:
    r286_result = _strict_json_bytes(payloads["R286_RESULT"])
    need(r286_result["ledger"]["row_count"] == 7_616, "R286 result row count")
    need(r286_result["ledger"]["file_sha256"] == "bb7e28cbe029e2bb414313ec4a08f6366acbbad88a519926ec2a3a424e679eda", "R286 result ledger pin")
    need("ZERO_CREDIT" in r286_result["status"], "R286 zero credit")
    r286_verification = _strict_json_bytes(payloads["R286_VERIFICATION"])
    need(r286_verification["reconstruction"]["output_refinement_cell_count"] == 7_616, "R286 verification row count")
    need("ZERO_CREDIT" in r286_verification["status"], "R286 verification zero credit")
    r295_result = _strict_json_bytes(payloads["R295A_RESULT"])
    need(r295_result["representation_alias_ledger"]["row_count"] == 276, "R295A result alias count")
    need(r295_result["formal_credit_transition"]["formal_representation_alias_credit_delta"] == 276, "R295A alias delta")
    need(r295_result["formal_credit_transition"]["formal_new_expanded_occurrence_credit"] == 0, "R295A no new identity")
    r295_verification = _strict_json_bytes(payloads["R295A_VERIFICATION"])
    need(r295_verification["atomic_promotion_audit"]["representation_alias_row_count"] == 276, "R295A verification alias count")
    need(r295_verification["atomic_promotion_audit"]["new_occurrence_count"] == 0, "R295A verification no identity")
    need(r295_verification["strict_nonpromotion"]["D02"] == "BLOCKED", "R295A D02")


def verify_authority() -> dict[str, Any]:
    document = contract()
    data = Path(__file__).absolute().parent
    directory_before = os.stat(data, follow_symlinks=False)
    need(stat.S_ISDIR(directory_before.st_mode), "deliverables directory")
    directory_fd = os.open(data, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    opened: list[tuple[dict[str, Any], int, tuple[int, ...]]] = []
    try:
        need(_fingerprint(os.fstat(directory_fd)) == _fingerprint(directory_before), "directory fd binding")
        for pin in document["file_pin_catalog"]["records"]:
            filename = pin["filename"]
            need(filename not in {"", ".", ".."} and "/" not in filename and "\\" not in filename, "simple pinned basename")
            before = os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)
            need(stat.S_ISREG(before.st_mode), "regular pinned file:" + filename)
            need(before.st_nlink == 1, "single-link pinned file:" + filename)
            need(before.st_size == pin["exact_size"], "pinned file size:" + filename)
            descriptor = os.open(
                filename,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=directory_fd,
            )
            fingerprint = _fingerprint(before)
            opened.append((pin, descriptor, fingerprint))
            need(_fingerprint(os.fstat(descriptor)) == fingerprint, "fd/path binding:" + filename)

        table_by_file: dict[str, list[dict[str, Any]]] = {}
        for row in document["table_authority_delta"]["records"]:
            table_by_file.setdefault(row["filename"], []).append(row)
        small_labels = {
            "AF3_PRIMARY_REPLAY_RESULT",
            "AF3_INDEPENDENT_REPLAY_RESULT",
            "R286_RESULT",
            "R286_VERIFICATION",
            "R295A_RESULT",
            "R295A_VERIFICATION",
        }
        payloads: dict[str, bytes] = {}
        table_results: list[dict[str, Any]] = []
        total_hash_pass_bytes = 0
        for pin, descriptor, opened_fingerprint in opened:
            first_sha, first_size = _hash_fd(descriptor, pin["exact_size"])
            need(first_sha == pin["sha256"] and first_size == pin["exact_size"], "first SHA pass:" + pin["filename"])
            need(_fingerprint(os.fstat(descriptor)) == opened_fingerprint, "stable after first pass:" + pin["filename"])
            second_sha, second_size = _hash_fd(descriptor, pin["exact_size"])
            need(second_sha == pin["sha256"] and second_size == pin["exact_size"], "second SHA pass:" + pin["filename"])
            need(first_sha == second_sha and first_size == second_size, "two-pass identity:" + pin["filename"])
            total_hash_pass_bytes += first_size + second_size
            need(_fingerprint(os.fstat(descriptor)) == opened_fingerprint, "stable after second pass:" + pin["filename"])
            if pin["filename"] in table_by_file:
                parsed = _strict_json_fd(descriptor, pin["filename"].endswith(".gz"))
                need(type(parsed) is dict, "table source object:" + pin["filename"])
                for table in table_by_file[pin["filename"]]:
                    table_results.append(_verify_table(table, parsed))
                del parsed
                need(_fingerprint(os.fstat(descriptor)) == opened_fingerprint, "stable after table parse:" + pin["filename"])
            if pin["label"] in small_labels:
                payloads[pin["label"]] = _read_fd(descriptor, pin["exact_size"])
                need(_fingerprint(os.fstat(descriptor)) == opened_fingerprint, "stable after capture:" + pin["filename"])

        _verify_af3_replay(
            payloads["AF3_PRIMARY_REPLAY_RESULT"],
            payloads["AF3_INDEPENDENT_REPLAY_RESULT"],
        )
        _verify_governance_payloads(payloads)
        need(len(table_results) == 7, "verified table count")
        need(sum(row["row_count"] for row in table_results) == 132_412, "verified row census")
        for pin, descriptor, opened_fingerprint in opened:
            need(_fingerprint(os.fstat(descriptor)) == opened_fingerprint, "final held-fd audit:" + pin["filename"])
            need(
                _fingerprint(os.stat(pin["filename"], dir_fd=directory_fd, follow_symlinks=False))
                == opened_fingerprint,
                "final pathname/inode audit:" + pin["filename"],
            )
        need(_fingerprint(os.fstat(directory_fd)) == _fingerprint(directory_before), "final directory fd audit")
        need(_fingerprint(os.stat(data, follow_symlinks=False)) == _fingerprint(directory_before), "final directory path audit")
    finally:
        for _pin, descriptor, _opened_fingerprint in opened:
            os.close(descriptor)
        os.close(directory_fd)
    result = {
        "schema": SCHEMA + ".authority-verification.v1",
        "status": "PASS_HELD_FD_TWO_PASS_EXACT_AUTHORITY_DELTA_VERIFICATION__ZERO_CREDIT",
        "contract_sha256": digest(document),
        "canonical_payload_sha256": document["canonical_payload_commitment"]["sha256"],
        "checked_file_count": len(FILE_PINS),
        "checked_file_bytes": sum(row[2] for row in FILE_PINS),
        "two_pass_hashed_bytes": total_hash_pass_bytes,
        "verified_table_count": len(table_results),
        "verified_stored_order_row_count": sum(row["row_count"] for row in table_results),
        "file_pin_catalog_sha256": document["file_pin_catalog"]["records_sha256"],
        "table_authority_catalog_sha256": document["table_authority_delta"]["records_sha256"],
        "authority_role_catalog_sha256": document["authority_role_policies"]["records_sha256"],
        "AF3_source_sha256": AF3_SOURCE_SHA256,
        "AF3_canonical_document_sha256": AF3_CANONICAL_DOCUMENT_SHA256,
        "AF3_replay_result_sha256": AF3_REPLAY_RESULT_SHA256,
        "held_directory_fd": True,
        "all_file_fds_held_until_global_reaudit": True,
        "two_pass_same_fd_SHA256": True,
        "path_inode_replacement_fail_close": True,
        "upstream_modules_imported_or_executed": False,
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
    parser.add_argument("--verify-authority", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--production-dir", type=Path)
    args = parser.parse_args()
    need(
        sum((
            args.print_contract,
            args.self_test,
            args.verify_authority,
            args.candidate_dir is not None,
            args.production_dir is not None,
        )) == 1,
        "choose exactly one mode",
    )
    if args.print_contract:
        print(canonical(contract()).decode("ascii"))
    elif args.self_test:
        print(canonical(self_test()).decode("ascii"))
    elif args.verify_authority:
        try:
            print(canonical(verify_authority()).decode("ascii"))
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
