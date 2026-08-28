#!/usr/bin/env python3
"""Read-only feasibility probe for outgoing-W lower-dimensional owners.

The probe treats the pinned Round208 certificate, the frozen Round173
half-open chart rule, and the Round195 geometry carried by Round208 as a
non-formal trust boundary.  It constructs deterministic in-memory lineage
rows for every 2D sheet, 1D clipping incidence, and 0D endpoint incidence.
Only a compact JSON summary is written to stdout.  No formal credit is issued.
"""

from __future__ import annotations

import ast
from collections import Counter, defaultdict
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round209.source-g-outgoing-half-open-owner-probe.v1"
STATUS = (
    "VALIDATED_READ_ONLY_FEASIBILITY__OUTGOING_W_HALF_OPEN_OWNER_LINEAGE"
    "__NONFORMAL_ZERO_PROMOTION"
)
MAX_INPUT_BYTES = 300 * 1024 * 1024

R208_SOURCE = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization.py"
)
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
EXPECTED_SHEET_LINEAGE_ROWS_SHA256 = (
    "be4955bf1d705ffd8730505b8407a05a220940d5b76878a9a7059a5df762289a"
)
EXPECTED_CURVE_LINEAGE_ROWS_SHA256 = (
    "a3e375fc26afa4df3db6e8fd4b07e4bc4f97d91c9eceb6893e29ffe4ce89422e"
)
EXPECTED_ENDPOINT_LINEAGE_ROWS_SHA256 = (
    "23eee8138694f9b53436a66740da7801146877a62ee2b8b2fce6e2cfc36e916b"
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
OWNER_CELLS = {"E", "W"}
SHADOW_CELLS = {"N", "S"}
FACTORS = {"HPLUS", "HMINUS"}


class Round209Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round209Error(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def encoded_chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode()


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in encoded_chunks(value):
        state.update(chunk)
    return state.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return b"".join(encoded_chunks(value))


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def pinned_regular_sha256(
    path: Path,
    expected: str | None = None,
    maximum: int = MAX_INPUT_BYTES,
) -> str:
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), f"input regular:{path.name}")
    require(not path.is_symlink(), f"input symlink:{path.name}")
    require(before.st_nlink == 1, f"input hardlink:{path.name}")
    require(0 < before.st_size <= maximum, f"input size:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
    )
    state = hashlib.sha256()
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
            f"input open race:{path.name}",
        )
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            state.update(chunk)
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
            f"input read race:{path.name}",
        )
    finally:
        os.close(descriptor)
    actual = state.hexdigest()
    if expected is not None:
        require(actual == expected, f"input SHA256:{path.name}")
    return actual


def load_json_regular(path: Path) -> Any:
    before = path.lstat()
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_size == before.st_size
            and opened.st_dev == before.st_dev
            and opened.st_ino == before.st_ino
            and opened.st_mtime_ns == before.st_mtime_ns,
            f"JSON open race:{path.name}",
        )
        with os.fdopen(descriptor, "r", encoding="utf-8") as handle:
            descriptor = -1
            value = json.load(handle)
            after = os.fstat(handle.fileno())
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
                f"JSON read race:{path.name}",
            )
            return value
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def install_read_only_audit_hook() -> None:
    mutation_events = {
        "os.remove",
        "os.rename",
        "os.rmdir",
        "os.mkdir",
        "os.link",
        "os.symlink",
        "os.truncate",
        "shutil.copyfile",
        "shutil.copymode",
        "shutil.copystat",
    }

    def audit(event: str, arguments: tuple[Any, ...]) -> None:
        if event == "open":
            mode = arguments[1]
            flags = arguments[2]
            if isinstance(mode, str):
                require(
                    not any(token in mode for token in ("w", "a", "x", "+")),
                    "runtime write-mode open rejected",
                )
            if isinstance(flags, int):
                write_flags = (
                    os.O_WRONLY
                    | os.O_RDWR
                    | os.O_CREAT
                    | os.O_TRUNC
                    | os.O_APPEND
                )
                require(
                    flags & write_flags == 0,
                    "runtime write-flags open rejected",
                )
        elif event in mutation_events:
            raise Round209Error(f"runtime filesystem mutation rejected:{event}")

    sys.addaudithook(audit)


