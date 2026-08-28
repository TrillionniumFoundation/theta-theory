#!/usr/bin/env python3
"""Read-only, zero-credit preflight for the CM2 D02 tail dependency chain.

This program is deliberately a *reader*, not a producer.  It opens the pinned
artifacts with ``O_NOFOLLOW`` where available, checks inode stability while a
file is being read, and emits one canonical JSON report on stdout.  It never
creates a candidate, checkpoint, pointer, receipt, seal, manifest, or runtime
surface.  Run it as ``python3 -I -B scripts/cm2_tail_dependency_preflight_v1.py``.

The report can say that the dependency chain is blocked; that is the expected
answer while D02 is incomplete.  A successful process exit means that the
preflight itself ran and its inputs were read consistently, not that CM2 is
authorized or that any theorem credit exists.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any, Callable

# Keep this assignment even when a caller forgot -B.  The report separately
# records whether the interpreter actually received the -B flag.
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]

C53_PREDECESSOR = (
    "10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41"
)
C53_HEAD_REL = (
    ".cm2-runtime/cm2-global-authority-heads/"
    f"predecessor-{C53_PREDECESSOR}.seal"
)
C53_CLAIM_REL = (
    ".cm2-runtime/cm2-global-successor-claims/"
    f"predecessor-{C53_PREDECESSOR}.claim"
)
C53_DIR_REL = (
    ".cm2-runtime/c53-pair-successor-audits/"
    "c53-independent-audit-a7bee7e57b65-v1"
)
C53_CHECKPOINT_REL = f"{C53_DIR_REL}/post_seal_effective_checkpoint.json"
C53_INSTALLER_REL = (
    f"{C53_DIR_REL}/installer__"
    "cm2_round306c53_d02a_pair1_pair_level_successor_installer_v1.py"
)
C53_VERIFIER_REL = (
    f"{C53_DIR_REL}/independent_verifier__"
    "cm2_round306c53_d02a_pair1_pair_level_successor_independent_verifier_v1.py"
)

EXPECTED_C53_FILE_SHA = {
    C53_HEAD_REL: "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    C53_CLAIM_REL: "3801e452f218e330bc16faed5986146202a7d7026e46924bf7bc00167b05f77b",
    C53_INSTALLER_REL: "ffe77bf55c1f782b3bb4cb5098c57bb12468b357b7cbfc66f85f3f44ef9062a6",
    C53_VERIFIER_REL: "ac6ae0eed9841df386785194bdbb3927736207cef0641dc2f462c9892932b136",
}

EXPECTED_C53_HEAD_OBJECT = (
    "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"
)
EXPECTED_C53_CLAIM_OBJECT = (
    "437138569d476d31ceda62496dc6d020dd570f2786288beecd8165a6baaea512"
)
EXPECTED_C53_CHECKPOINT_OBJECT = (
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
)

C46A_PLAN_REL = "deliverables/cm2_round306c46_d02a_general_adaptive_lower_strata_plan_v1.md"
C46A_SOURCE_REL = "deliverables/cm2_round306c46_d02a_general_adaptive_lower_strata_closure_engine_v1.py"
C46B_PLAN_REL = "deliverables/cm2_round306c46_d02b_resumable_occurrence_collision_continuation_plan_v1.md"
C46B_SOURCE_REL = "deliverables/cm2_round306c46_d02b_resumable_occurrence_collision_continuation_engine_v1.py"
EXPECTED_C46_SHA = {
    C46A_PLAN_REL: "28db3a4abc2daf790c65f9848e515446719696a9355592ad44089fdd3c9fd176",
    C46A_SOURCE_REL: "365432e96f2c287ef3c5497b7d15e01a80775f52d8cf5b71810d6f4c0e4442ea",
    C46B_PLAN_REL: "e7a30d6e8539d004730d438369312290cff81f293525d4f0b2f756e436c5b985",
    C46B_SOURCE_REL: "95a9e30101368b4bc91142a75ec7821b0d035f3dab52a556377c761c1bdac7b7",
}

D03_CONTRACT_REL = "deliverables/cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json"
D03_VERIFY_REL = "deliverables/cm2-round137-seed-independent-dyadic-basis-rank-contract-verification-2026-07-24.json"
D04_SCHEMA_REL = "deliverables/cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json"
D04_VERIFY_REL = "deliverables/cm2-round144-round137-v1-superseding-migration-schema-verification-2026-07-24.json"
GATE5_CERT_REL = "deliverables/cm2-round147-gate5-strict-reaudit-upgrade-frontier-2026-07-24.json"
GATE5_VERIFY_REL = "deliverables/cm2-round147-gate5-strict-reaudit-upgrade-frontier-verification-2026-07-24.json"
GATE5_TRANSFER_REL = "deliverables/cm2_gate5_transfer_manifest.json"
V16_AUDIT_REL = "deliverables/cm2_round306c79g_true_global_no_producer_consumer_static_audit_v16.json"
V16_REJECTION_REL = "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16_semantic_rejection_supersession_receipt_v1.json"

EXPECTED_FILE_SHA = {
    D03_CONTRACT_REL: "06918b7bbfdeed9bda41a1220a25b630df6eaaa5f06024757f25a8c9fe7b88bf",
    D03_VERIFY_REL: "53369532c293d9cb2830a362facef7e4c4040f826f5ddea70519fde9034a1a5c",
    D04_SCHEMA_REL: "bd2f4f0262b58e2847ab578fb2bad3c7ca01305bbd113f6c330697714276675f",
    D04_VERIFY_REL: "dabd57057c1a6fe7f9afa47f7445a4696297aa7488dc89ad808d5b8307bff9b5",
    GATE5_CERT_REL: "db7f1a01f36c56dc537a4873dcd232808c337298a0998608a2c34aeaaa7531ee",
    GATE5_VERIFY_REL: "8302642619f66a4a47ec79d8fefb0230378331b578a363f12ad1b64dffebbd3d",
    GATE5_TRANSFER_REL: "66dec1ec81fd7c15b53d939cf42ed065c860d662a4d14b3607befdd86ed84c13",
    V16_AUDIT_REL: "e2753ec302eecef28f714541e986b6d7a34c0484a428b996ad77c1bfa1a8ddd6",
    V16_REJECTION_REL: "4b05c7dcd7303311fed7b51ea878641e006e707b5fe413f2aefbc3146afddb3c",
}

EXPECTED_GATES = [5, 6, 10, 11, 14, 15, 17, 18]


class ReadFailure(RuntimeError):
    """A fail-closed input/read error."""


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def parse_json(raw: bytes, rel: str) -> Any:
    try:
        return json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_pairs,
            parse_constant=_reject_constant,
        )
    except Exception as exc:  # pragma: no cover - message is part of report
        raise ReadFailure(f"invalid JSON {rel}: {exc}") from exc


def stable_read(root: Path, rel: str) -> tuple[bytes, dict[str, Any]]:
    """Read one regular, single-link, non-symlink file and check TOCTOU."""

    path = root / rel
    try:
        # O_NOFOLLOW is intentionally used when the platform exposes it.
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
    except OSError as exc:
        raise ReadFailure(f"open failed for {rel}: {exc}") from exc
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise ReadFailure(f"not regular single-link: {rel}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(fd)
        try:
            named = os.lstat(path)
        except OSError as exc:
            raise ReadFailure(f"named stat failed for {rel}: {exc}") from exc
        if (before.st_dev, before.st_ino, before.st_size) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
        ):
            raise ReadFailure(f"descriptor drift: {rel}")
        if (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino):
            raise ReadFailure(f"path inode drift: {rel}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise ReadFailure(f"size drift: {rel}")
        meta = {
            "path": rel,
            "sha256": sha256(raw),
            "mode_octal": format(stat.S_IMODE(before.st_mode), "04o"),
            "nlink": before.st_nlink,
            "bytes": len(raw),
        }
        return raw, meta
    finally:
        os.close(fd)


def file_probe(
    root: Path,
    rel: str,
    expected_sha: str | None = None,
    parse: bool = False,
) -> tuple[dict[str, Any], Any | None]:
    try:
        raw, meta = stable_read(root, rel)
        if expected_sha is not None:
            meta["expected_sha256"] = expected_sha
            meta["sha256_match"] = meta["sha256"] == expected_sha
        value = parse_json(raw, rel) if parse else None
        return meta, value
    except ReadFailure as exc:
        return {"path": rel, "readable": False, "error": str(exc)}, None


def result_row(
    passed: bool,
    *,
    observed: Any = None,
    expected: Any = None,
    blocker: str | None = None,
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {"passed": bool(passed)}
    if observed is not None:
        row["observed"] = observed
    if expected is not None:
        row["expected"] = expected
    if blocker is not None:
        row["blocker"] = blocker
    if evidence:
        row["evidence"] = evidence
    return row


def nested(root: Any, *keys: str, default: Any = None) -> Any:
    value = root
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value


def check_c53(root: Path) -> dict[str, Any]:
    files: dict[str, Any] = {}
    docs: dict[str, Any] = {}
    for rel in (C53_HEAD_REL, C53_CLAIM_REL, C53_CHECKPOINT_REL):
        expected = EXPECTED_C53_FILE_SHA.get(rel)
        meta, value = file_probe(root, rel, expected, parse=True)
        files[rel] = meta
        if value is not None:
            docs[rel] = value
    # Source pins are useful evidence that the exact C53 prefix is present.
    for rel in (C53_INSTALLER_REL, C53_VERIFIER_REL):
        meta, _ = file_probe(root, rel, EXPECTED_C53_FILE_SHA[rel], parse=False)
        files[rel] = meta

    head = docs.get(C53_HEAD_REL, {})
    claim = docs.get(C53_CLAIM_REL, {})
    checkpoint = docs.get(C53_CHECKPOINT_REL, {})
    scope = nested(head, "formal_scope", default={})
    after = nested(scope, "after", default={})
    four_after = nested(scope, "D02_four_class_after", default={})
    expected_four = {
        "CONNECTED_TO_KNOWN": 0,
        "EARLIEST_PREFIX_EXCLUDED": 75388,
        "SOURCE_GRAZING_OR_CEMETERY": 0,
        "TYPED_EVENT_GRAPH": 296,
        "UNRESOLVED_R1648_CONTINUATION": 1148,
        "total": 76832,
    }
    expected_after = {
        "logical_pending_task_count": 33638,
        "paired_coarse_cells": 576,
        "representative_parents_remaining": 574,
        "two_side_pending_occurrence_count": 67276,
        "unresolved_coarse_cells": 1148,
        "whole_representative_parent_count": 288,
    }
    checks = {
        "head_file_pin": result_row(
            files.get(C53_HEAD_REL, {}).get("sha256_match") is True,
            observed=files.get(C53_HEAD_REL, {}).get("sha256"),
            expected=EXPECTED_C53_FILE_SHA[C53_HEAD_REL],
        ),
        "claim_file_pin": result_row(
            files.get(C53_CLAIM_REL, {}).get("sha256_match") is True,
            observed=files.get(C53_CLAIM_REL, {}).get("sha256"),
            expected=EXPECTED_C53_FILE_SHA[C53_CLAIM_REL],
        ),
        "head_object_and_role": result_row(
            head.get("authority_seal_object_sha256") == EXPECTED_C53_HEAD_OBJECT
            and head.get("authority_role") == "GLOBAL_COMPOSITE"
            and head.get("status")
            == "COMMITTED_C53_PAIR1_ATOMIC_TWO_TASK_PAIR_LEVEL_SUCCESSOR__ONE_WHOLE_PARENT_CREDIT__ZERO_D02_GATE_CREDIT",
            observed={
                "authority_seal_object_sha256": head.get("authority_seal_object_sha256"),
                "authority_role": head.get("authority_role"),
                "status": head.get("status"),
            },
            expected={
                "authority_seal_object_sha256": EXPECTED_C53_HEAD_OBJECT,
                "authority_role": "GLOBAL_COMPOSITE",
                "D02_gate_credit": 0,
            },
        ),
        "claim_object_and_target": result_row(
            claim.get("claim_object_sha256") == EXPECTED_C53_CLAIM_OBJECT
            and claim.get("authority_seal_target_path") == C53_HEAD_REL
            and claim.get("zero_credit_before_seal") is True,
            observed={
                "claim_object_sha256": claim.get("claim_object_sha256"),
                "authority_seal_target_path": claim.get("authority_seal_target_path"),
                "zero_credit_before_seal": claim.get("zero_credit_before_seal"),
            },
            expected={
                "claim_object_sha256": EXPECTED_C53_CLAIM_OBJECT,
                "authority_seal_target_path": C53_HEAD_REL,
                "zero_credit_before_seal": True,
            },
        ),
        "effective_checkpoint_binding": result_row(
            head.get("successor_checkpoint_object_sha256") == EXPECTED_C53_CHECKPOINT_OBJECT
            and claim.get("post_seal_effective_checkpoint_object_sha256")
            == EXPECTED_C53_CHECKPOINT_OBJECT
            and checkpoint.get("effective_checkpoint_object_sha256")
            == EXPECTED_C53_CHECKPOINT_OBJECT,
            observed={
                "head": head.get("successor_checkpoint_object_sha256"),
                "claim": claim.get("post_seal_effective_checkpoint_object_sha256"),
                "checkpoint": checkpoint.get("effective_checkpoint_object_sha256"),
            },
            expected=EXPECTED_C53_CHECKPOINT_OBJECT,
        ),
        "c53_global_four_class_after": result_row(
            four_after == expected_four,
            observed=four_after,
            expected=expected_four,
            blocker="C53 leaves 1,148 R1648 continuations; this is not D02-C closure.",
        ),
        "c53_global_task_after": result_row(
            after == expected_after,
            observed=after,
            expected=expected_after,
            blocker="C53 is only a pair-level successor; the 33,638-task D02-A queue remains.",
        ),
        "c53_zero_credit_lock": result_row(
            scope.get("D02_gate_credit") == 0
            and scope.get("whole_parent_credit") == 1
            and checkpoint.get("D02_gate_credit") == 0
            and checkpoint.get("individual_task_whole_parent_credit_sum") == 0,
            observed={
                "global_D02_gate_credit": scope.get("D02_gate_credit"),
                "pair_whole_parent_credit": scope.get("whole_parent_credit"),
                "checkpoint_D02_gate_credit": checkpoint.get("D02_gate_credit"),
                "individual_task_whole_parent_credit_sum": checkpoint.get(
                    "individual_task_whole_parent_credit_sum"
                ),
            },
            expected={
                "D02_gate_credit": 0,
                "individual_task_whole_parent_credit_sum": 0,
                "note": "one pair aggregate credit is not D02 credit",
            },
            blocker="No positive D02/global credit may be inferred from the C53 pair aggregate.",
        ),
        "exact_c53_prefix_sources": result_row(
            all(files.get(rel, {}).get("sha256_match") is True
                for rel in (C53_INSTALLER_REL, C53_VERIFIER_REL)),
            evidence={rel: files.get(rel) for rel in (C53_INSTALLER_REL, C53_VERIFIER_REL)},
        ),
        "c53_prefix_immutable_shape": result_row(
            all(
                files.get(rel, {}).get("mode_octal") == "0444"
                and files.get(rel, {}).get("nlink") == 1
                for rel in (C53_HEAD_REL, C53_CLAIM_REL, C53_CHECKPOINT_REL,
                            C53_INSTALLER_REL, C53_VERIFIER_REL)
            ),
            expected={"mode_octal": "0444", "nlink": 1},
            evidence={rel: files.get(rel) for rel in (
                C53_HEAD_REL, C53_CLAIM_REL, C53_CHECKPOINT_REL,
                C53_INSTALLER_REL, C53_VERIFIER_REL
            )},
        ),
    }
    return {
        "status": "C53_HEAD_PRESENT_ZERO_D02_CREDIT",
        "predecessor_identity_sha256": C53_PREDECESSOR,
        "head_path": C53_HEAD_REL,
        "claim_path": C53_CLAIM_REL,
        "checkpoint_path": C53_CHECKPOINT_REL,
        "files": files,
        "checks": checks,
        "required_next": "consume C53 checkpoint and GLOBAL_COMPOSITE; never C42/C48 legacy bridge",
    }


def check_d02_queue(root: Path) -> dict[str, Any]:
    files: dict[str, Any] = {}
    texts: dict[str, str] = {}
    for rel in (C46A_PLAN_REL, C46A_SOURCE_REL, C46B_PLAN_REL, C46B_SOURCE_REL):
        meta, _ = file_probe(root, rel, EXPECTED_C46_SHA[rel], parse=False)
        files[rel] = meta
        try:
            raw, _ = stable_read(root, rel)
            texts[rel] = raw.decode("utf-8", "strict")
        except Exception:
            pass

    a = texts.get(C46A_PLAN_REL, "")
    b = texts.get(C46B_PLAN_REL, "")
    # These are deliberately textual assertions: C46 is a read-only plan, not
    # an authority ledger.  The mismatch with C53 is itself a useful blocker.
    a_markers = {
        "genesis_only": "GENESIS_TEMPLATE_ONLY" in a and "No `.cm2-runtime` object was written" in a,
        "legacy_task_templates": "33,642 task templates" in a,
        "legacy_pending_templates": "33,641 pending task templates" in a,
        "zero_credit": "zero-credit" in a.lower() and "formal credit" in a.lower(),
    }
    b_markers = {
        "representative_rows": "7,463 representative collision-3-ready rows" in b,
        "physical_sides": "14,926 distinct physical sides" in b,
        "zero_credit": "zero-credit" in b.lower() and "not close D02-B" in b,
        "manifest_present": "9dd2ec13da5509d7f4c8e947090feaee05ac31924e2855086c17a6dc05b7b5f4" in b,
    }
    return {
        "status": "C46_READ_ONLY_BASELINES_ONLY",
        "files": files,
        "d02_a": {
            "required_current_logical_pending_tasks": 33638,
            "observed_c46a_task_templates": 33642,
            "observed_c46a_pending_templates": 33641,
            "queue_matches_c53": False,
            "authority_ready": False,
            "checks": a_markers,
            "blocker": "C46-A is genesis-only and tied to the old C42 1,150-unresolved baseline; a new C53-bound successor engine is required.",
        },
        "d02_b": {
            "required_representative_rows": 7463,
            "required_physical_sides": 14926,
            "observed_c46b_representative_rows": 7463,
            "observed_c46b_physical_sides": 14926,
            "authority_ready": False,
            "checks": b_markers,
            "blocker": "C46-B is a collision-3 diagnostic interface; collision 4..1648 and global owner/cemetery proofs are absent.",
        },
        "d02_c": {
            "required_parent_kraft_equations": 862,
            "required_rows": 76832,
            "required_unresolved_zero": True,
            "current_unresolved": 1148,
            "authority_ready": False,
            "blocker": "An independent no-producer D02-C consumer must rebuild all rows and parents and pass cold/TOCTOU/outer/terminal replay.",
        },
    }


def check_d03(root: Path) -> dict[str, Any]:
    files: dict[str, Any] = {}
    docs: dict[str, Any] = {}
    for rel in (D03_CONTRACT_REL, D03_VERIFY_REL):
        meta, value = file_probe(root, rel, EXPECTED_FILE_SHA[rel], parse=True)
        files[rel] = meta
        if value is not None:
            docs[rel] = value
    contract = nested(docs.get(D03_CONTRACT_REL, {}), "result", default={})
    verification = nested(docs.get(D03_VERIFY_REL, {}), "result", default={})
    ledger = nested(contract, "count_ledger", default={})
    strict = nested(contract, "strict_nonpromotion", default={})
    historical = nested(contract, "historical_schema_audit", default={})
    independence = nested(verification, "independence_contract", default={})
    checks = {
        "contract_status": result_row(
            contract.get("status") == "CERTIFIED_PROSPECTIVE_SEED_INDEPENDENT_DYADIC_BASIS_RANK_CONTRACT",
            observed=contract.get("status"),
        ),
        "verification_pass": result_row(
            verification.get("status") == "PASS",
            observed=verification.get("status"),
        ),
        "seed_independent_small_replays": result_row(
            ledger.get("exhaustive_small_1d_row_count") == 105
            and ledger.get("exhaustive_small_2d_row_count") == 11025
            and historical.get("new_v1_is_prospective_compatible_with_countability_schema_only") is True,
            observed={
                "exhaustive_small_1d_row_count": ledger.get("exhaustive_small_1d_row_count"),
                "exhaustive_small_2d_row_count": ledger.get("exhaustive_small_2d_row_count"),
                "prospective_only": historical.get("new_v1_is_prospective_compatible_with_countability_schema_only"),
            },
            expected={"exhaustive_small_1d_row_count": 105, "exhaustive_small_2d_row_count": 11025, "prospective_only": True},
        ),
        "no_historical_or_gate_credit": result_row(
            strict.get("global_complete_18_field_block_count") == 0
            and strict.get("gate5_global_maturity") == "10/18"
            and strict.get("CM2") == "NO-GO_FOR_CLAIM"
            and strict.get("Round50_owner_key_count") == 0,
            observed={
                "global_complete_18_field_block_count": strict.get("global_complete_18_field_block_count"),
                "gate5_global_maturity": strict.get("gate5_global_maturity"),
                "CM2": strict.get("CM2"),
                "Round50_owner_key_count": strict.get("Round50_owner_key_count"),
            },
            blocker="Round137 is prospective rank infrastructure, not D03 authorization or historical ID recovery.",
        ),
        "producer_not_executed_or_imported": result_row(
            independence.get("Round137_producer_executed") is False
            and independence.get("Round137_producer_imported") is False,
            observed={
                "Round137_producer_executed": independence.get("Round137_producer_executed"),
                "Round137_producer_imported": independence.get("Round137_producer_imported"),
            },
        ),
    }
    return {
        "status": "D03_BLOCKED_UNAUTHORIZED",
        "files": files,
        "checks": checks,
        "authorized": False,
        "blocker": "D03 least-rank negative oracle waits for a complete validated D02 outer atlas and exhausted event frontier.",
    }


def check_d04(root: Path) -> dict[str, Any]:
    files: dict[str, Any] = {}
    docs: dict[str, Any] = {}
    for rel in (D04_SCHEMA_REL, D04_VERIFY_REL):
        meta, value = file_probe(root, rel, EXPECTED_FILE_SHA[rel], parse=True)
        files[rel] = meta
        if value is not None:
            docs[rel] = value
    schema_result = nested(docs.get(D04_SCHEMA_REL, {}), "result", default={})
    verify_result = nested(docs.get(D04_VERIFY_REL, {}), "result", default={})
    dag = nested(schema_result, "migration_DAG_rows", default=[])
    dag_by_id = {row.get("node_id"): row for row in dag if isinstance(row, dict)}
    ids = nested(schema_result, "current_identifier_values", default={})
    expected_deps = {"D02": ["D01"], "D03": ["D02"], "D04": ["D03"]}
    dep_check = all(dag_by_id.get(k, {}).get("depends_on") == v for k, v in expected_deps.items())
    checks = {
        "migration_schema_status": result_row(
            schema_result.get("status")
            == "CERTIFIED_VERSIONED_SUPERSEDING_MIGRATION_SCHEMA__NO_CORRECTED_COMPONENT_MINTED",
            observed=schema_result.get("status"),
        ),
        "migration_verification_pass": result_row(
            verify_result.get("status") == "PASS",
            observed=verify_result.get("status"),
        ),
        "d02_d03_d04_dependency_order": result_row(
            dep_check,
            observed={k: dag_by_id.get(k, {}).get("depends_on") for k in expected_deps},
            expected=expected_deps,
        ),
        "d02_d03_d04_blocked": result_row(
            all(dag_by_id.get(k, {}).get("status") == "BLOCKED" for k in ("D02", "D03", "D04")),
            observed={k: dag_by_id.get(k, {}).get("status") for k in ("D02", "D03", "D04")},
            expected={"D02": "BLOCKED", "D03": "BLOCKED", "D04": "BLOCKED"},
            blocker="No component_v1_id may be minted before D02 and D03 both pass.",
        ),
        "all_versioned_identifiers_null": result_row(
            bool(ids) and all(value is None for value in ids.values()),
            observed=ids,
            blocker="D04 is not minted; null identifiers are intentional fail-closed state.",
        ),
    }
    return {
        "status": "D04_NOT_MINTED",
        "files": files,
        "checks": checks,
        "minted": False,
        "blocker": "D04 requires D02 then D03 and one immutable global registry transaction.",
    }


def check_gate5(root: Path) -> dict[str, Any]:
    files: dict[str, Any] = {}
    docs: dict[str, Any] = {}
    for rel in (GATE5_CERT_REL, GATE5_VERIFY_REL, GATE5_TRANSFER_REL):
        meta, value = file_probe(root, rel, EXPECTED_FILE_SHA[rel], parse=True)
        files[rel] = meta
        if value is not None:
            docs[rel] = value
    cert = nested(docs.get(GATE5_CERT_REL, {}), "result", default={})
    verify = nested(docs.get(GATE5_VERIFY_REL, {}), "result", default={})
    ledger = nested(cert, "gate5_global_ledger", default={})
    blocked = ledger.get("strictly_blocked_field_indices")
    transfer = docs.get(GATE5_TRANSFER_REL, {})
    sf2 = transfer.get("sf2_return_block_dq", {})
    sf5 = transfer.get("sf5_phase_test_norm_lift", {})
    field_rows = nested(cert, "gate5_field_rows", default=[])
    blocked_names = {
        str(row.get("field_index")): row.get("field_name")
        for row in field_rows
        if isinstance(row, dict) and row.get("field_index") in EXPECTED_GATES
    }
    checks = {
        "certificate_status": result_row(
            cert.get("status") == "CERTIFIED_GATE5_18_FIELD_STRICT_REAUDIT__10_SATISFIED__8_PROSPECTIVE_LOCAL_ONLY_AND_STRICTLY_BLOCKED__0_UPGRADES",
            observed=cert.get("status"),
        ),
        "gate5_maturity": result_row(
            ledger.get("global_maturity_after") == "10/18"
            and ledger.get("global_complete_18_field_block_count_after") == 0,
            observed={
                "global_maturity_after": ledger.get("global_maturity_after"),
                "global_complete_18_field_block_count_after": ledger.get("global_complete_18_field_block_count_after"),
            },
            expected={"global_maturity_after": "10/18", "global_complete_18_field_block_count_after": 0},
            blocker="Eight global fields remain strictly blocked; no complete 18-field block exists.",
        ),
        "gate5_blocked_field_set": result_row(
            blocked == EXPECTED_GATES,
            observed=blocked,
            expected=EXPECTED_GATES,
        ),
        "gate5_verification_pass": result_row(
            verify.get("status") == "PASS"
            and verify.get("gate5_global_maturity") == "10/18"
            and verify.get("global_complete_18_field_block_count") == 0,
            observed={
                "status": verify.get("status"),
                "gate5_global_maturity": verify.get("gate5_global_maturity"),
                "global_complete_18_field_block_count": verify.get("global_complete_18_field_block_count"),
            },
        ),
        "transfer_manifest_global_gaps": result_row(
            sf2.get("certified") is False
            and sf2.get("complete_return_word_manifest") is False
            and sf2.get("exact_occurrence_source_matching") is False
            and sf5.get("both_cm2_norms_intertwined") is False,
            observed={
                "sf2_certified": sf2.get("certified"),
                "sf2_complete_return_word_manifest": sf2.get("complete_return_word_manifest"),
                "sf2_exact_occurrence_source_matching": sf2.get("exact_occurrence_source_matching"),
                "sf5_both_cm2_norms_intertwined": sf5.get("both_cm2_norms_intertwined"),
            },
            blocker="Gate-3 event/occurrence registry and physical norm lift are still incomplete.",
        ),
    }
    return {
        "status": "GATE5_BLOCKED_10_OF_18",
        "files": files,
        "checks": checks,
        "blocked_field_indices": blocked,
        "blocked_field_names": blocked_names,
        "complete_global_block_count": ledger.get("global_complete_18_field_block_count_after"),
        "blocker": "F5/F6/F10/F11/F14/F15/F17/F18 require global recordwise evidence and one immutable F1--F17 block.",
    }


def check_c79g_and_tail(root: Path) -> dict[str, Any]:
    files: dict[str, Any] = {}
    docs: dict[str, Any] = {}
    for rel in (V16_AUDIT_REL, V16_REJECTION_REL):
        meta, value = file_probe(root, rel, EXPECTED_FILE_SHA[rel], parse=True)
        files[rel] = meta
        if value is not None:
            docs[rel] = value
    audit = docs.get(V16_AUDIT_REL, {})
    rejection = docs.get(V16_REJECTION_REL, {})
    static = audit.get("static_census", {})
    checks = {
        "v16_static_no_credit": result_row(
            audit.get("formal_global_closure_credit") == 0
            and audit.get("D02_unlock") is False
            and audit.get("runtime_not_executed") is True,
            observed={
                "formal_global_closure_credit": audit.get("formal_global_closure_credit"),
                "D02_unlock": audit.get("D02_unlock"),
                "runtime_not_executed": audit.get("runtime_not_executed"),
            },
        ),
        "v16_public_unresolved_matches_c53": result_row(
            static.get("rows") == 76832
            and static.get("kraft_parents") == 862
            and static.get("public_unresolved") == 1148,
            observed=static,
            expected={"rows": 76832, "kraft_parents": 862, "public_unresolved": 1148},
            blocker="C79g has not established public unresolved=0.",
        ),
        "v16_semantic_rejection_frozen": result_row(
            rejection.get("status") == "FROZEN_APPEND_ONLY_V16_SEMANTIC_REJECTION__V16R2_SUCCESSOR_ONLY"
            and rejection.get("formal_global_closure_credit") == 0
            and rejection.get("D02_unlock") is False
            and rejection.get("successor_runtime_authorized") is False,
            observed={
                "status": rejection.get("status"),
                "formal_global_closure_credit": rejection.get("formal_global_closure_credit"),
                "D02_unlock": rejection.get("D02_unlock"),
                "successor_runtime_authorized": rejection.get("successor_runtime_authorized"),
            },
            blocker="v16 is rejected; v16r2 semantic regeneration is the only successor namespace.",
        ),
    }
    return {
        "status": "C79G_NOT_AUTHORIZED_V16_REJECTED",
        "files": files,
        "checks": checks,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "required_next": "v16r2 semantic regeneration, then independent C79g consumer with unresolved=0",
    }


def flatten_failures(value: Any, prefix: str = "") -> list[str]:
    failures: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            if key == "passed" and child is False:
                failures.append(prefix or "check")
            else:
                failures.extend(flatten_failures(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            failures.extend(flatten_failures(child, f"{prefix}[{index}]"))
    return failures


def collect_failed_checks(value: Any, prefix: str = "") -> list[str]:
    """Collect explicit failed assertions and file-pin mismatches."""

    failures: list[str] = []
    if isinstance(value, dict):
        if value.get("passed") is False:
            failures.append(prefix or "check")
        if value.get("sha256_match") is False:
            failures.append(f"{prefix}.sha256_match" if prefix else "sha256_match")
        for key, child in value.items():
            if key in {"passed", "sha256_match"}:
                continue
            path = f"{prefix}.{key}" if prefix else key
            failures.extend(collect_failed_checks(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            failures.extend(collect_failed_checks(child, f"{prefix}[{index}]"))
    return failures


def run(root: Path) -> tuple[dict[str, Any], int]:
    report: dict[str, Any] = {
        "schema": "cm2.tail-dependency-preflight.v1",
        "workspace_root": str(root),
        "invocation": {
            "python_version": sys.version.split()[0],
            "python_hashseed_independent": True,
            "sys_flag_B_seen": bool(sys.flags.dont_write_bytecode),
            "bytecode_disabled": bool(sys.dont_write_bytecode),
            "read_only": True,
            "runtime_write_attempted": False,
            "credit_attempted": False,
        },
    }
    sections: dict[str, Any] = {}
    section_errors: list[str] = []
    for name, fn in (
        ("c53_head", check_c53),
        ("d02_dependency", check_d02_queue),
        ("d03_seed_contract", check_d03),
        ("d04_migration_schema", check_d04),
        ("gate5", check_gate5),
        ("c79g_and_tail", check_c79g_and_tail),
    ):
        try:
            sections[name] = fn(root)
        except Exception as exc:  # fail closed, but keep JSON output complete
            sections[name] = {
                "status": "FAIL_CLOSED_SECTION_ERROR",
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
            section_errors.append(name)
    report["sections"] = sections

    failed_checks = collect_failed_checks(sections)

    # This is a dependency audit, not an authorization gate.  The process is
    # successful when the report was produced under -B and no section crashed;
    # `cm2_ready` remains false until the explicit downstream conditions pass.
    report["tail_order"] = [
        "v16r2 semantic regeneration",
        "cold exact8 -> manifest -> outer",
        "C79g unresolved_zero consumer and positive wrapper",
        "D02-A 33638 tasks",
        "D02-B 7463 representatives / 14926 sides",
        "D02-C 862 parent equations + 76832 rows",
        "D03",
        "D04",
        "Gate5 18/18 + complete global block",
        "fresh five-gate clean-room",
    ]
    report["formal_global_closure_credit"] = 0
    report["D02_unlock"] = False
    report["d03_authorized"] = False
    report["d04_minted"] = False
    report["gate5_global_maturity"] = "10/18"
    report["complete_global_18_field_block_count"] = 0
    report["cm2_ready"] = False
    report["status"] = (
        "READ_ONLY_PREFLIGHT_COMPLETE__CM2_NO_GO"
        if not section_errors and not failed_checks and sys.flags.dont_write_bytecode
        else "FAIL_CLOSED_PREFLIGHT"
    )
    report["section_error_count"] = len(section_errors)
    report["section_errors"] = section_errors
    report["failed_check_count"] = len(failed_checks)
    report["failed_checks"] = failed_checks
    return report, (0 if report["status"] == "READ_ONLY_PREFLIGHT_COMPLETE__CM2_NO_GO" else 1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="workspace root (default: script's parent workspace)",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        report, code = run(root)
    except Exception as exc:  # keep stdout machine-readable even on bad root
        report = {
            "schema": "cm2.tail-dependency-preflight.failure.v1",
            "status": "FAIL_CLOSED_PREFLIGHT",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "read_only": True,
            "runtime_write_attempted": False,
            "credit_attempted": False,
        }
        code = 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
