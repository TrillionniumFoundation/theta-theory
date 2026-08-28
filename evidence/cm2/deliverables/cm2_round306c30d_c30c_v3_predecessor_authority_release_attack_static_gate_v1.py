#!/usr/bin/env python3
"""Static/release-attack gate for the append-only C30c-v3 -> C30d interface.

This gate does not execute C30d mathematics and does not validate an extant
publication.  It audits the two read-only implementations as source, applies
in-memory release-policy mutations, and runs only their explicit
missing-terminal negative mode against the not-yet-published versioned chain.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

sys.dont_write_bytecode = True

DELIVERABLES = Path(__file__).resolve().parent
WORKSPACE = DELIVERABLES.parent
PYTHON = Path("/usr/bin/python3")
NEGATIVE_CHAIN_REL = (
    ".cm2-runtime/audit/c30c-publication-v3-chain-v1-20260808T0715Z"
)

PROGRAMS = {
    "adapter": DELIVERABLES
    / "cm2_round306c30d_c30c_v3_predecessor_authority_adapter_v1.py",
    "independent_verifier": DELIVERABLES
    / (
        "cm2_round306c30d_c30c_v3_predecessor_authority_"
        "independent_verifier_v1.py"
    ),
}

PIN_SCHEMA = "cm2.round306c30d.c30c-v3-predecessor-dynamic-pins.v1"
PROJECTION_SCHEMA = "cm2.round306c30d.c30c-v3-predecessor-projection.v1"
PROJECTION_STATUS = (
    "PASS_EXACT_C30C_V3_TERMINAL_GRAPH_AS_C30D_PREDECESSOR__"
    "ZERO_C30D_FORMAL_CREDIT"
)
GATE_SCHEMA = (
    "cm2.round306c30d.c30c-v3-predecessor-authority."
    "release-attack-static-gate.v1"
)
GATE_STATUS = (
    "PASS_APPEND_ONLY_C30C_V3_AUTHORITY_INTERFACE_STATIC_AND_"
    "MISSING_TERMINAL_GATES__ZERO_C30D_CREDIT"
)

CHAIN_MEMBERS = frozenset({
    "c30c_v3_audit_evidence.tar.gz",
    "evidence_bundle_receipt.json",
    "manifest_receipt.json",
    "payload_manifest.sha256",
    "root_manifest.sha256",
    "outer_verification.json",
    "terminal_seal_receipt.json",
    "terminal_replay.json",
    "chain_status.json",
})

APPROVED_STATIC_HASHES = frozenset({
    "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248",
    "e9e72536be9ba707fe2fdf6034b47978be4d09235e5133414ec7b0a31acf4e71",
    "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4",
    "a928d0328e94ca98f04a0ee5d5d45ee0b75ee9ca2292afffe5c117880f0d5f93",
})

REQUIRED_LITERALS = frozenset({
    PIN_SCHEMA,
    PROJECTION_SCHEMA,
    PROJECTION_STATUS,
    "cm2.round306c30c.v3-publication-manifests.v1",
    "PASS_PAYLOAD_AND_ROOT_MANIFESTS__ZERO_FORMAL_CREDIT",
    "cm2.round306c30c.v3-formal-handoff-outer-verification.v1",
    "PASS_INDEPENDENT_OUTER_MATHEMATICAL_CHECK__CONDITIONAL_80_TO_78",
    "cm2.round306c30c.v3-terminal-seal.v1",
    "PASS_CONDITIONAL_TERMINAL_SEAL__ZERO_FORMAL_CREDIT__REPLAY_REQUIRED",
    "cm2.round306c30c.v3-terminal-replay.v1",
    "PASS_TERMINAL_REPLAY__FORMAL_SOURCE_W_80_TO_78",
    "cm2.round306c30c.v3-publication-chain-watch.v1",
    "PASS_C30C_V3_TERMINAL_REPLAY__FORMAL_SOURCE_W_80_TO_78",
    "BLOCKED_FAIL_CLOSED",
    "C30C_V3_TERMINAL_GRAPH_INCOMPLETE:terminal_replay.json",
    "BLOCKED_COMPOSITE",
    "UNAUTHORIZED",
    "NOT_MINTED",
    "10/18",
    "NO-GO_FOR_CLAIM",
    *CHAIN_MEMBERS,
})

REQUIRED_SOURCE_FRAGMENTS = (
    'parser.add_argument("--dynamic-pins", type=Path)',
    '"chain_members"',
    '"pinset_object_sha256"',
    '"mathematical_producer_executed": False',
    '"candidate_created": False',
    '"result_created": False',
    '"manifest_created": False',
    '"seal_created": False',
    '"C30d_transition_authorized": False',
    '.get("C30d_transition_authorized") is False',
    '"source_W_transition_authorized_by_this_projection": False',
    '.get("source_W_transition_authorized_by_this_projection") is False',
)

FORBIDDEN_TEXT = (
    ".startswith(",
    "cm2_round306c30c_sealed",
    (
        "cm2_round306c30c_source_w_full_delta_whole_origin_"
        "disposition_verification.json"
    ),
    "C30C_TERMINAL_REPLAY_SHA256",
    "C30C_TERMINAL_SEAL_SHA256",
    "C30C_ROOT_MANIFEST_SHA256",
    "C30C_PAYLOAD_MANIFEST_SHA256",
    "C30C_OUTER_VERIFICATION_SHA256",
    "C30C_CHAIN_STATUS_SHA256",
    (
        "cm2_round306c30d_source_w_multi_delta_whole_origin_"
        "exclusion_producer.py"
    ),
    "subprocess",
    "importlib",
    "write_bytes(",
    "write_text(",
    "O_WRONLY",
    "O_RDWR",
    "O_CREAT",
    "O_TRUNC",
    "O_APPEND",
)

ALLOWED_IMPORTS = frozenset({
    "__future__",
    "argparse",
    "hashlib",
    "json",
    "os",
    "re",
    "stat",
    "sys",
    "pathlib",
    "typing",
})
FORBIDDEN_CALL_NAMES = frozenset({
    "open",
    "exec",
    "eval",
    "compile",
    "__import__",
    "setattr",
    "delattr",
})
FORBIDDEN_METHODS = frozenset({
    "startswith",
    "write_bytes",
    "write_text",
    "touch",
    "mkdir",
    "makedirs",
    "unlink",
    "remove",
    "rmdir",
    "rename",
    "replace",
    "symlink_to",
    "hardlink_to",
    "chmod",
    "chown",
})

ZERO_C30D_CREDIT = {
    "multi_Delta_cell_dispositions": 0,
    "multi_Delta_whole_cell_exclusions": 0,
    "resolved_source_W_origin_dispositions": 0,
    "whole_source_W_origin_exclusions": 0,
}


class GateFailure(RuntimeError):
    """Fail-closed static or negative-test rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise GateFailure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_source(path: Path) -> bytes:
    absolute = path.resolve(strict=True)
    need(absolute.parent == DELIVERABLES, "source path containment")
    with absolute.open("rb") as handle:
        raw = handle.read()
    need(raw and b"\x00" not in raw, "source regular bytes")
    return raw


