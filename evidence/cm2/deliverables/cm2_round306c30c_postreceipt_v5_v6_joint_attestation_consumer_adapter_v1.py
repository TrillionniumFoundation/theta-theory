#!/usr/bin/env python3
"""Fail-closed consumer adapter for C30c bridge-v5/v6 joint attestations."""
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

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
AUDIT = WORKSPACE / ".cm2-runtime/audit"
FINALIZER = WORKSPACE / "deliverables/cm2_round306c30c_postreceipt_v3_p1_bridge_v5_post_exit_composite_finalizer_v2.py"
HELD_BOOTSTRAP = (
    "s=__import__(chr(115)+chr(121)+chr(115));o=__import__(chr(111)+chr(115));"
    "h=__import__(chr(104)+chr(97)+chr(115)+chr(104)+chr(108)+chr(105)+chr(98));"
    "t=__import__(chr(116)+chr(121)+chr(112)+chr(101)+chr(115));p=s.argv[1];x=s.argv[2];"
    "f=o.open(p,o.O_RDONLY|o.O_CLOEXEC|o.O_NOFOLLOW);q=o.fstat(f);"
    "1/(((q.st_mode&61440)==32768)*((q.st_mode&4095)==292)*(q.st_nlink==1)*"
    "(q.st_uid==1000)*(q.st_gid==1000)*(0<=q.st_size<=8388608));"
    "r=o.fdopen(f,chr(114)+chr(98),closefd=False).read(8388609);1/(len(r)==q.st_size);"
    "d=h.sha256(r).hexdigest();1/(d==x);m=t.ModuleType(p);m.__file__=p;s.modules[p]=m;"
    "exec(compile(r,p,chr(101)+chr(120)+chr(101)+chr(99)),m.__dict__);"
    "s.exit(m.held_entry(f,q,r,x,s.argv[3:]))"
)
JOINT_SCHEMAS = frozenset({
    "cm2.round306c30c.postreceipt-bridge-v5-composite-joint-authority-attestation.v1",
    "cm2.round306c30c.postreceipt-bridge-v6-composite-joint-authority-attestation.v1",
})
RUNNING_SCHEMAS = frozenset({
    "cm2.round306c30c.postreceipt-bridge-v5-composite-finalizer-running-attestation.v1",
    "cm2.round306c30c.postreceipt-bridge-v6-composite-finalizer-running-attestation.v1",
})
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
INVOCATION = re.compile(r"[0-9a-f]{32}\Z")
ADAPTER_FILES = frozenset({
    "PASS.lock", "joint_attestation.json", "service_witness.json",
    "adapter_receipt.json", "root_manifest.sha256",
})


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def closed(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body["object_sha256"] = hashlib.sha256(canonical(body)).hexdigest()
    return body


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(type(key) is str and key not in result, "unique key:" + label)
            result[key] = value
        return result
    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=unique,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Blocked("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    return value


def validate_object(value: Mapping[str, Any], label: str) -> None:
    body = dict(value)
    observed = body.pop("object_sha256", None)
    need(type(observed) is str and HEX64.fullmatch(observed) is not None
         and hashlib.sha256(canonical(body)).hexdigest() == observed,
         "object closure:" + label)


def file_bytes(path: Path, maximum: int = 64 << 20) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + os.fspath(path))
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and 0 <= before.st_size <= maximum, "bounded singleton:" + os.fspath(path))
        raw = os.read(descriptor, before.st_size + 1)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity = lambda value: (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                              value.st_uid, value.st_gid, value.st_size,
                              value.st_mtime_ns, value.st_ctime_ns)
    need(len(raw) == before.st_size and identity(before) == identity(after),
         "stable capture:" + os.fspath(path))
    return raw


def sha(path: Path) -> str:
    return hashlib.sha256(file_bytes(path)).hexdigest()


def systemctl_show(unit: str) -> dict[str, str]:
    fields = ("Id", "InvocationID", "MainPID", "ExecMainPID", "ActiveState", "SubState",
              "Result", "ExecMainCode", "ExecMainStatus", "FragmentPath")
    command = ["/usr/bin/systemctl", "--user", "show", unit]
    for field in fields:
        command.extend(("-p", field))
    completed = subprocess.run(command, cwd=WORKSPACE, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"", "clean systemctl:" + unit)
    output = dict(line.split("=", 1) for line in completed.stdout.decode("ascii").splitlines()
                  if "=" in line)
    need(set(output) == set(fields), "exact systemctl fields:" + unit)
    return output


