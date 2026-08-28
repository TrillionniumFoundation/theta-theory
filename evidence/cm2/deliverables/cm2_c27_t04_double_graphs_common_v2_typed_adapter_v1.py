#!/usr/bin/env python3
"""Adapt sealed native T04 pair rows to the corrected common-v2 interface."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
CANDIDATE_PREFIX = "round306c27-v5-t04-double-graphs-candidate:"
PROOF_PREFIX = "round306c27-v5-t04-double-graphs-physical-proof:"
EXPECTED = {"CROSS_CHART_QUOTIENT_RECHART": 1_361_424,
            "SAME_CHART_TRANSVERSE_1D": 448,
            "CROSS_CHART_GRAPH_SIDE_T0": 192,
            "CODIMENSION_TWO_LOWER_OWNER": 24}


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


def close(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def sequence(one: str) -> str:
    return hashlib.sha256(one.encode("ascii") + b"\n").hexdigest()


def native_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line); body = dict(row); claim = body.pop("row_sha256", None)
            need(claim == digest(body), "native row closure:" + str(ordinal))
            yield row


class Writer:
    def __init__(self, path: Path):
        self.path = path; self.raw = path.open("xb")
        self.gz = gzip.GzipFile(filename="", fileobj=self.raw, mode="wb", mtime=0)
        self.count = 0; self.seq = hashlib.sha256()
    def write(self, row: dict[str, Any]) -> None:
        body = dict(row); claim = body.pop("row_sha256", None)
        need(claim == digest(body), "adapter row closure")
        self.gz.write(enc(row) + b"\n"); self.seq.update(claim.encode("ascii") + b"\n")
        self.count += 1
    def finish(self, schema: str, unique: str) -> dict[str, Any]:
        self.gz.close(); self.raw.close()
        return {"path": str(self.path.resolve().relative_to(ROOT)), "sha256": sha(self.path),
                "size": self.path.stat().st_size, "row_count": self.count,
                "row_sequence_sha256": self.seq.hexdigest(), "row_schema": schema,
                "unique_key": unique, "ordering": ["ordinal"]}


def closed_document(path: Path, key: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes()); body = dict(value); claim = body.pop(key, None)
    need(claim == digest(body), "document closure:" + str(path)); return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--native-ledger", required=True); parser.add_argument("--native-ledger-sha256", required=True)
    parser.add_argument("--native-receipt", required=True); parser.add_argument("--native-receipt-sha256", required=True)
    parser.add_argument("--native-cold-replay", required=True); parser.add_argument("--native-cold-replay-sha256", required=True)
    parser.add_argument("--out-dir", required=True); parser.add_argument("--seed", required=True)
    args = parser.parse_args()
    need(args.seed in {"30649101", "30649991"}
         and os.environ.get("PYTHONHASHSEED") == args.seed,
         "active true adapter seed")
    need(sys.flags.isolated == 0 and sys.flags.ignore_environment == 0
         and sys.flags.hash_randomization == 1 and sys.flags.dont_write_bytecode == 1,
         "non-isolated seeded adapter runtime")
    need(hash("cm2-t04-common-v2-adapter-seed") == {
        "30649101": 1254683433925387923,
        "30649991": -1457501755408338885,
    }[args.seed], "active adapter seed fingerprint")
    native_ledger, native_receipt, cold_path = map(Path, (args.native_ledger, args.native_receipt, args.native_cold_replay))
    need(sha(native_ledger) == args.native_ledger_sha256
         and sha(native_receipt) == args.native_receipt_sha256
         and sha(cold_path) == args.native_cold_replay_sha256, "input pins")
    receipt = closed_document(native_receipt, "receipt_sha256")
    cold = closed_document(cold_path, "receipt_sha256")
    need(receipt["authority_slot"] == "T04_DOUBLE_GRAPHS"
         and receipt["terminal_ordinal"] == 4
         and receipt["pair_contract"]["candidate_pairs"] == 1_362_088
         and receipt["pair_contract"]["native_candidate_ledger_sha256"] == sha(native_ledger)
         and receipt["pair_contract"]["unresolved"] == 0
         and receipt["pair_contract"]["legal_cross_component_witnesses"] == 0
         and receipt["formal_credit"] == 0, "native terminal receipt")
    need(cold["base_receipt_file_sha256"] == sha(native_receipt)
         and cold["candidate_pairs"] == 1_362_088
         and cold["unique_candidate_ids"] == 1_362_088
         and cold["unresolved"] == 0 and cold["legal_cross_component_witnesses"] == 0
         and cold["pre_post_sha256_identical"] is True
         and cold["pre_post_stat_identical"] is True
         and cold["formal_credit"] == 0, "native cold receipt")
    output = Path(args.out_dir); need(not output.exists(), "fresh adapter output"); output.mkdir(parents=True)
    candidate_writer = Writer(output / "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz")
    proof_writer = Writer(output / "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz")
    census: Counter[str] = Counter(); seen: set[bytes] = set()
    for ordinal, native in enumerate(native_rows(native_ledger)):
        native_id_digest = hashlib.sha256(native["candidate_id"].encode("ascii")).digest()
        need(native_id_digest not in seen, "native candidate unique")
        seen.add(native_id_digest)
        candidate_key = CANDIDATE_PREFIX + digest({
            "native_candidate_id": native["candidate_id"],
            "native_candidate_key_sha256": native["candidate_key_sha256"],
            "terminal_ordinal": 4, "authority_slot": "T04_DOUBLE_GRAPHS"})
        proof_key = PROOF_PREFIX + digest([candidate_key, native["row_sha256"]])
        disposition = (
            "EXACT_TARGET_NONEDGE__COMPLETE_T0_OWNER_EQUALS_SOURCE_COMPONENT"
            if native["bucket"] == "CODIMENSION_TWO_LOWER_OWNER" else
            "EXACT_EMPTY_SAME_POINT_SOLUTION__COMPONENT_EDGE_IMPOSSIBLE")
        proof = close({
            "schema": PROOF_SCHEMA, "ordinal": ordinal,
            "proof_row_key": proof_key, "candidate_key": candidate_key,
            "atom_pair_incidence_key_or_null": None,
            "terminal": "DOUBLE_GRAPHS", "terminal_ordinal": 4,
            "authority_slot": "T04_DOUBLE_GRAPHS",
            "primitive_authority_row_sha256": native["row_sha256"],
            "ordered_C15_member_pair": None, "ordered_C15_component_pair": None,
            "component_edge_key": None, "physical_witness_key": None,
            "native_candidate_id": native["candidate_id"],
            "native_candidate_key": native["candidate_key"],
            "native_bucket": native["bucket"],
            "absence_disposition_route": native["exact_disposition_route"],
            "native_exact_physical_proof": native["exact_physical_proof"],
            "component_relation_disposition": disposition,
            "legal_cross_component_same_physical_point_witness": False,
            "formal_credit": 0,
        })
        candidate = close({
            "schema": CANDIDATE_SCHEMA, "ordinal": ordinal,
            "candidate_key": candidate_key,
            "candidate_kind": "DOUBLE_GRAPHS_PRIMITIVE_PAIR",
            "candidate_pair_key_or_null": None,
            "terminal_ordinal": 4, "terminal": "DOUBLE_GRAPHS",
            "authority_slot": "T04_DOUBLE_GRAPHS",
            "primitive_authority_row_sha256": native["row_sha256"],
            "component_relation_disposition": disposition,
            "physical_proof_row_count": 1,
            "physical_proof_row_sequence_sha256": sequence(proof["row_sha256"]),
            "formal_credit": 0,
        })
        proof_writer.write(proof); candidate_writer.write(candidate)
        census[native["bucket"]] += 1
    need(len(seen) == 1_362_088 and dict(census) == EXPECTED, "adapter exact census")
    candidate_desc = candidate_writer.finish(CANDIDATE_SCHEMA, "candidate_key")
    proof_desc = proof_writer.finish(PROOF_SCHEMA, "proof_row_key")
    need(candidate_desc["row_count"] == proof_desc["row_count"] == 1_362_088,
         "one materialized proof per candidate")
    body = {
        "schema": "cm2.c27-independent.t04-double-graphs.common-v2-typed-adapter-receipt.v1",
        "status": "PASS_T04_NATIVE_AUTHORITY_ADAPTED_TO_COMMON_CANDIDATE_OWNERSHIP_V2_WITH_ONE_MATERIALIZED_PROOF_PER_PAIR__ZERO_CREDIT",
        "terminal": "DOUBLE_GRAPHS", "terminal_ordinal": 4,
        "authority_slot": "T04_DOUBLE_GRAPHS",
        "candidate_key_namespace": CANDIDATE_PREFIX,
        "proof_key_namespace": PROOF_PREFIX,
        "candidate_ownership_ledger": candidate_desc,
        "materialized_physical_proof_join_ledger": proof_desc,
        "exact_census": {"candidate_pairs": 1_362_088,
                         "physical_proof_rows": 1_362_088,
                         "bucket_census": dict(census),
                         "unresolved": 0, "legal_cross_component_witnesses": 0,
                         "component_edges": 0},
        "common_v2_contract": {
            "candidate_key_is_not_atom_incidence_key": True,
            "each_candidate_exactly_one_terminal": True,
            "each_candidate_exactly_one_materialized_physical_proof": True,
            "physical_proof_sequence_bound_in_candidate_row": True,
            "component_disposition_materialized": True,
        },
        "source_authority": {"native_ledger_sha256": sha(native_ledger),
                             "native_receipt_sha256": sha(native_receipt),
                             "native_cold_replay_sha256": sha(cold_path)},
        "active_seed_intentionally_omitted_for_byte_identity": True,
        "formal_credit": 0, "manifest_authorized": False,
        "source_W_transition_authorized": False,
    }
    receipt_out = {**body, "receipt_sha256": digest(body)}
    (output / "adapter_receipt.json").write_bytes(enc(receipt_out) + b"\n")
    members = [output / "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz",
               output / "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz",
               output / "adapter_receipt.json"]
    (output / "manifest.sha256").write_bytes(b"".join(
        sha(path).encode("ascii") + b"  " + str(path.resolve().relative_to(ROOT)).encode("ascii") + b"\n"
        for path in sorted(members)))
    print(enc({"status": receipt_out["status"], "candidate_pairs": 1_362_088,
               "candidate_ledger_sha256": candidate_desc["sha256"],
               "proof_ledger_sha256": proof_desc["sha256"],
               "receipt_sha256": receipt_out["receipt_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except Reject as exc:
        print("T04_COMMON_V2_ADAPTER_REJECT:" + str(exc)); raise SystemExit(2)
