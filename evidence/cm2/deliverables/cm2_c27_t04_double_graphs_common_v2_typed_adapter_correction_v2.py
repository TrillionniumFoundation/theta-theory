#!/usr/bin/env python3
"""Correct T04 adapter: candidate ownership plus exact-absence authority, zero physical proofs.

The quarantined v1 adapter mislabeled exact nonincidence rows as materialized
physical proofs.  This append-only correction implements the actual-v5 v2
contract: every T04 candidate is resolved by terminal semantics, so the common
physical-proof join is empty.  Native exact absence evidence is retained in a
separate terminal authority ledger.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / ".cm2-runtime" / "audit"
CANDIDATE_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "candidate-ownership.row.v2")
PROOF_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "materialized-physical-proof-join.row.v2")
ABSENCE_SCHEMA = (
    "cm2.c27-independent.t04-double-graphs.common-v2-terminal-absence-"
    "authority.row.v2")
CANDIDATE_PREFIX = "round306c27-v5-t04-double-graphs-candidate:"
ABSENCE_PREFIX = "round306c27-v5-t04-double-graphs-absence-authority:"
EMPTY_SEQUENCE_SHA256 = hashlib.sha256(b"").hexdigest()
DISPOSITION = "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"
EXPECTED = {
    "CROSS_CHART_QUOTIENT_RECHART": 1_361_424,
    "SAME_CHART_TRANSVERSE_1D": 448,
    "CROSS_CHART_GRAPH_SIDE_T0": 192,
    "CODIMENSION_TWO_LOWER_OWNER": 24,
}
ALLOWED_ROUTES = {
    "CROSS_CHART_QUOTIENT_RECHART": {
        "EXACT_NONINCIDENCE__OPPOSITE_DOMINANT_STRICT_SIGN",
        "EXACT_NONINCIDENCE__PERPENDICULAR_REQUIRES_EXCLUDED_UNIT_T_ENDPOINT",
    },
    "SAME_CHART_TRANSVERSE_1D": {
        "EXACT_NONINCIDENCE__STRICT_RATIONAL_P_GAP",
    },
    "CROSS_CHART_GRAPH_SIDE_T0": {
        "EXACT_NONINCIDENCE__T0_GLOBAL_PHASE_POSITION_MISMATCH",
    },
    "CODIMENSION_TWO_LOWER_OWNER": {
        "EXACT_NONEDGE__OPEN_TARGET_EXCLUSION_AND_UNIQUE_SOURCE_COMPONENT_T0_OWNER",
    },
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


def close(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def closed_document(path: Path, closure: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claim = body.pop(closure, None)
    need(claim == digest(body), "document closure:" + str(path))
    return value


def native_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            body = dict(row)
            claim = body.pop("row_sha256", None)
            need(claim == digest(body), "native row closure:" + str(ordinal))
            yield row


class Writer:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.open("xb")
        self.gz = gzip.GzipFile(filename="", fileobj=self.raw, mode="wb",
                                compresslevel=9, mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def write(self, row: dict[str, Any]) -> None:
        body = dict(row)
        claim = body.pop("row_sha256", None)
        need(claim == digest(body), "output row closure")
        self.gz.write(enc(row) + b"\n")
        self.sequence.update(claim.encode("ascii") + b"\n")
        self.count += 1

    def finish(self, schema: str, unique_key: str,
               ordering: list[str]) -> dict[str, Any]:
        self.gz.close()
        self.raw.close()
        return {
            "path": self.path.name,
            "sha256": file_sha(self.path),
            "size": self.path.stat().st_size,
            "row_count": self.count,
            "row_sequence_sha256": self.sequence.hexdigest(),
            "row_schema": schema,
            "unique_key": unique_key,
            "ordering": ordering,
        }


def candidate_key(source: dict[str, Any]) -> str:
    return CANDIDATE_PREFIX + digest({
        "native_candidate_id": source["candidate_id"],
        "native_candidate_key_sha256": source["candidate_key_sha256"],
        "terminal_ordinal": 4,
        "authority_slot": "T04_DOUBLE_GRAPHS",
    })


def validate_native(source: dict[str, Any]) -> None:
    need(source["schema"] ==
         "cm2.c27-independent.t04-double-graphs.pair-ownership-row.v1",
         "native schema")
    identity = {"T04_terminal": "DOUBLE_GRAPHS",
                "bucket": source["bucket"],
                "candidate_key": source["candidate_key"]}
    need(source["candidate_id"] ==
         "t04-double-graphs-pair:" + digest(identity), "native candidate id")
    need(source["candidate_key_sha256"] == digest(source["candidate_key"]),
         "native candidate key closure")
    need(source["bucket"] in EXPECTED and source["exact_disposition_route"]
         in ALLOWED_ROUTES[source["bucket"]], "native typed absence route")
    need(type(source["exact_physical_proof"]) is dict
         and bool(source["exact_physical_proof"]), "native exact absence evidence")
    need(source["T04_terminal"] == "DOUBLE_GRAPHS"
         and source["pair_owner_terminal"] == "T04_DOUBLE_GRAPHS"
         and source["pair_owner_count"] == 1
         and source["resolved"] is True and source["unresolved"] is False
         and source["legal_cross_component_same_physical_point_witness"] is False
         and source["formal_credit"] == 0, "native exact nonincidence contract")


def validate_interface(path: Path) -> str:
    value = closed_document(path, "preflight_sha256")
    interface = value["corrected_interface"]
    candidate = interface["candidate_ownership_ledger"]
    proof = interface["materialized_physical_proof_join_ledger"]
    need(value["decision"] == "REJECT" and value["formal_credit"] == 0,
         "truthful correction-v2 interface")
    need(candidate["row_schema"] == CANDIDATE_SCHEMA
         and candidate["ordering"] == ["candidate_key"]
         and DISPOSITION in candidate["allowed_component_relation_dispositions"],
         "candidate correction-v2 interface")
    need(proof["row_schema"] == PROOF_SCHEMA
         and proof["incidence_row_is_not_automatically_a_physical_proof"] is True,
         "physical proof correction-v2 interface")
    return value["preflight_sha256"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface-v2", required=True)
    parser.add_argument("--interface-v2-sha256", required=True)
    parser.add_argument("--native-ledger", required=True)
    parser.add_argument("--native-ledger-sha256", required=True)
    parser.add_argument("--native-receipt", required=True)
    parser.add_argument("--native-receipt-sha256", required=True)
    parser.add_argument("--native-cold-replay", required=True)
    parser.add_argument("--native-cold-replay-sha256", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", required=True)
    args = parser.parse_args()

    need(args.seed in {"30649101", "30649991"}
         and os.environ.get("PYTHONHASHSEED") == args.seed,
         "active true correction-v2 seed")
    need(sys.flags.isolated == 0 and sys.flags.ignore_environment == 0
         and sys.flags.hash_randomization == 1
         and sys.flags.dont_write_bytecode == 1,
         "non-isolated seeded correction-v2 runtime")
    need(hash("cm2-t04-common-v2-correction-seed") == {
        "30649101": 653035249675436901,
        "30649991": -271415725888434318,
    }[args.seed], "active correction-v2 seed fingerprint")

    interface_path = Path(args.interface_v2).resolve()
    native_ledger = Path(args.native_ledger).resolve()
    native_receipt_path = Path(args.native_receipt).resolve()
    native_cold_path = Path(args.native_cold_replay).resolve()
    pins = ((interface_path, args.interface_v2_sha256),
            (native_ledger, args.native_ledger_sha256),
            (native_receipt_path, args.native_receipt_sha256),
            (native_cold_path, args.native_cold_replay_sha256))
    need(all(file_sha(path) == claim for path, claim in pins), "input pins")
    interface_object_sha = validate_interface(interface_path)
    native_receipt = closed_document(native_receipt_path, "receipt_sha256")
    native_cold = closed_document(native_cold_path, "receipt_sha256")
    need(native_receipt["authority_slot"] == "T04_DOUBLE_GRAPHS"
         and native_receipt["terminal_ordinal"] == 4
         and native_receipt["pair_contract"]["candidate_pairs"] == 1_362_088
         and native_receipt["pair_contract"]["native_candidate_ledger_sha256"]
             == file_sha(native_ledger)
         and native_receipt["pair_contract"]["unresolved"] == 0
         and native_receipt["pair_contract"]["legal_cross_component_witnesses"] == 0
         and native_receipt["pair_contract"]["physical_witness_ledger_rows"] == 0
         and native_receipt["formal_credit"] == 0, "native seal authority")
    need(native_cold["base_receipt_file_sha256"] == file_sha(native_receipt_path)
         and native_cold["candidate_pairs"] == 1_362_088
         and native_cold["unique_candidate_ids"] == 1_362_088
         and native_cold["unresolved"] == 0
         and native_cold["legal_cross_component_witnesses"] == 0
         and native_cold["pre_post_sha256_identical"] is True
         and native_cold["pre_post_stat_identical"] is True
         and native_cold["formal_credit"] == 0, "native cold authority")

    output = Path(args.out_dir).resolve()
    need(not output.exists() and output.parent == AUDIT.resolve(),
         "fresh direct audit output")
    output.mkdir(parents=True)
    db_path = output / ".correction_v2_staging.sqlite3"
    db = sqlite3.connect(db_path)
    try:
        db.execute("PRAGMA journal_mode=OFF")
        db.execute("PRAGMA synchronous=OFF")
        db.execute("PRAGMA temp_store=FILE")
        db.execute("CREATE TABLE staged (candidate_key TEXT PRIMARY KEY, "
                   "native_row_sha TEXT NOT NULL UNIQUE, candidate_id TEXT NOT NULL UNIQUE, "
                   "bucket TEXT NOT NULL, seed_rank TEXT NOT NULL, native_json BLOB NOT NULL)")
        census: Counter[str] = Counter()
        for source in native_rows(native_ledger):
            validate_native(source)
            key = candidate_key(source)
            seed_rank = hashlib.sha256((args.seed + "\0" + key).encode("ascii")).hexdigest()
            db.execute("INSERT INTO staged VALUES (?,?,?,?,?,?)",
                       (key, source["row_sha256"], source["candidate_id"],
                        source["bucket"], seed_rank, enc(source)))
            census[source["bucket"]] += 1
        db.commit()
        need(dict(census) == EXPECTED, "native exact bucket census")

        # A true-seed full pass: the two executions traverse the same authority
        # in different seed ranks, then independently emit canonical key order.
        seeded_census: Counter[str] = Counter()
        seeded_count = 0
        for bucket, raw in db.execute(
                "SELECT bucket,native_json FROM staged ORDER BY seed_rank,candidate_key"):
            source = json.loads(raw)
            validate_native(source)
            seeded_census[bucket] += 1
            seeded_count += 1
        need(seeded_count == 1_362_088 and dict(seeded_census) == EXPECTED,
             "seed-routed full authority pass")

        candidate_writer = Writer(
            output / "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz")
        absence_writer = Writer(
            output / "T04_DOUBLE_GRAPHS_terminal_absence_authority.jsonl.gz")
        proof_writer = Writer(
            output / "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz")
        for ordinal, (key, raw) in enumerate(db.execute(
                "SELECT candidate_key,native_json FROM staged ORDER BY candidate_key")):
            source = json.loads(raw)
            absence_key = ABSENCE_PREFIX + digest([
                key, source["row_sha256"], source["exact_disposition_route"]])
            absence = close({
                "schema": ABSENCE_SCHEMA,
                "ordinal": ordinal,
                "absence_authority_row_key": absence_key,
                "candidate_key": key,
                "terminal": "DOUBLE_GRAPHS",
                "terminal_ordinal": 4,
                "authority_slot": "T04_DOUBLE_GRAPHS",
                "native_candidate_id": source["candidate_id"],
                "native_candidate_key_sha256": source["candidate_key_sha256"],
                "native_bucket": source["bucket"],
                "native_authority_row_sha256": source["row_sha256"],
                "exact_disposition_route": source["exact_disposition_route"],
                "exact_physical_absence_evidence": source["exact_physical_proof"],
                "resolved": True,
                "unresolved": False,
                "legal_cross_component_same_physical_point_witness": False,
                "component_relation_disposition": DISPOSITION,
                "formal_credit": 0,
            })
            candidate = close({
                "schema": CANDIDATE_SCHEMA,
                "ordinal": ordinal,
                "candidate_key": key,
                "candidate_kind": "DOUBLE_GRAPHS_PRIMITIVE_PAIR",
                "candidate_pair_key_or_null": key,
                "terminal_ordinal": 4,
                "terminal": "DOUBLE_GRAPHS",
                "authority_slot": "T04_DOUBLE_GRAPHS",
                "primitive_authority_row_sha256": absence["row_sha256"],
                "component_relation_disposition": DISPOSITION,
                "physical_proof_row_count": 0,
                "physical_proof_row_sequence_sha256": EMPTY_SEQUENCE_SHA256,
                "formal_credit": 0,
            })
            absence_writer.write(absence)
            candidate_writer.write(candidate)

        candidate_desc = candidate_writer.finish(
            CANDIDATE_SCHEMA, "candidate_key", ["candidate_key"])
        absence_desc = absence_writer.finish(
            ABSENCE_SCHEMA, "absence_authority_row_key", ["candidate_key"])
        proof_desc = proof_writer.finish(
            PROOF_SCHEMA, "proof_row_key", ["candidate_key"])
        need(candidate_desc["row_count"] == absence_desc["row_count"] == 1_362_088
             and proof_desc["row_count"] == 0
             and proof_desc["row_sequence_sha256"] == EMPTY_SEQUENCE_SHA256,
             "correct candidate/absence/empty-proof census")
    finally:
        db.close()
    db_path.unlink()

    body = {
        "schema": (
            "cm2.c27-independent.t04-double-graphs.common-v2-typed-adapter-"
            "correction-receipt.v2"),
        "status": (
            "PASS_T04_1362088_COMMON_V2_CANDIDATES__EXACT_ABSENCE_AUTHORITY__"
            "ZERO_MATERIALIZED_PHYSICAL_PROOFS__ZERO_CREDIT"),
        "terminal": "DOUBLE_GRAPHS",
        "terminal_ordinal": 4,
        "authority_slot": "T04_DOUBLE_GRAPHS",
        "candidate_key_namespace": CANDIDATE_PREFIX,
        "absence_authority_key_namespace": ABSENCE_PREFIX,
        "candidate_ownership_ledger": candidate_desc,
        "terminal_absence_authority_ledger": absence_desc,
        "materialized_physical_proof_join_ledger": proof_desc,
        "exact_census": {
            "candidate_pairs": 1_362_088,
            "terminal_absence_authority_rows": 1_362_088,
            "physical_proof_rows": 0,
            "bucket_census": EXPECTED,
            "unresolved": 0,
            "legal_cross_component_witnesses": 0,
            "component_edges": 0,
        },
        "common_v2_contract": {
            "candidate_rows_ordered_by_candidate_key": True,
            "each_candidate_exactly_one_T04_owner": True,
            "candidate_pair_key_equals_candidate_key": True,
            "component_relation_disposition": DISPOSITION,
            "each_candidate_physical_proof_row_count": 0,
            "each_candidate_physical_proof_sequence_sha256": EMPTY_SEQUENCE_SHA256,
            "common_physical_proof_join_is_empty": True,
            "native_exact_absence_is_terminal_authority_not_physical_proof": True,
            "absence_authority_join_exact": True,
        },
        "source_authority": {
            "interface_v2_file_sha256": file_sha(interface_path),
            "interface_v2_object_sha256": interface_object_sha,
            "native_ledger_sha256": file_sha(native_ledger),
            "native_receipt_sha256": file_sha(native_receipt_path),
            "native_cold_replay_sha256": file_sha(native_cold_path),
        },
        "correction_governance": {
            "append_only": True,
            "quarantined_adapter_source":
                "deliverables/cm2_c27_t04_double_graphs_common_v2_typed_adapter_v1.py",
            "quarantined_attempt_directories": [
                ".cm2-runtime/audit/c27-t04-double-graphs-common-v2-adapter-v1-seed-30649101",
                ".cm2-runtime/audit/c27-t04-double-graphs-common-v2-adapter-v1-seed-30649991",
                ".cm2-runtime/audit/c27-t04-double-graphs-common-v2-adapter-v1-attempt2-seed-30649101",
                ".cm2-runtime/audit/c27-t04-double-graphs-common-v2-adapter-v1-attempt2-seed-30649991",
            ],
            "quarantine_reason": (
                "INVALID_CUSTOM_DISPOSITION_AND_EXACT_NONINCIDENCE_MISLABELED_AS_"
                "MATERIALIZED_PHYSICAL_PROOF_WITH_NULL_C15_EDGE_WITNESS_FIELDS"),
            "quarantined_outputs_may_not_be_consumed": True,
        },
        "active_seed_used_for_full_randomized_authority_pass_and_omitted_for_byte_identity": True,
        "formal_credit": 0,
        "manifest_authorized": False,
        "source_W_transition_authorized": False,
    }
    receipt = {**body, "receipt_sha256": digest(body)}
    receipt_path = output / "adapter_receipt.json"
    receipt_path.write_bytes(enc(receipt) + b"\n")
    members = [
        output / "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz",
        output / "T04_DOUBLE_GRAPHS_terminal_absence_authority.jsonl.gz",
        output / "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz",
        receipt_path,
    ]
    (output / "manifest.sha256").write_bytes(b"".join(
        file_sha(path).encode("ascii") + b"  " + path.name.encode("ascii") + b"\n"
        for path in sorted(members, key=lambda item: item.name)))
    print(enc({
        "status": receipt["status"],
        "candidate_pairs": 1_362_088,
        "absence_authority_rows": 1_362_088,
        "physical_proof_rows": 0,
        "candidate_ledger_sha256": candidate_desc["sha256"],
        "absence_ledger_sha256": absence_desc["sha256"],
        "empty_proof_ledger_sha256": proof_desc["sha256"],
        "receipt_sha256": receipt["receipt_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("T04_COMMON_V2_CORRECTION_ADAPTER_REJECT:" + str(exc))
        raise SystemExit(2)