def imported_modules(tree: ast.AST) -> set[str]:
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            need(node.module is not None, "relative import forbidden")
            result.add(node.module.split(".", 1)[0])
    return result


def source_policy(raw: bytes, label: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8")
        tree = ast.parse(text, filename=label)
    except (UnicodeDecodeError, SyntaxError) as error:
        raise GateFailure("source parse:" + label) from error

    imports = imported_modules(tree)
    need(imports <= ALLOWED_IMPORTS, "source import allowlist:" + label)
    for marker in FORBIDDEN_TEXT:
        need(marker not in text, "forbidden source marker:" + label + ":" + marker)

    literals = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and type(node.value) is str
    }
    need(REQUIRED_LITERALS <= literals, "required exact literals:" + label)
    for fragment in REQUIRED_SOURCE_FRAGMENTS:
        need(fragment in text, "required source fragment:" + label + ":" + fragment)
    need(
        any(
            "c30c-publication-v3-chain-v[0-9]+-" in literal
            for literal in literals
        ),
        "versioned chain-path grammar:" + label,
    )
    embedded_hashes = {
        value for value in literals if re.fullmatch(r"[0-9a-f]{64}", value)
    }
    need(
        embedded_hashes == APPROVED_STATIC_HASHES,
        "only approved predecessor/candidate static hashes:" + label,
    )

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            need(
                node.func.id not in FORBIDDEN_CALL_NAMES,
                "forbidden direct call:" + label + ":" + node.func.id,
            )
        elif isinstance(node.func, ast.Attribute):
            need(
                node.func.attr not in FORBIDDEN_METHODS,
                "forbidden method:" + label + ":" + node.func.attr,
            )

    return {
        "source_sha256": sha256_bytes(raw),
        "source_size": len(raw),
        "approved_static_hash_count": len(embedded_hashes),
        "dynamic_terminal_hash_count": 0,
        "exact_chain_member_count": len(CHAIN_MEMBERS),
        "read_only_ast_policy": "PASS",
    }


