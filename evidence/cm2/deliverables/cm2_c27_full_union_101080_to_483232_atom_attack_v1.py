#!/usr/bin/env python3
"""Coherent row/aggregate mutation gate for the full-union atom join.

This verifier rebuilds selected rows from pinned primitive inputs.  It imports
neither the producer nor C27 FAMILIES and treats G2A only as a bound diagnostic
alias of the C24A G2B positive route.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Iterator

TERMINALS = (
    "SIGNED_BOUNDARY_FACES",
    "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS",
)


class Reject(RuntimeError):
    pass


def need(value: bool, message: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_row(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    row["row_sha256"] = object_sha(row)


def check_file(path: Path, expected: str, label: str) -> None:
    need(hashlib.sha256(path.read_bytes()).hexdigest() == expected, label + ":pin")


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"row:{ordinal}:newline")
            row = json.loads(line)
            need(canonical(row) == line[:-1], f"row:{ordinal}:canonical")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(claimed == object_sha(body), f"row:{ordinal}:closure")
            yield row


def source_key(text: str) -> tuple[str, str]:
    source, digest = text.split(":", 1)
    need(source in {"C19A", "C19B", "C19C", "C20A", "C22A", "C23A"},
         "representative source")
    need(len(digest) == 64, "representative digest")
    return source, digest


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in (
        "atoms", "union-ledger", "current-priority", "current-positive",
        "g2b-exact", "c15", "endpoint-authority", "join-ledger",
        "join-result",
    ):
        parser.add_argument("--" + name, type=Path, required=True)
        parser.add_argument("--" + name + "-sha256", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    for name in (
        "atoms", "union_ledger", "current_priority", "current_positive",
        "g2b_exact", "c15", "endpoint_authority", "join_ledger",
        "join_result",
    ):
        check_file(getattr(args, name), getattr(args, name + "_sha256"), name)

    c15 = {row["registry_member_id"]: row["fresh_component_id"] for row in rows(args.c15)}
    endpoint = {row["member_id"]: row for row in rows(args.endpoint_authority)}
    need(len(c15) == 502204 and len(endpoint) == 33344, "base authorities")

    atoms: dict[str, dict[str, Any]] = {}
    by_source: dict[tuple[str, str], str] = {}
    atoms_by_owner: dict[str, list[str]] = defaultdict(list)
    atom_order: list[str] = []
    for row in rows(args.atoms):
        atom_id = row["atom_id"]
        key = (row["source_kernel"], row["source_row_sha256"])
        need(atom_id not in atoms and key not in by_source, "atom uniqueness")
        atoms[atom_id] = row
        by_source[key] = atom_id
        atoms_by_owner[row["owner_member_id"]].append(atom_id)
        atom_order.append(atom_id)
    need(len(atoms) == 483232, "atom census")

    current = {row["row_sha256"]: row for row in rows(args.current_priority)}
    positive = {row["row_sha256"]: row for row in rows(args.current_positive)}
    g2b = {row["row_sha256"]: row for row in rows(args.g2b_exact)}
    need(len(current) == 91672 and len(positive) == 55532 and len(g2b) == 18800,
         "route input census")

    incidence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    coarse_positive_regression: tuple[str, dict[str, Any]] | None = None
    union_count = 0
    for union in rows(args.union_ledger):
        union_count += 1
        pair = tuple(union["pair_key"])
        terminal = union["assigned_terminal"]
        common = {
            "assigned_terminal": terminal,
            "pair_key": "|".join(pair),
            "source_authority": union["source_authority"],
            "union_route_row_sha256": union["row_sha256"],
        }
        if union["source_authority"] == "CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER":
            route = current[union["source_row_sha256"]]
            need((route["left_member_id"], route["right_member_id"]) == pair,
                 "current pair binding")
            if terminal == "POSITIVE_VOLUME_CARRIERS":
                proof = positive[route["positive_primitive_row_sha256"]]
                keys = [source_key(value) for value in proof["representative_atom_ids"]]
                need([key[0] for key in keys] == proof["representative_sources"],
                     "positive representative sources")
                atom_ids = [by_source[key] for key in keys]
                mode = "EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS"
                evidence = proof["row_sha256"]
            else:
                atom_ids = atoms_by_owner[pair[0]] + atoms_by_owner[pair[1]]
                mode = "MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE"
                evidence = route["row_sha256"]
        else:
            need(union["source_authority"] == "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER",
                 "C24 authority")
            proof = g2b[union["C24A_G2B_exact_row_sha256"]]
            need(terminal == "POSITIVE_VOLUME_CARRIERS" and
                 pair == (proof["c24_member_id"], proof["target_member_id"]),
                 "C24 terminal/pair")
            need(not atoms_by_owner[proof["c24_member_id"]], "C24 source excluded")
            atom_ids = [by_source[("C22A", proof["C22_target_row_sha256"])]]
            mode = "EXACT_C24A_G2B_C22_TARGET_ATOM"
            evidence = proof["row_sha256"]
        for atom_id in atom_ids:
            item = dict(common)
            item["atom_binding_mode"] = mode
            item["source_evidence_row_sha256"] = evidence
            incidence[atom_id].append(item)
        if (mode == "EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS" and
                coarse_positive_regression is None):
            for owner in pair:
                nonrepresentatives = [
                    atom_id for atom_id in atoms_by_owner[owner]
                    if atom_id not in atom_ids
                ]
                if nonrepresentatives:
                    forged = dict(common)
                    forged["atom_binding_mode"] = mode
                    forged["source_evidence_row_sha256"] = evidence
                    coarse_positive_regression = (nonrepresentatives[0], forged)
                    break
    need(union_count == 101080, "union census")
    for values in incidence.values():
        values.sort(key=lambda row: (
            row["pair_key"], row["source_authority"], row["atom_binding_mode"],
            row["union_route_row_sha256"],
        ))

    def expected(atom: dict[str, Any]) -> dict[str, Any]:
        atom_id = atom["atom_id"]
        owner = atom["owner_member_id"]
        if atom["source_kernel"] == "C19C":
            authority = endpoint[owner]
            bits_doc = authority["endpoint_inclusion_bits"]
            bits = [
                bits_doc["t_lower_closed"], bits_doc["t_upper_closed"],
                bits_doc["p_lower_closed"], bits_doc["p_upper_closed"],
                bits_doc["s_lower_closed"], bits_doc["s_upper_closed"],
            ]
            endpoint_binding = {
                "authority_row_sha256": authority["row_sha256"],
                "authority_rule": authority["authority_rule"],
                "source": "C19C_ENDPOINT_OWNERSHIP_V3",
            }
        else:
            bits = atom["endpoint_inclusion_flags_lower_upper_t_p_s"]
            endpoint_binding = {
                "authority_row_sha256": atom["row_sha256"],
                "authority_rule": "PRIMITIVE_OPEN_SUPPORT",
                "source": "FROZEN_PRIMITIVE_ATOM_ROW",
            }
        incident = incidence.get(atom_id, [])
        terminal_counts = Counter(row["assigned_terminal"] for row in incident)
        terminal_set = [terminal for terminal in TERMINALS if terminal_counts[terminal]]
        disposition = (
            "INCIDENT_TO_FULL_101080_UNION_PAIR_ROUTES" if incident else
            "EXACT_COMPLEMENT__ATOM_ABSENT_FROM_ALL_FULL_UNION_ROUTE_INCIDENCES"
        )
        output = {
            "atom_id": atom_id,
            "atom_source_kernel": atom["source_kernel"],
            "atom_source_row_sha256": atom["source_row_sha256"],
            "candidate_disposition": disposition,
            "candidate_incidence_count": len(incident),
            "current_C15_component": c15[owner],
            "effective_endpoint_inclusion_flags_lower_upper_t_p_s": bits,
            "endpoint_authority_binding": endpoint_binding,
            "formal_credit": 0,
            "incident_union_pair_routes": incident,
            "owner_member_id": owner,
            "pair_routes_each_have_unique_20_terminal_ownership": True,
            "schema": "cm2.c27-independent.full-union-101080-on-483232.atom-incidence-complement.row.v2",
            "terminal_incidence_census": {
                terminal: terminal_counts[terminal] for terminal in TERMINALS
            },
            "terminal_incidence_set": terminal_set,
        }
        close_row(output)
        return output

    samples: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    with gzip.open(args.join_ledger, "rb") as stream:
        for atom_id, line in zip(atom_order, stream):
            observed = json.loads(line)
            atom = atoms[atom_id]
            need(observed == expected(atom), "baseline lockstep sample")
            routes = observed["incident_union_pair_routes"]
            if not routes:
                samples.setdefault("complement", (atom, observed))
            if atom["source_kernel"] == "C19C":
                samples.setdefault("c19c", (atom, observed))
            if any(route["atom_binding_mode"] == "EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS"
                   for route in routes):
                samples.setdefault("current_positive", (atom, observed))
            if any(route["atom_binding_mode"] == "MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE"
                   for route in routes):
                samples.setdefault("boundary", (atom, observed))
            if any(route["atom_binding_mode"] == "EXACT_C24A_G2B_C22_TARGET_ATOM"
                   for route in routes):
                samples.setdefault("c24", (atom, observed))
            if len(observed["terminal_incidence_set"]) > 1:
                samples.setdefault("multi", (atom, observed))
            if (coarse_positive_regression is not None and
                    atom_id == coarse_positive_regression[0]):
                samples.setdefault("coarse_nonrepresentative", (atom, observed))
            if len(samples) == 7:
                break
    need(len(samples) == 7 and coarse_positive_regression is not None,
         "attack sample classes including coarse-positive regression")

    def validate(atom: dict[str, Any], row: dict[str, Any]) -> None:
        need(row == expected(atom), "independent exact row semantics")

    def recalc(row: dict[str, Any]) -> None:
        routes = row["incident_union_pair_routes"]
        counts = Counter(route["assigned_terminal"] for route in routes)
        row["candidate_incidence_count"] = len(routes)
        row["terminal_incidence_census"] = {
            terminal: counts[terminal] for terminal in TERMINALS
        }
        row["terminal_incidence_set"] = [
            terminal for terminal in TERMINALS if counts[terminal]
        ]
        row["candidate_disposition"] = (
            "INCIDENT_TO_FULL_101080_UNION_PAIR_ROUTES" if routes else
            "EXACT_COMPLEMENT__ATOM_ABSENT_FROM_ALL_FULL_UNION_ROUTE_INCIDENCES"
        )
        close_row(row)

    def route_by_mode(row: dict[str, Any], mode: str) -> dict[str, Any]:
        matches = [route for route in row["incident_union_pair_routes"]
                   if route["atom_binding_mode"] == mode]
        need(bool(matches), "attack route mode:" + mode)
        return matches[0]

    def remove_route_by_mode(row: dict[str, Any], mode: str) -> None:
        row["incident_union_pair_routes"].remove(route_by_mode(row, mode))

    def duplicate_route_by_mode(row: dict[str, Any], mode: str) -> None:
        row["incident_union_pair_routes"].append(
            copy.deepcopy(route_by_mode(row, mode)))

    cases: list[tuple[str, str, Callable[[dict[str, Any]], None], bool]] = []

    def add(name: str, sample: str, mutation: Callable[[dict[str, Any]], None],
            derived: bool = False) -> None:
        cases.append((name, sample, mutation, derived))

    add("atom_id_flip", "complement", lambda row: row.__setitem__("atom_id", "forged"))
    add("owner_flip", "complement", lambda row: row.__setitem__("owner_member_id", "forged"))
    add("kernel_flip", "complement", lambda row: row.__setitem__("atom_source_kernel", "C19C"))
    add("source_row_flip", "complement", lambda row: row.__setitem__("atom_source_row_sha256", "0" * 64))
    add("C15_component_flip", "complement", lambda row: row.__setitem__("current_C15_component", "forged"))
    add("complement_inject_forged_incidence", "complement", lambda row: row["incident_union_pair_routes"].append({
        "assigned_terminal": "POSITIVE_VOLUME_CARRIERS", "pair_key": "forged|pair",
        "source_authority": "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER",
        "union_route_row_sha256": "0" * 64,
        "atom_binding_mode": "EXACT_C24A_G2B_C22_TARGET_ATOM",
        "source_evidence_row_sha256": "0" * 64,
    }), True)
    add("endpoint_bit_flip", "c19c", lambda row: row["effective_endpoint_inclusion_flags_lower_upper_t_p_s"].__setitem__(0, not row["effective_endpoint_inclusion_flags_lower_upper_t_p_s"][0]))
    add("endpoint_authority_hash_flip", "c19c", lambda row: row["endpoint_authority_binding"].__setitem__("authority_row_sha256", "0" * 64))
    add("endpoint_source_flip", "c19c", lambda row: row["endpoint_authority_binding"].__setitem__("source", "FROZEN_PRIMITIVE_ATOM_ROW"))
    add("positive_binding_mode_flip", "current_positive", lambda row: route_by_mode(row, "EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS").__setitem__("atom_binding_mode", "MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE"), True)
    add("positive_evidence_flip", "current_positive", lambda row: route_by_mode(row, "EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS").__setitem__("source_evidence_row_sha256", "0" * 64), True)
    add("positive_pair_key_flip", "current_positive", lambda row: route_by_mode(row, "EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS").__setitem__("pair_key", "forged|pair"), True)
    add("positive_route_hash_flip", "current_positive", lambda row: route_by_mode(row, "EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS").__setitem__("union_route_row_sha256", "0" * 64), True)
    add("positive_coarse_owner_fanout_regression", "coarse_nonrepresentative",
        lambda row: row["incident_union_pair_routes"].append(
            copy.deepcopy(coarse_positive_regression[1])), True)
    add("boundary_route_drop", "boundary", lambda row: remove_route_by_mode(row, "MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE"), True)
    add("boundary_route_duplicate", "boundary", lambda row: duplicate_route_by_mode(row, "MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE"), True)
    add("boundary_binding_mode_flip", "boundary", lambda row: route_by_mode(row, "MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE").__setitem__("atom_binding_mode", "EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS"), True)
    add("boundary_authority_flip", "boundary", lambda row: route_by_mode(row, "MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE").__setitem__("source_authority", "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER"), True)
    add("C24_terminal_flip", "c24", lambda row: route_by_mode(row, "EXACT_C24A_G2B_C22_TARGET_ATOM").__setitem__("assigned_terminal", "SIGNED_BOUNDARY_FACES"), True)
    add("C24_binding_mode_flip", "c24", lambda row: route_by_mode(row, "EXACT_C24A_G2B_C22_TARGET_ATOM").__setitem__("atom_binding_mode", "MEMBER_SUPPORT_UNION_BOUNDARY_FACE_INCIDENCE"), True)
    add("C24_source_authority_flip", "c24", lambda row: route_by_mode(row, "EXACT_C24A_G2B_C22_TARGET_ATOM").__setitem__("source_authority", "CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER"), True)
    add("C24_evidence_flip", "c24", lambda row: route_by_mode(row, "EXACT_C24A_G2B_C22_TARGET_ATOM").__setitem__("source_evidence_row_sha256", "0" * 64), True)
    add("C24_pair_key_flip", "c24", lambda row: route_by_mode(row, "EXACT_C24A_G2B_C22_TARGET_ATOM").__setitem__("pair_key", "forged|pair"), True)
    add("C24_route_hash_flip", "c24", lambda row: route_by_mode(row, "EXACT_C24A_G2B_C22_TARGET_ATOM").__setitem__("union_route_row_sha256", "0" * 64), True)
    add("G2A_alias_counted_as_extra_route", "c24", lambda row: duplicate_route_by_mode(row, "EXACT_C24A_G2B_C22_TARGET_ATOM"), True)
    add("multi_terminal_set_drop", "multi", lambda row: row["terminal_incidence_set"].pop())
    add("multi_terminal_census_flip", "multi", lambda row: row["terminal_incidence_census"].__setitem__("SIGNED_BOUNDARY_FACES", 999))
    add("incidence_count_flip", "c24", lambda row: row.__setitem__("candidate_incidence_count", row["candidate_incidence_count"] + 1))
    add("unique_owner_flag_flip", "c24", lambda row: row.__setitem__("pair_routes_each_have_unique_20_terminal_ownership", False))
    add("formal_credit_flip", "c24", lambda row: row.__setitem__("formal_credit", 1))
    add("schema_flip", "c24", lambda row: row.__setitem__("schema", row["schema"] + ".forged"))
    add("row_closure_flip", "c24", lambda row: row.__setitem__("row_sha256", "0" * 64))

    outcomes: list[dict[str, Any]] = []
    for ordinal, (name, sample_name, mutation, derived) in enumerate(cases):
        atom, baseline = samples[sample_name]
        attacked = copy.deepcopy(baseline)
        mutation(attacked)
        if derived:
            recalc(attacked)
        elif name != "row_closure_flip":
            close_row(attacked)
        try:
            validate(atom, attacked)
        except Reject as error:
            reason = str(error)
        else:
            raise RuntimeError("accepted row attack:" + name)
        outcome = {
            "attack": name,
            "ordinal": ordinal,
            "rejected": True,
            "reason": reason,
            "schema": "cm2.c27-independent.full-union-atom-join.attack-row.v1",
        }
        close_row(outcome)
        outcomes.append(outcome)

    result = json.loads(args.join_result.read_bytes())
    body = dict(result)
    claimed = body.pop("result_sha256", None)
    need(claimed == object_sha(body), "baseline result closure")

    aggregate: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("result_pair_count_flip", lambda doc: doc["pair_union"].__setitem__("pairs", 101079)),
        ("result_positive_count_flip", lambda doc: doc["pair_union"]["by_terminal"].__setitem__("POSITIVE_VOLUME_CARRIERS", 64939)),
        ("result_G2A_alias_count_flip", lambda doc: doc["pair_union"].__setitem__("G2A_alias_independent_candidate_count", 1)),
        ("result_G2B_owner_flip", lambda doc: doc["pair_union"].__setitem__("G2B_20_terminal_owner", "SAME_CHART_RELATIVE_CELLS")),
        ("result_G2B_same_chart_flip", lambda doc: doc["pair_union"].__setitem__("G2B_assigned_to_SAME_CHART_RELATIVE_CELLS", True)),
        ("result_incident_flip", lambda doc: doc["atom_denominator"].__setitem__("incident_atoms", 62767)),
        ("result_complement_flip", lambda doc: doc["atom_denominator"].__setitem__("exact_complement_atoms", 420465)),
        ("result_expanded_flip", lambda doc: doc["atom_denominator"].__setitem__("expanded_atom_route_incidences", 206631)),
        ("result_coarse_positive_fanout_plus_184", lambda doc: doc["atom_denominator"].__setitem__("expanded_atom_route_incidences", 206816)),
        ("result_coarse_positive_terminal_set_regression", lambda doc: (
            doc["atom_denominator"]["terminal_set_atom_census"].__setitem__(
                "SIGNED_BOUNDARY_FACES|COMPLETE_BOUNDARY_FACES", 3612),
            doc["atom_denominator"]["terminal_set_atom_census"].__setitem__(
                "SIGNED_BOUNDARY_FACES|COMPLETE_BOUNDARY_FACES|POSITIVE_VOLUME_CARRIERS", 252),
        )),
        ("result_remove_G2B_528_new_incident_atoms", lambda doc: (
            doc["atom_denominator"].__setitem__("incident_atoms", 62240),
            doc["atom_denominator"].__setitem__("exact_complement_atoms", 420992),
            doc["atom_denominator"].__setitem__("expanded_atom_route_incidences", 197224),
            doc["atom_denominator"]["terminal_set_atom_census"].__setitem__(
                "POSITIVE_VOLUME_CARRIERS", 50720),
        )),
        ("result_positive_binding_flip", lambda doc: doc["binding_census"].__setitem__("EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS", 111063)),
        ("result_G2B_binding_flip", lambda doc: doc["binding_census"].__setitem__("EXACT_C24A_G2B_C22_TARGET_ATOM", 9407)),
        ("result_C24_source_injection", lambda doc: doc["C24A_scope"].__setitem__("C24A_source_rows_added_to_atom_denominator", 1)),
        ("result_C24_target_atom_flip", lambda doc: doc["C24A_scope"].__setitem__("distinct_exact_C22_target_atoms", 1487)),
        ("result_endpoint_flip", lambda doc: doc.__setitem__("C19C_endpoint_v3_rows", 33343)),
        ("result_output_hash_flip", lambda doc: doc["output"].__setitem__("file_sha256", "0" * 64)),
        ("result_formal_credit_flip", lambda doc: doc.__setitem__("formal_credit", 1)),
        ("result_manifest_promotion", lambda doc: doc.__setitem__("manifest_authorized", True)),
        ("result_C27_promotion", lambda doc: doc.__setitem__("C27_C28_C29", "PASS")),
        ("result_Source_W_promotion", lambda doc: doc.__setitem__("Source_W_formal_remainder", 78)),
        ("result_CM2_promotion", lambda doc: doc.__setitem__("CM2", "GO")),
    ]

    def exact_aggregate(doc: dict[str, Any]) -> bool:
        return (
            doc["pair_union"]["pairs"] == 101080 and
            doc["pair_union"]["by_terminal"]["POSITIVE_VOLUME_CARRIERS"] == 64940 and
            doc["pair_union"]["G2A_alias_independent_candidate_count"] == 0 and
            doc["pair_union"]["G2B_20_terminal_owner"] == "POSITIVE_VOLUME_CARRIERS" and
            doc["pair_union"]["G2B_assigned_to_SAME_CHART_RELATIVE_CELLS"] is False and
            doc["atom_denominator"]["incident_atoms"] == 62768 and
            doc["atom_denominator"]["exact_complement_atoms"] == 420464 and
            doc["atom_denominator"]["expanded_atom_route_incidences"] == 206632 and
            doc["atom_denominator"]["multi_terminal_incident_atoms"] == 3896 and
            doc["atom_denominator"]["terminal_set_atom_census"][
                "SIGNED_BOUNDARY_FACES|COMPLETE_BOUNDARY_FACES"] == 3756 and
            doc["atom_denominator"]["terminal_set_atom_census"][
                "SIGNED_BOUNDARY_FACES|COMPLETE_BOUNDARY_FACES|POSITIVE_VOLUME_CARRIERS"] == 108 and
            doc["atom_denominator"]["terminal_set_atom_census"][
                "COMPLETE_BOUNDARY_FACES|POSITIVE_VOLUME_CARRIERS"] == 32 and
            doc["atom_denominator"]["terminal_set_atom_census"][
                "POSITIVE_VOLUME_CARRIERS"] == 51248 and
            doc["binding_census"]["EXACT_UNIQUE_POSITIVE_VOLUME_ATOM_WITNESS"] == 111064 and
            doc["binding_census"]["EXACT_C24A_G2B_C22_TARGET_ATOM"] == 9408 and
            doc["C24A_scope"]["C24A_source_rows_added_to_atom_denominator"] == 0 and
            doc["C24A_scope"]["distinct_exact_C22_target_atoms"] == 1488 and
            doc["C19C_endpoint_v3_rows"] == 33344 and
            doc["output"]["file_sha256"] == args.join_ledger_sha256 and
            doc["formal_credit"] == 0 and doc["manifest_authorized"] is False and
            doc["C27_C28_C29"] == "FULL_REBUILD_REQUIRED" and
            doc["Source_W_formal_remainder"] == 80 and doc["CM2"] == "NO-GO_FOR_CLAIM"
        )

    need(exact_aggregate(result), "baseline aggregate contract")
    for name, mutation in aggregate:
        attacked = copy.deepcopy(result)
        mutation(attacked)
        attacked.pop("result_sha256", None)
        attacked["result_sha256"] = object_sha(attacked)
        need(not exact_aggregate(attacked), "aggregate attack rejected")
        outcome = {
            "attack": name,
            "ordinal": len(outcomes),
            "rejected": True,
            "reason": "aggregate exact contract",
            "schema": "cm2.c27-independent.full-union-atom-join.attack-row.v1",
        }
        close_row(outcome)
        outcomes.append(outcome)

    output = {
        "schema": "cm2.c27-independent.full-union-101080-on-483232.atom-join.attacks.v1",
        "status": "PASS_ALL_COHERENT_FULL_UNION_ATOM_JOIN_ATTACKS_REJECTED__ZERO_CREDIT",
        "attack_count": len(outcomes),
        "rejected_count": len(outcomes),
        "accepted_count": 0,
        "formal_credit": 0,
        "manifest_authorized": False,
        "C27_C28_C29": "FULL_REBUILD_REQUIRED",
        "Source_W_formal_remainder": 80,
        "CM2": "NO-GO_FOR_CLAIM",
        "attacks": outcomes,
    }
    output["result_sha256"] = object_sha(output)
    args.out.parent.mkdir(parents=True, exist_ok=False)
    args.out.write_bytes(canonical(output) + b"\n")
    print(canonical({
        "rejected": len(outcomes),
        "result_sha256": output["result_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
