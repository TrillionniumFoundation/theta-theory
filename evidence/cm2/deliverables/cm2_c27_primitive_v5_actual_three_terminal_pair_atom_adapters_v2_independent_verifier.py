#!/usr/bin/env python3
"""No-producer-import inverse verifier for corrected T07/T08/T09 v2.

The verifier reconstructs candidate ownership and physical proofs from the
sealed 101,080 pair authority plus frozen C15, then reconstructs every atom
incidence and atom disposition from the sealed 483,232-atom authority.  It
also checks a second run for byte-identical ledgers.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
INCIDENCE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.atom-pair-incidence.row.v2"
DISPOSITION_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.atom-incidence-disposition.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
RECEIPT_SCHEMA = "cm2.c27-independent.primitive-v5-actual-three-terminal-pair-atom-adapters.v2"
PRODUCER = ROOT / "deliverables/cm2_c27_primitive_v5_actual_three_terminal_pair_atom_adapters_v2.py"
PRODUCER_SHA256 = "8b85ca7e84efde3c55ae54b6bd392de39741f29e29537c01e063cf1e697399e8"
EDGE_PREFIX = "round306c27r2-v5-component-edge:"
PAIR_PREFIX = "round306c27-v5-three-terminal-pair:"
INCIDENCE_PREFIX = "round306c27-v5-atom-pair-incidence:"
PROOF_PREFIX = "round306c27-v5-physical-proof:"
TERMINALS = {
    "SIGNED_BOUNDARY_FACES": (7, "T07_SIGNED_BOUNDARY_FACES"),
    "COMPLETE_BOUNDARY_FACES": (8, "T08_COMPLETE_BOUNDARY_FACES"),
    "POSITIVE_VOLUME_CARRIERS": (9, "T09_POSITIVE_VOLUME_CARRIERS"),
}
EXPECTED_PAIRS = {"SIGNED_BOUNDARY_FACES": 25_452,
                  "COMPLETE_BOUNDARY_FACES": 10_688,
                  "POSITIVE_VOLUME_CARRIERS": 64_940}
EXPECTED_INPUTS = {
    "interface_v2": "6873b33d7b131a4bde0c4dbcf99873e6826cf2190fde6dfdf6640ee47d53c9d6",
    "C15": "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    "pair_ownership": "caaee424b629887ce8d44479861f311f802140cdd9adcd4dcf7556b1c6eb5fe2",
    "full_atom_ledger": "9b642b40fea1bbae5121ca9fcc43461795190c92f38753d41ff7d0e4e358b114",
    "pair_union_receipt": "fc5d28d6046dea6546061171acd03b55dbc6aa2fc89deb506a1167ab519dbc09",
    "full_atom_receipt": "456d462da8f269112908caaed8bb30a9ff042d54760136c675d00abda28f0241",
    "full_atom_cold_receipt": "f9a25afa9beea59abaf37aeb5c2eb81ac03a9dee7328ee1db53f827db3af3977",
}
EMPTY_SHA = hashlib.sha256(b"").hexdigest()


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


def root_path(text: str) -> Path:
    path = (ROOT / text).resolve()
    need(path == ROOT or ROOT in path.parents, "path escapes workspace")
    return path


def document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    row = json.loads(payload)
    need(type(row) is dict and canonical(row) in {payload, payload.rstrip(b"\n")},
         "canonical document:" + path.name)
    body = dict(row)
    claim = body.pop(closure, None)
    need(type(claim) is str and claim == digest(body),
         "document closure:" + path.name)
    return row


def raw_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            payload = line[:-1]
            row = json.loads(payload)
            need(type(row) is dict and canonical(row) == payload,
                 f"canonical:{path.name}:{ordinal}")
            body = dict(row)
            claim = body.pop("row_sha256", None)
            need(type(claim) is str and claim == digest(body),
                 f"closure:{path.name}:{ordinal}")
            yield row


def descriptor_rows(desc: dict[str, Any]) -> Iterator[dict[str, Any]]:
    path = root_path(desc["path"])
    need(path.is_file() and path.stat().st_size == desc["size"]
         and fsha(path) == desc["sha256"], "descriptor file:" + path.name)
    count = 0
    sequence = hashlib.sha256()
    for row in raw_rows(path):
        need(row["schema"] == desc["row_schema"],
             "descriptor schema:" + path.name)
        sequence.update(row["row_sha256"].encode("ascii") + b"\n")
        count += 1
        yield row
    need(count == desc["row_count"]
         and sequence.hexdigest() == desc["row_sequence_sha256"],
         "descriptor census/sequence:" + path.name)


def one_next(iterator: Iterator[dict[str, Any]], label: str) -> dict[str, Any]:
    try:
        return next(iterator)
    except StopIteration as error:
        raise Failure("early EOF:" + label) from error


def no_extra(iterator: Iterator[dict[str, Any]], label: str) -> None:
    try:
        next(iterator)
    except StopIteration:
        return
    raise Failure("extra row:" + label)


def ordered_pair(value: Any, label: str) -> tuple[str, str]:
    need(type(value) is list and len(value) == 2
         and all(type(item) is str for item in value)
         and value[0] != value[1], label + ":pair")
    return tuple(sorted(value))


def sequence_sha(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def expected_manifest(receipt_path: Path, receipt: dict[str, Any]) -> bytes:
    lines = []
    for entry in receipt["terminal_adapters"]:
        for key in ("candidate_ownership_ledger",
                    "materialized_physical_proof_fragment_ledger"):
            desc = entry[key]
            lines.append(f"{desc['sha256']}  {desc['path']}\n")
    for key in ("atom_pair_incidence_ledger",
                "atom_incidence_disposition_ledger"):
        desc = receipt[key]
        lines.append(f"{desc['sha256']}  {desc['path']}\n")
    for attestation in receipt["root_input_capture"]["attestations"].values():
        lines.append(f"{attestation['sha256']}  {attestation['path']}\n")
    lines.extend((
        f"{PRODUCER_SHA256}  {PRODUCER.relative_to(ROOT)}\n",
        f"{fsha(receipt_path)}  {receipt_path.relative_to(ROOT)}\n",
    ))
    return "".join(sorted(set(lines))).encode("ascii")


def verify_receipt_shell(receipt_path: Path) -> dict[str, Any]:
    receipt = document(receipt_path, "receipt_sha256")
    need(receipt["schema"] == RECEIPT_SCHEMA
         and receipt["formal_credit"] == 0
         and receipt["manifest_authorized"] is False
         and receipt["producer_source_sha256"] == PRODUCER_SHA256
         and fsha(PRODUCER) == PRODUCER_SHA256,
         "receipt governance/source")
    need(receipt["exact_census"] == {
        "candidate_pair_count": 101_080,
        "terminal_candidate_pair_census": EXPECTED_PAIRS,
        "cross_component_candidate_pair_census": {
            "POSITIVE_VOLUME_CARRIERS": 32_608},
        "physical_proof_row_count": 32_608,
        "full_atom_rows": 483_232,
        "atom_pair_incidence_count": 206_632,
        "atom_pair_incidence_terminal_census": {
            "SIGNED_BOUNDARY_FACES": 55_536,
            "COMPLETE_BOUNDARY_FACES": 30_624,
            "POSITIVE_VOLUME_CARRIERS": 120_472},
        "incident_atoms": 62_768,
        "exact_complement_atoms": 420_464,
        "multi_terminal_atoms": 3_896,
        "unique_component_edges": 14_724,
    }, "receipt exact census")
    closures = receipt["separation_closures"]
    need(all(value is True for value in closures.values()),
         "all separation closures")
    forbidden = receipt["forbidden_input_governance"]
    need(all(value is False for value in forbidden.values()),
         "forbidden inputs absent")
    attestations = receipt["root_input_capture"]["attestations"]
    need(set(attestations) == set(EXPECTED_INPUTS), "input labels")
    for label, pin in EXPECTED_INPUTS.items():
        item = attestations[label]
        path = root_path(item["path"])
        info = path.stat()
        observed_fp = [info.st_dev, info.st_ino, info.st_size,
                       info.st_mtime_ns, info.st_ctime_ns, info.st_mode,
                       info.st_uid, info.st_gid]
        need(item["sha256"] == pin and fsha(path) == pin
             and item["size"] == info.st_size
             and item["stat_fingerprint"] == observed_fp
             and item["O_NOFOLLOW"] is True
             and item["single_open_file_description_hash_parse_fstat"] is True,
             "input attestation:" + label)
    manifest = receipt_path.parent / "manifest.sha256"
    need(manifest.is_file()
         and manifest.read_bytes() == expected_manifest(receipt_path, receipt),
         "exact output manifest")
    return receipt


def verify_second(first: dict[str, Any], second_path: Path) -> dict[str, Any]:
    second = verify_receipt_shell(second_path)
    need(second["exact_census"] == first["exact_census"],
         "dual-run census")
    first_entries = first["terminal_adapters"]
    second_entries = second["terminal_adapters"]
    need(len(first_entries) == len(second_entries) == 3, "dual terminal count")
    checked = 0
    for left, right in zip(first_entries, second_entries):
        need((left["terminal_ordinal"], left["terminal"], left["authority_slot"])
             == (right["terminal_ordinal"], right["terminal"],
                 right["authority_slot"]), "dual terminal identity")
        for key in ("candidate_ownership_ledger",
                    "materialized_physical_proof_fragment_ledger"):
            a, b = left[key], right[key]
            need(a["sha256"] == b["sha256"]
                 and root_path(a["path"]).read_bytes()
                    == root_path(b["path"]).read_bytes(),
                 "dual-run byte identity:" + key)
            checked += 1
    for key in ("atom_pair_incidence_ledger",
                "atom_incidence_disposition_ledger"):
        a, b = first[key], second[key]
        need(a["sha256"] == b["sha256"]
             and root_path(a["path"]).read_bytes()
                == root_path(b["path"]).read_bytes(),
             "dual-run byte identity:" + key)
        checked += 1
    return {"byte_identical_ledger_count": checked,
            "second_receipt_file_sha256": fsha(second_path),
            "second_receipt_object_sha256": second["receipt_sha256"]}


def verify(receipt_path: Path, second_path: Path) -> dict[str, Any]:
    receipt = verify_receipt_shell(receipt_path)
    dual = verify_second(receipt, second_path)
    attest = receipt["root_input_capture"]["attestations"]
    c15_path = root_path(attest["C15"]["path"])
    pair_path = root_path(attest["pair_ownership"]["path"])
    atom_path = root_path(attest["full_atom_ledger"]["path"])

    member_component: dict[str, str] = {}
    components = set()
    for ordinal, row in enumerate(raw_rows(c15_path)):
        need(row["member_ordinal"] == ordinal, "C15 ordinal")
        member = row["registry_member_id"]
        need(member not in member_component, "C15 member uniqueness")
        member_component[member] = row["fresh_component_id"]
        components.add(row["fresh_component_id"])
    need(len(member_component) == 502_204 and len(components) == 57_876,
         "C15 census")

    records = []
    seen_pairs = set()
    for ordinal, source in enumerate(raw_rows(pair_path)):
        pair = ordered_pair(source["pair_key"], f"pair:{ordinal}")
        need(pair not in seen_pairs, "pair uniqueness")
        seen_pairs.add(pair)
        terminal = source["assigned_terminal"]
        need(terminal in TERMINALS and source["formal_credit"] == 0,
             "pair terminal")
        ti, slot = TERMINALS[terminal]
        key = PAIR_PREFIX + digest(list(pair))
        component_pair = tuple(sorted((member_component[pair[0]],
                                       member_component[pair[1]])))
        cross = component_pair[0] != component_pair[1]
        proof_body = None
        if cross:
            witness = "three-terminal-formal-pair-witness:" + digest([
                key, list(pair), source["source_row_sha256"],
                source.get("C24A_G2B_exact_row_sha256")])
            edge = EDGE_PREFIX + digest(list(component_pair))
            proof_key = PROOF_PREFIX + digest([
                key, witness, list(pair), list(component_pair)])
            proof_body = {
                "schema": PROOF_SCHEMA, "ordinal": -1,
                "proof_row_key": proof_key, "candidate_key": key,
                "atom_pair_incidence_key_or_null": None,
                "terminal": terminal, "authority_slot": slot,
                "primitive_authority_row_sha256": source["row_sha256"],
                "ordered_C15_member_pair": list(pair),
                "ordered_C15_component_pair": list(component_pair),
                "component_edge_key": edge,
                "physical_witness_key": witness, "formal_credit": 0,
            }
        records.append({"pair": pair, "key": key, "terminal": terminal,
                        "ti": ti, "slot": slot,
                        "source_sha": source["row_sha256"],
                        "proof_body": proof_body})
    need(len(records) == 101_080, "candidate source census")
    records.sort(key=lambda item: item["key"])

    entry_by_terminal = {entry["terminal"]: entry
                         for entry in receipt["terminal_adapters"]}
    need(set(entry_by_terminal) == set(TERMINALS), "terminal entries")
    candidate_iters = {}
    proof_iters = {}
    for terminal, (ti, slot) in TERMINALS.items():
        entry = entry_by_terminal[terminal]
        need(entry["terminal_ordinal"] == ti and entry["authority_slot"] == slot,
             "terminal slot:" + terminal)
        cdesc = entry["candidate_ownership_ledger"]
        pdesc = entry["materialized_physical_proof_fragment_ledger"]
        need(cdesc["row_schema"] == CANDIDATE_SCHEMA
             and cdesc["unique_key"] == "candidate_key"
             and cdesc["ordering"] == ["candidate_key"]
             and pdesc["row_schema"] == PROOF_SCHEMA
             and pdesc["unique_key"] == "proof_row_key"
             and pdesc["ordering"] == ["candidate_key"],
             "terminal descriptors:" + terminal)
        candidate_iters[terminal] = descriptor_rows(cdesc)
        proof_iters[terminal] = descriptor_rows(pdesc)

    candidate_ordinals = Counter()
    proof_ordinals = Counter()
    candidate_by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    edge_keys = set()
    proof_count = 0
    for record in records:
        terminal = record["terminal"]
        proof_body = record["proof_body"]
        proof = None
        proof_sequence = EMPTY_SHA
        if proof_body is not None:
            proof_body["ordinal"] = proof_ordinals[terminal]
            proof = close(proof_body)
            observed_proof = one_next(proof_iters[terminal], terminal + ":proof")
            need(observed_proof == proof, "inverse proof row:" + terminal)
            proof_ordinals[terminal] += 1
            proof_count += 1
            proof_sequence = sequence_sha([proof["row_sha256"]])
            edge_keys.add(proof["component_edge_key"])
        expected = close({
            "schema": CANDIDATE_SCHEMA,
            "ordinal": candidate_ordinals[terminal],
            "candidate_key": record["key"],
            "candidate_kind": "THREE_TERMINAL_CANDIDATE_PAIR",
            "candidate_pair_key_or_null": record["key"],
            "terminal_ordinal": record["ti"], "terminal": terminal,
            "authority_slot": record["slot"],
            "primitive_authority_row_sha256": record["source_sha"],
            "component_relation_disposition": (
                "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED"
                if proof is not None else
                "SAME_FROZEN_C15_COMPONENT__NO_EDGE"),
            "physical_proof_row_count": int(proof is not None),
            "physical_proof_row_sequence_sha256": proof_sequence,
            "formal_credit": 0,
        })
        observed = one_next(candidate_iters[terminal], terminal + ":candidate")
        need(observed == expected, "inverse candidate row:" + terminal)
        candidate_by_pair[record["pair"]] = expected
        candidate_ordinals[terminal] += 1
    for terminal in TERMINALS:
        no_extra(candidate_iters[terminal], terminal + ":candidate")
        no_extra(proof_iters[terminal], terminal + ":proof")
    need(dict(candidate_ordinals) == EXPECTED_PAIRS and proof_count == 32_608
         and len(edge_keys) == 14_724, "candidate/proof/edge census")

    incidence_desc = receipt["atom_pair_incidence_ledger"]
    disposition_desc = receipt["atom_incidence_disposition_ledger"]
    need(incidence_desc["row_schema"] == INCIDENCE_SCHEMA
         and incidence_desc["unique_key"]
            == ["primitive_support_atom_key", "candidate_pair_key"]
         and incidence_desc["ordering"]
            == ["primitive_support_atom_key", "candidate_pair_key"],
         "incidence descriptor contract")
    need(disposition_desc["row_schema"] == DISPOSITION_SCHEMA
         and disposition_desc["unique_key"] == "primitive_support_atom_key"
         and disposition_desc["ordering"] == ["primitive_support_atom_key"],
         "disposition descriptor contract")
    incidence_iter = descriptor_rows(incidence_desc)
    disposition_iter = descriptor_rows(disposition_desc)
    incidence_count = incident_atoms = complement_atoms = multi_terminal = 0
    previous_atom = None
    observed_pairs = set()
    for atom_ordinal, atom in enumerate(raw_rows(atom_path)):
        atom_key = atom["atom_id"]
        need(previous_atom is None or previous_atom < atom_key,
             "source atom ordering")
        previous_atom = atom_key
        routes = atom["incident_union_pair_routes"]
        need(len(routes) == atom["candidate_incidence_count"],
             "source atom incidence count")
        route_records = []
        for route in routes:
            pieces = route["pair_key"].split("|")
            pair = tuple(sorted(pieces))
            need(len(pieces) == 2 and pair in candidate_by_pair,
                 "source route pair")
            candidate = candidate_by_pair[pair]
            need(route["assigned_terminal"] == candidate["terminal"],
                 "source route terminal")
            route_records.append((candidate["candidate_key"], candidate, pair))
        route_records.sort(key=lambda item: item[0])
        per_atom_shas = []
        terminals = set()
        for candidate_key, candidate, pair in route_records:
            incidence_key = INCIDENCE_PREFIX + digest([atom_key, candidate_key])
            expected = close({
                "schema": INCIDENCE_SCHEMA, "ordinal": incidence_count,
                "incidence_key": incidence_key,
                "primitive_support_atom_key": atom_key,
                "candidate_pair_key": candidate_key,
                "candidate_terminal": candidate["terminal"],
                "candidate_owner_row_sha256": candidate["row_sha256"],
                "formal_credit": 0,
            })
            observed = one_next(incidence_iter, "incidence")
            need(observed == expected, "inverse incidence row")
            per_atom_shas.append(expected["row_sha256"])
            terminals.add(candidate["terminal"])
            observed_pairs.add(pair)
            incidence_count += 1
        is_incident = bool(route_records)
        incident_atoms += int(is_incident)
        complement_atoms += int(not is_incident)
        multi_terminal += int(len(terminals) > 1)
        expected_disposition = close({
            "schema": DISPOSITION_SCHEMA, "ordinal": atom_ordinal,
            "primitive_support_atom_key": atom_key,
            "incidence_count": len(route_records),
            "incidence_row_sequence_sha256": sequence_sha(per_atom_shas),
            "terminal_set": sorted(terminals),
            "disposition": (
                "EXACT_NONEMPTY_ATOM_PAIR_INCIDENCE_SET" if is_incident
                else "EXACT_EMPTY_INCIDENCE_COMPLEMENT"),
            "formal_credit": 0,
        })
        observed_disposition = one_next(disposition_iter, "disposition")
        need(observed_disposition == expected_disposition,
             "inverse atom disposition row")
    no_extra(incidence_iter, "incidence")
    no_extra(disposition_iter, "disposition")
    need(incidence_count == 206_632 and incident_atoms == 62_768
         and complement_atoms == 420_464 and multi_terminal == 3_896
         and observed_pairs == seen_pairs, "inverse atom exact census")

    stable = {
        "candidate_pair_count": len(records),
        "physical_proof_row_count": proof_count,
        "unique_component_edge_count": len(edge_keys),
        "atom_pair_incidence_count": incidence_count,
        "atom_disposition_count": incident_atoms + complement_atoms,
        "incident_atoms": incident_atoms,
        "exact_complement_atoms": complement_atoms,
        "multi_terminal_atoms": multi_terminal,
        **dual,
    }
    body = {
        "schema": "cm2.c27-independent.primitive-v5-actual-three-terminal-pair-atom-adapters-v2-independent-verification.v1",
        "status": "PASS_NO_PRODUCER_IMPORT_INVERSE_RECONSTRUCTION__DUAL_RUN_BYTE_IDENTICAL__ZERO_CREDIT",
        "verified_receipt_file_sha256": fsha(receipt_path),
        "verified_receipt_object_sha256": receipt["receipt_sha256"],
        "producer_imported": False,
        "inverse_reconstruction": {
            "candidate_ownership_from_pair_authority_and_C15": True,
            "physical_proof_from_member_pair_and_frozen_C15": True,
            "atom_pair_incidence_from_full_atom_routes": True,
            "atom_disposition_from_exact_incidence_set": True,
            "manifest_reconstructed_exactly": True,
        },
        "exact_census": stable,
        "formal_credit": 0, "manifest_authorized": False,
        "C27_C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        "verifier_source_sha256": fsha(Path(__file__).resolve()),
    }
    result = dict(body)
    result["verification_sha256"] = digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--second-receipt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    try:
        need(not output.exists(), "fresh output")
        result = verify(Path(args.receipt).resolve(),
                        Path(args.second_receipt).resolve())
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(canonical(result) + b"\n")
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "exact_census": result["exact_census"],
                     "verification_sha256": result["verification_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
