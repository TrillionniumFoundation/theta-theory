#!/usr/bin/env python3
"""Primitive, C27-independent construction of the 20-family mechanism grammar.

This gate deliberately does not read Round306C27 or any edge ledger.  It
derives eleven support/stratum mechanisms from C25/C26 and nine chart-map
mechanisms from the primitive four-chart atlas.  The finite grammar is
exhaustive and disjoint as syntax.  Physical exhaustiveness remains REJECT
until each terminal has an independent geometry-to-terminal totality proof.

The local evidence binding below is deliberately non-promotional.  It binds
OUTGOING_GRAPHS, SINGLE_GRAPHS, and the exact joint boundary between
INCLUDED_STRATUM_ATTACHMENTS and RETAINED_CONTINUATION.  The latter is only
counted after the corrected 10,660 attachment set is proved disjoint from the
same 276 retained-continuation identities, with union size 10,936.
"""

from __future__ import annotations

import ast
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"
PRIMITIVE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
ATTACHMENT_RECEIPT = "cm2_c27_included_stratum_attachments_subgate_receipt.json"
ATTACHMENT_RECEIPT_SHA256 = "d66d8aacb517a642684f3ddbe184e270936346726b73fa518c76f29076c184f5"
OUTGOING_RECEIPT = "cm2_c27_outgoing_graphs_physical_totality_subgate_receipt.json"
OUTGOING_RECEIPT_SHA256 = "39fc442c396038dfcfd9ca01a99c1188c87015b778bc8d15795a0336a8bbd5e9"
RETAINED_RECEIPT = "cm2_c27_retained_continuation_subgate_receipt.json"
RETAINED_RECEIPT_SHA256 = "08b760876914406e2fbe4e897609afd6ffc6f3667acaf6a1b4a7a9df58f6e263"
SINGLE_RECEIPT = "cm2_c27_single_graphs_subgate_receipt.json"
SINGLE_RECEIPT_SHA256 = "40435bf43d9bab01b54f9bc0a8c283930228e84a33f95d2af14783a2eb1d6ad5"
OWNER_SHADOW_RECEIPT = "cm2_c27_sheet_owner_shadow_physical_totality_subgate_receipt.json"
OWNER_SHADOW_RECEIPT_SHA256 = "2833cc5f1c9d35eeca36722dfb348ad16e9d09e8d44d8983e63b61f390a93d0f"
SAME_CHART_DIRECT_RECEIPT = "cm2_c27_same_chart_exact_equal_cross_component_final_receipt_v2.json"
SAME_CHART_DIRECT_RECEIPT_SHA256 = "bb58cfb7a8929e322c81b8be617a184f523da862cb4d3f4c260acd80a4ba9969"
SAME_CHART_CROSS_RECEIPT = AUDIT / "c27-same-chart-witness-cross-implementation-comparator-20260807T2319" / "cm2_c27_same_chart_witness_cross_implementation_zero_credit_receipt.json"
SAME_CHART_CROSS_RECEIPT_SHA256 = "e4bdb0ca3f594602b61efa218ef3efe62ef048638ba618a443110c66c905eaf1"
PROVISIONAL_OVERLAY_RECEIPT = AUDIT / "c27r1bc-provisional-overlay-v2-final-receipt.json"
PROVISIONAL_OVERLAY_RECEIPT_SHA256 = "cd05b9c1260bc037f38ff5edde22c635a1dc40fe5dff3d10a632b453361ac6de"
BOUNDARY_BLOCKER_RECEIPT = "cm2_c27_boundary_volume_primitive_totality_unresolved_receipt.json"
BOUNDARY_BLOCKER_RECEIPT_SHA256 = "772bdcc750a44400342005c14230e2ea26fdf01c2d92244611ba6f66817689b7"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def canonical_object(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    payload = raw[:-1] if raw.endswith(b"\n") else raw
    need(payload != b"" and b"\n" not in payload, f"single JSON object:{path}")
    value = json.loads(payload)
    need(type(value) is dict and canonical(value) == payload, f"canonical JSON:{path}")
    return value


def closed_object(path: Path, field: str = "result_sha256") -> dict[str, Any]:
    value = canonical_object(path)
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == digest(body), f"object closure:{path}")
    return value


def pinned_closed_receipt(path: Path, expected_file_sha256: str, closure_field: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected_file_sha256, f"receipt file pin:{path}")
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw, f"canonical receipt:{path}")
    body = dict(value)
    claimed = body.pop(closure_field, None)
    need(type(claimed) is str and claimed == digest(body), f"receipt object closure:{path}")
    return value


