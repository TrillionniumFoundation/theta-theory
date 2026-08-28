#!/usr/bin/env python3
"""Corrected-v2 T07/T08/T09 adapters from sealed primitive authorities.

This producer deliberately keeps four identities separate:

* 101,080 candidate-pair ownership rows (one terminal per pair),
* 206,632 ``(support atom, candidate pair)`` incidence rows,
* 483,232 exact atom incidence-set/complement disposition rows, and
* physical component-proof rows for cross-component candidate pairs.

It does not import a prior producer and never treats an incidence as a
candidate.  All inputs are held on one stable O_NOFOLLOW file description
from hash through parse through final fstat.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "candidate-ownership.row.v2"
)
INCIDENCE_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "atom-pair-incidence.row.v2"
)
DISPOSITION_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "atom-incidence-disposition.row.v2"
)
PROOF_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "materialized-physical-proof-join.row.v2"
)
EDGE_PREFIX = "round306c27r2-v5-component-edge:"
PAIR_PREFIX = "round306c27-v5-three-terminal-pair:"
INCIDENCE_PREFIX = "round306c27-v5-atom-pair-incidence:"
PROOF_PREFIX = "round306c27-v5-physical-proof:"
EMPTY_SEQUENCE_SHA256 = hashlib.sha256(b"").hexdigest()
TERMINALS = {
    "SIGNED_BOUNDARY_FACES": (7, "T07_SIGNED_BOUNDARY_FACES"),
    "COMPLETE_BOUNDARY_FACES": (8, "T08_COMPLETE_BOUNDARY_FACES"),
    "POSITIVE_VOLUME_CARRIERS": (9, "T09_POSITIVE_VOLUME_CARRIERS"),
}
EXPECTED_PAIR_CENSUS = {
    "SIGNED_BOUNDARY_FACES": 25_452,
    "COMPLETE_BOUNDARY_FACES": 10_688,
    "POSITIVE_VOLUME_CARRIERS": 64_940,
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
    need("row_sha256" not in body, "fresh row")
    return {**body, "row_sha256": digest(body)}


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid)


@dataclass
class Capture:
    label: str
    path: Path
    fd: int
    initial: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str) -> "Capture":
        resolved = path.resolve()
        fd = os.open(resolved, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                     | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            need(observed == expected, label + ":sha256")
            need(fingerprint(os.fstat(fd)) == fingerprint(before),
                 label + ":hash-fstat")
            return cls(label, resolved, fd, fingerprint(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def stable(self, phase: str) -> None:
        need(fingerprint(os.fstat(self.fd)) == self.initial,
             self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        self.stable("raw")
        return b"".join(chunks)

    def document(self, closure_key: str) -> dict[str, Any]:
        payload = self.raw()
        row = json.loads(payload)
        need(type(row) is dict and canonical(row) in {payload, payload.rstrip(b"\n")},
             self.label + ":canonical-document")
        body = dict(row)
        claim = body.pop(closure_key, None)
        need(type(claim) is str and claim == digest(body),
             self.label + ":document-closure")
        return row

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"),
                         f"{self.label}:{ordinal}:newline")
                    payload = line[:-1]
                    row = json.loads(payload)
                    need(type(row) is dict and canonical(row) == payload,
                         f"{self.label}:{ordinal}:canonical")
                    body = dict(row)
                    claim = body.pop("row_sha256", None)
                    need(type(claim) is str and claim == digest(body),
                         f"{self.label}:{ordinal}:closure")
                    yield row
        self.stable("rows")

    def attestation(self) -> dict[str, Any]:
        self.stable("attestation")
        try:
            rendered = str(self.path.relative_to(ROOT))
        except ValueError:
            rendered = str(self.path)
        return {
            "path": rendered, "size": self.initial[2], "sha256": self.sha256,
            "stat_fingerprint": list(self.initial), "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def close(self) -> None:
        os.close(self.fd)


class RowWriter:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.open("xb")
        self.stream = gzip.GzipFile(filename="", fileobj=self.raw,
                                    mode="wb", mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def write(self, row: dict[str, Any]) -> None:
        body = dict(row)
        claim = body.pop("row_sha256", None)
        need(type(claim) is str and claim == digest(body),
             self.path.name + ":row-closure")
        self.stream.write(canonical(row) + b"\n")
        self.sequence.update(claim.encode("ascii") + b"\n")
        self.count += 1

    def finish(self, row_schema: str, unique_key: Any,
               ordering: list[str]) -> dict[str, Any]:
        self.stream.close()
        self.raw.close()
        return {
            "path": str(self.path.relative_to(ROOT)),
            "size": self.path.stat().st_size,
            "sha256": file_sha(self.path),
            "row_count": self.count,
            "row_sequence_sha256": self.sequence.hexdigest(),
            "row_schema": row_schema,
            "unique_key": unique_key,
            "ordering": ordering,
        }


def ordered_pair(value: Any, label: str) -> tuple[str, str]:
    need(type(value) is list and len(value) == 2
         and all(type(item) is str for item in value)
         and value[0] != value[1], label + ":pair")
    return tuple(sorted(value))


def pair_candidate_key(pair: tuple[str, str]) -> str:
    return PAIR_PREFIX + digest(list(pair))


def sequence_sha(row_shas: list[str]) -> str:
    state = hashlib.sha256()
    for value in row_shas:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def validate_interface(row: dict[str, Any]) -> None:
    need(row["decision"] == "REJECT" and row["formal_credit"] == 0,
         "corrected interface truthful reject")
    interface = row["corrected_interface"]
    need(interface["candidate_ownership_ledger"]["row_schema"]
         == CANDIDATE_SCHEMA, "candidate schema interface")
    need(interface["atom_pair_incidence_ledger"]["row_schema"]
         == INCIDENCE_SCHEMA, "incidence schema interface")
    need(interface["atom_incidence_disposition_ledger"]["row_schema"]
         == DISPOSITION_SCHEMA, "disposition schema interface")
    need(interface["materialized_physical_proof_join_ledger"]["row_schema"]
         == PROOF_SCHEMA, "proof schema interface")
    rule = interface["candidate_ownership_ledger"]["T07_T08_T09_rule"]
    need(rule["candidate_count"] == 101_080
         and rule["terminal_census"] == EXPECTED_PAIR_CENSUS
         and rule["candidate_key_equals_candidate_pair_key"] is True,
         "candidate interface census")
    atom = interface["atom_pair_incidence_ledger"][
        "T07_T08_T09_exact_census"]
    need(atom == {
        "incidence_count": 206_632,
        "candidate_pair_count": 101_080,
        "primitive_atom_denominator": 483_232,
        "incident_atoms": 62_768,
        "exact_complement_atoms": 420_464,
        "multi_terminal_atoms": 3_896,
    }, "atom interface census")


def build(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_dir).resolve()
    need(not output.exists(), "fresh output")
    specs = {
        "interface_v2": (args.interface_v2, args.interface_v2_sha256),
        "C15": (args.c15, args.c15_sha256),
        "pair_ownership": (args.pair_ownership, args.pair_ownership_sha256),
        "full_atom_ledger": (args.full_atom_ledger,
                             args.full_atom_ledger_sha256),
        "pair_union_receipt": (args.pair_union_receipt,
                               args.pair_union_receipt_sha256),
        "full_atom_receipt": (args.full_atom_receipt,
                              args.full_atom_receipt_sha256),
        "full_atom_cold_receipt": (args.full_atom_cold_receipt,
                                   args.full_atom_cold_receipt_sha256),
    }
    captures: dict[str, Capture] = {}
    open_writers: list[RowWriter] = []
    try:
        for label, (path, sha) in specs.items():
            captures[label] = Capture.open(label, Path(path), sha)
        interface = captures["interface_v2"].document("preflight_sha256")
        validate_interface(interface)
        union = captures["pair_union_receipt"].document("result_sha256")
        atom_receipt = captures["full_atom_receipt"].document("receipt_sha256")
        cold = captures["full_atom_cold_receipt"].document("receipt_sha256")
        need(union["authority_scope"]["candidate_pair_count"] == 101_080
             and union["authority_scope"][
                 "each_candidate_pair_exactly_one_terminal"] is True
             and union["formal_credit"] == 0, "pair union authority")
        exact = atom_receipt["exact_atom_contract"]
        need(atom_receipt["schema"] == (
            "cm2.c27-independent.full-union-101080-on-483232."
            "atom-terminal-zero-credit.v3")
             and atom_receipt["dual_seed"]["ledgers_byte_identical"] is True
             and atom_receipt["dual_seed"]["ledger_sha256"]
                == captures["full_atom_ledger"].sha256
             and exact["atoms"] == 483_232
             and exact["expanded_atom_route_incidences"] == 206_632
             and exact["exact_complement_atoms"] == 420_464
             and atom_receipt["formal_credit"] == 0, "full atom authority")
        need(cold["base_receipt_file_sha256"]
                == captures["full_atom_receipt"].sha256
             and cold["pre_post_sha256_identical"] is True
             and cold["pre_post_stat_identical"] is True
             and cold["numeric_exit"] == 0 and cold["formal_credit"] == 0,
             "full atom cold replay")

        member_component: dict[str, str] = {}
        components: set[str] = set()
        for ordinal, row in enumerate(captures["C15"].rows()):
            need(row["member_ordinal"] == ordinal, "C15 ordinal")
            member = row["registry_member_id"]
            need(member not in member_component, "C15 unique member")
            member_component[member] = row["fresh_component_id"]
            components.add(row["fresh_component_id"])
        need(len(member_component) == 502_204 and len(components) == 57_876,
             "C15 census")

        # Candidate ownership and physical proof rows are determined solely by
        # the 101,080 sealed pair rows plus the frozen C15 map.  They are built
        # before atom incidence rows so every incidence can bind the exact
        # candidate-owner output row hash.
        records: list[dict[str, Any]] = []
        seen_pairs: set[tuple[str, str]] = set()
        candidate_keys: set[str] = set()
        pair_census = Counter()
        cross_census = Counter()
        edge_sets: dict[str, set[str]] = {name: set() for name in TERMINALS}
        for source_ordinal, row in enumerate(captures["pair_ownership"].rows()):
            pair = ordered_pair(row["pair_key"], f"pair:{source_ordinal}")
            need(pair not in seen_pairs, "unique pair")
            seen_pairs.add(pair)
            terminal = row["assigned_terminal"]
            need(terminal in TERMINALS and row["formal_credit"] == 0,
                 "pair terminal")
            need(pair[0] in member_component and pair[1] in member_component,
                 "pair members in frozen C15")
            key = pair_candidate_key(pair)
            need(key not in candidate_keys, "candidate-key collision")
            candidate_keys.add(key)
            ti, slot = TERMINALS[terminal]
            component_pair = tuple(sorted((member_component[pair[0]],
                                           member_component[pair[1]])))
            cross = component_pair[0] != component_pair[1]
            proof = None
            if cross:
                witness_key = "three-terminal-formal-pair-witness:" + digest([
                    key, list(pair), row["source_row_sha256"],
                    row.get("C24A_G2B_exact_row_sha256"),
                ])
                edge_key = EDGE_PREFIX + digest(list(component_pair))
                proof_key = PROOF_PREFIX + digest([
                    key, witness_key, list(pair), list(component_pair)])
                proof = close({
                    "schema": PROOF_SCHEMA,
                    "ordinal": -1,
                    "proof_row_key": proof_key,
                    "candidate_key": key,
                    "atom_pair_incidence_key_or_null": None,
                    "terminal": terminal,
                    "authority_slot": slot,
                    "primitive_authority_row_sha256": row["row_sha256"],
                    "ordered_C15_member_pair": list(pair),
                    "ordered_C15_component_pair": list(component_pair),
                    "component_edge_key": edge_key,
                    "physical_witness_key": witness_key,
                    "formal_credit": 0,
                })
                cross_census[terminal] += 1
                edge_sets[terminal].add(edge_key)
            records.append({
                "key": key, "pair": pair, "terminal": terminal,
                "terminal_ordinal": ti, "slot": slot,
                "source_row_sha256": row["row_sha256"],
                "component_pair": component_pair, "proof": proof,
            })
            pair_census[terminal] += 1
        need(len(records) == 101_080 and dict(pair_census) == EXPECTED_PAIR_CENSUS,
             "pair candidate census")
        records.sort(key=lambda item: item["key"])

        output.mkdir(parents=True)
        candidate_writers: dict[str, RowWriter] = {}
        proof_writers: dict[str, RowWriter] = {}
        for terminal, (ti, _) in TERMINALS.items():
            candidate_writers[terminal] = RowWriter(
                output / f"T{ti:02d}_{terminal}_candidate_ownership.jsonl.gz")
            proof_writers[terminal] = RowWriter(
                output / f"T{ti:02d}_{terminal}_physical_proof_fragment.jsonl.gz")
            open_writers.extend((candidate_writers[terminal],
                                 proof_writers[terminal]))
        local_candidate_ordinals = Counter()
        local_proof_ordinals = Counter()
        candidate_by_pair: dict[tuple[str, str], dict[str, Any]] = {}
        proof_keys: set[str] = set()
        for record in records:
            terminal = record["terminal"]
            proof = record["proof"]
            proof_sequence = EMPTY_SEQUENCE_SHA256
            if proof is not None:
                proof_body = dict(proof)
                proof_body.pop("row_sha256")
                proof_body["ordinal"] = local_proof_ordinals[terminal]
                proof = close(proof_body)
                need(proof["proof_row_key"] not in proof_keys,
                     "unique proof key")
                proof_keys.add(proof["proof_row_key"])
                proof_writers[terminal].write(proof)
                local_proof_ordinals[terminal] += 1
                proof_sequence = sequence_sha([proof["row_sha256"]])
            candidate = close({
                "schema": CANDIDATE_SCHEMA,
                "ordinal": local_candidate_ordinals[terminal],
                "candidate_key": record["key"],
                "candidate_kind": "THREE_TERMINAL_CANDIDATE_PAIR",
                "candidate_pair_key_or_null": record["key"],
                "terminal_ordinal": record["terminal_ordinal"],
                "terminal": terminal,
                "authority_slot": record["slot"],
                "primitive_authority_row_sha256":
                    record["source_row_sha256"],
                "component_relation_disposition": (
                    "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED"
                    if proof is not None else
                    "SAME_FROZEN_C15_COMPONENT__NO_EDGE"),
                "physical_proof_row_count": int(proof is not None),
                "physical_proof_row_sequence_sha256": proof_sequence,
                "formal_credit": 0,
            })
            candidate_writers[terminal].write(candidate)
            candidate_by_pair[record["pair"]] = candidate
            local_candidate_ordinals[terminal] += 1

        incidence_writer = RowWriter(
            output / "T07_T09_atom_pair_incidence.jsonl.gz")
        disposition_writer = RowWriter(
            output / "T07_T09_atom_incidence_disposition.jsonl.gz")
        open_writers.extend((incidence_writer, disposition_writer))
        seen_incidences: set[tuple[str, str]] = set()
        observed_pairs: set[tuple[str, str]] = set()
        previous_atom: str | None = None
        incident_atoms = complement_atoms = multi_terminal_atoms = 0
        atom_count = 0
        incidence_terminal_census = Counter()
        for atom_ordinal, atom_row in enumerate(captures["full_atom_ledger"].rows()):
            atom_count += 1
            atom_key = atom_row["atom_id"]
            need(previous_atom is None or previous_atom < atom_key,
                 "atom ledger strict ordering")
            previous_atom = atom_key
            routes = atom_row["incident_union_pair_routes"]
            need(atom_row["candidate_incidence_count"] == len(routes),
                 "atom incidence count")
            route_records = []
            for route in routes:
                pieces = route["pair_key"].split("|")
                pair = tuple(sorted(pieces))
                need(len(pieces) == 2 and pair in candidate_by_pair,
                     "route candidate pair")
                candidate = candidate_by_pair[pair]
                need(route["assigned_terminal"] == candidate["terminal"],
                     "route inherits candidate terminal")
                candidate_key = candidate["candidate_key"]
                incidence_tuple = (atom_key, candidate_key)
                need(incidence_tuple not in seen_incidences,
                     "duplicate atom-pair incidence")
                seen_incidences.add(incidence_tuple)
                observed_pairs.add(pair)
                route_records.append((candidate_key, candidate, route))
            route_records.sort(key=lambda item: item[0])
            per_atom_shas: list[str] = []
            terminal_set: set[str] = set()
            for candidate_key, candidate, route in route_records:
                incidence_key = INCIDENCE_PREFIX + digest([
                    atom_key, candidate_key])
                incidence = close({
                    "schema": INCIDENCE_SCHEMA,
                    "ordinal": incidence_writer.count,
                    "incidence_key": incidence_key,
                    "primitive_support_atom_key": atom_key,
                    "candidate_pair_key": candidate_key,
                    "candidate_terminal": candidate["terminal"],
                    "candidate_owner_row_sha256": candidate["row_sha256"],
                    "formal_credit": 0,
                })
                incidence_writer.write(incidence)
                per_atom_shas.append(incidence["row_sha256"])
                terminal_set.add(candidate["terminal"])
                incidence_terminal_census[candidate["terminal"]] += 1
            is_incident = bool(route_records)
            incident_atoms += int(is_incident)
            complement_atoms += int(not is_incident)
            multi_terminal_atoms += int(len(terminal_set) > 1)
            disposition = close({
                "schema": DISPOSITION_SCHEMA,
                "ordinal": atom_ordinal,
                "primitive_support_atom_key": atom_key,
                "incidence_count": len(route_records),
                "incidence_row_sequence_sha256": sequence_sha(per_atom_shas),
                "terminal_set": sorted(terminal_set),
                "disposition": (
                    "EXACT_NONEMPTY_ATOM_PAIR_INCIDENCE_SET" if is_incident
                    else "EXACT_EMPTY_INCIDENCE_COMPLEMENT"),
                "formal_credit": 0,
            })
            disposition_writer.write(disposition)
        need(atom_count == 483_232 and len(seen_incidences) == 206_632
             and incident_atoms == 62_768 and complement_atoms == 420_464
             and multi_terminal_atoms == 3_896,
             "exact atom incidence/disposition census")
        need(observed_pairs == seen_pairs, "every candidate pair incident")

        terminal_entries = []
        for terminal, (ti, slot) in sorted(TERMINALS.items(),
                                           key=lambda item: item[1][0]):
            candidate_desc = candidate_writers[terminal].finish(
                CANDIDATE_SCHEMA, "candidate_key", ["candidate_key"])
            proof_desc = proof_writers[terminal].finish(
                PROOF_SCHEMA, "proof_row_key", ["candidate_key"])
            need(candidate_desc["row_count"] == pair_census[terminal]
                 and proof_desc["row_count"] == cross_census[terminal],
                 terminal + ":output census")
            terminal_entries.append({
                "terminal_ordinal": ti, "terminal": terminal,
                "authority_slot": slot,
                "candidate_ownership_ledger": candidate_desc,
                "materialized_physical_proof_fragment_ledger": proof_desc,
                "candidate_count": pair_census[terminal],
                "cross_component_candidate_count": cross_census[terminal],
                "unique_component_edge_count": len(edge_sets[terminal]),
            })
        incidence_desc = incidence_writer.finish(
            INCIDENCE_SCHEMA,
            ["primitive_support_atom_key", "candidate_pair_key"],
            ["primitive_support_atom_key", "candidate_pair_key"])
        disposition_desc = disposition_writer.finish(
            DISPOSITION_SCHEMA, "primitive_support_atom_key",
            ["primitive_support_atom_key"])
        open_writers.clear()

        source_path = Path(__file__).resolve()
        body = {
            "schema": (
                "cm2.c27-independent.primitive-v5-actual-three-terminal-"
                "pair-atom-adapters.v2"),
            "status": (
                "PASS_CORRECTED_V2_T07_T08_T09_PAIR_OWNERSHIP_ATOM_"
                "INCIDENCE_DISPOSITION_AND_PHYSICAL_PROOF__ZERO_CREDIT"),
            "interface_v2_object_sha256": interface["preflight_sha256"],
            "terminal_adapters": terminal_entries,
            "atom_pair_incidence_ledger": incidence_desc,
            "atom_incidence_disposition_ledger": disposition_desc,
            "exact_census": {
                "candidate_pair_count": len(records),
                "terminal_candidate_pair_census": dict(sorted(pair_census.items())),
                "cross_component_candidate_pair_census":
                    dict(sorted(cross_census.items())),
                "physical_proof_row_count": len(proof_keys),
                "full_atom_rows": atom_count,
                "atom_pair_incidence_count": len(seen_incidences),
                "atom_pair_incidence_terminal_census":
                    dict(sorted(incidence_terminal_census.items())),
                "incident_atoms": incident_atoms,
                "exact_complement_atoms": complement_atoms,
                "multi_terminal_atoms": multi_terminal_atoms,
                "unique_component_edges": len(set().union(*edge_sets.values())),
            },
            "separation_closures": {
                "candidate_pair_each_exactly_one_terminal": True,
                "candidate_ownership_count_is_101080_not_206632": True,
                "atom_pair_incidence_never_counted_as_candidate": True,
                "every_incidence_inherits_candidate_owner_terminal": True,
                "every_candidate_pair_has_at_least_one_incidence": True,
                "all_483232_atoms_have_exact_incidence_set_or_empty_complement": True,
                "multi_pair_and_multi_terminal_atoms_allowed": True,
                "every_cross_component_candidate_has_exactly_one_physical_proof": True,
                "same_component_candidate_has_no_component_edge_proof": True,
                "proof_member_pairs_mapped_through_frozen_C15": True,
            },
            "forbidden_input_governance": {
                "old_C27_FAMILIES_imported_or_read": False,
                "old_transition_ledger_imported_or_read": False,
                "C28_imported_or_read": False,
                "C29_imported_or_read": False,
                "historical_edge_ledger_used_as_candidate_universe": False,
                "strict_14772_used_as_candidate_universe": False,
                "scoped_14724_used_as_candidate_universe": False,
                "superseded_v1_adapter_consumed": False,
            },
            "formal_credit": 0,
            "manifest_authorized": False,
            "Source_W_transition_authorized": False,
            "strict_nonpromotion": {
                "C27_transition_totality": 0, "C28_pair_routing": 0,
                "C29_physical_maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
            "producer_source_sha256": file_sha(source_path),
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {label: capture.attestation()
                                 for label, capture in sorted(captures.items())},
            },
        }
        receipt = dict(body)
        receipt["receipt_sha256"] = digest(receipt)
        receipt_path = output / "adapter_receipt.json"
        receipt_path.write_bytes(canonical(receipt) + b"\n")
        manifest_rows = []
        for entry in terminal_entries:
            for key in ("candidate_ownership_ledger",
                        "materialized_physical_proof_fragment_ledger"):
                desc = entry[key]
                manifest_rows.append(f"{desc['sha256']}  {desc['path']}\n")
        for desc in (incidence_desc, disposition_desc):
            manifest_rows.append(f"{desc['sha256']}  {desc['path']}\n")
        for capture in captures.values():
            item = capture.attestation()
            manifest_rows.append(f"{item['sha256']}  {item['path']}\n")
        manifest_rows.extend((
            f"{file_sha(source_path)}  {source_path.relative_to(ROOT)}\n",
            f"{file_sha(receipt_path)}  {receipt_path.relative_to(ROOT)}\n",
        ))
        (output / "manifest.sha256").write_text(
            "".join(sorted(set(manifest_rows))), encoding="ascii")
        return receipt
    finally:
        for writer in open_writers:
            if not writer.raw.closed:
                writer.stream.close()
                writer.raw.close()
        for capture in captures.values():
            capture.close()


def add_input(parser: argparse.ArgumentParser, name: str) -> None:
    parser.add_argument("--" + name, required=True)
    parser.add_argument("--" + name + "-sha256", required=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in ("interface-v2", "c15", "pair-ownership",
                 "full-atom-ledger", "pair-union-receipt",
                 "full-atom-receipt", "full-atom-cold-receipt"):
        add_input(parser, name)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    try:
        receipt = build(args)
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(canonical({"status": receipt["status"],
                     "exact_census": receipt["exact_census"],
                     "receipt_sha256": receipt["receipt_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
