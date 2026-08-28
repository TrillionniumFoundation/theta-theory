#!/usr/bin/env python3
"""Coherent re-signed attacks on the T11--T19 native authority roles."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
VERIFIER = ROOT / "deliverables/cm2_c27_t11_t19_atlas_control_alias_authority_independent_verifier_v1.py"
CANDIDATES = "t11_t19_atlas_seam_candidate_ownership.jsonl.gz"
PROOFS = "t11_t18_auxiliary_proof_rows.jsonl.gz"
SLOTS = "t11_t19_slot_authority.jsonl.gz"


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def dig(value: Any) -> str: return hashlib.sha256(enc(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20): state.update(block)
    return state.hexdigest()


def seq(rows: list[dict[str, Any]]) -> str:
    return dig([row["row_sha256"] for row in rows])


def load(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as stream:
        return [json.loads(line) for line in stream]


def write(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            for row in rows: zipped.write(enc(row) + b"\n")


def close_sort(rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    rows.sort(key=lambda row: tuple(str(row[field]) for field in fields))
    for ordinal, row in enumerate(rows):
        row["ordinal"] = ordinal; row.pop("row_sha256", None)
        row["row_sha256"] = dig(row)


def mutate(directory: Path, name: str,
           edit: Callable[[list[dict[str, Any]]], None]) -> None:
    path = directory / name; rows = load(path); edit(rows); write(path, rows)


def resign(directory: Path, result: dict[str, Any], sync_slots: bool = True) -> None:
    candidates = load(directory / CANDIDATES)
    proofs = load(directory / PROOFS)
    slots = load(directory / SLOTS)
    close_sort(candidates, ("terminal", "candidate_key"))
    close_sort(proofs, ("terminal", "proof_key"))
    if sync_slots:
        candidate_counts = {}
        for row in candidates:
            candidate_counts[row["terminal"]] = candidate_counts.get(row["terminal"], 0) + 1
        proof_counts = {}
        for row in proofs:
            proof_counts[row["terminal"]] = proof_counts.get(row["terminal"], 0) + 1
        for row in slots:
            row["candidate_count"] = candidate_counts.get(row["terminal"], 0)
            row["authority_row_count"] = (276 if row["slot"] == "T19"
                                             else candidate_counts.get(row["terminal"], 0)
                                             + proof_counts.get(row["terminal"], 0))
    close_sort(slots, ("slot",))
    for path, rows in ((directory / CANDIDATES, candidates),
                       (directory / PROOFS, proofs),
                       (directory / SLOTS, slots)):
        write(path, rows)
        descriptor = result["ledgers"][path.name]
        descriptor["row_count"] = len(rows)
        descriptor["file_sha256"] = fsha(path)
        descriptor["row_sequence_sha256"] = seq(rows)
    result["candidate_ownership_total"] = len(candidates)
    result["local_auxiliary_proof_row_total_T11_T18"] = len(proofs)
    result["total_proof_only_authority_rows"] = len(proofs) + 276
    result["slot_census"] = {
        row["slot"]: {"terminal": row["terminal"], "role": row["role"],
                      "candidate_count": row["candidate_count"],
                      "authority_row_count": row["authority_row_count"]}
        for row in slots}
    result.pop("result_sha256", None); result["result_sha256"] = dig(result)
    (directory / "result.json").write_bytes(enc(result) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    baseline = Path(args.baseline).resolve()
    baseline_result = json.loads((baseline / "result.json").read_bytes())
    attacks: list[tuple[str, Callable[[Path, dict[str, Any]], None], bool]] = []

    def add(name: str, edit: Callable[[Path, dict[str, Any]], None],
            sync_slots: bool = True) -> None:
        attacks.append((name, edit, sync_slots))

    def seam(field: str, value: Any):
        return lambda d, r: mutate(d, CANDIDATES,
                                   lambda rows: rows[0].__setitem__(field, value))

    def reverse(field: str, value: Any):
        def edit(directory: Path, result: dict[str, Any]) -> None:
            def row_edit(rows: list[dict[str, Any]]) -> None:
                next(row for row in rows if row["terminal"] == "REVERSE_RECHART")[field] = value
            mutate(directory, PROOFS, row_edit)
        return edit

    def control(field: str, value: Any):
        def edit(directory: Path, result: dict[str, Any]) -> None:
            def row_edit(rows: list[dict[str, Any]]) -> None:
                next(row for row in rows if "NEGATIVE_CONTROL" in row["terminal"])[field] = value
            mutate(directory, PROOFS, row_edit)
        return edit

    add("drop_seam_candidate", lambda d, r: mutate(d, CANDIDATES, lambda rows: rows.pop(0)))
    add("duplicate_seam_candidate", lambda d, r: mutate(
        d, CANDIDATES, lambda rows: rows.append(copy.deepcopy(rows[0]))))
    add("seam_terminal", seam("terminal", "REVERSE_RECHART"))
    add("seam_chart_pair", seam("forward_chart_pair", ["E", "W"]))
    add("seam_faces", seam("forward_faces", ["-kappa", "+kappa"]))
    add("seam_source_pin", seam("source_seam_body_sha256", "0" * 64))
    add("seam_namespace", seam("candidate_key_namespace", "ATLAS_REVERSE_PROOF_ONLY"))
    add("seam_formal_credit", seam("formal_credit", 1))
    add("drop_reverse_proof", lambda d, r: mutate(
        d, PROOFS, lambda rows: rows.remove(next(row for row in rows
                                                 if row["terminal"] == "REVERSE_RECHART"))))
    add("duplicate_reverse_proof", lambda d, r: mutate(
        d, PROOFS, lambda rows: rows.append(copy.deepcopy(next(
            row for row in rows if row["terminal"] == "REVERSE_RECHART")))))
    add("reverse_chart_pair", reverse("reverse_chart_pair", ["W", "E"]))
    add("reverse_inverse_flag", reverse("inverse_of_exact_bijective_phase_glue", False))
    add("reverse_forward_candidate_link", reverse("forward_candidate_id", "forged-candidate"))
    add("control_action", control("action", "identity"))
    add("control_source_member", control("source_sheet_member_id", "forged-member"))
    add("control_p_zero", control("p_zero_in_open_interval", True))
    add("control_decisive_fact", control("decisive_empty_fixed_set_fact", "FORGED"))
    add("control_fixed_count", control("fixed_sheet_point_family_count", 1))
    add("control_quotient_flag", control("physical_action_is_quotient_identification", True))
    add("control_candidate_flag", control("independent_terminal_candidate", True))
    add("slot_role", lambda d, r: mutate(
        d, SLOTS, lambda rows: rows[0].__setitem__("role", "CANDIDATE_OWNERSHIP")), False)
    add("slot_namespace", lambda d, r: mutate(
        d, SLOTS, lambda rows: rows[0].__setitem__("candidate_key_namespace", "ATLAS_FORWARD_SEAM")), False)
    add("source_W_promotion", lambda d, r: r.__setitem__("source_W_transition_authorized", True))
    add("global_totality_promotion", lambda d, r: r.__setitem__(
        "global_atom_and_full_twenty_family_totality_closed", True))
    if len(attacks) != 24: raise RuntimeError("attack census")

    results = []
    with tempfile.TemporaryDirectory(prefix="cm2-t11-t19-authority-attacks-") as temp:
        root = Path(temp)
        for ordinal, (name, edit, sync_slots) in enumerate(attacks):
            directory = root / f"attack-{ordinal:02d}"
            shutil.copytree(baseline, directory)
            result = copy.deepcopy(baseline_result)
            edit(directory, result); resign(directory, result, sync_slots)
            verification = directory / "attack_verification.json"
            process = subprocess.run(
                [sys.executable, "-I", "-B", str(VERIFIER),
                 "--candidate-dir", str(directory), "--output", str(verification)],
                cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            rejected = process.returncode == 2 and process.stderr == b""
            results.append({"ordinal": ordinal, "attack": name,
                            "rejected": rejected, "numeric_exit": process.returncode,
                            "stderr_empty": process.stderr == b"",
                            "stdout_sha256": hashlib.sha256(process.stdout).hexdigest()})
            if not rejected:
                raise RuntimeError(f"not rejected:{name}:{process.stdout!r}:{process.stderr!r}")
    body = {"schema": "cm2.c27-independent.t11-t19.atlas-control-alias-authority.coherent-attacks.v1",
            "status": "PASS_24_OF_24_COHERENT_RESIGNED_AUTHORITY_ATTACKS_REJECTED__ZERO_CREDIT",
            "attack_count": 24, "all_rejected": True, "attacks": results,
            "baseline_result_file_sha256": fsha(baseline / "result.json"),
            "verifier_file_sha256": fsha(VERIFIER),
            "formal_credit": 0, "manifest_authorized": False,
            "source_W_transition_authorized": False,
            "global_atom_and_full_twenty_family_totality_closed": False}
    value = {**body, "attack_result_sha256": dig(body)}
    output = Path(args.output)
    if output.exists(): raise RuntimeError("fresh output required")
    output.write_bytes(enc(value) + b"\n")
    print(enc({"status": value["status"],
               "attack_result_sha256": value["attack_result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__": raise SystemExit(main())
