#!/usr/bin/env python3
"""Build the C55-A exact compact-atlas/BnB/glue snapshot.

This is deliberately a fail-closed evidence materializer.  C32 supplies an
exact s=0 compact cell complex, not a full R1648 continuation theorem.  The
only terminal dispositions emitted here are those selected by the installed
C53 GLOBAL_COMPOSITE authority.  Every other ordinary C32 cell remains
explicitly unresolved, even when it touches a geometric source-grazing face.

The producer never imports an older producer and never writes runtime state.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
CANDIDATES = RUNTIME / "candidates"

SCHEMA = "cm2.round306c55a.four-chart-fundamental-domain-bnb.v1"
LEAF_SCHEMA = SCHEMA + ".leaf"
BLOCKER_SCHEMA = SCHEMA + ".blocker"
GLUE_SCHEMA = SCHEMA + ".exact-glue"
RESULT_SCHEMA = SCHEMA + ".result"

LEAF_PATH = DELIVERABLES / "cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json"
GLUE_PATH = DELIVERABLES / "cm2_round306c55a_four_chart_fundamental_domain_exact_glue_ledger_v1.json"
RESULT_PATH = DELIVERABLES / "cm2_round306c55a_four_chart_fundamental_domain_bnb_result_v1.json"

EXPECTED_TOKENS = {
    32: "c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9",
    33: "c33-row-crosswalk-20260810T135223Z-eb0796f41e16d927",
    34: "c34-seed-event-frontier-20260810T142445Z-6ec6dac7de032cdb",
    37: "c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38",
    41: "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599",
    42: "c42-p391-formal-producer-20260811T044500Z-f1",
}
EXPECTED_OBJECTS = {
    32: "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474",
    33: "82dedeace982db89763e8a7e318fa6605d18cadc6bf390d6b23585d0922b87a0",
    34: "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e",
    37: "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b",
    41: "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
    42: "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2",
}

C53_HEAD_REL = (
    ".cm2-runtime/cm2-global-authority-heads/"
    "predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
)
C53_HEAD_FILE = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_HEAD_OBJECT = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"
C53_EFFECTIVE = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
C53_AUDIT_OBJECT = "a7bee7e57b6527c7bf9ea7f17966379c62a722fe9ce2ce2009f19f85a5afaa7c"
C53_AUDIT_REL = "deliverables/cm2_round306c53_d02a_pair1_pair_level_successor_independent_audit_v1.json"

C48_TOKEN = "c48-pair668-gen1-bbd909cad5a5-61de17d0a812-v1"
C48_OBJECT = "61de17d0a8122a4a03af34cf832cd717fdb715cd9c4cd2fac4162bdab8ddceab"
C48_RESULT_REL = (
    ".cm2-runtime/c48-successor-candidates/" + C48_TOKEN +
    "/candidate_result__cm2_round306c48_d02a_pair668_two_side_owner_closure_result_v1.json"
)

C50B_REL = "deliverables/cm2_round306c50b_d02b_global_cemetery_disconnected_exterior_oracle_contract_v1.json"
C50B_FILE = "25248a20e5a81f5119b204d856ef61ce18c2307412f3b304f2bb35213729ce1e"
C50B_OBJECT = "ddd1776bc133cac340b872f03325e97e8526a545e3e1a3fb11d56a159a4f9d97"
C55P0_REL = "deliverables/cm2_round306c55p0_global_strict_decider_input_contract_v1.json"
C55P0_FILE = "0e2a7b713f3c4c007c65a27a42079ca33b024b8489b5dfd149312fcd5702333b"

HISTORICAL_INPUTS = [
    ("deliverables/cm2_round162_exterior_frozen_prefix_pruning_certificate.json", "927bc20ca139e5bd1756c0b35bb10a8dbdddad1dde09bb4e6f2f3e73ddd88980", "9ee6d81996bc9c3886c3d48ac011b68e4ed51c7ea8ca6d34224d0911f9b39eb0", "FROZEN_PREFIX_NEGATIVE_FILTER_ALREADY_SUBSUMED_BY_C34"),
    ("deliverables/cm2_round162_exterior_unique_owner_pruning_certificate.json", "9cf6e0a65659a6c835e476d283b48d3fcd3b29f450ca2bf1b71d66dfb695f97f", "744ca0ca17bcb51077d154d1a3bb6b8055918acae519ad9c640b12bae54e2ea7", "FROZEN_PREFIX_UNIQUE_OWNER_FILTER_ALREADY_SUBSUMED_BY_C34"),
    ("deliverables/cm2_round177_tangency_boundary_and_source_seam_ledger_certificate.json", "8e0a7d3d093026932d847657d737f7f1dfc5aaea3727ff4d3e202728aa64c7cc", "9352f036325bc6e884fc6d31da2e1e2a04532d45fb11de90b3e5051103f56a9f", "EXACT_HALF_OPEN_SEAM_AND_TANGENCY_ZERO_WHOLE_PARENT_CREDIT"),
    ("deliverables/cm2_round178_later_return_exact_key_bridge_certificate.json", "31005b55c465db29e2e562ca8b94cde18b6c14fb830da7cbc6ef63d27a532f70", "c9da1d3312c4fe8253941e35e8113e1ac14e23e6ce58b7e0ff4ed2b0ebbda31b", "EXACT_SEAM_CORNER_COLLARS_BOUNDED_ONLY_ZERO_WHOLE_PARENT_CREDIT"),
]

TERMINALS = (
    "CONNECTED_TO_KNOWN",
    "EARLIEST_PREFIX_EXCLUDED",
    "SOURCE_GRAZING_OR_CEMETERY",
    "TYPED_EVENT_GRAPH",
)
GLOBAL_REQUIREMENTS = [
    "S0_TO_COMPLETE_CONTINUATION_BRIDGE",
    "GLOBAL_EXTERIOR_BNB_UNRESOLVED_ZERO",
    "GLOBAL_COMPONENT_ADJACENCY_AND_KNOWN_SHEET_ANCHOR",
    "NO_PRODUCER_GLOBAL_STRICT_DECIDER",
]
RULES = [
    "C34_SOURCE_W_FRONTIER",
    "C37_HORIZONTAL_REFLECTION",
    "C42_FORMAL_PARENT_CLOSURE",
    "C48_INSTALLED_TASK_LEVEL_CLOSURE_NO_WHOLE_PARENT_CREDIT",
    "C53_PAIR1_GLOBAL_COMPOSITE",
    "C34_KNOWN_ANCHOR_STRICT_SUBSET_ONLY",
    "ROUND162_FIXED_PREFIX_FILTER_ALREADY_SUBSUMED_NO_DOUBLE_CREDIT",
    "ROUND177_EXACT_HALF_OPEN_SEAM_ZERO_WHOLE_PARENT_CREDIT",
    "ROUND178_BOUNDED_COLLAR_ZERO_WHOLE_PARENT_CREDIT",
    "C32_SOURCE_GRAZING_GEOMETRY_ZERO_DYNAMIC_CREDIT",
    "C50B_POSITIVE_EXTERIOR_DISABLED",
]


ENCODER = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False,
)


def require(ok: bool, label: str) -> None:
    if not ok:
        raise RuntimeError(label)


def canonical_bytes(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    h = hashlib.sha256()
    for part in ENCODER.iterencode(value):
        h.update(part.encode("ascii"))
    return h.hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, f"duplicate-key:{path}:{key}")
            out[key] = value
        return out

    def no_float(token: str) -> None:
        raise RuntimeError(f"float-forbidden:{path}:{token}")

    with path.open("r", encoding="ascii", newline="") as f:
        value = json.load(f, object_pairs_hook=pairs, parse_float=no_float)
    require(type(value) is dict, f"object-required:{path}")
    return value


def verify_closed(value: dict[str, Any], field: str, expected: str | None = None) -> None:
    require(type(value.get(field)) is str, f"missing-self-hash:{field}")
    bare = dict(value)
    claimed = bare.pop(field)
    require(digest(bare) == claimed, f"self-hash:{field}")
    if expected is not None:
        require(claimed == expected, f"expected-self-hash:{field}")


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in value, "row-already-closed")
    return {**value, "row_sha256": digest(value)}


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    require("object_sha256" not in value, "object-already-closed")
    return {**value, "object_sha256": digest(value)}


def write_canonical_no_replace(path: Path, value: dict[str, Any]) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, 0o444)
    try:
        with os.fdopen(fd, "wb", closefd=False) as f:
            for part in ENCODER.iterencode(value):
                f.write(part.encode("ascii"))
            f.write(b"\n")
            f.flush()
            os.fsync(f.fileno())
    finally:
        os.close(fd)
    require(path.stat().st_nlink == 1, f"output-link-count:{path}")


def read_rows(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii", newline="") as f:
        for line in f:
            value = json.loads(line)
            require(type(value) is dict, f"row-object:{path}")
            yield value


def validate_source_row(row: dict[str, Any], path: Path) -> None:
    require(type(row.get("row_sha256")) is str, f"row-sha:{path}")
    bare = dict(row)
    claimed = bare.pop("row_sha256")
    require(digest(bare) == claimed, f"source-row-self-hash:{path}")


def candidate(n: int) -> Path:
    token_path = RUNTIME / f"c{n}-current-token"
    require(token_path.read_text(encoding="ascii").strip() == EXPECTED_TOKENS[n], f"token-c{n}")
    return CANDIDATES / EXPECTED_TOKENS[n]


def load_result(n: int) -> tuple[Path, dict[str, Any]]:
    directory = candidate(n)
    value = strict_json(directory / "result.json")
    verify_closed(value, "object_sha256", EXPECTED_OBJECTS[n])
    return directory, value


def checked_rows(directory: Path, result: dict[str, Any], descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    path = directory / descriptor["filename"]
    require(file_sha(path) == descriptor["sha256"], f"ledger-file:{path}")
    rows = list(read_rows(path))
    require(len(rows) == descriptor["row_count"], f"ledger-count:{path}")
    for row in rows:
        validate_source_row(row, path)
    seq = hashlib.sha256("".join(row["row_sha256"] + "\n" for row in rows).encode("ascii")).hexdigest()
    require(seq == descriptor["row_hash_line_sequence_sha256"], f"ledger-sequence:{path}")
    return rows


def asset(path: Path, role: str, object_sha256: str | None = None) -> dict[str, Any]:
    return {
        "file_sha256": file_sha(path),
        "object_sha256": object_sha256,
        "path": str(path.relative_to(ROOT)),
        "role": role,
    }


def authority_binding() -> dict[str, Any]:
    return {
        "C32_object_sha256": EXPECTED_OBJECTS[32],
        "C33_object_sha256": EXPECTED_OBJECTS[33],
        "C34_object_sha256": EXPECTED_OBJECTS[34],
        "C37_object_sha256": EXPECTED_OBJECTS[37],
        "C53_effective_checkpoint_object_sha256": C53_EFFECTIVE,
        "C53_global_head_file_sha256": C53_HEAD_FILE,
        "C53_global_head_object_sha256": C53_HEAD_OBJECT,
        "C53_global_head_path": C53_HEAD_REL,
        "C53_independent_audit_object_sha256": C53_AUDIT_OBJECT,
    }


def normalize_glue(source: dict[str, Any], ordinal: int, family: str) -> dict[str, Any]:
    bare = dict(source)
    source_sha = bare.pop("row_sha256")
    bare["ordinal"] = ordinal
    bare["source_row_sha256"] = source_sha
    row = close_row(bare)
    expected_keys = {
        "intra_faces": {"axis", "classification", "compact_chart", "coordinate", "dimension", "face_id", "negative_cell_id", "ordinal", "positive_cell_id", "row_sha256", "source_row_sha256", "span"},
        "source_seams": {"classification", "dimension", "exact_state_gluing_inherited_from_round162", "face_id", "left_cell_id", "left_chart", "left_compact_endpoint", "ordinal", "physical_p_span", "right_cell_id", "right_chart", "right_compact_endpoint", "row_sha256", "seam_id", "source_row_sha256", "terminal"},
        "source_grazing_faces": {"classification", "compact_chart", "compact_q", "dimension", "face_id", "incident_cell_id", "ordinal", "physical_p", "physical_t_span", "round144_dynamic_cemetery_credit", "row_sha256", "source_row_sha256", "terminal_for_compact_geometry"},
        "source_grazing_corners": {"classification", "compact_q", "corner_id", "dimension", "left_cell_id", "ordinal", "physical_p", "right_cell_id", "round144_dynamic_cemetery_credit", "row_sha256", "seam_id", "source_row_sha256", "terminal_for_compact_geometry"},
    }[family]
    require(set(row) == expected_keys, f"glue-schema:{family}")
    return row


def rational_value(endpoint: dict[str, Any]) -> Fraction:
    require(endpoint == {"kind": "RATIONAL", "value": endpoint.get("value")}, "rational-endpoint")
    return Fraction(endpoint["value"])


def validate_seam_coverage(rows: list[dict[str, Any]]) -> bool:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[row["seam_id"]].append(row)
    require(set(groups) == {"E_TO_N", "N_TO_W", "W_TO_S", "S_TO_E"}, "seam-cycle")
    for seam_rows in groups.values():
        intervals = sorted((rational_value(r["physical_p_span"][0]), rational_value(r["physical_p_span"][1])) for r in seam_rows)
        require(intervals[0][0] == -1 and intervals[-1][1] == 1, "seam-endpoints")
        require(all(a[1] == b[0] and a[0] < a[1] for a, b in zip(intervals, intervals[1:])), "seam-partition")
    return True


def validate_grazing_coverage(rows: list[dict[str, Any]]) -> bool:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        require(row["round144_dynamic_cemetery_credit"] == 0, "grazing-no-dynamic-credit")
        groups[(row["compact_chart"], row["compact_q"])].append(row)
    require(set(groups) == {(c, q) for c in "ENWS" for q in ("-1", "1")}, "grazing-groups")
    neg = {"isolating_interval": ["-708/1000", "-707/1000"], "kind": "ALGEBRAIC", "minimal_polynomial": "2*x^2-1", "value": "-1/sqrt(2)"}
    pos = {"isolating_interval": ["707/1000", "708/1000"], "kind": "ALGEBRAIC", "minimal_polynomial": "2*x^2-1", "value": "+1/sqrt(2)"}
    for group in groups.values():
        require(len(group) == 128, "grazing-group-count")
        by_low = {digest(r["physical_t_span"][0]): r for r in group}
        cursor = neg
        seen = 0
        while cursor != pos:
            row = by_low.get(digest(cursor))
            require(row is not None, "grazing-gap")
            cursor = row["physical_t_span"][1]
            seen += 1
        require(seen == 128, "grazing-cycle")
    return True


def build() -> dict[str, Any]:
    require(not LEAF_PATH.exists() and not GLUE_PATH.exists() and not RESULT_PATH.exists(), "C55A-output-exists")
    directories: dict[int, Path] = {}
    results: dict[int, dict[str, Any]] = {}
    for n in EXPECTED_TOKENS:
        directories[n], results[n] = load_result(n)

    head_path = ROOT / C53_HEAD_REL
    require(file_sha(head_path) == C53_HEAD_FILE, "C53-head-file")
    head = strict_json(head_path)
    verify_closed(head, "authority_seal_object_sha256", C53_HEAD_OBJECT)
    require(head["authority_role"] == "GLOBAL_COMPOSITE", "C53-head-role")
    require(head["post_seal_effective_checkpoint_object_sha256"] == C53_EFFECTIVE, "C53-effective")

    audit_path = ROOT / C53_AUDIT_REL
    audit = strict_json(audit_path)
    verify_closed(audit, "object_sha256", C53_AUDIT_OBJECT)
    projections = audit["post_seal_promotion_derivation"]["parent_projections"]
    require(len(projections) == 862, "C53-projection-count")
    projection_by_pair = {row["pair_index"]: row for row in projections}
    require(set(projection_by_pair) == set(range(862)), "C53-projection-index")
    for row in projections:
        bare = dict(row)
        claimed = bare.pop("projection_object_sha256")
        require(digest(bare) == claimed, "C53-projection-self-hash")

    c48_path = ROOT / C48_RESULT_REL
    c48 = strict_json(c48_path)
    verify_closed(c48, "object_sha256", C48_OBJECT)
    c48_closed_ambient = c48["selection"]["ambient_cell_id"]
    require(c48["selection"]["pair_index"] == 668, "C48-pair")

    c50b_path = ROOT / C50B_REL
    require(file_sha(c50b_path) == C50B_FILE, "C50b-file")
    c50b = strict_json(c50b_path)
    verify_closed(c50b, "object_sha256", C50B_OBJECT)
    require(c50b["positive_terminal_enabled"] is False, "C50b-positive-disabled")
    require(c50b["approved_global_decider_source_sha256"] is None, "C50b-decider-null")
    require(file_sha(ROOT / C55P0_REL) == C55P0_FILE, "C55p0-file")

    history_assets: list[dict[str, Any]] = []
    for rel, expected_file, expected_result, role in HISTORICAL_INPUTS:
        path = ROOT / rel
        require(file_sha(path) == expected_file, f"historical-file:{rel}")
        value = strict_json(path)
        require(value.get("result_sha256") == expected_result, f"historical-result:{rel}")
        require(digest(value["result"]) == expected_result, f"historical-self-hash:{rel}")
        history_assets.append(asset(path, role, expected_result))

    c32_ledgers = results[32]["ledgers"]
    source_cells = checked_rows(directories[32], results[32], c32_ledgers["cells"])
    require(len(source_cells) == 76832, "C32-cell-count")
    cells: list[dict[str, Any]] = []
    cell_by_id: dict[str, dict[str, Any]] = {}
    for row in source_cells:
        compact = {
            "cell_id": row["cell_id"],
            "origin_key": row["origin_key"],
            "physical_chart": row["compact_chart"],
            "source_cell_row_sha256": row["row_sha256"],
            "exact_box": {
                "physical_p_interval": row["physical_p_interval"],
                "physical_slice": row["physical_slice"],
                "physical_t_interval": row["physical_t_interval"],
            },
        }
        require(compact["cell_id"] not in cell_by_id, "duplicate-cell")
        cells.append(compact)
        cell_by_id[compact["cell_id"]] = compact
    del source_cells

    refs: dict[str, dict[str, list[int]]] = {
        cell_id: {
            "intra_face_ordinals": [],
            "source_grazing_corner_ordinals": [],
            "source_grazing_face_ordinals": [],
            "source_seam_ordinals": [],
        }
        for cell_id in cell_by_id
    }
    glue_rows: dict[str, list[dict[str, Any]]] = {}
    glue_specs = [
        ("intra_faces", "intra_chart_adjacency", ("negative_cell_id", "positive_cell_id"), "intra_face_ordinals"),
        ("source_seams", "source_chart_seams", ("left_cell_id", "right_cell_id"), "source_seam_ordinals"),
        ("source_grazing_faces", "grazing", ("incident_cell_id",), "source_grazing_face_ordinals"),
        ("source_grazing_corners", "corners", ("left_cell_id", "right_cell_id"), "source_grazing_corner_ordinals"),
    ]
    all_refs_exist = True
    for family, descriptor_key, incident_fields, ref_key in glue_specs:
        source = checked_rows(directories[32], results[32], c32_ledgers[descriptor_key])
        normalized: list[dict[str, Any]] = []
        for ordinal, row in enumerate(source):
            out = normalize_glue(row, ordinal, family)
            normalized.append(out)
            for field in incident_fields:
                cell_id = row[field]
                if cell_id not in refs:
                    all_refs_exist = False
                else:
                    refs[cell_id][ref_key].append(ordinal)
        glue_rows[family] = normalized

    require(all_refs_exist, "glue-cell-foreign-key")
    require(len(glue_rows["intra_faces"]) == 161586, "intra-count")
    require(len(glue_rows["source_seams"]) == 888, "seam-count")
    require(len(glue_rows["source_grazing_faces"]) == 1024, "grazing-count")
    require(len(glue_rows["source_grazing_corners"]) == 8, "corner-count")
    seam_complete = validate_seam_coverage(glue_rows["source_seams"])
    grazing_complete = validate_grazing_coverage(glue_rows["source_grazing_faces"])

    binding = authority_binding()
    source_assets = [
        asset(directories[n] / "result.json", f"C{n}_RESULT", EXPECTED_OBJECTS[n])
        for n in sorted(EXPECTED_TOKENS)
    ] + [
        asset(head_path, "INSTALLED_C53_GLOBAL_COMPOSITE_HEAD", C53_HEAD_OBJECT),
        asset(audit_path, "C53_NO_PRODUCER_INDEPENDENT_AUDIT", C53_AUDIT_OBJECT),
        asset(c48_path, "INSTALLED_C48_TASK_LEVEL_OVERLAY", C48_OBJECT),
        asset(c50b_path, "POSITIVE_EXTERIOR_DISABLED_CONTRACT", C50B_OBJECT),
        asset(ROOT / C55P0_REL, "C55_SHARED_STRICT_DECIDER_INPUT_CONTRACT", None),
    ] + history_assets

    glue_bare = {
        "authority_binding": binding,
        "coverage": {
            "all_corner_cells_exist": all_refs_exist,
            "all_face_cells_exist": all_refs_exist,
            "cell_count": 76832,
            "corner_count": 8,
            "grazing_face_count": 1024,
            "intra_face_count": 161586,
            "leaf_glue_refs_bidirectional": True,
            "source_grazing_boundary_complete": grazing_complete,
            "source_seam_count": 888,
            "source_seam_cyclic_span_complete": seam_complete,
            "unexpected_or_missing_cell_reference_count": 0,
        },
        "exact_gluing_model": {
            "chart_cycle": ["E", "N", "W", "S", "E"],
            "compact_domain": "S1_A_x_[-1,1]_p_at_s=0",
            "kappa_minimal_polynomial": "kappa^2+2*kappa-1",
            "source_chart_gluing": ["E:+kappa=N:-kappa", "N:+kappa=W:-kappa", "W:+kappa=S:-kappa", "S:+kappa=E:-kappa"],
            "source_grazing_rule": "p=+/-1_is_compact_geometric_boundary_only__dynamic_cemetery_credit_zero",
        },
        "glue_rows": glue_rows,
        "row_order": {
            "intra_faces": "C32_SOURCE_ORDER",
            "source_grazing_corners": "C32_SOURCE_ORDER",
            "source_grazing_faces": "C32_SOURCE_ORDER",
            "source_seams": "C32_SOURCE_ORDER",
        },
        "schema": GLUE_SCHEMA,
        "source_assets": source_assets,
        "status": "EXACT_C32_S0_CELL_COMPLEX_GLUE_MATERIALIZED__ZERO_DYNAMIC_CEMETERY_CREDIT",
    }
    glue = close_object(glue_bare)
    write_canonical_no_replace(GLUE_PATH, glue)
    glue_file = file_sha(GLUE_PATH)
    del glue_rows, glue

    frontier_rows = checked_rows(directories[34], results[34], results[34]["ledgers"]["terminal_frontier"])
    frontier_by_cell = {row["cell_id"]: row for row in frontier_rows}
    require(set(frontier_by_cell) == set(cell_by_id), "frontier-cell-set")
    typed_rows = checked_rows(directories[34], results[34], results[34]["ledgers"]["typed_first_event_bindings"])
    typed_by_cell = {row["cell_id"]: row for row in typed_rows}
    component_rows = checked_rows(directories[34], results[34], results[34]["ledgers"]["ordinary_components"])
    component_by_index = {row["component_index"]: row for row in component_rows}

    pair_rows = checked_rows(directories[37], results[37], results[37]["ledgers"]["ordinary_cell_reflection_pairs"])
    pair_by_cell: dict[str, tuple[dict[str, Any], str, str]] = {}
    for row in pair_rows:
        pair_by_cell[row["representative_cell_id"]] = (row, "REPRESENTATIVE", row["reflected_cell_id"])
        pair_by_cell[row["reflected_cell_id"]] = (row, "REFLECTED", row["representative_cell_id"])
    require(len(pair_by_cell) == 1724, "pair-cell-count")

    c42_rows = checked_rows(directories[42], results[42], results[42]["ledgers"]["parent_conservation"])
    c42_by_pair = {row["pair_index"]: row for row in c42_rows}
    require(set(c42_by_pair) == set(range(862)), "C42-pair-index")
    for i, projection in projection_by_pair.items():
        require(projection["C42_parent_row_sha256"] == c42_by_pair[i]["row_sha256"], "C53-C42-bind")

    ambient_desc = results[41]["ledgers"]["routed_ambient_cells"]
    ambient_path = directories[41] / ambient_desc["filename"]
    require(file_sha(ambient_path) == ambient_desc["sha256"], "C41-ambient-file")
    residual_counts: dict[int, Counter[str]] = defaultdict(Counter)
    residual_hashes: dict[int, list[str]] = defaultdict(list)
    residual_seen = 0
    for row in read_rows(ambient_path):
        validate_source_row(row, ambient_path)
        residual = row["residual_classification"]
        if residual is None:
            continue
        residual_seen += 1
        pair_index = row["pair_index"]
        if projection_by_pair[pair_index]["after_whole_representative"]:
            continue
        if row["c41_ambient_cell_id"] == c48_closed_ambient:
            require(pair_index == 668, "C48-ambient-pair")
            continue
        residual_counts[pair_index][residual] += 1
        residual_hashes[pair_index].append(row["row_sha256"])
    require(residual_seen == 33642, "C41-residual-source-count")
    require(sum(map(len, residual_hashes.values())) == 33638, "post-C53-logical-pending-count")

    blocker_rows: list[dict[str, Any]] = []
    blocker_by_pair: dict[int, dict[str, Any]] = {}
    primary_partition: Counter[str] = Counter()
    for pair_index in range(862):
        projection = projection_by_pair[pair_index]
        if projection["after_whole_representative"]:
            continue
        pair = pair_rows[pair_index]
        counts = residual_counts[pair_index]
        require(counts, f"missing-residuals:{pair_index}")
        maximum = max(counts.values())
        primary = min(key for key, value in counts.items() if value == maximum)
        key = {
            "pair_index": pair_index,
            "primary_residual_classification": primary,
            "representative_cell_id": pair["representative_cell_id"],
            "reflected_cell_id": pair["reflected_cell_id"],
        }
        blocker_id = "c55a-blocker:" + digest(key)
        bare = {
            "blocker_row_id": blocker_id,
            "c37_reflection_row_sha256": pair["row_sha256"],
            "c42_parent_row_sha256": c42_by_pair[pair_index]["row_sha256"],
            "c53_projection_object_sha256": projection["projection_object_sha256"],
            "current_nonterminal_leaf_count": projection["after_nonterminal_leaf_count"],
            "current_unresolved_parent_volume": projection["after_unresolved_parent_volume"],
            "global_missing_requirement_ids": GLOBAL_REQUIREMENTS,
            "pair_index": pair_index,
            "primary_residual_classification": primary,
            "reflected_cell_id": pair["reflected_cell_id"],
            "representative_cell_id": pair["representative_cell_id"],
            "residual_classification_census": dict(sorted(counts.items())),
            "residual_source_row_sha256s": sorted(residual_hashes[pair_index]),
            "schema": BLOCKER_SCHEMA,
        }
        closed = close_row(bare)
        blocker_rows.append(closed)
        blocker_by_pair[pair_index] = closed
        primary_partition[primary] += 2
    require(len(blocker_rows) == 574 and sum(primary_partition.values()) == 1148, "blocker-count")

    seed_path = directories[34] / "r1648_seed_crosswalk.json"
    seed = strict_json(seed_path)
    seed_file_sha = file_sha(seed_path)
    require(seed["coarse_cell_is_not_promoted_to_connected"] is True, "seed-nonpromotion")
    seed_cell = seed["cell_id"]

    rules_digest = digest(RULES)
    leaves: list[dict[str, Any]] = []
    census: Counter[str] = Counter()
    for ordinal, cell in enumerate(cells):
        cell_id = cell["cell_id"]
        frontier = frontier_by_cell[cell_id]
        initial = frontier["terminal_class"]
        pair_info = pair_by_cell.get(cell_id)
        terminal: str | None
        unresolved: str | None
        component_ref: dict[str, Any] | None
        reflection_ref: dict[str, Any] | None
        pair_index: int | None
        projection: dict[str, Any] | None
        if initial == "EARLIEST_PREFIX_EXCLUDED":
            terminal, unresolved = initial, None
            pair_index = None
            projection = None
            component_ref = None
            reflection_ref = None
            proof_authority = "C34_FRONTIER"
            primary_evidence = frontier["row_sha256"]
        elif initial == "TYPED_EVENT_GRAPH":
            terminal, unresolved = initial, None
            pair_index = None
            projection = None
            component_ref = None
            reflection_ref = None
            proof_authority = "C34_FRONTIER"
            primary_evidence = frontier["row_sha256"]
            require(cell_id in typed_by_cell, "typed-binding")
        else:
            require(initial == "UNRESOLVED_R1648_CONTINUATION", "unexpected-frontier-class")
            require(pair_info is not None, "ordinary-pair-missing")
            pair, role, partner = pair_info
            pair_index = pair["pair_index"]
            projection = projection_by_pair[pair_index]
            component_index = pair["representative_component_index"] if role == "REPRESENTATIVE" else pair["reflected_component_index"]
            component = component_by_index[component_index]
            component_ref = {
                "cell_role": role,
                "component_id": component["component_id"],
                "component_index": component_index,
                "component_row_sha256": component["row_sha256"],
            }
            reflection_ref = {
                "C37_row_sha256": pair["row_sha256"],
                "pair_index": pair_index,
                "partner_cell_id": partner,
                "role": role,
            }
            if projection["after_whole_representative"]:
                terminal, unresolved = "EARLIEST_PREFIX_EXCLUDED", None
                proof_authority = "C53_GLOBAL_COMPOSITE"
                primary_evidence = projection["projection_object_sha256"]
            else:
                terminal = None
                blocker = blocker_by_pair[pair_index]
                unresolved = "C55A_GLOBAL_DECIDER_BLOCKED:" + blocker["primary_residual_classification"] + ":" + blocker["blocker_row_id"]
                proof_authority = None
                primary_evidence = None

        if terminal is None:
            census["UNRESOLVED_R1648_CONTINUATION"] += 1
        else:
            require(terminal in TERMINALS, "terminal-enum")
            census[terminal] += 1

        is_seed = cell_id == seed_cell
        blocker_id = blocker_by_pair[pair_index]["blocker_row_id"] if terminal is None and pair_index is not None else None
        row = {
            "anchor_or_exterior_proof": {
                "C34_seed_crosswalk_sha256": seed_file_sha if is_seed else None,
                "C50b_contract_object_sha256": C50B_OBJECT,
                "kind": "KNOWN_ANCHOR_STRICT_SUBSET_ONLY" if is_seed else "NO_POSITIVE_ANCHOR_OR_EXTERIOR_PROOF",
                "known_anchor_status": "STRICT_SUBSET_DOES_NOT_PROMOTE_COARSE_LEAF" if is_seed else "NOT_APPLICABLE_NO_POSITIVE_PROOF",
                "strict_exterior_decider_object_sha256": None,
            },
            "bnb_state": {
                "base_leaf_is_full_continuation_proof": False,
                "blocker_row_id": blocker_id,
                "current_after_nonterminal_leaf_count": projection["after_nonterminal_leaf_count"] if projection else 0,
                "current_after_unresolved_parent_volume": projection["after_unresolved_parent_volume"] if projection else "0",
                "depth_cap_terminal_used": False,
                "pair_index": pair_index,
                "reusable_rule_sequence_sha256": rules_digest,
            },
            "c34_frontier_row_sha256": frontier["row_sha256"],
            "cell_id": cell_id,
            "component_ref": component_ref,
            "exact_box": cell["exact_box"],
            "glue_refs": refs[cell_id],
            "leaf_ordinal": ordinal,
            "origin_key": cell["origin_key"],
            "physical_chart": cell["physical_chart"],
            "proof_ref": {
                "C34_typed_event_row_sha256": typed_by_cell[cell_id]["row_sha256"] if cell_id in typed_by_cell else None,
                "C53_parent_projection_object_sha256": projection["projection_object_sha256"] if projection else None,
                "authority": proof_authority,
                "primary_evidence_row_sha256": primary_evidence,
            },
            "reflection_pair_ref": reflection_ref,
            "schema": LEAF_SCHEMA,
            "source_cell_row_sha256": cell["source_cell_row_sha256"],
            "terminal_disposition": terminal,
            "unresolved_reason": unresolved,
        }
        leaves.append(close_row(row))

    expected_census = {
        "CONNECTED_TO_KNOWN": 0,
        "EARLIEST_PREFIX_EXCLUDED": 75388,
        "SOURCE_GRAZING_OR_CEMETERY": 0,
        "TYPED_EVENT_GRAPH": 296,
        "UNRESOLVED_R1648_CONTINUATION": 1148,
    }
    require(dict(census) == {k: v for k, v in expected_census.items() if v}, "C55A-census")
    census_closed = {**expected_census, "total": 76832, "unresolved_zero": False}
    leaf_bare = {
        "authority_binding": binding,
        "blocker_partition": {
            "by_primary_residual_classification": dict(sorted(primary_partition.items())),
            "global_requirement_blockers": GLOBAL_REQUIREMENTS,
            "new_terminals_by_C55A": 0,
            "remaining_unresolved": 1148,
        },
        "blocker_rows": blocker_rows,
        "census": census_closed,
        "leaf_order": "C32_LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
        "leaves": leaves,
        "proof_policy": {
            "allowed_terminal_dispositions": list(TERMINALS),
            "depth_cap_terminal_forbidden": True,
            "geometric_grazing_is_dynamic_cemetery_credit": False,
            "local_chart_exit_is_terminal": False,
            "null_disposition_rule": "terminal_disposition_is_null_iff_unresolved_reason_is_nonempty",
            "positive_exterior_requires_unresolved_zero": True,
            "reusable_rule_order": RULES,
            "reusable_rule_sequence_sha256": rules_digest,
        },
        "schema": SCHEMA + ".leaf-ledger",
        "source_assets": source_assets + [
            asset(seed_path, "C34_KNOWN_ANCHOR_STRICT_SUBSET_ONLY", None),
            asset(ambient_path, "C41_RECONSTRUCTIBLE_RESIDUAL_BLOCKER_ROWS", None),
        ],
        "status": "FULL_76832_S0_ATLAS_AND_FORMAL_DISPOSITION_OVERLAY__1148_EXPLICITLY_UNRESOLVED__ZERO_NEW_TERMINALS",
    }
    leaf_ledger = close_object(leaf_bare)
    write_canonical_no_replace(LEAF_PATH, leaf_ledger)
    leaf_file = file_sha(LEAF_PATH)

    result_bare = {
        "authority_binding": binding,
        "bnb": {
            "blocker_row_count": 574,
            "leaf_count": 76832,
            "leaf_ledger_file_sha256": leaf_file,
            "leaf_ledger_object_sha256": leaf_ledger["object_sha256"],
            "new_terminal_leaf_count": 0,
            "remaining_unresolved_leaf_count": 1148,
            "s0_base_atlas_is_full_continuation_proof": False,
            "unresolved_zero": False,
        },
        "formal_credit": {
            "D02_gate_credit": 0,
            "formal_credit": 0,
            "source_grazing_or_cemetery_new_credit": 0,
        },
        "glue": {
            "corner_count": 8,
            "exact_glue_ledger_file_sha256": glue_file,
            "exact_glue_ledger_object_sha256": glue_bare["object_sha256"] if "object_sha256" in glue_bare else digest(glue_bare),
            "grazing_face_count": 1024,
            "intra_face_count": 161586,
            "source_seam_count": 888,
        },
        "required_next": GLOBAL_REQUIREMENTS,
        "schema": RESULT_SCHEMA,
        "source_assets": source_assets,
        "status": "FAIL_CLOSED_GLOBAL_BNB_MATERIALIZED_WITH_1148_UNRESOLVED__NO_GLOBAL_STRICT_DECIDER",
    }
    result = close_object(result_bare)
    write_canonical_no_replace(RESULT_PATH, result)
    return result


def self_test() -> dict[str, Any]:
    tests = 0
    sample = close_row({"a": 1, "b": None})
    require(sample["row_sha256"] == digest({"a": 1, "b": None}), "self-row")
    tests += 1
    obj = close_object({"z": [1, 2], "a": True})
    verify_closed(obj, "object_sha256")
    tests += 1
    require(digest(RULES) == digest(list(RULES)), "self-rules")
    tests += 1
    require(set(TERMINALS) == {"CONNECTED_TO_KNOWN", "EARLIEST_PREFIX_EXCLUDED", "SOURCE_GRAZING_OR_CEMETERY", "TYPED_EVENT_GRAPH"}, "self-enum")
    tests += 1
    require(C53_EFFECTIVE != C53_HEAD_OBJECT, "self-role-separation")
    tests += 1
    require(len(GLOBAL_REQUIREMENTS) == 4, "self-global-blockers")
    tests += 1
    require(Fraction("-1") < Fraction("1"), "self-fraction")
    tests += 1
    require(canonical_bytes({"b": 2, "a": 1}) == b'{"a":1,"b":2}', "self-canonical")
    tests += 1
    return {"status": "PASS", "tests_passed": tests, "tests_total": tests}


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--build", action="store_true")
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    value = self_test() if args.self_test else build()
    print(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True))


if __name__ == "__main__":
    main()
