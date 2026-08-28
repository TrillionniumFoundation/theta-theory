#!/usr/bin/env python3
"""Coherent, re-signed attacks against the independent 10,660-row verifier."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
VERIFIER = ROOT / "deliverables/cm2_c27_included_stratum_10660_independent_verifier_v1.py"


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def close(value: dict[str, Any], key: str) -> None:
    value.pop(key, None)
    value[key] = digest(value)


def semantic_close(row: dict[str, Any]) -> None:
    semantic = {key: row[key] for key in (
        "representation_id", "owner_member_id", "fresh_component_id",
        "base_root_id", "official_key_id", "representation_semantic_kind",
        "semantic_kernel", "owner_normalized_support_ast_sha256",
        "representation_semantic_certificate_sha256",
        "C15_member_row_sha256", "C25_representation_row_sha256",
        "C26_handle_row_sha256", "C20D_source_semantics",
        "C20D_row_sha256", "cross_component", "formal_credit")}
    row["semantic_body_sha256"] = digest(semantic)
    close(row, "row_sha256")


def write_ledger(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            for row in rows:
                zipped.write(encode(row) + b"\n")


def resign_result(result: dict[str, Any], ledger: Path,
                  rows: list[dict[str, Any]]) -> None:
    result["ledger"]["file_sha256"] = file_hash(ledger)
    result["ledger"]["row_count"] = len(rows)
    result["ledger"]["row_sequence_sha256"] = digest(
        [row["row_sha256"] for row in rows])
    close(result, "result_sha256")


def flip_hex(value: str) -> str:
    return ("0" if value[0] != "0" else "1") + value[1:]


Mutation = Callable[[list[dict[str, Any]], dict[str, Any]], None]


def row_mutation(field: str, value: Any, semantic: bool = False) -> Mutation:
    def mutate(rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
        del result
        rows[len(rows) // 2][field] = value
        if semantic:
            semantic_close(rows[len(rows) // 2])
        else:
            close(rows[len(rows) // 2], "row_sha256")
    return mutate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", required=True)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result_path = Path(args.result)
    ledger_path = Path(args.ledger)
    baseline_result = json.loads(result_path.read_bytes())
    with gzip.open(ledger_path, "rt", encoding="ascii") as handle:
        baseline_rows = [json.loads(line) for line in handle]

    def drop(rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
        del result
        rows.pop(len(rows) // 2)
        for ordinal, row in enumerate(rows):
            row["ordinal"] = ordinal
            close(row, "row_sha256")

    def duplicate(rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
        del result
        row = copy.deepcopy(rows[len(rows) // 2])
        rows.insert(len(rows) // 2, row)
        for ordinal, current in enumerate(rows):
            current["ordinal"] = ordinal
            close(current, "row_sha256")

    def reverse_pair(rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
        del result
        middle = len(rows) // 2
        rows[middle], rows[middle + 1] = rows[middle + 1], rows[middle]
        for ordinal in (middle, middle + 1):
            rows[ordinal]["ordinal"] = ordinal
            close(rows[ordinal], "row_sha256")

    def result_mutation(field: str, value: Any) -> Mutation:
        def mutate(rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
            del rows
            result[field] = value
        return mutate

    row = baseline_rows[len(baseline_rows) // 2]
    attacks: list[tuple[str, Mutation]] = [
        ("drop_candidate_and_reindex", drop),
        ("duplicate_candidate_and_reindex", duplicate),
        ("swap_adjacent_candidates_and_reindex", reverse_pair),
        ("terminal_flip", row_mutation("terminal", "RETAINED_CONTINUATION")),
        ("terminal_disposition_flip", row_mutation(
            "terminal_disposition", "UNIQUE_RETAINED_CONTINUATION")),
        ("retained_flag_flip", row_mutation("retained_continuation_candidate", True)),
        ("cross_component_flip", row_mutation("cross_component", True, True)),
        ("formal_credit_flip", row_mutation("formal_credit", 1, True)),
        ("source_authorization_flip", row_mutation("source_W_transition_authorized", True)),
        ("owner_member_flip", row_mutation(
            "owner_member_id", row["owner_member_id"] + ":mutant", True)),
        ("component_flip", row_mutation(
            "fresh_component_id", row["fresh_component_id"] + ":mutant", True)),
        ("C15_pin_flip", row_mutation(
            "C15_member_row_sha256", flip_hex(row["C15_member_row_sha256"]), True)),
        ("C25_pin_flip", row_mutation(
            "C25_representation_row_sha256",
            flip_hex(row["C25_representation_row_sha256"]), True)),
        ("C26_pin_flip", row_mutation(
            "C26_handle_row_sha256", flip_hex(row["C26_handle_row_sha256"]), True)),
        ("semantic_kind_flip", row_mutation(
            "representation_semantic_kind", "MUTATED_DISPOSITION", True)),
        ("semantic_kernel_flip", row_mutation("semantic_kernel", "MUTATED_KERNEL", True)),
        ("result_formal_credit_flip", result_mutation("formal_credit", 1)),
        ("result_manifest_authorized_flip", result_mutation("manifest_authorized", True)),
        ("result_source_authorized_flip", result_mutation(
            "source_W_transition_authorized", True)),
        ("result_count_flip", result_mutation("candidate_count", 10_659)),
    ]
    attack_results = []
    with tempfile.TemporaryDirectory(prefix="cm2-c27-included-attacks-") as tmp:
        temp = Path(tmp)
        for index, (name, mutate) in enumerate(attacks):
            rows = copy.deepcopy(baseline_rows)
            result = copy.deepcopy(baseline_result)
            mutate(rows, result)
            attack_ledger = temp / f"{index:02d}.jsonl.gz"
            attack_result = temp / f"{index:02d}.json"
            verification = temp / f"{index:02d}.verification.json"
            write_ledger(attack_ledger, rows)
            resign_result(result, attack_ledger, rows)
            attack_result.write_bytes(encode(result) + b"\n")
            completed = subprocess.run(
                [sys.executable, "-I", "-B", str(VERIFIER),
                 "--result", str(attack_result), "--ledger", str(attack_ledger),
                 "--sqlite-seed", str(args.seed + index),
                 "--output", str(verification)],
                cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                check=False)
            rejected = completed.returncode == 2 and completed.stderr == b""
            attack_results.append({
                "ordinal": index, "attack": name, "rejected": rejected,
                "numeric_exit": completed.returncode,
                "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
                "stderr_empty": completed.stderr == b"",
            })
            if not rejected:
                raise RuntimeError(f"attack not rejected: {name}: {completed.stdout!r}")
    body = {
        "schema": "cm2.c27-independent.included-stratum-10660.coherent-attacks.v1",
        "status": "PASS_20_OF_20_COHERENT_RESIGNED_ATTACKS_REJECTED__ZERO_CREDIT",
        "attack_count": len(attacks), "all_rejected": True,
        "attacks": attack_results,
        "baseline_result_file_sha256": file_hash(result_path),
        "baseline_ledger_file_sha256": file_hash(ledger_path),
        "verifier_file_sha256": file_hash(VERIFIER),
        "formal_credit": 0, "manifest_authorized": False,
        "source_W_transition_authorized": False,
    }
    output = Path(args.output)
    if output.exists():
        raise RuntimeError("fresh output required")
    value = {**body, "attack_result_sha256": digest(body)}
    output.write_bytes(encode(value) + b"\n")
    print(encode({"status": value["status"],
                  "attack_result_sha256": value["attack_result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
