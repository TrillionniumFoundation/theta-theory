#!/usr/bin/env python3
"""Independent trace reconstruction helpers for C30a supplemental v5."""

from __future__ import annotations

import copy
import os
import stat
from pathlib import Path
from typing import Any

import sys

_DELIVERABLES_BOOTSTRAP = os.path.dirname(os.path.abspath(__file__))
if _DELIVERABLES_BOOTSTRAP not in sys.path:
    sys.path.insert(0, _DELIVERABLES_BOOTSTRAP)

import cm2_round306c30a_supplemental_audit_closure_v5_common as common


PRODUCER_STAGES = {
    "30630071": "30_producer_seed30630071",
    "30630929": "40_producer_seed30630929",
}
VERIFIER_STAGES = {
    "30630071": "60_verifier_seed30630071",
    "30630929": "61_verifier_seed30630929",
}


def candidate_dir(root: Path, seed: str) -> Path:
    return root / "candidates" / ("seed" + seed)


def provenance_path(root: Path, seed: str) -> Path:
    return root / "provenance" / ("seed" + seed + ".json")


def exact_candidate(root: Path, seed: str) -> dict[str, common.Capture]:
    directory = candidate_dir(root, seed)
    status = directory.lstat()
    common.require(
        stat.S_ISDIR(status.st_mode) and not directory.is_symlink(),
        "candidate directory:" + seed,
    )
    actual: set[str] = set()
    captures: dict[str, common.Capture] = {}
    with os.scandir(directory) as iterator:
        for entry in iterator:
            common.require(
                entry.is_file(follow_symlinks=False) and not entry.is_symlink(),
                "candidate regular entry:" + seed + ":" + entry.name,
            )
            actual.add(entry.name)
    common.require(actual == set(common.OUTPUT_NAMES), "candidate exact map:" + seed)
    for name in common.OUTPUT_NAMES:
        cap = common.capture(directory / name)
        common.require(
            cap.sha256 == common.OUTPUT_HASHES[name],
            "candidate equals formal C30a seal:" + seed + ":" + name,
        )
        captures[name] = cap
    return captures


def _contract(
    root: Path,
    *,
    kind: str,
    seed: str,
    analyzer: Any,
) -> tuple[dict[str, Any], dict[str, Any]]:
    common.require(kind in {"producer", "verifier"}, "trace role kind")
    stage_name = (
        PRODUCER_STAGES[seed] if kind == "producer" else VERIFIER_STAGES[seed]
    )
    stage = common.validate_stage(root, stage_name)
    trace = common.capture(root / "stages" / stage_name / "trace.raw")
    candidates = exact_candidate(root, seed)
    common.require(stage["stdout"].raw is not None, "trace stdout retained")
    stdout_object = common.strict_json(
        stage["stdout"].raw, stage_name + " stdout", newline=True
    )
    legacy = common.load_legacy_checker()
    allowed: list[str] = []
    protected = [
        os.fspath(common.DELIVERABLES),
        os.fspath(common.WORKSPACE / ".cm2-runtime/python-flint-0.9.0"),
        os.fspath(common.WORKSPACE / ".cm2-runtime/candidates"),
    ]
    if kind == "producer":
        allowed = sorted([
            os.fspath(candidate_dir(root, seed)),
            os.fspath(provenance_path(root, seed)),
            *(os.fspath(candidate_dir(root, seed) / name)
              for name in common.OUTPUT_NAMES),
        ])
        protected.append(
            os.fspath(candidate_dir(root, common.SEEDS[1] if seed == common.SEEDS[0]
                                     else common.SEEDS[0]))
        )
    else:
        protected.append(os.fspath(candidate_dir(root, seed)))
    contract = {
        "schema": analyzer.CONTRACT_SCHEMA,
        "profile": "c30a-p0b-v5-" + kind + "-seed" + seed,
        "workspace": os.fspath(common.WORKSPACE),
        "paths": {
            "trace": os.fspath(root / "stages" / stage_name / "trace.raw"),
            "stdout": os.fspath(root / "stages" / stage_name / "stdout.raw"),
            "stderr": os.fspath(root / "stages" / stage_name / "stderr.raw"),
            "time": os.fspath(root / "stages" / stage_name / "time.txt"),
            "manifest": os.fspath(common.WORKSPACE / common.BASE_MANIFEST_REL),
            "candidate_dir": os.fspath(candidate_dir(root, seed)),
        },
        "pins": {
            "trace_sha256": trace.sha256,
            "stdout_sha256": stage["stdout"].sha256,
            "stderr_sha256": stage["stderr"].sha256,
            "time_sha256": stage["time"].sha256,
            "manifest_sha256": common.BASE_MANIFEST_SHA256,
        },
        "manifest_members": legacy.BASE_MEMBERS,
        "candidate_members": common.OUTPUT_HASHES,
        "candidate_manifest_bindings": {
            name: "cm2_round306c30a_sealed/" + name
            for name in common.OUTPUT_NAMES
        },
        "stdout": {
            "policy": "one-canonical-json-write",
            "expected_object": stdout_object,
        },
        "stderr": {
            "policy": "c30a-round215-diagnostics",
            "expected_line_count": 50,
        },
        "allowed_write_paths": allowed,
        "protected_roots": protected,
        "capture": {
            "require_follow_forks": True,
            "require_fd_path_decoding": True,
            "require_percent_file": True,
            "minimum_string_limit": 4096,
            "stream_transport": "docker-attach-pipe",
            "required_explicit_syscalls": analyzer.REQUIRED_EXPLICIT_CAPTURE_SYSCALLS,
        },
    }
    return contract, {
        "stage": stage,
        "trace": trace,
        "candidate": candidates,
        "stage_name": stage_name,
    }


