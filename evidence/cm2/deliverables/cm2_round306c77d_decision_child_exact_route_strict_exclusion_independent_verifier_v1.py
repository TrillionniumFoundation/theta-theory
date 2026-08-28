#!/usr/bin/env python3
"""Independent no-producer verifier/finalizer for the C77d v1 candidate.

The C77d producer and the C72x helper are prohibited inputs.  This verifier
reconstructs the 33,100 C71b numeric decision rows from frozen numeric modules
and published ledgers, compares two isolated candidate stages byte for byte,
then appends an independent verification, one final manifest, and the final
outer receipt in that order.
"""
from __future__ import annotations

import argparse
import collections
import copy
import gzip
import hashlib
import io
import itertools
import json
import os
import stat
import subprocess
import sys
import tempfile
import zlib
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterator, Mapping

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
SITE = ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages"

SCHEMA = "cm2.round306c77d.decision-child-exact-route-strict-exclusion.v1"
CORE_SCHEMA = "cm2.round306c72x.implicit-h1-root-physical-glue-core.v1"
PREFIX = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1"
ROWS = PREFIX + "_rows.jsonl.gz"
INCIDENCE = PREFIX + "_root_incidence.jsonl.gz"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
CANDIDATE_MANIFEST = PREFIX + "_candidate_manifest.sha256"
LOCK = "ZERO_CREDIT_STAGED_C77D_DECISION_ROUTE_STRICT_EXCLUSION_ONLY.lock"
VERIFY = PREFIX + "_independent_verification_v1.json"
FINAL_MANIFEST = PREFIX + "_final_manifest_v1.sha256"
OUTER = PREFIX + "_final_outer_receipt_v1.json"
PRODUCER_BASENAME = PREFIX + ".py"
PRODUCER_DECLARED_PIN = "cae2a2139e2330e3566e42c0d5265a2390567af44a9f69329116e49c0b24edaf"

CONTRACT = OUT / (PREFIX.removesuffix("_v1") + "_contract_v1.json")
SCHEMAS = OUT / (PREFIX.removesuffix("_v1") + "_closed_schemas_v1.json")
CONTRACT_FILE_PIN = "0245ceb9b76d7d5a0271f92002b2a6d54fff6451155b1f99ccb8af8a467e6c8a"
CONTRACT_OBJECT_PIN = "5fffc6b21e30970bb3805b1945a744b4d24ca9056eae40d1bb1363b61d6d66d4"
SCHEMAS_FILE_PIN = "ccfc507e65996a31d568bf7fe22142ce2c05338d34627b480202a7d2b804529c"
SCHEMAS_OBJECT_PIN = "684764629f81a6ad96110f9061f5a2e9e9de740e8725597bfd6b1ca26348638c"

C71B_STAGE = ROOT / ".cm2-runtime/c71b-v3-final-75c21279"
C71B_ROWS_NAME = (
    "cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_rows.jsonl.gz")
C71B_RESULT_NAME = (
    "cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_result.json")
C71B_VERIFY_NAME = "independent_verification_v3_1.json"
C71B_RECEIPT_NAME = "dual_build_publication_completion_receipt_v3.json"
C71B_PINS = {
    C71B_ROWS_NAME:
        "f9f04044809e46b9811d52abef94844d84b058a2f0c3fb6f5b9f97f2302cbec6",
    C71B_RESULT_NAME:
        "5ede807e4860b60fe8582597cc6be10cdfdc7b3a0eeba57ced317f4980092246",
    C71B_VERIFY_NAME:
        "ee105922e263d9cea551088ee67c350cc9adc4d9f375a8584428e4fa55575612",
    C71B_RECEIPT_NAME:
        "3a6cfa624fab8cd1b787d3facd139cf9e055a008236864d894d2633522fe9fbc",
}
C71B_OBJECT_PINS = {
    C71B_RESULT_NAME:
        "75c21279e3440a32116e67c20f12c7ec9d299491d018e2982ab18d68118d4158",
    C71B_VERIFY_NAME:
        "c45c5b19daeaef930f981810722460424a0d55c8302380829757e2132754f5c3",
    C71B_RECEIPT_NAME:
        "d7fd8322b72fad933bb80542913b00cb54c5d7a3d93bf8cb7601aefa5daadbcd",
}

C35 = (ROOT /
       ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-"
       "43f2cb35f9817ae2/path_occurrences.jsonl.gz")
C37 = (ROOT /
       ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-"
       "be0d65d5e1cc3c38/reflected_r1648_occurrences.jsonl.gz")
C38 = (ROOT /
       ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-"
       "0d5047fe3a316133/collision1_2_child_pairs.jsonl.gz")
C35_RESULT = C35.parent / "result.json"
C37_RESULT = C37.parent / "result.json"
C38_RESULT = C38.parent / "result.json"
C35_AUDIT = (ROOT /
    ".cm2-runtime/audit/c35-independent-audit-20260810T145205Z-"
    "1583ed4d15344427/independent_audit.json")
C37_AUDIT = (ROOT /
    ".cm2-runtime/audit/c37-independent-audit-20260810T155248Z-"
    "49ba0249b7685f58/independent_audit.json")
C38_AUDIT = (ROOT /
    ".cm2-runtime/audit/c38-independent-audit-20260810T180628Z-"
    "c149ee1692741ec7/independent_audit.json")
UPSTREAM_PINS = {
    "C35_PATH": "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66",
    "C35_RESULT": "3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
    "C35_AUDIT": "d45582baed7dea4246864afd42664df9442c6e6e45afa4562bc36ae0c8050efe",
    "C37_PATH": "7c87829f6ef883b7928ff8a313d5bfcf240383c51a9040739de1cfe7e617bef5",
    "C37_RESULT": "5b968d957cbca2a4f8aec855a44643f5add7fe0244d933401dfdef9ad7be61f3",
    "C37_AUDIT": "e707314bc21032af0b344b664825ab683d411f1391c041cb92efc35d6807d7eb",
    "C38_CHILDREN": "0347849c0368368430f5456b71cd4a4bce4e5912c8a3da33649cfac35b1708a2",
    "C38_RESULT": "094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501",
    "C38_AUDIT": "e3fa567b3553415f5357ead66feb00b860c050a6ea687aeb7719666362ffac79",
}
UPSTREAM_OBJECT_PINS = {
    "C35_AUDIT": "914b1440a311a922819e488e4ed4ef39cb87df74b884f2fe7821336f7cb8d33a",
    "C37_AUDIT": "b5be1e8d97337ff90f514695f06bbb1156c606324a50b05766ed080a261d8044",
    "C38_AUDIT": "5e6d0a7a0d1f2216014ac5ef5858ddda6738802a1a02e5749a1f674f766eddf2",
}

CHART_MANIFEST = OUT / "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
CHART_MANIFEST_PIN = "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b"
CHART_CERTIFICATE_PIN = "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1"
CHART_DEPENDENCIES = {
    "cm2-gate3-endpoint-identity-refinement-manifest-2026-07-15.json":
        "dc394ee38b1e1c36a3cabf27d69279576a8f58f40705537c38c04524781b37d7",
    "cm2-gate3-first-miss-stratification-manifest-2026-07-15.json":
        "58f2460f7bbfb5bab6c0c7cb48c706482359ffb423dc35abcbd2069220db1388",
    "cm2-v52-manifest.sha256":
        "5cef5b8e60f0cfe2291da6bb34b2c57eed6cf2d1a13d164b74b566f752b6b368",
    "cm2_gate3_endpoint_identity_refinement_cert.py":
        "547c48d1b350fb1781719f936634b72c5664b4842e1f33fddb02c33bcbdf7563",
    "cm2_gate3_global_physical_subrow_atlas_cert.py":
        "0445331455e5cc8d17c3393108e997712502cdb606f65ac57de6e0b698b3c1fc",
}

NUMERIC_PINS = {
    "r185": "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    "r178": "06075baac268e8e6c9deeeedae3e502b3a96630f3650c0b783c2b2a77dbd23f9",
    "atlas": "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "ge": "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "registry": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "r139": "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    "lower": "42d749dccea86aa3a122707db0226def176e75047d5dcb4bf19826b50e09282b",
    "round136": "4e78309d5275bf367e6df03509c40ebaaac6f344c7948446a25b3b508c8c2bc2",
    "time3": "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
    "time2": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "core": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "step1": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
}

PRECISION = 384
FROZEN_OWNER = "W[1,0]"
EXPECTED_WORD = (
    "gate5-word:266945:f86c66902f1acc76521086a8d15abc55cf7a1d77a13bf03fb64dffbf9eb47ea8")
EXPECTED_OWNERS = {"G[0,0]", "G[0,1]"}
CORE_INDEX = {"W:E": 14, "W:N": 17, "W:S": 20, "W:W": 23}
TARGET_PAIRS = {31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853}
EXPECTED_INPUT = {
    "LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX": 1,
    "LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX": 7352,
    "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS": 8093,
    "LOCAL_H1_CLIPPED_GRAPH_AND_TWO_OFF_GRAPH_REGIONS": 17654,
}
EXPECTED_FRESH = {"STRICT_NEGATIVE": 1, "STRICT_POSITIVE": 7352,
                  "CLIPPED": 25747}
EXPECTED_ROUTE = {
    "COLLISION1_OUTGOING_CHART_MISMATCH": 1,
    "COLLISION1_OFFICIAL_WORD_MISMATCH": 31338,
    "COLLISION2_STRICT_OWNER_MISMATCH": 1761,
}
PURE_CORE_DECLARED_PIN = "98f13225cbd9caf886242fbedf5071846b77df192727a7bdbc4075eb89a8adc8"
ZERO_FIELDS = ("formal_credit", "D02_gate_credit", "CM2_credit",
               "whole_parent_credit", "global_installed_credit")


