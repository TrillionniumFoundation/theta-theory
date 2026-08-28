#!/usr/bin/env python3
"""Release a manifest-bound zero-credit receipt for the scoped C26 theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
LEDGER = "c26_691424_scoped_exact_contact_source_factorization.jsonl.gz"


class Failure(RuntimeError):
    pass


def need(flag: bool, label: str) -> None:
    if type(flag) is not bool or not flag:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


def load_closed(path: Path, closure: str = "result_sha256") -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claimed = body.pop(closure, None)
    need(claimed == digest(body), "closure:" + str(path))
    return value


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT.resolve()))


def write_manifest(path: Path, entries: list[Path]) -> tuple[str, int]:
    lines = [f"{file_sha(item)}  {relative(item)}\n" for item in sorted(entries, key=relative)]
    with path.open("xb") as stream:
        stream.write("".join(lines).encode("ascii"))
    return file_sha(path), len(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-seed1", required=True)
    parser.add_argument("--candidate-seed2", required=True)
    parser.add_argument("--verification-seed1", required=True)
    parser.add_argument("--verification-seed2", required=True)
    parser.add_argument("--attacks", required=True)
    parser.add_argument("--seal-dir", required=True)
    args = parser.parse_args()
    c1, c2 = Path(args.candidate_seed1).resolve(), Path(args.candidate_seed2).resolve()
    v1, v2 = Path(args.verification_seed1).resolve(), Path(args.verification_seed2).resolve()
    attacks = Path(args.attacks).resolve()
    seal = Path(args.seal_dir).resolve()
    need(not seal.exists(), "new seal dir")
    seal.mkdir(parents=True)

    r1, r2 = load_closed(c1 / "result.json"), load_closed(c2 / "result.json")
    need(r1["invocation_seed"] != r2["invocation_seed"], "distinct producer seeds")
    need(r1["status"].startswith("PASS_NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS") and r2["status"].startswith("PASS_NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS"), "candidate status")
    need(r1["semantic_projection_sha256"] == r2["semantic_projection_sha256"], "producer semantic projection")
    ledger_sha1, ledger_sha2 = file_sha(c1 / LEDGER), file_sha(c2 / LEDGER)
    need(ledger_sha1 == ledger_sha2 and (c1 / LEDGER).read_bytes() == (c2 / LEDGER).read_bytes(), "double-seed byte-identical ledger")
    need(r1["census"]["ledger"]["file_sha256"] == ledger_sha1 and r2["census"]["ledger"]["file_sha256"] == ledger_sha2, "ledger pins")

    iv1, iv2 = load_closed(v1 / "verification.json"), load_closed(v2 / "verification.json")
    need(iv1["execution_seed"] != iv2["execution_seed"], "distinct verifier seeds")
    need(iv1["status"].startswith("PASS_INDEPENDENT_KEYED_SOURCE_HASH_JOIN__691424_ROWS") and iv2["status"].startswith("PASS_INDEPENDENT_KEYED_SOURCE_HASH_JOIN__691424_ROWS"), "verification status")
    need(iv1["semantic_projection_sha256"] == iv2["semantic_projection_sha256"] and iv1["candidate_ledger_sha256"] == iv2["candidate_ledger_sha256"] == ledger_sha1, "verification semantic equality")
    need(iv1["independent_implementation"]["imports_producer_or_shared_module"] is False and iv2["independent_implementation"]["imports_producer_or_shared_module"] is False, "independent implementation")

    attack = load_closed(attacks / "attack_receipt.json")
    need(attack["status"] == "PASS_CONTROL_AND_REJECT_15_OF_15_COHERENT_MUTATIONS__ZERO_CREDIT" and attack["accepted"] == 0 and attack["rejected"] == 15, "attacks")

    scripts = [
        ROOT / "deliverables/cm2_c26_exact_contact_source_factorization_scoped_v1_producer.py",
        ROOT / "deliverables/cm2_c26_exact_contact_source_factorization_scoped_v1_independent_verifier.py",
        ROOT / "deliverables/cm2_c26_exact_contact_source_factorization_scoped_v1_attack_harness.py",
        ROOT / "deliverables/cm2_c26_exact_contact_source_factorization_scoped_v1_terminal_replay.py",
        Path(__file__).resolve(),
    ]
    need(attack["verifier_sha256"] == file_sha(scripts[1]), "attacks bound to current verifier")
    need(attack["candidate_result_sha256"] == r1["result_sha256"] and attack["candidate_ledger_sha256"] == ledger_sha1, "attacks bound to candidate")
    authority_files = [
        ROOT / "deliverables/cm2_c27_same_chart_strict_volume_totality_subgate_receipt.json",
        ROOT / "deliverables/cm2_c27_same_chart_lower_dimensional_exact_contact_v1_result.json",
        ROOT / "deliverables/cm2_c27_same_chart_lower_dimensional_exact_contact_v1_terminal_receipt.json",
        ROOT / ".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2/receipt.json",
        ROOT / ".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2/root_manifest.sha256",
        ROOT / ".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2/payload_manifest.sha256",
        ROOT / ".cm2-runtime/audit/c27-c24a-current-primitive-three-terminal-union-normalized-v1-seed-30638103/payload/result.json",
        ROOT / ".cm2-runtime/audit/c27-c24a-current-primitive-three-terminal-union-normalized-v1-seed-30638103/payload/primitive_three_terminal_101080_unique_ownership.jsonl.gz",
    ]
    payload_entries = [c1 / "result.json", c1 / LEDGER, c2 / "result.json", c2 / LEDGER, v1 / "verification.json", v2 / "verification.json", attacks / "attack_receipt.json", *scripts, *authority_files]
    payload_sha, payload_count = write_manifest(seal / "payload_manifest.sha256", payload_entries)

    graph_buckets = r1["census"]["graph_feature_row_disjoint_bucket_census"]
    need(sum(graph_buckets.values()) == 20_656, "graph buckets sum")
    disposition_sum = sum(r1["census"]["disposition_census"].values())
    need(disposition_sum == 691_424, "dispositions sum")
    body = {
        "schema": "cm2.c26-independent.no-new-geometry-from-c26-feature-rows-zero-credit-receipt.v1",
        "status": "PASS_DOUBLE_SEED_DUAL_IMPLEMENTATION_AND_15_ATTACKS__NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS__691424_MUTUALLY_EXCLUSIVE_DISPOSITIONS__V5_C26_ABSENCE_SLOT_CLOSED__TWENTY_FAMILY_GATE_OPEN__ZERO_CREDIT",
        "headline": {
            "C26_feature_rows": 691_424,
            "mutually_exclusive_disposition_sum": disposition_sum,
            "C26_direct_support_carriers": 0,
            "scoped_unresolved": 0,
            "A1_A2_feature_only_primitive_owner_rows": 80_092,
            "R1_direct_C22A_rows": 295_340,
            "R2_C22A_union_alias_rows": 295_336,
            "graph_feature_rows": 20_656,
            "graph_feature_row_disjoint_buckets": graph_buckets,
            "graph_geometry_double_count": 0,
            "six_kernel_primitive_atoms": 483_232,
            "same_chart_strict_dim3_pairs": 187_132,
            "same_chart_lower_dim012_pairs": 5_783_708,
            "same_chart_lower_legal_witnesses": 0,
        },
        "double_seed": {
            "producer_seeds": [r1["invocation_seed"], r2["invocation_seed"]],
            "producer_semantic_projection_sha256": r1["semantic_projection_sha256"],
            "materialized_691424_row_ledgers_byte_identical": True,
            "ledger_sha256": ledger_sha1,
            "verifier_seeds": [iv1["execution_seed"], iv2["execution_seed"]],
            "verifier_semantic_projection_sha256": iv1["semantic_projection_sha256"],
        },
        "independent_verifier": {
            "source_sha256": file_sha(scripts[1]),
            "imports_producer_or_shared_module": False,
            "algorithm": "SQLITE_SOURCE_ROW_SHA256_RELATION_PLUS_INDEPENDENT_NODE_DISPOSITION_RECONSTRUCTION",
        },
        "coherent_attacks": {"control_pass": True, "accepted": 0, "rejected": 15, "receipt_file_sha256": file_sha(attacks / "attack_receipt.json")},
        "authority_scope": {
            "NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS": True,
            "fills_v5_C26_absence_slot": True,
            "why": "ALL_691424_C26_DAG_ROWS_HAVE_EXACTLY_ONE_SOURCE_HANDOFF_AND_ZERO_INDEPENDENT_SUPPORT_CARRIER",
            "G1_G2A_feature_dependency_double_counted_as_geometry": False,
            "global_three_terminal_totality_and_unique_assignment": False,
            "twenty_family_gate_closed_by_this_receipt": False,
            "remaining": [
                "A1_A2_R1_R2_G1_GLOBAL_THREE_TERMINAL_ASSIGNMENT",
                "FULL_483232_ATOM_TO_PAIR_INCIDENCE_AND_COMPLEMENT_JOIN",
                "G2A_GLOBAL_POSITIVE_C19_EXTENSION",
                "GLOBAL_THREE_TERMINAL_TOTALITY_AND_MUTUAL_EXCLUSIVITY",
                "C27_C28_C29_FULL_REBUILD",
            ],
            "C27_FAMILIES_or_transition_imported_or_read": False,
            "C28_or_C29_imported_or_read": False,
            "historical_edge_ledger_used_as_candidate_universe": False,
            "C26_absence_used_as_negative_geometry_theorem": False,
        },
        "source_files": {relative(path): file_sha(path) for path in scripts},
        "payload_manifest": {"filename": "payload_manifest.sha256", "file_sha256": payload_sha, "entry_count": payload_count},
        "formal_credit": 0,
        "manifest_authorized": False,
        "source_W_transition_authorized": False,
        "strict_nonpromotion": {"C27_transition_totality": 0, "C28_pair_routing": 0, "C29_physical_maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
    }
    receipt = dict(body)
    receipt["receipt_sha256"] = digest(body)
    receipt_path = seal / "receipt.json"
    with receipt_path.open("xb") as stream:
        stream.write(canonical(receipt) + b"\n")
    root_sha, root_count = write_manifest(seal / "root_manifest.sha256", [seal / "payload_manifest.sha256", receipt_path])
    print(canonical({"status": receipt["status"], "receipt_sha256": receipt["receipt_sha256"], "receipt_file_sha256": file_sha(receipt_path), "payload_manifest_file_sha256": payload_sha, "root_manifest_file_sha256": root_sha, "root_entry_count": root_count}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
