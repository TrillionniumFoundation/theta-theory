#!/usr/bin/env python3
"""Independent post-terminal auditor for the C29-v2 release chain."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
AUDIT = ROOT / ".cm2-runtime/audit"
PREFIX = "cm2_round306c29_source_g_post_c27r2_member_rebound_fibre_exhaustion_v2"
WATCHER = ROOT / f"deliverables/{PREFIX}_release_chain_watcher_v4.py"
PROGRAMS = {
    "cold": ROOT / f"deliverables/{PREFIX}_release_cold_replay_runner_v4.py",
    "evidence": ROOT / f"deliverables/{PREFIX}_release_evidence_bundle_builder_v1.py",
    "release_attacks": ROOT / f"deliverables/{PREFIX}_release_only_attack_harness_v1.py",
    "manifests": ROOT / f"deliverables/{PREFIX}_release_manifest_builder_v1.py",
    "outer": ROOT / f"deliverables/{PREFIX}_release_outer_verifier_v1.py",
    "seal": ROOT / f"deliverables/{PREFIX}_release_terminal_seal_builder_v1.py",
    "terminal": ROOT / f"deliverables/{PREFIX}_terminal_byte_replay_v1.py",
}
PINS = {
    "cold": "715601a73c4e9957cc3681313e8c11bffd22c3937e93b2a5b9ef8c9f924de27f",
    "evidence": "766c217ac0aee04d81493a6ff4ab019702a856bc24dc1d585225535a60d4f28c",
    "release_attacks": "5409cf898395aa3c81da588fe309e9d4aaa534889ea23944b29846e7c2e20e15",
    "manifests": "143b0962dd1dd1b6c00653c18f855e5431307736cc27da5ba5f42896255fa0d7",
    "outer": "41f7dcd8a352bd82e200472d8263c62fc7738b7ce72b727e31394ba7eb223829",
    "seal": "9d47ab01af382c11c8e157546772119f1f5b479807e6e6def472fc56c939f61e",
    "terminal": "d77c2b2e2b80cf879c791e8f3dcfa95964096c9ba1f7c752dd4d3a46596e184f",
}
BASE = "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
TERMINAL_STATUS = "PASS_C29_V2_TERMINAL_BYTE_REPLAY__FORMAL_SOURCE_G_FIBRE_AUTHORITY_MINTED"
STAGE_STATUS = {
    "cold": "PASS_C29_V2_FRESH_NO_IMPORT_COLD_BYTE_REPLAY_WITH_ALL_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT",
    "evidence": "PASS_C29_V2_DUAL_PREDECESSOR_CORE_COLD_PROCESS_AND_BYTE_EVIDENCE_FROZEN__ZERO_CREDIT",
    "release_attacks": "PASS_C29_V2_40_OF_40_DUAL_PREDECESSOR_RELEASE_ONLY_ATTACKS_REJECTED__ZERO_CREDIT",
    "manifests": "PASS_C29_V2_MANIFEST_FIRST_PAYLOAD_AND_DUAL_PREDECESSOR_ROOT_CLOSURE__ZERO_CREDIT_PENDING_OUTER_TERMINAL",
    "outer": "PASS_INDEPENDENT_C29_V2_FULL_LEDGER_DUAL_PREDECESSOR_MANIFEST_COLD_AND_40_RELEASE_ATTACK_CHECK__CONDITIONAL_ZERO_CREDIT",
    "seal": "PASS_CONDITIONAL_C29_V2_TERMINAL_SEAL_CANDIDATE__ZERO_CREDIT_PENDING_INDEPENDENT_BYTE_REPLAY",
    "terminal": TERMINAL_STATUS,
}
CLOSURES = {
    "cold": "cold_replay_receipt_sha256",
    "evidence": "evidence_bundle_sha256",
    "release_attacks": "release_attacks_sha256",
    "manifests": "manifest_receipt_sha256",
    "outer": "outer_verification_sha256",
    "seal": "seal_candidate_sha256",
}
TERMINAL_FILES = frozenset({
    "PASS.lock", "chain_status.json", "payload_manifest.sha256",
    "root_manifest.sha256", "terminal_receipt.json", "terminal_replay.json",
})
PASS_TERMINAL = b"PASS_C29_V2_SOURCE_G_FIBRE_AUTHORITY_TERMINAL_BYTE_REPLAY__SOURCE_W_UNCHANGED_CM2_NO_GO\n"
PASS_WATCH = b"PASS_C29_V2_RELEASE_CHAIN_TERMINAL_MINTED__SOURCE_W_UNCHANGED_CM2_NO_GO\n"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
INVOCATION = re.compile(r"[0-9a-f]{32}\Z")
EXACT_CENSUS = {
    "component_key_incidences": 60296,
    "component_key_multiplicity_census": {"1": 27108, "2": 16556, "3": 8, "4": 8, "5": 4},
    "cross_post_component_member_pairs": 125561998198,
    "family_member_census": {
        "G2A": 5264, "G2B": 10128, "NON_GRAPH": 55604,
        "PRESERVED": 126468, "R2": 295336, "R292": 9404,
    },
    "members": 502204,
    "official_keys": 124,
    "post_C27R2_components": 43684,
    "representations": 549616,
    "total_unordered_member_pairs": 126104177706,
    "within_post_component_member_pairs": 542179508,
}


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def stable_bytes(path: Path, maximum: int = 1 << 30) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + os.fspath(path))
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and 0 <= before.st_size <= maximum, "regular singleton:" + os.fspath(path))
        output = bytearray()
        while len(output) <= before.st_size:
            block = os.read(descriptor, min(4 << 20, before.st_size + 1 - len(output)))
            if not block:
                break
            output.extend(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity = lambda value: (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                              value.st_uid, value.st_gid, value.st_size,
                              value.st_mtime_ns, value.st_ctime_ns)
    need(len(output) == before.st_size and identity(before) == identity(after),
         "stable read:" + os.fspath(path))
    return bytes(output)


def sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def strict(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(type(key) is str and key not in output, "unique JSON:" + label)
            output[key] = value
        return output

    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=unique,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Blocked("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    return value


def document(path: Path, field: str, label: str) -> dict[str, Any]:
    value = strict(stable_bytes(path, 64 << 20), label)
    body = dict(value)
    observed = body.pop(field, None)
    need(type(observed) is str and HEX64.fullmatch(observed) is not None
         and digest(body) == observed, "object closure:" + label)
    return value


def manifest(path: Path, label: str) -> dict[str, str]:
    raw = stable_bytes(path, 64 << 20)
    output: dict[str, str] = {}
    for row in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_./-]+)", row)
        need(match is not None and match.group(2) not in output, "manifest row:" + label)
        relative = Path(match.group(2))
        need(not relative.is_absolute() and ".." not in relative.parts,
             "manifest relative path:" + label)
        output[match.group(2)] = match.group(1)
    need(bool(output) and raw.endswith(b"\n"), "manifest termination:" + label)
    return output


def replay_manifest(path: Path, label: str) -> int:
    rows = manifest(path, label)
    for relative, expected in rows.items():
        member = (ROOT / relative).resolve(strict=True)
        need(member.is_relative_to(ROOT) and sha(member) == expected,
             "manifest member:" + relative)
    return len(rows)


def unit_fields(unit: str) -> dict[str, str]:
    names = ("Id", "InvocationID", "MainPID", "ExecMainPID", "ActiveState", "SubState",
             "Result", "ExecMainCode", "ExecMainStatus", "ExecStart")
    command = ["/usr/bin/systemctl", "--user", "show", unit]
    for name in names:
        command.extend(("-p", name))
    completed = subprocess.run(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"", "systemctl")
    fields = dict(row.split("=", 1) for row in completed.stdout.decode("ascii").splitlines()
                  if "=" in row)
    need(set(fields) == set(names), "systemctl fields")
    return fields


def targets(stem: str) -> dict[str, Path]:
    need(re.fullmatch(r"c29-v2-release-[a-z0-9][a-z0-9-]{7,100}", stem) is not None,
         "release stem")
    return {
        "control": AUDIT / (stem + "-control"),
        "cold_control": AUDIT / (stem + "-cold-control"),
        "cold_run": AUDIT / (stem + "-cold-run"),
        "evidence": AUDIT / (stem + "-evidence"),
        "release_attacks": AUDIT / (stem + "-release-attacks.json"),
        "manifests": AUDIT / (stem + "-manifests"),
        "outer": AUDIT / (stem + "-outer.json"),
        "seal": AUDIT / (stem + "-seal"),
        "terminal": AUDIT / (stem + "-terminal"),
    }


def audit(stem: str, unit: str, invocation: str, watcher_sha256: str) -> dict[str, Any]:
    paths = targets(stem)
    need(type(unit) is str and unit == "cm2-" + stem + ".service"
         and INVOCATION.fullmatch(invocation) is not None
         and HEX64.fullmatch(watcher_sha256) is not None
         and sha(WATCHER) == watcher_sha256, "watcher and identity pins")
    need(all(sha(PROGRAMS[name]) == PINS[name] for name in PROGRAMS), "release source pins")
    fields = unit_fields(unit)
    need(fields.get("Id") == unit and fields.get("InvocationID") == invocation
         and fields.get("MainPID") == "0" and int(fields.get("ExecMainPID", "0")) > 1
         and fields.get("ActiveState") == "active" and fields.get("SubState") == "exited"
         and fields.get("Result") == "success" and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and watcher_sha256 in fields.get("ExecStart", "")
         and os.fspath(WATCHER) in fields.get("ExecStart", ""), "release unit success")
    stage_paths = {
        "cold": paths["cold_control"] / "cold_replay_receipt.json",
        "evidence": paths["evidence"] / "evidence_bundle.json",
        "release_attacks": paths["release_attacks"],
        "manifests": paths["manifests"] / "manifest_receipt.json",
        "outer": paths["outer"],
        "seal": paths["seal"] / "seal_candidate.json",
    }
    stages = {name: document(path, CLOSURES[name], name)
              for name, path in stage_paths.items()}
    for name, value in stages.items():
        need(value.get("status") == STAGE_STATUS[name] and value.get("formal_credit") == 0
             and value.get("manifest_authorized") is False
             and value.get("CM2") == "NO-GO_FOR_CLAIM", "stage boundary:" + name)
    attacks = stages["release_attacks"].get("attacks")
    need(type(attacks) is list and len(attacks) == 40
         and all(type(row) is dict and row.get("outcome") == "REJECTED" for row in attacks)
         and stages["release_attacks"].get("authoritative_inputs_mutated") is False,
         "40 release attacks")
    need(stages["cold"].get("formal_verification_byte_identical") is True
         and stages["cold"].get("all_core_inputs_pre_post_sha_stat_identical") is True
         and stages["cold"].get("numeric_exit_code") == 0
         and stages["cold"].get("stderr_empty") is True
         and stages["outer"].get("all_three_ledgers_independently_replayed") is True
         and stages["outer"].get("cold_replay_byte_identical") is True
         and stages["outer"].get("release_attacks_rejected") == 40
         and stages["outer"].get("core_attacks_rejected") == 34
         and stages["outer"].get("exact_census") == EXACT_CENSUS,
         "cold and outer conclusions")
    control = paths["control"]
    for name in STAGE_STATUS:
        need(stable_bytes(control / (name + ".exit_code.txt"), 16) == b"0\n"
             and stable_bytes(control / (name + ".stderr.log"), 1 << 20) == b"",
             "clean child logs:" + name)
        stdout = strict(stable_bytes(control / (name + ".stdout.log"), 1 << 20),
                        "stdout:" + name)
        need(stdout == {"CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
                        "status": STAGE_STATUS[name]}, "stage stdout:" + name)
    terminal_dir = paths["terminal"]
    need({entry.name for entry in terminal_dir.iterdir()} == TERMINAL_FILES,
         "terminal inventory")
    terminal_receipt = document(terminal_dir / "terminal_receipt.json",
                                "terminal_receipt_sha256", "terminal receipt")
    terminal_replay = document(terminal_dir / "terminal_replay.json",
                               "terminal_replay_sha256", "terminal replay")
    chain_status = document(terminal_dir / "chain_status.json", "chain_status_sha256",
                            "chain status")
    watch = document(control / "watch_receipt.json", "watch_receipt_sha256", "watch")
    need(terminal_receipt.get("status") == terminal_replay.get("status")
         == chain_status.get("status") == watch.get("status") == TERMINAL_STATUS
         and terminal_receipt.get("authority_minted") is True
         and terminal_replay.get("authority_minted") is True
         and chain_status.get("authority_minted") is True
         and watch.get("authority_minted") is True
         and terminal_receipt.get("manifest_authorized") is True
         and terminal_replay.get("manifest_authorized") is True
         and chain_status.get("manifest_authorized") is True
         and watch.get("manifest_authorized") is True
         and terminal_receipt.get("exact_census") == EXACT_CENSUS
         and terminal_receipt.get("terminal_replay_completed") is True
         and terminal_replay.get("terminal_receipt_byte_replay_identical") is True
         and terminal_receipt.get("C29") == terminal_replay.get("C29")
         == chain_status.get("C29") == watch.get("C29")
         == "AUTHORIZED_TERMINAL_SOURCE_G_POST_C27R2_FIBRE_AUTHORITY"
         and terminal_receipt.get("CM2") == terminal_replay.get("CM2")
         == chain_status.get("CM2") == watch.get("CM2") == "NO-GO_FOR_CLAIM",
         "terminal authority")
    need(chain_status.get("terminal_receipt_file_sha256") == sha(terminal_dir / "terminal_receipt.json")
         and chain_status.get("terminal_receipt_object_sha256")
             == terminal_receipt["terminal_receipt_sha256"]
         and chain_status.get("terminal_replay_file_sha256") == sha(terminal_dir / "terminal_replay.json")
         and chain_status.get("terminal_replay_object_sha256")
             == terminal_replay["terminal_replay_sha256"]
         and watch.get("terminal_receipt_object_sha256")
             == terminal_receipt["terminal_receipt_sha256"]
         and watch.get("terminal_replay_object_sha256")
             == terminal_replay["terminal_replay_sha256"]
         and watch.get("release_unit_name") == unit
         and watch.get("release_invocation_id") == invocation,
         "terminal/watch bindings")
    need(stable_bytes(terminal_dir / "PASS.lock", 256) == PASS_TERMINAL
         and stable_bytes(control / "PASS.lock", 256) == PASS_WATCH
         and not (control / "FAILED.lock").exists(), "terminal markers")
    manifest_paths = [
        paths["evidence"] / "evidence_inventory.sha256",
        paths["manifests"] / "payload_manifest.sha256",
        paths["manifests"] / "root_manifest.sha256",
        paths["seal"] / "seal_payload_manifest.sha256",
        paths["seal"] / "seal_root_manifest.sha256",
        terminal_dir / "payload_manifest.sha256",
        terminal_dir / "root_manifest.sha256",
    ]
    replayed = sum(replay_manifest(path, path.name) for path in manifest_paths)
    need(terminal_receipt.get("terminal_payload_manifest_sha256")
         == sha(terminal_dir / "payload_manifest.sha256")
         and terminal_receipt.get("terminal_root_manifest_sha256")
         == sha(terminal_dir / "root_manifest.sha256")
         and terminal_replay.get("terminal_payload_manifest_sha256")
         == sha(terminal_dir / "payload_manifest.sha256")
         and terminal_replay.get("terminal_root_manifest_sha256")
         == sha(terminal_dir / "root_manifest.sha256"), "terminal manifests")
    body = {
        "schema": BASE + "release-chain-independent-audit.v1",
        "status": "PASS_C29_V2_RELEASE_UNIT_STAGES_40_ATTACKS_MANIFESTS_AND_TERMINAL_REPLAY",
        "release_stem": stem,
        "release_unit": unit,
        "release_InvocationID": invocation,
        "release_ExecMainPID": int(fields["ExecMainPID"]),
        "watcher_sha256": watcher_sha256,
        "watch_receipt_object_sha256": watch["watch_receipt_sha256"],
        "terminal_receipt_object_sha256": terminal_receipt["terminal_receipt_sha256"],
        "terminal_replay_object_sha256": terminal_replay["terminal_replay_sha256"],
        "chain_status_object_sha256": chain_status["chain_status_sha256"],
        "release_attacks_rejected": 40,
        "core_attacks_rejected": 34,
        "manifest_rows_replayed": replayed,
        "exact_census": EXACT_CENSUS,
        "authority_minted": True,
        "manifest_authorized": True,
        "Source_W": "UNCHANGED",
        "C29": "AUTHORIZED_TERMINAL_SOURCE_G_POST_C27R2_FIBRE_AUTHORITY",
        "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    body["object_sha256"] = digest(body)
    return body


def self_test() -> dict[str, Any]:
    body = {"schema": "fixture", "status": "PASS"}
    value = dict(body)
    value["object_sha256"] = digest(value)
    observed = dict(value)
    claim = observed.pop("object_sha256")
    need(claim == digest(observed) and len(STAGE_STATUS) == 7
         and set(STAGE_STATUS) == set(PROGRAMS), "auditor fixtures")
    return {
        "schema": BASE + "release-chain-independent-auditor-self-test.v1",
        "status": "PASS_C29_V2_RELEASE_AUDITOR_STATIC_FIXTURES",
        "formal_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--stem")
    parser.add_argument("--unit")
    parser.add_argument("--invocation-id")
    parser.add_argument("--watcher-sha256")
    args = parser.parse_args()
    try:
        fields = (args.stem, args.unit, args.invocation_id, args.watcher_sha256)
        if args.self_test:
            need(all(value is None for value in fields), "self-test isolation")
            result = self_test()
        else:
            need(all(type(value) is str for value in fields), "audit arguments")
            result = audit(args.stem, args.unit, args.invocation_id, args.watcher_sha256)
    except (Blocked, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError) as error:
        result = {
            "schema": BASE + "release-chain-independent-audit.v1",
            "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error),
            "authority_minted": False,
            "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 2
    sys.stdout.buffer.write(canonical(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
