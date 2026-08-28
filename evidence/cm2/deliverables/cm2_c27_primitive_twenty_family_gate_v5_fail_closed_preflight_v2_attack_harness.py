#!/usr/bin/env python3
"""Coherent re-signed attacks for the authority-hardened v5 preflight v2."""

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
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def load_document(path: Path, expected: str, closure_key: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected, path.name + ":file pin")
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw,
         path.name + ":canonical")
    body = dict(value)
    claim = body.pop(closure_key, None)
    need(type(claim) is str and claim == digest(body), path.name + ":closure")
    return value


def reclose_row(row: dict[str, Any]) -> dict[str, Any]:
    body = dict(row)
    body.pop("row_sha256", None)
    body["row_sha256"] = digest(body)
    return body


def reclose_result(value: dict[str, Any]) -> dict[str, Any]:
    result = json.loads(json.dumps(value))
    result.pop("semantic_projection_sha256", None)
    result.pop("result_sha256", None)
    result["semantic_projection_sha256"] = digest({
        key: item for key, item in result.items()
        if key not in {"invocation_seed", "root_input_capture"}
    })
    result["result_sha256"] = digest(result)
    return result


def write_rows(path: Path, rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    count = 0
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as stream:
            for row in rows:
                stream.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
                count += 1
    return {"filename": path.name, "row_count": count,
            "file_sha256": file_sha(path),
            "row_sequence_sha256": sequence.hexdigest()}


@dataclass(frozen=True)
class GapAttack:
    name: str
    predicate: Callable[[dict[str, Any]], bool]
    mutate: Callable[[dict[str, Any]], list[dict[str, Any]]]


@dataclass(frozen=True)
class ResultAttack:
    name: str
    mutate: Callable[[dict[str, Any]], None]


def set_row_fields(**changes: Any) -> Callable[[dict[str, Any]], list[dict[str, Any]]]:
    def apply(row: dict[str, Any]) -> list[dict[str, Any]]:
        changed = dict(row)
        changed.update(changes)
        return [reclose_row(changed)]
    return apply


def change_evidence(path: tuple[str, ...], value: Any) -> Callable[[dict[str, Any]], list[dict[str, Any]]]:
    def apply(row: dict[str, Any]) -> list[dict[str, Any]]:
        changed = json.loads(json.dumps(row))
        cursor: dict[str, Any] = changed["evidence"]
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        return [reclose_row(changed)]
    return apply


def delete_row(_: dict[str, Any]) -> list[dict[str, Any]]:
    return []


def duplicate_row(row: dict[str, Any]) -> list[dict[str, Any]]:
    return [row, row]


def set_result_path(path: tuple[str, ...], value: Any) -> Callable[[dict[str, Any]], None]:
    def apply(result: dict[str, Any]) -> None:
        cursor: dict[str, Any] = result
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
    return apply


def restore_atom_single_terminal(result: dict[str, Any]) -> None:
    contract = result["corrected_contract"]
    contract["atom_multi_pair_allowed"] = False
    contract["atom_multi_terminal_allowed"] = False
    contract["atom_single_pair_or_terminal_constraint_imposed"] = True


def accept_invalidated_g2a(result: dict[str, Any]) -> None:
    result["authority_hardening"]["G2A_old_invalidated_seal_rejected"] = False
    result["forbidden_input_governance"]["old_invalidated_G2A_seal_accepted"] = True


def false_global_promotion(result: dict[str, Any]) -> None:
    result["status"] = "PASS_ATTACK_FALSE_GLOBAL_TOTALITY__ZERO_CREDIT"
    result["decision"] = "SCOPED_READY_ZERO_CREDIT"
    result["intended_process_exit_code"] = 0
    result["blocking_authority_slots"] = []
    result["authority_slot_census"] = {
        "total": 9, "present": 9, "missing_or_blocking": 0}
    result["global_gate"]["full_atom_formal_receipt_present"] = True
    result["global_gate"]["C26_formal_receipt_present"] = True
    result["global_gate"]["primitive_twenty_family_totality_proved"] = True
    result["global_gate"]["decision"] = "ZERO_CREDIT_SCOPED_READY"


def promote_credit(result: dict[str, Any]) -> None:
    result["formal_credit"] = 1
    result["manifest_authorized"] = True
    result["strict_nonpromotion"]["C27_transition_totality"] = 1
    result["strict_nonpromotion"]["CM2"] = "GO"


def attack_specs() -> tuple[list[GapAttack], list[ResultAttack]]:
    slot = lambda name: (lambda row: row.get("authority_slot") == name)
    full = "FULL_101080_TO_483232_ATOM_INCIDENCE_FORMAL_RECEIPT"
    c26 = "C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_FORMAL_RECEIPT"
    union = "SEALED_SCOPED_PAIR_UNION_101080"
    gap_attacks = [
        GapAttack("full_atom_gap_falsely_closed", slot(full),
                  set_row_fields(authority_status="PRESENT_VALID", gate_blocking=False)),
        GapAttack("C26_gap_falsely_closed", slot(c26),
                  set_row_fields(authority_status="PRESENT_VALID", gate_blocking=False)),
        GapAttack("full_atom_gap_deleted", slot(full), delete_row),
        GapAttack("C26_gap_duplicated", slot(c26), duplicate_row),
        GapAttack("pair_authority_count_tampered", slot(union),
                  change_evidence(("pair_count",), 101_081)),
        GapAttack("full_atom_seed_result_promoted_to_formal", slot(full),
                  change_evidence(("seed_result_is_not_formal_authority",), False)),
        GapAttack("legacy_coarse_atom_census_restored", slot(full),
                  change_evidence(("required_exact_formal_census",
                                   "current_exact_expanded_incidences"), 197_408)),
    ]
    result_attacks = [
        ResultAttack("atom_single_terminal_constraint_restored",
                     restore_atom_single_terminal),
        ResultAttack("old_invalidated_G2A_seal_accepted", accept_invalidated_g2a),
        ResultAttack("G2A_manifest_binding_removed",
                     set_result_path(("authority_hardening",
                                      "G2A_payload_and_root_manifests_bound"), False)),
        ResultAttack("G2A_terminal_replay_binding_removed",
                     set_result_path(("authority_hardening",
                                      "G2A_terminal_replay_bound"), False)),
        ResultAttack("pair_union_no_import_binding_removed",
                     set_result_path(("authority_hardening",
                                      "pair_union_no_import_verification_bound"), False)),
        ResultAttack("pair_union_18_attack_binding_removed",
                     set_result_path(("authority_hardening",
                                      "pair_union_18_of_18_attacks_bound"), False)),
        ResultAttack("raw_pair_union_result_promoted_to_authority",
                     set_result_path(("authority_hardening",
                                      "raw_pair_union_result_alone_is_authority"), True)),
        ResultAttack("false_global_totality_promotion", false_global_promotion),
        ResultAttack("formal_credit_and_manifest_promotion", promote_credit),
        ResultAttack("C26_blocker_removed_from_result",
                     set_result_path(("blocking_authority_slots",), [
                         "FULL_101080_TO_483232_ATOM_INCIDENCE_FORMAL_RECEIPT"])),
        ResultAttack("pair_reconstruction_count_tampered",
                     set_result_path(("pair_authority_reconstruction", "pair_count"),
                                     101_081)),
    ]
    need(len(gap_attacks) + len(result_attacks) == 18, "18 attack definitions")
    return gap_attacks, result_attacks


def source_path(item: dict[str, Any]) -> Path:
    path = Path(item["path"])
    return path if path.is_absolute() else ROOT / path


def verifier_command(verifier: Path, baseline: dict[str, Any], result_path: Path,
                     result_sha: str, gap_path: Path, gap_sha: str,
                     out_path: Path, seed: int) -> list[str]:
    labels = (
        "correction_v2", "strict_volume_receipt", "lower_contact_receipt",
        "c19c_receipt", "g2a_final_receipt", "g2a_payload_manifest",
        "g2a_root_manifest", "g2a_terminal_replay", "g2a_invalidation_notice",
        "g2b_receipt", "pair_union_receipt", "pair_union_manifest",
        "pair_ownership",
    )
    attestations = baseline["root_input_capture"]["attestations"]
    answer = ["python3", str(verifier)]
    for label in labels:
        option = label.replace("_", "-")
        item = attestations[label]
        answer.extend(["--" + option, str(source_path(item)),
                       "--" + option + "-sha256", item["sha256"]])
    answer.extend([
        "--preflight-result", str(result_path),
        "--preflight-result-sha256", result_sha,
        "--gap-ledger", str(gap_path),
        "--gap-ledger-sha256", gap_sha,
        "--out-file", str(out_path), "--seed", str(seed),
    ])
    return answer


def materialize_gap(attack: GapAttack, baseline: dict[str, Any], baseline_gap: Path,
                    directory: Path) -> tuple[Path, str, Path, str]:
    result = json.loads(json.dumps(baseline))
    gap_path = directory / "authority_gap_ledger_v2.jsonl.gz"
    changed = 0

    def rows() -> Iterable[dict[str, Any]]:
        nonlocal changed
        with gzip.open(baseline_gap, "rb") as stream:
            for line in stream:
                row = json.loads(line)
                if changed == 0 and attack.predicate(row):
                    changed += 1
                    yield from attack.mutate(row)
                else:
                    yield row

    result["gap_ledger"] = write_rows(gap_path, rows())
    need(changed == 1, attack.name + ":target")
    result = reclose_result(result)
    result_path = directory / "preflight_result_v2.json"
    result_path.write_bytes(canonical(result) + b"\n")
    return result_path, file_sha(result_path), gap_path, file_sha(gap_path)


def materialize_result(attack: ResultAttack, baseline: dict[str, Any],
                       baseline_gap: Path,
                       directory: Path) -> tuple[Path, str, Path, str]:
    result = json.loads(json.dumps(baseline))
    attack.mutate(result)
    result = reclose_result(result)
    result_path = directory / "preflight_result_v2.json"
    result_path.write_bytes(canonical(result) + b"\n")
    gap_path = directory / "authority_gap_ledger_v2.jsonl.gz"
    gap_path.write_bytes(baseline_gap.read_bytes())
    return result_path, file_sha(result_path), gap_path, file_sha(gap_path)


def invoke(name: str, verifier: Path, baseline: dict[str, Any], result_path: Path,
           result_sha: str, gap_path: Path, gap_sha: str, directory: Path,
           seed: int, timeout: int, expect_success: bool) -> dict[str, Any]:
    out_path = directory / "verification.json"
    completed = subprocess.run(
        verifier_command(verifier, baseline, result_path, result_sha, gap_path,
                         gap_sha, out_path, seed), cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        timeout=timeout, check=False)
    accepted = completed.returncode == 0 and out_path.exists()
    rejected = (completed.returncode == 2
                and completed.stdout.startswith("REJECT:") and not out_path.exists())
    need(accepted if expect_success else rejected,
         name + (":control acceptance" if expect_success else ":attack rejection"))
    return {
        "attack": name,
        "mutated_preflight_result_file_sha256": result_sha,
        "mutated_gap_ledger_file_sha256": gap_sha,
        "verifier_exit_code": completed.returncode,
        "verifier_stdout": completed.stdout.strip()[:500],
        "verifier_stderr": completed.stderr.strip()[:500],
        "verification_output_created": out_path.exists(),
        "rejected": rejected,
    }


def execute(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_file)
    need(not output.exists(), "fresh attack output")
    verifier = Path(args.verifier).resolve()
    need(file_sha(verifier) == args.verifier_sha256, "verifier pin")
    baseline_path = Path(args.baseline_result).resolve()
    baseline_gap = Path(args.baseline_gap).resolve()
    baseline = load_document(baseline_path, args.baseline_result_sha256,
                             "result_sha256")
    need(file_sha(baseline_gap) == args.baseline_gap_sha256, "gap pin")
    gap_attacks, result_attacks = attack_specs()
    with tempfile.TemporaryDirectory(prefix="cm2-v5-preflight-v2-attacks-") as temp:
        root = Path(temp)
        control_dir = root / "control"
        control_dir.mkdir()
        control = invoke("unmutated_control", verifier, baseline, baseline_path,
                         args.baseline_result_sha256, baseline_gap,
                         args.baseline_gap_sha256, control_dir, args.seed,
                         args.timeout, True)
        jobs: list[tuple[str, Path, str, Path, str, Path, int]] = []
        ordinal = 1
        for attack in gap_attacks:
            directory = root / f"{ordinal:02d}-{attack.name}"
            directory.mkdir()
            result_path, result_sha, gap_path, gap_sha = materialize_gap(
                attack, baseline, baseline_gap, directory)
            jobs.append((attack.name, result_path, result_sha, gap_path, gap_sha,
                         directory, args.seed + ordinal))
            ordinal += 1
        for attack in result_attacks:
            directory = root / f"{ordinal:02d}-{attack.name}"
            directory.mkdir()
            result_path, result_sha, gap_path, gap_sha = materialize_result(
                attack, baseline, baseline_gap, directory)
            jobs.append((attack.name, result_path, result_sha, gap_path, gap_sha,
                         directory, args.seed + ordinal))
            ordinal += 1
        results: list[dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(invoke, name, verifier, baseline, result_path,
                                result_sha, gap_path, gap_sha, directory, seed,
                                args.timeout, False): name
                for name, result_path, result_sha, gap_path, gap_sha, directory,
                    seed in jobs
            }
            for future in as_completed(futures):
                results.append(future.result())
        results.sort(key=lambda item: item["attack"])
        rejected = sum(item["rejected"] for item in results)
        need(rejected == 18, "18/18 rejected")

    body = {
        "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-preflight-attacks.v2",
        "status": "PASS_CONTROL_AND_18_OF_18_COHERENT_RESIGNED_ATTACKS_REJECTED__ZERO_CREDIT",
        "attack_seed": args.seed,
        "control": control,
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
        "coverage": {
            "false_full_atom_or_C26_closure": True,
            "seed_result_as_formal_authority": True,
            "legacy_coarse_atom_census": True,
            "old_invalidated_G2A_seal": True,
            "missing_G2A_manifest_or_replay_binding": True,
            "missing_pair_union_no_import_or_attack_binding": True,
            "restored_atom_single_terminal_constraint": True,
            "global_or_credit_promotion": True,
            "gap_deletion_or_duplication": True,
            "pair_count_tamper": True,
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
        key: value for key, value in body.items() if key != "attack_seed"})
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
    print(canonical({"status": report["status"],
                     "attack_count": report["attack_count"],
                     "rejected_attack_count": report["rejected_attack_count"],
                     "attack_result_sha256":
                         report["attack_result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