def rows(name: str):
    with gzip.open(ROOT / name, "rt", encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def attachment_receipt() -> dict[str, Any]:
    raw = (ROOT / ATTACHMENT_RECEIPT).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == ATTACHMENT_RECEIPT_SHA256,
         "included-stratum receipt pin")
    value = json.loads(raw)
    need(canonical(value) + b"\n" == raw, "included-stratum canonical receipt")
    need(
        value["status"]
        == "PASS_LOCAL_ZERO_CREDIT__INCLUDED_STRATUM_ATTACHMENTS_10660__276_EXCLUDED_AND_RESERVED_FOR_OPEN_RETAINED_CONTINUATION"
        and value["candidate_commitment"]["candidate_count"] == 10_660
        and value["candidate_commitment"]["C20D_adjacent_positive_t_excluded_and_reserved_for_open_retained_continuation"] == 276
        and value["candidate_commitment"]["candidate_excluded_intersection_count"] == 0
        and value["candidate_commitment"]["candidate_plus_excluded_union_count"] == 10_936
        and value["candidate_commitment"]["candidate_representation_ids_sha256"] == "3c18dda4883dcc9a357d898ffa7c0f126b7a1ffde985bc77a879369b2978c511"
        and value["candidate_commitment"]["excluded_adjacent_representation_ids_sha256"] == "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd"
        and value["cross_implementation_exact_commitments_identical"] is True
        and value["attack_harness"]["attack_count"] == 29
        and value["attack_harness"]["all_rejected"] is True
        and value["retained_continuation_terminal_closed"] is False
        and value["terminal_credit_withheld_until_retained_continuation_joint_boundary"] is True
        and value["formal_credit"] == 0
        and value["C27_C28_C29"] == "REJECT_PENDING_REMAINING_TERMINALS"
        and value["CM2"] == "NO-GO_FOR_CLAIM",
        "included-stratum truthful zero-credit closure",
    )
    for name, expected in {
        "cm2_c27_included_stratum_attachments_stream_probe.py": value["stream_implementation"]["script_sha256"],
        "cm2_c27_included_stratum_attachments_sqlite_probe.py": value["sqlite_implementation"]["script_sha256"],
        "cm2_c27_included_stratum_attachments_attack_harness.py": value["attack_harness"]["script_sha256"],
    }.items():
        need(file_hash(ROOT / name) == expected, f"included-stratum script pin:{name}")
    stream_paths = [
        AUDIT / "c27-included-stratum-c20d-split-v2b-stream-seed-101" / "result.json",
        AUDIT / "c27-included-stratum-c20d-split-v2b-stream-seed-909" / "result.json",
    ]
    sqlite_paths = [
        AUDIT / "c27-included-stratum-c20d-split-v2b-sqlite-seed-101" / "result.json",
        AUDIT / "c27-included-stratum-c20d-split-v2b-sqlite-seed-909" / "result.json",
    ]
    attack_path = AUDIT / "c27-included-stratum-c20d-split-v2b-attacks-101" / "result.json"
    need(stream_paths[0].read_bytes() == stream_paths[1].read_bytes(), "included-stratum stream two-seed bytes")
    need(sqlite_paths[0].read_bytes() == sqlite_paths[1].read_bytes(), "included-stratum sqlite two-seed bytes")
    stream_result = closed_object(stream_paths[0])
    sqlite_result = closed_object(sqlite_paths[0])
    attack_result = closed_object(attack_path)
    need(file_hash(stream_paths[0]) == value["stream_implementation"]["result_file_sha256"], "included-stratum stream evidence hash")
    need(file_hash(sqlite_paths[0]) == value["sqlite_implementation"]["result_file_sha256"], "included-stratum sqlite evidence hash")
    need(file_hash(attack_path) == value["attack_harness"]["result_file_sha256"], "included-stratum attack evidence hash")
    need(stream_result["result_sha256"] == value["stream_implementation"]["result_sha256"], "included-stratum stream object pin")
    need(sqlite_result["result_sha256"] == value["sqlite_implementation"]["result_sha256"], "included-stratum sqlite object pin")
    need(attack_result["result_sha256"] == value["attack_harness"]["result_sha256"], "included-stratum attack object pin")
    for result in (stream_result, sqlite_result):
        need(
            result["candidate_universe"]["candidate_count"] == 10_660
            and result["candidate_universe"]["candidate_excluded_intersection_count"] == 0
            and result["candidate_universe"]["candidate_plus_excluded_union_count"] == 10_936
            and result["candidate_universe"]["candidate_representation_ids_sha256"]
            == "3c18dda4883dcc9a357d898ffa7c0f126b7a1ffde985bc77a879369b2978c511"
            and result["candidate_universe"]["excluded_adjacent_representation_ids_sha256"]
            == "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd"
            and result["candidate_universe"]["candidate_plus_excluded_union_ids_sha256"]
            == "e2ffc75d183889b90eee29d15e0c0783976d8290ebde977c3081a82bf57c602f"
            and all(count == 0 for count in result["join_gap_census"].values()),
            "included-stratum runtime exact boundary",
        )
    need(
        attack_result["attack_count"] == 29
        and attack_result["rejected_count"] == 29
        and attack_result["all_rejected"] is True,
        "included-stratum runtime attacks",
    )
    return {
        "terminal": "INCLUDED_STRATUM_ATTACHMENTS",
        "receipt_filename": ATTACHMENT_RECEIPT,
        "receipt_sha256": ATTACHMENT_RECEIPT_SHA256,
        "candidate_count": 10_660,
        "candidate_representation_ids_sha256": "3c18dda4883dcc9a357d898ffa7c0f126b7a1ffde985bc77a879369b2978c511",
        "excluded_adjacent_count": 276,
        "excluded_adjacent_representation_ids_sha256": "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd",
        "candidate_plus_excluded_union_count": 10_936,
        "candidate_plus_excluded_union_ids_sha256": "e2ffc75d183889b90eee29d15e0c0783976d8290ebde977c3081a82bf57c602f",
        "terminal_credit_counted_after_joint_boundary": True,
        "paired_terminal": "RETAINED_CONTINUATION",
        "formal_credit": 0,
    }