def validate_source_has_no_write_surface(source_path: Path) -> dict[str, Any]:
    raw = source_path.read_text(encoding="utf-8")
    tree = ast.parse(raw, filename=source_path.name)
    forbidden_attributes = {
        "write_text",
        "write_bytes",
        "unlink",
        "rename",
        "replace",
        "mkdir",
        "rmdir",
        "remove",
        "truncate",
        "makedirs",
        "removedirs",
        "renames",
    }
    forbidden_names = {"remove", "unlink", "rename", "replace"}
    violations: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        if (
            isinstance(function, ast.Attribute)
            and function.attr in forbidden_attributes
        ):
            violations.append(function.attr)
        elif isinstance(function, ast.Name) and function.id in forbidden_names:
            violations.append(function.id)
    require(not violations, "source write API surface")
    return {
        "AST_filesystem_mutation_call_count": 0,
        "output_path_option_exists": False,
        "stdout_only_result_document": True,
        "runtime_read_only_audit_hook_installed": True,
    }


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
    require(digest(rows) == expected_digest, f"{label} ledger digest")
    for row in rows:
        row_copy = dict(row)
        row_sha256 = row_copy.pop("row_sha256")
        require(digest(row_copy) == row_sha256, f"{label} row closure")


def strip_fields(
    rows: list[dict[str, Any]],
    removed: set[str],
) -> list[dict[str, Any]]:
    return [
        {
            key: value
            for key, value in row.items()
            if key not in removed
        }
        for row in rows
    ]


def validate_inputs() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    input_hashes = {
        "Round173_source_sha256": pinned_regular_sha256(
            HERE / R173_SOURCE,
            R173_SOURCE_SHA256,
            5_000_000,
        ),
        "Round173_certificate_sha256": pinned_regular_sha256(
            HERE / R173_CERTIFICATE,
            R173_CERTIFICATE_SHA256,
            5_000_000,
        ),
        "Round195_probe_source_sha256": pinned_regular_sha256(
            HERE / R195_SOURCE,
            R195_SOURCE_SHA256,
            5_000_000,
        ),
        "Round195_spike_report_sha256": pinned_regular_sha256(
            HERE / R195_REPORT,
            R195_REPORT_SHA256,
            5_000_000,
        ),
        "Round208_producer_source_sha256": pinned_regular_sha256(
            HERE / R208_SOURCE,
            R208_SOURCE_SHA256,
            5_000_000,
        ),
        "Round208_certificate_sha256": pinned_regular_sha256(
            HERE / R208_CERTIFICATE,
            R208_CERTIFICATE_SHA256,
        ),
    }

    r173_envelope = load_json_regular(HERE / R173_CERTIFICATE)
    require(
        set(r173_envelope) == {"schema", "result", "result_sha256"}
        and r173_envelope["schema"] == R173_SCHEMA
        and r173_envelope["result_sha256"] == R173_RESULT_SHA256
        and digest(r173_envelope["result"]) == R173_RESULT_SHA256,
        "Round173 envelope integrity",
    )
    r173 = r173_envelope["result"]
    rule = r173["outgoing_chart_contract"]
    require(
        rule["diagonal_seam_rule"] == "E or W owns; N or S excludes"
        and rule["owner_set"] == ["E", "W"]
        and rule["duplicate_trace_is_identified_not_added"] is True
        and rule["owner_set_is_invariant_under_Jx_and_Jy"] is True
        and rule["strict_chart_transport_is_total_on_E_W_N_S"] is True
        and r173["scope"][
            "half_open_seam_outgoing_chart_transport_certified"
        ] is True
        and all(
            row["half_open_diagonal_owner_rule"]
            == "E or W owns; N or S excludes"
            and row["half_open_owner_set_image"] == ["E", "W"]
            and row["half_open_owner_rule_equivariant"] is True
            for row in r173["exact_transport_generators"]
        ),
        "Round173 frozen half-open rule",
    )

    r208_envelope = load_json_regular(HERE / R208_CERTIFICATE)
    require(
        set(r208_envelope) == {"schema", "result", "result_sha256"}
        and r208_envelope["schema"] == R208_SCHEMA
        and r208_envelope["result_sha256"] == R208_RESULT_SHA256
        and digest(r208_envelope["result"]) == R208_RESULT_SHA256,
        "Round208 envelope integrity",
    )
    r208 = r208_envelope["result"]
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
        "Round208 scope and nonpromotion boundary",
    )
    input_hashes.update({
        "Round173_result_sha256": R173_RESULT_SHA256,
        "Round195_probe_result_sha256": R195_RESULT_SHA256,
        "Round195_probe_document_sha256": R195_DOCUMENT_SHA256,
        "Round208_result_sha256": R208_RESULT_SHA256,
    })
    return r173, r208, input_hashes


