#!/usr/bin/env python3
"""Coherently re-signed attacks on the corrected T07/T08/T09 adapter.

Every attacked receipt is re-closed and receives a matching rebuilt manifest.
Four attacks also rewrite, re-close, re-compress, and re-describe a ledger.
Acceptance therefore cannot rely on stale hashes alone.
"""

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
VERIFIER = ROOT / "deliverables/cm2_c27_primitive_v5_actual_three_terminal_pair_atom_adapters_v2_independent_verifier.py"
PRODUCER = ROOT / "deliverables/cm2_c27_primitive_v5_actual_three_terminal_pair_atom_adapters_v2.py"
PRODUCER_SHA = "8b85ca7e84efde3c55ae54b6bd392de39741f29e29537c01e063cf1e697399e8"


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


def root_path(text: str) -> Path:
    path = (ROOT / text).resolve()
    need(ROOT in path.parents, "path inside workspace")
    return path


def resign(receipt: dict[str, Any]) -> dict[str, Any]:
    body = dict(receipt)
    body.pop("receipt_sha256", None)
    body["receipt_sha256"] = digest(body)
    return body


def manifest_bytes(receipt_path: Path, receipt: dict[str, Any]) -> bytes:
    lines = []
    for entry in receipt["terminal_adapters"]:
        for key in ("candidate_ownership_ledger",
                    "materialized_physical_proof_fragment_ledger"):
            desc = entry[key]
            lines.append(f"{desc['sha256']}  {desc['path']}\n")
    for key in ("atom_pair_incidence_ledger",
                "atom_incidence_disposition_ledger"):
        desc = receipt[key]
        lines.append(f"{desc['sha256']}  {desc['path']}\n")
    for item in receipt["root_input_capture"]["attestations"].values():
        lines.append(f"{item['sha256']}  {item['path']}\n")
    lines.extend((
        f"{PRODUCER_SHA}  {PRODUCER.relative_to(ROOT)}\n",
        f"{fsha(receipt_path)}  {receipt_path.relative_to(ROOT)}\n",
    ))
    return "".join(sorted(set(lines))).encode("ascii")


def write_case(case_dir: Path, receipt: dict[str, Any]) -> Path:
    case_dir.mkdir()
    receipt_path = case_dir / "adapter_receipt.json"
    receipt_path.write_bytes(canonical(receipt) + b"\n")
    (case_dir / "manifest.sha256").write_bytes(
        manifest_bytes(receipt_path, receipt))
    return receipt_path


