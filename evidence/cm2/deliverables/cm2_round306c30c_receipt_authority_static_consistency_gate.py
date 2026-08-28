#!/usr/bin/env python3
"""Static and synthetic-data consistency gate for the C30c receipt bridge.

The gate imports publication helpers without invoking their CLIs.  It neither
reads nor writes the completed attack run or candidate trees.  It proves that
the bundle builder and outer verifier declare the same exact evidence tree,
consume the same receipt/run bytes, and independently derive the same closed
receipt-authority object from a synthetic JSON fixture.  It also checks the
payload/root member contracts and the matching verification-schema fragment.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import stat
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
SOURCES = {
    "builder": ROOT / (PREFIX + "_audit_evidence_bundle_builder.py"),
    "outer": ROOT / (PREFIX + "_formal_handoff_outer_verifier.py"),
    "publication": ROOT / (PREFIX + "_publication_manifest_builder.py"),
    "terminal": ROOT / (PREFIX + "_manifest_first_sealed_verifier.py"),
}
SCHEMA = ROOT / (PREFIX + "_formal_handoff_verification.schema.json")
RECEIPT_SCRIPTS = {
    "cm2_round306c30c_62_attack_run_receipt_validator.py":
        "8692c8a8e57d535ba8f8162bd4f7f51e8acb04f28755384158b45b4eb2629b61",
    "cm2_round306c30c_attack_receipt_evidence_adapter.py":
        "f4dac9c42f3de9d02e97060f14bb42ccdfca98015ed4a760bbca044b50c56590",
    "cm2_round306c30c_attack_receipt_evidence_adapter_independent_verifier.py":
        "43611f53caa199dce8c529151731db025e197d42232736200fd7b73cd67ba153",
}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable_bytes(path: Path, maximum: int = 8 << 20) -> bytes:
    descriptor = os.open(
        path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and 0 < before.st_size <= maximum,
            "bounded regular source:" + path.name,
        )
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    fields = lambda value: (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )
    need(fields(before) == fields(after) and sum(map(len, chunks)) == before.st_size,
         "stable source capture:" + path.name)
    return b"".join(chunks)


def load(name: str, path: Path) -> ModuleType:
    raw = stable_bytes(path)
    spec = importlib.util.spec_from_file_location("_c30c_static_" + name, path)
    need(spec is not None, "module spec:" + name)
    module = ModuleType("_c30c_static_" + name)
    module.__file__ = os.fspath(path)
    module.__package__ = ""
    exec(compile(raw, os.fspath(path), "exec", dont_inherit=True), module.__dict__)
    return module


class RecordingMap(dict[str, bytes]):
    def __init__(self, values: dict[str, bytes]) -> None:
        super().__init__(values)
        self.consumed: set[str] = set()

    def __getitem__(self, key: str) -> bytes:
        self.consumed.add(key)
        return super().__getitem__(key)


def closed(body: dict[str, Any]) -> bytes:
    value = {**body, "payload_sha256": sha256(canonical(body))}
    return canonical(value) + b"\n"


def synthetic_bridge(module: ModuleType) -> tuple[RecordingMap, dict[str, Any]]:
    run_files = tuple(module.ATTACK_RUN_FILES)
    run: dict[str, bytes] = {
        name: ("synthetic:" + name + "\n").encode("ascii") for name in run_files
    }
    run["stdout.json"] = b'{"synthetic_attack_stdout":true}\n'
    run["stderr.log"] = b""
    run["exit_code.txt"] = b"0\n"
    run["time.txt"] = b"synthetic GNU time receipt\n"
    run["pre.sha256"] = run["post.sha256"] = b"a" * 64 + b"  candidate\n"
    run["pre.stat"] = run["post.stat"] = b"candidate synthetic-stat\n"
    run_map = {
        name: {"sha256": sha256(run[name]), "size": len(run[name])}
        for name in run_files
    }
    receipt = {
        "schema": "cm2.round306c30c.attack-run-receipt-validation.v1",
        "status": module.RECEIPT_STATUS,
        "run_directory": module.ATTACK_RUN_NAME,
        "run_start_utc": "2026-08-07T00:00:00Z",
        "run_end_utc": "2026-08-07T01:00:00Z",
        "elapsed": "1:00:00",
        "harness_stdout_sha256": sha256(run["stdout.json"]),
        "harness_sha256": module.HARNESS_SHA256,
        "verifier_sha256": module.VERIFIER_SHA256,
        "python_sha256": module.INTERPRETER_SHA256,
        "baseline_result_sha256": "b" * 64,
        "attack_count": 62,
        "pre_post_sha256_identical": True,
        "pre_post_stat_identical": True,
        "numeric_exit_code": 0,
        "signal": None,
        "formal_credit": 0,
        "manifest_authorized": False,
        "authority": "SYNTHETIC_ZERO_CREDIT_TEST_ONLY",
    }
    watcher = {
        "validator_exit_code": 0,
        "validator_result": receipt,
        "validator_stderr": "",
        "watch_status": "VALIDATOR_COMPLETED",
    }
    watcher_raw = canonical(watcher)
    bindings = {
        "harness_stdout_sha256": sha256(run["stdout.json"]),
        "numeric_exit_sha256": sha256(run["exit_code.txt"]),
        "pre_sha256_ledger_sha256": sha256(run["pre.sha256"]),
        "post_sha256_ledger_sha256": sha256(run["post.sha256"]),
        "pre_stat_ledger_sha256": sha256(run["pre.stat"]),
        "post_stat_ledger_sha256": sha256(run["post.stat"]),
        "pre_post_sha256_identical": True,
        "pre_post_stat_identical": True,
        "numeric_exit_code": 0,
        "signal": None,
    }
    adapter_body = {
        "schema": "cm2.round306c30c.attack-receipt-evidence-adapter.v1",
        "status": module.ADAPTER_STATUS,
        "run_directory": ".cm2-runtime/audit/" + module.ATTACK_RUN_NAME,
        "receipt_file": (
            ".cm2-runtime/audit/" + module.ATTACK_RUN_NAME
            + "-receipt-validation.json"
        ),
        "receipt_file_sha256": sha256(watcher_raw),
        "receipt_result_sha256": sha256(canonical(receipt)),
        "receipt_validator": {
            "path": "deliverables/" + module.RECEIPT_VALIDATOR,
            "sha256": module.RECEIPT_VALIDATOR_SHA256,
            "replay_stdout_sha256": sha256(canonical(receipt) + b"\n"),
        },
        "python_sha256": module.INTERPRETER_SHA256,
        "run_files": run_map,
        "required_bindings": bindings,
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }
    adapter_raw = closed(adapter_body)
    verification = {
        "schema": (
            "cm2.round306c30c.attack-receipt-evidence-adapter-verification.v1"
        ),
        "status": module.ADAPTER_VERIFICATION_STATUS,
        "adapter_sha256": sha256(adapter_raw),
        "receipt_file_sha256": sha256(watcher_raw),
        "receipt_validator_sha256": module.RECEIPT_VALIDATOR_SHA256,
        "harness_stdout_sha256": bindings["harness_stdout_sha256"],
        "pre_post_sha256_identical": True,
        "pre_post_stat_identical": True,
        "numeric_exit_code": 0,
        "signal": None,
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }
    raw = {
        "attacks/validator_receipt.raw": watcher_raw,
        "attacks/receipt_adapter.raw": adapter_raw,
        "attacks/receipt_adapter_verification.raw": canonical(verification) + b"\n",
        "attacks/stdout.raw": run["stdout.json"],
        "attacks/stderr.raw": run["stderr.log"],
        "attacks/time.raw": run["time.txt"],
        "attacks/exit.txt": run["exit_code.txt"],
        **{"attacks/run/" + name: value for name, value in run.items()},
    }
    recording = RecordingMap(raw)
    result = module.validate_attack_receipt_bridge(recording)
    return recording, result


def require_cross_reference_tamper_rejected(
    module: ModuleType, fixture: RecordingMap,
) -> None:
    tampered = dict(fixture)
    verification = json.loads(
        tampered["attacks/receipt_adapter_verification.raw"]
    )
    verification["adapter_sha256"] = "0" * 64
    tampered["attacks/receipt_adapter_verification.raw"] = (
        canonical(verification) + b"\n"
    )
    try:
        module.validate_attack_receipt_bridge(tampered)
    except module.Blocked:
        return
    raise Reject("receipt cross-reference tamper accepted:" + module.__name__)


def unique_required_lists(value: Any, label: str = "$schema") -> None:
    if type(value) is dict:
        required = value.get("required")
        if type(required) is list:
            need(len(required) == len(set(required)), "duplicate required key:" + label)
        for key, child in value.items():
            unique_required_lists(child, label + "/" + key)
    elif type(value) is list:
        for index, child in enumerate(value):
            unique_required_lists(child, label + "/" + str(index))


def outer_body_keys(raw: bytes) -> set[str]:
    try:
        tree = ast.parse(raw, filename=os.fspath(SOURCES["outer"]))
    except SyntaxError as error:
        raise Reject("outer verifier parses") from error
    candidates: list[set[str]] = []
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name) and node.target.id == "body"
            and isinstance(node.value, ast.Dict)
        ):
            continue
        keys: set[str] = set()
        literal = True
        for key in node.value.keys:
            if isinstance(key, ast.Constant) and type(key.value) is str:
                keys.add(key.value)
            else:
                literal = False
        if literal and {"schema", "status", "formal_handoff"} <= keys:
            candidates.append(keys)
    need(len(candidates) == 1, "single literal outer verification body")
    return candidates[0]


def run_gate() -> dict[str, Any]:
    modules = {name: load(name, path) for name, path in SOURCES.items()}
    builder = modules["builder"]
    outer = modules["outer"]
    publication = modules["publication"]
    terminal = modules["terminal"]

    need(tuple(builder.ATTACK_RUN_FILES) == tuple(outer.ATTACK_RUN_FILES),
         "builder/outer exact run-file tuple")
    need(len(set(builder.ATTACK_RUN_FILES)) == 16, "exact 16 unique run artifacts")
    builder_tree = tuple(builder.evidence_files())
    outer_tree = tuple(outer.evidence_files())
    need(builder_tree == outer_tree, "builder/outer exact evidence tree identity")
    receipt_tree = {
        "attacks/validator_receipt.raw", "attacks/receipt_adapter.raw",
        "attacks/receipt_adapter_verification.raw",
        *("attacks/run/" + name for name in builder.ATTACK_RUN_FILES),
    }
    need(receipt_tree <= set(builder_tree) and len(receipt_tree) == 19,
         "exact receipt three plus raw run sixteen in evidence tree")

    builder_recording, builder_authority = synthetic_bridge(builder)
    outer_recording, outer_authority = synthetic_bridge(outer)
    consumed = receipt_tree | {
        "attacks/stdout.raw", "attacks/stderr.raw", "attacks/time.raw",
        "attacks/exit.txt",
    }
    need(builder_recording.consumed == consumed, "builder exact consumed bridge keys")
    need(outer_recording.consumed == consumed, "outer exact consumed bridge keys")
    need(builder_authority == outer_authority,
         "independent builder/outer receipt-authority identity")
    require_cross_reference_tamper_rejected(builder, builder_recording)
    require_cross_reference_tamper_rejected(outer, outer_recording)

    for filename, expected in RECEIPT_SCRIPTS.items():
        need(sha256(stable_bytes(ROOT / filename)) == expected,
             "receipt script hash:" + filename)
    for module_name in ("builder", "outer", "terminal"):
        module = modules[module_name]
        need(module.RECEIPT_VALIDATOR_SHA256 == RECEIPT_SCRIPTS[
            "cm2_round306c30c_62_attack_run_receipt_validator.py"
        ], "validator constant:" + module_name)
        need(module.RECEIPT_ADAPTER_SHA256 == RECEIPT_SCRIPTS[
            "cm2_round306c30c_attack_receipt_evidence_adapter.py"
        ], "adapter constant:" + module_name)
        need(module.RECEIPT_ADAPTER_VERIFIER_SHA256 == RECEIPT_SCRIPTS[
            "cm2_round306c30c_attack_receipt_evidence_adapter_independent_verifier.py"
        ], "adapter verifier constant:" + module_name)

    payload_sets = {
        name: tuple(module.PAYLOAD_MEMBERS)
        for name, module in (
            ("outer", outer), ("publication", publication), ("terminal", terminal)
        )
    }
    need(len(set(payload_sets.values())) == 1,
         "outer/publication/terminal exact payload member identity")
    payload = set(payload_sets["outer"])
    need(set(RECEIPT_SCRIPTS) <= payload, "payload pins all receipt scripts")
    need(tuple(publication.ROOT_MEMBERS) == tuple(terminal.ROOT_MEMBERS),
         "publication/terminal exact root member identity")

    schema = json.loads(stable_bytes(SCHEMA))
    need(type(schema) is dict, "schema object")
    unique_required_lists(schema)
    need("attack_receipt_authority" in schema.get("required", []),
         "schema requires receipt authority")
    body_keys = outer_body_keys(stable_bytes(SOURCES["outer"]))
    schema_keys = set(schema.get("required", []))
    need(
        schema.get("additionalProperties") is False
        and set(schema.get("properties", {})) == schema_keys
        and body_keys | {"verification_object_sha256"} == schema_keys,
        "outer body/schema exact top-level key identity",
    )
    receipt_schema = schema.get("properties", {}).get("attack_receipt_authority")
    need(type(receipt_schema) is dict, "schema receipt authority object")
    try:
        import jsonschema
    except ImportError as error:
        raise Reject("jsonschema unavailable") from error
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
        authority_schema = {
            "$schema": schema["$schema"], "$defs": schema["$defs"],
            **receipt_schema,
        }
        jsonschema.Draft202012Validator(authority_schema).validate(builder_authority)
    except (jsonschema.exceptions.SchemaError,
            jsonschema.exceptions.ValidationError) as error:
        raise Reject("receipt authority schema validation") from error

    return {
        "schema": "cm2.round306c30c.receipt-authority-static-consistency.v1",
        "status": "PASS_EXACT_TREE_CONSUMED_KEYS_AND_SYNTHETIC_RECEIPT_BINDING",
        "evidence_member_count": len(builder_tree),
        "receipt_tree_member_count": len(receipt_tree),
        "raw_run_file_count": len(builder.ATTACK_RUN_FILES),
        "consumed_bridge_key_count": len(consumed),
        "payload_member_count": len(payload),
        "root_member_count": len(publication.ROOT_MEMBERS),
        "verification_top_level_key_count": len(schema_keys),
        "cross_reference_tamper_rejections": 2,
        "receipt_authority_sha256": sha256(canonical(builder_authority)),
        "source_sha256": {
            name: sha256(stable_bytes(path)) for name, path in SOURCES.items()
        },
        "schema_sha256": sha256(stable_bytes(SCHEMA)),
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }


def main() -> int:
    try:
        output = run_gate()
    except (Reject, OSError, KeyError, TypeError, ValueError) as error:
        print(canonical({
            "schema": "cm2.round306c30c.receipt-authority-static-consistency.v1",
            "status": "BLOCKED_FAIL_CLOSED", "error": str(error),
            "formal_credit": 0, "source_W_transition_authorized": False,
        }).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