def outgoing_receipt() -> dict[str, Any]:
    raw = (ROOT / OUTGOING_RECEIPT).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == OUTGOING_RECEIPT_SHA256,
         "outgoing-graphs receipt pin")
    value = json.loads(raw)
    need(canonical(value) + b"\n" == raw, "outgoing-graphs canonical receipt")
    body = dict(value)
    claimed = body.pop("receipt_sha256", None)
    need(isinstance(claimed, str) and claimed == digest(body),
         "outgoing-graphs receipt closure")
    need(
        value["status"]
        == "PASS_OUTGOING_GRAPHS_DUAL_SEMANTICS_DOUBLE_SEED_31_ATTACKS__ZERO_CREDIT"
        and value["fresh_G1_partition"] == {"DOUBLE": 16, "OUTGOING": 264, "SINGLE": 4_984}
        and value["outgoing_roots"] == 264
        and value["G2A_sheet_dispositions"] == 264
        and value["G2B_side_dispositions"] == 528
        and value["unresolved"] == 0
        and value["stream_double_seed_byte_identical"] is True
        and value["sqlite_double_seed_byte_identical"] is True
        and value["cross_implementation_per_candidate_digest_mismatch"] == 0
        and value["coherent_attacks_rejected"] == 31
        and value["C27_FAMILIES_imported_or_read"] is False
        and value["edge_ledger_used_as_candidate_universe"] is False
        and value["formal_credit"] == 0
        and value["strict_nonpromotion"] == {
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "outgoing-graphs truthful zero-credit closure",
    )
    return {
        "terminal": "OUTGOING_GRAPHS",
        "receipt_filename": OUTGOING_RECEIPT,
        "receipt_sha256": OUTGOING_RECEIPT_SHA256,
        "candidate_count": 264,
        "formal_credit": 0,
    }


def retained_receipt() -> dict[str, Any]:
    raw = (ROOT / RETAINED_RECEIPT).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == RETAINED_RECEIPT_SHA256,
         "retained-continuation receipt pin")
    value = json.loads(raw)
    need(canonical(value) + b"\n" == raw, "retained-continuation canonical receipt")
    need(
        value["status"]
        == "PASS_LOCAL_ZERO_CREDIT__RETAINED_CONTINUATION_PHYSICAL_TOTALITY_AND_UNIQUE_ASSIGNMENT"
        and value["terminal"] == "RETAINED_CONTINUATION"
        and value["candidate_commitment"]["candidate_count"] == 276
        and value["candidate_commitment"]["candidate_representation_ids_sha256"]
        == "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd"
        and value["candidate_commitment"]["candidate_row_sequence_sha256"]
        == "73c46567074bb302e7e16e61742445da1365a7d778cf31843ec95f6c5d5fa0aa"
        and value["primitive_identity_route"]["C20D_row_count"] == 2_520
        and value["primitive_identity_route"]["R295A_row_count"] == 276
        and value["primitive_identity_route"]["unresolved"] == 0
        and value["cross_implementation_exact_commitments_identical"] is True
        and value["attack_harness"]["attack_count"] == 38
        and value["attack_harness"]["all_rejected"] is True
        and value["formal_credit"] == 0
        and value["C27_C28_C29"] == "REJECT_PENDING_REMAINING_TERMINALS"
        and value["CM2"] == "NO-GO_FOR_CLAIM",
        "retained-continuation truthful zero-credit closure",
    )
    for name, expected in {
        "cm2_c27_retained_continuation_stream_probe.py": value["script_pins"]["stream_probe"],
        "cm2_c27_retained_continuation_sqlite_verifier.py": value["script_pins"]["sqlite_verifier"],
        "cm2_c27_retained_continuation_attack_harness.py": value["script_pins"]["attack_harness"],
    }.items():
        need(file_hash(ROOT / name) == expected, f"retained-continuation script pin:{name}")
    stream_paths = [
        AUDIT / "c27-retained-continuation-stream-v4-seed-30627401" / "result.json",
        AUDIT / "c27-retained-continuation-stream-v4-seed-30627941" / "result.json",
    ]
    sqlite_paths = [
        AUDIT / "c27-retained-continuation-sqlite-v2-seed-30627402" / "result.json",
        AUDIT / "c27-retained-continuation-sqlite-v2-seed-30627942" / "result.json",
    ]
    attack_path = AUDIT / "c27-retained-continuation-attacks-v2" / "result.json"
    need(stream_paths[0].read_bytes() == stream_paths[1].read_bytes(), "retained stream two-seed bytes")
    need(sqlite_paths[0].read_bytes() == sqlite_paths[1].read_bytes(), "retained sqlite two-seed bytes")
    for path in stream_paths + sqlite_paths:
        need((path.parent / "stderr.txt").read_bytes() == b"", f"retained empty stderr:{path.parent.name}")
    stream_result = closed_object(stream_paths[0])
    sqlite_result = closed_object(sqlite_paths[0])
    attack_result = closed_object(attack_path)
    need(file_hash(stream_paths[0]) == value["implementation_runs"]["stream"]["result_sha256"], "retained stream evidence hash")
    need(file_hash(sqlite_paths[0]) == value["implementation_runs"]["sqlite"]["result_sha256"], "retained sqlite evidence hash")
    need(file_hash(attack_path) == value["attack_harness"]["result_sha256"], "retained attack evidence hash")
    need(stream_result["result_sha256"] == value["implementation_runs"]["stream"]["result_object_sha256"], "retained stream object pin")
    need(sqlite_result["result_sha256"] == value["implementation_runs"]["sqlite"]["result_object_sha256"], "retained sqlite object pin")
    need(attack_result["result_sha256"] == value["attack_harness"]["result_object_sha256"], "retained attack object pin")
    for result in (stream_result, sqlite_result):
        need(
            result["candidate_universe"]["candidate_count"] == 276
            and result["candidate_universe"]["candidate_representation_ids_sha256"]
            == "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd"
            and result["candidate_universe"]["candidate_row_sequence_sha256"]
            == "73c46567074bb302e7e16e61742445da1365a7d778cf31843ec95f6c5d5fa0aa"
            and result["attachment_terminal_overlap_after_required_C20D_SOURCE_SPLIT"] == 0
            and all(count == 0 for count in result["join_gap_census"].values()),
            "retained runtime exact boundary",
        )
    need(
        attack_result["attack_count"] == 38
        and attack_result["rejected_count"] == 38
        and attack_result["baseline_candidate_representation_ids_sha256"]
        == "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd",
        "retained runtime attacks",
    )
    return {
        "terminal": "RETAINED_CONTINUATION",
        "receipt_filename": RETAINED_RECEIPT,
        "receipt_sha256": RETAINED_RECEIPT_SHA256,
        "candidate_count": 276,
        "candidate_representation_ids_sha256": "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd",
        "candidate_row_sequence_sha256": "73c46567074bb302e7e16e61742445da1365a7d778cf31843ec95f6c5d5fa0aa",
        "terminal_credit_counted_after_joint_boundary": True,
        "paired_terminal": "INCLUDED_STRATUM_ATTACHMENTS",
        "formal_credit": 0,
    }


