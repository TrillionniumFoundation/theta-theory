#!/usr/bin/env python3
"""Build a non-authoritative dual-adapter fixture for C29 contract-v3 tests."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
ADAPTER_SCHEMA = (
    "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion."
    "v2.terminal-consumer-adapter-receipt.v3"
)
C27_SCHEMA = "cm2.round306c27r2.c29-consumer-projection.v1"
C28_SCHEMA = "cm2.round306c28-v2.c29-consumer-projection.v1"
C27_ROOT = "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc"
C27_RECEIPT_FILE = "feccb0b9290bd82ac1d8e78e8e7a21d4f25e0ca3aa3556cc3f0bb6007f61c3dd"
C27_RECEIPT_OBJECT = "8afbd127c9518f569c2f7b3edcdbe9e0ebf77d88bcca855822e58d21e5cfe782"
C27_REPLAY_FILE = "b480df4b8caaf9876a48720f92a8fb6d86e2b1b5966bcc71b0022c5e49fc12ee"
C27_REPLAY_OBJECT = "216d2592c49b0302de0042677ce54c96cd5ad1fcb32231da02b39c003cb837e8"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"), "newline")
    value = json.loads(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1], "canonical")
    body = dict(value)
    claim = body.pop(closure, None)
    need(claim == digest(body), "closure")
    return value


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_closed(path: Path, body: dict[str, Any], closure: str) -> dict[str, Any]:
    value = dict(body)
    value[closure] = digest(value)
    write_once(path, canonical(value) + b"\n")
    return value


def relative(path: Path) -> str:
    absolute = path.absolute()
    need(absolute.is_relative_to(ROOT), "path inside workspace")
    return absolute.relative_to(ROOT).as_posix()


def manifest(entries: list[Path], *, basename: bool = False) -> bytes:
    rows = []
    for path in sorted(entries, key=lambda value: value.name if basename else relative(value)):
        name = path.name if basename else relative(path)
        rows.append(file_sha(path) + "  " + name + "\n")
    return "".join(rows).encode("ascii")


def fake_sha(label: str) -> str:
    return hashlib.sha256(("SYNTHETIC_NON_AUTHORITY:" + label).encode()).hexdigest()


def build_adapter(base: Path, kind: str, members: dict[str, dict[str, Any]],
                  source: dict[str, str], census: dict[str, Any],
                  extra: dict[str, Any]) -> dict[str, str]:
    adapter = base / ("c27r2-adapter" if kind == "C27R2" else "c28-adapter")
    need(not adapter.exists(), "fresh adapter")
    adapter.mkdir(parents=True, mode=0o700)
    pass_bytes = (
        b"PASS_C29_V2_C27R2_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT\n"
        if kind == "C27R2" else
        b"PASS_C29_V2_C28_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT\n"
    )
    write_once(adapter / "PASS.lock", pass_bytes)
    projection_body = {
        "schema": C27_SCHEMA if kind == "C27R2" else C28_SCHEMA,
        "status": ("PASS_C27R2_TERMINAL_AUTHORITY_FOR_C29_CONSUMER"
                   if kind == "C27R2" else
                   "PASS_C28_V2_TERMINAL_AUTHORITY_FOR_C29_CONSUMER"),
        "terminal_replay_passed": True, "authority_minted": True,
        "terminal_root_manifest_sha256": source["root"],
        "terminal_receipt_file_sha256": source["receipt_file"],
        "terminal_receipt_object_sha256": source["receipt_object"],
        "terminal_replay_file_sha256": source["replay_file"],
        "terminal_replay_object_sha256": source["replay_object"],
        "terminal_status": source["status"],
        "PASS_lock_sha256": file_sha(adapter / "PASS.lock"),
        "payload_members": members, "exact_census": census,
        "formal_credit": 0, "C29": "UNAUTHORIZED_SYNTHETIC_FIXTURE",
        **extra,
    }
    projection = write_closed(adapter / "c29_consumer_projection.json",
                              projection_body, "projection_sha256")
    payload_members = [adapter / "c29_consumer_projection.json"]
    payload_members.extend(ROOT / item["path"] for item in members.values())
    write_once(adapter / "payload_manifest.sha256", manifest(payload_members))
    status = ("PASS_C29_V2_C27R2_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT"
              if kind == "C27R2" else
              "PASS_C29_V2_C28_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT")
    receipt_body = {
        "schema": ADAPTER_SCHEMA, "status": status, "authority_kind": kind,
        "terminal_replay_passed": True, "authority_minted": True,
        "source_terminal_root_manifest_sha256": source["root"],
        "source_terminal_receipt_file_sha256": source["receipt_file"],
        "source_terminal_receipt_object_sha256": source["receipt_object"],
        "source_terminal_replay_file_sha256": source["replay_file"],
        "source_terminal_replay_object_sha256": source["replay_object"],
        "source_terminal_status": source["status"],
        "consumer_projection_file_sha256": file_sha(adapter / "c29_consumer_projection.json"),
        "consumer_projection_object_sha256": projection["projection_sha256"],
        "payload_manifest_sha256": file_sha(adapter / "payload_manifest.sha256"),
        "formal_credit": 0, "manifest_authorized": False,
        "synthetic_fixture_only": True, "C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = write_closed(adapter / "terminal_receipt.json", receipt_body,
                           "terminal_receipt_sha256")
    write_once(adapter / "root_manifest.sha256", manifest([
        adapter / "payload_manifest.sha256", adapter / "terminal_receipt.json"],
        basename=True))
    return {"dir": str(adapter), "root": file_sha(adapter / "root_manifest.sha256"),
            "receipt_file": file_sha(adapter / "terminal_receipt.json"),
            "receipt_object": receipt["terminal_receipt_sha256"]}


def execute(args: argparse.Namespace) -> dict[str, Any]:
    out = Path(args.out_dir).absolute()
    need(out.is_relative_to(ROOT) and not out.exists(), "fresh fixture root")
    for raw in (args.c27r2_result, args.c27r2_member, args.c27r2_census):
        path = Path(raw).absolute()
        need(path.is_relative_to(ROOT) and path.is_file() and not path.is_symlink(),
             "source file")
    c27_result_path = Path(args.c27r2_result).absolute()
    c27_result = document(c27_result_path, "result_sha256")
    out.mkdir(parents=True, mode=0o700)
    c28_result_body = {
        "schema": "cm2.round306c28.synthetic-non-authority-result.v1",
        "status": "PASS_SYNTHETIC_C28_RESULT_FOR_C29_CONTRACT_TEST_ONLY",
        "formal_credit": 0, "manifest_authorized": False,
        "C28": "UNAUTHORIZED_SYNTHETIC_FIXTURE", "CM2": "NO-GO_FOR_CLAIM",
    }
    c28_result = write_closed(out / "synthetic_c28_result.json", c28_result_body,
                              "result_sha256")
    c27_members = {
        "producer_result": {"path": relative(c27_result_path),
                            "file_sha256": file_sha(c27_result_path),
                            "object_sha256": c27_result["result_sha256"]},
        "member_to_post_component": {"path": relative(Path(args.c27r2_member)),
                                     "file_sha256": file_sha(Path(args.c27r2_member))},
        "post_component_census": {"path": relative(Path(args.c27r2_census)),
                                  "file_sha256": file_sha(Path(args.c27r2_census))},
    }
    c27_source = {"root": C27_ROOT, "receipt_file": C27_RECEIPT_FILE,
                  "receipt_object": C27_RECEIPT_OBJECT,
                  "replay_file": C27_REPLAY_FILE,
                  "replay_object": C27_REPLAY_OBJECT,
                  "status": "PASS_C27R2_TERMINAL_BYTE_REPLAY__FORMAL_C27R2_AUTHORITY_MINTED"}
    c28_source = {key: fake_sha("C28:" + key) for key in (
        "root", "receipt_file", "receipt_object", "replay_file", "replay_object")}
    c28_source["status"] = (
        "PASS_C28_TERMINAL_BYTE_REPLAY__FORMAL_C28_PAIR_ROUTING_AUTHORITY_MINTED")
    c27 = build_adapter(out, "C27R2", c27_members, c27_source, {
        "members": 502204, "post_C27R2_components": 43684,
        "within_post_component_member_pairs": 542179508,
        "cross_post_component_member_pairs": 125561998198}, {})
    c28 = build_adapter(out, "C28", {
        "producer_result": {"path": relative(out / "synthetic_c28_result.json"),
                            "file_sha256": file_sha(out / "synthetic_c28_result.json"),
                            "object_sha256": c28_result["result_sha256"]}},
        c28_source, {"post_C27R2_components": 43684,
                     "cross_post_component_member_pairs": 125561998198}, {
            "C27R2_terminal_root_manifest_sha256": C27_ROOT,
            "B2_pair_routing_complete": True, "component_maximality_complete": True,
            "new_legal_cross_component_pairs": 0, "unresolved_pairs": 0})
    return {"schema": ADAPTER_SCHEMA + ".synthetic-fixture",
            "status": "PASS_CONSTRUCTIBLE_DUAL_ADAPTER_SYNTHETIC_FIXTURE__NO_AUTHORITY",
            "c27r2": c27, "c28": c28, "formal_credit": 0,
            "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def self_test() -> dict[str, Any]:
    need(fake_sha("a") == fake_sha("a") and fake_sha("a") != fake_sha("b"),
         "fixture digest")
    return {"status": "PASS_SYNTHETIC_FIXTURE_BUILDER_SELF_TEST",
            "formal_credit": 0, "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--c27r2-result")
    parser.add_argument("--c27r2-member")
    parser.add_argument("--c27r2-census")
    parser.add_argument("--out-dir")
    args = parser.parse_args()
    try:
        fields = (args.c27r2_result, args.c27r2_member, args.c27r2_census, args.out_dir)
        if args.self_test:
            need(all(value is None for value in fields), "self-test arguments")
            result = self_test()
        else:
            need(all(type(value) is str for value in fields), "all fixture arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
