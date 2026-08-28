#!/usr/bin/env python3
"""Coherent fail-closed attacks for the append-only C28-v2 math core.

The harness first requires a clean no-import verifier baseline, then runs
candidate reclosure, inventory, link, source-pin, and terminal-pin attacks in
private copies.  It does not supply release-only TOCTOU/cold/manifest/outer/
terminal coverage; those remain mandatory downstream.  PASS is zero-credit.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
BLOCK_FILE = "member_home_block_census.jsonl.gz"
ROUTE_FILE = "cross_component_pair_route_shard.jsonl.gz"
RESULT_FILE = "result.json"
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_C27R2_TERMINAL_PARTITION_AND_32896_PAIR_SHARDS_"
    "INDEPENDENTLY_REBUILT__ZERO_CREDIT_PENDING_ATTACKS_AND_RELEASE_CHAIN"
)
HARNESS_SCHEMA = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
    "coherent-attack-harness.v1"
)
HARNESS_STATUS = (
    "PASS_BASELINE_AND_26_OF_26_COHERENT_ATTACKS_REJECTED_FAIL_CLOSED__"
    "ZERO_CREDIT_PENDING_RELEASE_CHAIN"
)


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def is_hash(value: Any) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def strict_json(payload: bytes, closure: str | None = None) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            need(key not in output, "duplicate JSON key:" + key)
            output[key] = value
        return output

    def constant(value: str) -> None:
        raise Failure("non-finite JSON:" + value)

    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "JSON one newline")
    value = json.loads(
        payload[:-1], object_pairs_hook=pairs, parse_constant=constant
    )
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON")
    if closure is not None:
        body = dict(value)
        claim = body.pop(closure, None)
        need(is_hash(claim) and claim == digest(body), "JSON closure")
    return value


def local(raw: str | Path, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    value = (ROOT / supplied if not supplied.is_absolute() else supplied).absolute()
    try:
        relative = value.relative_to(ROOT)
    except ValueError as error:
        raise Failure("path outside workspace:" + str(raw)) from error
    need(all(part not in {"", ".", ".."} for part in relative.parts),
         "canonical workspace path:" + str(raw))
    cursor = ROOT
    for part in relative.parts:
        cursor = cursor / part
        if not cursor.exists():
            need(absent is True, "missing path component:" + str(cursor))
            break
        need(not cursor.is_symlink(), "symlink path component:" + str(cursor))
    return value


def regular_single(path: Path, label: str) -> None:
    info = path.stat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1
         and not path.is_symlink(), label + ":regular single-link")


def flip(value: str) -> str:
    need(is_hash(value), "flip SHA")
    return ("0" if value[0] != "0" else "1") + value[1:]


def close_result(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("result_sha256", None)
    result = dict(body)
    result["result_sha256"] = digest(body)
    return result


def clone_candidate(source: Path, target: Path) -> None:
    target.mkdir(mode=0o700)
    for name in (BLOCK_FILE, ROUTE_FILE, RESULT_FILE):
        source_path = source / name
        target_path = target / name
        with source_path.open("rb") as input_stream:
            descriptor = os.open(
                target_path,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL
                | getattr(os, "O_NOFOLLOW", 0),
                0o600,
            )
            try:
                while block := input_stream.read(4 << 20):
                    offset = 0
                    while offset < len(block):
                        offset += os.write(descriptor, block[offset:])
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
        regular_single(target_path, "private clone:" + name)


def rewrite_result(candidate: Path, mutate: Callable[[dict[str, Any]], None]) -> None:
    path = candidate / RESULT_FILE
    value = strict_json(path.read_bytes(), "result_sha256")
    mutate(value)
    path.write_bytes(canonical(close_result(value)) + b"\n")


def ledger_rows(path: Path) -> list[dict[str, Any]]:
    with gzip.GzipFile(fileobj=io.BytesIO(path.read_bytes()), mode="rb") as source:
        lines = source.readlines()
    output: list[dict[str, Any]] = []
    for ordinal, line in enumerate(lines):
        need(line.endswith(b"\n"), f"ledger newline:{ordinal}")
        value = json.loads(line[:-1])
        need(type(value) is dict and canonical(value) == line[:-1],
             f"ledger canonical:{ordinal}")
        output.append(value)
    return output


def write_ledger(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(
            filename="", mode="wb", compresslevel=9, fileobj=raw, mtime=0
        ) as output:
            for row in rows:
                body = dict(row)
                body.pop("row_sha256", None)
                closed = dict(body)
                closed["row_sha256"] = digest(body)
                output.write(canonical(closed) + b"\n")


def reclose_ledger_descriptor(candidate: Path, role: str, filename: str) -> None:
    path = candidate / filename
    rows = ledger_rows(path)
    state = hashlib.sha256()
    for row in rows:
        state.update(row["row_sha256"].encode("ascii") + b"\n")
    value = strict_json((candidate / RESULT_FILE).read_bytes(), "result_sha256")
    descriptor = value["ledgers"][role]
    descriptor["sha256"] = file_hash(path)
    descriptor["size"] = path.stat().st_size
    descriptor["row_count"] = len(rows)
    descriptor["row_sequence_sha256"] = state.hexdigest()
    (candidate / RESULT_FILE).write_bytes(
        canonical(close_result(value)) + b"\n"
    )


def mutate_ledger_row(
    candidate: Path, filename: str, index: int,
    mutate: Callable[[dict[str, Any]], None], role: str,
) -> None:
    path = candidate / filename
    rows = ledger_rows(path)
    need(0 <= index < len(rows), "ledger mutation index")
    mutate(rows[index])
    write_ledger(path, rows)
    reclose_ledger_descriptor(candidate, role, filename)


def verifier_command(
    args: argparse.Namespace, candidate: Path, out_file: Path,
    overrides: dict[str, str] | None = None,
) -> list[str]:
    values = {
        "contract": args.expect_authority_contract_sha256,
        "terminal_root": args.expect_terminal_root_sha256,
        "terminal_file": args.expect_terminal_receipt_file_sha256,
        "terminal_object": args.expect_terminal_receipt_object_sha256,
        "producer": args.expect_producer_sha256,
        "verifier": args.expect_verifier_sha256,
    }
    if overrides is not None:
        values.update(overrides)
    return [
        str(local(args.python)), "-I", "-B", str(local(args.verifier)),
        "--c27r2-terminal-dir", args.c27r2_terminal_dir,
        "--authority-contract", args.authority_contract,
        "--expect-authority-contract-sha256", values["contract"],
        "--expect-terminal-root-sha256", values["terminal_root"],
        "--expect-terminal-receipt-file-sha256", values["terminal_file"],
        "--expect-terminal-receipt-object-sha256", values["terminal_object"],
        "--producer", args.producer,
        "--expect-producer-sha256", values["producer"],
        "--expect-verifier-sha256", values["verifier"],
        "--candidate-dir", str(candidate), "--out-file", str(out_file),
    ]


def run_verifier(
    args: argparse.Namespace, candidate: Path, out_file: Path,
    overrides: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        verifier_command(args, candidate, out_file, overrides),
        cwd=ROOT,
        env={
            "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
            "PYTHONHASHSEED": "30662802",
        },
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )


def main_run(args: argparse.Namespace) -> dict[str, Any]:
    candidate = local(args.candidate_dir)
    work = local(args.work_dir, absent=True)
    out_file = local(args.result_file, absent=True)
    producer = local(args.producer)
    verifier = local(args.verifier)
    python = local(args.python)
    need(candidate.is_dir() and set(path.name for path in candidate.iterdir())
         == {BLOCK_FILE, ROUTE_FILE, RESULT_FILE},
         "baseline candidate exact file set")
    for path, expected, label in (
        (producer, args.expect_producer_sha256, "producer"),
        (verifier, args.expect_verifier_sha256, "verifier"),
        (SELF, args.expect_harness_sha256, "harness"),
        (python, args.expect_python_sha256, "python"),
    ):
        regular_single(path, label)
        need(file_hash(path) == expected, label + ":external SHA pin")
    need(not work.exists() and not out_file.exists()
         and out_file.parent.is_dir() and out_file.parent != candidate
         and candidate not in work.parents,
         "fresh work/result paths outside candidate")
    work.mkdir(parents=True, mode=0o700)

    baseline_out = work / "baseline_verification.json"
    baseline_run = run_verifier(args, candidate, baseline_out)
    expected_stdout = canonical({
        "status": VERIFICATION_STATUS, "formal_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }) + b"\n"
    need(baseline_run.returncode == 0 and baseline_run.stderr == b""
         and baseline_run.stdout == expected_stdout
         and baseline_out.is_file(), "clean verifier baseline")
    baseline_verification = strict_json(
        baseline_out.read_bytes(), "verification_sha256"
    )
    baseline_result = strict_json(
        (candidate / RESULT_FILE).read_bytes(), "result_sha256"
    )

    attacks: list[tuple[
        str, Callable[[Path], None], dict[str, str] | None
    ]] = []

    def result_attack(
        name: str, mutate: Callable[[dict[str, Any]], None]
    ) -> None:
        attacks.append((name, lambda path: rewrite_result(path, mutate), None))

    result_attack("result-status-formal-lie",
                  lambda value: value.__setitem__("status", "PASS_FORMAL_C28"))
    result_attack("result-formal-credit-one",
                  lambda value: value.__setitem__("formal_credit", 1))
    result_attack("result-manifest-authorized",
                  lambda value: value.__setitem__("manifest_authorized", True))
    result_attack("result-C28-authorized",
                  lambda value: value.__setitem__("C28", "AUTHORIZED"))
    result_attack("result-component-count",
                  lambda value: value["post_C27R2_partition_census"].__setitem__(
                      "components", 43_683))
    result_attack("result-cross-denominator",
                  lambda value: value["pair_route_census"].__setitem__(
                      "cross_post_component_pairs_routed", 125_561_998_197))

    def theorem_lie(value: dict[str, Any]) -> None:
        value["maximality_candidate_theorem"]["kind"] = (
            "OLD_C27_FRONTIER_THEOREM"
        )
        value["maximality_candidate_theorem_sha256"] = digest(
            value["maximality_candidate_theorem"]
        )

    result_attack("result-theorem-kind-coherent-reclosure", theorem_lie)
    result_attack("result-old-C15-read-lie",
                  lambda value: value["derivation_closures"].__setitem__(
                      "old_C15_partition_authority_read", True))
    result_attack("result-extra-key",
                  lambda value: value.__setitem__("formal_C28", True))
    result_attack("result-ledger-descriptor-hash",
                  lambda value: value["ledgers"][
                      "cross_component_pair_route_shard"].__setitem__(
                          "sha256", flip(value["ledgers"][
                              "cross_component_pair_route_shard"]["sha256"])))

    attacks.append((
        "block-member-count-coherent-reclosure",
        lambda path: mutate_ledger_row(
            path, BLOCK_FILE, 0,
            lambda row: row.__setitem__("member_count", row["member_count"] + 1),
            "member_home_block_census",
        ), None,
    ))
    attacks.append((
        "block-authority-coherent-reclosure",
        lambda path: mutate_ledger_row(
            path, BLOCK_FILE, 1,
            lambda row: row["partition_authority"].__setitem__(
                "c27r2_terminal_receipt_object_sha256",
                flip(row["partition_authority"]
                    ["c27r2_terminal_receipt_object_sha256"])),
            "member_home_block_census",
        ), None,
    ))
    attacks.append((
        "route-cross-count-coherent-reclosure",
        lambda path: mutate_ledger_row(
            path, ROUTE_FILE, 0,
            lambda row: row.__setitem__(
                "cross_post_component_member_pairs_routed",
                row["cross_post_component_member_pairs_routed"] + 1,
            ), "cross_component_pair_route_shard",
        ), None,
    ))
    attacks.append((
        "route-classification-coherent-reclosure",
        lambda path: mutate_ledger_row(
            path, ROUTE_FILE, 1,
            lambda row: row["pair_classification"].__setitem__(
                "UNRESOLVED", 1),
            "cross_component_pair_route_shard",
        ), None,
    ))

    def truncate_route(path: Path) -> None:
        target = path / ROUTE_FILE
        payload = target.read_bytes()
        target.write_bytes(payload[:-17])

    attacks.append(("route-gzip-truncation", truncate_route, None))
    attacks.append((
        "candidate-extra-file",
        lambda path: (path / "UNAUTHORIZED.txt").write_text(
            "not allowed\n", encoding="ascii"), None,
    ))
    attacks.append((
        "candidate-missing-file",
        lambda path: (path / BLOCK_FILE).unlink(), None,
    ))

    def symlink_route(path: Path) -> None:
        target = path / ROUTE_FILE
        target.unlink()
        os.symlink(candidate / ROUTE_FILE, target)

    def hardlink_route(path: Path) -> None:
        target = path / ROUTE_FILE
        private_source = path.parent / "hardlink-source-route.jsonl.gz"
        shutil.copyfile(target, private_source)
        regular_single(private_source, "hardlink private source")
        target.unlink()
        os.link(private_source, target)

    attacks.append(("candidate-symlink-member", symlink_route, None))
    attacks.append(("candidate-hardlink-member", hardlink_route, None))

    def duplicate_result(path: Path) -> None:
        (path / RESULT_FILE).write_bytes(b'{"schema":"x","schema":"y"}\n')

    attacks.append(("result-duplicate-JSON-key", duplicate_result, None))
    attacks.append(("wrong-authority-contract-pin", lambda path: None, {
        "contract": flip(args.expect_authority_contract_sha256),
    }))
    attacks.append(("wrong-terminal-root-pin", lambda path: None, {
        "terminal_root": flip(args.expect_terminal_root_sha256),
    }))
    attacks.append(("wrong-terminal-receipt-file-pin", lambda path: None, {
        "terminal_file": flip(args.expect_terminal_receipt_file_sha256),
    }))
    attacks.append(("wrong-terminal-receipt-object-pin", lambda path: None, {
        "terminal_object": flip(args.expect_terminal_receipt_object_sha256),
    }))
    attacks.append(("wrong-producer-source-pin", lambda path: None, {
        "producer": flip(args.expect_producer_sha256),
    }))
    attacks.append(("wrong-verifier-source-pin", lambda path: None, {
        "verifier": flip(args.expect_verifier_sha256),
    }))
    need(len(attacks) == 26 and len({name for name, _, _ in attacks}) == 26,
         "exact attack inventory")

    rejected: list[dict[str, Any]] = []
    for ordinal, (name, mutate, overrides) in enumerate(attacks):
        attack_root = work / f"attack-{ordinal:02d}-{name}"
        attack_root.mkdir(mode=0o700)
        private = attack_root / "candidate"
        clone_candidate(candidate, private)
        mutate(private)
        verification_out = attack_root / "verification.json"
        run = run_verifier(args, private, verification_out, overrides)
        need(run.returncode == 2 and run.stdout == b""
             and run.stderr.startswith(b"REJECT:")
             and run.stderr.endswith(b"\n")
             and not verification_out.exists(),
             "attack rejected fail closed:" + name)
        rejected.append({
            "ordinal": ordinal, "name": name,
            "exit_code": run.returncode,
            "stderr_sha256": hashlib.sha256(run.stderr).hexdigest(),
            "verification_output_created": False,
        })

    body = {
        "schema": HARNESS_SCHEMA, "status": HARNESS_STATUS,
        "source_pins": {
            "producer_sha256": args.expect_producer_sha256,
            "verifier_sha256": args.expect_verifier_sha256,
            "harness_sha256": args.expect_harness_sha256,
            "python_sha256": args.expect_python_sha256,
        },
        "authority_pins": {
            "adapter_contract_sha256":
                args.expect_authority_contract_sha256,
            "terminal_root_sha256": args.expect_terminal_root_sha256,
            "terminal_receipt_file_sha256":
                args.expect_terminal_receipt_file_sha256,
            "terminal_receipt_object_sha256":
                args.expect_terminal_receipt_object_sha256,
        },
        "baseline": {
            "candidate_result_sha256": baseline_result["result_sha256"],
            "verification_sha256":
                baseline_verification["verification_sha256"],
            "numeric_exit_code": 0, "stderr_empty": True,
        },
        "attack_census": {
            "planned": 26, "executed": len(rejected),
            "rejected_fail_closed": len(rejected), "accepted": 0,
        },
        "rejected_attacks": rejected,
        "coverage": {
            "candidate_semantic_reclosure": True,
            "gzip_and_inventory_corruption": True,
            "symlink_and_hardlink_rejection": True,
            "source_pin_substitution": True,
            "external_terminal_pin_substitution": True,
            "release_TOCTOU_process_dual_seed_manifest_outer_cold_terminal":
                "MANDATORY_BUT_NOT_EXECUTED_BY_MATH_CORE_HARNESS",
        },
        "formal_credit": 0, "manifest_authorized": False,
        "C28": "UNAUTHORIZED_PENDING_RELEASE_CHAIN",
        "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["attack_receipt_sha256"] = digest(result)
    descriptor = os.open(
        out_file,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        payload = canonical(result) + b"\n"
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    regular_single(out_file, "attack receipt")
    return result


def self_test() -> dict[str, Any]:
    body = {"schema": HARNESS_SCHEMA, "formal_credit": 0}
    closed = {**body, "attack_receipt_sha256": digest(body)}
    need(closed["attack_receipt_sha256"] == digest(body),
         "fixture closure")
    with tempfile.TemporaryDirectory(prefix="cm2-c28-v2-attacks-") as raw:
        source = Path(raw) / "source"
        target = Path(raw) / "target"
        source.mkdir()
        for name in (BLOCK_FILE, ROUTE_FILE, RESULT_FILE):
            (source / name).write_bytes(name.encode("ascii"))
        clone_candidate(source, target)
        need(all((target / name).read_bytes() == name.encode("ascii")
                 for name in (BLOCK_FILE, ROUTE_FILE, RESULT_FILE)),
             "fixture private clone")
    return {
        "schema": HARNESS_SCHEMA + ".self-test",
        "status": "PASS_SMALL_FIXTURE_CLOSURE_AND_PRIVATE_CLONE_TESTS",
        "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM",
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--c27r2-terminal-dir")
    value.add_argument("--authority-contract")
    value.add_argument("--expect-authority-contract-sha256")
    value.add_argument("--expect-terminal-root-sha256")
    value.add_argument("--expect-terminal-receipt-file-sha256")
    value.add_argument("--expect-terminal-receipt-object-sha256")
    value.add_argument("--producer")
    value.add_argument("--verifier")
    value.add_argument("--python")
    value.add_argument("--expect-producer-sha256")
    value.add_argument("--expect-verifier-sha256")
    value.add_argument("--expect-harness-sha256")
    value.add_argument("--expect-python-sha256")
    value.add_argument("--candidate-dir")
    value.add_argument("--work-dir")
    value.add_argument("--result-file")
    return value


def main() -> int:
    args = parser().parse_args()
    names = (
        "c27r2_terminal_dir", "authority_contract",
        "expect_authority_contract_sha256", "expect_terminal_root_sha256",
        "expect_terminal_receipt_file_sha256",
        "expect_terminal_receipt_object_sha256", "producer", "verifier",
        "python", "expect_producer_sha256", "expect_verifier_sha256",
        "expect_harness_sha256", "expect_python_sha256", "candidate_dir",
        "work_dir", "result_file",
    )
    try:
        if args.self_test:
            need(all(getattr(args, name) is None for name in names),
                 "self-test accepts no external arguments")
            result = self_test()
        else:
            need(all(getattr(args, name) is not None for name in names),
                 "all authority/source/candidate/work/result arguments required")
            result = main_run(args)
        sys.stdout.buffer.write(canonical({
            "status": result["status"], "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }) + b"\n")
        return 0
    except (
        Failure, OSError, ValueError, KeyError, TypeError,
        subprocess.SubprocessError,
    ) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
