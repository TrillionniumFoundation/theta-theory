#!/usr/bin/env python3
"""Fail-closed clean-room Round303B expected-state verifier candidate.

The module does not import or execute an R303B producer.  It constructs the
complete expected state from pinned upstream before opening a candidate.
Until the Round303A ten-member seal and the final R303B schema are frozen,
formal candidate access is deliberately unreachable.
"""

from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import heapq
import json
import os
import re
import stat
import sys
import tempfile
import types
from collections import Counter, deque
from collections.abc import Iterable, Iterator
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction as Q
from io import BytesIO
from pathlib import Path
from typing import Any, TextIO

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent if HERE.name == "deliverables" else HERE.parents[2]
INPUT_DIR = WORKSPACE / "deliverables"

SCHEMA = "cm2.round303b.source-g-unified-attachment-edge-promotion.v1"
THEOREM_ID = "CM2_TWO_SIDED_INCLUDED_STRATUM_ATTACHMENT_GLUING_V1"
B1_THEOREM_ID = "ROUND303B_B1_MONOTONE_GRAPH_SIDE_ATTACHMENT_LEMMA_V1"
B2A_THEOREM_ID = "ROUND303B_B2A_R204_ANALYTIC_TARGET_SHEET_LEMMA_V1"
B2B_THEOREM_ID = "ROUND303B_B2B_R291_PHYSICAL_SHEET_INCLUSION_LEMMA_V1"
LIMIT_THEOREM_ID = (
    "CM2_STRICT_T_MONOTONE_FULL_SIGN_SIDES_TWO_CLOSURE_LIMIT_V1"
)
FULL_2D_CERT = "PINNED_ROUND182_FULL_2D_ENDPOINT_BRACKET"
TAIL_CERT = (
    "ROUND204_TAIL_T_BRACKET_MONOTONICITY_AND_P_OUTER_INTERVAL_NEWTON"
)
R182_TARGET_FACTOR_SHEET_THEOREM_ID = (
    "ROUND182_WALL_LEAF_IS_TARGET_FACTOR_GRAPH"
)
R182_PACKAGE_PREFIX = (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
)
R182_PACKAGE_MANIFEST = R182_PACKAGE_PREFIX + "_manifest.sha256"
R182_PACKAGE_MANIFEST_SHA256 = (
    "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5"
)
R182_PACKAGE_MEMBER_PINS = {
    R182_PACKAGE_PREFIX + ".py":
        "8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56",
    R182_PACKAGE_PREFIX + "_certificate.json":
        "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08",
    R182_PACKAGE_PREFIX + "_rows.json":
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    R182_PACKAGE_PREFIX + "_verifier.py":
        "790b17cf6dadebc37b889fff63c6ecde985cccf53c95523cd6c2bc39d12db566",
    R182_PACKAGE_PREFIX + "_verification.json":
        "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36",
    R182_PACKAGE_PREFIX + "_report.md":
        "708272e9425bef74f3f4639c76fd17078f509d3acc5d324325c224e743985f0c",
    R182_PACKAGE_PREFIX + "_cold_replay.md":
        "c0fd075a0ba56de5380c6cc89620dc82fa640c0466b118565cf1755aedf61f99",
}
R294B_PACKAGE_PREFIX = (
    "cm2_round294b_source_g_registry_builder_admission_closure"
)
R294B_MANIFEST = R294B_PACKAGE_PREFIX + "_manifest.sha256"
R294B_VERIFICATION = R294B_PACKAGE_PREFIX + "_verification.json"
R294B_MANIFEST_SHA256 = (
    "fc16aa2792a59dff922afcc8ec66b1ca015251af3c5f718d9d909439a2990d76"
)
R294B_VERIFICATION_FILE_SHA256 = (
    "b1440432a082b392de744bc6f4ca20e893122cb923a3236899357ccfb4fd6581"
)
R294B_VERIFICATION_OBJECT_SHA256 = (
    "1746adb7b71607909eae031da879671885deee8602fdb5685dc561ba9afa4179"
)
R294B_PACKAGE_MEMBER_PINS = {
    "cm2_round292_source_g_occurrence_registry_candidate_construction.py":
        "2c0b7e864839880f47cca2989b3f8d48fcec0399c0644c92f8aabab225402004",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_verifier.py":
        "9efd78054cdde8172b016a684951395f1ca96958412122034dfc1971312ea010",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_manifest.sha256":
        "4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    R294B_PACKAGE_PREFIX + ".py":
        "ed8346b550c461cea28a4a01393c4c5d1be802f9e6145537a0ae7fe5c2e13192",
    R294B_PACKAGE_PREFIX + "_result.json":
        "656676d6f5dd4accc7b9aa473a14d9c1326b83eff2fe8974e7b43694adb44ccc",
    R294B_PACKAGE_PREFIX + "_verifier.py":
        "f6aa9278de7a8c478b6c4d8b49bbf8517f54ba1fb2a2b15fda5ce8afae41cc92",
    R294B_VERIFICATION: R294B_VERIFICATION_FILE_SHA256,
    R294B_PACKAGE_PREFIX + "_attack_suite.json":
        "4d4f99615078062b0fbc544ff04245f6bd9055beb3ca8807480e0aff4aacdcff",
    R294B_PACKAGE_PREFIX + "_report.md":
        "358471a38a0c32c411179c373519fc426d3d32cbc56c3526c41392e0ed158ebe",
    R294B_PACKAGE_PREFIX + "_cold_replay.md":
        "502dd01eade98f5cd5e33c716ebd077b03257dc2f42f110919365662ce759944",
}
WT_DISPOSITION = (
    "UNRESOLVED__ROUND271_W_TAIL_CONNECTED_SIDE_EXTENSION_MISSING"
)
R303A_THEOREM_ID = (
    "ROUND294_CANONICAL_ATOM_OCCURRENCE_ANCHOR_TO_CONNECTED_SOURCE_SIDE_"
    "BRIDGE_V1"
)
R301_SOURCE_RELATION = (
    "R300D_CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_INCIDENCE_EDGE"
)
R301_UNRESOLVED = "INELIGIBLE_INCIDENCE_ONLY__NO_STRONGER_GATE_PROOF"
R303A_WTAIL = "UNRESOLVED__W_TAIL_CONNECTED_SOURCE_SIDE_EXTENSION_MISSING"

R288_KIND = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
PRESERVED_KIND = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
PIN_RE = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_R300D = 111_524
EXPECTED_CROSS = 44_108
EXPECTED_B1_SCOPE = 43_916
EXPECTED_B1 = 43_912
EXPECTED_B2 = 192
EXPECTED_WTAIL = 4
EXPECTED_EDGE = 44_104
EXPECTED_ENDPOINTS = 88_216
EXPECTED_R204_FULL_2D = 192
EXPECTED_R204_TAIL = 32
MAX_BASE_SPLIT_DEPTH = 24
MAX_CORRIDOR_DYADIC_DEPTH = 48

PREFIX = "cm2_round303b_source_g_unified_attachment_edge_promotion"
VERIFIER_NAME = PREFIX + "_verifier.py"
OUTPUTS = {
    "b1": PREFIX + "_b1_graph_attachment_lemma_ledger.json.gz",
    "b2a": PREFIX + "_b2a_analytic_sheet_lemma_ledger.json.gz",
    "b2b": PREFIX + "_b2b_physical_inclusion_lemma_ledger.json.gz",
    "edge": PREFIX + "_component_edge_ledger.json.gz",
    "unresolved": PREFIX + "_wtail_unresolved_ledger.json.gz",
    "result": PREFIX + "_result.json",
}
ATTACK_OUTPUT = PREFIX + "_attack_suite.json"
VERIFICATION_OUTPUT = PREFIX + "_verification.json"
PRODUCER_NAME = (
    "cm2_round303b_source_g_unified_attachment_edge_producer.py"
)
TABLES = {
    "b1": "B1_graph_attachment_lemma_rows",
    "b2a": "B2a_analytic_sheet_lemma_rows",
    "b2b": "B2b_physical_inclusion_lemma_rows",
    "edge": "component_connectivity_edge_rows",
    "unresolved": "W_tail_unresolved_rows",
}
ID_FIELDS = {
    "b1": "Round303B_B1_attachment_lemma_row_id",
    "b2a": "Round303B_B2a_analytic_sheet_lemma_row_id",
    "b2b": "Round303B_B2b_physical_inclusion_lemma_row_id",
    "edge": "Round303B_component_connectivity_edge_row_id",
    "unresolved": "Round303B_W_tail_unresolved_row_id",
}
ID_PREFIXES = {
    "b1": "round303b-b1-attachment-lemma:",
    "b2a": "round303b-b2a-analytic-sheet-lemma:",
    "b2b": "round303b-b2b-physical-inclusion-lemma:",
    "edge": "round303b-component-connectivity-edge:",
    "unresolved": "round303b-wtail-unresolved:",
}
ID_CONTEXTS = {
    "b1": B1_THEOREM_ID,
    "b2a": B2A_THEOREM_ID,
    "b2b": B2B_THEOREM_ID,
    "edge": THEOREM_ID,
    "unresolved": "ROUND303B_WTAIL_UNRESOLVED_V1",
}
ZERO_FIELDS = (
    "formal_occurrence_identity_collapse_credit",
    "formal_official_key_merge_credit",
    "formal_component_union_credit",
    "formal_component_quotient_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_seam_edge_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)

R300D = (
    "cm2_round300d_source_g_lower_physical_witness_component_edge_"
    "promotion_ledger.json.gz"
)
R301_MEMBERS = (
    "cm2_round301_source_g_legal_component_dsu_application_"
    "member_component_ledger.json.gz"
)
R301_INELIGIBLE = (
    "cm2_round301_source_g_legal_component_dsu_application_"
    "ineligible_source_consumption_ledger.json.gz"
)
R294 = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R295A = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
    "closure_physical_witness_incidence_binding_ledger.json.gz"
)
R293 = (
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_"
    "closure_ledger.json.gz"
)
R291 = (
    "cm2_round291_source_g_complete_lower_stratum_local_disposition_"
    "freeze_ledger.json.gz"
)
R303A_PRODUCER = (
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge.py"
)
R303A_BRIDGES = (
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_"
    "bridge_ledger.json.gz"
)
R303A_UNRESOLVED = (
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_"
    "unresolved_bridge_ledger.json.gz"
)
R303A_RESULT = (
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_result.json"
)
R303A_MANIFEST = (
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_"
    "manifest.sha256"
)
R204 = (
    "cm2_round204_source_g_wall_return_signature_local_replacement_"
    "certificate.json"
)
R182 = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R179_KERNEL = "cm2_round179_source_g_residual_tube_arrangement.py"
R174_KERNEL = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_"
    "materialization_verifier.py"
)
FIRST_HIT_KERNEL = "cm2_gate3_candidate_first_hit_cert.py"
INTERVAL_ATLAS_KERNEL = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
GE_KERNEL = "cm2_gate3_ge_interval_atlas_cert.py"


class VerificationError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=True,
    allow_nan=False,
)


def pieces(value: Any) -> Iterable[bytes]:
    for piece in ENCODER.iterencode(value):
        yield piece.encode("ascii")


def canonical(value: Any) -> bytes:
    return b"".join(pieces(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for piece in pieces(value):
        state.update(piece)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def close_row(route: str, payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row[ID_FIELDS[route]] = (
        ID_PREFIXES[route] + digest([ID_CONTEXTS[route], payload])
    )
    row["row_sha256"] = digest(row)
    return row


def verify_row(row: dict[str, Any], label: str) -> None:
    need(type(row) is dict, "ROW_OBJECT:" + label)
    claimed = row.get("row_sha256")
    payload = dict(row)
    payload.pop("row_sha256", None)
    need(
        type(claimed) is str
        and PIN_RE.fullmatch(claimed) is not None
        and claimed == digest(payload),
        "ROW_CLOSURE:" + label,
    )


def canonical_pair(value: Any, label: str) -> tuple[str, str]:
    need(
        type(value) is list
        and len(value) == 2
        and all(type(item) is str and item for item in value)
        and value[0] < value[1],
        "CANONICAL_PAIR:" + label,
    )
    return value[0], value[1]


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "DUPLICATE_JSON_KEY:" + key)
        output[key] = value
    return output


def reject_number(token: str) -> Any:
    raise VerificationError("NONINTEGER_JSON_NUMBER:" + token)


STRICT_DECODER = json.JSONDecoder(
    object_pairs_hook=strict_object,
    parse_float=reject_number,
    parse_constant=reject_number,
)


def strict_json_bytes(raw: bytes, label: str) -> Any:
    try:
        text = raw.decode("utf-8")
        value, end = STRICT_DECODER.raw_decode(text)
    except (UnicodeDecodeError, json.JSONDecodeError, VerificationError) as exc:
        raise VerificationError("STRICT_JSON:" + label) from exc
    need(not text[end:].strip(), "JSON_TRAILING_BYTES:" + label)
    return value


def read_json(path: Path) -> dict[str, Any]:
    need(path.is_file() and not path.is_symlink(), "REGULAR_JSON:" + path.name)
    value = strict_json_bytes(path.read_bytes(), path.name)
    need(type(value) is dict, "JSON_OBJECT:" + path.name)
    return value


def open_text(path: Path) -> TextIO:
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", newline="")
    return path.open("rt", encoding="utf-8", newline="")


def iter_array(
    path: Path,
    table: str,
    *,
    after_marker: str | None = None,
) -> Iterator[Any]:
    marker = json.dumps(table, separators=(",", ":")) + ":["
    with open_text(path) as stream:
        buffer = ""
        if after_marker is not None:
            while after_marker not in buffer:
                chunk = stream.read(1 << 20)
                need(
                    bool(chunk),
                    "ARRAY_ANCHOR:" + path.name + ":" + after_marker,
                )
                buffer += chunk
                if len(buffer) > (1 << 21):
                    buffer = buffer[-(
                        len(after_marker) + (1 << 20)
                    ):]
            buffer = buffer.split(after_marker, 1)[1]
        while marker not in buffer:
            chunk = stream.read(1 << 20)
            need(bool(chunk), "TABLE_MARKER:" + path.name + ":" + table)
            buffer += chunk
            if len(buffer) > (1 << 21):
                buffer = buffer[-(len(marker) + (1 << 20)):]
        buffer = buffer.split(marker, 1)[1]
        cursor = 0
        while True:
            while True:
                while cursor < len(buffer) and (
                    buffer[cursor].isspace() or buffer[cursor] == ","
                ):
                    cursor += 1
                if cursor < len(buffer):
                    break
                chunk = stream.read(1 << 20)
                need(bool(chunk), "UNTERMINATED_ARRAY:" + path.name)
                buffer = buffer[cursor:] + chunk
                cursor = 0
            if buffer[cursor] == "]":
                return
            try:
                value, end = STRICT_DECODER.raw_decode(buffer, cursor)
            except json.JSONDecodeError:
                chunk = stream.read(1 << 20)
                need(bool(chunk), "TRUNCATED_ARRAY_ROW:" + path.name)
                buffer = buffer[cursor:] + chunk
                cursor = 0
                continue
            yield value
            cursor = end
            if cursor > (1 << 20):
                buffer = buffer[cursor:]
                cursor = 0


def parse_manifest(path: Path) -> dict[str, str]:
    need(path.is_file() and not path.is_symlink(), "MANIFEST_PATH:" + path.name)
    members: dict[str, str] = {}
    for raw in path.read_text("utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        need(
            len(parts) >= 2 and PIN_RE.fullmatch(parts[0]) is not None,
            "MANIFEST_SYNTAX:" + path.name,
        )
        name = parts[-1].removeprefix("*").removeprefix("./")
        need(name not in members, "MANIFEST_DUPLICATE:" + name)
        members[name] = parts[0]
    return members


BASE_INPUT_PINS = {
    R179_KERNEL:
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    R179:
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    **R182_PACKAGE_MEMBER_PINS,
    R182_PACKAGE_MANIFEST: R182_PACKAGE_MANIFEST_SHA256,
    R204:
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    R291:
        "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    R293:
        "0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c",
    R294:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R295A:
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R300D:
        "287d1382b25fd3d5cd0a52c6da8cabbb012040b8a6e35c9f887d7a425b812fa7",
    R301_MEMBERS:
        "88adb1ac6c9ee447fddb2ccd8e657a238827e9b31712d974a2a9abd2a3591b93",
    R301_INELIGIBLE:
        "5fbc5a409eccd4e04954c7b63dab6739897efd8d9e327c47045cbfbbbaf7633e",
    "cm2_round179_source_g_residual_tube_arrangement_manifest.sha256":
        "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76",
    "cm2_round204_source_g_wall_return_signature_local_replacement_manifest.sha256":
        "ae3310f8ae0a4c565a39153e268c09fcb983aa04cccce6e3d7dd72fb7803c213",
    "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_manifest.sha256":
        "d655907a45cfb7b47ebdc822d35a0e604fc27fa38547c300139c116d7a2191ce",
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_manifest.sha256":
        "14fef7e62be76cefaa2c331d7c6f72e50f732c7b5df17596759afe1a49406987",
    "cm2_round293b_source_g_r293_dual_producer_seed_replay_manifest.sha256":
        "4bca00a379bb2abb0e5d1dd2b2de7f750e77df32ad37d1c1bc2feab33f2354dd",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_manifest.sha256":
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_manifest.sha256":
        "8dd3907a363ae0c4fe7d524061a02b4c70944ce870ded941d5d617911ea1124e",
    "cm2_round301_source_g_legal_component_dsu_application_manifest.sha256":
        "5789b23e74b6e0db9a1b4e311fb22ebe5e3612e4972d2fc3547957230fda214c",
    **R294B_PACKAGE_MEMBER_PINS,
    R294B_MANIFEST: R294B_MANIFEST_SHA256,
}
EXECUTABLE_TRANSITIVE_CLOSURE_PINS = {
    R179_KERNEL:
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    R174_KERNEL:
        "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058",
    FIRST_HIT_KERNEL:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    INTERVAL_ATLAS_KERNEL:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    GE_KERNEL:
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
}
EXECUTABLE_IMPORT_GRAPH = {
    R179_KERNEL: [R174_KERNEL],
    R174_KERNEL: [FIRST_HIT_KERNEL, INTERVAL_ATLAS_KERNEL],
    INTERVAL_ATLAS_KERNEL: [FIRST_HIT_KERNEL, GE_KERNEL],
    GE_KERNEL: [FIRST_HIT_KERNEL],
    FIRST_HIT_KERNEL: [],
}
EXECUTABLE_LOAD_ORDER = (
    FIRST_HIT_KERNEL,
    GE_KERNEL,
    INTERVAL_ATLAS_KERNEL,
    R174_KERNEL,
)
BASE_MANIFEST_MEMBERS = {
    "cm2_round179_source_g_residual_tube_arrangement_manifest.sha256": {
        R179_KERNEL: BASE_INPUT_PINS[R179_KERNEL],
        R179: BASE_INPUT_PINS[R179],
    },
    R182_PACKAGE_MANIFEST: dict(R182_PACKAGE_MEMBER_PINS),
    R294B_MANIFEST: dict(R294B_PACKAGE_MEMBER_PINS),
    "cm2_round204_source_g_wall_return_signature_local_replacement_manifest.sha256": {
        R204: BASE_INPUT_PINS[R204],
    },
    "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_manifest.sha256": {
        R291: BASE_INPUT_PINS[R291],
    },
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_manifest.sha256": {
        R293: BASE_INPUT_PINS[R293],
    },
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256": {
        R294: BASE_INPUT_PINS[R294],
    },
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_manifest.sha256": {
        R295A: BASE_INPUT_PINS[R295A],
    },
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_manifest.sha256": {
        R300D: BASE_INPUT_PINS[R300D],
    },
    "cm2_round301_source_g_legal_component_dsu_application_manifest.sha256": {
        R301_MEMBERS: BASE_INPUT_PINS[R301_MEMBERS],
        R301_INELIGIBLE: BASE_INPUT_PINS[R301_INELIGIBLE],
    },
}

RAW_R303A_PINS = {
    R303A_PRODUCER:
        "b85d6a8f33e81feb613b2cdb04de648376a10c94635b23119bd7f70439ba461a",
    R303A_BRIDGES:
        "efe0e4b71804848611f3702063698ee77bbdf9dc779bc473fba989fb5db7e465",
    R303A_UNRESOLVED:
        "a029eae97e1f35b87f9699adb0446f1b1329a55c5b4ee0887b03bd1f4a9db0b8",
    R303A_RESULT:
        "796b2167e2263108e3e2c373650e1d488152f7558bbc03fffe977d38e0e81d19",
}

# Fill only from a genuinely sealed package.  Ten exact manifest members are
# mandatory; a raw result or manifest template is never accepted.
R303A_SEAL_MEMBER_PINS: dict[str, str | None] = {
    R303A_PRODUCER:
        "b85d6a8f33e81feb613b2cdb04de648376a10c94635b23119bd7f70439ba461a",
    R303A_BRIDGES:
        "efe0e4b71804848611f3702063698ee77bbdf9dc779bc473fba989fb5db7e465",
    R303A_UNRESOLVED:
        "a029eae97e1f35b87f9699adb0446f1b1329a55c5b4ee0887b03bd1f4a9db0b8",
    R303A_RESULT:
        "796b2167e2263108e3e2c373650e1d488152f7558bbc03fffe977d38e0e81d19",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_verifier.py":
        "f8ffa2080b6ccc51c48ce7a37dc6c80ae0a94187f19a744b3f46a03a144f45e3",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_verification.json":
        "ada33e5f1a780f92b228861f0e3606ff2c383665d056f1c83b38c0fda56a4549",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_attack_suite.json":
        "ce29c15b9d685d9e863ab4534adc50302995131283f4dc03e68d34a18a678bf2",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_cold_replay.md":
        "40fd98df494a4aba2c4c2697bf1c99e30b304cb62f295349ce0d12f8d93b2e9d",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_report.md":
        "190ed08b89be1fd8f719562b22898e860fbb3031d231ded0788bf68154c834fe",
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_attestation.json":
        "d46f8074761cdb5f4b9706d033665c2fc260be5a363cd96095ed350a2b125c10",
}
R303A_MANIFEST_SHA256: str | None = (
    "6f195f8325f107328f7e375411bb8a95146b0cfd65180f5cc9f85b3643d0b098"
)
FINAL_R303B_PRODUCER_SHA256: str | None = (
    "02ce70a560b7fa029e2c7a70a1e4627cb423ac67ba187dba059b57194a646735"
)
FINAL_R303B_SCHEMA_SNAPSHOT_SHA256: str | None = (
    "dea4a7bec1a056fe99db2c6d5deec617b9f39d4a13c17a185acddfb475751e80"
)


GLUING_THEOREM = {
    "theorem_id": THEOREM_ID,
    "version": 1,
    "hypotheses": {
        "G0_exact_provenance_pins_and_row_closures": (
            "Every endpoint, bridge, chart, active equation, physical cell, "
            "included stratum, and source file is exactly pinned and row "
            "closed."
        ),
        "G1_endpoint_occurrence_connected_supports": (
            "Each endpoint has a nonempty occurrence anchor contained in one "
            "formal connected physical source side."
        ),
        "G2_nonempty_connected_included_lower_stratum": (
            "The common lower-dimensional patch Gamma is nonempty, connected, "
            "and included in the physical space."
        ),
        "G3_left_closure_attaches_to_included_patch": (
            "The closure of the left endpoint's connected side meets Gamma."
        ),
        "G4_right_closure_attaches_to_included_patch": (
            "The closure of the right endpoint's connected side meets Gamma."
        ),
        "G5_endpoint_patch_provenance_exactly_closed": (
            "Both occurrence IDs, connected sides, attachments, and Gamma "
            "close through one exact chart/equation/leaf provenance chain."
        ),
    },
    "conclusion": (
        "closure(A_left) union Gamma union closure(A_right) is connected, "
        "hence the two registry occurrences lie in one physical component."
    ),
    "credit_boundary": {
        "formal_component_edge_credit": 1,
        "formal_occurrence_identity_collapse_credit": 0,
        "formal_official_key_merge_credit": 0,
        "formal_component_union_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
        "formal_Jx_Jy_same_point_glue_credit": 0,
    },
}

MONOTONE_LIMIT_THEOREM = {
    "theorem_id": LIMIT_THEOREM_ID,
    "version": 1,
    "hypotheses": {
        "L0_exact_relative_domain": (
            "D=I_t x U is an exact nondegenerate rational prism, U is a "
            "positive-area connected rational rectangle, and any excluded "
            "relative-open face is named and disjoint from Gamma."
        ),
        "L1_continuous_active_scalar": (
            "F is continuous on D; chart radicands/discriminants are strictly "
            "positive and every divisor is nonzero on the serialized domain."
        ),
        "L2_strict_t_monotonicity": (
            "The t derivative enclosure of F has one strict sign on D."
        ),
        "L3_uniform_opposite_face_signs": (
            "The two t faces of F have opposite uniform strict signs, each "
            "certified either by one direct interval enclosure or by an "
            "independently replayed transverse-monotonicity zero-absence "
            "status."
        ),
        "L4_exact_included_Gamma_binding": (
            "The unique zero graph Gamma is exactly the selected Round291 "
            "WHOLE_PHYSICAL_SUPPORT cell patch and closes through Round295A "
            "and Round300D."
        ),
        "L5_complete_connected_sign_sides": (
            "The two sealed Round303A A objects are included connected "
            "complete sign sides, and {F<0} in D and {F>0} in D are each "
            "symbolically contained in the corresponding A."
        ),
        "L6_endpoint_opposite_sign_bijection": (
            "The two endpoints biject to opposite signs and the "
            "Round294/Round303A/leaf/chart/owner/equation chain closes."
        ),
    },
    "conclusion": (
        "Gamma={F=0} in D is one nonempty continuous graph over U, and "
        "Gamma is contained in closure({F<0} in D) intersect "
        "closure({F>0} in D)."
    ),
    "proof_contract": (
        "Existence is IVT on every base fibre; uniqueness is strict "
        "monotonicity; continuity of the root map follows from continuity, "
        "the uniform strict face bracket, and uniqueness; approaching the "
        "root from either t direction supplies the two closure limits."
    ),
    "forbidden_shortcut": (
        "A strict nonzero corridor is disjoint from Gamma and is never an "
        "intersection or attachment witness."
    ),
}

B1_LAYER_THEOREM = {
    "theorem_id": B1_THEOREM_ID,
    "version": 1,
    "hypotheses": {
        "B1_0_exact_scope_and_sealed_bridges": (
            "The Round300D/Round301 pair and both opposite-sign Round303A "
            "connected-side bridges close through exact pinned rows."
        ),
        "B1_1_exact_monotone_graph": (
            "The pinned R179/R182 active scalar has one strict t derivative "
            "and opposite strict t-face signs on a positive-base prism."
        ),
        "B1_2_included_Gamma_identity": (
            "The unique zero graph is the selected included Round291 "
            "WHOLE_PHYSICAL_SUPPORT cell carried through R293/R295A."
        ),
        "B1_3_two_complete_side_attachments": (
            "The complete local sign sides lie in the two connected "
            "Round303A sides and Gamma lies in both closures."
        ),
    },
    "conclusion": (
        "The two endpoint connected supports attach to the same nonempty "
        "connected included Gamma."
    ),
    "kernel_theorem_id": LIMIT_THEOREM_ID,
    "credit_boundary": {
        "formal_B1_attachment_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        "all_downstream_credits": 0,
    },
}

B2A_LAYER_THEOREM = {
    "theorem_id": B2A_THEOREM_ID,
    "version": 1,
    "hypotheses": {
        "B2A_0_exact_FULL_2D_route": (
            "The selected R204 sheet is certified only by "
            "PINNED_ROUND182_FULL_2D_ENDPOINT_BRACKET; both incident regions "
            "are strict, positive-volume, non-tail FULL_2D graph cells."
        ),
        "B2A_1_strict_monotone_bracket": (
            "The exact continuous target factor has one strict t derivative "
            "and opposite uniform t-face signs over a connected positive-area "
            "rational base."
        ),
        "B2A_2_opposite_graph_cells": (
            "The two selected endpoint regions are exactly the negative and "
            "positive subgraph cells of the unique root graph."
        ),
    },
    "conclusion": (
        "Gamma is one nonempty connected unique graph; both strict graph "
        "cells are connected and Gamma lies in both analytic closures."
    ),
    "forbidden_route": TAIL_CERT,
    "credit_boundary": {
        "formal_B2a_analytic_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        "physical_inclusion_claimed_at_B2a": False,
        "all_downstream_credits": 0,
    },
}

R182_TARGET_FACTOR_SHEET_THEOREM = {
    "theorem_id": R182_TARGET_FACTOR_SHEET_THEOREM_ID,
    "version": 1,
    "sealed_package": {
        "manifest_filename": R182_PACKAGE_MANIFEST,
        "manifest_sha256": R182_PACKAGE_MANIFEST_SHA256,
        "exact_member_count": 7,
        "exact_member_pins": dict(sorted(R182_PACKAGE_MEMBER_PINS.items())),
    },
    "hypotheses": {
        "T0_exact_sealed_Round182_package": (
            "The exact seven-member Round182 manifest, including producer, "
            "rows, independent verifier, and verification, is content pinned."
        ),
        "T1_WALL_geometry_value_is_target_selector": (
            "For kind WALL and axis X or Y, Round182 geometry_value evaluates "
            "subtract_wall(independent_geometry[hit_x or hit_y], "
            "integer_wall); it does not evaluate the source factor or the "
            "nominal product equation."
        ),
        "T2_FULL_2D_unique_target_graph": (
            "On the exact leaf box the target selector has a strict t "
            "derivative and opposite uniform lower/upper t-face signs.  Each "
            "face sign is certified either directly or by the independently "
            "replayed Round182 transverse-monotonicity zero-absence status, "
            "so the serialized FULL_2D leaf with sheet count one is the "
            "unique target factor graph over its positive-area base."
        ),
        "T3_exact_concrete_leaf_selector": (
            "Leaf id, collar id, retained child, chart, owner target, axis, "
            "integer wall, exact box, and exact base area all agree."
        ),
    },
    "conclusion": (
        "The selected Round182 WALL FULL_2D leaf carries exactly the unique "
        "target-factor graph target_axis-integer_wall=0 over that base."
    ),
    "nonclaims": {
        "nominal_product_equation_is_sheet_identity": False,
        "product_zero_iff_target_zero_on_closed_leaf": False,
        "closed_leaf_source_factor_strict_nonzero_required": False,
    },
}

B2B_LAYER_THEOREM = {
    "theorem_id": B2B_THEOREM_ID,
    "version": 1,
    "target_factor_sheet_theorem_id": R182_TARGET_FACTOR_SHEET_THEOREM_ID,
    "target_factor_sheet_theorem_sha256": None,
    "hypotheses": {
        "B2B_0_exact_physical_chain": (
            "One exact Round300D -> Round295A -> Round293 -> Round291 "
            "row-and-cell chain binds the same endpoint pair."
        ),
        "B2B_1_Round182_target_factor_sheet": (
            "The content-pinned ROUND182_WALL_LEAF_IS_TARGET_FACTOR_GRAPH "
            "theorem identifies the selected FULL_2D leaf as the unique target "
            "factor graph, independently of the nominal product equation."
        ),
        "B2B_2_R204_Gamma_is_R291_DIRECT_target_sheet": (
            "The R204 Gamma and the Round291 DIRECT_GRAPH_SHEET_WITNESS select "
            "that same concrete target sheet by identical leaf, collar, chart, "
            "owner, axis, wall, exact box, positive base, and target selector."
        ),
        "B2B_3_product_equation_is_nominal_lineage_only": (
            "The Round179/R291 product equation is checked only as nominal "
            "lineage compatibility; no product identity, product iff, or "
            "closed-leaf source-factor strictness is used as a logical bridge."
        ),
    },
    "conclusion": (
        "The B2a/R204 Gamma equals the target-factor graph sheet carried by the "
        "selected Round291 DIRECT witness and is therefore included in its "
        "WHOLE_PHYSICAL_SUPPORT ambient support."
    ),
    "credit_boundary": {
        "formal_B2b_physical_inclusion_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        "all_downstream_credits": 0,
    },
}

THEOREM_SHA256 = digest(GLUING_THEOREM)
MONOTONE_LIMIT_THEOREM_SHA256 = digest(MONOTONE_LIMIT_THEOREM)
B1_LAYER_THEOREM_SHA256 = digest(B1_LAYER_THEOREM)
B2A_LAYER_THEOREM_SHA256 = digest(B2A_LAYER_THEOREM)
R182_TARGET_FACTOR_SHEET_THEOREM_SHA256 = digest(
    R182_TARGET_FACTOR_SHEET_THEOREM
)
B2B_LAYER_THEOREM["target_factor_sheet_theorem_sha256"] = (
    R182_TARGET_FACTOR_SHEET_THEOREM_SHA256
)
B2B_LAYER_THEOREM_SHA256 = digest(B2B_LAYER_THEOREM)


def sorted_keys(*groups: Iterable[str]) -> list[str]:
    return sorted({item for group in groups for item in group})


ROW_KEY_SETS = {
    "b1": sorted_keys(
        (
            "schema",
            "proof_path",
            "theorem_id",
            "theorem_sha256",
            "gluing_theorem_id",
            "gluing_theorem_sha256",
            "monotone_limit_theorem",
            "monotone_limit_theorem_sha256",
            "source_Round300D_row_id",
            "source_Round300D_row_sha256",
            "source_Round301_ineligible_reference",
            "canonical_endpoint_pair",
            "endpoint_connected_side_rows",
            "physical_inclusion_chain",
            "Gamma",
            "local_side_nonempty_witnesses",
            "two_sided_limit_attachment",
            "inactive_wall_source_factor_replay",
            "B1_predicates",
            "limit_theorem_predicates",
            "G0_exact_provenance_pins_and_row_closures",
            "G1_endpoint_occurrence_connected_supports",
            "G2_nonempty_connected_included_lower_stratum",
            "G3_left_closure_attaches_to_included_patch",
            "G4_right_closure_attaches_to_included_patch",
            "G5_endpoint_patch_provenance_exactly_closed",
            "candidate_B1_lemma_conclusion",
            "formal_B1_attachment_lemma_credit",
            "formal_component_edge_credit",
            ID_FIELDS["b1"],
            "row_sha256",
        ),
        ZERO_FIELDS,
    ),
    "b2a": sorted_keys(
        (
            "schema",
            "proof_path",
            "theorem_id",
            "theorem_sha256",
            "source_Round300D_row_id",
            "source_Round300D_row_sha256",
            "canonical_endpoint_pair",
            "Round204_target_sheet_reference",
            "endpoint_open_region_references",
            "exact_join",
            "analytic_conclusion",
            "candidate_B2a_analytic_lemma_conclusion",
            "formal_B2a_analytic_lemma_credit",
            "formal_component_edge_credit",
            ID_FIELDS["b2a"],
            "row_sha256",
        ),
        ZERO_FIELDS,
    ),
    "b2b": sorted_keys(
        (
            "schema",
            "proof_path",
            "theorem_id",
            "theorem_sha256",
            "Round182_target_factor_sheet_theorem_id",
            "Round182_target_factor_sheet_theorem_sha256",
            "source_B2a_row_id",
            "source_B2a_row_sha256",
            "source_Round300D_row_id",
            "source_Round300D_row_sha256",
            "canonical_endpoint_pair",
            "Round204_target_sheet_row_id",
            "Round204_target_sheet_row_sha256",
            "physical_inclusion_chain",
            "exact_join",
            "candidate_B2b_inclusion_lemma_conclusion",
            "formal_B2b_physical_inclusion_lemma_credit",
            "formal_component_edge_credit",
            ID_FIELDS["b2b"],
            "row_sha256",
        ),
        ZERO_FIELDS,
    ),
    "edge": sorted_keys(
        (
            "schema",
            "theorem_id",
            "theorem_sha256",
            "proof_path",
            "source_Round300D_row_id",
            "source_Round300D_row_sha256",
            "source_Round301_ineligible_reference",
            "canonical_unordered_registry_occurrence_ids",
            "source_lemma_references",
            "Round301_pre_edge_components",
            "official_key_metadata",
            "G0_exact_provenance_pins_and_row_closures",
            "G1_endpoint_occurrence_connected_supports",
            "G2_nonempty_connected_included_lower_stratum",
            "G3_left_closure_attaches_to_included_patch",
            "G4_right_closure_attaches_to_included_patch",
            "G5_endpoint_patch_provenance_exactly_closed",
            "candidate_component_connectivity_conclusion",
            "formal_component_edge_credit",
            "eligible_for_later_fresh_DSU_application",
            "old_63224_component_result_reused",
            "Round301_DSU_mutated_here",
            ID_FIELDS["edge"],
            "row_sha256",
        ),
        ZERO_FIELDS,
    ),
    "unresolved": sorted_keys(
        (
            "schema",
            "source_Round300D_row_id",
            "source_Round300D_row_sha256",
            "source_Round301_ineligible_reference",
            "canonical_unordered_registry_occurrence_ids",
            "Round303A_unresolved_endpoint_references",
            "disposition",
            "formal_component_edge_credit",
            "nonedge_credit",
            "exclusion_credit",
            "eligible_for_later_fresh_DSU_application",
            ID_FIELDS["unresolved"],
            "row_sha256",
        ),
        ZERO_FIELDS,
    ),
}