def validate_round195_geometry(
    r208: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    face_ledger = r208["formal_final_factor_face_ledger"]
    leaf_ledger = r208["formal_leaf_geometry_ledger"]
    u2_ledger = r208["formal_U_pipe_U_side_specific_ledger"]
    region_ledger = r208["formal_local_open_3D_signature_ledger"]
    faces = face_ledger["rows"]
    leaves = leaf_ledger["rows"]
    u2_rows = u2_ledger["rows"]
    regions = region_ledger["rows"]

    validate_closed_rows(
        faces,
        18_412,
        face_ledger["rows_sha256"],
        "face_row_id",
        "Round208 face",
    )
    validate_closed_rows(
        leaves,
        EXPECTED_LEAVES,
        leaf_ledger["rows_sha256"],
        "leaf_row_id",
        "Round208 leaf",
    )
    validate_closed_rows(
        u2_rows,
        EXPECTED_U2_SHEETS,
        u2_ledger["rows_sha256"],
        "leaf_row_id",
        "Round208 U|U",
    )
    validate_closed_rows(
        regions,
        EXPECTED_STRICT_REGIONS,
        region_ledger["rows_sha256"],
        "region_row_id",
        "Round208 strict region",
    )

    raw_faces = strip_fields(faces, {"row_sha256"})
    raw_leaves = strip_fields(
        leaves,
        {"row_sha256", "formal_final_geometry_row_materialized"},
    )
    raw_u2 = strip_fields(
        u2_rows,
        {
            "row_sha256",
            "both_strict_sides_formally_signature_materialized",
        },
    )
    require(
        face_ledger["raw_Round195_rows_sha256"] == R195_FACE_ROWS_SHA256
        and leaf_ledger["raw_Round195_rows_sha256"] == R195_LEAF_ROWS_SHA256
        and u2_ledger["raw_Round195_rows_sha256"] == R195_U2_ROWS_SHA256
        and digest(raw_faces) == R195_FACE_ROWS_SHA256
        and digest(raw_leaves) == R195_LEAF_ROWS_SHA256
        and digest(raw_u2) == R195_U2_ROWS_SHA256,
        "Round195 geometry exact reconstruction from Round208",
    )
    return leaves, regions, faces, u2_rows


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
        "closed local return signature schema",
    )
    return {
        key: value
        for key, value in signature.items()
        if key not in {"outgoing_cell", "target_chart"}
    }


def expected_shadow_cell(
    active_factor: str,
    inactive_sign: str,
) -> str:
    active_sign = OPPOSITE_SIGN[inactive_sign]
    pair = (
        (active_sign, inactive_sign)
        if active_factor == "HPLUS"
        else (inactive_sign, active_sign)
    )
    return SIGN_CELL[pair]


def lineage_id(prefix: str, payload: dict[str, Any]) -> str:
    return f"round209-{prefix}:{digest(payload)}"


