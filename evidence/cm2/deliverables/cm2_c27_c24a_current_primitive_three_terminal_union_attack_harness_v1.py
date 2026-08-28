#!/usr/bin/env python3
"""Coherent re-signed attacks against the independent union verifier.

Every mutation is cryptographically re-closed.  Ledger attacks recompute the
row closure, deterministic gzip digest, row-sequence digest, comparator ledger
descriptor, semantic projection, and result closure.  Result attacks likewise
recompute both result closures.  The independent verifier is executed as a
pinned subprocess; it is never imported.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any, Callable, Iterable


ROOT = Path(__file__).resolve().parent.parent


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def parse_result(path: Path, expected: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected, "baseline result file pin")
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw, "baseline canonical")
    body = dict(value)
    claim = body.pop("result_sha256")
    need(claim == digest(body), "baseline result closure")
    return value


def reclose_row(row: dict[str, Any]) -> dict[str, Any]:
    body = dict(row)
    body.pop("row_sha256", None)
    body["row_sha256"] = digest(body)
    return body


def reclose_result(result: dict[str, Any]) -> dict[str, Any]:
    value = json.loads(json.dumps(result))
    value.pop("semantic_projection_sha256", None)
    value.pop("result_sha256", None)
    value["semantic_projection_sha256"] = digest({
        key: item for key, item in value.items()
        if key not in {"invocation_seed", "root_input_capture"}
    })
    value["result_sha256"] = digest(value)
    return value


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    count = 0
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as stream:
            for row in rows:
                stream.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
                count += 1
    return {
        "filename": path.name,
        "row_count": count,
        "file_sha256": file_hash(path),
        "row_sequence_sha256": sequence.hexdigest(),
    }


@dataclass(frozen=True)
class LedgerAttack:
    name: str
    ledger_key: str
    predicate: Callable[[dict[str, Any]], bool]
    action: Callable[[dict[str, Any]], list[dict[str, Any]]]


@dataclass(frozen=True)
class ResultAttack:
    name: str
    action: Callable[[dict[str, Any]], None]


def changed(field: str, value: Any) -> Callable[[dict[str, Any]], list[dict[str, Any]]]:
    def apply(row: dict[str, Any]) -> list[dict[str, Any]]:
        value_row = dict(row)
        value_row[field] = value
        return [reclose_row(value_row)]
    return apply


def delete(_: dict[str, Any]) -> list[dict[str, Any]]:
    return []


def duplicate(row: dict[str, Any]) -> list[dict[str, Any]]:
    return [row, row]


def rebound_pair(field: str) -> Callable[[dict[str, Any]], list[dict[str, Any]]]:
    def apply(row: dict[str, Any]) -> list[dict[str, Any]]:
        value_row = dict(row)
        values = list(value_row[field])
        values[0] += ":coherent-attack"
        value_row[field] = values
        return [reclose_row(value_row)]
    return apply


def set_path(path: tuple[str, ...], value: Any) -> Callable[[dict[str, Any]], None]:
    def apply(document: dict[str, Any]) -> None:
        cursor: dict[str, Any] = document
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
    return apply


def promote_global(document: dict[str, Any]) -> None:
    gate = document["global_claim_gate"]
    gate["atom_to_pair_incidence_ledger_materialized_here"] = True
    gate["atom_without_pair_complement_census_materialized_here"] = True
    gate["primitive_row_bound_terminal_selection_exhaustive"] = True
    gate["primitive_row_bound_terminal_selection_mutually_exclusive"] = True
    gate["pair_routing_total_on_483232_atom_denominator"] = True
    gate["global_candidate_totality_proved"] = True
    gate["global_unique_assignment_proved"] = True
    gate["decision"] = "PASS_GLOBAL_PROMOTION"
    document["status"] = "ATTACK_GLOBAL_PROMOTION"


def promote_formal(document: dict[str, Any]) -> None:
    document["formal_credit"] = 1
    document["manifest_authorized"] = True
    document["strict_nonpromotion"]["C27_transition_totality"] = 1
    document["strict_nonpromotion"]["CM2"] = "GO"


def source_path(attestation: dict[str, Any]) -> Path:
    path = Path(attestation["path"])
    return path if path.is_absolute() else ROOT / path


def make_command(
    verifier: Path,
    result: dict[str, Any],
    mutated_result: Path,
    mutated_result_sha: str,
    verifier_output: Path,
    seed: int,
) -> list[str]:
    labels = (
        "g2a_contacts",
        "g2a_reverse_empty",
        "g2a_edges",
        "g2a_scoped_result",
        "g2b_terminal_receipt",
        "g2b_exact",
        "g2b_priority",
        "g2b_edges",
        "current_routes",
        "current_seed2_routes",
        "current_dual_seed_authority",
        "c19c_endpoint_v3_receipt",
        "strict_validation_edges",
    )
    command = ["python3", str(verifier)]
    attestations = result["root_input_capture"]["attestations"]
    for label in labels:
        option = label.replace("_", "-")
        command.extend([
            "--" + option,
            str(source_path(attestations[label])),
            "--" + option + "-sha256",
            attestations[label]["sha256"],
        ])
    command.extend([
        "--comparator-result", str(mutated_result),
        "--comparator-result-sha256", mutated_result_sha,
        "--out-file", str(verifier_output),
        "--seed", str(seed),
    ])
    return command


def link_baseline_ledgers(
    baseline_dir: Path, attack_dir: Path, result: dict[str, Any], skip_key: str | None
) -> None:
    for ledger_key, descriptor in result["ledgers"].items():
        if ledger_key == skip_key:
            continue
        source = baseline_dir / descriptor["filename"]
        destination = attack_dir / descriptor["filename"]
        os.link(source, destination)


def materialize_ledger_attack(
    attack: LedgerAttack,
    baseline_dir: Path,
    attack_dir: Path,
    baseline_result: dict[str, Any],
) -> tuple[Path, str, dict[str, Any]]:
    result = json.loads(json.dumps(baseline_result))
    link_baseline_ledgers(baseline_dir, attack_dir, result, attack.ledger_key)
    descriptor = result["ledgers"][attack.ledger_key]
    source = baseline_dir / descriptor["filename"]
    destination = attack_dir / descriptor["filename"]
    mutated = 0

    def rows() -> Iterable[dict[str, Any]]:
        nonlocal mutated
        with gzip.open(source, "rb") as stream:
            for line in stream:
                row = json.loads(line)
                if mutated == 0 and attack.predicate(row):
                    mutated += 1
                    yield from attack.action(row)
                else:
                    yield row

    result["ledgers"][attack.ledger_key] = write_jsonl(destination, rows())
    need(mutated == 1, attack.name + ":target row")
    result = reclose_result(result)
    result_path = attack_dir / "result.json"
    result_path.write_bytes(canonical(result) + b"\n")
    result_file_sha = file_hash(result_path)
    return result_path, result_file_sha, result


def materialize_result_attack(
    attack: ResultAttack,
    baseline_dir: Path,
    attack_dir: Path,
    baseline_result: dict[str, Any],
) -> tuple[Path, str, dict[str, Any]]:
    result = json.loads(json.dumps(baseline_result))
    link_baseline_ledgers(baseline_dir, attack_dir, result, None)
    attack.action(result)
    result = reclose_result(result)
    result_path = attack_dir / "result.json"
    result_path.write_bytes(canonical(result) + b"\n")
    result_file_sha = file_hash(result_path)
    return result_path, result_file_sha, result


def run_one(
    attack_name: str,
    verifier: Path,
    baseline_result: dict[str, Any],
    result_path: Path,
    result_sha: str,
    attack_dir: Path,
    seed: int,
    timeout: int,
) -> dict[str, Any]:
    output = attack_dir / "unexpected_verification.json"
    completed = subprocess.run(
        make_command(verifier, baseline_result, result_path, result_sha, output, seed),
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
        check=False,
    )
    rejected = completed.returncode == 2 and completed.stdout.startswith("REJECT:")
    return {
        "attack": attack_name,
        "mutated_result_file_sha256": result_sha,
        "verifier_exit_code": completed.returncode,
        "verifier_stdout": completed.stdout.strip()[:500],
        "verifier_stderr": completed.stderr.strip()[:500],
        "unexpected_verification_output_created": output.exists(),
        "rejected": rejected,
    }


def attacks() -> tuple[list[LedgerAttack], list[ResultAttack]]:
    positive_key = lambda row: row.get("disposition") == "EXACT_POSITIVE_SUPPORT"
    empty_key = lambda row: row.get("disposition") == "EXACT_EMPTY_INTERSECTION"
    current_ownership = lambda row: row.get("source_authority") == "CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER"
    c24_ownership = lambda row: row.get("source_authority") == "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER"
    novel_edge = lambda row: row.get("novel_against_current_support") is True
    overlap_edge = lambda row: (row.get("present_in_current_support_primitive") is True
                                and row.get("present_in_G2B_terminal_authority") is True)
    ledger_attacks = [
        LedgerAttack("key_positive_disposition_flip", "C24A_key_comparison",
                     positive_key, changed("disposition", "EXACT_EMPTY_INTERSECTION")),
        LedgerAttack("key_positive_priority_binding_removed", "C24A_key_comparison",
                     positive_key, changed("g2b_priority_row_sha256", None)),
        LedgerAttack("key_empty_row_deleted", "C24A_key_comparison", empty_key, delete),
        LedgerAttack("key_authority_pair_rebound", "C24A_key_comparison",
                     positive_key, rebound_pair("authority_pair_key")),
        LedgerAttack("ownership_current_source_rebound", "unique_ownership",
                     current_ownership, changed("source_row_sha256", "0" * 64)),
        LedgerAttack("ownership_C24_terminal_flip", "unique_ownership",
                     c24_ownership, changed("assigned_terminal", "COMPLETE_BOUNDARY_FACES")),
        LedgerAttack("ownership_C24_row_duplicated", "unique_ownership",
                     c24_ownership, duplicate),
        LedgerAttack("ownership_pair_rebound", "unique_ownership",
                     current_ownership, rebound_pair("pair_key")),
        LedgerAttack("edge_current_membership_flip", "cross_C15_edge_union",
                     overlap_edge, changed("present_in_current_support_primitive", False)),
        LedgerAttack("edge_rank_contribution_flip", "cross_C15_edge_union",
                     novel_edge, changed("incremental_rank_contribution_after_current_support", False)),
        LedgerAttack("edge_history_promoted_to_candidate", "cross_C15_edge_union",
                     novel_edge, changed("strict_volume_used_as_candidate_source", True)),
        LedgerAttack("edge_overlap_row_deleted", "cross_C15_edge_union", overlap_edge, delete),
    ]
    result_attacks = [
        ResultAttack("result_global_totality_promotion", promote_global),
        ResultAttack("result_atom_denominator_changed",
                     set_path(("global_claim_gate", "primitive_support_atom_denominator"), 483_231)),
        ResultAttack("result_historical_edge_candidate_enable",
                     set_path(("candidate_governance",
                               "historical_edge_ledger_used_as_candidate_universe"), True)),
        ResultAttack("result_G2A_alias_double_count_enable",
                     set_path(("scoped_candidate_union",
                               "G2A_graph_alias_counted_as_independent_candidate"), True)),
        ResultAttack("result_union_count_inflated",
                     set_path(("scoped_candidate_union", "union_pair_count"), 101_081)),
        ResultAttack("result_formal_credit_promotion", promote_formal),
    ]
    return ledger_attacks, result_attacks


def execute(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_file)
    need(not output.exists(), "fresh attack output")
    verifier = Path(args.verifier).resolve()
    need(file_hash(verifier) == args.verifier_sha256, "verifier source pin")
    baseline_path = Path(args.baseline_result).resolve()
    baseline = parse_result(baseline_path, args.baseline_result_sha256)
    baseline_dir = baseline_path.parent
    ledger_attacks, result_attacks = attacks()
    materialized: list[tuple[str, Path, str, Path, int]] = []
    with tempfile.TemporaryDirectory(prefix="cm2-c24-current-union-attacks-") as temp_name:
        temporary = Path(temp_name)
        ordinal = 0
        for attack in ledger_attacks:
            attack_dir = temporary / f"{ordinal:02d}-{attack.name}"
            attack_dir.mkdir()
            result_path, result_sha, _ = materialize_ledger_attack(
                attack, baseline_dir, attack_dir, baseline
            )
            materialized.append((attack.name, result_path, result_sha, attack_dir,
                                 args.seed + ordinal))
            ordinal += 1
        for attack in result_attacks:
            attack_dir = temporary / f"{ordinal:02d}-{attack.name}"
            attack_dir.mkdir()
            result_path, result_sha, _ = materialize_result_attack(
                attack, baseline_dir, attack_dir, baseline
            )
            materialized.append((attack.name, result_path, result_sha, attack_dir,
                                 args.seed + ordinal))
            ordinal += 1

        results: list[dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            pending = {
                executor.submit(
                    run_one,
                    name,
                    verifier,
                    baseline,
                    result_path,
                    result_sha,
                    attack_dir,
                    seed,
                    args.timeout,
                ): name
                for name, result_path, result_sha, attack_dir, seed in materialized
            }
            for future in as_completed(pending):
                results.append(future.result())
        results.sort(key=lambda item: item["attack"])
        rejected = sum(item["rejected"] for item in results)
        need(rejected == len(results)
             and all(not item["unexpected_verification_output_created"] for item in results),
             "all coherent attacks rejected")

    body = {
        "schema": "cm2.c27-independent.c24a-current-primitive-three-terminal-union-attacks.v1",
        "status": "PASS_ALL_COHERENT_RESIGNED_ATTACKS_REJECTED__GLOBAL_FAIL_CLOSED__ZERO_CREDIT",
        "attack_seed": args.seed,
        "attack_count": len(results),
        "rejected_attack_count": rejected,
        "accepted_attack_count": len(results) - rejected,
        "attacks": results,
        "coherence": {
            "mutated_rows_reclosed": True,
            "mutated_gzip_and_row_sequence_digests_recomputed": True,
            "mutated_ledger_descriptors_recomputed": True,
            "semantic_projection_recomputed": True,
            "result_closure_recomputed": True,
            "verifier_source_pinned_and_executed_as_subprocess_not_imported": True,
        },
        "global_claim_gate": {
            "primitive_support_atom_denominator": 483_232,
            "global_totality_proved": False,
            "decision": "FAIL_CLOSED_NO_PROMOTION",
        },
        "formal_credit": 0,
        "manifest_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
        "pins": {
            "verifier_source_sha256": args.verifier_sha256,
            "baseline_result_file_sha256": args.baseline_result_sha256,
            "baseline_result_sha256": baseline["result_sha256"],
        },
    }
    report = dict(body)
    report["semantic_projection_sha256"] = digest({
        key: value for key, value in body.items() if key != "attack_seed"
    })
    report["attack_result_sha256"] = digest(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical(report) + b"\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--verifier-sha256", required=True)
    parser.add_argument("--baseline-result", required=True)
    parser.add_argument("--baseline-result-sha256", required=True)
    parser.add_argument("--out-file", required=True)
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    try:
        report = execute(args)
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError, subprocess.SubprocessError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({
        "status": report["status"],
        "attack_count": report["attack_count"],
        "rejected_attack_count": report["rejected_attack_count"],
        "semantic_projection_sha256": report["semantic_projection_sha256"],
        "attack_result_sha256": report["attack_result_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