def single_receipt() -> dict[str, Any]:
    raw = (ROOT / SINGLE_RECEIPT).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SINGLE_RECEIPT_SHA256,
         "single-graphs receipt pin")
    value = json.loads(raw)
    need(canonical(value) + b"\n" == raw, "single-graphs canonical receipt")
    expected_allocation = {
        "C24A": {
            "DOUBLE_GRAPHS": {"G2A": 16, "G2B": 16},
            "OUTGOING_GRAPHS": {"G2A": 264, "G2B": 528},
            "SINGLE_GRAPHS": {"G2A": 4_984, "G2B": 9_416},
        },
        "C24B": {
            "DOUBLE_GRAPHS": {"G2B": 16},
            "OUTGOING_GRAPHS": {},
            "SINGLE_GRAPHS": {"G2B": 152},
        },
    }
    need(
        value["status"] == "PASS_LOCAL_ZERO_CREDIT__SINGLE_GRAPHS_PHYSICAL_TOTALITY_AND_UNIQUE_ASSIGNMENT"
        and value["terminal"] == "SINGLE_GRAPHS"
        and value["single_roots"] == 4_984
        and value["single_graph_class_partition"]
        == {"R235_SOURCE_EXACT_FACE_FULL_BASE": 552, "R235_TARGET_POSITIVE_PARTIAL_BASE": 4_432}
        and value["C24_full_terminal_allocation"] == expected_allocation
        and value["materialized_C15_C24_C25_C26_proof_rows"] == 14_552
        and value["unresolved"] == 0
        and value["stream_double_seed_byte_identical"] is True
        and value["sqlite_double_seed_byte_identical"] is True
        and value["cross_implementation_per_candidate_digest_mismatch"] == 0
        and value["attack_harness"] == {
            "all_rejected": True,
            "attack_count": 48,
            "result_sha256": "0beedda9f87830355755504533e718d2043e0500f0dd514399cc84e79a5bc9a7",
        }
        and value["formal_credit"] == 0
        and value["C27_C28_C29"] == "REJECT_PENDING_REMAINING_TERMINALS"
        and value["CM2"] == "NO-GO_FOR_CLAIM",
        "single-graphs truthful zero-credit closure",
    )
    script_names = {
        "stream_probe": "cm2_c27_single_graphs_physical_totality_stream_probe.py",
        "sqlite_verifier": "cm2_c27_single_graphs_physical_totality_sqlite_verifier.py",
        "attack_harness": "cm2_c27_single_graphs_physical_totality_attack_harness.py",
        "final_receipt_builder": "cm2_c27_single_graphs_physical_totality_final_receipt_builder.py",
    }
    for key, name in script_names.items():
        need(file_hash(ROOT / name) == value["script_pins"][key], f"single-graphs script pin:{name}")
    final_path = ROOT.parent / value["runtime_receipt"]["path"]
    need(file_hash(final_path) == value["runtime_receipt"]["file_sha256"], "single final receipt file hash")
    final = closed_object(final_path, "receipt_sha256")
    need(final["receipt_sha256"] == value["runtime_receipt"]["internal_receipt_sha256"], "single final receipt closure")
    need(
        final["status"] == "PASS_SINGLE_GRAPHS_DUAL_SEMANTICS_DOUBLE_SEED_48_ATTACKS__ZERO_CREDIT"
        and final["single_roots"] == 4_984
        and final["C24_full_terminal_allocation"] == expected_allocation
        and final["G2A_sheet_dispositions"] == 4_984
        and final["G2B_positive_side_dispositions"] == 9_416
        and final["G2B_exact_empty_side_dispositions"] == 152
        and final["unresolved"] == 0
        and final["coherent_attacks_rejected"] == 48
        and final["formal_credit"] == 0,
        "single final runtime semantics",
    )
    runtime_paths = {
        "stream_seed_A": AUDIT / "c27-single-graphs-stream-seed-30628101",
        "stream_seed_B": AUDIT / "c27-single-graphs-stream-seed-30628901",
        "sqlite_seed_A": AUDIT / "c27-single-graphs-sqlite-verify-seed-30628201",
        "sqlite_seed_B": AUDIT / "c27-single-graphs-sqlite-verify-seed-30628902",
        "attacks": AUDIT / "c27-single-graphs-attacks-30628301",
    }
    for group, members in final["evidence"].items():
        for name, expected in members.items():
            need(file_hash(runtime_paths[group] / name) == expected, f"single runtime evidence:{group}/{name}")
    need(
        (runtime_paths["stream_seed_A"] / "ledger.jsonl.gz").read_bytes()
        == (runtime_paths["stream_seed_B"] / "ledger.jsonl.gz").read_bytes()
        and (runtime_paths["stream_seed_A"] / "result.json").read_bytes()
        == (runtime_paths["stream_seed_B"] / "result.json").read_bytes()
        and (runtime_paths["stream_seed_A"] / "manifest.json").read_bytes()
        == (runtime_paths["stream_seed_B"] / "manifest.json").read_bytes(),
        "single stream two-seed bytes",
    )
    need(
        (runtime_paths["sqlite_seed_A"] / "verification.json").read_bytes()
        == (runtime_paths["sqlite_seed_B"] / "verification.json").read_bytes(),
        "single sqlite two-seed bytes",
    )
    stream_result = closed_object(runtime_paths["stream_seed_A"] / "result.json")
    sqlite_result = closed_object(runtime_paths["sqlite_seed_A"] / "verification.json", "verification_sha256")
    attack_result = closed_object(runtime_paths["attacks"] / "attack_result.json")
    need(
        stream_result["single_root_count"] == 4_984
        and stream_result["unresolved_count"] == 0
        and sqlite_result["candidate_count"] == 4_984
        and sqlite_result["per_candidate_digest_mismatch_count"] == 0
        and attack_result["attack_count"] == 48
        and attack_result["rejected_count"] == 48
        and attack_result["unexpected_accept_count"] == 0,
        "single runtime exact evidence",
    )
    return {
        "terminal": "SINGLE_GRAPHS",
        "receipt_filename": SINGLE_RECEIPT,
        "receipt_sha256": SINGLE_RECEIPT_SHA256,
        "candidate_count": 4_984,
        "materialized_proof_row_count": 14_552,
        "terminal_credit_counted": True,
        "formal_credit": 0,
    }


