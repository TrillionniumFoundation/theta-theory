#!/usr/bin/env python3
"""Adapt T11--T19 authority roles to the corrected actual-v5 common-v2 wire."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / ".cm2-runtime/audit/c27-t11-t19-atlas-control-alias-authority-v1-seed-30653101-r2"
SOURCE_RESULT = SOURCE / "result.json"
SOURCE_CANDIDATES = SOURCE / "t11_t19_atlas_seam_candidate_ownership.jsonl.gz"
SOURCE_PROOFS = SOURCE / "t11_t18_auxiliary_proof_rows.jsonl.gz"
SOURCE_SLOTS = SOURCE / "t11_t19_slot_authority.jsonl.gz"
SOURCE_VERIFY = SOURCE / "independent_verification_seed30654701.json"
INTERFACE = ROOT / ".cm2-runtime/audit/c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json"
PINS = {
    SOURCE_RESULT: "702c53920711982477a16b3f17ddf6738c73496041f58d0b79be20c68e4f3d1a",
    SOURCE_CANDIDATES: "195d563049299b3eb548d9cca757971e395ba7e77f3c24749df6749e0e9468ca",
    SOURCE_PROOFS: "458e4d18d6de93f063311bd57f906dc4f49043ce86e6ef22925a5a2bc484cab2",
    SOURCE_SLOTS: "4fe3172c20fded85835d70f7c80986375b8ed7334614c7f691e560cbc550c80d",
    SOURCE_VERIFY: "aa5e71934638758f17ad49e843747212545457be6b1459735f45966f5bf9d661",
    INTERFACE: "6873b33d7b131a4bde0c4dbcf99873e6826cf2190fde6dfdf6640ee47d53c9d6",
}
CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
SLOTS = [
    (11, "T11_REVERSE_RECHART", "REVERSE_RECHART", 0, 4,
     "AUXILIARY_INVERSE_PROOF_ONLY"),
    (12, "T12_TRUE_CYCLIC_SEAM_E_TO_N", "TRUE_CYCLIC_SEAM_E_TO_N", 1, 1,
     "CANDIDATE_OWNERSHIP"),
    (13, "T13_TRUE_CYCLIC_SEAM_N_TO_W", "TRUE_CYCLIC_SEAM_N_TO_W", 1, 1,
     "CANDIDATE_OWNERSHIP"),
    (14, "T14_TRUE_CYCLIC_SEAM_W_TO_S", "TRUE_CYCLIC_SEAM_W_TO_S", 1, 1,
     "CANDIDATE_OWNERSHIP"),
    (15, "T15_TRUE_CYCLIC_SEAM_S_TO_E", "TRUE_CYCLIC_SEAM_S_TO_E", 1, 1,
     "CANDIDATE_OWNERSHIP"),
    (16, "T16_Jx_NEGATIVE_CONTROL", "Jx_NEGATIVE_CONTROL", 0, 16,
     "NEGATIVE_CONTROL_PROOF_ONLY"),
    (17, "T17_Jy_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL", 0, 16,
     "NEGATIVE_CONTROL_PROOF_ONLY"),
    (18, "T18_JxJy_NEGATIVE_CONTROL", "JxJy_NEGATIVE_CONTROL", 0, 16,
     "NEGATIVE_CONTROL_PROOF_ONLY"),
    (19, "T19_REPRESENTATION_ALIASES", "REPRESENTATION_ALIASES", 0, 276,
     "AUXILIARY_ALIAS_PROOF_ONLY"),
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


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            for row in rows: zipped.write(enc(row) + b"\n")


def descriptor(path: Path, rows: list[dict[str, Any]], schema: str,
               unique_key: str) -> dict[str, Any]:
    return {"path": str(path.relative_to(path.parents[1])), "row_schema": schema,
            "row_count": len(rows), "file_size": path.stat().st_size,
            "file_sha256": fsha(path), "row_sequence_sha256": sequence(rows),
            "unique_key": unique_key, "ordering": ["candidate_key"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        for path, pin in PINS.items():
            need(path.is_file() and not path.is_symlink() and fsha(path) == pin,
                 "input pin:" + path.name)
        interface = json.loads(INTERFACE.read_bytes())["corrected_interface"]
        need(interface["candidate_ownership_ledger"]["row_schema"] == CANDIDATE_SCHEMA
             and interface["materialized_physical_proof_join_ledger"]["row_schema"] == PROOF_SCHEMA,
             "corrected interface")
        source_result = json.loads(SOURCE_RESULT.read_bytes())
        closed(source_result, "result_sha256", "source result")
        source_verify = json.loads(SOURCE_VERIFY.read_bytes())
        closed(source_verify, "verification_sha256", "source verification")
        need(source_result["candidate_ownership_total"] == 4
             and source_result["total_proof_only_authority_rows"] == 328
             and source_verify["materializer_imported_or_executed"] is False
             and source_verify["candidate_ownership_total"] == 4
             and source_verify["total_proof_only_authority_rows"] == 328,
             "verified source semantics")
        source_candidates = list(jsonl(SOURCE_CANDIDATES))
        source_by_terminal = {}
        for ordinal, row in enumerate(source_candidates):
            closed(row, "row_sha256", f"source candidate:{ordinal}")
            need(row["ordinal"] == ordinal and row["terminal_assignment_cardinality"] == 1,
                 "source candidate wire")
            source_by_terminal[row["terminal"]] = row
        need(len(source_by_terminal) == 4, "four seam source candidates")
        source_slots = list(jsonl(SOURCE_SLOTS))
        need([(row["slot"], row["candidate_count"], row["authority_row_count"])
              for row in source_slots]
             == [(f"T{ordinal}", candidate_count, authority_count)
                 for ordinal, _, _, candidate_count, authority_count, _ in SLOTS],
             "source slot census")

        output = Path(args.output_dir).resolve()
        need(not output.exists(), "fresh output")
        output.mkdir(parents=True)
        entries = []
        for ordinal, slot, terminal, candidate_count, auxiliary_count, role in SLOTS:
            candidates = []
            if candidate_count:
                source = source_by_terminal[terminal]
                body = {
                    "schema": CANDIDATE_SCHEMA,
                    "ordinal": 0,
                    "candidate_key": source["candidate_id"],
                    "candidate_kind": "ATLAS_FORWARD_SEAM_CANDIDATE",
                    "candidate_pair_key_or_null": None,
                    "terminal_ordinal": ordinal,
                    "terminal": terminal,
                    "authority_slot": slot,
                    "primitive_authority_row_sha256": source["row_sha256"],
                    "component_relation_disposition": "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS",
                    "physical_proof_row_count": 0,
                    "physical_proof_row_sequence_sha256": EMPTY_SHA,
                    "formal_credit": 0,
                }
                candidates.append({**body, "row_sha256": dig(body)})
            proofs: list[dict[str, Any]] = []
            terminal_dir = output / slot
            terminal_dir.mkdir()
            candidate_path = terminal_dir / "candidate_ownership.jsonl.gz"
            proof_path = terminal_dir / "materialized_physical_proof_join.jsonl.gz"
            write_rows(candidate_path, candidates); write_rows(proof_path, proofs)
            entries.append({
                "terminal_ordinal": ordinal, "terminal": terminal,
                "authority_slot": slot, "role": role,
                "native_candidate_count": candidate_count,
                "auxiliary_authority_row_count": auxiliary_count,
                "semantic_incidences_promoted_to_physical_proof_count": 0,
                "candidate_ownership_ledger": descriptor(
                    candidate_path, candidates, CANDIDATE_SCHEMA, "candidate_key"),
                "materialized_physical_proof_join_ledger": descriptor(
                    proof_path, proofs, PROOF_SCHEMA, "proof_row_key"),
                "formal_credit": 0,
            })
        body = {
            "schema": "cm2.c27-independent.t11-t19.common-v2-adapter.result.v1",
            "status": "PASS_T11_T19_ACTUAL_V5_COMMON_V2__4_FORWARD_SEAM_CANDIDATES__0_MATERIALIZED_PHYSICAL_PROOFS__328_AUXILIARY_ROWS_NOT_PROMOTED__ZERO_CREDIT",
            "adapter_entries": entries,
            "candidate_ownership_row_schema": CANDIDATE_SCHEMA,
            "materialized_physical_proof_join_row_schema": PROOF_SCHEMA,
            "candidate_total": 4,
            "materialized_physical_proof_join_total": 0,
            "auxiliary_authority_row_total": 328,
            "component_relation_disposition_census": {
                "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 4},
            "auxiliary_authority_is_not_materialized_physical_proof": True,
            "reverse_control_alias_independent_candidate_count": 0,
            "source_authority_verification_sha256": source_verify["verification_sha256"],
            "input_pins": {str(path.relative_to(ROOT)): pin
                           for path, pin in sorted(PINS.items(), key=lambda item: str(item[0]))},
            "seed_declared_but_not_semantically_used": True,
            "old_C27_FAMILIES_imported_or_read": False,
            "old_transition_or_edge_ledger_used_as_candidate_universe": False,
            "global_atom_and_full_twenty_family_totality_closed": False,
            "formal_credit": 0, "manifest_authorized": False,
            "source_W_transition_authorized": False,
            "C27_C28_C29": "REJECT_PENDING_COMPLETE_PRIMITIVE_TWENTY_TERMINAL_GATE",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        result = {**body, "result_sha256": dig(body)}
        (output / "result.json").write_bytes(enc(result) + b"\n")
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error)); return 2
    print(enc({"status": result["status"],
               "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__": raise SystemExit(main())