class Reject(RuntimeError):
    """Fail-closed validation exception."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def raw_digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def reject_number(token: str) -> Any:
    raise Reject("non-integral JSON number:" + token)


def parse_json(raw: bytes, label: str, newline: bool = True,
               canonical_required: bool = True) -> dict[str, Any]:
    try:
        value = json.loads(raw, object_pairs_hook=no_duplicates,
                           parse_float=reject_number,
                           parse_constant=reject_number)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Reject(label + ":invalid JSON") from error
    need(type(value) is dict, label + ":JSON object")
    if canonical_required:
        need(raw == canonical(value) + (b"\n" if newline else b""),
             label + ":canonical object")
    return value


def file_sha(path: Path) -> str:
    need(path.name != PRODUCER_BASENAME, "producer source is prohibited input")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link:" + str(path))
        hasher = hashlib.sha256()
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
        after = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
        identity = lambda value: (
            value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)
        need(identity(before) == identity(after) == identity(named),
             "TOCTOU:" + str(path))
        return hasher.hexdigest()
    finally:
        os.close(descriptor)


def safe_bytes(path: Path, expected: str | None = None) -> bytes:
    actual = file_sha(path)
    if expected is not None:
        need(actual == expected, "file pin:" + str(path))
    raw = path.read_bytes()
    need(raw_digest(raw) == actual, "terminal stable read:" + str(path))
    return raw


def close_row(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":row closure")


def close_object(value: Mapping[str, Any], label: str,
                 expected: str | None = None) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(type(claim) is str and claim == digest(body) and
         (expected is None or claim == expected), label + ":object closure")


def one_member(raw: bytes) -> None:
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    for offset in range(0, len(raw), 1 << 20):
        decoder.decompress(raw[offset:offset + (1 << 20)])
        need(decoder.unused_data == b"", "single-member gzip/no trailing")
    decoder.flush()
    need(decoder.eof and decoder.unused_data == b"" and
         decoder.unconsumed_tail == b"", "complete single-member gzip")


def iter_jsonl(path: Path, expected_sha: str | None = None,
               expected_count: int | None = None) -> Iterator[dict[str, Any]]:
    raw = safe_bytes(path, expected_sha)
    one_member(raw)
    count = 0
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
        for line in stream:
            need(line.endswith(b"\n"), "JSONL newline:" + str(path))
            row = parse_json(line, "JSONL row")
            close_row(row, "JSONL row")
            count += 1
            yield row
    if expected_count is not None:
        need(count == expected_count, "JSONL count:" + str(path))


def arb_payload(value: Any) -> dict[str, Any]:
    return {"lower": str(value.lower()), "upper": str(value.upper()),
            "contains_zero": bool(value.contains(0))}


def sign(value: Any) -> int:
    return 1 if bool(value > 0) else -1 if bool(value < 0) else 0


def exact_faces(pair: int, box: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    t0, t1 = box["t"]
    p0, p1 = box["p"]
    return {
        "T_LOW": {"pair_index": pair, "fixed_axis": "t", "fixed_value": t0,
                  "varying_axis": "p", "varying_interval": [p0, p1]},
        "T_HIGH": {"pair_index": pair, "fixed_axis": "t", "fixed_value": t1,
                   "varying_axis": "p", "varying_interval": [p0, p1]},
        "P_LOW": {"pair_index": pair, "fixed_axis": "p", "fixed_value": p0,
                  "varying_axis": "t", "varying_interval": [t0, t1]},
        "P_HIGH": {"pair_index": pair, "fixed_axis": "p", "fixed_value": p1,
                   "varying_axis": "t", "varying_interval": [t0, t1]},
    }


def face_key(spec: Mapping[str, Any]) -> str:
    return digest({"schema": CORE_SCHEMA + ".exact-face-key", **dict(spec)})


def root_id(spec: Mapping[str, Any]) -> str:
    return digest({"schema": CORE_SCHEMA + ".unique-H1-edge-root",
                   "collision1_owner": FROZEN_OWNER,
                   "equation": "H1=nx^2-ny^2", **dict(spec)})


def first_difference(left: Any, right: Any, path: str = "$"
                     ) -> str | None:
    if type(left) is not type(right):
        return path + ":type"
    if isinstance(left, dict):
        if set(left) != set(right):
            return path + ":keys:" + repr(sorted(set(left) ^ set(right)))
        for key in sorted(left):
            found = first_difference(left[key], right[key],
                                     path + "." + str(key))
            if found is not None:
                return found
        return None
    if isinstance(left, list):
        if len(left) != len(right):
            return path + ":length"
        for ordinal, (a, b) in enumerate(zip(left, right, strict=True)):
            found = first_difference(a, b, path + f"[{ordinal}]")
            if found is not None:
                return found
        return None
    return None if left == right else path + ":value"


def chart_authority() -> dict[str, Any]:
    raw = safe_bytes(CHART_MANIFEST, CHART_MANIFEST_PIN)
    manifest = parse_json(raw, "chart manifest", canonical_required=False)
    need(manifest["certificate_sha256"] == CHART_CERTIFICATE_PIN and
         manifest["dependencies"] == CHART_DEPENDENCIES and
         manifest["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED",
         "chart authority certificate")
    rule = manifest["result"]["unique_half_open_owner_rule"]
    need(rule["diagonal_tie"] == "E or W owns; N or S excludes" and
         rule["same_physical_normal_on_paired_representations"] is True and
         rule["duplicate_trace_is_identified_not_added"] is True and
         manifest["result"]["scope_limits"]
             ["ownership_rule_applies_to_analytic_strata"] is True,
         "chart authority rule")
    for name, expected in CHART_DEPENDENCIES.items():
        need(file_sha(OUT / name) == expected, "chart dependency pin:" + name)
    return {
        "manifest_file_sha256": CHART_MANIFEST_PIN,
        "certificate_sha256": CHART_CERTIFICATE_PIN,
        "eight_chart_seam_ownership": "CERTIFIED",
        "diagonal_tie": "E or W owns; N or S excludes",
        "same_physical_normal_on_paired_representations": True,
        "duplicate_trace_is_identified_not_added": True,
    }


def load_closed_contract() -> tuple[dict[str, Any], dict[str, Any]]:
    need("TO_BE_PATCHED" not in {
        CONTRACT_FILE_PIN, CONTRACT_OBJECT_PIN,
        SCHEMAS_FILE_PIN, SCHEMAS_OBJECT_PIN}, "contract pins frozen")
    contract = parse_json(safe_bytes(CONTRACT, CONTRACT_FILE_PIN), "contract",
                          canonical_required=False)
    schemas = parse_json(safe_bytes(SCHEMAS, SCHEMAS_FILE_PIN), "schemas",
                         canonical_required=False)
    close_object(contract, "contract", CONTRACT_OBJECT_PIN)
    close_object(schemas, "schemas", SCHEMAS_OBJECT_PIN)
    need(contract["schema"] == SCHEMA.rsplit(".", 1)[0] + ".contract.v1" and
         schemas["schema"] == SCHEMA.rsplit(".", 1)[0] + ".closed-schemas.v1",
         "contract/schema names")
    return contract, schemas


def load_json_object(path: Path, expected_file: str, expected_object: str,
                     label: str) -> dict[str, Any]:
    value = parse_json(safe_bytes(path, expected_file), label)
    close_object(value, label, expected_object)
    return value


def frozen_upstreams() -> dict[str, Any]:
    result = load_json_object(
        C71B_STAGE / C71B_RESULT_NAME, C71B_PINS[C71B_RESULT_NAME],
        C71B_OBJECT_PINS[C71B_RESULT_NAME], "C71b result")
    verification = load_json_object(
        C71B_STAGE / C71B_VERIFY_NAME, C71B_PINS[C71B_VERIFY_NAME],
        C71B_OBJECT_PINS[C71B_VERIFY_NAME], "C71b verification")
    receipt = load_json_object(
        C71B_STAGE / C71B_RECEIPT_NAME, C71B_PINS[C71B_RECEIPT_NAME],
        C71B_OBJECT_PINS[C71B_RECEIPT_NAME], "C71b receipt")
    need(result["coverage"]["child_level_H1_full_box_closed_count"] == 33100 and
         result["coverage"]["blocker_source_child_count"] == 134155 and
         verification["status"].startswith("PASS_NO_PRODUCER_EXACT_REBUILD") and
         verification["producer_source_imported_read_decoded_compiled_or_executed"]
            is False and
         receipt["independent_verification"]["file_sha256"] ==
            C71B_PINS[C71B_VERIFY_NAME] and
         receipt["terminal_byte_replay"]["all_stable_single_link_exact_sha256"]
            is True and
         all(result[field] == 0 for field in
             ("formal_credit", "D02_gate_credit", "whole_parent_credit")) and
         result["candidate_is_authority"] is False and
         result["global_consumption_ready"] is False,
         "C71b corrected zero-credit release")
    need(file_sha(C71B_STAGE / C71B_ROWS_NAME) == C71B_PINS[C71B_ROWS_NAME],
         "C71b rows pin")

    paths = {"C35_PATH": C35, "C35_RESULT": C35_RESULT,
             "C35_AUDIT": C35_AUDIT, "C37_PATH": C37,
             "C37_RESULT": C37_RESULT, "C37_AUDIT": C37_AUDIT,
             "C38_CHILDREN": C38, "C38_RESULT": C38_RESULT,
             "C38_AUDIT": C38_AUDIT}
    for name, path in paths.items():
        need(file_sha(path) == UPSTREAM_PINS[name], "upstream pin:" + name)
    audits = {}
    for name, path in (("C35_AUDIT", C35_AUDIT),
                       ("C37_AUDIT", C37_AUDIT),
                       ("C38_AUDIT", C38_AUDIT)):
        value = parse_json(safe_bytes(path, UPSTREAM_PINS[name]), name)
        close_object(value, name, UPSTREAM_OBJECT_PINS[name])
        need(value["status"].startswith("PASS_INDEPENDENT_"),
             name + ":independent PASS")
        audits[name] = value["object_sha256"]
    return {
        "C71b_result_object_sha256": result["object_sha256"],
        "C71b_verification_object_sha256": verification["object_sha256"],
        "C71b_receipt_object_sha256": receipt["object_sha256"],
        "independent_audit_object_sha256": audits,
    }


def first_two(path: Path, sha: str) -> list[dict[str, Any]]:
    output = []
    for ordinal, row in enumerate(iter_jsonl(path, sha, 1648)):
        if ordinal < 2:
            output.append(row)
    need(len(output) == 2, "two transition anchors")
    return output


def origin_map() -> dict[int, str]:
    origins: dict[int, str] = {}
    for row in iter_jsonl(C38, UPSTREAM_PINS["C38_CHILDREN"], 10486):
        pair = row["pair_index"]
        if pair in TARGET_PAIRS:
            value = row["representative_origin_key"]
            need(pair not in origins or origins[pair] == value,
                 "C38 origin consistency")
            origins[pair] = value
    need(set(origins) == TARGET_PAIRS, "C38 origin coverage")
    return origins


def registry_anchors() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    original = first_two(C35, UPSTREAM_PINS["C35_PATH"])
    reflected = first_two(C37, UPSTREAM_PINS["C37_PATH"])
    need(original[0]["official_word_key_id"] == EXPECTED_WORD and
         original[0]["outgoing_chart"] == "W" and
         {original[1]["selected_absolute_owner_id"],
          reflected[1]["selected_absolute_owner_id"]} == EXPECTED_OWNERS,
         "C35/C37 route anchors")
    return original, reflected


def expected_graph_glue(normal_signs: dict[str, int], roots: list[str],
                        route: dict[str, Any],
                        authority: dict[str, Any]) -> dict[str, Any]:
    shadow = "N" if normal_signs["ny"] > 0 else "S"
    return {
        "schema": CORE_SCHEMA + ".implicit-graph-state-glue",
        "implicit_equation": "H1=nx^2-ny^2=0",
        "graph_definition":
            "UNIQUE_REGULAR_ROOT_GRAPH_BETWEEN_TWO_EXACT_FACE_ROOTS",
        "boundary_root_ids": roots,
        "paired_charts": ["W", shadow],
        "half_open_physical_owner_chart": "W",
        "shadow_chart": shadow,
        "chart_authority": authority,
        "same_physical_normal_under_cross_chart_transform": True,
        "same_physical_contact_and_outgoing_state_under_cross_chart_transform":
            True,
        "cross_chart_transform": {
            "input": "W-owned implicit H1 root state",
            "output": shadow + " shadow representation of the same physical normal",
            "physical_normal_identity": "(nx,ny)_W=(nx,ny)_shadow",
            "physical_state_identity":
                "contact_W=contact_shadow; outgoing_W=outgoing_shadow"},
        "W_route_evaluated_on_closed_ambient_box": True,
        "W_route_strict_margins_restrict_to_graph": True,
        "graph_exit_class": "STRICT_EXCLUSION",
        "graph_exclusion_reason": route["outcome"],
        "graph_is_not_source_grazing_or_cemetery": True,
        "graph_is_not_counted_as_a_coordinate_terminal": True,
        "duplicate_physical_trace_added": False,
        "full_dimensional_Kraft_weight": "0",
    }


def collision0_delta(r185: Any, parent: str, box: Any, target: str) -> Any:
    return r185.ad_root(r185.ad_initial_geometry(parent, box), target)["Delta"]


def next_owner(r139: Any, state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    time2 = r139.lower.time3.time2_cert
    future = []
    census = collections.Counter()
    for identifier in time2.translated_candidate_ids(FROZEN_OWNER, state["chart"]):
        row = time2.candidate_root(
            state["contact_x"], state["contact_y"], state["outgoing_x"],
            state["outgoing_y"], state["s"], identifier)
        kind = row["classification"]
        census[kind] += 1
        need(kind in {"no_real_intersection", "intersection_strictly_behind",
                      "strict_future_near_root"},
             "collision2 competitor classification")
        if kind == "strict_future_near_root":
            future.append((identifier, row))
    winners = [(identifier, row) for identifier, row in future if all(
        identifier == other or bool(row["near"] < other_row["near"])
        for other, other_row in future)]
    need(len(winners) == 1, "unique collision2 owner")
    selected_id, selected = winners[0]
    gaps = [row["near"] - selected["near"] for identifier, row in future
            if identifier != selected_id]
    need(all(bool(gap > 0) for gap in gaps), "collision2 strict owner gaps")
    return selected_id, {
        "classification_census": dict(sorted(census.items())),
        "strict_future_candidate_count": len(future),
        "all_owner_order_gaps_strict": True,
    }


def route_outcome(r185: Any, r139: Any, origin: str, box: Any,
                  cores: tuple[Any, ...], pair_index: dict[Any, Any],
                  pattern_index: dict[Any, Any]) -> dict[str, Any]:
    raw = r185.ad_root(r185.ad_initial_geometry(origin, box), FROZEN_OWNER)
    delta = r185.centered_enclosure(
        lambda parent, current_box, target: collision0_delta(
            r185, parent, current_box, target),
        origin, box, FROZEN_OWNER, raw["Delta"])
    need(bool(delta > 0), "centered collision1 Delta")
    radius = raw["radius"].value
    radical = delta.sqrt()
    transverse = raw["transverse"].value
    near = raw["ell"].value - radical
    tau = r139.lower.time3.time2_cert.step1.arbq(
        r139.lower.time3.time2_cert.first_hit.TAU_MAX)
    need(bool(near > 0) and bool(near < tau), "collision1 near root margins")
    chart_id = ":".join(origin.split(":")[:2])
    atom = r139.lower.step1.Atom(
        CORE_INDEX[chart_id], cores[CORE_INDEX[chart_id]],
        box.t0, box.t1, box.p0, box.p1, Q(0), Q(0), "audit")
    initial = r139.lower.round136.initial_state(atom)
    sx, sy = initial["outgoing_x"], initial["outgoing_y"]
    nx = (-radical * sx + transverse * sy) / radius
    ny = (-radical * sy - transverse * sx) / radius
    radial = radical / radius
    cx, cy = r139.lower.time3.time2_cert.target_center(
        FROZEN_OWNER, initial["s"])
    state = {
        "contact_x": cx + radius * nx,
        "contact_y": cy + radius * ny,
        "outgoing_x": radial * nx - (transverse / radius) * ny,
        "outgoing_y": radial * ny + (transverse / radius) * nx,
        "s": initial["s"], "chart": "W", "normal_x": nx,
        "normal_y": ny, "p": transverse / radius,
    }
    owner = {"selected_target_id": FROZEN_OWNER, "selected_root": near,
             "normal_x": nx, "normal_y": ny,
             "p": transverse / radius, "cosine": radial}
    word, error = r139.lower.round136.translation_normalized_official_word(
        initial, "W[0,0]", owner, pair_index, pattern_index)
    need(word is not None and error is None, "official word materialized")
    compact = r139.lower.round136.compact_key(word["key"])
    word_id = compact["official_word_key_id"]
    evidence = {
        "method": "CHART_FREE_PHYSICAL_STATE_THEN_W_HALF_OPEN_OWNER_ROUTE",
        "closed_rectangular_box_enclosure": True,
        "therefore_applies_to_implicit_H1_graph_subset": True,
        "centered_Delta": arb_payload(delta),
        "near_root": arb_payload(near),
        "tau_minus_near": arb_payload(tau - near),
        "physical_state_formula": {
            "contact": "target_center(s)+R*(nx,ny)",
            "outgoing": "(sqrt(Delta)/R)*(nx,ny)+(p/R)*(-ny,nx)"},
        "computed_official_word_key_id": word_id,
        "expected_official_word_key_id": EXPECTED_WORD,
        "registry_row_sha256": compact["registry_row_sha256"],
        "ordered_clean_wall_record": word["ordered_clean_wall_record"],
    }
    if word_id != EXPECTED_WORD:
        return {**evidence, "outcome": "COLLISION1_OFFICIAL_WORD_MISMATCH",
                "selected_collision2_owner": None}
    selected, order = next_owner(r139, state)
    need(selected not in EXPECTED_OWNERS,
         "unexpected expected-owner match requires collision3 handoff")
    return {
        **evidence, "outcome": "COLLISION2_STRICT_OWNER_MISMATCH",
        "selected_collision2_owner": selected,
        "collision2_owner_order": order,
        "expected_collision2_owner_set": sorted(EXPECTED_OWNERS),
    }


def geometry_and_roots(r185: Any, origin: str, box: Any, pair: int,
                       raw_box: Mapping[str, Any]) -> tuple[
                           dict[str, Any], str, list[str], dict[str, int]]:
    full, nx, ny = r185.collision1_h1_ad(origin, box, FROZEN_OWNER)
    dt, dp = sign(full.derivative[0]), sign(full.derivative[1])
    nx_sign, ny_sign = sign(nx.value), sign(ny.value)
    need(dt != 0 and dp != 0 and nx_sign != 0 and ny_sign != 0,
         "strict derivatives and normal components")
    signs: list[int] = []
    corner_records = []
    for t, p in itertools.product(raw_box["t"], raw_box["p"]):
        point = r185.point_box(box, Q(t), Q(p), Q(0), ".audit.corner")
        value, _nx, _ny = r185.collision1_h1_ad(
            origin, point, FROZEN_OWNER)
        current = sign(value.value)
        need(current != 0, "strict corner")
        signs.append(current)
        corner_records.append({"point": {"t": t, "p": p, "s": "0"},
                               "H1": arb_payload(value.value),
                               "sign": current})
    common = {
        "precision_bits": PRECISION,
        "equation": "H1=nx^2-ny^2",
        "full_box_natural_interval": arb_payload(full.value),
        "full_box_derivatives": {
            "t": arb_payload(full.derivative[0]),
            "p": arb_payload(full.derivative[1]),
            "s": arb_payload(full.derivative[2])},
        "normal_component_bounds": {
            "nx": arb_payload(nx.value), "ny": arb_payload(ny.value)},
        "normal_component_signs": {"nx": nx_sign, "ny": ny_sign},
        "four_strict_corner_records": corner_records,
        "corner_zero_incidence_count": 0,
    }
    if len(set(signs)) == 1:
        side = signs[0]
        fresh = "STRICT_NEGATIVE" if side < 0 else "STRICT_POSITIVE"
        geometry = {
            **common, "kind": "STRICT_WHOLE_CHILD_H1_SIDE",
            "proof_method": "STRICT_DT_DP_MONOTONE_EXTREMAL_CORNER",
            "strict_H1_sign": "NEGATIVE" if side < 0 else "POSITIVE",
            "boundary_root_count": 0,
            "partition": {
                "H1_LT_0": "EXACT_CHILD" if side < 0 else "EMPTY",
                "H1_EQ_0": "EMPTY",
                "H1_GT_0": "EXACT_CHILD" if side > 0 else "EMPTY",
                "pairwise_disjoint": True, "union_exact_child": True},
        }
        return geometry, fresh, [], {"nx": nx_sign, "ny": ny_sign}

    specs = exact_faces(pair, raw_box)
    edge_pairs = {"T_LOW": (0, 1), "T_HIGH": (2, 3),
                  "P_LOW": (0, 2), "P_HIGH": (1, 3)}
    edges = []
    roots = []
    root_ids = []
    for edge_id in ("T_LOW", "T_HIGH", "P_LOW", "P_HIGH"):
        left, right = edge_pairs[edge_id]
        ordered = [signs[left], signs[right]]
        spec = specs[edge_id]
        tangent = dt if spec["varying_axis"] == "t" else dp
        need((tangent > 0 and ordered[0] <= ordered[1]) or
             (tangent < 0 and ordered[0] >= ordered[1]),
             "strict edge monotone order")
        base = {"edge_id": edge_id, "exact_face": spec,
                "face_key_sha256": face_key(spec),
                "ordered_endpoint_signs": ordered}
        if ordered[0] != ordered[1]:
            identifier = root_id(spec)
            root_ids.append(identifier)
            edges.append({**base,
                          "disposition": "ONE_UNIQUE_INTERIOR_H1_ROOT",
                          "root_id": identifier})
            roots.append({
                "root_id": identifier, "edge_id": edge_id,
                "exact_face": spec, "face_key_sha256": face_key(spec),
                "definition": "UNIQUE_H1_ZERO_IN_OPEN_EXACT_FACE",
                "existence_by_IVT": True,
                "uniqueness_by_strict_tangential_derivative": True,
                "not_a_corner": True})
        else:
            edges.append({**base, "disposition": "STRICT_NO_H1_ROOT",
                          "root_id": None,
                          "strict_H1_sign":
                              "NEGATIVE" if ordered[0] < 0 else "POSITIVE"})
    need(len(roots) == 2, "two exact face roots")
    geometry = {
        **common,
        "kind": "EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFFGRAPH_REGIONS",
        "proof_method":
            "STRICT_DT_DP_FOUR_CORNERS_FOUR_FACES_TWO_ROOTS_IFT",
        "boundary_root_count": 2,
        "boundary_edges": edges,
        "boundary_roots": roots,
        "single_connected_graph_arc": True,
        "partition": {
            "H1_LT_0": "EXACT_OPEN_NEGATIVE_REGION",
            "H1_EQ_0": "EXACT_SINGLE_REGULAR_GRAPH_ARC",
            "H1_GT_0": "EXACT_OPEN_POSITIVE_REGION",
            "pairwise_disjoint": True, "union_exact_child": True,
            "W_half_open_owns_H1_EQ_0": True,
            "graph_full_dimensional_Kraft_weight": "0"},
    }
    return geometry, "CLIPPED", root_ids, {"nx": nx_sign, "ny": ny_sign}


def expected_row(c71b: dict[str, Any], ordinal: int, origin: str,
                 geometry: dict[str, Any], fresh: str, roots: list[str],
                 normal_signs: dict[str, int], route: dict[str, Any] | None,
                 authority: dict[str, Any], registry: str) -> dict[str, Any]:
    old = c71b["arrangement_disposition"]
    expected_fresh = {
        "LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX": "STRICT_NEGATIVE",
        "LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX": "STRICT_POSITIVE",
        "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS": "CLIPPED",
        "LOCAL_H1_CLIPPED_GRAPH_AND_TWO_OFF_GRAPH_REGIONS": "CLIPPED",
    }
    need(expected_fresh.get(old) == fresh, "C71b disposition/fresh geometry")
    if fresh == "STRICT_NEGATIVE":
        outcome = "COLLISION1_OUTGOING_CHART_MISMATCH"
        downstream = None
        glue_kind = "STRICT_NON_W_CHART_NO_DIAGONAL_SEAM"
        exits = [{
            "stratum": "EXACT_CHILD", "exit_class": "STRICT_EXCLUSION",
            "reason": outcome,
            "expected_outgoing_chart": "W",
            "actual_outgoing_chart":
                "N" if normal_signs["ny"] > 0 else "S"}]
    elif fresh == "STRICT_POSITIVE":
        need(route is not None, "positive route evidence")
        outcome = route["outcome"]
        downstream = route
        glue_kind = "STRICT_W_CHART_NO_DIAGONAL_SEAM"
        exits = [{"stratum": "EXACT_CHILD", "exit_class": "STRICT_EXCLUSION",
                  "chart": "W", "downstream": route}]
    else:
        need(fresh == "CLIPPED" and route is not None and len(roots) == 2,
             "clipped route and roots")
        outcome = route["outcome"]
        downstream = route
        glue_kind = "W_HALF_OPEN_GRAPH_OWNER_WITH_N_OR_S_SHADOW"
        exits = [
            {"stratum": "H1_LT_0", "exit_class": "STRICT_EXCLUSION",
             "reason": "COLLISION1_OUTGOING_CHART_MISMATCH",
             "expected_outgoing_chart": "W",
             "actual_outgoing_chart":
                "N" if normal_signs["ny"] > 0 else "S"},
            {"stratum": "H1_GT_0", "exit_class": "STRICT_EXCLUSION",
             "chart": "W", "downstream": route},
            {"stratum": "H1_EQ_0", "exit_class": "STRICT_EXCLUSION",
             "chart": "W", "downstream": route,
             "graph_is_not_a_terminal": True,
             "physical_chart_glue": expected_graph_glue(
                 normal_signs, roots, route, authority)},
        ]
    body = {
        "schema": SCHEMA + ".decision-row",
        "ordinal": ordinal,
        "C71b_arrangement_row_sha256": c71b["row_sha256"],
        "C65_aggregate_child_row_sha256":
            c71b["C65_aggregate_leaf_row_sha256"],
        "C61_aggregate_leaf_row_sha256":
            c71b["source_C61_aggregate_leaf_row_sha256"],
        "pair_index": c71b["pair_index"],
        "source_path": c71b["source_path"],
        "child_path": c71b["child_path"],
        "parent_key": origin,
        "exact_representative_box": c71b["exact_representative_box"],
        "input_arrangement_disposition": old,
        "fresh_geometry_kind": fresh,
        "H1_geometry": geometry,
        "stratum_exits": exits,
        "route_outcome": outcome,
        "closed_box_downstream_evidence": downstream,
        "physical_chart_glue_kind": glue_kind,
        "whole_child_strict_exclusion_closed": True,
        "physical_chart_glue_closed": True,
        "allowed_exit_closed_for_every_stratum": True,
        "explicit_residual_strata": 0,
        "sealed_collision3_handoff_count": 0,
        "collision3_handoff": None,
        "current_disposition":
            "STAGED_ZERO_CREDIT_WHOLE_CHILD_STRICT_EXCLUSION",
        "candidate_is_authority": False,
        "global_consumption_ready": False,
        "additional_dyadic_depth": 0,
        "official_registry_sha256": registry,
        "formal_credit": 0,
        "D02_gate_credit": 0,
        "CM2_credit": 0,
        "whole_parent_credit": 0,
        "global_installed_credit": 0,
    }
    return {**body, "row_sha256": digest(body)}


def endpoint_occurrences(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    output = []
    for root in candidate["H1_geometry"].get("boundary_roots", []):
        record = {
            "C71b_arrangement_row_sha256":
                candidate["C71b_arrangement_row_sha256"],
            "C65_aggregate_child_row_sha256":
                candidate["C65_aggregate_child_row_sha256"],
            "child_path": candidate["child_path"],
            "edge_id": root["edge_id"],
            "exact_face": root["exact_face"],
        }
        output.append({"root_id": root["root_id"], "record": record,
                       "occurrence_sha256": digest(record)})
    return output


def worker() -> int:
    payload = json.load(sys.stdin)
    sys.path.insert(0, str(SITE))
    sys.path.insert(0, str(OUT))
    from flint import ctx
    ctx.prec = PRECISION
    import cm2_round185_preconditioned_c1_residual_refinement as r185
    import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
    need(PRODUCER_BASENAME.removesuffix(".py") not in sys.modules and
         all("round306c72x" not in name for name in sys.modules),
         "prohibited producer/helper module dependency")
    modules = {
        "r185": r185, "r178": r185.r178, "atlas": r185.atlas,
        "ge": r185.ge, "registry": r185.registry, "r139": r139,
        "lower": r139.lower, "round136": r139.lower.round136,
        "time3": r139.lower.time3,
        "time2": r139.lower.time3.time2_cert,
        "core": r139.lower.core_cert, "step1": r139.lower.step1,
    }
    need({name: file_sha(Path(module.__file__).resolve())
          for name, module in modules.items()} == NUMERIC_PINS, "numeric pins")
    authority = chart_authority()
    origins = {int(key): value for key, value in payload["origins"].items()}
    pair_index, pattern_index, registry = (
        r139.lower.component_cert.key_index_tables())
    cores = tuple(r139.lower.core_cert.physical_cores())
    input_census = collections.Counter()
    fresh_census = collections.Counter()
    route_census = collections.Counter()
    graph_route_census = collections.Counter()
    route_by_input: dict[str, collections.Counter[str]] = (
        collections.defaultdict(collections.Counter))
    pair_census = collections.Counter()
    pair_route: dict[str, collections.Counter[str]] = (
        collections.defaultdict(collections.Counter))
    occurrences = []
    root_specs: dict[str, dict[str, Any]] = {}
    samples: dict[str, list[dict[str, Any]]] = {}
    for ordinal, c71b, candidate in payload["pairs"]:
        need(type(ordinal) is int and candidate.get("ordinal") == ordinal,
             "candidate ordinal")
        raw_box = c71b["exact_representative_box"]
        box = r185.atlas.AtlasBox(
            Q(raw_box["t"][0]), Q(raw_box["t"][1]),
            Q(raw_box["p"][0]), Q(raw_box["p"][1]), Q(0), Q(0),
            len(c71b["child_path"]), c71b["child_path"])
        origin = origins[c71b["pair_index"]]
        geometry, fresh, roots, normal_signs = geometry_and_roots(
            r185, origin, box, c71b["pair_index"], raw_box)
        route = None if fresh == "STRICT_NEGATIVE" else route_outcome(
            r185, r139, origin, box, cores, pair_index, pattern_index)
        expected = expected_row(c71b, ordinal, origin, geometry, fresh, roots,
                                normal_signs, route, authority, registry)
        close_row(candidate, "candidate decision")
        if candidate != expected:
            difference = first_difference(candidate, expected)
            candidate_body = copy.deepcopy(candidate)
            candidate_body.pop("row_sha256")
            expected_body = copy.deepcopy(expected)
            expected_claim = expected_body.pop("row_sha256")
            candidate_raw = canonical(candidate_body)
            expected_raw = canonical(expected_body)
            byte_at = next((index for index, (left, right) in enumerate(
                itertools.zip_longest(candidate_raw, expected_raw))
                if left != right), None)
            raise Reject(
                "exact independent decision reconstruction:" + str(difference) +
                ":candidate=" + str(candidate.get("row_sha256")) +
                ":expected=" + str(expected_claim) +
                ":reclosed=" + digest(expected_body) +
                ":byte_at=" + str(byte_at) +
                ":candidate_slice=" + repr(candidate_raw[
                    max(0, (byte_at or 0) - 40):(byte_at or 0) + 80]) +
                ":expected_slice=" + repr(expected_raw[
                    max(0, (byte_at or 0) - 40):(byte_at or 0) + 80]))
        old = c71b["arrangement_disposition"]
        outcome = expected["route_outcome"]
        input_census[old] += 1
        fresh_census[fresh] += 1
        route_census[outcome] += 1
        route_by_input[old][outcome] += 1
        pair_census[c71b["pair_index"]] += 1
        pair_route[str(c71b["pair_index"])][outcome] += 1
        if fresh == "CLIPPED":
            graph_route_census[outcome] += 1
        occurrences.extend(endpoint_occurrences(expected))
        for root in expected["H1_geometry"].get("boundary_roots", []):
            value = {"face_key_sha256": root["face_key_sha256"],
                     "exact_face": root["exact_face"]}
            need(root["root_id"] not in root_specs or
                 root_specs[root["root_id"]] == value,
                 "worker root identity consistency")
            root_specs[root["root_id"]] = value
        samples.setdefault(old, [expected, candidate])
    json.dump({
        "count": len(payload["pairs"]),
        "input_census": input_census,
        "fresh_census": fresh_census,
        "route_census": route_census,
        "graph_route_census": graph_route_census,
        "route_by_input": {key: dict(value)
                           for key, value in route_by_input.items()},
        "pair_census": pair_census,
        "pair_route_census": {key: dict(value)
                              for key, value in pair_route.items()},
        "endpoint_occurrences": occurrences,
        "root_specs": root_specs,
        "samples": samples,
    }, sys.stdout, sort_keys=True, separators=(",", ":"))
    return 0


def read_result(stage: Path) -> dict[str, Any]:
    raw = safe_bytes(stage / RESULT)
    result = parse_json(raw, "candidate result")
    close_object(result, "candidate result")
    return result


def row_hash_sequence(path: Path, expected_count: int) -> tuple[str, int]:
    sequence = hashlib.sha256()
    count = 0
    for row in iter_jsonl(path, expected_count=expected_count):
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
        count += 1
    return sequence.hexdigest(), count


def expected_incidence(
        root_specs: dict[str, dict[str, Any]],
        occurrences: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    by_face = {value["face_key_sha256"]: identifier
               for identifier, value in root_specs.items()}
    need(len(by_face) == len(root_specs), "injective root/face inventory")
    incidents: dict[str, list[dict[str, Any]]] = {
        identifier: [] for identifier in root_specs}
    for row in iter_jsonl(C71B_STAGE / C71B_ROWS_NAME,
                          C71B_PINS[C71B_ROWS_NAME], 167255):
        for edge_id, spec in exact_faces(
                row["pair_index"], row["exact_representative_box"]).items():
            key = face_key(spec)
            if key in by_face:
                incidents[by_face[key]].append({
                    "C71b_arrangement_row_sha256": row["row_sha256"],
                    "C65_aggregate_child_row_sha256":
                        row["C65_aggregate_leaf_row_sha256"],
                    "child_path": row["child_path"],
                    "edge_id": edge_id,
                    "exact_face": spec})
    output = []
    for identifier in sorted(root_specs):
        atlas_rows = sorted(incidents[identifier],
                            key=lambda value: (value["child_path"],
                                               value["edge_id"]))
        target_rows = sorted(occurrences[identifier],
                             key=lambda value: (value["child_path"],
                                                value["edge_id"]))
        need(1 <= len(atlas_rows) <= 2 and 1 <= len(target_rows) <= 2,
             "root C71b/target incidence 1/2")
        atlas_keys = {(row["C71b_arrangement_row_sha256"], row["edge_id"])
                      for row in atlas_rows}
        target_keys = {(row["C71b_arrangement_row_sha256"], row["edge_id"])
                       for row in target_rows}
        need(len(atlas_keys) == len(atlas_rows) and
             len(target_keys) == len(target_rows) and
             target_keys.issubset(atlas_keys) and
             all(row["exact_face"] == root_specs[identifier]["exact_face"]
                 for row in target_rows),
             "unique target endpoint mapping")
        high = [row for row in atlas_rows if row["edge_id"].endswith("HIGH")]
        owner = high[0] if len(high) == 1 else atlas_rows[0]
        body = {
            "schema": SCHEMA + ".root-incidence-row",
            "root_id": identifier,
            "face_key_sha256": root_specs[identifier]["face_key_sha256"],
            "exact_face": root_specs[identifier]["exact_face"],
            "target_graph_endpoint_occurrences": target_rows,
            "incidence_count": len(target_rows),
            "incidence_class": "TARGET_GRAPH_SHARED_FACE"
                if len(target_rows) == 2 else
                "TARGET_GRAPH_SINGLE_ENDPOINT_OCCURRENCE",
            "incident_C71b_faces": atlas_rows,
            "atlas_face_incidence_count": len(atlas_rows),
            "atlas_face_incidence_class": "SHARED_C71B_FACE"
                if len(atlas_rows) == 2 else "C71B_SCOPE_BOUNDARY_FACE",
            "unique_half_open_dyadic_face_owner": owner,
            "dyadic_face_owner_rule":
                "LOWER_COORDINATE_CHILD_HIGH_FACE_ELSE_SCOPE_BOUNDARY_ONLY_FACE",
            "corner_incidence": False,
            "physical_chart_owner": "W",
            "paired_N_or_S_representation_is_shadow_only": True,
            "same_physical_trace_duplicate_identified_not_added": True,
            "root_is_graph_endpoint_not_physical_terminal": True,
            "full_dimensional_Kraft_weight": "0",
            "incidence_closed": True,
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "CM2_credit": 0,
            "whole_parent_credit": 0,
            "global_installed_credit": 0,
        }
        output.append({**body, "row_sha256": digest(body)})
    return output


BASE_MEMBERS = (ROWS, INCIDENCE, RESULT, REPORT, CANDIDATE_MANIFEST, LOCK)


def manifest_raw(pins: Mapping[str, str],
                 order: tuple[str, ...] | None = None) -> bytes:
    names = order if order is not None else tuple(sorted(pins))
    need(set(names) == set(pins) and len(names) == len(pins),
         "manifest exact member order")
    return b"".join(
        f"{pins[name]}  {name}\n".encode("ascii") for name in names)


def validate_manifest(raw: bytes, pins: Mapping[str, str], label: str,
                      order: tuple[str, ...] | None = None) -> None:
    need(raw == manifest_raw(pins, order), label + ":canonical manifest")


def validate_stages(stage_a: Path, stage_b: Path) -> tuple[
        dict[str, str], dict[str, bytes]]:
    need(stage_a.is_dir() and stage_b.is_dir() and stage_a != stage_b and
         not stage_a.is_symlink() and not stage_b.is_symlink(),
         "two isolated candidate stages")
    need({path.name for path in stage_a.iterdir()} == set(BASE_MEMBERS) and
         {path.name for path in stage_b.iterdir()} == set(BASE_MEMBERS),
         "exact initial candidate member sets")
    identity: dict[str, str] = {}
    common: dict[str, bytes] = {}
    for name in BASE_MEMBERS:
        left, right = stage_a / name, stage_b / name
        left_sha, right_sha = file_sha(left), file_sha(right)
        need(left_sha == right_sha, "dual-build bytes:" + name)
        left_stat, right_stat = left.stat(), right.stat()
        need((left_stat.st_dev, left_stat.st_ino) !=
             (right_stat.st_dev, right_stat.st_ino),
             "dual-build inode isolation:" + name)
        left_raw, right_raw = safe_bytes(left, left_sha), safe_bytes(right, right_sha)
        need(left_raw == right_raw, "dual terminal recapture:" + name)
        identity[name] = left_sha
        common[name] = left_raw
    candidate_pins = {name: identity[name] for name in BASE_MEMBERS
                      if name != CANDIDATE_MANIFEST}
    validate_manifest(common[CANDIDATE_MANIFEST], candidate_pins,
                      "candidate manifest", (LOCK, ROWS, INCIDENCE, RESULT, REPORT))
    return identity, common


def consume_worker(current: dict[str, Any], totals: dict[str, Any]) -> None:
    totals["count"] += current["count"]
    for key in ("input_census", "fresh_census", "route_census",
                "graph_route_census", "pair_census"):
        totals[key].update(current[key])
    for old, census in current["route_by_input"].items():
        totals["route_by_input"][old].update(census)
    for pair, census in current["pair_route_census"].items():
        totals["pair_route_census"][pair].update(census)
    for occurrence in current["endpoint_occurrences"]:
        record = occurrence["record"]
        claim = occurrence["occurrence_sha256"]
        need(claim == digest(record) and claim not in totals["occurrence_ids"],
             "independent occurrence closure/uniqueness")
        totals["occurrence_ids"].add(claim)
        totals["occurrences"][occurrence["root_id"]].append(record)
    for identifier, value in current["root_specs"].items():
        need(identifier not in totals["root_specs"] or
             totals["root_specs"][identifier] == value,
             "global root identity consistency")
        totals["root_specs"][identifier] = value
    for key, value in current["samples"].items():
        totals["samples"].setdefault(key, value)


def reconstruct_rows(stage: Path, result: dict[str, Any], batch_size: int) -> dict[str, Any]:
    need(100 <= batch_size <= 1200, "worker batch size")
    descriptor = result["ledgers"]["decision_rows"]
    need(descriptor["filename"] == ROWS and descriptor["row_count"] == 33100 and
         descriptor["sha256"] == file_sha(stage / ROWS) and
         descriptor["size"] == (stage / ROWS).stat().st_size,
         "decision ledger descriptor")
    origins = origin_map()
    original, reflected = registry_anchors()
    totals = {
        "count": 0,
        "input_census": collections.Counter(),
        "fresh_census": collections.Counter(),
        "route_census": collections.Counter(),
        "graph_route_census": collections.Counter(),
        "route_by_input": collections.defaultdict(collections.Counter),
        "pair_census": collections.Counter(),
        "pair_route_census": collections.defaultdict(collections.Counter),
        "occurrence_ids": set(),
        "occurrences": collections.defaultdict(list),
        "root_specs": {},
        "samples": {},
    }
    candidates = iter_jsonl(stage / ROWS, descriptor["sha256"], 33100)
    candidate = next(candidates, None)
    batch = []
    numeric_ordinal = 0
    input_census = collections.Counter()
    target_hashes = set()
    for row in iter_jsonl(C71B_STAGE / C71B_ROWS_NAME,
                          C71B_PINS[C71B_ROWS_NAME], 167255):
        if row["child_numeric_domain"] is not True:
            continue
        need(candidate is not None and row["child_level_H1_full_box_closed"] is True and
             row["consumer_review_ready"] is True and
             row["global_consumption_ready"] is False and
             row["remaining_blocker_codes"] == [] and
             all(row[field] == 0 for field in
                 ("formal_credit", "D02_gate_credit", "whole_parent_credit",
                  "terminal_disposition_credit")) and
             row["row_sha256"] not in target_hashes,
             "C71b numeric zero-credit row")
        target_hashes.add(row["row_sha256"])
        input_census[row["arrangement_disposition"]] += 1
        batch.append([numeric_ordinal + 1, row, candidate])
        numeric_ordinal += 1
        candidate = next(candidates, None)
        if len(batch) == batch_size:
            payload = {"pairs": batch, "origins": origins,
                       "original": original, "reflected": reflected}
            completed = subprocess.run(
                [sys.executable, str(SELF), "--worker"],
                input=canonical(payload), capture_output=True, check=True)
            consume_worker(json.loads(completed.stdout), totals)
            batch = []
    need(candidate is None and next(candidates, None) is None,
         "candidate numeric scope exact length")
    if batch:
        payload = {"pairs": batch, "origins": origins,
                   "original": original, "reflected": reflected}
        completed = subprocess.run(
            [sys.executable, str(SELF), "--worker"],
            input=canonical(payload), capture_output=True, check=True)
        consume_worker(json.loads(completed.stdout), totals)
    need(numeric_ordinal == totals["count"] == 33100 and
         len(target_hashes) == 33100 and
         dict(input_census) == EXPECTED_INPUT and
         dict(totals["input_census"]) == EXPECTED_INPUT and
         dict(totals["fresh_census"]) == EXPECTED_FRESH and
         dict(totals["route_census"]) == EXPECTED_ROUTE and
         set(totals["samples"]) == set(EXPECTED_INPUT),
         "complete independent 33100 census")
    row_sequence, row_count = row_hash_sequence(stage / ROWS, 33100)
    need(row_count == 33100 and
         descriptor["row_hash_line_sequence_sha256"] == row_sequence,
         "decision row hash sequence")
    totals["row_sequence"] = row_sequence
    return totals


def reconstruct_incidence(stage: Path, result: dict[str, Any],
                          totals: dict[str, Any]) -> dict[str, Any]:
    need(len(totals["occurrence_ids"]) == 51494 and
         sum(len(rows) for rows in totals["occurrences"].values()) == 51494 and
         set(totals["occurrences"]) == set(totals["root_specs"]),
         "2x25747 endpoint conservation")
    degree_census = collections.Counter(
        len(totals["occurrences"][identifier])
        for identifier in totals["root_specs"])
    need(set(degree_census).issubset({1, 2}) and
         sum(degree * count for degree, count in degree_census.items()) == 51494 and
         sum(degree_census.values()) == len(totals["root_specs"]),
         "root degree decomposition")
    expected = expected_incidence(totals["root_specs"], totals["occurrences"])
    descriptor = result["ledgers"]["root_incidence"]
    need(descriptor["filename"] == INCIDENCE and
         descriptor["row_count"] == len(expected) and
         descriptor["sha256"] == file_sha(stage / INCIDENCE) and
         descriptor["size"] == (stage / INCIDENCE).stat().st_size,
         "incidence ledger descriptor")
    sequence = hashlib.sha256()
    sample = None
    count = 0
    observed_iter = iter_jsonl(stage / INCIDENCE, descriptor["sha256"],
                               len(expected))
    for expected_row, observed in itertools.zip_longest(expected, observed_iter):
        need(expected_row is not None and observed is not None and
             observed == expected_row,
             "exact independently reconstructed incidence row")
        sequence.update((observed["row_sha256"] + "\n").encode("ascii"))
        sample = sample or [expected_row, observed]
        count += 1
    sequence_sha = sequence.hexdigest()
    need(count == len(expected) and
         descriptor["row_hash_line_sequence_sha256"] == sequence_sha,
         "incidence row hash sequence")
    incidence_census = collections.Counter(
        row["incidence_class"] for row in expected)
    atlas_census = collections.Counter(
        row["atlas_face_incidence_class"] for row in expected)
    return {
        "row_count": count,
        "row_sequence": sequence_sha,
        "degree_census": degree_census,
        "incidence_census": incidence_census,
        "atlas_census": atlas_census,
        "sum_incidence_count": sum(row["incidence_count"] for row in expected),
        "sample": sample,
    }


RESULT_KEYS = {
    "schema", "status", "candidate_is_authority", "producer_file_sha256",
    "contract_file_sha256", "contract_object_sha256",
    "closed_schemas_file_sha256", "closed_schemas_object_sha256",
    "pure_core_file_sha256", "numeric_source_pins",
    "chart_seam_quotient_manifest_file_sha256",
    "chart_seam_certificate_sha256", "frozen_input_release", "scope",
    "input_arrangement_disposition_census", "fresh_geometry_census",
    "route_census", "disposition_route_census", "pair_route_census",
    "expected_official_word_key_id", "expected_collision2_owner_set",
    "expected_owner_match_count", "whole_child_strict_exclusion_count",
    "sealed_collision3_handoff_count", "explicit_residual_child_count",
    "graph_child_count", "graph_endpoint_occurrence_count",
    "unique_graph_boundary_root_count", "target_graph_root_degree_census",
    "all_graph_endpoints_have_classified_half_open_face_owner",
    "duplicate_physical_graph_traces_added", "ledgers",
    "runtime_canonical_pointer_or_seal_writes", "global_consumption_ready",
    "formal_credit", "D02_gate_credit", "CM2_credit",
    "whole_parent_credit", "global_installed_credit", "object_sha256",
}


def sorted_nested(value: Mapping[Any, Mapping[Any, int]]) -> dict[str, dict[str, int]]:
    return {str(key): dict(sorted(dict(census).items()))
            for key, census in sorted(value.items(), key=lambda item: str(item[0]))}


def flattened_routes(value: Mapping[Any, Mapping[Any, int]]) -> dict[str, int]:
    return dict(sorted(
        (str(key) + "|" + str(route), count)
        for key, census in value.items() for route, count in census.items()))


def validate_result(result: dict[str, Any], stage: Path,
                    totals: dict[str, Any], incidence: dict[str, Any]) -> None:
    close_object(result, "candidate result")
    need(set(result) == RESULT_KEYS and
         result["schema"] == SCHEMA + ".result" and
         result["status"].startswith("PASS_") and
         result["candidate_is_authority"] is False and
         result["producer_file_sha256"] == PRODUCER_DECLARED_PIN and
         result["contract_file_sha256"] == CONTRACT_FILE_PIN and
         result["contract_object_sha256"] == CONTRACT_OBJECT_PIN and
         result["closed_schemas_file_sha256"] == SCHEMAS_FILE_PIN and
         result["closed_schemas_object_sha256"] == SCHEMAS_OBJECT_PIN and
         result["pure_core_file_sha256"] == PURE_CORE_DECLARED_PIN and
         result["numeric_source_pins"] == NUMERIC_PINS and
         result["chart_seam_quotient_manifest_file_sha256"] ==
            CHART_MANIFEST_PIN and
         result["chart_seam_certificate_sha256"] == CHART_CERTIFICATE_PIN,
         "result identity/pins")
    need(result["frozen_input_release"] == {
            "pin_count": 41, "C65_v9": True, "C69c": True,
            "C71_v2": True, "C71b_v3": True,
            "C72b2_route_capability": True,
            "C35_C37_C38_audited": True} and
         result["scope"] == {"target_child_count": 33100,
                             "pair_count": len(totals["pair_census"]),
                             "additional_dyadic_depth": 0},
         "result frozen release/scope")
    need(result["input_arrangement_disposition_census"] == EXPECTED_INPUT and
         result["fresh_geometry_census"] == EXPECTED_FRESH and
         result["route_census"] == EXPECTED_ROUTE and
         result["disposition_route_census"] ==
            flattened_routes(totals["route_by_input"]) and
         result["pair_route_census"] ==
            flattened_routes(totals["pair_route_census"]),
         "result route and geometry census")
    need(result["expected_official_word_key_id"] == EXPECTED_WORD and
         result["expected_collision2_owner_set"] == sorted(EXPECTED_OWNERS) and
         result["expected_owner_match_count"] == 0 and
         result["whole_child_strict_exclusion_count"] == 33100 and
         result["sealed_collision3_handoff_count"] == 0 and
         result["explicit_residual_child_count"] == 0 and
         result["graph_child_count"] == 25747 and
         result["graph_endpoint_occurrence_count"] == 51494 and
         result["unique_graph_boundary_root_count"] ==
            incidence["row_count"] and
         result["target_graph_root_degree_census"] ==
            {str(key): value for key, value in
             sorted(incidence["degree_census"].items())} and
         result["all_graph_endpoints_have_classified_half_open_face_owner"]
            is True and
         result["duplicate_physical_graph_traces_added"] == 0,
         "result closure census")
    decision = result["ledgers"]["decision_rows"]
    roots = result["ledgers"]["root_incidence"]
    descriptor_keys = {"filename", "order", "row_count", "sha256", "size",
                       "row_hash_line_sequence_sha256"}
    need(set(result["ledgers"]) == {"decision_rows", "root_incidence"} and
         set(decision) == descriptor_keys and set(roots) == descriptor_keys and
         decision["filename"] == ROWS and
         decision["order"] ==
            "C71B_ACCEPTED_ROW_ORDER_FILTER_CHILD_NUMERIC_DOMAIN" and
         decision["row_count"] == 33100 and
         decision["sha256"] == file_sha(stage / ROWS) and
         decision["size"] == (stage / ROWS).stat().st_size and
         decision["row_hash_line_sequence_sha256"] == totals["row_sequence"] and
         roots["filename"] == INCIDENCE and
         roots["order"] == "ROOT_ID_ASCENDING" and
         roots["row_count"] == incidence["row_count"] and
         roots["sha256"] == file_sha(stage / INCIDENCE) and
         roots["size"] == (stage / INCIDENCE).stat().st_size and
         roots["row_hash_line_sequence_sha256"] == incidence["row_sequence"],
         "result exact ledger descriptors")
    need(result["runtime_canonical_pointer_or_seal_writes"] is False and
         result["global_consumption_ready"] is False and
         all(result[field] == 0 for field in ZERO_FIELDS),
         "result all-zero credit boundary")


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def reclose_row(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop("row_sha256", None)
    return {**body, "row_sha256": digest(body)}


def reclose_object(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop("object_sha256", None)
    return {**body, "object_sha256": digest(body)}


def expect_reject(name: str, action: Any, outcomes: dict[str, str]) -> None:
    rejected = False
    try:
        action()
    except (Reject, OSError, ValueError, KeyError, TypeError):
        rejected = True
    need(rejected, "coherent attack accepted:" + name)
    need(name not in outcomes, "duplicate attack label:" + name)
    outcomes[name] = "FAIL_CLOSED"


def exact_row_guard(observed: dict[str, Any], expected: dict[str, Any]) -> None:
    close_row(observed, "attacked decision row")
    need(observed == expected, "attacked decision semantic equality")


def exact_object_guard(observed: dict[str, Any], expected: dict[str, Any]) -> None:
    close_object(observed, "attacked result")
    need(observed == expected, "attacked result semantic equality")


def run_attacks(totals: dict[str, Any], incidence: dict[str, Any],
                result: dict[str, Any], common: dict[str, bytes]) -> dict[str, Any]:
    outcomes: dict[str, str] = {}
    generic_row_attacks = (
        (("ordinal",), 999999),
        (("C71b_arrangement_row_sha256",), "0" * 64),
        (("C65_aggregate_child_row_sha256",), "1" * 64),
        (("child_path",), "0"),
        (("parent_key",), "W:E:FAKE"),
        (("fresh_geometry_kind",), "MUTATED"),
        (("route_outcome",), "EXPECTED_OWNER_MATCH"),
        (("whole_child_strict_exclusion_closed",), False),
        (("physical_chart_glue_closed",), False),
        (("allowed_exit_closed_for_every_stratum",), False),
        (("explicit_residual_strata",), 1),
        (("sealed_collision3_handoff_count",), 1),
        (("collision3_handoff",), {"fake": True}),
        (("current_disposition",), "FORMALLY_INSTALLED"),
        (("candidate_is_authority",), True),
        (("global_consumption_ready",), True),
        (("additional_dyadic_depth",), 1),
        (("formal_credit",), 1),
        (("D02_gate_credit",), 1),
        (("CM2_credit",), 1),
        (("whole_parent_credit",), 1),
        (("global_installed_credit",), 1),
    )
    for disposition, pair in sorted(totals["samples"].items()):
        expected, observed = pair
        for path, replacement in generic_row_attacks:
            attacked = copy.deepcopy(observed)
            set_path(attacked, path, replacement)
            attacked = reclose_row(attacked)
            label = "row_" + disposition + "_" + "_".join(map(str, path))
            need(canonical(attacked) != canonical(observed),
                 "effective row attack:" + label)
            expect_reject(
                label, lambda a=attacked, e=expected: exact_row_guard(a, e),
                outcomes)

    graph_disposition = "LOCAL_H1_CLIPPED_GRAPH_AND_TWO_OFF_GRAPH_REGIONS"
    graph_expected, graph_observed = totals["samples"][graph_disposition]
    graph_attacks = (
        (("H1_geometry", "boundary_root_count"), 1),
        (("H1_geometry", "kind"), "STRICT_WHOLE_CHILD_H1_SIDE"),
        (("H1_geometry", "partition", "W_half_open_owns_H1_EQ_0"), False),
        (("H1_geometry", "boundary_roots", 0, "root_id"), "f" * 64),
        (("H1_geometry", "boundary_roots", 0, "face_key_sha256"), "e" * 64),
        (("H1_geometry", "boundary_roots", 0, "not_a_corner"), False),
        (("stratum_exits", 0, "exit_class"), "UNRESOLVED"),
        (("stratum_exits", 1, "chart"), "N"),
        (("stratum_exits", 2, "physical_chart_glue",
          "half_open_physical_owner_chart"), "N"),
        (("stratum_exits", 2, "physical_chart_glue",
          "duplicate_physical_trace_added"), True),
        (("stratum_exits", 2, "physical_chart_glue",
          "graph_is_not_source_grazing_or_cemetery"), False),
        (("closed_box_downstream_evidence", "centered_Delta",
          "contains_zero"), True),
    )
    for path, replacement in graph_attacks:
        attacked = copy.deepcopy(graph_observed)
        set_path(attacked, path, replacement)
        attacked = reclose_row(attacked)
        label = "graph_" + "_".join(map(str, path))
        expect_reject(label,
                      lambda a=attacked, e=graph_expected:
                          exact_row_guard(a, e), outcomes)

    result_attacks = (
        (("producer_file_sha256",), "0" * 64),
        (("frozen_input_release", "pin_count"), 40),
        (("scope", "target_child_count"), 33099),
        (("fresh_geometry_census", "CLIPPED"), 25746),
        (("route_census", "COLLISION1_OFFICIAL_WORD_MISMATCH"), 31337),
        (("expected_owner_match_count",), 1),
        (("whole_child_strict_exclusion_count",), 33099),
        (("sealed_collision3_handoff_count",), 1),
        (("explicit_residual_child_count",), 1),
        (("graph_endpoint_occurrence_count",), 51493),
        (("unique_graph_boundary_root_count",), incidence["row_count"] - 1),
        (("all_graph_endpoints_have_classified_half_open_face_owner",), False),
        (("duplicate_physical_graph_traces_added",), 1),
        (("global_consumption_ready",), True),
        (("formal_credit",), 1),
    )
    for path, replacement in result_attacks:
        attacked = copy.deepcopy(result)
        set_path(attacked, path, replacement)
        attacked = reclose_object(attacked)
        label = "result_" + "_".join(map(str, path))
        expect_reject(label,
                      lambda a=attacked, e=result:
                          exact_object_guard(a, e), outcomes)

    need(incidence["sample"] is not None, "incidence attack sample")
    incidence_expected, incidence_observed = incidence["sample"]
    incidence_attacks = (
        (("root_id",), "0" * 64),
        (("face_key_sha256",), "1" * 64),
        (("incidence_count",), 0),
        (("atlas_face_incidence_count",), 3),
        (("corner_incidence",), True),
        (("physical_chart_owner",), "N"),
        (("same_physical_trace_duplicate_identified_not_added",), False),
        (("root_is_graph_endpoint_not_physical_terminal",), False),
        (("incidence_closed",), False),
        (("formal_credit",), 1),
    )
    for path, replacement in incidence_attacks:
        attacked = copy.deepcopy(incidence_observed)
        set_path(attacked, path, replacement)
        attacked = reclose_row(attacked)
        label = "incidence_" + "_".join(map(str, path))
        expect_reject(label,
                      lambda a=attacked, e=incidence_expected:
                          exact_row_guard(a, e), outcomes)

    candidate_pins = {name: raw_digest(common[name]) for name in BASE_MEMBERS
                      if name != CANDIDATE_MANIFEST}
    candidate_order = (LOCK, ROWS, INCIDENCE, RESULT, REPORT)
    correct_manifest = manifest_raw(candidate_pins, candidate_order)
    expect_reject("file_manifest_deleted_member", lambda: validate_manifest(
        b"".join(correct_manifest.splitlines(keepends=True)[:-1]),
        candidate_pins, "attack", candidate_order), outcomes)
    expect_reject("file_manifest_reordered", lambda: validate_manifest(
        b"".join(reversed(correct_manifest.splitlines(keepends=True))),
        candidate_pins, "attack", candidate_order), outcomes)
    drift = bytearray(correct_manifest)
    drift[0] = ord("0") if drift[0] != ord("0") else ord("1")
    expect_reject("file_manifest_hash_drift", lambda: validate_manifest(
        bytes(drift), candidate_pins, "attack", candidate_order), outcomes)
    expect_reject("file_dual_byte_drift",
                  lambda: need(common[ROWS][:-1] == common[ROWS], "dual drift"),
                  outcomes)
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as stream:
        stream.write(canonical({"x": 1}) + b"\n")
    member = buffer.getvalue()
    expect_reject("file_gzip_trailing", lambda: one_member(member + b"x"),
                  outcomes)
    expect_reject("file_gzip_multimember", lambda: one_member(member + member),
                  outcomes)
    expect_reject("file_duplicate_json_key",
                  lambda: parse_json(b'{"x":1,"x":2}\n', "attack"), outcomes)
    expect_reject("file_noncanonical_json",
                  lambda: parse_json(b'{ "x": 1 }\n', "attack"), outcomes)
    with tempfile.TemporaryDirectory(prefix="c77d-verifier-attack-",
                                     dir=ROOT / ".cm2-runtime") as scratch_name:
        scratch = Path(scratch_name)
        base = scratch / "base"
        base.write_bytes(b"x")
        hard = scratch / "hard"
        os.link(base, hard)
        expect_reject("file_hardlink", lambda: file_sha(hard), outcomes)
        soft = scratch / "soft"
        soft.symlink_to(base)
        expect_reject("file_symlink", lambda: file_sha(soft), outcomes)
    need(len(outcomes) >= 48 and
         all(value == "FAIL_CLOSED" for value in outcomes.values()),
         "at least 48 coherent attacks")
    return {"attack_count": len(outcomes), "rejected": len(outcomes),
            "all_semantic_mutations_hash_reclosed": True,
            "results": dict(sorted(outcomes.items())),
            "status": f"PASS_{len(outcomes)}_OF_{len(outcomes)}_COHERENT_"
                      "HASH_RECLOSED_SEMANTIC_FILE_ATTACKS_FAIL_CLOSED"}


def write_exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_CLOEXEC", 0) |
                         getattr(os, "O_NOFOLLOW", 0), 0o444)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "exclusive write progress")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    need(safe_bytes(path, raw_digest(raw)) == raw,
         "exclusive terminal-byte replay:" + path.name)


def verification_object(identity: dict[str, str], result: dict[str, Any],
                        upstreams: dict[str, Any], authority: dict[str, Any],
                        totals: dict[str, Any], incidence: dict[str, Any],
                        attacks: dict[str, Any], stage_a: Path,
                        stage_b: Path) -> dict[str, Any]:
    value = {
        "schema": SCHEMA + ".independent-verification.v1",
        "status":
            "PASS_NO_C77D_PRODUCER_OR_C72X_HELPER_READ_IMPORT_COMPILE_EXECUTE__"
            "DUAL_BYTE_IDENTITY__33100_WHOLE_CHILD_STRICT_EXCLUSIONS__"
            "25747_GRAPH_GLUES__51494_ENDPOINTS__ZERO_HANDOFF_RESIDUAL_CREDIT",
        "verifier_file_sha256": file_sha(SELF),
        "producer_file_sha256_declaration_only": PRODUCER_DECLARED_PIN,
        "producer_source_policy": {
            "opened": False, "read": False, "parsed": False,
            "decoded": False, "imported": False, "compiled": False,
            "executed": False},
        "C72x_helper_policy": {
            "opened": False, "read": False, "parsed": False,
            "decoded": False, "imported": False, "compiled": False,
            "executed": False,
            "declared_inert_file_sha256": PURE_CORE_DECLARED_PIN,
            "formula_rewritten_independently": True},
        "contract": {"file_sha256": CONTRACT_FILE_PIN,
                     "object_sha256": CONTRACT_OBJECT_PIN,
                     "closed_schemas_file_sha256": SCHEMAS_FILE_PIN,
                     "closed_schemas_object_sha256": SCHEMAS_OBJECT_PIN},
        "frozen_upstreams": upstreams,
        "chart_authority": authority,
        "numeric_source_pins": NUMERIC_PINS,
        "dual_isolated_candidate_builds": {
            "stage_a": str(stage_a.relative_to(ROOT)),
            "stage_b": str(stage_b.relative_to(ROOT)),
            "base_member_count": len(BASE_MEMBERS),
            "all_base_members_byte_identical": True,
            "base_file_sha256": identity},
        "candidate_result_object_sha256": result["object_sha256"],
        "coverage": {
            "target_child_count": 33100,
            "whole_child_strict_exclusion_count": 33100,
            "strict_negative_count": 1,
            "strict_positive_count": 7352,
            "clipped_graph_count": 25747,
            "graph_endpoint_occurrence_count": 51494,
            "unique_graph_boundary_root_count": incidence["row_count"],
            "sum_incidence_count": incidence["sum_incidence_count"],
            "expected_owner_match_count": 0,
            "sealed_collision3_handoff_count": 0,
            "explicit_residual_child_count": 0},
        "independent_input_disposition_census":
            dict(sorted(totals["input_census"].items())),
        "independent_fresh_geometry_census":
            dict(sorted(totals["fresh_census"].items())),
        "independent_route_census":
            dict(sorted(totals["route_census"].items())),
        "independent_disposition_route_census":
            flattened_routes(totals["route_by_input"]),
        "independent_pair_route_census":
            flattened_routes(totals["pair_route_census"]),
        "independent_graph_route_census":
            dict(sorted(totals["graph_route_census"].items())),
        "root_degree_census": {
            str(key): value for key, value in
            sorted(incidence["degree_census"].items())},
        "root_incidence_census":
            dict(sorted(incidence["incidence_census"].items())),
        "atlas_face_incidence_census":
            dict(sorted(incidence["atlas_census"].items())),
        "all_graph_endpoints_have_classified_half_open_owner": True,
        "all_graphs_have_W_half_open_owner_and_N_or_S_shadow": True,
        "all_closed_box_route_margins_restrict_to_graph": True,
        "all_rows_results_and_incidence_hash_closed": True,
        "coherent_attacks": attacks,
        "candidate_is_authority": False,
        "global_consumption_ready": False,
        "runtime_canonical_pointer_or_seal_writes": False,
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0,
    }
    return {**value, "object_sha256": digest(value)}


def finalize(stage_a: Path, stage_b: Path, identity: dict[str, str],
             verification: dict[str, Any]) -> dict[str, Any]:
    verify_raw = canonical(verification) + b"\n"
    verify_sha = raw_digest(verify_raw)
    for stage in (stage_a, stage_b):
        write_exclusive(stage / VERIFY, verify_raw)
    need(safe_bytes(stage_a / VERIFY, verify_sha) ==
         safe_bytes(stage_b / VERIFY, verify_sha),
         "dual verification bytes")

    members = {**identity, VERIFY: verify_sha}
    final_order = (LOCK, ROWS, INCIDENCE, RESULT, REPORT,
                   CANDIDATE_MANIFEST, VERIFY)
    final_manifest_raw = manifest_raw(members, final_order)
    final_manifest_sha = raw_digest(final_manifest_raw)
    for stage in (stage_a, stage_b):
        write_exclusive(stage / FINAL_MANIFEST, final_manifest_raw)

    outer_body = {
        "schema": SCHEMA + ".final-outer-receipt.v1",
        "status":
            "PASS_DUAL_ISOLATED_BYTE_IDENTICAL__INDEPENDENT_NO_PRODUCER_"
            "RECONSTRUCTION__ONE_FINAL_MANIFEST__OUTER_LAST__ZERO_CREDIT",
        "candidate_is_authority": False,
        "producer_file_sha256_declaration_only": PRODUCER_DECLARED_PIN,
        "producer_source_opened_read_parsed_decoded_imported_compiled_or_executed":
            False,
        "C72x_helper_opened_read_parsed_decoded_imported_compiled_or_executed":
            False,
        "verification_filename": VERIFY,
        "verification_file_sha256": verify_sha,
        "verification_object_sha256": verification["object_sha256"],
        "final_manifest_filename": FINAL_MANIFEST,
        "final_manifest_file_sha256": final_manifest_sha,
        "final_manifest_member_count": len(members),
        "final_manifest_order": list(final_order),
        "final_outer_receipt_published_last_in_each_stage": True,
        "terminal_byte_replay_member_count_per_stage": len(members) + 2,
        "all_final_members_terminal_byte_replayed_in_both_stages": True,
        "all_final_stage_bytes_identical": True,
        "expected_owner_match_count": 0,
        "sealed_collision3_handoff_count": 0,
        "explicit_residual_child_count": 0,
        "candidate_public_unresolved_decrement": 0,
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0,
    }
    outer = {**outer_body, "object_sha256": digest(outer_body)}
    outer_raw = canonical(outer) + b"\n"
    outer_sha = raw_digest(outer_raw)
    for stage in (stage_a, stage_b):
        write_exclusive(stage / OUTER, outer_raw)

    all_pins = {**members, FINAL_MANIFEST: final_manifest_sha,
                OUTER: outer_sha}
    for name, expected in all_pins.items():
        left = stage_a / name
        right = stage_b / name
        need(safe_bytes(left, expected) == safe_bytes(right, expected),
             "terminal dual replay:" + name)
        left_stat, right_stat = left.stat(), right.stat()
        need((left_stat.st_dev, left_stat.st_ino) !=
             (right_stat.st_dev, right_stat.st_ino),
             "terminal dual inode isolation:" + name)
    return {
        "verification_file_sha256": verify_sha,
        "verification_object_sha256": verification["object_sha256"],
        "final_manifest_file_sha256": final_manifest_sha,
        "final_outer_file_sha256": outer_sha,
        "final_outer_object_sha256": outer["object_sha256"],
        "final_member_count": len(all_pins),
    }


def verify(stage_a: Path, stage_b: Path, batch_size: int,
           audit_only: bool) -> dict[str, Any]:
    load_closed_contract()
    upstreams = frozen_upstreams()
    authority = chart_authority()
    identity, common = validate_stages(stage_a, stage_b)
    result_a, result_b = read_result(stage_a), read_result(stage_b)
    need(result_a == result_b and
         identity[RESULT] == raw_digest(canonical(result_a) + b"\n"),
         "dual canonical result equality")
    totals = reconstruct_rows(stage_a, result_a, batch_size)
    incidence = reconstruct_incidence(stage_a, result_a, totals)
    validate_result(result_a, stage_a, totals, incidence)
    attacks = run_attacks(totals, incidence, result_a, common)
    verification = verification_object(
        identity, result_a, upstreams, authority, totals, incidence, attacks,
        stage_a, stage_b)
    if audit_only:
        return {
            "status": "PASS_AUDIT_ONLY_NO_WRITES",
            "verification_object_sha256": verification["object_sha256"],
            "attacks": attacks["status"],
            "producer_source_read": False,
            "C72x_helper_read": False,
            "formal_credit": 0,
        }
    completion = finalize(stage_a, stage_b, identity, verification)
    return {"status": "PASS", "attacks": attacks["status"], **completion}


def static_self_test() -> dict[str, Any]:
    tests: dict[str, bool] = {
        "numeric_scope": sum(EXPECTED_INPUT.values()) == 33100,
        "fresh_scope": sum(EXPECTED_FRESH.values()) == 33100,
        "route_scope": sum(EXPECTED_ROUTE.values()) == 33100,
        "graph_endpoint_identity": 2 * EXPECTED_FRESH["CLIPPED"] == 51494,
        "zero_credit_fields": len(ZERO_FIELDS) == 5,
        "producer_not_loaded":
            PRODUCER_BASENAME.removesuffix(".py") not in sys.modules,
        "C72x_helper_not_loaded": all("round306c72x" not in name
                                      for name in sys.modules),
        "four_input_dispositions": len(EXPECTED_INPUT) == 4,
    }
    try:
        parse_json(b'{"x":1,"x":2}\n', "duplicate")
    except Reject:
        tests["duplicate_JSON_rejected"] = True
    need(all(tests.values()), "static self-test")
    return {"schema": SCHEMA + ".independent-verifier-static-self-test.v1",
            "status": "PASS_9_OF_9_STATIC_NO_PRODUCER_SCOPE_JSON_CREDIT_TESTS",
            "tests": tests, "files_written": False,
            "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--stage-a", type=Path)
    parser.add_argument("--stage-b", type=Path)
    parser.add_argument("--batch-size", type=int, default=600)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()
    if args.worker:
        need(not args.self_test and args.stage_a is None and args.stage_b is None,
             "worker arguments")
        return worker()
    if args.self_test:
        need(args.stage_a is None and args.stage_b is None and
             not args.audit_only, "self-test arguments")
        result = static_self_test()
    else:
        need(args.stage_a is not None and args.stage_b is not None,
             "stage arguments")
        result = verify(args.stage_a.resolve(), args.stage_b.resolve(),
                        args.batch_size, args.audit_only)
    print(canonical(result).decode("utf-8"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        print(canonical({"status": "REJECTED", "reason": str(error)}).decode(),
              file=sys.stderr)
        raise SystemExit(2)