def _decoded_path(analyzer: Any, call: Any) -> str | None:
    if call.name in {"open", "stat", "lstat", "access", "readlink", "mkdir"}:
        index = 0
    elif call.name in {
        "openat", "openat2", "newfstatat", "faccessat", "faccessat2",
        "readlinkat", "mkdirat",
    }:
        index = 1
    else:
        return None
    if len(call.args) <= index:
        return None
    try:
        return analyzer.decode_c_string(call.args[index]).decode("utf-8", "strict")
    except Exception:
        return None


def _normalize(path: str) -> str:
    return os.path.normpath(
        path if os.path.isabs(path) else os.fspath(common.WORKSPACE / path)
    )


def cold_facts(analyzer: Any, trace_raw: bytes, root: Path, seed: str) -> dict[str, Any]:
    """Derive cold-start claims only from the complete syscall trace."""

    calls = analyzer.parse_trace(trace_raw)
    candidate = os.path.normpath(os.fspath(candidate_dir(root, seed)))
    pycache = os.path.normpath(os.fspath(root / "pycache" / ("seed" + seed)))
    successful_candidate_mkdir: list[int] = []
    failed_candidate_mkdir: list[int] = []
    candidate_success_before_mkdir: list[int] = []
    candidate_absence_probes: list[int] = []
    pycache_success: list[int] = []
    pycache_absence_probes: list[int] = []
    successful_pyc_reads: list[int] = []
    network_calls: list[int] = []

    for call in calls:
        if call.name in common.NETWORK_SYSCALLS:
            network_calls.append(call.line_number)
        decoded = _decoded_path(analyzer, call)
        normalized = _normalize(decoded) if decoded is not None else None
        if normalized == candidate:
            if call.name in {"mkdir", "mkdirat"}:
                if call.result_integer == 0:
                    successful_candidate_mkdir.append(call.line_number)
                else:
                    failed_candidate_mkdir.append(call.line_number)
            elif call.result_integer is not None and call.result_integer >= 0:
                first_mkdir = successful_candidate_mkdir[0] if successful_candidate_mkdir else 10**18
                if call.line_number < first_mkdir:
                    candidate_success_before_mkdir.append(call.line_number)
            elif "ENOENT" in call.result_text:
                candidate_absence_probes.append(call.line_number)
        if normalized is not None and (
            normalized == pycache or normalized.startswith(pycache + os.sep)
        ):
            if call.result_integer is not None and call.result_integer >= 0:
                pycache_success.append(call.line_number)
            elif "ENOENT" in call.result_text:
                pycache_absence_probes.append(call.line_number)
        if decoded is not None and decoded.endswith(".pyc") and call.name in {
            "open", "openat", "openat2"
        } and call.result_integer is not None and call.result_integer >= 0:
            successful_pyc_reads.append(call.line_number)
        if call.name in {"read", "readv", "pread64", "preadv", "preadv2"}:
            first = call.args[0] if call.args else ""
            if ".pyc>" in first and call.result_integer is not None and call.result_integer >= 0:
                successful_pyc_reads.append(call.line_number)

    facts = {
        "candidate_absence_probe_lines": candidate_absence_probes,
        "candidate_preexisted": bool(candidate_success_before_mkdir),
        "candidate_success_before_mkdir_lines": candidate_success_before_mkdir,
        "failed_candidate_mkdir_lines": failed_candidate_mkdir,
        "fresh_candidate_mkdir_lines": successful_candidate_mkdir,
        "fresh_candidate_mkdir_succeeded": len(successful_candidate_mkdir) == 1,
        "network_syscall_lines": network_calls,
        "network_syscalls": len(network_calls),
        "pycache_absence_probe_lines": pycache_absence_probes,
        "pycache_prefix_preexisted": bool(pycache_success),
        "pycache_success_lines": pycache_success,
        "successful_pyc_read_lines": successful_pyc_reads,
        "successful_pyc_reads": len(successful_pyc_reads),
    }
    common.require(
        bool(candidate_absence_probes)
        and facts["candidate_preexisted"] is False
        and facts["fresh_candidate_mkdir_succeeded"] is True
        and failed_candidate_mkdir == []
        and facts["pycache_prefix_preexisted"] is False
        and facts["successful_pyc_reads"] == 0
        and facts["network_syscalls"] == 0,
        "analyzer-derived cold facts:seed" + seed,
    )
    return facts


