#!/usr/bin/env python3
"""Coherent re-signed attacks on the T11--T19 common-v2 adapter."""

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
VERIFIER = ROOT / "deliverables/cm2_c27_t11_t19_common_v2_adapter_independent_verifier_v1.py"


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
    state = hashlib.sha256()
    for row in rows: state.update(row["row_sha256"].encode("ascii") + b"\n")
    return state.hexdigest()


def load(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as stream:
        return [json.loads(line) for line in stream]


def write(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            for row in rows: zipped.write(enc(row) + b"\n")


def close_rows(rows: list[dict[str, Any]]) -> None:
    for ordinal, row in enumerate(rows):
        row["ordinal"] = ordinal
        row.pop("row_sha256", None)
        row["row_sha256"] = dig(row)


def mutate_rows(directory: Path, slot: str, kind: str,
                edit: Callable[[list[dict[str, Any]]], None]) -> None:
    name = ("candidate_ownership.jsonl.gz" if kind == "candidate"
            else "materialized_physical_proof_join.jsonl.gz")
    path = directory / slot / name
    rows = load(path); edit(rows); write(path, rows)


def resign(directory: Path, result: dict[str, Any], sync: bool = True) -> None:
    candidate_total = proof_total = 0
    relation = {}
    for entry in result["adapter_entries"]:
        candidate_path = directory / entry["candidate_ownership_ledger"]["path"]
        proof_path = directory / entry["materialized_physical_proof_join_ledger"]["path"]
        candidates = load(candidate_path); proofs = load(proof_path)
        close_rows(proofs)
        if sync:
            by_candidate = {}
            for proof in proofs:
                by_candidate.setdefault(proof["candidate_key"], []).append(proof)
            for candidate in candidates:
                owned = by_candidate.get(candidate["candidate_key"], [])
                candidate["physical_proof_row_count"] = len(owned)
                candidate["physical_proof_row_sequence_sha256"] = seq(owned)
        close_rows(candidates); write(candidate_path, candidates); write(proof_path, proofs)
        for path, rows, key in (
                (candidate_path, candidates, "candidate_ownership_ledger"),
                (proof_path, proofs, "materialized_physical_proof_join_ledger")):
            descriptor = entry[key]
            descriptor["row_count"] = len(rows)
            descriptor["file_size"] = path.stat().st_size
            descriptor["file_sha256"] = fsha(path)
            descriptor["row_sequence_sha256"] = seq(rows)
        entry["native_candidate_count"] = len(candidates)
        entry["semantic_incidences_promoted_to_physical_proof_count"] = len(proofs)
        candidate_total += len(candidates); proof_total += len(proofs)
        for candidate in candidates:
            disposition = candidate["component_relation_disposition"]
            relation[disposition] = relation.get(disposition, 0) + 1
    result["candidate_total"] = candidate_total
    result["materialized_physical_proof_join_total"] = proof_total
    result["component_relation_disposition_census"] = dict(sorted(relation.items()))
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
            sync: bool = True) -> None:
        attacks.append((name, edit, sync))

    def candidate_field(field: str, value: Any):
        return lambda directory, result: mutate_rows(
            directory, "T12_TRUE_CYCLIC_SEAM_E_TO_N", "candidate",
            lambda rows: rows[0].__setitem__(field, value))

    add("drop_forward_seam_candidate", lambda d, r: mutate_rows(
        d, "T12_TRUE_CYCLIC_SEAM_E_TO_N", "candidate", lambda rows: rows.pop()))
    add("duplicate_forward_seam_candidate", lambda d, r: mutate_rows(
        d, "T13_TRUE_CYCLIC_SEAM_N_TO_W", "candidate",
        lambda rows: rows.append(copy.deepcopy(rows[0]))))
    add("inject_reverse_candidate", lambda d, r: mutate_rows(
        d, "T11_REVERSE_RECHART", "candidate",
        lambda rows: rows.append(copy.deepcopy(load(
            d / "T12_TRUE_CYCLIC_SEAM_E_TO_N/candidate_ownership.jsonl.gz")[0]))))
    add("inject_negative_control_candidate", lambda d, r: mutate_rows(
        d, "T16_Jx_NEGATIVE_CONTROL", "candidate",
        lambda rows: rows.append(copy.deepcopy(load(
            d / "T12_TRUE_CYCLIC_SEAM_E_TO_N/candidate_ownership.jsonl.gz")[0]))))
    add("inject_alias_candidate", lambda d, r: mutate_rows(
        d, "T19_REPRESENTATION_ALIASES", "candidate",
        lambda rows: rows.append(copy.deepcopy(load(
            d / "T12_TRUE_CYCLIC_SEAM_E_TO_N/candidate_ownership.jsonl.gz")[0]))))
    add("candidate_kind", candidate_field("candidate_kind", "FORGED_KIND"))
    add("candidate_pair_nonnull", candidate_field("candidate_pair_key_or_null", "forged-pair"))
    add("terminal_ordinal", candidate_field("terminal_ordinal", 11))
    add("terminal", candidate_field("terminal", "REVERSE_RECHART"))
    add("authority_slot", candidate_field("authority_slot", "T11_REVERSE_RECHART"))
    add("primitive_authority_pin", candidate_field("primitive_authority_row_sha256", "0" * 64))
    add("component_relation_cross", candidate_field(
        "component_relation_disposition", "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED"))
    add("candidate_proof_count", candidate_field("physical_proof_row_count", 1), False)
    add("candidate_proof_sequence", candidate_field("physical_proof_row_sequence_sha256", "0" * 64), False)
    add("candidate_formal_credit", candidate_field("formal_credit", 1))

    def inject_physical_proof(directory: Path, result: dict[str, Any]) -> None:
        candidate = load(directory / "T12_TRUE_CYCLIC_SEAM_E_TO_N/candidate_ownership.jsonl.gz")[0]
        body = {"schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2",
                "ordinal": 0, "proof_row_key": "forged-seam-physical-proof",
                "candidate_key": candidate["candidate_key"],
                "atom_pair_incidence_key_or_null": None,
                "terminal": candidate["terminal"], "authority_slot": candidate["authority_slot"],
                "primitive_authority_row_sha256": candidate["primitive_authority_row_sha256"],
                "ordered_C15_member_pair": ["forged-member-a", "forged-member-b"],
                "ordered_C15_component_pair": ["forged-component-a", "forged-component-b"],
                "component_edge_key": "round306c27r2-v5-component-edge:" + "0" * 64,
                "physical_witness_key": "forged-seam-witness", "formal_credit": 0}
        mutate_rows(directory, "T12_TRUE_CYCLIC_SEAM_E_TO_N", "proof",
                    lambda rows: rows.append({**body, "row_sha256": dig(body)}))

    add("promote_auxiliary_as_physical_proof", inject_physical_proof)
    add("auxiliary_total", lambda d, r: r.__setitem__("auxiliary_authority_row_total", 327))
    add("auxiliary_not_physical_flag", lambda d, r: r.__setitem__(
        "auxiliary_authority_is_not_materialized_physical_proof", False))
    add("reverse_control_alias_candidate_count", lambda d, r: r.__setitem__(
        "reverse_control_alias_independent_candidate_count", 1))
    add("source_W_promotion", lambda d, r: r.__setitem__("source_W_transition_authorized", True))
    add("global_totality_promotion", lambda d, r: r.__setitem__(
        "global_atom_and_full_twenty_family_totality_closed", True))
    add("formal_credit_promotion", lambda d, r: r.__setitem__("formal_credit", 1))
    add("manifest_authorization", lambda d, r: r.__setitem__("manifest_authorized", True))
    add("old_families_import_flag", lambda d, r: r.__setitem__("old_C27_FAMILIES_imported_or_read", True))
    need_count = 24
    if len(attacks) != need_count:
        raise RuntimeError(f"attack census:{len(attacks)}")

    results = []
    with tempfile.TemporaryDirectory(prefix="cm2-t11-t19-common-v2-attacks-") as temp:
        root = Path(temp)
        for ordinal, (name, edit, sync) in enumerate(attacks):
            directory = root / f"attack-{ordinal:02d}"
            shutil.copytree(baseline, directory)
            result = copy.deepcopy(baseline_result)
            edit(directory, result); resign(directory, result, sync)
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
    body = {
        "schema": "cm2.c27-independent.t11-t19.common-v2-adapter.coherent-attacks.v1",
        "status": "PASS_24_OF_24_COHERENT_RESIGNED_ATTACKS_REJECTED__AUXILIARY_NOT_PROMOTED__ZERO_CREDIT",
        "attack_count": 24, "all_rejected": True, "attacks": results,
        "baseline_result_file_sha256": fsha(baseline / "result.json"),
        "verifier_file_sha256": fsha(VERIFIER),
        "formal_credit": 0, "manifest_authorized": False,
        "source_W_transition_authorized": False,
        "global_atom_and_full_twenty_family_totality_closed": False,
    }
    value = {**body, "attack_result_sha256": dig(body)}
    output = Path(args.output)
    if output.exists(): raise RuntimeError("fresh output required")
    output.write_bytes(enc(value) + b"\n")
    print(enc({"status": value["status"],
               "attack_result_sha256": value["attack_result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__": raise SystemExit(main())
