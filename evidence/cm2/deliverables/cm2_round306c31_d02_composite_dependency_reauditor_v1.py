#!/usr/bin/env python3
"""Fail-closed re-audit of the composite D02 dependency after C29 and C30q10."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent

STATIC_PINS = {
    "round144": (
        "deliverables/cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json",
        "bd2f4f0262b58e2847ab578fb2bad3c7ca01305bbd113f6c330697714276675f",
    ),
    "round144_verification": (
        "deliverables/cm2-round144-round137-v1-superseding-migration-schema-verification-2026-07-24.json",
        "dabd57057c1a6fe7f9afa47f7445a4696297aa7488dc89ad808d5b8307bff9b5",
    ),
    "round150": (
        "deliverables/cm2-round150-connected-2d-corridor-atlas-2026-07-24.json",
        "6bb182760205190ad635ef34c21eca6221d2224e2dcdb585f70c157fad76321c",
    ),
    "round150_verification": (
        "deliverables/cm2-round150-connected-2d-corridor-atlas-verification-2026-07-24.json",
        "686e236dbe998c111a0307e3edfd34d0b26185b6f52ec54fa33e340725655ee5",
    ),
    "round151": (
        "deliverables/cm2-round151-dual-boundary-event-census-2026-07-24.json",
        "593188b5e9996cfa8151cd15c318a7a6136c108dba123cc91e421c83f7aea821",
    ),
    "round151_verification": (
        "deliverables/cm2-round151-dual-boundary-event-census-verification-2026-07-24.json",
        "61e053ca782cd030bb6d3a182e7ff4f032e4d6bb2fadf1fa82682789908ae1cd",
    ),
    "round161": (
        "deliverables/cm2-round161-dyadic-sheared-recentering-to-2500000000000000h-2026-07-25.json",
        "317ee6a43cd6db687f9ac4b089940c436817b4bfec7449ab778b462cff35e0cd",
    ),
    "round161_verification": (
        "deliverables/cm2-round161-dyadic-sheared-recentering-to-2500000000000000h-verification-2026-07-25.json",
        "01da56a79ec34736946c047784de75aa773e61822ffd45fa8a3fe5cc339832db",
    ),
    "round162": (
        "deliverables/cm2_round162_exterior_unique_owner_pruning_certificate.json",
        "9cf6e0a65659a6c835e476d283b48d3fcd3b29f450ca2bf1b71d66dfb695f97f",
    ),
    "round162_verification": (
        "deliverables/cm2_round162_exterior_unique_owner_pruning_verification.json",
        "c7dda884faa817e5dbafc94756f01023eafe00def62de1676fa830d605e45b79",
    ),
    "round165": (
        "deliverables/cm2_round165_adaptive_typed_seam_census_certificate.json",
        "2cbd69e8cbde66966d78764c0d5b34518c2ec55891d0238a62f40073ae4876a8",
    ),
    "round165_verification": (
        "deliverables/cm2_round165_adaptive_typed_seam_census_verification.json",
        "af684b956c40c97e26fdd5f9ddacea85b9c693b0b9a935d387ed1a5142ffa3b5",
    ),
}

C29_FILES = {
    "PASS.lock",
    "chain_status.json",
    "payload_manifest.sha256",
    "root_manifest.sha256",
    "terminal_receipt.json",
    "terminal_replay.json",
}
Q10_CHAIN_FILES = {
    "PASS.lock",
    "chain_status.json",
    "evidence_bundle_receipt.json",
    "manifest_receipt.json",
    "outer_verification.json",
    "payload",
    "payload_manifest.sha256",
    "root_manifest.sha256",
    "terminal_replay.json",
    "terminal_seal_receipt.json",
}
Q10_LEDGER_FILES = {
    "PASS.lock",
    "application_receipt.json",
    "hostile_audit.json",
    "root_manifest.sha256",
    "source_w_formal_ledger.json",
}

C29_MARKER = (
    "PASS_C29_V2_SOURCE_G_FIBRE_AUTHORITY_TERMINAL_BYTE_REPLAY__"
    "SOURCE_W_UNCHANGED_CM2_NO_GO\n"
).encode("ascii")
Q10_CHAIN_MARKER = (
    "PASS_C30Q10_C30F_Q9_JOINT_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_W_ZERO\n"
).encode("ascii")
Q10_LEDGER_MARKER = b"PASS_C30Q10_FORMAL_SOURCE_W_LEDGER__REMAINDER_0\n"

STATUS = (
    "PASS_D02_COMPOSITE_REAUDIT__SOURCE_G_TERMINAL_AND_SOURCE_W_ZERO__"
    "D02_FAIL_CLOSED_ON_MISSING_TWO_GENERATOR_OUTER_ATLAS"
)


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result["object_sha256"] = digest(result)
    return result


def duplicate_safe(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise Reject("non-finite JSON number:" + value)


def workspace(path: Path) -> Path:
    absolute = path if path.is_absolute() else ROOT / path
    resolved = absolute.resolve(strict=True)
    need(resolved == ROOT or ROOT in resolved.parents, "path outside workspace")
    return resolved


def raw_file(path: Path, label: str, maximum: int = 512 << 20) -> bytes:
    absolute = workspace(path)
    before = absolute.lstat()
    need(stat.S_ISREG(before.st_mode), label + ":regular")
    need(before.st_nlink == 1, label + ":single-link")
    need(0 <= before.st_size <= maximum, label + ":size")
    raw = absolute.read_bytes()
    after = absolute.lstat()
    need(
        (before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
         before.st_size, before.st_mtime_ns, before.st_ctime_ns)
        ==
        (after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
         after.st_size, after.st_mtime_ns, after.st_ctime_ns),
        label + ":TOCTOU",
    )
    return raw


def file_sha(path: Path, label: str) -> str:
    return hashlib.sha256(raw_file(path, label)).hexdigest()


def strict_json(path: Path, label: str) -> dict[str, Any]:
    raw = raw_file(path, label)
    try:
        value = json.loads(
            raw, object_pairs_hook=duplicate_safe, parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ":JSON") from exc
    need(type(value) is dict, label + ":object")
    return value


def exact_names(path: Path, expected: set[str], label: str) -> None:
    directory = workspace(path)
    need(directory.is_dir() and not directory.is_symlink(), label + ":directory")
    need({entry.name for entry in os.scandir(directory)} == expected, label + ":members")


def load_static() -> tuple[dict[str, Any], dict[str, str]]:
    documents: dict[str, Any] = {}
    hashes: dict[str, str] = {}
    for label, (name, expected) in STATIC_PINS.items():
        path = Path(name)
        actual = file_sha(path, label)
        need(actual == expected, label + ":SHA256")
        documents[label] = strict_json(path, label)
        hashes[name] = actual
    return documents, hashes


def process_attestation() -> dict[str, Any]:
    token = os.environ.get("CM2_AUDIT_TOKEN", "")
    unit = os.environ.get("CM2_AUDIT_UNIT", "")
    invocation = os.environ.get("INVOCATION_ID", "")
    need(re.fullmatch(r"c31-d02-reaudit-[a-z0-9-]{16,160}", token) is not None,
         "fresh audit token")
    need(re.fullmatch(r"cm2-c31-d02-reaudit-[a-z0-9-]{16,160}\.service", unit) is not None,
         "audit unit")
    need(re.fullmatch(r"[0-9a-f]{32}", invocation) is not None, "InvocationID")
    need(
        os.environ.get("HOME") == "/nonexistent"
        and os.environ.get("LC_ALL") == "C.UTF-8"
        and os.environ.get("TZ") == "UTC"
        and os.environ.get("PYTHONHASHSEED") == "0",
        "controlled environment",
    )
    return {
        "publication_token": token,
        "unit": unit,
        "InvocationID": invocation,
        "ExecMainPID": os.getpid(),
        "uid": os.getuid(),
    }


def load_snapshot(c29_path: Path, q10_chain_path: Path, q10_ledger_path: Path) -> dict[str, Any]:
    static, static_hashes = load_static()
    exact_names(c29_path, C29_FILES, "C29 terminal")
    exact_names(q10_chain_path, Q10_CHAIN_FILES, "Q10 chain")
    exact_names(q10_ledger_path, Q10_LEDGER_FILES, "Q10 ledger")
    snapshot = {
        "static": static,
        "static_hashes": static_hashes,
        "c29": {
            "marker": raw_file(c29_path / "PASS.lock", "C29 marker"),
            "root_sha256": file_sha(c29_path / "root_manifest.sha256", "C29 root"),
            "receipt_file_sha256": file_sha(c29_path / "terminal_receipt.json", "C29 receipt"),
            "replay_file_sha256": file_sha(c29_path / "terminal_replay.json", "C29 replay"),
            "receipt": strict_json(c29_path / "terminal_receipt.json", "C29 receipt"),
            "replay": strict_json(c29_path / "terminal_replay.json", "C29 replay"),
        },
        "q10": {
            "chain_marker": raw_file(q10_chain_path / "PASS.lock", "Q10 chain marker"),
            "chain_root_sha256": file_sha(q10_chain_path / "root_manifest.sha256", "Q10 chain root"),
            "terminal_replay_file_sha256": file_sha(q10_chain_path / "terminal_replay.json", "Q10 replay"),
            "terminal_replay": strict_json(q10_chain_path / "terminal_replay.json", "Q10 replay"),
            "ledger_marker": raw_file(q10_ledger_path / "PASS.lock", "Q10 ledger marker"),
            "ledger_root_sha256": file_sha(q10_ledger_path / "root_manifest.sha256", "Q10 ledger root"),
            "ledger_file_sha256": file_sha(q10_ledger_path / "source_w_formal_ledger.json", "Q10 ledger"),
            "ledger": strict_json(q10_ledger_path / "source_w_formal_ledger.json", "Q10 ledger"),
            "application": strict_json(q10_ledger_path / "application_receipt.json", "Q10 application"),
            "hostile": strict_json(q10_ledger_path / "hostile_audit.json", "Q10 hostile"),
        },
        "claimed_complete_outer_atlas": False,
        "claimed_D03_authorized": False,
    }
    return snapshot


def validate_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    static = snapshot["static"]
    r144 = static["round144"]
    r144v = static["round144_verification"]
    blocker = r144["result"]["first_exact_blocker"]
    need(r144.get("schema") == "cm2.round144.round137-v1-superseding-migration-schema.v1",
         "Round144 schema")
    need(blocker == {
        "corrected_component_id": None,
        "next_after_D02": "D03 least-rank negative oracle",
        "node_id": "D02",
        "object": "a complete validated two-generator centered-jet outer atlas with exhausted event frontier",
        "row_sha256": "a25e021d4386ae25437efdd2c658533bb579e195894036b0ab6e26ae0f0b4132",
        "why_first": "the known adaptive cell and contained basis row give only a positive upper bound; without a maximal-component outer atlas no complete earlier-rank exclusion query is valid",
    }, "Round144 D02 contract")
    need(r144v["result"].get("status") == "PASS"
         and r144v["result"]["independent_reconstruction"].get("first_exact_blocker") == "D02",
         "Round144 verification")

    r150 = static["round150"]
    r150v = static["round150_verification"]
    need(r150["result"].get("status")
         == "CERTIFIED_CONNECTED_PHYSICAL_2D_CORRIDOR_AND_UNIQUE_TERMINAL_C24_GRAPH__D02_STILL_BLOCKED",
         "Round150 boundary")
    need(r150v["result"].get("status") == "PASS"
         and r150v["result"].get("D02_status") == "BLOCKED", "Round150 verification")

    r151 = static["round151"]
    r151v = static["round151_verification"]
    need(r151["result"].get("status")
         == "CERTIFIED_GLOBAL_DUAL_EVENT_GRAPH_CENSUS_ON_CONNECTED_X_CORRIDOR__D02_STILL_BLOCKED",
         "Round151 boundary")
    need(r151v["result"].get("status") == "PASS"
         and r151v["result"].get("D02_status") == "BLOCKED", "Round151 verification")

    r161 = static["round161"]
    r161v = static["round161_verification"]
    atlas = r161["result"]["combined_typed_atlas"]
    need(atlas == {
        "connected": True,
        "interior_untyped_event_cell_count": 0,
        "lower_symmetry_axis_terminal": True,
        "slab_count": 75,
        "typed_box_count": 225,
        "upper_endpoint_in_h_units": "2500000000000000",
        "upper_endpoint_terminal": False,
    }, "Round161 bounded atlas")
    need(r161v["result"].get("status") == "PASS"
         and r161v["result"].get("D02_status") == "BLOCKED"
         and r161v["result"].get("compact_angular_fundamental_domain_exhausted") is False
         and r161v["result"].get("disconnected_exterior_sheets_exhausted") is False,
         "Round161 non-exhaustion")

    r162 = static["round162"]
    r162v = static["round162_verification"]
    scope = r162["result"]["scope"]
    census = r162["result"]["combined_frozen_prefix_census"]
    need(scope.get("not_D02_closure") is True
         and scope.get("not_full_exterior_sheet_exhaustion") is True
         and scope.get("not_all_return_signatures") is True,
         "Round162 scope")
    need(census.get("source_W_leaf_count") == 76_828
         and census.get("remaining_leaf_count") == 39_388
         and census.get("frozen_prefix_unresolved_leaves_zero") is False,
         "Round162 census")
    need(r162v["result"].get("status") == "PASS"
         and r162v["result"].get("strict_nonpromotion_recomputed") is True,
         "Round162 verification")

    r165 = static["round165"]
    r165v = static["round165_verification"]
    refined = r165["result"]["refined_recordwise_census"]
    need(refined.get("round163_total_source_W_records") == 76_828
         and refined.get("round163_seam_parent_records_replaced") == 618
         and refined.get("refined_total_records") == 76_832
         and refined.get("refined_excluded_records") + refined.get("refined_live_records") == 76_832,
         "Round165 76828-to-76832 refinement")
    need(r165["result"]["strict_nonpromotion"].get("D02") == "BLOCKED"
         and r165v["result"].get("status") == "PASS"
         and r165v["result"].get("strict_nonpromotion_recomputed") is True,
         "Round165 nonpromotion")

    c29 = snapshot["c29"]
    need(c29["marker"] == C29_MARKER, "C29 marker")
    need(c29["root_sha256"] == "382b0615f92762cd68ac6a54daf0007ee2b4b27d826eaec0d55297151c5b111d",
         "C29 root")
    need(c29["receipt_file_sha256"] == "4f395cd6160ce3e3b629330af9b0f14631a8e7976db4faa00b18c045cfce4ae9",
         "C29 receipt SHA")
    need(c29["replay_file_sha256"] == "2c94b556227f30b1514e83b505db60588d648c487d97ed45af6b1feb23a95b4d",
         "C29 replay SHA")
    c29_receipt = c29["receipt"]
    c29_replay = c29["replay"]
    need(c29_receipt.get("status")
         == "PASS_C29_V2_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_G_FIBRE_AUTHORITY_MINTED"
         and c29_receipt.get("authority_minted") is True
         and c29_receipt.get("D02") == "BLOCKED_COMPOSITE"
         and c29_receipt["exact_census"] == {
             "component_key_incidences": 60_296,
             "component_key_multiplicity_census": {"1": 27_108, "2": 16_556, "3": 8, "4": 8, "5": 4},
             "cross_post_component_member_pairs": 125_561_998_198,
             "family_member_census": {"G2A": 5_264, "G2B": 10_128, "NON_GRAPH": 55_604, "PRESERVED": 126_468, "R2": 295_336, "R292": 9_404},
             "members": 502_204,
             "official_keys": 124,
             "post_C27R2_components": 43_684,
             "representations": 549_616,
             "total_unordered_member_pairs": 126_104_177_706,
             "within_post_component_member_pairs": 542_179_508,
         }, "C29 terminal authority")
    need(c29_replay.get("authority_minted") is True
         and c29_replay.get("terminal_receipt_object_sha256")
         == c29_receipt.get("terminal_receipt_sha256"), "C29 terminal replay")

    q10 = snapshot["q10"]
    need(q10["chain_marker"] == Q10_CHAIN_MARKER, "Q10 chain marker")
    need(q10["chain_root_sha256"] == "2d1e380cf7d3fe36b047f729cebde36cacc9c60ae5cc7c1069e8ebef973758a1",
         "Q10 chain root")
    need(q10["terminal_replay_file_sha256"] == "f51c25e1cfcfcc2b97bcf57e2234f3ca5470b1d0567fcb798e9b2cd439f91be3",
         "Q10 replay SHA")
    need(q10["ledger_marker"] == Q10_LEDGER_MARKER, "Q10 ledger marker")
    need(q10["ledger_root_sha256"] == "8a41816ca2d0838471b38983a08d7ec52416caf68a326e76497aaf0f1979e968",
         "Q10 ledger root")
    need(q10["ledger_file_sha256"] == "a18922715a7bf05e591c36afaed2c1ab14f682f79a32af2632a70ffd533d90c4",
         "Q10 ledger SHA")
    q10_replay = q10["terminal_replay"]
    ledger = q10["ledger"]
    application = q10["application"]
    hostile = q10["hostile"]
    need(q10_replay.get("status")
         == "PASS_FORMAL_C30Q10_JOINT_TERMINAL__SOURCE_W_54_TO_0_AUTHORIZED"
         and q10_replay.get("source_W_formal_remainder") == 0
         and q10_replay.get("D02") == "BLOCKED_COMPOSITE", "Q10 terminal")
    need(ledger.get("status") == "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_0"
         and ledger.get("formal_coverage_numerator") == 76_832
         and ledger.get("formal_coverage_denominator") == 76_832
         and ledger["current_state"] == {
             "conservative_live": 2_020,
             "excluded": 74_812,
             "remaining": 0,
             "remaining_partition": {"compact_q": 0},
             "resolved_nonexcluded": 2_020,
             "total": 76_832,
         }
         and ledger["strict_nonpromotion"].get("D02") == "BLOCKED_COMPOSITE",
         "Q10 formal ledger")
    need(application.get("source_W_transition_authorized") is True
         and application.get("source_W_formal_remainder") == 0
         and application.get("ExecMainPID") == 1_952_739
         and application.get("InvocationID") == "97937b6825fe44f08f25676e7b876ca7",
         "Q10 process-bound application")
    need(hostile.get("negative_test_count") == 9
         and hostile.get("rejected_attacks")
         == ["conservation", "duplicate", "out_of_order", "schema", "PID", "stale", "marker", "manifest", "object"],
         "Q10 hostile audit")

    need(snapshot.get("claimed_complete_outer_atlas") is False, "unbacked D02 atlas promotion")
    need(snapshot.get("claimed_D03_authorized") is False, "premature D03 authorization")

    return {
        "d02_contract": blocker["object"],
        "source_G_terminal": {
            "status": "AUTHORIZED_TERMINAL_SOURCE_G_POST_C27R2_FIBRE_AUTHORITY",
            "post_C27R2_components": 43_684,
            "members": 502_204,
            "official_keys": 124,
            "fibre_or_disposition_gap_count": 0,
        },
        "source_W_terminal": {
            "status": "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_0",
            "total": 76_832,
            "excluded": 74_812,
            "resolved_nonexcluded": 2_020,
            "remaining": 0,
        },
        "record_refinement_bridge": {
            "Round162_source_W_leaf_count": 76_828,
            "Round165_seam_parents_replaced": 618,
            "Round165_terminal_records_inserted": 622,
            "Round165_refined_total": 76_832,
            "net_record_delta": 4,
        },
        "latest_validated_geometry": {
            "connected_typed_slabs": 75,
            "typed_boxes": 225,
            "interior_untyped_event_cells": 0,
            "upper_endpoint_terminal": False,
            "compact_angular_fundamental_domain_exhausted": False,
            "disconnected_exterior_sheets_exhausted": False,
        },
        "missing_D02_obligations": {
            "complete_versioned_two_generator_outer_atlas": True,
            "maximal_component_beta_extent_exhaustion": True,
            "every_component_exit_typed": True,
            "all_competing_event_families_exhausted": True,
            "all_chart_grazing_corner_strata_glued_or_typed": True,
            "disconnected_exterior_sheet_exhaustion": True,
            "terminal_four_class_census_with_zero_unresolved": True,
        },
    }


def hostile_audit(snapshot: dict[str, Any]) -> list[str]:
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("round144_schema", lambda x: x["static"]["round144"].__setitem__("schema", "forged")),
        ("round144_D02_contract", lambda x: x["static"]["round144"]["result"]["first_exact_blocker"].__setitem__("object", "source-W zero")),
        ("round144_verification", lambda x: x["static"]["round144_verification"]["result"].__setitem__("status", "FAIL")),
        ("round161_terminal", lambda x: x["static"]["round161"]["result"]["combined_typed_atlas"].__setitem__("upper_endpoint_terminal", True)),
        ("round161_exterior", lambda x: x["static"]["round161_verification"]["result"].__setitem__("disconnected_exterior_sheets_exhausted", True)),
        ("round162_scope", lambda x: x["static"]["round162"]["result"]["scope"].__setitem__("not_D02_closure", False)),
        ("round165_record_conservation", lambda x: x["static"]["round165"]["result"]["refined_recordwise_census"].__setitem__("refined_total_records", 76_831)),
        ("C29_authority", lambda x: x["c29"]["receipt"].__setitem__("authority_minted", False)),
        ("C29_marker", lambda x: x["c29"].__setitem__("marker", b"PASS\n")),
        ("source_W_remainder", lambda x: x["q10"]["ledger"]["current_state"].__setitem__("remaining", 1)),
        ("unbacked_D02_promotion", lambda x: x.__setitem__("claimed_complete_outer_atlas", True)),
        ("premature_D03_authorization", lambda x: x.__setitem__("claimed_D03_authorized", True)),
    ]
    rejected: list[str] = []
    for name, mutate in attacks:
        candidate = copy.deepcopy(snapshot)
        mutate(candidate)
        try:
            validate_snapshot(candidate)
        except Reject:
            rejected.append(name)
        else:
            raise Reject("hostile attack accepted:" + name)
    return rejected


def write_atomic(path: Path, raw: bytes) -> None:
    absolute = path if path.is_absolute() else ROOT / path
    parent = absolute.parent.resolve(strict=True)
    need(parent == ROOT or ROOT in parent.parents, "output outside workspace")
    need(not absolute.exists(), "output exists")
    temporary = parent / ("." + absolute.name + ".tmp-" + str(os.getpid()))
    need(not temporary.exists(), "temporary output exists")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, absolute)
        directory_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def publish(output: Path, snapshot: dict[str, Any], evidence: dict[str, Any], process: dict[str, Any]) -> dict[str, Any]:
    output_absolute = output if output.is_absolute() else ROOT / output
    need(not output_absolute.exists(), "output directory exists")
    output_absolute.parent.mkdir(parents=True, exist_ok=True)
    output_absolute.mkdir(mode=0o700)
    rejected = hostile_audit(snapshot)
    attack_receipt = seal({
        "schema": "cm2.round306c31.d02-composite-dependency-hostile-audit.v1",
        "status": "PASS_D02_COMPOSITE_REAUDIT_ALL_12_HOSTILE_PROMOTIONS_REJECTED",
        "negative_test_count": len(rejected),
        "rejected_attacks": rejected,
        "formal_promotion_authorized_by_attacks": False,
    })
    receipt = seal({
        "schema": "cm2.round306c31.d02-composite-dependency-reaudit.v1",
        "status": STATUS,
        "process_attestation": process,
        "input_sha256": snapshot["static_hashes"] | {
            "C29_terminal_receipt.json": snapshot["c29"]["receipt_file_sha256"],
            "C29_terminal_replay.json": snapshot["c29"]["replay_file_sha256"],
            "C29_terminal_root_manifest.sha256": snapshot["c29"]["root_sha256"],
            "C30q10_terminal_replay.json": snapshot["q10"]["terminal_replay_file_sha256"],
            "C30q10_terminal_root_manifest.sha256": snapshot["q10"]["chain_root_sha256"],
            "source_w_formal_ledger.json": snapshot["q10"]["ledger_file_sha256"],
            "source_w_formal_ledger_root_manifest.sha256": snapshot["q10"]["ledger_root_sha256"],
        },
        "evidence": evidence,
        "dependency_state": {
            "D02": "BLOCKED_BY_MISSING_COMPLETE_TWO_GENERATOR_OUTER_ATLAS_AND_EXTERIOR_SHEET_EXHAUSTION",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "complete_global_18_field_blocks": 0,
            "five_gate_clean_room_promotion": "NOT_PERFORMED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "hostile_audit_object_sha256": attack_receipt["object_sha256"],
        "required_next": (
            "build one formally pinned Round144-compatible two-generator centered-jet outer-atlas "
            "certificate over the compact four-chart fundamental domain; materialize cell, adjacency, "
            "event-face, exit, seam, grazing, corner, and disconnected-sheet ledgers; require the "
            "four-class terminal census unresolved count to be zero before D03"
        ),
    })
    write_atomic(output_absolute / "hostile_audit.json", canonical(attack_receipt) + b"\n")
    write_atomic(output_absolute / "d02_composite_reaudit.json", canonical(receipt) + b"\n")
    manifest_rows = []
    for name in ("d02_composite_reaudit.json", "hostile_audit.json"):
        manifest_rows.append(file_sha(output_absolute / name, "output:" + name) + "  " + name)
    write_atomic(output_absolute / "root_manifest.sha256", ("\n".join(manifest_rows) + "\n").encode("ascii"))
    write_atomic(output_absolute / "PASS.lock", (STATUS + "\n").encode("ascii"))
    return receipt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--c29-terminal", type=Path, required=True)
    parser.add_argument("--q10-chain", type=Path, required=True)
    parser.add_argument("--q10-ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    try:
        snapshot = load_snapshot(arguments.c29_terminal, arguments.q10_chain, arguments.q10_ledger)
        evidence = validate_snapshot(snapshot)
        receipt = publish(arguments.output, snapshot, evidence, process_attestation())
    except (OSError, Reject, KeyError, TypeError, ValueError) as exc:
        print("REJECT:" + str(exc), file=sys.stderr)
        return 1
    print(canonical(receipt).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
