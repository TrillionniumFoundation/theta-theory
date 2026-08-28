#!/usr/bin/env python3
"""Materialize the Round211 Jx/Jy sheet orbits and prove they are non-glue.

Jx and Jy are pinned nonidentity physical reflections.  Their exact sheet
partners certify equivariance, not two coordinate names for one physical
point.  This package therefore assigns zero physical-glue/component credit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterable


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round227_source_g_sheet_symmetry_non_glue_audit"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round227.source-g-sheet-symmetry-non-glue-audit.v1"

R173_SOURCE = "cm2_round173_source_g_exact_return_signature_transport.py"
R173_SOURCE_SHA256 = "bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f"
R173_CERT = "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
R173_CERT_SHA256 = "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a"
R173_RESULT_SHA256 = "948ab0a8539b08adc96c9493de415b44a5ffb75a1ee3ef47a4742902c211c11f"
R208_CERT = "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
R208_CERT_SHA256 = "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"
R208_RESULT_SHA256 = "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8"
R211_CERT = "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json"
R211_CERT_SHA256 = "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"
R211_RESULT_SHA256 = "3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b"


class Round227Error(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round227Error(label)


ENCODER = json.JSONEncoder(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode()


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value):
        state.update(chunk)
    return state.hexdigest()


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def closed(value: dict[str, Any]) -> dict[str, Any]:
    row = dict(value)
    row["row_sha256"] = digest(row)
    return row


def ledger(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    need(len({row[id_key] for row in rows}) == len(rows), f"unique:{id_key}")
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def regular_bytes(path: Path, maximum: int) -> bytes:
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and not path.is_symlink() and before.st_nlink == 1, f"regular:{path.name}")
    need(0 < before.st_size <= maximum, f"bounded:{path.name}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    try:
        opened = os.fstat(descriptor)
        need((opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns) == (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns), f"stable open:{path.name}")
        parts: list[bytes] = []
        size = 0
        while True:
            part = os.read(descriptor, 1024 * 1024)
            if not part:
                break
            size += len(part)
            need(size <= maximum, f"bounded read:{path.name}")
            parts.append(part)
        after = os.fstat(descriptor)
        need((after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns), f"stable read:{path.name}")
        return b"".join(parts)
    finally:
        os.close(descriptor)


def strict_json(raw: bytes) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, f"duplicate key:{key}")
            result[key] = value
        return result
    def reject(token: str) -> None:
        raise Round227Error(f"non-integral number:{token}")
    result = json.loads(raw, object_pairs_hook=pairs, parse_float=reject, parse_constant=reject)
    need(isinstance(result, dict), "JSON object")
    return result


def load_envelope(name: str, file_sha: str, result_sha: str, maximum: int) -> dict[str, Any]:
    raw = regular_bytes(HERE / name, maximum)
    need(hashlib.sha256(raw).hexdigest() == file_sha, f"file pin:{name}")
    envelope = strict_json(raw)
    need(envelope["result_sha256"] == result_sha and digest(envelope["result"]) == result_sha, f"result pin:{name}")
    return envelope["result"]


def negate(value: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return (-value[1], -value[0])


def transform_box(box: list[str], generator: str, chart: str) -> tuple[str, ...]:
    t = (Fraction(box[0]), Fraction(box[1]))
    p = (Fraction(box[2]), Fraction(box[3]))
    s = (Fraction(box[4]), Fraction(box[5]))
    cell = chart[-1]
    if generator == "Jx":
        if cell in "NS":
            t = negate(t)
        p, s = negate(p), negate(s)
    else:
        need(generator == "Jy", "generator")
        if cell in "EW":
            t = negate(t)
        p = negate(p)
    return tuple(str(item) for interval in (t, p, s) for item in interval)


def permutations() -> dict[str, list[int]]:
    source = HERE / R173_SOURCE
    need(hashlib.sha256(regular_bytes(source, 5_000_000)).hexdigest() == R173_SOURCE_SHA256, "Round173 source pin")
    specification = importlib.util.spec_from_file_location("round173_pinned_evaluator", source)
    need(specification is not None and specification.loader is not None, "Round173 import spec")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    inputs = module.load_inputs()
    tables = module.rebuild_registry(inputs["gate5"])
    result = {}
    for generator in ("Jx", "Jy"):
        row, permutation = module.generator_contract(generator, tables)
        need(row["source_G_ordinal_permutation"]["domain_count"] == 224_580, f"{generator} domain")
        result[generator] = permutation
    return result


def build(producer_sha256: str) -> dict[str, Any]:
    r173 = load_envelope(R173_CERT, R173_CERT_SHA256, R173_RESULT_SHA256, 100_000_000)
    physical_maps = {row["generator"]: row["physical_reflection"] for row in r173["exact_transport_generators"]}
    need(physical_maps == {"Jx": "(x,y,s,p)->(-x,y,-s,-p)", "Jy": "(x,y,s,p)->(x,-y,s,-p)"}, "nonidentity physical maps")
    r208 = load_envelope(R208_CERT, R208_CERT_SHA256, R208_RESULT_SHA256, 300_000_000)
    r211 = load_envelope(R211_CERT, R211_CERT_SHA256, R211_RESULT_SHA256, 250_000_000)
    geometry = {row["leaf_row_id"]: row for row in r208["formal_leaf_geometry_ledger"]["rows"]}
    signatures = {row["region_row_id"]: row for row in r208["formal_local_open_3D_signature_ledger"]["rows"]}
    sheets = r211["formal_2D_sheet_owner_ledger"]["rows"]
    need(len(geometry) == 18_324 and len(signatures) == 36_040 and len(sheets) == 17_716, "input census")
    perms = permutations()

    index: dict[tuple[int, tuple[str, ...]], dict[str, Any]] = {}
    metadata: dict[str, tuple[dict[str, Any], list[str], dict[str, Any]]] = {}
    for sheet in sheets:
        signature = signatures[sheet["owner_region_row_id"]]["local_return_signature"]
        box = geometry[sheet["leaf_row_id"]]["box"]
        key = (signature["official_key_ordinal"], tuple(box))
        need(key not in index, "unique ordinal-box sheet")
        index[key] = sheet
        metadata[sheet["sheet_row_id"]] = (signature, box, sheet)

    partners: dict[str, dict[str, str]] = {generator: {} for generator in perms}
    partner_rows: list[dict[str, Any]] = []
    active_pairs: Counter[tuple[str, str, str]] = Counter()
    owner_pairs: Counter[tuple[str, str, str]] = Counter()
    for sheet_id in sorted(metadata):
        signature, box, source_sheet = metadata[sheet_id]
        for generator in ("Jx", "Jy"):
            destination_key = (perms[generator][signature["official_key_ordinal"]], transform_box(box, generator, signature["source_chart"]))
            need(destination_key in index, f"unique exact partner:{generator}")
            destination_sheet = index[destination_key]
            destination_id = destination_sheet["sheet_row_id"]
            partners[generator][sheet_id] = destination_id
            active_pairs[(generator, source_sheet["active_factor"], destination_sheet["active_factor"])] += 1
            owner_pairs[(generator, source_sheet["owner_outgoing_cell"], destination_sheet["owner_outgoing_cell"])] += 1
            partner_rows.append(closed({
                "symmetry_partner_row_id": f"round227-symmetry-partner:{generator}:{sheet_id.split(':', 1)[1]}",
                "generator": generator,
                "source_sheet_row_id": sheet_id,
                "destination_sheet_row_id": destination_id,
                "source_official_key_ordinal": signature["official_key_ordinal"],
                "destination_official_key_ordinal": destination_key[0],
                "transformed_box_exactly_equal": True,
                "active_factor_source": source_sheet["active_factor"],
                "active_factor_destination": destination_sheet["active_factor"],
                "owner_cell_source": source_sheet["owner_outgoing_cell"],
                "owner_cell_destination": destination_sheet["owner_outgoing_cell"],
                "map_kind": "NONIDENTITY_PHYSICAL_REFLECTION",
                "same_physical_point_atlas_transition": False,
                "physical_glue_credit": 0,
                "component_union_credit": 0,
            }))

    need(all(partners[g][partners[g][sheet]] == sheet for g in partners for sheet in metadata), "involutions")
    need(all(partners[g][sheet] != sheet for g in partners for sheet in metadata), "no fixed sheets")
    need(all(partners["Jx"][partners["Jy"][sheet]] == partners["Jy"][partners["Jx"][sheet]] for sheet in metadata), "Jx/Jy commute on every sheet")
    orbit_rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for sheet_id in sorted(metadata):
        if sheet_id in seen:
            continue
        members = sorted({sheet_id, partners["Jx"][sheet_id], partners["Jy"][sheet_id], partners["Jx"][partners["Jy"][sheet_id]]})
        need(len(members) == 4, "orbit size four")
        seen.update(members)
        orbit_rows.append(closed({
            "symmetry_orbit_id": f"round227-symmetry-orbit:{digest(members)}",
            "member_sheet_row_ids": members,
            "orbit_size": 4,
            "equivariance_credit": 1,
            "physical_component_claimed": False,
            "component_union_credit": 0,
        }))
    need(len(seen) == 17_716 and len(orbit_rows) == 4_429, "orbit exhaustion")
    orbit_by_member = {member: row["symmetry_orbit_id"] for row in orbit_rows for member in row["member_sheet_row_ids"]}
    need(all(orbit_by_member[sheet] == orbit_by_member[partners[generator][sheet]] for generator in partners for sheet in metadata), "every generator edge stays in its reported orbit")
    need(digest([row["member_sheet_row_ids"] for row in orbit_rows]) == "1daabf6231863b9ed9225a647b8813b6820d9db316d00e79c38b596959ad185d", "orbit hash")

    return {
        "status": "CERTIFIED_COMPLETE_SHEET_KLEIN_EQUIVARIANCE__SYMMETRY_IS_NOT_GLUE__ZERO_COMPONENT_PROMOTION",
        "formal_input_binding": {
            "Round173_source_sha256": R173_SOURCE_SHA256, "Round173_certificate_sha256": R173_CERT_SHA256,
            "Round173_result_sha256": R173_RESULT_SHA256, "Round208_certificate_sha256": R208_CERT_SHA256,
            "Round208_result_sha256": R208_RESULT_SHA256, "Round211_certificate_sha256": R211_CERT_SHA256,
            "Round211_result_sha256": R211_RESULT_SHA256,
        },
        "formal_symmetry_partner_ledger": ledger(partner_rows, "symmetry_partner_row_id"),
        "formal_Klein_orbit_ledger": ledger(orbit_rows, "symmetry_orbit_id"),
        "census": {
            "sheet_count": 17_716, "generator_count": 2, "directed_partner_row_count": 35_432,
            "unique_partner_per_sheet_per_generator": True, "fixed_sheet_count_Jx": 0, "fixed_sheet_count_Jy": 0,
            "Klein_orbit_count": 4_429, "Klein_orbit_size_histogram": {"4": 4_429},
            "Jx_Jy_commutation_failure_count": 0, "cross_orbit_generator_edge_count": 0,
            "Klein_relations_checked_on_every_sheet": True,
            "Klein_orbit_member_rows_sha256": "1daabf6231863b9ed9225a647b8813b6820d9db316d00e79c38b596959ad185d",
            "physical_glue_credit": 0, "component_union_credit": 0,
        },
        "map_contract": {
            "Jx_physical_reflection": physical_maps["Jx"], "Jy_physical_reflection": physical_maps["Jy"],
            "both_maps_nonidentity_on_physical_space": True, "symmetry_partner_is_same_physical_point_atlas_transition": False,
            "equivariance_does_not_authorize_union_find_edge": True,
        },
        "factor_pair_histogram": {"|".join(key): value for key, value in sorted(active_pairs.items())},
        "owner_pair_histogram": {"|".join(key): value for key, value in sorted(owner_pairs.items())},
        "strict_nonpromotion": {
            "known_connectivity_blocks": 7_404, "known_connectivity_blocks_are_maximal_physical_components": False,
            "symmetry_orbits_claimed_as_physical_components": False, "component_credit": 0,
            "global_exact_key_disposition_credit": 0, "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED", "global_Gate5_fields": "10/18", "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": "construct true same-physical-point atlas overlap contracts on retained event-sheet strata; reject any edge justified only by Jx/Jy equivariance",
        "provenance": {"schema": SCHEMA, "producer_sha256": producer_sha256, "python_version": sys.version.split()[0], "Round173_pinned_evaluator_imported": True},
    }


def safe_write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(prefix=f".{OUTPUT.name}.", suffix=".tmp", dir=HERE)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--no-write", action="store_true"); args = parser.parse_args()
    producer_sha256 = hashlib.sha256(regular_bytes(Path(__file__), 5_000_000)).hexdigest()
    result = build(producer_sha256)
    envelope = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    encoded = canonical(envelope) + b"\n"
    if not args.no_write:
        safe_write(encoded)
    print(result["status"])
    print(f"producer_sha256={producer_sha256}")
    print(f"result_sha256={envelope['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(encoded).hexdigest()}")
    print("sheets=17716 directed_partners=35432 Klein_orbits=4429 orbit_size=4")
    print("symmetry_is_glue=false component_credit=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
