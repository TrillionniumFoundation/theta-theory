#!/usr/bin/env python3
"""No-adapter-import inverse verifier for the T11--T19 common-v2 adapter."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / ".cm2-runtime/audit/c27-t11-t19-atlas-control-alias-authority-v1-seed-30653101-r2"
SOURCE_CANDIDATES = SOURCE / "t11_t19_atlas_seam_candidate_ownership.jsonl.gz"
SOURCE_PROOFS = SOURCE / "t11_t18_auxiliary_proof_rows.jsonl.gz"
SOURCE_SLOTS = SOURCE / "t11_t19_slot_authority.jsonl.gz"
SOURCE_VERIFY = SOURCE / "independent_verification_seed30654701.json"
PINS = {
    SOURCE_CANDIDATES: "195d563049299b3eb548d9cca757971e395ba7e77f3c24749df6749e0e9468ca",
    SOURCE_PROOFS: "458e4d18d6de93f063311bd57f906dc4f49043ce86e6ef22925a5a2bc484cab2",
    SOURCE_SLOTS: "4fe3172c20fded85835d70f7c80986375b8ed7334614c7f691e560cbc550c80d",
    SOURCE_VERIFY: "aa5e71934638758f17ad49e843747212545457be6b1459735f45966f5bf9d661",
}
CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
SLOTS = [
    (11, "T11_REVERSE_RECHART", "REVERSE_RECHART", 0, 4, "AUXILIARY_INVERSE_PROOF_ONLY"),
    (12, "T12_TRUE_CYCLIC_SEAM_E_TO_N", "TRUE_CYCLIC_SEAM_E_TO_N", 1, 1, "CANDIDATE_OWNERSHIP"),
    (13, "T13_TRUE_CYCLIC_SEAM_N_TO_W", "TRUE_CYCLIC_SEAM_N_TO_W", 1, 1, "CANDIDATE_OWNERSHIP"),
    (14, "T14_TRUE_CYCLIC_SEAM_W_TO_S", "TRUE_CYCLIC_SEAM_W_TO_S", 1, 1, "CANDIDATE_OWNERSHIP"),
    (15, "T15_TRUE_CYCLIC_SEAM_S_TO_E", "TRUE_CYCLIC_SEAM_S_TO_E", 1, 1, "CANDIDATE_OWNERSHIP"),
    (16, "T16_Jx_NEGATIVE_CONTROL", "Jx_NEGATIVE_CONTROL", 0, 16, "NEGATIVE_CONTROL_PROOF_ONLY"),
    (17, "T17_Jy_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL", 0, 16, "NEGATIVE_CONTROL_PROOF_ONLY"),
    (18, "T18_JxJy_NEGATIVE_CONTROL", "JxJy_NEGATIVE_CONTROL", 0, 16, "NEGATIVE_CONTROL_PROOF_ONLY"),
    (19, "T19_REPRESENTATION_ALIASES", "REPRESENTATION_ALIASES", 0, 276, "AUXILIARY_ALIAS_PROOF_ONLY"),
]


class Reject(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def dig(value: Any) -> str: return hashlib.sha256(enc(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 << 20): state.update(block)
    return state.hexdigest()


def closed(row: dict[str, Any], key: str, label: str) -> None:
    body = dict(row); claim = body.pop(key, None)
    need(type(claim) is str and claim == dig(body), label + ":closure")


def jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for line in stream: yield json.loads(line)


def sequence(rows: list[dict[str, Any]]) -> str:
    state = hashlib.sha256()
    for row in rows: state.update(row["row_sha256"].encode("ascii") + b"\n")
    return state.hexdigest()


def load(path: Path, schema: str, label: str) -> list[dict[str, Any]]:
    rows = []
    for ordinal, row in enumerate(jsonl(path)):
        closed(row, "row_sha256", f"{label}:{ordinal}")
        need(row["schema"] == schema and row["ordinal"] == ordinal,
             f"{label}:{ordinal}:wire")
        rows.append(row)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        for path, pin in PINS.items():
            need(path.is_file() and not path.is_symlink() and fsha(path) == pin,
                 "source pin:" + path.name)
        source_verify = json.loads(SOURCE_VERIFY.read_bytes())
        closed(source_verify, "verification_sha256", "source verification")
        need(source_verify["materializer_imported_or_executed"] is False
             and source_verify["candidate_ownership_total"] == 4
             and source_verify["total_proof_only_authority_rows"] == 328,
             "source verification semantics")
        seams = list(jsonl(SOURCE_CANDIDATES))
        seam_by_terminal = {}
        for ordinal, seam in enumerate(seams):
            closed(seam, "row_sha256", f"source seam:{ordinal}")
            need(seam["ordinal"] == ordinal
                 and seam["candidate_key_namespace"] == "ATLAS_FORWARD_SEAM"
                 and seam["terminal_assignment_cardinality"] == 1,
                 "source seam semantics")
            seam_by_terminal[seam["terminal"]] = seam
        need(len(seam_by_terminal) == 4, "four seams")
        local_aux = list(jsonl(SOURCE_PROOFS))
        aux_census = {}
        for ordinal, row in enumerate(local_aux):
            closed(row, "row_sha256", f"source auxiliary:{ordinal}")
            need(row["ordinal"] == ordinal
                 and row["independent_terminal_candidate"] is False
                 and row["candidate_count_contribution"] == 0,
                 "auxiliary not candidate")
            aux_census[row["terminal"]] = aux_census.get(row["terminal"], 0) + 1
        need(aux_census == {"JxJy_NEGATIVE_CONTROL": 16,
                            "Jx_NEGATIVE_CONTROL": 16,
                            "Jy_NEGATIVE_CONTROL": 16,
                            "REVERSE_RECHART": 4},
             "local auxiliary census")

        directory = Path(args.candidate_dir).resolve()
        result_path = directory / "result.json"
        result = json.loads(result_path.read_bytes())
        closed(result, "result_sha256", "result")
        need(result["candidate_total"] == 4
             and result["materialized_physical_proof_join_total"] == 0
             and result["auxiliary_authority_row_total"] == 328
             and result["component_relation_disposition_census"]
                == {"NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 4}
             and result["auxiliary_authority_is_not_materialized_physical_proof"] is True
             and result["reverse_control_alias_independent_candidate_count"] == 0
             and result["old_C27_FAMILIES_imported_or_read"] is False
             and result["old_transition_or_edge_ledger_used_as_candidate_universe"] is False
             and result["formal_credit"] == 0
             and result["manifest_authorized"] is False
             and result["source_W_transition_authorized"] is False
             and result["global_atom_and_full_twenty_family_totality_closed"] is False,
             "result semantics")
        entries = {entry["authority_slot"]: entry for entry in result["adapter_entries"]}
        need(set(entries) == {slot for _, slot, _, _, _, _ in SLOTS}, "entry slots")
        candidate_total = proof_total = 0
        seen_keys = set()
        for terminal_ordinal, slot, terminal, candidate_count, auxiliary_count, role in SLOTS:
            entry = entries[slot]
            candidate_path = directory / entry["candidate_ownership_ledger"]["path"]
            proof_path = directory / entry["materialized_physical_proof_join_ledger"]["path"]
            candidates = load(candidate_path, CANDIDATE_SCHEMA, slot + ":candidate")
            proofs = load(proof_path, PROOF_SCHEMA, slot + ":proof")
            for path, rows, descriptor in (
                    (candidate_path, candidates, entry["candidate_ownership_ledger"]),
                    (proof_path, proofs, entry["materialized_physical_proof_join_ledger"])):
                need(fsha(path) == descriptor["file_sha256"]
                     and path.stat().st_size == descriptor["file_size"]
                     and len(rows) == descriptor["row_count"]
                     and sequence(rows) == descriptor["row_sequence_sha256"],
                     "descriptor:" + slot)
            expected_candidates = []
            if candidate_count:
                source = seam_by_terminal[terminal]
                body = {"schema": CANDIDATE_SCHEMA, "ordinal": 0,
                        "candidate_key": source["candidate_id"],
                        "candidate_kind": "ATLAS_FORWARD_SEAM_CANDIDATE",
                        "candidate_pair_key_or_null": None,
                        "terminal_ordinal": terminal_ordinal, "terminal": terminal,
                        "authority_slot": slot,
                        "primitive_authority_row_sha256": source["row_sha256"],
                        "component_relation_disposition": "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS",
                        "physical_proof_row_count": 0,
                        "physical_proof_row_sequence_sha256": EMPTY_SHA,
                        "formal_credit": 0}
                expected_candidates.append({**body, "row_sha256": dig(body)})
            need(candidates == expected_candidates and proofs == [], "exact inverse:" + slot)
            need(entry["terminal_ordinal"] == terminal_ordinal
                 and entry["terminal"] == terminal and entry["role"] == role
                 and entry["native_candidate_count"] == candidate_count
                 and entry["auxiliary_authority_row_count"] == auxiliary_count
                 and entry["semantic_incidences_promoted_to_physical_proof_count"] == 0,
                 "entry semantics:" + slot)
            for candidate in candidates:
                need(candidate["candidate_key"] not in seen_keys, "candidate key unique")
                seen_keys.add(candidate["candidate_key"])
            candidate_total += len(candidates); proof_total += len(proofs)
        need(candidate_total == len(seen_keys) == 4 and proof_total == 0,
             "global candidate/proof census")
        body = {
            "schema": "cm2.c27-independent.t11-t19.common-v2-adapter.verification.v1",
            "status": "PASS_NO_ADAPTER_IMPORT__EXACT_INVERSE_9_SLOTS__4_FORWARD_SEAM_CANDIDATES__0_PHYSICAL_PROOFS__328_AUXILIARY_ROWS_NOT_PROMOTED__ZERO_CREDIT",
            "adapter_imported_or_executed": False,
            "source_authority_independent_verification_bound": True,
            "candidate_total": 4,
            "materialized_physical_proof_join_total": 0,
            "auxiliary_authority_row_total": 328,
            "seam_candidate_count": 4,
            "reverse_control_alias_candidate_count": 0,
            "result_file_sha256": fsha(result_path),
            "formal_credit": 0, "manifest_authorized": False,
            "source_W_transition_authorized": False,
            "global_atom_and_full_twenty_family_totality_closed": False,
        }
        verification = {**body, "verification_sha256": dig(body)}
        output = Path(args.output)
        need(not output.exists(), "fresh output")
        output.write_bytes(enc(verification) + b"\n")
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error)); return 2
    print(enc({"status": verification["status"],
               "verification_sha256": verification["verification_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__": raise SystemExit(main())
