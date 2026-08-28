#!/usr/bin/env python3
"""Coherent candidate-corruption suite for append-only C30d-v3.

The suite reconstructs the independent reference once, verifies the baseline,
then applies closed mutations to fresh one-at-a-time copies.  It does not
publish any candidate, manifest, seal, or formal credit.  Predecessor/release
TOCTOU attacks remain the responsibility of the later transaction runner.
"""
from __future__ import annotations

import argparse
import ast
import copy
import gzip
import hashlib
import importlib.util
import json
import os
import shutil
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

sys.dont_write_bytecode = True

DELIVERABLES = Path(__file__).resolve().parent
WORKSPACE = DELIVERABLES.parent
PREFIX = "cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion_v3"
VERIFIER_REL = "deliverables/" + PREFIX + "_independent_verifier.py"
VERIFIER_SHA256 = (
    "a7d88985d591ea981eb78ff56fa407c48ba7e90e88860a72f7b87a3b88949a1c"
)
PRODUCER_REL = "deliverables/" + PREFIX + "_producer.py"
PRODUCER_SHA256 = (
    "946955775cfe1ddc2acba538f6723b64c57b8080ce12bd34e4959c2c46e1f11c"
)
CELL_LEDGER = PREFIX + "_multi_delta_cell_ledger.jsonl.gz"
ATOMIC_OWNER_LEDGER = PREFIX + "_atomic_half_open_owner_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
RUNTIME_ATTESTATION = "cm2_round306c30b_python_flint_runtime_attestation.json"
EXPECTED_FILES = {
    RUNTIME_ATTESTATION,
    CELL_LEDGER,
    ATOMIC_OWNER_LEDGER,
    ORIGIN_LEDGER,
    RESULT,
}
ZERO_FORMAL = {
    "multi_Delta_cell_dispositions": 0,
    "multi_Delta_whole_cell_exclusions": 0,
    "resolved_source_W_origin_dispositions": 0,
    "whole_source_W_origin_exclusions": 0,
}


class HarnessFailure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise HarnessFailure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(4 << 20)
            if block == b"":
                break
            state.update(block)
    return state.hexdigest()


def close_object(value: dict[str, Any], field: str) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop(field, None)
    return {**body, field: digest(body)}


def read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    need(type(value) is dict, "object fixture:" + path.name)
    return value


def write_result(target: Path, result: dict[str, Any]) -> None:
    (target / RESULT).write_bytes(canonical(close_object(result, "result_sha256")))


