#!/usr/bin/env python3
"""Independent verifier for the Round211 local owner materialization.

The verifier treats the producer as inert pinned bytes.  Before opening the
Round211 certificate it independently reconstructs the complete expected
result from the pinned Round173 rule and Round208 producer/certificate rows.
It neither imports nor executes the Round211 producer or Round209 probe.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round211_source_g_outgoing_half_open_owner_materialization"
PRODUCER = f"{PREFIX}.py"
CERTIFICATE = f"{PREFIX}_certificate.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"
SCHEMA = "cm2.round211.source-g-outgoing-half-open-owner-materialization.v1"
VERIFICATION_SCHEMA = (
    "cm2.round211.source-g-outgoing-half-open-owner-materialization."
    "verification.v1"
)
STATUS = (
    "CERTIFIED_LOCAL_SOURCE_G_OUTGOING_W_HALF_OPEN_OWNER_LINEAGES__"
    "NO_GLOBAL_COMPONENT_OR_EXACT_KEY_DISPOSITION"
)
PASS_STATUS = "PASS_PARTIAL_FORMAL_ROUND211"
MAX_INPUT_BYTES = 300 * 1024 * 1024

PRODUCER_SHA256 = (
    "9e8874672150d7585316524a7724070f4543e231de5481d1c1dfbd00ddc65a02"
)
CERTIFICATE_SHA256 = (
    "bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"
)
CERTIFICATE_RESULT_SHA256 = (
    "3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b"
)

R209_SOURCE = "cm2_round209_source_g_outgoing_half_open_owner_probe.py"
R209_REPORT = "cm2_round209_source_g_outgoing_half_open_owner_spike_report.md"
R209_SOURCE_SHA256 = (
    "dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f"
)
R209_REPORT_SHA256 = (
    "7501e73fdad0c3721ed70b73226a4c3a4f7288f9b8429a553a50dde725812524"
)
R209_RESULT_SHA256 = (
    "7bb2117148571c23432ab8bbee86107fdadc3198c61628b2f8a46760be91a120"
)
R209_DOCUMENT_SHA256 = (
    "d561ad855ff22b067f5ac997941a0cc96ba53d368ba6dcaa303c6d6d5672471d"
)
R173_SOURCE = "cm2_round173_source_g_exact_return_signature_transport.py"
R173_CERTIFICATE = (
    "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
)
R173_SOURCE_SHA256 = (
    "bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f"
)
R173_CERTIFICATE_SHA256 = (
    "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a"
)
R173_RESULT_SHA256 = (
    "948ab0a8539b08adc96c9493de415b44a5ffb75a1ee3ef47a4742902c211c11f"
)
R173_SCHEMA = "cm2.round173.source-g-exact-return-signature-transport.v1"
R195_SOURCE = "cm2_round195_source_g_outgoing_assembly_and_u2_order_probe.py"
R195_REPORT = (
    "cm2_round195_source_g_outgoing_assembly_and_u2_order_spike_report.md"
)
R195_SOURCE_SHA256 = (
    "f70734937ed2630f4357b9e1d860e862c1a932c573c1f93c45788cd5697ee4e1"
)
R195_REPORT_SHA256 = (
    "2f4318f381b79c28c457ce3e2f54e0b6e843c649738789c6d0f95dc8a6332dac"
)
R195_RESULT_SHA256 = (
    "bc1a983b5acab0b3a41c9c5941a77313a80d4376932b41ea31e3aabeed96511b"
)
R195_DOCUMENT_SHA256 = (
    "5ddd98453bf313b2cbed862aa5ca05bef76ba542750beaba75259a41415454a0"
)
R195_FACE_ROWS_SHA256 = (
    "0efb78285bc7836c84860f157ab4ec45593029aa523a95fd62171d307d7a5396"
)
R195_LEAF_ROWS_SHA256 = (
    "0370fb57e9d2881a8bc2d0e66351a6c551e147d483558c682f051153924f88b5"
)
R195_U2_ROWS_SHA256 = (
    "12fbc70f82645ae2ad252b4e88587a7841814a03fda1972a0241cd63c45d6ee0"
)
R208_SOURCE = "cm2_round208_source_g_outgoing_direct_signature_materialization.py"
R208_CERTIFICATE = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization"
    "_certificate.json"
)
R208_SOURCE_SHA256 = (
    "c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913"
)
R208_CERTIFICATE_SHA256 = (
    "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"
)
R208_RESULT_SHA256 = (
    "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8"
)
R208_SCHEMA = (
    "cm2.round208.source-g-outgoing-direct-signature-materialization.v1"
)
R208_STATUS = (
    "CERTIFIED_LOCAL_SOURCE_G_OUTGOING_W_DIRECT_SIGNATURE_ROWS__"
    "NO_LOWER_DIMENSIONAL_OR_GLOBAL_EXACT_KEY_DISPOSITION"
)

EXPECTED_LEAVES = 18_324
EXPECTED_EMPTY_LEAVES = 608
EXPECTED_SHEETS = 17_716
EXPECTED_CURVES = 20_456
EXPECTED_ENDPOINTS = 40_912
EXPECTED_STRICT_REGIONS = 36_040
EXPECTED_U2_SHEETS = 88
EXPECTED_U2_ORIGINS = 76
EXPECTED_U2_CURVES = 164
EXPECTED_U2_ENDPOINTS = 328
EXPECTED_SOURCE_G_EXACT_KEYS = 224_580
EXPECTED_PROBE_SHEET_ROWS_SHA256 = (
    "be4955bf1d705ffd8730505b8407a05a220940d5b76878a9a7059a5df762289a"
)
EXPECTED_PROBE_CURVE_ROWS_SHA256 = (
    "a3e375fc26afa4df3db6e8fd4b07e4bc4f97d91c9eceb6893e29ffe4ce89422e"
)
EXPECTED_PROBE_ENDPOINT_ROWS_SHA256 = (
    "23eee8138694f9b53436a66740da7801146877a62ee2b8b2fce6e2cfc36e916b"
)
EXPECTED_FORMAL_SHEET_ROWS_SHA256 = (
    "ed26068a92d4ed74f54cd724680da5bc9cafa811d553415380999ae69ea7fdeb"
)
EXPECTED_FORMAL_CURVE_ROWS_SHA256 = (
    "3d93dd7860c1025bb68acf3568a0b4b66e3106189776aae4bafa12d3902a8522"
)
EXPECTED_FORMAL_ENDPOINT_ROWS_SHA256 = (
    "e5466d386b45ea8ab473a8483b5a90a244592491cdb9ecbcdf01b7a40c87d712"
)

STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
OPPOSITE_SIGN = {
    "STRICT_NEGATIVE": "STRICT_POSITIVE",
    "STRICT_POSITIVE": "STRICT_NEGATIVE",
}
CELL_SIGNS = {
    "E": ("STRICT_POSITIVE", "STRICT_POSITIVE"),
    "W": ("STRICT_NEGATIVE", "STRICT_NEGATIVE"),
    "N": ("STRICT_POSITIVE", "STRICT_NEGATIVE"),
    "S": ("STRICT_NEGATIVE", "STRICT_POSITIVE"),
}
SIGN_CELL = {value: key for key, value in CELL_SIGNS.items()}


class Round211VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round211VerificationError(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_number(token: str) -> None:
    raise Round211VerificationError(f"noninteger JSON number:{token}")


def validate_tree(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (bool, str, int)):
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            validate_tree(child, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, child in value.items():
            require(isinstance(key, str), f"nonstring key:{path}")
            validate_tree(child, f"{path}.{key}")
        return
    raise Round211VerificationError(f"forbidden JSON type:{path}")


def strict_json(
    raw: bytes,
    label: str,
    maximum: int,
    *,
    canonical_required: bool = True,
) -> dict[str, Any]:
    require(0 < len(raw) <= maximum, f"{label} size")
    require(not raw.startswith(b"\xef\xbb\xbf"), f"{label} BOM")
    require(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), f"{label} newline")
    try:
        text = raw[:-1].decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise Round211VerificationError(f"{label} UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=unique_pairs,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (json.JSONDecodeError, ValueError) as error:
        raise Round211VerificationError(f"{label} JSON") from error
    require(isinstance(value, dict), f"{label} root")
    validate_tree(value)
    if canonical_required:
        require(canonical_bytes(value) == raw[:-1], f"{label} canonical")
    return value


def regular_bytes(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(before.st_nlink == 1, f"hardlink:{path.name}")
    require(0 < before.st_size <= maximum, f"size:{path.name}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        require(
            (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            )
            == (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ),
            f"stable-open:{path.name}",
        )
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            require(total <= maximum, f"bounded-read:{path.name}")
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
            (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
            == (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            ),
            f"stable-read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def pinned(path: Path, expected: str, maximum: int) -> bytes:
    raw = regular_bytes(path, maximum)
    require(hashlib.sha256(raw).hexdigest() == expected, f"SHA256:{path.name}")
    return raw


def validate_closed_rows(
    rows: list[dict[str, Any]],
    expected_count: int,
    expected_digest: str,
    id_key: str,
    label: str,
) -> None:
    require(len(rows) == expected_count, f"{label} count")
    require(
        len({row[id_key] for row in rows}) == expected_count,
        f"{label} unique IDs",
    )
    require(digest(rows) == expected_digest, f"{label} digest")
    for row in rows:
        payload = dict(row)
        row_sha256 = payload.pop("row_sha256")
        require(digest(payload) == row_sha256, f"{label} row closure")


def unwrap(raw: bytes, schema: str, result_sha256: str, label: str) -> dict[str, Any]:
    envelope = strict_json(
        raw,
        label,
        MAX_INPUT_BYTES,
        canonical_required=False,
    )
    require(
        set(envelope) == {"schema", "result", "result_sha256"}
        and envelope["schema"] == schema
        and envelope["result_sha256"] == result_sha256
        and digest(envelope["result"]) == result_sha256,
        f"{label} envelope",
    )
    return envelope["result"]


def load_formal_inputs() -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    pinned(HERE / PRODUCER, PRODUCER_SHA256, 5_000_000)
    pinned(HERE / R209_SOURCE, R209_SOURCE_SHA256, 5_000_000)
    pinned(HERE / R209_REPORT, R209_REPORT_SHA256, 5_000_000)
    pinned(HERE / R173_SOURCE, R173_SOURCE_SHA256, 5_000_000)
    r173 = unwrap(
        pinned(
            HERE / R173_CERTIFICATE,
            R173_CERTIFICATE_SHA256,
            5_000_000,
        ),
        R173_SCHEMA,
        R173_RESULT_SHA256,
        "Round173",
    )
    rule = r173["outgoing_chart_contract"]
    require(
        rule["diagonal_seam_rule"] == "E or W owns; N or S excludes"
        and rule["owner_set"] == ["E", "W"]
        and rule["duplicate_trace_is_identified_not_added"] is True
        and rule["owner_set_is_invariant_under_Jx_and_Jy"] is True,
        "Round173 half-open rule",
    )
    pinned(HERE / R195_SOURCE, R195_SOURCE_SHA256, 5_000_000)
    pinned(HERE / R195_REPORT, R195_REPORT_SHA256, 5_000_000)
    pinned(HERE / R208_SOURCE, R208_SOURCE_SHA256, 5_000_000)
    r208 = unwrap(
        pinned(
            HERE / R208_CERTIFICATE,
            R208_CERTIFICATE_SHA256,
            MAX_INPUT_BYTES,
        ),
        R208_SCHEMA,
        R208_RESULT_SHA256,
        "Round208",
    )
    require(
        r208["status"] == R208_STATUS
        and r208["provenance"]["producer_sha256"] == R208_SOURCE_SHA256
        and r208["formal_scope_contract"][
            "lower_dimensional_half_open_ownership_materialized"
        ] is False
        and r208["formal_scope_contract"]["whole_original_tube_credit"] == 0
        and r208["formal_scope_contract"][
            "global_exact_key_disposition_credit"
        ] == 0,
        "Round208 scope",
    )
    face_ledger = r208["formal_final_factor_face_ledger"]
    leaf_ledger = r208["formal_leaf_geometry_ledger"]
    u2_ledger = r208["formal_U_pipe_U_side_specific_ledger"]
    region_ledger = r208["formal_local_open_3D_signature_ledger"]
    faces = face_ledger["rows"]
    leaves = leaf_ledger["rows"]
    u2_rows = u2_ledger["rows"]
    regions = region_ledger["rows"]
    validate_closed_rows(
        faces, 18_412, face_ledger["rows_sha256"],
        "face_row_id", "Round208 face",
    )
    validate_closed_rows(
        leaves, EXPECTED_LEAVES, leaf_ledger["rows_sha256"],
        "leaf_row_id", "Round208 leaf",
    )
    validate_closed_rows(
        u2_rows, EXPECTED_U2_SHEETS, u2_ledger["rows_sha256"],
        "leaf_row_id", "Round208 U|U",
    )
    validate_closed_rows(
        regions, EXPECTED_STRICT_REGIONS, region_ledger["rows_sha256"],
        "region_row_id", "Round208 region",
    )
    raw_faces = [
        {key: value for key, value in row.items() if key != "row_sha256"}
        for row in faces
    ]
    raw_leaves = [
        {
            key: value for key, value in row.items()
            if key not in {"row_sha256", "formal_final_geometry_row_materialized"}
        }
        for row in leaves
    ]
    raw_u2 = [
        {
            key: value for key, value in row.items()
            if key not in {
                "row_sha256",
                "both_strict_sides_formally_signature_materialized",
            }
        }
        for row in u2_rows
    ]
    require(
        digest(raw_faces) == R195_FACE_ROWS_SHA256
        and digest(raw_leaves) == R195_LEAF_ROWS_SHA256
        and digest(raw_u2) == R195_U2_ROWS_SHA256,
        "independent Round195 geometry reconstruction",
    )
    return r173, leaves, regions, faces, u2_rows


def signature_core(signature: dict[str, Any]) -> dict[str, Any]:
    require(
        set(signature)
        == {
            "official_key_id",
            "official_key_ordinal",
            "official_key_row",
            "ordered_integer_wall_events",
            "outgoing_cell",
            "roof",
            "signed_wall_word",
            "source_chart",
            "target_chart",
            "target_lift",
        },
        "signature schema",
    )
    return {
        key: value for key, value in signature.items()
        if key not in {"outgoing_cell", "target_chart"}
    }


def shadow_cell(active_factor: str, inactive_sign: str) -> str:
    active_sign = OPPOSITE_SIGN[inactive_sign]
    signs = (
        (active_sign, inactive_sign)
        if active_factor == "HPLUS"
        else (inactive_sign, active_sign)
    )
    return SIGN_CELL[signs]


def probe_id(kind: str, payload: dict[str, Any]) -> str:
    return f"round209-{kind}:{digest(payload)}"


def build_probe_lineages(
    leaves: list[dict[str, Any]],
    regions: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    by_leaf: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for region in regions:
        by_leaf[region["leaf_row_id"]].append(region)
    require(len(by_leaf) == EXPECTED_LEAVES, "region leaf join")
    sheets: list[dict[str, Any]] = []
    curves: list[dict[str, Any]] = []
    endpoints: list[dict[str, Any]] = []
    owner_counts: Counter[str] = Counter()
    shadow_counts: Counter[str] = Counter()
    pair_counts: Counter[str] = Counter()
    factor_counts: Counter[str] = Counter()
    c0_counts: Counter[str] = Counter()
    core_counts: Counter[str] = Counter()
    curve_pairs: Counter[str] = Counter()
    curve_axes: Counter[str] = Counter()
    curve_sides: Counter[str] = Counter()
    curve_provenance: Counter[str] = Counter()

    for leaf in sorted(leaves, key=lambda row: row["leaf_row_id"]):
        leaf_id = leaf["leaf_row_id"]
        joined = sorted(by_leaf[leaf_id], key=lambda row: row["region_row_id"])
        classification = leaf["final_graph_classification"]
        if classification == "EMPTY":
            require(
                leaf["two_dimensional_graph_sheet_count"] == 0
                and leaf["one_dimensional_clipping_curve_segment_count"] == 0
                and leaf["zero_dimensional_boundary_endpoint_incidence_count"]
                == 0
                and leaf["side_specific_signature_candidate_region_count"] == 1
                and len(joined) == 1,
                f"empty leaf:{leaf_id}",
            )
            continue
        require(
            classification in {"CLIPPED_2D_BOUNDARY_1D", "FULL_2D"}
            and leaf["two_dimensional_graph_sheet_count"] == 1
            and leaf["side_specific_signature_candidate_region_count"] == 2
            and leaf["candidate_region_signs"]
            == ["STRICT_NEGATIVE", "STRICT_POSITIVE"]
            and len(joined) == 2,
            f"nonempty leaf:{leaf_id}",
        )
        owner_rows = [
            row for row in joined if row["outgoing_cell"] in {"E", "W"}
        ]
        shadow_rows = [
            row for row in joined if row["outgoing_cell"] in {"N", "S"}
        ]
        require(
            len(owner_rows) == len(shadow_rows) == 1,
            f"owner pair:{leaf_id}",
        )
        owner = owner_rows[0]
        shadow = shadow_rows[0]
        require(
            owner["F_sign"] == "STRICT_POSITIVE"
            and shadow["F_sign"] == "STRICT_NEGATIVE",
            f"F sides:{leaf_id}",
        )
        inactive_set = {row["inactive_factor"] for row in joined}
        require(
            len(inactive_set) == 1
            and next(iter(inactive_set)) in {"HPLUS", "HMINUS"},
            f"inactive factor:{leaf_id}",
        )
        inactive_factor = next(iter(inactive_set))
        active_factor = "HMINUS" if inactive_factor == "HPLUS" else "HPLUS"
        require(
            owner["whole_box_factor_C0"] == shadow["whole_box_factor_C0"],
            f"C0 equality:{leaf_id}",
        )
        inactive_c0 = owner["whole_box_factor_C0"][inactive_factor]
        inactive_sign = inactive_c0["selected_sign"]
        require(inactive_sign in STRICT_SIGNS, f"strict C0:{leaf_id}")
        if inactive_c0["direct_sign"] == inactive_sign:
            c0_proof = "DIRECT_WHOLE_BOX_C0"
        else:
            require(
                inactive_c0["centered_sign"] == inactive_sign,
                f"centered C0:{leaf_id}",
            )
            c0_proof = "CENTERED_WHOLE_BOX_C0"
        owner_cell = "E" if inactive_sign == "STRICT_POSITIVE" else "W"
        excluded_cell = shadow_cell(active_factor, inactive_sign)
        require(
            owner["outgoing_cell"] == owner_cell
            and shadow["outgoing_cell"] == excluded_cell
            and (owner["HPLUS_sign"], owner["HMINUS_sign"])
            == CELL_SIGNS[owner_cell]
            and (shadow["HPLUS_sign"], shadow["HMINUS_sign"])
            == CELL_SIGNS[excluded_cell],
            f"factor owner cells:{leaf_id}",
        )
        owner_active = owner[
            "HPLUS_sign" if active_factor == "HPLUS" else "HMINUS_sign"
        ]
        owner_inactive = owner[
            "HPLUS_sign" if inactive_factor == "HPLUS" else "HMINUS_sign"
        ]
        shadow_active = shadow[
            "HPLUS_sign" if active_factor == "HPLUS" else "HMINUS_sign"
        ]
        shadow_inactive = shadow[
            "HPLUS_sign" if inactive_factor == "HPLUS" else "HMINUS_sign"
        ]
        require(
            owner_active == owner_inactive == inactive_sign
            and shadow_inactive == inactive_sign
            and shadow_active == OPPOSITE_SIGN[inactive_sign],
            f"factor side derivation:{leaf_id}",
        )
        owner_sig = owner["local_return_signature"]
        shadow_sig = shadow["local_return_signature"]
        owner_prefix = owner_sig["target_lift"].split("[", 1)[0]
        shadow_prefix = shadow_sig["target_lift"].split("[", 1)[0]
        require(
            owner_sig["outgoing_cell"] == owner_cell
            and shadow_sig["outgoing_cell"] == excluded_cell
            and owner_sig["target_chart"] == f"{owner_prefix}:{owner_cell}"
            and shadow_sig["target_chart"] == f"{shadow_prefix}:{excluded_cell}"
            and signature_core(owner_sig) == signature_core(shadow_sig),
            f"signature pair:{leaf_id}",
        )
        core_sha256 = digest(signature_core(owner_sig))
        relation = (
            "HMINUS=2*Nx_ON_HPLUS_ZERO_SHEET"
            if active_factor == "HPLUS"
            else "HPLUS=2*Nx_ON_HMINUS_ZERO_SHEET"
        )
        identity = {
            "leaf_row_id": leaf_id,
            "owner_region_row_id": owner["region_row_id"],
            "shadow_region_row_id": shadow["region_row_id"],
            "rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
        }
        sheet_id = probe_id("half-open-sheet", identity)
        sheet = closed_row({
            "sheet_row_id": sheet_id,
            "leaf_row_id": leaf_id,
            "origin_row_id": leaf["origin_row_id"],
            "occurrence_row_id": leaf["occurrence_row_id"],
            "retained_child_row_id": leaf["retained_child_row_id"],
            "leaf_classification": classification,
            "active_factor": active_factor,
            "inactive_factor": inactive_factor,
            "inactive_factor_whole_box_C0_proof": c0_proof,
            "inactive_factor_whole_box_strict_sign": inactive_sign,
            "factor_identity_on_sheet": relation,
            "Nx_sign_on_sheet": inactive_sign,
            "owner_region_row_id": owner["region_row_id"],
            "shadow_region_row_id": shadow["region_row_id"],
            "owner_outgoing_cell": owner_cell,
            "shadow_outgoing_cell": excluded_cell,
            "owner_signature_core_sha256": core_sha256,
            "shadow_signature_core_sha256": core_sha256,
            "signature_difference_field_allowlist": [
                "outgoing_cell", "target_chart",
            ],
            "Round173_half_open_rule": "E or W owns; N or S excludes",
            "deterministic_unique_owner_lineage": True,
            "incidence_is_not_a_global_component": True,
            "formal_half_open_owner_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        sheets.append(sheet)
        owner_counts[owner_cell] += 1
        shadow_counts[excluded_cell] += 1
        pair_counts[f"{owner_cell}|{excluded_cell}"] += 1
        factor_counts[f"{active_factor}|{inactive_sign}"] += 1
        c0_counts[c0_proof] += 1
        core_counts[core_sha256] += 1

        leaf_curve_count = 0
        leaf_endpoint_count = 0
        for face_key, side in (
            ("lower_t_face", "LOWER"),
            ("upper_t_face", "UPPER"),
        ):
            face = leaf[face_key]
            if face["zero_set_kind"] != "CURVE":
                continue
            leaf_curve_count += 1
            boundary_pair = face["boundary_edge_pair"]
            boundary_edges = boundary_pair.split("|")
            require(
                len(boundary_edges) == 2
                and len(set(boundary_edges)) == 2
                and set(boundary_edges) <= {"E", "W", "N", "S"}
                and face["boundary_endpoint_incidence_count"] == 2,
                f"curve endpoints:{leaf_id}:{side}",
            )
            curve_identity = {
                "sheet_row_id": sheet_id,
                "face_side": side,
                "boundary_edge_pair": boundary_pair,
                "graph_axis": face["graph_axis"],
                "provenance": face["provenance"],
            }
            curve_id = probe_id(
                "half-open-curve-incidence",
                curve_identity,
            )
            curve = closed_row({
                "curve_row_id": curve_id,
                "sheet_row_id": sheet_id,
                "sheet_row_sha256": sheet["row_sha256"],
                "leaf_row_id": leaf_id,
                "face_side": side,
                "graph_axis": face["graph_axis"],
                "boundary_edge_pair": boundary_pair,
                "geometry_provenance": face["provenance"],
                "owner_region_row_id": owner["region_row_id"],
                "owner_outgoing_cell": owner_cell,
                "shadow_region_row_id": shadow["region_row_id"],
                "shadow_outgoing_cell": excluded_cell,
                "owner_signature_core_sha256": core_sha256,
                "deterministic_owner_lineage_inherited_from_sheet": True,
                "incidence_is_not_a_global_component": True,
                "formal_half_open_owner_credit": 0,
                "whole_original_tube_credit": 0,
                "global_exact_key_disposition_credit": 0,
            })
            curves.append(curve)
            curve_pairs[boundary_pair] += 1
            curve_axes[str(face["graph_axis"])] += 1
            curve_sides[side] += 1
            curve_provenance[face["provenance"]] += 1
            for ordinal, boundary_edge in enumerate(boundary_edges, 1):
                leaf_endpoint_count += 1
                endpoint_identity = {
                    "curve_row_id": curve_id,
                    "endpoint_ordinal": ordinal,
                    "boundary_edge": boundary_edge,
                }
                endpoints.append(closed_row({
                    "endpoint_row_id": probe_id(
                        "half-open-endpoint-incidence",
                        endpoint_identity,
                    ),
                    "curve_row_id": curve_id,
                    "curve_row_sha256": curve["row_sha256"],
                    "sheet_row_id": sheet_id,
                    "leaf_row_id": leaf_id,
                    "face_side": side,
                    "endpoint_ordinal": ordinal,
                    "boundary_edge": boundary_edge,
                    "owner_region_row_id": owner["region_row_id"],
                    "owner_outgoing_cell": owner_cell,
                    "shadow_region_row_id": shadow["region_row_id"],
                    "shadow_outgoing_cell": excluded_cell,
                    "owner_signature_core_sha256": core_sha256,
                    "deterministic_owner_lineage_inherited_from_curve": True,
                    "incidence_is_not_a_global_component": True,
                    "formal_half_open_owner_credit": 0,
                    "whole_original_tube_credit": 0,
                    "global_exact_key_disposition_credit": 0,
                }))
            leaf_endpoint_count += 0
        require(
            leaf_curve_count
            == leaf["one_dimensional_clipping_curve_segment_count"]
            and leaf_endpoint_count
            == leaf["zero_dimensional_boundary_endpoint_incidence_count"]
            and leaf_endpoint_count == 2 * leaf_curve_count,
            f"leaf dimensional conservation:{leaf_id}",
        )

    sheets.sort(key=lambda row: row["sheet_row_id"])
    curves.sort(key=lambda row: row["curve_row_id"])
    endpoints.sort(key=lambda row: row["endpoint_row_id"])
    require(
        digest(sheets) == EXPECTED_PROBE_SHEET_ROWS_SHA256
        and digest(curves) == EXPECTED_PROBE_CURVE_ROWS_SHA256
        and digest(endpoints) == EXPECTED_PROBE_ENDPOINT_ROWS_SHA256,
        "independent Round209 lineage pins",
    )
    require(
        owner_counts == {"E": 8_858, "W": 8_858}
        and shadow_counts == {"N": 8_858, "S": 8_858}
        and pair_counts
        == {
            "E|N": 4_429, "E|S": 4_429,
            "W|N": 4_429, "W|S": 4_429,
        }
        and factor_counts
        == {
            "HMINUS|STRICT_NEGATIVE": 4_429,
            "HMINUS|STRICT_POSITIVE": 4_429,
            "HPLUS|STRICT_NEGATIVE": 4_429,
            "HPLUS|STRICT_POSITIVE": 4_429,
        },
        "owner census",
    )
    audit = {
        "owner_outgoing_cell_count": dict(sorted(owner_counts.items())),
        "shadow_outgoing_cell_count": dict(sorted(shadow_counts.items())),
        "owner_shadow_pair_count": dict(sorted(pair_counts.items())),
        "active_factor_and_Nx_sign_count": dict(sorted(factor_counts.items())),
        "inactive_factor_C0_proof_count": dict(sorted(c0_counts.items())),
        "distinct_signature_core_count": len(core_counts),
        "signature_core_multiplicity_histogram": {
            str(key): value
            for key, value in sorted(Counter(core_counts.values()).items())
        },
        "curve_boundary_edge_pair_count": dict(sorted(curve_pairs.items())),
        "curve_graph_axis_count": dict(sorted(curve_axes.items())),
        "curve_face_side_count": dict(sorted(curve_sides.items())),
        "curve_geometry_provenance_count":
            dict(sorted(curve_provenance.items())),
    }
    return sheets, curves, endpoints, audit


def audit_u2(
    u2_rows: list[dict[str, Any]],
    sheets: list[dict[str, Any]],
    curves: list[dict[str, Any]],
    endpoints: list[dict[str, Any]],
) -> dict[str, Any]:
    sheet_by_leaf = {row["leaf_row_id"]: row for row in sheets}
    u2_leaf_ids = {row["leaf_row_id"] for row in u2_rows}
    require(
        len(u2_leaf_ids) == EXPECTED_U2_SHEETS
        and len({row["origin_row_id"] for row in u2_rows})
        == EXPECTED_U2_ORIGINS
        and u2_leaf_ids <= set(sheet_by_leaf),
        "U|U join",
    )
    owner: Counter[str] = Counter()
    active: Counter[str] = Counter()
    active_owner: Counter[str] = Counter()
    cross: Counter[str] = Counter()
    ordering: Counter[str] = Counter()
    face_count: Counter[str] = Counter()
    for row in u2_rows:
        sheet = sheet_by_leaf[row["leaf_row_id"]]
        require(
            row["active_factor"] == sheet["active_factor"]
            and row["curve_pair_nonintersection"] is True
            and row["local_geometric_residual"] is False
            and row["global_exact_key_disposition_credit"] == 0,
            "U|U row",
        )
        owner[sheet["owner_outgoing_cell"]] += 1
        active[sheet["active_factor"]] += 1
        active_owner[
            f"{sheet['active_factor']}|{sheet['owner_outgoing_cell']}"
        ] += 1
        cross[row["cross_t_status"]] += 1
        ordering[str(row["strict_curve_ordering"])] += 1
        face_count[str(row["curve_t_face_count"])] += 1
    u2_curves = [row for row in curves if row["leaf_row_id"] in u2_leaf_ids]
    u2_endpoints = [
        row for row in endpoints if row["leaf_row_id"] in u2_leaf_ids
    ]
    require(
        owner == {"E": 44, "W": 44}
        and active == {"HPLUS": 44, "HMINUS": 44}
        and active_owner
        == {
            "HMINUS|E": 22, "HMINUS|W": 22,
            "HPLUS|E": 22, "HPLUS|W": 22,
        }
        and cross
        == {
            "ONE_CURVE_OTHER_T_FACE_STRICTLY_ZERO_ABSENT": 12,
            "TWO_CURVES_STRICTLY_ORDERED_AND_DISJOINT": 76,
        }
        and ordering
        == {
            "None": 12,
            "UPPER_CURVE_STRICTLY_GREATER_P_THAN_LOWER_CURVE": 38,
            "UPPER_CURVE_STRICTLY_LESS_P_THAN_LOWER_CURVE": 38,
        }
        and face_count == {"1": 12, "2": 76}
        and len(u2_curves) == EXPECTED_U2_CURVES
        and len(u2_endpoints) == EXPECTED_U2_ENDPOINTS,
        "U|U census",
    )
    return {
        "sheet_count": EXPECTED_U2_SHEETS,
        "distinct_origin_count": EXPECTED_U2_ORIGINS,
        "owner_outgoing_cell_count": dict(sorted(owner.items())),
        "active_factor_count": dict(sorted(active.items())),
        "active_factor_owner_cell_count": dict(sorted(active_owner.items())),
        "cross_t_status_count": dict(sorted(cross.items())),
        "strict_curve_ordering_count": dict(sorted(ordering.items())),
        "curve_t_face_count": dict(sorted(face_count.items())),
        "1D_clipping_incidence_count": len(u2_curves),
        "0D_endpoint_incidence_count": len(u2_endpoints),
        "two_curve_pairs_strictly_ordered_and_disjoint": 76,
        "curve_pair_intersection_count": 0,
        "all_owner_lineages_joined": True,
    }


def formal_id(kind: str, probe_row_id: str, probe_sha256: str) -> str:
    return (
        f"round211-{kind}:"
        f"{digest({'probe_id': probe_row_id, 'probe_row_sha256': probe_sha256})}"
    )


def without(row: dict[str, Any], removed: set[str]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value) for key, value in row.items()
        if key not in removed
    }


def formalize(
    probe_sheets: list[dict[str, Any]],
    probe_curves: list[dict[str, Any]],
    probe_endpoints: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    sheet_map: dict[str, dict[str, Any]] = {}
    sheets: list[dict[str, Any]] = []
    for probe in probe_sheets:
        sheet_id = formal_id(
            "half-open-sheet-owner",
            probe["sheet_row_id"],
            probe["row_sha256"],
        )
        payload = without(
            probe,
            {
                "sheet_row_id", "row_sha256",
                "formal_half_open_owner_credit",
                "whole_original_tube_credit",
                "global_exact_key_disposition_credit",
            },
        )
        row = closed_row({
            "sheet_row_id": sheet_id,
            "probe_sheet_row_id": probe["sheet_row_id"],
            "probe_sheet_row_sha256": probe["row_sha256"],
            **payload,
            "local_dimensional_owner_materialized": True,
            "formal_half_open_owner_credit": 1,
            "component_deduplication_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        sheet_map[probe["sheet_row_id"]] = row
        sheets.append(row)
    curve_map: dict[str, dict[str, Any]] = {}
    curves: list[dict[str, Any]] = []
    for probe in probe_curves:
        parent = sheet_map[probe["sheet_row_id"]]
        curve_id = formal_id(
            "half-open-curve-incidence-owner",
            probe["curve_row_id"],
            probe["row_sha256"],
        )
        payload = without(
            probe,
            {
                "curve_row_id", "sheet_row_id", "sheet_row_sha256",
                "row_sha256", "formal_half_open_owner_credit",
                "whole_original_tube_credit",
                "global_exact_key_disposition_credit",
            },
        )
        row = closed_row({
            "curve_row_id": curve_id,
            "probe_curve_row_id": probe["curve_row_id"],
            "probe_curve_row_sha256": probe["row_sha256"],
            "sheet_row_id": parent["sheet_row_id"],
            "sheet_row_sha256": parent["row_sha256"],
            **payload,
            "local_dimensional_owner_materialized": True,
            "formal_half_open_owner_credit": 1,
            "component_deduplication_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        curve_map[probe["curve_row_id"]] = row
        curves.append(row)
    endpoints: list[dict[str, Any]] = []
    for probe in probe_endpoints:
        parent_curve = curve_map[probe["curve_row_id"]]
        parent_sheet = sheet_map[probe["sheet_row_id"]]
        endpoint_id = formal_id(
            "half-open-endpoint-incidence-owner",
            probe["endpoint_row_id"],
            probe["row_sha256"],
        )
        payload = without(
            probe,
            {
                "endpoint_row_id", "curve_row_id", "curve_row_sha256",
                "sheet_row_id", "row_sha256",
                "formal_half_open_owner_credit",
                "whole_original_tube_credit",
                "global_exact_key_disposition_credit",
            },
        )
        endpoints.append(closed_row({
            "endpoint_row_id": endpoint_id,
            "probe_endpoint_row_id": probe["endpoint_row_id"],
            "probe_endpoint_row_sha256": probe["row_sha256"],
            "curve_row_id": parent_curve["curve_row_id"],
            "curve_row_sha256": parent_curve["row_sha256"],
            "sheet_row_id": parent_sheet["sheet_row_id"],
            "sheet_row_sha256": parent_sheet["row_sha256"],
            **payload,
            "local_dimensional_owner_materialized": True,
            "formal_half_open_owner_credit": 1,
            "component_deduplication_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    sheets.sort(key=lambda row: row["sheet_row_id"])
    curves.sort(key=lambda row: row["curve_row_id"])
    endpoints.sort(key=lambda row: row["endpoint_row_id"])
    require(
        digest(sheets) == EXPECTED_FORMAL_SHEET_ROWS_SHA256
        and digest(curves) == EXPECTED_FORMAL_CURVE_ROWS_SHA256
        and digest(endpoints) == EXPECTED_FORMAL_ENDPOINT_ROWS_SHA256,
        "formal row pins",
    )
    sheet_by_id = {row["sheet_row_id"]: row for row in sheets}
    curve_by_id = {row["curve_row_id"]: row for row in curves}
    require(
        all(
            row["sheet_row_sha256"]
            == sheet_by_id[row["sheet_row_id"]]["row_sha256"]
            for row in curves
        )
        and all(
            row["sheet_row_sha256"]
            == sheet_by_id[row["sheet_row_id"]]["row_sha256"]
            and row["curve_row_sha256"]
            == curve_by_id[row["curve_row_id"]]["row_sha256"]
            for row in endpoints
        ),
        "formal lineage join hashes",
    )
    return sheets, curves, endpoints


def ledger(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def build_expected() -> dict[str, Any]:
    r173, leaves, regions, _faces, u2_rows = load_formal_inputs()
    probe_sheets, probe_curves, probe_endpoints, owner_audit = (
        build_probe_lineages(leaves, regions)
    )
    u2_audit = audit_u2(
        u2_rows,
        probe_sheets,
        probe_curves,
        probe_endpoints,
    )
    sheets, curves, endpoints = formalize(
        probe_sheets,
        probe_curves,
        probe_endpoints,
    )
    origin_count = len({row["origin_row_id"] for row in sheets})
    occurrence_count = len({row["occurrence_row_id"] for row in sheets})
    retained_child_count = len({
        row["retained_child_row_id"] for row in sheets
    })
    return {
        "status": STATUS,
        "formal_input_binding": {
            "Round209_probe_source_sha256": R209_SOURCE_SHA256,
            "Round209_spike_report_sha256": R209_REPORT_SHA256,
            "Round209_probe_result_sha256": R209_RESULT_SHA256,
            "Round209_probe_document_sha256": R209_DOCUMENT_SHA256,
            "Round208_producer_source_sha256": R208_SOURCE_SHA256,
            "Round208_certificate_sha256": R208_CERTIFICATE_SHA256,
            "Round208_result_sha256": R208_RESULT_SHA256,
            "Round208_verifier_or_manifest_used": False,
            "Round209_used_as_pinned_producer_side_evaluator": True,
        },
        "formal_scope_and_conservation": {
            "input_leaf_count": len(leaves),
            "empty_leaf_count": EXPECTED_EMPTY_LEAVES,
            "nonempty_sheet_leaf_count": EXPECTED_SHEETS,
            "strict_open_3D_region_count": EXPECTED_STRICT_REGIONS,
            "strict_region_identity": "36040=608+2*17716",
            "2D_sheet_owner_row_count": EXPECTED_SHEETS,
            "1D_curve_incidence_owner_row_count": EXPECTED_CURVES,
            "0D_endpoint_incidence_owner_row_count": EXPECTED_ENDPOINTS,
            "endpoint_identity": "40912=2*20456",
            "covered_origin_count_without_whole_origin_credit": origin_count,
            "covered_occurrence_count_without_global_component_credit":
                occurrence_count,
            "covered_retained_child_count": retained_child_count,
            "all_nonempty_sheets_have_exactly_one_E_or_W_owner": True,
            "all_sheet_signature_pairs_match_except_outgoing_chart_fields":
                True,
            "incidence_rows_are_not_deduplicated_global_components": True,
            "owner_audit": owner_audit,
            "U_pipe_U_audit": u2_audit,
        },
        "formal_2D_sheet_owner_ledger": ledger(sheets, "sheet_row_id"),
        "formal_1D_curve_incidence_owner_ledger":
            ledger(curves, "curve_row_id"),
        "formal_0D_endpoint_incidence_owner_ledger":
            ledger(endpoints, "endpoint_row_id"),
        "formal_credit_contract": {
            "formal_2D_half_open_owner_credits": EXPECTED_SHEETS,
            "formal_1D_incidence_owner_credits": EXPECTED_CURVES,
            "formal_0D_incidence_owner_credits": EXPECTED_ENDPOINTS,
            "formal_local_dimensional_owner_credit_total":
                EXPECTED_SHEETS + EXPECTED_CURVES + EXPECTED_ENDPOINTS,
            "local_lower_dimensional_ownership_materialized": True,
            "global_component_deduplication_complete": False,
            "global_component_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator":
                EXPECTED_SOURCE_G_EXACT_KEYS,
            "D02": "BLOCKED",
            "Gate5": "10/18",
            "complete_global_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "join and deduplicate local sheet/curve/endpoint incidences into "
            "true physical components, then combine Round208 open-region "
            "rows and the separate wall-G replacement by immutable exact "
            "key; no fibre may be disposed until every occurrence and every "
            "owned lower-dimensional component in that fibre is exhausted"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": PRODUCER_SHA256,
            "python_version": sys.version.split()[0],
            "producer_imported_or_executed_by_independent_verifier": False,
        },
    }


def validate_candidate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    require(candidate == expected, "full expected canonical equality")
    contract = candidate["formal_credit_contract"]
    require(
        contract["formal_local_dimensional_owner_credit_total"] == 79_084
        and contract["global_component_deduplication_complete"] is False
        and contract["global_component_credit"] == 0
        and contract["whole_leaf_credit"] == 0
        and contract["whole_origin_credit"] == 0
        and contract["whole_original_tube_credit"] == 0
        and contract["global_exact_key_disposition_credit"] == 0,
        "credit boundary",
    )


def semantic_attacks(expected: dict[str, Any]) -> dict[str, Any]:
    mutations: list[tuple[str, list[Any], str, Any]] = [
        ("sheet owner swap", ["formal_2D_sheet_owner_ledger", "rows", 0], "owner_outgoing_cell", "N"),
        ("sheet credit zero", ["formal_2D_sheet_owner_ledger", "rows", 0], "formal_half_open_owner_credit", 0),
        ("sheet credit two", ["formal_2D_sheet_owner_ledger", "rows", 0], "formal_half_open_owner_credit", 2),
        ("sheet component merge", ["formal_2D_sheet_owner_ledger", "rows", 0], "incidence_is_not_a_global_component", False),
        ("sheet dedup credit", ["formal_2D_sheet_owner_ledger", "rows", 0], "component_deduplication_credit", 1),
        ("curve parent forgery", ["formal_1D_curve_incidence_owner_ledger", "rows", 0], "sheet_row_id", "forged"),
        ("curve hash forgery", ["formal_1D_curve_incidence_owner_ledger", "rows", 0], "sheet_row_sha256", "0" * 64),
        ("endpoint parent forgery", ["formal_0D_endpoint_incidence_owner_ledger", "rows", 0], "curve_row_id", "forged"),
        ("endpoint owner swap", ["formal_0D_endpoint_incidence_owner_ledger", "rows", 0], "owner_outgoing_cell", "INVALID"),
        ("global component true", ["formal_credit_contract"], "global_component_deduplication_complete", True),
        ("global component credit", ["formal_credit_contract"], "global_component_credit", 1),
        ("whole leaf credit", ["formal_credit_contract"], "whole_leaf_credit", 1),
        ("whole origin credit", ["formal_credit_contract"], "whole_origin_credit", 1),
        ("whole tube credit", ["formal_credit_contract"], "whole_original_tube_credit", 1),
        ("global disposition credit", ["formal_credit_contract"], "global_exact_key_disposition_credit", 1),
        ("official disposition count", ["formal_credit_contract"], "official_source_G_global_disposition_count", 1),
        ("Gate5 promotion", ["formal_credit_contract"], "Gate5", "11/18"),
        ("CM2 promotion", ["formal_credit_contract"], "CM2", "GO"),
        ("input pin forgery", ["formal_input_binding"], "Round208_result_sha256", "0" * 64),
        ("count forgery", ["formal_scope_and_conservation"], "2D_sheet_owner_row_count", 17717),
    ]
    rejected = 0
    for _label, path, field, value in mutations:
        candidate: Any = expected.copy()
        original: Any = expected
        cloned: Any = candidate
        for step in path:
            original_child = original[step]
            cloned_child = (
                original_child.copy()
                if isinstance(original_child, dict)
                else list(original_child)
            )
            cloned[step] = cloned_child
            original = original_child
            cloned = cloned_child
        cloned[field] = value
        require(
            digest(candidate) != CERTIFICATE_RESULT_SHA256,
            f"semantic attack changes signed result:{_label}",
        )
        try:
            validate_candidate(candidate, expected)
        except Round211VerificationError:
            rejected += 1
    require(rejected == len(mutations), "semantic attacks")
    return {"rejected": rejected, "total": len(mutations)}


def json_attacks() -> dict[str, Any]:
    attacks = [
        b'{"a":1,"a":2}\n',
        b'{"a":1.0}\n',
        b'{"a":NaN}\n',
        b'{"a":1}\n\n',
        b'\xef\xbb\xbf{"a":1}\n',
        b' [1]\n',
        b'{"b":1,"a":2}\n',
        b'{"a":"\xff"}\n',
        b'{}\x00\n',
    ]
    rejected = 0
    for raw in attacks:
        try:
            strict_json(raw, "attack", 1024)
        except Round211VerificationError:
            rejected += 1
    require(rejected == len(attacks), "JSON attacks")
    return {"rejected": rejected, "total": len(attacks)}


def validate_certificate_path(path: Path) -> Path:
    absolute = path.resolve(strict=False)
    require(absolute.parent == HERE.resolve(), "certificate parent")
    official = absolute.name == CERTIFICATE
    replay = (
        absolute.name.startswith(f".{PREFIX}_replay_")
        and absolute.name.endswith(".json")
    )
    require(official or replay, "certificate filename")
    require(not absolute.is_symlink(), "certificate symlink")
    return absolute


def validate_output(path: Path) -> Path:
    absolute = path.resolve(strict=False)
    require(absolute.parent == HERE.resolve(), "output parent")
    official = absolute.name == OUTPUT.name
    replay = (
        absolute.name.startswith(f".{PREFIX}_verification_replay_")
        and absolute.name.endswith(".json")
    )
    require(official or replay, "output filename")
    require(not absolute.is_symlink(), "output symlink")
    if absolute.exists():
        meta = absolute.lstat()
        require(
            stat.S_ISREG(meta.st_mode) and meta.st_nlink == 1,
            "output regular unique",
        )
    return absolute


def path_attacks() -> dict[str, Any]:
    candidates = [
        Path("/tmp/round211.json"),
        HERE / "../escape.json",
        HERE / "wrong.json",
        Path("."),
        HERE,
        HERE / f".{PREFIX}_replay_bad.txt",
        HERE / f"{PREFIX}_certificate.json/child",
        HERE / f".{PREFIX}_verification_replay_bad.txt",
    ]
    rejected = 0
    for index, path in enumerate(candidates):
        validator = validate_certificate_path if index < 7 else validate_output
        try:
            validator(path)
        except (Round211VerificationError, OSError):
            rejected += 1
    require(rejected == len(candidates), "path attacks")
    return {"rejected": rejected, "total": len(candidates)}


def safe_write(path: Path, data: bytes) -> None:
    destination = validate_output(path)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{PREFIX}.verification.tmp.",
        dir=HERE,
    )
    temp_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, destination)
        directory = os.open(HERE, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    expected = build_expected()
    expected_sha256 = digest(expected)
    require(
        expected_sha256 == CERTIFICATE_RESULT_SHA256,
        "independent expected result pin",
    )
    certificate_path = validate_certificate_path(arguments.certificate)
    raw = regular_bytes(certificate_path, MAX_INPUT_BYTES)
    if certificate_path.name == CERTIFICATE:
        require(
            hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256,
            "official certificate SHA256",
        )
    envelope = strict_json(raw, "Round211 certificate", MAX_INPUT_BYTES)
    require(
        set(envelope) == {"schema", "result", "result_sha256"}
        and envelope["schema"] == SCHEMA
        and envelope["result_sha256"] == CERTIFICATE_RESULT_SHA256
        and digest(envelope["result"]) == CERTIFICATE_RESULT_SHA256,
        "Round211 envelope",
    )
    validate_candidate(envelope["result"], expected)
    semantic = semantic_attacks(expected)
    json_suite = json_attacks()
    paths = path_attacks()
    verification = {
        "status": PASS_STATUS,
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "producer_sha256": PRODUCER_SHA256,
        "verifier_sha256": hashlib.sha256(
            regular_bytes(Path(__file__), 5_000_000)
        ).hexdigest(),
        "complete_expected_object_rebuilt_before_certificate_open": True,
        "producer_imported_or_executed": False,
        "Round209_probe_imported_or_executed": False,
        "full_expected_python_object_and_canonical_equality": True,
        "formal_census": {
            "2D_sheet_owner_rows": EXPECTED_SHEETS,
            "1D_curve_incidence_owner_rows": EXPECTED_CURVES,
            "0D_endpoint_incidence_owner_rows": EXPECTED_ENDPOINTS,
            "formal_local_dimensional_owner_credit_total": 79_084,
            "covered_origins_without_whole_origin_credit": 8_264,
            "global_component_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "attack_results": {
            "re_signed_semantic": semantic,
            "strict_JSON_and_encoding": json_suite,
            "path_type_and_output": paths,
        },
        "strict_state": {
            "source_G_global_dispositions": "0/224580",
            "D02": "BLOCKED",
            "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    document = {
        "schema": VERIFICATION_SCHEMA,
        "verification": verification,
        "verification_result_sha256": digest(verification),
    }
    safe_write(arguments.output, canonical_bytes(document) + b"\n")
    print(PASS_STATUS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