FACE_CERTIFICATE_KEYS = sorted([
    "kind",
    "raw_interval_sign",
    "resolved_sign",
    "axis",
    "derivative_sign",
    "axis_lower_sign",
    "axis_upper_sign",
    "newton_interior",
])

ROUND301_MEMBER_REFERENCE_KEYS = sorted([
    "row_id",
    "row_sha256",
    "component_id",
    "base_root_id",
    "official_key_id",
    "member_kind",
])

B2A_COMMON_EXACT_JOIN_KEYS = sorted([
    "Round182_target_factor_sheet_theorem_id",
    "Round182_target_factor_sheet_theorem_sha256",
    "Round204_sheet_leaf_row_id",
    "Round204_sheet_chart",
    "Round204_sheet_owner_target",
    "Round204_sheet_origin_row_id",
    "Round204_sheet_exact_box",
    "Round204_sheet_base_coordinate_area",
    "Round204_target_factor_equation",
    "Round182_collar_row_id",
    "Round182_leaf_row_id",
    "Round182_leaf_graph_classification",
    "Round182_leaf_base_coordinate_area",
    "Round182_WALL_geometry_selector",
    "Round182_WALL_geometry_selector_source",
    "Round182_replayed_target_t_derivative_sign",
    "Round182_raw_lower_t_face_interval_sign",
    "Round182_raw_upper_t_face_interval_sign",
    "Round182_replayed_lower_t_face_encoded_status",
    "Round182_replayed_upper_t_face_encoded_status",
    "Round182_replayed_lower_t_face_certificate",
    "Round182_replayed_upper_t_face_certificate",
    "Round182_serialized_lower_t_face_status",
    "Round182_serialized_upper_t_face_status",
    "Round182_replayed_lower_t_face_sign",
    "Round182_replayed_upper_t_face_sign",
    "Round182_FULL_2D_unique_target_graph_checked",
    "Round179_active_row_id",
    "Round179_nominal_product_lineage_equation",
    "Round179_source_factor_equation",
    "Round179_target_factor_equation",
    "Round179_target_factor_classification",
    "Round179_target_gradient_axis",
    "Round179_target_gradient_sign",
    "active_factor_semantic_mapping",
    "Round204_half_open_source_sign_on_leaf",
    "source_sign_join_role",
    "nominal_product_lineage_compatibility_checked",
    "nominal_product_equation_used_as_sheet_identity",
    "product_zero_iff_target_zero_claimed",
    "closed_leaf_source_factor_strict_nonzero_required",
    "exact_owner_leaf_chart_box_base_area_join_checked",
    "exact_active_factor_provenance_mapping_checked",
])

B2B_EXACT_JOIN_KEYS = sorted_keys(
    B2A_COMMON_EXACT_JOIN_KEYS,
    (
        "Round291_local_disposition_row_id",
        "Round291_local_disposition_row_sha256",
        "Round291_physical_witness_cell_index",
        "Round291_physical_witness_leaf_row_id",
        "Round291_physical_witness_graph_classification",
        "Round291_physical_witness_exact_box",
        "Round291_physical_witness_base_coordinate_area",
        "Round291_nominal_predicate_product_equation",
        "Round291_representation_role",
        "Round291_local_disposition",
        "Round204_sheet_and_R291_witness_same_leaf",
        "Round204_sheet_and_R291_witness_same_exact_box",
        "Round204_sheet_and_R291_witness_same_chart",
        "Round204_sheet_and_R291_witness_same_owner_target",
        "Round204_sheet_and_R291_witness_same_base_area",
        "Round204_Gamma_equals_Round182_target_factor_graph",
        "Round291_DIRECT_witness_carries_same_Round182_target_sheet",
        "Round293_and_Round295A_bind_same_two_Round294_occurrences",
        "Gamma_included_via_R291_DIRECT_target_sheet_witness",
    ),
)

NESTED_KEY_SETS = {
    "source_Round301_ineligible_reference": sorted([
        "row_id",
        "row_sha256",
        "disposition",
    ]),
    "physical_inclusion_chain": sorted([
        "Round291",
        "Round293",
        "Round295A",
    ]),
    "physical_inclusion_chain.Round291": sorted([
        "row_id",
        "row_sha256",
        "physical_witness_cell_index",
        "physical_witness_cell",
    ]),
    "physical_inclusion_chain.Round291.physical_witness_cell": sorted([
        "witness_kind",
        "leaf_row_id",
        "retained_child_row_id",
        "graph_classification",
        "exact_box",
        "base_coordinate_area",
    ]),
    "physical_inclusion_chain.binding": sorted([
        "row_id",
        "row_sha256",
        "binding_classification",
    ]),
    "B1.endpoint_connected_side_row": sorted([
        "registry_occurrence_id",
        "Round294_registry_row_id",
        "Round294_registry_row_sha256",
        "Round301_member_reference",
        "Round303A_bridge_row_id",
        "Round303A_bridge_row_sha256",
        "Round303A_theorem_id",
        "Round303A_theorem_sha256",
        "strict_anchor_box",
        "active_factor_strict_sign",
        "normalized_A_contract",
        "normalized_A_definition",
        "connected_source_side_witness",
        "matched_graph_side",
        "local_graph_sign_side_subset_normalized_A",
        "closure_attachment_to_Gamma",
    ]),
    "B1.connected_source_side_witness": sorted([
        "formal_connected_source_signed_region_id",
        "formal_connected_source_signed_region_definition",
        "connected_contract",
        "relative_open_excluded_face",
        "connected",
        "strict_anchor_subbox_has_same_active_factor_sign",
    ]),
    "B1.closure_attachment_to_Gamma": sorted([
        "theorem_id",
        "theorem_sha256",
        "Gamma_subset_closure_of_this_local_sign_side",
        "local_sign_side_subset_normalized_A",
        "therefore_Gamma_subset_closure_of_normalized_A",
    ]),
    "B1.Gamma": sorted([
        "kind",
        "exact_active_scalar_equation",
        "Round182_leaf_row_id",
        "root_physical_leaf_box",
        "positive_base_graph_prism",
        "exact_positive_base_area",
        "base_split_schedule",
        "base_split_path",
        "base_split_depth",
        "strict_t_derivative_sign",
        "strict_t_derivative_enclosure",
        "lower_face_active_sign",
        "lower_face_active_enclosure",
        "upper_face_active_sign",
        "upper_face_active_enclosure",
        "exact_chart_radicand_margins",
        "active_scalar_continuous_on_D",
        "unique_zero_graph_by_strict_monotonicity_and_IVT",
        "connected",
        "nonempty",
        "included_by_R291_R293_R295A_physical_chain",
        "Round272_excluded_t0_face_active_sign",
        "Round272_Gamma_misses_excluded_t0_face",
        "relative_domain",
    ]),
    "B1.Gamma.exact_chart_radicand_margins": sorted([
        "one_minus_t_squared_margin",
        "one_minus_p_squared_margin",
        "both_strictly_positive",
    ]),
    "B1.local_side_nonempty_witnesses": sorted([
        "lower_graph_facing_corridor_box",
        "lower_corridor_dyadic_depth",
        "lower_corridor_active_sign",
        "upper_graph_facing_corridor_box",
        "upper_corridor_dyadic_depth",
        "upper_corridor_active_sign",
        "both_positive_volume",
        "corridor_intersects_Gamma_claimed",
        "corridor_used_as_attachment_witness",
    ]),
    "B1.two_sided_limit_attachment": sorted([
        "left_local_sign_side_subset_normalized_A",
        "right_local_sign_side_subset_normalized_A",
        "Gamma_subset_closure_of_left_local_sign_side",
        "Gamma_subset_closure_of_right_local_sign_side",
        "Gamma_subset_closure_of_both_normalized_A_sides",
        "proof_source",
        "corridor_box_closure_meets_Gamma",
    ]),
    "B1.inactive_wall_source_factor_replay": sorted([
        "root_checked_box",
        "domain",
        "strict_sign",
        "corridor_checks",
    ]),
    "B1.inactive_wall_source_factor_replay.corridor_check": sorted([
        "checked_box",
        "domain",
        "strict_sign",
    ]),
    "B1.B1_predicates": sorted([
        "B1_P0_exact_scope_and_physical_binding_join",
        "B1_P1_two_complete_connected_A_bridges",
        "B1_P2_exact_chart_and_inactive_factor_domain",
        "B1_P3_positive_base_strict_monotone_bracket",
        "B1_P4_Gamma_same_included_R291_sheet_patch",
        "B1_P5_left_local_side_subset_A_and_limit_attachment",
        "B1_P6_right_local_side_subset_A_and_limit_attachment",
        "B1_P7_endpoint_patch_provenance_exactly_closed",
    ]),
    "B1.limit_theorem_predicates": sorted([
        "L0_exact_relative_domain",
        "L1_continuous_active_scalar",
        "L2_strict_t_monotonicity",
        "L3_uniform_opposite_face_signs",
        "L4_exact_included_Gamma_binding",
        "L5_complete_connected_sign_sides",
        "L6_endpoint_opposite_sign_bijection",
    ]),
    "B2a.Round204_target_sheet_reference": sorted([
        "sheet_row_id",
        "row_sha256",
        "leaf_row_id",
        "chart",
        "owner_target",
        "leaf_t_exact_bounds",
        "base_p_s_exact_bounds",
        "target_t_derivative_sign",
        "existence_certification",
    ]),
    "B2a.endpoint_open_region_reference": sorted([
        "registry_occurrence_id",
        "Round204_region_row_id",
        "Round204_region_row_sha256",
        "target_factor_sign",
        "Round294_registry_row_id",
        "Round294_registry_row_sha256",
        "Round301_member_reference",
    ]),
    "B2a.analytic_conclusion": sorted([
        "Gamma_nonempty",
        "Gamma_unique_graph_over_connected_positive_area_base",
        "Gamma_connected",
        "physical_inclusion_claimed_at_B2a",
    ]),
    "edge.source_lemma_reference": sorted([
        "row_id",
        "row_sha256",
    ]),
    "unresolved.endpoint_reference": sorted([
        "endpoint",
        "row_id",
        "row_sha256",
        "missing_obligation",
    ]),
}

REQUIRED_BEFORE_EDGE_CONSUMPTION = [
    (
        "Run this producer under two distinct nonempty seeds and "
        "confirm exact byte-identical outputs."
    ),
    (
        "Run a separately implemented cacheless verifier and its "
        "focused re-sign, schema, semantic, and path attacks."
    ),
    (
        "Seal the producer, five ledgers, result, verifier, "
        "verification, attack suite, dual-seed replay, and cold "
        "replay in one exact manifest before edge consumption."
    ),
]

EXPECTED_RESULT_INPUT_PINS = dict(sorted({
    **BASE_INPUT_PINS,
    **EXECUTABLE_TRANSITIVE_CLOSURE_PINS,
    **RAW_R303A_PINS,
    R303A_MANIFEST: R303A_MANIFEST_SHA256,
    **R303A_SEAL_MEMBER_PINS,
}.items()))

RESULT_TOP_KEYS = sorted([
    "schema",
    "status",
    "producer_sha256",
    "seed_affects_output",
    "complete_formal_run",
    "provisional_Round303A_consumed",
    "input_file_pins",
    "executable_runtime_closure",
    "Round303A_seal",
    "Round294B_registry_builder_admission",
    "theorem",
    "theorem_sha256",
    "theorem_objects",
    "scope_census",
    "run_census",
    "output_ledgers",
    "formal_credit_transition",
    "strict_nonclaims",
    "atomicity_contract",
    "required_before_edge_consumption",
    "result_sha256",
])

RESULT_NESTED_KEY_SETS = {
    "executable_runtime_closure": sorted([
        "entrypoint",
        "transitive_file_pins",
        "recursive_import_graph",
        "module_files_exactly_pinned",
        "sys_modules_alternates_cleared",
        "python_flint_version",
        "interval_precision_bits",
    ]),
    "Round303A_seal": sorted([
        "manifest_filename",
        "manifest_file_sha256",
        "manifest_member_count",
        "manifest_members",
        "manifest_exact_member_set_checked",
        "manifest_member_hashes_checked",
    ]),
    "Round294B_registry_builder_admission": sorted([
        "manifest_filename",
        "manifest_file_sha256",
        "manifest_member_count",
        "verification_filename",
        "verification_file_sha256",
        "verification_object_sha256",
        "formal_occurrence_registry_row_count",
        "formal_representation_binding_count",
        "direct_Round287_union_issuance_count_rejected",
        "binding_rows_issuing_occurrence_ID_count",
        "admission_checked_before_Round294_consumption",
        "bypass_permitted",
    ]),
    "scope_census": sorted([
        "Round300D_rows",
        "cross_Round301_pairs",
        "B1_scope_pairs",
        "B1_accepted_pairs",
        "B2_accepted_pairs",
        "W_tail_unresolved_pairs",
        "accepted_plus_unresolved",
        "selected_distinct_endpoint_count",
        "old_63224_component_result_reused",
        "conditional_DSU_result_consumed",
    ]),
    "run_census": sorted([
        "B1_rows",
        "B2a_rows",
        "B2b_rows",
        "candidate_edge_rows",
        "W_tail_unresolved_rows",
    ]),
    "output_ledger_entry": sorted([
        "filename",
        "schema",
        "row_count",
        "row_ids_sha256",
        "row_hashes_sha256",
        "rows_sha256",
        "file_sha256",
    ]),
    "theorem_objects": sorted([
        "B1_monotone_closure",
        "B2a_FULL_2D_analytic_closure",
        "B2b_target_factor_sheet_inclusion",
        "G0_G5_final_gluing",
    ]),
    "B1_monotone_closure": sorted([
        "theorem",
        "theorem_sha256",
        "kernel_theorem",
        "kernel_theorem_sha256",
    ]),
    "single_theorem_entry": sorted([
        "theorem",
        "theorem_sha256",
    ]),
    "B2b_target_factor_sheet_inclusion": sorted([
        "theorem",
        "theorem_sha256",
        "target_factor_sheet_theorem",
        "target_factor_sheet_theorem_sha256",
    ]),
    "formal_credit_transition": sorted([
        "formal_component_edge_credit",
        *ZERO_FIELDS,
    ]),
    "strict_nonclaims": sorted([
        "occurrence_identity_collapsed",
        "official_key_identity_merged",
        "Round301_DSU_mutated_or_reused",
        "old_63224_partition_used",
        "conditional_92696_partition_used",
        "maximality_claimed",
        "fibre_exhaustion_claimed",
        "global_disposition_claimed",
        "W_tail_rows_are_nonedges_or_exclusions",
    ]),
    "atomicity_contract": sorted([
        "five_ledgers_staged_before_any_publication",
        "result_staged_before_any_publication",
        "ledger_batch_directory_fsynced_before_result",
        "result_published_no_replace_last_as_commit_marker",
        "output_directory_fsynced_after_result_commit",
        "all_six_targets_no_clobber",
        "result_absent_reuses_only_exact_prior_crash_ledgers",
        "result_present_idempotence_requires_all_six_exact",
        "mismatched_existing_target_left_untouched_and_rejected",
        "nlink2_crash_orphan_requires_manual_recovery",
        "partial_formal_promotion_permitted",
        "sample_run_writes_formal_outputs",
    ]),
}

SCHEMA_SNAPSHOT = {
    "schema": "cm2.round303b.independent-schema-snapshot.v1",
    "package_schema": SCHEMA,
    "output_names": dict(sorted(OUTPUTS.items())),
    "ledger_tables": dict(sorted(TABLES.items())),
    "row_id_fields": dict(sorted(ID_FIELDS.items())),
    "row_id_prefixes": dict(sorted(ID_PREFIXES.items())),
    "row_id_contexts": dict(sorted(ID_CONTEXTS.items())),
    "ledger_exact_key_sets": {
        route: sorted([
            "every_row_closed_by_own_SHA256",
            "row_count",
            "row_hashes_sha256",
            "row_ids_sha256",
            "rows_sha256",
            "schema",
            "status",
            TABLES[route],
        ])
        for route in ID_FIELDS
    },
    "row_exact_key_sets": ROW_KEY_SETS,
    "B2_exact_join_key_sets": {
        "B2a_common": B2A_COMMON_EXACT_JOIN_KEYS,
        "B2b_common_plus_physical": B2B_EXACT_JOIN_KEYS,
    },
    "Round182_face_certificate_exact_keys": FACE_CERTIFICATE_KEYS,
    "Round301_member_reference_exact_keys":
        ROUND301_MEMBER_REFERENCE_KEYS,
    "nested_exact_key_sets": {
        path: keys for path, keys in sorted(NESTED_KEY_SETS.items())
    },
    "result_top_keys": RESULT_TOP_KEYS,
    "result_nested_key_sets": RESULT_NESTED_KEY_SETS,
    "executable_transitive_closure_pins": dict(sorted(
        EXECUTABLE_TRANSITIVE_CLOSURE_PINS.items()
    )),
    "executable_recursive_import_graph": {
        name: sorted(children)
        for name, children in sorted(EXECUTABLE_IMPORT_GRAPH.items())
    },
    "result_exact_dynamic_values": {
        "input_file_pins": EXPECTED_RESULT_INPUT_PINS,
        "executable_transitive_closure_pins": dict(sorted(
            EXECUTABLE_TRANSITIVE_CLOSURE_PINS.items()
        )),
        "executable_recursive_import_graph": {
            name: sorted(children)
            for name, children in sorted(
                EXECUTABLE_IMPORT_GRAPH.items()
            )
        },
        "Round303A_manifest_members":
            dict(sorted(R303A_SEAL_MEMBER_PINS.items())),
        "required_before_edge_consumption":
            REQUIRED_BEFORE_EDGE_CONSUMPTION,
    },
    "theorem_object_hashes": {
        "B1_layer": B1_LAYER_THEOREM_SHA256,
        "B1_monotone_kernel": MONOTONE_LIMIT_THEOREM_SHA256,
        "B2a_FULL_2D_layer": B2A_LAYER_THEOREM_SHA256,
        "B2b_identity_lift_layer": B2B_LAYER_THEOREM_SHA256,
        "G0_G5_gluing": THEOREM_SHA256,
    },
    "Round294B_admission_closure": {
        "manifest_filename": R294B_MANIFEST,
        "manifest_file_sha256": R294B_MANIFEST_SHA256,
        "verification_filename": R294B_VERIFICATION,
        "verification_file_sha256": R294B_VERIFICATION_FILE_SHA256,
        "verification_object_sha256":
            R294B_VERIFICATION_OBJECT_SHA256,
        "bypass_permitted": False,
    },
    "R204_required_selector": FULL_2D_CERT,
    "R204_forbidden_selector": TAIL_CERT,
    "lexical_output_row_id_order": True,
}
COMPUTED_SCHEMA_SNAPSHOT_SHA256 = digest(SCHEMA_SNAPSHOT)


def validate_schema_snapshot() -> None:
    need(
        FINAL_R303B_SCHEMA_SNAPSHOT_SHA256
        == COMPUTED_SCHEMA_SNAPSHOT_SHA256,
        "R303B_SCHEMA_SNAPSHOT_DIGEST",
    )


def regular_single_link(path: Path, label: str) -> None:
    need(path.is_file() and not path.is_symlink(), "INPUT_PATH:" + label)
    info = path.stat()
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and info.st_size > 0,
        "INPUT_REGULAR_SINGLE_LINK:" + label,
    )


def validate_base_boundary(input_dir: Path) -> None:
    need(
        input_dir.resolve() == INPUT_DIR.resolve(),
        "FORMAL_INPUT_DIR_MUST_BE_DELIVERABLES",
    )
    for name, expected in BASE_INPUT_PINS.items():
        path = input_dir / name
        regular_single_link(path, name)
        need(file_sha256(path) == expected, "BASE_PIN:" + name)
    for name, expected in EXECUTABLE_TRANSITIVE_CLOSURE_PINS.items():
        path = input_dir / name
        regular_single_link(path, "EXECUTABLE_CLOSURE:" + name)
        need(
            file_sha256(path) == expected,
            "EXECUTABLE_CLOSURE_PIN:" + name,
        )
    need(
        EXECUTABLE_TRANSITIVE_CLOSURE_PINS[R179_KERNEL]
        == BASE_INPUT_PINS[R179_KERNEL],
        "R179_EXECUTABLE_PIN_AGREEMENT",
    )
    for manifest_name, expected_members in BASE_MANIFEST_MEMBERS.items():
        members = parse_manifest(input_dir / manifest_name)
        if manifest_name in {R182_PACKAGE_MANIFEST, R294B_MANIFEST}:
            need(
                set(members) == set(expected_members),
                "BASE_MANIFEST_EXACT_MEMBER_SET:" + manifest_name,
            )
        for name, expected in expected_members.items():
            need(
                members.get(name) == expected,
                "BASE_MANIFEST_MEMBER:" + manifest_name + ":" + name,
            )
    validate_r294b_admission(input_dir)


def validate_r294b_verification_object(
    verification: Any,
) -> None:
    try:
        need(
            type(verification) is dict,
            "ROUND294B_VERIFICATION_OBJECT_TYPE",
        )
        claimed = verification.get("verification_sha256")
        payload = dict(verification)
        payload.pop("verification_sha256", None)
        census = verification["independent_registry_census"]
        direct = verification["direct_actual_file_audit"]
        independence = verification["independence_contract"]
        manifest_audit = verification["manifest_exact_set_audit"]
        nonpromotion = verification["strict_nonpromotion"]
        credits = verification["formal_credit_transition"]
        need(
            claimed == R294B_VERIFICATION_OBJECT_SHA256
            and digest(payload) == claimed
            and verification["status"] == (
                "PASS_INDEPENDENT_ROUND294B_ZERO_CREDIT_ADMISSION__"
                "ACTUAL_R292A_VERIFIER_DIRECT_PIN__7_PLUS_9_EXACT_MANIFESTS__"
                "431208_REGISTRY_ROWS__46288_BINDINGS__"
                "38_OF_38_ATTACKS_REJECTED"
            )
            and verification["attack_audit"]["attack_count"] == 38
            and verification["attack_audit"][
                "rejected_attack_count"
            ] == 38
            and verification["attack_audit"][
                "accepted_attack_count"
            ] == 0
            and verification["attack_audit"][
                "all_attacks_rejected"
            ] is True
            and census["formal_occurrence_registry_row_count"] == 431_208
            and census["formal_representation_binding_count"] == 46_288
            and census["binding_rows_issuing_occurrence_ID_count"] == 0
            and census[
                "direct_Round287_union_issuance_count_rejected"
            ] == 10_020
            and census["legacy_63224_as_current_quotient_rejected"] is True
            and census["superseded_registry_row_count_rejected"] == 431_824
            and direct["Round294_manifest_sha256"]
            == BASE_INPUT_PINS[
                "cm2_round294_source_g_occurrence_registry_atomic_"
                "promotion_manifest.sha256"
            ]
            and direct["Round292_builder_sha256"]
            == R294B_PACKAGE_MEMBER_PINS[
                "cm2_round292_source_g_occurrence_registry_"
                "candidate_construction.py"
            ]
            and verification["candidate_artifacts"]["producer_sha256"]
            == R294B_PACKAGE_MEMBER_PINS[R294B_PACKAGE_PREFIX + ".py"]
            and verification["candidate_artifacts"]["verifier_sha256"]
            == R294B_PACKAGE_MEMBER_PINS[
                R294B_PACKAGE_PREFIX + "_verifier.py"
            ]
            and manifest_audit["Round292A_member_count"] == 7
            and manifest_audit["Round294_member_count"] == 9
            and manifest_audit["all_16_members_actual_hash_match"] is True
            and manifest_audit["extra_or_missing_member_count"] == 0
            and independence[
                "Round292A_or_Round294_producer_imported_or_executed"
            ] is False
            and independence[
                "Round294B_producer_imported_or_executed"
            ] is False
            and independence["candidate_used_as_expected_oracle"] is False
            and nonpromotion[
                "post_Round294_expanded_registry_component_DSU_status"
            ] == "NOT_REBUILT"
            and nonpromotion[
                "post_Round294_quotient_component_count"
            ] is None
            and all(value == 0 for value in credits.values()),
            "ROUND294B_ADMISSION_VERIFICATION_CLOSURE",
        )
    except (KeyError, TypeError, AttributeError) as exc:
        raise VerificationError(
            "ROUND294B_ADMISSION_VERIFICATION_SCHEMA"
        ) from exc


def validate_r294b_admission(input_dir: Path) -> None:
    manifest = parse_manifest(input_dir / R294B_MANIFEST)
    need(
        len(manifest) == 11
        and set(manifest) == set(R294B_PACKAGE_MEMBER_PINS),
        "ROUND294B_EXACT_ELEVEN_MEMBER_MANIFEST",
    )
    for name, expected in R294B_PACKAGE_MEMBER_PINS.items():
        need(
            manifest[name] == expected,
            "ROUND294B_MANIFEST_MEMBER:" + name,
        )
    validate_r294b_verification_object(
        read_json(input_dir / R294B_VERIFICATION)
    )


def r303a_seal_ready() -> bool:
    values = [
        R303A_MANIFEST_SHA256,
        *R303A_SEAL_MEMBER_PINS.values(),
    ]
    return all(
        type(value) is str and PIN_RE.fullmatch(value) is not None
        for value in values
    )


def seal_ready() -> bool:
    return (
        r303a_seal_ready()
        and type(FINAL_R303B_PRODUCER_SHA256) is str
        and PIN_RE.fullmatch(FINAL_R303B_PRODUCER_SHA256) is not None
        and type(FINAL_R303B_SCHEMA_SNAPSHOT_SHA256) is str
        and PIN_RE.fullmatch(FINAL_R303B_SCHEMA_SNAPSHOT_SHA256) is not None
        and FINAL_R303B_SCHEMA_SNAPSHOT_SHA256
        == COMPUTED_SCHEMA_SNAPSHOT_SHA256
    )


def validate_r303a_formal_boundary(input_dir: Path) -> None:
    need(r303a_seal_ready(), "R303A_SEAL_PINS_UNFILLED")
    need(
        type(R303A_MANIFEST_SHA256) is str,
        "R303A_MANIFEST_PIN_TYPE",
    )
    manifest_path = input_dir / R303A_MANIFEST
    regular_single_link(manifest_path, R303A_MANIFEST)
    need(
        file_sha256(manifest_path) == R303A_MANIFEST_SHA256,
        "R303A_MANIFEST_PIN",
    )
    members = parse_manifest(manifest_path)
    need(
        set(members) == set(R303A_SEAL_MEMBER_PINS),
        "R303A_MANIFEST_EXACT_TEN_MEMBER_SET",
    )
    need(len(members) == 10, "R303A_MANIFEST_EXACT_TEN_MEMBER_CENSUS")
    for name, expected in R303A_SEAL_MEMBER_PINS.items():
        need(type(expected) is str, "R303A_MEMBER_PIN_TYPE:" + name)
        path = input_dir / name
        regular_single_link(path, name)
        need(members[name] == expected, "R303A_MANIFEST_PIN:" + name)
        need(file_sha256(path) == expected, "R303A_MEMBER_PIN:" + name)


def validate_raw_r303a_scope_boundary(input_dir: Path) -> None:
    for name, expected in RAW_R303A_PINS.items():
        path = input_dir / name
        regular_single_link(path, name)
        need(file_sha256(path) == expected, "RAW_R303A_PIN:" + name)


