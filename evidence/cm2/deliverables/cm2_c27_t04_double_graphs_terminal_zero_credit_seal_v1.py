#!/usr/bin/env python3
"""Manifest-first zero-credit seal for the T04/DOUBLE_GRAPHS authority."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent


class Reject(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str: return hashlib.sha256(enc(value)).hexdigest()


def sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""): state.update(block)
    return state.hexdigest()


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def manifest(paths: list[Path]) -> bytes:
    return b"".join(sha(path).encode("ascii") + b"  " + rel(path).encode("ascii") + b"\n"
                    for path in sorted(paths, key=rel))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-a", required=True); parser.add_argument("--candidate-b", required=True)
    parser.add_argument("--verification", required=True); parser.add_argument("--attacks", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    a, b = Path(args.candidate_a), Path(args.candidate_b)
    verification, attacks = Path(args.verification), Path(args.attacks)
    output = Path(args.out_dir); need(not output.exists(), "fresh seal")
    names = ["t04_double_graphs_1362088_pair_ownership.jsonl.gz",
             "t04_double_graphs_legal_cross_component_physical_witnesses.jsonl.gz",
             "result.json", "manifest.json"]
    for name in names:
        need((a / name).is_file() and (b / name).is_file()
             and sha(a / name) == sha(b / name), "dual candidate bytes:" + name)
    va = json.loads(verification.read_bytes()); aa = json.loads(attacks.read_bytes())
    need(va["verification_sha256"] == digest({k:v for k,v in va.items() if k != "verification_sha256"})
         and va["status"].startswith("PASS_TWO_INDEPENDENT_SEMANTIC_RECONSTRUCTIONS")
         and va["candidate_pairs"] == 1_362_088 and va["unresolved"] == 0
         and va["legal_cross_component_witnesses"] == 0, "independent verification")
    need(aa["attack_receipt_sha256"] == digest({k:v for k,v in aa.items() if k != "attack_receipt_sha256"})
         and aa["attack_count"] == aa["rejected"] == 31 and aa["accepted"] == 0,
         "coherent attacks")
    result = json.loads((a / "result.json").read_bytes())
    need(result["result_sha256"] == digest(result["result"]), "candidate result")
    pair = result["result"]["pair_contract"]
    need(pair["candidate_pairs"] == 1_362_088
         and sum(pair["bucket_census"].values()) == 1_362_088
         and pair["unresolved"] == 0
         and pair["legal_cross_component_same_physical_point_witnesses"] == 0,
         "candidate contract")
    sources = [
        ROOT / "deliverables/cm2_c27_t04_double_graphs_pair_ownership_materializer_v1.py",
        ROOT / "deliverables/cm2_c27_t04_double_graphs_pair_ownership_independent_verifier_v1.py",
        ROOT / "deliverables/cm2_c27_t04_double_graphs_pair_ownership_attack_harness_v1.py",
        ROOT / "deliverables/cm2_c27_t04_double_graphs_terminal_zero_credit_seal_v1.py",
        ROOT / "deliverables/cm2_c27_t04_double_graphs_postpublication_cold_terminal_replay_v1.py",
    ]
    payload_members = [*(a / name for name in names), *(b / name for name in names),
                       verification, attacks, *sources]
    output.mkdir(parents=True)
    payload_path = output / "payload_manifest.sha256"
    payload_path.write_bytes(manifest(payload_members))
    body = {
        "schema": "cm2.c27-independent.t04-double-graphs.terminal-zero-credit-receipt.v1",
        "status": "PASS_T04_DOUBLE_GRAPHS_PAIR_LEVEL_TOTALITY_UNIQUE_OWNERSHIP_DUAL_IMPLEMENTATION_DUAL_SEED_31_ATTACKS__ZERO_CREDIT",
        "terminal": "DOUBLE_GRAPHS", "terminal_ordinal": 4,
        "authority_slot": "T04_DOUBLE_GRAPHS",
        "native_candidate_row_schema": "cm2.c27-independent.t04-double-graphs.pair-ownership-row.v1",
        "typed_common_v2_adapter_required_before_actual_v5_consumption": True,
        "pair_contract": {
            "candidate_pairs": 1_362_088,
            "bucket_census": pair["bucket_census"],
            "each_candidate_pair_exactly_one_T04_owner": True,
            "unresolved": 0, "legal_cross_component_witnesses": 0,
            "native_candidate_ledger_sha256": sha(a / names[0]),
            "physical_witness_ledger_sha256": sha(a / names[1]),
            "physical_witness_ledger_rows": 0,
        },
        "semantic_independence": {
            "cross_chart": ["EXPLICIT_GLOBAL_PHASE_N_Q_EQUATIONS",
                            "PRIMITIVE_CHART_RELATION_FIXED_SET_EQUATIONS"],
            "transverse_1d": ["DIRECT_INTERVAL_PROJECTION_GAP",
                              "INDEPENDENT_RATIONAL_INTERVAL_PROJECTION"],
            "graph_side_and_lower_owner_two_implementations_exact": True,
            "dual_seed_files_byte_identical": True,
        },
        "coherent_attacks": {"accepted": 0, "rejected": 31},
        "scope_governance": {
            "old_C27_FAMILIES_read_or_imported": False,
            "old_transition_ledger_read_or_imported": False,
            "C28_C29_read_or_imported": False,
            "historical_edge_ledger_used_as_candidate_universe": False,
        },
        "payload_manifest": {"path": rel(payload_path), "sha256": sha(payload_path),
                             "entry_count": len(payload_members)},
        "formal_credit": 0, "manifest_authorized": False,
        "source_W_transition_authorized": False,
        "strict_nonpromotion": {"C27": "UNAUTHORIZED", "C28": "UNAUTHORIZED",
                                "C29": "UNAUTHORIZED", "Source_W": 80,
                                "CM2": "NO-GO_FOR_CLAIM"},
    }
    receipt = {**body, "receipt_sha256": digest(body)}
    receipt_path = output / "receipt.json"; receipt_path.write_bytes(enc(receipt) + b"\n")
    root_path = output / "root_manifest.sha256"
    root_path.write_bytes(manifest([payload_path, receipt_path]))
    print(enc({"status": receipt["status"], "receipt_file_sha256": sha(receipt_path),
               "receipt_sha256": receipt["receipt_sha256"],
               "payload_manifest_sha256": sha(payload_path),
               "root_manifest_sha256": sha(root_path)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except Reject as exc:
        print("T04_SEAL_REJECT:" + str(exc)); raise SystemExit(2)
