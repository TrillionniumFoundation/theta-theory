#!/usr/bin/env python3
"""No-producer-import verifier for correction-v2 typed ownership ledgers."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "deliverables"
R = ROOT / ".cm2-runtime/audit"
RETAINED_SQLITE = D / "cm2_c27_retained_continuation_sqlite_verifier.py"
RETAINED_RECEIPT = D / "cm2_c27_retained_continuation_subgate_receipt.json"
R295A = D / "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz"
OUTGOING = R / "c27-outgoing-graphs-stream-seed-30627101/ledger.jsonl.gz"
SINGLE = R / "c27-single-graphs-stream-seed-30628101/ledger.jsonl.gz"
SHEET = R / "c27-sheet-owner-shadow-physical-stream-seed-30627401/sheet_owner_shadow_terminal_ledger.jsonl.gz"
INCLUDED = R / "c27-included-stratum-10660-materialized-v1-seed-30646101/included_stratum_10660_materialized_candidates.jsonl.gz"

PINS = {
    RETAINED_SQLITE: "b9936e811068164a016a31f28e8e7aed2eba0b34f555ce58cc411d377e93d589",
    RETAINED_RECEIPT: "08b760876914406e2fbe4e897609afd6ffc6f3667acaf6a1b4a7a9df58f6e263",
    R295A: "5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f",
    OUTGOING: "3e915eb5f45d2e0cef6911b898d3f9653d13e2035c8d4129613021e82e9f5f4e",
    SINGLE: "72f34d0246799fa89338849c92c2f1a3e0048ef9d4e75f4da054812822496262",
    SHEET: "3050f59733c5f5e183a3babc3ff1f2e772153b2e655997a3acd0826ad184fac2",
    INCLUDED: "4fc13179695407b093395243fb891d59ed7b7c5c7423208d394a59d6612a78be",
}
EXPECTED_CANDIDATES = {
    "INCLUDED_STRATUM_ATTACHMENTS": 10_660,
    "OUTGOING_GRAPHS": 264,
    "RETAINED_CONTINUATION": 276,
    "SHEET_OWNER": 17_940,
    "SHEET_SHADOW": 17_940,
    "SINGLE_GRAPHS": 4_984,
}
EXPECTED_INCIDENCES = {
    "INCLUDED_STRATUM_ATTACHMENTS": 10_660,
    "OUTGOING_GRAPHS": 792,
    "RETAINED_CONTINUATION": 276,
    "SHEET_OWNER": 17_940,
    "SHEET_SHADOW": 17_940,
    "SINGLE_GRAPHS": 14_552,
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(8 << 20):
            state.update(block)
    return state.hexdigest()


def closed(row: dict[str, Any], key: str, label: str) -> None:
    claim = row.get(key)
    body = dict(row); body.pop(key, None)
    need(type(claim) is str and claim == digest(body), label + ":closure")


def jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as handle:
        for line in handle:
            yield json.loads(line)


def candidate_id(terminal: str, key: str) -> str:
    return f"cm2-c27-independent:{terminal}:{key}"


def verify(directory: Path, seed: int) -> dict[str, Any]:
    for path, expected in PINS.items():
        need(path.is_file() and not path.is_symlink() and file_hash(path) == expected,
             "source pin:" + path.name)
    result_path = directory / "result.json"
    candidate_path = directory / "typed_candidate_ownership.jsonl.gz"
    incidence_path = directory / "proof_incidence.jsonl.gz"
    alias_path = directory / "representation_alias_auxiliary_crosswalk.jsonl.gz"
    result = json.loads(result_path.read_bytes())
    closed(result, "result_sha256", "result")
    need(result["status"].startswith("PASS_SCOPED_ROW_BACKED_TERMINALS_NORMALIZED")
         and result["candidate_census"] == EXPECTED_CANDIDATES
         and result["proof_incidence_census"] == EXPECTED_INCIDENCES
         and result["candidate_total"] == 52_064
         and result["proof_incidence_total"] == 62_160
         and result["representation_aliases"] == {
             "auxiliary_crosswalk_rows": 276,
             "independent_terminal_candidates": 0,
             "double_count_with_retained_continuation": 0}
         and result["scope_excludes_DOUBLE_GRAPHS"] is True
         and result["global_atom_and_full_twenty_family_totality_closed"] is False
         and result["formal_credit"] == 0
         and result["manifest_authorized"] is False
         and result["source_W_transition_authorized"] is False,
         "result semantics")
    for path in (candidate_path, incidence_path, alias_path):
        metadata = result["ledgers"][path.name]
        need(file_hash(path) == metadata["file_sha256"], "ledger file:" + path.name)

    candidates: dict[str, dict[str, Any]] = {}
    candidate_census: dict[str, int] = {}
    candidate_hashes: list[str] = []
    for ordinal, row in enumerate(jsonl(candidate_path)):
        closed(row, "row_sha256", f"candidate:{ordinal}")
        need(row["ordinal"] == ordinal
             and row["schema"] == "cm2.c27-independent.legacy-terminal.typed-candidate-ownership-row.v1"
             and row["terminal_assignment_cardinality"] == 1
             and row["formal_credit"] == 0
             and row["source_W_transition_authorized"] is False,
             f"candidate:{ordinal}:semantics")
        need(row["candidate_id"] == candidate_id(row["terminal"], row["candidate_key"])
             and row["candidate_id"] not in candidates, f"candidate:{ordinal}:id")
        candidates[row["candidate_id"]] = row
        candidate_census[row["terminal"]] = candidate_census.get(row["terminal"], 0) + 1
        candidate_hashes.append(row["row_sha256"])
    need(candidate_census == EXPECTED_CANDIDATES and len(candidates) == 52_064,
         "candidate census")
    need(digest(candidate_hashes) == result["ledgers"][candidate_path.name]["row_sequence_sha256"],
         "candidate sequence")

    incidences: dict[tuple[str, int], dict[str, Any]] = {}
    incidence_census: dict[str, int] = {}
    incidence_by_candidate: dict[str, int] = {}
    incidence_hashes: list[str] = []
    for ordinal, row in enumerate(jsonl(incidence_path)):
        closed(row, "row_sha256", f"incidence:{ordinal}")
        need(row["ordinal"] == ordinal
             and row["schema"] == "cm2.c27-independent.legacy-terminal.proof-incidence-row.v1"
             and row["candidate_id"] in candidates
             and row["terminal"] == candidates[row["candidate_id"]]["terminal"]
             and row["evidence_sha256"] == digest(row["evidence"])
             and row["formal_credit"] == 0
             and row["source_W_transition_authorized"] is False,
             f"incidence:{ordinal}:semantics")
        key = (row["candidate_id"], row["incidence_ordinal_within_candidate"])
        need(key not in incidences, f"incidence:{ordinal}:unique")
        incidences[key] = row
        incidence_census[row["terminal"]] = incidence_census.get(row["terminal"], 0) + 1
        incidence_by_candidate[row["candidate_id"]] = incidence_by_candidate.get(row["candidate_id"], 0) + 1
        incidence_hashes.append(row["row_sha256"])
    need(incidence_census == EXPECTED_INCIDENCES and len(incidences) == 62_160,
         "incidence census")
    need(all(incidence_by_candidate.get(key) == row["proof_incidence_count"]
             for key, row in candidates.items()), "per-candidate incidence cardinality")
    need(digest(incidence_hashes) == result["ledgers"][incidence_path.name]["row_sequence_sha256"],
         "incidence sequence")

    aliases: dict[str, dict[str, Any]] = {}
    alias_hashes: list[str] = []
    for ordinal, row in enumerate(jsonl(alias_path)):
        closed(row, "row_sha256", f"alias:{ordinal}")
        need(row["ordinal"] == ordinal
             and row["schema"] == "cm2.c27-independent.representation-alias.auxiliary-crosswalk-row.v1"
             and row["candidate_terminal"] == "RETAINED_CONTINUATION"
             and row["representation_map_role"] == "AUXILIARY_ALIAS_ANNOTATION"
             and row["independent_terminal_candidate"] is False
             and row["representation_alias_terminal_candidate_count"] == 0
             and row["retained_candidate_id"] in candidates
             and candidates[row["retained_candidate_id"]]["terminal"] == "RETAINED_CONTINUATION"
             and row["formal_credit"] == 0
             and row["source_W_transition_authorized"] is False,
             f"alias:{ordinal}:semantics")
        need(row["representation_id"] not in aliases, f"alias:{ordinal}:unique")
        aliases[row["representation_id"]] = row
        alias_hashes.append(row["row_sha256"])
    need(len(aliases) == 276
         and digest(alias_hashes) == result["ledgers"][alias_path.name]["row_sequence_sha256"],
         "alias census/sequence")

    # Retained candidates are independently rebuilt by the existing SQLite
    # implementation.  Its semantic-body commitment must equal the normalized
    # proof incidence sequence, while R295A remains auxiliary-only.
    retained_receipt = json.loads(RETAINED_RECEIPT.read_bytes())
    retained_ids = hashlib.sha256(); retained_sequence = hashlib.sha256()
    retained_representations = sorted(row["candidate_key"] for row in candidates.values()
                                      if row["terminal"] == "RETAINED_CONTINUATION")
    with gzip.open(R295A, "rt", encoding="utf-8") as handle:
        r295_top = json.load(handle)
    r295_by_sha = {row["row_sha256"]: row for row in r295_top["rows"]}
    need(len(r295_by_sha) == 276, "R295A exact rows")
    for representation in retained_representations:
        cid = candidate_id("RETAINED_CONTINUATION", representation)
        proof = incidences[(cid, 0)]
        body = proof["evidence"]
        need(proof["incidence_role"] == "EXACT_POSITIVE_T_FULL_FACE_AUTHORITY"
             and body["representation_id"] == representation
             and digest(body) == candidates[cid]["source_authority_row_sha256"],
             "retained proof body")
        alias = aliases[representation]
        source_alias = r295_by_sha.get(body["R295A_row_sha256"])
        need(source_alias is not None
             and alias["R295A_alias_row_id"] == source_alias["Round295A_retained_continuation_alias_row_id"]
             and alias["R295A_alias_row_sha256"] == source_alias["row_sha256"]
             and alias["retained_candidate_id"] == cid,
             "retained alias exact binding")
        retained_ids.update(representation.encode("ascii") + b"\n")
        retained_sequence.update(bytes.fromhex(digest(body)))
    commitment = retained_receipt["candidate_commitment"]
    need(retained_ids.hexdigest() == commitment["candidate_representation_ids_sha256"]
         and retained_sequence.hexdigest() == commitment["candidate_row_sequence_sha256"],
         "retained published commitment")

    # Exact projections of all other source ledgers.
    for source in jsonl(OUTGOING):
        closed(source, "candidate_digest", "source outgoing")
        cid = candidate_id("OUTGOING_GRAPHS", source["graph_id"])
        need(cid in candidates and candidates[cid]["source_authority_row_sha256"] == source["candidate_digest"]
             and candidates[cid]["proof_incidence_count"] == len(source["dispositions"]),
             "outgoing candidate projection")
        for index, evidence in enumerate(source["dispositions"]):
            need(incidences[(cid, index)]["evidence"] == evidence, "outgoing incidence projection")
    for source in jsonl(SINGLE):
        closed(source, "candidate_digest", "source single")
        cid = candidate_id("SINGLE_GRAPHS", source["graph_id"])
        need(cid in candidates and candidates[cid]["source_authority_row_sha256"] == source["candidate_digest"]
             and candidates[cid]["proof_incidence_count"] == len(source["dispositions"]),
             "single candidate projection")
        for index, evidence in enumerate(source["dispositions"]):
            need(incidences[(cid, index)]["evidence"] == evidence, "single incidence projection")
    for source in jsonl(SHEET):
        closed(source, "row_sha256", "source sheet")
        key = source["physical_sheet_id"] + "|" + source["role"]
        cid = candidate_id(source["terminal"], key)
        expected = {name: source[name] for name in (
            "physical_sheet_id", "role", "assigned_member_id", "owner_member_id",
            "shadow_member_id", "fresh_component_id", "primitive_sheet_row_sha256",
            "owner_C15_row_sha256", "shadow_C15_row_sha256", "owner_C25_row_sha256",
            "shadow_C25_row_sha256", "C26_owner_root_row_sha256",
            "materialized_shadow_node_row_sha256", "terminal_disposition")}
        expected["source_row_sha256"] = source["row_sha256"]
        need(cid in candidates and candidates[cid]["source_authority_row_sha256"] == source["row_sha256"]
             and incidences[(cid, 0)]["evidence"] == expected, "sheet projection")
    for source in jsonl(INCLUDED):
        closed(source, "row_sha256", "source included")
        cid = candidate_id("INCLUDED_STRATUM_ATTACHMENTS", source["representation_id"])
        expected = {name: source[name] for name in (
            "representation_id", "owner_member_id", "fresh_component_id", "base_root_id",
            "official_key_id", "representation_semantic_kind", "semantic_kernel",
            "semantic_body_sha256", "C15_member_row_sha256",
            "C25_representation_row_sha256", "C26_handle_row_sha256")}
        expected["source_row_sha256"] = source["row_sha256"]
        need(cid in candidates and candidates[cid]["source_authority_row_sha256"] == source["row_sha256"]
             and incidences[(cid, 0)]["evidence"] == expected, "included projection")

    completed = subprocess.run(
        [sys.executable, "-I", "-B", str(RETAINED_SQLITE), "--seed", str(seed)],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"", "retained independent SQLite")
    sqlite = json.loads(completed.stdout)
    need(sqlite["implementation"] == "SQLITE_EXACT_FACE_JOIN_THEN_AUTHORITY_BINDING"
         and sqlite["candidate_universe"]["candidate_count"] == 276
         and sqlite["candidate_universe"]["candidate_representation_ids_sha256"] == retained_ids.hexdigest()
         and sqlite["candidate_universe"]["candidate_row_sequence_sha256"] == retained_sequence.hexdigest()
         and sqlite["formal_credit"] == 0,
         "retained SQLite agreement")
    body = {
        "schema": "cm2.c27-independent.legacy-terminal.typed-candidate-ownership.verification.v1",
        "status": "PASS_NO_PRODUCER_IMPORT__EXACT_SOURCE_PROJECTIONS__CORRECTION_V2_52064_CANDIDATES_62160_INCIDENCES__ZERO_CREDIT",
        "producer_imported_or_executed": False,
        "retained_independent_sqlite_executed": True,
        "candidate_census": EXPECTED_CANDIDATES,
        "candidate_total": 52_064,
        "proof_incidence_census": EXPECTED_INCIDENCES,
        "proof_incidence_total": 62_160,
        "representation_alias_auxiliary_rows": 276,
        "representation_alias_independent_candidate_count": 0,
        "all_source_rows_exactly_projected": True,
        "candidate_exact_one_terminal": True,
        "proof_incidences_not_counted_as_candidates": True,
        "result_file_sha256": file_hash(result_path),
        "candidate_ledger_file_sha256": file_hash(candidate_path),
        "incidence_ledger_file_sha256": file_hash(incidence_path),
        "alias_ledger_file_sha256": file_hash(alias_path),
        "retained_sqlite_result_sha256": sqlite["result_sha256"],
        "formal_credit": 0,
        "manifest_authorized": False,
        "source_W_transition_authorized": False,
        "global_atom_and_full_twenty_family_totality_closed": False,
    }
    return {**body, "verification_sha256": digest(body)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        value = verify(Path(args.candidate_dir), args.seed)
        output = Path(args.output)
        need(not output.exists(), "fresh output")
        output.write_bytes(encode(value) + b"\n")
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({"status": value["status"],
                  "verification_sha256": value["verification_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
