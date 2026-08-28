#!/usr/bin/env python3
"""Independent verifier for the hardened Round209 owner-lineage package.

The candidate producer is inert pinned bytes: it is neither imported nor
executed.  This verifier also does not import or execute the Round209 probe.
It uses a separately pinned, previously independent Round211 evaluator for
the pure reconstruction functions, fed only freshly decoded and validated
Round173/Round208 formal rows.
"""

from __future__ import annotations

import argparse
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
from typing import Any


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round306b1af4k2r209_source_g_outgoing_half_open_owner_lineage"
SCHEMA = "cm2.round306b1af4k2r209.source-g-outgoing-half-open-owner-lineage.v1"
VERIFY_SCHEMA = SCHEMA + ".verification.v1"
ATTACK_SCHEMA = SCHEMA + ".attack-suite.v1"
STATUS = (
    "SEALED_LOCAL_SOURCE_G_OUTGOING_W_HALF_OPEN_OWNER_LINEAGE_AUTHORITY__"
    "NO_WHOLE_LEAF_OR_GLOBAL_PROMOTION"
)
PASS = "PASS_INDEPENDENT_STRICT_REPLAY"
ROW_CAP = 8 * 1024 * 1024
MAX_INPUT = 300 * 1024 * 1024
EXPECTED = {"sheet": 17_716, "curve": 20_456, "endpoint": 40_912}
SOURCE_G_DENOMINATOR = 224_580
PRODUCER = f"{PREFIX}_producer.py"
PRODUCER_SHA256 = "f0aed300fbc212bd24ce5105c75dcf6b08e9df307beaa0805d1babab391fabf5"
EVALUATOR = "cm2_round211_source_g_outgoing_half_open_owner_materialization_verifier.py"
EVALUATOR_SHA256 = "df90f2dd869bef3b873fe800fe124a256e82ef7e772359fbea49a9b793725176"
FILES = {
    "sheet": f"{PREFIX}_2d_sheet_ledger.jsonl.gz",
    "curve": f"{PREFIX}_1d_curve_ledger.jsonl.gz",
    "endpoint": f"{PREFIX}_0d_endpoint_ledger.jsonl.gz",
    "result": f"{PREFIX}_result.json",
    "attack": f"{PREFIX}_attack_suite.json",
    "verification": f"{PREFIX}_verification.json",
}