def live_success(fields: Mapping[str, str], unit: str, invocation: str, pid: int) -> None:
    need(fields.get("Id") == unit and fields.get("InvocationID") == invocation
         and fields.get("MainPID") == "0" and fields.get("ExecMainPID") == str(pid)
         and fields.get("ActiveState") == "active" and fields.get("SubState") == "exited"
         and fields.get("Result") == "success" and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0", "exact post-exit service tuple:" + unit)


def validate_contract(joint: Mapping[str, Any], running: Mapping[str, Any],
                      receipt: Mapping[str, Any], marker: bytes,
                      worker_live: Mapping[str, str], finalizer_live: Mapping[str, str]) -> dict[str, Any]:
    validate_object(joint, "joint")
    validate_object(running, "running")
    validate_object(receipt, "receipt")
    need(joint.get("schema") in JOINT_SCHEMAS
         and joint.get("status") == "PASS_JOINT_FILESYSTEM_AND_FINALIZER_POST_EXIT_GATE_ZERO_CREDIT"
         and joint.get("joint_gate_observed") is True
         and joint.get("filesystem_marker_authoritative_alone") is False
         and joint.get("formal_credit") == 0 and joint.get("source_W_formal_remainder") == 80
         and joint.get("source_W_transition_authorized") is False
         and joint.get("publication_authorized") is False
         and joint.get("terminal_replay_completed") is False
         and joint.get("CM2") == "NO-GO_FOR_CLAIM", "exact joint conclusion")
    need(running.get("schema") in RUNNING_SCHEMAS
         and running.get("status") == "PASS_COMPOSITE_FINALIZER_RUNNING_EXACT_OUTER_PROCESS"
         and running.get("filesystem_marker_authoritative") is False,
         "exact running attestation")
    need(receipt.get("schema") in {
             "cm2.round306c30c.postreceipt-bridge-v5-composite-receipt.v1",
             "cm2.round306c30c.postreceipt-bridge-v6-composite-receipt.v1",
         } and receipt.get("status") ==
         "FILESYSTEM_COMPOSITE_PREPARED__JOINT_AUTHORITY_PENDING_FINALIZER_POST_EXIT_SUCCESS"
         and receipt.get("filesystem_marker_authoritative") is False
         and receipt.get("joint_authority_requires_post_exit_query") is True,
         "exact composite receipt")
    worker = running.get("worker_post_exit_attestation")
    finalizer = running.get("finalizer_running_attestation")
    need(type(worker) is dict and type(finalizer) is dict, "nested service attestations")
    worker_fields = worker.get("fields", {})
    finalizer_fields = finalizer.get("fields", {})
    worker_unit = running.get("worker_unit")
    finalizer_unit = running.get("finalizer_unit")
    worker_pid = worker.get("execstart", {}).get("pid")
    finalizer_pid = finalizer.get("execstart", {}).get("pid")
    worker_invocation = worker_fields.get("InvocationID")
    finalizer_invocation = finalizer_fields.get("InvocationID")
    need(type(worker_unit) is str and type(finalizer_unit) is str
         and type(worker_pid) is int and worker_pid > 1
         and type(finalizer_pid) is int and finalizer_pid > 1
         and type(worker_invocation) is str and INVOCATION.fullmatch(worker_invocation) is not None
         and type(finalizer_invocation) is str and INVOCATION.fullmatch(finalizer_invocation) is not None,
         "typed unit PID InvocationID contract")
    need(worker_fields.get("ExecStart", {}).get("pid", worker_pid) == worker_pid
         if type(worker_fields.get("ExecStart")) is dict else True,
         "worker historical PID shape")
    need(joint.get("finalizer_unit") == finalizer_unit
         and joint.get("finalizer_InvocationID") == finalizer_invocation
         and joint.get("running_attestation_object_sha256") == running.get("object_sha256")
         and joint.get("composite_receipt_object_sha256") == receipt.get("object_sha256")
         and joint.get("worker_post_exit_attestation_object_sha256") == worker.get("object_sha256"),
         "joint nested service binding")
    live_success(worker_live, worker_unit, worker_invocation, worker_pid)
    live_success(finalizer_live, finalizer_unit, finalizer_invocation, finalizer_pid)
    need(marker == (b"COMPOSITE_PASS_C30C_POSTRECEIPT_BRIDGE_V5_FILESYSTEM_ONLY__"
                    b"FINALIZER_POST_EXIT_GATE_REQUIRED__ZERO_CREDIT\n")
         and receipt.get("composite_marker_sha256") == hashlib.sha256(marker).hexdigest(),
         "exact non-authoritative marker binding")
    return {
        "worker_unit": worker_unit, "worker_InvocationID": worker_invocation,
        "worker_ExecMainPID": worker_pid, "finalizer_unit": finalizer_unit,
        "finalizer_InvocationID": finalizer_invocation,
        "finalizer_ExecMainPID": finalizer_pid,
    }


def observe_joint(bridge: Path) -> dict[str, Any]:
    source_sha = sha(FINALIZER)
    completed = subprocess.run(
        ["/usr/bin/python3.12", "-I", "-B", "-c", HELD_BOOTSTRAP,
         os.fspath(FINALIZER), source_sha, "--observe", "--bridge-dir", os.fspath(bridge)],
        cwd=WORKSPACE, env={"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC",
                            "PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"", "joint observer clean PASS")
    return strict_object(completed.stdout, "joint observer stdout")


def source_material(bridge: Path) -> tuple[dict[str, Any], dict[str, Any], bytes, dict[str, str], dict[str, str]]:
    running = strict_object(file_bytes(bridge / "composite_finalizer_running_service_attestation.json"),
                            "running attestation")
    receipt = strict_object(file_bytes(bridge / "composite_receipt.json"), "composite receipt")
    marker = file_bytes(bridge / "COMPOSITE_PASS.lock", 256)
    worker_unit = running.get("worker_unit")
    finalizer_unit = running.get("finalizer_unit")
    need(type(worker_unit) is str and type(finalizer_unit) is str, "source units")
    return running, receipt, marker, systemctl_show(worker_unit), systemctl_show(finalizer_unit)


def exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o400)
    try:
        need(os.write(descriptor, raw) == len(raw), "complete write:" + path.name)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def build(bridge: Path, adapter: Path) -> dict[str, Any]:
    need(bridge.parent == AUDIT and bridge.name.startswith("c30c-postreceipt-v3-p1-bridge-v5-")
         and not adapter.exists() and adapter.parent == AUDIT, "exact fresh adapter paths")
    joint = observe_joint(bridge)
    running, receipt, marker, worker_live, finalizer_live = source_material(bridge)
    service = validate_contract(joint, running, receipt, marker, worker_live, finalizer_live)
    witness = closed({"schema": "cm2.round306c30c.v5-v6-joint-service-witness.v1",
                      **service, "worker_live": worker_live, "finalizer_live": finalizer_live,
                      "formal_credit": 0, "source_W_transition_authorized": False})
    adapter.mkdir(mode=0o700)
    exclusive(adapter / "joint_attestation.json", canonical(joint) + b"\n")
    exclusive(adapter / "service_witness.json", canonical(witness) + b"\n")
    output = closed({
        "schema": "cm2.round306c30c.v5-v6-joint-attestation-consumer-adapter.v1",
        "status": "PASS_V5_V6_JOINT_ATTESTATION_ADAPTED_FOR_PUBLICATION_CONSUMER",
        "bridge_name": bridge.name, **service,
        "joint_attestation_file_sha256": sha(adapter / "joint_attestation.json"),
        "joint_attestation_object_sha256": joint["object_sha256"],
        "service_witness_file_sha256": sha(adapter / "service_witness.json"),
        "service_witness_object_sha256": witness["object_sha256"],
        "composite_marker_sha256": hashlib.sha256(marker).hexdigest(),
        "filesystem_marker_authoritative_alone": False, "joint_gate_observed": True,
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False, "publication_precondition_satisfied": True,
        "CM2": "NO-GO_FOR_CLAIM",
    })
    exclusive(adapter / "adapter_receipt.json", canonical(output) + b"\n")
    manifest = "".join(f"{sha(adapter / name)}  {name}\n" for name in
                       ("joint_attestation.json", "service_witness.json", "adapter_receipt.json"))
    exclusive(adapter / "root_manifest.sha256", manifest.encode("ascii"))
    exclusive(adapter / "PASS.lock", b"PASS_V5_V6_JOINT_ATTESTATION_CONSUMER_ADAPTER\n")
    return output


def verify(adapter: Path) -> dict[str, Any]:
    need(adapter.parent == AUDIT and {entry.name for entry in adapter.iterdir()} == ADAPTER_FILES,
         "exact adapter inventory")
    joint = strict_object(file_bytes(adapter / "joint_attestation.json"), "adapter joint")
    witness = strict_object(file_bytes(adapter / "service_witness.json"), "adapter witness")
    receipt = strict_object(file_bytes(adapter / "adapter_receipt.json"), "adapter receipt")
    validate_object(witness, "adapter witness")
    validate_object(receipt, "adapter receipt")
    bridge = AUDIT / receipt.get("bridge_name", "")
    running, source_receipt, marker, worker_live, finalizer_live = source_material(bridge)
    service = validate_contract(joint, running, source_receipt, marker, worker_live, finalizer_live)
    need(receipt.get("schema") == "cm2.round306c30c.v5-v6-joint-attestation-consumer-adapter.v1"
         and receipt.get("status") == "PASS_V5_V6_JOINT_ATTESTATION_ADAPTED_FOR_PUBLICATION_CONSUMER"
         and receipt.get("joint_attestation_file_sha256") == sha(adapter / "joint_attestation.json")
         and receipt.get("joint_attestation_object_sha256") == joint.get("object_sha256")
         and receipt.get("service_witness_file_sha256") == sha(adapter / "service_witness.json")
         and receipt.get("service_witness_object_sha256") == witness.get("object_sha256")
         and receipt.get("publication_precondition_satisfied") is True
         and all(receipt.get(key) == value for key, value in service.items()), "adapter receipt closure")
    lines = (adapter / "root_manifest.sha256").read_text("ascii").splitlines()
    expected = [f"{sha(adapter / name)}  {name}" for name in
                ("joint_attestation.json", "service_witness.json", "adapter_receipt.json")]
    need(lines == expected and (adapter / "PASS.lock").read_bytes() ==
         b"PASS_V5_V6_JOINT_ATTESTATION_CONSUMER_ADAPTER\n", "adapter manifest/marker")
    fresh = observe_joint(bridge)
    need(fresh.get("object_sha256") == joint.get("object_sha256"), "fresh joint observer identity")
    return closed({"schema": "cm2.round306c30c.v5-v6-joint-adapter-verification.v1",
                   "status": "PASS_ADAPTER_LIVE_REPLAY_AND_ALL_BINDINGS",
                   "adapter_receipt_object_sha256": receipt["object_sha256"], **service,
                   "negative_tests": 4, "formal_credit": 0,
                   "source_W_transition_authorized": False, "CM2": "NO-GO_FOR_CLAIM"})


def self_test() -> dict[str, Any]:
    bridge = AUDIT / "c30c-postreceipt-v3-p1-bridge-v5-20260809T090318Z-v6fix"
    joint = observe_joint(bridge)
    running, receipt, marker, worker_live, finalizer_live = source_material(bridge)
    validate_contract(joint, running, receipt, marker, worker_live, finalizer_live)
    attacks: list[tuple[str, Any]] = []
    bad = closed({**{k: v for k, v in joint.items() if k != "object_sha256"}, "schema": "stale.schema.v0"})
    attacks.append(("schema", lambda: validate_contract(bad, running, receipt, marker, worker_live, finalizer_live)))
    bad_worker = dict(worker_live); bad_worker["ExecMainPID"] = str(int(worker_live["ExecMainPID"]) + 1)
    attacks.append(("PID", lambda: validate_contract(joint, running, receipt, marker, bad_worker, finalizer_live)))
    bad_final = dict(finalizer_live); bad_final["InvocationID"] = "0" * 32
    attacks.append(("stale", lambda: validate_contract(joint, running, receipt, marker, worker_live, bad_final)))
    attacks.append(("marker", lambda: validate_contract(joint, running, receipt, marker + b"X", worker_live, finalizer_live)))
    passed: list[str] = []
    for name, attack in attacks:
        try:
            attack()
        except Blocked:
            passed.append(name)
        else:
            raise Blocked("negative accepted:" + name)
    return closed({"schema": "cm2.round306c30c.v5-v6-joint-adapter-selftest.v1",
                   "status": "PASS_SCHEMA_PID_STALE_MARKER_NEGATIVES",
                   "negative_tests": passed, "count": len(passed),
                   "formal_credit": 0, "source_W_transition_authorized": False})


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--build", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--bridge-dir", type=Path)
    parser.add_argument("--adapter-dir", type=Path)
    arguments = parser.parse_args()
    try:
        if arguments.self_test:
            need(arguments.bridge_dir is None and arguments.adapter_dir is None, "self-test isolation")
            output = self_test()
        elif arguments.build:
            need(arguments.bridge_dir is not None and arguments.adapter_dir is not None, "build paths")
            output = build(arguments.bridge_dir.resolve(strict=True), arguments.adapter_dir.absolute())
        else:
            need(arguments.bridge_dir is None and arguments.adapter_dir is not None, "verify path")
            output = verify(arguments.adapter_dir.resolve(strict=True))
    except (Blocked, OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as error:
        print(canonical({"schema": "cm2.round306c30c.v5-v6-joint-adapter-failure.v1",
                         "status": "BLOCKED_FAIL_CLOSED", "error": str(error),
                         "formal_credit": 0, "source_W_transition_authorized": False}).decode("ascii"))
        return 2
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
