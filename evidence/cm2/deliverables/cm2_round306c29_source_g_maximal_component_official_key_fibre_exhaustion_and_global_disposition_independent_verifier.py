#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c29_source_g_maximal_component_official_key_fibre_exhaustion_and_global_disposition"
COMPONENT_LEDGER = PREFIX + "_maximal_component_fibre_assignment_ledger.jsonl.gz"
FIBRE_LEDGER = PREFIX + "_official_key_fibre_exhaustion_ledger.jsonl.gz"
DISPOSITION_LEDGER = PREFIX + "_global_member_disposition_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"

C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger"
C28 = "cm2_round306c28_source_g_125616475670_cross_component_pair_block_routing_and_maximality"
C15_COMPONENT = C15 + "_component_census_ledger.jsonl.gz"
C25_MEMBER = C25 + "_member_ledger.jsonl.gz"
C25_REPRESENTATION = C25 + "_representation_ledger.jsonl.gz"
C28_BLOCK = C28 + "_member_home_block_census_ledger.jsonl.gz"
C28_ROUTE = C28 + "_cross_component_pair_route_shard_ledger.jsonl.gz"

SOURCES = (
    ("C15", C15, "a1eea2c41123d2ff7f7d3e1f35f1deabc5bae9d93b24f825b4831f6324c1e2c4", "99ad5fb9f2f940155effdcb24ac076824f6436f2d92a66bd6d9ed196d0ac8f71", (C15_COMPONENT,)),
    ("C25", C25, "8885eb09f4e0aef3107654996ef520cca3ce59f59fc5b5d8a1652d44f9bb9a81", "ad6b4ae09985f23fd0db00e79bee859014c23c6792aa732582e50aa39c745bef", (C25_MEMBER, C25_REPRESENTATION)),
    ("C28", C28, "59a6a16b83720fba38dece52ce6dbd1ea30509ee6e0c6f5bd071f83a41dc9250", "fe8ed1fd164e7892d83f41de2e06916e002338cde0f21e6c128b40671a5201cc", (C28_BLOCK, C28_ROUTE)),
)

MEMBERS = 502204
REPRESENTATIONS = 549616
COMPONENTS = 57876
KEYS = 124
INCIDENCES = 74400
FAMILIES = {"PRESERVED": 126468, "NON_GRAPH": 55604, "R2": 295336, "R292": 9404, "G2A": 5264, "G2B": 10128}
MULTIPLICITY = {"1": 41364, "2": 16508, "5": 4}
SUPPORT_KINDS = {"EXACT_MEMBER_SUPPORT_EQUALITY", "FINITE_CELL_UNION_MEMBER_SUPPORT_EQUALITY", "RELATION_BACKED_MEMBER_SUPPORT_EQUALITY", "EXACT_EMPTY_MEMBER_SUPPORT_EQUALITY"}


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def wire(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def reject_constant(value: str) -> None:
    raise Reject("constant:" + value)


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in output, "duplicate:" + key)
        output[key] = value
    return output


