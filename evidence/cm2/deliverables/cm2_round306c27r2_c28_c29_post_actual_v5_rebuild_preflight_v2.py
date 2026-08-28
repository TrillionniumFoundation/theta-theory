#!/usr/bin/env python3
"""Fail-closed post-actual-v5 preflight for a fresh C27R2 -> C28 -> C29 rebuild.

This consumer is intentionally downstream of the actual primitive twenty-family
gate.  It never imports a producer module and never reads old C27 FAMILIES,
old transition ledgers, C28, C29, or a historical component-edge ledger as an
authority.  Until the corrected actual-v5 terminal receipt exists, it writes a
canonical append-only REJECT receipt and exits 2.

The PASS branch is already machine-specified.  It streams exactly 7,486,076
globally unique candidate ownership rows, conserves the three component
dispositions, materializes exactly 65,064 proof joins, independently derives
the component-pair union through the frozen C15 member map, and rebuilds a new
DSU on all 57,876 frozen components.  The historical-looking counts 14,860
edges and 43,684 final DSU components are diagnostics only: authority is the
exact proof-derived edge set and the fresh DSU computation, never those counts.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import tempfile
from typing import Any, Iterator


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent

CORRECTION = (WORKSPACE / ".cm2-runtime/audit/"
              "c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json")
ACTUAL = (WORKSPACE / ".cm2-runtime/audit/"
          "c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v2/receipt.json")
T00_FUTURE_SEAL = (WORKSPACE / ".cm2-runtime/audit/"
                   "c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-"
                   "zero-credit-seal-v1/receipt.json")
C15 = HERE / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"

ACTUAL_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-zero-credit-receipt.v2"
CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
EDGE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.full-component-edge-union.row.v2"

TERMINALS = (
    "SAME_CHART_RELATIVE_CELLS", "RETAINED_CONTINUATION", "OUTGOING_GRAPHS",
    "SINGLE_GRAPHS", "DOUBLE_GRAPHS", "SHEET_OWNER", "SHEET_SHADOW",
    "SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS", "INCLUDED_STRATUM_ATTACHMENTS",
    "REVERSE_RECHART", "TRUE_CYCLIC_SEAM_E_TO_N",
    "TRUE_CYCLIC_SEAM_N_TO_W", "TRUE_CYCLIC_SEAM_W_TO_S",
    "TRUE_CYCLIC_SEAM_S_TO_E", "Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL", "REPRESENTATION_ALIASES",
)
SLOTS = tuple(f"T{i:02d}_{name}" for i, name in enumerate(TERMINALS))

DISPOSITIONS = {
    "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 65_064,
    "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 264_156,
    "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 7_156_856,
}
EXPECTED_CANDIDATES = 7_486_076
EXPECTED_PROOFS = 65_064
FROZEN_MEMBERS = 502_204
FROZEN_COMPONENTS = 57_876
DIAGNOSTIC_EDGE_EXPECTATION = 14_860
DIAGNOSTIC_DSU_COMPONENT_EXPECTATION = 43_684

C15_PIN = (142_025_813, "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a")
CORRECTION_PIN = (6866, "6873b33d7b131a4bde0c4dbcf99873e6826cf2190fde6dfdf6640ee47d53c9d6")

# Only terminal receipts which are already sealed and cold-replayed are
# consumed here.  T00 and the actual gate remain explicit future blockers.
SEALED_INPUTS = (
    {
        "label": "T04_DOUBLE_GRAPHS",
        "receipt": ".cm2-runtime/audit/c27-t04-double-graphs-common-v2-correction-terminal-seal-v2/receipt.json",
        "receipt_pin": "007b9162a83d9cb665c72ec123253f6eab6d6b831e3225a0bafb585f256150d7",
        "receipt_closure": "receipt_sha256",
        "replay": ".cm2-runtime/audit/c27-t04-double-graphs-common-v2-correction-terminal-seal-v2-cold-replay/terminal_replay.json",
        "replay_pin": "a2601fa76add2d86ca87b12cdb16109d799bcc760ac491223e8a34036d44d87e",
        "replay_closure": "receipt_sha256",
        "candidate_count": 1_362_088,
        "proof_count": 0,
        "dispositions": {"NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 1_362_088},
    },
    {
        "label": "T01_T02_T03_T05_T06_T10",
        "receipt": ".cm2-runtime/audit/c27-legacy-terminal-common-v2-adapter-zero-credit-seal-v1/receipt.json",
        "receipt_pin": "4fd0ae953336743384967c1f3a05712df5cdcae4076240b75f73863829ea9598",
        "receipt_closure": "receipt_sha256",
        "replay": ".cm2-runtime/audit/c27-legacy-terminal-common-v2-adapter-postpublication-cold-terminal-replay-v1/terminal_replay.json",
        "replay_pin": "2f56d9cba3f0cb0e23a42c10c34795d63291087f5589de32e579ec925543c9b0",
        "replay_closure": "replay_sha256",
        "candidate_count": 52_064,
        "proof_count": 216,
        "dispositions": {
            "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 216,
            "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 40_792,
            "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 11_056,
        },
    },
    {
        "label": "T07_T08_T09",
        "receipt": ".cm2-runtime/audit/c27-primitive-v5-actual-three-terminal-pair-atom-adapters-v2-zero-credit-seal-v1/receipt.json",
        "receipt_pin": "6a9c5c28863948f2fb5c122b7d7139db6e774d328064e0c91d3c7a7172d17a1b",
        "receipt_closure": "receipt_sha256",
        "replay": ".cm2-runtime/audit/c27-primitive-v5-actual-three-terminal-pair-atom-adapters-v2-zero-credit-seal-v1-terminal-replay/terminal_replay.json",
        "replay_pin": "fbf7c43e933443b8fe11d06d0b927601d80cd3a0a056aab39f263d774134aa87",
        "replay_closure": "result_sha256",
        "candidate_count": 101_080,
        "proof_count": 32_608,
        "dispositions": {
            "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 32_608,
            "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 68_472,
        },
    },
    {
        "label": "T11_T19",
        "receipt": ".cm2-runtime/audit/c27-t11-t19-common-v2-zero-credit-seal-v1/receipt.json",
        "receipt_pin": "3a697d2e1e18aee57c3fed205193cf2b84fb9f305817544bf070e9741a8ac293",
        "receipt_closure": "receipt_sha256",
        "replay": ".cm2-runtime/audit/c27-t11-t19-common-v2-postpublication-cold-terminal-replay-v1/terminal_replay.json",
        "replay_pin": "5738daf2e15dace9a4e16204d93b1d4c5239918d52310b58fceeb01debb883b5",
        "replay_closure": "replay_sha256",
        "candidate_count": 4,
        "proof_count": 0,
        "dispositions": {"NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 4},
    },
)

FORBIDDEN_INPUTS = (
    "OLD_C27_FAMILIES", "OLD_C27_TRANSITION_LEDGER", "OLD_C28",
    "OLD_C29", "HISTORICAL_COMPONENT_EDGE_LEDGER_AS_AUTHORITY",
    "14772_AS_EDGE_AUTHORITY", "14724_AS_EDGE_AUTHORITY",
)


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid)


class Capture:
    def __init__(self, path: Path,
                 expected: tuple[int | None, str | None], label: str):
        self.path = path.resolve()
        self.label = label
        need(self.path.is_relative_to(WORKSPACE), label + ":workspace-bound")
        self.fd = os.open(self.path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        before = os.fstat(self.fd)
        need(stat.S_ISREG(before.st_mode), label + ":regular")
        self.before = fingerprint(before)
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        self.sha256 = state.hexdigest()
        need(fingerprint(os.fstat(self.fd)) == self.before, label + ":hash-fstat")
        size, sha = expected
        if size is not None:
            need(before.st_size == size, label + ":size-pin")
        if sha is not None:
            need(self.sha256 == sha, label + ":sha-pin")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        parts = []
        while block := os.read(self.fd, 4 << 20):
            parts.append(block)
        need(fingerprint(os.fstat(self.fd)) == self.before, self.label + ":raw-fstat")
        return b"".join(parts)

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        dup = os.dup(self.fd)
        with os.fdopen(dup, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as packed:
                for ordinal, line in enumerate(packed):
                    need(line.endswith(b"\n"), f"{self.label}:newline:{ordinal}")
                    payload = line[:-1]
                    row = json.loads(payload)
                    need(type(row) is dict and canonical(row) == payload,
                         f"{self.label}:canonical:{ordinal}")
                    body = dict(row)
                    claimed = body.pop("row_sha256", None)
                    need(type(claimed) is str and claimed == digest(body),
                         f"{self.label}:row-closure:{ordinal}")
                    yield row
        need(fingerprint(os.fstat(self.fd)) == self.before, self.label + ":rows-fstat")

    def attestation(self) -> dict[str, Any]:
        need(fingerprint(os.fstat(self.fd)) == self.before, self.label + ":attest-fstat")
        return {
            "path": str(self.path.relative_to(WORKSPACE)), "size": self.before[2],
            "sha256": self.sha256, "stat_fingerprint": list(self.before),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def closed_json(cap: Capture, closure: str) -> dict[str, Any]:
    value = json.loads(cap.raw())
    need(type(value) is dict, cap.label + ":object")
    body = dict(value)
    claimed = body.pop(closure, None)
    need(type(claimed) is str and claimed == digest(body), cap.label + ":closure")
    return value


def append_new(path: Path, value: dict[str, Any]) -> None:
    path = path.resolve()
    need(path.is_relative_to(WORKSPACE), "output:workspace-bound")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def descriptor(value: Any, name: str, schema: str) -> dict[str, Any]:
    need(type(value) is dict, name + ":descriptor")
    required = {"path", "size", "sha256", "row_count", "row_sequence_sha256",
                "row_schema", "ordering", "unique_key"}
    need(set(value) >= required, name + ":fields")
    need(value["row_schema"] == schema, name + ":schema")
    need(type(value["size"]) is int and value["size"] > 0, name + ":size")
    need(type(value["row_count"]) is int and value["row_count"] >= 0, name + ":rows")
    for field in ("sha256", "row_sequence_sha256"):
        need(type(value[field]) is str and len(value[field]) == 64, name + ":" + field)
    path = (WORKSPACE / value["path"]).resolve()
    need(path.is_relative_to(WORKSPACE), name + ":path")
    return value


def validate_current_seals() -> tuple[list[dict[str, Any]], list[Capture]]:
    captures: list[Capture] = []
    correction_cap = Capture(CORRECTION, CORRECTION_PIN, "corrected-interface-v2")
    captures.append(correction_cap)
    correction = closed_json(correction_cap, "preflight_sha256")
    need(correction["schema"] == "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-interface-correction-preflight.v2",
         "corrected-interface:schema")
    need(correction["corrected_interface"]["actual_gate_receipt"] == {
        "path": str(ACTUAL.relative_to(WORKSPACE)), "schema": ACTUAL_SCHEMA,
        "closure_field": "receipt_sha256"}, "corrected-interface:actual")
    need(correction["formal_credit"] == 0 and correction["manifest_authorized"] is False,
         "corrected-interface:nonpromotion")

    consumed = []
    for spec in SEALED_INPUTS:
        receipt_cap = Capture(WORKSPACE / spec["receipt"], (None, spec["receipt_pin"]),
                              spec["label"] + ":receipt")
        replay_cap = Capture(WORKSPACE / spec["replay"], (None, spec["replay_pin"]),
                             spec["label"] + ":replay")
        captures.extend((receipt_cap, replay_cap))
        receipt = closed_json(receipt_cap, spec["receipt_closure"])
        replay = closed_json(replay_cap, spec["replay_closure"])
        need(receipt.get("formal_credit") == 0 and receipt.get("manifest_authorized") is False,
             spec["label"] + ":receipt-nonpromotion")
        need(replay.get("formal_credit") == 0 and replay.get("manifest_authorized") is False,
             spec["label"] + ":replay-nonpromotion")
        consumed.append({
            "label": spec["label"], "candidate_count": spec["candidate_count"],
            "proof_count": spec["proof_count"], "dispositions": spec["dispositions"],
            "receipt": receipt_cap.attestation(), "receipt_object_sha256": receipt[spec["receipt_closure"]],
            "cold_replay": replay_cap.attestation(), "cold_replay_object_sha256": replay[spec["replay_closure"]],
        })
    return consumed, captures


def pipeline_contract() -> dict[str, Any]:
    return {
        "actual_gate_receipt": {
            "path": str(ACTUAL.relative_to(WORKSPACE)), "schema": ACTUAL_SCHEMA,
            "closure_field": "receipt_sha256", "required_top_level_descriptors": [
                "terminal_authority_descriptors", "materialized_ledger_descriptors"],
        },
        "terminal_order": list(TERMINALS), "authority_slot_order": list(SLOTS),
        "global_candidate_ownership": {
            "row_schema": CANDIDATE_SCHEMA, "ordering": ["candidate_key"],
            "unique_key": "candidate_key", "exact_rows": EXPECTED_CANDIDATES,
            "one_row_one_terminal": True, "streaming_validation": True,
        },
        "candidate_component_disposition_conservation": dict(DISPOSITIONS),
        "materialized_physical_proof_join": {
            "row_schema": PROOF_SCHEMA, "ordering": ["candidate_key", "proof_row_key"],
            "unique_key": "proof_row_key", "exact_rows": EXPECTED_PROOFS,
            "exactly_one_proof_for_each_cross_candidate": True,
            "zero_proofs_for_non_cross_candidates": True,
            "member_pair_rederived_through_frozen_C15": True,
        },
        "full_component_edge_union": {
            "row_schema": EDGE_SCHEMA, "ordering": ["component_edge_key"],
            "unique_key": "component_edge_key",
            "exact_authority": "DISTINCT_COMPONENT_PAIRS_DERIVED_FROM_ALL_65064_PROOF_MEMBER_PAIRS",
            "diagnostic_expected_count_not_authority": DIAGNOSTIC_EDGE_EXPECTATION,
            "historical_14772_or_14724_accepted_as_authority": False,
        },
        "fresh_C28": {
            "route_source": "EXACT_C27R2_MATERIALIZED_PROOF_JOIN_ROWS_ONLY",
            "component_pair_union_rederived_not_imported": True,
        },
        "fresh_C29": {
            "frozen_C15": {"members": FROZEN_MEMBERS, "components": FROZEN_COMPONENTS,
                           "path": str(C15.relative_to(WORKSPACE)),
                           "size": C15_PIN[0], "sha256": C15_PIN[1]},
            "fresh_DSU_from_all_frozen_components_and_exact_derived_edges": True,
            "diagnostic_expected_final_components_not_authority": DIAGNOSTIC_DSU_COMPONENT_EXPECTATION,
        },
        "forbidden_dependencies": {name: False for name in FORBIDDEN_INPUTS},
        "append_only_outputs": {
            "C27R2": "fresh-c27r2-candidate-proof-conservation.v2",
            "C28": "fresh-c28-proof-derived-component-pair-routing.v2",
            "C29": "fresh-c29-frozen-c15-exact-edge-dsu.v2",
        },
    }


class DSU:
    def __init__(self, components: set[str]):
        self.values = sorted(components)
        self.index = {value: i for i, value in enumerate(self.values)}
        self.parent = list(range(len(self.values)))
        self.size = [1] * len(self.values)
        self.merges = 0

    def find(self, i: int) -> int:
        while self.parent[i] != i:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i

    def union(self, left: str, right: str) -> None:
        a, b = self.find(self.index[left]), self.find(self.index[right])
        if a == b:
            return
        if self.size[a] < self.size[b] or (self.size[a] == self.size[b] and self.values[a] > self.values[b]):
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.merges += 1


def read_c15(cap: Capture) -> tuple[dict[str, str], set[str]]:
    members: dict[str, str] = {}
    components: set[str] = set()
    for ordinal, row in enumerate(cap.rows()):
        need(row["member_ordinal"] == ordinal, "C15:ordinal")
        member, component = row["registry_member_id"], row["fresh_component_id"]
        need(member not in members, "C15:duplicate-member")
        members[member] = component
        components.add(component)
    need(len(members) == FROZEN_MEMBERS and len(components) == FROZEN_COMPONENTS,
         "C15:census")
    return members, components


def validate_actual(actual_cap: Capture) -> dict[str, Any]:
    actual = closed_json(actual_cap, "receipt_sha256")
    need(actual.get("schema") == ACTUAL_SCHEMA, "actual:schema")
    need(actual.get("formal_credit") == 0 and actual.get("manifest_authorized") is False,
         "actual:nonpromotion")
    need(actual.get("source_W_transition_authorized") is False, "actual:source-W")
    need(type(actual.get("terminal_authority_descriptors")) is list
         and len(actual["terminal_authority_descriptors"]) == 20, "actual:20-authorities")
    need(actual.get("exact_census") == {
        "candidate_total": EXPECTED_CANDIDATES,
        "materialized_physical_proof_total": EXPECTED_PROOFS,
        "candidate_component_disposition_census": DISPOSITIONS,
    }, "actual:exact-census")
    ledgers = actual.get("materialized_ledger_descriptors")
    need(type(ledgers) is dict, "actual:ledger-descriptors")
    candidate_spec = descriptor(ledgers.get("candidate_ownership"), "candidate", CANDIDATE_SCHEMA)
    proof_spec = descriptor(ledgers.get("materialized_physical_proof_join"), "proof", PROOF_SCHEMA)
    edge_spec = descriptor(ledgers.get("full_component_edge_union"), "edge", EDGE_SCHEMA)
    need(candidate_spec["row_count"] == EXPECTED_CANDIDATES
         and candidate_spec["ordering"] == ["candidate_key"]
         and candidate_spec["unique_key"] == "candidate_key", "candidate:descriptor-contract")
    need(proof_spec["row_count"] == EXPECTED_PROOFS
         and proof_spec["ordering"] == ["candidate_key", "proof_row_key"]
         and proof_spec["unique_key"] == "proof_row_key", "proof:descriptor-contract")
    need(edge_spec["ordering"] == ["component_edge_key"]
         and edge_spec["unique_key"] == "component_edge_key", "edge:descriptor-contract")

    candidate_cap = Capture(WORKSPACE / candidate_spec["path"],
                            (candidate_spec["size"], candidate_spec["sha256"]), "actual:candidates")
    proof_cap = Capture(WORKSPACE / proof_spec["path"],
                        (proof_spec["size"], proof_spec["sha256"]), "actual:proofs")
    edge_cap = Capture(WORKSPACE / edge_spec["path"],
                       (edge_spec["size"], edge_spec["sha256"]), "actual:edges")
    c15_cap = Capture(C15, C15_PIN, "frozen-C15")
    opened = [candidate_cap, proof_cap, edge_cap, c15_cap]
    try:
        with tempfile.TemporaryDirectory(prefix="cm2-c27r2-v2-") as tmp:
            db = sqlite3.connect(str(Path(tmp) / "cross.sqlite"))
            db.execute("PRAGMA journal_mode=OFF")
            db.execute("PRAGMA synchronous=OFF")
            db.execute("CREATE TABLE cross_candidate(k TEXT PRIMARY KEY, terminal TEXT, slot TEXT, authority TEXT, row_sha TEXT, proof_seq TEXT)")
            counts: Counter[str] = Counter()
            previous = None
            candidate_sequence = hashlib.sha256()
            for ordinal, row in enumerate(candidate_cap.rows()):
                need(row.get("schema") == CANDIDATE_SCHEMA and row.get("ordinal") == ordinal,
                     "candidate:row-header")
                key = row.get("candidate_key")
                need(type(key) is str and (previous is None or previous < key), "candidate:global-order")
                previous = key
                terminal_ordinal = row.get("terminal_ordinal")
                need(type(terminal_ordinal) is int and 0 <= terminal_ordinal < 20,
                     "candidate:terminal-ordinal")
                need(row.get("terminal") == TERMINALS[terminal_ordinal]
                     and row.get("authority_slot") == SLOTS[terminal_ordinal], "candidate:terminal-owner")
                need(row.get("formal_credit") == 0, "candidate:credit")
                disposition = row.get("component_relation_disposition")
                need(disposition in DISPOSITIONS, "candidate:disposition")
                proof_count = row.get("physical_proof_row_count")
                need(proof_count == (1 if disposition.startswith("CROSS_COMPONENT") else 0),
                     "candidate:proof-count")
                counts[disposition] += 1
                candidate_sequence.update(row["row_sha256"].encode("ascii") + b"\n")
                if proof_count == 1:
                    db.execute("INSERT INTO cross_candidate VALUES (?,?,?,?,?,?)", (
                        key, row["terminal"], row["authority_slot"],
                        row["primitive_authority_row_sha256"], row["row_sha256"],
                        row["physical_proof_row_sequence_sha256"]))
            db.commit()
            need(sum(counts.values()) == EXPECTED_CANDIDATES and dict(counts) == DISPOSITIONS,
                 "candidate:conservation")
            need(candidate_sequence.hexdigest() == candidate_spec["row_sequence_sha256"],
                 "candidate:sequence")

            members, components = read_c15(c15_cap)
            support: defaultdict[str, list[str]] = defaultdict(list)
            edge_pairs: dict[str, tuple[str, str]] = {}
            proof_sequence = hashlib.sha256()
            previous_proof = None
            seen_proof_keys: set[str] = set()
            for ordinal, row in enumerate(proof_cap.rows()):
                need(row.get("schema") == PROOF_SCHEMA and row.get("ordinal") == ordinal,
                     "proof:row-header")
                order = (row.get("candidate_key"), row.get("proof_row_key"))
                need(all(type(x) is str for x in order)
                     and (previous_proof is None or previous_proof < order), "proof:order")
                previous_proof = order
                need(order[1] not in seen_proof_keys, "proof:duplicate-key")
                seen_proof_keys.add(order[1])
                found = db.execute("SELECT terminal,slot,authority,proof_seq FROM cross_candidate WHERE k=?", (order[0],)).fetchone()
                need(found is not None, "proof:owned-cross-candidate")
                terminal, slot, authority, expected_sequence = found
                need(row.get("terminal") == terminal and row.get("authority_slot") == slot
                     and row.get("primitive_authority_row_sha256") == authority, "proof:owner-binding")
                pair = row.get("ordered_C15_member_pair")
                need(type(pair) is list and len(pair) == 2 and pair == sorted(pair)
                     and pair[0] in members and pair[1] in members, "proof:member-pair")
                component_pair = sorted([members[pair[0]], members[pair[1]]])
                need(component_pair[0] != component_pair[1]
                     and row.get("ordered_C15_component_pair") == component_pair, "proof:component-map")
                edge = "round306c27r2-v5-component-edge:" + hashlib.sha256(canonical(component_pair)).hexdigest()
                need(row.get("component_edge_key") == edge, "proof:edge-key")
                need(row.get("formal_credit") == 0, "proof:credit")
                need(expected_sequence == hashlib.sha256((row["row_sha256"] + "\n").encode("ascii")).hexdigest(),
                     "proof:candidate-sequence-binding")
                db.execute("DELETE FROM cross_candidate WHERE k=?", (order[0],))
                support[edge].append(row["row_sha256"])
                edge_pairs[edge] = (component_pair[0], component_pair[1])
                proof_sequence.update(row["row_sha256"].encode("ascii") + b"\n")
            db.commit()
            need(len(seen_proof_keys) == EXPECTED_PROOFS
                 and db.execute("SELECT COUNT(*) FROM cross_candidate").fetchone()[0] == 0,
                 "proof:exact-join-conservation")
            need(proof_sequence.hexdigest() == proof_spec["row_sequence_sha256"], "proof:sequence")

            previous_edge = None
            edge_sequence = hashlib.sha256()
            seen_edges = set()
            for ordinal, row in enumerate(edge_cap.rows()):
                need(row.get("schema") == EDGE_SCHEMA and row.get("ordinal") == ordinal,
                     "edge:row-header")
                edge = row.get("component_edge_key")
                need(type(edge) is str and (previous_edge is None or previous_edge < edge), "edge:order")
                previous_edge = edge
                need(edge in edge_pairs and row.get("ordered_C15_component_pair") == list(edge_pairs[edge]),
                     "edge:exact-proof-derived-pair")
                hashes = support[edge]
                seq = hashlib.sha256(b"".join((h + "\n").encode("ascii") for h in hashes)).hexdigest()
                need(row.get("supporting_physical_proof_row_count") == len(hashes)
                     and row.get("supporting_physical_proof_row_sequence_sha256") == seq,
                     "edge:support-closure")
                need(row.get("formal_credit") == 0, "edge:credit")
                seen_edges.add(edge)
                edge_sequence.update(row["row_sha256"].encode("ascii") + b"\n")
            need(seen_edges == set(edge_pairs) and len(seen_edges) == edge_spec["row_count"],
                 "edge:exact-union")
            need(edge_sequence.hexdigest() == edge_spec["row_sequence_sha256"], "edge:sequence")

            dsu = DSU(components)
            for left, right in edge_pairs.values():
                dsu.union(left, right)
            final_components = FROZEN_COMPONENTS - dsu.merges
            return {
                "actual_receipt": actual_cap.attestation(),
                "candidate_rows": EXPECTED_CANDIDATES,
                "candidate_dispositions": dict(counts),
                "proof_rows": EXPECTED_PROOFS,
                "proof_derived_component_edges": len(edge_pairs),
                "diagnostic_edge_expectation": DIAGNOSTIC_EDGE_EXPECTATION,
                "diagnostic_edge_expectation_matches": len(edge_pairs) == DIAGNOSTIC_EDGE_EXPECTATION,
                "fresh_DSU_initial_components": FROZEN_COMPONENTS,
                "fresh_DSU_merges": dsu.merges,
                "fresh_DSU_final_components": final_components,
                "diagnostic_DSU_expectation": DIAGNOSTIC_DSU_COMPONENT_EXPECTATION,
                "diagnostic_DSU_expectation_matches": final_components == DIAGNOSTIC_DSU_COMPONENT_EXPECTATION,
                "count_diagnostics_used_as_authority": False,
                "ledger_attestations": [cap.attestation() for cap in opened],
            }
    finally:
        for cap in opened:
            cap.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    captures: list[Capture] = []
    try:
        consumed, captures = validate_current_seals()
        subtotal_dispositions: Counter[str] = Counter()
        for item in SEALED_INPUTS:
            subtotal_dispositions.update(item["dispositions"])
        subtotal_candidates = sum(item["candidate_count"] for item in SEALED_INPUTS)
        subtotal_proofs = sum(item["proof_count"] for item in SEALED_INPUTS)
        t00_expected = {
            "candidate_count": EXPECTED_CANDIDATES - subtotal_candidates,
            "proof_count": EXPECTED_PROOFS - subtotal_proofs,
            "dispositions": {key: DISPOSITIONS[key] - subtotal_dispositions[key]
                             for key in DISPOSITIONS},
            "future_seal_receipt_path": str(T00_FUTURE_SEAL.relative_to(WORKSPACE)),
        }
        need(t00_expected == {
            "candidate_count": 5_970_840, "proof_count": 32_240,
            "dispositions": {
                "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 32_240,
                "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 154_892,
                "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 5_783_708,
            },
            "future_seal_receipt_path": str(T00_FUTURE_SEAL.relative_to(WORKSPACE)),
        }, "T00:reconciliation")

        if not ACTUAL.is_file():
            body = {
                "schema": "cm2.round306c27r2-c28-c29.post-actual-v5-rebuild-preflight.v2",
                "status": "REJECT_ACTUAL_V5_TERMINAL_RECEIPT_V2_MISSING__PIPELINE_ARMED_FAIL_CLOSED_ZERO_CREDIT",
                "decision": "REJECT", "intended_process_exit_code": 2,
                "observed_actual_gate_receipt_present": False,
                "blocking_authorities": [
                    "ACTUAL_V5_TWENTY_FAMILY_TERMINAL_RECEIPT_V2",
                    "T00_SEALED_SUBAUTHORITY_TRANSITIVELY_REQUIRED_BY_ACTUAL_V5",
                ],
                "sealed_subauthorities_consumed": consumed,
                "sealed_subauthority_subtotal": {
                    "candidate_count": subtotal_candidates, "proof_count": subtotal_proofs,
                    "dispositions": dict(subtotal_dispositions),
                },
                "T00_expected_reconciliation_not_yet_consumed": t00_expected,
                "eventual_exact_global_conservation": {
                    "candidate_count": EXPECTED_CANDIDATES, "proof_count": EXPECTED_PROOFS,
                    "dispositions": dict(DISPOSITIONS),
                    "disposition_sum": sum(DISPOSITIONS.values()),
                },
                "pipeline_contract": pipeline_contract(),
                "corrected_interface_object_sha256": "3ece982b83b968e7cc23c4d43f2602fb5f8490484af5ed2f214515be4f0eb37e",
                "producer_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "fresh_C27R2_C28_C29_producer_may_start": False,
                "formal_credit": 0, "manifest_authorized": False,
                "C27R2": "UNAUTHORIZED", "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
                "Source_W_transition_authorized": False, "Source_W_formal_remainder": 80,
                "CM2": "NO-GO_FOR_CLAIM",
            }
            body["preflight_sha256"] = digest(body)
            append_new(Path(args.output), body)
            return 2

        actual_cap = Capture(ACTUAL, (None, None), "actual-v5-v2")
        result = validate_actual(actual_cap)
        actual_cap.close()
        body = {
            "schema": "cm2.round306c27r2-c28-c29.post-actual-v5-rebuild-preflight.v2",
            "status": "PASS_ACTUAL_V5_EXACT_CANDIDATE_PROOF_EDGE_DSU_PREFLIGHT__ZERO_CREDIT",
            "decision": "PASS", "intended_process_exit_code": 0,
            "sealed_subauthorities_consumed": consumed,
            "actual_validation": result, "pipeline_contract": pipeline_contract(),
            "producer_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "fresh_C27R2_C28_C29_producer_may_start": True,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "PREFLIGHT_ONLY_NOT_YET_MINTED", "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
            "Source_W_transition_authorized": False, "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        body["preflight_sha256"] = digest(body)
        append_new(Path(args.output), body)
        return 0
    except (Reject, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError,
            sqlite3.Error) as exc:
        print("REJECT:" + str(exc))
        return 2
    finally:
        for cap in captures:
            try:
                cap.close()
            except OSError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