def reconstruct_scope(
    input_dir: Path,
    *,
    provisional: bool,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    validate_base_boundary(input_dir)
    if provisional:
        validate_raw_r303a_scope_boundary(input_dir)
    else:
        validate_r303a_formal_boundary(input_dir)

    raw: dict[str, dict[str, Any]] = {}
    endpoints: set[str] = set()
    all_pairs: set[tuple[str, str]] = set()
    tranches: Counter[str] = Counter()
    for row in iter_array(
        input_dir / R300D, "canonical_incidence_edge_rows"
    ):
        row_id = row.get(
            "Round300D_lower_physical_witness_incidence_edge_row_id"
        )
        need(
            type(row_id) is str and row_id not in raw,
            "R300D_UNIQUE_ROW",
        )
        verify_row(row, row_id)
        pair = canonical_pair(
            row["canonical_unordered_Round294_registry_occurrence_ids"],
            row_id,
        )
        need(pair not in all_pairs, "R300D_UNIQUE_CANONICAL_PAIR")
        all_pairs.add(pair)
        left = row["left_endpoint"]
        right = row["right_endpoint"]
        need(
            [left["registry_occurrence_id"], right["registry_occurrence_id"]]
            == list(pair)
            and row["shared_lower_witness_incidence_proved"] is True
            and row["included_stratum_gluing_lemma_pinned"] is False
            and row["formal_component_edge_credit"] == 0
            and row["eligible_for_component_DSU_application"] is False,
            "R300D_FAIL_CLOSED:" + row_id,
        )
        tranche = (
            left["registry_entry_kind"]
            + "|"
            + right["registry_entry_kind"]
        )
        endpoint_refs = {
            endpoint["registry_occurrence_id"]: {
                "row_id": endpoint["Round294_occurrence_registry_row_id"],
                "row_sha256":
                    endpoint["Round294_occurrence_registry_row_sha256"],
                "kind": endpoint["registry_entry_kind"],
                "chart": endpoint["physical_support_chart"],
                "official_key_id":
                    endpoint["final_Round299A_official_key_id"],
                "official_key_ordinal":
                    endpoint["final_Round299A_official_key_ordinal"],
                "signature_sha256":
                    endpoint["complete_10_field_return_signature_sha256"],
            }
            for endpoint in (left, right)
        }
        raw[row_id] = {
            "source_id": row_id,
            "source_sha256": row["row_sha256"],
            "pair": pair,
            "tranche": tranche,
            "endpoint_refs": endpoint_refs,
            "r295_ids": list(
                row[
                    "source_Round295A_physical_incidence_binding_row_ids"
                ]
            ),
            "r295_hashes": list(
                row[
                    "source_Round295A_physical_incidence_binding_row_sha256s"
                ]
            ),
            "r291_ids": list(
                row["source_Round291_local_disposition_row_ids"]
            ),
            "cell_indices": list(row["physical_witness_cell_indices"]),
            "source_charts": list(row["source_charts"]),
            "witness_kind_histogram": dict(
                row["witness_kind_histogram"]
            ),
            "witness_multiplicity": row["witness_multiplicity"],
        }
        endpoints.update(pair)
        tranches[tranche] += 1
    need(len(raw) == EXPECTED_R300D, "R300D_CENSUS")
    need(len(all_pairs) == EXPECTED_R300D, "R300D_PAIR_CENSUS")
    need(
        tranches
        == Counter({
            R288_KIND + "|" + R288_KIND: 111_332,
            PRESERVED_KIND + "|" + PRESERVED_KIND: EXPECTED_B2,
        }),
        "R300D_TRANCHE_CENSUS",
    )

    members: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_dir / R301_MEMBERS, "rows"):
        endpoint = row.get("registry_or_frontier_member_id")
        if endpoint not in endpoints:
            continue
        verify_row(row, str(endpoint))
        need(
            endpoint not in members
            and row["member_kind"] in {
                "EXPANDED_OCCURRENCE",
                R288_KIND,
                PRESERVED_KIND,
            }
            and row["formal_component_membership_credit"] == 1
            and row["member_identity_preserved"] is True
            and row["formal_occurrence_identity_collapse_credit"] == 0,
            "R301_MEMBER_CONTRACT:" + str(endpoint),
        )
        members[str(endpoint)] = {
            "row_id": row["Round301_member_to_component_row_id"],
            "row_sha256": row["row_sha256"],
            "component_id": row["final_Round301_component_id"],
            "base_root_id": row["base_component_root_id"],
            "official_key_id": row["official_key_id"],
            "member_kind": row["member_kind"],
        }
    need(set(members) == endpoints, "R301_ENDPOINT_COVERAGE")

    component_cross_ids = {
        row_id
        for row_id, item in raw.items()
        if members[item["pair"][0]]["component_id"]
        != members[item["pair"][1]]["component_id"]
    }

    residual_refs: dict[str, dict[str, Any]] = {}
    consumed: set[str] = set()
    for row in iter_array(input_dir / R301_INELIGIBLE, "rows"):
        if row.get("source_relation") != R301_SOURCE_RELATION:
            continue
        source_id = row.get("source_row_id")
        need(
            source_id in raw and source_id not in consumed,
            "R301_SOURCE_UNIQUE",
        )
        verify_row(row, str(source_id))
        source = raw[str(source_id)]
        need(
            row["source_row_sha256"] == source["source_sha256"]
            and canonical_pair(
                row["canonical_occurrence_endpoint_pair"],
                str(source_id),
            ) == source["pair"]
            and row["source_row_fed_to_DSU"] is False
            and row["eligible_for_component_DSU_application"] is False
            and row["formal_DSU_rank_reduction_credit"] == 0
            and row["formal_component_edge_application_credit"] == 0,
            "R301_SOURCE_FAIL_CLOSED:" + str(source_id),
        )
        consumed.add(str(source_id))
        if row["disposition"] == R301_UNRESOLVED:
            residual_refs[str(source_id)] = {
                "row_id":
                    row["Round301_ineligible_source_consumption_row_id"],
                "row_sha256": row["row_sha256"],
                "disposition": row["disposition"],
            }
    need(consumed == set(raw), "R301_COMPLETE_R300D_CONSUMPTION")
    need(len(residual_refs) == 110_516, "R301_RESIDUAL_CENSUS")
    cross_ids = component_cross_ids & set(residual_refs)
    need(len(cross_ids) == EXPECTED_CROSS, "CROSS_ROUND301_CENSUS")
    cross_pairs = {raw[source_id]["pair"] for source_id in cross_ids}
    cross_endpoints = {
        endpoint
        for source_id in cross_ids
        for endpoint in raw[source_id]["pair"]
    }
    need(
        len(cross_pairs) == EXPECTED_CROSS
        and len(cross_endpoints) == EXPECTED_ENDPOINTS,
        "CROSS_ROUND301_EXACT_PAIR_ENDPOINT_CENSUS",
    )
    ineligible = {
        source_id: residual_refs[source_id] for source_id in cross_ids
    }
    need(set(ineligible) == cross_ids, "R301_CROSS_COVERAGE")

    bridges: dict[str, dict[str, Any]] = {}
    for row in iter_array(
        input_dir / R303A_BRIDGES, "materialized_bridge_rows"
    ):
        endpoint = row.get("registry_occurrence_id")
        need(
            type(endpoint) is str and endpoint not in bridges,
            "R303A_SCOPE_BRIDGE_UNIQUE",
        )
        verify_row(row, endpoint)
        scope_ref = row["Round300D_Round301_scope_reference"]
        side = row["connected_source_side_witness"]
        need(
            row["theorem_id"] == R303A_THEOREM_ID
            and row[
                "A0_exact_provenance_pins_and_row_closures"
            ] is True
            and row[
                "A4_unique_formal_connected_source_signed_region_materialized"
            ] is True
            and row["eligible_as_R303B_G1_bridge_input"] is True
            and row[
                "formal_occurrence_anchor_connected_side_bridge_credit"
            ] == 1
            and row["formal_component_edge_credit"] == 0
            and side["connected"] is True,
            "R303A_SCOPE_BRIDGE_CONTRACT:" + endpoint,
        )
        bridges[endpoint] = {
            "source_id": scope_ref["source_Round300D_row_id"],
            "source_sha256": scope_ref["source_Round300D_row_sha256"],
            "opposite_endpoint": scope_ref["opposite_endpoint"],
            "source_R301_row_id":
                scope_ref["source_Round301_ineligible_row_id"],
            "source_R301_row_sha256":
                scope_ref["source_Round301_ineligible_row_sha256"],
        }
    gaps: dict[str, dict[str, Any]] = {}
    for row in iter_array(
        input_dir / R303A_UNRESOLVED, "unresolved_bridge_rows"
    ):
        endpoint = row.get("registry_occurrence_id")
        need(
            type(endpoint) is str and endpoint not in gaps,
            "R303A_SCOPE_GAP_UNIQUE",
        )
        verify_row(row, endpoint)
        scope_ref = row["Round300D_Round301_scope_reference"]
        need(
            row[
                "A4_unique_formal_connected_source_signed_region_materialized"
            ] is False
            and row["eligible_as_R303B_G1_bridge_input"] is False
            and row[
                "formal_occurrence_anchor_connected_side_bridge_credit"
            ] == 0
            and row["formal_component_edge_credit"] == 0
            and row["nonedge_or_exclusion_claimed"] is False
            and row["disposition"] == R303A_WTAIL,
            "R303A_SCOPE_GAP_CONTRACT:" + endpoint,
        )
        gaps[endpoint] = {
            "source_id": scope_ref["source_Round300D_row_id"],
            "source_sha256": scope_ref["source_Round300D_row_sha256"],
            "opposite_endpoint": scope_ref["opposite_endpoint"],
            "source_R301_row_id":
                scope_ref["source_Round301_ineligible_row_id"],
            "source_R301_row_sha256":
                scope_ref["source_Round301_ineligible_row_sha256"],
        }
    need(
        set(bridges).isdisjoint(gaps)
        and len(bridges) == 87_824
        and len(gaps) == 8,
        "R303A_SCOPE_ENDPOINT_PARTITION",
    )

    b1: list[dict[str, Any]] = []
    b2: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    r288_endpoints: set[str] = set()
    for source_id in sorted(cross_ids):
        record = deepcopy(raw[source_id])
        pair = record["pair"]
        record["member_refs"] = {
            endpoint: deepcopy(members[endpoint]) for endpoint in pair
        }
        record["r301_ineligible_ref"] = deepcopy(
            ineligible[source_id]
        )
        if record["tranche"] == PRESERVED_KIND + "|" + PRESERVED_KIND:
            b2.append(record)
            continue
        need(
            record["tranche"] == R288_KIND + "|" + R288_KIND,
            "KNOWN_CROSS_TRANCHE",
        )
        r288_endpoints.update(pair)
        accepted = set(pair) <= set(bridges)
        withheld = set(pair) <= set(gaps)
        need(
            accepted ^ withheld,
            "R303A_WHOLE_PAIR_PARTITION:" + source_id,
        )
        refs = bridges if accepted else gaps
        for endpoint in pair:
            ref = refs[endpoint]
            opposite = next(item for item in pair if item != endpoint)
            need(
                ref["source_id"] == source_id
                and ref["source_sha256"] == record["source_sha256"]
                and ref["opposite_endpoint"] == opposite
                and ref["source_R301_row_id"]
                == record["r301_ineligible_ref"]["row_id"]
                and ref["source_R301_row_sha256"]
                == record["r301_ineligible_ref"]["row_sha256"],
                "R303A_SCOPE_EXACT_JOIN:" + endpoint,
            )
        (b1 if accepted else unresolved).append(record)
    need(
        set(bridges) | set(gaps) == r288_endpoints,
        "R303A_EXACT_R288_ENDPOINT_COVERAGE",
    )
    need(
        len(b1) == EXPECTED_B1
        and len(b2) == EXPECTED_B2
        and len(unresolved) == EXPECTED_WTAIL,
        "SCOPE_ROUTE_CENSUS",
    )
    route_pairs = {
        "B1": {record["pair"] for record in b1},
        "B2": {record["pair"] for record in b2},
        "W_tail": {record["pair"] for record in unresolved},
    }
    route_endpoints = {
        route: {
            endpoint
            for record in records
            for endpoint in record["pair"]
        }
        for route, records in (
            ("B1", b1),
            ("B2", b2),
            ("W_tail", unresolved),
        )
    }
    need(
        len(route_pairs["B1"]) == EXPECTED_B1
        and len(route_pairs["B2"]) == EXPECTED_B2
        and len(route_pairs["W_tail"]) == EXPECTED_WTAIL
        and route_pairs["B1"].isdisjoint(route_pairs["B2"])
        and route_pairs["B1"].isdisjoint(route_pairs["W_tail"])
        and route_pairs["B2"].isdisjoint(route_pairs["W_tail"])
        and set().union(*route_pairs.values()) == cross_pairs
        and len(route_endpoints["B1"]) == 2 * EXPECTED_B1
        and len(route_endpoints["B2"]) == 2 * EXPECTED_B2
        and len(route_endpoints["W_tail"]) == 2 * EXPECTED_WTAIL
        and route_endpoints["B1"].isdisjoint(route_endpoints["B2"])
        and route_endpoints["B1"].isdisjoint(route_endpoints["W_tail"])
        and route_endpoints["B2"].isdisjoint(route_endpoints["W_tail"])
        and set().union(*route_endpoints.values()) == cross_endpoints
        and len(cross_endpoints) == EXPECTED_ENDPOINTS,
        "SCOPE_EXACT_PAIR_ENDPOINT_ROUTE_PARTITION",
    )
    return b1, b2, unresolved


def enrich_from_r300d(
    input_dir: Path,
    routes: tuple[
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
    ],
) -> None:
    all_records = [record for route in routes for record in route]
    by_id = {record["source_id"]: record for record in all_records}
    need(len(by_id) == EXPECTED_CROSS, "R300D_SELECTED_UNIQUE")
    seen: set[str] = set()
    for row in iter_array(
        input_dir / R300D, "canonical_incidence_edge_rows"
    ):
        row_id = row.get(
            "Round300D_lower_physical_witness_incidence_edge_row_id"
        )
        if row_id not in by_id:
            continue
        verify_row(row, str(row_id))
        record = by_id[row_id]
        pair = canonical_pair(
            row["canonical_unordered_Round294_registry_occurrence_ids"],
            str(row_id),
        )
        need(
            row_id not in seen
            and pair == record["pair"]
            and row["row_sha256"] == record["source_sha256"],
            "R300D_SELECTED_EXACT:" + str(row_id),
        )
        left = row["left_endpoint"]
        right = row["right_endpoint"]
        need(
            [left["registry_occurrence_id"], right["registry_occurrence_id"]]
            == list(pair),
            "R300D_ENDPOINT_ORDER:" + str(row_id),
        )
        record["endpoint_refs"] = {
            endpoint["registry_occurrence_id"]: {
                "row_id": endpoint["Round294_occurrence_registry_row_id"],
                "row_sha256":
                    endpoint["Round294_occurrence_registry_row_sha256"],
                "kind": endpoint["registry_entry_kind"],
                "chart": endpoint["physical_support_chart"],
                "official_key_id":
                    endpoint["final_Round299A_official_key_id"],
                "official_key_ordinal":
                    endpoint["final_Round299A_official_key_ordinal"],
                "signature_sha256":
                    endpoint["complete_10_field_return_signature_sha256"],
            }
            for endpoint in (left, right)
        }
        record["r295_ids"] = list(
            row["source_Round295A_physical_incidence_binding_row_ids"]
        )
        record["r295_hashes"] = list(
            row["source_Round295A_physical_incidence_binding_row_sha256s"]
        )
        record["r291_ids"] = list(
            row["source_Round291_local_disposition_row_ids"]
        )
        record["cell_indices"] = list(row["physical_witness_cell_indices"])
        record["source_charts"] = list(row["source_charts"])
        record["witness_kind_histogram"] = dict(
            row["witness_kind_histogram"]
        )
        record["witness_multiplicity"] = row["witness_multiplicity"]
        seen.add(str(row_id))
    need(seen == set(by_id), "R300D_SELECTED_COVERAGE")


def normalized_A_definition(contract: str, sign: str) -> str:
    if contract in {
        "ROUND269_DIRECT_WHOLE_LEAF_F_SIGN_SIDE",
        "ROUND270_DIRECT_WHOLE_LEAF_F_SIGN_SIDE",
    }:
        return (
            "{x in exact pinned Round182 leaf: active_F(x) has "
            + sign + "}"
        )
    if contract == (
        "ROUND271_SINGLE_ACTIVE_FACTOR_STRICT_T_MONOTONE_WHOLE_F_SIGN_SIDE"
    ):
        return (
            "{x in exact pinned Round182 wall leaf: active target_F(x) has "
            + sign + "}"
        )
    need(
        contract == (
            "ROUND272_ONE_SIDED_SOURCE_FACTOR_TARGET_ONLY_ACTIVE_"
            "WHOLE_F_SIGN_SIDE"
        ),
        "KNOWN_NORMALIZED_A_CONTRACT",
    )
    return (
        "{x in relative-open pinned Round182 wall leaf excluding t=0: "
        "active target_F(x) has " + sign + "}"
    )


def compact_bridge(row: dict[str, Any]) -> dict[str, Any]:
    endpoint = row["registry_occurrence_id"]
    scope = row["Round300D_Round301_scope_reference"]
    witness = row["connected_source_side_witness"]
    need(
        row["theorem_id"] == R303A_THEOREM_ID
        and row["A0_exact_provenance_pins_and_row_closures"] is True
        and row[
            "A1_Round294_issued_occurrence_has_nonempty_inner_anchor"
        ] is True
        and row[
            "A2_strict_anchor_subbox_inside_issued_inner_support"
        ] is True
        and row[
            "A3_occurrence_atom_source_side_provenance_exactly_closed"
        ] is True
        and row[
            "A4_unique_formal_connected_source_signed_region_materialized"
        ] is True
        and row["eligible_as_R303B_G1_bridge_input"] is True
        and row[
            "formal_occurrence_anchor_connected_side_bridge_credit"
        ] == 1
        and row["formal_component_edge_credit"] == 0
        and row["full_occurrence_support_equality_claimed"] is False
        and witness["connected"] is True
        and witness[
            "strict_anchor_subbox_has_same_active_factor_sign"
        ] is True
        and row["active_factor_strict_sign"] in STRICT_SIGNS,
        "R303A_BRIDGE_CONTRACT:" + endpoint,
    )
    return {
        "endpoint": endpoint,
        "row_id":
            row["Round303A_occurrence_anchor_source_side_bridge_row_id"],
        "row_sha256": row["row_sha256"],
        "source_R300D_row_id": scope["source_Round300D_row_id"],
        "source_R300D_row_sha256": scope["source_Round300D_row_sha256"],
        "source_R301_row_id": scope["source_Round301_ineligible_row_id"],
        "source_R301_row_sha256":
            scope["source_Round301_ineligible_row_sha256"],
        "opposite_endpoint": scope["opposite_endpoint"],
        "Round301_member_row": scope["this_Round301_member_row"],
        "Round294_registry_reference": row["Round294_registry_reference"],
        "active_factor_strict_sign": row["active_factor_strict_sign"],
        "active_factor_equation": row["active_factor_equation"],
        "anchor_box": row["exact_strict_anchor_subbox"],
        "issued_inner_support_box": row["exact_issued_inner_support_box"],
        "connected_source_side_witness": witness,
        "source_side_row_references": row["source_side_row_references"],
        "Round182_leaf_reference": row["Round182_leaf_reference"],
        "Round179_active_geometry_reference":
            row["Round179_active_geometry_reference"],
        "theorem_id": row["theorem_id"],
        "theorem_sha256": row["theorem_sha256"],
    }


def compact_unresolved(row: dict[str, Any]) -> dict[str, Any]:
    endpoint = row["registry_occurrence_id"]
    scope = row["Round300D_Round301_scope_reference"]
    need(
        row["A0_exact_provenance_pins_and_row_closures"] is True
        and row[
            "A4_unique_formal_connected_source_signed_region_materialized"
        ] is False
        and row["eligible_as_R303B_G1_bridge_input"] is False
        and row[
            "formal_occurrence_anchor_connected_side_bridge_credit"
        ] == 0
        and row["formal_component_edge_credit"] == 0
        and row["nonedge_or_exclusion_claimed"] is False
        and row["disposition"]
        == "UNRESOLVED__W_TAIL_CONNECTED_SOURCE_SIDE_EXTENSION_MISSING",
        "R303A_UNRESOLVED_CONTRACT:" + endpoint,
    )
    return {
        "endpoint": endpoint,
        "row_id":
            row["Round303A_unresolved_occurrence_anchor_bridge_row_id"],
        "row_sha256": row["row_sha256"],
        "source_R300D_row_id": scope["source_Round300D_row_id"],
        "source_R300D_row_sha256": scope["source_Round300D_row_sha256"],
        "source_R301_row_id": scope["source_Round301_ineligible_row_id"],
        "source_R301_row_sha256":
            scope["source_Round301_ineligible_row_sha256"],
        "opposite_endpoint": scope["opposite_endpoint"],
        "missing_obligation": row["missing_obligation"],
        "disposition": row["disposition"],
    }


def attach_r303a_rows(
    input_dir: Path,
    b1_records: list[dict[str, Any]],
    unresolved_records: list[dict[str, Any]],
) -> None:
    wanted_bridges = {
        endpoint for record in b1_records for endpoint in record["pair"]
    }
    wanted_gaps = {
        endpoint
        for record in unresolved_records
        for endpoint in record["pair"]
    }
    bridges: dict[str, dict[str, Any]] = {}
    for row in iter_array(
        input_dir / R303A_BRIDGES, "materialized_bridge_rows"
    ):
        endpoint = row.get("registry_occurrence_id")
        if endpoint not in wanted_bridges:
            continue
        verify_row(row, str(endpoint))
        need(endpoint not in bridges, "R303A_BRIDGE_UNIQUE")
        bridges[endpoint] = compact_bridge(row)
    gaps: dict[str, dict[str, Any]] = {}
    for row in iter_array(
        input_dir / R303A_UNRESOLVED, "unresolved_bridge_rows"
    ):
        endpoint = row.get("registry_occurrence_id")
        if endpoint not in wanted_gaps:
            continue
        verify_row(row, str(endpoint))
        need(endpoint not in gaps, "R303A_GAP_UNIQUE")
        gaps[endpoint] = compact_unresolved(row)
    need(set(bridges) == wanted_bridges, "R303A_BRIDGE_COVERAGE")
    need(set(gaps) == wanted_gaps, "R303A_GAP_COVERAGE")
    for record in b1_records:
        record["bridge_refs"] = {
            endpoint: bridges[endpoint] for endpoint in record["pair"]
        }
        for endpoint, bridge in record["bridge_refs"].items():
            opposite = next(
                item for item in record["pair"] if item != endpoint
            )
            need(
                bridge["source_R300D_row_id"] == record["source_id"]
                and bridge["source_R300D_row_sha256"]
                == record["source_sha256"]
                and bridge["source_R301_row_id"]
                == record["r301_ineligible_ref"]["row_id"]
                and bridge["source_R301_row_sha256"]
                == record["r301_ineligible_ref"]["row_sha256"]
                and bridge["opposite_endpoint"] == opposite,
                "R303A_BRIDGE_SCOPE_JOIN:" + endpoint,
            )
    for record in unresolved_records:
        record["unresolved_refs"] = {
            endpoint: gaps[endpoint] for endpoint in record["pair"]
        }
        for endpoint, gap in record["unresolved_refs"].items():
            need(
                gap["source_R300D_row_id"] == record["source_id"]
                and gap["source_R300D_row_sha256"]
                == record["source_sha256"]
                and gap["source_R301_row_id"]
                == record["r301_ineligible_ref"]["row_id"]
                and gap["source_R301_row_sha256"]
                == record["r301_ineligible_ref"]["row_sha256"],
                "R303A_GAP_SCOPE_JOIN:" + endpoint,
            )


def load_r294(
    input_dir: Path,
    records: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    wanted = {
        endpoint for record in records for endpoint in record["pair"]
    }
    expected = {
        endpoint: record["endpoint_refs"][endpoint]
        for record in records
        for endpoint in record["pair"]
    }
    selected: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_dir / R294, "rows"):
        endpoint = row.get("registry_occurrence_id")
        if endpoint not in wanted:
            continue
        verify_row(row, str(endpoint))
        ref = expected[endpoint]
        need(
            endpoint not in selected
            and row["Round294_occurrence_registry_row_id"] == ref["row_id"]
            and row["row_sha256"] == ref["row_sha256"]
            and row["registry_entry_kind"] == ref["kind"]
            and row["physical_support_chart"] == ref["chart"]
            and row["official_key_id"] == ref["official_key_id"]
            and row["official_key_ordinal"] == ref["official_key_ordinal"]
            and row["complete_10_field_return_signature_sha256"]
            == ref["signature_sha256"],
            "R294_ENDPOINT_JOIN:" + str(endpoint),
        )
        selected[str(endpoint)] = row
    need(set(selected) == wanted, "R294_ENDPOINT_COVERAGE")
    return selected


def load_physical_chain(
    input_dir: Path,
    records: list[dict[str, Any]],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    wanted_295: dict[str, str] = {}
    for record in records:
        need(
            len(record["r295_ids"]) == len(record["r295_hashes"]) == 1
            and len(record["r291_ids"]) == len(record["cell_indices"]) == 1
            and record["witness_kind_histogram"]
            == {"ROUND182_GRAPH_SHEET_LEAF": 1}
            and record["witness_multiplicity"] == 1,
            "SINGLE_PHYSICAL_WITNESS:" + record["source_id"],
        )
        row_id = record["r295_ids"][0]
        need(row_id not in wanted_295, "R295_SELECTED_UNIQUE")
        wanted_295[row_id] = record["r295_hashes"][0]

    r295: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_dir / R295A, "rows"):
        row_id = row.get(
            "Round295A_R291_physical_incidence_binding_row_id"
        )
        if row_id not in wanted_295:
            continue
        verify_row(row, str(row_id))
        need(
            row_id not in r295
            and row["row_sha256"] == wanted_295[row_id]
            and row["Round295A_binding_classification"]
            == (
                "FORMAL_ROUND294_REGISTRY_REBIND__"
                "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            )
            and row["source_Round293_binding_classification"]
            == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and row[
                "exact_witness_covered_by_named_registry_supports"
            ] is True
            and row["formal_target_reference_credit"] == 2
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "R295_SELECTED_CONTRACT:" + str(row_id),
        )
        r295[str(row_id)] = row
    need(set(r295) == set(wanted_295), "R295_SELECTED_COVERAGE")

    wanted_293 = {
        row["source_Round293_R291_physical_witness_binding_row_id"]:
            row["source_Round293_R291_physical_witness_binding_row_sha256"]
        for row in r295.values()
    }
    r293: dict[str, dict[str, Any]] = {}
    for row in iter_array(
        input_dir / R293, "Round291_physical_witness_binding_rows"
    ):
        row_id = row.get("Round292_R291_physical_witness_binding_row_id")
        if row_id not in wanted_293:
            continue
        verify_row(row, str(row_id))
        need(
            row_id not in r293
            and row["row_sha256"] == wanted_293[row_id]
            and row["binding_classification"]
            == "EXACT_TWO_SIDED_GRAPH_SHEET_ATOM_INCIDENCE"
            and row[
                "exact_witness_covered_by_named_registry_supports"
            ] is True
            and row["component_edge_credit"] == 0,
            "R293_SELECTED_CONTRACT:" + str(row_id),
        )
        r293[str(row_id)] = row
    need(set(r293) == set(wanted_293), "R293_SELECTED_COVERAGE")

    requested_291: dict[str, set[int]] = {}
    for record in records:
        requested_291.setdefault(record["r291_ids"][0], set()).add(
            record["cell_indices"][0]
        )
    r291: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_dir / R291, "rows"):
        row_id = row.get(
            "complete_lower_stratum_local_disposition_row_id"
        )
        if row_id not in requested_291:
            continue
        verify_row(row, str(row_id))
        need(
            row_id not in r291
            and row["local_disposition"] == "WHOLE_PHYSICAL_SUPPORT"
            and row["representation_role"] == "DIRECT_GRAPH_SHEET_WITNESS"
            and row["component_edge_credit"] == 0,
            "R291_INCLUDED_ROW:" + str(row_id),
        )
        cells: dict[int, dict[str, Any]] = {}
        for index in requested_291[str(row_id)]:
            need(
                0 <= index < len(row["physical_witness_cells"]),
                "R291_CELL_INDEX",
            )
            cell = row["physical_witness_cells"][index]
            need(
                cell["witness_kind"] == "ROUND182_GRAPH_SHEET_LEAF"
                and Q(cell["base_coordinate_area"]) > 0,
                "R291_POSITIVE_GRAPH_CELL",
            )
            cells[index] = cell
        r291[str(row_id)] = {"row": row, "cells": cells}
    need(set(r291) == set(requested_291), "R291_SELECTED_COVERAGE")

    for record in records:
        row295 = r295[record["r295_ids"][0]]
        row293 = r293[
            row295[
                "source_Round293_R291_physical_witness_binding_row_id"
            ]
        ]
        need(
            row295["Round291_local_disposition_row_id"]
            == row293["Round291_local_disposition_row_id"]
            == record["r291_ids"][0]
            and row295["physical_witness_cell_index"]
            == row293["physical_witness_cell_index"]
            == record["cell_indices"][0]
            and sorted(row295["target_Round294_registry_occurrence_ids"])
            == sorted(row293["terminal_registry_target_references"])
            == list(record["pair"])
            and row295[
                "source_Round293_R291_physical_witness_binding_row_sha256"
            ] == row293["row_sha256"],
            "PHYSICAL_CHAIN_EXACT:" + record["source_id"],
        )
    return r295, r293, r291


R182_LEAF_COLUMNS = [
    "row_id", "occurrence_row_id", "retained_child_row_id",
    "base_refinement_path", "box", "coordinate_volume",
    "base_coordinate_area", "lower_t_face_status", "upper_t_face_status",
    "graph_classification", "two_dimensional_graph_sheet_count",
    "one_dimensional_clipping_curve_segment_count",
    "zero_dimensional_boundary_endpoint_incidence_count",
    "closed_3d_side_union_volume", "residual_3d_collar_volume",
]
R182_COLLAR_COLUMNS = [
    "row_id", "Round179_occurrence_row_id", "origin_row_id", "parent_id",
    "chart", "owner_target", "kind", "reason_label", "equation",
    "target_obstacle", "strict_t_derivative_sign",
    "Round179_origin_already_fully_replaced",
    "Round179_retained_child_count", "Round179_retained_coordinate_volume",
    "bounded_base_split_axis", "bounded_base_split_depth",
    "closed_leaf_count", "closed_coordinate_volume", "residual_leaf_count",
    "residual_coordinate_volume", "full_base_graph_leaf_count",
    "absent_graph_leaf_count", "clipped_graph_leaf_count",
    "two_dimensional_graph_sheet_count",
    "one_dimensional_clipping_curve_segment_count",
    "zero_dimensional_boundary_endpoint_incidence_count",
    "fully_clipped_over_Round179_retained_children", "leaf_rows_sha256",
    "whole_original_tube_credit", "global_exact_key_disposition_credit",
    "provenance",
]
R179_ORIGIN_COLUMNS = [
    "origin_row_id", "parent_id", "chart", "owner_target",
    "original_refinement_path", "original_box",
    "original_coordinate_volume", "original_reason_labels", "reason_count",
    "chosen_split_axis", "resolved_child_count",
    "resolved_child_coordinate_volume", "guard_child_count",
    "guard_child_coordinate_volume", "retained_child_count",
    "retained_child_coordinate_volume", "fully_replaced_by_bounded_children",
    "released_exact_key_count", "released_exact_key_ordinals_sha256",
    "provenance",
]
R179_RETAINED_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "child_index",
    "refinement_path", "box", "coordinate_volume", "reason_labels",
    "ambient_dimension", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
]
R179_OUTGOING_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "equation",
    "gradient_axis", "gradient_sign", "regularity_certification",
    "lower_t_face_sign", "upper_t_face_sign", "face_classification",
    "zero_set_dimension_account", "existence_over_full_base",
    "two_open_3d_sides_retained", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
]
R179_WALL_COLUMNS = [
    "row_id", "origin_row_id", "parent_id", "chart", "reason_label",
    "axis", "integer_wall", "zero_equation",
    "source_factor_classification", "source_gradient_axis",
    "source_gradient_sign", "target_factor_classification",
    "target_gradient_axis", "target_gradient_sign",
    "target_lower_face_sign", "target_upper_face_sign",
    "target_face_classification", "zero_set_dimension_account",
    "crossing_time_dependency_overwrap_discharged", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
]