def retained_attachment_joint_boundary(
    attachment: dict[str, Any], retained: dict[str, Any]
) -> dict[str, Any]:
    retained_digest = "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd"
    need(attachment["candidate_count"] == 10_660, "joint attachment count")
    need(retained["candidate_count"] == 276, "joint retained count")
    need(attachment["excluded_adjacent_count"] == retained["candidate_count"], "joint retained cardinality")
    need(attachment["excluded_adjacent_representation_ids_sha256"] == retained_digest, "joint attachment excluded digest")
    need(retained["candidate_representation_ids_sha256"] == retained_digest, "joint retained candidate digest")
    need(attachment["candidate_plus_excluded_union_count"] == 10_936 == 10_660 + 276, "joint disjoint union count")
    return {
        "terminals": ["INCLUDED_STRATUM_ATTACHMENTS", "RETAINED_CONTINUATION"],
        "status": "PASS_EXACT_DISJOINT_JOINT_BOUNDARY__10660_ATTACHMENTS_PLUS_276_RETAINED_EQUALS_10936",
        "attachment_candidate_count": 10_660,
        "retained_candidate_count": 276,
        "intersection_count": 0,
        "union_count": 10_936,
        "attachment_candidate_representation_ids_sha256": attachment["candidate_representation_ids_sha256"],
        "retained_candidate_representation_ids_sha256": retained_digest,
        "attachment_excluded_adjacent_representation_ids_sha256": retained_digest,
        "union_representation_ids_sha256": attachment["candidate_plus_excluded_union_ids_sha256"],
        "both_terminal_credits_counted": True,
        "formal_credit": 0,
    }


