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
OFFICIAL_KEYS = 124
COMPONENT_KEY_INCIDENCES = 74400
FAMILY_COUNTS = {"PRESERVED": 126468, "NON_GRAPH": 55604, "R2": 295336, "R292": 9404, "G2A": 5264, "G2B": 10128}
COMPONENT_KEY_MULTIPLICITY = {"1": 41364, "2": 16508, "5": 4}


class Failure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1 << 20):
            state.update(chunk)
    return state.hexdigest()


def bad_constant(value: str) -> None:
    raise Failure("constant:" + value)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate:" + key)
        result[key] = value
    return result


def decode(raw: bytes, label: str) -> Any:
    payload = raw[:-1] if raw.endswith(b"\n") else raw
    need(not payload.endswith(b"\n"), "trailing newlines:" + label)
    try:
        value = json.loads(payload.decode("ascii"), object_pairs_hook=unique_object, parse_constant=bad_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Failure("JSON:" + label) from error
    need(canonical(value) == payload, "canonical:" + label)
    return value


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as source:
        for ordinal, line in enumerate(source):
            need(line.endswith(b"\n"), "newline:" + path.name)
            value = decode(line[:-1], path.name + ":" + str(ordinal))
            need(type(value) is dict, "row object:" + path.name)
            body = dict(value)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == digest(body), "row closure:" + path.name + ":" + str(ordinal))
            yield value


def result_object(path: Path) -> tuple[dict[str, Any], str]:
    value = decode(path.read_bytes(), path.name)
    need(type(value) is dict, "result object")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == digest(body), "result closure:" + path.name)
    return value, claimed


