#!/usr/bin/env python3
"""Five-layer release checker for the fresh C30a supplemental P0-B v5 run.

This checker never consumes a v4 bundle.  It validates the real precheck,
Docker-enforced offline runtime reconstruction, two producers, comparator,
two verifiers, attacks, independently recomputed trace audit, and postcheck in
strict phase order.  Publication is staged under the run root; a separate
publisher may atomically rename only the exact absent official targets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

_DELIVERABLES_BOOTSTRAP = os.path.dirname(os.path.abspath(__file__))
if _DELIVERABLES_BOOTSTRAP not in sys.path:
    sys.path.insert(0, _DELIVERABLES_BOOTSTRAP)

import cm2_round306c30a_supplemental_audit_closure_v5_common as common
import cm2_round306c30a_supplemental_audit_closure_v5_trace_auditor as auditor
import cm2_round306c30a_supplemental_audit_closure_v5_trace_lib as traces


sys.dont_write_bytecode = True

PREFIX = "cm2_round306c30a_supplemental_audit_closure"
OFFICIAL_SEALED = common.DELIVERABLES / (PREFIX + "_sealed")
OFFICIAL_PAYLOAD = common.DELIVERABLES / (PREFIX + "_payload_manifest.sha256")
OFFICIAL_COLD = common.DELIVERABLES / (PREFIX + "_cold_replay_receipt.json")
OFFICIAL_OUTER = common.DELIVERABLES / (PREFIX + "_outer_verification.json")
OFFICIAL_ROOT = common.DELIVERABLES / (PREFIX + "_root_manifest.sha256")
OFFICIAL_TERMINAL = common.DELIVERABLES / (PREFIX + "_terminal_checker_receipt.json")
OFFICIAL_COMMIT = common.DELIVERABLES / (PREFIX + "_final_commit_receipt.json")
PIPELINE_RECEIPT_NAME = PREFIX + "_pipeline_precommit_receipt.json"

STATIC_PATHS = (
    common.BASE_MANIFEST_REL,
    "deliverables/cm2_round306c30a_python_flint_requirements.lock",
    "deliverables/cm2_round306c30a_python_flint_runtime_lock.json",
    "deliverables/cm2_round306c30a_python_flint_fresh_runtime_rebuild.py",
    "deliverables/cm2_round306c30a_python_flint_fresh_runtime_attestor.py",
    "deliverables/" + common.BASE_PREFIX + "_independent_verifier.py",
    "deliverables/" + PREFIX + "_controlled_replay_launcher.py",
    "deliverables/" + PREFIX + "_coherent_attack_harness.py",
    "deliverables/" + PREFIX + "_protocol.md",
    "deliverables/" + PREFIX + "_strace_analyzer.py",
    "deliverables/" + PREFIX + "_release_checker.py",
    "deliverables/" + PREFIX + "_v5_common.py",
    "deliverables/" + PREFIX + "_v5_trace_lib.py",
    "deliverables/" + PREFIX + "_v5_comparator.py",
    "deliverables/" + PREFIX + "_v5_trace_auditor.py",
    "deliverables/" + PREFIX + "_v5_release_checker.py",
    "deliverables/" + PREFIX + "_v5_offline_pipeline.py",
)

CORE_GROUPS = (
    ("00_base_precheck",),
    ("10_preflight",),
    ("20_runtime_rebuild",),
    ("21_runtime_recheck",),
    ("30_producer_seed30630071", "40_producer_seed30630929"),
    ("50_comparator",),
    ("55_verifier_manifest_pre_seed30630071",
     "55_verifier_manifest_pre_seed30630929"),
    ("60_verifier_seed30630071", "61_verifier_seed30630929"),
    ("65_verifier_manifest_post_seed30630071",
     "65_verifier_manifest_post_seed30630929"),
    ("70_attacks",),
    ("80_trace_audit",),
    ("90_base_postcheck",),
)
MINT_STAGES = (
    "95_assemble_payload", "96_mint_cold", "97_mint_outer",
    "98_build_root", "99_mint_terminal", "100_terminal_replay",
)
FINAL_COMMIT_STAGE = "101_final_commit"
EXCLUDED_RUN_DIRS = {"fresh-python-flint-0.9.0", "pycache", "publication"}


def _manifest_stdout() -> bytes:
    cap = common.capture(common.BASE_MANIFEST_REL)
    common.require(cap.raw is not None, "base manifest retained")
    return b"".join(
        name.encode("ascii") + b": OK\n"
        for name in common.parse_manifest(cap.raw, "base").keys()
    )


def _static_table() -> dict[str, dict[str, Any]]:
    table: dict[str, dict[str, Any]] = {}
    for relpath in STATIC_PATHS:
        cap = common.capture(relpath, retain=False)
        table[relpath] = {"sha256": cap.sha256, "size": cap.size}
    return table


def preflight(root: Path) -> dict[str, Any]:
    common.validate_base_manifest()
    common.require(
        not any((common.DELIVERABLES / name).exists() for name in (
            PREFIX + "_payload_manifest.sha256",
            PREFIX + "_cold_replay_receipt.json",
            PREFIX + "_outer_verification.json",
            PREFIX + "_root_manifest.sha256",
            PREFIX + "_terminal_checker_receipt.json",
            PREFIX + "_final_commit_receipt.json",
        ))
        and not OFFICIAL_SEALED.exists(),
        "fresh official supplemental publication precondition",
    )
    body = {
        "schema": "cm2.round306c30a.supplemental-preflight.v5",
        "status": "READY_FOR_FRESH_P0B_V5_CHAIN__ZERO_AUTHORITY",
        "run_root": common.workspace_rel(root),
        "base_manifest_sha256": common.BASE_MANIFEST_SHA256,
        "static_tools": _static_table(),
        "prohibited_evidence": {
            "v4_bundle_authority": "PERMANENTLY_DISABLED",
            "retrospective_raw_stream_derivation": "FORBIDDEN",
        },
        "conclusion": common.fixed_conclusion(),
    }
    return common.close_object(body)


def _validate_precheck(root: Path, stage_name: str) -> None:
    stage = common.validate_stage(root, stage_name)
    common.require(
        stage["stdout"].raw == _manifest_stdout()
        and stage["stderr"].size == 0
        and stage["receipt"]["inner_argv"] == [
            "/usr/bin/sha256sum", "-c", common.BASE_MANIFEST_REL.split("/", 1)[1]
        ]
        and stage["receipt"].get("working_directory")
        == os.fspath(common.DELIVERABLES),
        "real base manifest check:" + stage_name,
    )


def _validate_preflight_stage(root: Path) -> None:
    stage = common.validate_stage(root, "10_preflight")
    common.require(stage["stdout"].raw is not None, "preflight stdout retained")
    reported = common.strict_json(stage["stdout"].raw, "v5 preflight")
    common.validate_closed(reported, "v5 preflight")
    common.require(
        reported == preflight(root)
        and stage["stderr"].size == 0,
        "preflight/current code exact identity",
    )


def _artifact_matches(row: Any, path: Path, label: str) -> None:
    cap = common.capture(path)
    common.require(
        row == {"path": row.get("path"), "sha256": cap.sha256, "size": cap.size}
        and type(row.get("path")) is str,
        "runtime artifact binding:" + label,
    )


def _validate_runtime(root: Path) -> None:
    rebuild = common.validate_stage(root, "20_runtime_rebuild")
    recheck = common.validate_stage(root, "21_runtime_recheck")
    common.require(
        rebuild["stdout"].raw is not None
        and recheck["stdout"].raw is not None
        and rebuild["stderr"].size == 0
        and recheck["stderr"].size == 0,
        "runtime outer raw streams",
    )
    completion = common.strict_json(rebuild["stdout"].raw, "runtime completion")
    common.require(
        completion.get("schema")
        == "cm2.round306c30a.python-flint-fresh-runtime-completion.v1"
        and completion.get("status")
        == "PASS_FRESH_OFFLINE_RUNTIME_REBUILT_AND_INDEPENDENTLY_ATTESTED",
        "fresh runtime completion",
    )
    runtime = root / "runtime"
    descriptor_cap = common.capture(runtime / "fresh_runtime_rebuild_descriptor.json")
    common.require(descriptor_cap.raw is not None, "runtime descriptor retained")
    descriptor = common.strict_json(descriptor_cap.raw, "runtime descriptor")
    stages = descriptor.get("stages")
    common.require(
        descriptor.get("verdict") == "PASS"
        and descriptor.get("offline") is True
        and descriptor.get("target_precondition") == "ABSENT"
        and descriptor.get("target_policy")
        == "EXCLUSIVE_CREATE_NO_DELETE_NO_OVERWRITE"
        and type(stages) is list
        and [row.get("stage") for row in stages]
        == ["venv_create", "offline_install", "freeze", "attestation"],
        "runtime descriptor stage sequence",
    )
    file_names = {
        "venv_create": ("fresh_runtime_venv_create_stdout.log",
                        "fresh_runtime_venv_create_stderr.log"),
        "offline_install": ("fresh_runtime_offline_install_stdout.log",
                            "fresh_runtime_offline_install_stderr.log"),
        "freeze": ("fresh_runtime_freeze.txt", "fresh_runtime_freeze_stderr.log"),
        "attestation": ("fresh_runtime_attestation.json",
                        "fresh_runtime_attestation_stderr.log"),
    }
    for row in stages:
        name = row["stage"]
        record_cap = common.capture(runtime / f"fresh_runtime_{name}_stage.json")
        common.require(record_cap.raw is not None, "runtime stage retained")
        record = common.strict_json(record_cap.raw, "runtime stage:" + name)
        stdout_name, stderr_name = file_names[name]
        stdout_cap = common.capture(runtime / stdout_name)
        stderr_cap = common.capture(runtime / stderr_name)
        common.require(
            row == record
            and record.get("returncode") == 0
            and record.get("stdout", {}).get("sha256") == stdout_cap.sha256
            and record.get("stdout", {}).get("size") == stdout_cap.size
            and record.get("stderr", {}).get("sha256") == stderr_cap.sha256
            and record.get("stderr", {}).get("size") == stderr_cap.size,
            "runtime same-stage raw binding:" + name,
        )
    attestation = common.capture(runtime / "fresh_runtime_attestation.json")
    common.require(
        attestation.raw == recheck["stdout"].raw,
        "runtime byte-identical attestation recheck",
    )
    attestation_object = common.strict_json(
        attestation.raw or b"", "runtime attestation"
    )
    common.require(
        attestation_object.get("verdict") == "PASS"
        and attestation_object.get("offline") is True
        and attestation_object.get("imported_flint", {}).get(
            "python_flint_version"
        ) == "0.9.0"
        and attestation_object.get("imported_flint", {}).get("flint_version")
        == "3.6.0",
        "runtime attestation semantics",
    )


def _validate_comparator(root: Path) -> None:
    stage = common.validate_stage(root, "50_comparator")
    common.require(stage["stdout"].raw is not None and stage["stderr"].size == 0,
                   "comparator raw streams")
    value = common.strict_json(stage["stdout"].raw, "comparator")
    common.validate_closed(value, "comparator")
    common.require(
        value.get("run_root") == common.workspace_rel(root)
        and value.get("status") == (
            "PASS_REAL_DUAL_SEED_SAME_INVOCATION_EVIDENCE__"
            "KERNEL_NETWORK_NONE__ZERO_ADDITIONAL_CREDIT"
        )
        and value.get("conclusion") == common.fixed_conclusion(),
        "comparator fixed boundary",
    )


def _validate_trace_audit(root: Path) -> dict[str, Any]:
    stage = common.validate_stage(root, "80_trace_audit")
    common.require(stage["stdout"].raw is not None and stage["stderr"].size == 0,
                   "trace audit raw streams")
    reported = common.strict_json(stage["stdout"].raw, "trace audit")
    common.validate_closed(reported, "trace audit")
    recomputed = auditor.build(root)
    common.require(reported == recomputed, "post-attack trace audit exact recomputation")
    return reported


def _phase_order(root: Path, groups: Iterable[tuple[str, ...]]) -> None:
    previous: list[dict[str, Any]] | None = None
    for group in groups:
        current = [common.validate_stage(root, name) for name in group]
        if previous is not None:
            for before in previous:
                for after in current:
                    common.require(
                        before["receipt_capture"].mtime_ns
                        < after["start_capture"].mtime_ns
                        and before["receipt_capture"].ctime_ns
                        < after["start_capture"].ctime_ns
                        and before["receipt"]["ended_wall_time_ns"]
                        <= after["start"]["wall_time_ns"],
                        "strict stage partial order:"
                        + before["receipt"]["stage"] + "->" + after["receipt"]["stage"],
                    )
        previous = current


def validate_core(root: Path) -> dict[str, Any]:
    common.validate_base_manifest()
    _validate_precheck(root, "00_base_precheck")
    _validate_preflight_stage(root)
    _validate_runtime(root)
    for seed in common.SEEDS:
        common.validate_stage(root, traces.PRODUCER_STAGES[seed])
        traces.exact_candidate(root, seed)
    _validate_comparator(root)
    trace = _validate_trace_audit(root)
    _validate_precheck(root, "90_base_postcheck")
    _phase_order(root, CORE_GROUPS)
    return trace


def _walk_evidence(root: Path) -> list[tuple[str, Path]]:
    selected_roots = [
        *(root / "stages" / name for group in CORE_GROUPS for name in group),
        root / "runtime", root / "candidates", root / "provenance",
        root / "attacks",
    ]
    result: list[tuple[str, Path]] = []
    for selected in selected_roots:
        status = selected.lstat()
        common.require(stat.S_ISDIR(status.st_mode) and not selected.is_symlink(),
                       "evidence root directory")
        pending = [selected]
        while pending:
            directory = pending.pop()
            for entry in sorted(os.scandir(directory), key=lambda item: os.fsencode(item.name)):
                path = directory / entry.name
                relative_parts = path.relative_to(root).parts
                if any(part in EXCLUDED_RUN_DIRS for part in relative_parts):
                    continue
                common.require(not entry.is_symlink(), "evidence no symlink")
                if entry.is_dir(follow_symlinks=False):
                    pending.append(path)
                elif entry.is_file(follow_symlinks=False):
                    rel = path.relative_to(root).as_posix()
                    result.append((rel, path))
                else:
                    raise common.Reject("evidence special entry:" + os.fspath(path))
    descriptor = root / "run_descriptor.json"
    result.append(("run_descriptor.json", descriptor))
    names = [name for name, _ in result]
    common.require(len(names) == len(set(names)), "evidence unique paths")
    return sorted(result, key=lambda row: os.fsencode(row[0]))


def _mkdirs(root: Path, relative_files: Iterable[str]) -> None:
    directories: set[str] = set()
    for name in relative_files:
        parent = PurePosixPath(name).parent
        while parent.as_posix() != ".":
            directories.add(parent.as_posix())
            parent = parent.parent
    for name in sorted(directories, key=lambda value: (value.count("/"), os.fsencode(value))):
        (root / name).mkdir(mode=0o755)


def _copy_once(source: Path, target: Path) -> tuple[str, int]:
    common.validate_parent_chain(source, final_may_be_absent=True)
    before = source.lstat()
    common.require(stat.S_ISREG(before.st_mode) and not source.is_symlink()
                   and before.st_nlink == 1, "copy source singleton")
    source_fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    target_fd = os.open(
        target,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
        0o444,
    )
    digest = hashlib.sha256()
    total = 0
    try:
        opened = os.fstat(source_fd)
        common.require(
            (opened.st_dev, opened.st_ino, opened.st_size,
             opened.st_mtime_ns, opened.st_ctime_ns)
            == (before.st_dev, before.st_ino, before.st_size,
                before.st_mtime_ns, before.st_ctime_ns),
            "copy source pre/open identity",
        )
        remaining = opened.st_size
        while remaining:
            block = os.read(source_fd, min(1 << 20, remaining))
            common.require(bool(block), "copy source short read")
            digest.update(block)
            offset = 0
            while offset < len(block):
                count = os.write(target_fd, block[offset:])
                common.require(count > 0, "copy target short write")
                offset += count
            total += len(block)
            remaining -= len(block)
        common.require(not os.read(source_fd, 1), "copy source growing")
        final = os.fstat(source_fd)
        common.require(
            (final.st_dev, final.st_ino, final.st_size,
             final.st_mtime_ns, final.st_ctime_ns)
            == (opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns, opened.st_ctime_ns),
            "copy source open/final identity",
        )
        os.fsync(target_fd)
    finally:
        os.close(source_fd)
        os.close(target_fd)
    after = source.lstat()
    common.require(
        (after.st_dev, after.st_ino, after.st_size,
         after.st_mtime_ns, after.st_ctime_ns)
        == (before.st_dev, before.st_ino, before.st_size,
            before.st_mtime_ns, before.st_ctime_ns),
        "copy source post identity",
    )
    return digest.hexdigest(), total


def _publication(root: Path) -> Path:
    path = root / "publication"
    status = path.lstat()
    common.require(stat.S_ISDIR(status.st_mode) and not path.is_symlink(),
                   "publication staging directory")
    return path


def assemble(root: Path) -> dict[str, Any]:
    trace = validate_core(root)
    publication = _publication(root)
    sealed = publication / OFFICIAL_SEALED.name
    sealed.mkdir(mode=0o755)
    evidence_root = sealed / "evidence"
    evidence_root.mkdir(mode=0o755)
    sources = _walk_evidence(root)
    _mkdirs(evidence_root, (name for name, _ in sources))
    rows: dict[str, Any] = {}
    for name, source in sources:
        target = evidence_root / name
        digest, size = _copy_once(source, target)
        rows[name] = {
            "source_relpath": common.workspace_rel(source),
            "sealed_relpath": "evidence/" + name,
            "sha256": digest,
            "size": size,
        }
    source_manifest = common.close_object({
        "schema": "cm2.round306c30a.supplemental-evidence-source-map.v5",
        "status": "PASS_FRESH_V5_SOURCE_MAP__NO_V4_INPUTS",
        "run_root": common.workspace_rel(root),
        "files": rows,
        "trace_audit_payload_sha256": trace["payload_sha256"],
        "conclusion": common.fixed_conclusion(),
    })
    common.write_json(sealed / "source_manifest.json", source_manifest)
    payload_rows: dict[str, str] = {}
    for relpath in STATIC_PATHS:
        payload_rows[relpath] = common.capture(relpath, retain=False).sha256
    for name in sorted(rows, key=os.fsencode):
        relpath = "deliverables/" + OFFICIAL_SEALED.name + "/evidence/" + name
        payload_rows[relpath] = rows[name]["sha256"]
    source_cap = common.capture(sealed / "source_manifest.json", retain=False)
    payload_rows[
        "deliverables/" + OFFICIAL_SEALED.name + "/source_manifest.json"
    ] = source_cap.sha256
    payload_raw = b"".join(
        payload_rows[name].encode("ascii") + b"  " + name.encode("ascii") + b"\n"
        for name in sorted(payload_rows, key=os.fsencode)
    )
    payload_staging = publication / OFFICIAL_PAYLOAD.name
    common.write_exclusive(payload_staging, payload_raw)
    return {
        "schema": "cm2.round306c30a.supplemental-assembly-result.v5",
        "status": "PASS_STAGED_SEALED_EVIDENCE_AND_PAYLOAD__NOT_YET_AUTHORITY",
        "sealed_staging": common.workspace_rel(sealed),
        "payload_staging": common.workspace_rel(payload_staging),
        "payload_manifest_sha256": common.sha256(payload_raw),
        "payload_member_count": len(payload_rows),
        "conclusion": common.fixed_conclusion(),
    }


def _scan_sealed_exact(
    source_map: dict[str, Any], sealed_root: Path
) -> dict[str, common.Capture]:
    expected = {"source_manifest.json"}
    expected.update("evidence/" + name for name in source_map["files"])
    actual: set[str] = set()
    pending = [sealed_root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            common.require(not entry.is_symlink(), "official seal no symlink")
            path = directory / entry.name
            if entry.is_dir(follow_symlinks=False):
                pending.append(path)
            elif entry.is_file(follow_symlinks=False):
                actual.add(path.relative_to(sealed_root).as_posix())
            else:
                raise common.Reject("official seal special entry")
    common.require(actual == expected, "official seal exact file map")
    return {
        name: common.capture(sealed_root / name, retain=False)
        for name in sorted(expected, key=os.fsencode)
    }


def validate_payload(
    expected_sha: str, *, staging_root: Path | None = None
) -> tuple[common.Capture, dict[str, str]]:
    common.validate_base_manifest()
    common.require(common.HEX64.fullmatch(expected_sha) is not None,
                   "external payload SHA256")
    payload_path = (
        OFFICIAL_PAYLOAD if staging_root is None
        else _publication(staging_root) / OFFICIAL_PAYLOAD.name
    )
    sealed_root = (
        OFFICIAL_SEALED if staging_root is None
        else _publication(staging_root) / OFFICIAL_SEALED.name
    )
    payload = common.capture(payload_path)
    common.require(payload.raw is not None and payload.sha256 == expected_sha,
                   "payload external pin")
    rows = common.parse_manifest(payload.raw, "supplemental v5 payload")
    source_cap = common.capture(sealed_root / "source_manifest.json")
    common.require(source_cap.raw is not None, "source map retained")
    source_map = common.strict_json(source_cap.raw, "source map")
    common.validate_closed(source_map, "source map")
    sealed = _scan_sealed_exact(source_map, sealed_root)
    expected_paths = set(STATIC_PATHS)
    expected_paths.update(
        "deliverables/" + OFFICIAL_SEALED.name + "/" + name for name in sealed
    )
    common.require(set(rows) == expected_paths, "payload exact member map")
    for relpath in STATIC_PATHS:
        common.require(common.capture(relpath, retain=False).sha256 == rows[relpath],
                       "payload static hash:" + relpath)
    for name, cap in sealed.items():
        relpath = "deliverables/" + OFFICIAL_SEALED.name + "/" + name
        common.require(cap.sha256 == rows[relpath], "payload sealed hash:" + name)
    for name, row in source_map["files"].items():
        cap = sealed["evidence/" + name]
        common.require(
            row.get("sealed_relpath") == "evidence/" + name
            and row.get("sha256") == cap.sha256
            and row.get("size") == cap.size
            and not row.get("source_relpath", "").startswith(
                ".cm2-runtime/audit/c30a-supplemental-release-evidence-v4"
            ),
            "source map sealed binding:" + name,
        )
    common.require(source_map.get("conclusion") == common.fixed_conclusion(),
                   "source map fixed conclusion")
    return payload, rows


def _output_path(root: Path, name: str) -> Path:
    common.require(name in {
        OFFICIAL_COLD.name, OFFICIAL_OUTER.name, OFFICIAL_ROOT.name,
        OFFICIAL_TERMINAL.name, OFFICIAL_COMMIT.name,
    }, "known publication output")
    path = _publication(root) / name
    common.require(not path.exists() and not path.is_symlink(), "fresh staged output")
    return path


def mint_cold(root: Path, expected_payload: str) -> dict[str, Any]:
    payload, rows = validate_payload(expected_payload, staging_root=root)
    body = {
        "schema": "cm2.round306c30a.supplemental-audit-cold-receipt.v1",
        "status": "PASS_PAYLOAD_AND_AUTHORITATIVE_FULL_TRACE_COLD_REPLAY",
        "payload_manifest_sha256": payload.sha256,
        "payload_member_count": len(rows),
        "trace_audit_payload_sha256": common.strict_json(
            common.capture(
                _publication(root) / OFFICIAL_SEALED.name / "source_manifest.json"
            ).raw or b"",
            "source map cold",
        )["trace_audit_payload_sha256"],
        "receipt_file_sha256": None,
        "conclusion": common.fixed_conclusion(),
    }
    value = common.close_object(body)
    output = _output_path(root, OFFICIAL_COLD.name)
    common.write_json(output, value)
    return {"status": "COLD_RECEIPT_STAGED__NOT_YET_AUTHORITY",
            "sha256": common.capture(output, retain=False).sha256}


def _closed_file(path: Path, label: str) -> tuple[common.Capture, dict[str, Any]]:
    cap = common.capture(path)
    common.require(cap.raw is not None, "closed file retained:" + label)
    value = common.strict_json(cap.raw, label)
    common.validate_closed(value, label)
    return cap, value


def mint_outer(root: Path, expected_payload: str, expected_cold: str) -> dict[str, Any]:
    payload, _ = validate_payload(expected_payload, staging_root=root)
    cold_cap, cold = _closed_file(
        _publication(root) / OFFICIAL_COLD.name, "cold receipt"
    )
    common.require(
        cold_cap.sha256 == expected_cold
        and cold.get("payload_manifest_sha256") == payload.sha256
        and cold.get("conclusion") == common.fixed_conclusion(),
        "external cold receipt binding",
    )
    value = common.close_object({
        "schema": "cm2.round306c30a.supplemental-audit-outer-verification.v1",
        "status": "PASS_SUPPLEMENTAL_AUDIT_CLOSURE__ZERO_ADDITIONAL_CREDIT",
        "payload_manifest_sha256": payload.sha256,
        "cold_replay_receipt_sha256": cold_cap.sha256,
        "conclusion": common.fixed_conclusion(),
    })
    output = _output_path(root, OFFICIAL_OUTER.name)
    common.write_json(output, value)
    return {"status": "OUTER_VERIFICATION_STAGED__NOT_YET_AUTHORITY",
            "sha256": common.capture(output, retain=False).sha256}


def build_root(root: Path, expected_payload: str, expected_cold: str) -> dict[str, Any]:
    payload, _ = validate_payload(expected_payload, staging_root=root)
    cold_cap, cold = _closed_file(
        _publication(root) / OFFICIAL_COLD.name, "cold receipt"
    )
    outer_cap, outer = _closed_file(
        _publication(root) / OFFICIAL_OUTER.name, "outer verification"
    )
    common.require(
        cold_cap.sha256 == expected_cold
        and outer.get("payload_manifest_sha256") == payload.sha256
        and outer.get("cold_replay_receipt_sha256") == cold_cap.sha256,
        "root inputs closed",
    )
    raw = b"".join(
        digest.encode("ascii") + b"  " + common.workspace_rel(path).encode("ascii") + b"\n"
        for path, digest in sorted(
            ((OFFICIAL_PAYLOAD, payload.sha256), (OFFICIAL_OUTER, outer_cap.sha256)),
            key=lambda row: os.fsencode(common.workspace_rel(row[0])),
        )
    )
    output = _output_path(root, OFFICIAL_ROOT.name)
    common.write_exclusive(output, raw)
    return {"status": "ROOT_MANIFEST_STAGED__NOT_YET_AUTHORITY",
            "sha256": common.capture(output, retain=False).sha256}


def mint_terminal(
    root: Path, expected_payload: str, expected_cold: str, expected_root: str
) -> dict[str, Any]:
    payload, _ = validate_payload(expected_payload, staging_root=root)
    cold_cap, cold = _closed_file(
        _publication(root) / OFFICIAL_COLD.name, "cold receipt"
    )
    outer_cap, outer = _closed_file(
        _publication(root) / OFFICIAL_OUTER.name, "outer verification"
    )
    root_cap = common.capture(_publication(root) / OFFICIAL_ROOT.name)
    common.require(root_cap.raw is not None and root_cap.sha256 == expected_root,
                   "external root pin")
    rows = common.parse_manifest(root_cap.raw, "root manifest")
    common.require(rows == {
        common.workspace_rel(OFFICIAL_PAYLOAD): payload.sha256,
        common.workspace_rel(OFFICIAL_OUTER): outer_cap.sha256,
    }, "root exact two-member map")
    common.require(
        cold_cap.sha256 == expected_cold
        and cold.get("conclusion") == common.fixed_conclusion()
        and outer.get("conclusion") == common.fixed_conclusion(),
        "terminal predecessor closure",
    )
    value = common.close_object({
        "schema": "cm2.round306c30a.supplemental-audit-terminal-receipt.v1",
        "status": (
            "PASS_TERMINAL_C30A_SUPPLEMENTAL_AUDIT_AUTHORIZATION__"
            "252_TO_92_ONLY"
        ),
        "root_manifest_sha256": root_cap.sha256,
        "payload_manifest_sha256": payload.sha256,
        "outer_verification_sha256": outer_cap.sha256,
        "cold_replay_receipt_sha256": cold_cap.sha256,
        "authority_condition": (
            "REQUIRES_POST_PUBLICATION_STAGE100_REPLAY_AND_FINAL_COMMIT"
        ),
        "conclusion": common.fixed_conclusion(),
    })
    output = _output_path(root, OFFICIAL_TERMINAL.name)
    common.write_json(output, value)
    return value


def check_terminal(
    root: Path, expected_payload: str, expected_cold: str,
    expected_root: str, expected_terminal: str,
) -> dict[str, Any]:
    payload, _ = validate_payload(expected_payload)
    cold_cap, cold = _closed_file(OFFICIAL_COLD, "cold receipt")
    outer_cap, outer = _closed_file(OFFICIAL_OUTER, "outer verification")
    root_cap = common.capture(OFFICIAL_ROOT)
    terminal_cap, terminal = _closed_file(OFFICIAL_TERMINAL, "terminal receipt")
    common.require(
        cold_cap.sha256 == expected_cold
        and root_cap.sha256 == expected_root
        and terminal_cap.sha256 == expected_terminal
        and terminal.get("root_manifest_sha256") == root_cap.sha256
        and terminal.get("payload_manifest_sha256") == payload.sha256
        and terminal.get("outer_verification_sha256") == outer_cap.sha256
        and terminal.get("cold_replay_receipt_sha256") == cold_cap.sha256
        and terminal.get("authority_condition")
        == "REQUIRES_POST_PUBLICATION_STAGE100_REPLAY_AND_FINAL_COMMIT"
        and terminal.get("conclusion") == common.fixed_conclusion()
        and cold.get("conclusion") == common.fixed_conclusion()
        and outer.get("conclusion") == common.fixed_conclusion(),
        "terminal chain exact external pins",
    )
    _phase_order(root, CORE_GROUPS + tuple((name,) for name in MINT_STAGES[:-1]))
    return common.close_object({
        "schema": "cm2.round306c30a.supplemental-terminal-replay.v5",
        "status": "PASS_FULL_FIVE_LAYER_TERMINAL_REPLAY__252_TO_92_ONLY",
        "payload_manifest_sha256": payload.sha256,
        "cold_replay_receipt_sha256": cold_cap.sha256,
        "outer_verification_sha256": outer_cap.sha256,
        "root_manifest_sha256": root_cap.sha256,
        "terminal_receipt_sha256": terminal_cap.sha256,
        "conclusion": common.fixed_conclusion(),
    })


def _sealed_tree_record() -> dict[str, Any]:
    """Hash the exact official sealed directory as one of six targets."""

    status = OFFICIAL_SEALED.lstat()
    common.require(
        stat.S_ISDIR(status.st_mode) and not OFFICIAL_SEALED.is_symlink(),
        "official sealed directory",
    )
    rows: list[tuple[str, common.Capture]] = []
    pending = [OFFICIAL_SEALED]
    while pending:
        directory = pending.pop()
        for entry in sorted(os.scandir(directory), key=lambda item: os.fsencode(item.name)):
            common.require(not entry.is_symlink(), "official tree no symlink")
            path = directory / entry.name
            if entry.is_dir(follow_symlinks=False):
                pending.append(path)
            elif entry.is_file(follow_symlinks=False):
                rows.append((path.relative_to(OFFICIAL_SEALED).as_posix(), common.capture(path)))
            else:
                raise common.Reject("official tree special entry")
    rows.sort(key=lambda row: os.fsencode(row[0]))
    common.require(bool(rows), "official tree nonempty")
    raw = b"".join(
        cap.sha256.encode("ascii") + b" "
        + str(cap.size).encode("ascii") + b" "
        + name.encode("ascii") + b"\n"
        for name, cap in rows
    )
    return {
        "kind": "directory-tree",
        "sha256": common.sha256(raw),
        "file_count": len(rows),
        "total_size": sum(cap.size for _, cap in rows),
    }


def _official_target_table() -> dict[str, Any]:
    table: dict[str, Any] = {
        common.workspace_rel(OFFICIAL_SEALED): _sealed_tree_record(),
    }
    for path in (
        OFFICIAL_PAYLOAD, OFFICIAL_COLD, OFFICIAL_OUTER,
        OFFICIAL_ROOT, OFFICIAL_TERMINAL,
    ):
        cap = common.capture(path, retain=False)
        table[common.workspace_rel(path)] = {
            "kind": "file", "sha256": cap.sha256, "size": cap.size,
        }
    common.require(len(table) == 6, "exact six official precommit targets")
    return table


def _stage_artifacts(stage: dict[str, Any]) -> dict[str, Any]:
    captures = {
        "exit": stage["receipt_capture"],
        "start": stage["start_capture"],
        "stdout": stage["stdout"],
        "stderr": stage["stderr"],
        "time": stage["time"],
        "docker_inspect_pre": stage["inspect_pre"],
        "docker_inspect_post": stage["inspect_post"],
        "docker_inspect_pre_raw": stage["inspect_pre_raw"],
        "docker_inspect_post_raw": stage["inspect_post_raw"],
        "docker_create_stdout": stage["create_stdout"],
        "docker_create_stderr": stage["create_stderr"],
    }
    return {
        name: {"sha256": cap.sha256, "size": cap.size}
        for name, cap in sorted(captures.items())
    }


def build_pipeline_receipt(
    root: Path, expected_payload: str, expected_cold: str,
    expected_root: str, expected_terminal: str,
) -> dict[str, Any]:
    """Recompute all post-publication inputs before a final commit can exist."""

    expected_replay = check_terminal(
        root, expected_payload, expected_cold, expected_root, expected_terminal
    )
    stage = common.validate_stage(root, "100_terminal_replay")
    common.require(
        stage["stdout"].raw is not None
        and stage["stderr"].size == 0
        and common.strict_json(stage["stdout"].raw, "stage100 replay")
        == expected_replay,
        "post-publication stage100 exact replay",
    )
    _phase_order(root, CORE_GROUPS + tuple((name,) for name in MINT_STAGES))
    targets = _official_target_table()
    common.require(
        targets[common.workspace_rel(OFFICIAL_PAYLOAD)]["sha256"]
        == expected_payload
        and targets[common.workspace_rel(OFFICIAL_COLD)]["sha256"]
        == expected_cold
        and targets[common.workspace_rel(OFFICIAL_ROOT)]["sha256"]
        == expected_root
        and targets[common.workspace_rel(OFFICIAL_TERMINAL)]["sha256"]
        == expected_terminal,
        "six-target external pins",
    )
    return common.close_object({
        "schema": "cm2.round306c30a.supplemental-pipeline-precommit.v5",
        "status": "PASS_STAGE100_AND_SIX_OFFICIAL_TARGETS__READY_TO_COMMIT",
        "run_root": common.workspace_rel(root),
        "official_targets": targets,
        "stage100_receipt": stage["receipt"],
        "stage100_artifacts": _stage_artifacts(stage),
        "terminal_replay": expected_replay,
        "conclusion": common.fixed_conclusion(),
    })


def mint_final_commit(
    root: Path, expected_payload: str, expected_cold: str,
    expected_root: str, expected_terminal: str,
    expected_pipeline_receipt: str,
) -> dict[str, Any]:
    common.require(
        common.HEX64.fullmatch(expected_pipeline_receipt) is not None,
        "external pipeline precommit receipt SHA256",
    )
    receipt_cap, receipt = _closed_file(
        root / PIPELINE_RECEIPT_NAME, "pipeline precommit receipt"
    )
    recomputed = build_pipeline_receipt(
        root, expected_payload, expected_cold, expected_root, expected_terminal
    )
    common.require(
        receipt_cap.sha256 == expected_pipeline_receipt
        and receipt == recomputed,
        "pipeline precommit exact independent recomputation",
    )
    value = common.close_object({
        "schema": "cm2.round306c30a.supplemental-final-commit.v5",
        "status": (
            "PASS_FINAL_COMMIT_AFTER_POST_PUBLICATION_REPLAY__"
            "ZERO_ADDITIONAL_CREDIT"
        ),
        "run_root": common.workspace_rel(root),
        "pipeline_precommit_receipt_sha256": receipt_cap.sha256,
        "pipeline_precommit_receipt": receipt,
        "official_targets": receipt["official_targets"],
        "stage100_exit_sha256": receipt["stage100_artifacts"]["exit"]["sha256"],
        "conclusion": common.fixed_conclusion(),
    })
    output = _output_path(root, OFFICIAL_COMMIT.name)
    common.write_json(output, value)
    return value


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("mode", choices=(
        "preflight", "assemble", "mint-cold", "mint-outer", "build-root",
        "mint-terminal", "check-terminal", "mint-final-commit",
    ))
    value.add_argument("--run-root", required=True)
    value.add_argument("--expected-payload-sha256")
    value.add_argument("--expected-cold-sha256")
    value.add_argument("--expected-root-sha256")
    value.add_argument("--expected-terminal-sha256")
    value.add_argument("--expected-pipeline-receipt-sha256")
    return value


def main() -> int:
    try:
        args = parser().parse_args()
        root = common.run_root(args.run_root)
        if args.mode == "preflight":
            result = preflight(root)
        elif args.mode == "assemble":
            result = assemble(root)
        elif args.mode == "mint-cold":
            result = mint_cold(root, args.expected_payload_sha256 or "")
        elif args.mode == "mint-outer":
            result = mint_outer(
                root, args.expected_payload_sha256 or "",
                args.expected_cold_sha256 or "",
            )
        elif args.mode == "build-root":
            result = build_root(
                root, args.expected_payload_sha256 or "",
                args.expected_cold_sha256 or "",
            )
        elif args.mode == "mint-terminal":
            result = mint_terminal(
                root, args.expected_payload_sha256 or "",
                args.expected_cold_sha256 or "", args.expected_root_sha256 or "",
            )
        elif args.mode == "check-terminal":
            result = check_terminal(
                root, args.expected_payload_sha256 or "",
                args.expected_cold_sha256 or "", args.expected_root_sha256 or "",
                args.expected_terminal_sha256 or "",
            )
        else:
            result = mint_final_commit(
                root, args.expected_payload_sha256 or "",
                args.expected_cold_sha256 or "", args.expected_root_sha256 or "",
                args.expected_terminal_sha256 or "",
                args.expected_pipeline_receipt_sha256 or "",
            )
    except Exception as error:
        print(
            "C30A_SUPPLEMENTAL_V5_RELEASE_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1
    sys.stdout.buffer.write(common.canonical(result) + b"\n")
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