def read_rows(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        rows = [json.loads(line) for line in stream]
    need(bool(rows) and all(type(row) is dict for row in rows), "ledger fixture:" + path.name)
    return rows


def write_rows(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as stream:
            for row in rows:
                stream.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
    return {
        "row_count": len(rows),
        "size": path.stat().st_size,
        "sha256": file_hash(path),
        "row_sequence_sha256": sequence.hexdigest(),
    }


def rebind_ledger(
    target: Path,
    result: dict[str, Any],
    filename: str,
    descriptor_key: str,
    rows: list[dict[str, Any]],
) -> None:
    facts = write_rows(target / filename, rows)
    descriptor = result["ledgers"][descriptor_key]
    for key, value in facts.items():
        descriptor[key] = value


def mutate_result(target: Path, operation: Callable[[dict[str, Any]], None]) -> None:
    result = read_object(target / RESULT)
    operation(result)
    write_result(target, result)


def mutation_extra_file(target: Path) -> None:
    (target / "UNEXPECTED").write_bytes(b"attack\n")


def mutation_missing_result(target: Path) -> None:
    (target / RESULT).unlink()


def mutation_result_symlink(target: Path) -> None:
    (target / RESULT).unlink()
    (target / RESULT).symlink_to(CELL_LEDGER)


def mutation_runtime_hardlink(target: Path) -> None:
    (target / RUNTIME_ATTESTATION).unlink()
    os.link(target / CELL_LEDGER, target / RUNTIME_ATTESTATION)


def mutation_truncated_gzip(target: Path) -> None:
    path = target / CELL_LEDGER
    raw = path.read_bytes()
    need(len(raw) > 32, "truncation fixture")
    path.write_bytes(raw[:-17])


def mutation_noncanonical_result(target: Path) -> None:
    path = target / RESULT
    path.write_bytes(path.read_bytes() + b"\n")


def mutation_schema(target: Path) -> None:
    mutate_result(target, lambda result: result.__setitem__("schema", "cm2.attack.schema"))


def mutation_status(target: Path) -> None:
    mutate_result(target, lambda result: result.__setitem__("status", "PASS_ATTACK"))


def mutation_producer_hash(target: Path) -> None:
    mutate_result(
        target,
        lambda result: result["producer_contract"].__setitem__("source_sha256", "0" * 64),
    )


def mutation_authority_root(target: Path) -> None:
    mutate_result(
        target,
        lambda result: result["upstream_credit_boundary"]["authority"].__setitem__(
            "root_manifest_sha256", "1" * 64
        ),
    )


def mutation_input_pin(target: Path) -> None:
    mutate_result(
        target,
        lambda result: result["input_pins"][0].__setitem__("sha256", "2" * 64),
    )


def mutation_theorem(target: Path) -> None:
    def operation(result: dict[str, Any]) -> None:
        result["candidate_theorem"]["child_count_or_volume_used_as_whole_origin_credit"] = True
        result["candidate_theorem_sha256"] = digest(result["candidate_theorem"])

    mutate_result(target, operation)


def mutation_formal_credit(target: Path) -> None:
    mutate_result(
        target,
        lambda result: result["formal_credit"].__setitem__("whole_source_W_origin_exclusions", 20),
    )


def mutation_d02(target: Path) -> None:
    mutate_result(target, lambda result: result["strict_nonpromotion"].__setitem__("D02", "PASS"))


def mutation_d03(target: Path) -> None:
    mutate_result(target, lambda result: result["strict_nonpromotion"].__setitem__("D03", "AUTHORIZED"))


def mutation_d04(target: Path) -> None:
    mutate_result(target, lambda result: result["strict_nonpromotion"].__setitem__("D04", "MINTED"))


def mutation_gate5(target: Path) -> None:
    mutate_result(target, lambda result: result["strict_nonpromotion"].__setitem__("Gate5", "18/18"))


def mutation_cm2(target: Path) -> None:
    mutate_result(target, lambda result: result["strict_nonpromotion"].__setitem__("CM2", "GO"))


def mutation_transition_before(target: Path) -> None:
    mutate_result(
        target,
        lambda result: result["proposed_source_W_transition_if_C30d_is_terminally_sealed"]["before"].__setitem__("remaining", 77),
    )


def mutation_transition_after(target: Path) -> None:
    mutate_result(
        target,
        lambda result: result["proposed_source_W_transition_if_C30d_is_terminally_sealed"]["after"].__setitem__("remaining", 57),
    )


def mutation_transition_authorized(target: Path) -> None:
    mutate_result(
        target,
        lambda result: result["proposed_source_W_transition_if_C30d_is_terminally_sealed"].__setitem__("C30d_transition_authorized", True),
    )


def mutation_descriptor_order(target: Path) -> None:
    mutate_result(
        target,
        lambda result: result["ledgers"]["multi_Delta_cell_candidate"].__setitem__("order", "ATTACK_ORDER"),
    )


def mutation_cell_deep_reclosure(target: Path) -> None:
    result = read_object(target / RESULT)
    rows = read_rows(target / CELL_LEDGER)
    row = rows[0]
    row["whole_closed_cell_excluded"] = False
    rows[0] = close_object(row, "row_sha256")
    rebind_ledger(target, result, CELL_LEDGER, "multi_Delta_cell_candidate", rows)
    write_result(target, result)


def mutation_owner_deep_reclosure(target: Path) -> None:
    result = read_object(target / RESULT)
    rows = read_rows(target / ATOMIC_OWNER_LEDGER)
    row = rows[0]
    row["owner_disposition"] = "LIVE"
    rows[0] = close_object(row, "row_sha256")
    rebind_ledger(target, result, ATOMIC_OWNER_LEDGER, "atomic_half_open_owner_candidate", rows)
    write_result(target, result)


def mutation_origin_deep_reclosure(target: Path) -> None:
    result = read_object(target / RESULT)
    rows = read_rows(target / ORIGIN_LEDGER)
    row = rows[0]
    row["whole_origin_disposition_candidate"] = "RESOLVED_MIXED"
    row["whole_original_physical_origin_excluded_candidate"] = False
    rows[0] = close_object(row, "row_sha256")
    rebind_ledger(target, result, ORIGIN_LEDGER, "whole_origin_exclusion_candidate", rows)
    write_result(target, result)


def mutation_runtime_bytes(target: Path) -> None:
    path = target / RUNTIME_ATTESTATION
    raw = bytearray(path.read_bytes())
    raw[-1] ^= 1
    path.write_bytes(bytes(raw))


@dataclass(frozen=True)
class Attack:
    name: str
    mutate: Callable[[Path], None]


ATTACKS = (
    Attack("extra_file", mutation_extra_file),
    Attack("missing_result", mutation_missing_result),
    Attack("result_symlink", mutation_result_symlink),
    Attack("runtime_hardlink", mutation_runtime_hardlink),
    Attack("truncated_gzip", mutation_truncated_gzip),
    Attack("noncanonical_result", mutation_noncanonical_result),
    Attack("schema", mutation_schema),
    Attack("status", mutation_status),
    Attack("producer_hash", mutation_producer_hash),
    Attack("authority_root", mutation_authority_root),
    Attack("input_pin", mutation_input_pin),
    Attack("theorem_reclosure", mutation_theorem),
    Attack("formal_credit", mutation_formal_credit),
    Attack("D02", mutation_d02),
    Attack("D03", mutation_d03),
    Attack("D04", mutation_d04),
    Attack("Gate5", mutation_gate5),
    Attack("CM2", mutation_cm2),
    Attack("transition_before", mutation_transition_before),
    Attack("transition_after", mutation_transition_after),
    Attack("transition_authorized", mutation_transition_authorized),
    Attack("descriptor_order", mutation_descriptor_order),
    Attack("cell_deep_reclosure", mutation_cell_deep_reclosure),
    Attack("owner_deep_reclosure", mutation_owner_deep_reclosure),
    Attack("origin_deep_reclosure", mutation_origin_deep_reclosure),
    Attack("runtime_bytes", mutation_runtime_bytes),
)


def load_verifier() -> ModuleType:
    path = WORKSPACE / VERIFIER_REL
    need(file_hash(path) == VERIFIER_SHA256, "verifier source pin")
    need(file_hash(WORKSPACE / PRODUCER_REL) == PRODUCER_SHA256, "producer provenance pin")
    name = "_cm2_round306c30d_v3_verifier_for_attacks"
    need(name not in sys.modules, "verifier not preloaded")
    specification = importlib.util.spec_from_file_location(name, path)
    need(specification is not None and specification.loader is not None, "verifier import specification")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    need(
        Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
        and file_hash(path) == VERIFIER_SHA256,
        "imported verifier identity",
    )
    return module


def copy_candidate(source: Path, target: Path) -> None:
    os.mkdir(target, 0o700)
    for filename in sorted(EXPECTED_FILES):
        shutil.copyfile(source / filename, target / filename)
    need(
        {entry.name for entry in os.scandir(target)} == EXPECTED_FILES
        and all(
            stat.S_ISREG((target / filename).lstat().st_mode)
            and (target / filename).lstat().st_nlink == 1
            and not (target / filename).is_symlink()
            for filename in EXPECTED_FILES
        ),
        "fresh attack copy",
    )


def run_attacks(chain: Path, pins: Path, candidate: Path, work: Path) -> dict[str, Any]:
    verifier = load_verifier()
    verifier.independent_runtime_guard()
    projection = verifier.run_authority(chain, pins)
    legacy = verifier.load_math_verifier()
    reference = verifier.reconstruct_reference(
        legacy,
        projection,
        Path(os.path.abspath(os.fspath(pins))),
    )
    baseline = verifier.validate_candidate_directory(candidate, projection, reference)
    need(
        baseline["status"]
        == (
            "PASS_NO_IMPORT_INDEPENDENT_C30D_V3__1176_CELLS__20_EXCLUDED_ORIGINS__"
            "ZERO_FORMAL_CREDIT__MANIFEST_UNAUTHORIZED"
        )
        and baseline["formal_credit"] == ZERO_FORMAL
        and baseline["C30d_transition_authorized"] is False,
        "baseline candidate verification",
    )
    absolute_work = Path(os.path.abspath(os.fspath(work)))
    need(
        absolute_work.parent.resolve(strict=True) == absolute_work.parent
        and absolute_work.is_relative_to(WORKSPACE)
        and not absolute_work.exists()
        and not absolute_work.is_symlink(),
        "fresh attack work directory",
    )
    os.mkdir(absolute_work, 0o700)
    rejected: list[str] = []
    try:
        for ordinal, attack in enumerate(ATTACKS):
            target = absolute_work / f"attack-{ordinal:02d}-{attack.name}"
            copy_candidate(candidate, target)
            attack.mutate(target)
            accepted = False
            try:
                verifier.validate_candidate_directory(target, projection, reference)
                accepted = True
            except (
                verifier.Reject,
                OSError,
                ValueError,
                TypeError,
                KeyError,
                AssertionError,
                gzip.BadGzipFile,
                EOFError,
            ):
                rejected.append(attack.name)
            need(not accepted, "attack accepted:" + attack.name)
            shutil.rmtree(target)
    finally:
        if absolute_work.is_dir() and not any(absolute_work.iterdir()):
            absolute_work.rmdir()
    need(rejected == [attack.name for attack in ATTACKS], "all coherent attacks rejected")
    return {
        "schema": "cm2.round306c30d.v3-coherent-attack-harness.v1",
        "status": "PASS_ALL_C30D_V3_COHERENT_CANDIDATE_ATTACKS_REJECTED__ZERO_FORMAL_CREDIT",
        "verifier_sha256": VERIFIER_SHA256,
        "producer_sha256": PRODUCER_SHA256,
        "candidate_result_sha256": baseline["candidate_result_sha256"],
        "attack_count": len(ATTACKS),
        "rejected_attacks": rejected,
        "release_only_attacks_deferred_to_transaction_runner": True,
        "formal_credit": ZERO_FORMAL,
        "C30d_transition_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def self_test() -> dict[str, Any]:
    names = [attack.name for attack in ATTACKS]
    need(len(names) == 26 and len(set(names)) == 26, "attack registry uniqueness")
    fixture = {
        "schema": "fixture",
        "formal_credit": copy.deepcopy(ZERO_FORMAL),
        "strict_nonpromotion": {
            "D02": "BLOCKED_COMPOSITE",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    closed = close_object(fixture, "result_sha256")
    body = dict(closed)
    claimed = body.pop("result_sha256")
    need(claimed == digest(body), "synthetic object closure")
    tree = ast.parse(Path(__file__).read_bytes())
    suspicious: list[int] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "need" and node.args:
            first = node.args[0]
            if isinstance(first, ast.BoolOp) and isinstance(first.values[-1], (ast.Name, ast.Attribute, ast.Subscript)):
                suspicious.append(node.lineno)
    need(not suspicious, "exact-bool static audit")
    need(file_hash(WORKSPACE / VERIFIER_REL) == VERIFIER_SHA256, "self-test verifier pin")
    need(file_hash(WORKSPACE / PRODUCER_REL) == PRODUCER_SHA256, "self-test producer pin")
    return {
        "schema": "cm2.round306c30d.v3-coherent-attack-self-test.v1",
        "status": "PASS_C30D_V3_ATTACK_REGISTRY_AND_STATIC_FIXTURES__ZERO_FORMAL_CREDIT",
        "attack_count": len(ATTACKS),
        "attack_names": names,
        "exact_bool_suspicious_lines": suspicious,
        "formal_credit": ZERO_FORMAL,
        "C30d_transition_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chain-dir", type=Path)
    parser.add_argument("--dynamic-pins", type=Path)
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    try:
        if arguments.self_test:
            need(
                arguments.chain_dir is None
                and arguments.dynamic_pins is None
                and arguments.candidate_dir is None
                and arguments.work_dir is None,
                "self-test argument isolation",
            )
            output = self_test()
        else:
            need(
                arguments.chain_dir is not None
                and arguments.dynamic_pins is not None
                and arguments.candidate_dir is not None
                and arguments.work_dir is not None,
                "complete attack arguments",
            )
            output = run_attacks(
                arguments.chain_dir,
                arguments.dynamic_pins,
                arguments.candidate_dir,
                arguments.work_dir,
            )
    except (HarnessFailure, OSError, ValueError, TypeError, KeyError, AssertionError):
        return 2
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