def manifest(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        fields = line.split(None, 1)
        need(len(fields) == 2 and len(fields[0]) == 64, "manifest line")
        name = Path(fields[1].strip()).name
        need(name == fields[1].strip() and name not in entries, "manifest name")
        entries[name] = fields[0]
    return entries


def validate_sources() -> tuple[dict[str, str], list[dict[str, str]]]:
    objects: dict[str, str] = {}
    pins: list[dict[str, str]] = []
    for tag, base, manifest_pin, object_pin, ledgers in SOURCES:
        manifest_name = base + "_manifest.sha256"
        result_name = base + "_result.json"
        verification_name = base + "_verification.json"
        need(file_hash(ROOT / manifest_name) == manifest_pin, "manifest pin:" + tag)
        entries = manifest(ROOT / manifest_name)
        for name in (*ledgers, result_name, verification_name):
            need(name in entries and file_hash(ROOT / name) == entries[name], "manifest member:" + tag + ":" + name)
        source_result, object_hash = result_object(ROOT / result_name)
        need(object_hash == object_pin and str(source_result.get("status", "")).startswith("PASS"), "result pin:" + tag)
        verification = decode((ROOT / verification_name).read_bytes(), verification_name)
        need(str(verification.get("status", "")).startswith("PASS"), "verification pin:" + tag)
        objects[tag] = object_hash
        pins.append({"filename": manifest_name, "sha256": manifest_pin})
        pins.extend({"filename": name, "sha256": entries[name]} for name in (*ledgers, result_name, verification_name))
    c25_result, _ = result_object(ROOT / (C25 + "_result.json"))
    c28_result, _ = result_object(ROOT / (C28 + "_result.json"))
    need(c25_result["global_credit"]["member_normalized_support_set_equality"] == MEMBERS, "C25 member support")
    need(c25_result["global_credit"]["typed_representation_semantic_disposition"] == REPRESENTATIONS, "C25 representations")
    need(c28_result["formal_credit"]["B2"] == 1 and c28_result["formal_credit"]["maximality"] == 1, "C28 B2/maximality")
    need(c28_result["pair_route_census"]["unresolved_pairs"] == 0 and c28_result["pair_route_census"]["new_legal_cross_component_pairs"] == 0, "C28 pair closure")
    return objects, sorted(pins, key=lambda item: item["filename"])


def new_accumulator() -> dict[str, Any]:
    return {"members": 0, "keys": Counter(), "families": Counter(), "member_ids": hashlib.sha256(), "supports": hashlib.sha256()}


def reconstruct() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    components: dict[str, dict[str, Any]] = {}
    keys: dict[str, dict[str, Any]] = {}
    identities: set[str] = set()
    global_families: Counter[str] = Counter()
    member_rows = 0
    for ordinal, row in enumerate(rows(ROOT / C25_MEMBER)):
        need(row["member_ordinal"] == ordinal, "member ordinal")
        need(row["support_semantic_kind"] in {"EXACT_MEMBER_SUPPORT_EQUALITY", "FINITE_CELL_UNION_MEMBER_SUPPORT_EQUALITY", "RELATION_BACKED_MEMBER_SUPPORT_EQUALITY", "EXACT_EMPTY_MEMBER_SUPPORT_EQUALITY"}, "member support kind")
        need(row["formal_credit"] == {"fresh_DSU_member_binding": 1, "member_normalized_support_set_equality": 1, "typed_global_support_ledger": 1, "typed_member_identity": 1}, "member support credit")
        member_id = row["member_id"]
        component_id = row["fresh_component_id"]
        official_key = row["official_key_id"]
        family = row["coarse_family"]
        need(member_id not in identities, "duplicate member")
        identities.add(member_id)
        component = components.setdefault(component_id, new_accumulator())
        fibre = keys.setdefault(official_key, {**new_accumulator(), "components": set()})
        for accumulator in (component, fibre):
            accumulator["members"] += 1
            accumulator["keys"][official_key] += 1
            accumulator["families"][family] += 1
            accumulator["member_ids"].update(member_id.encode("ascii") + b"\n")
            accumulator["supports"].update(bytes.fromhex(row["support_semantic_certificate_sha256"]))
        fibre["components"].add(component_id)
        global_families[family] += 1
        member_rows += 1
    need(member_rows == MEMBERS and len(identities) == MEMBERS, "member exhaustion")
    need(len(components) == COMPONENTS and len(keys) == OFFICIAL_KEYS, "component/key census")
    need(dict(global_families) == FAMILY_COUNTS, "family census")

    component_source_rows: list[dict[str, Any]] = []
    source_component_ids: set[str] = set()
    for ordinal, row in enumerate(rows(ROOT / C15_COMPONENT)):
        need(row["component_ordinal"] == ordinal, "component ordinal")
        component_id = row["fresh_component_id"]
        need(component_id not in source_component_ids and component_id in components, "component source set")
        need(row["member_count"] == components[component_id]["members"], "component member count")
        source_component_ids.add(component_id)
        component_source_rows.append(row)
    need(len(source_component_ids) == COMPONENTS and source_component_ids == set(components), "component source exhaustion")
    multiplicity = Counter(str(len(value["keys"])) for value in components.values())
    need(dict(multiplicity) == COMPONENT_KEY_MULTIPLICITY, "component key multiplicity")
    incidences = sum(len(value["components"]) for value in keys.values())
    need(incidences == COMPONENT_KEY_INCIDENCES, "component key incidences")
    return components, keys, component_source_rows, dict(global_families)


def close(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def write_ledger(path: Path, source: Iterator[dict[str, Any]], key_field: str | None = None) -> tuple[int, str, dict[str, str]]:
    count = 0
    sequence = hashlib.sha256()
    row_hashes: dict[str, str] = {}
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as output:
            for row in source:
                output.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
                if key_field is not None:
                    key = row[key_field]
                    need(key not in row_hashes, "duplicate output key:" + str(key))
                    row_hashes[key] = row["row_sha256"]
                count += 1
    return count, sequence.hexdigest(), row_hashes


def component_rows(components: dict[str, dict[str, Any]], source_rows: list[dict[str, Any]], objects: dict[str, str]) -> Iterator[dict[str, Any]]:
    for source in source_rows:
        component_id = source["fresh_component_id"]
        value = components[component_id]
        body = {
            "schema": "cm2.round306c29.source-g-maximal-component-fibre-assignment.v1.row.v1",
            "component_ordinal": source["component_ordinal"],
            "fresh_component_id": component_id,
            "member_count": value["members"],
            "base_root_count": source["base_root_count"],
            "official_key_count": len(value["keys"]),
            "official_key_member_census": dict(sorted(value["keys"].items())),
            "family_member_census": dict(sorted(value["families"].items())),
            "member_id_sequence_sha256": value["member_ids"].hexdigest(),
            "support_certificate_sequence_sha256": value["supports"].hexdigest(),
            "source_bindings": {"C15_component_row_sha256": source["row_sha256"], "C25_global_support_result_sha256": objects["C25"], "C28_B2_maximality_result_sha256": objects["C28"]},
            "maximality_disposition": "MAXIMAL_UNDER_CORRECTED_EXHAUSTIVE_TRANSITION_RELATION",
            "formal_credit": {"maximal_component_assignment": 1, "component_fibre_inventory": 1},
            "strict_nonpromotion": {"D02": 0, "D03": 0, "D04": 0, "CM2": 0},
        }
        yield close(body)


def fibre_rows(keys: dict[str, dict[str, Any]], component_hashes: dict[str, str], objects: dict[str, str]) -> Iterator[dict[str, Any]]:
    for ordinal, official_key in enumerate(sorted(keys)):
        value = keys[official_key]
        component_ids = sorted(value["components"])
        component_rows_sha256 = hashlib.sha256()
        for component_id in component_ids:
            component_rows_sha256.update(bytes.fromhex(component_hashes[component_id]))
        body = {
            "schema": "cm2.round306c29.source-g-official-key-fibre-exhaustion.v1.row.v1",
            "fibre_ordinal": ordinal,
            "official_key_id": official_key,
            "official_key_registry_ordinal": int(official_key.split(":", 2)[1]),
            "member_count": value["members"],
            "maximal_component_incidence_count": len(component_ids),
            "maximal_component_ids_sha256": digest(component_ids),
            "maximal_component_row_sequence_sha256": component_rows_sha256.hexdigest(),
            "family_member_census": dict(sorted(value["families"].items())),
            "member_id_sequence_sha256": value["member_ids"].hexdigest(),
            "support_certificate_sequence_sha256": value["supports"].hexdigest(),
            "fibre_inventory_complete": True,
            "every_member_has_exact_normalized_support": True,
            "every_incident_component_is_C28_maximal": True,
            "global_transition_residual_count": 0,
            "global_member_disposition_count": value["members"],
            "source_bindings": {"C25_global_support_result_sha256": objects["C25"], "C28_B2_maximality_result_sha256": objects["C28"]},
            "formal_credit": {"official_key_fibre_exhaustion": 1, "global_member_dispositions": value["members"]},
            "strict_nonpromotion": {"D02": 0, "D03": 0, "D04": 0, "CM2": 0},
        }
        yield close(body)


def disposition_rows(component_hashes: dict[str, str], fibre_hashes: dict[str, str], objects: dict[str, str]) -> Iterator[dict[str, Any]]:
    for ordinal, source in enumerate(rows(ROOT / C25_MEMBER)):
        need(source["member_ordinal"] == ordinal, "disposition source ordinal")
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
        yield close(body)


def descriptor(path: Path, count: int, sequence: str, order: str) -> dict[str, Any]:
    return {"filename": path.name, "row_count": count, "size": path.stat().st_size, "sha256": file_hash(path), "row_sequence_sha256": sequence, "order": order}


def build(candidate: Path) -> dict[str, Any]:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated runtime")
    objects, pins = validate_sources()
    candidate.mkdir(parents=True, exist_ok=True)
    need(not any(candidate.iterdir()), "candidate directory not empty")
    components, keys, source_rows, families = reconstruct()
    component_count, component_sequence, component_hashes = write_ledger(candidate / COMPONENT_LEDGER, component_rows(components, source_rows, objects), "fresh_component_id")
    fibre_count, fibre_sequence, fibre_hashes = write_ledger(candidate / FIBRE_LEDGER, fibre_rows(keys, component_hashes, objects), "official_key_id")
    disposition_count, disposition_sequence, _ = write_ledger(candidate / DISPOSITION_LEDGER, disposition_rows(component_hashes, fibre_hashes, objects))
    need(component_count == COMPONENTS and fibre_count == OFFICIAL_KEYS and disposition_count == MEMBERS, "output census")
    component_descriptor = descriptor(candidate / COMPONENT_LEDGER, component_count, component_sequence, "C15_COMPONENT_ORDINAL")
    fibre_descriptor = descriptor(candidate / FIBRE_LEDGER, fibre_count, fibre_sequence, "LEXICOGRAPHIC_OFFICIAL_KEY_ID")
    disposition_descriptor = descriptor(candidate / DISPOSITION_LEDGER, disposition_count, disposition_sequence, "C25_MEMBER_ORDINAL")
    theorem = {
        "kind": "CORRECTED_SOURCE_G_MAXIMAL_COMPONENT_FIBRE_AND_GLOBAL_DISPOSITION_THEOREM",
        "C25_exact_member_support_complete": True,
        "C25_representation_semantics_complete": True,
        "C28_B2_and_component_maximality_complete": True,
        "every_member_has_exactly_one_official_key": True,
        "every_member_has_exactly_one_C15_component": True,
        "every_C15_component_is_C28_maximal": True,
        "every_official_key_fibre_inventory_is_complete": True,
        "every_official_key_fibre_is_globally_exhausted": True,
        "every_member_has_exactly_one_global_disposition": True,
        "source_G_fibre_or_disposition_gap_count": 0,
    }
    body = {
        "schema": "cm2.round306c29.source-g-maximal-component-official-key-fibre-exhaustion-and-global-disposition.v1",
        "status": "PASS_57876_MAXIMAL_COMPONENTS__124_OFFICIAL_KEY_FIBRES_EXHAUSTED__502204_GLOBAL_MEMBER_DISPOSITIONS_SEALED__D02_SOURCE_W_GATE_REMAINS_BLOCKED",
        "corrected_source_G_census": {"members": MEMBERS, "representations": REPRESENTATIONS, "maximal_components": COMPONENTS, "official_keys": OFFICIAL_KEYS, "component_key_incidences": COMPONENT_KEY_INCIDENCES, "component_key_multiplicity_census": COMPONENT_KEY_MULTIPLICITY, "family_member_census": families},
        "fibre_census": {"required": OFFICIAL_KEYS, "exhausted": fibre_count, "open": 0, "component_incidences": COMPONENT_KEY_INCIDENCES},
        "global_disposition_census": {"corrected_typed_member_denominator": MEMBERS, "issued": disposition_count, "missing": 0, "duplicate": 0, "orphan": 0},
        "source_G_fibre_and_disposition_theorem": theorem,
        "source_G_fibre_and_disposition_theorem_sha256": digest(theorem),
        "ledgers": {"maximal_component_fibre_assignment": component_descriptor, "official_key_fibre_exhaustion": fibre_descriptor, "global_member_disposition": disposition_descriptor},
        "input_pins": pins,
        "formal_credit": {"C25_global_support_consumed": 1, "C28_B2_maximality_consumed": 1, "maximal_component_assignments": COMPONENTS, "official_key_fibres_exhausted": OFFICIAL_KEYS, "global_member_dispositions": MEMBERS, "fibre": 1, "global_disposition": 1},
        "strict_nonpromotion": {"D02": "BLOCKED_BY_252_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE", "D03": "UNAUTHORIZED", "D04": "NOT_MINTED", "Gate5_filled_field_slots": "10/18", "Gate5_complete_global_blocks": 0, "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": "CLOSE_SOURCE_W_198_MIXED_PLUS_54_COMPACT_Q_ORIGINS_WITH_FULL_3D_2D_1D_0D_PARTITION_THEN_REAUDIT_D02_D03_D04_GATE5_CM2",
    }
    result = {**body, "result_sha256": digest(body)}
    (candidate / RESULT).write_bytes(canonical(result))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    args = parser.parse_args()
    result = build(Path(args.candidate_dir).resolve())
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"]}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