def parse(raw: bytes, label: str) -> Any:
    payload = raw[:-1] if raw.endswith(b"\n") else raw
    require(not payload.endswith(b"\n"), "trailing newlines:" + label)
    try:
        value = json.loads(payload.decode("ascii"), object_pairs_hook=unique, parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Reject("JSON:" + label) from error
    require(wire(value) == payload, "canonical:" + label)
    return value


def ledger(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as source:
        for ordinal, line in enumerate(source):
            require(line.endswith(b"\n"), "newline:" + path.name)
            value = parse(line[:-1], path.name + ":" + str(ordinal))
            require(type(value) is dict, "row type")
            body = dict(value)
            claimed = body.pop("row_sha256", None)
            require(type(claimed) is str and claimed == sha(body), "row closure:" + path.name + ":" + str(ordinal))
            yield value


def result(path: Path) -> tuple[dict[str, Any], str]:
    value = parse(path.read_bytes(), path.name)
    require(type(value) is dict, "result type")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    require(type(claimed) is str and claimed == sha(body), "result closure")
    return value, claimed


def manifest_entries(path: Path) -> dict[str, str]:
    output: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        fields = line.split(None, 1)
        require(len(fields) == 2 and len(fields[0]) == 64, "manifest line")
        name = Path(fields[1].strip()).name
        require(name == fields[1].strip() and name not in output, "manifest name")
        output[name] = fields[0]
    return output


def seal_sources() -> tuple[dict[str, str], list[dict[str, str]]]:
    objects: dict[str, str] = {}
    pins: list[dict[str, str]] = []
    for tag, base, manifest_pin, object_pin, ledgers in SOURCES:
        manifest_name = base + "_manifest.sha256"
        result_name = base + "_result.json"
        verification_name = base + "_verification.json"
        require(file_sha(ROOT / manifest_name) == manifest_pin, "manifest pin:" + tag)
        listed = manifest_entries(ROOT / manifest_name)
        for name in (*ledgers, result_name, verification_name):
            require(name in listed and file_sha(ROOT / name) == listed[name], "manifest member:" + tag + ":" + name)
        source_result, object_hash = result(ROOT / result_name)
        require(object_hash == object_pin and str(source_result.get("status", "")).startswith("PASS"), "source result:" + tag)
        verification = parse((ROOT / verification_name).read_bytes(), verification_name)
        require(str(verification.get("status", "")).startswith("PASS"), "source verification:" + tag)
        objects[tag] = object_hash
        pins.append({"filename": manifest_name, "sha256": manifest_pin})
        pins.extend({"filename": name, "sha256": listed[name]} for name in (*ledgers, result_name, verification_name))
    c25, _ = result(ROOT / (C25 + "_result.json"))
    c28, _ = result(ROOT / (C28 + "_result.json"))
    require(c25["global_credit"]["member_normalized_support_set_equality"] == MEMBERS, "C25 members")
    require(c25["global_credit"]["typed_representation_semantic_disposition"] == REPRESENTATIONS, "C25 representations")
    require(c28["formal_credit"]["B2"] == 1 and c28["formal_credit"]["maximality"] == 1, "C28 credits")
    require(c28["pair_route_census"]["new_legal_cross_component_pairs"] == 0 and c28["pair_route_census"]["unresolved_pairs"] == 0, "C28 closure")
    return objects, sorted(pins, key=lambda item: item["filename"])


def accumulator() -> dict[str, Any]:
    return {"count": 0, "key_counts": Counter(), "family_counts": Counter(), "identity_hash": hashlib.sha256(), "support_hash": hashlib.sha256()}


def reconstruct() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    by_component: dict[str, dict[str, Any]] = {}
    by_key: dict[str, dict[str, Any]] = {}
    seen: set[str] = set()
    family_total: Counter[str] = Counter()
    count = 0
    expected_credit = {"fresh_DSU_member_binding": 1, "member_normalized_support_set_equality": 1, "typed_global_support_ledger": 1, "typed_member_identity": 1}
    for ordinal, row in enumerate(ledger(ROOT / C25_MEMBER)):
        require(row["member_ordinal"] == ordinal, "member ordinal")
        require(row["support_semantic_kind"] in SUPPORT_KINDS and row["formal_credit"] == expected_credit, "support closure")
        identity = row["member_id"]
        component_id = row["fresh_component_id"]
        key_id = row["official_key_id"]
        family = row["coarse_family"]
        require(identity not in seen, "member duplicate")
        seen.add(identity)
        component = by_component.setdefault(component_id, accumulator())
        fibre = by_key.setdefault(key_id, {**accumulator(), "component_ids": set()})
        for value in (component, fibre):
            value["count"] += 1
            value["key_counts"][key_id] += 1
            value["family_counts"][family] += 1
            value["identity_hash"].update(identity.encode("ascii") + b"\n")
            value["support_hash"].update(bytes.fromhex(row["support_semantic_certificate_sha256"]))
        fibre["component_ids"].add(component_id)
        family_total[family] += 1
        count += 1
    require(count == MEMBERS and len(seen) == MEMBERS, "member exhaustion")
    require(len(by_component) == COMPONENTS and len(by_key) == KEYS, "component/key count")
    require(dict(family_total) == FAMILIES, "family count")

    source_components: list[dict[str, Any]] = []
    source_ids: set[str] = set()
    for ordinal, row in enumerate(ledger(ROOT / C15_COMPONENT)):
        require(row["component_ordinal"] == ordinal, "component ordinal")
        component_id = row["fresh_component_id"]
        require(component_id not in source_ids and component_id in by_component, "component source")
        require(row["member_count"] == by_component[component_id]["count"], "component size")
        source_ids.add(component_id)
        source_components.append(row)
    require(source_ids == set(by_component), "component source exhaustion")
    require(dict(Counter(str(len(value["key_counts"])) for value in by_component.values())) == MULTIPLICITY, "key multiplicity")
    require(sum(len(value["component_ids"]) for value in by_key.values()) == INCIDENCES, "incidences")
    return by_component, by_key, source_components, dict(family_total)


def closed(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": sha(body)}


def expected_component(source: dict[str, Any], components: dict[str, dict[str, Any]], objects: dict[str, str]) -> dict[str, Any]:
    component_id = source["fresh_component_id"]
    value = components[component_id]
    body = {
        "schema": "cm2.round306c29.source-g-maximal-component-fibre-assignment.v1.row.v1",
        "component_ordinal": source["component_ordinal"],
        "fresh_component_id": component_id,
        "member_count": value["count"],
        "base_root_count": source["base_root_count"],
        "official_key_count": len(value["key_counts"]),
        "official_key_member_census": dict(sorted(value["key_counts"].items())),
        "family_member_census": dict(sorted(value["family_counts"].items())),
        "member_id_sequence_sha256": value["identity_hash"].hexdigest(),
        "support_certificate_sequence_sha256": value["support_hash"].hexdigest(),
        "source_bindings": {"C15_component_row_sha256": source["row_sha256"], "C25_global_support_result_sha256": objects["C25"], "C28_B2_maximality_result_sha256": objects["C28"]},
        "maximality_disposition": "MAXIMAL_UNDER_CORRECTED_EXHAUSTIVE_TRANSITION_RELATION",
        "formal_credit": {"maximal_component_assignment": 1, "component_fibre_inventory": 1},
        "strict_nonpromotion": {"D02": 0, "D03": 0, "D04": 0, "CM2": 0},
    }
    return closed(body)


def expected_fibre(ordinal: int, key_id: str, value: dict[str, Any], component_hashes: dict[str, str], objects: dict[str, str]) -> dict[str, Any]:
    component_ids = sorted(value["component_ids"])
    row_sequence = hashlib.sha256()
    for component_id in component_ids:
        row_sequence.update(bytes.fromhex(component_hashes[component_id]))
    body = {
        "schema": "cm2.round306c29.source-g-official-key-fibre-exhaustion.v1.row.v1",
        "fibre_ordinal": ordinal,
        "official_key_id": key_id,
        "official_key_registry_ordinal": int(key_id.split(":", 2)[1]),
        "member_count": value["count"],
        "maximal_component_incidence_count": len(component_ids),
        "maximal_component_ids_sha256": sha(component_ids),
        "maximal_component_row_sequence_sha256": row_sequence.hexdigest(),
        "family_member_census": dict(sorted(value["family_counts"].items())),
        "member_id_sequence_sha256": value["identity_hash"].hexdigest(),
        "support_certificate_sequence_sha256": value["support_hash"].hexdigest(),
        "fibre_inventory_complete": True,
        "every_member_has_exact_normalized_support": True,
        "every_incident_component_is_C28_maximal": True,
        "global_transition_residual_count": 0,
        "global_member_disposition_count": value["count"],
        "source_bindings": {"C25_global_support_result_sha256": objects["C25"], "C28_B2_maximality_result_sha256": objects["C28"]},
        "formal_credit": {"official_key_fibre_exhaustion": 1, "global_member_dispositions": value["count"]},
        "strict_nonpromotion": {"D02": 0, "D03": 0, "D04": 0, "CM2": 0},
    }
    return closed(body)


def expected_disposition(ordinal: int, source: dict[str, Any], component_hashes: dict[str, str], fibre_hashes: dict[str, str], objects: dict[str, str]) -> dict[str, Any]:
    body = {
        "schema": "cm2.round306c29.source-g-global-member-disposition.v1.row.v1",
        "disposition_ordinal": ordinal,
        "member_id": source["member_id"],
        "official_key_id": source["official_key_id"],
        "fresh_component_id": source["fresh_component_id"],
        "coarse_family": source["coarse_family"],
        "normalized_support_ast_sha256": source["normalized_support_ast_sha256"],
        "support_semantic_certificate_sha256": source["support_semantic_certificate_sha256"],
        "global_disposition": "ASSIGNED_TO_C28_MAXIMAL_COMPONENT_IN_EXHAUSTED_OFFICIAL_KEY_FIBRE",
        "source_bindings": {"C25_member_row_sha256": source["row_sha256"], "C29_component_row_sha256": component_hashes[source["fresh_component_id"]], "C29_fibre_row_sha256": fibre_hashes[source["official_key_id"]], "C28_B2_maximality_result_sha256": objects["C28"]},
        "formal_credit": {"global_exact_key_member_disposition": 1, "member_support_consumed": 1, "maximal_component_consumed": 1, "official_key_fibre_consumed": 1},
        "strict_nonpromotion": {"D02": 0, "D03": 0, "D04": 0, "CM2": 0},
    }
    return closed(body)


def descriptor(path: Path, count: int, sequence: str, order: str) -> dict[str, Any]:
    return {"filename": path.name, "row_count": count, "size": path.stat().st_size, "sha256": file_sha(path), "row_sequence_sha256": sequence, "order": order}


def verify(candidate: Path) -> dict[str, Any]:
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated runtime")
    preliminary, _ = result(candidate / RESULT)
    require(preliminary.get("status") == "PASS_57876_MAXIMAL_COMPONENTS__124_OFFICIAL_KEY_FIBRES_EXHAUSTED__502204_GLOBAL_MEMBER_DISPOSITIONS_SEALED__D02_SOURCE_W_GATE_REMAINS_BLOCKED", "preflight status")
    require(preliminary.get("fibre_census") == {"required": KEYS, "exhausted": KEYS, "open": 0, "component_incidences": INCIDENCES}, "preflight fibres")
    require(preliminary.get("global_disposition_census") == {"corrected_typed_member_denominator": MEMBERS, "issued": MEMBERS, "missing": 0, "duplicate": 0, "orphan": 0}, "preflight dispositions")
    require(preliminary.get("formal_credit") == {"C25_global_support_consumed": 1, "C28_B2_maximality_consumed": 1, "maximal_component_assignments": COMPONENTS, "official_key_fibres_exhausted": KEYS, "global_member_dispositions": MEMBERS, "fibre": 1, "global_disposition": 1}, "preflight credit")
    require(preliminary.get("strict_nonpromotion") == {"D02": "BLOCKED_BY_252_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE", "D03": "UNAUTHORIZED", "D04": "NOT_MINTED", "Gate5_filled_field_slots": "10/18", "Gate5_complete_global_blocks": 0, "CM2": "NO-GO_FOR_CLAIM"}, "preflight boundary")

    objects, pins = seal_sources()
    components, keys, source_components, families = reconstruct()
    candidate_components = ledger(candidate / COMPONENT_LEDGER)
    component_sequence = hashlib.sha256()
    component_hashes: dict[str, str] = {}
    for source in source_components:
        actual = next(candidate_components, None)
        expected = expected_component(source, components, objects)
        require(actual is not None and actual == expected, "component reconstruction:" + str(source["component_ordinal"]))
        component_sequence.update(bytes.fromhex(actual["row_sha256"]))
        component_hashes[actual["fresh_component_id"]] = actual["row_sha256"]
    require(next(candidate_components, None) is None and len(component_hashes) == COMPONENTS, "component exhaustion")

    candidate_fibres = ledger(candidate / FIBRE_LEDGER)
    fibre_sequence = hashlib.sha256()
    fibre_hashes: dict[str, str] = {}
    for ordinal, key_id in enumerate(sorted(keys)):
        actual = next(candidate_fibres, None)
        expected = expected_fibre(ordinal, key_id, keys[key_id], component_hashes, objects)
        require(actual is not None and actual == expected, "fibre reconstruction:" + str(ordinal))
        fibre_sequence.update(bytes.fromhex(actual["row_sha256"]))
        fibre_hashes[key_id] = actual["row_sha256"]
    require(next(candidate_fibres, None) is None and len(fibre_hashes) == KEYS, "fibre exhaustion")

    candidate_dispositions = ledger(candidate / DISPOSITION_LEDGER)
    disposition_sequence = hashlib.sha256()
    disposition_count = 0
    for ordinal, source in enumerate(ledger(ROOT / C25_MEMBER)):
        actual = next(candidate_dispositions, None)
        expected = expected_disposition(ordinal, source, component_hashes, fibre_hashes, objects)
        require(actual is not None and actual == expected, "disposition reconstruction:" + str(ordinal))
        disposition_sequence.update(bytes.fromhex(actual["row_sha256"]))
        disposition_count += 1
    require(next(candidate_dispositions, None) is None and disposition_count == MEMBERS, "disposition exhaustion")

    component_descriptor = descriptor(candidate / COMPONENT_LEDGER, COMPONENTS, component_sequence.hexdigest(), "C15_COMPONENT_ORDINAL")
    fibre_descriptor = descriptor(candidate / FIBRE_LEDGER, KEYS, fibre_sequence.hexdigest(), "LEXICOGRAPHIC_OFFICIAL_KEY_ID")
    disposition_descriptor = descriptor(candidate / DISPOSITION_LEDGER, MEMBERS, disposition_sequence.hexdigest(), "C25_MEMBER_ORDINAL")
    theorem = {"kind": "CORRECTED_SOURCE_G_MAXIMAL_COMPONENT_FIBRE_AND_GLOBAL_DISPOSITION_THEOREM", "C25_exact_member_support_complete": True, "C25_representation_semantics_complete": True, "C28_B2_and_component_maximality_complete": True, "every_member_has_exactly_one_official_key": True, "every_member_has_exactly_one_C15_component": True, "every_C15_component_is_C28_maximal": True, "every_official_key_fibre_inventory_is_complete": True, "every_official_key_fibre_is_globally_exhausted": True, "every_member_has_exactly_one_global_disposition": True, "source_G_fibre_or_disposition_gap_count": 0}
    body = {
        "schema": "cm2.round306c29.source-g-maximal-component-official-key-fibre-exhaustion-and-global-disposition.v1",
        "status": "PASS_57876_MAXIMAL_COMPONENTS__124_OFFICIAL_KEY_FIBRES_EXHAUSTED__502204_GLOBAL_MEMBER_DISPOSITIONS_SEALED__D02_SOURCE_W_GATE_REMAINS_BLOCKED",
        "corrected_source_G_census": {"members": MEMBERS, "representations": REPRESENTATIONS, "maximal_components": COMPONENTS, "official_keys": KEYS, "component_key_incidences": INCIDENCES, "component_key_multiplicity_census": MULTIPLICITY, "family_member_census": families},
        "fibre_census": {"required": KEYS, "exhausted": KEYS, "open": 0, "component_incidences": INCIDENCES},
        "global_disposition_census": {"corrected_typed_member_denominator": MEMBERS, "issued": MEMBERS, "missing": 0, "duplicate": 0, "orphan": 0},
        "source_G_fibre_and_disposition_theorem": theorem,
        "source_G_fibre_and_disposition_theorem_sha256": sha(theorem),
        "ledgers": {"maximal_component_fibre_assignment": component_descriptor, "official_key_fibre_exhaustion": fibre_descriptor, "global_member_disposition": disposition_descriptor},
        "input_pins": pins,
        "formal_credit": {"C25_global_support_consumed": 1, "C28_B2_maximality_consumed": 1, "maximal_component_assignments": COMPONENTS, "official_key_fibres_exhausted": KEYS, "global_member_dispositions": MEMBERS, "fibre": 1, "global_disposition": 1},
        "strict_nonpromotion": {"D02": "BLOCKED_BY_252_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE", "D03": "UNAUTHORIZED", "D04": "NOT_MINTED", "Gate5_filled_field_slots": "10/18", "Gate5_complete_global_blocks": 0, "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": "CLOSE_SOURCE_W_198_MIXED_PLUS_54_COMPACT_Q_ORIGINS_WITH_FULL_3D_2D_1D_0D_PARTITION_THEN_REAUDIT_D02_D03_D04_GATE5_CM2",
    }
    expected_result = {**body, "result_sha256": sha(body)}
    actual_result, claimed = result(candidate / RESULT)
    require(actual_result == expected_result and claimed == expected_result["result_sha256"], "result reconstruction")
    return {"status": "PASS_INDEPENDENT_C29_57876_COMPONENTS_124_FIBRES_502204_DISPOSITIONS_RECONSTRUCTED__D02_BOUNDARY_PRESERVED", "result_sha256": claimed, "component_rows": COMPONENTS, "fibre_rows": KEYS, "disposition_rows": MEMBERS, "total_rows": COMPONENTS + KEYS + MEMBERS}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir")
    args = parser.parse_args()
    candidate = ROOT if args.candidate_dir is None else Path(args.candidate_dir).resolve()
    print(wire(verify(candidate)).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
