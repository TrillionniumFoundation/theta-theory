#!/usr/bin/env python3
"""Independent lockstep verifier for the T04 common-v2 typed adapter."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterator


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


def sequence(value: str) -> str:
    return hashlib.sha256(value.encode("ascii") + b"\n").hexdigest()


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line); body = dict(row); claim = body.pop("row_sha256", None)
            need(claim == digest(body), "row closure:" + path.name + ":" + str(ordinal))
            yield row


def doc(path: Path, key: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes()); body = dict(value); claim = body.pop(key, None)
    need(claim == digest(body), "document closure:" + path.name); return value


def no_extra(stream: Iterator[dict[str, Any]], label: str) -> None:
    try: next(stream)
    except StopIteration: return
    raise Reject("extra row:" + label)


def verify(native: Path, adapter: Path) -> tuple[dict[str, Any], dict[str, str]]:
    candidate_path = adapter / "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz"
    proof_path = adapter / "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz"
    receipt_path = adapter / "adapter_receipt.json"
    manifest_path = adapter / "manifest.sha256"
    receipt = doc(receipt_path, "receipt_sha256")
    need(receipt["terminal_ordinal"] == 4 and receipt["authority_slot"] == "T04_DOUBLE_GRAPHS"
         and receipt["candidate_key_namespace"] == CANDIDATE_PREFIX
         and receipt["proof_key_namespace"] == PROOF_PREFIX
         and receipt["exact_census"]["candidate_pairs"] == 1_362_088
         and receipt["exact_census"]["physical_proof_rows"] == 1_362_088
         and receipt["exact_census"]["bucket_census"] == EXPECTED
         and receipt["exact_census"]["unresolved"] == 0
         and receipt["exact_census"]["legal_cross_component_witnesses"] == 0
         and receipt["exact_census"]["component_edges"] == 0
         and receipt["formal_credit"] == 0 and receipt["manifest_authorized"] is False,
         "adapter receipt contract")
    need(receipt["source_authority"]["native_ledger_sha256"] == sha(native), "native ledger pin")
    entries = {}
    for line in manifest_path.read_text("ascii").splitlines():
        value, name = line.split("  ", 1); entries[name] = value
    for path in (candidate_path, proof_path, receipt_path):
        match = [value for name, value in entries.items() if name.endswith("/" + path.name)]
        need(match == [sha(path)], "adapter manifest:" + path.name)
    candidate_stream, proof_stream, native_stream = rows(candidate_path), rows(proof_path), rows(native)
    census: Counter[str] = Counter(); candidate_sequence = hashlib.sha256(); proof_sequence = hashlib.sha256()
    seen_candidate: set[bytes] = set(); seen_proof: set[bytes] = set()
    for ordinal, source in enumerate(native_stream):
        try: candidate, proof = next(candidate_stream), next(proof_stream)
        except StopIteration as exc: raise Reject("adapter omission:" + str(ordinal)) from exc
        candidate_key = CANDIDATE_PREFIX + digest({
            "native_candidate_id": source["candidate_id"],
            "native_candidate_key_sha256": source["candidate_key_sha256"],
            "terminal_ordinal": 4, "authority_slot": "T04_DOUBLE_GRAPHS"})
        proof_key = PROOF_PREFIX + digest([candidate_key, source["row_sha256"]])
        disposition = ("EXACT_TARGET_NONEDGE__COMPLETE_T0_OWNER_EQUALS_SOURCE_COMPONENT"
                       if source["bucket"] == "CODIMENSION_TWO_LOWER_OWNER" else
                       "EXACT_EMPTY_SAME_POINT_SOLUTION__COMPONENT_EDGE_IMPOSSIBLE")
        need(candidate["schema"] == CANDIDATE_SCHEMA and candidate["ordinal"] == ordinal
             and candidate["candidate_key"] == candidate_key
             and candidate["candidate_kind"] == "DOUBLE_GRAPHS_PRIMITIVE_PAIR"
             and candidate["candidate_pair_key_or_null"] is None
             and candidate["terminal_ordinal"] == 4 and candidate["terminal"] == "DOUBLE_GRAPHS"
             and candidate["authority_slot"] == "T04_DOUBLE_GRAPHS"
             and candidate["primitive_authority_row_sha256"] == source["row_sha256"]
             and candidate["component_relation_disposition"] == disposition
             and candidate["physical_proof_row_count"] == 1
             and candidate["physical_proof_row_sequence_sha256"] == sequence(proof["row_sha256"])
             and candidate["formal_credit"] == 0, "candidate exact adaptation")
        need(proof["schema"] == PROOF_SCHEMA and proof["ordinal"] == ordinal
             and proof["proof_row_key"] == proof_key and proof["candidate_key"] == candidate_key
             and proof["atom_pair_incidence_key_or_null"] is None
             and proof["terminal"] == "DOUBLE_GRAPHS" and proof["terminal_ordinal"] == 4
             and proof["authority_slot"] == "T04_DOUBLE_GRAPHS"
             and proof["primitive_authority_row_sha256"] == source["row_sha256"]
             and proof["ordered_C15_member_pair"] is None
             and proof["ordered_C15_component_pair"] is None
             and proof["component_edge_key"] is None and proof["physical_witness_key"] is None
             and proof["native_candidate_id"] == source["candidate_id"]
             and proof["native_candidate_key"] == source["candidate_key"]
             and proof["native_bucket"] == source["bucket"]
             and proof["absence_disposition_route"] == source["exact_disposition_route"]
             and proof["native_exact_physical_proof"] == source["exact_physical_proof"]
             and proof["component_relation_disposition"] == disposition
             and proof["legal_cross_component_same_physical_point_witness"] is False
             and proof["formal_credit"] == 0, "proof exact adaptation")
        ck, pk = hashlib.sha256(candidate_key.encode()).digest(), hashlib.sha256(proof_key.encode()).digest()
        need(ck not in seen_candidate and pk not in seen_proof, "adapter key uniqueness")
        seen_candidate.add(ck); seen_proof.add(pk)
        candidate_sequence.update(candidate["row_sha256"].encode() + b"\n")
        proof_sequence.update(proof["row_sha256"].encode() + b"\n")
        census[source["bucket"]] += 1
    no_extra(candidate_stream, "candidate"); no_extra(proof_stream, "proof")
    need(len(seen_candidate) == len(seen_proof) == 1_362_088 and dict(census) == EXPECTED,
         "adapter exact totals")
    cd, pd = receipt["candidate_ownership_ledger"], receipt["materialized_physical_proof_join_ledger"]
    need(cd["sha256"] == sha(candidate_path) and cd["row_count"] == 1_362_088
         and cd["row_sequence_sha256"] == candidate_sequence.hexdigest()
         and cd["row_schema"] == CANDIDATE_SCHEMA and cd["unique_key"] == "candidate_key"
         and pd["sha256"] == sha(proof_path) and pd["row_count"] == 1_362_088
         and pd["row_sequence_sha256"] == proof_sequence.hexdigest()
         and pd["row_schema"] == PROOF_SCHEMA and pd["unique_key"] == "proof_row_key",
         "adapter receipt ledgers")
    files = {"candidate_ledger_sha256": sha(candidate_path), "proof_ledger_sha256": sha(proof_path),
             "receipt_file_sha256": sha(receipt_path), "manifest_file_sha256": sha(manifest_path)}
    return receipt, files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--native-ledger", required=True); parser.add_argument("--adapter-a", required=True)
    parser.add_argument("--adapter-b", required=True); parser.add_argument("--output", required=True)
    args = parser.parse_args(); output = Path(args.output); need(not output.exists(), "fresh output")
    ra, fa = verify(Path(args.native_ledger), Path(args.adapter_a))
    adapter_b = Path(args.adapter_b)
    rb = doc(adapter_b / "adapter_receipt.json", "receipt_sha256")
    fb = {
        "candidate_ledger_sha256": sha(adapter_b / "T04_DOUBLE_GRAPHS_candidate_ownership.jsonl.gz"),
        "proof_ledger_sha256": sha(adapter_b / "T04_DOUBLE_GRAPHS_materialized_physical_proof_join.jsonl.gz"),
        "receipt_file_sha256": sha(adapter_b / "adapter_receipt.json"),
        "manifest_file_sha256": sha(adapter_b / "manifest.sha256"),
    }
    need(ra == rb and fa == fb, "dual adapter byte and semantic identity")
    body = {
        "schema": "cm2.c27-independent.t04-double-graphs.common-v2-typed-adapter-independent-verification.v1",
        "status": "PASS_NO_ADAPTER_IMPORT_LOCKSTEP_1362088_COMMON_V2_CANDIDATES_AND_PROOFS_DUAL_SEED_IDENTICAL",
        "candidate_pairs": 1_362_088, "physical_proof_rows": 1_362_088,
        "bucket_census": EXPECTED, "terminal_ordinal": 4,
        "authority_slot": "T04_DOUBLE_GRAPHS",
        "candidate_schema": CANDIDATE_SCHEMA, "proof_schema": PROOF_SCHEMA,
        "candidate_key_namespace": CANDIDATE_PREFIX, "proof_key_namespace": PROOF_PREFIX,
        "unresolved": 0, "legal_cross_component_witnesses": 0, "component_edges": 0,
        "adapter_source_imported": False, "dual_seed_all_files_byte_identical": True,
        "files": fa, "formal_credit": 0, "manifest_authorized": False,
    }
    wrapper = {**body, "verification_sha256": digest(body)}
    output.parent.mkdir(parents=True, exist_ok=True); output.write_bytes(enc(wrapper) + b"\n")
    print(enc(wrapper).decode("ascii")); return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except Reject as exc:
        print("T04_COMMON_V2_VERIFIER_REJECT:" + str(exc)); raise SystemExit(2)
