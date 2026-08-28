#!/usr/bin/env python3
"""Fail-closed consumer preflight for a fresh C27R2 rebuild.

This is not a C27 producer and can never authorize C27, C28, or C29.  Its
only complete-input authority is the future *actual* primitive twenty-family
v5 terminal receipt.  In particular, it never imports an old C27 FAMILIES or
transition table, C28, C29, or any historical component-edge ledger.  The
14,772 strict-volume and 14,724 scoped three-terminal edge sets are explicitly
not accepted as the global edge universe.

When the actual receipt is absent the program emits an append-only canonical
truthful REJECT and exits 2.  The receipt contract below locks the normalized
primitive-authority, atomic-ownership, materialized-proof and final edge
interfaces needed by the later rebuild.  A future complete run derives every
component edge from proof member pairs through the frozen C15 map, compares
that derived set exactly with the actual-gate edge ledger, rebuilds a new DSU,
and checks atomic ownership against all twenty normalized primitive ledgers.
Even such a complete run is only an input preflight; formal state remains
unauthorized until a separate C27R2 producer/verifier/seal chain exists.
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

C15 = HERE / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
ACTUAL_GATE_RECEIPT = (
    WORKSPACE / ".cm2-runtime/audit/"
    "c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v1/receipt.json"
)

C15_SIZE = 142_025_813
C15_SHA256 = "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"
ACTUAL_RECEIPT_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-zero-credit-receipt.v1"
)

TERMINALS = (
    "SAME_CHART_RELATIVE_CELLS",
    "RETAINED_CONTINUATION",
    "OUTGOING_GRAPHS",
    "SINGLE_GRAPHS",
    "DOUBLE_GRAPHS",
    "SHEET_OWNER",
    "SHEET_SHADOW",
    "SIGNED_BOUNDARY_FACES",
    "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS",
    "INCLUDED_STRATUM_ATTACHMENTS",
    "REVERSE_RECHART",
    "TRUE_CYCLIC_SEAM_E_TO_N",
    "TRUE_CYCLIC_SEAM_N_TO_W",
    "TRUE_CYCLIC_SEAM_W_TO_S",
    "TRUE_CYCLIC_SEAM_S_TO_E",
    "Jx_NEGATIVE_CONTROL",
    "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL",
    "REPRESENTATION_ALIASES",
)

AUTHORITY_SLOTS = tuple(
    f"T{ordinal:02d}_{terminal}" for ordinal, terminal in enumerate(TERMINALS)
)

NORMALIZED_AUTHORITY_ROW_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "normalized-primitive-authority.row.v1"
)
ATOMIC_ROW_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "atomic-ownership.row.v1"
)
PROOF_ROW_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "materialized-proof-row-join.row.v1"
)
EDGE_ROW_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "full-component-edge-union.row.v1"
)
EDGE_PREFIX = "round306c27r2-v5-component-edge:"

FORBIDDEN_DEPENDENCIES = (
    "OLD_C27_FAMILIES",
    "OLD_C27_TRANSITION_CANDIDATE_LEDGER",
    "OLD_C27_TRANSITION_FAMILY_COVERAGE_LEDGER",
    "OLD_C28_PAIR_ROUTING",
    "OLD_C29_PHYSICAL_MAXIMALITY",
    "HISTORICAL_EDGE_LEDGER_AS_CANDIDATE_UNIVERSE",
    "STRICT_VOLUME_14772_AS_GLOBAL_CANDIDATE_UNIVERSE",
    "SCOPED_THREE_TERMINAL_14724_AS_GLOBAL_CANDIDATE_UNIVERSE",
)


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


def sequence_digest(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid)


class Capture:
    """One stable, no-follow file description for hash/parse/fstat."""

    def __init__(self, path: Path, expected: tuple[int, str] | None, label: str):
        self.path = path.resolve()
        self.label = label
        need(self.path.is_relative_to(WORKSPACE), label + ":workspace-bound")
        self.fd = os.open(self.path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        before = os.fstat(self.fd)
        need(stat.S_ISREG(before.st_mode), label + ":regular")
        self.before = fingerprint(before)
        h = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            h.update(block)
        self.sha256 = h.hexdigest()
        need(fingerprint(os.fstat(self.fd)) == self.before, label + ":hash-fstat")
        if expected is not None:
            need(before.st_size == expected[0], label + ":size-pin")
            need(self.sha256 == expected[1], label + ":sha-pin")

    def unchanged(self, phase: str) -> None:
        need(fingerprint(os.fstat(self.fd)) == self.before,
             self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        self.unchanged("raw")
        return b"".join(chunks)

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
        self.unchanged("rows")

    def attestation(self) -> dict[str, Any]:
        self.unchanged("attestation")
        return {
            "path": str(self.path.relative_to(WORKSPACE)),
            "size": self.before[2],
            "sha256": self.sha256,
            "stat_fingerprint": list(self.before),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def closed_object(cap: Capture, field: str) -> dict[str, Any]:
    raw = cap.raw()
    payload = raw[:-1] if raw.endswith(b"\n") else raw
    need(payload and b"\n" not in payload, cap.label + ":single-object")
    value = json.loads(payload)
    need(type(value) is dict and canonical(value) == payload,
         cap.label + ":canonical-object")
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == digest(body),
         cap.label + ":object-closure")
    return value


def under_workspace(path_value: str, label: str) -> Path:
    need(type(path_value) is str and path_value != "", label + ":path")
    path = (WORKSPACE / path_value).resolve()
    need(path.is_relative_to(WORKSPACE), label + ":workspace-bound")
    return path


def ledger_spec(value: Any, label: str, schema: str, key_field: str) -> dict[str, Any]:
    need(type(value) is dict, label + ":object")
    required = {
        "path", "size", "sha256", "row_count", "row_sequence_sha256",
        "row_schema", "unique_key_field", "ordering",
    }
    need(set(value) >= required, label + ":required-fields")
    need(value["row_schema"] == schema, label + ":row-schema")
    need(value["unique_key_field"] == key_field, label + ":unique-key")
    need(type(value["size"]) is int and value["size"] > 0, label + ":size")
    need(type(value["row_count"]) is int and value["row_count"] >= 0,
         label + ":row-count")
    for field in ("sha256", "row_sequence_sha256"):
        need(type(value[field]) is str and len(value[field]) == 64,
             label + ":" + field)
    under_workspace(value["path"], label)
    return value


class DSU:
    def __init__(self, components: set[str]):
        self.values = sorted(components)
        self.index = {value: ordinal for ordinal, value in enumerate(self.values)}
        self.parent = list(range(len(self.values)))
        self.size = [1] * len(self.values)

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: str, right: str) -> int:
        a = self.find(self.index[left])
        b = self.find(self.index[right])
        if a == b:
            return 0
        if self.size[a] < self.size[b] or (
            self.size[a] == self.size[b] and self.values[a] > self.values[b]
        ):
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return 1


def interface_contract() -> dict[str, Any]:
    common = {
        "row_closure": "row_sha256=SHA256(canonical row without row_sha256)",
        "ledger_sequence": "SHA256_ASCII_ROW_SHA256_NEWLINE_IN_LEDGER_ORDER",
        "canonical_json": "ASCII_SORTED_KEYS_NO_WHITESPACE_NO_NAN_NEWLINE_DELIMITED",
    }
    return {
        "actual_gate_receipt": {
            "path": str(ACTUAL_GATE_RECEIPT.relative_to(WORKSPACE)),
            "schema": ACTUAL_RECEIPT_SCHEMA,
            "closure_field": "receipt_sha256",
            "required_state": {
                "formal_credit": 0,
                "manifest_authorized": False,
                "primitive_twenty_family_totality_proved": True,
                "terminal_count": 20,
                "open_terminal_count": 0,
                "unresolved": 0,
            },
        },
        "primitive_authorities": {
            "entry_count": 20,
            "terminal_order": list(TERMINALS),
            "authority_slot_order": list(AUTHORITY_SLOTS),
            "entry_fields": [
                "terminal_ordinal", "terminal", "authority_slot",
                "authority_receipt_path", "authority_receipt_size",
                "authority_receipt_sha256", "normalized_candidate_ledger",
            ],
            "normalized_candidate_ledger_row_schema": NORMALIZED_AUTHORITY_ROW_SCHEMA,
            "normalized_candidate_unique_key": "atomic_candidate_key",
            "normalized_candidate_required_fields": [
                "authority_candidate_ordinal", "atomic_candidate_key", "terminal",
                "authority_slot", "primitive_authority_row_sha256", "formal_credit",
                "row_sha256",
            ],
            **common,
        },
        "atomic_ownership_ledger": {
            "row_schema": ATOMIC_ROW_SCHEMA,
            "unique_key": "atomic_candidate_key",
            "ordering": ["atomic_candidate_key"],
            "required_fields": [
                "ordinal", "atomic_candidate_key", "terminal_ordinal", "terminal",
                "authority_slot", "primitive_authority_row_sha256", "disposition",
                "proof_row_count", "proof_row_sequence_sha256",
                "component_edge_key_count", "formal_credit", "row_sha256",
            ],
            "allowed_dispositions": [
                "NO_CROSS_COMPONENT_EDGE", "CROSS_COMPONENT_EDGE_PROVED",
            ],
            **common,
        },
        "materialized_proof_row_join_ledger": {
            "row_schema": PROOF_ROW_SCHEMA,
            "unique_key": "proof_row_key",
            "ordering": ["atomic_candidate_key", "proof_row_key"],
            "required_fields": [
                "ordinal", "proof_row_key", "atomic_candidate_key", "terminal",
                "authority_slot", "primitive_authority_row_sha256",
                "ordered_C15_member_pair", "ordered_C15_component_pair",
                "component_edge_key", "physical_witness_key", "formal_credit",
                "row_sha256",
            ],
            "component_edge_key_formula": (
                EDGE_PREFIX + "SHA256(canonical ordered_C15_component_pair)"
            ),
            **common,
        },
        "full_component_edge_union_ledger": {
            "row_schema": EDGE_ROW_SCHEMA,
            "unique_key": "component_edge_key",
            "ordering": ["ordered_C15_component_pair"],
            "required_fields": [
                "ordinal", "component_edge_key", "ordered_C15_component_pair",
                "proof_row_count", "proof_row_sequence_sha256", "terminal_census",
                "authority_slot_census", "formal_credit", "row_sha256",
            ],
            "authority_rule": (
                "EXACTLY_DERIVED_FROM_MATERIALIZED_PROOF_MEMBER_PAIRS_THROUGH_"
                "FROZEN_C15_MAP__NEVER_A_CANDIDATE_UNIVERSE"
            ),
            **common,
        },
        "fixed_census": {
            "frozen_C15_members": 502_204,
            "initial_frozen_C15_components": 57_876,
            "terminal_count": 20,
            "open_terminal_count": 0,
            "unresolved": 0,
        },
        "derived_not_hardcoded_census": [
            "global_atomic_candidate_count",
            "materialized_proof_row_count",
            "full_component_edge_count",
            "fresh_DSU_rank",
            "fresh_component_count",
        ],
        "scoped_not_global_census": {
            "three_terminal_pair_rows": 101_080,
            "three_terminal_atom_denominator": 483_232,
            "same_chart_strict_volume_rows": 187_132,
            "same_chart_lower_exact_contact_rows": 5_783_708,
            "may_be_summed_or_used_as_global_universe": False,
        },
    }


def parse_c15(cap: Capture) -> tuple[dict[str, str], set[str]]:
    member_to_component: dict[str, str] = {}
    components: set[str] = set()
    for ordinal, row in enumerate(cap.rows()):
        need(row.get("schema") ==
             "cm2.round306c15.source-g-502204-member-fresh-dsu-freeze.v1.member-component-row.v1",
             "C15:schema")
        need(row.get("member_ordinal") == ordinal, "C15:ordinal")
        member = row.get("registry_member_id")
        component = row.get("fresh_component_id")
        need(type(member) is str and member not in member_to_component,
             "C15:unique-member")
        need(type(component) is str, "C15:component")
        member_to_component[member] = component
        components.add(component)
    need((len(member_to_component), len(components)) == (502_204, 57_876),
         "C15:exact-census")
    return member_to_component, components


def validate_actual_gate(
    receipt_cap: Capture,
    member_to_component: dict[str, str],
    components: set[str],
    scratch_parent: Path,
) -> tuple[dict[str, Any], dict[str, Capture], dict[str, Any]]:
    """Validate the future interface without granting any formal authority."""
    receipt = closed_object(receipt_cap, "receipt_sha256")
    need(receipt.get("schema") == ACTUAL_RECEIPT_SCHEMA, "actual:schema")
    need(type(receipt.get("status")) is str and receipt["status"].startswith("PASS_"),
         "actual:PASS-status")
    need(receipt.get("formal_credit") == 0
         and receipt.get("manifest_authorized") is False,
         "actual:zero-credit")
    gate = receipt.get("actual_gate")
    need(type(gate) is dict, "actual:gate-object")
    need(gate.get("primitive_twenty_family_totality_proved") is True
         and gate.get("terminal_count") == 20
         and gate.get("open_terminal_count") == 0
         and gate.get("unresolved") == 0,
         "actual:closed-20-family-gate")
    forbidden = receipt.get("forbidden_input_governance")
    expected_forbidden = {
        "old_C27_FAMILIES_imported_or_read": False,
        "old_transition_ledger_imported_or_read": False,
        "C28_imported_or_read": False,
        "C29_imported_or_read": False,
        "historical_edge_ledger_used_as_candidate_universe": False,
        "strict_volume_14772_used_as_global_candidate_universe": False,
        "scoped_three_terminal_14724_used_as_global_candidate_universe": False,
    }
    need(forbidden == expected_forbidden, "actual:forbidden-input-governance")
    rebuild = receipt.get("fresh_rebuild_input")
    need(type(rebuild) is dict, "actual:fresh-rebuild-input")

    authorities = rebuild.get("primitive_authorities")
    need(type(authorities) is list and len(authorities) == 20,
         "actual:20-authorities")
    captures: dict[str, Capture] = {}
    authority_specs = []
    for ordinal, entry in enumerate(authorities):
        label = f"authority:{ordinal}"
        need(type(entry) is dict, label + ":object")
        need(entry.get("terminal_ordinal") == ordinal
             and entry.get("terminal") == TERMINALS[ordinal],
             label + ":terminal")
        slot = entry.get("authority_slot")
        need(slot == AUTHORITY_SLOTS[ordinal], label + ":slot")
        receipt_path = under_workspace(entry.get("authority_receipt_path"),
                                       label + ":receipt")
        rcap = Capture(receipt_path,
                       (entry.get("authority_receipt_size"),
                        entry.get("authority_receipt_sha256")),
                       label + ":receipt")
        captures[label + ":receipt"] = rcap
        spec = ledger_spec(entry.get("normalized_candidate_ledger"),
                           label + ":normalized",
                           NORMALIZED_AUTHORITY_ROW_SCHEMA,
                           "atomic_candidate_key")
        need(spec["ordering"] == ["authority_candidate_ordinal"],
             label + ":normalized-order")
        authority_specs.append((ordinal, TERMINALS[ordinal], slot, spec))

    atomic_spec = ledger_spec(rebuild.get("atomic_ownership_ledger"),
                              "atomic", ATOMIC_ROW_SCHEMA,
                              "atomic_candidate_key")
    proof_spec = ledger_spec(rebuild.get("materialized_proof_row_join_ledger"),
                             "proof", PROOF_ROW_SCHEMA, "proof_row_key")
    edge_spec = ledger_spec(rebuild.get("full_component_edge_union_ledger"),
                            "edge", EDGE_ROW_SCHEMA, "component_edge_key")
    need(atomic_spec["ordering"] == ["atomic_candidate_key"], "atomic:ordering")
    need(proof_spec["ordering"] == ["atomic_candidate_key", "proof_row_key"],
         "proof:ordering")
    need(edge_spec["ordering"] == ["ordered_C15_component_pair"],
         "edge:ordering")

    for name, spec in (("atomic", atomic_spec), ("proof", proof_spec),
                       ("edge", edge_spec)):
        cap = Capture(under_workspace(spec["path"], name),
                      (spec["size"], spec["sha256"]), name)
        captures[name] = cap

    scratch_parent.mkdir(parents=True, exist_ok=True)
    fd, scratch_name = tempfile.mkstemp(prefix="c27r2-v5-preflight-", suffix=".sqlite3",
                                        dir=scratch_parent)
    os.close(fd)
    scratch = Path(scratch_name)
    try:
        db = sqlite3.connect(scratch)
        db.execute("PRAGMA journal_mode=OFF")
        db.execute("PRAGMA synchronous=OFF")
        db.execute("CREATE TABLE atomic(k TEXT PRIMARY KEY,t TEXT,slot TEXT,src TEXT,pc INTEGER,ps TEXT,ec INTEGER,d TEXT)")
        db.execute("CREATE TABLE candidate(k TEXT PRIMARY KEY,t TEXT,slot TEXT,src TEXT)")

        last_atomic = None
        atomic_sequence = hashlib.sha256()
        atomic_rows = 0
        for ordinal, row in enumerate(captures["atomic"].rows()):
            need(row.get("schema") == ATOMIC_ROW_SCHEMA
                 and row.get("ordinal") == ordinal, f"atomic:wire:{ordinal}")
            key = row.get("atomic_candidate_key")
            need(type(key) is str and (last_atomic is None or last_atomic < key),
                 f"atomic:strict-order:{ordinal}")
            last_atomic = key
            terminal = row.get("terminal")
            ti = row.get("terminal_ordinal")
            need(type(ti) is int and 0 <= ti < 20 and terminal == TERMINALS[ti],
                 f"atomic:terminal:{ordinal}")
            slot = row.get("authority_slot")
            src = row.get("primitive_authority_row_sha256")
            pc = row.get("proof_row_count")
            ps = row.get("proof_row_sequence_sha256")
            ec = row.get("component_edge_key_count")
            disp = row.get("disposition")
            need(type(slot) is str and slot and type(src) is str and len(src) == 64,
                 f"atomic:authority:{ordinal}")
            need(type(pc) is int and pc >= 0 and type(ec) is int and ec >= 0,
                 f"atomic:counts:{ordinal}")
            need(type(ps) is str and len(ps) == 64, f"atomic:sequence:{ordinal}")
            need(disp in {"NO_CROSS_COMPONENT_EDGE", "CROSS_COMPONENT_EDGE_PROVED"},
                 f"atomic:disposition:{ordinal}")
            need((pc == 0 and ec == 0 and disp == "NO_CROSS_COMPONENT_EDGE") or
                 (pc > 0 and ec > 0 and disp == "CROSS_COMPONENT_EDGE_PROVED"),
                 f"atomic:disposition-count-bind:{ordinal}")
            need(row.get("formal_credit") == 0, f"atomic:credit:{ordinal}")
            try:
                db.execute("INSERT INTO atomic VALUES(?,?,?,?,?,?,?,?)",
                           (key, terminal, slot, src, pc, ps, ec, disp))
            except sqlite3.IntegrityError as error:
                raise Failure(f"atomic:duplicate:{ordinal}") from error
            atomic_sequence.update(row["row_sha256"].encode("ascii") + b"\n")
            atomic_rows += 1
        need(atomic_rows == atomic_spec["row_count"], "atomic:row-count")
        need(atomic_sequence.hexdigest() == atomic_spec["row_sequence_sha256"],
             "atomic:row-sequence")
        db.commit()

        candidate_rows = 0
        terminal_candidate_census: dict[str, int] = {}
        for terminal_ordinal, terminal, slot, spec in authority_specs:
            cap = Capture(under_workspace(spec["path"], "normalized"),
                          (spec["size"], spec["sha256"]),
                          f"normalized:{terminal_ordinal}")
            captures[f"normalized:{terminal_ordinal}"] = cap
            seq = hashlib.sha256()
            count = 0
            for ordinal, row in enumerate(cap.rows()):
                need(row.get("schema") == NORMALIZED_AUTHORITY_ROW_SCHEMA
                     and row.get("authority_candidate_ordinal") == ordinal,
                     f"normalized:{terminal_ordinal}:wire:{ordinal}")
                need(row.get("terminal") == terminal
                     and row.get("authority_slot") == slot,
                     f"normalized:{terminal_ordinal}:authority:{ordinal}")
                key = row.get("atomic_candidate_key")
                src = row.get("primitive_authority_row_sha256")
                need(type(key) is str and type(src) is str and len(src) == 64,
                     f"normalized:{terminal_ordinal}:keys:{ordinal}")
                need(row.get("formal_credit") == 0,
                     f"normalized:{terminal_ordinal}:credit:{ordinal}")
                try:
                    db.execute("INSERT INTO candidate VALUES(?,?,?,?)",
                               (key, terminal, slot, src))
                except sqlite3.IntegrityError as error:
                    raise Failure(f"normalized:global-duplicate:{key}") from error
                seq.update(row["row_sha256"].encode("ascii") + b"\n")
                count += 1
            need(count == spec["row_count"], f"normalized:{terminal_ordinal}:count")
            need(seq.hexdigest() == spec["row_sequence_sha256"],
                 f"normalized:{terminal_ordinal}:sequence")
            terminal_candidate_census[terminal] = count
            candidate_rows += count
            db.commit()
        need(candidate_rows == atomic_rows, "candidate-vs-atomic-count")
        need(db.execute("SELECT COUNT(*) FROM candidate c LEFT JOIN atomic a ON a.k=c.k WHERE a.k IS NULL OR (a.t,a.slot,a.src)!=(c.t,c.slot,c.src)").fetchone()[0] == 0,
             "candidate-to-atomic-exact-join")
        need(db.execute("SELECT COUNT(*) FROM atomic a LEFT JOIN candidate c ON c.k=a.k WHERE c.k IS NULL").fetchone()[0] == 0,
             "atomic-to-candidate-exact-join")

        proof_by_atom: dict[str, list[str]] = defaultdict(list)
        edges_by_atom: dict[str, set[str]] = defaultdict(set)
        proof_by_edge: dict[str, list[str]] = defaultdict(list)
        terminal_by_edge: dict[str, Counter[str]] = defaultdict(Counter)
        slot_by_edge: dict[str, Counter[str]] = defaultdict(Counter)
        pair_by_edge: dict[str, tuple[str, str]] = {}
        proof_sequence = hashlib.sha256()
        proof_rows = 0
        last_proof_sort = None
        seen_proof_keys: set[str] = set()
        for ordinal, row in enumerate(captures["proof"].rows()):
            need(row.get("schema") == PROOF_ROW_SCHEMA
                 and row.get("ordinal") == ordinal, f"proof:wire:{ordinal}")
            atomic_key = row.get("atomic_candidate_key")
            proof_key = row.get("proof_row_key")
            sort_key = (atomic_key, proof_key)
            need(type(atomic_key) is str and type(proof_key) is str
                 and (last_proof_sort is None or last_proof_sort < sort_key),
                 f"proof:strict-order:{ordinal}")
            last_proof_sort = sort_key
            need(proof_key not in seen_proof_keys, f"proof:unique:{ordinal}")
            seen_proof_keys.add(proof_key)
            found = db.execute("SELECT t,slot,src FROM atomic WHERE k=?",
                               (atomic_key,)).fetchone()
            need(found is not None, f"proof:known-atomic:{ordinal}")
            terminal, slot, src = found
            need((row.get("terminal"), row.get("authority_slot"),
                  row.get("primitive_authority_row_sha256")) == (terminal, slot, src),
                 f"proof:atomic-bind:{ordinal}")
            members = row.get("ordered_C15_member_pair")
            need(type(members) is list and len(members) == 2
                 and members == sorted(members) and members[0] != members[1],
                 f"proof:member-pair:{ordinal}")
            need(members[0] in member_to_component and members[1] in member_to_component,
                 f"proof:C15-members:{ordinal}")
            pair = tuple(sorted((member_to_component[members[0]],
                                 member_to_component[members[1]])))
            need(pair[0] != pair[1], f"proof:cross-component:{ordinal}")
            need(row.get("ordered_C15_component_pair") == list(pair),
                 f"proof:component-map:{ordinal}")
            edge_key = EDGE_PREFIX + digest(list(pair))
            need(row.get("component_edge_key") == edge_key,
                 f"proof:edge-key:{ordinal}")
            need(type(row.get("physical_witness_key")) is str
                 and row["physical_witness_key"], f"proof:witness:{ordinal}")
            need(row.get("formal_credit") == 0, f"proof:credit:{ordinal}")
            pair_by_edge.setdefault(edge_key, pair)
            need(pair_by_edge[edge_key] == pair, f"proof:edge-collision:{ordinal}")
            proof_by_atom[atomic_key].append(proof_key)
            edges_by_atom[atomic_key].add(edge_key)
            proof_by_edge[edge_key].append(proof_key)
            terminal_by_edge[edge_key][terminal] += 1
            slot_by_edge[edge_key][slot] += 1
            proof_sequence.update(row["row_sha256"].encode("ascii") + b"\n")
            proof_rows += 1
        need(proof_rows == proof_spec["row_count"], "proof:row-count")
        need(proof_sequence.hexdigest() == proof_spec["row_sequence_sha256"],
             "proof:row-sequence")

        incident_expected = db.execute("SELECT COUNT(*) FROM atomic WHERE pc>0").fetchone()[0]
        need(incident_expected == len(proof_by_atom), "proof:incident-atom-cover")
        for atomic_key, proof_keys in proof_by_atom.items():
            pc, ps, ec = db.execute("SELECT pc,ps,ec FROM atomic WHERE k=?",
                                    (atomic_key,)).fetchone()
            need(pc == len(proof_keys) and ps == sequence_digest(proof_keys)
                 and ec == len(edges_by_atom[atomic_key]),
                 "proof:atomic-exact-aggregation:" + atomic_key)

        edge_sequence = hashlib.sha256()
        edge_rows = 0
        last_pair = None
        seen_edge_keys: set[str] = set()
        dsu = DSU(components)
        rank = 0
        for ordinal, row in enumerate(captures["edge"].rows()):
            need(row.get("schema") == EDGE_ROW_SCHEMA
                 and row.get("ordinal") == ordinal, f"edge:wire:{ordinal}")
            pair_value = row.get("ordered_C15_component_pair")
            need(type(pair_value) is list and len(pair_value) == 2
                 and pair_value == sorted(pair_value) and pair_value[0] != pair_value[1],
                 f"edge:pair:{ordinal}")
            pair = tuple(pair_value)
            need(last_pair is None or last_pair < pair, f"edge:strict-order:{ordinal}")
            last_pair = pair
            edge_key = EDGE_PREFIX + digest(list(pair))
            need(row.get("component_edge_key") == edge_key
                 and edge_key not in seen_edge_keys,
                 f"edge:key:{ordinal}")
            seen_edge_keys.add(edge_key)
            need(edge_key in pair_by_edge and pair_by_edge[edge_key] == pair,
                 f"edge:derived-from-proof:{ordinal}")
            proof_keys = sorted(proof_by_edge[edge_key])
            need(row.get("proof_row_count") == len(proof_keys)
                 and row.get("proof_row_sequence_sha256") == sequence_digest(proof_keys),
                 f"edge:proof-aggregation:{ordinal}")
            need(row.get("terminal_census") == dict(sorted(terminal_by_edge[edge_key].items()))
                 and row.get("authority_slot_census") == dict(sorted(slot_by_edge[edge_key].items())),
                 f"edge:census:{ordinal}")
            need(row.get("formal_credit") == 0, f"edge:credit:{ordinal}")
            rank += dsu.union(*pair)
            edge_sequence.update(row["row_sha256"].encode("ascii") + b"\n")
            edge_rows += 1
        need(seen_edge_keys == set(pair_by_edge), "edge:exact-proof-derived-union")
        need(edge_rows == edge_spec["row_count"], "edge:row-count")
        need(edge_sequence.hexdigest() == edge_spec["row_sequence_sha256"],
             "edge:row-sequence")

        census = rebuild.get("census")
        expected_census = {
            "frozen_C15_members": 502_204,
            "initial_frozen_C15_components": 57_876,
            "terminal_count": 20,
            "open_terminal_count": 0,
            "unresolved": 0,
            "global_atomic_candidate_count": atomic_rows,
            "materialized_proof_row_count": proof_rows,
            "full_component_edge_count": edge_rows,
            "fresh_DSU_rank": rank,
            "fresh_component_count": 57_876 - rank,
        }
        need(census == expected_census, "actual:exact-derived-census")
        closures = rebuild.get("closures")
        need(closures == {
            "twenty_normalized_authority_union_equals_atomic_ownership": True,
            "each_atomic_candidate_has_exactly_one_terminal_owner": True,
            "all_proof_rows_join_atomic_owner_and_primitive_authority": True,
            "proof_member_pairs_map_through_frozen_C15": True,
            "proof_derived_edge_union_equals_full_component_edge_ledger": True,
            "fresh_DSU_rebuilt_from_proof_derived_edges": True,
        }, "actual:closures")
        db.close()
        summary = {
            "terminal_candidate_census": terminal_candidate_census,
            "global_atomic_candidate_count": atomic_rows,
            "materialized_proof_row_count": proof_rows,
            "full_component_edge_count": edge_rows,
            "fresh_DSU_rank": rank,
            "fresh_component_count": 57_876 - rank,
        }
        return receipt, captures, summary
    finally:
        try:
            scratch.unlink()
        except FileNotFoundError:
            pass


def write_exclusive(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def build(output: Path) -> tuple[dict[str, Any], bool]:
    captures: dict[str, Capture] = {}
    try:
        c15_cap = Capture(C15, (C15_SIZE, C15_SHA256), "C15")
        captures["C15"] = c15_cap
        member_to_component, components = parse_c15(c15_cap)

        missing = []
        invalid = []
        actual_attestations: dict[str, Any] = {}
        derived_summary = None
        if not ACTUAL_GATE_RECEIPT.exists():
            missing.append("ACTUAL_V5_TWENTY_FAMILY_TERMINAL_RECEIPT")
        else:
            try:
                receipt_cap = Capture(ACTUAL_GATE_RECEIPT, None, "actual-receipt")
                captures["actual-receipt"] = receipt_cap
                _, local, derived_summary = validate_actual_gate(
                    receipt_cap, member_to_component, components, output.parent
                )
                captures.update({"actual:" + key: cap for key, cap in local.items()})
                actual_attestations = {
                    key: cap.attestation() for key, cap in sorted(local.items())
                }
                actual_attestations["receipt"] = receipt_cap.attestation()
            except (Failure, KeyError, TypeError, ValueError, OSError,
                    sqlite3.DatabaseError) as error:
                invalid.append("ACTUAL_V5_TWENTY_FAMILY_TERMINAL_RECEIPT:" + str(error))

        complete = not missing and not invalid and derived_summary is not None
        body = {
            "schema": "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-preflight.v1",
            "status": (
                "PASS_COMPLETE_ACTUAL_V5_INPUT_FOR_SEPARATE_FRESH_C27R2_PRODUCER__"
                "NO_C27_AUTHORIZATION__ZERO_CREDIT"
                if complete else
                "REJECT_MISSING_OR_INVALID_ACTUAL_V5_TWENTY_FAMILY_AUTHORITY__"
                "NO_C27_AUTHORIZATION__ZERO_CREDIT"
            ),
            "decision": "PASS_INPUT_PREFLIGHT_ONLY" if complete else "REJECT",
            "intended_process_exit_code": 0 if complete else 2,
            "missing_required_authority": missing,
            "invalid_required_authority": invalid,
            "input_interface": interface_contract(),
            "observed_frozen_C15": {
                "members": len(member_to_component),
                "components": len(components),
                "capture": c15_cap.attestation(),
            },
            "derived_actual_gate_summary_if_valid": derived_summary,
            "fresh_rebuild_algorithm": [
                "UNION_TWENTY_NORMALIZED_PRIMITIVE_AUTHORITY_LEDGERS_BY_UNIQUE_ATOMIC_CANDIDATE_KEY",
                "EXACT_JOIN_ATOMIC_OWNERSHIP_TO_THAT_PRIMITIVE_UNION",
                "JOIN_EVERY_MATERIALIZED_PROOF_ROW_TO_ATOMIC_OWNER_AND_PRIMITIVE_AUTHORITY_ROW_SHA256",
                "MAP_PROOF_MEMBER_PAIRS_THROUGH_FROZEN_C15_MEMBER_TO_COMPONENT_MAP",
                "DERIVE_FULL_COMPONENT_EDGE_UNION_FROM_MAPPED_CROSS_COMPONENT_PROOFS",
                "COMPARE_DERIVED_EDGE_UNION_EXACTLY_TO_ACTUAL_GATE_EDGE_LEDGER",
                "REBUILD_NEW_DSU_FROM_DERIVED_EDGES_ON_ALL_57876_FROZEN_COMPONENTS",
                "MATERIALIZE_SEPARATE_FRESH_C27R2_ATOMIC_OWNERSHIP_AND_PROOF_ROW_OUTPUTS",
                "RUN_INDEPENDENT_NO_IMPORT_VERIFIER_ATTACKS_COLD_MANIFEST_OUTER_TERMINAL_CHAIN_BEFORE_ANY_C27_AUTHORIZATION",
            ],
            "edge_universe_governance": {
                "edge_candidate_source": (
                    "MATERIALIZED_PRIMITIVE_PROOF_MEMBER_PAIRS_MAPPED_THROUGH_FROZEN_C15"
                ),
                "actual_gate_edge_ledger_role": "EXACT_AFTER_THE_FACT_COMPARATOR_ONLY",
                "strict_volume_14772_role": "SCOPED_DIAGNOSTIC_SUBSET_ONLY",
                "three_terminal_14724_role": "SCOPED_DIAGNOSTIC_SUBSET_ONLY",
                "strict_or_scoped_edge_ledger_used_as_candidate_universe": False,
            },
            "forbidden_dependencies": list(FORBIDDEN_DEPENDENCIES),
            "forbidden_dependency_open_count": 0,
            "root_input_capture": {
                "all_opened_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "actual_authorities_if_present": actual_attestations,
            },
            "fresh_C27R2_producer_may_start": complete,
            "C27_transition_totality": "UNAUTHORIZED",
            "C28_pair_routing": "UNAUTHORIZED",
            "C29_physical_maximality": "UNAUTHORIZED",
            "C29_patch_or_preservation_permitted": False,
            "formal_credit": 0,
            "manifest_authorized": False,
            "Source_W_transition_authorized": False,
            "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        result = dict(body)
        result["preflight_sha256"] = digest(body)
        write_exclusive(output, result)
        return result, complete
    finally:
        seen = set()
        for cap in captures.values():
            if id(cap) not in seen:
                seen.add(id(cap))
                cap.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result, complete = build(Path(args.output))
    except (Failure, KeyError, TypeError, ValueError, OSError,
            sqlite3.DatabaseError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "preflight_sha256": result["preflight_sha256"]}).decode("ascii"))
    return 0 if complete else 2


if __name__ == "__main__":
    raise SystemExit(main())