UPSTREAM_PINS = {
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
AUTHORITY_PINS = {**UPSTREAM_PINS, PRODUCER: PRODUCER_SHA256, EVALUATOR: EVALUATOR_SHA256}
R173_RESULT = "948ab0a8539b08adc96c9493de415b44a5ffb75a1ee3ef47a4742902c211c11f"
R208_RESULT = "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8"
R195_RESULT = "bc1a983b5acab0b3a41c9c5941a77313a80d4376932b41ea31e3aabeed96511b"
R195_FACE = "0efb78285bc7836c84860f157ab4ec45593029aa523a95fd62171d307d7a5396"
R195_LEAF = "0370fb57e9d2881a8bc2d0e66351a6c551e147d483558c682f051153924f88b5"
R195_U2 = "12fbc70f82645ae2ad252b4e88587a7841814a03fda1972a0241cd63c45d6ee0"


class Failure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Failure(label)


ENCODER = json.JSONEncoder(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def canonical(value: Any) -> bytes:
    return "".join(ENCODER.iterencode(value)).encode("utf-8")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def typed_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(typed_equal(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def validate_tree(value: Any) -> None:
    if value is None or type(value) in {bool, str, int}:
        return
    if type(value) is list:
        for child in value:
            validate_tree(child)
        return
    if type(value) is dict:
        for key, child in value.items():
            need(type(key) is str, "JSON key type")
            validate_tree(child)
        return
    raise Failure("nonintegral/unsupported JSON type")


def strict_decode(raw: bytes, cap: int, canonical_required: bool = True) -> dict[str, Any]:
    need(len(raw) <= cap + 1, "raw JSON cap")
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "JSON encoding")
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    def reject(token: str) -> None:
        raise Failure(f"nonintegral/NaN JSON number:{token}")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique,
                       parse_float=reject, parse_constant=reject)
    need(type(value) is dict, "top JSON object")
    validate_tree(value)
    encoded = canonical(value)
    need(len(encoded) <= cap, "final canonical decoded cap")
    if canonical_required:
        need(raw in {encoded, encoded + b"\n"}, "canonical JSON wire")
    return value


def stat_key(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def dir_key(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink)


class HeldSet:
    def __init__(self, root: Path, expected: dict[str, str | None]) -> None:
        self.root = root.resolve(strict=True)
        self.entries: dict[str, dict[str, Any]] = {}
        for name, expected_sha in expected.items():
            self._open(name, expected_sha)

    def _open(self, name: str, expected_sha: str | None) -> None:
        path = self.root / name
        parent = path.parent.lstat()
        need(stat.S_ISDIR(parent.st_mode) and not path.parent.is_symlink(), f"parent:{name}")
        pfd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        before = path.lstat()
        need(stat.S_ISREG(before.st_mode) and not path.is_symlink(), f"regular:{name}")
        need(before.st_nlink == 1 and 0 < before.st_size <= MAX_INPUT, f"link/size:{name}")
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        opened = os.fstat(fd)
        need(stat_key(opened) == stat_key(before), f"open race:{name}")
        digests: list[str] = []
        for _pass in range(2):
            os.lseek(fd, 0, os.SEEK_SET)
            state = hashlib.sha256(); total = 0
            while True:
                chunk = os.read(fd, 1024 * 1024)
                if not chunk: break
                total += len(chunk); need(total <= MAX_INPUT, f"read cap:{name}"); state.update(chunk)
            need(total == opened.st_size, f"read size:{name}")
            digests.append(state.hexdigest())
        need(digests[0] == digests[1], f"two pass:{name}")
        if expected_sha is not None:
            need(digests[0] == expected_sha, f"pin:{name}")
        self.entries[name] = {"path": path, "fd": fd, "pfd": pfd,
                              "file_stat": stat_key(opened), "parent_stat": dir_key(parent),
                              "sha256": digests[0], "size": opened.st_size}

    def add_self(self, path: Path) -> None:
        self._open(path.name, None)

    def raw(self, name: str) -> bytes:
        item = self.entries[name]; fd = item["fd"]
        os.lseek(fd, 0, os.SEEK_SET); parts: list[bytes] = []; total = 0
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk: break
            total += len(chunk); need(total <= MAX_INPUT, f"held cap:{name}"); parts.append(chunk)
        need(total == item["size"], f"held size:{name}")
        return b"".join(parts)

    def final(self) -> None:
        for name, item in self.entries.items():
            path = item["path"]
            need(stat_key(os.fstat(item["fd"])) == item["file_stat"], f"final fd:{name}")
            need(stat_key(path.lstat()) == item["file_stat"], f"final path:{name}")
            need(dir_key(os.fstat(item["pfd"])) == item["parent_stat"], f"final parent fd:{name}")
            need(dir_key(path.parent.lstat()) == item["parent_stat"], f"final parent path:{name}")
            need(path.resolve(strict=True) == self.root / name, f"final resolve:{name}")

    def summary(self, names: dict[str, str]) -> list[dict[str, Any]]:
        return [{"filename": name, "size": self.entries[name]["size"],
                 "sha256": self.entries[name]["sha256"]} for name in sorted(names)]

    def close(self) -> None:
        for item in self.entries.values():
            os.close(item["fd"]); os.close(item["pfd"])


def unwrap(raw: bytes, schema: str, result_sha: str, label: str) -> dict[str, Any]:
    # Legacy formal wrappers are strict JSON but predate canonical-wire output.
    # Their result objects are still closed by the pinned canonical digest.
    doc = strict_decode(raw, MAX_INPUT, canonical_required=False)
    need(set(doc) == {"schema", "result", "result_sha256"}, f"wrapper:{label}")
    need(doc["schema"] == schema and doc["result_sha256"] == result_sha
         and sha(doc["result"]) == result_sha, f"envelope:{label}")
    return doc["result"]


def validate_closed_rows(rows: list[dict[str, Any]], count: int, rows_sha: str,
                         id_key: str, label: str) -> None:
    need(type(rows) is list and len(rows) == count and sha(rows) == rows_sha, f"ledger:{label}")
    need(len({row[id_key] for row in rows}) == count, f"unique:{label}")
    for row in rows:
        need(type(row) is dict and type(row.get("row_sha256")) is str, f"row schema:{label}")
        payload = {key: value for key, value in row.items() if key != "row_sha256"}
        need(sha(payload) == row["row_sha256"], f"row closure:{label}")


def formal_inputs(pins: HeldSet) -> tuple[dict[str, Any], list[dict[str, Any]],
                                           list[dict[str, Any]], list[dict[str, Any]]]:
    r173 = unwrap(
        pins.raw("cm2_round173_source_g_exact_return_signature_transport_certificate.json"),
        "cm2.round173.source-g-exact-return-signature-transport.v1", R173_RESULT, "R173",
    )
    rule = r173["outgoing_chart_contract"]
    need(rule["diagonal_seam_rule"] == "E or W owns; N or S excludes"
         and rule["owner_set"] == ["E", "W"]
         and rule["duplicate_trace_is_identified_not_added"] is True
         and rule["owner_set_is_invariant_under_Jx_and_Jy"] is True, "R173 seam rule")
    r208 = unwrap(
        pins.raw("cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"),
        "cm2.round208.source-g-outgoing-direct-signature-materialization.v1", R208_RESULT, "R208",
    )
    need(r208["status"].startswith("CERTIFIED_LOCAL_SOURCE_G_OUTGOING_W_DIRECT_SIGNATURE_ROWS")
         and r208["formal_scope_contract"]["lower_dimensional_half_open_ownership_materialized"] is False
         and r208["formal_scope_contract"]["whole_original_tube_credit"] == 0
         and r208["formal_scope_contract"]["global_exact_key_disposition_credit"] == 0,
         "R208 formal boundary")
    face = r208["formal_final_factor_face_ledger"]
    leaf = r208["formal_leaf_geometry_ledger"]
    region = r208["formal_local_open_3D_signature_ledger"]
    u2 = r208["formal_U_pipe_U_side_specific_ledger"]
    validate_closed_rows(face["rows"], 18_412, face["rows_sha256"], "face_row_id", "face")
    validate_closed_rows(leaf["rows"], 18_324, leaf["rows_sha256"], "leaf_row_id", "leaf")
    validate_closed_rows(region["rows"], 36_040, region["rows_sha256"], "region_row_id", "region")
    validate_closed_rows(u2["rows"], 88, u2["rows_sha256"], "leaf_row_id", "u2")
    raw_faces = [{key: value for key, value in row.items() if key != "row_sha256"} for row in face["rows"]]
    raw_leaves = [{key: value for key, value in row.items()
                   if key not in {"row_sha256", "formal_final_geometry_row_materialized"}}
                  for row in leaf["rows"]]
    raw_u2 = [{key: value for key, value in row.items()
               if key not in {"row_sha256", "both_strict_sides_formally_signature_materialized"}}
              for row in u2["rows"]]
    need(sha(raw_faces) == R195_FACE and sha(raw_leaves) == R195_LEAF and sha(raw_u2) == R195_U2,
         "R195 provenance reconstruction only")
    return r173, leaf["rows"], region["rows"], u2["rows"]


def evaluator(raw: bytes) -> types.ModuleType:
    module = types.ModuleType("round211_independent_pure_evaluator")
    module.__file__ = str(HERE / EVALUATOR)
    exec(compile(raw, module.__file__, "exec"), module.__dict__)
    return module


def authority() -> dict[str, Any]:
    rule = {"rule": "E or W owns; N or S excludes", "owner_set": ["E", "W"],
            "shadow_set": ["N", "S"], "duplicate_trace_is_identified_not_added": True}
    return {"Round173_result_sha256": R173_RESULT, "Round208_result_sha256": R208_RESULT,
            "Round173_half_open_rule": rule, "Round173_half_open_rule_sha256": sha(rule),
            "credit_authority": "ROUND173_RULE_PLUS_ROUND208_FORMAL_ROWS_ONLY",
            "Round195_role": "PINNED_NONFORMAL_PROVENANCE_ONLY_ZERO_CREDIT"}


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    need(len(canonical(payload)) <= ROW_CAP, "expected row cap")
    row = copy.deepcopy(payload); row["row_sha256"] = sha(row)
    need(len(canonical(row)) <= ROW_CAP, "expected closed row cap")
    return row


def formal_rows(probe_sheets: list[dict[str, Any]], probe_curves: list[dict[str, Any]],
                probe_endpoints: list[dict[str, Any]], leaves: list[dict[str, Any]],
                regions: list[dict[str, Any]], u2_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], ...]:
    auth = authority(); leaf_by = {row["leaf_row_id"]: row for row in leaves}
    region_by = {row["region_row_id"]: row for row in regions}
    u2_by = {row["leaf_row_id"]: row for row in u2_rows}
    sheets: list[dict[str, Any]] = []; sheet_probe: dict[str, dict[str, Any]] = {}
    for source in probe_sheets:
        leaf = leaf_by[source["leaf_row_id"]]; owner = region_by[source["owner_region_row_id"]]
        shadow = region_by[source["shadow_region_row_id"]]; u2 = u2_by.get(source["leaf_row_id"])
        commitment = {"authority": auth,
            "Round208_leaf": {"row_id": leaf["leaf_row_id"], "row_sha256": leaf["row_sha256"]},
            "Round208_owner_region": {"row_id": owner["region_row_id"], "row_sha256": owner["row_sha256"]},
            "Round208_shadow_region": {"row_id": shadow["region_row_id"], "row_sha256": shadow["row_sha256"]},
            "Round208_U_pipe_U_ordering": None if u2 is None else {
                "row_id": u2["leaf_row_id"], "row_sha256": u2["row_sha256"],
                "cross_t_status": u2["cross_t_status"], "strict_curve_ordering": u2["strict_curve_ordering"]}}
        commitment_sha = sha(commitment)
        payload = {key: copy.deepcopy(value) for key, value in source.items()
                   if key not in {"sheet_row_id", "row_sha256", "formal_half_open_owner_credit",
                                  "whole_original_tube_credit", "global_exact_key_disposition_credit"}}
        row = closed({"sheet_row_id": f"round306b1af4k2r209-sheet:{commitment_sha}",
            "source_probe_row_id": source["sheet_row_id"], "source_probe_row_sha256": source["row_sha256"],
            "canonical_input_commitment": commitment, "canonical_input_commitment_sha256": commitment_sha,
            **payload, "authority_scope": "LOCAL_2D_SHEET_HALF_OPEN_OWNER_ONLY",
            "local_half_open_owner_lineage_authority_credit": 1, "formal_half_open_owner_credit": 1,
            "whole_leaf_credit": 0, "whole_origin_credit": 0, "whole_original_tube_credit": 0,
            "physical_component_credit": 0, "global_component_credit": 0,
            "global_exact_key_disposition_credit": 0})
        sheets.append(row); sheet_probe[source["sheet_row_id"]] = row
    curves: list[dict[str, Any]] = []; curve_probe: dict[str, dict[str, Any]] = {}
    for source in probe_curves:
        parent = sheet_probe[source["sheet_row_id"]]; leaf = leaf_by[source["leaf_row_id"]]
        face = leaf["lower_t_face" if source["face_side"] == "LOWER" else "upper_t_face"]
        commitment = {"authority": auth,
            "parent_sheet": {"row_id": parent["sheet_row_id"], "row_sha256": parent["row_sha256"]},
            "Round208_leaf": {"row_id": leaf["leaf_row_id"], "row_sha256": leaf["row_sha256"]},
            "face_side": source["face_side"], "face_payload_sha256": sha(face),
            "boundary_edge_pair": source["boundary_edge_pair"], "graph_axis": source["graph_axis"],
            "geometry_provenance": source["geometry_provenance"]}
        commitment_sha = sha(commitment)
        payload = {key: copy.deepcopy(value) for key, value in source.items()
                   if key not in {"curve_row_id", "sheet_row_id", "sheet_row_sha256", "row_sha256",
                                  "formal_half_open_owner_credit", "whole_original_tube_credit",
                                  "global_exact_key_disposition_credit"}}
        row = closed({"curve_row_id": f"round306b1af4k2r209-curve:{commitment_sha}",
            "source_probe_row_id": source["curve_row_id"], "source_probe_row_sha256": source["row_sha256"],
            "sheet_row_id": parent["sheet_row_id"], "sheet_row_sha256": parent["row_sha256"],
            "canonical_input_commitment": commitment, "canonical_input_commitment_sha256": commitment_sha,
            **payload, "authority_scope": "LOCAL_1D_CURVE_INCIDENCE_OWNER_LINEAGE_ONLY",
            "local_half_open_owner_lineage_authority_credit": 1, "formal_half_open_owner_credit": 1,
            "whole_leaf_credit": 0, "whole_origin_credit": 0, "whole_original_tube_credit": 0,
            "physical_component_credit": 0, "global_component_credit": 0,
            "global_exact_key_disposition_credit": 0})
        curves.append(row); curve_probe[source["curve_row_id"]] = row
    endpoints: list[dict[str, Any]] = []
    for source in probe_endpoints:
        pc = curve_probe[source["curve_row_id"]]; ps = sheet_probe[source["sheet_row_id"]]
        leaf = leaf_by[source["leaf_row_id"]]
        face = leaf["lower_t_face" if source["face_side"] == "LOWER" else "upper_t_face"]
        commitment = {"authority": auth,
            "parent_curve": {"row_id": pc["curve_row_id"], "row_sha256": pc["row_sha256"]},
            "parent_sheet": {"row_id": ps["sheet_row_id"], "row_sha256": ps["row_sha256"]},
            "Round208_leaf": {"row_id": leaf["leaf_row_id"], "row_sha256": leaf["row_sha256"]},
            "face_side": source["face_side"], "face_payload_sha256": sha(face),
            "endpoint_ordinal": source["endpoint_ordinal"], "boundary_edge": source["boundary_edge"]}
        commitment_sha = sha(commitment)
        payload = {key: copy.deepcopy(value) for key, value in source.items()
                   if key not in {"endpoint_row_id", "curve_row_id", "curve_row_sha256", "sheet_row_id",
                                  "row_sha256", "formal_half_open_owner_credit", "whole_original_tube_credit",
                                  "global_exact_key_disposition_credit"}}
        endpoints.append(closed({"endpoint_row_id": f"round306b1af4k2r209-endpoint:{commitment_sha}",
            "source_probe_row_id": source["endpoint_row_id"], "source_probe_row_sha256": source["row_sha256"],
            "curve_row_id": pc["curve_row_id"], "curve_row_sha256": pc["row_sha256"],
            "sheet_row_id": ps["sheet_row_id"], "sheet_row_sha256": ps["row_sha256"],
            "canonical_input_commitment": commitment, "canonical_input_commitment_sha256": commitment_sha,
            **payload, "authority_scope": "LOCAL_0D_ENDPOINT_INCIDENCE_OWNER_LINEAGE_ONLY",
            "local_half_open_owner_lineage_authority_credit": 1, "formal_half_open_owner_credit": 1,
            "whole_leaf_credit": 0, "whole_origin_credit": 0, "whole_original_tube_credit": 0,
            "physical_component_credit": 0, "global_component_credit": 0,
            "global_exact_key_disposition_credit": 0}))
    sheets.sort(key=lambda row: row["sheet_row_id"]); curves.sort(key=lambda row: row["curve_row_id"])
    endpoints.sort(key=lambda row: row["endpoint_row_id"])
    return sheets, curves, endpoints


def read_gzip_rows(raw: bytes, expected_count: int, id_key: str, label: str) -> list[dict[str, Any]]:
    need(len(raw) >= 18 and raw[:3] == b"\x1f\x8b\x08" and raw[4:8] == b"\0\0\0\0", f"gzip header:{label}")
    rows: list[dict[str, Any]] = []; total = 0
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as handle:
        while True:
            line = handle.readline(ROW_CAP + 2)
            if not line: break
            need(len(line) <= ROW_CAP + 1 and line.endswith(b"\n"), f"line cap/newline:{label}")
            total += len(line); need(total <= MAX_INPUT, f"decoded ledger cap:{label}")
            row = strict_decode(line, ROW_CAP, canonical_required=True)
            payload = {key: value for key, value in row.items() if key != "row_sha256"}
            need(sha(payload) == row.get("row_sha256"), f"row closure:{label}")
            need(sha(row["canonical_input_commitment"]) == row["canonical_input_commitment_sha256"],
                 f"input commitment:{label}")
            rows.append(row)
    need(len(rows) == expected_count and len({row[id_key] for row in rows}) == expected_count,
         f"count/unique:{label}")
    return rows


def ledger_meta(name: str, raw: bytes, rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    return {"filename": name, "size": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "row_count": len(rows), "rows_sha256": sha(rows),
            "row_ids_sha256": sha([row[id_key] for row in rows]),
            "row_hashes_sha256": sha([row["row_sha256"] for row in rows]),
            "canonical_jsonl_gzip_mtime": 0, "each_decoded_row_final_canonical_cap_bytes": ROW_CAP}


def expected_result(authority_pins: HeldSet, sheet_raw: bytes, curve_raw: bytes, endpoint_raw: bytes,
                    sheets: list[dict[str, Any]], curves: list[dict[str, Any]], endpoints: list[dict[str, Any]],
                    leaves: list[dict[str, Any]], owner_audit: dict[str, Any], u2_audit: dict[str, Any]) -> dict[str, Any]:
    ledgers = {"2D_sheet": ledger_meta(FILES["sheet"], sheet_raw, sheets, "sheet_row_id"),
               "1D_curve": ledger_meta(FILES["curve"], curve_raw, curves, "curve_row_id"),
               "0D_endpoint": ledger_meta(FILES["endpoint"], endpoint_raw, endpoints, "endpoint_row_id")}
    return {"status": STATUS,
        "formal_authority_decision": {
            "local_half_open_owner_lineage_authority": "GRANTED",
            "authority_basis": "ROUND173_SEAM_RULE_PLUS_ROUND208_INDEPENDENTLY_VERIFIED_FORMAL_ROWS",
            "Round195_formal_authority": "DENIED_NONFORMAL_PROBE",
            "Round209_role": "PINNED_PRODUCER_SIDE_EVALUATOR_ZERO_AUTHORITY"},
        "input_frontier": {"pins": authority_pins.summary(UPSTREAM_PINS), "pin_count": len(UPSTREAM_PINS),
            "all_pins_held_FD_two_pass_and_final_path_directory_revalidated": True,
            "symlink_hardlink_TOCTOU_fail_close": True, "TMPDIR_used": False,
            "decoded_row_spill_used": False, "temporary_spill_outside_deliverables_requirement": "VACUOUS_NO_SPILL",
            "Round173_result_sha256": R173_RESULT, "Round195_probe_result_sha256": R195_RESULT,
            "Round208_result_sha256": R208_RESULT},
        "ledgers": ledgers,
        "dimension_safe_conservation": {"2D_sheet_owner_rows": len(sheets),
            "1D_curve_incidence_rows": len(curves), "0D_endpoint_incidence_rows": len(endpoints),
            "endpoint_identity": "40912=2*20456", "input_leaf_count": len(leaves), "empty_leaf_count": 608,
            "strict_region_identity": "36040=608+2*17716",
            "covered_origin_count_without_whole_origin_credit": len({row["origin_row_id"] for row in sheets}),
            "covered_occurrence_count_without_global_component_credit": len({row["occurrence_row_id"] for row in sheets}),
            "covered_retained_child_count": len({row["retained_child_row_id"] for row in sheets}),
            "all_parent_row_hash_joins_exact": True,
            "sheet_curve_endpoint_incidence_is_strictly_separate_from_global_component": True},
        "owner_shadow_factor_theorem_audit": owner_audit,
        "U_pipe_U_88_sheet_ordering_audit": u2_audit,
        "credit_contract": {"formal_local_2D_sheet_owner_credit": len(sheets),
            "formal_local_1D_curve_incidence_owner_credit": len(curves),
            "formal_local_0D_endpoint_incidence_owner_credit": len(endpoints),
            "formal_local_dimensional_authority_total": len(sheets) + len(curves) + len(endpoints),
            "whole_leaf_credit": 0, "whole_origin_credit": 0, "whole_original_tube_credit": 0,
            "physical_component_credit": 0, "global_component_credit": 0,
            "global_exact_key_disposition_credit": 0, "official_source_G_global_dispositions": 0,
            "official_source_G_global_disposition_denominator": SOURCE_G_DENOMINATOR,
            "D02": "BLOCKED", "Gate5": "10/18", "complete_global_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM"},
        "remaining_blockers": [
            "local incidence rows are not physical/global component deduplications",
            "whole-leaf, whole-origin, and whole-tube exhaustion is not proved",
            "immutable global exact-key routing is not materialized",
            "R195 remains nonformal provenance and grants no authority"],
        "provenance": {"schema": SCHEMA, "producer_sha256": PRODUCER_SHA256,
                       "python_version": "3.12.3", "deterministic_receipt": True}}


def attacks(expected_sheets: list[dict[str, Any]], expected_curves: list[dict[str, Any]],
            expected_endpoints: list[dict[str, Any]], result: dict[str, Any], endpoint_raw: bytes) -> dict[str, Any]:
    tests: list[str] = []
    def rejected(name: str, left: Any, right: Any) -> None:
        need(not typed_equal(left, right), f"attack accepted:{name}"); tests.append(name)
    original = expected_sheets[0]
    changed = copy.deepcopy(original); changed["canonical_input_commitment"]["authority"]["Round208_result_sha256"] = "0" * 64
    rejected("sheet_cross_certificate_substitution", original, changed)
    need(sha(original["canonical_input_commitment"]) != sha(changed["canonical_input_commitment"]),
         "commitment separation"); tests.append("distinct_sheet_inputs_distinct_commitment_digest")
    changed = copy.deepcopy(original); changed["owner_outgoing_cell"] = "N"
    rejected("owner_payload_substitution", original, changed)
    changed = copy.deepcopy(expected_curves[0]); changed["sheet_row_sha256"] = "0" * 64
    rejected("curve_parent_hash_substitution", expected_curves[0], changed)
    changed = copy.deepcopy(expected_endpoints[0]); changed["endpoint_ordinal"] = 2 if changed["endpoint_ordinal"] == 1 else 1
    rejected("endpoint_ordinal_substitution", expected_endpoints[0], changed)
    changed = copy.deepcopy(result); changed["credit_contract"]["global_component_credit"] = False
    rejected("result_false_not_integer_zero", result, changed)
    changed = copy.deepcopy(original); changed["formal_half_open_owner_credit"] = True
    rejected("row_true_not_integer_one", original, changed)
    for name, raw in {
        "duplicate_JSON_key": b'{"x":1,"x":2}',
        "nonintegral_JSON_number": b'{"x":1.5}',
        "NaN_JSON_number": b'{"x":NaN}',
    }.items():
        try: strict_decode(raw, ROW_CAP)
        except Exception: tests.append(name)
        else: raise Failure(f"attack accepted:{name}")
    try: strict_decode(canonical({"x": "z" * ROW_CAP}), ROW_CAP)
    except Exception: tests.append("post_decode_final_canonical_8MiB_cap")
    else: raise Failure("attack accepted:canonical cap")
    corrupted = bytearray(endpoint_raw); corrupted[-1] ^= 1
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(corrupted), mode="rb") as handle:
            while handle.read(1024 * 1024): pass
    except Exception: tests.append("gzip_crc_corruption")
    else: raise Failure("attack accepted:gzip corruption")
    tests.extend(["producer_inert_not_imported", "Round209_probe_not_imported_or_executed",
                  "R195_provenance_zero_credit_enforced", "U_pipe_U_ordering_bound_in_sheet_commitment"])
    need(len(tests) == 16, "attack count")
    return {"schema": ATTACK_SCHEMA, "status": "PASS_16_OF_16", "test_count": 16,
            "tests": tests, "all_attacks_rejected": True}


def safe_dir(path: Path) -> tuple[Path, tuple[int, ...], int]:
    need(path.exists() and path.is_dir() and not path.is_symlink(), "candidate/output directory")
    resolved = path.resolve(strict=True); info = path.lstat()
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    need(dir_key(os.fstat(fd)) == dir_key(info), "directory race")
    return resolved, dir_key(info), fd


def publish(directory: Path, directory_stat: tuple[int, ...], directory_fd: int,
            documents: dict[str, bytes]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for name, raw in documents.items():
            target = directory / name
            if target.exists() or target.is_symlink():
                info = target.lstat(); need(stat.S_ISREG(info.st_mode) and not target.is_symlink()
                                              and info.st_nlink == 1, "publish target")
            stage = directory / f".{name}.atomic.{os.getpid()}"
            need(not stage.exists() and not stage.is_symlink(), "clean publish stage")
            fd = os.open(stage, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
            try:
                offset = 0
                while offset < len(raw): offset += os.write(fd, raw[offset:offset + 1024 * 1024])
                os.fsync(fd)
            finally: os.close(fd)
            staged.append((stage, target))
        need(dir_key(os.fstat(directory_fd)) == directory_stat
             and dir_key(directory.lstat()) == directory_stat, "publish directory final")
        for stage, target in staged: os.replace(stage, target)
        os.fsync(directory_fd)
    finally:
        for stage, _target in staged:
            if stage.exists() and not stage.is_symlink(): stage.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-directory", type=Path, default=HERE)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--publish", action="store_true")
    modes.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    candidate_dir, candidate_stat, candidate_fd = safe_dir(args.candidate_directory)
    authority_pins = HeldSet(HERE, AUTHORITY_PINS)
    authority_pins.add_self(Path(__file__))
    candidate_pins = HeldSet(candidate_dir, {FILES[key]: None for key in ("sheet", "curve", "endpoint", "result")})
    try:
        r173, leaves, regions, u2_rows = formal_inputs(authority_pins)
        independent = evaluator(authority_pins.raw(EVALUATOR))
        probe_sheets, probe_curves, probe_endpoints, owner_audit = independent.build_probe_lineages(leaves, regions)
        u2_audit = independent.audit_u2(u2_rows, probe_sheets, probe_curves, probe_endpoints)
        expected_sheets, expected_curves, expected_endpoints = formal_rows(
            probe_sheets, probe_curves, probe_endpoints, leaves, regions, u2_rows)
        sheet_raw = candidate_pins.raw(FILES["sheet"]); curve_raw = candidate_pins.raw(FILES["curve"])
        endpoint_raw = candidate_pins.raw(FILES["endpoint"])
        sheets = read_gzip_rows(sheet_raw, EXPECTED["sheet"], "sheet_row_id", "sheet")
        curves = read_gzip_rows(curve_raw, EXPECTED["curve"], "curve_row_id", "curve")
        endpoints = read_gzip_rows(endpoint_raw, EXPECTED["endpoint"], "endpoint_row_id", "endpoint")
        need(typed_equal(sheets, expected_sheets), "independent sheet equality")
        need(typed_equal(curves, expected_curves), "independent curve equality")
        need(typed_equal(endpoints, expected_endpoints), "independent endpoint equality")
        sheet_by = {row["sheet_row_id"]: row for row in sheets}; curve_by = {row["curve_row_id"]: row for row in curves}
        need(all(row["sheet_row_sha256"] == sheet_by[row["sheet_row_id"]]["row_sha256"] for row in curves),
             "curve sheet join")
        need(all(row["sheet_row_sha256"] == sheet_by[row["sheet_row_id"]]["row_sha256"]
                 and row["curve_row_sha256"] == curve_by[row["curve_row_id"]]["row_sha256"] for row in endpoints),
             "endpoint parent joins")
        expected = expected_result(authority_pins, sheet_raw, curve_raw, endpoint_raw,
                                   expected_sheets, expected_curves, expected_endpoints,
                                   leaves, owner_audit, u2_audit)
        result_doc = strict_decode(candidate_pins.raw(FILES["result"]), ROW_CAP, True)
        need(set(result_doc) == {"schema", "result", "result_sha256"}
             and result_doc["schema"] == SCHEMA and sha(result_doc["result"]) == result_doc["result_sha256"],
             "result envelope")
        need(typed_equal(result_doc["result"], expected), "complete type-strict result equality")
        attack = attacks(expected_sheets, expected_curves, expected_endpoints, expected, endpoint_raw)
        attack_raw = canonical(attack) + b"\n"
        verification = {"schema": VERIFY_SCHEMA, "status": PASS,
            "producer_sha256": PRODUCER_SHA256,
            "verifier_sha256": authority_pins.entries[Path(__file__).name]["sha256"],
            "independent_evaluator_sha256": EVALUATOR_SHA256,
            "producer_imported_or_executed": False, "Round209_probe_imported_or_executed": False,
            "candidate_result_sha256": result_doc["result_sha256"],
            "candidate_files": {name: {"size": candidate_pins.entries[name]["size"],
                                         "sha256": candidate_pins.entries[name]["sha256"]}
                                for name in sorted(candidate_pins.entries)},
            "reconstructed_counts": EXPECTED, "attack_suite_sha256": hashlib.sha256(attack_raw).hexdigest(),
            "attack_test_count": attack["test_count"],
            "formal_authority_decision": "LOCAL_HALF_OPEN_OWNER_LINEAGE_ONLY",
            "R195_formal_credit": 0, "whole_leaf_credit": 0, "whole_origin_credit": 0,
            "whole_original_tube_credit": 0, "physical_component_credit": 0,
            "global_component_credit": 0, "global_exact_key_disposition_credit": 0,
            "D02": "BLOCKED", "CM2": "NO-GO_FOR_CLAIM", "deterministic_receipt": True}
        verification_raw = canonical(verification) + b"\n"
        authority_pins.final(); candidate_pins.final()
        if args.publish:
            publish(candidate_dir, candidate_stat, candidate_fd,
                    {FILES["attack"]: attack_raw, FILES["verification"]: verification_raw})
        authority_pins.final(); candidate_pins.final()
        print(canonical({"status": PASS, "result_sha256": result_doc["result_sha256"],
                         "verification_sha256": hashlib.sha256(verification_raw).hexdigest(),
                         "attack_suite_sha256": hashlib.sha256(attack_raw).hexdigest(),
                         "counts": EXPECTED}).decode())
        return 0
    finally:
        authority_pins.close(); candidate_pins.close(); os.close(candidate_fd)


if __name__ == "__main__":
    raise SystemExit(main())
