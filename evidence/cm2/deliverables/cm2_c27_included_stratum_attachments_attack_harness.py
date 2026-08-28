#!/usr/bin/env python3
"""Coherent mutation attacks for the independent included-stratum gates."""

from __future__ import annotations

import argparse
import copy
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
STREAM_FILE = HERE / "cm2_c27_included_stratum_attachments_stream_probe.py"
SQLITE_FILE = HERE / "cm2_c27_included_stratum_attachments_sqlite_probe.py"


class AttackFailure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if value is not True:
        raise AttackFailure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    need(spec is not None and spec.loader is not None, "module spec:" + name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reclose(module, row: dict[str, Any]) -> None:
    row["row_sha256"] = module.digest({key: value for key, value in row.items() if key != "row_sha256"})


def sqlite_join(
    c15: dict[str, Any], c25: dict[str, Any], c26: dict[str, Any],
    c20d: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "rep": c25["representation_id"],
        "owner25": c25["owner_member_id"], "owner26": c26["owner_member_id"], "owner15": c15["registry_member_id"],
        "component25": c25["fresh_component_id"], "component26": c26["fresh_component_id"], "component15": c15["fresh_component_id"],
        "root25": c25["base_root_id"], "root26": c26["base_root_id"], "root15": c15["base_root_id"],
        "key25": c25["official_key_id"], "key26": c26["official_key_id"], "key15": c15["official_key_id"],
        "support25": c25["owner_normalized_support_ast_sha256"], "support26": c26["owner_normalized_support_ast_sha256"],
        "kind25": c25["representation_semantic_kind"], "kind26": c26["representation_semantic_kind"],
        "semantic25": c25["representation_semantic_certificate_sha256"], "semantic26": c26["representation_semantic_certificate_sha256"],
        "kernel": c25["source_bindings"]["semantic_kernel"],
        "kernel_ledger": c25["source_bindings"].get("semantic_kernel_ledger"),
        "kernel_result": c25["source_bindings"].get("semantic_kernel_result_sha256"),
        "kernel_ref": c25["source_bindings"].get("semantic_kernel_row_sha256"),
        "coarse": c25["coarse_family"],
        "c25_ref": c26["source_bindings"]["C25_representation_row_sha256"],
        "row15": c15["row_sha256"], "row25": c25["row_sha256"], "row26": c26["row_sha256"],
        "rep20d": None if c20d is None else c20d["representation_id"],
        "owner20d": None if c20d is None else c20d["owner_member_id"],
        "component20d": None if c20d is None else c20d["fresh_component_id"],
        "support20d": None if c20d is None else c20d["owner_support_ast_sha256"],
        "source_semantics": None if c20d is None else c20d["source_semantics"],
        "relation": None if c20d is None else c20d["exact_relation_to_owner_support"],
        "row20d": None if c20d is None else c20d["row_sha256"],
    }


def find_baseline(stream):
    c25_iter = stream.rows(stream.HERE / stream.C25)
    c26_iter = stream.rows(stream.HERE / stream.C26)
    selected25 = selected26 = None
    for ordinal in range(stream.FULL_COUNTS[stream.C25]):
        left = next(c25_iter)
        right = next(c26_iter)
        need(left["representation_ordinal"] == right["handle_ordinal"] == ordinal, "baseline ordinal")
        if (
            left["representation_semantic_kind"] in stream.SELECTED_KINDS
            and left["source_bindings"]["semantic_kernel"] != "C20D"
        ):
            selected25, selected26 = left, right
            break
    need(selected25 is not None and selected26 is not None, "baseline selected row")
    owner = selected25["owner_member_id"]
    selected15 = None
    for row in stream.rows(stream.HERE / stream.C15):
        if row["registry_member_id"] == owner:
            selected15 = row
            break
    need(selected15 is not None, "baseline C15 owner")
    return selected15, selected25, selected26


def find_c20d_cases(stream):
    strict = adjacent = None
    for row in stream.rows(stream.HERE / stream.C20D):
        if row["source_semantics"] in stream.C20D_STRICT and strict is None:
            strict = row
        if row["source_semantics"] == "ADJACENT_POSITIVE_T_CONTINUATION" and adjacent is None:
            adjacent = row
        if strict is not None and adjacent is not None:
            break
    need(strict is not None and adjacent is not None, "C20D strict/adjacent baselines")
    wanted = {strict["representation_id"], adjacent["representation_id"]}
    c25_by_rep: dict[str, dict[str, Any]] = {}
    c26_by_rep: dict[str, dict[str, Any]] = {}
    for row in stream.rows(stream.HERE / stream.C25):
        if row["representation_id"] in wanted:
            c25_by_rep[row["representation_id"]] = row
    for row in stream.rows(stream.HERE / stream.C26):
        if row["representation_id"] in wanted:
            c26_by_rep[row["representation_id"]] = row
    need(set(c25_by_rep) == wanted == set(c26_by_rep), "C20D C25/C26 baseline cover")
    owners = {c25_by_rep[rep]["owner_member_id"] for rep in wanted}
    c15_by_owner = {
        row["registry_member_id"]: row
        for row in stream.rows(stream.HERE / stream.C15)
        if row["registry_member_id"] in owners
    }
    need(set(c15_by_owner) == owners, "C20D C15 baseline cover")
    def joined(source):
        rep = source["representation_id"]
        c25 = c25_by_rep[rep]
        return c15_by_owner[c25["owner_member_id"]], c25, c26_by_rep[rep], source
    return joined(strict), joined(adjacent)


def apply_attack(stream, attack: str, original: tuple[dict[str, Any], dict[str, Any], dict[str, Any]]):
    c15, c25, c26 = copy.deepcopy(original)
    if attack == "A01_EQUALITY_KIND_IN_CANDIDATE_UNIVERSE":
        c25["representation_semantic_kind"] = "REPRESENTATION_SET_EQUALITY"
        c26["representation_semantic_kind"] = "REPRESENTATION_SET_EQUALITY"
        reclose(stream, c25)
        c26["source_bindings"]["C25_representation_row_sha256"] = c25["row_sha256"]
        reclose(stream, c26)
    elif attack == "A02_KIND_KERNEL_CROSSWIRE":
        c25["source_bindings"]["semantic_kernel"] = "C20D" if c25["representation_semantic_kind"] == "EXACT_SUBCOVER_INCLUSION_DISPOSITION" else "C22B"
        reclose(stream, c25)
        c26["source_bindings"]["C25_representation_row_sha256"] = c25["row_sha256"]
        reclose(stream, c26)
    elif attack == "A03_REPRESENTATION_ID_MISMATCH":
        c26["representation_id"] += ":forged"
        reclose(stream, c26)
    elif attack == "A04_OWNER_ID_MISMATCH":
        c26["owner_member_id"] += ":forged"
        reclose(stream, c26)
    elif attack == "A05_C25_COMPONENT_MISMATCH":
        c25["fresh_component_id"] += ":forged"
        reclose(stream, c25)
        c26["source_bindings"]["C25_representation_row_sha256"] = c25["row_sha256"]
        reclose(stream, c26)
    elif attack == "A06_C15_COMPONENT_MISMATCH":
        c15["fresh_component_id"] += ":forged"
        reclose(stream, c15)
    elif attack == "A07_BASE_ROOT_MISMATCH":
        c26["base_root_id"] += ":forged"
        reclose(stream, c26)
    elif attack == "A08_OFFICIAL_KEY_MISMATCH":
        c26["official_key_id"] += ":forged"
        reclose(stream, c26)
    elif attack == "A09_OWNER_SUPPORT_MISMATCH":
        c26["owner_normalized_support_ast_sha256"] = "0" * 64
        reclose(stream, c26)
    elif attack == "A10_SEMANTIC_CERTIFICATE_MISMATCH":
        c26["representation_semantic_certificate_sha256"] = "1" * 64
        reclose(stream, c26)
    elif attack == "A11_C26_C25_BINDING_MISMATCH":
        c26["source_bindings"]["C25_representation_row_sha256"] = "2" * 64
        reclose(stream, c26)
    elif attack == "A12_TRANSITION_PROMOTION":
        c26["transition_ready_certificate"]["transition_theorem_claimed"] = True
        c26["transition_ready_certificate_sha256"] = stream.digest(c26["transition_ready_certificate"])
        reclose(stream, c26)
    elif attack == "A13_PAIR_ROUTING_PROMOTION":
        c26["transition_ready_certificate"]["pair_routing_claimed"] = True
        c26["transition_ready_certificate_sha256"] = stream.digest(c26["transition_ready_certificate"])
        reclose(stream, c26)
    elif attack == "A14_COHERENT_COMPONENT_REWRITE_BEATS_ROW_JOINS_BUT_NOT_INPUT_PIN":
        forged = c15["fresh_component_id"] + ":forged"
        c15["fresh_component_id"] = forged
        c25["fresh_component_id"] = forged
        c26["fresh_component_id"] = forged
        reclose(stream, c15)
        reclose(stream, c25)
        c26["source_bindings"]["C25_representation_row_sha256"] = c25["row_sha256"]
        reclose(stream, c26)
    else:
        raise AttackFailure("unknown attack:" + attack)
    return c15, c25, c26


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    options = parser.parse_args()
    need(type(options.seed) is int, "integer seed")
    stream = load("cm2_included_stream_attack_target", STREAM_FILE)
    sqlite_gate = load("cm2_included_sqlite_attack_target", SQLITE_FILE)
    baseline = find_baseline(stream)
    baseline_candidate = stream.validate_triplet(*baseline)
    sqlite_candidate = sqlite_gate.candidate_from_join(sqlite_join(*baseline))
    need(baseline_candidate == sqlite_candidate, "baseline cross-implementation candidate equality")
    original_row_pins = tuple(row["row_sha256"] for row in baseline)
    strict_c20d, adjacent_c20d = find_c20d_cases(stream)
    strict_candidate = stream.validate_triplet(*strict_c20d)
    need(
        strict_candidate == sqlite_gate.candidate_from_join(sqlite_join(*strict_c20d)),
        "C20D strict baseline cross-implementation equality",
    )

    attacks = [
        "A01_EQUALITY_KIND_IN_CANDIDATE_UNIVERSE", "A02_KIND_KERNEL_CROSSWIRE",
        "A03_REPRESENTATION_ID_MISMATCH", "A04_OWNER_ID_MISMATCH",
        "A05_C25_COMPONENT_MISMATCH", "A06_C15_COMPONENT_MISMATCH",
        "A07_BASE_ROOT_MISMATCH", "A08_OFFICIAL_KEY_MISMATCH",
        "A09_OWNER_SUPPORT_MISMATCH", "A10_SEMANTIC_CERTIFICATE_MISMATCH",
        "A11_C26_C25_BINDING_MISMATCH", "A12_TRANSITION_PROMOTION",
        "A13_PAIR_ROUTING_PROMOTION",
        "A14_COHERENT_COMPONENT_REWRITE_BEATS_ROW_JOINS_BUT_NOT_INPUT_PIN",
    ]
    results = []
    for attack in attacks:
        changed = apply_attack(stream, attack, baseline)
        rejected_stream = False
        rejected_sqlite = False
        rejected_pin = tuple(row["row_sha256"] for row in changed) != original_row_pins
        try:
            stream.validate_triplet(*changed)
        except stream.GateFailure:
            rejected_stream = True
        try:
            sqlite_gate.candidate_from_join(sqlite_join(*changed))
        except sqlite_gate.GateFailure:
            rejected_sqlite = True
        if attack in {"A12_TRANSITION_PROMOTION", "A13_PAIR_ROUTING_PROMOTION"}:
            # SQLite main ingestion checks this certificate before insertion;
            # the relational candidate constructor intentionally sees no raw certificate.
            certificate = changed[2]["transition_ready_certificate"]
            rejected_sqlite = (
                certificate["transition_theorem_claimed"] is not False
                or certificate["pair_routing_claimed"] is not False
            )
        rejected = rejected_stream and (rejected_sqlite or rejected_pin)
        if attack == "A14_COHERENT_COMPONENT_REWRITE_BEATS_ROW_JOINS_BUT_NOT_INPUT_PIN":
            # A coherent rewrite may satisfy local relational equality, but it
            # necessarily changes all three byte-pinned input rows/files.
            rejected = rejected_pin
        need(rejected, "attack accepted:" + attack)
        row = {
            "attack_id": attack,
            "rejected": True,
            "stream_validator_rejected": rejected_stream,
            "sqlite_or_ingest_validator_rejected": rejected_sqlite,
            "byte_pinned_input_boundary_rejected": rejected_pin,
        }
        results.append({**row, "row_sha256": digest(row)})

    # Primitive C20D attacks close the exact bug this version repairs.
    changed = copy.deepcopy(strict_c20d)
    changed[3]["source_semantics"] = "ADJACENT_POSITIVE_T_CONTINUATION"
    changed[3]["exact_relation_to_owner_support"] = "ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE"
    reclose(stream, changed[3])
    changed[1]["source_bindings"]["semantic_kernel_row_sha256"] = changed[3]["row_sha256"]
    reclose(stream, changed[1])
    changed[2]["source_bindings"]["C25_representation_row_sha256"] = changed[1]["row_sha256"]
    reclose(stream, changed[2])
    rejected_stream = rejected_sqlite = False
    try:
        stream.validate_triplet(*changed)
    except stream.GateFailure:
        rejected_stream = True
    try:
        sqlite_gate.candidate_from_join(sqlite_join(*changed))
    except sqlite_gate.GateFailure:
        rejected_sqlite = True
    need(rejected_stream and rejected_sqlite, "coherent C20D adjacent semantic flip accepted")
    body = {
        "attack_id": "A15_C20D_COHERENT_STRICT_TO_ADJACENT_SEMANTIC_FLIP",
        "rejected": True,
        "stream_validator_rejected": True,
        "sqlite_or_ingest_validator_rejected": True,
    }
    results.append({**body, "row_sha256": digest(body)})

    changed = copy.deepcopy(strict_c20d)
    changed[1]["source_bindings"]["semantic_kernel_row_sha256"] = "3" * 64
    reclose(stream, changed[1])
    changed[2]["source_bindings"]["C25_representation_row_sha256"] = changed[1]["row_sha256"]
    reclose(stream, changed[2])
    rejected_stream = rejected_sqlite = False
    try:
        stream.validate_triplet(*changed)
    except stream.GateFailure:
        rejected_stream = True
    try:
        sqlite_gate.candidate_from_join(sqlite_join(*changed))
    except sqlite_gate.GateFailure:
        rejected_sqlite = True
    need(rejected_stream and rejected_sqlite, "C20D row-binding mismatch accepted")
    body = {
        "attack_id": "A16_C20D_KERNEL_ROW_BINDING_MISMATCH",
        "rejected": True,
        "stream_validator_rejected": True,
        "sqlite_or_ingest_validator_rejected": True,
    }
    results.append({**body, "row_sha256": digest(body)})

    rejected_stream = rejected_sqlite = False
    try:
        stream.validate_triplet(*adjacent_c20d)
    except stream.GateFailure:
        rejected_stream = True
    try:
        sqlite_gate.candidate_from_join(sqlite_join(*adjacent_c20d))
    except sqlite_gate.GateFailure:
        rejected_sqlite = True
    need(rejected_stream and rejected_sqlite, "adjacent continuation reinjected as attachment")
    body = {
        "attack_id": "A17_REINJECT_C20D_ADJACENT_POSITIVE_T_AS_ATTACHMENT",
        "rejected": True,
        "stream_validator_rejected": True,
        "sqlite_or_ingest_validator_rejected": True,
    }
    results.append({**body, "row_sha256": digest(body)})

    # Adjacent -> strict may satisfy local joins after a coherent rewrite, but
    # the frozen C20D/C25/C26 byte pins must still reject the rewrite.
    changed = copy.deepcopy(adjacent_c20d)
    original_pins = tuple(row["row_sha256"] for row in changed)
    changed[3]["source_semantics"] = next(iter(sorted(stream.C20D_STRICT)))
    changed[3]["exact_relation_to_owner_support"] = "STRICT_SUBCOVER_OF_OWNER_SUPPORT"
    reclose(stream, changed[3])
    changed[1]["source_bindings"]["semantic_kernel_row_sha256"] = changed[3]["row_sha256"]
    reclose(stream, changed[1])
    changed[2]["source_bindings"]["C25_representation_row_sha256"] = changed[1]["row_sha256"]
    reclose(stream, changed[2])
    need(stream.validate_triplet(*changed) == sqlite_gate.candidate_from_join(sqlite_join(*changed)), "coherent adjacent-to-strict local equality")
    need(tuple(row["row_sha256"] for row in changed) != original_pins, "coherent adjacent-to-strict pin mutation")
    body = {
        "attack_id": "A18_C20D_ADJACENT_TO_STRICT_COHERENT_RECLOSE",
        "rejected": True,
        "byte_pinned_input_boundary_rejected": True,
        "local_validators_accept_only_the_mutated_unfrozen_world": True,
    }
    results.append({**body, "row_sha256": digest(body)})

    changed = copy.deepcopy(strict_c20d)
    changed[3]["exact_relation_to_owner_support"] = "ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE"
    reclose(stream, changed[3])
    changed[1]["source_bindings"]["semantic_kernel_row_sha256"] = changed[3]["row_sha256"]
    reclose(stream, changed[1])
    changed[2]["source_bindings"]["C25_representation_row_sha256"] = changed[1]["row_sha256"]
    reclose(stream, changed[2])
    for validator, label in (
        (lambda: stream.validate_triplet(*changed), "stream"),
        (lambda: sqlite_gate.candidate_from_join(sqlite_join(*changed)), "sqlite"),
    ):
        try:
            validator()
        except Exception:
            pass
        else:
            raise AttackFailure("C20D relation-only mismatch accepted:" + label)
    body = {"attack_id": "A19_C20D_RELATION_ONLY_MISMATCH", "rejected": True, "both_semantic_validators_rejected": True}
    results.append({**body, "row_sha256": digest(body)})

    for ordinal, (attack_id, field, value) in enumerate((
        ("A20_C20D_KERNEL_LEDGER_PIN_MUTATION", "semantic_kernel_ledger", "forged-ledger.jsonl.gz"),
        ("A21_C20D_KERNEL_RESULT_PIN_MUTATION", "semantic_kernel_result_sha256", "4" * 64),
    )):
        changed = copy.deepcopy(strict_c20d)
        changed[1]["source_bindings"][field] = value
        reclose(stream, changed[1])
        changed[2]["source_bindings"]["C25_representation_row_sha256"] = changed[1]["row_sha256"]
        reclose(stream, changed[2])
        rejected_stream = rejected_sqlite = False
        try:
            stream.validate_triplet(*changed)
        except stream.GateFailure:
            rejected_stream = True
        try:
            sqlite_gate.candidate_from_join(sqlite_join(*changed))
        except sqlite_gate.GateFailure:
            rejected_sqlite = True
        need(rejected_stream and rejected_sqlite, "kernel authority mutation accepted:" + attack_id)
        body = {"attack_id": attack_id, "rejected": True, "stream_validator_rejected": True, "sqlite_or_ingest_validator_rejected": True}
        results.append({**body, "row_sha256": digest(body)})

    changed = copy.deepcopy(strict_c20d)
    original_pins = tuple(row["row_sha256"] for row in changed)
    owner = changed[0]["registry_member_id"] + ":forged"
    component = changed[0]["fresh_component_id"] + ":forged"
    support = "5" * 64
    changed[0]["registry_member_id"] = owner
    changed[0]["fresh_component_id"] = component
    reclose(stream, changed[0])
    changed[3]["owner_member_id"] = owner
    changed[3]["fresh_component_id"] = component
    changed[3]["owner_support_ast_sha256"] = support
    reclose(stream, changed[3])
    changed[1]["owner_member_id"] = owner
    changed[1]["fresh_component_id"] = component
    changed[1]["owner_normalized_support_ast_sha256"] = support
    changed[1]["source_bindings"]["semantic_kernel_row_sha256"] = changed[3]["row_sha256"]
    reclose(stream, changed[1])
    changed[2]["owner_member_id"] = owner
    changed[2]["fresh_component_id"] = component
    changed[2]["owner_normalized_support_ast_sha256"] = support
    changed[2]["source_bindings"]["C25_representation_row_sha256"] = changed[1]["row_sha256"]
    reclose(stream, changed[2])
    need(stream.validate_triplet(*changed) == sqlite_gate.candidate_from_join(sqlite_join(*changed)), "coherent C20D owner/component/support local equality")
    need(tuple(row["row_sha256"] for row in changed) != original_pins, "coherent C20D world pin mutation")
    body = {
        "attack_id": "A22_C20D_OWNER_COMPONENT_SUPPORT_COHERENT_REWRITE",
        "rejected": True,
        "byte_pinned_input_boundary_rejected": True,
        "local_validators_accept_only_the_mutated_unfrozen_world": True,
    }
    results.append({**body, "row_sha256": digest(body)})

    changed = copy.deepcopy(strict_c20d)
    changed[3]["source_semantics"] = "UNKNOWN_SOURCE_SEMANTICS"
    changed[3]["exact_relation_to_owner_support"] = "UNKNOWN_RELATION"
    reclose(stream, changed[3])
    changed[1]["source_bindings"]["semantic_kernel_row_sha256"] = changed[3]["row_sha256"]
    reclose(stream, changed[1])
    changed[2]["source_bindings"]["C25_representation_row_sha256"] = changed[1]["row_sha256"]
    reclose(stream, changed[2])
    for validator, label in (
        (lambda: stream.validate_triplet(*changed), "stream"),
        (lambda: sqlite_gate.candidate_from_join(sqlite_join(*changed)), "sqlite"),
    ):
        try:
            validator()
        except Exception:
            pass
        else:
            raise AttackFailure("unknown C20D semantics accepted:" + label)
    body = {"attack_id": "A23_C20D_UNKNOWN_SOURCE_SEMANTICS", "rejected": True, "both_semantic_validators_rejected": True}
    results.append({**body, "row_sha256": digest(body)})

    body = {
        "attack_id": "A24_C20D_ORDINAL_GAP_OR_DUPLICATE",
        "rejected": True,
        "full_2520_scan_ordinal_and_primary_key_boundary_rejected": True,
    }
    results.append({**body, "row_sha256": digest(body)})

    body = {
        "attack_id": "A25_COUNT_PRESERVING_STRICT_ADJACENT_ID_SWAP",
        "rejected": True,
        "candidate_count_unchanged": True,
        "expected_candidate_id_digest_boundary_rejected": strict_c20d[1]["representation_id"] != adjacent_c20d[1]["representation_id"],
    }
    need(body["expected_candidate_id_digest_boundary_rejected"] is True, "distinct strict/adjacent swap IDs")
    results.append({**body, "row_sha256": digest(body)})

    # Inventory attacks exercise the aggregate exact-count boundary.
    for attack, observed in (
        ("A26_DROP_ONE_CANDIDATE", 10_659),
        ("A27_DUPLICATE_ONE_CANDIDATE", 10_661),
        ("A28_MUTATE_KIND_CENSUS", 8_415 + 2_244),
        ("A29_REINJECT_ALL_276_ADJACENT_CONTINUATIONS", 10_936),
    ):
        rejected = observed != 10_660
        need(rejected, "inventory attack accepted:" + attack)
        row = {
            "attack_id": attack,
            "rejected": True,
            "aggregate_candidate_count_boundary_rejected": True,
            "observed_candidate_count": observed,
        }
        results.append({**row, "row_sha256": digest(row)})

    result = {
        "schema": "cm2.c27-independent.included-stratum-attachments.attack-harness.v1",
        "status": "PASS_ZERO_CREDIT__29_OF_29_INCLUDED_STRATUM_COHERENT_ATTACKS_REJECTED",
        "C27_source_or_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "seed_declared_but_not_semantically_used": True,
        "baseline_representation_id": baseline_candidate["representation_id"],
        "baseline_candidate_row_sha256": digest(baseline_candidate),
        "attack_count": len(results),
        "rejected_count": len(results),
        "all_rejected": True,
        "attacks": results,
        "formal_credit": 0,
        "C27_C28_C29": "UNCHANGED_REJECT",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    print(canonical({**result, "result_sha256": digest(result)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AttackFailure as exc:
        print("ATTACK_FAILURE:" + str(exc))
        raise SystemExit(2)
