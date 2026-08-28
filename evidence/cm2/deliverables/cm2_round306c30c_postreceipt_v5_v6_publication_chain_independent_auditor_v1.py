#!/usr/bin/env python3
"""Independent terminal auditor for the v5/v6 C30c publication chain."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tarfile
from pathlib import Path
from typing import Any

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
AUDIT = WORKSPACE / ".cm2-runtime/audit"
ADAPTER_PROGRAM = WORKSPACE / "deliverables/cm2_round306c30c_postreceipt_v5_v6_joint_attestation_consumer_adapter_v1.py"
WATCHER = WORKSPACE / "deliverables/cm2_round306c30c_postreceipt_v5_v6_publication_chain_watch_v2.py"
FILES = frozenset({"PUBLICATION_PASS.lock", "adapter_verification.json",
                   "c30c_v5_v6_joint_publication_evidence.tar.gz", "chain_status.json",
                   "evidence_index.json", "outer_verification.json", "payload_manifest.sha256",
                   "root_manifest.sha256", "terminal_replay.json"})
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def strict(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("ascii"))
    need(type(value) is dict and raw == canonical(value) + b"\n", "canonical:" + path.name)
    body = dict(value); observed = body.pop("object_sha256", None)
    need(type(observed) is str and HEX64.fullmatch(observed) is not None
         and hashlib.sha256(canonical(body)).hexdigest() == observed,
         "object closure:" + path.name)
    return value


def sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def manifest(path: Path) -> dict[str, str]:
    output: dict[str, str] = {}
    for row in path.read_text("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", row)
        need(match is not None and match.group(2) not in output, "manifest row:" + path.name)
        output[match.group(2)] = match.group(1)
    return output


def unit_fields(unit: str) -> dict[str, str]:
    names = ("Id", "InvocationID", "MainPID", "ExecMainPID", "ActiveState", "SubState",
             "Result", "ExecMainCode", "ExecMainStatus", "ExecStart")
    command = ["/usr/bin/systemctl", "--user", "show", unit]
    for name in names:
        command.extend(("-p", name))
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "clean systemctl")
    fields = dict(row.split("=", 1) for row in result.stdout.decode("ascii").splitlines() if "=" in row)
    need(set(fields) == set(names), "exact unit fields")
    return fields


def adapter_verify(adapter: Path) -> dict[str, Any]:
    environment = {"HOME": os.environ.get("HOME", "/home/qian-qi"), "LC_ALL": "C.UTF-8",
                   "TZ": "UTC", "PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1",
                   "XDG_RUNTIME_DIR": os.environ.get("XDG_RUNTIME_DIR", "/run/user/1000")}
    if "DBUS_SESSION_BUS_ADDRESS" in os.environ:
        environment["DBUS_SESSION_BUS_ADDRESS"] = os.environ["DBUS_SESSION_BUS_ADDRESS"]
    result = subprocess.run(["/usr/bin/python3", "-I", "-B", os.fspath(ADAPTER_PROGRAM),
                             "--verify", "--adapter-dir", os.fspath(adapter)],
                            cwd=WORKSPACE, env=environment, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "live adapter replay")
    value = json.loads(result.stdout.decode("ascii"))
    need(value.get("status") == "PASS_ADAPTER_LIVE_REPLAY_AND_ALL_BINDINGS", "adapter PASS")
    return value


def audit(chain: Path, adapter: Path, unit: str, invocation: str,
          watcher_sha256: str) -> dict[str, Any]:
    need(chain.parent == AUDIT and adapter.parent == AUDIT
         and {path.name for path in chain.iterdir()} == FILES, "exact chain inventory")
    need(sha(WATCHER) == watcher_sha256, "watcher source pin")
    fields = unit_fields(unit)
    need(fields.get("Id") == unit and fields.get("InvocationID") == invocation
         and fields.get("MainPID") == "0" and int(fields.get("ExecMainPID", "0")) > 1
         and fields.get("ActiveState") == "active" and fields.get("SubState") == "exited"
         and fields.get("Result") == "success" and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and watcher_sha256 in fields.get("ExecStart", "")
         and os.fspath(WATCHER) in fields.get("ExecStart", ""), "exact held-source unit success")
    adapter_result = adapter_verify(adapter)
    verification = strict(chain / "adapter_verification.json")
    outer = strict(chain / "outer_verification.json")
    evidence = strict(chain / "evidence_index.json")
    terminal = strict(chain / "terminal_replay.json")
    status = strict(chain / "chain_status.json")
    payload = manifest(chain / "payload_manifest.sha256")
    need(payload == {name: sha(chain / name) for name in (
             "adapter_verification.json", "outer_verification.json",
             "c30c_v5_v6_joint_publication_evidence.tar.gz", "evidence_index.json")},
         "payload manifest replay")
    need(manifest(chain / "root_manifest.sha256") == {
             "payload_manifest.sha256": sha(chain / "payload_manifest.sha256")},
         "root manifest replay")
    entries = evidence.get("entries")
    need(type(entries) is list and evidence.get("entry_count") == len(entries)
         and evidence.get("bundle_sha256") ==
             sha(chain / "c30c_v5_v6_joint_publication_evidence.tar.gz"), "evidence index")
    expected = {row["name"]: row["sha256"] for row in entries}
    observed: dict[str, str] = {}
    with tarfile.open(chain / "c30c_v5_v6_joint_publication_evidence.tar.gz", "r:gz") as archive:
        for member in archive:
            need(member.isfile() and member.name not in observed, "regular unique tar entry")
            stream = archive.extractfile(member)
            need(stream is not None, "tar stream")
            observed[member.name] = hashlib.sha256(stream.read()).hexdigest()
    need(observed == expected, "full tar/index byte replay")
    need(outer.get("status") ==
         "PASS_JOINT_ADAPTER_AND_AUDITED_DUAL_MATHEMATICS__CONDITIONAL_80_TO_78"
         and outer.get("source_W_transition_authorized") is False
         and terminal.get("status") == "PASS_TERMINAL_REPLAY__FORMAL_SOURCE_W_80_TO_78"
         and terminal.get("source_W_transition") == {"before": 80, "after": 78}
         and terminal.get("source_W_transition_authorized") is True
         and terminal.get("source_W_formal_remainder") == 78
         and status.get("status") ==
             "PASS_C30C_V5_V6_JOINT_PUBLICATION__FORMAL_SOURCE_W_80_TO_78"
         and status.get("terminal_replay_object_sha256") == terminal.get("object_sha256")
         and status.get("source_W_transition_authorized") is True
         and status.get("source_W_formal_remainder") == 78
         and terminal.get("CM2") == status.get("CM2") == "NO-GO_FOR_CLAIM",
         "terminal publication conclusion")
    need((chain / "PUBLICATION_PASS.lock").read_bytes() ==
         b"PASS_C30C_V5_V6_JOINT_PUBLICATION__SOURCE_W_80_TO_78__CM2_NO_GO\n",
         "exact publication marker")
    body = {"schema": "cm2.round306c30c.v5-v6-publication-independent-audit.v1",
            "status": "PASS_FULL_TAR_MANIFEST_OBJECT_UNIT_AND_LIVE_ADAPTER_REPLAY",
            "chain_name": chain.name, "unit": unit, "InvocationID": invocation,
            "ExecMainPID": int(fields["ExecMainPID"]), "watcher_sha256": watcher_sha256,
            "adapter_verification_object_sha256": adapter_result["object_sha256"],
            "chain_status_object_sha256": status["object_sha256"],
            "terminal_replay_object_sha256": terminal["object_sha256"],
            "evidence_entry_count": len(observed), "bundle_sha256": evidence["bundle_sha256"],
            "source_W_formal_remainder": 78, "source_W_transition_authorized": True,
            "CM2": "NO-GO_FOR_CLAIM"}
    body["object_sha256"] = hashlib.sha256(canonical(body)).hexdigest()
    return body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chain-dir", required=True, type=Path)
    parser.add_argument("--adapter-dir", required=True, type=Path)
    parser.add_argument("--unit", required=True)
    parser.add_argument("--invocation-id", required=True)
    parser.add_argument("--watcher-sha256", required=True)
    args = parser.parse_args()
    try:
        result = audit(args.chain_dir.resolve(strict=True), args.adapter_dir.resolve(strict=True),
                       args.unit, args.invocation_id, args.watcher_sha256)
    except (Blocked, OSError, ValueError, TypeError, KeyError, json.JSONDecodeError,
            subprocess.SubprocessError, tarfile.TarError) as error:
        print(canonical({"schema": "cm2.round306c30c.v5-v6-publication-independent-audit.v1",
                         "status": "BLOCKED_FAIL_CLOSED", "error": str(error),
                         "source_W_transition_authorized": False,
                         "CM2": "NO-GO_FOR_CLAIM"}).decode("ascii"))
        return 2
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