def owner_shadow_receipt() -> dict[str, Any]:
    value = pinned_closed_receipt(
        ROOT / OWNER_SHADOW_RECEIPT,
        OWNER_SHADOW_RECEIPT_SHA256,
        "receipt_sha256",
    )
    need(
        value["receipt_sha256"] == "1e8216806e7efcf3f19d7fbe7de61879f6cd8ca1e970cfb592f237370fa95c2c"
        and value["status"] == "PASS_SHEET_OWNER_SHADOW_DUAL_PHYSICAL_SEMANTICS_DOUBLE_SEED_50_ATTACKS__ZERO_CREDIT"
        and value["primitive_candidate_generation"] == {"R204": 224, "R211": 17_716, "total": 17_940}
        and value["terminal_census"] == {"SHEET_OWNER": 17_940, "SHEET_SHADOW": 17_940}
        and value["role_rows"] == 35_880
        and value["materialized_shadow_companions"] == 17_940
        and value["unresolved"] == 0
        and value["legal_cross_component_witness"] == 0
        and value["cross_implementation_role_row_mismatch"] == 0
        and value["cross_implementation_shadow_row_mismatch"] == 0
        and value["stream_double_seed_ledger_byte_identical"] is True
        and value["sqlite_cross_seed_semantic_projection_identical"] is True
        and value["coherent_attacks_rejected"] == 50
        and value["primitive_candidates_generated_before_C21_C25_C26_binding"] is True
        and value["C27_FAMILIES_imported_or_read"] is False
        and value["edge_ledger_used_as_candidate_universe"] is False
        and value["formal_credit"] == 0
        and value["strict_nonpromotion"] == {
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "owner/shadow physical-totality receipt semantics",
    )
    return {
        "terminals": ["SHEET_OWNER", "SHEET_SHADOW"],
        "receipt_filename": OWNER_SHADOW_RECEIPT,
        "receipt_file_sha256": OWNER_SHADOW_RECEIPT_SHA256,
        "receipt_object_sha256": value["receipt_sha256"],
        "candidate_count_per_terminal": 17_940,
        "unresolved": 0,
        "legal_cross_component_witness": 0,
        "dual_semantics_double_seed": True,
        "coherent_attacks_rejected": 50,
        "formal_credit": 0,
    }


def same_chart_witness_evidence() -> dict[str, Any]:
    direct = pinned_closed_receipt(
        ROOT / SAME_CHART_DIRECT_RECEIPT,
        SAME_CHART_DIRECT_RECEIPT_SHA256,
        "receipt_sha256",
    )
    cross = pinned_closed_receipt(
        SAME_CHART_CROSS_RECEIPT,
        SAME_CHART_CROSS_RECEIPT_SHA256,
        "receipt_sha256",
    )
    need(
        direct["status"] == "PASS_FINAL_ZERO_CREDIT__INDEPENDENT_228_GROUP_SAME_CHART_POSITIVE_VOLUME_CROSS_COMPONENT_WITNESSES__C27_C28_C29_REBUILD_REQUIRED"
        and direct["legal_cross_component_witness_found"] is True
        and direct["witness_census"] == {
            "cross_component_member_pair_count": 228,
            "duplicate_exact_box_group_count": 134_968,
            "witness_component_occurrence_count": 456,
            "witness_group_count": 228,
            "witness_member_count": 456,
        }
        and direct["observed_witness_structure"]["strict_positive_volume_groups"] == 228
        and direct["observed_witness_structure"]["source_pair"] == "C22A+C22A"
        and direct["observed_witness_structure"]["support_kind_pair"] == "OPEN_RATIONAL_BOX+OPEN_RATIONAL_BOX"
        and direct["endpoint_bits_needed_for_these_witnesses"] is False
        and direct["double_seed_ledger_byte_identical"] is True
        and direct["cross_seed_semantic_projection_identical"] is True
        and direct["attack_count"] == 27
        and direct["C27_C28_C29"] == "REJECT_AND_REBUILD_REQUIRED"
        and direct["formal_credit"] == 0,
        "same-chart direct-source witness receipt semantics",
    )
    exact = cross["cross_implementation_exact_match"]
    need(
        cross["status"] == "PASS_FINAL_ZERO_CREDIT__TWO_INDEPENDENT_IMPLEMENTATIONS_EXACTLY_MATCH_228_GROUPS_AND_456_PROJECTIONS__192_COMPONENT_EDGES_FORCE_DSU_RANK_192__C27_C28_C29_REBUILD_REQUIRED"
        and cross["legal_cross_component_witness_found"] is True
        and exact["group_count"] == 228
        and exact["projection_count"] == 456
        and exact["unique_component_edge_count"] == 192
        and exact["affected_component_vertex_count"] == 312
        and exact["connected_component_count_on_affected_vertices"] == 120
        and exact["DSU_rank_reduction"] == 192
        and exact["group_ids_sha256"] == direct["group_ids_sha256"]
        and cross["attack_count"] == 20
        and cross["formal_credit"] == 0
        and cross["C27_C28_C29"] == "REJECT_AND_REBUILD_REQUIRED",
        "same-chart cross-implementation witness receipt semantics",
    )
    return {
        "terminal": "SAME_CHART_RELATIVE_CELLS",
        "terminal_state": "OPEN_TOTALITY_WITH_CONFIRMED_LEGAL_WITNESSES",
        "source_direct_receipt_filename": SAME_CHART_DIRECT_RECEIPT,
        "source_direct_receipt_file_sha256": SAME_CHART_DIRECT_RECEIPT_SHA256,
        "source_direct_receipt_object_sha256": direct["receipt_sha256"],
        "cross_implementation_receipt_path": str(SAME_CHART_CROSS_RECEIPT.relative_to(ROOT.parent)),
        "cross_implementation_receipt_file_sha256": SAME_CHART_CROSS_RECEIPT_SHA256,
        "cross_implementation_receipt_object_sha256": cross["receipt_sha256"],
        "witness_group_count": 228,
        "witness_projection_count": 456,
        "unique_component_edge_count": 192,
        "affected_component_vertex_count": 312,
        "forced_DSU_rank_reduction": 192,
        "legal_cross_component_witness_found": True,
        "same_chart_totality_proved": False,
        "required_governance_action": "REBUILD_C27_THROUGH_C29__PATCHING_OR_PRESERVING_C29_UNCONDITIONAL_AUTHORITY_IS_FORBIDDEN",
        "formal_credit": 0,
    }


def provisional_overlay_evidence() -> dict[str, Any]:
    value = pinned_closed_receipt(
        PROVISIONAL_OVERLAY_RECEIPT,
        PROVISIONAL_OVERLAY_RECEIPT_SHA256,
        "receipt_object_sha256",
    )
    census = value["census"]
    need(
        value["status"] == "PASS_PROVISIONAL_UPPER_BOUND_ONLY__APPEND_ONLY__ZERO_FORMAL_CREDIT"
        and value["authority_limit"] == "WITNESS_ONLY_PROVISIONAL_OVERLAY__NOT_A_FORMAL_C27R1_C28R1_OR_C29R1_SEAL"
        and census["old_components"] == 57_876
        and census["certain_component_edges"] == 192
        and census["forced_rank_reduction"] == 192
        and census["affected_vertices"] == 312
        and census["affected_clusters"] == 120
        and census["provisional_components"] == 57_684
        and census["newly_internalized_pairs"] == 691_416
        and census["provisional_cross_denominator"] == 125_615_784_254
        and value["qualification"]["partition"] == "PROVISIONAL_UPPER_BOUND_ONLY"
        and value["qualification"]["twenty_family_totality"] == "OPEN"
        and value["qualification"]["C28"] == "REJECT"
        and value["qualification"]["C29"] == "REJECT"
        and value["formal_credit"] == 0
        and value["forbidden_state_changes"]["old_C27_C28_C29_modified"] is False
        and value["forbidden_state_changes"]["formal_seal_published"] is False,
        "provisional overlay authority limit",
    )
    return {
        "receipt_path": str(PROVISIONAL_OVERLAY_RECEIPT.relative_to(ROOT.parent)),
        "receipt_file_sha256": PROVISIONAL_OVERLAY_RECEIPT_SHA256,
        "receipt_object_sha256": value["receipt_object_sha256"],
        "authority": "PROVISIONAL_UPPER_BOUND_ONLY__NOT_MAXIMALITY__NOT_FORMAL_C27R1_C28R1_C29R1",
        "old_component_count": 57_876,
        "provisional_component_count": 57_684,
        "forced_rank_reduction": 192,
        "newly_internalized_pairs": 691_416,
        "formal_credit": 0,
    }


def boundary_blocker_evidence() -> dict[str, Any]:
    value = pinned_closed_receipt(
        ROOT / BOUNDARY_BLOCKER_RECEIPT,
        BOUNDARY_BLOCKER_RECEIPT_SHA256,
        "receipt_sha256",
    )
    missing = value["minimal_missing_authority"]
    need(
        value["status"] == "PASS_EXACT_BLOCKER_MATERIALIZATION__SIGNED_COMPLETE_POSITIVE_TERMINALS_REMAIN_OPEN__ZERO_CREDIT"
        and value["double_seed"] == {"ledger_byte_identical": True, "result_byte_identical": True, "seeds": [30628111, 30628991]}
        and value["attack_harness"]["attack_count"] == 27
        and value["attack_harness"]["all_rejected"] is True
        and missing["C19C_half_open_atom_count"] == 33_344
        and missing["endpoint_ownership_bit_count"] == 200_064
        and missing["C26_direct_three_terminal_assignment_row_count"] == 0
        and missing["three_terminal_unassigned_atom_count"] == 483_232
        and value["terminal_credit_counted"] == {
            "COMPLETE_BOUNDARY_FACES": False,
            "POSITIVE_VOLUME_CARRIERS": False,
            "SIGNED_BOUNDARY_FACES": False,
        }
        and value["formal_credit"] == 0,
        "boundary/volume exact blocker receipt semantics",
    )
    return {
        "terminals": ["SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES", "POSITIVE_VOLUME_CARRIERS"],
        "terminal_state": "OPEN_EXACT_BLOCKERS_MATERIALIZED",
        "receipt_filename": BOUNDARY_BLOCKER_RECEIPT,
        "receipt_file_sha256": BOUNDARY_BLOCKER_RECEIPT_SHA256,
        "receipt_object_sha256": value["receipt_sha256"],
        "C19C_half_open_atom_count": 33_344,
        "missing_endpoint_ownership_bit_count": 200_064,
        "C26_direct_three_terminal_assignment_row_count": 0,
        "three_terminal_unassigned_atom_count": 483_232,
        "double_seed_byte_identical": True,
        "coherent_attacks_rejected": 27,
        "formal_credit": 0,
    }


def primitive_charts() -> tuple[str, ...]:
    tree = ast.parse((ROOT / PRIMITIVE).read_text(encoding="utf-8"), filename=PRIMITIVE)
    geometry = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "geometry")
    cells = []
    for node in ast.walk(geometry):
        if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
            continue
        if ast.unparse(node.test.left) != "cell" or len(node.test.comparators) != 1:
            continue
        value = node.test.comparators[0]
        if isinstance(value, ast.Constant) and value.value in {"E", "W", "N", "S"}:
            cells.append(str(value.value))
    need(set(cells) == {"E", "W", "N", "S"}, "primitive four-chart cover")
    return ("E", "N", "W", "S")


