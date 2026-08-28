#!/usr/bin/env python3
"""Hardened local owner/lineage authority producer for the Round209 lane.

This replacement does not promote the Round195 feasibility probe.  Formal
authority comes only from the pinned Round173 seam contract and the pinned,
independently verified Round208 formal leaf/region/U|U rows.  Round209 is a
producer-side frozen evaluator and Round195 is provenance-only.

The three output ledgers are local dimensional incidences.  They are not
whole leaves, origins, tubes, physical/global components, or exact-key
dispositions.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import types
from typing import Any, Iterable


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round306b1af4k2r209_source_g_outgoing_half_open_owner_lineage"
SCHEMA = "cm2.round306b1af4k2r209.source-g-outgoing-half-open-owner-lineage.v1"
STATUS = (
    "SEALED_LOCAL_SOURCE_G_OUTGOING_W_HALF_OPEN_OWNER_LINEAGE_AUTHORITY__"
    "NO_WHOLE_LEAF_OR_GLOBAL_PROMOTION"
)
ROW_CAP = 8 * 1024 * 1024
MAX_INPUT = 300 * 1024 * 1024
EXPECTED = {"sheet": 17_716, "curve": 20_456, "endpoint": 40_912}
SOURCE_G_DENOMINATOR = 224_580

FILES = {
    "sheet": f"{PREFIX}_2d_sheet_ledger.jsonl.gz",
    "curve": f"{PREFIX}_1d_curve_ledger.jsonl.gz",
    "endpoint": f"{PREFIX}_0d_endpoint_ledger.jsonl.gz",
    "result": f"{PREFIX}_result.json",
}

PINS = {
    "cm2_round209_source_g_outgoing_half_open_owner_probe.py":
        "dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f",
    "cm2_round209_source_g_outgoing_half_open_owner_spike_report.md":
        "7501e73fdad0c3721ed70b73226a4c3a4f7288f9b8429a553a50dde725812524",
    "cm2_round173_source_g_exact_return_signature_transport.py":
        "bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f",
    "cm2_round173_source_g_exact_return_signature_transport_certificate.json":
        "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a",
    "cm2_round173_source_g_exact_return_signature_transport_verifier.py":
        "eb2b51929719563cd9fe72d180f3f1932a049e983ad1e7a8ec9ac89526bc30f1",
    "cm2_round173_source_g_exact_return_signature_transport_verification.json":
        "e205367506bc02aa982de074253e5806f07b4358dd3738fb4a0e14476e44ce99",
    "cm2-round173-source-g-exact-return-signature-transport-report-2026-07-26.md":
        "bef5a14534a5e825a830dfd96df8f6262552d860ed5b0c50f3ce089cb7be4141",
    "cm2-round173-source-g-exact-return-signature-transport-cold-replay-2026-07-26.md":
        "c956735ba014d6a9c6b326611fc51929163d738ae44886c93174bcc4e641d46e",
    "cm2-round173-source-g-exact-return-signature-transport-manifest-2026-07-26.sha256":
        "ba2a1b6eea612e538e3ca70e2916e07469fda38eaef24a751ff862262336f275",
    "cm2_round195_source_g_outgoing_assembly_and_u2_order_probe.py":
        "f70734937ed2630f4357b9e1d860e862c1a932c573c1f93c45788cd5697ee4e1",
    "cm2_round195_source_g_outgoing_assembly_and_u2_order_spike_report.md":
        "2f4318f381b79c28c457ce3e2f54e0b6e843c649738789c6d0f95dc8a6332dac",
    "cm2_round208_source_g_outgoing_direct_signature_materialization.py":
        "c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_verifier.py":
        "718c731004fe2125511a9a52c84f45c77eab842d4c042942e91cc5881b64ee36",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_verification.json":
        "29faabf06adab4e4a7a1cfc99d1dc2c14aa9d7bfc7e32773fad41056bb2c8f31",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_report.md":
        "e4b1a34c2d9c978720fcca47cfc71dc2c937ab30246e43bb76dfe934e6bb21ea",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_cold_replay.md":
        "43b11e5c8455bcacef327cff72a69f06b6cdb5ed47c3ce0e3b7b7b1cb7a824ba",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_manifest.sha256":
        "f35c1d00bb1e5c6fc35465ffa29fc66e5648c009d07069ea09b6332c657c1c83",
}

R173_RESULT = "948ab0a8539b08adc96c9493de415b44a5ffb75a1ee3ef47a4742902c211c11f"
R208_RESULT = "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8"
R195_RESULT = "bc1a983b5acab0b3a41c9c5941a77313a80d4376932b41ea31e3aabeed96511b"


class Failure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Failure(label)


ENCODER = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False,
)


def canonical(value: Any) -> bytes:
    return "".join(ENCODER.iterencode(value)).encode("utf-8")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    need(len(canonical(row)) <= ROW_CAP, "final canonical row cap")
    row["row_sha256"] = sha(row)
    need(len(canonical(row)) <= ROW_CAP, "closed canonical row cap")
    return row


def stat_key(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
        info.st_size, info.st_mtime_ns, info.st_ctime_ns,
    )


def dir_key(info: os.stat_result) -> tuple[int, ...]:
    # Directory mtime/ctime necessarily changes during our own atomic staging.
    # Identity, type and link count must remain stable.
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink)


class HeldPins:
    """Two-pass hashes with held descriptors and final path/dir validation."""

    def __init__(self, expected: dict[str, str]) -> None:
        self.entries: dict[str, dict[str, Any]] = {}
        for name, expected_sha in expected.items():
            self._open(name, expected_sha)

    def _open(self, name: str, expected_sha: str | None) -> None:
        path = HERE / name
        parent_before = path.parent.lstat()
        need(stat.S_ISDIR(parent_before.st_mode), f"parent directory:{name}")
        need(not path.parent.is_symlink(), f"parent symlink:{name}")
        parent_fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        before = path.lstat()
        need(stat.S_ISREG(before.st_mode), f"regular:{name}")
        need(not path.is_symlink(), f"symlink:{name}")
        need(before.st_nlink == 1, f"hardlink:{name}")
        need(0 < before.st_size <= MAX_INPUT, f"size:{name}")
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        opened = os.fstat(fd)
        need(stat_key(opened) == stat_key(before), f"open race:{name}")
        hashes: list[str] = []
        for _pass in range(2):
            os.lseek(fd, 0, os.SEEK_SET)
            state = hashlib.sha256()
            total = 0
            while True:
                chunk = os.read(fd, 1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                need(total <= MAX_INPUT, f"read bound:{name}")
                state.update(chunk)
            need(total == opened.st_size, f"read size:{name}")
            hashes.append(state.hexdigest())
        need(hashes[0] == hashes[1], f"two-pass hash:{name}")
        if expected_sha is not None:
            need(hashes[0] == expected_sha, f"pin:{name}")
        self.entries[name] = {
            "path": path, "fd": fd, "parent_fd": parent_fd,
            "file_stat": stat_key(opened), "parent_stat": dir_key(parent_before),
            "sha256": hashes[0], "size": opened.st_size,
        }

    def add_self(self, path: Path) -> None:
        self._open(path.name, None)

    def raw(self, name: str) -> bytes:
        item = self.entries[name]
        fd = item["fd"]
        os.lseek(fd, 0, os.SEEK_SET)
        parts: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            need(total <= MAX_INPUT, f"held read bound:{name}")
            parts.append(chunk)
        need(total == item["size"], f"held read size:{name}")
        return b"".join(parts)

    def final(self) -> None:
        for name, item in self.entries.items():
            path = item["path"]
            need(stat_key(os.fstat(item["fd"])) == item["file_stat"], f"final fd:{name}")
            need(stat_key(path.lstat()) == item["file_stat"], f"final path:{name}")
            need(dir_key(os.fstat(item["parent_fd"])) == item["parent_stat"], f"final parent fd:{name}")
            need(dir_key(path.parent.lstat()) == item["parent_stat"], f"final parent path:{name}")
            need(path.resolve(strict=True) == HERE / name, f"final resolve:{name}")

    def summary(self) -> list[dict[str, Any]]:
        return [
            {"filename": name, "size": item["size"], "sha256": item["sha256"]}
            for name, item in sorted(self.entries.items())
            if name != Path(__file__).name
        ]

    def close(self) -> None:
        for item in self.entries.values():
            os.close(item["fd"])
            os.close(item["parent_fd"])


def load_probe(raw: bytes) -> types.ModuleType:
    module = types.ModuleType("round209_frozen_evaluator")
    module.__file__ = str(HERE / "cm2_round209_source_g_outgoing_half_open_owner_probe.py")
    exec(compile(raw, module.__file__, "exec"), module.__dict__)
    return module


def authority() -> dict[str, Any]:
    rule = {
        "rule": "E or W owns; N or S excludes",
        "owner_set": ["E", "W"],
        "shadow_set": ["N", "S"],
        "duplicate_trace_is_identified_not_added": True,
    }
    return {
        "Round173_result_sha256": R173_RESULT,
        "Round208_result_sha256": R208_RESULT,
        "Round173_half_open_rule": rule,
        "Round173_half_open_rule_sha256": sha(rule),
        "credit_authority": "ROUND173_RULE_PLUS_ROUND208_FORMAL_ROWS_ONLY",
        "Round195_role": "PINNED_NONFORMAL_PROVENANCE_ONLY_ZERO_CREDIT",
    }


def formal_rows(
    probe_sheets: list[dict[str, Any]],
    probe_curves: list[dict[str, Any]],
    probe_endpoints: list[dict[str, Any]],
    leaves: list[dict[str, Any]],
    regions: list[dict[str, Any]],
    u2_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    auth = authority()
    leaf_by_id = {row["leaf_row_id"]: row for row in leaves}
    region_by_id = {row["region_row_id"]: row for row in regions}
    u2_by_leaf = {row["leaf_row_id"]: row for row in u2_rows}
    sheets: list[dict[str, Any]] = []
    sheet_by_probe: dict[str, dict[str, Any]] = {}
    for source in probe_sheets:
        leaf = leaf_by_id[source["leaf_row_id"]]
        owner = region_by_id[source["owner_region_row_id"]]
        shadow = region_by_id[source["shadow_region_row_id"]]
        u2 = u2_by_leaf.get(source["leaf_row_id"])
        commitment = {
            "authority": auth,
            "Round208_leaf": {"row_id": leaf["leaf_row_id"], "row_sha256": leaf["row_sha256"]},
            "Round208_owner_region": {"row_id": owner["region_row_id"], "row_sha256": owner["row_sha256"]},
            "Round208_shadow_region": {"row_id": shadow["region_row_id"], "row_sha256": shadow["row_sha256"]},
            "Round208_U_pipe_U_ordering": None if u2 is None else {
                "row_id": u2["leaf_row_id"], "row_sha256": u2["row_sha256"],
                "cross_t_status": u2["cross_t_status"],
                "strict_curve_ordering": u2["strict_curve_ordering"],
            },
        }
        commitment_sha = sha(commitment)
        payload = {
            key: copy.deepcopy(value) for key, value in source.items()
            if key not in {"sheet_row_id", "row_sha256", "formal_half_open_owner_credit",
                           "whole_original_tube_credit", "global_exact_key_disposition_credit"}
        }
        row = closed({
            "sheet_row_id": f"round306b1af4k2r209-sheet:{commitment_sha}",
            "source_probe_row_id": source["sheet_row_id"],
            "source_probe_row_sha256": source["row_sha256"],
            "canonical_input_commitment": commitment,
            "canonical_input_commitment_sha256": commitment_sha,
            **payload,
            "authority_scope": "LOCAL_2D_SHEET_HALF_OPEN_OWNER_ONLY",
            "local_half_open_owner_lineage_authority_credit": 1,
            "formal_half_open_owner_credit": 1,
            "whole_leaf_credit": 0, "whole_origin_credit": 0,
            "whole_original_tube_credit": 0, "physical_component_credit": 0,
            "global_component_credit": 0, "global_exact_key_disposition_credit": 0,
        })
        sheets.append(row)
        sheet_by_probe[source["sheet_row_id"]] = row

    curves: list[dict[str, Any]] = []
    curve_by_probe: dict[str, dict[str, Any]] = {}
    for source in probe_curves:
        parent = sheet_by_probe[source["sheet_row_id"]]
        leaf = leaf_by_id[source["leaf_row_id"]]
        face_key = "lower_t_face" if source["face_side"] == "LOWER" else "upper_t_face"
        face = leaf[face_key]
        commitment = {
            "authority": auth,
            "parent_sheet": {"row_id": parent["sheet_row_id"], "row_sha256": parent["row_sha256"]},
            "Round208_leaf": {"row_id": leaf["leaf_row_id"], "row_sha256": leaf["row_sha256"]},
            "face_side": source["face_side"], "face_payload_sha256": sha(face),
            "boundary_edge_pair": source["boundary_edge_pair"],
            "graph_axis": source["graph_axis"], "geometry_provenance": source["geometry_provenance"],
        }
        commitment_sha = sha(commitment)
        payload = {
            key: copy.deepcopy(value) for key, value in source.items()
            if key not in {"curve_row_id", "sheet_row_id", "sheet_row_sha256", "row_sha256",
                           "formal_half_open_owner_credit", "whole_original_tube_credit",
                           "global_exact_key_disposition_credit"}
        }
        row = closed({
            "curve_row_id": f"round306b1af4k2r209-curve:{commitment_sha}",
            "source_probe_row_id": source["curve_row_id"],
            "source_probe_row_sha256": source["row_sha256"],
            "sheet_row_id": parent["sheet_row_id"], "sheet_row_sha256": parent["row_sha256"],
            "canonical_input_commitment": commitment,
            "canonical_input_commitment_sha256": commitment_sha,
            **payload,
            "authority_scope": "LOCAL_1D_CURVE_INCIDENCE_OWNER_LINEAGE_ONLY",
            "local_half_open_owner_lineage_authority_credit": 1,
            "formal_half_open_owner_credit": 1,
            "whole_leaf_credit": 0, "whole_origin_credit": 0,
            "whole_original_tube_credit": 0, "physical_component_credit": 0,
            "global_component_credit": 0, "global_exact_key_disposition_credit": 0,
        })
        curves.append(row)
        curve_by_probe[source["curve_row_id"]] = row

    endpoints: list[dict[str, Any]] = []
    for source in probe_endpoints:
        parent_curve = curve_by_probe[source["curve_row_id"]]
        parent_sheet = sheet_by_probe[source["sheet_row_id"]]
        leaf = leaf_by_id[source["leaf_row_id"]]
        face_key = "lower_t_face" if source["face_side"] == "LOWER" else "upper_t_face"
        face = leaf[face_key]
        commitment = {
            "authority": auth,
            "parent_curve": {"row_id": parent_curve["curve_row_id"], "row_sha256": parent_curve["row_sha256"]},
            "parent_sheet": {"row_id": parent_sheet["sheet_row_id"], "row_sha256": parent_sheet["row_sha256"]},
            "Round208_leaf": {"row_id": leaf["leaf_row_id"], "row_sha256": leaf["row_sha256"]},
            "face_side": source["face_side"], "face_payload_sha256": sha(face),
            "endpoint_ordinal": source["endpoint_ordinal"], "boundary_edge": source["boundary_edge"],
        }
        commitment_sha = sha(commitment)
        payload = {
            key: copy.deepcopy(value) for key, value in source.items()
            if key not in {"endpoint_row_id", "curve_row_id", "curve_row_sha256", "sheet_row_id",
                           "row_sha256", "formal_half_open_owner_credit", "whole_original_tube_credit",
                           "global_exact_key_disposition_credit"}
        }
        endpoints.append(closed({
            "endpoint_row_id": f"round306b1af4k2r209-endpoint:{commitment_sha}",
            "source_probe_row_id": source["endpoint_row_id"],
            "source_probe_row_sha256": source["row_sha256"],
            "curve_row_id": parent_curve["curve_row_id"], "curve_row_sha256": parent_curve["row_sha256"],
            "sheet_row_id": parent_sheet["sheet_row_id"], "sheet_row_sha256": parent_sheet["row_sha256"],
            "canonical_input_commitment": commitment,
            "canonical_input_commitment_sha256": commitment_sha,
            **payload,
            "authority_scope": "LOCAL_0D_ENDPOINT_INCIDENCE_OWNER_LINEAGE_ONLY",
            "local_half_open_owner_lineage_authority_credit": 1,
            "formal_half_open_owner_credit": 1,
            "whole_leaf_credit": 0, "whole_origin_credit": 0,
            "whole_original_tube_credit": 0, "physical_component_credit": 0,
            "global_component_credit": 0, "global_exact_key_disposition_credit": 0,
        }))

    sheets.sort(key=lambda row: row["sheet_row_id"])
    curves.sort(key=lambda row: row["curve_row_id"])
    endpoints.sort(key=lambda row: row["endpoint_row_id"])
    need(len(sheets) == EXPECTED["sheet"] and len(curves) == EXPECTED["curve"]
         and len(endpoints) == EXPECTED["endpoint"], "formal counts")
    sheet_by_id = {row["sheet_row_id"]: row for row in sheets}
    curve_by_id = {row["curve_row_id"]: row for row in curves}
    need(all(row["sheet_row_sha256"] == sheet_by_id[row["sheet_row_id"]]["row_sha256"] for row in curves),
         "curve sheet joins")
    need(all(row["sheet_row_sha256"] == sheet_by_id[row["sheet_row_id"]]["row_sha256"]
             and row["curve_row_sha256"] == curve_by_id[row["curve_row_id"]]["row_sha256"]
             for row in endpoints), "endpoint parent joins")
    return sheets, curves, endpoints


def gzip_rows(rows: list[dict[str, Any]]) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0, compresslevel=9) as handle:
        for row in rows:
            raw = canonical(row)
            need(len(raw) <= ROW_CAP, "ledger canonical cap")
            handle.write(raw + b"\n")
    return buffer.getvalue()


def ledger_meta(name: str, raw: bytes, rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    return {
        "filename": name, "size": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
        "row_count": len(rows), "rows_sha256": sha(rows),
        "row_ids_sha256": sha([row[id_key] for row in rows]),
        "row_hashes_sha256": sha([row["row_sha256"] for row in rows]),
        "canonical_jsonl_gzip_mtime": 0, "each_decoded_row_final_canonical_cap_bytes": ROW_CAP,
    }


def safe_directory(path: Path) -> tuple[Path, tuple[int, ...], int]:
    need(path.exists() and path.is_dir() and not path.is_symlink(), "output directory")
    resolved = path.resolve(strict=True)
    info = path.lstat()
    need(stat.S_ISDIR(info.st_mode), "output directory mode")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    need(stat_key(os.fstat(fd)) == stat_key(info), "output directory race")
    return resolved, dir_key(info), fd


def validate_target(path: Path, directory: Path) -> None:
    need(path.parent.resolve(strict=True) == directory, "output target parent")
    if path.exists() or path.is_symlink():
        info = path.lstat()
        need(stat.S_ISREG(info.st_mode) and not path.is_symlink(), "output target regular")
        need(info.st_nlink == 1, "output target hardlink")


def publish(directory: Path, directory_stat: tuple[int, ...], directory_fd: int,
            documents: dict[str, bytes]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for name, raw in documents.items():
            target = directory / name
            validate_target(target, directory)
            stage = directory / f".{name}.atomic.{os.getpid()}"
            need(not stage.exists() and not stage.is_symlink(), "clean atomic stage")
            fd = os.open(stage, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
            try:
                offset = 0
                while offset < len(raw):
                    offset += os.write(fd, raw[offset:offset + 1024 * 1024])
                os.fsync(fd)
            finally:
                os.close(fd)
            staged.append((stage, target))
        need(dir_key(os.fstat(directory_fd)) == directory_stat, "final output directory fd")
        need(dir_key(directory.lstat()) == directory_stat, "final output directory path")
        for stage, target in staged:
            validate_target(target, directory)
            os.replace(stage, target)
        os.fsync(directory_fd)
    finally:
        for stage, _target in staged:
            if stage.exists() and not stage.is_symlink():
                stage.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-directory", type=Path, default=HERE)
    args = parser.parse_args()
    output_dir, output_stat, output_fd = safe_directory(args.output_directory)
    pins = HeldPins(PINS)
    pins.add_self(Path(__file__))
    try:
        probe = load_probe(pins.raw("cm2_round209_source_g_outgoing_half_open_owner_probe.py"))
        r173, r208, _input_hashes = probe.validate_inputs()
        leaves, regions, _faces, u2_rows = probe.validate_round195_geometry(r208)
        probe_sheets, probe_curves, probe_endpoints, owner_audit = probe.build_lineages(leaves, regions)
        u2_audit = probe.audit_u2(u2_rows, probe_sheets, probe_curves, probe_endpoints)
        sheets, curves, endpoints = formal_rows(
            probe_sheets, probe_curves, probe_endpoints, leaves, regions, u2_rows,
        )
        sheet_raw = gzip_rows(sheets)
        curve_raw = gzip_rows(curves)
        endpoint_raw = gzip_rows(endpoints)
        ledgers = {
            "2D_sheet": ledger_meta(FILES["sheet"], sheet_raw, sheets, "sheet_row_id"),
            "1D_curve": ledger_meta(FILES["curve"], curve_raw, curves, "curve_row_id"),
            "0D_endpoint": ledger_meta(FILES["endpoint"], endpoint_raw, endpoints, "endpoint_row_id"),
        }
        origin_count = len({row["origin_row_id"] for row in sheets})
        occurrence_count = len({row["occurrence_row_id"] for row in sheets})
        retained_count = len({row["retained_child_row_id"] for row in sheets})
        result = {
            "status": STATUS,
            "formal_authority_decision": {
                "local_half_open_owner_lineage_authority": "GRANTED",
                "authority_basis": "ROUND173_SEAM_RULE_PLUS_ROUND208_INDEPENDENTLY_VERIFIED_FORMAL_ROWS",
                "Round195_formal_authority": "DENIED_NONFORMAL_PROBE",
                "Round209_role": "PINNED_PRODUCER_SIDE_EVALUATOR_ZERO_AUTHORITY",
            },
            "input_frontier": {
                "pins": pins.summary(), "pin_count": len(PINS),
                "all_pins_held_FD_two_pass_and_final_path_directory_revalidated": True,
                "symlink_hardlink_TOCTOU_fail_close": True,
                "TMPDIR_used": False, "decoded_row_spill_used": False,
                "temporary_spill_outside_deliverables_requirement": "VACUOUS_NO_SPILL",
                "Round173_result_sha256": R173_RESULT,
                "Round195_probe_result_sha256": R195_RESULT,
                "Round208_result_sha256": R208_RESULT,
            },
            "ledgers": ledgers,
            "dimension_safe_conservation": {
                "2D_sheet_owner_rows": len(sheets), "1D_curve_incidence_rows": len(curves),
                "0D_endpoint_incidence_rows": len(endpoints), "endpoint_identity": "40912=2*20456",
                "input_leaf_count": len(leaves), "empty_leaf_count": 608,
                "strict_region_identity": "36040=608+2*17716",
                "covered_origin_count_without_whole_origin_credit": origin_count,
                "covered_occurrence_count_without_global_component_credit": occurrence_count,
                "covered_retained_child_count": retained_count,
                "all_parent_row_hash_joins_exact": True,
                "sheet_curve_endpoint_incidence_is_strictly_separate_from_global_component": True,
            },
            "owner_shadow_factor_theorem_audit": owner_audit,
            "U_pipe_U_88_sheet_ordering_audit": u2_audit,
            "credit_contract": {
                "formal_local_2D_sheet_owner_credit": len(sheets),
                "formal_local_1D_curve_incidence_owner_credit": len(curves),
                "formal_local_0D_endpoint_incidence_owner_credit": len(endpoints),
                "formal_local_dimensional_authority_total": len(sheets) + len(curves) + len(endpoints),
                "whole_leaf_credit": 0, "whole_origin_credit": 0,
                "whole_original_tube_credit": 0, "physical_component_credit": 0,
                "global_component_credit": 0, "global_exact_key_disposition_credit": 0,
                "official_source_G_global_dispositions": 0,
                "official_source_G_global_disposition_denominator": SOURCE_G_DENOMINATOR,
                "D02": "BLOCKED", "Gate5": "10/18", "complete_global_18_field_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "remaining_blockers": [
                "local incidence rows are not physical/global component deduplications",
                "whole-leaf, whole-origin, and whole-tube exhaustion is not proved",
                "immutable global exact-key routing is not materialized",
                "R195 remains nonformal provenance and grants no authority",
            ],
            "provenance": {
                "schema": SCHEMA, "producer_sha256": pins.entries[Path(__file__).name]["sha256"],
                "python_version": sys.version.split()[0], "deterministic_receipt": True,
            },
        }
        envelope = {"schema": SCHEMA, "result": result, "result_sha256": sha(result)}
        result_raw = canonical(envelope) + b"\n"
        need(len(canonical(envelope)) <= ROW_CAP, "result final canonical cap")
        pins.final()
        publish(output_dir, output_stat, output_fd, {
            FILES["sheet"]: sheet_raw, FILES["curve"]: curve_raw,
            FILES["endpoint"]: endpoint_raw, FILES["result"]: result_raw,
        })
        pins.final()
        print(canonical({
            "status": STATUS, "result_sha256": envelope["result_sha256"],
            "ledger_counts": EXPECTED,
            "ledger_file_sha256": {key: value["sha256"] for key, value in ledgers.items()},
        }).decode())
        return 0
    finally:
        pins.close()
        os.close(output_fd)


if __name__ == "__main__":
    raise SystemExit(main())
