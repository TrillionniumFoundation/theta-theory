#!/usr/bin/env python3
"""Round306B1AF1 pre-schema admission contract for formal feature cover.

Round306B1AF0 correctly resolved the B1A/B2 scope cycle and froze several
useful censuses, but independent audit showed that it was not an implementable
wire schema.  In particular, 824,864 is a theorem-obligation census, not a
derived complete feature-ledger cardinality.  This successor therefore makes
the failure explicit and closes admission before any producer, candidate, or
formal package can be created.

This file grants no theorem or consumability credit.  It freezes only the
confirmed scope/census facts, the unresolved schema obligations, and the exact
conditions that must be discharged before a real B1A schema may be issued.
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
    """Fail-closed pre-schema admission violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ContractBlocked(label)


SCHEMA = "cm2.round306b1af1.source-g-feature-cover-pre-schema-admission.v1"
STATUS = (
    "BLOCKED_ZERO_CREDIT_PRE_SCHEMA__COMPLETE_PRIMITIVE_PARTITION_TYPED_WIRE_"
    "AND_CONSTRUCTION_PINS_NOT_FROZEN"
)
CANDIDATE_BLOCK_REASON = (
    "Round306B1AF1 is a pre-schema admission contract; candidate mode is "
    "blocked before every filesystem or output action"
)

# Filled after the canonical document is finalized.  validate_contract()
# compares against this literal rather than deriving an expected value from a
# mutable peer object.
EXPECTED_CONTRACT_SHA256 = "2057964163567b3d9e86ff03b10c009c7cacb31bb9e21410978997933bea7a0f"

FEATURE_OBLIGATION_COUNT = 824_864
ROOT_OBLIGATION_COUNT = 351_904
DEPENDENT_OBLIGATION_COUNT = 472_960
MEMBER_COUNT = 564_492
REPRESENTATION_COUNT = 611_904