def replaced(text: str, old: str, new: str) -> str:
    need(old in text, "attack fixture anchor missing:" + old)
    return text.replace(old, new)


def mutations(text: str) -> dict[str, str]:
    return {
        "legacy_prefix_acceptance": text + "\n# .startswith(\n",
        "legacy_sealed_alias": text + "\n# cm2_round306c30c_sealed\n",
        "legacy_verification_alias": text
        + "\n# cm2_round306c30c_source_w_full_delta_whole_origin_"
        "disposition_verification.json\n",
        "frozen_future_terminal_hash_symbol": text
        + "\n# C30C_TERMINAL_REPLAY_SHA256\n",
        "terminal_status_downgrade": replaced(
            text,
            "PASS_TERMINAL_REPLAY__FORMAL_SOURCE_W_80_TO_78",
            "PASS_TERMINAL_REPLAY__MUTATED",
        ),
        "outer_status_downgrade": replaced(
            text,
            "PASS_INDEPENDENT_OUTER_MATHEMATICAL_CHECK__CONDITIONAL_80_TO_78",
            "PASS_OUTER__MUTATED",
        ),
        "c30d_math_producer_reference": text
        + "\n# cm2_round306c30d_source_w_multi_delta_whole_origin_"
        "exclusion_producer.py\n",
        "filesystem_write_primitive": text + "\n# write_bytes(\n",
        "c30d_transition_authorization": replaced(
            text,
            '"C30d_transition_authorized": False',
            '"C30d_transition_authorized": True',
        ),
        "projection_transition_authorization": replaced(
            text,
            '"source_W_transition_authorized_by_this_projection": False',
            '"source_W_transition_authorized_by_this_projection": True',
        ),
        "projection_status_relaxation": replaced(
            text,
            "ZERO_C30D_FORMAL_CREDIT",
            "MUTATED_C30D_FORMAL_CREDIT",
        ),
    }


