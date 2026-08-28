#!/usr/bin/env python3
"""Coherent re-signed attacks on the v5 preflight reject verifier."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
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


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def document(path: Path, expected: str, closure_key: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected, path.name + ":file pin")
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw,
         path.name + ":canonical")
    body = dict(value)
    claim = body.pop(closure_key)
    need(claim == digest(body), path.name + ":closure")
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


def write_rows(path: Path, rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
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
        "file_sha256": file_sha(path),
        "row_sequence_sha256": sequence.hexdigest(),
    }


@dataclass(frozen=True)
class GapAttack:
    name: str
    predicate: Callable[[dict[str, Any]], bool]
    action: Callable[[dict[str, Any]], list[dict[str, Any]]]


@dataclass(frozen=True)
class ResultAttack:
    name: str
    action: Callable[[dict[str, Any]], None]


def set_fields(**changes: Any) -> Callable[[dict[str, Any]], list[dict[str, Any]]]:
    def apply(row: dict[str, Any]) -> list[dict[str, Any]]:
        value = dict(row)
        value.update(changes)
        return [reclose_row(value)]
    return apply


def change_evidence(key: str, value: Any) -> Callable[[dict[str, Any]], list[dict[str, Any]]]:
    def apply(row: dict[str, Any]) -> list[dict[str, Any]]:
        changed = dict(row)
        evidence = dict(changed["evidence"])
        evidence[key] = value
        changed["evidence"] = evidence
        return [reclose_row(changed)]
    return apply


def delete(_: dict[str, Any]) -> list[dict[str, Any]]:
    return []


def duplicate(row: dict[str, Any]) -> list[dict[str, Any]]:
    return [row, row]


def set_path(path: tuple[str, ...], value: Any) -> Callable[[dict[str, Any]], None]:
    def apply(result: dict[str, Any]) -> None:
        cursor: dict[str, Any] = result
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
    return apply


def promote_result(result: dict[str, Any]) -> None:
    result["status"] = "PASS_ATTACK_FALSE_GLOBAL_AUTHORITY"
    result["decision"] = "SCOPED_READY_ZERO_CREDIT"
    result["intended_process_exit_code"] = 0
    result["blocking_authority_slots"] = []
    result["authority_slot_census"] = {"total": 9, "present": 9, "missing_or_blocking": 0}
    result["global_gate"]["full_atom_incidence_formal_authority_present"] = True
    result["global_gate"]["C26_exact_contact_absence_formal_authority_present"] = True
    result["global_gate"]["primitive_twenty_family_totality_proved"] = True
    result["global_gate"]["decision"] = "ZERO_CREDIT_SCOPED_READY"


def promote_credit(result: dict[str, Any]) -> None:
    result["formal_credit"] = 1
    result["manifest_authorized"] = True
    result["strict_nonpromotion"]["C27_transition_totality"] = 1
    result["strict_nonpromotion"]["CM2"] = "GO"


def source_path(item: dict[str, Any]) -> Path:
    path = Path(item["path"])
    return path if path.is_absolute() else ROOT / path


def command(
    verifier: Path,
    baseline: dict[str, Any],
    result_path: Path,
    result_sha: str,
    gap_path: Path,
    gap_sha: str,
    out_path: Path,
    seed: int,
) -> list[str]:
    labels = (
        "correction_v2",
        "strict_volume_receipt",
        "lower_contact_receipt",
        "c19c_receipt",
        "g2a_result",
        "g2b_receipt",
        "pair_union_result",
        "pair_ownership",
    )
    attestations = baseline["root_input_capture"]["attestations"]
    answer = ["python3", str(verifier)]
    for label in labels:
        option = label.replace("_", "-")
        item = attestations[label]
        answer.extend([
            "--" + option, str(source_path(item)),
            "--" + option + "-sha256", item["sha256"],
        ])
    answer.extend([
        "--preflight-result", str(result_path),
        "--preflight-result-sha256", result_sha,
        "--gap-ledger", str(gap_path),
        "--gap-ledger-sha256", gap_sha,
        "--out-file", str(out_path),
        "--seed", str(seed),
    ])
    return answer


def materialize_gap_attack(
    attack: GapAttack,
    baseline: dict[str, Any],
    baseline_gap: Path,
    destination: Path,
) -> tuple[Path, str, Path, str]:
    result = json.loads(json.dumps(baseline))
    gap_path = destination / "authority_gap_ledger.jsonl.gz"
    mutated = 0

    def rows() -> Iterable[dict[str, Any]]:
        nonlocal mutated
        with gzip.open(baseline_gap, "rb") as stream:
            for line in stream:
                row = json.loads(line)
                if mutated == 0 and attack.predicate(row):
                    mutated += 1
                    yield from attack.action(row)
                else:
                    yield row

    result["gap_ledger"] = write_rows(gap_path, rows())
    need(mutated == 1, attack.name + ":target")
    result = reclose_result(result)
    result_path = destination / "preflight_result.json"
    result_path.write_bytes(canonical(result) + b"\n")
    return result_path, file_sha(result_path), gap_path, file_sha(gap_path)


def materialize_result_attack(
    attack: ResultAttack,
    baseline: dict[str, Any],
    baseline_gap: Path,
    destination: Path,
) -> tuple[Path, str, Path, str]:
    result = json.loads(json.dumps(baseline))
    attack.action(result)
    result = reclose_result(result)
    result_path = destination / "preflight_result.json"
    result_path.write_bytes(canonical(result) + b"\n")
    gap_path = destination / "authority_gap_ledger.jsonl.gz"
    os.link(baseline_gap, gap_path)
    return result_path, file_sha(result_path), gap_path, file_sha(gap_path)


def run_one(
    name: str,
    verifier: Path,
    baseline: dict[str, Any],
    result_path: Path,
    result_sha: str,
    gap_path: Path,
    gap_sha: str,
    directory: Path,
    seed: int,
    timeout: int,
) -> dict[str, Any]:
    out_path = directory / "unexpected_verification.json"
    completed = subprocess.run(
        command(verifier, baseline, result_path, result_sha, gap_path, gap_sha,
                out_path, seed),
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
        check=False,
    )
    rejected = completed.returncode == 2 and completed.stdout.startswith("REJECT:")
    return {
        "attack": name,
        "mutated_preflight_result_file_sha256": result_sha,
        "mutated_gap_ledger_file_sha256": gap_sha,
        "verifier_exit_code": completed.returncode,
        "verifier_stdout": completed.stdout.strip()[:500],
        "verifier_stderr": completed.stderr.strip()[:500],
        "unexpected_verification_output_created": out_path.exists(),
        "rejected": rejected,
    }


def attack_specs() -> tuple[list[GapAttack], list[ResultAttack]]:
    slot = lambda name: (lambda row: row.get("authority_slot") == name)
    gap_attacks = [
        GapAttack("full_atom_gap_falsely_closed",
                  slot("FULL_101080_TO_483232_ATOM_INCIDENCE"),
                  set_fields(authority_status="PRESENT_VALID", gate_blocking=False)),
        GapAttack("C26_gap_falsely_closed",
                  slot("C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_THEOREM"),
                  set_fields(authority_status="PRESENT_VALID", gate_blocking=False)),
        GapAttack("full_atom_gap_deleted",
                  slot("FULL_101080_TO_483232_ATOM_INCIDENCE"), delete),
        GapAttack("C26_gap_duplicated",
                  slot("C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_THEOREM"), duplicate),
        GapAttack("pair_authority_count_inflated",
                  slot("SCOPED_PAIR_UNION_101080"),
                  change_evidence("pair_count", 101_081)),
        GapAttack("atom_denominator_mutated",
                  slot("FULL_101080_TO_483232_ATOM_INCIDENCE"),
                  change_evidence("required_atom_denominator", 483_231)),
        GapAttack("present_strict_authority_marked_blocking",
                  slot("SAME_CHART_STRICT_VOLUME_187132"),
                  set_fields(gate_blocking=True)),
    ]
    result_attacks = [
        ResultAttack("false_global_promotion", promote_result),
        ResultAttack("atom_multi_pair_forbidden",
                     set_path(("corrected_contract", "atom_multi_pair_allowed"), False)),
        ResultAttack("atom_multi_terminal_forbidden",
                     set_path(("corrected_contract", "atom_multi_terminal_allowed"), False)),
        ResultAttack("atom_single_terminal_constraint_restored",
                     set_path(("corrected_contract",
                               "atom_single_pair_or_terminal_constraint_imposed"), True)),
        ResultAttack("C26_blocker_removed_from_result",
                     set_path(("blocking_authority_slots",),
                              ["FULL_101080_TO_483232_ATOM_INCIDENCE"])),
        ResultAttack("pair_reconstruction_count_inflated",
                     set_path(("pair_authority_reconstruction", "pair_count"), 101_081)),
        ResultAttack("old_C27_FAMILIES_claimed_read",
                     set_path(("forbidden_input_governance",
                               "old_C27_FAMILIES_imported_or_read"), True)),
        ResultAttack("formal_credit_promotion", promote_credit),
    ]
    return gap_attacks, result_attacks


def execute(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_file)
    need(not output.exists(), "fresh attack output")
    verifier = Path(args.verifier).resolve()
    need(file_sha(verifier) == args.verifier_sha256, "verifier source pin")
    baseline_path = Path(args.baseline_result).resolve()
    gap_path = Path(args.baseline_gap).resolve()
    baseline = document(baseline_path, args.baseline_result_sha256, "result_sha256")
    need(file_sha(gap_path) == args.baseline_gap_sha256, "baseline gap pin")
    gap_attacks, result_attacks = attack_specs()
    jobs: list[tuple[str, Path, str, Path, str, Path, int]] = []
    with tempfile.TemporaryDirectory(prefix="cm2-v5-preflight-attacks-") as temp_name:
        root = Path(temp_name)
        ordinal = 0
        for attack in gap_attacks:
            directory = root / f"{ordinal:02d}-{attack.name}"
            directory.mkdir()
            result_path, result_sha, attack_gap, attack_gap_sha = materialize_gap_attack(
                attack, baseline, gap_path, directory
            )
            jobs.append((attack.name, result_path, result_sha, attack_gap,
                         attack_gap_sha, directory, args.seed + ordinal))
            ordinal += 1
        for attack in result_attacks:
            directory = root / f"{ordinal:02d}-{attack.name}"
            directory.mkdir()
            result_path, result_sha, attack_gap, attack_gap_sha = materialize_result_attack(
                attack, baseline, gap_path, directory
            )
            jobs.append((attack.name, result_path, result_sha, attack_gap,
                         attack_gap_sha, directory, args.seed + ordinal))
            ordinal += 1

        results: list[dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            pending = {
                executor.submit(
                    run_one, name, verifier, baseline, result_path, result_sha,
                    attack_gap, attack_gap_sha, directory, seed, args.timeout
                ): name
                for (name, result_path, result_sha, attack_gap, attack_gap_sha,
                     directory, seed) in jobs
            }
            for future in as_completed(pending):
                results.append(future.result())
        results.sort(key=lambda item: item["attack"])
        rejected = sum(item["rejected"] for item in results)
        need(rejected == len(results)
             and all(not item["unexpected_verification_output_created"] for item in results),
             "all coherent attacks rejected")

    body = {
        "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-preflight-attacks.v1",
        "status": "PASS_ALL_COHERENT_RESIGNED_PREFLIGHT_ATTACKS_REJECTED__ZERO_CREDIT",
        "attack_seed": args.seed,
        "attack_count": len(results),
        "rejected_attack_count": rejected,
        "accepted_attack_count": len(results) - rejected,
        "attacks": results,
        "coherence": {
            "mutated_rows_reclosed": True,
            "mutated_gap_gzip_and_sequence_hashes_recomputed": True,
            "mutated_gap_descriptor_recomputed": True,
            "mutated_semantic_projection_recomputed": True,
            "mutated_result_closure_recomputed": True,
            "verifier_pinned_and_run_as_subprocess_not_imported": True,
        },
        "verified_decision": "REJECT",
        "formal_credit": 0,
        "manifest_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
        "pins": {
            "verifier_source_sha256": args.verifier_sha256,
            "baseline_result_file_sha256": args.baseline_result_sha256,
            "baseline_gap_file_sha256": args.baseline_gap_sha256,
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
    parser.add_argument("--baseline-gap", required=True)
    parser.add_argument("--baseline-gap-sha256", required=True)
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
        "attack_result_sha256": report["attack_result_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