def mutate_ledger(source: Path, destination: Path,
                  mutate: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    count = 0
    sequence = hashlib.sha256()
    changed = False
    with destination.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as out:
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
    need(changed, "ledger attack changed a row")
    return {"path": str(destination.relative_to(ROOT)),
            "size": destination.stat().st_size, "sha256": fsha(destination),
            "row_count": count, "row_sequence_sha256": sequence.hexdigest()}


def run_verifier(receipt: Path, second: Path, output: Path) -> tuple[int, str]:
    command = ["python", "-B", str(VERIFIER), "--receipt", str(receipt),
               "--second-receipt", str(second), "--output", str(output)]
    completed = subprocess.run(command, cwd=ROOT, text=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, check=False)
    return completed.returncode, completed.stdout.strip()


def build(args: argparse.Namespace) -> dict[str, Any]:
    base_path = Path(args.receipt).resolve()
    second_path = Path(args.second_receipt).resolve()
    output = Path(args.out_dir).resolve()
    need(not output.exists(), "fresh output")
    output.mkdir(parents=True)
    base = json.loads(base_path.read_bytes())
    body = dict(base)
    claim = body.pop("receipt_sha256")
    need(claim == digest(body), "base receipt closure")
    need(fsha(VERIFIER) == args.verifier_sha256, "verifier source pin")
    need(fsha(PRODUCER) == PRODUCER_SHA, "producer source pin")

    structural: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("candidate_count_conflated_with_incidences",
         lambda r: r["exact_census"].__setitem__("candidate_pair_count", 206_632)),
        ("incidence_count_conflated_with_candidates",
         lambda r: r["exact_census"].__setitem__("atom_pair_incidence_count", 101_080)),
        ("complement_count_forged",
         lambda r: r["exact_census"].__setitem__("exact_complement_atoms", 420_992)),
        ("multi_terminal_atoms_suppressed",
         lambda r: r["exact_census"].__setitem__("multi_terminal_atoms", 0)),
        ("physical_proof_count_forged",
         lambda r: r["exact_census"].__setitem__("physical_proof_row_count", 32_607)),
        ("edge_count_forged",
         lambda r: r["exact_census"].__setitem__("unique_component_edges", 14_772)),
        ("terminal_candidate_census_forged",
         lambda r: r["exact_census"]["terminal_candidate_pair_census"].__setitem__("SIGNED_BOUNDARY_FACES", 25_453)),
        ("incidence_terminal_census_forged",
         lambda r: r["exact_census"]["atom_pair_incidence_terminal_census"].__setitem__("SIGNED_BOUNDARY_FACES", 55_535)),
        ("formal_credit_promoted", lambda r: r.__setitem__("formal_credit", 1)),
        ("manifest_authorized", lambda r: r.__setitem__("manifest_authorized", True)),
        ("candidate_separation_closure_false",
         lambda r: r["separation_closures"].__setitem__("candidate_ownership_count_is_101080_not_206632", False)),
        ("incidence_separation_closure_false",
         lambda r: r["separation_closures"].__setitem__("atom_pair_incidence_never_counted_as_candidate", False)),
        ("superseded_v1_consumed",
         lambda r: r["forbidden_input_governance"].__setitem__("superseded_v1_adapter_consumed", True)),
        ("producer_source_pin_forged",
         lambda r: r.__setitem__("producer_source_sha256", "0" * 64)),
        ("pair_authority_input_pin_forged",
         lambda r: r["root_input_capture"]["attestations"]["pair_ownership"].__setitem__("sha256", "0" * 64)),
        ("candidate_descriptor_v1_schema",
         lambda r: r["terminal_adapters"][0]["candidate_ownership_ledger"].__setitem__("row_schema", "cm2.invalid.v1")),
        ("incidence_unique_key_conflated",
         lambda r: r["atom_pair_incidence_ledger"].__setitem__("unique_key", "candidate_key")),
        ("disposition_descriptor_count_forged",
         lambda r: r["atom_incidence_disposition_ledger"].__setitem__("row_count", 483_231)),
    ]
    outcomes = []
    for index, (name, mutate) in enumerate(structural, 1):
        case_dir = output / f"attack_{index:02d}_{name}"
        attacked = deepcopy(base)
        mutate(attacked)
        attacked = resign(attacked)
        receipt_path = write_case(case_dir, attacked)
        exit_code, stdout = run_verifier(
            receipt_path, second_path, case_dir / "unexpected_verification.json")
        rejected = exit_code == 2 and stdout.startswith("REJECT:")
        need(rejected, "structural attack not rejected:" + name)
        outcomes.append({"attack": name, "coherently_resigned": True,
                         "ledger_reclosed": False, "exit_code": exit_code,
                         "rejected": rejected, "diagnostic": stdout[:300]})

    # Deep row attacks update row closure, gzip bytes, descriptor, receipt
    # closure, and manifest.  They test inverse semantics rather than a stale
    # digest detector.
    deep = [
        ("candidate_kind_row_forged", "candidate",
         lambda row: row.__setitem__("candidate_kind", "ATOM_PAIR_INCIDENCE_FORBIDDEN")),
        ("physical_proof_edge_row_forged", "proof",
         lambda row: row.__setitem__("component_edge_key", "round306c27r2-v5-component-edge:" + "0" * 64)),
        ("incidence_owner_binding_row_forged", "incidence",
         lambda row: row.__setitem__("candidate_owner_row_sha256", "0" * 64)),
        ("atom_disposition_row_forged", "disposition",
         lambda row: row.__setitem__("disposition", "EXACT_NONEMPTY_ATOM_PAIR_INCIDENCE_SET")),
    ]
    for offset, (name, kind, mutate_row) in enumerate(deep, len(structural) + 1):
        case_dir = output / f"attack_{offset:02d}_{name}"
        case_dir.mkdir()
        attacked = deepcopy(base)
        if kind == "candidate":
            desc = attacked["terminal_adapters"][0]["candidate_ownership_ledger"]
        elif kind == "proof":
            desc = attacked["terminal_adapters"][2]["materialized_physical_proof_fragment_ledger"]
        elif kind == "incidence":
            desc = attacked["atom_pair_incidence_ledger"]
        else:
            desc = attacked["atom_incidence_disposition_ledger"]
        source = root_path(desc["path"])
        destination = case_dir / source.name
        replacement = mutate_ledger(source, destination, mutate_row)
        desc.update(replacement)
        attacked = resign(attacked)
        receipt_path = case_dir / "adapter_receipt.json"
        receipt_path.write_bytes(canonical(attacked) + b"\n")
        (case_dir / "manifest.sha256").write_bytes(
            manifest_bytes(receipt_path, attacked))
        exit_code, stdout = run_verifier(
            receipt_path, second_path, case_dir / "unexpected_verification.json")
        rejected = exit_code == 2 and stdout.startswith("REJECT:")
        need(rejected, "deep attack not rejected:" + name)
        outcomes.append({"attack": name, "coherently_resigned": True,
                         "ledger_reclosed": True, "exit_code": exit_code,
                         "rejected": rejected, "diagnostic": stdout[:300]})

    stable = {"attack_count": len(outcomes),
              "coherently_resigned_attack_count": len(outcomes),
              "row_reclosed_attack_count": len(deep),
              "rejected_count": sum(item["rejected"] for item in outcomes)}
    result_body = {
        "schema": "cm2.c27-independent.primitive-v5-actual-three-terminal-pair-atom-adapters-v2-coherent-attack-result.v1",
        "status": "PASS_ALL_COHERENTLY_RESIGNED_CONFLATION_AND_ROW_ATTACKS_REJECTED__ZERO_CREDIT",
        "base_receipt_file_sha256": fsha(base_path),
        "base_receipt_object_sha256": base["receipt_sha256"],
        "verifier_source_sha256": args.verifier_sha256,
        "census": stable, "outcomes": outcomes,
        "formal_credit": 0, "manifest_authorized": False,
        "C27_C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(result_body)
    result["attack_result_sha256"] = digest(result)
    (output / "attack_result.json").write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--second-receipt", required=True)
    parser.add_argument("--verifier-sha256", required=True)
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
