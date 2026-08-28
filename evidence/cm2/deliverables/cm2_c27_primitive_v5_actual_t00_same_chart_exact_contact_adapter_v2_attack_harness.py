#!/usr/bin/env python3
"""Coherently re-signed structural and row attacks for T00 corrected-v2."""

from __future__ import annotations

import argparse
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
PRODUCER = ROOT / "deliverables/cm2_c27_primitive_v5_actual_t00_same_chart_exact_contact_adapter_v2.py"
PRODUCER_SHA = "27b1a0e0eef9d71070a5925a40b3a2d4e33608437545fde2e4ec2ad9013f4e66"
VERIFIER = ROOT / "deliverables/cm2_c27_primitive_v5_actual_t00_same_chart_exact_contact_adapter_v2_independent_verifier.py"
VERIFIER_SHA = "775ddcebebc8758d2fe70a28e0c34c02767d65f4f01235898396eeca92a2731b"


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


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def root_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    need(ROOT in path.parents, "path inside workspace")
    return path


def resign(row: dict[str, Any], closure: str) -> dict[str, Any]:
    body = dict(row)
    body.pop(closure, None)
    body[closure] = digest(body)
    return body


def manifest_bytes(receipt_path: Path, receipt: dict[str, Any]) -> bytes:
    lines = []
    for key in ("primitive_authority_ledger", "candidate_ownership_ledger",
                "materialized_physical_proof_fragment_ledger"):
        desc = receipt["terminal_adapter"][key]
        lines.append(f"{desc['sha256']}  {desc['path']}\n")
    for item in receipt["root_input_capture"]["attestations"].values():
        lines.append(f"{item['sha256']}  {item['path']}\n")
    lines.extend((f"{PRODUCER_SHA}  {PRODUCER.relative_to(ROOT)}\n",
                  f"{fsha(receipt_path)}  {receipt_path.relative_to(ROOT)}\n"))
    return "".join(sorted(set(lines))).encode("ascii")


def write_receipt(case_dir: Path, receipt: dict[str, Any]) -> Path:
    case_dir.mkdir(parents=True)
    path = case_dir / "adapter_receipt.json"
    path.write_bytes(canonical(receipt) + b"\n")
    (case_dir / "manifest.sha256").write_bytes(manifest_bytes(path, receipt))
    return path


def rewrite_run(base_run: dict[str, Any], receipt_path: Path,
                receipt: dict[str, Any], destination: Path) -> Path:
    row = deepcopy(base_run)
    row["run"]["receipt_file_sha256"] = fsha(receipt_path)
    row["run"]["receipt_object_sha256"] = receipt["receipt_sha256"]
    row = resign(row, "run_attestation_sha256")
    destination.write_bytes(canonical(row) + b"\n")
    return destination


def mutate_ledger(source: Path, destination: Path,
                  mutate: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    count = 0
    sequence = hashlib.sha256()
    changed = False
    with destination.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw,
                           mtime=0, compresslevel=1) as out:
            with gzip.open(source, "rb") as stream:
                for line in stream:
                    row = json.loads(line)
                    if not changed:
                        body = dict(row)
                        body.pop("row_sha256")
                        mutate(body)
                        row = {**body, "row_sha256": digest(body)}
                        changed = True
                    out.write(canonical(row) + b"\n")
                    sequence.update(row["row_sha256"].encode("ascii") + b"\n")
                    count += 1
    need(changed, "row attack changed ledger")
    return {"path": str(destination.relative_to(ROOT)),
            "size": destination.stat().st_size, "sha256": fsha(destination),
            "row_count": count, "row_sequence_sha256": sequence.hexdigest()}


def run_verifier(receipt: Path, second: Path, run1: Path, run2: Path,
                 case_dir: Path) -> tuple[int, str]:
    command = ["/usr/bin/python3.12", "-B", str(VERIFIER),
               "--receipt", str(receipt), "--second-receipt", str(second),
               "--run-attestation", str(run1),
               "--second-run-attestation", str(run2),
               "--temporary-db", str(case_dir / "temporary.sqlite"),
               "--output", str(case_dir / "unexpected_verification.json")]
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, check=False)
    return result.returncode, result.stdout.strip()