def normalize_result(result: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(result)
    common.require(
        type(normalized.get("contract")) is dict
        and type(normalized["contract"].get("source")) is str,
        "analyzer result provenance source",
    )
    normalized["contract"]["source"] = "<PROVENANCE_SOURCE_NORMALIZED>"
    return normalized


def analyze_role(
    root: Path,
    *,
    kind: str,
    seed: str,
    source: str,
) -> dict[str, Any]:
    common.require(seed in common.SEEDS, "known trace seed")
    analyzer = common.load_analyzer()
    contract, evidence = _contract(root, kind=kind, seed=seed, analyzer=analyzer)
    contract_sha = common.sha256(analyzer.canonical_bytes(contract))
    result = analyzer.audit(contract, source, contract_sha)
    trace_contract = result.get("trace_contract", {})
    syscall_counts = trace_contract.get("syscall_counts", {})
    network_count = sum(syscall_counts.get(name, 0) for name in common.NETWORK_SYSCALLS)
    common.require(
        result.get("status") == "PASS_C30A_STRACE_ZERO_MUTATION_CERTIFIED"
        and result.get("errors") == []
        and result.get("contract", {}).get("source") == source
        and result.get("contract", {}).get("sha256") == contract_sha
        and trace_contract.get("sha256") == evidence["trace"].sha256
        and trace_contract.get("captures_all_syscalls") is True
        and trace_contract.get("capture_complete_for_claimed_scope") is True
        and trace_contract.get("missing_explicit_mutation_syscalls") == []
        and trace_contract.get("forbidden_mutation_attempt_count") == 0
        and trace_contract.get("protected_mutation_attempt_count") == 0
        and network_count == 0,
        "authoritative complete zero-network trace:" + kind + ":" + seed,
    )
    cold = (
        cold_facts(analyzer, evidence["trace"].raw or b"", root, seed)
        if kind == "producer" else None
    )
    normalized = normalize_result(result)
    row = {
        "kind": kind,
        "seed": seed,
        "contract": contract,
        "contract_sha256": contract_sha,
        "contract_source": source,
        "result": result,
        "analyzer_result_sha256": common.sha256(common.canonical(result)),
        "normalized_analyzer_result_sha256": common.sha256(common.canonical(normalized)),
        "cold_facts": cold,
        "cold_facts_sha256": (
            None if cold is None else common.sha256(common.canonical(cold))
        ),
        "network_syscalls": network_count,
    }
    return row
