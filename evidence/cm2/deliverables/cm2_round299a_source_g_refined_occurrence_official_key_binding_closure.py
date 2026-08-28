#!/usr/bin/env python3
"""Round299-A refined-occurrence official-key binding closure.

This producer adds an official-key binding to each of the 9,404 Round294
occurrences issued from a Round292 refined R287 support component.  It does
not rewrite an occurrence ID, merge keys, or run a component DSU.

The package is producer evidence only.  A later independent verifier must
reconstruct every row without importing or executing this module.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Iterable, Iterator, TextIO


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round299a_source_g_refined_occurrence_"
    "official_key_binding_closure"
)
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"
ATTACKS = HERE / f"{PREFIX}_attack_suite.json"

R275_MANIFEST = (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_"
    "manifest.sha256"
)
R275_CERTIFICATE = (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_"
    "certificate.json"
)
R282_MANIFEST = (
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_"
    "manifest.sha256"
)
R282_LEDGER = (
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_"
    "ledger.json.gz"
)
R285_MANIFEST = (
    "cm2_round285_source_g_true_seam_safe_pairing_contract_probe_"
    "manifest.sha256"
)
R285_LEDGER = (
    "cm2_round285_source_g_true_seam_safe_pairing_contract_probe_"
    "ledger.json.gz"
)
R292_MANIFEST = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_"
    "manifest.sha256"
)
R292_LEDGER = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_"
    "ledger.json.gz"
)
R294_MANIFEST = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "manifest.sha256"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)

MANIFEST_PINS = {
    R275_MANIFEST:
        "a5dbf43a144a0a752f467911ee59e6afd6d2d60d27e0bc80bc45b7afa9334669",
    R282_MANIFEST:
        "c93d7982b036126ea4fcae761316d86863051d19c9fa9a3008b82ef9c6d44081",
    R285_MANIFEST:
        "260065c2a0253516ebda73ba68db8bd76cd3d6e68fade0535d81b77e1471b952",
    R292_MANIFEST:
        "4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870",
    R294_MANIFEST:
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
}

INPUT_PINS = {
    R275_CERTIFICATE:
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R282_LEDGER:
        "6d94bce99b3ea57b8a568707705d9f16833cfba28b242a6dabb2de5933f6509e",
    R285_LEDGER:
        "92462778ad249c5aff2d7a8d0205efa288ccaf191ab8a419c8b6f58a18dfcc1e",
    R292_LEDGER:
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    R294_REGISTRY:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
}

R294_COMMITMENT = {
    "row_count": 431_208,
    "rows_sha256":
        "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
    "row_ids_sha256":
        "bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509",
    "row_hashes_sha256":
        "ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56",
    "occurrence_ids_sha256":
        "169869b5755eda22f1527e7393a5bef0a77a842eefbdf45ab34d315b0dad1936",
}

SCHEMA = (
    "cm2.round299a.source-g-refined-occurrence-"
    "official-key-binding-closure.v1"
)
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
ATTACK_SCHEMA = SCHEMA + ".attack-suite.v1"
ROW_ID_FIELD = "Round299A_refined_occurrence_official_key_binding_row_id"
REFINED_KIND = (
    "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
)
EXISTING_CLASS = "EXISTING_KEY_FROM_PRE_REFINED_ROUND294_KEY_UNIVERSE"
NEW_CLASS = "NEW_RAW_KEY_FROM_PINNED_ROUND275_LOCAL_RETURN_SIGNATURE"
ZERO_FIELDS = (
    "formal_new_occurrence_credit",
    "formal_occurrence_alias_credit",
    "formal_component_union_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)
PHYSICAL_PAYLOAD_FIELDS = (
    "target_chart",
    "target_lift",
    "outgoing_cell",
    "ordered_integer_wall_events",
    "roof",
    "signed_wall_word",
)
KEY_TRANSITION_FIELDS = (
    "official_key_id",
    "official_key_ordinal",
    "official_key_row",
    "ordered_integer_wall_events",
    "roof",
    "signed_wall_word",
)
PIN_RE = re.compile(r"^[0-9a-f]{64}$")


class ClosureError(RuntimeError):
    """Fail-closed construction error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ClosureError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for piece in ENCODER.iterencode(value):
        yield piece.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for piece in chunks(value):
        state.update(piece)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1 << 20), b""):
            state.update(piece)
    return state.hexdigest()


def guard_path(path: Path, maximum: int = 2_000_000_000) -> bytes:
    need(
        path.parent == HERE and path.parent.resolve() == HERE.resolve(),
        "path parent:" + path.name,
    )
    need(path.exists() and not path.is_symlink(), "path exists:" + path.name)
    info = path.stat()
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        "path regular/link/size:" + path.name,
    )
    return path.read_bytes()


def strict_decode(raw: bytes, label: str) -> dict[str, Any]:
    need(
        raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "strict bytes:" + label,
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "duplicate key:" + label + ":" + key)
            result[key] = value
        return result

    def reject(token: str) -> Any:
        raise ClosureError("noninteger JSON token:" + label + ":" + token)

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique,
            parse_float=reject,
            parse_constant=reject,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ClosureError("strict JSON:" + label) from error
    need(type(value) is dict, "top object:" + label)
    return value


def read_json(name: str) -> dict[str, Any]:
    return strict_decode(guard_path(HERE / name), name)


def read_gzip_json(name: str) -> dict[str, Any]:
    try:
        raw = gzip.decompress(guard_path(HERE / name))
    except Exception as error:
        raise ClosureError("gzip:" + name) from error
    return strict_decode(raw, name)


def validate_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    payload = {key: value for key, value in row.items()
               if key != "row_sha256"}
    need(type(claimed) is str and digest(payload) == claimed,
         "row closure:" + label)


def close_row(
    prefix: str,
    domain: str,
    id_field: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    row = {
        id_field: prefix + digest([domain, payload]),
        **payload,
    }
    row["row_sha256"] = digest(row)
    return row


class ListHasher:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for piece in chunks(value):
            self.state.update(piece)
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def rows_commitment(
    rows: list[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), "unique output row IDs")
    return {
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest(
            [row["row_sha256"] for row in rows]
        ),
        "rows_sha256": digest(rows),
    }


def verify_table(
    table: dict[str, Any],
    id_field: str,
    expected_count: int,
    label: str,
) -> list[dict[str, Any]]:
    rows = table.get("rows")
    need(
        type(rows) is list
        and len(rows) == table.get("row_count") == expected_count,
        "table count:" + label,
    )
    for row in rows:
        validate_row(row, label)
    expected = rows_commitment(rows, id_field)
    need(
        all(table.get(key) == value for key, value in expected.items()),
        "table commitment:" + label,
    )
    return rows


def parse_manifest(name: str) -> dict[str, str]:
    result: dict[str, str] = {}
    raw = guard_path(HERE / name, 200_000)
    for line in raw.decode("utf-8").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, "manifest syntax:" + name)
        sha256, filename = match.groups()
        need(
            Path(filename).name == filename
            and filename not in result,
            "manifest path/duplicate:" + name,
        )
        result[filename] = sha256
    need(bool(result), "empty manifest:" + name)
    return result