def build(args: argparse.Namespace) -> dict[str, Any]:
    receipt_path = Path(args.receipt).resolve()
    second_path = Path(args.second_receipt).resolve()
    run_path = Path(args.run_attestation).resolve()
    second_run_path = Path(args.second_run_attestation).resolve()
    output = Path(args.out_dir).resolve()
    need(not output.exists(), "fresh attack output")
    need(fsha(PRODUCER) == PRODUCER_SHA and fsha(VERIFIER) == VERIFIER_SHA,
         "source pins")
    base = json.loads(receipt_path.read_bytes())
    second_base = json.loads(second_path.read_bytes())
    base_run = json.loads(run_path.read_bytes())
    second_run = json.loads(second_run_path.read_bytes())
    for row, closure in ((base, "receipt_sha256"),
                         (second_base, "receipt_sha256"),
                         (base_run, "run_attestation_sha256"),
                         (second_run, "run_attestation_sha256")):
        body = dict(row)
        claim = body.pop(closure)
        need(claim == digest(body), "base closure:" + closure)
    output.mkdir(parents=True)

    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("old_t00_slot_name",
         lambda r: r["terminal_adapter"].__setitem__("authority_slot", "T00_SAME_CHART_PRIMITIVE_EXACT_CONTACT")),
        ("wrong_terminal",
         lambda r: r["terminal_adapter"].__setitem__("terminal", "SIGNED_BOUNDARY_FACES")),
        ("candidate_count_minus_one",
         lambda r: r["exact_census"].__setitem__("candidate_count", 5_970_839)),
        ("lower_cross_missing_one_million",
         lambda r: r["exact_census"].__setitem__("lower_cross_component_candidate_count", 1_598_666)),
        ("lower_same_forged",
         lambda r: r["exact_census"].__setitem__("lower_same_component_candidate_count", 3_185_041)),
        ("lower_total_forged",
         lambda r: r["exact_census"].__setitem__("lower_dimension0_1_2_candidate_count", 5_783_707)),
        ("strict_total_forged",
         lambda r: r["exact_census"].__setitem__("strict_dimension3_candidate_count", 187_131)),
        ("fully_open_rejection_forged",
         lambda r: r["exact_census"].__setitem__("lower_fully_open_rejection_count", 5_707_707)),
        ("c19c_rejection_forged",
         lambda r: r["exact_census"].__setitem__("lower_C19C_endpoint_dependent_rejection_count", 75_999)),
        ("proof_count_forged",
         lambda r: r["exact_census"].__setitem__("strict_cross_component_physical_proof_count", 32_239)),
        ("scoped_edge_count_confused_for_strict",
         lambda r: r["exact_census"].__setitem__("unique_component_edge_count", 14_724)),
        ("lower_no_edge_disposition_forged",
         lambda r: r["exact_census"]["candidate_component_disposition_census"].__setitem__("NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS", 5_783_707)),
        ("formal_credit_promoted", lambda r: r.__setitem__("formal_credit", 1)),
        ("manifest_authorized", lambda r: r.__setitem__("manifest_authorized", True)),
        ("c26_adds_candidates",
         lambda r: r["authority_closures"].__setitem__("C26_691424_is_absence_coverage_theorem_not_candidate_rows", False)),
        ("g2a_adds_candidates",
         lambda r: r["authority_closures"].__setitem__("G2A_G2B_alias_adds_no_T00_candidate", False)),
        ("old_c27_consumed",
         lambda r: r["forbidden_input_governance"].__setitem__("old_C27_FAMILIES_imported_or_read", True)),
        ("candidate_v1_schema",
         lambda r: r["terminal_adapter"]["candidate_ownership_ledger"].__setitem__("row_schema", "cm2.invalid.v1")),
        ("proof_descriptor_count_forged",
         lambda r: r["terminal_adapter"]["materialized_physical_proof_fragment_ledger"].__setitem__("row_count", 32_241)),
        ("authority_descriptor_count_forged",
         lambda r: r["terminal_adapter"]["primitive_authority_ledger"].__setitem__("row_count", 5_970_839)),
    ]
    outcomes = []
    for index, (name, mutate) in enumerate(attacks, 1):
        case = output / f"attack_{index:02d}_{name}"
        attacked = deepcopy(base)
        mutate(attacked)
        attacked = resign(attacked, "receipt_sha256")
        test_receipt = write_receipt(case, attacked)
        test_run = rewrite_run(base_run, test_receipt, attacked,
                               case / "run_attestation.json")
        code, stdout = run_verifier(test_receipt, second_path, test_run,
                                    second_run_path, case)
        rejected = code == 2 and stdout.startswith("REJECT:")
        need(rejected, "structural attack accepted:" + name)
        outcomes.append({"attack": name, "coherently_resigned": True,
                         "row_reclosed": False, "exit_code": code,
                         "rejected": rejected, "diagnostic": stdout[:300]})

    row_attacks = [
        ("candidate_kind_row_forged", "candidate_ownership_ledger",
         lambda row: row.__setitem__("candidate_kind", "ATOM_PAIR_INCIDENCE_FORBIDDEN")),
        ("proof_old_slot_row_forged", "materialized_physical_proof_fragment_ledger",
         lambda row: row.__setitem__("authority_slot", "T00_SAME_CHART_PRIMITIVE_EXACT_CONTACT")),
    ]
    for offset, (name, descriptor_key, mutator) in enumerate(
            row_attacks, len(attacks) + 1):
        case = output / f"attack_{offset:02d}_{name}"
        case.mkdir()
        attacked1, attacked2 = deepcopy(base), deepcopy(second_base)
        source_desc = attacked1["terminal_adapter"][descriptor_key]
        mutated_path = case / Path(source_desc["path"]).name
        replacement = mutate_ledger(root_path(source_desc["path"]),
                                    mutated_path, mutator)
        for attacked in (attacked1, attacked2):
            attacked["terminal_adapter"][descriptor_key].update(replacement)
        attacked1 = resign(attacked1, "receipt_sha256")
        attacked2 = resign(attacked2, "receipt_sha256")
        test1 = write_receipt(case / "seed1", attacked1)
        test2 = write_receipt(case / "seed2", attacked2)
        run1 = rewrite_run(base_run, test1, attacked1,
                           case / "seed1_run_attestation.json")
        run2 = rewrite_run(second_run, test2, attacked2,
                           case / "seed2_run_attestation.json")
        code, stdout = run_verifier(test1, test2, run1, run2, case)
        rejected = code == 2 and stdout.startswith("REJECT:")
        need(rejected, "row attack accepted:" + name)
        outcomes.append({"attack": name, "coherently_resigned": True,
                         "row_reclosed": True, "exit_code": code,
                         "rejected": rejected, "diagnostic": stdout[:300]})

    census = {"attack_count": len(outcomes),
              "coherently_resigned_attack_count": len(outcomes),
              "row_reclosed_attack_count": len(row_attacks),
              "rejected_count": sum(item["rejected"] for item in outcomes)}
    body = {
        "schema": "cm2.c27-independent.primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-coherent-attack-result.v1",
        "status": "PASS_ALL_T00_COUNT_SLOT_CONFLATION_AND_ROW_ATTACKS_REJECTED__ZERO_CREDIT",
        "base_receipt_file_sha256": fsha(receipt_path),
        "base_receipt_object_sha256": base["receipt_sha256"],
        "verifier_source_sha256": VERIFIER_SHA,
        "census": census, "outcomes": outcomes,
        "formal_credit": 0, "manifest_authorized": False,
        "C27_C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
    result = dict(body)
    result["attack_result_sha256"] = digest(result)
    (output / "attack_result.json").write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--second-receipt", required=True)
    parser.add_argument("--run-attestation", required=True)
    parser.add_argument("--second-run-attestation", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    try:
        result = build(args)
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"], "census": result["census"],
                     "attack_result_sha256": result["attack_result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