INPUT_PINS = (
    (
        "Round306B1AF0_REJECTED_SCHEMA_DRAFT",
        "cm2_round306b1af0_source_g_formal_full_feature_cover_schema_contract.py",
        46_865,
        "d2edaf5247e90ad1e9344261e18b29612ed37b8d928bd1f715c5a6fab3a70e04",
    ),
    (
        "Round306B1A_DIAGNOSTIC_DRAFT",
        "cm2_round306b1a_source_g_r306b0_carrier_witness_and_support_gap_atlas.py",
        45_144,
        "6e198755d946bc5828a4366dc818469df7af5e44873c470d9d1050003960473a",
    ),
    (
        "Round306B2C0_ZERO_CREDIT_CONTRACT",
        "cm2_round306b2c0_source_g_feature_transition_pair_routing_contract.py",
        53_212,
        "6a4fbbc3c614b7adaf275d0870a0205360827ed9fe89b8e26748e966a04f4d69",
    ),
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
)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def _contract_document() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "candidate_is_formal": False,
        "scope": {
            "B1A_responsibility": [
                "source_free_feature_and_support_definitions",
                "complete_member_support_cover",
                "complete_representation_cover",
                "transition_ready_handles_without_transition_completeness",
            ],
            "B1A_exclusions": [
                "transition_atlas_completeness",
                "pair_routing",
                "candidate_pair_classification",
                "known_edge_geometry_first_recovery",
                "component_union",
                "maximality",
                "fibre",
                "global_disposition",
                "CM2_claim",
            ],
            "transition_atlas_is_B1A_precondition": False,
            "B1A_formal_must_precede_successor_B2": True,
            "existing_B1A_and_B2C0_files_remain_immutable": True,
        },
        "confirmed_census": {
            "B0_member_count": MEMBER_COUNT,
            "B0_occurrence_member_count": 431_208,
            "B0_virtual_positive_3D_count": 94_660,
            "B0_virtual_sheet_count": 38_624,
            "B0_component_count_metadata_only": 92_688,
            "representation_count": REPRESENTATION_COUNT,
            "primary_representation_count": 564_492,
            "extra_representation_count": 47_412,
            "refined_primary_extra_count": 848,
            "alias_representation_count": 46_564,
            "R294_alias_count": 46_288,
            "R295A_alias_count": 276,
            "feature_obligation_count": FEATURE_OBLIGATION_COUNT,
            "independent_root_obligation_count": ROOT_OBLIGATION_COUNT,
            "dependent_closure_obligation_count": DEPENDENT_OBLIGATION_COUNT,
            "A1": 17_940,
            "A2": 62_152,
            "R1": 295_340,
            "R2": 295_336,
            "R2_member_union_cell_count_histogram": {"1": 295_332, "2": 4},
            "G1": 38_624,
            "G2a": 38_624,
            "G2b": 76_848,
            "graph_physical_incidence_count": 115_472,
            "graph_sheet_identification_count": 38_624,
            "graph_side_reference_count": 76_848,
            "distinct_graph_side_carrier_count": 76_304,
        },
        "representation_cross_table": [
            ["PRIMARY", "TPS", 421_804],
            ["PRIMARY", "T2PS", 9_404],
            ["PRIMARY", "VIRTUAL_P3D", 94_660],
            ["PRIMARY", "VIRTUAL_SHEET", 38_624],
            ["REFINED_PRIMARY_EXTRA", "T2PS", 848],
            ["ALIAS_EXISTING_MEMBER", "T2PS", 1_600],
            ["ALIAS_EXISTING_MEMBER", "TPS", 44_964],
        ],
        "critical_count_distinction": {
            "824864_is_typed_theorem_obligation_census": True,
            "824864_is_complete_feature_definition_ledger_count": False,
            "complete_feature_definition_ledger_count": None,
            "primitive_support_partition_derived": False,
            "feature_definition_ledger_row_count_may_be_frozen_now": False,
            "source_closure_name_is_prohibited_as_ambiguous_alias": True,
            "future_B2_logical_ledger_name": "feature_definition",
        },
        "analytic_lineage_feasibility_evidence": {
            "status": "DIAGNOSTIC_ONLY__NO_FORMAL_CREDIT",
            "R204_root_count": 224,
            "R204_curve_count": 504,
            "R204_point_count": 280,
            "R208_R211_root_count": 17_716,
            "R208_R211_curve_count": 20_456,
            "R208_R211_endpoint_count": 40_912,
            "total_analytic_root_count": 17_940,
            "total_dependent_incidence_count": 62_152,
            "missing_parent_count": 0,
            "duplicate_typed_id_count": 0,
            "R204_descriptor_commitment":
                "b2fb80f7925505499d300bd2c77d17b3514e57e43b0eeb7380462c8b7d3a55c1",
            "R208_R211_descriptor_commitment":
                "0ebd81663d9a120d9775f02efa358fa5a6c2ec76e465bc2a7fd1d1153bd41722",
            "probe_result_commitment":
                "f7d3b6d6a5c9fdb263005cb3916967d662da9a485cc7806bd98f081b3bd619fa",
            "probe_artifact_externally_pinned": False,
            "evidence_may_authorize_schema_or_producer": False,
            "independent_interval_or_equivalence_reconstruction_complete": False,
        },
        "construction_input_admission": {
            "currently_pinned_scope_inputs": [
                {
                    "label": label,
                    "filename": filename,
                    "exact_size": size,
                    "sha256": sha256,
                }
                for label, filename, size, sha256 in INPUT_PINS
            ],
            "currently_pinned_scope_input_count": len(INPUT_PINS),
            "currently_pinned_inputs_are_complete_construction_inputs": False,
            "missing_construction_input_families": [
                "B0_member_support_source_index_consumed_ledger",
                "B1R0_predicate_source_cell_and_member_union_consumed_ledgers",
                "B1G0_graph_source_sheet_side_consumed_ledgers",
                "R174_R179_R182_R204_R208_R211_R220",
                "R245_R246_R247_R248_R264_R266",
                "R269_R270_R271_R272_R288_R290_R292",
                "R294_registry_and_representation_bindings",
                "R295A_alias_ledger",
                "raw_R235_R236_R242_graph_sources_and_seals",
                "B1R0_raw_predicate_source_backbindings",
                "B1G0_correction_and_B0_backbindings",
            ],
            "producer_may_open_unpinned_construction_source": False,
            "producer_authorized": False,
        },
        "machine_executable_schema_admission": {
            "family_discriminated_feature_union_frozen": False,
            "typed_scalar_predicate_set_map_AST_grammar_frozen": False,
            "operator_arity_and_sort_rules_frozen": False,
            "family_natural_keys_and_source_bindings_frozen": False,
            "proof_kernel_to_family_mapping_frozen": False,
            "certificate_payload_and_theorem_schema_frozen": False,
            "member_B0_exact_binding_and_source_exhaustion_frozen": False,
            "representation_map_inverse_and_pullback_proof_frozen": False,
            "transition_ready_handle_schema_frozen": False,
            "ledger_envelope_and_hash_domains_frozen": False,
            "result_schema_frozen": False,
            "verification_marker_schema_frozen": False,
            "attack_suite_schema_frozen": False,
            "manifest_grammar_and_transaction_frozen": False,
            "successor_validator_exact_literal_field_coverage_frozen": False,
            "successor_semantic_mutation_coverage_frozen": False,
            "normative_successor_schema_externally_pinned_or_packaged": False,
            "candidate_row_credit_must_be_integer_zero": True,
            "candidate_result_is_formal_must_be_false": True,
            "only_external_independent_verification_may_grant_consumability": True,
            "implementable_formal_schema_admitted": False,
        },
        "exact_next_closure_order": [
            "derive_provisional_primitive_support_feature_partition_read_only",
            "freeze_all_construction_files_by_size_hash_table_id_and_row_commitment",
            "independently_rederive_and_seal_primitive_partition_against_frozen_inputs",
            "freeze_family_discriminated_keys_bindings_and_cardinality_equations",
            "freeze_typed_AST_and_certificate_grammars",
            "freeze_member_and_representation_cross_source_exhaustion_rules",
            "freeze_transition_ready_boundary_stratum_handle_schema",
            "freeze_ledger_result_verification_attack_manifest_wire_schemas",
            "freeze_exact_successor_validator_mutations_and_external_schema_pin",
            "issue_independently_audited_successor_schema",
            "only_then_implement_private_candidate_producer",
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
        "self_source_seal": {
            "self_contained_program_can_prove_its_own_source_immutability": False,
            "independent_external_source_hash_required": True,
            "formal_package_claimed": False,
        },
        "emission_accounting": {
            "large_construction_sources_opened": 0,
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

    census = document["confirmed_census"]
    need(
        census["B0_occurrence_member_count"]
        + census["B0_virtual_positive_3D_count"]
        + census["B0_virtual_sheet_count"]
        == census["B0_member_count"]
        == MEMBER_COUNT,
        "member census",
    )
    need(
        census["independent_root_obligation_count"]
        + census["dependent_closure_obligation_count"]
        == census["feature_obligation_count"]
        == FEATURE_OBLIGATION_COUNT,
        "obligation census",
    )
    need(
        census["A1"] + census["R1"] + census["G1"]
        == census["independent_root_obligation_count"],
        "root obligation partition",
    )
    need(
        census["A2"] + census["R2"] + census["G2a"] + census["G2b"]
        == census["dependent_closure_obligation_count"],
        "dependent obligation partition",
    )
    need(
        census["graph_sheet_identification_count"]
        + census["graph_side_reference_count"]
        == census["graph_physical_incidence_count"],
        "graph incidence census",
    )
    distinction = document["critical_count_distinction"]
    need(distinction["824864_is_complete_feature_definition_ledger_count"] is False, "no false feature total")
    need(distinction["complete_feature_definition_ledger_count"] is None, "feature total unresolved")
    need(document["candidate_mode"]["enabled"] is False, "candidate disabled")
    need(document["machine_executable_schema_admission"]["implementable_formal_schema_admitted"] is False, "schema not admitted")
    need(document["construction_input_admission"]["producer_authorized"] is False, "producer not authorized")
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
    directory_fd: int,
    filename: str,
    expected_size: int,
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


def verify_scope_inputs() -> dict[str, Any]:
    data = Path(__file__).absolute().parent
    data_before = os.stat(data, follow_symlinks=False)
    need(stat.S_ISDIR(data_before.st_mode), "deliverables directory")
    directory_fd = os.open(
        data,
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
    )
    checked: list[dict[str, Any]] = []
    opened_inputs: list[tuple[str, int, tuple[int, ...]]] = []
    try:
        directory_fingerprint = _fingerprint(data_before)
        need(_fingerprint(os.fstat(directory_fd)) == directory_fingerprint, "deliverables dirfd binding")
        for label, filename, size, expected_sha256 in INPUT_PINS:
            actual, descriptor, opened_fingerprint = _open_and_hash_at(
                directory_fd, filename, size
            )
            opened_inputs.append((filename, descriptor, opened_fingerprint))
            need(actual == expected_sha256, "scope input hash:" + filename)
            checked.append({
                "label": label,
                "filename": filename,
                "exact_size": size,
                "sha256": actual,
            })
        for filename, descriptor, opened_fingerprint in opened_inputs:
            need(
                _fingerprint(os.fstat(descriptor)) == opened_fingerprint,
                "held input fd unchanged:" + filename,
            )
            need(
                _fingerprint(os.stat(filename, dir_fd=directory_fd, follow_symlinks=False))
                == opened_fingerprint,
                "held input pathname rebound:" + filename,
            )
        data_after = os.stat(data, follow_symlinks=False)
        need(_fingerprint(data_after) == directory_fingerprint, "deliverables pathname unchanged")
        need(_fingerprint(os.fstat(directory_fd)) == directory_fingerprint, "deliverables dirfd unchanged")
    finally:
        for _filename, descriptor, _fingerprint_value in reversed(opened_inputs):
            os.close(descriptor)
        os.close(directory_fd)
    result = {
        "schema": SCHEMA + ".scope-input-verification.v1",
        "status": "PASS_EXACT_PRE_SCHEMA_SCOPE_INPUT_PINS__NOT_CONSTRUCTION_ADMISSION",
        "checked_file_count": len(checked),
        "checked_byte_count": sum(row[2] for row in INPUT_PINS),
        "checked_rows_sha256": digest(checked),
        "proof_scope": "ALL_HELD_INPUTS_AT_FINAL_RECHECK_MOMENT_ONLY",
        "input_paths_claimed_immutable_after_return": False,
        "construction_input_set_complete": False,
        "producer_authorized": False,
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
        (("status",), "PASS"),
        (("candidate_is_formal",), True),
        (("scope", "B1A_responsibility", 0), "pair_routing"),
        (("scope", "B1A_exclusions"), []),
        (("scope", "transition_atlas_is_B1A_precondition"), True),
        (("scope", "B1A_formal_must_precede_successor_B2"), False),
        (("confirmed_census", "B0_member_count"), MEMBER_COUNT + 1),
        (("confirmed_census", "feature_obligation_count"), FEATURE_OBLIGATION_COUNT - 1),
        (("confirmed_census", "G2b"), 76_847),
        (("representation_cross_table", 0, 2), 421_803),
        (("critical_count_distinction", "824864_is_complete_feature_definition_ledger_count"), True),
        (("critical_count_distinction", "complete_feature_definition_ledger_count"), FEATURE_OBLIGATION_COUNT),
        (("critical_count_distinction", "primitive_support_partition_derived"), True),
        (("critical_count_distinction", "future_B2_logical_ledger_name"), "source_closure"),
        (("analytic_lineage_feasibility_evidence", "missing_parent_count"), 1),
        (("analytic_lineage_feasibility_evidence", "independent_interval_or_equivalence_reconstruction_complete"), True),
        (("construction_input_admission", "currently_pinned_inputs_are_complete_construction_inputs"), True),
        (("construction_input_admission", "missing_construction_input_families"), []),
        (("construction_input_admission", "producer_may_open_unpinned_construction_source"), True),
        (("construction_input_admission", "producer_authorized"), True),
        (("machine_executable_schema_admission", "family_discriminated_feature_union_frozen"), True),
        (("machine_executable_schema_admission", "typed_scalar_predicate_set_map_AST_grammar_frozen"), True),
        (("machine_executable_schema_admission", "result_schema_frozen"), True),
        (("machine_executable_schema_admission", "candidate_row_credit_must_be_integer_zero"), False),
        (("machine_executable_schema_admission", "candidate_result_is_formal_must_be_false"), False),
        (("machine_executable_schema_admission", "implementable_formal_schema_admitted"), True),
        (("exact_next_closure_order", 0), "implement_private_candidate_producer"),
        (("candidate_mode", "enabled"), True),
        (("candidate_mode", "block_before_any_path_inspection"), False),
        (("candidate_mode", "block_before_any_input_open"), False),
        (("candidate_mode", "candidate_files"), ["forbidden"]),
        (("formal_credit", "feature_definition"), 1),
        (("formal_credit", "transition"), 1),
        (("formal_credit", "D02"), "PASS"),
        (("formal_credit", "CM2"), "GO"),
        (("self_source_seal", "independent_external_source_hash_required"), False),
        (("self_source_seal", "formal_package_claimed"), True),
        (("emission_accounting", "large_construction_sources_opened"), 1),
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
        "status": "PASS_ZERO_CREDIT_PRE_SCHEMA_DOCUMENT_AND_CANDIDATE_BOUNDARY_TEST",
        "contract_sha256": digest(document),
        "semantic_mutations_rejected": rejected,
        "semantic_mutation_count": total,
        "candidate_boundary_probe": boundary,
        "scope_or_construction_inputs_opened": 0,
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
    parser.add_argument("--verify-scope-inputs", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    args = parser.parse_args()
    need(
        sum((
            args.print_contract,
            args.self_test,
            args.verify_scope_inputs,
            args.candidate_dir is not None,
        )) == 1,
        "choose exactly one mode",
    )
    if args.print_contract:
        print(canonical(contract()).decode("ascii"))
    elif args.self_test:
        print(canonical(self_test()).decode("ascii"))
    elif args.verify_scope_inputs:
        print(canonical(verify_scope_inputs()).decode("ascii"))
    else:
        assert args.candidate_dir is not None
        try:
            build_private_candidate(args.candidate_dir)
        except ContractBlocked:
            raise SystemExit(1) from None


if __name__ == "__main__":
    main()
