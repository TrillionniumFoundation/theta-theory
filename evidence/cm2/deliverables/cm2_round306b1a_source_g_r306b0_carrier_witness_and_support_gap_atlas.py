#!/usr/bin/env python3
"""Round306B1A: reconstruct carrier witnesses and explicit support gaps.

This file is deliberately a zero-credit, fail-closed census contract.  It
freezes the expected expansion of the sealed Round306B0 member universe into
carrier/representation primitives and enumerates the source closures that a
future loader must reconstruct.  No atlas row is reconstructed or certified
while ``COMPLETE_ATLAS_LOADER_INSTALLED`` is false.  In particular, an
outer/carrier box and a strict inner witness are different objects; neither is
silently promoted to the other.

The sealed Round211 2D/1D/0D owner-incidence ledgers are pinned as available
source lineage.  Their 79,084 nested typed rows are not physical components.
They also do not replace the still-missing independently evaluable analytic
definitions for 224 Round204 target sheets and 17,716 Round208 factor sheets.

Only a direct child of ``.cm2-round306b1a-private-candidates`` can be written.
Formal publication belongs to a later independent verifier.  Official keys
and return signatures are retained as metadata and are never routing filters.
"""

from __future__ import annotations

import argparse
from collections import Counter
import ctypes
from dataclasses import dataclass
import errno
from fractions import Fraction
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, BinaryIO, Callable, Iterator, TextIO