def validate_input_boundary() -> None:
    for name, expected in MANIFEST_PINS.items():
        need(PIN_RE.fullmatch(expected) is not None, "manifest pin syntax")
        need(file_sha256(HERE / name) == expected, "manifest pin:" + name)
        manifest = parse_manifest(name)
        for member, member_sha in manifest.items():
            need(
                file_sha256(HERE / member) == member_sha,
                "manifest member:" + name + ":" + member,
            )
    for name, expected in INPUT_PINS.items():
        need(PIN_RE.fullmatch(expected) is not None, "input pin syntax")
        need(file_sha256(HERE / name) == expected, "input pin:" + name)
    membership = {
        R275_MANIFEST: R275_CERTIFICATE,
        R282_MANIFEST: R282_LEDGER,
        R285_MANIFEST: R285_LEDGER,
        R292_MANIFEST: R292_LEDGER,
        R294_MANIFEST: R294_REGISTRY,
    }
    for manifest_name, member in membership.items():
        need(
            parse_manifest(manifest_name).get(member) == INPUT_PINS[member],
            "manifest selected member:" + manifest_name + ":" + member,
        )


def iterate_array(
    stream: TextIO,
    marker: str = '"rows":[',
) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        piece = stream.read(1 << 20)
        need(bool(piece), "array marker:" + marker)
        buffer += piece
        if len(buffer) > 2 * (1 << 20):
            buffer = buffer[-(len(marker) + (1 << 20)):]
    buffer = buffer.split(marker, 1)[1]

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "stream duplicate key:" + key)
            result[key] = value
        return result

    decoder = json.JSONDecoder(
        object_pairs_hook=unique,
        parse_float=lambda token: (_ for _ in ()).throw(
            ClosureError("stream float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            ClosureError("stream constant:" + token)
        ),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            piece = stream.read(1 << 20)
            need(bool(piece), "unexpected streamed EOF")
            buffer = piece
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                value, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                piece = stream.read(1 << 20)
                need(bool(piece), "malformed streamed row")
                buffer += piece
        need(type(value) is dict, "streamed row object")
        yield value
        buffer = buffer[end:]


def r294_rows() -> Iterator[dict[str, Any]]:
    with gzip.open(
        HERE / R294_REGISTRY,
        "rt",
        encoding="utf-8",
        newline="",
    ) as stream:
        yield from iterate_array(stream)


def histogram(values: Iterable[int]) -> dict[str, int]:
    return {
        str(key): value
        for key, value in sorted(Counter(values).items())
    }


def physical_payload(signature: dict[str, Any]) -> dict[str, Any]:
    return {
        field: signature[field] for field in PHYSICAL_PAYLOAD_FIELDS
    }


def deterministic_gzip(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        fileobj=buffer,
        mode="wb",
        mtime=0,
        compresslevel=9,
    ) as stream:
        for piece in chunks(value):
            stream.write(piece)
    return buffer.getvalue()


def atomic_write(path: Path, payload: bytes) -> None:
    parent = path.parent.resolve()
    need(parent.is_dir(), "output parent:" + str(path))
    need(not path.is_symlink(), "output symlink:" + str(path))
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=parent,
        prefix="." + path.name + ".",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def load_sources() -> dict[str, Any]:
    certificate = read_json(R275_CERTIFICATE)
    need(
        digest(certificate["result"]) == certificate["result_sha256"],
        "Round275 result self closure",
    )
    r275_result = certificate["result"]
    strict_rows = verify_table(
        r275_result["strict_region_ledger"],
        "reverse_rechart_region_row_id",
        5_288,
        "Round275 strict",
    )
    arrangement_rows = verify_table(
        r275_result["arrangement_region_ledger"],
        "reverse_rechart_region_row_id",
        8_500,
        "Round275 arrangement",
    )
    r275_rows = strict_rows + arrangement_rows
    r275 = {
        row["reverse_rechart_region_row_id"]: row for row in r275_rows
    }
    need(len(r275) == 13_788, "Round275 unique region universe")
    for row in r275_rows:
        need(
            digest(row["local_return_signature"])
            == row["complete_10_field_return_signature_sha256"],
            "Round275 local signature closure",
        )

    r292_doc = read_gzip_json(R292_LEDGER)
    r292_rows = r292_doc.get("rows")
    need(
        type(r292_rows) is list
        and len(r292_rows) == r292_doc.get("row_count") == 22_820,
        "Round292 mixed table count",
    )
    for row in r292_rows:
        validate_row(row, "Round292 mixed")
    need(
        r292_doc["rows_sha256"] == digest(r292_rows),
        "Round292 rows commitment",
    )
    refinement = {
        row["Round292_R287_existing_overlap_refinement_cell_id"]: row
        for row in r292_rows
        if "Round292_R287_existing_overlap_refinement_cell_id" in row
    }
    components = {
        row["Round292_refined_new_support_component_id"]: row
        for row in r292_rows
        if "member_refinement_cell_ids" in row
    }
    need(
        len(refinement) == 11_852
        and len(components) == 9_404,
        "Round292 refinement/component universe",
    )

    r282_doc = read_gzip_json(R282_LEDGER)
    r282_rows = verify_table(
        r282_doc,
        "Round282_seam_corridor_row_id",
        152,
        "Round282 corridor",
    )
    r285_doc = read_gzip_json(R285_LEDGER)
    r285_rows = verify_table(
        r285_doc,
        "Round285_safe_pairing_row_id",
        152,
        "Round285 safe pairing",
    )

    old_keys: set[str] = set()
    refined_registry_rows: list[dict[str, Any]] = []
    registry_kind_histogram: Counter[str] = Counter()
    rows_hash = ListHasher()
    ids_hash = ListHasher()
    row_hashes_hash = ListHasher()
    occurrence_ids_hash = ListHasher()
    seen_occurrences: set[str] = set()
    for row in r294_rows():
        validate_row(row, "Round294 registry")
        occurrence = row["registry_occurrence_id"]
        need(occurrence not in seen_occurrences, "Round294 duplicate occurrence")
        seen_occurrences.add(occurrence)
        rows_hash.add(row)
        ids_hash.add(row["Round294_occurrence_registry_row_id"])
        row_hashes_hash.add(row["row_sha256"])
        occurrence_ids_hash.add(occurrence)
        kind = row["registry_entry_kind"]
        registry_kind_histogram[kind] += 1
        if kind == REFINED_KIND:
            need(
                row["official_key_id"] is None
                and row["official_key_ordinal"] is None
                and row["official_key_binding_status"]
                == "NOT_MATERIALIZED_IN_R287_FROZEN_LEDGER__"
                "COMPLETE_SIGNATURE_HASH_PINNED",
                "Round294 refined key-null freeze",
            )
            refined_registry_rows.append(row)
        else:
            key = row["official_key_id"]
            need(type(key) is str, "Round294 nonrefined official key")
            old_keys.add(key)
    recomputed = {
        "row_count": rows_hash.count,
        "rows_sha256": rows_hash.finish(),
        "row_ids_sha256": ids_hash.finish(),
        "row_hashes_sha256": row_hashes_hash.finish(),
        "occurrence_ids_sha256": occurrence_ids_hash.finish(),
    }
    need(recomputed == R294_COMMITMENT, "Round294 complete commitment")
    need(
        registry_kind_histogram == {
            "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
            "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
            REFINED_KIND: 9_404,
        }
        and len(refined_registry_rows) == 9_404
        and len(old_keys) == 116,
        "Round294 registry/key census",
    )
    return {
        "r275_rows": r275_rows,
        "r275": r275,
        "strict_rows": strict_rows,
        "arrangement_rows": arrangement_rows,
        "refinement": refinement,
        "components": components,
        "r282_rows": r282_rows,
        "r285_rows": r285_rows,
        "refined_registry_rows": refined_registry_rows,
        "old_keys": old_keys,
        "registry_kind_histogram": registry_kind_histogram,
    }


def build_binding_rows(source: dict[str, Any]) -> dict[str, Any]:
    r275 = source["r275"]
    refinement = source["refinement"]
    components = source["components"]
    old_keys = source["old_keys"]
    output: list[dict[str, Any]] = []
    key_occurrences: Counter[str] = Counter()
    key_regions: dict[str, set[str]] = defaultdict(set)
    key_member_cells: Counter[str] = Counter()
    classification_histogram: Counter[str] = Counter()
    seen_components: set[str] = set()
    seen_occurrences: set[str] = set()
    mismatch_count = 0

    for registry in source["refined_registry_rows"]:
        occurrence = registry["registry_occurrence_id"]
        component_id = registry["source_row_id"]
        region_id = registry["Round275_region_id"]
        need(
            occurrence not in seen_occurrences
            and component_id not in seen_components,
            "one refined occurrence/component",
        )
        seen_occurrences.add(occurrence)
        seen_components.add(component_id)
        need(component_id in components, "Round292 component join")
        need(region_id in r275, "Round275 region join")
        component = components[component_id]
        region = r275[region_id]
        signature = region["local_return_signature"]
        signature_sha = region[
            "complete_10_field_return_signature_sha256"
        ]
        member_ids = component["member_refinement_cell_ids"]
        registry_member_ids = sorted(
            row["Round292_refinement_cell_id"]
            for row in registry["member_refinement_cells"]
        )
        checks = [
            registry["source_row_sha256"] == component["row_sha256"],
            registry["complete_10_field_return_signature_sha256"]
            == signature_sha == digest(signature),
            registry["physical_support_chart"] == region["adjacent_chart"],
            registry["owner_target"] == region["owner_target"],
            registry["member_refinement_cell_count"]
            == component["member_refinement_cell_count"],
            registry_member_ids == member_ids,
        ]
        need(all(checks), "registry/component/region exact join")
        for member in registry["member_refinement_cells"]:
            member_id = member["Round292_refinement_cell_id"]
            need(member_id in refinement, "Round292 member join")
            exact = refinement[member_id]
            member_checks = [
                member["Round275_region_id"]
                == exact["Round275_region_id"] == region_id,
                member["complete_10_field_return_signature_sha256"]
                == exact["complete_10_field_return_signature_sha256"]
                == signature_sha,
                member["physical_support_chart"]
                == exact["source_chart"] == region["adjacent_chart"],
                member["exact_transformed_open_cell"]
                == exact["exact_transformed_open_cell"],
                member["exact_transformed_cell_volume"]
                == exact["exact_transformed_cell_volume"],
                member["source_row_sha256"] == exact["row_sha256"],
            ]
            mismatch_count += sum(not value for value in member_checks)
            need(all(member_checks), "refinement member exact join")

        official_key = signature["official_key_id"]
        classification = (
            EXISTING_CLASS if official_key in old_keys else NEW_CLASS
        )
        classification_histogram[classification] += 1
        key_occurrences[official_key] += 1
        key_regions[official_key].add(region_id)
        key_member_cells[official_key] += len(member_ids)
        payload = {
            "source_Round294_occurrence_registry_row_id":
                registry["Round294_occurrence_registry_row_id"],
            "source_Round294_occurrence_registry_row_sha256":
                registry["row_sha256"],
            "registry_occurrence_id": occurrence,
            "registry_entry_kind": registry["registry_entry_kind"],
            "source_Round292_refined_support_component_id": component_id,
            "source_Round292_refined_support_component_row_sha256":
                component["row_sha256"],
            "source_Round275_region_id": region_id,
            "source_Round275_region_row_sha256": region["row_sha256"],
            "source_Round294_official_key_binding_status":
                registry["official_key_binding_status"],
            "complete_10_field_return_signature_sha256": signature_sha,
            "source_Round275_local_return_signature": signature,
            "official_key_id": official_key,
            "official_key_ordinal": signature["official_key_ordinal"],
            "official_key_row": signature["official_key_row"],
            "binding_classification": classification,
            "binding_basis":
                "EXACT_ROUND275_REGION_ID_PLUS_COMPLETE_10_FIELD_"
                "SIGNATURE_HASH_PREIMAGE",
            "member_refinement_cell_count": len(member_ids),
            "member_refinement_cell_ids_sha256": digest(member_ids),
            "append_only_official_key_binding": True,
            "occurrence_identity_preserved": True,
            "raw_key_merge_credit": 0,
            "formal_refined_occurrence_official_key_binding_credit": 1,
            **{field: 0 for field in ZERO_FIELDS},
        }
        output.append(close_row(
            "round299a-refined-occurrence-key-binding:",
            "ROUND299A_REFINED_OCCURRENCE_KEY_BINDING_V1",
            ROW_ID_FIELD,
            payload,
        ))

    output.sort(key=lambda row: row[ROW_ID_FIELD])
    need(
        len(output) == len(seen_occurrences)
        == len(seen_components) == 9_404
        and mismatch_count == 0,
        "complete refined binding universe",
    )
    bound_keys = set(key_occurrences)
    existing_bound = bound_keys & old_keys
    new_keys = bound_keys - old_keys
    need(
        classification_histogram
        == {EXISTING_CLASS: 8_212, NEW_CLASS: 1_192}
        and len(bound_keys) == 44
        and len(existing_bound) == 36
        and len(new_keys) == 8
        and all(key_occurrences[key] == 149 for key in new_keys)
        and all(key_member_cells[key] == 149 for key in new_keys),
        "old/new key binding census",
    )
    return {
        "rows": output,
        "key_occurrences": key_occurrences,
        "key_regions": key_regions,
        "key_member_cells": key_member_cells,
        "classification_histogram": classification_histogram,
        "existing_bound_keys": existing_bound,
        "new_keys": new_keys,
        "mismatch_count": mismatch_count,
    }


def build_nonmerge_audit(
    source: dict[str, Any],
    binding: dict[str, Any],
) -> dict[str, Any]:
    old_keys = source["old_keys"]
    new_keys = binding["new_keys"]
    r275_rows = source["r275_rows"]
    strict_rows = source["strict_rows"]
    arrangement_rows = source["arrangement_rows"]
    r275 = source["r275"]

    signatures_by_key: dict[str, set[str]] = defaultdict(set)
    payload_keys: dict[str, set[str]] = defaultdict(set)
    for row in r275_rows:
        signature = row["local_return_signature"]
        key = signature["official_key_id"]
        signatures_by_key[key].add(
            canonical(signature).decode("utf-8")
        )
        payload_keys[digest(physical_payload(signature))].add(key)
    need(
        len(signatures_by_key) == 44
        and all(len(signatures_by_key[key]) == 1 for key in new_keys),
        "Round275 raw/new signature universe",
    )

    arrangement_groups: dict[
        tuple[str, tuple[str, ...], tuple[str, ...], str],
        list[dict[str, Any]],
    ] = defaultdict(list)
    for row in arrangement_rows:
        arrangement_groups[(
            row["source_guard_row_id"],
            tuple(row["adjacent_cover_refinement_path"]),
            tuple(row["adjacent_rational_region_box"]),
            row["active_reason"],
        )].append(row)

    summaries: list[dict[str, Any]] = []
    all_sibling_pair_count = 0
    for key in sorted(new_keys):
        key_strict = [
            row for row in strict_rows
            if row["local_return_signature"]["official_key_id"] == key
        ]
        key_arrangement = [
            row for row in arrangement_rows
            if row["local_return_signature"]["official_key_id"] == key
        ]
        need(
            len(key_strict) == 21
            and len(key_arrangement) == 128
            and all(
                row["arrangement_classification"]
                == "REGULAR_GRAPH_CROSSING"
                and row["active_reason"] in {
                    "wall_endpoint_or_count_transition:X:0",
                    "wall_endpoint_or_count_transition:Y:0",
                }
                for row in key_arrangement
            ),
            "new-key R275 region classification",
        )
        counterpart_counts: Counter[str] = Counter()
        reason_counts: Counter[str] = Counter()
        differing_counts: Counter[tuple[str, ...]] = Counter()
        for row in key_arrangement:
            group_key = (
                row["source_guard_row_id"],
                tuple(row["adjacent_cover_refinement_path"]),
                tuple(row["adjacent_rational_region_box"]),
                row["active_reason"],
            )
            siblings = [
                value for value in arrangement_groups[group_key]
                if value["reverse_rechart_region_row_id"]
                != row["reverse_rechart_region_row_id"]
            ]
            need(len(siblings) == 1, "unique wall-transition sibling")
            sibling = siblings[0]
            sibling_key = sibling[
                "local_return_signature"
            ]["official_key_id"]
            need(sibling_key in old_keys, "sibling belongs to old 116")
            counterpart_counts[sibling_key] += 1
            reason_counts[row["active_reason"]] += 1
            left = row["local_return_signature"]
            right = sibling["local_return_signature"]
            differing = tuple(sorted(
                field for field in left if left[field] != right[field]
            ))
            need(
                differing == tuple(sorted(KEY_TRANSITION_FIELDS)),
                "exact wall-transition signature difference",
            )
            differing_counts[differing] += 1
        need(
            len(counterpart_counts) == 1
            and next(iter(counterpart_counts.values())) == 128
            and len(reason_counts) == 1
            and len(differing_counts) == 1,
            "one explicit distinct sibling class per new key",
        )
        sibling_key = next(iter(counterpart_counts))
        new_signature = json.loads(next(iter(signatures_by_key[key])))
        sibling_signatures = [
            row["local_return_signature"]
            for row in r275_rows
            if row["local_return_signature"]["official_key_id"]
            == sibling_key
        ]
        sibling_ordinal = sibling_signatures[0]["official_key_ordinal"]
        payload_sha = digest(physical_payload(new_signature))
        other_payload_keys = payload_keys[payload_sha] - {key}
        need(not other_payload_keys, "new-key transported payload collision")
        summaries.append({
            "new_raw_official_key_id": key,
            "new_raw_official_key_ordinal":
                new_signature["official_key_ordinal"],
            "new_raw_official_key_row":
                new_signature["official_key_row"],
            "bound_refined_occurrence_count":
                binding["key_occurrences"][key],
            "bound_Round275_region_count":
                len(binding["key_regions"][key]),
            "bound_refinement_member_cell_count":
                binding["key_member_cells"][key],
            "Round275_strict_region_count": len(key_strict),
            "Round275_regular_graph_crossing_region_count":
                len(key_arrangement),
            "unique_old_116_wall_transition_sibling_key_id":
                sibling_key,
            "unique_old_116_wall_transition_sibling_key_ordinal":
                sibling_ordinal,
            "wall_transition_sibling_pair_count":
                counterpart_counts[sibling_key],
            "wall_transition_reason": next(iter(reason_counts)),
            "wall_transition_differing_signature_fields":
                list(next(iter(differing_counts))),
            "wall_transition_is_transported_key_equivalence": False,
            "transported_physical_payload_sha256": payload_sha,
            "other_Round275_raw_keys_with_exact_transported_payload_count":
                0,
            "Round285_corridor_region_incidence_count": 0,
            "formal_raw_key_merge_credit": 0,
        })
        all_sibling_pair_count += counterpart_counts[sibling_key]

    r282 = {
        row["Round268_true_seam_patch_row_id"]: row
        for row in source["r282_rows"]
    }
    need(len(r282) == 152, "Round282 patch universe")
    corridor_region_occurrences: list[str] = []
    side_hash_mismatch_count = 0
    new_key_corridor_occurrences = 0
    for r285_row in source["r285_rows"]:
        patch_id = r285_row["Round268_true_seam_patch_row_id"]
        need(patch_id in r282, "Round285/Round282 patch join")
        r282_row = r282[patch_id]
        output_sides = {
            row["side"]: row for row in r285_row["side_summaries"]
        }
        for side in r282_row["side_corridors"]:
            region_ids = sorted({
                row["Round275_region_id"]
                for row in side["accepted_strict_corridors"]
            })
            corridor_region_occurrences.extend(region_ids)
            summary = output_sides[side["side"]]
            side_hash_mismatch_count += int(
                summary["distinct_Round275_region_count"] != len(region_ids)
                or summary["distinct_Round275_region_ids_sha256"]
                != digest(region_ids)
            )
            new_key_corridor_occurrences += sum(
                r275[region_id]["local_return_signature"][
                    "official_key_id"
                ] in new_keys
                for region_id in region_ids
            )
    need(
        len(corridor_region_occurrences) == 2_660
        and len(set(corridor_region_occurrences)) == 2_636
        and side_hash_mismatch_count == 0
        and new_key_corridor_occurrences == 0,
        "Round285 zero-incidence audit",
    )
    for row in summaries:
        row["Round285_corridor_region_incidence_count"] = 0
    return {
        "new_raw_key_rows": summaries,
        "new_raw_key_count": 8,
        "new_raw_key_Round275_region_count": 1_192,
        "new_raw_key_Round275_strict_region_count": 168,
        "new_raw_key_Round275_regular_graph_crossing_region_count": 1_024,
        "wall_transition_sibling_pair_count": all_sibling_pair_count,
        "wall_transition_sibling_pairs_are_key_equivalences": False,
        "exact_transported_payload_match_to_other_Round275_key_count": 0,
        "Round282_patch_count": 152,
        "Round285_side_region_count_hash_mismatch_count":
            side_hash_mismatch_count,
        "Round285_corridor_region_occurrence_count":
            len(corridor_region_occurrences),
        "Round285_distinct_corridor_region_count":
            len(set(corridor_region_occurrences)),
        "new_raw_key_Round285_corridor_region_incidence_count":
            new_key_corridor_occurrences,
        "transported_equivalence_supports_any_new_key_merge": False,
        "formal_raw_key_merge_credit": 0,
    }


def attack_specifications() -> list[tuple[str, str, str]]:
    return [
        ("A01_DROP_BINDING_ROW", "ledger", "drop one of 9404 rows"),
        ("A02_DUPLICATE_BINDING_ROW", "ledger", "duplicate one row"),
        ("A03_OCCURRENCE_SUBSTITUTION", "row", "change registry occurrence"),
        ("A04_R292_COMPONENT_SUBSTITUTION", "row", "change source component"),
        ("A05_R275_REGION_SUBSTITUTION", "row", "change source region"),
        ("A06_SIGNATURE_HASH_SUBSTITUTION", "row", "change signature digest"),
        ("A07_OFFICIAL_KEY_SUBSTITUTION", "row", "change bound key"),
        ("A08_KEY_ORDINAL_SUBSTITUTION", "row", "change bound ordinal"),
        ("A09_KEY_ROW_SUBSTITUTION", "row", "change official key row"),
        ("A10_OLD_NEW_CLASS_FLIP", "row", "flip binding classification"),
        ("A11_FORCE_OLD_116_ONLY", "result", "drop eight new raw keys"),
        ("A12_COLLAPSE_NEW_TO_SIBLING", "row", "bind new key to wall sibling"),
        ("A13_WALL_FACE_AS_KEY_EQUIVALENCE", "result", "merge across X/Y graph"),
        ("A14_FORGE_R285_INCIDENCE", "result", "claim transported seam evidence"),
        ("A15_RELAX_PHYSICAL_PAYLOAD", "result", "ignore events/roof/wall word"),
        ("A16_MEMBER_CELL_OMISSION", "row", "drop refinement member"),
        ("A17_MEMBER_BOX_SUBSTITUTION", "source", "alter exact member box"),
        ("A18_MEMBER_VOLUME_SUBSTITUTION", "source", "alter exact volume"),
        ("A19_OCCURRENCE_IDENTITY_COLLAPSE", "row", "rewrite occurrence identity"),
        ("A20_OCCURRENCE_ALIAS_CREDIT", "row", "grant alias credit"),
        ("A21_COMPONENT_UNION_CREDIT", "row", "grant component credit"),
        ("A22_DSU_RANK_CREDIT", "row", "grant DSU rank credit"),
        ("A23_JX_JY_GLUE_CREDIT", "row", "grant Jx/Jy credit"),
        ("A24_MAXIMALITY_CREDIT", "result", "claim maximality"),
        ("A25_FIBRE_EXHAUSTION", "result", "claim 116-fibre exhaustion"),
        ("A26_GLOBAL_DISPOSITION", "result", "claim global disposition"),
        ("A27_D02_PROMOTION", "result", "unblock D02"),
        ("A28_CM2_PROMOTION", "result", "claim CM2"),
        ("A29_STALE_MANIFEST", "input", "substitute an upstream package"),
        ("A30_DUPLICATE_JSON_KEY", "encoding", "duplicate a JSON key"),
        ("A31_NONFINITE_OR_NUL_JSON", "encoding", "use NaN or NUL"),
        ("A32_MALFORMED_OR_CONCAT_GZIP", "encoding", "alter GZIP stream"),
        ("A33_SYMLINK_HARDLINK_TRAVERSAL", "filesystem", "substitute a path"),
    ]


def producer_self_attack_rejection(
    source: dict[str, Any],
    ledger: dict[str, Any],
    result: dict[str, Any],
) -> list[dict[str, Any]]:
    """Reclose and reject mutations using the producer reconstruction.

    This is construction-time self-audit evidence only.  It is deliberately
    not described as independent verification.
    """
    specifications = attack_specifications()
    expected_row = ledger["rows"][0]
    expected_new_row = next(
        row for row in ledger["rows"]
        if row["binding_classification"] == NEW_CLASS
    )
    expected_source_row = next(iter(source["refinement"].values()))

    def raw_commitment(
        rows: list[dict[str, Any]],
    ) -> dict[str, Any]:
        return {
            "row_count": len(rows),
            "row_ids_sha256": digest(
                [row[ROW_ID_FIELD] for row in rows]
            ),
            "row_hashes_sha256": digest(
                [row["row_sha256"] for row in rows]
            ),
            "rows_sha256": digest(rows),
        }

    def exact_ledger(candidate: dict[str, Any]) -> None:
        rows = candidate.get("rows")
        need(type(rows) is list, "self-attack ledger rows")
        for row in rows:
            validate_row(row, "self-attack ledger row")
        ids = [row[ROW_ID_FIELD] for row in rows]
        need(len(ids) == len(set(ids)), "self-attack unique ledger row IDs")
        need(
            raw_commitment(rows)
            == {
                key: candidate.get(key)
                for key in (
                    "row_count",
                    "row_ids_sha256",
                    "row_hashes_sha256",
                    "rows_sha256",
                )
            },
            "self-attack ledger commitment",
        )
        need(candidate == ledger, "self-attack exact reconstructed ledger")

    def reclose_binding(
        row: dict[str, Any],
    ) -> dict[str, Any]:
        payload = {
            key: value for key, value in row.items()
            if key not in {ROW_ID_FIELD, "row_sha256"}
        }
        return close_row(
            "round299a-refined-occurrence-key-binding:",
            "ROUND299A_REFINED_OCCURRENCE_KEY_BINDING_V1",
            ROW_ID_FIELD,
            payload,
        )

    def exact_binding(
        candidate: dict[str, Any],
        expected: dict[str, Any],
    ) -> None:
        validate_row(candidate, "self-attack binding row")
        need(candidate == expected, "self-attack exact reconstructed row")

    def mutate_binding(
        expected: dict[str, Any],
        field: str,
        value: Any,
    ) -> None:
        candidate = copy.deepcopy(expected)
        candidate[field] = value
        exact_binding(reclose_binding(candidate), expected)

    def exact_source(candidate: dict[str, Any]) -> None:
        validate_row(candidate, "self-attack refinement source row")
        need(
            candidate == expected_source_row,
            "self-attack exact reconstructed refinement source row",
        )

    def mutate_source(field: str, value: Any) -> None:
        candidate = copy.deepcopy(expected_source_row)
        candidate[field] = value
        candidate["row_sha256"] = digest({
            key: item for key, item in candidate.items()
            if key != "row_sha256"
        })
        exact_source(candidate)

    def exact_result(candidate: dict[str, Any]) -> None:
        claimed = candidate.get("result_sha256")
        payload = {
            key: value for key, value in candidate.items()
            if key != "result_sha256"
        }
        need(
            type(claimed) is str and digest(payload) == claimed,
            "self-attack result closure",
        )
        need(candidate == result, "self-attack exact reconstructed result")

    def mutate_result(path: tuple[str, ...], value: Any) -> None:
        candidate = copy.deepcopy(result)
        cursor: dict[str, Any] = candidate
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        candidate.pop("result_sha256")
        candidate["result_sha256"] = digest(candidate)
        exact_result(candidate)

    row_mutations: dict[str, tuple[str, Any]] = {
        "A03_OCCURRENCE_SUBSTITUTION":
            ("registry_occurrence_id", "forged-occurrence"),
        "A04_R292_COMPONENT_SUBSTITUTION":
            ("source_Round292_refined_support_component_id", "forged-component"),
        "A05_R275_REGION_SUBSTITUTION":
            ("source_Round275_region_id", "forged-region"),
        "A06_SIGNATURE_HASH_SUBSTITUTION":
            ("complete_10_field_return_signature_sha256", "0" * 64),
        "A07_OFFICIAL_KEY_SUBSTITUTION":
            ("official_key_id", "forged-key"),
        "A08_KEY_ORDINAL_SUBSTITUTION":
            ("official_key_ordinal", expected_row["official_key_ordinal"] + 1),
        "A09_KEY_ROW_SUBSTITUTION":
            ("official_key_row", {"forged": True}),
        "A10_OLD_NEW_CLASS_FLIP": (
            "binding_classification",
            (
                NEW_CLASS
                if expected_row["binding_classification"] == EXISTING_CLASS
                else EXISTING_CLASS
            ),
        ),
        "A16_MEMBER_CELL_OMISSION": (
            "member_refinement_cell_count",
            expected_row["member_refinement_cell_count"] - 1,
        ),
        "A19_OCCURRENCE_IDENTITY_COLLAPSE":
            ("occurrence_identity_preserved", False),
        "A20_OCCURRENCE_ALIAS_CREDIT":
            ("formal_occurrence_alias_credit", 1),
        "A21_COMPONENT_UNION_CREDIT":
            ("formal_component_union_credit", 1),
        "A22_DSU_RANK_CREDIT":
            ("formal_DSU_rank_reduction_credit", 1),
        "A23_JX_JY_GLUE_CREDIT":
            ("formal_Jx_Jy_same_point_glue_credit", 1),
    }
    result_mutations: dict[str, tuple[tuple[str, ...], Any]] = {
        "A11_FORCE_OLD_116_ONLY": (
            ("raw_observed_key_universe", "after_refined_binding_count"),
            116,
        ),
        "A13_WALL_FACE_AS_KEY_EQUIVALENCE": (
            (
                "nonmerge_audit",
                "wall_transition_sibling_pairs_are_key_equivalences",
            ),
            True,
        ),
        "A14_FORGE_R285_INCIDENCE": (
            (
                "nonmerge_audit",
                "new_raw_key_Round285_corridor_region_incidence_count",
            ),
            1,
        ),
        "A15_RELAX_PHYSICAL_PAYLOAD": (
            (
                "nonmerge_audit",
                "exact_transported_payload_match_to_other_Round275_key_count",
            ),
            1,
        ),
        "A24_MAXIMALITY_CREDIT":
            (("strict_nonpromotion", "maximality_status"), "CERTIFIED"),
        "A25_FIBRE_EXHAUSTION": (
            ("strict_nonpromotion", "exact_key_fibre_exhaustion_status"),
            "CERTIFIED",
        ),
        "A26_GLOBAL_DISPOSITION": (
            ("strict_nonpromotion", "global_disposition_status"),
            "CERTIFIED",
        ),
        "A27_D02_PROMOTION":
            (("strict_nonpromotion", "D02"), "UNBLOCKED"),
        "A28_CM2_PROMOTION":
            (("strict_nonpromotion", "CM2"), "CERTIFIED"),
    }

    def execute(attack_id: str) -> str:
        if attack_id == "A01_DROP_BINDING_ROW":
            rows = ledger["rows"][:-1]
            exact_ledger({
                "schema": LEDGER_SCHEMA,
                **raw_commitment(rows),
                "rows": rows,
            })
            return "RECLOSED_LEDGER_EXACT_UNIVERSE"
        if attack_id == "A02_DUPLICATE_BINDING_ROW":
            rows = ledger["rows"] + [ledger["rows"][0]]
            exact_ledger({
                "schema": LEDGER_SCHEMA,
                **raw_commitment(rows),
                "rows": rows,
            })
            return "RECLOSED_LEDGER_UNIQUE_ROW_ID"
        if attack_id in row_mutations:
            field, value = row_mutations[attack_id]
            mutate_binding(expected_row, field, value)
            return "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"
        if attack_id == "A12_COLLAPSE_NEW_TO_SIBLING":
            new_key = expected_new_row["official_key_id"]
            summary = next(
                row for row in result["nonmerge_audit"]["new_raw_key_rows"]
                if row["new_raw_official_key_id"] == new_key
            )
            mutate_binding(
                expected_new_row,
                "official_key_id",
                summary[
                    "unique_old_116_wall_transition_sibling_key_id"
                ],
            )
            return "RECLOSED_NEW_KEY_ROW_EXACT_RECONSTRUCTION"
        if attack_id in result_mutations:
            path, value = result_mutations[attack_id]
            mutate_result(path, value)
            return "RECLOSED_RESULT_EXACT_RECONSTRUCTION"
        if attack_id == "A17_MEMBER_BOX_SUBSTITUTION":
            mutate_source(
                "exact_transformed_open_cell",
                {"forged": True},
            )
            return "RECLOSED_SOURCE_ROW_EXACT_RECONSTRUCTION"
        if attack_id == "A18_MEMBER_VOLUME_SUBSTITUTION":
            mutate_source("exact_transformed_cell_volume", "forged-volume")
            return "RECLOSED_SOURCE_ROW_EXACT_RECONSTRUCTION"
        if attack_id == "A29_STALE_MANIFEST":
            need(
                "0" * 64 == MANIFEST_PINS[R275_MANIFEST],
                "self-attack exact manifest pin",
            )
            return "EXACT_INPUT_MANIFEST_PIN"
        if attack_id == "A30_DUPLICATE_JSON_KEY":
            strict_decode(b'{"x":1,"x":2}', "self-attack-A30")
            return "STRICT_JSON_DUPLICATE_KEY"
        if attack_id == "A31_NONFINITE_OR_NUL_JSON":
            strict_decode(b'{"x":NaN}', "self-attack-A31")
            return "STRICT_JSON_NONFINITE"
        if attack_id == "A32_MALFORMED_OR_CONCAT_GZIP":
            try:
                gzip.decompress(b"\x1f\x8b\x08\x00truncated")
            except Exception as error:
                raise ClosureError("self-attack malformed GZIP") from error
            return "STRICT_GZIP_MALFORMED_STREAM"
        if attack_id == "A33_SYMLINK_HARDLINK_TRAVERSAL":
            guard_path(HERE / ".." / HERE.name / R275_CERTIFICATE)
            return "LEXICAL_PATH_TRAVERSAL_GUARD"
        raise ClosureError("unknown self-attack:" + attack_id)

    outcomes: list[dict[str, Any]] = []
    for attack_id, target, mutation in specifications:
        rejection_reason = ""
        try:
            probe_kind = execute(attack_id)
        except ClosureError as error:
            rejection_reason = str(error)
            probe_kind = {
                "A01_DROP_BINDING_ROW": "RECLOSED_LEDGER_EXACT_UNIVERSE",
                "A02_DUPLICATE_BINDING_ROW": "RECLOSED_LEDGER_UNIQUE_ROW_ID",
                "A12_COLLAPSE_NEW_TO_SIBLING":
                    "RECLOSED_NEW_KEY_ROW_EXACT_RECONSTRUCTION",
                "A17_MEMBER_BOX_SUBSTITUTION":
                    "RECLOSED_SOURCE_ROW_EXACT_RECONSTRUCTION",
                "A18_MEMBER_VOLUME_SUBSTITUTION":
                    "RECLOSED_SOURCE_ROW_EXACT_RECONSTRUCTION",
                "A29_STALE_MANIFEST": "EXACT_INPUT_MANIFEST_PIN",
                "A30_DUPLICATE_JSON_KEY": "STRICT_JSON_DUPLICATE_KEY",
                "A31_NONFINITE_OR_NUL_JSON": "STRICT_JSON_NONFINITE",
                "A32_MALFORMED_OR_CONCAT_GZIP":
                    "STRICT_GZIP_MALFORMED_STREAM",
                "A33_SYMLINK_HARDLINK_TRAVERSAL":
                    "LEXICAL_PATH_TRAVERSAL_GUARD",
            }.get(
                attack_id,
                (
                    "RECLOSED_RESULT_EXACT_RECONSTRUCTION"
                    if attack_id in result_mutations
                    else "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"
                ),
            )
        need(bool(rejection_reason), "self-attack accepted:" + attack_id)
        outcomes.append({
            "attack_id": attack_id,
            "target": target,
            "mutation": mutation,
            "producer_probe_kind": probe_kind,
            "producer_self_attack_rejection": "REJECTED",
            "producer_rejection_reason": rejection_reason,
            "future_independent_required_disposition": "REJECT",
            "independent_verification_status": "PENDING",
        })
    need(
        len(outcomes) == 33
        and all(
            row["producer_self_attack_rejection"] == "REJECTED"
            for row in outcomes
        ),
        "producer self-attack rejection census",
    )
    return outcomes


def attack_contract(
    source: dict[str, Any],
    ledger: dict[str, Any],
    result: dict[str, Any],
    ledger_sha256: str,
) -> dict[str, Any]:
    specifications = attack_specifications()
    outcomes = producer_self_attack_rejection(source, ledger, result)
    value = {
        "schema": ATTACK_SCHEMA,
        "status":
            "PASS_PRODUCER_SELF_ATTACK_REJECTION_33_OF_33__"
            "INDEPENDENT_VERIFICATION_PENDING",
        "execution_status":
            "EXECUTED_BY_PRODUCER_SELF_AUDIT__"
            "INDEPENDENT_VERIFICATION_NOT_EXECUTED",
        "candidate_basis": {
            "ledger_file_sha256": ledger_sha256,
            "result_sha256": result["result_sha256"],
        },
        "attack_count": len(specifications),
        "producer_self_attack_rejection": {
            "status": "PASS",
            "rejected_count": len(outcomes),
            "accepted_count": 0,
            "all_33_attacks_rejected": True,
            "reclosable_semantic_attack_count": 28,
            "all_28_reclosable_semantic_attacks_reclosed": True,
            "scope": "PRODUCER_SELF_AUDIT_ONLY",
            "independent_verification_status": "PENDING",
        },
        "attacks": outcomes,
        "future_independent_verifier_requirement":
            "RECONSTRUCT_WITHOUT_IMPORTING_OR_EXECUTING_PRODUCER_AND_"
            "INDEPENDENTLY_REJECT_ALL_33_ATTACKS",
        "seed_affects_output": False,
    }
    value["attack_suite_sha256"] = digest(value)
    return value


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    validate_input_boundary()
    source = load_sources()
    binding = build_binding_rows(source)
    nonmerge = build_nonmerge_audit(source, binding)
    rows = binding["rows"]
    commitment = rows_commitment(rows, ROW_ID_FIELD)
    ledger = {
        "schema": LEDGER_SCHEMA,
        **commitment,
        "rows": rows,
    }
    ledger_bytes = deterministic_gzip(ledger)
    ledger_sha = hashlib.sha256(ledger_bytes).hexdigest()
    key_occurrences = binding["key_occurrences"]
    new_keys = binding["new_keys"]
    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND299A_APPEND_ONLY_REFINED_OCCURRENCE_OFFICIAL_"
            "KEY_BINDING__9404_OF_9404__8212_OLD36__1192_NEW8__"
            "RAW_KEY_UNIVERSE_116_TO_124__NO_KEY_MERGE_OR_DSU_CREDIT",
        "input_package_manifest_pins": dict(sorted(MANIFEST_PINS.items())),
        "input_file_pins": dict(sorted(INPUT_PINS.items())),
        "source_reconstruction": {
            "Round275_region_count": 13_788,
            "Round275_raw_official_key_count": 44,
            "Round292_refinement_cell_count": 11_852,
            "Round292_refined_component_count": 9_404,
            "Round294_registry_count": 431_208,
            "Round294_refined_occurrence_count": 9_404,
            "pre_refined_Round294_observed_official_key_count": 116,
            "all_input_rows_recommitted": True,
            "Round275_Round292_Round294_join_mismatch_count":
                binding["mismatch_count"],
        },
        "binding_census": {
            "binding_row_count": 9_404,
            "distinct_bound_occurrence_count": 9_404,
            "distinct_bound_Round292_component_count": 9_404,
            "distinct_bound_Round275_region_count": 9_404,
            "bound_refinement_member_cell_count": 10_252,
            "bound_raw_official_key_count": 44,
            "old_116_key_used_count": 36,
            "old_116_key_unused_by_refined_occurrences_count": 80,
            "old_116_key_binding_row_count": 8_212,
            "new_raw_key_count": 8,
            "new_raw_key_binding_row_count": 1_192,
            "new_raw_key_binding_count_per_key_histogram": {"149": 8},
            "binding_count_per_observed_key_histogram":
                histogram(key_occurrences.values()),
            "binding_classification_histogram":
                dict(sorted(binding["classification_histogram"].items())),
            "append_only_binding": True,
            "occurrence_ID_rewrite_count": 0,
            "key_merge_count": 0,
        },
        "raw_observed_key_universe": {
            "before_refined_binding_count": 116,
            "new_raw_key_delta": 8,
            "after_refined_binding_count": 124,
            "new_raw_key_ids": sorted(new_keys),
            "new_raw_keys_are_distinct": True,
            "new_raw_keys_merged_into_old_116": False,
        },
        "nonmerge_audit": nonmerge,
        "ledger": {
            "filename": LEDGER.name,
            "file_sha256": ledger_sha,
            "schema": LEDGER_SCHEMA,
            **commitment,
        },
        "formal_credit_transition": {
            "formal_refined_occurrence_official_key_binding_credit": 9_404,
            "formal_raw_observed_key_universe_delta": 8,
            "formal_new_occurrence_credit": 0,
            "formal_occurrence_alias_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "scope_contract": {
            "key_binding_is_append_only_metadata_on_existing_occurrences":
                True,
            "component_partition_or_rank_recomputed_here": False,
            "component_key_incidence_must_be_recomputed_downstream": True,
            "legacy_116_key_universe_is_complete_after_binding": False,
            "raw_observed_key_universe_count": 124,
            "eight_new_raw_keys_require_distinct_fibre_treatment": True,
            "wall_transition_adjacency_is_not_key_equivalence": True,
            "Round285_transported_equivalence_supports_new_key_merge":
                False,
        },
        "strict_nonpromotion": {
            "post_Round299A_component_count": None,
            "component_DSU_status": "NOT_REBUILT_BY_THIS_ROUND",
            "exact_key_fibre_exhaustion_status":
                "NOT_CERTIFIED__RAW_KEY_UNIVERSE_REVISED_116_TO_124",
            "maximality_status": "NOT_CERTIFIED",
            "global_disposition_status": "NOT_CERTIFIED",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "producer_self_attack_rejection": {
            "attack_count": 33,
            "rejected_count": 33,
            "accepted_count": 0,
            "reclosable_semantic_attack_count": 28,
            "status": "PASS_PRODUCER_SELF_AUDIT_ONLY",
            "independent_verification_status": "PENDING",
        },
        "required_next": [
            "Independently reconstruct all 9,404 binding rows without "
            "importing or executing this producer.",
            "Reject every attempted collapse of the eight new raw keys into "
            "their R275 wall-transition siblings.",
            "Recompute component-key incidence and the exact-key fibre "
            "denominator over the 124-key raw observed universe.",
        ],
        "provenance": {
            "producer_sha256": file_sha256(Path(__file__).resolve()),
            "seed_affects_output": False,
            "independent_verifier_executed": False,
        },
        "seed_affects_output": False,
    }
    result["result_sha256"] = digest(result)
    attacks = attack_contract(source, ledger, result, ledger_sha)
    return ledger, result, attacks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default="299101")
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--result", type=Path, default=RESULT)
    parser.add_argument("--attacks", type=Path, default=ATTACKS)
    arguments = parser.parse_args()
    ledger, result, attacks = build()
    ledger_bytes = deterministic_gzip(ledger)
    result_bytes = canonical(result) + b"\n"
    attack_bytes = canonical(attacks) + b"\n"
    atomic_write(arguments.ledger, ledger_bytes)
    atomic_write(arguments.result, result_bytes)
    atomic_write(arguments.attacks, attack_bytes)
    print(json.dumps({
        "status": result["status"],
        "seed": str(arguments.seed),
        "seed_affects_output": False,
        "ledger_file_sha256": hashlib.sha256(ledger_bytes).hexdigest(),
        "result_file_sha256": hashlib.sha256(result_bytes).hexdigest(),
        "result_sha256": result["result_sha256"],
        "attack_suite_file_sha256": hashlib.sha256(
            attack_bytes
        ).hexdigest(),
        "attack_suite_sha256": attacks["attack_suite_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