def build_lineages(
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
    require(len(by_leaf) == EXPECTED_LEAVES, "region-to-leaf total join")

    sheet_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    endpoint_rows: list[dict[str, Any]] = []
    owner_counts: Counter[str] = Counter()
    shadow_counts: Counter[str] = Counter()
    pair_counts: Counter[str] = Counter()
    factor_sign_counts: Counter[str] = Counter()
    c0_proof_counts: Counter[str] = Counter()
    signature_core_counts: Counter[str] = Counter()
    curve_pair_counts: Counter[str] = Counter()
    curve_axis_counts: Counter[str] = Counter()
    curve_side_counts: Counter[str] = Counter()
    curve_provenance_counts: Counter[str] = Counter()

    for leaf in sorted(leaves, key=lambda row: row["leaf_row_id"]):
        leaf_id = leaf["leaf_row_id"]
        joined = sorted(
            by_leaf[leaf_id],
            key=lambda row: row["region_row_id"],
        )
        classification = leaf["final_graph_classification"]
        if classification == "EMPTY":
            require(
                leaf["two_dimensional_graph_sheet_count"] == 0
                and leaf["one_dimensional_clipping_curve_segment_count"] == 0
                and leaf["zero_dimensional_boundary_endpoint_incidence_count"]
                == 0
                and leaf["side_specific_signature_candidate_region_count"]
                == 1
                and len(joined) == 1,
                f"empty leaf exact dimensional form:{leaf_id}",
            )
            continue

        require(
            classification in {"CLIPPED_2D_BOUNDARY_1D", "FULL_2D"}
            and leaf["two_dimensional_graph_sheet_count"] == 1
            and leaf["side_specific_signature_candidate_region_count"] == 2
            and leaf["candidate_region_signs"]
            == ["STRICT_NEGATIVE", "STRICT_POSITIVE"]
            and len(joined) == 2,
            f"nonempty sheet exact form:{leaf_id}",
        )
        owners = [row for row in joined if row["outgoing_cell"] in OWNER_CELLS]
        shadows = [
            row for row in joined if row["outgoing_cell"] in SHADOW_CELLS
        ]
        require(
            len(owners) == len(shadows) == 1,
            f"unique E/W owner and N/S shadow:{leaf_id}",
        )
        owner = owners[0]
        shadow = shadows[0]
        require(
            owner["F_sign"] == "STRICT_POSITIVE"
            and shadow["F_sign"] == "STRICT_NEGATIVE",
            f"owner/shadow strict F sides:{leaf_id}",
        )
        inactive_factors = {row["inactive_factor"] for row in joined}
        require(
            len(inactive_factors) == 1
            and next(iter(inactive_factors)) in FACTORS,
            f"unique inactive factor:{leaf_id}",
        )
        inactive_factor = next(iter(inactive_factors))
        active_factor = (
            "HMINUS" if inactive_factor == "HPLUS" else "HPLUS"
        )
        require(
            owner["whole_box_factor_C0"] == shadow["whole_box_factor_C0"],
            f"shared whole-box factor enclosure:{leaf_id}",
        )
        inactive_c0 = owner["whole_box_factor_C0"][inactive_factor]
        inactive_sign = inactive_c0["selected_sign"]
        require(
            inactive_sign in STRICT_SIGNS,
            f"inactive factor whole-box strict sign:{leaf_id}",
        )
        if (
            inactive_c0["direct_sign"] == inactive_sign
            and inactive_sign in STRICT_SIGNS
        ):
            c0_proof = "DIRECT_WHOLE_BOX_C0"
        else:
            require(
                inactive_c0["centered_sign"] == inactive_sign
                and inactive_sign in STRICT_SIGNS,
                f"inactive factor selected C0 source:{leaf_id}",
            )
            c0_proof = "CENTERED_WHOLE_BOX_C0"

        owner_cell = "E" if inactive_sign == "STRICT_POSITIVE" else "W"
        shadow_cell = expected_shadow_cell(active_factor, inactive_sign)
        require(
            owner["outgoing_cell"] == owner_cell
            and shadow["outgoing_cell"] == shadow_cell,
            f"factor-derived owner/shadow cells:{leaf_id}",
        )
        owner_pair = CELL_SIGNS[owner_cell]
        shadow_pair = CELL_SIGNS[shadow_cell]
        require(
            (owner["HPLUS_sign"], owner["HMINUS_sign"]) == owner_pair
            and (shadow["HPLUS_sign"], shadow["HMINUS_sign"]) == shadow_pair,
            f"strict sign-pair outgoing charts:{leaf_id}",
        )
        owner_active_sign = (
            owner["HPLUS_sign"]
            if active_factor == "HPLUS"
            else owner["HMINUS_sign"]
        )
        owner_inactive_sign = (
            owner["HPLUS_sign"]
            if inactive_factor == "HPLUS"
            else owner["HMINUS_sign"]
        )
        shadow_active_sign = (
            shadow["HPLUS_sign"]
            if active_factor == "HPLUS"
            else shadow["HMINUS_sign"]
        )
        shadow_inactive_sign = (
            shadow["HPLUS_sign"]
            if inactive_factor == "HPLUS"
            else shadow["HMINUS_sign"]
        )
        require(
            owner_active_sign == owner_inactive_sign == inactive_sign
            and shadow_inactive_sign == inactive_sign
            and shadow_active_sign == OPPOSITE_SIGN[inactive_sign],
            f"owner/shadow factor-side derivation:{leaf_id}",
        )

        owner_signature = owner["local_return_signature"]
        shadow_signature = shadow["local_return_signature"]
        owner_target_prefix = owner_signature["target_lift"].split("[", 1)[0]
        shadow_target_prefix = shadow_signature["target_lift"].split("[", 1)[0]
        require(
            owner_signature["outgoing_cell"] == owner_cell
            and shadow_signature["outgoing_cell"] == shadow_cell
            and owner_signature["target_chart"]
            == f"{owner_target_prefix}:{owner_cell}"
            and shadow_signature["target_chart"]
            == f"{shadow_target_prefix}:{shadow_cell}"
            and signature_core(owner_signature)
            == signature_core(shadow_signature),
            f"signature equality except outgoing cell/target chart:{leaf_id}",
        )
        core_sha256 = digest(signature_core(owner_signature))
        relation = (
            "HMINUS=2*Nx_ON_HPLUS_ZERO_SHEET"
            if active_factor == "HPLUS"
            else "HPLUS=2*Nx_ON_HMINUS_ZERO_SHEET"
        )
        identity_payload = {
            "leaf_row_id": leaf_id,
            "owner_region_row_id": owner["region_row_id"],
            "shadow_region_row_id": shadow["region_row_id"],
            "rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
        }
        sheet_row_id = lineage_id("half-open-sheet", identity_payload)
        sheet_row = closed_row({
            "sheet_row_id": sheet_row_id,
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
            "shadow_outgoing_cell": shadow_cell,
            "owner_signature_core_sha256": core_sha256,
            "shadow_signature_core_sha256": core_sha256,
            "signature_difference_field_allowlist": [
                "outgoing_cell",
                "target_chart",
            ],
            "Round173_half_open_rule":
                "E or W owns; N or S excludes",
            "deterministic_unique_owner_lineage": True,
            "incidence_is_not_a_global_component": True,
            "formal_half_open_owner_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        sheet_rows.append(sheet_row)

        owner_counts[owner_cell] += 1
        shadow_counts[shadow_cell] += 1
        pair_counts[f"{owner_cell}|{shadow_cell}"] += 1
        factor_sign_counts[f"{active_factor}|{inactive_sign}"] += 1
        c0_proof_counts[c0_proof] += 1
        signature_core_counts[core_sha256] += 1

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
                f"curve boundary endpoint pair:{leaf_id}:{side}",
            )
            curve_identity = {
                "sheet_row_id": sheet_row_id,
                "face_side": side,
                "boundary_edge_pair": boundary_pair,
                "graph_axis": face["graph_axis"],
                "provenance": face["provenance"],
            }
            curve_row_id = lineage_id(
                "half-open-curve-incidence",
                curve_identity,
            )
            curve_row = closed_row({
                "curve_row_id": curve_row_id,
                "sheet_row_id": sheet_row_id,
                "sheet_row_sha256": sheet_row["row_sha256"],
                "leaf_row_id": leaf_id,
                "face_side": side,
                "graph_axis": face["graph_axis"],
                "boundary_edge_pair": boundary_pair,
                "geometry_provenance": face["provenance"],
                "owner_region_row_id": owner["region_row_id"],
                "owner_outgoing_cell": owner_cell,
                "shadow_region_row_id": shadow["region_row_id"],
                "shadow_outgoing_cell": shadow_cell,
                "owner_signature_core_sha256": core_sha256,
                "deterministic_owner_lineage_inherited_from_sheet": True,
                "incidence_is_not_a_global_component": True,
                "formal_half_open_owner_credit": 0,
                "whole_original_tube_credit": 0,
                "global_exact_key_disposition_credit": 0,
            })
            curve_rows.append(curve_row)
            curve_pair_counts[boundary_pair] += 1
            curve_axis_counts[str(face["graph_axis"])] += 1
            curve_side_counts[side] += 1
            curve_provenance_counts[face["provenance"]] += 1

            for ordinal, boundary_edge in enumerate(boundary_edges, 1):
                leaf_endpoint_count += 1
                endpoint_identity = {
                    "curve_row_id": curve_row_id,
                    "endpoint_ordinal": ordinal,
                    "boundary_edge": boundary_edge,
                }
                endpoint_row = closed_row({
                    "endpoint_row_id": lineage_id(
                        "half-open-endpoint-incidence",
                        endpoint_identity,
                    ),
                    "curve_row_id": curve_row_id,
                    "curve_row_sha256": curve_row["row_sha256"],
                    "sheet_row_id": sheet_row_id,
                    "leaf_row_id": leaf_id,
                    "face_side": side,
                    "endpoint_ordinal": ordinal,
                    "boundary_edge": boundary_edge,
                    "owner_region_row_id": owner["region_row_id"],
                    "owner_outgoing_cell": owner_cell,
                    "shadow_region_row_id": shadow["region_row_id"],
                    "shadow_outgoing_cell": shadow_cell,
                    "owner_signature_core_sha256": core_sha256,
                    "deterministic_owner_lineage_inherited_from_curve":
                        True,
                    "incidence_is_not_a_global_component": True,
                    "formal_half_open_owner_credit": 0,
                    "whole_original_tube_credit": 0,
                    "global_exact_key_disposition_credit": 0,
                })
                endpoint_rows.append(endpoint_row)
        require(
            leaf_curve_count
            == leaf["one_dimensional_clipping_curve_segment_count"]
            and leaf_endpoint_count
            == leaf["zero_dimensional_boundary_endpoint_incidence_count"]
            and leaf_endpoint_count == 2 * leaf_curve_count,
            f"per-sheet dimensional lineage conservation:{leaf_id}",
        )

    sheet_rows.sort(key=lambda row: row["sheet_row_id"])
    curve_rows.sort(key=lambda row: row["curve_row_id"])
    endpoint_rows.sort(key=lambda row: row["endpoint_row_id"])
    require(
        len(sheet_rows) == EXPECTED_SHEETS
        and len({row["sheet_row_id"] for row in sheet_rows})
        == EXPECTED_SHEETS
        and len(curve_rows) == EXPECTED_CURVES
        and len({row["curve_row_id"] for row in curve_rows})
        == EXPECTED_CURVES
        and len(endpoint_rows) == EXPECTED_ENDPOINTS
        and len({row["endpoint_row_id"] for row in endpoint_rows})
        == EXPECTED_ENDPOINTS,
        "global dimensional lineage census and uniqueness",
    )
    require(
        digest(sheet_rows) == EXPECTED_SHEET_LINEAGE_ROWS_SHA256
        and digest(curve_rows) == EXPECTED_CURVE_LINEAGE_ROWS_SHA256
        and digest(endpoint_rows) == EXPECTED_ENDPOINT_LINEAGE_ROWS_SHA256,
        "exact deterministic dimensional lineage pins",
    )
    require(
        owner_counts == {"E": 8_858, "W": 8_858}
        and shadow_counts == {"N": 8_858, "S": 8_858}
        and pair_counts
        == {
            "E|N": 4_429,
            "E|S": 4_429,
            "W|N": 4_429,
            "W|S": 4_429,
        }
        and factor_sign_counts
        == {
            "HMINUS|STRICT_NEGATIVE": 4_429,
            "HMINUS|STRICT_POSITIVE": 4_429,
            "HPLUS|STRICT_NEGATIVE": 4_429,
            "HPLUS|STRICT_POSITIVE": 4_429,
        },
        "balanced owner/shadow factor census",
    )
    sheet_ids = {row["sheet_row_id"] for row in sheet_rows}
    curve_ids = {row["curve_row_id"] for row in curve_rows}
    require(
        all(row["sheet_row_id"] in sheet_ids for row in curve_rows)
        and all(
            row["sheet_row_id"] in sheet_ids
            and row["curve_row_id"] in curve_ids
            for row in endpoint_rows
        ),
        "complete curve/endpoint owner lineage joins",
    )
    require(
        all(
            row["formal_half_open_owner_credit"] == 0
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            and row["incidence_is_not_a_global_component"] is True
            for row in sheet_rows + curve_rows + endpoint_rows
        ),
        "all lineage rows zero-promotion",
    )
    audit = {
        "owner_outgoing_cell_count":
            dict(sorted(owner_counts.items())),
        "shadow_outgoing_cell_count":
            dict(sorted(shadow_counts.items())),
        "owner_shadow_pair_count":
            dict(sorted(pair_counts.items())),
        "active_factor_and_Nx_sign_count":
            dict(sorted(factor_sign_counts.items())),
        "inactive_factor_C0_proof_count":
            dict(sorted(c0_proof_counts.items())),
        "distinct_signature_core_count": len(signature_core_counts),
        "signature_core_multiplicity_histogram": {
            str(key): value
            for key, value in sorted(Counter(
                signature_core_counts.values()
            ).items())
        },
        "curve_boundary_edge_pair_count":
            dict(sorted(curve_pair_counts.items())),
        "curve_graph_axis_count":
            dict(sorted(curve_axis_counts.items())),
        "curve_face_side_count":
            dict(sorted(curve_side_counts.items())),
        "curve_geometry_provenance_count":
            dict(sorted(curve_provenance_counts.items())),
    }
    return sheet_rows, curve_rows, endpoint_rows, audit


def compact_ledger(
    rows: list[dict[str, Any]],
    id_key: str,
) -> dict[str, Any]:
    require(rows, f"nonempty compact ledger:{id_key}")
    row_hashes = [row["row_sha256"] for row in rows]
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest(row_hashes),
        "first_row": rows[0],
        "last_row": rows[-1],
        "every_row_closed_by_own_SHA256": all(
            digest({
                key: value
                for key, value in row.items()
                if key != "row_sha256"
            }) == row["row_sha256"]
            for row in rows
        ),
    }


def audit_u2(
    u2_rows: list[dict[str, Any]],
    sheet_rows: list[dict[str, Any]],
    curve_rows: list[dict[str, Any]],
    endpoint_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    sheet_by_leaf = {row["leaf_row_id"]: row for row in sheet_rows}
    u2_leaf_ids = {row["leaf_row_id"] for row in u2_rows}
    require(
        len(u2_leaf_ids) == EXPECTED_U2_SHEETS
        and len({row["origin_row_id"] for row in u2_rows})
        == EXPECTED_U2_ORIGINS
        and u2_leaf_ids <= set(sheet_by_leaf),
        "U|U sheet/origin join",
    )
    owner_counts: Counter[str] = Counter()
    active_counts: Counter[str] = Counter()
    active_owner_counts: Counter[str] = Counter()
    cross_status: Counter[str] = Counter()
    ordering: Counter[str] = Counter()
    curve_face_counts: Counter[str] = Counter()
    for row in u2_rows:
        sheet = sheet_by_leaf[row["leaf_row_id"]]
        owner = sheet["owner_outgoing_cell"]
        active = sheet["active_factor"]
        require(
            row["active_factor"] == active
            and row["curve_pair_nonintersection"] is True
            and row["local_geometric_residual"] is False
            and row["global_exact_key_disposition_credit"] == 0,
            f"U|U strict nonintersection:{row['leaf_row_id']}",
        )
        if row["curve_t_face_count"] == 2:
            require(
                row["cross_t_status"]
                == "TWO_CURVES_STRICTLY_ORDERED_AND_DISJOINT"
                and row["strict_curve_ordering"] in {
                    "UPPER_CURVE_STRICTLY_GREATER_P_THAN_LOWER_CURVE",
                    "UPPER_CURVE_STRICTLY_LESS_P_THAN_LOWER_CURVE",
                },
                f"U|U two-curve strict order:{row['leaf_row_id']}",
            )
        else:
            require(
                row["curve_t_face_count"] == 1
                and row["cross_t_status"]
                == "ONE_CURVE_OTHER_T_FACE_STRICTLY_ZERO_ABSENT"
                and row["strict_curve_ordering"] is None,
                f"U|U one-curve absence:{row['leaf_row_id']}",
            )
        owner_counts[owner] += 1
        active_counts[active] += 1
        active_owner_counts[f"{active}|{owner}"] += 1
        cross_status[row["cross_t_status"]] += 1
        ordering[str(row["strict_curve_ordering"])] += 1
        curve_face_counts[str(row["curve_t_face_count"])] += 1

    u2_curve_rows = [
        row for row in curve_rows if row["leaf_row_id"] in u2_leaf_ids
    ]
    u2_endpoint_rows = [
        row for row in endpoint_rows if row["leaf_row_id"] in u2_leaf_ids
    ]
    require(
        owner_counts == {"E": 44, "W": 44}
        and active_counts == {"HPLUS": 44, "HMINUS": 44}
        and active_owner_counts
        == {
            "HMINUS|E": 22,
            "HMINUS|W": 22,
            "HPLUS|E": 22,
            "HPLUS|W": 22,
        }
        and cross_status
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
        and curve_face_counts == {"1": 12, "2": 76}
        and len(u2_curve_rows) == EXPECTED_U2_CURVES
        and len(u2_endpoint_rows) == EXPECTED_U2_ENDPOINTS,
        "U|U exact balanced owner and ordering census",
    )
    return {
        "sheet_count": EXPECTED_U2_SHEETS,
        "distinct_origin_count": EXPECTED_U2_ORIGINS,
        "owner_outgoing_cell_count": dict(sorted(owner_counts.items())),
        "active_factor_count": dict(sorted(active_counts.items())),
        "active_factor_owner_cell_count":
            dict(sorted(active_owner_counts.items())),
        "cross_t_status_count": dict(sorted(cross_status.items())),
        "strict_curve_ordering_count": dict(sorted(ordering.items())),
        "curve_t_face_count": dict(sorted(curve_face_counts.items())),
        "1D_clipping_incidence_count": len(u2_curve_rows),
        "0D_endpoint_incidence_count": len(u2_endpoint_rows),
        "two_curve_pairs_strictly_ordered_and_disjoint": 76,
        "curve_pair_intersection_count": 0,
        "all_owner_lineages_joined": True,
    }


def build_result(probe_source_sha256: str) -> dict[str, Any]:
    print("Round209 validating pinned trust boundary", file=sys.stderr)
    r173, r208, input_hashes = validate_inputs()
    print("Round209 reconstructing Round195 geometry", file=sys.stderr)
    leaves, regions, _faces, u2_rows = validate_round195_geometry(r208)
    print("Round209 materializing deterministic owner lineages", file=sys.stderr)
    sheet_rows, curve_rows, endpoint_rows, owner_audit = build_lineages(
        leaves,
        regions,
    )
    print("Round209 auditing U|U ordering", file=sys.stderr)
    u2_audit = audit_u2(
        u2_rows,
        sheet_rows,
        curve_rows,
        endpoint_rows,
    )
    leaf_classes = Counter(
        row["final_graph_classification"] for row in leaves
    )
    dimension_totals = {
        "2D_sheet_count": sum(
            row["two_dimensional_graph_sheet_count"] for row in leaves
        ),
        "1D_clipping_incidence_count": sum(
            row["one_dimensional_clipping_curve_segment_count"]
            for row in leaves
        ),
        "0D_endpoint_incidence_count": sum(
            row["zero_dimensional_boundary_endpoint_incidence_count"]
            for row in leaves
        ),
    }
    require(
        leaf_classes
        == {
            "CLIPPED_2D_BOUNDARY_1D": 17_308,
            "EMPTY": EXPECTED_EMPTY_LEAVES,
            "FULL_2D": 408,
        }
        and dimension_totals
        == {
            "2D_sheet_count": EXPECTED_SHEETS,
            "1D_clipping_incidence_count": EXPECTED_CURVES,
            "0D_endpoint_incidence_count": EXPECTED_ENDPOINTS,
        }
        and EXPECTED_ENDPOINTS == 2 * EXPECTED_CURVES
        and EXPECTED_STRICT_REGIONS
        == EXPECTED_EMPTY_LEAVES + 2 * EXPECTED_SHEETS,
        "exact dimension-safe census",
    )
    source_safety = validate_source_has_no_write_surface(Path(__file__))
    return {
        "status": STATUS,
        "verdict": (
            "FEASIBLE_FOR_FORMALIZATION__EVERY_NONEMPTY_OUTGOING_W_LEAF_"
            "HAS_ONE_FACTOR_DERIVED_E_OR_W_OWNER_AND_ONE_N_OR_S_SHADOW"
        ),
        "probe_trust_boundary": {
            **input_hashes,
            "Round173_half_open_rule_used_as_frozen_input": True,
            "Round195_geometry_reconstructed_from_pinned_rows_carried_in_"
            "Round208": True,
            "Round208_certificate_used_as_trusted_formal_input": True,
            "Round208_producer_imported_or_executed": False,
            "Round195_probe_imported_or_executed": False,
            "trust_boundary_independently_reproved_here": False,
            "probe_is_formal_certificate": False,
        },
        "frozen_half_open_rule": {
            "rule": r173["outgoing_chart_contract"]["diagonal_seam_rule"],
            "owner_set": ["E", "W"],
            "shadow_or_excluded_set": ["N", "S"],
            "duplicate_trace_is_identified_not_added": True,
            "factorization": "F=(Nx+Ny)(Nx-Ny)=HPLUS*HMINUS",
            "active_HPLUS_zero_identity": "HMINUS=2*Nx",
            "active_HMINUS_zero_identity": "HPLUS=2*Nx",
            "owner_cell_from_inactive_factor_sign": {
                "STRICT_NEGATIVE": "W",
                "STRICT_POSITIVE": "E",
            },
            "all_sheet_owner_cells_derived_from_whole_box_strict_"
            "inactive_factor_sign": True,
        },
        "strict_region_pair_audit": {
            "nonempty_leaf_count": EXPECTED_SHEETS,
            "strict_region_pair_count": EXPECTED_SHEETS,
            "owner_region_count": EXPECTED_SHEETS,
            "shadow_region_count": EXPECTED_SHEETS,
            "unique_owner_per_nonempty_leaf": True,
            "unique_shadow_per_nonempty_leaf": True,
            "owner_is_E_or_W": True,
            "shadow_is_N_or_S": True,
            "owner_region_F_sign": "STRICT_POSITIVE",
            "shadow_region_F_sign": "STRICT_NEGATIVE",
            "signature_exact_equality_after_removing_only": [
                "outgoing_cell",
                "target_chart",
            ],
            "all_17716_signature_pairs_match_under_that_projection": True,
            **owner_audit,
        },
        "dimension_safe_materialized_lineage": {
            "input_leaf_classification_count":
                dict(sorted(leaf_classes.items())),
            "exact_dimension_count": dimension_totals,
            "endpoint_identity": "40912=2*20456",
            "strict_region_identity": "36040=608+2*17716",
            "sheet_owner_lineage":
                compact_ledger(sheet_rows, "sheet_row_id"),
            "curve_owner_lineage":
                compact_ledger(curve_rows, "curve_row_id"),
            "endpoint_owner_lineage":
                compact_ledger(endpoint_rows, "endpoint_row_id"),
            "all_curve_rows_join_exactly_one_sheet_owner_lineage": True,
            "all_endpoint_rows_join_exactly_one_curve_and_sheet_owner_"
            "lineage": True,
            "incidences_are_not_global_components": True,
        },
        "U_pipe_U_audit": u2_audit,
        "zero_promotion_contract": {
            "probe_only": True,
            "runtime_filesystem_writes": 0,
            "formal_half_open_owner_credit": 0,
            "whole_leaf_credit_issued": 0,
            "whole_origin_credit_issued": 0,
            "whole_original_tube_credit": 0,
            "global_component_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator":
                EXPECTED_SOURCE_G_EXACT_KEYS,
            "D02": "UNCHANGED_BLOCKED",
            "global_Gate5_fields": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
        },
        "output_safety": source_safety,
        "required_next": (
            "build a fresh formal producer and independent verifier that "
            "recompute these lower-dimensional owner lineages without "
            "treating 1D/0D incidences as global components; this read-only "
            "probe itself issues zero formal, whole-tube, or global credit"
        ),
        "provenance": {
            "schema": SCHEMA,
            "probe_source_sha256": probe_source_sha256,
            "python_version": sys.version.split()[0],
            "probe_only": True,
            "formal_upstream_files_modified": False,
        },
    }


def main() -> int:
    install_read_only_audit_hook()
    source_sha256 = pinned_regular_sha256(Path(__file__), maximum=5_000_000)
    result = build_result(source_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    sys.stdout.buffer.write(canonical_bytes(envelope) + b"\n")
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