class AtlasBlocked(RuntimeError):
    """Fail-closed input, geometry, or publication contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise AtlasBlocked(label)


def discover_root(source: Path) -> Path:
    resolved = source.resolve()
    for ancestor in (resolved.parent, *resolved.parents):
        if (ancestor / "deliverables").is_dir() and (ancestor / ".venv-cm2").is_dir():
            return ancestor
    raise AtlasBlocked("workspace root not found")


ROOT = discover_root(Path(__file__))
DATA = ROOT / "deliverables"
PRIVATE_ROOT = ROOT / ".cm2-round306b1a-private-candidates"
PREFIX = "cm2_round306b1a_source_g_r306b0_carrier_witness_and_support_gap_atlas"
SCHEMA = "cm2.round306b1a.source-g-r306b0-carrier-witness-and-support-gap-atlas.v1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ENCODER = json.JSONEncoder(
    ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")
)

FILES = {
    "source": PREFIX + "_source_closure.json.gz",
    "member": PREFIX + "_member_cover.json.gz",
    "piece": PREFIX + "_representation_piece.json.gz",
    "gap": PREFIX + "_gap.json.gz",
    "result": PREFIX + "_result.json",
}
CANDIDATE_ORDER = tuple(FILES.values())
TABLES = {
    "source": "source_closure_rows",
    "member": "member_cover_rows",
    "piece": "representation_piece_rows",
    "gap": "gap_rows",
}
ID_FIELDS = {
    "source": "Round306B1A_source_closure_row_id",
    "member": "Round306B1A_member_cover_row_id",
    "piece": "Round306B1A_representation_piece_row_id",
    "gap": "Round306B1A_gap_row_id",
}

# Every consumed byte source is pinned.  Candidate mode re-hashes before
# opening and re-checks at the final admission boundary.
INPUT_PINS = {
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256":
        "9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269",
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz":
        "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af",
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json":
        "badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735",
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json":
        "f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz":
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz":
        "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz":
        "5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f",
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz":
        "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    "cm2_round290_source_g_isolated_atom_inner_support_closure_inner_support_ledger.json.gz":
        "9c2a596f3b981d24baa039e02c72e5270889d145dc146963532f3dedebc94025",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz":
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json":
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round211_source_g_outgoing_half_open_owner_materialization_manifest.sha256":
        "c0cf8b70de6dd147fd1009c97d28549ec4571f9d6c82b8bf46dba023e3fe943c",
    "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json":
        "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f",
    "cm2_round211_source_g_outgoing_half_open_owner_materialization_verification.json":
        "1dee3afbe5cc04829ef5546ef16f8ef76b6d9a32f7bd1aab61037066419ad2f9",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":
        "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json":
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json":
        "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1",
    "cm2_round246_source_g_whole_signature_retained_quotient_certificate.json":
        "a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9",
    "cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json":
        "72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7",
    "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json":
        "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
}

ROUND211_EXPECTED = {
    "manifest": {
        "filename":
            "cm2_round211_source_g_outgoing_half_open_owner_materialization_manifest.sha256",
        "file_sha256":
            "c0cf8b70de6dd147fd1009c97d28549ec4571f9d6c82b8bf46dba023e3fe943c",
    },
    "certificate": {
        "filename":
            "cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json",
        "file_sha256":
            "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f",
        "schema":
            "cm2.round211.source-g-outgoing-half-open-owner-materialization.v1",
        "result_sha256":
            "3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b",
    },
    "verification": {
        "filename":
            "cm2_round211_source_g_outgoing_half_open_owner_materialization_verification.json",
        "file_sha256":
            "1dee3afbe5cc04829ef5546ef16f8ef76b6d9a32f7bd1aab61037066419ad2f9",
        "schema":
            "cm2.round211.source-g-outgoing-half-open-owner-materialization.verification.v1",
        "verification_result_sha256":
            "eed5687f736c6244421ec432a4d1fc283d84386147293825a19837173cbb819d",
    },
    "typed_source_lineage_ledgers": {
        "formal_2D_sheet_owner_ledger": {
            "id_field": "sheet_row_id",
            "row_count": 17_716,
            "row_ids_sha256":
                "bb25748d3c7bc46043f9588983788ecc3cb4a38faa8d40c6ea13383c262570aa",
            "row_hashes_sha256":
                "97e1b400d0df06228239f5bda23051cdae8b0b0caa1be0fdb64d8b4bc5527c7e",
            "rows_sha256":
                "ed26068a92d4ed74f54cd724680da5bc9cafa811d553415380999ae69ea7fdeb",
        },
        "formal_1D_curve_incidence_owner_ledger": {
            "id_field": "curve_row_id",
            "row_count": 20_456,
            "row_ids_sha256":
                "c604ff7fee7d12c7bb39f5f670848f673e1afa0a44b9fad75d829f264e8fbb71",
            "row_hashes_sha256":
                "a9d68f724a257ae768657dff51767207277a9fff6eebd345d539434789b88270",
            "rows_sha256":
                "3d93dd7860c1025bb68acf3568a0b4b66e3106189776aae4bafa12d3902a8522",
        },
        "formal_0D_endpoint_incidence_owner_ledger": {
            "id_field": "endpoint_row_id",
            "row_count": 40_912,
            "row_ids_sha256":
                "de9c48038c7da03671941bd713b9f393a4a5a5b89a0dc53f76bd418a8cd13ed8",
            "row_hashes_sha256":
                "dd9b72a5e03904dcf649a54e5828aa1e3fa41aa6f453b88a32f7b2abd3005e39",
            "rows_sha256":
                "e5466d386b45ea8ab473a8483b5a90a244592491cdb9ecbcdf01b7a40c87d712",
        },
    },
}

EXPECTED = {
    "member_count": 564_492,
    "occurrence_count": 431_208,
    "preserved_occurrence_count": 126_468,
    "preserved_R174_whole_rational_box_count": 72_500,
    "preserved_R179_whole_rational_box_count": 17_192,
    "preserved_R204_curved_sign_cell_count": 736,
    "preserved_R208_factorized_sign_cell_count": 36_040,
    "preserved_unique_outer_envelope_count": 108_528,
    "R204_unique_leaf_outer_envelope_count": 512,
    "R208_unique_leaf_outer_envelope_count": 18_324,
    "Round211_2D_sheet_owner_source_lineage_count": 17_716,
    "Round211_1D_curve_incidence_source_lineage_count": 20_456,
    "Round211_0D_endpoint_incidence_source_lineage_count": 40_912,
    "Round211_typed_source_lineage_count": 79_084,
    "R204_target_sheet_analytic_definition_root_gap_count": 224,
    "R204_target_graph_1D_dependent_incidence_count": 504,
    "R204_target_graph_0D_dependent_incidence_count": 280,
    "R204_target_graph_dependent_incidence_count": 784,
    "R208_factor_sheet_analytic_definition_root_gap_count": 17_716,
    "R208_curve_dependent_incidence_count": 20_456,
    "R208_endpoint_dependent_incidence_count": 40_912,
    "R208_dependent_incidence_count": 61_368,
    "preserved_analytic_definition_independent_root_gap_count": 17_940,
    "preserved_analytic_definition_dependent_incidence_count": 62_152,
    "R288_occurrence_count": 295_336,
    "R292_occurrence_count": 9_404,
    "virtual_positive_3D_count": 94_660,
    "virtual_R245_positive_3D_count": 6_124,
    "virtual_R248_positive_3D_count": 88_536,
    "sheet_count": 38_624,
    "R245_sheet_count": 264,
    "R248_sheet_count": 38_360,
    "occurrence_primitive_count": 478_620,
    "TPS_occurrence_primitive_count": 466_768,
    "T2PS_occurrence_primitive_count": 11_852,
    "virtual_positive_3D_carrier_count": 94_660,
    "sheet_carrier_count": 38_624,
    "positive_3D_carrier_count": 573_280,
    "carrier_count": 611_904,
    "primary_member_representation_count": 564_492,
    "extra_refined_primary_cell_count": 848,
    "alias_representation_count": 46_564,
    "extra_representation_count": 47_412,
    "graph_side_positive_3D_embedding_gap_count": 76_304,
    "sheet_graph_embedding_gap_count": 38_624,
    "graph_definition_gap_count": 38_624,
    "physical_incidence_gap_count": 115_472,
    "R288_atom_support_predicate_cell_gap_count": 295_340,
}

# Deliberately false until every loader/join listed by ``contract()`` is
# implemented and independently count-audited.  Candidate mode checks this
# before hashing or opening any large input.
COMPLETE_ATLAS_LOADER_INSTALLED = False

TRANCHES = {
    "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
    "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
    "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT": 9_404,
    "INHERITED_ROUND247_VIRTUAL_STRATUM": 6_388,
    "ROUND248_WALL_BULK": 88_536,
    "ROUND248_WALL_SHEET": 38_360,
}


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in payload, "row is open")
    return {**payload, "row_sha256": digest(payload)}


def check_row(row: dict[str, Any], label: str) -> None:
    need(type(row) is dict and type(row.get("row_sha256")) is str, label + ":closed")
    payload = dict(row)
    claimed = payload.pop("row_sha256")
    need(claimed == digest(payload), label + ":row SHA")


def file_sha256(path: Path, limit: int | None = None) -> str:
    info = os.lstat(path)
    need(stat.S_ISREG(info.st_mode) and not path.is_symlink(), "regular source:" + path.name)
    need(limit is None or info.st_size <= limit, "source size bound:" + path.name)
    state = hashlib.sha256()
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            state.update(block)
        after = os.fstat(descriptor)
        need(
            (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
            "stable source fd:" + path.name,
        )
    finally:
        os.close(descriptor)
    return state.hexdigest()


def verify_input_pins() -> None:
    for name, expected in INPUT_PINS.items():
        need(file_sha256(DATA / name) == expected, "input byte pin:" + name)


class ListHash:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        self.state.update(canonical(value))
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


class RowSpool:
    def __init__(self, kind: str) -> None:
        need(kind in ID_FIELDS, "known spool kind")
        self.kind = kind
        self.id_field = ID_FIELDS[kind]
        self.stream = tempfile.TemporaryFile(mode="w+b")
        self.rows, self.ids, self.hashes = ListHash(), ListHash(), ListHash()
        self.seen: set[str] = set()

    def add(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = close_row(payload)
        row_id = row.get(self.id_field)
        need(type(row_id) is str and row_id not in self.seen, "unique spool row ID")
        self.seen.add(row_id)
        if self.rows.count:
            self.stream.write(b",")
        self.stream.write(canonical(row))
        self.rows.add(row)
        self.ids.add(row_id)
        self.hashes.add(row["row_sha256"])
        return row

    def metadata(self) -> dict[str, Any]:
        return {
            "row_count": self.rows.count,
            "row_ids_sha256": self.ids.finish(),
            "row_hashes_sha256": self.hashes.finish(),
            "rows_sha256": self.rows.finish(),
        }

    def close(self) -> None:
        self.stream.close()


def iter_array(stream: TextIO, marker: str, initial: str = "") -> Iterator[dict[str, Any]]:
    """Stream one object array without materialising a multi-gigabyte envelope."""

    buffer = initial
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing array marker:" + marker)
        buffer += block
    buffer = buffer.split(marker, 1)[1]

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in out, "duplicate JSON key:" + key)
            out[key] = value
        return out

    decoder = json.JSONDecoder(
        object_pairs_hook=unique,
        parse_float=lambda value: (_ for _ in ()).throw(AtlasBlocked("float:" + value)),
        parse_constant=lambda value: (_ for _ in ()).throw(AtlasBlocked("constant:" + value)),
    )
    comma_allowed = False
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated streamed array")
            buffer = block
            continue
        if buffer[0] == "]":
            return
        if comma_allowed:
            need(buffer[0] == ",", "missing streamed comma")
            buffer = buffer[1:].lstrip()
            need(bool(buffer) or bool(stream.read(0)), "stream state")
        else:
            need(buffer[0] != ",", "leading streamed comma")
        while True:
            try:
                row, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated streamed row")
                buffer += block
        need(type(row) is dict, "streamed row object")
        yield row
        buffer = buffer[end:]
        comma_allowed = True


def open_rows(name: str, marker: str, *, compressed: bool) -> Iterator[dict[str, Any]]:
    raw: BinaryIO = open(DATA / name, "rb")
    binary: BinaryIO = gzip.GzipFile(fileobj=raw, mode="rb") if compressed else raw
    text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
    try:
        yield from iter_array(text, marker)
    finally:
        try:
            text.detach()
        except Exception:
            pass
        if compressed:
            binary.close()
        raw.close()


def positive_box(box: Any, dimension: int, label: str) -> None:
    need(type(box) is list and len(box) == 2 * dimension, label + ":box arity")
    for axis in range(dimension):
        need(Fraction(box[2 * axis]) < Fraction(box[2 * axis + 1]), label + ":positive axis")


def arithmetic_contract() -> None:
    need(sum(TRANCHES.values()) == EXPECTED["member_count"], "member tranche sum")
    need(126_468 + 295_336 + 9_404 == EXPECTED["occurrence_count"], "occurrence tranches")
    need(
        72_500 + 17_192 + 736 + 36_040
        == EXPECTED["preserved_occurrence_count"],
        "preserved occurrence historical source partition",
    )
    need(
        72_500 + 17_192 + 512 + 18_324
        == EXPECTED["preserved_unique_outer_envelope_count"],
        "preserved unique outer-envelope source partition",
    )
    need(
        288 + 2 * 224 == EXPECTED["preserved_R204_curved_sign_cell_count"]
        and 288 + 224 == EXPECTED["R204_unique_leaf_outer_envelope_count"],
        "R204 one-region and two-region leaf-envelope partition",
    )
    need(
        608 + 2 * 17_716 == EXPECTED["preserved_R208_factorized_sign_cell_count"]
        and 608 + 17_716 == EXPECTED["R208_unique_leaf_outer_envelope_count"],
        "R208 empty and two-sign-region leaf-envelope partition",
    )
    need(
        17_716 + 20_456 + 40_912
        == EXPECTED["Round211_typed_source_lineage_count"]
        and 40_912 == 2 * 20_456,
        "Round211 nested typed source-lineage census",
    )
    need(
        [
            item["row_count"]
            for item in ROUND211_EXPECTED["typed_source_lineage_ledgers"].values()
        ]
        == [
            EXPECTED["Round211_2D_sheet_owner_source_lineage_count"],
            EXPECTED["Round211_1D_curve_incidence_source_lineage_count"],
            EXPECTED["Round211_0D_endpoint_incidence_source_lineage_count"],
        ],
        "Round211 ledger commitments match typed source-lineage census",
    )
    need(
        224 + 17_716
        == EXPECTED["preserved_analytic_definition_independent_root_gap_count"],
        "preserved independent analytic-definition root gaps",
    )
    need(
        504 + 280 == EXPECTED["R204_target_graph_dependent_incidence_count"]
        and 20_456 + 40_912 == EXPECTED["R208_dependent_incidence_count"]
        and 784 + 61_368
        == EXPECTED["preserved_analytic_definition_dependent_incidence_count"],
        "preserved analytic-definition dependent incidences",
    )
    need(6_124 + 88_536 == EXPECTED["virtual_positive_3D_count"], "virtual 3D tranches")
    need(264 + 38_360 == EXPECTED["sheet_count"], "sheet tranches")
    need(6_124 + 264 == TRANCHES["INHERITED_ROUND247_VIRTUAL_STRATUM"], "inherited virtual dimension split")
    need(
        431_208 + 94_660 + 38_624 == EXPECTED["member_count"],
        "occurrence plus virtual member census",
    )
    need(
        EXPECTED["primary_member_representation_count"] == EXPECTED["member_count"],
        "one primary representation per member",
    )
    need(466_768 + 11_852 == EXPECTED["occurrence_primitive_count"], "primitive coordinate systems")
    need(
        431_208 + 848 + 46_564 == EXPECTED["occurrence_primitive_count"],
        "occurrence primary plus refined and alias representations",
    )
    need(46_288 + 276 == EXPECTED["alias_representation_count"], "alias source tranches")
    need(10_252 + 1_600 == EXPECTED["T2PS_occurrence_primitive_count"], "T2PS cell tranches")
    need(478_620 + 94_660 == EXPECTED["positive_3D_carrier_count"], "3D carrier sum")
    need(573_280 + 38_624 == EXPECTED["carrier_count"], "all carrier sum")
    need(848 + 46_564 == EXPECTED["extra_representation_count"], "extra representation sum")
    need(564_492 + 47_412 == EXPECTED["carrier_count"], "member plus extra carrier sum")
    need(
        EXPECTED["graph_definition_gap_count"] == EXPECTED["sheet_count"],
        "one graph definition per sheet",
    )
    need(
        EXPECTED["R288_atom_support_predicate_cell_gap_count"]
        == EXPECTED["R288_occurrence_count"] + 4,
        "R288 predicate cells include four artificial split aliases",
    )
    need(
        EXPECTED["graph_side_positive_3D_embedding_gap_count"] == 76_256 + 48,
        "R248 graph-side 3D carrier split",
    )
    need(
        EXPECTED["physical_incidence_gap_count"] == 792 + 114_584 + 96,
        "graph-feature incidence split",
    )


def contract() -> dict[str, Any]:
    return {
        "schema": SCHEMA + ".contract.v1",
        "status": (
            "BLOCKED_FAIL_CLOSED_CENSUS_CONTRACT_DIAGNOSTIC__"
            "COMPLETE_ATLAS_LOADER_NOT_INSTALLED__NO_CANDIDATE_EMISSION"
        ),
        "sealed_Round306B0_manifest_sha256": INPUT_PINS[
            "cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256"
        ],
        "exact_Round306B0_identity_tranches": dict(TRANCHES),
        "derived_inherited_virtual_dimension_split": {
            "INHERITED_ROUND247_VIRTUAL_STRATUM__positive_3D": 6_124,
            "INHERITED_ROUND247_VIRTUAL_STRATUM__sheet_2D": 264,
        },
        "preserved_occurrence_exact_source_partition": {
            "ROUND174_RESOLVED__whole_rational_box": 72_500,
            "ROUND179_RESOLVED__whole_rational_box": 17_192,
            "ROUND204_REGION__curved_sign_cell": 736,
            "ROUND208_REGION__factorized_sign_cell": 36_040,
            "total": 126_468,
        },
        "preserved_occurrence_outer_envelope_census": {
            "R174_occurrence_boxes": 72_500,
            "R179_occurrence_boxes": 17_192,
            "R204_unique_leaf_outer_envelopes": 512,
            "R204_regions_on_leaf_outer_envelopes": "736=288+2*224",
            "R208_unique_leaf_outer_envelopes": 18_324,
            "R208_regions_on_leaf_outer_envelopes": "36040=608+2*17716",
            "unique_source_outer_envelope_count": 108_528,
            "outer_envelope_count_is_not_normalized_support_count": True,
        },
        "exact_representation_census": {
            key: EXPECTED[key]
            for key in (
                "occurrence_primitive_count",
                "TPS_occurrence_primitive_count",
                "T2PS_occurrence_primitive_count",
                "virtual_positive_3D_carrier_count",
                "sheet_carrier_count",
                "positive_3D_carrier_count",
                "carrier_count",
                "primary_member_representation_count",
                "extra_refined_primary_cell_count",
                "alias_representation_count",
                "extra_representation_count",
            )
        },
        "semantic_separation": {
            "representation_piece_is_not_member_identity": True,
            "outer_envelope_is_not_inner_witness": True,
            "carrier_or_parent_box_is_not_normalized_full_graph_support": True,
            "R174_R179_rational_box_is_coordinate_local_support_only": True,
            "R204_R208_outer_leaf_box_is_not_curved_region_support": True,
            "R288_inner_support_witness_is_not_full_atom_support": True,
            "physical_incidence_requires_a_separate_witness": True,
            "alias_does_not_issue_or_union_member_identity": True,
            "Round211_typed_owner_or_incidence_row_is_not_a_component": True,
            "nested_incidence_rows_are_not_independent_analytic_root_gaps": True,
        },
        "routing_contract": {
            "official_key_is_metadata_only": True,
            "return_signature_is_metadata_only": True,
            "cross_official_key_incidence_must_remain_admissible": True,
            "transition_atlas_complete": False,
            "transition_atlas_gap_must_be_explicit": True,
        },
        "known_finite_graph_definition_blockers": {
            "R248_graph_side_positive_3D_carriers": 76_304,
            "sheet_carriers": 38_624,
            "source_free_graph_definition_gaps": 38_624,
            "physical_incidence_gaps": 115_472,
            "R288_atom_support_predicate_cell_gaps": 295_340,
            "R245_sheet_requires_R242_owner_and_shadow_edge_join": True,
            "parent_or_carrier_box_may_not_be_claimed_as_full_normalized_support": True,
        },
        "pinned_Round211_local_dimensional_owner_source_lineage": {
            **ROUND211_EXPECTED,
            "typed_row_count": 79_084,
            "typed_rows_are_pairwise_disjoint_by_row_type_and_row_ID": True,
            "incidence_hierarchy": "17716_sheets__20456_curves__40912_endpoints",
            "endpoint_identity": "40912=2*20456",
            "nested_geometry_not_independent_components": True,
            "upstream_local_dimensional_owner_credit_is_source_evidence_only": True,
            "Round306B1A_new_component_or_support_credit": 0,
        },
        "preserved_occurrence_remaining_analytic_definition_gaps": {
            "independent_root_gap_count": 17_940,
            "root_gaps": {
                "R204_target_regular_graph_sheet_definition_instances": 224,
                "R208_factor_sheet_definition_instances": 17_716,
            },
            "dependent_incidence_count": 62_152,
            "dependent_incidences": {
                "R204_target_graph_1D_curves": 504,
                "R204_target_graph_0D_points": 280,
                "R208_curve_incidences": 20_456,
                "R208_endpoint_incidences": 40_912,
            },
            "dependencies_are_not_double_counted_as_independent_roots": True,
            "factor_or_graph_label_without_evaluable_formula_is_not_a_definition": True,
            "complete_source_free_normalized_support": False,
            "formal_credit": 0,
        },
        "implementation_closure_required_before_candidate_mode": [
            {
                "block": "PRESERVED_OCCURRENCE_IDENTITY_ENVELOPE_AND_SIGNATURE_SOURCE_FREEZE",
                "required": (
                    "byte-pinned row-exact B0->Round294->Round266->historical "
                    "source joins for all 126468 identities, exact outer envelopes, "
                    "and complete 10-field return signatures; R174/R179 rational "
                    "boxes are coordinate-local supports while R204/R208 leaf boxes "
                    "remain outer envelopes and may not be called normalized support"
                ),
                "expected_member_count": 126_468,
                "exact_source_partition": "72500+17192+736+36040",
                "unique_outer_envelope_count": 108_528,
                "normalized_full_support_complete": False,
            },
            {
                "block": "ROUND211_TYPED_LOCAL_DIMENSIONAL_OWNER_SOURCE_LINEAGE",
                "required": (
                    "independently scan and row-close the pinned 17716 sheet, 20456 "
                    "curve-incidence, and 40912 endpoint-incidence rows; preserve "
                    "their sheet->curve->endpoint and R208 owner/shadow joins without "
                    "issuing any B1A support, component, or deduplication credit"
                ),
                "typed_source_lineage_count": 79_084,
                "source_lineage_data_available": True,
                "component_count_claimed": 0,
            },
            {
                "block": "PRESERVED_CURVED_ANALYTIC_SUPPORT_DEFINITIONS",
                "required": (
                    "materialize independently evaluable normalized predicates for "
                    "224 R204 target sheets and 17716 R208 factor sheets; factor "
                    "names, proof-method strings, producer hashes, and leaf boxes "
                    "alone are insufficient"
                ),
                "independent_root_gap_count": 17_940,
                "dependent_incidence_count": 62_152,
                "dependencies_must_not_be_counted_as_additional_roots": True,
            },
            {
                "block": "ROUND288_ATOM_SUPPORT",
                "required": (
                    "separate 295336 strict inner witnesses from the complete "
                    "295340 Round269-Round272 predicate-cell support definition"
                ),
                "inner_witness_count": 295_336,
                "predicate_cell_gap_count": 295_340,
            },
            {
                "block": "ROUND292_TRANSFORMED_CELLS",
                "required": (
                    "materialize all 11852 exact (t^2,p,s) cells, including 10252 "
                    "new-component cells and 1600 occupied alias cells"
                ),
                "expected_cell_count": 11_852,
            },
            {
                "block": "REPRESENTATION_ALIASES",
                "required": (
                    "join all 46288 Round294 representation bindings and all 276 "
                    "Round295A same-origin continuation aliases to current members"
                ),
                "expected_alias_count": 46_564,
            },
            {
                "block": "VIRTUAL_CARRIER_AND_PARENT_BOXES",
                "required": (
                    "reconstruct 94660 positive-3D and 38624 sheet carriers from "
                    "their full Round179/Round220/Round245-Round248 carrier lineage; "
                    "strict inner witnesses may not stand in for the carrier"
                ),
                "expected_virtual_count": 133_284,
            },
            {
                "block": "GRAPH_DEFINITION_AND_INCIDENCE",
                "required": (
                    "source-free graph definitions for 38624 sheets, physical "
                    "incidence closure for 115472 cases, and the two-edge Round242 "
                    "owner/shadow join for every inherited Round245 sheet"
                ),
                "graph_definition_gap_count": 38_624,
                "physical_incidence_gap_count": 115_472,
            },
            {
                "block": "TRANSITION_ATLAS",
                "required": (
                    "lossless cross-chart/transformed-face/event/sheet transition "
                    "routing without official-key or signature filtering"
                ),
                "complete": False,
            },
        ],
        "complete_atlas_loader_installed": COMPLETE_ATLAS_LOADER_INSTALLED,
        "candidate_mode_opens_large_sources_when_blocked": False,
        "candidate_mode_writes_any_file_when_blocked": False,
        "candidate_files": list(CANDIDATE_ORDER),
        "dedicated_private_candidate_root": PRIVATE_ROOT.name,
        "formal_credit": {
            "Round211_source_lineage_admission": 0,
            "preserved_analytic_definition": 0,
            "carrier_witness_atlas": 0,
            "full_support_cover": 0,
            "maximality": 0,
            "fibre": 0,
            "global_disposition": 0,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def self_test() -> dict[str, Any]:
    arithmetic_contract()
    sample = close_row({"schema": SCHEMA + ".self-test-row.v1", "value": 1})
    check_row(sample, "self-test")
    positive_box(["0", "1", "-1/2", "1/2", "2", "3"], 3, "self-test")
    need(all(HEX64.fullmatch(value) is not None for value in INPUT_PINS.values()), "pin syntax")
    for artifact in ("manifest", "certificate", "verification"):
        item = ROUND211_EXPECTED[artifact]
        need(
            INPUT_PINS[item["filename"]] == item["file_sha256"],
            "Round211 source file pin:" + artifact,
        )
    need(
        HEX64.fullmatch(ROUND211_EXPECTED["certificate"]["result_sha256"])
        is not None
        and HEX64.fullmatch(
            ROUND211_EXPECTED["verification"]["verification_result_sha256"]
        )
        is not None,
        "Round211 result pin syntax",
    )
    for table, item in ROUND211_EXPECTED["typed_source_lineage_ledgers"].items():
        need(
            item["row_count"] > 0
            and all(
                HEX64.fullmatch(item[field]) is not None
                for field in ("row_ids_sha256", "row_hashes_sha256", "rows_sha256")
            ),
            "Round211 ledger commitment syntax:" + table,
        )
    probe = contract()
    need(
        probe["formal_credit"]["carrier_witness_atlas"] == 0
        and probe["formal_credit"]["Round211_source_lineage_admission"] == 0
        and probe["formal_credit"]["preserved_analytic_definition"] == 0
        and probe["formal_credit"]["maximality"] == 0
        and probe["routing_contract"]["official_key_is_metadata_only"] is True
        and probe["known_finite_graph_definition_blockers"][
            "R248_graph_side_positive_3D_carriers"
        ] == 76_304
        and probe["pinned_Round211_local_dimensional_owner_source_lineage"][
            "typed_row_count"
        ] == 79_084
        and probe["pinned_Round211_local_dimensional_owner_source_lineage"][
            "nested_geometry_not_independent_components"
        ] is True
        and probe["preserved_occurrence_remaining_analytic_definition_gaps"][
            "independent_root_gap_count"
        ] == 17_940
        and probe["preserved_occurrence_remaining_analytic_definition_gaps"][
            "dependent_incidence_count"
        ] == 62_152
        and probe["preserved_occurrence_remaining_analytic_definition_gaps"][
            "dependencies_are_not_double_counted_as_independent_roots"
        ] is True
        and probe["complete_atlas_loader_installed"] is False
        and probe["candidate_mode_opens_large_sources_when_blocked"] is False,
        "zero-credit and gap boundary",
    )
    return {
        "schema": SCHEMA + ".self-test.v1",
        "status": (
            "PASS_ROUND306B1A_LIGHTWEIGHT_FAIL_CLOSED_DIAGNOSTIC_SELF_TEST__"
            "CANDIDATE_MODE_BLOCKED"
        ),
        "large_source_opened": False,
        "candidate_written": False,
        "arithmetic_contract": True,
        "source_pin_syntax_count": len(INPUT_PINS),
        "Round211_manifest_certificate_verification_pins_checked": True,
        "Round211_typed_source_lineage_commitments_checked": 3,
        "Round211_typed_source_lineage_count": 79_084,
        "Round211_typed_source_lineage_is_not_component_count": True,
        "preserved_analytic_definition_independent_root_gap_count": 17_940,
        "preserved_analytic_definition_dependent_incidence_count": 62_152,
        "dependent_incidences_not_double_counted_as_roots": True,
        "semantic_separation_checked": True,
        "official_key_filter_rejected_by_contract": True,
        "finite_graph_definition_gaps_explicit": True,
        "R288_predicate_cell_gap_explicit": True,
        "formal_maximality_credit": 0,
    }


def ledger_envelope(kind: str, spool: RowSpool) -> dict[str, Any]:
    meta = spool.metadata()
    payload = {
        "schema": SCHEMA + "." + kind + "-ledger.v1",
        "status": "ZERO_CREDIT_SUPPORT_PREIMAGE_ATLAS_CANDIDATE",
        "formal_credit": {"maximality": 0, "fibre": 0, "global_disposition": 0},
        **meta,
    }
    return {**payload, "ledger_sha256": digest(payload)}


def emit_ledger(path: Path, kind: str, spool: RowSpool) -> dict[str, Any]:
    envelope = ledger_envelope(kind, spool)
    spool.stream.flush()
    spool.stream.seek(0)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    raw = os.fdopen(descriptor, "wb", closefd=True)
    state = hashlib.sha256()

    class Sink:
        def write(self, block: bytes) -> int:
            state.update(block)
            return raw.write(block)

        def flush(self) -> None:
            raw.flush()

    prefix = canonical(envelope)[:-1] + b',"' + TABLES[kind].encode("ascii") + b'":['
    try:
        with gzip.GzipFile(fileobj=Sink(), mode="wb", filename="", mtime=0, compresslevel=9) as zipped:
            zipped.write(prefix)
            while True:
                block = spool.stream.read(1 << 20)
                if not block:
                    break
                zipped.write(block)
            zipped.write(b"]}")
        raw.flush()
        os.fsync(raw.fileno())
    finally:
        raw.close()
    return {
        "filename": path.name,
        "file_sha256": state.hexdigest(),
        "ledger_sha256": envelope["ledger_sha256"],
        **spool.metadata(),
    }


def exclusive_bytes(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        offset = 0
        while offset < len(raw):
            offset += os.write(descriptor, raw[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def rename_noreplace(old_fd: int, old_name: str, new_fd: int, new_name: str) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameat2", None)
    need(function is not None, "renameat2 required")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    if function(old_fd, os.fsencode(old_name), new_fd, os.fsencode(new_name), 1) != 0:
        code = ctypes.get_errno()
        if code == errno.EEXIST:
            raise FileExistsError(code, os.strerror(code), new_name)
        raise OSError(code, os.strerror(code), new_name)


def create_stage(candidate: Path) -> tuple[Path, int, int]:
    if not os.path.lexists(PRIVATE_ROOT):
        os.mkdir(PRIVATE_ROOT, 0o700)
    info = os.lstat(PRIVATE_ROOT)
    need(stat.S_ISDIR(info.st_mode) and not PRIVATE_ROOT.is_symlink(), "private root directory")
    need(stat.S_IMODE(info.st_mode) == 0o700, "private root mode")
    absolute = Path(os.path.abspath(os.fspath(candidate)))
    need(absolute.parent == PRIVATE_ROOT and absolute.name not in {"", ".", ".."}, "direct private child")
    need(not os.path.lexists(absolute), "candidate target absent")
    root_fd = os.open(PRIVATE_ROOT, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
    stage_name = "." + absolute.name + ".stage." + digest([os.getpid(), absolute.name])[:24]
    os.mkdir(stage_name, 0o700, dir_fd=root_fd)
    stage_fd = os.open(stage_name, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0), dir_fd=root_fd)
    return PRIVATE_ROOT / stage_name, root_fd, stage_fd


def build_spools() -> tuple[dict[str, RowSpool], dict[str, Any]]:
    """Future heavy reconstruction entry point; no loader is installed now.

    Before candidate mode can ever be enabled, an audited loader must populate
    every carrier row, keep unavailable graph embeddings as explicit gaps, and
    reject all count drift or carrier/full-support conflation.
    """

    # Fail closed rather than emitting a partial atlas until that future
    # implementation is installed and independently audited.
    need("_build_complete_atlas" in globals(), "complete atlas loader installed")
    return globals()["_build_complete_atlas"]()


def result_payload(producer_sha256: str, meta: dict[str, Any], audit: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema": SCHEMA,
        "status": (
            "UNREACHABLE_UNTIL_COMPLETE_ATLAS_LOADER_IS_INSTALLED_AND_AUDITED__"
            "ZERO_CREDIT"
        ),
        "producer_file_sha256": producer_sha256,
        "sealed_Round306B0_manifest_sha256": INPUT_PINS[
            "cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256"
        ],
        "exact_expected": dict(EXPECTED),
        "reconstruction_audit": audit,
        "output_ledgers": meta,
        "strict_boundary": {
            "Round211_typed_source_lineage_rows_pinned": 79_084,
            "Round211_typed_source_lineage_rows_are_not_components": True,
            "preserved_analytic_definition_independent_root_gaps": 17_940,
            "preserved_analytic_definition_dependent_incidences": 62_152,
            "dependent_incidences_counted_as_independent_roots": False,
            "complete_source_free_preserved_normalized_support": False,
            "carrier_witness_complete": False,
            "full_support_cover_complete": False,
            "carrier_cover_is_not_full_transition_atlas": True,
            "outer_envelope_used_as_inner_witness": False,
            "parent_box_claimed_as_normalized_graph_support": False,
            "official_key_used_as_filter": False,
            "complete_transition_atlas_proved": False,
            "full_maximality_proved": False,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "candidate_is_formal": False,
    }
    return {**payload, "result_sha256": digest(payload)}


def build_private_candidate(candidate: Path) -> dict[str, Any]:
    need(
        COMPLETE_ATLAS_LOADER_INSTALLED,
        "candidate mode blocked before large-input open or output write: "
        "complete atlas loader is not installed",
    )
    verify_input_pins()
    spools, audit = build_spools()
    stage, root_fd, stage_fd = create_stage(candidate)
    try:
        meta: dict[str, Any] = {}
        for kind in ("source", "member", "piece", "gap"):
            meta[kind] = emit_ledger(stage / FILES[kind], kind, spools[kind])
            os.fsync(stage_fd)
        producer_sha = file_sha256(DATA / (PREFIX + ".py"), 3_000_000)
        result = result_payload(producer_sha, meta, audit)
        raw = canonical(result)
        exclusive_bytes(stage / FILES["result"], raw)
        os.fsync(stage_fd)
        need(set(os.listdir(stage_fd)) == set(CANDIDATE_ORDER), "exact candidate files")
        verify_input_pins()
        rename_noreplace(root_fd, stage.name, root_fd, Path(candidate).name)
        os.fsync(root_fd)
        return {
            "status": "PASS_ROUND306B1A_PRIVATE_ZERO_CREDIT_CANDIDATE_WRITTEN",
            "candidate_directory": str(PRIVATE_ROOT / Path(candidate).name),
            "result_sha256": result["result_sha256"],
            "output_file_sha256s": {item["filename"]: item["file_sha256"] for item in meta.values()},
            "formal_maximality_credit": 0,
            "formal_artifact_written": False,
        }
    finally:
        for spool in spools.values():
            spool.close()
        os.close(stage_fd)
        os.close(root_fd)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    args = parser.parse_args()
    need(sum((args.print_contract, args.self_test, args.candidate_dir is not None)) == 1, "choose one mode")
    if args.print_contract:
        print(canonical(contract()).decode("ascii"))
    elif args.self_test:
        print(canonical(self_test()).decode("ascii"))
    else:
        assert args.candidate_dir is not None
        print(canonical(build_private_candidate(args.candidate_dir)).decode("ascii"))


if __name__ == "__main__":
    main()