def construct_terminals(cycle: tuple[str, ...]) -> list[dict[str, Any]]:
    strata = (
        "SAME_CHART_RELATIVE_CELLS", "RETAINED_CONTINUATION", "OUTGOING_GRAPHS",
        "SINGLE_GRAPHS", "DOUBLE_GRAPHS", "SHEET_OWNER", "SHEET_SHADOW",
        "SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES",
        "POSITIVE_VOLUME_CARRIERS", "INCLUDED_STRATUM_ATTACHMENTS",
    )
    output = [{"branch": "SUPPORT_STRATUM", "terminal": name} for name in strata]
    output.append({"branch": "ATLAS_MAP", "terminal": "REVERSE_RECHART"})
    output.extend({
        "branch": "ATLAS_MAP", "terminal": f"TRUE_CYCLIC_SEAM_{cycle[i]}_TO_{cycle[(i+1)%4]}"
    } for i in range(4))
    # The nonidentity elements of the two-reflection Klein group are physical
    # actions, not quotient glues.
    output.extend({"branch": "PHYSICAL_ACTION_NEGATIVE_CONTROL", "terminal": name}
                  for name in ("Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL", "JxJy_NEGATIVE_CONTROL"))
    output.append({"branch": "REPRESENTATION_MAP", "terminal": "REPRESENTATION_ALIASES"})
    need(len(output) == 20 and len({row["terminal"] for row in output}) == 20, "20 unique grammar terminals")
    for ordinal, row in enumerate(output):
        row["ordinal"] = ordinal
        row["row_sha256"] = digest(row)
    return output


