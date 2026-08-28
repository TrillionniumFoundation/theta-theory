#!/usr/bin/env python3
"""Fresh actual-v5 v2 assembler over twenty sealed terminal authorities.

The assembler never reads an old C27 family/transition artifact, C28/C29
artifact, or historical edge ledger.  It re-closes every global row, derives
the component-edge union only from materialized physical proof member pairs,
and runs a fresh DSU over the frozen C15 component denominator.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import heapq
import json
import os
from pathlib import Path
import random
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
INCIDENCE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.atom-pair-incidence.row.v2"
DISPOSITION_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.atom-incidence-disposition.row.v2"
EDGE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.full-component-edge-union.row.v2"
EDGE_PREFIX = "round306c27r2-v5-component-edge:"
TERMINALS = (
    "SAME_CHART_RELATIVE_CELLS", "RETAINED_CONTINUATION",
    "OUTGOING_GRAPHS", "SINGLE_GRAPHS", "DOUBLE_GRAPHS",
    "SHEET_OWNER", "SHEET_SHADOW", "SIGNED_BOUNDARY_FACES",
    "COMPLETE_BOUNDARY_FACES", "POSITIVE_VOLUME_CARRIERS",
    "INCLUDED_STRATUM_ATTACHMENTS", "REVERSE_RECHART",
    "TRUE_CYCLIC_SEAM_E_TO_N", "TRUE_CYCLIC_SEAM_N_TO_W",
    "TRUE_CYCLIC_SEAM_W_TO_S", "TRUE_CYCLIC_SEAM_S_TO_E",
    "Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL", "REPRESENTATION_ALIASES")
SLOTS = tuple(f"T{index:02d}_{terminal}"
              for index, terminal in enumerate(TERMINALS))
EXPECTED_CANDIDATES = (5_970_840, 276, 264, 4_984, 1_362_088,
                       17_940, 17_940, 25_452, 10_688, 64_940,
                       10_660, 0, 1, 1, 1, 1, 0, 0, 0, 0)
EXPECTED_PROOFS = (32_240, 0, 0, 216, 0, 0, 0, 0, 0, 32_608,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
EXPECTED_DISPOSITIONS = {
    "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 65_064,
    "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 264_156,
    "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 7_156_856,
}
C15 = (
    "deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz",
    "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a")
INTERFACE = (
    ".cm2-runtime/audit/c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json",
    "6873b33d7b131a4bde0c4dbcf99873e6826cf2190fde6dfdf6640ee47d53c9d6",
    "3ece982b83b968e7cc23c4d43f2602fb5f8490484af5ed2f214515be4f0eb37e")

# Each tuple is receipt, receipt file SHA, receipt object SHA, payload SHA,
# root SHA, cold replay, cold file SHA, cold object closure key/value.
SEALS = {
    "T00": (
        ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-zero-credit-seal-v1/receipt.json",
        "38e48470d487d65e6a70433bebc67f3e2068715aaf4bd4e008ca89d1ed128dc7",
        "8c13783792d9b9cd1752ef2f89f3cb7ac74499c92d33fc68c9cde64bab6b011e",
        "9b043a567323366dccbd5b4acd7b6dac09655822493bf0a38437bc7925a9eb82",
        "18ea6e69afe11e14ef26318a411048b3ab606b42ed3d2eebac2b26d2056b5c8f",
        ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-zero-credit-seal-v1-terminal-replay/terminal_replay.json",
        "2ce21c14f1d0f5446fb759dd3730cac6578d566c0ea11442c9fafe382e4c47fb",
        "result_sha256",
        "a677884c3a8da3369d0fb636ef5fb80cc48b5b4a7d0d8f733da5c32568ae6964"),
    "legacy": (
        ".cm2-runtime/audit/c27-legacy-terminal-common-v2-adapter-zero-credit-seal-v1/receipt.json",
        "4fd0ae953336743384967c1f3a05712df5cdcae4076240b75f73863829ea9598",
        "e95bdbf3cd14a541f5b9f29b6c3c5c8b2907175b90c7313978bcd5a46967ba17",
        "bfadad9849859ce925473bd08f12e815ec716e5a053e9698acc1dea1b4591506",
        "c0d05a3230898a3fa69d1468678d7133def6dfeb3eab3aaf9d362e68aeff0444",
        ".cm2-runtime/audit/c27-legacy-terminal-common-v2-adapter-postpublication-cold-terminal-replay-v1/terminal_replay.json",
        "2f56d9cba3f0cb0e23a42c10c34795d63291087f5589de32e579ec925543c9b0",
        "replay_sha256",
        "cbe2a1086a4aae3eab1573a077d0ce41ba7739e948953f98a42b2e51927bf1a3"),
    "T04": (
        ".cm2-runtime/audit/c27-t04-double-graphs-common-v2-correction-terminal-seal-v2/receipt.json",
        "007b9162a83d9cb665c72ec123253f6eab6d6b831e3225a0bafb585f256150d7",
        "1a191f8c9a9097a92c1bdad859f632adf6a88725b2360adf63b4ee1aa2a9591b",
        "2b5420718a8bd005e666ce45dcb92f5e0c9695f928d277fa21791d7495cd8671",
        "1896f8ed9684c1158eecc3aa39cf30007afaccae960068eda9c35bb1cce59be1",
        ".cm2-runtime/audit/c27-t04-double-graphs-common-v2-correction-terminal-seal-v2-cold-replay/terminal_replay.json",
        "a2601fa76add2d86ca87b12cdb16109d799bcc760ac491223e8a34036d44d87e",
        "receipt_sha256",
        "341024c30865d04bb5fe7982eaac14932af4fca7e426ab1b861de8d67489dc79"),
    "T07_T09": (
        ".cm2-runtime/audit/c27-primitive-v5-actual-three-terminal-pair-atom-adapters-v2-zero-credit-seal-v1/receipt.json",
        "6a9c5c28863948f2fb5c122b7d7139db6e774d328064e0c91d3c7a7172d17a1b",
        "22c439ea471d76b0efd4368a3408bd67e3bb8e207cb4b47443b065e26a48a777",
        "6ec39202dd8d0eddc1d867c6172f788b64f1d120722b587e95013887022c78a4",
        "5ff8f8eaa02f96532802c35f1d14135908659185e56d7074a63536e46a91cca2",
        ".cm2-runtime/audit/c27-primitive-v5-actual-three-terminal-pair-atom-adapters-v2-zero-credit-seal-v1-terminal-replay/terminal_replay.json",
        "fbf7c43e933443b8fe11d06d0b927601d80cd3a0a056aab39f263d774134aa87",
        "result_sha256",
        "4fd5df25d61c4501bd60608192194030827cd27b6232d1ed4a46b38ef83d8ff7"),
    "T11_T19": (
        ".cm2-runtime/audit/c27-t11-t19-common-v2-zero-credit-seal-v1/receipt.json",
        "3a697d2e1e18aee57c3fed205193cf2b84fb9f305817544bf070e9741a8ac293",
        "c863e83dfec699e6f13408ca004b66ab32e9770f8c7e6acb9a49e41fa5eaeb46",
        "556eb98ba3a677f60f5d343027bfdeb9876b276cc974b82cf1ad7dfac5acbf98",
        "89d5c35b291c02aeb4176b5b6cd1d3f7c0fb5572949d9e87bb3504e88f03961a",
        ".cm2-runtime/audit/c27-t11-t19-common-v2-postpublication-cold-terminal-replay-v1/terminal_replay.json",
        "5738daf2e15dace9a4e16204d93b1d4c5239918d52310b58fceeb01debb883b5",
        "replay_sha256",
        "ce2e806071af942bbd39096d6d53e194fa643ac5205fd9029674e18ba39d8f4a"),
}
SOURCE_DOCUMENTS = {
    "legacy": (
        ".cm2-runtime/audit/c27-legacy-terminal-common-v2-adapter-v1-seed-30655101-r5/result.json",
        "7417f9c7ab3181c955769de6bfe4153704437961cb3b181d36a8ae612e71a87f",
        "result_sha256",
        "ffdd00feaa02e2efb7fd19b9bcd75972aad30eee3a7ac8bb3b6be020e0d4287b"),
    "T04": (
        ".cm2-runtime/audit/c27-t04-double-graphs-common-v2-adapter-correction-v2-attempt2-seed-30649101/adapter_receipt.json",
        "3422db03bd0034d0cb25c23bb2086a89b90df86681cedd97ff18fb6a3ab2ac23",
        "receipt_sha256",
        "2a830f60cd0bf8cee71792055a84bd6242be2e0ba76e9aafe83e5ed27da981d7"),
    "T11_T19": (
        ".cm2-runtime/audit/c27-t11-t19-common-v2-adapter-v1-seed-30658101/result.json",
        "02e3e4d3e61f20d5cf7d9bead5eb673224f1adb878f19980346a2c14cdb24965",
        "result_sha256",
        "d76ac7a9d9b90ee919015bf78628bd0611217e3a065ca4e40a49d52f28c30d9b"),
}


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


def close(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def strict_json(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key")
            result[key] = value
        return result

    def constant(value: str) -> None:
        raise Failure("non-finite JSON:" + value)

    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=constant)


def closed_document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "document newline:" + path.name)
    value = strict_json(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical document:" + path.name)
    body = dict(value)
    claim = body.pop(closure, None)
    need(type(claim) is str and claim == digest(body),
         "document closure:" + path.name)
    return value


def fixed_path(relative: str) -> Path:
    need(type(relative) is str and relative
         and not Path(relative).is_absolute(), "relative fixed path")
    pieces = Path(relative).parts
    need(all(piece not in {"", ".", ".."} for piece in pieces),
         "canonical fixed path")
    path = ROOT.joinpath(*pieces)
    current = ROOT
    for piece in pieces:
        current = current / piece
        need(not current.is_symlink(), "no symlink walk:" + relative)
    resolved = path.resolve()
    need(ROOT in resolved.parents, "fixed path inside workspace")
    return resolved


def parse_manifest(path: Path) -> list[tuple[str, str]]:
    rows = []
    seen = set()
    for ordinal, line in enumerate(path.read_text("ascii").splitlines()):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64,
             f"manifest row:{ordinal}")
        need(pieces[1] not in seen, "manifest unique path")
        seen.add(pieces[1])
        rows.append((pieces[0], pieces[1]))
    return rows


def validate_seal(label: str) -> tuple[dict[str, Any], dict[str, Any]]:
    record = SEALS[label]
    need(all(item != "PENDING" for item in record),
         "formal seal finalized:" + label)
    receipt_path = fixed_path(record[0])
    payload_path = receipt_path.parent / "payload_manifest.sha256"
    root_path = receipt_path.parent / "root_manifest.sha256"
    cold_path = fixed_path(record[5])
    need(fsha(receipt_path) == record[1]
         and fsha(payload_path) == record[3]
         and fsha(root_path) == record[4]
         and fsha(cold_path) == record[6], "seal file pins:" + label)
    receipt = closed_document(receipt_path, "receipt_sha256")
    cold = closed_document(cold_path, record[7])
    need(receipt["receipt_sha256"] == record[2]
         and cold[record[7]] == record[8]
         and receipt["formal_credit"] == cold["formal_credit"] == 0
         and receipt["manifest_authorized"] is False
         and cold["manifest_authorized"] is False
         and cold.get("base_receipt_sha256", cold.get("receipt_sha256"))
             == receipt["receipt_sha256"], "seal object/governance:" + label)
    payload_rows = parse_manifest(payload_path)
    root_expected = {
        f"{record[3]}  {payload_path.relative_to(ROOT)}",
        f"{record[1]}  {receipt_path.relative_to(ROOT)}"}
    root_observed = root_path.read_text("ascii").splitlines()
    need(len(root_observed) == 2 and set(root_observed) == root_expected,
         "root manifest:" + label)
    need(len(payload_rows) > 0, "nonempty payload manifest:" + label)
    return receipt, cold


def normalize_descriptor(raw: dict[str, Any], base: Path,
                         legacy_names: bool) -> dict[str, Any]:
    relative = raw["path"]
    need(type(relative) is str and not Path(relative).is_absolute(),
         "descriptor relative path")
    if relative.startswith(".cm2-runtime/") or relative.startswith("deliverables/"):
        path = fixed_path(relative)
    else:
        path = (base / relative).resolve()
        need(ROOT in path.parents and not path.is_symlink()
             and ".." not in Path(relative).parts,
             "relative descriptor path under source document")
    sha_key, size_key = (("file_sha256", "file_size") if legacy_names
                         else ("sha256", "size"))
    result = {"path": str(path.relative_to(ROOT)),
              "size": raw[size_key], "sha256": raw[sha_key],
              "row_count": raw["row_count"],
              "row_sequence_sha256": raw["row_sequence_sha256"],
              "row_schema": raw["row_schema"],
              "ordering": raw["ordering"],
              "unique_key": raw["unique_key"]}
    need(type(result["size"]) is int and result["size"] >= 0
         and type(result["row_count"]) is int and result["row_count"] >= 0
         and path.is_file() and path.stat().st_size == result["size"],
         "normalized descriptor file")
    return result


class LedgerReader:
    def __init__(self, descriptor: dict[str, Any], terminal_ordinal: int,
                 terminal: str, slot: str, kind: str):
        self.desc = descriptor
        self.path = fixed_path(descriptor["path"])
        self.terminal_ordinal = terminal_ordinal
        self.terminal = terminal
        self.slot = slot
        self.kind = kind
        need(self.path.stat().st_size == descriptor["size"]
             and fsha(self.path) == descriptor["sha256"],
             "ledger descriptor file:" + self.path.name)
        self.stream = gzip.open(self.path, "rb")
        self.count = 0
        self.sequence = hashlib.sha256()
        self.previous: Any = None

    def __iter__(self) -> Iterator[dict[str, Any]]:
        try:
            for line in self.stream:
                need(line.endswith(b"\n"), "ledger newline:" + self.path.name)
                payload = line[:-1]
                row = strict_json(payload)
                need(type(row) is dict and canonical(row) == payload,
                     "canonical ledger row:" + self.path.name)
                body = dict(row)
                claim = body.pop("row_sha256", None)
                need(type(claim) is str and claim == digest(body),
                     "ledger row closure:" + self.path.name)
                need(type(row.get("ordinal")) is int
                     and row["ordinal"] == self.count
                     and row["formal_credit"] == 0,
                     "local ordinal/formal credit:" + self.path.name)
                if self.kind == "candidate":
                    need(row["schema"] == CANDIDATE_SCHEMA
                         and row["terminal_ordinal"] == self.terminal_ordinal
                         and row["terminal"] == self.terminal
                         and row["authority_slot"] == self.slot,
                         "candidate terminal binding")
                    key = row["candidate_key"]
                elif self.kind == "proof":
                    need(row["schema"] == PROOF_SCHEMA
                         and row["terminal"] == self.terminal
                         and row["authority_slot"] == self.slot,
                         "proof terminal binding")
                    key = (row["candidate_key"], row["proof_row_key"])
                elif self.kind == "incidence":
                    need(row["schema"] == INCIDENCE_SCHEMA,
                         "incidence schema")
                    key = (row["primitive_support_atom_key"],
                           row["candidate_pair_key"])
                else:
                    need(row["schema"] == DISPOSITION_SCHEMA,
                         "disposition schema")
                    key = row["primitive_support_atom_key"]
                need(self.previous is None or self.previous < key,
                     "strict source ordering:" + self.path.name)
                self.previous = key
                self.sequence.update(claim.encode("ascii") + b"\n")
                self.count += 1
                yield row
        finally:
            self.stream.close()
        need(self.count == self.desc["row_count"]
             and self.sequence.hexdigest()
                 == self.desc["row_sequence_sha256"],
             "source descriptor count/sequence:" + self.path.name)


class LedgerWriter:
    def __init__(self, path: Path, schema: str, ordering: list[str],
                 unique_key: Any):
        self.path = path
        self.schema = schema
        self.ordering = ordering
        self.unique_key = unique_key
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw = path.open("xb")
        self.stream = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw,
                                    mtime=0, compresslevel=1)

    def write(self, row: dict[str, Any]) -> None:
        need(row["schema"] == self.schema and row["ordinal"] == self.count,
             "output schema/ordinal")
        self.stream.write(canonical(row) + b"\n")
        self.sequence.update(row["row_sha256"].encode("ascii") + b"\n")
        self.count += 1

    def finish(self) -> dict[str, Any]:
        self.stream.close()
        self.raw.close()
        return {"path": str(self.path.relative_to(ROOT)),
                "size": self.path.stat().st_size,
                "sha256": fsha(self.path), "row_count": self.count,
                "row_sequence_sha256": self.sequence.hexdigest(),
                "row_schema": self.schema, "ordering": self.ordering,
                "unique_key": self.unique_key}


class DSU:
    def __init__(self, components: set[str]):
        self.parent = {item: item for item in components}
        self.size = {item: 1 for item in components}

    def find(self, item: str) -> str:
        parent = self.parent[item]
        while parent != self.parent[parent]:
            parent = self.parent[parent]
        while item != parent:
            next_item = self.parent[item]
            self.parent[item] = parent
            item = next_item
        return parent

    def union(self, left: str, right: str) -> bool:
        a, b = self.find(left), self.find(right)
        if a == b:
            return False
        if self.size[a] < self.size[b] or (self.size[a] == self.size[b]
                                          and b < a):
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


def load_authorities() -> tuple[list[dict[str, Any]], dict[str, Any],
                                dict[str, Any]]:
    interface_path = fixed_path(INTERFACE[0])
    need(fsha(interface_path) == INTERFACE[1], "interface file pin")
    interface = closed_document(interface_path, "preflight_sha256")
    need(interface["preflight_sha256"] == INTERFACE[2]
         and interface["corrected_interface"]["terminal_order"]
             == list(TERMINALS)
         and interface["corrected_interface"]["authority_slot_order"]
             == list(SLOTS), "corrected interface object/order")
    sealed = {label: validate_seal(label) for label in SEALS}
    documents = {}
    for label, (relative, file_pin, closure, object_pin) in SOURCE_DOCUMENTS.items():
        path = fixed_path(relative)
        need(fsha(path) == file_pin, "source document file pin:" + label)
        row = closed_document(path, closure)
        need(row[closure] == object_pin, "source document object pin:" + label)
        documents[label] = row
    need(sealed["legacy"][0]["evidence"]["result_file_sha256"]
             == SOURCE_DOCUMENTS["legacy"][1]
         and sealed["legacy"][0]["evidence"]["result_object_sha256"]
             == SOURCE_DOCUMENTS["legacy"][3]
         and sealed["T04"][0]["adapter_receipt_file_sha256"]
             == SOURCE_DOCUMENTS["T04"][1]
         and sealed["T11_T19"][0]["evidence"]["common_result_file_sha256"]
             == SOURCE_DOCUMENTS["T11_T19"][1]
         and sealed["T11_T19"][0]["evidence"]["common_result_object_sha256"]
             == SOURCE_DOCUMENTS["T11_T19"][3],
         "source documents bound by terminal seals")

    entries: dict[int, dict[str, Any]] = {}

    def add(index: int, seal_label: str, source_relative: str,
            candidate: dict[str, Any], proof: dict[str, Any],
            base: Path, legacy_names: bool) -> None:
        need(index not in entries, "unique terminal entry")
        cand = normalize_descriptor(candidate, base, legacy_names)
        physical = normalize_descriptor(proof, base, legacy_names)
        need(cand["row_schema"] == CANDIDATE_SCHEMA
             and cand["row_count"] == EXPECTED_CANDIDATES[index]
             and cand["ordering"] == ["candidate_key"]
             and cand["unique_key"] == "candidate_key"
             and physical["row_schema"] == PROOF_SCHEMA
             and physical["row_count"] == EXPECTED_PROOFS[index]
             and physical["unique_key"] == "proof_row_key",
             "terminal descriptor contract:" + SLOTS[index])
        source_path = fixed_path(source_relative)
        seal = SEALS[seal_label]
        entries[index] = {
            "terminal_ordinal": index, "terminal": TERMINALS[index],
            "authority_slot": SLOTS[index],
            "formal_terminal_seal_receipt_path": seal[0],
            "formal_terminal_seal_receipt_file_sha256": seal[1],
            "formal_terminal_seal_receipt_object_sha256": seal[2],
            "formal_terminal_cold_replay_path": seal[5],
            "formal_terminal_cold_replay_file_sha256": seal[6],
            "source_document_path": source_relative,
            "source_document_file_sha256": fsha(source_path),
            "candidate_ownership_ledger": cand,
            "materialized_physical_proof_join_ledger": physical,
        }

    t00_receipt = sealed["T00"][0]
    t00 = t00_receipt["terminal_adapter"]
    need(t00_receipt["exact_census"]["candidate_count"] == 5_970_840
         and t00_receipt["exact_census"]
             ["lower_dimension0_1_2_candidate_count"] == 5_783_708
         and t00_receipt["exact_census"]
             ["strict_dimension3_candidate_count"] == 187_132
         and t00_receipt["exact_census"]
             ["strict_cross_component_physical_proof_count"] == 32_240
         and t00_receipt["exact_census"]
             ["strict_same_component_no_edge_count"] == 154_892,
         "T00 exact terminal theorem")
    add(0, "T00", SEALS["T00"][0], t00["candidate_ownership_ledger"],
        t00["materialized_physical_proof_fragment_ledger"], ROOT, False)

    legacy_path = fixed_path(SOURCE_DOCUMENTS["legacy"][0])
    need(sealed["legacy"][0]["native_semantic_proof_incidence_total"]
             == 62_160
         and sealed["legacy"][0]["materialized_physical_proof_join_total"]
             == 216,
         "legacy semantic incidence is not physical proof")
    for item in documents["legacy"]["adapter_entries"]:
        index = item["terminal_ordinal"]
        need(index in {1, 2, 3, 5, 6, 10}
             and item["terminal"] == TERMINALS[index]
             and item["authority_slot"] == SLOTS[index],
             "legacy terminal identity")
        add(index, "legacy", SOURCE_DOCUMENTS["legacy"][0],
            item["candidate_ownership_ledger"],
            item["materialized_physical_proof_join_ledger"],
            legacy_path.parent, True)

    t04_path = fixed_path(SOURCE_DOCUMENTS["T04"][0])
    t04 = documents["T04"]
    need((t04["terminal_ordinal"], t04["terminal"], t04["authority_slot"])
         == (4, TERMINALS[4], SLOTS[4])
         and t04["exact_census"]["terminal_absence_authority_rows"]
             == 1_362_088
         and t04["exact_census"]["physical_proof_rows"] == 0,
         "corrected T04 identity/absence semantics")
    add(4, "T04", SOURCE_DOCUMENTS["T04"][0],
        t04["candidate_ownership_ledger"],
        t04["materialized_physical_proof_join_ledger"],
        t04_path.parent, False)

    t079 = sealed["T07_T09"][0]
    for item in t079["terminal_adapters"]:
        index = item["terminal_ordinal"]
        need(index in {7, 8, 9} and item["terminal"] == TERMINALS[index]
             and item["authority_slot"] == SLOTS[index],
             "T07-T09 terminal identity")
        add(index, "T07_T09", SEALS["T07_T09"][0],
            item["candidate_ownership_ledger"],
            item["materialized_physical_proof_fragment_ledger"], ROOT, False)

    t1119_path = fixed_path(SOURCE_DOCUMENTS["T11_T19"][0])
    need(sealed["T11_T19"][0]["auxiliary_authority_row_total"] == 328
         and sealed["T11_T19"][0]
             ["auxiliary_authority_is_not_candidate_or_materialized_physical_proof"]
             is True,
         "T11-T19 auxiliary nonpromotion")
    slot_by_index = {item["terminal_ordinal"]: item
                     for item in sealed["T11_T19"][0]["slot_census"]}
    for item in documents["T11_T19"]["adapter_entries"]:
        index = item["terminal_ordinal"]
        need(11 <= index <= 19 and item["terminal"] == TERMINALS[index]
             and item["authority_slot"] == SLOTS[index]
             and item["native_candidate_count"]
                 == slot_by_index[index]["native_candidate_count"],
             "T11-T19 terminal identity/seal alignment")
        add(index, "T11_T19", SOURCE_DOCUMENTS["T11_T19"][0],
            item["candidate_ownership_ledger"],
            item["materialized_physical_proof_join_ledger"],
            t1119_path.parent, True)
    need(set(entries) == set(range(20)), "all twenty terminal entries")
    return [entries[index] for index in range(20)], t079, interface


def load_c15() -> tuple[dict[str, str], set[str]]:
    path = fixed_path(C15[0])
    need(path.is_file() and fsha(path) == C15[1], "frozen C15 pin")
    members = {}
    components = set()
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), "C15 newline")
            payload = line[:-1]
            row = strict_json(payload)
            need(type(row) is dict and canonical(row) == payload
                 and type(row.get("member_ordinal")) is int
                 and row["member_ordinal"] == ordinal,
                 "C15 canonical/ordinal")
            body = dict(row)
            claim = body.pop("row_sha256", None)
            need(type(claim) is str and claim == digest(body),
                 "C15 row closure")
            member = row["registry_member_id"]
            component = row["fresh_component_id"]
            need(member not in members, "C15 unique member")
            members[member] = component
            components.add(component)
    need(len(members) == 502_204 and len(components) == 57_876,
         "frozen C15 census")
    return members, components


def merged_rows(entries: list[dict[str, Any]], kind: str,
                seed: int) -> Iterator[tuple[dict[str, Any], dict[str, Any]]]:
    order = list(range(20))
    random.Random(seed ^ (0xA51 if kind == "candidate" else 0xB72)).shuffle(order)
    heap: list[tuple[Any, int, dict[str, Any], Iterator[dict[str, Any]]]] = []
    for index in order:
        entry = entries[index]
        descriptor = entry["candidate_ownership_ledger" if kind == "candidate"
                           else "materialized_physical_proof_join_ledger"]
        reader = LedgerReader(descriptor, index, entry["terminal"],
                              entry["authority_slot"], kind)
        iterator = iter(reader)
        try:
            row = next(iterator)
        except StopIteration:
            continue
        key = (row["candidate_key"] if kind == "candidate" else
               (row["candidate_key"], row["proof_row_key"]))
        heapq.heappush(heap, (key, index, row, iterator))
    previous = None
    while heap:
        key, index, row, iterator = heapq.heappop(heap)
        need(previous is None or previous < key,
             "global unique strict " + kind + " ordering")
        previous = key
        yield row, entries[index]
        try:
            following = next(iterator)
        except StopIteration:
            continue
        following_key = (following["candidate_key"] if kind == "candidate"
                         else (following["candidate_key"],
                               following["proof_row_key"]))
        heapq.heappush(heap, (following_key, index, following, iterator))


def sequence(hashes: list[str]) -> str:
    state = hashlib.sha256()
    for value in hashes:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def manifest_entry(path: Path) -> str:
    return f"{fsha(path)}  {path.relative_to(ROOT)}\n"


def write_exclusive(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def build(out_dir: Path, seed: int) -> dict[str, Any]:
    need(type(seed) is int and seed > 0 and not out_dir.exists(),
         "positive seed/fresh output")
    entries, t079_receipt, interface = load_authorities()
    members, components = load_c15()
    out_dir.mkdir(parents=True)

    proof_writer = LedgerWriter(
        out_dir / "materialized_physical_proof_join.jsonl.gz",
        PROOF_SCHEMA, ["candidate_key", "proof_row_key"], "proof_row_key")
    source_proof_hashes: dict[str, list[str]] = defaultdict(list)
    actual_proof_hashes: dict[str, list[str]] = defaultdict(list)
    proof_terminal_census = Counter()
    terminal_edge_sets: dict[int, set[str]] = defaultdict(set)
    edge_support: dict[str, tuple[list[str], list[str]]] = {}
    for row, entry in merged_rows(entries, "proof", seed):
        member_pair = row["ordered_C15_member_pair"]
        component_pair = row["ordered_C15_component_pair"]
        need(type(member_pair) is list and len(member_pair) == 2
             and member_pair[0] < member_pair[1]
             and all(member in members for member in member_pair),
             "proof ordered known C15 member pair")
        remapped = sorted((members[member_pair[0]], members[member_pair[1]]))
        need(type(component_pair) is list and len(component_pair) == 2
             and component_pair[0] < component_pair[1]
             and component_pair == remapped,
             "proof component pair freshly remapped through C15")
        edge_key = EDGE_PREFIX + digest(component_pair)
        need(row["component_edge_key"] == edge_key,
             "proof component edge key derivation")
        source_proof_hashes[row["candidate_key"]].append(row["row_sha256"])
        body = dict(row)
        body.pop("row_sha256")
        body["ordinal"] = proof_writer.count
        actual = close(body)
        proof_writer.write(actual)
        actual_proof_hashes[row["candidate_key"]].append(actual["row_sha256"])
        proof_terminal_census[entry["terminal_ordinal"]] += 1
        terminal_edge_sets[entry["terminal_ordinal"]].add(edge_key)
        if edge_key not in edge_support:
            edge_support[edge_key] = (component_pair, [])
        need(edge_support[edge_key][0] == component_pair,
             "edge key unique component pair")
        edge_support[edge_key][1].append(actual["row_sha256"])
    proof_descriptor = proof_writer.finish()
    need(tuple(proof_terminal_census[index] for index in range(20))
             == EXPECTED_PROOFS
         and proof_descriptor["row_count"] == 65_064
         and len(terminal_edge_sets[0]) == 14_772
         and len(terminal_edge_sets[3]) == 88
         and len(terminal_edge_sets[9]) == 14_724
         and terminal_edge_sets[9].issubset(terminal_edge_sets[0])
         and terminal_edge_sets[3].isdisjoint(terminal_edge_sets[0]),
         "global physical proof census")

    candidate_writer = LedgerWriter(
        out_dir / "candidate_ownership.jsonl.gz", CANDIDATE_SCHEMA,
        ["candidate_key"], "candidate_key")
    candidate_terminal_census = Counter()
    disposition_census = Counter()
    source_t079_owner: dict[str, str] = {}
    actual_t079_owner: dict[str, str] = {}
    t079_terminal: dict[str, str] = {}
    proof_candidate_seen = set()
    for row, entry in merged_rows(entries, "candidate", seed):
        key = row["candidate_key"]
        old_hashes = source_proof_hashes.get(key, [])
        new_hashes = actual_proof_hashes.get(key, [])
        need(row["physical_proof_row_count"] == len(old_hashes)
             and row["physical_proof_row_sequence_sha256"]
                 == sequence(old_hashes),
             "source candidate/proof exact join")
        disposition = row["component_relation_disposition"]
        need(disposition in EXPECTED_DISPOSITIONS
             and ((disposition
                   == "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED")
                  == (len(old_hashes) > 0)),
             "candidate disposition/proof equivalence")
        if old_hashes:
            proof_candidate_seen.add(key)
        body = dict(row)
        body.pop("row_sha256")
        body["ordinal"] = candidate_writer.count
        body["physical_proof_row_count"] = len(new_hashes)
        body["physical_proof_row_sequence_sha256"] = sequence(new_hashes)
        actual = close(body)
        candidate_writer.write(actual)
        index = entry["terminal_ordinal"]
        candidate_terminal_census[index] += 1
        disposition_census[disposition] += 1
        if index in {7, 8, 9}:
            source_t079_owner[key] = row["row_sha256"]
            actual_t079_owner[key] = actual["row_sha256"]
            t079_terminal[key] = entry["terminal"]
    candidate_descriptor = candidate_writer.finish()
    need(tuple(candidate_terminal_census[index] for index in range(20))
             == EXPECTED_CANDIDATES
         and candidate_descriptor["row_count"] == 7_486_076
         and dict(disposition_census) == EXPECTED_DISPOSITIONS
         and proof_candidate_seen == set(source_proof_hashes)
         and set(source_proof_hashes) == set(actual_proof_hashes)
         and len(source_t079_owner) == 101_080,
         "global candidate census/conservation/proof totality")

    incidence_source = normalize_descriptor(
        t079_receipt["atom_pair_incidence_ledger"], ROOT, False)
    incidence_reader = LedgerReader(incidence_source, 7, TERMINALS[7],
                                    SLOTS[7], "incidence")
    incidence_writer = LedgerWriter(
        out_dir / "atom_pair_incidence.jsonl.gz", INCIDENCE_SCHEMA,
        ["primitive_support_atom_key", "candidate_pair_key"],
        ["primitive_support_atom_key", "candidate_pair_key"])
    old_atom_hashes: dict[str, list[str]] = defaultdict(list)
    new_atom_hashes: dict[str, list[str]] = defaultdict(list)
    atom_terminals: dict[str, set[str]] = defaultdict(set)
    incidence_candidates = set()
    incidence_keys = set()
    incidence_terminal_census = Counter()
    for row in incidence_reader:
        candidate = row["candidate_pair_key"]
        atom = row["primitive_support_atom_key"]
        terminal = row["candidate_terminal"]
        need(candidate in source_t079_owner
             and terminal == t079_terminal[candidate]
             and row["candidate_owner_row_sha256"]
                 == source_t079_owner[candidate]
             and row["incidence_key"] not in incidence_keys,
             "incidence exact candidate owner/terminal/key binding")
        incidence_keys.add(row["incidence_key"])
        incidence_candidates.add(candidate)
        old_atom_hashes[atom].append(row["row_sha256"])
        atom_terminals[atom].add(terminal)
        incidence_terminal_census[terminal] += 1
        body = dict(row)
        body.pop("row_sha256")
        body["ordinal"] = incidence_writer.count
        body["candidate_owner_row_sha256"] = actual_t079_owner[candidate]
        actual = close(body)
        incidence_writer.write(actual)
        new_atom_hashes[atom].append(actual["row_sha256"])
    incidence_descriptor = incidence_writer.finish()
    need(incidence_descriptor["row_count"] == 206_632
         and incidence_candidates == set(source_t079_owner)
         and dict(incidence_terminal_census) == {
             "SIGNED_BOUNDARY_FACES": 55_536,
             "COMPLETE_BOUNDARY_FACES": 30_624,
             "POSITIVE_VOLUME_CARRIERS": 120_472},
         "incidence exact census/candidate coverage")

    disposition_source = normalize_descriptor(
        t079_receipt["atom_incidence_disposition_ledger"], ROOT, False)
    disposition_reader = LedgerReader(disposition_source, 7, TERMINALS[7],
                                      SLOTS[7], "disposition")
    disposition_writer = LedgerWriter(
        out_dir / "atom_incidence_disposition.jsonl.gz", DISPOSITION_SCHEMA,
        ["primitive_support_atom_key"], "primitive_support_atom_key")
    incident_atoms = complement_atoms = multi_terminal_atoms = 0
    disposition_atoms = set()
    for row in disposition_reader:
        atom = row["primitive_support_atom_key"]
        need(atom not in disposition_atoms, "unique disposition atom")
        disposition_atoms.add(atom)
        old_hashes = old_atom_hashes.get(atom, [])
        new_hashes = new_atom_hashes.get(atom, [])
        terminals = sorted(atom_terminals.get(atom, set()))
        expected_disposition = ("EXACT_NONEMPTY_ATOM_PAIR_INCIDENCE_SET"
                                if old_hashes else
                                "EXACT_EMPTY_INCIDENCE_COMPLEMENT")
        need(row["incidence_count"] == len(old_hashes)
             and row["incidence_row_sequence_sha256"] == sequence(old_hashes)
             and row["terminal_set"] == terminals
             and row["disposition"] == expected_disposition,
             "source atom disposition exact incidence join")
        incident_atoms += int(bool(old_hashes))
        complement_atoms += int(not old_hashes)
        multi_terminal_atoms += int(len(terminals) > 1)
        body = dict(row)
        body.pop("row_sha256")
        body["ordinal"] = disposition_writer.count
        body["incidence_count"] = len(new_hashes)
        body["incidence_row_sequence_sha256"] = sequence(new_hashes)
        body["terminal_set"] = terminals
        body["disposition"] = expected_disposition
        disposition_writer.write(close(body))
    disposition_descriptor = disposition_writer.finish()
    need(disposition_descriptor["row_count"] == 483_232
         and set(old_atom_hashes) == set(new_atom_hashes)
         and set(old_atom_hashes).issubset(disposition_atoms)
         and incident_atoms == 62_768 and complement_atoms == 420_464
         and multi_terminal_atoms == 3_896,
         "atom disposition exact census/complement")

    edge_writer = LedgerWriter(
        out_dir / "full_component_edge_union.jsonl.gz", EDGE_SCHEMA,
        ["component_edge_key"], "component_edge_key")
    dsu = DSU(components)
    successful_merges = cycle_edges = 0
    for edge_key in sorted(edge_support):
        component_pair, proof_hashes = edge_support[edge_key]
        body = {"schema": EDGE_SCHEMA, "ordinal": edge_writer.count,
                "component_edge_key": edge_key,
                "ordered_C15_component_pair": component_pair,
                "supporting_physical_proof_row_count": len(proof_hashes),
                "supporting_physical_proof_row_sequence_sha256":
                    sequence(proof_hashes),
                "formal_credit": 0}
        edge_writer.write(close(body))
        if dsu.union(component_pair[0], component_pair[1]):
            successful_merges += 1
        else:
            cycle_edges += 1
    edge_descriptor = edge_writer.finish()
    final_components = len(components) - successful_merges
    need(edge_descriptor["row_count"] == 14_860
         and successful_merges == 14_192 and cycle_edges == 668
         and final_components == 43_684,
         "fresh proof-derived edge union/DSU census")

    descriptors = {
        "candidate_ownership": candidate_descriptor,
        "materialized_physical_proof_join": proof_descriptor,
        "atom_pair_incidence": incidence_descriptor,
        "atom_incidence_disposition": disposition_descriptor,
        "full_component_edge_union": edge_descriptor,
    }
    exact = {
        "candidate_total": candidate_descriptor["row_count"],
        "materialized_physical_proof_total": proof_descriptor["row_count"],
        "terminal_candidate_census": {
            TERMINALS[index]: candidate_terminal_census[index]
            for index in range(20)},
        "terminal_materialized_physical_proof_census": {
            TERMINALS[index]: proof_terminal_census[index]
            for index in range(20)},
        "candidate_component_disposition_census": dict(disposition_census),
        "atom_pair_incidence_total": incidence_descriptor["row_count"],
        "atom_pair_incidence_terminal_census": dict(incidence_terminal_census),
        "primitive_atom_denominator": disposition_descriptor["row_count"],
        "incident_atoms": incident_atoms,
        "exact_complement_atoms": complement_atoms,
        "multi_terminal_atoms": multi_terminal_atoms,
        "full_component_edge_union_total": edge_descriptor["row_count"],
        "frozen_C15_member_total": len(members),
        "frozen_C15_component_total": len(components),
        "fresh_DSU_successful_merges": successful_merges,
        "fresh_DSU_cycle_edges": cycle_edges,
        "fresh_DSU_final_component_total": final_components,
    }
    body = {
        "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-assembler-receipt.v2",
        "status": "PASS_FRESH_TWENTY_TERMINAL_GLOBAL_RECLOSURE_PROOF_DERIVED_EDGE_UNION_AND_DSU__PENDING_FINAL_ZERO_CREDIT_RECEIPT_V2",
        "execution_seed": seed,
        "seed_usage": "RANDOMIZED_TERMINAL_READER_INITIALIZATION__OUTPUT_SORTED_AND_SEED_INDEPENDENT",
        "interface_v2_file_sha256": INTERFACE[1],
        "interface_v2_object_sha256": interface["preflight_sha256"],
        "terminal_authority_descriptors": entries,
        "materialized_ledger_descriptors": descriptors,
        "exact_census": exact,
        "derivation_closures": {
            "candidate_pairs_each_exactly_one_terminal": True,
            "incidence_is_candidate": False,
            "candidate_proof_sequences_use_global_reclosed_proof_rows": True,
            "incidence_owner_hashes_use_global_reclosed_candidate_rows": True,
            "atom_dispositions_use_global_reclosed_incidence_rows": True,
            "component_edges_derived_only_from_physical_proof_member_pairs": True,
            "proof_member_pairs_freshly_remapped_through_frozen_C15": True,
            "fresh_DSU_starts_from_57876_singletons": True,
        },
        "forbidden_input_governance": {
            "old_C27_FAMILIES_imported_or_read": False,
            "old_transition_ledger_imported_or_read": False,
            "old_C28_or_C29_imported_or_read": False,
            "historical_edge_ledger_imported_or_read": False,
            "old_actual_v1_receipt_or_ledger_imported_or_read": False,
        },
        "formal_credit": 0, "manifest_authorized": False,
        "source_W_transition_authorized": False,
        "C27_C28_C29": "UNAUTHORIZED_PENDING_FINAL_RECEIPT_V2",
        "CM2": "NO-GO_FOR_CLAIM",
        "assembler_source_sha256": fsha(Path(__file__).resolve()),
    }
    receipt = dict(body)
    receipt["assembler_receipt_sha256"] = digest(receipt)
    receipt_path = out_dir / "assembler_receipt.json"
    write_exclusive(receipt_path, canonical(receipt) + b"\n")

    payload_paths = {Path(__file__).resolve(), fixed_path(C15[0]),
                     fixed_path(INTERFACE[0])}
    for record in SEALS.values():
        receipt_input = fixed_path(record[0])
        payload_paths.update((receipt_input,
                              receipt_input.parent / "payload_manifest.sha256",
                              receipt_input.parent / "root_manifest.sha256",
                              fixed_path(record[5])))
    for record in SOURCE_DOCUMENTS.values():
        payload_paths.add(fixed_path(record[0]))
    for entry in entries:
        payload_paths.add(fixed_path(entry["candidate_ownership_ledger"]["path"]))
        payload_paths.add(fixed_path(
            entry["materialized_physical_proof_join_ledger"]["path"]))
    payload_paths.add(fixed_path(incidence_source["path"]))
    payload_paths.add(fixed_path(disposition_source["path"]))
    payload_paths.update(fixed_path(desc["path"]) for desc in descriptors.values())
    payload_paths.add(receipt_path)
    manifest = "".join(sorted(manifest_entry(path) for path in payload_paths))
    write_exclusive(out_dir / "manifest.sha256", manifest.encode("ascii"))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        receipt = build(Path(args.out_dir).resolve(), args.seed)
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": receipt["status"],
                     "exact_census": receipt["exact_census"],
                     "assembler_receipt_sha256":
                         receipt["assembler_receipt_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