def release_attacks(raw: bytes, label: str) -> dict[str, Any]:
    text = raw.decode("utf-8")
    cases = mutations(text)
    rejected: list[str] = []
    for name, mutant in sorted(cases.items()):
        try:
            source_policy(mutant.encode("utf-8"), label + ":attack:" + name)
        except GateFailure:
            rejected.append(name)
    need(len(rejected) == len(cases), "all release attacks rejected:" + label)
    return {
        "attack_count": len(cases),
        "rejected_count": len(rejected),
        "rejected": rejected,
    }


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "duplicate JSON key:" + label)
            result[key] = value
        return result

    try:
        value = json.loads(
            raw.decode("ascii"),
            object_pairs_hook=pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise GateFailure("negative JSON:" + label) from error
    need(type(value) is dict, "negative object:" + label)
    need(raw == canonical(value) + b"\n", "negative canonical stdout:" + label)
    return value


def negative_terminal_test(path: Path, label: str, chain: Path) -> dict[str, Any]:
    environment = {
        "HOME": "/nonexistent",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "PATH": "/usr/bin:/bin",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    completed = subprocess.run(
        [
            os.fspath(PYTHON),
            "-I",
            "-B",
            os.fspath(path.resolve(strict=True)),
            "--chain-dir",
            os.fspath(chain),
            "--negative-missing-terminal-test",
        ],
        cwd=WORKSPACE,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    need(completed.returncode == 1, "negative numeric exit 1:" + label)
    need(completed.stderr == b"", "negative empty stderr:" + label)
    value = strict_object(completed.stdout, label)
    need(
        value
        == {
            "schema": PROJECTION_SCHEMA,
            "status": "BLOCKED_FAIL_CLOSED",
            "error": "C30C_V3_TERMINAL_GRAPH_INCOMPLETE:terminal_replay.json",
            "formal_credit": ZERO_C30D_CREDIT,
            "source_W_formal_remainder": 78,
            "source_W_transition_authorized_by_this_projection": False,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "negative exact fail-closed receipt:" + label,
    )
    return {
        "returncode": completed.returncode,
        "signal": None,
        "stderr_sha256": sha256_bytes(completed.stderr),
        "stdout_sha256": sha256_bytes(completed.stdout),
        "status": value["status"],
        "error": value["error"],
    }


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def run() -> dict[str, Any]:
    chain = WORKSPACE / NEGATIVE_CHAIN_REL
    need(not (chain / "terminal_replay.json").is_file(), "negative terminal is absent")

    static: dict[str, Any] = {}
    attacks: dict[str, Any] = {}
    negative: dict[str, Any] = {}
    for label, path in PROGRAMS.items():
        raw = read_source(path)
        static[label] = source_policy(raw, label)
        attacks[label] = release_attacks(raw, label)
        negative[label] = negative_terminal_test(path, label, chain)

    python_resolved = PYTHON.resolve(strict=True)
    return {
        "schema": GATE_SCHEMA,
        "status": GATE_STATUS,
        "programs": static,
        "release_attacks": attacks,
        "negative_missing_terminal": {
            "chain_relative_path": NEGATIVE_CHAIN_REL,
            "terminal_present": False,
            "programs": negative,
        },
        "dynamic_pins_interface": {
            "schema": PIN_SCHEMA,
            "exact_chain_members": sorted(CHAIN_MEMBERS),
            "dynamic_pinset_created": False,
            "future_terminal_hash_embedded": False,
        },
        "python": {
            "launch_path": os.fspath(PYTHON),
            "resolved_path": os.fspath(python_resolved),
            "sha256": file_sha256(python_resolved),
        },
        "C30d_mathematical_producer_executed": False,
        "candidate_created": False,
        "result_created": False,
        "manifest_created": False,
        "seal_created": False,
        "run_created": False,
        "formal_credit": ZERO_C30D_CREDIT,
        "source_W_formal_remainder": 78,
        "C30d_transition_authorized": False,
        "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    try:
        result = run()
    except (
        GateFailure,
        OSError,
        ValueError,
        TypeError,
        KeyError,
        subprocess.SubprocessError,
    ) as error:
        print(
            canonical({
                "schema": GATE_SCHEMA,
                "status": "BLOCKED_FAIL_CLOSED",
                "error": str(error),
                "formal_credit": ZERO_C30D_CREDIT,
                "source_W_formal_remainder": 78,
                "C30d_transition_authorized": False,
                "CM2": "NO-GO_FOR_CLAIM",
            }).decode("ascii")
        )
        return 1
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