def main() -> int:
    cycle = primitive_charts()
    terminals = construct_terminals(cycle)
    included_stratum_receipt = attachment_receipt()
    outgoing_graphs_receipt = outgoing_receipt()
    retained_continuation_receipt = retained_receipt()
    single_graphs_receipt = single_receipt()
    owner_shadow = owner_shadow_receipt()
    same_chart_witnesses = same_chart_witness_evidence()
    provisional_overlay = provisional_overlay_evidence()
    boundary_blockers = boundary_blocker_evidence()
    joint_boundary = retained_attachment_joint_boundary(
        included_stratum_receipt, retained_continuation_receipt
    )
    c15_count = sum(1 for _ in rows(C15))
    need(c15_count == 502_204, "C15 universe")
    c25_kernels: Counter[str] = Counter()
    c25_semantics: Counter[str] = Counter()
    for row in rows(C25):
        c25_kernels[row["source_bindings"]["support_kernel"]] += 1
        c25_semantics[row["support_semantic_kind"]] += 1
    need(sum(c25_kernels.values()) == 502_204, "C25 universe")
    need(c25_semantics == {
        "EXACT_EMPTY_MEMBER_SUPPORT_EQUALITY": 168,
        "EXACT_MEMBER_SUPPORT_EQUALITY": 182_072,
        "FINITE_CELL_UNION_MEMBER_SUPPORT_EQUALITY": 304_740,
        "RELATION_BACKED_MEMBER_SUPPORT_EQUALITY": 15_224,
    }, "C25 semantic partition")
    c26_kinds: Counter[str] = Counter()
    c26_nodes: Counter[str] = Counter()
    for row in rows(C26):
        c26_kinds[row["obligation_kind"]] += 1
        c26_nodes[row["node_id"]] += 1
    need(sum(c26_kinds.values()) == 691_424, "C26 feature universe")
    need(set(c26_nodes) == {"A1", "A2", "G1", "G2A", "G2B", "R1", "R2"}, "C26 node grammar")

    # These are the precise remaining totality obligations.  A terminal is
    # not promoted merely because it is syntactically present.
    obligations = []
    closed = {
        "DOUBLE_GRAPHS", "REPRESENTATION_ALIASES", "REVERSE_RECHART",
        "TRUE_CYCLIC_SEAM_E_TO_N", "TRUE_CYCLIC_SEAM_N_TO_W",
        "TRUE_CYCLIC_SEAM_W_TO_S", "TRUE_CYCLIC_SEAM_S_TO_E",
        "Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL", "JxJy_NEGATIVE_CONTROL",
        "OUTGOING_GRAPHS",
        "RETAINED_CONTINUATION", "SINGLE_GRAPHS", "INCLUDED_STRATUM_ATTACHMENTS",
        "SHEET_OWNER", "SHEET_SHADOW",
    }
    for terminal in terminals:
        name = terminal["terminal"]
        state = (
            "LOCAL_SUBGATE_CLOSED_ZERO_CREDIT"
            if name in closed
            else "INDEPENDENT_TOTALITY_PROOF_REQUIRED"
        )
        obligations.append({
            "terminal": name,
            "state": state,
            "must_prove_candidate_generation_from_primitive_geometry": True,
            "must_prove_unique_terminal_assignment": True,
            "must_reject_or_route_every_cross_component_witness": True,
        })
    result = {
        "status": "REJECT_ZERO_CREDIT__16_OF_20_TERMINALS_EVIDENCE_CLOSED__228_LEGAL_SAME_CHART_WITNESS_GROUPS_FORCE_C27_C28_C29_REBUILD__4_TOTALITY_PROOFS_REMAIN",
        "C27_source_or_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "primitive_chart_cycle": list(cycle),
        "grammar": {
            "support_stratum_terminal_count": 11,
            "atlas_or_action_or_representation_terminal_count": 9,
            "terminal_count": 20,
            "terminals": terminals,
            "syntactic_coverage": "PASS",
            "syntactic_mutual_exclusivity": "PASS",
            "physical_totality": "REJECT__LEGAL_CROSS_COMPONENT_WITNESSES_FOUND__4_TERMINALS_OPEN",
        },
        "primitive_universes": {
            "C15_member_count": c15_count,
            "C25_support_kernel_census": dict(sorted(c25_kernels.items())),
            "C25_support_semantic_census": dict(sorted(c25_semantics.items())),
            "C26_feature_count": sum(c26_kinds.values()),
            "C26_node_census": dict(sorted(c26_nodes.items())),
            "C26_obligation_kind_census": dict(sorted(c26_kinds.items())),
        },
        "terminal_obligations": obligations,
        "closed_subgate_receipts": [
            retained_continuation_receipt,
            outgoing_graphs_receipt,
            single_graphs_receipt,
            included_stratum_receipt,
            owner_shadow,
        ],
        "same_chart_legal_witness_evidence": same_chart_witnesses,
        "boundary_volume_unresolved_evidence": boundary_blockers,
        "C27R1BC_provisional_overlay": provisional_overlay,
        "joint_boundary_bindings": [joint_boundary],
        "withheld_joint_boundary_receipts": [],
        "closed_zero_credit_terminal_count": 16,
        "remaining_terminal_totality_proof_count": 4,
        "remaining_terminal_totality_proofs": [
            "SAME_CHART_RELATIVE_CELLS",
            "SIGNED_BOUNDARY_FACES",
            "COMPLETE_BOUNDARY_FACES",
            "POSITIVE_VOLUME_CARRIERS",
        ],
        "legal_cross_component_witness_found": True,
        "legal_same_chart_witness_group_count": 228,
        "unique_witness_component_edge_count": 192,
        "prior_C27_C28_C29_authority": "INVALIDATED__REBUILD_REQUIRED",
        "C29_patch_or_preservation_permitted": False,
        "provisional_overlay_is_maximality_authority": False,
        "rebuild_required": True,
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    print(canonical({**result, "result_sha256": digest(result)}).decode("ascii"))
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