def unpack_selected(
    path: Path,
    table: str,
    columns: list[str],
    id_field: str,
    wanted: set[str],
    *,
    after_marker: str | None = None,
) -> dict[str, dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    for packed in iter_array(path, table, after_marker=after_marker):
        need(
            type(packed) is list and len(packed) == len(columns),
            "PACKED_ROW_ARITY:" + table,
        )
        row = dict(zip(columns, packed, strict=True))
        row_id = row[id_field]
        if row_id not in wanted:
            continue
        need(row_id not in selected, "PACKED_ROW_UNIQUE:" + str(row_id))
        selected[str(row_id)] = row
    need(set(selected) == wanted, "PACKED_ROW_COVERAGE:" + table)
    return selected


def load_geometry(
    input_dir: Path,
    records: list[dict[str, Any]],
    r291: dict[str, dict[str, Any]],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    leaf_ids = {
        r291[record["r291_ids"][0]]["cells"][
            record["cell_indices"][0]
        ]["leaf_row_id"]
        for record in records
    }
    leaves = unpack_selected(
        input_dir / R182,
        "collar_leaf_rows",
        R182_LEAF_COLUMNS,
        "row_id",
        leaf_ids,
    )
    occurrence_ids = {row["occurrence_row_id"] for row in leaves.values()}
    collars = unpack_selected(
        input_dir / R182,
        "collar_occurrence_rows",
        R182_COLLAR_COLUMNS,
        "Round179_occurrence_row_id",
        occurrence_ids,
    )
    origin_ids = {row["origin_row_id"] for row in collars.values()}
    origins = unpack_selected(
        input_dir / R179,
        "origin_tube_rows",
        R179_ORIGIN_COLUMNS,
        "origin_row_id",
        origin_ids,
    )
    retained_ids = {
        row["retained_child_row_id"] for row in leaves.values()
    }
    retained = unpack_selected(
        input_dir / R179,
        "retained_3d_child_rows",
        R179_RETAINED_COLUMNS,
        "row_id",
        retained_ids,
    )
    outgoing_ids = {
        row_id
        for row_id, row in collars.items()
        if row["kind"] == "OUTGOING"
    }
    wall_ids = occurrence_ids - outgoing_ids
    outgoing = (
        unpack_selected(
            input_dir / R179,
            "outgoing_normal_form_rows",
            R179_OUTGOING_COLUMNS,
            "row_id",
            outgoing_ids,
        )
        if outgoing_ids
        else {}
    )
    walls = (
        unpack_selected(
            input_dir / R179,
            "wall_normal_form_rows",
            R179_WALL_COLUMNS,
            "row_id",
            wall_ids,
            after_marker='"table_census_and_sha256":{',
        )
        if wall_ids
        else {}
    )
    active = {**outgoing, **walls}
    need(set(active) == occurrence_ids, "ACTIVE_METADATA_COVERAGE")

    for record in records:
        local = r291[record["r291_ids"][0]]
        cell = local["cells"][record["cell_indices"][0]]
        leaf = leaves[cell["leaf_row_id"]]
        collar = collars[leaf["occurrence_row_id"]]
        origin = origins[collar["origin_row_id"]]
        child = retained[leaf["retained_child_row_id"]]
        need(
            leaf["box"] == cell["exact_box"]
            and leaf["base_coordinate_area"]
            == cell["base_coordinate_area"]
            and leaf["graph_classification"]
            == cell["graph_classification"]
            and leaf["retained_child_row_id"]
            == cell["retained_child_row_id"]
            and leaf["occurrence_row_id"]
            == local["row"]["canonical_support_row_id"]
            and collar["chart"] == local["row"]["source_chart"]
            and collar["equation"] == local["row"]["predicate_equation"]
            and origin["chart"] == collar["chart"]
            and origin["owner_target"] == collar["owner_target"]
            and child["origin_row_id"] == origin["origin_row_id"]
            and leaf["two_dimensional_graph_sheet_count"] == 1
            and Q(leaf["base_coordinate_area"]) > 0
            and Q(leaf["residual_3d_collar_volume"]) == 0
            and Q(leaf["closed_3d_side_union_volume"])
            == Q(leaf["coordinate_volume"]),
            "R179_R182_R291_LINEAGE:" + record["source_id"],
        )
        record["leaf_id"] = leaf["row_id"]
        record["occurrence_row_id"] = leaf["occurrence_row_id"]
        record["origin_row_id"] = collar["origin_row_id"]
        record["retained_child_row_id"] = leaf["retained_child_row_id"]
        record["collar_kind"] = collar["kind"]
        record["source_chart"] = collar["chart"]
        record["owner_target"] = collar["owner_target"]
        record["active_equation"] = collar["equation"]
    return leaves, collars, origins, active


def read_pinned_executable(
    path: Path,
    expected_sha256: str,
    label: str,
) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        info = os.fstat(descriptor)
        need(
            stat.S_ISREG(info.st_mode)
            and info.st_nlink == 1
            and info.st_size > 0,
            "EXECUTABLE_DESCRIPTOR:" + label,
        )
        source_parts: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            source_parts.append(block)
    finally:
        os.close(descriptor)
    source = b"".join(source_parts)
    need(
        len(source) == info.st_size
        and hashlib.sha256(source).hexdigest() == expected_sha256,
        "EXECUTABLE_DESCRIPTOR_PIN:" + label,
    )
    return source


def executable_local_imports(source: bytes, filename: str) -> set[str]:
    try:
        tree = ast.parse(source, filename=filename)
    except (SyntaxError, ValueError) as exc:
        raise VerificationError("EXECUTABLE_AST:" + filename) from exc
    output: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            need(node.level == 0, "EXECUTABLE_RELATIVE_IMPORT:" + filename)
            modules = [node.module] if node.module is not None else []
        else:
            if isinstance(node, ast.Call):
                function = node.func
                dynamic = (
                    isinstance(function, ast.Name)
                    and function.id == "__import__"
                ) or (
                    isinstance(function, ast.Attribute)
                    and function.attr == "import_module"
                )
                need(
                    not dynamic,
                    "EXECUTABLE_DYNAMIC_IMPORT:" + filename,
                )
            continue
        for module_name in modules:
            top = module_name.split(".", 1)[0]
            if top.startswith("cm2_"):
                output.add(top + ".py")
    return output


def verifier_pinned_executable_sources(
    input_dir: Path,
) -> dict[str, bytes]:
    sources = {
        name: read_pinned_executable(
            input_dir / name,
            expected,
            name,
        )
        for name, expected in EXECUTABLE_TRANSITIVE_CLOSURE_PINS.items()
    }
    actual_graph = {
        name: sorted(executable_local_imports(source, name))
        for name, source in sources.items()
    }
    need(
        actual_graph
        == {
            name: sorted(children)
            for name, children in EXECUTABLE_IMPORT_GRAPH.items()
        },
        "EXECUTABLE_RECURSIVE_IMPORT_GRAPH:"
        + json.dumps(actual_graph, sort_keys=True),
    )
    discovered = {R179_KERNEL}
    pending = [R179_KERNEL]
    while pending:
        current = pending.pop()
        for dependency in actual_graph[current]:
            if dependency not in discovered:
                discovered.add(dependency)
                pending.append(dependency)
    need(
        discovered == set(EXECUTABLE_TRANSITIVE_CLOSURE_PINS),
        "EXECUTABLE_TRANSITIVE_CLOSURE",
    )
    return sources


def verifier_execute_pinned_module(
    *,
    module_name: str,
    filename: str,
    source: bytes,
    input_dir: Path,
) -> Any:
    path = (input_dir / filename).resolve()
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[module_name] = module
    try:
        code = compile(source, str(path), "exec", dont_inherit=True)
        # The bytes were O_NOFOLLOW-read, SHA-closed, and AST-audited above.
        exec(code, module.__dict__)  # noqa: S102
    except BaseException:
        if sys.modules.get(module_name) is module:
            del sys.modules[module_name]
        raise
    need(
        sys.modules.get(module_name) is module
        and Path(module.__file__).resolve() == path,
        "EXECUTABLE_MODULE_IDENTITY:" + module_name,
    )
    return module


def import_kernel(input_dir: Path) -> Any:
    sources = verifier_pinned_executable_sources(input_dir)
    names = {
        filename: Path(filename).stem
        for filename in EXECUTABLE_TRANSITIVE_CLOSURE_PINS
    }
    root_name = "_r303b_verifier_pinned_round179_kernel"
    for module_name in [*names.values(), root_name]:
        sys.modules.pop(module_name, None)

    loaded: dict[str, Any] = {}
    for filename in EXECUTABLE_LOAD_ORDER:
        module_name = names[filename]
        loaded[filename] = verifier_execute_pinned_module(
            module_name=module_name,
            filename=filename,
            source=sources[filename],
            input_dir=input_dir,
        )
    module = verifier_execute_pinned_module(
        module_name=root_name,
        filename=R179_KERNEL,
        source=sources[R179_KERNEL],
        input_dir=input_dir,
    )
    for filename in EXECUTABLE_LOAD_ORDER:
        dependency = loaded[filename]
        module_name = names[filename]
        need(
            sys.modules.get(module_name) is dependency
            and Path(dependency.__file__).resolve()
            == (input_dir / filename).resolve(),
            "EXECUTABLE_DEPENDENCY_PATH:" + filename,
        )
    need(
        Path(module.__file__).resolve()
        == (input_dir / R179_KERNEL).resolve()
        and module.FLINT_VERSION == "0.9.0"
        and module.PRECISION_BITS == 256,
        "PINNED_INTERVAL_KERNEL_RUNTIME",
    )
    module.ctx.prec = module.PRECISION_BITS
    return module


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def box_values(box: Any) -> list[str]:
    return [
        qstr(box.t0), qstr(box.t1), qstr(box.p0),
        qstr(box.p1), qstr(box.s0), qstr(box.s1),
    ]


def volume(box: Any) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def base_area(box: Any) -> Q:
    return (box.p1 - box.p0) * (box.s1 - box.s0)


def contains(outer: Any, inner: Any) -> bool:
    return (
        outer.t0 <= inner.t0 <= inner.t1 <= outer.t1
        and outer.p0 <= inner.p0 <= inner.p1 <= outer.p1
        and outer.s0 <= inner.s0 <= inner.s1 <= outer.s1
    )


def rational_domain_margin(box: Any, axis: str) -> Q:
    need(axis in {"t", "p"}, "RADICAND_AXIS")
    bounds = (
        (box.t0, box.t1) if axis == "t" else (box.p0, box.p1)
    )
    return 1 - max(abs(bounds[0]), abs(bounds[1])) ** 2


def active_dual(
    kernel: Any,
    origin: dict[str, Any],
    kind: str,
    metadata: dict[str, Any],
    box: Any,
) -> tuple[Any, tuple[Any, ...]]:
    geometry = kernel.interval_geometry(
        origin["chart"], origin["owner_target"], box
    )
    if kind == "OUTGOING":
        return geometry["outgoing_equality"]
    need(kind == "WALL", "ACTIVE_KIND")
    target = "hit_x" if metadata["axis"] == "X" else "hit_y"
    return kernel.subtract_wall(
        geometry[target], metadata["integer_wall"]
    )


def inactive_wall_dual(
    kernel: Any,
    origin: dict[str, Any],
    metadata: dict[str, Any],
    box: Any,
) -> tuple[Any, tuple[Any, ...]]:
    geometry = kernel.interval_geometry(
        origin["chart"], origin["owner_target"], box
    )
    source = "source_x" if metadata["axis"] == "X" else "source_y"
    return kernel.subtract_wall(
        geometry[source], metadata["integer_wall"]
    )


def split_base(kernel: Any, box: Any, axis: str, bit: int) -> Any:
    need(axis in {"p", "s"} and bit in {0, 1}, "BASE_SPLIT")
    if axis == "p":
        middle = (box.p0 + box.p1) / 2
        values = (
            (box.t0, box.t1, box.p0, middle, box.s0, box.s1)
            if bit == 0
            else (box.t0, box.t1, middle, box.p1, box.s0, box.s1)
        )
    else:
        middle = (box.s0 + box.s1) / 2
        values = (
            (box.t0, box.t1, box.p0, box.p1, box.s0, middle)
            if bit == 0
            else (box.t0, box.t1, box.p0, box.p1, middle, box.s1)
        )
    return kernel.r174.atlas.AtlasBox(
        *values, box.depth + 1, f"{box.path}:{axis}{bit}"
    )


def t_subbox(
    kernel: Any,
    box: Any,
    lower: Q,
    upper: Q,
    label: str,
) -> Any:
    return kernel.r174.atlas.AtlasBox(
        lower,
        upper,
        box.p0,
        box.p1,
        box.s0,
        box.s1,
        box.depth + 1,
        f"{box.path}:{label}",
    )


def active_face_signs(
    kernel: Any,
    origin: dict[str, Any],
    kind: str,
    metadata: dict[str, Any],
    box: Any,
) -> tuple[str, str]:
    lower = kernel.fixed_axis_face(box, "t", False)
    upper = kernel.fixed_axis_face(box, "t", True)
    return (
        kernel.sign(active_dual(kernel, origin, kind, metadata, lower)[0]),
        kernel.sign(active_dual(kernel, origin, kind, metadata, upper)[0]),
    )


def independent_round182_face_status(
    kernel: Any,
    origin: dict[str, Any],
    metadata: dict[str, Any],
    box: Any,
    upper: bool,
) -> dict[str, Any]:
    """Recompute one Round182 face status without importing Round182."""

    face = kernel.fixed_axis_face(box, "t", upper)
    value = active_dual(kernel, origin, "WALL", metadata, face)
    direct_sign = kernel.sign(value[0])
    if direct_sign in STRICT_SIGNS:
        return {
            "kind": "STRICT",
            "raw_interval_sign": direct_sign,
            "resolved_sign": direct_sign,
            "axis": None,
            "derivative_sign": None,
            "axis_lower_sign": None,
            "axis_upper_sign": None,
            "newton_interior": None,
        }

    absence_certificates: list[dict[str, Any]] = []
    curve_certificates: list[dict[str, Any]] = []
    for axis in ("p", "s"):
        axis_index = "tps".index(axis)
        derivative = value[1][axis_index]
        if derivative is None:
            continue
        derivative_sign = kernel.sign(derivative)
        if derivative_sign not in STRICT_SIGNS:
            continue
        lower_face = kernel.fixed_axis_face(face, axis, False)
        upper_face = kernel.fixed_axis_face(face, axis, True)
        lower_sign = kernel.sign(
            active_dual(
                kernel, origin, "WALL", metadata, lower_face
            )[0]
        )
        upper_sign = kernel.sign(
            active_dual(
                kernel, origin, "WALL", metadata, upper_face
            )[0]
        )
        classification = kernel.face_classification(
            active_dual(
                kernel, origin, "WALL", metadata, lower_face
            )[0],
            active_dual(
                kernel, origin, "WALL", metadata, upper_face
            )[0],
        )
        if classification not in {
            "FULL_BASE_UNIQUE_GRAPH",
            "STRICT_ZERO_ABSENT",
        }:
            continue
        is_curve = classification == "FULL_BASE_UNIQUE_GRAPH"
        if not is_curve:
            need(
                lower_sign == upper_sign
                and lower_sign in STRICT_SIGNS,
                "ROUND182_ABSENT_FACE_ENDPOINT_SIGNS",
            )
        record = {
            "kind": "CURVE" if is_curve else "ABSENT",
            "raw_interval_sign": direct_sign,
            "resolved_sign": None if is_curve else lower_sign,
            "axis": axis,
            "derivative_sign": derivative_sign,
            "axis_lower_sign": lower_sign,
            "axis_upper_sign": upper_sign,
            "newton_interior": None,
        }
        (curve_certificates if is_curve else absence_certificates).append(
            record
        )
    need(
        not (curve_certificates and absence_certificates),
        "ROUND182_CONFLICTING_FACE_NORMAL_FORMS",
    )
    if curve_certificates:
        return curve_certificates[0]
    if absence_certificates:
        return absence_certificates[0]
    return {
        "kind": "UNRESOLVED",
        "raw_interval_sign": direct_sign,
        "resolved_sign": None,
        "axis": None,
        "derivative_sign": None,
        "axis_lower_sign": None,
        "axis_upper_sign": None,
        "newton_interior": None,
    }


def independent_encode_round182_face_status(
    status: dict[str, Any],
) -> str:
    signs = {
        "STRICT_NEGATIVE": "-",
        "STRICT_POSITIVE": "+",
        None: "_",
    }
    if status["kind"] == "STRICT":
        return "S" + signs[status["resolved_sign"]]
    if status["kind"] == "UNRESOLVED":
        return "U"
    need(
        status["kind"] in {"CURVE", "ABSENT"},
        "ROUND182_FACE_STATUS_KIND",
    )
    return "".join([
        "C" if status["kind"] == "CURVE" else "A",
        status["axis"],
        signs[status["derivative_sign"]],
        signs[status["axis_lower_sign"]],
        signs[status["axis_upper_sign"]],
        signs[status["resolved_sign"]],
        (
            "1" if status["newton_interior"] is True
            else "0" if status["newton_interior"] is False
            else "_"
        ),
    ])


def independent_compact_round182_face_status(
    status: dict[str, Any],
) -> dict[str, Any]:
    fields = (
        "kind",
        "raw_interval_sign",
        "resolved_sign",
        "axis",
        "derivative_sign",
        "axis_lower_sign",
        "axis_upper_sign",
        "newton_interior",
    )
    return {field: status[field] for field in fields}


def base_schedule(
    kernel: Any,
    origin: dict[str, Any],
    kind: str,
    metadata: dict[str, Any],
    root: Any,
) -> tuple[str, ...]:
    strict_axes = kernel.strict_derivative_axes(
        active_dual(kernel, origin, kind, metadata, root)
    )
    axes = [axis for axis in ("p", "s") if axis in strict_axes]
    if kind == "OUTGOING" and origin["owner_target"].startswith("W["):
        axes.sort(key=lambda axis: 0 if axis == "s" else 1)
    return tuple(axes or ["p", "s"])


def find_graph_prism(
    kernel: Any,
    origin: dict[str, Any],
    kind: str,
    metadata: dict[str, Any],
    root: Any,
) -> dict[str, Any]:
    schedule = base_schedule(kernel, origin, kind, metadata, root)
    queue = deque([(root, 0, "")])
    visited = 0
    while queue:
        candidate, depth, path = queue.popleft()
        visited += 1
        lower, upper = active_face_signs(
            kernel, origin, kind, metadata, candidate
        )
        if {lower, upper} == STRICT_SIGNS:
            need(base_area(candidate) > 0, "POSITIVE_GRAPH_BASE")
            return {
                "box": candidate,
                "split_depth": depth,
                "split_path": path,
                "schedule": schedule,
                "lower_sign": lower,
                "upper_sign": upper,
                "visited": visited,
            }
        if lower == upper and lower in STRICT_SIGNS:
            continue
        if depth == MAX_BASE_SPLIT_DEPTH:
            continue
        axis = schedule[depth % len(schedule)]
        for bit in (0, 1):
            queue.append((
                split_base(kernel, candidate, axis, bit),
                depth + 1,
                path + axis + str(bit),
            ))
    raise VerificationError("NO_POSITIVE_BASE_GRAPH_PRISM")


def find_corridor(
    kernel: Any,
    origin: dict[str, Any],
    kind: str,
    metadata: dict[str, Any],
    graph_box: Any,
    side: str,
    expected_sign: str,
) -> tuple[Any, int]:
    need(side in {"LOWER", "UPPER"}, "CORRIDOR_SIDE")
    width = graph_box.t1 - graph_box.t0
    for depth in range(2, MAX_CORRIDOR_DYADIC_DEPTH + 1):
        lane = width / (2 ** depth)
        lower, upper = (
            (graph_box.t0, graph_box.t0 + lane)
            if side == "LOWER"
            else (graph_box.t1 - lane, graph_box.t1)
        )
        candidate = t_subbox(
            kernel,
            graph_box,
            lower,
            upper,
            side.lower() + f"-corridor-{depth}",
        )
        sign = kernel.sign(
            active_dual(kernel, origin, kind, metadata, candidate)[0]
        )
        if sign == expected_sign:
            need(volume(candidate) > 0, "POSITIVE_CORRIDOR")
            return candidate, depth
    raise VerificationError("CORRIDOR_SEARCH_CAP:" + side)


def source_refs(
    record: dict[str, Any],
    r295: dict[str, dict[str, Any]],
    r293: dict[str, dict[str, Any]],
    r291: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    row295 = r295[record["r295_ids"][0]]
    row293 = r293[
        row295["source_Round293_R291_physical_witness_binding_row_id"]
    ]
    local = r291[record["r291_ids"][0]]
    cell = local["cells"][record["cell_indices"][0]]
    return {
        "Round291": {
            "row_id": local["row"][
                "complete_lower_stratum_local_disposition_row_id"
            ],
            "row_sha256": local["row"]["row_sha256"],
            "physical_witness_cell_index": record["cell_indices"][0],
            "physical_witness_cell": cell,
        },
        "Round293": {
            "row_id": row293[
                "Round292_R291_physical_witness_binding_row_id"
            ],
            "row_sha256": row293["row_sha256"],
            "binding_classification": row293["binding_classification"],
        },
        "Round295A": {
            "row_id": row295[
                "Round295A_R291_physical_incidence_binding_row_id"
            ],
            "row_sha256": row295["row_sha256"],
            "binding_classification":
                row295["Round295A_binding_classification"],
        },
    }


def load_r204_full_2d_lineage(
    input_dir: Path,
    records: list[dict[str, Any]],
    r294: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    wanted_regions = {
        endpoint for record in records for endpoint in record["pair"]
    }
    document = read_json(input_dir / R204)
    need(
        document.get("schema")
        == "cm2.round204.source-g-wall-return-signature-local-replacement.v1"
        and document.get("result_sha256") == digest(document["result"]),
        "R204_CERTIFICATE_ENVELOPE",
    )
    result = document["result"]
    region_ledger = result["formal_local_open_3D_region_ledger"]
    sheet_ledger = result["formal_2D_sheet_lineage"]
    all_regions = region_ledger["rows"]
    all_sheets = sheet_ledger["target_sheet_rows"]
    need(
        region_ledger["row_count"] == len(all_regions) == 736
        and region_ledger["rows_sha256"] == digest(all_regions)
        and sheet_ledger["target_sheet_row_count"] == len(all_sheets) == 224
        and sheet_ledger["target_sheet_rows_sha256"] == digest(all_sheets),
        "R204_EMBEDDED_LEDGER_COMMITMENTS",
    )
    certification_census = Counter(
        row.get("existence_certification") for row in all_sheets
    )
    need(
        certification_census
        == Counter({
            FULL_2D_CERT: EXPECTED_R204_FULL_2D,
            TAIL_CERT: EXPECTED_R204_TAIL,
        }),
        "R204_EXACT_FULL2D_TAIL_PARTITION",
    )

    regions: dict[str, dict[str, Any]] = {}
    for row in all_regions:
        endpoint = row["region_row_id"]
        if endpoint not in wanted_regions:
            continue
        verify_row(row, endpoint)
        registry = r294[endpoint]
        need(
            endpoint not in regions
            and registry["registry_entry_kind"] == PRESERVED_KIND
            and registry["source_occurrence_round"] == 266
            and registry["source_geometry_row_id"] == endpoint
            and registry["source_geometry_row_sha256"]
            == row["row_sha256"]
            and registry["support_geometry_status"]
            == "RECONSTRUCT_FROM_PINNED_SOURCE_GEOMETRY_ROW"
            and row["ambient_dimension"] == 3
            and row["strict_open_region"] is True
            and row["positive_coordinate_volume"] is True
            and row["target_graph_sheet_incident"] is True
            and row["tail_region"] is False
            and row["graph_classification"] == "FULL_2D"
            and row["target_factor_sign"] in {"NEGATIVE", "POSITIVE"}
            and row["formal_local_signature_credit"] == 1
            and row["missing_signature_field_count"] == 0
            and row["conflicting_signature_count"] == 0,
            "R204_FULL2D_REGION:" + endpoint,
        )
        regions[endpoint] = row
    need(set(regions) == wanted_regions, "R204_REGION_COVERAGE")

    sheets_by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    for row in all_sheets:
        pair = tuple(sorted([
            row["negative_side_region_row_id"],
            row["positive_side_region_row_id"],
        ]))
        if not set(pair) <= wanted_regions:
            continue
        verify_row(row, row["sheet_row_id"])
        need(
            pair not in sheets_by_pair
            and row["ambient_dimension"] == 2
            and row["sheet_kind"] == "TARGET_REGULAR_GRAPH_SHEET_CELL"
            and row["local_dimension_lineage_materialized"] is True
            and row["target_factor_graph_axis"] == "t"
            and row["target_t_derivative_sign"] in STRICT_SIGNS
            and row["existence_certification"] == FULL_2D_CERT
            and row["existence_certification"] != TAIL_CERT
            and row["source_sign_on_leaf"] in {"NEGATIVE", "POSITIVE"}
            and Q(row["base_p_s_exact_bounds"][1])
            > Q(row["base_p_s_exact_bounds"][0])
            and Q(row["base_p_s_exact_bounds"][3])
            > Q(row["base_p_s_exact_bounds"][2])
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0,
            "R204_FULL2D_SHEET:" + row["sheet_row_id"],
        )
        sheets_by_pair[pair] = row
    need(
        len(sheets_by_pair) == EXPECTED_B2,
        "R204_SELECTED_FULL2D_SHEET_CENSUS",
    )

    output: dict[str, dict[str, Any]] = {}
    for record in records:
        pair = record["pair"]
        need(pair in sheets_by_pair, "R300D_R204_FULL2D_PAIR")
        sheet = sheets_by_pair[pair]
        negative = regions[sheet["negative_side_region_row_id"]]
        positive = regions[sheet["positive_side_region_row_id"]]
        need(
            negative["target_factor_sign"] == "NEGATIVE"
            and positive["target_factor_sign"] == "POSITIVE"
            and negative["target_sheet_row_id"]
            == positive["target_sheet_row_id"]
            == sheet["sheet_row_id"]
            and negative["leaf_row_id"]
            == positive["leaf_row_id"]
            == sheet["leaf_row_id"]
            and negative["chart"] == positive["chart"] == sheet["chart"]
            and negative["owner_target"]
            == positive["owner_target"]
            == sheet["owner_target"]
            and negative["leaf_exact_box"]
            == positive["leaf_exact_box"]
            == [
                *sheet["leaf_t_exact_bounds"],
                *sheet["base_p_s_exact_bounds"],
            ],
            "R204_NEGATIVE_SHEET_POSITIVE_JOIN:" + record["source_id"],
        )
        output[record["source_id"]] = {
            "sheet": sheet,
            "negative": negative,
            "positive": positive,
        }
    need(len(output) == EXPECTED_B2, "R204_FULL2D_OUTPUT_CENSUS")
    return output


def r204_selector_self_test(input_dir: Path) -> dict[str, Any]:
    document = read_json(input_dir / R204)
    sheets = document["result"]["formal_2D_sheet_lineage"][
        "target_sheet_rows"
    ]
    census = Counter(row["existence_certification"] for row in sheets)
    need(
        census[FULL_2D_CERT] == EXPECTED_R204_FULL_2D,
        "SELF_TEST_FULL2D_CENSUS",
    )
    need(
        census[TAIL_CERT] == EXPECTED_R204_TAIL,
        "SELF_TEST_TAIL_CENSUS",
    )
    accepted = [
        row for row in sheets
        if row["existence_certification"] == FULL_2D_CERT
    ]
    need(
        all(row["existence_certification"] != TAIL_CERT for row in accepted),
        "SELF_TEST_TAIL_REJECTION",
    )
    return {
        "FULL_2D_selected": len(accepted),
        "tail_rejected": census[TAIL_CERT],
        "selector": FULL_2D_CERT,
        "forbidden_selector": TAIL_CERT,
    }


def build_b1_row(
    *,
    record: dict[str, Any],
    r294: dict[str, dict[str, Any]],
    r295: dict[str, dict[str, Any]],
    r293: dict[str, dict[str, Any]],
    r291: dict[str, dict[str, Any]],
    leaves: dict[str, dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    origins: dict[str, dict[str, Any]],
    active: dict[str, dict[str, Any]],
    kernel: Any,
) -> dict[str, Any]:
    local = r291[record["r291_ids"][0]]
    cell = local["cells"][record["cell_indices"][0]]
    leaf = leaves[record["leaf_id"]]
    origin = origins[record["origin_row_id"]]
    metadata = active[record["occurrence_row_id"]]
    root = kernel.box_from(
        cell["exact_box"],
        len(leaf["base_refinement_path"]),
        cell["leaf_row_id"],
    )
    scalar = active_dual(
        kernel, origin, record["collar_kind"], metadata, root
    )
    derivative_sign = kernel.sign(scalar[1][0])
    need(
        derivative_sign in STRICT_SIGNS,
        "B1_STRICT_T_DERIVATIVE:" + record["source_id"],
    )
    graph = find_graph_prism(
        kernel, origin, record["collar_kind"], metadata, root
    )
    graph_box = graph["box"]
    graph_dual = active_dual(
        kernel, origin, record["collar_kind"], metadata, graph_box
    )
    derivative_enclosure = graph_dual[1][0]
    need(
        kernel.sign(derivative_enclosure) == derivative_sign,
        "B1_DERIVATIVE_RESTRICTION:" + record["source_id"],
    )
    lower_face = kernel.fixed_axis_face(graph_box, "t", False)
    upper_face = kernel.fixed_axis_face(graph_box, "t", True)
    lower_enclosure = active_dual(
        kernel, origin, record["collar_kind"], metadata, lower_face
    )[0]
    upper_enclosure = active_dual(
        kernel, origin, record["collar_kind"], metadata, upper_face
    )[0]
    expected_faces = (
        ("STRICT_NEGATIVE", "STRICT_POSITIVE")
        if derivative_sign == "STRICT_POSITIVE"
        else ("STRICT_POSITIVE", "STRICT_NEGATIVE")
    )
    need(
        (graph["lower_sign"], graph["upper_sign"]) == expected_faces,
        "B1_ORIENTED_FACE_BRACKET:" + record["source_id"],
    )
    t_margin = rational_domain_margin(graph_box, "t")
    p_margin = rational_domain_margin(graph_box, "p")
    need(
        t_margin > 0 and p_margin > 0,
        "B1_STRICT_RADICAND_MARGINS:" + record["source_id"],
    )
    lower_corridor, lower_depth = find_corridor(
        kernel,
        origin,
        record["collar_kind"],
        metadata,
        graph_box,
        "LOWER",
        graph["lower_sign"],
    )
    upper_corridor, upper_depth = find_corridor(
        kernel,
        origin,
        record["collar_kind"],
        metadata,
        graph_box,
        "UPPER",
        graph["upper_sign"],
    )
    need(
        lower_corridor.t1 < upper_corridor.t0
        and volume(lower_corridor) > 0
        and volume(upper_corridor) > 0,
        "B1_DISJOINT_POSITIVE_CORRIDORS:" + record["source_id"],
    )

    round272 = any(
        bridge["connected_source_side_witness"][
            "connected_contract"
        ].startswith("ROUND272_")
        for bridge in record["bridge_refs"].values()
    )
    inactive_source_factor: dict[str, Any] | None = None
    if record["collar_kind"] == "WALL":
        source_sign = kernel.sign(
            inactive_wall_dual(kernel, origin, metadata, root)[0]
        )
        checked_root = root
        domain = "CLOSED_R291_PHYSICAL_LEAF"
        if source_sign not in STRICT_SIGNS:
            need(
                round272 and ((root.t0 == 0) + (root.t1 == 0)) == 1,
                "B1_ROUND272_ONLY_ZERO_FACE",
            )
            middle = (root.t0 + root.t1) / 2
            checked_root = t_subbox(
                kernel,
                root,
                middle if root.t0 == 0 else root.t0,
                root.t1 if root.t0 == 0 else middle,
                "round272-relative-open-source-check",
            )
            source_sign = kernel.sign(
                inactive_wall_dual(
                    kernel, origin, metadata, checked_root
                )[0]
            )
            domain = (
                "ROUND272_RELATIVE_OPEN_INTERIOR__EXCLUDED_t_EQUALS_0_FACE"
            )
        need(source_sign in STRICT_SIGNS, "B1_INACTIVE_SOURCE_STRICT")
        corridor_checks: list[dict[str, Any]] = []
        for corridor in (lower_corridor, upper_corridor):
            checked = corridor
            sign = kernel.sign(
                inactive_wall_dual(kernel, origin, metadata, checked)[0]
            )
            check_domain = "CLOSED_CORRIDOR"
            if sign != source_sign and round272:
                need(
                    ((corridor.t0 == 0) + (corridor.t1 == 0)) == 1,
                    "B1_ROUND272_CORRIDOR_ZERO_FACE",
                )
                middle = (corridor.t0 + corridor.t1) / 2
                checked = t_subbox(
                    kernel,
                    corridor,
                    middle if corridor.t0 == 0 else corridor.t0,
                    corridor.t1 if corridor.t0 == 0 else middle,
                    "round272-relative-open-corridor-check",
                )
                sign = kernel.sign(
                    inactive_wall_dual(
                        kernel, origin, metadata, checked
                    )[0]
                )
                check_domain = "RELATIVE_OPEN_POSITIVE_VOLUME_SUBBOX"
            need(sign == source_sign, "B1_CORRIDOR_INACTIVE_SOURCE")
            corridor_checks.append({
                "checked_box": box_values(checked),
                "domain": check_domain,
                "strict_sign": sign,
            })
        inactive_source_factor = {
            "root_checked_box": box_values(checked_root),
            "domain": domain,
            "strict_sign": source_sign,
            "corridor_checks": corridor_checks,
        }

    endpoint_rows: list[dict[str, Any]] = []
    matched_sides: set[str] = set()
    normalized_contracts: list[str] = []
    for endpoint in record["pair"]:
        bridge = record["bridge_refs"][endpoint]
        registry = r294[endpoint]
        member_ref = record["member_refs"][endpoint]
        connected = bridge["connected_source_side_witness"]
        contract = connected["connected_contract"]
        sign = bridge["active_factor_strict_sign"]
        leaf_ref = bridge["Round182_leaf_reference"]
        active_ref = bridge["Round179_active_geometry_reference"]
        need(
            bridge["Round294_registry_reference"][
                "Round294_occurrence_registry_row_id"
            ] == registry["Round294_occurrence_registry_row_id"]
            and bridge["Round294_registry_reference"]["row_sha256"]
            == registry["row_sha256"]
            and bridge["Round301_member_row"]["row_id"]
            == member_ref["row_id"]
            and bridge["Round301_member_row"]["row_sha256"]
            == member_ref["row_sha256"]
            and bridge["Round301_member_row"]["component_id"]
            == member_ref["component_id"]
            and leaf_ref["Round182_leaf_row_id"] == record["leaf_id"]
            and leaf_ref["exact_leaf_box"] == leaf["box"]
            and active_ref["Round179_active_normal_form_row_id"]
            == record["occurrence_row_id"]
            and active_ref["Round179_origin_row_id"]
            == record["origin_row_id"]
            and active_ref["source_chart"] == record["source_chart"]
            and active_ref["owner_target"] == record["owner_target"]
            and bridge["active_factor_equation"]
            == record["active_equation"]
            and connected[
                "formal_connected_source_signed_region_definition"
            ] == normalized_A_definition(contract, sign)
            and (
                connected["relative_open_excluded_face"] == "t=0"
                if contract.startswith("ROUND272_")
                else connected["relative_open_excluded_face"] is None
            )
            and all(
                reference["connected_contract"] == contract
                and reference["active_factor_strict_sign"] == sign
                and reference[
                    "connected_side_extension_materialized"
                ] is True
                and reference[
                    "formal_connected_source_signed_region_id"
                ] == connected["formal_connected_source_signed_region_id"]
                for reference in bridge["source_side_row_references"]
            ),
            "B1_ENDPOINT_PROVENANCE:" + endpoint,
        )
        anchor = kernel.box_from(
            bridge["anchor_box"], 0, "Round303A-anchor:" + endpoint
        )
        need(
            volume(anchor) > 0
            and contains(root, anchor)
            and kernel.sign(
                active_dual(
                    kernel,
                    origin,
                    record["collar_kind"],
                    metadata,
                    anchor,
                )[0]
            ) == sign,
            "B1_ANCHOR_INTERVAL_REPLAY:" + endpoint,
        )
        matched = (
            "LOWER_GRAPH_SIDE"
            if sign == graph["lower_sign"]
            else "UPPER_GRAPH_SIDE"
            if sign == graph["upper_sign"]
            else "NO_MATCH"
        )
        need(matched != "NO_MATCH", "B1_ENDPOINT_GRAPH_SIDE:" + endpoint)
        matched_sides.add(matched)
        normalized_contracts.append(contract)
        endpoint_rows.append({
            "registry_occurrence_id": endpoint,
            "Round294_registry_row_id":
                registry["Round294_occurrence_registry_row_id"],
            "Round294_registry_row_sha256": registry["row_sha256"],
            "Round301_member_reference": member_ref,
            "Round303A_bridge_row_id": bridge["row_id"],
            "Round303A_bridge_row_sha256": bridge["row_sha256"],
            "Round303A_theorem_id": bridge["theorem_id"],
            "Round303A_theorem_sha256": bridge["theorem_sha256"],
            "strict_anchor_box": bridge["anchor_box"],
            "active_factor_strict_sign": sign,
            "normalized_A_contract": contract,
            "normalized_A_definition":
                normalized_A_definition(contract, sign),
            "connected_source_side_witness": connected,
            "matched_graph_side": matched,
            "local_graph_sign_side_subset_normalized_A": True,
            "closure_attachment_to_Gamma": {
                "theorem_id": LIMIT_THEOREM_ID,
                "theorem_sha256": MONOTONE_LIMIT_THEOREM_SHA256,
                "Gamma_subset_closure_of_this_local_sign_side": True,
                "local_sign_side_subset_normalized_A": True,
                "therefore_Gamma_subset_closure_of_normalized_A": True,
            },
        })
    need(
        matched_sides == {"LOWER_GRAPH_SIDE", "UPPER_GRAPH_SIDE"},
        "B1_TWO_OPPOSITE_GRAPH_SIDES:" + record["source_id"],
    )
    if round272:
        need(
            all(
                contract.startswith("ROUND272_")
                for contract in normalized_contracts
            )
            and ((root.t0 == 0) + (root.t1 == 0)) == 1,
            "B1_ROUND272_RELATIVE_DOMAIN",
        )
        excluded_face_sign = (
            graph["lower_sign"]
            if graph_box.t0 == 0
            else graph["upper_sign"]
        )
        need(
            excluded_face_sign in STRICT_SIGNS,
            "B1_ROUND272_GAMMA_MISSES_T0",
        )
    else:
        excluded_face_sign = None

    payload = {
        "schema": SCHEMA + ".b1-lemma-row.v1",
        "proof_path": "B1_MONOTONE_GRAPH_TWO_CONNECTED_SIDE_ATTACHMENTS",
        "theorem_id": B1_THEOREM_ID,
        "theorem_sha256": B1_LAYER_THEOREM_SHA256,
        "gluing_theorem_id": THEOREM_ID,
        "gluing_theorem_sha256": THEOREM_SHA256,
        "monotone_limit_theorem": MONOTONE_LIMIT_THEOREM,
        "monotone_limit_theorem_sha256":
            MONOTONE_LIMIT_THEOREM_SHA256,
        "source_Round300D_row_id": record["source_id"],
        "source_Round300D_row_sha256": record["source_sha256"],
        "source_Round301_ineligible_reference":
            record["r301_ineligible_ref"],
        "canonical_endpoint_pair": list(record["pair"]),
        "endpoint_connected_side_rows": endpoint_rows,
        "physical_inclusion_chain": source_refs(
            record, r295, r293, r291
        ),
        "Gamma": {
            "kind":
                "UNIQUE_MONOTONE_TARGET_GRAPH_OVER_POSITIVE_RATIONAL_BASE",
            "exact_active_scalar_equation": record["active_equation"],
            "Round182_leaf_row_id": record["leaf_id"],
            "root_physical_leaf_box": box_values(root),
            "positive_base_graph_prism": box_values(graph_box),
            "exact_positive_base_area": qstr(base_area(graph_box)),
            "base_split_schedule": list(graph["schedule"]),
            "base_split_path": graph["split_path"],
            "base_split_depth": graph["split_depth"],
            "strict_t_derivative_sign": derivative_sign,
            "strict_t_derivative_enclosure": str(derivative_enclosure),
            "lower_face_active_sign": graph["lower_sign"],
            "lower_face_active_enclosure": str(lower_enclosure),
            "upper_face_active_sign": graph["upper_sign"],
            "upper_face_active_enclosure": str(upper_enclosure),
            "exact_chart_radicand_margins": {
                "one_minus_t_squared_margin": qstr(t_margin),
                "one_minus_p_squared_margin": qstr(p_margin),
                "both_strictly_positive": True,
            },
            "active_scalar_continuous_on_D": True,
            "unique_zero_graph_by_strict_monotonicity_and_IVT": True,
            "connected": True,
            "nonempty": True,
            "included_by_R291_R293_R295A_physical_chain": True,
            "Round272_excluded_t0_face_active_sign":
                excluded_face_sign,
            "Round272_Gamma_misses_excluded_t0_face":
                True if round272 else None,
            "relative_domain": (
                "ROUND272_RELATIVE_OPEN_LEAF_EXCLUDING_t=0"
                if round272
                else "CLOSED_EXACT_GRAPH_PRISM"
            ),
        },
        "local_side_nonempty_witnesses": {
            "lower_graph_facing_corridor_box":
                box_values(lower_corridor),
            "lower_corridor_dyadic_depth": lower_depth,
            "lower_corridor_active_sign": graph["lower_sign"],
            "upper_graph_facing_corridor_box":
                box_values(upper_corridor),
            "upper_corridor_dyadic_depth": upper_depth,
            "upper_corridor_active_sign": graph["upper_sign"],
            "both_positive_volume": True,
            "corridor_intersects_Gamma_claimed": False,
            "corridor_used_as_attachment_witness": False,
        },
        "two_sided_limit_attachment": {
            "left_local_sign_side_subset_normalized_A": True,
            "right_local_sign_side_subset_normalized_A": True,
            "Gamma_subset_closure_of_left_local_sign_side": True,
            "Gamma_subset_closure_of_right_local_sign_side": True,
            "Gamma_subset_closure_of_both_normalized_A_sides": True,
            "proof_source": LIMIT_THEOREM_ID,
            "corridor_box_closure_meets_Gamma": False,
        },
        "inactive_wall_source_factor_replay": inactive_source_factor,
        "B1_predicates": {
            "B1_P0_exact_scope_and_physical_binding_join": True,
            "B1_P1_two_complete_connected_A_bridges": True,
            "B1_P2_exact_chart_and_inactive_factor_domain": True,
            "B1_P3_positive_base_strict_monotone_bracket": True,
            "B1_P4_Gamma_same_included_R291_sheet_patch": True,
            "B1_P5_left_local_side_subset_A_and_limit_attachment": True,
            "B1_P6_right_local_side_subset_A_and_limit_attachment": True,
            "B1_P7_endpoint_patch_provenance_exactly_closed": True,
        },
        "limit_theorem_predicates": {
            "L0_exact_relative_domain": True,
            "L1_continuous_active_scalar": True,
            "L2_strict_t_monotonicity": True,
            "L3_uniform_opposite_face_signs": True,
            "L4_exact_included_Gamma_binding": True,
            "L5_complete_connected_sign_sides": True,
            "L6_endpoint_opposite_sign_bijection": True,
        },
        "G0_exact_provenance_pins_and_row_closures": True,
        "G1_endpoint_occurrence_connected_supports": True,
        "G2_nonempty_connected_included_lower_stratum": True,
        "G3_left_closure_attaches_to_included_patch": True,
        "G4_right_closure_attaches_to_included_patch": True,
        "G5_endpoint_patch_provenance_exactly_closed": True,
        "candidate_B1_lemma_conclusion": True,
        "formal_B1_attachment_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        **{field: 0 for field in ZERO_FIELDS},
    }
    return close_row("b1", payload)


def independent_b2_exact_join_payloads(
    *,
    record: dict[str, Any],
    lineage: dict[str, Any],
    r291: dict[str, dict[str, Any]],
    leaves: dict[str, dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    origins: dict[str, dict[str, Any]],
    active: dict[str, dict[str, Any]],
    kernel: Any,
) -> tuple[dict[str, Any], dict[str, Any]]:
    sheet = lineage["sheet"]
    negative = lineage["negative"]
    positive = lineage["positive"]
    local = r291[record["r291_ids"][0]]
    cell_index = record["cell_indices"][0]
    cell = local["cells"][cell_index]
    leaf = leaves[cell["leaf_row_id"]]
    collar = collars[leaf["occurrence_row_id"]]
    origin = origins[collar["origin_row_id"]]
    active_row = active[leaf["occurrence_row_id"]]
    exact_box = [
        *sheet["leaf_t_exact_bounds"],
        *sheet["base_p_s_exact_bounds"],
    ]
    exact_base_area = (
        (
            Q(sheet["base_p_s_exact_bounds"][1])
            - Q(sheet["base_p_s_exact_bounds"][0])
        )
        * (
            Q(sheet["base_p_s_exact_bounds"][3])
            - Q(sheet["base_p_s_exact_bounds"][2])
        )
    )
    axis = sheet["wall_axis"]
    wall = sheet["integer_wall"]
    coordinate = axis.lower()
    source_scalar = f"source_{coordinate}-{wall}"
    target_scalar = f"target_{coordinate}-{wall}"
    source_factor_equation = f"({source_scalar})=0"
    target_factor_equation = f"({target_scalar})=0"
    product_equation = f"({source_scalar})*({target_scalar})=0"
    selector_coordinate = "hit_x" if axis == "X" else "hit_y"
    target_selector_scalar = f"{selector_coordinate}-{wall}"
    root = kernel.box_from(
        exact_box,
        len(leaf["base_refinement_path"]),
        leaf["row_id"],
    )
    selector_dual = active_dual(
        kernel, origin, "WALL", active_row, root
    )
    replayed_derivative_sign = kernel.sign(selector_dual[1][0])
    lower_face_status = independent_round182_face_status(
        kernel, origin, active_row, root, False
    )
    upper_face_status = independent_round182_face_status(
        kernel, origin, active_row, root, True
    )
    replayed_face_statuses = (
        independent_encode_round182_face_status(lower_face_status),
        independent_encode_round182_face_status(upper_face_status),
    )
    raw_face_interval_signs = (
        lower_face_status["raw_interval_sign"],
        upper_face_status["raw_interval_sign"],
    )
    replayed_face_signs = (
        lower_face_status["resolved_sign"],
        upper_face_status["resolved_sign"],
    )
    expected_face_signs = (
        ("STRICT_NEGATIVE", "STRICT_POSITIVE")
        if replayed_derivative_sign == "STRICT_POSITIVE"
        else ("STRICT_POSITIVE", "STRICT_NEGATIVE")
    )
    need(
        local["row"]["local_disposition"] == "WHOLE_PHYSICAL_SUPPORT"
        and local["row"]["representation_role"]
        == "DIRECT_GRAPH_SHEET_WITNESS"
        and local["row"]["absence_witness_cell_count"] == 0
        and local["row"]["absence_witness_cells"] == []
        and cell["witness_kind"] == "ROUND182_GRAPH_SHEET_LEAF"
        and cell["graph_classification"] == "FULL_2D"
        and leaf["graph_classification"] == "FULL_2D"
        and negative["graph_classification"] == "FULL_2D"
        and positive["graph_classification"] == "FULL_2D"
        and cell["leaf_row_id"] == sheet["leaf_row_id"] == leaf["row_id"]
        and cell["retained_child_row_id"]
        == leaf["retained_child_row_id"]
        == negative["retained_child_row_id"]
        == positive["retained_child_row_id"]
        and cell["exact_box"]
        == exact_box
        == leaf["box"]
        == negative["leaf_exact_box"]
        == positive["leaf_exact_box"]
        and Q(cell["base_coordinate_area"])
        == Q(leaf["base_coordinate_area"])
        == exact_base_area > 0
        and local["row"]["source_chart"]
        == sheet["chart"]
        == negative["chart"]
        == positive["chart"]
        == collar["chart"]
        == origin["chart"]
        == active_row["chart"]
        and sheet["owner_target"]
        == negative["owner_target"]
        == positive["owner_target"]
        == collar["owner_target"]
        == origin["owner_target"]
        and sheet["origin_row_id"]
        == negative["origin_row_id"]
        == positive["origin_row_id"]
        == collar["origin_row_id"]
        == origin["origin_row_id"]
        == active_row["origin_row_id"]
        and sheet["parent_id"]
        == negative["parent_id"]
        == positive["parent_id"]
        == collar["parent_id"]
        == origin["parent_id"]
        == active_row["parent_id"]
        == local["row"]["parent_id"]
        and negative["occurrence_row_id"]
        == positive["occurrence_row_id"]
        == leaf["occurrence_row_id"]
        == collar["Round179_occurrence_row_id"]
        == active_row["row_id"]
        == local["row"]["canonical_support_row_id"]
        and negative["Round182_leaf_packed_sha256"]
        == positive["Round182_leaf_packed_sha256"]
        and sheet["wall_axis"]
        == negative["wall_axis"]
        == positive["wall_axis"]
        == active_row["axis"]
        and sheet["integer_wall"]
        == negative["integer_wall"]
        == positive["integer_wall"]
        == active_row["integer_wall"]
        and local["row"]["predicate_equation"]
        == collar["equation"]
        == active_row["zero_equation"]
        == product_equation
        and collar["reason_label"] == active_row["reason_label"]
        and collar["kind"] == "WALL"
        and active_row["target_factor_classification"] == "REGULAR_GRAPH"
        and active_row["target_gradient_axis"]
        == sheet["target_factor_graph_axis"]
        == "t"
        and active_row["target_gradient_sign"]
        == collar["strict_t_derivative_sign"]
        == sheet["target_t_derivative_sign"]
        == replayed_derivative_sign
        and replayed_derivative_sign in STRICT_SIGNS
        and all(sign in STRICT_SIGNS for sign in replayed_face_signs)
        and replayed_face_signs == expected_face_signs
        and leaf["lower_t_face_status"]
        == replayed_face_statuses[0]
        and leaf["upper_t_face_status"]
        == replayed_face_statuses[1]
        and leaf["two_dimensional_graph_sheet_count"] == 1
        and sheet["source_sign_on_leaf"] in {"NEGATIVE", "POSITIVE"},
        "B2_EXACT_OWNER_EQUATION_FACTOR_LEAF_PROVENANCE:"
        + record["source_id"],
    )
    b2a_exact_join = {
        "Round182_target_factor_sheet_theorem_id":
            R182_TARGET_FACTOR_SHEET_THEOREM_ID,
        "Round182_target_factor_sheet_theorem_sha256":
            R182_TARGET_FACTOR_SHEET_THEOREM_SHA256,
        "Round204_sheet_leaf_row_id": sheet["leaf_row_id"],
        "Round204_sheet_chart": sheet["chart"],
        "Round204_sheet_owner_target": sheet["owner_target"],
        "Round204_sheet_origin_row_id": sheet["origin_row_id"],
        "Round204_sheet_exact_box": exact_box,
        "Round204_sheet_base_coordinate_area": qstr(exact_base_area),
        "Round204_target_factor_equation": target_factor_equation,
        "Round182_collar_row_id": collar["row_id"],
        "Round182_leaf_row_id": leaf["row_id"],
        "Round182_leaf_graph_classification":
            leaf["graph_classification"],
        "Round182_leaf_base_coordinate_area":
            leaf["base_coordinate_area"],
        "Round182_WALL_geometry_selector": target_selector_scalar,
        "Round182_WALL_geometry_selector_source":
            "independent_geometry." + selector_coordinate,
        "Round182_replayed_target_t_derivative_sign":
            replayed_derivative_sign,
        "Round182_raw_lower_t_face_interval_sign":
            raw_face_interval_signs[0],
        "Round182_raw_upper_t_face_interval_sign":
            raw_face_interval_signs[1],
        "Round182_replayed_lower_t_face_encoded_status":
            replayed_face_statuses[0],
        "Round182_replayed_upper_t_face_encoded_status":
            replayed_face_statuses[1],
        "Round182_replayed_lower_t_face_certificate":
            independent_compact_round182_face_status(lower_face_status),
        "Round182_replayed_upper_t_face_certificate":
            independent_compact_round182_face_status(upper_face_status),
        "Round182_serialized_lower_t_face_status":
            leaf["lower_t_face_status"],
        "Round182_serialized_upper_t_face_status":
            leaf["upper_t_face_status"],
        "Round182_replayed_lower_t_face_sign":
            replayed_face_signs[0],
        "Round182_replayed_upper_t_face_sign":
            replayed_face_signs[1],
        "Round182_FULL_2D_unique_target_graph_checked": True,
        "Round179_active_row_id": active_row["row_id"],
        "Round179_nominal_product_lineage_equation": product_equation,
        "Round179_source_factor_equation": source_factor_equation,
        "Round179_target_factor_equation": target_factor_equation,
        "Round179_target_factor_classification":
            active_row["target_factor_classification"],
        "Round179_target_gradient_axis":
            active_row["target_gradient_axis"],
        "Round179_target_gradient_sign":
            active_row["target_gradient_sign"],
        "active_factor_semantic_mapping":
            "ROUND204_TARGET_FACTOR_IS_ROUND182_WALL_TARGET_SELECTOR",
        "Round204_half_open_source_sign_on_leaf":
            sheet["source_sign_on_leaf"],
        "source_sign_join_role":
            "INFORMATIONAL_HALF_OPEN_STRENGTHENING_NOT_LOGICAL_BRIDGE",
        "nominal_product_lineage_compatibility_checked": True,
        "nominal_product_equation_used_as_sheet_identity": False,
        "product_zero_iff_target_zero_claimed": False,
        "closed_leaf_source_factor_strict_nonzero_required": False,
        "exact_owner_leaf_chart_box_base_area_join_checked": True,
        "exact_active_factor_provenance_mapping_checked": True,
    }
    b2b_exact_join = {
        **b2a_exact_join,
        "Round291_local_disposition_row_id": local["row"][
            "complete_lower_stratum_local_disposition_row_id"
        ],
        "Round291_local_disposition_row_sha256":
            local["row"]["row_sha256"],
        "Round291_physical_witness_cell_index": cell_index,
        "Round291_physical_witness_leaf_row_id": cell["leaf_row_id"],
        "Round291_physical_witness_graph_classification":
            cell["graph_classification"],
        "Round291_physical_witness_exact_box": cell["exact_box"],
        "Round291_physical_witness_base_coordinate_area":
            cell["base_coordinate_area"],
        "Round291_nominal_predicate_product_equation":
            local["row"]["predicate_equation"],
        "Round291_representation_role":
            local["row"]["representation_role"],
        "Round291_local_disposition":
            local["row"]["local_disposition"],
        "Round204_sheet_and_R291_witness_same_leaf": True,
        "Round204_sheet_and_R291_witness_same_exact_box": True,
        "Round204_sheet_and_R291_witness_same_chart": True,
        "Round204_sheet_and_R291_witness_same_owner_target": True,
        "Round204_sheet_and_R291_witness_same_base_area": True,
        "Round204_Gamma_equals_Round182_target_factor_graph": True,
        "Round291_DIRECT_witness_carries_same_Round182_target_sheet": True,
        "Round293_and_Round295A_bind_same_two_Round294_occurrences": True,
        "Gamma_included_via_R291_DIRECT_target_sheet_witness": True,
    }
    return b2a_exact_join, b2b_exact_join


def build_b2_rows(
    *,
    record: dict[str, Any],
    lineage: dict[str, Any],
    r294: dict[str, dict[str, Any]],
    r295: dict[str, dict[str, Any]],
    r293: dict[str, dict[str, Any]],
    r291: dict[str, dict[str, Any]],
    leaves: dict[str, dict[str, Any]],
    collars: dict[str, dict[str, Any]],
    origins: dict[str, dict[str, Any]],
    active: dict[str, dict[str, Any]],
    kernel: Any,
) -> tuple[dict[str, Any], dict[str, Any]]:
    sheet = lineage["sheet"]
    negative = lineage["negative"]
    positive = lineage["positive"]
    local = r291[record["r291_ids"][0]]
    cell = local["cells"][record["cell_indices"][0]]
    leaf = leaves[cell["leaf_row_id"]]
    collar = collars[leaf["occurrence_row_id"]]
    origin = origins[collar["origin_row_id"]]
    sheet_leaf_box = [
        *sheet["leaf_t_exact_bounds"],
        *sheet["base_p_s_exact_bounds"],
    ]
    base_measure = (
        (
            Q(sheet["base_p_s_exact_bounds"][1])
            - Q(sheet["base_p_s_exact_bounds"][0])
        )
        * (
            Q(sheet["base_p_s_exact_bounds"][3])
            - Q(sheet["base_p_s_exact_bounds"][2])
        )
    )
    need(
        sheet["existence_certification"] == FULL_2D_CERT
        and sheet["existence_certification"] != TAIL_CERT
        and negative["tail_region"] is False
        and positive["tail_region"] is False
        and negative["graph_classification"] == "FULL_2D"
        and positive["graph_classification"] == "FULL_2D",
        "B2A_FULL2D_ROUTE_ONLY:" + record["source_id"],
    )
    need(
        local["row"]["local_disposition"] == "WHOLE_PHYSICAL_SUPPORT"
        and local["row"]["representation_role"]
        == "DIRECT_GRAPH_SHEET_WITNESS"
        and local["row"]["absence_witness_cell_count"] == 0
        and local["row"]["absence_witness_cells"] == []
        and cell["graph_classification"] == "FULL_2D"
        and leaf["graph_classification"] == "FULL_2D"
        and cell["leaf_row_id"] == sheet["leaf_row_id"] == leaf["row_id"]
        and cell["exact_box"] == sheet_leaf_box == leaf["box"]
        and cell["retained_child_row_id"]
        == leaf["retained_child_row_id"]
        and local["row"]["source_chart"] == sheet["chart"]
        and sheet["chart"] == collar["chart"] == origin["chart"]
        and sheet["owner_target"]
        == collar["owner_target"]
        == origin["owner_target"]
        and sheet["origin_row_id"] == origin["origin_row_id"]
        and Q(cell["base_coordinate_area"]) == base_measure > 0,
        "B2B_EXACT_R204_R182_R179_R291_IDENTITY:"
        + record["source_id"],
    )
    b2a_exact_join, b2b_exact_join = independent_b2_exact_join_payloads(
        record=record,
        lineage=lineage,
        r291=r291,
        leaves=leaves,
        collars=collars,
        origins=origins,
        active=active,
        kernel=kernel,
    )
    endpoint_rows: list[dict[str, Any]] = []
    for endpoint in record["pair"]:
        region = (
            negative if endpoint == negative["region_row_id"] else positive
        )
        registry = r294[endpoint]
        member = record["member_refs"][endpoint]
        need(
            region["region_row_id"] == endpoint
            and registry["source_geometry_row_id"] == endpoint
            and registry["source_geometry_row_sha256"]
            == region["row_sha256"]
            and member["official_key_id"] == registry["official_key_id"],
            "B2_ENDPOINT_JOIN:" + endpoint,
        )
        endpoint_rows.append({
            "registry_occurrence_id": endpoint,
            "Round204_region_row_id": region["region_row_id"],
            "Round204_region_row_sha256": region["row_sha256"],
            "target_factor_sign": region["target_factor_sign"],
            "Round294_registry_row_id":
                registry["Round294_occurrence_registry_row_id"],
            "Round294_registry_row_sha256": registry["row_sha256"],
            "Round301_member_reference": member,
        })
    need(
        {row["target_factor_sign"] for row in endpoint_rows}
        == {"NEGATIVE", "POSITIVE"},
        "B2A_OPPOSITE_ENDPOINT_SIGNS",
    )

    b2a = close_row("b2a", {
        "schema": SCHEMA + ".b2a-analytic-lemma-row.v1",
        "proof_path": "B2A_R204_ANALYTIC_TARGET_GRAPH_SHEET",
        "theorem_id": B2A_THEOREM_ID,
        "theorem_sha256": B2A_LAYER_THEOREM_SHA256,
        "source_Round300D_row_id": record["source_id"],
        "source_Round300D_row_sha256": record["source_sha256"],
        "canonical_endpoint_pair": list(record["pair"]),
        "Round204_target_sheet_reference": {
            "sheet_row_id": sheet["sheet_row_id"],
            "row_sha256": sheet["row_sha256"],
            "leaf_row_id": sheet["leaf_row_id"],
            "chart": sheet["chart"],
            "owner_target": sheet["owner_target"],
            "leaf_t_exact_bounds": sheet["leaf_t_exact_bounds"],
            "base_p_s_exact_bounds": sheet["base_p_s_exact_bounds"],
            "target_t_derivative_sign":
                sheet["target_t_derivative_sign"],
            "existence_certification": sheet["existence_certification"],
        },
        "endpoint_open_region_references": endpoint_rows,
        "exact_join": b2a_exact_join,
        "analytic_conclusion": {
            "Gamma_nonempty": True,
            "Gamma_unique_graph_over_connected_positive_area_base": True,
            "Gamma_connected": True,
            "physical_inclusion_claimed_at_B2a": False,
        },
        "candidate_B2a_analytic_lemma_conclusion": True,
        "formal_B2a_analytic_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        **{field: 0 for field in ZERO_FIELDS},
    })
    b2b = close_row("b2b", {
        "schema": SCHEMA + ".b2b-inclusion-lemma-row.v1",
        "proof_path": "B2B_R291_R293_R295A_PHYSICAL_SHEET_INCLUSION",
        "theorem_id": B2B_THEOREM_ID,
        "theorem_sha256": B2B_LAYER_THEOREM_SHA256,
        "Round182_target_factor_sheet_theorem_id":
            R182_TARGET_FACTOR_SHEET_THEOREM_ID,
        "Round182_target_factor_sheet_theorem_sha256":
            R182_TARGET_FACTOR_SHEET_THEOREM_SHA256,
        "source_B2a_row_id": b2a[ID_FIELDS["b2a"]],
        "source_B2a_row_sha256": b2a["row_sha256"],
        "source_Round300D_row_id": record["source_id"],
        "source_Round300D_row_sha256": record["source_sha256"],
        "canonical_endpoint_pair": list(record["pair"]),
        "Round204_target_sheet_row_id": sheet["sheet_row_id"],
        "Round204_target_sheet_row_sha256": sheet["row_sha256"],
        "physical_inclusion_chain": source_refs(
            record, r295, r293, r291
        ),
        "exact_join": b2b_exact_join,
        "candidate_B2b_inclusion_lemma_conclusion": True,
        "formal_B2b_physical_inclusion_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        **{field: 0 for field in ZERO_FIELDS},
    })
    return b2a, b2b


def build_edge_row(
    record: dict[str, Any],
    route: str,
    lemma_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    expected_fields = (
        [ID_FIELDS["b1"]]
        if route == "b1"
        else [ID_FIELDS["b2a"], ID_FIELDS["b2b"]]
        if route == "b2"
        else None
    )
    need(expected_fields is not None, "EDGE_ROUTE")
    need(
        len(lemma_rows) == len(expected_fields)
        and all(
            field in row
            for field, row in zip(expected_fields, lemma_rows, strict=True)
        ),
        "EDGE_LEMMA_ARITY",
    )
    references = [
        {"row_id": row[field], "row_sha256": row["row_sha256"]}
        for field, row in zip(expected_fields, lemma_rows, strict=True)
    ]
    components = {
        endpoint: record["member_refs"][endpoint]["component_id"]
        for endpoint in record["pair"]
    }
    need(
        len(set(components.values())) == 2,
        "EDGE_MUST_BE_CROSS_ROUND301",
    )
    return close_row("edge", {
        "schema": SCHEMA + ".component-edge-row.v1",
        "theorem_id": THEOREM_ID,
        "theorem_sha256": THEOREM_SHA256,
        "proof_path": (
            "B1_MONOTONE_GRAPH_SIDE_ATTACHMENT"
            if route == "b1"
            else "B2_R204_ANALYTIC_PLUS_R291_PHYSICAL_INCLUSION"
        ),
        "source_Round300D_row_id": record["source_id"],
        "source_Round300D_row_sha256": record["source_sha256"],
        "source_Round301_ineligible_reference":
            record["r301_ineligible_ref"],
        "canonical_unordered_registry_occurrence_ids":
            list(record["pair"]),
        "source_lemma_references": references,
        "Round301_pre_edge_components": components,
        "official_key_metadata": {
            endpoint: record["endpoint_refs"][endpoint][
                "official_key_id"
            ]
            for endpoint in record["pair"]
        },
        "G0_exact_provenance_pins_and_row_closures": True,
        "G1_endpoint_occurrence_connected_supports": True,
        "G2_nonempty_connected_included_lower_stratum": True,
        "G3_left_closure_attaches_to_included_patch": True,
        "G4_right_closure_attaches_to_included_patch": True,
        "G5_endpoint_patch_provenance_exactly_closed": True,
        "candidate_component_connectivity_conclusion": True,
        "formal_component_edge_credit": 1,
        "eligible_for_later_fresh_DSU_application": True,
        "old_63224_component_result_reused": False,
        "Round301_DSU_mutated_here": False,
        **{field: 0 for field in ZERO_FIELDS},
    })


def build_unresolved_row(record: dict[str, Any]) -> dict[str, Any]:
    refs = [
        record["unresolved_refs"][endpoint]
        for endpoint in record["pair"]
    ]
    need(
        all(
            ref["disposition"]
            == "UNRESOLVED__W_TAIL_CONNECTED_SOURCE_SIDE_EXTENSION_MISSING"
            for ref in refs
        ),
        "WTAIL_UNRESOLVED_ONLY",
    )
    return close_row("unresolved", {
        "schema": SCHEMA + ".wtail-unresolved-row.v1",
        "source_Round300D_row_id": record["source_id"],
        "source_Round300D_row_sha256": record["source_sha256"],
        "source_Round301_ineligible_reference":
            record["r301_ineligible_ref"],
        "canonical_unordered_registry_occurrence_ids":
            list(record["pair"]),
        "Round303A_unresolved_endpoint_references": [
            {
                "endpoint": ref["endpoint"],
                "row_id": ref["row_id"],
                "row_sha256": ref["row_sha256"],
                "missing_obligation": ref["missing_obligation"],
            }
            for ref in refs
        ],
        "disposition": WT_DISPOSITION,
        "formal_component_edge_credit": 0,
        "nonedge_credit": 0,
        "exclusion_credit": 0,
        "eligible_for_later_fresh_DSU_application": False,
        **{field: 0 for field in ZERO_FIELDS},
    })


class ListHasher:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for part in pieces(value):
            self.state.update(part)
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


class ExternalRowSorter:
    """Bounded-memory lexical sorter by canonical output row ID."""

    def __init__(
        self,
        directory: Path,
        route: str,
        *,
        chunk_rows: int = 256,
    ) -> None:
        self.directory = directory
        self.route = route
        self.id_field = ID_FIELDS[route]
        self.chunk_rows = chunk_rows
        self.buffer: list[tuple[str, bytes]] = []
        self.chunks: list[Path] = []
        self.seen: set[str] = set()

    def add(self, row: dict[str, Any]) -> None:
        verify_expected_row(self.route, row)
        row_id = row[self.id_field]
        need(row_id not in self.seen, "OUTPUT_ROW_ID_UNIQUE:" + row_id)
        self.seen.add(row_id)
        self.buffer.append((row_id, canonical(row)))
        if len(self.buffer) >= self.chunk_rows:
            self._flush()

    def _flush(self) -> None:
        if not self.buffer:
            return
        self.buffer.sort(key=lambda item: item[0])
        path = self.directory / (
            f".{self.route}.sort-{len(self.chunks):06d}.chunk"
        )
        with path.open("wb") as stream:
            for row_id, raw in self.buffer:
                stream.write(row_id.encode("ascii") + b"\t" + raw + b"\n")
        self.chunks.append(path)
        self.buffer.clear()

    @staticmethod
    def _iter_chunk(path: Path) -> Iterator[tuple[str, bytes]]:
        with path.open("rb") as stream:
            for line in stream:
                row_id, raw = line.rstrip(b"\n").split(b"\t", 1)
                yield row_id.decode("ascii"), raw

    def finish(self) -> tuple[Path, dict[str, Any]]:
        self._flush()
        rows_path = self.directory / (self.route + ".expected.rows")
        row_hasher = ListHasher()
        id_hasher = ListHasher()
        hash_hasher = ListHasher()
        previous: str | None = None
        iterators = [self._iter_chunk(path) for path in self.chunks]
        with rows_path.open("wb") as output:
            for row_id, raw in heapq.merge(
                *iterators, key=lambda item: item[0]
            ):
                need(
                    previous is None or previous < row_id,
                    "OUTPUT_ROW_ID_STRICT_ORDER:" + self.route,
                )
                value = strict_json_bytes(raw, self.route + ":sorted-row")
                need(type(value) is dict, "SORTED_ROW_OBJECT")
                verify_expected_row(self.route, value)
                output.write(raw + b"\n")
                row_hasher.add(value)
                id_hasher.add(row_id)
                hash_hasher.add(value["row_sha256"])
                previous = row_id
        for path in self.chunks:
            path.unlink()
        commitments = {
            "row_count": row_hasher.count,
            "row_ids_sha256": id_hasher.finish(),
            "row_hashes_sha256": hash_hasher.finish(),
            "rows_sha256": row_hasher.finish(),
        }
        return rows_path, commitments


def exact_nested_dict(
    value: Any,
    schema_path: str,
    label: str,
) -> dict[str, Any]:
    need(
        type(value) is dict
        and sorted(value) == NESTED_KEY_SETS[schema_path],
        "NESTED_EXACT_KEYS:" + label + ":" + schema_path,
    )
    return value


def validate_canonical_pair(value: Any, label: str) -> list[str]:
    need(
        type(value) is list
        and len(value) == 2
        and all(type(item) is str for item in value)
        and value == sorted(value)
        and len(set(value)) == 2,
        "NESTED_CANONICAL_PAIR:" + label,
    )
    return value


def validate_physical_inclusion_chain(
    value: Any,
    label: str,
) -> None:
    chain = exact_nested_dict(
        value,
        "physical_inclusion_chain",
        label,
    )
    round291 = exact_nested_dict(
        chain["Round291"],
        "physical_inclusion_chain.Round291",
        label,
    )
    exact_nested_dict(
        round291["physical_witness_cell"],
        "physical_inclusion_chain.Round291.physical_witness_cell",
        label,
    )
    for round_name in ("Round293", "Round295A"):
        exact_nested_dict(
            chain[round_name],
            "physical_inclusion_chain.binding",
            label + ":" + round_name,
        )


def validate_nested_row_schema(
    route: str,
    row: dict[str, Any],
) -> None:
    if route in {"b1", "edge", "unresolved"}:
        exact_nested_dict(
            row["source_Round301_ineligible_reference"],
            "source_Round301_ineligible_reference",
            route,
        )
    if route in {"b1", "b2b"}:
        validate_physical_inclusion_chain(
            row["physical_inclusion_chain"],
            route,
        )

    if route == "b1":
        validate_canonical_pair(row["canonical_endpoint_pair"], "B1")
        endpoints = row["endpoint_connected_side_rows"]
        need(
            type(endpoints) is list and len(endpoints) == 2,
            "B1_ENDPOINT_CONNECTED_SIDE_CENSUS",
        )
        for index, endpoint in enumerate(endpoints):
            endpoint_label = "B1:endpoint:" + str(index)
            exact_nested_dict(
                endpoint,
                "B1.endpoint_connected_side_row",
                endpoint_label,
            )
            need(
                type(endpoint["Round301_member_reference"]) is dict
                and sorted(endpoint["Round301_member_reference"])
                == ROUND301_MEMBER_REFERENCE_KEYS,
                "B1_MEMBER_REFERENCE_KEYS:" + endpoint_label,
            )
            exact_nested_dict(
                endpoint["connected_source_side_witness"],
                "B1.connected_source_side_witness",
                endpoint_label,
            )
            exact_nested_dict(
                endpoint["closure_attachment_to_Gamma"],
                "B1.closure_attachment_to_Gamma",
                endpoint_label,
            )
        gamma = exact_nested_dict(row["Gamma"], "B1.Gamma", "B1")
        exact_nested_dict(
            gamma["exact_chart_radicand_margins"],
            "B1.Gamma.exact_chart_radicand_margins",
            "B1",
        )
        exact_nested_dict(
            row["local_side_nonempty_witnesses"],
            "B1.local_side_nonempty_witnesses",
            "B1",
        )
        exact_nested_dict(
            row["two_sided_limit_attachment"],
            "B1.two_sided_limit_attachment",
            "B1",
        )
        inactive = row["inactive_wall_source_factor_replay"]
        need(
            inactive is None or type(inactive) is dict,
            "B1_INACTIVE_REPLAY_NULL_OR_OBJECT",
        )
        if inactive is not None:
            inactive = exact_nested_dict(
                inactive,
                "B1.inactive_wall_source_factor_replay",
                "B1",
            )
            need(
                type(inactive["corridor_checks"]) is list,
                "B1_INACTIVE_CORRIDOR_CHECKS_LIST",
            )
            for index, check in enumerate(inactive["corridor_checks"]):
                exact_nested_dict(
                    check,
                    "B1.inactive_wall_source_factor_replay.corridor_check",
                    "B1:corridor:" + str(index),
                )
        exact_nested_dict(
            row["B1_predicates"],
            "B1.B1_predicates",
            "B1",
        )
        exact_nested_dict(
            row["limit_theorem_predicates"],
            "B1.limit_theorem_predicates",
            "B1",
        )
        need(
            row["monotone_limit_theorem"] == MONOTONE_LIMIT_THEOREM,
            "B1_MONOTONE_LIMIT_THEOREM_FULL_OBJECT",
        )
    elif route == "b2a":
        validate_canonical_pair(row["canonical_endpoint_pair"], "B2A")
        exact_nested_dict(
            row["Round204_target_sheet_reference"],
            "B2a.Round204_target_sheet_reference",
            "B2A",
        )
        endpoints = row["endpoint_open_region_references"]
        need(
            type(endpoints) is list and len(endpoints) == 2,
            "B2A_ENDPOINT_OPEN_REGION_CENSUS",
        )
        for index, endpoint in enumerate(endpoints):
            exact_nested_dict(
                endpoint,
                "B2a.endpoint_open_region_reference",
                "B2A:endpoint:" + str(index),
            )
            need(
                type(endpoint["Round301_member_reference"]) is dict
                and sorted(endpoint["Round301_member_reference"])
                == ROUND301_MEMBER_REFERENCE_KEYS,
                "B2A_MEMBER_REFERENCE_KEYS:" + str(index),
            )
        exact_nested_dict(
            row["analytic_conclusion"],
            "B2a.analytic_conclusion",
            "B2A",
        )
    elif route == "b2b":
        validate_canonical_pair(row["canonical_endpoint_pair"], "B2B")
    elif route == "edge":
        pair = validate_canonical_pair(
            row["canonical_unordered_registry_occurrence_ids"],
            "EDGE",
        )
        lemma_refs = row["source_lemma_references"]
        expected_arity = (
            1
            if row["proof_path"]
            == "B1_MONOTONE_GRAPH_SIDE_ATTACHMENT"
            else 2
        )
        need(
            row["proof_path"] in {
                "B1_MONOTONE_GRAPH_SIDE_ATTACHMENT",
                "B2_R204_ANALYTIC_PLUS_R291_PHYSICAL_INCLUSION",
            }
            and type(lemma_refs) is list
            and len(lemma_refs) == expected_arity,
            "EDGE_LEMMA_REFERENCE_ARITY",
        )
        for index, reference in enumerate(lemma_refs):
            exact_nested_dict(
                reference,
                "edge.source_lemma_reference",
                "EDGE:" + str(index),
            )
        components = row["Round301_pre_edge_components"]
        official = row["official_key_metadata"]
        need(
            type(components) is dict
            and type(official) is dict
            and sorted(components) == pair
            and sorted(official) == pair
            and all(type(value) is str for value in components.values())
            and all(type(value) is str for value in official.values()),
            "EDGE_DYNAMIC_ENDPOINT_MAPS",
        )
    else:
        need(route == "unresolved", "NESTED_ROUTE")
        pair = validate_canonical_pair(
            row["canonical_unordered_registry_occurrence_ids"],
            "UNRESOLVED",
        )
        references = row["Round303A_unresolved_endpoint_references"]
        need(
            type(references) is list and len(references) == 2,
            "UNRESOLVED_ENDPOINT_REFERENCE_CENSUS",
        )
        for index, reference in enumerate(references):
            exact_nested_dict(
                reference,
                "unresolved.endpoint_reference",
                "UNRESOLVED:" + str(index),
            )
        need(
            sorted(reference["endpoint"] for reference in references)
            == pair,
            "UNRESOLVED_ENDPOINT_REFERENCE_EXACT_PAIR",
        )


def validate_common_b2_exact_join_semantics(
    exact_join: dict[str, Any],
    label: str,
) -> None:
    expected_keys = (
        B2A_COMMON_EXACT_JOIN_KEYS
        if label == "B2A"
        else B2B_EXACT_JOIN_KEYS
    )
    need(
        label in {"B2A", "B2B"}
        and sorted(exact_join) == expected_keys,
        "B2_EXACT_JOIN_EXACT_KEY_SET:" + label,
    )
    need(
        exact_join["Round182_target_factor_sheet_theorem_id"]
        == R182_TARGET_FACTOR_SHEET_THEOREM_ID
        and exact_join["Round182_target_factor_sheet_theorem_sha256"]
        == R182_TARGET_FACTOR_SHEET_THEOREM_SHA256
        and exact_join[
            "Round182_FULL_2D_unique_target_graph_checked"
        ] is True
        and exact_join["active_factor_semantic_mapping"]
        == "ROUND204_TARGET_FACTOR_IS_ROUND182_WALL_TARGET_SELECTOR"
        and exact_join[
            "nominal_product_lineage_compatibility_checked"
        ] is True
        and exact_join[
            "nominal_product_equation_used_as_sheet_identity"
        ] is False
        and exact_join["product_zero_iff_target_zero_claimed"] is False
        and exact_join[
            "closed_leaf_source_factor_strict_nonzero_required"
        ] is False
        and exact_join["source_sign_join_role"]
        == "INFORMATIONAL_HALF_OPEN_STRENGTHENING_NOT_LOGICAL_BRIDGE",
        "B2_COMMON_TARGET_SELECTOR_AND_NONCLAIMS:" + label,
    )
    resolved_faces = (
        exact_join["Round182_replayed_lower_t_face_sign"],
        exact_join["Round182_replayed_upper_t_face_sign"],
    )
    derivative_sign = exact_join[
        "Round182_replayed_target_t_derivative_sign"
    ]
    oriented_faces = (
        ("STRICT_NEGATIVE", "STRICT_POSITIVE")
        if derivative_sign == "STRICT_POSITIVE"
        else ("STRICT_POSITIVE", "STRICT_NEGATIVE")
    )
    need(
        derivative_sign in STRICT_SIGNS
        and resolved_faces == oriented_faces,
        "B2_COMMON_OPPOSITE_RESOLVED_FACE_SIGNS:" + label,
    )
    for side, resolved in zip(
        ("lower", "upper"), resolved_faces, strict=True
    ):
        raw = exact_join[
            "Round182_raw_" + side + "_t_face_interval_sign"
        ]
        encoded = exact_join[
            "Round182_replayed_" + side + "_t_face_encoded_status"
        ]
        serialized = exact_join[
            "Round182_serialized_" + side + "_t_face_status"
        ]
        certificate = exact_join[
            "Round182_replayed_" + side + "_t_face_certificate"
        ]
        need(
            sorted(certificate) == FACE_CERTIFICATE_KEYS
            and certificate["raw_interval_sign"] == raw
            and certificate["resolved_sign"] == resolved
            and independent_encode_round182_face_status(certificate)
            == encoded
            == serialized,
            "B2_COMMON_FACE_CERTIFICATE_CROSS_FIELDS:"
            + label
            + ":"
            + side,
        )
        direct = certificate["kind"] == "STRICT"
        absent = certificate["kind"] == "ABSENT"
        need(
            (
                direct
                and raw == resolved
                and certificate["axis"] is None
                and certificate["derivative_sign"] is None
                and certificate["axis_lower_sign"] is None
                and certificate["axis_upper_sign"] is None
                and certificate["newton_interior"] is None
            )
            or (
                absent
                and raw == "OVERWRAP"
                and certificate["axis"] in {"p", "s"}
                and certificate["derivative_sign"] in STRICT_SIGNS
                and certificate["axis_lower_sign"]
                == certificate["axis_upper_sign"]
                == resolved
                and certificate["newton_interior"] is None
            ),
            "B2_COMMON_FACE_CERTIFICATE_SEMANTICS:"
            + label
            + ":"
            + side,
        )


def validate_round301_member_references(
    endpoint_rows: Any,
    label: str,
) -> None:
    need(
        type(endpoint_rows) is list and len(endpoint_rows) == 2,
        "ROUND301_MEMBER_REFERENCE_ENDPOINT_CENSUS:" + label,
    )
    for index, endpoint_row in enumerate(endpoint_rows):
        need(
            type(endpoint_row) is dict
            and type(endpoint_row.get("Round301_member_reference")) is dict
            and sorted(endpoint_row["Round301_member_reference"])
            == ROUND301_MEMBER_REFERENCE_KEYS,
            "ROUND301_MEMBER_REFERENCE_EXACT_KEYS:"
            + label
            + ":"
            + str(index),
        )


def verify_expected_row(
    route: str,
    row: dict[str, Any],
    *,
    trusted_expected_row: dict[str, Any] | None = None,
) -> None:
    need(
        sorted(row) == ROW_KEY_SETS[route],
        "EXPECTED_ROW_EXACT_KEY_SET:" + route,
    )
    validate_nested_row_schema(route, row)
    verify_row(row, route)
    payload = dict(row)
    claimed_hash = payload.pop("row_sha256")
    claimed_id = payload.pop(ID_FIELDS[route])
    need(
        claimed_hash == digest({**payload, ID_FIELDS[route]: claimed_id}),
        "EXPECTED_ROW_HASH:" + route,
    )
    need(
        claimed_id
        == ID_PREFIXES[route] + digest([ID_CONTEXTS[route], payload]),
        "EXPECTED_ROW_ID_PREIMAGE:" + route,
    )
    for field in ZERO_FIELDS:
        need(row.get(field) == 0, "ZERO_CREDIT:" + route + ":" + field)
    if route == "b1":
        validate_round301_member_references(
            row["endpoint_connected_side_rows"],
            "B1",
        )
        need(
            row.get("theorem_sha256") == B1_LAYER_THEOREM_SHA256
            and row.get("monotone_limit_theorem")
            == MONOTONE_LIMIT_THEOREM
            and row.get("monotone_limit_theorem_sha256")
            == MONOTONE_LIMIT_THEOREM_SHA256
            and row.get("formal_B1_attachment_lemma_credit") == 1
            and row.get("formal_component_edge_credit") == 0,
            "B1_THEOREM_CREDIT_BOUNDARY",
        )
        witnesses = row["local_side_nonempty_witnesses"]
        need(
            witnesses["corridor_intersects_Gamma_claimed"] is False
            and witnesses["corridor_used_as_attachment_witness"] is False,
            "B1_CORRIDOR_NONCLAIM",
        )
    elif route == "b2a":
        validate_round301_member_references(
            row["endpoint_open_region_references"],
            "B2A",
        )
        exact_join = row["exact_join"]
        validate_common_b2_exact_join_semantics(exact_join, "B2A")
        if trusted_expected_row is not None:
            need(
                trusted_expected_row["exact_join"] == exact_join,
                "B2A_TRUSTED_INDEPENDENT_EXPECTED_EXACT_JOIN",
            )
        need(
            row.get("theorem_sha256") == B2A_LAYER_THEOREM_SHA256
            and row["Round204_target_sheet_reference"][
                "existence_certification"
            ] == FULL_2D_CERT
            and row["Round204_target_sheet_reference"][
                "existence_certification"
            ] != TAIL_CERT
            and row.get("formal_B2a_analytic_lemma_credit") == 1
            and row.get("formal_component_edge_credit") == 0,
            "B2A_FULL2D_THEOREM_BOUNDARY",
        )
        need(
            exact_join["active_factor_semantic_mapping"]
            == "ROUND204_TARGET_FACTOR_IS_ROUND182_WALL_TARGET_SELECTOR"
            and exact_join["Round182_target_factor_sheet_theorem_id"]
            == R182_TARGET_FACTOR_SHEET_THEOREM_ID
            and exact_join["Round182_target_factor_sheet_theorem_sha256"]
            == R182_TARGET_FACTOR_SHEET_THEOREM_SHA256
            and exact_join[
                "Round182_FULL_2D_unique_target_graph_checked"
            ] is True
            and exact_join[
                "nominal_product_equation_used_as_sheet_identity"
            ] is False
            and exact_join[
                "product_zero_iff_target_zero_claimed"
            ] is False
            and exact_join[
                "exact_owner_leaf_chart_box_base_area_join_checked"
            ] is True
            and exact_join[
                "exact_active_factor_provenance_mapping_checked"
            ] is True,
            "B2A_EXACT_JOIN_BOUNDARY",
        )
        resolved_faces = (
            exact_join["Round182_replayed_lower_t_face_sign"],
            exact_join["Round182_replayed_upper_t_face_sign"],
        )
        need(
            set(resolved_faces) == STRICT_SIGNS,
            "B2A_OPPOSITE_RESOLVED_FACE_SIGNS",
        )
        for side, resolved in zip(
            ("lower", "upper"), resolved_faces, strict=True
        ):
            raw = exact_join[
                "Round182_raw_" + side + "_t_face_interval_sign"
            ]
            encoded = exact_join[
                "Round182_replayed_"
                + side
                + "_t_face_encoded_status"
            ]
            serialized = exact_join[
                "Round182_serialized_" + side + "_t_face_status"
            ]
            certificate = exact_join[
                "Round182_replayed_" + side + "_t_face_certificate"
            ]
            need(
                sorted(certificate) == FACE_CERTIFICATE_KEYS
                and certificate["raw_interval_sign"] == raw
                and certificate["resolved_sign"] == resolved
                and independent_encode_round182_face_status(certificate)
                == encoded
                == serialized,
                "B2A_FACE_CERTIFICATE_CROSS_FIELDS:" + side,
            )
            direct = certificate["kind"] == "STRICT"
            absent = certificate["kind"] == "ABSENT"
            need(
                (
                    direct
                    and raw == resolved
                    and certificate["axis"] is None
                    and certificate["derivative_sign"] is None
                    and certificate["axis_lower_sign"] is None
                    and certificate["axis_upper_sign"] is None
                    and certificate["newton_interior"] is None
                )
                or (
                    absent
                    and raw == "OVERWRAP"
                    and certificate["axis"] in {"p", "s"}
                    and certificate["derivative_sign"] in STRICT_SIGNS
                    and certificate["axis_lower_sign"]
                    == certificate["axis_upper_sign"]
                    == resolved
                    and certificate["newton_interior"] is None
                ),
                "B2A_FACE_CERTIFICATE_SEMANTICS:" + side,
            )
        need(
            exact_join["source_sign_join_role"]
            == "INFORMATIONAL_HALF_OPEN_STRENGTHENING_NOT_LOGICAL_BRIDGE"
            and exact_join[
                "nominal_product_lineage_compatibility_checked"
            ] is True
            and exact_join[
                "closed_leaf_source_factor_strict_nonzero_required"
            ] is False,
            "B2A_NOMINAL_PRODUCT_AND_SOURCE_SIGN_NONCLAIMS",
        )
    elif route == "b2b":
        exact_join = row["exact_join"]
        validate_common_b2_exact_join_semantics(exact_join, "B2B")
        if trusted_expected_row is not None:
            need(
                trusted_expected_row["exact_join"] == exact_join,
                "B2B_TRUSTED_INDEPENDENT_EXPECTED_EXACT_JOIN",
            )
        need(
            row.get("theorem_sha256") == B2B_LAYER_THEOREM_SHA256
            and row.get("Round182_target_factor_sheet_theorem_id")
            == R182_TARGET_FACTOR_SHEET_THEOREM_ID
            and row.get("Round182_target_factor_sheet_theorem_sha256")
            == R182_TARGET_FACTOR_SHEET_THEOREM_SHA256
            and row.get("formal_B2b_physical_inclusion_lemma_credit") == 1
            and row.get("formal_component_edge_credit") == 0,
            "B2B_THEOREM_CREDIT_BOUNDARY",
        )
        need(
            exact_join[
                "Round291_physical_witness_graph_classification"
            ] == "FULL_2D"
            and exact_join[
                "Round204_Gamma_equals_Round182_target_factor_graph"
            ] is True
            and exact_join[
                "Round291_DIRECT_witness_carries_same_Round182_target_sheet"
            ] is True
            and exact_join[
                "Gamma_included_via_R291_DIRECT_target_sheet_witness"
            ] is True,
            "B2B_EXACT_JOIN_BOUNDARY",
        )
    elif route == "edge":
        need(
            row.get("theorem_sha256") == THEOREM_SHA256
            and row.get("formal_component_edge_credit") == 1
            and row.get("eligible_for_later_fresh_DSU_application") is True
            and row.get("old_63224_component_result_reused") is False
            and row.get("Round301_DSU_mutated_here") is False,
            "EDGE_THEOREM_CREDIT_BOUNDARY",
        )
    else:
        need(
            route == "unresolved"
            and row.get("disposition") == WT_DISPOSITION
            and row.get("formal_component_edge_credit") == 0
            and row.get("nonedge_credit") == 0
            and row.get("exclusion_credit") == 0
            and row.get("eligible_for_later_fresh_DSU_application") is False,
            "WTAIL_FAIL_CLOSED_BOUNDARY",
        )


def write_expected_ledger(
    path: Path,
    route: str,
    rows_path: Path,
    commitments: dict[str, Any],
) -> None:
    document = {
        "every_row_closed_by_own_SHA256": True,
        "row_count": commitments["row_count"],
        "row_hashes_sha256": commitments["row_hashes_sha256"],
        "row_ids_sha256": commitments["row_ids_sha256"],
        "rows_sha256": commitments["rows_sha256"],
        "schema": SCHEMA + "." + route + "-ledger.v1",
        "status": "FORMAL_COMPLETE__ROUND303A_SEALED__G0_G5_REPLAYED",
        TABLES[route]: None,
    }
    with path.open("wb") as raw, gzip.GzipFile(
        filename="",
        fileobj=raw,
        mode="wb",
        mtime=0,
        compresslevel=9,
    ) as stream:
        stream.write(b"{")
        first = True
        for key in sorted(document):
            if not first:
                stream.write(b",")
            first = False
            stream.write(canonical(key) + b":")
            if key != TABLES[route]:
                stream.write(canonical(document[key]))
                continue
            stream.write(b"[")
            first_row = True
            with rows_path.open("rb") as rows:
                for raw_row in rows:
                    if not first_row:
                        stream.write(b",")
                    first_row = False
                    stream.write(raw_row.rstrip(b"\n"))
            stream.write(b"]")
        stream.write(b"}")


@dataclass
class ExpectedPackage:
    directory: Path
    commitments: dict[str, dict[str, Any]]
    result: dict[str, Any]


def validate_result_schema(result: dict[str, Any]) -> None:
    need(sorted(result) == RESULT_TOP_KEYS, "RESULT_EXACT_TOP_KEYS")
    for field in (
        "executable_runtime_closure",
        "Round303A_seal",
        "Round294B_registry_builder_admission",
        "scope_census",
        "run_census",
        "strict_nonclaims",
        "atomicity_contract",
        "formal_credit_transition",
    ):
        need(
            sorted(result[field]) == RESULT_NESTED_KEY_SETS[field],
            "RESULT_EXACT_NESTED_KEYS:" + field,
        )
    need(
        sorted(result["theorem_objects"])
        == RESULT_NESTED_KEY_SETS["theorem_objects"],
        "RESULT_THEOREM_OBJECT_KEYS",
    )
    need(
        sorted(result["theorem_objects"]["B1_monotone_closure"])
        == RESULT_NESTED_KEY_SETS["B1_monotone_closure"],
        "RESULT_B1_THEOREM_KEYS",
    )
    for field in (
        "B2a_FULL_2D_analytic_closure",
        "G0_G5_final_gluing",
    ):
        need(
            sorted(result["theorem_objects"][field])
            == RESULT_NESTED_KEY_SETS["single_theorem_entry"],
            "RESULT_THEOREM_ENTRY_KEYS:" + field,
        )
    need(
        sorted(
            result["theorem_objects"][
                "B2b_target_factor_sheet_inclusion"
            ]
        )
        == RESULT_NESTED_KEY_SETS[
            "B2b_target_factor_sheet_inclusion"
        ],
        "RESULT_B2B_THEOREM_ENTRY_KEYS",
    )
    need(
        set(result["output_ledgers"]) == set(ID_FIELDS),
        "RESULT_OUTPUT_LEDGER_ROUTES",
    )
    for route, entry in result["output_ledgers"].items():
        need(
            sorted(entry)
            == RESULT_NESTED_KEY_SETS["output_ledger_entry"],
            "RESULT_OUTPUT_LEDGER_KEYS:" + route,
        )
    executable = result["executable_runtime_closure"]
    theorem_objects = result["theorem_objects"]
    need(
        result["input_file_pins"] == EXPECTED_RESULT_INPUT_PINS,
        "RESULT_EXACT_INPUT_FILE_PINS",
    )
    need(
        executable["transitive_file_pins"]
        == dict(sorted(EXECUTABLE_TRANSITIVE_CLOSURE_PINS.items()))
        and executable["recursive_import_graph"]
        == {
            name: sorted(children)
            for name, children in sorted(
                EXECUTABLE_IMPORT_GRAPH.items()
            )
        },
        "RESULT_EXACT_EXECUTABLE_CLOSURE_MAPS",
    )
    need(
        result["Round303A_seal"]["manifest_members"]
        == dict(sorted(R303A_SEAL_MEMBER_PINS.items())),
        "RESULT_EXACT_ROUND303A_MANIFEST_MEMBERS",
    )
    need(
        result["theorem"] == GLUING_THEOREM
        and result["theorem_sha256"] == THEOREM_SHA256
        and theorem_objects["B1_monotone_closure"]["theorem"]
        == B1_LAYER_THEOREM
        and theorem_objects["B1_monotone_closure"]["theorem_sha256"]
        == B1_LAYER_THEOREM_SHA256
        and theorem_objects["B1_monotone_closure"]["kernel_theorem"]
        == MONOTONE_LIMIT_THEOREM
        and theorem_objects["B1_monotone_closure"][
            "kernel_theorem_sha256"
        ] == MONOTONE_LIMIT_THEOREM_SHA256
        and theorem_objects["B2a_FULL_2D_analytic_closure"]["theorem"]
        == B2A_LAYER_THEOREM
        and theorem_objects["B2a_FULL_2D_analytic_closure"][
            "theorem_sha256"
        ] == B2A_LAYER_THEOREM_SHA256
        and theorem_objects["B2b_target_factor_sheet_inclusion"][
            "theorem"
        ] == B2B_LAYER_THEOREM
        and theorem_objects["B2b_target_factor_sheet_inclusion"][
            "theorem_sha256"
        ] == B2B_LAYER_THEOREM_SHA256
        and theorem_objects["B2b_target_factor_sheet_inclusion"][
            "target_factor_sheet_theorem"
        ] == R182_TARGET_FACTOR_SHEET_THEOREM
        and theorem_objects["B2b_target_factor_sheet_inclusion"][
            "target_factor_sheet_theorem_sha256"
        ] == R182_TARGET_FACTOR_SHEET_THEOREM_SHA256
        and theorem_objects["G0_G5_final_gluing"]["theorem"]
        == GLUING_THEOREM
        and theorem_objects["G0_G5_final_gluing"]["theorem_sha256"]
        == THEOREM_SHA256,
        "RESULT_EXACT_THEOREM_OBJECTS",
    )
    need(
        result["required_before_edge_consumption"]
        == REQUIRED_BEFORE_EDGE_CONSUMPTION,
        "RESULT_EXACT_REQUIRED_BEFORE_EDGE_CONSUMPTION",
    )


def exact_result(
    commitments: dict[str, dict[str, Any]],
    file_hashes: dict[str, str],
) -> dict[str, Any]:
    need(seal_ready(), "RESULT_REQUIRES_FROZEN_BOUNDARY")
    need(
        type(FINAL_R303B_PRODUCER_SHA256) is str,
        "FINAL_R303B_PRODUCER_PIN_TYPE",
    )
    need(
        type(R303A_MANIFEST_SHA256) is str,
        "R303A_MANIFEST_PIN_TYPE",
    )
    input_pins: dict[str, str] = {
        **{
            name: value for name, value in BASE_INPUT_PINS.items()
        },
        **EXECUTABLE_TRANSITIVE_CLOSURE_PINS,
        **RAW_R303A_PINS,
        R303A_MANIFEST: R303A_MANIFEST_SHA256,
        **{
            name: value
            for name, value in R303A_SEAL_MEMBER_PINS.items()
            if type(value) is str
        },
    }
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND303B_43912_B1_192_B2_COMPONENT_EDGES__"
            "4_WTAIL_UNRESOLVED__ZERO_DSU_AND_DOWNSTREAM_CREDIT"
        ),
        "producer_sha256": FINAL_R303B_PRODUCER_SHA256,
        "seed_affects_output": False,
        "complete_formal_run": True,
        "provisional_Round303A_consumed": False,
        "input_file_pins": dict(sorted(input_pins.items())),
        "executable_runtime_closure": {
            "entrypoint": R179_KERNEL,
            "transitive_file_pins": dict(sorted(
                EXECUTABLE_TRANSITIVE_CLOSURE_PINS.items()
            )),
            "recursive_import_graph": {
                name: sorted(children)
                for name, children in sorted(
                    EXECUTABLE_IMPORT_GRAPH.items()
                )
            },
            "module_files_exactly_pinned": True,
            "sys_modules_alternates_cleared": True,
            "python_flint_version": "0.9.0",
            "interval_precision_bits": 256,
        },
        "Round303A_seal": {
            "manifest_filename": R303A_MANIFEST,
            "manifest_file_sha256": R303A_MANIFEST_SHA256,
            "manifest_member_count": 10,
            "manifest_members":
                dict(sorted(R303A_SEAL_MEMBER_PINS.items())),
            "manifest_exact_member_set_checked": True,
            "manifest_member_hashes_checked": True,
        },
        "Round294B_registry_builder_admission": {
            "manifest_filename": R294B_MANIFEST,
            "manifest_file_sha256": R294B_MANIFEST_SHA256,
            "manifest_member_count": 11,
            "verification_filename": R294B_VERIFICATION,
            "verification_file_sha256":
                R294B_VERIFICATION_FILE_SHA256,
            "verification_object_sha256":
                R294B_VERIFICATION_OBJECT_SHA256,
            "formal_occurrence_registry_row_count": 431_208,
            "formal_representation_binding_count": 46_288,
            "direct_Round287_union_issuance_count_rejected": 10_020,
            "binding_rows_issuing_occurrence_ID_count": 0,
            "admission_checked_before_Round294_consumption": True,
            "bypass_permitted": False,
        },
        "theorem": GLUING_THEOREM,
        "theorem_sha256": THEOREM_SHA256,
        "theorem_objects": {
            "B1_monotone_closure": {
                "theorem": B1_LAYER_THEOREM,
                "theorem_sha256": B1_LAYER_THEOREM_SHA256,
                "kernel_theorem": MONOTONE_LIMIT_THEOREM,
                "kernel_theorem_sha256":
                    MONOTONE_LIMIT_THEOREM_SHA256,
            },
            "B2a_FULL_2D_analytic_closure": {
                "theorem": B2A_LAYER_THEOREM,
                "theorem_sha256": B2A_LAYER_THEOREM_SHA256,
            },
            "B2b_target_factor_sheet_inclusion": {
                "theorem": B2B_LAYER_THEOREM,
                "theorem_sha256": B2B_LAYER_THEOREM_SHA256,
                "target_factor_sheet_theorem":
                    R182_TARGET_FACTOR_SHEET_THEOREM,
                "target_factor_sheet_theorem_sha256":
                    R182_TARGET_FACTOR_SHEET_THEOREM_SHA256,
            },
            "G0_G5_final_gluing": {
                "theorem": GLUING_THEOREM,
                "theorem_sha256": THEOREM_SHA256,
            },
        },
        "scope_census": {
            "Round300D_rows": EXPECTED_R300D,
            "cross_Round301_pairs": EXPECTED_CROSS,
            "B1_scope_pairs": EXPECTED_B1_SCOPE,
            "B1_accepted_pairs": EXPECTED_B1,
            "B2_accepted_pairs": EXPECTED_B2,
            "W_tail_unresolved_pairs": EXPECTED_WTAIL,
            "accepted_plus_unresolved": EXPECTED_CROSS,
            "selected_distinct_endpoint_count": EXPECTED_ENDPOINTS,
            "old_63224_component_result_reused": False,
            "conditional_DSU_result_consumed": False,
        },
        "run_census": {
            "B1_rows": commitments["b1"]["row_count"],
            "B2a_rows": commitments["b2a"]["row_count"],
            "B2b_rows": commitments["b2b"]["row_count"],
            "candidate_edge_rows": commitments["edge"]["row_count"],
            "W_tail_unresolved_rows":
                commitments["unresolved"]["row_count"],
        },
        "output_ledgers": {
            route: {
                "filename": OUTPUTS[route],
                "schema": SCHEMA + "." + route + "-ledger.v1",
                **commitments[route],
                "file_sha256": file_hashes[route],
            }
            for route in ID_FIELDS
        },
        "formal_credit_transition": {
            "formal_component_edge_credit": EXPECTED_EDGE,
            **{field: 0 for field in ZERO_FIELDS},
        },
        "strict_nonclaims": {
            "occurrence_identity_collapsed": False,
            "official_key_identity_merged": False,
            "Round301_DSU_mutated_or_reused": False,
            "old_63224_partition_used": False,
            "conditional_92696_partition_used": False,
            "maximality_claimed": False,
            "fibre_exhaustion_claimed": False,
            "global_disposition_claimed": False,
            "W_tail_rows_are_nonedges_or_exclusions": False,
        },
        "atomicity_contract": {
            "five_ledgers_staged_before_any_publication": True,
            "result_staged_before_any_publication": True,
            "ledger_batch_directory_fsynced_before_result": True,
            "result_published_no_replace_last_as_commit_marker": True,
            "output_directory_fsynced_after_result_commit": True,
            "all_six_targets_no_clobber": True,
            "result_absent_reuses_only_exact_prior_crash_ledgers": True,
            "result_present_idempotence_requires_all_six_exact": True,
            "mismatched_existing_target_left_untouched_and_rejected":
                True,
            "nlink2_crash_orphan_requires_manual_recovery": True,
            "partial_formal_promotion_permitted": False,
            "sample_run_writes_formal_outputs": False,
        },
        "required_before_edge_consumption":
            list(REQUIRED_BEFORE_EDGE_CONSUMPTION),
    }
    result["result_sha256"] = digest(result)
    validate_result_schema(result)
    return result


def build_expected_package(
    input_dir: Path,
    stage: Path,
) -> ExpectedPackage:
    """Build all expected bytes before a candidate path is touched."""
    validate_schema_snapshot()
    need(seal_ready(), "FORMAL_EXPECTED_BUILD_REQUIRES_FROZEN_PINS")
    b1_records, b2_records, unresolved_records = reconstruct_scope(
        input_dir, provisional=False
    )
    attach_r303a_rows(input_dir, b1_records, unresolved_records)
    selected = b1_records + b2_records
    r294 = load_r294(input_dir, selected)
    r295, r293, r291 = load_physical_chain(input_dir, selected)
    leaves, collars, origins, active = load_geometry(
        input_dir, selected, r291
    )
    r204 = load_r204_full_2d_lineage(input_dir, b2_records, r294)
    kernel = import_kernel(input_dir)

    sorters = {
        route: ExternalRowSorter(stage, route)
        for route in ID_FIELDS
    }
    for record in b1_records:
        lemma = build_b1_row(
            record=record,
            r294=r294,
            r295=r295,
            r293=r293,
            r291=r291,
            leaves=leaves,
            collars=collars,
            origins=origins,
            active=active,
            kernel=kernel,
        )
        edge = build_edge_row(record, "b1", [lemma])
        sorters["b1"].add(lemma)
        sorters["edge"].add(edge)
    for record in b2_records:
        b2a, b2b = build_b2_rows(
            record=record,
            lineage=r204[record["source_id"]],
            r294=r294,
            r295=r295,
            r293=r293,
            r291=r291,
            leaves=leaves,
            collars=collars,
            origins=origins,
            active=active,
            kernel=kernel,
        )
        edge = build_edge_row(record, "b2", [b2a, b2b])
        sorters["b2a"].add(b2a)
        sorters["b2b"].add(b2b)
        sorters["edge"].add(edge)
    for record in unresolved_records:
        sorters["unresolved"].add(build_unresolved_row(record))

    rows_and_commitments = {
        route: sorter.finish() for route, sorter in sorters.items()
    }
    commitments = {
        route: item[1] for route, item in rows_and_commitments.items()
    }
    need(
        commitments["b1"]["row_count"] == EXPECTED_B1
        and commitments["b2a"]["row_count"] == EXPECTED_B2
        and commitments["b2b"]["row_count"] == EXPECTED_B2
        and commitments["edge"]["row_count"] == EXPECTED_EDGE
        and commitments["unresolved"]["row_count"] == EXPECTED_WTAIL,
        "EXPECTED_OUTPUT_CENSUS",
    )
    file_hashes: dict[str, str] = {}
    for route, (rows_path, route_commitments) in (
        rows_and_commitments.items()
    ):
        output = stage / OUTPUTS[route]
        write_expected_ledger(
            output, route, rows_path, route_commitments
        )
        file_hashes[route] = file_sha256(output)
    result = exact_result(commitments, file_hashes)
    result_path = stage / OUTPUTS["result"]
    result_path.write_bytes(canonical(result) + b"\n")
    return ExpectedPackage(stage, commitments, result)


def files_equal(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    with left.open("rb") as left_stream, right.open("rb") as right_stream:
        while True:
            left_block = left_stream.read(1 << 20)
            right_block = right_stream.read(1 << 20)
            if left_block != right_block:
                return False
            if not left_block:
                return True


def immutable_file_snapshot(path: Path) -> tuple[int, ...]:
    info = os.stat(path, follow_symlinks=False)
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_uid,
        info.st_gid,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def revalidate_protected_candidate(
    *,
    candidate_dir: Path,
    expected_dir: Path,
    candidate_pins: dict[str, str],
    protected_snapshots: dict[str, tuple[int, ...]],
    phase: str,
) -> None:
    expected_names = {*OUTPUTS.values(), PRODUCER_NAME}
    need(
        set(candidate_pins) == expected_names
        and set(protected_snapshots) == expected_names,
        "PROTECTED_CANDIDATE_EXACT_PATH_SET:" + phase,
    )
    for name in sorted(expected_names):
        candidate = candidate_dir / name
        regular_single_link(
            candidate,
            "protected-candidate:" + phase + ":" + name,
        )
        need(
            candidate.resolve().parent == candidate_dir
            and immutable_file_snapshot(candidate)
            == protected_snapshots[name]
            and file_sha256(candidate) == candidate_pins[name],
            "PROTECTED_CANDIDATE_SNAPSHOT_PIN:" + phase + ":" + name,
        )
        if name != PRODUCER_NAME:
            need(
                files_equal(candidate, expected_dir / name),
                "PROTECTED_CANDIDATE_EXPECTED_BYTES:"
                + phase
                + ":"
                + name,
            )
        need(
            immutable_file_snapshot(candidate)
            == protected_snapshots[name],
            "PROTECTED_CANDIDATE_POSTREAD_SNAPSHOT:"
            + phase
            + ":"
            + name,
        )


def close_artifact(
    payload: dict[str, Any],
    closure_field: str,
) -> tuple[dict[str, Any], bytes]:
    value = dict(payload)
    value[closure_field] = digest(payload)
    return value, canonical(value) + b"\n"


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def stage_exclusive(path: Path, raw: bytes) -> Path:
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix="." + path.name + ".exclusive.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            os.fchmod(stream.fileno(), 0o644)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        return temporary
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise


def publish_exclusive(staged: Path, target: Path) -> None:
    # link(2) is the portable same-filesystem no-clobber publication primitive.
    # Unlike os.replace(), it cannot overwrite an artifact created by another
    # process between the precondition check and this commit.
    try:
        os.link(staged, target, follow_symlinks=False)
    except FileExistsError as error:
        raise VerificationError(
            "ARTIFACT_TARGET_ALREADY_EXISTS:" + target.name
        ) from error
    staged.unlink()


def commit_artifact_pair(
    formal_dir: Path,
    attack_raw: bytes,
    verification_raw: bytes,
) -> None:
    attack_target = formal_dir / ATTACK_OUTPUT
    verification_target = formal_dir / VERIFICATION_OUTPUT
    need(
        attack_target.parent == formal_dir
        and verification_target.parent == formal_dir,
        "ARTIFACT_TARGET_CONFINEMENT",
    )

    # The verification artifact is the sole pair commit marker.  Once it
    # exists, idempotence requires both exact artifacts; a missing or altered
    # attack artifact fails closed without repair.
    if os.path.lexists(verification_target):
        read_exact_atomic_fixture_target(
            verification_target,
            verification_raw,
            "idempotent-verification-artifact",
        )
        read_exact_atomic_fixture_target(
            attack_target,
            attack_raw,
            "idempotent-attack-artifact",
        )
        return

    reusable_attack = os.path.lexists(attack_target)
    if reusable_attack:
        read_exact_atomic_fixture_target(
            attack_target,
            attack_raw,
            "crash-recovery-attack-artifact",
        )

    staged_attack: Path | None = None
    staged_verification: Path | None = None
    try:
        # Both canonical byte strings are already in memory.  Stage and fsync
        # both before either formal artifact becomes visible.
        if not reusable_attack:
            staged_attack = stage_exclusive(attack_target, attack_raw)
        staged_verification = stage_exclusive(
            verification_target, verification_raw
        )
        need(
            not os.path.lexists(verification_target),
            "VERIFICATION_COMMIT_MARKER_RACED",
        )
        if reusable_attack:
            read_exact_atomic_fixture_target(
                attack_target,
                attack_raw,
                "precommit-reused-attack-artifact",
            )
        else:
            need(staged_attack is not None, "STAGED_ATTACK_ARTIFACT")
            publish_exclusive(staged_attack, attack_target)
            staged_attack = None
        fsync_directory(formal_dir)
        read_exact_atomic_fixture_target(
            attack_target,
            attack_raw,
            "pre-verification-attack-artifact",
        )
        need(
            not os.path.lexists(verification_target),
            "VERIFICATION_MUST_BE_LAST_COMMIT_MARKER",
        )
        # The verification artifact is deliberately the final commit point.
        publish_exclusive(staged_verification, verification_target)
        staged_verification = None
        fsync_directory(formal_dir)
        read_exact_atomic_fixture_target(
            attack_target,
            attack_raw,
            "committed-attack-artifact",
        )
        read_exact_atomic_fixture_target(
            verification_target,
            verification_raw,
            "committed-verification-artifact",
        )
    finally:
        for staged in (staged_attack, staged_verification):
            if staged is not None and staged.exists():
                staged.unlink()


ATOMIC_FIXTURE_LEDGER_NAMES = tuple(
    "fixture-ledger-" + str(index) + ".json"
    for index in range(5)
)
ATOMIC_FIXTURE_RESULT_NAME = "fixture-result.json"


def read_exact_atomic_fixture_target(
    target: Path,
    expected: bytes,
    label: str,
) -> tuple[int, int]:
    need(os.path.lexists(target), "ATOMIC_FIXTURE_MISSING:" + label)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(target, flags)
    except OSError as exc:
        raise VerificationError(
            "ATOMIC_FIXTURE_UNSAFE_PATH:" + label
        ) from exc
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1
            and before.st_size == len(expected)
            and before.st_size > 0,
            "ATOMIC_FIXTURE_REGULAR_SINGLE_LINK:" + label,
        )
        chunks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    path_info = os.stat(target, follow_symlinks=False)
    need(
        before.st_dev == after.st_dev == path_info.st_dev
        and before.st_ino == after.st_ino == path_info.st_ino
        and after.st_nlink == path_info.st_nlink == 1
        and b"".join(chunks) == expected,
        "ATOMIC_FIXTURE_EXACT_STABLE_BYTES:" + label,
    )
    return after.st_dev, after.st_ino


def independent_atomic_fixture_commit(
    directory: Path,
    ledger_bytes: dict[str, bytes],
    result_bytes: bytes,
) -> dict[str, Any]:
    need(
        tuple(sorted(ledger_bytes)) == tuple(sorted(
            ATOMIC_FIXTURE_LEDGER_NAMES
        ))
        and result_bytes,
        "ATOMIC_FIXTURE_INPUT_CONTRACT",
    )
    ledger_targets = {
        name: directory / name for name in ATOMIC_FIXTURE_LEDGER_NAMES
    }
    result_target = directory / ATOMIC_FIXTURE_RESULT_NAME

    if os.path.lexists(result_target):
        read_exact_atomic_fixture_target(
            result_target,
            result_bytes,
            "idempotent-result",
        )
        for name, target in ledger_targets.items():
            read_exact_atomic_fixture_target(
                target,
                ledger_bytes[name],
                "idempotent-" + name,
            )
        return {
            "mode": "SIX_EXACT_IDEMPOTENT",
            "all_five_ledgers_present_before_result": True,
            "result_absent_immediately_before_publication": False,
            "result_is_commit_marker": True,
        }

    reusable: set[str] = set()
    for name, target in ledger_targets.items():
        if not os.path.lexists(target):
            continue
        read_exact_atomic_fixture_target(
            target,
            ledger_bytes[name],
            "crash-recovery-" + name,
        )
        reusable.add(name)

    staged_ledgers: dict[str, Path] = {}
    staged_result: Path | None = None
    try:
        for name, target in ledger_targets.items():
            if name not in reusable:
                staged_ledgers[name] = stage_exclusive(
                    target,
                    ledger_bytes[name],
                )
        staged_result = stage_exclusive(result_target, result_bytes)
        need(
            not os.path.lexists(result_target),
            "ATOMIC_FIXTURE_RESULT_RACED_BEFORE_LEDGER_PUBLICATION",
        )
        for name, staged in list(staged_ledgers.items()):
            publish_exclusive(staged, ledger_targets[name])
            del staged_ledgers[name]
        fsync_directory(directory)
        for name, target in ledger_targets.items():
            read_exact_atomic_fixture_target(
                target,
                ledger_bytes[name],
                "pre-result-" + name,
            )
        pre_result_absent = not os.path.lexists(result_target)
        need(
            pre_result_absent,
            "ATOMIC_FIXTURE_RESULT_MUST_BE_LAST",
        )
        publish_exclusive(staged_result, result_target)
        staged_result = None
        fsync_directory(directory)
        read_exact_atomic_fixture_target(
            result_target,
            result_bytes,
            "committed-result",
        )
        return {
            "mode": "RECOVERED_OR_FRESH_COMMIT",
            "reused_exact_prior_crash_ledger_count": len(reusable),
            "published_missing_ledger_count":
                len(ledger_targets) - len(reusable),
            "all_five_ledgers_present_before_result": True,
            "result_absent_immediately_before_publication":
                pre_result_absent,
            "result_is_commit_marker": True,
        }
    finally:
        for staged in staged_ledgers.values():
            if staged.exists():
                staged.unlink()
        if staged_result is not None and staged_result.exists():
            staged_result.unlink()


def atomic_publication_contract_self_test() -> dict[str, Any]:
    ledger_bytes = {
        name: ("exact-" + name + "\n").encode("ascii")
        for name in ATOMIC_FIXTURE_LEDGER_NAMES
    }
    result_bytes = b"exact-result-commit-marker\n"
    with tempfile.TemporaryDirectory(
        prefix="r303b-atomic-positive."
    ) as root:
        directory = Path(root)
        orphan_name = ATOMIC_FIXTURE_LEDGER_NAMES[0]
        orphan_target = directory / orphan_name
        orphan_target.write_bytes(ledger_bytes[orphan_name])
        orphan_inode = orphan_target.stat().st_ino
        recovery = independent_atomic_fixture_commit(
            directory,
            ledger_bytes,
            result_bytes,
        )
        need(
            orphan_target.stat().st_ino == orphan_inode
            and recovery["reused_exact_prior_crash_ledger_count"] == 1
            and recovery["published_missing_ledger_count"] == 4
            and recovery["all_five_ledgers_present_before_result"] is True
            and recovery[
                "result_absent_immediately_before_publication"
            ] is True
            and all(
                read_exact_atomic_fixture_target(
                    directory / name,
                    ledger_bytes[name],
                    "positive-" + name,
                )
                for name in ATOMIC_FIXTURE_LEDGER_NAMES
            ),
            "ATOMIC_FIXTURE_POSITIVE_RECOVERY",
        )
        idempotent = independent_atomic_fixture_commit(
            directory,
            ledger_bytes,
            result_bytes,
        )
        need(
            idempotent["mode"] == "SIX_EXACT_IDEMPOTENT"
            and idempotent["result_is_commit_marker"] is True,
            "ATOMIC_FIXTURE_POSITIVE_IDEMPOTENCE",
        )
    with tempfile.TemporaryDirectory(
        prefix="r303b-artifact-pair-positive."
    ) as root:
        directory = Path(root)
        attack_raw = b"exact-attack-artifact\n"
        verification_raw = b"exact-verification-commit-marker\n"
        attack_target = directory / ATTACK_OUTPUT
        verification_target = directory / VERIFICATION_OUTPUT
        attack_target.write_bytes(attack_raw)
        orphan_inode = attack_target.stat().st_ino
        commit_artifact_pair(
            directory,
            attack_raw,
            verification_raw,
        )
        committed_inodes = (
            attack_target.stat().st_ino,
            verification_target.stat().st_ino,
        )
        need(
            attack_target.stat().st_ino == orphan_inode
            and attack_target.read_bytes() == attack_raw
            and verification_target.read_bytes() == verification_raw,
            "ARTIFACT_PAIR_CRASH_RECOVERY",
        )
        commit_artifact_pair(
            directory,
            attack_raw,
            verification_raw,
        )
        need(
            (
                attack_target.stat().st_ino,
                verification_target.stat().st_ino,
            ) == committed_inodes,
            "ARTIFACT_PAIR_SIX_EXACT_IDEMPOTENCE",
        )
    return {
        "independently_implemented_fixture": True,
        "producer_imported_or_executed": False,
        "exact_prior_crash_ledger_reused_without_inode_replacement": True,
        "four_absent_ledgers_completed": True,
        "all_five_ledgers_observed_before_result_publication": True,
        "result_absent_immediately_before_last_publication": True,
        "result_published_last_as_commit_marker": True,
        "six_exact_idempotent_replay": True,
        "exact_attack_orphan_reused_after_mid_pair_crash": True,
        "verification_artifact_published_last_as_pair_commit_marker": True,
        "two_exact_artifact_pair_idempotent_replay": True,
    }


def build_attack_artifact(
    candidate_pins: dict[str, str],
) -> tuple[dict[str, Any], bytes]:
    outcomes = attack_self_test()
    mechanisms = {
        "stale_semantic_mutation": "row closure and exact expected bytes",
        "fully_resigned_semantic_mutation":
            "independently rebuilt semantic row",
        "fully_resigned_tail_route":
            "exact FULL_2D selector and forbidden tail route",
        "fully_resigned_B2_target_selector_swap":
            "pinned Round182 target-selector sheet identity",
        "fully_resigned_B2_encoded_face_status_forgery":
            "independent Round182 face-status replay and exact encoding",
        "fully_resigned_B2_exact_join_key_injection":
            "frozen exact B2 nested join key sets",
        "fully_resigned_B1_Gamma_nested_key_injection":
            "frozen recursive B1 Gamma schema",
        "fully_resigned_edge_component_map_extra_endpoint":
            "edge dynamic endpoint maps equal the canonical pair",
        "fully_resigned_unresolved_reference_nested_key_injection":
            "frozen unresolved endpoint-reference schema",
        "fully_resigned_B2_resolved_face_sign_forgery":
            "opposite replayed resolved t-face signs",
        "fully_resigned_raw_OVERWRAP_as_direct_strict":
            "raw interval sign versus direct/absence certificate typing",
        "fully_resigned_B2_absence_axis_swap":
            "independent geometry replay and exact expected row bytes",
        "fully_resigned_B2_absence_derivative_swap":
            "independent geometry replay and exact expected row bytes",
        "fully_resigned_B2_absence_endpoint_swap":
            "absence endpoint signs must equal the resolved face sign",
        "fully_resigned_B2_face_orientation_swap":
            "target-t derivative fixes lower/upper face orientation",
        "fully_resigned_R182_theorem_reference_swap":
            "exact Round182 target-factor theorem id and content hash",
        "R182_seven_member_package_pin_replacement":
            "exact sealed Round182 seven-member package pins",
        "fully_resigned_product_equation_as_identity":
            "nominal product lineage is never target-sheet identity",
        "fully_resigned_source_sign_as_logical_bridge":
            "source sign is informational and never a logical bridge",
        "fully_resigned_closed_source_factor_requirement":
            "closed-leaf source-factor strict nonzero is not assumed",
        "fully_resigned_nominal_lineage_deletion":
            "nominal product lineage compatibility remains mandatory",
        "fully_resigned_owner_leaf_chart_box_base_area_swap":
            "exact owner/leaf/chart/box/base-area provenance join",
        "fully_resigned_B2a_physical_credit_escalation":
            "B2a analytic layer has zero physical edge credit",
        "fully_resigned_B2b_inclusion_deletion":
            "B2b physical inclusion is mandatory before edge credit",
        "fully_resigned_B2b_absence_axis_swap":
            "independent geometry replay and exact expected row bytes",
        "fully_resigned_B2b_absence_endpoint_swap":
            "absence endpoint signs must equal the resolved face sign",
        "fully_resigned_B2b_absence_newton_flag_forgery":
            "absence certificates forbid a Newton-interior flag",
        "fully_resigned_Wtail_edge_promotion":
            "W-tail remains unresolved with zero edge credit",
        "fully_resigned_corridor_shortcut":
            "corridor nonclaim and monotone-limit theorem",
        "fully_resigned_downstream_credit":
            "zero DSU/downstream credit boundary",
        "duplicate_JSON_key": "strict duplicate-key decoder",
        "gzip_header_mutation": "deterministic gzip byte equality",
        "gzip_truncation": "gzip framing and exact bytes",
        "gzip_trailing_member": "single canonical gzip member",
        "ledger_row_delete": "exact expected row census and list hash",
        "ledger_row_add": "exact expected row census and list hash",
        "ledger_row_reorder": "strict lexical row-id order and list hash",
        "ledger_row_semantic_resign":
            "independently reconstructed exact expected row bytes",
        "candidate_symlink_path_escape":
            "regular nonsymlink confined candidate paths",
        "preexisting_artifact_target_no_clobber":
            "pre-existing artifact targets remain untouched",
        "publication_race_target_no_clobber":
            "link-based publication rejects a raced target without overwrite",
        "result_present_missing_ledger_fail_closed":
            "result commit marker requires all five exact ledgers",
        "unsafe_existing_symlink_rejected":
            "O_NOFOLLOW exact-crash-ledger recovery boundary",
        "nlink2_crash_orphan_rejected":
            "recovery accepts only regular single-link prior ledgers",
        "executable_transitive_dependency_byte_substitution":
            "exact transitive executable dependency byte pins",
        "executable_dynamic_import_injection":
            "AST closure rejects __import__ and import_module calls",
        "R294B_admission_missing":
            "mandatory Round294B manifest and verification closure",
        "R294B_admission_pin_replacement":
            "exact Round294B manifest/file/object pins",
        "R294B_verification_substitution":
            "exact Round294B verification file and object closure pins",
        "R294B_admission_bypass":
            "Round294 consumption requires prior admission closure",
        "fully_resigned_result_status":
            "independently rebuilt exact result",
        "fully_resigned_result_schema":
            "frozen canonical schema snapshot",
        "fully_resigned_result_executable_graph_injection":
            "exact recursive executable import graph",
        "fully_resigned_result_input_pin_injection":
            "exact frozen result input-pin map",
        "fully_resigned_result_credit":
            "exact 44,104 edge and zero downstream transition",
    }
    need(set(outcomes) == set(mechanisms), "FORMAL_ATTACK_MATRIX_KEYS")
    rows = [
        {
            "attack_id": attack_id,
            "status": "REJECTED",
            "rejection_boundary": mechanisms[attack_id],
        }
        for attack_id in sorted(outcomes)
    ]
    payload = {
        "schema": SCHEMA + ".attack-suite.v1",
        "status": "PASS_ALL_FOCUSED_ATTACKS_REJECTED",
        "verifier_sha256": file_sha256(Path(__file__).resolve()),
        "producer_inert_sha256": FINAL_R303B_PRODUCER_SHA256,
        "schema_snapshot_sha256":
            FINAL_R303B_SCHEMA_SNAPSHOT_SHA256,
        "candidate_exact_baseline_pins":
            dict(sorted(candidate_pins.items())),
        "attack_count": len(rows),
        "rejected_count": len(rows),
        "all_attacks_rejected": all(outcomes.values()),
        "attacks": rows,
        "formal_component_edge_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_downstream_credit": 0,
    }
    need(
        len(rows) == 55 and all(outcomes.values()),
        "FORMAL_ATTACK_CENSUS",
    )
    return close_artifact(payload, "attack_suite_sha256")


def build_verification_artifact(
    candidate_pins: dict[str, str],
    expected_pins: dict[str, str],
    attack_object: dict[str, Any],
    attack_raw: bytes,
) -> tuple[dict[str, Any], bytes]:
    payload = {
        "schema": SCHEMA + ".verification.v1",
        "status": "PASS_EXACT_CACHELESS_EXPECTED_STATE",
        "verifier_sha256": file_sha256(Path(__file__).resolve()),
        "producer": {
            "filename": PRODUCER_NAME,
            "inert_byte_pin_checked": True,
            "file_sha256": FINAL_R303B_PRODUCER_SHA256,
            "imported_or_executed": False,
        },
        "candidate_exact_file_pins":
            dict(sorted(candidate_pins.items())),
        "independently_rebuilt_expected_file_pins":
            dict(sorted(expected_pins.items())),
        "all_five_ledgers_and_result_exact": (
            candidate_pins == expected_pins
        ),
        "census": {
            "B1_rows": EXPECTED_B1,
            "B2a_rows": EXPECTED_B2,
            "B2b_rows": EXPECTED_B2,
            "formal_component_edge_rows": EXPECTED_EDGE,
            "W_tail_unresolved_rows": EXPECTED_WTAIL,
        },
        "candidate_opened_only_after_full_expected_state": True,
        "schema_snapshot": {
            "frozen_sha256": FINAL_R303B_SCHEMA_SNAPSHOT_SHA256,
            "runtime_recomputed_sha256":
                COMPUTED_SCHEMA_SNAPSHOT_SHA256,
            "exact_match_checked": True,
        },
        "Round303A_seal": {
            "manifest_filename": R303A_MANIFEST,
            "manifest_sha256": R303A_MANIFEST_SHA256,
            "exact_ten_member_closure_checked": True,
        },
        "attack_suite": {
            "filename": ATTACK_OUTPUT,
            "attack_count": attack_object["attack_count"],
            "rejected_count": attack_object["rejected_count"],
            "attack_suite_sha256":
                attack_object["attack_suite_sha256"],
            "file_sha256": hashlib.sha256(attack_raw).hexdigest(),
        },
        "atomic_publication_self_test":
            atomic_publication_contract_self_test(),
        "formal_credit_boundary": {
            "formal_component_edge_credit": EXPECTED_EDGE,
            "formal_DSU_rank_reduction_credit": 0,
            "all_identity_key_union_quotient_seam_JxJy_maximality_"
            "fibre_global_disposition_credits": 0,
        },
        "result_or_ledger_modified_by_verifier": False,
    }
    need(
        candidate_pins == expected_pins,
        "VERIFICATION_EXACT_PIN_EQUALITY",
    )
    return close_artifact(payload, "verification_sha256")


def verify_candidate(
    input_dir: Path,
    candidate_dir: Path,
    *,
    no_write: bool,
) -> dict[str, Any]:
    # Security-critical order: candidate_dir is not resolved, stated or opened
    # until the complete expected package exists.
    with tempfile.TemporaryDirectory(
        dir=HERE, prefix=".r303b-verifier-expected."
    ) as stage_text:
        expected = build_expected_package(input_dir, Path(stage_text))
        resolved_candidate = candidate_dir.resolve(strict=True)
        need(
            resolved_candidate.is_dir()
            and not candidate_dir.is_symlink(),
            "CANDIDATE_DIRECTORY",
        )
        candidate_pins: dict[str, str] = {}
        expected_pins: dict[str, str] = {}
        protected_snapshots: dict[str, tuple[int, ...]] = {}
        for name in OUTPUTS.values():
            candidate = resolved_candidate / name
            regular_single_link(candidate, "candidate:" + name)
            need(
                candidate.resolve().parent == resolved_candidate,
                "CANDIDATE_PATH_CONFINEMENT:" + name,
            )
            reference = expected.directory / name
            candidate_pins[name] = file_sha256(candidate)
            expected_pins[name] = file_sha256(reference)
            need(
                candidate_pins[name] == expected_pins[name]
                and files_equal(candidate, reference),
                "EXACT_CANDIDATE_BYTES:" + name,
            )
            protected_snapshots[name] = immutable_file_snapshot(candidate)
        producer = resolved_candidate / PRODUCER_NAME
        regular_single_link(producer, "candidate:" + PRODUCER_NAME)
        need(
            producer.resolve().parent == resolved_candidate
            and file_sha256(producer) == FINAL_R303B_PRODUCER_SHA256,
            "INERT_PRODUCER_BYTE_PIN",
        )
        candidate_pins[PRODUCER_NAME] = file_sha256(producer)
        expected_pins[PRODUCER_NAME] = str(
            FINAL_R303B_PRODUCER_SHA256
        )
        protected_snapshots[PRODUCER_NAME] = immutable_file_snapshot(
            producer
        )
        attack_object, attack_raw = build_attack_artifact(
            candidate_pins
        )
        verification_object, verification_raw = (
            build_verification_artifact(
                candidate_pins,
                expected_pins,
                attack_object,
                attack_raw,
            )
        )
        if not no_write:
            formal_dir = INPUT_DIR.resolve(strict=True)
            invoked_verifier = Path(__file__).absolute()
            need(
                input_dir == INPUT_DIR
                and candidate_dir == INPUT_DIR
                and resolved_candidate == formal_dir
                and INPUT_DIR == formal_dir
                and not INPUT_DIR.is_symlink(),
                "FORMAL_WRITE_REQUIRES_EXACT_DELIVERABLES",
            )
            regular_single_link(
                invoked_verifier, "formal_Round303B_verifier"
            )
            need(
                invoked_verifier.name == VERIFIER_NAME
                and invoked_verifier.parent == formal_dir
                and invoked_verifier.resolve()
                == formal_dir / VERIFIER_NAME,
                "FORMAL_WRITE_REQUIRES_VERIFIER_IN_DELIVERABLES",
            )
            for target in (
                formal_dir / ATTACK_OUTPUT,
                formal_dir / VERIFICATION_OUTPUT,
            ):
                need(
                    target.parent == formal_dir,
                    "FORMAL_ARTIFACT_TARGET_CONFINEMENT:"
                    + target.name,
                )
            revalidate_protected_candidate(
                candidate_dir=formal_dir,
                expected_dir=expected.directory,
                candidate_pins=candidate_pins,
                protected_snapshots=protected_snapshots,
                phase="PRECOMMIT",
            )
            commit_artifact_pair(
                formal_dir,
                attack_raw,
                verification_raw,
            )
            revalidate_protected_candidate(
                candidate_dir=formal_dir,
                expected_dir=expected.directory,
                candidate_pins=candidate_pins,
                protected_snapshots=protected_snapshots,
                phase="POSTCOMMIT",
            )
        return {
            "status": "PASS_EXACT_CACHELESS_EXPECTED_STATE",
            "candidate_opened_only_after_expected_state": True,
            "five_ledger_exact_bytes": True,
            "exact_result": True,
            "formal_component_edges": EXPECTED_EDGE,
            "W_tail_unresolved": EXPECTED_WTAIL,
            "no_write": no_write,
            "attack_suite": {
                "filename": ATTACK_OUTPUT,
                "object_sha256":
                    attack_object["attack_suite_sha256"],
                "file_sha256":
                    hashlib.sha256(attack_raw).hexdigest(),
                "written": not no_write,
            },
            "verification": {
                "filename": VERIFICATION_OUTPUT,
                "object_sha256":
                    verification_object["verification_sha256"],
                "file_sha256":
                    hashlib.sha256(verification_raw).hexdigest(),
                "written": not no_write,
            },
        }


def resign_row(route: str, row: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(row)
    payload.pop("row_sha256", None)
    payload.pop(ID_FIELDS[route], None)
    return close_row(route, payload)


def sample_rows() -> dict[str, dict[str, Any]]:
    pair = ["occurrence:left", "occurrence:right"]
    zero = {field: 0 for field in ZERO_FIELDS}
    sample_member_reference = {
        "row_id": "round301-member:sample",
        "row_sha256": "0" * 64,
        "component_id": "component:sample",
        "base_root_id": "root:sample",
        "official_key_id": "official-key:sample",
        "member_kind": PRESERVED_KIND,
    }

    def nested(
        schema_path: str,
        **updates: Any,
    ) -> dict[str, Any]:
        value = {
            key: None for key in NESTED_KEY_SETS[schema_path]
        }
        value.update(updates)
        return value

    sample_source_reference = nested(
        "source_Round301_ineligible_reference",
        row_id="round301-ineligible:sample",
        row_sha256="1" * 64,
        disposition=R301_UNRESOLVED,
    )
    sample_physical_chain = nested(
        "physical_inclusion_chain",
        Round291=nested(
            "physical_inclusion_chain.Round291",
            row_id="round291:sample",
            row_sha256="2" * 64,
            physical_witness_cell_index=0,
            physical_witness_cell=nested(
                "physical_inclusion_chain.Round291.physical_witness_cell"
            ),
        ),
        Round293=nested(
            "physical_inclusion_chain.binding",
            row_id="round293:sample",
            row_sha256="3" * 64,
            binding_classification="SAMPLE",
        ),
        Round295A=nested(
            "physical_inclusion_chain.binding",
            row_id="round295a:sample",
            row_sha256="4" * 64,
            binding_classification="SAMPLE",
        ),
    )
    sample_b1_endpoint_rows = []
    sample_b2a_endpoint_rows = []
    for side in ("left", "right"):
        member = {
            **sample_member_reference,
            "row_id": "round301-member:" + side,
        }
        sample_b1_endpoint_rows.append(nested(
            "B1.endpoint_connected_side_row",
            registry_occurrence_id="occurrence:" + side,
            Round301_member_reference=member,
            connected_source_side_witness=nested(
                "B1.connected_source_side_witness"
            ),
            closure_attachment_to_Gamma=nested(
                "B1.closure_attachment_to_Gamma"
            ),
        ))
        sample_b2a_endpoint_rows.append(nested(
            "B2a.endpoint_open_region_reference",
            registry_occurrence_id="occurrence:" + side,
            Round301_member_reference=member,
        ))

    def sample_close(
        route: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        required = (
            set(ROW_KEY_SETS[route])
            - {ID_FIELDS[route], "row_sha256"}
        )
        complete = {key: payload.get(key) for key in required}
        return close_row(route, complete)

    b1 = sample_close("b1", {
        "schema": SCHEMA + ".b1-lemma-row.v1",
        "proof_path": "B1_MONOTONE_GRAPH_TWO_CONNECTED_SIDE_ATTACHMENTS",
        "theorem_id": B1_THEOREM_ID,
        "theorem_sha256": B1_LAYER_THEOREM_SHA256,
        "gluing_theorem_id": THEOREM_ID,
        "gluing_theorem_sha256": THEOREM_SHA256,
        "monotone_limit_theorem": MONOTONE_LIMIT_THEOREM,
        "monotone_limit_theorem_sha256":
            MONOTONE_LIMIT_THEOREM_SHA256,
        "source_Round301_ineligible_reference":
            deepcopy(sample_source_reference),
        "canonical_endpoint_pair": pair,
        "endpoint_connected_side_rows":
            deepcopy(sample_b1_endpoint_rows),
        "physical_inclusion_chain": deepcopy(sample_physical_chain),
        "Gamma": nested(
            "B1.Gamma",
            exact_chart_radicand_margins=nested(
                "B1.Gamma.exact_chart_radicand_margins"
            ),
        ),
        "local_side_nonempty_witnesses": nested(
            "B1.local_side_nonempty_witnesses",
            corridor_intersects_Gamma_claimed=False,
            corridor_used_as_attachment_witness=False,
        ),
        "two_sided_limit_attachment": nested(
            "B1.two_sided_limit_attachment"
        ),
        "inactive_wall_source_factor_replay": None,
        "B1_predicates": nested("B1.B1_predicates"),
        "limit_theorem_predicates": nested(
            "B1.limit_theorem_predicates"
        ),
        "formal_B1_attachment_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        **zero,
    })
    b2a = sample_close("b2a", {
        "schema": SCHEMA + ".b2a-analytic-lemma-row.v1",
        "proof_path": "B2A_R204_ANALYTIC_TARGET_GRAPH_SHEET",
        "theorem_id": B2A_THEOREM_ID,
        "theorem_sha256": B2A_LAYER_THEOREM_SHA256,
        "Round204_target_sheet_reference": {
            **nested("B2a.Round204_target_sheet_reference"),
            "existence_certification": FULL_2D_CERT,
        },
        "canonical_endpoint_pair": pair,
        "endpoint_open_region_references":
            deepcopy(sample_b2a_endpoint_rows),
        "exact_join": {
            **{
                key: None
                for key in B2A_COMMON_EXACT_JOIN_KEYS
            },
            "active_factor_semantic_mapping": (
                "ROUND204_TARGET_FACTOR_IS_ROUND182_WALL_TARGET_SELECTOR"
            ),
            "Round182_target_factor_sheet_theorem_id":
                R182_TARGET_FACTOR_SHEET_THEOREM_ID,
            "Round182_target_factor_sheet_theorem_sha256":
                R182_TARGET_FACTOR_SHEET_THEOREM_SHA256,
            "Round182_FULL_2D_unique_target_graph_checked": True,
            "Round182_replayed_target_t_derivative_sign":
                "STRICT_POSITIVE",
            "Round182_raw_lower_t_face_interval_sign":
                "STRICT_NEGATIVE",
            "Round182_raw_upper_t_face_interval_sign": "OVERWRAP",
            "Round182_replayed_lower_t_face_encoded_status": "S-",
            "Round182_replayed_upper_t_face_encoded_status": "Ap-+++_",
            "Round182_replayed_lower_t_face_certificate": {
                "kind": "STRICT",
                "raw_interval_sign": "STRICT_NEGATIVE",
                "resolved_sign": "STRICT_NEGATIVE",
                "axis": None,
                "derivative_sign": None,
                "axis_lower_sign": None,
                "axis_upper_sign": None,
                "newton_interior": None,
            },
            "Round182_replayed_upper_t_face_certificate": {
                "kind": "ABSENT",
                "raw_interval_sign": "OVERWRAP",
                "resolved_sign": "STRICT_POSITIVE",
                "axis": "p",
                "derivative_sign": "STRICT_NEGATIVE",
                "axis_lower_sign": "STRICT_POSITIVE",
                "axis_upper_sign": "STRICT_POSITIVE",
                "newton_interior": None,
            },
            "Round182_serialized_lower_t_face_status": "S-",
            "Round182_serialized_upper_t_face_status": "Ap-+++_",
            "Round182_replayed_lower_t_face_sign": "STRICT_NEGATIVE",
            "Round182_replayed_upper_t_face_sign": "STRICT_POSITIVE",
            "source_sign_join_role":
                "INFORMATIONAL_HALF_OPEN_STRENGTHENING_NOT_LOGICAL_BRIDGE",
            "nominal_product_lineage_compatibility_checked": True,
            "nominal_product_equation_used_as_sheet_identity": False,
            "product_zero_iff_target_zero_claimed": False,
            "closed_leaf_source_factor_strict_nonzero_required": False,
            "exact_owner_leaf_chart_box_base_area_join_checked": True,
            "exact_active_factor_provenance_mapping_checked": True,
        },
        "analytic_conclusion": nested("B2a.analytic_conclusion"),
        "formal_B2a_analytic_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        **zero,
    })
    b2b = sample_close("b2b", {
        "schema": SCHEMA + ".b2b-inclusion-lemma-row.v1",
        "proof_path": "B2B_R291_R293_R295A_PHYSICAL_SHEET_INCLUSION",
        "theorem_id": B2B_THEOREM_ID,
        "theorem_sha256": B2B_LAYER_THEOREM_SHA256,
        "Round182_target_factor_sheet_theorem_id":
            R182_TARGET_FACTOR_SHEET_THEOREM_ID,
        "Round182_target_factor_sheet_theorem_sha256":
            R182_TARGET_FACTOR_SHEET_THEOREM_SHA256,
        "source_B2a_row_id": b2a[ID_FIELDS["b2a"]],
        "source_B2a_row_sha256": b2a["row_sha256"],
        "canonical_endpoint_pair": pair,
        "physical_inclusion_chain": deepcopy(sample_physical_chain),
        "exact_join": {
            **{key: None for key in B2B_EXACT_JOIN_KEYS},
            **b2a["exact_join"],
            "Round291_physical_witness_graph_classification": "FULL_2D",
            "Round204_Gamma_equals_Round182_target_factor_graph": True,
            "Round291_DIRECT_witness_carries_same_Round182_target_sheet":
                True,
            "Gamma_included_via_R291_DIRECT_target_sheet_witness": True,
        },
        "formal_B2b_physical_inclusion_lemma_credit": 1,
        "formal_component_edge_credit": 0,
        **zero,
    })
    edge = sample_close("edge", {
        "schema": SCHEMA + ".component-edge-row.v1",
        "theorem_id": THEOREM_ID,
        "theorem_sha256": THEOREM_SHA256,
        "proof_path": "B1_MONOTONE_GRAPH_SIDE_ATTACHMENT",
        "source_Round301_ineligible_reference":
            deepcopy(sample_source_reference),
        "canonical_unordered_registry_occurrence_ids": pair,
        "source_lemma_references": [
            nested(
                "edge.source_lemma_reference",
                row_id=b1[ID_FIELDS["b1"]],
                row_sha256=b1["row_sha256"],
            )
        ],
        "Round301_pre_edge_components": {
            endpoint: "component:" + endpoint for endpoint in pair
        },
        "official_key_metadata": {
            endpoint: "official:" + endpoint for endpoint in pair
        },
        "formal_component_edge_credit": 1,
        "eligible_for_later_fresh_DSU_application": True,
        "old_63224_component_result_reused": False,
        "Round301_DSU_mutated_here": False,
        **zero,
    })
    unresolved = sample_close("unresolved", {
        "schema": SCHEMA + ".wtail-unresolved-row.v1",
        "source_Round301_ineligible_reference":
            deepcopy(sample_source_reference),
        "canonical_unordered_registry_occurrence_ids": pair,
        "Round303A_unresolved_endpoint_references": [
            nested(
                "unresolved.endpoint_reference",
                endpoint=endpoint,
            )
            for endpoint in pair
        ],
        "disposition": WT_DISPOSITION,
        "formal_component_edge_credit": 0,
        "nonedge_credit": 0,
        "exclusion_credit": 0,
        "eligible_for_later_fresh_DSU_application": False,
        **zero,
    })
    return {
        "b1": b1,
        "b2a": b2a,
        "b2b": b2b,
        "edge": edge,
        "unresolved": unresolved,
    }


def deterministic_gzip_bytes(value: Any) -> bytes:
    target = BytesIO()
    with gzip.GzipFile(
        filename="",
        fileobj=target,
        mode="wb",
        mtime=0,
        compresslevel=9,
    ) as stream:
        stream.write(canonical(value))
    return target.getvalue()


def validate_deterministic_gzip_bytes(raw: bytes, label: str) -> Any:
    try:
        payload = gzip.decompress(raw)
    except (OSError, EOFError) as exc:
        raise VerificationError("GZIP_FRAMING:" + label) from exc
    value = strict_json_bytes(payload, label)
    need(
        raw == deterministic_gzip_bytes(value),
        "DETERMINISTIC_GZIP_BYTES:" + label,
    )
    return value


def close_small_result(value: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(value)
    payload.pop("result_sha256", None)
    payload["result_sha256"] = digest(payload)
    return payload


def sample_full_result_schema_object() -> dict[str, Any]:
    def nested_result(
        schema_name: str,
        **updates: Any,
    ) -> dict[str, Any]:
        value = {
            key: None
            for key in RESULT_NESTED_KEY_SETS[schema_name]
        }
        value.update(updates)
        return value

    result = {key: None for key in RESULT_TOP_KEYS}
    result.update({
        "schema": SCHEMA,
        "status": "SAMPLE",
        "producer_sha256": "0" * 64,
        "seed_affects_output": False,
        "complete_formal_run": True,
        "provisional_Round303A_consumed": False,
        "input_file_pins": deepcopy(EXPECTED_RESULT_INPUT_PINS),
        "executable_runtime_closure": nested_result(
            "executable_runtime_closure",
            transitive_file_pins=dict(sorted(
                EXECUTABLE_TRANSITIVE_CLOSURE_PINS.items()
            )),
            recursive_import_graph={
                name: sorted(children)
                for name, children in sorted(
                    EXECUTABLE_IMPORT_GRAPH.items()
                )
            },
        ),
        "Round303A_seal": nested_result(
            "Round303A_seal",
            manifest_members=dict(sorted(
                R303A_SEAL_MEMBER_PINS.items()
            )),
        ),
        "Round294B_registry_builder_admission": nested_result(
            "Round294B_registry_builder_admission"
        ),
        "theorem": deepcopy(GLUING_THEOREM),
        "theorem_sha256": THEOREM_SHA256,
        "theorem_objects": {
            "B1_monotone_closure": {
                "theorem": deepcopy(B1_LAYER_THEOREM),
                "theorem_sha256": B1_LAYER_THEOREM_SHA256,
                "kernel_theorem": deepcopy(MONOTONE_LIMIT_THEOREM),
                "kernel_theorem_sha256":
                    MONOTONE_LIMIT_THEOREM_SHA256,
            },
            "B2a_FULL_2D_analytic_closure": {
                "theorem": deepcopy(B2A_LAYER_THEOREM),
                "theorem_sha256": B2A_LAYER_THEOREM_SHA256,
            },
            "B2b_target_factor_sheet_inclusion": {
                "theorem": deepcopy(B2B_LAYER_THEOREM),
                "theorem_sha256": B2B_LAYER_THEOREM_SHA256,
                "target_factor_sheet_theorem":
                    deepcopy(R182_TARGET_FACTOR_SHEET_THEOREM),
                "target_factor_sheet_theorem_sha256":
                    R182_TARGET_FACTOR_SHEET_THEOREM_SHA256,
            },
            "G0_G5_final_gluing": {
                "theorem": deepcopy(GLUING_THEOREM),
                "theorem_sha256": THEOREM_SHA256,
            },
        },
        "scope_census": nested_result("scope_census"),
        "run_census": nested_result("run_census"),
        "output_ledgers": {
            route: nested_result("output_ledger_entry")
            for route in ID_FIELDS
        },
        "formal_credit_transition": nested_result(
            "formal_credit_transition"
        ),
        "strict_nonclaims": nested_result("strict_nonclaims"),
        "atomicity_contract": nested_result("atomicity_contract"),
        "required_before_edge_consumption":
            list(REQUIRED_BEFORE_EDGE_CONSUMPTION),
    })
    result["result_sha256"] = digest({
        key: value
        for key, value in result.items()
        if key != "result_sha256"
    })
    validate_result_schema(result)
    return result


def attack_self_test() -> dict[str, Any]:
    rows = sample_rows()
    for route, row in rows.items():
        verify_expected_row(route, row)
    attacks: dict[str, bool] = {}

    stale = deepcopy(rows["unresolved"])
    stale["disposition"] = "FALSELY_PROMOTED"
    try:
        verify_expected_row("unresolved", stale)
    except VerificationError:
        attacks["stale_semantic_mutation"] = True
    else:
        attacks["stale_semantic_mutation"] = False

    resigned = deepcopy(rows["unresolved"])
    resigned["disposition"] = "FALSELY_PROMOTED"
    resigned = resign_row("unresolved", resigned)
    try:
        verify_expected_row("unresolved", resigned)
    except VerificationError:
        attacks["fully_resigned_semantic_mutation"] = True
    else:
        attacks["fully_resigned_semantic_mutation"] = False

    tail = deepcopy(rows["b2a"])
    tail["Round204_target_sheet_reference"][
        "existence_certification"
    ] = TAIL_CERT
    tail = resign_row("b2a", tail)
    try:
        verify_expected_row("b2a", tail)
    except VerificationError:
        attacks["fully_resigned_tail_route"] = True
    else:
        attacks["fully_resigned_tail_route"] = False

    factor_swap = deepcopy(rows["b2b"])
    factor_swap["exact_join"][
        "Round204_Gamma_equals_Round182_target_factor_graph"
    ] = False
    factor_swap = resign_row("b2b", factor_swap)
    try:
        verify_expected_row("b2b", factor_swap)
    except VerificationError:
        attacks["fully_resigned_B2_target_selector_swap"] = True
    else:
        attacks["fully_resigned_B2_target_selector_swap"] = False

    encoded_face = deepcopy(rows["b2a"])
    encoded_face["exact_join"][
        "Round182_replayed_upper_t_face_encoded_status"
    ] = "S+"
    encoded_face = resign_row("b2a", encoded_face)
    try:
        verify_expected_row("b2a", encoded_face)
    except VerificationError:
        attacks["fully_resigned_B2_encoded_face_status_forgery"] = True
    else:
        attacks["fully_resigned_B2_encoded_face_status_forgery"] = False

    nested_key_injection = deepcopy(rows["b2a"])
    nested_key_injection["exact_join"]["attacker_extension"] = True
    nested_key_injection = resign_row("b2a", nested_key_injection)
    try:
        verify_expected_row("b2a", nested_key_injection)
    except VerificationError:
        attacks["fully_resigned_B2_exact_join_key_injection"] = True
    else:
        attacks["fully_resigned_B2_exact_join_key_injection"] = False

    b1_gamma_injection = deepcopy(rows["b1"])
    b1_gamma_injection["Gamma"]["attacker_extension"] = True
    b1_gamma_injection = resign_row("b1", b1_gamma_injection)
    try:
        verify_expected_row("b1", b1_gamma_injection)
    except VerificationError:
        attacks["fully_resigned_B1_Gamma_nested_key_injection"] = True
    else:
        attacks["fully_resigned_B1_Gamma_nested_key_injection"] = False

    edge_map_injection = deepcopy(rows["edge"])
    edge_map_injection["Round301_pre_edge_components"][
        "occurrence:attacker"
    ] = "component:attacker"
    edge_map_injection = resign_row("edge", edge_map_injection)
    try:
        verify_expected_row("edge", edge_map_injection)
    except VerificationError:
        attacks["fully_resigned_edge_component_map_extra_endpoint"] = True
    else:
        attacks["fully_resigned_edge_component_map_extra_endpoint"] = False

    unresolved_reference_injection = deepcopy(rows["unresolved"])
    unresolved_reference_injection[
        "Round303A_unresolved_endpoint_references"
    ][0]["attacker_extension"] = True
    unresolved_reference_injection = resign_row(
        "unresolved",
        unresolved_reference_injection,
    )
    try:
        verify_expected_row("unresolved", unresolved_reference_injection)
    except VerificationError:
        attacks[
            "fully_resigned_unresolved_reference_nested_key_injection"
        ] = True
    else:
        attacks[
            "fully_resigned_unresolved_reference_nested_key_injection"
        ] = False

    resolved_face = deepcopy(rows["b2a"])
    resolved_face["exact_join"][
        "Round182_replayed_upper_t_face_sign"
    ] = "STRICT_NEGATIVE"
    resolved_face = resign_row("b2a", resolved_face)
    try:
        verify_expected_row("b2a", resolved_face)
    except VerificationError:
        attacks["fully_resigned_B2_resolved_face_sign_forgery"] = True
    else:
        attacks["fully_resigned_B2_resolved_face_sign_forgery"] = False

    false_direct = deepcopy(rows["b2a"])
    false_direct["exact_join"][
        "Round182_replayed_upper_t_face_encoded_status"
    ] = "S+"
    false_direct["exact_join"][
        "Round182_raw_upper_t_face_interval_sign"
    ] = "OVERWRAP"
    false_direct = resign_row("b2a", false_direct)
    try:
        verify_expected_row("b2a", false_direct)
    except VerificationError:
        attacks["fully_resigned_raw_OVERWRAP_as_direct_strict"] = True
    else:
        attacks["fully_resigned_raw_OVERWRAP_as_direct_strict"] = False

    for attack_id, forged_status, certificate_updates in (
        (
            "fully_resigned_B2_absence_axis_swap",
            "As-+++_",
            {"axis": "s"},
        ),
        (
            "fully_resigned_B2_absence_derivative_swap",
            "Ap++++_",
            {"derivative_sign": "STRICT_POSITIVE"},
        ),
        (
            "fully_resigned_B2_absence_endpoint_swap",
            "Ap--++_",
            {"axis_lower_sign": "STRICT_NEGATIVE"},
        ),
    ):
        forged = deepcopy(rows["b2a"])
        forged["exact_join"][
            "Round182_replayed_upper_t_face_encoded_status"
        ] = forged_status
        forged["exact_join"][
            "Round182_serialized_upper_t_face_status"
        ] = forged_status
        forged["exact_join"][
            "Round182_replayed_upper_t_face_certificate"
        ].update(certificate_updates)
        forged = resign_row("b2a", forged)
        try:
            verify_expected_row(
                "b2a",
                forged,
                trusted_expected_row=rows["b2a"],
            )
        except VerificationError:
            attacks[attack_id] = True
        else:
            attacks[attack_id] = False

    orientation_swap = deepcopy(rows["b2a"])
    for field_template in (
        "Round182_raw_{}_t_face_interval_sign",
        "Round182_replayed_{}_t_face_encoded_status",
        "Round182_replayed_{}_t_face_certificate",
        "Round182_serialized_{}_t_face_status",
        "Round182_replayed_{}_t_face_sign",
    ):
        lower_field = field_template.format("lower")
        upper_field = field_template.format("upper")
        (
            orientation_swap["exact_join"][lower_field],
            orientation_swap["exact_join"][upper_field],
        ) = (
            orientation_swap["exact_join"][upper_field],
            orientation_swap["exact_join"][lower_field],
        )
    orientation_swap = resign_row("b2a", orientation_swap)
    try:
        verify_expected_row("b2a", orientation_swap)
    except VerificationError:
        attacks["fully_resigned_B2_face_orientation_swap"] = True
    else:
        attacks["fully_resigned_B2_face_orientation_swap"] = False

    theorem_swap = deepcopy(rows["b2b"])
    theorem_swap["Round182_target_factor_sheet_theorem_id"] += "_FORGED"
    theorem_swap = resign_row("b2b", theorem_swap)
    try:
        verify_expected_row("b2b", theorem_swap)
    except VerificationError:
        attacks["fully_resigned_R182_theorem_reference_swap"] = True
    else:
        attacks["fully_resigned_R182_theorem_reference_swap"] = False

    mutated_r182_pins = dict(R182_PACKAGE_MEMBER_PINS)
    first_r182_member = min(mutated_r182_pins)
    mutated_r182_pins[first_r182_member] = "0" * 64
    attacks["R182_seven_member_package_pin_replacement"] = (
        len(mutated_r182_pins) == 7
        and mutated_r182_pins != R182_PACKAGE_MEMBER_PINS
        and mutated_r182_pins[first_r182_member]
        != R182_PACKAGE_MEMBER_PINS[first_r182_member]
    )

    product_identity = deepcopy(rows["b2a"])
    product_identity["exact_join"][
        "nominal_product_equation_used_as_sheet_identity"
    ] = True
    product_identity = resign_row("b2a", product_identity)
    try:
        verify_expected_row("b2a", product_identity)
    except VerificationError:
        attacks["fully_resigned_product_equation_as_identity"] = True
    else:
        attacks["fully_resigned_product_equation_as_identity"] = False

    source_sign_bridge = deepcopy(rows["b2a"])
    source_sign_bridge["exact_join"]["source_sign_join_role"] = (
        "LOGICAL_BRIDGE"
    )
    source_sign_bridge = resign_row("b2a", source_sign_bridge)
    try:
        verify_expected_row("b2a", source_sign_bridge)
    except VerificationError:
        attacks["fully_resigned_source_sign_as_logical_bridge"] = True
    else:
        attacks["fully_resigned_source_sign_as_logical_bridge"] = False

    closed_factor = deepcopy(rows["b2a"])
    closed_factor["exact_join"][
        "closed_leaf_source_factor_strict_nonzero_required"
    ] = True
    closed_factor = resign_row("b2a", closed_factor)
    try:
        verify_expected_row("b2a", closed_factor)
    except VerificationError:
        attacks["fully_resigned_closed_source_factor_requirement"] = True
    else:
        attacks["fully_resigned_closed_source_factor_requirement"] = False

    nominal_lineage = deepcopy(rows["b2a"])
    nominal_lineage["exact_join"][
        "nominal_product_lineage_compatibility_checked"
    ] = False
    nominal_lineage = resign_row("b2a", nominal_lineage)
    try:
        verify_expected_row("b2a", nominal_lineage)
    except VerificationError:
        attacks["fully_resigned_nominal_lineage_deletion"] = True
    else:
        attacks["fully_resigned_nominal_lineage_deletion"] = False

    owner_swap = deepcopy(rows["b2a"])
    owner_swap["exact_join"][
        "exact_owner_leaf_chart_box_base_area_join_checked"
    ] = False
    owner_swap = resign_row("b2a", owner_swap)
    try:
        verify_expected_row("b2a", owner_swap)
    except VerificationError:
        attacks[
            "fully_resigned_owner_leaf_chart_box_base_area_swap"
        ] = True
    else:
        attacks[
            "fully_resigned_owner_leaf_chart_box_base_area_swap"
        ] = False

    b2a_credit = deepcopy(rows["b2a"])
    b2a_credit["formal_component_edge_credit"] = 1
    b2a_credit = resign_row("b2a", b2a_credit)
    try:
        verify_expected_row("b2a", b2a_credit)
    except VerificationError:
        attacks["fully_resigned_B2a_physical_credit_escalation"] = True
    else:
        attacks["fully_resigned_B2a_physical_credit_escalation"] = False

    b2b_deletion = deepcopy(rows["b2b"])
    b2b_deletion["exact_join"][
        "Gamma_included_via_R291_DIRECT_target_sheet_witness"
    ] = False
    b2b_deletion = resign_row("b2b", b2b_deletion)
    try:
        verify_expected_row("b2b", b2b_deletion)
    except VerificationError:
        attacks["fully_resigned_B2b_inclusion_deletion"] = True
    else:
        attacks["fully_resigned_B2b_inclusion_deletion"] = False

    for attack_id, forged_status, certificate_updates in (
        (
            "fully_resigned_B2b_absence_axis_swap",
            "As-+++_",
            {"axis": "s"},
        ),
        (
            "fully_resigned_B2b_absence_endpoint_swap",
            "Ap--++_",
            {"axis_lower_sign": "STRICT_NEGATIVE"},
        ),
        (
            "fully_resigned_B2b_absence_newton_flag_forgery",
            "Ap-+++1",
            {"newton_interior": True},
        ),
    ):
        forged_b2b = deepcopy(rows["b2b"])
        forged_b2b["exact_join"][
            "Round182_replayed_upper_t_face_encoded_status"
        ] = forged_status
        forged_b2b["exact_join"][
            "Round182_serialized_upper_t_face_status"
        ] = forged_status
        forged_b2b["exact_join"][
            "Round182_replayed_upper_t_face_certificate"
        ].update(certificate_updates)
        forged_b2b = resign_row("b2b", forged_b2b)
        try:
            if attack_id == "fully_resigned_B2b_absence_axis_swap":
                verify_expected_row(
                    "b2b",
                    forged_b2b,
                    trusted_expected_row=rows["b2b"],
                )
            else:
                verify_expected_row("b2b", forged_b2b)
        except VerificationError:
            attacks[attack_id] = True
        else:
            attacks[attack_id] = False

    wtail_edge = deepcopy(rows["unresolved"])
    wtail_edge["formal_component_edge_credit"] = 1
    wtail_edge["eligible_for_later_fresh_DSU_application"] = True
    wtail_edge = resign_row("unresolved", wtail_edge)
    try:
        verify_expected_row("unresolved", wtail_edge)
    except VerificationError:
        attacks["fully_resigned_Wtail_edge_promotion"] = True
    else:
        attacks["fully_resigned_Wtail_edge_promotion"] = False

    corridor = deepcopy(rows["b1"])
    corridor["local_side_nonempty_witnesses"][
        "corridor_used_as_attachment_witness"
    ] = True
    corridor = resign_row("b1", corridor)
    try:
        verify_expected_row("b1", corridor)
    except VerificationError:
        attacks["fully_resigned_corridor_shortcut"] = True
    else:
        attacks["fully_resigned_corridor_shortcut"] = False

    dsu = deepcopy(rows["edge"])
    dsu["formal_DSU_rank_reduction_credit"] = 1
    dsu = resign_row("edge", dsu)
    try:
        verify_expected_row("edge", dsu)
    except VerificationError:
        attacks["fully_resigned_downstream_credit"] = True
    else:
        attacks["fully_resigned_downstream_credit"] = False

    try:
        strict_json_bytes(b'{"x":1,"x":2}', "duplicate")
    except VerificationError:
        attacks["duplicate_JSON_key"] = True
    else:
        attacks["duplicate_JSON_key"] = False

    sample_document = {
        "schema": SCHEMA + ".unresolved-ledger.v1",
        TABLES["unresolved"]: [rows["unresolved"]],
    }
    canonical_gzip = deterministic_gzip_bytes(sample_document)
    validate_deterministic_gzip_bytes(canonical_gzip, "baseline")

    mutated_header = BytesIO()
    with gzip.GzipFile(
        filename="named.json",
        fileobj=mutated_header,
        mode="wb",
        mtime=123,
        compresslevel=9,
    ) as stream:
        stream.write(canonical(sample_document))
    try:
        validate_deterministic_gzip_bytes(
            mutated_header.getvalue(), "header"
        )
    except VerificationError:
        attacks["gzip_header_mutation"] = True
    else:
        attacks["gzip_header_mutation"] = False

    try:
        validate_deterministic_gzip_bytes(
            canonical_gzip[:-3], "truncated"
        )
    except VerificationError:
        attacks["gzip_truncation"] = True
    else:
        attacks["gzip_truncation"] = False

    try:
        validate_deterministic_gzip_bytes(
            canonical_gzip + canonical_gzip, "trailing-member"
        )
    except VerificationError:
        attacks["gzip_trailing_member"] = True
    else:
        attacks["gzip_trailing_member"] = False

    second_row = deepcopy(rows["unresolved"])
    second_row["source_Round300D_row_id"] = "source:second"
    second_row = resign_row("unresolved", second_row)
    expected_rows = sorted(
        [rows["unresolved"], second_row],
        key=lambda row: row[ID_FIELDS["unresolved"]],
    )
    deleted_rows = expected_rows[:-1]
    third_row = deepcopy(rows["unresolved"])
    third_row["source_Round300D_row_id"] = "source:third"
    third_row = resign_row("unresolved", third_row)
    added_rows = [*expected_rows, third_row]
    reordered_rows = list(reversed(expected_rows))
    resigned_row_attack = deepcopy(expected_rows[0])
    resigned_row_attack["source_Round300D_row_id"] = "source:resigned"
    resigned_row_attack = resign_row("unresolved", resigned_row_attack)
    attacks["ledger_row_delete"] = digest(deleted_rows) != digest(
        expected_rows
    )
    attacks["ledger_row_add"] = digest(added_rows) != digest(expected_rows)
    attacks["ledger_row_reorder"] = digest(reordered_rows) != digest(
        expected_rows
    )
    attacks["ledger_row_semantic_resign"] = (
        canonical(resigned_row_attack) != canonical(expected_rows[0])
    )

    with tempfile.TemporaryDirectory(prefix="r303b-path-attack.") as root:
        root_path = Path(root)
        outside = root_path / "outside.json"
        outside.write_bytes(b"{}")
        candidate = root_path / "candidate.json"
        candidate.symlink_to(outside)
        try:
            regular_single_link(candidate, "path-escape")
        except VerificationError:
            attacks["candidate_symlink_path_escape"] = True
        else:
            attacks["candidate_symlink_path_escape"] = False

    with tempfile.TemporaryDirectory(
        prefix="r303b-existing-target-attack."
    ) as root:
        root_path = Path(root)
        existing_target = root_path / ATTACK_OUTPUT
        existing_bytes = b"pre-existing-artifact\n"
        existing_target.write_bytes(existing_bytes)
        try:
            commit_artifact_pair(
                root_path,
                b"attacker-replacement\n",
                b"verification\n",
            )
        except VerificationError:
            attacks["preexisting_artifact_target_no_clobber"] = (
                existing_target.read_bytes() == existing_bytes
                and not (root_path / VERIFICATION_OUTPUT).exists()
            )
        else:
            attacks["preexisting_artifact_target_no_clobber"] = False

    with tempfile.TemporaryDirectory(
        prefix="r303b-publication-race-attack."
    ) as root:
        root_path = Path(root)
        race_target = root_path / "raced-artifact.json"
        staged = stage_exclusive(race_target, b"candidate\n")
        raced_bytes = b"concurrent-winner\n"
        race_target.write_bytes(raced_bytes)
        try:
            publish_exclusive(staged, race_target)
        except VerificationError:
            attacks["publication_race_target_no_clobber"] = (
                race_target.read_bytes() == raced_bytes
                and staged.exists()
                and staged.read_bytes() == b"candidate\n"
            )
        else:
            attacks["publication_race_target_no_clobber"] = False
        finally:
            if staged.exists():
                staged.unlink()

    fixture_ledgers = {
        name: ("exact-" + name + "\n").encode("ascii")
        for name in ATOMIC_FIXTURE_LEDGER_NAMES
    }
    fixture_result = b"exact-result-commit-marker\n"

    with tempfile.TemporaryDirectory(
        prefix="r303b-result-missing-ledger-attack."
    ) as root:
        root_path = Path(root)
        result_target = root_path / ATOMIC_FIXTURE_RESULT_NAME
        result_target.write_bytes(fixture_result)
        try:
            independent_atomic_fixture_commit(
                root_path,
                fixture_ledgers,
                fixture_result,
            )
        except VerificationError:
            attacks["result_present_missing_ledger_fail_closed"] = (
                result_target.read_bytes() == fixture_result
                and all(
                    not os.path.lexists(root_path / name)
                    for name in ATOMIC_FIXTURE_LEDGER_NAMES
                )
            )
        else:
            attacks["result_present_missing_ledger_fail_closed"] = False

    with tempfile.TemporaryDirectory(
        prefix="r303b-existing-symlink-attack."
    ) as root:
        root_path = Path(root)
        first_name = ATOMIC_FIXTURE_LEDGER_NAMES[0]
        outside = root_path / "outside-ledger.json"
        outside.write_bytes(fixture_ledgers[first_name])
        symlink_target = root_path / first_name
        symlink_target.symlink_to(outside.name)
        try:
            independent_atomic_fixture_commit(
                root_path,
                fixture_ledgers,
                fixture_result,
            )
        except VerificationError:
            attacks["unsafe_existing_symlink_rejected"] = (
                symlink_target.is_symlink()
                and outside.read_bytes() == fixture_ledgers[first_name]
                and not os.path.lexists(
                    root_path / ATOMIC_FIXTURE_RESULT_NAME
                )
                and all(
                    not os.path.lexists(root_path / name)
                    for name in ATOMIC_FIXTURE_LEDGER_NAMES[1:]
                )
            )
        else:
            attacks["unsafe_existing_symlink_rejected"] = False

    with tempfile.TemporaryDirectory(
        prefix="r303b-nlink2-orphan-attack."
    ) as root:
        root_path = Path(root)
        first_name = ATOMIC_FIXTURE_LEDGER_NAMES[0]
        first_target = root_path / first_name
        first_target.write_bytes(fixture_ledgers[first_name])
        hardlink_alias = root_path / "crash-stage-hardlink.tmp"
        os.link(first_target, hardlink_alias)
        try:
            independent_atomic_fixture_commit(
                root_path,
                fixture_ledgers,
                fixture_result,
            )
        except VerificationError:
            attacks["nlink2_crash_orphan_rejected"] = (
                first_target.stat().st_nlink == 2
                and hardlink_alias.stat().st_ino
                == first_target.stat().st_ino
                and not os.path.lexists(
                    root_path / ATOMIC_FIXTURE_RESULT_NAME
                )
                and all(
                    not os.path.lexists(root_path / name)
                    for name in ATOMIC_FIXTURE_LEDGER_NAMES[1:]
                )
            )
        else:
            attacks["nlink2_crash_orphan_rejected"] = False

    with tempfile.TemporaryDirectory(
        prefix="r303b-executable-byte-attack."
    ) as root:
        dependency = Path(root) / "cm2_fixture_dependency.py"
        original_source = b"value = 1\n"
        substituted_source = b"value = 2\n"
        dependency.write_bytes(substituted_source)
        try:
            read_pinned_executable(
                dependency,
                hashlib.sha256(original_source).hexdigest(),
                dependency.name,
            )
        except VerificationError:
            attacks[
                "executable_transitive_dependency_byte_substitution"
            ] = (
                len(original_source) == len(substituted_source)
                and dependency.read_bytes() == substituted_source
            )
        else:
            attacks[
                "executable_transitive_dependency_byte_substitution"
            ] = False

    dynamic_rejections: list[bool] = []
    for index, source in enumerate((
        b"module = __import__('cm2_attacker')\n",
        b"module = importlib.import_module('cm2_attacker')\n",
    )):
        try:
            executable_local_imports(
                source,
                "dynamic-attack-" + str(index) + ".py",
            )
        except VerificationError:
            dynamic_rejections.append(True)
        else:
            dynamic_rejections.append(False)
    attacks["executable_dynamic_import_injection"] = all(
        dynamic_rejections
    )

    actual_r294b = read_json(INPUT_DIR / R294B_VERIFICATION)

    def resign_r294b(value: dict[str, Any]) -> dict[str, Any]:
        resigned_value = deepcopy(value)
        resigned_value.pop("verification_sha256", None)
        resigned_value["verification_sha256"] = digest(resigned_value)
        return resigned_value

    missing_r294b = deepcopy(actual_r294b)
    missing_r294b.pop("attack_audit")
    replaced_r294b = deepcopy(actual_r294b)
    replaced_r294b["candidate_artifacts"]["producer_sha256"] = "0" * 64
    substituted_r294b_verification = deepcopy(actual_r294b)
    substituted_r294b_verification["candidate_artifacts"][
        "verifier_sha256"
    ] = "f" * 64
    bypassed_r294b = deepcopy(actual_r294b)
    bypassed_r294b["strict_nonpromotion"][
        "post_Round294_expanded_registry_component_DSU_status"
    ] = "REBUILT"
    bypassed_r294b["strict_nonpromotion"][
        "post_Round294_quotient_component_count"
    ] = 1
    for attack_id, forged_r294b in (
        ("R294B_admission_missing", missing_r294b),
        ("R294B_admission_pin_replacement", replaced_r294b),
        (
            "R294B_verification_substitution",
            substituted_r294b_verification,
        ),
        ("R294B_admission_bypass", bypassed_r294b),
    ):
        try:
            validate_r294b_verification_object(
                resign_r294b(forged_r294b)
            )
        except VerificationError:
            attacks[attack_id] = True
        else:
            attacks[attack_id] = False

    full_result = sample_full_result_schema_object()
    result_graph_injection = deepcopy(full_result)
    result_graph_injection["executable_runtime_closure"][
        "recursive_import_graph"
    ]["cm2_attacker.py"] = []
    result_graph_injection = close_small_result(result_graph_injection)
    try:
        validate_result_schema(result_graph_injection)
    except VerificationError:
        attacks["fully_resigned_result_executable_graph_injection"] = True
    else:
        attacks["fully_resigned_result_executable_graph_injection"] = False

    result_input_pin_injection = deepcopy(full_result)
    result_input_pin_injection["input_file_pins"][
        "cm2_attacker.py"
    ] = "0" * 64
    result_input_pin_injection = close_small_result(
        result_input_pin_injection
    )
    try:
        validate_result_schema(result_input_pin_injection)
    except VerificationError:
        attacks["fully_resigned_result_input_pin_injection"] = True
    else:
        attacks["fully_resigned_result_input_pin_injection"] = False

    baseline_result = close_small_result({
        "schema": SCHEMA,
        "status": "PASS",
        "formal_credit_transition": {
            "formal_component_edge_credit": EXPECTED_EDGE,
            **{field: 0 for field in ZERO_FIELDS},
        },
    })
    baseline_result_bytes = canonical(baseline_result) + b"\n"

    resigned_status = deepcopy(baseline_result)
    resigned_status["status"] = "FALSE_PASS"
    resigned_status = close_small_result(resigned_status)
    attacks["fully_resigned_result_status"] = (
        canonical(resigned_status) + b"\n" != baseline_result_bytes
    )

    resigned_schema = deepcopy(baseline_result)
    resigned_schema["schema"] = SCHEMA + ".attacker"
    resigned_schema = close_small_result(resigned_schema)
    attacks["fully_resigned_result_schema"] = (
        canonical(resigned_schema) + b"\n" != baseline_result_bytes
    )

    resigned_credit = deepcopy(baseline_result)
    resigned_credit["formal_credit_transition"][
        "formal_DSU_rank_reduction_credit"
    ] = 1
    resigned_credit = close_small_result(resigned_credit)
    attacks["fully_resigned_result_credit"] = (
        canonical(resigned_credit) + b"\n" != baseline_result_bytes
    )
    need(all(attacks.values()), "ATTACK_SELF_TEST:" + repr(attacks))
    return dict(sorted(attacks.items()))


def full_b2_join_self_test(input_dir: Path) -> dict[str, Any]:
    b2_records = reconstruct_b2_scope(input_dir)
    r294 = load_r294(input_dir, b2_records)
    r295, r293, r291 = load_physical_chain(input_dir, b2_records)
    leaves, collars, origins, active = load_geometry(
        input_dir, b2_records, r291
    )
    lineage = load_r204_full_2d_lineage(
        input_dir, b2_records, r294
    )
    kernel = import_kernel(input_dir)
    rows = [
        build_b2_rows(
            record=record,
            lineage=lineage[record["source_id"]],
            r294=r294,
            r295=r295,
            r293=r293,
            r291=r291,
            leaves=leaves,
            collars=collars,
            origins=origins,
            active=active,
            kernel=kernel,
        )
        for record in b2_records
    ]
    need(
        len(rows) == EXPECTED_B2
        and all(
            pair[0]["Round204_target_sheet_reference"][
                "existence_certification"
            ] == FULL_2D_CERT
            for pair in rows
        ),
        "B2_FULL_JOIN_SELF_TEST",
    )
    return {
        "B2a_FULL_2D_rows": len(rows),
        "B2b_physical_join_rows": len(rows),
        "tail_rows_accepted": 0,
        "formal_promotion": False,
    }


def reconstruct_b2_scope(input_dir: Path) -> list[dict[str, Any]]:
    """Rebuild the 192 preserved route without opening any Round303A file."""
    validate_base_boundary(input_dir)
    records: dict[str, dict[str, Any]] = {}
    endpoints: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    for row in iter_array(
        input_dir / R300D, "canonical_incidence_edge_rows"
    ):
        left = row["left_endpoint"]
        right = row["right_endpoint"]
        tranche = (
            left["registry_entry_kind"]
            + "|"
            + right["registry_entry_kind"]
        )
        if tranche != PRESERVED_KIND + "|" + PRESERVED_KIND:
            continue
        row_id = row[
            "Round300D_lower_physical_witness_incidence_edge_row_id"
        ]
        verify_row(row, row_id)
        pair = canonical_pair(
            row["canonical_unordered_Round294_registry_occurrence_ids"],
            row_id,
        )
        need(
            [left["registry_occurrence_id"], right["registry_occurrence_id"]]
            == list(pair)
            and row_id not in records
            and row["formal_component_edge_credit"] == 0
            and row["eligible_for_component_DSU_application"] is False,
            "B2_SCOPE_R300D:" + row_id,
        )
        need(pair not in pairs, "B2_SCOPE_UNIQUE_CANONICAL_PAIR")
        pairs.add(pair)
        records[row_id] = {
            "source_id": row_id,
            "source_sha256": row["row_sha256"],
            "pair": pair,
            "tranche": tranche,
            "endpoint_refs": {
                endpoint["registry_occurrence_id"]: {
                    "row_id":
                        endpoint["Round294_occurrence_registry_row_id"],
                    "row_sha256": endpoint[
                        "Round294_occurrence_registry_row_sha256"
                    ],
                    "kind": endpoint["registry_entry_kind"],
                    "chart": endpoint["physical_support_chart"],
                    "official_key_id":
                        endpoint["final_Round299A_official_key_id"],
                    "official_key_ordinal": endpoint[
                        "final_Round299A_official_key_ordinal"
                    ],
                    "signature_sha256": endpoint[
                        "complete_10_field_return_signature_sha256"
                    ],
                }
                for endpoint in (left, right)
            },
            "r295_ids": list(
                row[
                    "source_Round295A_physical_incidence_binding_row_ids"
                ]
            ),
            "r295_hashes": list(
                row[
                    "source_Round295A_physical_incidence_binding_row_sha256s"
                ]
            ),
            "r291_ids": list(
                row["source_Round291_local_disposition_row_ids"]
            ),
            "cell_indices": list(row["physical_witness_cell_indices"]),
            "source_charts": list(row["source_charts"]),
            "witness_kind_histogram": dict(
                row["witness_kind_histogram"]
            ),
            "witness_multiplicity": row["witness_multiplicity"],
        }
        endpoints.update(pair)
    need(
        len(records) == EXPECTED_B2
        and len(pairs) == EXPECTED_B2
        and len(endpoints) == 2 * EXPECTED_B2,
        "B2_SCOPE_R300D_CENSUS",
    )

    members: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_dir / R301_MEMBERS, "rows"):
        endpoint = row.get("registry_or_frontier_member_id")
        if endpoint not in endpoints:
            continue
        verify_row(row, str(endpoint))
        need(
            endpoint not in members
            and row["formal_component_membership_credit"] == 1
            and row["member_identity_preserved"] is True,
            "B2_SCOPE_R301_MEMBER:" + str(endpoint),
        )
        members[str(endpoint)] = {
            "row_id": row["Round301_member_to_component_row_id"],
            "row_sha256": row["row_sha256"],
            "component_id": row["final_Round301_component_id"],
            "base_root_id": row["base_component_root_id"],
            "official_key_id": row["official_key_id"],
            "member_kind": row["member_kind"],
        }
    need(set(members) == endpoints, "B2_SCOPE_MEMBER_COVERAGE")

    wanted = set(records)
    ineligible: dict[str, dict[str, Any]] = {}
    for row in iter_array(input_dir / R301_INELIGIBLE, "rows"):
        source_id = row.get("source_row_id")
        if (
            row.get("source_relation") != R301_SOURCE_RELATION
            or source_id not in wanted
        ):
            continue
        verify_row(row, str(source_id))
        record = records[str(source_id)]
        need(
            source_id not in ineligible
            and row["source_row_sha256"] == record["source_sha256"]
            and canonical_pair(
                row["canonical_occurrence_endpoint_pair"],
                str(source_id),
            ) == record["pair"]
            and row["disposition"] == R301_UNRESOLVED
            and row["source_row_fed_to_DSU"] is False
            and row["formal_component_edge_application_credit"] == 0,
            "B2_SCOPE_R301_INELIGIBLE:" + str(source_id),
        )
        ineligible[str(source_id)] = {
            "row_id":
                row["Round301_ineligible_source_consumption_row_id"],
            "row_sha256": row["row_sha256"],
            "disposition": row["disposition"],
        }
    need(set(ineligible) == wanted, "B2_SCOPE_INELIGIBLE_COVERAGE")

    output: list[dict[str, Any]] = []
    for source_id in sorted(records):
        record = records[source_id]
        left, right = record["pair"]
        need(
            members[left]["component_id"]
            != members[right]["component_id"],
            "B2_SCOPE_CROSS_ROUND301:" + source_id,
        )
        record["member_refs"] = {
            endpoint: members[endpoint] for endpoint in record["pair"]
        }
        record["r301_ineligible_ref"] = ineligible[source_id]
        output.append(record)
    need(len(output) == EXPECTED_B2, "B2_SCOPE_FINAL_CENSUS")
    return output


def theorem_self_test() -> dict[str, str]:
    hashes = {
        "B1_layer": digest(B1_LAYER_THEOREM),
        "B1_monotone_kernel": digest(MONOTONE_LIMIT_THEOREM),
        "B2a_FULL_2D_layer": digest(B2A_LAYER_THEOREM),
        "B2b_identity_lift_layer": digest(B2B_LAYER_THEOREM),
        "G0_G5_gluing": digest(GLUING_THEOREM),
    }
    need(
        hashes["B1_layer"] == B1_LAYER_THEOREM_SHA256
        and hashes["B1_monotone_kernel"]
        == MONOTONE_LIMIT_THEOREM_SHA256
        and hashes["B2a_FULL_2D_layer"]
        == B2A_LAYER_THEOREM_SHA256
        and hashes["B2b_identity_lift_layer"]
        == B2B_LAYER_THEOREM_SHA256
        and hashes["G0_G5_gluing"] == THEOREM_SHA256,
        "THEOREM_CONTENT_HASH_SELF_TEST",
    )
    return hashes


def scope_summary(
    routes: tuple[
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
    ],
) -> dict[str, Any]:
    b1, b2, unresolved = routes
    all_records = b1 + b2 + unresolved
    return {
        "B1_rows": len(b1),
        "B2a_rows": len(b2),
        "B2b_rows": len(b2),
        "candidate_edge_rows": len(b1) + len(b2),
        "W_tail_unresolved_rows": len(unresolved),
        "cross_Round301_pairs": len(all_records),
        "distinct_endpoint_count": len({
            endpoint
            for record in all_records
            for endpoint in record["pair"]
        }),
        "source_Round300D_row_ids_sha256": digest(
            sorted(record["source_id"] for record in all_records)
        ),
        "canonical_pairs_sha256": digest(
            sorted([list(record["pair"]) for record in all_records])
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=INPUT_DIR)
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--full-b2-self-test", action="store_true")
    parser.add_argument("--provisional-scope", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    need(
        args.self_test
        or args.full_b2_self_test
        or args.provisional_scope
        or args.preflight_only
        or args.candidate_dir is not None,
        "CHOOSE_OPERATION",
    )
    output: dict[str, Any] = {
        "schema": (
            "cm2.round303b.independent-verifier-readiness-candidate.v1"
        ),
        "formal_promotion_authorized": False,
        "producer_imported_or_executed": False,
        "R303B_result_consumed_as_truth": False,
    }
    if args.self_test:
        validate_base_boundary(args.input_dir)
        validate_schema_snapshot()
        output["self_test"] = {
            "theorem_content_hashes": theorem_self_test(),
            "R204_selector": r204_selector_self_test(args.input_dir),
            "attack_framework": attack_self_test(),
            "status": "PASS_DEVELOPMENT_SELF_TEST",
        }
    if args.preflight_only:
        validate_base_boundary(args.input_dir)
        validate_r303a_formal_boundary(args.input_dir)
        validate_schema_snapshot()
        output["preflight"] = {
            "base_pins_and_manifests": "PASS",
            "Round303A_exact_ten_member_seal": "PASS",
            "Round303A_manifest_sha256": R303A_MANIFEST_SHA256,
            "theorem_content_hashes": theorem_self_test(),
            "R204_selector": r204_selector_self_test(args.input_dir),
            "candidate_opened": False,
            "R303B_final_schema_pins_ready": seal_ready(),
            "schema_snapshot": {
                "frozen_sha256":
                    FINAL_R303B_SCHEMA_SNAPSHOT_SHA256,
                "runtime_recomputed_sha256":
                    COMPUTED_SCHEMA_SNAPSHOT_SHA256,
                "exact_match_checked": True,
            },
            "status": (
                "PASS_FORMAL_BOUNDARY_PREFLIGHT__READY_FOR_EXACT_BUILD"
                if seal_ready()
                else (
                    "PASS_R303A_AND_BASE_PREFLIGHT__"
                    "R303B_FINAL_PRODUCER_SCHEMA_STILL_FAIL_CLOSED"
                )
            ),
        }
    if args.provisional_scope:
        routes = reconstruct_scope(args.input_dir, provisional=True)
        output["provisional_scope"] = {
            **scope_summary(routes),
            "status": "PROVISIONAL_R303A_SCOPE_ONLY__ZERO_FORMAL_CREDIT",
            "candidate_opened": False,
        }
    if args.full_b2_self_test:
        output["full_b2_self_test"] = full_b2_join_self_test(
            args.input_dir
        )
    if args.candidate_dir is not None:
        output["candidate_verification"] = verify_candidate(
            args.input_dir,
            args.candidate_dir,
            no_write=args.no_write,
        )
    output["formal_boundary_ready"] = seal_ready()
    output["Round303A_seal_ready"] = r303a_seal_ready()
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
