#!/usr/bin/env python3
"""No-producer-import verifier for the corrected T04 common-v2 adapter."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterator


CANDIDATE_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "candidate-ownership.row.v2")
PROOF_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "materialized-physical-proof-join.row.v2")
ABSENCE_SCHEMA = (
    "cm2.c27-independent.t04-double-graphs.common-v2-terminal-absence-"
    "authority.row.v2")
CP = "round306c27-v5-t04-double-graphs-candidate:"
AP = "round306c27-v5-t04-double-graphs-absence-authority:"
EMPTY = hashlib.sha256(b"").hexdigest()
DISPOSITION = "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"
EXPECTED = {
    "CROSS_CHART_QUOTIENT_RECHART": 1_361_424,
    "SAME_CHART_TRANSVERSE_1D": 448,
    "CROSS_CHART_GRAPH_SIDE_T0": 192,
    "CODIMENSION_TWO_LOWER_OWNER": 24,
}
ROUTES = {
    "CROSS_CHART_QUOTIENT_RECHART": {
        "EXACT_NONINCIDENCE__OPPOSITE_DOMINANT_STRICT_SIGN",
        "EXACT_NONINCIDENCE__PERPENDICULAR_REQUIRES_EXCLUDED_UNIT_T_ENDPOINT",
    },
    "SAME_CHART_TRANSVERSE_1D": {
        "EXACT_NONINCIDENCE__STRICT_RATIONAL_P_GAP"},
    "CROSS_CHART_GRAPH_SIDE_T0": {
        "EXACT_NONINCIDENCE__T0_GLOBAL_PHASE_POSITION_MISMATCH"},
    "CODIMENSION_TWO_LOWER_OWNER": {
        "EXACT_NONEDGE__OPEN_TARGET_EXCLUSION_AND_UNIQUE_SOURCE_COMPONENT_T0_OWNER"},
}
CANDIDATE_FIELDS = {
    "schema", "ordinal", "candidate_key", "candidate_kind",
    "candidate_pair_key_or_null", "terminal_ordinal", "terminal",
    "authority_slot", "primitive_authority_row_sha256",
    "component_relation_disposition", "physical_proof_row_count",
    "physical_proof_row_sequence_sha256", "formal_credit", "row_sha256",
}
ABSENCE_FIELDS = {
    "schema", "ordinal", "absence_authority_row_key", "candidate_key",
    "terminal", "terminal_ordinal", "authority_slot", "native_candidate_id",
    "native_candidate_key_sha256", "native_bucket",
    "native_authority_row_sha256", "exact_disposition_route",
    "exact_physical_absence_evidence", "resolved", "unresolved",
    "legal_cross_component_same_physical_point_witness",
    "component_relation_disposition", "formal_credit", "row_sha256",
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(enc(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            state.update(block)
    return state.hexdigest()


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            body = dict(row)
            claim = body.pop("row_sha256", None)
            need(claim == digest(body), "row closure:" + path.name + ":" + str(ordinal))
            yield row


def document(path: Path, closure: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claim = body.pop(closure, None)
    need(claim == digest(body), "document closure:" + path.name)
    return value


def next_required(stream: Iterator[dict[str, Any]], label: str,
                  ordinal: int) -> dict[str, Any]:
    try:
        return next(stream)
    except StopIteration as exc:
        raise Reject("row omission:" + label + ":" + str(ordinal)) from exc


def no_extra(stream: Iterator[dict[str, Any]], label: str) -> None:
    try:
        next(stream)
    except StopIteration:
        return
    raise Reject("extra row:" + label)


def common_candidate_key(source: dict[str, Any]) -> str:
    return CP + digest({
        "native_candidate_id": source["candidate_id"],
        "native_candidate_key_sha256": source["candidate_key_sha256"],
        "terminal_ordinal": 4,
        "authority_slot": "T04_DOUBLE_GRAPHS",
    })


def validate_native(source: dict[str, Any]) -> None:
    identity = {"T04_terminal": "DOUBLE_GRAPHS",
                "bucket": source["bucket"],
                "candidate_key": source["candidate_key"]}
    need(source["schema"] ==
         "cm2.c27-independent.t04-double-graphs.pair-ownership-row.v1"
         and source["candidate_id"] ==
         "t04-double-graphs-pair:" + digest(identity)
         and source["candidate_key_sha256"] == digest(source["candidate_key"]),
         "native identity")
    need(source["bucket"] in EXPECTED
         and source["exact_disposition_route"] in ROUTES[source["bucket"]]
         and type(source["exact_physical_proof"]) is dict
         and bool(source["exact_physical_proof"]), "native typed absence evidence")
    need(source["T04_terminal"] == "DOUBLE_GRAPHS"
         and source["pair_owner_terminal"] == "T04_DOUBLE_GRAPHS"
         and source["pair_owner_count"] == 1
         and source["resolved"] is True and source["unresolved"] is False
         and source["legal_cross_component_same_physical_point_witness"] is False
         and source["formal_credit"] == 0, "native nonincidence semantics")


def manifest(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text("ascii").splitlines():
        claim, name = line.split("  ", 1)
        need(name not in entries, "manifest duplicate")
        entries[name] = claim
    return entries


def verify_adapter(native_path: Path, adapter: Path,
                   scratch: Path) -> tuple[dict[str, Any], dict[str, str]]:
    candidate_path = adapter / "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz"
    absence_path = adapter / "T04_DOUBLE_GRAPHS_terminal_absence_authority.jsonl.gz"
    proof_path = adapter / "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz"
    receipt_path = adapter / "adapter_receipt.json"
    manifest_path = adapter / "manifest.sha256"
    receipt = document(receipt_path, "receipt_sha256")
    need(receipt["schema"] ==
         "cm2.c27-independent.t04-double-graphs.common-v2-typed-adapter-correction-receipt.v2"
         and receipt["terminal"] == "DOUBLE_GRAPHS"
         and receipt["terminal_ordinal"] == 4
         and receipt["authority_slot"] == "T04_DOUBLE_GRAPHS"
         and receipt["candidate_key_namespace"] == CP
         and receipt["absence_authority_key_namespace"] == AP,
         "receipt identity")
    exact = receipt["exact_census"]
    need(exact == {
        "candidate_pairs": 1_362_088,
        "terminal_absence_authority_rows": 1_362_088,
        "physical_proof_rows": 0,
        "bucket_census": EXPECTED,
        "unresolved": 0,
        "legal_cross_component_witnesses": 0,
        "component_edges": 0,
    }, "receipt exact census")
    contract = receipt["common_v2_contract"]
    need(contract["component_relation_disposition"] == DISPOSITION
         and contract["each_candidate_physical_proof_row_count"] == 0
         and contract["each_candidate_physical_proof_sequence_sha256"] == EMPTY
         and contract["common_physical_proof_join_is_empty"] is True
         and contract["native_exact_absence_is_terminal_authority_not_physical_proof"] is True
         and contract["absence_authority_join_exact"] is True,
         "corrected common-v2 semantics")
    need(receipt["correction_governance"]["quarantined_outputs_may_not_be_consumed"] is True
         and receipt["formal_credit"] == 0
         and receipt["manifest_authorized"] is False
         and receipt["source_W_transition_authorized"] is False,
         "fail-closed governance")
    entries = manifest(manifest_path)
    expected_files = (candidate_path, absence_path, proof_path, receipt_path)
    need(set(entries) == {path.name for path in expected_files}, "manifest exact membership")
    for path in expected_files:
        need(entries[path.name] == file_sha(path), "manifest member:" + path.name)

    need(not scratch.exists(), "fresh verifier scratch")
    db = sqlite3.connect(scratch)
    try:
        db.execute("PRAGMA journal_mode=OFF")
        db.execute("PRAGMA synchronous=OFF")
        db.execute("CREATE TABLE expected (candidate_key TEXT PRIMARY KEY, native_json BLOB NOT NULL)")
        census: Counter[str] = Counter()
        for source in rows(native_path):
            validate_native(source)
            db.execute("INSERT INTO expected VALUES (?,?)",
                       (common_candidate_key(source), enc(source)))
            census[source["bucket"]] += 1
        db.commit()
        need(dict(census) == EXPECTED, "independent native census")

        candidate_stream = rows(candidate_path)
        absence_stream = rows(absence_path)
        candidate_sequence = hashlib.sha256()
        absence_sequence = hashlib.sha256()
        previous: str | None = None
        count = 0
        for ordinal, (key, raw) in enumerate(db.execute(
                "SELECT candidate_key,native_json FROM expected ORDER BY candidate_key")):
            source = json.loads(raw)
            candidate = next_required(candidate_stream, "candidate", ordinal)
            absence = next_required(absence_stream, "absence", ordinal)
            absence_key = AP + digest([
                key, source["row_sha256"], source["exact_disposition_route"]])
            need(set(candidate) == CANDIDATE_FIELDS, "candidate exact fields")
            need(set(absence) == ABSENCE_FIELDS, "absence exact fields")
            need(previous is None or previous < key, "strict candidate ordering")
            previous = key
            need(candidate["schema"] == CANDIDATE_SCHEMA
                 and candidate["ordinal"] == ordinal
                 and candidate["candidate_key"] == key
                 and candidate["candidate_kind"] == "DOUBLE_GRAPHS_PRIMITIVE_PAIR"
                 and candidate["candidate_pair_key_or_null"] == key
                 and candidate["terminal_ordinal"] == 4
                 and candidate["terminal"] == "DOUBLE_GRAPHS"
                 and candidate["authority_slot"] == "T04_DOUBLE_GRAPHS"
                 and candidate["primitive_authority_row_sha256"] == absence["row_sha256"]
                 and candidate["component_relation_disposition"] == DISPOSITION
                 and candidate["physical_proof_row_count"] == 0
                 and candidate["physical_proof_row_sequence_sha256"] == EMPTY
                 and candidate["formal_credit"] == 0,
                 "candidate exact corrected adaptation")
            need(absence["schema"] == ABSENCE_SCHEMA
                 and absence["ordinal"] == ordinal
                 and absence["absence_authority_row_key"] == absence_key
                 and absence["candidate_key"] == key
                 and absence["terminal"] == "DOUBLE_GRAPHS"
                 and absence["terminal_ordinal"] == 4
                 and absence["authority_slot"] == "T04_DOUBLE_GRAPHS"
                 and absence["native_candidate_id"] == source["candidate_id"]
                 and absence["native_candidate_key_sha256"] == source["candidate_key_sha256"]
                 and absence["native_bucket"] == source["bucket"]
                 and absence["native_authority_row_sha256"] == source["row_sha256"]
                 and absence["exact_disposition_route"] == source["exact_disposition_route"]
                 and absence["exact_physical_absence_evidence"] == source["exact_physical_proof"]
                 and absence["resolved"] is True and absence["unresolved"] is False
                 and absence["legal_cross_component_same_physical_point_witness"] is False
                 and absence["component_relation_disposition"] == DISPOSITION
                 and absence["formal_credit"] == 0,
                 "absence authority exact adaptation")
            candidate_sequence.update(candidate["row_sha256"].encode("ascii") + b"\n")
            absence_sequence.update(absence["row_sha256"].encode("ascii") + b"\n")
            count += 1
        no_extra(candidate_stream, "candidate")
        no_extra(absence_stream, "absence")
        proof_stream = rows(proof_path)
        no_extra(proof_stream, "physical proof")
        need(count == 1_362_088, "exact candidate count")
    finally:
        db.close()
    scratch.unlink()

    cd = receipt["candidate_ownership_ledger"]
    ad = receipt["terminal_absence_authority_ledger"]
    pd = receipt["materialized_physical_proof_join_ledger"]
    need(cd["sha256"] == file_sha(candidate_path)
         and cd["row_count"] == 1_362_088
         and cd["row_sequence_sha256"] == candidate_sequence.hexdigest()
         and cd["row_schema"] == CANDIDATE_SCHEMA
         and cd["unique_key"] == "candidate_key"
         and cd["ordering"] == ["candidate_key"], "candidate descriptor")
    need(ad["sha256"] == file_sha(absence_path)
         and ad["row_count"] == 1_362_088
         and ad["row_sequence_sha256"] == absence_sequence.hexdigest()
         and ad["row_schema"] == ABSENCE_SCHEMA
         and ad["unique_key"] == "absence_authority_row_key"
         and ad["ordering"] == ["candidate_key"], "absence descriptor")
    need(pd["sha256"] == file_sha(proof_path)
         and pd["row_count"] == 0
         and pd["row_sequence_sha256"] == EMPTY
         and pd["row_schema"] == PROOF_SCHEMA
         and pd["unique_key"] == "proof_row_key", "empty proof descriptor")
    files = {
        "candidate_ledger_sha256": file_sha(candidate_path),
        "absence_ledger_sha256": file_sha(absence_path),
        "empty_proof_ledger_sha256": file_sha(proof_path),
        "receipt_file_sha256": file_sha(receipt_path),
        "manifest_file_sha256": file_sha(manifest_path),
    }
    return receipt, files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--native-ledger", required=True)
    parser.add_argument("--adapter-a", required=True)
    parser.add_argument("--adapter-b", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    need(not output.exists(), "fresh verification output")
    output.parent.mkdir(parents=True, exist_ok=True)
    native_path = Path(args.native_ledger).resolve()
    adapter_a = Path(args.adapter_a).resolve()
    adapter_b = Path(args.adapter_b).resolve()
    receipt_a, files_a = verify_adapter(
        native_path, adapter_a, output.parent / ".t04_v2_verifier.sqlite3")
    receipt_b = document(adapter_b / "adapter_receipt.json", "receipt_sha256")
    files_b = {
        "candidate_ledger_sha256": file_sha(
            adapter_b / "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz"),
        "absence_ledger_sha256": file_sha(
            adapter_b / "T04_DOUBLE_GRAPHS_terminal_absence_authority.jsonl.gz"),
        "empty_proof_ledger_sha256": file_sha(
            adapter_b / "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz"),
        "receipt_file_sha256": file_sha(adapter_b / "adapter_receipt.json"),
        "manifest_file_sha256": file_sha(adapter_b / "manifest.sha256"),
    }
    need(receipt_a == receipt_b and files_a == files_b,
         "dual-seed all common adapter files byte-identical")
    body = {
        "schema": (
            "cm2.c27-independent.t04-double-graphs.common-v2-typed-adapter-"
            "correction-independent-verification.v2"),
        "status": (
            "PASS_NO_PRODUCER_IMPORT_1362088_CANDIDATES_1362088_ABSENCE_AUTHORITIES_"
            "ZERO_PHYSICAL_PROOFS_DUAL_TRUE_SEED_IDENTICAL"),
        "candidate_pairs": 1_362_088,
        "terminal_absence_authority_rows": 1_362_088,
        "physical_proof_rows": 0,
        "bucket_census": EXPECTED,
        "terminal_ordinal": 4,
        "authority_slot": "T04_DOUBLE_GRAPHS",
        "component_relation_disposition": DISPOSITION,
        "candidate_schema": CANDIDATE_SCHEMA,
        "absence_schema": ABSENCE_SCHEMA,
        "proof_schema": PROOF_SCHEMA,
        "candidate_key_namespace": CP,
        "absence_authority_key_namespace": AP,
        "unresolved": 0,
        "legal_cross_component_witnesses": 0,
        "component_edges": 0,
        "adapter_source_imported": False,
        "dual_seed_all_files_byte_identical": True,
        "files": files_a,
        "formal_credit": 0,
        "manifest_authorized": False,
        "source_W_transition_authorized": False,
    }
    wrapper = {**body, "verification_sha256": digest(body)}
    output.write_bytes(enc(wrapper) + b"\n")
    print(enc(wrapper).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("T04_COMMON_V2_CORRECTION_VERIFIER_REJECT:" + str(exc))
        raise SystemExit(2)
