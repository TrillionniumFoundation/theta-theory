#!/usr/bin/env python3
"""Fresh T07/T08/T09 normalized adapters from sealed pair/atom authorities.

Every normalized candidate is one exact (primitive atom, uniquely-owned pair)
incidence from the formal 483,232-atom join.  Component proofs are emitted
only when the pair's two frozen C15 members lie in distinct components.
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
NORMALIZED_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "normalized-primitive-authority.row.v1"
)
PROOF_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "materialized-proof-row-join.row.v1"
)
SOURCE_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual."
    "three-terminal-atom-adapter-source.row.v1"
)
EDGE_PREFIX = "round306c27r2-v5-component-edge:"
ATOMIC_PREFIX = "round306c27-v5-atomic:"
PROOF_PREFIX = "round306c27-v5-proof:"
TERMINALS = {
    "SIGNED_BOUNDARY_FACES": (7, "T07_SIGNED_BOUNDARY_FACES"),
    "COMPLETE_BOUNDARY_FACES": (8, "T08_COMPLETE_BOUNDARY_FACES"),
    "POSITIVE_VOLUME_CARRIERS": (9, "T09_POSITIVE_VOLUME_CARRIERS"),
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


def fp(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid)


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


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
            need(fp(os.fstat(fd)) == fp(before), label + ":hash fstat")
            return cls(label, resolved, fd, fp(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def stable(self, phase: str) -> None:
        need(fp(os.fstat(self.fd)) == self.initial,
             self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        self.stable("raw")
        return b"".join(chunks)

    def document(self, closure_key: str) -> dict[str, Any]:
        value = json.loads(self.raw())
        need(type(value) is dict, self.label + ":document")
        body = dict(value)
        claim = body.pop(closure_key, None)
        need(type(claim) is str and claim == digest(body), self.label + ":closure")
        return value

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"), f"{self.label}:{ordinal}:newline")
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
        return {"path": rendered, "size": self.initial[2],
                "sha256": self.sha256, "stat_fingerprint": list(self.initial),
                "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True}

    def close(self) -> None:
        os.close(self.fd)


class RowWriter:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.open("xb")
        self.stream = gzip.GzipFile(filename="", fileobj=self.raw, mode="wb", mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def write(self, row: dict[str, Any]) -> None:
        body = dict(row)
        claim = body.pop("row_sha256", None)
        need(type(claim) is str and claim == digest(body), self.path.name + ":row")
        self.stream.write(canonical(row) + b"\n")
        self.sequence.update(claim.encode("ascii") + b"\n")
        self.count += 1

    def finish(self, row_schema: str, unique_key: str,
               ordering: list[str]) -> dict[str, Any]:
        self.stream.close()
        self.raw.close()
        return {"path": str(self.path.relative_to(ROOT)),
                "size": self.path.stat().st_size, "sha256": file_sha(self.path),
                "row_count": self.count,
                "row_sequence_sha256": self.sequence.hexdigest(),
                "row_schema": row_schema, "unique_key_field": unique_key,
                "ordering": ordering}


def ordered_pair(value: Any, label: str) -> tuple[str, str]:
    need(type(value) is list and len(value) == 2
         and all(type(item) is str for item in value) and value[0] != value[1],
         label + ":pair")
    return tuple(sorted(value))


def build(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_dir).resolve()
    need(not output.exists(), "fresh output")
    specs = {
        "C15": (args.c15, args.c15_sha256),
        "pair_ownership": (args.pair_ownership, args.pair_ownership_sha256),
        "full_atom_ledger": (args.full_atom_ledger, args.full_atom_ledger_sha256),
        "pair_union_receipt": (args.pair_union_receipt,
                               args.pair_union_receipt_sha256),
        "full_atom_receipt": (args.full_atom_receipt,
                              args.full_atom_receipt_sha256),
        "full_atom_cold_receipt": (args.full_atom_cold_receipt,
                                   args.full_atom_cold_receipt_sha256),
    }
    captures: dict[str, Capture] = {}
    writers: dict[str, dict[str, RowWriter]] = {}
    try:
        for label, (path, sha) in specs.items():
            captures[label] = Capture.open(label, Path(path), sha)
        union = captures["pair_union_receipt"].document("result_sha256")
        atom_receipt = captures["full_atom_receipt"].document("receipt_sha256")
        cold = captures["full_atom_cold_receipt"].document("receipt_sha256")
        need(union["authority_scope"]["candidate_pair_count"] == 101_080
             and union["authority_scope"]["each_candidate_pair_exactly_one_terminal"]
                is True and union["formal_credit"] == 0,
             "pair union authority")
        exact = atom_receipt["exact_atom_contract"]
        need(atom_receipt["schema"]
                == "cm2.c27-independent.full-union-101080-on-483232.atom-terminal-zero-credit.v3"
             and atom_receipt["dual_seed"]["ledgers_byte_identical"] is True
             and atom_receipt["dual_seed"]["ledger_sha256"]
                == captures["full_atom_ledger"].sha256
             and exact["atoms"] == 483_232
             and exact["expanded_atom_route_incidences"] == 206_632
             and exact["exact_complement_atoms"] == 420_464
             and atom_receipt["formal_credit"] == 0,
             "full atom authority")
        need(cold["base_receipt_file_sha256"] == captures["full_atom_receipt"].sha256
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
        pair_authority: dict[tuple[str, str], tuple[str, str]] = {}
        terminal_pair_census = Counter()
        for ordinal, row in enumerate(captures["pair_ownership"].rows()):
            pair = ordered_pair(row["pair_key"], f"pair:{ordinal}")
            need(pair not in pair_authority, "unique pair authority")
            terminal = row["assigned_terminal"]
            need(terminal in TERMINALS and row["formal_credit"] == 0,
                 "pair terminal")
            pair_authority[pair] = (terminal, row["row_sha256"])
            terminal_pair_census[terminal] += 1
        need(len(pair_authority) == 101_080
             and terminal_pair_census == {"SIGNED_BOUNDARY_FACES": 25_452,
                                          "COMPLETE_BOUNDARY_FACES": 10_688,
                                          "POSITIVE_VOLUME_CARRIERS": 64_940},
             "pair authority census")

        output.mkdir(parents=True)
        for terminal, (terminal_ordinal, _) in TERMINALS.items():
            prefix = f"T{terminal_ordinal:02d}_{terminal}"
            writers[terminal] = {
                "source": RowWriter(output / (prefix + "_adapter_source.jsonl.gz")),
                "normalized": RowWriter(output / (prefix + "_normalized_candidate.jsonl.gz")),
                "proof": RowWriter(output / (prefix + "_proof_fragment.jsonl.gz")),
            }
        candidate_ordinals = Counter()
        proof_ordinals = Counter()
        terminal_candidate_census = Counter()
        terminal_proof_census = Counter()
        terminal_edge_sets: dict[str, set[str]] = {name: set() for name in TERMINALS}
        observed_pairs: set[tuple[str, str]] = set()
        atom_rows = 0
        complement_atoms = 0
        seen_atomic: set[str] = set()
        for atom_row in captures["full_atom_ledger"].rows():
            atom_rows += 1
            routes = atom_row["incident_union_pair_routes"]
            need(atom_row["candidate_incidence_count"] == len(routes),
                 "atom incidence count")
            if not routes:
                complement_atoms += 1
            for route in routes:
                pieces = route["pair_key"].split("|")
                need(len(pieces) == 2, "route pair serialization")
                pair = tuple(sorted(pieces))
                need(pair in pair_authority, "route pair in authority")
                terminal, pair_row_sha = pair_authority[pair]
                need(route["assigned_terminal"] == terminal, "route terminal binding")
                need(pair[0] in member_component and pair[1] in member_component,
                     "route pair C15 members")
                observed_pairs.add(pair)
                ti, slot = TERMINALS[terminal]
                atomic_key = ATOMIC_PREFIX + digest([
                    slot, atom_row["atom_id"], list(pair)])
                need(atomic_key not in seen_atomic, "unique atom-pair candidate")
                seen_atomic.add(atomic_key)
                component_pair = tuple(sorted((member_component[pair[0]],
                                               member_component[pair[1]])))
                cross = component_pair[0] != component_pair[1]
                witness_key = ("full-atom-pair-incidence:" + digest([
                    atom_row["atom_id"], list(pair),
                    route["union_route_row_sha256"]])) if cross else None
                source_ordinal = candidate_ordinals[terminal]
                source_body = {
                    "schema": SOURCE_SCHEMA,
                    "authority_candidate_ordinal": source_ordinal,
                    "atomic_candidate_key": atomic_key,
                    "terminal_ordinal": ti, "terminal": terminal,
                    "authority_slot": slot,
                    "atom_id": atom_row["atom_id"],
                    "atom_authority_row_sha256": atom_row["row_sha256"],
                    "atom_source_row_sha256": atom_row["atom_source_row_sha256"],
                    "ordered_C15_member_pair": list(pair),
                    "ordered_C15_component_pair": list(component_pair),
                    "pair_authority_row_sha256": pair_row_sha,
                    "union_route_row_sha256": route["union_route_row_sha256"],
                    "incidence_binding_mode": route["atom_binding_mode"],
                    "disposition": ("CROSS_COMPONENT_EDGE_PROVED" if cross
                                    else "NO_CROSS_COMPONENT_EDGE"),
                    "physical_witness_key": witness_key,
                    "formal_credit": 0,
                }
                source_row = close(source_body)
                writers[terminal]["source"].write(source_row)
                normalized = close({
                    "schema": NORMALIZED_SCHEMA,
                    "authority_candidate_ordinal": source_ordinal,
                    "atomic_candidate_key": atomic_key,
                    "terminal": terminal, "authority_slot": slot,
                    "primitive_authority_row_sha256": source_row["row_sha256"],
                    "formal_credit": 0,
                })
                writers[terminal]["normalized"].write(normalized)
                if cross:
                    edge_key = EDGE_PREFIX + digest(list(component_pair))
                    proof_key = PROOF_PREFIX + digest([
                        atomic_key, witness_key, list(pair)])
                    proof = close({
                        "schema": PROOF_SCHEMA,
                        "ordinal": proof_ordinals[terminal],
                        "proof_row_key": proof_key,
                        "atomic_candidate_key": atomic_key,
                        "terminal": terminal, "authority_slot": slot,
                        "primitive_authority_row_sha256": source_row["row_sha256"],
                        "ordered_C15_member_pair": list(pair),
                        "ordered_C15_component_pair": list(component_pair),
                        "component_edge_key": edge_key,
                        "physical_witness_key": witness_key,
                        "formal_credit": 0,
                    })
                    writers[terminal]["proof"].write(proof)
                    proof_ordinals[terminal] += 1
                    terminal_proof_census[terminal] += 1
                    terminal_edge_sets[terminal].add(edge_key)
                candidate_ordinals[terminal] += 1
                terminal_candidate_census[terminal] += 1
        need(atom_rows == 483_232 and complement_atoms == 420_464,
             "full atom row census")
        need(len(seen_atomic) == 206_632 and observed_pairs == set(pair_authority),
             "exact pair/atom incidence coverage")

        adapter_entries = []
        for terminal, (ti, slot) in sorted(TERMINALS.items(),
                                           key=lambda item: item[1][0]):
            source_desc = writers[terminal]["source"].finish(
                SOURCE_SCHEMA, "atomic_candidate_key", ["authority_candidate_ordinal"])
            normalized_desc = writers[terminal]["normalized"].finish(
                NORMALIZED_SCHEMA, "atomic_candidate_key",
                ["authority_candidate_ordinal"])
            proof_desc = writers[terminal]["proof"].finish(
                PROOF_SCHEMA, "proof_row_key",
                ["adapter_local_proof_ordinal__global_merge_must_resort"])
            need(source_desc["row_count"] == normalized_desc["row_count"]
                 == terminal_candidate_census[terminal]
                 and proof_desc["row_count"] == terminal_proof_census[terminal],
                 terminal + ":descriptor census")
            adapter_entries.append({
                "terminal_ordinal": ti, "terminal": terminal,
                "authority_slot": slot,
                "source_authority_ledger": source_desc,
                "normalized_candidate_ledger": normalized_desc,
                "materialized_proof_fragment_ledger": proof_desc,
                "candidate_count": terminal_candidate_census[terminal],
                "proof_row_count": terminal_proof_census[terminal],
                "unique_component_edge_count": len(terminal_edge_sets[terminal]),
            })

        body = {
            "schema": "cm2.c27-independent.primitive-v5-actual-three-terminal-atom-adapters.v1",
            "status": "PASS_T07_T08_T09_FRESH_NORMALIZED_ATOM_PAIR_INCIDENCE_ADAPTERS__ZERO_CREDIT",
            "terminal_adapters": adapter_entries,
            "exact_census": {
                "full_atom_rows": atom_rows,
                "exact_complement_atoms_excluded_from_terminal_candidates":
                    complement_atoms,
                "expanded_atom_pair_incidence_candidates": len(seen_atomic),
                "distinct_pair_authority_rows": len(pair_authority),
                "terminal_pair_census": dict(sorted(terminal_pair_census.items())),
                "terminal_candidate_census":
                    dict(sorted(terminal_candidate_census.items())),
                "terminal_proof_census": dict(sorted(terminal_proof_census.items())),
                "terminal_unique_component_edge_census": {
                    terminal: len(values)
                    for terminal, values in sorted(terminal_edge_sets.items())},
            },
            "closures": {
                "every_full_atom_incidence_joins_unique_pair_authority": True,
                "every_101080_pair_observed_in_at_least_one_atom_incidence": True,
                "every_normalized_candidate_has_materialized_source_row": True,
                "every_cross_component_proof_maps_pair_members_through_frozen_C15": True,
                "same_component_candidates_emit_no_component_edge_proof": True,
                "atom_complement_rows_do_not_invent_terminal_candidates": True,
            },
            "forbidden_input_governance": {
                "old_C27_FAMILIES_imported_or_read": False,
                "old_transition_ledger_imported_or_read": False,
                "C28_imported_or_read": False,
                "C29_imported_or_read": False,
                "historical_edge_ledger_used_as_candidate_universe": False,
                "strict_14772_used_as_candidate_universe": False,
                "scoped_14724_used_as_candidate_universe": False,
            },
            "formal_credit": 0, "manifest_authorized": False,
            "Source_W_transition_authorized": False,
            "strict_nonpromotion": {"C27_transition_totality": 0,
                                    "C28_pair_routing": 0,
                                    "C29_physical_maximality": 0,
                                    "CM2": "NO-GO_FOR_CLAIM"},
            "producer_source_sha256": file_sha(Path(__file__).resolve()),
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {label: capture.attestation()
                                 for label, capture in sorted(captures.items())}},
        }
        receipt = dict(body)
        receipt["receipt_sha256"] = digest(receipt)
        receipt_path = output / "adapter_receipt.json"
        receipt_path.write_bytes(canonical(receipt) + b"\n")
        manifest_lines = []
        for entry in adapter_entries:
            for key in ("source_authority_ledger", "normalized_candidate_ledger",
                        "materialized_proof_fragment_ledger"):
                item = entry[key]
                manifest_lines.append(f"{item['sha256']}  {item['path']}\n")
        manifest_lines.extend([
            f"{capture.sha256}  {capture.attestation()['path']}\n"
            for capture in captures.values()])
        manifest_lines.append(
            f"{file_sha(Path(__file__).resolve())}  {relative_self()}\n")
        manifest_lines.append(
            f"{file_sha(receipt_path)}  {receipt_path.relative_to(ROOT)}\n")
        (output / "manifest.sha256").write_text(
            "".join(sorted(set(manifest_lines))), encoding="ascii")
        return receipt
    finally:
        for groups in writers.values():
            for writer in groups.values():
                if not writer.raw.closed:
                    writer.stream.close()
                    writer.raw.close()
        for capture in captures.values():
            capture.close()


def relative_self() -> str:
    return str(Path(__file__).resolve().relative_to(ROOT))


def add_input(parser: argparse.ArgumentParser, name: str) -> None:
    parser.add_argument("--" + name, required=True)
    parser.add_argument("--" + name + "-sha256", required=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in ("c15", "pair-ownership", "full-atom-ledger",
                 "pair-union-receipt", "full-atom-receipt",
                 "full-atom-cold-receipt"):
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
